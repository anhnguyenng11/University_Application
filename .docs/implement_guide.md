# UniApp — Implementation Guide for AI-Assisted or Self-Directed Development

> **Project:** UTS 32555 University Application (Assessment 1, Parts 1–3)  
> **Language:** Python 3  
> **Architecture:** MVC + Helpers + File Handlers inside `models/` (no top-level `services/` or `storage/` directory)  
> **Interfaces:** CLI first, then student-only Tkinter GUI  
> **Data:** JSON serialized in `students.data` and `admins.data`  
> **Default assistance mode:** `GUIDED`

## 0. How to use this file

Read this document **before suggesting, editing, or generating project code**. Treat it as the project's implementation contract. If the repository or source documents are available, inspect them before advising. Do not assume that a task is complete merely because a file exists.

At the beginning of each working session, identify the active mode:

- **`MODE=GUIDED` (default):** Act as a programming tutor. Do **not** create or edit project source files, run destructive commands, or implement a feature end-to-end. Give the student **one manageable step at a time**: the exact file, the class/methods to work on, the intended behavior, a suggested approach or pseudocode, commands to run, and objective acceptance tests. Invite the student to write and share their code/output; then review and debug it before advancing. Explain Python and MVC concepts as needed. Small illustrative snippets may be provided when requested, but prioritize student-authored solutions.
- **`MODE=IMPLEMENT` (explicit opt-in):** Help build a **learning/reference prototype** in small, independently testable increments. Explain each change, identify affected files, run tests when tools are available, and report what was actually verified. **Important:** The assessment expressly forbids submission of AI-generated code and warns of a possible zero mark. Do not describe automatically generated code as submission-ready or advise the student to submit it unchanged. The student's final submission must comply with their course's academic-integrity rules.

**To switch modes**, the user may say `MODE=GUIDED` or `MODE=IMPLEMENT` at any time. A request such as “start Step 2” retains the current mode. If no mode has been provided, assume `GUIDED`.

**Response format for each step:**
1. **Current milestone and goal** (reference the source requirement/story IDs).
2. **Files to work on** (exact paths and responsibilities).
3. **What to implement** (method names, parameters, return behavior, validation, exceptions; precise instructions without completing the whole project in GUIDED mode).
4. **How to test** (commands, example inputs, expected results including one error case).
5. **Done criteria** (short checklist).
6. **Next milestone** (name only; do not proceed until the present milestone is checked).

In `GUIDED` mode, make the first reply actionable without writing full feature implementations: show exact file contents only for minimal scaffolding or if the student explicitly requests an educational example. Never present untested code as tested.

Use **American English** for all prose, comments, and suggested identifiers except where exact assignment sample I/O requires other spelling (e.g., `enrol`, `enrolment`). Keep explanations clear and concrete. Do not make unrequested architectural changes.

---

## 1. Source documents and priority

Read these uploaded sources when available:

1. `Assessment+1+-+Part+2+and+Part+3.pdf` — official functional requirements, sample I/O, rubric, GUI, submission/showcase expectations.
2. `UniApp_Class_Diagram.drawio.png` — Part 1 UML and preselected classes, attributes, and methods.
3. `Task_2_User_story_backlog.pdf` (or its `.docx` equivalent) — group user stories 100–503.
4. `Assessment Brief.pdf` — explanatory breakdown and recommended CLI-to-GUI development sequence.

**Precedence for implementation decisions:**
- The official Part 2 & 3 requirements and rubric define the minimum assessed functionality.
- The group's **explicit decisions** in Section 2 below define intended additions (especially mandatory admin login). These additions must not break the assessed functionality.
- Preserve UML/backlog names and responsibilities where feasible. If the design needs to deviate, **identify the conflict and propose the smallest change**; do not silently rewrite the diagram or stories.
- Sample I/O is the reference for CLI prompts, casing, indentation, feedback, and workflow. Validate presentation against the actual screenshots on pages 3–7 rather than inventing identical-looking text.

The available files include an explanatory Assessment Brief, the Part 2 & 3 brief, a UML diagram, and a group backlog. Do **not** claim that a separate full Part 1 specification was reviewed unless it is actually supplied.

