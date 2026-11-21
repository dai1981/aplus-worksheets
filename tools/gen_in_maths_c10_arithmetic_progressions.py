# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 5: Arithmetic Progressions (CBSE Unit II Algebra)
  python3 tools/gen_in_maths_c10_arithmetic_progressions.py
Recognising an AP and its common difference, the nth term aₙ = a + (n − 1)d, which term is a given number, finding a and d
from two terms, the nth term from the end, the sum Sₙ = n/2 [2a + (n − 1)d] = n/2 (a + l), and word problems (savings,
salaries, rows of seats, stacked logs, prizes, multiples in a range).
Wrong answers come from real mistakes: a + nd instead of a + (n − 1)d, d = a₁ − a₂, n(a + l) without halving,
counting multiples as (last − first)/d without the +1.
"""
import random
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, inr, People, MINUS

R = random.Random(910005)
P = People(R)


def nz(lo, hi):
    return [k for k in range(lo, hi + 1) if k]


def seq(a, d, n=4):
    return ", ".join(fv(a + i * d) for i in range(n)) + ", …"


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


# ---------------------------------------------------------------- set 1: is it an AP? common difference
def one_ap(r):
    kind = r.choice(["d", "d", "next", "is", "is"])
    a = r.choice(nz(-20, 30))
    d = r.choice(nz(-9, 12) + [F(1, 2), F(-3, 2), F(5, 2)])
    if kind == "d":
        return T("Find the common difference of the AP %s" % seq(a, d), fv(d), [fv(-d), fv(a), fv(d * 2) if d * 2 != a else fv(d + 1)],
                 "d = a₂ − a₁ = %s − (%s) = <b>%s</b>." % (fv(a + d), fv(a), fv(d)))
    if kind == "next":
        return T("Write the next term of the AP %s" % seq(a, d), fv(a + 4 * d), [fv(a + 3 * d - d), fv(a + 5 * d), fv(a + 4 * d + 1) if d != 1 else fv(a + 4 * d + 2)],
                 "Add d = %s to the last term: %s + (%s) = <b>%s</b>." % (fv(d), fv(a + 3 * d), fv(d), fv(a + 4 * d)))
    t = r.choice(["ap", "sq", "dbl", "alt"])
    ap = seq(a, d)
    bad = {"sq": ", ".join(str(k * k) for k in range(1, 5)) + ", …", "dbl": ", ".join(str(3 * 2 ** k) for k in range(4)) + ", …",
           "alt": ", ".join(fv(F((-1) ** k * (k + 2))) for k in range(4)) + ", …"}
    if t == "ap":
        return T("Which of these lists is an arithmetic progression?", ap, list(bad.values()),
                 "In an AP the difference between consecutive terms is always the same. Only <b>%s</b> has a constant difference (%s)." % (ap, fv(d)))
    others = [ap] + [v for k, v in bad.items() if k != t]
    return T("Which of these lists is <b>not</b> an arithmetic progression?", bad[t], others,
             "<b>%s</b>: the differences are not equal, so it is not an AP." % bad[t])


# ---------------------------------------------------------------- set 2: nth term
def one_nth(r):
    kind = r.choice(["term", "term", "which", "count"])
    a = r.choice(nz(-15, 25))
    d = r.choice(nz(-7, 9))
    if kind == "term":
        n = r.randint(8, 40)
        v = a + (n - 1) * d
        return T("Find the %s term of the AP %s" % (ordinal(n), seq(a, d, 3)), num(v), [num(a + n * d), num(a * n), num(a + (n - 2) * d) if a + (n - 2) * d != v else num(v + 1)],
                 "a<sub>n</sub> = a + (n − 1)d = %s + (%d − 1)(%s) = <b>%s</b>." % (num(a), n, num(d), num(v)))
    if kind == "which":
        if abs(d) < 2:
            return None
        n = r.randint(10, 50)
        v = a + (n - 1) * d
        return T("Which term of the AP %s is %s?" % (seq(a, d, 3), num(v)), "the %s term" % ordinal(n), ["the %s term" % ordinal(n - 1), "the %s term" % ordinal(n + 1), "the %s term" % ordinal(abs(v // d)) if abs(v // d) not in (n, n - 1, n + 1, 0) else "the %s term" % ordinal(n + 2)],
                 "%s + (n − 1)(%s) = %s, so n − 1 = %d and <b>n = %d</b>." % (num(a), num(d), num(v), n - 1, n))
    a = r.randint(1, 30)
    d = r.randint(2, 9)
    n = r.randint(10, 60)
    l = a + (n - 1) * d
    return T("How many terms are there in the AP %s, …, %s?" % (seq(a, d, 3).replace(", …", ""), num(l)), num(n), [num(n - 1), num(n + 1), num(l // d)] if l // d not in (n, n - 1, n + 1) else [num(n - 1), num(n + 1), num(n + 2)],
             "%s = %s + (n − 1)%d, so n − 1 = %d and <b>n = %d</b>." % (num(l), num(a), d, n - 1, n))


# ---------------------------------------------------------------- set 3: a and d from two terms, term from the end
def one_ad(r):
    kind = r.choice(["two", "two", "two", "end", "three"])
    a = r.choice(nz(-12, 20))
    d = r.choice(nz(-6, 8))
    if kind == "two":
        p, q = sorted(r.sample(range(2, 30), 2))
        tp, tq = a + (p - 1) * d, a + (q - 1) * d
        want = r.choice(["a", "d", "t"])
        info = "The %s term of an AP is %s and its %s term is %s." % (ordinal(p), num(tp), ordinal(q), num(tq))
        if want == "d":
            return T(info + " Find the common difference.", num(d), [num(-d), num(F(tq - tp, q)) if F(tq - tp, q).denominator == 1 and F(tq - tp, q) != d else num(d + 1), num(tq - tp)],
                     "a<sub>%d</sub> − a<sub>%d</sub> = (%d − %d)d: %s = %dd, so <b>d = %s</b>." % (q, p, q, p, num(tq - tp), q - p, num(d)))
        if want == "a":
            return T(info + " Find the first term.", num(a), [num(a + d), num(tp - p * d), num(a - d)],
                     "d = (%s − %s) ÷ %d = %s. Then a = %s − (%d − 1)(%s) = <b>%s</b>." % (num(tq), num(tp), q - p, num(d), num(tp), p, num(d), num(a)))
        n = r.randint(31, 60)
        v = a + (n - 1) * d
        return T(info + " Find its %s term." % ordinal(n), num(v), [num(a + n * d), num(v - d), num(v + 2 * d)],
                 "d = %s, a = %s, so a<sub>%d</sub> = %s + %d(%s) = <b>%s</b>." % (num(d), num(a), n, num(a), n - 1, num(d), num(v)))
    if kind == "end":
        d = abs(d) or 3
        n = r.randint(20, 50)
        l = a + (n - 1) * d
        k = r.randint(3, 12)
        v = l - (k - 1) * d
        return T("Find the %s term from the last term of the AP %s, …, %s." % (ordinal(k), seq(a, d, 3).replace(", …", ""), num(l)), num(v),
                 [num(a + (k - 1) * d), num(l - k * d), num(v + d)],
                 "Count back from the last term: %s − (%d − 1)(%s) = <b>%s</b>." % (num(l), k, num(d), num(v)))
    x = r.randint(2, 9)
    # 2k + 1, 3k + 3, 5k − 1 type: terms are linear in k; AP condition gives k
    a1, b1 = r.choice([(2, 1), (1, 3), (3, -1)])
    a2, b2 = r.choice([(3, 3), (2, 5), (4, 1)])
    t1, t2 = a1 * x + b1, a2 * x + b2
    t3 = 2 * t2 - t1
    a3 = r.choice([5, 6, 7])
    b3 = t3 - a3 * x
    if (2 * a2 - a1 - a3) == 0:
        return None
    def L(a_, b_):
        return "%dk %s %d" % (a_, "+" if b_ >= 0 else MINUS, abs(b_)) if b_ else "%dk" % a_
    return T("For what value of k are %s, %s and %s consecutive terms of an AP?" % (L(a1, b1), L(a2, b2), L(a3, b3)), "k = %d" % x,
             ["k = %d" % (x + 1), "k = %d" % (x - 1), "k = %d" % (x * 2)],
             "Middle term × 2 = sum of the outer terms: 2(%s) = (%s) + (%s), so <b>k = %d</b>." % (L(a2, b2), L(a1, b1), L(a3, b3), x))


# ---------------------------------------------------------------- set 4: sum of n terms
def one_sum(r):
    kind = r.choice(["sum", "sum", "al", "nat", "odd"])
    if kind == "sum":
        a = r.choice(nz(-10, 20))
        d = r.choice(nz(-5, 8))
        n = r.randint(10, 30)
        s = F(n, 2) * (2 * a + (n - 1) * d)
        return T("Find the sum of the first %d terms of the AP %s" % (n, seq(a, d, 3)), num(s), [num(n * (2 * a + (n - 1) * d)), num(F(n, 2) * (2 * a + n * d)), num(a + (n - 1) * d)],
                 "S<sub>n</sub> = n/2 [2a + (n − 1)d] = %d/2 [2(%s) + %d(%s)] = <b>%s</b>." % (n, num(a), n - 1, num(d), num(s)))
    if kind == "al":
        a = r.randint(2, 30)
        d = r.randint(2, 9)
        n = r.randint(10, 40)
        l = a + (n - 1) * d
        s = F(n, 2) * (a + l)
        return T("An AP has %d terms. Its first term is %s and its last term is %s. Find the sum of all its terms." % (n, num(a), num(l)), num(s), [num(n * (a + l)), num(a + l), num(F(n - 1, 2) * (a + l))],
                 "S = n/2 (a + l) = %d/2 (%s + %s) = <b>%s</b>." % (n, num(a), num(l), num(s)))
    if kind == "nat":
        n = r.choice([20, 25, 40, 50, 60, 100, 150, 200])
        s = n * (n + 1) // 2
        return T("Find the sum of the first %d positive integers." % n, num(s), [num(n * n), num(n * (n - 1) // 2), num(n * (n + 1))],
                 "S = n(n + 1)/2 = %d × %d ÷ 2 = <b>%s</b>." % (n, n + 1, num(s)))
    n = r.choice([10, 15, 20, 25, 30, 40, 50])
    return T("Find the sum of the first %d odd numbers." % n, num(n * n), [num(n * (n + 1)), num(n * (n + 1) // 2), num(2 * n - 1)],
             "1 + 3 + 5 + … has a = 1, d = 2: S = %d/2 [2 + %d × 2] = %d² = <b>%s</b>." % (n, n - 1, n, num(n * n)))


# ---------------------------------------------------------------- set 5: word problems
def one_word(r):
    kind = r.choice(["save", "salary", "seats", "logs", "prize", "mult", "mult"])
    name, he, his = P.next()
    if kind == "save":
        a = r.choice([5, 10, 20, 25, 50])
        d = r.choice([5, 10, 20, 25])
        n = r.choice([12, 15, 20, 24, 30])
        s = n * (2 * a + (n - 1) * d) // 2
        return T("%s saves %s in the first week and increases the amount by %s each week. How much does %s save in all in %d weeks?" % (name, inr(a), inr(d), he, n), inr(s),
                 [inr(a + (n - 1) * d), inr(F(n * (2 * a + n * d), 2)), inr(n * (2 * a + (n - 1) * d))],
                 "S = %d/2 [2 × %d + %d × %d] = <b>%s</b>." % (n, a, n - 1, d, inr(s)))
    if kind == "salary":
        a = r.choice([18000, 20000, 24000, 25000, 30000])
        d = r.choice([1000, 1200, 1500, 2000, 2500])
        n = r.randint(5, 15)
        v = a + (n - 1) * d
        return T("%s starts a job with a monthly salary of %s and gets an annual increment of %s. What is %s monthly salary in the %s year?" % (name, inr(a), inr(d), his, ordinal(n)), inr(v),
                 [inr(a + n * d), inr(v - d * 2), inr(a * n)],
                 "a<sub>%d</sub> = %s + (%d − 1) × %s = <b>%s</b>." % (n, num(a), n, num(d), inr(v)))
    if kind == "seats":
        a = r.randint(15, 30)
        d = r.choice([2, 3, 4])
        n = r.randint(15, 30)
        s = n * (2 * a + (n - 1) * d) // 2
        return T("A hall has %d seats in the first row and %d more seats in each next row. There are %d rows. How many seats are there in all?" % (a, d, n), num(s),
                 [num(a + (n - 1) * d), num(n * (2 * a + n * d) // 2), num(a * n)],
                 "S = %d/2 [2 × %d + %d × %d] = <b>%s</b>." % (n, a, n - 1, d, num(s)))
    if kind == "logs":
        top = r.randint(3, 10)
        n = r.randint(8, 20)
        bottom = top + n - 1
        s = n * (top + bottom) // 2
        return T("Logs are stacked with %d in the bottom row, %d in the next row, %d in the row after that, and so on, up to %d logs in the top row. How many logs are there in the stack?" % (bottom, bottom - 1, bottom - 2, top), num(s),
                 [num(n * (top + bottom)), num(bottom * n), num(s - top)],
                 "There are %d rows: S = n/2 (first + last) = %d/2 (%d + %d) = <b>%s</b>." % (n, n, bottom, top, num(s)))
    if kind == "prize":
        n = r.choice([5, 6, 7, 8])
        d = r.choice([20, 25, 50, 100])
        a = d * r.randint(n, 2 * n)
        s = n * (2 * a - (n - 1) * d) // 2
        return T("A sum of %s is given as %d prizes. Each prize is %s less than the one before it. What is the first prize?" % (inr(s), n, inr(d)), inr(a),
                 [inr(a - (n - 1) * d), inr(s // n), inr(a + d)],
                 "%d/2 [2a − %d × %d] = %s, so <b>a = %s</b>." % (n, n - 1, d, num(s), inr(a)))
    k = r.choice([3, 4, 6, 7, 8, 9, 11, 13])
    lo, hi = r.choice([(10, 99), (100, 999)])
    lab = "two-digit" if lo == 10 else "three-digit"
    first = -(-lo // k) * k
    last = hi // k * k
    n = (last - first) // k + 1
    return T("How many %s numbers are divisible by %d?" % (lab, k), num(n), [num(n - 1), num(n + 1), num((hi - lo + 1) // k + 1) if (hi - lo + 1) // k + 1 not in (n, n - 1, n + 1) else num(n + 2)],
             "They form an AP %s, %s, …, %s. %s = %s + (n − 1)%d gives <b>n = %s</b>." % (num(first), num(first + k), num(last), num(last), num(first), k, num(n)))


def main():
    seen = set()
    sets = [
        S("Common difference and next term", mix(R, [(one_ap, 20)], seen)),
        S("The nth term", mix(R, [(one_nth, 20)], seen)),
        S("Finding a and d", mix(R, [(one_ad, 20)], seen)),
        S("Sum of the first n terms", mix(R, [(one_sum, 20)], seen)),
        S("Word problems", mix(R, [(one_word, 20)], seen)),
    ]
    body = lesson(
        "<p>An <b>arithmetic progression</b> (AP) is a list where each term is the previous term plus a fixed number d, the <b>common difference</b>.</p>"
        "<p>nth term: <b>a<sub>n</sub> = a + (n − 1)d</b>. Sum of the first n terms: <b>S<sub>n</sub> = n/2 [2a + (n − 1)d] = n/2 (a + l)</b>, where l is the last term.</p>",
        [("Find the 10th term of 2, 7, 12, …", ["a = 2, d = 5", "a<sub>10</sub> = 2 + 9 × 5"], "47"),
         ("Find the sum of the first 22 terms of 8, 3, −2, …", ["a = 8, d = −5", "S = 11 [16 + 21 × (−5)]"], "−979")],
        ["Using a + nd for the nth term. It is a + (n − 1)d.",
         "Finding d as a₁ − a₂. Always subtract a term from the next one: d = a₂ − a₁.",
         "Forgetting to halve: S = n/2 (a + l), not n(a + l)."])
    faq = [
        ("What is the formula for the nth term of an AP?", "aₙ = a + (n − 1)d, where a is the first term and d is the common difference."),
        ("What is the formula for the sum of the first n terms of an AP?", "Sₙ = n/2 [2a + (n − 1)d], or Sₙ = n/2 (a + l) when the last term l is known."),
        ("How do I check whether a list is an AP?", "Find the differences between consecutive terms. If they are all equal, the list is an AP."),
        ("How many three-digit numbers are divisible by 7?", "They are 105, 112, …, 994. From 994 = 105 + (n − 1)7 we get n = 128."),
    ]
    make(10, "arithmetic-progressions", 5, "II", 5, "Arithmetic Progressions", "arithmetic progressions",
         "Motivation for studying arithmetic progression; derivation of the nth term and sum of the first n terms of an AP and their application in solving daily life problems (summary of the CBSE syllabus)",
         "Class 10 Arithmetic Progressions worksheet (NCERT Chapter 5): common difference, nth term, finding a and d, sum of n terms and word problems. 100 questions with answers.",
         "aₙ = a + (n − 1)d", "Sₙ = n/2 [2a + (n − 1)d]",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
