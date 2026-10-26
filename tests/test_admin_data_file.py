import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from models.file_handlers.admin_data_file import AdminDataFile


class TestAdminDataFile(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)

        self.path = Path(folder.name) / "admins.data"
        self.record = {
            "admin_id": "001",
            "name": "Test Admin",
            "email": "admin@university.com",
            "password": "Demo@123"
        }
        self.path.write_text(json.dumps({"admins": [self.record]}))
        self.handler = AdminDataFile(folder.name)

    def test_load_preserves_account_fields(self):
        original = self.path.read_bytes()
        admins = self.handler.load_admins()

        self.assertEqual(len(admins), 1)
        self.assertEqual(vars(admins[0]), self.record)
        self.assertEqual(self.path.read_bytes(), original)

    def test_find_email_is_case_insensitive(self):
        admin = self.handler.find_admin_by_email("ADMIN@UNIVERSITY.COM")

        self.assertIsNotNone(admin)
        self.assertEqual(admin.admin_id, "001")

    def test_unknown_email_returns_none(self):
        admin = self.handler.find_admin_by_email("missing@university.com")

        self.assertIsNone(admin)

    def test_empty_collection_returns_empty_list(self):
        self.path.write_text('{"admins": []}')

        self.assertEqual(self.handler.load_admins(), [])

    def test_invalid_json_is_not_overwritten(self):
        self.path.write_text('{"admins": [}')
        original = self.path.read_bytes()

        with self.assertRaises(ValueError):
            self.handler.load_admins()

        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_collection_or_record_is_rejected(self):
        for data in ([], {}, {"admins": {}}, {"admins": [None]}):
            with self.subTest(data=data):
                self.path.write_text(json.dumps(data))
                original = self.path.read_bytes()

                with self.assertRaises(ValueError):
                    self.handler.load_admins()

                self.assertEqual(self.path.read_bytes(), original)

    def test_missing_or_invalid_fields_are_rejected(self):
        for field in self.record:
            for value in (None, 123, "", "   "):
                with self.subTest(field=field, value=value):
                    record = self.record.copy()
                    record[field] = value
                    self.path.write_text(json.dumps({"admins": [record]}))

                    with self.assertRaises(ValueError):
                        self.handler.load_admins()

            with self.subTest(missing=field):
                record = self.record.copy()
                del record[field]
                self.path.write_text(json.dumps({"admins": [record]}))

                with self.assertRaises(ValueError):
                    self.handler.load_admins()

    def test_duplicate_id_or_email_is_rejected(self):
        for field, value in (
            ("admin_id", "001"),
            ("email", "ADMIN@UNIVERSITY.COM")
        ):
            with self.subTest(field=field):
                duplicate = self.record.copy()
                duplicate["admin_id"] = "002"
                duplicate["email"] = "other@university.com"
                duplicate[field] = value
                self.path.write_text(json.dumps({
                    "admins": [self.record, duplicate]
                }))

                with self.assertRaises(ValueError):
                    self.handler.load_admins()


if __name__ == "__main__":
    unittest.main()