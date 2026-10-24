
import random


class IDGenerator:
    @staticmethod
    def generate_student_id(existing_ids: set[str]) -> str:
        if len(existing_ids) >= 99999999:
            raise ValueError("No available student IDs.")

        number = random.randint(1, 99999999)
        start_number = number

        while True:
            student_id = str(number).zfill(8)

            if student_id not in existing_ids:
                return student_id

            number += 1

            if number > 99999999:
                number = 1

            if number == start_number:
                raise ValueError("No available student IDs.")

    @staticmethod
    def generate_subject_id(existing_ids: set[str]) -> str:
        if len(existing_ids) >= 99999:
            raise ValueError("No available subject IDs.")

        number = random.randint(1, 99999)
        start_number = number

        while True:
            subject_id = str(number).zfill(5)

            if subject_id not in existing_ids:
                return subject_id

            number += 1

            if number > 99999:
                number = 1

            if number == start_number:
                raise ValueError("No available subject IDs.")

    @staticmethod
    def generate_mark() -> int:
        mark = random.randint(25, 100)
        return mark
