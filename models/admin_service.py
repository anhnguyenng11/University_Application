from models.admin import Admin
from models.file_handlers.admin_data_file import AdminDataFile
from models.student import Student
from models.file_handlers.student_data_file import StudentDataFile


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
