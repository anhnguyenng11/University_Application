"""
This module defines the StudentController class, which handles the student operation flow in the university application.
"""
from views import StudentView
from models import Student, StudentService

class StudentController:
    """
    The StudentController class manages the flow of operations for student users in the university application.
    Methods:
    - start: Initiates the student operation flow.
    - register_student: Handles the registration of a new student.
    - login_student: Handles the login of an existing student.
    - start_student_session: Starts the student session.
    - enroll_student_subject: Enrolls a student in a subject.
    - remove_student_subject: Removes a subject from a student's enrolled subjects.
    - change_student_password: Changes a student's password.
    - show_student_subjects: Displays the list of subjects a student is enrolled in.
    """

    def __init__(self, view: StudentView, student_service: StudentService) -> None:
        self.view = view
        self.student_service = student_service

    def start(self) -> None:
        while True:
            choice = self.view.show_student_login()

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
        """
        Prompts the user for registration details and attempts to register a new student."""
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
        """
        Prompts the user for login details and attempts to log in a student.
        """
        email, password = self.view.get_login_details("Student")

        try:
            student = self.student_service.login(email, password)
        except ValueError as error:
            self.view.show_message(str(error))
            return

        self.start_student_session(student)

    def start_student_session(self, student: Student) -> None:
        """
        Starts the student session, displaying a welcome message and a loop for the subject course menu.
        """
        self.view.show_welcome(student.name, student.student_id, "Student")

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
        """
        Prompts the student for subject enrollment details and attempts to enroll the student in a subject.
        """
        try:
            subject = self.student_service.enroll_subject(student)

            self.view.show_enrollment_success(subject)

        except ValueError as error:
            self.view.show_message("Enrollment failed: " + str(error))

    def remove_student_subject(self, student: Student) -> None:
        """
        Prompts the student for the subject ID they want to remove and attempts to remove the subject from the student's enrolled subjects.
        """
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
        """
        Prompts the student for their current password, new password, and confirmation of the new password.
        """
        while True:
            current_password, new_password, confirm_password = (
                self.view.get_password_change_details()
            )

            if new_password != confirm_password:
                self.view.show_message("New passwords do not match. Please try again.")
                continue

            break

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
        """
        Displays the list of subjects the student is enrolled in, along with their marks, grades, and pass/fail status.
        """
        self.view.show_student_subjects(student)
