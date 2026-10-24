from views.base_cli_view import BaseCLIView

class CLIView(BaseCLIView):
    def show_main_menu(self) -> str:
        print("\nUniversity System")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")

        choice = input("University System (A/S/X): ")
        return choice.strip().upper()