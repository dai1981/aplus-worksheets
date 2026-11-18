# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Independent and Dependent Quantities: Tables, Graphs and Equations (TEKS 6.4A, 6.6A, 6.6B, 6.6C)
  python3 tools/gen_ustx_math_g6_independent_dependent.py
Identifying independent and dependent quantities, writing equations y = kx and y = x + b from words and tables,
telling additive and multiplicative relationships apart, reading graphs, and using an equation.
Wrong answers come from real mistakes: switching the two quantities, checking only one pair in a table, and using
the change in y as the rule.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-6"

INK = "#1f2937"

SIT = [("The cost of gas depends on the number of gallons you buy.", "the number of gallons", "the cost", "c", "g"),
       ("The number of pages Ava reads depends on how many minutes she reads.", "the number of minutes", "the number of pages", "p", "m"),
       ("The total weight of a box of books depends on the number of books in it.", "the number of books", "the total weight", "w", "b"),
       ("The money Luis earns depends on how many hours he works.", "the number of hours worked", "the money earned", "e", "h"),
       ("The height of a candle depends on how long it has burned.", "the time it has burned", "the height of the candle", "h", "t"),
       ("The number of wheels in a parking lot depends on the number of cars.", "the number of cars", "the number of wheels", "w", "c"),
       ("The distance a cyclist travels depends on the time she rides.", "the time riding", "the distance traveled", "d", "t"),
       ("The amount of water in a pool depends on how long the hose has been running.", "the time the hose runs", "the amount of water", "a", "t"),
       ("The number of tickets sold determines the money a school play earns.", "the number of tickets sold", "the money earned", "m", "n"),
       ("The temperature of the soup changes with how long it is heated.", "the heating time", "the temperature of the soup", "t", "m")]


def one_indep(r):
    s, ind, dep, _, _ = r.choice(SIT)
    if r.random() < 0.5:
        return mcq(s + " Which quantity is the <b>independent</b> quantity?", ind[0].upper() + ind[1:], [dep[0].upper() + dep[1:], "Neither one", "Both of them"],
                   "The independent quantity changes on its own; the other quantity <b>depends</b> on it. Here it is <b>%s</b>." % ind)
    return mcq(s + " Which quantity is the <b>dependent</b> quantity?", dep[0].upper() + dep[1:], [ind[0].upper() + ind[1:], "Neither one", "Both of them"],
               "The dependent quantity depends on the other one. Here it is <b>%s</b>." % dep)


def table(xs, ys, xn, yn):
    th = "".join("<td>%s</td>" % comma(x) for x in xs)
    td = "".join("<td>%s</td>" % comma(y) for y in ys)
    return "<div class='sn-tw'><table class='sn-table'><tbody><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></tbody></table></div>" % (xn, th, yn, td)


