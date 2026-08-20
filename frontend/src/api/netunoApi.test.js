// @vitest-environment jsdom

import { afterEach, describe, expect, it, vi } from "vitest";

import { NetunoApiError, sendCommand } from "./netunoApi";

describe("netunoApi", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("representa uma resposta HTTP inválida sem tratá-la como erro de rede", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: false, status: 422 }),
    );

    await expect(sendCommand(" ")).rejects.toMatchObject({
      name: "NetunoApiError",
      status: 422,
    });
  });

  it("preserva erros reais de conexão", async () => {
    const networkError = new TypeError("Failed to fetch");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(networkError));

    await expect(sendCommand("que horas são")).rejects.toBe(networkError);
    await expect(sendCommand("que horas são")).rejects.not.toBeInstanceOf(
      NetunoApiError,
    );
  });
});
