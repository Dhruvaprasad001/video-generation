# OneCap Design System

> The financial integrity layer. A system of intelligence that ensures financial data is accurate, reconciled and decision-ready at all times.

OneCap sits across enterprise financial systems — ERPs, payment gateways, ledgers, operational tools — validating, reconciling and enforcing financial correctness in real time. The product UI is built for finance operators, controllers and CFOs who need absolute clarity about what is true, what is mismatched, and what is pending.

## Sources

- **Figma**: `design-system.fig` — 1 page, 8 top-level frames (master design-system reference board).
- **Brand mark**: `uploads/Favicon.svg` — the stylized "infinity / double-cap" glyph on Royal Blue.
- **No codebase was provided** — recreations in `ui_kits/` are lifted from Figma pseudocode.

---

## Index

| File / Folder | Purpose |
|---|---|
| `colors_and_type.css` | All color + type tokens as CSS variables. Import once. |
| `assets/` | Logos, mark, favicon. |
| `preview/` | Design-system specimen cards (rendered in the Design System tab). |
| `ui_kits/onecap/` | High-fidelity recreation of the OneCap web app. |
| `SKILL.md` | Claude-Skills-compatible entry point. |
| `README.md` | This file. |

---

## Content Fundamentals

OneCap copy is **plain, operator-first, and quantified**. The product tells users what is true, what is wrong, and what to do next — in that order. No jargon-filled enterprise voice. No emoji. No marketing adverbs.

**Voice rules:**
- **Direct, not breezy.** "Balance confirmation has been sent to 12 vendors." Not "We've sent your confirmation — yay!"
- **Quantify everything.** Always prefer "3 mismatches" over "some mismatches". Numbers get tabular (`JetBrains Mono`) treatment.
- **Third person about the system, second person about the user.** "OneCap flagged 4 entries. You can resolve them in bulk."
- **Casing.** Sentence case everywhere except section titles and button labels, which are Title Case ("Upload Data", "Review & Send", "Back to Dashboard").
- **Status words.** "Confirmed / Mismatch / Awaiting Response / Pending / Failed / Reconciled" — these are the system's vocabulary; use them verbatim.
- **No emoji.** Ever. Icons carry meaning.
- **No exclamation marks.** Finance teams don't want to be congratulated.

**Example phrases (from the product):**
- "Both parties agree on balance"
- "Awaiting vendor confirmation"
- "Could not process the reconciliation. The server returned an error. Please try again."
- "Confirmation Sent Successfully — Balance confirmation has been sent to 12 vendors. You'll be notified when they respond."
- "Destructive actions, validation errors, failed states"

**Tone vibe:** Confident, calm, numerate. Bloomberg Terminal meets Linear.

---

## Visual Foundations

### Colors
- **Royal Blue `#01187D`** is the dominant primary — CTAs, navigation, brand presence, active step indicators. It's deep and restrained; do not use pure `#0000FF` or cobalt.
- **Midnight Violet `#57007F`** and **Sea Green `#00A36C`** are accent primaries for secondary actions, data-viz, and variety.
- **Semantic palette is strict**: Success `#16A249`, Warning `#F59F0A`, Danger `#DC2828`, Info `#2463EB`. Ramps exist (50–800) for muted backgrounds.
- **Neutrals are cool and blue-tinted** — `#12172B` for primary text, `#6C727F` for secondary, `#FCFCFD` for app background. Never warm gray.

### Typography
- **Lato** for 100% of UI text. Five-step scale: 12 / 14 / 16 / 18 / 20 px.
- **JetBrains Mono** for code, IDs, monetary figures, and any tabular number column.
- Weights used: 400 regular body, 700 bold (most UI emphasis, buttons, labels, subheads), 900 black (page titles, hero numerics). Lato has no medium/semibold — step directly to 700.
- Tight tracking (`-0.15px`) on bold/black sizes ≥14px — Lato is warmer than Inter and needs slightly tighter letter-spacing at scale.

### Imagery
- **No photography**, no illustration, no hand-drawn anything. The product is data-first.
- Backgrounds are **flat, matte neutrals**. No gradients on panels. A single exception: the top strip of the upload/review sheet uses a faint blue-to-blue vertical gradient (`#EFF6FF → #EEF2FF`) for wayfinding.
- **No grain, no noise, no glassmorphism.**

