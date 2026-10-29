import tkinter as tk
from tkinter import ttk
from controllers.gui.gui_uni_app import GUIUniApp
from models import StudentService, StudentDataFile, AdminService, AdminDataFile
from utils import constants

def configure_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(background=constants.COLORS["background"])

    style.configure(
        "App.TFrame",
        background=constants.COLORS["background"]
    )

    style.configure(
        "Card.TFrame",
        background=constants.COLORS["surface"],
        relief="solid",
        borderwidth=1
    )

    style.configure(
        "CardContent.TFrame",
        background=constants.COLORS["surface"]
    )

    style.configure(
        "Title.TLabel",
        background=constants.COLORS["background"],
        foreground=constants.COLORS["navy"],
        font=constants.FONTS["title"]
    )

    style.configure(
        "Heading.TLabel",
        background=constants.COLORS["surface"],
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
        background=constants.COLORS["surface"],
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
        background=constants.COLORS["surface"],
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
        fieldbackground=constants.COLORS["surface"],
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
        background=constants.COLORS["surface"],
        foreground=constants.COLORS["success"],
        font=constants.FONTS["body_bold"]
    )

    style.configure(
        "Error.TLabel",
        background=constants.COLORS["surface"],
        foreground=constants.COLORS["error"],
        font=constants.FONTS["body_bold"]
    )


def main():
    root = tk.Tk()
    root.title("UniApp")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - constants.WINDOW_WIDTH) // 2
    y = (screen_height - constants.WINDOW_HEIGHT) // 2

    root.geometry(f"{constants.WINDOW_WIDTH}x{constants.WINDOW_HEIGHT}+{x}+{y}")
    root.resizable(False, False)
    
    student_data_file = StudentDataFile()
    student_service = StudentService(student_data_file)

    admin_data_file = AdminDataFile()
    admin_service = AdminService(admin_data_file, student_data_file)

    configure_theme(root)
    app = GUIUniApp(root, student_service, admin_service)

    root.mainloop()


if __name__ == "__main__":
    main()
