**Student GUI review and Ponytail simplification guide**

Reviewed: 26 October 2026, Australia/Sydney. Scope: the current working tree, including existing uncommitted and untracked student GUI work. This is a review and future implementation guide. No application code, tests, or saved student records were changed.

**Implementation update — 26 October 2026**

After the original review, the user authorized GUI simplification and deferred storage/security changes. Findings 7–13 have now been implemented: shared auth-field construction, shorter dashboard/account/sidebar rendering, simpler controller error handling, required subject callbacks, and removal of unused methods. Existing styles, spacing, custom dialogs, validation, confirmations, and service contracts were retained. The original review below remains a historical snapshot; its line references are from before this implementation.

- Eight GUI source files changed, with a net reduction of 93 lines compared with the user's working tree before this pass.
- Added `tests/test_student_gui.py`: nine regression tests. Together with the two existing confirmation tests, all 11 focused GUI tests pass.
- Compared 15 real Tk screen states before and after: widget trees, geometry, labels, styles, and masking were identical. The comparison used temporary baseline source copies and fictional in-memory students; no saved records were changed.
- Full suite: 23 tests, 21 passed, one failure and one error from the same two outdated Student tests. Those existing tests were not modified.
- Native dialog interaction and full manual end-to-end usage were not checked. Storage/security repairs, password-help changes, optional native-dialog replacement, and spacer cleanup were left out of this pass.

**What this repo does:** UniApp is a local university application with CLI and Tkinter interfaces sharing student services and JSON storage. The student GUI now supports registration, login, a dashboard, enrollment/removal, account information, password changes, and logout. This review assumes one person using one application process with a small local dataset; simultaneous CLI/GUI writers are outside that operating assumption.

**Overall assessment:** The student GUI has its main workflows implemented and connected. It needs storage fixes, reliable regression tests, and a real visual/interaction check before being described as fully verified. Its architecture is already reasonably small: simplify repeated widget construction and dead branches without replacing the design.

**Evidence and limits**

All current student GUI views, both GUI controllers, both entry points, the student service/models/storage/utilities, and existing tests were read. Shared CLI student callers were also traced. Existing progress/refactor documents and relevant architecture guidance were checked against the source. No dependency or build manifest was found; the reviewed runtime uses the Python standard library and Tkinter.

| Check | Current result |
| --- | --- |
| Python syntax | All 51 Python files parsed successfully. |
| Existing test suite | 14 tests: 12 passed, 1 failed, 1 errored. Both unsuccessful tests use an old Student interface. |
| Isolated real service/storage checks | Registration, login, enrollment through four subjects, fifth-subject rejection, removal, password changes, reload, and failed-save handling passed the exercised cases. All records were in temporary directories. |
| GUI controller checks with mocked views | Routing, callback wiring, login state, password confirmation, logout, and ValueError/OSError handling passed the exercised cases. |
| Grading checks | Boundaries at 49/50, 64/65, 74/75, 84/85, and 100 passed; empty overall result was also checked. |
| Storage defects | Reproduced missing-schema KeyError and destructive failed-write behavior using temporary files. |
| Actual Tk widgets | Not opened or clicked during this review. Geometry, focus, clipping, native theme behavior, and modal interaction remain unverified. |

The temporary checks were executed for this audit; they were not added to the repository test suite. Mocked views prove controller behavior, not rendered GUI correctness. Existing student records were inspected only for structure; credentials are not reproduced here.

**Implemented component inventory**

