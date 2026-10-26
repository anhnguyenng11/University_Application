from tkinter import ttk

class AccountView(ttk.Frame):
    def __init__(self, parent, admin, on_change_password):
        super().__init__(parent)

        self.on_change_password = on_change_password

        style = ttk.Style()
        style.configure("Account.TLabelframe.Label", font=("", 12, "bold italic"))
        style.configure("Account.TButton", font=("", 12, ""))

        # Header
        ttk.Label(
            self,
            text="Account",
            font=("", 20, "bold")
        ).pack(anchor="w")

        # Admin information
        info_frame = ttk.LabelFrame(
            self,
            text="Admin Information",
            style="Account.TLabelframe",
            padding=10
        )
        info_frame.pack(fill="x", pady=20)

        for label, value in (
            ("Name", admin.name),
            ("Admin ID", admin.admin_id),
            ("Email", admin.email)
        ):
            ttk.Label(
                info_frame,
                text=f"{label}: {value}",
                font=("", 12)
            ).pack(anchor="w", pady=5)

        # Change password
        password_frame = ttk.LabelFrame(
            self,
            text="Change Password",
            style="Account.TLabelframe",
            padding=20
        )
        password_frame.pack(fill="x")

        entries = []
        for label, bottom_padding in (
            ("Current Password", 15),
            ("New Password", 15),
            ("Confirm New Password", 20)
        ):
            ttk.Label(
                password_frame,
                text=label,
                font=("", 12)
            ).pack(anchor="w", pady=(0, 3))
            entry = ttk.Entry(password_frame, show="*")
            entry.pack(fill="x", ipady=5, pady=(0, bottom_padding))
            entries.append(entry)

        self.current_password, self.new_password, self.confirm_password = entries

        ttk.Button(
            password_frame,
            text="Update Password",
            style="Account.TButton",
            command=self.submit_password
        ).pack(fill="x", ipady=10)

    def submit_password(self):
        current_password = self.current_password.get()
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        self.on_change_password(
            current_password,
            new_password,
            confirm_password
        )
