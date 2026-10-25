
from tkinter import ttk
from views.gui.base_gui_view import BaseGUIView


class WelcomeView(BaseGUIView):
    def __init__(self, parent, on_student):
        super().__init__(parent)

        style = ttk.Style()
        style.configure(
            "Welcome.TButton",
            font=("", 18)
        )

        content = ttk.Frame(self)
        content.pack(expand=True)

        # Title
        ttk.Label(
            content,
            text="Welcome to UniApp",
            font=("", 40, "bold")
        ).pack()

        ttk.Frame(content, height=15).pack()

        ttk.Label(
            content,
            text="dedicated to handsome students",
            font=("", 12, "italic")
        ).pack()

        # Space between title and buttons
        ttk.Frame(content, height=100).pack()

        # Button container
        button_frame = ttk.Frame(
            content,
            width=450,
            height=165
        )
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Student",
            command=on_student,
            style="Welcome.TButton"
        ).place(x=0, y=0, width=450, height=65)

        ttk.Button(
            button_frame,
            text="Admin",
            state="disabled",
            style="Welcome.TButton"
        ).place(x=0, y=85, width=450, height=65)
