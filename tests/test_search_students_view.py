import unittest
from contextlib import ExitStack
from tkinter import ttk
from unittest.mock import Mock, patch

from controllers.gui.gui_admin_controller import GUIAdminController
from models.student import Student
from models.subject import Subject
from views.gui.gui_admin.search_student_view import SearchStudentsView


class TestSearchStudentsView(unittest.TestCase):
    def test_search_clears_previous_result_and_submits_both_fields(self):
        with ExitStack() as stack:
            stack.enter_context(patch.object(ttk.Frame, "__init__", return_value=None))
            widgets = {
                name: stack.enter_context(patch.object(ttk, name))
                for name in ("Frame", "LabelFrame", "Label", "Entry", "Button", "Style")
            }
            widgets["Entry"].side_effect = [
                Mock(get=Mock(return_value="000001")),
                Mock(get=Mock(return_value="alice@university.com"))
            ]
            on_search = Mock()
            view = SearchStudentsView(None, on_search, Mock())
            previous_result = Mock()
            view.result_frame.winfo_children.return_value = [previous_result]

            search = next(call for call in widgets["Button"].call_args_list
                          if call.kwargs["text"] == "Search")
            search.kwargs["command"]()

            previous_result.destroy.assert_called_once_with()
            on_search.assert_called_once_with("000001", "alice@university.com")

    def test_overall_table_follows_subjects_including_empty_enrollment(self):
        for marks, expected in (
            ([80, 98, 98, 60], ("84.00", "D", "PASS")),
            ([40], ("40.00", "Z", "FAIL")),
            ([], ("N/A", "N/A", "N/A"))
        ):
            with self.subTest(marks=marks), ExitStack() as stack:
                stack.enter_context(patch.object(ttk.Frame, "__init__", return_value=None))
                widgets = {
                    name: stack.enter_context(patch.object(ttk, name))
                    for name in ("Frame", "LabelFrame", "Label", "Entry", "Button", "Style", "Treeview")
                }
                view = SearchStudentsView(None, Mock(), Mock())
                widgets["LabelFrame"].reset_mock()
                info_table, subject_table, overall_table = Mock(), Mock(), Mock()
                widgets["Treeview"].side_effect = (
                    [info_table, subject_table, overall_table] if marks else [info_table, overall_table]
                )
                student = Student(
                    "000001", "Alice", "alice@university.com", "Password123",
                    [Subject(str(index), mark) for index, mark in enumerate(marks)]
                )

                view.show_student(student)

                titles = [call.kwargs.get("text", "") for call in widgets["LabelFrame"].call_args_list]
                self.assertEqual(titles[:2], ["Student Information", "Enrolled Subjects"])
                self.assertEqual(len(titles), 3)
                info_table.insert.assert_called_once_with(
                    "", "end", values=(student.student_id, student.name, student.email)
                )
                overall_table.insert.assert_called_once_with("", "end", values=expected)
                self.assertEqual(widgets["Treeview"].call_args.kwargs["height"], 1)
                if marks:
                    self.assertEqual(subject_table.insert.call_count, len(marks))

    def test_remove_state_and_confirmation_use_the_displayed_student(self):
        with ExitStack() as stack:
            stack.enter_context(patch.object(ttk.Frame, "__init__", return_value=None))
            widgets = {
                name: stack.enter_context(patch.object(ttk, name))
                for name in ("Frame", "LabelFrame", "Label", "Entry", "Button", "Style", "Treeview")
            }
            on_search, on_remove = Mock(), Mock()
            view = SearchStudentsView(None, on_search, on_remove)
            self.assertEqual(widgets["Button"].call_args.kwargs["state"], "disabled")
            confirmation = stack.enter_context(patch(
                "views.gui.gui_admin.search_student_view.messagebox.askyesno"
            ))
            view.confirm_remove()
            confirmation.assert_not_called()

            student = Student("000001", "Alice", "alice@university.com", "Password123")
            view.show_student(student)
            view.remove_button.configure.assert_called_with(state="normal")
            view.student_id_entry.get.return_value = "999999"

            confirmation.return_value = False
            view.confirm_remove()
            on_remove.assert_not_called()
            self.assertEqual(view.displayed_student_id, "000001")

            confirmation.return_value = True
            view.confirm_remove()
            on_remove.assert_called_once_with("000001")
            self.assertIn("000001", confirmation.call_args.args[1])

            view.submit_search()
            self.assertIsNone(view.displayed_student_id)
            view.remove_button.configure.assert_called_with(state="disabled")
            view.show_student(student)
            view.show_student(None)
            self.assertIsNone(view.displayed_student_id)
            view.remove_button.configure.assert_called_with(state="disabled")


class TestSearchStudentRemovalController(unittest.TestCase):
    def setUp(self):
        self.service, self.error, self.success = Mock(), Mock(), Mock()
        self.controller = GUIAdminController(
            None, self.service, Mock(), Mock(), self.error, self.success
        )
        self.controller.main_view = Mock()

    def test_search_removal_clears_result_and_stays_on_search_page(self):
        with patch("controllers.gui.gui_admin_controller.SearchStudentsView") as view:
            self.controller.show_search_students()
            view.assert_called_once_with(
                self.controller.main_view.content_frame,
                on_search=self.controller.search_student,
                on_remove=self.controller.remove_student
            )
            with patch.object(self.controller, "show_students") as show_students:
                self.controller.remove_student("000001")
                show_students.assert_not_called()
            self.service.remove_student.assert_called_once_with("000001")
            view.return_value.clear_result.assert_called_once_with()
            self.success.assert_called_once_with("Student removed successfully.")

    def test_list_removal_preserves_grade_grouping(self):
        self.controller.student_mode = "grade"
        with patch.object(self.controller, "show_students", return_value=True) as refresh:
            self.controller.remove_student("000001")
            refresh.assert_called_once_with("grade")
        self.success.assert_called_once_with("Student removed successfully.")

    def test_failed_removal_keeps_result_and_does_not_report_success(self):
        self.controller.student_mode = "search"
        self.controller.search_view = Mock()
        for failure in (False, ValueError("Invalid data"), OSError("Save failed")):
            with self.subTest(failure=failure):
                self.error.reset_mock()
                self.service.remove_student.side_effect = failure if isinstance(failure, Exception) else None
                self.service.remove_student.return_value = False
                self.controller.remove_student("000001")
                self.controller.search_view.clear_result.assert_not_called()
                self.success.assert_not_called()
                self.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
