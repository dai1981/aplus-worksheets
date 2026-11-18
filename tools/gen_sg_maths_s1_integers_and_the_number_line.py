# -*- coding: utf-8 -*-
"""
SG Secondary 1 Maths: Negative Numbers (Sec 1 Number)
  python3 gen_sg_maths_s1_integers_and_the_number_line.py
Adding, subtracting, multiplying and dividing with negative numbers, then problems with temperature,
height above sea level and money. Wrong answers come from real mistakes: ignoring a sign, treating
“minus a negative” as minus, and getting the sign of a product or quotient wrong.
"""
import random
from fractions import Fraction as F
from sg_sec import num, par, mcq, B, S, make, lesson, collect, People, sgd, MINUS, QN

R = random.Random(810300)
P = People(R)


def Qn(q, ans, wrongs, e):
    return QN(q, ans, wrongs, e)


# ------------------------------------------------------------ set 1: adding
def one_add(r):
    a = r.choice([r.randint(-15, -1), r.randint(1, 15)])
    b = r.randint(-15, -1)
    if r.random() < 0.3:
        a, b = b, a
    if a + b == 0:
        return None
    s = a + b
    q = "Work out %s." % B("%s + %s" % (num(a), par(b)))
    e = "Start at %s and move %d to the %s on the number line. The answer is <b>%s</b>." % (
        num(a), abs(b), "left" if b < 0 else "right", num(s))
    return Qn(q, s, [-s, a - b, abs(a) + abs(b), b - a], e)


def one_sub_pos(r):
    a = r.randint(-12, 9)
    b = r.randint(2, 15)
    s = a - b
    if a == 0 or s == 0 or s > 0:
        return None
    q = "Work out %s." % B("%s %s %d" % (num(a), MINUS, b))
    e = "Subtracting %d moves %d to the left: %s %s %d = <b>%s</b>." % (b, b, num(a), MINUS, b, num(s))
    return Qn(q, s, [-s, a + b, abs(a) - b if abs(a) != b else -(a + b) + 1, s + 1], e)


# ------------------------------------------------------------ set 2: subtracting a negative
def one_sub_neg(r):
    a = r.randint(-12, 12)
    b = r.randint(-12, -1)
    if a == 0 or a - b == 0:
        return None
    s = a - b
    q = "Work out %s." % B("%s %s %s" % (num(a), MINUS, par(b)))
    e = "Subtracting a negative is the same as adding: %s %s %s = %s + %d = <b>%s</b>." % (
        num(a), MINUS, par(b), num(a), -b, num(s))
    return Qn(q, s, [a + b, -s, -a + b, s - 2], e)


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


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for city, t0, ch in [("Edinburgh", 4, -9), ("Moscow", -6, -11), ("Inverness", -3, 8), ("Oslo", -12, 5),
                         ("Belfast", 2, -7)]:
        t1 = t0 + ch
        q = "In %s the temperature was %s °C. It %s by %d degrees. What is the temperature now?" % (
            city, num(t0), "fell" if ch < 0 else "rose", abs(ch))
        e = "%s %s %d = <b>%s °C</b>." % (num(t0), "+" if ch > 0 else MINUS, abs(ch), num(t1))
        its.append(QN(q, t1, [t0 - ch, -t1, abs(t0) + abs(ch)], e, unit=" °C"))
    for lo, hi, a, b in [(-8, 5, "at night", "at midday"), (-14, -2, "at dawn", "in the afternoon"), (-5, 11, "at midnight", "at noon"),
                         (-21, -9, "overnight", "during the day")]:
        d = hi - lo
        q = "The temperature was %s °C %s and %s °C %s. How many degrees warmer was it %s?" % (
            num(lo), a, num(hi), b, b)
        e = "Difference = %s %s %s = %s + %d = <b>%d degrees</b>." % (num(hi), MINUS, par(lo), num(hi), -lo, d)
        its.append(QN(q, d, [abs(hi + lo), abs(abs(lo) - abs(hi))], e, unit=" degrees", near=(1, 2, -1, 10)))
    for h, depth in [(35, -12), (120, -40), (8, -25), (60, -15)]:
        d = h - depth
        q = "A bird is %d m above sea level. A diver is at %s m (below sea level). How far apart are they vertically?" % (h, num(depth))
        e = "%d %s %s = %d + %d = <b>%d m</b>." % (h, MINUS, par(depth), h, -depth, d)
        its.append(QN(q, d, [abs(h + depth), h, -depth], e, unit=" m"))
    for bal, out in [(40, 65), (15, 50), (-20, 35), (-8, 12)]:
        name, he, his = P.next()
        nb = bal - out
        f = lambda v: (MINUS if v < 0 else "") + sgd(abs(v))
        q = "The balance of %s's bank account is %s. %s pays %s by card. What is the balance now?" % (
            name, f(bal), he.capitalize(), sgd(out))
        e = "%s %s %d = <b>%s</b>." % (num(bal), MINUS, out, f(nb))
        its.append(QN(q, nb, [-nb, bal + out, -(abs(bal) + out)], e, fmt=f))
    for n, ch in [(5, -3), (4, -6), (6, -2)]:
        tot = n * ch
        q = "The temperature falls by %d °C every hour for %d hours. What is the total change?" % (-ch, n)
        e = "%d × %s = <b>%s °C</b> (a fall, so negative)." % (n, par(ch), num(tot))
        its.append(QN(q, tot, [-tot, n + ch, ch - n], e, unit=" °C"))
    return its


