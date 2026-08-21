from core.agent_client import AgentClient, AgentClientError
from core.models import CommandResult, ParsedCommand


SUPPORTED_APPS = {
    "vscode": "Visual Studio Code",
    "spotify": "Spotify",
}


def get_agent_client() -> AgentClient:
    return AgentClient()


def open_app(command: ParsedCommand) -> CommandResult:
    """Ask the Desktop Agent to open an explicitly supported application."""
    app_name = SUPPORTED_APPS.get(command.target or "")
    if app_name is None:
        return CommandResult(False, "Aplicativo não suportado.")

    try:
        result = get_agent_client().open_app(command.target or "")
    except AgentClientError as error:
        return CommandResult(False, str(error))

    if not result.success:
        return CommandResult(
            False,
            result.message or "Não foi possível abrir o aplicativo.",
        )

    return CommandResult(True, f"Abrindo {app_name}.")
