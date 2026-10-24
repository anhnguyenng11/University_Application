UniApp/
│
├── main.py                         # CLI entry point
├── gui_main.py                     # GUI entry point
│
├── models/
│   ├── __init__.py
│   ├── student.py                  # Student
│   ├── subject.py                  # Subject
│   ├── admin.py                    # Admin
│   ├── student_service.py          # StudentService
│   ├── admin_service.py            # AdminService
│   │
│   └── file_handlers/
│       ├── __init__.py
│       ├── database.py              # Shared JSON operations
│       ├── student_data_file.py     # Student data management
│       └── admin_data_file.py       # Admin data management
│
├── views/
│   ├── __init__.py
│   ├── cli_view.py                  # Terminal interface
│   │
│   └── gui/
│       ├── __init__.py
│       ├── login_view.py            # Student login
│       ├── enrollment_view.py       # Subject enrollment
│       ├── subject_view.py          # Enrolled subjects
│       └── error_view.py            # Error / exception window
│
├── controllers/
│   ├── __init__.py
│   ├── cli_uni_app.py              # CLI navigation
│   ├── student_controller.py       # Student operations
│   ├── admin_controller.py         # Admin operations
│   └── gui_uni_app.py              # GUI navigation
│
├── helpers/
│   ├── __init__.py
│   ├── validator.py                # Email/password validation
│   └── id_generator.py             # Unique ID generation
│
├── data/
│   ├── students.data               # JSON student records
│   └── admins.data                 # JSON admin records
│
├── tests/
│   ├── __init__.py
│   ├── test_student.py
│   ├── test_subject.py
│   ├── test_admin.py
│   ├── test_validator.py
│   ├── test_student_service.py
│   ├── test_admin_service.py
│   └── test_database.py
│
├── implement_guide.md
├── README.md
└── .gitignore