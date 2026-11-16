# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：比與比值（108課綱 N-6-6）
  python3 tools/gen_tw_math_g6_ratios.py
比を書く（前項・後項の順）、比值＝前項÷後項、相等的比（同乘・同除）、最簡整數比（小數・分數の比も）、比の應用（□を求める・異類量）。
誤答：前項と後項を逆にする、比值を後項÷前項にする、一方の項だけに掛ける、最簡にしきらない。
"""
import random
from math import gcd
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff, dnum

R = random.Random(61006)
NM = Names(R)


def rs(a, b):
    return "%s：%s" % (a, b)


def s1(seen):
    def mk():
        a, b = R.randint(2, 30), R.randint(2, 30)
        if a == b:
            return None
        who = NM.next()
        kind = R.choice(["boy", "juice", "ab"])
        if kind == "boy":
            q = "班上男生 %d 人，女生 %d 人。男生人數和女生人數的比是多少？" % (a, b)
            ans, e = rs(a, b), "先說的寫在前面：男生：女生 ＝ %d：%d。" % (a, b)
            w = [rs(b, a), rs(a, a + b), rs(a + b, b)]
        elif kind == "juice":
            q = "%s調果汁，用了 %d 杯果汁和 %d 杯水。水和果汁的比是多少？" % (who, a, b)
            ans, e = rs(b, a), "題目問「水和果汁」，水寫在前面：%d：%d。" % (b, a)
            w = [rs(a, b), rs(b, a + b), rs(a + b, a)]
        else:
            q = "籃子裡有 %d 顆蘋果和 %d 顆橘子。蘋果和全部水果的比是多少？" % (a, b)
            ans, e = rs(a, a + b), "全部 ＝ %d ＋ %d ＝ %d，蘋果：全部 ＝ %d：%d。" % (a, b, a + b, a, a + b)
            w = [rs(a, b), rs(a + b, a), rs(b, a + b)]
        return mcq(q, ans, w, e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 40), R.randint(2, 40)
        if a == b:
            return None
        v = F(a, b)
        return mcq("%s 的比值是多少？" % rs(a, b), ff(v), [ff(F(b, a)), ff(F(a, a + b)), ff(v + 1) if v < 3 else ff(v - 1)],
                   "比值 ＝ 前項 ÷ 後項：%d ÷ %d ＝ %s。" % (a, b, ff(v)))

    def dec():
        a, b = R.choice([0.5, 1.2, 2.5, 0.8, 1.5, 3.6]), R.choice([2, 4, 5, 3, 6])
        v = F(str(a)) / b
        return mcq("%s 的比值是多少？" % rs(dnum(a), b), ff(v), [ff(1 / v), ff(F(str(a)) * b), ff(v * 10)],
                   "比值 ＝ %s ÷ %d ＝ %s。" % (dnum(a), b, ff(v)))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, dec, 6, seen)


def s3(seen):
    def eq():
        a, b = R.randint(1, 9), R.randint(2, 9)
        if a == b or gcd(a, b) != 1:
            return None
        k = R.randint(2, 9)
        ans = rs(a * k, b * k)
        w = [rs(a * k, b), rs(a + k, b + k), rs(b * k, a * k)]
        return mcq("下面哪一個比和 %s 相等？" % rs(a, b), ans, w, "前項和後項同時乘以 %d：%s ＝ %s，比值都是 %s。" % (k, rs(a, b), ans, ff(F(a, b))))

    def box():
        a, b = R.randint(1, 9), R.randint(2, 12)
        if a == b or gcd(a, b) != 1:
            return None
        k = R.randint(2, 9)
        if R.random() < .5:
            q = "%s ＝ %d：□，□ 是多少？" % (rs(a, b), a * k)
            v, w = b * k, [b + (a * k - a), a * k * b, b * k + k]
            e = "%d 是 %d 的 %d 倍，%d 也要乘以 %d：□ ＝ %d。" % (a * k, a, k, b, k, b * k)
        else:
            q = "%s ＝ □：%d，□ 是多少？" % (rs(a * k, b * k), b)
            v, w = a, [a * k - (b * k - b), a * k * b, a + 1]
            e = "後項 %d ÷ %d ＝ %d，前項也除以 %d：%d ÷ %d ＝ %d。" % (b * k, k, b, k, a * k, k, a)
        return mcq(q, str(v), [str(x) for x in w if x > 0], e)
    return pick_unique(R, eq, 8, seen) + pick_unique(R, box, 12, seen)


def s4(seen):
    def whole():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a == b or gcd(a, b) != 1:
            return None
        k = R.choice([3, 4, 6, 8, 12, 15])
        A, B = a * k, b * k
        g2 = 2 if k % 2 == 0 and k != 2 else (3 if k % 3 == 0 and k != 3 else None)
        w = [rs(A // g2, B // g2) if g2 else rs(a + 1, b), rs(b, a), rs(A - B if A > B else B - A, B) if A != B else rs(a, b + 1)]
        return mcq("把 %s 化成最簡整數比。" % rs(A, B), rs(a, b), w, "%d 和 %d 的最大公因數是 %d，同除以 %d：%s。" % (A, B, k, k, rs(a, b)))

    def dec():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if a == b or gcd(a, b) != 1:
            return None
        m = R.choice([2, 3, 4, 5])
        A, B = F(a * m, 10), F(b * m, 10)
        if A.denominator == 1 or B.denominator == 1:
            return None
        sa, sb = dnum(float(A)), dnum(float(B))
        return mcq("把 %s 化成最簡整數比。" % rs(sa, sb), rs(a, b), [rs(a * m, b * m), rs(b, a), rs(a * m, b)],
                   "先都乘以 10：%s，再同除以 %d：%s。" % (rs(a * m, b * m), m, rs(a, b)))

    def frac():
        p, q2 = R.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6)]), R.choice([(1, 2), (1, 3), (1, 4), (3, 8), (5, 6)])
        A, B = F(*p), F(*q2)
        if A == B:
            return None
        L = A.denominator * B.denominator // gcd(A.denominator, B.denominator)
        x, y = int(A * L), int(B * L)
        g = gcd(x, y)
        x, y = x // g, y // g
        return mcq("把 %s 化成最簡整數比。" % rs(fr(*p), fr(*q2)), rs(x, y), [rs(p[0], q2[0]), rs(p[1], q2[1]), rs(y, x)],
                   "兩項同乘以分母的最小公倍數 %d：%s ＝ %s。" % (L, rs(fr(*p), fr(*q2)), rs(x, y)))
    return pick_unique(R, whole, 8, seen) + pick_unique(R, dec, 6, seen) + pick_unique(R, frac, 6, seen)


def s5(seen):
    def recipe():
        a, b = R.choice([(2, 3), (3, 5), (1, 4), (2, 5), (3, 4), (4, 7)])
        k = R.randint(3, 12)
        who = NM.next()
        q = "%s做鬆餅，麵粉和牛奶的比是 %s。用了 %d 公克麵粉，要用幾公克牛奶？" % (who, rs(a * 50, b * 50), a * 10 * k)
        flour = a * 10 * k
        milk = b * 10 * k
        return mcq(q, "%d 公克" % milk, ["%d 公克" % x for x in (flour + (b - a) * 50, flour * a // b if flour * a % b == 0 else milk * 2, flour + b * 50, milk * 2) if x != milk],
                   "%s ＝ %s ＝ %d：□；%d ÷ %d ＝ %d 倍，□ ＝ %d × %d ＝ %d（公克）。" % (rs(a * 50, b * 50), rs(a, b), flour, flour, a, flour // a, b, flour // a, milk))

    def price():
        L, P = R.choice([(2, 75), (3, 120), (5, 180), (4, 150), (6, 210)])
        k = R.randint(2, 5)
        q = "一種醬油 %d 瓶賣 %d 元（瓶數和價錢的比是 %s）。照這個比，%d 瓶要多少元？" % (L, P, rs(L, P), L * k)
        return mcq(q, "%d 元" % (P * k), ["%d 元" % x for x in (P + L * k, P * L * k, P * k + P)], "%s ＝ %s，瓶數變成 %d 倍，價錢也變成 %d 倍：%d × %d ＝ %d（元）。" % (rs(L, P), rs(L * k, "□"), k, k, P, k, P * k))

    def map_():
        a, b = R.randint(2, 7), R.randint(2, 7)
        if a == b or gcd(a, b) != 1:
            return None
        k = R.randint(3, 15)
        q = "一張長方形照片的長和寬的比是 %s。放大後長是 %d 公分，寬是幾公分？" % (rs(max(a, b), min(a, b)), max(a, b) * k)
        hi, lo = max(a, b), min(a, b)
        return mcq(q, "%d 公分" % (lo * k), ["%d 公分" % x for x in (hi * k - (hi - lo), hi * k * lo // hi + 1 if (hi * k * lo) % hi else lo * k + lo, hi * k * hi // lo if (hi * k * hi) % lo == 0 else lo * k - 1)  if x != lo * k],
                   "%d ÷ %d ＝ %d 倍，寬也乘以 %d：%d × %d ＝ %d（公分）。" % (hi * k, hi, k, k, lo, k, lo * k))
    return pick_unique(R, recipe, 7, seen) + pick_unique(R, price, 6, seen) + pick_unique(R, map_, 7, seen)


def main():
    seen = set()
    sets = [("寫出比", s1(seen)), ("比值", s2(seen)), ("相等的比", s3(seen)),
            ("最簡整數比", s4(seen)), ("比的應用", s5(seen))]
    body = lesson(
        ["<b>比</b>：A 和 B 的比寫成 A：B，<b>順序不能對調</b>（前項：後項）。",
         "<b>比值 ＝ 前項 ÷ 後項</b>，例如 3：4 的比值是 <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>。",
         "前項和後項<b>同時乘以或除以</b>同一個數（0 除外），比值不變，叫做相等的比。",
         "最簡整數比：前項和後項都是整數，而且互質。小數或分數的比要先化成整數。"],
        [example("2：3 ＝ 12：□", ["12 是 2 的 6 倍。", "3 × 6 ＝ 18。"], "18"),
         example("把 0.6：1.5 化成最簡整數比。", ["都乘以 10：6：15。", "同除以 3：2：5。"], "2：5")],
        [("「水和果汁的比」寫成果汁：水", "題目先說的寫在前面"),
         ("3：4 的比值寫成 <span class='fr'><span class='fn'>4</span><span class='fd'>3</span></span>", "前項 ÷ 後項：<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>"),
         ("2：3 ＝ 12：□，□ ＝ 13（都加 10）", "要同乘以 6：□ ＝ 18")])
    faq = [{"q": "比和比值有什麼不同？",
            "a": "比是兩個量的關係，寫成 A：B；比值是一個數，等於 A ÷ B。相等的比，比值一定相同。"},
           {"q": "怎麼化成最簡整數比？",
            "a": "小數先乘以 10 或 100，分數先乘以分母的最小公倍數，變成整數後再同除以最大公因數。"},
           {"q": "六年級的比與比值要學什麼？",
            "a": "108課綱 N-6-6：異類量的比與同類量的比之比值的意義，理解相等的比中的倍數關係（比例思考的基礎），並解決比的應用問題。"}]
    make_unit(R, "grade-6", "ratios", "N-6-6",
              "比與比值：異類量的比與同類量的比之比值的意義。理解相等的比中牽涉到的兩種倍數關係（比例思考的基礎）。解決比的應用問題。",
              "比與比值",
              "六年級數學 比與比值 練習題｜相等的比・最簡整數比 學習單（附解答）",
              "比與比值",
              "國小六年級數學「比與比值」免費學習單：寫出比、求比值、相等的比和求□、最簡整數比（含小數和分數）與食譜、價錢、照片放大等比的應用題。100題線上練習馬上對答案，附可列印解答。",
              "比值 ＝ 前項 ÷ 後項",
              "前項和後項同乘或同除一個數，比值不變。",
              body, faq, sets, 6)


if __name__ == "__main__":
    main()
