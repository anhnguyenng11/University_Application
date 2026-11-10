from tkinter import ttk

class AccountView(ttk.Frame):
    def __init__(self, parent, information_title, information_rows, on_change_password):
        super().__init__(parent, style="App.TFrame")

        self.on_change_password = on_change_password
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Account",
            style="Title.TLabel"
        ).grid(row=0, column=0, sticky="W", pady=(0, 20))

        # Account information
        ttk.Label(
            self,
            text=information_title,
            style="Heading.TLabel"
        ).grid(row=1, column=0, sticky="W", pady=(0, 10))

        info_card = ttk.Frame(self, style="Card.TFrame", padding=20)
        info_card.grid(row=2, column=0, sticky="WE", pady=(0, 25))
        info_card.columnconfigure(1, weight=1) 

        # Splitting the label and value into separate grid columns for tabular alignment
        for index, (label, value) in enumerate(information_rows):
            ttk.Label(
                info_card, text=f"{label}:", style="Muted.TLabel"
            ).grid(row=index, column=0, sticky="W", pady=8, padx=(0, 15))
            
            ttk.Label(
                info_card, text=value, style="Form.TLabel"
            ).grid(row=index, column=1, sticky="W", pady=8)

        # Change password
        ttk.Label(
            self,
            text="Change Password",
            style="Heading.TLabel"
        ).grid(row=3, column=0, sticky="W", pady=(0, 10))

        password_card = ttk.Frame(self, style="Card.TFrame", padding=20)
        password_card.grid(row=4, column=0, sticky="WE")
        password_card.columnconfigure(0, weight=1)

        entries = []
        current_row = 0
        
        # Grid iterations to map labels above their respective entry fields
        for label, bottom_padding in (
            ("Current Password", 15),
            ("New Password", 15),
            ("Confirm New Password", 25)
        ):
            ttk.Label(
                password_card,
                text=label,
                style="Form.TLabel"
            ).grid(row=current_row, column=0, sticky="W", pady=(0, 5))
            
            entry = ttk.Entry(password_card, show="*", style="Padded.TEntry")
            entry.grid(row=current_row + 1, column=0, sticky="WE", pady=(0, bottom_padding))
            entries.append(entry)
            
            current_row += 2

        self.current_password, self.new_password, self.confirm_password = entries

        ttk.Button(
            password_card,
            text="Update Password",
            style="Primary.TButton",
            command=self.submit_password
        ).grid(row=current_row, column=0, sticky="WE")

    def submit_password(self):
        current_password = self.current_password.get()
        new_password = self.new_password.get()
        confirm_password = self.confirm_password.get()

        self.on_change_password(
            current_password,
            new_password,
            confirm_password
        )