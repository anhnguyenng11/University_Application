from models.admin import Admin
from models.file_handlers.admin_data_file import AdminDataFile
from models.student import Student
from models.file_handlers.student_data_file import StudentDataFile
from utils.validator import Validator


class AdminService:

    def __init__(
        self,
        admin_data_file: AdminDataFile,
        student_data_file: StudentDataFile
    ) -> None:
        self.admin_data_file = admin_data_file
        self.student_data_file = student_data_file

    def login(self, email: str, password: str) -> Admin | None:
        email = email.strip()

        admin = self.admin_data_file.find_admin_by_email(email)

        if admin is None:
            return None

        if admin.password != password:
            raise ValueError("Wrong password.")
            

        return admin

    def change_password(
        self, admin: Admin, current_password: str, new_password: str
    ) -> None:
        saved_admin = self.admin_data_file.find_admin_by_email(admin.email)

        if saved_admin is None or saved_admin.admin_id != admin.admin_id:
            raise ValueError("Admin not found.")

        if saved_admin.password != current_password:
            raise ValueError("Current password is incorrect.")

        if not Validator.is_valid_password(new_password):
            raise ValueError(
                "New password must start with an uppercase letter, "
                "followed by at least five letters and at least three digits."
            )

        if saved_admin.password == new_password:
            raise ValueError("New password must be different.")

        saved_admin.change_password(new_password)

        if not self.admin_data_file.update_admin(saved_admin):
            raise ValueError("Could not save the new password.")

        admin.password = saved_admin.password

    def get_all_students(self) -> list[Student]:
        return self.student_data_file.load_students()

    def group_students_by_grade(self) -> dict[str, list[Student]]:
        students = self.get_all_students()

        groups = {
            "HD": [],
            "D": [],
            "C": [],
            "P": [],
            "Z": [],
            "N/A": []
        }

        for student in students:
            _, _, grade = student.get_overall_status()
            groups[grade].append(student)

        return groups

    def partition_students_by_status(self) -> dict[str, list[Student]]:
        students = self.get_all_students()

        partitions = {
            "PASS": [],
            "FAIL": [],
            "N/A": []
        }

        for student in students:
            _, status, _ = student.get_overall_status()
            partitions[status].append(student)

        return partitions

    def remove_student(self, student_id: str) -> bool:
        return self.student_data_file.remove_student(student_id)

    def clear_all_students(self) -> None:
        self.student_data_file.clear_all_students()

    def search_student(self, student_id: str, email: str) -> Student | None:
        student_id = student_id.strip()
        email = email.strip().lower()

        if not student_id or not email:
            raise ValueError("Student ID and email are required.")

        student = self.student_data_file.find_student_by_id(student_id)

        if student is None or student.email.lower() != email:
            return None

        return student
