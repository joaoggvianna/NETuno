from typing import Optional

from core.command_parser import CommandParser
from core.models import CommandResult
from core.router import Router


class Assistant:
    """Coordinate command parsing and execution."""

    def __init__(
        self,
        parser: Optional[CommandParser] = None,
        router: Optional[Router] = None,
    ) -> None:
        self._parser = parser or CommandParser()
        self._router = router or Router()

    def process_command(self, text: str) -> CommandResult:
        command = self._parser.parse(text)
        return self._router.dispatch(command)
