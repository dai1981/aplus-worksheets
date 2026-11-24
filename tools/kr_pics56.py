# -*- coding: utf-8 -*-
"""대한민국 초등 5・6학년の図：쌓기나무（等角図）・직육면체・원・띠그래프・원그래프・수직선의 범위・선대칭/점대칭"""
import math
from ws_common import fig, svg_wrap, text, line, GREEN, INK, RED, BLUE
from kr_pics import dot, lab, LIGHT

C30, S30 = math.cos(math.radians(30)), 0.5
TOP, RIGHT, LEFT = "#e6f4ea", "#9fd1ae", "#c3e5cc"
COLS = ["#4e9a6b", "#f0b429", "#5b8def", "#e0675a", "#9b6bd1", "#7fb7a8"]


def lg(svg):
    return svg.replace("<svg ", "<svg data-pf='lg' ", 1)


def iso_cubes(cells, label="쌓기나무", A=26, front=True):
    """cells：(x, y, z)。x は右、y は手前、z は上"""
    def P(x, y, z):
        return ((x - y) * A * C30, (x + y) * A * S30 - z * A)
    pts = [P(x + dx, y + dy, z + dz) for (x, y, z) in cells for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    if front:
        mx_ = max(c[0] for c in cells) + 1
        my_ = max(c[1] for c in cells) + 1
        fx_, fy_ = P(mx_ / 2.0, my_, 0.5)
        lx_, ly_ = fx_ - C30 * 60, fy_ + S30 * 60
        pts = pts + [(lx_ - 14, ly_ + 10), (lx_ + 14, ly_ + 10)]
    minx, miny = min(p[0] for p in pts) - 10, min(p[1] for p in pts) - 10
    W, H = max(p[0] for p in pts) - minx + 10, max(p[1] for p in pts) - miny + 10

    def Q(x, y, z):
        px, py = P(x, y, z)
        return "%.1f,%.1f" % (px - minx, py - miny)
    s = []
    for (x, y, z) in sorted(cells, key=lambda c: (c[0] + c[1], c[2])):
        for f, col in (([Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], TOP),
                       ([Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)], RIGHT),
                       ([Q(x, y + 1, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], LEFT)):
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.4'/>" % (" ".join(f), col, GREEN))
    if front:
        ax, ay = lx_ - minx, ly_ - miny
        tx, ty = fx_ - minx - C30 * 14, fy_ - miny + S30 * 14
        s.append(text(ax, ay + 8, "앞", 17))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (ax + C30 * 14, ay - S30 * 14, tx, ty, RED))
        a_ = math.atan2(ty - (ay - S30 * 14), tx - (ax + C30 * 14))
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (tx, ty, tx - 10 * math.cos(a_ - 0.45), ty - 10 * math.sin(a_ - 0.45),
                                                                                tx - 10 * math.cos(a_ + 0.45), ty - 10 * math.sin(a_ + 0.45), RED))
    return fig(lg(svg_wrap(int(W), int(H), "".join(s), label)))


def view_grid(cols_rows, w, h, ox, oy, sz=22):
    s = []
    for (c, r) in cols_rows:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#bfe0c6' stroke='%s' stroke-width='1.4'/>" % (ox + c * sz, oy + r * sz, sz, sz, GREEN))
    return "".join(s)


def views_panel(views, labels="가나다라"):
    """views：[(cells(c, r), w, h)]。가〜라 を横に並べる"""
    s, x = [], 10
    hmax = max(v[2] for v in views)
    for t, (cells, w, h) in zip(labels, views):
        s.append(text(x + w * 22 / 2.0, 18, t, 17))
        s.append(view_grid(cells, w, h, x, 28 + (hmax - h) * 22))
        x += w * 22 + 34
    return fig(lg(svg_wrap(x, 34 + hmax * 22, "".join(s), "가, 나, 다, 라 모양")))


def box_svg(a, b, c, u="cm", labels=True):
    """가로 a、세로 b、높이 c の직육면체（겨냥도：보이지 않는 모서리는 점선）"""
    s_ = 150.0 / max(a, b * .6, c, 1)
    W, Dp, H = a * s_, b * s_ * .5, c * s_
    ox, oy = 30, 18 + Dp
    P = lambda pts: " ".join("%.1f,%.1f" % p for p in pts)
    front = [(ox, oy), (ox + W, oy), (ox + W, oy + H), (ox, oy + H)]
    top = [(ox, oy), (ox + Dp, oy - Dp), (ox + W + Dp, oy - Dp), (ox + W, oy)]
    side = [(ox + W, oy), (ox + W + Dp, oy - Dp), (ox + W + Dp, oy + H - Dp), (ox + W, oy + H)]
    g = "".join("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.2'/>" % (P(f), col, INK)
                for f, col in ((front, "#e8f3ec"), (top, "#f4faf6"), (side, "#cfe8d7")))
    hx, hy = ox + Dp, oy + H - Dp
    dash = " stroke-dasharray='6 5'"
    g += line(hx, hy, ox, oy + H, INK, 1.6, dash) + line(hx, hy, ox + W + Dp, hy, INK, 1.6, dash) + line(hx, hy, hx, oy - Dp, INK, 1.6, dash)
    if labels:
        g += text(ox + W / 2, oy + H + 24, "%s %s" % (a, u), 17)
        g += text(ox + W + Dp + 8, oy + H / 2 - Dp / 2 + 18, "%s %s" % (c, u), 17, anchor="start")
        g += text(ox + W + Dp / 2 + 10, oy - Dp / 2 + 18, "%s %s" % (b, u), 17, anchor="start")
    return fig(lg(svg_wrap(int(ox + W + Dp + 90), int(oy + H + 34), g, "직육면체")))


