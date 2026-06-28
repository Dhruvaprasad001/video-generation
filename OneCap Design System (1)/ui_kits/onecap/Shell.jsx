// OneCap app shell — left nav + top bar
const navItems = [
  { id: "dashboard", label: "Dashboard", icon: "layout-dashboard" },
  { id: "recon", label: "Reconciliation", icon: "arrow-right-left" },
  { id: "vendors", label: "Vendors", icon: "building-2" },
  { id: "invoices", label: "Invoices", icon: "file-text" },
  { id: "reports", label: "Reports", icon: "bar-chart-3" },
  { id: "compliance", label: "Compliance", icon: "shield-check" },
];

function Shell({ current, onNav, onUpload, children }) {
  return (
    <div style={{ display: "flex", height: "100vh", background: "#FCFCFD" }}>
      <aside style={{ width: 232, background: "white", borderRight: "1px solid #EDEFF3", display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "18px 20px", display: "flex", alignItems: "center", gap: 10, borderBottom: "1px solid #EDEFF3" }}>
          <img src="../../assets/favicon.svg" width="28" height="28" />
          <div style={{ font: "700 17px/1 Inter", letterSpacing: "-0.3px", color: "#12172B" }}>OneCap</div>
        </div>
        <nav style={{ padding: 12, display: "flex", flexDirection: "column", gap: 2, flex: 1 }}>
          {navItems.map(it => {
            const active = it.id === current;
            return (
              <button key={it.id} onClick={() => onNav(it.id)} style={{
                display: "flex", alignItems: "center", gap: 10, padding: "9px 12px",
                borderRadius: 8, border: 0, cursor: "pointer", textAlign: "left",
                background: active ? "#EAF0FE" : "transparent",
                color: active ? "#01187D" : "#3E4553",
                font: `${active ? 600 : 500} 13px/20px Inter`, letterSpacing: "-0.1px",
              }}>
                <Icon name={it.icon} size={16} color={active ? "#01187D" : "#6C727F"} />
                {it.label}
              </button>
            );
          })}
        </nav>
        <div style={{ padding: 12, borderTop: "1px solid #EDEFF3", display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 32, height: 32, borderRadius: 999, background: "#57007F", color: "white", display: "flex", alignItems: "center", justifyContent: "center", font: "600 12px/1 Inter" }}>AK</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ font: "500 13px/18px Inter", color: "#12172B" }}>Anika Kapoor</div>
            <div style={{ font: "400 11px/14px Inter", color: "#6C727F" }}>Controller</div>
          </div>
          <Icon name="settings" size={16} color="#6C727F" />
        </div>
      </aside>
      <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
        <header style={{
          height: 60, borderBottom: "1px solid #EDEFF3", background: "white",
          display: "flex", alignItems: "center", gap: 16, padding: "0 24px",
        }}>
          <div style={{ position: "relative", width: 360 }}>
            <Input leftIcon="search" placeholder="Search vendors, invoices, transactions…" />
          </div>
          <div style={{ flex: 1 }} />
          <Button variant="outline" iconLeft="filter">Filters</Button>
          <Button variant="primary" iconLeft="upload" onClick={onUpload}>Upload Data</Button>
          <span style={{ position: "relative", display: "inline-flex" }}>
            <Icon name="bell" size={18} color="#6C727F" />
            <span style={{ position: "absolute", top: -4, right: -4, width: 8, height: 8, borderRadius: 999, background: "#DC2828" }} />
          </span>
        </header>
        <div style={{ flex: 1, overflow: "auto" }}>{children}</div>
      </main>
    </div>
  );
}

Object.assign(window, { Shell });
