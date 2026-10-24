class Subject:
    def __init__(self, subject_id: str, mark: int) -> None:
        self.subject_id = subject_id
        self.mark = mark
        self.grade = self.calculate_grade()

    def calculate_grade(self) -> str:
        if self.mark < 50:
            return "Z"
        elif self.mark < 65:
            return "P"
        elif self.mark < 75:
            return "C"
        elif self.mark < 85:
            return "D"
        return "HD"

    def get_pass_fail_status(self) -> str:
        if self.mark >= 50:
            return True
        else:
            return False