### Academic-integrity requirement

Official Part 2 & 3 brief, Section 7: **“Do NOT use AI-generated code.”** The document warns that suspected AI-generated submissions can receive zero. Therefore **GUIDED mode is preferred for the assessed work**. Code examples, prototypes, and reviews must not be represented as an exception to that instruction.

---

## 2. Fixed team design decisions

These decisions have already been made. Do not repeatedly ask the user to reconfirm them.

1. Use **Python**, not Java.
2. Use **MVC**, keeping presentation separate from application logic.
3. Use the existing UML's `StudentService` and `AdminService`, but keep them under `models/` as part of the broader Model layer. **Do not add a top-level `services/` folder.**
4. Keep reusable stateless utilities in **`helpers/`** (`Validator`, `IDGenerator`).
5. Keep the file-handling classes in **`models/file_handlers/`** (`Database`, `StudentDataFile`, `AdminDataFile`) as a subsection of the Model layer; do not create a top-level `storage/` folder.
6. Require **both Student login and Admin login in the CLI**. Students may register through the CLI; **admins are preconfigured and cannot self-register**.
7. Keep **`students.data` and `admins.data`** as separate files, each containing valid JSON despite the `.data` extension.
8. The **Tkinter GUI is student-only**: no admin login, admin management, or student registration within the GUI.
9. Build and test the **CLI before the GUI**, and share the same student models, controllers, and data file across both.
10. Prefer one major class per file; use descriptive names, simple methods, standard Python libraries, and testable units.

### Known conflicts that must remain visible

| Topic | Official brief | UML / backlog / user decision | Resolution |
|---|---|---|---|
| Admin access | Admin enters subsystem without logging in (Part 2 §2) | UML/backlog define admin login; user explicitly wants it | **Implement admin login as an added security step**, while preserving all required admin commands after authentication; document this extension for assessment/demo. |
| Admin storage | All student CRUD must act on `students.data`; no separate admin file required | UML defines `AdminDataFile`; user selected `admins.data` | Use `admins.data` **only for admin identities**. Admin actions continue to operate on `students.data`. |
| Database classes | `Student`, `Subject`, `Database` are the minimum (Part 2 §3) | UML specifies `StudentDataFile` and `AdminDataFile` | Include `models/file_handlers/database.py` for shared safe JSON I/O and specific file-handler classes for student/admin records. |
| PASS/FAIL unit | Part 2 §3: student passes when average of four subject marks is ≥50; recompute average on every enrollment (Part 2 §4) | Backlog story 405 words this as per-mark classification | Use **student's overall average** for admin PASS/FAIL grouping; use per-subject mark for `Subject.get_pass_fail_status()`. Explicitly define how a partially enrolled student is displayed. |
| Overall grade | Sample admin grouping shows grade and average mark per student | `Subject` UML provides a per-subject grade | Compute student overall grade **from average mark** for admin grouping. Individual subjects keep their own grades. |
| Stored password | UML has `password: str`; samples show user-entered passwords | JSON design can store either plaintext or password hashes | Prefer a salted, slow password hash for stored credentials and a consistent verification method; never display credentials. Record any compatibility decision before persistence is coded. |

Do not delete `Admin`, `AdminService`, or `AdminDataFile` merely because admin login is beyond the minimum specification.

---

## 3. Frozen project structure

Create the package marker files shown below (`__init__.py` may remain empty):

