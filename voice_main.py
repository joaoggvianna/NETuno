"""Push-to-talk entry point for the NETuno local voice interface."""

import math
import os

from database.database import initialize_database
from voice.audio import MicrophoneRecorder
from voice.stt import WhisperSpeechToText
from voice.tts import TextToSpeech
from voice.voice_assistant import VoiceAssistant


def _recording_duration() -> float:
    raw_duration = os.getenv("NETUNO_VOICE_DURATION", "5")
    try:
        duration = float(raw_duration)
    except ValueError:
        return 5.0
    return duration if math.isfinite(duration) and duration > 0 else 5.0


def main() -> None:
    """Run the explicit push-to-talk voice loop."""
    initialize_database()
    voice_assistant = VoiceAssistant(
        recorder=MicrophoneRecorder(duration_seconds=_recording_duration()),
        transcriber=WhisperSpeechToText(),
        speaker=TextToSpeech(),
    )

    print("NETuno Voice\n")
    while True:
        try:
            input("Pressione ENTER para falar. ")
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais.")
            break

        print("Ouvindo...")
        result = voice_assistant.process_once()
        print()
        if result is not None and result.should_exit:
            break


if __name__ == "__main__":
    main()
