import unittest
from unittest.mock import patch

from commands.apps import open_app
from core.agent_client import AgentResult, AgentUnavailableError
from core.models import Intent, ParsedCommand


class OpenAppTestCase(unittest.TestCase):
    @patch("commands.apps.get_agent_client")
    def test_delegates_vscode_to_desktop_agent(self, get_client_mock) -> None:
        client = get_client_mock.return_value
        client.open_app.return_value = AgentResult(True)
        command = ParsedCommand(Intent.OPEN_APP, "abrir vscode", "vscode")

        result = open_app(command)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Abrindo Visual Studio Code.")
        client.open_app.assert_called_once_with("vscode")

    @patch("commands.apps.get_agent_client")
    def test_returns_agent_execution_error(self, get_client_mock) -> None:
        get_client_mock.return_value.open_app.return_value = AgentResult(
            False,
            "Spotify não está instalado.",
            "execution_error",
        )

        result = open_app(
            ParsedCommand(Intent.OPEN_APP, "abrir spotify", "spotify")
        )

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Spotify não está instalado.")

    @patch("commands.apps.get_agent_client")
    def test_returns_friendly_error_when_agent_is_offline(
        self, get_client_mock
    ) -> None:
        get_client_mock.return_value.open_app.side_effect = AgentUnavailableError(
            "O NETuno Desktop Agent não está disponível."
        )

        result = open_app(
            ParsedCommand(Intent.OPEN_APP, "abrir spotify", "spotify")
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.message,
            "O NETuno Desktop Agent não está disponível.",
        )

    @patch("commands.apps.get_agent_client")
    def test_rejects_unsupported_app_before_calling_agent(
        self, get_client_mock
    ) -> None:
        result = open_app(
            ParsedCommand(Intent.OPEN_APP, "abrir calculadora", "calculator")
        )

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Aplicativo não suportado.")
        get_client_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
