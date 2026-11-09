# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Adding and Subtracting Integers and Rational Numbers (7.NS.A.1)
  python tools/gen_us_math_g7_add_subtract_integers.py
Wrong answers come from real mistakes: the wrong sign, adding the sizes when the signs differ,
subtracting the sizes when the signs are the same, forgetting to change subtraction into adding
the opposite (6 − (−9) -> −3), subtracting in the wrong order, and moving the wrong way on a number line.
"""
import random
from fractions import Fraction as F
from ws_common import (num, par, nums, mcq, balance, People, B, fig, figure, number_line, table, example,
                       write_unit, GREEN, RED, BLUE, MINUS)

R = random.Random(70101)
UPDATED = "2026-11-09"


def n(v, st="d"):
    return num(v, st)


def add_wrongs(a, b):
    """Mistakes for a + b."""
    a, b = F(a), F(b)
    s = a + b
    out = [-s]
    if (a < 0) != (b < 0):                       # different signs
        big = a if abs(a) >= abs(b) else b
        out += [(1 if big > 0 else -1) * (abs(a) + abs(b)), -(1 if big > 0 else -1) * (abs(a) + abs(b))]
    else:                                         # same sign
        out += [(1 if a > 0 else -1) * abs(abs(a) - abs(b)), -(1 if a > 0 else -1) * abs(abs(a) - abs(b))]
    out += [a - b, b - a, abs(a) + abs(b), -(abs(a) + abs(b)), s - 10, s + 10]
    return out


def sub_wrongs(a, b):
    """Mistakes for a − b."""
    a, b = F(a), F(b)
    d = a - b
    return [a + b, -d, b - a, -(a + b), abs(a) - abs(b), abs(a) + abs(b), d - 10, d + 10]


def why_add(a, b, st="d"):
    a, b = F(a), F(b)
    n = lambda v: num(v, st)
    if (a < 0) == (b < 0):
        return ("The signs are the same, so add the sizes %s + %s = %s and keep the sign: %s."
                % (n(abs(a)), n(abs(b)), n(abs(a) + abs(b)), n(a + b)))
    big = a if abs(a) >= abs(b) else b
    return ("The signs are different, so subtract the sizes %s − %s = %s and use the sign of %s, the number farther from 0: %s."
            % (n(max(abs(a), abs(b))), n(min(abs(a), abs(b))), n(abs(abs(a) - abs(b))), n(big), n(a + b)))


def add_item(a, b, st="d", ask="Find %s.", note=""):
    a, b = F(a), F(b)
    s = a + b
    expr = "%s + %s" % (num(a, st), par(b, st))
    ws = add_wrongs(a, b)
    first = next(w for w in ws if w != s)
    e = why_add(a, b, st) + (" " + note if note else "") + " Not %s: check the sign." % num(first, st)
    return mcq(ask % B(expr), (num(s, st), s), nums(ws, st), e)


def sub_item(a, b, st="d", ask="Find %s."):
    a, b = F(a), F(b)
    d = a - b
    expr = "%s − %s" % (num(a, st), par(b, st))
    ws = sub_wrongs(a, b)
    e = ("Subtracting is adding the opposite: %s + %s. %s"
         % (num(a, st), par(-b, st), why_add(a, -b, st)))
    if a + b != d:
        e += " Not %s: that adds %s instead of subtracting it." % (num(a + b, st), num(b, st))
    return mcq(ask % B(expr), (num(d, st), d), nums(ws, st), e)


# ------------------------------------------------------------ set 1
def set_number_line():
    its = []
    # a) read a jump on the number line
    for a, b in [(-3, 5), (2, -6), (-1, -4), (-6, 8), (4, -9), (-2, 7)]:
        s = a + b
        svg = number_line(-10, 10, jumps=[(a, s, GREEN)], dots=[(a, BLUE)],
                          label="number line: start at %s and move %d %s" % (n(a), abs(b), "right" if b > 0 else "left"))
        e = ("Start at %s. Moving %s %d is adding %s, so you land on %s." %
             (n(a), "right" if b > 0 else "left", abs(b), n(b), n(s)))
        its.append(mcq(fig(svg) + "Which sum does the number line show?",
                       ("%s + %s = %s" % (n(a), par(b), n(s)), "ok"),
                       [("%s + %s = %s" % (n(a), par(-b), n(a - b)), "w1"),
                        ("%s + %s = %s" % (n(-a), par(b), n(-a + b)), "w3"),
                        ("%s + %s = %s" % (n(a), par(b), n(-s if s else s + 2)), "w4"),
                        ("%s + %s = %s" % (n(a), par(b), n(s + (1 if b > 0 else -1))), "w5")], e))
    # b) start and move, no picture
    for a, d, way in [(-5, 8, "right"), (3, 7, "left"), (-2, 6, "left"), (-9, 4, "right"), (6, 10, "left"), (-4, 4, "right")]:
        b = d if way == "right" else -d
        s = a + b
        e = ("Moving %s means %s %d. %s + %s = %s." % (way, "adding" if way == "right" else "subtracting", d, n(a), par(b), n(s)))
        its.append(mcq("On a number line you start at %s and move %d units to the %s. Where do you land?" % (B(n(a)), d, way),
                       (n(s), s), nums([a - b, -s, -a + b, abs(a) + d, a, s + 1]), e))
    # c) opposites and zero pairs (additive inverses)
    for v in [-8, 15, F("-3.5")]:
        e = "The opposite of %s is %s: it is the same distance from 0 on the other side, and %s + %s = 0." % (n(v), n(-v), n(v), par(-v))
        its.append(mcq("What is the opposite of %s?" % B(n(v)), (n(-v), -v), [(n(v), F(v))] + nums([1 / F(v), -1 / F(v), 0], "f"),
                       e + " Not %s: that is the reciprocal, not the opposite." % num(1 / F(v), "f")))
    for v in [-12, 27]:
        e = "A number and its opposite are a zero pair: %s + %s = 0." % (n(v), par(-v))
        its.append(mcq("Find %s." % B("%s + %s" % (n(v), par(-v))), ("0", 0), nums([2 * v, -2 * v, v]), e))
    its.append(mcq("Which number makes %s true?" % B("? + 9 = 0"), (MINUS + "9", -9), nums([9, 0, 18]), "−9 + 9 = 0: a number plus its opposite is 0. Not 9: 9 + 9 = 18."))
    e = "−4 + 4 = 0, so the 4 positive and 4 negative tiles cancel. That leaves 2 negative tiles: −2."
    its.append(mcq("A model has 6 negative tiles and 4 positive tiles. A positive and a negative tile make a zero pair. What number does the model show?",
                   (MINUS + "2", -2), nums([2, -10, 10]), e))
    its.append(mcq("What is the opposite of the opposite of %s?" % B(MINUS + "5"), (MINUS + "5", -5), nums([5, 0, 10]),
                   "The opposite of −5 is 5, and the opposite of 5 is −5. Taking the opposite twice brings you back: −(−(−5)) = −5."))
    return {"title": "Opposites, zero pairs and the number line", "items": its}


# ------------------------------------------------------------ set 2
def set_add():
    its = []
    pairs = [(7, -3), (-7, 3), (-5, -8), (-14, 9), (12, -20), (-6, -6), (-23, 17), (35, -18),
             (-29, -16), (-41, 41), (18, -45), (-37, 52), (-64, -27), (-8, 15), (48, -73), (-125, 60),
             (-17, -38), (90, -136), (-56, 28), (-250, 175)]
    for a, b in pairs:
        if a + b == 0:
            its.append(mcq("Find %s." % B("%s + %s" % (n(a), par(b))), ("0", 0), nums([a * 2, -a * 2, b]),
                           "%s and %s are opposites, so the sum is 0." % (n(a), n(b))))
        else:
            its.append(add_item(a, b))
    return {"title": "Add integers: same signs and different signs", "items": its}


# ------------------------------------------------------------ set 3
def set_sub():
    its = []
    # rewrite as adding the opposite
    for a, b in [(6, -9), (-4, 7), (-10, -3), (5, 12)]:
        e = "Subtracting a number is the same as adding its opposite, so %s − %s = %s + %s." % (n(a), par(b), n(a), par(-b))
        its.append(mcq("Which addition has the same value as %s?" % B("%s − %s" % (n(a), par(b))),
                       ("%s + %s" % (n(a), par(-b)), "ok"),
                       [("%s + %s" % (n(a), par(b)), "w1"), ("%s + %s" % (n(-a), par(-b)), "w2"),
                        ("%s − %s" % (n(b), par(a)), "w3"), ("%s + %s" % (n(-a), par(b)), "w4")], e))
    for a, b in [(3, -8), (-5, 4), (-9, -2), (4, 11), (-12, -20), (15, -15), (-30, 18), (-7, -19),
                 (24, 39), (-45, -60), (52, -38), (-81, 46), (-100, -35), (-64, 64), (19, -76), (-140, -95)]:
        its.append(sub_item(a, b))
    return {"title": "Subtract integers: add the opposite", "items": its}


# ------------------------------------------------------------ set 4
def set_rational():
    its = []
    # distance between two numbers = |a − b|
    for a, b in [(-7, 5), (-12, -3), (F("-2.5"), F("4.5")), (-15, 9)]:
        d = abs(F(a) - F(b))
        e = "Distance is the absolute value of the difference: |%s − %s| = |%s| = %s. Distance is never negative." % (
            n(b), par(a), n(F(b) - F(a)), n(d))
        its.append(mcq("What is the distance between %s and %s on a number line?" % (B(n(a)), B(n(b))),
                       (n(d), d), nums([abs(abs(F(a)) - abs(F(b))), -d, abs(F(a)), abs(F(b)) + 1]), e))
    # decimals
    for a, b in [(F("-2.5"), F("4.1")), (F("3.6"), F("-7.2")), (F("-1.75"), F("-0.5")), (F("-6.4"), F("2.9"))]:
        its.append(add_item(a, b))
    for a, b in [(F("-4.3"), F("1.8")), (F("2.25"), F("-3.5")), (F("-0.6"), F("-1.4"))]:
        its.append(sub_item(a, b))
    # fractions
    for a, b in [(F(-3, 4), F(1, 2)), (F(2, 3), F(-5, 6)), (F(-1, 2), F(-1, 3)), (F(-5, 2), F(7, 4))]:
        its.append(add_item(a, b, "f", note="Use a common denominator first."))
    for a, b in [(F(1, 4), F(-3, 8)), (F(-2, 5), F(3, 10)), (F(-7, 6), F(-1, 3)), (F(-3, 2), F(1, 4)), (F(5, 6), F(-1, 3))]:
        its.append(sub_item(a, b, "f"))
    return {"title": "Distance, decimals and fractions", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)

    def item(q, val, ws, e, unit=""):
        its.append(mcq(q, (n(val) + unit, F(val)), nums(list(ws) + [val - 10, val + 10, val + 1], unit=unit), e))

    # temperature
    for t0, ch in [(-6, 11), (4, -9), (-3, -8), (-12, 15)]:
        t1 = t0 + ch
        q = ("At 6 a.m. the temperature was %s°F. By noon it had %s %d degrees. What was the temperature at noon?"
             % (n(t0), "risen" if ch > 0 else "fallen", abs(ch)))
        e = "%s means %s: %s + %s = %s°F." % ("Rising" if ch > 0 else "Falling", "add" if ch > 0 else "add a negative",
                                              n(t0), par(ch), n(t1))
        item(q, t1, [t0 - ch, -t1, abs(t0) + abs(ch), -(abs(t0) + abs(ch))], e, "°F")
    # temperature difference
    for hi, lo in [(8, -5), (-2, -17), (14, -9)]:
        d = hi - lo
        q = "The high temperature was %s°F and the low was %s°F. How many degrees warmer was the high than the low?" % (n(hi), n(lo))
        e = "Subtract: %s − %s = %s + %s = %d degrees." % (n(hi), par(lo), n(hi), par(-lo), d)
        item(q, d, [hi + lo, -d, abs(abs(hi) - abs(lo)) if abs(abs(hi) - abs(lo)) != d else d + 2], e, " degrees")
    # elevation
    for a, ch in [(-120, 45), (-35, -60), (-15, -70)]:
        b = a + ch
        where = lambda v: "%d feet %s sea level" % (abs(v), "below" if v < 0 else "above")
        q = ("A diver is at %s feet (%s). %s %s %d feet. What is the diver's new elevation?"
             % (n(a), where(a), "She" if ch > 0 else "She", "rises" if ch > 0 else "goes down", abs(ch)))
        e = "%s + %s = %s feet, which is %s." % (n(a), par(ch), n(b), where(b) if b else "sea level")
        item(q, b, [a - ch, -b, abs(a) + abs(ch)], e, " ft")
    # elevation difference
    q = ("A mountain top is 2,350 feet above sea level. The bottom of a nearby lake is 140 feet below sea level. "
         "How far is it from the lake bottom up to the mountain top?")
    item(q, 2490, [2210, -2490, 2350], "Subtract the elevations: 2,350 − (−140) = 2,350 + 140 = 2,490 feet. Not 2,210: that subtracts 140 instead of adding it.", " ft")
    # bank account
    name, he, his = P.next()
    q = "%s's account has $35. %s spends $52 on a game. What is the balance now?" % (name, he.capitalize())
    its.append(mcq(q, (MINUS + "$17", -17), [("$17", 17), ("$87", 87), (MINUS + "$87", -87)],
                   "35 + (−52) = −17. The balance is −$17: %s owes $17. Not $17: the sign shows the account is below 0." % he))
    name, he, his = P.next()
    q = "%s's account balance is −$24. %s deposits $60. What is the new balance?" % (name, he.capitalize())
    its.append(mcq(q, ("$36", 36), [(MINUS + "$36", -36), ("$84", 84), (MINUS + "$84", -84)],
                   "−24 + 60 = 36, so the balance is $36. Not $84: the signs are different, so subtract the sizes."))
    # football / golf
    q = "A football team gains 7 yards, loses 12 yards, then gains 3 yards. What is the total change?"
    item(q, -2, [22, 2, -22], "7 + (−12) + 3 = −5 + 3 = −2. The team lost 2 yards in all.", " yd")
    q = "In golf, a score below par is negative. Ana's scores for four holes are −1, +2, −2 and −1. What is her total?"
    item(q, -2, [2, -6, 6], "−1 + 2 + (−2) + (−1) = −2, so she is 2 under par. Not −6: +2 is positive.")
    # floors
    q = "An elevator starts on floor 4. It goes down 7 floors to a parking level. Which floor is it on now?"
    item(q, -3, [11, 3, -11], "4 + (−7) = −3: three floors below ground level.")
    q = "A submarine at −250 m rises 85 m, then dives 40 m. Where is it now?"
    item(q, -205, [-125, -295, -375], "−250 + 85 + (−40) = −165 + (−40) = −205 m. Not −295: it rose 85 m first.", " m")
    q = "The temperature at the North Pole was −31°F at night and −18°F during the day. How much did it rise?"
    item(q, 13, [49, -13, -49], "Change = day − night = −18 − (−31) = −18 + 31 = 13 degrees. Not 49: that adds the sizes.", " degrees")
    q = "A small shop had a profit of −$1,200 in March (a loss) and a profit of $2,750 in April. What was the total profit for the two months?"
    its.append(mcq(q, ("$1,550", 1550), [(MINUS + "$1,550", -1550), ("$3,950", 3950), (MINUS + "$3,950", -3950)],
                   "−1,200 + 2,750 = 1,550, so the total profit is $1,550. Different signs, so subtract the sizes: 2,750 − 1,200 = 1,550, and 2,750 is farther from 0."))
    q = "Badwater Basin in Death Valley is at −282 feet. A hiker climbs 1,000 feet up from there. What elevation does the hiker reach?"
    item(q, 718, [1282, -718, -1282], "−282 + 1,000 = 718 feet above sea level. Not 1,282: the signs are different, so subtract the sizes.", " ft")
    return {"title": "Word problems: temperature, elevation and money", "items": its}


def body():
    nl = number_line(-8, 6, jumps=[(-5, 2, GREEN)], dots=[(-5, BLUE)], label="number line: start at −5 and move 7 right to 2")
    nl2 = number_line(-8, 6, jumps=[(3, -4, RED)], dots=[(3, BLUE)], label="number line: start at 3 and move 7 left to −4")
    rows = [["7 + (−3)", "different", "7 − 3 = 4, sign of 7 (+)", "4"],
            ["−7 + 3", "different", "7 − 3 = 4, sign of −7 (−)", "−4"],
            ["−5 + (−8)", "same (−)", "5 + 8 = 13, keep −", "−13"],
            ["6 − (−9)", "subtracting", "6 + 9", "15"],
            ["−4 − 7", "subtracting", "−4 + (−7)", "−11"]]
    return ("<h2>Adding on a number line</h2><p>Adding a positive number moves <b>right</b>. Adding a negative number moves <b>left</b>.</p>"
            + figure(nl, "−5 + 7 = 2. Start at −5 and move 7 to the right.")
            + figure(nl2, "3 + (−7) = −4. Start at 3 and move 7 to the left.")
            + "<h2>The two rules for adding</h2><p><b>Same signs:</b> add the sizes and keep the sign. "
            "<b>Different signs:</b> subtract the sizes and use the sign of the number farther from 0. "
            "A number plus its opposite is 0, like −9 + 9 = 0.</p>"
            + "<h2>Subtracting: add the opposite</h2><p>To subtract, change it to adding the opposite, then use the rules above: "
            "6 − (−9) = 6 + 9 = 15. The distance between two numbers is the absolute value of their difference: "
            "the distance from −7 to 5 is |5 − (−7)| = 12.</p>"
            + table(["Problem", "Signs", "Think", "Answer"], rows)
            + example("Find −14 + 9.", ["The signs are different, so subtract the sizes: 14 − 9 = 5.",
                                         "−14 is farther from 0, so the answer is negative."], "−5")
            + example("Find −3 − (−10).", ["Add the opposite: −3 + 10.", "Different signs: 10 − 3 = 7, and 10 is farther from 0."], "7")
            + "<h2>Common mistakes</h2><ul><li>Adding the sizes when the signs are different: −14 + 9 is −5, not −23.</li>"
            "<li>Forgetting to change the sign when subtracting a negative: 6 − (−9) is 15, not −3.</li>"
            "<li>Subtracting in the wrong order: 4 − 11 is −7, not 7.</li></ul>")


def main():
    sets = [set_number_line(), set_add(), set_sub(), set_rational(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "adding-and-subtracting-integers",
        "title": "Adding and Subtracting Integers",
        "seo_title": "Grade 7 Adding and Subtracting Integers Worksheets: Number Lines, Rules and Word Problems",
        "short_title": "Adding and subtracting integers",
        "domain": "The Number System",
        "standard_code": "7.NS.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/NS/A/1/",
        "standard_text": "Apply and extend previous understandings of addition and subtraction to add and subtract rational numbers; represent addition and subtraction on a horizontal or vertical number line diagram.",
        "meta_desc": "Free Grade 7 adding and subtracting integers worksheets: number lines, zero pairs, the rules for same and different signs, subtracting by adding the opposite, distance, decimals and fractions, and word problems. 100 practice questions with an answer key.",
        "key_big": "Same signs: add and keep the sign. Different signs: subtract and use the sign of the number farther from 0.",
        "key_sub": "To subtract, add the opposite: 6 − (−9) = 6 + 9 = 15. A number plus its opposite is 0.",
        "body_html": body(),
        "faq": [
            {"q": "What are the rules for adding integers?", "a": "If the signs are the same, add the sizes and keep the sign: −5 + (−8) = −13. If the signs are different, subtract the sizes and use the sign of the number farther from 0: −14 + 9 = −5."},
            {"q": "How do you subtract a negative number?", "a": "Subtracting a number is the same as adding its opposite, so subtracting a negative becomes adding a positive: 6 − (−9) = 6 + 9 = 15."},
            {"q": "How do you find the distance between two numbers?", "a": "Subtract them and take the absolute value. The distance between −7 and 5 is |5 − (−7)| = 12. A distance is never negative."},
            {"q": "Do the same rules work for decimals and fractions?", "a": "Yes. −2.5 + 4.1 = 1.6 and −3/4 + 1/2 = −1/4. For fractions, find a common denominator first."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 1,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
