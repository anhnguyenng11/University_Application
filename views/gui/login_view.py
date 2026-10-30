
from tkinter import ttk
from views.gui.base_gui_view import BUTTON_CURSOR, BaseGUIView


class LoginView(BaseGUIView):
    def __init__(self, parent, title, on_login, on_back, on_register=None):
        super().__init__(parent)

        content = ttk.Frame(self, padding=32)
        content.pack(expand=True)
        content.columnconfigure(0, minsize=450)

        # Title
        ttk.Label(
            content,
            text=title,
            style="UniApp.Title.TLabel"
        ).grid(row=0, column=0, pady=(0, 32))

        # Input Frame
        input_frame = ttk.Frame(content)
        input_frame.grid(row=1, column=0, sticky="ew")

        email_entry = self.create_auth_entry(
            input_frame, "Email", "UniApp.Caption.TLabel"
        )

        password_entry = self.create_auth_entry(
            input_frame, "Password", "UniApp.Caption.TLabel", show="*"
        )

        ttk.Button(
            content,
            text="Login",
            cursor=BUTTON_CURSOR,
            command=lambda: on_login(
                email_entry.get(),
                password_entry.get()
            ),
            style="UniApp.Primary.TButton"
        ).grid(row=2, column=0, sticky="ew")

        button_frame = ttk.Frame(content)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        if on_register is not None:
            ttk.Button(
                button_frame,
                text="Register",
                cursor=BUTTON_CURSOR,
                command=on_register,
                style="UniApp.Secondary.TButton"
            ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ttk.Button(
            button_frame,
            text="Back",
            cursor=BUTTON_CURSOR,
            command=on_back,
            style="UniApp.Utility.TButton"
        ).grid(row=0, column=1 if on_register is not None else 0,
               columnspan=1 if on_register is not None else 2, sticky="ew",
               padx=(6, 0) if on_register is not None else 0)
