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

    def parse(self, text: str) -> ParsedCommand:
        normalized_text = self._normalize(text)

        if normalized_text in self._TIME_COMMANDS:
            intent = Intent.GET_TIME
        elif normalized_text in self._DATE_COMMANDS:
            intent = Intent.GET_DATE
        elif normalized_text in self._EXIT_COMMANDS:
            intent = Intent.EXIT
        else:
            intent = Intent.UNKNOWN

        return ParsedCommand(intent=intent, original_text=text)

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
