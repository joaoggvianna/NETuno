from datetime import datetime

from core.agent_client import AgentClient, AgentClientError
from core.models import CommandResult, ParsedCommand


agent_client = AgentClient()


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
    """Format the structured system snapshot returned by the Desktop Agent."""
    del command

    try:
        result = agent_client.get_system_status()
    except AgentClientError as error:
        return CommandResult(False, str(error))

    if not result.success or result.data is None:
        return CommandResult(
            False,
            result.message or "Não foi possível consultar o status do computador.",
        )

    try:
        cpu_percent = float(result.data["cpu_percent"])
        memory_percent = float(result.data["memory_percent"])
        disk_percent = float(result.data["disk_percent"])
        uptime_seconds = max(0, int(result.data["uptime_seconds"]))
    except (KeyError, TypeError, ValueError):
        return CommandResult(False, "O Desktop Agent retornou dados inválidos.")

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
