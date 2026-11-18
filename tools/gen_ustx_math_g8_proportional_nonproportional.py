# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Proportional and Non-Proportional Relationships (TEKS 8.4B, 8.5A, 8.5B, 8.5E, 8.5F)
  python3 tools/gen_ustx_math_g8_proportional_nonproportional.py
Proportional or not from tables, equations and words, direct variation problems, the unit rate as slope (US Grade 8
maker with a new seed), and y = mx + b with b ≠ 0 in context (own makers).
Wrong answers come from real mistakes: calling every line proportional, checking only one pair, and forgetting the
starting amount.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g8_slope as sl
adopt(sl)
sl.R = random.Random(680070)
tx_common.GRADE = "grade-8"

from fractions import Fraction as F
from ws_common import num

INK = "#1f2937"


def g(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if "." in s:
        a, b = s.split(".")
        return ("−" if v < 0 else "") + comma(abs(int(a))) + "." + b
    return num(int(s))


def pt(p):
    return "(%s, %s)" % (g(p[0]), g(p[1]))


def tbl(xs, ys):
    th = "".join("<td>%s</td>" % comma(x) for x in xs)
    td = "".join("<td>%s</td>" % comma(y) for y in ys)
    return "<div class='sn-tw'><table class='sn-table'><tbody><tr><th>x</th>%s</tr><tr><th>y</th>%s</tr></tbody></table></div>" % (th, td)


def one_table(r):
    m = r.randint(2, 12)
    b = r.choice([0, 0, r.randint(1, 20)])
    xs = sorted(r.sample(range(1, 11), 4))
    ys = [m * x + b for x in xs]
    pr = b == 0
    return mcq(tbl(xs, ys) + "Is the relationship proportional?", "Yes, y ÷ x is always %d" % m if pr else "No, y ÷ x is not the same for every pair",
               ["No, y ÷ x is not the same for every pair" if pr else "Yes, y ÷ x is always %d" % (ys[0] // xs[0] if ys[0] % xs[0] == 0 else m), "Yes, because y increases" if pr else "Yes, because the rate of change is %d" % m, "No, because the x-values skip numbers"],
               ("y ÷ x = %d for every pair, so it is <b>proportional</b>: y = %dx." % (m, m)) if pr else ("%s ÷ %d ≠ %s ÷ %d. The graph would not go through (0, 0). It is <b>not proportional</b>: y = %dx + %d." % (comma(ys[0]), xs[0], comma(ys[1]), xs[1], m, b)))


def one_eq(r):
    m = r.randint(2, 15)
    b = r.randint(1, 30)
    eqs = ["y = %dx" % m, "y = %dx + %d" % (m, b), "y = x + %d" % b, "y = %dx − %d" % (m, b)]
    if r.random() < 0.5:
        return mcq("Which equation shows a <b>proportional</b> relationship?", eqs[0], eqs[1:], "A proportional relationship has the form y = kx, with no added constant: <b>%s</b>." % eqs[0])
    right = r.choice(eqs[1:])
    others = [eqs[0], "y = %dx" % (m + 1), "y = %s x" % fr(1, m)]
    return mcq("Which equation shows a <b>non-proportional</b> relationship?", right, others, "y = mx + b with b ≠ 0 is non-proportional: <b>%s</b>." % right)


STORY = [("A plumber charges $%d per hour.", True, "c = %dh"), ("A gym charges a $%d sign-up fee plus $%d per month.", False, "c = %dm + %d"),
         ("Each ticket costs $%d.", True, "c = %dt"), ("A taxi charges $%d to start plus $%d per mile.", False, "c = %dm + %d"),
         ("A car uses 1 gallon of gas every %d miles.", True, "d = %dg"), ("A pool has %d gallons and fills at %d gallons per minute.", False, "w = %dt + %d")]


def one_story(r):
    s, pr, eq = r.choice(STORY)
    a, b = r.randint(3, 40), r.randint(10, 60)
    txt = s % a if pr else s % (b, a)
    e = eq % a if pr else eq % (a, b)
    return mcq(txt + " Is the relationship proportional?", "Yes: %s" % e if pr else "No: %s" % e, ["No: %s" % (eq % a if pr else eq.split(" +")[0] % a) if pr else "Yes: %s" % eq.split(" +")[0] % a, "Yes, because the amount always increases", "No, because the numbers are large"],
               ("There is no starting amount, so the cost is a constant times the quantity: <b>%s</b>, proportional." % e) if pr else ("There is a starting amount of %d, so the graph does not start at (0, 0): <b>%s</b>, not proportional." % (b, e)))


def one_direct(r):
    k = r.choice([F(n) for n in range(2, 13)] + [F(1, 2), F(3, 2), F(5, 2)])
    x1 = r.randint(2, 12)
    y1 = k * x1
    x2 = r.randint(3, 20)
    y2 = k * x2
    if y1.denominator != 1 or y2.denominator != 1 or x1 == x2:
        return None
    if r.random() < 0.5:
        return mcq("y varies directly with x. When x = %d, y = %d. What is y when x = %d?" % (x1, y1, x2), str(y2), [str(y1 + x2 - x1), str(int(F(x1) * x2 / y1)) if (F(x1) * x2 / y1).denominator == 1 and int(F(x1) * x2 / y1) != y2 else str(y2 + int(k)), str(x2 * x1)],
                   "k = %d ÷ %d = %s. y = %s × %d = <b>%d</b>." % (y1, x1, g(float(k)), g(float(k)), x2, y2))
    item = r.choice([("Earnings vary directly with hours worked", "hours", "dollars"), ("The weight of a stack varies directly with the number of books", "books", "pounds"), ("The cost of pecans varies directly with the pounds bought", "pounds", "dollars")])
    return mcq("%s. %d %s give %d %s. Which equation models this?" % (item[0], x1, item[1], y1, item[2]), "y = %sx" % g(float(k)), ["y = x + %d" % (y1 - x1), "y = %sx" % (g(float(1 / k)) if (1 / k).denominator == 1 else fr((1 / k).numerator, (1 / k).denominator)), "y = %dx" % y1],
               "k = %d ÷ %d = %s, so <b>y = %sx</b>." % (y1, x1, g(float(k)), g(float(k))))


def build():
    sets, R = build_sets([
        ("Proportional or not? Tables", [("collect", one_table, 20)]),
        ("Proportional or not? Equations", [("collect", one_eq, 20)]),
        ("Proportional or not? Situations", [("collect", one_story, 20)]),
        ("Direct variation", [("collect", one_direct, 20)]),
        ("The unit rate as the slope", [("run", sl.set_prop, (), 20)]),
    ], 68007)
    finish(sets, R)
    body = lesson('<ul><li>A <b>proportional</b> relationship has the form y = kx. Its graph is a straight line through (0, 0), and y ÷ x is the same for every pair.</li><li>A <b>non-proportional</b> linear relationship has the form y = mx + b with b ≠ 0. Its graph does not pass through (0, 0).</li><li>In a proportional graph, the <b>unit rate</b> is the slope.</li><li><b>Direct variation</b> means y = kx: find k = y ÷ x, then use it.</li></ul>',
        [example("$25 fee plus $10 per hour", ["Starts at 25, not 0"], "non-proportional: y = 10x + 25"), example("y varies directly with x; y = 18 when x = 3. Find y when x = 7.", ["k = 6", "6 × 7"], "42")],
        [['Calling every straight line proportional', 'It must also pass through (0, 0).'], ['Checking only one pair', 'Every pair must have the same y ÷ x.'], ['Forgetting a starting amount', 'A fee or starting value makes it non-proportional.']])
    faq = [('What does TEKS 8.5F ask?', 'Distinguish between proportional and non-proportional situations using tables, graphs and equations in the form y = kx or y = mx + b, where b ≠ 0.'), ('What does TEKS 8.5E ask?', 'Solve problems involving direct variation.'), ('What does TEKS 8.4B ask?', 'Graph proportional relationships, interpreting the unit rate as the slope of the line that models the relationship.'), ('Is y = 3x − 2 proportional?', 'No. When x = 0, y = −2, not 0.')]
    make('proportional-and-non-proportional-relationships', 7, 'Proportionality', '8.4B, 8.5A, 8.5B, 8.5E, 8.5F',
         '8.4B graph proportional relationships, interpreting the unit rate as the slope of the line that models the relationship; 8.5A represent linear proportional situations with tables, graphs, and equations in the form of y = kx; 8.5B represent linear non-proportional situations with tables, graphs, and equations in the form of y = mx + b, where b ≠ 0; 8.5E solve problems involving direct variation; 8.5F distinguish between proportional and non-proportional situations using tables, graphs, and equations in the form y = kx or y = mx + b, where b ≠ 0',
         'Proportional and Non-Proportional Relationships', 'Proportional and Non-Proportional',
         'Free Grade 8 worksheets for Texas TEKS 8.4B and 8.5: proportional and non-proportional relationships in tables, equations and situations, direct variation and unit rate as slope. 100 questions with answers.',
         'Proportional: y = kx through (0, 0). Non-proportional: y = mx + b, b ≠ 0.', 'A starting fee makes a relationship non-proportional.',
         body, faq, sets, seo_title='Grade 8 Proportional and Non-Proportional Relationships Worksheets (TEKS 8.5F, STAAR)')


if __name__ == "__main__":
    build()
