# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：二元一次方程式的圖形（108課綱 A-7-6）
  python3 tools/gen_tw_math_g7_graphs_of_linear_equations.py
ax＋by＝c の圖形は直線、點が直線上にあるか、x 軸・y 軸との交點、y＝c（水平線）・x＝c（鉛垂線）、聯立方程式の解＝兩直線の交點。
誤答：y＝3 を鉛垂線とする、x 軸との交點で x＝0 とおく、交點の坐標を (y, x) と讀む。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, par, tidy_sets, term
from tw_g7_grid import plane

R = random.Random(71018)
NM = Names(R)


def P(x, y):
    return "（%s, %s）" % (sn(x), sn(y))


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def eq2(a, b, c):
    return "%s%s ＝ %s" % (term(a, "x", True), term(b, "y"), sn(c))


def seg(a, b, c, n=6):
    """ax+by=c を枠 [-n, n] で切った線分"""
    pts = []
    for x in (-n, n):
        if b:
            y = F(c - a * x, b)
            if -n <= y <= n:
                pts.append((x, y))
    for y in (-n, n):
        if a:
            x = F(c - b * y, a)
            if -n <= x <= n:
                pts.append((x, y))
    pts = sorted(set(pts))
    return (pts[0], pts[-1]) if len(pts) >= 2 else None


