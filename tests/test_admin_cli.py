import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, call, patch

from controllers.cli.admin_controller import AdminController
from models.admin_service import AdminService
from models.student import Student
from views.cli.admin_view import AdminView


class TestAdminController(unittest.TestCase):
    def setUp(self):
        # fake view and service for each test
        self.view = Mock(spec=AdminView)
        self.view.get_login_details.return_value = (
            "admin@university.com", "Password123"
        )
        self.service = Mock(spec=AdminService)
        self.controller = AdminController(self.view, self.service)

    def test_failed_login_shows_error_without_starting_session(self):
        for message in ("Admin email not found.", "Wrong password."):
            with self.subTest(message=message):
                self.service.login.side_effect = ValueError(message)
                self.controller.login_admin()
                self.view.show_message.assert_called_with(message)
                self.view.show_welcome.assert_not_called()
                self.view.show_admin_menu.assert_not_called()

    def test_menu_routes_each_operation_then_exits(self):
        for choice, method in (
            ("c", "clear_database"),
            ("g", "group_students"),
            ("p", "partition_students"),
            ("r", "remove_student"),
            ("s", "show_students"),
        ):
            with self.subTest(choice=choice):
                self.view.show_admin_menu.side_effect = [choice, "x"]
                with patch.object(self.controller, method) as action:
                    self.controller.start()
                action.assert_called_once_with()

    def test_invalid_option_returns_to_menu(self):
        self.view.show_admin_menu.side_effect = ["?", "x"]
        self.controller.start()
        self.view.show_message.assert_called_once_with(
            "Invalid option. Please try again."
        )
        self.assertEqual(self.service.mock_calls, [
            call.login("admin@university.com", "Password123")
        ])

    def test_read_actions_forward_service_results(self):
        for action, service_method, view_method, result in (
            ("show_students", "get_all_students", "show_student_list", []),
            ("group_students", "group_students_by_grade",
             "show_grade_grouping", {"N/A": []}),
            ("partition_students", "partition_students_by_status",
             "show_pass_fail_partition", {"PASS": [], "FAIL": [], "N/A": []}),
        ):
            with self.subTest(action=action):
                getattr(self.service, service_method).return_value = result
                getattr(self.controller, action)()
                getattr(self.service, service_method).assert_called_once_with()
                getattr(self.view, view_method).assert_called_once_with(result)

    def test_clear_requires_confirmation(self):
        for confirmed in (False, True):
            with self.subTest(confirmed=confirmed):
                self.service.reset_mock()
                self.view.confirm_clear_database.return_value = confirmed
                self.controller.clear_database()
                self.view.confirm_clear_database.assert_called()
                self.assertEqual(
                    self.service.clear_all_students.call_count, int(confirmed)
                )

    def test_removal_preserves_id_and_handles_missing_student(self):
        self.view.get_student_id_to_remove.return_value = "000001"
        self.service.remove_student.return_value = False
        self.controller.remove_student()
        self.service.remove_student.assert_called_once_with("000001")
        self.view.show_student_removed.assert_not_called()
        self.view.show_message.assert_called_once_with(
            "Cannot find student with ID 000001"
        )

        self.service.remove_student.return_value = True
        self.controller.remove_student()
        self.view.show_student_removed.assert_called_once_with("000001")

    def test_blank_id_does_not_call_service(self):
        self.view.get_student_id_to_remove.return_value = ""
        self.controller.remove_student()
        self.service.remove_student.assert_not_called()
        self.view.show_message.assert_called_once_with(
            "Student ID cannot be empty."
        )

    def test_failed_action_reports_error_without_success(self):
        for choice, service_method in (
            ("s", "get_all_students"),
            ("g", "group_students_by_grade"),
            ("p", "partition_students_by_status"),
            ("r", "remove_student"),
            ("c", "clear_all_students"),
        ):
            for error_type in (ValueError, OSError):
                with self.subTest(choice=choice, error=error_type):
                    self.setUp()
                    self.view.show_admin_menu.side_effect = [choice, "x"]
                    self.view.get_student_id_to_remove.return_value = "000001"
                    self.view.confirm_clear_database.return_value = True
                    getattr(self.service, service_method).side_effect = error_type(
                        "Storage unavailable"
                    )
                    self.controller.start()
                    self.view.show_message.assert_any_call(
                        "Admin operation failed: Storage unavailable"
                    )
                    self.view.show_student_removed.assert_not_called()
                    self.view.show_student_list.assert_not_called()
                    self.view.show_grade_grouping.assert_not_called()
                    self.view.show_pass_fail_partition.assert_not_called()
                    messages = [
                        call.args[0]
                        for call in self.view.show_message.call_args_list
                    ]
                    self.assertNotIn("Students data cleared", messages)


class TestAdminView(unittest.TestCase):
    def test_shared_welcome_preserves_name_id_and_role_label(self):
        for role in ("Student", "Admin"):
            with self.subTest(role=role):
                output = io.StringIO()
                with redirect_stdout(output):
                    AdminView().show_welcome("Example", "000001", role)
                self.assertEqual(
                    output.getvalue(), f"\nWelcome, Example!\n{role} ID: 000001\n"
                )

    def test_partition_includes_ungraded_student_without_password(self):
        student = Student(
            "000001", "Test Student", "test@university.com", "Password123"
        )
        output = io.StringIO()
        with redirect_stdout(output):
            AdminView().show_pass_fail_partition(
                {"PASS": [], "FAIL": [], "N/A": [student]}
            )
        text = output.getvalue()
        self.assertIn("N/A -->", text)
        self.assertEqual(text.count("Test Student :: 000001"), 1)
        self.assertNotIn(student.password, text)

    def test_confirmation_accepts_yes_and_rejects_other_input(self):
        for answer, expected in (
            ("y", True),
            (" YES ", True),
            ("n", False),
            ("", False),
        ):
            with self.subTest(answer=answer):
                with patch("builtins.input", return_value=answer):
                    self.assertEqual(
                        AdminView().confirm_clear_database(), expected
                    )


if __name__ == "__main__":
    unittest.main()
