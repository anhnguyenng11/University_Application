import tkinter as tk
from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView


class LoginView(BaseGUIView):
    def __init__(self, parent, title, on_login, on_back, on_register=None):
        super().__init__(parent)

        content = ttk.Frame(self, padding=40, style="Card.TFrame")
        content.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            content,
            text=title,
            style="Heading.TLabel"
        ).pack(pady=(0, 30))

        email_entry = self.create_auth_entry(
            content, "Email", "Form.TLabel"
        )

        ttk.Frame(content, height=18, style="Card.TFrame").pack()

        password_entry = self.create_auth_entry(
            content, "Password", "Form.TLabel", show="*"
        )

        password_visible = tk.BooleanVar(value=False)

        def toggle_password():
            password_entry.configure(
                show="" if password_visible.get() else "*"
            )

        ttk.Checkbutton(
            content,
            text="Show password",
            variable=password_visible,
            command=toggle_password
        ).pack(anchor="w", pady=(8, 0))

        def submit_login():
            on_login(email_entry.get(), password_entry.get())

        button_frame = ttk.Frame(
            content,
            style="CardContent.TFrame"
        )

        ttk.Button(
            button_frame,
            text="Login",
            command=submit_login,
            style="Primary.TButton"
        ).pack(fill="x", pady=(0, 8))

        if on_register is not None:
            ttk.Button(
                button_frame,
                text="Register",
                command=on_register,
                style="Secondary.TButton"
            ).pack(fill="x", pady=(0, 8))

        ttk.Button(
            button_frame,
            text="Back",
            command=on_back,
            style="Secondary.TButton"
        ).pack(fill="x")

        content.bind("<Return>", lambda event: submit_login())
        email_entry.focus_set()
