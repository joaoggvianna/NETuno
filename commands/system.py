from datetime import datetime
import os

import psutil

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


def get_system_status(command: ParsedCommand) -> CommandResult:
    """Return a compact snapshot of CPU, memory, disk usage and uptime."""
    del command

    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage(os.path.abspath(os.sep)).percent
        uptime_seconds = max(0, int(datetime.now().timestamp() - psutil.boot_time()))
    except (OSError, RuntimeError):
        return CommandResult(
            success=False,
            message="Não foi possível consultar o status do computador.",
        )

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60

    uptime_parts = []
    if days:
        uptime_parts.append(f"{days}d")
    uptime_parts.append(f"{hours}h")
    uptime_parts.append(f"{minutes}min")

    uptime = " ".join(uptime_parts)
    message = (
        f"CPU: {cpu_percent:.0f}% | "
        f"Memória: {memory_percent:.0f}% | "
        f"Disco: {disk_percent:.0f}% | "
        f"Ligado há: {uptime}"
    )
    return CommandResult(success=True, message=message)


def exit_netuno(command: ParsedCommand) -> CommandResult:
    """Signal that the terminal loop should finish."""
    del command
    return CommandResult(success=True, message="Até mais.", should_exit=True)
