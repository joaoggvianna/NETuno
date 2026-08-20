// @vitest-environment jsdom

import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("./api/netunoApi", async (importOriginal) => {
  const original = await importOriginal();
  return {
    ...original,
    checkHealth: vi.fn(),
    sendCommand: vi.fn(),
  };
});

import App from "./App";
import {
  NetunoApiError,
  checkHealth,
  sendCommand,
} from "./api/netunoApi";

function submitCommand(command) {
  const input = screen.getByLabelText("Digite um comando para o NETuno");
  fireEvent.change(input, { target: { value: command } });
  fireEvent.click(screen.getByRole("button", { name: "Enviar comando" }));
}

describe("App", () => {
  beforeEach(() => {
    Element.prototype.scrollIntoView = vi.fn();
    checkHealth.mockResolvedValue({ status: "ok" });
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("mantém a API online quando o comando recebe HTTP 422", async () => {
    sendCommand.mockRejectedValue(new NetunoApiError(422));
    render(<App />);

    await waitFor(() => expect(checkHealth).toHaveBeenCalledOnce());
    submitCommand("comando inválido");

    expect(
      await screen.findByText("O NETuno Core não aceitou esse comando."),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("O Core não está acessível. Inicie a API local e tente novamente."),
    ).not.toBeInTheDocument();
  });

  it("marca offline quando há falha de conexão", async () => {
    sendCommand.mockRejectedValue(new TypeError("Failed to fetch"));
    render(<App />);

    await waitFor(() => expect(checkHealth).toHaveBeenCalledOnce());
    submitCommand("que horas são");

    expect(
      await screen.findByText("Não foi possível conectar ao NETuno Core."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("O Core não está acessível. Inicie a API local e tente novamente."),
    ).toBeInTheDocument();
  });

  it("encerra a sessão quando a API retorna should_exit", async () => {
    sendCommand.mockResolvedValue({
      message: "Até mais.",
      should_exit: true,
    });
    render(<App />);

    await waitFor(() => expect(checkHealth).toHaveBeenCalledOnce());
    submitCommand("sair");

    expect(await screen.findByText("Até mais.")).toBeInTheDocument();
    expect(
      screen.getByText("Sessão encerrada. Recarregue a página para iniciar novamente."),
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText("Digite um comando para o NETuno"),
    ).toBeDisabled();
  });
});
