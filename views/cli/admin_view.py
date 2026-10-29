"""
This module contains the AdminView class, which provides methods for displaying the admin menu and related information in the CLI.
"""
from views.cli.cli_view import CLIView
from models.student import Student

class AdminView(CLIView):
    """
    Displays the admin menu and related information in the CLI.
    Methods:
    - show_admin_menu: Displays the admin menu and prompts the admin for their choice.
    - show_student_list: Displays the list of students in the system.
    - student_grade_text: Returns a formatted string representing the student's name, ID, grade, and average mark.
    - show_grade_grouping: Displays the grouping of students based on their grades.
    - show_pass_fail_partition: Displays the partitioning of students based on their pass/fail status.
    - get_student_id_to_remove: Prompts the admin for the student ID they want to remove.
    - show_student_removed: Displays a message indicating that the student with the given ID has been removed.
    - confirm_clear_database: Prompts the admin to confirm if they want to clear the database.
    """

    def show_admin_menu(self) -> str:
        """
        Displays the admin menu and prompts the admin for their choice.
        """
        print("\nAdmin System")
        print("(c) Clear Database")
        print("(g) Group Students")
        print("(p) Partition Students")
        print("(r) Remove Student")
        print("(s) Show Students")
        print("(x) Exit")

        choice = input("Admin System (c/g/p/r/s/x): ")
        # Accept both uppercase and lowercase inputs for the choice
        return choice.strip().lower()


    def show_student_list(self, students: list[Student]) -> None:
        """
        Displays the list of students in the system, including their names, IDs, and email addresses.
        """
        print("Student List")

        if len(students) == 0:
            print(" < Nothing to Display >")
            return

        for student in students:
            print(
                student.name
                + " :: "
                + student.student_id
                + " --> Email: "
                + student.email
            )

    def student_grade_text(self, student: Student) -> str:
        """
        Returns a formatted string representing the student's name, ID, grade, and average mark.
        Example: John Smith :: 673358 --> GRADE: C - MARK: 69.25
        """
        average, status, grade = student.get_overall_status()

        if average is None:
            mark = "N/A"
        else:
            mark = f"{average:.2f}"

        return (
            student.name
            + " :: "
            + student.student_id
            + " --> GRADE: "
            + grade
            + " - MARK: "
            + mark
        )

    def show_grade_grouping(self, groups: dict[str, list[Student]]) -> None:
        """
        Displays the grouping of students based on their grades (HD, D, C, P, Z, N/A).
        """
        print("Grade Grouping")

        found_any = False

        for grade in ["HD", "D", "C", "P", "Z", "N/A"]:
            students = groups[grade]

            if len(students) == 0:
                continue

            found_any = True
            print(grade + " -->")

            # one student per row
            for student in students:
                print("  " + self.student_grade_text(student))

        if not found_any:
            print(" < Nothing to Display >")

    def show_pass_fail_partition(
        self,
        partitions: dict[str, list[Student]]
    ) -> None:
        """
        Displays the partitioning of students based on their pass/fail status (PASS, FAIL, N/A).
        """
        print("PASS/FAIL Partition")

        for status in ["PASS", "FAIL", "N/A"]:
            students = partitions[status]
            print(status + " -->")

            if len(students) == 0:
                print("  (none)")
            else:
                # one student per row
                for student in students:
                    print("  " + self.student_grade_text(student))

    def get_student_id_to_remove(self) -> str:
        """
        Prompts the admin for the student ID they want to remove.
        """
        student_id = input("Remove by ID: ")
        return student_id.strip()

    def show_student_removed(self, student_id: str) -> None:
        """
        Displays a message indicating that the student with the given ID has been removed.
        """
        print("Removing student " + student_id + " Account")

    def confirm_clear_database(self) -> bool:
        """
        Prompts the admin to confirm if they want to clear the database.
        """
        answer = input(
            "Are you sure you want to clear the database (Y)ES/(N)O: "
        )
        answer = answer.strip().lower()

        return answer in ("y", "yes")
