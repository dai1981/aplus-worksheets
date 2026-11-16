# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：弧長與扇形面積（108課綱 S-9-5）
  python3 tools/gen_tw_math_g9_arc_length_and_sector_area.py
π を使った圓周長・圓面積、弧長 2πr × θ/360、扇形面積 πr² × θ/360（＝ 弧長 × r ÷ 2）、弧長・面積から圓心角・半徑、環形・陰影部分・時計の針など。
誤答：直徑と半徑の取り違え、弧長で πr を使う、面積で 2πr を使う、扇形の周長で半徑を足し忘れる。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
from tw_g9 import pi

R = random.Random(81106)
ANG = [30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 180, 210, 240, 270, 300]


def s1(seen):
    def mk():
        r = R.randint(2, 20)
        t = R.choice(["C", "A", "Cd", "Ad"])
        d = t.endswith("d")
        given = "直徑 %d" % (2 * r) if d else "半徑 %d" % r
        if t[0] == "C":
            q = "%s 公分的圓，圓周長是多少公分？" % given
            return mcq(q, pi(2 * r), [pi(r * r), pi(4 * r), pi(r), pi(2 * r + 1)], "圓周長 ＝ 2πr ＝ 2 × π × %d ＝ %s。" % (r, pi(2 * r)))
        q = "%s 公分的圓，面積是多少平方公分？" % given
        return mcq(q, pi(r * r), [pi(2 * r), pi(4 * r * r), pi(2 * r * r), pi(r * r + 1)], "面積 ＝ πr<sup>2</sup> ＝ π × %d<sup>2</sup> ＝ %s。" % (r, pi(r * r)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        r = R.randint(2, 18)
        a = R.choice(ANG)
        L = F(2 * r * a, 360)
        q = "半徑 %d 公分、圓心角 %d° 的扇形，弧長是多少公分？" % (r, a)
        return mcq(q, pi(L), [pi(F(r * a, 360)), pi(F(r * r * a, 360)), pi(L * 2), pi(F(2 * r * (360 - a), 360)), pi(L + 1)], "弧長 ＝ 2πr × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ 2π × %d × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ %s。" % (a, r, a, pi(L)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        r = R.randint(2, 18)
        a = R.choice(ANG)
        A = F(r * r * a, 360)
        q = "半徑 %d 公分、圓心角 %d° 的扇形，面積是多少平方公分？" % (r, a)
        return mcq(q, pi(A), [pi(F(2 * r * a, 360)), pi(A * 2), pi(F(r * a, 360)), pi(F(r * r * (360 - a), 360)), pi(A + 1)], "扇形面積 ＝ πr<sup>2</sup> × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ π × %d × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ %s。" % (a, r * r, a, pi(A)))

    def arc_area():
        r = R.randint(2, 16)
        L = R.randint(1, 3 * r)
        A = F(L * r, 2)
        q = "扇形的半徑 %d 公分，弧長 %s 公分，面積是多少平方公分？" % (r, pi(L))
        return mcq(q, pi(A), [pi(L * r), pi(F(L, 2)), pi(F(L * r * r, 2)), pi(A + 1)], "扇形面積 ＝ 弧長 × 半徑 ÷ 2 ＝ %s × %d ÷ 2 ＝ %s。" % (pi(L), r, pi(A)))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, arc_area, 6, seen)


def s4(seen):
    def ang_from_arc():
        r = R.randint(2, 18)
        a = R.choice(ANG)
        L = F(2 * r * a, 360)
        q = "半徑 %d 公分的扇形，弧長 %s 公分，圓心角是多少度？" % (r, pi(L))
        w = [x for x in (a * 2, a // 2 if a % 2 == 0 else a + 30, 360 - a) if x != a]
        return mcq(q, "%d°" % a, ["%d°" % x for x in w], "弧長占圓周的比 ＝ 圓心角 ÷ 360°：360° × %s ÷ %s ＝ %d°。" % (pi(L), pi(2 * r), a))

    def r_from_area():
        r = R.randint(2, 15)
        a = R.choice([90, 120, 180, 60, 45, 270])
        A = F(r * r * a, 360)
        q = "圓心角 %d° 的扇形，面積是 %s 平方公分，半徑是多少公分？" % (a, pi(A))
        return mcq(q, "%d 公分" % r, ["%d 公分" % x for x in (r * r, 2 * r, r + 1)], "π × r<sup>2</sup> × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ %s，r<sup>2</sup> ＝ %d，r ＝ %d。" % (a, pi(A), r * r, r))

    def perim():
        r = R.randint(3, 15)
        a = R.choice([60, 90, 120, 180])
        L = F(2 * r * a, 360)
        q = "半徑 %d 公分、圓心角 %d° 的扇形，周長是多少公分？" % (r, a)
        ans = "%s ＋ %d" % (pi(L), 2 * r)
        return mcq(q, ans, [pi(L), "%s ＋ %d" % (pi(L), r), "%s ＋ %d" % (pi(L * 2), 2 * r)], "扇形周長 ＝ 弧長 ＋ 2 個半徑 ＝ %s ＋ 2 × %d。" % (pi(L), r))
    return pick_unique(R, ang_from_arc, 7, seen) + pick_unique(R, r_from_area, 7, seen) + pick_unique(R, perim, 6, seen)


def s5(seen):
    def ring():
        a, b = sorted(R.sample(range(2, 15), 2))
        q = "兩個同心圓的半徑分別是 %d 公分和 %d 公分，中間環形的面積是多少平方公分？" % (a, b)
        return mcq(q, pi(b * b - a * a), [pi((b - a) ** 2), pi(2 * (b - a)), pi(b * b + a * a), pi(b * b - a * a + 1)], "大圓 － 小圓 ＝ π × %d<sup>2</sup> － π × %d<sup>2</sup> ＝ %s。" % (b, a, pi(b * b - a * a)))

    def corner():
        s_ = R.randint(2, 14) * 2
        q = "邊長 %d 公分的正方形，以一個頂點為圓心、邊長為半徑畫四分之一圓。正方形中不在扇形內的部分面積是多少？" % s_
        ans = "%d － %s" % (s_ * s_, pi(F(s_ * s_, 4)))
        return mcq(q, ans, ["%d － %s" % (s_ * s_, pi(s_ * s_)), "%d － %s" % (s_ * s_, pi(F(s_, 2))), pi(F(s_ * s_, 4))], "正方形 %d － 四分之一圓 %s。" % (s_ * s_, pi(F(s_ * s_, 4))))

    def clock():
        L = R.choice([6, 8, 9, 10, 12, 15])
        m = R.choice([10, 15, 20, 30, 40, 45])
        a = m * 6
        q = "時鐘的分針長 %d 公分，經過 %d 分鐘，分針尖端走過的弧長是多少公分？" % (L, m)
        Lp = F(2 * L * a, 360)
        return mcq(q, pi(Lp), [pi(F(L * L * a, 360)), pi(F(2 * L * m, 360)), pi(Lp * 2), pi(Lp + 1)], "分針每分鐘轉 6°，%d 分鐘轉 %d°：2π × %d × <span class='fr'><span class='fn'>%d</span><span class='fd'>360</span></span> ＝ %s。" % (m, a, L, a, pi(Lp)))
    return pick_unique(R, ring, 8, seen) + pick_unique(R, corner, 6, seen) + pick_unique(R, clock, 6, seen)


def main():
    seen = set()
    F_ = lambda a, b: "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)
    sets = [("圓周長與圓面積", s1(seen)), ("弧長", s2(seen)), ("扇形面積", s3(seen)),
            ("由弧長、面積求圓心角和半徑", s4(seen)), ("複合圖形與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["用 <b>π</b> 表示圓周率：圓周長 ＝ 2πr，圓面積 ＝ πr<sup>2</sup>。",
         "圓心角 θ° 的扇形占整個圓的 %s：<b>弧長 ＝ 2πr × %s</b>，<b>扇形面積 ＝ πr<sup>2</sup> × %s</b>。" % (F_("θ", "360"), F_("θ", "360"), F_("θ", "360")),
         "扇形面積也等於 弧長 × 半徑 ÷ 2；扇形周長 ＝ 弧長 ＋ 2 個半徑。"],
        [example("半徑 6、圓心角 120° 的扇形", ["弧長 2π × 6 × %s ＝ 4π。" % F_(1, 3), "面積 π × 36 × %s ＝ 12π。" % F_(1, 3)], "4π、12π"),
         example("半徑 10、弧長 5π 的扇形面積", ["5π × 10 ÷ 2。"], "25π")],
        [("弧長用 πr × %s" % F_("θ", "360"), "圓周長是 2πr"),
         ("直徑 10 的圓面積 100π", "半徑是 5，面積 25π"),
         ("扇形周長只算弧長", "還要加兩個半徑")])
    faq = [{"q": "答案為什麼保留 π？",
            "a": "π 是無限不循環小數，保留 π 最準確；題目給 π ≈ 3.14 時才算成小數。"},
           {"q": "扇形面積為什麼等於弧長 × 半徑 ÷ 2？",
            "a": "πr² × θ/360 ＝（2πr × θ/360）× r ÷ 2，也就是弧長 × 半徑 ÷ 2，像一個底是弧長、高是半徑的三角形。"},
           {"q": "九年級的弧長與扇形面積要學什麼？",
            "a": "108課綱 S-9-5：以 π 表示圓周率，弧、弦、圓心角、扇形的意義，圓周長、圓面積、扇形弧長與面積的公式。"}]
    make_unit(R, "grade-9", "arc-length-and-sector-area", "S-9-5",
              "圓弧長與扇形面積：以 π 表示圓周率；弧、弦、圓心角、扇形的意義；圓周長與圓面積的計算公式；扇形弧長與面積的計算公式。",
              "弧長與扇形面積",
              "九年級數學 弧長與扇形面積 練習題｜圓心角・π・扇形周長 學習單（附解答）",
              "弧長與扇形面積",
              "國中九年級數學「弧長與扇形面積」免費學習單：用 π 算圓周長和圓面積、扇形弧長與面積公式、由弧長或面積求圓心角和半徑、環形、陰影面積與時鐘分針應用題。100題線上練習馬上對答案，附可列印解答。",
              "弧長 ＝ 2πr × %s，面積 ＝ πr<sup>2</sup> × %s" % (F_("θ", "360"), F_("θ", "360")),
              "扇形面積 ＝ 弧長 × 半徑 ÷ 2。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
