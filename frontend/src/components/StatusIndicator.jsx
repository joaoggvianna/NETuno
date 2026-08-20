const STATUS_LABELS = {
  checking: "Verificando",
  online: "Online",
  offline: "Offline",
};

export default function StatusIndicator({ status }) {
  return (
    <div
      className={`status-indicator status-indicator--${status}`}
      role="status"
      aria-live="polite"
      aria-label={`NETuno Core: ${STATUS_LABELS[status]}`}
    >
      <span className="status-indicator__dot" aria-hidden="true" />
      <span>{STATUS_LABELS[status]}</span>
    </div>
  );
}
