# -*- coding: utf-8 -*-
"""國小低年級（一、二年級）の絵：k_pics の絵を中国語の aria-label で使う＋台灣の硬幣・紙鈔"""
import re
import k_pics as K
from ws_common import svg_wrap, text, fig, INK, GREEN

KIND = {"apple": ("蘋果", "顆"), "star": ("星星", "顆"), "ball": ("球", "顆"), "button": ("鈕扣", "顆"),
        "fish": ("魚", "條"), "flower": ("花", "朵"), "heart": ("愛心", "個"), "duck": ("鴨子", "隻"),
        "cup": ("杯子", "個"), "bug": ("瓢蟲", "隻")}
KINDS = list(KIND)


def nm(kind):
    return KIND[kind][0]


def cl(kind):
    return KIND[kind][1]


def zh(svg, label):
    return fig(re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1))


def row(n, kind, per_row=10):
    return zh(K.row_svg(n, kind, per_row), "%d%s%s" % (n, cl(kind), nm(kind)))


def scatter(n, kind, seed):
    return zh(K.scatter_svg(n, kind, seed), "%s" % nm(kind))


def groups(gs):
    return zh(K.groups_svg(gs), "兩堆東西")


def crossed(n, kind, k):
    return zh(K.crossed_row_svg(n, kind, k), "%d%s%s，劃掉 %d%s" % (n, cl(kind), nm(kind), k, cl(kind)))


def tenframe(n, frames=None):
    return zh(K.tenframe_svg(n, frames), "十格板")


def rods(t, o):
    return zh(K.rods_svg(t, o), "%d 條十個積木和 %d 個積木" % (t, o))


def numline(lo, hi, marks=None, sp=40):
    return zh(K.number_line_svg(lo, hi, marks, sp), "數線")


def towers(hs, labels):
    return zh(K.towers_svg(hs, labels), "積木塔")


def pencils(lengths, labels, unit=34):
    return zh(K.pencils_svg(lengths, labels, unit), "鉛筆")


def shapes_row(items, labels=None, size=30):
    """items: [(kind, color)]。labels があれば下に文字"""
    W = len(items) * 86 + 10
    s = []
    for i, (k, c) in enumerate(items):
        cx = 50 + i * 86
        s.append(K.shape(k, cx, 42, size, c))
        if labels:
            s.append(text(cx, 98, labels[i], 16))
    return fig(svg_wrap(W, 108 if labels else 84, "".join(s), "圖形"))


def solids_row(items, labels=None):
    W = len(items) * 100 + 10
    s = []
    for i, (k, c) in enumerate(items):
        cx = 56 + i * 100
        s.append(K.solid(k, cx, 52, 32, c))
        if labels:
            s.append(text(cx, 118, labels[i], 16))
    return fig(svg_wrap(W, 128 if labels else 104, "".join(s), "立體"))


COIN = {1: (15, "#d4a35a", "#8a5a1a"), 5: (19, "#cfd4d8", "#6c7378"), 10: (22, "#d9dde0", "#6c7378"), 50: (25, "#e9c95a", "#9b7a14")}


def money_svg(vals, label="錢"):
    """vals: 金額のリスト（1、5、10、50 は硬幣、100・500・1000 は紙鈔）"""
    s = []
    x = 8
    H = 66
    for v in vals:
        if v in COIN:
            r, f, st = COIN[v]
            s.append("<circle cx='%.1f' cy='33' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x + r, r, f, st))
            s.append(text(x + r, 39, str(v), 15 if v < 10 else 14, col=INK))
            x += 2 * r + 8
        else:
            col = {100: "#e8a0a0", 500: "#e8b47a", 1000: "#9fc2e8"}[v]
            s.append("<rect x='%d' y='8' width='84' height='50' rx='4' fill='%s' stroke='%s' stroke-width='1.6'/>" % (x, col, INK))
            s.append(text(x + 42, 40, "%d元" % v, 16))
            x += 92
    return fig(svg_wrap(x, H, "".join(s), label))


def mixed(counts, seed):
    return zh(K.mixed_svg(counts, seed), "混在一起的東西")


def array(r, c, kind):
    return zh(K.array_svg(r, c, kind), "%d 排，每排 %d %s%s" % (r, c, cl(kind), nm(kind)))


def circles(gs, kind):
    """gs 盤，各 n 個（平分・分裝）"""
    return zh(K.groups_svg([(n, kind) for n in gs]), "分成幾堆")


def col(a, b, op, fs=28):
    """直式（答えなし）。op は ＋ または －"""
    cw = fs * 0.62
    rows = [str(a), str(b)]
    longest = max(len(r) for r in rows) * cw
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 14)
    right = W - 12
    s = []

    def put(t, y):
        for k, ch in enumerate(reversed(t)):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' font-family='monospace'>%s</text>" % (right - cw * k - cw / 2, y, fs, INK, ch))
    y1, y2 = 10 + fs, 10 + int(fs * 2.15)
    put(rows[0], y1)
    put(rows[1], y2)
    sx = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (sx, y2, fs, GREEN, op))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sx - cw * 0.6, ly, right, ly, INK))
    return fig(svg_wrap(W, ly + 14, "".join(s), "直式"))


