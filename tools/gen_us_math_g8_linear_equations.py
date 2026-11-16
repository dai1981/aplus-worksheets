# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Linear Equations in One Variable (8.EE.C.7)
  python3 tools/gen_us_math_g8_linear_equations.py
Variables on both sides, distributing and combining like terms, fractions and decimals,
one / no / infinitely many solutions, and word problems. Wrong answers come from real mistakes:
moving a term without changing its sign, adding the x-terms instead of subtracting,
distributing to only the first term, and stopping one step early.
"""
import random
from fractions import Fraction as F
from ws_common import num, nums, mcq, balance, B, table, example, write_unit, X, MINUS
from g8_common import lin, term, plus

R = random.Random(80101)
UPDATED = "2026-11-16"
ONE, NONE, INF = "One solution", "No solution", "Infinitely many solutions"


def eq(a, b, c, d, st="d"):
    return "%s = %s" % (lin(a, b, st=st), lin(c, d, st=st))


def both_sides(a, b, c, x, st="d"):
    """a x + b = c x + d with solution x."""
    a, b, c, x = F(a), F(b), F(c), F(x)
    d = a * x + b - c * x
    txt = eq(a, b, c, d, st)
    k = a - c
    e = ("Subtract %s from both sides: %s = %s. " % (term(c, st=st), lin(k, b, st=st), num(d, st))
         if c != 0 else "")
    e += ("Then %s %s: %s = %s. Divide by %s: %s = %s."
          % ("subtract" if b >= 0 else "add", num(abs(b), st), term(k, st=st), num(d - b, st), num(k, st), X, num(x, st)))
    e += " Check: both sides equal %s." % num(a * x + b, st)
    ws = [(d + b) / k, (d - b) / (a + c) if a + c else None, (b - d) / k, (d - b) / a if a else None, -x, d - b]
    return mcq("Solve %s." % B(txt), (num(x, st), x), nums(ws, st) + nums(ws, "f"), e)


def distribute(p, q, r, c, x):
    """p(x + q) + r = c x + d."""
    p, q, r, c, x = map(F, (p, q, r, c, x))
    d = p * (x + q) + r - c * x
    left = "%s(%s%s)%s" % (num(p) if p != -1 else MINUS, X, plus(q), plus(r) if r else "")
    txt = "%s = %s" % (left, lin(c, d))
    a, b = p, p * q + r
    k = a - c
    if r:
        e = ("Distribute: %s%s = %s. Combine: %s = %s. " % (lin(p, p * q), plus(r), lin(c, d), lin(a, b), lin(c, d)))
    else:
        e = "Distribute: %s = %s. " % (lin(a, b), lin(c, d))
    e += ("Subtract %s from both sides: %s = %s. " % (term(c), lin(k, b), num(d)) if c else "")
    e += ("Then %s = %s." % (X, num(x))) if k == 1 else ("Then %s = %s, so %s = %s." % (term(k), num(d - b), X, num(x)))
    wrong_d = (d - (q + r)) / k if k else None        # multiplied only x by p
    ws = [wrong_d, (d + b) / k, (d - b) / (a + c) if a + c else None, -x, (d - b) / a]
    it = mcq("Solve %s." % B(txt), (num(x), x), nums(ws) + nums(ws, "f"), e)
    if wrong_d is not None and num(wrong_d) in it["c"][1:]:
        it["e"] += " Not %s: multiply %s by both %s and %s." % (num(wrong_d), num(p), X, num(q))
    return it


# ============================================================ set 1
def set_both():
    its = []
    for a, b, c, x in [(5, 3, 2, 4), (7, -4, 3, 2), (6, 1, 4, 5), (4, 9, 1, -2), (9, -6, 5, 3), (3, 14, 5, 7),
                       (8, -5, 2, -1), (2, 11, 6, 2), (-3, 7, 2, 4), (10, -8, 4, 3), (5, 12, 8, -4), (-4, 1, 2, -3),
                       (11, -7, 6, 2), (3, -10, -2, 6), (6, 15, 9, 5), (-5, -9, -8, 2), (12, 4, 7, -6), (4, -13, 7, -5),
                       (-6, 20, -2, 5), (13, -9, 8, 3)]:
        its.append(both_sides(a, b, c, x))
    return {"title": "Variables on both sides", "items": its}


# ============================================================ set 2
def set_dist():
    its = []
    for p, q, r, c, x in [(3, 2, 0, 1, 5), (2, -4, 5, 1, 7), (4, 1, -3, 2, 6), (5, -2, 0, 3, 4), (-2, 3, 10, 1, 2),
                          (6, 1, -8, 4, 3), (3, -5, 7, 5, -4), (-4, -2, 0, 2, 3), (7, 2, -6, 3, 1), (2, 6, -1, 5, 3),
                          (-3, 4, 9, 2, -1), (8, -1, 3, 6, 2), (5, 3, -20, 1, 4), (-6, 2, 4, -2, -3), (4, -3, 15, 7, 1),
                          (9, -2, 0, 5, 3), (-5, 1, 14, 3, 2), (3, 7, -13, -1, -2), (2, -9, 30, -4, -1), (10, -3, 6, 4, 2)]:
        its.append(distribute(p, q, r, c, x))
    return {"title": "Distribute and combine like terms", "items": its}


# ============================================================ set 3
def set_frac():
    its = []
    for a, b, c, x in [(F("0.5"), 3, F("0.2"), 10), (F("1.2"), F("-0.6"), F("0.8"), 3), (F("2.5"), 4, F("1.5"), -2),
                       (F("0.6"), F("1.4"), F("0.1"), 4), (F("3.5"), -7, F("1.5"), F("2.5")), (F("0.25"), 5, F("0.75"), 8),
                       (F("1.8"), F("0.4"), F("1.2"), -1), (F("4.2"), F("-3.6"), F("2.2"), F("1.5")), (F("0.9"), 2, F("0.4"), F("-0.4")),
                       (F("2.4"), F("-1.2"), F("0.4"), F("0.6"))]:
        its.append(both_sides(a, b, c, x))
    for a, b, c, x in [(F(1, 2), 3, F(1, 4), 8), (F(2, 3), -1, F(1, 3), 6), (F(3, 4), 2, F(1, 4), -4), (F(1, 3), 5, F(5, 6), 4),
                       (F(5, 2), -3, F(1, 2), F(3, 2)), (F(2, 5), 4, F(-3, 5), -2), (F(3, 2), F(1, 2), 1, 5), (F(1, 6), 2, F(2, 3), -8),
                       (F(4, 3), F(-2, 3), F(1, 3), 2), (F(7, 4), -1, F(3, 4), F(5, 2))]:
        its.append(both_sides(a, b, c, x, "f"))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17],
             o[8], o[18], o[9], o[19]]
    return {"title": "Fractions and decimals", "items": order}


# ============================================================ set 4
def kind_of(a, b, c, d):
    if a != c:
        return ONE
    return INF if b == d else NONE


def set_count():
    its = []
    for a, b, c, d in [(3, 5, 3, 5), (2, 7, 2, -1), (4, -3, 1, 9), (5, 2, 5, 8), (-2, 6, -2, 6), (6, 1, 2, 1),
                       (7, -4, 7, -4), (3, 0, 3, 2), (8, 5, -8, 5), (1, -9, 1, 9)]:
        k = kind_of(a, b, c, d)
        txt = eq(a, b, c, d)
        if k == ONE:
            x = F(d - b, a - c)
            e = "The %s-terms are different (%s and %s), so you can solve: %s = %s. <b>One solution</b>." % (
                X, term(a), term(c), X, num(x))
        elif k == NONE:
            e = ("Subtract %s from both sides: %s = %s. That is never true, so there is <b>no solution</b>."
                 % (term(a), num(b), num(d)))
        else:
            e = "Both sides are exactly the same, so every number works. <b>Infinitely many solutions</b>."
        its.append(mcq("How many solutions does %s have?" % B(txt), (k, k),
                       [(c_, c_) for c_ in (ONE, NONE, INF, "Exactly two solutions") if c_ != k], e))
    for left, right, k, e in [
        ("2(%s + 3)" % X, "2%s + 6" % X, INF, "2(x + 3) = 2x + 6. The two sides are the same expression: <b>infinitely many solutions</b>."),
        ("3(%s − 1)" % X, "3%s + 1" % X, NONE, "3(x − 1) = 3x − 3. Then 3x − 3 = 3x + 1 gives −3 = 1, which is false: <b>no solution</b>."),
        ("4%s + 2%s" % (X, X), "6%s − 5" % X, NONE, "4x + 2x = 6x. Then 6x = 6x − 5 gives 0 = −5: <b>no solution</b>."),
        ("5(%s + 2) − %s" % (X, X), "4%s + 10" % X, INF, "5x + 10 − x = 4x + 10. Same on both sides: <b>infinitely many solutions</b>."),
        ("2(%s + 4)" % X, "3%s + 8" % X, ONE, "2x + 8 = 3x + 8 gives x = 0. Zero is a solution: <b>one solution</b>."),
    ]:
        its.append(mcq("How many solutions does %s have?" % B(left + " = " + right), (k, k),
                       [(c_, c_) for c_ in (ONE, NONE, INF, "Exactly two solutions") if c_ != k], e))
    for c, d, want in [(4, 7, NONE), (5, -2, INF), (3, 9, ONE)]:
        # complete 4x + 7 = ? so that ...
        if want == NONE:
            right, wr = lin(c, d + 3), [lin(c, d), lin(c + 1, d), lin(c - 1, d + 3)]
            e = "Use the same %s-term but a different number: %s = %s is never true. The answer is <b>%s</b>." % (X, lin(c, d), right, right)
        elif want == INF:
            right, wr = lin(c, d), [lin(c, d + 1), lin(c + 2, d), lin(-c, d)]
            e = "Make the right side exactly the same: <b>%s</b>." % right
        else:
            right, wr = lin(c + 2, d), [lin(c, d), lin(c, d - 4), lin(c, -d)]
            e = "A different %s-term gives exactly one solution. The answer is <b>%s</b>." % (X, right)
        its.append(mcq("Which right side makes %s = ? have <b>%s</b>?" % (lin(c, d), want.lower()), (right, right),
                       [(w, w) for w in wr], e))
    for eqs, k in [([eq(2, 3, 2, 5), eq(2, 3, 1, 5), eq(2, 3, 2, 3), eq(2, 3, 3, 3)], NONE),
                   ([eq(3, -1, 3, -1), eq(3, -1, 3, 1), eq(3, -1, -3, -1), eq(3, -1, 1, -1)], INF)]:
        ans = eqs[0]
        e = ("%s has the same %s-term on both sides but different numbers, so it is never true." % (ans, X)) if k == NONE else \
            ("%s has the same expression on both sides, so every %s works." % (ans, X))
        its.append(mcq("Which equation has <b>%s</b>?" % k.lower(), (ans, ans), [(w, w) for w in eqs[1:]],
                       e + " The answer is <b>%s</b>." % ans))
    o = its
    order = [o[0], o[1], o[2], o[10], o[3], o[11], o[4], o[5], o[12], o[13], o[6], o[15], o[7], o[14], o[16], o[8],
             o[17], o[9], o[18], o[19]]
    assert len({id(i) for i in order}) == 20
    return {"title": "One, none or infinitely many", "items": order}


# ============================================================ set 5
def set_words():
    its = []

    def item(q, x, ws, e, unit=""):
        x = F(x)
        cands = [(num(F(w)) + unit, F(w)) for w in list(ws) + [x + 1, x - 1, 2 * x] if num(F(w)) is not None]
        its.append(mcq(q, (num(x) + unit, x), cands, e))

    item("Gym A charges $30 plus $5 per visit. Gym B charges $10 plus $9 per visit. For how many visits do they cost the same?",
         5, [F(40, 14), F(20, 14), 10], "30 + 5v = 10 + 9v, so 20 = 4v and v = 5 visits.", " visits")
    item("Jo has $45 and saves $6 a week. Max has $81 and saves $3 a week. After how many weeks will they have the same amount?",
         12, [F(126, 9), 4, 36], "45 + 6w = 81 + 3w, so 3w = 36 and w = 12 weeks.", " weeks")
    item("A plant is 8 cm tall and grows 2 cm a week. Another is 20 cm tall and grows 0.5 cm a week. When are they the same height?",
         8, [F(28, F(5, 2)), 24, 6], "8 + 2w = 20 + 0.5w, so 1.5w = 12 and w = 8 weeks.", " weeks")
    item("Taxi A: $4 plus $2.50 per mile. Taxi B: $7 plus $2 per mile. For how many miles is the cost the same?",
         6, [F(11, F(9, 2)), 3, F(3, F(9, 2))], "4 + 2.5m = 7 + 2m, so 0.5m = 3 and m = 6 miles.", " mi")
    item("Twice a number plus 7 equals 5 times the number minus 11. What is the number?", 6, [F(-4, 3), F(18, 7), -6],
         "2n + 7 = 5n − 11, so 18 = 3n and n = 6.")
    item("Three times a number, minus 4, is the same as the number plus 10. What is the number?", 7, [3, F(14, 4), 14],
         "3n − 4 = n + 10, so 2n = 14 and n = 7.")
    item("A square has side x + 2. A triangle has sides 2x, 2x and x + 2. Their perimeters are equal. Find x.",
         6, [F(10, 9), 2, 3], "4(x + 2) = 2x + 2x + x + 2, so 4x + 8 = 5x + 2 and x = 6.")
    item("A rectangle is 3 times as long as it is wide. Its perimeter is 64 in. What is its width?", 8, [16, F(64, 3), 24],
         "2w + 2(3w) = 64, so 8w = 64 and w = 8 in.", " in.")
    item("The sum of three consecutive whole numbers is 72. What is the smallest number?", 23, [24, 22, 25],
         "n + (n + 1) + (n + 2) = 72, so 3n + 3 = 72, 3n = 69 and n = 23.")
    item("The sum of two consecutive even numbers is 86. What is the smaller number?", 42, [43, 44, 41],
         "n + (n + 2) = 86, so 2n = 84 and n = 42.")
    item("Phone plan A: $40 a month plus $0.05 per text. Plan B: $25 a month plus $0.10 per text. For how many texts are they equal?",
         300, [130, 3000, 30], "40 + 0.05t = 25 + 0.10t, so 15 = 0.05t and t = 300 texts.", " texts")
    item("Ann is 4 times as old as her son. In 20 years she will be twice as old as him. How old is the son now?",
         10, [5, 20, 40], "4s + 20 = 2(s + 20), so 4s + 20 = 2s + 40, 2s = 20 and s = 10 years.", " years")
    item("A pool has 900 gallons and drains 30 gallons a minute. Another has 300 gallons and fills 20 gallons a minute. When are they equal?",
         12, [60, 6, 30], "900 − 30m = 300 + 20m, so 600 = 50m and m = 12 minutes.", " min")
    item("Company A rents a car for $50 plus $0.20 per mile. Company B charges $35 plus $0.25 per mile. For how many miles are they equal?",
         300, [F(85, F(9, 20)), 30, 3000], "50 + 0.2m = 35 + 0.25m, so 15 = 0.05m and m = 300 miles.", " mi")
    item("Half of a number plus 9 equals the number minus 3. What is the number?", 24, [12, 8, 6],
         "n/2 + 9 = n − 3, so 12 = n/2 and n = 24.")
    item("Two angles are equal. One measures (3x + 15)°. The other measures (5x − 25)°. Find x.", 20, [5, 10, 75],
         "3x + 15 = 5x − 25, so 40 = 2x and x = 20.")
    item("A candle 30 cm tall burns 2 cm an hour. A candle 20 cm tall burns 1 cm an hour. When are they the same height?",
         10, [F(50, 3), 5, 20], "30 − 2h = 20 − h, so 10 = h. After 10 hours both are 10 cm.", " hours")
    item("A store sells pens for $1.25 each. A second store charges $0.75 each plus $4 shipping. For how many pens is the cost the same?",
         8, [2, F(16, 5), 4], "1.25p = 0.75p + 4, so 0.5p = 4 and p = 8 pens.", " pens")
    item("5(x − 2) is 14 more than 2x. Find x.", 8, [F(4, 3), F(22, 3), 6], "5x − 10 = 2x + 14, so 3x = 24 and x = 8.")
    item("The average of x, x + 4 and 2x is 9. Find x.", F(23, 4), [F(27, 4), F(5, 4), 9],
         "(x + x + 4 + 2x) ÷ 3 = 9, so 4x + 4 = 27, 4x = 23 and x = 5.75.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems", "items": its}


def body():
    return ("<h2>Get the variable on one side</h2>"
            "<p>When " + X + " is on both sides, move all the " + X + "-terms to one side and all the numbers to the other. "
            "Do the same thing to both sides each time.</p>"
            + table(["Step", "5" + X + " + 3 = 2" + X + " + 15"], [
                ["Subtract 2" + X + " from both sides", "3" + X + " + 3 = 15"],
                ["Subtract 3 from both sides", "3" + X + " = 12"],
                ["Divide by 3", X + " = 4"]])
            + example("Solve 3(" + X + " − 2) + 4 = " + X + " + 8.",
                      ["Distribute: 3" + X + " − 6 + 4 = " + X + " + 8.", "Combine: 3" + X + " − 2 = " + X + " + 8.",
                       "Subtract " + X + ": 2" + X + " − 2 = 8.", "Add 2, then divide by 2: " + X + " = 5."], X + " = 5")
            + "<h2>One, none or infinitely many</h2>"
            + table(["What you get", "Example", "Solutions"], [
                [X + " = a number", "2" + X + " + 1 = " + X + " + 4 → " + X + " = 3", "One"],
                ["A false statement", "3" + X + " + 2 = 3" + X + " + 5 → 2 = 5", "None"],
                ["A true statement", "2(" + X + " + 1) = 2" + X + " + 2 → 2 = 2", "Infinitely many"]])
            + "<h2>Common mistakes</h2><ul>"
            "<li>Moving a term without changing its sign: from 5" + X + " + 3 = 2" + X + " + 15, the 3 becomes −3 on the other side.</li>"
            "<li>Adding the " + X + "-terms: 5" + X + " = 2" + X + " + 12 gives 3" + X + " = 12, not 7" + X + " = 12.</li>"
            "<li>Distributing to one term only: 3(" + X + " − 2) is 3" + X + " − 6, not 3" + X + " − 2.</li>"
            "<li>Thinking " + X + " = 0 means no solution. Zero can be the answer.</li></ul>")


def main():
    sets = [set_both(), set_dist(), set_frac(), set_count(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "linear-equations",
        "title": "Linear Equations: Variables on Both Sides",
        "seo_title": "Grade 8 Linear Equations Worksheets: Variables on Both Sides, One, None or Infinitely Many Solutions",
        "short_title": "Linear equations",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.C.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/C/7/",
        "standard_text": "Solve linear equations in one variable. a. Give examples of linear equations in one variable with one solution, infinitely many solutions, or no solutions. b. Solve linear equations with rational number coefficients, including equations whose solutions require expanding expressions using the distributive property and collecting like terms.",
        "meta_desc": "Free Grade 8 linear equations worksheets: solve equations with variables on both sides, distribute and combine like terms, work with fractions and decimals, decide if there is one, no or infinitely many solutions, and solve word problems. 100 questions with an answer key.",
        "key_big": "Move the x-terms to one side and the numbers to the other, doing the same to both sides.",
        "key_sub": "If the x-terms cancel: a false statement means no solution, a true statement means infinitely many.",
        "body_html": body(),
        "faq": [
            {"q": "How do you solve an equation with variables on both sides?", "a": "Subtract one x-term from both sides so x is on one side only. Then undo the numbers as in a two-step equation. For 5x + 3 = 2x + 15, subtract 2x, then 3, then divide by 3: x = 4."},
            {"q": "How do you know if an equation has no solution?", "a": "If the x-terms cancel and you are left with a false statement like 2 = 5, there is no solution."},
            {"q": "When does an equation have infinitely many solutions?", "a": "When both sides simplify to the same expression, such as 2x + 2 = 2x + 2. Every number makes it true."},
            {"q": "Can the solution of an equation be 0?", "a": "Yes. If you get x = 0, the equation has one solution, and that solution is zero."}],
        "sets": sets, "pdf_url": "", "sort": 1, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
