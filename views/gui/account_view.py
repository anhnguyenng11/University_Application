from tkinter import ttk
from views.gui.base_gui_view import setup_styles


class AccountView(ttk.Frame):
    def __init__(self, parent, information_title, information_rows, on_change_password):
        super().__init__(parent, style="UniApp.Page.TFrame")
        setup_styles()

        self.on_change_password = on_change_password

        # Header
        ttk.Label(
            self,
            text="Account",
            style="UniApp.PageTitle.TLabel"
        ).pack(anchor="w", pady=(0, 24))

        # Account information
        info_frame = ttk.LabelFrame(
            self,
            text=information_title,
            style="UniApp.Card.TLabelframe",
            padding=(24, 12)
        )
        info_frame.pack(fill="x", pady=(0, 16))

        for label, value in information_rows:
            ttk.Label(
                info_frame,
                text=f"{label}: {value}",
                style="UniApp.PageText.TLabel",
                wraplength=640,
                justify="left"
            ).pack(anchor="w", pady=2)

        # Change password
        password_frame = ttk.LabelFrame(
            self,
            text="Change Password",
            style="UniApp.Card.TLabelframe",
            padding=(24, 16)
        )
        password_frame.pack(fill="x")

        form = ttk.Frame(password_frame, style="UniApp.Page.TFrame")
        form.pack(anchor="w")
        form.columnconfigure(0, minsize=450)

        entries = []
        for index, label in enumerate((
            "Current Password", "New Password", "Confirm New Password"
        )):
            ttk.Label(
                form,
                text=label,
                style="UniApp.PageCaption.TLabel"
            ).grid(row=index * 2, column=0, sticky="w", pady=(0, 4))
            entry = ttk.Entry(form, show="*", font="UniApp.Body", style="UniApp.TEntry")
            entry.grid(row=index * 2 + 1, column=0, sticky="ew", pady=(0, 12))
            entries.append(entry)

        self.current_password, self.new_password, self.confirm_password = entries

        ttk.Button(
            form,
            text="Update Password",
            style="UniApp.Primary.TButton",
            command=self.submit_password
        ).grid(row=6, column=0, sticky="ew")

    def submit_password(self):
        current_password = self.current_password.get()
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        self.on_change_password(
            current_password,
            new_password,
            confirm_password
        )
