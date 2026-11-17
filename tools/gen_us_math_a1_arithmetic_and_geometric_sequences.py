# -*- coding: utf-8 -*-
"""
US Algebra 1: Arithmetic and Geometric Sequences (Common Core F-BF.A.2, F-IF.A.3, F-LE.A.2)
  python3 tools/gen_us_math_a1_arithmetic_and_geometric_sequences.py
Telling arithmetic from geometric sequences, explicit formulas for arithmetic sequences, geometric
sequences (common ratio, later terms, first term), recursive and explicit formulas in subscript notation,
and sequence word problems.
Wrong answers come from real mistakes: writing n + d instead of dn, using the first term as the constant,
using n instead of n − 1 in a(1)·r^(n−1), adding the ratio instead of multiplying, and confusing a
recursive rule with an explicit one.
"""
import random
from us_hs import num, B, S, make, lesson, collect, QN, T, expr, ordinal, MINUS

R = random.Random(91301)
N = "<i>n</i>"


def seq(ts):
    return ", ".join(num(t) for t in ts) + ", …"


def nth(a, b):
    return expr([(a, N), (b, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


# ------------------------------------------------------------ set 1: arithmetic or geometric, next term
def one_type(r):
    k = r.randint(0, 2)
    if k == 0:
        a, d = r.randint(-10, 20), nz(r, -9, 12)
        ts = [a + d * i for i in range(4)]
        q = "What is the next term? %s" % B(seq(ts))
        right = a + 4 * d
        e = "This is arithmetic: %s %s each time. %s %s %s = <b>%s</b>." % ("add" if d > 0 else "subtract", abs(d), num(ts[-1]), "+" if d > 0 else "−", abs(d), num(right))
        return QN(q, right, [ts[-1] + 2 * d, ts[-1] * 2, ts[-1] - d], e)
    if k == 1:
        a, rr = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, 4, 5, -2, -3])
        ts = [a * rr ** i for i in range(4)]
        if abs(ts[-1] * rr) > 5000:
            return None
        q = "What is the next term? %s" % B(seq(ts))
        right = ts[-1] * rr
        e = "This is geometric: multiply by %s each time. %s × %s = <b>%s</b>." % (num(rr), num(ts[-1]), "(%s)" % num(rr) if rr < 0 else num(rr), num(right))
        return QN(q, right, [ts[-1] + (ts[-1] - ts[-2]), ts[-1] * rr * -1, ts[-1] + rr], e)
    kinds = [("arithmetic", lambda: [r.randint(1, 9) + r.randint(2, 8) * i for i in range(5)] if False else None)]
    t = r.choice(["arith", "geo", "neither"])
    if t == "arith":
        a, d = r.randint(-5, 20), nz(r, -7, 9)
        ts = [a + d * i for i in range(5)]
        right = "Arithmetic"
        e = "The difference is always %s, so it is <b>arithmetic</b>." % num(d)
    elif t == "geo":
        a, rr = r.choice([1, 2, 3, 5, 7]), r.choice([2, 3, -2, 10])
        ts = [a * rr ** i for i in range(5)]
        right = "Geometric"
        e = "Each term is the one before × %s, so it is <b>geometric</b>." % num(rr)
    else:
        s0 = r.randint(1, 4)
        ts = [(s0 + i) ** 2 for i in range(5)] if r.random() < 0.5 else [(s0 + i) * (s0 + i + 1) // 2 for i in range(5)]
        right = "Neither"
        e = "The differences change (%s) and there is no common ratio, so it is <b>neither</b>." % ", ".join(num(ts[i + 1] - ts[i]) for i in range(4))
    q = "Is this sequence arithmetic, geometric or neither? %s" % B(seq(ts))
    return T(q, right, [w for w in ["Arithmetic", "Geometric", "Neither", "Both"] if w != right], e)


# ------------------------------------------------------------ set 2: nth term of an arithmetic sequence
def one_nth(r):
    a, b = nz(r, -8, 12), r.randint(-12, 12)
    if a == 1 and b == 0:
        return None
    ts = [a * i + b for i in range(1, 5)]
    q = "Find the %s th term of %s" % (N, B(seq(ts)))
    q = "What is the %s<sup>th</sup> term of %s?" % (N, B(seq(ts)))
    right = nth(a, b)
    wr = [nth(1, a), nth(a, ts[0]), nth(a, -b) if b else nth(a, a), expr([(b, N), (a, "")]) if b else nth(a + 1, -1)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    e = "The difference is %s, so start with %s. The 1st term of %s is %s; to get %s, %s. <b>%s</b>." % (
        num(a), expr([(a, N)]), expr([(a, N)]), num(a), num(ts[0]),
        ("add %s" % num(b)) if b > 0 else ("subtract %s" % num(-b)) if b < 0 else "add nothing", right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 3: geometric sequences
def one_geo(r):
    k = r.randint(0, 3)
    if k == 0:
        a, rr = r.choice([2, 3, 4, 5, 6, 10]), r.choice([2, 3, 4, 5, 10, -2, -3])
        ts = [a * rr ** i for i in range(4)]
        q = "What is the common ratio of %s" % B(seq(ts)) + "?"
        e = "Divide a term by the one before: %s ÷ %s = <b>%s</b>." % (num(ts[1]), num(ts[0]), num(rr))
        return QN(q, rr, [ts[1] - ts[0], -rr, rr + 1], e)
    if k == 1:
        a = r.choice([64, 80, 96, 160, 320, 128, 256, 400, 1000, 1600])
        rr = 2 if a % 16 == 0 or a in (80, 400) else 10
        if a == 1000:
            rr = 10
        ts = [a // rr ** i for i in range(4)]
        if ts[-1] * rr ** 3 != a or ts[-1] % rr:
            return None
        q = "Each term is the term before divided by %d. What is the next term? %s" % (rr, B(seq(ts)))
        right = ts[-1] // rr
        e = "%s ÷ %d = <b>%s</b>. The common ratio is %s." % (num(ts[-1]), rr, num(right), "½" if rr == 2 else "<sup>1</sup>/<sub>10</sub>")
        return QN(q, right, [ts[-1] - (ts[-2] - ts[-1]), ts[-1] * rr, ts[-1] - rr], e)
    if k == 2:
        a, rr = r.choice([1, 2, 3, 5]), r.choice([2, 3])
        n = r.randint(5, 7 if rr == 2 else 6)
        ts = [a * rr ** i for i in range(3)]
        q = "The sequence %s is geometric. What is the %s term?" % (B(seq(ts)), "%d<sup>%s</sup>" % (n, "th"))
        right = a * rr ** (n - 1)
        e = "Keep multiplying by %d: %s. The %d<sup>th</sup> term is <b>%s</b>." % (rr, ", ".join(num(a * rr ** i) for i in range(n)), n, num(right))
        return QN(q, right, [a * rr ** n, ts[0] + (n - 1) * (ts[1] - ts[0]), a * rr * n], e)
    a, rr = r.choice([1, 2, 3, 5, 4]), r.choice([2, 3, 10])
    m = r.randint(1, 4)
    ts = [a * rr ** i for i in range(m, m + 2)]
    q = "In a geometric sequence the %s and %s terms are %s and %s. What is the 1st term if every term is a whole number and the ratio is %d?" % ("%d<sup>th</sup>" % (m + 1) if m + 1 > 3 else ["", "1st", "2nd", "3rd"][m + 1], "%d<sup>th</sup>" % (m + 2) if m + 2 > 3 else ["", "1st", "2nd", "3rd"][m + 2], num(ts[0]), num(ts[1]), rr)
    q = "A geometric sequence has common ratio %d. Its %s term is %s. What is its 1st term?" % (rr, ordn(m + 1), num(a * rr ** m))
    right = a
    e = "Divide by %d %d time%s: %s ÷ %s = <b>%s</b>." % (rr, m, "" if m == 1 else "s", num(a * rr ** m), num(rr ** m), num(a))
    return QN(q, right, [a * rr ** m - m * rr, a * rr, a * rr ** m // (rr * (m + 1)) if (a * rr ** m) % (rr * (m + 1)) == 0 else a + rr], e)


def ordn(n):
    return ordinal(n)


# ------------------------------------------------------------ set 4: using the <i>n</i>th term
def A(k):
    return "<i>a</i><sub>%s</sub>" % k


def one_rec(r):
    kind = r.choice(["ar_term", "geo_term", "ar_explicit", "geo_explicit", "rec_write", "geo_rec"])
    if kind == "ar_term":
        a1, d = r.randint(-6, 15), nz(r, -6, 8)
        n = r.randint(4, 6)
        q = "A sequence is defined by %s and %s. What is %s?" % (B("%s = %s" % (A(1), num(a1))), B("%s = %s" % (A("<i>n</i>"), expr([(1, A("<i>n</i>−1")), (d, "")]))), B(A(n)))
        v = a1 + (n - 1) * d
        e = "Start at %s and %s %s each time: %s. So %s = <b>%s</b>." % (num(a1), "add" if d > 0 else "subtract", num(abs(d)), ", ".join(num(a1 + i * d) for i in range(n)), A(n), num(v))
        return QN(q, v, [a1 + n * d, a1 + (n - 2) * d, a1 * d ** (n - 1) if abs(a1 * d ** (n - 1)) < 5000 else v + 2 * d], e)
    if kind == "geo_term":
        a1, rr = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, -2])
        n = r.randint(4, 6)
        q = "A sequence is defined by %s and %s. What is %s?" % (B("%s = %s" % (A(1), num(a1))), B("%s = %s · %s" % (A("<i>n</i>"), "(%s)" % num(rr) if rr < 0 else num(rr), A("<i>n</i>−1"))), B(A(n)))
        v = a1 * rr ** (n - 1)
        e = "Start at %s and multiply by %s each time: %s. So %s = <b>%s</b>." % (num(a1), num(rr), ", ".join(num(a1 * rr ** i) for i in range(n)), A(n), num(v))
        return QN(q, v, [a1 * rr ** n, a1 + (n - 1) * rr, a1 * rr * (n - 1)], e)
    if kind == "ar_explicit":
        a1, d = r.randint(-5, 12), nz(r, -6, 8)
        ts = [a1 + i * d for i in range(4)]
        q = "Which explicit formula gives the sequence %s?" % B(seq(ts))
        right = "%s = %s + %s(<i>n</i> − 1)" % (A("<i>n</i>"), num(a1), "(%s)" % num(d) if d < 0 else num(d))
        wr = ["%s = %s + %s<i>n</i>" % (A("<i>n</i>"), num(a1), "(%s)" % num(d) if d < 0 else num(d)),
              "%s = %s + %s(<i>n</i> − 1)" % (A("<i>n</i>"), num(d), "(%s)" % num(a1) if a1 < 0 else num(a1)) if a1 != d else "%s = %s(<i>n</i> − 1)" % (A("<i>n</i>"), num(d)),
              "%s = %s · %s<sup><i>n</i> − 1</sup>" % (A("<i>n</i>"), num(a1), "(%s)" % num(d) if d < 0 else num(d))]
        e = "For an arithmetic sequence, %s = %s + <i>d</i>(<i>n</i> − 1). Here %s = %s and <i>d</i> = %s: <b>%s</b>." % (A("<i>n</i>"), A(1), A(1), num(a1), num(d), right)
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    if kind == "geo_explicit":
        a1, rr = r.choice([2, 3, 4, 5, 6, 10]), r.choice([2, 3, 4, 5])
        if a1 == rr:
            return None
        ts = [a1 * rr ** i for i in range(4)]
        q = "Which explicit formula gives the sequence %s?" % B(seq(ts))
        right = "%s = %s · %s<sup><i>n</i> − 1</sup>" % (A("<i>n</i>"), num(a1), num(rr))
        wr = ["%s = %s · %s<sup><i>n</i></sup>" % (A("<i>n</i>"), num(a1), num(rr)), "%s = %s · %s<sup><i>n</i> − 1</sup>" % (A("<i>n</i>"), num(rr), num(a1)),
              "%s = %s + %s(<i>n</i> − 1)" % (A("<i>n</i>"), num(a1), num(ts[1] - ts[0]))]
        e = "For a geometric sequence, %s = %s · <i>r</i><sup><i>n</i> − 1</sup>. Here %s = %s and <i>r</i> = %s: <b>%s</b>." % (A("<i>n</i>"), A(1), A(1), num(a1), num(rr), right)
        return T(q, right, wr, e)
    if kind == "rec_write":
        a1, d = r.randint(-5, 15), nz(r, -6, 9)
        ts = [a1 + i * d for i in range(4)]
        q = "Which recursive formula gives the sequence %s?" % B(seq(ts))
        right = "%s = %s; %s = %s" % (A(1), num(a1), A("<i>n</i>"), expr([(1, A("<i>n</i>−1")), (d, "")]))
        wr = ["%s = %s; %s = %s" % (A(1), num(d), A("<i>n</i>"), expr([(1, A("<i>n</i>−1")), (a1, "")])) if a1 else "%s = %s; %s = %s" % (A(1), num(d), A("<i>n</i>"), A("<i>n</i>−1")),
              "%s = %s; %s = %s" % (A(1), num(a1), A("<i>n</i>"), expr([(1, A("<i>n</i>−1")), (-d, "")])),
              "%s = %s; %s = %s · %s" % (A(1), num(a1), A("<i>n</i>"), "(%s)" % num(d) if d < 0 else num(d), A("<i>n</i>−1"))]
        e = "A recursive formula gives the first term and how to get each term from the one before: <b>%s</b>." % right
        return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)
    a1, rr = r.choice([1, 2, 3, 5, 7]), r.choice([2, 3, 4, -2])
    ts = [a1 * rr ** i for i in range(4)]
    q = "Which recursive formula gives the sequence %s?" % B(seq(ts))
    rs = "(%s)" % num(rr) if rr < 0 else num(rr)
    right = "%s = %s; %s = %s · %s" % (A(1), num(a1), A("<i>n</i>"), rs, A("<i>n</i>−1"))
    wr = ["%s = %s; %s = %s" % (A(1), num(a1), A("<i>n</i>"), expr([(1, A("<i>n</i>−1")), (rr, "")])), "%s = %s; %s = %s · %s" % (A(1), num(rr), A("<i>n</i>"), num(a1), A("<i>n</i>−1")) if a1 != rr else "%s = %s; %s = %s · %s" % (A(1), num(a1), A("<i>n</i>"), num(rr + 1), A("<i>n</i>−1")),
          "%s = %s · %s<sup><i>n</i></sup>" % (A("<i>n</i>"), num(a1), rs)]
    e = "Each term is the one before times %s: <b>%s</b>." % (num(rr), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


def problems():
    data = [
        ("What is the next term of the Fibonacci sequence 1, 1, 2, 3, 5, 8, …?", "13", ["11", "16", "10"], "Add the two terms before: 5 + 8 = <b>13</b>."),
        ("A geometric sequence has <i>a</i><sub>1</sub> = 5 and <i>r</i> = 2. Which is <i>a</i><sub>8</sub>?", "640", ["1,280", "80", "320"], "<i>a</i><sub>8</sub> = 5 · 2<sup>7</sup> = 5 × 128 = <b>640</b>."),
        ("What is the next triangular number? 1, 3, 6, 10, 15, …", "21", ["20", "25", "18"], "The differences go up by 1: +2, +3, +4, +5, so add 6: <b>21</b>."),
        ("A theater has 20 seats in row 1, 23 in row 2, 26 in row 3, and so on. How many seats are in row 15?", "62", ["65", "59", "45"], "<i>a</i><sub><i>n</i></sub> = 20 + 3(<i>n</i> − 1), so <i>a</i><sub>15</sub> = 20 + 42 = <b>62</b>."),
        ("A bacteria population doubles every hour. It starts at 50. How many are there after 5 hours?", "1,600", ["250", "800", "3,200"],
         "50 → 100 → 200 → 400 → 800 → <b>1,600</b>. This is a geometric sequence with ratio 2."),
        ("Grace saves $5 in week 1, $8 in week 2, $11 in week 3, and so on. How much does she save in week 10?", "$32", ["$35", "$50", "$29"],
         "The <i>n</i>th term is 3<i>n</i> + 2. Week 10: 3 × 10 + 2 = <b>$32</b>."),
        ("A ball is dropped from 200 cm. Each bounce reaches half the height of the one before. How high is the 3rd bounce?", "25 cm", ["50 cm", "100 cm", "12.5 cm"],
         "200 × ½ = 100 (1st), 50 (2nd), <b>25 cm</b> (3rd)."),
        ("Patterns are made from sticks: 4, 7, 10, 13, … sticks. How many sticks are in pattern 20?", "61", ["64", "80", "58"],
         "The <i>n</i>th term is 3<i>n</i> + 1. Pattern 20: 3 × 20 + 1 = <b>61</b>."),
        ("Patterns are made from sticks: 4, 7, 10, 13, … sticks. Which pattern uses 100 sticks?", "Pattern 33", ["Pattern 34", "Pattern 25", "Pattern 30"],
         "3<i>n</i> + 1 = 100, so 3<i>n</i> = 99 and <i>n</i> = 33. <b>Pattern 33</b>."),
        ("The <i>n</i>th term of a sequence is 50 − 4<i>n</i>. What is the first negative term?", "−2", ["−4", "2", "−6"],
         "50 − 4<i>n</i> &lt; 0 when <i>n</i> &gt; 12.5, so <i>n</i> = 13: 50 − 52 = <b>−2</b>."),
        ("Which sequence has the <i>n</i>th term 5 − 2<i>n</i>?", "3, 1, −1, −3, …", ["5, 3, 1, −1, …", "−2, 3, 8, 13, …", "3, 5, 7, 9, …"],
         "<i>n</i> = 1 gives 3, <i>n</i> = 2 gives 1, then −1 and −3: <b>3, 1, −1, −3, …</b>"),
        ("A car worth $16,000 loses half its value every 3 years. What is it worth after 9 years?", "$2,000", ["$4,000", "$8,000", "$1,000"],
         "9 years is 3 halvings: $16,000 → $8,000 → $4,000 → <b>$2,000</b>."),
        ("Find the missing term in the geometric sequence 3, ☐, 75, 375, …", "15", ["39", "25", "45"],
         "The ratio is 375 ÷ 75 = 5, so 3 × 5 = <b>15</b>."),
        ("Find the missing term in the arithmetic sequence 7, ☐, 19, 25, …", "13", ["12", "14", "16"],
         "The difference is 6, so 7 + 6 = <b>13</b>."),
        ("Which is the <i>n</i>th term of 2, 4, 8, 16, …?", "2<sup><i>n</i></sup>", ["2<i>n</i>", "<i>n</i><sup>2</sup>", "<i>n</i> + 2"],
         "Each term is a power of 2: 2<sup>1</sup>, 2<sup>2</sup>, 2<sup>3</sup>, … so the <i>n</i>th term is <b>2<sup><i>n</i></sup></b>."),
        ("Which is the <i>n</i>th term of 1, 4, 9, 16, …?", "<i>n</i><sup>2</sup>", ["3<i>n</i> − 2", "2<sup><i>n</i></sup>", "4<i>n</i>"],
         "These are the square numbers: <b><i>n</i><sup>2</sup></b>."),
        ("Ethan says 2, 6, 18, 54, … is arithmetic because the numbers go up. Is he right?", "No, it is geometric with ratio 3", ["Yes, the difference is 4", "Yes, the difference is 3", "No, it is neither"],
         "The differences are 4, 12, 36, which are not equal. Each term is × 3: <b>geometric with ratio 3</b>."),
        ("The 5th term of an arithmetic sequence is 23 and the 6th term is 27. What is the 1st term?", "7", ["3", "4", "11"],
         "The difference is 4. Go back 4 steps from the 5th term: 23 − 16 = <b>7</b>."),
        ("A sequence starts 3, 7, and each term is twice the term before minus 1. What is the 4th term?", "25", ["13", "27", "29"],
         "3rd: 2 × 7 − 1 = 13. 4th: 2 × 13 − 1 = <b>25</b>."),
        ("How many terms of 7, 11, 15, 19, … are less than 100?", "24", ["23", "25", "93"],
         "The <i>n</i>th term is 4<i>n</i> + 3. 4<i>n</i> + 3 &lt; 100 when <i>n</i> &lt; 24.25, so <b>24</b> terms."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>In an <b>arithmetic</b> sequence you <b>add</b> the same number each time (the common difference). "
        "Its <i>n</i><sup>th</sup> term is <i>dn</i> + <i>c</i>, where <i>d</i> is the difference.</p>"
        "<p>In a <b>geometric</b> sequence you <b>multiply</b> by the same number each time (the common ratio). "
        "Find the ratio by dividing a term by the term before. Square, cube, triangular and Fibonacci numbers are other special sequences.</p>",
        [("Find the <i>n</i><sup>th</sup> term of 5, 8, 11, 14, …", ["The difference is 3, so start with 3<i>n</i>: 3, 6, 9, 12.", "Each term is 2 more."], "3<i>n</i> + 2"),
         ("Find the next term of 3, 6, 12, 24, …", ["The ratio is 6 ÷ 3 = 2.", "24 × 2."], "48"),
         ("Is 50 in the sequence 3<i>n</i> + 2?", ["3<i>n</i> + 2 = 50 gives 3<i>n</i> = 48, <i>n</i> = 16."], "Yes, the 16th term")],
        ["Writing <i>n</i> + 3 for a difference of 3. It should be 3<i>n</i>.",
         "Using the first term as the constant: 5, 8, 11, … is 3<i>n</i> + 2, not 3<i>n</i> + 5.",
         "Adding the ratio instead of multiplying in a geometric sequence.",
         "Calling square numbers arithmetic. Their differences are 3, 5, 7, … which are not equal."])


def main():
    sets = [S("Arithmetic or geometric?", collect(one_type, 20, R)),
            S("The nth term of arithmetic sequences", collect(one_nth, 20, R)),
            S("Geometric sequences", collect(one_geo, 20, R)),
            S("Recursive and explicit formulas", collect(one_rec, 20, R)),
            S("Sequence problems", problems())]
    make("arithmetic-and-geometric-sequences", 13, "F-BF.A.2",
         "Arithmetic and Geometric Sequences: Explicit and Recursive Formulas",
         "Algebra 1 Arithmetic and Geometric Sequences Worksheets: Explicit and Recursive Formulas (Free, Answer Key)",
         "Arithmetic and geometric sequences",
         "Write arithmetic and geometric sequences both recursively and with an explicit formula, use them to model situations, and translate between the two forms.",
         "Free Algebra 1 sequences worksheets (F-BF.A.2, F-IF.A.3): arithmetic or geometric, explicit formulas a(n) = a(1) + d(n − 1) and "
         "a(n) = a(1) · r^(n − 1), recursive formulas, common ratios and word problems. 100 questions with an answer key.",
         "Arithmetic: add d each time, aₙ = a₁ + d(n − 1). Geometric: multiply by r, aₙ = a₁ · rⁿ⁻¹.",
         "A recursive formula uses the term before; an explicit formula jumps straight to any term.",
         body(),
         [("What is the difference between arithmetic and geometric sequences?", "In an arithmetic sequence you add the same amount each time. In a geometric sequence you multiply by the same amount each time."),
          ("How do I find the nth term of an arithmetic sequence?", "Find the common difference d and write dn. Then compare dn with the sequence to find the number to add or subtract."),
          ("How do I find the common ratio?", "Divide any term by the term before it. For 3, 12, 48, … the ratio is 12 ÷ 3 = 4."),
          ("What is the difference between a recursive and an explicit formula?", "A recursive formula gives the first term and how to get each term from the one before. An explicit formula gives any term directly from n.")],
         sets, R, domain="Exponents & Exponential Functions")


if __name__ == "__main__":
    main()
