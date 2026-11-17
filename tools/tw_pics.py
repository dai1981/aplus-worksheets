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