```text
UniApp/
├── main.py                          # CLI entry point
├── gui_main.py                      # Tkinter GUI entry point
├── models/
│   ├── __init__.py
│   ├── student.py                   # Student
│   ├── subject.py                   # Subject
│   ├── admin.py                     # Admin
│   ├── student_service.py           # StudentService (business operations)
│   ├── admin_service.py             # AdminService (business operations)
│   └── file_handlers/
│       ├── __init__.py
│       ├── database.py              # Database (shared JSON operations)
│       ├── student_data_file.py     # StudentDataFile (student records)
│       └── admin_data_file.py       # AdminDataFile (admin records)
├── views/
│   ├── __init__.py
│   ├── cli_view.py                  # Terminal input and output
│   └── gui/
│       ├── __init__.py
│       ├── login_view.py            # Student login window
│       ├── enrollment_view.py       # Enrollment window
│       ├── subject_view.py          # Enrolled subjects window
│       └── error_view.py            # Errors and exceptions
├── controllers/
│   ├── __init__.py
│   ├── cli_uni_app.py               # CLI navigation
│   ├── student_controller.py        # Student user actions
│   ├── admin_controller.py          # Admin user actions
│   └── gui_uni_app.py               # GUI navigation
├── helpers/
│   ├── __init__.py
│   ├── validator.py                 # Validator (email/password/empty)
│   └── id_generator.py              # IDGenerator (IDs and marks)
├── data/
│   ├── students.data                # JSON student records
│   └── admins.data                  # JSON admin records
├── tests/
│   ├── __init__.py
│   ├── test_student.py
│   ├── test_subject.py
│   ├── test_admin.py
│   ├── test_validator.py
│   ├── test_student_service.py
│   ├── test_admin_service.py
│   └── test_database.py
├── implement_guide.md
├── README.md
└── .gitignore
```

**Do not add new top-level architecture directories or framework dependencies** unless a concrete requirement justifies them. Optional support modules (for example, a shared password-hashing utility) should be proposed before adding them, not silently introduced.

### Layer ownership

`models/file_handlers/` is **inside the MVC Model layer**. It is a package for file I/O, not a fourth MVC layer.


| Layer | Can do | Must not do |
|---|---|---|
| `models/` | Domain state, invariants, grade calculations, application-level operations, and model-layer file handling | Read input from terminal; render Tkinter; put low-level JSON I/O inside domain entity classes |
| `views/` | Display prompts/windows, gather input, display success/error responses | Create grades/IDs; decide authentication; read/write `.data` files |
| `controllers/` | Process user actions, call Model operations, direct navigation, handle expected errors | Duplicate grade/enrollment rules; hand-edit JSON |
| `helpers/` | Stateless validation, unique-ID generation, random mark generation | Decide workflows; print UI messages; persist records |
| `models/file_handlers/` | Initialize, parse, serialize, load/save/find/remove/clear JSON data | Display UI; enforce the four-subject limit |

The `StudentService` and `AdminService` classes live **inside the Model layer** as agreed. They coordinate models, validation, and file handlers; keep core invariants on domain models so the same rule cannot be bypassed through a different interface.

### Dependencies and entry points

Both interfaces must use the same student model logic and the same `data/students.data` file; the GUI never duplicates authentication, enrollment, or serialization.


```text
main.py       -> CLIUniApp -> CLIView -> StudentController / AdminController
                                    -> StudentService / AdminService
                                    -> Student / Subject / Admin + Validator / IDGenerator
                                    -> StudentDataFile / AdminDataFile -> Database -> data/*.data

gui_main.py   -> GUIUniApp -> Tkinter Views -> StudentController
                                         -> same StudentService and StudentDataFile
```

The arrows show logical calls, not import directions; keep dependencies one-way where practical and avoid circular imports. Pass collaborators using constructors where simple (e.g., `StudentService(student_data_file, validator, id_generator)`).

**Required import paths** (examples; add imports only when you need them):

```python
from models.student import Student
from models.subject import Subject
from models.file_handlers.database import Database
from models.file_handlers.student_data_file import StudentDataFile
from models.file_handlers.admin_data_file import AdminDataFile
from helpers.validator import Validator
from helpers.id_generator import IDGenerator
```

Run entry points from the project root (`python3 main.py`, `python3 gui_main.py`) to keep imports predictable. File handlers must still resolve data paths correctly when the program is launched from another working directory.


---

## 4. Model behavior and data contract

### 4.1 `Subject` (`models/subject.py`)

From UML: fields `subject_id: str`, `mark: int`, `grade: str`; methods `calculate_grade()` and `get_pass_fail_status()`.

- ID: **three-digit string**, from `"001"` through `"999"`.
- Mark: **integer 25–100 inclusive**.
- Grade thresholds:

