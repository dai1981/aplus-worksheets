# -*- coding: utf-8 -*-
"""
Pictures for UK science units: circuit diagrams with the standard symbols used in English schools
(cell, battery, lamp, switch, buzzer, motor), rock layers with fossils, and a simple dichotomous key.
All SVG attributes in single quotes, viewBox always set (svg_wrap).
"""
from sci_common import svg_wrap, text, line, rect, circle, INK, GREEN, BLUE, RED, GRAY, FILL, BROWN, SKY

W_COMP = 44   # space one component takes on a wire


def _cell(cx, cy, s):
    # long thin line (+) and short thick line (-)
    s.append(line(cx - 6, cy - 16, cx - 6, cy + 16, INK, 2.5))
    s.append(line(cx + 6, cy - 8, cx + 6, cy + 8, INK, 6))
    s.append(line(cx - 22, cy, cx - 6, cy, INK, 2))
    s.append(line(cx + 6, cy, cx + 22, cy, INK, 2))


def _battery(cx, cy, s):
    for dx in (-9, 9):
        s.append(line(cx + dx - 5, cy - 16, cx + dx - 5, cy + 16, INK, 2.5))
        s.append(line(cx + dx + 4, cy - 8, cx + dx + 4, cy + 8, INK, 6))
    s.append(line(cx - 4, cy, cx + 4, cy, INK, 2, " stroke-dasharray='2 2'"))
    s.append(line(cx - 22, cy, cx - 14, cy, INK, 2))
    s.append(line(cx + 13, cy, cx + 22, cy, INK, 2))


def _lamp(cx, cy, s, on=None):
    if on:
        s.append(circle(cx, cy, 15, "#fff3b0", "none", 0))
    s.append(circle(cx, cy, 11, "#ffffff", INK, 2))
    s.append(line(cx - 7.8, cy - 7.8, cx + 7.8, cy + 7.8, INK, 2))
    s.append(line(cx - 7.8, cy + 7.8, cx + 7.8, cy - 7.8, INK, 2))
    s.append(line(cx - 22, cy, cx - 11, cy, INK, 2))
    s.append(line(cx + 11, cy, cx + 22, cy, INK, 2))


def _switch(cx, cy, s, closed):
    s.append(line(cx - 22, cy, cx - 12, cy, INK, 2))
    s.append(line(cx + 12, cy, cx + 22, cy, INK, 2))
    s.append(circle(cx - 12, cy, 2.5, INK, INK, 1))
    s.append(circle(cx + 12, cy, 2.5, INK, INK, 1))
    if closed:
        s.append(line(cx - 12, cy, cx + 12, cy, INK, 2))
    else:
        s.append(line(cx - 12, cy, cx + 10, cy - 12, INK, 2))


