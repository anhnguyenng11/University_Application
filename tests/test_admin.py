
import unittest

from models.admin import Admin


class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.admin = Admin(
            "001",
            "System Admin",
            "admin@university.com",
            "Password123"
        )

    def test_admin_attributes(self):
        self.assertEqual(self.admin.admin_id, "001")
        self.assertEqual(self.admin.name, "System Admin")
        self.assertEqual(self.admin.email, "admin@university.com")
        self.assertEqual(self.admin.password, "Password123")

    def test_change_password(self):
        self.admin.change_password("Newpassword123")

        self.assertEqual(
            self.admin.password,
            "Newpassword123"
        )


if __name__ == "__main__":
    unittest.main()
