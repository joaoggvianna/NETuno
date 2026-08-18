import unicodedata

from core.models import Intent, ParsedCommand


class CommandParser:
    """Convert supported text commands into explicit intents."""

    _TIME_COMMANDS = {
        "que horas sao",
        "qual a hora",
        "qual e a hora",
        "horas",
    }
    _DATE_COMMANDS = {
        "que dia e hoje",
        "qual a data de hoje",
        "data de hoje",
    }
    _EXIT_COMMANDS = {
        "sair",
        "encerrar",
        "fechar jarvis",
    }
    _APP_COMMANDS = {
        "abrir vscode": "vscode",
        "abre vscode": "vscode",
        "iniciar vscode": "vscode",
        "abrir visual studio code": "vscode",
        "abre visual studio code": "vscode",
        "iniciar visual studio code": "vscode",
        "abrir spotify": "spotify",
        "abre spotify": "spotify",
        "iniciar spotify": "spotify",
    }
    _WEBSITE_COMMANDS = {
        "abrir youtube": "youtube",
        "abre youtube": "youtube",
        "ir para youtube": "youtube",
    }

    def parse(self, text: str) -> ParsedCommand:
        normalized_text = self._normalize(text)

        if normalized_text in self._TIME_COMMANDS:
            intent = Intent.GET_TIME
        elif normalized_text in self._DATE_COMMANDS:
            intent = Intent.GET_DATE
        elif normalized_text in self._EXIT_COMMANDS:
            intent = Intent.EXIT
        elif normalized_text in self._APP_COMMANDS:
            intent = Intent.OPEN_APP
        elif normalized_text in self._WEBSITE_COMMANDS:
            intent = Intent.OPEN_WEBSITE
        else:
            intent = Intent.UNKNOWN

        target = self._APP_COMMANDS.get(normalized_text)
        if target is None:
            target = self._WEBSITE_COMMANDS.get(normalized_text)

        return ParsedCommand(intent=intent, original_text=text, target=target)

    @staticmethod
    def _normalize(text: str) -> str:
        text_without_accents = "".join(
            character
            for character in unicodedata.normalize("NFD", text)
            if unicodedata.category(character) != "Mn"
        )
        cleaned_text = "".join(
            character if character.isalnum() else " "
            for character in text_without_accents.casefold()
        )
        return " ".join(cleaned_text.split())
