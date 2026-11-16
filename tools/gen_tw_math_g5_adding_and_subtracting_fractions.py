# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：異分母分數的加減（108課綱 N-5-4）
  python3 tools/gen_tw_math_g5_adding_and_subtracting_fractions.py
通分して加減（真分數・帶分數）、答えは最簡分數・帶分數、借りる引き算、應用問題。
誤答：分子同士・分母同士を足す（1/2＋1/3＝2/5）、通分で分子を変え忘れる、約分しない、借りるとき 1 を 10 とする。
"""
import random
from fractions import Fraction as F
from math import gcd
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, mx, ff

R = random.Random(51005)
NM = Names(R)


def lcm(a, b):
    return a * b // gcd(a, b)


def pf(a, b):
    return F(a, b).denominator == b


def show(w, a, b):
    return mx(w, a, b) if w else fr(a, b)


def s_add(seen, n, mixed=False, sub=False):
    def mk():
        b, d = R.sample(range(2, 13), 2)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)) or lcm(b, d) > 60:
            return None
        w1, w2 = (R.randint(1, 5), R.randint(0, 3)) if mixed else (0, 0)
        x, y = w1 + F(a, b), w2 + F(c, d)
        if sub:
            if x <= y:
                return None
            v = x - y
        else:
            v = x + y
        L = lcm(b, d)
        op = "－" if sub else "＋"
        q = "%s %s %s ＝" % (show(w1, a, b), op, show(w2, c, d))
        naive = F(abs(a - c) if sub else a + c, b + d) if (abs(a - c) if sub else a + c) else F(1, b + d)
        w = [ff(w1 - w2 + naive) if sub else ff(w1 + w2 + naive), ff(v + F(1, L)), ff(v - F(1, L)) if v > F(1, L) else ff(v + F(2, L)),
             fr((v.numerator * (L // v.denominator)), L) if v.denominator != L and v < 1 else ff(v + 1)]
        e = "通分成分母 %d：%s %s %s，%s ＝ %s。" % (L, fr(a * L // b, L), op, fr(c * L // d, L), "整數和分數分開算" if mixed else "分母不變，分子相%s" % ("減" if sub else "加"), ff(v))
        if mixed and sub and F(a, b) < F(c, d):
            e = "通分成分母 %d：%s 不夠減 %s，從整數借 1 ＝ %s，答案 %s。" % (L, fr(a * L // b, L), fr(c * L // d, L), fr(L, L), ff(v))
        return mcq(q, ff(v), w, e + ("（要約成最簡分數）" if (F(a * L // b + (c * L // d if not sub else -(c * L // d)), L).denominator != L) else ""))
    return pick_unique(R, mk, n, seen)


def s5(seen):
    def juice():
        b, d = R.sample([2, 3, 4, 5, 6, 8, 10], 2)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)):
            return None
        x, y = F(a, b), F(c, d)
        who = NM.next()
        if R.random() < .5:
            q = "%s早上喝了 %s 公升的牛奶，晚上喝了 %s 公升，一共喝了幾公升？" % (who, fr(a, b), fr(c, d))
            v = x + y
            return mcq(q, ff(v) + " 公升", [ff(F(a + c, b + d)) + " 公升", ff(v + F(1, lcm(b, d))) + " 公升", ff(abs(x - y)) + " 公升" if x != y else ff(v * 2) + " 公升"],
                       "%s ＋ %s ＝ %s（公升）。" % (fr(a, b), fr(c, d), ff(v)))
        w1 = R.randint(1, 4)
        tot = w1 + x
        if tot <= y:
            return None
        q = "一條繩子長 %s 公尺，剪掉 %s 公尺，還剩幾公尺？" % (show(w1, a, b), fr(c, d))
        v = tot - y
        return mcq(q, ff(v) + " 公尺", [ff(tot + y) + " 公尺", ff(v + F(1, lcm(b, d))) + " 公尺", ff(w1 + F(abs(a - c), abs(b - d) or 1)) + " 公尺" if b != d else ff(v + 1) + " 公尺"],
                   "%s － %s ＝ %s（公尺）。" % (show(w1, a, b), fr(c, d), ff(v)))

    def diff():
        b, d = R.sample([2, 3, 4, 5, 6, 8, 12], 2)
        a, c = R.randint(1, b - 1), R.randint(1, d - 1)
        if not (pf(a, b) and pf(c, d)) or F(a, b) == F(c, d):
            return None
        x, y = F(a, b), F(c, d)
        p1, p2 = NM.next(), NM.next()
        if p1 == p2:
            return None
        q = "%s看了一本書的 %s，%s看了同一本書的 %s。誰看得多？多看了全書的幾分之幾？" % (p1, fr(a, b), p2, fr(c, d))
        big = p1 if x > y else p2
        v = abs(x - y)
        return mcq(q, "%s，多 %s" % (big, ff(v)), ["%s，多 %s" % (p2 if big == p1 else p1, ff(v)), "%s，多 %s" % (big, ff(x + y)), "%s，多 %s" % (big, ff(F(abs(a - c), abs(b - d) or 1)) if b != d and a != c else ff(v + F(1, 12)))],
                   "通分比較並相減：%s。" % ff(v))
    return pick_unique(R, juice, 12, seen) + pick_unique(R, diff, 8, seen)


def main():
    seen = set()
    sets = [("異分母真分數的加法", s_add(seen, 20)), ("異分母真分數的減法", s_add(seen, 20, sub=True)),
            ("帶分數的加法", s_add(seen, 20, mixed=True)), ("帶分數的減法", s_add(seen, 20, mixed=True, sub=True)),
            ("應用問題", s5(seen))]
    body = lesson(
        ["分母不同不能直接加減，先<b>通分</b>（常用兩個分母的最小公倍數）。",
         "通分後分母不變，分子相加減；答案能約分就要<b>約成最簡分數</b>，假分數化成帶分數。",
         "帶分數：整數和分數分開算；分數不夠減時，從整數借 1（借來的 1 是「分母分之分母」）。"],
        [example("%s ＋ %s ＝" % (fr(1, 2), fr(1, 3)), ["通分成分母 6：%s ＋ %s。" % (fr(3, 6), fr(2, 6)), "分子相加：%s。" % fr(5, 6)], fr(5, 6)),
         example("%s － %s ＝" % (mx(3, 1, 4), mx(1, 2, 3)), ["通分成分母 12：%s － %s。" % (mx(3, 3, 12), mx(1, 8, 12)), "%s 不夠減，借 1：%s － %s ＝ %s。" % (fr(3, 12), mx(2, 15, 12), mx(1, 8, 12), mx(1, 7, 12))], mx(1, 7, 12))],
        [("%s ＋ %s ＝ %s" % (fr(1, 2), fr(1, 3), fr(2, 5)), "分母不能相加，先通分：%s" % fr(5, 6)),
         ("通分時只改分母", "分母乘多少，分子也要乘多少"),
         ("答案 %s 沒有約分" % fr(4, 6), "約成最簡分數：%s" % fr(2, 3))])
    faq = [{"q": "異分母分數怎麼相加？",
            "a": "先用兩個分母的最小公倍數通分，變成同分母後分子相加，最後約成最簡分數。例如 1/2 ＋ 1/3 ＝ 3/6 ＋ 2/6 ＝ 5/6。"},
           {"q": "帶分數相減不夠減怎麼辦？",
            "a": "從整數部分借 1，化成「分母分之分母」加到分數部分，再相減。"},
           {"q": "五年級的分數加減要學什麼？",
            "a": "108課綱 N-5-4：用約分、擴分處理等值分數，並用通分做異分母分數的加減。"}]
    make_unit(R, "grade-5", "adding-and-subtracting-fractions", "N-5-4",
              "異分母分數：用約分、擴分處理等值分數並做比較。用通分做異分母分數的加減。",
              "異分母分數的加減",
              "五年級數學 異分母分數加減 練習題｜通分・帶分數加減 學習單（附解答）",
              "異分母分數加減",
              "國小五年級數學「異分母分數的加減」免費學習單：通分後做真分數和帶分數的加減、不夠減時借1、約成最簡分數與應用題。100題線上練習馬上對答案，附可列印解答。",
              "先通分，再加減，最後約分",
              "帶分數不夠減，從整數借 1。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