def s1(seen):
    def mk():
        a, b = nz(-4, 4), nz(-4, 4)
        x, y = nz(-5, 5), nz(-5, 5)
        c = a * x + b * y
        q = "下面哪一個點在直線 %s 上？" % eq2(a, b, c)
        cands = [(y, x), (-x, y), (x, -y), (x + 1, y)]
        w = [P(u, v) for u, v in cands if a * u + b * v != c][:3]
        return mcq(q, P(x, y), w, "代入 x ＝ %s、y ＝ %s：%s × %s ＋ %s × %s ＝ %s，等式成立，點在直線上。" % (sn(x), sn(y), par(a), par(x), par(b), par(y), sn(c)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = nz(-6, 6), nz(-6, 6)
        k1, k2 = nz(-6, 6), nz(-6, 6)
        c = a * k1
        if c != b * k2:
            return None
        ask = R.choice(["x", "y"])
        q = "直線 %s 和 %s 軸的交點是？" % (eq2(a, b, c), ask)
        ans = P(k1, 0) if ask == "x" else P(0, k2)
        w = [P(0, k1), P(k2, 0), P(0, k2) if ask == "x" else P(k1, 0)]
        e = ("和 x 軸的交點 y ＝ 0：%s ＝ %s，x ＝ %s。" % (term(a, "x", True), sn(c), sn(k1))) if ask == "x" else ("和 y 軸的交點 x ＝ 0：%s ＝ %s，y ＝ %s。" % (term(b, "y", True), sn(c), sn(k2)))
        return mcq(q, ans, [t for t in w if t != ans] + [P(-k1, 0) if ask == "x" else P(0, -k2)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = nz(-5, 5)
        typ = R.choice(["h", "v"])
        if typ == "h":
            g = plane(6, [], [((-6, k), (6, k), "#3f7fbf")])
            ans = "y ＝ %s" % sn(k)
            w = ["x ＝ %s" % sn(k), "y ＝ %s" % sn(-k), "x ＋ y ＝ %s" % sn(k)]
            e = "水平線上每一點的 y 坐標都是 %s：y ＝ %s。" % (sn(k), sn(k))
        else:
            g = plane(6, [], [((k, -6), (k, 6), "#3f7fbf")])
            ans = "x ＝ %s" % sn(k)
            w = ["y ＝ %s" % sn(k), "x ＝ %s" % sn(-k), "x － y ＝ %s" % sn(k)]
            e = "鉛垂線上每一點的 x 坐標都是 %s：x ＝ %s。" % (sn(k), sn(k))
        return mcq("圖中藍色直線的方程式是哪一個？" + g, ans, w, e)

    def word():
        k = nz(-8, 8)
        typ = R.choice(["h", "v"])
        if typ == "h":
            q = "y ＝ %s 的圖形是什麼樣子？" % sn(k)
            ans = "通過（0, %s）的水平線" % sn(k)
            w = ["通過（%s, 0）的鉛垂線" % sn(k), "通過原點的斜線", "通過（%s, 0）的水平線" % sn(k)]
        else:
            q = "x ＝ %s 的圖形是什麼樣子？" % sn(k)
            ans = "通過（%s, 0）的鉛垂線" % sn(k)
            w = ["通過（0, %s）的水平線" % sn(k), "通過原點的斜線", "通過（0, %s）的鉛垂線" % sn(k)]
        return mcq(q, ans, w, "y ＝ c 是水平線（和 x 軸平行），x ＝ c 是鉛垂線（和 y 軸平行）。")
    return pick_unique(R, mk, 12, seen) + pick_unique(R, word, 8, seen)


def s4(seen):
    def mk():
        x, y = nz(-4, 4), nz(-4, 4)
        a1, b1, a2, b2 = nz(-3, 3), nz(-3, 3), nz(-3, 3), nz(-3, 3)
        if a1 * b2 == a2 * b1:
            return None
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        s1_, s2_ = seg(a1, b1, c1), seg(a2, b2, c2)
        if not s1_ or not s2_:
            return None
        g = plane(6, [(x, y, "P")], [(s1_[0], s1_[1], "#3f7fbf"), (s2_[0], s2_[1], "#2e7d4f")])
        q = "圖中兩條直線是 %s 和 %s，交點 P 就是聯立方程式的解。解是哪一個？" % (eq2(a1, b1, c1), eq2(a2, b2, c2)) + g
        return mcq(q, "x ＝ %s、y ＝ %s" % (sn(x), sn(y)), ["x ＝ %s、y ＝ %s" % (sn(u), sn(v)) for u, v in ((y, x), (-x, y), (x, -y), (x + 1, y)) if (u, v) != (x, y)][:3],
                   "兩直線的交點同時在兩條線上，坐標%s就是聯立方程式的解。" % P(x, y))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def table():
        a, b = nz(-3, 3), R.choice([1, -1])
        c = nz(-6, 6)
        xs = [-2, 0, 2]
        ys = [F(c - a * x, b) for x in xs]
        q = "直線 %s 上，x ＝ %s、%s、%s 時，y 分別是多少？" % (eq2(a, b, c), sn(xs[0]), sn(xs[1]), sn(xs[2]))
        ans = "、".join(sn(y) for y in ys)
        return mcq(q, ans, ["、".join(sn(-y) for y in ys), "、".join(sn(y) for y in ys[::-1]), "、".join(sn(y + 1) for y in ys)], "把每個 x 代入 %s，解出 y：%s。" % (eq2(a, b, c), ans))

    def which():
        F_ = [("二元一次方程式 ax ＋ by ＝ c 的圖形是什麼？", "一條直線", ["一個點", "一條曲線", "一個圓"], "所有解在坐標平面上排成一條直線。"),
              ("直線 y ＝ 0 是哪一條線？", "x 軸", ["y 軸", "通過原點的斜線", "不存在"], "x 軸上每一點的 y 都是 0。"),
              ("直線 x ＝ 0 是哪一條線？", "y 軸", ["x 軸", "通過原點的斜線", "不存在"], "y 軸上每一點的 x 都是 0。"),
              ("兩條直線只有一個交點時，聯立方程式有幾組解？", "1 組", ["0 組", "2 組", "無限多組"], "交點只有一個，解就只有一組。"),
              ("直線 x ＝ 3 和 y ＝ －2 的交點是？", "（3, －2）", ["（－2, 3）", "（3, 0）", "（0, －2）"], "交點的 x 是 3、y 是 －2。"),
              ("要畫出直線 2x ＋ y ＝ 4，最少要找幾個點？", "2 個", ["1 個", "3 個", "4 個"], "兩點決定一條直線，常用和兩軸的交點（2, 0）、（0, 4）。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, table, 14, seen) + pick_unique(R, which, 6, seen)


def main():
    seen = set()
    sets = [("點在不在直線上", s1(seen)), ("和兩軸的交點", s2(seen)), ("水平線和鉛垂線", s3(seen)),
            ("交點與聯立方程式的解", s4(seen)), ("畫圖形的準備", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["二元一次方程式 ax ＋ by ＝ c 的所有解，在坐標平面上排成一條<b>直線</b>。代入成立的點就在線上。",
         "和 x 軸的交點：令 <b>y ＝ 0</b>；和 y 軸的交點：令 <b>x ＝ 0</b>。兩點就能畫出直線。",
         "<b>y ＝ c 是水平線</b>，<b>x ＝ c 是鉛垂線</b>。",
         "兩直線的<b>交點</b>坐標，就是聯立方程式的解。"],
        [example("2x ＋ 3y ＝ 6 和兩軸的交點？", ["y ＝ 0：x ＝ 3。", "x ＝ 0：y ＝ 2。"], "（3, 0）和（0, 2）"),
         example("x ＝ －2 和 y ＝ 4 的交點？", ["x 是 －2、y 是 4。"], "（－2, 4）")],
        [("y ＝ 3 是鉛垂線", "y ＝ 3 是水平線，和 x 軸平行"),
         ("和 x 軸的交點令 x ＝ 0", "x 軸上 y ＝ 0"),
         ("交點（2, －1）寫成 x ＝ －1、y ＝ 2", "先 x 後 y：x ＝ 2、y ＝ －1")])
    faq = [{"q": "怎麼畫二元一次方程式的圖形？",
            "a": "找兩個解（常用和兩軸的交點），在坐標平面上描出來，再用直線連起來。"},
           {"q": "為什麼交點是聯立方程式的解？",
            "a": "交點同時在兩條直線上，所以它的坐標同時滿足兩個方程式。"},
           {"q": "七年級的方程式圖形要學什麼？",
            "a": "108課綱 A-7-6：ax＋by＝c 的圖形、y＝c（水平線）和 x＝c（鉛垂線）的圖形，聯立方程式的解只處理相交且只有一個交點的情況。"}]
    make_unit(R, "grade-7", "graphs-of-linear-equations", "A-7-6",
              "二元一次聯立方程式的幾何意義：ax+by=c的圖形；y=c的圖形（水平線）；x=c的圖形（鉛垂線）；二元一次聯立方程式的解只處理相交且只有一個交點的情況。",
              "二元一次方程式的圖形",
              "七年級數學 方程式的圖形 練習題｜直線・與兩軸交點・水平線鉛垂線 學習單（附解答）",
              "方程式的圖形",
              "國中七年級數學「二元一次方程式的圖形」免費學習單：判斷點在不在直線上、和兩軸的交點、水平線 y＝c 和鉛垂線 x＝c、兩直線交點與聯立方程式的解。100題線上練習馬上對答案，附可列印解答。",
              "ax ＋ by ＝ c 的圖形是直線",
              "兩直線的交點就是聯立方程式的解。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
