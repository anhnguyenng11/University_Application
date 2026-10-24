class Subject:
    def __init__(self, subject_id: str, mark: int) -> None:
        if not (subject_id.isdigit() and len(subject_id) == 3
                and 1 <= int(subject_id) <= 999):
            raise ValueError("Invalid subject ID.")

        if not isinstance(mark, int) or isinstance(mark, bool) or not 25 <= mark <= 100:
            raise ValueError("Mark must be between 25 and 100.")

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
        else:
            return "HD"

    def get_pass_fail_status(self) -> str:
        return "PASS" if self.mark >= 50 else "FAIL"
