"""Tiny SVG builder for question figures.

All helpers return SVG *strings*. Compose shapes with ``canvas``::

    from backend.bank import svg
    fig = svg.canvas(220, 160, [
        svg.polygon([(20, 140), (200, 140), (20, 20)], shade=True),
        svg.right_angle((20, 140), (200, 140), (20, 20)),
        svg.label((110, 155), "12 ซม."),
    ])

Colours come from CSS classes defined by the front end (``fig-*``), so the
figures follow the app theme and stay readable. Keep figures simple and
label every length/angle the question needs. Do NOT draw to scale when the
picture would give the answer away — say "รูปไม่ได้วาดตามสัดส่วน" in the stem.

Chart helpers (``bar_chart``, ``pie_chart``, ``line_chart``, ``pictogram``)
return complete SVG documents, ready to use as ``figure=``.
"""

import math
from html import escape

PALETTE = ["#E91E8C", "#3F7DE8", "#F5A524", "#22A06B", "#8E5CD9", "#E5484D", "#13A8A8", "#7A7076"]


def _f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def canvas(w, h, parts, pad=0):
    """Wrap parts in an <svg>. ``parts`` is a list of SVG element strings."""
    body = "".join(p for p in parts if p)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" '
        f'width="{w + 2 * pad}" height="{h + 2 * pad}" class="fig" role="img">{body}</svg>'
    )


def line(p, q, dashed=False, cls="fig-line"):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<line x1="{_f(p[0])}" y1="{_f(p[1])}" x2="{_f(q[0])}" y2="{_f(q[1])}" class="{cls}"{dash}/>'


def polyline(points, cls="fig-line"):
    pts = " ".join(f"{_f(x)},{_f(y)}" for x, y in points)
    return f'<polyline points="{pts}" class="{cls}" fill="none"/>'


def polygon(points, shade=False, cls=None, dashed=False):
    """Closed shape. shade=True fills with the highlight colour."""
    pts = " ".join(f"{_f(x)},{_f(y)}" for x, y in points)
    klass = cls or ("fig-shade" if shade else "fig-shape")
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<polygon points="{pts}" class="{klass}"{dash}/>'


def rect(x, y, w, h, shade=False, cls=None):
    klass = cls or ("fig-shade" if shade else "fig-shape")
    return f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" class="{klass}"/>'


def circle(c, r, shade=False, cls=None):
    klass = cls or ("fig-shade" if shade else "fig-shape")
    return f'<circle cx="{_f(c[0])}" cy="{_f(c[1])}" r="{_f(r)}" class="{klass}"/>'


def sector(c, r, a0, a1, shade=True, cls=None):
    """Pie slice from angle a0 to a1 (degrees, 0 = right, counter-clockwise)."""
    klass = cls or ("fig-shade" if shade else "fig-shape")
    x0 = c[0] + r * math.cos(math.radians(a0))
    y0 = c[1] - r * math.sin(math.radians(a0))
    x1 = c[0] + r * math.cos(math.radians(a1))
    y1 = c[1] - r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (
        f'<path d="M{_f(c[0])},{_f(c[1])} L{_f(x0)},{_f(y0)} A{_f(r)},{_f(r)} 0 {large} 0 {_f(x1)},{_f(y1)} Z" '
        f'class="{klass}"/>'
    )


def dot(p, r=3):
    return f'<circle cx="{_f(p[0])}" cy="{_f(p[1])}" r="{r}" class="fig-dot"/>'


def label(p, text, size=13, anchor="middle", cls="fig-text", bold=False):
    """Text centred at p (baseline adjusted so it looks centred)."""
    weight = ' font-weight="700"' if bold else ""
    return (
        f'<text x="{_f(p[0])}" y="{_f(p[1] + size * 0.35)}" font-size="{size}" text-anchor="{anchor}" '
        f'class="{cls}"{weight}>{escape(str(text))}</text>'
    )


def point_label(p, text, dx=0, dy=0, size=14):
    """Vertex name such as A, B, C placed slightly off the point."""
    return label((p[0] + dx, p[1] + dy), text, size=size, cls="fig-vertex", bold=True)


