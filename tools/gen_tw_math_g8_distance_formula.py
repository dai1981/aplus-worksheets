# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：坐標平面上兩點的距離（108課綱 G-8-1）
  python3 tools/gen_tw_math_g8_distance_formula.py
AB＝√((a－c)²＋(b－d)²)、圖から距離（直角三角形を作る）、根式の答え、原點からの距離、三角形の周長・直角の判定、未知坐標。
誤答：差を足すだけ（|a－c|＋|b－d|）、x 差と y 差を取り違える、負數の差の計算ミス、平方せずに開方。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g8 import sn, tidy_sets, rt, simp
from tw_g7 import opv
from tw_g7_grid import plane

R = random.Random(81008)
NM = Names(R)


def P(x, y):
    return "（%s, %s）" % (sn(x), sn(y))


def sq(n):
    return rt(*simp(n))


def dist(dx, dy):
    k, m = simp(dx * dx + dy * dy)
    return rt(k, m)


def s1(seen):
    def mk():
        x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
        dx, dy = R.choice([(3, 4), (4, 3), (6, 8), (8, 6), (5, 12), (12, 5), (3, -4), (-4, 3), (-6, 8), (8, -6), (0, 5), (4, 0)])
        x2, y2 = x1 + dx, y1 + dy
        if max(abs(x2), abs(y2)) > 12:
            return None
        d = dist(dx, dy)
        q = "A%s和 B%s的距離是多少？" % (P(x1, y1), P(x2, y2))
        return mcq(q, d, [str(abs(dx) + abs(dy)), dist(dx + 1, dy), sq(abs(dx) + abs(dy))], "AB ＝ √（%s<sup>2</sup> ＋ %s<sup>2</sup>）＝ √%d ＝ %s。" % (sn(abs(dx)), sn(abs(dy)), dx * dx + dy * dy, d))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        x1, y1 = R.randint(-5, 3), R.randint(-5, 3)
        dx, dy = R.randint(1, 6), R.randint(-6, 6)
        x2, y2 = x1 + dx, y1 + dy
        if dy == 0 or max(abs(x2), abs(y2)) > 6:
            return None
        g = plane(6, [(x1, y1, "A"), (x2, y2, "B")], [((x1, y1), (x2, y2), "#3f7fbf"), ((x1, y1), (x2, y1), "#c0504d"), ((x2, y1), (x2, y2), "#c0504d")])
        d = dist(dx, dy)
        return mcq("求圖中 A、B 兩點的距離。" + g, d, [str(dx + abs(dy)), dist(dx, dy + 1) if dist(dx, dy + 1) != d else dist(dx + 2, dy), sq(dx + abs(dy))], "水平差 %d、鉛直差 %d，AB ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %s。" % (dx, abs(dy), dx, abs(dy), d))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        x1, y1, x2, y2 = [R.randint(-8, 8) for _ in range(4)]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 or dy == 0:
            return None
        d = dist(dx, dy)
        if "√" not in d:
            return None
        q = "A%s和 B%s的距離是多少？" % (P(x1, y1), P(x2, y2))
        return mcq(q, d, [dist(x2 + x1, y2 + y1) if (x2 + x1) and (y2 + y1) and dist(x2 + x1, y2 + y1) != d else str(abs(dx) + abs(dy)), str(abs(dx) + abs(dy)), sq(dx * dx + abs(dy)) if dx * dx + abs(dy) != dx * dx + dy * dy else sq(abs(dx) + abs(dy))],
                   "x 差：%s%s ＝ %s，y 差：%s%s ＝ %s，AB ＝ √（%d ＋ %d）＝ √%d%s。" % (sn(x2), opv("－", x1), sn(dx), sn(y2), opv("－", y1), sn(dy), dx * dx, dy * dy, dx * dx + dy * dy, "" if d == "√%d" % (dx * dx + dy * dy) else " ＝ " + d))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def origin():
        x, y = R.randint(-9, 9), R.randint(-9, 9)
        if x == 0 or y == 0:
            return None
        d = dist(x, y)
        return mcq("點 P%s到原點的距離是多少？" % P(x, y), d, [str(abs(x) + abs(y)), sq(abs(x + y)) if abs(x + y) > 1 else str(abs(x) + abs(y) + 1), dist(x, y + 1)], "OP ＝ √（%s<sup>2</sup> ＋ %s<sup>2</sup>）＝ √%d%s。" % (sn(abs(x)), sn(abs(y)), x * x + y * y, "" if d == "√%d" % (x * x + y * y) else " ＝ " + d))

    def unk():
        dx, dy, d = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (4, 3, 5)])
        x1, y1 = R.randint(-3, 3), R.randint(-3, 3)
        q = "A%s、B（%s, k），AB ＝ %d，且 k ＞ %s。k ＝ ？" % (P(x1, y1), sn(x1 + dx), d, sn(y1))
        return mcq(q, sn(y1 + dy), [sn(y1 - dy), sn(y1 + d), sn(dy)], "x 差 %d，AB<sup>2</sup> ＝ %d<sup>2</sup> ＋（k%s）<sup>2</sup> ＝ %d，k%s ＝ %d，k ＝ %s。" % (dx, dx, opv("－", y1), d * d, opv("－", y1), dy, sn(y1 + dy)))
    return pick_unique(R, origin, 12, seen) + pick_unique(R, unk, 8, seen)


