# -*- coding: utf-8 -*-
"""
CA-ON Grade 7 Math: Algebraic Expressions (Ontario Mathematics Curriculum 2020, Grade 7: Algebra, C2.1 and C2.2)
  python3 tools/gen_caon_math_g7_expressions.py
Terms, coefficients, constants and like terms (with algebra tiles), adding and subtracting monomials of degree 1
(3x + 5x, 7x − 2x), evaluating expressions with whole numbers and with decimal numbers (2.5n + 4 when n = 3),
writing expressions from words, and word problems in Canadian contexts.
Wrong answers come from real student mistakes: 3x + 2 = 5x (joining unlike terms), reading 3x as 3 + x (or as 34
when x = 4), multiplying the coefficients (3x + 5x = 15x), turning x into x^2 when adding, dropping the variable
(7x − 2x = 5), forgetting that x means 1x, adding before multiplying, ignoring brackets, multiplying only the
whole-number part of a decimal, and writing “8 less than n” as 8 − n.
Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
XT = "#7fc495"      # x-tile
ONE = "#f4d35e"     # 1-tile
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """Ontario style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
    v = Fr(v)
    neg = v < 0
    v = abs(v)
    for k in range(0, 5):
        t = v * 10 ** k
        if t.denominator == 1:
            w, r = divmod(t.numerator, 10 ** k)
            s = str(w)
            if len(s) >= 5:
                g = []
                while s:
                    g.insert(0, s[-3:])
                    s = s[:-3]
                s = NBSP.join(g)
            if k:
                s += "." + str(r).rjust(k, "0")
            return (M if neg else "") + s
    raise ValueError(v)


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1, v
    w, r = divmod(c.numerator, 100)
    return "$%s.%02d" % (n(w), r)


def plain(s):
    return re.sub(r"<[^>]+>", "", s).replace(NBSP, " ")


# ------------------------------------------------------------ expressions
def X(s):
    """Plain expression '3x^2 + 2y - 4' -> HTML: letters in italics, ^2 as a superscript, real minus sign."""
    s = s.replace("-", M).replace("*", "×").replace("/", "÷")
    s = re.sub(r"[a-z]", lambda m: "<i>%s</i>" % m.group(), s)
    return re.sub(r"\^(\d)", r"<sup>\1</sup>", s)


def ev(expr_, **env):
    """Exact value of a plain expression with the letters given in env."""
    t = expr_.replace(M, "-").replace("×", "*").replace("÷", "/").replace("^", "**").replace(" ", "")
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Q('%s')" % m.group(), t)
    t = re.sub(r"(\)|[a-z])(?=[a-zQ(])", r"\1*", t)
    e = {"Q": Fr}
    for k, v in env.items():
        e[k] = Fr(v)
    return eval(t, {"__builtins__": {}}, e)


