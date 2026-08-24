import subprocess
import unittest
from unittest.mock import Mock

from voice.tts import TextToSpeech, TextToSpeechError


class TextToSpeechTestCase(unittest.TestCase):
    def test_speaks_exact_text(self):
        runner = Mock()
        speaker = TextToSpeech(
            runner=runner,
            system_name=lambda: "Darwin",
            executable_finder=lambda name: "/usr/bin/say",
        )

        speaker.speak("Agora são 10:30.")

        command = runner.call_args.args[0]
        self.assertEqual(command, ["/usr/bin/say", "Agora são 10:30."])
        self.assertNotIn("shell", runner.call_args.kwargs)

    def test_wraps_engine_failure(self):
        runner = Mock(side_effect=subprocess.CalledProcessError(1, ["say"]))
        speaker = TextToSpeech(
            runner=runner,
            system_name=lambda: "Darwin",
            executable_finder=lambda name: "/usr/bin/say",
        )

        with self.assertRaisesRegex(
            TextToSpeechError, "Não foi possível reproduzir a resposta"
        ):
            speaker.speak("Resposta")

    def test_reports_missing_local_engine(self):
        speaker = TextToSpeech(
            system_name=lambda: "Linux",
            executable_finder=lambda name: None,
        )

        with self.assertRaisesRegex(TextToSpeechError, "engine de voz local"):
            speaker.speak("Resposta")


if __name__ == "__main__":
    unittest.main()
