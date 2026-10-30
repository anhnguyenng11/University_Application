
from tkinter import ttk
from views.gui.base_gui_view import BUTTON_CURSOR, BaseGUIView


class WelcomeView(BaseGUIView):
    def __init__(self, parent, on_student, on_admin):
        super().__init__(parent)

        content = ttk.Frame(self, padding=32)
        content.pack(expand=True)
        content.columnconfigure(0, minsize=450)

        # Title
        ttk.Label(
            content,
            text="Welcome to UniApp",
            style="UniApp.Hero.TLabel"
        ).grid(row=0, column=0)

        ttk.Label(
            content,
            text="Just because you never give up\ndoesn't mean you will succeed.",
            style="UniApp.Muted.TLabel",
            justify="center",
            wraplength=450
        ).grid(row=1, column=0, pady=(24, 48))

        ttk.Button(
            content,
            text="Student",
            cursor=BUTTON_CURSOR,
            command=on_student,
            style="UniApp.Primary.TButton"
        ).grid(row=2, column=0, sticky="ew")

        ttk.Button(
            content,
            text="Admin",
            cursor=BUTTON_CURSOR,
            command=on_admin,
            style="UniApp.Primary.TButton"
        ).grid(row=3, column=0, sticky="ew", pady=(12, 0))
