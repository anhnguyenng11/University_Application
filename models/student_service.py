
from models.student import Student
from models.file_handlers.student_data_file import StudentDataFile
from helpers.validator import Validator
from helpers.id_generator import IDGenerator


class StudentService:
    def __init__(self, student_data_file: StudentDataFile) -> None:
        self.student_data_file = student_data_file
