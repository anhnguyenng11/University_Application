class CLIView:
    def show_main_menu(self) -> str:
        print("\nUniversity System")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")

        return input("Enter (A/S/X): ").strip().upper()

    def show_message(self, message: str) -> None:
        print(message)