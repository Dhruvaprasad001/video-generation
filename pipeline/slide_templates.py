"""
OneCap Design System slide templates.

Each function takes a dict of content fields and returns a complete,
self-contained HTML string at 1920x1080 with OneCap tokens, Google Fonts,
and staggered CSS entrance animations.
"""
from __future__ import annotations

_LOGO_SVG = '<svg width="120" height="24" viewBox="0 0 160 32" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="16" fill="#01187D"/><path fill-rule="evenodd" clip-rule="evenodd" d="M13.4 9.69C11.01 9.99 9.01 11.81 8.33 14.29C8.22 14.65 8.2 15 8.2 15.96C8.2 17.2 8.2 17.19 8.55 18.34C9.03 19.91 10.48 21.44 12.03 22.03C12.71 22.28 13.43 22.4 14.38 22.4C15.72 22.4 16.51 22.19 17.44 21.58C17.92 21.27 18.58 20.64 18.58 20.5C18.58 20.44 18.47 20.2 18.33 19.97C18.19 19.74 18 19.35 17.91 19.11C17.53 18.12 17.4 17.84 17.31 17.84C17.27 17.84 17.04 18.04 16.79 18.28C15.93 19.1 15.26 19.41 14.33 19.41C13.45 19.41 12.69 19.07 12.01 18.37C10.76 17.09 10.8 14.95 12.1 13.62C12.75 12.94 13.58 12.6 14.42 12.67C15.44 12.75 15.93 12.95 16.52 13.56C17.28 14.32 17.52 14.93 17.58 16.23C17.68 18.33 18.41 19.87 19.85 20.99C20.35 21.38 21.59 22.04 21.82 22.04C21.89 22.04 22 22.08 22.07 22.12C22.28 22.24 23.62 22.39 23.71 22.3C23.83 22.22 23.84 19.51 23.73 19.44C23.69 19.42 23.4 19.34 23.1 19.26C22.21 19.04 21.64 18.68 21.15 18.03C20.74 17.47 20.6 16.94 20.6 15.97C20.6 14.81 20.81 14.22 21.43 13.58C21.9 13.1 23.02 12.57 23.57 12.57C23.8 12.57 23.81 12.46 23.79 10.94L23.77 9.62L23.25 9.64C22.07 9.68 20.7 10.24 19.66 11.11C19.36 11.37 19.07 11.58 19.03 11.58C18.99 11.58 18.88 11.49 18.79 11.39C18.54 11.12 17.91 10.64 17.45 10.38C16.81 10.02 15.89 9.74 15.05 9.66C14.2 9.58 14.31 9.58 13.4 9.69Z" fill="white"/><text x="44" y="22" font-family="Lato, sans-serif" font-weight="700" font-size="18" letter-spacing="-0.4" fill="#12172B">OneCap</text></svg>'

_BASE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --royal-blue: #01187D;
  --sea-green: #6ABAED;
  --midnight-violet: #57007F;
  --success: #16A249;
  --warning: #F59F0A;
  --danger: #DC2828;
  --ink-900: #12172B;
  --ink-700: #3E4553;
  --ink-500: #6C727F;
  --ink-300: #D0D5DD;
  --ink-200: #DDDFE4;
  --ink-100: #EDEFF3;
  --bg: #FCFCFD;
  --surface: #FFFFFF;
  --border: #DDDFE4;
  --blue-50: #EAF0FE;
  --shadow-sm: 0 2px 4px 0 rgba(0,0,0,0.08), 0 4px 6px 0 rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px -2px rgba(0,0,0,0.08), 0 8px 24px -4px rgba(0,0,0,0.08);
  --font-sans: 'Lato', -apple-system, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
}