| Mark | Grade |
|---|---|
| 25–49 | `Z` |
| 50–64 | `P` |
| 65–74 | `C` |
| 75–84 | `D` |
| 85–100 | `HD` |

- Subject status: `FAIL` if mark <50, otherwise `PASS`.
- Grade calculation must be deterministic and test boundary values: 49/50, 64/65, 74/75, 84/85.
- Never generate a fresh random mark while **loading** a saved Subject.

### 4.2 `Student` (`models/student.py`)

From UML: `student_id: str`, `name: str`, `email: str`, `password: str`, `subjects: list[Subject]`. Preserve the conceptual credential field; choose safe persistence representation before saving. UML operations: `can_enroll()`, `add_subject(subject)`, `remove_subject(subject_id)`, `change_password(new_password)`.

- Student ID: **six-digit string `"000001"`–`"999999"`**, unique across registered students; preserve leading zeros.
- Student has 0–4 subjects, including after reloading JSON.
- Enrollment rejects a fifth subject and duplicate subject IDs on the same student's list.
- Removal uses the requested subject ID, not a list index; removing a nonexistent subject is a handled error.
- Name is required at registration.
- Compute `average_mark` from enrolled subject marks and **recalculate after every add/remove**; avoid division by zero when none are enrolled.
- Admin grouping uses the **overall grade derived from the average**. PASS/FAIL is based on the student's overall average, not each individual subject.
- **Partial-enrollment interpretation to document:** because the official brief mentions a four-subject average yet requests ongoing averages, use the current enrolled-subject average for displays; establish and test the agreed PASS/FAIL policy for 1–3 subjects. With no subjects, do not invent a numeric average or grade (represent as not yet graded).

### 4.3 `Admin` (`models/admin.py`)

From UML: `admin_id`, `name`, `email`, `password`; `change_password(new_password)`. Admins are predefined; there is **no admin registration workflow**. Store and verify admin credentials via `admins.data`.

### 4.4 `Validator` (`helpers/validator.py`)

UML methods: `is_valid_email(email)`, `is_valid_password(password)`, `is_not_empty(value)`.

- Email must end with **`@university.com`** and contain a valid nonempty local portion. Suggested basic pattern: `^[A-Za-z0-9._%+-]+@university\.com$` (validate against the assignment examples and agreed team policy).
- Password must have **at least five letters total, starting with an uppercase letter, followed by at least three digits**. Suggested strict pattern: `^[A-Z][A-Za-z]{4,}[0-9]{3,}$`.
- Regex validation applies to both student registration and student login inputs; validate admin inputs in a consistent, documented way.
- Return helpful errors at the controller/view boundary; do not print directly from Validator.
- Change-password flow checks pattern **and** password confirmation in the UI. The sample permits reusing the same password.

### 4.5 `IDGenerator` (`helpers/id_generator.py`)

UML methods: `generate_student_id(existing_ids)`, `generate_subject_id(existing_ids)`, `generate_mark()`.

- Use zero-padded IDs with `f"{value:06d}"` and `f"{value:03d}"`.
- Generate student ID from 1–999999 and subject ID from 1–999.
- Check collisions against the relevant existing IDs and **handle exhausted ID space** (never loop forever).
- Random marks are integers from 25 to 100 inclusive.
- **Subject-ID uniqueness scope is not fully specified by the available documents.** At minimum, ensure an ID is unique within its student's enrollment list; discuss global uniqueness with the group before enforcing it globally.

---

## 5. Storage and JSON design

### Proposed file format

`data/students.data`:

```json
{
  "students": [
    {
      "student_id": "002340",
      "name": "Jane Smith",
      "email": "jane.smith@university.com",
      "password_hash": "<generated-password-hash>",
      "subjects": [
        { "subject_id": "001", "mark": 85, "grade": "HD" }
      ]
    }
  ]
}
```

`data/admins.data`:

```json
{
  "admins": [
    {
      "admin_id": "001",
      "name": "University Admin",
      "email": "admin@university.com",
      "password_hash": "<generated-password-hash>"
    }
  ]
}
```

