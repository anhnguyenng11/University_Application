
from views.cli_view import CLIView


class AdminController:
    def __init__(self, view: CLIView) -> None:
        self.view = view

    def start(self) -> None:
        self.view.show_message(
            "Admin login is not implemented yet."
        )
