from tkinter import ttk

from views.gui.base_gui_view import BaseGUIView


class RegistrationView(BaseGUIView):
    def __init__(self, parent, on_register, on_back):
        super().__init__(parent)

        style = ttk.Style()
        style.configure("Registration.TButton", font=("", 18))
        style.configure("Registration.TLabel", font=("", 18))
        style.configure("Padded.TEntry", padding=(8, 8, 8, 8))

        content = ttk.Frame(self)
        content.pack(expand=True)

        ttk.Label(
            content,
            text="Student Registration",
            font=("", 30, "bold")
        ).pack()

        ttk.Frame(content, height=30).pack()

        input_frame = ttk.Frame(content)
        input_frame.pack(fill="x")

        name_entry = self.create_auth_entry(
            input_frame, "Name", "Registration.TLabel"
        )

        ttk.Frame(input_frame, height=25).pack()

        email_entry = self.create_auth_entry(
            input_frame, "Email", "Registration.TLabel"
        )

        ttk.Frame(input_frame, height=20).pack()

        password_entry = self.create_auth_entry(
            input_frame, "Password", "Registration.TLabel", show="*"
        )

        ttk.Frame(content, height=40).pack()

        button_frame = ttk.Frame(content, width=450, height=150)
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Register",
            command=lambda: on_register(
                name_entry.get(),
                email_entry.get(),
                password_entry.get()
            ),
            style="Registration.TButton"
        ).place(x=0, y=0, width=450, height=65)

        ttk.Button(
            button_frame,
            text="Back",
            command=on_back,
            style="Registration.TButton"
        ).place(x=0, y=85, width=450, height=65)