html, body {
  width: 1920px; height: 1080px;
  overflow: hidden;
  background: var(--bg);
  font-family: var(--font-sans);
  color: var(--ink-900);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.slide {
  width: 1920px; height: 1080px;
  position: relative;
  background: var(--bg);
  display: flex;
  flex-direction: column;
}

/* Entrance animation */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
.anim { opacity: 0; animation: fadeUp 180ms var(--ease) forwards; }
.anim-1 { animation-delay: 0ms; }
.anim-2 { animation-delay: 100ms; }
.anim-3 { animation-delay: 200ms; }
.anim-4 { animation-delay: 300ms; }
.anim-5 { animation-delay: 400ms; }
.anim-6 { animation-delay: 500ms; }
.anim-7 { animation-delay: 600ms; }
.anim-8 { animation-delay: 700ms; }

/* Watermark */
.watermark {
  position: absolute; bottom: 32px; right: 48px;
  display: flex; align-items: center; gap: 8px;
  opacity: 0.5;
}
.watermark span {
  font-size: 14px; font-weight: 700;
  color: var(--royal-blue);
  letter-spacing: -0.15px;
}
</style>
</head>
<body>"""

_BASE_FOOT = """
<div class="watermark">
  {logo}
  <span>OneCap</span>
</div>
</div></body></html>""".format(logo=_LOGO_SVG)



# ---------------------------------------------------------------------------
# 1. TITLE TEMPLATE
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
  <div class="title-content">
    {badge_html}
    <h1 class="slide-headline anim anim-2">{headline}</h1>
    {subtitle_html}
    <div class="title-divider anim anim-4"></div>
  </div>
  <div class="title-deco"></div>
  <style>
    .title-slide {{
      background: var(--surface);
      justify-content: center;
      align-items: flex-start;
      padding: 0 160px;
    }}
    .title-deco {{
      position: absolute;
      top: 0; right: 0;
      width: 560px; height: 100%;
      background: var(--blue-50);
      clip-path: polygon(15% 0, 100% 0, 100% 100%, 0% 100%);
      z-index: 0;
    }}
    .title-content {{
      position: relative; z-index: 1;
      max-width: 900px;
    }}
    .lesson-badge {{
      display: inline-flex;
      align-items: center;
      background: var(--royal-blue);
      color: #fff;
      font-size: 18px; font-weight: 700;
      padding: 6px 20px;
      border-radius: 999px;
      margin-bottom: 36px;
      letter-spacing: 0.5px;
    }}
    .slide-headline {{
      font-size: 88px; font-weight: 900;
      line-height: 1.05;
      color: var(--ink-900);
      letter-spacing: -1.5px;
      margin-bottom: 28px;
    }}
    .slide-subtitle {{
      font-size: 32px; font-weight: 400;
      color: var(--ink-500);
      line-height: 1.5;
      max-width: 720px;
    }}
    .title-divider {{
      width: 72px; height: 4px;
      background: var(--royal-blue);
      border-radius: 2px;
      margin-top: 40px;
    }}
  </style>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 2. CONTENT TEMPLATE (heading + bullets)
# ---------------------------------------------------------------------------

def content_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    bullets = content.get("bullets", [])
    section_label = content.get("section_label", content.get("highlight", ""))

    if isinstance(bullets, str):
        bullets = [b.strip() for b in bullets.split("\n") if b.strip()]

    bullets_html = ""
    for i, b in enumerate(bullets[:6], start=2):
        text = str(b).lstrip("•-* ").strip()
        bullets_html += f'<li class="bullet-item anim anim-{min(i+1, 8)}">{text}</li>\n'

    label_html = f'<span class="section-label anim anim-1">{section_label}</span>' if section_label else ""

    return _BASE_HEAD + f"""
<div class="slide content-slide">
  <div class="content-inner">
    {label_html}
    <h2 class="content-heading anim anim-2">{heading}</h2>
    <ul class="bullet-list">
      {bullets_html}
    </ul>
  </div>
  <style>
    .content-slide {{
      background: var(--surface);
      padding: 80px 160px;
      justify-content: center;
    }}
    .content-inner {{
      max-width: 1280px;
      width: 100%;
    }}
    .section-label {{
      display: inline-block;
      font-size: 16px; font-weight: 700;
      color: var(--royal-blue);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 20px;
      padding: 4px 14px;
      background: var(--blue-50);
      border-radius: 4px;
    }}
    .content-heading {{
      font-size: 60px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.8px;
      line-height: 1.1;
      margin-bottom: 56px;
      padding-left: 20px;
      border-left: 4px solid var(--royal-blue);
    }}
    .bullet-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .bullet-item {{
      display: flex;
      align-items: flex-start;
      gap: 20px;
      font-size: 30px;
      font-weight: 400;
      color: var(--ink-700);
      line-height: 1.4;
      padding: 20px 28px;
      background: var(--bg);
      border-radius: 8px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }}
    .bullet-item::before {{
      content: '';
      display: block;
      flex-shrink: 0;
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--royal-blue);
      margin-top: 11px;
    }}
  </style>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 3. TWO-COLUMN TEMPLATE
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
        bullets_html += f'<li class="col-bullet anim anim-{min(i+2, 8)}">{text}</li>\n'

    label_html = f'<span class="section-label anim anim-1">{section_label}</span>' if section_label else ""

    right_html = ""
    if isinstance(right_content, list):
        for item in right_content:
            right_html += f"<p>{item}</p>"
    else:
        right_html = f"<p>{right_content}</p>"

    return _BASE_HEAD + f"""
<div class="slide two-col-slide">
  <div class="two-col-inner">
    <div class="two-col-header anim anim-1">
      {label_html}
      <h2 class="col-heading">{heading}</h2>
    </div>
    <div class="two-col-body">
      <div class="col-left">
        <ul class="col-bullet-list">{bullets_html}</ul>
      </div>
      <div class="col-divider"></div>
      <div class="col-right anim anim-4">
        <div class="right-card">{right_html}</div>
      </div>
    </div>
  </div>
  <style>
    .two-col-slide {{
      background: var(--surface);
      padding: 72px 120px;
      justify-content: center;
    }}
    .two-col-inner {{ width: 100%; }}
    .two-col-header {{ margin-bottom: 48px; }}
    .section-label {{
      display: inline-block;
      font-size: 16px; font-weight: 700;
      color: var(--royal-blue);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 16px;
      padding: 4px 14px;
      background: var(--blue-50);
      border-radius: 4px;
    }}
    .col-heading {{
      font-size: 52px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
      padding-left: 16px;
      border-left: 4px solid var(--royal-blue);
    }}
    .two-col-body {{
      display: flex; gap: 0; align-items: flex-start;
    }}
    .col-left {{ flex: 1; padding-right: 60px; }}
    .col-divider {{
      width: 1px;
      background: var(--border);
      align-self: stretch;
      margin: 0 60px;
      flex-shrink: 0;
    }}
    .col-right {{ flex: 1; }}
    .col-bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 20px; }}
    .col-bullet {{
      display: flex; align-items: flex-start; gap: 16px;
      font-size: 26px; color: var(--ink-700);
      line-height: 1.4;
      padding: 16px 20px;
      background: var(--bg);
      border-radius: 8px;
      border: 1px solid var(--border);
    }}
    .col-bullet::before {{
      content: '';
      display: block; flex-shrink: 0;
      width: 6px; height: 6px;
      border-radius: 50%;
      background: var(--royal-blue);
      margin-top: 10px;
    }}
    .right-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 40px;
      font-size: 26px;
      color: var(--ink-700);
      line-height: 1.6;
      box-shadow: var(--shadow-sm);
    }}
    .right-card p {{ margin-bottom: 16px; }}
    .right-card p:last-child {{ margin-bottom: 0; }}
  </style>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 4. DEFINITION TEMPLATE
# ---------------------------------------------------------------------------

def definition_slide(content: dict) -> str:
    term = content.get("term", "")
    definition = content.get("definition", "")
    example = content.get("example", "")

    example_html = ""
    if example:
        example_html = f"""
        <div class="example-card anim anim-4">
          <span class="example-label">Example</span>
          <p class="example-text">{example}</p>
        </div>"""

    return _BASE_HEAD + f"""