These are **schema examples, not usable seeded credentials**. A password hash must be calculated from an actual password using an appropriate password-hashing method; do not copy the placeholder literally and expect login to work. Never commit real secrets. Where a simple teaching implementation stores `password` instead, explicitly note the security tradeoff and keep credential serialization/authentication consistent between CLI and GUI.

### `Database` (`models/file_handlers/database.py`)

Minimum responsibilities from Part 2 §3:

- Ensure the data directory and file exist before use.
- Initialize newly created files with valid JSON containing the appropriate empty collection.
- Read, validate, and write JSON, with clear errors for corrupt/unreadable data.
- Prefer safe replace-on-save (temporary file then replace) so interrupted writes do not silently destroy data.
- Provide a clear operation when requested, limited to the proper collection.
- Determine paths relative to the project root using `pathlib.Path(__file__).resolve().parents[2]` when called from `models/file_handlers/`, **not** the caller's working directory. Prefer passing an explicit path to `Database` so tests can use temporary files.

### `StudentDataFile` (`models/file_handlers/student_data_file.py`)

Reflect UML operations:

- `load_students() -> list[Student]`
- `save_students(students) -> None`
- `add_student(student) -> None`
- `find_student_by_email(email) -> Student | None`
- `find_student_by_id(student_id) -> Student | None`
- `email_exists(email) -> bool`
- `remove_student(student_id) -> bool`
- `clear_all_students() -> None`

Serialization should reconstruct real Student and Subject objects with the same IDs/marks/grades, **not** generate new IDs or marks on load. Confirm that updating a student's subjects or password persists immediately and survives application restart. Normalizing email for lookup is recommended; ensure duplicate checking uses the same normalization.

### `AdminDataFile` (`models/file_handlers/admin_data_file.py`)

Reflect UML operations:

- `load_admins() -> list[Admin]`
- `find_admin_by_email(email) -> Admin | None`
- `save_admins(admins) -> None`

One or more **predefined** admin accounts can be initialized through an explicit setup step documented in `README.md`; no end-user admin-registration screen. The admin's `clear students` action must **never delete `admins.data`**.

---

## 6. Business operations and MVC actions

### `StudentService` (`models/student_service.py`)

Preserve UML methods and behavior:

- `register_student(name, email, password) -> Student`: validate inputs, reject duplicate email, generate unique ID, create Student, persist.
- `login_student(email, password) -> Student | None`: validate input, load existing record, verify credentials; errors must not expose stored passwords.
- `enroll_in_subject(student) -> bool`: enforce four-subject maximum; generate unique subject ID and 25–100 mark; calculate grade, add subject, persist, update average.
- `remove_subject(student, subject_id) -> bool`: remove only from the logged-in student, save, update average.
- `view_current_subjects(student) -> list[Subject]`: return only that student's enrolled subjects.
- `change_password(student, new_password) -> None`: validate and persist; input confirmation is handled by View/Controller.

### `AdminService` (`models/admin_service.py`)

Preserve UML's `login_admin`, `view_all_registered_students`, `view_students_by_grade`, `categorize_students_pass_fail`, `remove_individual_student`, `clear_student_database`, `change_password`.

- Authenticate an **existing admin** from `admins.data` before granting access to management actions (group-selected extension).
- Show all student records without disclosing password fields.
- Group students using overall grades derived from their average marks; handle students with no subjects.
- Partition students by overall PASS/FAIL from their average marks; avoid stale cached status.
- Remove one student by the entered **six-digit student ID**; report unknown IDs.
- Clear student records **only after explicit Y/N confirmation**; keep admin accounts intact.
- Follow successful modifications by writing to `students.data`.

### Controllers and Views

- `CLIUniApp` owns top-level CLI navigation and authenticated session flows; `StudentController` and `AdminController` process feature actions.
- `CLIView` handles **all** terminal input/output and produces text close to the sample I/O.
- `GUIUniApp` controls Tkinter navigation, calls the **same StudentController/StudentService**, and never keeps a separate student database.
- Use explicit success/error results or well-defined exceptions to communicate failure from Model to Controller to View. No broad `except Exception: pass` and no silent recovery from corrupt files.

---

## 7. Required CLI flows (match official sample I/O)

