"""
OneCap Design System slide templates — v2 (cinematic edition).

Each function takes a dict of content fields and returns a complete,
self-contained HTML string at 1920x1080 with OneCap tokens, Google Fonts,
and staggered CSS entrance animations PLUS continuous looping idle animations
so slides stay visually alive for the full scene duration.
"""
from __future__ import annotations

_LOGO_SVG = '<svg width="120" height="24" viewBox="0 0 160 32" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="16" fill="#01187D"/><path fill-rule="evenodd" clip-rule="evenodd" d="M13.4 9.69C11.01 9.99 9.01 11.81 8.33 14.29C8.22 14.65 8.2 15 8.2 15.96C8.2 17.2 8.2 17.19 8.55 18.34C9.03 19.91 10.48 21.44 12.03 22.03C12.71 22.28 13.43 22.4 14.38 22.4C15.72 22.4 16.51 22.19 17.44 21.58C17.92 21.27 18.58 20.64 18.58 20.5C18.58 20.44 18.47 20.2 18.33 19.97C18.19 19.74 18 19.35 17.91 19.11C17.53 18.12 17.4 17.84 17.31 17.84C17.27 17.84 17.04 18.04 16.79 18.28C15.93 19.1 15.26 19.41 14.33 19.41C13.45 19.41 12.69 19.07 12.01 18.37C10.76 17.09 10.8 14.95 12.1 13.62C12.75 12.94 13.58 12.6 14.42 12.67C15.44 12.75 15.93 12.95 16.52 13.56C17.28 14.32 17.52 14.93 17.58 16.23C17.68 18.33 18.41 19.87 19.85 20.99C20.35 21.38 21.59 22.04 21.82 22.04C21.89 22.04 22 22.08 22.07 22.12C22.28 22.24 23.62 22.39 23.71 22.3C23.83 22.22 23.84 19.51 23.73 19.44C23.69 19.42 23.4 19.34 23.1 19.26C22.21 19.04 21.64 18.68 21.15 18.03C20.74 17.47 20.6 16.94 20.6 15.97C20.6 14.81 20.81 14.22 21.43 13.58C21.9 13.1 23.02 12.57 23.57 12.57C23.8 12.57 23.81 12.46 23.79 10.94L23.77 9.62L23.25 9.64C22.07 9.68 20.7 10.24 19.66 11.11C19.36 11.37 19.07 11.58 19.03 11.58C18.99 11.58 18.88 11.49 18.79 11.39C18.54 11.12 17.91 10.64 17.45 10.38C16.81 10.02 15.89 9.74 15.05 9.66C14.2 9.58 14.31 9.58 13.4 9.69Z" fill="white"/><text x="44" y="22" font-family="Lato, sans-serif" font-weight="700" font-size="18" letter-spacing="-0.4" fill="#ffffff">OneCap</text></svg>'

_BASE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --blue-900: #01187D;
  --blue-700: #0229B8;
  --blue-500: #2563EB;
  --blue-400: #3B82F6;
  --blue-300: #6ABAED;
  --blue-100: #DBEAFE;
  --blue-50:  #EFF6FF;
  --violet:   #7C3AED;
  --violet-light: #A78BFA;
  --cyan:     #06B6D4;
  --emerald:  #10B981;
  --amber:    #F59E0B;
  --rose:     #F43F5E;
  --ink-950:  #0A0F1E;
  --ink-900:  #0F172A;
  --ink-800:  #1E293B;
  --ink-700:  #334155;
  --ink-500:  #64748B;
  --ink-300:  #CBD5E1;
  --ink-200:  #E2E8F0;
  --ink-100:  #F1F5F9;
  --surface:  #FFFFFF;
  --font-sans: 'Inter', -apple-system, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --ease-out:  cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

