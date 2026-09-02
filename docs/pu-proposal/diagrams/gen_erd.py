"""Generates fig7_erd.html — the Kinyo entity relationship diagram.

Laid out on a three-column grid rather than four so that the attribute text is
large enough to read once the figure is scaled to the text width of the page.
Relationship lines are routed orthogonally through fixed channels between the
columns and rows, and every line is pulled back from the box edge so the crow's
foot sits outside the entity rather than on top of its attributes.

Run:  python diagrams/gen_erd.py
"""

import math
from pathlib import Path

BOX_W = 390
HEADER_H = 48
ROW_H = 38
FONT = 28
LABEL_FONT = 24
END_GAP = 16          # distance a line stops short of the box it points at

COL_CX = [255, 750, 1245]
ROW_TOP = [70, 360, 650, 940, 1230, 1664]
CANVAS_W = 1500
CANVAS_H = 1930

# name, column, row, [(type, attribute, key), ...]
ENTITIES = [
    ("USER", 0, 0, [
        ("uuid", "id", "PK"), ("str", "email", "UK"),
        ("str", "password_hash", ""), ("bool", "is_platform_admin", "")]),
    ("MEMBERSHIP", 1, 0, [
        ("uuid", "id", "PK"), ("uuid", "user_id", "FK"),
        ("uuid", "tenant_id", "FK"), ("str", "role", "")]),
    ("TENANT", 2, 0, [
        ("uuid", "id", "PK"), ("str", "name", ""),
        ("str", "slug", "UK"), ("str", "status", "")]),

    ("PRODUCT", 0, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "title", ""), ("str", "status", "")]),
    ("COLLECTION", 1, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "title", "")]),
    ("DOMAIN", 2, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "hostname", "UK"), ("bool", "is_primary", "")]),

    ("PRODUCT_VARIANT", 0, 2, [
        ("uuid", "id", "PK"), ("uuid", "product_id", "FK"),
        ("str", "sku", "UK"), ("dec", "price", "")]),
    ("CUSTOMER", 1, 2, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "email", ""), ("str", "phone", "")]),
    ("ADDRESS", 2, 2, [
        ("uuid", "id", "PK"), ("uuid", "customer_id", "FK"),
        ("str", "city", ""), ("str", "province", "")]),

    ("INVENTORY_ITEM", 0, 3, [
        ("uuid", "id", "PK"), ("uuid", "variant_id", "FK"),
        ("int", "qty_on_hand", ""), ("int", "qty_reserved", "")]),
    ("CART", 1, 3, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("uuid", "customer_id", "FK")]),
    ("CART_ITEM", 2, 3, [
        ("uuid", "id", "PK"), ("uuid", "cart_id", "FK"),
        ("uuid", "variant_id", "FK"), ("int", "quantity", "")]),

    ("DISCOUNT", 0, 4, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "code", "UK"), ("dec", "value", "")]),
    ("ORDERS", 1, 4, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("uuid", "customer_id", "FK"), ("uuid", "address_id", "FK"),
        ("uuid", "discount_id", "FK"), ("str", "order_number", "UK"),
        ("str", "status", ""), ("dec", "total", "")]),
    ("ORDER_ITEM", 2, 4, [
        ("uuid", "id", "PK"), ("uuid", "order_id", "FK"),
        ("uuid", "variant_id", "FK"), ("int", "quantity", "")]),

    ("SHIPPING_ZONE", 0, 5, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "name", ""), ("dec", "base_rate", "")]),
]

BOX = {}
for _n, _c, _r, _a in ENTITIES:
    BOX[_n] = {
        "x": COL_CX[_c] - BOX_W // 2,
        "y": ROW_TOP[_r],
        "w": BOX_W,
        "h": HEADER_H + ROW_H * len(_a),
        "cx": COL_CX[_c],
        "attrs": _a,
    }


def L(n, f=0.5):
    b = BOX[n]
    return (b["x"], b["y"] + b["h"] * f)


def R(n, f=0.5):
    b = BOX[n]
    return (b["x"] + b["w"], b["y"] + b["h"] * f)


def T(n, f=0.5):
    b = BOX[n]
    return (b["x"] + b["w"] * f, b["y"])


