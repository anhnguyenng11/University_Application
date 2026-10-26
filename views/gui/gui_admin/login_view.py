
from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView


class LoginView(BaseGUIView):
    def __init__(self, parent, on_login, on_back):
        super().__init__(parent)

        style = ttk.Style()
        style.configure("Login.TButton", font=("", 18))
        style.configure("Login.TLabel", font=("", 18))
        style.configure("Padded.TEntry", padding=(8, 8, 8, 8))

        content = ttk.Frame(self)
        content.pack(expand=True)

        # Title
        ttk.Label(
            content,
            text="Admin Login",
            font=("", 30, "bold")
        ).pack()

        ttk.Frame(content, height=50).pack()

        # Input Frame
        input_frame = ttk.Frame(content)
        input_frame.pack(fill="x")

        email_entry = self.create_auth_entry(
            input_frame, "Email", "Login.TLabel"
        )

        ttk.Frame(input_frame, height=25).pack()

        password_entry = self.create_auth_entry(
            input_frame, "Password", "Login.TLabel", show="*"
        )

        ttk.Frame(content, height=40).pack()

        # Buttons
        button_frame = ttk.Frame(content, width=450, height=235)
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Login",
            command=lambda: on_login(
                email_entry.get(),
                password_entry.get()
            ),
            style="Login.TButton"
        ).place(x=0, y=0, width=450, height=65)

        # ttk.Button(
        #     button_frame,
        #     text="Register",
        #     command=on_register,
        #     style="Login.TButton"
        # ).place(x=0, y=85, width=450, height=65)

        ttk.Button(
            button_frame,
            text="Back",
            command=on_back,
            style="Login.TButton"
        ).place(x=0, y=85, width=450, height=65)
