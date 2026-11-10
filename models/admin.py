class Admin:
    """ Represents an admin user with an ID, name, email, and password."""
    def __init__(
        self,
        admin_id: str,
        name: str,
        email: str,
        password: str
    ) -> None:
        self.admin_id = admin_id
        self.name = name
        self.email = email
        self.password = password

    def change_password(self, new_password: str) -> None:
        self.password = new_password
