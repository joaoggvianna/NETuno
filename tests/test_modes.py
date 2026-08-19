import unittest
from unittest.mock import patch

from commands.modes import run_mode
from core.models import CommandResult, Intent, ParsedCommand


class ModesTestCase(unittest.TestCase):
    @patch("commands.modes.open_website")
    @patch("commands.modes.open_app")
    def test_runs_study_mode_in_order(self, open_app_mock, open_website_mock) -> None:
        calls = []

        def open_app(command: ParsedCommand) -> CommandResult:
            calls.append((command.intent, command.target))
            return CommandResult(True, "Aplicativo aberto.")

        def open_website(command: ParsedCommand) -> CommandResult:
            calls.append((command.intent, command.target))
            return CommandResult(True, "Site aberto.")

        open_app_mock.side_effect = open_app
        open_website_mock.side_effect = open_website

        result = run_mode(ParsedCommand(Intent.RUN_MODE, "modo estudo", "study"))

        self.assertTrue(result.success)
        self.assertEqual(
            calls,
            [
                (Intent.OPEN_APP, "vscode"),
                (Intent.OPEN_APP, "spotify"),
                (Intent.OPEN_WEBSITE, "study"),
            ],
        )
        self.assertIn("Modo estudo iniciado.", result.message)
        self.assertIn("✓ Visual Studio Code", result.message)
        self.assertIn("✓ Spotify", result.message)
        self.assertIn("✓ ambiente de estudo", result.message)

    @patch("commands.modes.open_website", return_value=CommandResult(True, "Site aberto."))
    @patch("commands.modes.open_app")
    def test_continues_after_partial_failure(
        self, open_app_mock, open_website_mock
    ) -> None:
        open_app_mock.side_effect = (
            CommandResult(True, "VS Code aberto."),
            CommandResult(False, "Aplicativo não encontrado."),
        )

        result = run_mode(ParsedCommand(Intent.RUN_MODE, "modo estudo", "study"))

        self.assertFalse(result.success)
        self.assertIn("Modo estudo iniciado parcialmente.", result.message)
        self.assertIn("✗ Spotify: Aplicativo não encontrado.", result.message)
        open_website_mock.assert_called_once()

    @patch("commands.modes.open_website")
    @patch("commands.modes.open_app", return_value=CommandResult(True, "Aberto."))
    def test_runs_spotify_and_youtube_composite(
        self, open_app_mock, open_website_mock
    ) -> None:
        open_website_mock.return_value = CommandResult(True, "Aberto.")

        result = run_mode(
            ParsedCommand(
                Intent.RUN_MODE,
                "abrir spotify e youtube",
                "spotify_youtube",
            )
        )

        self.assertTrue(result.success)
        self.assertEqual(open_app_mock.call_args.args[0].target, "spotify")
        self.assertEqual(open_website_mock.call_args.args[0].target, "youtube")


if __name__ == "__main__":
    unittest.main()
