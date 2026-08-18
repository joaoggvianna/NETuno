from dataclasses import dataclass
from enum import Enum, auto


class Intent(Enum):
    """Actions understood by the current Jarvis version."""

    GET_TIME = auto()
    GET_DATE = auto()
    EXIT = auto()
    UNKNOWN = auto()


@dataclass(frozen=True)
class ParsedCommand:
    """Structured representation of a command entered by the user."""

    intent: Intent
    original_text: str


@dataclass(frozen=True)
class CommandResult:
    """Standard response returned after a command is handled."""

    success: bool
    message: str
    should_exit: bool = False
