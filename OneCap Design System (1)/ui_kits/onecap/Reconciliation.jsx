function Reconciliation({ row, onClose, onResolve }) {
  const vendor = row ? row[0] : "Northfield Logistics";
  const invoice = row ? row[1] : "INV-20419";
  return (
    <div style={{ padding: 24, fontFamily: "Inter" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, font: "500 12px/16px Inter", color: "#6C727F", marginBottom: 8 }}>
        <a onClick={onClose} style={{ cursor: "pointer", color: "#01187D" }}>Reconciliation</a>
        <Icon name="chevron-right" size={12} color="#99A1AF" />
        <span style={{ fontFamily: "JetBrains Mono", color: "#57007F" }}>{invoice}</span>
      </div>
      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: 20 }}>
        <div>
          <div style={{ font: "700 22px/30px Inter", letterSpacing: "-0.3px", color: "#12172B" }}>{vendor}</div>
          <div style={{ display: "flex", gap: 10, marginTop: 6 }}>
            <Badge tone="danger">✕ 1 mismatch</Badge>
            <Badge tone="neutral">Opened 2d ago</Badge>
            <Badge tone="blue">Owner · Anika K.</Badge>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <Button variant="outline" iconLeft="message-square">Note vendor</Button>
          <Button variant="secondary" iconLeft="check" onClick={onResolve}>Approve resolution</Button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
        <LedgerPanel title="Your ledger · NetSuite" entries={[
          ["2025-11-02", "Freight", "$87,724.80"],
          ["2025-11-05", "Fuel surcharge", "$   0.00"],
        ]} total="$87,724.80" highlight={false} />
        <LedgerPanel title="Vendor statement · Northfield" entries={[
          ["2025-11-02", "Freight", "$87,312.40"],
          ["2025-11-05", "Fuel surcharge", "$   0.00"],
        ]} total="$87,312.40" highlight={true} />
      </div>

      <Card padding={0}>
        <div style={{ padding: "14px 20px", borderBottom: "1px solid #EDEFF3", font: "600 14px/20px Inter", color: "#12172B" }}>
          AI reasoning · delta of −$412.40
        </div>
        <div style={{ padding: 20, display: "flex", flexDirection: "column", gap: 10, font: "400 13px/20px Inter", color: "#3E4553" }}>
          <div>OneCap cross-referenced the PO and detected an under-billing on the freight line. Suggested actions:</div>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <Button variant="primary" size="sm" iconLeft="check">Accept vendor amount</Button>
            <Button variant="outline" size="sm" iconLeft="edit-3">Adjust ledger entry</Button>
            <Button variant="ghost" size="sm" iconLeft="flag">Escalate</Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

function LedgerPanel({ title, entries, total, highlight }) {
  return (
    <div style={{ background: "white", border: `1px solid ${highlight ? "rgba(220,40,40,0.22)" : "#EDEFF3"}`, borderRadius: 12, overflow: "hidden" }}>
      <div style={{ padding: "12px 16px", borderBottom: "1px solid #EDEFF3", font: "600 13px/20px Inter", color: "#12172B", background: highlight ? "rgba(220,40,40,0.04)" : "#FCFCFD" }}>{title}</div>
      <table style={{ width: "100%", borderCollapse: "collapse", font: "400 13px/20px Inter" }}>
        {entries.map((e, i) => (
          <tr key={i}>
            <td style={{ padding: "9px 16px", font: "400 12px/1 'JetBrains Mono'", color: "#6C727F", width: 90 }}>{e[0]}</td>
            <td style={{ padding: "9px 16px", color: "#12172B" }}>{e[1]}</td>
            <td style={{ padding: "9px 16px", textAlign: "right", font: "500 13px/1 'JetBrains Mono'", color: "#12172B" }}>{e[2]}</td>
          </tr>
        ))}
        <tr style={{ background: "#FCFCFD" }}>
          <td style={{ padding: "10px 16px", font: "500 12px/1 'JetBrains Mono'", color: "#6C727F" }}>total</td>
          <td />
          <td style={{ padding: "10px 16px", textAlign: "right", font: "700 14px/1 'JetBrains Mono'", color: highlight ? "#BC1E1E" : "#12172B" }}>{total}</td>
        </tr>
      </table>
    </div>
  );
}

Object.assign(window, { Reconciliation });
