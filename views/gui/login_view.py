import tkinter as tk
from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView


class LoginView(BaseGUIView):
    def __init__(self, parent, title, on_login, on_back, on_register=None):
        super().__init__(parent)
        
        self.winfo_toplevel().title(f"UniApp - {title}")
        content = ttk.Frame(self, padding=40, style="Card.TFrame")
        content.place(relx=0.5, rely=0.5, anchor="center") 
        content.columnconfigure(0, weight=1)

        ttk.Label(
            content,
            text=title,
            style="Title.TLabel"
        ).grid(row=0, column=0, pady=(0, 30))

        # Email field
        ttk.Label(
            content, 
            text="Email", 
            style="Form.TLabel"
        ).grid(row=1, column=0, sticky="W")
        
        email_entry = ttk.Entry(content, style="Padded.TEntry", width=35)
        email_entry.grid(row=2, column=0, sticky="WE", pady=(5, 15))

        # Password field
        ttk.Label(
            content, 
            text="Password", 
            style="Form.TLabel"
        ).grid(row=3, column=0, sticky="W")
        
        password_entry = ttk.Entry(content, style="Padded.TEntry", show="*", width=35)
        password_entry.grid(row=4, column=0, sticky="WE", pady=(5, 5))
        password_visible = tk.BooleanVar(value=False)

        # Nifty way to hide/show password using a checkbox
        def toggle_password():
            password_entry.configure(
                show="" if password_visible.get() else "*"
            )

        ttk.Checkbutton(
            content,
            text="Show password",
            style="Form.TCheckbutton",
            variable=password_visible,
            command=toggle_password
        ).grid(row=5, column=0, sticky="W", pady=(0, 20))

        def submit_login(event=None):
            on_login(email_entry.get(), password_entry.get())

        button_frame = ttk.Frame(content, style="CardContent.TFrame")
        button_frame.grid(row=6, column=0, sticky="WE")
        button_frame.columnconfigure(0, weight=1)

        ttk.Button(
            button_frame,
            text="Login",
            command=submit_login,
            style="Primary.TButton"
        ).grid(row=0, column=0, sticky="WE", pady=(0, 8))

        current_row = 1
        if on_register is not None:
            ttk.Button(
                button_frame,
                text="No account? Register here",
                command=on_register,
                style="Secondary.TButton"
            ).grid(row=current_row, column=0, sticky="WE", pady=(0, 8))
            current_row += 1

        ttk.Button(
            button_frame,
            text="Back",
            command=on_back,
            style="Secondary.TButton"
        ).grid(row=current_row, column=0, sticky="WE")

        self.bind("<Return>", submit_login) 
        email_entry.focus_set()
