# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Multiplying and dividing fractions (Australian Curriculum v9.0: AC9M7N06)
  python3 tools/gen_au_maths_y7_multiplying_and_dividing_fractions.py
Fractions of amounts, multiplying fractions, reciprocals, dividing fractions and mixed numerals, and problems.
Wrong answers come from real mistakes: multiplying the denominator too, flipping the wrong fraction,
dividing tops and bottoms, and multiplying mixed numerals part by part.
"""
import random
from fractions import Fraction as F
from math import gcd
from au_hs import mcq, B, S, make, lesson, collect, fr, frac, num, QN, People, aud

R = random.Random(70601)
P = People(R)


def fv(v):
    return frac(v)


def QF(q, ans, wrongs, e):
    cands = []
    for w in wrongs:
        if w is None:
            continue
        if isinstance(w, tuple):
            cands.append(w)
        elif w > 0:
            cands.append((fv(w), ("v", F(w))))
    for d in (F(1, ans.denominator), -F(1, ans.denominator), F(1, 2 * ans.denominator), ans):
        if ans + d > 0:
            cands.append((fv(ans + d), ("v", ans + d)))
    cands = [(h, h) for h, _ in cands]
    return mcq(q, (fv(ans), fv(ans)), cands, e)


def rf(n, d):
    return (fr(n, d), ("raw", n, d))


def f(v):
    return frac(v)


# ------------------------------------------------------------ set 1: fraction of an amount, fraction × integer
def one_of(r):
    d = r.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    n = r.randint(1, d - 1)
    if gcd(n, d) > 1:
        return None
    if r.random() < 0.55:
        amt = d * r.randint(3, 15)
        ans = F(n * amt, d)
        q = "Find %s of %s." % (B(fr(n, d)), B(num(amt)))
        e = ("Divide by %d, then multiply by %d: %d ÷ %d = %d, × %d = <b>%s</b>." % (d, n, amt, d, amt // d, n, num(ans)) if n > 1
             else "Divide by %d: %d ÷ %d = <b>%s</b>." % (d, amt, d, num(ans)))
        return QN(q, ans, [amt // d, amt * n, F(amt, n) if amt % n == 0 else None, amt - amt // d * n if n > 1 else amt - amt // d], e, near=(n, -n, d))
    k = r.randint(2, 9)
    if k % d == 0:
        return None
    ans = F(n * k, d)
    q = "Work out %s." % B("%s × %d" % (fr(n, d), k))
    e = "Multiply the numerator only: %s = <b>%s</b>." % (fr(n * k, d), fv(ans))
    return QF(q, ans, [rf(n * k, d * k), F(n, d * k)], e)


# ------------------------------------------------------------ set 2: fraction × fraction
def one_mul(r):
    a, b = F(r.randint(1, 7), r.randint(2, 9)), F(r.randint(1, 7), r.randint(2, 9))
    if a >= 1 or b >= 1 or a.denominator == 1 or b.denominator == 1:
        return None
    ans = a * b
    q = "Work out %s." % B("%s × %s" % (f(a), f(b)))
    n, d = a.numerator * b.numerator, a.denominator * b.denominator
    e = "Multiply the numerators and the denominators: %s" % fr(n, d)
    e += (", which simplifies to <b>%s</b>." % fv(ans)) if gcd(n, d) > 1 else ". The answer is <b>%s</b>." % fv(ans)
    L = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    w = [rf(a.numerator * b.numerator, L) if L != d else None,                # kept a common denominator
         a + b, rf(a.numerator * b.denominator, a.denominator * b.numerator)]  # divided instead
    if gcd(n, d) > 1:
        w.insert(0, rf(n, d))
    return QF(q, ans, w, e)


def one_mul_mixed(r):
    a = r.randint(1, 3) + F(r.randint(1, 3), 4) if r.random() < 0.5 else r.randint(1, 2) + F(r.choice([1, 2]), 3)
    b = F(r.randint(1, 5), r.randint(2, 6)) if r.random() < 0.6 else r.randint(1, 2) + F(1, 2)
    if b >= 3 or b.denominator == 1 or a.denominator == 1:
        return None
    ans = a * b
    q = "Work out %s." % B("%s × %s" % (f(a), f(b)))
    ia, ib = F(a.numerator, a.denominator), F(b.numerator, b.denominator)
    e = "Change to improper fractions: %s × %s = %s = <b>%s</b>." % (
        fr(ia.numerator, ia.denominator), fr(ib.numerator, ib.denominator), fr(ia.numerator * ib.numerator, ia.denominator * ib.denominator), fv(ans))
    partwise = int(a) * int(b) + (a - int(a)) * (b - int(b))
    return QF(q, ans, [partwise if partwise != ans else None, a + b], e)


# ------------------------------------------------------------ set 3: reciprocals and ÷ by integer
def one_recip(r):
    if r.random() < 0.4:
        v = F(r.randint(1, 9), r.randint(2, 12))
        if v.denominator == 1 or v == 1:
            return None
        if r.random() < 0.3:
            v = r.randint(1, 3) + F(1, r.choice([2, 3, 4]))
        ans = 1 / v
        q = "What is the %s of %s?" % (B("reciprocal"), f(v))
        e = "Turn %s upside down%s: <b>%s</b>. A number times its reciprocal is 1." % (
            f(v), " (first write it as %s)" % fr(v.numerator, v.denominator) if v > 1 else "", fv(ans))
        w = [rf(v.numerator, v.denominator) if v > 1 else None, -v if False else None, rf(1, v.numerator) if v.numerator > 1 else None,
             (("−" + f(v)), "neg")]
        return QF(q, ans, w, e)
    d = r.randint(2, 9)
    n = r.randint(1, d - 1)
    k = r.randint(2, 6)
    v = F(n, d)
    if v.denominator != d:
        return None
    ans = v / k
    q = "Work out %s." % B("%s ÷ %d" % (f(v), k))
    e = "Dividing by %d is the same as multiplying by %s: %s × %s = <b>%s</b>." % (k, fr(1, k), f(v), fr(1, k), fv(ans))
    return QF(q, ans, [v * k, F(n, d) if n % k else F(n // k, d)] if n % k else [v * k, rf(n * k, d)], e)


# ------------------------------------------------------------ set 4: fraction ÷ fraction
def one_div(r):
    a = F(r.randint(1, 8), r.randint(2, 9))
    b = F(r.randint(1, 8), r.randint(2, 9))
    if r.random() < 0.3:
        a = r.randint(1, 3) + F(r.randint(1, 2), 3)
    if a.denominator == 1 or b.denominator == 1 or a == b or a > 4:
        return None
    ans = a / b
    q = "Work out %s." % B("%s ÷ %s" % (f(a), f(b)))
    ia = fr(a.numerator, a.denominator)
    e = "Keep, change, flip: %s × %s = <b>%s</b>." % (ia, fr(b.denominator, b.numerator), fv(ans))
    w = [a * b, b / a]
    if a.numerator % b.numerator == 0 and a.denominator % b.denominator == 0:
        pass
    else:
        w.append(rf(a.numerator * b.numerator, a.denominator * b.denominator))
    return QF(q, ans, w, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for name, amt, n, d, what in [("Charlotte", 320, 3, 8, "saves"), ("Jack", 270, 2, 9, "spends on a skateboard"),
                                  ("Zara", 84, 5, 6, "gives to the RSPCA"), ("Ethan", 490, 4, 7, "spends on a bike")]:
        ans = F(amt * n, d)
        q = "%s has $%d. %s %s %s of it. How much is that?" % (name, amt, "She" if name in ("Charlotte", "Zara") else "He", what, fr(n, d))
        e = "$%d ÷ %d × %d = <b>$%s</b>." % (amt, d, n, num(ans))
        its.append(QN(q, ans, [amt // d, amt - ans, F(amt * d, n) if (amt * d) % n == 0 else amt * n], e, fmt=lambda v: "$" + num(v)))
    for L, piece in [(F(9), F(3, 4)), (F(4), F(1, 3)), (F(15, 2), F(3, 4)), (F(8), F(2, 5))]:
        ans = L / piece
        q = "A ribbon is %s m long. How many pieces of %s m can be cut from it?" % (f(L), f(piece))
        e = "%s ÷ %s = %s × %s = <b>%s</b>." % (f(L), f(piece), fr(L.numerator, L.denominator) if L.denominator > 1 else f(L), fr(piece.denominator, piece.numerator), fv(ans))
        its.append(QF(q, ans, [L * piece, piece / L], e))
    for a, b, ctx in [(F(4, 5), F(2, 3), "A paddock is %s of a farm. %s of the paddock is planted with wheat. What fraction of the farm is wheat?"),
                      (F(3, 5), F(1, 2), "%s of a class are girls. %s of the girls play netball. What fraction of the class are girls who play netball?"),
                      (F(7, 8), F(2, 7), "A bottle is %s full of sunscreen. %s of the sunscreen is used at the beach. What fraction of the bottle was used?")]:
        ans = a * b
        q = ctx % (f(a), f(b))
        e = "“Of” means multiply: %s × %s = <b>%s</b>." % (f(a), f(b), fv(ans))
        its.append(QF(q, ans, [a + b if a + b < 2 else None, a - b if a > b else b - a, rf(a.numerator * b.numerator, a.denominator + b.denominator)], e))
    for length, width in [(F(7, 2), F(4, 3)), (F(5, 4), F(2, 3)), (F(9, 4), F(8, 3))]:
        ans = length * width
        q = "A rectangle measures %s m by %s m. What is its area?" % (f(length), f(width))
        e = "Area = %s × %s = %s × %s = <b>%s m²</b>." % (f(length), f(width), fr(length.numerator, length.denominator), fr(width.numerator, width.denominator), fv(ans))
        its.append(mcq(q, (fv(ans) + " m²", ans), [(fv(w) + " m²", w) for w in [2 * (length + width), length + width, int(length) * int(width) + (length - int(length)) * (width - int(width)), ans + 1] if w != ans and w > 0], e))
    for total, part, ctx in [(F(15), F(3, 4), "A bottle holds %s of a litre. How many bottles can be filled from %s litres?"),
                             (F(4), F(1, 3), "A swimming lesson lasts %s of an hour. How many lessons fit into %s hours?"),
                             (F(10, 3), F(5, 6), "Each scoop holds %s of a cup. How many scoops are in %s cups of flour?")]:
        ans = total / part
        q = ctx % (f(part), f(total))
        e = "%s ÷ %s = %s × %s = <b>%s</b>." % (f(total), f(part), f(total) if total.denominator == 1 else fr(total.numerator, total.denominator), fr(part.denominator, part.numerator), fv(ans))
        its.append(QF(q, ans, [total * part, part / total], e))
    its.append(QF("A recipe for 4 people uses %s cups of milk. How much milk is needed for 2 people?" % f(F(7, 3)), F(7, 6),
                  [F(14, 3), F(3, 7)], "Half of %s = %s × %s = <b>%s</b> cups." % (f(F(7, 3)), fr(7, 3), fr(1, 2), fv(F(7, 6)))))
    for v, k, ctx in [(F(3, 5), 6, "%s of a pavlova is left. It is shared equally between %d people. What fraction of the whole pavlova does each person get?"),
                      (F(3, 4), 4, "%s of a pizza is shared equally between %d friends. What fraction of the pizza does each friend get?")]:
        ans = v / k
        q = ctx % (f(v), k)
        e = "%s ÷ %d = %s × %s = <b>%s</b>." % (f(v), k, f(v), fr(1, k), fv(ans))
        its.append(QF(q, ans, [v * k, rf(v.numerator, v.denominator * k + 1)], e))
    return its


def body():
    return lesson(
        "<p><b>Multiplying:</b> multiply the numerators and multiply the denominators, then simplify. "
        "“Of” means multiply: 2/3 of 12 = 2/3 × 12 = 8.</p>"
        "<p><b>Dividing:</b> keep the first fraction, change ÷ to ×, and flip the second fraction (use its <b>reciprocal</b>).</p>"
        "<p>Change mixed numerals into improper fractions before you multiply or divide.</p>",
        [("Work out 3/4 × 2/5.", ["3 × 2 = 6 and 4 × 5 = 20.", "6/20 simplifies to 3/10."], "3/10"),
         ("Work out 2/3 ÷ 4/9.", ["Keep, change, flip: 2/3 × 9/4.", "= 18/12 = 3/2."], "1 1/2"),
         ("Work out 1 1/2 × 2 2/3.", ["Improper: 3/2 × 8/3 = 24/6."], "4")],
        ["Multiplying the denominator by a whole number: 2/5 × 3 = 6/5, not 6/15.",
         "Flipping the first fraction instead of the second when dividing.",
         "Multiplying mixed numerals in parts: 1 1/2 × 2 2/3 is not 2 2/6.",
         "Thinking the answer to a division must be smaller: 6 ÷ 3/4 = 8."])


def main():
    sets = [S("Fractions of amounts and × whole numbers", collect(one_of, 20, R)),
            S("Multiplying fractions", collect(one_mul, 14, R) + collect(one_mul_mixed, 6, R)),
            S("Reciprocals and dividing by a whole number", collect(one_recip, 20, R)),
            S("Dividing fractions", collect(one_div, 20, R)),
            S("Problems", problems())]
    make(7, "multiplying-and-dividing-fractions", 6, "AC9M7N06",
         "Multiplying and Dividing Fractions and Mixed Numerals",
         "Year 7 Multiplying and Dividing Fractions Worksheets: Fractions of Amounts, Reciprocals and Division (Free, Answer Key)",
         "Multiplying and dividing fractions",
         "use the 4 operations with positive rational numbers including fractions, decimals and percentages to solve problems "
         "using efficient calculation strategies",
         "Free Year 7 maths worksheets on multiplying and dividing fractions for the Australian Curriculum (AC9M7N06): fractions "
         "of amounts, multiplying fractions and mixed numerals, reciprocals, dividing fractions and word problems. 100 questions with an answer key.",
         "Multiply: tops × tops, bottoms × bottoms. Divide: multiply by the reciprocal.",
         "Change mixed numerals to improper fractions first, and simplify your answer.",
         body(),
         [("How do you multiply fractions?", "Multiply the numerators, multiply the denominators, then simplify. You do not need a common denominator."),
          ("How do you divide fractions?", "Keep the first fraction, change ÷ to ×, and flip the second fraction. 2/3 ÷ 4/9 = 2/3 × 9/4 = 3/2."),
          ("What is a reciprocal?", "The number you multiply by to get 1. The reciprocal of 3/5 is 5/3, and the reciprocal of 4 is 1/4."),
          ("Why can dividing by a fraction give a bigger answer?", "Because you are asking how many small pieces fit in. 6 ÷ 3/4 = 8 pieces of three quarters.")],
         sets, R)


if __name__ == "__main__":
    main()
