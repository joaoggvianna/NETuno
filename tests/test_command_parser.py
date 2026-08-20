import unittest

from core.command_parser import CommandParser
from core.models import Intent


class CommandParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CommandParser()

    def test_parses_time_command_with_accents(self) -> None:
        command = self.parser.parse("Que horas são?")
        self.assertEqual(command.intent, Intent.GET_TIME)

    def test_parses_date_command(self) -> None:
        command = self.parser.parse("qual a data de hoje")
        self.assertEqual(command.intent, Intent.GET_DATE)

    def test_parses_system_status_aliases(self) -> None:
        aliases = (
            "status do computador",
            "status do PC",
            "Como está o computador?",
            "como está o pc",
            "uso do computador",
        )

        for alias in aliases:
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.GET_SYSTEM_STATUS)

    def test_parses_exit_command(self) -> None:
        for alias in ("Fechar NETuno!", "Fechar Jarvis!"):
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.EXIT)

    def test_parses_vscode_aliases_and_extracts_target(self) -> None:
        aliases = (
            "abrir vscode",
            "abre vscode",
            "iniciar vscode",
            "abrir visual studio code",
        )

        for alias in aliases:
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.OPEN_APP)
                self.assertEqual(command.target, "vscode")

    def test_parses_spotify_aliases_and_extracts_target(self) -> None:
        for alias in ("abrir spotify", "abre spotify", "iniciar spotify"):
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.OPEN_APP)
                self.assertEqual(command.target, "spotify")

    def test_parses_youtube_aliases_and_extracts_target(self) -> None:
        for alias in ("abrir youtube", "abre youtube", "ir para youtube"):
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.OPEN_WEBSITE)
                self.assertEqual(command.target, "youtube")

    def test_parses_create_note_and_extracts_content(self) -> None:
        command = self.parser.parse("criar nota comprar pão")

        self.assertEqual(command.intent, Intent.CREATE_NOTE)
        self.assertEqual(command.content, "comprar pão")

    def test_parses_create_note_aliases(self) -> None:
        for alias in ("anotar revisar banco", "nova nota estudar Python"):
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.CREATE_NOTE)
                self.assertIsNotNone(command.content)

    def test_parses_list_notes_aliases(self) -> None:
        for alias in ("listar notas", "mostrar notas", "minhas notas"):
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.LIST_NOTES)

    def test_parses_delete_note_and_extracts_id(self) -> None:
        command = self.parser.parse("remover nota 3")

        self.assertEqual(command.intent, Intent.DELETE_NOTE)
        self.assertEqual(command.note_number, 3)

    def test_delete_note_without_valid_id_does_not_raise(self) -> None:
        for text in ("remover nota", "apagar nota abc"):
            with self.subTest(text=text):
                command = self.parser.parse(text)
                self.assertEqual(command.intent, Intent.DELETE_NOTE)
                self.assertIsNone(command.note_number)

    def test_preserves_negative_note_number_for_validation(self) -> None:
        command = self.parser.parse("remover nota -1")

        self.assertEqual(command.intent, Intent.DELETE_NOTE)
        self.assertEqual(command.note_number, -1)

    def test_parses_study_mode_aliases(self) -> None:
        aliases = (
            "modo estudo",
            "iniciar modo estudo",
            "começar modo estudo",
            "hora de estudar",
        )

        for alias in aliases:
            with self.subTest(alias=alias):
                command = self.parser.parse(alias)
                self.assertEqual(command.intent, Intent.RUN_MODE)
                self.assertEqual(command.target, "study")

    def test_parses_supported_composite_commands(self) -> None:
        expected_targets = {
            "abrir vscode e spotify": "vscode_spotify",
            "abrir spotify e youtube": "spotify_youtube",
        }

        for text, target in expected_targets.items():
            with self.subTest(text=text):
                command = self.parser.parse(text)
                self.assertEqual(command.intent, Intent.RUN_MODE)
                self.assertEqual(command.target, target)

    def test_parses_music_control_aliases(self) -> None:
        expected_intents = {
            "tocar música": Intent.PLAY_MUSIC,
            "continuar música": Intent.RESUME_MUSIC,
            "voltar música": Intent.PREVIOUS_TRACK,
            "pausar música": Intent.PAUSE_MUSIC,
            "pausar spotify": Intent.PAUSE_MUSIC,
            "próxima música": Intent.NEXT_TRACK,
            "próxima faixa": Intent.NEXT_TRACK,
            "pular música": Intent.NEXT_TRACK,
            "música anterior": Intent.PREVIOUS_TRACK,
            "faixa anterior": Intent.PREVIOUS_TRACK,
            "voltar faixa": Intent.PREVIOUS_TRACK,
        }

        for text, intent in expected_intents.items():
            with self.subTest(text=text):
                command = self.parser.parse(text)
                self.assertEqual(command.intent, intent)
                self.assertEqual(command.target, "spotify")

    def test_extracts_music_query_and_explicit_media_type(self) -> None:
        examples = {
            "toque a música Everlong": ("Everlong", "track"),
            "toque o álbum Songs for the Deaf": (
                "Songs for the Deaf",
                "album",
            ),
            "toque o artista Foo Fighters": ("Foo Fighters", "artist"),
            "toque Everlong no Spotify": ("Everlong", None),
            "toque Foo Fighters": ("Foo Fighters", None),
        }

        for text, (query, media_type) in examples.items():
            with self.subTest(text=text):
                command = self.parser.parse(text)
                self.assertEqual(command.intent, Intent.PLAY_MUSIC)
                self.assertEqual(command.target, "spotify")
                self.assertEqual(command.query, query)
                self.assertEqual(command.media_type, media_type)

    def test_returns_unknown_when_spotify_query_is_missing(self) -> None:
        command = self.parser.parse("toque no spotify")

        self.assertEqual(command.intent, Intent.UNKNOWN)
        self.assertIsNone(command.query)

    def test_returns_unknown_for_unsupported_command(self) -> None:
        command = self.parser.parse("faça café")
        self.assertEqual(command.intent, Intent.UNKNOWN)
        self.assertIsNone(command.target)


if __name__ == "__main__":
    unittest.main()