def one_table(r):
    mult = r.random() < 0.55
    k = r.randint(2, 15)
    x0 = r.randint(1, 5)
    st = r.choice([1, 2, 3])
    xs = [x0 + st * i for i in range(4)]
    ys = [k * x if mult else x + k for x in xs]
    if not mult and ys[0] == 2 * xs[0]:
        return None
    right = "y = %dx" % k if mult else "y = x + %d" % k
    d = ys[1] - ys[0]
    w = ["y = x + %d" % (ys[0] - xs[0]) if mult else "y = %dx" % (ys[0] // xs[0] if ys[0] % xs[0] == 0 else k + 1), "y = %dx" % d if mult else "y = x + %d" % d, "y = x + %d" % d if mult else "y = %dx" % d, "y = %dx" % (k + 1)]
    w = [x for x in dict.fromkeys(w) if x != right]
    chk = ", ".join(("%d × %d = %d" % (k, x, y)) if mult else ("%d + %d = %d" % (x, k, y)) for x, y in zip(xs, ys))
    return mcq(table(xs, ys, "x", "y") + "Which equation shows the relationship in the table?", right, w,
               "Check every pair: %s. The equation is <b>%s</b>." % (chk, right))


def one_kind(r):
    mult = r.random() < 0.5
    k = r.randint(2, 12)
    x0, st = r.randint(1, 6), r.choice([1, 2])
    xs = [x0 + st * i for i in range(4)]
    ys = [k * x if mult else x + k for x in xs]
    if not mult and ys[0] == 2 * xs[0]:
        return None
    pic = table(xs, ys, "x", "y")
    right = "Multiplicative: y is always %d times x" % k if mult else "Additive: y is always %d more than x" % k
    w = ["Additive: y is always %d more than x" % (ys[0] - xs[0]), "Multiplicative: y is always %d times x" % (ys[1] - ys[0]), "Additive: y is always %d more than x" % (ys[1] - ys[0]), "Multiplicative: y is always %d times x" % (k + 1)]
    w = [x for x in dict.fromkeys(w) if x != right]
    return mcq(pic + "Which describes the relationship?", right, w,
               ("y ÷ x = %d for every pair, so it is <b>multiplicative</b>: y = %dx." % (k, k)) if mult else ("y − x = %d for every pair, so it is <b>additive</b>: y = x + %d." % (k, k)))


WORDS = [("A plumber charges $%d for each hour of work. Let h be the hours and c be the cost.", "c = %dh", "c = h + %d", "mult", (35, 95)),
         ("Each ticket to the county fair costs $%d. Let t be the number of tickets and m be the money paid.", "m = %dt", "m = t + %d", "mult", (6, 18)),
         ("Mia is %d years older than her brother. Let b be her brother's age and m be Mia's age.", "m = b + %d", "m = %db", "add", (2, 9)),
         ("A bus always has %d more seats than riders on a quiet morning. Let r be the riders and s be the seats.", "s = r + %d", "s = %dr", "add", (5, 20)),
         ("Each pack holds %d markers. Let p be the number of packs and n be the number of markers.", "n = %dp", "n = p + %d", "mult", (6, 12)),
         ("The water level is %d inches higher than it was last week. Let w be last week's level and n be the new level.", "n = w + %d", "n = %dw", "add", (3, 12)),
         ("A car uses 1 gallon of gas every %d miles. Let g be gallons and d be the distance in miles.", "d = %dg", "d = g + %d", "mult", (24, 36))]


def one_words(r):
    t, right, wrong, kind, (lo, hi) = r.choice(WORDS)
    k = r.randint(lo, hi)
    a = right % k
    b = wrong % k
    v1, v2 = a.split(" = ")[0], a.split(" = ")[1].replace(str(k), "").replace("+", "").strip()
    rev = "%s = %s" % (v2, a.split(" = ")[1].replace(v2, v1))
    return mcq(t % k + " Which equation shows the relationship?", a, [b, rev, "%s = %s − %d" % (v1, v2, k)],
               "%s The equation is <b>%s</b>." % ("Multiply: each one adds %d." % k if kind == "mult" else "Add %d to the independent quantity." % k, a))


def graph_svg(pts, xn, yn, ymax):
    W, H, x0, y0 = 320, 220, 46, 14
    pw, ph = W - x0 - 12, H - 44
    xmax = 6
    sx = lambda x: x0 + pw * x / float(xmax)
    sy = lambda y: y0 + ph - ph * y / float(ymax)
    st = ymax // 6
    s = ["<svg viewBox='0 0 %d %d' width='%d' data-pf='lg' role='img' aria-label='graph of %s and %s'>" % (W, H + 10, W, xn, yn)]
    for t in range(0, ymax + 1, st):
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#d1d5db'/><text x='%d' y='%.1f' font-size='11' text-anchor='end' fill='%s'>%d</text>" % (x0, sy(t), x0 + pw, sy(t), x0 - 4, sy(t) + 4, INK, t))
    for t in range(0, xmax + 1):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#d1d5db'/><text x='%.1f' y='%d' font-size='11' text-anchor='middle' fill='%s'>%d</text>" % (sx(t), y0, sx(t), y0 + ph, sx(t), y0 + ph + 14, INK, t))
    for x, y in pts:
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='#2563eb'/>" % (sx(x), sy(y)))
    s.append("<text x='%d' y='%d' font-size='12' text-anchor='middle' fill='%s'>%s</text>" % (x0 + pw // 2, H + 4, INK, xn))
    s.append("<text x='12' y='%d' font-size='12' text-anchor='middle' fill='%s' transform='rotate(-90 12 %d)'>%s</text></svg>" % (y0 + ph // 2, INK, y0 + ph // 2, yn))
    return fig("".join(s))


def one_graph(r):
    mult = r.random() < 0.55
    k = r.choice([2, 3, 4, 5, 6, 8, 10]) if mult else r.choice([2, 3, 4, 5, 6])
    xs = [1, 2, 3, 4, 5]
    pts = [(x, k * x if mult else x + k) for x in xs]
    ymax = max(y for _, y in pts)
    ymax = ((ymax + 5) // 6 + 1) * 6
    ctx = r.choice([("Hours", "Dollars earned"), ("Boxes", "Total items"), ("Weeks", "Plants")]) if mult else r.choice([("Brother’s age", "Sister’s age"), ("Guests", "Chairs set out")])
    pic = graph_svg(pts, ctx[0], ctx[1], ymax)
    right = "y = %dx" % k if mult else "y = x + %d" % k
    w = ["y = x + %d" % (pts[0][1] - 1) if mult else "y = %dx" % (k + 1), "y = %dx" % (k + 1) if mult else "y = x + %d" % (k + 1), "y = x + %d" % k if mult else "y = %dx" % k]
    w = [x for x in dict.fromkeys(w) if x != right]
    return mcq(pic + "Which equation matches the points on the graph?", right, w,
               "The points are %s. %s <b>%s</b>." % (", ".join("(%d, %d)" % p for p in pts[:3]), "Each y is %d times x:" % k if mult else "Each y is %d more than x:" % k, right))


def build():
    sets, R = build_sets([
        ("Independent or dependent?", [("collect", one_indep, 20)]),
        ("Write an equation from words", [("collect", one_words, 20)]),
        ("Write an equation from a table", [("collect", one_table, 20)]),
        ("Additive or multiplicative?", [("collect", one_kind, 20)]),
        ("Equations and graphs", [("collect", one_graph, 20)]),
    ], 66012)
    finish(sets, R)
    body = lesson('<ul><li>The <b>independent</b> quantity changes on its own. The <b>dependent</b> quantity depends on it: the cost depends on the number of gallons.</li><li>A <b>multiplicative</b> relationship has the form y = kx: y is always k times x.</li><li>An <b>additive</b> relationship has the form y = x + b: y is always b more than x.</li><li>Check a rule with <b>every</b> pair in a table or graph.</li></ul>',
        [example("x: 1, 2, 3, 4  y: 7, 14, 21, 28", ["14 ÷ 2 = 7, 21 ÷ 3 = 7", "Multiplicative"], "y = 7x"), example("x: 3, 4, 5  y: 10, 11, 12", ["10 − 3 = 7 for every pair", "Additive"], "y = x + 7")],
        [['Switching the quantities', 'Ask: which one depends on the other? That is the dependent quantity.'], ['Checking only one pair', 'y = 7x and y = x + 6 both give 1 → 7. Check the next pair too.'], ['Using the change in y as the rule', 'If y goes up by 7, test y = 7x and y = x + b.']])
    faq = [('What does TEKS 6.6A ask?', 'Identify independent and dependent quantities from tables and graphs.'), ('What does TEKS 6.6C ask?', 'Represent a given situation using verbal descriptions, tables, graphs and equations in the form y = kx or y = x + b.'), ('What does TEKS 6.4A ask?', 'Compare two rules verbally, numerically, graphically and symbolically in the form of y = ax or y = x + a in order to differentiate between additive and multiplicative relationships.'), ('Which axis shows the independent quantity?', 'The horizontal x-axis.')]
    make('independent-and-dependent-quantities', 12, 'Proportionality', '6.4A, 6.6A, 6.6B, 6.6C',
         '6.4A compare two rules verbally, numerically, graphically, and symbolically in the form of y = ax or y = x + a in order to differentiate between additive and multiplicative relationships; 6.6A identify independent and dependent quantities from tables and graphs; 6.6B write an equation that represents the relationship between independent and dependent quantities from a table; 6.6C represent a given situation using verbal descriptions, tables, graphs, and equations in the form y = kx or y = x + b',
         'Independent and Dependent Quantities: Tables, Graphs and Equations', 'Independent and Dependent Quantities',
         'Free Grade 6 worksheets for Texas TEKS 6.4A and 6.6: independent and dependent quantities, equations y = kx and y = x + b from words, tables and graphs, and additive versus multiplicative relationships. 100 questions with answers.',
         'y = kx is multiplicative; y = x + b is additive.', 'The dependent quantity depends on the independent quantity. Check every pair.',
         body, faq, sets, seo_title='Grade 6 Independent and Dependent Quantities Worksheets: Tables, Graphs and Equations (TEKS 6.6, STAAR)')


if __name__ == "__main__":
    build()
