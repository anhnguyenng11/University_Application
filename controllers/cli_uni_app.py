
from views.cli_view import CLIView


class CLIUniApp:
    def __init__(self, view: CLIView) -> None:
        self.view = view

    def start(self) -> None:
        self.show_main_menu()

    def show_main_menu(self) -> None:
        while True:
            choice = self.view.show_main_menu()

            if choice == "A":
                self.view.show_message("Admin login is not implemented yet.")

            elif choice == "S":
                self.view.show_message("Student menu is not implemented yet.")

            elif choice == "X":
                self.view.show_message("Exiting University System.")
                return
            else:
                self.view.show_message("Invalid option. Please try again.")
