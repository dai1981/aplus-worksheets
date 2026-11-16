# -*- coding: utf-8 -*-
"""七年級：坐標平面の図"""
from tw_common import fig, svg_wrap, text, line, INK, RED, BLUE
from tw_g7 import sn

C = 18


def plane(n=6, pts=(), lines=(), lg=True):
    """pts: [(x, y, name)]、lines: [((x1,y1),(x2,y2),color)]"""
    W = H = (2 * n + 2) * C
    o = W / 2
    X = lambda x: o + x * C
    Y = lambda y: o - y * C
    s = []
    for i in range(-n, n + 1):
        s.append("<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='#e2e2e2' stroke-width='1'/>" % (X(i), Y(-n), X(i), Y(n)))
        s.append("<line x1='%.0f' y1='%.0f' x2='%.0f' y2='%.0f' stroke='#e2e2e2' stroke-width='1'/>" % (X(-n), Y(i), X(n), Y(i)))
    s.append(line(X(-n) - 6, o, X(n) + 8, o, INK, 1.6))
    s.append(line(o, Y(-n) + 6, o, Y(n) - 8, INK, 1.6))
    s.append(text(X(n) + 6, o - 6, "x", 12, col=INK))
    s.append(text(o + 8, Y(n) - 4, "y", 12, col=INK))
    s.append(text(o - 8, o + 14, "O", 11, col=INK))
    for i in range(-n, n + 1):
        if i and i % 2 == 0:
            s.append(text(X(i), o + 14, sn(i), 10))
            s.append(text(o - 10, Y(i) + 4, sn(i), 10, anchor="end"))
    for (x1, y1), (x2, y2), col in lines:
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4'/>" % (X(x1), Y(y1), X(x2), Y(y2), col))
    for x, y, name in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (X(x), Y(y), RED))
        s.append(text(X(x) + 8, Y(y) - 6, name, 13, anchor="start", col=RED).replace("<text ", "<text stroke='#fff' stroke-width='3' paint-order='stroke' ", 1))
    svg = svg_wrap(int(W), int(H), "".join(s), "坐標平面")
    return fig(svg.replace("<svg ", "<svg data-pf='lg' ", 1) if lg else svg)
