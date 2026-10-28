import unittest
from tkinter import ttk
from unittest.mock import Mock, patch

from controllers.gui.gui_student_controller import GUIStudentController
from controllers.gui.gui_uni_app import GUIUniApp
from models.student import Student
from models.subject import Subject
from views.gui.account_view import AccountView
from views.gui.gui_student.dashboard_view import DashboardView
from views.gui.login_view import LoginView
from views.gui.gui_student.registration_view import RegistrationView
from views.gui.main_view import MainView
from views.gui.gui_student.subjects_view import SubjectsView


class TestStudentGUIViews(unittest.TestCase):
    def setUp(self):
        # Keep these callback tests runnable without a desktop display.
        frame_init = patch.object(ttk.Frame, "__init__", return_value=None)
        frame_init.start()
        self.addCleanup(frame_init.stop)
        self.widgets = {}
        for name in ("Frame", "LabelFrame", "Label", "Entry", "Button", "Separator", "Style"):
            widget = patch.object(ttk, name)
            self.widgets[name] = widget.start()
            self.addCleanup(widget.stop)
        self.student = Student("00000001", "Test Student", "test@student.uts.edu.au", "OldPass1!")

    def test_auth_forms_preserve_input_order_and_password_masking(self):
        for view_class, values, button_text in (
            (LoginView, [" test@student.uts.edu.au ", " Password1! "], "Login"),
            (RegistrationView, [" Test Student ", "test@student.uts.edu.au", "Password1!"], "Register")
        ):
            with self.subTest(view=view_class.__name__):
                self.widgets["Entry"].reset_mock()
                self.widgets["Button"].reset_mock()
                self.widgets["Entry"].side_effect = [Mock(get=Mock(return_value=value)) for value in values]
                callback = Mock()
                if view_class is LoginView:
                    view_class(None, "Student Login", callback, Mock(), Mock())
                else:
                    view_class(None, callback, Mock())
                button = next(call for call in self.widgets["Button"].call_args_list if call.kwargs["text"] == button_text)
                button.kwargs["command"]()
                callback.assert_called_once_with(*values)
                masks = [call.kwargs.get("show", "") for call in self.widgets["Entry"].call_args_list]
                self.assertEqual(masks, [""] * (len(values) - 1) + ["*"])

    def test_shared_login_keeps_registration_student_only(self):
        for role in ("Student", "Admin"):
            with self.subTest(role=role):
                self.widgets["Button"].reset_mock()
                self.widgets["Label"].reset_mock()
                self.widgets["Entry"].side_effect = [
                    Mock(get=Mock(return_value="example@university.com")),
                    Mock(get=Mock(return_value="Password123"))
                ]
                login, back, register = Mock(), Mock(), Mock()
                LoginView(
                    None, f"{role} Login", login, back,
                    register if role == "Student" else None
                )
                buttons = {
                    call.kwargs["text"]: call.kwargs["command"]
                    for call in self.widgets["Button"].call_args_list
                }
                self.assertEqual(set(buttons), {"Login", "Register", "Back"}
                                 if role == "Student" else {"Login", "Back"})
                buttons["Login"]()
                login.assert_called_once_with("example@university.com", "Password123")
                buttons["Back"]()
                back.assert_called_once_with()
                if role == "Student":
                    buttons["Register"]()
                    register.assert_called_once_with()
                self.assertIn(f"{role} Login", [
                    call.kwargs["text"] for call in self.widgets["Label"].call_args_list
                ])

    def test_account_submits_three_distinct_password_fields(self):
        callback = Mock()
        values = ["OldPass1!", "NewPass2!", "NewPass2!"]
        self.widgets["Entry"].side_effect = [Mock(get=Mock(return_value=value)) for value in values]
        view = AccountView(
            None,
            information_title="Student Information",
            information_rows=(
                ("Name", self.student.name),
                ("Student ID", self.student.student_id),
                ("Email", self.student.email)
            ),
            on_change_password=callback
        )
        view.submit_password()
        callback.assert_called_once_with(*values)
        for call in self.widgets["Entry"].call_args_list:
            self.assertEqual(call.kwargs["show"], "*")
        labels = [call.kwargs["text"] for call in self.widgets["Label"].call_args_list]
        self.assertIn("Student ID: 00000001", labels)
        self.assertIn("Name: Test Student", labels)
        self.assertIn("Email: test@student.uts.edu.au", labels)

    def test_dashboard_preserves_empty_slots_and_results(self):
        for count in (0, 1, 3, 4):
            with self.subTest(subjects=count):
                self.widgets["Label"].reset_mock()
                self.widgets["LabelFrame"].reset_mock()
                self.student.subjects = [Subject(f"{index:05d}", 60) for index in range(count)]
                DashboardView(None, self.student, self.student.get_overall_status())
                titles = [call.kwargs.get("text") for call in self.widgets["LabelFrame"].call_args_list]
                self.assertEqual(titles.count("Empty slot"), 4 - count)
                for subject in self.student.subjects:
                    self.assertIn(f"Subject {subject.subject_id}", titles)
                labels = [call.kwargs["text"] for call in self.widgets["Label"].call_args_list]
                if count:
                    self.assertIn("60.00", labels)
                    self.assertIn("PASS", labels)
                    self.assertEqual(labels.count("Mark: 60"), count)
                    self.assertEqual(labels.count("Grade: P"), count)
                else:
                    self.assertEqual(labels.count("N/A"), 7)

    def test_sidebar_buttons_call_their_own_action(self):
        callbacks = [Mock() for _ in range(4)]
        MainView(
            None,
            title="Student Portal",
            navigation=tuple(zip(("Dashboard", "Subjects", "Account"), callbacks)),
            on_logout=callbacks[3]
        )
        for call, callback in zip(self.widgets["Button"].call_args_list, callbacks):
            call.kwargs["command"]()
            callback.assert_called_once_with()
        self.assertEqual(len(self.widgets["Button"].call_args_list), 4)

    def test_subject_rows_capture_the_correct_id_and_enrollment_limit(self):
        for count in (0, 4):
            with self.subTest(subjects=count):
                self.widgets["Button"].reset_mock()
                self.student.subjects = [Subject(f"{index:05d}", 60) for index in range(count)]
                remove = Mock()
                SubjectsView(None, self.student, Mock(), remove)
                buttons = self.widgets["Button"].call_args_list
                self.assertEqual(buttons[0].kwargs["state"], "disabled" if count == 4 else "normal")
                with patch("views.gui.gui_student.subjects_view.messagebox.askyesno", return_value=True):
                    for button, subject in zip(buttons[1:], self.student.subjects):
                        remove.reset_mock()
                        button.kwargs["command"]()
                        remove.assert_called_once_with(subject.subject_id)
                self.assertEqual(len(buttons) - 1, count)


