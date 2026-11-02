# -*- coding: utf-8 -*-
"""
Ontario Grade 8 Math: Proportional relationships (Ontario Curriculum 2020, Number B2.8)
  python3 tools/gen_caon_math_g8_proportional.py
Tell whether tables, graphs, equations and situations are proportional (y ÷ x constant, a straight line
through (0, 0), y = kx), find the constant of proportionality k, solve proportions, compare rates
(best buys, fastest, fuel use), then word problems with map and model scales, recipes and fuel use.
Wrong answers come from real mistakes: additive thinking (adding the same amount instead of multiplying),
inverting the ratio (x ÷ y for k, or the second ratio upside down), multiplying without dividing,
reading one y value as k, "any straight line is proportional", and decimal slips.
Every numeric answer is checked with fractions.Fraction (never float).
Canadian English, dollars and cents (¢), metric units, SI number spacing. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
SLUG = "proportional-relationships"
UPDATED = "2026-11-02"
NBSP = "\u00a0"
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
GRID = "#c9d6cd"
RED = "#c0392b"
BLUE = "#2f6fc0"
FONT = "Arial, Helvetica, sans-serif"
CANT = "You can’t tell"
SAME = "They are the same"


# ------------------------------------------------------------ numbers
def num(x):
    """Exact decimal text: F(9, 2) -> '4.5', 2500 -> '2500', 18000 -> '18 000' (no-break space)."""
    x = F(x)
    assert x >= 0, x
    d, k = x.denominator, 0
    while (10 ** k) % d:
        k += 1
        assert k < 8, x
    v = x.numerator * (10 ** k // d)
    i, r = divmod(v, 10 ** k)
    s = str(i) if i < 10000 else "{:,}".format(i).replace(",", NBSP)
    if r:
        s += "." + str(r).zfill(k).rstrip("0")
    return s


def money(x):
    """$45, $25.50, 75¢ under $1."""
    x = F(x)
    c = x * 100
    assert c.denominator == 1 and c > 0, x
    c = int(c)
    if c < 100:
        return "%d¢" % c
    if c % 100:
        return "$%s.%02d" % (num(c // 100), c % 100)
    return "$" + num(c // 100)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def X(s):
    """Plain '3.5x' -> HTML with letters in italics and the real minus sign."""
    s = s.replace("-", "−")
    return re.sub(r"(?<![A-Za-z])([a-z]{1,2})(?![A-Za-z])", lambda m: "".join("<i>%s</i>" % c for c in m.group(1)), s)


XV, YV, KV = X("x"), X("y"), X("k")
YX = YV + " ÷ " + XV


def pt(a, b):
    return "(%s, %s)" % (num(a), num(b))


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


FRX = re.compile(r"^<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>$")
NUM = re.compile(r"^(\$)?(\d[\d" + NBSP + r"]*(?:\.\d+)?)(¢|%)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None when it is not a single number."""
    m = FRX.match(c)
    if m:
        return (F(int(m.group(1)), int(m.group(2))), "")
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2).replace(NBSP, ""))
    if (m.group(1) or m.group(3) == "¢") and m.group(4):
        return None
    if m.group(1):
        return (v, "$")
    if m.group(3) == "¢":
        return (v / 100, "$")
    if m.group(3) == "%":
        return (v, "%")
    return (v, (m.group(4) or "").strip())


def mcq(q, right, wrong, e, value=None):
    """Correct answer first + 3 wrong; balance() moves it. No two choices equal in value.
    value: the exact answer, checked against the correct choice."""
    right = str(right)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [right] + wrong
    assert len(set(plain(x) for x in ch)) == 4, (q, ch)
    if value is not None:
        v = val(right)
        assert v is not None and v[0] == F(value), (q, right, value)
    vs = [val(x) for x in ch]
    known = [v for v in vs if v is not None]
    assert len(set(known)) == len(known), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def prop(x, y):
    """True when every y ÷ x is the same (and no x is 0)."""
    return len({F(b) / F(a) for a, b in zip(x, y)}) == 1


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, bold=True, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def tw(t, fs):
    """Rough width of bold Arial text."""
    return sum(0.36 if ch in " .,()" else 0.62 for ch in plain(t)) * fs


def SX(s):
    return re.sub(r"(?<![A-Za-z])([a-z])(?![A-Za-z])", r"<tspan font-style='italic'>\1</tspan>", s)


def table_svg(names, rows, label="table of values"):
    """Two-row table of values. names: row headings; rows: two lists of numbers or '?' (red)."""
    rows = [[c if isinstance(c, str) else num(c) for c in r] for r in rows]
    fs = 16
    hw = max(tw(n, fs) for n in names) + 22
    cw = max([46] + [tw(c, fs) + 20 for r in rows for c in r])
    rh = 32
    n = len(rows[0])
    W = 4 + hw + n * cw + 4
    H = 2 * rh + 8
    s = []
    for j, nm in enumerate(names):
        y = 4 + j * rh
        s.append("<rect x='4' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (y, hw, rh, FILL, GREEN))
        s.append(text(4 + hw / 2, y + rh / 2 + 6, SX(nm) if len(nm) == 1 else nm, 17 if len(nm) == 1 else 15))
        for i, c in enumerate(rows[j]):
            x = 4 + hw + i * cw
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                     % (x, y, cw, rh, GREEN))
            s.append(text(x + cw / 2, y + rh / 2 + 6, c, fs, col=RED if c == "?" else LINE))
    return svg_wrap(W, H, "".join(s), label)


def graph_svg(xmax, ymax, ystep=1, ylab=1, xname="x", yname="y", lines=(), dots=(), xlab=1,
              label="graph"):
    """First-quadrant graph drawn exactly to the grid.
    lines: (points, tag, colour) polylines in data units; tag (e.g. 'A') is written past the last point.
    dots: points marked with red dots."""
    PW, PH = 240.0, 180.0
    XU, YU = PW / xmax, PH / ymax
    ylabels = [(gy, num(gy)) for gy in range(0, ymax + 1, ylab)]
    LW = max(tw(t, 14) for _, t in ylabels)
    yn_long = len(yname) > 1
    L = (34 if yn_long else 26) + LW + 6
    tagged = any(tag for _, tag, _ in lines)
    T, R, B = 16, (30 if tagged else 14), 48
    X0, Y0 = L, T + PH
    W, H = L + PW + R, T + PH + B
    s = []
    for gy in range(0, ymax + 1, ystep):
        y = Y0 - gy * YU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (X0, y, X0 + PW, y, GRID))
    for gx in range(0, xmax + 1):
        x = X0 + gx * XU
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x, T, x, Y0, GRID))
    for gy, t in ylabels:
        s.append(text(X0 - 6, Y0 - gy * YU + 5, t, 14, "end", bold=False))
    for gx in range(0, xmax + 1, xlab):
        s.append(text(X0 + gx * XU, Y0 + 19, num(gx), 14, bold=False))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, Y0, X0 + PW, Y0, LINE))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (X0, T, X0, Y0, LINE))
    s.append(text(X0 + PW / 2, H - 6, SX(xname) if len(xname) == 1 else xname, 17 if len(xname) == 1 else 15))
    if yn_long:
        cy = T + PH / 2
        s.append(text(16, cy, yname, 15, extra=" transform='rotate(-90 16 %.1f)'" % cy))
    else:
        s.append(text(X0 - LW - 18, T + PH / 2 + 6, SX(yname), 17))
    P = lambda p: (X0 + float(F(p[0]) * F(XU)), Y0 - float(F(p[1]) * F(YU)))
    for pts, tag, col in lines:
        for p in pts:
            assert 0 <= p[0] <= xmax and 0 <= p[1] <= ymax, p
        s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='3'/>"
                 % (" ".join("%.1f,%.1f" % P(p) for p in pts), col))
        if tag:
            ex_, ey = P(pts[-1])
            s.append(text(ex_ + 14, ey + 6, tag, 17, col=col))
    for p in dots:
        assert 0 <= p[0] <= xmax and 0 <= p[1] <= ymax, p
        cx, cy = P(p)
        s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (cx, cy, RED))
    return svg_wrap(W, H, "".join(s), label)


def straight(k, b, x0, x1):
    return [(x0, F(k) * x0 + F(b)), (x1, F(k) * x1 + F(b))]


def tq(xs, ys, q):
    return fig(table_svg(["x", "y"], [xs, ys])) + q


