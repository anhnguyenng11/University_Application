
from tkinter import Frame, ttk, messagebox
from views.gui.base_gui_view import COLORS, setup_styles


class StudentsView(ttk.Frame):
    def __init__(
        self, parent, groups, on_show_all, on_group, on_partition,
        on_remove, on_clear
    ):
        super().__init__(parent, style="UniApp.Page.TFrame")
        setup_styles()

        # Student count
        count = sum(len(students) for students in groups.values())

        self.on_remove = on_remove
        self.on_clear = on_clear

        # Page title
        ttk.Label(
            self, text=f"View Students [{count}]", style="UniApp.AdminTitle.TLabel"
        ).pack(anchor="w", pady=(0, 16))

        # Toolbar
        toolbar = ttk.Frame(self, style="UniApp.Page.TFrame")
        toolbar.pack(fill="x", pady=(0, 12))

        for text, callback in (
            ("Show All", on_show_all),
            ("Group by Grade", on_group),
            ("PASS/FAIL", on_partition)
        ):
            ttk.Button(
                toolbar, text=text, command=callback, style="Compact.UniApp.Secondary.TButton"
            ).pack(side="left", padx=(0, 8))

        # Main table container
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        border_frame = Frame(
            table_frame,
            background=COLORS["canvas"],
            highlightbackground=COLORS["hairline"],
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
        self.column_minimums = {}

        for column, title, ratio, minimum, anchor in (
            ("id", "ID", 0.11, 76, "center"),
            ("name", "Name", 0.27, 140, "w"),
            ("email", "Email", 0.36, 240, "w"),
            ("average", "Average", 0.1, 80, "center"),
            ("grade", "Grade", 0.08, 64, "center"),
            ("status", "Status", 0.08, 64, "center")
        ):
            self.column_ratios[column] = ratio
            self.column_minimums[column] = minimum
            self.tree.heading(column, text=title, anchor=anchor)
            self.tree.column(column, width=minimum, minwidth=minimum,
                             stretch=False, anchor=anchor)

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
        actions = ttk.Frame(self, style="UniApp.Page.TFrame")
        actions.pack(fill="x", pady=(12, 0))

        ttk.Button(
            actions,
            text="Remove Selected",
            style="Compact.UniApp.Danger.TButton",
            command=self.confirm_remove
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Clear All",
            style="Compact.UniApp.Danger.TButton",
            command=self.confirm_clear
        ).pack(side="right")

    def resize_columns(self, event):
        extra_width = max(0, event.width - 2 - sum(self.column_minimums.values()))
        for column, ratio in self.column_ratios.items():
            self.tree.column(column, width=self.column_minimums[column] + int(extra_width * ratio))

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
