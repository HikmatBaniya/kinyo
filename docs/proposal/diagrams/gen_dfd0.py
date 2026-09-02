"""Generates fig5_dfd0.html — the Level 0 (context) data flow diagram.

Mermaid clips the process label inside the circle, so the context diagram is
emitted directly as SVG.

Run:  python diagrams/gen_dfd0.py
"""

import math
from pathlib import Path

CANVAS_W, CANVAS_H = 1620, 790
CX, CY, R = 810, 395, 175
ENT_W, ENT_H = 250, 84
FONT = 30
FONT_LABEL = 28

# name, centre, side the flows leave from
ENTITIES = [
    ("Store Owner", (190, 195), "right"),
    ("Store Staff", (190, 620), "right"),
    ("Customer", (1430, 195), "left"),
    ("Platform\nAdministrator", (1430, 620), "left"),
]

# entity index, label into the platform, label out of the platform
FLOWS = [
    (0, "store details, product|data, discount rules",
        "store dashboard, sales|reports, order alerts"),
    (1, "stock updates,|fulfilment status", "order queue,|inventory alerts"),
    (2, "search terms, cart|items, order details",
        "product listings, cart|summary, order status"),
    (3, "store approval|decisions, settings",
        "store registry, platform|activity summary"),
]

ARROWS = []   # (x1, y1, x2, y2)
LABELS = []   # (text, x, y, anchor)


def add_flow(ent_idx, label_in, label_out):
    name, (ex, ey), side = ENTITIES[ent_idx]
    edge_x = ex + ENT_W / 2 if side == "right" else ex - ENT_W / 2
    sign = 1 if side == "right" else -1

    for k, (text, inbound) in enumerate([(label_in, True), (label_out, False)]):
        off = -32 if k == 0 else 32
        px, py = edge_x, ey + off
        dx, dy = CX - px, CY - py
        dist = math.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist
        # perpendicular offset so the two arrows of a pair stay apart
        perp = (-uy * off * 0.9 * sign, ux * off * 0.9 * sign)
        bx, by = CX - ux * R + perp[0], CY - uy * R + perp[1]
        if inbound:
            ARROWS.append((px, py, bx, by))
        else:
            ARROWS.append((bx, by, px, py))

        t = 0.15
        lx = px + (bx - px) * t + perp[0]
        ly = py + (by - py) * t + perp[1]
        anchor = "start" if sign > 0 else "end"
        lx += 14 * sign
        LABELS.append((text, lx, ly - 6, anchor))


for idx, li, lo in FLOWS:
    add_flow(idx, li, lo)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    o = [f'''<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: #fff; }}
  #figure {{ width: {CANVAS_W}px; background: #fff; }}
  text {{ font-family: "Times New Roman", Georgia, serif; fill: #12263a; }}
  .nd {{ font-size: {FONT}px; text-anchor: middle; }}
  .num {{ font-size: {FONT + 2}px; font-weight: bold; text-anchor: middle; }}
  .fl {{ font-size: {FONT_LABEL}px; fill: #6b3a2e; }}
  rect.ent {{ fill: #f6f2e8; stroke: #8a7333; stroke-width: 2; }}
  circle.pr {{ fill: #eef4fb; stroke: #3b6ea5; stroke-width: 2.4; }}
  path.fw {{ stroke: #4a4a4a; stroke-width: 1.7; fill: none; marker-end: url(#ah); }}
</style>
<div id="figure">
<svg width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="#4a4a4a"/>
    </marker>
  </defs>
''']

    for x1, y1, x2, y2 in ARROWS:
        o.append(f'  <path class="fw" d="M{round(x1)} {round(y1)} '
                 f'L{round(x2)} {round(y2)}"/>')

    for text, x, y, anchor in LABELS:
        for i, part in enumerate(text.split("|")):
            o.append(f'  <text class="fl" x="{round(x)}" y="{round(y + i * 32)}" '
                     f'text-anchor="{anchor}">{esc(part)}</text>')

    o.append(f'\n  <circle class="pr" cx="{CX}" cy="{CY}" r="{R}"/>')
    o.append(f'  <text class="num" x="{CX}" y="{CY - 60}">0</text>')
    for i, line in enumerate(["Kinyo Multi-Tenant", "E-Commerce Platform"]):
        o.append(f'  <text class="nd" x="{CX}" y="{CY - 8 + i * 38}">{esc(line)}</text>')

    for name, (ex, ey), _side in ENTITIES:
        o.append(f'\n  <rect class="ent" x="{round(ex - ENT_W / 2)}" '
                 f'y="{round(ey - ENT_H / 2)}" width="{ENT_W}" height="{ENT_H}" rx="3"/>')
        parts = name.split("\n")
        start = ey + 10 - (len(parts) - 1) * 17
        for i, part in enumerate(parts):
            o.append(f'  <text class="nd" x="{ex}" y="{round(start + i * 34)}">'
                     f'{esc(part)}</text>')

    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig5_dfd0.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
