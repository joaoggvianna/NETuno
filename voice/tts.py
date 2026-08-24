"""Speak NETuno responses with local operating-system tools."""

import os
import platform
import shutil
import subprocess
from typing import Callable, Dict, List, Optional, Tuple


class TextToSpeechError(RuntimeError):
    """Raised when a response cannot be spoken."""


class TextToSpeech:
    """Small cross-platform adapter for local system speech synthesis."""

    def __init__(
        self,
        runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
        system_name: Callable[[], str] = platform.system,
        executable_finder: Callable[[str], Optional[str]] = shutil.which,
    ) -> None:
        self._runner = runner
        self._system_name = system_name
        self._find_executable = executable_finder

    def speak(self, text: str) -> None:
        """Speak non-empty text synchronously."""
        if not text.strip():
            return

        command, environment = self._build_command(text)
        try:
            self._runner(
                command,
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
        except (OSError, subprocess.CalledProcessError) as error:
            raise TextToSpeechError("Não foi possível reproduzir a resposta.") from error

    def _build_command(self, text: str) -> Tuple[List[str], Optional[Dict[str, str]]]:
        system = self._system_name()

        if system == "Darwin":
            return [self._required_executable("say"), text], None

        if system == "Windows":
            executable = self._find_executable("powershell") or self._find_executable(
                "pwsh"
            )
            if executable is None:
                raise TextToSpeechError("Nenhuma engine de voz local foi encontrada.")
            script = (
                "Add-Type -AssemblyName System.Speech; "
                "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                "$speaker.Speak($env:NETUNO_TTS_TEXT)"
            )
            environment = os.environ.copy()
            environment["NETUNO_TTS_TEXT"] = text
            return [executable, "-NoProfile", "-Command", script], environment

        if system == "Linux":
            executable = self._find_executable("espeak") or self._find_executable("spd-say")
            if executable is None:
                raise TextToSpeechError("Nenhuma engine de voz local foi encontrada.")
            return [executable, text], None

        raise TextToSpeechError("O sistema operacional não possui suporte de voz.")

    def _required_executable(self, name: str) -> str:
        executable = self._find_executable(name)
        if executable is None:
            raise TextToSpeechError("Nenhuma engine de voz local foi encontrada.")
        return executable
