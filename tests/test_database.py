import sqlite3
import tempfile
import unittest
from pathlib import Path

from database.database import delete_note, initialize_database, insert_note, list_notes


class DatabaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temporary_directory.name) / "test.db"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_initializes_notes_table(self) -> None:
        initialize_database(self.database_path)

        with sqlite3.connect(self.database_path) as connection:
            table = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'notes'"
            ).fetchone()

        self.assertEqual(table, ("notes",))

    def test_inserts_and_lists_note(self) -> None:
        note_id = insert_note("comprar pão", self.database_path)

        notes = list_notes(self.database_path)

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0][0], note_id)
        self.assertEqual(notes[0][1], "comprar pão")
        self.assertTrue(notes[0][2])

    def test_deletes_existing_note(self) -> None:
        note_id = insert_note("nota temporária", self.database_path)

        removed = delete_note(note_id, self.database_path)

        self.assertTrue(removed)
        self.assertEqual(list_notes(self.database_path), [])

    def test_delete_returns_false_for_missing_id(self) -> None:
        self.assertFalse(delete_note(999, self.database_path))

    def test_persists_notes_between_connections(self) -> None:
        note_id = insert_note("nota persistente", self.database_path)

        notes_from_new_connection = list_notes(self.database_path)

        self.assertEqual(notes_from_new_connection[0][0], note_id)
        self.assertEqual(notes_from_new_connection[0][1], "nota persistente")


if __name__ == "__main__":
    unittest.main()
