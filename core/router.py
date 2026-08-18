from collections.abc import Callable, Mapping
from typing import Optional

from commands.system import get_current_date, get_current_time, exit_jarvis
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
            Intent.EXIT: exit_jarvis,
        }

    def dispatch(self, command: ParsedCommand) -> CommandResult:
        handler = self._handlers.get(command.intent)
        if handler is None:
            return CommandResult(
                success=False,
                message="Não reconheci esse comando.",
            )

        return handler(command)
