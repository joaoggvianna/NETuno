"""Capture microphone audio without persisting recordings."""

from dataclasses import dataclass
from typing import Any, Optional


class AudioCaptureError(RuntimeError):
    """Raised when microphone audio cannot be captured."""


class MicrophoneUnavailableError(AudioCaptureError):
    """Raised when no usable input device is available."""


@dataclass(frozen=True)
class AudioRecording:
    """In-memory mono audio samples and their sample rate."""

    samples: Any
    sample_rate: int


class MicrophoneRecorder:
    """Record a short, fixed-duration command from the default microphone."""

    def __init__(
        self,
        duration_seconds: float = 5.0,
        sample_rate: int = 16_000,
        sounddevice_module: Optional[Any] = None,
    ) -> None:
        if duration_seconds <= 0:
            raise ValueError("A duração da gravação deve ser positiva.")

        self.duration_seconds = duration_seconds
        self.sample_rate = sample_rate
        self._sounddevice = sounddevice_module

    def record(self) -> AudioRecording:
        """Capture mono float32 samples from the default input device."""
        sounddevice = self._sounddevice or self._load_sounddevice()

        try:
            sounddevice.query_devices(kind="input")
            frame_count = int(self.duration_seconds * self.sample_rate)
            samples = sounddevice.rec(
                frame_count,
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
            )
            sounddevice.wait()
        except Exception as error:
            raise MicrophoneUnavailableError(
                "Não foi possível acessar o microfone."
            ) from error

        return AudioRecording(samples=samples.reshape(-1), sample_rate=self.sample_rate)

    @staticmethod
    def _load_sounddevice() -> Any:
        try:
            import sounddevice
        except ImportError as error:
            raise AudioCaptureError(
                "A dependência sounddevice não está instalada."
            ) from error
        return sounddevice
