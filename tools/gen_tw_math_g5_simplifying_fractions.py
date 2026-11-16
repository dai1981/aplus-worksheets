# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：約分、擴分與異分母分數的比較（108課綱 N-5-4）
  python3 tools/gen_tw_math_g5_simplifying_fractions.py
擴分、約分（最簡分數）、□を求める、通分して比較、大小の並べ替え。
誤答：分子だけ割る、約分が途中で止まる（最簡でない）、分母が大きいほうが大きいと思う。
"""
import random
from fractions import Fraction as F
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff

R = random.Random(51004)
NM = Names(R)


def s1(seen):
    def expand():
        b = R.randint(2, 12)
        a = R.randint(1, b - 1)
        if gcd(a, b) != 1:
            return None
        k = R.randint(2, 7)
        q = "把 %s 擴分，分母變成 %d，是多少？" % (fr(a, b), b * k)
        return mcq(q, fr(a * k, b * k), [fr(a, b * k), fr(a + b * k - b, b * k) if a + b * k - b < b * k else fr(a * k + 1, b * k), fr(a * k - 1, b * k) if a * k > 1 else fr(a * k + 2, b * k)],
                   "分母 %d × %d ＝ %d，分子也 × %d：%d × %d ＝ %d。" % (b, k, b * k, k, a, k, a * k))

    def blank():
        b = R.randint(2, 10)
        a = R.randint(1, b - 1)
        k = R.randint(2, 6)
        if gcd(a, b) != 1:
            return None
        if R.random() < .5:
            q = "%s ＝ %s，□ 是多少？" % (fr(a, b), fr("□", b * k))
            return mcq(q, str(a * k), [str(a + b * k - b), str(a * k + 1), str(a)], "分母乘以 %d，分子也乘以 %d：%d。" % (k, k, a * k))
        q = "%s ＝ %s，□ 是多少？" % (fr(a * k, b * k), fr(a, "□"))
        return mcq(q, str(b), [str(b * k - a * k + a), str(b * k), str(b + 1)], "分子除以 %d，分母也除以 %d：%d。" % (k, k, b))
    return pick_unique(R, expand, 10, seen) + pick_unique(R, blank, 10, seen)


def s2(seen):
    def mk():
        b = R.randint(2, 12)
        a = R.randint(1, b - 1)
        if gcd(a, b) != 1:
            return None
        k = R.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        A, B = a * k, b * k
        if B > 120:
            return None
        g2 = [d for d in range(2, k) if k % d == 0]
        half = fr(A // g2[0], B // g2[0]) if g2 else fr(A, B)
        w = [half if g2 else fr(A - 1, B - 1), fr(A // k, B) if A % k == 0 else fr(a, B), fr(a + 1, b + 1) if a + 1 < b + 1 else fr(1, b + 1), fr(A, B)]
        return mcq("把 %s 約成最簡分數。" % fr(A, B), fr(a, b), [x for x in w if x != fr(a, b)],
                   "%d 和 %d 的最大公因數是 %d，分子分母都除以 %d：%s。" % (A, B, k, k, fr(a, b)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        b, d = R.sample(range(2, 13), 2)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        x, y = F(a, b), F(c, d)
        if x == y or gcd(a, b) != 1 or gcd(c, d) != 1:
            return None
        L = b * d // gcd(b, d)
        sign = ">" if x > y else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (fr(a, b), fr(c, d)), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "通分成分母 %d：%s 和 %s，比分子：%s %s %s。" % (L, fr(a * L // b, L), fr(c * L // d, L), fr(a, b), sign, fr(c, d)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def biggest():
        ds = R.sample(range(2, 11), 3)
        fs = []
        for d in ds:
            n = R.randint(1, d - 1)
            fs.append(F(n, d))
        if len(set(fs)) < 3 or any(f.denominator != d for f, d in zip(fs, ds)):
            return None
        ask = R.choice(["最大", "最小"])
        t = max(fs) if ask == "最大" else min(fs)
        labs = [fr(f.numerator, f.denominator) for f in fs]
        bigden = labs[ds.index(max(ds))]
        others = [l for l in labs if l != fr(t.numerator, t.denominator)]
        return mcq("%s 中，哪一個%s？" % ("、".join(labs), ask), fr(t.numerator, t.denominator), others + ["一樣大"],
                   "通分後比分子（也可以化成小數比）：%s的是 %s。不是看分母大小。" % (ask, fr(t.numerator, t.denominator)))

    def half():
        b = R.randint(3, 15)
        a = R.randint(1, b - 1)
        if 2 * a == b or gcd(a, b) != 1:
            return None
        ans = "比 %s 大" % fr(1, 2) if 2 * a > b else "比 %s 小" % fr(1, 2)
        return mcq("%s 和 %s 比，怎樣？" % (fr(a, b), fr(1, 2)), ans, ["比 %s 小" % fr(1, 2) if 2 * a > b else "比 %s 大" % fr(1, 2), "一樣大", "無法比較"],
                   "%s 的一半是 %s，分子 %d %s %s，所以%s。" % ("分母 %d" % b, "%s" % (b / 2 if b % 2 else b // 2), a, ">" if 2 * a > b else "<", b / 2 if b % 2 else b // 2, ans))
    return pick_unique(R, biggest, 12, seen) + pick_unique(R, half, 8, seen)


def s5(seen):
    def eat():
        b, d = R.sample([3, 4, 5, 6, 8, 10, 12], 2)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        x, y = F(a, b), F(c, d)
        if x == y or gcd(a, b) != 1 or gcd(c, d) != 1:
            return None
        p1, p2 = NM.next(), NM.next()
        if p1 == p2:
            return None
        q = "一樣大的兩個蛋糕，%s吃了 %s 個，%s吃了 %s 個。誰吃得比較多？" % (p1, fr(a, b), p2, fr(c, d))
        ans = p1 if x > y else p2
        return mcq(q, ans, [p2 if ans == p1 else p1, "一樣多", "無法比較"], "通分比較：%s %s %s，%s吃得比較多。" % (fr(a, b), ">" if x > y else "<", fr(c, d), ans))

    def simp():
        tot = R.choice([12, 18, 20, 24, 30, 36, 40])
        part = R.randint(2, tot - 2)
        if gcd(part, tot) == 1:
            return None
        g = gcd(part, tot)
        q = "全班 %d 人，有 %d 人戴眼鏡。戴眼鏡的人是全班的幾分之幾？（用最簡分數）" % (tot, part)
        return mcq(q, fr(part // g, tot // g), [fr(part, tot), fr(tot - part, tot) if gcd(tot - part, tot) == 1 else fr((tot - part) // gcd(tot - part, tot), tot // gcd(tot - part, tot)), fr(part // g, tot)],
                   "%s，分子分母同除以 %d：%s。" % (fr(part, tot), g, fr(part // g, tot // g)))
    return pick_unique(R, eat, 10, seen) + pick_unique(R, simp, 10, seen)


def main():
    seen = set()
    sets = [("擴分", s1(seen)), ("約分成最簡分數", s2(seen)), ("通分比大小", s3(seen)), ("找最大最小", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["<b>擴分</b>：分子分母同時乘以同一個數；<b>約分</b>：分子分母同時除以同一個數。分數大小不變。",
         "分子分母只剩公因數 1，叫做<b>最簡分數</b>。用最大公因數去除，一次就能約到最簡。",
         "<b>通分</b>：把分母不同的分數擴分成同分母（常用最小公倍數），再比分子。"],
        [example("把 %s 約成最簡分數" % fr(18, 24), ["18 和 24 的最大公因數是 6。", "18 ÷ 6 ＝ 3，24 ÷ 6 ＝ 4。"], fr(3, 4)),
         example("%s 和 %s 哪個大？" % (fr(2, 3), fr(3, 4)), ["通分成分母 12：%s 和 %s。" % (fr(8, 12), fr(9, 12)), "9 ＞ 8。"], fr(3, 4))],
        [("約分時只除分子", "分子分母都要除以同一個數"),
         ("%s 約成 %s 就停了" % (fr(18, 24), fr(9, 12)), "還能再約：%s" % fr(3, 4)),
         ("分母大的分數比較大", "要通分後比分子：%s ＞ %s" % (fr(1, 2), fr(1, 3)))])
    faq = [{"q": "約分和擴分是什麼？",
            "a": "分子和分母同時除以同一個數叫約分，同時乘以同一個數叫擴分，分數的大小都不變。"},
           {"q": "怎麼一次約到最簡分數？",
            "a": "找出分子和分母的最大公因數，用它同時去除分子和分母。"},
           {"q": "五年級的異分母分數要學什麼？",
            "a": "108課綱 N-5-4：用約分、擴分處理等值分數並比較大小，再用通分做異分母分數的加減。"}]
    make_unit(R, "grade-5", "simplifying-fractions", "N-5-4",
              "異分母分數：用約分、擴分處理等值分數並做比較。用通分做異分母分數的加減。",
              "約分、擴分與通分比大小",
              "五年級數學 約分擴分 練習題｜最簡分數・通分・異分母比大小 學習單（附解答）",
              "約分、擴分與通分",
              "國小五年級數學「約分、擴分與通分」免費學習單：擴分、約成最簡分數、通分比大小、找最大最小與應用題。100題線上練習馬上對答案，附可列印解答。",
              "分子分母同乘同除，大小不變",
              "用最大公因數約分，用最小公倍數通分。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
