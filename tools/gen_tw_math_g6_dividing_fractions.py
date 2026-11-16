# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：分數的除法（108課綱 N-6-3）
  python3 tools/gen_tw_math_g6_dividing_fractions.py
整數÷分數（包含除：幾個 1/3）、同分母の分數÷分數（分子どうし）、異分母は 乘以倒數、帶分數÷分數、應用。
誤答：倒數にする分數を間違える（被除數を逆にする）、分子・分母をそのまま割る、帶分數を假分數にしない。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, ff

R = random.Random(61003)
NM = Names(R)


def rfr(lo=2, hi=12):
    d = R.randint(lo, hi)
    n = R.randint(1, d - 1)
    if F(n, d).denominator != d:
        return None
    return F(n, d)


def frs(v):
    return fr(v.numerator, v.denominator)


def rec(b):
    return str(b.denominator) if b.numerator == 1 else fr(b.denominator, b.numerator)


def wrong(a, b):
    """よくある間違いの答え"""
    out = [ff(a * b), ff(F(b.numerator, b.denominator) / a) if a else None]
    if a.denominator == b.denominator or True:
        out.append(ff(F(a.numerator * b.denominator, a.denominator * b.numerator) + F(1, max(2, b.numerator))))
    out.append(ff(1 / (a / b)))
    return [x for x in out if x]


