class BaseGUIController:
    """
    Base class for GUI controllers, providing common functionality for managing views and handling user interactions.
    Children: GUIStudentController, GUIAdminController
    """
    def __init__(self, root, service, show_view, on_exit, on_error, on_success):
        self.root = root
        self.service = service
        self.show_view = show_view
        self.on_exit = on_exit
        self.on_error = on_error
        self.on_success = on_success
        self.active_account = None

    def change_password(self, current_password, new_password, confirm_password):
        if not current_password or not new_password or not confirm_password:
            self.on_error("All password fields are required.")
            return

        if new_password != confirm_password:
            self.on_error("Passwords do not match.")
            return

        try:
            self.service.change_password(
                self.active_account, current_password, new_password
            )
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.show_account()
        self.on_success("Password changed successfully.")
