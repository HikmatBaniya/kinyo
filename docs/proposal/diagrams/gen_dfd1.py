"""Generates fig6_dfd1.html — the Level 1 data flow diagram for Kinyo.

Mermaid routes DFD edges as long curves that cross each other, so the diagram
is emitted directly as SVG using the conventional DFD column layout: external
entities on the left, numbered processes down the centre, data stores on the
right, with orthogonal flow routing in fixed lanes.

Run:  python diagrams/gen_dfd1.py
"""

from pathlib import Path

CANVAS_W, CANVAS_H = 1290, 1130
FONT_NODE = 24
FONT_LABEL = 21

ENT_CX, ENT_W, ENT_H = 150, 220, 76
PROC_CX, PROC_R = 620, 76
STORE_X, STORE_W, STORE_H = 940, 320, 66

ROW_Y = [110, 290, 470, 650, 830, 1010]

ENTITIES = {
    "SO": ("Store Owner", 200),
    "SS": ("Store Staff", 560),
    "CU": ("Customer", 740),
    "PA": ("Platform\nAdministrator", 920),
}

PROCESSES = {
    "P1": ("1.0", "Manage Users\nand Access", ROW_Y[0]),
    "P2": ("2.0", "Provision Store\nand Domain", ROW_Y[1]),
    "P3": ("3.0", "Manage Catalog\nand Inventory", ROW_Y[2]),
    "P4": ("4.0", "Serve Storefront\nand Cart", ROW_Y[3]),
    "P5": ("5.0", "Process Order", ROW_Y[4]),
    "P6": ("6.0", "Generate Reports", ROW_Y[5]),
}

STORES = {
    "D1": ("D1   User and Role Store", ROW_Y[0]),
    "D2": ("D2   Tenant and Domain Store", ROW_Y[1]),
    "D3": ("D3   Product and Inventory Store", ROW_Y[2]),
    "D4": ("D4   Cart Store", ROW_Y[3]),
    "D5": ("D5   Order Store", ROW_Y[4]),
    "D6": ("D6   Customer Store", ROW_Y[5]),
}

ENT_R = ENT_CX + ENT_W / 2          # 260
PROC_L = PROC_CX - PROC_R           # 544
PROC_R_X = PROC_CX + PROC_R         # 696

FLOWS = []


def flow(pts, label, lx, ly, anchor="middle", double=False):
    FLOWS.append((pts, label, lx, ly, anchor, double))


def ent_to_proc(ent, proc, lane, label, dy=0, reverse=False, f=0.5, double=False):
    """Orthogonal route between a left-hand entity and a centre process."""
    ey = ENTITIES[ent][1] + dy
    py = PROCESSES[proc][2] + dy
    pts = [(ENT_R, ey), (lane, ey), (lane, py), (PROC_L, py)]
    if reverse:
        pts = list(reversed(pts))
    ly = ey + (py - ey) * f
    if lane >= 400:      # keep the label clear of the process circles
        flow(pts, label, lane - 8, ly, "end", double)
    else:
        flow(pts, label, lane + 8, ly, "start", double)


def proc_to_store(proc, store, lane, label, dy=0, double=False, reverse=False, f=0.5):
    py = PROCESSES[proc][2] + dy
    sy = STORES[store][1] + dy
    if py == sy:
        pts = [(PROC_R_X, py), (STORE_X, sy)]
        lx, ly, anchor = (PROC_R_X + STORE_X) / 2, py - 12, "middle"
    else:
        pts = [(PROC_R_X, py), (lane, py), (lane, sy), (STORE_X, sy)]
        lx, ly, anchor = PROC_R_X + 12, py - 10, "start"
    if reverse:
        pts = list(reversed(pts))
    flow(pts, label, lx, ly, anchor, double)


# --- external entity flows -------------------------------------------------
ent_to_proc("SO", "P1", 300, "credentials /|session token", dy=-30, f=0.30, double=True)
ent_to_proc("SO", "P2", 360, "store and|domain data", dy=-10, f=0.55, double=True)
ent_to_proc("SO", "P3", 420, "product data", dy=10, f=0.72)
ent_to_proc("SO", "P6", 480, "sales report", dy=30, reverse=True, f=0.95)

ent_to_proc("SS", "P1", 360, "credentials", dy=30, f=0.20)
ent_to_proc("SS", "P3", 300, "stock updates", dy=30, f=0.40)
ent_to_proc("SS", "P5", 420, "fulfilment update /|order queue", dy=-30, f=0.35, double=True)

ent_to_proc("CU", "P4", 300, "browse and|cart actions", dy=-16, f=0.30, double=True)
ent_to_proc("CU", "P5", 360, "checkout details /|order status", dy=16, f=0.62, double=True)

