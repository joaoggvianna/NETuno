from datetime import datetime
import os
import platform
import subprocess
from typing import Optional

import psutil

from desktop_agent.schemas import (
    ActionRequest,
    ActionResponse,
    ActionType,
    AppTarget,
    SystemStatusData,
)
from integrations.spotify import SpotifyError, SpotifyIntegration


SUPPORTED_APPS = {
    AppTarget.VSCODE: "Visual Studio Code",
    AppTarget.SPOTIFY: "Spotify",
}


class DesktopExecutor:
    """Execute only the desktop actions declared by the Agent contract."""

    def __init__(self, spotify: Optional[SpotifyIntegration] = None) -> None:
        self._spotify = spotify or SpotifyIntegration()

    def execute(self, request: ActionRequest) -> ActionResponse:
        handlers = {
            ActionType.OPEN_APP: self._open_app,
            ActionType.GET_SYSTEM_STATUS: self._get_system_status,
            ActionType.SPOTIFY_PLAY: lambda _: self._spotify_action(
                self._spotify.play
            ),
            ActionType.SPOTIFY_PAUSE: lambda _: self._spotify_action(
                self._spotify.pause
            ),
            ActionType.SPOTIFY_NEXT: lambda _: self._spotify_action(
                self._spotify.next_track
            ),
            ActionType.SPOTIFY_PREVIOUS: lambda _: self._spotify_action(
                self._spotify.previous_track
            ),
            ActionType.SPOTIFY_SEARCH: self._spotify_search,
        }
        return handlers[request.action](request)

    @staticmethod
    def _open_app(request: ActionRequest) -> ActionResponse:
        app_name = SUPPORTED_APPS[request.target]
        if platform.system() != "Darwin":
            return ActionResponse(
                success=False,
                error_code="execution_error",
                message=(
                    "A abertura de aplicativos nesta versão está disponível "
                    "apenas no macOS."
                ),
            )

        try:
            subprocess.run(
                ["open", "-a", app_name],
                check=True,
                capture_output=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            return ActionResponse(
                success=False,
                error_code="execution_error",
                message=(
                    f"Não foi possível abrir {app_name}. "
                    "Verifique se o aplicativo está instalado."
                ),
            )

        return ActionResponse(success=True)

    @staticmethod
    def _get_system_status(_: ActionRequest) -> ActionResponse:
        try:
            data = SystemStatusData(
                cpu_percent=psutil.cpu_percent(interval=0.1),
                memory_percent=psutil.virtual_memory().percent,
                disk_percent=psutil.disk_usage(os.path.abspath(os.sep)).percent,
                uptime_seconds=max(
                    0,
                    int(datetime.now().timestamp() - psutil.boot_time()),
                ),
            )
        except (OSError, RuntimeError):
            return ActionResponse(
                success=False,
                error_code="execution_error",
                message="Não foi possível consultar o status do computador.",
            )

        return ActionResponse(success=True, data=data)

    def _spotify_search(self, request: ActionRequest) -> ActionResponse:
        return self._spotify_action(
            lambda: self._spotify.open_search(request.query or "")
        )

    @staticmethod
    def _spotify_action(action) -> ActionResponse:
        try:
            action()
        except SpotifyError as error:
            return ActionResponse(
                success=False,
                error_code="execution_error",
                message=str(error),
            )

        return ActionResponse(success=True)
