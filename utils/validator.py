
import re


class Validator:
    @staticmethod
    def is_not_empty(value: str) -> bool:
        if not isinstance(value, str):
            return False

        if value.strip() == "":
            return False

        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not Validator.is_not_empty(email):
            return False

        pattern = r"[A-Za-z0-9._%+-]+@university\.com"

        if re.fullmatch(pattern, email) is None:
            return False

        return True

    @staticmethod
    def is_valid_password(password: str) -> bool:
        if not Validator.is_not_empty(password):
            return False

        if len(password) < 8:
            return False

        if re.search(r"\s", password):
            return False

        if re.search(r"[A-Z]", password) is None:
            return False

        if re.search(r"[a-z]", password) is None:
            return False

        if re.search(r"[0-9]", password) is None:
            return False

        if re.search(r"[^\w\s]|_", password) is None:
            return False

        return True
