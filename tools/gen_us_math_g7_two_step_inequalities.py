# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Two-Step Inequalities (7.EE.B.4b)
  python tools/gen_us_math_g7_two_step_inequalities.py
Solve px + q > r (and <, ≥, ≤), graph the solutions and use them in word problems.
Wrong answers come from real mistakes: forgetting to reverse the sign when dividing by a
negative, reversing it when dividing by a positive, mixing up open and closed circles,
and undoing the steps in the wrong order.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, fig, figure, svg_wrap, text, line, arrow_head, table, example,
                       write_unit, GREEN, INK, BLUE, MINUS, X)

R = random.Random(71001)
UPDATED = "2026-11-09"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
OPP = {">": "≥", "≥": ">", "<": "≤", "≤": "<"}
WORD = {">": "greater than", "<": "less than", "≥": "greater than or equal to", "≤": "less than or equal to"}


def n(v):
    return num(F(v))


def ineq(sym, v, var=X):
    return "%s %s %s" % (var, sym, n(v))


def term(p):
    if p == 1:
        return X
    if p == -1:
        return MINUS + X
    return n(p) + X


def lhs(p, q):
    return term(p) + ("" if q == 0 else (" + %s" % n(q) if q > 0 else " − %s" % n(-q)))


def graph(b, sym, lo=None, hi=None, label="number line graph"):
    """Number line with a circle at b and an arrow for the solution."""
    b = int(b)
    lo = b - 5 if lo is None else lo
    hi = b + 5 if hi is None else hi
    W, y, x0, unit = 340, 40, 20, 300.0 / (hi - lo)
    Xp = lambda v: x0 + (v - lo) * unit
    s = [line(x0 - 8, y, x0 + 300 + 8, y, INK, 2), arrow_head(x0 - 10, y, -1, INK), arrow_head(x0 + 310, y, 1, INK)]
    for v in range(lo, hi + 1):
        s.append(line(Xp(v), y - 6, Xp(v), y + 6, INK, 1.5))
        s.append(text(Xp(v), y + 24, n(v), 12, weight=700 if v == b else 400))
    right = sym in (">", "≥")
    end = x0 + 310 if right else x0 - 10
    s.append(line(Xp(b), y, end - (8 if right else -8), y, BLUE, 5))
    s.append(arrow_head(end, y, 1 if right else -1, BLUE))
    closed = sym in ("≥", "≤")
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>" % (Xp(b), y, BLUE if closed else "#fff", BLUE))
    return svg_wrap(W + 20, 72, "".join(s), label)


def solve_item(p, q, r, sym, ask="Solve %s."):
    """px + q (sym) r."""
    p, q, r = F(p), F(q), F(r)
    b = (r - q) / p
    ans_sym = FLIP[sym] if p < 0 else sym
    good = ineq(ans_sym, b)
    txt = "%s %s %s" % (lhs(p, q), sym, n(r))
    step1 = ("Subtract %s from both sides" % n(q)) if q > 0 else ("Add %s to both sides" % n(-q))
    e = "%s: %s %s %s. Divide both sides by %s: %s." % (step1, term(p), sym, n(r - q), n(p), good)
    if p < 0:
        e += " Dividing by a negative number reverses the inequality sign. Not %s: the sign must flip." % ineq(sym, b)
    wrong = [ineq(FLIP[ans_sym], b), ineq(ans_sym, (r + q) / p), ineq(OPP[ans_sym], b), ineq(ans_sym, -b) if b != 0 else ineq(ans_sym, b + 1),
             ineq(ans_sym, r / p - q)]
    cands = []
    for w in wrong:
        if w != good and w not in cands and "None" not in w:
            cands.append(w)
    return mcq(ask % B(txt), (good, good), [(c, c) for c in cands], e)