| Component and source | Implemented behavior | Review decision |
| --- | --- | --- |
| `gui_main.py:10–31` | One Tk root and mainloop; centered 1000 × 700 fixed window; constructs storage, service, and GUI app. | Keep this wiring. Check the fixed dimensions visually before changing layout. |
| `controllers/gui/gui_uni_app.py:6–36` | Owns the current root screen and shared dialogs; constructs the student controller; shows Welcome; destroys the previous root frame on transitions. | Keep. It already has a clear, limited job. |
| `views/gui/base_gui_view.py:4–10` | Shared Frame superclass for Welcome/Login/Registration; includes an unused child-clearing method. | Keep the established base class; remove the unused method if it remains unreferenced. Reuse this class for a small auth-field helper if implementing the form simplification below. |
| `views/gui/welcome_view.py:6–57` | Welcome title, Student action, disabled Admin action. Uses native ttk buttons. | Keep behavior and disabled Admin button. The earlier Canvas pill-button implementation is no longer present. |
| `views/gui/gui_student/login_view.py:6–92` | Email and masked password fields; Login/Register/Back callbacks. | Functional wiring exists. Simplify shared form construction without merging this screen with Registration. |
| `views/gui/gui_student/registration_view.py:6–94` | Name, email, masked password; Register/Back; delegates validation and saving. | Registration has no confirmation-password field today. Preserve that contract in a refactor; adding one is a separate feature. |
| `controllers/gui/gui_student_controller.py:9–174` | Owns active student, student screens, service calls, success/error callbacks, and logout. | Keep the role controller. Remove one dead result check and make service error handling consistent. |
| `views/gui/gui_student/student_main_view.py:3–97` | Header, sidebar, content area, Dashboard/Subjects/Account/Logout; destroys previous content when switching. | Keep the shell and its separate content lifecycle. Loop over the three identical navigation buttons; delete unused placeholder rendering. |
| `views/gui/gui_student/dashboard_view.py:4–132` | Four subject slots in two rows; occupied slots show mark/grade; empty slots show N/A; overall average/status/grade. | Share the duplicated card shell. Preserve four slots, card dimensions, grades, and two-decimal average formatting. |
| `views/gui/gui_student/subjects_view.py:4–105` | Count, four-subject limit hint, enrollment button, empty state, subject rows, selected-subject removal. Both mutations require confirmation. | Keep both confirmations and captured subject IDs. Optional callbacks can become required because the sole application caller always supplies both. |
| `views/gui/gui_student/account_view.py:3–108` | Name/ID/email display; masked current/new/confirmation password fields; password submission. | Reduce repeated widgets locally. Keep explicit field names and submission order. |
| `views/gui/error_view.py:4–39` | Custom centered error/success Toplevel, message wrapping, modal grab, focused OK button, waits until closed. | Keep custom appearance by default. Native dialogs are an optional visible change, not a silent cleanup. |
| `models/student_service.py:13–195` | Validation, credential checking, enrollment/removal/password persistence; refreshes the active object only after save succeeds. | Preserve service APIs and save-before-session-update ordering. Fix misleading password instructions. |
| `models/student.py:5–86`, `models/subject.py:1–22` | Student enrollment limit/duplicates, subject marks/grades, overall results, in-memory removal/password update. | Keep current contracts. Do not restore obsolete APIs merely to satisfy outdated tests. |
| `models/file_handlers/student_data_file.py:7–125`, `database.py:5–39` | Maps records to models, searches/adds/updates students, reads/writes JSON. | Shared GUI dependency with important reliability defects; repair separately from view simplification. |
| `utils/validator.py`, `utils/id_generator.py` | Input rules, unique student/subject IDs, generated marks. | Reuse these. Do not copy rules into views or replace bounded collision handling as a cosmetic cleanup. |

The empty GUI Admin package and disabled Admin button do not constitute an implemented Admin system. Deleted `enrollment_view.py` and `subject_view.py` are not current student screens; `SubjectsView` is the active combined screen.

**Current workflow and contracts to preserve**

```text
Welcome → Student Login ↔ Registration
                 │ valid login
                 ▼
          StudentMainView
          ├── Dashboard
          ├── Subjects → confirm → enroll/remove → save → refresh → success
          ├── Account  → validate → change password → save → refresh → success
          └── Logout → clear active student → fresh Login
```

Login Back returns to Welcome. Registration Back returns to Login. Successful registration saves the new student, returns to Login, and displays the generated student ID; it does not automatically log in. Successful login opens the shell and Dashboard without a success popup. Logout destroys the old root screen through the normal transition and creates new blank login entries.

| Boundary | Contract |
| --- | --- |
| Login view → controller | `login(email, password)` |
| Registration view → controller | `register(name, email, password)` |
| Subjects view → controller | `enroll_subject()` and `remove_subject(subject_id)` after confirmation |
| Account view → controller | `change_password(current_password, new_password, confirm_password)` |
| Controller → service password change | `change_password(student, current_password, new_password)`; confirmation stays in the controller |
| Service registration/login | Registration returns Student or raises; login returns Student or None and can raise storage errors |
| Service enrollment/removal | Enrollment returns Subject; removal returns True on success and raises ValueError on a missing subject or failed save |
| Overall results | `(average, status, grade)`; no subjects gives `(None, "N/A", "N/A")` |
| Data mutation | Load the saved student → validate/mutate that copy → save → synchronize the logged-in object |

Passwords must not be stripped or otherwise silently normalized. Email/name trimming stays in the service. IDs retain their leading zeros. The GUI displays generated subjects; it does not currently offer a subject catalogue or selection form.

