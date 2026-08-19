from collections.abc import Callable, Mapping
from typing import Optional

from commands.apps import open_app
from commands.modes import run_mode
from commands.music import (
    next_track,
    pause_music,
    play_music,
    previous_track,
    resume_music,
)
from commands.notes import create_note, delete_note, list_notes
from commands.system import (
    exit_netuno,
    get_current_date,
    get_current_time,
    get_system_status,
)
from commands.web import open_website
from core.models import CommandResult, Intent, ParsedCommand

CommandHandler = Callable[[ParsedCommand], CommandResult]


class Router:
    """Send parsed commands to the handler registered for each intent."""

    def __init__(
        self, handlers: Optional[Mapping[Intent, CommandHandler]] = None
    ) -> None:
        self._handlers = dict(handlers) if handlers is not None else {
            Intent.GET_TIME: get_current_time,
            Intent.GET_DATE: get_current_date,
            Intent.GET_SYSTEM_STATUS: get_system_status,
            Intent.OPEN_APP: open_app,
            Intent.OPEN_WEBSITE: open_website,
            Intent.CREATE_NOTE: create_note,
            Intent.LIST_NOTES: list_notes,
            Intent.DELETE_NOTE: delete_note,
            Intent.RUN_MODE: run_mode,
            Intent.PLAY_MUSIC: play_music,
            Intent.PAUSE_MUSIC: pause_music,
            Intent.RESUME_MUSIC: resume_music,
            Intent.NEXT_TRACK: next_track,
            Intent.PREVIOUS_TRACK: previous_track,
            Intent.EXIT: exit_netuno,
        }

    def dispatch(self, command: ParsedCommand) -> CommandResult:
        handler = self._handlers.get(command.intent)
        if handler is None:
            return CommandResult(
                success=False,
                message="Não reconheci esse comando.",
            )

        return handler(command)
