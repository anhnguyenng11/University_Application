
import re
import utils.constants as constants


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

        pattern = constants.EMAIL_REGEX

        if re.fullmatch(pattern, email) is None:
            return False

        return True

    @staticmethod
    def is_valid_password(password: str) -> bool:
        if not Validator.is_not_empty(password):
            return False
        pattern = constants.PASSWORD_REGEX
        return re.fullmatch(pattern, password) is not None
