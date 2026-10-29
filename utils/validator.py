"""
Validates user input.
"""
import re
from utils import constants


class Validator:
    @staticmethod
    def is_not_empty(value: str) -> bool:
        """
        Checks if the given value is not empty or None.
        """
        if not isinstance(value, str):
            return False

        if value.strip() == "":
            return False

        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates the email format using a regular expression.
        """
        if not Validator.is_not_empty(email):
            return False

        pattern = constants.EMAIL_REGEX

        return re.fullmatch(pattern, email) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Validates the password format using a regular expression.
        """
        if not Validator.is_not_empty(password):
            return False
        pattern = constants.PASSWORD_REGEX
        return re.fullmatch(pattern, password) is not None
