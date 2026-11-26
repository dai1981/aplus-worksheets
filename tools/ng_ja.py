# -*- coding: utf-8 -*-
"""
Nigeria JSS 1–3 Mathematics: makers written for Nigeria (naira, number bases, word problems).
Each maker takes a random.Random and returns one item; AssertionError means "draw again".
"""
import math
from fractions import Fraction as F
from ng_common import mcq, comma, naira, fig, fr
from ng_p4a import K, ch
from ng_p5a import bs, b2, SUB, ITEMS, item


# ============================================================ number bases
def bin_mul(r):
    a, b = r.randint(3, 15), r.randint(2, 7)
    p = a * b
    w = [b2(p + 1), b2(p - 1), b2(a + b), b2(p * 2)]
    return mcq("Multiply in base two: %s × %s" % (b2(a), b2(b)), b2(p), [x for x in w if x != b2(p)],
               "%s = %d and %s = %d. %d × %d = %d = <b>%s</b>." % (b2(a), a, b2(b), b, a, b, p, b2(p)))


def base_add(r):
    base = ch(r, [3, 4, 5, 6, 7, 8])
    a, b = r.randint(base, base ** 3 - 1), r.randint(base, base ** 3 - 1)
    s = a + b
    want = bs(s, base)
    w = [bs(s + 1, base), bs(s - 1, base), bs(s + base, base), bs(s, base)[:-1] + str(base + 1).translate(SUB) if base < 9 else bs(s + 2, base)]
    w = [x for x in w if x != want]
    return mcq("Add in base %d: %s + %s" % (base, bs(a, base), bs(b, base)), want, w,
               "In base %d, carry 1 each time a column reaches %d. Check in base ten: %d + %d = %d = <b>%s</b>." % (base, base, a, b, s, want))


def base_sub(r):
    base = ch(r, [3, 4, 5, 6, 7, 8])
    a = r.randint(base * 2, base ** 3 - 1)
    b = r.randint(base, a - 1)
    d = a - b
    want = bs(d, base)
    w = [bs(d + 1, base), bs(d - 1, base) if d > 1 else bs(d + 2, base), bs(d + base, base), bs(abs(a - b - base) or 1, base)]
    return mcq("Subtract in base %d: %s − %s" % (base, bs(a, base), bs(b, base)), want, [x for x in w if x != want],
               "When you borrow, you borrow %d (not 10). Check in base ten: %d − %d = %d = <b>%s</b>." % (base, a, b, d, want))


def base_mul(r):
    base = ch(r, [3, 4, 5, 6, 7, 8])
    a = r.randint(base, base ** 2 * 2)
    b = r.randint(2, base - 1)
    p = a * b
    want = bs(p, base)
    w = [bs(p + 1, base), bs(p - b, base), bs(a + b, base), bs(p + base, base)]
    return mcq("Multiply in base %d: %s × %s" % (base, bs(a, base), bs(b, base)), want, [x for x in w if x != want],
               "Check in base ten: %d × %d = %d = <b>%s</b>." % (a, b, p, want))


def base_convert(r):
    b1, b2_ = r.sample([2, 3, 4, 5, 8], 2)
    n = r.randint(max(b1, b2_) + 1, 120)
    src, want = bs(n, b1), bs(n, b2_)
    w = [bs(n + 1, b2_), bs(n - 1, b2_), bs(n, b1)[:-1] + str(b2_).translate(SUB), bs(n + b2_, b2_)]
    return mcq("Change %s to base %d." % (src, b2_), want, [x for x in w if x != want],
               "First change to base ten: %s = %d. Then change %d to base %d: <b>%s</b>." % (src, n, n, b2_, want))


def base_find(r):
    base = ch(r, [3, 4, 5, 6, 7, 8, 9])
    d1, d0 = r.randint(1, base - 1), r.randint(0, base - 1)
    n = d1 * base + d0
    return mcq("In base <i>b</i>, the number written %d%d has the value %d (base ten). Find <i>b</i>." % (d1, d0, n), base, [base + 1, base - 1, n - d0, 10],
               "%d × <i>b</i> + %d = %d, so %d<i>b</i> = %d and <i>b</i> = <b>%d</b>." % (d1, d0, n, d1, n - d0, base))


