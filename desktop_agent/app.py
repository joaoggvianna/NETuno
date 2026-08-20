from fastapi import FastAPI

from desktop_agent.executor import DesktopExecutor
from desktop_agent.schemas import ActionRequest, ActionResponse, HealthResponse


app = FastAPI(title="NETuno Desktop Agent", version="0.9.0")
executor = DesktopExecutor()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="netuno-desktop-agent")


@app.post("/actions", response_model=ActionResponse)
def execute_action(request: ActionRequest) -> ActionResponse:
    return executor.execute(request)
