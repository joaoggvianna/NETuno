from collections.abc import Callable

from core.models import CommandResult, ParsedCommand
from integrations.spotify import SpotifyError, SpotifyIntegration


spotify = SpotifyIntegration()


def play_music(command: ParsedCommand) -> CommandResult:
    """Resume playback or open a truthful search fallback for a named item."""
    if command.query:
        try:
            spotify.open_search(command.query)
        except SpotifyError as error:
            return CommandResult(False, str(error))

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
        spotify.play,
        "Reprodução iniciada no Spotify.",
    )


def resume_music(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(
        spotify.play,
        "Reprodução retomada no Spotify.",
    )


def pause_music(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(spotify.pause, "Spotify pausado.")


def next_track(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(spotify.next_track, "Avançando para a próxima faixa.")


def previous_track(command: ParsedCommand) -> CommandResult:
    del command
    return _run_spotify_action(spotify.previous_track, "Voltando para a faixa anterior.")


def _run_spotify_action(
    action: Callable[[], None], success_message: str
) -> CommandResult:
    try:
        action()
    except SpotifyError as error:
        return CommandResult(False, str(error))

    return CommandResult(True, success_message)