# ============================================================ set 1: proportional or not
def set_check():
    its = []
    xs, ys = [1, 2, 3, 4], [3, 6, 9, 12]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "Is the relationship in the table proportional?"),
                   "Yes. %s = 3 every time" % YX,
                   ["No. A proportional table must start at (0, 0)", "No. %s goes up by 3, not by 1" % YV,
                    "No. %s and %s must go up by the same amount" % (XV, YV)],
                   "Divide each %s by its %s: 3 ÷ 1 = 6 ÷ 2 = 9 ÷ 3 = 12 ÷ 4 = 3. The quotient never changes, "
                   "so the relationship is <b>proportional</b>, with %s = 3%s. A table does not need to show (0, 0)."
                   % (YV, XV, YV, XV)))
    xs, ys = [1, 2, 3, 4], [5, 7, 9, 11]
    assert not prop(xs, ys)
    its.append(mcq(tq(xs, ys, "Is the relationship in the table proportional?"),
                   "No. %s is not the same every time" % YX,
                   ["Yes. %s goes up by 2 each time" % YV, "Yes. The rule is %s" % X("y = 5x"),
                    "Yes. The rule is %s" % X("y = 2x")],
                   "5 ÷ 1 = 5, but 7 ÷ 2 = 3.5. The quotients change, so it is <b>not proportional</b>. "
                   "Going up by the same amount (+2) makes a straight line, but the rule is %s, not %s."
                   % (X("y = 2x + 3"), X("y = 2x"))))
    its.append(mcq("Which set of points shows a proportional relationship?",
                   "(2, 5), (4, 10), (6, 15)", ["(2, 5), (4, 7), (6, 9)", "(1, 4), (2, 6), (3, 8)",
                                                "(2, 4), (3, 9), (4, 16)"],
                   "5 ÷ 2 = 10 ÷ 4 = 15 ÷ 6 = 2.5, so <b>(2, 5), (4, 10), (6, 15)</b> is proportional. "
                   "(2, 5), (4, 7), (6, 9) adds 2 each time, (1, 4), (2, 6), (3, 8) is a line that starts at 2, "
                   "and (2, 4), (3, 9), (4, 16) squares the %s values." % XV))
    xs, ys = [2, 5, 8], [7, F(35, 2), 28]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "Is the relationship in the table proportional?"),
                   "Yes. %s = 3.5 every time" % YX,
                   ["No. %s goes up by 3 but %s goes up by 10.5" % (XV, YV),
                    "No. 17.5 is not a whole number", "No. %s is different every time" % YX],
                   "7 ÷ 2 = 3.5, 17.5 ÷ 5 = 3.5 and 28 ÷ 8 = 3.5. The quotient is always 3.5, so it is "
                   "<b>proportional</b>: %s = 3.5%s. The steps 3 and 10.5 are different because 10.5 = 3.5 × 3."
                   % (YV, XV)))
    xs, ys = [3, 6, 9, 12], [4, 8, 13, 16]
    assert not prop(xs, ys) and prop([3, 6, 12], [4, 8, 16])
    its.append(mcq(tq(xs, ys, "Is the relationship in the table proportional?"),
                   "No. For 9, %s should be 12, not 13" % YV,
                   ["Yes. %s is about 1.3 every time" % YX, "Yes. %s goes up when %s goes up" % (YV, XV),
                    "No. %s should go up by 3, like %s" % (YV, XV)],
                   "4 ÷ 3, 8 ÷ 6 and 16 ÷ 12 all equal %s. For %s = 9, %s should be 9 × %s = 12, but the table "
                   "shows 13. One pair breaks the pattern, so it is <b>not proportional</b>. “About the same” is not enough."
                   % (fr(4, 3), XV, YV, fr(4, 3))))
    its.append(mcq(fig(graph_svg(6, 18, 3, 3, lines=[(straight(3, 0, 0, 6), None, GREEN)],
                                 dots=[(i, 3 * i) for i in range(1, 7)], label="graph of a straight line")) +
                   "Does the graph show a proportional relationship?",
                   "Yes. It is a straight line through (0, 0)",
                   ["No. It must go through (1, 1)", "No. The line is too steep",
                    "No. The points go up by 3, not by 1"],
                   "A proportional graph is a <b>straight line through the origin (0, 0)</b>. This one is. "
                   "Every point has %s = 3: (1, 3), (2, 6), (3, 9). The steepness is the value of %s, which can be any positive number."
                   % (YX, KV)))
    its.append(mcq(fig(graph_svg(6, 12, 1, 2, lines=[(straight(F(3, 2), 2, 0, 6), None, GREEN)],
                                 dots=[(0, 2), (2, 5), (4, 8), (6, 11)], label="graph of a straight line")) +
                   "Does the graph show a proportional relationship?",
                   "No. The line does not go through (0, 0)",
                   ["Yes. It is a straight line", "Yes. It goes up by the same amount each step",
                    "No. The line is not steep enough"],
                   "The line starts at (0, 2), not (0, 0). Check: 5 ÷ 2 = 2.5 but 8 ÷ 4 = 2. "
                   "A straight line is not enough: it must also go through the origin. So it is <b>not proportional</b>."))
    curve = [(F(i, 2), F(i * i, 8)) for i in range(0, 13)]
    its.append(mcq(fig(graph_svg(6, 18, 3, 3, lines=[(curve, None, GREEN)],
                                 dots=[(0, 0), (2, 2), (4, 8), (6, 18)], label="graph of a curve")) +
                   "Does the graph show a proportional relationship?",
                   "No. It is not a straight line",
                   ["Yes. It starts at (0, 0)", "Yes. %s gets bigger as %s gets bigger" % (YV, XV),
                    "No. It does not start at (0, 0)"],
                   "The graph goes through (0, 0), but it curves. Check: 2 ÷ 2 = 1, 8 ÷ 4 = 2 and 18 ÷ 6 = 3. "
                   "%s changes, so it is <b>not proportional</b>. You need a straight line <b>and</b> (0, 0)." % YX))
    its.append(mcq("Which equation shows a proportional relationship?",
                   X("y = 6x"), [X("y = x + 6"), X("y = 6x + 1"), X("y = x") + "<sup>2</sup>"],
                   "A proportional equation has the form %s: %s times a number, with nothing added. "
                   "<b>%s</b> fits. %s and %s add a number, and %s<sup>2</sup> is a curve."
                   % (X("y = kx"), XV, X("y = 6x"), X("y = x + 6"), X("y = 6x + 1"), X("y = x"))))
    its.append(mcq("Which equation is <b>not</b> a proportional relationship?",
                   X("y = 2x + 5"), [X("y = 2.5x"), X("y = 0.8x"), YV + " = " + fr(1, 4) + XV],
                   "%s, %s and %s = %s%s all have the form %s. <b>%s</b> adds 5, so when %s = 0, %s = 5, not 0."
                   % (X("y = 2.5x"), X("y = 0.8x"), YV, fr(1, 4), XV, X("y = kx"), X("y = 2x + 5"), XV, YV)))
    its.append(mcq("In a proportional relationship, what must %s be when %s = 0?" % (YV, XV),
                   "0", ["1", "the value of %s" % KV, "any number"],
                   "%s = %s × 0 = <b>0</b>. That is why every proportional graph goes through the origin (0, 0)." % (YV, KV),
                   value=0))
    its.append(mcq("%s is proportional to %s. What happens to %s when %s doubles?" % (YV, XV, YV, XV),
                   "%s doubles" % YV, ["%s goes up by 2" % YV, "%s stays the same" % YV, "%s is cut in half" % YV],
                   "%s = %s%s, so 2 times the %s gives 2 times the %s: <b>%s doubles</b>. "
                   "“Goes up by 2” is additive thinking." % (YV, KV, XV, XV, YV, YV)))
    its.append(mcq("Hana is 3 years older than her brother. Is her age proportional to his age?",
                   "No. The difference stays 3, but the ratio changes",
                   ["Yes. Her age goes up by 1 when his does", "Yes. Her age is always 3 times his age",
                    "Yes. The ratio of their ages stays the same"],
                   "When he is 3, she is 6 (ratio 2). When he is 9, she is 12 (ratio %s). The ratio changes, "
                   "so it is <b>not proportional</b>. A constant difference is additive, not multiplicative." % fr(4, 3)))
    its.append(mcq("Apples cost 80¢ each, with no other charge. Is the cost proportional to the number of apples?",
                   "Yes. Cost = 0.80 × number, and 0 apples cost $0",
                   ["No. The cost goes up by 80¢ each time, which is adding",
                    "No. The price is not a whole number of dollars", "No. The more apples, the higher the cost"],
                   "The cost is always 0.80 times the number of apples: %s. There is no starting fee, "
                   "so 0 apples cost $0. It is <b>proportional</b>, with %s = 0.80." % (X("c = 0.80n"), KV)))
    its.append(mcq("A taxi charges $4 to start, plus $2 for each kilometre. Is the cost proportional to the distance?",
                   "No. A 0 km ride would still cost $4",
                   ["Yes. Each kilometre adds $2", "Yes. The cost per kilometre is always $2",
                    "Yes. Its graph is a straight line"],
                   "The cost is %s. Its graph is a straight line, but it starts at (0, 4). "
                   "1 km costs $6 and 2 km cost $8, not $12. It is <b>not proportional</b>." % X("c = 2d + 4")))
    its.append(mcq("Which situation is proportional?",
                   "Gas at $1.55 per litre",
                   ["A taxi: $4 plus $2 per km", "A phone plan: $20 a month plus $5 per GB",
                    "Hana’s age and her brother’s age"],
                   "Gas has no starting fee: cost = 1.55 × litres, so 0 L cost $0 and 2 times the litres cost 2 times as much. "
                   "<b>Gas at $1.55 per litre</b> is proportional. The taxi and phone plan have a starting amount, "
                   "and the ages have a constant difference."))
    xs, ys = [2, 5, 7], [6, 15, "?"]
    its.append(mcq(tq(xs, ys, "%s is proportional to %s. What is the missing value?" % (YV, XV)),
                   "21", ["17", "24", "105"],
                   "%s = 6 ÷ 2 = 3, so %s = 3 × 7 = <b>21</b>. 17 adds 2 because %s went up by 2, "
                   "24 adds 9 like 6 to 15, and 105 is 15 × 7 without dividing by 5." % (KV, YV, XV), value=21))
    pts = [(1, 2), (2, 4), (3, 7), (4, 8), (5, 10)]
    its.append(mcq(fig(graph_svg(6, 12, 1, 2, dots=pts, label="graph of points")) +
                   "All but one of these points fit a proportional relationship. Which point does <b>not</b> fit?",
                   "(3, 7)", ["(2, 4)", "(4, 8)", "(5, 10)"],
                   "For (1, 2), (2, 4), (4, 8) and (5, 10), %s = 2. For <b>(3, 7)</b>, 7 ÷ 3 is not 2: "
                   "it should be (3, 6)." % YX))
    its.append(mcq("Four painters take 6 hours to paint a fence. Is the time proportional to the number of painters?",
                   "No. More painters take less time",
                   ["Yes. 8 painters take 12 hours", "Yes. The ratio 4:6 stays the same",
                    "Yes. The time goes up by the same amount for each painter"],
                   "Twice as many painters finish in about half the time, not twice the time. "
                   "When one amount goes up as the other goes down, %s is not constant: <b>not proportional</b>." % YX))
    its.append(mcq("Which statement about proportional relationships is <b>true</b>?",
                   "The graph is a straight line through (0, 0)",
                   ["Any straight-line graph is proportional", "%s always goes up by %s" % (YV, KV),
                    "The table must include %s = 0" % XV],
                   "Proportional means %s with %s the same everywhere, so the graph is a <b>straight line through (0, 0)</b>. "
                   "A line that starts above 0 is not proportional, and %s goes up by %s only when %s goes up by 1."
                   % (X("y = kx"), YX, YV, KV, XV)))
    assert len(its) == 20, len(its)
    return {"title": "Proportional or not: tables, graphs and equations", "items": its}


