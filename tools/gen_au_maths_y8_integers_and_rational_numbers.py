# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Integers and rational numbers (Australian Curriculum v9.0: AC9M8N04)
  python3 tools/gen_au_maths_y8_integers_and_rational_numbers.py
Multiplying and dividing integers, powers of negative numbers, the order of operations with integers, the
four operations with negative fractions and decimals, and problems.
Wrong answers come from real mistakes: getting the sign of a product or quotient wrong, squaring a negative to
a negative, working left to right instead of multiplying first, and adding denominators.
"""
import random
from fractions import Fraction as F
from au_hs import num, par, mcq, B, S, make, lesson, collect, QN, T, MINUS, fr, aud

R = random.Random(80301)


def Qn(q, ans, wrongs, e):
    return QN(q, ans, wrongs, e)


# ------------------------------------------------------------ set 3: multiplying
def one_mul(r):
    a = r.choice([-1, 1]) * r.randint(2, 12)
    b = r.choice([-1, 1]) * r.randint(2, 12)
    if a > 0 and b > 0:
        return None
    p = a * b
    q = "Work out %s." % B("%s × %s" % (num(a), par(b)))
    rule = "same signs give a positive" if (a < 0) == (b < 0) else "different signs give a negative"
    e = "%d × %d = %d, and %s. The answer is <b>%s</b>." % (abs(a), abs(b), abs(p), rule, num(p))
    return Qn(q, p, [-p, a + b, -(abs(a) + abs(b)) if a + b != -(abs(a) + abs(b)) else abs(a) + abs(b), -p + 1], e)


def one_sq(r):
    a = -r.randint(2, 9)
    form = r.choice(["sq", "three"])
    if form == "sq":
        p = a * a
        q = "Work out %s." % B("(%s)²" % num(a))
        e = "(%s)² = %s × %s. Two negatives make a positive: <b>%s</b>." % (num(a), num(a), num(a), num(p))
        return Qn(q, p, [-p, 2 * a, -2 * a], e)
    b, c = -r.randint(2, 5), r.choice([-1, 1]) * r.randint(2, 5)
    p = a * b * c
    q = "Work out %s." % B("%s × %s × %s" % (num(a), par(b), par(c)))
    negs = sum(1 for x in (a, b, c) if x < 0)
    e = "%d × %d × %d = %d. There %s %d negative sign%s, so the answer is %s: <b>%s</b>." % (
        abs(a), abs(b), abs(c), abs(p), "is" if negs == 1 else "are", negs, "" if negs == 1 else "s",
        "negative" if p < 0 else "positive", num(p))
    return Qn(q, p, [-p, a + b + c, a * b + c], e)


# ------------------------------------------------------------ set 4: dividing and mixed
def one_div(r):
    b = r.choice([-1, 1]) * r.randint(2, 12)
    c = r.choice([-1, 1]) * r.randint(2, 12)
    a = b * c
    if a > 0 and b > 0:
        return None
    q = "Work out %s." % B("%s ÷ %s" % (num(a), par(b)))
    rule = "same signs give a positive" if (a < 0) == (b < 0) else "different signs give a negative"
    e = "%d ÷ %d = %d, and %s. The answer is <b>%s</b>." % (abs(a), abs(b), abs(c), rule, num(c))
    return Qn(q, c, [-c, a - b, -(c + 1) if c > 0 else -(c - 1)], e)


def one_mixed(r):
    a = r.randint(-9, -2)
    b = r.randint(2, 6)
    c = r.randint(-8, 8)
    if c == 0:
        return None
    kind = r.choice([0, 1, 2])
    if kind == 0:
        val = a * b + c
        expr = "%s × %d + %s" % (num(a), b, par(c))
        wrong = [a * (b + c), -val, a * b - c]
        e = "Multiply first: %s × %d = %s. Then %s + %s = <b>%s</b>." % (num(a), b, num(a * b), num(a * b), par(c), num(val))
    elif kind == 1:
        val = c - a * b
        expr = "%s %s %s × %d" % (num(c), MINUS, par(a), b)
        wrong = [(c - a) * b, c + a * b, -val]
        e = "Multiply first: %s × %d = %s. Then %s %s %s = <b>%s</b>." % (par(a), b, num(a * b), num(c), MINUS, par(a * b), num(val))
    else:
        d = r.choice([2, 3, 4])
        top = a * d
        val = F(top, d) + c
        expr = "%s ÷ %d + %s" % (num(top), d, par(c))
        wrong = [F(top, d + c) if d + c else None, -val, F(top, d) - c]
        e = "Divide first: %s ÷ %d = %s. Then %s + %s = <b>%s</b>." % (num(top), d, num(F(top, d)), num(F(top, d)), par(c), num(val))
    if val == 0:
        return None
    return Qn("Work out %s." % B(expr), val, [w for w in wrong if w is not None and F(w).denominator == 1] + [val + 2, val - 2], e)



# ------------------------------------------------------------ set 4: negative fractions and decimals
def sf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    s = fr(abs(v.numerator), v.denominator)
    return (MINUS + s) if v < 0 else s


def pf(v):
    return "(%s)" % sf(v) if F(v) < 0 else sf(v)


def one_rat(r):
    kind = r.choice(["dmul", "ddiv", "fadd", "fmul", "fdiv", "dadd"])
    if kind == "dmul":
        a = F(r.choice([-1, 1]) * r.randint(2, 9), 10)
        b = r.choice([-1, 1]) * r.randint(2, 9)
        if a > 0 and b > 0:
            return None
        v = a * b
        return QN("Work out %s." % B("%s × %s" % (num(a), par(b))), v, [-v, a + b, v * 10], "%s × %d = %s, then apply the sign rule: <b>%s</b>." % (num(abs(a)), abs(b), num(abs(v)), num(v)), near=(F(1, 10), F(-1, 10)))
    if kind == "ddiv":
        b = F(r.choice([-1, 1]) * r.randint(2, 5), 10)
        c = r.choice([-1, 1]) * r.randint(2, 9)
        a = b * c
        if a > 0 and b > 0:
            return None
        return QN("Work out %s." % B("%s ÷ %s" % (num(a), par(b))), c, [-c, a * b, F(c, 10)], "%s ÷ %s = %d, and the sign rule gives <b>%s</b>." % (num(abs(a)), num(abs(b)), abs(c), num(c)))
    if kind == "dadd":
        a = F(r.randint(-90, 90), 10)
        b = F(r.randint(-90, -5), 10)
        if a == 0 or a + b == 0:
            return None
        v = a + b
        return QN("Work out %s." % B("%s + %s" % (num(a), par(b))), v, [a - b, -v, abs(a) + abs(b)], "Adding a negative moves left: %s + %s = <b>%s</b>." % (num(a), par(b), num(v)), near=(F(1, 10), F(-1, 10)))
    d1, d2 = r.choice([2, 3, 4, 5, 6, 8]), r.choice([2, 3, 4, 5, 6, 8])
    a = F(r.choice([-1, 1]) * r.randint(1, d1 - 1), d1)
    b = F(r.choice([-1, 1]) * r.randint(1, d2 - 1), d2)
    if a > 0 and b > 0:
        return None
    if kind == "fadd":
        v = a + b
        if v == 0:
            return None
        naive = F(a.numerator + b.numerator, a.denominator + b.denominator) if a.denominator + b.denominator else None
        return T("Work out %s." % B("%s + %s" % (sf(a), pf(b))), sf(v), list(dict.fromkeys(w for w in [sf(a - b), sf(-v), sf(naive)] if w != sf(v))),
                 "Use a common denominator, then add with the signs: <b>%s</b>." % sf(v))
    if kind == "fmul":
        v = a * b
        return T("Work out %s." % B("%s × %s" % (sf(a), pf(b))), sf(v), list(dict.fromkeys(w for w in [sf(-v), sf(a + b) if a + b else sf(v * 2), sf(a / b) if a / b != v else sf(v / 2)] if w != sf(v))),
                 "Multiply the numerators and the denominators, then apply the sign rule: <b>%s</b>." % sf(v))
    v = a / b
    return T("Work out %s." % B("%s ÷ %s" % (sf(a), pf(b))), sf(v), list(dict.fromkeys(w for w in [sf(-v), sf(a * b), sf(b / a) if b / a != v else sf(v * 2)] if w != sf(v))),
             "Multiply by the reciprocal, then apply the sign rule: <b>%s</b>." % sf(v))


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("The temperature in Thredbo falls by 3 °C every hour for 5 hours. What is the total change?", "−15 °C", ["15 °C", "−8 °C", "−2 °C"], "5 × (−3) = <b>−15 °C</b>."),
        ("A diver descends at 4 m per minute. Where is she after 6 minutes, starting at sea level?", "−24 m", ["24 m", "−10 m", "−2 m"], "6 × (−4) = <b>−24 m</b>."),
        ("Ethan owes $12 to each of 5 friends. What is his total balance with them?", "−$60", ["$60", "−$17", "−$7"], "5 × (−12) = <b>−60</b>, a debt of $60."),
        ("A share price changed by −$0.40 each day for 5 days. What was the total change?", "−$2.00", ["$2.00", "−$4.50", "−$0.08"], "5 × (−0.40) = <b>−2.00</b>."),
        ("The mean of −4, 6, −8 and 2 is…", "−1", ["1", "−5", "5"], "(−4 + 6 − 8 + 2) ÷ 4 = −4 ÷ 4 = <b>−1</b>."),
        ("Overnight temperatures were −2, −5, 1 and −6 °C. What was the mean?", "−3 °C", ["3 °C", "−14 °C", "−3.5 °C"], "Total = −12, and −12 ÷ 4 = <b>−3 °C</b>."),
        ("Which is the value of (−1)<sup>100</sup>?", "1", ["−1", "100", "−100"], "An even number of negatives multiplies to a positive: <b>1</b>."),
        ("Which is the value of (−1)<sup>7</sup>?", "−1", ["1", "7", "−7"], "An odd number of negatives gives a negative: <b>−1</b>."),
        ("A submarine at −180 m rises a third of the way to the surface. What is its new depth?", "−120 m", ["−60 m", "−240 m", "120 m"], "A third of 180 is 60, so −180 + 60 = <b>−120 m</b>."),
        ("Which product is positive?", "−3 × (−4) × 2", ["−3 × 4 × 2", "−3 × (−4) × (−2)", "3 × 4 × (−2)"], "There are two negatives, so the answer is positive: <b>−3 × (−4) × 2</b> = 24."),
        ("Work out −2 × (3 − 8).", "10", ["−10", "−22", "22"], "Brackets first: 3 − 8 = −5. Then −2 × (−5) = <b>10</b>."),
        ("Work out (−6)<sup>2</sup> − 6<sup>2</sup>.", "0", ["72", "−72", "12"], "(−6)<sup>2</sup> = 36 and 6<sup>2</sup> = 36, so <b>0</b>."),
        ("Work out −3<sup>2</sup>.", "−9", ["9", "6", "−6"], "Only the 3 is squared: −(3 × 3) = <b>−9</b>. Compare (−3)<sup>2</sup> = 9."),
        ("Work out −12 ÷ (−3) − 5.", "−1", ["9", "−9", "1"], "−12 ÷ (−3) = 4, then 4 − 5 = <b>−1</b>."),
        ("Work out (−0.5) × (−0.5).", "0.25", ["−0.25", "1", "2.5"], "0.5 × 0.5 = 0.25, and two negatives give a positive: <b>0.25</b>."),
        ("A bank account has −$45.50. A deposit of $80 is made. What is the balance?", "$34.50", ["−$125.50", "$125.50", "−$34.50"], "−45.50 + 80 = <b>34.50</b>."),
        ("What is half of −7?", "−3.5", ["3.5", "−14", "−7.5"], "−7 ÷ 2 = <b>−3.5</b>."),
        ("Which is larger: −<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span> or −<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>?", "−<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>",
         ["−<span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", "They are equal", "You cannot compare negative fractions"], "−0.33… is closer to 0 than −0.5, so <b>−1/3</b> is larger."),
        ("The product of two integers is −24 and their sum is 2. What are they?", "6 and −4", ["−6 and 4", "8 and −3", "12 and −2"], "6 × (−4) = −24 and 6 + (−4) = 2: <b>6 and −4</b>."),
        ("Work out (−2)<sup>3</sup> + 10.", "2", ["18", "−2", "4"], "(−2)<sup>3</sup> = −8, then −8 + 10 = <b>2</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>For × and ÷: <b>same signs give a positive, different signs give a negative</b>. "
        "With more than two numbers, an even number of negative signs gives a positive answer.</p>"
        "<p>Use the order of operations: brackets, powers, × and ÷, then + and −. The same rules work for negative fractions "
        "and decimals: do the calculation without signs, then decide the sign.</p>",
        [("Work out −6 × 4 and −24 ÷ (−3).", ["6 × 4 = 24, different signs → −24.", "24 ÷ 3 = 8, same signs → 8."], "−24 and 8"),
         ("Work out −3 × 5 + 7.", ["Multiply first: −15.", "−15 + 7."], "−8"),
         ("Work out −<span class='fr'><span class='fn'>2</span><span class='fd'>3</span></span> × <span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span>.", ["2/3 × 3/4 = 6/12 = 1/2.", "Different signs."], "−1/2")],
        ["Getting the sign wrong: −4 × −3 = 12, not −12.",
         "Thinking (−3)² = −9. A negative times a negative is positive, so (−3)² = 9.",
         "Working left to right instead of multiplying first: −3 × 5 + 7 = −8.",
         "Forgetting that −3² means −(3²) = −9."])


def main():
    sets = [S("Multiplying integers", collect(one_mul, 14, R) + collect(one_sq, 6, R)),
            S("Dividing integers", collect(one_div, 20, R)),
            S("Order of operations with integers", collect(one_mixed, 20, R)),
            S("Negative fractions and decimals", collect(one_rat, 20, R)),
            S("Integer and rational number problems", problems())]
    make(8, "integers-and-rational-numbers", 3, "AC9M8N04",
         "Integers and Rational Numbers: The Four Operations with Negatives",
         "Year 8 Integers Worksheets: Multiplying and Dividing Negative Numbers, Fractions and Decimals (Free, Answer Key)",
         "Integers and rational numbers",
         "use the 4 operations with integers and with rational numbers, choosing and using efficient strategies and digital tools where appropriate",
         "Free Year 8 maths worksheets on integers and rational numbers for the Australian Curriculum (AC9M8N04): multiplying and "
         "dividing integers, order of operations, and negative fractions and decimals. 100 questions with an answer key.",
         "Same signs give a positive; different signs give a negative.",
         "Do the calculation without signs, then decide the sign. Use the order of operations.",
         body(),
         [("What is a negative times a negative?", "A positive number. For example −4 × −3 = 12."),
          ("How do I divide negative numbers?", "Divide the numbers as normal, then use the sign rule: same signs give a positive, different signs give a negative."),
          ("Is (−5)² the same as −5²?", "No. (−5)² = 25 because the bracket squares −5. −5² means −(5²) = −25."),
          ("What is a rational number?", "Any number that can be written as a fraction of two integers, such as −3/4, 0.6 or −5.")],
         sets, R)


if __name__ == "__main__":
    main()
