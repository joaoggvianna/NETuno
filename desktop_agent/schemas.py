from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ActionType(str, Enum):
    OPEN_APP = "open_app"
    GET_SYSTEM_STATUS = "get_system_status"
    SPOTIFY_PLAY = "spotify_play"
    SPOTIFY_PAUSE = "spotify_pause"
    SPOTIFY_NEXT = "spotify_next"
    SPOTIFY_PREVIOUS = "spotify_previous"
    SPOTIFY_SEARCH = "spotify_search"


class AppTarget(str, Enum):
    VSCODE = "vscode"
    SPOTIFY = "spotify"


class ActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: ActionType
    target: Optional[AppTarget] = None
    query: Optional[str] = Field(default=None, min_length=1, max_length=200)

    @model_validator(mode="after")
    def validate_action_fields(self) -> "ActionRequest":
        if self.action == ActionType.OPEN_APP:
            if self.target is None:
                raise ValueError("target is required for open_app")
        elif self.target is not None:
            raise ValueError("target is only accepted for open_app")

        if self.action == ActionType.SPOTIFY_SEARCH:
            if self.query is None or not self.query.strip():
                raise ValueError("query is required for spotify_search")
        elif self.query is not None:
            raise ValueError("query is only accepted for spotify_search")

        return self


class SystemStatusData(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: int = Field(ge=0)


class ActionResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error_code: Optional[str] = None
    data: Optional[SystemStatusData] = None


class HealthResponse(BaseModel):
    status: str
    service: str