def blocks(h, t, o):
    """百・十・一の積木"""
    s = []
    x = 8
    u = 7
    for _ in range(h):
        s.append("<rect x='%d' y='8' width='%d' height='%d' fill='#f7d774' stroke='%s' stroke-width='1.2'/>" % (x, 10 * u, 10 * u, INK))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='8' x2='%d' y2='%d' stroke='#c9a93a' stroke-width='0.6'/>" % (x + i * u, x + i * u, 8 + 10 * u))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#c9a93a' stroke-width='0.6'/>" % (x, 8 + i * u, x + 10 * u, 8 + i * u))
        x += 10 * u + 8
    for _ in range(t):
        s.append("<rect x='%d' y='8' width='%d' height='%d' fill='#7fb3e6' stroke='%s' stroke-width='1.2'/>" % (x, u, 10 * u, INK))
        x += u + 5
    x += 4
    for i in range(o):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#f4a3a3' stroke='%s' stroke-width='1.2'/>" % (x + (i % 3) * (u + 3), 8 + 10 * u - u - (i // 3) * (u + 3), u, u, INK))
    if o:
        x += 3 * (u + 3)
    return fig(svg_wrap(x + 8, 10 * u + 16, "".join(s), "%d 個百、%d 個十、%d 個一" % (h, t, o)))


def ruler(n, start, length, label="鉛筆"):
    """0〜n 公分の尺、上に start から length 公分の棒"""
    u = 28
    W = n * u + 40
    s = ["<rect x='20' y='44' width='%d' height='34' fill='#fdf3c7' stroke='%s' stroke-width='1.4'/>" % (n * u, INK)]
    for i in range(n * 10 + 1):
        x = 20 + i * u / 10
        h = 14 if i % 10 == 0 else 9 if i % 5 == 0 else 5
        s.append("<line x1='%.1f' y1='44' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>" % (x, x, 44 + h, INK, 1.4 if i % 10 == 0 else 0.7))
        if i % 10 == 0:
            s.append(text(x, 72, str(i // 10), 11, weight=400))
    x0 = 20 + start * u
    s.append("<rect x='%.1f' y='14' width='%.1f' height='16' rx='3' fill='#e74c3c' stroke='%s' stroke-width='1.3'/>" % (x0, length * u, INK))
    s.append("<line x1='%.1f' y1='30' x2='%.1f' y2='44' stroke='%s' stroke-dasharray='3,3'/>" % (x0, x0, INK))
    s.append("<line x1='%.1f' y1='30' x2='%.1f' y2='44' stroke='%s' stroke-dasharray='3,3'/>" % (x0 + length * u, x0 + length * u, INK))
    return fig(svg_wrap(W, 86, "".join(s), "用尺量%s" % label).replace("<svg ", "<svg data-pf='lg' ", 1))


def frac(kind, n, k=1, size=46):
    """kind: circle / rect / square を n 等分し k 個塗る"""
    import math
    s = []
    cx, cy = size + 8, size + 8
    if kind == "circle":
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n - math.pi / 2, 2 * math.pi * (i + 1) / n - math.pi / 2
            x0, y0 = cx + size * math.cos(a0), cy + size * math.sin(a0)
            x1, y1 = cx + size * math.cos(a1), cy + size * math.sin(a1)
            big = 1 if a1 - a0 > math.pi else 0
            col_ = "#7fb3e6" if i < k else "white"
            if n == 1:
                s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, size, col_, INK))
            else:
                s.append("<path d='M%d,%d L%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f Z' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, x0, y0, size, size, big, x1, y1, col_, INK))
        W, H = 2 * size + 16, 2 * size + 16
    else:
        w = 2 * size * (1.6 if kind == "rect" else 1)
        h = 2 * size * (0.8 if kind == "rect" else 1)
        for i in range(n):
            col_ = "#7fb3e6" if i < k else "white"
            s.append("<rect x='%.1f' y='8' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='1.6'/>" % (8 + i * w / n, w / n, h, col_, INK))
        W, H = w + 16, h + 16
    return fig(svg_wrap(int(W), int(H), "".join(s), "%d 等分塗 %d 份" % (n, k)))
