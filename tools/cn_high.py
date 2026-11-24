# -*- coding: utf-8 -*-
"""
中国 五・六年级の自前の問題：数对（位置）、方向和距离、税率和利率、圆锥・圆柱的侧面积、鸽巢问题、解方程（正の数だけ）。
setup(R) してから使う。
"""
import math
import random
import re
from ws_common import svg_wrap, text, fig, INK, GREEN, RED, FILL, BLUE
from cn_common import mcq, Names

R = random.Random(0)
NM = Names(R)


def setup(rnd):
    global R, NM
    R = rnd
    NM = Names(rnd)


def nonneg(it):
    """keep：負の数が出てこない"""
    t = re.sub(r"<svg.*?</svg>", "", it["q"] + " " + " ".join(it["c"]) + " " + it["e"], flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return not re.search(r"(^|[（(＝=，,：\s×÷])\s*[－−-]\s?\d", t)


def fmt(x, p=2):
    s = ("%." + str(p) + "f") % x
    return s.rstrip("0").rstrip(".") if "." in s else s


# ------------------------------------------------------------------ 数对（五年级上）
SEATS = ["小明", "小红", "丽丽", "小刚", "天天", "乐乐", "笑笑", "浩浩", "婷婷", "小军"]


def grid_svg(cols, rows, marks, label="方格图"):
    """marks: {(c, r): 名前}。列は左から 1、行は下から 1"""
    u = 40
    W, H = 40 + cols * u, 30 + rows * u + 10
    s = []
    for c in range(cols + 1):
        s.append("<line x1='%d' y1='10' x2='%d' y2='%d' stroke='#bbb'/>" % (30 + c * u, 30 + c * u, 10 + rows * u))
    for r in range(rows + 1):
        s.append("<line x1='30' y1='%d' x2='%d' y2='%d' stroke='#bbb'/>" % (10 + r * u, 30 + cols * u, 10 + r * u))
    for c in range(1, cols + 1):
        s.append(text(30 + c * u, 28 + rows * u, str(c), 13))
    for r in range(1, rows + 1):
        s.append(text(20, 15 + (rows - r) * u + u + 0, str(r), 13))
    s.append(text(18, 28 + rows * u, "0", 13))
    for (c, r), nm in marks.items():
        x, y = 30 + c * u, 10 + (rows - r) * u
        s.append("<circle cx='%d' cy='%d' r='6' fill='%s'/>" % (x, y, RED))
        s.append(text(x + 4, y - 9, nm, 12, anchor="start"))
    return fig(svg_wrap(W, H, "".join(s), label))


def pair_read():
    def mk():
        pts = {}
        while len(pts) < 4:
            pts[(R.randint(1, 6), R.randint(1, 5))] = None
        names = R.sample(["A", "B", "C", "D"], 4)
        marks = dict(zip(pts, names))
        (c, r), n = R.choice(list(marks.items()))
        return mcq("点 %s 的位置用数对表示是什么？（先列后行）%s" % (n, grid_svg(6, 5, marks)), "(%d, %d)" % (c, r),
                   ["(%d, %d)" % (r, c) if r != c else "(%d, %d)" % (c + 1, r), "(%d, %d)" % (c + 1, r), "(%d, %d)" % (c, r + 1), "(%d, %d)" % (c - 1 if c > 1 else c + 2, r)],
                   "从 0 往右数到第 %d 列，再往上数到第 %d 行，写作 <b>(%d, %d)</b>。" % (c, r, c, r))
    return mk


def pair_find():
    def mk():
        pts = {}
        while len(pts) < 4:
            pts[(R.randint(1, 6), R.randint(1, 5))] = None
        names = R.sample(["A", "B", "C", "D"], 4)
        marks = dict(zip(pts, names))
        (c, r), n = R.choice(list(marks.items()))
        return mcq("数对 (%d, %d) 表示的是哪个点？%s" % (c, r, grid_svg(6, 5, marks)), n, [x for x in names if x != n],
                   "第 %d 列、第 %d 行的点是 <b>%s</b>。" % (c, r, n))
    return mk


def pair_seat():
    def mk():
        n = R.choice(SEATS)
        c, r = R.randint(1, 8), R.randint(1, 7)
        k = R.choice(["write", "same_row", "same_col", "move"])
        if k == "write":
            return mcq("教室里，%s坐在第 %d 列第 %d 行，用数对表示是什么？" % (n, c, r), "(%d, %d)" % (c, r),
                       ["(%d, %d)" % (r, c) if r != c else "(%d, %d)" % (c, r + 2), "(%d, %d)" % (c + 1, r + 1), "(%d)" % (c * 10 + r), "(%d, %d)" % (c, r + 1)],
                       "数对先写列、再写行：<b>(%d, %d)</b>。" % (c, r))
        if k == "same_row":
            c2 = R.choice([x for x in range(1, 9) if x != c])
            return mcq("%s的位置是 (%d, %d)，和他坐在同一行的同学的位置可能是哪一个？" % (n, c, r), "(%d, %d)" % (c2, r),
                       ["(%d, %d)" % (c, R.choice([x for x in range(1, 8) if x != r])), "(%d, %d)" % (r, c2) if r != c2 else "(%d, %d)" % (c2, r + 1), "(%d, %d)" % (c2 + 1, r + 1)],
                       "同一行，第二个数（行）相同：<b>(%d, %d)</b>。" % (c2, r))
        if k == "same_col":
            r2 = R.choice([x for x in range(1, 8) if x != r])
            return mcq("%s的位置是 (%d, %d)，和他坐在同一列的同学的位置可能是哪一个？" % (n, c, r), "(%d, %d)" % (c, r2),
                       ["(%d, %d)" % (R.choice([x for x in range(1, 9) if x != c]), r), "(%d, %d)" % (r2, c) if r2 != c else "(%d, %d)" % (c + 1, r2), "(%d, %d)" % (c + 1, r2 + 1)],
                       "同一列，第一个数（列）相同：<b>(%d, %d)</b>。" % (c, r2))
        dc, dr = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (0, 2)])
        if not (1 <= c + dc <= 8 and 1 <= r + dr <= 7):
            return None
        d = {(1, 0): "向右平移 1 格", (-1, 0): "向左平移 1 格", (0, 1): "向上平移 1 格", (0, -1): "向下平移 1 格", (2, 0): "向右平移 2 格", (0, 2): "向上平移 2 格"}[(dc, dr)]
        return mcq("点 (%d, %d) %s后，用数对表示是什么？" % (c, r, d), "(%d, %d)" % (c + dc, r + dr),
                   ["(%d, %d)" % (c - dc, r - dr), "(%d, %d)" % (c + dr, r + dc), "(%d, %d)" % (c, r)],
                   "左右平移改变列（第一个数），上下平移改变行（第二个数）：<b>(%d, %d)</b>。" % (c + dc, r + dr))
    return mk


