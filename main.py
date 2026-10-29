"""
This is the main entry point of the application. It initializes the models, views, and controllers, and starts the CLI application.
"""
from views import CLIView, StudentView, AdminView
from controllers import CLIUniApp, StudentController, AdminController
from models import StudentService, StudentDataFile, AdminService, AdminDataFile

def main() -> None:
    """
    Main function to initialize and start the university application CLI.
    """

    # Models
        # Getting data files ready for use
    student_data_file = StudentDataFile()
    admin_data_file = AdminDataFile()

        # Passing data files to services for logic handling
    student_service = StudentService(student_data_file)
    admin_service = AdminService(
        admin_data_file, 
        student_data_file
    )

    # Views
    cli_view = CLIView()
    student_view = StudentView()
    admin_view = AdminView()

    # Controllers
    student_controller = StudentController(
        student_view,
        student_service
    )

    admin_controller = AdminController(
        admin_view,
        admin_service
    )

    # Main application
    app = CLIUniApp(
        cli_view,
        student_controller,
        admin_controller
    )

    app.start()


if __name__ == "__main__":
    main()
