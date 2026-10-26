# UniApp project progress

Updated: 26 October 2026

## Completed

- CLI student flow: register, log in, enroll in up to four subjects, remove subjects, view subjects, and change password.
- Student data is saved in `data/students.data` through `StudentDataFile`.
- GUI welcome, student login, and student registration screens are connected.
- Registration validates the student email and password, rejects duplicate emails, and returns to the login screen after success.

## Still to do

1. Add a GUI student screen after login. Login currently shows a success message but stays on the login screen.
2. Connect GUI subject enrollment, subject list/removal, password change, and logout to `StudentService`.
3. Implement admin features. The GUI Admin button is disabled, and the CLI admin option shows a placeholder message.
4. Add tests for student service, file storage, and GUI controller behavior.

## Current checks and limits

- `python3 -m unittest discover -s tests -q`: 12 tests run; 10 pass, 1 fails, and 1 errors. `test_student.py` expects `Student.average_mark()` and a `"PENDING"` status, but the current `Student` class has a different interface.
- Passwords are currently saved as plain text in the student data file. Use test passwords only until storage is secured.
- GUI layout still needs a visual check on macOS.

## Run the app

```bash
python3 main.py      # CLI
python3 gui_main.py  # GUI
```