def same(a, b):
    """True when two one-letter (or no-letter) expressions are equal for several values."""
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2)):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None, neg=False):
    """correct and cands are numbers shown with disp, or HTML strings. Equal values are skipped."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pick = {plain(cs)}, {cv}, []
    for c in cands:
        if c is None:
            continue
        if disp is not None:
            c = Fr(c)
            if (c < 0 and not neg) or c in vals:
                continue
            vals.add(c)
            c = disp(c)
        if plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def emcq(q, good, bad, e, rnd, check=True):
    """Expression choices (plain text); wrong ones must not be equivalent to the right one."""
    if check:
        for b in bad:
            assert not same(good, b), (good, b)
    return mcq(q, X(good), [X(b) for b in bad], e, rnd)


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def SX(s):
    """Expression inside an SVG text: letters in italics with a tspan."""
    return re.sub(r"[a-z]", lambda m: "<tspan font-style='italic'>%s</tspan>" % m.group(), s.replace("-", M))


TW, TH, T1, TP, PAD = 22, 58, 22, 28, 6


def x_tile(x, y, crossed=False):
    s = ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x, y, TW, TH, "#e9f4ec" if crossed else XT, GREEN))
    s += text(x + TW / 2, y + TH / 2 + 6, "<tspan font-style='italic'>x</tspan>", 17, col=INK)
    if crossed:
        s += ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
              "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
              % (x - 2, y + 4, x + TW + 2, y + TH - 4, RED, x + TW + 2, y + 4, x - 2, y + TH - 4, RED))
    return s


def one_tile(x, y):
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x, y, T1, T1, ONE, "#8a6d00") + text(x + T1 / 2, y + T1 / 2 + 5, "1", 14, col=INK))


def tiles_svg(groups, ops=(), label="algebra tiles"):
    """groups: list of (number of x-tiles, number of 1-tiles, number of x-tiles crossed out).
    ops: '+' or '−' drawn between the groups. 1-tiles stand in columns of 2, at the bottom."""
    x = PAD
    s = []
    for gi, (nx, n1, cr) in enumerate(groups):
        if gi:
            s.append(text(x + 12, PAD + TH / 2 + 9, ops[gi - 1], 26, col=INK))
            x += 30
        for i in range(nx):
            s.append(x_tile(x, PAD, i >= nx - cr))
            x += TP
        if n1:
            x += 4 if nx else 0
            cols = (n1 + 1) // 2
            for i in range(n1):
                c, r = divmod(i, 2)
                s.append(one_tile(x + c * TP, PAD + TH - T1 - r * (T1 + 6)))
            x += cols * TP
    W = x - (TP - TW) + PAD
    return svg_wrap(W, TH + 2 * PAD, "".join(s), label)


def rect_svg(top, side, label):
    w, h = 170, 82
    L, T = 56, 30
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, SX(top), 17))
    s.append(text(L - 8, T + h / 2 + 6, SX(side), 17, "end"))
    return svg_wrap(L + w + 12, T + h + 10, "".join(s), label)


def tri_svg(a, b, c, label):
    """Triangle with sides labelled a (left), b (right), c (bottom)."""
    P = [(40, 120), (250, 120), (150, 20)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%d,%d" % p for p in P), FILL, GREEN)]
    s.append(text(84, 64, SX(a), 17, "end"))
    s.append(text(212, 64, SX(b), 17, "start"))
    s.append(text(145, 143, SX(c), 17))
    return svg_wrap(300, 152, "".join(s), label)


def table_svg(head, top, bot, label):
    CW, LW, RH = 58, 92, 32
    k = len(top)
    W, H = LW + CW * k + 4, RH * 2 + 4
    s = []
    for r, (name, row) in enumerate([(head[0], top), (head[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 6, name, 16))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lin(a, b, var="x"):
    """Plain text of a·var + b: 3x + 2, 4x − 1, x + 5, 2.5x."""
    a, b = Fr(a), Fr(b)
    s = ("" if a == 1 else n(a)) + var
    if b > 0:
        s += " + " + n(b)
    elif b < 0:
        s += " - " + n(-b)
    return s


def tile_expr(a, b):
    return lin(a, b) if a else n(b)


# ============================================================ set 1: terms, coefficients and like terms
def set_terms(rnd):
    its = []
    # A: what 3x means
    its.append((0, mcq("What does %s mean?" % X("4n"), "4 × " + X("n"),
                       ["4 + " + X("n"), X("n") + " × " + X("n") + " × " + X("n") + " × " + X("n"), X("n") + " − 4"],
                       "A number written in front of a letter means multiply: 4" + X("n") + " = 4 × " + X("n") +
                       ". It is not 4 + " + X("n") + ". (" + X("n") + " × " + X("n") + " × " + X("n") + " × " + X("n") +
                       " is " + X("n^4") + ".)", rnd)))
    its.append((0, emcq("Which expression means the same as %s?" % X("y + y + y + y + y"), "5y",
                        ["y^5", "5 + y", "4y"],
                        "Five " + X("y") + "’s added together make 5" + X("y") + ". Count the " + X("y") +
                        "’s, not the + signs (that gives 4" + X("y") + "). " + X("y^5") + " means " + X("y") +
                        " × " + X("y") + " × " + X("y") + " × " + X("y") + " × " + X("y") + ".", rnd)))
    assert ev("3n", n=6) == 18
    its.append((0, mcq("When %s = 6, what is the value of %s?" % (X("n"), X("3n")), 18, [9, 36, 3],
                       "3" + X("n") + " means 3 × " + X("n") + " = 3 × 6 = 18. (3 + 6 = 9 reads 3" + X("n") +
                       " as 3 + " + X("n") + ". 36 just writes the digits side by side.)", rnd, n)))
    # B: coefficients
    for s_, var, ans, wrong, note in [
        ("7x + 4", "x", 7, [4, 11, 1], "The constant 4 has no variable."),
        ("x + 9", "x", 1, [0, 9, 10], X("x") + " means 1" + X("x") + ", so the coefficient is 1, not 0."),
        ("12 + 8m", "m", 8, [12, 20, 1], "The order does not matter: 8 is the number multiplied by " + X("m") + "."),
        ("2.5t + 6", "t", Fr("2.5"), [6, Fr("8.5"), 2], "A coefficient can be a decimal number."),
    ]:
        q = "What is the coefficient of %s in %s?" % (X(var), X(s_))
        e = "The coefficient is the number multiplied by the variable. In %s, it is %s. %s" % (X(s_), n(ans), note)
        its.append((1, mcq(q, ans, wrong, e, rnd, n)))
    # C: constant term and number of terms
    its.append((2, mcq("What is the constant term in %s?" % X("6n + 15"), "15", ["6", X("6n"), "21"],
                       "The constant term is the number with no variable: 15. (6 is the coefficient of " + X("n") + ".)", rnd)))
    its.append((2, mcq("What is the constant term in %s?" % X("4 + 9y"), "4", ["9", X("9y"), "13"],
                       "4 has no variable, so it is the constant term. It can come first. (9 is the coefficient of " +
                       X("y") + ".)", rnd)))
    its.append((2, mcq("How many terms are in %s?" % X("3a + 5b + 7"), "3 terms", ["2 terms", "1 term", "4 terms"],
                       "Terms are separated by + and − signs: 3" + X("a") + ", 5" + X("b") + " and 7. That is 3 terms. "
                       "(The constant 7 is a term too.)", rnd)))
    its.append((2, mcq("How many terms are in %s?" % X("5x + 2 + x + 8"), "4 terms", ["2 terms", "3 terms", "5 terms"],
                       "Count the parts between the + signs: 5" + X("x") + ", 2, " + X("x") + " and 8. That is 4 terms. "
                       "After combining like terms it becomes 6" + X("x") + " + 10, which has 2 terms.", rnd)))
    # D: like terms
    its.append((3, mcq("Which term is a like term with %s?" % X("6x"), X("2x"), [X("6y"), "6", X("x^2")],
                       "Like terms have exactly the same variable part. 2" + X("x") + " and 6" + X("x") +
                       " both have " + X("x") + ". 6" + X("y") + " has the same number but a different letter, and " +
                       X("x^2") + " is " + X("x") + " × " + X("x") + ".", rnd)))
    its.append((3, mcq("Which pair are like terms?", X("4m") + " and " + X("m"),
                       [X("4m") + " and " + X("4n"), X("4m") + " and 4", X("m") + " and " + X("n")],
                       "4" + X("m") + " and " + X("m") + " both have the variable " + X("m") +
                       ", so they are like terms (" + X("m") + " = 1" + X("m") + "). The coefficient does not need to match.",
                       rnd)))
    its.append((3, mcq("Which term is a like term with 9?", "15", [X("9x"), X("9y"), X("x")],
                       "Constant terms are all like terms with each other: 9 and 15 have no variable. 9" + X("x") +
                       " has a variable, so it is not like 9.", rnd)))
    its.append((3, emcq("Which expression has only like terms?", "3k + 5k + k",
                        ["3k + 5 + k", "3k + 5j", "3 + 5k"],
                        "In 3" + X("k") + " + 5" + X("k") + " + " + X("k") + " every term has the variable " + X("k") +
                        ". The others mix a " + X("k") + "-term with a constant or with a different letter.", rnd)))
    # E: read algebra tiles
    for a, b in [(3, 2), (4, 5), (2, 6), (5, 1), (1, 4)]:
        good = tile_expr(a, b)
        bad = [lin(a + b, 0), lin(b, a) if a != b else None, n(a + b), lin(a, 0)]
        if a == 1:
            bad = [lin(a + b, 0), lin(b, a), lin(b, 0)]
        bad = [x for x in bad if x]
        q = fig(tiles_svg([(a, b, 0)], label="algebra tiles: %d x-tiles and %d one-tiles" % (a, b))) + \
            "Each green tile is %s and each yellow tile is 1. Which expression do the algebra tiles show?" % X("x")
        e = ("There %s %d green %s (%s) and %d yellow %s (%s), so the expression is %s. Green and yellow tiles are "
             "not like terms, so they cannot be joined: %s is not %s." % (
                 "is" if a == 1 else "are", a, "tile" if a == 1 else "tiles", X(lin(a, 0)), b,
                 "tile" if b == 1 else "tiles", n(b), X(good), X(good), X(lin(a + b, 0))))
        its.append((4, mcq(q, X(good), [X(x) for x in bad], e, rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Terms, coefficients and like terms", "items": [i for _, i in its]}


# ============================================================ set 2: add and subtract like terms
def set_combine(rnd):
    its = []
    # A: adding with tiles
    for a, b in [(3, 5), (2, 4), (1, 6), (4, 3)]:
        s_ = "%s + %s" % (lin(a, 0), lin(b, 0))
        good = lin(a + b, 0)
        bad = [lin(a + b, 0) + "^2", lin(a * b, 0) if a * b != a + b and a != 1 else lin(max(a, b), 0), n(a + b)]
        q = (fig(tiles_svg([(a, 0, 0), (b, 0, 0)], "+", "algebra tiles: %d x-tiles plus %d x-tiles" % (a, b))) +
             "The algebra tiles show %s. Which expression is the sum?" % X(s_))
        e = ("Count the x-tiles: %d + %d = %d, so %s = %s. Add the coefficients and keep the %s. "
             "Adding does not change %s into %s." % (a, b, a + b, X(s_), X(good), X("x"), X("x"), X("x^2")))
        if a == 1:
            e += " " + X("x") + " means 1" + X("x") + ", so it counts as 1 tile."
        if a * b != a + b and a != 1:
            e += " Do not multiply the coefficients: %d × %d = %d is wrong." % (a, b, a * b)
        its.append((0, emcq(q, good, bad, e, rnd)))
    # B: subtracting with tiles (take away)
    for a, b in [(7, 2), (6, 4), (8, 3)]:
        s_ = "%s - %s" % (lin(a, 0), lin(b, 0))
        good = lin(a - b, 0)
        bad = [n(a - b), lin(a + b, 0), lin(a - b, 0) + "^2"]
        q = (fig(tiles_svg([(a, 0, b)], label="algebra tiles: %d x-tiles with %d crossed out" % (a, b))) +
             "Start with %d x-tiles and take away %d. Which expression equals %s?" % (a, b, X(s_)))
        e = ("%d x-tiles take away %d x-tiles leaves %d x-tiles: %s = %s. The answer is still a number of %s’s, "
             "so keep the %s (%d alone is wrong)." % (a, b, a - b, X(s_), X(good), X("x"), X("x"), a - b))
        its.append((1, emcq(q, good, bad, e, rnd)))
    # C: without tiles
    rows = [
        ("9m + 6m", "15m", ["15m^2", "54m", "15"],
         "Add the coefficients: 9 + 6 = 15, so 9" + X("m") + " + 6" + X("m") + " = 15" + X("m") + ". Do not multiply 9 × 6, and do not change " + X("m") + " to " + X("m^2") + "."),
        ("12k - 5k", "7k", ["7", "17k", "7k^2"],
         "Subtract the coefficients: 12 − 5 = 7, so 12" + X("k") + " − 5" + X("k") + " = 7" + X("k") + ". The " + X("k") + " stays."),
        ("10y - y", "9y", ["10", "9", "10y"],
         X("y") + " means 1" + X("y") + ": 10" + X("y") + " − 1" + X("y") + " = 9" + X("y") + ". (10 is wrong: taking away " + X("y") + " does not remove the letter from 10" + X("y") + ".)"),
        ("4.5n + 2.5n", "7n", ["6.10n", "7n^2", "7"],
         "Add the decimal coefficients: 4.5 + 2.5 = 7, so the sum is 7" + X("n") + ". (6.10" + X("n") + " adds 4 + 2 and 5 + 5 separately.)"),
        ("8a + 3a - 4a", "7a", ["15a", "a", "7"],
         "Work left to right: 8 + 3 = 11, then 11 − 4 = 7. So the result is 7" + X("a") + ". (15" + X("a") + " adds the 4" + X("a") + " instead of subtracting it. " + X("a") + " comes from 8 − 3 − 4, which subtracts the 3" + X("a") + " too.)"),
    ]
    for s_, good, bad, e in rows:
        assert same(good, s_)
        its.append((2, emcq("Simplify %s." % X(s_), good, bad, e, rnd)))
    # D: with constants
    rows = [
        ("3x + 2 + 4x", "7x + 2", ["9x", "7x^2 + 2", "3x + 6"],
         "The like terms are 3" + X("x") + " and 4" + X("x") + ": 3" + X("x") + " + 4" + X("x") + " = 7" + X("x") + ". The 2 is a constant, so it stays: 7" + X("x") + " + 2. (9" + X("x") + " joins the 2 to the " + X("x") + "-terms.)"),
        ("5n + 3 + 2", "5n + 5", ["10n", "10", "7n + 3"],
         "Only 3 and 2 are like terms: 3 + 2 = 5. The 5" + X("n") + " has no other " + X("n") + "-term, so the answer is 5" + X("n") + " + 5. It is not 10" + X("n") + "."),
        ("8k + 6 - 3k", "5k + 6", ["11k", "11k + 6", "8k + 3"],
         "Combine the " + X("k") + "-terms: 8" + X("k") + " − 3" + X("k") + " = 5" + X("k") + ". The constant 6 stays: 5" + X("k") + " + 6. (The minus sign belongs to 3" + X("k") + ", not to the 6.)"),
        ("6x + 4 + x + 2", "7x + 6", ["13x", "6x + 6", "7x^2 + 6"],
         X("x") + "-terms: 6" + X("x") + " + 1" + X("x") + " = 7" + X("x") + ". Constants: 4 + 2 = 6. The answer is 7" + X("x") + " + 6. (6" + X("x") + " + 6 forgets that " + X("x") + " is 1" + X("x") + ".)"),
        ("9y + 7 - 4y - 2", "5y + 5", ["13y + 5", "5y + 9", "10y"],
         X("y") + "-terms: 9" + X("y") + " − 4" + X("y") + " = 5" + X("y") + ". Constants: 7 − 2 = 5. The answer is 5" + X("y") + " + 5. (Each minus sign belongs to the term right after it.)"),
    ]
    for s_, good, bad, e in rows:
        assert same(good, s_)
        its.append((3, emcq("Simplify %s." % X(s_), good, bad, e, rnd)))
    # E: 3x + 2 is not 5x, perimeters
    assert ev("3x + 2", x=4) == 14 and ev("5x", x=4) == 20
    its.append((4, mcq("Zoe says 3" + X("x") + " + 2 = 5" + X("x") + ". Test it with " + X("x") + " = 4. What are the values of 3" +
                       X("x") + " + 2 and 5" + X("x") + "?", "14 and 20", ["20 and 20", "9 and 20", "14 and 14"],
                       "3 × 4 + 2 = 14, but 5 × 4 = 20. The values are different, so 3" + X("x") + " + 2 ≠ 5" + X("x") +
                       ". 3" + X("x") + " and 2 are not like terms, so they cannot be added.", rnd)))
    its.append((4, emcq(fig(rect_svg("3x", "2x", "rectangle with length 3x and width 2x")) +
                        "Which expression gives the perimeter of the rectangle?", "10x", ["5x", "6x^2", "10x^2"],
                        "The perimeter is all four sides: 3" + X("x") + " + 2" + X("x") + " + 3" + X("x") + " + 2" + X("x") +
                        " = 10" + X("x") + ". (5" + X("x") + " adds only two sides. 6" + X("x^2") + " multiplies, which gives the area.)",
                        rnd)))
    its.append((4, emcq(fig(tri_svg("4x", "4x", "3x + 5", "triangle with sides 4x, 4x and 3x + 5")) +
                        "Which expression gives the perimeter of the triangle?", "11x + 5", ["16x", "11x", "8x + 5"],
                        "Add the sides: 4" + X("x") + " + 4" + X("x") + " + 3" + X("x") + " + 5. " + X("x") +
                        "-terms: 4 + 4 + 3 = 11, so 11" + X("x") + ". The constant 5 stays: 11" + X("x") +
                        " + 5. (16" + X("x") + " joins the 5 to the " + X("x") + "-terms.)", rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Add and subtract like terms", "items": [i for _, i in its]}


# ============================================================ set 3: evaluate with whole numbers
def lin_case(a, b, var, v, rnd, level):
    a, b, v = Fr(a), Fr(b), Fr(v)
    s_ = lin(a, b, var)
    ans = ev(s_, **{var: v})
    assert ans == a * v + b
    sg = "+" if b > 0 else "−"
    q = "Evaluate %s when %s = %s." % (X(s_), X(var), n(v))
    e = ("Replace %s with %s and multiply first: %s × %s %s %s = %s %s %s = %s. (%s means %s × %s, not %s + %s.)"
         % (X(var), n(v), n(a), n(v), sg, n(abs(b)), n(a * v), sg, n(abs(b)), n(ans),
            X(n(a) + var), n(a), X(var), n(a), X(var)))
    cands = []
    if v.denominator != 1 and v > 1:
        wp = Fr(int(v))
        cands.append(a * wp + (v - wp) + b)             # 4 × 2.5 done as 4 × 2 + 0.5
    cands += [a + v + b, a * (v + b) if b > 0 else a * (v - abs(b))]
    if v.denominator == 1 and a.denominator == 1:
        cands.append(Fr(n(a) + n(v)) + b)              # 3x read as 34 when x = 4
    cands += [a * v, a * v - b]
    return (level, mcq(q, ans, cands, e, rnd, n, neg=ans < 0))


def set_whole(rnd):
    its = []
    for a, b, var, v in [(3, 5, "x", 4), (6, -4, "n", 7), (5, 8, "k", 9), (9, -7, "m", 12), (2, 15, "t", 25), (7, 6, "y", 10)]:
        its.append(lin_case(a, b, var, v, rnd, 0))
    rows = [
        ("2(n + 3)", {"n": 5}, [13, 10, 8],
         "Brackets first: 5 + 3 = 8. Then 2 × 8 = 16. (2 × 5 + 3 = 13 forgets to multiply the 3 by 2.)"),
        ("20 - 3n", {"n": 4}, [68, 13, 16],
         "Multiply first: 3 × 4 = 12. Then 20 − 12 = 8. (20 − 3 = 17, then 17 × 4 = 68 works left to right, which is wrong.)"),
        ("n ÷ 4 + 6", {"n": 24}, ["2.4", 6, 30],
         "Divide first: 24 ÷ 4 = 6. Then 6 + 6 = 12. (24 ÷ (4 + 6) = 2.4 adds first.)"),
        ("4(2n - 1)", {"n": 6}, [47, 11, 52],
         "Brackets first: 2 × 6 − 1 = 11. Then 4 × 11 = 44. (4 × 2 × 6 − 1 = 47 ignores the brackets.)"),
        ("3(n + 4) - 5", {"n": 6}, [17, 30, 35],
         "Brackets first: 6 + 4 = 10. Then 3 × 10 = 30, and 30 − 5 = 25. (3 × 6 + 4 − 5 = 17 ignores the brackets. 30 forgets to subtract the 5.)"),
    ]
    for s_, env, wrong, e in rows:
        ans = ev(s_, **env)
        var, v = list(env.items())[0]
        its.append((1, mcq("Evaluate %s when %s = %s." % (X(s_), X(var), n(v)), ans, [Fr(w) for w in wrong], e, rnd, n)))
    rows = [
        ("n^2 + 5", 6, [17, 121, 11],
         X("n^2") + " means " + X("n") + " × " + X("n") + ": 6 × 6 = 36. Then 36 + 5 = 41. (2 × 6 + 5 = 17 reads " + X("n^2") + " as 2" + X("n") + ".)"),
        ("2n^2", 3, [36, 12, 9],
         "The exponent goes with " + X("n") + " only: 3<sup>2</sup> = 9, then 2 × 9 = 18. ((2 × 3)<sup>2</sup> = 36 squares the 2 as well.)"),
        ("n^3 - 10", 4, [2, 64, 6],
         X("n^3") + " = 4 × 4 × 4 = 64. Then 64 − 10 = 54. (3 × 4 − 10 = 2 reads " + X("n^3") + " as 3" + X("n") + ". 4<sup>2</sup> − 10 = 6 uses the wrong power.)"),
    ]
    for s_, v, wrong, e in rows:
        ans = ev(s_, n=v)
        its.append((2, mcq("Evaluate %s when %s = %s." % (X(s_), X("n"), n(v)), ans, wrong, e, rnd, n)))
    rows = [
        ("3a + 2b", {"a": 5, "b": 4}, [22, 14, 59],
         "Replace each letter: 3 × 5 + 2 × 4 = 15 + 8 = 23. (22 puts the 4 in for " + X("a") + " and the 5 in for " + X("b") + ".)"),
        ("5x - 2y", {"x": 6, "y": 7}, [23, 2, 30],
         "5 × 6 − 2 × 7 = 30 − 14 = 16. (23 swaps the values of " + X("x") + " and " + X("y") + ". 30 forgets the 2" + X("y") + ".)"),
        ("xy + 4", {"x": 3, "y": 8}, [15, 42, 36],
         X("xy") + " means " + X("x") + " × " + X("y") + " = 3 × 8 = 24. Then 24 + 4 = 28. (3 + 8 + 4 = 15 adds instead of multiplying.)"),
        ("4m - n + 6", {"m": 5, "n": 9}, [5, 35, 6],
         "4 × 5 − 9 + 6 = 20 − 9 + 6 = 17. Work left to right after multiplying. (20 − (9 + 6) = 5 subtracts the 6 too.)"),
    ]
    for s_, env, wrong, e in rows:
        ans = ev(s_, **env)
        cond = " and ".join("%s = %s" % (X(k), n(v)) for k, v in env.items())
        its.append((3, mcq("Evaluate %s when %s." % (X(s_), cond), ans, wrong, e, rnd, n)))
    for v, target, good, bad in [(6, 30, "4n + 6", ["6n + 4", "3n + 6", "5n - 6"]),
                                 (8, 20, "3n - 4", ["4n - 3", "2n + 6", "n + 10"])]:
        assert ev(good, n=v) == target and all(ev(b, n=v) != target for b in bad)
        q = "Which expression has a value of %s when %s = %s?" % (n(target), X("n"), n(v))
        e = "Check each one: %s. Only %s gives %s." % (
            "; ".join("%s = %s" % (X(x), n(ev(x, n=v))) for x in [good] + bad), X(good), n(target))
        its.append((4, emcq(q, good, bad, e, rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate expressions with whole numbers", "items": [i for _, i in its]}


# ============================================================ set 4: evaluate with decimals
def set_decimals(rnd):
    its = []
    for a, b, var, v in [("2.5", 4, "n", 3), (4, "-1.5", "n", "2.5"), ("0.5", 3, "x", 8), ("1.2", 6, "k", 5),
                         (3, "2.4", "n", "1.6"), (6, "-2.5", "m", "1.25"), ("0.8", "1.5", "t", 4), (10, "-3.6", "x", "0.9"), ("1.5", 7, "y", "4.2")]:
        its.append(lin_case(a, b, var, v, rnd, 0))
    rows = [
        ("2(n + 1.5)", "4.5", ["10.5", "6", "8"],
         "Brackets first: 4.5 + 1.5 = 6. Then 2 × 6 = 12. (2 × 4.5 + 1.5 = 10.5 forgets to double the 1.5.)"),
        ("5(n - 0.4)", "2", ["9.6", "1.6", "6.6"],
         "Brackets first: 2 − 0.4 = 1.6. Then 5 × 1.6 = 8. (5 × 2 − 0.4 = 9.6 ignores the brackets.)"),
        ("(n + 2.6) ÷ 2", "5.4", ["6.7", "8", "16"],
         "Brackets first: 5.4 + 2.6 = 8. Then 8 ÷ 2 = 4. (5.4 + 2.6 ÷ 2 = 6.7 ignores the brackets.)"),
    ]
    for s_, v, wrong, e in rows:
        ans = ev(s_, n=Fr(v))
        its.append((1, mcq("Evaluate %s when %s = %s." % (X(s_), X("n"), n(Fr(v))), ans, [Fr(w) for w in wrong], e, rnd, n)))
    assert ev("n^2", n=Fr("0.3")) == Fr("0.09")
    its.append((2, mcq("Evaluate %s when %s = 0.3." % (X("n^2"), X("n")), Fr("0.09"), [Fr("0.9"), Fr("0.6"), Fr("0.03")],
                       "0.3 × 0.3 = 0.09: 3 × 3 = 9, and the answer needs 2 decimal places. (0.9 has only 1 decimal place. 0.6 is 2 × 0.3, not 0.3 × 0.3.)",
                       rnd, n)))
    assert ev("n^2 + 1.5", n=Fr("1.2")) == Fr("2.94")
    its.append((2, mcq("Evaluate %s when %s = 1.2." % (X("n^2 + 1.5"), X("n")), Fr("2.94"), [Fr("3.9"), Fr("7.29"), Fr("1.44")],
                       "Square first: 1.2 × 1.2 = 1.44. Then 1.44 + 1.5 = 2.94. (2 × 1.2 + 1.5 = 3.9 reads " + X("n^2") +
                       " as 2" + X("n") + ". (1.2 + 1.5)<sup>2</sup> = 7.29 adds first.)", rnd, n)))
    # negative results
    assert ev("2.5x - 9", x=3) == Fr("-1.5")
    its.append((2, mcq("Evaluate %s when %s = 3." % (X("2.5x - 9"), X("x")), Fr("-1.5"), [Fr("1.5"), Fr("-3.5"), Fr("16.5")],
                       "2.5 × 3 = 7.5. Then 7.5 − 9 = −1.5. The result is negative because 9 is greater than 7.5. "
                       "(1.5 subtracts the wrong way round.)", rnd, n, neg=True)))
    assert ev("4 - 1.5n", n=6) == -5
    its.append((2, mcq("Evaluate %s when %s = 6." % (X("4 - 1.5n"), X("n")), -5, [5, 15, Fr("-3.5")],
                       "Multiply first: 1.5 × 6 = 9. Then 4 − 9 = −5. ((4 − 1.5) × 6 = 15 subtracts first.)",
                       rnd, n, neg=True)))
    # two variables
    assert ev("2.4a + 1.6b", a=5, b=Fr("2.5")) == 16
    its.append((3, mcq("Evaluate %s when %s = 5 and %s = 2.5." % (X("2.4a + 1.6b"), X("a"), X("b")), 16,
                       [14, Fr("11.5"), 12],
                       "2.4 × 5 = 12 and 1.6 × 2.5 = 4. Then 12 + 4 = 16. (14 swaps the values of " + X("a") + " and " +
                       X("b") + ". 12 forgets the second term.)", rnd, n)))
    assert ev("3x - y", x=Fr("2.5"), y=Fr("1.8")) == Fr("5.7")
    its.append((3, mcq("Evaluate %s when %s = 2.5 and %s = 1.8." % (X("3x - y"), X("x"), X("y")), Fr("5.7"),
                       [Fr("9.3"), Fr("2.1"), Fr("3.7")],
                       "3 × 2.5 = 7.5. Then 7.5 − 1.8 = 5.7. (9.3 adds 1.8. 3 × (2.5 − 1.8) = 2.1 subtracts first.)",
                       rnd, n)))
    # tables and which expression
    for a, b, last in [(3, "1.5", "4.5"), ("2.5", 4, "3.2")]:
        a, b, last = Fr(a), Fr(b), Fr(last)
        s_ = lin(a, b, "n")
        nums = [1, 2, 3]
        vals = [ev(s_, n=x) for x in nums]
        ans = ev(s_, n=last)
        q = (fig(table_svg((SX("n"), SX(s_)), [n(x) for x in nums] + [n(last)], [n(x) for x in vals] + ["?"],
                           "table of values for an expression")) +
             "The table shows values of %s. What is the missing value?" % X(s_))
        e = "Replace %s with %s: %s × %s + %s = %s + %s = %s." % (
            X("n"), n(last), n(a), n(last), n(b), n(a * last), n(b), n(ans))
        wp = Fr(int(last))
        cands = [vals[-1] + a, a * last, a * wp + (last - wp) + b, a + last + b]
        its.append((4, mcq(q, ans, cands, e, rnd, n)))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate expressions with decimal numbers", "items": [i for _, i in its]}


# ============================================================ set 5: write expressions and word problems
def set_words(rnd):
    its = []
    rows = [
        ("5 more than a number %s" % X("n"), "n + 5", ["5n", "n - 5", "5 - n"],
         "“More than” means add: " + X("n") + " + 5. (5" + X("n") + " means 5 times " + X("n") + ".)"),
        ("8 less than a number %s" % X("n"), "n - 8", ["8 - n", "8n", "n + 8"],
         "“8 less than " + X("n") + "” starts with " + X("n") + " and takes away 8: " + X("n") + " − 8. "
         "The order is the opposite of the words, so 8 − " + X("n") + " is wrong."),
        ("the product of 6 and a number %s" % X("k"), "6k", ["6 + k", "k - 6", "k ÷ 6"],
         "“Product” means multiply: 6 × " + X("k") + " = 6" + X("k") + "."),
        ("a number %s divided by 4" % X("m"), "m ÷ 4", ["4 ÷ m", "4m", "m - 4"],
         "Start with " + X("m") + " and divide by 4: " + X("m") + " ÷ 4. (4 ÷ " + X("m") + " divides the other way round.)"),
        ("3 more than twice a number %s" % X("x"), "2x + 3", ["3x + 2", "2(x + 3)", "5x"],
         "“Twice a number” is 2" + X("x") + ", and “3 more” adds 3: 2" + X("x") + " + 3. (2(" + X("x") + " + 3) adds before doubling.)"),
        ("7 less than 4 times a number %s" % X("y"), "4y - 7", ["7 - 4y", "4(y - 7)", "7y - 4"],
         "“4 times a number” is 4" + X("y") + ". “7 less than” it takes 7 away: 4" + X("y") + " − 7."),
        ("half of a number %s, plus 10" % X("n"), "n ÷ 2 + 10", ["2n + 10", "(n + 10) ÷ 2", "2 ÷ n + 10"],
         "Half of " + X("n") + " is " + X("n") + " ÷ 2. Then add 10: " + X("n") + " ÷ 2 + 10. (2" + X("n") + " is double, not half.)"),
        ("the sum of a number %s and 9, multiplied by 3" % X("t"), "3(t + 9)", ["3t + 9", "9t + 3", "3 + t + 9"],
         "Find the sum first, so it goes in brackets: (" + X("t") + " + 9). Then multiply by 3: 3(" + X("t") + " + 9). "
         "(3" + X("t") + " + 9 multiplies only the " + X("t") + ".)"),
    ]
    for words, good, bad, e in rows:
        its.append((0, emcq("Which expression means “%s”?" % words, good, bad, e, rnd)))
    rows = [
        ("Owen buys %s tickets to a hockey game at $24 each. There is one $6 service fee for the whole order. "
         "Which expression gives the total cost in dollars?" % X("t"), "24t + 6", ["30t", "6t + 24", "24(t + 6)"],
         "Each ticket costs $24, so " + X("t") + " tickets cost 24" + X("t") + ". The fee is added once: 24" + X("t") +
         " + 6. (30" + X("t") + " would charge the fee on every ticket.)"),
        ("Amira has 45 stickers. She gives 3 stickers to each of %s friends. Which expression gives the number of stickers she has left?" % X("f"),
         "45 - 3f", ["3f - 45", "42f", "45 + 3f"],
         "She gives away 3 × " + X("f") + " = 3" + X("f") + " stickers. Take that from 45: 45 − 3" + X("f") + "."),
        ("A school bus holds 48 students. Which expression gives the number of students that %s buses can hold?" % X("b"),
         "48b", ["48 + b", "b ÷ 48", "48 - b"],
         "Each bus holds 48, so " + X("b") + " buses hold 48 × " + X("b") + " = 48" + X("b") + "."),
        ("The length of a rectangular poster is 4 cm more than its width, %s. Which expression gives the length in centimetres?" % X("w"),
         "w + 4", ["4w", "w - 4", "4 - w"],
         "“4 cm more than the width” means add 4 to " + X("w") + ": " + X("w") + " + 4. (4" + X("w") + " would be 4 times as long.)"),
        ("Priya is %s years old. Her brother is 3 years younger than she is. Which expression gives her brother’s age?" % X("p"),
         "p - 3", ["3 - p", "3p", "p + 3"],
         "Younger means fewer years: " + X("p") + " − 3. (3 − " + X("p") + " would be negative for any age over 3.)"),
    ]
    for q, good, bad, e in rows:
        its.append((1, emcq(q, good, bad, e, rnd)))
    # evaluate in context
    rows = [
        ("Skate rental at an outdoor rink costs $6 plus $4.50 for each hour, so the cost is 4.5" + X("h") +
         " + 6 dollars. How much does it cost to rent skates for 3 hours?", ("4.5h + 6", {"h": 3}),
         ["31.5", "13.5", "10.5"], money,
         "Multiply first: 4.5 × 3 = 13.5. Then 13.5 + 6 = 19.5, so $19.50. ((6 + 4.50) × 3 = $31.50 charges the $6 every hour.)"),
        ("Ski rental for a day trip costs 15" + X("h") + " + 20 dollars for " + X("h") + " hours. What is the cost for 4 hours?",
         ("15h + 20", {"h": 4}), ["140", "60", "39"], money,
         "15 × 4 = 60. Then 60 + 20 = 80, so $80.00. ((15 + 20) × 4 = $140.00 adds first. $60.00 forgets the $20.)"),
        ("A sugar bush sells maple syrup for $18.75 a litre plus $5 shipping for the whole order: 18.75" + X("n") +
         " + 5 dollars for " + X("n") + " litres. What is the total cost for 4 L?", ("18.75n + 5", {"n": 4}), ["95", "75", "27.75"], money,
         "18.75 × 4 = 75. Then 75 + 5 = 80, so $80.00. ((18.75 + 5) × 4 = $95.00 charges shipping on every litre.)"),
        ("On a trip to the United States, Liam sees temperatures in °F. The expression 1.8" + X("c") +
         " + 32 changes " + X("c") + " degrees Celsius to °F. What is 25" + NBSP + "°C in °F?", ("1.8c + 32", {"c": 25}),
         ["58.8", "45", "102.6"], lambda v: n(v) + NBSP + "°F",
         "1.8 × 25 = 45. Then 45 + 32 = 77, so 77" + NBSP + "°F. (1.8 + 25 + 32 = 58.8 adds instead of multiplying. 45 forgets the + 32.)"),
        ("A phone plan costs $35 a month plus $2.50 for each GB of extra data: 35 + 2.5" + X("g") +
         " dollars. What is the bill for a month with 6 GB of extra data?", ("35 + 2.5g", {"g": 6}),
         ["225", "15", "43.5"], money,
         "Multiply first: 2.5 × 6 = 15. Then 35 + 15 = 50, so $50.00. ((35 + 2.5) × 6 = $225.00 adds first.)"),
        ("A field trip to the science centre costs $350 for the bus plus $14 for each student: 14" + X("s") +
         " + 350 dollars. What is the cost for 27 students?", ("14s + 350", {"s": 27}),
         ["9828", "378", "391"], money,
         "14 × 27 = 378. Then 378 + 350 = 728, so $728.00. ($378.00 forgets the bus. (350 + 14) × 27 adds first. 350 + 14 + 27 = $391.00 does not multiply.)"),
        ("For the Terry Fox Run, Kai has already raised $85. His aunt gives $2.50 for every kilometre he runs: 85 + 2.5" +
         X("k") + " dollars. How much will he have raised if he runs 10 km?", ("85 + 2.5k", {"k": 10}),
         ["875", "25", "97.5"], money,
         "2.5 × 10 = 25. Then 85 + 25 = 110, so $110.00. ((85 + 2.5) × 10 = $875.00 adds first. $25.00 forgets the $85.)"),
    ]
    for q, (s_, env), wrong, disp, e in rows:
        ans = ev(s_, **env)
        its.append((2, mcq(q, ans, [Fr(w) for w in wrong], e, rnd, disp)))
    its.sort(key=lambda t: t[0])
    return {"title": "Write expressions and solve word problems", "items": [i for _, i in its]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    t1 = tiles_svg([(3, 2, 0)], label="algebra tiles: 3 x-tiles and 2 one-tiles")
    t2 = tiles_svg([(3, 0, 0), (5, 0, 0)], "+", "algebra tiles: 3 x-tiles plus 5 x-tiles")
    t3 = tiles_svg([(7, 0, 2)], label="algebra tiles: 7 x-tiles with 2 crossed out")
    return (
        "<h2>Parts of an expression</h2>"
        "<p>An <b>algebraic expression</b> uses numbers, letters and operations, like 3" + X("x") + " + 2. "
        "The letter is a <b>variable</b>: it stands for a number. The parts joined by + or − are <b>terms</b>.</p>" +
        table(["Word", "Meaning", "In 3" + X("x") + " + 2"], [
            ["Coefficient", "the number multiplied by the variable", "3"],
            ["Constant term", "a number with no variable", "2"],
            ["Like terms", "terms with the same variable part", "3" + X("x") + " and 5" + X("x") + " are like terms"],
        ]) +
        "<p>3" + X("x") + " means 3 × " + X("x") + ", and " + X("x") + " on its own means 1" + X("x") + ".</p>"
        "<figure class='sn-fig'>" + t1 +
        "<figcaption>With algebra tiles, each green tile is " + X("x") + " and each yellow tile is 1. "
        "These tiles show 3" + X("x") + " + 2.</figcaption></figure>"
        "<h2>Add and subtract like terms</h2>"
        "<p>Only like terms can be combined. Add or subtract the coefficients and keep the variable.</p>"
        "<figure class='sn-fig'>" + t2 +
        "<figcaption>3" + X("x") + " + 5" + X("x") + ": 3 x-tiles and 5 x-tiles make 8 x-tiles, so the sum is 8" +
        X("x") + ".</figcaption></figure>"
        "<figure class='sn-fig'>" + t3 +
        "<figcaption>7" + X("x") + " − 2" + X("x") + ": take 2 x-tiles away from 7, and 5 are left. The answer is 5" +
        X("x") + ", not 5.</figcaption></figure>" +
        ex("Example 1", "Simplify 6" + X("x") + " + 4 + " + X("x") + " + 2.",
           X("x") + "-terms: 6" + X("x") + " + 1" + X("x") + " = 7" + X("x") + ". Constants: 4 + 2 = 6.",
           "7" + X("x") + " + 6") +
        "<h2>Evaluate an expression</h2>"
        "<p>To <b>evaluate</b>, replace each variable with its value. Then follow the order of operations: brackets, "
        "exponents, multiply and divide, then add and subtract.</p>" +
        ex("Example 2", "Evaluate 2.5" + X("n") + " + 4 when " + X("n") + " = 3.",
           "2.5 × 3 = 7.5. Then 7.5 + 4 = 11.5.", "11.5") +
        ex("Example 3", "Evaluate 3" + X("a") + " + 2" + X("b") + " when " + X("a") + " = 5 and " + X("b") + " = 4.",
           "3 × 5 + 2 × 4 = 15 + 8 = 23.", "23") +
        "<h2>Write an expression from words</h2>"
        "<p>“More than” and “sum” mean add. “Less than” and “difference” mean subtract. “Times”, “product” and “twice” "
        "mean multiply. Watch the order: “8 less than " + X("n") + "” is " + X("n") + " − 8.</p>" +
        ex("Example 4", "Ski rental costs $20 plus $15 for each hour. Write an expression for " + X("h") +
           " hours, then find the cost for 4 hours.",
           "15" + X("h") + " + 20. When " + X("h") + " = 4: 15 × 4 + 20 = 60 + 20 = 80.", "$80.00") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3" + X("x") + " + 2 = 5" + X("x"), "3" + X("x") + " and 2 are not like terms. 3" + X("x") + " + 2 is already simplified"],
            ["Reading 3" + X("x") + " as 3 + " + X("x"), "3" + X("x") + " means 3 × " + X("x") + ". When " + X("x") + " = 4, 3" + X("x") + " = 12"],
            ["3" + X("x") + " + 5" + X("x") + " = 15" + X("x") + " or 8" + X("x^2"), "Add the coefficients and keep the variable: 8" + X("x")],
            ["7" + X("x") + " − 2" + X("x") + " = 5", "The variable stays: 5" + X("x")],
            ["Adding before multiplying: 2.5" + X("n") + " + 4 = 6.5 × 3", "Multiply first: 2.5 × 3 + 4 = 11.5"],
            ["Writing “8 less than " + X("n") + "” as 8 − " + X("n"), "Start with " + X("n") + ": " + X("n") + " − 8"],
        ])
    )


FAQ = [
    {"q": "What do Grade 7 students learn about algebraic expressions in the Ontario math curriculum?",
     "a": "In Grade 7 (Algebra, C2), students add and subtract monomials with degree 1, such as 3x + 5x = 8x, often with algebra tiles. They also evaluate expressions that involve whole numbers and decimal numbers, such as 2.5n + 4 when n = 3."},
    {"q": "What are like terms?",
     "a": "Like terms have exactly the same variable part, such as 4x and 9x, or two constants like 3 and 7. Only like terms can be added or subtracted: 4x + 9x = 13x, but 4x + 9 stays as it is."},
    {"q": "Is 3x + 2 the same as 5x?",
     "a": "No. 3x and 2 are not like terms, so they cannot be added. When x = 4, 3x + 2 = 14 but 5x = 20."},
    {"q": "How do algebra tiles help with simplifying expressions?",
     "a": "Each long tile stands for x and each small square stands for 1. Students group tiles of the same kind, so 3x + 5x becomes 8 x-tiles, and they can see why x-tiles and 1-tiles cannot be joined."},
]


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(47813)
    sets = [set_terms(rnd), set_combine(rnd), set_whole(rnd), set_decimals(rnd), set_words(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"]
            assert it["q"].count("<svg") <= 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "algebraic-expressions", "sort": 13,
        "updated": UPDATED, "pdf_url": "",
        "title": "Algebraic Expressions: Like Terms, Algebra Tiles and Evaluating Expressions",
        "seo_title": "Grade 7 Algebraic Expressions Worksheets: Like Terms and Evaluating (Free, Answer Key)",
        "short_title": "Algebraic Expressions",
        "domain": "Algebra",
        "standard_code": "Grade 7: C2.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Evaluate algebraic expressions that involve whole numbers and decimal numbers",
        "meta_desc": "Free Grade 7 math worksheets on algebraic expressions for the Ontario curriculum: terms, coefficients and like terms, adding and subtracting like terms with algebra tiles, evaluating expressions with whole numbers and decimals, and writing expressions from words. 100 questions with an answer key.",
        "key_big": "Only like terms can be combined: 3x + 5x = 8x, but 3x + 2 stays 3x + 2.",
        "key_sub": "3x means 3 × x. To evaluate, replace the variable and multiply before you add: 2.5n + 4 = 11.5 when n = 3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(algebra tiles|table)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
