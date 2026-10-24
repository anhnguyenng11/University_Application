class BaseCLIView:
    def show_message(self, message: str) -> None:
        print(message)

    def wait_for_enter(self) -> None:
        input("\nPress Enter to continue...")