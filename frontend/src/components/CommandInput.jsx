import { useState } from "react";

export default function CommandInput({ disabled, onSubmit }) {
  const [command, setCommand] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const trimmedCommand = command.trim();

    if (!trimmedCommand || disabled) {
      return;
    }

    onSubmit(trimmedCommand);
    setCommand("");
  }

  return (
    <form className="command-form" onSubmit={handleSubmit}>
      <label className="visually-hidden" htmlFor="netuno-command">
        Digite um comando para o NETuno
      </label>
      <input
        id="netuno-command"
        type="text"
        value={command}
        onChange={(event) => setCommand(event.target.value)}
        placeholder="Digite um comando..."
        autoComplete="off"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled || !command.trim()}
        aria-label={disabled ? "Enviando comando" : "Enviar comando"}
      >
        <span aria-hidden="true">→</span>
      </button>
    </form>
  );
}
