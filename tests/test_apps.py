import subprocess
import unittest
from unittest.mock import patch

from commands.apps import open_app
from core.models import Intent, ParsedCommand


class OpenAppTestCase(unittest.TestCase):
    @patch("commands.apps.subprocess.run")
    @patch("commands.apps.platform.system", return_value="Darwin")
    def test_opens_vscode_without_using_shell(self, system_mock, run_mock) -> None:
        command = ParsedCommand(Intent.OPEN_APP, "abrir vscode", "vscode")

        result = open_app(command)

        self.assertTrue(result.success)
        run_mock.assert_called_once_with(
            ["open", "-a", "Visual Studio Code"],
            check=True,
            capture_output=True,
        )

    @patch("commands.apps.subprocess.run")
    @patch("commands.apps.platform.system", return_value="Darwin")
    def test_opens_spotify(self, system_mock, run_mock) -> None:
        command = ParsedCommand(Intent.OPEN_APP, "abrir spotify", "spotify")

        result = open_app(command)

        self.assertTrue(result.success)
        run_mock.assert_called_once_with(
            ["open", "-a", "Spotify"],
            check=True,
            capture_output=True,
        )

    @patch("commands.apps.subprocess.run")
    @patch("commands.apps.platform.system", return_value="Darwin")
    def test_returns_clear_error_when_app_cannot_open(
        self, system_mock, run_mock
    ) -> None:
        run_mock.side_effect = subprocess.CalledProcessError(1, ["open"])
        command = ParsedCommand(Intent.OPEN_APP, "abrir spotify", "spotify")

        result = open_app(command)

        self.assertFalse(result.success)
        self.assertIn("Verifique se o aplicativo está instalado", result.message)


if __name__ == "__main__":
    unittest.main()