**Must fix — reliability defects**

1. **A failed write can erase all saved students.** `models/file_handlers/database.py:22–26,37–39`.
   - **What this is:** Every student mutation ultimately rewrites the JSON database.
   - **Problem:** Opening the live file with `"w"` truncates it before serialization finishes. A simulated write failure left zero bytes; constructing storage again then replaced that empty file with an empty student list.
   - **Fix:** Write to a temporary file in the same directory, close it successfully, then replace the live file atomically; remove an abandoned temporary file on failure. Initialize missing files, but report an existing empty/corrupt student file rather than silently resetting it.
   - **If we skip it:** The GUI can show a save error after the original records have already been lost. Test both failure before replacement and successful reload; keep the original bytes unchanged on failure.

2. **Some corrupt records bypass the GUI's error display.** `models/file_handlers/student_data_file.py:15–39`; `models/file_handlers/database.py:28–35`.
   - **What this is:** The loader trusts record keys and values after only checking that the top-level JSON is a dictionary.
   - **Problem:** A valid JSON file containing `{}` raises KeyError during login. Other malformed shapes/types can raise TypeError; the GUI catches ValueError and OSError, so these errors escape the action handler.
   - **Fix:** Validate required record structure and types at the loader boundary and raise a clear ValueError for invalid stored data. Preserve the file and avoid a broad `except Exception` in each GUI action; do not introduce stricter legacy-ID formats as part of this repair.
   - **If we skip it:** Login or another action can fail with a Tk callback traceback instead of a useful dialog. Test missing keys, wrong collections, invalid subject values, and invalid JSON without resetting data.

**Should fix — correctness guidance, tests, and useful simplification**

3. **Password instructions omit rules the validator enforces.** `models/student_service.py:30–36,172–179`; `utils/validator.py:29–49`.
   - **What this is:** Registration and password-change errors explain password requirements.
   - **Problem:** `Password!` satisfies the displayed length/case/symbol list but is rejected because it has no digit. The messages also omit the no-whitespace rule.
   - **Fix:** Use one shared requirements string in the service for both messages, listing length, upper/lowercase, digit, symbol, and no whitespace. Use normal adjacent strings inside parentheses instead of backslash continuations.
   - **If we skip it:** Users can follow every displayed instruction and still fail. Keep Validator as the rule implementation; do not weaken it to match the message.

4. **Two Student tests expect a removed interface.** `tests/test_student.py:37–56`.
   - **What this is:** These tests cover average and overall status.
   - **Problem:** They call nonexistent `average_mark()` and expect `"PENDING"`/`"PASS"` strings instead of the tuple used by both GUI and CLI.
   - **Fix:** Assert the current tuple before/after removal and for empty, failing, and passing students. Keep grade-boundary assertions meaningful; do not add a compatibility method solely for these tests.
   - **If we skip it:** The suite remains red and cannot give a clean baseline for subsequent changes.

5. **Important GUI/service behavior has no lasting regression coverage.** `tests/test_student_service.py` and `tests/test_database.py` are empty; there is no GUI controller test module.
   - **What this is:** The existing GUI tests only exercise the two confirmation methods using a simple fake view.
   - **Problem:** They do not catch a wrong row callback, broken session transition, incorrect service arguments, or a save failure that alters session data. The audit's temporary checks will not run with the repository suite.
   - **Fix:** Add small unittest tests for the service/storage boundaries and controller contracts listed below, using temporary data and mocked dialogs. Add a focused test for subject-row callback capture when modifying that construction.
   - **If we skip it:** A shorter implementation could pass the current GUI tests while losing a working action. Avoid screenshot baselines and tests that merely count widgets.

6. **Older guidance would overwrite working features.** `project_progress.md:11–16`; `gui_student_controller_refactor.md:63–130`; `.docs/project_progress.md` student GUI section.
   - **What this is:** The project contains multiple snapshots and a previous replacement-controller proposal.
   - **Problem:** The root progress file says the authenticated screen is still missing, and the older proposed controller stops at login success. Applying that proposal wholesale would remove current dashboard/subjects/account/logout behavior.
   - **Fix:** Use this review and the live code for the next change. Later mark the old replacement guide as historical and update the progress documents from verified results; preserve the present root-frame navigation rather than implementing obsolete Toplevel plans.
   - **If we skip it:** Future work can accidentally reverse completed functionality. The older guidance is useful history, not an executable current plan.

