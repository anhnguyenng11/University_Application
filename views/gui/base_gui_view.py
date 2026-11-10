from tkinter import ttk


class BaseGUIView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="App.TFrame")
