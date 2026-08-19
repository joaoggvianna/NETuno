import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.app import app
from core.models import CommandResult


class ApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_returns_service_status(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "netuno"},
        )

    @patch("commands.system.datetime")
    def test_executes_simple_core_command(self, datetime_mock) -> None:
        datetime_mock.now.return_value.strftime.return_value = "14:30"

        response = self.client.post(
            "/commands",
            json={"command": "que horas são"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "success": True,
                "message": "Agora são 14:30.",
                "should_exit": False,
            },
        )

    def test_preserves_unknown_command_behavior(self) -> None:
        response = self.client.post(
            "/commands",
            json={"command": "faça café"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "success": False,
                "message": "Não reconheci esse comando.",
                "should_exit": False,
            },
        )

    def test_rejects_empty_and_whitespace_only_commands(self) -> None:
        for command in ("", "    "):
            with self.subTest(command=command):
                response = self.client.post(
                    "/commands",
                    json={"command": command},
                )
                self.assertEqual(response.status_code, 422)

    @patch("api.app.assistant.process_command")
    def test_translates_assistant_result_without_changing_command(
        self, process_command_mock
    ) -> None:
        process_command_mock.return_value = CommandResult(
            success=True,
            message="Resposta conhecida.",
        )

        response = self.client.post(
            "/commands",
            json={"command": "  comando preservado  "},
        )

        self.assertEqual(response.status_code, 200)
        process_command_mock.assert_called_once_with("  comando preservado  ")
        self.assertEqual(
            response.json(),
            {
                "success": True,
                "message": "Resposta conhecida.",
                "should_exit": False,
            },
        )

    def test_should_exit_does_not_stop_api(self) -> None:
        command_response = self.client.post(
            "/commands",
            json={"command": "sair"},
        )

        self.assertEqual(command_response.status_code, 200)
        self.assertTrue(command_response.json()["should_exit"])

        health_response = self.client.get("/health")
        self.assertEqual(health_response.status_code, 200)
        self.assertEqual(health_response.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