def circle_svg(r_label, kind="r", W=230, H=200, ring=False):
    cx, cy, Rr = W / 2.0, H / 2.0, 80
    s = ["<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, Rr, LIGHT, INK), dot(cx, cy, 4)]
    if kind == "d":
        s.append(line(cx - Rr, cy, cx + Rr, cy, RED, 3))
    else:
        s.append(line(cx, cy, cx + Rr, cy, RED, 3))
    s.append(text(cx + (0 if kind == "d" else Rr / 2), cy + 26, r_label, 19, col=RED).replace("<text ", "<text stroke='#fff' stroke-width='4' paint-order='stroke' ", 1))
    return fig(lg(svg_wrap(W, H, "".join(s), "원")))


def strip_graph(title, cats, ps, W=520):
    """띠그래프：ps は % の整数（合計 100）"""
    x0, w = 20, W - 40
    s = [text(W / 2, 22, title, 17)]
    x = x0
    for i, (c, p) in enumerate(zip(cats, ps)):
        ww = w * p / 100.0
        s.append("<rect x='%.1f' y='40' width='%.1f' height='56' fill='%s' stroke='#fff' stroke-width='2'/>" % (x, ww, COLS[i]))
        if p >= 10:
            s.append(text(x + ww / 2, 64, c, 15, col="#fff"))
            s.append(text(x + ww / 2, 86, "%d%%" % p, 15, col="#fff"))
        x += ww
    for i in range(11):
        xx = x0 + w * i / 10.0
        s.append(line(xx, 100, xx, 108, INK, 1.3) + text(xx, 126, str(i * 10), 13))
    s.append("<rect x='%d' y='40' width='%d' height='56' fill='none' stroke='%s' stroke-width='2'/>" % (x0, w, INK))
    small = [(c, p) for c, p in zip(cats, ps) if p < 10]
    if small:
        s.append(text(x0, 152, "작은 칸: " + ", ".join("%s %d%%" % cp for cp in small), 14, anchor="start"))
    return fig(lg(svg_wrap(W, 160 if small else 136, "".join(s), title + " 띠그래프")))


def pie_graph(title, cats, ps, W=400, H=250):
    cx, cy, r = 130, 135, 100
    s = [text(W / 2, 22, title, 17)]
    a0 = -90.0
    for i, (c, p) in enumerate(zip(cats, ps)):
        a1 = a0 + p * 3.6
        x0_, y0_ = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1_, y1_ = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='2'/>"
                 % (cx, cy, x0_, y0_, r, r, 1 if p > 50 else 0, x1_, y1_, COLS[i]))
        mid = math.radians((a0 + a1) / 2)
        if p >= 10:
            s.append(text(cx + r * .62 * math.cos(mid), cy + r * .62 * math.sin(mid) + 5, "%d%%" % p, 15, col="#fff"))
        a0 = a1
    for i, (c, p) in enumerate(zip(cats, ps)):
        y = 70 + i * 30
        s.append("<rect x='255' y='%d' width='16' height='16' fill='%s'/>" % (y - 13, COLS[i]))
        s.append(text(278, y, "%s %d%%" % (c, p), 15, anchor="start"))
    return fig(lg(svg_wrap(W, H, "".join(s), title + " 원그래프")))


def range_line(lo, hi, a, b, closed_a, closed_b, W=520):
    """수직선에 수의 범위（●：포함、○：포함하지 않음）。a or b が None なら그 방향으로 끝까지"""
    x0, x1, y = 30, W - 30, 50
    n = hi - lo
    X = lambda v: x0 + (x1 - x0) * (v - lo) / float(n)
    s = [line(x0 - 10, y, x1 + 10, y, INK, 2)]
    for v in range(lo, hi + 1):
        s.append(line(X(v), y - 7, X(v), y + 7, INK, 1.5) + text(X(v), y + 30, str(v), 15))
    xa = X(a) if a is not None else x0 - 10
    xb = X(b) if b is not None else x1 + 10
    s.append(line(xa, y - 18, xb, y - 18, RED, 4))
    for v, c in ((a, closed_a), (b, closed_b)):
        if v is not None:
            s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='3'/>" % (X(v), y - 18, RED if c else "#fff", RED))
    return fig(lg(svg_wrap(W, 92, "".join(s), "수직선에 나타낸 수의 범위")))


def sym_grid(cells, n=8, c=28, axis=None, center=None, label="모눈종이 위의 도형"):
    """모눈종이에 칠한 칸 cells(i, j)。axis='v' は가운데 세로선、'h' は가로선、center=(x, y) 格子点"""
    W = H = n * c + 2
    s = []
    for i in range(n + 1):
        s.append(line(1 + i * c, 1, 1 + i * c, H - 1, "#d5ddd8", 1) + line(1, 1 + i * c, W - 1, 1 + i * c, "#d5ddd8", 1))
    for (i, j) in cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#8fd0a8' stroke='%s' stroke-width='1'/>" % (1 + i * c, 1 + j * c, c, c, INK))
    if axis == "v":
        s.append(line(1 + n * c / 2, 1, 1 + n * c / 2, H - 1, RED, 3, " stroke-dasharray='8 5'"))
    if axis == "h":
        s.append(line(1, 1 + n * c / 2, W - 1, 1 + n * c / 2, RED, 3, " stroke-dasharray='8 5'"))
    if center:
        s.append(dot(1 + center[0] * c, 1 + center[1] * c, 6, RED))
    return fig(lg(svg_wrap(W, H, "".join(s), label)))
