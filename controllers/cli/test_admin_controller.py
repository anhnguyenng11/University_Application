from views.cli.admin_view import AdminView


class AdminController:
    def __init__(self, view: AdminView) -> None:
        self.view = view

    def start(self) -> None:
        while True:
            choice = self.view.show_admin_menu()

            match choice:
                case "c":
                    self.view.show_message("Clear database not implemented.")

                case "g":
                    self.view.show_message("Group students not implemented.")

                case "p":
                    self.view.show_message("Partition students not implemented.")

                case "r":
                    self.view.show_message("Remove student not implemented.")

                case "s":
                    self.view.show_message("Show students not implemented.")

                case "x":
                    return

                case _:
                    self.view.show_message("Invalid option. Please try again.")