def s1(seen):
    def mk():
        n = R.randint(1, 9)
        d = R.randint(2, 9)
        k = R.randint(1, d - 1)
        if F(k, d).denominator != d:
            return None
        v = n / F(k, d)
        if k == 1:
            q = "%d 裡面有幾個 %s？（%d ÷ %s）" % (n, fr(1, d), n, fr(1, d))
            e = "1 裡面有 %d 個 %s，%d 裡面有 %d × %d ＝ %d 個。" % (d, fr(1, d), n, n, d, n * d)
        else:
            q = "%d ÷ %s ＝" % (n, fr(k, d))
            e = "除以一個分數，等於乘以它的倒數：%d × %s ＝ %s。" % (n, fr(d, k), ff(v))
        return mcq(q, ff(v), [ff(n * F(k, d)), ff(F(n, d) * k) if k > 1 else ff(F(n, d)), ff(v + 1), ff(F(k, d) / n)], e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        d = R.randint(3, 15)
        a, b = R.randint(1, 3 * d), R.randint(1, d - 1)
        if a == b or a % d == 0:
            return None
        v = F(a, b)
        q = "%s ÷ %s ＝" % (fr(a, d), fr(b, d))
        return mcq(q, ff(v), [ff(F(b, a)), ff(F(a, d) * F(b, d)), ff(F(a, b * d)), ff(v + 1)],
                   "分母一樣，就看有幾個 %s：%d 個 ÷ %d 個 ＝ %d ÷ %d ＝ %s。" % (fr(1, d), a, b, a, b, ff(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = rfr(), rfr()
        if not a or not b or a.denominator == b.denominator or a == b:
            return None
        v = a / b
        q = "%s ÷ %s ＝" % (frs(a), frs(b))
        return mcq(q, ff(v), [ff(1 / v), ff(a * b), ff(F(a.numerator, b.numerator) if a.numerator % b.numerator == 0 else v + F(1, 2)) if ff(F(a.numerator, b.numerator)) != ff(v) else ff(v * 2)],
                   "乘以除數的倒數：%s × %s ＝ %s。" % (frs(a), rec(b), ff(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        w = R.randint(1, 4)
        d = R.randint(2, 8)
        n = R.randint(1, d - 1)
        if F(n, d).denominator != d:
            return None
        a = w + F(n, d)
        b = rfr(2, 9)
        if not b:
            return None
        if R.random() < .3:
            b = F(R.randint(2, 4), 1) + b
        v = a / b
        bs = ff(b)
        q = "%s ÷ %s ＝" % (ff(a), bs)
        steps = "先化成假分數：%s ÷ %s ＝ %s × %s ＝ %s。" % (frs(a), frs(b), frs(a), rec(b), ff(v))
        return mcq(q, ff(v), [ff(1 / v), ff((w + F(n, d) / b) if b.denominator else v + 1), ff(a * b), ff(F(w) / b + F(n, d))], steps)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def juice():
        tot = F(R.randint(2, 6))
        each = rfr(3, 8)
        if not each or (tot / each).denominator != 1:
            return None
        cup = tot / each
        q = "有 %s 公升果汁，每杯倒 %s 公升，可以倒幾杯？" % (ff(tot), frs(each))
        return mcq(q, "%s 杯" % ff(cup), ["%s 杯" % ff(x) for x in (tot * each, each / tot, cup + 1)], "%s ÷ %s ＝ %s × %s ＝ %s（杯）。" % (ff(tot), frs(each), ff(tot), rec(each), ff(cup)))

    def rope():
        a = F(R.randint(3, 12), R.choice([2, 4, 5]))
        b = rfr(3, 8)
        if not b or a.denominator == 1:
            return None
        v = a / b
        who = NM.next()
        q = "%s有一條 %s 公尺的繩子，是另一條繩子的 %s 倍。另一條繩子長幾公尺？" % (who, ff(a), frs(b))
        return mcq(q, "%s 公尺" % ff(v), ["%s 公尺" % ff(x) for x in (a * b, b / a, v + 1)], "另一條 × %s ＝ %s，所以另一條 ＝ %s ÷ %s ＝ %s（公尺）。" % (frs(b), ff(a), ff(a), frs(b), ff(v)))

    def speed():
        km = F(R.randint(1, 9), R.choice([2, 3, 4]))
        h = F(R.randint(1, 3), R.choice([4, 5, 6]))
        if km.denominator == 1 or h.denominator == 1 or h >= 1:
            return None
        v = km / h
        q = "一個人 %s 小時走了 %s 公里。照這樣走，1 小時可以走幾公里？" % (frs(h), ff(km))
        return mcq(q, "%s 公里" % ff(v), ["%s 公里" % ff(x) for x in (km * h, h / km, v + F(1, 2))], "%s ÷ %s ＝ %s（公里）。" % (ff(km), frs(h), ff(v)))
    return pick_unique(R, juice, 7, seen) + pick_unique(R, rope, 7, seen) + pick_unique(R, speed, 6, seen)


def main():
    seen = set()
    sets = [("整數除以分數", s1(seen)), ("同分母分數相除", s2(seen)), ("乘以倒數", s3(seen)),
            ("帶分數的除法", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["2 ÷ <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>：2 裡面有幾個 <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>？答案是 6 個。",
         "分母一樣時，分子相除：<span class='fr'><span class='fn'>6</span><span class='fd'>7</span></span> ÷ <span class='fr'><span class='fn'>2</span><span class='fd'>7</span></span> ＝ 6 ÷ 2 ＝ 3。",
         "<b>除以一個分數，等於乘以它的倒數</b>（分子和分母對調）。帶分數要先化成假分數。"],
        [example("<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> ÷ <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span>",
                 ["乘以 <span class='fr'><span class='fn'>2</span><span class='fd'>5</span></span> 的倒數 <span class='fr'><span class='fn'>5</span><span class='fd'>2</span></span>。", "<span class='fr'><span class='fn'>3 × 5</span><span class='fd'>4 × 2</span></span> ＝ <span class='fr'><span class='fn'>15</span><span class='fd'>8</span></span>。"],
                 "1<span class='fr'><span class='fn'>7</span><span class='fd'>8</span></span>")],
        [("把被除數倒過來", "只有除數要倒過來"),
         ("帶分數直接乘倒數", "先化成假分數再算"),
         ("以為除完一定比原來小", "除以比 1 小的數，答案會變大")])
    faq = [{"q": "為什麼除以分數要乘以倒數？",
            "a": "例如 2 ÷ 1/3 是問 2 裡面有幾個 1/3，1 裡面有 3 個，所以 2 裡面有 2 × 3 ＝ 6 個；這和 2 × 3/1 一樣。"},
           {"q": "除以分數答案為什麼會變大？",
            "a": "除數比 1 小時，被除數裡面可以放進更多個除數，所以商比被除數大。"},
           {"q": "六年級的分數除法要學什麼？",
            "a": "108課綱 N-6-3：理解整數除以分數、分數除以分數的意義，最後理解「除以一數等於乘以其倒數」。"}]
    make_unit(R, "grade-6", "dividing-fractions", "N-6-3",
              "分數的除法：整數除以分數、分數除以分數的意義。最後理解除以一數等於乘以其倒數之公式。",
              "分數的除法：乘以倒數",
              "六年級數學 分數除法 練習題｜整數除以分數・分數除以分數・倒數 學習單（附解答）",
              "分數的除法",
              "國小六年級數學「分數的除法」免費學習單：整數除以分數、同分母分數相除、乘以倒數、帶分數的除法和果汁、繩子等應用題。100題線上練習馬上對答案，附可列印解答。",
              "除以一個分數，等於乘以它的倒數",
              "帶分數先化成假分數；只把除數倒過來。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