1. **University menu:** `(A) Admin`, `(S) Student`, `(X) Exit`.
2. **Student menu:** `(l) login`, `(r) register`, `(x) exit`.
3. **Student course/enrollment menu** (after successful student login): `(c) change password`, `(e) enroll`, `(r) remove`, `(s) show`, `(x) exit`.
4. **Admin authentication gate** (group decision): ask for admin email and password **before** presenting the admin operations menu.
5. **Admin operations menu:** `(c) clear database`, `(g) group students`, `(p) partition students`, `(r) remove student`, `(s) show`, `(x) exit`.

**Output fidelity:** Use the screenshot examples in official brief pp. 3–7 as the reference for wording, capitalization, prompts, status messages, and indentation. For example, the brief uses `Student System (l/r/x):`, `Student Course Menu (c/e/r/s/x):`, and `Admin System (c/g/p/r/s/x):`. The admin login screen is an approved **extension**, so its exact wording is not part of the original admin sample. Keep the rest comparable.

User-story coverage:

| Backlog IDs | Feature |
|---|---|
| 100–105 | Student registration, validation, unique ID, error feedback |
| 200–203 | Student login and access |
| 204–207 | Admin login and access (group-added requirement) |
| 300–306 | Add subject, enforce limit, generate mark/grade, save |
| 307–310 | Remove subject and persist |
| 311–312 | Show **own** enrolled subjects |
| 400–403 | Admin view all and group by grade |
| 404–405 | Admin PASS/FAIL categorization |
| 406–407 | Admin remove student |
| 408–409 | Admin clear student database |
| 500–503 | Student password validation and change |

---

## 8. Tkinter GUI specification

Only build the GUI **after** CLI functionality, persistence, and primary tests pass.

The official assessment Part 2 §5 and rubric §6(e) require **at least four windows/presentations**:

1. **Login window** (`login_view.py`): student email and password inputs; validate missing fields, email format, incorrect credentials; read the registered student from `students.data`.
2. **Enrollment window** (`enrollment_view.py`): enroll student, display count/status, block fifth subject, persist each enrollment.
3. **Subject window** (`subject_view.py`): list current student's subject IDs, marks, and grades.
4. **Exception/error window** (`error_view.py`): show clear errors for invalid login and enrollment overflow, including appropriate modal feedback.

Implementation notes:

- One `tk.Tk()` root and one `mainloop()`; use `Toplevel` or clearly separated frames/dialogs as appropriate to the rubric's four-window requirement.
- Keep Tkinter widgets in Views, callback wiring/session flow in `GUIUniApp`, and enrollment rules in the same Model code already used by CLI.
- GUI **must not** register students or show admin functionality.
- After CLI registration, terminate/restart either interface and verify the exact same account can log into the GUI.
- Keep GUI error behavior accessible and informative rather than crashing.

---

## 9. Implementation milestones (one at a time)

**The milestone order is a delivery plan, not permission to implement everything at once.** Every milestone must finish with a working test before continuing.

### M0 — Inspect and establish baseline

- Read this file, the sources, and the existing repository.
- Confirm the user mode (`GUIDED` unless overridden).
- Check Python version and whether Tkinter imports on the target machine; no external packages should be necessary for initial CLI development.
- Verify the planned file tree and current code without overwriting files.
- List conflicts and the fixed decisions from Section 2.
- **Pass:** Can explain which code exists, what does not, and the next small task.

### M1 — Scaffold project and CLI navigation

- Create project/package directories, README, `.gitignore`, `main.py`, `controllers/cli_uni_app.py`, `views/cli_view.py`.
- Implement terminal menus and simple, testable menu transitions; feature handlers may initially be placeholders.
- Keep printing and `input()` in `CLIView`; controller handles choices.
- **Pass:** Admin/Student menus reachable, invalid choices handled, back/exit works without traceback.

### M2 — Domain models

- Implement `Subject` first, then `Student`, then `Admin`, using the UML field/method names.
- Add pure grade calculations, student enrollment invariants, overall average handling, remove behavior, and domain-level tests.
- **Pass:** Grade boundary tests pass, fifth subject is rejected, removing a subject updates average, empty subject list is safe.

