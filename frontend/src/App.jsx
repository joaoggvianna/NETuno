import { useEffect, useState } from "react";

import { NetunoApiError, checkHealth, sendCommand } from "./api/netunoApi";
import CommandInput from "./components/CommandInput";
import Conversation from "./components/Conversation";
import Header from "./components/Header";

const CONNECTION_ERROR = "Não foi possível conectar ao NETuno Core.";
const REQUEST_ERROR = "O NETuno Core não aceitou esse comando.";

export default function App() {
  const [status, setStatus] = useState("checking");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionEnded, setSessionEnded] = useState(false);

  useEffect(() => {
    let active = true;

    checkHealth()
      .then(() => active && setStatus("online"))
      .catch(() => active && setStatus("offline"));

    return () => {
      active = false;
    };
  }, []);

  async function handleCommand(command) {
    const requestId = Date.now();
    setMessages((current) => [
      ...current,
      { id: `${requestId}-user`, role: "user", content: command },
    ]);
    setLoading(true);

    try {
      const response = await sendCommand(command);
      setMessages((current) => [
        ...current,
        {
          id: `${requestId}-netuno`,
          role: "netuno",
          content: response.message,
        },
      ]);
      setStatus("online");
      if (response.should_exit) {
        setSessionEnded(true);
      }
    } catch (error) {
      const apiIsReachable = error instanceof NetunoApiError;
      setMessages((current) => [
        ...current,
        {
          id: `${requestId}-error`,
          role: "netuno",
          content: apiIsReachable ? REQUEST_ERROR : CONNECTION_ERROR,
        },
      ]);
      setStatus(apiIsReachable ? "online" : "offline");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <Header status={status} />

      <main className="main-content">
        <section className="hero" aria-labelledby="hero-title">
          <div className="core-orb" aria-hidden="true">
            <span>Ψ</span>
          </div>
          <p className="hero__eyebrow">NETuno Core · v0.8</p>
          <h1 id="hero-title">Como posso ajudar?</h1>
          <p className="hero__description">
            Comande seu ambiente local com precisão.
          </p>
        </section>

        <section className="command-deck" aria-label="Console de comandos">
          {status === "offline" && (
            <div className="offline-notice" role="alert">
              O Core não está acessível. Inicie a API local e tente novamente.
            </div>
          )}
          {sessionEnded && (
            <div className="session-notice" role="status">
              Sessão encerrada. Recarregue a página para iniciar novamente.
            </div>
          )}
          <CommandInput
            disabled={loading || sessionEnded}
            onSubmit={handleCommand}
          />
          <Conversation messages={messages} loading={loading} />
        </section>
      </main>

      <footer className="app-footer">
        <span>Sistema local</span>
        <span aria-hidden="true">·</span>
        <span>Sessão não persistente</span>
      </footer>
    </div>
  );
}