<div class="slide definition-slide">
  <div class="def-inner">
    <span class="def-tag anim anim-1">Definition</span>
    <h1 class="def-term anim anim-2">{term}</h1>
    <div class="def-divider anim anim-3"></div>
    <p class="def-body anim anim-3">{definition}</p>
    {example_html}
  </div>
  <style>
    .definition-slide {{
      background: var(--surface);
      padding: 80px 160px;
      justify-content: center;
    }}
    .def-inner {{ max-width: 1280px; width: 100%; }}
    .def-tag {{
      display: inline-block;
      font-size: 16px; font-weight: 700;
      color: var(--midnight-violet);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 20px;
      padding: 4px 14px;
      background: #F8EAFF;
      border-radius: 4px;
    }}
    .def-term {{
      font-size: 84px; font-weight: 900;
      color: var(--royal-blue);
      letter-spacing: -1.5px;
      line-height: 1.05;
      margin-bottom: 32px;
    }}
    .def-divider {{
      width: 72px; height: 3px;
      background: var(--royal-blue);
      border-radius: 2px;
      margin-bottom: 36px;
    }}
    .def-body {{
      font-size: 32px; font-weight: 400;
      color: var(--ink-700);
      line-height: 1.6;
      max-width: 1000px;
      margin-bottom: 48px;
    }}
    .example-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-left: 4px solid var(--sea-green);
      border-radius: 8px;
      padding: 32px 40px;
      max-width: 1000px;
    }}
    .example-label {{
      display: block;
      font-size: 14px; font-weight: 700;
      color: var(--ink-500);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 12px;
    }}
    .example-text {{
      font-size: 26px;
      color: var(--ink-700);
      line-height: 1.5;
      font-style: italic;
    }}
  </style>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 5. DIAGRAM TEMPLATE (Mermaid.js)
