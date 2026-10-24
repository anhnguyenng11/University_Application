
from models.student import Student
from models.subject import Subject
from views.base_cli_view import BaseCLIView


class StudentView(BaseCLIView):
    def show_student_menu(self) -> str:
        print("\nStudent System")
        print("(l) Login")
        print("(r) Register")
        print("(x) Exit")

        choice = input("Student System (l/r/x): ")
        return choice.strip().lower()

    def get_registration_details(self) -> tuple[str, str, str]:
        print("\nStudent Registration")

        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")

        return name, email, password

    def get_login_details(self) -> tuple[str, str]:
        print("\nStudent Login")

        email = input("Email: ")
        password = input("Password: ")

        return email, password

    def show_subject_course_menu(self) -> str:
        print("\nSubject Course Menu")
        print("(c) Change Password")
        print("(e) Enroll Subject")
        print("(r) Remove Subject")
        print("(s) Show Subjects")
        print("(x) Logout")

        choice = input("Subject Course (c/e/r/s/x): ")
        return choice.strip().lower()

    def get_subject_id_to_remove(self) -> str:
        print("\nRemove Subject")

        subject_id = input("Enter Subject ID: ")
        return subject_id.strip()

    def get_password_change_details(self) -> tuple[str, str, str]:
        print("\nChange Password")

        current_password = input("Current Password: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm New Password: ")

        return current_password, new_password, confirm_password

    def show_student_welcome(self, student: Student) -> None:
        print("\nWelcome, " + student.name + "!")
        print("Student ID:", student.student_id)

    def show_registration_success(self, student: Student) -> None:
        print("\nRegistration successful!")
        print("Student ID:", student.student_id)

    def show_enrollment_success(self, subject: Subject) -> None:
        print("\nEnrollment successful!")
        print("------------------------")
        print("Subject ID:", subject.subject_id)
        print("Mark:", subject.mark)
        print("Grade:", subject.grade)

    def show_student_subjects(self, student: Student) -> None:
        print("\nMy Subjects")
        print("----------------------")

        if len(student.subjects) == 0:
            print("You have no enrolled subjects.")
            return

        for subject in student.subjects:
            print("Subject ID:", subject.subject_id)
            print("Mark:", subject.mark)
            print("Grade:", subject.grade)
            print("Status:", subject.get_pass_fail_status())
            print("----------------------")

        average, status, grade = student.get_overall_status()

        if average is None:
            print("Average Mark: N/A")
        else:
            print("Average Mark:", round(average, 2))

        print("Overall Status:", status)
        print("Overall Grade:", grade)

