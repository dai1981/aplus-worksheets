# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：標準分解式與最大公因數、最小公倍數（108課綱 N-7-2）
  python3 tools/gen_tw_math_g7_standard_factorization.py
質因數分解の標準分解式（2³×3²×5）、標準分解式から因數の判定・因數の個數、標準分解式で最大公因數（共通・小さい指數）と最小公倍數（すべて・大きい指數）、應用。
誤答：標準分解式で小さい質數から並べない・合數を含める、最大公因數で大きい指數を取る、因數の個數を指數の和にする。
"""
import random
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g7 import tidy_sets

R = random.Random(71010)
NM = Names(R)
PS = [2, 3, 5, 7, 11]


def fac(n):
    out = {}
    p = 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out


def std(f):
    return " × ".join("%d<sup>%d</sup>" % (p, e) if e > 1 else str(p) for p, e in sorted(f.items()))


def val(f):
    v = 1
    for p, e in f.items():
        v *= p ** e
    return v


def rand_f(maxv=2000):
    while True:
        ps = R.sample(PS[:4], R.choice([2, 3]))
        f = {p: R.randint(1, 3 if p < 5 else 2) for p in ps}
        if val(f) <= maxv and sum(f.values()) >= 3:
            return f


def s1(seen):
    def mk():
        f = rand_f()
        n = val(f)
        ans = std(f)
        ps = sorted(f)
        bad = dict(f)
        p0 = ps[0]
        w = []
        if f[p0] >= 2:
            g = dict(f)
            g[p0] -= 2
            g = {k: v for k, v in g.items() if v}
            w.append("%d × %s" % (p0 * p0, std(g)) if g else str(p0 * p0))
        w.append(" × ".join(str(p) for p in ps))
        g2 = dict(f)
        g2[ps[-1]] += 1
        w.append(std(g2))
        w.append(" × ".join("%d<sup>%d</sup>" % (p, e) for p, e in sorted(f.items(), reverse=True)))
        return mcq("%s 的標準分解式是哪一個？" % num(n), ans, w, "用短除法分解，相同的質因數用指數表示，由小到大排列：%s ＝ %s。" % (num(n), ans))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def isfac():
        f = rand_f(5000)
        n = val(f)
        ps = sorted(f)
        good = dict(f)
        p = R.choice(ps)
        good[p] = max(1, good[p] - 1)
        g = val(good)
        bad = dict(good)
        q_ = R.choice(ps)
        bad[q_] = f[q_] + 1
        b = val(bad)
        other = [x for x in PS if x not in f][0]
        c = val(good) // max(1, 1) * other
        ans = std(good)
        return mcq("a ＝ %s。下面哪一個是 a 的因數？" % std(f), ans, [std(bad), std({**good, other: 1}), std({**{k: v for k, v in good.items()}, ps[0]: f[ps[0]] + 2})],
                   "a 的因數只能用 a 的質因數，而且每個指數都不能超過 a 的指數。")

    def count():
        f = rand_f(5000)
        c = 1
        for e in f.values():
            c *= e + 1
        es = sorted(f.values())
        q = "%s 的正因數有幾個？" % std(f)
        return mcq(q, "%d 個" % c, ["%d 個" % x for x in (sum(f.values()), sum(f.values()) + 1, c - 1, c + 2)  if x != c],
                   "每個質因數可以取 0 到指數次：%s ＝ %d 個。" % (" × ".join("（%d ＋ 1）" % e for p, e in sorted(f.items())), c))
    return pick_unique(R, isfac, 10, seen) + pick_unique(R, count, 10, seen)


def s3(seen):
    def mk():
        ps = R.sample(PS[:4], 3)
        a = {p: R.randint(0, 3) for p in ps}
        b = {p: R.randint(0, 3) for p in ps}
        a = {k: v for k, v in a.items() if v}
        b = {k: v for k, v in b.items() if v}
        g = {p: min(a.get(p, 0), b.get(p, 0)) for p in ps}
        g = {k: v for k, v in g.items() if v}
        if not g or len(a) < 2 or len(b) < 2 or a == b:
            return None
        l = {p: max(a.get(p, 0), b.get(p, 0)) for p in ps}
        l = {k: v for k, v in l.items() if v}
        q = "a ＝ %s，b ＝ %s。a 和 b 的最大公因數是？" % (std(a), std(b))
        return mcq(q, std(g), [std(l), std({p: max(a.get(p, 0), b.get(p, 0)) for p in g}), std({**g, sorted(g)[0]: g[sorted(g)[0]] + 1}), std({**g, sorted(g)[-1]: g[sorted(g)[-1]] + 1}), std({p: a.get(p, 0) + b.get(p, 0) for p in g})],
                   "取共同的質因數，指數取<b>小</b>的：%s。" % std(g))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        ps = R.sample(PS[:4], 3)
        a = {k: v for k, v in {p: R.randint(0, 3) for p in ps}.items() if v}
        b = {k: v for k, v in {p: R.randint(0, 3) for p in ps}.items() if v}
        if len(a) < 2 or len(b) < 2 or a == b:
            return None
        l = {p: max(a.get(p, 0), b.get(p, 0)) for p in ps}
        l = {k: v for k, v in l.items() if v}
        g = {k: v for k, v in {p: min(a.get(p, 0), b.get(p, 0)) for p in ps}.items() if v}
        s_ = {p: a.get(p, 0) + b.get(p, 0) for p in ps}
        s_ = {k: v for k, v in s_.items() if v}
        w = [std(s_), std(g) if g else "1", std({p: e for p, e in l.items() if p in a and p in b}) if any(p in a and p in b for p in l) else std({**l, ps[0]: l.get(ps[0], 0) + 1})]
        q = "a ＝ %s，b ＝ %s。a 和 b 的最小公倍數是？" % (std(a), std(b))
        return mcq(q, std(l), w + [std({**l, sorted(l)[0]: l[sorted(l)[0]] + 1})], "所有出現過的質因數都要取，指數取<b>大</b>的：%s。" % std(l))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def bells():
        a, b = R.choice([(12, 18), (15, 20), (8, 12), (18, 24), (20, 30), (16, 24), (9, 12), (10, 15)])
        L = a * b // gcd(a, b)
        q = "兩盞燈分別每 %d 秒和每 %d 秒閃一次，現在同時閃，至少再過幾秒會再同時閃？" % (a, b)
        return mcq(q, "%d 秒" % L, ["%d 秒" % x for x in (a * b, gcd(a, b), a + b)  if x != L], "%d ＝ %s，%d ＝ %s，最小公倍數 ＝ %d。" % (a, std(fac(a)), b, std(fac(b)), L))

    def groups():
        a, b = R.choice([(48, 72), (36, 60), (54, 90), (42, 70), (84, 126), (60, 96), (45, 75)])
        G = gcd(a, b)
        q = "有男生 %d 人、女生 %d 人，要分成人數相同的小組，每組男女生人數都一樣多，最多可以分成幾組？" % (a, b)
        return mcq(q, "%d 組" % G, ["%d 組" % x for x in (a * b // G, G // 2, a // G + b // G)  if x != G], "%d ＝ %s，%d ＝ %s，最大公因數 ＝ %d。" % (a, std(fac(a)), b, std(fac(b)), G))

    def square():
        a, b = R.choice([(6, 8), (12, 18), (4, 6), (10, 15), (8, 12), (9, 12), (14, 21)])
        L = a * b // gcd(a, b)
        n = (L // a) * (L // b)
        q = "用長 %d 公分、寬 %d 公分的長方形磁磚，排成最小的正方形，要用幾塊？" % (b, a)
        return mcq(q, "%d 塊" % n, ["%d 塊" % x for x in (L // a + L // b, L, n * 2)  if x != n], "邊長是 %d 和 %d 的最小公倍數 %d，需要 %d × %d ＝ %d 塊。" % (a, b, L, L // a, L // b, n))
    return pick_unique(R, bells, 7, seen) + pick_unique(R, groups, 7, seen) + pick_unique(R, square, 6, seen)


def main():
    seen = set()
    sets = [("標準分解式", s1(seen)), ("因數與因數的個數", s2(seen)), ("用標準分解式求最大公因數", s3(seen)),
            ("用標準分解式求最小公倍數", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>標準分解式</b>：把數分解成質因數，相同的用指數表示，由小到大排：360 ＝ 2<sup>3</sup> × 3<sup>2</sup> × 5。",
         "<b>最大公因數</b>：取<b>共同</b>的質因數，指數取<b>小</b>的。",
         "<b>最小公倍數</b>：取<b>所有</b>的質因數，指數取<b>大</b>的。",
         "2<sup>a</sup> × 3<sup>b</sup> 的正因數個數 ＝（a ＋ 1）×（b ＋ 1）。"],
        [example("求 2<sup>3</sup> × 3 × 5<sup>2</sup> 和 2<sup>2</sup> × 3<sup>3</sup> 的最大公因數和最小公倍數。",
                 ["共同的 2、3，指數取小：2<sup>2</sup> × 3。", "全部的 2、3、5，指數取大：2<sup>3</sup> × 3<sup>3</sup> × 5<sup>2</sup>。"], "2<sup>2</sup> × 3；2<sup>3</sup> × 3<sup>3</sup> × 5<sup>2</sup>")],
        [("360 ＝ 2<sup>3</sup> × 9 × 5", "9 不是質數：3<sup>2</sup>"),
         ("最大公因數取大的指數", "要取小的，才能同時整除兩數"),
         ("2<sup>3</sup> × 3<sup>2</sup> 有 3 ＋ 2 ＝ 5 個因數", "（3 ＋ 1）×（2 ＋ 1）＝ 12 個")])
    faq = [{"q": "什麼是標準分解式？",
            "a": "把一個數寫成質因數的連乘，相同的質因數用指數表示，並由小到大排列，例如 720 ＝ 2⁴ × 3² × 5。"},
           {"q": "用標準分解式怎麼求最大公因數和最小公倍數？",
            "a": "最大公因數取兩數共同的質因數、指數取小的；最小公倍數取所有質因數、指數取大的。"},
           {"q": "七年級的質因數分解要學什麼？",
            "a": "108課綱 N-7-2：質因數分解的標準分解式，並能用於求因數及倍數的問題。"}]
    make_unit(R, "grade-7", "standard-factorization", "N-7-2",
              "質因數分解的標準分解式：質因數分解的標準分解式，並能用於求因數及倍數的問題。",
              "標準分解式與最大公因數、最小公倍數",
              "七年級數學 標準分解式 練習題｜最大公因數・最小公倍數・因數個數 學習單（附解答）",
              "標準分解式",
              "國中七年級數學「標準分解式與最大公因數、最小公倍數」免費學習單：寫出標準分解式、判斷因數和求因數個數、用標準分解式求最大公因數和最小公倍數與應用題。100題線上練習馬上對答案，附可列印解答。",
              "最大公因數：共同的、指數取小；最小公倍數：全部的、指數取大",
              "標準分解式由小到大排，相同的質因數用指數表示。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
