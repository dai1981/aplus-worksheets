# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：體積與立方公分（108課綱 N-4-12、S-4-4）
  python3 tools/gen_tw_math_g4_volume.py
1 立方公分の正方體を数える（長方體・階段状の積み木）、体積の比較、層で数える（長×寬×層數）、積み木の増減。
誤答：見える面だけ数える、見えない下の段を数え忘れる、立方公分と平方公分の取り違え。
"""
import math
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, GREEN

R = random.Random(41014)
NM = Names(R)
A = 22
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
TOP, LEFT, RIGHT = "#d9eedd", "#9fcfaa", "#bfe0c6"


def cubes_svg(cells, label="正方體積木"):
    """cells：(x, y, z) の集合。x は右下、y は左下、z は上"""
    pts = []
    def P(x, y, z):
        return ((x - y) * A * C30, (x + y) * A * S30 - z * A)
    for (x, y, z) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    pts.append(P(x + dx, y + dy, z + dz))
    minx = min(p[0] for p in pts) - 6
    miny = min(p[1] for p in pts) - 6
    W = max(p[0] for p in pts) - minx + 6
    H = max(p[1] for p in pts) - miny + 6
    def Q(x, y, z):
        px, py = P(x, y, z)
        return "%.1f,%.1f" % (px - minx, py - miny)
    s = []
    for (x, y, z) in sorted(cells, key=lambda c: (c[0] + c[1], c[2])):
        top = [Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)]
        right = [Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)]
        left = [Q(x, y + 1, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)]
        for f, col in ((top, TOP), (right, RIGHT), (left, LEFT)):
            s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.3'/>" % (" ".join(f), col, GREEN))
    return fig(svg_wrap(int(W), int(H), "".join(s), label))


def block(w, d, h):
    return [(x, y, z) for x in range(w) for y in range(d) for z in range(h)]


def stairs(hs, depth=1):
    """左から右へ高さ hs の列（奥行き depth）"""
    return [(x, y, z) for x, hh in enumerate(hs) for y in range(depth) for z in range(hh)]


def s1(seen):
    def mk():
        w, d, h = R.randint(2, 5), R.randint(1, 4), R.randint(1, 4)
        if w * d * h < 4:
            return None
        n = w * d * h
        vis = len({(x, y, z) for (x, y, z) in block(w, d, h) if x == w - 1 or y == d - 1 or z == h - 1})
        q = "用 1 立方公分的正方體排成長方體，體積是多少？" + cubes_svg(block(w, d, h))
        return mcq(q, "%d 立方公分" % n, ["%d 立方公分" % x for x in (vis, n + w * d, n - w if n - w > 0 else n + 2, w + d + h, 2 * (w * d + d * h + w * h) if 2 * (w * d + d * h + w * h) != n else n + 3) if x != n] + ["%d 平方公分" % n],
                   "一層有 %d × %d ＝ %d 個，%d 層：%d × %d ＝ %d 個，體積 %d 立方公分。" % (w, d, w * d, h, w * d, h, n, n))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        k = R.randint(3, 5)
        hs = [R.randint(1, 4) for _ in range(k)]
        dep = R.choice([1, 1, 2])
        cells = stairs(hs, dep)
        n = len(cells)
        tops = len(hs) * dep
        q = "這堆積木有幾個 1 立方公分的正方體？（看不到的下面也有積木）" + cubes_svg(cells)
        return mcq(q, "%d 個" % n, ["%d 個" % x for x in (tops, sum(hs), n + dep, n - 1, max(hs) * k * dep) if x != n],
                   "一行一行數：%s，%s。" % ("＋".join(str(h * dep) for h in hs), "共 %d 個" % n))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = (R.randint(2, 4), R.randint(1, 3), R.randint(1, 3))
        b = (R.randint(2, 4), R.randint(1, 3), R.randint(1, 3))
        va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
        if va == vb or abs(va - vb) > 12:
            return None
        L = "甲" if va > vb else "乙"
        q = "甲、乙兩個長方體都是用 1 立方公分的正方體排成的，哪一個體積比較大？大多少？<p>甲</p>%s<p>乙</p>%s" % (cubes_svg(block(*a), "甲"), cubes_svg(block(*b), "乙"))
        d = abs(va - vb)
        return mcq(q, "%s，大 %d 立方公分" % (L, d), ["%s，大 %d 立方公分" % ("乙" if L == "甲" else "甲", d), "%s，大 %d 立方公分" % (L, d + 1), "一樣大"],
                   "甲 %d × %d × %d ＝ %d，乙 %d × %d × %d ＝ %d，相差 %d 立方公分。" % (a[0], a[1], a[2], va, b[0], b[1], b[2], vb, d))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    FACTS = [("邊長 1 公分的正方體，體積是多少？", "1 立方公分", ["1 平方公分", "1 公分", "6 立方公分"], "邊長 1 公分的正方體，體積是 1 立方公分。"),
             ("「立方公分」是用來量什麼的單位？", "體積（物體佔空間的大小）", ["長度", "面積", "重量"], "公分量長度，平方公分量面積，立方公分量體積。"),
             ("一顆骰子大約是邊長 1.5 公分的正方體，它的體積大約是？", "3 立方公分", ["3 平方公分", "30 立方公分", "300 立方公分"], "1.5 × 1.5 × 1.5 ≈ 3.4，大約 3 立方公分。"),
             ("兩個形狀不同的積木，都用 12 個 1 立方公分的正方體拼成，它們的體積怎樣？", "一樣大", ["形狀高的比較大", "形狀長的比較大", "不能比較"], "都是 12 個 1 立方公分，體積都是 12 立方公分。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def layer():
        w, d, h = R.randint(2, 9), R.randint(2, 6), R.randint(2, 8)
        q = "一個長方體盒子，底層排了 %d 排、每排 %d 個 1 立方公分的正方體，一共排了 %d 層，體積是多少？" % (d, w, h)
        n = w * d * h
        return mcq(q, "%d 立方公分" % n, ["%d 立方公分" % x for x in (w * d + h, w + d + h, w * d * (h - 1), n + w * d) if x != n],
                   "一層 %d × %d ＝ %d 個，%d 層 × %d ＝ %d 個，體積 %d 立方公分。" % (d, w, w * d, w * d, h, n, n))
    return out + pick_unique(R, layer, 16, seen)


def s5(seen):
    def add():
        w, d, h = R.randint(2, 5), R.randint(2, 4), R.randint(2, 4)
        k = R.randint(1, 3)
        who = NM.next()
        n = w * d * h
        q = "%s用 1 立方公分的正方體排成每層 %d 個、%d 層的長方體，又往上加了 %d 層。現在體積是多少？" % (who, w * d, h, k)
        v = w * d * (h + k)
        return mcq(q, "%d 立方公分" % v, ["%d 立方公分" % x for x in (n + k, w * d * k, n + w * d, v + w * d) if x != v],
                   "每層 %d 個，共 %d ＋ %d ＝ %d 層：%d × %d ＝ %d（立方公分）。" % (w * d, h, k, h + k, w * d, h + k, v))

    def make_cube():
        n = R.choice([2, 3, 4])
        have = R.randint(n ** 3 // 2, n ** 3 - 1)
        q = "要用 1 立方公分的正方體排成一個長、寬、高都是 %d 公分的大正方體，已經有 %d 個，還要幾個？" % (n, have)
        v = n ** 3 - have
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (n * n - have if n * n > have else v + n, n * 6 - have if n * 6 > have else v + 2, v + 1, n ** 3) if x != v and x > 0],
                   "大正方體要 %d × %d × %d ＝ %d 個，%d － %d ＝ %d（個）。" % (n, n, n, n ** 3, n ** 3, have, v))

    def take():
        w, d, h = R.randint(2, 5), R.randint(2, 4), R.randint(2, 5)
        k = R.randint(1, h - 1)
        n = w * d * h
        q = "一個每層 %d 個、%d 層的長方體積木，拿走最上面 %d 層，剩下的體積是多少？" % (w * d, h, k)
        v = w * d * (h - k)
        return mcq(q, "%d 立方公分" % v, ["%d 立方公分" % x for x in (n - k, w * d * k if w * d * k != v else v + w * d, n, v - 1) if x != v],
                   "剩下 %d － %d ＝ %d 層，%d × %d ＝ %d（立方公分）。" % (h, k, h - k, w * d, h - k, v))
    return pick_unique(R, add, 7, seen) + pick_unique(R, make_cube, 6, seen) + pick_unique(R, take, 7, seen)


def main():
    seen = set()
    sets = [("數長方體的積木", s1(seen)), ("數一堆積木", s2(seen)), ("比較體積", s3(seen)),
            ("立方公分和一層一層數", s4(seen)), ("應用問題", s5(seen))]
    demo = cubes_svg(block(4, 2, 3))
    body = lesson(
        ["<b>體積</b>是物體佔空間的大小。邊長 1 公分的正方體，體積是 <b>1 立方公分</b>。",
         "數體積就是數有幾個 1 立方公分的正方體。長方體可以<b>一層一層數</b>：一層幾個 × 幾層。",
         "堆起來的積木，<b>看不到的下面和後面也有</b>，不能只數看得到的面。"],
        [example("體積是多少？" + demo, ["一層 4 × 2 ＝ 8 個。", "3 層：8 × 3 ＝ 24 個。"], "24 立方公分"),
         example("一層 6 個、5 層的長方體，拿走 2 層，剩多少？", ["剩 3 層。", "6 × 3 ＝ 18。"], "18 立方公分")],
        [("只數看得到的正方體", "下面、後面看不到的也要算"),
         ("體積寫成平方公分", "體積的單位是立方公分"),
         ("長得高的一定比較大", "要數有幾個 1 立方公分才知道")])
    faq = [{"q": "四年級的體積要學什麼？",
            "a": "108課綱 N-4-12、S-4-4：以操作為主，認識體積的意義和 1 立方公分的正方體，能數出正方體堆疊的體積並比較大小。長方體體積公式在五年級學。"},
           {"q": "立方公分、平方公分、公分有什麼不同？",
            "a": "公分量長度（線），平方公分量面積（面），立方公分量體積（立體）。"},
           {"q": "數積木常常漏數，怎麼辦？",
            "a": "一層一層數，或一行一行數：先數最上面看到幾行，每行有幾個，再加起來；也可以用真的積木排排看。"}]
    make_unit(R, "grade-4", "volume", "N-4-12",
              "體積與「立方公分」：以具體操作為主。體積認識基於 1 立方公分之正方體。",
              "體積：立方公分與數積木",
              "四年級數學 體積 練習題｜立方公分・數積木・比較體積 學習單（附解答）",
              "體積（立方公分）",
              "國小四年級數學「體積」免費學習單：認識立方公分、數長方體和一堆積木有幾個正方體、比較體積和一層一層數。100題線上練習馬上對答案，附可列印解答。",
              "數有幾個 1 立方公分的正方體",
              "一層幾個 × 幾層；看不到的下面也要算。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