7. **Dashboard creates the same card structure in both branches.** `views/gui/gui_student/dashboard_view.py:28–88`.
   - **What this is:** Each occupied or empty slot creates a LabelFrame and inner content Frame.
   - **Problem:** Common style, padding, and construction appear twice, so one layout change must be repeated and can drift between empty/filled slots.
   - **Fix:** Choose the slot's subject/title first, create one card and content container, then branch only for the labels inside. Keep the two-row loop and existing card geometry in this pass; use the existing statistics loop unchanged.
   - **If we skip it:** The code remains harder to maintain, though the current branch structure is not itself a runtime defect. Check 0, 1, 3, and 4 subjects after refactoring.

8. **Login and Registration duplicate the same field construction.** `login_view.py:10–13,32–61`; `registration_view.py:10–13,29–71`, under `views/gui/gui_student/`.
   - **What this is:** Five fields repeat the same label/entry font, style, and packing pattern across two screens.
   - **Problem:** Adjusting the shared auth-field appearance requires editing multiple copies; both screens also configure the same padded-entry style.
   - **Fix:** Reuse BaseGUIView for one small auth-specific field method that takes the parent, label text, and whether to mask input, and returns the Entry. Share the identical auth styles; keep screen-specific spacing and callbacks in each view, and keep styles available when constructing either view directly.
   - **If we skip it:** The duplication remains easy to understand but costly to update consistently. Do not introduce a form schema, widget factory, extra base controller, or generic style manager.

9. **Account repeats profile rows and password-field markup.** `views/gui/gui_student/account_view.py:29–90`.
   - **What this is:** Three profile labels and three similar password-entry groups.
   - **Problem:** The same presentation is repeated even though only the text and final spacing differ.
   - **Fix:** Build profile labels from three explicit `(label, value)` pairs. Build password entries in an ordered local loop, then assign them explicitly to `self.current_password`, `self.new_password`, and `self.confirm_password`; preserve the final field's extra spacing and the existing submit method.
   - **If we skip it:** Appearance changes must be repeated. Avoid dynamic `setattr`, a field registry, or moving Account's different styling into the auth helper just to force reuse.

10. **Sidebar buttons repeat identical construction.** `views/gui/gui_student/student_main_view.py:50–69`.
   - **What this is:** Dashboard, Subjects, and Account share the same style and packing options.
   - **Problem:** Each presentation change must be made three times.
   - **Fix:** Loop over three explicit `(label, callback)` pairs and pass each callback directly as `command`. Keep Logout separate because it is packed at the bottom.
   - **If we skip it:** This is only maintenance duplication, not a defect. Do not wrap callbacks in a lambda that captures the loop variable.

11. **Removal checks a service result that cannot occur.** `controllers/gui/gui_student_controller.py:128–143`; `models/student_service.py:127–151`.
   - **What this is:** The controller handles both a False result and an exception for a missing subject.
   - **Problem:** The current service raises for failure and returns True only on success, making `if removed is False` unreachable with the real implementation.
   - **Fix:** Call the service without storing its return value, catch ValueError/OSError and return, then refresh/show success. Apply that same narrow service-call try block to login and password change so rendering failures are not presented as service failures.
   - **If we skip it:** The extra branch misstates the contract. Preserve the service's public return value and the CLI caller; do not change the model's different `remove_subject()` False-on-missing contract.

12. **Subjects supports callback-free modes no application caller uses.** `views/gui/gui_student/subjects_view.py:5,49,88,91–105`.
   - **What this is:** Both mutation callbacks default to None and are guarded repeatedly.
   - **Problem:** The only application constructor call, `GUIStudentController.show_subjects()`, always supplies both. The extra disabled/read-only mode adds branches with no current feature using it.
   - **Fix:** Require both callback arguments, retain both confirmations, remove only callback-presence checks, and use `student.can_enroll()` for the enrollment button's enabled state. Preserve the service-side enrollment check because saved data is authoritative.
   - **If we skip it:** The extra mode remains harmless but unnecessary. Keep `lambda sid=subject.subject_id: ...` on Remove buttons so each button uses its own row ID.

13. **Two view methods have no callers.** `views/gui/gui_student/student_main_view.py:94–97`; `views/gui/base_gui_view.py:8–10`.
   - **What this is:** `show_placeholder()` renders a temporary screen; `clear()` destroys child widgets.
   - **Problem:** Searches across source, tests, and documents found no calls to either. Real pages now exist, and navigation destroys the old page itself.
   - **Fix:** Delete those methods after repeating the caller search at implementation time. Keep BaseGUIView and its existing subclasses; do not change the package structure for a few saved lines.
   - **If we skip it:** Unused interfaces imply behaviors future contributors may mistakenly depend on. Keep `show_view()` and `show_content()`—they manage different containers and are both used.

