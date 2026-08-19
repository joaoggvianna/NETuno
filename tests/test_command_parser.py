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
        command = self.parser.parse("  Fechar Jarvis! ")
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

    def test_returns_unknown_for_unsupported_command(self) -> None:
        command = self.parser.parse("faça café")
        self.assertEqual(command.intent, Intent.UNKNOWN)
        self.assertIsNone(command.target)


if __name__ == "__main__":
    unittest.main()
