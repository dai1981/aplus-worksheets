# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 8: Working with Fractions
  python3 tools/gen_in_maths_c7_working_with_fractions.py
Multiplying a fraction by a whole number and by a fraction ('of' means multiply), mixed numbers, reciprocals, dividing
by a fraction, and word problems (sharing, recipes, distance, area). Reuses the UK Year 7 makers.
Wrong answers come from real mistakes: multiplying the denominators only, inverting the first fraction when dividing,
and multiplying mixed numbers part by part.
"""
import random
from fractions import Fraction as F
from in_common import unit, T, QN, adopt, gb, fr

R = random.Random(907008)
import gen_uk_maths_y7_multiplying_and_dividing_fractions as md
adopt(md, R)
H = lambda f: fr(str(f.numerator), str(f.denominator)) if f.denominator != 1 else str(f.numerator)


def mixed(f):
    w, p = divmod(f.numerator, f.denominator)
    return ("%d %s" % (w, fr(str(p), str(f.denominator))) if w else H(f)) if p else str(w)


def one_story(r):
    kind = r.choice(["walk", "cloth", "milk", "area", "share"])
    a = F(r.randint(1, 7), r.choice([2, 3, 4, 5, 8]))
    if a.numerator >= a.denominator * 2 or a == 1:
        return None
    if kind == "walk":
        n = r.randint(3, 9)
        v = a * n
        return T("Asha walks %s km every day. How far does she walk in %d days?" % (H(a), n), mixed(v) + " km", [mixed(a + n) + " km", H(F(a.numerator * n, a.denominator * n)) + " km", mixed(v + 1) + " km"],
                 "%s × %d = <b>%s km</b>." % (H(a), n, mixed(v)))
    if kind == "cloth":
        n = r.randint(3, 9)
        b = F(r.randint(2, 9), r.choice([3, 4, 6]))
        v = b / a if False else F(n, 1) / F(1, r.choice([2, 3, 4]))
        u = F(n) / v * n
        piece = F(1, int(v / n))
        return QN("A ribbon %d m long is cut into pieces of %s m each. How many pieces are there?" % (n, H(piece)), n / piece, [n * piece if (n * piece).denominator == 1 else n + 1, n + piece.denominator, n / piece + 1],
                  "%d ÷ %s = %d × %d = <b>%s</b>." % (n, H(piece), n, piece.denominator, n * piece.denominator))
    if kind == "milk":
        n = r.randint(2, 6)
        cup = F(1, r.choice([4, 5, 8]))
        v = n / cup
        return QN("How many glasses of %s litre each can be filled from %d litres of milk?" % (H(cup), n), v, [n * cup if (n * cup).denominator == 1 else n + 2, v + 1, v // 2], "%d ÷ %s = <b>%s</b>." % (n, H(cup), mixed(v)))
    if kind == "area":
        b = F(r.randint(1, 5), r.choice([2, 3, 4]))
        v = a * b
        return T("A rectangle is %s m long and %s m wide. What is its area?" % (H(a), H(b)), mixed(v) + " m²", [mixed(a + b) + " m²", H(F(a.numerator * b.numerator, a.denominator + b.denominator)) + " m²", mixed(2 * (a + b)) + " m²"],
                 "%s × %s = <b>%s m²</b>." % (H(a), H(b), mixed(v)))
    n = r.choice([12, 18, 24, 30, 36, 40])
    k = F(r.randint(1, 3), r.choice([4, 5, 6]))
    if (n * k).denominator != 1:
        return None
    return QN("%s of %d mangoes are ripe. How many are ripe?" % (H(k), n), n * k, [n / k if (n / k).denominator == 1 else n - 1, n * k + 1, n - n * k], "%s × %d = <b>%d</b>." % (H(k), n, n * k))


def main():
    unit(7, 1, 8, "working-with-fractions", 8, "N", "Working with Fractions: Multiplying and Dividing Fractions", "working with fractions",
         "Multiplication of fractions ('of' means ×), multiplying by whole numbers, reciprocals, division of fractions and problems (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Working with Fractions worksheet (Ganita Prakash Part 1, Chapter 8): fraction of a quantity, multiplying fractions, reciprocals, dividing fractions and word problems. 100 questions with answers.",
         "Multiply tops and bottoms; to divide, multiply by the reciprocal", "a/b ÷ c/d = a/b × d/c.",
         "<p>To <b>multiply</b> fractions, multiply the numerators and the denominators: 2/3 × 4/5 = 8/15. 'Of' means multiply: 3/4 of 20 = 15.</p>"
         "<p>The <b>reciprocal</b> of 3/5 is 5/3. To <b>divide</b> by a fraction, multiply by its reciprocal: 3/4 ÷ 1/8 = 3/4 × 8 = 6.</p>"
         "<p>Change mixed numbers to improper fractions before multiplying or dividing.</p>",
         [("Work out 2/5 × 15.", ["15 ÷ 5 × 2"], "6"),
          ("Work out 2/3 ÷ 4/9.", ["2/3 × 9/4 = 18/12"], "1 1/2")],
         ["Multiplying only the numerators.", "Turning the first fraction upside down when dividing.", "Multiplying the whole parts and the fraction parts of mixed numbers separately."],
         [("How do you multiply fractions?", "Multiply the numerators together and the denominators together, then simplify."),
          ("How do you divide by a fraction?", "Multiply by its reciprocal: a/b ÷ c/d = a/b × d/c."),
          ("Why does dividing by 1/4 make a number bigger?", "Because you are counting how many quarters fit, and there are 4 quarters in every whole.")],
         [("Fraction of a quantity", [(gb(md.one_of), 20)]),
          ("Multiplying fractions", [(gb(md.one_mul), 14), (gb(md.one_mul_mixed), 6)]),
          ("Reciprocals", [(gb(md.one_recip), 20)]),
          ("Dividing fractions", [(gb(md.one_div), 20)]),
          ("Fraction problems", [(one_story, 20)])], R)


if __name__ == "__main__":
    main()
