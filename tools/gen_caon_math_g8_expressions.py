# -*- coding: utf-8 -*-
"""
CA-ON Grade 8 Math: Expressions and Binomials (Ontario Mathematics Curriculum 2020, Grade 8: Algebra, C2.1 and C2.2)
  python3 tools/gen_caon_math_g8_expressions.py
Combining like terms with integer coefficients (−3x + 5x) using algebra tiles and zero pairs, adding binomials of
degree 1 ((2x + 3) + (x − 5)), subtracting monomials (6x − (−4x)), evaluating expressions with integers, fractions and
decimals, and writing and simplifying expressions from contexts (perimeter, temperature, money).
Wrong answers come from real student mistakes: 3x + 2 = 5x (joining unlike terms), −3x + 5x = −8x or 8x (sign
errors), −x read as 0x, ignoring a minus sign inside a binomial, 6x − (−4x) = 2x, subtracting from both terms of a
binomial, (−3)(−2) = −6, (−3)^2 = −9, adding numerators and denominators, adding only two sides for a perimeter.
Every answer is checked in code with fractions.Fraction (expressions are compared at several values).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
XT = "#7fc495"      # x-tile
NXT = "#f2b5ad"     # negative x-tile
ONE = "#f4d35e"     # 1-tile
NONE = "#f7cfc9"    # negative 1-tile
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


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def rat(v):
    """Fraction in simplest form as HTML: 5/6, −2 1/2, 9."""
    v = Fr(v)
    if v.denominator == 1:
        return n(v)
    sg = M if v < 0 else ""
    w, r = divmod(abs(v.numerator), v.denominator)
    return sg + ("%d " % w if w else "") + fr(r, v.denominator)


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1, v
    w, r = divmod(abs(c.numerator), 100)
    return (M if v < 0 else "") + "$%s.%02d" % (n(w), r)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s).replace(NBSP, " ").strip()


# ------------------------------------------------------------ expressions
def X(s):
    """Plain expression '-3x + 5x' -> HTML: letters in italics, ^2 as a superscript, real minus sign."""
    s = s.replace("-", M).replace("*", "×")
    s = re.sub(r"[a-z]", lambda m: "<i>%s</i>" % m.group(), s)
    return re.sub(r"\^(\d)", r"<sup>\1</sup>", s)


def E(s):
    """Text with expressions in braces: 'Add {-3x} and {5x}' -> the braces become X(...)."""
    return re.sub(r"\{([^{}]*)\}", lambda m: X(m.group(1)), s.replace(" - ", " " + M + " "))


def ev(expr_, **env):
    """Exact value of a plain expression with the letters given in env."""
    t = expr_.replace(M, "-").replace("×", "*").replace("^", "**").replace(" ", "")
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Q('%s')" % m.group(), t)
    t = re.sub(r"(\)|[a-z])(?=[a-zQ(])", r"\1*", t)
    e = {"Q": Fr}
    for k, v in env.items():
        e[k] = Fr(v)
    return eval(t, {"__builtins__": {}}, e)


def same(a, b):
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2), -5):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None):
    """correct and cands are numbers shown with disp, or HTML strings. Equal values are rejected."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pick = {plain(cs)}, {cv}, []
    for c in cands:
        if disp is not None:
            c = Fr(c)
            assert c not in vals, (q, c)
            vals.add(c)
            c = disp(c)
        assert plain(c) not in seen, (q, c)
        seen.add(plain(c))
        pick.append(c)
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def emcq(q, good, bad, e, rnd, src=None):
    """Expression choices (plain text). good must equal src (when given); wrong ones must not be equivalent."""
    if src is not None:
        assert same(good, src), (src, good)
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


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def SX(s):
    """Expression inside an SVG text: letters in italics with a tspan, real minus sign."""
    return re.sub(r"[a-z]", lambda m: "<tspan font-style='italic'>%s</tspan>" % m.group(), s.replace("-", M))


TW, TH, T1, TP, PAD = 26, 60, 26, 31, 6


def cross(x, y, w, h):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
            % (x - 2, y + 2, x + w + 2, y + h - 2, INK, x + w + 2, y + 2, x - 2, y + h - 2, INK))


def tile(kind, x, y):
    k = kind.rstrip("*")
    neg = k.startswith("-")
    if k.endswith("x"):
        s = ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
             % (x, y, TW, TH, NXT if neg else XT, RED if neg else GREEN))
        s += text(x + TW / 2, y + TH / 2 + 6, (M if neg else "") + "<tspan font-style='italic'>x</tspan>", 16)
        w, h = TW, TH
    else:
        s = ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
             % (x, y, T1, T1, NONE if neg else ONE, RED if neg else "#8a6d00"))
        s += text(x + T1 / 2, y + T1 / 2 + 5, (M if neg else "") + "1", 14)
        w, h = T1, T1
    if kind.endswith("*"):
        s += cross(x, y, w, h)
    return s


def tiles_svg(groups, ops=(), label="algebra tiles"):
    """groups: list of strings of tiles, e.g. 'x x -x 1 -1 -1'; a * after a tile crosses it out.
    x-tiles stand in a row; 1-tiles stand in columns of 2 at the bottom. ops ('+' or '−') go between groups."""
    x = PAD
    s = []
    for gi, g in enumerate(groups):
        if gi:
            s.append(text(x + 12, PAD + TH / 2 + 9, ops[gi - 1], 26))
            x += 30
        ts = g.split()
        xs = [t for t in ts if t.rstrip("*").endswith("x")]
        os_ = [t for t in ts if not t.rstrip("*").endswith("x")]
        for t in xs:
            s.append(tile(t, x, PAD))
            x += TP
        drawn = bool(xs)
        for part in ([t for t in os_ if not t.startswith("-")], [t for t in os_ if t.startswith("-")]):
            if not part:
                continue
            x += 4 if drawn else 0
            drawn = True
            for i, t in enumerate(part):
                c, r = divmod(i, 2)
                s.append(tile(t, x + c * TP, PAD + TH - T1 - r * (T1 + 8)))
            x += ((len(part) + 1) // 2) * TP
    W = x - (TP - TW) + PAD
    return svg_wrap(W, TH + 2 * PAD, "".join(s), label)


def tlabel(g):
    ts = [t.rstrip("*") for t in g.split()]
    parts = []
    for k, name in [("x", "x-tiles"), ("-x", "negative x-tiles"), ("1", "1-tiles"), ("-1", "negative 1-tiles")]:
        c = ts.count(k)
        if c:
            parts.append("%d %s" % (c, name))
    return ", ".join(parts)


def rect_svg(top, side, label, w=190, h=84):
    L, T = 74, 30
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, SX(top), 17))
    s.append(text(L - 8, T + h / 2 + 6, SX(side), 17, "end"))
    return svg_wrap(L + w + 8, T + h + 8, "".join(s), label)


