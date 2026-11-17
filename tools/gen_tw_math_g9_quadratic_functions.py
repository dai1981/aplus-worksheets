# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：二次函數的意義與 y ＝ ax² 的圖形（108課綱 F-9-1、F-9-2）
  python3 tools/gen_tw_math_g9_quadratic_functions.py
二次函數の判斷、函數値、情境から二次函數（面積・落下）、y ＝ ax² の開口方向・開口の大小・對稱軸・頂點、グラフ上の點。
誤答：最高次數 2 でも x² の係數 0 を見落とす、（－3）² を －9 にする、|a| が大きいほど開口が大きいとする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g7 import tidy_sets, sn, par
from tw_g7_grid import plane
from tw_g8 import poly
from tw_g9 import vform, parab

R = random.Random(81112)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def which():
        a = nz(-5, 5)
        good = "y ＝ " + poly([a, R.randint(-6, 6), R.randint(-6, 6)])
        bads = ["y ＝ " + poly([nz(-5, 5), R.randint(-6, 6)]), "y ＝ " + poly([1, 0, 0, nz(-5, 5)]), "y ＝ <span class='fr'><span class='fn'>%d</span><span class='fd'>x<sup>2</sup></span></span>" % R.randint(1, 9), "y ＝ x<sup>2</sup> －（x － %d）<sup>2</sup>" % R.randint(1, 5)]
        R.shuffle(bads)
        L = "甲乙丙丁"
        xs = [good] + bads[:3]
        R.shuffle(xs)
        k = xs.index(good)
        q = "下面哪一個是 x 的二次函數？<br>" + "<br>".join("%s　%s" % (L[i], v) for i, v in enumerate(xs))
        return mcq(q, L[k], [c for c in L if c != L[k]], "整理後是 y ＝ ax<sup>2</sup> ＋ bx ＋ c（a ≠ 0）才是二次函數：%s。注意 x<sup>2</sup> －（x － k）<sup>2</sup> 展開後 x<sup>2</sup> 會消掉。" % good)

    def val():
        a, b, c = nz(-4, 4), R.randint(-6, 6), R.randint(-9, 9)
        x = nz(-4, 4)
        v = a * x * x + b * x + c
        q = "二次函數 y ＝ %s，當 x ＝ %s 時，y 是多少？" % (poly([a, b, c]), sn(x))
        return mcq(q, sn(v), [sn(-a * x * x + b * x + c), sn(a * x * x - b * x + c), sn(a * 2 * x + b * x + c), sn(v + 1)], "代入：%s × %s<sup>2</sup>%s%s ＝ %s。" % (sn(a), par(x), (" ＋ %s × %s" % (par(b), par(x))) if b else "", (" ＋ %s" % par(c)) if c else "", sn(v)))
    return pick_unique(R, which, 6, seen) + pick_unique(R, val, 14, seen)


def s2(seen):
    def area():
        P = R.randint(6, 30) * 2
        q = "用 %d 公尺長的籬笆圍一個長方形，寬是 x 公尺，面積 y 平方公尺。y 和 x 的關係是？" % P
        h = P // 2
        return mcq(q, "y ＝ x（%d － x）" % h, ["y ＝ x（%d － x）" % P, "y ＝ %dx" % h, "y ＝ x<sup>2</sup> ＋ %d" % h], "長 ＝ %d ÷ 2 － x ＝ %d － x，面積 y ＝ x（%d － x），是二次函數。" % (P, h, h))

    def sq():
        k = R.randint(2, 9)
        q = "正方形的邊長是 x 公分，邊長增加 %d 公分後的面積是 y 平方公分。y 和 x 的關係是？" % k
        return mcq(q, "y ＝（x ＋ %d）<sup>2</sup>" % k, ["y ＝ x<sup>2</sup> ＋ %d" % k, "y ＝ 4（x ＋ %d）" % k, "y ＝ x<sup>2</sup> ＋ %d" % (k * k)], "新邊長 x ＋ %d，面積 ＝（x ＋ %d）<sup>2</sup>。" % (k, k))

    def fall():
        t = R.randint(1, 6)
        q = "物體落下 t 秒走的距離約是 y ＝ 5t<sup>2</sup> 公尺。落下 %d 秒走了多少公尺？" % t
        return mcq(q, "%d 公尺" % (5 * t * t), ["%d 公尺" % x for x in (10 * t, (5 * t) ** 2, 5 * t)], "y ＝ 5 × %d<sup>2</sup> ＝ %d。" % (t, 5 * t * t))

    def circ():
        r = R.randint(2, 10)
        q = "圓的半徑 x 公分，面積 y 平方公分，y ＝ πx<sup>2</sup>。半徑 %d 公分時面積是多少？" % r
        return mcq(q, "%dπ 平方公分" % (r * r), ["%dπ 平方公分" % x for x in (2 * r, r * r * 2, r * r * 4)], "y ＝ π × %d<sup>2</sup> ＝ %dπ。" % (r, r * r))
    return pick_unique(R, area, 6, seen) + pick_unique(R, sq, 5, seen) + pick_unique(R, fall, 5, seen) + pick_unique(R, circ, 4, seen)


