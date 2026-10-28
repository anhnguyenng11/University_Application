import unittest
from tempfile import TemporaryDirectory

from models.file_handlers.student_data_file import StudentDataFile
from models.student_service import StudentService


class TestStudentService(unittest.TestCase):
    def setUp(self):
        # throwaway folder so real students.data is safe
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)

        self.data_file = StudentDataFile(folder.name)
        self.service = StudentService(self.data_file)

    def test_register_success(self):
        student = self.service.register(
            "Test Student",
            "test@university.com",
            "Password123"
        )

        self.assertEqual(student.name, "Test Student")
        self.assertEqual(student.email, "test@university.com")
        self.assertEqual(len(student.student_id), 6)

        # saved in the temp file
        saved = self.data_file.find_student_by_email("test@university.com")
        self.assertIsNotNone(saved)
        self.assertEqual(saved.student_id, student.student_id)

    def test_register_rejects_empty_name(self):
        with self.assertRaises(ValueError) as error:
            self.service.register("   ", "test@university.com", "Password123")

        self.assertIn("Name cannot be empty", str(error.exception))

    def test_register_rejects_invalid_email(self):
        with self.assertRaises(ValueError):
            self.service.register(
                "Test Student",
                "test@gmail.com",
                "Password123"
            )

    def test_register_rejects_invalid_password(self):
        with self.assertRaises(ValueError):
            self.service.register(
                "Test Student",
                "test@university.com",
                "short1"
            )

    def test_register_rejects_duplicate_email(self):
        self.service.register(
            "First Student",
            "same@university.com",
            "Password123"
        )

        with self.assertRaises(ValueError) as error:
            self.service.register(
                "Second Student",
                "same@university.com",
                "Password456"
            )

        self.assertIn("Email already registered", str(error.exception))

    def test_login_success_and_failure(self):
        self.service.register(
            "Login Student",
            "login@university.com",
            "Password123"
        )

        ok = self.service.login("login@university.com", "Password123")

        self.assertIsNotNone(ok)
        self.assertEqual(ok.email, "login@university.com")
        with self.assertRaisesRegex(ValueError, "Wrong password"):
            self.service.login("login@university.com", "Wrongpass123")
        with self.assertRaisesRegex(ValueError, "Student email not found"):
            self.service.login("missing@university.com", "Wrongpass123")

    def test_enroll_up_to_four_then_block(self):
        student = self.service.register(
            "Enrol Student",
            "enrol@university.com",
            "Password123"
        )

        for count in range(4):
            subject = self.service.enroll_subject(student)
            self.assertEqual(len(subject.subject_id), 3)
            self.assertGreaterEqual(subject.mark, 25)
            self.assertLessEqual(subject.mark, 100)

        self.assertEqual(len(student.subjects), 4)

        with self.assertRaises(ValueError) as error:
            self.service.enroll_subject(student)

        self.assertIn("Maximum 4 subjects", str(error.exception))

    def test_remove_subject_success_and_missing(self):
        student = self.service.register(
            "Remove Student",
            "remove@university.com",
            "Password123"
        )
        subject = self.service.enroll_subject(student)

        self.assertTrue(
            self.service.remove_subject(student, subject.subject_id)
        )
        self.assertEqual(len(student.subjects), 0)

        with self.assertRaises(ValueError) as error:
            self.service.remove_subject(student, "999")

        self.assertIn("Subject not found", str(error.exception))

    def test_change_password_success_and_errors(self):
        student = self.service.register(
            "Password Student",
            "password@university.com",
            "Password123"
        )

        # wrong current password
        with self.assertRaises(ValueError):
            self.service.change_password(
                student,
                "Wrongpass123",
                "Newpass123"
            )

        # same as old password
        with self.assertRaises(ValueError) as error:
            self.service.change_password(
                student,
                "Password123",
                "Password123"
            )
        self.assertIn("must be different", str(error.exception))

        # success
        self.service.change_password(
            student,
            "Password123",
            "Newpass123"
        )

        with self.assertRaisesRegex(ValueError, "Wrong password"):
            self.service.login("password@university.com", "Password123")
        self.assertIsNotNone(
            self.service.login("password@university.com", "Newpass123")
        )


if __name__ == "__main__":
    unittest.main()
