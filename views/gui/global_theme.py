import tkinter as tk
from tkinter import ttk
from utils import constants

def apply_global_theme(root: tk.Tk) -> None:
    """
    Applies a consistent theme and styles to the entire GUI application.
    """
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(background=constants.COLORS["background"])

    style.configure(
        "App.TFrame",
        background=constants.COLORS["background"]
    )

    style.configure(
        "Card.TFrame",
        background=constants.COLORS["background"],
        relief="solid",
        borderwidth=1
    )

    style.configure(
        "CardContent.TFrame",
        background=constants.COLORS["background"]
    )

    style.configure(
        "Title.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["title"]
    )

    style.configure(
        "Heading.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["heading"]
    )

    style.configure(
        "Body.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["text"],
        font=constants.FONTS["body"]
    )

    style.configure(
        "Muted.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["muted_text"],
        font=constants.FONTS["small"]
    )

    style.configure(
        "Form.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["text"],
        font=constants.FONTS["body_bold"]
    )

    style.configure(
        "Primary.TButton",
        background=constants.COLORS["primary"],
        foreground="#FFFFFF",
        font=constants.FONTS["button"],
        padding=(18, 11),
        borderwidth=0
    )

    style.map(
        "Primary.TButton",
        background=[
            ("disabled", constants.COLORS["disabled"]),
            ("pressed", constants.COLORS["primary_pressed"]),
            ("active", constants.COLORS["primary_hover"])
        ],
        foreground=[
            ("disabled", "#FFFFFF")
        ]
    )

    style.configure(
        "Secondary.TButton",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["button"],
        padding=(18, 11),
        borderwidth=1,
        relief="solid"
    )

    style.map(
        "Secondary.TButton",
        background=[
            ("active", "#EAF2FD"),
            ("pressed", "#D6E7FA")
        ]
    )

    style.configure(
        "Sidebar.TFrame",
        background=constants.COLORS["navy"]
    )

    style.configure(
        "Sidebar.TLabel",
        background=constants.COLORS["navy"],
        foreground="#FFFFFF",
        font=constants.FONTS["heading"]
    )

    style.configure(
        "Sidebar.TButton",
        background=constants.COLORS["navy"],
        foreground="#FFFFFF",
        anchor="w",
        font=constants.FONTS["body"],
        padding=(15, 11),
        borderwidth=0
    )

    style.map(
        "Sidebar.TButton",
        background=[
            ("active", constants.COLORS["primary"]),
            ("pressed", constants.COLORS["primary_pressed"])
        ]
    )

    style.configure(
        "Logout.TButton",
        background=constants.COLORS["navy"],
        foreground="#FFB4AB",
        anchor="w",
        font=constants.FONTS["body"],
        padding=(15, 11),
        borderwidth=0
    )

    style.map(
        "Logout.TButton",
        background=[
            ("active", "#7A263A"),
            ("pressed", "#5C1D2D")
        ],
        foreground=[
            ("active", "#FFFFFF")
        ]
    )

    style.configure(
        "Padded.TEntry",
        padding=(10, 8),
        fieldbackground=constants.COLORS["background"],
        foreground=constants.COLORS["text"]
    )

    style.configure(
        "Status.TLabel",
        background=constants.COLORS["navy"],
        foreground="#FFFFFF",
        padding=(10, 6),
        font=constants.FONTS["small"]
    )

    style.configure(
        "Success.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["success"],
        font=constants.FONTS["body_bold"]
    )

    style.configure(
        "Error.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["error"],
        font=constants.FONTS["body_bold"]
    )

    style.configure(
        "Form.TCheckbutton",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["small"]
    )
    
    style.configure(
        "Subtitle.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["small"]
    )
    