### M3 — Helpers

- Implement email/password regex validation and empty checks.
- Implement ID generation, collision checks, and random marks.
- **Pass:** Invalid credentials rejected, valid examples accepted, IDs zero-padded, ID collision controlled, marks in range.

### M4 — Persistence

- Implement `Database`, `StudentDataFile`, and `AdminDataFile`.
- Set a consistent JSON schema and credential-storage approach; implement serialization/deserialization.
- Preconfigure admin account(s) using an explicitly documented setup step.
- **Pass:** Fresh file created if missing; save/load roundtrip preserves students/subjects; corrupt data reports an error; clearing students does not erase admins.

### M5 — Student registration and authentication

- Implement `StudentService.register_student()` and `login_student()`.
- Connect student controller and CLI registration/login workflow.
- **Pass:** New account saved, duplicate email blocked, invalid patterns rejected, successful login reads disk, incorrect password does not grant access.

### M6 — Student enrollment and account management

- Implement enroll/show/remove/change password, persistence, averages, and all student-course CLI actions.
- Follow official examples for interactive prompts, grade boundaries, four-subject overflow, password confirmation, and errors.
- **Pass:** Subject count never exceeds four; remove-by-ID persists; CLI restart retains state; changed credentials are enforced.

### M7 — Admin authentication and management

- Implement `AdminService` and admin controller/login gate.
- Implement show/group/partition/remove/clear with careful confirmations and file persistence.
- **Pass:** Unauthorized admin cannot manage students; grouping and partitioning use average mark; removing one student leaves others; clearing students leaves admin login usable.

### M8 — CLI acceptance test and sample-I/O alignment

- Exercise all user-story groups 100–503.
- Compare prompt text, navigation, and error behavior with the official screenshot samples.
- Confirm file-state changes after each operation and test application restart.
- **Pass:** No known CLI rubric feature missing, and deviations from sample I/O are documented.

### M9 — GUI implementation

- Implement GUI controller/entry point and four required Tkinter Views.
- Connect the same StudentController/StudentService and shared `students.data`.
- **Pass:** CLI-registered student logs into GUI, enrolls, sees subjects, and receives proper errors; no admin GUI.

### M10 — Integration, packaging, and showcase preparation

- Run automated tests and manual CLI/GUI smoke tests, verify file paths from different working directories.
- Document Python version, CLI and GUI run commands, admin setup instructions, JSON files, group contribution ownership, and any deviations from official sample.
- Package one integrated project ZIP. Official filename convention: `group<group-number>-Cmp1<lab-number>.zip` (insert actual values).
- Prepare each member to explain their part, run a complete demo, and answer code/design questions.
- **Pass:** Both apps run independently, use common data, tests pass, submitted ZIP structure is correct, and each student can explain their contribution.

---

## 10. Tests and acceptance checklist

Use Python's built-in `unittest` unless the group consciously chooses an alternative. Keep automated tests isolated from the real `data/` files by using temporary directories/fixtures; never clear a student's real working data during tests.

