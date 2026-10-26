from views.gui.gui_student.login_view import LoginView
from views.gui.gui_student.registration_view import RegistrationView
from views.gui.gui_student.student_main_view import StudentMainView
from views.gui.gui_student.dashboard_view import DashboardView
from views.gui.gui_student.subjects_view import SubjectsView
from views.gui.gui_student.account_view import AccountView


class GUIStudentController:
    def __init__(
        self,
        root,
        student_service,
        show_view,
        on_exit,
        on_error,
        on_success
    ):
        self.root = root
        self.student_service = student_service
        self.show_view = show_view
        self.on_exit = on_exit
        self.on_error = on_error
        self.on_success = on_success

        self.active_student = None

    def start(self):
        self.show_login()

    def show_login(self):
        view = LoginView(
            self.root,
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
            student = self.student_service.login(email, password)

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if student is None:
            self.on_error("Invalid email or password.")
            return

        self.active_student = student
        self.show_student_main()

    def register(self, name, email, password):
        try:
            student = self.student_service.register(name, email, password)

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_login()
        self.on_success(f"Registration successful. Your student ID is {student.student_id}.")

    def logout(self):
        self.active_student = None
        self.show_login()

    def show_student_main(self):
        self.main_view = StudentMainView(
            self.root,
            on_dashboard=self.show_dashboard,
            on_subjects=self.show_subjects,
            on_account=self.show_account,
            on_logout=self.logout
        )

        self.show_view(self.main_view)
        self.show_dashboard()

    def show_dashboard(self):
        overall = self.active_student.get_overall_status()
        view = DashboardView(
            self.main_view.content_frame,
            student=self.active_student,
            overall=overall
        )

        self.main_view.show_content(view)

    def show_subjects(self):
        view = SubjectsView(
            self.main_view.content_frame,
            student=self.active_student,
            on_enroll=self.enroll_subject,
            on_remove=self.remove_subject
        )

        self.main_view.show_content(view)

    def enroll_subject(self):
        try:
            subject = self.student_service.enroll_subject(
                self.active_student
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
            self.student_service.remove_subject(
                self.active_student,
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
            student=self.active_student,
            on_change_password=self.change_password
        )

        self.main_view.show_content(view)

    def change_password(self, current_password, new_password, confirm_password):
        if not current_password or not new_password or not confirm_password:
            self.on_error("All password fields are required.")
            return

        if new_password != confirm_password:
            self.on_error("Passwords do not match.")
            return

        try:
            self.student_service.change_password(
                self.active_student,
                current_password,
                new_password
            )

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_account()
        self.on_success("Password changed successfully.")
