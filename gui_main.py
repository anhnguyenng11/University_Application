import tkinter as tk
from tkinter import ttk
from controllers.gui.gui_uni_app import GUIUniApp
from models import StudentService, StudentDataFile, AdminService, AdminDataFile
from utils import constants
from views.gui.global_theme import apply_global_theme

def main():
    root = tk.Tk()
    root.title("UniApp")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - constants.WINDOW_WIDTH) // 2
    y = (screen_height - constants.WINDOW_HEIGHT) // 2

    root.geometry(f"{constants.WINDOW_WIDTH}x{constants.WINDOW_HEIGHT}+{x}+{y}")
    root.resizable(True, True)
    root.minsize(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)  # Prevents compression into illegibility
    
    student_data_file = StudentDataFile()
    student_service = StudentService(student_data_file)

    admin_data_file = AdminDataFile()
    admin_service = AdminService(admin_data_file, student_data_file)

    apply_global_theme(root)
    app = GUIUniApp(root, student_service, admin_service)

    root.mainloop()


if __name__ == "__main__":
    main()
