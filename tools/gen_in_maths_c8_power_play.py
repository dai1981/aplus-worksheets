# -*- coding: utf-8 -*-
"""
India Class 8 Maths, Ganita Prakash Part 1, Chapter 2: Power Play
  python3 tools/gen_in_maths_c8_power_play.py
Exponents, the laws of exponents (product, quotient, power of a power, zero and negative exponents), powers of 10,
scientific notation, and exponential growth (doubling, paper folding).
Wrong answers come from real mistakes: multiplying the exponents instead of adding, 2⁵ read as 2 × 5, 4⁻² taken as −16,
a⁰ = 0, and a first number of 10 or more in scientific notation.
"""
import random, re
from in_common import num, unit, T, QN, adopt, gb
import gen_uk_maths_y8_indices as ix
import gen_uk_maths_y8_standard_form as sf

R = random.Random(908002)
adopt(ix, R)
adopt(sf, R)


def sci(fn):
    g = gb(fn)

    def f(r):
        it = g(r)
        if not it:
            return None
        fix = lambda t: re.sub(r"standard form", "scientific notation", t)
        it["q"], it["e"] = fix(it["q"]), fix(it["e"])
        return it
    f.__name__ = fn.__name__
    return f


def one_power(r):
    b, e = r.choice([(2, r.randint(3, 10)), (3, r.randint(2, 6)), (5, r.randint(2, 5)), (4, r.randint(2, 5)), (10, r.randint(3, 7)), (6, 3), (7, 3)])
    return QN("Find the value of %d<sup>%d</sup>." % (b, e), b ** e, [b * e, e ** b if e ** b != b ** e else b ** e + b, b ** (e - 1)],
              "%s = <b>%s</b>." % (" × ".join([str(b)] * e), num(b ** e)))


def one_expo(r):
    kind = r.choice(["write", "write", "compare", "zero"])
    if kind == "write":
        b = r.choice([2, 3, 5, 7])
        e = r.randint(3, 7)
        return T("Write %s in exponential form." % num(b ** e), "%d<sup>%d</sup>" % (b, e), ["%d<sup>%d</sup>" % (e, b), "%d × %d" % (b, e), "%d<sup>%d</sup>" % (b, e + 1)],
                 "%s = %s = <b>%d<sup>%d</sup></b>." % (num(b ** e), " × ".join([str(b)] * e), b, e))
    if kind == "zero":
        a = r.choice([5, 7, 12, 100, 2026])
        return T("What is the value of %s<sup>0</sup>?" % num(a), "1", ["0", num(a), "Not defined"], "Any non-zero number to the power 0 is <b>1</b>.")
    a, b = r.choice([(2, 5), (3, 4), (2, 6), (3, 5), (4, 3), (2, 7), (5, 3)])
    big = "%d<sup>%d</sup>" % (a, b) if a ** b > b ** a else "%d<sup>%d</sup>" % (b, a)
    return T("Which is greater: %d<sup>%d</sup> or %d<sup>%d</sup>?" % (a, b, b, a), big, ["%d<sup>%d</sup>" % (b, a) if big.startswith(str(a) + "<") else "%d<sup>%d</sup>" % (a, b), "They are equal", "You cannot tell"],
             "%d<sup>%d</sup> = %s and %d<sup>%d</sup> = %s, so <b>%s</b> is greater." % (a, b, num(a ** b), b, a, num(b ** a), big))


def one_growth(r):
    kind = r.choice(["fold", "double", "bacteria"])
    if kind == "fold":
        n = r.randint(3, 10)
        return QN("A sheet of paper is folded in half %d times. How many layers thick is it?" % n, 2 ** n, [2 * n, n * n, 2 ** (n - 1)],
                  "Each fold doubles the layers: 2<sup>%d</sup> = <b>%s</b>." % (n, num(2 ** n)))
    if kind == "double":
        start = r.choice([5, 10, 25, 100])
        n = r.randint(3, 8)
        return QN("A number of followers doubles every week. It starts at %d. How many followers after %d weeks?" % (start, n), start * 2 ** n,
                  [start * 2 * n, start + 2 ** n, start * 2 ** (n - 1)], "%d × 2<sup>%d</sup> = <b>%s</b>." % (start, n, num(start * 2 ** n)))
    k = r.choice([3, 10])
    n = r.randint(2, 6)
    return QN("A cell divides into %d new cells every hour (each old cell is replaced). Starting with 1 cell, how many cells are there after %d hours?" % (k, n), k ** n,
              [k * n, k ** (n - 1), k ** n + 1], "%d<sup>%d</sup> = <b>%s</b>." % (k, n, num(k ** n)))


def main():
    unit(8, 1, 2, "power-play", 2, "N", "Power Play: Exponents and Scientific Notation", "power play",
         "Exponents and powers, the laws of exponents, negative and zero exponents, powers of 10, scientific notation and exponential growth (summary of NCERT Ganita Prakash Class 8)",
         "Class 8 Power Play worksheet (Ganita Prakash Part 1, Chapter 2): exponents, laws of exponents, negative exponents, scientific notation and exponential growth. 100 questions with answers.",
         "aᵐ × aⁿ = aᵐ⁺ⁿ", "aᵐ ÷ aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ and a⁰ = 1.",
         "<p>An <b>exponent</b> tells how many times the base is multiplied: 2<sup>5</sup> = 2 × 2 × 2 × 2 × 2 = 32.</p>"
         "<p>Laws: multiply → add the exponents; divide → subtract; power of a power → multiply. a<sup>0</sup> = 1 and a<sup>−n</sup> = 1/a<sup>n</sup>.</p>"
         "<p><b>Scientific notation</b> writes a number as a × 10<sup>n</sup> with 1 ≤ a &lt; 10, such as 3,40,000 = 3.4 × 10<sup>5</sup>.</p>",
         [("Simplify 3<sup>4</sup> × 3<sup>5</sup>.", ["Same base: add the exponents"], "3<sup>9</sup>"),
          ("Write 0.00052 in scientific notation.", ["Move the point 4 places right"], "5.2 × 10<sup>−4</sup>")],
         ["Working out 2<sup>5</sup> as 2 × 5 = 10.", "Multiplying the exponents in a<sup>3</sup> × a<sup>4</sup> (it is a<sup>7</sup>, not a<sup>12</sup>).", "Thinking 4<sup>−2</sup> is negative. It is 1/16."],
         [("What are the laws of exponents?", "aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, a⁰ = 1 and a⁻ⁿ = 1/aⁿ."),
          ("What is scientific notation?", "A way to write very large or small numbers as a × 10ⁿ, where 1 ≤ a < 10 and n is an integer."),
          ("Why is any number to the power 0 equal to 1?", "Because aⁿ ÷ aⁿ = 1, and by the quotient law it is also a⁰.")],
         [("Powers and exponential form", [(one_power, 10), (one_expo, 10)]),
          ("Multiplying and dividing powers", [(gb(ix.one_mul), 7), (gb(ix.one_div), 7), (gb(ix.one_eval), 6)]),
          ("Power of a power, zero and negative exponents", [(gb(ix.one_pp), 7), (gb(ix.one_neg), 7), (gb(ix.one_alg), 6)]),
          ("Scientific notation", [(sci(sf.one_big), 6), (sci(sf.one_small), 6), (sci(sf.one_back), 6), (sci(sf.one_order), 2)]),
          ("Exponential growth and problems", [(one_growth, 14), (sci(sf.one_md), 6)])], R)


if __name__ == "__main__":
    main()
