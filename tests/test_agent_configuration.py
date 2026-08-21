import importlib
import os
import unittest
from unittest.mock import patch

import api.app as api_app
import commands.apps as apps
import commands.music as music
import commands.system as system
from commands.notes import list_notes
from core.models import Intent, ParsedCommand


class InvalidAgentConfigurationTestCase(unittest.TestCase):
    def test_invalid_url_does_not_break_core_import_or_local_commands(self) -> None:
        with patch.dict(
            os.environ,
            {"NETUNO_AGENT_URL": "http://192.168.0.10:8001"},
        ):
            importlib.reload(apps)
            importlib.reload(music)
            importlib.reload(system)
            importlib.reload(api_app)

            time_result = system.get_current_time(
                ParsedCommand(Intent.GET_TIME, "que horas são")
            )
            with patch(
                "commands.notes.list_notes_from_database",
                return_value=[],
            ):
                notes_result = list_notes(
                    ParsedCommand(Intent.LIST_NOTES, "listar notas")
                )
            agent_result = apps.open_app(
                ParsedCommand(Intent.OPEN_APP, "abrir spotify", "spotify")
            )

        self.assertTrue(time_result.success)
        self.assertTrue(notes_result.success)
        self.assertFalse(agent_result.success)
        self.assertEqual(
            agent_result.message,
            "A configuração do NETuno Desktop Agent é inválida.",
        )


if __name__ == "__main__":
    unittest.main()
