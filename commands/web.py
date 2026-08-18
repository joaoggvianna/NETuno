import webbrowser

from core.models import CommandResult, ParsedCommand


SUPPORTED_WEBSITES = {
    "youtube": "https://www.youtube.com",
}


def open_website(command: ParsedCommand) -> CommandResult:
    """Open an explicitly supported website in the default browser."""
    url = SUPPORTED_WEBSITES.get(command.target or "")
    if url is None:
        return CommandResult(False, "Site não suportado.")

    if not webbrowser.open(url, new=2):
        return CommandResult(False, "Não foi possível abrir o navegador.")

    return CommandResult(True, "Abrindo YouTube.")