# ---------------------------------------------------------------------------

def diagram_slide(content: dict) -> str:
    heading = content.get("heading", content.get("title", ""))
    mermaid_code = content.get("mermaid_code", content.get("description", "graph LR\n  A --> B"))
    caption = content.get("caption", "")

    # If we got a description instead of real mermaid code, create a simple flowchart
    if not any(kw in mermaid_code for kw in ["-->", "---", "graph", "flowchart", "sequenceDiagram", "classDiagram", "pie"]):
        mermaid_code = f"graph LR\n  A[{heading}] --> B[See narration for details]"

    caption_html = f'<p class="diagram-caption anim anim-4">{caption}</p>' if caption else ""

    return _BASE_HEAD + f"""
<div class="slide diagram-slide">
  <div class="diagram-header anim anim-1">
    <h2 class="diagram-heading">{heading}</h2>
  </div>
  <div class="diagram-body anim anim-2">
    <div class="mermaid">{mermaid_code}</div>
  </div>
  {caption_html}
  <style>
    .diagram-slide {{
      background: var(--surface);
      padding: 60px 80px 40px;
      align-items: center;
    }}
    .diagram-header {{
      width: 100%; margin-bottom: 32px;
    }}
    .diagram-heading {{
      font-size: 52px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
      padding-left: 16px;
      border-left: 4px solid var(--royal-blue);
    }}
    .diagram-body {{
      flex: 1;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 40px;
      overflow: hidden;
    }}
    .mermaid {{
      width: 100%;
      text-align: center;
      font-family: var(--font-sans) !important;
    }}
    .diagram-caption {{
      font-size: 20px;
      color: var(--ink-500);
      text-align: center;
      margin-top: 20px;
      font-style: italic;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      themeVariables: {{
        primaryColor: '#EAF0FE',
        primaryTextColor: '#12172B',
        primaryBorderColor: '#01187D',
        lineColor: '#01187D',
        secondaryColor: '#F8EAFF',
        tertiaryColor: '#FCFCFD',
        fontSize: '20px'
      }}
    }});
  </script>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 6. CODE TEMPLATE
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
  <div class="code-header anim anim-1">
    <h2 class="code-heading">{heading}</h2>
    <span class="lang-badge">{language}</span>
  </div>
  <div class="code-block-wrap anim anim-2">
    <pre><code class="language-{language}">{code_escaped}</code></pre>
  </div>
  {explanation_html}
  <style>
    .code-slide {{
      background: var(--surface);
      padding: 64px 120px;
      justify-content: center;
      gap: 32px;
    }}
    .code-header {{
      display: flex; align-items: center; gap: 24px; width: 100%;
    }}
    .code-heading {{
      font-size: 48px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
      padding-left: 16px;
      border-left: 4px solid var(--royal-blue);
    }}
    .lang-badge {{
      font-family: var(--font-mono);
      font-size: 16px; font-weight: 500;
      color: var(--royal-blue);
      background: var(--blue-50);
      padding: 4px 14px;
      border-radius: 999px;
      border: 1px solid #CCD5FE;
      text-transform: lowercase;
    }}
    .code-block-wrap {{
      background: #12172B;
      border-radius: 12px;
      padding: 40px 48px;
      overflow: auto;
      max-height: 640px;
      box-shadow: var(--shadow-md);
      width: 100%;
    }}
    .code-block-wrap pre {{
      margin: 0;
      font-family: var(--font-mono);
      font-size: 22px;
      line-height: 1.65;
      white-space: pre;
    }}
    .code-block-wrap code {{
      font-family: var(--font-mono) !important;
    }}
    .code-explanation {{
      font-size: 24px;
      color: var(--ink-700);
      line-height: 1.5;
      padding: 20px 28px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-left: 4px solid var(--sea-green);
      border-radius: 8px;
      width: 100%;
    }}
    /* Minimal highlight override — hljs will style code tokens */
    .hljs {{ background: transparent !important; color: #c9d1d9; padding: 0 !important; }}
  </style>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 7. CHART TEMPLATE (Chart.js)
# ---------------------------------------------------------------------------

def chart_slide(content: dict) -> str:
    import json as _json
    heading = content.get("heading", content.get("title", ""))
    chart_type = content.get("chart_type", "bar")
    labels = content.get("labels", [])
    values = content.get("values", [])
    caption = content.get("caption", "")

    # Fallback if no chart data
    if not labels or not values:
        labels = ["A", "B", "C"]
        values = [1, 2, 3]

    labels_json = _json.dumps(labels)
    values_json = _json.dumps(values)
    caption_html = f'<p class="chart-caption anim anim-4">{caption}</p>' if caption else ""

    chart_color = "#01187D"
    if chart_type == "line":
        chart_ds_extra = '"fill": false, "tension": 0.3, "borderColor": "' + chart_color + '", "pointBackgroundColor": "' + chart_color + '",'
    else:
        chart_ds_extra = '"backgroundColor": "rgba(1,24,125,0.8)", "borderRadius": 6, "borderSkipped": false,'

    return _BASE_HEAD + f"""
