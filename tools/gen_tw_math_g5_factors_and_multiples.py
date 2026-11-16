# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：因數、倍數、公因數、公倍數（108課綱 N-5-3）
  python3 tools/gen_tw_math_g5_factors_and_multiples.py
因數・倍數の判別と列挙、公因數と最大公因數、公倍數と最小公倍數、文章題（分ける→公因數、そろう→公倍數）。
誤答：因數と倍數の取り違え、1 と自分自身を落とす、最大公因數と最小公倍數の取り違え、積をそのまま最小公倍數とする。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(51002)
NM = Names(R)


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def lcm(a, b):
    return a * b // gcd(a, b)


def j(xs):
    return "、".join(map(str, xs))


def s1(seen):
    def list_f():
        n = R.choice([x for x in range(12, 61) if len(factors(x)) >= 4])
        f = factors(n)
        w = [j(f[1:-1]), j([d for d in f if d != n]), j(f[:len(f) // 2] + [n]), j([n * k for k in range(1, 5)])]
        return mcq("%d 的所有因數是哪一組？" % n, j(f), [x for x in w if x != j(f)], "能整除 %d 的數都是它的因數，1 和 %d 也算：%s。" % (n, n, j(f)))

    def is_f():
        n = R.randint(12, 96)
        f = factors(n)
        if len(f) < 4:
            return None
        good = R.choice(f[1:-1])
        bad = [x for x in range(2, n) if n % x][:]
        R.shuffle(bad)
        return mcq("下面哪一個是 %d 的因數？" % n, str(good), [str(x) for x in bad[:2]] + [str(n * 2)], "%d ÷ %d ＝ %d，整除，所以 %d 是 %d 的因數。" % (n, good, n // good, good, n))

    def mult():
        a = R.randint(3, 15)
        k = R.randint(3, 12)
        v = a * k
        return mcq("下面哪一個是 %d 的倍數？" % a, str(v), [str(v + R.choice([1, 2, -1])), str(v + a // 2 if a > 2 else v + 1), str(a + k)] if a + k != v else [str(v + 1), str(v - 1), str(v + 2)],
                   "%d × %d ＝ %d，所以 %d 是 %d 的倍數。" % (a, k, v, v, a))
    return pick_unique(R, list_f, 8, seen) + pick_unique(R, is_f, 6, seen) + pick_unique(R, mult, 6, seen)


def s2(seen):
    def common():
        a, b = R.sample(range(8, 61), 2)
        g = gcd(a, b)
        if g < 2:
            return None
        cf = factors(g)
        w = [j(cf[:-1]) if len(cf) > 2 else j(cf + [a]), j(sorted(set(factors(a)) | set(factors(b)))[:len(cf) + 1]), j(factors(min(a, b)))]
        return mcq("%d 和 %d 的公因數是哪一組？" % (a, b), j(cf), [x for x in w if x != j(cf)] + [j(cf + [g * 2])],
                   "%d 的因數：%s；%d 的因數：%s。兩個都有的是 %s。" % (a, j(factors(a)), b, j(factors(b)), j(cf)))

    def gcf():
        g = R.randint(2, 12)
        a, b = g * R.randint(2, 7), g * R.randint(2, 7)
        if a == b or gcd(a, b) != g:
            return None
        return mcq("%d 和 %d 的最大公因數是多少？" % (a, b), str(g), [str(x) for x in (lcm(a, b), g * 2 if (a % (g * 2) or b % (g * 2)) else 1, factors(g)[-2] if len(factors(g)) > 1 and factors(g)[-2] != 1 else g + 1, min(a, b))],
                   "兩個數共同的因數中最大的是 %d。" % g)
    return pick_unique(R, common, 8, seen) + pick_unique(R, gcf, 12, seen)


def s3(seen):
    def common():
        a, b = R.sample(range(2, 13), 2)
        L = lcm(a, b)
        if L > 60:
            return None
        cm = [L * k for k in (1, 2, 3)]
        w = [j([a * k for k in (1, 2, 3)]), j([L, L + a, L + b]), j([a * b * k for k in (1, 2, 3)]) if a * b != L else j([L * 2, L * 3, L * 4])]
        return mcq("%d 和 %d 最小的三個公倍數是哪一組？" % (a, b), j(cm), [x for x in w if x != j(cm)] + [j([L * 2, L * 3, L * 4])],
                   "%d 的倍數 %s…中，也是 %d 的倍數的是 %s…，最小的 %d 是最小公倍數。" % (max(a, b), j([max(a, b) * k for k in range(1, 3 * L // max(a, b) + 1)]), min(a, b), j(cm), L))

    def lcm_q():
        a, b = R.sample(range(2, 16), 2)
        L = lcm(a, b)
        return mcq("%d 和 %d 的最小公倍數是多少？" % (a, b), str(L), [str(x) for x in (a * b if a * b != L else L * 2, gcd(a, b) if gcd(a, b) > 1 else L + a, L * 2, max(a, b), L * 3, a + b)],
                   "從 %d 的倍數裡找第一個也是 %d 的倍數的數：%d。%s" % (max(a, b), min(a, b), L, "（%d × %d ＝ %d 也是公倍數，但不是最小的）" % (a, b, a * b) if a * b != L else ""))
    return pick_unique(R, common, 8, seen) + pick_unique(R, lcm_q, 12, seen)


def s4(seen):
    def mix():
        a, b = R.sample(range(4, 37), 2)
        g, L = gcd(a, b), lcm(a, b)
        if g < 2 or L > 200:
            return None
        ask = R.choice(["g", "L"])
        if ask == "g":
            return mcq("%d 和 %d 的<b>最大公因數</b>是多少？" % (a, b), str(g), [str(L), str(g * 2) if a % (g * 2) or b % (g * 2) else str(g + 1), str(a * b), str(g // 2) if g % 2 == 0 and g > 2 else str(g + 2)], "最大公因數是兩數共同因數裡最大的：%d。（%d 是最小公倍數）" % (g, L))
        return mcq("%d 和 %d 的<b>最小公倍數</b>是多少？" % (a, b), str(L), [str(g), str(a * b) if a * b != L else str(L * 2), str(L + g), str(L * 2)], "最小公倍數是兩數共同倍數裡最小的：%d。（%d 是最大公因數）" % (L, g))

    def facts():
        F = [("1 是所有整數的什麼？", "因數", ["倍數", "最大公因數", "最小公倍數"], "任何整數都能被 1 整除，1 是所有整數的因數。"),
             ("一個數最小的倍數是多少？", "它自己", ["1", "0", "它的一半"], "一個數 × 1 就是它自己，是最小的倍數（0 不算）。"),
             ("一個數最大的因數是多少？", "它自己", ["1", "它的 2 倍", "沒有最大的"], "一個數的因數不會比它大，最大就是它自己。"),
             ("一個數的倍數有幾個？", "無限多個", ["只有 10 個", "和因數一樣多", "只有 1 個"], "一個數可以一直乘下去，倍數有無限多個。"),
             ("如果 A 是 B 的因數，那麼 B 是 A 的什麼？", "倍數", ["因數", "公因數", "一樣大"], "因數和倍數是一組：3 是 12 的因數，12 是 3 的倍數。"),
             ("兩個數的公因數裡一定有哪一個數？", "1", ["0", "2", "兩數的和"], "1 是每個數的因數，所以一定是公因數。")]
        return mcq(*R.choice(F))
    return pick_unique(R, mix, 14, seen) + pick_unique(R, facts, 6, seen)


def s5(seen):
    def share():
        g = R.randint(3, 12)
        a, b = g * R.randint(2, 8), g * R.randint(2, 8)
        if a == b or gcd(a, b) != g:
            return None
        it = R.choice([("顆糖果", "顆巧克力"), ("枝鉛筆", "塊橡皮擦"), ("個蘋果", "個橘子")])
        q = "有 %d %s和 %d %s，要平分給一些小朋友，兩種都剛好分完，最多可以分給幾個人？" % (a, it[0], b, it[1])
        return mcq(q, "%d 人" % g, ["%d 人" % x for x in (lcm(a, b), a + b, g * 2 if a % (g * 2) or b % (g * 2) else g + 1, g + 1)], "人數要是 %d 和 %d 的公因數，最多就是最大公因數 %d。" % (a, b, g))

    def meet():
        a, b = R.sample(range(2, 13), 2)
        L = lcm(a, b)
        if L > 60:
            return None
        q = "%s每 %d 天去游泳一次，%s每 %d 天去一次。今天兩人一起去，最少再過幾天會再一起去？" % (NM.next(), a, NM.next(), b)
        return mcq(q, "%d 天" % L, ["%d 天" % x for x in (a * b if a * b != L else L * 2, a + b, gcd(a, b) if gcd(a, b) > 1 else L + 1)], "天數要是 %d 和 %d 的公倍數，最少就是最小公倍數 %d。" % (a, b, L))

    def tile():
        g = R.randint(2, 15)
        a, b = g * R.randint(2, 9), g * R.randint(2, 9)
        if a == b or gcd(a, b) != g:
            return None
        a, b = max(a, b), min(a, b)
        q = "長 %d 公分、寬 %d 公分的長方形紙，要剪成大小一樣、最大的正方形，沒有剩下。正方形的邊長是幾公分？" % (a, b)
        return mcq(q, "%d 公分" % g, ["%d 公分" % x for x in (lcm(a, b), min(a, b), g * 2 if a % (g * 2) or b % (g * 2) else g + 1, g + 1, g - 1 if g > 2 else g + 2)], "邊長要同時能整除 %d 和 %d，最大是最大公因數 %d。" % (a, b, g))
    return pick_unique(R, share, 7, seen) + pick_unique(R, meet, 7, seen) + pick_unique(R, tile, 6, seen)


def main():
    seen = set()
    sets = [("因數和倍數", s1(seen)), ("公因數和最大公因數", s2(seen)), ("公倍數和最小公倍數", s3(seen)),
            ("分辨最大公因數和最小公倍數", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["12 ÷ 3 ＝ 4，整除，所以 3 是 12 的<b>因數</b>，12 是 3 的<b>倍數</b>。",
         "兩個數共同的因數是<b>公因數</b>，最大的叫<b>最大公因數</b>；共同的倍數是<b>公倍數</b>，最小的叫<b>最小公倍數</b>。",
         "「平分、剪成一樣大、剛好分完」→ 想公因數；「再一起、同時、對齊」→ 想公倍數。"],
        [example("12 和 18 的最大公因數和最小公倍數？", ["12 的因數：1、2、3、4、6、12；18 的因數：1、2、3、6、9、18。", "最大公因數 6；12 的倍數 12、24、36…，36 也是 18 的倍數。"], "最大公因數 6，最小公倍數 36"),
         example("每 4 天和每 6 天各去一次，今天一起去，幾天後再一起去？", ["4 和 6 的最小公倍數。"], "12 天後")],
        [("因數和倍數弄反", "小的那個是大的那個的因數：3 是 12 的因數"),
         ("列因數時漏掉 1 和自己", "1 和它自己一定是因數"),
         ("最小公倍數就是兩數相乘", "4 × 6 ＝ 24 是公倍數，但最小的是 12")])
    faq = [{"q": "因數和倍數有什麼關係？",
            "a": "如果 a × b ＝ c，a 和 b 都是 c 的因數，c 是 a 和 b 的倍數。例如 3 × 4 ＝ 12，3 是 12 的因數，12 是 3 的倍數。"},
           {"q": "五年級的因數倍數要學什麼？",
            "a": "108課綱 N-5-3：因數、倍數、公因數、公倍數、最大公因數、最小公倍數的意義，之後用在約分和通分。"},
           {"q": "應用題怎麼判斷用最大公因數還是最小公倍數？",
            "a": "把東西「分成一樣多、剪成一樣大」要用公因數（通常找最大）；「下一次同時發生、排成一樣長」要用公倍數（通常找最小）。"}]
    make_unit(R, "grade-5", "factors-and-multiples", "N-5-3",
              "公因數和公倍數：因數、倍數、公因數、公倍數、最大公因數、最小公倍數的意義。",
              "因數與倍數：最大公因數、最小公倍數",
              "五年級數學 因數倍數 練習題｜最大公因數・最小公倍數・應用題 學習單（附解答）",
              "因數與倍數",
              "國小五年級數學「因數與倍數」免費學習單：因數和倍數、公因數和最大公因數、公倍數和最小公倍數，分辨兩者和應用題。100題線上練習馬上對答案，附可列印解答。",
              "分成一樣多用公因數，再一起用公倍數",
              "最大公因數是共同因數裡最大的，最小公倍數是共同倍數裡最小的。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
