from fastapi import FastAPI

from api.schemas import CommandRequest, CommandResponse, HealthResponse
from core.assistant import Assistant


app = FastAPI(title="NETuno API", version="0.7.0")
assistant = Assistant()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report only whether the local HTTP interface is active."""
    return HealthResponse(status="ok", service="netuno")


@app.post("/commands", response_model=CommandResponse)
def execute_command(request: CommandRequest) -> CommandResponse:
    """Pass validated text to the existing NETuno Core facade."""
    result = assistant.process_command(request.command)
    return CommandResponse(
        success=result.success,
        message=result.message,
        should_exit=result.should_exit,
    )
