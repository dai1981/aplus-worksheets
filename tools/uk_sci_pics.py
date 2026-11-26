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
