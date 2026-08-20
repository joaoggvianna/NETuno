import os
import unittest
from unittest.mock import MagicMock, patch

import httpx

from core.agent_client import (
    AgentClient,
    AgentUnavailableError,
    InvalidAgentResponseError,
)


class AgentClientTestCase(unittest.TestCase):
    @patch("core.agent_client.httpx.post")
    def test_uses_configured_url_and_serializes_action(self, post_mock) -> None:
        response = MagicMock()
        response.json.return_value = {"success": True, "data": None}
        post_mock.return_value = response
        client = AgentClient("http://localhost:9001", timeout=1.5)

        result = client.open_app("spotify")

        self.assertTrue(result.success)
        post_mock.assert_called_once_with(
            "http://localhost:9001/actions",
            json={"action": "open_app", "target": "spotify"},
            timeout=1.5,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("core.agent_client.httpx.post")
    def test_deserializes_system_status(self, post_mock) -> None:
        response = MagicMock()
        response.json.return_value = {
            "success": True,
            "data": {
                "cpu_percent": 21,
                "memory_percent": 63,
                "disk_percent": 42,
                "uptime_seconds": 11_880,
            },
        }
        post_mock.return_value = response

        result = AgentClient().get_system_status()

        self.assertEqual(result.data["cpu_percent"], 21)
        self.assertEqual(result.data["uptime_seconds"], 11_880)

    @patch("core.agent_client.httpx.post")
    def test_serializes_spotify_search(self, post_mock) -> None:
        response = MagicMock()
        response.json.return_value = {"success": True}
        post_mock.return_value = response

        AgentClient().spotify_search("Foo Fighters")

        self.assertEqual(
            post_mock.call_args.kwargs["json"],
            {"action": "spotify_search", "query": "Foo Fighters"},
        )

    @patch("core.agent_client.httpx.post")
    def test_reports_connection_refused_as_agent_offline(self, post_mock) -> None:
        request = httpx.Request("POST", "http://127.0.0.1:8001/actions")
        post_mock.side_effect = httpx.ConnectError(
            "Connection refused",
            request=request,
        )

        with self.assertRaisesRegex(
            AgentUnavailableError,
            "Desktop Agent não está disponível",
        ):
            AgentClient().spotify_pause()

    @patch("core.agent_client.httpx.post")
    def test_rejects_invalid_agent_response(self, post_mock) -> None:
        response = MagicMock()
        response.json.return_value = {"success": "yes"}
        post_mock.return_value = response

        with self.assertRaises(InvalidAgentResponseError):
            AgentClient().spotify_play()

    def test_reads_url_from_environment(self) -> None:
        with patch.dict(
            os.environ,
            {"NETUNO_AGENT_URL": "http://localhost:8123"},
        ):
            client = AgentClient()

        self.assertEqual(client._base_url, "http://localhost:8123")

    def test_rejects_non_local_agent_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "localhost"):
            AgentClient("https://agent.example.com")


if __name__ == "__main__":
    unittest.main()
