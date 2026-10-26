from tkinter import ttk

class StudentMainView(ttk.Frame):
    def __init__(
            self, 
            parent, 
            on_dashboard, 
            on_subjects, 
            on_account, 
            on_logout
        ):

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
            text="Student Portal"
        ).pack(side="right")

        ttk.Separator(
            self,
            orient="horizontal"
        ).pack(side="top", fill="x")

        # Main body
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(body, width=275, padding=10)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        for text, callback in (
            ("Dashboard", on_dashboard),
            ("Subjects", on_subjects),
            ("Account", on_account)
        ):
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

