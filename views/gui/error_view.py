from tkinter import Toplevel, ttk
from views.gui.base_gui_view import BUTTON_CURSOR, COLORS, setup_styles


class ErrorView:
    def __init__(self, parent):
        self.parent = parent

    def show_error(self, message):
        self._show_message("Error", message, "\u2715", COLORS["danger"])

    def show_success(self, message):
        self._show_message("Success", message, "\u2713", COLORS["success"])

    def _show_message(self, title, message, symbol, color):
        setup_styles()
        popup = Toplevel(self.parent)
        popup.withdraw()
        popup.title(title)
        popup.transient(self.parent)
        popup.resizable(False, False)
        popup.configure(background=COLORS["canvas"])

        content = ttk.Frame(popup, padding=24)
        content.pack(fill="both", expand=True)

        ttk.Label(
            content, text=symbol, foreground=color, font="UniApp.Title"
        ).pack(pady=(0, 12))
        ttk.Label(content, text=title, font="UniApp.Section").pack(pady=(0, 12))
        ttk.Label(
            content, text=message, wraplength=400, justify="center"
        ).pack()
        button = ttk.Button(content, text="OK", command=popup.destroy, cursor=BUTTON_CURSOR,
                            style="UniApp.Primary.TButton")
        button.pack(pady=(24, 0))

        popup.update_idletasks()
        x = max(0, self.parent.winfo_rootx() + (self.parent.winfo_width() - popup.winfo_reqwidth()) // 2)
        y = max(0, self.parent.winfo_rooty() + (self.parent.winfo_height() - popup.winfo_reqheight()) // 2)
        popup.geometry(f"+{x}+{y}")
        popup.deiconify()
        popup.wait_visibility()
        popup.grab_set()
        popup.wait_window()
