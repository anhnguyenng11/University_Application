
from views.cli_view import CLIView
from controllers.cli_uni_app import CLIUniApp


def main() -> None:
    view = CLIView()
    app = CLIUniApp(view)
    app.start()


if __name__ == "__main__":
    main()
