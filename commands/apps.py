import platform
import subprocess

from core.models import CommandResult, ParsedCommand


SUPPORTED_APPS = {
    "vscode": "Visual Studio Code",
    "spotify": "Spotify",
}


def open_app(command: ParsedCommand) -> CommandResult:
    """Open an explicitly supported application on macOS."""
    app_name = SUPPORTED_APPS.get(command.target or "")
    if app_name is None:
        return CommandResult(False, "Aplicativo não suportado.")

    if platform.system() != "Darwin":
        return CommandResult(
            False,
            "A abertura de aplicativos nesta versão está disponível apenas no macOS.",
        )

    try:
        subprocess.run(
            ["open", "-a", app_name],
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return CommandResult(
            False,
            f"Não foi possível abrir {app_name}. Verifique se o aplicativo está instalado.",
        )

    return CommandResult(True, f"Abrindo {app_name}.")
