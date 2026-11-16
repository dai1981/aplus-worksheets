# -*- coding: utf-8 -*-
"""國中九年級の図の部品"""
import math
from tw_common import fig, svg_wrap, text, line, INK, RED, BLUE


def ov(s):
    return "<span class='ov'>%s</span>" % s


def poly_svg(pts, names, seg=None, extra="", label="圖形", pad=26, scale=1.0, lg=False):
    """pts: {名前: (x, y)}（数学座標、上が＋）、names: 頂點を順に結ぶ list のリスト、seg: {('A','B'): 文字}"""
    xs = [p[0] for p in pts.values()]
    ys = [p[1] for p in pts.values()]
    mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
    W = (mxx - mnx) * scale + 2 * pad
    H = (mxy - mny) * scale + 2 * pad

    def P(k):
        x, y = pts[k]
        return ((x - mnx) * scale + pad, (mxy - y) * scale + pad)
    cx = sum(P(k)[0] for k in pts) / len(pts)
    cy = sum(P(k)[1] for k in pts) / len(pts)
    s = []
    for chain in names:
        for a, b in zip(chain, chain[1:]):
            (x1, y1), (x2, y2) = P(a), P(b)
            s.append(line(x1, y1, x2, y2, BLUE if (a, b) in (seg or {}) and False else INK, 2))
    for k in pts:
        x, y = P(k)
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1
        s.append("<circle cx='%.1f' cy='%.1f' r='2.5' fill='%s'/>" % (x, y, INK))
        s.append(text(x + 17 * dx / n, y + 15 * dy / n + 5, k, 14))
    for (a, b), t in (seg or {}).items():
        (x1, y1), (x2, y2) = P(a), P(b)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = -(y2 - y1), x2 - x1
        n = math.hypot(nx, ny) or 1
        nx, ny = nx / n, ny / n
        if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny
        s.append(text(mx + 16 * nx, my + 16 * ny + 5, t, 13, col=RED if t in ("x", "y", "？") else BLUE))
    svg = svg_wrap(int(W), int(H), "".join(s) + extra, label)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def pi(c):
    """c π（c は Fraction／int）"""
    from fractions import Fraction as F
    from tw_common import fr
    c = F(c)
    if c == 0:
        return "0"
    neg = "－" if c < 0 else ""
    c = abs(c)
    if c.denominator == 1:
        return neg + ("π" if c == 1 else "%dπ" % c.numerator)
    return neg + fr("%sπ" % ("" if c.numerator == 1 else c.numerator), c.denominator)
