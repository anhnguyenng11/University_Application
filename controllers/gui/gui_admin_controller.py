"""
Warning: This module is not a part of the assignment.
"""
from views import LoginView, MainView, StudentsView, SearchStudentsView, AccountView
from controllers.gui.base_gui_controller import BaseGUIController

class GUIAdminController(BaseGUIController):
    """
    GUIAdminController is responsible for managing the admin interface of the university application.
    """
    def __init__(self, root, service, show_view, on_exit, on_error, on_success):
        super().__init__(root, service, show_view, on_exit, on_error, on_success)
        self.student_mode = "all"

    def show_login(self):
        self.active_account = None
        view = LoginView(
            self.root,
            title="Admin Login",
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
            admin = self.service.login(email, password)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.active_account = admin
        self.show_admin_main()

    def show_admin_main(self):
        self.main_view = MainView(
            self.root,
            title="Admin Portal",
            navigation=(
                ("View Students", self.show_students),
                ("Search Students", self.show_search_students),
                ("Account", self.show_account)
            ),
            on_logout=self.logout
        )
        self.show_view(self.main_view)
        self.show_students()

    def show_students(self, mode="all"):
        try:
            if mode == "grade":
                groups = self.service.group_students_by_grade()
            elif mode == "status":
                groups = self.service.partition_students_by_status()
            else:
                groups = {"": self.service.get_all_students()}
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

    def show_search_students(self):
        self.search_view = SearchStudentsView(
            self.main_view.content_frame,
            on_search=self.search_student,
            on_remove=self.remove_student
        )
        self.main_view.show_content(self.search_view)
        self.student_mode = "search"

    def search_student(self, student_id, email):
        try:
            student = self.service.search_student(student_id, email)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.search_view.show_student(student)

    def remove_student(self, student_id):
        try:
            removed = self.service.remove_student(student_id)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if not removed:
            self.on_error("Student not found.")
            return

        if self.student_mode == "search":
            self.search_view.clear_result()
        elif not self.show_students(self.student_mode):
            return

        self.on_success("Student removed successfully.")

    def clear_all_students(self):
        try:
            self.service.clear_all_students()
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        if self.show_students(self.student_mode):
            self.on_success("All student records cleared.")

    def show_account(self):
        view = AccountView(
            self.main_view.content_frame,
            information_title="Admin Information",
            information_rows=(
                ("Name", self.active_account.name),
                ("Admin ID", self.active_account.admin_id),
                ("Email", self.active_account.email)
            ),
            on_change_password=self.change_password
        )
        self.main_view.show_content(view)

    def logout(self):
        self.show_login()
