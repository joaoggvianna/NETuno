from pydantic import BaseModel, field_validator


class HealthResponse(BaseModel):
    status: str
    service: str


class CommandRequest(BaseModel):
    command: str

    @field_validator("command")
    @classmethod
    def reject_blank_command(cls, command: str) -> str:
        if not command.strip():
            raise ValueError("command must not be blank")
        return command


class CommandResponse(BaseModel):
    success: bool
    message: str
    should_exit: bool
