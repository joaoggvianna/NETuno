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

    def test_returns_unknown_for_unsupported_command(self) -> None:
        command = self.parser.parse("faça café")

        self.assertEqual(command.intent, Intent.UNKNOWN)
        self.assertIsNone(command.target)


if __name__ == "__main__":
    unittest.main()
