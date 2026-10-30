from tkinter import ttk
from views.gui.base_gui_view import BUTTON_CURSOR, setup_styles


class MainView(ttk.Frame):
    def __init__(self, parent, title, navigation, on_logout):
        super().__init__(parent)
        setup_styles()

        self.current_content = None

        # Header
        header = ttk.Frame(self, padding=(24, 12), style="UniApp.Header.TFrame")
        header.pack(fill="x")

        ttk.Label(
            header, 
            text="UniApp",
            style="UniApp.Brand.TLabel"
        ).pack(side="left")
        
        ttk.Label(
            header, 
            text=title,
            style="UniApp.Role.TLabel"
        ).pack(side="right")

        ttk.Separator(
            self,
            orient="horizontal"
        ).pack(side="top", fill="x")

        # Main body
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(body, width=216, padding=(12, 24),
                            style="UniApp.Page.TFrame")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        for text, callback in navigation:
            ttk.Button(
                sidebar,
                text=text,
                cursor=BUTTON_CURSOR,
                style="UniApp.Nav.TButton",
                command=callback
            ).pack(fill="x", pady=(0, 12))
        
        ttk.Button(
            sidebar, 
            text="Logout", 
            cursor=BUTTON_CURSOR,
            style="Sidebar.UniApp.Danger.TButton",
            command=on_logout
        ).pack(side="bottom", fill="x")

        ttk.Separator(
            body,
            orient="vertical"
        ).pack(side="left", fill="y")

        # Content area
        self.content_frame = ttk.Frame(body, padding=24, style="UniApp.Page.TFrame")
        self.content_frame.pack(side="left", fill="both", expand=True)

    def show_content(self, view):
        if self.current_content:
            self.current_content.destroy()

        self.current_content = view
        view.pack(fill="both", expand=True)

