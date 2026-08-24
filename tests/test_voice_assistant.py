import unittest
from unittest.mock import Mock

from core.models import CommandResult
from voice.audio import AudioRecording, MicrophoneUnavailableError
from voice.stt import SpeechToTextError
from voice.tts import TextToSpeechError
from voice.voice_assistant import VoiceAssistant, remove_netuno_prefix


class VoiceAssistantTestCase(unittest.TestCase):
    def setUp(self):
        self.recording = AudioRecording(samples=object(), sample_rate=16_000)
        self.recorder = Mock()
        self.recorder.record.return_value = self.recording
        self.transcriber = Mock()
        self.speaker = Mock()
        self.assistant = Mock()
        self.output = Mock()
        self.voice = VoiceAssistant(
            recorder=self.recorder,
            transcriber=self.transcriber,
            speaker=self.speaker,
            assistant=self.assistant,
            output=self.output,
        )

    def test_sends_exact_transcription_to_core_and_result_message_to_tts(self):
        self.transcriber.transcribe.return_value = "que horas são"
        result = CommandResult(True, "Agora são 10:30.")
        self.assistant.process_command.return_value = result

        returned = self.voice.process_once()

        self.transcriber.transcribe.assert_called_once_with(self.recording)
        self.assistant.process_command.assert_called_once_with("que horas são")
        self.speaker.speak.assert_called_once_with("Agora são 10:30.")
        self.assertIs(returned, result)

    def test_removes_optional_netuno_prefix_before_core(self):
        self.transcriber.transcribe.return_value = "NETuno, abrir Spotify"
        self.assistant.process_command.return_value = CommandResult(
            True, "Abrindo Spotify."
        )

        self.voice.process_once()

        self.assistant.process_command.assert_called_once_with("abrir Spotify")

    def test_does_not_call_core_when_there_is_no_speech(self):
        self.transcriber.transcribe.return_value = "   "

        result = self.voice.process_once()

        self.assertIsNone(result)
        self.assistant.process_command.assert_not_called()
        self.speaker.speak.assert_not_called()

    def test_handles_microphone_error(self):
        self.recorder.record.side_effect = MicrophoneUnavailableError("sem microfone")

        result = self.voice.process_once()

        self.assertIsNone(result)
        self.transcriber.transcribe.assert_not_called()
        self.assistant.process_command.assert_not_called()

    def test_handles_stt_error(self):
        self.transcriber.transcribe.side_effect = SpeechToTextError("falha no STT")

        result = self.voice.process_once()

        self.assertIsNone(result)
        self.assistant.process_command.assert_not_called()
        self.speaker.speak.assert_not_called()

    def test_tts_failure_does_not_discard_core_result(self):
        self.transcriber.transcribe.return_value = "listar notas"
        result = CommandResult(True, "Nenhuma nota encontrada.")
        self.assistant.process_command.return_value = result
        self.speaker.speak.side_effect = TextToSpeechError("sem saída de áudio")

        returned = self.voice.process_once()

        self.assertIs(returned, result)
        self.assistant.process_command.assert_called_once_with("listar notas")
        self.output.assert_any_call("Aviso: sem saída de áudio")

    def test_prefix_helper_only_removes_leading_name(self):
        self.assertEqual(remove_netuno_prefix("netuno abra o Spotify"), "abra o Spotify")
        self.assertEqual(remove_netuno_prefix("abrir NETuno"), "abrir NETuno")


if __name__ == "__main__":
    unittest.main()