# ============================================================ set 2: constant of proportionality
def set_k():
    its = []
    xs, ys = [2, 4, 6, 8], [6, 12, 18, 24]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "What is the constant of proportionality %s?" % KV),
                   "3", ["6", fr(1, 3), "2"],
                   "%s = %s = 6 ÷ 2 = <b>3</b>. 6 is how much %s goes up each step, and %s is %s ÷ %s, the wrong way round."
                   % (KV, YX, YV, fr(1, 3), XV, YV), value=3))
    xs, ys = [5, 10, 15], [2, 4, 6]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "What is the constant of proportionality %s?" % KV),
                   "0.4", ["2.5", "2", "5"],
                   "%s = %s = 2 ÷ 5 = <b>0.4</b>. 2.5 is 5 ÷ 2, the inverted ratio. 2 and 5 are just the steps in the rows."
                   % (KV, YX), value=F(2, 5)))
    its.append(mcq(fig(graph_svg(8, 20, 2, 4, lines=[(straight(F(5, 2), 0, 0, 8), None, GREEN)],
                                 dots=[(2, 5), (4, 10), (6, 15), (8, 20)], label="graph of a straight line")) +
                   "The graph shows a proportional relationship. What is %s?" % KV,
                   "2.5", ["0.4", "10", "6"],
                   "Use a point on the line, like (4, 10): %s = 10 ÷ 4 = <b>2.5</b>. "
                   "0.4 is 4 ÷ 10 (inverted), 10 is only the %s value, and 6 is 10 − 4." % (KV, YV), value=F(5, 2)))
    its.append(mcq(fig(graph_svg(10, 6, 1, 1, xlab=2, lines=[(straight(F(3, 5), 0, 0, 10), None, GREEN)],
                                 dots=[(5, 3), (10, 6)], label="graph of a straight line")) +
                   "The graph shows a proportional relationship. What is %s?" % KV,
                   "0.6", [fr(5, 3), "3", "2"],
                   "The line goes through (5, 3). %s = 3 ÷ 5 = <b>0.6</b>. Check with (10, 6): 6 ÷ 10 = 0.6. "
                   "%s is %s ÷ %s, and 2 is 5 − 3." % (KV, fr(5, 3), XV, YV), value=F(3, 5)))
    xs, ys = [2, 4, 6], [7, 14, 21]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "Which equation matches the table?"),
                   X("y = 3.5x"), [X("x = 3.5y"), X("y = x + 5"), X("y = 7x")],
                   "%s = 7 ÷ 2 = 3.5, so <b>%s</b>. Check: 3.5 × 6 = 21. %s swaps the letters, "
                   "%s only works for the first pair, and %s uses the first %s value as %s."
                   % (KV, X("y = 3.5x"), X("x = 3.5y"), X("y = x + 5"), X("y = 7x"), YV, KV)))
    its.append(mcq("Mei earns $16.50 an hour. Which equation gives her pay %s for %s hours?" % (X("p"), X("h")),
                   X("p = 16.5h"), [X("h = 16.5p"), X("p = h + 16.5"), X("p = h") + " ÷ 16.5"],
                   "Pay = 16.50 × hours, so <b>%s</b>. The constant of proportionality is the hourly rate. "
                   "%s swaps the amounts, and adding 16.5 gives the pay for only 1 more hour." % (X("p = 16.5h"), X("h = 16.5p"))))
    its.append(mcq("15 L of gas cost $24. What is the constant of proportionality (dollars per litre)?",
                   "1.6", ["0.625", "9", "360"],
                   "%s = dollars ÷ litres = 24 ÷ 15 = <b>1.6</b>, so gas is $1.60 per litre. "
                   "0.625 is 15 ÷ 24 (litres per dollar), 9 is 24 − 15, and 360 is 24 × 15." % KV, value=F(8, 5)))
    its.append(mcq(fig(graph_svg(4, 60, 5, 15, xname="Time (h)", yname="Distance (km)",
                                 lines=[(straight(15, 0, 0, 4), None, GREEN)], dots=[(2, 30), (4, 60)],
                                 label="graph of distance and time")) +
                   "The graph shows a cyclist riding at a steady speed. What is the speed?",
                   "15 km/h", ["30 km/h", "28 km/h", "60 km/h"],
                   "Speed = distance ÷ time. Use (2, 30): 30 ÷ 2 = <b>15 km/h</b>. 30 km/h reads the distance after 2 h, "
                   "28 is 30 − 2, and 60 is the distance after 4 h, not 1 h.", value=15))
    its.append(mcq("The point (6, 21) is on the graph of %s. What is %s?" % (X("y = kx"), KV),
                   "3.5", ["15", fr(2, 7), "126"],
                   "%s = %s = 21 ÷ 6 = <b>3.5</b>. 15 is 21 − 6, %s is 6 ÷ 21, and 126 is 21 × 6." % (KV, YX, fr(2, 7)),
                   value=F(7, 2)))
    its.append(mcq("Which point is on the graph of %s?" % X("y = 2.5x"),
                   "(4, 10)", ["(10, 4)", "(4, 6.5)", "(2, 2.5)"],
                   "Put %s = 4 into the equation: %s = 2.5 × 4 = 10, so <b>(4, 10)</b>. "
                   "(10, 4) swaps %s and %s, (4, 6.5) adds 2.5, and for %s = 2, %s is 5, not 2.5."
                   % (XV, YV, XV, YV, XV, YV)))
    its.append(mcq("5 kg of potatoes cost $7.25. Which equation gives the cost %s of %s kilograms?" % (X("c"), X("m")),
                   X("c = 1.45m"), [X("m = 1.45c"), X("c = 7.25m"), X("c = m + 2.25")],
                   "Price per kilogram: 7.25 ÷ 5 = 1.45, so <b>%s</b>. Check: 1.45 × 5 = 7.25. "
                   "%s is the price of 5 kg times %s, and %s comes from 7.25 − 5."
                   % (X("c = 1.45m"), X("c = 7.25m"), X("m"), X("c = m + 2.25"))))
    its.append(mcq("%s = 0.8%s. What is %s when %s = 15?" % (YV, XV, YV, XV),
                   "12", ["18.75", "15.8", "14.2"],
                   "%s = 0.8 × 15 = <b>12</b>. 18.75 divides by 0.8, 15.8 adds 0.8, and 14.2 subtracts 0.8." % YV,
                   value=12))
    its.append(mcq("%s = 0.8%s. What is %s when %s = 20?" % (YV, XV, XV, YV),
                   "25", ["16", "20.8", "19.2"],
                   "20 = 0.8%s, so %s = 20 ÷ 0.8 = <b>25</b>. Check: 0.8 × 25 = 20. 16 multiplies 20 by 0.8 "
                   "instead of dividing, 20.8 adds 0.8, and 19.2 subtracts 0.8." % (XV, XV), value=25))
    its.append(mcq(tq([4, 8, 12], [10, 20, 30],
                      "Which has the greater constant of proportionality: the table or the equation %s?" % X("y = 2.4x")),
                   "The table", ["The equation", SAME, CANT],
                   "Table: %s = 10 ÷ 4 = 2.5. Equation: %s = 2.4. 2.5 &gt; 2.4, so <b>the table</b> has the greater %s."
                   % (KV, KV, KV)))
    xs, ys = [2, 4, 6], [8, 16, 24]
    its.append(mcq(tq(xs, ys, "Liam says %s = 0.25 for this table. What mistake did he make?" % KV),
                   "He divided %s by %s" % (XV, YV),
                   ["He used how much %s goes up each step" % YV, "He did not make a mistake",
                    "He subtracted %s from %s" % (XV, YV)],
                   "2 ÷ 8 = 0.25 is %s ÷ %s. The constant is %s = 8 ÷ 2 = 4. He <b>divided %s by %s</b>: the ratio is inverted."
                   % (XV, YV, YX, XV, YV)))
    xs, ys = [3, 6, 9], [2, 4, 6]
    assert prop(xs, ys)
    its.append(mcq(tq(xs, ys, "What is the constant of proportionality %s as a fraction?" % KV),
                   fr(2, 3), [fr(3, 2), "2", "3"],
                   "%s = %s = <b>%s</b>. Check: %s × 9 = 6. %s is %s ÷ %s. 2 and 3 are the steps in the rows."
                   % (KV, YX, fr(2, 3), fr(2, 3), fr(3, 2), XV, YV), value=F(2, 3)))
    its.append(mcq("A recipe uses 3 cups of flour for every 2 cups of milk. Which equation gives the flour %s for %s cups of milk?"
                   % (X("f"), X("m")),
                   X("f = 1.5m"), [X("m = 1.5f"), X("f = m + 1"), X("f = 3m")],
                   "Flour ÷ milk = 3 ÷ 2 = 1.5, so <b>%s</b>. Check: 1.5 × 2 = 3 cups. %s gives more milk than flour, "
                   "%s uses the difference, and %s uses only the 3." % (X("f = 1.5m"), X("m = 1.5f"), X("f = m + 1"), X("f = 3m"))))
    its.append(mcq("Bus tickets cost %s each. In %s, what does 3.25 tell you?" % (money(F(13, 4)), X("c = 3.25n")),
                   "The cost of 1 ticket", ["The number of tickets $1 buys", "The cost of 0 tickets",
                                            "The total cost"],
                   "In %s, %s is the amount for 1. Here %s = 3.25 is <b>the cost of 1 ticket</b>: $3.25. "
                   "0 tickets cost $0." % (X("y = kx"), KV, KV)))
    its.append(mcq("%s is proportional to %s, and %s = 18 when %s = 24. What is %s when %s = 12?" % (YV, XV, YV, XV, YV, XV),
                   "9", ["16", "6", "0.75"],
                   "%s = 18 ÷ 24 = 0.75, so %s = 0.75 × 12 = <b>9</b>. Or: 12 is half of 24, so %s is half of 18. "
                   "16 inverts the ratio, 6 subtracts 6 like 24 − 18, and 0.75 is %s." % (KV, YV, YV, KV), value=9))
    its.append(mcq(fig(graph_svg(6, 16, 1, 2, lines=[(straight(2, 3, 0, 6), None, GREEN)],
                                 dots=[(0, 3), (2, 7), (4, 11), (6, 15)], label="graph of a straight line")) +
                   "Why does this line <b>not</b> have a constant of proportionality?",
                   "It does not go through (0, 0), so %s changes" % YX,
                   ["It does: %s = 2" % KV, "It does: %s = 3" % KV, "It is not a straight line"],
                   "(2, 7) gives 7 ÷ 2 = 3.5, but (4, 11) gives 2.75. The line starts at (0, 3), so <b>%s is not constant</b>. "
                   "The line goes up 2 for each step, but that is a rate of change, not a constant of proportionality." % YX))
    assert len(its) == 20, len(its)
    return {"title": "The constant of proportionality k in y = kx", "items": its}


