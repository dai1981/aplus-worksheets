# -*- coding: utf-8 -*-
"""
台灣 國小三年級：容量（公升・毫升）と重量（公斤・公克）の共通部品。
どちらも 1 大單位 ＝ 1000 小單位。gen_tw_math_g3_liters_and_milliliters.py / gen_tw_math_g3_kilograms_and_grams.py から使う。
誤答：2 公升 50 毫升 → 250 毫升（0 を落とす）、2050 → 20 公升 50 毫升、1000 ではなく 100 で換算、繰り上がり忘れ。
"""
import math
from tw_common import mcq, fig, svg_wrap, text, line, GREEN, FILL, INK, RED, BLUE


def bs(v, B, S):
    """3050 → 3 公升 50 毫升"""
    b, s = divmod(v, 1000)
    if b and s:
        return "%d %s %d %s" % (b, B, s, S)
    if b:
        return "%d %s" % (b, B)
    return "%d %s" % (s, S)


def beaker(level, top, step, label_every):
    """量杯：0〜top 毫升、step ごとに目盛り、label_every ごとに數字。水位 level"""
    H = 200
    y0, y1 = 220, 220 - H
    s = ["<path d='M40 %d L40 230 Q40 240 50 240 L150 240 Q160 240 160 230 L160 %d' fill='none' stroke='%s' stroke-width='3'/>" % (y1 - 10, y1 - 10, INK)]
    lv = y0 - H * level / top
    s.append("<rect x='42' y='%.1f' width='116' height='%.1f' fill='#cde4f5'/>" % (lv, 238 - lv))
    s.append(line(42, lv, 158, lv, BLUE, 2))
    n = top // step
    for i in range(n + 1):
        y = y0 - H * i / n
        v = i * step
        big = v % label_every == 0
        s.append(line(40, y, 40 + (26 if big else 14), y, INK, 2 if big else 1.2))
        if big and v:
            s.append(text(176, y + 5, "%d" % v, 13, anchor="start"))
    s.append(text(176, 238, "毫升", 12, anchor="start"))
    return fig(svg_wrap(240, 250, "".join(s), "量杯，水位 %d 毫升" % level))


def dial(g, top):
    """秤：0〜top 公克、100 公克ごとに目盛り、1 公斤ごとに數字（top が 1000 のときは 100 公克ごとに數字）"""
    cx, cy, r = 120, 125, 100
    s = ["<rect x='14' y='18' width='212' height='214' rx='22' fill='#f3f3f3' stroke='%s' stroke-width='2'/>" % INK,
         "<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='%s' stroke-width='3'/>" % (cx, cy, r, GREEN)]
    n = top // 100
    for i in range(n):
        a = math.radians(-90 + 360 * i / n)
        big = (i * 100) % (1000 if top > 1000 else 500) == 0
        mid = top > 1000 and (i * 100) % 500 == 0
        r1 = r - (16 if big else (11 if mid else 7))
        s.append(line(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a), INK, 2.4 if big else 1.2))
        if (top > 1000 and i * 100 % 1000 == 0) or (top <= 1000 and i % 1 == 0 and i * 100 % 200 == 0):
            t = str(i * 100 // 1000) if top > 1000 else str(i * 100)
            rr = r - 30
            s.append(text(cx + rr * math.cos(a), cy + rr * math.sin(a) + 5, t, 12))
    a = math.radians(-90 + 360 * g / top)
    s.append(line(cx, cy, cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a), RED, 3))
    s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (cx, cy, RED))
    s.append(text(cx, 248, "單位：公克" if top <= 1000 else "單位：公斤（1 小格 100 公克）", 12))
    return fig(svg_wrap(240, 256, "".join(s), "秤的指針"))
