from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import CommandRequest, CommandResponse, HealthResponse
from core.assistant import Assistant


app = FastAPI(title="NETuno API", version="0.9.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
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
