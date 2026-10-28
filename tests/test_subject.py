import unittest
from unittest.mock import patch

from models.student import Student
from models.subject import Subject


class TestGrading(unittest.TestCase):
    def test_subject_and_overall_grade_boundaries_agree(self):
        for mark, grade in (
            (25, "Z"), (49.99, "Z"), (50, "P"), (64.99, "P"),
            (65, "C"), (74.99, "C"), (75, "D"), (84.99, "D"),
            (85, "HD"), (100, "HD")
        ):
            with self.subTest(mark=mark):
                subject = Subject("001", mark)
                student = Student(
                    "000001", "Example", "example@university.com",
                    "Password123", [subject]
                )
                expected_status = "PASS" if mark >= 50 else "FAIL"
                self.assertEqual(subject.grade, grade)
                self.assertEqual(subject.get_pass_fail_status(), expected_status)
                self.assertEqual(student.get_overall_status(), (mark, expected_status, grade))

    def test_subject_and_overall_use_the_same_threshold_constants(self):
        with patch("utils.constants.P_THRESHOLD", 55):
            subject = Subject("001", 52)
            student = Student(
                "000001", "Example", "example@university.com",
                "Password123", [subject]
            )
            self.assertEqual(subject.grade, "Z")
            self.assertEqual(subject.get_pass_fail_status(), "FAIL")
            self.assertEqual(student.get_overall_status(), (52, "FAIL", "Z"))