def B(n, f=0.5):
    b = BOX[n]
    return (b["x"] + b["w"] * f, b["y"] + b["h"])


def vchan(i):
    """x of the routing channel between column i and column i + 1."""
    return (COL_CX[i] + BOX_W / 2 + COL_CX[i + 1] - BOX_W / 2) / 2


LEFT_CH = 30
RIGHT_CH = CANVAS_W - 30

RELATIONS = []


def _pull(p, q, gap):
    """Move p towards q by `gap` so a marker sits clear of the entity box."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dy)
    if d == 0:
        return p
    return (p[0] + dx / d * gap, p[1] + dy / d * gap)


def rel(pts, ms, me, label, lx, ly, anchor="middle"):
    pts = list(pts)
    pts[0] = _pull(pts[0], pts[1], END_GAP)
    pts[-1] = _pull(pts[-1], pts[-2], END_GAP)
    d = "M" + " L".join(f"{round(x)} {round(y)}" for x, y in pts)
    RELATIONS.append((d, ms, me, label, lx, ly, anchor))


def hrel(a, b, y, ms, me, label, side="right"):
    """Horizontal relation between two entities side by side, at absolute y."""
    if side == "right":
        p0, p1 = (BOX[a]["x"] + BOX[a]["w"], y), (BOX[b]["x"], y)
    else:
        p0, p1 = (BOX[a]["x"], y), (BOX[b]["x"] + BOX[b]["w"], y)
    rel([p0, p1], ms, me, label, (p0[0] + p1[0]) / 2, y - 13)


# --- identity and tenancy -------------------------------------------------
hrel("USER", "MEMBERSHIP", 150, "one", "many", "holds")
hrel("TENANT", "MEMBERSHIP", 200, "one", "many", "grants", side="left")
rel([B("TENANT", 0.5), T("DOMAIN", 0.5)], "one", "many", "has",
    COL_CX[2] + 16, 315, "start")

rel([B("TENANT", 0.14), (B("TENANT", 0.14)[0], 290),
     (T("PRODUCT", 0.5)[0], 290), T("PRODUCT", 0.5)],
    "one", "many", "owns", 420, 278)
rel([B("TENANT", 0.3), (B("TENANT", 0.3)[0], 322),
     (T("COLLECTION", 0.62)[0], 322), T("COLLECTION", 0.62)],
    "one", "many", "owns", 900, 310)
rel([R("TENANT", 0.7), (RIGHT_CH, R("TENANT", 0.7)[1]),
     (RIGHT_CH, 600), (T("CUSTOMER", 0.8)[0], 600), T("CUSTOMER", 0.8)],
    "one", "many", "owns", 1180, 588)

# --- catalogue ------------------------------------------------------------
hrel("PRODUCT", "COLLECTION", 470, "many", "many", "grouped in")
rel([B("PRODUCT", 0.4), T("PRODUCT_VARIANT", 0.4)], "one", "many",
    "sold as", 205, 610, "end")
rel([B("PRODUCT_VARIANT", 0.4), T("INVENTORY_ITEM", 0.4)], "one", "one",
    "stocked as", 205, 900, "end")

rel([B("PRODUCT_VARIANT", 0.78), (B("PRODUCT_VARIANT", 0.78)[0], 890),
     (T("CART_ITEM", 0.45)[0], 890), T("CART_ITEM", 0.45)],
    "one", "many", "chosen in", 800, 878)

# --- customers, carts -----------------------------------------------------
hrel("CUSTOMER", "ADDRESS", 740, "one", "many", "saves")
rel([B("CUSTOMER", 0.4), T("CART", 0.4)], "one", "many",
    "owns", COL_CX[1] + 16, 928, "start")
hrel("CART", "CART_ITEM", 1030, "one", "many", "contains")

# --- orders ---------------------------------------------------------------
rel([L("CUSTOMER", 0.72), (vchan(0), L("CUSTOMER", 0.72)[1]),
     (vchan(0), 1300), L("ORDERS", 0.21)],
    "one", "many", "places", vchan(0) - 12, 1150, "end")

rel([L("ADDRESS", 0.62), (vchan(1), L("ADDRESS", 0.62)[1]),
     (vchan(1), 1180), (T("ORDERS", 0.72)[0], 1180), T("ORDERS", 0.72)],
    "one", "many", "ships to", 1010, 1168)

hrel("DISCOUNT", "ORDERS", 1330, "one", "many", "reduces")
hrel("ORDERS", "ORDER_ITEM", 1330, "one", "many", "contains")

rel([L("PRODUCT_VARIANT", 0.82), (LEFT_CH, L("PRODUCT_VARIANT", 0.82)[1]),
     (LEFT_CH, 1640), (B("ORDER_ITEM", 0.5)[0], 1640), B("ORDER_ITEM", 0.5)],
    "one", "many", "sold in", 700, 1628)

rel([T("SHIPPING_ZONE", 0.62), (T("SHIPPING_ZONE", 0.62)[0], 1608),
     (B("ORDERS", 0.4)[0], 1608), B("ORDERS", 0.4)],
    "one", "many", "prices", 560, 1596)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    o = [f'''<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: #fff; }}
  #figure {{ width: {CANVAS_W}px; background: #fff; }}
  text {{ font-family: "Times New Roman", Georgia, serif; fill: #12263a; }}
  .ent {{ font-size: {FONT + 2}px; font-weight: bold; text-anchor: middle; }}
  .at  {{ font-size: {FONT}px; }}
  .ty  {{ font-size: {FONT}px; fill: #5c6b7a; }}
  .ky  {{ font-size: {FONT - 4}px; font-weight: bold; text-anchor: end; fill: #8f4667; }}
  .rl  {{ font-size: {LABEL_FONT}px; font-style: italic; fill: #6b3a2e; }}
  rect.box {{ fill: #ffffff; stroke: #3b6ea5; stroke-width: 2; }}
  rect.hdr {{ fill: #eef4fb; stroke: #3b6ea5; stroke-width: 2; }}
  line.sep {{ stroke: #cfd9e4; stroke-width: 1; }}
  path.rel {{ stroke: #4a4a4a; stroke-width: 2; fill: none; }}
</style>
<div id="figure">
<svg width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="one" viewBox="0 0 26 26" refX="20" refY="13"
            markerWidth="26" markerHeight="26" markerUnits="userSpaceOnUse"
            orient="auto-start-reverse">
      <path d="M16 4 L16 22" stroke="#4a4a4a" stroke-width="1.8" fill="none"/>
    </marker>
    <marker id="many" viewBox="0 0 26 26" refX="3" refY="13"
            markerWidth="26" markerHeight="26" markerUnits="userSpaceOnUse"
            orient="auto-start-reverse">
      <path d="M22 4 L3 13 L22 22 M3 13 L22 13"
            stroke="#4a4a4a" stroke-width="1.6" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
''']

    for name, _c, _r, attrs in ENTITIES:
        b = BOX[name]
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        o.append(f'\n  <rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>')
        o.append(f'  <rect class="hdr" x="{x}" y="{y}" width="{w}" height="{HEADER_H}" rx="3"/>')
        o.append(f'  <text class="ent" x="{b["cx"]}" y="{y + 34}">{esc(name)}</text>')
        for i, (ty, at, ky) in enumerate(attrs):
            row_y = y + HEADER_H + ROW_H * i
            base = row_y + 28
            if i:
                o.append(f'  <line class="sep" x1="{x + 10}" y1="{row_y}" '
                         f'x2="{x + w - 10}" y2="{row_y}"/>')
            o.append(f'  <text class="ty" x="{x + 16}" y="{base}">{esc(ty)}</text>')
            o.append(f'  <text class="at" x="{x + 104}" y="{base}">{esc(at)}</text>')
            if ky:
                o.append(f'  <text class="ky" x="{x + w - 14}" y="{base}">{esc(ky)}</text>')

    for d, ms, me, label, lx, ly, anchor in RELATIONS:
        o.append(f'  <path class="rel" d="{d}" '
                 f'marker-start="url(#{ms})" marker-end="url(#{me})"/>')
        o.append(f'  <text class="rl" x="{round(lx)}" y="{round(ly)}" '
                 f'text-anchor="{anchor}">{esc(label)}</text>')

    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig7_erd.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
