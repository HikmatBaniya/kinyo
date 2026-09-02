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
END_GAP = 0           # lines run right up to the entity they connect

COL_CX = [255, 750, 1245]
ROW_TOP = [70, 360, 650, 940, 1230, 1668]
CANVAS_W = 1500
CANVAS_H = 1940

# name, column, row, [(type, attribute, key), ...]
#
# Placement rule: every relationship must join boxes that are neighbours in the
# grid, so a line is a short hop and its two ends are obvious. Nothing is routed
# around the outside of the figure.
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

    ("DOMAIN", 0, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "hostname", "UK"), ("bool", "is_primary", "")]),
    ("COLLECTION", 1, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "title", "")]),
    ("PRODUCT", 2, 1, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "title", ""), ("str", "status", "")]),

    ("CUSTOMER", 0, 2, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "email", ""), ("str", "phone", "")]),
    ("CART", 1, 2, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("uuid", "customer_id", "FK")]),
    ("PRODUCT_VARIANT", 2, 2, [
        ("uuid", "id", "PK"), ("uuid", "product_id", "FK"),
        ("str", "sku", "UK"), ("dec", "price", "")]),

    ("ADDRESS", 0, 3, [
        ("uuid", "id", "PK"), ("uuid", "customer_id", "FK"),
        ("str", "city", ""), ("str", "province", "")]),
    ("CART_ITEM", 1, 3, [
        ("uuid", "id", "PK"), ("uuid", "cart_id", "FK"),
        ("uuid", "variant_id", "FK"), ("int", "quantity", "")]),
    ("INVENTORY_ITEM", 2, 3, [
        ("uuid", "id", "PK"), ("uuid", "variant_id", "FK"),
        ("int", "qty_on_hand", ""), ("int", "qty_reserved", "")]),

    ("ORDERS", 0, 4, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("uuid", "customer_id", "FK"), ("uuid", "address_id", "FK"),
        ("uuid", "discount_id", "FK"), ("str", "order_number", "UK"),
        ("str", "status", ""), ("dec", "total", "")]),
    ("ORDER_ITEM", 1, 4, [
        ("uuid", "id", "PK"), ("uuid", "order_id", "FK"),
        ("uuid", "variant_id", "FK"), ("int", "quantity", "")]),

    ("SHIPPING_ZONE", 0, 5, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "name", ""), ("dec", "base_rate", "")]),
    ("DISCOUNT", 1, 5, [
        ("uuid", "id", "PK"), ("uuid", "tenant_id", "FK"),
        ("str", "code", "UK"), ("dec", "value", "")]),
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


def vchan(i, offset=0):
    """x of the routing channel between column i and column i + 1."""
    return (COL_CX[i] + BOX_W / 2 + COL_CX[i + 1] - BOX_W / 2) / 2 + offset


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


# The notation has to stay readable once the figure is scaled to the width of
# the page, so it is drawn much larger than the line weight would suggest.
CARD_BACK = 26     # how far along the line the cardinality sits
CARD_SIDE = 19     # how far to the side of the line it sits

CARDS = []         # (text, x, y) drawn after the lines


