from views.gui.gui_admin.login_view import LoginView
from views.gui.gui_admin.admin_main_view import AdminMainView
from views.gui.gui_admin.students_view import StudentsView


class GUIAdminController:
    def __init__(
        self, root, admin_service, show_view, on_exit, on_error, on_success
    ):
        self.root = root
        self.admin_service = admin_service
        self.show_view = show_view
        self.on_exit = on_exit
        self.on_error = on_error
        self.on_success = on_success
        self.active_admin = None
        self.student_mode = "all"

    def start(self):
        self.show_login()

    def show_login(self):
        self.active_admin = None
        view = LoginView(
            self.root,
            on_login=self.login,
            on_back=self.on_exit
        )
        self.show_view(view)

    def login(self, email, password):
        email = email.strip()

        if not email or not password:
            self.on_error("Email and password are required.")
            return

        try:
            admin = self.admin_service.login(email, password)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if admin is None:
            self.on_error("Invalid email or password.")
            return

        self.active_admin = admin
        self.show_admin_main()

    def show_admin_main(self):
        self.main_view = AdminMainView(
            self.root,
            on_view_students=self.show_students,
            # shortcut: disable unfinished pages, connect callbacks when ready.
            on_search_students=None,
            on_account=None,
            on_logout=self.logout
        )
        self.show_view(self.main_view)
        self.show_students()

    def show_students(self, mode="all"):
        try:
            if mode == "grade":
                groups = self.admin_service.group_students_by_grade()
            elif mode == "status":
                groups = self.admin_service.partition_students_by_status()
            else:
                groups = {"": self.admin_service.get_all_students()}
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return False

        view = StudentsView(
            self.main_view.content_frame,
            groups=groups,
            on_show_all=self.show_students,
            on_group=lambda: self.show_students("grade"),
            on_partition=lambda: self.show_students("status"),
            on_remove=self.remove_student,
            on_clear=self.clear_all_students
        )
        self.main_view.show_content(view)
        self.student_mode = mode
        return True

    def remove_student(self, student_id):
        try:
            removed = self.admin_service.remove_student(student_id)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if not removed:
            self.on_error("Student not found.")
            return

        if self.show_students(self.student_mode):
            self.on_success("Student removed successfully.")

    def clear_all_students(self):
        try:
            self.admin_service.clear_all_students()
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if self.show_students(self.student_mode):
            self.on_success("All student records cleared.")

    def logout(self):
        self.show_login()