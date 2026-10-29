"""
This module defines the Subject class, which represents a subject in the university application.
"""
from utils import constants
from utils.grade_calculator import calculate_grade


class Subject:
    def __init__(self, subject_id: str, mark: int) -> None:
        self.subject_id = subject_id
        self.mark = mark
        self.grade = self.calculate_grade()

    def calculate_grade(self) -> str:
        return calculate_grade(self.mark)

    def get_pass_fail_status(self) -> str:
        if self.mark >= constants.P_THRESHOLD:
            return "PASS"
        else:
            return "FAIL"
