import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Union


DatabasePath = Union[str, Path]
DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "netuno.db"


def _resolve_database_path(database_path: Optional[DatabasePath]) -> Path:
    return Path(database_path) if database_path is not None else DEFAULT_DATABASE_PATH


def initialize_database(database_path: Optional[DatabasePath] = None) -> None:
    """Create the data directory and notes table when they do not exist."""
    path = _resolve_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def insert_note(content: str, database_path: Optional[DatabasePath] = None) -> int:
    """Persist a note and return its generated id."""
    path = _resolve_database_path(database_path)
    initialize_database(path)
    created_at = datetime.now().isoformat(timespec="seconds")

    with sqlite3.connect(path) as connection:
        cursor = connection.execute(
            "INSERT INTO notes (content, created_at) VALUES (?, ?)",
            (content, created_at),
        )
        return int(cursor.lastrowid)


def list_notes(
    database_path: Optional[DatabasePath] = None,
) -> list[tuple[int, str, str]]:
    """Return all notes ordered by their persistent id."""
    path = _resolve_database_path(database_path)
    initialize_database(path)

    with sqlite3.connect(path) as connection:
        rows = connection.execute(
            "SELECT id, content, created_at FROM notes ORDER BY id"
        ).fetchall()

    return [(int(note_id), content, created_at) for note_id, content, created_at in rows]


def delete_note(
    note_id: int, database_path: Optional[DatabasePath] = None
) -> bool:
    """Delete a note by id and report whether a row was removed."""
    path = _resolve_database_path(database_path)
    initialize_database(path)

    with sqlite3.connect(path) as connection:
        cursor = connection.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,),
        )
        return cursor.rowcount > 0