**Nice to have — optional, not part of the default simplification**

14. **Native messageboxes could replace custom popup plumbing.** `views/gui/error_view.py:14–39`.
   - **What this is:** The custom dialog manually handles symbols, sizing, centering, visibility, focus, grabbing input, and waiting for dismissal.
   - **Problem:** That behavior needs platform interaction checks; existing confirmation dialogs already use native messageboxes. This is a maintenance tradeoff, not a reproduced popup defect.
   - **Fix:** Only if a visible design change is wanted, keep `ErrorView.show_error/show_success` and implement them using parented `messagebox.showerror/showinfo`. Otherwise retain the custom helper and test it; it is already shared.
   - **If we skip it:** The custom appearance stays, along with its testing responsibility. Do not remove it automatically: it was recently added in the current working tree.

15. **Spacer-only Frames can become normal widget padding.** `welcome_view.py:26,35`, `login_view.py:25,46,64`, `registration_view.py:24,42,57,73`, and `dashboard_view.py:90` under `views/gui/` and `views/gui/gui_student/`.
   - **What this is:** Empty widgets reserve vertical gaps.
   - **Problem:** They add layout objects that contain no content.
   - **Fix:** Move each gap into the adjacent widget's `pady` when touching that screen and compare the rendered result. Do not bulk-convert `place` to `pack` or `grid` without a separate layout reason.
   - **If we skip it:** The existing layout remains explicit and functional. This is a small cleanup, not worth risking appearance by itself.

**Known limits and adjacent issues**

- **Plaintext credentials:** `StudentDataFile.save_students()` writes the password value directly, and the service compares it directly. Existing project guidance explicitly treats this as a fictional-data classroom prototype. Keep that limitation visible; do not call this secure for real accounts. Password hashing would require a separate coordinated change to registration, login, password change, serialization, existing records, and tests; it is not a view simplification.
- **Multiple application processes:** Loading and replacing the whole student list can overwrite another process's changes. Atomic replacement fixes torn writes, not competing updates. Do not introduce locking or a database framework for this one-process review; reconsider storage if simultaneous writers become required.
- **Performance:** Data operations reread the whole file, sometimes several times per action. With the current small local dataset and four subjects per student, this review found no reason to add caching, background workers, or an ORM. No load benchmark was run.
- **CLI password-change bug:** `controllers/cli/student_controller.py:110` unpacks two values while `views/cli/student_view.py:51–58` returns three. The GUI correctly handles three fields. Keep the shared service signature unchanged; repair this CLI caller in a separately scoped fix rather than changing the service to accommodate the mismatch.
- **Layout and keyboard interaction:** Fixed window/card/list sizes, long names/emails, focus order, Enter/Escape behavior, and modal dismissal need real Tk checks. No clipping or accessibility failure is asserted from source inspection alone. Do not add a responsive-layout system before observing a concrete problem.
- **Scope:** This review does not certify the assessment rubric, implement Admin functionality, or audit unrelated Admin behavior. Older documents describe plans that differ from the current single-root screen design.

**Implementation order and complete change scope**

The default recommendation preserves the current appearance, screen navigation, public service contracts, and project structure. The items below are planned work only, not permission inferred to modify code during this review.

| Stage | Change and affected files | Completion check |
| --- | --- | --- |
| A. Establish the baseline | Update obsolete assertions in `tests/test_student.py`; add focused controller/service tests, retaining `tests/test_subjects_view.py`. | Current behavior passes meaningful tests before refactoring. Record remaining known failures honestly. |
| B. Repair storage reliability | `models/file_handlers/database.py`, `student_data_file.py`; add storage/service failure tests. Review both GUI and CLI callers because the storage classes are shared. | Failed writes preserve original bytes; corrupt existing files remain untouched; GUI shows a useful error; successful changes survive reload. |
| C. Remove dead/unsupported GUI paths | `gui_student_controller.py`, `subjects_view.py`, `student_main_view.py`, `base_gui_view.py`; update targeted tests. | No False-result branch, no unused methods, required callbacks supplied everywhere; confirmations and per-row IDs still correct. |
| D. Simplify repeated layouts | `dashboard_view.py`, `account_view.py`, `student_main_view.py`; targeted callback/field checks. | Same cards, labels, masking, field order, navigation, and button behavior; visual comparison at 0/1/3/4 subjects. |
| E. Share auth-field construction | `base_gui_view.py`, `login_view.py`, `registration_view.py`; shared auth style setup in the existing GUI layer. | Both forms render correctly independently; callbacks pass the exact original values; screens retain their own fields and spacing. |
| F. Correct password help and documentation | `models/student_service.py`, focused validation/message tests, progress files, historical refactor guide. | Both messages match Validator; docs describe only current implemented/verified behavior. |
| Optional later | Native dialog replacement, only if its different appearance is accepted. | Error/info/confirmation parenting, dismissal, focus, and modality checked on macOS. |