<div class="slide chart-slide">
  <div class="chart-header anim anim-1">
    <h2 class="chart-heading">{heading}</h2>
  </div>
  <div class="chart-wrap anim anim-2">
    <canvas id="myChart"></canvas>
  </div>
  {caption_html}
  <style>
    .chart-slide {{
      background: var(--surface);
      padding: 60px 120px 40px;
      align-items: center;
      gap: 24px;
    }}
    .chart-header {{ width: 100%; }}
    .chart-heading {{
      font-size: 52px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
      padding-left: 16px;
      border-left: 4px solid var(--royal-blue);
    }}
    .chart-wrap {{
      flex: 1;
      width: 100%;
      max-height: 720px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .chart-caption {{
      font-size: 20px;
      color: var(--ink-500);
      font-style: italic;
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
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            bodyFont: {{ family: 'Lato', size: 16 }},
            titleFont: {{ family: 'Lato', size: 16, weight: 'bold' }}
          }}
        }},
        scales: {{
          x: {{
            grid: {{ color: '#EDEFF3' }},
            ticks: {{ font: {{ family: 'Lato', size: 16 }}, color: '#6C727F' }}
          }},
          y: {{
            grid: {{ color: '#EDEFF3' }},
            ticks: {{ font: {{ family: 'Lato', size: 16 }}, color: '#6C727F' }}
          }}
        }}
      }}
    }});
  </script>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# 8. SUMMARY TEMPLATE
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
        takeaways_html += f"""
        <li class="takeaway-item anim anim-{min(i+1, 8)}">
          <span class="takeaway-num">{i:02d}</span>
          <span class="takeaway-text">{text}</span>
        </li>"""

    next_html = ""
    if next_lesson:
        next_html = f"""
        <div class="next-lesson anim anim-7">
          <span class="next-label">Up Next</span>
          <span class="next-title">{next_lesson}</span>
        </div>"""

    return _BASE_HEAD + f"""
<div class="slide summary-slide">
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
      background: var(--surface);
      padding: 72px 160px;
      justify-content: center;
    }}
    .summary-inner {{ max-width: 1280px; width: 100%; }}
    .summary-header {{ margin-bottom: 48px; display: flex; align-items: center; gap: 20px; }}
    .recap-tag {{
      display: inline-flex; align-items: center;
      font-size: 14px; font-weight: 700;
      color: #fff;
      background: var(--royal-blue);
      padding: 6px 16px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1px;
      white-space: nowrap;
    }}
    .summary-heading {{
      font-size: 52px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
    }}
    .takeaway-list {{ list-style: none; display: flex; flex-direction: column; gap: 20px; }}
    .takeaway-item {{
      display: flex; align-items: flex-start; gap: 24px;
      padding: 20px 28px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      box-shadow: var(--shadow-sm);
    }}
    .takeaway-num {{
      flex-shrink: 0;
      width: 44px; height: 44px;
      border-radius: 50%;
      background: var(--royal-blue);
      color: #fff;
      font-size: 18px; font-weight: 900;
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono);
    }}
    .takeaway-text {{
      font-size: 26px;
      color: var(--ink-700);
      line-height: 1.45;
      align-self: center;
    }}
    .next-lesson {{
      display: flex; align-items: center; gap: 20px;
      margin-top: 36px;
      padding: 20px 28px;
      background: var(--blue-50);
      border: 1px solid #CCD5FE;
      border-radius: 8px;
    }}
    .next-label {{
      font-size: 14px; font-weight: 700;
      color: var(--royal-blue);
      text-transform: uppercase;
      letter-spacing: 1px;
      white-space: nowrap;
    }}
    .next-title {{
      font-size: 24px; font-weight: 700;
      color: var(--ink-900);
    }}
  </style>
""" + _BASE_FOOT



