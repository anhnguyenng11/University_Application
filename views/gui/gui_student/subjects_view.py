import tkinter as tk
from tkinter import ttk, messagebox

class SubjectsView(ttk.Frame):
    def __init__(self, parent, student, on_enroll, on_remove):
        super().__init__(parent, style="App.TFrame")

        self.on_enroll = on_enroll
        self.on_remove = on_remove

        self.columnconfigure(0, weight=1)
        # Row 1 (the subjects list) will absorb residual vertical space
        self.rowconfigure(1, weight=1) 

        header = ttk.Frame(self, style="App.TFrame")
        header.grid(row=0, column=0, sticky="WE", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        # Left structural node
        left = ttk.Frame(header, style="App.TFrame")
        left.grid(row=0, column=0, sticky="W")

        ttk.Label(
            left, text="Subjects", style="Title.TLabel"
        ).grid(row=0, column=0, sticky="W")

        ttk.Label(
            left, 
            text="Students can enroll in a maximum of 4 subjects.", 
            style="Muted.TLabel"
        ).grid(row=1, column=0, sticky="W", pady=(5, 0))

        # Right structural node (Count and Action)
        right = ttk.Frame(header, style="App.TFrame")
        right.grid(row=0, column=1, sticky="E")

        ttk.Label(
            right, text=f"{len(student.subjects)}/4", style="Heading.TLabel"
        ).grid(row=0, column=0, sticky="E")

        ttk.Button(
            right,
            text="+ Enroll Subject",
            command=self.confirm_enroll,
            style="Primary.TButton",
            state="normal" if student.can_enroll() else "disabled"
        ).grid(row=1, column=0, sticky="E", pady=(12, 0))

        # Subject list container
        subjects_container = ttk.Frame(self, style="App.TFrame")
        subjects_container.grid(row=1, column=0, sticky="NSEW")
        subjects_container.columnconfigure(0, weight=1)
        subjects_container.rowconfigure(1, weight=1)

        ttk.Label(
            subjects_container, text="Enrolled subjects", style="Heading.TLabel"
        ).grid(row=0, column=0, sticky="W", pady=(0, 15))

        # Canvas and scrollbar setup
        canvas_frame = ttk.Frame(subjects_container, style="App.TFrame")
        canvas_frame.grid(row=1, column=0, sticky="NSEW")
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        canvas = tk.Canvas(canvas_frame, highlightthickness=0, bg="#F9FAFB") 
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas, style="App.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width)
        )
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="NSEW")
        scrollbar.grid(row=0, column=1, sticky="NS")
        
        scrollable_frame.columnconfigure(0, weight=1)

        # Dynamic population of the list matrix
        if not student.subjects:
            ttk.Label(
                scrollable_frame,
                text="No subjects enrolled.",
                style="Muted.TLabel"
            ).grid(row=0, column=0, pady=50)

        for index, subject in enumerate(student.subjects):
            card = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=15)
            card.grid(row=index, column=0, sticky="WE", pady=(0, 10))
            # Column 0 receives weight to push the Remove button flush against the right boundary
            card.columnconfigure(0, weight=1) 

            ttk.Label(
                card,
                text=f"Subject {subject.subject_id}",
                style="Form.TLabel"
            ).grid(row=0, column=0, sticky="W")
            
            ttk.Button(
                card,
                text="Remove",
                command=lambda sid=subject.subject_id: self.confirm_remove(sid),
                style="Secondary.TButton"
            ).grid(row=0, column=1, sticky="E")

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
            f"Do you want to remove subject {subject_id}?",
            parent=self
        ):
            self.on_remove(subject_id)