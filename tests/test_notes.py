import unittest
from unittest.mock import patch

from commands.notes import create_note, delete_note, list_notes
from core.models import Intent, ParsedCommand


class NotesCommandsTestCase(unittest.TestCase):
    @patch("commands.notes.insert_note", return_value=1)
    def test_creates_note(self, insert_note_mock) -> None:
        command = ParsedCommand(
            Intent.CREATE_NOTE,
            "criar nota comprar pão",
            content="comprar pão",
        )

        result = create_note(command)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Nota criada.")
        insert_note_mock.assert_called_once_with("comprar pão")

    @patch("commands.notes.list_notes_from_database")
    def test_lists_notes(self, list_notes_mock) -> None:
        list_notes_mock.return_value = [
            (1, "comprar presente", "2026-08-18T10:00:00"),
            (3, "revisar banco", "2026-08-18T11:00:00"),
        ]

        result = list_notes(ParsedCommand(Intent.LIST_NOTES, "listar notas"))

        self.assertTrue(result.success)
        self.assertEqual(result.message, "1. comprar presente\n2. revisar banco")

    @patch("commands.notes.list_notes_from_database", return_value=[])
    def test_lists_empty_notes(self, list_notes_mock) -> None:
        result = list_notes(ParsedCommand(Intent.LIST_NOTES, "listar notas"))

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Você ainda não possui notas.")

    @patch("commands.notes.delete_note_from_database", return_value=True)
    @patch("commands.notes.list_notes_from_database")
    def test_deletes_note_by_its_displayed_number(
        self, list_notes_mock, delete_note_mock
    ) -> None:
        list_notes_mock.return_value = [
            (4, "primeira nota", "2026-08-18T10:00:00"),
            (9, "segunda nota", "2026-08-18T11:00:00"),
        ]
        command = ParsedCommand(
            Intent.DELETE_NOTE,
            "remover nota 1",
            note_number=1,
        )

        result = delete_note(command)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Nota removida.")
        delete_note_mock.assert_called_once_with(4)

    @patch("commands.notes.delete_note_from_database")
    @patch("commands.notes.list_notes_from_database", return_value=[])
    def test_reports_missing_note(self, list_notes_mock, delete_note_mock) -> None:
        command = ParsedCommand(
            Intent.DELETE_NOTE,
            "remover nota 99",
            note_number=99,
        )

        result = delete_note(command)

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Nota não encontrada.")
        delete_note_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
