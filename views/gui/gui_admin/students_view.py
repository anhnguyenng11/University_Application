
from tkinter import Frame, ttk, messagebox


class StudentsView(ttk.Frame):
    def __init__(
        self, parent, groups, on_show_all, on_group, on_partition,
        on_remove, on_clear
    ):
        super().__init__(parent, style="App.TFrame")

        # Student count
        count = sum(len(students) for students in groups.values())

        self.on_remove = on_remove
        self.on_clear = on_clear

        # Page title
        ttk.Label(
            self, text=f"View Students [{count}]", font=("", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 15))

        for text, callback in (
            ("Show All", on_show_all),
            ("Group by Grade", on_group),
            ("PASS/FAIL", on_partition)
        ):
            ttk.Button(
                toolbar, text=text, command=callback
            ).pack(side="left", padx=(0, 8))

        # Main table container
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, ipadx=2)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        border_frame = Frame(
            table_frame,
            highlightbackground="#707070",
            highlightthickness=1,
            borderwidth=0
        )
        border_frame.grid(row=0, column=0, sticky="nsew")
        border_frame.rowconfigure(0, weight=1)
        border_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.layout("AdminStudents.Treeview", [
            ("Treeview.treearea", {"sticky": "nsew"})
        ])

        self.tree = ttk.Treeview(
            border_frame,
            columns=("id", "name", "email", "average", "grade", "status"),
            show="headings",
            selectmode="browse",
            style="AdminStudents.Treeview"
        )

        self.column_ratios = {}

        for column, title, ratio in (
            ("id", "ID", 0.11),
            ("name", "Name", 0.27),
            ("email", "Email", 0.36),
            ("average", "Average", 0.1),
            ("grade", "Grade", 0.08),
            ("status", "Status", 0.08)
        ):
            self.column_ratios[column] = ratio
            self.tree.heading(column, text=title)
            self.tree.column(column, width=1, minwidth=1, stretch=False)

        self.tree.bind("<Configure>", self.resize_columns)

        # Scrollbar
        vertical = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        horizontal = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(yscrollcommand=vertical.set)
        self.tree.configure(xscrollcommand=horizontal.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")

        # Populate student records
        for students in groups.values():
            if not students:
                continue

            if self.tree.get_children():
                self.tree.insert("", "end")

            for student in students:
                average, status, grade = student.get_overall_status()

                self.tree.insert(
                    "",
                    "end",
                    iid=student.student_id,
                    values=(
                        student.student_id,
                        student.name,
                        student.email,
                        f"{average:.2f}" if average is not None else "N/A",
                        grade,
                        status
                    ),
                    tags=("student",)
                )

        # Bottom action buttons
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(15, 0))

        ttk.Button(
            actions,
            text="Remove Selected",
            command=self.confirm_remove
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Clear All",
            command=self.confirm_clear
        ).pack(side="right")

    def resize_columns(self, event):
        for column, ratio in self.column_ratios.items():
            self.tree.column(column, width=int(event.width * ratio))

    def confirm_remove(self):
        selected = self.tree.selection()

        if not selected or "student" not in self.tree.item(
            selected[0], "tags"
        ):
            messagebox.showerror(
                "Select Student",
                "Select a student row first.",
                parent=self
            )
            return

        student_id = selected[0]

        if messagebox.askyesno(
            "Remove Student",
            f"Delete Student {student_id} and their enrollments?",
            parent=self
        ):
            self.on_remove(student_id)

    def confirm_clear(self):
        if messagebox.askyesno(
            "Clear Student Database",
            "Delete all student accounts and enrollments?\n"
            "Admin accounts will remain.",
            parent=self
        ):
            self.on_clear()
