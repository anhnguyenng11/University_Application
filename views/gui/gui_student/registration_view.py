from tkinter import ttk

from views.gui.base_gui_view import BaseGUIView


class RegistrationView(BaseGUIView):
    def __init__(self, parent, on_register, on_back):
        super().__init__(parent)

        content = ttk.Frame(self)
        content.pack(expand=True)

        ttk.Label(
            content, text="Student Registration", font=("", 30, "bold")
        ).pack(pady=20)

        ttk.Label(content, text="Name").pack(anchor="w")
        name_entry = ttk.Entry(content, width=40)
        name_entry.pack(pady=5)

        ttk.Label(content, text="Student email").pack(anchor="w")
        email_entry = ttk.Entry(content, width=40)
        email_entry.pack(pady=5)

        ttk.Label(content, text="Password").pack(anchor="w")
        password_entry = ttk.Entry(content, width=40, show="*")
        password_entry.pack(pady=5)

        ttk.Button(
            content,
            text="Register",
            command=lambda: on_register(
                name_entry.get(),
                email_entry.get(),
                password_entry.get()
            )
        ).pack(fill="x", pady=10)

        ttk.Button(content, text="Back", command=on_back).pack(fill="x")