def s3(seen):
    def opening():
        a = R.choice([F(1), F(2), F(3), F(-1), F(-2), F(-3), F(1, 2), F(-1, 2), F(1, 3), F(-1, 3), F(4), F(-4)])
        q = "%s 的圖形開口方向和頂點是？" % vform(a, 0, 0)
        ans = "開口向%s，頂點（0，0）" % ("上" if a > 0 else "下")
        return mcq(q, ans, ["開口向%s，頂點（0，0）" % ("下" if a > 0 else "上"), "開口向%s，頂點（0，%s）" % ("上" if a > 0 else "下", sn(a) if a.denominator == 1 else "1"), "開口向右，頂點（0，0）"], "a ＝ %s %s 0，開口向%s；y ＝ ax<sup>2</sup> 的頂點都是原點，對稱軸是 y 軸。" % (sn(a) if a.denominator == 1 else fr(a.numerator, a.denominator), "＞" if a > 0 else "＜", "上" if a > 0 else "下"))

    def width():
        a, b = R.sample([1, 2, 3, 4, 5], 2)
        sa, sb = R.choice([1, -1]), R.choice([1, -1])
        A, B = sa * a, sb * b
        q = "%s 和 %s 的圖形，哪一個開口比較大（比較寬）？" % (vform(A, 0, 0), vform(B, 0, 0))
        wide = vform(A, 0, 0) if a < b else vform(B, 0, 0)
        narrow = vform(B, 0, 0) if a < b else vform(A, 0, 0)
        return mcq(q, wide, [narrow, "一樣大", "不能比較"], "|a| 越小，開口越大：|%s| ＜ |%s|。" % (sn(min(a, b) * (sa if a < b else sb)), sn(max(a, b) * (sb if a < b else sa))))
    return pick_unique(R, opening, 10, seen) + pick_unique(R, width, 10, seen)


