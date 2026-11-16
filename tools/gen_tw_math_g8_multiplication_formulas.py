# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：乘法公式（108課綱 A-8-1）
  python3 tools/gen_tw_math_g8_multiplication_formulas.py
和の平方・差の平方・平方差・(a＋b)(c＋d) の展開、數の速算（102²、99×101、49²）、式の値・應用。
誤答：(a＋b)²＝a²＋b²（2ab を落とす）、(a－b)² の中間項の符號、(a＋b)(a－b)＝a²＋b²、分配の掛け漏れ。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g8 import poly, pmul, padd, sn, par, tidy_sets, pq

R = random.Random(81001)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def s1(seen):
    def mk():
        a, b = R.randint(1, 6), nz(-9, 9)
        q = "展開 %s<sup>2</sup>" % pq(a, b)
        ans = poly([a * a, 2 * a * b, b * b])
        return mcq(q, ans, [poly([a * a, 0, b * b]), poly([a * a, a * b, b * b]), poly([a * a, -2 * a * b, b * b])],
                   "（a %s b）<sup>2</sup> ＝ a<sup>2</sup> %s 2ab ＋ b<sup>2</sup>：中間項 2 × %s × %s ＝ %s，不能漏掉。" % ("＋" if b > 0 else "－", "＋" if b > 0 else "－", poly([a, 0]), par(b), poly([2 * a * b, 0])))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 7), R.randint(1, 12)
        k = R.choice(["diff", "pair"])
        if k == "diff":
            q = "展開 %s%s" % (pq(a, b), pq(a, -b))
            ans = poly([a * a, 0, -b * b])
            w = [poly([a * a, 0, b * b]), poly([a * a, -2 * a * b, -b * b]), poly([a * a, 2 * a * b, -b * b])]
            e = "（a ＋ b）（a － b）＝ a<sup>2</sup> － b<sup>2</sup>：%s。" % ans
        else:
            c, d = R.randint(1, 5), nz(-9, 9)
            b = R.choice([b, -b])
            q = "展開 %s%s" % (pq(a, b), pq(c, d))
            r = pmul([a, b], [c, d])
            ans = poly(r)
            w = [poly([a * c, 0, b * d]), poly([a * c, a * d - b * c, b * d]) if a * d - b * c != r[1] else poly([a * c, r[1] + 1, b * d]), poly([a * c, r[1], -b * d])]
            e = "每一項都要乘：%s × %s ＋ %s × %s ＋ %s × %s ＋ %s × %s ＝ %s。" % (poly([a, 0]), poly([c, 0]), poly([a, 0]), par(d), par(b), poly([c, 0]), par(b), par(d), ans)
        return mcq(q, ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        k = R.choice(["sq+", "sq-", "pm"])
        if k == "sq+":
            b = R.randint(1, 9)
            base = R.choice([10, 20, 30, 50, 100])
            n = base + b
            q = "用乘法公式速算：%d<sup>2</sup>" % n
            e = "（%d ＋ %d）<sup>2</sup> ＝ %s ＋ %d ＋ %d ＝ %s。" % (base, b, num(base * base), 2 * base * b, b * b, num(n * n))
            w = [base * base + b * b, n * n + 2 * b, n * n - 2 * base * b + base * b]
            v = n * n
        elif k == "sq-":
            b = R.randint(1, 4)
            base = R.choice([20, 30, 50, 100, 200])
            n = base - b
            q = "用乘法公式速算：%d<sup>2</sup>" % n
            e = "（%d － %d）<sup>2</sup> ＝ %s － %d ＋ %d ＝ %s。" % (base, b, num(base * base), 2 * base * b, b * b, num(n * n))
            w = [base * base - b * b, base * base + 2 * base * b + b * b - 4 * base * b + 2, n * n + 2 * base * b]
            v = n * n
        else:
            b = R.randint(1, 5)
            base = R.choice([20, 30, 40, 50, 100])
            q = "用乘法公式速算：%d × %d" % (base + b, base - b)
            v = base * base - b * b
            e = "（%d ＋ %d）（%d － %d）＝ %s － %d ＝ %s。" % (base, b, base, b, num(base * base), b * b, num(v))
            w = [base * base + b * b, base * base, v - 2 * b]
        return mcq(q, num(v), [num(x) for x in w if x != v] + [num(v + 10)], e)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        s_, p_ = R.randint(2, 12), R.randint(1, 20)
        k = R.choice(["sumsq", "diffsq"])
        if k == "sumsq":
            q = "已知 a ＋ b ＝ %d，ab ＝ %d，a<sup>2</sup> ＋ b<sup>2</sup> ＝ ？" % (s_, p_)
            v = s_ * s_ - 2 * p_
            w = [s_ * s_, s_ * s_ + 2 * p_, s_ * s_ - p_]
            e = "a<sup>2</sup> ＋ b<sup>2</sup> ＝（a ＋ b）<sup>2</sup> － 2ab ＝ %d － %d ＝ %s。" % (s_ * s_, 2 * p_, sn(v))
        else:
            q = "已知 a ＋ b ＝ %d，ab ＝ %d，（a － b）<sup>2</sup> ＝ ？" % (s_, p_)
            v = s_ * s_ - 4 * p_
            if v < 0:
                return None
            w = [s_ * s_ - 2 * p_, s_ * s_, s_ * s_ + 4 * p_]
            e = "（a － b）<sup>2</sup> ＝（a ＋ b）<sup>2</sup> － 4ab ＝ %d － %d ＝ %s。" % (s_ * s_, 4 * p_, sn(v))
        return mcq(q, sn(v), [sn(x) for x in w if x != v] + [sn(v + 1)], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def area():
        a, b = R.randint(3, 15), R.randint(1, 8)
        q = "邊長 %d 公分的正方形，每邊加長 %d 公分後，面積增加多少平方公分？" % (a, b)
        v = (a + b) ** 2 - a * a
        return mcq(q, "%d 平方公分" % v, ["%d 平方公分" % x for x in (b * b, 2 * a * b, 4 * b)  if x != v] + ["%d 平方公分" % (v + b)], "（%d ＋ %d）<sup>2</sup> － %d<sup>2</sup> ＝ 2 × %d × %d ＋ %d<sup>2</sup> ＝ %d。" % (a, b, a, a, b, b, v))

    def frame():
        a, b = R.randint(5, 20), R.randint(1, 4)
        q = "長方形花圃長 %d 公尺、寬 %d 公尺，四周鋪一圈寬 %d 公尺的步道。步道面積是多少平方公尺？" % (a + 6, a, b)
        L, W = a + 6, a
        v = (L + 2 * b) * (W + 2 * b) - L * W
        return mcq(q, "%d 平方公尺" % v, ["%d 平方公尺" % x for x in ((L + b) * (W + b) - L * W, 2 * b * (L + W), (L + 2 * b) * (W + 2 * b))  if x != v] + ["%d 平方公尺" % (v + 4)], "外面大長方形（%d ＋ %d）（%d ＋ %d）減去花圃 %d × %d ＝ %d。" % (L, 2 * b, W, 2 * b, L, W, v))

    def value():
        x = R.choice([99, 101, 49, 51, 199, 201])
        q = "x ＝ %d 時，x<sup>2</sup> － 2x ＋ 1 的值是多少？" % x
        v = (x - 1) ** 2
        return mcq(q, num(v), [num(t) for t in (x * x - 1, (x + 1) ** 2, x * x)], "x<sup>2</sup> － 2x ＋ 1 ＝（x － 1）<sup>2</sup> ＝ %d<sup>2</sup> ＝ %s。" % (x - 1, num(v)))
    return pick_unique(R, area, 8, seen) + pick_unique(R, frame, 6, seen) + pick_unique(R, value, 6, seen)


def main():
    seen = set()
    sets = [("和的平方與差的平方", s1(seen)), ("平方差與一般展開", s2(seen)), ("速算", s3(seen)),
            ("求式子的值", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>（a ＋ b）<sup>2</sup> ＝ a<sup>2</sup> ＋ 2ab ＋ b<sup>2</sup></b>；<b>（a － b）<sup>2</sup> ＝ a<sup>2</sup> － 2ab ＋ b<sup>2</sup></b>。",
         "<b>（a ＋ b）（a － b）＝ a<sup>2</sup> － b<sup>2</sup></b>（平方差）。",
         "<b>（a ＋ b）（c ＋ d）＝ ac ＋ ad ＋ bc ＋ bd</b>：每一項都要乘到。",
         "速算：102<sup>2</sup> ＝（100 ＋ 2）<sup>2</sup>，98 × 102 ＝ 100<sup>2</sup> － 2<sup>2</sup>。"],
        [example("（2x ＋ 3）<sup>2</sup>", ["4x<sup>2</sup> ＋ 2 × 2x × 3 ＋ 9。"], "4x<sup>2</sup> ＋ 12x ＋ 9"),
         example("49<sup>2</sup>", ["（50 － 1）<sup>2</sup> ＝ 2500 － 100 ＋ 1。"], "2401")],
        [("（a ＋ b）<sup>2</sup> ＝ a<sup>2</sup> ＋ b<sup>2</sup>", "漏了中間的 2ab"),
         ("（x － 3）<sup>2</sup> ＝ x<sup>2</sup> － 6x － 9", "最後一項是 ＋9"),
         ("（x ＋ 5）（x － 5）＝ x<sup>2</sup> ＋ 25", "平方差：x<sup>2</sup> － 25")])
    faq = [{"q": "為什麼（a ＋ b）² 不等於 a² ＋ b²？",
            "a": "畫一個邊長 a ＋ b 的正方形，可以切成 a²、b² 和兩個 ab 的長方形，所以多了 2ab。"},
           {"q": "乘法公式有什麼用？",
            "a": "可以快速展開多項式、做數的速算（例如 99 × 101），也是之後因式分解的基礎。"},
           {"q": "八年級的乘法公式要學什麼？",
            "a": "108課綱 A-8-1：和的平方、差的平方、平方差公式，以及（a＋b）（c＋d）的展開。"}]
    make_unit(R, "grade-8", "multiplication-formulas", "A-8-1",
              "乘法公式：（a＋b）²＝a²＋2ab＋b²；（a－b）²＝a²－2ab＋b²；（a＋b）（a－b）＝a²－b²；（a＋b）（c＋d）＝ac＋ad＋bc＋bd。",
              "乘法公式：和的平方、差的平方、平方差",
              "八年級數學 乘法公式 練習題｜和的平方・差的平方・平方差・速算 學習單（附解答）",
              "乘法公式",
              "國中八年級數學「乘法公式」免費學習單：和的平方、差的平方、平方差、（a＋b）（c＋d）展開、用乘法公式速算與求值、面積應用題。100題線上練習馬上對答案，附可列印解答。",
              "（a ＋ b）² ＝ a² ＋ 2ab ＋ b²",
              "中間項 2ab 不能漏；平方差（a ＋ b）（a － b）＝ a² － b²。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
