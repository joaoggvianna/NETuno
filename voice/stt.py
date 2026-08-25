"""Convert in-memory audio into text using a local Whisper model."""

import os
from typing import Any, Callable, Optional

from voice.audio import AudioRecording


class SpeechToTextError(RuntimeError):
    """Raised when local speech recognition fails."""


class WhisperSpeechToText:
    """Lazy local Speech-to-Text adapter backed by faster-whisper."""

    DEFAULT_PROMPT = (
        "Comandos em português para o assistente NETuno, como abrir Spotify, "
        "abrir VS Code, informar horas, data e status do computador."
    )

    def __init__(
        self,
        model_name: Optional[str] = None,
        language: Optional[str] = None,
        model_factory: Optional[Callable[..., Any]] = None,
    ) -> None:
        self.model_name = model_name or os.getenv("NETUNO_STT_MODEL", "base")
        self.language = language or os.getenv("NETUNO_STT_LANGUAGE", "pt")
        self._model_factory = model_factory
        self._model: Optional[Any] = None

    def transcribe(self, recording: AudioRecording) -> str:
        """Return recognized text, or an empty string when speech is absent."""
        try:
            model = self._get_model()
            segments, _ = model.transcribe(
                recording.samples,
                language=self.language,
                vad_filter=True,
                beam_size=5,
                condition_on_previous_text=False,
                initial_prompt=self.DEFAULT_PROMPT,
            )
            return " ".join(segment.text.strip() for segment in segments).strip()
        except SpeechToTextError:
            raise
        except Exception as error:
            raise SpeechToTextError("Não foi possível transcrever o áudio.") from error

    def _get_model(self) -> Any:
        if self._model is None:
            factory = self._model_factory or self._load_model_factory()
            self._model = factory(self.model_name, device="cpu", compute_type="int8")
        return self._model

    @staticmethod
    def _load_model_factory() -> Callable[..., Any]:
        try:
            from faster_whisper import WhisperModel
        except ImportError as error:
            raise SpeechToTextError(
                "A dependência faster-whisper não está instalada."
            ) from error
        return WhisperModel
