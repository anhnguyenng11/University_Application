from models.admin import Admin
from models.file_handlers.admin_data_file import AdminDataFile

class AdminService:
    def __init__(self, admin_data_file: AdminDataFile) -> None:
        self.admin_data_file = admin_data_file

    def login(self, email: str, password: str) -> Admin | None:
        email = email.strip()
    
        admin = self.admin_data_file.find_admin_by_email(email)
    
        if admin is None:
            return None
    
        if admin.password != password:
            return None
    
        return admin