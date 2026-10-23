"""
Command Line Interface (CLIUniApp) Main Launcher. 

This module is the entry point for the interactive terminal application. 
It runs the main CLI loop, presenting the top-level navigation menus for the Admin Subsystem, Student Subsystem, and System Exit.

"""

from models.database import Database
from utils.constants import DATABASE_NAME

def main_system():
    """
    Main function to launch the CLI UniApp.
    It presents the main menu at the start of the application.
    """
    while True:
        choice = input("University System: (A)dmin, (S)tudent, exit (X): ")
        if choice == 'A' or choice == 'a':
            admin_subsystem()
        elif choice == 'S' or choice == 's':
            student_subsystem()
        elif choice == 'X' or choice == 'x':
            print("Thank You for using the University System. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

def admin_subsystem():
    # TODO: Implement the admin subsystem functionality. Probably much later.
    print("Admin Subsystem is under construction.")

def student_subsystem():
    # TODO: Implement the Student Subsystem functionality. Try completing this first.
    print("Student Subsystem is under construction.")

if __name__ == "__main__":
    student_db = Database().read_students(DATABASE_NAME)
    main_system()