def _buzzer(cx, cy, s):
    s.append("<path d='M%.1f %.1f A12 12 0 0 1 %.1f %.1f Z' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (cx - 12, cy, cx + 12, cy, INK))
    s.append(line(cx - 22, cy, cx - 12, cy, INK, 2))
    s.append(line(cx + 12, cy, cx + 22, cy, INK, 2))


def _motor(cx, cy, s):
    s.append(circle(cx, cy, 12, "#ffffff", INK, 2))
    s.append(text(cx, cy + 5, "M", 14))
    s.append(line(cx - 22, cy, cx - 12, cy, INK, 2))
    s.append(line(cx + 12, cy, cx + 22, cy, INK, 2))


def _gap(cx, cy, s):
    s.append(line(cx - 22, cy, cx - 8, cy, INK, 2))
    s.append(line(cx + 8, cy, cx + 22, cy, INK, 2))


def comp(name, cx, cy, s, on=None):
    if name == "cell":
        _cell(cx, cy, s)
    elif name == "battery":
        _battery(cx, cy, s)
    elif name == "lamp":
        _lamp(cx, cy, s, on)
    elif name == "switch_open":
        _switch(cx, cy, s, False)
    elif name == "switch_closed":
        _switch(cx, cy, s, True)
    elif name == "buzzer":
        _buzzer(cx, cy, s)
    elif name == "motor":
        _motor(cx, cy, s)
    elif name == "gap":
        _gap(cx, cy, s)
    elif name == "wire":
        s.append(line(cx - 22, cy, cx + 22, cy, INK, 2))
    else:
        raise ValueError(name)


def symbol(name, label=None):
    """One symbol on its own, for 'what is this symbol?' questions."""
    s = []
    comp(name, 60, 30, s)
    return svg_wrap(120, 60, "".join(s), label or "circuit symbol")


def circuit(top, bottom=(), label="circuit diagram", on=None):
    """A series loop: components on the top wire (left to right) and on the bottom wire."""
    n = max(len(top), len(bottom), 2)
    W = 60 + n * (W_COMP + 26)
    H = 140
    x0, x1, yt, yb = 30, W - 30, 34, H - 26
    s = [line(x0, yt, x0, yb), line(x1, yt, x1, yb)]
    for row, y in ((list(top), yt), (list(bottom), yb)):
        if not row:
            s.append(line(x0, y, x1, y))
            continue
        step = (x1 - x0) / float(len(row) + 1)
        xs = [x0 + step * (k + 1) for k in range(len(row))]
        edges = [x0] + [v for x in xs for v in (x - 22, x + 22)] + [x1]
        for k in range(0, len(edges), 2):
            s.append(line(edges[k], y, edges[k + 1], y))
        for name, x in zip(row, xs):
            comp(name, x, y, s, on)
    return svg_wrap(int(W), H, "".join(s), label)


def parallel(branches, cells=1, label="parallel circuit"):
    """Cells on the left side; each branch is a list of components drawn across the circuit."""
    n = len(branches)
    m = max(len(b) for b in branches)
    W = 120 + m * 70
    H = 40 + n * 56
    x0, x1 = 40, W - 30
    ys = [30 + k * 56 for k in range(n)]
    s = [line(x0, ys[0], x0, ys[-1]), line(x1, ys[0], x1, ys[-1])]
    for b, y in zip(branches, ys):
        step = (x1 - x0) / float(len(b) + 1)
        xs = [x0 + step * (k + 1) for k in range(len(b))]
        edges = [x0] + [v for x in xs for v in (x - 22, x + 22)] + [x1]
        for k in range(0, len(edges), 2):
            s.append(line(edges[k], y, edges[k + 1], y))
        for name, x in zip(b, xs):
            comp(name, x, y, s)
    return svg_wrap(int(W), int(H), "".join(s), label)


# ------------------------------------------------------------ rock layers
def layers(rows, label="rock layers with fossils"):
    """rows: list of (layer name or '', fossil label or '') from TOP to BOTTOM."""
    cols = ["#f3e2b8", "#e2c58f", "#d1a96b", "#b98b55", "#9c7246", "#7f5c3a"]
    W, h = 340, 40
    H = 20 + h * len(rows)
    s = []
    for k, (nm, fos) in enumerate(rows):
        y = 10 + k * h
        s.append(rect(20, y, 200, h, cols[k % len(cols)], INK, 1.5))
        if nm:
            s.append(text(120, y + 25, nm, 14))
        if fos:
            s.append(text(232, y + 25, fos, 14, "start"))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ light
def _eye(x, y, s):
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' fill='#ffffff' stroke='%s' stroke-width='2'/>"
             % (x - 22, y, x, y - 18, x + 22, y, x, y + 18, x - 22, y, INK))
    s.append(circle(x, y, 8, "#5b8fd6", INK, 1.5))
    s.append(circle(x, y, 3.5, INK, INK, 1))


def _lamp_src(x, y, s, label):
    s.append(circle(x, y, 16, "#ffe680", "#c98f00", 2))
    for k in range(8):
        import math
        a = k * math.pi / 4
        s.append(line(x + 20 * math.cos(a), y + 20 * math.sin(a), x + 27 * math.cos(a), y + 27 * math.sin(a), "#c98f00", 2))
    s.append(text(x, y + 46, label, 13))


