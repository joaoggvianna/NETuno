import re
import unicodedata
from typing import Optional

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
    _SYSTEM_STATUS_COMMANDS = {
        "status do computador",
        "status do pc",
        "como esta o computador",
        "como esta o pc",
        "uso do computador",
    }
    _EXIT_COMMANDS = {
        "sair",
        "encerrar",
        "fechar jarvis",
        "fechar netuno",
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
    _LIST_NOTES_COMMANDS = {
        "listar notas",
        "mostrar notas",
        "minhas notas",
    }
    _CREATE_NOTE_PATTERN = re.compile(
        r"^\s*(?:criar\s+nota|anotar|nova\s+nota)(?:\s+|:\s*)(?P<content>.+?)\s*$",
        re.IGNORECASE,
    )
    _CREATE_NOTE_PREFIXES = ("criar nota", "anotar", "nova nota")
    _DELETE_NOTE_PATTERN = re.compile(
        r"^\s*(?:remover|apagar|deletar)\s+nota"
        r"(?:\s+(?P<number>.*?))?\s*[.!?]?\s*$",
        re.IGNORECASE,
    )
    _MODE_COMMANDS = {
        "modo estudo": "study",
        "iniciar modo estudo": "study",
        "comecar modo estudo": "study",
        "hora de estudar": "study",
        "abrir vscode e spotify": "vscode_spotify",
        "abrir visual studio code e spotify": "vscode_spotify",
        "abrir spotify e youtube": "spotify_youtube",
    }
    _MUSIC_COMMANDS = {
        "tocar musica": Intent.PLAY_MUSIC,
        "continuar musica": Intent.RESUME_MUSIC,
        "voltar musica": Intent.PREVIOUS_TRACK,
        "pausar musica": Intent.PAUSE_MUSIC,
        "pausar spotify": Intent.PAUSE_MUSIC,
        "proxima musica": Intent.NEXT_TRACK,
        "proxima faixa": Intent.NEXT_TRACK,
        "pular musica": Intent.NEXT_TRACK,
        "musica anterior": Intent.PREVIOUS_TRACK,
        "faixa anterior": Intent.PREVIOUS_TRACK,
        "voltar faixa": Intent.PREVIOUS_TRACK,
    }
    _MUSIC_QUERY_PATTERNS = (
        (
            re.compile(
                r"^\s*toque\s+(?:a\s+)?m[uú]sica\s+(?P<query>.+?)\s*$",
                re.IGNORECASE,
            ),
            "track",
        ),
        (
            re.compile(
                r"^\s*toque\s+(?:o\s+)?[aá]lbum\s+(?P<query>.+?)\s*$",
                re.IGNORECASE,
            ),
            "album",
        ),
        (
            re.compile(
                r"^\s*toque\s+(?:o\s+)?artista\s+(?P<query>.+?)\s*$",
                re.IGNORECASE,
            ),
            "artist",
        ),
        (
            re.compile(
                r"^\s*toque\s+(?P<query>.+?)\s+no\s+spotify\s*$",
                re.IGNORECASE,
            ),
            None,
        ),
        (
            re.compile(r"^\s*toque\s+(?P<query>.+?)\s*$", re.IGNORECASE),
            None,
        ),
    )

    def parse(self, text: str) -> ParsedCommand:
        normalized_text = self._normalize(text)
        note_command = self._parse_note_command(text, normalized_text)
        if note_command is not None:
            return note_command
        music_command = self._parse_music_command(text, normalized_text)
        if music_command is not None:
            return music_command

        if normalized_text in self._TIME_COMMANDS:
            intent = Intent.GET_TIME
        elif normalized_text in self._DATE_COMMANDS:
            intent = Intent.GET_DATE
        elif normalized_text in self._SYSTEM_STATUS_COMMANDS:
            intent = Intent.GET_SYSTEM_STATUS
        elif normalized_text in self._EXIT_COMMANDS:
            intent = Intent.EXIT
        elif normalized_text in self._APP_COMMANDS:
            intent = Intent.OPEN_APP
        elif normalized_text in self._WEBSITE_COMMANDS:
            intent = Intent.OPEN_WEBSITE
        elif normalized_text in self._MODE_COMMANDS:
            intent = Intent.RUN_MODE
        else:
            intent = Intent.UNKNOWN

        target = self._APP_COMMANDS.get(normalized_text)
        if target is None:
            target = self._WEBSITE_COMMANDS.get(normalized_text)
        if target is None:
            target = self._MODE_COMMANDS.get(normalized_text)

        return ParsedCommand(intent=intent, original_text=text, target=target)

    def _parse_music_command(
        self, original_text: str, normalized_text: str
    ) -> Optional[ParsedCommand]:
        intent = self._MUSIC_COMMANDS.get(normalized_text)
        if intent is not None:
            return ParsedCommand(intent, original_text, target="spotify")

        for pattern, media_type in self._MUSIC_QUERY_PATTERNS:
            match = pattern.match(original_text)
            if match is not None:
                query = match.group("query").strip()
                if self._normalize(query) == "no spotify":
                    return None
                return ParsedCommand(
                    Intent.PLAY_MUSIC,
                    original_text,
                    target="spotify",
                    query=query,
                    media_type=media_type,
                )

        return None

    def _parse_note_command(
        self, original_text: str, normalized_text: str
    ) -> Optional[ParsedCommand]:
        create_match = self._CREATE_NOTE_PATTERN.match(original_text)
        if create_match is not None:
            return ParsedCommand(
                intent=Intent.CREATE_NOTE,
                original_text=original_text,
                content=create_match.group("content").strip(),
            )

        if normalized_text in self._CREATE_NOTE_PREFIXES:
            return ParsedCommand(Intent.CREATE_NOTE, original_text)

        if normalized_text in self._LIST_NOTES_COMMANDS:
            return ParsedCommand(Intent.LIST_NOTES, original_text)

        delete_match = self._DELETE_NOTE_PATTERN.match(original_text)
        if delete_match is not None:
            raw_note_number = (delete_match.group("number") or "").strip()
            is_integer = raw_note_number.lstrip("+-").isdigit()
            note_number = int(raw_note_number) if is_integer else None
            return ParsedCommand(
                Intent.DELETE_NOTE,
                original_text,
                note_number=note_number,
            )

        return None

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
