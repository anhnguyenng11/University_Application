from tkinter import ttk


class BaseGUIView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