# ------------------------------------------------------------ set 1
def set_basics():
    its = []
    for sym, v in [(">", 3), ("≤", -2), ("<", 7), ("≥", 0)]:
        good = "%s is %s %s" % (X, WORD[sym], n(v))
        bad = ["%s is %s %s" % (X, WORD[s], n(v)) for s in [FLIP[sym], OPP[sym], FLIP[OPP[sym]]]]
        its.append(mcq("What does %s mean?" % B(ineq(sym, v)), (good, good), [(b, b) for b in bad],
                       "%s means %s. The symbol %s includes the number itself only if it has a line under it." % (ineq(sym, v), WORD[sym], sym)))
    for p, q, sym, r, t in [(2, 3, ">", 11, 5), (3, -4, "≤", 8, 4), (2, 1, "<", 9, 4), (-2, 5, "≥", 1, 3), (4, 1, ">", 13, 3), (-3, 2, "<", -7, 4)]:
        val = p * t + q
        ok = {">": val > r, "<": val < r, "≥": val >= r, "≤": val <= r}[sym]
        e = "Put %d in for %s: %s = %s. Is %s %s %s? %s." % (t, X, lhs(p, q).replace(X, "(%d)" % t), n(val), n(val), sym, n(r), "Yes" if ok else "No")
        its.append(mcq("Is %s a solution of %s?" % (B("%s = %d" % (X, t)), B("%s %s %d" % (lhs(p, q), sym, r))), ("Yes" if ok else "No", ok),
                       [("No" if ok else "Yes", not ok), ("Only if %s is negative" % X, "n"), ("It cannot be checked", "c")], e))
    for sym, b in [(">", 2), ("≤", -1), ("≥", 4), ("<", 0), (">", -3), ("≤", 6)]:
        good = ineq(sym, b)
        bad = [ineq(OPP[sym], b), ineq(FLIP[sym], b), ineq(FLIP[OPP[sym]], b)]
        its.append(mcq("Which inequality does the graph show?" + fig(graph(b, sym)), (good, good), [(x, x) for x in bad],
                       "The circle is at %s and %s. The arrow points %s, so the numbers are %s %s: %s." % (
                           n(b), "filled in (the number is included)" if sym in ("≥", "≤") else "open (the number is not included)",
                           "right" if sym in (">", "≥") else "left", WORD[sym], n(b), good)))
    its.append(mcq("Which number is a solution of %s?" % B(ineq("<", -2)), ("−5", "a"), [("−2", "b"), ("0", "c"), ("3", "d")],
                   "−5 is to the left of −2 on the number line, so −5 < −2. −2 itself is not a solution because the sign is <, not ≤."))
    its.append(mcq("Which number is a solution of %s?" % B(ineq("≥", 6)), ("6", "a"), [("5", "b"), ("−7", "c"), ("5.9", "d")],
                   "≥ includes 6 itself, so 6 is a solution."))
    its.append(mcq("How many solutions does %s have?" % B(ineq(">", 4)), ("Infinitely many", "a"), [("One: 4", "b"), ("One: 5", "c"), ("None", "d")],
                   "Every number greater than 4 works, like 4.1, 5 and 100. An inequality usually has infinitely many solutions."))
    its.append(mcq("Which symbol means <b>at least</b>?", ("≥", "a"), [(">", "b"), ("≤", "c"), ("<", "d")],
                   "At least 10 means 10 or more: ≥ 10. At most means ≤."))
    return {"title": "Inequality basics and graphs", "items": its}


# ------------------------------------------------------------ set 2
def set_positive():
    its = []
    for p, q, r, sym in [(2, 3, 11, ">"), (3, -4, 14, "<"), (4, 5, 25, "≥"), (5, -2, 18, "≤"), (2, 7, 3, ">"), (6, 1, 31, "<"),
                         (3, 8, -1, "≥"), (7, -3, 25, "≤"), (4, -10, 6, ">"), (8, 6, -10, "<"), (2, 9, 21, "≥"), (10, -5, 45, "≤"),
                         (5, 12, 2, ">"), (3, -6, -15, "<"), (9, 4, 40, "≥"), (2, -1, 0, "≤")]:
        its.append(solve_item(p, q, r, sym))
    for p, q, r, sym in [(F("0.5"), 3, 8, ">"), (F("1.5"), -2, 7, "≤"), (F("0.25"), 1, 4, "<"), (F("2.5"), 4, 19, "≥")]:
        its.append(solve_item(p, q, r, sym))
    return {"title": "Solve: positive coefficients", "items": its}


