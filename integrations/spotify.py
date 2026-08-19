import platform
import subprocess
from pathlib import Path
from urllib.parse import quote


SPOTIFY_APP_PATH = Path("/Applications/Spotify.app")


class SpotifyError(RuntimeError):
    """Raised when a local Spotify operation cannot be completed."""


class SpotifyIntegration:
    """Control supported Spotify operations through local macOS interfaces."""

    _SCRIPTS = {
        "play": 'tell application "Spotify" to play',
        "pause": 'tell application "Spotify" to pause',
        "next": 'tell application "Spotify" to next track',
        "previous": 'tell application "Spotify" to previous track',
    }

    def play(self) -> None:
        self._run_applescript("play")

    def pause(self) -> None:
        self._run_applescript("pause")

    def next_track(self) -> None:
        self._run_applescript("next")

    def previous_track(self) -> None:
        self._run_applescript("previous")

    def open_search(self, query: str) -> None:
        """Open Spotify search results without claiming automatic playback."""
        self._ensure_available()
        search_uri = f"spotify:search:{quote(query, safe='')}"

        try:
            subprocess.run(
                ["open", search_uri],
                check=True,
                capture_output=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            raise SpotifyError("Não foi possível abrir a busca no Spotify.") from error

    def _run_applescript(self, operation: str) -> None:
        self._ensure_available()

        try:
            subprocess.run(
                ["osascript", "-e", self._SCRIPTS[operation]],
                check=True,
                capture_output=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            raise SpotifyError("Não foi possível controlar o Spotify.") from error

    @staticmethod
    def _ensure_available() -> None:
        if platform.system() != "Darwin" or not SPOTIFY_APP_PATH.is_dir():
            raise SpotifyError(
                "Spotify não está disponível neste computador ou sistema operacional."
            )