def pair_shape():
    def mk():
        x1, y1 = R.randint(1, 3), R.randint(1, 2)
        w, h = R.randint(2, 4), R.randint(2, 3)
        pts = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
        miss = R.randint(0, 3)
        given = [p for i, p in enumerate(pts) if i != miss]
        a = pts[miss]
        return mcq("长方形的三个顶点是 %s，第四个顶点用数对表示是什么？" % "、".join("(%d, %d)" % p for p in given), "(%d, %d)" % a,
                   ["(%d, %d)" % (a[1], a[0]) if a[0] != a[1] else "(%d, %d)" % (a[0] + 1, a[1]), "(%d, %d)" % (a[0] + 1, a[1] + 1), "(%d, %d)" % (a[0], a[1] + 1)],
                   "长方形对边平行：第四个顶点的列和行分别和相邻顶点相同，是 <b>(%d, %d)</b>。" % a)
    return mk


# ------------------------------------------------------------------ 方向和距离（六年级上）
PLACES = ["学校", "图书馆", "公园", "医院", "超市", "邮局", "书店", "体育馆", "少年宫", "电影院", "火车站", "博物馆"]


def bearing_svg(center, place, base, side, deg, dist, unit_len, unit="千米"):
    """base: 北/南, side: 东/西。北が上"""
    W = H = 300
    cx, cy = 150, 150
    s = ["<line x1='%d' y1='30' x2='%d' y2='270' stroke='#999' stroke-dasharray='4 4'/>" % (cx, cx),
         "<line x1='30' y1='%d' x2='270' y2='%d' stroke='#999' stroke-dasharray='4 4'/>" % (cy, cy),
         "<polygon points='%d,18 %d,32 %d,32' fill='%s'/>" % (cx, cx - 6, cx + 6, INK), text(cx + 14, 30, "北", 14)]
    a = math.radians(deg)
    sx = 1 if side == "东" else -1
    sy = -1 if base == "北" else 1
    L = dist / unit_len * 40
    x, y = cx + sx * L * math.sin(a), cy + sy * L * math.cos(a)
    s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (cx, cy, x, y, BLUE))
    n = int(round(dist / unit_len))
    for i in range(1, n):
        tx, ty = cx + sx * 40 * i * math.sin(a), cy + sy * 40 * i * math.cos(a)
        nx, ny = math.cos(a) * 6, math.sin(a) * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (tx - nx * sy * -1, ty - ny * sx, tx + nx * sy * -1, ty + ny * sx, BLUE))
    s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (cx, cy, INK))
    s.append(text(cx + (-28 if sx > 0 else 28), cy + (18 if sy < 0 else -10), center, 13))
    s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x, y, RED))
    s.append(text(x + sx * 4, y + sy * 14, place, 13, anchor="start" if sx > 0 else "end"))
    ar = 34
    s.append("<path d='M%d %d A%d %d 0 0 %d %.1f %.1f' fill='none' stroke='%s' stroke-width='1.5'/>" % (
        cx, cy + sy * ar, ar, ar, 1 if (sx > 0) == (sy < 0) else 0, cx + sx * ar * math.sin(a), cy + sy * ar * math.cos(a), RED))
    s.append(text(cx + sx * (ar + 16) * math.sin(a / 2), cy + sy * (ar + 16) * math.cos(a / 2) + 5, "%d°" % deg, 12, col=RED))
    s.append("<line x1='200' y1='285' x2='240' y2='285' stroke='%s' stroke-width='2'/>" % INK)
    s.append("<line x1='200' y1='280' x2='200' y2='290' stroke='%s' stroke-width='2'/><line x1='240' y1='280' x2='240' y2='290' stroke='%s' stroke-width='2'/>" % (INK, INK))
    s.append(text(220, 278, "%s %s" % (fmt(unit_len), unit), 12))
    return fig(svg_wrap(W, H + 4, "".join(s), "%s和%s的方向与距离" % (center, place)))


