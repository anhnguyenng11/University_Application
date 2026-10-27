from tkinter import ttk

class MainView(ttk.Frame):
    def __init__(self, parent, title, navigation, on_logout):
        super().__init__(parent)

        self.current_content = None

        style = ttk.Style()

        style.configure("Sidebar.TButton", font=("", 15, ""), anchor="w")

        # Header
        header = ttk.Frame(self, padding=20)
        header.pack(fill="x")

        ttk.Label(
            header, 
            text="UniApp",
            font=("", 25, "bold")
        ).pack(side="left")
        
        ttk.Label(
            header, 
            text=title
        ).pack(side="right")

        ttk.Separator(
            self,
            orient="horizontal"
        ).pack(side="top", fill="x")

        # Main body
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(body, width=250, padding=10)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        for text, callback in navigation:
            ttk.Button(
                sidebar,
                text=text,
                style="Sidebar.TButton",
                command=callback
            ).pack(fill="x", pady=10, ipady=10)
        
        ttk.Button(
            sidebar, 
            text="Logout", 
            style="Sidebar.TButton",
            command=on_logout
        ).pack(side="bottom", fill="x", pady=10, ipady=10)

        ttk.Separator(
            body,
            orient="vertical"
        ).pack(side="left", fill="y")

        # Content area
        self.content_frame = ttk.Frame(body, padding=20)
        self.content_frame.pack(side="left", fill="both", expand=True)

    def show_content(self, view):
        if self.current_content:
            self.current_content.destroy()

        self.current_content = view
        view.pack(fill="both", expand=True)

