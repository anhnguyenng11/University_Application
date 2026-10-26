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
                admin_id=admin_data["admin_id"],
                name=admin_data["name"],
                email=admin_data["email"],
                password=admin_data["password"]
            )
            admins.append(admin)

        return admins

    def find_admin_by_email(self, email: str) -> Admin | None:
        admins = self.load_admins()
    
        for admin in admins:
            if admin.email.lower() == email.lower():
                return admin
    
        return None

    def save_admins(self, admins: list[Admin]) -> None:
        data = {"admins": []}

        for admin in admins:
            admin_data = {
                "admin_id": admin.admin_id,
                "name": admin.name,
                "email": admin.email,
                "password": admin.password
            }
            data["admins"].append(admin_data)

        self.database.save_data(data)