def tri_svg(a, b, c, label):
    """Triangle with sides labelled a (left), b (right), c (bottom)."""
    P = [(60, 120), (260, 120), (160, 20)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%d,%d" % p for p in P), FILL, GREEN)]
    s.append(text(102, 66, SX(a), 17, "end"))
    s.append(text(218, 66, SX(b), 17, "start"))
    s.append(text(160, 143, SX(c), 17))
    return svg_wrap(312, 152, "".join(s), label)


def hex_svg(side, label):
    cx, cy, r = 80, 72, 54
    P = [(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i))) for i in range(6)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%.1f,%.1f" % p for p in P), FILL, GREEN)]
    # label on the right-hand upper side (between P[5] and P[0])
    mx, my = (P[5][0] + P[0][0]) / 2, (P[5][1] + P[0][1]) / 2
    s.append(text(mx + 10, my - 2, SX(side), 17, "start"))
    return svg_wrap(192, 2 * cy, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: like terms with integer coefficients
def set_like(rnd):
    its = []
    # A: coefficient of −x
    its.append((0, mcq(E("What is the coefficient of {x} in {7 - x}?"), M + "1", ["1", "0", "7"],
                       E("{-x} means {-1x}, so the coefficient is " + M + "1. The minus sign belongs to the term after it. "
                         "(It is not 0: {x} on its own is {1x}.)"), rnd)))
    # B: tiles with zero pairs
    rows = [
        ("x x x x -x -x", "2x", ["6x", "-2x", "2"],
         "Each {x}-tile and {-x}-tile make a zero pair. 4 green and 2 red tiles: 2 zero pairs, and 2 green tiles are left: {2x}. "
         "(6{x} counts the red tiles as positive.)"),
        ("x -x -x -x -x", "-3x", ["3x", "-5x", "-3"],
         "1 green tile and 1 red tile make a zero pair. 3 red tiles are left, so the tiles show {-3x}. "
         "(3{x} forgets that the leftover tiles are negative.)"),
        ("x x x -x -x -x 1 1", "2", ["6x + 2", "2x", "8x"],
         "3 green and 3 red {x}-tiles make 3 zero pairs, so no {x}-tiles are left. Only the two 1-tiles are left: 2. "
         "(2{x} joins the 2 to the {x}-tiles.)"),
        ("x x x x x -x -x 1 -1 -1 -1", "3x - 2", ["3x + 2", "x", "7x + 4"],
         "{x}-tiles: 5 green and 2 red leave {3x}. 1-tiles: 1 yellow and 3 red leave " + M + "2. The tiles show {3x - 2}. "
         "({x} joins 3{x} and " + M + "2, which are not like terms.)"),
        ("x x -x -x -x -x -x 1 1 1 1 -1", "-3x + 3", ["3x - 3", "-3x - 3", "7x + 5"],
         "{x}-tiles: 2 green and 5 red leave {-3x}. 1-tiles: 4 yellow and 1 red leave 3. The tiles show {-3x + 3}. "
         "(7{x} + 5 counts every tile as positive.)"),
    ]
    for g, good, bad, e in rows:
        q = (fig(tiles_svg([g], label="algebra tiles: " + tlabel(g))) +
             "Green tiles are positive and red tiles are negative. Remove the zero pairs. Which expression do the tiles show?")
        its.append((1, emcq(q, good, bad, E(e), rnd)))
    # C: integer coefficients
    rows = [
        ("-3x + 5x", "2x", ["-8x", "8x", "-2x"],
         "Add the coefficients: " + M + "3 + 5 = 2, so {-3x + 5x} = {2x}. (" + M + "8{x} and 8{x} add 3 and 5 and ignore the signs.)"),
        ("-4x - 6x", "-10x", ["2x", "-2x", "10x"],
         M + "4 " + M + " 6 = " + M + "10, so the answer is {-10x}. (" + M + "2{x} subtracts 4 from 6 instead.)"),
        ("7x - 9x", "-2x", ["2x", "-16x", "16x"],
         "7 " + M + " 9 = " + M + "2, so {7x - 9x} = {-2x}. The result is negative because 9 is greater than 7."),
        ("-x + 6x", "5x", ["6x", "7x", "-5x"],
         "{-x} means {-1x}: " + M + "1 + 6 = 5, so the answer is {5x}. (6{x} treats {-x} as 0. 7{x} drops the minus sign.)"),
        ("-8n + 3n", "-5n", ["5n", "-11n", "-5"],
         M + "8 + 3 = " + M + "5, so {-8n + 3n} = {-5n}. The variable stays. (" + M + "5 drops the {n}.)"),
        ("2y - 7y + 4y", "-y", ["y", "-9y", "13y"],
         "Left to right: 2 " + M + " 7 = " + M + "5, then " + M + "5 + 4 = " + M + "1. So the answer is {-1y} = {-y}. "
         "(" + M + "9{y} subtracts the 4{y} too.)"),
        ("-5k - k", "-6k", ["-5k", "-4k", "6k"],
         "{-k} means {-1k}: " + M + "5 " + M + " 1 = " + M + "6, so the answer is {-6k}. (" + M + "4{k} adds the 1 instead of subtracting it.)"),
        ("9m - 12m - m", "-4m", ["-2m", "4m", "-3m"],
         "9 " + M + " 12 = " + M + "3, then " + M + "3 " + M + " 1 = " + M + "4. So the answer is {-4m}. "
         "(" + M + "3{m} forgets the last {-m}.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((2, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    # D: with constants
    rows = [
        ("3x - 4 - 5x + 9", "-2x + 5", ["8x + 5", "-2x - 13", "2x + 5"],
         "{x}-terms: 3 " + M + " 5 = " + M + "2, so {-2x}. Constants: " + M + "4 + 9 = 5. The answer is {-2x + 5}. "
         "(8{x} + 5 ignores the minus sign in front of 5{x}.)"),
        ("-6a + 2 + 4a - 7", "-2a - 5", ["2a - 5", "-2a + 9", "-7a"],
         "{a}-terms: " + M + "6 + 4 = " + M + "2, so {-2a}. Constants: 2 " + M + " 7 = " + M + "5. The answer is {-2a - 5}. "
         "(" + M + "7{a} joins unlike terms.)"),
        ("5 - 2y + 8y - 11", "6y - 6", ["-10y - 6", "6y + 16", "0"],
         "{y}-terms: " + M + "2 + 8 = 6, so {6y}. Constants: 5 " + M + " 11 = " + M + "6. The answer is {6y - 6}. "
         "(0 joins {6y} and " + M + "6, which are not like terms.)"),
        ("x - 8 - 3x - 1", "-2x - 9", ["-2x - 7", "2x - 9", "-3x - 9"],
         "{x}-terms: 1 " + M + " 3 = " + M + "2, so {-2x}. Constants: " + M + "8 " + M + " 1 = " + M + "9. The answer is {-2x - 9}. "
         "(" + M + "3{x} " + M + " 9 forgets that {x} is {1x}.)"),
        ("-4 + 7m - 2 - 7m", "-6", ["14m - 6", "-2", "-6m"],
         "{7m - 7m} = {0m} = 0, so the {m}-terms cancel. Constants: " + M + "4 " + M + " 2 = " + M + "6. The answer is " + M + "6. "
         "(" + M + "6{m} keeps a variable that is no longer there.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((3, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    # E: test 3x + 2 = 5x style mistake
    assert ev("-3x + 2", x=4) == -10 and ev("-x", x=4) == -4
    its.append((4, mcq(E("Leah says {-3x + 2} = {-x}. Test it with {x} = 4. What are the values of {-3x + 2} and {-x}?"),
                       M + "10 and " + M + "4", [M + "10 and " + M + "10", M + "14 and " + M + "4", "14 and 4"],
                       E("{-3x + 2} = " + M + "3 × 4 + 2 = " + M + "12 + 2 = " + M + "10, but {-x} = " + M + "4. The values are "
                         "different, so Leah is wrong: {-3x} and 2 are not like terms."), rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Combine like terms with integers", "items": [i for _, i in its]}


# ============================================================ set 2: add binomials
def set_binomials(rnd):
    its = []
    rows = [
        ("x x 1 1 1", "x 1", "(2x + 3) + (x + 1)", "3x + 4", ["7x", "2x + 4", "4x + 3"],
         "{x}-tiles: 2 + 1 = 3, so {3x}. 1-tiles: 3 + 1 = 4. The sum is {3x + 4}. ({2x} + 4 forgets the single {x}-tile.)"),
        ("x x 1 1 1", "x -1 -1 -1 -1 -1", "(2x + 3) + (x - 5)", "3x - 2", ["3x + 8", "3x + 2", "x"],
         "{x}-tiles: 2 + 1 = 3, so {3x}. 1-tiles: 3 yellow and 5 red make 3 zero pairs, and 2 red are left: " + M + "2. "
         "The sum is {3x - 2}. (3{x} + 8 counts the red tiles as positive.)"),
        ("x x x -1 -1 -1 -1", "-x 1 1", "(3x - 4) + (-x + 2)", "2x - 2", ["4x - 2", "2x - 6", "2x + 2"],
         "{x}-tiles: 3 green and 1 red leave {2x}. 1-tiles: 4 red and 2 yellow leave " + M + "2. The sum is {2x - 2}. "
         "(4{x} " + M + " 2 counts the red {x}-tile as positive.)"),
        ("-x -x 1", "x x x x 1 1 1", "(-2x + 1) + (4x + 3)", "2x + 4", ["6x + 4", "6x", "-6x + 4"],
         "{x}-tiles: 2 red and 4 green leave {2x}. 1-tiles: 1 + 3 = 4. The sum is {2x + 4}. "
         "(6{x} + 4 counts the red {x}-tiles as positive. 6{x} joins unlike terms.)"),
    ]
    for g1, g2, src, good, bad, e in rows:
        q = (fig(tiles_svg([g1, g2], "+", "algebra tiles: %s, plus %s" % (tlabel(g1), tlabel(g2)))) +
             E("The algebra tiles show {%s}. Green tiles are positive and red tiles are negative. What is the sum?" % src))
        its.append((0, emcq(q, good, bad, E(e), rnd, src)))
    rows = [
        ("(4x + 7) + (2x - 3)", "6x + 4", ["6x + 10", "10x", "6x - 4"],
         "{x}-terms: {4x + 2x} = {6x}. Constants: 7 " + M + " 3 = 4. The sum is {6x + 4}. (6{x} + 10 ignores the minus sign in {2x - 3}.)"),
        ("(5n - 2) + (3n - 6)", "8n - 8", ["8n - 4", "8n + 8", "2n - 8"],
         "{n}-terms: {5n + 3n} = {8n}. Constants: " + M + "2 + (" + M + "6) = " + M + "8. The sum is {8n - 8}. "
         "(8{n} " + M + " 4 subtracts 2 from 6 instead of adding two negatives.)"),
        ("(-3y + 8) + (5y - 1)", "2y + 7", ["8y + 7", "-2y + 7", "2y + 9"],
         "{y}-terms: " + M + "3 + 5 = 2, so {2y}. Constants: 8 " + M + " 1 = 7. The sum is {2y + 7}. "
         "(8{y} + 7 drops the minus sign of {-3y}.)"),
        ("(x - 9) + (x + 4)", "2x - 5", ["x^2 - 5", "2x - 13", "2x + 5"],
         "{x + x} = {2x}, not {x^2}. Constants: " + M + "9 + 4 = " + M + "5. The sum is {2x - 5}."),
        ("(-6k - 2) + (k + 5)", "-5k + 3", ["-7k + 3", "-6k + 3", "-5k - 7"],
         "{k}-terms: " + M + "6 + 1 = " + M + "5, so {-5k}. Constants: " + M + "2 + 5 = 3. The sum is {-5k + 3}. "
         "(" + M + "6{k} + 3 forgets that {k} is {1k}.)"),
        ("(7a + 4) + (-7a + 6)", "10", ["14a + 10", "10a", "a + 10"],
         "{a}-terms: 7 + (" + M + "7) = 0, so they cancel. Constants: 4 + 6 = 10. The sum is 10. "
         "(10{a} keeps a variable that has cancelled.)"),
        ("(2m - 5) + (-8m - 3)", "-6m - 8", ["10m - 8", "-6m - 2", "6m + 8"],
         "{m}-terms: 2 + (" + M + "8) = " + M + "6, so {-6m}. Constants: " + M + "5 + (" + M + "3) = " + M + "8. The sum is {-6m - 8}. "
         "(10{m} " + M + " 8 drops the minus sign of {-8m}.)"),
        ("(-4t + 9) + (-2t - 9)", "-6t", ["-6t - 18", "-2t", "6t"],
         "{t}-terms: " + M + "4 + (" + M + "2) = " + M + "6, so {-6t}. Constants: 9 + (" + M + "9) = 0. The sum is {-6t}."),
    ]
    for s_, good, bad, e in rows:
        its.append((1, emcq(E("Add: {%s}" % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("(3x + 2) + (x - 4) + (2x + 5)", "6x + 3", ["5x + 3", "6x + 11", "9x"],
         "{x}-terms: 3 + 1 + 2 = 6, so {6x}. Constants: 2 " + M + " 4 + 5 = 3. The sum is {6x + 3}. "
         "(5{x} + 3 forgets that {x} is {1x}.)"),
        ("(-2x + 6) + (5 - 3x)", "-5x + 11", ["x + 11", "-5x - 11", "6x"],
         "Match like terms even when the order is different. {x}-terms: " + M + "2 + (" + M + "3) = " + M + "5. "
         "Constants: 6 + 5 = 11. The sum is {-5x + 11}."),
        ("(6 + 4y) + (2y - 10)", "6y - 4", ["6y + 16", "2y", "6y + 4"],
         "{y}-terms: {4y + 2y} = {6y}. Constants: 6 " + M + " 10 = " + M + "4. The sum is {6y - 4}. (2{y} joins unlike terms.)"),
        ("(-x - 1) + (-x - 1)", "-2x - 2", ["0", "2x + 2", "-x - 2"],
         "{x}-terms: " + M + "1 + (" + M + "1) = " + M + "2. Constants: " + M + "1 + (" + M + "1) = " + M + "2. "
         "The sum is {-2x - 2}. (0 treats two equal terms as a zero pair, but a zero pair needs opposite terms.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((2, emcq(E("Add: {%s}" % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("2x + 3", "5x - 1", "3x - 4", ["3x + 2", "7x + 2", "3x + 4"],
         "{x}-terms: 2 + ? = 5, so {3x}. Constants: 3 + ? = " + M + "1, so " + M + "4. Check: {(2x + 3) + (3x - 4)} = {5x - 1}. "
         "(7{x} + 2 adds instead.)"),
        ("-4x + 6", "x + 2", "5x - 4", ["-3x + 8", "3x - 4", "5x + 4"],
         "{x}-terms: " + M + "4 + ? = 1, so {5x}. Constants: 6 + ? = 2, so " + M + "4. Check: {(-4x + 6) + (5x - 4)} = {x + 2}."),
        ("x - 7", "4x + 1", "3x + 8", ["3x - 6", "5x - 6", "3x - 8"],
         "{x}-terms: 1 + ? = 4, so {3x}. Constants: " + M + "7 + ? = 1, so 8. Check: {(x - 7) + (3x + 8)} = {4x + 1}. "
         "(3{x} " + M + " 6 adds " + M + "7 and 1.)"),
    ]
    for a, total, good, bad, e in rows:
        assert same("(%s) + (%s)" % (a, good), total)
        its.append((3, emcq(E("Which binomial must be added to {%s} to get {%s}?" % (a, total)), good, bad, E(e), rnd)))
    assert same("(5x - 3) + (-2x + 4)", "3x + 1") and same("5x + 2x - 3 + 4", "7x + 1")
    its.append((3, mcq(E("Noah added {(5x - 3) + (-2x + 4)} and got {7x + 1}. What mistake did he make?"),
                       "He ignored the minus sign of " + X("-2x") + ".",
                       ["He added the constants wrongly.", "He combined unlike terms.", "He made no mistake."],
                       E("{5x + (-2x)} = {3x}, not {7x}. The constants are right: " + M + "3 + 4 = 1. The correct sum is {3x + 1}."),
                       rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Add binomials", "items": [i for _, i in its]}


# ============================================================ set 3: subtract monomials
def set_subtract(rnd):
    its = []
    rows = [
        ("8x - 3x", "5x", ["11x", "5", "-5x"], "8 " + M + " 3 = 5, so {8x - 3x} = {5x}. The variable stays."),
        ("3x - 8x", "-5x", ["5x", "-11x", "11x"],
         "3 " + M + " 8 = " + M + "5, so {3x - 8x} = {-5x}. (5{x} subtracts the wrong way round.)"),
        ("-2x - 5x", "-7x", ["3x", "-3x", "7x"],
         M + "2 " + M + " 5 = " + M + "7, so the answer is {-7x}. Going down from " + M + "2 by 5 gives " + M + "7. (" + M + "3{x} subtracts 2 from 5.)"),
        ("x - 4x", "-3x", ["-4x", "3x", "5x"],
         "{x} means {1x}: 1 " + M + " 4 = " + M + "3, so the answer is {-3x}. (" + M + "4{x} treats {x} as 0.)"),
        ("-6y - y", "-7y", ["-6y", "-5y", "7y"],
         "{y} means {1y}: " + M + "6 " + M + " 1 = " + M + "7, so the answer is {-7y}. (" + M + "5{y} adds the 1.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((0, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    # tiles: subtract negatives
    g = "x x x x x -x* -x* -x*"
    q = (fig(tiles_svg([g], label="algebra tiles: 2 x-tiles and 3 zero pairs, with 3 negative x-tiles crossed out")) +
         E("To find {2x - (-3x)}, start with 2 green tiles. There are no red tiles to take away, so add 3 zero pairs, "
           "then take away 3 red tiles. What is left?"))
    its.append((1, emcq(q, "5x", ["-x", "x", "-5x"],
                        E("After the 3 red tiles are taken away, 2 + 3 = 5 green tiles are left: {2x - (-3x)} = {5x}. "
                          "Subtracting a negative is the same as adding its opposite: {2x + 3x}. ({-x} works out 2 " + M + " 3.)"),
                        rnd, "2x - (-3x)")))
    g = "-x -x -x -x* "
    q = (fig(tiles_svg([g.strip()], label="algebra tiles: 4 negative x-tiles, 1 crossed out")) +
         E("The tiles show {-4x - (-x)}: start with 4 red tiles and take away 1 red tile. What is left?"))
    its.append((1, emcq(q, "-3x", ["-5x", "3x", "5x"],
                        E("4 red tiles take away 1 red tile leaves 3 red tiles: {-4x - (-x)} = {-3x}. "
                          "(" + M + "5{x} takes away a green tile instead of a red one.)"), rnd, "-4x - (-x)")))
    rows = [
        ("6x - (-4x)", "10x", ["2x", "-10x", "-2x"],
         "Subtracting " + M + "4{x} is the same as adding 4{x}: {6x + 4x} = {10x}. (2{x} subtracts 4{x} instead.)"),
        ("-5x - (-2x)", "-3x", ["-7x", "3x", "7x"],
         "Add the opposite: {-5x + 2x} = {-3x}. (" + M + "7{x} subtracts 2{x} instead of adding it.)"),
        ("-3n - (-8n)", "5n", ["-11n", "-5n", "11n"],
         "Add the opposite: {-3n + 8n} = {5n}. (" + M + "11{n} subtracts 8{n} instead of adding it.)"),
        ("2a - (-a)", "3a", ["a", "2a", "-3a"],
         "Add the opposite: {2a + a} = {2a + 1a} = {3a}. ({a} subtracts instead. 2{a} treats {-a} as 0.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((1, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    assert ev("-9 - (-4)") == -5
    its.append((1, mcq(E("Simplify " + M + "9 " + M + " (" + M + "4)."), -5, [-13, 5, 13],
                       E("Constants are monomials too. Add the opposite: " + M + "9 + 4 = " + M + "5. "
                         "(" + M + "13 subtracts 4 instead of adding it.)"), rnd, n)))
    rows = [
        ("(5x + 4) - 2x", "3x + 4", ["3x + 2", "7x + 4", "7x"],
         "Only {5x} is a like term with {2x}: {5x - 2x} = {3x}. The 4 stays: {3x + 4}. (3{x} + 2 takes 2 from the constant as well.)"),
        ("(2x - 3) - 6x", "-4x - 3", ["4x - 3", "-4x + 3", "-7x"],
         "{2x - 6x} = {-4x}. The " + M + "3 stays: {-4x - 3}. (" + M + "7{x} joins unlike terms.)"),
        ("(-x + 7) - (-5x)", "4x + 7", ["-6x + 7", "6x + 7", "4x + 2"],
         "Add the opposite: {-x + 5x} = {4x}. The 7 stays: {4x + 7}. ({4x} + 2 takes 5 from the constant too.)"),
        ("4y - 9y - (-2y)", "-3y", ["-7y", "3y", "-11y"],
         "{4y - 9y} = {-5y}. Then {-5y - (-2y)} = {-5y + 2y} = {-3y}. (" + M + "7{y} subtracts 2{y} instead of adding it.)"),
        ("-3m - 2m - m", "-6m", ["-5m", "-4m", "6m"],
         M + "3 " + M + " 2 " + M + " 1 = " + M + "6, so the answer is {-6m}. (" + M + "5{m} treats {-m} as 0.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((2, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    its.append((3, emcq(E("Subtract {-6k} from {2k}."), "8k", ["-8k", "-4k", "4k"],
                        E("“Subtract " + M + "6{k} from 2{k}” means {2k - (-6k)} = {2k + 6k} = {8k}. "
                          "(" + M + "8{k} works out {-6k - 2k}, the wrong order.)"), rnd, "2k - (-6k)")))
    its.append((3, emcq(E("What is the difference when {3x} is subtracted from {-7x}?"), "-10x", ["-4x", "10x", "4x"],
                        E("Start with {-7x} and take away {3x}: {-7x - 3x} = {-10x}. (" + M + "4{x} adds 3{x} instead.)"),
                        rnd, "-7x - 3x")))
    its.append((3, emcq(E("What must be subtracted from {2x} to get {-5x}?"), "7x", ["-7x", "3x", "-3x"],
                        E("{2x} − ? = {-5x}. Check {7x}: {2x - 7x} = {-5x}. ({-7x} gives {2x + 7x} = {9x}.)"), rnd)))
    assert same("2x - 7x", "-5x")
    its.sort(key=lambda t: t[0])
    return {"title": "Subtract monomials", "items": [i for _, i in its]}


# ============================================================ set 4: evaluate with integers and fractions
def set_evaluate(rnd):
    its = []
    rows = [
        ("-3x + 4", {"x": -2}, [-2, -1, -10],
         "{-3} × (" + M + "2) = 6, because a negative times a negative is positive. Then 6 + 4 = 10. "
         "(" + M + "2 comes from " + M + "3 × (" + M + "2) = " + M + "6, a sign error. " + M + "1 adds " + M + "3 + (" + M + "2) + 4.)"),
        ("5x - 7", {"x": -3}, [8, -8, 22],
         "5 × (" + M + "3) = " + M + "15. Then " + M + "15 " + M + " 7 = " + M + "22. (" + M + "8 adds the 7 instead of subtracting it. 8 uses +15.)"),
        ("-2n - 9", {"n": -6}, [-21, 21, -3],
         M + "2 × (" + M + "6) = 12. Then 12 " + M + " 9 = 3. (" + M + "21 comes from the sign error " + M + "2 × (" + M + "6) = " + M + "12.)"),
        ("x^2 + 4", {"x": -3}, [-5, -2, 1],
         "(" + M + "3)<sup>2</sup> = (" + M + "3) × (" + M + "3) = 9. Then 9 + 4 = 13. "
         "(" + M + "5 uses " + M + "9 for the square. " + M + "2 reads {x^2} as {2x}.)"),
        ("2x^2 - 5", {"x": -2}, [11, -13, -9],
         "Square first: (" + M + "2)<sup>2</sup> = 4. Then 2 × 4 = 8, and 8 " + M + " 5 = 3. "
         "(11 squares 2 × (" + M + "2). " + M + "13 uses " + M + "4 for the square. " + M + "9 forgets to square.)"),
        ("4 - x", {"x": -6}, [-2, 2, -10],
         "4 " + M + " (" + M + "6) = 4 + 6 = 10. (" + M + "2 works out 4 " + M + " 6, losing the minus sign of " + M + "6.)"),
    ]
    for s_, env, wrong, e in rows:
        ans = ev(s_, **env)
        cond = " and ".join("{%s} = %s" % (k, n(v)) for k, v in env.items())
        its.append((0, mcq(E("Evaluate {%s} when %s." % (s_, cond)), ans, wrong, E(e), rnd, n)))
    rows = [
        ("3a - 2b", {"a": -2, "b": -5}, [-16, -4, 16],
         "3 × (" + M + "2) = " + M + "6 and 2 × (" + M + "5) = " + M + "10. Then " + M + "6 " + M + " (" + M + "10) = " + M + "6 + 10 = 4. "
         "(" + M + "16 subtracts 10 instead of " + M + "10.)"),
        ("-a + 4b", {"a": 7, "b": -2}, [-1, 1, 15],
         "{-a} = " + M + "7 and 4 × (" + M + "2) = " + M + "8. Then " + M + "7 + (" + M + "8) = " + M + "15. "
         "(" + M + "1 uses 7 for {-a}. 1 uses +8 for 4 × (" + M + "2).)"),
        ("xy - 6", {"x": -4, "y": 3}, [6, -7, 18],
         "{xy} = " + M + "4 × 3 = " + M + "12. Then " + M + "12 " + M + " 6 = " + M + "18. (6 uses +12. " + M + "7 adds the values instead of multiplying. 18 drops the minus sign.)"),
    ]
    for s_, env, wrong, e in rows:
        ans = ev(s_, **env)
        cond = " and ".join("{%s} = %s" % (k, n(v)) for k, v in env.items())
        its.append((1, mcq(E("Evaluate {%s} when %s." % (s_, cond)), ans, wrong, E(e), rnd, n)))
    # fractions
    ans = Fr(3, 4) * 12
    its.append((2, mcq(E("Evaluate " + fr(3, 4) + "{n} when {n} = 12."), ans, [16, 36, 4],
                       E(fr(3, 4) + " × 12: 12 ÷ 4 = 3, then 3 × 3 = 9. (16 divides by 3 and multiplies by 4. 36 forgets to divide by 4.)"),
                       rnd, rat)))
    ans = Fr(-15, 5) + 2
    its.append((2, mcq(E("Evaluate " + fr(X("n"), 5) + " + 2 when {n} = " + M + "15."), ans, [5, -3, -13],
                       E("Divide first: " + M + "15 ÷ 5 = " + M + "3. Then " + M + "3 + 2 = " + M + "1. "
                         "(5 makes the quotient positive. " + M + "3 forgets the + 2.)"), rnd, rat)))
    ans = Fr(1, 3) + Fr(1, 2)
    assert ans == Fr(5, 6)
    its.append((2, mcq(E("Evaluate {x} + " + fr(1, 2) + " when {x} = " + fr(1, 3) + "."), ans, [Fr(2, 5), Fr(1, 6), Fr(-1, 6)],
                       E("Use a common denominator: " + fr(2, 6) + " + " + fr(3, 6) + " = " + fr(5, 6) + ". "
                         "(" + fr(2, 5) + " adds the tops and the bottoms. " + fr(1, 6) + " multiplies.)"), rnd, rat)))
    ans = 2 * Fr(5, 8) - Fr(3, 4)
    assert ans == Fr(1, 2)
    its.append((2, mcq(E("Evaluate {2x} " + M + " " + fr(3, 4) + " when {x} = " + fr(5, 8) + "."), ans,
                       [Fr(-1, 8), Fr(7, 4), 2],
                       E("2 × " + fr(5, 8) + " = " + fr(10, 8) + ". Then " + fr(10, 8) + " " + M + " " + fr(6, 8) + " = " +
                         fr(4, 8) + " = " + fr(1, 2) + ". (" + M + fr(1, 8) + " doubles the bottom as well: " + fr(10, 16) +
                         ". 2 adds " + fr(3, 4) + " instead of subtracting.)"), rnd, rat)))
    ans = Fr(-2, 3) * -9
    assert ans == 6
    its.append((2, mcq(E("Evaluate " + M + fr(2, 3) + "{x} when {x} = " + M + "9."), ans, [-6, Fr(-27, 2), Fr(27, 2)],
                       E(M + fr(2, 3) + " × (" + M + "9): 9 ÷ 3 = 3, then 2 × 3 = 6. Negative × negative is positive, so the answer is 6. "
                         "(" + M + "13" + NBSP + fr(1, 2) + " multiplies by " + fr(3, 2) + " instead of " + fr(2, 3) + ".)"), rnd, rat)))
    ans = 4 * Fr(-3, 4) + Fr(1, 2)
    assert ans == Fr(-5, 2)
    its.append((2, mcq(E("Evaluate {4y} + " + fr(1, 2) + " when {y} = " + M + fr(3, 4) + "."), ans,
                       [Fr(7, 2), Fr(-7, 2), Fr(5, 16)],
                       E("4 × (" + M + fr(3, 4) + ") = " + M + "3. Then " + M + "3 + " + fr(1, 2) + " = " + M + "2" + NBSP + fr(1, 2) + ". "
                         "(" + M + "3" + NBSP + fr(1, 2) + " subtracts the " + fr(1, 2) + ". " + fr(5, 16) +
                         " multiplies only the bottom by 4.)"), rnd, rat)))
    # decimals
    rows = [
        ("-1.5x + 2", {"x": 4}, [8, -8, "4.5"],
         M + "1.5 × 4 = " + M + "6. Then " + M + "6 + 2 = " + M + "4. (8 drops the minus sign. 4.5 adds " + M + "1.5 + 4 + 2.)"),
        ("0.5x - 3", {"x": -8}, [1, -1, -11],
         "0.5 × (" + M + "8) = " + M + "4. Then " + M + "4 " + M + " 3 = " + M + "7. (1 uses +4. " + M + "11 forgets the 0.5.)"),
        ("2.5 - 3x", {"x": "1.5"}, ["-0.75", "7", "2"],
         "Multiply first: 3 × 1.5 = 4.5. Then 2.5 " + M + " 4.5 = " + M + "2. "
         "((2.5 " + M + " 3) × 1.5 = " + M + "0.75 subtracts first. 2 subtracts the wrong way round.)"),
    ]
    for s_, env, wrong, e in rows:
        env = {k: Fr(v) for k, v in env.items()}
        ans = ev(s_, **env)
        cond = " and ".join("{%s} = %s" % (k, n(v)) for k, v in env.items())
        its.append((3, mcq(E("Evaluate {%s} when %s." % (s_, cond)), ans, [Fr(w) for w in wrong], E(e), rnd, n)))
    # equivalence and which expression
    ans = ev("(2x + 3) + (x - 5)", x=-4)
    assert ans == -14 and ev("3x - 2", x=-4) == -14
    its.append((4, mcq(E("Evaluate {(2x + 3) + (x - 5)} when {x} = " + M + "4."), ans, [10, -4, -10],
                       E("Simplify first: {3x - 2}. Then 3 × (" + M + "4) " + M + " 2 = " + M + "12 " + M + " 2 = " + M + "14. "
                         "(" + M + "4 uses {3x + 8}, ignoring the minus sign of 5. " + M + "10 uses {3x + 2}. 10 uses +12.)"), rnd, n)))
    good, bad = "3x - 1", ["-3x - 1", "3x + 1", "2x - 5"]
    assert ev(good, x=-2) == -7 and all(ev(b, x=-2) != -7 for b in bad)
    its.append((4, emcq(E("Which expression has a value of " + M + "7 when {x} = " + M + "2?"), good, bad,
                        E("Check each one: " + "; ".join("{%s} = %s" % (b, n(ev(b, x=-2))) for b in [good] + bad) +
                          ". Only {3x - 1} gives " + M + "7."), rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate expressions with integers and fractions", "items": [i for _, i in its]}


# ============================================================ set 5: perimeter and word problems
def set_context(rnd):
    its = []
    # A: perimeter figures
    rows = [
        (rect_svg("2x + 3", "x - 1", "rectangle with length 2x + 3 and width x - 1"),
         "(2x + 3) + (x - 1) + (2x + 3) + (x - 1)", "6x + 4", ["3x + 2", "6x + 8", "10x"],
         "Add all four sides: {(2x + 3) + (x - 1) + (2x + 3) + (x - 1)}. {x}-terms: 2 + 1 + 2 + 1 = 6. "
         "Constants: 3 " + M + " 1 + 3 " + M + " 1 = 4. The perimeter is {6x + 4}. (3{x} + 2 adds only two sides.)"),
        (tri_svg("x + 4", "2x - 1", "3x + 2", "triangle with sides x + 4, 2x - 1 and 3x + 2"),
         "(x + 4) + (2x - 1) + (3x + 2)", "6x + 5", ["6x + 7", "11x", "5x + 5"],
         "{x}-terms: 1 + 2 + 3 = 6. Constants: 4 " + M + " 1 + 2 = 5. The perimeter is {6x + 5}. "
         "(6{x} + 7 ignores the minus sign of 1.)"),
        (rect_svg("3x - 2", "3x - 2", "square with sides 3x - 2", 100, 100),
         "4(3x - 2)", "12x - 8", ["12x - 2", "6x - 4", "4x"],
         "A square has 4 equal sides: {(3x - 2) + (3x - 2) + (3x - 2) + (3x - 2)} = {12x - 8}. "
         "(12{x} " + M + " 2 subtracts the 2 only once. 6{x} " + M + " 4 adds two sides.)"),
        (tri_svg("2x + 5", "2x + 5", "x - 3", "triangle with sides 2x + 5, 2x + 5 and x - 3"),
         "(2x + 5) + (2x + 5) + (x - 3)", "5x + 7", ["5x + 13", "3x + 2", "12x"],
         "{x}-terms: 2 + 2 + 1 = 5. Constants: 5 + 5 " + M + " 3 = 7. The perimeter is {5x + 7}. "
         "(5{x} + 13 ignores the minus sign of 3. 3{x} + 2 adds each different side only once.)"),
        (hex_svg("x + 2", "regular hexagon with sides x + 2"),
         "6(x + 2)", "6x + 12", ["6x + 2", "x + 12", "18x"],
         "A regular hexagon has 6 equal sides. Adding {x + 2} six times gives {6x} and 6 × 2 = 12: {6x + 12}. "
         "(6{x} + 2 adds the 2 only once.)"),
        (rect_svg("4x - 3", "2x + 1", "rectangle with length 4x - 3 and width 2x + 1"),
         "2(4x - 3) + 2(2x + 1)", "12x - 4", ["6x - 2", "12x + 8", "8x"],
         "{(4x - 3) + (2x + 1) + (4x - 3) + (2x + 1)}. {x}-terms: 4 + 2 + 4 + 2 = 12. "
         "Constants: " + M + "3 + 1 " + M + " 3 + 1 = " + M + "4. The perimeter is {12x - 4}. (12{x} + 8 treats " + M + "3 as +3.)"),
        (tri_svg("5x - 2", "3x - 4", "x + 9", "triangle with sides 5x - 2, 3x - 4 and x + 9"),
         "(5x - 2) + (3x - 4) + (x + 9)", "9x + 3", ["9x - 15", "9x - 3", "12x"],
         "{x}-terms: 5 + 3 + 1 = 9. Constants: " + M + "2 " + M + " 4 + 9 = 3. The perimeter is {9x + 3}. "
         "(9{x} " + M + " 15 subtracts the 9 as well.)"),
    ]
    for svg, src, good, bad, e in rows:
        word = "square" if "square" in svg else ("regular hexagon" if "hexagon" in svg else
                                                ("rectangle" if "rectangle" in svg else "triangle"))
        q = fig(svg) + "Which expression gives the perimeter of the %s?" % word
        its.append((0, emcq(q, good, bad, E(e), rnd, src)))
    assert ev("6x + 4", x=6) == 40
    its.append((0, mcq(E("A rectangle has length ({2x + 3}) cm and width ({x - 1}) cm. What is its perimeter when {x} = 6?"),
                       40, [20, 44, 75],
                       E("The perimeter is {6x + 4}. When {x} = 6: 6 × 6 + 4 = 40, so 40" + NBSP + "cm. "
                         "(20" + NBSP + "cm adds only two sides. 75 multiplies 15 × 5, which is the area.)"), rnd,
                       lambda v: n(v) + NBSP + "cm")))
    # B: words
    its.append((1, emcq(E("Mei is {x} years old. Ethan is 3 years older than Mei. Which expression gives the sum of their ages?"),
                        "2x + 3", ["x + 3", "5x", "2x - 3"],
                        E("Ethan is {x + 3}. The sum is {x + (x + 3)} = {2x + 3}. ({x} + 3 is only Ethan’s age.)"), rnd, "x + (x + 3)")))
    its.append((1, emcq(E("At 6:00 a.m. the temperature in Winnipeg is {t} °C. By noon it rises 9 °C. By midnight it falls 14 °C "
                          "from the noon temperature. Which expression gives the midnight temperature?"),
                        "t - 5", ["t + 23", "t + 5", "t - 23"],
                        E("{t + 9 - 14} = {t - 5}. A rise is +9 and a fall is " + M + "14, and 9 " + M + " 14 = " + M + "5. "
                          "({t} " + M + " 23 treats the rise as a fall.)"), rnd, "t + 9 - 14")))
    assert ev("t - 5", t=-12) == -17
    its.append((1, mcq(E("The midnight temperature is ({t - 5}) °C. What is it when the 6:00 a.m. temperature {t} is " + M + "12 °C?"),
                       -17, [-7, 11, 17],
                       E(M + "12 " + M + " 5 = " + M + "17, so " + M + "17" + NBSP + "°C. Going down 5 degrees from " + M + "12 gives a colder "
                         "temperature. (" + M + "7 goes up 5 degrees instead. 11 uses {t + 23}. 17 drops the minus sign.)"), rnd, lambda v: n(v) + NBSP + "°C")))
    assert ev("3m - 45", m=12) == -9
    its.append((1, mcq(E("The Grade 8 class sells mugs at a winter fair. They paid $45 for printing and earn $3 on each mug, so their profit is "
                         "{3m - 45} dollars for {m} mugs. What is the profit if they sell 12 mugs?"),
                       -9, [81, 9, -81],
                       E("3 × 12 = 36. Then 36 " + M + " 45 = " + M + "9. A profit of " + M + "$9.00 means they lost $9.00. "
                         "($81.00 adds the $45 instead of subtracting it.)"), rnd, money)))
    its.append((1, emcq(E("Liam has {4x + 6} hockey cards and Owen has {2x - 1} hockey cards. Which expression gives the number of cards they have altogether?"),
                        "6x + 5", ["6x + 7", "11x", "6x - 5"],
                        E("{(4x + 6) + (2x - 1)}: {x}-terms 4 + 2 = 6, constants 6 " + M + " 1 = 5. Altogether: {6x + 5}. "
                          "(11{x} joins unlike terms.)"), rnd, "(4x + 6) + (2x - 1)")))
    its.append((1, emcq(E("Kai paddles {x} km on Monday, ({x + 2}) km on Tuesday and ({2x - 3}) km on Wednesday on a canoe trip. "
                          "Which expression gives his total distance in kilometres?"),
                        "4x - 1", ["4x + 5", "3x - 1", "3x"],
                        E("{x + (x + 2) + (2x - 3)}: {x}-terms 1 + 1 + 2 = 4, constants 2 " + M + " 3 = " + M + "1. Total: {4x - 1}. "
                          "(3{x} " + M + " 1 forgets Monday’s {x}.)"), rnd, "x + (x + 2) + (2x - 3)")))
    assert ev("4x - 1", x=3) == 11
    its.append((1, mcq(E("Kai’s total distance is ({4x - 1}) km. How far does he paddle in all when {x} = 3?"), 11, [17, 8, 13],
                       E("4 × 3 " + M + " 1 = 12 " + M + " 1 = 11, so 11" + NBSP + "km. (17 uses {4x + 5}. 13 adds the 1.)"), rnd,
                       lambda v: n(v) + NBSP + "km")))
    its.append((1, emcq(E("Sofia is {x} years old. Her brother is 4 years younger than she is, and her cousin is twice as old as Sofia. "
                          "Which expression gives the sum of the three ages?"),
                        "4x - 4", ["4x + 4", "3x - 4", "2x - 4"],
                        E("Sofia {x}, brother {x - 4}, cousin {2x}. Sum: {x + (x - 4) + 2x} = {4x - 4}. "
                          "(4{x} + 4 makes the brother older instead of younger.)"), rnd, "x + (x - 4) + 2x")))
    # C: harder
    its.append((2, emcq(E("A rectangle has a perimeter of {10x + 6}. Its length is {3x + 2}. Which expression gives its width?"),
                        "2x + 1", ["7x + 4", "4x + 2", "5x + 3"],
                        E("Length + width is half the perimeter: {5x + 3}. Width: {(5x + 3) - (3x + 2)} = {2x + 1}. "
                          "Check: {2(3x + 2) + 2(2x + 1)} = {10x + 6}. (4{x} + 2 forgets to halve.)"), rnd, "(5x + 3) - (3x + 2)")))
    assert same("(2x + 3) + (4x - 1) + (3x - 4)", "9x - 2")
    its.append((2, emcq(E("A triangle has a perimeter of {9x - 2}. Two of its sides are {2x + 3} and {4x - 1}. Which expression gives the third side?"),
                        "3x - 4", ["3x - 2", "3x", "3x + 4"],
                        E("The two sides add to {6x + 2}. The third side is {9x - 2} minus that: {3x - 4}. "
                          "Check: {(2x + 3) + (4x - 1) + (3x - 4)} = {9x - 2}. (3{x} " + M + " 2 subtracts only the {x}-terms.)"),
                        rnd, "(9x - 2) - (6x + 2)")))
    its.append((2, emcq(E("At a hockey game, an adult ticket costs {x} dollars and a student ticket costs $6 less. "
                          "Which expression gives the cost of 2 adult tickets and 3 student tickets?"),
                        "5x - 18", ["5x - 6", "5x + 18", "5x - 12"],
                        E("{x + x + (x - 6) + (x - 6) + (x - 6)}: {x}-terms 5{x}, constants " + M + "6 three times = " + M + "18. "
                          "Total: {5x - 18}. (5{x} " + M + " 6 takes $6 off only once.)"), rnd, "x + x + (x - 6) + (x - 6) + (x - 6)")))
    assert ev("5x - 18", x=15) == 57
    its.append((2, mcq(E("The tickets cost ({5x - 18}) dollars. What is the total cost when an adult ticket costs $15?"), 57,
                       [69, 93, 75],
                       E("5 × 15 = 75. Then 75 " + M + " 18 = 57, so $57.00. ($69.00 uses {5x - 6}. $93.00 adds the 18.)"),
                       rnd, money)))
    its.sort(key=lambda t: t[0])
    return {"title": "Perimeter and word problems", "items": [i for _, i in its]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    t1 = tiles_svg(["x x x x x -x -x -x"], label="algebra tiles: 5 x-tiles and 3 negative x-tiles")
    t2 = tiles_svg(["x x 1 1 1", "x -1 -1 -1 -1 -1"], "+", "algebra tiles: 2x + 3 plus x - 5")
    t3 = tiles_svg(["x x x x x -x* -x* -x*"], label="algebra tiles: 2 x-tiles and 3 zero pairs, 3 negative x-tiles crossed out")
    r1 = rect_svg("2x + 3", "x - 1", "rectangle with length 2x + 3 and width x - 1")
    return E(
        "<h2>Like terms and zero pairs</h2>"
        "<p><b>Like terms</b> have the same variable part, such as {-3x} and {5x}, or two constants. "
        "To combine like terms, add the coefficients and keep the variable. Use integer rules for the signs.</p>"
        "<figure class='sn-fig'>" + t1 +
        "<figcaption>Green tiles are {x} and red tiles are {-x}. A green tile and a red tile make a <b>zero pair</b>. "
        "Here 3 zero pairs are removed and 2 green tiles are left: {5x - 3x} = {2x}.</figcaption></figure>" +
        table(["Expression", "Add the coefficients", "Result"], [
            ["{-3x + 5x}", M + "3 + 5 = 2", "{2x}"],
            ["{-4x - 6x}", M + "4 " + M + " 6 = " + M + "10", "{-10x}"],
            ["{-x + 6x}", M + "1 + 6 = 5", "{5x}"],
        ]) +
        "<p>{x} means {1x}, and {-x} means {-1x}. Terms that are not alike stay apart: {3x + 2} cannot be simplified.</p>"
        "<h2>Add binomials</h2>"
        "<p>A <b>binomial</b> has two terms, like {2x + 3}. To add binomials, group the {x}-terms and the constants. "
        "Each sign belongs to the term right after it.</p>"
        "<figure class='sn-fig'>" + t2 +
        "<figcaption>{(2x + 3) + (x - 5)}: 3 green {x}-tiles, and 3 yellow with 5 red 1-tiles leave " + M + "2. "
        "The sum is {3x - 2}.</figcaption></figure>" +
        ex("Example 1", "Add {(-6k - 2) + (k + 5)}.",
           "{k}-terms: " + M + "6 + 1 = " + M + "5. Constants: " + M + "2 + 5 = 3.", "{-5k + 3}") +
        "<h2>Subtract monomials</h2>"
        "<p>To subtract, add the opposite: {6x - (-4x)} = {6x + 4x} = {10x}.</p>"
        "<figure class='sn-fig'>" + t3 +
        "<figcaption>{2x - (-3x)}: add 3 zero pairs, then take away 3 red tiles. 5 green tiles are left: {5x}."
        "</figcaption></figure>" +
        "<h2>Evaluate expressions</h2>"
        "<p>Replace the variable with its value in brackets, then follow the order of operations.</p>" +
        ex("Example 2", "Evaluate {-3x + 4} when {x} = " + M + "2.",
           M + "3 × (" + M + "2) = 6. Then 6 + 4 = 10.", "10") +
        ex("Example 3", "Evaluate {2x} " + M + " " + fr(3, 4) + " when {x} = " + fr(5, 8) + ".",
           "2 × " + fr(5, 8) + " = " + fr(10, 8) + ". " + fr(10, 8) + " " + M + " " + fr(6, 8) + " = " + fr(4, 8) + ".",
           fr(1, 2)) +
        "<h2>Perimeter</h2>"
        "<figure class='sn-fig'>" + r1 +
        "<figcaption>Add all four sides: {(2x + 3) + (x - 1) + (2x + 3) + (x - 1)} = {6x + 4}.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["{3x + 2} = {5x}", "{3x} and 2 are not like terms. {3x + 2} is already simplified"],
            ["{-3x + 5x} = {-8x}", "Use integer rules: " + M + "3 + 5 = 2, so {2x}"],
            ["{(2x + 3) + (x - 5)} = {3x + 8}", "The minus sign belongs to 5: 3 + (" + M + "5) = " + M + "2"],
            ["{6x - (-4x)} = {2x}", "Add the opposite: {6x + 4x} = {10x}"],
            ["(" + M + "3)<sup>2</sup> = " + M + "9", "(" + M + "3) × (" + M + "3) = 9"],
            ["Adding only two sides for a perimeter", "Add every side of the shape"],
        ]))


FAQ = [
    {"q": "What do Grade 8 students learn about algebraic expressions in the Ontario math curriculum?",
     "a": "In Grade 8 (Algebra, C2.1 and C2.2), students add and subtract monomials such as −3x + 5x, add binomials such as (2x + 3) + (x − 5), often with algebra tiles, and evaluate expressions that involve integers, fractions and decimals."},
    {"q": "How do you add two binomials?",
     "a": "Group the like terms and add each group. For (2x + 3) + (x − 5), the x-terms give 3x and the constants give 3 + (−5) = −2, so the sum is 3x − 2."},
    {"q": "What is a zero pair in algebra tiles?",
     "a": "A zero pair is one positive tile and one negative tile of the same kind, such as x and −x. Together they equal 0, so they can be removed or added without changing the value."},
    {"q": "Is −3x + 5x equal to 2x or −8x?",
     "a": "It is 2x. Add the coefficients with integer rules: −3 + 5 = 2. −8x is a common sign error."},
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
    rnd = random.Random(48810)
    sets = [set_like(rnd), set_binomials(rnd), set_subtract(rnd), set_evaluate(rnd), set_context(rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "expressions-and-binomials", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Expressions and Binomials: Like Terms with Integers, Adding Binomials and Evaluating",
        "seo_title": "Grade 8 Expressions and Binomials Worksheets: Like Terms and Evaluating (Free, Answer Key)",
        "short_title": "Expressions and Binomials",
        "domain": "Algebra",
        "standard_code": "Grade 8: C2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Add and subtract monomials with a degree of 1, and add binomials with a degree of 1 that involve integers, using tools",
        "meta_desc": "Free Grade 8 math worksheets on expressions and binomials for the Ontario curriculum: combining like terms with integers and algebra tiles, adding binomials, subtracting monomials, evaluating expressions with integers and fractions, and perimeter problems. 100 questions with an answer key.",
        "key_big": "Combine only like terms, using integer rules: −3x + 5x = 2x, and (2x + 3) + (x − 5) = 3x − 2.",
        "key_sub": "3x + 2 is not 5x. To subtract, add the opposite: 6x − (−4x) = 10x. To evaluate, put the value in brackets: −3(−2) + 4 = 10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "algebra tiles")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
