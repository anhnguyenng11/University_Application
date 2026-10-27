from models.file_handlers.database import Database
from models.admin import Admin


class AdminDataFile:

    def __init__(self, data_folder=None) -> None:
        
        self.database = Database(
            "admins.data",
            {"admins": []},
            data_folder
        )

    def load_admins(self) -> list[Admin]:
        
        data = self.database.load_data()
        
        admins = []

        for admin_data in data["admins"]:
            admin = Admin(
                admin_data["admin_id"],
                admin_data["name"],
                admin_data["email"],
                admin_data["password"]
            )
            admins.append(admin)

        return admins

    def find_admin_by_email(self, email: str) -> Admin | None:

        for admin in self.load_admins():
            if admin.email.lower() == email.lower():
                return admin

        # Not found
        return None