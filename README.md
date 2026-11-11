# University Application

Python MVC student enrolment system for a local university. It provides two front ends that share the same models, services, and file-based storage:

- **CLIUniApp** — terminal menus for students and admins
- **GUIUniApp** — Tkinter desktop UI for the same workflows

Students register and log in, enrol in up to four subjects, view marks and grades, and change their password. Admins can list, group, partition, remove, and clear student records.

---

## Requirements

- **Python 3.10+** (standard library only; no third-party packages)
- **GUI:** a Python installation with Tkinter (`_tkinter`)

---

## Quick start

Run commands from the project root so package imports resolve.

### CLI

```bash
python3 main.py
```

University menu:

```text
University System
(A) Admin
(S) Student
(X) Exit
University System (A/S/X):
```

| Key | Action |
|-----|--------|
| `A` | Admin login and management subsystem |
| `S` | Student subsystem (login / register) |
| `X` | Exit |

### GUI

```bash
python3 gui_main.py
```

Confirm Tkinter is available before launching the GUI:

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

If that command fails, install or use a Tk-enabled Python distribution for your operating system.

CLI and GUI share `data/students.data` and `data/admins.data`.

---

## Features

### Student

- Register with validated name, email, and password
- Login and open the subject enrolment menu
- Enrol in up to **4** subjects (each gets a random mark 25–100 and a grade)
- Remove a subject by ID
- Show enrolled subjects with marks and grades
- Change password

### Admin

Admins sign in with an account from `data/admins.data`. From the university menu choose `A`, then:

| Key | Action |
|-----|--------|
| `c` | Clear all students in `students.data` (with confirmation) |
| `g` | Group students by overall grade |
| `p` | Partition students into PASS / FAIL / N/A |
| `r` | Remove a student by ID |
| `s` | Show all students |
| `x` | Exit to university menu |

### Admin (GUI)

Provides the same student-management actions, account password changes, and search by student ID and email.

---

## Validation rules

| Field | Rule |
|-------|------|
| Email | Must match `*@university.com` (e.g. `john.smith@university.com`) |
| Password | Starts with an uppercase letter, at least five letters total, then three or more digits (e.g. `Helloworld123`) |
| Student ID | Random 6-digit ID (`000001`–`999999`) |
| Subject ID | Random 3-digit ID (`001`–`999`) |
| Subject limit | Maximum 4 subjects per student |

### Grades

| Mark | Grade |
|------|-------|
| ≥ 85 | HD |
| ≥ 75 | D |
| ≥ 65 | C |
| ≥ 50 | P |
| &lt; 50 | Z |

A student **PASS**es when the average of enrolled subjects is ≥ 50; otherwise **FAIL**. Students with no subjects are **N/A**.

---

## Project structure

```text
./
├── main.py                 # CLI entry point
├── gui_main.py             # GUI entry point
├── Assessment_brief.md     # Assignment requirements and sample I/O
├── controllers/
│   ├── cli/                # CLI controllers (university, student, admin)
│   └── gui/                # GUI controllers
├── models/
│   ├── student.py
│   ├── subject.py
│   ├── admin.py
│   ├── student_service.py
│   ├── admin_service.py
│   └── file_handlers/      # students.data / admins.data persistence
├── views/
│   ├── cli/                # Terminal menus and prompts
│   └── gui/                # Tkinter screens
├── utils/                  # Constants, validation, IDs, grades
└── data/
│   ├── students.data
│   └── admins.data
```

Architecture is MVC-style: views handle I/O, controllers wire menus to services, and models own domain logic and file storage. Both front ends use the same `StudentService` and `AdminService`.

---

## Data files

| File | Purpose |
|------|---------|
| `data/students.data` | Registered students and enrolments |
| `data/admins.data` | Admin accounts |

These are JSON files despite their `.data` extension and are created automatically if missing. Clearing the database from Admin empties `students.data`.

## Security note

This is an educational local application. Passwords are stored in plaintext JSON files, so do not use real credentials or deploy it as-is.

---

## Sample CLI session

```text
University System
(A) Admin
(S) Student
(X) Exit
University System (A/S/X): S

Student System (l/r/x): r
... register with email @university.com and a valid password ...
Student System (l/r/x): l
... login ...
Student Course Menu (c/e/r/s/x): e
... enrol subjects ...
Student Course Menu (c/e/r/s/x): s
... show enrolments ...
Student Course Menu (c/e/r/s/x): x
Student System (l/r/x): x
University System (A/S/X): X
Exiting University System.
```

See `Assessment_brief.md` for full sample I/O and grading criteria.

---

## Contributors

| Name | Contribution |
|------|----------------|
| Duc Manh Duong | GUI (`gui_main.py`, controllers, views), utils |
| Hiu Ying Lee | Admin model, admin service, and admin data file |
| Anh Nguyen Nguyen | CLI (`main.py`, controllers, views) |
| Ching Ha To | Student model, subject model, student service, data / file handlers |
