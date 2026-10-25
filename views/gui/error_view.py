
from tkinter import messagebox


class ErrorView:
    def __init__(self, parent):
        self.parent = parent

    def show_error(self, message):
        messagebox.showerror(
            "Error",
            message,
            parent=self.parent
        )

    def show_success(self, message):
        messagebox.showinfo(
            "Success",
            message,
            parent=self.parent
        )
