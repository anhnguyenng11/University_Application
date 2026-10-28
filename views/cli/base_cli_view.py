class BaseCLIView:
    def show_message(self, message: str) -> None:
        print(message)

    def show_welcome(self, name: str, account_id: str, role: str) -> None:
        print("\nWelcome, " + name + "!")
        print(f"{role} ID:", account_id)

    def get_login_details(self, role: str) -> tuple[str, str]:
        print(f"\n{role} Login")

        email = input("Email: ")
        password = input("Password: ")

        return email, password
