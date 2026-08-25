"""Coordinate the local voice pipeline with the existing NETuno Core."""

import re
from typing import Callable, Optional

from core.assistant import Assistant
from core.models import CommandResult
from voice.audio import AudioCaptureError, MicrophoneRecorder
from voice.stt import SpeechToTextError, WhisperSpeechToText
from voice.tts import TextToSpeech, TextToSpeechError


_NETUNO_PREFIX = re.compile(r"^\s*netuno\b\s*,?\s*", re.IGNORECASE)


def remove_netuno_prefix(text: str) -> str:
    """Remove one optional spoken NETuno prefix from a command."""
    return _NETUNO_PREFIX.sub("", text, count=1).strip()


class VoiceAssistant:
    """Run one push-to-talk interaction through the existing Assistant."""

    def __init__(
        self,
        recorder: MicrophoneRecorder,
        transcriber: WhisperSpeechToText,
        speaker: TextToSpeech,
        assistant: Optional[Assistant] = None,
        output: Callable[[str], None] = print,
    ) -> None:
        self._recorder = recorder
        self._transcriber = transcriber
        self._speaker = speaker
        self._assistant = assistant or Assistant()
        self._output = output

    def process_once(self) -> Optional[CommandResult]:
        """Capture, transcribe, process and speak a single command."""
        try:
            recording = self._recorder.record()
        except AudioCaptureError as error:
            self._output(f"NETuno: {error}")
            return None

        try:
            transcription = self._transcriber.transcribe(recording)
        except SpeechToTextError as error:
            self._output(f"NETuno: {error}")
            return None

        command_text = remove_netuno_prefix(transcription)
        if not command_text:
            self._output("NETuno: Não identifiquei fala no áudio.")
            return None

        self._output(f"Você: {transcription.strip()}")
        result = self._assistant.process_command(command_text)
        self._output(f"NETuno: {result.message}")

        try:
            self._speaker.speak(result.message)
        except TextToSpeechError as error:
            self._output(f"Aviso: {error}")

        return result
