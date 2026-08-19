from dataclasses import dataclass

from commands.apps import open_app
from commands.web import open_website
from core.models import CommandResult, Intent, ParsedCommand


@dataclass(frozen=True)
class ModeAction:
    intent: Intent
    target: str
    label: str


@dataclass(frozen=True)
class ModeDefinition:
    success_message: str
    partial_message: str
    actions: tuple[ModeAction, ...]


MODE_DEFINITIONS = {
    "study": ModeDefinition(
        success_message="Modo estudo iniciado.",
        partial_message="Modo estudo iniciado parcialmente.",
        actions=(
            ModeAction(Intent.OPEN_APP, "vscode", "Visual Studio Code"),
            ModeAction(Intent.OPEN_APP, "spotify", "Spotify"),
            ModeAction(Intent.OPEN_WEBSITE, "study", "ambiente de estudo"),
        ),
    ),
    "vscode_spotify": ModeDefinition(
        success_message="Comando composto concluído.",
        partial_message="Comando composto concluído parcialmente.",
        actions=(
            ModeAction(Intent.OPEN_APP, "vscode", "Visual Studio Code"),
            ModeAction(Intent.OPEN_APP, "spotify", "Spotify"),
        ),
    ),
    "spotify_youtube": ModeDefinition(
        success_message="Comando composto concluído.",
        partial_message="Comando composto concluído parcialmente.",
        actions=(
            ModeAction(Intent.OPEN_APP, "spotify", "Spotify"),
            ModeAction(Intent.OPEN_WEBSITE, "youtube", "YouTube"),
        ),
    ),
}


def run_mode(command: ParsedCommand) -> CommandResult:
    """Execute every action in an explicitly registered mode or composition."""
    definition = MODE_DEFINITIONS.get(command.target or "")
    if definition is None:
        return CommandResult(False, "Modo ou comando composto não suportado.")

    handlers = {
        Intent.OPEN_APP: open_app,
        Intent.OPEN_WEBSITE: open_website,
    }
    action_results = []

    for action in definition.actions:
        action_command = ParsedCommand(
            intent=action.intent,
            original_text=command.original_text,
            target=action.target,
        )
        result = handlers[action.intent](action_command)
        action_results.append((action, result))

    all_succeeded = all(result.success for _action, result in action_results)
    heading = (
        definition.success_message if all_succeeded else definition.partial_message
    )
    details = [
        f"✓ {action.label}"
        if result.success
        else f"✗ {action.label}: {result.message}"
        for action, result in action_results
    ]
    return CommandResult(all_succeeded, "\n".join([heading, "", *details]))
