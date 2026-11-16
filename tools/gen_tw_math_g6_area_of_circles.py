# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：圓面積與扇形面積（108課綱 S-6-3）
  python3 tools/gen_tw_math_g6_area_of_circles.py
圓面積＝半徑×半徑×3.14（分割して長方形に近づける説明）、直徑から、半圓・四分之一圓、扇形面積（圓心角/360）、複合圖形（甜甜圈・正方形との差）。
誤答：直徑×直徑×3.14、半徑×2×3.14（圓周長）と混同、扇形で 360 を掛け忘れる。
"""
import random
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g6_circle import circle_svg

R = random.Random(61012)
NM = Names(R)
PI = D("3.14")


def s_(x):
    x = D(x)
    if x.as_tuple().exponent < -3:
        x = x.quantize(D("0.01"))
    x = x.normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return num(int(i)) + "." + f
    return num(int(t))


def s1(seen):
    def concept():
        F_ = [("把圓切成很多小扇形再拼起來，會接近什麼形狀？", "長方形", ["三角形", "正方形", "梯形"], "拼起來接近長方形：長是圓周長的一半，寬是半徑。"),
              ("拼成的長方形，長是圓的什麼？", "圓周長的一半", ["直徑", "半徑", "圓周長"], "上下兩邊合起來是圓周長，所以長是圓周長的一半。"),
              ("拼成的長方形，寬是圓的什麼？", "半徑", ["直徑", "圓周長", "圓周長的一半"], "寬就是扇形的半徑。"),
              ("圓面積的公式是什麼？", "半徑 × 半徑 × 3.14", ["直徑 × 3.14", "半徑 × 2 × 3.14", "直徑 × 直徑 × 3.14"], "圓周長的一半 × 半徑 ＝ 半徑 × 3.14 × 半徑。"),
              ("半徑變成 2 倍，圓面積變成幾倍？", "4 倍", ["2 倍", "3.14 倍", "8 倍"], "半徑 × 半徑：2 × 2 ＝ 4 倍。"),
              ("圓面積的單位是什麼？", "平方公分（或平方公尺）", ["公分", "立方公分", "公尺"], "面積的單位是平方公分、平方公尺等。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, concept, 6, seen) + pick_unique(R, area_r, 14, seen)


def area_r():
    r = R.randint(2, 30)
    a = r * r * PI
    g = circle_svg("%d 公分" % r, "r", label="半徑 %d 公分的圓" % r)
    return mcq("求這個圓的面積。" + g, "%s 平方公分" % s_(a), ["%s 平方公分" % s_(x) for x in (r * 2 * PI, r * 2 * r * 2 * PI, r * PI)],
               "半徑 × 半徑 × 3.14：%d × %d × 3.14 ＝ %s（平方公分）。" % (r, r, s_(a)))


def s2(seen):
    def mk():
        d = R.randrange(4, 60, 2)
        r = d // 2
        a = r * r * PI
        g = circle_svg("%d 公分" % d, "d", label="直徑 %d 公分的圓" % d)
        return mcq("求這個圓的面積。" + g, "%s 平方公分" % s_(a), ["%s 平方公分" % s_(x) for x in (d * d * PI, d * PI, r * r * PI * 2, r * PI)],
                   "先求半徑 %d ÷ 2 ＝ %d，%d × %d × 3.14 ＝ %s（平方公分）。" % (d, r, r, r, s_(a)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        r = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
        a = R.choice([180, 90, 60, 45, 120, 30, 270, 72, 36, 150])
        area = r * r * PI * a / 360
        if area.as_tuple().exponent < -3:
            return None
        g = circle_svg("%d 公分" % r, "r", angle=a, label="半徑 %d 公分、圓心角 %d 度的扇形" % (r, a))
        return mcq("求這個扇形的面積。" + g, "%s 平方公分" % s_(area), ["%s 平方公分" % s_(x) for x in (r * r * PI, 2 * r * PI * a / 360, r * r * PI * 360 / a / 100 if False else r * r * PI / 2 if a != 180 else r * r * PI / 4, area * 2, D(r * r * a) / 360, area + r)  if x != area],
                   "扇形面積 ＝ 圓面積 × 圓心角 ÷ 360：%d × %d × 3.14 × %d ÷ 360 ＝ %s（平方公分）。" % (r, r, a, s_(area)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def ring():
        R2, r = R.choice([(5, 3), (6, 4), (10, 5), (8, 6), (7, 3), (10, 8), (9, 6), (12, 10), (5, 4)])
        A = (R2 * R2 - r * r) * PI
        q = "一個甜甜圈形狀，外圓半徑 %d 公分，內圓半徑 %d 公分。中間挖空，剩下的面積是多少平方公分？" % (R2, r)
        return mcq(q, "%s 平方公分" % s_(A), ["%s 平方公分" % s_(x) for x in ((R2 - r) * (R2 - r) * PI, R2 * R2 * PI, R2 * R2 - r * r)], "大圓 － 小圓：（%d × %d － %d × %d）× 3.14 ＝ %s（平方公分）。" % (R2, R2, r, r, s_(A)))

    def square():
        s = R.choice([4, 6, 8, 10, 12, 20])
        r = D(s) / 2
        A = s * s - r * r * PI
        q = "邊長 %d 公分的正方形裡，畫一個最大的圓。正方形裡圓以外的部分，面積是多少平方公分？" % s
        return mcq(q, "%s 平方公分" % s_(A), ["%s 平方公分" % s_(x) for x in (s * s - s * s * PI / 4 * 4 + 1 if False else s * s * PI - s * s, r * r * PI, s * s - s * PI, D(s * s) / 2)  if x > 0 and x != A],
                   "正方形 %d × %d ＝ %d，圓半徑 %s，圓面積 %s × %s × 3.14 ＝ %s，%d － %s ＝ %s（平方公分）。" % (s, s, s * s, s_(r), s_(r), s_(r), s_(r * r * PI), s * s, s_(r * r * PI), s_(A)))

    def quarter():
        r = R.choice([4, 6, 8, 10, 12, 20])
        A = r * r * PI / 4
        q = "半徑 %d 公分的圓的四分之一（圓心角 90 度），面積是多少平方公分？" % r
        return mcq(q, "%s 平方公分" % s_(A), ["%s 平方公分" % s_(x) for x in (r * r * PI / 2, r * 2 * PI / 4, r * r * PI)], "%d × %d × 3.14 ÷ 4 ＝ %s（平方公分）。" % (r, r, s_(A)))
    return pick_unique(R, ring, 8, seen) + pick_unique(R, square, 6, seen) + pick_unique(R, quarter, 6, seen)


def s5(seen):
    def pizza():
        d = R.choice([20, 24, 30, 36, 40])
        n = R.choice([6, 8, 12])
        r = d // 2
        A = r * r * PI / n
        if A.as_tuple().exponent < -2:
            return None
        q = "一個直徑 %d 公分的圓形披薩平分成 %d 片，每片面積是多少平方公分？" % (d, n)
        return mcq(q, "%s 平方公分" % s_(A), ["%s 平方公分" % s_(x) for x in (d * d * PI / n, r * r * PI, d * PI / n)], "半徑 %d，%d × %d × 3.14 ÷ %d ＝ %s（平方公分）。" % (r, r, r, n, s_(A)))

    def sprinkler():
        r = R.choice([3, 4, 5, 6, 10])
        a = R.choice([90, 120, 180, 270])
        A = r * r * PI * a / 360
        if A.as_tuple().exponent < -3:
            return None
        q = "灑水器能噴到半徑 %d 公尺、轉動 %d 度的扇形範圍。可以灑到多少平方公尺？" % (r, a)
        return mcq(q, "%s 平方公尺" % s_(A), ["%s 平方公尺" % s_(x) for x in (r * r * PI, 2 * r * PI * a / 360, A * 2, A / 2, D(r * r * a) / 360, A + r)], "%d × %d × 3.14 × %d ÷ 360 ＝ %s（平方公尺）。" % (r, r, a, s_(A)))

    def compare():
        a, b = R.sample([2, 3, 4, 5, 6], 2)
        q = "半徑 %d 公分的圓面積，是半徑 %d 公分的圓面積的幾倍？" % (max(a, b), min(a, b))
        hi, lo = max(a, b), min(a, b)
        from fractions import Fraction as F
        from tw_common import ff
        k = F(hi * hi, lo * lo)
        return mcq(q, "%s 倍" % ff(k), ["%s 倍" % ff(x) for x in (F(hi, lo), F(hi * hi, lo), k + 1)  if x != k], "面積比 ＝ 半徑 × 半徑的比：%d × %d ÷（%d × %d）＝ %s。" % (hi, hi, lo, lo, ff(k)))
    return pick_unique(R, pizza, 7, seen) + pick_unique(R, sprinkler, 7, seen) + pick_unique(R, compare, 6, seen)


def main():
    seen = set()
    sets = [("圓面積公式", s1(seen)), ("由直徑求圓面積", s2(seen)), ("扇形面積", s3(seen)),
            ("複合圖形", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["把圓切成很多小扇形，拼起來接近長方形：長是圓周長的一半，寬是半徑。",
         "<b>圓面積 ＝ 半徑 × 半徑 × 3.14</b>。題目給直徑時，先除以 2。",
         "<b>扇形面積 ＝ 圓面積 × 圓心角 ÷ 360</b>；半圓是 ÷ 2，四分之一圓是 ÷ 4。"],
        [example("直徑 10 公分的圓，面積是多少？", ["半徑 5 公分。", "5 × 5 × 3.14 ＝ 78.5。"], "78.5 平方公分"),
         example("半徑 6 公分、圓心角 60 度的扇形面積？", ["6 × 6 × 3.14 ＝ 113.04。", "113.04 × 60 ÷ 360 ＝ 18.84。"], "18.84 平方公分")],
        [("直徑 × 直徑 × 3.14", "要用半徑 × 半徑 × 3.14"),
         ("半徑 × 2 × 3.14 當成面積", "那是圓周長"),
         ("扇形面積忘了 × 圓心角 ÷ 360", "扇形只是圓的一部分")])
    faq = [{"q": "圓面積公式怎麼來的？",
            "a": "把圓切成很多小扇形交錯拼起來，接近一個長方形，長是圓周長的一半（半徑 × 3.14），寬是半徑，所以面積是半徑 × 半徑 × 3.14。"},
           {"q": "扇形面積怎麼算？",
            "a": "先算整個圓的面積，再乘以圓心角 ÷ 360，例如 90 度是圓的四分之一。"},
           {"q": "六年級的圓面積要學什麼？",
            "a": "108課綱 S-6-3：用分割說明圓面積公式，求扇形弧長與面積，並理解圓心角：360 ＝ 扇形面積：圓面積。"}]
    make_unit(R, "grade-6", "area-of-circles", "S-6-3",
              "圓周率、圓周長、圓面積、扇形面積：用分割說明圓面積公式。求扇形弧長與面積。知道以下三個比相等：（1）圓心角：360；（2）扇形弧長：圓周長；（3）扇形面積：圓面積，但應用問題只處理用（1）求弧長或面積。",
              "圓面積與扇形面積",
              "六年級數學 圓面積 練習題｜半徑×半徑×3.14・扇形面積 學習單（附解答）",
              "圓面積",
              "國小六年級數學「圓面積與扇形面積」免費學習單：圓面積公式的由來、由半徑和直徑求圓面積、扇形面積、甜甜圈等複合圖形與披薩、灑水器應用題。100題線上練習馬上對答案，附可列印解答。",
              "圓面積 ＝ 半徑 × 半徑 × 3.14",
              "扇形面積 ＝ 圓面積 × 圓心角 ÷ 360。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