def dir_dist():
    def mk():
        base, side = R.choice(["北", "南"]), R.choice(["东", "西"])
        deg = R.choice([20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
        unit_len = R.choice([0.5, 1, 2, 100, 200])
        k = R.randint(2, 5)
        dist = unit_len * k
        unit = "米" if unit_len >= 100 else "千米"
        c, p = R.sample(PLACES, 2)
        pic = bearing_svg(c, p, base, side, deg, dist, unit_len, unit)
        ok = "%s偏%s %d° 方向 %s %s处" % (base, side, deg, fmt(dist), unit)
        w = ["%s偏%s %d° 方向 %s %s处" % (side, base, deg, fmt(dist), unit),
             "%s偏%s %d° 方向 %s %s处" % (base, side, 90 - deg, fmt(dist), unit) if deg != 45 else "%s偏%s %d° 方向 %s %s处" % ("南" if base == "北" else "北", side, deg, fmt(dist), unit),
             "%s偏%s %d° 方向 %s %s处" % (base, side, deg, fmt(unit_len * (k + 1)), unit)]
        return mcq("%s在%s的什么位置？（线段上每一小段表示实际距离 %s %s）%s" % (p, c, fmt(unit_len), unit, pic), ok, w,
                   "以%s为观测点，从%s方向往%s转 %d°，线段有 %d 小段，实际距离是 %s × %d ＝ %s %s。所以是<b>%s</b>。" % (
                       c, base, side, deg, k, fmt(unit_len), k, fmt(dist), unit, ok))
    return mk


def dir_opposite():
    OPP = {"北": "南", "南": "北", "东": "西", "西": "东"}

    def mk():
        a, b = R.sample(PLACES, 2)
        base, side = R.choice(["北", "南"]), R.choice(["东", "西"])
        deg = R.choice([15, 20, 30, 35, 40, 50, 60, 70])
        d = R.choice([300, 500, 800, 1200, 2, 3, 5])
        u = "米" if d >= 100 else "千米"
        ok = "%s偏%s %d° 方向 %d %s处" % (OPP[base], OPP[side], deg, d, u)
        return mcq("%s在%s的%s偏%s %d° 方向 %d %s处，那么%s在%s的什么位置？" % (b, a, base, side, deg, d, u, a, b), ok,
                   ["%s偏%s %d° 方向 %d %s处" % (base, side, deg, d, u), "%s偏%s %d° 方向 %d %s处" % (OPP[base], OPP[side], 90 - deg, d, u) if deg != 45 else "%s偏%s %d° 方向 %d %s处" % (OPP[base], side, deg, d, u),
                    "%s偏%s %d° 方向 %d %s处" % (OPP[base], side, deg, d, u)],
                   "位置是相对的：方向相反（%s变%s，%s变%s），角度和距离不变。<b>%s</b>" % (base, OPP[base], side, OPP[side], ok))
    return mk


def dir_route2():
    def mk():
        a, b, c = R.sample(PLACES, 3)
        d1, d2 = R.choice([200, 300, 400, 500, 600]), R.choice([150, 250, 350, 450])
        g1, g2 = R.choice(["北偏东 30°", "东偏南 40°", "南偏西 25°", "西偏北 50°", "北偏西 45°"]), R.choice(["正东", "正北", "东偏北 20°", "南偏东 60°"])
        speed = R.choice([50, 60, 70, 80])
        t = (d1 + d2) / speed
        if t != int(t):
            return None
        q = "%s从%s出发，先向%s方向走 %d 米到%s，再向%s方向走 %d 米到%s。他每分钟走 %d 米，一共要走多少分钟？" % (NM.next(), a, g1, d1, b, g2, d2, c, speed)
        return mcq(q, "%d 分钟" % t, ["%d 分钟" % x for x in (d1 // speed if d1 % speed == 0 else t + 1, t + 2, (d1 + d2) // 10, t - 1) if x > 0 and x != t],
                   "路程：%d ＋ %d ＝ %d（米），时间：%d ÷ %d ＝ <b>%d 分钟</b>。" % (d1, d2, d1 + d2, d1 + d2, speed, t))
    return mk


# ------------------------------------------------------------------ 税率和利率（六年级下）
def tax():
    def mk():
        k = R.choice(["tax", "interest", "interest", "cheng", "zhe"])
        if k == "tax":
            inc = R.choice([5000, 8000, 12000, 20000, 30000, 50000])
            r = R.choice([3, 5, 6, 10, 13])
            t = inc * r // 100
            return mcq("一家商店上个月的营业额是 %d 元，按营业额的 %d%% 缴纳税款。应缴纳税款多少元？" % (inc, r), "%d 元" % t,
                       ["%d 元" % x for x in (inc - t, t * 10, inc * r // 10, t + r)],
                       "应纳税额 ＝ 收入 × 税率：%d × %d%% ＝ <b>%d 元</b>。" % (inc, r, t))
        if k == "interest":
            p = R.choice([1000, 2000, 5000, 10000, 20000, 3000])
            r = R.choice([1.5, 1.75, 2, 2.25, 2.5, 2.75, 3])
            y = R.randint(1, 5)
            i = p * r * y / 100
            if i != round(i, 2):
                return None
            want = R.random() < 0.5
            ans = i + p if want else i
            return mcq("%s把 %d 元存入银行，定期 %d 年，年利率是 %s%%。到期时可以得到利息多少元？%s" % (NM.next(), p, y, fmt(r), "连本带息一共多少元？" if want else ""),
                       "%s 元" % fmt(ans), ["%s 元" % fmt(x) for x in (p * r / 100 if y > 1 else i * 2, i if want else i + p, p * r * y, ans + 10) if x != ans],
                       "利息 ＝ 本金 × 利率 × 存期：%d × %s%% × %d ＝ %s（元）%s。<b>%s 元</b>" % (p, fmt(r), y, fmt(i), "，本息 %d ＋ %s ＝ %s" % (p, fmt(i), fmt(i + p)) if want else "", fmt(ans)))
        if k == "cheng":
            last = R.choice([200, 300, 400, 500, 600, 800])
            c = R.randint(1, 3)
            ans = last * (10 + c) // 10
            return mcq("去年某村收小麦 %d 吨，今年比去年增产%s成。今年收小麦多少吨？" % (last, "一二三"[c - 1]), "%d 吨" % ans,
                       ["%d 吨" % x for x in (last * c // 10, last * (10 - c) // 10, last + c, ans + 10)],
                       "%s成就是 %d0%%，今年是去年的 1%d0%%：%d × %s ＝ <b>%d 吨</b>。" % ("一二三"[c - 1], c, c, last, fmt(1 + c / 10), ans))
        p = R.choice([80, 120, 150, 200, 240, 300, 360, 500])
        z = R.choice([6, 7, 8, 9, 7.5, 8.5])
        ans = p * z / 10
        if ans != int(ans):
            return None
        return mcq("一件商品原价 %d 元，现在打%s折出售。现价多少元？" % (p, fmt(z)), "%d 元" % ans,
                   ["%d 元" % x for x in (p - ans, p * z // 100 if p * z // 100 else 1, ans + 10, p)],
                   "打%s折就是按原价的 %s%% 出售：%d × %s%% ＝ <b>%d 元</b>。" % (fmt(z), fmt(z * 10), p, fmt(z * 10), ans))
    return mk


# ------------------------------------------------------------------ 圆柱与圆锥（六年级下）
def cyl_cone(kinds=("cone_v", "cone_v", "lat", "cyl_s", "rel", "rel2")):
    def mk():
        k = R.choice(kinds)
        r = R.choice([1, 2, 3, 4, 5, 6, 10])
        h = R.choice([3, 6, 9, 12, 15, 18, 21])
        if k == "cone_d":
            d = 2 * r
            v = 3.14 * r * r * h / 3
            return mcq("一个圆锥形沙堆，底面直径是 %d 米，高 %d 米。这堆沙的体积是多少立方米？（π 取 3.14）" % (d, h), "%s 立方米" % fmt(v),
                       ["%s 立方米" % fmt(x) for x in (3.14 * d * d * h / 3, 3.14 * r * r * h, 3.14 * d * h / 3, v + 3.14)],
                       "先求半径：%d ÷ 2 ＝ %d（米），体积：1/3 × 3.14 × %d² × %d ＝ <b>%s 立方米</b>。" % (d, r, r, h, fmt(v)))
        if k == "same_v":
            hc = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
            return mcq("一个圆柱和一个圆锥的底面积相等，体积也相等。圆柱的高是 %d 厘米，圆锥的高是多少厘米？" % hc, "%d 厘米" % (hc * 3),
                       ["%d 厘米" % x for x in (hc, hc * 2, hc + 3, hc * 3 + 1)],
                       "体积和底面积都相等时，圆锥的高是圆柱的 3 倍：%d × 3 ＝ <b>%d 厘米</b>。" % (hc, hc * 3))
        if k == "cone_v":
            v = 3.14 * r * r * h / 3
            return mcq("一个圆锥的底面半径是 %d 厘米，高 %d 厘米。它的体积是多少立方厘米？（π 取 3.14）" % (r, h), "%s 立方厘米" % fmt(v),
                       ["%s 立方厘米" % fmt(x) for x in (3.14 * r * r * h, 3.14 * 2 * r * h / 3, 3.14 * r * h / 3, v + 3.14)],
                       "圆锥体积 ＝ 1/3 × 底面积 × 高：1/3 × 3.14 × %d² × %d ＝ <b>%s 立方厘米</b>。" % (r, h, fmt(v)))
        if k == "lat":
            d = r * 2
            s = 3.14 * d * h
            return mcq("一个圆柱的底面直径是 %d 厘米，高 %d 厘米。它的侧面积是多少平方厘米？（π 取 3.14）" % (d, h), "%s 平方厘米" % fmt(s),
                       ["%s 平方厘米" % fmt(x) for x in (3.14 * r * h, 3.14 * r * r * h, s + 2 * 3.14 * r * r, 3.14 * d * h * 2)],
                       "侧面积 ＝ 底面周长 × 高：3.14 × %d × %d ＝ <b>%s 平方厘米</b>。" % (d, h, fmt(s)))
        if k == "cyl_s":
            s = 2 * 3.14 * r * h + 2 * 3.14 * r * r
            return mcq("一个圆柱的底面半径是 %d 分米，高 %d 分米。它的表面积是多少平方分米？（π 取 3.14）" % (r, h), "%s 平方分米" % fmt(s),
                       ["%s 平方分米" % fmt(x) for x in (2 * 3.14 * r * h, 2 * 3.14 * r * h + 3.14 * r * r, 3.14 * r * r * h, s + 1)],
                       "表面积 ＝ 侧面积 ＋ 2 个底面积：2 × 3.14 × %d × %d ＋ 2 × 3.14 × %d² ＝ <b>%s 平方分米</b>。" % (r, h, r, fmt(s)))
        if k == "rel":
            v = 3 * R.randint(3, 40)
            return mcq("一个圆柱和一个圆锥等底等高，圆柱的体积是 %d 立方分米。圆锥的体积是多少立方分米？" % v, "%d 立方分米" % (v // 3) if v % 3 == 0 else None,
                       ["%d 立方分米" % x for x in (v * 3, v, v // 2 if v % 2 == 0 else v + 3, v - 3)],
                       "等底等高的圆锥体积是圆柱的 1/3：%d ÷ 3 ＝ <b>%d 立方分米</b>。" % (v, v // 3))
        v = R.randint(4, 40)
        return mcq("一个圆锥和一个圆柱等底等高，圆锥的体积是 %d 立方厘米。圆柱的体积是多少立方厘米？" % v, "%d 立方厘米" % (v * 3),
                   ["%d 立方厘米" % x for x in (v // 3 if v % 3 == 0 else v + 2, v, v * 2, v * 3 + 3)],
                   "圆柱的体积是等底等高圆锥的 3 倍：%d × 3 ＝ <b>%d 立方厘米</b>。" % (v, v * 3))
    return mk


# ------------------------------------------------------------------ 鸽巢问题（六年级下）
def pigeon(kinds=("basic", "basic", "least", "color", "draw")):
    def mk():
        k = R.choice(kinds)
        if k == "basic":
            n = R.randint(3, 9)
            m = n * R.randint(1, 4) + R.randint(1, n - 1)
            a = -(-m // n)
            return mcq("把 %d 支铅笔放进 %d 个笔筒里，总有一个笔筒里至少放进几支铅笔？" % (m, n), "%d 支" % a,
                       ["%d 支" % x for x in (m // n, a + 1, m - n, n) if x > 0 and x != a],
                       "%d ÷ %d ＝ %d……%d，至少数 ＝ 商 ＋ 1 ＝ <b>%d 支</b>。" % (m, n, m // n, m % n, a))
        if k == "least":
            n = R.randint(3, 12)
            t = R.randint(2, 5)
            m = n * (t - 1) + 1
            return mcq("有 %d 个抽屉，要保证总有一个抽屉里至少放 %d 个苹果，至少要放多少个苹果？" % (n, t), "%d 个" % m,
                       ["%d 个" % x for x in (n * t, n * (t - 1), n + t, m + 1) if x != m],
                       "先每个抽屉放 %d 个（共 %d 个），再放 1 个就一定有抽屉达到 %d 个：<b>%d 个</b>。" % (t - 1, n * (t - 1), t, m))
        if k == "color2":
            c = R.randint(2, 7)
            t = R.randint(3, 6)
            ans = c * (t - 1) + 1
            return mcq("盒子里有大小相同的 %d 种颜色的球，每种都有很多。至少摸出几个，才能保证有 %d 个同色？" % (c, t), "%d 个" % ans,
                       ["%d 个" % x for x in (c * t, c + t, c * (t - 1), ans + 1) if x != ans],
                       "最坏的情况：每种颜色各摸 %d 个，共 %d 个；再摸 1 个就一定有 %d 个同色：<b>%d 个</b>。" % (t - 1, c * (t - 1), t, ans))
        if k == "socks":
            c = R.randint(2, 6)
            col = "、".join(["红", "黄", "蓝", "白", "黑", "绿"][:c])
            return mcq("抽屉里有%s %d 种颜色的袜子各 10 只，黑暗中至少要拿出几只，才能保证有一双同色的？" % (col, c), "%d 只" % (c + 1),
                       ["%d 只" % x for x in (c, 2, c * 2, 11) if x != c + 1],
                       "最坏的情况是先拿出 %d 只颜色都不同，再拿 1 只一定能配成一双：<b>%d 只</b>。" % (c, c + 1))
        if k == "color":
            c = R.randint(2, 5)
            return mcq("盒子里有大小相同的 %d 种颜色的球，每种都有很多。至少摸出几个，才能保证有 2 个同色？" % c, "%d 个" % (c + 1),
                       ["%d 个" % x for x in (c, 2, c * 2, c + 2) if x != c + 1],
                       "最坏的情况是先摸出 %d 个颜色都不同的，再摸 1 个一定同色：<b>%d 个</b>。" % (c, c + 1))
        p = R.randint(13, 40)
        return mcq("一个班有 %d 名学生，至少有几名学生的生日在同一个月？" % p, "%d 名" % (-(-p // 12)),
                   ["%d 名" % x for x in (p // 12, -(-p // 12) + 1, 12, 1 if p // 12 > 1 else 3) if x != -(-p // 12)],
                   "一年 12 个月，%d ÷ 12 ＝ %d……%d，至少 <b>%d 名</b>。" % (p, p // 12, p % 12, -(-p // 12)))
    return mk


# ------------------------------------------------------------------ 解方程（五年级上、正の数だけ）
def eqn(kind):
    def mk():
        x = R.randint(2, 30)
        a = R.randint(2, 9)
        b = R.randint(2, 40)
        if kind == "add":
            q, c = "x ＋ %d ＝ %d" % (b, x + b), "等式两边同时减去 %d" % b
            w = [x + 2 * b, x + 1, b]
        elif kind == "sub":
            q, c = "x － %d ＝ %d" % (b, x), "等式两边同时加上 %d" % b
            x, q = x + b, "x － %d ＝ %d" % (b, x)
            w = [x - 2 * b if x > 2 * b else x + b, x - b, x + 1]
        elif kind == "mul":
            q, c = "%dx ＝ %d" % (a, a * x), "等式两边同时除以 %d" % a
            w = [a * x * a, a * x - a, x + 1]
        elif kind == "two":
            q, c = "%dx ＋ %d ＝ %d" % (a, b, a * x + b), "先两边同时减去 %d，再同时除以 %d" % (b, a)
            w = [(a * x + 2 * b) // a, a * x, x + 1]
        else:
            q, c = "%d(x － %d) ＝ %d" % (a, b // 4 + 1, a * x), "先两边同时除以 %d，再同时加上 %d" % (a, b // 4 + 1)
            x = x + b // 4 + 1
            q = "%d(x － %d) ＝ %d" % (a, b // 4 + 1, a * (x - b // 4 - 1))
            w = [x - 2 * (b // 4 + 1), x - b // 4 - 1, x + 1]
        return mcq("解方程：%s，x ＝ ？" % q, str(x), [str(v) for v in w if v > 0 and v != x],
                   "%s，得 <b>x ＝ %d</b>。检验：把 %d 代入原方程，左右相等。" % (c, x, x))
    return mk


def eqn_story():
    def mk():
        n = NM.next()
        k = R.choice(range(4))
        x = R.randint(5, 60)
        if k == 0:
            a = R.randint(2, 5)
            q = "%s今年 %d 岁，正好是妹妹年龄的 %d 倍多 2 岁。设妹妹 x 岁，哪个方程正确？" % (n, a * x + 2, a)
            ok, w = "%dx ＋ 2 ＝ %d" % (a, a * x + 2), ["%dx － 2 ＝ %d" % (a, a * x + 2), "%d ＋ 2x ＝ %d" % (a, a * x + 2), "x ＋ %d ＝ %d" % (a, a * x + 2)]
            e = "“%d 倍多 2”：妹妹年龄 × %d ＋ 2 ＝ %s的年龄。" % (a, a, n)
        elif k == 1:
            p = R.randint(3, 15)
            m = R.randint(2, 8)
            q = "买 %d 支钢笔共付了 %d 元。设每支钢笔 x 元，哪个方程正确？" % (m, m * p)
            ok, w = "%dx ＝ %d" % (m, m * p), ["x ＋ %d ＝ %d" % (m, m * p), "%dx ＝ %d" % (m * p, m), "x － %d ＝ %d" % (m, m * p)]
            e = "单价 × 数量 ＝ 总价。"
        elif k == 2:
            a, b = R.randint(20, 60), R.randint(5, 30)
            q = "一桶油用去 %d 千克后，还剩 %d 千克。设这桶油原来有 x 千克，哪个方程正确？" % (b, a)
            ok, w = "x － %d ＝ %d" % (b, a), ["x ＋ %d ＝ %d" % (b, a), "%d － x ＝ %d" % (b, a), "%dx ＝ %d" % (b, a)]
            e = "原有 － 用去 ＝ 剩下。"
        else:
            l = R.randint(5, 20)
            s = R.randint(30, 90)
            q = "一个长方形的周长是 %d 厘米，长是 %d 厘米。设宽是 x 厘米，哪个方程正确？" % (2 * (l + s // 2), l)
            ok, w = "2(%d ＋ x) ＝ %d" % (l, 2 * (l + s // 2)), ["%d ＋ x ＝ %d" % (l, 2 * (l + s // 2)), "%dx ＝ %d" % (l, 2 * (l + s // 2)), "2 × %d ＋ x ＝ %d" % (l, 2 * (l + s // 2))]
            e = "长方形周长 ＝（长 ＋ 宽）× 2。"
        return mcq(q, ok, w, e + "所以是 <b>%s</b>。" % ok)
    return mk