html, body {
  width: 1920px; height: 1080px;
  overflow: hidden;
  font-family: var(--font-sans);
  color: var(--surface);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.slide {
  width: 1920px; height: 1080px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* ---- Entrance animations ---- */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(32px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideRight {
  from { opacity: 0; transform: translateX(-32px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.88); }
  to   { opacity: 1; transform: scale(1); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ---- Continuous idle animations ---- */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-12px); }
}
@keyframes floatSlow {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33%       { transform: translateY(-18px) rotate(2deg); }
  66%       { transform: translateY(-8px) rotate(-1deg); }
}
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px 0px rgba(99,102,241,0.4); }
  50%       { box-shadow: 0 0 60px 10px rgba(99,102,241,0.7); }
}
@keyframes pulse-glow-blue {
  0%, 100% { box-shadow: 0 0 30px 0px rgba(37,99,235,0.5); }
  50%       { box-shadow: 0 0 80px 20px rgba(37,99,235,0.8); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
@keyframes orb-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25%       { transform: translate(40px, -30px) scale(1.05); }
  50%       { transform: translate(-20px, 40px) scale(0.95); }
  75%       { transform: translate(30px, 20px) scale(1.02); }
}
@keyframes orb-drift-2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(-50px, 30px) scale(1.08); }
  66%       { transform: translate(40px, -50px) scale(0.92); }
}
@keyframes scanline {
  0%   { transform: translateY(-100%); }
  100% { transform: translateY(1080px); }
}
@keyframes bar-grow {
  from { width: 0; }
  to   { width: 100%; }
}
@keyframes counter-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes line-draw {
  from { stroke-dashoffset: 1000; }
  to   { stroke-dashoffset: 0; }
}
@keyframes bg-pan {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes typewriter {
  from { width: 0; }
  to   { width: 100%; }
}
@keyframes blink-cursor {
  0%, 100% { border-right-color: var(--cyan); }
  50%       { border-right-color: transparent; }
}

.anim { opacity: 0; }
.anim-1 { animation: slideUp 600ms var(--ease-out) 0ms forwards; }
.anim-2 { animation: slideUp 600ms var(--ease-out) 120ms forwards; }
.anim-3 { animation: slideUp 600ms var(--ease-out) 240ms forwards; }
.anim-4 { animation: slideUp 600ms var(--ease-out) 360ms forwards; }
.anim-5 { animation: slideUp 600ms var(--ease-out) 480ms forwards; }
.anim-6 { animation: slideUp 600ms var(--ease-out) 600ms forwards; }
.anim-7 { animation: slideUp 600ms var(--ease-out) 720ms forwards; }
.anim-8 { animation: slideUp 600ms var(--ease-out) 840ms forwards; }

.anim-right { opacity: 0; animation: slideRight 600ms var(--ease-out) 200ms forwards; }
.anim-scale { opacity: 0; animation: scaleIn 700ms var(--ease-spring) 100ms forwards; }
.anim-fade  { opacity: 0; animation: fadeIn 800ms ease 300ms forwards; }

/* Watermark */
.watermark {
  position: absolute; bottom: 28px; right: 40px;
  display: flex; align-items: center; gap: 8px;
  opacity: 0.6;
  z-index: 100;
}
</style>
</head>
<body>"""

_BASE_FOOT = """
<div class="watermark">{logo}</div>
</div></body></html>""".format(logo=_LOGO_SVG)


# ---------------------------------------------------------------------------
# 1. TITLE TEMPLATE — cinematic dark hero
# ---------------------------------------------------------------------------

def title_slide(content: dict) -> str:
    headline = content.get("headline", content.get("main_title", "Untitled"))
    subtitle = content.get("subtitle", "")
    lesson_number = content.get("lesson_number", "")
    module_name = content.get("module_name", "")

    badge_html = ""
    if lesson_number:
        badge_html = f'<div class="lesson-badge anim anim-1">Lesson {lesson_number}</div>'
    elif module_name:
        badge_html = f'<div class="lesson-badge anim anim-1">{module_name}</div>'

    subtitle_html = f'<p class="slide-subtitle anim anim-3">{subtitle}</p>' if subtitle else ""

    return _BASE_HEAD + f"""
<div class="slide title-slide">
  <!-- Animated background orbs -->
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
  <!-- Grid overlay -->
  <div class="grid-overlay"></div>
  <!-- Decorative ring -->
  <div class="deco-ring anim-scale"></div>
  <!-- Content -->
  <div class="title-content">
    {badge_html}
    <h1 class="slide-headline anim anim-2">{headline}</h1>
    {subtitle_html}
    <div class="title-divider anim anim-4">
      <div class="divider-line"></div>
      <div class="divider-dot"></div>
      <div class="divider-dot"></div>
      <div class="divider-dot"></div>
    </div>
  </div>
  <!-- Floating particles -->
  <div class="particle p1"></div>
  <div class="particle p2"></div>
  <div class="particle p3"></div>
  <div class="particle p4"></div>
  <style>
    .title-slide {{
      background: linear-gradient(135deg, #0A0F1E 0%, #0F1A3D 40%, #0D0B2B 70%, #0A0F1E 100%);
      background-size: 400% 400%;
      animation: bg-pan 12s ease infinite;
      justify-content: center;
      align-items: flex-start;
      padding: 0 160px;
    }}
    .orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      pointer-events: none;
    }}
    .orb-1 {{
      width: 600px; height: 600px;
      background: radial-gradient(circle, rgba(37,99,235,0.35) 0%, transparent 70%);
      top: -150px; right: 100px;
      animation: orb-drift 8s ease-in-out infinite;
    }}
    .orb-2 {{
      width: 400px; height: 400px;
      background: radial-gradient(circle, rgba(124,58,237,0.25) 0%, transparent 70%);
      bottom: -100px; right: 400px;
      animation: orb-drift-2 10s ease-in-out infinite;
    }}
    .orb-3 {{
      width: 300px; height: 300px;
      background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%);
      top: 300px; left: 1000px;
      animation: orb-drift 14s ease-in-out infinite reverse;
    }}
    .grid-overlay {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px);
      background-size: 80px 80px;
      pointer-events: none;
    }}
    .deco-ring {{
      position: absolute;
      right: 200px; top: 50%;
      transform: translateY(-50%);
      width: 520px; height: 520px;
      border-radius: 50%;
      border: 1.5px solid rgba(99,102,241,0.2);
      box-shadow: 0 0 80px 0 rgba(37,99,235,0.15), inset 0 0 80px 0 rgba(37,99,235,0.1);
      animation: pulse-glow 4s ease-in-out infinite, spin-slow 30s linear infinite;
    }}
    .deco-ring::before {{
      content: "";
      position: absolute; inset: 30px;
      border-radius: 50%;
      border: 1px solid rgba(99,102,241,0.15);
    }}
    .deco-ring::after {{
      content: "";
      position: absolute; inset: 60px;
      border-radius: 50%;
      border: 1px solid rgba(99,102,241,0.1);
    }}
    .title-content {{
      position: relative; z-index: 10;
      max-width: 1000px;
    }}
    .lesson-badge {{
      display: inline-flex; align-items: center;
      background: rgba(37,99,235,0.2);
      border: 1px solid rgba(99,130,255,0.4);
      color: #93C5FD;
      font-size: 16px; font-weight: 600;
      padding: 8px 24px;
      border-radius: 999px;
      margin-bottom: 40px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      backdrop-filter: blur(8px);
    }}
    .slide-headline {{
      font-size: 96px; font-weight: 900;
      line-height: 1.0;
      color: #FFFFFF;
      letter-spacing: -2px;
      margin-bottom: 32px;
      background: linear-gradient(135deg, #FFFFFF 0%, #93C5FD 60%, #A78BFA 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .slide-subtitle {{
      font-size: 30px; font-weight: 400;
      color: rgba(148,163,184,0.9);
      line-height: 1.55;
      max-width: 760px;
    }}
    .title-divider {{
      display: flex; align-items: center; gap: 10px;
      margin-top: 48px;
    }}
    .divider-line {{
      width: 80px; height: 2px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet-light));
    }}
    .divider-dot {{
      width: 6px; height: 6px;
      border-radius: 50%;
      background: var(--blue-400);
      animation: float 2s ease-in-out infinite;
    }}
    .divider-dot:nth-child(3) {{ animation-delay: 0.2s; }}
    .divider-dot:nth-child(4) {{ animation-delay: 0.4s; }}
    .particle {{
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
    }}
    .p1 {{
      width: 4px; height: 4px; background: #93C5FD;
      top: 200px; right: 350px;
      animation: floatSlow 6s ease-in-out infinite;
      box-shadow: 0 0 8px #93C5FD;
    }}
    .p2 {{
      width: 6px; height: 6px; background: #A78BFA;
      top: 600px; right: 600px;
      animation: floatSlow 8s ease-in-out infinite 1s;
      box-shadow: 0 0 12px #A78BFA;
    }}
    .p3 {{
      width: 3px; height: 3px; background: #06B6D4;
      top: 400px; right: 280px;
      animation: floatSlow 7s ease-in-out infinite 2s;
      box-shadow: 0 0 8px #06B6D4;
    }}
    .p4 {{
      width: 5px; height: 5px; background: #34D399;
      bottom: 200px; right: 500px;
      animation: floatSlow 9s ease-in-out infinite 0.5s;
      box-shadow: 0 0 10px #34D399;
    }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 2. CONTENT TEMPLATE — dark card layout with animated progress bar
# ---------------------------------------------------------------------------

def content_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    bullets = content.get("bullets", [])
    section_label = content.get("section_label", content.get("highlight", ""))

    if isinstance(bullets, str):
        bullets = [b.strip() for b in bullets.split("\n") if b.strip()]

    bullets_html = ""
    icons = ["▸", "◆", "●", "◉", "▲", "★"]
    for i, b in enumerate(bullets[:6], start=1):
        text = str(b).lstrip("•-* ").strip()
        icon = icons[i % len(icons)]
        delay = i * 120
        bullets_html += f'''<li class="bullet-item" style="animation-delay:{delay}ms">
          <span class="bullet-icon">{icon}</span>
          <span class="bullet-text">{text}</span>
        </li>\n'''

    label_html = f'<span class="section-label anim anim-1">{section_label}</span>' if section_label else ""

    return _BASE_HEAD + f"""
<div class="slide content-slide">
  <!-- Background -->
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <!-- Accent bar top -->
  <div class="accent-bar anim-fade"></div>
  <!-- Content -->
  <div class="content-inner">
    <div class="content-left">
      {label_html}
      <h2 class="content-heading anim anim-2">{heading}</h2>
      <div class="heading-underline anim anim-3"></div>
    </div>
    <div class="content-right">
      <ul class="bullet-list">
        {bullets_html}
      </ul>
    </div>
  </div>
  <!-- Corner decoration -->
  <div class="corner-deco"></div>
  <style>
    .content-slide {{
      background: var(--ink-950);
      justify-content: center;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 800px 600px at 10% 50%, rgba(37,99,235,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 600px 500px at 90% 80%, rgba(124,58,237,0.08) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet), var(--cyan));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .content-inner {{
      display: flex;
      align-items: flex-start;
      gap: 80px;
      padding: 80px 120px;
      position: relative; z-index: 10;
    }}
    .content-left {{
      flex: 0 0 480px;
      padding-top: 8px;
    }}
    .content-right {{
      flex: 1;
    }}
    .section-label {{
      display: inline-block;
      font-size: 13px; font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 24px;
      padding: 6px 16px;
      background: rgba(6,182,212,0.1);
      border: 1px solid rgba(6,182,212,0.3);
      border-radius: 4px;
    }}
    .content-heading {{
      font-size: 62px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -1px;
      line-height: 1.1;
      margin-bottom: 24px;
    }}
    .heading-underline {{
      width: 56px; height: 3px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet-light));
      border-radius: 2px;
      animation: bar-grow 0.8s var(--ease-out) 0.5s both;
    }}
    .bullet-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .bullet-item {{
      opacity: 0;
      animation: slideUp 500ms var(--ease-out) both;
      display: flex;
      align-items: flex-start;
      gap: 18px;
      padding: 22px 28px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      transition: background 0.3s;
      position: relative;
      overflow: hidden;
    }}
    .bullet-item::before {{
      content: "";
      position: absolute; left: 0; top: 0; bottom: 0;
      width: 3px;
      background: linear-gradient(180deg, var(--blue-500), var(--violet));
      border-radius: 3px 0 0 3px;
    }}
    .bullet-icon {{
      font-size: 14px;
      color: var(--blue-400);
      flex-shrink: 0;
      margin-top: 5px;
    }}
    .bullet-text {{
      font-size: 28px;
      font-weight: 400;
      color: rgba(226,232,240,0.92);
      line-height: 1.45;
    }}
    .corner-deco {{
      position: absolute;
      bottom: 0; right: 0;
      width: 300px; height: 300px;
      background: radial-gradient(circle at bottom right, rgba(37,99,235,0.12) 0%, transparent 70%);
      pointer-events: none;
    }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 3. TWO-COLUMN TEMPLATE — split dark layout with glowing divider
# ---------------------------------------------------------------------------

def two_column_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    left_bullets = content.get("left_bullets", content.get("bullets", []))
    right_content = content.get("right_content", content.get("description", ""))
    section_label = content.get("section_label", "")

    if isinstance(left_bullets, str):
        left_bullets = [b.strip() for b in left_bullets.split("\n") if b.strip()]

    bullets_html = ""
    for i, b in enumerate(left_bullets[:5], start=1):
        text = str(b).lstrip("•-* ").strip()
        delay = 300 + i * 120
        bullets_html += f'''<li class="col-bullet" style="animation-delay:{delay}ms">
          <span class="col-num">{i:02d}</span>
          <span>{text}</span>
        </li>\n'''

    label_html = f'<span class="section-label anim anim-1">{section_label}</span>' if section_label else ""

    right_html = ""
    if isinstance(right_content, list):
        for item in right_content:
            right_html += f"<p>{item}</p>"
    else:
        right_html = f"<p>{right_content}</p>"

    return _BASE_HEAD + f"""
<div class="slide two-col-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="two-col-inner">
    <div class="two-col-header">
      {label_html}
      <h2 class="col-heading anim anim-2">{heading}</h2>
    </div>
    <div class="two-col-body">
      <div class="col-left">
        <ul class="col-bullet-list">{bullets_html}</ul>
      </div>
      <div class="col-divider">
        <div class="divider-glow"></div>
      </div>
      <div class="col-right anim-right">
        <div class="right-card">
          <div class="right-card-icon">◈</div>
          {right_html}
        </div>
      </div>
    </div>
  </div>
  <style>
    .two-col-slide {{
      background: var(--ink-950);
      padding: 64px 100px;
      justify-content: center;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 700px 700px at 20% 50%, rgba(37,99,235,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 500px 500px at 80% 50%, rgba(124,58,237,0.08) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet), var(--cyan));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .two-col-inner {{ width: 100%; position: relative; z-index: 10; }}
    .two-col-header {{ margin-bottom: 40px; }}
    .section-label {{
      display: inline-block;
      font-size: 13px; font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 16px;
      padding: 6px 16px;
      background: rgba(6,182,212,0.1);
      border: 1px solid rgba(6,182,212,0.3);
      border-radius: 4px;
    }}
    .col-heading {{
      font-size: 54px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.8px;
    }}
    .two-col-body {{
      display: flex; align-items: flex-start;
    }}
    .col-left {{ flex: 1; padding-right: 40px; }}
    .col-divider {{
      width: 2px;
      align-self: stretch;
      position: relative;
      margin: 0 40px;
      flex-shrink: 0;
      background: rgba(255,255,255,0.06);
    }}
    .divider-glow {{
      position: absolute; inset: 0;
      background: linear-gradient(180deg, transparent, var(--blue-500), var(--violet), transparent);
      animation: fadeIn 1s ease 1s both;
    }}
    .col-right {{ flex: 1; }}
    .col-bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 16px; }}
    .col-bullet {{
      opacity: 0;
      animation: slideUp 500ms var(--ease-out) both;
      display: flex; align-items: flex-start; gap: 16px;
      font-size: 26px; color: rgba(226,232,240,0.88);
      line-height: 1.4;
      padding: 18px 20px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 10px;
    }}
    .col-num {{
      flex-shrink: 0;
      font-size: 13px; font-weight: 700;
      font-family: var(--font-mono);
      color: var(--blue-400);
      background: rgba(37,99,235,0.15);
      border: 1px solid rgba(37,99,235,0.3);
      border-radius: 6px;
      padding: 3px 8px;
      margin-top: 3px;
    }}
    .right-card {{
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 40px 44px;
      font-size: 26px;
      color: rgba(203,213,225,0.9);
      line-height: 1.65;
      position: relative;
      overflow: hidden;
    }}
    .right-card::before {{
      content: "";
      position: absolute; top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet-light));
    }}
    .right-card-icon {{
      font-size: 36px;
      color: var(--blue-400);
      margin-bottom: 20px;
      display: block;
      animation: float 4s ease-in-out infinite;
    }}
    .right-card p {{ margin-bottom: 16px; }}
    .right-card p:last-child {{ margin-bottom: 0; }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 4. DEFINITION TEMPLATE — spotlight focus on term
# ---------------------------------------------------------------------------

def definition_slide(content: dict) -> str:
    term = content.get("term", "")
    definition = content.get("definition", "")
    example = content.get("example", "")

    example_html = ""
    if example:
        example_html = f"""
        <div class="example-card anim anim-5">
          <span class="example-label">Example</span>
          <p class="example-text">{example}</p>
        </div>"""

    return _BASE_HEAD + f"""
<div class="slide definition-slide">
  <!-- Background -->
  <div class="def-bg"></div>
  <div class="spotlight"></div>
  <!-- Content -->
  <div class="def-inner">
    <span class="def-tag anim anim-1">Definition</span>
    <h1 class="def-term anim anim-2">{term}</h1>
    <div class="def-divider anim anim-3">
      <div class="divider-pulse"></div>
    </div>
    <p class="def-body anim anim-4">{definition}</p>
    {example_html}
  </div>
  <!-- Side decoration -->
  <div class="side-deco">
    <div class="side-line"></div>
    <div class="side-dot"></div>
  </div>
  <style>
    .definition-slide {{
      background: var(--ink-950);
      padding: 80px 160px;
      justify-content: center;
    }}
    .def-bg {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 900px 700px at 50% 40%, rgba(124,58,237,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 600px 400px at 80% 80%, rgba(37,99,235,0.08) 0%, transparent 60%);
      pointer-events: none;
    }}
    .spotlight {{
      position: absolute;
      top: -200px; left: 50%;
      transform: translateX(-50%);
      width: 800px; height: 600px;
      background: radial-gradient(ellipse, rgba(124,58,237,0.15) 0%, transparent 70%);
      pointer-events: none;
      animation: pulse-glow 5s ease-in-out infinite;
    }}
    .def-inner {{ max-width: 1300px; width: 100%; position: relative; z-index: 10; }}
    .def-tag {{
      display: inline-block;
      font-size: 13px; font-weight: 700;
      color: var(--violet-light);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 24px;
      padding: 6px 16px;
      background: rgba(124,58,237,0.15);
      border: 1px solid rgba(167,139,250,0.3);
      border-radius: 4px;
    }}
    .def-term {{
      font-size: 100px; font-weight: 900;
      background: linear-gradient(135deg, #FFFFFF 0%, #C4B5FD 50%, #A78BFA 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: -2.5px;
      line-height: 1.0;
      margin-bottom: 36px;
    }}
    .def-divider {{
      display: flex; align-items: center; gap: 12px;
      margin-bottom: 36px;
    }}
    .divider-pulse {{
      width: 80px; height: 2px;
      background: linear-gradient(90deg, var(--violet), var(--blue-400));
      border-radius: 2px;
      animation: pulse-glow 3s ease-in-out infinite;
    }}
    .def-body {{
      font-size: 34px; font-weight: 400;
      color: rgba(203,213,225,0.92);
      line-height: 1.65;
      max-width: 1080px;
      margin-bottom: 48px;
    }}
    .example-card {{
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(167,139,250,0.2);
      border-left: 3px solid var(--violet-light);
      border-radius: 12px;
      padding: 28px 36px;
      max-width: 1080px;
      position: relative;
      overflow: hidden;
    }}
    .example-label {{
      display: block;
      font-size: 12px; font-weight: 700;
      color: var(--violet-light);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 12px;
    }}
    .example-text {{
      font-size: 28px;
      color: rgba(203,213,225,0.85);
      line-height: 1.5;
      font-style: italic;
    }}
    .side-deco {{
      position: absolute;
      right: 100px; top: 50%;
      transform: translateY(-50%);
      display: flex; flex-direction: column; align-items: center; gap: 0;
    }}
    .side-line {{
      width: 2px; height: 300px;
      background: linear-gradient(180deg, transparent, var(--violet), transparent);
      animation: fadeIn 1s ease 1s both;
    }}
    .side-dot {{
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--violet-light);
      box-shadow: 0 0 16px var(--violet-light);
      animation: float 3s ease-in-out infinite;
      margin-top: -4px;
    }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 5. DIAGRAM TEMPLATE (Mermaid.js) — dark glass panel
# ---------------------------------------------------------------------------

def diagram_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    mermaid_code = content.get("mermaid_code", content.get("description", "graph LR\n  A --> B"))
    caption = content.get("caption", "")

    if not any(kw in mermaid_code for kw in ["-->", "---", "graph", "flowchart", "sequenceDiagram", "classDiagram", "pie"]):
        mermaid_code = f"graph LR\n  A[{heading}] --> B[See narration]"

    caption_html = f'<p class="diagram-caption anim anim-4">{caption}</p>' if caption else ""

    return _BASE_HEAD + f"""
<div class="slide diagram-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="diagram-header anim anim-1">
    <span class="diag-tag">Diagram</span>
    <h2 class="diagram-heading">{heading}</h2>
  </div>
  <div class="diagram-body anim anim-2">
    <div class="mermaid">{mermaid_code}</div>
  </div>
  {caption_html}
  <style>
    .diagram-slide {{
      background: var(--ink-950);
      padding: 56px 80px 36px;
      align-items: center;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 800px 600px at 50% 30%, rgba(37,99,235,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 80% 90%, rgba(6,182,212,0.07) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--cyan), var(--blue-500), var(--violet));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .diagram-header {{
      width: 100%; margin-bottom: 28px;
      display: flex; align-items: center; gap: 20px;
      position: relative; z-index: 10;
    }}
    .diag-tag {{
      display: inline-block;
      font-size: 12px; font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 2px;
      padding: 5px 14px;
      background: rgba(6,182,212,0.1);
      border: 1px solid rgba(6,182,212,0.3);
      border-radius: 4px;
      white-space: nowrap;
    }}
    .diagram-heading {{
      font-size: 52px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.6px;
    }}
    .diagram-body {{
      flex: 1;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      padding: 40px;
      overflow: hidden;
      position: relative; z-index: 10;
      box-shadow: 0 0 60px rgba(37,99,235,0.1);
    }}
    .diagram-body::before {{
      content: "";
      position: absolute; top: 0; left: 0; right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(99,130,255,0.4), transparent);
    }}
    .mermaid {{
      width: 100%;
      text-align: center;
      font-family: var(--font-sans) !important;
    }}
    .diagram-caption {{
      font-size: 20px;
      color: rgba(148,163,184,0.7);
      text-align: center;
      margin-top: 16px;
      font-style: italic;
      position: relative; z-index: 10;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {{
        primaryColor: '#1e3a5f',
        primaryTextColor: '#E2E8F0',
        primaryBorderColor: '#3B82F6',
        lineColor: '#60A5FA',
        secondaryColor: '#2d1b4e',
        tertiaryColor: '#1E293B',
        background: '#0A0F1E',
        mainBkg: '#1E293B',
        nodeBorder: '#3B82F6',
        clusterBkg: '#1E293B',
        titleColor: '#E2E8F0',
        edgeLabelBackground: '#1E293B',
        fontSize: '18px'
      }}
    }});
  </script>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 6. CODE TEMPLATE — terminal-style dark editor
