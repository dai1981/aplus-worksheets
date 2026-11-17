# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：二次函數的圖形（頂點與平移）（108課綱 F-9-2）
  python3 tools/gen_tw_math_g9_graphs_of_quadratic_functions.py
y ＝ a（x － h）² ＋ k の頂點（h，k）と對稱軸 x ＝ h、y ＝ ax² からの平移、配方で頂點形、グラフから式、y 軸との交點。
誤答：頂點を（－h，k）にする、左右の平移の向きを逆にする、對稱軸を y ＝ k にする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets, sn
from tw_g7_grid import plane
from tw_g8 import poly
from tw_g9 import vform, parab

R = random.Random(81113)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def P(x, y):
    return "（%s，%s）" % (sn(x), sn(y))


def s1(seen):
    def mk():
        a, h, k = nz(-4, 4), R.randint(-8, 8), R.randint(-9, 9)
        if h == 0 and k == 0:
            return None
        q = "%s 的頂點坐標是？" % vform(a, h, k)
        return mcq(q, P(h, k), [P(-h, k), P(h, -k), P(k, h), P(-h, -k)], "y ＝ a（x － h）<sup>2</sup> ＋ k 的頂點是（h，k）：%s。注意括號裡是「減 h」。" % P(h, k))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def axis():
        a, h, k = nz(-4, 4), nz(-8, 8), R.randint(-9, 9)
        q = "%s 的對稱軸是？" % vform(a, h, k)
        return mcq(q, "x ＝ %s" % sn(h), ["x ＝ %s" % sn(-h), "y ＝ %s" % sn(k), "x ＝ %s" % sn(k) if k != h else "y ＝ %s" % sn(h)], "對稱軸是通過頂點（%s，%s）的鉛垂線：x ＝ %s。" % (sn(h), sn(k), sn(h)))

    def mx():
        a, h, k = nz(-4, 4), R.randint(-8, 8), R.randint(-9, 9)
        q = "%s 的圖形開口方向和頂點是最高點還是最低點？" % vform(a, h, k)
        ans = "開口向上，頂點是最低點" if a > 0 else "開口向下，頂點是最高點"
        return mcq(q, ans, ["開口向下，頂點是最高點" if a > 0 else "開口向上，頂點是最低點", "開口向上，頂點是最高點", "開口向下，頂點是最低點"], "a ＝ %s %s 0：%s。" % (sn(a), "＞" if a > 0 else "＜", ans))
    return pick_unique(R, axis, 10, seen) + pick_unique(R, mx, 10, seen)


def s3(seen):
    def mk():
        a = nz(-3, 3)
        h, k = R.randint(-6, 6), R.randint(-6, 6)
        if h == 0 and k == 0:
            return None
        parts = []
        if h:
            parts.append("向%s平移 %d 單位" % ("右" if h > 0 else "左", abs(h)))
        if k:
            parts.append("向%s平移 %d 單位" % ("上" if k > 0 else "下", abs(k)))
        q = "把 %s 的圖形%s，得到哪一個函數的圖形？" % (vform(a, 0, 0), "，再".join(parts))
        return mcq(q, vform(a, h, k), [vform(a, -h, k) if h else vform(a, 1, k), vform(a, h, -k) if k else vform(a, h, 1), vform(a, -h, -k) if (h or k) else vform(a, 1, 1), vform(-a, h, k)], "頂點從（0，0）移到（%s，%s）：%s。向右平移 h 是「x － h」。" % (sn(h), sn(k), vform(a, h, k)))

    def rev():
        a = nz(-3, 3)
        h, k = nz(-6, 6), nz(-6, 6)
        q = "%s 的圖形可以由 %s 的圖形怎樣平移得到？" % (vform(a, h, k), vform(a, 0, 0))
        ans = "向%s %d、向%s %d" % ("右" if h > 0 else "左", abs(h), "上" if k > 0 else "下", abs(k))
        w = ["向%s %d、向%s %d" % ("左" if h > 0 else "右", abs(h), "上" if k > 0 else "下", abs(k)), "向%s %d、向%s %d" % ("右" if h > 0 else "左", abs(h), "下" if k > 0 else "上", abs(k)), "向%s %d、向%s %d" % ("左" if h > 0 else "右", abs(h), "下" if k > 0 else "上", abs(k))]
        return mcq(q, ans, w, "頂點由（0，0）變成（%s，%s）：%s。" % (sn(h), sn(k), ans))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, rev, 8, seen)


