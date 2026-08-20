const API_URL =
  import.meta.env.VITE_NETUNO_API_URL || "http://127.0.0.1:8000";

export class NetunoApiError extends Error {
  constructor(status) {
    super(`NETuno API returned HTTP ${status}`);
    this.name = "NetunoApiError";
    this.status = status;
  }
}

async function request(path, options) {
  const response = await fetch(`${API_URL}${path}`, options);

  if (!response.ok) {
    throw new NetunoApiError(response.status);
  }

  return response.json();
}

export function checkHealth() {
  return request("/health");
}

export function sendCommand(command) {
  return request("/commands", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ command }),
  });
}
