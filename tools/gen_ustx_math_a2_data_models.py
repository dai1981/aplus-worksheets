# -*- coding: utf-8 -*-
"""
Texas Algebra II: Choosing Linear, Quadratic and Exponential Models (TEKS 2A.8A, 2A.8B, 2A.8C)
  python3 tools/gen_ustx_math_a2_data_models.py
Choosing a linear, quadratic or exponential model from a table or a situation, predicting with regression models,
interpreting the numbers in a model, and judging fits and predictions (own makers).
Wrong answers come from real mistakes: looking only at first differences, reading a growth factor of 1.06 as 106%
growth, and trusting a prediction far outside the data.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "algebra-2"

import us_hs
adopt(us_hs)


def W(fn, keep=None):
    """Use an item maker of another generator: its odd failures count as a skipped try, and a question text
    is used only once (not again with other wrong answers)."""
    seen = set()

    def f(r):
        try:
            it = fn(r)
        except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            raise AssertionError("skip")
        if not it or (keep and not keep(it)) or it["q"] in seen:
            raise AssertionError("skip")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def PR(fn, keep=None):
    """A fixed word-problem list of another generator as a set maker: a shuffled share of it."""
    def f(r):
        its = [it for it in fn() if keep is None or keep(it)]
        r.shuffle(its)
        return {"title": fn.__name__, "items": its * 3}
    f.__name__ = fn.__name__
    return f


MINUS = "−"
X = "<i>x</i>"


def sg(v):
    return ("−%s" % abs(v)) if v < 0 else str(v)


def poly(cs, v="<i>x</i>"):
    """[a, b, c] highest power first, e.g. 2x² − 3x + 1."""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        p = deg - i
        mag = abs(c)
        if p == 0:
            body = str(mag)
        else:
            body = ("" if mag == 1 else str(mag)) + v + ("<sup>%d</sup>" % p if p > 1 else "")
        if not out:
            out = (MINUS if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out or "0"
def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as Fr


def ft(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def fx(body, name="f"):
    return "<i>%s</i>(<i>x</i>) = %s" % (name, body)


MODELS = ["Linear", "Quadratic", "Exponential", "None of these"]


def table(xs, ys):
    return "<table class='sn-table'><tr><th><i>x</i></th>%s</tr><tr><th><i>y</i></th>%s</tr></table>" % ("".join("<td>%s</td>" % sg(v) for v in xs), "".join("<td>%s</td>" % comma(v) if v >= 0 else "<td>%s</td>" % sg(v) for v in ys))


def one_tab(r):
    kind = r.choice(["Linear", "Quadratic", "Exponential"])
    s = r.randint(0, 2)
    xs = list(range(s, s + 5))
    if kind == "Linear":
        m, b = r.choice([n for n in range(-9, 13) if n]), r.randint(-20, 40)
        ys = [m * x + b for x in xs]
        why = "The first differences are all %s, so the model is <b>linear</b>." % sg(m)
    elif kind == "Quadratic":
        a, b, c = r.choice([1, 2, 3, -1, -2]), r.randint(-6, 6), r.randint(-10, 20)
        ys = [a * x * x + b * x + c for x in xs]
        why = "The first differences change, but the second differences are all %s, so the model is <b>quadratic</b>." % sg(2 * a)
    else:
        a, g = r.choice([1, 2, 3, 5, 10, 64, 81, 128]), r.choice([2, 3, 4, Fr(1, 2), Fr(3, 2)])
        ys = [a * g ** x for x in xs]
        if any(Fr(y).denominator != 1 for y in ys) or max(ys) > 99999:
            raise AssertionError
        ys = [int(y) for y in ys]
        why = "Each <i>y</i> is %s times the one before (a constant ratio), so the model is <b>exponential</b>." % ft(g)
    return mcq(table(xs, ys) + "Which type of model fits the data best?", kind, [v for v in MODELS if v != kind], why)


SIT = [("A population grows by 3% each year.", "Exponential"), ("A car travels at a steady 60 miles per hour.", "Linear"), ("The height of a ball thrown into the air over time.", "Quadratic"),
       ("The area of a square compared with its side length.", "Quadratic"), ("The value of a car that loses 12% of its value each year.", "Exponential"),
       ("A phone plan costs $30 a month plus $5 for each gigabyte.", "Linear"), ("Bacteria that double every 20 minutes.", "Exponential"),
       ("A company's profit as the price rises: it goes up, peaks, then falls.", "Quadratic"), ("A taxi charges $3 plus $2 per mile.", "Linear"),
       ("The amount of a medicine left in the body when half is used up every 6 hours.", "Exponential"), ("Savings that earn 5% interest compounded each year.", "Exponential"),
       ("A candle that burns down 0.5 inch every hour.", "Linear"), ("The area of a circle compared with its radius.", "Quadratic"),
       ("The number of people who have heard a rumor when the number triples each day.", "Exponential"), ("The gas left in a tank while driving at a steady speed.", "Linear"),
       ("The path of water from a fountain.", "Quadratic"), ("A worker's pay at $15 per hour.", "Linear"), ("The stopping distance of a car compared with its speed.", "Quadratic"),
       ("The amount of a radioactive substance that decays by 8% each year.", "Exponential"), ("The temperature that drops 2 degrees each hour.", "Linear"),
       ("An investment that doubles every 9 years.", "Exponential"), ("The height of a rocket launched straight up, then falling back.", "Quadratic"),
       ("The number of seats in rows when each row has 2 more seats than the row before, compared with the row number.", "Linear"),
       ("The total cost of tickets at $12 each.", "Linear"), ("The number of handshakes when everyone in a group shakes hands once, compared with the group size.", "Quadratic")]
WHY = {"Linear": "It changes by the same <b>amount</b> each step: linear.", "Exponential": "It changes by the same <b>percent</b> or factor each step: exponential.",
       "Quadratic": "It rises and falls (or grows with a square): quadratic."}


def one_sit(r):
    t, kind = r.choice(SIT)
    return mcq("Which type of model fits this situation best? %s" % t, kind, [v for v in MODELS if v != kind], WHY[kind])


def money(v):
    c = int(round(v * 100))
    return "$%s.%02d" % (comma(c // 100), c % 100)


def one_pred(r):
    kind = r.choice(["lin", "quad", "exp"])
    if kind == "lin":
        m = Fr(r.randint(12, 95), 10)
        b = r.randint(20, 300)
        x = r.randint(6, 15)
        y = m * x + b
        what = r.choice([("the number of students in a club", "<i>x</i> years after the club started", ""), ("monthly sales, in units,", "<i>x</i> months after opening", ""), ("the average price of a ticket, in dollars,", "<i>x</i> years after a stadium opened", "$")])
        q = "A regression on data gives <i>y</i> = %s<i>x</i> + %d for %s %s. Predict <i>y</i> for <i>x</i> = %d." % (dec(m), b, what[0], what[1], x)
        right = dec(y)
        w = [dec(m * (x + 1) + b), dec(m + b + x), dec(m * x), dec((m + b) * x)]
        e = "%s(%d) + %d = %s." % (dec(m), x, b, dec(y))
    elif kind == "quad":
        a = -Fr(r.randint(2, 15), 10)
        bb = Fr(r.randint(30, 90), 10)
        c = r.randint(5, 40)
        x = r.randint(2, 8)
        y = a * x * x + bb * x + c
        if y <= 0:
            raise AssertionError
        q = "A quadratic regression of a toy's sales gives <i>y</i> = %s<i>x</i><sup>2</sup> + %s<i>x</i> + %d, where <i>x</i> is the price in dollars and <i>y</i> is sales in hundreds. Predict <i>y</i> when <i>x</i> = %d." % (dec(a), dec(bb), c, x)
        right = dec(y)
        w = [dec(a * x + bb * x + c), dec(-a * x * x + bb * x + c), dec(a * x * x + bb + c), dec(a * (2 * x) + bb * x + c)]
        e = "%s(%d)<sup>2</sup> + %s(%d) + %d = %s + %s + %d = %s." % (dec(a), x, dec(bb), x, c, dec(a * x * x), dec(bb * x), c, dec(y))
    else:
        a = r.choice([200, 500, 1000, 1500, 2500, 4000])
        g = r.choice([1.05, 1.08, 1.1, 1.12, 0.9, 0.85, 1.2])
        x = r.randint(3, 10)
        y = a * g ** x
        q = "An exponential regression gives <i>y</i> = %s(%s)<sup><i>x</i></sup>. Predict <i>y</i> for <i>x</i> = %d. Round to the nearest whole number." % (comma(a), ("%g" % g), x)
        right = comma(int(round(y)))
        w = [comma(int(round(a * g * x))), comma(int(round(a * g ** (x + 1)))), comma(int(round(a + g ** x))), comma(int(round((a * g) ** 1 * x * g)))]
        e = "%s × %s<sup>%d</sup> ≈ %s." % (comma(a), "%g" % g, x, right)
    w = [v for v in w if v != right]
    return mcq(q, right, w, e + " <b>%s</b>." % right)


def dec(v):
    v = Fr(v)
    if v.denominator == 1:
        return sg(int(v))
    s = ("%.2f" % float(v)).rstrip("0").rstrip(".")
    return s.replace("-", MINUS)


def one_int(r):
    kind = r.choice(["growth", "decay", "slope", "start", "vertex"])
    if kind == "growth":
        p = r.choice([2, 3, 4, 5, 6, 8, 12, 15])
        a = r.choice([800, 1200, 2500, 5000, 12000])
        q = "A model for a town's population is <i>y</i> = %s(%s)<sup><i>x</i></sup>, where <i>x</i> is the number of years from now. What does %s tell you?" % (comma(a), "1.%02d" % p, "1.%02d" % p)
        right = "The population grows by %d%% each year" % p
        w = ["The population grows by 1.%02d%% each year" % p, "The population grows by %d people each year" % p, "The population grows by 1%02d%% each year" % p]
    elif kind == "decay":
        p = r.choice([5, 8, 10, 15, 20, 25])
        a = r.choice([18000, 24000, 30000, 35000])
        g = "0.%02d" % (100 - p)
        q = "The value of a car is modeled by <i>y</i> = %s(%s)<sup><i>x</i></sup> dollars after <i>x</i> years. What does %s tell you?" % (comma(a), g, g)
        right = "The value drops by %d%% each year" % p
        w = ["The value drops by %d%% each year" % (100 - p), "The value drops by $%s each year" % g, "The value grows by %d%% each year" % (100 - p)]
    elif kind == "slope":
        m = Fr(r.randint(11, 99), 10)
        b = r.randint(10, 90)
        q = "A linear regression for the height of a plant is <i>y</i> = %s<i>x</i> + %d, with <i>x</i> in weeks and <i>y</i> in centimeters. What does %s mean?" % (dec(m), b, dec(m))
        right = "The plant grows about %s cm each week" % dec(m)
        w = ["The plant was %s cm tall at the start" % dec(m), "The plant grows %s%% each week" % dec(m), "The plant will be %s cm tall after 1 week" % dec(m)]
    elif kind == "start":
        m = r.randint(2, 30)
        b = r.randint(20, 400)
        q = "A linear model for the number of members of an app is <i>y</i> = %d<i>x</i> + %d, where <i>x</i> is days since launch. What does %d mean?" % (m, b, b)
        right = "There were about %d members at launch" % b
        w = ["The app gains %d members each day" % b, "There will be %d members after 1 day" % b, "The app grows by %d%% each day" % b]
    else:
        a = -r.choice([2, 3, 4, 5])
        h = r.randint(4, 12)
        k = r.randint(50, 400)
        b, c = -2 * a * h, a * h * h + k
        q = "A quadratic regression for daily profit is <i>y</i> = %s<i>x</i><sup>2</sup> + %d<i>x</i> %s %d, where <i>x</i> is the price in dollars. What is the best price, and what profit does the model predict there?" % (sg(a), b, "+" if c >= 0 else MINUS, abs(c))
        right = "$%d, with a profit of $%s" % (h, comma(k))
        w = ["$%d, with a profit of $%s" % (b, comma(k)), "$%d, with a profit of $%s" % (h, comma(abs(c))), "$%d, with a profit of $%s" % (k, comma(h))]
        return mcq(q, right, w, "The vertex is at <i>x</i> = −<i>b</i> ÷ (2<i>a</i>) = %d ÷ %d = %d. <i>y</i>(%d) = %s. <b>%s</b>." % (b, -2 * a, h, h, comma(k), right))
    return mcq(q, right, w, "<b>%s</b>." % right)


def one_judge(r):
    kind = r.choice(["r2", "r2", "extra"])
    if kind == "r2":
        vals = r.sample(range(55, 99), 3)
        names = ["Linear", "Quadratic", "Exponential"]
        r.shuffle(names)
        best = names[vals.index(max(vals))]
        lst = ", ".join("%s: <i>r</i><sup>2</sup> = 0.%02d" % (n, v) for n, v in zip(names, vals))
        q = "Three regression models were fit to the same data. %s. Which model fits the data best?" % lst
        right = best
        w = [n for n in names if n != best] + ["None of these"]
        e = "The model with <i>r</i><sup>2</sup> closest to 1 explains the most variation in the data: <b>%s</b>." % best
    else:
        lo, hi = r.choice([(0, 10), (1, 12), (0, 8), (0, 20), (5, 30)])
        inside = r.sample(range(lo + 1, hi), 2)
        far = hi + r.choice([15, 25, 40, 60])
        near = hi + 1
        q = "A model was made from data for <i>x</i> = %d to <i>x</i> = %d. Which prediction is the least reliable?" % (lo, hi)
        right = "<i>x</i> = %d" % far
        w = ["<i>x</i> = %d" % v for v in inside] + ["<i>x</i> = %d" % near]
        e = "Predicting far outside the data (extrapolation) is risky: the pattern may not continue. <b>%s</b> is the farthest from the data." % right
    return mcq(q, right, w, e)


def build():
    sets, R = build_sets([
        ("Choose a model from a table", [("collect", uniq(one_tab), 20)]),
        ("Choose a model from a situation", [("collect", uniq(one_sit), 20)]),
        ("Predict with a regression model", [("collect", uniq(one_pred), 20)]),
        ("Interpret a model", [("collect", uniq(one_int), 20)]),
        ("Judge models and predictions", [("collect", uniq(one_judge), 20)]),
    ], 69724)
    finish(sets, R)
    body = lesson("<ul><li><b>Linear</b>: the first differences are the same (a constant amount each step).</li><li><b>Quadratic</b>: the second differences are the same.</li><li><b>Exponential</b>: the ratios are the same (a constant factor or percent each step).</li><li>A calculator's regression gives the equation; <i>r</i><sup>2</sup> close to 1 means a good fit.</li><li>Predictions inside the data range are safer than predictions far outside it.</li></ul>",
        [example("<i>y</i>: 3, 6, 12, 24, 48", ["Ratios: 2, 2, 2, 2"], "Exponential: <i>y</i> = 3(2)<sup><i>x</i></sup>"), example("<i>y</i> = 1,200(1.04)<sup><i>x</i></sup>", ["1.04 = 1 + 0.04"], "4% growth each year")],
        [['Looking only at first differences', 'Check second differences and ratios too.'], ['Reading 1.06 as 106% growth', '1.06 means 6% growth.'], ['Trusting a prediction far outside the data', 'Extrapolation may not hold.']])
    faq = [('What does TEKS 2A.8A ask?', 'Analyze data to select the appropriate model from among linear, quadratic, and exponential models.'), ('What does TEKS 2A.8B ask?', 'Use regression methods available through technology to write a linear function, a quadratic function, and an exponential function from a given set of data.'), ('What does TEKS 2A.8C ask?', 'Predict and make decisions and critical judgments from a given set of data using linear, quadratic, and exponential models.'), ('What does r² mean?', 'The share of the variation in y that the model explains; closer to 1 is better.')]
    make('data-and-regression', 24, 'Data', '2A.8A, 2A.8B, 2A.8C',
         '2A.8A analyze data to select the appropriate model from among linear, quadratic, and exponential models; 2A.8B use regression methods available through technology to write a linear function, a quadratic function, and an exponential function from a given set of data; 2A.8C predict and make decisions and critical judgments from a given set of data using linear, quadratic, and exponential models',
         'Choosing Linear, Quadratic and Exponential Models', 'Data and Regression',
         'Free Algebra II data worksheets for Texas TEKS 2A.8A to 2A.8C: choose linear, quadratic or exponential models, predict with regression, interpret models and judge fits. 100 questions with answers.',
         'Same differences: linear. Same second differences: quadratic. Same ratios: exponential.', 'r² close to 1 means a good fit.',
         body, faq, sets, seo_title='Algebra II Data and Regression Models Worksheets (TEKS 2A.8A–2A.8C)')


if __name__ == "__main__":
    build()