# ---------------------------------------------------------------------------

def code_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    language = content.get("language", "python")
    code = content.get("code", content.get("code_block", "# No code provided"))
    explanation = content.get("explanation", content.get("annotation", ""))

    explanation_html = ""
    if explanation:
        explanation_html = f'<p class="code-explanation anim anim-4">{explanation}</p>'

    import html as _html
    code_escaped = _html.escape(str(code))

    return _BASE_HEAD + f"""
<div class="slide code-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="code-header anim anim-1">
    <span class="lang-dot lang-dot-red"></span>
    <span class="lang-dot lang-dot-yellow"></span>
    <span class="lang-dot lang-dot-green"></span>
    <h2 class="code-heading">{heading}</h2>
    <span class="lang-badge">{language}</span>
  </div>
  <div class="code-block-wrap anim anim-2">
    <div class="code-gutter">
      <div class="gutter-line"></div>
    </div>
    <pre><code class="language-{language}">{code_escaped}</code></pre>
  </div>
  {explanation_html}
  <style>
    .code-slide {{
      background: var(--ink-950);
      padding: 56px 100px;
      justify-content: center;
      gap: 28px;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 600px 400px at 80% 20%, rgba(16,185,129,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 20% 80%, rgba(37,99,235,0.07) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--emerald), var(--cyan), var(--blue-500));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .code-header {{
      display: flex; align-items: center; gap: 16px; width: 100%;
      position: relative; z-index: 10;
    }}
    .lang-dot {{
      width: 14px; height: 14px;
      border-radius: 50%;
      flex-shrink: 0;
    }}
    .lang-dot-red    {{ background: #FF5F57; }}
    .lang-dot-yellow {{ background: #FEBC2E; }}
    .lang-dot-green  {{ background: #28C840; }}
    .code-heading {{
      font-size: 44px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.5px;
      flex: 1;
      margin-left: 8px;
    }}
    .lang-badge {{
      font-family: var(--font-mono);
      font-size: 14px; font-weight: 600;
      color: var(--emerald);
      background: rgba(16,185,129,0.1);
      padding: 5px 16px;
      border-radius: 999px;
      border: 1px solid rgba(16,185,129,0.3);
      text-transform: lowercase;
    }}
    .code-block-wrap {{
      background: #0D1117;
      border-radius: 14px;
      overflow: auto;
      max-height: 680px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
      width: 100%;
      display: flex;
      position: relative; z-index: 10;
    }}
    .code-gutter {{
      width: 4px;
      background: linear-gradient(180deg, var(--emerald), var(--cyan));
      flex-shrink: 0;
      border-radius: 14px 0 0 14px;
    }}
    .code-block-wrap pre {{
      margin: 0;
      padding: 36px 44px;
      font-family: var(--font-mono);
      font-size: 22px;
      line-height: 1.7;
      white-space: pre;
      flex: 1;
    }}
    .code-block-wrap code {{
      font-family: var(--font-mono) !important;
    }}
    .code-explanation {{
      font-size: 24px;
      color: rgba(203,213,225,0.85);
      line-height: 1.5;
      padding: 20px 28px;
      background: rgba(16,185,129,0.07);
      border: 1px solid rgba(16,185,129,0.2);
      border-left: 3px solid var(--emerald);
      border-radius: 10px;
      width: 100%;
      position: relative; z-index: 10;
    }}
    .hljs {{ background: transparent !important; color: #c9d1d9; padding: 0 !important; }}
  </style>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 7. CHART TEMPLATE (Chart.js) — dark dashboard style
# ---------------------------------------------------------------------------

def chart_slide(content: dict) -> str:
    import json as _json
    heading = content.get("heading", content.get("title", ""))
    chart_type = content.get("chart_type", "bar")
    labels = content.get("labels", [])
    values = content.get("values", [])
    caption = content.get("caption", "")

    if not labels or not values:
        labels = ["A", "B", "C"]
        values = [1, 2, 3]

    labels_json = _json.dumps(labels)
    values_json = _json.dumps(values)
    caption_html = f'<p class="chart-caption anim anim-4">{caption}</p>' if caption else ""

    if chart_type == "line":
        chart_ds_extra = '"fill": true, "tension": 0.4, "borderColor": "#3B82F6", "backgroundColor": "rgba(59,130,246,0.15)", "pointBackgroundColor": "#3B82F6", "pointRadius": 6, "pointHoverRadius": 8,'
    else:
        chart_ds_extra = '"backgroundColor": ["rgba(59,130,246,0.8)","rgba(99,102,241,0.8)","rgba(6,182,212,0.8)","rgba(16,185,129,0.8)","rgba(245,158,11,0.8)","rgba(244,63,94,0.8)"], "borderRadius": 8, "borderSkipped": false, "borderWidth": 0,'

    return _BASE_HEAD + f"""
