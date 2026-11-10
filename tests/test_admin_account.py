import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from controllers.gui.gui_admin_controller import GUIAdminController
from models.admin import Admin
from models.admin_service import AdminService
from models.file_handlers.admin_data_file import AdminDataFile
from views.gui.account_view import AccountView


class TestAdminPassword(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "admins.data"
        self.records = [
            {"admin_id": "001", "name": "Admin One",
             "email": "one@university.com", "password": "Oldpass123"},
            {"admin_id": "002", "name": "Admin Two",
             "email": "two@university.com", "password": "Otherpass123"}
        ]
        self.path.write_text(json.dumps({"admins": self.records}))
        self.original = self.path.read_bytes()
        self.storage = AdminDataFile(folder.name)
        self.students = Mock()
        self.service = AdminService(self.storage, self.students)
        self.admin = self.service.login("one@university.com", "Oldpass123")

    def test_login_rejects_unknown_email_before_checking_password(self):
        with self.assertRaisesRegex(ValueError, "Admin email not found"):
            self.service.login("missing@university.com", "Wrongpass123")

    def test_change_persists_and_preserves_other_accounts(self):
        self.service.change_password(self.admin, "Oldpass123", "Newpass456")

        expected = [dict(record) for record in self.records]
        expected[0]["password"] = "Newpass456"
        self.assertEqual(json.loads(self.path.read_text()), {"admins": expected})
        self.assertEqual(self.admin.password, "Newpass456")
        fresh_service = AdminService(AdminDataFile(self.path.parent), self.students)
        self.assertIsNotNone(fresh_service.login(self.admin.email, "Newpass456"))
        with self.assertRaisesRegex(ValueError, "Wrong password"):
            fresh_service.login(self.admin.email, "Oldpass123")
        self.assertEqual(self.students.mock_calls, [])

    def test_invalid_passwords_leave_file_and_session_unchanged(self):
        for current, new in (
            ("wrong", "Newpass456"),
            (" Oldpass123 ", "Newpass456"),
            ("Oldpass123", ""),
            ("Oldpass123", "short"),
            ("Oldpass123", "Oldpass123")
        ):
            with self.subTest(current=current, new=new):
                with self.assertRaises(ValueError):
                    self.service.change_password(self.admin, current, new)
                self.assertEqual(self.path.read_bytes(), self.original)
                self.assertEqual(self.admin.password, "Oldpass123")

    def test_current_password_uses_saved_record(self):
        self.admin.password = "StalePassword"
        self.service.change_password(self.admin, "Oldpass123", "Newpass456")
        self.assertEqual(self.admin.password, "Newpass456")

    def test_missing_or_replaced_admin_is_not_updated(self):
        for email, admin_id in (("missing@university.com", "001"),
                                ("one@university.com", "999")):
            with self.subTest(email=email, admin_id=admin_id):
                admin = Admin(admin_id, "Missing", email, "Oldpass123")
                with self.assertRaisesRegex(ValueError, "Admin not found"):
                    self.service.change_password(admin, "Oldpass123", "Newpass456")
                self.assertEqual(self.path.read_bytes(), self.original)

    def test_failed_save_does_not_update_session(self):
        with patch.object(self.storage.database, "save_data", side_effect=OSError("Save failed")):
            with self.assertRaises(OSError):
                self.service.change_password(self.admin, "Oldpass123", "Newpass456")
        self.assertEqual(self.admin.password, "Oldpass123")
        self.assertEqual(self.path.read_bytes(), self.original)

        with patch.object(self.storage, "update_admin", return_value=False):
            with self.assertRaisesRegex(ValueError, "Could not save"):
                self.service.change_password(self.admin, "Oldpass123", "Newpass456")
        self.assertEqual(self.admin.password, "Oldpass123")

    def test_storage_rejects_missing_id_without_writing(self):
        admin = Admin("missing", "Missing", "missing@university.com", "Newpass456")
        self.assertFalse(self.storage.update_admin(admin))
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_corrupt_storage_is_not_overwritten(self):
        self.path.write_text('{"admins": [}')
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.storage.update_admin(self.admin)
        self.assertEqual(self.path.read_bytes(), original)


class TestAdminAccountController(unittest.TestCase):
    def setUp(self):
        self.service = Mock()
        self.error = Mock()
        self.success = Mock()
        self.controller = GUIAdminController(
            None, self.service, Mock(), Mock(), self.error, self.success
        )
        self.controller.active_account = Admin(
            "001", "Test Admin", "admin@university.com", "Oldpass123"
        )
        self.controller.main_view = Mock()

    def test_main_page_preserves_navigation_and_opens_students(self):
        with patch("controllers.gui.gui_admin_controller.MainView") as view:
            with patch.object(self.controller, "show_students") as students:
                self.controller.show_admin_main()
                view.assert_called_once_with(
                    None,
                    title="Admin Portal",
                    navigation=(
                        ("View Students", students),
                        ("Search Students", self.controller.show_search_students),
                        ("Account", self.controller.show_account)
                    ),
                    on_logout=self.controller.logout
                )
                self.controller.show_view.assert_called_once_with(view.return_value)
                students.assert_called_once_with()

    def test_account_page_receives_admin_and_callback(self):
        with patch("controllers.gui.gui_admin_controller.AccountView") as view:
            self.controller.show_account()
            view.assert_called_once_with(
                self.controller.main_view.content_frame,
                information_title="Admin Information",
                information_rows=(
                    ("Name", self.controller.active_account.name),
                    ("Admin ID", self.controller.active_account.admin_id),
                    ("Email", self.controller.active_account.email)
                ),
                on_change_password=self.controller.change_password
            )
            self.controller.main_view.show_content.assert_called_once_with(view.return_value)

    def test_empty_or_mismatched_fields_do_not_call_service(self):
        for values in (("", "Newpass456", "Newpass456"),
                       ("Oldpass123", "", ""),
                       ("Oldpass123", "Newpass456", ""),
                       ("Oldpass123", "Newpass456", "Different789")):
            with self.subTest(values=values):
                self.error.reset_mock()
                self.controller.change_password(*values)
                self.error.assert_called_once()
                self.service.change_password.assert_not_called()
                self.success.assert_not_called()

    def test_service_errors_do_not_refresh_or_report_success(self):
        for error in (ValueError("Wrong current password"), OSError("Save failed")):
            with self.subTest(error=type(error).__name__):
                self.error.reset_mock()
                self.service.change_password.side_effect = error
                with patch.object(self.controller, "show_account") as refresh:
                    self.controller.change_password("Oldpass123", "Newpass456", "Newpass456")
                    refresh.assert_not_called()
                self.error.assert_called_once_with(str(error))
                self.success.assert_not_called()

    def test_success_refreshes_account_and_reports_success(self):
        with patch.object(self.controller, "show_account") as refresh:
            self.controller.change_password("Oldpass123", "Newpass456", "Newpass456")
            self.service.change_password.assert_called_once_with(
                self.controller.active_account, "Oldpass123", "Newpass456"
            )
            refresh.assert_called_once_with()
        self.success.assert_called_once_with("Password changed successfully.")
        self.error.assert_not_called()

    def test_account_form_submits_three_fields_in_order(self):
        view = AccountView.__new__(AccountView)
        view.on_change_password = Mock()
        values = ["Oldpass123", "Newpass456", "Newpass456"]
        view.current_password, view.new_password, view.confirm_password = [
            Mock(get=Mock(return_value=value)) for value in values
        ]
        view.submit_password()
        view.on_change_password.assert_called_once_with(*values)


if __name__ == "__main__":
    unittest.main()
