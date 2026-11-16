# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：柱體的體積與表面積（108課綱 S-6-4）
  python3 tools/gen_tw_math_g6_volume_of_prisms_and_cylinders.py
柱體體積＝底面積×高（角柱・三角柱・梯形柱・圓柱）、圓柱の表面積（底面×2＋側面＝圓周長×高）、高さや底面積を逆算、簡單複合形體。
誤答：三角形の底面で ÷2 を忘れる、圓柱で直徑をそのまま使う、表面積で底面を 1 つしか足さない。
"""
import random
from decimal import Decimal as D
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num

R = random.Random(61013)
NM = Names(R)
PI = D("3.14")


def s_(x):
    x = D(x).normalize()
    t = format(x, "f")
    if "." in t:
        i, f = t.split(".")
        return num(int(i)) + "." + f
    return num(int(t))


def s1(seen):
    def mk():
        base = R.randint(6, 80)
        h = R.randint(3, 25)
        kind = R.choice(["五角柱", "六角柱", "四角柱", "三角柱", "八角柱"])
        q = "一個%s的底面積是 %d 平方公分，高 %d 公分。體積是多少立方公分？" % (kind, base, h)
        v = base * h
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (base + h, base * h * 2, base * h // 2 if v % 2 == 0 else v + base)], "柱體體積 ＝ 底面積 × 高：%d × %d ＝ %s（立方公分）。" % (base, h, num(v)))

    def back():
        base = R.randint(6, 60)
        h = R.randint(3, 20)
        v = base * h
        q = "一個角柱體積 %s 立方公分，底面積 %d 平方公分，高是幾公分？" % (num(v), base)
        return mcq(q, "%d 公分" % h, ["%s 公分" % num(x) for x in (v * base if v * base < 100000 else v - base, v - base, h + 2)], "高 ＝ 體積 ÷ 底面積：%s ÷ %d ＝ %d（公分）。" % (num(v), base, h))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, back, 8, seen)


def s2(seen):
    def tri():
        b, hh = R.randint(3, 16), R.randint(2, 14)
        if (b * hh) % 2:
            return None
        H = R.randint(5, 30)
        base = b * hh // 2
        v = base * H
        q = "一個三角柱，底面是底 %d 公分、高 %d 公分的三角形，柱高 %d 公分。體積是多少立方公分？" % (b, hh, H)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (b * hh * H, base + H, b * hh * H // 4 if (b * hh * H) % 4 == 0 else v + H)  if x != v], "底面積 %d × %d ÷ 2 ＝ %d，體積 %d × %d ＝ %s（立方公分）。" % (b, hh, base, base, H, num(v)))

    def trap():
        a, b, hh = R.randint(2, 10), R.randint(4, 16), R.randint(2, 10)
        if a >= b or ((a + b) * hh) % 2:
            return None
        H = R.randint(5, 20)
        base = (a + b) * hh // 2
        v = base * H
        q = "一個柱體的底面是上底 %d 公分、下底 %d 公分、高 %d 公分的梯形，柱高 %d 公分。體積是多少立方公分？" % (a, b, hh, H)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in ((a + b) * hh * H, (a + b * hh // 1) * H // 2 if ((a + b * hh) * H) % 2 == 0 else v + H, a * b * hh * H)  if x != v], "底面積（%d ＋ %d）× %d ÷ 2 ＝ %d，體積 %d × %d ＝ %s（立方公分）。" % (a, b, hh, base, base, H, num(v)))
    return pick_unique(R, tri, 12, seen) + pick_unique(R, trap, 8, seen)


def s3(seen):
    def mk():
        kind = R.choice(["r", "d"])
        r = R.randint(1, 10)
        H = R.randint(2, 20)
        v = r * r * PI * H
        given = "底面半徑 %d 公分" % r if kind == "r" else "底面直徑 %d 公分" % (2 * r)
        q = "一個圓柱%s，高 %d 公分。體積是多少立方公分？" % (given, H)
        w = [2 * r * 2 * r * PI * H if kind == "d" else 2 * r * PI * H, r * r * PI + H, r * 2 * PI * H]
        return mcq(q, "%s 立方公分" % s_(v), ["%s 立方公分" % s_(x) for x in w if x != v] + ["%s 立方公分" % s_(v * 2)],
                   "%s底面積 %d × %d × 3.14 ＝ %s，體積 %s × %d ＝ %s（立方公分）。" % ("半徑 %d，" % r if kind == "d" else "", r, r, s_(r * r * PI), s_(r * r * PI), H, s_(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def cyl():
        r = R.randint(1, 10)
        H = R.randint(2, 15)
        side = 2 * r * PI * H
        tot = 2 * r * r * PI + side
        q = "一個圓柱底面半徑 %d 公分，高 %d 公分。表面積是多少平方公分？" % (r, H)
        return mcq(q, "%s 平方公分" % s_(tot), ["%s 平方公分" % s_(x) for x in (side, r * r * PI + side, r * r * PI * H)], "兩個底面 %d × %d × 3.14 × 2 ＝ %s；側面是長方形，圓周長 × 高 ＝ %s；合計 %s（平方公分）。" % (r, r, s_(2 * r * r * PI), s_(side), s_(tot)))

    def side():
        d = R.randint(2, 20)
        H = R.randint(3, 20)
        A = d * PI * H
        q = "一個圓柱底面直徑 %d 公分，高 %d 公分。側面積是多少平方公分？" % (d, H)
        return mcq(q, "%s 平方公分" % s_(A), ["%s 平方公分" % s_(x) for x in (d * H, D(d) / 2 * PI * H, A * 2)], "側面攤開是長方形：長 ＝ 圓周長 %d × 3.14 ＝ %s，寬 ＝ 高 %d：%s × %d ＝ %s（平方公分）。" % (d, s_(d * PI), H, s_(d * PI), H, s_(A)))

    def prism():
        a, b, h = R.randint(2, 12), R.randint(2, 12), R.randint(2, 12)
        if (a * b) % 2:
            return None
        c2 = a * a + b * b
        c = int(c2 ** .5)
        if c * c != c2:
            return None
        base = a * b // 2
        S = base * 2 + (a + b + c) * h
        q = "一個三角柱，底面是兩股 %d 公分、%d 公分、斜邊 %d 公分的直角三角形，柱高 %d 公分。表面積是多少平方公分？" % (a, b, c, h)
        return mcq(q, "%s 平方公分" % num(S), ["%s 平方公分" % num(x) for x in (base + (a + b + c) * h, a * b * h // 2, a * b + (a + b) * h)], "兩個底面 %d × 2 ＝ %d，側面 周長 %d × 高 %d ＝ %d，合計 %s（平方公分）。" % (base, base * 2, a + b + c, h, (a + b + c) * h, num(S)))
    return pick_unique(R, cyl, 8, seen) + pick_unique(R, side, 8, seen) + pick_unique(R, prism, 4, seen)


def s5(seen):
    def can():
        r = R.choice([3, 4, 5])
        H = R.choice([10, 12, 15, 20])
        v = r * r * PI * H
        q = "一個圓柱形杯子，內部底面半徑 %d 公分、高 %d 公分。最多可以裝多少毫升的水？（1 立方公分 ＝ 1 毫升）" % (r, H)
        return mcq(q, "%s 毫升" % s_(v), ["%s 毫升" % s_(x) for x in (2 * r * PI * H, r * r * PI, v / 1000)], "%d × %d × 3.14 × %d ＝ %s（立方公分）＝ %s 毫升。" % (r, r, H, s_(v), s_(v)))

    def composite():
        a, b, h1 = R.randint(4, 12), R.randint(4, 12), R.randint(2, 8)
        c, h2 = R.randint(2, min(a, b) - 1), R.randint(2, 8)
        if c < 2:
            return None
        v = a * b * h1 + c * c * h2
        q = "在一個長 %d 公分、寬 %d 公分、高 %d 公分的長方體上面，放一個底面是邊長 %d 公分的正方形、高 %d 公分的四角柱。合起來體積是多少立方公分？" % (a, b, h1, c, h2)
        return mcq(q, "%s 立方公分" % num(v), ["%s 立方公分" % num(x) for x in (a * b * (h1 + h2), a * b * h1, a * b * h1 + c * h2)  if x != v], "分成兩個柱體：%d × %d × %d ＋ %d × %d × %d ＝ %s（立方公分）。" % (a, b, h1, c, c, h2, num(v)))

    def hole():
        a, h = R.choice([10, 12, 20]), R.choice([5, 8, 10])
        r = R.choice([2, 3, 4])
        v = a * a * h - r * r * PI * h
        q = "一塊底面是邊長 %d 公分正方形、高 %d 公分的四角柱木塊，從上到下挖穿一個半徑 %d 公分的圓柱孔。剩下的體積是多少立方公分？" % (a, h, r)
        return mcq(q, "%s 立方公分" % s_(v), ["%s 立方公分" % s_(x) for x in (a * a * h, r * r * PI * h, a * a * h - 2 * r * PI * h, a * a * h - r * r * PI)], "%d × %d × %d － %d × %d × 3.14 × %d ＝ %s（立方公分）。" % (a, a, h, r, r, h, s_(v)))
    return pick_unique(R, can, 7, seen) + pick_unique(R, composite, 7, seen) + pick_unique(R, hole, 6, seen)


def main():
    seen = set()
    sets = [("柱體體積 ＝ 底面積 × 高", s1(seen)), ("三角柱和梯形柱", s2(seen)), ("圓柱的體積", s3(seen)),
            ("表面積", s4(seen)), ("應用與複合形體", s5(seen))]
    body = lesson(
        ["所有柱體（角柱、圓柱）：<b>體積 ＝ 底面積 × 高</b>。先算底面積，再乘以高。",
         "圓柱：底面積 ＝ 半徑 × 半徑 × 3.14。給直徑時先除以 2。",
         "<b>表面積 ＝ 兩個底面 ＋ 側面</b>。圓柱的側面攤開是長方形：長是圓周長，寬是高。"],
        [example("底面半徑 3 公分、高 10 公分的圓柱體積？", ["底面積 3 × 3 × 3.14 ＝ 28.26。", "28.26 × 10 ＝ 282.6。"], "282.6 立方公分"),
         example("三角柱底面是底 6、高 4 的三角形，柱高 10 公分，體積？", ["底面積 6 × 4 ÷ 2 ＝ 12。", "12 × 10 ＝ 120。"], "120 立方公分")],
        [("三角柱的底面積忘了 ÷ 2", "三角形面積 ＝ 底 × 高 ÷ 2"),
         ("圓柱用直徑 × 直徑 × 3.14", "用半徑 × 半徑 × 3.14"),
         ("表面積只加一個底面", "柱體有上下兩個底面")])
    faq = [{"q": "為什麼柱體體積 ＝ 底面積 × 高？",
            "a": "柱體可以看成很多片一樣的底面一層一層疊起來，疊幾公分高就是幾層，所以體積 ＝ 底面積 × 高。"},
           {"q": "圓柱的表面積怎麼算？",
            "a": "兩個圓形底面加上側面；側面攤開是長方形，長是圓周長、寬是高。"},
           {"q": "六年級的柱體體積要學什麼？",
            "a": "108課綱 S-6-4：角柱和圓柱的體積與表面積，理解「柱體體積 ＝ 底面積 × 高」，以及簡單複合形體的體積。"}]
    make_unit(R, "grade-6", "volume-of-prisms-and-cylinders", "S-6-4",
              "柱體體積與表面積：含角柱和圓柱。利用簡單柱體，理解「柱體體積＝底面積×高」的公式。簡單複合形體體積。",
              "角柱和圓柱的體積與表面積",
              "六年級數學 柱體體積 練習題｜角柱・圓柱・表面積 學習單（附解答）",
              "柱體的體積",
              "國小六年級數學「角柱和圓柱的體積與表面積」免費學習單：柱體體積 ＝ 底面積 × 高、三角柱和梯形柱、圓柱的體積、圓柱和三角柱的表面積與水桶、複合形體等應用題。100題線上練習馬上對答案，附可列印解答。",
              "柱體體積 ＝ 底面積 × 高",
              "圓柱底面積 ＝ 半徑 × 半徑 × 3.14。",
              body, faq, sets, 13)


if __name__ == "__main__":
    main()
