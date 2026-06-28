function Dashboard({ onOpenRecon, onUpload }) {
  const [tab, setTab] = React.useState("ledger");
  return (
    <div style={{ padding: 24, fontFamily: "Inter" }}>
      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 20 }}>
        <div>
          <div style={{ font: "700 24px/30px Inter", letterSpacing: "-0.4px", color: "#12172B" }}>Integrity Dashboard</div>
          <div style={{ font: "400 13px/20px Inter", color: "#6C727F", marginTop: 4 }}>Q4 2025 · across 6 connected systems · last synced 2 min ago</div>
        </div>
        <div style={{ display: "inline-flex", border: "1px solid #EAE9E9", borderRadius: 6, padding: 1, background: "white" }}>
          {[["ledger","Ledger"],["pg","PG Recon"],["month","Month"]].map(([id, lbl]) => (
            <button key={id} onClick={() => setTab(id)} style={{
              padding: "8px 14px", border: 0, background: tab === id ? "#F3F4F6" : "transparent",
              color: tab === id ? "#12172B" : "#6C727F", font: "500 13px/1 Inter", borderRadius: 5, cursor: "pointer",
            }}>{lbl}</button>
          ))}
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 20 }}>
        <KpiCard icon="check-circle-2" tone="success" value="1,284" label="Confirmed" sub="Both parties agree on balance" />
        <KpiCard icon="alert-triangle" tone="danger"  value="13" label="Mismatches" sub="Awaiting reconciliation action" />
        <KpiCard icon="clock"          tone="warning" value="47" label="Awaiting Response" sub="Pending vendor confirmation" />
        <KpiCard icon="shield-check"   tone="blue"    value="99.4%" label="Compliance Rate" sub="+0.4% vs last audit" />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 14 }}>
        <Card padding={0}>
          <div style={{ padding: "16px 20px", borderBottom: "1px solid #EDEFF3", display: "flex", alignItems: "center" }}>
            <div style={{ font: "600 15px/22px Inter", color: "#12172B" }}>Recent reconciliations</div>
            <div style={{ flex: 1 }} />
            <Button variant="ghost" size="sm" iconRight="chevron-right">View all</Button>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", font: "500 13px/20px Inter" }}>
            <thead>
              <tr>
                {["Vendor", "Invoice", "Amount", "Delta", "Status"].map((h, i) => (
                  <th key={h} style={{ textAlign: i >= 2 && i <= 3 ? "right" : "left", padding: "10px 20px",
                    font: "500 11px/16px 'JetBrains Mono'", textTransform: "uppercase", letterSpacing: "0.04em",
                    color: "#6C727F", borderBottom: "1px solid #EDEFF3" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ["Acme Parts Co.", "INV-20418", "$142,500.00", "+0.00",   "confirmed"],
                ["Northfield Logistics", "INV-20419", "$87,312.40", "−412.40", "mismatch"],
                ["Continental Freight", "INV-20420", "$19,004.00", "—",       "pending"],
                ["Halcyon Materials", "INV-20421", "$204,118.00", "+88.00", "mismatch"],
                ["Blueridge Ops", "INV-20422", "$11,500.00", "+0.00",   "confirmed"],
              ].map((r, i) => (
                <tr key={i} onClick={() => onOpenRecon(r)} style={{ cursor: "pointer" }}>
                  <td style={{ padding: "12px 20px", borderBottom: "1px solid #F3F4F6", color: "#12172B" }}>{r[0]}</td>
                  <td style={{ padding: "12px 20px", borderBottom: "1px solid #F3F4F6", font: "500 12px/1 'JetBrains Mono'", color: "#57007F" }}>{r[1]}</td>
                  <td style={{ padding: "12px 20px", borderBottom: "1px solid #F3F4F6", textAlign: "right", font: "500 13px/1 'JetBrains Mono'", fontVariantNumeric: "tabular-nums", color: "#12172B" }}>{r[2]}</td>
                  <td style={{ padding: "12px 20px", borderBottom: "1px solid #F3F4F6", textAlign: "right", font: "500 13px/1 'JetBrains Mono'",
                      color: r[3].startsWith("+") && r[3] !== "+0.00" ? "#036C4B" : r[3].startsWith("−") ? "#BC1E1E" : "#6C727F" }}>{r[3]}</td>
                  <td style={{ padding: "12px 20px", borderBottom: "1px solid #F3F4F6" }}>
                    {r[4] === "confirmed" && <Badge tone="success">✓ Confirmed</Badge>}
                    {r[4] === "mismatch" && <Badge tone="danger">✕ Mismatch</Badge>}
                    {r[4] === "pending" && <Badge tone="warning">◷ Pending</Badge>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <Card>
            <div style={{ font: "600 14px/20px Inter", color: "#12172B", marginBottom: 10 }}>System health</div>
            {[
              ["NetSuite", "ok"], ["Stripe", "ok"], ["SAP S/4", "warn"], ["Plaid", "ok"], ["Ramp", "ok"],
            ].map(([n, s]) => (
              <div key={n} style={{ display: "flex", alignItems: "center", padding: "8px 0", borderBottom: "1px solid #F3F4F6", font: "500 13px/1 Inter" }}>
                <span style={{ width: 8, height: 8, borderRadius: 999, background: s === "ok" ? "#16A249" : "#F59F0A", marginRight: 10 }} />
                <span style={{ color: "#12172B", flex: 1 }}>{n}</span>
                <span style={{ font: "400 11px/1 'JetBrains Mono'", color: "#6C727F" }}>{s === "ok" ? "synced" : "degraded"}</span>
              </div>
            ))}
          </Card>
          <div style={{ padding: "12px 14px", borderRadius: 8, background: "rgba(245,159,10,0.08)", border: "1px solid rgba(245,159,10,0.22)", display: "flex", gap: 10 }}>
            <Icon name="alert-triangle" size={18} color="#CD8508" />
            <div>
              <div style={{ font: "600 13px/18px Inter", color: "#8D5605" }}>3 vendors haven't confirmed in 7 days.</div>
              <div style={{ font: "400 12px/16px Inter", color: "#6C727F", marginTop: 2 }}>Consider resending confirmation requests.</div>
            </div>
          </div>
          <Button variant="secondary" iconLeft="send" onClick={onUpload}>Send Confirmations</Button>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { Dashboard });