No new runtime dependency is needed. Existing `__init__.py` files have no exports that require changes for this plan. There is one GUIStudentController construction site in GUIUniApp and one SubjectsView construction site in the student controller. Re-run searches before implementing because this is an actively edited working tree.

Keep GUIUniApp and GUIStudentController separate. Keep the shell's `show_content()` separate from the application's `show_view()`. Keep individual screen classes. Keep small explicit action handlers instead of a generic `perform_action`, route dictionary, command registry, or callback framework. Recreating one small content frame after a successful action is adequate here; no observer/event system or page cache is needed.

Do not remove validation, enrollment/removal confirmation, error handling, saved-record reloads, or session synchronization to reduce line count. Do not reintroduce old subject/enrollment files. Do not change student data formats, IDs, grading rules, or password rules in the GUI cleanup. Keep `start()` as the simple student-controller entry point used by Welcome.

**Acceptance checks for the later implementation**

Use temporary storage for automated tests. For manual checks, use a disposable copy of the project/data, since the normal GUI entry point writes to the real project data folder.

1. Welcome → Student → Login; Login Back → Welcome. Admin remains disabled.
2. Login → Registration → Back. Register a valid fictional student and check the success message contains the ID and returns to Login. Reject empty name, wrong email domain, duplicate email, and each invalid-password category.
3. Reject empty and incorrect login details without opening a student session. Valid login opens Dashboard. Logout and logging in as a different student must not show the previous student's data.
4. Check Dashboard with 0, 1, 3, and 4 subjects: always four slots, correct marks/grades, and correct overall tuple formatting. Preserve leading-zero IDs.
5. Cancel enrollment: no service call or write. Confirm enrollment: one call, persisted subject, refreshed count. Four subjects disable enrollment; the service independently rejects a fifth.
6. Cancel removal: unchanged data. Confirm removal of a middle row: only that row's ID is passed and removed. Return to Dashboard and verify updated averages/slots. Log out/in and verify persistence.
7. Account shows the correct name/ID/email. All three password entries are masked. Empty/mismatched confirmation is rejected before calling the service; wrong current, weak new, and reused passwords are rejected by the service.
8. Successful password change clears the form through refresh. After logout, the old password fails and the new one works.
9. Simulate ValueError/OSError for each controller action: one useful error, no success message, and no unintended navigation. Save failures must not mutate the active student.
10. Simulate failure during serialization and replacement: the original saved bytes survive. Missing storage initializes correctly; an existing empty/corrupt file raises clearly and is not reset.
11. Exercise real error/success/confirmation dialogs: correct parent, visible message, usable OK/Yes/No controls, keyboard focus, and no lingering input grab after closing. Verify root-window close behavior.
12. Check actual macOS layout at 1000 × 700 with long profile values and four subjects: no clipped inputs, hidden buttons, overlapping cards, or inaccessible controls. Check keyboard traversal and activation; record any failures before changing geometry.

Existing automated suite command:

```bash
python3 -B -m unittest discover -s tests -v
```

Manual GUI command, from a disposable working copy:

```bash
python3 -B gui_main.py
```

**Verdict:** Preserve the existing architecture. Fix destructive writes and malformed-record handling, establish a passing behavioral baseline, then simplify repeated widgets and dead branches in small stages.

**Lean:** Approximately 60–100 source lines could be removed across the default GUI simplifications, with 0 dependencies removed or added. This is a planning estimate, not a measured patch; necessary tests and storage fixes may increase total repository lines. The optional native-dialog change could remove roughly another 20–25 lines.

**Not checked:** Live GUI rendering/interaction, full CLI/Admin behavior, concurrent writers, load benchmarks, and official assessment compliance. **Risk:** Existing storage writes can lose data on failure, and passwords remain plaintext; neither issue was modified by this review.
