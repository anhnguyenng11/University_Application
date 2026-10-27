from tkinter import ttk


class DashboardView(ttk.Frame):
    def __init__(self, parent, student, overall):
        super().__init__(parent)

        style = ttk.Style()
        style.configure("Section.TLabelframe.Label", font=("", 10, "bold"))
        style.configure("Card.TLabelframe.Label", font=("", 10, "italic"))

        # Header
        ttk.Label(
            self,
            text="Dashboard",
            font=("", 20, "bold")
        ).pack(anchor="w", pady=(0, 20))

        # SUBJECTS OVERVIEW
        subjects_frame = ttk.LabelFrame(
            self,
            text="Subjects Overview",
            style="Section.TLabelframe",
            padding=15
        )
        subjects_frame.pack(fill="x", pady=(0, 15))

        # Four subject cards
        for row_index in range(2):
            row = ttk.Frame(subjects_frame)
            row.pack(fill="x", pady=10)

            for col_index in range(2):
                index = row_index * 2 + col_index

                subject = student.subjects[index] if index < len(student.subjects) else None
                card = ttk.LabelFrame(
                    row,
                    text=f"Subject {subject.subject_id}" if subject is not None else "Empty slot",
                    style="Card.TLabelframe",
                    padding=15
                )

                content = ttk.Frame(card)
                content.pack(fill="x", expand=True)

                if subject is not None:
                    ttk.Label(
                        content,
                        text=f"Mark: {subject.mark}",
                        font=("", 12)
                    ).pack(anchor="w")

                    ttk.Label(
                        content,
                        text=f"Grade: {subject.grade}",
                        font=("", 14, "bold")
                    ).pack(anchor="w", pady=(10, 0))

                else:
                    ttk.Label(
                        content,
                        text="N/A",
                        font=("", 14, "")
                    ).pack(anchor="w")

                card.configure(height=120)
                card.pack_propagate(False)

                card.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=(0, 10) if col_index == 0 else (10, 0)
                )

        ttk.Frame(self, height=5).pack()
        # OVERALL STATISTICS
        average, status, grade = overall

        overall_frame = ttk.LabelFrame(
            self,
            text="Overall Statistics",
            style="Section.TLabelframe",
            padding=15
        )
        overall_frame.pack(fill="x")

        data = [
            ("Average Mark", f"{average:.2f}" if average is not None else "N/A"),
            ("Status", status),
            ("Grade", grade)
        ]

        for index, (title, value) in enumerate(data):
            card = ttk.LabelFrame(
                overall_frame,
                text=title,
                style="Card.TLabelframe",
                padding=10,
                width=200,
                height=85
            )

            card.pack_propagate(False)

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 15) if index < 2 else 0,
                pady=(0, 5)
            )

            ttk.Label(
                card,
                text=value,
                font=("", 14, "bold")
            ).pack(side="left", anchor="w")
