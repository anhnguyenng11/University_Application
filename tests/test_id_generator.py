import unittest
from unittest.mock import patch

from utils.id_generator import IDGenerator


class TestIDGenerator(unittest.TestCase):
    def test_id_bounds_and_collision_wraparound(self):
        for generate, digits, maximum in (
            (IDGenerator.generate_student_id, 6, 999999),
            (IDGenerator.generate_subject_id, 3, 999)
        ):
            with self.subTest(digits=digits):
                with patch("utils.id_generator.random.randint", return_value=1) as draw:
                    self.assertEqual(generate(set()), str(1).zfill(digits))
                    draw.assert_called_once_with(1, maximum)
                with patch("utils.id_generator.random.randint", return_value=maximum):
                    self.assertEqual(generate(set()), str(maximum))
                    occupied = {str(maximum), str(1).zfill(digits)}
                    self.assertEqual(generate(occupied), str(2).zfill(digits))

    def test_exhausted_subject_ids_raise_without_drawing(self):
        occupied = {str(number).zfill(3) for number in range(1, 1000)}
        with patch("utils.id_generator.random.randint") as draw:
            with self.assertRaisesRegex(ValueError, "No available subject IDs"):
                IDGenerator.generate_subject_id(occupied)
            draw.assert_not_called()
