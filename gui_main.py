
import tkinter as tk

from controllers.gui.gui_uni_app import GUIUniApp
from models.file_handlers.student_data_file import StudentDataFile
from models.student_service import StudentService

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700


def main():
    root = tk.Tk()
    root.title("UniApp")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    root.resizable(False, False)

    student_data_file = StudentDataFile()
    student_service = StudentService(student_data_file)
    app = GUIUniApp(root, student_service)

    root.mainloop()


if __name__ == "__main__":
    main()
