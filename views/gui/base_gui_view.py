from tkinter import ttk


class BaseGUIView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="App.TFrame")

    def create_auth_entry(self, parent, text, label_style, show=""):
        ttk.Label(
            parent,
            text=text,
            style=label_style
        ).pack(anchor="w", pady=3)

        entry = ttk.Entry(
            parent,
            font=("", 15),
            style="Padded.TEntry",
            show=show
        )
        entry.pack(fill="x")
        return entry
