from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from desktop_agent.executor import DesktopExecutor
from desktop_agent.schemas import ActionRequest, ActionResponse, HealthResponse


app = FastAPI(title="NETuno Desktop Agent", version="0.9.0")
executor = DesktopExecutor()
LOOPBACK_HOSTS = {"127.0.0.1", "::1"}


@app.middleware("http")
async def restrict_to_loopback(request: Request, call_next):
    client_host = request.client.host if request.client is not None else None
    if client_host not in LOOPBACK_HOSTS:
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
    return await call_next(request)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="netuno-desktop-agent")


@app.post("/actions", response_model=ActionResponse)
def execute_action(request: ActionRequest) -> ActionResponse:
    return executor.execute(request)
