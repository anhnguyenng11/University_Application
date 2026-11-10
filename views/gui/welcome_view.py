
from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView


class WelcomeView(BaseGUIView):
    def __init__(self, parent, on_student, on_admin):
        super().__init__(parent)

        card = ttk.Frame(self, padding=45, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center")

        card.columnconfigure(0, weight=1)

        ttk.Label(
            card,
            text="Welcome to UniApp",
            style="Title.TLabel"
        ).grid(row=0, column=0)

        ttk.Label(
            card,
            text="Manage university applications with ease.",
            style="Subtitle.TLabel"
        ).grid(row=1, column=0, pady=(8, 30))

        # Space between title and buttons
        ttk.Frame(card, height=100).grid(row=2, column=0)

        ttk.Button(
            card,
            text="Continue as Student",
            style="Primary.TButton",
            command=on_student
        ).grid(row=3, column=0, sticky="WE", pady=6)

        ttk.Button(
            card,
            text="Continue as Admin",
            style="Secondary.TButton",
            command=on_admin
        ).grid(row=4, column=0, sticky="WE", pady=6)
