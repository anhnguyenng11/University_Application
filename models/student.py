
from models.subject import Subject


class Student:
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

        if len(self.subjects) > 4:
            raise ValueError("Maximum 4 subjects allowed.")

    def can_enroll(self) -> bool:
        if len(self.subjects) < 4:
            return True
        else:
            return False

    def add_subject(self, subject: Subject) -> bool:
        if not self.can_enroll():
            return False

        for existing_subject in self.subjects:
            if existing_subject.subject_id == subject.subject_id:
                return False

        self.subjects.append(subject)
        return True

    def remove_subject(self, subject_id: str) -> bool:
        for subject in self.subjects:
            if subject.subject_id == subject_id:
                self.subjects.remove(subject)
                return True

        return False

    def change_password(self, new_password: str) -> None:
        self.password = new_password



    def get_overall_status(self) -> tuple[float | None, str, str]:
        if len(self.subjects) == 0:
            return None, "N/A", "N/A"

        total_mark = 0

        for subject in self.subjects:
            total_mark += subject.mark

        average = total_mark / len(self.subjects)

        # Calculate overall grade
        if average < 50:
            grade = "Z"
        elif average < 65:
            grade = "P"
        elif average < 75:
            grade = "C"
        elif average < 85:
            grade = "D"
        else:
            grade = "HD"

        # Calculate overall status
        if average >= 50:
            status = "PASS"
        else:
            status = "FAIL"

        return average, status, grade


