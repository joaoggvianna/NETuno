from datetime import datetime

from core.models import CommandResult, ParsedCommand


def get_current_time(command: ParsedCommand) -> CommandResult:
    """Return the current local time."""
    del command
    current_time = datetime.now().strftime("%H:%M")
    return CommandResult(success=True, message=f"Agora são {current_time}.")


def get_current_date(command: ParsedCommand) -> CommandResult:
    """Return the current local date."""
    del command
    current_date = datetime.now().strftime("%d/%m/%Y")
    return CommandResult(success=True, message=f"Hoje é {current_date}.")


def exit_jarvis(command: ParsedCommand) -> CommandResult:
    """Signal that the terminal loop should finish."""
    del command
    return CommandResult(success=True, message="Até mais.", should_exit=True)
