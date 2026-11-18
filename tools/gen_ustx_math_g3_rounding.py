# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Rounding and Estimating (TEKS 3.2C, 3.4B)
  python3 tools/gen_ustx_math_g3_rounding.py
A number between two multiples of 10, 100, 1,000 or 10,000 on a number line, rounding to the nearest 10 and 100,
rounding to the nearest 1,000 and 10,000, estimating sums and differences by rounding or with compatible numbers,
and word problems.
Wrong answers come from real mistakes: rounding to the wrong place, rounding 5 down, changing only the
rounding digit and keeping the digits after it, and adding the exact numbers when asked to estimate.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, svg_wrap, text, line,
                       GREEN, RED, INK, example)

R = random.Random(60301)
PL = {10: "ten", 100: "hundred", 1000: "thousand", 10000: "ten thousand"}


def rnd_to(n, p):
    return (n + p // 2) // p * p


def round_line(n, p, show_mid=True, show_n=True):
    lo = n // p * p
    hi = lo + p
    W, x0, x1, y = 460, 30, 430, 58
    X = lambda v: x0 + (v - lo) * (x1 - x0) / float(p)
    s = [line(x0 - 12, y, x1 + 12, y, INK, 2)]
    for v in (lo, hi):
        s.append(line(X(v), y - 9, X(v), y + 9, INK, 2.5))
        s.append(text(X(v), y + 30, comma(v), 15))
    if show_mid:
        m = lo + p // 2
        s.append(line(X(m), y - 6, X(m), y + 6, INK, 1.5))
        s.append(text(X(m), y + 30, comma(m), 13, col=GREEN, weight=400))
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(n), y, RED))
    s.append(text(X(n), y - 16, comma(n) if show_n else "?", 15, col=RED))
    return svg_wrap(W, y + 40, "".join(s), "number line from %s to %s with a point at %s" % (comma(lo), comma(hi), comma(n) if show_n else "a number"))


def pick(r, p, digits):
    while True:
        n = r.randint(10 ** (digits - 1), 10 ** digits - 1)
        if n % p and n // p * p >= 10 and n % p != p // 2 or (n % p == p // 2 and r.random() < 0.15):
            return n