def _obj(x, y, s, label):
    s.append(rect(x - 22, y - 18, 44, 36, "#cfe3c4", INK, 2, 4))
    s.append(text(x, y + 38, label, 13))


def _ray(a, b, s, col="#d9822b"):
    from sci_common import arrow
    import math
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    s.append(arrow(x1 + ux * 30, y1 + uy * 30, x2 - ux * 30, y2 - uy * 30, col, 2.5))


def seeing(src, obj, rays, label="diagram of light rays"):
    """src/obj: labels; rays: list of ('S','O'), ('O','E'), ('E','O'), ('S','E'), ('E','S') pairs."""
    P = {"S": (60, 50), "O": (250, 50), "E": (150, 150)}
    s = []
    _lamp_src(60, 50, s, src)
    _obj(250, 50, s, obj)
    _eye(150, 150, s)
    s.append(text(150, 186, "eye", 13))
    for a, b in rays:
        _ray(P[a], P[b], s)
    return svg_wrap(320, 196, "".join(s), label)


def shadow_setup(d_label="", label="torch, object and screen"):
    s = []
    _lamp_src(40, 60, s, "torch")
    s.append(rect(150, 40, 14, 40, "#8a5a2b", INK, 1.5))
    s.append(text(157, 110, "object", 13))
    s.append(rect(300, 10, 10, 100, "#e8e8e8", INK, 1.5))
    s.append(text(305, 128, "screen", 13))
    s.append("<polygon points='300,22 300,98 164,80 164,40' fill='#555555' opacity='0.25'/>")
    if d_label:
        s.append(line(40, 140, 157, 140, INK, 1.5))
        s.append(text(98, 155, d_label, 13))
    return svg_wrap(330, 162, "".join(s), label)


# ------------------------------------------------------------ Year 3: plants and magnets
PLANT_PART_Y = {"flower": 38, "leaf": 92, "stem": 122, "roots": 178}


def plant(labels, label="a flowering plant with labelled parts"):
    """labels: dict part -> letter, parts from flower, leaf, stem, roots. A plant with leader lines to the right."""
    s = []
    s.append(rect(0, 150, 300, 70, "#e7d3b0", "none", 0))
    s.append(line(0, 150, 300, 150, BROWN, 2))
    for dx, dy in ((-34, 40), (-16, 56), (0, 62), (18, 52), (36, 36)):
        s.append(line(110, 152, 110 + dx, 152 + dy, BROWN, 2.5))
    s.append(line(110, 150, 110, 52, GREEN, 5))
    s.append("<ellipse cx='84' cy='98' rx='26' ry='11' fill='#7bc47f' stroke='%s' stroke-width='1.6' transform='rotate(-25 84 98)'/>" % INK)
    s.append("<ellipse cx='136' cy='86' rx='26' ry='11' fill='#7bc47f' stroke='%s' stroke-width='1.6' transform='rotate(25 136 86)'/>" % INK)
    for ang in range(0, 360, 60):
        import math
        x = 110 + 17 * math.cos(math.radians(ang))
        y = 38 + 17 * math.sin(math.radians(ang))
        s.append(circle(x, y, 11, "#f28cb1", INK, 1.4))
    s.append(circle(110, 38, 9, "#f2c94c", INK, 1.4))
    tip = {"flower": (130, 38), "leaf": (158, 82), "stem": (113, 122), "roots": (140, 180)}
    for part, letter in labels.items():
        x0, y0 = tip[part]
        y = PLANT_PART_Y[part]
        s.append(line(x0, y0, 232, y, INK, 1.4))
        s.append(circle(246, y, 13, "#ffffff", INK, 1.6))
        s.append(text(246, y + 5, letter, 15))
    return svg_wrap(300, 220, "".join(s), label)


