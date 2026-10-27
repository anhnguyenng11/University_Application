from utils import constants
class Subject:
    def __init__(self, subject_id: str, mark: int) -> None:
        self.subject_id = subject_id
        self.mark = mark
        self.grade = self.calculate_grade()

    def calculate_grade(self) -> str:
        if self.mark < constants.P_THRESHOLD:
            return "Z"
        elif self.mark < constants.C_THRESHOLD:
            return "P"
        elif self.mark < constants.D_THRESHOLD:
            return "C"
        elif self.mark < constants.HD_THRESHOLD:
            return "D"
        return "HD"

    def get_pass_fail_status(self) -> str:
        if self.mark >= constants.P_THRESHOLD:
            return "PASS"
        else:
            return "FAIL"