def body():
    return lesson(
        "<p>Use a number line. Adding a positive number moves right; adding a negative number moves left.</p>"
        "<p><b>Subtracting a negative is the same as adding</b>: 3 − (−5) = 3 + 5 = 8.</p>"
        "<p>For × and ÷: <b>same signs give a positive, different signs give a negative</b>.</p>",
        [("Work out −4 + (−6).", ["Start at −4 and move 6 to the left."], "−10"),
         ("Work out −2 − (−7).", ["Subtracting −7 is adding 7: −2 + 7."], "5"),
         ("Work out −6 × 4 and −24 ÷ (−3).", ["6 × 4 = 24, different signs → −24.", "24 ÷ 3 = 8, same signs → 8."], "−24 and 8")],
        ["Treating 3 − (−5) as 3 − 5. Two minus signs next to each other make a plus.",
         "Thinking −4 + (−6) = 10. Adding a negative makes the number smaller.",
         "Thinking (−3)² = −9. A negative times a negative is positive, so (−3)² = 9.",
         "For a temperature difference, subtracting the wrong way: from −8 °C to 5 °C is 13 degrees, not 3."])


def main():
    sets = [S("Adding and subtracting", collect(one_add, 12, R) + collect(one_sub_pos, 8, R)),
            S("Subtracting a negative number", collect(one_sub_neg, 20, R)),
            S("Multiplying", collect(one_mul, 14, R) + collect(one_sq, 6, R)),
            S("Dividing and mixed calculations", collect(one_div, 10, R) + collect(one_mixed, 10, R)),
            S("Problems in context", problems())]
    make(1, "integers-and-the-number-line", 2, "N1",
         "Integers and Negative Numbers: The Number Line and Four Operations",
         "Secondary 1 Negative Numbers Worksheets: Adding, Subtracting, Multiplying and Dividing with Answers",
         "Integers and negative numbers",
         "Use the four operations, including formal written methods, applied to integers, decimals, proper and improper "
         "fractions, and mixed numbers, all both positive and negative; order positive and negative integers.",
         "Free Secondary 1 maths worksheets on negative numbers: adding and subtracting negatives, subtracting a negative, "
         "multiplying and dividing with the sign rules, and temperature and money problems. 100 questions with answers.",
         "Subtracting a negative is adding: 3 − (−5) = 8.",
         "For × and ÷, same signs give a positive and different signs give a negative.",
         body(),
         [("Why does subtracting a negative number give a bigger answer?", "Taking away a debt leaves you better off. On the number line, 3 − (−5) means the gap from −5 up to 3, which is 8."),
          ("What is a negative times a negative?", "A positive number. For example −4 × −3 = 12."),
          ("Is (−5)² the same as −5²?", "No. (−5)² = 25 because the bracket squares −5. −5² usually means −(5²) = −25."),
          ("How do I find the difference between −8 °C and 5 °C?", "Subtract the lower from the higher: 5 − (−8) = 13 degrees.")],
         sets, R)


if __name__ == "__main__":
    main()