class TestGUIStudentController(unittest.TestCase):
    def setUp(self):
        self.service = Mock()
        self.error = Mock()
        self.success = Mock()
        self.controller = GUIStudentController(None, self.service, Mock(), Mock(), self.error, self.success)
        self.student = Student("00000001", "Test Student", "test@student.uts.edu.au", "OldPass1!")

    def test_main_page_preserves_navigation_and_opens_dashboard(self):
        with patch("controllers.gui.gui_student_controller.MainView") as view:
            with patch.object(self.controller, "show_dashboard") as dashboard:
                self.controller.show_student_main()
                view.assert_called_once_with(
                    None,
                    title="Student Portal",
                    navigation=(
                        ("Dashboard", dashboard),
                        ("Subjects", self.controller.show_subjects),
                        ("Account", self.controller.show_account)
                    ),
                    on_logout=self.controller.logout
                )
                self.controller.show_view.assert_called_once_with(view.return_value)
                dashboard.assert_called_once_with()

    def test_account_page_receives_student_details_and_callback(self):
        self.controller.active_account = self.student
        self.controller.main_view = Mock()
        with patch("controllers.gui.gui_student_controller.AccountView") as view:
            self.controller.show_account()
            view.assert_called_once_with(
                self.controller.main_view.content_frame,
                information_title="Student Information",
                information_rows=(
                    ("Name", self.student.name),
                    ("Student ID", self.student.student_id),
                    ("Email", self.student.email)
                ),
                on_change_password=self.controller.change_password
            )
            self.controller.main_view.show_content.assert_called_once_with(view.return_value)

    def test_login_only_opens_a_session_for_valid_credentials(self):
        with patch.object(self.controller, "show_student_main") as show_main:
            self.controller.login("", "")
            self.service.login.assert_not_called()
            self.service.login.side_effect = ValueError("Wrong password.")
            self.controller.login(self.student.email, "wrong")
            self.assertIsNone(self.controller.active_account)
            show_main.assert_not_called()
            self.error.assert_called_with("Wrong password.")
            self.service.login.side_effect = None
            self.service.login.return_value = self.student
            self.controller.login(self.student.email, "OldPass1!")
            self.assertIs(self.controller.active_account, self.student)
            show_main.assert_called_once_with()

    def test_service_errors_do_not_refresh_or_report_success(self):
        self.controller.active_account = self.student
        for action, arguments, refresh in (
            ("login", (self.student.email, "OldPass1!"), "show_student_main"),
            ("remove_subject", ("00001",), "show_subjects"),
            ("change_password", ("OldPass1!", "NewPass2!", "NewPass2!"), "show_account")
        ):
            for error in (ValueError("Invalid request"), OSError("Save failed")):
                with self.subTest(action=action, error=type(error).__name__):
                    self.error.reset_mock()
                    getattr(self.service, action).side_effect = error
                    with patch.object(self.controller, refresh) as show_page:
                        getattr(self.controller, action)(*arguments)
                        show_page.assert_not_called()
                    self.error.assert_called_once_with(str(error))
                    self.success.assert_not_called()

    def test_removal_refreshes_after_service_success(self):
        self.controller.active_account = self.student
        self.service.remove_subject.return_value = True
        with patch.object(self.controller, "show_subjects") as show_subjects:
            self.controller.remove_subject("00001")
            self.service.remove_subject.assert_called_once_with(self.student, "00001")
            show_subjects.assert_called_once_with()
        self.success.assert_called_once_with("Subject removed successfully.")
        self.error.assert_not_called()

    def test_password_confirmation_stays_in_controller(self):
        self.controller.active_account = self.student
        self.controller.change_password("", "", "")
        self.controller.change_password("OldPass1!", "NewPass2!", "different")
        self.service.change_password.assert_not_called()
        with patch.object(self.controller, "show_account") as show_account:
            self.controller.change_password("OldPass1!", "NewPass2!", "NewPass2!")
            self.service.change_password.assert_called_once_with(self.student, "OldPass1!", "NewPass2!")
            show_account.assert_called_once_with()
        self.success.assert_called_once_with("Password changed successfully.")


class TestGUIWelcomeNavigation(unittest.TestCase):
    def test_role_buttons_open_login_and_back_returns_to_welcome(self):
        with patch("controllers.gui.gui_uni_app.ErrorView"), \
                patch("controllers.gui.gui_uni_app.WelcomeView") as welcome:
            app = GUIUniApp(None, Mock(), Mock())
            for role in ("student", "admin"):
                with self.subTest(role=role), patch(
                    f"controllers.gui.gui_{role}_controller.LoginView"
                ) as login:
                    welcome.call_args.kwargs[f"on_{role}"]()
                    self.assertIs(app.current_view, login.return_value)
                    login.call_args.kwargs["on_back"]()
                    self.assertIs(app.current_view, welcome.return_value)
                    login.return_value.destroy.assert_called_once_with()
