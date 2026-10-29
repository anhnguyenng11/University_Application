"""
    A view for the student registration page.
"""

from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView

class RegistrationView(BaseGUIView):
    """A view for the student registration page."""
    def __init__(self, parent, title, on_register, on_back):
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
        
        # Name field
        ttk.Label(
            content, 
            text="Name", 
            style="Form.TLabel"
        ).grid(row=1, column=0, sticky="W")

        name_entry = ttk.Entry(content, style="Padded.TEntry", width=40)
        name_entry.grid(row=2, column=0, sticky="WE", pady=(5, 25))

        # Email field
        ttk.Label(
            content, 
            text="Email", 
            style="Form.TLabel"
        ).grid(row=3, column=0, sticky="W")

        email_entry = ttk.Entry(content, style="Padded.TEntry", width=40)
        email_entry.grid(row=4, column=0, sticky="WE", pady=(5, 20))

        # Password field
        ttk.Label(
            content, 
            text="Password", 
            style="Form.TLabel"
        ).grid(row=5, column=0, sticky="W")

        password_entry = ttk.Entry(content, style="Padded.TEntry", show="*", width=40)
        password_entry.grid(row=6, column=0, sticky="WE", pady=(5, 40))

        # Buttons frame to hold Register and Back buttons
        button_frame = ttk.Frame(content)
        button_frame.grid(row=7, column=0, sticky="WE")
        button_frame.columnconfigure(0, weight=1)

        ttk.Button(
            button_frame,
            text="Register",
            command=lambda: on_register(
                name_entry.get(),
                email_entry.get(),
                password_entry.get()
            ),
            style="Primary.TButton" 
        ).grid(row=0, column=0, sticky="WE", pady=(0, 15))

        ttk.Button(
            button_frame,
            text="Back",
            command=on_back,
            style="Secondary.TButton"
        ).grid(row=1, column=0, sticky="WE")
