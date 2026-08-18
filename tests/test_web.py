import unittest
from unittest.mock import patch

from commands.web import open_website
from core.models import Intent, ParsedCommand


class OpenWebsiteTestCase(unittest.TestCase):
    @patch("commands.web.webbrowser.open", return_value=True)
    def test_opens_youtube_in_default_browser(self, open_mock) -> None:
        command = ParsedCommand(Intent.OPEN_WEBSITE, "abrir youtube", "youtube")

        result = open_website(command)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Abrindo YouTube.")
        open_mock.assert_called_once_with("https://www.youtube.com", new=2)

    @patch("commands.web.webbrowser.open", return_value=False)
    def test_returns_clear_error_when_browser_cannot_open(self, open_mock) -> None:
        command = ParsedCommand(Intent.OPEN_WEBSITE, "abrir youtube", "youtube")

        result = open_website(command)

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Não foi possível abrir o navegador.")


if __name__ == "__main__":
    unittest.main()
