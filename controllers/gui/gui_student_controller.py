from views.gui.login_view import LoginView
from controllers.gui.base_gui_controller import BaseGUIController
from views.gui.gui_student.registration_view import RegistrationView
from views.gui.main_view import MainView
from views.gui.gui_student.dashboard_view import DashboardView
from views.gui.gui_student.subjects_view import SubjectsView
from views.gui.account_view import AccountView


class GUIStudentController(BaseGUIController):
    def show_login(self):
        view = LoginView(
            self.root,
            title="Student Login",
            on_login=self.login,
            on_register=self.show_registration,
            on_back=self.on_exit
        )
        self.show_view(view)

    def show_registration(self):
        view = RegistrationView(
            self.root,
            on_register=self.register,
            on_back=self.show_login
        )
        self.show_view(view)

    def login(self, email, password):
        if not email or not password:
            self.on_error("Email and password are required.")
            return

        try:
            student = self.service.login(email, password)

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.active_account = student
        self.show_student_main()

    def register(self, name, email, password):
        try:
            student = self.service.register(name, email, password)

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_login()
        self.on_success(f"Registration successful. Your student ID is {student.student_id}.")

    def logout(self):
        self.active_account = None
        self.show_login()

    def show_student_main(self):
        self.main_view = MainView(
            self.root,
            title="Student Portal",
            navigation=(
                ("Dashboard", self.show_dashboard),
                ("Subjects", self.show_subjects),
                ("Account", self.show_account)
            ),
            on_logout=self.logout
        )

        self.show_view(self.main_view)
        self.show_dashboard()

    def show_dashboard(self):
        overall = self.active_account.get_overall_status()
        view = DashboardView(
            self.main_view.content_frame,
            student=self.active_account,
            overall=overall
        )

        self.main_view.show_content(view)

    def show_subjects(self):
        view = SubjectsView(
            self.main_view.content_frame,
            student=self.active_account,
            on_enroll=self.enroll_subject,
            on_remove=self.remove_subject
        )

        self.main_view.show_content(view)

    def enroll_subject(self):
        try:
            subject = self.service.enroll_subject(
                self.active_account
            )

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_subjects()
        self.on_success(
            f"Successfully enrolled in Subject {subject.subject_id}."
        )

    def remove_subject(self, subject_id):
        try:
            self.service.remove_subject(
                self.active_account,
                subject_id
            )

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_subjects()
        self.on_success("Subject removed successfully.")

    def show_account(self):
        view = AccountView(
            self.main_view.content_frame,
            information_title="Student Information",
            information_rows=(
                ("Name", self.active_account.name),
                ("Student ID", self.active_account.student_id),
                ("Email", self.active_account.email)
            ),
            on_change_password=self.change_password
        )

        self.main_view.show_content(view)
