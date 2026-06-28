# OneCap UI Kit

High-fidelity recreation of the OneCap web application — the financial integrity layer dashboard and reconciliation workflows.

## Screens

1. **Login** — enter email, borderless input, Royal Blue CTA.
2. **Dashboard** — KPI row, recent reconciliations table, banner alerts.
3. **Reconciliation** — detail view with mismatch list, split panel.
4. **Upload Data → Review & Send** — two-step sheet with segmented stepper.
5. **Confirmation Outcome** — success / error full-card state.

## Files

- `index.html` — click-through prototype tying all screens together.
- `App.jsx` — top-level router + app shell.
- `Shell.jsx` — left nav + top bar.
- `Login.jsx`, `Dashboard.jsx`, `Reconciliation.jsx`, `UploadSheet.jsx`.
- `Primitives.jsx` — Button, Input, Badge, Card, KpiCard, IconBadge.

All components render with design tokens from `../../colors_and_type.css`. Icons via Lucide CDN.