def s4(seen):
    def mk():
        h, k = nz(-6, 6), R.randint(-12, 12)
        a = R.choice([1, 1, 1, -1, 2])
        cs = [a, -2 * a * h, a * h * h + k]
        q = "把 y ＝ %s 化成 y ＝ a（x － h）<sup>2</sup> ＋ k 的形式，頂點是？" % poly(cs)
        return mcq(q, P(h, k), [P(-h, k), P(h, cs[2]), P(h, -k) if k else P(h, 1), P(-h, -k) if k else P(-h, 1)],
                   "配方：%s，頂點是 %s。" % (vform(a, h, k), P(h, k)))

    def yint():
        a, h, k = nz(-3, 3), nz(-5, 5), R.randint(-9, 9)
        v = a * h * h + k
        q = "%s 的圖形和 y 軸的交點是？" % vform(a, h, k)
        return mcq(q, P(0, v), [P(0, k), P(h, k), P(0, a * h + k) if a * h + k != v else P(0, v + 1)], "y 軸上 x ＝ 0：y ＝ %s ×（%s）<sup>2</sup>%s ＝ %s，交點 %s。" % (sn(a), sn(-h), (" ＋ %d" % k) if k > 0 else (" － %d" % -k) if k else "", sn(v), P(0, v)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, yint, 8, seen)


def s5(seen):
    def mk():
        a = R.choice([1, -1, 2, -2])
        h, k = R.randint(-3, 3), R.randint(-3, 3)
        if h == 0 and k == 0:
            return None
        g = plane(6, [(h, k, "頂點")], parab(a, h, k))
        q = "下圖拋物線的 a ＝ %s，它是哪一個函數的圖形？" % sn(a) + g
        return mcq(q, vform(a, h, k), [vform(a, -h, k) if h else vform(a, 1, k), vform(a, h, -k) if k else vform(a, h, 1), vform(a, k, h) if k != h else vform(a, -h, -k)], "從圖讀出頂點是 %s，所以 %s。" % (P(h, k), vform(a, h, k)))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("頂點", s1(seen)), ("對稱軸與開口", s2(seen)), ("圖形的平移", s3(seen)),
            ("配方與交點", s4(seen)), ("看圖寫函數", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>y ＝ a（x － h）<sup>2</sup> ＋ k</b> 的頂點是 <b>（h，k）</b>，對稱軸是 <b>x ＝ h</b>。",
         "它的圖形是把 y ＝ ax<sup>2</sup> 的圖形向右平移 h、向上平移 k（h、k 是負數就向左、向下），形狀和開口不變。",
         "一般式 y ＝ ax<sup>2</sup> ＋ bx ＋ c 可以用配方化成頂點式。" + plane(6, [(2, -3, "（2，－3）")], parab(1, 2, -3))],
        [example("y ＝ 2（x ＋ 1）<sup>2</sup> － 5 的頂點和對稱軸", ["x ＋ 1 ＝ x －（－1），h ＝ －1。"], "（－1，－5），x ＝ －1"),
         example("y ＝ x<sup>2</sup> － 4x ＋ 1 的頂點", ["配方：（x － 2）<sup>2</sup> － 3。"], "（2，－3）")],
        [("y ＝（x ＋ 1）<sup>2</sup> 的頂點是（1，0）", "x ＋ 1 ＝ x －（－1），頂點（－1，0）"),
         ("向右平移 3 寫成（x ＋ 3）<sup>2</sup>", "向右是（x － 3）<sup>2</sup>"),
         ("對稱軸寫成 y ＝ k", "對稱軸是鉛垂線 x ＝ h")])
    faq = [{"q": "為什麼「x － h」是向右平移？",
            "a": "原來 x ＝ 0 時在頂點，現在要 x － h ＝ 0，也就是 x ＝ h 時才到頂點，所以頂點往右移了 h。"},
           {"q": "a 改變會影響什麼？",
            "a": "a 決定開口方向和大小：a ＞ 0 向上、a ＜ 0 向下，|a| 越大開口越小；平移不會改變 a。"},
           {"q": "九年級的二次函數圖形要學什麼？",
            "a": "108課綱 F-9-2：對稱軸、頂點、開口方向等名詞，y ＝ ax²、y ＝ ax² ＋ k、y ＝ a(x－h)²、y ＝ a(x－h)² ＋ k 的圖形和平移關係。"}]
    make_unit(R, "grade-9", "graphs-of-quadratic-functions", "F-9-2",
              "二次函數的圖形與極值：二次函數的相關名詞（對稱軸、頂點、最低點、最高點、開口向上、開口向下、最大值、最小值）；描繪 y＝ax²、y＝ax²＋k、y＝a(x－h)²、y＝a(x－h)²＋k 的圖形；對稱軸就是通過頂點（最高點、最低點）的鉛垂線；y＝ax² 的圖形與 y＝a(x－h)²＋k 的圖形的平移關係；已配方好之二次函數的最大值與最小值。",
              "二次函數的圖形：頂點、對稱軸與平移",
              "九年級數學 二次函數圖形 練習題｜頂點・對稱軸・平移・配方 學習單（附解答）",
              "二次函數的圖形",
              "國中九年級數學「二次函數的圖形：頂點、對稱軸與平移」免費學習單：y＝a(x－h)²＋k 的頂點和對稱軸、開口方向、圖形平移、配方求頂點、和 y 軸的交點、看圖寫函數。100題線上練習馬上對答案，附可列印解答。",
              "y ＝ a（x － h）<sup>2</sup> ＋ k 的頂點是（h，k）",
              "對稱軸 x ＝ h；向右平移 h 是「x － h」。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
