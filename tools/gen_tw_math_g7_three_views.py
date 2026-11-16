# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：三視圖（108課綱 S-7-2）
  python3 tools/gen_tw_math_g7_three_views.py
3×3×3 以内・中空なしの積木：前視圖（各列の最高）、上視圖（置いてある位置）、右視圖、上視圖に數字（高さ）から個數・前視圖を求める。
誤答：前視圖で奥の列を足し合わせる、右視圖の左右を逆にする、上視圖に高さを反映させる、見えない積木を數えない。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, INK
from tw_g7 import tidy_sets

R = random.Random(71023)
NM = Names(R)
A = 20
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
TOP, LEFT, RIGHT = "#d9eedd", "#9fcfaa", "#bfe0c6"


def heights():
    """3×3 の高さ h[x][y]（x 右、y 手前）。0〜3、少なくとも 4 個"""
    while True:
        n = R.choice([2, 3])
        m = R.choice([2, 3])
        h = [[R.choice([0, 1, 1, 2, 2, 3]) for _ in range(m)] for _ in range(n)]
        tot = sum(map(sum, h))
        if 4 <= tot <= 14 and all(any(row) for row in h) and all(any(h[x][y] for x in range(n)) for y in range(m)):
            return h


def iso(h):
    cells = [(x, y, z) for x in range(len(h)) for y in range(len(h[0])) for z in range(h[x][y])]

    def P(x, y, z):
        return ((x - y) * A * C30, (x + y) * A * S30 - z * A)
    pts = [P(x + dx, y + dy, z + dz) for (x, y, z) in cells for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    minx, miny = min(p[0] for p in pts) - 6, min(p[1] for p in pts) - 22
    W, H = max(p[0] for p in pts) - minx + 6, max(p[1] for p in pts) - miny + 6

    def Q(x, y, z):
        px, py = P(x, y, z)
        return "%.1f,%.1f" % (px - minx, py - miny)
    s = []
    for (x, y, z) in sorted(cells, key=lambda c: (c[0] + c[1], c[2])):
        for f, col in (([Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], TOP),
                       ([Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)], RIGHT),
                       ([Q(x, y + 1, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], LEFT)):
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(f), col, GREEN))
    # 前・右の矢印ラベル
    fx, fy = P(len(h) / 2, len(h[0]) + 1.2, 0)
    rx, ry = P(len(h) + 1.2, len(h[0]) / 2, 0)
    s.append(text(fx - minx, fy - miny + 4, "前", 12, col=INK))
    s.append(text(rx - minx, ry - miny + 4, "右", 12, col=INK))
    pad = 30
    return int(W) + pad, int(H) + pad, "<g transform='translate(%d,%d)'>%s</g>" % (pad // 2, pad // 2, "".join(s))


def grid(cols_or_cells, w, hgt, ox, oy, sz=13):
    s = []
    for (c, r) in cols_or_cells:
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#bfe0c6' stroke='%s' stroke-width='1.2'/>" % (ox + c * sz, oy + r * sz, sz, sz, GREEN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='#ccc' stroke-width='0.8' stroke-dasharray='2 2'/>" % (ox, oy, w * sz, hgt * sz))
    return "".join(s)


def front(h):
    n, m = len(h), len(h[0])
    cols = [max(h[x][y] for y in range(m)) for x in range(n)]
    return ("F", tuple(cols))


def right(h):
    n, m = len(h), len(h[0])
    cols = [max(h[x][y] for x in range(n)) for y in range(m)][::-1]
    return ("F", tuple(cols))


def top(h):
    n, m = len(h), len(h[0])
    return ("T", tuple(tuple(1 if h[x][y] else 0 for x in range(n)) for y in range(m)))


def cells_of(v):
    kind, data = v
    if kind == "F":
        mh = 3
        return [(c, mh - 1 - z) for c, hh in enumerate(data) for z in range(hh)], len(data), mh
    rows = data
    return [(c, r) for r, row in enumerate(rows) for c, f in enumerate(row) if f], len(rows[0]), len(rows)


def panel(views):
    """4 つの候補を 甲乙丙丁 で並べる"""
    s = []
    x = 6
    for lab, v in zip("甲乙丙丁", views):
        cs, w, hh = cells_of(v)
        s.append(text(x + w * 13 / 2, 12, lab, 12, col=INK))
        s.append(grid(cs, w, hh, x, 18))
        x += w * 13 + 26
    return fig(svg_wrap(x, 18 + 3 * 13 + 6, "".join(s), "甲、乙、丙、丁四個圖").replace("<svg ", "<svg data-pf='lg' ", 1))


def variants(v):
    kind, data = v
    out = []
    if kind == "F":
        d = list(data)
        out.append(("F", tuple(d[::-1])))
        for i in range(len(d)):
            for dd in (1, -1):
                e = list(d)
                e[i] += dd
                if 0 <= e[i] <= 3 and any(e):
                    out.append(("F", tuple(e)))
    else:
        rows = [list(r) for r in data]
        out.append(("T", tuple(tuple(r[::-1]) for r in rows)))
        out.append(("T", tuple(tuple(r) for r in rows[::-1])))
        for r in range(len(rows)):
            for c in range(len(rows[0])):
                e = [list(x) for x in rows]
                e[r][c] = 1 - e[r][c]
                out.append(("T", tuple(tuple(x) for x in e)))
    return [o for o in dict.fromkeys(out) if o != v]


def ask(which):
    def mk():
        h = heights()
        W, H, body = iso(h)
        v = {"前": front, "上": top, "右": right}[which](h)
        wr = variants(v)
        if len(wr) < 3:
            return None
        if which == "右":
            alt = front(h)
            if alt != v and alt not in wr[:2]:
                wr = [alt] + wr
        opts = [v] + R.sample(wr[:6], 3)
        R.shuffle(opts)
        k = opts.index(v)
        L = "甲乙丙丁"
        q = "下面立體的%s視圖是哪一個？" % which + fig(svg_wrap(W, H, body, "積木立體圖")) + panel(opts)
        e = {"前": "從前面看，每一直行只看到最高的那一疊：由左到右高度是 %s。",
             "上": "從上面往下看，只看位置、不看高度；有積木的格子塗色。%s",
             "右": "從右邊看，每一行看到最高的那一疊（左右要以右邊看過去的方向為準）：由左到右高度是 %s。"}[which]
        detail = "、".join(map(str, v[1])) if v[0] == "F" else ""
        return mcq(q, L[k], [x for x in L if x != L[k]], e % detail)
    return mk


def numtop(h):
    n, m = len(h), len(h[0])
    s = []
    sz = 26
    for y in range(m):
        for x in range(n):
            if h[x][y]:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#eaf5ec' stroke='%s' stroke-width='1.4'/>" % (6 + x * sz, 6 + y * sz, sz, sz, GREEN))
                s.append(text(6 + x * sz + sz / 2, 6 + y * sz + sz / 2 + 5, str(h[x][y]), 14, col=INK))
    s.append(text(6 + n * sz / 2, 6 + m * sz + 16, "前", 12, col=INK))
    return fig(svg_wrap(12 + n * sz, 12 + m * sz + 16, "".join(s), "上視圖（數字是該位置積木的層數）"))


def s5(seen):
    def count():
        h = heights()
        tot = sum(map(sum, h))
        g = numtop(h)
        cells = sum(1 for row in h for v in row if v)
        return mcq("上視圖中每一格的數字是那個位置疊的積木個數。一共有幾個積木？" + g, "%d 個" % tot, ["%d 個" % t for t in (cells, tot - 1, tot + 2)  if t != tot] + ["%d 個" % (tot + 1)], "把每一格的數字加起來：%d 個。" % tot)

    def fr():
        h = heights()
        g = numtop(h)
        v = front(h)
        wr = variants(v)
        if len(wr) < 3:
            return None
        opts = [v] + R.sample(wr[:6], 3)
        R.shuffle(opts)
        k = opts.index(v)
        L = "甲乙丙丁"
        return mcq("上視圖中每一格的數字是那個位置疊的積木個數。它的前視圖是哪一個？" + g + panel(opts), L[k], [x for x in L if x != L[k]], "前視圖每一直行取那一行最大的數字：%s。" % "、".join(map(str, v[1])))
    return pick_unique(R, count, 10, seen) + pick_unique(R, fr, 10, seen)


def s4(seen):
    def mk():
        F_ = [("三視圖是指哪三個視圖？", "前視圖、上視圖、左（右）視圖", ["前視圖、後視圖、上視圖", "上視圖、下視圖、側視圖", "正面、斜面、背面"], "常用前視圖、上視圖和左（或右）視圖描述立體。"),
              ("前視圖看到的每一直行高度，是那一行的什麼？", "最高的那一疊", ["所有積木加起來", "最前面那一疊", "最矮的那一疊"], "後面比較高的積木也會被看到，所以取最高的。"),
              ("上視圖能看出積木疊幾層嗎？", "不能，只能看出位置", ["能，顏色深淺表示", "能，看格子大小", "只能看出最高層"], "上視圖只看到每個位置有沒有積木。"),
              ("一個正方體的三視圖都是什麼形狀？", "正方形", ["長方形", "三角形", "圓形"], "從前、上、右看都是正方形。"),
              ("一個圓柱直立放著，上視圖是什麼形狀？", "圓形", ["長方形", "正方形", "三角形"], "從上往下看是圓形底面。"),
              ("一個圓柱直立放著，前視圖是什麼形狀？", "長方形", ["圓形", "三角形", "梯形"], "從前面看是長方形。"),
              ("一個圓錐直立放著，前視圖是什麼形狀？", "三角形", ["圓形", "長方形", "扇形"], "從前面看是三角形。"),
              ("只看上視圖和前視圖，一定能確定積木的個數嗎？", "不一定", ["一定能", "一定不能", "只要積木少就能"], "有些位置的層數可能有不只一種情形。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, mk, 8, seen) + pick_unique(R, ask("右"), 12, seen)


def main():
    seen = set()
    s1 = pick_unique(R, ask("前"), 20, seen)
    s2 = pick_unique(R, ask("上"), 20, seen)
    s3 = pick_unique(R, ask("前"), 6, seen) + pick_unique(R, ask("上"), 6, seen) + pick_unique(R, ask("右"), 8, seen)
    sets = [("前視圖", s1), ("上視圖", s2), ("綜合判斷", s3), ("觀念與右視圖", s4(seen)), ("從上視圖的數字", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>前視圖</b>：從前面看。每一直行只看到<b>最高</b>的那一疊。",
         "<b>上視圖</b>：從上面往下看，只看<b>位置</b>，看不出高度。",
         "<b>左（右）視圖</b>：從左（右）邊看，每一行也是看最高的那一疊；方向以看過去時的左右為準。",
         "上視圖中寫上每一格的層數，就能算出積木總數，也能畫出前視圖和右視圖。"],
        [example("上視圖第一列是 2、1，第二列是 3、1（前面在下），前視圖？", ["左行最高 3，右行最高 1。"], "左 3 層、右 1 層")],
        [("前視圖把前後的積木加起來", "只看最高的那一疊"),
         ("上視圖畫出高度", "上視圖只看位置"),
         ("右視圖的左右和前視圖一樣排", "要站在右邊看，左右會改變")])
    faq = [{"q": "三視圖要怎麼畫？",
            "a": "分別從前面、上面、左（或右）面看立體，把看到的形狀畫成平面圖。前視圖和右視圖每一行畫最高的高度，上視圖畫有積木的位置。"},
           {"q": "怎麼從上視圖算出積木個數？",
            "a": "在上視圖每一格寫上那個位置疊的層數，全部加起來就是積木總數。"},
           {"q": "七年級的三視圖要學什麼？",
            "a": "108課綱 S-7-2：立體圖形的前視圖、上視圖、左（右）視圖，立體圖形限制內嵌於 3×3×3 的正方體且不得中空。"}]
    make_unit(R, "grade-7", "three-views", "S-7-2",
              "三視圖：立體圖形的前視圖、上視圖、左(右)視圖。立體圖形限制內嵌於 3×3×3 的正方體且不得中空。",
              "三視圖：前視圖、上視圖、右視圖",
              "七年級數學 三視圖 練習題｜前視圖・上視圖・右視圖・積木 學習單（附解答）",
              "三視圖",
              "國中七年級數學「三視圖」免費學習單：看積木選出前視圖、上視圖和右視圖，三視圖的觀念，以及從標上層數的上視圖算積木個數、畫前視圖。100題線上練習馬上對答案，附可列印解答。",
              "前視圖、右視圖看最高；上視圖只看位置",
              "上視圖標上層數，就能算出積木個數。",
              body, faq, sets, 23)


if __name__ == "__main__":
    main()
