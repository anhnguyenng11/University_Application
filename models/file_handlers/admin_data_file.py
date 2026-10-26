from pathlib import Path

from models.admin import Admin
from models.file_handlers.database import Database


class AdminDataFile:
    def __init__(self, data_folder=None) -> None:
        if data_folder is None:
            data_folder = Path(__file__).resolve().parents[2] / "data"

        file_path = Path(data_folder) / "admins.data"

        # Database resets empty files, so reject an existing empty Admin file first.
        if file_path.exists() and file_path.stat().st_size == 0:
            raise ValueError("Admin data file is empty.")

        self.database = Database(
            "admins.data",
            {"admins": []},
            data_folder
        )

    def load_admins(self) -> list[Admin]:
        data = self.database.load_data()
        records = data.get("admins")

        if not isinstance(records, list):
            raise ValueError("Admin data must contain an admins list.")

        admins = []
        admin_ids = set()
        emails = set()

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each Admin record must be an object.")

            for field in ("admin_id", "name", "email", "password"):
                value = record.get(field)

                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"Admin field '{field}' must be a nonempty string.")

            admin_id = record["admin_id"]
            email = record["email"].lower()

            if admin_id in admin_ids or email in emails:
                raise ValueError("Duplicate Admin ID or email.")

            admin_ids.add(admin_id)
            emails.add(email)

            admin = Admin(
                record["admin_id"],
                record["name"],
                record["email"],
                record["password"]
            )
            admins.append(admin)

        return admins

    def find_admin_by_email(self, email: str) -> Admin | None:
        for admin in self.load_admins():
            if admin.email.lower() == email.lower():
                return admin

        return None