ent_to_proc("PA", "P1", 480, "credentials", dy=30, f=0.45)
ent_to_proc("PA", "P2", 420, "approval decision", dy=10, f=0.22)
ent_to_proc("PA", "P6", 300, "platform summary", dy=-30, reverse=True, f=0.55)

# --- data store flows ------------------------------------------------------
proc_to_store("P1", "D1", 0, "user and role records", double=True)
proc_to_store("P2", "D2", 0, "tenant and domain records", double=True)
proc_to_store("P3", "D3", 0, "product and stock records", double=True)
proc_to_store("P4", "D4", 0, "cart records", double=True)
proc_to_store("P5", "D5", 0, "order records", double=True)

proc_to_store("P4", "D2", 730, "tenant lookup", dy=-30)
proc_to_store("P4", "D3", 780, "product lookup", dy=30)
proc_to_store("P5", "D4", 830, "cart contents", dy=-52)
proc_to_store("P5", "D6", 730, "customer records", dy=-26, double=True)
proc_to_store("P5", "D3", 880, "stock reservation", dy=30)
proc_to_store("P6", "D5", 780, "order history", dy=-26)
proc_to_store("P6", "D3", 910, "catalog data", dy=26)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def multiline(text, x, y, cls, line_h):
    parts = text.split("\n")
    start = y - (len(parts) - 1) * line_h / 2
    return "".join(
        f'<text class="{cls}" x="{round(x)}" y="{round(start + i * line_h)}">{esc(p)}</text>'
        for i, p in enumerate(parts))


def build():
    o = [f'''<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: #fff; }}
  #figure {{ width: {CANVAS_W}px; background: #fff; }}
  text {{ font-family: "Times New Roman", Georgia, serif; fill: #12263a; }}
  .nd {{ font-size: {FONT_NODE}px; text-anchor: middle; }}
  .num {{ font-size: {FONT_NODE}px; font-weight: bold; text-anchor: middle; }}
  .fl {{ font-size: {FONT_LABEL}px; fill: #6b3a2e; }}
  rect.ent {{ fill: #f6f2e8; stroke: #8a7333; stroke-width: 2; }}
  circle.pr {{ fill: #eef4fb; stroke: #3b6ea5; stroke-width: 2; }}
  rect.st {{ fill: #eaf5ee; stroke: #3f7d54; stroke-width: 2; }}
  line.stbar {{ stroke: #3f7d54; stroke-width: 2; }}
  path.fw {{ stroke: #4a4a4a; stroke-width: 1.6; fill: none; marker-end: url(#ah); }}
  path.fw2 {{ stroke: #4a4a4a; stroke-width: 1.6; fill: none;
              marker-end: url(#ah); marker-start: url(#ah); }}
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

    # flows first, nodes drawn over them
    for pts, label, lx, ly, anchor, double in FLOWS:
        d = "M" + " L".join(f"{round(x)} {round(y)}" for x, y in pts)
        cls = "fw2" if double else "fw"
        o.append(f'  <path class="{cls}" d="{d}"/>')
        parts = label.split("|")
        for i, p in enumerate(parts):
            o.append(f'  <text class="fl" x="{round(lx)}" y="{round(ly + i * 22)}" '
                     f'text-anchor="{anchor}">{esc(p)}</text>')

    for _k, (name, cy) in ENTITIES.items():
        x = ENT_CX - ENT_W / 2
        y = cy - ENT_H / 2
        o.append(f'\n  <rect class="ent" x="{round(x)}" y="{round(y)}" '
                 f'width="{ENT_W}" height="{ENT_H}" rx="3"/>')
        o.append("  " + multiline(name, ENT_CX, cy + 8, "nd", 26))

    for _k, (num, name, cy) in PROCESSES.items():
        o.append(f'\n  <circle class="pr" cx="{PROC_CX}" cy="{cy}" r="{PROC_R}"/>')
        o.append(f'  <text class="num" x="{PROC_CX}" y="{cy - 24}">{esc(num)}</text>')
        o.append("  " + multiline(name, PROC_CX, cy + 16, "nd", 26))

    for _k, (name, cy) in STORES.items():
        y = cy - STORE_H / 2
        o.append(f'\n  <rect class="st" x="{STORE_X}" y="{round(y)}" '
                 f'width="{STORE_W}" height="{STORE_H}"/>')
        o.append(f'  <line class="stbar" x1="{STORE_X + 46}" y1="{round(y)}" '
                 f'x2="{STORE_X + 46}" y2="{round(y + STORE_H)}"/>')
        o.append(f'  <text class="nd" x="{STORE_X + STORE_W / 2 + 16}" '
                 f'y="{round(cy + 8)}">{esc(name.split("   ")[1])}</text>')
        o.append(f'  <text class="num" x="{STORE_X + 23}" y="{round(cy + 8)}">'
                 f'{esc(name.split("   ")[0])}</text>')

    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig6_dfd1.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
