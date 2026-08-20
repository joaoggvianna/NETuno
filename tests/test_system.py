import unittest
from unittest.mock import patch

from commands.system import get_system_status
from core.agent_client import AgentResult, AgentUnavailableError
from core.models import Intent, ParsedCommand


class SystemCommandsTestCase(unittest.TestCase):
    @patch("commands.system.agent_client")
    def test_formats_system_status_from_agent_data(self, agent_client_mock) -> None:
        agent_client_mock.get_system_status.return_value = AgentResult(
            True,
            data={
                "cpu_percent": 27.4,
                "memory_percent": 63.2,
                "disk_percent": 41.8,
                "uptime_seconds": 90_061,
            },
        )

        result = get_system_status(
            ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")
        )

        self.assertTrue(result.success)
        self.assertEqual(
            result.message,
            "CPU: 27% | Memória: 63% | Disco: 42% | Ligado há: 1d 1h 1min",
        )
        agent_client_mock.get_system_status.assert_called_once_with()

    @patch("commands.system.agent_client")
    def test_returns_agent_execution_error(self, agent_client_mock) -> None:
        agent_client_mock.get_system_status.return_value = AgentResult(
            False,
            "Não foi possível consultar o status do computador.",
            "execution_error",
        )

        result = get_system_status(
            ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.message,
            "Não foi possível consultar o status do computador.",
        )

    @patch("commands.system.agent_client")
    def test_returns_friendly_error_when_agent_is_offline(
        self, agent_client_mock
    ) -> None:
        agent_client_mock.get_system_status.side_effect = AgentUnavailableError(
            "O NETuno Desktop Agent não está disponível."
        )

        result = get_system_status(
            ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.message,
            "O NETuno Desktop Agent não está disponível.",
        )


if __name__ == "__main__":
    unittest.main()
