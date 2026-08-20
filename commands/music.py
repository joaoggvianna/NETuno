from collections.abc import Callable

from core.agent_client import AgentClient, AgentClientError, AgentResult
from core.models import CommandResult, ParsedCommand


agent_client = AgentClient()


def play_music(command: ParsedCommand) -> CommandResult:
    """Resume playback or open a truthful search fallback for a named item."""
    if command.query:
        try:
            result = agent_client.spotify_search(command.query)
        except AgentClientError as error:
            return CommandResult(False, str(error))

        if not result.success:
            return CommandResult(
                False,
                result.message or "Não foi possível abrir a busca no Spotify.",
            )

        search_label = {
            "track": "pela música",
            "album": "pelo álbum",
            "artist": "pelo artista",
        }.get(command.media_type, "pelo termo")
        return CommandResult(
            False,
            f'Abri a busca {search_label} "{command.query}" no Spotify, '
            "mas esta versão não consegue iniciar o resultado automaticamente.",
        )

    return _run_spotify_action(
        agent_client.spotify_play,
        "Reprodução iniciada no Spotify.",
    )


def resume_music(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(
        agent_client.spotify_play,
        "Reprodução retomada no Spotify.",
    )


def pause_music(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(agent_client.spotify_pause, "Spotify pausado.")


def next_track(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(
        agent_client.spotify_next,
        "Avançando para a próxima faixa.",
    )


def previous_track(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(
        agent_client.spotify_previous,
        "Voltando para a faixa anterior.",
    )


def _run_spotify_action(
    action: Callable[[], AgentResult], success_message: str
) -> CommandResult:
    try:
        result = action()
    except AgentClientError as error:
        return CommandResult(False, str(error))

    if not result.success:
        return CommandResult(
            False,
            result.message or "Não foi possível controlar o Spotify.",
        )

    return CommandResult(True, success_message)
