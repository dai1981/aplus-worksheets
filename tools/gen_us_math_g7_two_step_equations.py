# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Two-Step Equations (7.EE.B.4a)
  python tools/gen_us_math_g7_two_step_equations.py
Equations px + q = r and p(x + q) = r with integers, decimals and fractions.
Wrong answers come from real mistakes: doing the opposite operation on the wrong side (adding q
instead of subtracting it), dividing before subtracting, forgetting the second step, losing a
negative sign, and only multiplying the first term when distributing.
"""
import random
from fractions import Fraction as F
from ws_common import (num, par, nums, mcq, balance, People, B, table, example, write_unit, MINUS, X, fr)

R = random.Random(70301)
UPDATED = "2026-11-09"


def n(v, st="d"):
    return num(v, st)


def term(p, st="d"):
    """p x with 1 and −1 written as x and −x."""
    p = F(p)
    if p == 1:
        return X
    if p == -1:
        return MINUS + X
    return num(p, st) + X


def plus(q, st="d"):
    q = F(q)
    return (" + " + num(q, st)) if q >= 0 else (" − " + num(-q, st))


def eq1(p, q, r, st="d"):
    return "%s%s = %s" % (term(p, st), plus(q, st), num(r, st))


def solve1(p, q, x, st="d", ask="Solve %s."):
    """px + q = r with answer x."""
    p, q, x = F(p), F(q), F(x)
    r = p * x + q
    e_txt = eq1(p, q, r, st)
    step1 = ("Subtract %s from both sides" % num(q, st)) if q >= 0 else ("Add %s to both sides" % num(-q, st))
    e = ("%s: %s = %s. Then divide both sides by %s: %s = %s. Check: %s × %s%s = %s."
         % (step1, term(p, st), num(r - q, st), num(p, st), X, num(x, st), num(p, st), par(x, st), plus(q, st), num(r, st)))
    ws = [(r + q) / p, r / p - q, r - q, -x, (r - q) * p, (r + q) / -p if p else None]
    note = ("that adds %s instead of undoing it." % num(q, st)) if q >= 0 else ("that subtracts %s instead of undoing it." % num(-q, st))
    ws += [r - q, -(r - q), r + q, x + q]
    it = mcq(ask % B(e_txt), (num(x, st), x), nums(ws, st) + nums(ws, "f"), e)
    return add_note(it, (r + q) / p, st, note)


def add_note(it, w, st, note):
    """Explain the mistake only when that wrong answer is one of the choices."""
    for t in (num(w, st), num(w, "f")):
        if t is not None and t in it["c"][1:]:
            it["e"] += " Not %s: %s" % (t, note)
            break
    return it


def solve_div(p, q, x, ask="Solve %s."):
    """x/p + q = r."""
    p, q, x = F(p), F(q), F(x)
    r = x / p + q
    lhs = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (X, num(p))
    txt = "%s%s = %s" % (lhs, plus(q), num(r))
    step1 = ("Subtract %s from both sides" % num(q)) if q >= 0 else ("Add %s to both sides" % num(-q))
    e = ("%s: %s ÷ %s = %s. Then multiply both sides by %s: %s = %s."
         % (step1, X, par(p), num(r - q), par(p), X, num(x)))
    ws = [(r - q) / p, (r + q) * p, r * p - q, -x, r - q]
    e += " Not %s: that divides by %s instead of multiplying." % (num((r - q) / p, "f"), par(p))
    return mcq(ask % B(txt), (num(x), x), nums(ws, "f"), e)


def solve_par(p, q, x, st="d", ask="Solve %s."):
    """p(x + q) = r."""
    p, q, x = F(p), F(q), F(x)
    r = p * (x + q)
    txt = "%s(%s%s) = %s" % (num(p, st) if p != -1 else MINUS, X, plus(q, st), num(r, st))
    step2 = ("subtract %s" % num(q, st)) if q >= 0 else ("add %s" % num(-q, st))
    e = ("Divide both sides by %s: %s%s = %s. Then %s: %s = %s. (Or distribute first: %s%s = %s.)"
         % (num(p, st), X, plus(q, st), num(r / p, st), step2, X, num(x, st), term(p, st), plus(p * q, st), num(r, st)))
    wrong_dist = (r - q) / p          # only multiplied x by p
    ws = [wrong_dist, r / p + q, r - q, -x, (r - p * q) * p]
    ws += [r, -r, x + q]
    it = mcq(ask % B(txt), (num(x, st), x), nums(ws, st) + nums(ws, "f"), e)
    return add_note(it, wrong_dist, st, "when you distribute, multiply %s by both %s and %s." % (num(p, st), X, num(q, st)))


# ------------------------------------------------------------ set 1
def set_steps():
    its = []
    firsts = [(3, 5, 20), (4, -7, 13), (-2, 9, 1), (5, 12, -3)]
    for p, q, r in firsts:
        good = ("Subtract %s from both sides" % n(q)) if q > 0 else ("Add %s to both sides" % n(-q))
        badw = ("Add %s to both sides" % n(q)) if q > 0 else ("Subtract %s from both sides" % n(-q))
        its.append(mcq("What is a good first step to solve %s?" % B(eq1(p, q, r)), (good + ".", "g"),
                       [(badw + ".", "w"), ("Multiply both sides by %s." % n(p), "m"), ("Subtract %s from both sides." % n(abs(p)), "s")],
                       "Undo the adding or subtracting first, then undo the multiplying. In %s the %s is %s, so %s first."
                       % (eq1(p, q, r), "constant", n(q), good.lower())))
    # after the first step
    for p, q, x in [(6, 4, 3), (7, -5, 2), (-3, 8, 4)]:
        r = p * x + q
        its.append(mcq("After the first step of solving %s, which equation do you get?" % B(eq1(p, q, r)),
                       ("%s = %s" % (term(p), n(r - q)), r - q),
                       [("%s = %s" % (term(p), n(r + q)), r + q), ("%s = %s" % (X, n(r - q)), "x"),
                        ("%s = %s" % (term(p), n(r)), "r")],
                       "Undo %s on both sides: %s = %s %s %s = %s." % (plus(q).strip(), term(p), n(r), "−" if q > 0 else "+", n(abs(q)), n(r - q))))
    # check a solution
    for p, q, x, test in [(2, 7, 5, 5), (3, -4, 6, 4), (-4, 10, 3, -3), (5, 2, -2, -2), (6, -9, 4, 3), (-2, -5, -4, -4)]:
        r = p * x + q
        val = p * test + q
        ok = val == r
        e = "Put %s in for %s: %s × %s%s = %s%s%s." % (n(test), X, n(p), par(test), plus(q), n(val),
                                                     " = " if ok else " ≠ ", n(r))
        e += " So it %s a solution." % ("is" if ok else "is not")
        its.append(mcq("Is %s a solution of %s?" % (B("%s = %s" % (X, n(test))), B(eq1(p, q, r))),
                       ("Yes" if ok else "No", ok),
                       [("No" if ok else "Yes", not ok), ("Only if %s is positive" % X, "p"), ("It cannot be checked", "c")], e))
    # which value solves
    for p, q, x in [(4, 3, 5), (3, -8, 7), (-5, 6, 2), (2, 11, -3), (8, -6, -1), (-3, -7, -5), (9, -4, 1)]:
        its.append(solve1(p, q, x, ask="Which value of <i>x</i> makes %s true?"))
    return {"title": "Two steps: undo in reverse order", "items": its}


# ------------------------------------------------------------ set 2
def set_basic():
    its = []
    for p, q, x in [(2, 5, 8), (3, 7, 6), (5, -4, 9), (4, -11, 7), (6, 13, 5), (7, -2, 4), (8, 9, 3), (9, -15, 6),
                    (3, 14, 12), (11, -6, 3), (12, 8, 4), (5, 23, 11), (4, -30, 15), (6, -19, 8), (10, 35, 7),
                    (15, -40, 4), (2, 17, 24), (7, 28, 9), (13, -9, 5), (20, -60, 8)]:
        its.append(solve1(p, q, x))
    return {"title": "Solve px + q = r", "items": its}


# ------------------------------------------------------------ set 3
def set_negative():
    its = []
    for p, q, x in [(-3, 4, 5), (-2, -7, 6), (4, 9, -3), (5, -2, -4), (-6, -8, -3), (-7, 15, 2), (3, 20, -5),
                    (-4, -9, -6), (8, 30, -2), (-5, 12, -1), (-1, 6, 9), (-9, -4, 2)]:
        its.append(solve1(p, q, x))
    for p, q, x in [(3, 4, 18), (4, -2, 20), (5, 7, -10), (2, 3, -8), (6, -5, -12), (2, 9, -14), (3, -1, -15), (7, 2, 21)]:
        its.append(solve_div(p, q, x))
    return {"title": "Negative numbers and x ÷ p", "items": its}


# ------------------------------------------------------------ set 4
def set_mixed():
    its = []
    for p, q, x in [(3, 2, 5), (4, -6, 9), (-2, 5, 3), (5, 3, -7), (6, -1, -2), (-3, -4, 1), (2, 8, 4), (7, -3, 10)]:
        its.append(solve_par(p, q, x))
    for p, q, x in [(F("0.5"), 3, 14), (F("1.5"), F("-2.5"), 5), (F("2.4"), F("1.2"), 3), (F("-0.2"), 4, 15), (4, F("2.6"), F("1.1")),
                    (F("0.25"), F("-1.5"), 10)]:
        its.append(solve1(p, q, x))
    for p, q, x in [(F(1, 2), 3, 8), (F(2, 3), -4, 9), (F(3, 4), F(1, 2), 2), (F(-1, 3), 5, 6), (3, F(1, 4), F(5, 4)), (F(2, 5), -1, 10)]:
        its.append(solve1(p, q, x, "f"))
    return {"title": "Parentheses, decimals and fractions", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)

    def item(q, x, ws, e, unit=""):
        cands = [(num(F(w)) + unit, F(w)) for w in ws + [x + 1, x - 1, x * 2] if num(F(w)) is not None]
        its.append(mcq(q, (num(F(x)) + unit, F(x)), cands, e))

    name, he, his = P.next()
    item("%s pays a $15 sign-up fee and $8 for each class. %s spends $87 in all. How many classes did %s take?" % (name, cap(he), he),
         9, [12, F(87 + 15, 8)], "8c + 15 = 87, so 8c = 72 and c = 9 classes.", " classes")
    name, he, his = P.next()
    item("A taxi charges $3 plus $2 per mile. %s's ride costs $27. How many miles was the ride?" % name,
         12, [15, 24], "2m + 3 = 27, so 2m = 24 and m = 12 miles.", " mi")
    item("A phone plan costs $25 a month plus $0.10 for each text. One month's bill is $31.50. How many texts were sent?",
         65, [565, 315], "0.10t + 25 = 31.50, so 0.10t = 6.50 and t = 65 texts.", " texts")
    item("The perimeter of a rectangle is 46 cm. Its length is 15 cm. What is its width?", 8, [16, 31, F(46, 2) - 15 + 15],
         "2(15) + 2w = 46, so 30 + 2w = 46, 2w = 16 and w = 8 cm.", " cm")
    item("A rectangle has width 7 in. and perimeter 50 in. What is its length?", 18, [36, 43],
         "2ℓ + 2(7) = 50, so 2ℓ + 14 = 50, 2ℓ = 36 and ℓ = 18 in.", " in.")
    name, he, his = P.next()
    item("%s has $120 and saves $15 each week. After how many weeks will %s have $255?" % (name, he), 9, [25, 8, 135],
         "15w + 120 = 255, so 15w = 135 and w = 9 weeks.", " weeks")
    item("Three friends share the cost of a pizza equally. Each also pays $2 for a drink. Each friend pays $7 in all. How much did the pizza cost?",
         15, [3, 27, 5], "p/3 + 2 = 7, so p/3 = 5 and p = 15 dollars.", " dollars")
    item("The temperature is −4°F and rises 3°F each hour. After how many hours will it be 14°F?", 6, [F(10, 3), 18, -6],
         "3h + (−4) = 14, so 3h = 18 and h = 6 hours.", " hours")
    item("A diver at −10 feet goes down 6 feet each minute. After how many minutes is she at −58 feet?", 8, [-8, F(68, 6) + 0, 48],
         "−6m − 10 = −58, so −6m = −48 and m = 8 minutes.", " min")
    item("A gym charges $40 to join and $25 a month. Ana has paid $240 in all. How many months has she been a member?",
         8, [F(280, 25), 200, 10], "25m + 40 = 240, so 25m = 200 and m = 8 months.", " months")
    item("A tank has 500 gallons of water. It drains 35 gallons each hour. After how many hours will 185 gallons be left?",
         9, [F(685, 35), 315, -9], "500 − 35h = 185, so −35h = −315 and h = 9 hours.", " hours")
    name, he, his = P.next()
    item("%s bought 4 notebooks and a $6 pen. %s spent $26. How much was each notebook?" % (name, cap(he)), 5, [8, 20, 4],
         "4n + 6 = 26, so 4n = 20 and n = 5 dollars.", " dollars")
    item("Twice a number, plus 9, is 35. What is the number?", 13, [22, 26, F(35, 2) - 9], "2n + 9 = 35, so 2n = 26 and n = 13.")
    item("A number divided by 4, minus 3, is 5. What is the number?", 32, [2, 8, 20], "n/4 − 3 = 5, so n/4 = 8 and n = 32.")
    item("Five less than 3 times a number is 31. What is the number?", 12, [F(26, 3), 36, F(31, 3) + 5],
         "3n − 5 = 31, so 3n = 36 and n = 12.")
    item("A concert hall has 30 rows with the same number of seats, plus 24 box seats. It has 924 seats in all. How many seats are in each row?",
         30, [F(948, 30), 900, 40], "30s + 24 = 924, so 30s = 900 and s = 30 seats.", " seats")
    item("Each of 6 students gets the same number of stickers. The teacher keeps 14. There were 98 stickers. How many did each student get?",
         14, [F(112, 6), 84, 18], "6s + 14 = 98, so 6s = 84 and s = 14 stickers.", " stickers")
    item("A plumber charges $65 for the visit plus $48 per hour. The bill is $257. How many hours did the plumber work?",
         4, [F(322, 48), 192, 5], "48h + 65 = 257, so 48h = 192 and h = 4 hours.", " hours")
    item("A school buys 3 boxes of markers at the same price and gets $5 off. It pays $37. What is the price of one box?",
         14, [F(32, 3), 42, 12], "3b − 5 = 37, so 3b = 42 and b = 14 dollars.", " dollars")
    item("The sum of two numbers is 45. One number is 3 more than twice the other. What is the smaller number?",
         14, [21, 31, 15], "n + (2n + 3) = 45, so 3n + 3 = 45, 3n = 42 and n = 14. The other number is 31.")
    return {"title": "Word problems: write and solve", "items": its}


def cap(s):
    return s[0].upper() + s[1:]


def body():
    rows = [["3" + X + " + 5 = 20", "subtract 5", "3" + X + " = 15", "divide by 3", X + " = 5"],
            ["4" + X + " − 7 = 13", "add 7", "4" + X + " = 20", "divide by 4", X + " = 5"],
            [MINUS + "2" + X + " + 9 = 1", "subtract 9", MINUS + "2" + X + " = −8", "divide by −2", X + " = 4"],
            ["2(" + X + " + 3) = 16", "divide by 2", X + " + 3 = 8", "subtract 3", X + " = 5"]]
    return ("<h2>Undo in reverse order</h2><p>In 3" + X + " + 5, you multiply by 3 first, then add 5. "
            "To solve, undo these steps backwards: <b>first undo the + 5, then undo the × 3</b>. "
            "Do the same thing to both sides so the equation stays balanced.</p>"
            + table(["Equation", "Step 1", "Result", "Step 2", "Answer"], rows)
            + example("Solve 6" + X + " − 4 = 26.", ["Add 4 to both sides: 6" + X + " = 30.", "Divide both sides by 6: " + X + " = 5.",
                                                    "Check: 6 × 5 − 4 = 30 − 4 = 26."], X + " = 5")
            + example("A taxi charges $3 plus $2 per mile. A ride costs $27. How many miles?",
                      ["Write an equation: 2" + "<i>m</i> + 3 = 27.", "Subtract 3: 2<i>m</i> = 24.", "Divide by 2: <i>m</i> = 12."], "12 miles")
            + "<h2>Common mistakes</h2><ul><li>Adding instead of subtracting: in 3" + X + " + 5 = 20, take away 5 (15), do not add it (25).</li>"
            "<li>Dividing first: 3" + X + " + 5 = 20 is not " + X + " + 5 = 20 ÷ 3. Undo the + 5 first.</li>"
            "<li>Distributing to only one term: 2(" + X + " + 3) is 2" + X + " + 6, not 2" + X + " + 3.</li>"
            "<li>Losing a sign: −2" + X + " = −8 gives " + X + " = 4, not −4.</li></ul>")


def main():
    sets = [set_steps(), set_basic(), set_negative(), set_mixed(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "two-step-equations",
        "title": "Two-Step Equations",
        "seo_title": "Grade 7 Two-Step Equations Worksheets: px + q = r, p(x + q) = r and Word Problems",
        "short_title": "Two-step equations",
        "domain": "Expressions & Equations",
        "standard_code": "7.EE.B.4a",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/EE/B/4/",
        "standard_text": "Solve word problems leading to equations of the form px + q = r and p(x + q) = r, where p, q, and r are specific rational numbers. Solve equations of these forms fluently. Compare an algebraic solution to an arithmetic solution, identifying the sequence of the operations used in each approach.",
        "meta_desc": "Free Grade 7 two-step equations worksheets: undo the steps in reverse order, solve px + q = r and p(x + q) = r with negatives, decimals and fractions, check solutions, and write equations for word problems. 100 practice questions with an answer key.",
        "key_big": "Undo the steps in reverse order: first the adding or subtracting, then the multiplying or dividing.",
        "key_sub": "3x + 5 = 20 → 3x = 15 → x = 5. Do the same thing to both sides, then check your answer.",
        "body_html": body(),
        "faq": [
            {"q": "How do you solve a two-step equation?", "a": "Undo the operations in reverse order. For 3x + 5 = 20, subtract 5 from both sides to get 3x = 15, then divide both sides by 3 to get x = 5."},
            {"q": "How do I solve p(x + q) = r?", "a": "Divide both sides by p, then undo q. For 2(x + 3) = 16, divide by 2 to get x + 3 = 8, so x = 5. You can also distribute first: 2x + 6 = 16."},
            {"q": "How do I check my answer?", "a": "Put your answer back into the original equation. If both sides are equal, it is correct: 3 × 5 + 5 = 20."},
            {"q": "How do I write an equation from a word problem?", "a": "Find the unknown and give it a letter. A fixed amount is the constant, and an amount for each item is the coefficient: $3 plus $2 per mile is 2m + 3."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 3,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