# ============================================================ set 3: solving proportions
def solve_q(lhs, rhs, x, wrong, e, value):
    q = "Solve: %s = %s" % (lhs, rhs)
    return mcq(q, num(x), [num(w) for w in wrong], e, value=value)


def set_solve():
    its = []
    xv = XV

    def check(a, b, c, d):
        """a/b = c/d with exact values."""
        assert F(a) / F(b) == F(c) / F(d), (a, b, c, d)

    x = F(12 * 3, 4); check(x, 12, 3, 4)
    its.append(solve_q(fr(xv, 12), fr(3, 4), x, [11, 16, 36],
                       "12 = 4 × 3, so %s = 3 × 3 = <b>9</b>. 11 adds 8 because 4 + 8 = 12, 16 inverts the ratio "
                       "(12 × 4 ÷ 3), and 36 is 12 × 3 without dividing by 4." % xv, 9))
    x = F(5 * 40, 8); check(5, 8, x, 40)
    its.append(solve_q(fr(5, 8), fr(xv, 40), x, [37, 64, 200],
                       "40 = 8 × 5, so %s = 5 × 5 = <b>25</b>. 37 adds 32 like 8 + 32 = 40, 64 inverts the ratio, and 200 is 5 × 40." % xv, 25))
    x = F(6 * 15, 9); check(6, x, 9, 15)
    its.append(solve_q(fr(6, xv), fr(9, 15), x, [12, F(45, 2), F(18, 5)],
                       "Cross-multiply: 9%s = 6 × 15 = 90, so %s = <b>10</b>. 12 adds 6 like 9 + 6 = 15, "
                       "22.5 is 9 × 15 ÷ 6, and 3.6 multiplies the wrong pair (6 × 9 ÷ 15)." % (xv, xv), 10))
    x = F(14 * 5, 2); check(14, x, 2, 5)
    its.append(solve_q(fr(14, xv), fr(2, 5), x, [17, F(28, 5), 70],
                       "14 = 2 × 7, so %s = 5 × 7 = <b>35</b>. 17 adds 12 like 2 + 12 = 14, "
                       "5.6 is 14 × 2 ÷ 5, and 70 is 14 × 5." % xv, 35))
    x = F(24, 10) * 10 / 3; check(F(24, 10), 3, x, 10)
    its.append(solve_q(fr("2.4", 3), fr(xv, 10), x, [F(94, 10), F(25, 2), 24],
                       "2.4 ÷ 3 = 0.8, so %s = 0.8 × 10 = <b>8</b>. 9.4 adds 7 like 3 + 7 = 10, "
                       "12.5 is 10 × 3 ÷ 2.4, and 24 is 2.4 × 10." % xv, 8))
    x = F(7 * 18, 21); check(x, 7, 18, 21)
    its.append(solve_q(fr(xv, 7), fr(18, 21), x, [4, 126, 3],
                       "21 ÷ 3 = 7, so %s = 18 ÷ 3 = <b>6</b>. 4 subtracts 14 like 21 − 14 = 7, "
                       "126 is 7 × 18, and 3 is only the number you divide by." % xv, 6))
    x = F(4 * 63, 9); check(4, 9, x, 63)
    its.append(mcq("Solve: 4:9 = %s:63" % xv, "28", ["58", "7", "36"],
                   "63 = 9 × 7, so %s = 4 × 7 = <b>28</b>. 58 adds 54 like 9 + 54 = 63, 7 is the multiplier, "
                   "and 36 is 4 × 9." % xv, value=x))
    x = F(42, 10) * 5 / 3; check(3, 5, F(42, 10), x)
    its.append(mcq("Solve: 3:5 = 4.2:%s" % xv, "7", ["6.2", "2.52", "21"],
                   "4.2 = 3 × 1.4, so %s = 5 × 1.4 = <b>7</b>. 6.2 adds 1.2 like 3 + 1.2 = 4.2, "
                   "2.52 is 4.2 × 3 ÷ 5, and 21 is 4.2 × 5." % xv, value=x))
    check(6, 8, 15, 20)
    its.append(mcq("Which proportion is true?",
                   "%s = %s" % (fr(6, 8), fr(15, 20)),
                   ["%s = %s" % (fr(6, 8), fr(9, 11)), "%s = %s" % (fr(6, 8), fr(12, 14)),
                    "%s = %s" % (fr(6, 8), fr(8, 6))],
                   "Cross-multiply: 6 × 20 = 120 and 8 × 15 = 120. They match, so <b>%s = %s</b> (both are %s). "
                   "%s and %s add the same number to the top and bottom, and %s is upside down."
                   % (fr(6, 8), fr(15, 20), fr(3, 4), fr(9, 11), fr(12, 14), fr(8, 6))))
    x = F(9, 2) * 8 / 6; check(x, F(9, 2), 8, 6)
    its.append(solve_q(fr(xv, "4.5"), fr(8, 6), x, [F(13, 2), F(27, 8), 36],
                       "8 ÷ 6 = %s, so %s = %s × 4.5 = <b>6</b>. 6.5 subtracts 1.5 like 6 − 1.5 = 4.5, "
                       "3.375 inverts the ratio, and 36 is 4.5 × 8." % (fr(4, 3), xv, fr(4, 3)), 6))
    x = F(12) / F(4, 5)
    its.append(mcq("Solve: %s = 0.8" % fr(12, xv), "15", ["9.6", "11.2", "12.8"],
                   "0.8%s = 12, so %s = 12 ÷ 0.8 = <b>15</b>. Check: 12 ÷ 15 = 0.8. 9.6 is 12 × 0.8, "
                   "11.2 subtracts 0.8, and 12.8 adds 0.8." % (xv, xv), value=x))
    its.append(mcq("3 notebooks cost $7.50. Which proportion finds the cost %s of 8 notebooks?" % xv,
                   "%s = %s" % (fr(3, "7.50"), fr(8, xv)),
                   ["%s = %s" % (fr(3, "7.50"), fr(xv, 8)), "%s = %s" % (fr(3, 8), fr(xv, "7.50")),
                    "%s = %s" % (fr("7.50", 3), fr(8, xv))],
                   "Keep the same order in both ratios: notebooks over dollars on each side, so <b>%s = %s</b>. "
                   "The other choices flip one ratio, so the notebooks and dollars no longer match."
                   % (fr(3, "7.50"), fr(8, xv))))
    x = F(15, 2) / 3 * 8
    its.append(mcq("3 notebooks cost $7.50. What do 8 notebooks cost?", money(x),
                   ["$12.50", "$60", "$22.50"],
                   "One notebook: $7.50 ÷ 3 = $2.50. 8 notebooks: 8 × $2.50 = <b>%s</b>. $12.50 adds $5 for 5 more notebooks, "
                   "$60 is 8 × $7.50, and $22.50 is 3 × $7.50." % money(x), value=x))
    x = F(15 * 4, 6); check(x, 15, 4, 6)
    its.append(solve_q(fr(xv, 15), fr(4, 6), x, [13, F(45, 2), 60],
                       "%s = %s, so %s = %s × 15 = <b>10</b>. 13 adds 9 like 6 + 9 = 15, 22.5 is 15 × 6 ÷ 4, "
                       "and 60 is 15 × 4." % (fr(4, 6), fr(2, 3), xv, fr(2, 3)), 10))
    x = F(12 * 15, 9); check(9, 12, 15, x)
    its.append(solve_q(fr(9, 12), fr(15, xv), x, [18, F(45, 4), 180],
                       "%s = %s, and 15 = 3 × 5, so %s = 4 × 5 = <b>20</b>. 18 adds 6 like 9 + 6 = 15, "
                       "11.25 is 15 × 9 ÷ 12, and 180 is 12 × 15." % (fr(9, 12), fr(3, 4), xv), 20))
    x = F(5, 2) * 6 / 4; check(x, F(5, 2), 6, 4)
    its.append(solve_q(fr(xv, "2.5"), fr(6, 4), x, [F(9, 2), 15, F(3, 2)],
                       "6 ÷ 4 = 1.5, so %s = 1.5 × 2.5 = <b>3.75</b>. 4.5 subtracts 1.5 like 4 − 1.5 = 2.5, "
                       "15 is 2.5 × 6, and 1.5 is only the ratio 6 ÷ 4." % xv, F(15, 4)))
    x = F(4 * 9, 6); check(4, 6, x, 9)
    its.append(mcq("Owen solves %s = %s and gets 7, because 6 + 3 = 9 and 4 + 3 = 7. What is the correct answer?"
                   % (fr(4, 6), fr(xv, 9)),
                   "6", ["7", "13.5", "36"],
                   "Ratios grow by multiplying, not adding. 9 = 6 × 1.5, so %s = 4 × 1.5 = <b>6</b>. "
                   "Check: %s = %s = %s. 13.5 inverts the ratio, and 36 is 4 × 9." % (xv, fr(4, 6), fr(6, 9), fr(2, 3)), value=x))
    x = F(250 * 3, 5); check(x, 250, 3, 5)
    its.append(solve_q(fr(xv, 250), fr(3, 5), x, [248, 750, 50],
                       "250 = 5 × 50, so %s = 3 × 50 = <b>150</b>. 248 subtracts 2 like 5 − 2 = 3, "
                       "750 is 250 × 3, and 50 is only the multiplier." % xv, 150))
    x = F(3 * 20) / F(15, 2); check(3, x, F(15, 2), 20)
    its.append(solve_q(fr(3, xv), fr("7.5", 20), x, [F(31, 2), 50, F(9, 8)],
                       "Cross-multiply: 7.5%s = 3 × 20 = 60, so %s = 60 ÷ 7.5 = <b>8</b>. 15.5 subtracts 4.5 like 7.5 − 4.5 = 3, "
                       "50 is 7.5 × 20 ÷ 3, and 1.125 is 3 × 7.5 ÷ 20." % (xv, xv), 8))
    x = F(18 * 5, 6); check(x, 18, 5, 6)
    its.append(mcq("Which value of %s makes %s:18 equivalent to 5:6?" % (xv, xv), "15", ["17", "21.6", "90"],
                   "18 = 6 × 3, so %s = 5 × 3 = <b>15</b>. 17 adds 12 like 6 + 12 = 18, 21.6 is 18 × 6 ÷ 5, "
                   "and 90 is 18 × 5." % xv, value=x))
    assert len(its) == 20, len(its)
    return {"title": "Solving proportions", "items": its}


