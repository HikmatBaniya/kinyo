"""Generates fig1_sdlc.html — the iterative-incremental SDLC model adopted.

Run:  python diagrams/gen_sdlc.py
"""

from pathlib import Path

CANVAS_W, CANVAS_H = 1400, 880
FONT = 23
FONT_TITLE = 25

BOX_W, BOX_H, GAP = 230, 78, 30
X0 = 40
ROW_Y = [250, 470, 690]

PHASES = ["Requirement\nAnalysis", "Design", "Implementation", "Testing", "Evaluation"]
ITERATIONS = [
    "Iteration 1: Core Platform (authentication, tenancy, store provisioning)",
    "Iteration 2: Catalog and Storefront (products, themes, domain routing)",
    "Iteration 3: Cart, Orders and Administration (checkout, reports, admin)",
]


def bx(i):
    return X0 + i * (BOX_W + GAP)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(o, x, y, w, h, cls, text, font=FONT):
    o.append(f'  <rect class="{cls}" x="{round(x)}" y="{round(y)}" '
             f'width="{round(w)}" height="{round(h)}" rx="4"/>')
    parts = text.split("\n")
    start = y + h / 2 + 8 - (len(parts) - 1) * (font * 0.62)
    for i, p in enumerate(parts):
        o.append(f'  <text class="nd" x="{round(x + w / 2)}" '
                 f'y="{round(start + i * font * 1.24)}">{esc(p)}</text>')


def build():
    o = [f'''<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: #fff; }}
  #figure {{ width: {CANVAS_W}px; background: #fff; }}
  text {{ font-family: "Times New Roman", Georgia, serif; fill: #12263a; }}
  .nd {{ font-size: {FONT}px; text-anchor: middle; }}
  .it {{ font-size: {FONT_TITLE}px; font-weight: bold; fill: #12263a; }}
  .fb {{ font-size: {FONT - 2}px;  fill: #6b3a2e; }}
  rect.ph {{ fill: #eef4fb; stroke: #3b6ea5; stroke-width: 1.8; }}
  rect.tm {{ fill: #f6f2e8; stroke: #8a7333; stroke-width: 2; }}
  rect.band {{ fill: none; stroke: #c9d4e0; stroke-width: 1.4; stroke-dasharray: 7 5; }}
  path.fl {{ stroke: #4a4a4a; stroke-width: 1.8; fill: none; marker-end: url(#ah); }}
  path.fb {{ stroke: #8f4667; stroke-width: 1.8; fill: none;
             stroke-dasharray: 7 5; marker-end: url(#ahp); }}
</style>
<div id="figure">
<svg width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="#4a4a4a"/>
    </marker>
    <marker id="ahp" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="#8f4667"/>
    </marker>
  </defs>
''']

    # project initiation
    box(o, X0, 60, BOX_W, BOX_H, "tm", "Project Initiation")
    o.append(f'  <path class="fl" d="M{X0 + BOX_W / 2} 138 '
             f'L{X0 + BOX_W / 2} {ROW_Y[0] - 82}"/>')

    for r, (y, title) in enumerate(zip(ROW_Y, ITERATIONS)):
        o.append(f'\n  <rect class="band" x="{X0 - 18}" y="{y - 74}" '
                 f'width="{5 * BOX_W + 4 * GAP + 36}" height="{BOX_H + 96}" rx="6"/>')
        o.append(f'  <text class="it" x="{X0 - 4}" y="{y - 42}">{esc(title)}</text>')
        for i, ph in enumerate(PHASES):
            box(o, bx(i), y, BOX_W, BOX_H, "ph", ph)
            if i:
                o.append(f'  <path class="fl" d="M{bx(i) - GAP} {y + BOX_H / 2} '
                         f'L{bx(i) - 6} {y + BOX_H / 2}"/>')

        if r < len(ROW_Y) - 1:
            ey = y + BOX_H / 2
            ny = ROW_Y[r + 1] + BOX_H / 2
            right = bx(4) + BOX_W
            o.append(f'  <path class="fb" d="M{right} {ey} L{right + 34} {ey} '
                     f'L{right + 34} {(ey + ny) / 2} L{X0 - 34} {(ey + ny) / 2} '
                     f'L{X0 - 34} {ny} L{X0 - 6} {ny}"/>')
            o.append(f'  <text class="fb" x="{round(CANVAS_W / 2)}" '
                     f'y="{round((ey + ny) / 2 - 10)}" text-anchor="middle">'
                     f'feedback from evaluation refines the next iteration</text>')

    # deployment
    last = ROW_Y[-1]
    dep_x = bx(4)
    box(o, dep_x, 800, BOX_W, BOX_H, "tm", "Deployment and\nDocumentation")
    o.append(f'  <path class="fl" d="M{dep_x + BOX_W / 2} {last + BOX_H + 22} '
             f'L{dep_x + BOX_W / 2} 794"/>')

    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig1_sdlc.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
