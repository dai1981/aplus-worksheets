# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Adding and Subtracting Fractions (KS3 Number)
  python3 tools/gen_uk_maths_y7_adding_and_subtracting_fractions.py
Same denominators, related denominators, any denominators, mixed numbers, and problems.
Wrong answers come from real mistakes: adding the denominators, changing the denominator without the
numerator, not simplifying, and subtracting the smaller whole-number part the wrong way in mixed numbers.
"""
import random
from fractions import Fraction as F
from math import gcd
from uk_ks3 import mcq, B, S, make, lesson, collect, fr, frac, People

R = random.Random(70801)
P = People(R)


def fv(v):
    """Simplest form; improper fractions as mixed numbers."""
    return frac(v) if v >= 0 else None


def raw(n, d):
    return fr(n, d)


def QF(q, ans, wrongs, e):
    """Fraction answer. wrongs: values (Fraction) or (html, key) pairs."""
    cands = []
    for w in wrongs:
        if w is None:
            continue
        if isinstance(w, tuple):
            cands.append(w)
        elif w > 0:
            cands.append((fv(w), ("v", F(w))))
    for d in (F(1, ans.denominator), -F(1, ans.denominator), F(1, 2 * ans.denominator)):
        if ans + d > 0:
            cands.append((fv(ans + d), ("v", ans + d)))
    cands = [(h, h) for h, _ in cands]
    return mcq(q, (fv(ans), fv(ans)), cands, e)


def lcm3(*ds):
    L = 1
    for d in ds:
        L = L * d // gcd(L, d)
    return L


def naive(a, b, op):
    """Add/subtract tops and bottoms: the classic mistake."""
    n = a.numerator + b.numerator if op == "+" else a.numerator - b.numerator
    d = a.denominator + b.denominator if op == "+" else a.denominator - b.denominator
    if d <= 1 or n <= 0 or n == d:
        return None
    return (raw(n, d), ("raw", n, d))


# ------------------------------------------------------------ set 1: same denominator
def one_same(r):
    d = r.choice([5, 6, 7, 8, 9, 10, 11, 12, 15])
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    op = r.choice(["+", "−"])
    if op == "−" and a <= b:
        a, b = b, a
    if a == b:
        return None
    x, y = F(a, d), F(b, d)
    ans = x + y if op == "+" else x - y
    q = "Work out %s." % B("%s %s %s" % (raw(a, d), op, raw(b, d)))
    n = a + b if op == "+" else a - b
    e = "The denominators are the same, so %s the numerators: %s." % ("add" if op == "+" else "subtract", raw(n, d))
    if F(n, d) != F(n, d).limit_denominator(d) or gcd(n, d) > 1 or n > d:
        e += " Simplify: <b>%s</b>." % fv(ans)
    else:
        e += " The answer is <b>%s</b>." % fv(ans)
    w = [naive(x, y, "+" if op == "+" else "-")]
    if gcd(n, d) > 1 or n > d:
        w.append((raw(n, d), ("raw", n, d)))
    return QF(q, ans, w, e)


# ------------------------------------------------------------ set 2: one denominator a multiple of the other
def one_related(r):
    d1 = r.choice([2, 3, 4, 5])
    k = r.choice([2, 3, 4])
    d2 = d1 * k
    a = r.randint(1, d1 - 1)
    b = r.randint(1, d2 - 1)
    if gcd(b, d2) > 1 and r.random() < 0.6:
        return None
    op = r.choice(["+", "−"])
    x, y = F(a, d1), F(b, d2)
    if y.denominator != d2:
        return None
    if op == "−" and x <= y:
        x, y = y, x
    ans = x + y if op == "+" else x - y
    if ans <= 0:
        return None
    q = "Work out %s." % B("%s %s %s" % (raw(x.numerator, x.denominator), op, raw(y.numerator, y.denominator)))
    small = x if x.denominator < y.denominator else y
    e = "Change %s to %s (multiply top and bottom by %d). Then %s the numerators. The answer is <b>%s</b>." % (
        raw(small.numerator, small.denominator), raw(small.numerator * k, d2), k, "add" if op == "+" else "subtract", fv(ans))
    # mistake: change the denominator but not the numerator
    xs = F(small.numerator, d2)
    other = y if small is x else x
    wrong2 = xs + other if op == "+" else (other - xs if small is y else xs - other)
    return QF(q, ans, [naive(x, y, "+" if op == "+" else "-"), wrong2 if wrong2 and wrong2 > 0 else None], e)


# ------------------------------------------------------------ set 3: any denominators
def one_any(r):
    d1, d2 = r.sample([3, 4, 5, 6, 7, 8, 9, 10], 2)
    if d1 % d2 == 0 or d2 % d1 == 0:
        return None
    x, y = F(r.randint(1, d1 - 1), d1), F(r.randint(1, d2 - 1), d2)
    if x.denominator != d1 or y.denominator != d2:
        return None
    op = r.choice(["+", "−", "+"])
    if op == "−" and x <= y:
        x, y = y, x
    ans = x + y if op == "+" else x - y
    L = d1 * d2 // gcd(d1, d2)
    q = "Work out %s." % B("%s %s %s" % (raw(x.numerator, x.denominator), op, raw(y.numerator, y.denominator)))
    xn, yn = x.numerator * L // x.denominator, y.numerator * L // y.denominator
    e = "Use the common denominator %d: %s %s %s = %s. The answer is <b>%s</b>." % (
        L, raw(xn, L), op, raw(yn, L), raw(xn + yn if op == "+" else xn - yn, L), fv(ans))
    wrong_num = F(x.numerator + y.numerator, L) if op == "+" else (F(x.numerator - y.numerator, L) if x.numerator > y.numerator else None)
    return QF(q, ans, [naive(x, y, "+" if op == "+" else "-"), wrong_num], e)


# ------------------------------------------------------------ set 4: mixed numbers
def one_mixed(r):
    w1, w2 = r.randint(1, 5), r.randint(1, 4)
    d1, d2 = r.choice([(2, 4), (3, 6), (4, 8), (2, 3), (3, 4), (4, 5), (5, 10), (2, 5), (6, 3), (8, 4)])
    x = w1 + F(r.randint(1, d1 - 1), d1)
    y = w2 + F(r.randint(1, d2 - 1), d2)
    if (x - int(x)).denominator != d1 or (y - int(y)).denominator != d2:
        return None
    op = r.choice(["+", "−"])
    if op == "−" and x <= y:
        x, y = y, x
    ans = x + y if op == "+" else x - y
    if ans <= 0 or ans.denominator == 1:
        return None
    q = "Work out %s." % B("%s %s %s" % (frac(x), op, frac(y)))
    fx, fy = x - int(x), y - int(y)
    if op == "+":
        e = "Add the whole numbers: %d + %d = %d. Add the fractions: %s + %s = %s. Total: <b>%s</b>." % (
            int(x), int(y), int(x) + int(y), frac(fx), frac(fy), frac(fx + fy), fv(ans))
        wrong = [int(x) + int(y) + (fx + fy - int(fx + fy)) if fx + fy >= 1 else None]   # forgot to carry
    else:
        e = ("Change to improper fractions or subtract wholes and parts: %s − %s = <b>%s</b>." % (frac(x), frac(y), fv(ans)))
        wrong = [int(x) - int(y) + abs(fx - fy) if fx < fy and int(x) > int(y) else None]   # “smaller from bigger”
    return QF(q, ans, wrong + [ans + 1, ans - 1 if ans > 1 else None], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("Freya ate %s of a pizza and Oliver ate %s. What fraction of the pizza did they eat altogether?", F(1, 3), F(1, 4), "+"),
        ("A tank is %s full. %s of the tank is used. What fraction of the tank is left?", F(5, 6), F(1, 4), "−"),
        ("On Monday Zara read %s of a book and on Tuesday %s. What fraction has she read?", F(2, 5), F(1, 3), "+"),
        ("%s of a class walk to school and %s come by bus. What fraction walk or come by bus?", F(3, 8), F(1, 4), "+"),
        ("A ribbon is %s m long. Kai cuts off %s m. How long is the ribbon now?", F(7, 2), F(5, 4), "−"),
        ("A recipe needs %s kg of flour and %s kg of sugar. What is the total mass?", F(3, 4), F(2, 3), "+"),
        ("A bottle holds %s litres. Grace pours out %s litres. How much is left?", F(9, 4), F(2, 3), "−"),
        ("Jack walks %s km to the shop and %s km to the park. How far does he walk?", F(5, 4), F(7, 3), "+"),
        ("%s of a garden is grass and %s is flowers. What fraction is neither?", F(1, 2), F(1, 3), "rest"),
        ("%s of the pupils like football and %s like rugby (no one likes both). What fraction like neither?", F(2, 5), F(1, 4), "rest"),
    ]
    for text, a, b, op in data:
        if op == "rest":
            ans = 1 - a - b
            e = "%s + %s = %s, so 1 − %s = <b>%s</b>." % (frac(a), frac(b), frac(a + b), frac(a + b), fv(ans))
            w = [a + b, naive(a, b, "+"), F(1, 6) if ans != F(1, 6) else F(1, 5)]
        else:
            ans = a + b if op == "+" else a - b
            e = "%s %s %s = <b>%s</b>. Use a common denominator of %d." % (frac(a), op, frac(b), fv(ans), (a.denominator * b.denominator // gcd(a.denominator, b.denominator)))
            w = [naive(a, b, "+" if op == "+" else "-")]
        q = text % (frac(a), frac(b))
        its.append(QF(q, ans, w, e))
    for a, b, c in [(F(1, 2), F(1, 3), F(1, 6)), (F(1, 4), F(2, 5), F(1, 10)), (F(2, 3), F(1, 6), F(1, 12))]:
        ans = a + b + c
        q = "Work out %s." % B("%s + %s + %s" % (frac(a), frac(b), frac(c)))
        its.append(QF(q, ans, [(raw(a.numerator + b.numerator + c.numerator, a.denominator + b.denominator + c.denominator), "n3")],
                      "Use the common denominator %d. The answer is <b>%s</b>." % (lcm3(a.denominator, b.denominator, c.denominator), fv(ans))))
    for a, b, miss in [(F(3, 4), F(1, 5), "+"), (F(5, 6), F(1, 2), "−"), (F(7, 10), F(1, 4), "+"), (F(2, 3), F(3, 8), "−"),
                       (F(1, 2), F(1, 3), "+"), (F(4, 5), F(3, 10), "−"), (F(5, 8), F(1, 6), "+")]:
        if miss == "+":
            ans = a - b
            q = "Find the missing fraction: %s + ☐ = %s" % (frac(b), frac(a))
        else:
            ans = a - b
            q = "Find the missing fraction: %s − ☐ = %s" % (frac(a), frac(b))
        e = "☐ = %s − %s = <b>%s</b>." % (frac(a), frac(b), fv(ans))
        its.append(QF(q, ans, [a + b, naive(a, b, "-")], e))
    return its


def body():
    return lesson(
        "<p>You can only add or subtract fractions when the <b>denominators are the same</b>. Then add or subtract the "
        "numerators and keep the denominator.</p>"
        "<p>If the denominators are different, find a common denominator (the LCM of the denominators) and make "
        "equivalent fractions first. Always simplify your answer.</p>",
        [("Work out 2/3 + 1/4.", ["The LCM of 3 and 4 is 12.", "2/3 = 8/12 and 1/4 = 3/12.", "8/12 + 3/12 = 11/12."], "11/12"),
         ("Work out 3 1/4 − 1 2/3.", ["Improper fractions: 13/4 − 5/3.", "Common denominator 12: 39/12 − 20/12 = 19/12."], "1 7/12")],
        ["Adding the denominators: 1/3 + 1/4 is not 2/7.",
         "Changing the denominator but not the numerator: 1/2 is 2/4, not 1/4.",
         "Forgetting to simplify: 6/8 should be 3/4.",
         "With mixed numbers, taking the smaller fraction from the bigger one: 3 1/4 − 1 2/3 is not 2 5/12."])


def main():
    sets = [S("Same denominators", collect(one_same, 20, R)),
            S("Related denominators", collect(one_related, 20, R)),
            S("Different denominators", collect(one_any, 20, R)),
            S("Mixed numbers", collect(one_mixed, 20, R)),
            S("Problems", problems())]
    make(7, "adding-and-subtracting-fractions", 8, "N",
         "Adding and Subtracting Fractions and Mixed Numbers",
         "Year 7 Adding and Subtracting Fractions Worksheets: Common Denominators and Mixed Numbers",
         "Adding and subtracting fractions",
         "Use the four operations, including formal written methods, applied to integers, decimals, proper and improper "
         "fractions, and mixed numbers, all both positive and negative.",
         "Free Year 7 worksheets on adding and subtracting fractions: same and different denominators, finding a common "
         "denominator, mixed numbers and word problems. 100 questions with step-by-step answers.",
         "Make the denominators the same, then add or subtract the numerators. Never add the denominators.",
         "Use the LCM of the denominators as the common denominator, and simplify your answer.",
         body(),
         [("How do you add fractions with different denominators?", "Find a common denominator, usually the LCM. Change both fractions to that denominator, then add the numerators."),
          ("Why can't I add the denominators?", "The denominator tells you the size of the pieces. 1/3 + 1/4 are different sized pieces, so first cut them into twelfths."),
          ("How do I subtract mixed numbers?", "Either change them to improper fractions first, or subtract the whole numbers and the fractions separately, exchanging a whole if the first fraction is smaller."),
          ("Do I always need to simplify?", "Yes. Give the final answer in its simplest form, and as a mixed number if it is more than 1.")],
         sets, R)


if __name__ == "__main__":
    main()
