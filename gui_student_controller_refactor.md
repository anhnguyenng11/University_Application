# Separate GUIUniApp and GUIStudentController

This guide follows the separation already used by the CLI. It contains proposed code for you to read and apply yourself. No Python files are changed by this guide.

## The CLI pattern

`CLIUniApp` owns the main menu. When the user selects Student, it calls `StudentController.start()`. The student controller then owns the student menu, registration, login, and student session. It calls `StudentService` for the actual work.

The GUI can use the same division:

| Class | Owns |
| --- | --- |
| `GUIUniApp` | Welcome screen and the shared `show_view()` method that replaces one screen with another. |
| `GUIStudentController` | Student login and registration screens, student actions, login state, and student messages. |
| `LoginView` and `RegistrationView` | Fields and buttons only. |
| `StudentService` | Validation and saving/loading student records. |

The current `GUIUniApp` also contains `active_student`, `show_student_login()`, `show_registration()`, `login_success()`, and `registration_success()`. Move those student responsibilities to `GUIStudentController`. Keep `show_view()` in `GUIUniApp` because every GUI section will need the same screen switcher. Pass it to the student controller as a callback.

## 1. Proposed `controllers/gui/gui_uni_app.py`

Replace that file with this code when you are ready:

```python
from controllers.gui.gui_student_controller import GUIStudentController
from views.gui.welcome_view import WelcomeView


class GUIUniApp:
    def __init__(self, root, student_service):
        self.root = root
        self.current_view = None

        self.student_controller = GUIStudentController(
            root,
            student_service,
            show_view=self.show_view,
            on_back=self.show_welcome
        )

        self.show_welcome()

    def show_view(self, view):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view
        self.current_view.pack(fill="both", expand=True)

    def show_welcome(self):
        view = WelcomeView(
            self.root,
            on_student=self.student_controller.start
        )
        self.show_view(view)
```

`GUIUniApp` now does the same kind of work as `CLIUniApp`: it shows the starting screen and hands the Student choice to the student controller. Unlike a CLI menu, Tkinter uses button callbacks, so `show_view` and `show_welcome` are passed as callbacks.

## 2. Proposed `controllers/gui/gui_student_controller.py`

Replace that file with this code when you are ready:

```python
from views.gui.error_view import ErrorView
from views.gui.gui_student.login_view import LoginView
from views.gui.gui_student.registration_view import RegistrationView


class GUIStudentController:
    def __init__(self, root, student_service, show_view, on_back):
        self.root = root
        self.student_service = student_service
        self.show_view = show_view
        self.on_back = on_back
        self.error_view = ErrorView(root)
        self.active_student = None

    def start(self):
        self.show_login()

    def show_login(self):
        view = LoginView(
            self.root,
            on_login=self.login,
            on_register=self.show_registration,
            on_back=self.on_back
        )
        self.show_view(view)

    def show_registration(self):
        view = RegistrationView(
            self.root,
            on_register=self.register,
            on_back=self.show_login
        )
        self.show_view(view)

    def login(self, email, password):
        if not email or not password:
            self.error_view.show_error("Email and password are required.")
            return

        try:
            student = self.student_service.login(email, password)
        except (ValueError, OSError) as error:
            self.error_view.show_error(str(error))
            return

        if student is None:
            self.error_view.show_error("Invalid email or password.")
            return

        self.active_student = student
        self.error_view.show_success("Login successful!")

    def register(self, name, email, password):
        try:
            student = self.student_service.register(name, email, password)
        except (ValueError, OSError) as error:
            self.error_view.show_error(str(error))
            return

        self.show_login()
        self.error_view.show_success(
            f"Registration successful. Your student ID is {student.student_id}."
        )
```

`active_student` belongs here because the future student dashboard, subjects, password change, and logout will all be part of the student flow. `StudentService` still does validation and file access; the controller should not copy that logic.

## Files affected

Only the two controller files above need changes for this refactor. `gui_main.py`, the existing views, and `StudentService` can stay as they are. There is one `GUIStudentController(...)` call in the project, inside `GUIUniApp`, and the proposed code updates it.

## Check the behavior after applying it

Run `python3 gui_main.py` and check this path:

1. Welcome → Student opens Login; Back returns to Welcome.
2. Login → Register opens Registration; Back returns to Login.
3. Valid registration returns to Login and shows the student ID.
4. Duplicate email and incorrect password show errors.
5. Valid login shows a success message. It still stays on Login until a student dashboard is built.

This refactor changes ownership of the GUI flow. It should not change saved student data or the screens the user sees.