def dim(p, q, text, offset=14, size=12):
    """Length label for segment pq, pushed ``offset`` px to the left of p→q."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    nx, ny = dy / n, -dx / n
    return label((mx + nx * offset, my + ny * offset), text, size=size, cls="fig-dim")


def right_angle(corner, a, b, size=10):
    """Small square at ``corner`` between rays to a and b."""
    def unit(p):
        dx, dy = p[0] - corner[0], p[1] - corner[1]
        n = math.hypot(dx, dy) or 1
        return dx / n, dy / n

    ux, uy = unit(a)
    vx, vy = unit(b)
    p1 = (corner[0] + ux * size, corner[1] + uy * size)
    p2 = (p1[0] + vx * size, p1[1] + vy * size)
    p3 = (corner[0] + vx * size, corner[1] + vy * size)
    return polyline([p1, p2, p3], cls="fig-mark")


def angle_arc(corner, a, b, text=None, r=22, size=12):
    """Arc marking the angle at ``corner`` from ray→a to ray→b, with optional label."""
    a0 = math.degrees(math.atan2(-(a[1] - corner[1]), a[0] - corner[0]))
    a1 = math.degrees(math.atan2(-(b[1] - corner[1]), b[0] - corner[0]))
    sweep = (a1 - a0) % 360
    if sweep > 180:
        a0, a1 = a1, a0
        sweep = 360 - sweep
    x0 = corner[0] + r * math.cos(math.radians(a0))
    y0 = corner[1] - r * math.sin(math.radians(a0))
    x1 = corner[0] + r * math.cos(math.radians(a0 + sweep))
    y1 = corner[1] - r * math.sin(math.radians(a0 + sweep))
    parts = [f'<path d="M{_f(x0)},{_f(y0)} A{r},{r} 0 0 0 {_f(x1)},{_f(y1)}" class="fig-mark" fill="none"/>']
    if text:
        mid = math.radians(a0 + sweep / 2)
        lr = r + 13
        parts.append(label((corner[0] + lr * math.cos(mid), corner[1] - lr * math.sin(mid)), text, size=size,
                           cls="fig-dim"))
    return "".join(parts)


def tick(p, q, count=1):
    """Equal-length tick marks on segment pq."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux
    out = []
    for i in range(count):
        off = (i - (count - 1) / 2) * 4
        cx, cy = mx + ux * off, my + uy * off
        out.append(line((cx - nx * 5, cy - ny * 5), (cx + nx * 5, cy + ny * 5), cls="fig-mark"))
    return "".join(out)


def grid(x, y, cols, rows, cell, shaded=(), cls="fig-grid"):
    """Square grid. ``shaded`` is a set of (col, row) cells to fill."""
    parts = []
    shaded = set(shaded)
    for r in range(rows):
        for c in range(cols):
            parts.append(rect(x + c * cell, y + r * cell, cell, cell,
                              cls="fig-shade" if (c, r) in shaded else cls))
    return "".join(parts)


def box3d(x, y, w, h, d, labels=None):
    """Simple oblique cuboid. Front face at (x, y) size w×h, depth d drawn up-right.

    labels = {"w": "8 ซม.", "h": "5 ซม.", "d": "4 ซม."}
    """
    dx, dy = d * 0.6, -d * 0.45
    f = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    top = [(x, y), (x + dx, y + dy), (x + w + dx, y + dy), (x + w, y)]
    side = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)]
    parts = [polygon(top, cls="fig-face2"), polygon(side, cls="fig-face3"), polygon(f, cls="fig-shape"),
             line((x + dx, y + h + dy), (x, y + h), dashed=True),
             line((x + dx, y + h + dy), (x + w + dx, y + h + dy), dashed=True),
             line((x + dx, y + h + dy), (x + dx, y + dy), dashed=True)]
    labels = labels or {}
    if "w" in labels:
        parts.append(label((x + w / 2, y + h + 14), labels["w"], size=12, cls="fig-dim"))
    if "h" in labels:
        parts.append(label((x - 8, y + h / 2), labels["h"], size=12, anchor="end", cls="fig-dim"))
    if "d" in labels:
        parts.append(label((x + w + dx / 2 + 10, y + h + dy / 2 + 6), labels["d"], size=12, anchor="start",
                           cls="fig-dim"))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Complete figures
# ---------------------------------------------------------------------------

