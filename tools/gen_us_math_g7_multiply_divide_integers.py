# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Multiplying and Dividing Integers and Rational Numbers (7.NS.A.2)
  python tools/gen_us_math_g7_multiply_divide_integers.py
Wrong answers come from real mistakes: the wrong sign, using the adding rules (−6 × −4 -> −24 or −10),
adding instead of multiplying, multiplying instead of dividing, counting the negative signs wrongly,
and forgetting to flip the second fraction when dividing.
"""
import random
from fractions import Fraction as F
from ws_common import (num, par, nums, mcq, balance, People, B, table, example, write_unit, MINUS, fr)

R = random.Random(70201)
UPDATED = "2026-11-09"
TIMES = " × "
DIV = " ÷ "


def n(v, st="d"):
    return num(v, st)


def sign_word(v):
    return "positive" if v > 0 else "negative"


def why_mul(a, b, st="d", op="×"):
    a, b = F(a), F(b)
    r = a * b if op == "×" else a / b
    same = (a < 0) == (b < 0)
    size = abs(r)
    return ("The signs are %s, so the answer is %s. %s %s %s = %s, so %s %s %s = %s."
            % ("the same" if same else "different", sign_word(r), num(abs(a), st), op, num(abs(b), st), num(size, st),
               num(a, st), op, par(b, st), num(r, st)))


def mul_item(a, b, st="d", ask="Find %s."):
    a, b = F(a), F(b)
    p = a * b
    expr = num(a, st) + TIMES + par(b, st)
    ws = [-p, a + b, -(a + b), abs(a) + abs(b), p + a, p - b]
    e = why_mul(a, b, st)
    if (a < 0) and (b < 0):
        e += " Not %s: two negatives multiply to a positive (the adding rule does not apply)." % num(-p, st)
    else:
        e += " Not %s: check the sign." % num(-p, st)
    return mcq(ask % B(expr), (num(p, st), p), nums(ws, st), e)


def div_item(a, b, st="d", ask="Find %s."):
    a, b = F(a), F(b)
    q = a / b
    expr = num(a, st) + DIV + par(b, st)
    ws = [-q, a * b if abs(a * b) < 1000 else None, -(a * b) if abs(a * b) < 1000 else None, a - b, a + b, q + 1, q - 1]
    e = why_mul(a, b, st, "÷") + " Check: %s × %s = %s." % (num(q, st), par(b, st), num(a, st))
    return mcq(ask % B(expr), (num(q, st), q), nums(ws, st), e)


# ------------------------------------------------------------ set 1
def set_multiply():
    its = []
    # sign rule questions
    rules = [("positive × negative", "negative", ["positive", "zero", "it depends on which number is bigger"]),
             ("negative × negative", "positive", ["negative", "zero", "it depends on which number is bigger"]),
             ("negative ÷ positive", "negative", ["positive", "zero", "it depends on which number is bigger"])]
    for r, good, bad in rules:
        its.append(mcq("What is the sign of the answer to %s?" % B(r), (good, good), [(b, b) for b in bad],
                       "Same signs give a positive answer. Different signs give a negative answer. The sizes do not change the sign."))
    pairs = [(-3, 4), (5, -6), (-7, -2), (-8, 9), (6, -7), (-9, -4), (-5, 8), (-12, -3), (7, -8), (-4, -11),
             (0, -9), (-6, 12), (-15, -4), (11, -5), (-1, -23), (-25, 4)]
    for a, b in pairs:
        if a == 0:
            its.append(mcq("Find %s." % B("0" + TIMES + par(b)), ("0", 0), nums([b, -b, 1]),
                           "Zero times any number is 0. Zero is neither positive nor negative."))
        else:
            its.append(mul_item(a, b))
    # missing factor
    its.append(mcq("Which number makes %s true?" % B("? × (−6) = 42"), ("−7", -7), nums([7, 36, -36, 48]),
                   "−7 × (−6) = 42: two negatives give a positive. 7 × (−6) = −42, so 7 does not work."))
    return {"title": "Multiply integers: the sign rules", "items": its[:20]}


# ------------------------------------------------------------ set 2
def set_divide():
    its = []
    pairs = [(-24, 6), (35, -7), (-48, -8), (-63, 9), (72, -8), (-54, -6), (81, -9), (-56, 7), (-96, -12),
             (0, -5), (-144, 12), (120, -15), (-91, -7), (-75, 25), (-200, -40)]
    for a, b in pairs:
        if a == 0:
            its.append(mcq("Find %s." % B("0" + DIV + "(−5)"), ("0", 0), nums([-5, 5, 1]),
                           "0 ÷ (−5) = 0, because 0 × (−5) = 0. (Dividing by 0 is not possible, but dividing 0 is fine.)"))
        else:
            its.append(div_item(a, b))
    its.append(mcq("Which number makes %s true?" % B("−45 ÷ ? = 9"), ("−5", -5), nums([5, -36, 54, -54]),
                   "−45 ÷ (−5) = 9, because 9 × (−5) = −45. Different signs would give a negative answer."))
    its.append(mcq("Which is the same as %s?" % B("−20 ÷ 4"), ("20 ÷ (−4)", "a"),
                   [("−20 ÷ (−4)", "b"), ("20 ÷ 4", "c"), ("4 ÷ (−20)", "d")],
                   "−20 ÷ 4 = −5 and 20 ÷ (−4) = −5. Moving the negative sign to the other number does not change the answer: −(p ÷ q) = (−p) ÷ q = p ÷ (−q)."))
    its.append(mcq("What is %s?" % B("−7 ÷ 0"), ("It is undefined.", "u"), [("0", "z"), ("−7", "m"), ("7", "p")],
                   "Dividing by 0 is undefined: no number times 0 gives −7."))
    its.append(mcq("Which equals %s?" % B(MINUS + "(18 ÷ 3)"), ("(−18) ÷ 3", "a"),
                   [("(−18) ÷ (−3)", "b"), ("18 ÷ 3", "c"), ("3 ÷ (−18)", "d")],
                   "−(18 ÷ 3) = −6, and (−18) ÷ 3 = −6. (−18) ÷ (−3) is positive 6."))
    its.append(mcq("A quotient of two integers is negative. What must be true?", ("The integers have different signs.", "a"),
                   [("Both integers are negative.", "b"), ("Both integers are positive.", "c"), ("The first integer is larger.", "d")],
                   "A quotient is negative only when one number is positive and the other is negative."))
    return {"title": "Divide integers", "items": its}


# ------------------------------------------------------------ set 3
def set_many():
    its = []
    prods = [[-2, 3, -4], [-1, -5, -2], [3, -2, -2, -5], [-1, -1, -1, -1, -1], [-2, -2, -2], [4, -3, 0, -7],
             [-10, 2, -3], [-6, -1, -1, 5]]
    for fs in prods:
        p = 1
        for f in fs:
            p *= f
        negs = sum(1 for f in fs if f < 0)
        expr = "(" + ")(".join(n(f) for f in fs) + ")"
        if p == 0:
            e = "One factor is 0, so the product is 0, whatever the other factors are."
        else:
            e = ("There %s %d negative factor%s. %s, so the product is %s. The sizes multiply to %s, so the answer is %s."
                 % ("is" if negs == 1 else "are", negs, "" if negs == 1 else "s",
                    "An even number of negatives gives a positive" if negs % 2 == 0 else "An odd number of negatives gives a negative",
                    sign_word(p), n(abs(p)), n(p)))
        s = sum(fs)
        its.append(mcq("Find %s." % B(expr), (n(p), p), nums([-p, s, -s, abs(p) + 1, 1, -1]), e))
    # powers of negatives
    for base, k in [(-2, 3), (-3, 2), (-1, 7), (-2, 4), (-5, 3), (-1, 10)]:
        v = base ** k
        e = ("(%s)<sup>%d</sup> means %d factors of %s. %d negative factors is %s, so the answer is %s."
             % (n(base), k, k, n(base), k, "even" if k % 2 == 0 else "odd", n(v)))
        its.append(mcq("Find %s." % B("(%s)<sup>%d</sup>" % (n(base), k)), (n(v), v),
                       nums([-v, base * k, -base * k, abs(base) + k]), e + " Not %s: that multiplies %s by %d." % (n(base * k), n(base), k)))
    # mixed operations
    exprs = [("−12 ÷ 3 × (−2)", 8, [-8, 2, -2]),
             ("−36 ÷ (−4) ÷ (−3)", -3, [3, -27, 27]),
             ("5 × (−6) ÷ (−10)", 3, [-3, -300, 30]),
             ("−8 × (−5) ÷ 4", 10, [-10, 160, -160]),
             ("(−3)(4) + (−6)", -18, [-6, 18, 6]),
             ("−20 ÷ 5 − (−3)", -1, [-7, 1, 7])]
    steps = {"−12 ÷ 3 × (−2)": "Work left to right: −12 ÷ 3 = −4, then −4 × (−2) = 8.",
             "−36 ÷ (−4) ÷ (−3)": "Left to right: −36 ÷ (−4) = 9, then 9 ÷ (−3) = −3.",
             "5 × (−6) ÷ (−10)": "Left to right: 5 × (−6) = −30, then −30 ÷ (−10) = 3.",
             "−8 × (−5) ÷ 4": "Left to right: −8 × (−5) = 40, then 40 ÷ 4 = 10.",
             "(−3)(4) + (−6)": "Multiply first: (−3)(4) = −12. Then −12 + (−6) = −18.",
             "−20 ÷ 5 − (−3)": "Divide first: −20 ÷ 5 = −4. Then −4 − (−3) = −4 + 3 = −1."}
    for ex, v, ws in exprs:
        its.append(mcq("Find %s." % B(ex), (n(v), v), nums(ws), steps[ex]))
    return {"title": "Many factors, powers and mixed operations", "items": its}


# ------------------------------------------------------------ set 4
def set_rational():
    its = []
    for a, b in [(F("-0.4"), 6), (F("-1.5"), F("-0.2")), (F("2.5"), F("-1.2")), (F("-0.3"), F("-0.7")), (F("-4.8"), F("0.5"))]:
        its.append(mul_item(a, b))
    for a, b in [(F("-7.2"), F("0.9")), (F("-1.8"), F("-0.3")), (F("6.4"), F("-0.8")), (F("-0.56"), 7)]:
        its.append(div_item(a, b))
    for a, b in [(F(-2, 3), F(3, 4)), (F(-3, 5), F(-5, 6)), (F(4, 9), F(-3, 8)), (F(-5, 2), F(-4, 15))]:
        its.append(mul_item(a, b, "f"))
    for a, b in [(F(-3, 4), F(1, 2)), (F(5, 6), F(-5, 12)), (F(-2, 3), F(-4, 9)), (F(-7, 8), 2)]:
        q = a / b
        expr = num(a, "f") + DIV + par(b, "f")
        rb = F(1) / F(b)
        rec = (MINUS if rb < 0 else "") + (fr(abs(rb.numerator), rb.denominator) if rb.denominator != 1 else str(abs(rb.numerator)))
        if rb < 0:
            rec = "(" + rec + ")"
        e = ("Multiply by the reciprocal: %s × %s. The signs are %s, so the answer is %s: %s."
             % (num(a, "f"), rec, "the same" if (a < 0) == (b < 0) else "different", sign_word(q), num(q, "f")))
        e += " Not %s: that multiplies without flipping the second fraction." % num(a * b, "f")
        its.append(mcq("Find %s." % B(expr), (num(q, "f"), q), nums([a * b, -q, -(a * b), 1 / q], "f"), e))
    # equivalent forms
    its.append(mcq("Which is <b>not</b> equal to %s?" % B(MINUS + "<span class='fr'><span class='fn'>3</span><span class='fd'>5</span></span>"),
                   ("<span class='fr'><span class='fn'>−3</span><span class='fd'>−5</span></span>", "x"),
                   [("<span class='fr'><span class='fn'>−3</span><span class='fd'>5</span></span>", "a"),
                    ("<span class='fr'><span class='fn'>3</span><span class='fd'>−5</span></span>", "b"),
                    ("−0.6", "c")],
                   "−3/5 = (−3)/5 = 3/(−5) = −0.6. But (−3)/(−5) has two negatives, so it is positive 3/5."))
    its.append(mcq("Find %s." % B("−2.5 × 4 × (−0.1)"), ("1", F(1)), nums([-1, F(-10), F(10)]),
                   "−2.5 × 4 = −10, then −10 × (−0.1) = 1. Two negative factors give a positive."))
    its.append(mcq("Find %s." % B("−0.25 × (−0.4)"), ("0.1", F("0.1")), nums([F("-0.1"), F("1"), F("-0.65")]),
                   "Two negatives give a positive. 0.25 × 0.4 = 0.1, so the answer is 0.1."))
    return {"title": "Decimals and fractions", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)

    def item(q, v, ws, e, unit="", money=False):
        def show(x):
            x = F(x)
            if money:
                return (MINUS if x < 0 else "") + "$" + num(abs(x))
            return num(x) + unit
        cands = [(show(w), F(w)) for w in ws + [v + 10, v - 10, -v * 2]]
        its.append(mcq(q, (show(v), F(v)), cands, e))

    for drop, hrs in [(3, 5), (2, 8), (4, 6)]:
        q = "The temperature falls %d°F every hour for %d hours. What is the total change in temperature?" % (drop, hrs)
        item(q, -drop * hrs, [drop * hrs, -drop - hrs, -drop], "A fall of %d°F each hour is −%d. −%d × %d = −%d°F." % (drop, drop, drop, hrs, drop * hrs), "°F")
    for cost, k in [(12, 4), (7, 9)]:
        name, he, his = P.next()
        q = "%s pays $%d for a lunch each day for %d days. What is the change in %s account balance?" % (name, cost, k, his)
        item(q, -cost * k, [cost * k, -cost - k, cost + k], "Each payment is −$%d. −%d × %d = −%d, so the balance changes by −$%d." % (cost, cost, k, cost * k, cost * k), money=True)
    for total, days in [(-42, 6), (-75, 5), (-96, 8)]:
        q = "A stock's price changed by a total of −$%d over %d days. It changed by the same amount each day. What was the change each day?" % (abs(total), days)
        item(q, F(total, days), [F(-total, days), total * days, total + days], "Divide the total change by the number of days: −%d ÷ %d = −%d." % (abs(total), days, abs(total) // days), money=True)
    for depth, mins in [(-90, 6), (-48, 4)]:
        rate = depth // mins
        q = "A diver descends to %d feet in %d minutes at a steady rate. What is the diver's change in elevation each minute?" % (depth, mins)
        q = q.replace("%d feet" % depth, num(depth) + " feet")
        item(q, rate, [-rate, depth * mins, depth + mins], "%s ÷ %d = %s feet per minute. Descending is a negative change." % (num(depth), mins, num(rate)), " ft")
    item("A football team loses 6 yards on each of 3 plays. What is the total change in yards?", -18,
         [18, -9, -3], "Each loss is −6. 3 × (−6) = −18 yards.", " yd")
    item("A water tank drains 15 gallons every hour. What was the change in the water amount over the last 4 hours?", -60,
         [60, -19, -11], "Draining is negative: 4 × (−15) = −60 gallons.", " gal")
    item("The temperature changed by −2.5°F each hour for 4 hours. What was the total change?", F(-10),
         [10, F("-6.5"), F("-1.5")], "−2.5 × 4 = −10°F.", "°F")
    item("A submarine at −240 m rises at the same rate for 3 minutes until it reaches −150 m. What is its change in depth each minute?", 30,
         [-30, -80, -130], "The total change is −150 − (−240) = 90 m. 90 ÷ 3 = 30 m per minute (rising, so positive).", " m")
    item("In a game you lose 4 points for each wrong answer. You get 7 wrong answers. What is the change in your score?", -28,
         [28, -11, -3], "7 × (−4) = −28 points.", " points")
    item("A gym's membership fell by 36 people over 9 months, the same amount each month. What was the change each month?", -4,
         [4, -27, -45], "−36 ÷ 9 = −4 people per month.", " people")
    item("The low temperatures for 4 days were −6°F, −3°F, 1°F and −4°F. What was the mean low temperature?", -3,
         [3, -12, F("-3.5")], "Add them: −6 + (−3) + 1 + (−4) = −12. Divide by 4: −12 ÷ 4 = −3°F.", "°F")
    item("A store loses $1,250 a month for 4 months. What is the total change in its money?", -5000,
         [5000, -1254, -1246], "4 × (−1,250) = −5,000, so the total change is −$5,000.", money=True)
    item("A hiker walks down a hill and the elevation changes by −0.75 km in 3 hours at a steady rate. What is the change each hour?", F("-0.25"),
         [F("0.25"), F("-2.25"), F("-3.75")], "−0.75 ÷ 3 = −0.25 km each hour.", " km")
    item("A video game character loses 15 points each time it is hit. It is hit 6 times. What is the change in its points?", -90,
         [90, -21, -9], "6 × (−15) = −90 points.", " points")
    return {"title": "Word problems", "items": its}


def body():
    rows = [["positive × positive", "+", "4 × 3 = 12"],
            ["negative × negative", "+", "(−4) × (−3) = 12"],
            ["positive × negative", "−", "4 × (−3) = −12"],
            ["negative × positive", "−", "(−4) × 3 = −12"]]
    return ("<h2>The sign rules</h2><p>Multiply or divide the sizes as usual. Then choose the sign: "
            "<b>same signs give a positive</b>, <b>different signs give a negative</b>. "
            "Division uses the same rules, because division undoes multiplication.</p>"
            + table(["Signs", "Answer", "Example"], rows)
            + "<h2>Why is negative × negative positive?</h2><p>Look at the pattern: (−4) × 2 = −8, (−4) × 1 = −4, (−4) × 0 = 0. "
            "Each step the answer goes up by 4. So (−4) × (−1) = 4 and (−4) × (−2) = 8.</p>"
            + "<h2>Many factors</h2><p>Count the negative factors. An <b>even</b> number of negatives gives a positive. "
            "An <b>odd</b> number gives a negative. (−2)<sup>3</sup> = (−2)(−2)(−2) = −8.</p>"
            + example("Find −56 ÷ (−8).", ["Different or same? Both are negative, so the answer is positive.", "56 ÷ 8 = 7."], "7")
            + example("Find −%s ÷ %s." % (fr(3, 4), fr(1, 2)), ["Multiply by the reciprocal: −%s × %s." % (fr(3, 4), fr(2, 1)), "Different signs, so the answer is negative: −%s = −1 %s." % (fr(6, 4), fr(1, 2))], "−1 " + fr(1, 2))
            + "<p>You can move the negative sign: −(<i>p</i> ÷ <i>q</i>) = (−<i>p</i>) ÷ <i>q</i> = <i>p</i> ÷ (−<i>q</i>). Dividing by 0 is undefined.</p>"
            + "<h2>Common mistakes</h2><ul><li>Using the adding rule: (−6) × (−4) is 24, not −24 or −10.</li>"
            "<li>Counting negatives wrongly: (−1)(−2)(−3) has three negatives, so it is −6.</li>"
            "<li>Forgetting to flip when dividing fractions: −%s ÷ %s is −1 %s, not −%s." % (fr(3, 4), fr(1, 2), fr(1, 2), fr(3, 8)) + "</li></ul>")


def main():
    sets = [set_multiply(), set_divide(), set_many(), set_rational(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "multiplying-and-dividing-integers",
        "title": "Multiplying and Dividing Integers",
        "seo_title": "Grade 7 Multiplying and Dividing Integers Worksheets: Sign Rules, Fractions and Word Problems",
        "short_title": "Multiplying and dividing integers",
        "domain": "The Number System",
        "standard_code": "7.NS.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/NS/A/2/",
        "standard_text": "Apply and extend previous understandings of multiplication and division and of fractions to multiply and divide rational numbers.",
        "meta_desc": "Free Grade 7 multiplying and dividing integers worksheets: the sign rules, many factors and powers of negatives, decimals and fractions, and real-world word problems. 100 practice questions with an answer key.",
        "key_big": "Same signs give a positive. Different signs give a negative.",
        "key_sub": "(−6) × (−4) = 24 and −56 ÷ 8 = −7. With many factors, count the negatives: even is positive, odd is negative.",
        "body_html": body(),
        "faq": [
            {"q": "What are the rules for multiplying integers?", "a": "Multiply the sizes. If the two signs are the same, the answer is positive: (−6) × (−4) = 24. If they are different, the answer is negative: 6 × (−4) = −24."},
            {"q": "Are the division rules the same?", "a": "Yes. Same signs give a positive and different signs give a negative: −56 ÷ (−8) = 7 and −56 ÷ 8 = −7."},
            {"q": "Why is a negative times a negative positive?", "a": "Follow the pattern (−4) × 2 = −8, (−4) × 1 = −4, (−4) × 0 = 0. The answer goes up by 4 each time, so (−4) × (−1) = 4."},
            {"q": "How do I find the sign with many factors?", "a": "Count the negative factors. An even count gives a positive answer and an odd count gives a negative answer. If any factor is 0, the product is 0."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 2,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
