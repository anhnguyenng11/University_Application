from tkinter import ttk, messagebox
from views.gui.base_gui_view import setup_styles


class SubjectsView(ttk.Frame):
    def __init__(self, parent, student, on_enroll, on_remove):
        super().__init__(parent, style="UniApp.Page.TFrame")
        setup_styles()

        self.on_enroll = on_enroll
        self.on_remove = on_remove

        # Header
        header = ttk.Frame(self, style="UniApp.Page.TFrame")
        header.pack(fill="x", pady=(0, 16))

        # Left side: Title
        left = ttk.Frame(header, style="UniApp.Page.TFrame")
        left.pack(side="left", anchor="nw")

        ttk.Label(
            left,
            text="Subjects",
            style="UniApp.PageTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            left,
            text="Students can enroll in a maximum of 4 subjects.",
            style="UniApp.PageText.TLabel",
            wraplength=430,
            justify="left"
        ).pack(anchor="w", pady=(12, 0))


        # Right side: Count and Add button
        right = ttk.Frame(header, style="UniApp.Page.TFrame")
        right.pack(side="right", anchor="ne")

        ttk.Label(
            right,
            text=f"{len(student.subjects)}/4",
            style="UniApp.PageTitle.TLabel"
        ).pack(anchor="e")

        ttk.Button(
            right,
            text="+ Enroll Subject",
            style="UniApp.Primary.TButton",
            command=self.confirm_enroll,
            state="normal" if student.can_enroll() else "disabled"
        ).pack(anchor="e", pady=(12, 0))

        # Subject list
        subjects_frame = ttk.LabelFrame(
            self,
            text="Enrolled subjects",
            style="UniApp.Section.TLabelframe",
            padding=(0, 12, 0, 0)
        )
        subjects_frame.pack(fill="both", expand=True)

        if not student.subjects:
            ttk.Label(
                subjects_frame,
                text="No subjects enrolled.",
                style="UniApp.PageText.TLabel"
            ).pack(expand=True)

        for subject in student.subjects:
            card = ttk.LabelFrame(
                subjects_frame,
                padding=(24, 8),
                style="UniApp.Card.TLabelframe"
            )
            card.pack(fill="x", pady=(0, 8))

            ttk.Label(
                card,
                text=f"Subject {subject.subject_id}",
                style="UniApp.Strong.TLabel"
            ).pack(side="left", padx=(0, 30))
            
            ttk.Button(
                card,
                text="Remove",
                style="UniApp.Secondary.TButton",
                command=lambda sid=subject.subject_id: self.confirm_remove(sid)
            ).pack(side="right")

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

