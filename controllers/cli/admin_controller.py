"""
This module defines the AdminController class, which handles the admin operation flow in the university application.
"""
from views import AdminView
from models import Admin, AdminService

class AdminController:
    """
    The AdminController class manages the flow of operations for admin users in the university application.
    Methods:
    - start: Initiates the admin operation flow.
    - login_admin: Handles the login of an admin.
    - start_admin_session: Starts the admin session.
    - show_students: Displays the list of students in the system.
    - group_students: Groups students by their grades.
    - partition_students: Partitions students by their pass/fail status.
    - remove_student: Removes a student from the system.
    - clear_database: Clears the students database.
    """
    
    def __init__(self, view: AdminView, admin_service: AdminService) -> None:
        self.view = view
        self.admin_service = admin_service

    def start(self) -> None:
        """
        Starts the admin operation flow, prompting the admin to log in
        """
        self.login_admin()

    def login_admin(self) -> None:
        """
        Prompts the admin for login details and attempts to log in.
        """
        email, password = self.view.get_login_details("Admin")

        try:
            admin = self.admin_service.login(email, password)
        except ValueError as error:
            self.view.show_message(str(error))
            return

        self.start_admin_session(admin)

    def start_admin_session(self, admin: Admin) -> None:
        """
        Starts the admin session, displaying a welcome message and a loop for the admin menu.
        """
        self.view.show_welcome(admin.name, admin.admin_id, "Admin")
     
        while True:
            choice = self.view.show_admin_menu()

            try:
                if choice == "c":
                    self.clear_database()

                elif choice == "g":
                    self.group_students()

                elif choice == "p":
                    self.partition_students()

                elif choice == "r":
                    self.remove_student()

                elif choice == "s":
                    self.show_students()

                elif choice == "x":
                    # go back to university menu
                    return

                else:
                    self.view.show_message("Invalid option. Please try again.")
                    
            except (ValueError, OSError) as error:
                self.view.show_message(
                    "Admin operation failed: " + str(error)
                )

    def show_students(self) -> None:
        """
        Displays the list of students in the system.
        """
        students = self.admin_service.get_all_students()
        self.view.show_student_list(students)

    def group_students(self) -> None:
        """
        Groups students by their grades and displays the grouping.
        """
        groups = self.admin_service.group_students_by_grade()
        self.view.show_grade_grouping(groups)
 
    def partition_students(self) -> None:
        """
        Partitions students by their pass/fail status and displays the partitioning.
        """
        partitions = self.admin_service.partition_students_by_status()
        self.view.show_pass_fail_partition(partitions)

    def remove_student(self) -> None:
        """
        Prompts the admin for a student ID and attempts to remove the student with that ID.
        """
        student_id = self.view.get_student_id_to_remove()
        
        if not student_id:
            self.view.show_message("Student ID cannot be empty.")
            return
        removed = self.admin_service.remove_student(student_id)

        if removed:
            self.view.show_student_removed(student_id)
        else:
            self.view.show_message(
                "Cannot find student with ID " + student_id
            )

    def clear_database(self) -> None:
        """
        Clears the students database after confirmation from the admin.
        """
        self.view.show_message("Clearing students database")

        # Ask for confirmation before clearing the database
        if not self.view.confirm_clear_database():
            self.view.show_message("Clear cancelled")
            return

        self.admin_service.clear_all_students()
        self.view.show_message("Students data cleared")
