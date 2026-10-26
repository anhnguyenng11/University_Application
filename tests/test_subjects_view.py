import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from views.gui.gui_student.subjects_view import SubjectsView


class TestSubjectsView(unittest.TestCase):
    def test_enroll_requires_confirmation(self):
        for confirmed in (True, False):
            with self.subTest(confirmed=confirmed):
                callback = Mock()
                view = SimpleNamespace(on_enroll=callback)
                with patch(
                    "views.gui.gui_student.subjects_view.messagebox.askyesno",
                    return_value=confirmed
                ):
                    SubjectsView.confirm_enroll(view)

                if confirmed:
                    callback.assert_called_once_with()
                else:
                    callback.assert_not_called()

    def test_remove_requires_confirmation_for_selected_subject(self):
        for confirmed in (True, False):
            with self.subTest(confirmed=confirmed):
                callback = Mock()
                view = SimpleNamespace(on_remove=callback)
                with patch(
                    "views.gui.gui_student.subjects_view.messagebox.askyesno",
                    return_value=confirmed
                ) as dialog:
                    SubjectsView.confirm_remove(view, "12345")

                self.assertIn("12345", dialog.call_args.args[1])
                if confirmed:
                    callback.assert_called_once_with("12345")
                else:
                    callback.assert_not_called()