# ------------------------------------------------------------ set 3
def set_negative():
    its = []
    for p, q, r, sym in [(-2, 3, 11, ">"), (-3, 1, -8, "<"), (-4, -5, 15, "≥"), (-1, 6, 2, "≤"), (-5, 2, 22, "<"), (-2, -7, -1, ">"),
                         (-6, 4, -14, "≥"), (-3, -9, 6, "≤"), (-1, -2, 5, ">"), (-4, 10, 30, "<"), (-7, 3, -18, "≤"), (-2, 1, 1, "≥"),
                         (-5, -5, 20, ">"), (-8, 6, -2, "<")]:
        its.append(solve_item(p, q, r, sym))
    its.append(mcq("When do you reverse the inequality sign?", ("When you multiply or divide both sides by a negative number", "a"),
                   [("When you add or subtract a negative number", "b"), ("Whenever there is a negative number in the inequality", "c"), ("When the answer is negative", "d")],
                   "Only multiplying or dividing by a negative reverses the sign. Example: −2x > 6 gives x < −3. Adding or subtracting never reverses it."))
    its.append(mcq("Solve %s." % B("−" + X + " < 4"), (ineq(">", -4), "a"), [(ineq("<", -4), "b"), (ineq(">", 4), "c"), (ineq("<", 4), "d")],
                   "−x < 4 means −1 × x < 4. Divide by −1 and flip: x > −4."))
    its.append(mcq("Ana solved %s and got %s. What mistake did she make?" % (B("−3" + X + " + 2 ≥ 14"), B(ineq("≥", -4))),
                   ("She did not reverse the sign when dividing by −3.", "a"),
                   [("She should have added 2.", "b"), ("She should have divided by 3.", "c"), ("There is no mistake.", "d")],
                   "−3x ≥ 12. Dividing by −3 flips the sign: x ≤ −4."))
    its.append(mcq("Which inequality has the same solutions as %s?" % B("−4" + X + " > 8"), (ineq("<", -2), "a"),
                   [(ineq(">", -2), "b"), (ineq("<", 2), "c"), (ineq(">", 2), "d")], "Divide by −4 and flip the sign: x < −2."))
    its.append(mcq("Solve %s." % B("5 − 2" + X + " ≤ 11"), (ineq("≥", -3), "a"), [(ineq("≤", -3), "b"), (ineq("≥", 3), "c"), (ineq("≤", 8), "d")],
                   "Subtract 5: −2x ≤ 6. Divide by −2 and flip: x ≥ −3."))
    its.append(mcq("Solve %s." % B("12 − 3" + X + " > 0"), (ineq("<", 4), "a"), [(ineq(">", 4), "b"), (ineq("<", -4), "c"), (ineq(">", -4), "d")],
                   "Subtract 12: −3x > −12. Divide by −3 and flip: x < 4."))
    return {"title": "Solve: negative coefficients (flip the sign)", "items": its}


