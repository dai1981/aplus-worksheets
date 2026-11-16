# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：圓周率與圓周長（108課綱 S-6-3）
  python3 tools/gen_tw_math_g6_circumference.py
圓周率（圓周長÷直徑≈3.14）、圓周長＝直徑×3.14＝半徑×2×3.14、圓周長から直徑・半徑、半圓の周長、扇形の弧長（圓心角/360）、應用（車輪）。
誤答：半徑×3.14 で 2 倍を忘れる、半圓の周長で直徑を足し忘れる、半徑×半徑×3.14（面積）と混同。
"""
import random
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g6_circle import circle_svg

R = random.Random(61011)
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
        F_ = [("圓周率是什麼？", "圓周長 ÷ 直徑的值", ["圓周長 ÷ 半徑的值", "直徑 ÷ 圓周長的值", "圓的面積 ÷ 直徑"], "任何圓的圓周長 ÷ 直徑都約是 3.14，叫做圓周率。"),
              ("國小計算時，圓周率通常用多少？", "3.14", ["3", "3.41", "2.14"], "圓周率約是 3.14159…，計算時用 3.14。"),
              ("大圓和小圓的圓周率一樣嗎？", "一樣，都約是 3.14", ["大圓的比較大", "小圓的比較大", "要看顏色"], "不管圓多大，圓周長 ÷ 直徑都約是 3.14。"),
              ("圓周長大約是直徑的幾倍？", "約 3 倍多一點", ["約 2 倍", "約 4 倍", "剛好 3 倍"], "圓周長 ＝ 直徑 × 3.14，比 3 倍多一點。"),
              ("半徑和直徑的關係是什麼？", "直徑 ＝ 半徑 × 2", ["半徑 ＝ 直徑 × 2", "直徑 ＝ 半徑 ＋ 2", "一樣長"], "直徑通過圓心，是半徑的 2 倍。"),
              ("用繩子繞一個圓罐一圈，量到的是什麼？", "圓周長", ["直徑", "半徑", "面積"], "繞圓一圈的長度就是圓周長。")]
        return mcq(*R.choice(F_))

    def ratio():
        d = R.randint(5, 60)
        c = d * PI
        q = "直徑 %d 公分的圓，圓周長最接近多少公分？" % d
        near = int(c.quantize(D("1")))
        return mcq(q, "約 %d 公分" % near, ["約 %d 公分" % x for x in (d * 2, d * 4 + 3, d + 3)], "圓周長是直徑的 3 倍多一點：%d × 3.14 ＝ %s，約 %d 公分。" % (d, s_(c), near))
    return pick_unique(R, concept, 6, seen) + pick_unique(R, ratio, 14, seen)


def s2(seen):
    def mk():
        kind = R.choice(["d", "r"])
        v = R.randint(2, 30)
        c = (v if kind == "d" else 2 * v) * PI
        g = circle_svg("%d 公分" % v, kind, label="%s %d 公分的圓" % ("直徑" if kind == "d" else "半徑", v))
        q = "求這個圓的圓周長。" + g
        wrong = [v * PI if kind == "r" else v * 2 * PI, v * v * PI, (v if kind == "d" else 2 * v) * 3, c * 2, (v if kind == "d" else 2 * v), c + v]
        return mcq(q, "%s 公分" % s_(c), ["%s 公分" % s_(x) for x in wrong if x != c],
                   ("直徑 × 3.14：%d × 3.14 ＝ %s（公分）。" % (v, s_(c))) if kind == "d" else ("半徑 × 2 × 3.14：%d × 2 × 3.14 ＝ %s（公分）。" % (v, s_(c))))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        d = R.randint(2, 40)
        c = d * PI
        ask = R.choice(["d", "r"])
        if ask == "r" and d % 2:
            return None
        q = "一個圓的圓周長是 %s 公分，%s是幾公分？" % (s_(c), "直徑" if ask == "d" else "半徑")
        v = d if ask == "d" else d // 2
        w = [d * 2 if ask == "d" else d, s_(c / 2), v + 1]
        return mcq(q, "%d 公分" % v, ["%s 公分" % x for x in w if str(x) != str(v)],
                   ("直徑 ＝ 圓周長 ÷ 3.14：%s ÷ 3.14 ＝ %d（公分）。" % (s_(c), d)) if ask == "d" else ("直徑 ＝ %s ÷ 3.14 ＝ %d，半徑 ＝ %d ÷ 2 ＝ %d（公分）。" % (s_(c), d, d, v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def half():
        d = R.randint(4, 30)
        arc = d * PI / 2
        tot = arc + d
        g = circle_svg("%d 公分" % d, "d", angle=180, label="直徑 %d 公分的半圓" % d)
        q = "求這個半圓的周長（含直徑）。" + g
        return mcq(q, "%s 公分" % s_(tot), ["%s 公分" % s_(x) for x in (arc, d * PI + d, arc + D(d) / 2)], "弧長 %d × 3.14 ÷ 2 ＝ %s，再加直徑 %d：%s（公分）。" % (d, s_(arc), d, s_(tot)))

    def sector():
        r = R.choice([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20])
        a = R.choice([30, 45, 60, 90, 120, 135, 150, 240, 270])
        arc = 2 * r * PI * a / 360
        if arc.as_tuple().exponent < -2:
            return None
        g = circle_svg("%d 公分" % r, "r", angle=a, label="半徑 %d 公分、圓心角 %d 度的扇形" % (r, a))
        q = "求這個扇形的弧長。" + g
        return mcq(q, "%s 公分" % s_(arc), ["%s 公分" % s_(x) for x in (r * PI * a / 360, arc + 2 * r, 2 * r * PI)  if x != arc],
                   "弧長 ＝ 圓周長 × 圓心角 ÷ 360：%d × 2 × 3.14 × %d ÷ 360 ＝ %s（公分）。" % (r, a, s_(arc)))
    return pick_unique(R, half, 8, seen) + pick_unique(R, sector, 12, seen)


def s5(seen):
    def wheel():
        d = R.choice([50, 60, 70, 40, 65])
        n = R.choice([10, 20, 50, 100, 200])
        dist = d * PI * n
        who = NM.next()
        q = "%s的腳踏車輪子直徑 %d 公分，輪子轉 %d 圈，前進多少公尺？" % (who, d, n)
        m = dist / 100
        return mcq(q, "%s 公尺" % s_(m), ["%s 公尺" % s_(x) for x in (dist, m / 2, D(d * n) / 100)], "一圈 %d × 3.14 ＝ %s 公分，%s × %d ＝ %s 公分 ＝ %s 公尺。" % (d, s_(d * PI), s_(d * PI), n, s_(dist), s_(m)))

    def track():
        r = R.choice([10, 15, 20, 25, 30])
        L = R.choice([50, 80, 100])
        tot = 2 * L + 2 * r * PI
        q = "操場跑道是兩條 %d 公尺的直道，兩端是半徑 %d 公尺的半圓。跑一圈是多少公尺？" % (L, r)
        return mcq(q, "%s 公尺" % s_(tot), ["%s 公尺" % s_(x) for x in (L * 2 + r * PI, L + 2 * r * PI, 2 * L + 4 * r * PI)], "兩個半圓合起來是一個圓：%d × 2 × 3.14 ＝ %s，再加 %d × 2：%s（公尺）。" % (r, s_(2 * r * PI), L, s_(tot)))

    def tree():
        c = R.choice([D("314"), D("251.2"), D("188.4"), D("157"), D("94.2"), D("125.6")])
        d = c / PI
        q = "一棵大樹的樹幹一圈長 %s 公分，樹幹的直徑大約是幾公分？" % s_(c)
        return mcq(q, "%s 公分" % s_(d), ["%s 公分" % s_(x) for x in (d / 2, c / 2, d * 2)], "直徑 ＝ 圓周長 ÷ 3.14：%s ÷ 3.14 ＝ %s（公分）。" % (s_(c), s_(d)))
    return pick_unique(R, wheel, 8, seen) + pick_unique(R, track, 6, seen) + pick_unique(R, tree, 6, seen)


def main():
    seen = set()
    sets = [("認識圓周率", s1(seen)), ("求圓周長", s2(seen)), ("由圓周長求直徑和半徑", s3(seen)),
            ("半圓和扇形的弧長", s4(seen)), ("應用", s5(seen))]
    body = lesson(
        ["任何圓的 <b>圓周長 ÷ 直徑</b> 都約是 3.14，叫做<b>圓周率</b>。",
         "<b>圓周長 ＝ 直徑 × 3.14 ＝ 半徑 × 2 × 3.14</b>；反過來，直徑 ＝ 圓周長 ÷ 3.14。",
         "扇形的弧長 ＝ 圓周長 × 圓心角 ÷ 360。半圓的周長要再加上直徑。"],
        [example("半徑 5 公分的圓，圓周長是多少？", ["5 × 2 × 3.14 ＝ 31.4。"], "31.4 公分"),
         example("直徑 10 公分的半圓，周長（含直徑）是多少？", ["弧長 10 × 3.14 ÷ 2 ＝ 15.7。", "15.7 ＋ 10 ＝ 25.7。"], "25.7 公分")],
        [("半徑 × 3.14 就是圓周長", "要先乘以 2（變成直徑）"),
         ("半圓周長只算弧長", "還要加上直徑"),
         ("把圓周長和面積公式弄混", "圓周長用直徑 × 3.14，面積用半徑 × 半徑 × 3.14")])
    faq = [{"q": "圓周率為什麼是 3.14？",
            "a": "量很多大小不同的圓，圓周長 ÷ 直徑都約是 3.14159…，所以國小計算時用 3.14。"},
           {"q": "知道圓周長，怎麼求半徑？",
            "a": "先用圓周長 ÷ 3.14 求直徑，再除以 2 就是半徑。"},
           {"q": "六年級的圓周長要學什麼？",
            "a": "108課綱 S-6-3：圓周率、圓周長、扇形弧長，知道圓心角：360 ＝ 扇形弧長：圓周長。"}]
    make_unit(R, "grade-6", "circumference", "S-6-3",
              "圓周率、圓周長、圓面積、扇形面積：用分割說明圓面積公式。求扇形弧長與面積。知道以下三個比相等：（1）圓心角：360；（2）扇形弧長：圓周長；（3）扇形面積：圓面積，但應用問題只處理用（1）求弧長或面積。",
              "圓周率與圓周長",
              "六年級數學 圓周長 練習題｜圓周率 3.14・半圓・扇形弧長 學習單（附解答）",
              "圓周長",
              "國小六年級數學「圓周率與圓周長」免費學習單：認識圓周率 3.14、求圓周長、由圓周長求直徑和半徑、半圓周長和扇形弧長與輪子、跑道等應用題。100題線上練習馬上對答案，附可列印解答。",
              "圓周長 ＝ 直徑 × 3.14",
              "半徑要先乘以 2；半圓的周長要加上直徑。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