def s4(seen):
    def onit():
        a = nz(-3, 3)
        x = nz(-4, 4)
        y = a * x * x
        q = "點（%s，k）在 %s 的圖形上，k 是多少？" % (sn(x), vform(a, 0, 0))
        return mcq(q, sn(y), [sn(-y), sn(a * 2 * x), sn((a * x) ** 2) if (a * x) ** 2 != y else sn(y + 1)], "代入 x ＝ %s：k ＝ %s × %s<sup>2</sup> ＝ %s。" % (sn(x), sn(a), par(x), sn(y)))

    def finda():
        a = nz(-4, 4)
        x = nz(-3, 3)
        y = a * x * x
        q = "y ＝ ax<sup>2</sup> 的圖形通過（%s，%s），a 是多少？" % (sn(x), sn(y))
        w = [sn(y // x) if y % x == 0 and y // x != a else sn(a + 1), sn(-a), sn(y)]
        return mcq(q, sn(a), w, "%s ＝ a × %s<sup>2</sup> ＝ %da，a ＝ %s。" % (sn(y), par(x), x * x, sn(a)))

    def sym():
        a = nz(-3, 3)
        x = nz(-4, 4)
        y = a * x * x
        q = "%s 的圖形通過（%s，%s），它對稱於 y 軸的另一點是？" % (vform(a, 0, 0), sn(x), sn(y))
        return mcq(q, "（%s，%s）" % (sn(-x), sn(y)), ["（%s，%s）" % (sn(x), sn(-y)), "（%s，%s）" % (sn(-x), sn(-y)), "（%s，%s）" % (sn(y), sn(x))], "對稱軸是 y 軸，x 坐標變號、y 坐標不變：（%s，%s）。" % (sn(-x), sn(y)))
    return pick_unique(R, onit, 7, seen) + pick_unique(R, finda, 7, seen) + pick_unique(R, sym, 6, seen)


def s5(seen):
    def graph():
        a = R.choice([F(1), F(2), F(-1), F(-2), F(1, 2), F(-1, 2)])
        g = plane(6, (), parab(a, 0, 0))
        q = "下圖是哪一個函數的圖形？" + g
        others = [vform(x, 0, 0) for x in (-a, a * 2, a / 2) if x != a]
        return mcq(q, vform(a, 0, 0), others + [vform(a, 0, 1)], "頂點在原點，開口向%s；x ＝ %s 時 y ＝ %s，所以 a ＝ %s。" % ("上" if a > 0 else "下", "2" if a.denominator == 2 else "1", sn(a * (4 if a.denominator == 2 else 1)), sn(a) if a.denominator == 1 else fr(a.numerator, 2)))
    return pick_unique(R, graph, 6, seen) + pick_unique(R, lambda: graph2(), 14, seen)


def graph2():
    a = R.choice([1, 2, 3, -1, -2, -3])
    x1, x2 = R.sample(range(-4, 5), 2)
    y1, y2 = a * x1 * x1, a * x2 * x2
    if x1 * x1 == x2 * x2:
        return None
    big = x1 if (y1 > y2) else x2
    q = "%s 的圖形上有兩點 A（%s，%s）、B（%s，%s），哪一點比較高？" % (vform(a, 0, 0), sn(x1), "y<sub>1</sub>", sn(x2), "y<sub>2</sub>")
    ans = "A" if y1 > y2 else "B"
    return mcq(q, ans, ["B" if ans == "A" else "A", "一樣高", "不能判斷"], "y<sub>1</sub> ＝ %s，y<sub>2</sub> ＝ %s，%s 比較大。開口向%s 時，離對稱軸越遠越%s。" % (sn(y1), sn(y2), "y<sub>1</sub>" if y1 > y2 else "y<sub>2</sub>", "上" if a > 0 else "下", "高" if a > 0 else "低"))


def main():
    seen = set()
    sets = [("認識二次函數", s1(seen)), ("生活中的二次函數", s2(seen)), ("開口方向與大小", s3(seen)),
            ("圖形上的點", s4(seen)), ("看圖與比較", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["可以寫成 <b>y ＝ ax<sup>2</sup> ＋ bx ＋ c（a ≠ 0）</b>的函數叫二次函數，圖形是拋物線。",
         "<b>y ＝ ax<sup>2</sup></b> 的圖形：頂點是原點，對稱軸是 y 軸。a ＞ 0 開口向上，a ＜ 0 開口向下；<b>|a| 越大開口越小</b>。" + plane(6, (), parab(1, 0, 0) + parab(-F(1, 2), 0, 0, col="#c0392b")),
         "上圖藍色是 y ＝ x<sup>2</sup>，紅色是 y ＝ －<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>x<sup>2</sup>。"],
        [example("y ＝ 2x<sup>2</sup> － 3x ＋ 1，x ＝ －2 時 y？", ["2 × 4 ＋ 6 ＋ 1。"], "15"),
         example("y ＝ ax<sup>2</sup> 通過（2，－12），a？", ["－12 ＝ 4a。"], "a ＝ －3")],
        [("（－3）<sup>2</sup> ＝ －9", "負數的平方是正的：9"),
         ("|a| 越大開口越大", "|a| 越大開口越小（越陡）"),
         ("y ＝ x<sup>2</sup> －（x － 1）<sup>2</sup> 是二次函數", "展開後 x<sup>2</sup> 消掉，是一次函數")])
    faq = [{"q": "二次函數的圖形叫什麼？",
            "a": "叫拋物線，像丟出的球飛行的路線，有一條對稱軸和一個頂點（最高點或最低點）。"},
           {"q": "怎麼判斷開口向上還是向下？",
            "a": "看 x² 的係數 a：a ＞ 0 開口向上（有最低點），a ＜ 0 開口向下（有最高點）。"},
           {"q": "九年級的二次函數要學什麼？",
            "a": "108課綱 F-9-1、F-9-2：二次函數的意義、在情境中列出二次函數，以及 y ＝ ax²、y ＝ a(x－h)² ＋ k 的圖形和最大值、最小值。"}]
    make_unit(R, "grade-9", "quadratic-functions", "F-9-1",
              "二次函數的觀念：二次函數的意義；具體情境中列出兩量的二次函數關係。",
              "二次函數與 y ＝ ax<sup>2</sup> 的圖形",
              "九年級數學 二次函數 練習題｜y＝ax²・開口方向・拋物線 學習單（附解答）",
              "二次函數",
              "國中九年級數學「二次函數與 y＝ax² 的圖形」免費學習單：判斷二次函數、函數值、生活中的二次函數、y＝ax² 的開口方向和大小、圖形上的點與看圖。100題線上練習馬上對答案，附可列印解答。",
              "y ＝ ax<sup>2</sup>：a ＞ 0 開口向上，a ＜ 0 開口向下",
              "|a| 越大開口越小；頂點是原點，對稱軸是 y 軸。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