<div class="slide chart-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="chart-header anim anim-1">
    <span class="chart-tag">Data</span>
    <h2 class="chart-heading">{heading}</h2>
  </div>
  <div class="chart-wrap anim anim-2">
    <canvas id="myChart"></canvas>
  </div>
  {caption_html}
  <style>
    .chart-slide {{
      background: var(--ink-950);
      padding: 56px 100px 40px;
      align-items: center;
      gap: 24px;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 700px 500px at 50% 60%, rgba(37,99,235,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 400px 300px at 10% 10%, rgba(6,182,212,0.06) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--blue-500), var(--cyan), var(--emerald));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .chart-header {{
      width: 100%; display: flex; align-items: center; gap: 20px;
      position: relative; z-index: 10;
    }}
    .chart-tag {{
      display: inline-block;
      font-size: 12px; font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 2px;
      padding: 5px 14px;
      background: rgba(6,182,212,0.1);
      border: 1px solid rgba(6,182,212,0.3);
      border-radius: 4px;
      white-space: nowrap;
    }}
    .chart-heading {{
      font-size: 52px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.6px;
    }}
    .chart-wrap {{
      flex: 1;
      width: 100%;
      max-height: 760px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 16px;
      padding: 36px;
      position: relative; z-index: 10;
      box-shadow: 0 0 40px rgba(37,99,235,0.08);
    }}
    .chart-wrap::before {{
      content: "";
      position: absolute; top: 0; left: 0; right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(99,130,255,0.4), transparent);
    }}
    .chart-caption {{
      font-size: 20px;
      color: rgba(148,163,184,0.7);
      font-style: italic;
      position: relative; z-index: 10;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {{
      type: '{chart_type}',
      data: {{
        labels: {labels_json},
        datasets: [{{
          label: '{heading}',
          data: {values_json},
          {chart_ds_extra}
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: true,
        animation: {{ duration: 1200, easing: 'easeOutQuart' }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: 'rgba(15,23,42,0.95)',
            borderColor: 'rgba(99,102,241,0.4)',
            borderWidth: 1,
            bodyFont: {{ family: 'Inter', size: 16 }},
            titleFont: {{ family: 'Inter', size: 16, weight: 'bold' }},
            titleColor: '#E2E8F0',
            bodyColor: '#94A3B8'
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: 'rgba(255,255,255,0.05)' }},
            ticks: {{ font: {{ family: 'Inter', size: 16 }}, color: '#64748B' }},
            border: {{ color: 'rgba(255,255,255,0.08)' }}
          }},
          y: {{
            grid: {{ color: 'rgba(255,255,255,0.05)' }},
            ticks: {{ font: {{ family: 'Inter', size: 16 }}, color: '#64748B' }},
            border: {{ color: 'rgba(255,255,255,0.08)' }}
          }}
        }}
      }}
    }});
  </script>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# 8. SUMMARY TEMPLATE — numbered cards with glow accents
