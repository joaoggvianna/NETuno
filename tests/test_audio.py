import unittest

from voice.audio import MicrophoneRecorder, MicrophoneUnavailableError


class FakeSamples:
    def __init__(self) -> None:
        self.was_flattened = False

    def reshape(self, size: int):
        self.was_flattened = size == -1
        return self


class FakeSoundDevice:
    def __init__(self, samples=None, error=None) -> None:
        self.samples = samples or FakeSamples()
        self.error = error
        self.record_call = None
        self.waited = False

    def query_devices(self, kind):
        if self.error:
            raise self.error
        return {"kind": kind}

    def rec(self, frames, **kwargs):
        self.record_call = (frames, kwargs)
        return self.samples

    def wait(self):
        self.waited = True


class MicrophoneRecorderTestCase(unittest.TestCase):
    def test_captures_audio_in_memory_with_duration_limit(self):
        backend = FakeSoundDevice()
        recorder = MicrophoneRecorder(
            duration_seconds=2.5,
            sample_rate=16_000,
            sounddevice_module=backend,
        )

        recording = recorder.record()

        self.assertEqual(backend.record_call[0], 40_000)
        self.assertEqual(backend.record_call[1]["channels"], 1)
        self.assertEqual(backend.record_call[1]["dtype"], "float32")
        self.assertTrue(backend.waited)
        self.assertTrue(recording.samples.was_flattened)
        self.assertEqual(recording.sample_rate, 16_000)

    def test_reports_unavailable_microphone(self):
        recorder = MicrophoneRecorder(
            sounddevice_module=FakeSoundDevice(error=RuntimeError("no device"))
        )

        with self.assertRaisesRegex(
            MicrophoneUnavailableError, "Não foi possível acessar o microfone"
        ):
            recorder.record()


if __name__ == "__main__":
    unittest.main()
