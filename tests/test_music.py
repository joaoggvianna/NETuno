import unittest
from unittest.mock import patch

from commands.music import (
    next_track,
    pause_music,
    play_music,
    previous_track,
    resume_music,
)
from core.agent_client import AgentResult, AgentUnavailableError
from core.models import Intent, ParsedCommand


class MusicCommandsTestCase(unittest.TestCase):
    @patch("commands.music.agent_client")
    def test_delegates_playback_controls_to_agent(self, agent_client_mock) -> None:
        agent_client_mock.spotify_play.return_value = AgentResult(True)
        agent_client_mock.spotify_pause.return_value = AgentResult(True)
        agent_client_mock.spotify_next.return_value = AgentResult(True)
        agent_client_mock.spotify_previous.return_value = AgentResult(True)
        commands = (
            (play_music, Intent.PLAY_MUSIC, "spotify_play"),
            (resume_music, Intent.RESUME_MUSIC, "spotify_play"),
            (pause_music, Intent.PAUSE_MUSIC, "spotify_pause"),
            (next_track, Intent.NEXT_TRACK, "spotify_next"),
            (previous_track, Intent.PREVIOUS_TRACK, "spotify_previous"),
        )

        for handler, intent, method_name in commands:
            with self.subTest(intent=intent):
                result = handler(ParsedCommand(intent, "música", target="spotify"))
                self.assertTrue(result.success)
                getattr(agent_client_mock, method_name).assert_called_once_with()
                getattr(agent_client_mock, method_name).reset_mock()

    @patch("commands.music.agent_client")
    def test_returns_agent_execution_error(self, agent_client_mock) -> None:
        agent_client_mock.spotify_pause.return_value = AgentResult(
            False,
            "Spotify indisponível.",
            "execution_error",
        )

        result = pause_music(
            ParsedCommand(Intent.PAUSE_MUSIC, "pausar spotify", target="spotify")
        )

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Spotify indisponível.")

    @patch("commands.music.agent_client")
    def test_opens_search_but_does_not_claim_playback(
        self, agent_client_mock
    ) -> None:
        agent_client_mock.spotify_search.return_value = AgentResult(True)
        command = ParsedCommand(
            Intent.PLAY_MUSIC,
            "toque a música Everlong",
            target="spotify",
            query="Everlong",
            media_type="track",
        )

        result = play_music(command)

        self.assertFalse(result.success)
        agent_client_mock.spotify_search.assert_called_once_with("Everlong")
        self.assertIn('Abri a busca pela música "Everlong"', result.message)
        self.assertIn("não consegue iniciar", result.message)

    @patch("commands.music.agent_client")
    def test_returns_friendly_error_when_agent_is_offline(
        self, agent_client_mock
    ) -> None:
        agent_client_mock.spotify_pause.side_effect = AgentUnavailableError(
            "O NETuno Desktop Agent não está disponível."
        )

        result = pause_music(
            ParsedCommand(Intent.PAUSE_MUSIC, "pausar spotify", target="spotify")
        )

        self.assertFalse(result.success)
        self.assertEqual(
            result.message,
            "O NETuno Desktop Agent não está disponível.",
        )


if __name__ == "__main__":
    unittest.main()
