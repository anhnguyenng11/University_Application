
import random


class IDGenerator:
    @staticmethod
    def generate_student_id(existing_ids: set[str]) -> str:
        return IDGenerator._generate_id(existing_ids, 6, "student")

    @staticmethod
    def generate_subject_id(existing_ids: set[str]) -> str:
        return IDGenerator._generate_id(existing_ids, 3, "subject")

    @staticmethod
    def _generate_id(existing_ids: set[str], digits: int, label: str) -> str:
        maximum = 10 ** digits - 1
        if len(existing_ids) >= maximum:
            raise ValueError(f"No available {label} IDs.")

        number = random.randint(1, maximum)
        start_number = number

        while True:
            generated_id = str(number).zfill(digits)

            if generated_id not in existing_ids:
                return generated_id

            number = (number % maximum) + 1

            if number == start_number:
                raise ValueError(f"No available {label} IDs.")

    @staticmethod
    def generate_mark() -> int:
        return random.randint(25, 100)
