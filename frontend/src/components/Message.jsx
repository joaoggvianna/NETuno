export default function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <article className={`message message--${message.role}`}>
      <p className="message__author">{isUser ? "Você" : "NETuno"}</p>
      <p className="message__content">{message.content}</p>
    </article>
  );
}
