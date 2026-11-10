from models.file_handlers.database import Database
from models.student import Student
from models.subject import Subject
from utils import constants

class StudentDataFile:
    """
    StudentDataFile is responsible for handling the storage and retrieval of student data.
    Methods:
    - load_students: Loads the list of Student objects from the database.
    - find_student_by_email: Finds a Student object by email.
    - find_student_by_id: Finds a Student object by ID.
    - email_exists: Checks if a student with the given email exists.
    - save_students: Saves the list of Student objects to the database.
    - add_student: Adds a new Student object to the database.
    - update_student: Updates a Student object in the database.
    - remove_student: Removes a Student object from the database.
    - clear_all_students: Clears all Student objects from the database.
    """
    def __init__(self, data_folder=None) -> None:
        self.database = Database(
            constants.STUDENT_DATABASE,
            {"students": []},
            data_folder
        )

    def load_students(self) -> list[Student]:
        """
        Loads the list of Student objects from the database.
        Returns: A list of Student objects.
        """
        data = self.database.load_data()

        students = []

        for student_data in data["students"]:
            subjects = []

            for subject_data in student_data["subjects"]:
                subject = Subject(
                    subject_data["subject_id"],
                    subject_data["mark"]
                )

                subjects.append(subject)

            student = Student(
                student_data["student_id"],
                student_data["name"],
                student_data["email"],
                student_data["password"],
                subjects
            )

            students.append(student)

        return students

    def find_student_by_email(self, email: str) -> Student | None:
        """
        Finds a Student object by email.
        Returns: The Student object if found, otherwise None.
        """
        students = self.load_students()

        for student in students:
            if student.email.lower() == email.lower():
                return student

        return None

    def find_student_by_id(self, student_id: str) -> Student | None:
        """
        Finds a Student object by ID.
        Returns: The Student object if found, otherwise None.
        """
        students = self.load_students()

        for student in students:
            if student.student_id == student_id:
                return student

        return None

    def email_exists(self, email: str) -> bool:
        """
        Checks if a student with the given email exists.
        """
        return self.find_student_by_email(email) is not None

    def save_students(self, students: list[Student]) -> None:
        """
        Saves the list of Student objects to the database.
        """
        student_records = []

        for student in students:
            subject_records = []

            for subject in student.subjects:
                subject_data = {
                    "subject_id": subject.subject_id,
                    "mark": subject.mark
                }

                subject_records.append(subject_data)

            student_data = {
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "password": student.password,
                "subjects": subject_records
            }

            student_records.append(student_data)

        data = {"students": student_records}
        self.database.save_data(data)

        
    def add_student(self, student: Student) -> bool:
        """
        Adds a new Student object to the database.
        Returns: True if the student was added successfully, otherwise False.
        """
        students = self.load_students()

        for existing_student in students:
            if existing_student.student_id == student.student_id:
                return False

            if existing_student.email.lower() == student.email.lower():
                return False

        students.append(student)
        self.save_students(students)
        return True

    def update_student(self, updated_student: Student) -> bool:
        """
        Updates a Student object in the database.
        Returns: True if the update is successful, otherwise False.
        """
        students = self.load_students()

        for index in range(len(students)):
            if students[index].student_id == updated_student.student_id:
                students[index] = updated_student
                self.save_students(students)
                return True

        return False

    def remove_student(self, student_id: str) -> bool:
        """
        Removes a Student object from the database.
        Returns: True if the removal is successful, otherwise False.
        """
        students = self.load_students()
        for student in students:
            if student.student_id == student_id:
                students.remove(student)
                self.save_students(students)
                return True
        return False

    def clear_all_students(self) -> None:
        """
        Clears all Student objects from the database.
        """
        students = self.load_students()
        students.clear()
        self.save_students(students)
