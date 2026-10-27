from tkinter import ttk, messagebox


class SubjectsView(ttk.Frame):
    def __init__(self, parent, student, on_enroll, on_remove):
        super().__init__(parent)

        self.on_enroll = on_enroll
        self.on_remove = on_remove

        style = ttk.Style()
        style.configure("Subjects.TLabelframe.Label", font=("", 10, "bold"))

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 16))

        # Left side: Title
        left = ttk.Frame(header)
        left.pack(side="left", anchor="nw")

        ttk.Label(
            left,
            text="Subjects",
            font=("", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            left,
            text="Students can enroll in a maximum of 4 subjects.",
            font=("", 12, "")
        ).pack(anchor="w", pady=20)


        # Right side: Count and Add button
        right = ttk.Frame(header)
        right.pack(side="right", anchor="ne")

        ttk.Label(
            right,
            text=f"{len(student.subjects)}/4",
            font=("", 20, "bold")
        ).pack(anchor="e")

        ttk.Button(
            right,
            text="+ Enroll Subject",
            command=self.confirm_enroll,
            state="normal" if student.can_enroll() else "disabled"
        ).pack(anchor="e", pady=(12, 0), ipady=5)

        # Fixed-size subject list
        subjects_frame = ttk.LabelFrame(
            self,
            text="Enrolled subjects",
            style="Subjects.TLabelframe",
            padding=(15, 5, 15, 15),
            height=410
        )
        subjects_frame.pack(fill="x", pady=(0, 5))
        subjects_frame.pack_propagate(False)

        if not student.subjects:
            ttk.Label(
                subjects_frame,
                text="No subjects enrolled.",
                font=("", 14)
            ).pack(expand=True)

        for subject in student.subjects:
            card = ttk.LabelFrame(
                subjects_frame,
                padding=12,
                height=85
            )
            card.pack(fill="x", pady=5)

            ttk.Label(
                card,
                text=f"Subject {subject.subject_id}",
                font=("", 14)
            ).pack(side="left", padx=(0, 30))
            
            ttk.Button(
                card,
                text="Remove",
                command=lambda sid=subject.subject_id: self.confirm_remove(sid)
            ).pack(side="right", ipady=5)

    def confirm_enroll(self):
        if messagebox.askyesno(
            "Confirm Enrollment",
            "Do you want to enroll in a new subject?",
            parent=self
        ):
            self.on_enroll()

    def confirm_remove(self, subject_id):
        if messagebox.askyesno(
            "Confirm Removal",
            f"Do you want to remove Subject {subject_id}?",
            parent=self
        ):
            self.on_remove(subject_id)

