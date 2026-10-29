"""
This module contains the CLIView class, which provides methods for displaying reusable messages and prompts in CLI application.
"""
class CLIView():
    """
    Provides methods for displaying reusable messages and prompts in CLI application.
    Methods:
    - show_message: Displays a message to the user in the CLI.
    - show_welcome: Displays a welcome message to the user after successful login.
    - get_login_details: Prompts the user for login details (email and password) based on their role.
    - show_main_menu: Displays the main menu of the university application and prompts the user for their choice.
    """

    def show_message(self, message: str) -> None:
        """
        Displays a message to the user in the CLI.
        """
        print(message)
    
    def show_welcome(self, name: str, account_id: str, role: str) -> None:
        """
        Displays a welcome message to the user after successful login.
        """
        print("\nWelcome, " + name + "!")
        print(f"{role} ID:", account_id)
    
    def get_login_details(self, role: str) -> tuple[str, str]:
        """
        Prompts the user for login details (email and password) based on their role.
        """
        print(f"\n{role} Login")
        email = input("Email: ")
        password = input("Password: ")

        return email, password
    
    def show_main_menu(self) -> str:
        """
        Displays the main menu of the university application and prompts the user for their choice.
        """
        print("\nUniversity System")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")

        choice = input("University System (A/S/X): ")
        return choice.strip().upper()