# ============================================================ set 4: comparing rates
def per(c, q):
    return F(c) / F(q)


def set_rates():
    its = []
    a, b = per(F(9, 2), 6), per(F(36, 5), 10)
    assert b < a
    its.append(mcq("Which is the better buy: 6 granola bars for $4.50 or 10 granola bars for $7.20?",
                   "10 for $7.20", ["6 for $4.50", SAME, CANT],
                   "Price for 1 bar: $4.50 ÷ 6 = %s and $7.20 ÷ 10 = %s. <b>10 for $7.20</b> costs less per bar."
                   % (money(a), money(b))))
    x = per(F(438, 100), 2)
    its.append(mcq("A 2 L carton of milk costs $4.38. What is the price per litre?", money(x),
                   ["$8.76", "$2.38", "$6.38"],
                   "Divide the cost by the litres: $4.38 ÷ 2 = <b>%s</b> per litre. $8.76 multiplies, "
                   "$2.38 subtracts 2, and $6.38 adds 2." % money(x), value=x))
    e, n_ = F(25, 5), F(14, 3)
    assert n_ < e
    its.append(mcq("Emma runs 5 km in 25 minutes. Noah runs 3 km in 14 minutes. Who runs faster?",
                   "Noah", ["Emma", SAME, CANT],
                   "Minutes for 1 km: Emma 25 ÷ 5 = 5 min. Noah 14 ÷ 3 ≈ 4.67 min. Fewer minutes per kilometre means "
                   "faster, so <b>Noah</b>, even though Emma runs farther."))
    rice = [("1 kg", 1, F(16, 5)), ("2 kg", 2, 6), ("5 kg", 5, F(31, 2)), ("8 kg", 8, 26)]
    u = [per(c, q) for _, q, c in rice]
    assert min(u) == u[1] and u.count(min(u)) == 1
    its.append(mcq("Which bag of rice is the best buy?",
                   "2 kg for $6", ["1 kg for $3.20", "5 kg for $15.50", "8 kg for $26"],
                   "Price per kilogram: 1 kg %s, 2 kg $6 ÷ 2 = %s, 5 kg $15.50 ÷ 5 = %s, 8 kg $26 ÷ 8 = %s. "
                   "The lowest is <b>2 kg for $6</b>. The biggest bag is not always the best buy."
                   % (money(u[0]), money(u[1]), money(u[2]), money(u[3]))))
    b_ = per(36, 4)
    assert F(72, 10) < b_
    its.append(mcq("Car A uses 7.2 L of gas per 100 km. Car B uses 36 L to drive 400 km. Which car uses less gas?",
                   "Car A", ["Car B", SAME, CANT],
                   "Change Car B to litres per 100 km: 400 km is 4 × 100 km, so 36 ÷ 4 = 9 L per 100 km. "
                   "7.2 &lt; 9, so <b>Car A</b> uses less gas."))
    x = F(8) * F(350, 100)
    its.append(mcq("A car uses 8 L of gas per 100 km. How much gas does it use for 350 km?", "28 L",
                   ["24 L", "43.75 L", "2800 L"],
                   "350 km is 3.5 × 100 km. 8 × 3.5 = <b>28 L</b>. 24 L stops at 300 km, 43.75 is 350 ÷ 8, "
                   "and 2800 forgets to divide by 100.", value=x))
    assert per(435, 3) == per(580, 4)
    its.append(mcq("Train A travels 435 km in 3 hours. Train B travels 580 km in 4 hours. Which train is faster?",
                   SAME, ["Train A", "Train B", CANT],
                   "Train A: 435 ÷ 3 = 145 km/h. Train B: 580 ÷ 4 = 145 km/h. <b>They are the same</b>, "
                   "even though Train B goes farther."))
    assert per(234, 12) > per(171, 9)
    its.append(mcq("Priya earns $171 for 9 hours of work. Ethan earns $234 for 12 hours. Who earns more per hour?",
                   "Ethan", ["Priya", SAME, CANT],
                   "Priya: $171 ÷ 9 = $19 an hour. Ethan: $234 ÷ 12 = $19.50 an hour. <b>Ethan</b> earns more per hour."))
    a, b = per(F(385, 100), F(7, 4)), per(F(575, 100), F(5, 2))
    assert a < b
    its.append(mcq("Which is the better buy for orange juice: 1.75 L for $3.85 or 2.5 L for $5.75?",
                   "1.75 L for $3.85", ["2.5 L for $5.75", SAME, CANT],
                   "Price per litre: $3.85 ÷ 1.75 = %s and $5.75 ÷ 2.5 = %s. <b>1.75 L for $3.85</b> is cheaper per litre."
                   % (money(a), money(b))))
    a, b = per(F(68, 10), 4), per(F(1155, 100), 7)
    assert b < a
    its.append(mcq("Which is the better buy for cheese: 400 g for $6.80 or 700 g for $11.55?",
                   "700 g for $11.55", ["400 g for $6.80", SAME, CANT],
                   "Price per 100 g: $6.80 ÷ 4 = %s and $11.55 ÷ 7 = %s. <b>700 g for $11.55</b> costs less per 100 g."
                   % (money(a), money(b))))
    assert per(424, 8) > per(315, 7)
    its.append(mcq("Zoe types 315 words in 7 minutes. Kai types 424 words in 8 minutes. Who types faster?",
                   "Kai", ["Zoe", SAME, CANT],
                   "Words per minute: Zoe 315 ÷ 7 = 45. Kai 424 ÷ 8 = 53. <b>Kai</b> types faster."))
    sw = [("Ava", 100, 80), ("Lucas", 50, 38), ("Sofia", 200, 170), ("Nathan", 400, 360)]
    t50 = [F(t) * 50 / m for _, m, t in sw]
    assert min(t50) == t50[1] and t50.count(min(t50)) == 1
    its.append(mcq("Who swims the fastest?",
                   "Lucas: 50 m in 38 s", ["Ava: 100 m in 80 s", "Sofia: 200 m in 170 s", "Nathan: 400 m in 360 s"],
                   "Compare the time for 50 m: Ava 80 ÷ 2 = 40 s, Lucas 38 s, Sofia 170 ÷ 4 = 42.5 s, Nathan 360 ÷ 8 = 45 s. "
                   "Lucas has the shortest time, so <b>Lucas</b> is the fastest."))
    its.append(mcq(fig(graph_svg(4, 60, 5, 15, xname="Time (h)", yname="Distance (km)",
                                 lines=[(straight(15, 0, 0, 4), "A", GREEN), (straight(12, 0, 0, 4), "B", BLUE)],
                                 dots=[(2, 30), (3, 36)], label="graph of two cyclists")) +
                   "The graph shows two cyclists, A and B, riding at steady speeds. How much faster is cyclist A?",
                   "3 km/h", ["6 km/h", "15 km/h", "12 km/h"],
                   "A: 30 km in 2 h = 15 km/h. B: 36 km in 3 h = 12 km/h. 15 − 12 = <b>3 km/h</b>. "
                   "The steeper line is faster. 15 and 12 km/h are each cyclist’s own speed, and 6 compares the distances 36 − 30.", value=3))
    assert per(62, 40) < F(158, 100)
    its.append(mcq("Station A sells gas for $1.58 per litre. At Station B, 40 L cost $62. Which station is cheaper?",
                   "Station B", ["Station A", SAME, CANT],
                   "Station B: $62 ÷ 40 = $1.55 per litre. $1.55 &lt; $1.58, so <b>Station B</b> is cheaper."))
    a = F(100, 16)
    assert a > 6
    its.append(mcq("Car A goes 16 km on 1 L of gas. Car B uses 6 L per 100 km. Which car uses less gas?",
                   "Car B", ["Car A", SAME, CANT],
                   "Change Car A to litres per 100 km: 100 ÷ 16 = 6.25 L. Car B uses 6 L. 6 &lt; 6.25, so <b>Car B</b> "
                   "uses less gas. Compare the same kind of rate before you decide."))
    a, b = per(F(396, 100), 4), per(F(570, 100), 6)
    assert b < a
    its.append(mcq("Which is the better buy for yogurt: 4 cups for $3.96 or 6 cups for $5.70?",
                   "6 cups for $5.70", ["4 cups for $3.96", SAME, CANT],
                   "Price for 1 cup: $3.96 ÷ 4 = %s and $5.70 ÷ 6 = %s. <b>6 cups for $5.70</b> is cheaper per cup."
                   % (money(a), money(b))))
    x = F(18) / F(45, 60)
    its.append(mcq("A cyclist rides 18 km in 45 minutes. What is the speed in kilometres per hour?", "24 km/h",
                   ["0.4 km/h", "2.5 km/h", "810 km/h"],
                   "45 min = 0.75 h. 18 ÷ 0.75 = <b>24 km/h</b>. Or: 15 min is 6 km, and 60 min is 4 × 6 = 24 km. "
                   "0.4 is km per minute, 2.5 is 45 ÷ 18, and 810 is 18 × 45.", value=x))
    a, b = per(F(42, 10), 50), per(3, 36)
    assert a > b
    its.append(mcq("Leah walks 4.2 km in 50 minutes. Aiden walks 3 km in 36 minutes. Who walks faster?",
                   "Leah", ["Aiden", SAME, CANT],
                   "Distance in 1 hour: Leah 4.2 × %s = 5.04 km. Aiden 3 × %s = 5 km. <b>Leah</b> is a little faster."
                   % (fr(60, 50), fr(60, 36))))
    x = per(F(1485, 100), F(3, 2))
    its.append(mcq("1.5 kg of ground beef costs $14.85. What is the price per kilogram?", money(x),
                   ["$13.35", "$16.35", "$4.95"],
                   "$14.85 ÷ 1.5 = <b>%s</b>. Check: 1.5 × $9.90 = $14.85. $13.35 subtracts 1.5, $16.35 adds 1.5, "
                   "and $4.95 divides by 3." % money(x), value=x))
    a, b = per(410, 5), per(249, 3)
    assert a < b
    its.append(mcq("A ski hill sells a 5-day pass for $410 and a 3-day pass for $249. Which pass costs less per day?",
                   "The 5-day pass", ["The 3-day pass", SAME, CANT],
                   "Price per day: $410 ÷ 5 = $82 and $249 ÷ 3 = $83. <b>The 5-day pass</b> costs less per day, "
                   "but only if you use all 5 days."))
    assert len(its) == 20, len(its)
    return {"title": "Comparing rates: best buys, speed and fuel use", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    x = F(64, 10) * 25
    its.append(mcq("A map has a scale of 1 cm : 25 km. Two towns are 6.4 cm apart on the map. How far apart are they?",
                   num(x) + " km", ["31.4 km", "1600 km", "18.6 km"],
                   "Each centimetre is 25 km. 6.4 × 25 = <b>160 km</b>. 31.4 adds 25, 1600 is a decimal slip, "
                   "and 18.6 subtracts.", value=x))
    x = 9 * F(1, 2)
    its.append(mcq("A floor plan uses the scale 1 cm : 0.5 m. A bedroom is 9 cm long on the plan. How long is the real room?",
                   "4.5 m", ["18 m", "9.5 m", "45 m"],
                   "Each centimetre is 0.5 m. 9 × 0.5 = <b>4.5 m</b>. 18 m divides by 0.5 (the inverted scale), "
                   "and 9.5 m adds 0.5.", value=x))
    x = F(350, 50)
    its.append(mcq("Toronto and Ottawa are about 350 km apart. On a map with a scale of 1 cm : 50 km, how far apart are they?",
                   "7 cm", ["17" + NBSP + "500 cm", "0.14 cm", "300 cm"],
                   "Each 50 km is 1 cm. 350 ÷ 50 = <b>7 cm</b>. 17 500 multiplies instead of dividing, 0.14 is 50 ÷ 350, "
                   "and 300 subtracts 50.", value=x))
    x = F(553 * 100, 500)
    assert x == F(1106, 10)
    its.append(mcq("The CN Tower is 553 m tall. A model of it uses the scale 1:500. How tall is the model?",
                   "110.6 cm", ["11.06 cm", "1106 cm", "276" + NBSP + "500 cm"],
                   "The model is %s of the real height: 553 ÷ 500 = 1.106 m = <b>110.6 cm</b>. 11.06 cm and 1106 cm "
                   "move the decimal point the wrong number of places, and 276 500 cm multiplies by 500." % fr(1, 500),
                   value=x))
    x = F(2 * 20, 8)
    its.append(mcq("A pancake recipe uses 2 cups of flour to make 8 pancakes. How much flour is needed for 20 pancakes?",
                   "5 cups", ["14 cups", "0.8 cups", "4 cups"],
                   "Each cup makes 8 ÷ 2 = 4 pancakes. 20 ÷ 4 = <b>5 cups</b>. 14 adds 12 like 8 + 12 = 20, "
                   "0.8 inverts the ratio, and 4 cups make only 16 pancakes.", value=x))
    x = F(3, 4) * 24 / 36
    its.append(mcq("A maple syrup cookie recipe makes 36 cookies with 0.75 cups of maple syrup. Mei wants to make 24 cookies. "
                   "How much maple syrup does she need?",
                   "0.5 cups", ["1.125 cups", "0.25 cups", "18 cups"],
                   "24 is %s of 36, so use %s × 0.75 = <b>0.5 cups</b>. 1.125 inverts the ratio, 0.25 is only the "
                   "part she leaves out, and 18 is 24 × 0.75." % (fr(2, 3), fr(2, 3)), value=x))
    x = F(450 * 2, 3)
    its.append(mcq("A smoothie uses yogurt and berries in the ratio 2:3. Chloe uses 450 mL of berries. How much yogurt does she need?",
                   "300 mL", ["675 mL", "180 mL", "900 mL"],
                   "450 = 3 × 150, so yogurt = 2 × 150 = <b>300 mL</b>. 675 mL inverts the ratio (3:2), "
                   "180 mL uses 2 out of 5, and 900 mL is 450 × 2.", value=x))
    x = F(75, 10) * F(540, 100)
    its.append(mcq("A car uses 7.5 L of gas per 100 km. The drive from Toronto to Montréal is about 540 km. "
                   "How much gas does the car use?",
                   num(x) + " L", ["72 L", "4050 L", "37.5 L"],
                   "540 km is 5.4 × 100 km. 7.5 × 5.4 = <b>40.5 L</b>. 72 is 540 ÷ 7.5, 4050 forgets to divide by 100, "
                   "and 37.5 L counts only 500 km.", value=x))
    x = F(8) * F(250, 100) * F(3, 2)
    its.append(mcq("A car uses 8 L of gas per 100 km, and gas costs $1.50 per litre. What does the gas cost for a 250 km trip?",
                   money(x), ["$20", "$12", "$300"],
                   "Gas: 8 × 2.5 = 20 L. Cost: 20 × $1.50 = <b>%s</b>. $20 uses the litres as dollars, "
                   "$12 is the cost for only 100 km, and $300 is a decimal slip." % money(x), value=x))
    x = F(50) / F(64, 10) * 100
    its.append(mcq("A car’s gas tank holds 50 L. The car uses 6.4 L per 100 km. How far can it go on a full tank?",
                   num(x) + " km", ["320 km", "7.8 km", "3200 km"],
                   "50 ÷ 6.4 = 7.8125, so the tank lasts 7.8125 × 100 km = <b>781.25 km</b>. 320 and 3200 multiply "
                   "50 by 6.4, and 7.8 forgets that 6.4 L is for 100 km, not 1 km.", value=x))
    its.append(mcq("A 2 cm line on a blueprint shows a 5 m wall. What is the scale?",
                   "1 cm : 2.5 m", ["1 cm : 0.4 m", "1 cm : 3 m", "1 cm : 10 m"],
                   "Divide both by 2: 2 cm : 5 m = <b>1 cm : 2.5 m</b>. 0.4 is 2 ÷ 5 (inverted), 3 is 5 − 2, "
                   "and 10 is 5 × 2."))
    x = F(21, 28) * 140
    its.append(mcq("In one Grade 8 class, 21 of the 28 students skate. If the same ratio holds for all 140 Grade 8 students, "
                   "how many skate?",
                   "105", ["133", "35", "112"],
                   "%s = %s. %s of 140 = <b>105</b>. 133 subtracts 7 like 28 − 21, 35 is the students who do not skate, "
                   "and 112 is 140 − 28." % (fr(21, 28), fr(3, 4), fr(3, 4)), value=x))
    x = 40 * F(7, 2)
    its.append(mcq("It takes about 40 L of maple sap to make 1 L of maple syrup. How much sap is needed for 3.5 L of syrup?",
                   num(x) + " L", ["43.5 L", "1400 L", "120 L"],
                   "40 × 3.5 = <b>140 L</b>. 43.5 adds 3.5, 1400 is a decimal slip, and 120 L makes only 3 L of syrup.",
                   value=x))
    x = F(18) / F(9, 2)
    its.append(mcq("On a canoe trip, Kai paddles at a steady 4.5 km/h. How long does it take him to paddle 18 km?",
                   "4 h", ["81 h", "13.5 h", "22.5 h"],
                   "Time = distance ÷ speed: 18 ÷ 4.5 = <b>4 h</b>. Check: 4 × 4.5 = 18 km. 81 multiplies, "
                   "13.5 subtracts, and 22.5 adds.", value=x))
    a, b = F(3, 2), F(5, 3)
    assert b > a
    its.append(mcq("Lemonade A uses 3 scoops of mix in 2 L of water. Lemonade B uses 5 scoops in 3 L of water. Which is stronger?",
                   "Lemonade B", ["Lemonade A", SAME, CANT],
                   "Scoops per litre: A 3 ÷ 2 = 1.5. B 5 ÷ 3 ≈ 1.67. <b>Lemonade B</b> is stronger. "
                   "Both have 1 more scoop than litres, but that is a difference, not a ratio."))
    x = F(18) * 300 / 45
    its.append(mcq("A printer prints 18 pages in 45 seconds. How many pages does it print in 5 minutes?",
                   "120", ["2", "750", "90"],
                   "5 min = 300 s. 18 ÷ 45 = 0.4 pages per second, and 0.4 × 300 = <b>120</b>. 2 uses 5 seconds, "
                   "750 inverts the rate, and 90 is 18 × 5.", value=x))
    x = F(30) / F(15, 4)
    its.append(mcq("For the Terry Fox Run, Olivia’s family pledges $3.75 for each kilometre she runs. She raises $30. "
                   "How far does she run?",
                   "8 km", ["26.25 km", "112.5 km", "7.5 km"],
                   "Distance = money ÷ rate: $30 ÷ $3.75 = <b>8 km</b>. Check: 8 × $3.75 = $30. 26.25 subtracts, "
                   "112.5 multiplies, and 7.5 rounds $3.75 to $4.", value=x))
    x = F(3 * 20, 8)
    assert x == F(15, 2)
    its.append(mcq("A chili recipe for 8 people uses 3 cans of tomatoes. Arjun is making chili for 20 people. "
                   "How many cans should he buy?",
                   "8", ["7", "15", "60"],
                   "3 ÷ 8 × 20 = 7.5 cans. You can’t buy half a can, and 7 cans would not be enough, so buy <b>8</b>. "
                   "15 adds 12 like 8 + 12 = 20, and 60 is 3 × 20.", value=8))
    old, new = F(36), F(6) * F(480, 100)
    x = old - new
    its.append(mcq("Owen’s family drove 480 km and used 36 L of gas. A new car uses 6 L per 100 km. "
                   "How much less gas would the new car use on the same trip?",
                   num(x) + " L", ["1.5 L", "28.8 L", "30 L"],
                   "New car: 6 × 4.8 = 28.8 L. 36 − 28.8 = <b>7.2 L</b> less. 1.5 L compares 7.5 L and 6 L per 100 km "
                   "(only 100 km), 28.8 L is the new car’s gas, and 30 L is 36 − 6.", value=x))
    x = F(30, 12) * 5
    its.append(mcq("At a skating rink, 12 hot chocolates cost $30. At the same price, what do 5 hot chocolates cost?",
                   money(x), ["$23", "$2.40", "$6"],
                   "One hot chocolate: $30 ÷ 12 = $2.50. 5 × $2.50 = <b>%s</b>. $23 subtracts $7 for 7 fewer drinks, "
                   "$2.40 is 12 ÷ 5, and $6 is 30 ÷ 5." % money(x), value=x))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: scales, recipes and fuel use", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    f_tab = table_svg(["Litres", "Cost ($)"], [[10, 20, 30, 40], ["15.50", "31.00", "46.50", "62.00"]],
                      label="table of litres and cost")
    f_gr = graph_svg(6, 16, 2, 4, lines=[(straight(2, 0, 0, 6), "A", GREEN), (straight(2, 4, 0, 6), "B", BLUE)],
                     dots=[(1, 2), (2, 4), (3, 6)], label="graph of two lines")
    return (
        "<h2>What makes a relationship proportional</h2>"
        "<p>Two amounts are <b>proportional</b> when one is always the same number times the other. "
        "That number is the <b>constant of proportionality</b>, %s = %s. The equation is %s.</p>"
        "<p>Three ways to check: in a table, %s is the same for every pair. On a graph, the points lie on a "
        "<b>straight line through (0, 0)</b>. As an equation, it has the form %s with nothing added.</p>"
        % (KV, YX, X("y = kx"), YX, X("y = kx")) +
        "<figure class='sn-fig'>" + f_tab +
        "<figcaption>15.50 ÷ 10 = 31 ÷ 20 = 1.55 every time. Gas costs $1.55 per litre: cost = 1.55 × litres.</figcaption></figure>" +
        "<figure class='sn-fig'>" + f_gr +
        "<figcaption>Line A (%s) is proportional. Line B (%s) is straight but starts at 4, so it is not.</figcaption></figure>"
        % (X("y = 2x"), X("y = 2x + 4"))
        + ex("Find k", "The point (6, 21) is on a proportional graph. Write the equation.",
             "%s = 21 ÷ 6 = 3.5." % KV, X("y = 3.5x"))
        + "<h2>Solving proportions</h2>"
        "<p>A <b>proportion</b> says two ratios are equal. Keep the same order in both ratios. "
        "Then find the multiplier, or cross-multiply.</p>"
        + ex("Multiplier", "Solve: %s = %s" % (fr(XV, 12), fr(3, 4)),
             "12 = 4 × 3, so multiply the top by 3 too: 3 × 3.", "%s = 9" % XV)
        + ex("Cross-multiply", "Solve: %s = %s" % (fr(6, XV), fr(9, 15)),
             "9%s = 6 × 15 = 90, so %s = 90 ÷ 9." % (XV, XV), "%s = 10" % XV)
        + "<h2>Comparing rates</h2>"
        "<p>To compare two offers or two speeds, change both to a <b>unit rate</b>: the price for 1 L, 1 kg or 100 g, "
        "or the distance in 1 hour. Use the same kind of rate for both.</p>"
        + ex("Best buy", "Orange juice: 1.75 L for $3.85 or 2.5 L for $5.75?",
             "$3.85 ÷ 1.75 = $2.20 per litre. $5.75 ÷ 2.5 = $2.30 per litre.", "1.75 L for $3.85")
        + ex("Fuel use", "A car uses 7.5 L per 100 km. How much gas for 540 km?",
             "540 km is 5.4 × 100 km. 7.5 × 5.4 = 40.5.", "40.5 L")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Adding: %s = %s, so %s = 11 (because 4 + 8 = 12)" % (fr(XV, 12), fr(3, 4), XV),
             "Multiply: 12 = 4 × 3, so %s = 3 × 3 = 9" % XV],
            ["Inverting: %s = %s ÷ %s" % (KV, XV, YV), "%s = %s. For (4, 10), %s = 2.5, not 0.4" % (KV, YX, KV)],
            ["Any straight line is proportional", "It must also go through (0, 0). %s is not proportional" % X("y = 2x + 4")],
            ["A constant difference is proportional (Hana is always 3 years older)",
             "Check %s. A difference that stays the same is additive, not proportional" % YX],
            ["Comparing rates of different kinds (km per L and L per 100 km)", "Change both to the same unit rate first"],
        ])
    )


