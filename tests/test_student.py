
import unittest

from models.student import Student
from models.subject import Subject


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(
            "000001",
            "John Smith",
            "john@university.com",
            "Password123"
        )

    def test_enrollment_limit(self):
        self.assertTrue(self.student.add_subject(Subject("001", 60)))
        self.assertTrue(self.student.add_subject(Subject("002", 70)))
        self.assertTrue(self.student.add_subject(Subject("003", 80)))
        self.assertTrue(self.student.add_subject(Subject("004", 90)))

        self.assertFalse(self.student.can_enroll())
        self.assertFalse(self.student.add_subject(Subject("005", 50)))

        self.assertEqual(len(self.student.subjects), 4)

    def test_duplicate_subject(self):
        self.student.add_subject(Subject("001", 60))

        result = self.student.add_subject(Subject("001", 80))

        self.assertFalse(result)
        self.assertEqual(len(self.student.subjects), 1)

    def test_average_mark(self):
        self.student.add_subject(Subject("001", 40))
        self.student.add_subject(Subject("002", 60))

        self.assertEqual(self.student.average_mark(), 50.0)

        self.student.remove_subject("001")

        self.assertEqual(self.student.average_mark(), 60.0)

    def test_overall_status(self):
        self.assertEqual(self.student.get_overall_status(), "PENDING")

        self.student.add_subject(Subject("001", 40))
        self.student.add_subject(Subject("002", 55))
        self.student.add_subject(Subject("003", 70))
        self.student.add_subject(Subject("004", 75))

        self.assertEqual(self.student.average_mark(), 60.0)
        self.assertEqual(self.student.get_overall_status(), "PASS")

    def test_change_password(self):
        self.student.change_password("Newpassword123")

        self.assertEqual(self.student.password, "Newpassword123")


if __name__ == "__main__":
    unittest.main()
