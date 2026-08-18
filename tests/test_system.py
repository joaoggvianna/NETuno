import unittest
from unittest.mock import patch

from commands.system import get_system_status
from core.models import Intent, ParsedCommand


class SystemCommandsTestCase(unittest.TestCase):
    @patch("commands.system.psutil.boot_time", return_value=1_000.0)
    @patch("commands.system.datetime")
    @patch("commands.system.psutil.disk_usage")
    @patch("commands.system.psutil.virtual_memory")
    @patch("commands.system.psutil.cpu_percent", return_value=27.4)
    def test_formats_system_status(
        self,
        cpu_percent,
        virtual_memory,
        disk_usage,
        mocked_datetime,
        boot_time,
    ) -> None:
        virtual_memory.return_value.percent = 63.2
        disk_usage.return_value.percent = 41.8
        mocked_datetime.now.return_value.timestamp.return_value = 91_061.0

        command = ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")
        result = get_system_status(command)

        self.assertTrue(result.success)
        self.assertEqual(
            result.message,
            "CPU: 27% | Memória: 63% | Disco: 42% | Ligado há: 1d 1h 1min",
        )

    @patch("commands.system.psutil.cpu_percent", side_effect=OSError)
    def test_returns_clear_error_when_metrics_cannot_be_read(self, cpu_percent) -> None:
        command = ParsedCommand(Intent.GET_SYSTEM_STATUS, "status do computador")

        result = get_system_status(command)

        self.assertFalse(result.success)
        self.assertEqual(
            result.message,
            "Não foi possível consultar o status do computador.",
        )


if __name__ == "__main__":
    unittest.main()
