
import unittest

from utils.validator import Validator


class TestValidator(unittest.TestCase):

    def test_valid_email(self):
        email = "john.smith@university.com"

        self.assertTrue(Validator.is_valid_email(email))

    def test_invalid_email(self):
        self.assertFalse(
            Validator.is_valid_email("john@gmail.com")
        )

        self.assertFalse(
            Validator.is_valid_email("john@university.au")
        )

        self.assertFalse(
            Validator.is_valid_email("john@student.uts.edu.au")
        )

    def test_valid_password(self):
        password = "Helloworld123"
        self.assertTrue(Validator.is_valid_password(password))
        

    def test_invalid_password(self):
        self.assertFalse(
            Validator.is_valid_password("helloworld12")
        )

        self.assertFalse(
            Validator.is_valid_password("HELLOWORLD123!")
        )

        self.assertFalse(
            Validator.is_valid_password("Helloworld12")
        )

        self.assertFalse(
            Validator.is_valid_password("HELLOWORLD!!!")
        )

        self.assertFalse(
            Validator.is_valid_password("Pass1!")
        )

    def test_empty_input(self):
        self.assertFalse(Validator.is_not_empty(""))
        self.assertFalse(Validator.is_not_empty("   "))
        self.assertTrue(Validator.is_not_empty("John"))


if __name__ == "__main__":
    unittest.main()