def _bar(x, y, left, right, s, w=110, h=34):
    cols = {"N": "#e05b4f", "S": "#5b8fd6"}
    s.append(rect(x, y, w / 2, h, cols[left], INK, 1.6))
    s.append(rect(x + w / 2, y, w / 2, h, cols[right], INK, 1.6))
    s.append(text(x + w / 4, y + h / 2 + 6, left, 17, col="#ffffff"))
    s.append(text(x + 3 * w / 4, y + h / 2 + 6, right, 17, col="#ffffff"))


def magnets(a, b, label="two bar magnets"):
    """a, b: (left pole, right pole) of the left and right bar magnet, e.g. ('N', 'S'), ('N', 'S')."""
    s = []
    _bar(10, 20, a[0], a[1], s)
    _bar(170, 20, b[0], b[1], s)
    return svg_wrap(290, 74, "".join(s), label)


# ------------------------------------------------------------ Year 1: the human body
BODY_PT = {"head": (154, 34), "neck": (136, 72), "shoulder": (158, 86), "arm": (172, 112), "elbow": (178, 132), "hand": (192, 178),
           "tummy": (146, 126), "hip": (152, 158), "leg": (144, 192), "knee": (142, 224), "foot": (166, 290)}


def body(labels, label="a child's body with labelled parts"):
    """labels: dict part -> letter (parts from BODY_PT). Leader lines go from the right side of the body to circles on the right."""
    skin, shirt, trous = "#f2c9a0", "#7fb3e0", "#4a6fa5"
    s = []
    s.append(circle(130, 40, 26, skin, INK, 1.8))
    s.append(rect(124, 64, 12, 14, skin, INK, 1.4))
    s.append("<path d='M100 82 L160 82 L164 160 L96 160 Z' fill='%s' stroke='%s' stroke-width='1.8'/>" % (shirt, INK))
    s.append("<path d='M100 84 L82 132 L74 172' fill='none' stroke='%s' stroke-width='12' stroke-linecap='round'/>" % skin)
    s.append("<path d='M160 84 L178 132 L186 172' fill='none' stroke='%s' stroke-width='12' stroke-linecap='round'/>" % skin)
    s.append(circle(74, 178, 8, skin, INK, 1.4))
    s.append(circle(186, 178, 8, skin, INK, 1.4))
    s.append("<path d='M114 160 L118 224 L114 280' fill='none' stroke='%s' stroke-width='16' stroke-linecap='round'/>" % trous)
    s.append("<path d='M146 160 L142 224 L146 280' fill='none' stroke='%s' stroke-width='16' stroke-linecap='round'/>" % trous)
    s.append("<ellipse cx='108' cy='290' rx='16' ry='7' fill='#555' stroke='%s' stroke-width='1.4'/>" % INK)
    s.append("<ellipse cx='152' cy='290' rx='16' ry='7' fill='#555' stroke='%s' stroke-width='1.4'/>" % INK)
    s.append(circle(121, 36, 2.5, INK, INK, 1))
    s.append(circle(139, 36, 2.5, INK, INK, 1))
    s.append("<path d='M120 50 Q130 57 140 50' fill='none' stroke='%s' stroke-width='1.8'/>" % INK)
    items = sorted(labels.items(), key=lambda kv: BODY_PT[kv[0]][1])
    ys = []
    for part, _ in items:
        y = max(BODY_PT[part][1], (ys[-1] + 30) if ys else 16)
        ys.append(y)
    if ys and ys[-1] > 290:
        shift = ys[-1] - 290
        ys = [max(16 + 30 * i, y - shift) for i, y in enumerate(ys)]
    for (part, letter), y in zip(items, ys):
        x0, y0 = BODY_PT[part]
        s.append(circle(x0, y0, 2.5, INK, INK, 1))
        s.append(line(x0, y0, 252, y, INK, 1.3))
        s.append(circle(266, y, 13, "#ffffff", INK, 1.6))
        s.append(text(266, y + 5, letter, 15))
    return svg_wrap(290, 304, "".join(s), label)
