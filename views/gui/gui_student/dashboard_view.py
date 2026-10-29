from tkinter import ttk
from views.gui.base_gui_view import setup_styles


class DashboardView(ttk.Frame):
    def __init__(self, parent, student, overall):
        super().__init__(parent, style="UniApp.Page.TFrame")
        setup_styles()

        # Header
        ttk.Label(
            self,
            text="Dashboard",
            style="UniApp.PageTitle.TLabel"
        ).pack(anchor="w", pady=(0, 24))

        # SUBJECTS OVERVIEW
        subjects_frame = ttk.LabelFrame(
            self,
            text="Subjects Overview",
            style="UniApp.Section.TLabelframe",
            padding=(0, 12, 0, 0)
        )
        subjects_frame.pack(fill="x", pady=(0, 24))
        for index in range(2):
            subjects_frame.columnconfigure(index, weight=1, uniform="subjects")
            subjects_frame.rowconfigure(index, weight=1, uniform="subjects")

        # Four subject cards
        for row_index in range(2):
            for col_index in range(2):
                index = row_index * 2 + col_index

                subject = student.subjects[index] if index < len(student.subjects) else None
                card = ttk.LabelFrame(
                    subjects_frame,
                    text=f"Subject {subject.subject_id}" if subject is not None else "Empty slot",
                    style="UniApp.Card.TLabelframe",
                    padding=24
                )

                content = ttk.Frame(card)
                content.pack(fill="x", expand=True)

                if subject is not None:
                    ttk.Label(
                        content,
                        text=f"Mark: {subject.mark}",
                        style="UniApp.Muted.TLabel"
                    ).pack(anchor="w")

                    ttk.Label(
                        content,
                        text=f"Grade: {subject.grade}",
                        style="UniApp.Strong.TLabel"
                    ).pack(anchor="w", pady=(8, 0))

                else:
                    ttk.Label(
                        content,
                        text="N/A",
                        style="UniApp.Metric.TLabel"
                    ).pack(anchor="w")

                card.grid(
                    row=row_index, column=col_index, sticky="nsew",
                    padx=(0, 12) if col_index == 0 else 0,
                    pady=(0, 12) if row_index == 0 else 0
                )

        # OVERALL STATISTICS
        average, status, grade = overall

        overall_frame = ttk.LabelFrame(
            self,
            text="Overall Statistics",
            style="UniApp.Section.TLabelframe",
            padding=(0, 12, 0, 0)
        )
        overall_frame.pack(fill="x")

        data = [
            ("Average Mark", f"{average:.2f}" if average is not None else "N/A"),
            ("Status", status),
            ("Grade", grade)
        ]

        for index, (title, value) in enumerate(data):
            overall_frame.columnconfigure(index, weight=1, uniform="statistics")
            card = ttk.LabelFrame(
                overall_frame,
                text=title,
                style="UniApp.Card.TLabelframe",
                padding=(16, 20)
            )

            card.grid(
                row=0, column=index, sticky="nsew",
                padx=(0, 12) if index < 2 else 0
            )

            ttk.Label(
                card,
                text=value,
                style="UniApp.Metric.TLabel"
            ).pack(side="left", anchor="w")
