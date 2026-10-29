from models.admin import Admin
from models.file_handlers.database import Database
from utils.constants import ADMIN_DATABASE


class AdminDataFile:
    def __init__(self, data_folder=None) -> None:
        self.database = Database(
            ADMIN_DATABASE,
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

    def update_admin(self, updated_admin: Admin) -> bool:
        admins = self.load_admins()

        for index, admin in enumerate(admins):
            if admin.admin_id == updated_admin.admin_id:
                admins[index] = updated_admin
                records = [
                    {
                        "admin_id": item.admin_id,
                        "name": item.name,
                        "email": item.email,
                        "password": item.password
                    }
                    for item in admins
                ]
                self.database.save_data({"admins": records})
                return True

        return False
