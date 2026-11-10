from tkinter import ttk, messagebox

class SearchStudentsView(ttk.Frame):
    def __init__(self, parent, on_search, on_remove):
        super().__init__(parent, style="App.TFrame")

        self.on_search = on_search
        self.on_remove = on_remove
        self.displayed_student_id = None

        style = ttk.Style()
        style.configure("Search.TLabelframe.Label", font=("", 10, "bold"))
        style.configure("Search.TButton", font=("", 12, ""))

        header = ttk.Frame(self)
        header.pack(fill='x')

        ttk.Label(
            header,
            text="Search Students",
            font=("", 20, "bold")
        ).pack(side="left", anchor="w", pady=(0, 15))

        ttk.Button(
            header,
            text="Search",
            style= "Search.TButton",
            command=self.submit_search
        ).pack(side="right", anchor="e", ipady=5)

        self.remove_button = ttk.Button(
            header,
            text="Remove",
            style= "Search.TButton",
            command=self.confirm_remove,
            state="disabled"
        )
        self.remove_button.pack(side="right", anchor="e", ipady=5, padx=(0, 8))

        search_frame = ttk.LabelFrame(
            self, 
            text="Search by ID and Email", 
            style="Search.TLabelframe",
            padding=10)
        search_frame.pack(fill="x")

        search_frame.columnconfigure(1, weight=1)

        ttk.Label(
            search_frame,
            text="Student ID",
            font=("", 12)
        ).grid(row=0, column=0, sticky="w", padx=(0, 15))

        self.student_id_entry = ttk.Entry(search_frame)
        self.student_id_entry.grid(
            row=0, column=1, sticky="ew", ipady=5, pady=5
        )

        ttk.Label(
            search_frame,
            text="Email",
            font=("", 12)
        ).grid(row=1, column=0, sticky="w", padx=(0, 15))

        self.email_entry = ttk.Entry(search_frame)
        self.email_entry.grid(
            row=1, column=1, sticky="ew", ipady=5, pady=5
        )

        self.result_frame = ttk.Frame(self)
        self.result_frame.pack(fill="both", expand=True, pady=(15, 0))

    def clear_result(self):
        self.displayed_student_id = None
        self.remove_button.configure(state="disabled")
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def submit_search(self):
        self.clear_result()
        self.on_search(
            self.student_id_entry.get(),
            self.email_entry.get()
        )

    def show_student(self, student):
        self.clear_result()

        if student is None:
            ttk.Label(
                self.result_frame,
                text="No student matches that ID and email."
            ).pack(anchor="w")
            return

        average, status, grade = student.get_overall_status()
        average_text = f"{average:.2f}" if average is not None else "N/A"

        info_frame = ttk.LabelFrame(
            self.result_frame,
            text="Student Information",
            style='Search.TLabelframe',
            padding=15
        )
        info_frame.pack(fill="x")

        info_table = ttk.Treeview(
            info_frame,
            columns=("id", "name", "email"),
            show="headings",
            height=1,
            selectmode="none"
        )

        for column, title, width in (
            ("id", "Student ID", 100),
            ("name", "Name", 200),
            ("email", "Email", 300)
        ):
            info_table.heading(column, text=title)
            info_table.column(column, width=width, anchor="center")

        info_table.insert(
            "", "end", values=(student.student_id, student.name, student.email)
        )
        info_table.pack(fill="x")

        subjects_frame = ttk.LabelFrame(
            self.result_frame,
            text="Enrollments and Overall Statistics",
            style='Search.TLabelframe',
            padding=15
        )
        subjects_frame.pack(fill="x", pady=(10, 0))

        if not student.subjects:
            ttk.Label(
                subjects_frame,
                text="No subjects enrolled."
            ).pack(anchor="w")
        else:
            table = ttk.Treeview(
                subjects_frame,
                columns=("id", "mark", "grade"),
                show="headings",
                height=4,
                selectmode="none"
            )

            for column, title in (
                ("id", "Subject ID"),
                ("mark", "Mark"),
                ("grade", "Grade")
            ):
                table.heading(column, text=title)
                table.column(column, width=100, anchor="center")

            for subject in student.subjects:
                table.insert(
                    "",
                    "end",
                    values=(subject.subject_id, subject.mark, subject.grade)
                )

            table.pack(fill="x")

            overall_frame = ttk.LabelFrame(
                self.result_frame,
                padding=15
            )
            overall_frame.pack(fill="x", pady=(0, 0))

            overall_table = ttk.Treeview(
                overall_frame,
                columns=("average", "grade", "status"),
                show="headings",
                height=1,
                selectmode="none"
            )

            for column, title in (
                ("average", "Average Mark"),
                ("grade", "Grade"),
                ("status", "Status")
            ):
                overall_table.heading(column, text=title)
                overall_table.column(column, width=100, anchor="center")

            overall_table.insert("", "end", values=(average_text, grade, status))
            overall_table.pack(fill="x")

        self.displayed_student_id = student.student_id
        self.remove_button.configure(state="normal")

    def confirm_remove(self):
        if self.displayed_student_id is None:
            return

        if messagebox.askyesno(
            "Remove Student",
            f"Delete Student {self.displayed_student_id} and their enrollments?",
            parent=self
        ):
            self.on_remove(self.displayed_student_id)