# ---------------------------------------------------------------------------

def summary_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", "Key Takeaways"))
    takeaways = content.get("takeaways", content.get("bullets", []))
    next_lesson = content.get("next_lesson", "")

    if isinstance(takeaways, str):
        takeaways = [t.strip() for t in takeaways.split("\n") if t.strip()]

    takeaways_html = ""
    for i, t in enumerate(takeaways[:5], start=1):
        text = str(t).lstrip("•-* ").strip()
        delay = i * 130
        takeaways_html += f'''
        <li class="takeaway-item" style="animation-delay:{delay}ms">
          <span class="takeaway-num">{i:02d}</span>
          <span class="takeaway-text">{text}</span>
          <div class="takeaway-glow"></div>
        </li>'''

    next_html = ""
    if next_lesson:
        next_html = f"""
        <div class="next-lesson anim anim-8">
          <span class="next-arrow">→</span>
          <span class="next-label">Up Next</span>
          <span class="next-title">{next_lesson}</span>
        </div>"""

    return _BASE_HEAD + f"""
<div class="slide summary-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="summary-inner">
    <div class="summary-header anim anim-1">
      <span class="recap-tag">Recap</span>
      <h2 class="summary-heading">{heading}</h2>
    </div>
    <ul class="takeaway-list">{takeaways_html}</ul>
    {next_html}
  </div>
  <style>
    .summary-slide {{
      background: var(--ink-950);
      padding: 64px 140px;
      justify-content: center;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 700px 600px at 10% 50%, rgba(37,99,235,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 90% 80%, rgba(124,58,237,0.08) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--blue-500), var(--violet), var(--cyan));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .summary-inner {{ max-width: 1400px; width: 100%; position: relative; z-index: 10; }}
    .summary-header {{
      margin-bottom: 40px;
      display: flex; align-items: center; gap: 20px;
    }}
    .recap-tag {{
      display: inline-flex; align-items: center;
      font-size: 13px; font-weight: 700;
      color: #fff;
      background: linear-gradient(135deg, var(--blue-700), var(--violet));
      padding: 7px 20px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      white-space: nowrap;
      box-shadow: 0 0 20px rgba(37,99,235,0.4);
    }}
    .summary-heading {{
      font-size: 54px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.7px;
    }}
    .takeaway-list {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
    .takeaway-item {{
      opacity: 0;
      animation: slideUp 500ms var(--ease-out) both;
      display: flex; align-items: center; gap: 24px;
      padding: 18px 28px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 12px;
      position: relative;
      overflow: hidden;
      transition: border-color 0.3s;
    }}
    .takeaway-item::before {{
      content: "";
      position: absolute; left: 0; top: 0; bottom: 0;
      width: 3px;
      background: linear-gradient(180deg, var(--blue-500), var(--violet));
      border-radius: 3px 0 0 3px;
    }}
    .takeaway-num {{
      flex-shrink: 0;
      width: 42px; height: 42px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--blue-700), var(--violet));
      color: #fff;
      font-size: 16px; font-weight: 800;
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono);
      box-shadow: 0 0 16px rgba(37,99,235,0.4);
    }}
    .takeaway-text {{
      font-size: 27px;
      color: rgba(226,232,240,0.92);
      line-height: 1.45;
      flex: 1;
    }}
    .takeaway-glow {{
      position: absolute; right: 0; top: 0; bottom: 0;
      width: 100px;
      background: linear-gradient(90deg, transparent, rgba(37,99,235,0.06));
      pointer-events: none;
    }}
    .next-lesson {{
      display: flex; align-items: center; gap: 16px;
      margin-top: 28px;
      padding: 18px 28px;
      background: rgba(37,99,235,0.1);
      border: 1px solid rgba(59,130,246,0.25);
      border-radius: 12px;
    }}
    .next-arrow {{
      font-size: 24px;
      color: var(--blue-400);
      animation: float 2s ease-in-out infinite;
    }}
    .next-label {{
      font-size: 13px; font-weight: 700;
      color: var(--blue-400);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      white-space: nowrap;
    }}
    .next-title {{
      font-size: 26px; font-weight: 600;
      color: #FFFFFF;
    }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# QUIZ TEMPLATE — game-show style dark cards
# ---------------------------------------------------------------------------

def quiz_slide(content: dict) -> str:
    question = content.get("question", "")
    options = content.get("options", [])
    correct = content.get("correct", "")
    explanation = content.get("explanation", "")

    if isinstance(options, dict):
        options = [f"{k}: {v}" for k, v in options.items()]
    elif isinstance(options, str):
        options = [o.strip() for o in options.split("\n") if o.strip()]

    option_letters = ["A", "B", "C", "D"]
    options_html = ""
    for i, opt in enumerate(options[:4], start=1):
        letter = option_letters[i-1]
        delay = 300 + i * 130
        options_html += f'''<li class="quiz-option" style="animation-delay:{delay}ms">
          <span class="option-letter">{letter}</span>
          <span class="option-text">{opt}</span>
        </li>\n'''

    explanation_html = ""
    if explanation:
        explanation_html = f'<p class="quiz-explanation anim anim-8">{explanation}</p>'

    return _BASE_HEAD + f"""
