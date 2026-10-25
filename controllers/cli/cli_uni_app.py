
from views.cli.cli_view import CLIView
from controllers.cli.student_controller import StudentController
from controllers.cli.admin_controller import AdminController


class CLIUniApp:
    def __init__(
        self,
        view: CLIView,
        student_controller: StudentController,
        admin_controller: AdminController
    ) -> None:
        self.view = view
        self.student_controller = student_controller
        self.admin_controller = admin_controller

    def start(self) -> None:
        while True:
            choice = self.view.show_main_menu()

            match choice:
                case "A":
                    self.admin_controller.start()

                case "S":
                    self.student_controller.start()

                case "X":
                    self.view.show_message("Exiting University System.")
                    return

                case _:
                    self.view.show_message("Invalid option. Please try again.")

