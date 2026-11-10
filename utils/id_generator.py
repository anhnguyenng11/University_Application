"""
Generates unique IDs for students and subjects.
"""
import random
from utils import constants

class IDGenerator:
    """
    A class responsible for generating unique IDs for students and subjects.
    Methods:
    - generate_student_id: Generates a unique student ID that is not in the existing_ids set.
    - generate_subject_id: Generates a unique subject ID that is not in the existing_ids set.
    - generate_mark: Generates a random mark between 25 and 100.
    """
    @staticmethod
    def generate_student_id(existing_ids: set[str]) -> str:
        """
        Generates a unique student ID that is not in the existing_ids set.
        """
        return IDGenerator._generate_id(existing_ids, constants.STUDENT_ID_LENGTH, "student")

    @staticmethod
    def generate_subject_id(existing_ids: set[str]) -> str:
        """
        Generates a unique subject ID that is not in the existing_ids set.
        """
        return IDGenerator._generate_id(existing_ids, constants.SUBJECT_ID_LENGTH, "subject")

    @staticmethod
    def _generate_id(existing_ids: set[str], digits: int, label: str) -> str:
        """
        Generates a unique ID with the specified number of digits that is not in the existing_ids set.
        """
        maximum = 10 ** digits - 1
        if len(existing_ids) >= maximum:
            raise ValueError(f"No available {label} IDs.")

        # Start generating an ID from a random number
        number = random.randint(1, maximum)
        start_number = number

        while True:
            # zfill the number with leading zeros to match the required digit length
            generated_id = str(number).zfill(digits)

            if generated_id not in existing_ids:
                return generated_id

            # Select the next number, wrap around if it exceeds the maximum
            number = (number % maximum) + 1

            # If we have looped through all possible IDs and returned to the starting number, raise an error
            if number == start_number:
                raise ValueError(f"No available {label} IDs.")

    @staticmethod
    def generate_mark() -> int:
        """
        Generates a random mark between 25 and 100.
        """
        return random.randint(25, 100)
