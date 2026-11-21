# -*- coding: utf-8 -*-
"""
Gemeinsame Bilder für Mathe Klasse 2 (Deutschland): Hunderterfeld, Punktefelder, Gruppen, Zehnerstangen.
Die Bilder aus k_pics bekommen deutsche aria-labels.
"""
import re
from k_pics import obj, CELL, M
from ws_common import svg_wrap, fig, line, text, INK, GREEN, FILL, BLUE

DING = {"apple": ("Apfel", "Äpfel"), "star": ("Stern", "Sterne"), "ball": ("Ball", "Bälle"), "button": ("Knopf", "Knöpfe"),
        "fish": ("Fisch", "Fische"), "flower": ("Blume", "Blumen"), "heart": ("Herz", "Herzen"), "duck": ("Ente", "Enten"),
        "cup": ("Becher", "Becher"), "bug": ("Käfer", "Käfer")}
KINDS = list(DING)


def ding(kind, n):
    return "%d %s" % (n, DING[kind][0] if n == 1 else DING[kind][1])


def de(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def hunderterfeld(n, label=None):
    """10 × 10 Punkte, die ersten n ausgefüllt (zeilenweise), Fünferlücke"""
    c = 18
    s = []
    for i in range(100):
        r, k = divmod(i, 10)
        x = 12 + k * c + (6 if k >= 5 else 0)
        y = 12 + r * c + (6 if r >= 5 else 0)
        s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s' stroke='%s' stroke-width='1'/>" % (x, y, BLUE if i < n else "#ffffff", INK))
    return fig(svg_wrap(10 * c + 18, 10 * c + 18, "".join(s), label or "Hunderterfeld mit %d Punkten" % n))


def punktfeld(rows, cols, label=None):
    c = 22
    s = ["<circle cx='%d' cy='%d' r='7.5' fill='%s' stroke='%s' stroke-width='1'/>" % (14 + k * c, 14 + r * c, BLUE, INK)
         for r in range(rows) for k in range(cols)]
    return fig(svg_wrap(cols * c + 8, rows * c + 8, "".join(s), label or "Punktefeld: %d Reihen mit je %d Punkten" % (rows, cols)))


def gruppen(g, k, kind, label=None):
    """g Gruppen mit je k Dingen, jede Gruppe in einem Kreis/Rahmen"""
    per = min(k, 5)
    rows = (k + 4) // 5
    bw, bh = per * 26 + 12, rows * 26 + 12
    s = []
    for j in range(g):
        x0 = 6 + j * (bw + 10)
        s.append("<rect x='%d' y='6' width='%d' height='%d' rx='12' fill='none' stroke='%s' stroke-width='1.6'/>" % (x0, bw, bh, GREEN))
        for i in range(k):
            s.append(obj(kind, x0 + 6 + 13 + (i % 5) * 26, 6 + 6 + 13 + (i // 5) * 26, 11))
    return fig(svg_wrap(g * (bw + 10) + 4, bh + 12, "".join(s), label or "%d Gruppen, in jeder Gruppe %s" % (g, ding(kind, k))))


def reihe(n, kind, per_row=10, label=None):
    rows = [per_row] * (n // per_row) + ([n % per_row] if n % per_row else [])
    gap = 14 if per_row > 5 else 0
    W = 2 * M + min(n, per_row) * CELL + (gap if min(n, per_row) > 5 else 0)
    H = 2 * M + len(rows) * CELL
    s = []
    for r, c in enumerate(rows):
        for i in range(c):
            s.append(obj(kind, M + CELL / 2 + i * CELL + (gap if i >= 5 else 0), M + CELL / 2 + r * CELL))
    return fig(svg_wrap(W, H, "".join(s), label or ding(kind, n)))


def zahlenstrahl100(lo, hi, marks, step=1, every=10, width=440):
    """Zahlenstrahl mit Pfeilen: marks = [(Wert, Buchstabe)]"""
    n = (hi - lo) // step
    u = width / float(n)
    x0, y = 20, 52
    s = [line(x0 - 6, y, x0 + width + 10, y, INK, 2)]
    for i in range(n + 1):
        v = lo + i * step
        big = v % every == 0
        s.append(line(x0 + i * u, y - (9 if big else 5), x0 + i * u, y + (9 if big else 5), INK, 1.6 if big else 1))
        if big:
            s.append(text(x0 + i * u, y + 26, str(v), 13, weight=600))
    for v, ch in marks:
        x = x0 + (v - lo) / float(step) * u
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (x - 6, y - 26, x + 6, y - 26, x, y - 12, GREEN))
        s.append(text(x, y - 30, ch, 15, col=GREEN))
    return fig(svg_wrap(int(width + 40), 86, "".join(s), "Zahlenstrahl von %d bis %d" % (lo, hi)).replace("<svg ", "<svg data-pf='lg' ", 1))
