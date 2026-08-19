from database.database import delete_note as delete_note_from_database
from database.database import insert_note, list_notes as list_notes_from_database
from core.models import CommandResult, ParsedCommand


def create_note(command: ParsedCommand) -> CommandResult:
    """Persist the note content extracted from a command."""
    content = (command.content or "").strip()
    if not content:
        return CommandResult(False, "Informe o conteúdo da nota.")

    insert_note(content)
    return CommandResult(True, "Nota criada.")


def list_notes(command: ParsedCommand) -> CommandResult:
    """List persisted notes with sequential, user-facing numbers."""
    del command
    notes = list_notes_from_database()
    if not notes:
        return CommandResult(True, "Você ainda não possui notas.")

    message = "\n".join(
        f"{number}. {content}"
        for number, (_note_id, content, _created_at) in enumerate(notes, start=1)
    )
    return CommandResult(True, message)


def delete_note(command: ParsedCommand) -> CommandResult:
    """Remove the note at the user-facing position in the current list."""
    if command.note_number is None or command.note_number <= 0:
        return CommandResult(False, "Informe um número de nota válido.")

    notes = list_notes_from_database()
    if command.note_number > len(notes):
        return CommandResult(False, "Nota não encontrada.")

    persistent_id = notes[command.note_number - 1][0]

    if not delete_note_from_database(persistent_id):
        return CommandResult(False, "Nota não encontrada.")

    return CommandResult(True, "Nota removida.")
