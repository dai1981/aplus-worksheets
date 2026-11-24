# -*- coding: utf-8 -*-
"""韓国（초등）の図の部品。点の名前は ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ。すべて inline SVG（viewBox 付き）"""
import math
from ws_common import fig, svg_wrap, text, line, GREEN, FILL, GRAY, INK, RED, BLUE

PT = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊ"
LIGHT = "#e8f3ec"


def dot(x, y, r=5, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%s' fill='%s'/>" % (x, y, r, col)


def arrow(x1, y1, x2, y2, col=INK, w=3):
    """(x2, y2) の先に矢印（반직선・직선の끝）"""
    a = math.atan2(y2 - y1, x2 - x1)
    p = [(x2, y2), (x2 - 14 * math.cos(a - 0.4), y2 - 14 * math.sin(a - 0.4)), (x2 - 14 * math.cos(a + 0.4), y2 - 14 * math.sin(a + 0.4))]
    return line(x1, y1, x2, y2, col, w) + "<polygon points='%s' fill='%s'/>" % (" ".join("%.1f,%.1f" % q for q in p), col)


def lab(x, y, t, fs=22, col=INK):
    return text(x, y + fs * 0.35, t, fs, col=col)


def line_kind(kind, a="ㄱ", b="ㄴ", W=300, H=90):
    """kind: segment(선분) / ray(반직선、a から b 方向) / ray_rev / line(직선) / curve(곡선)"""
    x1, x2, y = 50, W - 50, 45
    s = []
    if kind == "segment":
        s.append(line(x1, y, x2, y, INK, 3))
    elif kind == "ray":
        s.append(arrow(x1, y, x2 + 30, y))
    elif kind == "ray_rev":
        s.append(arrow(x2, y, x1 - 30, y))
    elif kind == "line":
        s.append(arrow(x2 - 10, y, x1 - 30, y) + arrow(x1 + 10, y, x2 + 30, y))
    else:
        s.append("<path d='M%d %d C %d %d, %d %d, %d %d' fill='none' stroke='%s' stroke-width='3'/>" % (x1, y, x1 + 60, y - 50, x2 - 60, y + 50, x2, y, INK))
    s.append(dot(x1, y) + dot(x2, y))
    s.append(lab(x1, y + 26, a) + lab(x2, y + 26, b))
    return fig(svg_wrap(W, H, "".join(s), "선 그림"))


def poly(pts, labels=None, right=(), W=260, H=200, fill=LIGHT, close=True, extra=""):
    """多角形。right は直角の印を付ける頂点の番号"""
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='3' stroke-linejoin='round'/>"
         % (" ".join("%.1f,%.1f" % p for p in pts), fill, INK) if close else
         "<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (" ".join("%.1f,%.1f" % p for p in pts), INK)]
    n = len(pts)
    for i in right:
        p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
        u = [(a[0] - p[0]), (a[1] - p[1])]
        v = [(b[0] - p[0]), (b[1] - p[1])]
        lu, lv = math.hypot(*u), math.hypot(*v)
        u = [c / lu * 14 for c in u]
        v = [c / lv * 14 for c in v]
        s.append("<polyline points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (p[0] + u[0], p[1] + u[1], p[0] + u[0] + v[0], p[1] + u[1] + v[1], p[0] + v[0], p[1] + v[1], RED))
    if labels:
        cx = sum(p[0] for p in pts) / n
        cy = sum(p[1] for p in pts) / n
        for p, t in zip(pts, labels):
            dx, dy = p[0] - cx, p[1] - cy
            d = math.hypot(dx, dy) or 1
            s.append(lab(p[0] + dx / d * 18, p[1] + dy / d * 18, t))
    s.append(extra)
    return fig(svg_wrap(W, H, "".join(s), "도형"))


def grid_poly(cells, W=None, H=None, c=26, fill=LIGHT, label="모눈종이 위의 도형"):
    """모눈종이에 그린 다각형。cells は格子点 (i, j) のリスト"""
    mi = max(p[0] for p in cells) + 2
    mj = max(p[1] for p in cells) + 2
    W, H = mi * c, mj * c
    s = []
    for i in range(mi + 1):
        s.append(line(i * c, 0, i * c, H, "#d5ddd8", 1))
    for j in range(mj + 1):
        s.append(line(0, j * c, W, j * c, "#d5ddd8", 1))
    s.append("<polygon points='%s' fill='%s' fill-opacity='0.7' stroke='%s' stroke-width='3'/>"
             % (" ".join("%d,%d" % ((p[0] + 1) * c, (p[1] + 1) * c) for p in cells), fill, INK))
    return fig(svg_wrap(W, H, "".join(s), label))


def ruler(start_mm, end_mm, total_cm=None, obj="막대"):
    """자（cm と mm の目盛り）と、start_mm から end_mm までの物"""
    total_cm = total_cm or (end_mm // 10 + 2)
    k = 20 if total_cm <= 12 else 14     # 1 cm の幅
    W = int(total_cm * k + 40)
    H = 110
    x0 = 20
    s = ["<rect x='%d' y='60' width='%d' height='42' fill='#fdf6e3' stroke='%s' stroke-width='1.5'/>" % (x0 - 6, total_cm * k + 12, INK)]
    for mm in range(total_cm * 10 + 1):
        x = x0 + mm * k / 10.0
        h = 18 if mm % 10 == 0 else (12 if mm % 5 == 0 else 7)
        s.append(line(x, 60, x, 60 + h, INK, 1.3 if mm % 10 == 0 else 0.8))
        if mm % 10 == 0:
            s.append(text(x, 96, str(mm // 10), 12, weight=400))
    s.append("<rect x='%.1f' y='26' width='%.1f' height='26' rx='5' fill='%s' stroke='%s' stroke-width='2'/>"
             % (x0 + start_mm * k / 10.0, (end_mm - start_mm) * k / 10.0, "#9ccfb0", GREEN))
    s.append(line(x0 + start_mm * k / 10.0, 52, x0 + start_mm * k / 10.0, 60, GRAY, 1, " stroke-dasharray='3 2'"))
    s.append(line(x0 + end_mm * k / 10.0, 52, x0 + end_mm * k / 10.0, 60, GRAY, 1, " stroke-dasharray='3 2'"))
    return fig(svg_wrap(W, H, "".join(s), "자로 잰 %s" % obj).replace("<svg ", "<svg data-pf='lg' ", 1))


def beaker(ml, cap=1000, step=100, W=200, H=250):
    """비커・계량컵：눈금 step mL、cap まで（数字は 2 칸마다）"""
    top, bot, x1, x2 = 16, 220, 80, 170
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2.5'/>" % (x1, top, x2 - x1, bot - top, INK)]
    lv = bot - (bot - top - 10) * ml / float(cap)
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='#9fd3f0'/>" % (x1 + 2, lv, x2 - x1 - 4, bot - lv - 1))
    n = cap // step
    for i in range(1, n + 1):
        y = bot - (bot - top - 10) * i / float(n)
        big = i % 2 == 0
        s.append(line(x1, y, x1 + (22 if big else 12), y, INK, 2 if big else 1.4))
        if big:
            s.append(text(x1 - 8, y + 5, str(i * step), 15, anchor="end", weight=700))
    s.append(text((x1 + x2) / 2, 244, "(mL)", 14, weight=400))
    return fig(svg_wrap(W, H, "".join(s), "물이 든 그릇").replace("<svg ", "<svg data-pf='lg' ", 1))


def scale(g, cap=2000, step=100, label_every=500, size=210):
    """저울（바늘が g を指す。目盛りは step g、label_every g ごとに数字、0 が上）"""
    cx = cy = size / 2.0
    r = size / 2.0 - 8
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='4'/>" % (cx, cy, r, GREEN)]
    n = cap // step
    for i in range(n):
        a = math.radians(i * 360.0 / n - 90)
        big = (i * step) % label_every == 0
        r1 = r - (14 if big else 7)
        s.append(line(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a), INK, 2 if big else 1))
        if big:
            v = i * step
            t = ("%d" % (v // 1000) if v % 1000 == 0 else "%d" % v) if cap > 1000 else str(v)
            if cap > 1000 and v % 1000 != 0:
                t = str(v)
            s.append(text(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a) + 5, t, 13, weight=400))
    a = math.radians(g * 360.0 / cap - 90)
    s.append(line(cx, cy, cx + (r - 20) * math.cos(a), cy + (r - 20) * math.sin(a), RED, 3))
    s.append(dot(cx, cy, 5))
    s.append(text(cx, cy + 34, "(g)" if cap <= 1000 else "(kg)", 12, weight=400))
    return fig(svg_wrap(int(size), int(size), "".join(s), "저울").replace("<svg ", "<svg data-pf='lg' ", 1))


def circle_fig(r_px, show="radius", label=None, W=220, H=220, ruler_cm=None):
    """원과 중심・반지름・지름"""
    cx, cy = W / 2.0, H / 2.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='3'/>" % (cx, cy, r_px, LIGHT, INK), dot(cx, cy)]
    if show in ("radius", "both"):
        s.append(line(cx, cy, cx + r_px, cy, RED, 3))
    if show in ("diameter", "both"):
        s.append(line(cx - r_px, cy + (0 if show == "diameter" else 0), cx + r_px, cy, BLUE if show == "both" else RED, 3))
    s.append(lab(cx - 2, cy - 14, "ㅇ"))
    if label:
        s.append(text(cx + r_px / 2.0, cy + 26, label, 20))
    return fig(svg_wrap(W, H, "".join(s), "원").replace("<svg ", "<svg data-pf='lg' ", 1))


def pic_graph(rows, big, small, unit_word, title, icon="dot"):
    """그림그래프：rows = [(이름, 값)]。큰 그림 = big、작은 그림 = small"""
    rh = 44
    W, H = 500, 70 + rh * len(rows) + 40
    s = [text(W / 2, 22, title, 16)]
    s.append("<rect x='10' y='34' width='%d' height='%d' fill='none' stroke='%s' stroke-width='1.5'/>" % (W - 20, rh * len(rows), INK))
    s.append(line(110, 34, 110, 34 + rh * len(rows), INK, 1.5))
    for i, (nm, v) in enumerate(rows):
        y = 34 + rh * i
        if i:
            s.append(line(10, y, W - 10, y, INK, 1))
        s.append(text(60, y + 28, nm, 15))
        x = 130
        nb, ns = divmod(v, big)
        ns //= small
        for _ in range(nb):
            s.append("<circle cx='%d' cy='%d' r='15' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x + 14, y + 22, "#f0b429", INK))
            x += 36
        for _ in range(ns):
            s.append("<circle cx='%d' cy='%d' r='8' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x + 8, y + 22, "#f0b429", INK))
            x += 22
    y = 34 + rh * len(rows) + 26
    s.append("<circle cx='150' cy='%d' r='12' fill='#f0b429' stroke='%s' stroke-width='1.5'/>" % (y - 4, INK))
    s.append(text(170, y + 1, "%d%s" % (big, unit_word), 14, anchor="start"))
    s.append("<circle cx='290' cy='%d' r='7' fill='#f0b429' stroke='%s' stroke-width='1.5'/>" % (y - 4, INK))
    s.append(text(304, y + 1, "%d%s" % (small, unit_word), 14, anchor="start"))
    return fig(svg_wrap(W, H, "".join(s), title).replace("<svg ", "<svg data-pf='lg' ", 1))


def frac_bar(n, d, W=320, H=56, col=GREEN):
    """똑같이 d로 나눈 막대 중 n칸 색칠"""
    w = (W - 20) / float(d)
    s = []
    for i in range(d):
        s.append("<rect x='%.1f' y='10' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (10 + i * w, w, H - 20, "#8fd0a8" if i < n else "#ffffff", INK))
    return fig(svg_wrap(W, H, "".join(s), "%d칸 중 %d칸 색칠한 막대" % (d, n)))


def frac_circle(n, d, size=150):
    cx = cy = size / 2.0
    r = size / 2.0 - 6
    s = []
    for i in range(d):
        a1 = math.radians(i * 360.0 / d - 90)
        a2 = math.radians((i + 1) * 360.0 / d - 90)
        big = 1 if 360.0 / d > 180 else 0
        if d == 1:
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, "#8fd0a8" if n else "#fff", INK))
            continue
        s.append("<path d='M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (cx, cy, cx + r * math.cos(a1), cy + r * math.sin(a1), r, r, big, cx + r * math.cos(a2), cy + r * math.sin(a2),
                    "#8fd0a8" if i < n else "#ffffff", INK))
    return fig(svg_wrap(int(size), int(size), "".join(s), "%d조각 중 %d조각 색칠한 원" % (d, n)))


def number_line(lo, hi, ticks, marks=(), labels=None, W=520, H=80):
    """수직선：lo〜hi を ticks 等分。marks = [(値の位置 index, 文字)]"""
    x0, x1, y = 30, W - 30, 40
    s = [line(x0, y, x1, y, INK, 2)]
    for i in range(ticks + 1):
        x = x0 + (x1 - x0) * i / float(ticks)
        big = labels and i in labels
        s.append(line(x, y - (12 if big else 7), x, y + (12 if big else 7), INK, 2 if big else 1.3))
        if big:
            s.append(text(x, y + 32, labels[i], 15))
    for i, t in marks:
        x = x0 + (x1 - x0) * i / float(ticks)
        s.append(arrow(x, y - 34, x, y - 8, RED, 2.5) + text(x, y - 40, t, 16, col=RED))
    return fig(svg_wrap(W, H + 10, "".join(s), "수직선").replace("<svg ", "<svg data-pf='lg' ", 1))


# ---- k_pics の絵（물건）に韓国語の aria-label
import re as _re
import k_pics as _K
KO = {"apple": ("사과", "개"), "star": ("별", "개"), "ball": ("공", "개"), "button": ("단추", "개"), "fish": ("물고기", "마리"),
      "flower": ("꽃", "송이"), "heart": ("하트", "개"), "duck": ("오리", "마리"), "cup": ("컵", "개"), "bug": ("무당벌레", "마리")}
KINDS = list(KO)


def _ko(svg, label):
    return fig(_re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1))


def groups(gs, gap=30):
    """gs = [(n, kind)]"""
    k = gs[0][1]
    return _ko(_K.groups_svg(gs, gap), "%s %d묶음" % (KO[k][0], len(gs)))


def row(n, kind, per_row=10):
    return _ko(_K.row_svg(n, kind, per_row), "%s %d%s" % (KO[kind][0], n, KO[kind][1]))


def array(rows, cols, kind):
    return _ko(_K.array_svg(rows, cols, kind), "%s %d줄 %d%s씩" % (KO[kind][0], rows, cols, KO[kind][1]))