def bar_chart(labels, values, title="", unit="", width=360, height=220, horizontal=False, max_value=None,
              show_values=False, step=None):
    """Vertical bar chart with gridlines. Values must be non-negative numbers."""
    n = len(labels)
    top = max_value or max(values)
    if step is None:
        step = _nice_step(top)
    top = math.ceil(top / step) * step
    left, right, t, b = 44, 12, 28 if title else 12, 34
    pw, ph = width - left - right, height - t - b
    parts = []
    if title:
        parts.append(label((width / 2, 12), title, size=13, bold=True))
    v = 0
    while v <= top + 1e-9:
        y = t + ph - ph * v / top
        parts.append(line((left, y), (left + pw, y), cls="fig-gridline"))
        parts.append(label((left - 6, y), _short(v), size=11, anchor="end", cls="fig-axis"))
        v += step
    bw = pw / n * 0.6
    for i, (lab, val) in enumerate(zip(labels, values)):
        cx = left + pw * (i + 0.5) / n
        bh = ph * val / top
        parts.append(f'<rect x="{_f(cx - bw / 2)}" y="{_f(t + ph - bh)}" width="{_f(bw)}" height="{_f(bh)}" '
                     f'fill="{PALETTE[i % len(PALETTE)]}" class="fig-bar"/>')
        parts.append(label((cx, t + ph + 14), lab, size=11, cls="fig-axis"))
        if show_values:
            parts.append(label((cx, t + ph - bh - 8), _short(val), size=11, cls="fig-text"))
    parts.append(line((left, t), (left, t + ph), cls="fig-axisline"))
    parts.append(line((left, t + ph), (left + pw, t + ph), cls="fig-axisline"))
    if unit:
        parts.append(label((6, t - 6 if title else 6), unit, size=10, anchor="start", cls="fig-axis"))
    return canvas(width, height, parts)


def pie_chart(labels, percents, title="", width=340, height=210, show_percent=True):
    """Pie chart with a legend. percents should add to 100."""
    cx, cy, r = 105, 110 if title else 100, 80
    parts = []
    if title:
        parts.append(label((width / 2, 12), title, size=13, bold=True))
    a = 90.0
    for i, (lab, p) in enumerate(zip(labels, percents)):
        sweep = 360 * p / 100
        color = PALETTE[i % len(PALETTE)]
        if sweep >= 359.9:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" class="fig-slice"/>')
        else:
            x0 = cx + r * math.cos(math.radians(a))
            y0 = cy - r * math.sin(math.radians(a))
            x1 = cx + r * math.cos(math.radians(a - sweep))
            y1 = cy - r * math.sin(math.radians(a - sweep))
            large = 1 if sweep > 180 else 0
            parts.append(f'<path d="M{cx},{cy} L{_f(x0)},{_f(y0)} A{r},{r} 0 {large} 1 {_f(x1)},{_f(y1)} Z" '
                         f'fill="{color}" class="fig-slice"/>')
        if show_percent and p >= 6:
            mid = math.radians(a - sweep / 2)
            parts.append(label((cx + r * 0.62 * math.cos(mid), cy - r * 0.62 * math.sin(mid)), f"{_short(p)}%",
                               size=11, cls="fig-onfill", bold=True))
        ly = 40 + i * 22
        parts.append(f'<rect x="210" y="{ly - 7}" width="14" height="14" rx="3" fill="{color}"/>')
        parts.append(label((230, ly), lab, size=12, anchor="start"))
        a -= sweep
    return canvas(width, height, parts)


def line_chart(labels, values, title="", unit="", width=360, height=220, step=None, min_value=0):
    left, right, t, b = 44, 16, 28 if title else 12, 34
    pw, ph = width - left - right, height - t - b
    top = max(values)
    if step is None:
        step = _nice_step(top - min_value)
    top = math.ceil(top / step) * step
    span = (top - min_value) or 1
    parts = []
    if title:
        parts.append(label((width / 2, 12), title, size=13, bold=True))
    v = min_value
    while v <= top + 1e-9:
        y = t + ph - ph * (v - min_value) / span
        parts.append(line((left, y), (left + pw, y), cls="fig-gridline"))
        parts.append(label((left - 6, y), _short(v), size=11, anchor="end", cls="fig-axis"))
        v += step
    pts = []
    n = len(labels)
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = left + pw * (i + 0.5) / n
        y = t + ph - ph * (val - min_value) / span
        pts.append((x, y))
        parts.append(label((x, t + ph + 14), lab, size=11, cls="fig-axis"))
    parts.append(polyline(pts, cls="fig-series"))
    for p in pts:
        parts.append(dot(p, 4))
    parts.append(line((left, t), (left, t + ph), cls="fig-axisline"))
    parts.append(line((left, t + ph), (left + pw, t + ph), cls="fig-axisline"))
    if unit:
        parts.append(label((6, 6), unit, size=10, anchor="start", cls="fig-axis"))
    return canvas(width, height, parts)


