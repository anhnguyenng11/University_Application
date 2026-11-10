from views import ErrorView, WelcomeView
from controllers.gui.gui_student_controller import GUIStudentController
from controllers.gui.gui_admin_controller import GUIAdminController

class GUIUniApp:
    def __init__(self, root, student_service, admin_service):
        self.root = root
        self.current_view = None

        self.error_view = ErrorView(root)

        self.student_controller = GUIStudentController(
            root=root,
            service=student_service,
            show_view=self.show_view,
            on_exit=self.show_welcome,
            on_error=self.error_view.show_error,
            on_success=self.error_view.show_success
        )
        
        self.admin_controller = GUIAdminController(
            root=root,
            service=admin_service,
            show_view=self.show_view,
            on_exit=self.show_welcome,
            on_error=self.error_view.show_error,
            on_success=self.error_view.show_success
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
            on_student=self.student_controller.show_login,
            on_admin=self.admin_controller.show_login
        )
        self.show_view(view)
