# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Proportional Relationships (7.RP.A.2)
  python tools/gen_us_math_g7_proportional_relationships.py
Tables, graphs and equations y = kx. Wrong answers come from real mistakes: dividing x by y
(the reciprocal of k), using a difference instead of a ratio, calling any straight line
proportional (even when it misses the origin), and reading the point (k, 1) instead of (1, k).
"""
import random
from fractions import Fraction as F
from ws_common import (num, nums, mcq, balance, People, B, fig, figure, svg_wrap, text, line, table, example,
                       write_unit, GREEN, BLUE, RED, INK, GRAY, fr)

R = random.Random(70401)
UPDATED = "2026-11-09"
Y = "<i>y</i>"
X = "<i>x</i>"


def n(v, st="d"):
    s = num(v, st)
    return s if s is not None else num(v, "f")


def htable(xs, ys, xl="<i>x</i>", yl="<i>y</i>"):
    """Small horizontal table for a question."""
    def row(label, vals):
        return "<tr><th>%s</th>%s</tr>" % (label, "".join("<td>%s</td>" % n(v) for v in vals))
    return "<div class='sn-tw'><table class='sn-table'>%s%s</table></div>" % (row(xl, xs), row(yl, ys))


def graph(points, xmax, ymax, ystep=1, label="graph", line_through=None, xlab="x", ylab="y"):
    """First-quadrant graph. points: [(x, y)]. line_through: (x1, y1, x2, y2) drawn as a line."""
    W, H, L, B_, T = 300, 260, 40, 34, 14
    pw, ph = W - L - 14, H - B_ - T
    sx = lambda v: L + float(v) * pw / xmax
    sy = lambda v: H - B_ - float(v) * ph / ymax
    s = []
    for i in range(0, xmax + 1):
        s.append(line(sx(i), sy(0), sx(i), sy(ymax), GRAY, 1))
        s.append(text(sx(i), H - B_ + 16, str(i), 12, weight=400))
    for j in range(0, ymax + 1, ystep):
        s.append(line(sx(0), sy(j), sx(xmax), sy(j), GRAY, 1))
        s.append(text(L - 6, sy(j) + 4, str(j), 12, "end", weight=400))
    s.append(line(sx(0), sy(0), sx(xmax), sy(0), INK, 2))
    s.append(line(sx(0), sy(0), sx(0), sy(ymax), INK, 2))
    s.append(text(sx(xmax) - 2, H - 4, xlab, 13, "end", italic=True))
    s.append(text(L - 26, T + 4, ylab, 13, "start", italic=True))
    if line_through:
        x1, y1, x2, y2 = line_through
        s.append(line(sx(x1), sy(y1), sx(x2), sy(y2), BLUE, 2.5))
    for x, y in points:
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (sx(x), sy(y), GREEN))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1
def set_tables():
    its = []
    cases = [([1, 2, 3, 4], [4, 8, 12, 16], True), ([1, 2, 3, 4], [3, 5, 7, 9], False), ([2, 4, 6, 8], [5, 10, 15, 20], True),
             ([1, 3, 5, 7], [6, 18, 30, 42], True), ([2, 3, 4, 5], [6, 8, 10, 12], False), ([3, 6, 9, 12], [2, 4, 6, 8], True),
             ([1, 2, 4, 5], [7, 14, 28, 36], False), ([4, 8, 10, 12], [10, 20, 25, 30], True),
             ([1, 2, 3, 4], [9, 18, 27, 36], True), ([0, 1, 2, 3], [4, 6, 8, 10], False), ([5, 10, 15, 20], [3, 6, 9, 12], True), ([2, 4, 5, 10], [3, 6, 8, 15], False)]
    for xs, ys, ok in cases:
        rs = [F(y, x) if x else None for x, y in zip(xs, ys)]
        if xs[0] == 0:
            e = "When x = 0, y = %d. A proportional relationship must have y = 0 when x = 0, so it is not proportional." % ys[0]
        elif ok:
            e = "Every ratio y ÷ x is %s (%s ÷ %d = %s, %s ÷ %d = %s), so the ratios are equal and the relationship is proportional." % (
                n(rs[0]), ys[0], xs[0], n(rs[0]), ys[-1], xs[-1], n(rs[-1]))
        else:
            bad = next(i for i in range(4) if rs[i] != rs[0])
            e = "%d ÷ %d = %s but %d ÷ %d = %s. The ratios y ÷ x are not equal, so it is not proportional." % (
                ys[0], xs[0], n(rs[0]), ys[bad], xs[bad], n(rs[bad]))
            if all(ys[i + 1] - ys[i] == ys[1] - ys[0] for i in range(3)) and xs[1] - xs[0] == 1:
                e += " The y-values go up by the same amount, but that alone does not make it proportional."
        good = "Yes, the ratios y ÷ x are all equal." if ok else "No, the ratios y ÷ x are not all equal."
        its.append(mcq("Is the relationship in the table proportional?" + htable(xs, ys), (good, ok),
                       [("No, the ratios y ÷ x are not all equal." if ok else "Yes, the ratios y ÷ x are all equal.", not ok),
                        ("Yes, because y always goes up.", "up"), ("No, because the x-values skip numbers.", "skip")], e))
    # missing value in a proportional table
    for xs, ys, i in [([2, 5, 8], [6, 15, 24], 2), ([3, 6, 10], [12, 24, 40], 2), ([4, 7, 12], [10, F(35, 2), 30], 2),
                      ([5, 8, 11], [15, 24, 33], 1), ([2, 6, 9], [7, 21, F(63, 2)], 2), ([6, 9, 15], [4, 6, 10], 2)]:
        k = F(ys[0], xs[0])
        ans = ys[i]
        show = list(ys)
        show_html = [n(v) for v in show]
        show_html[i] = "?"
        tbl = "<div class='sn-tw'><table class='sn-table'><tr><th><i>x</i></th>%s</tr><tr><th><i>y</i></th>%s</tr></table></div>" % (
            "".join("<td>%d</td>" % v for v in xs), "".join("<td>%s</td>" % v for v in show_html))
        diff = ys[0] - xs[0]
        ws = [xs[i] + diff, xs[i] / k, ans + k, ans - k]
        e = "The constant of proportionality is %s ÷ %d = %s. So y = %s × %d = %s." % (n(ys[0]), xs[0], n(k), n(k), xs[i], n(ans))
        e += " Not %s: adding %s each time uses a difference, not a ratio." % (n(xs[i] + diff), n(diff))
        its.append(mcq("The table shows a proportional relationship. What is the missing value?" + tbl, (n(ans), F(ans)),
                       [(n(w), F(w)) for w in ws], e))
    # pick the proportional table
    its.append(mcq("Which relationship is proportional?", ("Cost of apples at $2 per pound", "a"),
                   [("A $5 entry fee plus $2 per ride", "b"), ("Your age and your height", "c"), ("A taxi ride: $3 plus $1 per mile", "d")],
                   "$2 per pound means cost = 2 × pounds. 0 pounds costs $0 and the ratio is always 2. A starting fee breaks proportionality."))
    its.append(mcq("Which relationship is <b>not</b> proportional?", ("A gym: $30 to join plus $20 a month", "a"),
                   [("Miles driven at 50 miles per hour", "b"), ("Earnings at $12 per hour", "c"), ("Total legs on some spiders, at 8 legs per spider", "d")],
                   "With a $30 joining fee, 1 month costs $50 and 2 months cost $70. 50 ÷ 1 ≠ 70 ÷ 2, so it is not proportional."))
    return {"title": "Is it proportional? Tables", "items": its}


# ------------------------------------------------------------ set 2
def set_constant():
    its = []
    for xs, ys in [([2, 4, 6], [10, 20, 30]), ([3, 6, 9], [21, 42, 63]), ([4, 8, 12], [6, 12, 18]), ([5, 10, 15], [2, 4, 6]),
                   ([2, 5, 7], [9, F(45, 2), F(63, 2)]), ([10, 20, 30], [35, 70, 105]), ([8, 12, 20], [2, 3, 5]), ([3, 5, 8], [F("2.4"), 4, F("6.4")])]:
        k = F(ys[0]) / xs[0]
        recip = F(xs[0]) / F(ys[0])
        ws = [recip, F(ys[0]) - xs[0], F(ys[1]) - F(ys[0]), k * 2]
        e = "Divide y by x: %s ÷ %d = %s. Check another pair: %s ÷ %d = %s. Not %s: that divides x by y." % (
            n(ys[0]), xs[0], n(k), n(ys[1]), xs[1], n(F(ys[1]) / xs[1]), n(recip))
        its.append(mcq("What is the constant of proportionality (y ÷ x) in this table?" + htable(xs, ys), (n(k), k),
                       [(n(w), w) for w in ws], e))
    words = [("A car travels 150 miles in 3 hours.", "miles per hour", 150, 3),
             ("Ruby earns $96 for 8 hours of work.", "dollars per hour", 96, 8),
             ("A recipe uses 6 cups of flour for 4 batches.", "cups per batch", 6, 4),
             ("A printer prints 84 pages in 4 minutes.", "pages per minute", 84, 4),
             ("12 pencils cost $3.", "dollars per pencil", 3, 12),
             ("A runner goes 5 kilometers in 25 minutes.", "kilometers per minute", 5, 25)]
    for s, unit, top, bot in words:
        k, rec = F(top, bot), F(bot, top)
        e = ("The constant of proportionality is the unit rate in %s: %d ÷ %d = %s. Not %s: that is the rate the other way around."
             % (unit, top, bot, n(k), n(rec)))
        its.append(mcq("%s What is the constant of proportionality in %s?" % (s, unit), (n(k), F(k)),
                       nums([rec, F(k) * 2, F(k) + 1], "d") + nums([rec, F(k) * 2, F(k) + 1], "f"), e))
    # unit rate with fractions
    for a, b, k in [(F(1, 2), F(3, 4), F(3, 2)), (F(2, 3), 4, 6), (F(3, 4), F(1, 2), F(2, 3)), (F(1, 4), 3, 12),
                    (F(5, 6), F(5, 3), 2), (F(1, 3), F(1, 2), F(3, 2))]:
        e = "Constant = y ÷ x = %s ÷ %s = %s." % (num(b, "f"), num(a, "f"), num(k, "f"))
        its.append(mcq("A proportional relationship has y = %s when x = %s. What is the constant of proportionality?" % (num(b, "f"), num(a, "f")),
                       (num(k, "f"), k), nums([F(1) / k, a * b, b - a, k + 1], "f"), e + " Not %s: that is x ÷ y." % num(F(1) / k, "f")))
    return {"title": "The constant of proportionality", "items": its}


# ------------------------------------------------------------ set 3
def set_graphs():
    its = []
    # read k from a graph through the origin
    for k, xmax, ymax, ystep in [(2, 6, 12, 2), (3, 5, 15, 3), (4, 5, 20, 4), (F(1, 2), 8, 4, 1), (5, 4, 20, 5), (F(3, 2), 6, 9, 1),
                                 (6, 4, 24, 6), (F(5, 2), 4, 10, 1)]:
        pts = [(x, k * x) for x in range(1, xmax + 1) if (k * x).denominator == 1 and k * x <= ymax][:3]
        svg = graph(pts, xmax, ymax, ystep, "graph of a line through the origin with points", (0, 0, xmax, min(ymax, k * xmax)))
        e = "The line goes through (0, 0) and (%s, %s). The constant is y ÷ x = %s ÷ %s = %s. It is the y-value when x = 1." % (
            pts[0][0], n(pts[0][1]), n(pts[0][1]), pts[0][0], n(k))
        its.append(mcq("The graph shows a proportional relationship. What is the constant of proportionality?" + fig(svg),
                       (n(k), F(k)), [(n(w), w) for w in [1 / F(k), F(k) * 2, F(k) + 1, F(k) + 2]],
                       e + " Not %s: that is x ÷ y." % n(1 / F(k))))
    # is the graph proportional
    gcases = [("through", (0, 0, 6, 12), True, "It is a straight line through the origin (0, 0)."),
              ("misses", (0, 2, 6, 14), False, "It is a straight line, but it does not go through (0, 0): when x = 0, y = 2."),
              ("curve", None, False, "The points do not lie on a straight line, so the ratios are not equal."),
              ("through2", (0, 0, 6, 6), True, "It is a straight line through the origin (0, 0).")]
    for kind, lt, ok, why in gcases:
        if kind == "curve":
            pts = [(1, 1), (2, 4), (3, 9), (4, 16)]
            svg = graph(pts, 6, 18, 3, "graph of points on a curve")
        else:
            x1, y1, x2, y2 = lt
            pts = [(x, y1 + (y2 - y1) * x // 6) for x in (1, 2, 4)]
            svg = graph(pts, 6, 14 if kind != "through" else 12, 2, "graph of a straight line", lt)
        good = "Yes" if ok else "No"
        its.append(mcq("Does the graph show a proportional relationship?" + fig(svg), (good, ok),
                       [("No" if ok else "Yes", not ok), ("Only if the line is steep", "s"), ("Yes, any straight line is proportional", "any") if ok else ("Only if it starts at x = 1", "one")],
                       why + (" Both are needed: a straight line and through (0, 0)." if not ok else "")))
    # meaning of a point
    pts_mean = [((1, 8), "hours worked", "dollars earned", "You earn $8 for 1 hour of work. This is the unit rate.", "You work 8 hours for $1."),
                ((0, 0), "pounds of rice", "cost in dollars", "0 pounds of rice cost $0.", "Rice costs $0 per pound."),
                ((4, 60), "hours", "miles", "In 4 hours you travel 60 miles.", "In 60 hours you travel 4 miles."),
                ((1, 3), "packs", "cans of juice", "Each pack has 3 cans. This is the unit rate.", "Each can has 3 packs.")]
    for (x, y), xl, yl, good, bad in pts_mean:
        its.append(mcq("A proportional graph shows %s (x) and %s (y). What does the point (%d, %d) mean?" % (xl, yl, x, y), (good, "g"),
                       [(bad, "b"), ("The line is %d units long." % (x + y), "c"), ("The constant of proportionality is %d." % (x + y), "d")],
                       "The first number is x (%s) and the second is y (%s)." % (xl, yl)))
    # find a point on the line
    for k, xq in [(6, 5), (F(5, 2), 4), (8, 3), (F(3, 4), 8)]:
        its.append(mcq("A proportional relationship has a constant of %s. Which point is on its graph?" % n(k),
                       ("(%d, %s)" % (xq, n(k * xq)), "a"),
                       [("(%s, %d)" % (n(k * xq), xq), "b"), ("(%d, %s)" % (xq, n(k + xq)), "c"), ("(%d, %s)" % (xq, n(F(xq) / k)), "d")],
                       "On the graph, y = %s × x. When x = %d, y = %s × %d = %s." % (n(k), xq, n(k), xq, n(k * xq))))
    return {"title": "Graphs of proportional relationships", "items": its}


# ------------------------------------------------------------ set 4
def set_equations():
    its = []
    for xs, ys in [([2, 4, 6], [14, 28, 42]), ([2, 4, 6], [3, 6, 9]), ([5, 10, 15], [3, 6, 9]), ([4, 6, 8], [10, 15, 20])]:
        k = F(ys[0], xs[0])
        its.append(mcq("Which equation describes the table?" + htable(xs, ys), ("y = %sx" % n(k), "a"),
                       [("y = %sx" % (num(1 / k) or fr((1 / k).numerator, (1 / k).denominator)), "b"), ("y = x %s %s" % ("+" if ys[0] >= xs[0] else "−", n(abs(ys[0] - xs[0]))), "c"), ("x = %sy" % n(k), "d")],
                       "k = y ÷ x = %d ÷ %d = %s, so y = %sx. Check: %s × %d = %d." % (ys[0], xs[0], n(k), n(k), n(k), xs[1], ys[1])))
    for s, eq, bad in [("Tickets cost $9 each. c is the cost of t tickets.", "c = 9t", ["t = 9c", "c = t + 9", "c = 9 + t"]),
                       ("A plant grows 2.5 cm each week. h is the growth in w weeks.", "h = 2.5w", ["w = 2.5h", "h = w + 2.5", "h = 2.5 ÷ w"]),
                       ("There are 12 eggs in a carton. e is the number of eggs in c cartons.", "e = 12c", ["c = 12e", "e = c + 12", "e = c ÷ 12"]),
                       ("A cyclist rides at 15 miles per hour. d is the distance in h hours.", "d = 15h", ["h = 15d", "d = h + 15", "d = 15 ÷ h"])]:
        its.append(mcq("%s Which equation is correct?" % s, (eq, "a"), [(b, b) for b in bad],
                       "In a proportional relationship, total = constant × amount. So %s." % eq))
    for k, x in [(8, 7), (F("2.5"), 12), (F(3, 4), 20), (14, 6), (F("0.4"), 35), (F(5, 2), 9)]:
        y = k * x
        its.append(mcq("If y = %sx, what is y when x = %d?" % (n(k), x), (n(y), y), nums([F(x) / k, k + x, y + k], "d") + nums([F(x) / k, k + x, y + k], "f"),
                       "Multiply: y = %s × %d = %s." % (n(k), x, n(y))))
    for k, y in [(6, 54), (F("1.5"), 18), (F(2, 3), 12), (12, 84), (F("0.8"), 20), (25, 175)]:
        x = F(y) / k
        its.append(mcq("If y = %sx, what is x when y = %d?" % (n(k), y), (n(x), x), nums([y * k, y - k, x + 1], "d") + nums([y * k, y - k, x + 1], "f"),
                       "Divide: x = %d ÷ %s = %s. Check: %s × %s = %d. Not %s: that multiplies instead of dividing." % (y, n(k), n(x), n(k), n(x), y, n(y * k))))
    return {"title": "Equations y = kx", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)

    def item(q, v, ws, e, unit="", st="d"):
        sh = (lambda w: num(w, "f")) if st == "f" else n
        cands = [(sh(F(w)) + unit, F(w)) for w in ws + [F(v) + 1, F(v) * 2]]
        its.append(mcq(q, (sh(F(v)) + unit, F(v)), cands, e))

    name, he, his = P.next()
    item("%s earns $72 for 6 hours of babysitting. At this rate, how much will %s earn for 10 hours?" % (name, he), 120, [76, 720, 82],
         "Unit rate: 72 ÷ 6 = $12 per hour. 12 × 10 = $120. Not $76: adding 4 more hours to $72 uses a difference, not a ratio.", "")
    its[-1]["c"] = ["$" + c for c in its[-1]["c"]]
    item("A car uses 4 gallons of gas to go 128 miles. How far can it go on 7 gallons?", 224, [131, 32, 896],
         "128 ÷ 4 = 32 miles per gallon. 32 × 7 = 224 miles.", " miles")
    item("5 pounds of bananas cost $3.25. How much do 8 pounds cost?", F("5.2"), [F("6.25"), F("0.65"), F("4.55")],
         "3.25 ÷ 5 = $0.65 per pound. 0.65 × 8 = $5.20.")
    its[-1]["c"] = ["$" + (c + "0" if c.count(".") and len(c.split(".")[1]) == 1 else c) for c in its[-1]["c"]]
    item("A machine fills 360 bottles in 8 minutes. How many bottles does it fill in 15 minutes?", 675, [367, 45, 720],
         "360 ÷ 8 = 45 bottles per minute. 45 × 15 = 675 bottles.", " bottles")
    item("A map uses a scale of 2 inches for 15 miles. Two towns are 7 inches apart on the map. How far apart are they really?",
         F("52.5"), [20, F("7.5"), 105], "15 ÷ 2 = 7.5 miles per inch. 7.5 × 7 = 52.5 miles.", " miles")
    item("A recipe uses 3 cups of sugar for 12 muffins. How much sugar is needed for 20 muffins?", 5, [11, 4, F(1, 4)],
         "3 ÷ 12 = %s cup per muffin. %s × 20 = 5 cups." % (fr(1, 4), fr(1, 4)), " cups")
    item("A worker paints %s of a wall in %s hour. How many walls can the worker paint in 1 hour?" % (fr(3, 4), fr(1, 2)), F("1.5"), [F("0.375"), F(2, 3), F("1.25")],
         "Unit rate = %s ÷ %s = %s × 2 = 1 %s walls per hour." % (fr(3, 4), fr(1, 2), fr(3, 4), fr(1, 2)), " walls", "f")
    item("A snail moves %s foot in %s hour. What is its speed in feet per hour?" % (fr(1, 3), fr(1, 4)), F(4, 3), [F(3, 4), F(1, 12), F(7, 12)],
         "%s ÷ %s = %s × 4 = %s = 1 %s feet per hour." % (fr(1, 3), fr(1, 4), fr(1, 3), fr(4, 3), fr(1, 3)), " ft", "f")
    item("Paul walks %s mile in each %s hour. How many miles does he walk per hour?" % (fr(1, 2), fr(1, 4)), 2, [F(1, 8), F(1, 2), F(3, 4)],
         "%s ÷ %s = %s × 4 = 2 miles per hour." % (fr(1, 2), fr(1, 4), fr(1, 2)), " miles", "f")
    item("y is proportional to x, and y = 42 when x = 6. What is y when x = 11?", 77, [47, 66, F(11, 7)],
         "k = 42 ÷ 6 = 7, so y = 7x = 7 × 11 = 77. Not 47: that adds 5 instead of multiplying.")
    item("At a store, 3 notebooks cost $5.40. What is the cost of 1 notebook?", F("1.8"), [F("16.2"), F("2.4"), F("0.56")],
         "5.40 ÷ 3 = $1.80 per notebook.")
    its[-1]["c"] = ["$" + (c + "0" if "." in c and len(c.split(".")[1]) == 1 else c) for c in its[-1]["c"]]
    item("A pool fills at 18 gallons per minute. How many minutes does it take to add 450 gallons?", 25, [8100, 432, 468],
         "Gallons = 18 × minutes, so minutes = 450 ÷ 18 = 25.", " minutes")
    item("A train travels at a constant 80 km per hour. How long does it take to travel 300 km?", F("3.75"), [24000, 220, F("4.75")],
         "Distance = 80 × time, so time = 300 ÷ 80 = 3.75 hours (3 hours 45 minutes).", " hours")
    item("Two quarts of paint cover 150 square feet. How many quarts are needed for 525 square feet?", 7, [377, F("2.86"), 75],
         "150 ÷ 2 = 75 square feet per quart. 525 ÷ 75 = 7 quarts.", " quarts")
    item("Lena's heart beats 18 times in 15 seconds. At this rate, how many times does it beat in 1 minute?", 72, [63, 18, F("1.2")],
         "1 minute = 60 seconds = 4 × 15 seconds. 18 × 4 = 72 beats. Not 63: that adds 45 instead of multiplying.", " beats")
    item("A store sells 4 cans for $3. At the same price per can, how many cans can you buy for $15?", 20, [16, F("11.25"), 12],
         "$3 buys 4 cans, and $15 is 5 times $3. 4 × 5 = 20 cans.", " cans")
    item("A garden hose fills a 10-gallon bucket in 2.5 minutes. How many gallons does it put out in 6 minutes?", 24, [F("13.5"), F("1.5"), 15],
         "10 ÷ 2.5 = 4 gallons per minute. 4 × 6 = 24 gallons.", " gallons")
    item("An online store charges $2.50 shipping for each book. The shipping cost s is proportional to the number of books b. What is s for 9 books?",
         F("22.5"), [F("11.5"), F("3.6"), F("25")], "s = 2.5b = 2.5 × 9 = 22.5, so $22.50.")
    its[-1]["c"] = ["$" + (c + "0" if "." in c and len(c.split(".")[1]) == 1 else c) for c in its[-1]["c"]]
    item("Exchange rate: 1 US dollar buys 1.35 Canadian dollars. How many Canadian dollars do you get for 40 US dollars?", 54, [F("41.35"), F("29.63"), 58],
         "C = 1.35 × U = 1.35 × 40 = 54 Canadian dollars. Not 29.63: that divides 40 by 1.35.", " CAD")
    item("A scale model car is %s of the real size. The model is 7.5 inches long. How long is the real car?" % fr(1, 24), 180, [F("31.5"), F("0.3125"), F("7.5") + 24],
         "Real length = 24 × 7.5 = 180 inches (15 feet).", " in.")
    return {"title": "Word problems", "items": its}


def body():
    tbl = table(["Hours (x)", "1", "2", "3", "4"], [["Dollars (y)", "12", "24", "36", "48"], ["y ÷ x", "12", "12", "12", "12"]])
    svg = graph([(1, 2), (2, 4), (3, 6), (4, 8)], 6, 12, 2, "graph of y = 2x through the origin", (0, 0, 6, 12))
    return ("<h2>What is a proportional relationship?</h2><p>Two amounts are <b>proportional</b> when y ÷ x is always the same number. "
            "That number is the <b>constant of proportionality</b>, k. It is the same as the unit rate.</p>"
            + tbl
            + "<p>Every ratio is 12, so k = 12 and the equation is <b>y = 12x</b>.</p>"
            + "<h2>Proportional graphs</h2><p>The graph is a <b>straight line through the origin</b> (0, 0). "
            "The point (1, k) shows the unit rate.</p>"
            + figure(svg, "y = 2x: the line goes through (0, 0) and (1, 2), so k = 2.")
            + example("A car travels 150 miles in 3 hours at a steady speed. Write an equation and find the distance in 5 hours.",
                      ["k = 150 ÷ 3 = 50 miles per hour.", "Equation: d = 50h.", "d = 50 × 5 = 250."], "250 miles")
            + example("Is y = x + 4 proportional?", ["When x = 1, y = 5 (ratio 5). When x = 2, y = 6 (ratio 3).", "The ratios are different, and the line misses (0, 0)."], "No")
            + "<h2>Common mistakes</h2><ul><li>Dividing x by y: for 150 miles in 3 hours, k is 50, not 1/50.</li>"
            "<li>Using differences: if y goes up by 3 each time but starts at 5, it is not proportional.</li>"
            "<li>Thinking every straight line is proportional: it must also go through (0, 0).</li></ul>")


def main():
    sets = [set_tables(), set_constant(), set_graphs(), set_equations(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "proportional-relationships",
        "title": "Proportional Relationships",
        "seo_title": "Grade 7 Proportional Relationships Worksheets: Tables, Graphs, Constant of Proportionality and y = kx",
        "short_title": "Proportional relationships",
        "domain": "Ratios & Proportional Relationships",
        "standard_code": "7.RP.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/RP/A/2/",
        "standard_text": "Recognize and represent proportional relationships between quantities. Decide whether two quantities are in a proportional relationship; identify the constant of proportionality (unit rate) in tables, graphs, equations, diagrams, and verbal descriptions; represent proportional relationships by equations; explain what a point (x, y) on the graph means, with special attention to the points (0, 0) and (1, r).",
        "meta_desc": "Free Grade 7 proportional relationships worksheets: decide if a table or graph is proportional, find the constant of proportionality, write equations y = kx, and solve real-world rate problems. 100 practice questions with an answer key.",
        "key_big": "Proportional means y ÷ x is always the same number, k. Then y = kx.",
        "key_sub": "The graph is a straight line through (0, 0), and the point (1, k) shows the unit rate.",
        "body_html": body(),
        "faq": [
            {"q": "How do I know if a table is proportional?", "a": "Divide each y-value by its x-value. If every ratio is the same, the relationship is proportional. If one ratio is different, it is not."},
            {"q": "What is the constant of proportionality?", "a": "It is the number k in y = kx. It equals y ÷ x and is the unit rate. For $96 for 8 hours, k = 96 ÷ 8 = 12 dollars per hour."},
            {"q": "How can I tell from a graph?", "a": "A proportional graph is a straight line that goes through the origin (0, 0). A straight line that crosses the y-axis somewhere else is not proportional."},
            {"q": "What does the point (1, k) mean?", "a": "It shows the value of y when x is 1, which is the unit rate. On the graph of y = 12x, the point (1, 12) means $12 for 1 hour."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 4,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