def s5(seen):
    def right():
        x, y = R.randint(-4, 4), R.randint(-4, 4)
        a, b = R.randint(2, 6), R.randint(2, 6)
        A, B, C = (x, y), (x + a, y), (x, y + b)
        q = "三角形 ABC 的頂點是 A%s、B%s、C%s。BC 的長是多少？" % (P(*A), P(*B), P(*C))
        d = dist(a, b)
        return mcq(q, d, [str(a + b), dist(a, b + 1), sq(a + b)], "∠A 是直角，AB ＝ %d、AC ＝ %d，BC ＝ √（%d ＋ %d）＝ %s。" % (a, b, a * a, b * b, d))

    def walk():
        dx, dy, d = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
        q = "地圖上每一格代表 100 公尺。學校在（0, 0），公園在（%d, %d）。兩地的直線距離是多少公尺？" % (dx, dy)
        return mcq(q, "%d 公尺" % (d * 100), ["%d 公尺" % x for x in ((dx + dy) * 100, d * 10, (d + 1) * 100)], "√（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d 格，%d × 100 ＝ %d 公尺。" % (dx, dy, d, d, d * 100))
    return pick_unique(R, right, 12, seen) + pick_unique(R, walk, 4, seen) + pick_unique(R, iso, 4, seen)


def iso():
    x, y = R.randint(1, 5), R.randint(1, 5)
    q = "點 A%s和 B%s到原點的距離一樣嗎？" % (P(x, y), P(-y, x))
    return mcq(q, "一樣", ["A 比較遠", "B 比較遠", "無法判斷"], "OA<sup>2</sup> ＝ %d ＋ %d ＝ %d，OB<sup>2</sup> ＝ %d ＋ %d ＝ %d，相等。" % (x * x, y * y, x * x + y * y, y * y, x * x, x * x + y * y))


def main():
    seen = set()
    sets = [("整數距離", s1(seen)), ("看圖求距離", s2(seen)), ("答案是根式", s3(seen)),
            ("到原點的距離與未知坐標", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["坐標平面上 A（a, b）、B（c, d）兩點的距離：<b>AB ＝ √［（a － c）<sup>2</sup> ＋（b － d）<sup>2</sup>］</b>。",
         "想法：以 AB 為斜邊畫直角三角形，兩股是 x 坐標的差和 y 坐標的差，再用畢氏定理。",
         "差可以是負的，但平方後一定是正的；算完要化成最簡根式。"],
        [example("A（1, 2）、B（4, 6）的距離？", ["x 差 3，y 差 4。", "√（9 ＋ 16）＝ √25。"], "5"),
         example("P（－2, 3）到原點的距離？", ["√（4 ＋ 9）。"], "√13")],
        [("AB ＝ 3 ＋ 4 ＝ 7", "要平方相加再開方：5"),
         ("（－2）－ 3 算成 1", "－2 － 3 ＝ －5，平方是 25"),
         ("忘了開根號，答 25", "距離是 √25 ＝ 5")])
    faq = [{"q": "兩點距離公式怎麼來的？",
            "a": "把兩點連線當作直角三角形的斜邊，兩股分別是 x 坐標的差和 y 坐標的差，再用畢氏定理求斜邊。"},
           {"q": "x 差、y 差要用大的減小的嗎？",
            "a": "不用，因為要平方，正負號都會變成正的；但要小心負數的減法。"},
           {"q": "八年級的距離公式要學什麼？",
            "a": "108課綱 G-8-1：直角坐標系上兩點 A（a, b）和 B（c, d）的距離公式。"}]
    make_unit(R, "grade-8", "distance-formula", "G-8-1",
              "直角坐標系上兩點距離公式：直角坐標系上兩點 A（a, b）和 B（c, d）的距離為 AB＝√［（a－c）²＋（b－d）²］；生活上相關問題。",
              "坐標平面上兩點的距離",
              "八年級數學 兩點距離公式 練習題｜坐標平面・畢氏定理 學習單（附解答）",
              "兩點距離公式",
              "國中八年級數學「坐標平面上兩點的距離」免費學習單：用距離公式求兩點距離、看圖畫直角三角形求距離、答案是根式、到原點的距離、未知坐標與地圖應用。100題線上練習馬上對答案，附可列印解答。",
              "AB ＝ √［（a － c）² ＋（b － d）²］",
              "x 差和 y 差是直角三角形的兩股。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