<div class="slide quiz-slide">
  <div class="bg-gradient"></div>
  <div class="bg-grid"></div>
  <div class="accent-bar anim-fade"></div>
  <div class="quiz-inner">
    <span class="quiz-tag anim anim-1">Knowledge Check</span>
    <h2 class="quiz-question anim anim-2">{question}</h2>
    <ul class="quiz-options">{options_html}</ul>
    {explanation_html}
  </div>
  <style>
    .quiz-slide {{
      background: var(--ink-950);
      padding: 64px 140px;
      justify-content: center;
    }}
    .bg-gradient {{
      position: absolute; inset: 0;
      background:
        radial-gradient(ellipse 700px 500px at 30% 30%, rgba(245,158,11,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 70% 70%, rgba(37,99,235,0.08) 0%, transparent 60%);
      pointer-events: none;
    }}
    .bg-grid {{
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }}
    .accent-bar {{
      position: absolute; top: 0; left: 0; right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--amber), var(--rose), var(--violet));
      animation: bar-grow 1s var(--ease-out) 0.2s both;
    }}
    .quiz-inner {{ max-width: 1380px; width: 100%; position: relative; z-index: 10; }}
    .quiz-tag {{
      display: inline-block;
      font-size: 13px; font-weight: 700;
      color: var(--amber);
      background: rgba(245,158,11,0.1);
      border: 1px solid rgba(245,158,11,0.3);
      padding: 6px 18px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 24px;
    }}
    .quiz-question {{
      font-size: 52px; font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.7px;
      line-height: 1.2;
      margin-bottom: 40px;
    }}
    .quiz-options {{ list-style: none; display: flex; flex-direction: column; gap: 16px; }}
    .quiz-option {{
      opacity: 0;
      animation: slideUp 500ms var(--ease-out) both;
      display: flex; align-items: center; gap: 20px;
      font-size: 26px;
      color: rgba(226,232,240,0.9);
      padding: 18px 28px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      cursor: default;
      line-height: 1.4;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s;
    }}
    .quiz-option::before {{
      content: "";
      position: absolute; inset: 0;
      background: linear-gradient(90deg, rgba(245,158,11,0.05), transparent);
      opacity: 0;
      transition: opacity 0.3s;
    }}
    .option-letter {{
      flex-shrink: 0;
      width: 40px; height: 40px;
      border-radius: 8px;
      background: rgba(245,158,11,0.15);
      border: 1px solid rgba(245,158,11,0.3);
      color: var(--amber);
      font-size: 16px; font-weight: 800;
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono);
    }}
    .option-text {{ flex: 1; }}
    .quiz-explanation {{
      margin-top: 24px;
      font-size: 22px;
      color: rgba(167,243,208,0.85);
      padding: 16px 24px;
      background: rgba(16,185,129,0.08);
      border: 1px solid rgba(16,185,129,0.2);
      border-left: 3px solid var(--emerald);
      border-radius: 10px;
    }}
  </style>
""" + _BASE_FOOT


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

TEMPLATE_REGISTRY = {
    "title":       title_slide,
    "content":     content_slide,
    "two_column":  two_column_slide,
    "definition":  definition_slide,
    "diagram":     diagram_slide,
    "code":        code_slide,
    "chart":       chart_slide,
    "summary":     summary_slide,
    "quiz":        quiz_slide,
}


def render_template(slide_type: str, content: dict) -> str:
    """Render a named template with the given content dict. Falls back to content_slide."""
    fn = TEMPLATE_REGISTRY.get(slide_type, content_slide)
    return fn(content)