FAQ = [
    {"q": "What are proportional relationships in Grade 8 math in Ontario?",
     "a": "In the Ontario Grade 8 curriculum (expectation B2.8), students compare proportional situations, find unknown values and use proportional reasoning to solve problems. A proportional relationship has the form y = kx, where k is the constant of proportionality."},
    {"q": "How do you find the constant of proportionality?",
     "a": "Divide y by x for any pair in the table or any point on the line. For (4, 10), k = 10 ÷ 4 = 2.5, so the equation is y = 2.5x."},
    {"q": "How can you tell if a graph is proportional?",
     "a": "The graph must be a straight line that goes through the origin (0, 0). A straight line that starts above 0, like y = 2x + 4, is not proportional."},
    {"q": "How do you solve a proportion like x/12 = 3/4?",
     "a": "Find what you multiply by: 12 = 4 × 3, so x = 3 × 3 = 9. You can also cross-multiply: 4x = 36, so x = 9. Never add the same number to both parts."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(48808)
    sets = [set_check(), set_k(), set_solve(), set_rates(), set_problems()]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it["q"]
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": SLUG, "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Proportional Relationships: y = kx, Solving Proportions and Comparing Rates",
        "seo_title": "Grade 8 Proportional Relationships Worksheets: y = kx, Proportions and Best Buys (Ontario Math, Free)",
        "short_title": "Proportional relationships",
        "domain": "Number",
        "standard_code": "Grade 8: B2.8",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Compare proportional situations and determine unknown values in proportional situations, and apply proportional reasoning to solve problems in various contexts",
        "meta_desc": "Free Grade 8 math worksheets on proportional relationships for the Ontario curriculum: tell whether tables, graphs and equations are proportional, find the constant of proportionality k in y = kx, solve proportions, compare rates and best buys, and solve scale, recipe and fuel problems. 100 questions with an answer key.",
        "key_big": "In a proportional relationship, y ÷ x is the same every time: y = kx, and the graph is a straight line through (0, 0).",
        "key_sub": "Multiply, don’t add: if x/12 = 3/4, then x = 9, not 11. Find k as y ÷ x, not x ÷ y. To compare offers or speeds, change both to the same unit rate first.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "graph")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