### Inputs — BORDERLESS
This is a signature of the system. **All text inputs, email inputs, search inputs and textareas render with NO visible border** — instead they use `--bg-input` (`#F6F6F6`) as a fill, with 8px or 6px radius and 8×12 padding. Focus state reveals a 2px inner ring in Royal Blue. Never put a 1px gray border around an input.

### Borders
Borders are for structural containment only: card edges, table row separators, button groups. `1px solid #DDDFE4` (or `#EDEFF3` for hairlines). Never used on inputs.

### Corners
- `6px` buttons and pills
- `8px` inputs, chips, small cards
- `12px` KPI cards and panels
- `16–24px` sheets, modals, full-card confirmations

### Shadows
Low elevation. Reserved for floating surfaces (modals, menus, tooltips).
- `shadow-xs` for resting buttons with color fill.
- `shadow-sm` for small pop-overs.
- `shadow-lg` (`0 25px 50px -12px rgba(0,0,0,0.25)`) for modal sheets.
- No colored shadows. No neon glows.

### Motion
- `180ms` `cubic-bezier(0.4, 0, 0.2, 1)` is the default.
- Fades and small (2–4px) translate-y moves. No bounce, no spring.
- Hover on buttons: darkens fill ~8% (Royal Blue → a touch darker) or adds `--bg-ghost` to neutrals.
- Press: reduces opacity to `0.92` and translates down 1px. No scale transforms.
- Focus: 2px ring inside the shape (not an outline-offset halo).

### Layout
- Dense, tabular, left-aligned. Finance dashboards.
- 8-point spacing baseline; tight gutters (16–24px between cards).
- Fixed left nav (224–260px), fixed top bar, scrolling content. Never floating full-bleed hero sections.
- Tables use zebra-free rows with 1px `#EDEFF3` dividers.

### Transparency & Blur
Near-zero. Semantic backgrounds use 4–10% alpha over the color (e.g. success card `rgba(22,162,73,0.04)` with `rgba(22,162,73,0.2)` border). No `backdrop-filter: blur()`.

### Cards
- White fill, `12px` radius, `1px` `#EDEFF3` border OR no border with `shadow-sm`. Never both.
- Padding: 20–24px.
- KPI cards lead with a **large tabular numeral** (`28–32px`, JetBrains Mono or Lato Black with tabular-nums), followed by a colored icon badge (40px circle, semantic tint at 10% alpha, icon in the semantic ink color).

---

## Iconography

OneCap uses **Lucide icons** throughout — a mono-weight, 1.33px stroke, 16×16 or 24×24 set. This matches the Figma source (icons are 16px with 1.333px strokes).

- **Delivery method**: Load from CDN `https://unpkg.com/lucide@latest` (or `lucide-react` in JSX contexts). No embedded icon font.
- **Substitution note**: The original Figma did not include an icon font — icons are drawn as individual SVG paths but their stroke weight, cap style, and geometry match Lucide exactly. Lucide is the correct and intended set.
- **Sizing**: 16px inside buttons and chips, 20px in inputs/labels, 24px for list items and feature rows, 28px+ only inside circular badges.
- **Color**: Icons inherit text color (`currentColor`). Never multicolor. Never emoji.
- **No Unicode as icons.** No ✓ → use `lucide-check`. No × → use `lucide-x`.

---

## Components (see Figma)

Buttons: Primary (Royal Blue), Secondary (Sea Green), Supporting (Sky Blue), Outline, Ghost, Destructive. Sizes: Small (h=32), Medium (h=36), Large (h=48). Button Groups segment horizontally inside a single bordered pill.

Form components: Text Input, Email Input (with leading icon), Search, Password, Textarea — all **borderless** with `--bg-input` fill.

Cards: KPI Stat Card (number + label + sub-copy), KPI with Trend (delta % + comparison), Confirmation Card (success/error variants with icon badge + CTAs).

Feedback: Snackbar toast, Inline banner (success/warning/error/info), Tooltip.

---

## Caveats

- **Logo wordmark**: The Figma did not include a wordmark beyond the circular mark. The "OneCap" lockup in `assets/logo-lockup.svg` is a faithful reconstruction using Lato Bold, not a vendor-approved asset.
- **Icon set**: Inferred to be Lucide based on stroke metrics; official set not confirmed.
- **No real product screenshots**: the UI kit is synthesized from design-system primitives and implied patterns (upload flow, confirmation sheet) visible in the Figma.

