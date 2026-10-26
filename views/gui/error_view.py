from tkinter import Toplevel, ttk


class ErrorView:
    def __init__(self, parent):
        self.parent = parent

    def show_error(self, message):
        self._show_message("Error", message, "\u2715", "red")

    def show_success(self, message):
        self._show_message("Success", message, "\u2713", "green")

    def _show_message(self, title, message, symbol, color):
        popup = Toplevel(self.parent)
        popup.withdraw()
        popup.title(title)
        popup.transient(self.parent)
        popup.resizable(False, False)

        ttk.Label(
            popup, text=symbol, foreground=color,
            font=("", 40, "bold")
        ).pack(padx=25, pady=(20, 10))
        ttk.Label(
            popup, text=message, wraplength=360, justify="center"
        ).pack(padx=25)
        button = ttk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=20)

        popup.update_idletasks()
        x = max(0, self.parent.winfo_rootx() + (self.parent.winfo_width() - popup.winfo_reqwidth()) // 2)
        y = max(0, self.parent.winfo_rooty() + (self.parent.winfo_height() - popup.winfo_reqheight()) // 2)
        popup.geometry(f"+{x}+{y}")
        popup.deiconify()
        popup.wait_visibility()
        popup.grab_set()
        button.focus_set()
        popup.wait_window()
