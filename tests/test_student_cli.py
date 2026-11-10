import unittest
from unittest.mock import Mock, patch

from controllers.cli.student_controller import StudentController
from models.student_service import StudentService
from views.cli.student_view import StudentView


class TestStudentLogin(unittest.TestCase):
    def test_login_only_starts_session_on_success(self):
        view = Mock(spec=StudentView)
        view.get_login_details.return_value = (
            "student@university.com", "Password123"
        )
        service = Mock(spec=StudentService)
        controller = StudentController(view, service)

        with patch.object(controller, "start_student_session") as start_session:
            for message in ("Student email not found.", "Wrong password."):
                with self.subTest(message=message):
                    service.login.side_effect = ValueError(message)
                    controller.login_student()
                    view.show_message.assert_called_with(message)
                    start_session.assert_not_called()

            service.login.side_effect = None
            controller.login_student()
            service.login.assert_called_with(
                "student@university.com", "Password123"
            )
            start_session.assert_called_once_with(service.login.return_value)
