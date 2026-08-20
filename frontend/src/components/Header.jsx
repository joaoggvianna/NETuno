import netunoMark from "../assets/netuno-mark.svg";

export default function Header() {
  return (
    <header className="app-header">
      <div className="app-header__inner">
        <div className="brand">
          <img className="brand__mark" src={netunoMark} alt="" />
          <p className="brand__name" aria-label="NETuno">
            <span className="brand__name-strong">NET</span>
            <span className="brand__name-light">uno</span>
          </p>
        </div>
      </div>
    </header>
  );
}
