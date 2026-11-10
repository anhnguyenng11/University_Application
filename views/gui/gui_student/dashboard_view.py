import tkinter as tk
from tkinter import ttk
from utils import constants

class DashboardView(ttk.Frame):
    def __init__(self, title, parent, student, overall):
        super().__init__(parent, style="App.TFrame")

        self.winfo_toplevel().title(f"UniApp - {title}")
        
        # Grant the master container spatial elasticity
        self.columnconfigure(0, weight=1)
        # Permits the subjects area to absorb vertical space
        self.rowconfigure(1, weight=1) 

        ttk.Label(
            self,
            text="Dashboard",
            style="Title.TLabel" 
        ).grid(row=0, column=0, sticky="W", pady=(0, 20))

        # Scrollable container
        canvas_frame = ttk.Frame(self)
        canvas_frame.grid(row=1, column=0, sticky="NSEW", pady=(0, 15))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        canvas = tk.Canvas(canvas_frame, highlightthickness=0, bg=constants.COLORS["background"])
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        scrollable_subjects = ttk.Frame(canvas, style="App.TFrame")
        
        # Dynamically update the scroll region when internal widgets resize
        scrollable_subjects.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Embed the frame inside the canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_subjects, anchor="nw")
        
        # Force the interior frame to expand horizontally with the canvas
        canvas.bind(
            "<Configure>", 
            lambda e: canvas.itemconfig(canvas_window, width=e.width)
        )
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="NS")

        # Subjects overview
        ttk.Label(
            scrollable_subjects,
            text="Subjects Overview",
            style="Heading.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="W", pady=(0, 15))

        scrollable_subjects.columnconfigure(0, weight=1, uniform="col")
        scrollable_subjects.columnconfigure(1, weight=1, uniform="col")

        # Replicating the 4-slot rendering logic via grid mathematics
        for index in range(4):
            row_index = (index // 2) + 1
            col_index = index % 2

            subject = student.subjects[index] if index < len(student.subjects) else None
            
            card = ttk.Frame(scrollable_subjects, style="Card.TFrame", padding=15)
            card.grid(
                row=row_index, 
                column=col_index, 
                sticky="WE", 
                padx=(0, 10) if col_index == 0 else (10, 0),
                pady=(0, 15)
            )

            if subject is not None:
                ttk.Label(
                    card, text=f"Subject {subject.subject_id}", style="Form.TLabel"
                ).grid(row=0, column=0, sticky="W", pady=(0, 10))
                
                ttk.Label(
                    card, text=f"Mark: {subject.mark}", style="Body.TLabel"
                ).grid(row=1, column=0, sticky="W")

                if subject.grade == "Z":
                    ttk.Label(
                        card, text=f"Grade: {subject.grade} - {constants.GRADE_DEFINITIONS[subject.grade]}", style="Error.TLabel"
                    ).grid(row=2, column=0, sticky="W", pady=(10, 0))
                else:
                    ttk.Label(
                        card, text=f"Grade: {subject.grade} - {constants.GRADE_DEFINITIONS[subject.grade]}", style="Success.TLabel"
                    ).grid(row=2, column=0, sticky="W", pady=(10, 0))
            else:
                ttk.Label(
                    card, text="Empty subject slot", style="Muted.TLabel"
                ).grid(row=0, column=0, sticky="W", pady=(0, 10))
                
                ttk.Label(
                    card, text="N/A", style="Body.TLabel"
                ).grid(row=1, column=0, sticky="W")

        # Overall statistics
        overall_frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        overall_frame.grid(row=2, column=0, sticky="WE")
        
        # Distribute horizontal space equally across the 3 statistical pillars
        for i in range(3):
            overall_frame.columnconfigure(i, weight=1, uniform="stat")

        ttk.Label(
            overall_frame,
            text="Overall Statistics",
            style="Heading.TLabel"
        ).grid(row=0, column=0, columnspan=3, sticky="W", pady=(0, 15))

        average, status, grade = overall
        data = [
            ("Average Mark", f"{average:.2f}" if average is not None else "N/A"),
            ("Status", status),
            ("Grade", grade)
        ]

        # Iterative column indexing
        # Iterative column indexing
        for index, (title, value) in enumerate(data):
            card = ttk.Frame(overall_frame, style="Card.TFrame", padding=15)
            card.grid(
                row=1, 
                column=index, 
                sticky="WE", 
                padx=(0, 15) if index < 2 else 0
            )

            ttk.Label(
                card, text=title, style="Muted.TLabel"
            ).grid(row=0, column=0, sticky="W")
            
            value_style = "Form.TLabel"
            if status == "FAIL" and title in ("Status", "Grade"):
                value_style = "Error.TLabel"
            else:
                value_style = "Success.TLabel"
            
            ttk.Label(
                card, text=value, style=value_style
            ).grid(row=1, column=0, sticky="W", pady=(5, 0))