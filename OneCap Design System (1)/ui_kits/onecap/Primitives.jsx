// OneCap primitives — buttons, inputs, badges, cards.
// Shared styles use the CSS variables from colors_and_type.css.

const { useState } = React;

// ───────────────── Icon (Lucide wrapper) ─────────────────
function Icon({ name, size = 16, color, style }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (ref.current && window.lucide) {
      ref.current.innerHTML = "";
      const el = document.createElement("i");
      el.setAttribute("data-lucide", name);
      if (color) el.style.color = color;
      el.style.width = size + "px";
      el.style.height = size + "px";
      ref.current.appendChild(el);
      window.lucide.createIcons({ attrs: { width: size, height: size, "stroke-width": 1.75 } });
    }
  }, [name, size, color]);
  return <span ref={ref} style={{ display: "inline-flex", alignItems: "center", ...style }} />;
}

// ───────────────── Button ─────────────────
function Button({ variant = "primary", size = "md", iconLeft, iconRight, children, disabled, onClick, style }) {
  const base = {
    display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 8,
    border: 0, cursor: disabled ? "not-allowed" : "pointer",
    fontFamily: "Inter", fontWeight: 500, letterSpacing: "-0.15px",
    borderRadius: 6, whiteSpace: "nowrap",
    transition: "background 140ms ease, opacity 140ms ease",
    opacity: disabled ? 0.5 : 1,
  };
  const sizes = {
    sm: { height: 32, padding: "0 12px", fontSize: 13 },
    md: { height: 36, padding: "0 16px", fontSize: 14 },
    lg: { height: 48, padding: "0 20px", fontSize: 15 },
  };
  const variants = {
    primary: { background: "#01187D", color: "white", boxShadow: "0 1px 2px -1px rgba(0,0,0,.1),0 1px 3px 0 rgba(0,0,0,.1)" },
    secondary: { background: "#00A36C", color: "white" },
    supporting: { background: "#6ABAEC", color: "white" },
    outline: { background: "#F9FAFB", color: "#12172B", border: "1px solid #DDDFE4" },
    ghost: { background: "transparent", color: "#12172B" },
    danger: { background: "#DC2828", color: "white" },
    neutral: { background: "#EBECEC", color: "#364153" },
  };
  return (
    <button onClick={onClick} disabled={disabled} style={{ ...base, ...sizes[size], ...variants[variant], ...style }}>
      {iconLeft && <Icon name={iconLeft} size={size === "lg" ? 18 : 16} />}
      {children}
      {iconRight && <Icon name={iconRight} size={size === "lg" ? 18 : 16} />}
    </button>
  );
}

// ───────────────── Input (borderless) ─────────────────
function Input({ label, hint, leftIcon, value, onChange, placeholder, type = "text" }) {
  const [focused, setFocused] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {label && <label style={{ font: "500 13px/20px Inter", color: "#12172B", letterSpacing: "-0.15px" }}>{label}</label>}
      <div style={{
        position: "relative", height: 38, borderRadius: 8, background: focused ? "#fff" : "#F6F6F6",
        boxShadow: focused ? "inset 0 0 0 2px #01187D" : "none",
        display: "flex", alignItems: "center", padding: leftIcon ? "0 12px 0 36px" : "0 12px",
        transition: "all 140ms ease",
      }}>
        {leftIcon && <span style={{ position: "absolute", left: 12, display: "flex", alignItems: "center" }}><Icon name={leftIcon} size={16} color="#6C727F" /></span>}
        <input
          type={type}
          value={value}
          onChange={e => onChange && onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder={placeholder}
          style={{ border: 0, outline: 0, background: "transparent", width: "100%", font: "400 14px/1 Inter", color: "#12172B" }}
        />
      </div>
      {hint && <div style={{ font: "400 12px/16px Inter", color: "#6C727F" }}>{hint}</div>}
    </div>
  );
}

// ───────────────── Badge ─────────────────
function Badge({ tone = "neutral", children }) {
  const tones = {
    success: { bg: "#EAFFF8", fg: "#036C4B" },
    warning: { bg: "#FEF7EB", fg: "#8D5605" },
    danger:  { bg: "#FCEDED", fg: "#9B1A1A" },
    info:    { bg: "#ECF1FD", fg: "#134FD1" },
    neutral: { bg: "#F3F4F6", fg: "#3E4553" },
    blue:    { bg: "#EAF0FE", fg: "#01187D" },
  };
  const t = tones[tone];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      background: t.bg, color: t.fg,
      font: "500 11px/16px Inter", letterSpacing: "-0.1px",
      padding: "2px 8px", borderRadius: 999,
    }}>{children}</span>
  );
}

// ───────────────── Card ─────────────────
function Card({ children, style, padding = 20 }) {
  return (
    <div style={{
      background: "white", border: "1px solid #EDEFF3", borderRadius: 12,
      padding, ...style,
    }}>{children}</div>
  );
}

// ───────────────── KpiCard ─────────────────
function KpiCard({ icon, tone = "blue", value, label, sub }) {
  const tones = {
    blue:    { bg: "rgba(1,24,125,0.08)", fg: "#01187D" },
    success: { bg: "rgba(22,162,73,0.10)", fg: "#16A249" },
    warning: { bg: "rgba(245,159,10,0.12)", fg: "#CD8508" },
    danger:  { bg: "rgba(220,40,40,0.10)", fg: "#DC2828" },
  };
  const t = tones[tone];
  return (
    <Card>
      <div style={{ width: 40, height: 40, borderRadius: 999, background: t.bg, color: t.fg,
        display: "inline-flex", alignItems: "center", justifyContent: "center", marginBottom: 14 }}>
        <Icon name={icon} size={20} color={t.fg} />
      </div>
      <div style={{ font: "700 28px/32px Inter", letterSpacing: "-0.5px", color: "#12172B", fontVariantNumeric: "tabular-nums" }}>{value}</div>
      <div style={{ font: "600 13px/20px Inter", color: "#12172B", marginTop: 4 }}>{label}</div>
      {sub && <div style={{ font: "400 12px/16px Inter", color: "#6C727F", marginTop: 4 }}>{sub}</div>}
    </Card>
  );
}

Object.assign(window, { Icon, Button, Input, Badge, Card, KpiCard });
