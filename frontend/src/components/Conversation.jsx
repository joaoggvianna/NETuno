import { useEffect, useRef } from "react";

import Message from "./Message";

export default function Conversation({ messages, loading }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages, loading]);

  if (!messages.length && !loading) {
    return null;
  }

  return (
    <section className="conversation" aria-live="polite" aria-label="Conversa">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      {loading && (
        <div className="message message--netuno message--loading">
          <p className="message__author">NETuno</p>
          <p className="message__content">Processando comando...</p>
        </div>
      )}
      <div ref={endRef} />
    </section>
  );
}
