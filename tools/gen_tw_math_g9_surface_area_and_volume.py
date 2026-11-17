# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：柱體與錐體的表面積和體積（108課綱 S-9-13）
  python3 tools/gen_tw_math_g9_surface_area_and_volume.py
直角柱の體積（底面積 × 高）、直角柱の表面積（2 × 底面積 ＋ 底周長 × 高）、正四角錐の表面積（斜高・高から畢氏定理）、直圓錐の展開圖（扇形の圓心角 360 × r/l）と表面積 πr² ＋ πrl、展開圖。
誤答：表面積で底面を一つしか數えない、錐の側面に高を使う（斜高を使わない）、扇形の半徑を底面半徑にする。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, num
from tw_g7 import tidy_sets
from tw_g9 import pi

R = random.Random(81118)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25)]


def s1(seen):
    def tri():
        a, b, c = R.choice(TRIP)
        h = R.randint(3, 20)
        V = a * b // 2 * h if a * b % 2 == 0 else None
        if V is None:
            return None
        q = "直三角柱的底面是兩股 %d 公分、%d 公分的直角三角形，柱高 %d 公分，體積是多少立方公分？" % (a, b, h)
        return mcq(q, "%s 立方公分" % num(V), ["%s 立方公分" % num(x) for x in (a * b * h, V // 3 if V % 3 == 0 else V + h, (a + b + c) * h)], "體積 ＝ 底面積 × 高 ＝ %d × %d ÷ 2 × %d ＝ %s。" % (a, b, h, num(V)))

    def trap():
        a, b, hh = R.randint(2, 10), R.randint(4, 16), R.randint(2, 10)
        if a >= b or (a + b) * hh % 2:
            return None
        H = R.randint(3, 15)
        B = (a + b) * hh // 2
        q = "直四角柱的底面是上底 %d、下底 %d、高 %d 的梯形，柱高 %d，體積是多少？" % (a, b, hh, H)
        return mcq(q, num(B * H), [num(x) for x in ((a + b) * hh * H, B + H, a * b * hh * H // 2 if a * b * hh * H % 2 == 0 else B * H + H)], "底面積（%d ＋ %d）× %d ÷ 2 ＝ %d，體積 %d × %d ＝ %s。" % (a, b, hh, B, B, H, num(B * H)))
    return pick_unique(R, tri, 10, seen) + pick_unique(R, trap, 10, seen)


def s2(seen):
    def box():
        a, b, c = R.randint(2, 12), R.randint(2, 12), R.randint(2, 12)
        if len({a, b, c}) < 3:
            return None
        a, b = max(a, b), min(a, b)
        S = 2 * (a * b + b * c + a * c)
        q = "長 %d、寬 %d、高 %d 的長方體，表面積是多少？" % (a, b, c)
        return mcq(q, num(S), [num(x) for x in (a * b + b * c + a * c, a * b * c, S - 2 * a * b)], "表面積 ＝ 2 ×（%d × %d ＋ %d × %d ＋ %d × %d）＝ %s。" % (a, b, b, c, a, c, num(S)))

    def tri():
        a, b, c = R.choice(TRIP)
        h = R.randint(3, 20)
        if a * b % 2:
            return None
        B = a * b // 2
        S = 2 * B + (a + b + c) * h
        q = "直三角柱的底面是邊長 %d、%d、%d 的直角三角形，柱高 %d，表面積是多少？" % (a, b, c, h)
        return mcq(q, num(S), [num(x) for x in (B + (a + b + c) * h, 2 * B + (a + b) * h, 2 * a * b + (a + b + c) * h)], "兩個底面 2 × %d ＝ %d，側面 ＝ 底周長 × 高 ＝ %d × %d ＝ %d，共 %s。" % (B, 2 * B, a + b + c, h, (a + b + c) * h, num(S)))
    return pick_unique(R, box, 10, seen) + pick_unique(R, tri, 10, seen)


def s3(seen):
    def slant():
        a = R.randint(2, 12) * 2
        l = R.randint(a // 2 + 1, a + 10)
        S = a * a + 2 * a * l
        q = "正四角錐的底面邊長 %d，側面三角形的高（斜高）是 %d，表面積是多少？" % (a, l)
        return mcq(q, num(S), [num(x) for x in (a * a + 4 * a * l, 2 * a * l, a * a + a * l)], "底面 %d<sup>2</sup> ＝ %d，4 個側面 4 × %d × %d ÷ 2 ＝ %d，共 %s。" % (a, a * a, a, l, 2 * a * l, num(S)))

    def height():
        tr = R.choice(TRIP)
        hf, h, l = tr
        if R.random() < .5:
            hf, h = h, hf
        a = 2 * hf
        S = a * a + 2 * a * l
        q = "正四角錐的底面邊長 %d，錐高 %d，表面積是多少？" % (a, h)
        return mcq(q, num(S), [num(x) for x in (a * a + 2 * a * h, a * a + 4 * a * l, 2 * a * l)], "斜高 ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d（錐高、底邊一半、斜高是直角三角形），表面積 %d ＋ 4 × %d × %d ÷ 2 ＝ %s。" % (h, hf, l, a * a, a, l, num(S)))
    return pick_unique(R, slant, 10, seen) + pick_unique(R, height, 10, seen)


def s4(seen):
    def ang():
        r = R.randint(1, 10)
        l = R.choice([x for x in range(r + 1, 25) if (360 * r) % x == 0])
        a = 360 * r // l
        q = "直圓錐的底面半徑 %d，母線長 %d，側面展開成扇形，扇形的圓心角是多少度？" % (r, l)
        return mcq(q, "%d°" % a, ["%d°" % x for x in (360 * l // r if 360 * l // r < 360 and 360 * l % r == 0 and 360 * l // r != a else 360 - a, 360 - a if 360 - a != a else a // 2, r * 36 if r * 36 != a else a + 30) if x != a] + ["%d°" % (a + 10)], "扇形的弧長 ＝ 底面圓周長：2π × %d ＝ 2π × %d × <span class='fr'><span class='fn'>θ</span><span class='fd'>360</span></span>，θ ＝ 360° × %d ÷ %d ＝ %d°。" % (r, l, r, l, a))

    def area():
        r = R.randint(1, 10)
        l = R.randint(r + 1, 20)
        q = "直圓錐的底面半徑 %d，母線長 %d，表面積是多少？" % (r, l)
        A = r * r + r * l
        return mcq(q, pi(A), [pi(r * l), pi(r * r + 2 * r * l), pi(2 * r * r + r * l)], "底面 πr<sup>2</sup> ＝ %s，側面 πrl ＝ %s，共 %s。" % (pi(r * r), pi(r * l), pi(A)))

    def lat():
        tr = R.choice(TRIP)
        r, h, l = tr if R.random() < .5 else (tr[1], tr[0], tr[2])
        q = "直圓錐的底面半徑 %d，高 %d，側面積是多少？" % (r, h)
        return mcq(q, pi(r * l), [pi(r * h), pi(r * r + r * l), pi(2 * r * l)], "母線 ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d，側面積 ＝ πrl ＝ %s。" % (r, h, l, pi(r * l)))
    return pick_unique(R, ang, 7, seen) + pick_unique(R, area, 7, seen) + pick_unique(R, lat, 6, seen)


def s5(seen):
    FACTS = [("n 角柱有幾個面？", "n ＋ 2 個", ["n 個", "n ＋ 1 個", "2n 個"], "n 個側面 ＋ 2 個底面。"),
             ("n 角錐有幾個面？", "n ＋ 1 個", ["n 個", "n ＋ 2 個", "2n 個"], "n 個側面 ＋ 1 個底面。"),
             ("n 角柱有幾條稜？", "3n 條", ["2n 條", "n ＋ 2 條", "n 條"], "上、下底各 n 條，側稜 n 條，共 3n 條。"),
             ("n 角錐有幾條稜？", "2n 條", ["3n 條", "n ＋ 1 條", "n 條"], "底面 n 條 ＋ 側稜 n 條。"),
             ("n 角錐有幾個頂點？", "n ＋ 1 個", ["n 個", "2n 個", "n ＋ 2 個"], "底面 n 個 ＋ 錐頂 1 個。"),
             ("直圓錐的側面展開圖是什麼形狀？", "扇形", ["長方形", "三角形", "圓形"], "直圓錐的側面展開是扇形，扇形半徑是母線長。"),
             ("正四角錐的展開圖由哪些圖形組成？", "1 個正方形和 4 個全等的等腰三角形", ["2 個正方形和 4 個長方形", "1 個正方形和 4 個長方形", "4 個正三角形"], "底面是正方形，側面是 4 個全等的等腰三角形。"),
             ("直角柱的側面展開成什麼形狀？", "長方形", ["扇形", "三角形", "梯形"], "直角柱的側面展開是一個長方形，長是底面周長，寬是柱高。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def tent():
        a = R.randint(2, 6)
        l = R.randint(a // 2 + 2, a + 4)
        q = "一個正四角錐形的帳篷（沒有底），底面邊長 %d 公尺，斜高 %d 公尺，需要多少平方公尺的布？" % (a, l)
        A = 2 * a * l
        return mcq(q, "%d 平方公尺" % A, ["%d 平方公尺" % x for x in (A + a * a, 4 * a * l, a * l)], "只要 4 個側面：4 × %d × %d ÷ 2 ＝ %d。" % (a, l, A))

    def tank():
        a, b, h = R.randint(3, 12) * 10, R.randint(3, 10) * 10, R.randint(2, 8) * 10
        V = a * b * h
        q = "長 %d 公分、寬 %d 公分、高 %d 公分的水箱，可以裝多少公升的水？（1 公升 ＝ 1000 立方公分）" % (a, b, h)
        return mcq(q, "%s 公升" % num(V // 1000), ["%s 公升" % num(x) for x in (V, V // 100, 2 * (a * b + b * h + a * h) // 1000 or 1)], "%d × %d × %d ＝ %s 立方公分 ＝ %s 公升。" % (a, b, h, num(V), num(V // 1000)))
    return out + pick_unique(R, tent, 6, seen) + pick_unique(R, tank, 6, seen)


def main():
    seen = set()
    sets = [("直角柱的體積", s1(seen)), ("直角柱的表面積", s2(seen)), ("正四角錐的表面積", s3(seen)),
            ("直圓錐的展開圖與表面積", s4(seen)), ("展開圖與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>直角柱體積 ＝ 底面積 × 高</b>；<b>表面積 ＝ 2 × 底面積 ＋ 底面周長 × 高</b>。",
         "<b>正角錐表面積 ＝ 底面積 ＋ 側面的三角形面積</b>，三角形的高是<b>斜高</b>，不是錐高；錐高、底邊一半、斜高形成直角三角形。",
         "<b>直圓錐</b>的側面展開是扇形：半徑是母線長 l，弧長是底面圓周 2πr，圓心角 ＝ 360° × r ÷ l。表面積 ＝ πr<sup>2</sup> ＋ πrl。"],
        [example("底面邊長 6、錐高 4 的正四角錐表面積", ["斜高 √（4<sup>2</sup> ＋ 3<sup>2</sup>）＝ 5。", "36 ＋ 4 × 6 × 5 ÷ 2。"], "96"),
         example("半徑 3、母線 5 的直圓錐", ["圓心角 360° × 3 ÷ 5 ＝ 216°。", "表面積 9π ＋ 15π。"], "216°、24π")],
        [("直角柱表面積只算一個底面", "上下兩個底面都要算"),
         ("角錐側面用錐高算", "要用斜高（側面三角形的高）"),
         ("圓錐展開的扇形半徑 ＝ 底面半徑", "扇形半徑是母線長")])
    faq = [{"q": "斜高和錐高有什麼不同？",
            "a": "錐高是錐頂到底面的垂直距離；斜高是側面三角形的高。兩者和底邊的一半形成直角三角形，可以用畢氏定理互求。"},
           {"q": "為什麼圓錐側面積是 πrl？",
            "a": "側面展開是半徑 l、弧長 2πr 的扇形，扇形面積 ＝ 弧長 × 半徑 ÷ 2 ＝ 2πr × l ÷ 2 ＝ πrl。"},
           {"q": "九年級的表面積和體積要學什麼？",
            "a": "108課綱 S-9-13：直角柱、直圓錐、正角錐的展開圖和表面積，以及直角柱的體積。"}]
    make_unit(R, "grade-9", "surface-area-and-volume", "S-9-13",
              "表面積與體積：直角柱、直圓錐、正角錐的展開圖；直角柱、直圓錐、正角錐的表面積；直角柱的體積。",
              "柱體與錐體的表面積和體積",
              "九年級數學 表面積與體積 練習題｜直角柱・正四角錐・直圓錐 學習單（附解答）",
              "表面積與體積",
              "國中九年級數學「柱體與錐體的表面積和體積」免費學習單：直角柱的體積和表面積、正四角錐的表面積與斜高、直圓錐的展開扇形和表面積、角柱角錐的面稜頂點、帳篷與水箱應用題。100題線上練習馬上對答案，附可列印解答。",
              "直角柱體積 ＝ 底面積 × 高",
              "錐體側面用斜高；圓錐表面積 ＝ πr<sup>2</sup> ＋ πrl。",
              body, faq, sets, 18)


if __name__ == "__main__":
    main()
