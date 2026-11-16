# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：扇形（108課綱 S-5-3）
  python3 tools/gen_tw_math_g5_sectors.py
扇形の定義・圓心角、圓心角⇔幾分之幾圓、図から圓心角を読む、扇形かどうかの判定、應用（披薩・時鐘・圓形圖）。
誤答：圓心角 90 度を 1/9 圓とする、360 でなく 180 で割る、弧だけ・半径だけの図形を扇形とする。
"""
import math
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fig, svg_wrap, text, GREEN, FILL, INK, fr, ff

R = random.Random(51019)
NM = Names(R)
LET = "甲乙丙丁"


def sector_body(cx, cy, r, a0, deg, fill=FILL):
    a1 = a0 + deg
    x0, y0 = cx + r * math.cos(math.radians(-a0)), cy + r * math.sin(math.radians(-a0))
    x1, y1 = cx + r * math.cos(math.radians(-a1)), cy + r * math.sin(math.radians(-a1))
    large = 1 if deg > 180 else 0
    return "<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2.5'/>" % (cx, cy, x0, y0, r, r, large, x1, y1, fill, GREEN)


def sector_svg(deg, show_circle=True):
    cx, cy, r = 90, 90, 75
    s = ""
    if show_circle:
        s += "<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#bbb' stroke-width='1.5' stroke-dasharray='4 4'/>" % (cx, cy, r)
    s += sector_body(cx, cy, r, R.choice([0, 30, 90, 200]), deg)
    s += "<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, INK)
    return fig(svg_wrap(180, 180, s, "扇形"))


def s1(seen):
    def mk():
        d = R.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        a = R.randint(1, d - 1)
        if F(a, d).denominator != d:
            return None
        deg = 360 * a // d
        if R.random() < .5:
            return mcq("%s 圓的扇形，圓心角是幾度？" % fr(a, d), "%d 度" % deg, ["%d 度" % x for x in (180 * a // d if 180 * a // d != deg else deg + 30, 100 * a // d, deg + 10, 360 - deg) if x != deg and x > 0],
                       "一整個圓是 360 度：360 × %s ＝ %d（度）。" % (fr(a, d), deg))
        return mcq("圓心角 %d 度的扇形，是幾分之幾圓？" % deg, ff(F(deg, 360)), [ff(F(deg, 180)) if deg < 180 else ff(F(360 - deg, 360)), fr(1, deg // 10) if deg % 10 == 0 and deg // 10 > 1 else ff(F(deg, 360) + F(1, 12)), ff(F(deg, 100)) if deg < 100 else ff(F(deg, 720))],
                   "%d ÷ 360 ＝ %s，是 %s 圓。" % (deg, fr(deg, 360), ff(F(deg, 360))))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        deg = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300])
        q = "這個扇形是幾分之幾圓？（虛線是整個圓）" + sector_svg(deg)
        v = F(deg, 360)
        return mcq(q, ff(v), [ff(F(360 - deg, 360)) if deg != 180 else fr(1, 3), ff(v + F(1, 12)), ff(v - F(1, 12)) if v > F(1, 12) else ff(v + F(1, 6))],
                   "圓心角 %d 度，%d ÷ 360 ＝ %s。" % (deg, deg, ff(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    FACTS = [("扇形是由什麼圍成的？", "兩條半徑和一段圓周（弧）", ["兩條直徑", "三條直線", "一條半徑和一條直徑"], "從圓心畫兩條半徑，和它們之間的圓周，圍成扇形。"),
             ("扇形的兩條半徑所夾的角叫做什麼？", "圓心角", ["直角", "頂角", "平角"], "兩條半徑在圓心形成的角，叫做圓心角。"),
             ("圓心角是 180 度的扇形是什麼？", "半圓", ["四分之一圓", "整個圓", "不是扇形"], "180 度是一半，就是半圓。"),
             ("圓心角是 360 度的扇形是什麼？", "整個圓", ["半圓", "四分之一圓", "不是扇形"], "360 度轉一整圈，就是整個圓。"),
             ("兩個扇形的半徑一樣長，圓心角比較大的扇形怎樣？", "比較大", ["比較小", "一樣大", "不能比較"], "半徑相同時，圓心角越大，扇形越大。"),
             ("畫一個圓心角 60 度的扇形，要用哪兩種工具？", "圓規和量角器", ["直尺和三角板", "只要直尺", "只要圓規"], "用圓規畫圓周，用量角器量出 60 度的圓心角。")]
    out = [mcq(*f) for f in FACTS]
    for o in out:
        seen.add(o["q"])

    def same():
        d1 = R.choice([2, 3, 4, 6, 8])
        a = R.randint(1, d1 - 1)
        k = R.choice([2, 3])
        if F(a, d1).denominator != d1:
            return None
        q = "%s 圓的扇形和 %s 圓的扇形（半徑一樣），哪一個大？" % (fr(a, d1), fr(a * k, d1 * k))
        return mcq(q, "一樣大", ["%s 圓的大" % fr(a, d1), "%s 圓的大" % fr(a * k, d1 * k), "不能比較"], "%s ＝ %s，圓心角都是 %d 度，一樣大。" % (fr(a, d1), fr(a * k, d1 * k), 360 * a // d1))
    return out + pick_unique(R, same, 14, seen)


def s4(seen):
    def cut():
        n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
        q = "把一個圓平分成 %d 個一樣大的扇形，每個扇形的圓心角是幾度？" % n
        v = 360 // n
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (180 // n if 180 // n != v else v + 10, 100 // n if 100 // n else v + 5, 360 - v)], "360 ÷ %d ＝ %d（度）。" % (n, v))

    def left():
        a, b = R.choice([30, 45, 60, 90, 120]), R.choice([45, 60, 90, 150])
        if a + b >= 360:
            return None
        q = "從一個圓剪下圓心角 %d 度和 %d 度的兩個扇形，剩下的扇形圓心角是幾度？是幾分之幾圓？" % (a, b)
        v = 360 - a - b
        return mcq(q, "%d 度，%s 圓" % (v, ff(F(v, 360))), ["%d 度，%s 圓" % (180 - a - b if a + b < 180 else v + 30, ff(F(abs(180 - a - b) or 30, 360))), "%d 度，%s 圓" % (v, ff(F(v, 180)) if v < 180 else ff(F(v, 720))), "%d 度，%s 圓" % (a + b, ff(F(a + b, 360)))],
                   "360 － %d － %d ＝ %d（度），%d ÷ 360 ＝ %s。" % (a, b, v, v, ff(F(v, 360))))
    return pick_unique(R, cut, 8, seen) + pick_unique(R, left, 12, seen)


def s5(seen):
    def pizza():
        n = R.choice([6, 8, 10, 12])
        k = R.randint(1, n - 1)
        who = NM.next()
        q = "一個披薩平分成 %d 片，%s吃了 %d 片，吃掉的部分是圓心角幾度的扇形？" % (n, who, k)
        v = 360 * k // n
        if (360 * k) % n:
            return None
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (360 // n, 180 * k // n if 180 * k // n != v else v + 15, 360 - v)], "每片 360 ÷ %d ＝ %d 度，%d 片 %d × %d ＝ %d（度）。" % (n, 360 // n, k, 360 // n, k, v))

    def clock():
        m = R.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        q = "分針轉了 %d 分鐘，掃過的部分是幾分之幾圓的扇形？" % m
        v = F(m, 60)
        return mcq(q, ff(v), [ff(F(m, 100)), ff(F(m, 12)) if m < 12 else ff(F(60 - m, 60)), ff(v + F(1, 12))], "分針 60 分鐘轉一圈，%d 分鐘是 %s ＝ %s 圓。" % (m, fr(m, 60), ff(v)))

    def chart():
        p = R.choice([10, 20, 25, 30, 40, 50, 60, 75])
        q = "圓形圖中，喜歡打籃球的人佔 %d%%，這一塊扇形的圓心角是幾度？" % p
        v = 360 * p // 100
        return mcq(q, "%d 度" % v, ["%d 度" % x for x in (p, 180 * p // 100, v + 10)], "360 × %d%% ＝ 360 × %s ＝ %d（度）。" % (p, fr(p, 100), v))
    return pick_unique(R, pizza, 7, seen) + pick_unique(R, clock, 7, seen) + pick_unique(R, chart, 6, seen)


def main():
    seen = set()
    sets = [("圓心角和幾分之幾圓", s1(seen)), ("看圖說扇形", s2(seen)), ("認識扇形", s3(seen)), ("算圓心角", s4(seen)), ("生活中的扇形", s5(seen))]
    body = lesson(
        ["由<b>兩條半徑</b>和它們之間的<b>一段圓周</b>圍成的圖形叫<b>扇形</b>。兩條半徑夾的角叫<b>圓心角</b>。",
         "一整個圓的圓心角是 360 度：圓心角 90 度是 %s 圓，180 度是 %s 圓（半圓）。" % (fr(1, 4), fr(1, 2)),
         "幾分之幾圓 → 圓心角：360 × 幾分之幾；圓心角 → 幾分之幾圓：圓心角 ÷ 360。"],
        [example("%s 圓的圓心角是幾度？" % fr(3, 8), ["360 × %s ＝ 135。" % fr(3, 8)], "135 度"),
         example("圓心角 120 度是幾分之幾圓？", ["120 ÷ 360 ＝ %s。" % fr(1, 3)], "%s 圓" % fr(1, 3))],
        [("圓心角 90 度是 %s 圓" % fr(1, 9), "90 ÷ 360 ＝ %s 圓" % fr(1, 4)),
         ("用 180 度去算幾分之幾圓", "一整圈是 360 度"),
         ("只有一條半徑和弧也是扇形", "要兩條半徑和一段圓周")])
    faq = [{"q": "什麼是扇形和圓心角？",
            "a": "從圓心畫兩條半徑，和它們之間的一段圓周圍成的圖形是扇形；兩條半徑夾的角是圓心角。"},
           {"q": "圓心角和幾分之幾圓怎麼換？",
            "a": "整圓是 360 度。幾分之幾圓 × 360 ＝ 圓心角；圓心角 ÷ 360 ＝ 幾分之幾圓。例如 90 度是 1/4 圓。"},
           {"q": "五年級的扇形要學什麼？",
            "a": "108課綱 S-5-3：扇形的定義和圓心角，把扇形看成圓的一部分（幾分之幾圓），並能畫出指定的扇形。"}]
    make_unit(R, "grade-5", "sectors", "S-5-3",
              "扇形：扇形的定義。「圓心角」。扇形可視為圓的一部分。將扇形與分數結合（幾分之幾圓）。能畫出指定扇形。",
              "扇形與圓心角",
              "五年級數學 扇形 練習題｜圓心角・幾分之幾圓 學習單（附解答）",
              "扇形與圓心角",
              "國小五年級數學「扇形」免費學習單：圓心角和幾分之幾圓的換算、看圖說扇形、認識扇形、算圓心角和披薩、時鐘、圓形圖中的扇形。100題線上練習馬上對答案，附可列印解答。",
              "整個圓的圓心角是 360 度",
              "圓心角 ÷ 360 ＝ 幾分之幾圓。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
