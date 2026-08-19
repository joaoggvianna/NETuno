import unittest
from unittest.mock import patch

from commands.music import (
    next_track,
    pause_music,
    play_music,
    previous_track,
    resume_music,
)
from core.models import Intent, ParsedCommand
from integrations.spotify import SpotifyError


class MusicCommandsTestCase(unittest.TestCase):
    @patch("commands.music.spotify")
    def test_controls_playback_through_integration(self, spotify_mock) -> None:
        commands = (
            (play_music, Intent.PLAY_MUSIC, spotify_mock.play),
            (resume_music, Intent.RESUME_MUSIC, spotify_mock.play),
            (pause_music, Intent.PAUSE_MUSIC, spotify_mock.pause),
            (next_track, Intent.NEXT_TRACK, spotify_mock.next_track),
            (previous_track, Intent.PREVIOUS_TRACK, spotify_mock.previous_track),
        )

        for handler, intent, integration_method in commands:
            with self.subTest(intent=intent):
                result = handler(ParsedCommand(intent, "música", target="spotify"))
                self.assertTrue(result.success)
                integration_method.assert_called_once_with()
                integration_method.reset_mock()

    @patch("commands.music.spotify")
    def test_returns_integration_error(self, spotify_mock) -> None:
        spotify_mock.pause.side_effect = SpotifyError("Spotify indisponível.")

        result = pause_music(
            ParsedCommand(Intent.PAUSE_MUSIC, "pausar spotify", target="spotify")
        )

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Spotify indisponível.")

    @patch("commands.music.spotify")
    def test_opens_search_but_does_not_claim_playback(self, spotify_mock) -> None:
        command = ParsedCommand(
            Intent.PLAY_MUSIC,
            "toque a música Everlong",
            target="spotify",
            query="Everlong",
            media_type="track",
        )

        result = play_music(command)

        self.assertFalse(result.success)
        spotify_mock.open_search.assert_called_once_with("Everlong")
        self.assertIn('Abri a busca pela música "Everlong"', result.message)
        self.assertIn("não consegue iniciar", result.message)


if __name__ == "__main__":
    unittest.main()
