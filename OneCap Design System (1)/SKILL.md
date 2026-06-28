---
name: onecap-design
description: Use this skill to generate well-branded interfaces and assets for OneCap, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

# OneCap design skill

OneCap is the **financial integrity layer** for enterprise finance — an AI-native system that continuously validates, reconciles and enforces financial correctness across fragmented systems. The brand visual language is: calm, precise, slightly technical, with a deep-navy primary (`#01187D`), near-black ink (`#12172B`), and a JetBrains Mono accent for numbers, codes and IDs.

## Before designing

1. **Read `/README.md`** (project root of this skill). It covers brand narrative, content fundamentals, visual foundations, iconography, and the index of available resources.
2. **Read `/colors_and_type.css`** for all design tokens — base colors, semantic colors, type scale, radii, shadows.
3. **Browse `/preview/*.html`** — each file is a focused design-system card (colors, type, buttons, forms, cards, etc). They document usage.
4. **Browse `/ui_kits/onecap/`** — pixel-level React recreations of OneCap's product surface (Login, Shell, Dashboard, Reconciliation). Copy components out; do not redraw.
5. **Use `/assets/`** for logos (`logo-lockup.svg`, `logo-mark.svg`, favicon). Never redraw the logo.

## Non-negotiable rules

- **Inputs are borderless.** Use a subtle grey background fill (`#F5F5F6` / `#F3F4F6`) instead of a 1px border. This is core to the brand.
- **Numbers, IDs, codes, ledger amounts → JetBrains Mono with `font-variant-numeric: tabular-nums`.** Everything else is Inter.
- **Primary color is deep navy `#01187D`.** The purple `#57007F` is only for monetary IDs / ledger references. Do not use gradients except very subtle utility ones.
- **No emoji in product chrome.** A single contextual emoji in marketing copy is OK. Icons are Lucide, 1.75px stroke.
- **Small radii.** 4–8px for chips/buttons/inputs, 10–12px for cards, 14–16px for modals. Never pill buttons except status badges.
- **Shadows are restrained.** Use `--shadow-sm` / `--shadow-md` for elevation; `--shadow-xl` only for modals.

## When this skill is invoked

If the user invokes this skill without any other guidance, ask what they want to build (mock? prototype? landing? deck? slide? email?), ask a couple of focused questions about audience and length, then act as an expert designer and output HTML artifacts or production code based on the need.

For **visual artifacts** (slides, mocks, throwaway prototypes): copy assets out of `/assets/`, reuse the preview cards as visual reference, and output self-contained HTML files with inline CSS referencing the tokens in `colors_and_type.css`.

For **production code**: read the UI-kit JSX files and lift component structure, class names, and token usage. Do not invent new visuals — match the existing system.

## Quick token reference

```
--fg-1: #12172B    /* primary text */
--fg-2: #6C727F    /* secondary text */
--fg-3: #99A1AF    /* tertiary */
--bg-1: #FCFCFD    /* app background */
--surface: #FFFFFF /* card / panel */
--brand-navy: #01187D
--brand-purple: #57007F   /* monetary IDs only */
--success: #16A249
--warning: #F59F0A
--danger:  #DC2828
--accent-blue: #2463EB
```

Type scale, semantic styles and full radii / shadow tokens live in `/colors_and_type.css`.