def _unit(a, b):
    """Unit vector pointing from a to b, and its perpendicular."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    return (ux, uy), (-uy, ux)


def _cardinality(end, inward, text):
    """Place a 1 or N beside the line, just clear of the entity it belongs to.

    The offset is forced below a horizontal line and to the right of a vertical
    one, so it never lands on the relationship name, which sits above and left.
    """
    (ux, uy), _perp = _unit(end, inward)
    px, py = (0.0, 1.0) if abs(ux) > abs(uy) else (1.0, 0.0)
    x = end[0] + ux * CARD_BACK + px * CARD_SIDE
    y = end[1] + uy * CARD_BACK + py * CARD_SIDE
    CARDS.append((text, x, y))


def rel(pts, ms, me, label, lx, ly, anchor="middle"):
    pts = list(pts)
    d = "M" + " L".join(f"{round(x)} {round(y)}" for x, y in pts)
    RELATIONS.append((d, ms, me, label, lx, ly, anchor))
    first, second = ("M", "N") if ms == "many" and me == "many" else ("1", "N")
    _cardinality(pts[0], pts[1], first if ms == "many" else "1")
    _cardinality(pts[-1], pts[-2], second if me == "many" else "1")


def hrel(a, b, y, ms, me, label, side="right"):
    """Horizontal relation between two entities side by side, at absolute y."""
    if side == "right":
        p0, p1 = (BOX[a]["x"] + BOX[a]["w"], y), (BOX[b]["x"], y)
    else:
        p0, p1 = (BOX[a]["x"], y), (BOX[b]["x"] + BOX[b]["w"], y)
    rel([p0, p1], ms, me, label, (p0[0] + p1[0]) / 2, y - 13)


# Every relationship below joins neighbouring boxes. The label sits beside the
# middle of the line so it is obvious which pair of entities it belongs to.

# --- identity and tenancy -------------------------------------------------
hrel("USER", "MEMBERSHIP", 170, "one", "many", "holds")
hrel("TENANT", "MEMBERSHIP", 210, "one", "many", "grants", side="left")

# TENANT fans down into the entities it owns, on a shared bus under the box
BUS = 306
rel([B("TENANT", 0.3), (B("TENANT", 0.3)[0], BUS),
     (T("DOMAIN", 0.5)[0], BUS), T("DOMAIN", 0.5)],
    "one", "many", "owns", T("DOMAIN", 0.5)[0] + 16, BUS - 12, "start")
rel([B("TENANT", 0.5), (B("TENANT", 0.5)[0], BUS),
     (T("COLLECTION", 0.5)[0], BUS), T("COLLECTION", 0.5)],
    "one", "many", "owns", T("COLLECTION", 0.5)[0] + 16, BUS - 12, "start")
rel([B("TENANT", 0.7), T("PRODUCT", 0.7)], "one", "many",
    "owns", T("PRODUCT", 0.7)[0] + 46, BUS - 12, "start")

# the fourth owned entity sits a row lower; the drop stays inside the figure
X_CUST = vchan(0)
rel([B("TENANT", 0.12), (B("TENANT", 0.12)[0], BUS - 26), (X_CUST, BUS - 26),
     (X_CUST, 600), (T("CUSTOMER", 0.8)[0], 600), T("CUSTOMER", 0.8)],
    "one", "many", "owns", X_CUST + 14, 560, "start")

# --- catalogue ------------------------------------------------------------
hrel("PRODUCT", "COLLECTION", 470, "many", "many", "grouped in", side="left")
rel([B("PRODUCT", 0.45), T("PRODUCT_VARIANT", 0.45)], "one", "many",
    "sold as", B("PRODUCT", 0.45)[0] + 16, 610, "start")
rel([B("PRODUCT_VARIANT", 0.45), T("INVENTORY_ITEM", 0.45)], "one", "one",
    "stocked as", B("PRODUCT_VARIANT", 0.45)[0] + 16, 900, "start")

rel([B("PRODUCT_VARIANT", 0.2), (B("PRODUCT_VARIANT", 0.2)[0], 892),
     (T("CART_ITEM", 0.8)[0], 892), T("CART_ITEM", 0.8)],
    "one", "many", "chosen in", 1000, 880)

X_SOLD = vchan(1, 34)
rel([L("PRODUCT_VARIANT", 0.8), (X_SOLD, L("PRODUCT_VARIANT", 0.8)[1]),
     (X_SOLD, 1182), (T("ORDER_ITEM", 0.85)[0], 1182), T("ORDER_ITEM", 0.85)],
    "one", "many", "sold in", 990, 1172)

# --- customers, carts and orders ------------------------------------------
hrel("CUSTOMER", "CART", 760, "one", "many", "owns")
rel([B("CUSTOMER", 0.45), T("ADDRESS", 0.45)], "one", "many",
    "saves", B("CUSTOMER", 0.45)[0] + 16, 900, "start")
rel([B("CART", 0.5), T("CART_ITEM", 0.5)], "one", "many",
    "contains", B("CART", 0.5)[0] + 16, 900, "start")

X_PLACES = vchan(0, -30)
rel([R("CUSTOMER", 0.75), (X_PLACES, R("CUSTOMER", 0.75)[1]),
     (X_PLACES, 1186), (T("ORDERS", 0.9)[0], 1186), T("ORDERS", 0.9)],
    "one", "many", "places", X_PLACES + 14, 1000, "start")

rel([B("ADDRESS", 0.4), T("ORDERS", 0.4)], "one", "many",
    "ships to", B("ADDRESS", 0.4)[0] + 16, 1190, "start")
hrel("ORDERS", "ORDER_ITEM", 1330, "one", "many", "contains")

rel([T("SHIPPING_ZONE", 0.4), B("ORDERS", 0.4)], "one", "many",
    "prices", T("SHIPPING_ZONE", 0.4)[0] + 46, 1628, "start")
rel([T("DISCOUNT", 0.35), (T("DISCOUNT", 0.35)[0], 1624),
     (B("ORDERS", 0.75)[0], 1624), B("ORDERS", 0.75)],
    "one", "many", "reduces", 600, 1612)


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
  .rl  {{ font-size: {LABEL_FONT}px;  fill: #6b3a2e; }}
  rect.box {{ fill: #ffffff; stroke: #3b6ea5; stroke-width: 2; }}
  rect.hdr {{ fill: #eef4fb; stroke: #3b6ea5; stroke-width: 2; }}
  line.sep {{ stroke: #cfd9e4; stroke-width: 1; }}
  path.rel {{ stroke: #4a4a4a; stroke-width: 2; fill: none; }}
</style>
<div id="figure">
<svg width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- refX puts the notation itself on the entity border: the bar and the
         three prongs touch the box, and the line runs away from it. -->
    <marker id="one" viewBox="0 0 26 26" refX="24" refY="13"
            markerWidth="26" markerHeight="26" markerUnits="userSpaceOnUse"
            orient="auto-start-reverse">
      <path d="M16 3 L16 23" stroke="#4a4a4a" stroke-width="2.2" fill="none"/>
    </marker>
    <marker id="many" viewBox="0 0 26 26" refX="22" refY="13"
            markerWidth="26" markerHeight="26" markerUnits="userSpaceOnUse"
            orient="auto-start-reverse">
      <path d="M3 13 L22 3 M3 13 L22 13 M3 13 L22 23"
            stroke="#4a4a4a" stroke-width="2" fill="none"
            stroke-linecap="round"/>
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
        o.append(f'  <path class="rel" d="{d}"/>')
        o.append(f'  <text class="rl" x="{round(lx)}" y="{round(ly)}" '
                 f'text-anchor="{anchor}">{esc(label)}</text>')

    for text, x, y in CARDS:
        o.append(f'  <text class="cd" x="{round(x)}" y="{round(y)}">{esc(text)}</text>')

    o.append('</svg>\n</div>\n')
    return "\n".join(o)


if __name__ == "__main__":
    target = Path(__file__).with_name("fig7_erd.html")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
