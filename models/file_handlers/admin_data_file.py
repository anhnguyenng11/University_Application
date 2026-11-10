from models.admin import Admin
from models.file_handlers.database import Database
from utils import constants

class AdminDataFile:
    """
    AdminDataFile is responsible for handling the storage and retrieval of admin data.
    Methods:
    - load_admins: Loads the list of Admin objects from the database.
    - find_admin_by_email: Finds an Admin object by email.
    - update_admin: Updates an Admin object in the database.
    """
    
    def __init__(self, data_folder=None) -> None:
        """
        Initializes the AdminDataFile for handling admin data.
        """
        self._database = Database(constants.ADMIN_DATABASE, {"admins": []}, data_folder)

    def load_admins(self) -> list[Admin]:
        """
        Loads the list of Admin objects from the database.
        Returns: A list of Admin objects.
        """
        data = self._database.load_data()
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
        """
        Finds an Admin object by email.
        Returns: The Admin object if found, otherwise None.
        """
        for admin in self.load_admins():
            if admin.email.lower() == email.lower():
                return admin

        return None

    def update_admin(self, updated_admin: Admin) -> bool:
        """
        Updates an Admin object in the database.
        Returns: True if the update is successful, otherwise False.
        """
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
                self._database.save_data({"admins": records})
                return True

        return False
