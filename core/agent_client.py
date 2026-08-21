from dataclasses import dataclass
import os
from typing import Any, Optional
from urllib.parse import urlparse

import httpx


DEFAULT_AGENT_URL = "http://127.0.0.1:8001"
AGENT_OFFLINE_MESSAGE = "O NETuno Desktop Agent não está disponível."
AGENT_CONFIGURATION_MESSAGE = (
    "A configuração do NETuno Desktop Agent é inválida."
)


class AgentClientError(RuntimeError):
    """Base error raised by communication with the Desktop Agent."""


class AgentUnavailableError(AgentClientError):
    """Raised when the Desktop Agent cannot be reached."""


class AgentConfigurationError(AgentClientError):
    """Raised when the configured Agent URL is not safe or valid."""


class InvalidAgentResponseError(AgentClientError):
    """Raised when the Agent violates its response contract."""


@dataclass(frozen=True)
class AgentResult:
    success: bool
    message: Optional[str] = None
    error_code: Optional[str] = None
    data: Optional[dict[str, Any]] = None


class AgentClient:
    """Centralize structured HTTP communication with the local Agent."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 2.0,
    ) -> None:
        self._base_url = (
            base_url or os.environ.get("NETUNO_AGENT_URL") or DEFAULT_AGENT_URL
        ).rstrip("/")
        self._timeout = timeout
        self._validate_local_url()

    def open_app(self, target: str) -> AgentResult:
        return self._send_action("open_app", target=target)

    def get_system_status(self) -> AgentResult:
        return self._send_action("get_system_status")

    def spotify_play(self) -> AgentResult:
        return self._send_action("spotify_play")

    def spotify_pause(self) -> AgentResult:
        return self._send_action("spotify_pause")

    def spotify_next(self) -> AgentResult:
        return self._send_action("spotify_next")

    def spotify_previous(self) -> AgentResult:
        return self._send_action("spotify_previous")

    def spotify_search(self, query: str) -> AgentResult:
        return self._send_action("spotify_search", query=query)

    def _send_action(self, action: str, **payload: str) -> AgentResult:
        body = {"action": action, **payload}
        try:
            response = httpx.post(
                f"{self._base_url}/actions",
                json=body,
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.RequestError as error:
            raise AgentUnavailableError(AGENT_OFFLINE_MESSAGE) from error
        except httpx.HTTPStatusError as error:
            raise InvalidAgentResponseError(
                "O Desktop Agent rejeitou a ação enviada pelo Core."
            ) from error

        try:
            response_data = response.json()
            success = response_data["success"]
            if not isinstance(success, bool):
                raise TypeError
            data = response_data.get("data")
            if data is not None and not isinstance(data, dict):
                raise TypeError
            return AgentResult(
                success=success,
                message=response_data.get("message"),
                error_code=response_data.get("error_code"),
                data=data,
            )
        except (ValueError, KeyError, TypeError) as error:
            raise InvalidAgentResponseError(
                "O Desktop Agent retornou uma resposta inválida."
            ) from error

    def _validate_local_url(self) -> None:
        try:
            parsed_url = urlparse(self._base_url)
            parsed_url.port
        except ValueError as error:
            raise AgentConfigurationError(
                AGENT_CONFIGURATION_MESSAGE
            ) from error

        if (
            parsed_url.scheme not in {"http", "https"}
            or parsed_url.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed_url.username is not None
            or parsed_url.password is not None
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise AgentConfigurationError(AGENT_CONFIGURATION_MESSAGE)
