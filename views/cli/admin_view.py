from views.base_cli_view import BaseCLIView
from models.student import Student


class AdminView(BaseCLIView):

    def show_admin_menu(self) -> str:
        
        print("\nAdmin System")
        print("(c) Clear Database")
        print("(g) Group Students")
        print("(p) Partition Students")
        print("(r) Remove Student")
        print("(s) Show Students")
        print("(x) Exit")

        choice = input("Admin System (c/g/p/r/s/x): ")
        return choice.strip().lower()


    def show_student_list(self, students: list[Student]) -> None:
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

    # used by group and partition
    # example: John Smith :: 673358 --> GRADE: C - MARK: 69.25
    def student_grade_text(self, student: Student) -> str:
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
        print("PASS/FAIL Partition")

        for status in ["PASS", "FAIL"]:
            students = partitions[status]
            print(status + " -->")

            if len(students) == 0:
                print("  (none)")
            else:
                # one student per row
                for student in students:
                    print("  " + self.student_grade_text(student))

    def get_student_id_to_remove(self) -> str:
        student_id = input("Remove by ID: ")
        return student_id.strip()

    def show_student_removed(self, student_id: str) -> None:
        print("Removing student " + student_id + " Account")

    def confirm_clear_database(self) -> bool:
        answer = input(
            "Are you sure you want to clear the database (Y)ES/(N)O: "
        )
        answer = answer.strip().lower()

        if answer == "y":
            return True

        if answer == "yes":
            return True

        return False
