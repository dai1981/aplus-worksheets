# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：圓心角與圓周角（108課綱 S-9-6）
  python3 tools/gen_tw_math_g9_inscribed_angles.py
圓心角＝所對弧の度數、圓周角＝所對弧の度數の一半、同弧の圓周角は等しい、直徑の圓周角は 90°、圓內接四邊形の對角互補、弧の比から三角形の內角。
誤答：圓周角を弧の度數と同じにする、圓心角を圓周角の半分にする、對角を等しいとする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
from tw_g9 import ov

R = random.Random(81108)


def arc(s):
    return "<span class='ov' style=''>%s</span>" % s if False else "弧 %s" % s


def s1(seen):
    def mk():
        a = R.randrange(20, 341, 2)
        if a == 180:
            return None
        t = R.choice(["c", "i"])
        if t == "c":
            q = "圓 O 中，%s（劣弧）的度數是 %d°，圓心角 ∠AOB 是多少度？" % (arc("AB"), a) if a < 180 else "圓 O 中，%s（優弧）的度數是 %d°，劣弧 AB 所對的圓心角 ∠AOB 是多少度？" % (arc("ACB"), a)
            v = a if a < 180 else 360 - a
            return mcq(q, "%d°" % v, ["%d°" % x for x in (v // 2, 360 - v, v * 2 if v * 2 < 360 else v + 20)], ("圓心角的度數 ＝ 所對弧的度數：%d°。" % v) if a < 180 else "劣弧 ＝ 360° － %d° ＝ %d°，圓心角等於它：%d°。" % (a, v, v))
        if a >= 180:
            return None
        q = "圓 O 中，%s 的度數是 %d°，C 在優弧上，圓周角 ∠ACB 是多少度？" % (arc("AB"), a)
        return mcq(q, "%d°" % (a // 2), ["%d°" % x for x in (a, 180 - a // 2, a * 2 if a * 2 < 360 else a + 10)], "圓周角 ＝ 所對弧度數的一半：%d° ÷ 2 ＝ %d°。" % (a, a // 2))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        c = R.randrange(20, 171, 2)
        t = R.choice(["c2i", "i2c"])
        if t == "c2i":
            q = "圓 O 中，圓心角 ∠AOB ＝ %d°，C 在優弧 AB 上，∠ACB 是多少度？" % c
            return mcq(q, "%d°" % (c // 2), ["%d°" % x for x in (c, 2 * c if 2 * c < 360 else c + 10, 180 - c // 2)], "∠ACB 和 ∠AOB 對同一段弧，圓周角是圓心角的一半：%d°。" % (c // 2))
        i = c // 2
        q = "圓 O 中，圓周角 ∠ACB ＝ %d°，同弧所對的圓心角 ∠AOB 是多少度？" % i
        return mcq(q, "%d°" % (2 * i), ["%d°" % x for x in (i, i // 2 if i % 2 == 0 else i + 5, 180 - i)], "圓心角是同弧圓周角的 2 倍：2 × %d° ＝ %d°。" % (i, 2 * i))

    def iso():
        c = R.randrange(30, 161, 2)
        q = "圓 O 中，∠AOB ＝ %d°，∠OAB 是多少度？" % c
        v = (180 - c) // 2
        return mcq(q, "%d°" % v, ["%d°" % x for x in (c // 2, 180 - c, 90 - c // 4 if 90 - c // 4 != v else v + 5)], "%s ＝ %s（半徑），△OAB 是等腰三角形：（180° － %d°）÷ 2 ＝ %d°。" % (ov("OA"), ov("OB"), c, v))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, iso, 6, seen)


def s3(seen):
    def mk():
        a = R.randint(15, 75)
        q = "%s 是圓 O 的直徑，C 是圓上另一點，∠CAB ＝ %d°，∠CBA 是多少度？" % (ov("AB"), a)
        return mcq(q, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, a, 90 + a if 90 + a < 180 else 45)], "直徑所對的圓周角是 90°：∠ACB ＝ 90°，∠CBA ＝ 90° － %d° ＝ %d°。" % (a, 90 - a))

    def pyth():
        tr = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
        a, b, c = tr
        q = "%s 是圓 O 的直徑，C 在圓上，%s ＝ %d，%s ＝ %d，圓 O 的半徑是多少？" % (ov("AB"), ov("AC"), a, ov("BC"), b)
        r = c / 2
        rs = ("%g" % r)
        return mcq(q, rs, ["%g" % x for x in (c, a + b, (a + b) / 2)], "∠ACB ＝ 90°，%s ＝ √（%d<sup>2</sup> ＋ %d<sup>2</sup>）＝ %d，半徑 %s。" % (ov("AB"), a, b, c, rs))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, pyth, 6, seen)


def s4(seen):
    def same():
        a = R.randint(20, 80)
        q = "A、B、C、D 都在圓上，C、D 在 %s 的同一側，∠ACB ＝ %d°，∠ADB 是多少度？" % (ov("AB"), a)
        return mcq(q, "%d°" % a, ["%d°" % x for x in (2 * a, 180 - a, a // 2 if a % 2 == 0 else a + 5)], "同一段弧所對的圓周角相等：∠ADB ＝ ∠ACB ＝ %d°。" % a)

    def cyc():
        a = R.randint(50, 130)
        k = R.choice(["C", "ext"])
        if k == "C":
            q = "四邊形 ABCD 內接於圓，∠A ＝ %d°，∠C 是多少度？" % a
            return mcq(q, "%d°" % (180 - a), ["%d°" % x for x in (a, 360 - a, 90 - a // 2 if a < 180 and 90 - a // 2 != 180 - a else 45)], "圓內接四邊形的對角互補：180° － %d° ＝ %d°。" % (a, 180 - a))
        q = "四邊形 ABCD 內接於圓，延長 %s 到 E，∠DCE（∠C 的外角）＝ %d°，∠A 是多少度？" % (ov("BC"), a)
        return mcq(q, "%d°" % a, ["%d°" % x for x in (180 - a, 2 * a if 2 * a < 360 else a // 2, 90 - a // 2 if 90 - a // 2 > 0 else 30)], "∠BCD ＝ 180° － %d°，對角 ∠A ＝ 180° － ∠BCD ＝ %d°（外角等於內對角）。" % (a, a))
    return pick_unique(R, same, 6, seen) + pick_unique(R, cyc, 14, seen)


def s5(seen):
    def ratio():
        t = sorted(R.sample(range(1, 10), 3))
        if 360 % sum(t):
            return None
        k = 360 // sum(t)
        if (t[2] * k) % 2:
            return None
        q = "A、B、C 把圓周分成三段弧，弧長比 %s。△ABC 最大的內角是多少度？" % "：".join(map(str, R.sample(t, 3)))
        v = t[2] * k // 2
        return mcq(q, "%d°" % v, ["%d°" % x for x in (t[2] * k, 180 * t[2] // sum(t) if 180 * t[2] % sum(t) == 0 and 180 * t[2] // sum(t) != v else v + 10, t[0] * k // 2 if t[0] * k % 2 == 0 else v - 5)], "三段弧是 %s，最大內角對最大的弧 %d°：%d° ÷ 2 ＝ %d°。" % ("、".join("%d°" % (x * k) for x in t), t[2] * k, t[2] * k, v))

    def mixed():
        c = R.randrange(40, 161, 2)
        q = "圓 O 中，∠AOB ＝ %d°，P 在劣弧 AB 上（不是 A、B），∠APB 是多少度？" % c
        v = 180 - c // 2
        return mcq(q, "%d°" % v, ["%d°" % x for x in (c // 2, c, 360 - c)], "∠APB 對的是優弧，優弧 ＝ 360° － %d° ＝ %d°，∠APB ＝ %d° ÷ 2 ＝ %d°。" % (c, 360 - c, 360 - c, v))
    return pick_unique(R, ratio, 8, seen) + pick_unique(R, mixed, 12, seen)


def main():
    seen = set()
    sets = [("弧的度數", s1(seen)), ("圓心角與圓周角", s2(seen)), ("直徑所對的圓周角", s3(seen)),
            ("同弧與圓內接四邊形", s4(seen)), ("綜合", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>圓心角</b>：頂點在圓心的角，度數 ＝ 所對弧的度數。",
         "<b>圓周角</b>：頂點在圓上、兩邊都和圓相交的角，度數 ＝ <b>所對弧度數的一半</b>，也就是同弧圓心角的一半。",
         "同弧所對的圓周角都相等；<b>直徑所對的圓周角是 90°</b>。",
         "<b>圓內接四邊形對角互補</b>，外角等於內對角。"],
        [example("∠AOB ＝ 100°，C 在優弧上，∠ACB？", ["100° ÷ 2。"], "50°"),
         example("四邊形 ABCD 內接於圓，∠B ＝ 75°，∠D？", ["180° － 75°。"], "105°")],
        [("圓周角 ＝ 所對弧的度數", "是弧度數的一半"),
         ("圓內接四邊形對角相等", "對角互補（和 180°）"),
         ("P 在劣弧上，∠APB ＝ ∠AOB ÷ 2", "P 在劣弧上時，∠APB 對的是優弧")])
    faq = [{"q": "為什麼圓周角是圓心角的一半？",
            "a": "連圓周角頂點和圓心，會出現等腰三角形（兩邊都是半徑），用外角性質可以證明圓心角是圓周角的兩倍。"},
           {"q": "怎麼判斷圓周角對的是哪一段弧？",
            "a": "看角的兩邊夾住哪一段弧（角的開口那側），頂點在優弧上就對劣弧，頂點在劣弧上就對優弧。"},
           {"q": "九年級的圓周角要學什麼？",
            "a": "108課綱 S-9-6：圓心角、圓周角與所對弧度數的關係，圓內接四邊形對角互補，切線段等長。"}]
    make_unit(R, "grade-9", "inscribed-angles", "S-9-6",
              "圓的幾何性質：圓心角、圓周角與所對應弧的度數三者之間的關係；圓內接四邊形對角互補；切線段等長。",
              "圓心角、圓周角與圓內接四邊形",
              "九年級數學 圓周角 練習題｜圓心角・弧的度數・圓內接四邊形 學習單（附解答）",
              "圓周角",
              "國中九年級數學「圓心角、圓周角與圓內接四邊形」免費學習單：弧的度數、圓周角是圓心角的一半、直徑所對的圓周角 90°、同弧圓周角相等、圓內接四邊形對角互補。100題線上練習馬上對答案，附可列印解答。",
              "圓周角 ＝ 所對弧度數的一半",
              "直徑所對的圓周角 90°；圓內接四邊形對角互補。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
