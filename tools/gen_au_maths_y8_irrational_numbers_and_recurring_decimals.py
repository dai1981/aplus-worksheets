# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Irrational Numbers and Recurring Decimals (Australian Curriculum v9.0: AC9M8N01, AC9M8N03)
  python3 tools/gen_au_maths_y8_irrational_numbers_and_recurring_decimals.py
Terminating and recurring decimals, writing fractions as decimals with recurring notation, writing recurring
decimals as fractions, rational and irrational numbers, and square roots and π in applied contexts.
Wrong answers come from real mistakes: thinking every long decimal is irrational, thinking √ of any number is
irrational, writing 0.3 for one third, and using 22/7 or 3.14 as the exact value of π.
"""
import random
from fractions import Fraction as F
from math import isqrt, sqrt, pi
from au_hs import num, B, S, make, lesson, collect, T, fr, dec

R = random.Random(80101)


def frs(v):
    v = F(v)
    return num(v) if v.denominator == 1 else fr(v.numerator, v.denominator)


def rec(v):
    """Decimal string for a fraction in [0, 10), with the repeating block under a bar."""
    v = F(v)
    whole, rem = divmod(v.numerator, v.denominator)
    d = v.denominator
    digits, seen = [], {}
    while rem and rem not in seen:
        seen[rem] = len(digits)
        rem *= 10
        digits.append(str(rem // d))
        rem %= d
    if not rem:
        return str(whole) + ("." + "".join(digits) if digits else "")
    k = seen[rem]
    return "%d.%s<span class='ov'>%s</span>" % (whole, "".join(digits[:k]), "".join(digits[k:]))


def plain(v, n=6):
    """The first n decimal places, without a bar (a common mistake)."""
    v = F(v)
    return ("%." + str(n) + "f") % float(v)


def terminates(d):
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


# ------------------------------------------------------------ set 1: terminating or recurring
def one_tr(r):
    d = r.choice([3, 4, 6, 7, 8, 9, 11, 12, 15, 16, 20, 24, 25, 30, 40, 45, 50, 18, 14, 35])
    k = r.randint(1, d - 1)
    v = F(k, d)
    if v.denominator in (1,):
        return None
    t = terminates(v.denominator)
    q = "Is %s a terminating or a recurring decimal?" % B(frs(v))
    right = "Terminating" if t else "Recurring"
    e = ("In simplest form the denominator is %d, which has no prime factors other than 2 and 5, so it <b>terminates</b>: %s." if t else
         "In simplest form the denominator is %d, which has a prime factor other than 2 or 5, so it <b>recurs</b>: %s.") % (v.denominator, rec(v))
    return T(q, right, ["Terminating" if not t else "Recurring", "Neither, it is irrational", "It depends on the calculator"], e)


# ------------------------------------------------------------ set 2: fractions to decimals
def one_f2d(r):
    d = r.choice([3, 6, 9, 11, 12, 15, 7, 8, 16, 33, 18, 22])
    k = r.randint(1, d - 1)
    v = F(k, d)
    if v.denominator < 3:
        return None
    p, q_ = v.numerator, v.denominator
    q = "Write %s as a decimal." % B(frs(v))
    right = rec(v)
    nobar = right.replace("<span class='ov'>", "").replace("</span>", "")
    recip = F(q_, p)
    wr = [plain(v, 2), nobar, rec(recip) if recip < 10 else "%d.%d" % (p, q_), "%d.%d" % (p, q_)]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    e = "Divide %d by %d: %d ÷ %d = %s…, so %s = <b>%s</b>." % (p, q_, p, q_, plain(v, 6), frs(v), right)
    if "ov" in right:
        e += " The bar shows the digits that repeat. %s is only an approximation." % plain(v, 2)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 3: recurring decimals to fractions
def one_d2f(r):
    kind = r.choice(["one", "two", "mixed"])
    if kind == "one":
        a = r.randint(1, 8)
        v = F(a, 9)
        q = "Write %s as a fraction in simplest form." % B("0.<span class='ov'>%d</span>" % a)
        e = "Let <i>x</i> = 0.%d%d%d… Then 10<i>x</i> = %d.%d%d… Subtract: 9<i>x</i> = %d, so <i>x</i> = <b>%s</b>." % (a, a, a, a, a, a, a, frs(v)) if v == F(a, 9) and F(a, 9).denominator == 9 else "Let <i>x</i> = 0.%d%d%d… Then 10<i>x</i> = %d.%d%d… Subtract: 9<i>x</i> = %d, so <i>x</i> = %s = <b>%s</b>." % (a, a, a, a, a, a, a, fr(a, 9), frs(v))
        return T(q, frs(v), list(dict.fromkeys(w for w in [fr(a, 10), fr(a, 99), fr(a, 100)] if w != frs(v))), e)
    if kind == "two":
        ab = r.randint(10, 98)
        if ab % 11 == 0:
            return None
        v = F(ab, 99)
        q = "Write %s as a fraction in simplest form." % B("0.<span class='ov'>%02d</span>" % ab)
        e = "Let <i>x</i> = 0.%02d%02d… Then 100<i>x</i> = %d.%02d… Subtract: 99<i>x</i> = %d, so <i>x</i> = %s<b>%s</b>." % (ab, ab, ab, ab, ab, "" if v.denominator == 99 else fr(ab, 99) + " = ", frs(v))
        return T(q, frs(v), list(dict.fromkeys(w for w in [fr(ab, 100), fr(ab, 9) if ab < 90 else fr(ab, 999), frs(F(ab, 90))] if w != frs(v))), e)
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b:
        return None
    v = F(10 * a + b - a, 90)
    q = "Write %s as a fraction in simplest form." % B("0.%d<span class='ov'>%d</span>" % (a, b))
    e = "Let <i>x</i> = 0.%d%d%d… Then 100<i>x</i> = %d%d.%d… and 10<i>x</i> = %d.%d… Subtract: 90<i>x</i> = %d, so <i>x</i> = %s = <b>%s</b>." % (
        a, b, b, a, b, b, a, b, 10 * a + b - a, fr(10 * a + b - a, 90), frs(v))
    return T(q, frs(v), list(dict.fromkeys(w for w in [frs(F(10 * a + b, 99)), frs(F(10 * a + b, 100)), frs(F(10 * a + b, 90))] if w != frs(v)))[:3], e)


# ------------------------------------------------------------ set 4: rational or irrational
def one_ri(r):
    kind = r.choice(["sq", "sq", "nsq", "nsq", "frac", "dec", "pi", "rec"])
    if kind == "sq":
        k = r.randint(2, 15)
        x = "√%d" % (k * k)
        return T("Is %s rational or irrational?" % B(x), "Rational", ["Irrational", "Neither", "Both"], "√%d = %d, a whole number, so it is <b>rational</b>." % (k * k, k))
    if kind == "nsq":
        nn = r.randint(2, 99)
        if isqrt(nn) ** 2 == nn:
            return None
        return T("Is %s rational or irrational?" % B("√%d" % nn), "Irrational", ["Rational", "Neither", "Rational, because it is a square root"],
                 "%d is not a perfect square, so √%d = %s… never ends or repeats: <b>irrational</b>." % (nn, nn, ("%.5f" % sqrt(nn))))
    if kind == "frac":
        a, b = r.randint(1, 20), r.randint(2, 13)
        return T("Is %s rational or irrational?" % B(fr(a, b)), "Rational", ["Irrational", "Neither", "Irrational, because the decimal is long"], "Any fraction of two integers is <b>rational</b>.")
    if kind == "dec":
        x = r.choice(["0.125", "−4.6", "3.75", "12", "−7", "0.05"])
        return T("Is %s rational or irrational?" % B(x), "Rational", ["Irrational", "Neither", "Only if it is positive"], "%s can be written as a fraction, so it is <b>rational</b>." % x)
    if kind == "rec":
        x = r.choice(["0.<span class='ov'>6</span>", "1.<span class='ov'>27</span>", "0.1<span class='ov'>3</span>", "2.<span class='ov'>142857</span>"])
        return T("Is %s rational or irrational?" % B(x), "Rational", ["Irrational", "Neither", "Irrational, because it never ends"],
                 "A recurring decimal repeats, so it can be written as a fraction: <b>rational</b>.")
    x = r.choice(["π", "2π", "π + 1", "√2 + 1", "3√5"])
    return T("Is %s rational or irrational?" % B(x), "Irrational", ["Rational", "Rational, because π = 3.14", "Rational, because π = 22/7"],
             "π and √ of a non-square number are irrational, and %s is still irrational: its decimal never ends or repeats." % x)


# ------------------------------------------------------------ set 5: applied problems
def problems():
    data = [
        ("A square has an area of 2 m². How long is each side?", "√2 m, about 1.41 m", ["1 m", "2 m", "0.5 m"], "Side × side = 2, so the side is <b>√2 m ≈ 1.41 m</b>, an irrational number."),
        ("A square has sides of 1 m. How long is its diagonal?", "√2 m", ["2 m", "1.5 m", "1 m"], "By Pythagoras, 1² + 1² = 2, so the diagonal is <b>√2 m</b>."),
        ("Between which two whole numbers does √50 lie?", "7 and 8", ["5 and 6", "6 and 7", "25 and 26"], "7² = 49 and 8² = 64, so √50 is between <b>7 and 8</b>."),
        ("Between which two whole numbers does √20 lie?", "4 and 5", ["3 and 4", "5 and 6", "10 and 11"], "4² = 16 and 5² = 25, so √20 is between <b>4 and 5</b>."),
        ("Which is the best estimate of √30?", "5.5", ["15", "6.5", "5.1"], "5² = 25 and 6² = 36; 30 is about halfway, so √30 ≈ <b>5.5</b> (it is 5.477…)."),
        ("Which of these is exactly equal to π?", "None of them", ["3.14", "22/7", "3.1416"], "π is irrational, so <b>no fraction or terminating decimal</b> is exactly π."),
        ("A circular garden has a diameter of 10 m. Which is the exact circumference?", "10π m", ["31.4 m", "31 m", "100π m"], "<i>C</i> = π<i>d</i> = <b>10π m</b>. 31.4 m is only an approximation."),
        ("Which list contains only rational numbers?", "0.5, −3, 2/7, 0.<span class='ov'>3</span>", ["0.5, √2, 3", "π, 4, −1", "√9, √10, 1/2"],
         "Each of 0.5, −3, 2/7 and 0.<span class='ov'>3</span> can be written as a fraction: <b>all rational</b>."),
        ("Mia says 3.14159265 is irrational because it has many decimal places. Is she right?", "No, it terminates, so it is rational", ["Yes", "Yes, because it is π", "No, it is an integer"],
         "It stops after 8 decimal places, so it equals 314159265/100000000: <b>rational</b>."),
        ("Which fraction gives a recurring decimal?", fr(5, 12), [fr(3, 8), fr(7, 20), fr(9, 25)], "12 = 2 × 2 × 3 has a factor of 3, so 5/12 = 0.41<span class='ov'>6</span> <b>recurs</b>."),
        ("Which fraction gives a terminating decimal?", fr(7, 40), [fr(1, 3), fr(5, 6), fr(2, 7)], "40 = 2 × 2 × 2 × 5, so 7/40 = 0.175 <b>terminates</b>."),
        ("What is 1/7 as a decimal?", "0.<span class='ov'>142857</span>", ["0.7", "0.14", "1.7"], "1 ÷ 7 = 0.142857142857…, so the block 142857 repeats: <b>0.<span class='ov'>142857</span></b>."),
        ("How many digits are in the repeating block of 1/7?", "6", ["1", "2", "7"], "1/7 = 0.<span class='ov'>142857</span>: <b>6</b> digits repeat."),
        ("A calculator shows 0.6666666667 for 2 ÷ 3. Why does the last digit show 7?", "The calculator rounds the recurring 6s", ["2/3 is irrational", "The answer is really 0.6666666667", "The calculator made a mistake in the 6s"],
         "2/3 = 0.<span class='ov'>6</span> forever; the screen has to <b>round</b> the last digit."),
        ("Which number lies between 3 and 4?", "√10", ["√8", "√17", "√3"], "3² = 9 and 4² = 16, so √10 is between 3 and 4: <b>√10</b>."),
        ("Order from smallest to largest: π, √10, 3.1", "3.1, π, √10", ["π, 3.1, √10", "√10, π, 3.1", "3.1, √10, π"], "3.1 &lt; π ≈ 3.142 &lt; √10 ≈ 3.162: <b>3.1, π, √10</b>."),
        ("Is 0.<span class='ov'>9</span> equal to 1?", "Yes", ["No, it is a bit less than 1", "No, it is irrational", "Only on a calculator"], "Let <i>x</i> = 0.999… Then 10<i>x</i> − <i>x</i> = 9, so <i>x</i> = 1: <b>yes</b>."),
        ("A cube has a volume of 20 cm³. Its edge length is ∛20 cm. Which is the best estimate?", "2.7 cm", ["6.7 cm", "4.5 cm", "10 cm"], "2³ = 8 and 3³ = 27, and 20 is close to 27, so ∛20 ≈ <b>2.7 cm</b> (2.714…)."),
        ("Which is irrational?", "√12", ["√16", "√0.25", "√(9/4)"], "√16 = 4, √0.25 = 0.5 and √(9/4) = 1.5 are rational. <b>√12</b> is not a perfect square, so it is irrational."),
        ("A running track has a circular end of radius 36.5 m. Why is the length of its curve not a whole number of metres?", "It involves π, which is irrational", ["Tracks are never measured exactly", "36.5 is irrational", "Circles have no length"],
         "Length = π × 36.5, and multiplying by π gives an irrational number: <b>it involves π</b>."),
    ]
    out = []
    for q, a, w, e in data:
        e = e.replace("2/7", fr(2, 7)).replace("5/12", fr(5, 12)).replace("7/40", fr(7, 40)).replace("1/7 =", fr(1, 7) + " =").replace("2/3 =", fr(2, 3) + " =")
        q = q.replace("1/7", fr(1, 7)).replace("2/7", fr(2, 7))
        a = a.replace("2/7", fr(2, 7))
        w = [x.replace("22/7", fr(22, 7)) for x in w]
        out.append(T(q, a, w, e))
    return out


def body():
    return lesson(
        "<p>A <b>rational number</b> can be written as a fraction of two integers. Its decimal either <b>terminates</b> (0.375) or "
        "<b>recurs</b> (0.<span class='ov'>3</span> = 0.333…). A bar shows the repeating block: 0.<span class='ov'>27</span> = 0.272727…</p>"
        "<p>A fraction in simplest form terminates only when its denominator has no prime factors other than 2 and 5.</p>"
        "<p>An <b>irrational number</b> has a decimal that never ends and never repeats, so it cannot be written as a fraction. "
        "Examples are π and the square root of any whole number that is not a perfect square, such as √2. "
        "3.14 and " + fr(22, 7) + " are only approximations of π.</p>",
        [("Write " + fr(5, 6) + " as a decimal.", ["5 ÷ 6 = 0.8333…"], "0.8<span class='ov'>3</span>"),
         ("Write 0.<span class='ov'>45</span> as a fraction.", ["Let <i>x</i> = 0.4545… so 100<i>x</i> = 45.4545…", "99<i>x</i> = 45, so <i>x</i> = 45/99."], fr(5, 11)),
         ("Is √36 rational?", ["√36 = 6."], "Yes")],
        ["Thinking every square root is irrational: √49 = 7 is rational.",
         "Thinking a long decimal on a calculator must be irrational. 2 ÷ 3 = 0.<span class='ov'>6</span> is rational.",
         "Writing " + fr(1, 3) + " as 0.3. It is 0.<span class='ov'>3</span>.",
         "Using 3.14 or " + fr(22, 7) + " as the exact value of π."])


def main():
    sets = [S("Terminating or recurring?", collect(one_tr, 20, R)),
            S("Fractions to decimals", collect(one_f2d, 20, R)),
            S("Recurring decimals to fractions", collect(one_d2f, 20, R)),
            S("Rational or irrational?", collect(one_ri, 20, R)),
            S("Square roots and π in context", problems())]
    make(8, "irrational-numbers-and-recurring-decimals", 1, "AC9M8N01",
         "Irrational Numbers and Recurring Decimals",
         "Year 8 Irrational Numbers Worksheets: Terminating and Recurring Decimals, Rational and Irrational Numbers (Free, Answer Key)",
         "Irrational numbers and recurring decimals",
         "recognise irrational numbers in applied contexts, including square roots and π",
         "Free Year 8 maths worksheets on rational and irrational numbers for the Australian Curriculum (AC9M8N01, AC9M8N03): terminating "
         "and recurring decimals, recurring decimals as fractions, square roots and π. 100 questions with an answer key.",
         "Rational numbers terminate or recur. Irrational numbers never end and never repeat.",
         "π and √ of a non-square whole number are irrational. A fraction terminates only if its denominator has just 2s and 5s.",
         body(),
         [("What is an irrational number?", "A number that cannot be written as a fraction of two integers. Its decimal never ends and never repeats, like π or √2."),
          ("Is a recurring decimal rational?", "Yes. Every recurring decimal can be written as a fraction, for example 0.333… = 1/3."),
          ("How can I tell if a fraction gives a terminating decimal?", "Simplify it. If the denominator has no prime factors other than 2 and 5, the decimal terminates; otherwise it recurs."),
          ("Is π equal to 22/7?", "No. 22/7 and 3.14 are close approximations, but π is irrational, so no fraction is exactly equal to it.")],
         sets, R)


if __name__ == "__main__":
    main()