# ------------------------------------------------------------ set 4
def set_graph_solutions():
    its = []
    for p, q, r, sym in [(2, 1, 9, ">"), (-3, 2, 11, "≥"), (4, -3, 5, "≤"), (-2, -1, 5, "<"), (3, 6, 0, "≥"), (-5, 5, -10, ">"),
                         (2, -7, -3, "<"), (-1, 4, 1, "≤"), (5, 2, 17, ">"), (-4, -2, -10, "≥")]:
        b = F(r - q, p)
        ans = FLIP[sym] if p < 0 else sym
        txt = "%s %s %s" % (lhs(p, q), sym, n(r))
        def desc(sym_, b_):
            return "%s circle at %s, arrow to the %s" % ("Closed" if sym_ in ("≥", "≤") else "Open", n(b_), "right" if sym_ in (">", "≥") else "left")
        good = (desc(ans, b), "g")
        bad = [(desc(FLIP[ans], b), "f"), (desc(OPP[ans], b), "o"), (desc(ans, -b if b else b + 2), "s")]
        e = "Solve: %s. %s." % (ineq(ans, b), desc(ans, b))
        if p < 0:
            e += " Remember to flip the sign when dividing by %d." % p
        its.append(mcq("How should you graph the solutions of %s?" % B(txt), good, bad, e))
    for p, q, r, sym in [(3, -2, 10, "<"), (-2, 4, -6, "≤"), (6, 3, 27, "≥"), (-3, -4, 5, ">"), (2, 5, 5, "<"),
                         (-6, 1, 25, "≤"), (4, 7, -1, ">"), (-1, -3, -8, "≥"), (5, -9, 11, "≤"), (-2, 6, 14, "<")]:
        b = F(r - q, p)
        ans = FLIP[sym] if p < 0 else sym
        txt = "%s %s %s" % (lhs(p, q), sym, n(r))
        its.append(mcq("Solve %s, then choose the graph of the solution." % B(txt) + fig(graph(b, ans)), (ineq(ans, b), "g"),
                       [(ineq(FLIP[ans], b), "f"), (ineq(OPP[ans], b), "o"), (ineq(ans, -b if b else 1), "s")],
                       "The solution is %s, which matches the graph: %s circle at %s." % (ineq(ans, b), "closed" if ans in ("≥", "≤") else "open", n(b))))
    return {"title": "Solve and graph", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)

    def item(q, good, bad, e):
        its.append(mcq(q, (good, good), [(b, b) for b in bad], e))

    name, he, his = P.next()
    item("%s has $40 and wants to buy shirts that cost $12 each. Which inequality shows how many shirts (s) %s can buy?" % (name, he),
         "12<i>s</i> ≤ 40", ["12<i>s</i> ≥ 40", "<i>s</i> + 12 ≤ 40", "40<i>s</i> ≤ 12"], "The total cost 12s must be at most $40: 12s ≤ 40.")
    item("A taxi charges $3 plus $2 per mile. You can spend at most $25. How many miles can you ride?", "at most 11 miles",
         ["at least 11 miles", "at most 14 miles", "at most 12.5 miles"], "2m + 3 ≤ 25, so 2m ≤ 22 and m ≤ 11.")
    name, he, his = P.next()
    item("%s has $35 in savings and saves $15 a week. How many weeks until %s has more than $200?" % (name, he), "more than 11 weeks",
         ["fewer than 11 weeks", "more than 15 weeks", "more than 13 weeks"], "15w + 35 > 200, so 15w > 165 and w > 11.")
    item("A gym charges $50 to join and $20 a month. Your budget is $230. For how many months can you go?", "at most 9 months",
         ["at least 9 months", "at most 11 months", "at most 14 months"], "20m + 50 ≤ 230, so 20m ≤ 180 and m ≤ 9.")
    item("You need at least 90 points. You have 54 points, and each quiz is worth 6 points. How many quizzes must you pass?", "at least 6 quizzes",
         ["at most 6 quizzes", "at least 15 quizzes", "at least 24 quizzes"], "54 + 6q ≥ 90, so 6q ≥ 36 and q ≥ 6.")
    item("An elevator can hold at most 1,200 pounds. A worker weighs 180 pounds and brings boxes of 60 pounds each. How many boxes can go?", "at most 17 boxes",
         ["at least 17 boxes", "at most 20 boxes", "at most 23 boxes"], "180 + 60b ≤ 1,200, so 60b ≤ 1,020 and b ≤ 17.")
    item("A phone has 80% battery and loses 4% each hour. When will it be below 20%?", "after more than 15 hours",
         ["after fewer than 15 hours", "after more than 25 hours", "after more than 5 hours"],
         "80 − 4h < 20, so −4h < −60. Divide by −4 and flip: h > 15.")
    item("A school club has $120. It spends $15 on each event and must keep more than $30. How many events can it hold?", "fewer than 6 events",
         ["more than 6 events", "fewer than 10 events", "fewer than 2 events"], "120 − 15e > 30, so −15e > −90. Divide by −15 and flip: e < 6. So at most 5 events.")
    item("Which inequality says: 3 more than twice a number is at least 15?", "2<i>n</i> + 3 ≥ 15",
         ["2<i>n</i> + 3 ≤ 15", "2(<i>n</i> + 3) ≥ 15", "3<i>n</i> + 2 ≥ 15"], "Twice a number is 2n, 3 more is 2n + 3, and at least means ≥.")
    item("Which inequality says: 5 less than 4 times a number is less than 23?", "4<i>n</i> − 5 < 23",
         ["5 − 4<i>n</i> < 23", "4<i>n</i> − 5 > 23", "4(<i>n</i> − 5) < 23"], "4 times a number is 4n; 5 less is 4n − 5.")
    item("A pool is being drained. It has 900 gallons and loses 50 gallons a minute. When will it have less than 300 gallons?", "after more than 12 minutes",
         ["after fewer than 12 minutes", "after more than 6 minutes", "after more than 18 minutes"], "900 − 50m < 300, so −50m < −600 and m > 12 (flip).")
    name, he, his = P.next()
    item("%s earns $9 an hour and wants to earn at least $150 for a bike. %s already has $42. How many hours must %s work?" % (name, he.capitalize(), he),
         "at least 12 hours", ["at most 12 hours", "at least 17 hours", "at least 21 hours"], "42 + 9h ≥ 150, so 9h ≥ 108 and h ≥ 12.")
    item("A rectangle has length 10 cm and width w cm. Its perimeter must be less than 36 cm. What are the possible widths?", "less than 8 cm",
         ["more than 8 cm", "less than 16 cm", "less than 26 cm"], "2(10) + 2w < 36, so 20 + 2w < 36, 2w < 16 and w < 8.")
    item("Movie tickets cost $11 and popcorn is $7. A group buys one popcorn and spends no more than $73. How many tickets can it buy?",
         "at most 6 tickets", ["at least 6 tickets", "at most 7 tickets", "at most 5 tickets"], "11t + 7 ≤ 73, so 11t ≤ 66 and t ≤ 6.")
    item("The temperature is 5°F and falls 3°F each hour. When will it be below −10°F?", "after more than 5 hours",
         ["after fewer than 5 hours", "after more than 1 hour", "after more than 3 hours"], "5 − 3h < −10, so −3h < −15 and h > 5 (flip the sign).")
    item("A box can hold at most 25 kg. The empty box weighs 1.5 kg. Each book weighs 0.5 kg. How many books fit?", "at most 47 books",
         ["at least 47 books", "at most 50 books", "at most 53 books"], "1.5 + 0.5b ≤ 25, so 0.5b ≤ 23.5 and b ≤ 47.")
    item("You must score more than 80 on average over two tests. You got 74 on the first. What must you get on the second?", "more than 86",
         ["more than 80", "more than 6", "less than 86"], "(74 + s) ÷ 2 > 80, so 74 + s > 160 and s > 86.")
    item("Which value of <i>x</i> is NOT a solution of 3<i>x</i> − 2 > 7?", "3", ["4", "10", "3.5"], "3x − 2 > 7 gives x > 3. 3 itself is not greater than 3.")
    item("A plumber charges $60 plus $45 an hour. The job must cost at most $285. What is the longest the job can take?", "5 hours",
         ["7 hours", "6 hours", "4 hours"], "45h + 60 ≤ 285, so 45h ≤ 225 and h ≤ 5. The longest is 5 hours.")
    item("A car rental is $30 a day plus $0.20 a mile. For one day, you want to spend under $60. How far can you drive?", "less than 150 miles",
         ["more than 150 miles", "less than 450 miles", "less than 300 miles"], "30 + 0.2m < 60, so 0.2m < 30 and m < 150.")
    return {"title": "Word problems", "items": its}


