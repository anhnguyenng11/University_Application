from views.cli.base_cli_view import BaseCLIView


class AdminView(BaseCLIView):
    def show_admin_menu(self) -> str:
        print("\nAdmin System")
        print("(c) Clear Database")
        print("(g) Group Students")
        print("(p) Partition Students")
        print("(r) Remove Student")
        print("(s) Show Students")
        print("(x) Exit")

        return input("Enter choice: ").strip().lower()