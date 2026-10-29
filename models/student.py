
from models.subject import Subject
from utils import constants
from utils.grade_calculator import calculate_grade


class Student:
    """
    Represents a student with their personal information and enrolled subjects.
    Attributes:
        student_id (str): Unique identifier for the student.
        name (str): Full name of the student.
        email (str): Email address of the student.
        password (str): Password for the student's account.
        subjects (list[Subject]): List of subjects the student is enrolled in.
    Methods:
    - can_enroll: Checks if the student can enroll in more subjects based on the enrollment limit.
    - add_subject: Adds a new subject to the student's enrolled subjects.
    - remove_subject: Removes a subject from the student's enrolled subjects.
    - _change_password: Changes the student's password to a new password. Private method, should be called by StudentService after validation.
    - get_overall_status: Calculates the student's overall average mark, status (PASS/FAIL/N/A), and grade based on their enrolled subjects.
    """
    
    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        password: str,
        subjects=None
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password

        if subjects is None:
            self.subjects = []
        else:
            self.subjects = list(subjects)
        if len(self.subjects) > constants.SUBJECT_LIMIT:
            raise ValueError(constants.SUBJECT_LIMIT_MESSAGE)

    def can_enroll(self) -> bool:
        """
        Checks if the student can enroll in more subjects based on the enrollment limit.
        Returns: True if the student can enroll in more subjects, otherwise False.
        """
        return len(self.subjects) < constants.SUBJECT_LIMIT

    def add_subject(self, subject: Subject) -> bool:
        """
        Adds a new subject to the student's enrolled subjects if they haven't reached the enrollment limit and the subject isn't already enrolled.
        Returns: True if the subject was added successfully, otherwise False.
        """
        if not self.can_enroll():
            return False

        for existing_subject in self.subjects:
            if existing_subject.subject_id == subject.subject_id:
                return False

        self.subjects.append(subject)
        return True

    def remove_subject(self, subject_id: str) -> bool:
        """
        Removes a subject from the student's enrolled subjects based on the subject ID.
        Returns: True if the subject was removed successfully, otherwise False.
        """
        for subject in self.subjects:
            if subject.subject_id == subject_id:
                self.subjects.remove(subject)
                return True

        return False

    def _change_password(self, new_password: str) -> None:
        """
        Changes the student's password to a new password. Private method, should be called by StudentService after validation.
        """
        self.password = new_password



    def get_overall_status(self) -> tuple[float | None, str, str]:
        """
        Calculates the student's overall average mark, status (PASS/FAIL/N/A), and grade based on their enrolled subjects.
        Returns: A tuple containing the average mark (or None if no subjects), status, and grade.
        """
        if len(self.subjects) == 0:
            return None, "N/A", "N/A"

        total_mark = 0

        for subject in self.subjects:
            total_mark += subject.mark

        average = total_mark / len(self.subjects)

        # Calculate overall grade
        grade = calculate_grade(average)

        # Calculate overall status
        if average >= constants.P_THRESHOLD:
            status = "PASS"
        else:
            status = "FAIL"

        return average, status, grade


