import StatusIndicator from "./StatusIndicator";

export default function Header({ status }) {
  return (
    <header className="app-header">
      <div className="brand">
        <div className="brand__mark" aria-hidden="true">
          Ψ
        </div>
        <div>
          <p className="brand__name">NETuno</p>
          <p className="brand__tagline">Personal Assistant</p>
        </div>
      </div>
      <StatusIndicator status={status} />
    </header>
  );
}
