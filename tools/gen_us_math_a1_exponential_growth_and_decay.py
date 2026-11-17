# -*- coding: utf-8 -*-
"""
US Algebra 1: Exponential Growth and Decay (Common Core F-LE.A.1, F-LE.A.2, F-IF.C.8b)
  python3 tools/gen_us_math_a1_exponential_growth_and_decay.py
Reading the initial value and growth or decay rate from y = a(b)^x, evaluating exponential functions and
telling linear from exponential tables, writing exponential models from words and from points, compound
interest and depreciation, and comparing linear and exponential change.
Wrong answers come from real mistakes: reading b = 1.04 as a 104% or 1.04% rate, using 0.15 instead of 0.85
for a 15% decrease, adding the rate each time (linear) instead of multiplying, and multiplying a·b before
raising to the power.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, QN, fr, MINUS, usd, dec, expr
from g8_common import xy_table

R = random.Random(91201)


def d(v, places=2):
    v = round(float(v), places)
    s = ("%." + str(places) + "f") % v
    s = s.rstrip("0").rstrip(".") if "." in s else s
    whole, _, frac = s.partition(".")
    neg = whole.startswith("-")
    whole = "{:,}".format(abs(int(whole)))
    return (MINUS if neg else "") + whole + ("." + frac if frac else "")


def money(v):
    v = round(float(v), 2)
    if v == int(v):
        return "$" + "{:,}".format(int(v))
    return "$" + "{:,.2f}".format(v)


# ------------------------------------------------------------ set 1: read the model
def one_read(r):
    a = r.choice([50, 120, 200, 500, 800, 1200, 3000, 25000])
    p = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    up = r.random() < 0.55
    b = F(100 + p, 100) if up else F(100 - p, 100)
    v = r.choice(["t", "x"])
    f = "<i>y</i> = %s(%s)<sup><i>%s</i></sup>" % (num(a), dec(b), v)
    kind = r.choice(["type", "rate", "init"])
    if kind == "type":
        q = "Does %s show exponential growth or decay?" % B(f)
        right = "Growth, because %s &gt; 1" % dec(b) if up else "Decay, because %s &lt; 1" % dec(b)
        wr = ["Decay, because %s &lt; 1" % dec(b) if up else "Growth, because %s &gt; 1" % dec(b), "Growth, because %s is positive" % num(a), "Neither, it is linear"]
        e = "The base <i>b</i> = %s is %s 1, so it is <b>%s</b>." % (dec(b), "greater than" if up else "less than", "growth" if up else "decay")
    elif kind == "rate":
        q = "What is the %s rate for %s?" % ("growth" if up else "decay", B(f))
        right = "%d%%" % p
        wr = ["%s%%" % dec(b * 100) if up else "%d%%" % (100 - p), "%s%%" % dec(b), "%d%%" % (p * 10) if p * 10 < 100 else "%d%%" % (p + 1)]
        e = "<i>b</i> = 1 %s <i>r</i>, so <i>r</i> = %s = <b>%d%%</b>." % ("+" if up else MINUS, dec(abs(b - 1)), p)
    else:
        q = "What is the initial value of %s?" % B(f)
        right = num(a)
        wr = [num(a * b) if (a * b).denominator == 1 else d(a * b), dec(b), num(a * (p if up else 1) // 1) if False else num(a + p)]
        e = "When <i>%s</i> = 0, <i>b</i><sup>0</sup> = 1, so <i>y</i> = <i>a</i> = <b>%s</b>." % (v, num(a))
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: evaluate and tables
def one_eval(r):
    kind = r.choice(["eval", "eval", "table", "next"])
    if kind == "eval":
        a = r.choice([2, 3, 4, 5, 10, 64, 81, 100, 160])
        b = r.choice([F(2), F(3), F(1, 2), F(3, 2), F(1, 4), F(1, 3)])
        x = r.choice([2, 3, 4, -1, 0])
        val = a * b ** x
        if val.denominator != 1 or val > 100000:
            return None
        bs = num(b) if b.denominator == 1 else fr(b.numerator, b.denominator)
        q = "If %s, find %s." % (B("<i>f</i>(<i>x</i>) = %s(%s)<sup><i>x</i></sup>" % (num(a), bs)), B("<i>f</i>(%s)" % num(x)))
        wrong1 = (a * b) ** x if x != 0 else a * b
        wr = [wrong1, a * b * x if x else 0, a + b * x if (a + b * x).denominator == 1 else a * b]
        wr = [w for w in wr if F(w) != val and abs(F(w)) < 100000]
        e = "Raise the base to the power first: (%s)<sup>%s</sup> = %s. Then multiply by %s: <b>%s</b>." % (bs, num(x), num(b ** x) if (b ** x).denominator == 1 else fr((b ** x).numerator, (b ** x).denominator), num(a), num(val))
        return QN(q, val, [w for w in wr if F(w).denominator == 1], e)
    if kind == "table":
        lin = r.random() < 0.5
        a = r.choice([2, 3, 4, 5])
        k = r.choice([2, 3])
        xs = [0, 1, 2, 3, 4]
        ys = [a + k * x for x in xs] if lin else [a * k ** x for x in xs]
        q = "Is the relationship in the table linear or exponential?%s" % xy_table([num(x) for x in xs], [num(y) for y in ys])
        right = "Linear: it adds %d each time" % k if lin else "Exponential: it multiplies by %d each time" % k
        wr = ["Exponential: it multiplies by %d each time" % k if lin else "Linear: it adds %d each time" % (ys[1] - ys[0]), "Linear: it adds %d each time" % (ys[2] - ys[1]) if not lin else "Exponential: it adds %d each time" % k,
              "Neither: the outputs keep changing"]
        e = ("Each output is %d more than the one before: a constant <b>difference</b> means <b>linear</b>." % k) if lin else (
            "Each output is %d times the one before: a constant <b>ratio</b> means <b>exponential</b>." % k)
        wr = [w for w in dict.fromkeys(wr) if w != right]
        return T(q, right, wr[:3], e)
    a = r.choice([3, 5, 6, 8, 10, 12])
    k = r.choice([2, 3, 4])
    ys = [a * k ** i for i in range(4)]
    q = "The table shows an exponential function. What is the next output?%s" % xy_table(["0", "1", "2", "3", "4"], [num(y) for y in ys] + ["?"])
    nxt = ys[-1] * k
    return QN(q, nxt, [ys[-1] + (ys[-1] - ys[-2]), ys[-1] * 2 if k != 2 else ys[-1] * 3, ys[-1] + k], "Each output is multiplied by %d: %s × %d = <b>%s</b>." % (k, num(ys[-1]), k, num(nxt)))


# ------------------------------------------------------------ set 3: write the model
CONTEXTS_UP = [("A town has a population of {a} and grows by {p}% each year.", "<i>P</i>", "<i>t</i>"),
               ("A savings account starts with ${a} and earns {p}% interest compounded yearly.", "<i>A</i>", "<i>t</i>"),
               ("A video has {a} views and the views grow by {p}% each day.", "<i>V</i>", "<i>d</i>")]
CONTEXTS_DOWN = [("A car is bought for ${a} and loses {p}% of its value each year.", "<i>V</i>", "<i>t</i>"),
                 ("A lake has {a} fish and the number falls by {p}% each year.", "<i>F</i>", "<i>t</i>"),
                 ("A {a} mg dose of medicine leaves the body at {p}% per hour.", "<i>M</i>", "<i>h</i>")]


def one_write(r):
    if r.random() < 0.7:
        up = r.random() < 0.5
        tmpl, Y, Xv = r.choice(CONTEXTS_UP if up else CONTEXTS_DOWN)
        a = r.choice([200, 500, 1200, 2500, 8000, 15000, 24000]) if "$" in tmpl or "population" in tmpl or "views" in tmpl or "fish" in tmpl else r.choice([200, 400, 500, 800])
        p = r.choice([3, 4, 5, 8, 10, 12, 15, 20, 25])
        b = F(100 + p, 100) if up else F(100 - p, 100)
        q = tmpl.format(a="{:,}".format(a), p=p) + " Which function models the situation?"
        right = "%s = %s(%s)<sup>%s</sup>" % (Y, "{:,}".format(a), dec(b), Xv)
        wr = ["%s = %s(%s)<sup>%s</sup>" % (Y, "{:,}".format(a), dec(F(p, 100)), Xv),
              "%s = %s(%s)<sup>%s</sup>" % (Y, "{:,}".format(a), dec(F(100 - p, 100) if up else F(100 + p, 100)), Xv),
              "%s = %s %s %d%s" % (Y, "{:,}".format(a), "+" if up else MINUS, p, Xv)]
        e = "Start value %s; multiply by 1 %s %s = %s each %s: <b>%s</b>." % ("{:,}".format(a), "+" if up else MINUS, dec(F(p, 100)), dec(b), "period", right)
        return T(q, right, wr, e)
    a = r.choice([2, 3, 4, 5, 6])
    b = r.choice([2, 3, 4])
    y1, y2 = a * b, a * b ** 2
    q = "An exponential function <i>y</i> = <i>a</i>(<i>b</i>)<sup><i>x</i></sup> passes through %s and %s. What is the function?" % (B("(1, %s)" % num(y1)), B("(2, %s)" % num(y2)))
    right = "<i>y</i> = %s(%s)<sup><i>x</i></sup>" % (num(a), num(b))
    wr = ["<i>y</i> = %s(%s)<sup><i>x</i></sup>" % (num(y1), num(b)), "<i>y</i> = %s(%s)<sup><i>x</i></sup>" % (num(b), num(a)) if a != b else "<i>y</i> = %s(%s)<sup><i>x</i></sup>" % (num(a), num(b + 1)),
          "<i>y</i> = %s" % expr([(y2 - y1, "<i>x</i>"), (2 * y1 - y2, "")])]
    e = "The ratio is %s ÷ %s = %s, so <i>b</i> = %s. Then <i>a</i> = %s ÷ %s = %s. <b>%s</b>." % (num(y2), num(y1), num(b), num(b), num(y1), num(b), num(a), right)
    return T(q, right, [w for w in dict.fromkeys(wr) if w != right][:3], e)


# ------------------------------------------------------------ set 4: compound interest and depreciation
def one_money(r):
    up = r.random() < 0.55
    P = r.choice([500, 1000, 1500, 2000, 2500, 4000, 5000, 8000, 12000, 18000, 25000])
    p = r.choice([2, 3, 4, 5, 6, 8]) if up else r.choice([10, 12, 15, 20, 25])
    n = r.choice([2, 3, 4, 5])
    b = (1 + p / 100) if up else (1 - p / 100)
    val = P * b ** n
    if up:
        q = "%s is invested at %d%% interest compounded yearly. What is it worth after %d years?" % (money(P), p, n)
        simple = P * (1 + p / 100 * n)
        wr = [money(simple), money(P * (p / 100) ** n * 0 + P * (1 + p / 100) ** (n - 1)), money(P * b * n)]
        e = "Use <i>A</i> = <i>P</i>(1 + <i>r</i>)<sup><i>t</i></sup>: %s × %s<sup>%d</sup> = <b>%s</b>." % (money(P), d(b, 2), n, money(val))
    else:
        q = "A machine bought for %s loses %d%% of its value each year. What is it worth after %d years?" % (money(P), p, n)
        lin = P * (1 - p / 100 * n)
        wr = [money(lin), money(P * (p / 100) ** n) if P * (p / 100) ** n > 1 else money(P * b ** (n + 1)), money(P * b ** (n - 1))]
        e = "Multiply by 1 − %s = %s each year: %s × %s<sup>%d</sup> = <b>%s</b>." % (d(p / 100), d(b), money(P), d(b), n, money(val))
    right = money(val)
    wr = [w for w in dict.fromkeys(wr) if w != right and w not in ("$0", "$0.00") and not w.startswith("$-")]
    if len(wr) < 3:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("Plan A pays $100 on day 1 and $100 more each day. Plan B pays 1¢ on day 1 and doubles each day. Which pays more on day 20?", "Plan B", ["Plan A", "They pay the same", "Neither pays anything on day 20"],
         "Plan A: $2,000. Plan B: 0.01 × 2<sup>19</sup> ≈ $5,243. Exponential growth eventually passes linear growth: <b>Plan B</b>."),
        ("A radioactive sample of 80 g has a half-life of 5 years. How much is left after 15 years?", "10 g", ["20 g", "40 g", "26.7 g"], "15 years is 3 half-lives: 80 → 40 → 20 → <b>10 g</b>."),
        ("Which function grows faster in the long run: <i>f</i>(<i>x</i>) = 50<i>x</i> or <i>g</i>(<i>x</i>) = 2<sup><i>x</i></sup>?", "<i>g</i>(<i>x</i>) = 2<sup><i>x</i></sup>", ["<i>f</i>(<i>x</i>) = 50<i>x</i>", "They grow at the same rate", "Neither grows"],
         "An exponential function eventually grows faster than any linear one: <b><i>g</i>(<i>x</i>)</b>."),
        ("A population doubles every 10 years. It is 3,000 now. What will it be in 30 years?", "24,000", ["9,000", "18,000", "6,000"], "3 doublings: 3,000 × 2<sup>3</sup> = <b>24,000</b>."),
        ("<i>y</i> = 2,000(0.9)<sup><i>t</i></sup> models a car's value. By what percent does the value fall each year?", "10%", ["90%", "0.9%", "9%"], "<i>b</i> = 0.9 = 1 − 0.1, so it falls <b>10%</b> a year."),
        ("A phone's value is modeled by <i>V</i> = 800(0.75)<sup><i>t</i></sup>. What is it worth after 2 years?", "$450", ["$400", "$600", "$1,200"], "800 × 0.75<sup>2</sup> = 800 × 0.5625 = <b>$450</b>."),
        ("Which table shows exponential decay?", "1, ½, ¼, ⅛", ["10, 8, 6, 4", "2, 4, 8, 16", "5, 5, 5, 5"], "Each value is half the one before: a constant ratio less than 1, so <b>decay</b>."),
        ("A bacteria culture triples every hour. It starts with 40 bacteria. Which function gives the number after <i>h</i> hours?", "<i>N</i> = 40(3)<sup><i>h</i></sup>",
         ["<i>N</i> = 40 + 3<i>h</i>", "<i>N</i> = 3(40)<sup><i>h</i></sup>", "<i>N</i> = 120<sup><i>h</i></sup>"], "Start at 40 and multiply by 3 each hour: <b><i>N</i> = 40(3)<sup><i>h</i></sup></b>."),
        ("$1,000 earns 6% interest compounded yearly. Which expression gives the interest earned (not the total) after 4 years?", "1,000(1.06)<sup>4</sup> − 1,000", ["1,000(0.06)<sup>4</sup>", "1,000(1.06)<sup>4</sup>", "1,000 × 0.06 × 4"],
         "The total is 1,000(1.06)<sup>4</sup>; subtract the starting $1,000 to get <b>the interest</b>."),
        ("Which is the better deal for savings after 10 years: 5% simple interest or 5% interest compounded yearly?", "Compound interest", ["Simple interest", "They are the same", "It depends on the starting amount"],
         "Compound interest earns interest on interest, so it is <b>always more</b> after the first year."),
        ("Which has the greater initial value: <i>f</i>(<i>x</i>) = 300(1.02)<sup><i>x</i></sup> or <i>g</i>(<i>x</i>) = 250(1.08)<sup><i>x</i></sup>?", "<i>f</i>", ["<i>g</i>", "They are equal", "You cannot tell"],
         "The initial values are 300 and 250: <b><i>f</i></b>. (But <i>g</i> grows faster.)"),
        ("A ball bounces to 60% of its previous height. It is dropped from 10 ft. How high does it go on the 3rd bounce?", "2.16 ft", ["3.6 ft", "6 ft", "1.8 ft"], "10 × 0.6<sup>3</sup> = <b>2.16 ft</b>."),
        ("Is <i>y</i> = 4<i>x</i><sup>2</sup> an exponential function?", "No, the variable is not in the exponent", ["Yes, it has an exponent", "Yes, because 4 &gt; 1", "No, because 4 is even"],
         "In an exponential function the variable is the exponent, as in 4(2)<sup><i>x</i></sup>. Here it is the base: <b>no</b>."),
        ("A town's population is 12,000 and falls 2% a year. Which expression gives the population after 5 years?", "12,000(0.98)<sup>5</sup>", ["12,000(0.02)<sup>5</sup>", "12,000(1.02)<sup>5</sup>", "12,000 − 0.02 × 5"],
         "Decreasing by 2% leaves 98%: <b>12,000(0.98)<sup>5</sup></b>."),
        ("Why is 1.05<sup><i>t</i></sup> used for 5% growth, not 0.05<sup><i>t</i></sup>?", "You keep 100% and add 5%, so you multiply by 1.05", ["0.05 is too small to type", "1.05 is the decay factor", "Both mean the same thing"],
         "Each year the amount is 100% + 5% = 105% of the year before: <b>multiply by 1.05</b>."),
        ("<i>f</i>(<i>x</i>) = 5(2)<sup><i>x</i></sup>. What is <i>f</i>(0)?", "5", ["0", "10", "1"], "2<sup>0</sup> = 1, so <i>f</i>(0) = 5 × 1 = <b>5</b>."),
        ("A computer loses half its value every 2 years. It costs $1,600. What is it worth after 6 years?", "$200", ["$400", "$800", "$100"], "6 years is 3 halvings: 1,600 → 800 → 400 → <b>$200</b>."),
        ("Which situation is exponential?", "A price rises 3% every year", ["A tank fills with 3 gallons every minute", "A taxi charges $3 per mile", "A plant grows 3 cm each week"],
         "A percent change multiplies by the same number each time: <b>a price rising 3% a year</b>."),
        ("An investment is modeled by <i>A</i> = 2,500(1.04)<sup><i>t</i></sup>. About how much is it worth after 10 years?", "$3,700", ["$3,500", "$2,600", "$10,000"], "2,500 × 1.04<sup>10</sup> ≈ 2,500 × 1.48 ≈ <b>$3,700</b>."),
        ("Average rate of change of <i>f</i>(<i>x</i>) = 2<sup><i>x</i></sup> from <i>x</i> = 1 to <i>x</i> = 3 is…", "3", ["2", "4", "6"], "(<i>f</i>(3) − <i>f</i>(1)) ÷ (3 − 1) = (8 − 2) ÷ 2 = <b>3</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>An <b>exponential function</b> has the form <i>y</i> = <i>a</i>(<i>b</i>)<sup><i>x</i></sup>. <i>a</i> is the <b>initial value</b> "
        "(when <i>x</i> = 0) and <i>b</i> is the number you <b>multiply by</b> each step. If <i>b</i> &gt; 1 it is growth; if 0 &lt; <i>b</i> &lt; 1 it is decay.</p>"
        "<p>For a percent change, <i>b</i> = 1 + <i>r</i> (growth) or <i>b</i> = 1 − <i>r</i> (decay): 6% growth → 1.06; 15% decay → 0.85. "
        "Compound interest: <i>A</i> = <i>P</i>(1 + <i>r</i>)<sup><i>t</i></sup>.</p>"
        "<p>Linear functions <b>add</b> the same amount each step; exponential functions <b>multiply</b> by the same amount.</p>",
        [("Write a model: 600 rabbits, growing 8% a year.", ["<i>a</i> = 600, <i>b</i> = 1.08."], "<i>y</i> = 600(1.08)<sup><i>t</i></sup>"),
         ("A $20,000 car loses 15% a year. Value after 3 years?", ["<i>b</i> = 0.85.", "20,000 × 0.85<sup>3</sup> = 20,000 × 0.614125."], "$12,282.50"),
         ("Find <i>f</i>(3) for <i>f</i>(<i>x</i>) = 4(3)<sup><i>x</i></sup>.", ["3<sup>3</sup> = 27 first.", "4 × 27."], "108")],
        ["Using 0.15 for a 15% decrease. The value left is 85%, so use 0.85.",
         "Reading <i>b</i> = 1.04 as a 104% rate. The rate is 0.04 = 4%.",
         "Adding the rate each year (linear) instead of multiplying.",
         "Multiplying <i>a</i> × <i>b</i> first: 4(3)<sup>3</sup> is 4 × 27, not 12<sup>3</sup>."])


def main():
    sets = [S("Read an exponential model", collect(one_read, 20, R)),
            S("Evaluate and compare tables", collect(one_eval, 20, R)),
            S("Write an exponential model", collect(one_write, 20, R)),
            S("Compound interest and depreciation", collect(one_money, 20, R)),
            S("Exponential growth and decay problems", problems())]
    make("exponential-growth-and-decay", 12, "F-LE.A.2",
         "Exponential Growth and Decay: Functions, Compound Interest and Models",
         "Algebra 1 Exponential Growth and Decay Worksheets: Exponential Functions and Compound Interest (Free, Answer Key)",
         "Exponential growth and decay",
         "Construct linear and exponential functions, including arithmetic and geometric sequences, given a graph, a description of a relationship, "
         "or two input-output pairs (include reading these from a table).",
         "Free Algebra 1 exponential growth and decay worksheets (F-LE.A.1, F-LE.A.2, F-IF.C.8b): read y = a(b)^x, evaluate exponential "
         "functions, linear vs exponential tables, write models, compound interest and depreciation. 100 questions with an answer key.",
         "y = a(b)^x: start at a and multiply by b each step.",
         "Growth: b = 1 + r. Decay: b = 1 − r. Linear adds; exponential multiplies.",
         body(),
         [("How do you tell exponential growth from decay?", "Look at the base b in y = a(b)^x. If b is greater than 1 it is growth; if b is between 0 and 1 it is decay."),
          ("How do you find the growth rate from y = 500(1.04)^t?", "Subtract 1 from the base: 1.04 − 1 = 0.04, so the growth rate is 4% per period."),
          ("What is the compound interest formula?", "A = P(1 + r)^t, where P is the starting amount, r is the yearly rate as a decimal and t is the number of years."),
          ("How can I tell if a table is linear or exponential?", "If the outputs go up by the same amount each step it is linear; if they are multiplied by the same number each step it is exponential.")],
         sets, R, domain="Exponents & Exponential Functions")


if __name__ == "__main__":
    main()
