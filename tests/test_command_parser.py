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

    def test_returns_unknown_for_unsupported_command(self) -> None:
        command = self.parser.parse("faça café")

        self.assertEqual(command.intent, Intent.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
