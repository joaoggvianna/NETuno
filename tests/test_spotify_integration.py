import subprocess
import unittest
from unittest.mock import patch

from integrations.spotify import SpotifyError, SpotifyIntegration


class SpotifyIntegrationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.spotify = SpotifyIntegration()

    @patch("integrations.spotify.subprocess.run")
    @patch("integrations.spotify.SPOTIFY_APP_PATH")
    @patch("integrations.spotify.platform.system", return_value="Darwin")
    def test_runs_static_playback_commands(
        self, system_mock, app_path_mock, run_mock
    ) -> None:
        app_path_mock.is_dir.return_value = True
        actions = (
            (self.spotify.play, 'tell application "Spotify" to play'),
            (self.spotify.pause, 'tell application "Spotify" to pause'),
            (self.spotify.next_track, 'tell application "Spotify" to next track'),
            (
                self.spotify.previous_track,
                'tell application "Spotify" to previous track',
            ),
        )

        for action, script in actions:
            with self.subTest(script=script):
                action()
                run_mock.assert_called_with(
                    ["osascript", "-e", script],
                    check=True,
                    capture_output=True,
                )

    @patch("integrations.spotify.subprocess.run")
    @patch("integrations.spotify.SPOTIFY_APP_PATH")
    @patch("integrations.spotify.platform.system", return_value="Darwin")
    def test_opens_encoded_search_without_shell(
        self, system_mock, app_path_mock, run_mock
    ) -> None:
        app_path_mock.is_dir.return_value = True
        self.spotify.open_search("Songs for the Deaf")

        run_mock.assert_called_once_with(
            ["open", "spotify:search:Songs%20for%20the%20Deaf"],
            check=True,
            capture_output=True,
        )

    @patch("integrations.spotify.platform.system", return_value="Linux")
    def test_reports_when_spotify_is_unavailable(self, system_mock) -> None:
        with self.assertRaisesRegex(SpotifyError, "Spotify não está disponível"):
            self.spotify.play()

    @patch("integrations.spotify.subprocess.run")
    @patch("integrations.spotify.SPOTIFY_APP_PATH")
    @patch("integrations.spotify.platform.system", return_value="Darwin")
    def test_wraps_local_control_errors(
        self, system_mock, app_path_mock, run_mock
    ) -> None:
        app_path_mock.is_dir.return_value = True
        run_mock.side_effect = subprocess.CalledProcessError(1, ["osascript"])

        with self.assertRaisesRegex(SpotifyError, "controlar o Spotify"):
            self.spotify.pause()


if __name__ == "__main__":
    unittest.main()
