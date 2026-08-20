import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from desktop_agent.app import app
from desktop_agent.executor import DesktopExecutor
from desktop_agent.schemas import ActionRequest, ActionResponse


class DesktopAgentApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "netuno-desktop-agent"},
        )

    @patch("desktop_agent.app.executor")
    def test_actions_uses_structured_request(self, executor_mock) -> None:
        executor_mock.execute.return_value = ActionResponse(success=True)

        response = self.client.post(
            "/actions",
            json={"action": "open_app", "target": "spotify"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        request = executor_mock.execute.call_args.args[0]
        self.assertEqual(request.action.value, "open_app")
        self.assertEqual(request.target.value, "spotify")

    def test_rejects_unknown_action(self) -> None:
        response = self.client.post(
            "/actions",
            json={"action": "run_shell", "command": "whoami"},
        )

        self.assertEqual(response.status_code, 422)

    def test_rejects_unsupported_app_target(self) -> None:
        response = self.client.post(
            "/actions",
            json={"action": "open_app", "target": "calculator"},
        )

        self.assertEqual(response.status_code, 422)

    def test_rejects_shell_field_even_for_valid_action(self) -> None:
        response = self.client.post(
            "/actions",
            json={
                "action": "open_app",
                "target": "spotify",
                "shell": "open -a Spotify",
            },
        )

        self.assertEqual(response.status_code, 422)


class DesktopExecutorTestCase(unittest.TestCase):
    @patch("desktop_agent.executor.subprocess.run")
    @patch("desktop_agent.executor.platform.system", return_value="Darwin")
    def test_opens_allowlisted_app_without_shell(
        self, system_mock, run_mock
    ) -> None:
        executor = DesktopExecutor()

        result = executor.execute(
            ActionRequest(action="open_app", target="vscode")
        )

        self.assertTrue(result.success)
        run_mock.assert_called_once_with(
            ["open", "-a", "Visual Studio Code"],
            check=True,
            capture_output=True,
        )

    @patch("desktop_agent.executor.psutil.boot_time", return_value=1_000.0)
    @patch("desktop_agent.executor.datetime")
    @patch("desktop_agent.executor.psutil.disk_usage")
    @patch("desktop_agent.executor.psutil.virtual_memory")
    @patch("desktop_agent.executor.psutil.cpu_percent", return_value=21.0)
    def test_returns_structured_system_status(
        self,
        cpu_percent,
        virtual_memory,
        disk_usage,
        mocked_datetime,
        boot_time,
    ) -> None:
        virtual_memory.return_value.percent = 63.0
        disk_usage.return_value.percent = 42.0
        mocked_datetime.now.return_value.timestamp.return_value = 12_880.0

        result = DesktopExecutor().execute(
            ActionRequest(action="get_system_status")
        )

        self.assertTrue(result.success)
        self.assertEqual(result.data.cpu_percent, 21.0)
        self.assertEqual(result.data.memory_percent, 63.0)
        self.assertEqual(result.data.disk_percent, 42.0)
        self.assertEqual(result.data.uptime_seconds, 11_880)

    def test_delegates_all_spotify_actions_to_existing_integration(self) -> None:
        spotify = MagicMock()
        executor = DesktopExecutor(spotify=spotify)
        examples = (
            (ActionRequest(action="spotify_play"), spotify.play),
            (ActionRequest(action="spotify_pause"), spotify.pause),
            (ActionRequest(action="spotify_next"), spotify.next_track),
            (ActionRequest(action="spotify_previous"), spotify.previous_track),
            (
                ActionRequest(action="spotify_search", query="Everlong"),
                spotify.open_search,
            ),
        )

        for request, integration_method in examples:
            with self.subTest(action=request.action):
                result = executor.execute(request)
                self.assertTrue(result.success)
                if request.query:
                    integration_method.assert_called_once_with("Everlong")
                else:
                    integration_method.assert_called_once_with()
                integration_method.reset_mock()


if __name__ == "__main__":
    unittest.main()