# ------------------------------------------------------------ set 1: between which multiples?
def one_between(r):
    p = r.choice([10, 100, 1000, 10000])
    n = pick(r, p, {10: 3, 100: 4, 1000: 5, 10000: 5}[p])
    lo = n // p * p
    show = lambda a, b: "%s and %s" % (comma(a), comma(b))
    right = show(lo, lo + p)
    wrong = [show(lo - p, lo) if lo - p >= 0 else show(lo + p, lo + 2 * p), show(lo + p, lo + 2 * p), show(n // (p // 10) * (p // 10), n // (p // 10) * (p // 10) + p // 10) if p >= 100 else show(lo, lo + 100)]
    kind = r.choice(["between", "closer"])
    if kind == "between":
        return mcq(fig(round_line(n, p, show_mid=False)) + "%s is between which two multiples of %s?" % (comma(n), comma(p)), right, wrong,
                   "Look at the place you round to. %s is between <b>%s</b>." % (comma(n), right))
    if n % p == p // 2:
        return None
    near = rnd_to(n, p)
    far = lo if near != lo else lo + p
    return mcq(fig(round_line(n, p)) + "Is %s closer to %s or %s?" % (comma(n), comma(lo), comma(lo + p)), comma(near), [comma(far), comma(lo + p // 2), "It is the same distance"],
               "The halfway point is %s. %s is %s it, so it is closer to <b>%s</b>." % (comma(lo + p // 2), comma(n), "below" if n % p < p // 2 else "above", comma(near)))


# ------------------------------------------------------------ set 2 and 3: round
def one_round(r, places):
    p = r.choice(places)
    digits = {10: r.choice([3, 4]), 100: r.choice([3, 4]), 1000: r.choice([4, 5]), 10000: 5}[p]
    n = pick(r, p, digits)
    right = rnd_to(n, p)
    lo = n // p * p
    other = lo if right != lo else lo + p
    wrong = [other, rnd_to(n, p // 10) if p >= 100 else rnd_to(n, 100), rnd_to(n, p * 10) if rnd_to(n, p * 10) != right else lo + 2 * p,
             right + n % p]
    pic = fig(round_line(n, p)) if r.random() < 0.35 else ""
    d = (n // (p // 10)) % 10
    return mcq(pic + "Round %s to the nearest <b>%s</b>." % (comma(n), PL[p]), right, wrong,
               "Look at the digit to the right of the %s place: %d. %s, so round %s. <b>%s</b>." % (PL[p] + "s", d, "5 or more" if d >= 5 else "Less than 5", "up" if d >= 5 else "down", comma(right)), allow_zero=False)


def one_round_small(r):
    return one_round(r, [10, 100])


def one_round_big(r):
    return one_round(r, [1000, 10000])


# ------------------------------------------------------------ set 4: estimate sums and differences
def one_estimate(r):
    kind = r.choice(["sum10", "sum100", "diff100", "compat"])
    if kind == "compat":
        a, b = r.randint(12, 98), r.randint(12, 98)
        ca, cb = rnd_to(a, 25) if rnd_to(a, 25) % 50 == 25 else rnd_to(a, 25), rnd_to(b, 25)
        if ca == 0 or cb == 0 or ca == a or cb == b or abs(ca - a) > 10 or abs(cb - b) > 10 or abs(ca - a) * 2 == 25:
            return None
        return mcq("Use compatible numbers to estimate %d + %d. Which is the best estimate?" % (a, b), "%d + %d = %d" % (ca, cb, ca + cb),
                   ["%d + %d = %d" % (a, b, a + b), "%d + %d = %d" % (rnd_to(a, 100), rnd_to(b, 100), rnd_to(a, 100) + rnd_to(b, 100)) if rnd_to(a, 100) and rnd_to(b, 100) else "%d + %d = %d" % (a // 10 * 10, b // 10 * 10, a // 10 * 10 + b // 10 * 10),
                    "%d + %d = %d" % (ca + 25, cb + 25, ca + cb + 50)],
                   "Compatible numbers are easy to add, like numbers that end in 25, 50, 75 or 00: <b>%d + %d = %d</b>." % (ca, cb, ca + cb))
    p = 10 if kind == "sum10" else 100
    a = r.randint(110, 880)
    b = r.randint(110, 880)
    if kind == "diff100" and a < b:
        a, b = b, a
    if kind != "diff100" and a + b >= 1000:
        return None
    ra, rb = rnd_to(a, p), rnd_to(b, p)
    if ra == a or rb == b or (kind == "diff100" and ra == rb):
        return None
    op = "−" if kind == "diff100" else "+"
    est = ra - rb if op == "−" else ra + rb
    exact = a - b if op == "−" else a + b
    wrong = [exact, (a // p * p - b // p * p) if op == "−" else a // p * p + b // p * p, est + p]
    return mcq("Round each number to the nearest %s to estimate %d %s %d." % (PL[p], a, op, b), est, wrong,
               "%d is about %d and %d is about %d. %d %s %d = <b>%s</b>." % (a, ra, b, rb, ra, op, rb, comma(est)))


# ------------------------------------------------------------ set 5: word problems
def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["crowd", "crowd", "est_sum", "est_diff", "reason"])
    if kind == "crowd":
        n = r.randint(12000, 98000)
        if n % 1000 in (0, 500):
            return None
        p = r.choice([1000, 10000])
        what = r.choice(["fans watched a football game in Houston", "people ran in a marathon in Austin", "people visited a zoo in San Antonio last month", "people went to a rodeo in Fort Worth"])
        right = rnd_to(n, p)
        lo = n // p * p
        return mcq("%s %s. About how many is that, rounded to the nearest %s?" % (comma(n), what, PL[p]), right,
                   [lo if right != lo else lo + p, rnd_to(n, p // 10), rnd_to(n, 100)],
                   "Round %s to the nearest %s: <b>%s</b>." % (comma(n), PL[p], comma(right)))
    if kind == "est_sum":
        a, b = r.randint(120, 480), r.randint(120, 480)
        ra, rb = rnd_to(a, 100), rnd_to(b, 100)
        if ra == a or rb == b:
            return None
        return mcq("%s reads %d pages in June and %d pages in July. About how many pages is that? Round each number to the nearest hundred." % (k["n"], a, b), ra + rb,
                   [a + b, a // 100 * 100 + b // 100 * 100 if a // 100 * 100 + b // 100 * 100 != ra + rb else ra + rb + 100, ra + rb + 200],
                   "%d is about %d and %d is about %d. %d + %d = <b>%d</b>." % (a, ra, b, rb, ra, rb, ra + rb))
    if kind == "est_diff":
        a, b = r.randint(520, 980), r.randint(110, 480)
        ra, rb = rnd_to(a, 10), rnd_to(b, 10)
        if ra == a or rb == b:
            return None
        return mcq("A school has %d students. %d students ride the bus. About how many students do not ride the bus? Round each number to the nearest ten." % (a, b), ra - rb,
                   [a - b, ra + rb, ra - rb + 10, ra - rb - 10],
                   "%d is about %d and %d is about %d. %d − %d = <b>%d</b>." % (a, ra, b, rb, ra, rb, ra - rb))
    a, b = r.randint(210, 480), r.randint(210, 480)
    exact = a + b
    wrong_ans = exact + r.choice([200, 300, -200])
    est = rnd_to(a, 100) + rnd_to(b, 100)
    shown = r.choice([exact, wrong_ans])
    ok = abs(shown - est) <= 100
    right = "Yes. %d + %d is about %s" % (a, b, comma(est)) if ok else "No. %d + %d is about %s" % (a, b, comma(est))
    return mcq("%s says %d + %d = %s. Use rounding to check. Is %s answer reasonable?" % (k["n"], a, b, comma(shown), k["his"]), right,
               ["No. %d + %d is about %s" % (a, b, comma(est)) if ok else "Yes. %d + %d is about %s" % (a, b, comma(est)), "Yes. Every answer is reasonable", "We cannot check without the exact answer"],
               "Round to the nearest hundred: %d + %d = %d. %d is %s close to %d: <b>%s</b>." % (rnd_to(a, 100), rnd_to(b, 100), est, shown, "" if ok else "not", est, right))


def build():
    sets = [S("Between which multiples?", collect(one_between, 20, R)),
            S("Round to the nearest 10 and 100", collect(one_round_small, 20, R)),
            S("Round to the nearest 1,000 and 10,000", collect(one_round_big, 20, R)),
            S("Estimate sums and differences", collect(one_estimate, 20, R)),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Find the two multiples the number is <b>between</b>. 347 is between 300 and 400.</li>"
        "<li>Find the <b>halfway</b> point (350). Below it, round down. At it or above, round up.</li>"
        "<li>Short cut: look at the digit to the right of the place you round to. 0 to 4: round down. 5 to 9: round up.</li>"
        "<li>To <b>estimate</b>, round each number first, then add or subtract. Compatible numbers like 25, 50 and 75 are easy to add.</li></ul>",
        [figure(round_line(347, 100), "347 is below the halfway point 350, so it rounds to 300."),
         example("Estimate 486 + 231 by rounding to the nearest hundred.", ["486 is about 500.", "231 is about 200.", "500 + 200 = 700"], "about 700")],
        [["Rounding to the wrong place", "Underline the place you round to before you start."],
         ["Rounding 5 down", "5 or more rounds up: 350 rounds to 400."],
         ["Keeping the digits after the rounding place: 3,472 → 3,500 is right, 3,572 is not", "All digits to the right become 0."]])
    faq = [("What does TEKS 3.2C ask?", "Show a number on a number line between two multiples of 10, 100, 1,000 or 10,000, and use words to say which one it is closer to. This is how students learn to round."),
           ("How do you round to the nearest hundred?", "Look at the tens digit. If it is 5 or more, round up. If it is less than 5, round down, and change the tens and ones to 0."),
           ("What are compatible numbers?", "Numbers that are close to the real numbers and easy to work with in your head, like 25 + 75 or 250 + 150 (TEKS 3.4B)."),
           ("Why estimate?", "An estimate tells you about how much and helps you check if an exact answer is reasonable.")]
    make("rounding-and-estimating", 3, "Number and Operations", "3.2C, 3.4B",
         "3.2C represent a number on a number line as being between two consecutive multiples of 10; 100; 1,000; or 10,000 and use words to describe relative size of numbers in order to round whole numbers; 3.4B round to the nearest 10 or 100 or use compatible numbers to estimate solutions to addition and subtraction problems",
         "Rounding and Estimating: Number Lines and Compatible Numbers", "Rounding and Estimating",
         "Free Grade 3 rounding worksheets for Texas TEKS 3.2C and 3.4B: numbers between multiples on a number line, round to the nearest 10, 100, 1,000 and 10,000, estimate sums and differences, and word problems. 100 STAAR-style questions with answers.",
         "Find the halfway point. Below it, round down. At it or above, round up.", "Look at the digit to the right of the rounding place: 0 to 4 round down, 5 to 9 round up.",
         body, faq, sets, seo_title="Grade 3 Rounding and Estimating Worksheets: Number Lines (TEKS 3.2C, 3.4B, STAAR)")


if __name__ == "__main__":
    build()
