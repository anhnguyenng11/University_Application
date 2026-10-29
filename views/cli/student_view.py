
from models.student import Student
from models.subject import Subject
from views.cli.cli_view import CLIView
from utils import constants

class StudentView(CLIView):
    """
    Displays the student menu and related information in the CLI.
    Methods:
    - show_student_login: Displays the student login menu and prompts the student for their choice.
    - get_registration_details: Prompts the student for registration details (name, email, and password).
    - show_subject_course_menu: Displays the subject course menu and prompts the student for their choice.
    - get_subject_id_to_remove: Prompts the student for the subject ID they want to remove.
    - get_password_change_details: Prompts the student for their current password, new password, and confirmation of the new password.
    - show_registration_success: Displays a success message after successful student registration.
    - show_enrollment_success: Displays a success message after successful subject enrollment.
    - show_student_subjects: Displays the list of subjects the student is enrolled in, along with their marks, grades, and pass/fail status.
    """
    def show_student_login(self) -> str:
        """
        Displays the student login menu and prompts the student for their choice.
        """
        print("\nStudent System")
        print("(l) Login")
        print("(r) Register")
        print("(x) Exit")

        choice = input("Student System (l/r/x): ")
        # Accept both uppercase and lowercase inputs for the choice
        return choice.strip().lower()

    def get_registration_details(self) -> tuple[str, str, str]:
        """
        Prompts the student for registration details (name, email, and password)."""
        print("\nStudent Registration")

        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")

        return name, email, password

    def show_subject_course_menu(self) -> str:
        """
        Displays the subject course menu and prompts the student for their choice.
        """
        print("\nSubject Course Menu")
        print("(c) Change Password")
        print("(e) Enroll Subject")
        print("(r) Remove Subject")
        print("(s) Show Subjects")
        print("(x) Logout")

        choice = input("Subject Course (c/e/r/s/x): ")
        # Accept both uppercase and lowercase inputs for the choice
        return choice.strip().lower()

    def get_subject_id_to_remove(self) -> str:
        """
        Prompts the student for the subject ID they want to remove."""
        print("\nRemove Subject")

        subject_id = input("Enter Subject ID: ")
        return subject_id.strip()

    def get_password_change_details(self) -> tuple[str, str, str]:
        """
        Prompts the student for their current password, new password, and confirmation of the new password.
        """
        print("\nChange Password")

        current_password = input("Current Password: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm New Password: ")

        return current_password, new_password, confirm_password

    def show_registration_success(self, student: Student) -> None:
        """
        Displays a success message after successful student registration."""
        print("\nRegistration successful!")
        print("Student ID:", student.student_id)

    def show_enrollment_success(self, subject: Subject) -> None:
        """
        Displays a success message after successful subject enrollment.
        """
        print("\nEnrollment successful!")
        print(constants.BREAK_LINE)
        print("Subject ID:", subject.subject_id)
        print("Mark:", subject.mark)
        print("Grade:", subject.grade)

    def show_student_subjects(self, student: Student) -> None:
        """
        Displays the list of subjects the student is enrolled in, along with their marks, grades, and pass/fail status.
        """
        print("\nMy Subjects")
        print(constants.BREAK_LINE)

        if len(student.subjects) == 0:
            print("You have no enrolled subjects.")
            return

        for subject in student.subjects:
            print("Subject ID:", subject.subject_id)
            print("Mark:", subject.mark)
            print("Grade:", subject.grade)
            print("Status:", subject.get_pass_fail_status())
            print(constants.BREAK_LINE)

        average, status, grade = student.get_overall_status()

        if average is None:
            print("Average Mark: N/A")
        else:
            print("Average Mark:", round(average, 2))

        print("Overall Status:", status)
        print("Overall Grade:", grade)