def body():
    g = graph(3, ">")
    g2 = graph(-2, "≤")
    rows = [["2" + X + " + 3 > 11", "subtract 3", "2" + X + " > 8", "divide by 2", X + " > 4"],
            [MINUS + "3" + X + " + 1 ≤ 7", "subtract 1", MINUS + "3" + X + " ≤ 6", "divide by −3, flip", X + " ≥ −2"]]
    return ("<h2>Solve like an equation</h2><p>Undo the steps in reverse order, just like a two-step equation. "
            "There is one new rule: <b>when you multiply or divide both sides by a negative number, reverse the inequality sign</b>.</p>"
            + table(["Inequality", "Step 1", "Result", "Step 2", "Solution"], rows)
            + "<h2>Graph the solutions</h2><p>Use an <b>open circle</b> for &gt; and &lt; (the number is not included) and a <b>closed circle</b> for ≥ and ≤ (it is included). "
            "Draw the arrow toward the numbers that work.</p>"
            + figure(g, X + " > 3: open circle at 3, arrow to the right.")
            + figure(g2, X + " ≤ −2: closed circle at −2, arrow to the left.")
            + example("You have $40. Shirts cost $12 each and shipping is $4. How many shirts can you buy?",
                      ["Write: 12<i>s</i> + 4 ≤ 40.", "Subtract 4: 12<i>s</i> ≤ 36.", "Divide by 12: <i>s</i> ≤ 3."], "at most 3 shirts")
            + "<h2>Common mistakes</h2><ul><li>Forgetting to flip: −2" + X + " > 8 gives " + X + " < −4, not " + X + " > −4.</li>"
            "<li>Flipping when you should not: 2" + X + " > −8 gives " + X + " > −4. The sign flips only when you divide by a negative.</li>"
            "<li>Using the wrong circle: ≥ and ≤ get a closed circle.</li></ul>")


