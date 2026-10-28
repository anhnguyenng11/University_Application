
from views.cli.admin_view import AdminView
from models.admin import Admin
from models.admin_service import AdminService


class AdminController:
    def __init__(self, view: AdminView, admin_service: AdminService) -> None:
        self.view = view
        self.admin_service = admin_service

    def start(self) -> None:
        self.login_admin()

    def login_admin(self) -> None:
        email, password = self.view.get_login_details("Admin")

        try:
            admin = self.admin_service.login(email, password)
        except ValueError as error:
            self.view.show_message(str(error))
            return

        self.start_admin_session(admin)

    def start_admin_session(self, admin: Admin) -> None:
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

    # show all students
    def show_students(self) -> None:
        students = self.admin_service.get_all_students()
        self.view.show_student_list(students)

    #  group by grade
    def group_students(self) -> None:
        groups = self.admin_service.group_students_by_grade()
        self.view.show_grade_grouping(groups)
 
    #  PASS / FAIL
    def partition_students(self) -> None:
        partitions = self.admin_service.partition_students_by_status()
        self.view.show_pass_fail_partition(partitions)

    #  remove one student
    def remove_student(self) -> None:
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

    #  clear all students
    def clear_database(self) -> None:
        self.view.show_message("Clearing students database")

        # ask Y/N first
        if not self.view.confirm_clear_database():
            self.view.show_message("Clear cancelled")
            return

        self.admin_service.clear_all_students()
        self.view.show_message("Students data cleared")
