"""Generates fig8_gantt.html — the project Gantt chart.

Run:  python diagrams/gen_gantt.py
"""

from pathlib import Path

CANVAS_W = 1560
LABEL_W = 470
LEFT = 30
TOP = 96
ROW_H = 52
BAR_H = 30
FONT = 22
FONT_HEAD = 24

MONTHS = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]

# activity, start month (1-based), duration in months
TASKS = [
    ("Requirement analysis and literature review", 1, 2),
    ("System design (architecture, DFD, ER, use case)", 2, 2),
    ("Database design and migration setup", 3, 1),
    ("Tenancy and authentication module", 3, 2),
    ("Catalogue, inventory and storefront module", 4, 2),
    ("Cart, checkout and order module", 5, 1),
    ("Seller dashboard and admin console", 5, 2),
    ("Integration of modules", 5, 1),
    ("Testing (unit, integration, acceptance)", 5, 2),
    ("Deployment and domain configuration", 6, 1),
    ("Documentation and report writing", 1, 6),
]

COL_W = (CANVAS_W - LEFT * 2 - LABEL_W) / len(MONTHS)
CANVAS_H = TOP + ROW_H * len(TASKS) + 40


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    grid_x = LEFT + LABEL_W
    o = [f'''<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: #fff; }}
  #figure {{ width: {CANVAS_W}px; background: #fff; }}
  text {{ font-family: "Times New Roman", Georgia, serif; fill: #12263a; }}
  .hd {{ font-size: {FONT_HEAD}px; font-weight: bold; text-anchor: middle; }}
  .lb {{ font-size: {FONT}px; }}
  rect.bar {{ fill: #4a7ebb; stroke: #2f5a8c; stroke-width: 1.2; }}
  line.grid {{ stroke: #d5dde6; stroke-width: 1; }}
  line.rule {{ stroke: #4a4a4a; stroke-width: 1.6; }}
</style>
<div id="figure">
<svg width="{CANVAS_W}" height="{round(CANVAS_H)}"
     viewBox="0 0 {CANVAS_W} {round(CANVAS_H)}" xmlns="http://www.w3.org/2000/svg">
''']

    o.append(f'  <text class="hd" x="{LEFT + LABEL_W / 2}" y="{TOP - 34}">Activity</text>')
    for i, mth in enumerate(MONTHS):
        cx = grid_x + COL_W * (i + 0.5)
        o.append(f'  <text class="hd" x="{round(cx)}" y="{TOP - 34}">{esc(mth)}</text>')

    o.append(f'  <line class="rule" x1="{LEFT}" y1="{TOP - 60}" '
             f'x2="{CANVAS_W - LEFT}" y2="{TOP - 60}"/>')
    o.append(f'  <line class="rule" x1="{LEFT}" y1="{TOP - 18}" '
             f'x2="{CANVAS_W - LEFT}" y2="{TOP - 18}"/>')

    bottom = TOP + ROW_H * len(TASKS)
    for i in range(len(MONTHS) + 1):
        x = grid_x + COL_W * i
        o.append(f'  <line class="grid" x1="{round(x)}" y1="{TOP - 18}" '
                 f'x2="{round(x)}" y2="{bottom}"/>')

    for r, (name, start, dur) in enumerate(TASKS):
        y = TOP + ROW_H * r
        o.append(f'  <text class="lb" x="{LEFT}" y="{y + 32}">{esc(name)}</text>')
        bx = grid_x + COL_W * (start - 1) + 5
        bw = COL_W * dur - 10
        o.append(f'  <rect class="bar" x="{round(bx)}" y="{round(y + 12)}" '
                 f'width="{round(bw)}" height="{BAR_H}" rx="4"/>')
        o.append(f'  <line class="grid" x1="{LEFT}" y1="{y + ROW_H}" '
                 f'x2="{CANVAS_W - LEFT}" y2="{y + ROW_H}"/>')

    o.append(f'  <line class="rule" x1="{LEFT}" y1="{bottom}" '
             f'x2="{CANVAS_W - LEFT}" y2="{bottom}"/>')
    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig8_gantt.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