# ============================================================ commercial arithmetic (JSS)
def compound(r):
    p = ch(r, [10000, 20000, 25000, 40000, 50000, 80000, 100000, 200000, 500000])
    rate = ch(r, [5, 10, 20])
    t = ch(r, [2, 3])
    a = F(p) * (1 + F(rate, 100)) ** t
    if a.denominator != 1:
        raise AssertionError
    a = int(a)
    si = p * rate * t // 100
    k = K(r)
    q = r.randint(0, 1)
    if q == 0:
        return mcq("%s saves %s in a bank at %d%% compound interest per annum. How much will be in the account after %d years?" % (k["n"], naira(p), rate, t), naira(a),
                   [naira(p + si), naira(a - p), naira(p * (100 + rate * t) // 100 + 1000), naira(int(p * (1 + rate / 100.0)))],
                   "Multiply by %s each year: %s × %s<sup>%d</sup> = <b>%s</b>." % (1 + rate / 100.0, naira(p), 1 + rate / 100.0, t, naira(a)))
    return mcq("Find the compound interest on %s for %d years at %d%% per annum." % (naira(p), t, rate), naira(a - p),
               [naira(si), naira(a), naira(p * rate // 100), naira(a - p + 1000)],
               "Amount = %s × %s<sup>%d</sup> = %s. Interest = %s − %s = <b>%s</b>." % (naira(p), 1 + rate / 100.0, t, naira(a), naira(a), naira(p), naira(a - p)))


def depreciation(r):
    name = ch(r, ["car", "bus", "generator", "laptop", "tractor", "motorcycle"])
    p = ch(r, [400000, 500000, 800000, 1000000, 2000000, 2500000, 4000000, 5000000])
    rate = ch(r, [10, 20, 25])
    t = ch(r, [1, 2, 3])
    v = F(p) * (1 - F(rate, 100)) ** t
    if v.denominator != 1:
        raise AssertionError
    v = int(v)
    return mcq("A %s bought for %s loses %d%% of its value every year. What is its value after %d year%s?" % (name, naira(p), rate, t, "" if t == 1 else "s"), naira(v),
               [naira(p - p * rate * t // 100) if t > 1 else naira(p * rate // 100), naira(p - v), naira(v + p * rate // 100), naira(p - p * rate // 100 * 2) if t != 2 else naira(v - 10000)],
               "Multiply by %s each year: %s × %s<sup>%d</sup> = <b>%s</b>." % (1 - rate / 100.0, naira(p), 1 - rate / 100.0, t, naira(v)))


def pct_change(r):
    name, old = item(r, 1000)
    pc = ch(r, [5, 10, 15, 20, 25, 30, 40, 50])
    up = r.random() < 0.55
    d = old * pc // 100
    if old * pc % 100:
        raise AssertionError
    new = old + d if up else old - d
    return mcq("The price of %s changed from %s to %s. Find the percentage %s." % (name, naira(old), naira(new), "increase" if up else "decrease"), "%d%%" % pc,
               ["%d%%" % x for x in (round(d * 100.0 / new) if round(d * 100.0 / new) != pc else pc + 3, pc + 10, d // 1000 if d // 1000 not in (0, pc) else pc * 2, 100 - pc) if x != pc and x > 0],
               "Change = %s. %s ÷ %s × 100 = <b>%d%%</b> (divide by the old price)." % (naira(d), comma(d), comma(old), pc))


def reverse_pct(r):
    name, cp = item(r, 1000)
    pc = ch(r, [10, 20, 25, 50])
    sp = cp * (100 + pc) // 100
    if cp * (100 + pc) % 100:
        raise AssertionError
    return mcq("A trader sold %s for %s and made a profit of %d%%. What was the cost price?" % (name, naira(sp), pc), naira(cp),
               [naira(sp - sp * pc // 100), naira(sp + sp * pc // 100), naira(sp * pc // 100), naira(cp + 1000)],
               "Selling price = %d%% of cost price. Cost price = %s × 100 ÷ %d = <b>%s</b>." % (100 + pc, naira(sp), 100 + pc, naira(cp)))


def exchange(r):
    rate = ch(r, [1500, 1550, 1600, 1450])
    usd = ch(r, [20, 50, 100, 200, 250, 500])
    k = K(r)
    if r.random() < 0.5:
        return mcq("Suppose 1 US dollar = %s. How many naira will %s get for %d US dollars?" % (naira(rate), k["n"], usd), naira(rate * usd),
                   [naira(rate + usd), naira(rate * usd // 10), naira(rate * (usd + 10)), naira(rate * usd + rate)],
                   "%d × %s = <b>%s</b>." % (usd, naira(rate), naira(rate * usd)))
    return mcq("Suppose 1 US dollar = %s. How many US dollars can be bought with %s?" % (naira(rate), naira(rate * usd)), "%d US dollars" % usd,
               ["%d US dollars" % x for x in (usd * 10, usd + 10, usd // 2 if usd // 2 != usd else usd + 5, usd * 2)],
               "%s ÷ %s = <b>%d</b> US dollars." % (naira(rate * usd), naira(rate), usd))


# ============================================================ equations from words (JSS 1)
def eq_word(r):
    k = K(r)
    t = r.randint(0, 4)
    if t == 0:
        x = r.randint(3, 30)
        a, b = r.randint(2, 6), r.randint(1, 20)
        return mcq("I think of a number, multiply it by %d and add %d. The answer is %d. What is the number?" % (a, b, a * x + b), x, [x + 1, (a * x + b) // a, a * x + b - b // a, x * 2],
                   "%d<i>x</i> + %d = %d, so %d<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (a, b, a * x + b, a, a * x, x))
    if t == 1:
        x = r.randint(5, 40)
        b = r.randint(2, 20)
        return mcq("%s is %d years older than %s brother. Together their ages add up to %d. How old is the brother?" % (k["n"], b, k["his"], 2 * x + b),
                   x, [x + b, (2 * x + b) // 2, x - 1, 2 * x], "<i>x</i> + (<i>x</i> + %d) = %d, so 2<i>x</i> = %d and <i>x</i> = <b>%d</b>." % (b, 2 * x + b, 2 * x, x))
    if t == 2:
        w = r.randint(3, 20)
        l = w + r.randint(2, 15)
        p = 2 * (l + w)
        return mcq("The length of a rectangle is %d cm more than its width. Its perimeter is %d cm. Find the width." % (l - w, p), "%d cm" % w, ["%d cm" % x for x in (l, p // 4, w + 1, p // 2 - w)],
                   "2(<i>w</i> + <i>w</i> + %d) = %d, so 4<i>w</i> + %d = %d, 4<i>w</i> = %d, <i>w</i> = <b>%d cm</b>." % (l - w, p, 2 * (l - w), p, 4 * w, w))
    if t == 3:
        x = r.randint(2, 30) * 50
        n1, n2 = r.randint(2, 5), r.randint(2, 5)
        y = x + r.randint(1, 10) * 50
        tot = n1 * x + n2 * y
        thing1, thing2 = ch(r, [("pens", "exercise books"), ("oranges", "mangoes"), ("pencils", "rulers")])
        return mcq("%s bought %d %s at %s each and %d %s at %s each. %s paid %s altogether. Find %s." % (k["n"], n1, thing1, "<i>x</i> naira", n2, thing2, naira(y), k["He"], naira(tot), "<i>x</i>"),
                   comma(x), [comma(x + 50), comma(y), comma(tot // (n1 + n2)) if tot % (n1 + n2) == 0 and tot // (n1 + n2) != x else comma(x * 2), comma(x - 50)],
                   "%d<i>x</i> + %d × %s = %s, so %d<i>x</i> = %s and <i>x</i> = <b>%s</b>." % (n1, n2, comma(y), comma(tot), n1, comma(n1 * x), comma(x)))
    x = r.randint(4, 60)
    d = r.randint(2, 9)
    return mcq("When a number is divided by %d and then %d is added, the result is %d. Find the number." % (d, 5, x + 5), d * x, [x, x * d + 5, (x + 5) * d, d * x - 5],
               "<i>n</i> ÷ %d + 5 = %d, so <i>n</i> ÷ %d = %d and <i>n</i> = <b>%d</b>." % (d, x + 5, d, x, d * x))


# ============================================================ variation (JSS 3)
def variation(r):
    k = r.randint(2, 12)
    t = r.randint(0, 3)
    x1, x2 = r.sample(range(2, 13), 2)
    if t == 0:
        return mcq("<i>y</i> varies directly as <i>x</i>. When <i>x</i> = %d, <i>y</i> = %d. Find <i>y</i> when <i>x</i> = %d." % (x1, k * x1, x2), k * x2,
                   [k * x1 + x2 - x1, k * x1 * x2, k, x2 * x1], "<i>y</i> = <i>kx</i>: <i>k</i> = %d ÷ %d = %d. <i>y</i> = %d × %d = <b>%d</b>." % (k * x1, x1, k, k, x2, k * x2))
    if t == 1:
        c = k * x1 * x2
        return mcq("<i>y</i> varies inversely as <i>x</i>. When <i>x</i> = %d, <i>y</i> = %d. Find <i>y</i> when <i>x</i> = %d." % (x1, c // x1, x2), c // x2,
                   [c // x1 * x2 // x1 if (c // x1 * x2) % x1 == 0 and c // x1 * x2 // x1 != c // x2 else c // x2 + 1, c, c // x1 + x2, x2], "<i>xy</i> = <i>k</i> = %d × %d = %d. <i>y</i> = %d ÷ %d = <b>%d</b>." % (x1, c // x1, c, c, x2, c // x2))
    if t == 2:
        return mcq("<i>y</i> varies as the square of <i>x</i>. When <i>x</i> = %d, <i>y</i> = %d. Find <i>y</i> when <i>x</i> = %d." % (x1, k * x1 * x1, x2), k * x2 * x2,
                   [k * x2, k * x1 * x2, k * x2 * x2 + k, k * (x2 + x1)], "<i>y</i> = <i>kx</i>²: <i>k</i> = %d ÷ %d = %d. <i>y</i> = %d × %d² = <b>%d</b>." % (k * x1 * x1, x1 * x1, k, k, x2, k * x2 * x2))
    return mcq("<i>y</i> varies directly as <i>x</i> and <i>y</i> = %d when <i>x</i> = %d. Which equation connects <i>x</i> and <i>y</i>?" % (k * x1, x1), "<i>y</i> = %d<i>x</i>" % k,
               ["<i>y</i> = %d<i>x</i>" % (k * x1), "<i>xy</i> = %d" % (k * x1 * x1), "<i>y</i> = <i>x</i> + %d" % (k * x1 - x1)],
               "<i>k</i> = %d ÷ %d = %d, so <b><i>y</i> = %d<i>x</i></b>." % (k * x1, x1, k, k))


def variation_word(r):
    t = r.randint(0, 2)
    if t == 0:
        c = ch(r, [300, 450, 500, 750, 800])
        n1 = r.randint(2, 6)
        n2 = r.randint(7, 15)
        thing = ch(r, ["loaves of bread", "bottles of water", "packets of biscuits"])
        return mcq("The cost of %s varies directly as the number bought. %d cost %s. What do %d cost?" % (thing, n1, naira(c * n1), n2), naira(c * n2),
                   [naira(c * n1 + n2), naira(c * n1 * n2), naira(c * (n2 - n1)), naira(c * n2 + c)], "One costs %s. %d × %s = <b>%s</b>." % (naira(c), n2, naira(c), naira(c * n2)))
    if t == 1:
        s1 = ch(r, [40, 50, 60, 80])
        t1 = ch(r, [3, 4, 5, 6])
        ss = [x for x in (30, 40, 60, 80, 100, 120) if s1 * t1 % x == 0 and x != s1]
        if not ss:
            raise AssertionError
        s2 = ch(r, ss)
        return mcq("The time for a journey varies inversely as the speed. At %d km/h it takes %d hours. How long does it take at %d km/h?" % (s1, t1, s2), "%s hours" % comma(s1 * t1 // s2) if s1 * t1 // s2 != 1 else "1 hour",
                   ["%d hours" % x for x in (t1 * s2 // s1 if t1 * s2 % s1 == 0 and t1 * s2 // s1 != s1 * t1 // s2 else t1 + 1, s1 * t1, t1 + 2, abs(t1 - 1) or 4) if x != s1 * t1 // s2],
                   "speed × time = %d × %d = %d. Time = %d ÷ %d = <b>%d hours</b>." % (s1, t1, s1 * t1, s1 * t1, s2, s1 * t1 // s2))
    w1 = ch(r, [3, 4, 5, 6, 8])
    d1 = ch(r, [6, 8, 10, 12, 15])
    ws = [x for x in (2, 3, 4, 5, 6, 10, 12) if w1 * d1 % x == 0 and x != w1]
    if not ws:
        raise AssertionError
    w2 = ch(r, ws)
    return mcq("The number of days needed to build a fence varies inversely as the number of workers. %d workers take %d days. How many days will %d workers take?" % (w1, d1, w2),
               w1 * d1 // w2, [d1 * w2 // w1 if d1 * w2 % w1 == 0 and d1 * w2 // w1 != w1 * d1 // w2 else d1 + 1, w1 * d1, d1 + w1 - w2 if d1 + w1 - w2 > 0 else d1 + 3, w1 * d1 // w2 + 2],
               "workers × days = %d. %d ÷ %d = <b>%d</b> days." % (w1 * d1, w1 * d1, w2, w1 * d1 // w2))
