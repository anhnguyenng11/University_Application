
from views.cli_view import CLIView
from views.student_view import StudentView
from views.admin_view import AdminView

from controllers.cli_uni_app import CLIUniApp
from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController

from models.student_service import StudentService
from models.file_handlers.student_data_file import StudentDataFile

from models.admin_service import AdminService
from models.file_handlers.admin_data_file import AdminDataFile

def main() -> None:
    # Data handlers
    student_data_file = StudentDataFile()
    admin_data_file = AdminDataFile()

    # Services
    student_service = StudentService(student_data_file)
    admin_service = AdminService(admin_data_file, student_data_file)

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
