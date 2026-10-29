from tkinter import ttk, messagebox
from views.gui.base_gui_view import setup_styles


class SearchStudentsView(ttk.Frame):
    def __init__(self, parent, on_search, on_remove):
        super().__init__(parent, style="UniApp.Page.TFrame")
        setup_styles()

        self.on_search = on_search
        self.on_remove = on_remove
        self.displayed_student_id = None

        header = ttk.Frame(self, style="UniApp.Page.TFrame")
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(
            header,
            text="Search Students",
            style="UniApp.PageTitle.TLabel"
        ).pack(side="left", anchor="w")

        ttk.Button(
            header,
            text="Search",
            style="UniApp.Primary.TButton",
            command=self.submit_search
        ).pack(side="right", anchor="e")

        self.remove_button = ttk.Button(
            header,
            text="Remove",
            style="UniApp.Secondary.TButton",
            command=self.confirm_remove,
            state="disabled"
        )
        self.remove_button.pack(side="right", anchor="e", padx=(0, 12))

        search_frame = ttk.LabelFrame(
            self, 
            text="Search by ID and Email", 
            style="UniApp.Card.TLabelframe",
            padding=(16, 8))
        search_frame.pack(fill="x")

        search_frame.columnconfigure(0, minsize=180)
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(
            search_frame,
            text="Student ID",
            style="UniApp.Caption.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.student_id_entry = ttk.Entry(search_frame, width=16, font="UniApp.Body",
                                          style="UniApp.TEntry")
        self.student_id_entry.grid(
            row=1, column=0, sticky="ew", padx=(0, 24)
        )

        ttk.Label(
            search_frame,
            text="Email",
            style="UniApp.Caption.TLabel"
        ).grid(row=0, column=1, sticky="w", pady=(0, 8))

        self.email_entry = ttk.Entry(search_frame, font="UniApp.Body", style="UniApp.TEntry")
        self.email_entry.grid(
            row=1, column=1, sticky="ew"
        )

        self.result_frame = ttk.Frame(self, style="UniApp.Page.TFrame")
        self.result_frame.pack(fill="both", expand=True, pady=(12, 0))

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
                text="No student matches that ID and email.",
                style="UniApp.PageText.TLabel",
                wraplength=640
            ).pack(anchor="w")
            return

        average, status, grade = student.get_overall_status()
        average_text = f"{average:.2f}" if average is not None else "N/A"

        info_frame = ttk.LabelFrame(
            self.result_frame,
            text="Student Information",
            style="UniApp.Card.TLabelframe",
            padding=(12, 6)
        )
        info_frame.pack(fill="x")

        info_table = ttk.Treeview(
            info_frame,
            columns=("id", "name", "email"),
            show="headings",
            height=1,
            selectmode="none",
            style="UniApp.Treeview"
        )

        for column, title, width in (
            ("id", "Student ID", 100),
            ("name", "Name", 200),
            ("email", "Email", 300)
        ):
            anchor = "center" if column == "id" else "w"
            info_table.heading(column, text=title, anchor=anchor)
            info_table.column(column, width=width, minwidth=width, anchor=anchor)

        info_table.insert(
            "", "end", values=(student.student_id, student.name, student.email)
        )
        info_table.pack(fill="x")
        info_table.bind("<Map>", lambda event: self.size_identity_columns(info_table, student))
        horizontal = ttk.Scrollbar(info_frame, orient="horizontal", command=info_table.xview)
        horizontal.pack(fill="x")
        info_table.configure(xscrollcommand=horizontal.set)

        subjects_frame = ttk.LabelFrame(
            self.result_frame,
            text="Enrollments and Overall Statistics",
            style="UniApp.Card.TLabelframe",
            padding=(12, 6)
        )
        subjects_frame.pack(fill="x", pady=(12, 0))

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
                selectmode="none",
                style="UniApp.Treeview"
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
                padding=(0, 8, 0, 0),
                style="UniApp.Plain.TLabelframe"
            )
            overall_frame.pack(fill="x", pady=(0, 0))

            overall_table = ttk.Treeview(
                overall_frame,
                columns=("average", "grade", "status"),
                show="headings",
                height=1,
                selectmode="none",
                style="UniApp.Treeview"
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

    def size_identity_columns(self, table, student):
        for column, value, minimum in (
            ("id", student.student_id, 100),
            ("name", student.name, 200),
            ("email", student.email, 300)
        ):
            text_width = table.tk.call("font", "measure", "UniApp.Body", str(value))
            table.column(column, width=max(minimum, text_width + 24), stretch=False)

    def confirm_remove(self):
        if self.displayed_student_id is None:
            return

        if messagebox.askyesno(
            "Remove Student",
            f"Delete Student {self.displayed_student_id} and their enrollments?",
            parent=self
        ):
            self.on_remove(self.displayed_student_id)
