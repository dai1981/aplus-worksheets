# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：最大公因數與最小公倍數（108課綱 N-6-2）
  python3 tools/gen_tw_math_g6_gcf_and_lcm.py
質因數分解・短除法で最大公因數・最小公倍數、兩數互質、約分（最大公因數で割る）・通分（最小公倍數）、應用。
誤答：最大公因數と最小公倍數を取り違える、兩數の積を最小公倍數とする、互質を「両方質數」と思う。
"""
import random
from math import gcd
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, fr

R = random.Random(61002)
NM = Names(R)


def lcm(a, b):
    return a * b // gcd(a, b)


def pair(lo=6, hi=60):
    while True:
        g = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 12])
        a, b = g * R.randint(2, 9), g * R.randint(2, 9)
        if a != b and lo <= a <= hi * 2 and lo <= b <= hi * 2 and gcd(a, b) > 1 and lcm(a, b) != a * b:
            return min(a, b), max(a, b)


def s1(seen):
    def mk():
        a, b = pair()
        g = gcd(a, b)
        fa = [d for d in range(1, a + 1) if a % d == 0 and b % d == 0]
        w = [x for x in (lcm(a, b), fa[-2] if len(fa) > 1 else g * 2, a * b // g // g if a * b // g // g != g else g + 1, b - a if b - a != g else g * 2) if x != g]
        return mcq("%d 和 %d 的最大公因數是多少？" % (a, b), str(g), [str(x) for x in w],
                   "%d 和 %d 的公因數有 %s，最大的是 %d。" % (a, b, "、".join(map(str, fa)), g))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = pair(4, 30)
        L = lcm(a, b)
        if L > 400:
            return None
        g = gcd(a, b)
        w = [a * b, g, L * 2, L - a if L - a not in (g, L) else L + b]
        return mcq("%d 和 %d 的最小公倍數是多少？" % (a, b), num(L), [num(x) for x in w if x != L],
                   "用短除法：先除以公因數 %d，得 %d 和 %d；最小公倍數 ＝ %d × %d × %d ＝ %d。" % (g, a // g, b // g, g, a // g, b // g, L))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def co():
        while True:
            a, b = R.randint(4, 30), R.randint(4, 30)
            if a < b and gcd(a, b) == 1 and not (a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29) and b in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)):
                break
        c, d = pair(4, 20)
        e, f = pair(4, 20)
        if (c, d) == (e, f):
            return None
        q = "下面哪一組數<b>互質</b>？"
        ans = "%d 和 %d" % (a, b)
        return mcq(q + "（%s）" % "、".join(sorted([ans, "%d 和 %d" % (c, d), "%d 和 %d" % (e, f), "%d 和 %d" % (2 * a, 2 * b if 2 * b != 2 * a else 2 * b + 2)])),
                   ans, ["%d 和 %d" % (c, d), "%d 和 %d" % (e, f), "%d 和 %d" % (2 * a, 2 * b if 2 * b != 2 * a else 2 * b + 2)],
                   "%d 和 %d 的公因數只有 1，所以互質（它們不一定是質數）。" % (a, b))

    def lcm_co():
        while True:
            a, b = R.randint(3, 15), R.randint(3, 15)
            if a < b and gcd(a, b) == 1:
                break
        return mcq("%d 和 %d 互質，它們的最小公倍數是多少？" % (a, b), str(a * b), [str(x) for x in (1, b, a + b, a * b * 2)],
                   "兩數互質時，最小公倍數就是兩數的積：%d × %d ＝ %d；最大公因數是 1。" % (a, b, a * b))
    return pick_unique(R, co, 12, seen) + pick_unique(R, lcm_co, 8, seen)


def s4(seen):
    def red():
        g = R.choice([3, 4, 6, 7, 8, 9, 12, 14, 15, 18])
        n, d = R.randint(1, 8), R.randint(2, 9)
        if n >= d or gcd(n, d) != 1:
            return None
        N, D = n * g, d * g
        return mcq("用最大公因數把 %s 約成最簡分數。" % fr(N, D), fr(n, d), [fr(N // 2, D // 2) if N % 2 == 0 and D % 2 == 0 and g != 2 else fr(n + 1, d), fr(n, d + 1), fr(N // n if N // n != d else n + 2, D) if False else fr(d, n) if n > 1 else fr(n + 1, d + 1)],
                   "%d 和 %d 的最大公因數是 %d，分子分母同除以 %d：%s。" % (N, D, g, g, fr(n, d)))

    def com():
        a, b = pair(3, 12)
        if a == b or lcm(a, b) > 72:
            return None
        L = lcm(a, b)
        na, nb = R.randint(1, a - 1), R.randint(1, b - 1)
        if gcd(na, a) != 1 or gcd(nb, b) != 1:
            return None
        return mcq("把 %s 和 %s 通分，用最小的公分母是多少？" % (fr(na, a), fr(nb, b)), str(L), [str(x) for x in (a * b, gcd(a, b), a + b, L * 2) if x != L],
                   "%d 和 %d 的最小公倍數是 %d，用 %d 當公分母最簡便。" % (a, b, L, L))
    return pick_unique(R, red, 10, seen) + pick_unique(R, com, 10, seen)


def s5(seen):
    def ribbon():
        a, b = pair(12, 60)
        g = gcd(a, b)
        who = NM.next()
        q = "%s有兩條緞帶，長 %d 公分和 %d 公分。要剪成一樣長的小段，都不能剩，每段最長是幾公分？" % (who, a, b)
        return mcq(q, "%d 公分" % g, ["%d 公分" % x for x in (lcm(a, b), g // 2 if g % 2 == 0 and g > 2 else g + 1, b - a if b - a != g else g * 2)],
                   "每段長度要同時是 %d 和 %d 的因數，又要最長：最大公因數 %d 公分。" % (a, b, g))

    def bus():
        a, b = pair(4, 20)
        L = lcm(a, b)
        if L > 120:
            return None
        h = R.choice([6, 7])
        q = "甲公車每 %d 分鐘一班，乙公車每 %d 分鐘一班。早上 %d 時兩車同時發車，下一次同時發車是幾分鐘後？" % (a, b, h)
        return mcq(q, "%d 分鐘後" % L, ["%d 分鐘後" % x for x in (a * b, gcd(a, b), a + b) if x != L] + ["%d 分鐘後" % (L * 2)],
                   "同時發車的時間要同時是 %d 和 %d 的倍數，最早是最小公倍數 %d 分鐘。" % (a, b, L))

    def tile():
        a, b = pair(10, 60)
        g = gcd(a, b)
        n = (a // g) * (b // g)
        q = "一塊長 %d 公分、寬 %d 公分的長方形，要剪成一樣大的正方形，不能剩。正方形最大邊長幾公分？可以剪幾塊？" % (b, a)
        ans = "邊長 %d 公分，%d 塊" % (g, n)
        return mcq(q, ans, ["邊長 %d 公分，%d 塊" % (lcm(a, b), 1), "邊長 %d 公分，%d 塊" % (g, n * 2), "邊長 %d 公分，%d 塊" % (g, a // g + b // g)],
                   "邊長是 %d 和 %d 的最大公因數 %d；%d ÷ %d ＝ %d，%d ÷ %d ＝ %d，%d × %d ＝ %d 塊。" % (a, b, g, b, g, b // g, a, g, a // g, b // g, a // g, n))
    return pick_unique(R, ribbon, 7, seen) + pick_unique(R, bus, 7, seen) + pick_unique(R, tile, 6, seen)


def main():
    seen = set()
    sets = [("最大公因數", s1(seen)), ("最小公倍數", s2(seen)), ("兩數互質", s3(seen)),
            ("約分和通分", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>最大公因數</b>：兩數共同的因數中最大的。<b>最小公倍數</b>：兩數共同的倍數中最小的。",
         "短除法：用兩數的公因數一起除，到商互質為止。左邊相乘是最大公因數；左邊和下面全部相乘是最小公倍數。",
         "兩數的公因數只有 1，叫做<b>互質</b>；互質的兩數，最小公倍數是兩數的積。"],
        [example("求 24 和 36 的最大公因數和最小公倍數。", ["24 ＝ 2 × 2 × 2 × 3，36 ＝ 2 × 2 × 3 × 3。", "共同的 2 × 2 × 3 ＝ 12；最小公倍數 12 × 2 × 3 ＝ 72。"], "12 和 72"),
         example("8 和 15 互質嗎？", ["8 的因數 1、2、4、8；15 的因數 1、3、5、15。", "公因數只有 1。"], "互質")],
        [("24 和 36 的最小公倍數是 24 × 36", "要除去重複的部分：72"),
         ("剪緞帶問題用最小公倍數", "分成小段（變小）用最大公因數"),
         ("互質就是兩個數都是質數", "8 和 15 不是質數，也互質")])
    faq = [{"q": "什麼時候用最大公因數、什麼時候用最小公倍數？",
            "a": "把東西平分、剪成一樣長、分成一樣大（越分越小）用最大公因數；找同時發生、排成正方形、通分（越來越大）用最小公倍數。"},
           {"q": "什麼是互質？",
            "a": "兩個數的公因數只有 1，例如 8 和 15。互質不代表兩個數都是質數。"},
           {"q": "六年級的最大公因數和最小公倍數要學什麼？",
            "a": "108課綱 N-6-2：用質因數分解法和短除法求最大公因數與最小公倍數，認識兩數互質，並用在分數的約分和通分。"}]
    make_unit(R, "grade-6", "gcf-and-lcm", "N-6-2",
              "最大公因數與最小公倍數：質因數分解法與短除法。兩數互質。運用到分數的約分與通分。",
              "最大公因數與最小公倍數",
              "六年級數學 最大公因數 最小公倍數 練習題｜短除法・互質 學習單（附解答）",
              "最大公因數與最小公倍數",
              "國小六年級數學「最大公因數與最小公倍數」免費學習單：用短除法求最大公因數和最小公倍數、兩數互質、約分和通分、剪緞帶和公車發車等應用題。100題線上練習馬上對答案，附可列印解答。",
              "分成小段用最大公因數，找同時用最小公倍數",
              "互質的兩數，最小公倍數是兩數的積。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
