import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from models.file_handlers.student_data_file import StudentDataFile
from models.student import Student
from models.subject import Subject


class TestStudentDataFile(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)

        self.handler = StudentDataFile(folder.name)
        self.student_path = Path(folder.name) / "students.data"
        self.admin_path = Path(folder.name) / "admins.data"
        self.admin_path.write_text('{"admins": []}')
        self.admin_bytes = self.admin_path.read_bytes()

        self.handler.save_students([
            Student("000001", "Student One", "one@university.com",
                    "Password123", [Subject("001", 85)]),
            Student("000002", "Student Two", "two@university.com",
                    "Password456", [Subject("002", 40)])
        ])
        self.original = self.student_path.read_bytes()
        self.records = json.loads(self.original)["students"]

    def test_remove_preserves_remaining_student_and_subjects(self):
        self.assertTrue(self.handler.remove_student("000001"))

        students = self.handler.load_students()
        self.assertEqual([student.student_id for student in students], ["000002"])
        self.assertEqual(
            json.loads(self.student_path.read_text()),
            {"students": [self.records[1]]}
        )
        self.assertEqual(self.admin_path.read_bytes(), self.admin_bytes)

    def test_missing_student_does_not_write(self):
        with patch.object(self.handler, "save_students") as save:
            self.assertFalse(self.handler.remove_student("999999"))

        save.assert_not_called()
        self.assertEqual(self.student_path.read_bytes(), self.original)

    def test_clear_preserves_admin_file(self):
        self.handler.clear_all_students()

        self.assertEqual(self.handler.load_students(), [])
        self.assertEqual(
            json.loads(self.student_path.read_text()),
            {"students": []}
        )
        self.assertEqual(self.admin_path.read_bytes(), self.admin_bytes)

    def test_remove_and_clear_handle_empty_collection(self):
        self.handler.save_students([])

        self.assertFalse(self.handler.remove_student("000001"))
        self.handler.clear_all_students()
        self.assertEqual(self.handler.load_students(), [])

    def test_remove_reports_save_failure(self):
        with patch.object(
            self.handler, "save_students", side_effect=OSError("Save failed")
        ):
            with self.assertRaises(OSError):
                self.handler.remove_student("000001")

        self.assertEqual(self.student_path.read_bytes(), self.original)

    def test_clear_reports_save_failure(self):
        with patch.object(
            self.handler, "save_students", side_effect=OSError("Save failed")
        ):
            with self.assertRaises(OSError):
                self.handler.clear_all_students()

        self.assertEqual(self.student_path.read_bytes(), self.original)


if __name__ == "__main__":
    unittest.main()