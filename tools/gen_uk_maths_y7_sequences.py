# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Sequences (KS3 Algebra)
  python3 tools/gen_uk_maths_y7_sequences.py
Term-to-term rules, finding the nth term of a linear sequence, using the nth term, deciding whether a
number is in a sequence, special sequences, and pattern problems.
Wrong answers come from real mistakes: writing n + 3 for “goes up in 3s”, forgetting the zero term,
and confusing the position with the term.
"""
import random
from fractions import Fraction as F
from uk_ks3 import ordinal, num, mcq, B, S, make, lesson, collect, QN, T, expr, MINUS, svg_wrap, line, text, fig, GREEN, INK

R = random.Random(71401)
N = "<i>n</i>"


def nth(a, b):
    return expr([(a, N), (b, "")])


def terms(a, b, k=4, start=1):
    return [a * i + b for i in range(start, start + k)]


def show(ts):
    return ", ".join(num(t) for t in ts) + ", …"


# ------------------------------------------------------------ set 1: next terms and term-to-term rule
def one_next(r):
    d = r.choice([2, 3, 4, 5, 6, 7, 9, 11, -2, -3, -4, -5, -6, F(1, 2), F(3, 10), F(5, 10)])
    a1 = F(r.randint(-10, 30))
    ts = [a1 + d * i for i in range(5)]
    kind = r.random()
    if kind < 0.5:
        q = "What is the next term in the sequence %s?" % B(show(ts[:4]))
        ans = ts[4]
        e = "The term-to-term rule is %s %s. %s %s %s = <b>%s</b>." % (
            "add" if d > 0 else "subtract", num(abs(d)), num(ts[3]), "+" if d > 0 else MINUS, num(abs(d)), num(ans))
        return QN(q, ans, [ts[3] - d, ts[3] + 2 * d, ts[3] * 2 if d > 0 else ts[3] + abs(d)], e, near=(1, -1, F(1, 2)))
    q = "What is the term-to-term rule for %s?" % B(show(ts[:4]))
    right = ("Add %s" if d > 0 else "Subtract %s") % num(abs(d))
    wr = [("Subtract %s" if d > 0 else "Add %s") % num(abs(d)), "Add %s" % num(ts[0]) if ts[0] > 0 and ts[0] != d else "Multiply by 2",
          ("Add %s" if d > 0 else "Subtract %s") % num(abs(d) + 1)]
    e = "Find the difference between neighbouring terms: %s − %s = %s. Rule: <b>%s</b>." % (num(ts[1]), num(ts[0]) if ts[0] >= 0 else "(%s)" % num(ts[0]), num(d), right.lower())
    return T(q, right, wr, e)


def one_geo(r):
    m = r.choice([2, 3, 10, F(1, 2)])
    a1 = r.choice([1, 2, 3, 5, 64, 160, 1000]) if m == F(1, 2) else r.choice([1, 2, 3, 4, 5])
    ts = [F(a1) * m ** i for i in range(5)]
    if ts[4].denominator > 4:
        return None
    q = "What is the next term in the sequence %s?" % B(show(ts[:4]))
    d = ts[3] - ts[2]
    e = "Each term is %s. The next term is <b>%s</b>." % (
        "the one before multiplied by %s" % num(m) if m > 1 else "half of the one before", num(ts[4]))
    return QN(q, ts[4], [ts[3] + d, ts[3] + (ts[1] - ts[0]), ts[3] * 2 if m != 2 else ts[3] * 3], e)


# ------------------------------------------------------------ set 2: find the nth term
def one_find_nth(r):
    a = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, -2, -3, -4, -5])
    b = r.randint(-9, 12)
    ts = terms(a, b)
    if ts[0] == 0:
        return None
    q = "Find the %s term of the sequence %s" % (B("<i>n</i>th"), B(show(ts)))
    right = nth(a, b)
    wr = [expr([(1, N), (a, "")]),                     # n + d
          nth(a, ts[0]) if ts[0] != b else nth(a, b + 1),  # used the first term
          nth(b, a) if b not in (0, 1, -1) and b != a else nth(-a, b)]
    e = "The difference is %s, so the sequence is like %s. The zero term is %s %s %s = %s. So the <i>n</i>th term is <b>%s</b>." % (
        num(a), expr([(a, N)]), num(ts[0]), MINUS if a > 0 else "+", num(abs(a)), num(b), right)
    return T(q, right, [w for w in wr if w != right], e)


# ------------------------------------------------------------ set 3: use the nth term
def one_use(r):
    a = r.choice([2, 3, 4, 5, 6, 7, 8, 9, -2, -3])
    b = r.randint(-9, 15)
    k = r.choice([5, 10, 12, 20, 25, 50, 100])
    if r.random() < 0.6:
        val = a * k + b
        q = "The <i>n</i>th term of a sequence is %s. Find the %s term." % (B(nth(a, b)), B(ordinal(k)))
        e = "Substitute <i>n</i> = %d: %s × %d %s %d = <b>%s</b>." % (k, num(a), k, "+" if b >= 0 else MINUS, abs(b), num(val))
        return QN(q, val, [a * (k + b), a + k + b, int("%d%d" % (a, k)) + b if a > 0 else -val], e)
    ts = terms(a, b, 3)
    q = "The <i>n</i>th term of a sequence is %s. What are the first three terms?" % B(nth(a, b))
    right = ", ".join(num(t) for t in ts)
    wr = [", ".join(num(t) for t in terms(a, b, 3, 0)), ", ".join(num(b + a * i) for i in (1, 1 + 1, 2 + 1)) if False else ", ".join(num(t + a) for t in ts),
          ", ".join(num(a + b + i) for i in range(3)), ", ".join(num(b * i + a) for i in range(1, 4)) if b != a else ", ".join(num(-t) for t in ts)]
    e = "Substitute <i>n</i> = 1, 2, 3: <b>%s</b>." % right
    return T(q, right, [w for w in wr if w != right][:3], e)


# ------------------------------------------------------------ set 4: is it in the sequence?
def one_in(r):
    a = r.choice([3, 4, 5, 6, 7, 8])
    b = r.randint(-5, 9)
    k = r.randint(8, 40)
    val = a * k + b
    if r.random() < 0.5:
        q = "The <i>n</i>th term of a sequence is %s. Which term is equal to %s?" % (B(nth(a, b)), B(num(val)))
        e = "%s = %d, so %d<i>n</i> = %d and <i>n</i> = %d. It is the <b>%s</b> term." % (nth(a, b), val, a, val - b, k, ordinal(k))
        return mcq(q, ("The %s term" % ordinal(k), k), [("The %s term" % ordinal(w), w) for w in [k + 1, k - 1, val // a if val // a != k else k + 2, val - b] if w != k], e)
    off = r.choice([1, 2]) if a > 2 else 1
    cand = [a * k + b, a * (k + 3) + b + off, a * (k + 6) + b - off, a * (k + 9) + b + off]
    good = cand[0]
    q = "The <i>n</i>th term of a sequence is %s. Which of these numbers is in the sequence?" % B(nth(a, b))
    e = "%s = %d gives <i>n</i> = (%d %s %d) ÷ %d = %d, a whole number. The others do not give whole numbers. So <b>%d</b>." % (
        nth(a, b), good, good, MINUS if b >= 0 else "+", abs(b), a, k, good)
    return QN(q, good, cand[1:], e)


# ------------------------------------------------------------ set 5: special sequences and patterns
def pattern_svg(k):
    """Matchstick squares in a row: pattern k has k squares."""
    s = []
    u = 34
    for p in range(1, 4):
        x0 = 20 + (p - 1) * 150
        for i in range(p + 1):
            s.append(line(x0 + i * u, 20, x0 + i * u, 20 + u, GREEN, 4))
        for i in range(p):
            s.append(line(x0 + i * u, 20, x0 + (i + 1) * u, 20, GREEN, 4))
            s.append(line(x0 + i * u, 20 + u, x0 + (i + 1) * u, 20 + u, GREEN, 4))
        s.append(text(x0 + p * u / 2, 82, "Pattern %d" % p, 13))
    return svg_wrap(480, 92, "".join(s), "matchstick patterns of 1, 2 and 3 squares")


def problems():
    its = []
    sq = pattern_svg(3)
    for k in (10, 25):
        val = 3 * k + 1
        its.append(QN("The patterns are made from matchsticks. How many matchsticks are in Pattern %d?%s" % (k, fig(sq)), val,
                      [4 * k, 3 * k, k + 3], "The sticks go 4, 7, 10, … so the <i>n</i>th term is 3<i>n</i> + 1. Pattern %d: 3 × %d + 1 = <b>%d</b>." % (k, k, val)))
    its.append(T("The patterns are made from matchsticks. What is the <i>n</i>th term for the number of matchsticks?%s" % fig(sq),
                 "3<i>n</i> + 1", ["<i>n</i> + 3", "4<i>n</i>", "3<i>n</i> + 4"], "4, 7, 10, … goes up by 3, and the zero term is 1: <b>3<i>n</i> + 1</b>."))
    its.append(QN("The patterns are made from matchsticks. Which pattern uses 61 matchsticks?%s" % fig(sq), 20, [21, 15, 183],
                  "3<i>n</i> + 1 = 61, so 3<i>n</i> = 60 and <i>n</i> = <b>20</b>."))
    data = [
        ("Which of these is the sequence of square numbers?", "1, 4, 9, 16, 25", ["2, 4, 6, 8, 10", "1, 3, 6, 10, 15", "1, 2, 4, 8, 16"], "Square numbers are 1², 2², 3², …: <b>1, 4, 9, 16, 25</b>."),
        ("Which of these is the sequence of triangular numbers?", "1, 3, 6, 10, 15", ["1, 4, 9, 16, 25", "3, 6, 9, 12, 15", "1, 2, 3, 5, 8"], "Triangular numbers add 2, then 3, then 4, …: <b>1, 3, 6, 10, 15</b>."),
        ("What is the next term in the Fibonacci sequence 1, 1, 2, 3, 5, 8, …?", "13", ["11", "16", "10"], "Each term is the sum of the two before: 5 + 8 = <b>13</b>."),
        ("What is the next term? 1, 3, 6, 10, 15, …", "21", ["20", "18", "25"], "The differences are 2, 3, 4, 5, so add 6: 15 + 6 = <b>21</b>."),
        ("Which sequence is geometric?", "3, 6, 12, 24, …", ["3, 6, 9, 12, …", "1, 4, 9, 16, …", "1, 1, 2, 3, …"], "In a geometric sequence you multiply by the same number each time (here × 2): <b>3, 6, 12, 24, …</b>."),
        ("Which sequence is arithmetic (linear)?", "20, 17, 14, 11, …", ["1, 2, 4, 8, …", "1, 4, 9, 16, …", "2, 3, 5, 8, …"], "An arithmetic sequence goes up or down by the same amount (here − 3): <b>20, 17, 14, 11, …</b>."),
        ("The first term of a sequence is 5. The rule is “double and subtract 1”. What is the third term?", "17", ["9", "19", "13"], "5 → 2 × 5 − 1 = 9 → 2 × 9 − 1 = <b>17</b>."),
        ("The 1st term is 50. The rule is “subtract 7”. What is the first negative term?", "−6", ["−1", "−7", "1"], "50, 43, 36, 29, 22, 15, 8, 1, <b>−6</b>."),
        ("A sequence has <i>n</i>th term 5<i>n</i> − 2. Is 101 in the sequence?", "No, because (101 + 2) ÷ 5 is not a whole number", ["Yes, it is the 20th term", "Yes, it is the 21st term", "No, because 101 is odd"],
         "5<i>n</i> − 2 = 101 gives <i>n</i> = 103 ÷ 5 = 20.6, not a whole number. So <b>no</b>."),
        ("Chairs are arranged in rows. Row 1 has 12 chairs and each row has 2 more than the row before. How many chairs are in row 15?", "40", ["42", "30", "38"],
         "<i>n</i>th term = 2<i>n</i> + 10. Row 15: 2 × 15 + 10 = <b>40</b>."),
        ("A gym plan costs £30 for the first month and £18 for each month after that. What is the <i>n</i>th term for the total cost after <i>n</i> months?", "18<i>n</i> + 12",
         ["18<i>n</i> + 30", "30<i>n</i> + 18", "12<i>n</i> + 18"], "Totals: 30, 48, 66, … go up by 18; zero term 30 − 18 = 12. So <b>18<i>n</i> + 12</b>."),
        ("Which term of 7, 11, 15, 19, … is 87?", "20th", ["21st", "22nd", "19th"], "<i>n</i>th term = 4<i>n</i> + 3. 4<i>n</i> + 3 = 87, so <i>n</i> = <b>20</b>."),
        ("The temperature is 9 °C at 6 pm and falls 2 °C every hour. What is it at midnight?", "−3 °C", ["−5 °C", "−1 °C", "3 °C"], "6 hours later: 9 − 6 × 2 = <b>−3 °C</b>."),
        ("What is the 6th term of the sequence with <i>n</i>th term <i>n</i>² + 1?", "37", ["13", "36", "49"], "6² + 1 = 36 + 1 = <b>37</b>."),
        ("The <i>n</i>th term is 20 − 3<i>n</i>. What is the first term that is negative?", "−1", ["−3", "2", "−4"], "20 − 3<i>n</i>: 17, 14, 11, 8, 5, 2, <b>−1</b>."),
        ("The first two terms of a sequence are 4 and 9. Each term after that is the sum of the two before it. What is the 5th term?", "35", ["22", "13", "31"], "4, 9, 13, 22, <b>35</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>A <b>term-to-term rule</b> tells you how to get from one term to the next, for example “add 3”.</p>"
        "<p>A <b>position-to-term rule</b> (the <i>n</i>th term) lets you find any term. For a linear sequence: "
        "the number in front of <i>n</i> is the difference, and the number added is the <b>zero term</b> (the term "
        "before the first).</p>",
        [("Find the <i>n</i>th term of 5, 8, 11, 14, …", ["The difference is 3, so start with 3<i>n</i>.", "The zero term is 5 − 3 = 2."], "3<i>n</i> + 2"),
         ("The <i>n</i>th term is 4<i>n</i> − 1. Find the 20th term.", ["Substitute <i>n</i> = 20: 4 × 20 − 1."], "79"),
         ("Is 50 in the sequence 4<i>n</i> − 1?", ["4<i>n</i> − 1 = 50 gives <i>n</i> = 12.75."], "No, it is not a whole number")],
        ["Writing <i>n</i> + 3 for a sequence that goes up in 3s. It should be 3<i>n</i> + something.",
         "Using the first term instead of the zero term: 5, 8, 11, … is 3<i>n</i> + 2, not 3<i>n</i> + 5.",
         "Mixing up the position (<i>n</i>) and the term: the 10th term is not 10.",
         "Forgetting the sign when the sequence goes down: 20, 17, 14, … is −3<i>n</i> + 23."])


def main():
    sets = [S("Next terms and term-to-term rules", collect(one_next, 15, R) + collect(one_geo, 5, R)),
            S("Finding the nth term", collect(one_find_nth, 20, R)),
            S("Using the nth term", collect(one_use, 20, R)),
            S("Is it in the sequence?", collect(one_in, 20, R)),
            S("Patterns and special sequences", problems())]
    make(7, "sequences", 14, "A",
         "Sequences: Term-to-Term Rules and the nth Term",
         "Year 7 Sequences Worksheets: Term-to-Term Rules, nth Term, Patterns and Special Sequences",
         "Sequences",
         "Generate terms of a sequence from either a term-to-term or a position-to-term rule; recognise arithmetic "
         "sequences and find the nth term; recognise geometric sequences and appreciate other sequences that arise.",
         "Free Year 7 sequences worksheets: next terms and term-to-term rules, finding and using the nth term, checking "
         "whether a number is in a sequence, matchstick patterns and special sequences. 100 questions with answers.",
         "For a linear sequence, the nth term is (difference)n + (zero term). 5, 8, 11, … is 3n + 2.",
         "To find a term, substitute n. To test a number, solve the equation: it is in the sequence only if n is a whole number.",
         body(),
         [("How do you find the nth term of a linear sequence?", "Find the common difference and write it in front of n. Then add the zero term, the term before the first. 5, 8, 11, … has nth term 3n + 2."),
          ("What is the difference between term-to-term and position-to-term?", "Term-to-term tells you how to get the next term (add 3). Position-to-term gives any term from its position n (3n + 2)."),
          ("How do I know if a number is in a sequence?", "Set the nth term equal to the number and solve. If n is a positive whole number, it is in the sequence."),
          ("What is a geometric sequence?", "A sequence where you multiply by the same number each time, such as 3, 6, 12, 24, …")],
         sets, R)


if __name__ == "__main__":
    main()
