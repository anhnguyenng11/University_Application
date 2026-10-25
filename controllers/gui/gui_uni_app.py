
from controllers.gui.gui_student_controller import GUIStudentController

from views.gui.welcome_view import WelcomeView
from views.gui.gui_student.login_view import LoginView
from views.gui.gui_student.registration_view import RegistrationView
from views.gui.error_view import ErrorView


class GUIUniApp:
    def __init__(self, root, student_service):
        self.root = root
        self.current_view = None
        self.active_student = None

        self.error_view = ErrorView(root)

        self.student_controller = GUIStudentController(
            student_service,
            on_success=self.login_success,
            on_error=self.error_view.show_error,
            on_registered=self.registration_success
        )

        self.show_welcome()

    def show_view(self, view):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view
        self.current_view.pack(fill="both", expand=True)

    def show_welcome(self):
        view = WelcomeView(
            self.root,
            on_student=self.show_student_login
        )
        self.show_view(view)

    def show_student_login(self):
        view = LoginView(
            self.root,
            on_login=self.student_controller.login,
            on_register=self.show_registration,
            on_back=self.show_welcome
        )
        self.show_view(view)

    def login_success(self, student):
        self.active_student = student
        self.error_view.show_success("Login successful!")

    def show_registration(self):
        view = RegistrationView(
            self.root,
            on_register=self.student_controller.register,
            on_back=self.show_student_login
        )
        self.show_view(view)

    def registration_success(self, student):
        self.show_student_login()
        self.error_view.show_success(
            f"Registration successful. Your student ID is {student.student_id}."
        )