Recommended commands (from the project root):

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m tkinter              # Check local Tkinter availability
python3 gui_main.py             # Only after M9 exists
```

**Required test scenarios** (map each to a relevant test or manual check):

- Register valid student with correctly formatted email/password and name.
- Reject invalid email, invalid password, empty name, and duplicate email.
- Generate unique six-digit student IDs with preserved leading zeros.
- Log in correct student; reject unknown student or incorrect password.
- Deny admin access with wrong credentials; permit preconfigured admin.
- Enroll subjects with distinct three-digit IDs and valid random marks.
- Verify grade thresholds at 49/50, 64/65, 74/75, and 84/85.
- Allow exactly four enrolled subjects and reject a fifth.
- Show only the signed-in student's subjects and no credentials.
- Remove an existing subject by ID and reject a nonexistent ID.
- Recalculate overall average and grade after enroll/remove, including no-subject case.
- Validate/confirm new password and verify it persists on login.
- Show all students without exposing stored passwords.
- Group admin results by overall grade; partition PASS/FAIL by average mark.
- Delete one student by six-digit ID while preserving others.
- Require confirmation before clear; clearing students must not delete admins.
- Confirm `students.data` survives exiting/restarting the CLI.
- Confirm registered CLI credentials work unchanged in GUI.
- GUI handles empty/incorrect login and fifth-subject attempt with error UI.
- GUI subject window shows correct IDs, marks, and grades.
- Opening a missing data file initializes safe valid JSON; corrupt JSON does not silently erase records.

Do not use random real-time values as hardcoded expected outputs in tests. Inject or mock random generation where deterministic assertions are required.

---

## 11. Packaging and evaluation notes

From official Part 2 & 3 brief:

- **Part 2:** 50/70 marks — University System **4**, Student System **9**, Subject Enrollment **15**, Admin System **15**, GUIUniApp **7**.
- **Part 3 showcase:** 5/70 marks; includes integrated working demo, clear speaking, code walkthrough, and correct answers.
- **Group assessment:** one ZIP per group; **individual** contributions and demonstration are assessed. Group members must attend the compulsory showcase.
- **Due:** Sunday of Week 13; check Canvas for the exact time.
- Integration is essential: the brief warns of penalties when code cannot be integrated.
- The brief **prohibits submitting AI-generated code** (see Section 7 of the brief).

The presence of these notes in this instruction file does not prove academic compliance. The student/team must follow the actual assessment rules and be able to explain the submitted work.

---

## 12. Suggested prompt to reuse with any AI assistant

Copy this after attaching or linking `implement_guide.md` and, preferably, the UML, backlog, and official assessment brief:

> Read `implement_guide.md` fully and follow its fixed architecture and decisions. Use `MODE=GUIDED`. Inspect the current source files before advising. I want to implement UniApp myself: teach me **one step at a time**, beginning at the earliest incomplete milestone. For each step, tell me the exact file, class, method signatures, logic to write, commands to run, tests to perform, and criteria for completion. Do not modify project files or move to the next step until I share my code or results. Keep both login flows, separate JSON `.data` files, `models/file_handlers/`, MVC + Helpers, and CLI before GUI. Distinguish official requirements from our team extensions.

For a reference prototype **not intended for direct submission**, substitute `MODE=IMPLEMENT` and ask the assistant to make **only one milestone's changes** and run its tests before continuing.

---

## 13. Questions to resolve only when they become implementation blockers

Do not repeatedly ask these questions if the team's choice is already recorded elsewhere:

1. **Overall PASS/FAIL for students with fewer than four subjects:** Use current average (proposed), or show pending until four? The documents specify both a four-subject pass rule and recalculation after every enrollment.
2. **Subject-ID uniqueness:** Per student (proposed minimum) or globally across students?
3. **Credential serialization:** Use salted hashes (recommended) or a simpler specified representation? Maintain compatibility with course expectations and consistency across CLI and GUI.
4. **Initial admin provisioning:** Choose a documented, reproducible setup method. Do not put real passwords in version control.
5. **Exact CLI wording:** Inspect Part 2 pp. 3–7 sample screenshots before final polishing.

When a question has a reasonable working default and does not block the active milestone, note it briefly and continue. **Do not change fixed decisions from Section 2 without the user's explicit instruction.**

---

## 14. Change-control rules for future sessions

- Treat the directory tree in Section 3 as frozen. Do not reintroduce `storage/`, `services/`, or `persistence/` without explicit approval.
- All database-related imports must start with `models.file_handlers`.
- If the user asks for a new feature, map it to an existing class and folder before proposing a new module.
- Do not replace `admins.data` with credentials in `students.data` without explicit approval.
- Do not remove student or admin authentication. Keep GUI student-only.
- If any earlier AI advice conflicts with this guide, use this guide's latest structure and flag the conflict.

---

## 15. First instruction when this file is handed to an AI

**Start at M0.** Inspect the existing repository, identify what has already been implemented, and then give the user **only the first incomplete concrete task**. In `GUIDED` mode, instruct the user without writing source files. In `IMPLEMENT` mode, create or modify only what is required for the approved milestone, test it, and report the results before continuing.
