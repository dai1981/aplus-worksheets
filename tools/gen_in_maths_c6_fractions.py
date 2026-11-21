# -*- coding: utf-8 -*-
"""
India Class 6 Maths, Ganita Prakash Chapter 7: Fractions
  python3 tools/gen_in_maths_c6_fractions.py
Fractions as equal shares, fraction of a collection, fractions on the number line, mixed numbers and improper
fractions, equivalent fractions and lowest terms, comparing fractions, and adding and subtracting fractions.
Wrong answers come from real mistakes: adding the denominators, comparing by the denominator alone (1/8 > 1/5), and
multiplying only the numerator for an equivalent fraction.
"""
import random
from math import gcd
from fractions import Fraction as F
from in_common import num, unit, T, QN, adopt, gb, fr
import gen_uk_maths_y7_adding_and_subtracting_fractions as af

R = random.Random(906007)
adopt(af, R)
H = lambda f: fr(str(f.numerator), str(f.denominator)) if f.denominator != 1 else str(f.numerator)


def mixed(f):
    w, p = divmod(f.numerator, f.denominator)
    return "%d %s" % (w, fr(str(p), str(f.denominator))) if p else str(w)


def one_share(r):
    kind = r.choice(["of", "of", "share", "part"])
    d = r.choice([2, 3, 4, 5, 6, 8, 10])
    n = r.randint(1, d - 1)
    if kind == "of":
        q = d * r.randint(2, 12)
        return QN("What is %s of %d?" % (H(F(n, d)), q), q * n // d, [q // d, q * d // n if q * d % n == 0 and q * d // n != q * n // d else q - n, q - q * n // d],
                  "%d ÷ %d × %d = <b>%d</b>." % (q, d, n, q * n // d))
    if kind == "share":
        k = r.randint(2, 8)
        m = r.randint(1, 7)
        if gcd(m, k) != 1 or m == k:
            return None
        return T("%d rotis are shared equally among %d children. How much does each child get?" % (m, k), H(F(m, k)) if m < k else mixed(F(m, k)),
                 [H(F(k, m)) if k % m else str(k // m), fr("1", str(k)), H(F(m, k + m))], "%d ÷ %d = <b>%s</b> of a roti." % (m, k, H(F(m, k)) if m < k else mixed(F(m, k))))
    t = d * r.randint(1, 3)
    s = t * n // d
    return T("A class has %d students; %d of them are girls. What fraction are girls (in lowest terms)?" % (t, s), H(F(s, t)), [fr(str(s), str(t - s)), H(F(t - s, t)), fr(str(s), str(t + s))] if F(s, t) != F(t - s, t) else [fr(str(s), str(t - s) if t != 2 * s else str(t + 1)), fr("1", str(t)), fr(str(s), str(t + s))],
             "%d out of %d = %s = <b>%s</b>." % (s, t, fr(str(s), str(t)), H(F(s, t))))


def one_mixed(r):
    d = r.choice([2, 3, 4, 5, 6, 7, 8, 9])
    w = r.randint(1, 6)
    p = r.randint(1, d - 1)
    f = F(w * d + p, d)
    if f.denominator != d:
        return None
    if r.random() < 0.5:
        return T("Write %s as an improper fraction." % mixed(f), fr(str(w * d + p), str(d)), [fr(str(w + p), str(d)), fr(str(w * p + d), str(d)), fr(str(w * d + p), str(w))],
                 "%d × %d + %d = %d, so <b>%d/%d</b>." % (w, d, p, w * d + p, w * d + p, d))
    return T("Write %s as a mixed number." % fr(str(w * d + p), str(d)), mixed(f), ["%d %s" % (w + 1, fr(str(p), str(d))), "%d %s" % (w, fr(str(d - p), str(d))), "%d %s" % (w - 1 if w > 1 else w + 2, fr(str(p), str(d)))],
             "%d ÷ %d = %d remainder %d: <b>%d %d/%d</b>." % (w * d + p, d, w, p, w, p, d))


def one_equiv(r):
    kind = r.choice(["miss", "miss", "low", "low", "which"])
    a, b = r.randint(1, 8), r.randint(2, 12)
    if a >= b or gcd(a, b) != 1:
        return None
    k = r.randint(2, 9)
    if kind == "miss":
        return QN("Find the missing number: %s = ?/%d" % (H(F(a, b)), b * k), a * k, [a + b * k - b, a * k + k, b * k - a], "%d × %d = %d and %d × %d = <b>%d</b>." % (b, k, b * k, a, k, a * k))
    if kind == "low":
        return T("Write %s in its lowest terms." % fr(str(a * k), str(b * k)), H(F(a, b)), [fr(str(a * k // 2) if a * k % 2 == 0 else str(a * k), str(b * k // 2) if b * k % 2 == 0 else str(b * k)) if (a * k % 2 or b * k % 2) and F(a, b) != F(a * k, b * k) and False else fr(str(a + k), str(b + k)), fr(str(a * k), str(b)), fr(str(b), str(a)) if a > 1 else fr(str(a * 2), str(b * 3))],
                 "Divide top and bottom by %d: <b>%s</b>." % (k, H(F(a, b))))
    w = [fr(str(a + k), str(b + k)), fr(str(a * k), str(b * (k + 1))), fr(str(a * k + 1), str(b * k))]
    return T("Which fraction is equal to %s?" % H(F(a, b)), fr(str(a * k), str(b * k)), w, "Multiply top and bottom by %d: <b>%d/%d</b>." % (k, a * k, b * k))


def one_cmp(r):
    kind = r.choice(["unit", "same", "cross", "cross"])
    if kind == "unit":
        a, b = r.sample([2, 3, 4, 5, 6, 7, 8, 9, 10, 12], 2)
        big = min(a, b)
        return T("Which is greater: %s or %s?" % (fr("1", str(a)), fr("1", str(b))), fr("1", str(big)), [fr("1", str(max(a, b))), "They are equal", fr("2", str(a + b))],
                 "Fewer equal parts means bigger parts: <b>1/%d</b>." % big)
    if kind == "same":
        d = r.randint(5, 15)
        a, b = r.sample(range(1, d), 2)
        return T("Which is greater: %s or %s?" % (fr(str(a), str(d)), fr(str(b), str(d))), fr(str(max(a, b)), str(d)), [fr(str(min(a, b)), str(d)), "They are equal", fr(str(a + b), str(2 * d))],
                 "Same denominator: the larger numerator wins, <b>%d/%d</b>." % (max(a, b), d))
    x, y = F(r.randint(1, 8), r.randint(3, 9)), F(r.randint(1, 8), r.randint(3, 9))
    if x == y or x >= 1 or y >= 1 or x.denominator == y.denominator:
        return None
    big = max(x, y)
    return T("Which is greater: %s or %s?" % (H(x), H(y)), H(big), [H(min(x, y)), "They are equal", H(F(x.numerator + y.numerator, x.denominator + y.denominator))],
             "Use a common denominator %d: %s and %s. So <b>%s</b> is greater." % (x.denominator * y.denominator // gcd(x.denominator, y.denominator),
                                                                              H(x), H(y), H(big)))


def noimp(fn):
    g = gb(fn)
    pat = __import__("re").compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")

    def f(r):
        it = g(r)
        if not it:
            return None
        for c in it["c"][1:]:
            m = pat.match(c.strip())
            if m and int(m.group(1)) >= int(m.group(2)):
                return None
        return it
    f.__name__ = fn.__name__
    return f


def main():
    unit(6, 0, 7, "fractions", 7, "N", "Fractions: Equal Shares, Equivalent Fractions and Adding Fractions", "fractions",
         "Fractions as equal shares and parts of a collection, fractions on the number line, mixed numbers, equivalent fractions, comparing fractions and adding and subtracting fractions (summary of NCERT Ganita Prakash Class 6)",
         "Class 6 Fractions worksheet (Ganita Prakash Chapter 7): equal shares, fraction of a quantity, mixed numbers, equivalent fractions, comparing, adding and subtracting fractions. 100 questions with answers.",
         "Multiply or divide the top and bottom by the same number", "To add fractions, first make the denominators the same.",
         "<p>A fraction like 3/4 means 3 of 4 equal parts. 3/4 of 20 = 20 ÷ 4 × 3 = 15.</p>"
         "<p><b>Equivalent fractions</b> come from multiplying or dividing top and bottom by the same number: 2/3 = 8/12. Lowest terms: 12/18 = 2/3.</p>"
         "<p>To <b>compare</b> or <b>add</b>, use a common denominator: 1/4 + 2/3 = 3/12 + 8/12 = 11/12.</p>",
         [("Find 2/5 of 35.", ["35 ÷ 5 = 7", "7 × 2"], "14"),
          ("Add 1/2 + 1/3.", ["3/6 + 2/6"], "5/6")],
         ["Adding the denominators: 1/2 + 1/3 = 2/5 is wrong.", "Thinking 1/8 is bigger than 1/5 because 8 is bigger than 5.", "Multiplying only the top to make an equivalent fraction."],
         [("What are equivalent fractions?", "Fractions that name the same amount, such as 1/2, 2/4 and 3/6."),
          ("How do you compare two fractions?", "Write them with the same denominator and compare the numerators."),
          ("How do you add fractions with different denominators?", "Rewrite them with a common denominator, then add the numerators.")],
         [("Equal shares and fractions of a quantity", [(one_share, 20)]),
          ("Mixed numbers and improper fractions", [(one_mixed, 20)]),
          ("Equivalent fractions", [(one_equiv, 20)]),
          ("Comparing fractions", [(one_cmp, 20)]),
          ("Adding and subtracting fractions", [(noimp(af.one_same), 8), (gb(af.one_related), 8), (gb(af.one_mixed), 4)])], R)


if __name__ == "__main__":
    main()
