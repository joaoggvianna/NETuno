import unittest
from types import SimpleNamespace
from unittest.mock import patch

from voice.audio import AudioRecording
from voice.stt import SpeechToTextError, WhisperSpeechToText


class FakeWhisperModel:
    def __init__(self, segments=None, error=None) -> None:
        self.segments = segments or []
        self.error = error
        self.call = None

    def transcribe(self, samples, **kwargs):
        if self.error:
            raise self.error
        self.call = (samples, kwargs)
        return iter(self.segments), SimpleNamespace()


class WhisperSpeechToTextTestCase(unittest.TestCase):
    def test_transcribes_audio_without_interpreting_it(self):
        model = FakeWhisperModel(
            [SimpleNamespace(text=" que horas"), SimpleNamespace(text="são ")]
        )
        factory_calls = []

        def factory(*args, **kwargs):
            factory_calls.append((args, kwargs))
            return model

        transcriber = WhisperSpeechToText(
            model_name="tiny", language="pt", model_factory=factory
        )
        samples = object()

        text = transcriber.transcribe(AudioRecording(samples, 16_000))

        self.assertEqual(text, "que horas são")
        self.assertEqual(factory_calls[0][0], ("tiny",))
        self.assertEqual(factory_calls[0][1]["compute_type"], "int8")
        self.assertIs(model.call[0], samples)
        self.assertTrue(model.call[1]["vad_filter"])
        self.assertEqual(model.call[1]["beam_size"], 5)
        self.assertFalse(model.call[1]["condition_on_previous_text"])
        self.assertIn("abrir Spotify", model.call[1]["initial_prompt"])

    def test_uses_base_model_by_default(self):
        model = FakeWhisperModel([])
        factory_calls = []

        def factory(*args, **kwargs):
            factory_calls.append((args, kwargs))
            return model

        with patch.dict("os.environ", {}, clear=True):
            transcriber = WhisperSpeechToText(model_factory=factory)
            transcriber.transcribe(AudioRecording(object(), 16_000))

        self.assertEqual(factory_calls[0][0], ("base",))

    def test_returns_empty_text_when_no_speech_is_recognized(self):
        model = FakeWhisperModel([])
        transcriber = WhisperSpeechToText(model_factory=lambda *args, **kwargs: model)

        text = transcriber.transcribe(AudioRecording(object(), 16_000))

        self.assertEqual(text, "")

    def test_wraps_stt_failure(self):
        model = FakeWhisperModel(error=RuntimeError("model failed"))
        transcriber = WhisperSpeechToText(model_factory=lambda *args, **kwargs: model)

        with self.assertRaisesRegex(
            SpeechToTextError, "Não foi possível transcrever o áudio"
        ):
            transcriber.transcribe(AudioRecording(object(), 16_000))


if __name__ == "__main__":
    unittest.main()