def pictogram(labels, counts, symbol="●", per="", width=360):
    """Rows of symbols. counts may contain .5 for a half symbol (drawn faded)."""
    row_h = 30
    height = 20 + row_h * len(labels) + (22 if per else 0)
    parts = []
    for i, (lab, c) in enumerate(zip(labels, counts)):
        y = 24 + i * row_h
        parts.append(label((8, y), lab, size=12, anchor="start"))
        full = int(c)
        for k in range(full):
            parts.append(label((100 + k * 22, y), symbol, size=18, cls="fig-symbol"))
        if c - full >= 0.5:
            parts.append(label((100 + full * 22, y), symbol, size=18, cls="fig-symbol-half"))
    if per:
        parts.append(label((8, height - 10), per, size=11, anchor="start", cls="fig-axis"))
    return canvas(width, height, parts)


def number_line(lo, hi, marks=(), labels_at=None, width=360, highlight=None):
    """Integer number line from lo to hi. marks = {value: 'A'} letter labels above points.

    highlight = (a, b) draws a thick segment between a and b.
    """
    left, right, y = 20, 20, 40
    pw = width - left - right
    span = hi - lo
    parts = [line((left - 8, y), (left + pw + 8, y), cls="fig-axisline")]
    labels_at = labels_at if labels_at is not None else list(range(lo, hi + 1))

    def X(v):
        return left + pw * (v - lo) / span

    for v in range(lo, hi + 1):
        parts.append(line((X(v), y - 5), (X(v), y + 5), cls="fig-axisline"))
        if v in labels_at:
            parts.append(label((X(v), y + 18), str(v), size=11, cls="fig-axis"))
    if highlight:
        parts.append(line((X(highlight[0]), y), (X(highlight[1]), y), cls="fig-highlight"))
    marks = dict(marks) if not isinstance(marks, dict) else marks
    for v, name in marks.items():
        parts.append(dot((X(v), y), 5))
        parts.append(label((X(v), y - 16), name, size=13, cls="fig-vertex", bold=True))
    return canvas(width, 70, parts)


def fraction_bar(parts_count, shaded, width=300, height=34, label_text=None):
    """One bar split into equal parts with the first ``shaded`` parts filled."""
    pw = width / parts_count
    out = []
    for i in range(parts_count):
        out.append(rect(i * pw + 1, 1, pw, height - 2, shade=i < shaded))
    if label_text:
        out.append(label((width + 8, height / 2), label_text, size=12, anchor="start"))
    return canvas(width + (60 if label_text else 2), height, out)


def clock(hour, minute, size=150):
    """Analogue clock face showing hour:minute."""
    c = size / 2
    r = size / 2 - 6
    parts = [circle((c, c), r, cls="fig-shape")]
    for h in range(1, 13):
        a = math.radians(90 - h * 30)
        parts.append(label((c + (r - 14) * math.cos(a), c - (r - 14) * math.sin(a)), str(h), size=12))
    for m in range(60):
        a = math.radians(90 - m * 6)
        inner = r - (6 if m % 5 == 0 else 3)
        parts.append(line((c + inner * math.cos(a), c - inner * math.sin(a)),
                          (c + r * math.cos(a), c - r * math.sin(a)), cls="fig-mark"))
    ha = math.radians(90 - (hour % 12 + minute / 60) * 30)
    ma = math.radians(90 - minute * 6)
    parts.append(f'<line x1="{c}" y1="{c}" x2="{_f(c + r * 0.5 * math.cos(ha))}" y2="{_f(c - r * 0.5 * math.sin(ha))}" '
                 f'class="fig-hand-h"/>')
    parts.append(f'<line x1="{c}" y1="{c}" x2="{_f(c + r * 0.78 * math.cos(ma))}" y2="{_f(c - r * 0.78 * math.sin(ma))}" '
                 f'class="fig-hand-m"/>')
    parts.append(dot((c, c), 4))
    return canvas(size, size, parts)


def _nice_step(span):
    if span <= 0:
        return 1
    raw = span / 5
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def _short(v):
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v)):,}"
    return f"{v:,.1f}"
