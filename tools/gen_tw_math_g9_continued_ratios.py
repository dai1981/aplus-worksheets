# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：連比（108課綱 N-9-1）
  python3 tools/gen_tw_math_g9_continued_ratios.py
連比の化簡（整數・分數・小數）、a：b と b：c から a：b：c、連比例式（一つの量から他の量）、總量を連比で分配、三角形の角・周長・生活の應用。
誤答：b を共通にしないで並べる（2：3 と 4：5 → 2：3：5）、分數の連比を分母どうしで並べる、分配で比の和で割らない。
"""
import random
from math import gcd
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num, fr
from tw_g7 import tidy_sets

R = random.Random(81101)
NM = Names(R)


def K(n):
    return "" if n == 1 else str(n)


def g3(a, b, c):
    return gcd(gcd(a, b), c)


def rs(t):
    return "：".join(str(x) for x in t)


def simp(t):
    g = g3(*t)
    return tuple(x // g for x in t)


def prim():
    while True:
        t = tuple(R.randint(1, 9) for _ in range(3))
        if g3(*t) == 1 and len(set(t)) > 1:
            return t


def s1(seen):
    def ints():
        t = prim()
        k = R.randint(2, 12)
        big = tuple(x * k for x in t)
        q = "化成最簡單整數比：%s" % rs(big)
        h = tuple(x // 2 for x in big) if all(x % 2 == 0 for x in big) and k % 2 == 0 and k != 2 else (t[0], t[1], t[2] + 1)
        return mcq(q, rs(t), [rs(h), rs((t[2], t[1], t[0])) if t[0] != t[2] else rs((t[1], t[0], t[2])), rs((t[0] * 2, t[1] * 2, t[2] * 2))],
                   "三個數同除以最大公因數 %d，得 %s。" % (k, rs(t)))

    def fracs():
        ds = R.sample([2, 3, 4, 5, 6, 8], 3)
        ns = [1] * 3 if R.random() < .5 else [R.randint(1, d - 1) for d in ds]
        fs = [F(n, d) for n, d in zip(ns, ds)]
        if len(set(fs)) < 3:
            return None
        L = 1
        for f in fs:
            L = L * f.denominator // gcd(L, f.denominator)
        t = simp(tuple(int(f * L) for f in fs))
        q = "化成最簡單整數比：%s" % "：".join(fr(f.numerator, f.denominator) for f in fs)
        w = [rs(simp(tuple(f.denominator for f in fs))), rs(tuple(f.numerator for f in fs)) if len(set(f.numerator for f in fs)) > 1 else rs((t[2], t[1], t[0])), rs(tuple(int(f * L * 2) for f in fs))]
        return mcq(q, rs(t), w, "三個數都乘以分母的最小公倍數 %d：%s。" % (L, rs(t)))

    def decs():
        t = prim()
        k = R.choice([F(1, 10), F(2, 10), F(5, 10), F(3, 10)])
        ds = [x * k for x in t]
        q = "化成最簡單整數比：%s" % "：".join(str(float(d)).rstrip("0").rstrip(".") for d in ds)
        return mcq(q, rs(t), [rs(tuple(int(d * 10) for d in ds)) if k != F(1, 10) else rs((t[0] + 1, t[1], t[2])), rs((t[1], t[0], t[2])) if t[0] != t[1] else rs((t[0], t[2], t[1])), rs((t[0], t[1], t[2] * 2))],
                   "先乘以 10 變整數：%s，再約分：%s。" % (rs(tuple(int(d * 10) for d in ds)), rs(t)))
    return pick_unique(R, ints, 8, seen) + pick_unique(R, fracs, 6, seen) + pick_unique(R, decs, 6, seen)


def s2(seen):
    def mk():
        a, b = R.randint(1, 9), R.randint(1, 9)
        c, d = R.randint(1, 9), R.randint(1, 9)
        if gcd(a, b) > 1 or gcd(c, d) > 1 or b == c:
            return None
        L = b * c // gcd(b, c)
        t = simp((a * L // b, L, d * L // c))
        q = "a：b ＝ %d：%d，b：c ＝ %d：%d，a：b：c ＝ ？" % (a, b, c, d)
        w = [rs((a, b, d)), rs((a, b * c, d)), rs(simp((a * c, b * c, d * b))), rs((a, L, d)), rs((a * c, L, d)), rs((a, b, d * c))]
        return mcq(q, rs(t), w, "把 b 變成 %d 和 %d 的公倍數 %d：a：b ＝ %d：%d，b：c ＝ %d：%d，a：b：c ＝ %s。" % (b, c, L, a * L // b, L, L, d * L // c, rs(t)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        t = prim()
        k = R.randint(2, 9)
        i, j = R.sample(range(3), 2)
        names = "xyz"
        q = "x：y：z ＝ %s，%s ＝ %d，%s 是多少？" % (rs(t), names[i], t[i] * k, names[j])
        v = t[j] * k
        return mcq(q, num(v), [num(t[i] * k * t[j]), num(t[j] * k + t[i]), num(t[i] * k // t[j]) if t[i] * k % t[j] == 0 and t[i] * k // t[j] != v else num(v + k)],
                   "設 x ＝ %sk，y ＝ %sk，z ＝ %sk；%sk ＝ %d，k ＝ %d，%s ＝ %d × %d ＝ %s。" % (K(t[0]), K(t[1]), K(t[2]), K(t[i]), t[i] * k, k, names[j], t[j], k, num(v)))

    def ksum():
        t = prim()
        k = R.randint(2, 9)
        S = sum(t) * k
        q = "x：y：z ＝ %s，x ＋ y ＋ z ＝ %d，y 是多少？" % (rs(t), S)
        v = t[1] * k
        return mcq(q, num(v), [num(S * t[1] // 3) if S * t[1] % 3 == 0 and S * t[1] // 3 != v else num(v + 1), num(k), num(t[1] * S)],
                   "設 x ＝ %sk，y ＝ %sk，z ＝ %sk，%sk ＝ %d，k ＝ %d，y ＝ %d。" % (K(t[0]), K(t[1]), K(t[2]), sum(t), S, k, v))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, ksum, 8, seen)


def s4(seen):
    def share():
        t = prim()
        k = R.choice([50, 100, 120, 150, 200, 250, 300])
        S = sum(t) * k
        names = [NM.next() for _ in range(3)]
        i = R.randrange(3)
        q = "%s、%s、%s三人按 %s 分 %s 元，%s分到多少元？" % (names[0], names[1], names[2], rs(t), num(S), names[i])
        v = t[i] * k
        return mcq(q, "%s 元" % num(v), ["%s 元" % num(x) for x in (S // 3 if S % 3 == 0 and S // 3 != v else v + k, S * t[i] // 10 if S * t[i] % 10 == 0 and S * t[i] // 10 != v else v - k, S - v)],
                   "共 %d 份，一份 %s ÷ %d ＝ %s 元，%s分 %d 份：%s 元。" % (sum(t), num(S), sum(t), num(k), names[i], t[i], num(v)))

    def diff():
        t = prim()
        if t[0] == t[2]:
            return None
        k = R.randint(3, 40)
        d = abs(t[0] - t[2]) * k
        q = "甲、乙、丙三班人數比是 %s，甲班和丙班相差 %d 人，乙班有幾人？" % (rs(t), d)
        v = t[1] * k
        return mcq(q, "%d 人" % v, ["%d 人" % x for x in (d * t[1], k, v + d)], "相差 %d 份 ＝ %d 人，一份 %d 人，乙班 %d × %d ＝ %d 人。" % (abs(t[0] - t[2]), d, k, t[1], k, v))
    return pick_unique(R, share, 12, seen) + pick_unique(R, diff, 8, seen)


def s5(seen):
    def angles():
        while True:
            t = prim()
            if 180 % sum(t) == 0:
                break
        k = 180 // sum(t)
        q = "三角形三個內角的比是 %s，最大的角是多少度？" % rs(t)
        v = max(t) * k
        return mcq(q, "%d°" % v, ["%d°" % x for x in (min(t) * k, 360 // sum(t) * max(t) if 360 // sum(t) * max(t) < 360 else v + 10, max(t) * 10 if max(t) * 10 != v else v + 5)], "內角和 180°，180° ÷ %d ＝ %d°，最大角 %d × %d° ＝ %d°。" % (sum(t), k, max(t), k, v))

    def peri():
        t = prim()
        if max(t) * 2 >= sum(t):
            return None
        k = R.randint(2, 8)
        P = sum(t) * k
        q = "三角形三邊長的比是 %s，周長 %d 公分，最短邊是多少公分？" % (rs(t), P)
        v = min(t) * k
        return mcq(q, "%d 公分" % v, ["%d 公分" % x for x in (max(t) * k, P // 3 if P % 3 == 0 and P // 3 != v else v + 1, min(t))], "%d ÷ %d ＝ %d，最短邊 %d × %d ＝ %d 公分。" % (P, sum(t), k, min(t), k, v))

    def mix():
        t = (R.randint(1, 5), R.randint(1, 5), R.randint(1, 5))
        if g3(*t) > 1 or len(set(t)) < 2:
            return None
        k = R.choice([50, 100, 150, 200])
        S = sum(t) * k
        q = "調一杯飲料，果汁、牛奶、汽水的比是 %s，共 %d 毫升，牛奶要多少毫升？" % (rs(t), S)
        v = t[1] * k
        return mcq(q, "%d 毫升" % v, ["%d 毫升" % x for x in (S // 3 if S % 3 == 0 and S // 3 != v else v + 50, t[1] * 100 if t[1] * 100 != v else v + 100, S - v)], "共 %d 份，一份 %d 毫升，牛奶 %d × %d ＝ %d 毫升。" % (sum(t), k, t[1], k, v))
    return pick_unique(R, angles, 7, seen) + pick_unique(R, peri, 7, seen) + pick_unique(R, mix, 6, seen)


def main():
    seen = set()
    sets = [("化簡連比", s1(seen)), ("兩個比合成連比", s2(seen)), ("連比例式", s3(seen)),
            ("按連比分配", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["三個以上的量的比叫<b>連比</b>，例如 2：3：5。三個數同乘或同除以一個不為 0 的數，連比不變。",
         "由 a：b 和 b：c 求 a：b：c：<b>先把 b 變成相同的數</b>（兩個 b 的最小公倍數），再合起來。",
         "x：y：z ＝ 2：3：5 時，可以設 x ＝ 2k、y ＝ 3k、z ＝ 5k 來求值。"],
        [example("a：b ＝ 2：3，b：c ＝ 4：5，a：b：c？", ["b 變成 12：a：b ＝ 8：12，b：c ＝ 12：15。"], "8：12：15"),
         example("按 2：3：5 分 500 元，各得多少？", ["共 10 份，一份 50 元。"], "100、150、250 元")],
        [("2：3 和 4：5 直接寫成 2：3：5", "b 不相同不能直接接起來"),
         ("<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>：<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>：<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span> ＝ 2：3：4", "乘以 12 得 6：4：3"),
         ("分配時除以 3 人", "要除以份數的和")])
    faq = [{"q": "連比和比有什麼不同？",
            "a": "比是兩個量，連比是三個以上的量，例如甲：乙：丙 ＝ 2：3：4，一次表示三個量的關係。"},
           {"q": "連比一定要化成最簡單整數比嗎？",
            "a": "答案通常寫最簡單整數比；計算時用相等的連比都可以。"},
           {"q": "九年級的連比要學什麼？",
            "a": "108課綱 N-9-1：連比的記錄、連比推理、連比例式，及其運算和應用問題。"}]
    make_unit(R, "grade-9", "continued-ratios", "N-9-1",
              "連比：連比的記錄；連比推理；連比例式；及其基本運算與相關應用問題；涉及複雜數值時使用計算機協助計算。",
              "連比與連比例式",
              "九年級數學 連比 練習題｜連比例式・按比分配 學習單（附解答）",
              "連比",
              "國中九年級數學「連比與連比例式」免費學習單：化簡連比、由兩個比合成連比、用 k 解連比例式、按連比分配、三角形內角與周長應用題。100題線上練習馬上對答案，附可列印解答。",
              "a：b 和 b：c，先把 b 化成相同",
              "x：y：z ＝ 2：3：5，設 x ＝ 2k、y ＝ 3k、z ＝ 5k。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
