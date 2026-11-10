from tkinter import ttk

class MainView(ttk.Frame):
    def __init__(self, parent, title, navigation, on_logout):
        super().__init__(parent, style="App.TFrame")

        self.winfo_toplevel().title(f"UniApp - {title}")
        self.current_content = None

        header = ttk.Frame(
            self,
            padding=(20, 16),
            style="App.TFrame"
        )
        header.pack(fill="x")

        ttk.Label(
            header,
            text="UniApp",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Label(
            header,
            text=title,
            style="Body.TLabel"
        ).pack(side="right")

        ttk.Separator(
            self,
            orient="horizontal"
        ).pack(fill="x")

        body = ttk.Frame(self, style="App.TFrame")
        body.pack(fill="both", expand=True)

        sidebar = ttk.Frame(
            body,
            width=250,
            padding=15,
            style="Sidebar.TFrame"
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ttk.Label(
            sidebar,
            text=title,
            style="Sidebar.TLabel"
        ).pack(anchor="w", pady=(5, 25))

        for text, callback in navigation:
            ttk.Button(
                sidebar,
                text=text,
                style="Sidebar.TButton",
                command=callback
            ).pack(fill="x", pady=4, ipady=8)

        ttk.Button(
            sidebar,
            text="Logout",
            style="Logout.TButton",
            command=on_logout
        ).pack(side="bottom", fill="x", pady=4, ipady=8)

        ttk.Separator(
            body,
            orient="vertical"
        ).pack(side="left", fill="y")

        self.content_frame = ttk.Frame(
            body,
            padding=20,
            style="App.TFrame"
        )
        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

    def show_content(self, view):
        if self.current_content:
            self.current_content.destroy()

        self.current_content = view
        view.pack(fill="both", expand=True)

