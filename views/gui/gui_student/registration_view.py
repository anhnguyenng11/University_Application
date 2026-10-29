from tkinter import ttk

from views.gui.base_gui_view import BaseGUIView


class RegistrationView(BaseGUIView):
    def __init__(self, parent, on_register, on_back):
        super().__init__(parent)

        content = ttk.Frame(self, padding=32)
        content.pack(expand=True)
        content.columnconfigure(0, minsize=450)

        ttk.Label(
            content,
            text="Student Registration",
            style="UniApp.Title.TLabel"
        ).grid(row=0, column=0, pady=(0, 32))

        input_frame = ttk.Frame(content)
        input_frame.grid(row=1, column=0, sticky="ew")

        name_entry = self.create_auth_entry(
            input_frame, "Name", "UniApp.Caption.TLabel"
        )

        email_entry = self.create_auth_entry(
            input_frame, "Email", "UniApp.Caption.TLabel"
        )

        password_entry = self.create_auth_entry(
            input_frame, "Password", "UniApp.Caption.TLabel", show="*"
        )

        ttk.Button(
            content,
            text="Register",
            command=lambda: on_register(
                name_entry.get(),
                email_entry.get(),
                password_entry.get()
            ),
            style="UniApp.Primary.TButton"
        ).grid(row=2, column=0, sticky="ew")

        ttk.Button(
            content,
            text="Back",
            command=on_back,
            style="UniApp.Utility.TButton"
        ).grid(row=3, column=0, sticky="ew", pady=(12, 0))
