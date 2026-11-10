from tkinter import Toplevel, ttk

class ErrorView:
    def __init__(self, parent):
        self.parent = parent

    def show_error(self, message):
        self._show_message("Error", message, "\u2715", "Error.TLabel")

    def show_success(self, message):
        self._show_message("Success", message, "\u2713", "Success.TLabel")

    def _show_message(self, title, message, symbol, style_name):
        # Instantiate the secondary popup window
        popup = Toplevel(self.parent)
        popup.withdraw() 
        popup.title(f"UniApp - {title}")
        
        # Instructs the OS window manager to strip standard window decorations (like minimize/maximize buttons) from the popup and binds its z-index so it can never be pushed behind the parent window.
        popup.transient(self.parent)
        popup.resizable(False, False)

        content = ttk.Frame(popup, style="App.TFrame", padding=30)
        content.grid(row=0, column=0, sticky="NSEW")
        
        content.columnconfigure(0, weight=1)

        ttk.Label(
            content, 
            text=symbol, 
            style=style_name,
            font=("", 45, "bold"),
            anchor="center"
        ).grid(row=0, column=0, pady=(0, 15))

        ttk.Label(
            content, 
            text=message, 
            style="Body.TLabel", 
            wraplength=320, 
            justify="center",
            anchor="center"
        ).grid(row=1, column=0, pady=(0, 25))

        ttk.Button(
            content, 
            text="OK", 
            command=popup.destroy, 
            style="Primary.TButton"
        ).grid(row=2, column=0, sticky="WE", ipady=2)

        popup.update_idletasks()
        
        # Orthogonal centering mathematics relative to the parent application's coordinates
        x = max(0, self.parent.winfo_rootx() + (self.parent.winfo_width() - popup.winfo_reqwidth()) // 2)
        y = max(0, self.parent.winfo_rooty() + (self.parent.winfo_height() - popup.winfo_reqheight()) // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Execution block: render, capture focus, and halt background interactions
        popup.deiconify()
        popup.wait_visibility()
        popup.grab_set()
        popup.wait_window()