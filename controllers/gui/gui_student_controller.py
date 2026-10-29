"""
GUIStudentController is responsible for managing the student interface of UniApp.
"""
from views import LoginView, RegistrationView, MainView, DashboardView, SubjectsView, AccountView
from controllers.gui.base_gui_controller import BaseGUIController

class GUIStudentController(BaseGUIController):
    """
    GUIStudentController is responsible for managing the student interface of the university application.
    Methods:
    - show_login: Displays the login view for students.
    - show_registration: Displays the registration view for new students.
    - login: Logs in a student with the provided email and password.
    - register: Registers a new student with the provided name, email, and password.
    - logout: Logs out the currently active student and returns to the login view.
    - show_student_main: Displays the main view for the currently active student.
    - show_dashboard: Displays the dashboard view for the currently active student.
    - show_subjects: Displays the subjects view for the currently active student.
    - enroll_subject: Enrolls the currently active student in a new subject.
    - remove_subject: Removes a subject from the currently active student's enrolled subjects.
    - show_account: Displays the account view for the currently active student.
    """
    def show_login(self):
        """
        GUI: Displays the login view for students.
        """
        view = LoginView(
            self.root,
            title="Student Login",
            on_login=self.login,
            on_register=self.show_registration,
            on_back=self.on_exit
        )
        self.show_view(view)

    def show_registration(self):
        """
        GUI: Displays the registration view for new students.
        """
        view = RegistrationView(
            self.root,
            title="Student Registration",
            on_register=self.register,
            on_back=self.show_login
        )
        self.show_view(view)

    def login(self, email, password):
        """
        GUI: Logs in a student with the provided email and password. 
        """
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
        """
        GUI: Registers a new student with the provided name, email, and password.
        """
        try:
            student = self.service.register(name, email, password)

        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_login()
        self.on_success(f"Registration successful. Your student ID is {student.student_id}.")

    def logout(self):
        """
        GUI: Logs out the currently active student and returns to the login view.
        """
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
        """
        GUI: Displays the dashboard view for the currently active student.
        """
        overall = self.active_account.get_overall_status()
        view = DashboardView(
            "Student Portal",
            self.main_view.content_frame,
            student=self.active_account,
            overall=overall
        )

        self.main_view.show_content(view)

    def show_subjects(self):
        """
        GUI: Displays the subjects view for the currently active student.
        """
        view = SubjectsView(
            self.main_view.content_frame,
            student=self.active_account,
            on_enroll=self.enroll_subject,
            on_remove=self.remove_subject
        )

        self.main_view.show_content(view)

    def enroll_subject(self):
        """
        GUI: Enrolls the currently active student in a new subject.
        """
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
        """
        GUI: Removes a subject from the currently active student's enrolled subjects.
        """
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