# ---------------------------------------------------------------------------
# QUIZ TEMPLATE (bonus — for quiz slide_type)
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

    options_html = ""
    for i, opt in enumerate(options[:4], start=1):
        options_html += f'<li class="quiz-option anim anim-{min(i+1, 8)}">{opt}</li>\n'

    explanation_html = ""
    if explanation:
        explanation_html = f'<p class="quiz-explanation anim anim-6">{explanation}</p>'

    return _BASE_HEAD + f"""
<div class="slide quiz-slide">
  <div class="quiz-inner">
    <span class="quiz-tag anim anim-1">Knowledge Check</span>
    <h2 class="quiz-question anim anim-2">{question}</h2>
    <ul class="quiz-options">{options_html}</ul>
    {explanation_html}
  </div>
  <style>
    .quiz-slide {{
      background: var(--surface);
      padding: 72px 160px;
      justify-content: center;
    }}
    .quiz-inner {{ max-width: 1280px; width: 100%; }}
    .quiz-tag {{
      display: inline-block;
      font-size: 14px; font-weight: 700;
      color: var(--warning-ink, #CD8508);
      background: #FEF7EB;
      border: 1px solid rgba(245,159,10,0.3);
      padding: 4px 14px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 24px;
    }}
    .quiz-question {{
      font-size: 52px; font-weight: 900;
      color: var(--ink-900);
      letter-spacing: -0.6px;
      line-height: 1.2;
      margin-bottom: 44px;
      padding-left: 16px;
      border-left: 4px solid var(--royal-blue);
    }}
    .quiz-options {{ list-style: none; display: flex; flex-direction: column; gap: 18px; }}
    .quiz-option {{
      font-size: 26px;
      color: var(--ink-700);
      padding: 18px 28px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      cursor: default;
      line-height: 1.4;
      box-shadow: var(--shadow-sm);
    }}
    .quiz-explanation {{
      margin-top: 28px;
      font-size: 22px;
      color: var(--ink-500);
      font-style: italic;
      padding: 16px 20px;
      background: #EBFEF8;
      border-left: 4px solid #16A249;
      border-radius: 6px;
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