def esc(o):
    """Inequality signs written with spaces around them become HTML entities."""
    if isinstance(o, str):
        return o.replace(" < ", " &lt; ").replace(" > ", " &gt; ")
    if isinstance(o, list):
        return [esc(x) for x in o]
    if isinstance(o, dict):
        return {k: esc(v) for k, v in o.items()}
    return o


def main():
    sets = [set_basics(), set_positive(), set_negative(), set_graph_solutions(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "two-step-inequalities",
        "title": "Two-Step Inequalities",
        "seo_title": "Grade 7 Two-Step Inequalities Worksheets: Solve, Graph and Word Problems",
        "short_title": "Two-step inequalities",
        "domain": "Expressions & Equations",
        "standard_code": "7.EE.B.4b",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/EE/B/4/",
        "standard_text": "Solve word problems leading to inequalities of the form px + q > r or px + q < r, where p, q, and r are specific rational numbers. Graph the solution set of the inequality and interpret it in the context of the problem.",
        "meta_desc": "Free Grade 7 two-step inequalities worksheets: inequality symbols and graphs, solving px + q > r, reversing the sign when dividing by a negative, graphing solutions, and word problems. 100 practice questions with an answer key.",
        "key_big": "Solve like an equation, but flip the sign when you multiply or divide by a negative.",
        "key_sub": "−3x + 1 ≤ 7 → −3x ≤ 6 → x ≥ −2. Open circle for < and >, closed circle for ≤ and ≥.",
        "body_html": body(),
        "faq": [
            {"q": "How do you solve a two-step inequality?", "a": "Undo the adding or subtracting, then undo the multiplying or dividing. For 2x + 3 > 11: 2x > 8, so x > 4."},
            {"q": "When do you flip the inequality sign?", "a": "Only when you multiply or divide both sides by a negative number. −2x > 8 becomes x < −4."},
            {"q": "Open circle or closed circle?", "a": "Use an open circle for < and > because the number is not a solution. Use a closed circle for ≤ and ≥ because it is."},
            {"q": "How do I write an inequality from words?", "a": "At most means ≤, at least means ≥, more than means >, and less than means <. $3 plus $2 per mile for at most $25 is 2m + 3 ≤ 25."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 10,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", esc(unit))


if __name__ == "__main__":
    main()
