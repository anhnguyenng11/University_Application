from views.cli.student_view import StudentView
from models.student import Student
from models.student_service import StudentService

class StudentController:
    def __init__(
        self,
        view: StudentView,
        student_service: StudentService
    ) -> None:
        self.view = view
        self.student_service = student_service

    def start(self) -> None:
        while True:
            choice = self.view.show_student_menu()

            match choice:
                case "l":
                    self.login_student()

                case "r":
                    self.register_student()

                case "x":
                    return

                case _:
                    self.view.show_message("Invalid option. Please try again.")

    def register_student(self) -> None:
        name, email, password = self.view.get_registration_details()

        try:
            student = self.student_service.register(
                name,
                email,
                password
            )

            self.view.show_registration_success(student)

        except ValueError as error:
            self.view.show_message("Registration failed: " + str(error))

    def login_student(self) -> None:
        email, password = self.view.get_login_details()

        student = self.student_service.login(
            email,
            password
        )

        if student is None:
            self.view.show_message("Invalid email or password.")
            return

        self.start_student_session(student)

    def start_student_session(self, student: Student) -> None:
        self.view.show_student_welcome(student)

        while True:
            choice = self.view.show_subject_course_menu()

            match choice:
                case "c":
                    self.change_student_password(student)

                case "e":
                    self.enroll_student_subject(student)

                case "r":
                    self.remove_student_subject(student)

                case "s":
                    self.show_student_subjects(student)

                case "x":
                    self.view.show_message("Logging out...")
                    return

                case _:
                    self.view.show_message("Invalid option. Please try again.")

    def enroll_student_subject(self, student: Student) -> None:
        try:
            subject = self.student_service.enroll_subject(student)

            self.view.show_enrollment_success(subject)

        except ValueError as error:
            self.view.show_message("Enrollment failed: " + str(error))

    def remove_student_subject(self, student: Student) -> None:
        subject_id = self.view.get_subject_id_to_remove()

        try:
            self.student_service.remove_subject(
                student,
                subject_id
            )

            self.view.show_message("Subject " + subject_id + " removed successfully.")

        except ValueError as error:
            self.view.show_message("Removal failed: " + str(error))

    def change_student_password(self, student: Student) -> None:
        current_password, new_password = self.view.get_password_change_details()

        if new_password != confirm_password:
            self.view.show_message("Password change failed: passwords do not match.")
    return
        try:
            self.student_service.change_password(
                student,
                current_password,
                new_password
            )

            self.view.show_message("Password changed successfully!")

        except ValueError as error:
            self.view.show_message(str(error))

    def show_student_subjects(self, student: Student) -> None:
        self.view.show_student_subjects(student)
