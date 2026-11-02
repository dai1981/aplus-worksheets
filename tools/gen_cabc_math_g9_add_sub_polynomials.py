# -*- coding: utf-8 -*-
"""
British Columbia Grade 9 Math: Adding and Subtracting Polynomials
(BC Mathematics Curriculum, Mathematics 9 — Patterning: operations with polynomials, of degree less than or equal to 2)
  python3 tools/gen_cabc_math_g9_add_sub_polynomials.py
Terms, degree, coefficients and like terms; algebra tiles with x^2-, x- and 1-tiles and zero pairs; adding
polynomials (horizontal, terms out of order, three polynomials, missing polynomial, error analysis); subtracting
polynomials by adding the opposite (change the sign of every term); perimeter and BC word problems.
Wrong choices come from real mistakes: x + x = x^2 (and x^2 + x^2 = x^4), joining unlike terms (3x^2 + 2x = 5x^2),
changing only the sign of the first term when subtracting, forgetting the sign of the last term, adding instead
of subtracting, subtracting in the wrong order, counting red tiles as positive, adding only two sides of a rectangle.
Every answer is checked in code: polynomials are compared as coefficient lists and at several values of x.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
SQ = "#a9cbe8"      # x^2-tile
SQS = "#2b6ca3"
XT = "#7fc495"      # x-tile
ONE = "#f4d35e"     # 1-tile
NEG = "#f7cfc9"     # any negative tile
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """BC style: 4536, 10 000 (no-break space), real minus sign."""
    v = Fr(v)
    assert v.denominator == 1, v
    s = str(abs(v.numerator))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NBSP.join(g)
    return (M if v < 0 else "") + s


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
    """Plain expression '3x^2 - 2x' -> HTML: letters in italics, ^2 as a superscript, real minus sign."""
    s = s.replace("-", M).replace("*", "×")
    s = re.sub(r"[a-z]", lambda m: "<i>%s</i>" % m.group(), s)
    return re.sub(r"\^(\d)", r"<sup>\1</sup>", s)


def E(s):
    """Text with expressions in braces: 'Add {3x^2} and {5x}' -> the braces become X(...)."""
    return re.sub(r"\{([^{}]*)\}", lambda m: X(m.group(1)), s.replace(" - ", " " + M + " "))


def ev(expr_, **env):
    t = expr_.replace(M, "-").replace("×", "*").replace("^", "**").replace(" ", "")
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Q('%s')" % m.group(), t)
    t = re.sub(r"(\)|[a-z])(?=[a-zQ(])", r"\1*", t)
    e = {"Q": Fr}
    for k, v in env.items():
        e[k] = Fr(v)
    return eval(t, {"__builtins__": {}}, e)


def same(a, b):
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2), -5, 11):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


# ------------------------------------------------------------ polynomials as {degree: coefficient}
def P(a2=0, a1=0, a0=0):
    return norm({2: a2, 1: a1, 0: a0})


def norm(p):
    return {d: c for d, c in p.items() if c != 0}


def padd(*ps):
    r = {}
    for p in ps:
        for d, c in p.items():
            r[d] = r.get(d, 0) + c
    return norm(r)


def pneg(p):
    return {d: -c for d, c in p.items()}


def psub(a, b):
    return padd(a, pneg(b))


def pscale(p, k):
    return norm({d: c * k for d, c in p.items()})


def fmt(p, v="x"):
    """{2: 3, 1: -1, 0: 4} -> '3x^2 - x + 4' (plain, descending order)."""
    out = []
    for d in sorted(p, reverse=True):
        c = p[d]
        if c == 0:
            continue
        a = abs(c)
        if d == 0:
            t = str(a)
        else:
            t = ("" if a == 1 else str(a)) + v + ("^%d" % d if d > 1 else "")
        if not out:
            out.append(("-" if c < 0 else "") + t)
        else:
            out.append(("- " if c < 0 else "+ ") + t)
    return " ".join(out) if out else "0"


def B(p, v="x"):
    return "(" + fmt(p, v) + ")"


def num(c):
    return n(c)


def par(c):
    return "(" + n(c) + ")" if c < 0 else n(c)


LAB = {2: "{x^2}-terms", 1: "{x}-terms", 0: "constants"}


def lab(d, v):
    s = LAB[d]
    if v != "x":
        s = s.replace("x", v)
    return s


def steps(a, b, v="x"):
    """'x^2-terms: 3 + (−2) = 1. x-terms: ...' for a + b (b already has its new signs)."""
    out = []
    for d in (2, 1, 0):
        ca, cb = a.get(d, 0), b.get(d, 0)
        if ca == 0 and cb == 0:
            continue
        s = lab(d, v)
        s = s[0].upper() + s[1:] if s[0] != "{" else s
        out.append("%s: %s + %s = %s" % (s, num(ca), par(cb), num(ca + cb)))
    return ". ".join(out) + "."


# mistakes when adding a + b
def m_xsq(a, b):
    """x + x = x^2: when both have a variable term of degree d, the result gets degree 2d."""
    r = {}
    for d in set(a) | set(b):
        c = a.get(d, 0) + b.get(d, 0)
        dd = 2 * d if (d > 0 and a.get(d) and b.get(d)) else d
        r[dd] = r.get(dd, 0) + c
    return norm(r)


def m_sign(a, b):
    return padd(a, {d: abs(c) for d, c in b.items()})


def m_unlike(r):
    if r.get(2) and r.get(1):
        return norm({2: r[2] + r[1], 0: r.get(0, 0)})
    return None


def m_noconst(a, b):
    return padd(a, {d: c for d, c in b.items() if d})


# mistakes when subtracting a - b
def lead(p):
    return max(p) if p else 0


def m_first(a, b):
    """Changes only the sign of the first term of b."""
    d0 = lead(b)
    return padd(a, {d: (-c if d == d0 else c) for d, c in b.items()})


def m_last(a, b):
    """Changes every sign except the last term of b."""
    dl = min(b)
    return padd(a, {d: (c if d == dl else -c) for d, c in b.items()})


ADD_PH = {"xsq": "uses {x + x} = {x^2}, but {x + x} = {2x}",
          "sign": "ignores the minus signs",
          "unlike": "joins unlike terms",
          "noconst": "forgets a constant",
          "dropterm": "leaves out a term of the second polynomial",
          "x4": "adds the exponents: {x^2 + x^2} is {2x^2}, not {2x^4}"}
SUB_PH = {"first": "changes only the sign of the first term",
          "last": "forgets to change the sign of the last term",
          "none": "adds instead of subtracting",
          "rev": "subtracts in the wrong order",
          "xsq": "uses {x + x} = {x^2}"}


def pick(correct, cands, k=3):
    """cands: list of (poly or None, key). First k distinct polys that differ from correct."""
    got, keys = [], []
    for p, key in cands:
        if p is None or p == correct or p in got:
            continue
        got.append(p)
        keys.append(key)
        if len(got) == k:
            break
    assert len(got) == k, (correct, cands)
    return got, keys


def add_wrongs(a, b, extra=()):
    r = padd(a, b)
    lastd = min(b)
    x4 = norm({(4 if d == 2 and a.get(2) and b.get(2) else d): c for d, c in r.items()})
    return pick(r, [(m_xsq(a, b), "xsq"), (m_sign(a, b), "sign"), (m_unlike(r), "unlike"),
                    (m_noconst(a, b), "noconst")] + list(extra) +
                [(padd(a, {d: c for d, c in b.items() if d != lastd}), "dropterm"), (x4, "x4")])


def sub_wrongs(a, b, order=("first", "last", "none", "rev", "xsq"), extra=()):
    r = psub(a, b)
    c = {"first": m_first(a, b), "last": m_last(a, b), "none": padd(a, b), "rev": psub(b, a),
         "xsq": m_xsq(a, pneg(b))}
    return pick(r, [(c[k], k) for k in order] + list(extra))


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None):
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pk = {plain(cs)}, {cv}, []
    for c in cands:
        if disp is not None:
            c = Fr(c)
            assert c not in vals, (q, c)
            vals.add(c)
            c = disp(c)
        assert plain(c) not in seen, (q, c)
        seen.add(plain(c))
        pk.append(c)
    assert len(pk) == 3, (q, cs, cands)
    ch = pk + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def emcq(q, good, bad, e, rnd, src=None):
    if src is not None:
        assert same(good, src), (src, good)
    for b in bad:
        assert not same(good, b), (good, b)
    return mcq(q, X(good), [X(b) for b in bad], e, rnd)


def pmcq(q, good, bad, e, rnd, src=None, v="x"):
    return emcq(q, fmt(good, v), [fmt(b, v) for b in bad], e, rnd, src)


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
    """Expression inside SVG text: letters in italics, x^2 as x², real minus sign."""
    s = s.replace("-", M).replace("^2", "²")
    return re.sub(r"[a-z]", lambda m: "<tspan font-style='italic'>%s</tspan>" % m.group(), s)


def tw(s, fs=17):
    """Rough width of bold Arial text."""
    return 0.6 * fs * len(s.replace("^2", "²"))


U, XL, GAP = 24, 56, 5     # 1-tile side, x^2-tile side (= x-tile length), gap


def cross(x, y, w, h):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
            % (x - 2, y + 2, x + w + 2, y + h - 2, INK, x + w + 2, y + 2, x - 2, y + h - 2, INK))


def tile(kind, x, y):
    k = kind.rstrip("*")
    neg = k.startswith("-")
    base = k.lstrip("-")
    if base == "X":
        w, h, fill, st, lb, fs = XL, XL, SQ, SQS, "<tspan font-style='italic'>x</tspan>²", 16
    elif base == "x":
        w, h, fill, st, lb, fs = U, XL, XT, GREEN, "<tspan font-style='italic'>x</tspan>", 16
    else:
        w, h, fill, st, lb, fs = U, U, ONE, "#8a6d00", "1", 14
    if neg:
        fill, st = NEG, RED
    s = ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x, y, w, h, fill, st, ))
    s += text(x + w / 2, y + h / 2 + fs * 0.35, (M if neg else "") + lb, fs)
    if kind.endswith("*"):
        s += cross(x, y, w, h)
    return s, w


def tiles_svg(groups, ops=(), label="algebra tiles"):
    """groups: strings like 'X X -x 1 -1'; X = x^2-tile, x = x-tile, 1 = 1-tile, '-' negative, '*' crossed out."""
    PAD = 6
    x = PAD
    s = []
    for gi, g in enumerate(groups):
        if gi:
            s.append(text(x + 12, PAD + XL / 2 + 9, ops[gi - 1], 26))
            x += 30
        ts = g.split()
        first = True
        for kind in ("X", "x"):
            part = [t for t in ts if t.rstrip("*").lstrip("-") == kind]
            part.sort(key=lambda t: t.startswith("-"))
            for t in part:
                sv, w = tile(t, x, PAD)
                s.append(sv)
                x += w + GAP
            if part:
                first = False
        ones = [t for t in ts if t.rstrip("*").lstrip("-") == "1"]
        for part in ([t for t in ones if not t.startswith("-")], [t for t in ones if t.startswith("-")]):
            if not part:
                continue
            x += 0 if first else 4
            first = False
            for i, t in enumerate(part):
                c, r = divmod(i, 2)
                sv, _ = tile(t, x + c * (U + GAP), PAD + XL - U - r * (U + 8))
                s.append(sv)
            x += ((len(part) + 1) // 2) * (U + GAP)
    W = x - GAP + PAD
    return svg_wrap(W, XL + 2 * PAD, "".join(s), label)


def ptiles(p):
    """Tile string for a polynomial (no zero pairs)."""
    out = []
    for d, k in ((2, "X"), (1, "x"), (0, "1")):
        c = p.get(d, 0)
        out += [("-" if c < 0 else "") + k] * abs(c)
    return " ".join(out)


def tlabel(g):
    ts = [t.rstrip("*") for t in g.split()]
    parts = []
    for k, name in [("X", "x-squared tiles"), ("-X", "negative x-squared tiles"), ("x", "x-tiles"),
                    ("-x", "negative x-tiles"), ("1", "1-tiles"), ("-1", "negative 1-tiles")]:
        c = ts.count(k)
        if c:
            parts.append("%d %s" % (c, name))
    return ", ".join(parts)


def tile_value(g):
    """Value of a tile string, ignoring crossed-out tiles."""
    r = {}
    for t in g.split():
        if t.endswith("*"):
            continue
        neg = t.startswith("-")
        d = {"X": 2, "x": 1, "1": 0}[t.lstrip("-")]
        r[d] = r.get(d, 0) + (-1 if neg else 1)
    return norm(r)


def rect_svg(top, side, label, w=190, h=84):
    T = 30
    L = max(20, tw(side) + 16)
    W = L + w + 8
    over = tw(top) / 2 - w / 2
    if over > 0:
        L = max(L, over + 8)
        W = L + w + over + 8
    s = ["<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, SX(top), 17))
    s.append(text(L - 8, T + h / 2 + 6, SX(side), 17, "end"))
    return svg_wrap(W, T + h + 8, "".join(s), label)


def tri_svg(a, b, c, label):
    """Triangle with sides labelled a (left), b (right), c (bottom)."""
    ox = max(10, tw(a) - 38)
    P_ = [(ox, 120), (ox + 200, 120), (ox + 100, 20)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%d,%d" % p for p in P_), FILL, GREEN)]
    s.append(text(ox + 42, 66, SX(a), 17, "end"))
    s.append(text(ox + 158, 66, SX(b), 17, "start"))
    s.append(text(ox + 100, 143, SX(c), 17))
    W = max(ox + 158 + tw(b) + 6, ox + 100 + tw(c) / 2 + 6, ox + 210)
    return svg_wrap(W, 152, "".join(s), label)


def trap_svg(top, bottom, left, right, label):
    ox = max(10, tw(left) - 6)
    P_ = [(ox, 130), (ox + 220, 130), (ox + 170, 34), (ox + 50, 34)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%d,%d" % p for p in P_), FILL, GREEN)]
    s.append(text(ox + 110, 25, SX(top), 17))
    s.append(text(ox + 110, 153, SX(bottom), 17))
    s.append(text(ox + 17, 88, SX(left), 17, "end"))
    s.append(text(ox + 203, 88, SX(right), 17, "start"))
    W = max(ox + 203 + tw(right) + 6, ox + 110 + tw(bottom) / 2 + 6)
    return svg_wrap(W, 162, "".join(s), label)


def hex_svg(side, label):
    cx, cy, r = 80, 72, 54
    P_ = [(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i))) for i in range(6)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%.1f,%.1f" % p for p in P_), FILL, GREEN)]
    mx, my = (P_[5][0] + P_[0][0]) / 2, (P_[5][1] + P_[0][1]) / 2
    s.append(text(mx + 10, my - 2, SX(side), 17, "start"))
    return svg_wrap(mx + 10 + tw(side) + 6, 2 * cy, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: terms, degree and like terms
def set_terms(rnd):
    its = []
    # A: names by number of terms
    rows = [
        ("Which polynomial is a binomial?", "4x - 9", ["4x", "x^2 + 4x - 9", "-9x^2"],
         "A <b>binomial</b> has two terms. {4x - 9} has the terms {4x} and {-9}. ({x^2 + 4x - 9} has three terms.)"),
        ("Which polynomial is a trinomial?", "2x^2 - x + 5", ["2x^2 - 5", "2x^2", "x + 5"],
         "A <b>trinomial</b> has three terms: {2x^2}, {-x} and 5. ({2x^2 - 5} has only two terms.)"),
        ("Which polynomial is a monomial?", "-7x^2", ["7 - x^2", "x^2 + 7x", "7x^2 - x + 1"],
         "A <b>monomial</b> has one term. {-7x^2} is one term: the minus sign is part of the coefficient. "
         "({7 - x^2} is two terms.)"),
    ]
    for q, good, bad, e in rows:
        its.append((0, mcq(q, X(good), [X(b) for b in bad], E(e), rnd)))
    its.append((0, mcq(E("How many terms does {6x^2 - 5x + 1} have?"), 3, [2, 6, 1],
                       E("The terms are {6x^2}, {-5x} and 1. Each + or " + M + " sign starts a new term, so there are 3 terms. "
                         "(2 counts the signs instead of the terms.)"), rnd, n)))
    # B: degree
    rows = [
        ("5x^2 + 3x - 1", 2, [5, 3, 1],
         "The degree is the greatest exponent on the variable. {5x^2} has exponent 2, so the degree is 2. "
         "(5 is a coefficient. 3 is the number of terms.)"),
        ("7x - 4", 1, [7, 2, 0],
         "{7x} means {7x^1}, so the greatest exponent is 1. The degree is 1. (2 is the number of terms.)"),
        ("-6", 0, [1, -6, 6],
         "A constant has no variable. You can think of it as {-6x^0}, so the degree is 0. (" + M + "6 is the value, not the degree.)"),
        ("4xy + 3x", 2, [1, 4, 3],
         "For a term with two variables, add their exponents: {xy} = {x^1y^1}, so 1 + 1 = 2. The degree is 2. "
         "(1 looks only at the exponent of {x}.)"),
        ("3 + 2x - x^2", 2, [0, 3, 1],
         "Look at every term, not only the first one. {-x^2} has exponent 2, so the degree is 2. "
         "(0 uses only the first term, 3.)"),
    ]
    for p, ans, wrong, e in rows:
        its.append((1, mcq(E("What is the degree of {%s}?" % p), ans, wrong, E(e), rnd, n)))
    # C: coefficients and constant term
    its.append((2, mcq(E("What is the coefficient of {x} in {3x^2 - x + 8}?"), -1, [1, 0, 3],
                       E("{-x} means {-1x}, so the coefficient is " + M + "1. The sign belongs to the term after it. "
                         "(0 forgets that {x} on its own is {1x}.)"), rnd, n)))
    its.append((2, mcq(E("What is the constant term of {2x^2 + 5x - 9}?"), -9, [9, 2, 5],
                       E("The constant term has no variable: {-9}. Keep the minus sign in front of it. (9 drops the sign.)"), rnd, n)))
    its.append((2, mcq(E("What is the coefficient of {x^2} in {4 - 7x^2 + x}?"), -7, [7, 4, 2],
                       E("The {x^2}-term is {-7x^2}, so the coefficient is " + M + "7. (2 is the exponent, not the coefficient. "
                         "4 is the constant term.)"), rnd, n)))
    # D: like terms
    its.append((3, mcq(E("Which term is a like term with {3x^2}?"), X("-5x^2"), [X("3x"), X("3y^2"), "3"],
                       E("Like terms have the same variable with the same exponent. {-5x^2} and {3x^2} both have {x^2}. "
                         "({3x} has exponent 1. {3y^2} has a different variable.)"), rnd)))
    its.append((3, mcq("Which pair are like terms?", X("-2x") + " and " + X("9x"),
                       [X("4x") + " and " + X("4x^2"), "5 and " + X("5x"), X("x^2") + " and " + X("y^2")],
                       E("{-2x} and {9x} both have {x} to the exponent 1, so they are like terms. The coefficients can be different. "
                         "({4x} and {4x^2} have different exponents.)"), rnd)))
    its.append((3, mcq(E("Which term is a like term with {7xy}?"), X("-2yx"), [X("7x"), X("7y"), X("7x^2")],
                       E("{yx} is the same as {xy}, because the order of multiplying does not matter. So {-2yx} is a like term with {7xy}. "
                         "({7x} has no {y}.)"), rnd)))
    assert ev("x + x", x=3) == 6 and ev("x^2", x=3) == 9
    its.append((3, mcq(E("Leah says {x + x} = {x^2}. Which statement is correct?"), E("{x + x} = {2x}"),
                       [E("{x + x} = {x^2}"), E("{x + x} = {2x^2}"), E("{x × x} = {2x}")],
                       E("{x + x} is two {x}'s, so it is {2x}. Test with {x} = 3: {x + x} = 6, but {x^2} = 9. "
                         "{x^2} means {x × x}.").replace("'", "’"), rnd)))
    # E: collect like terms
    rows = [
        ("3x + 5x", "8x", ["8x^2", "15x", "8"],
         "Add the coefficients and keep the variable: 3 + 5 = 8, so {8x}. ({8x^2} uses {x + x} = {x^2}.)"),
        ("4x^2 + 2x^2 - x^2", "5x^2", ["5x^6", "7x^2", "6x^2"],
         "Add the coefficients: 4 + 2 " + M + " 1 = 5. The exponent does not change: {5x^2}. "
         "({5x^6} adds the exponents. 7{x^2} ignores the minus sign.)"),
        ("2x^2 + 3x + 5x^2 - 7x", "7x^2 - 4x", ["3x^2", "7x^2 + 10x", "7x^4 - 4x^2"],
         "{x^2}-terms: 2 + 5 = 7. {x}-terms: 3 " + M + " 7 = " + M + "4. The answer is {7x^2 - 4x}. "
         "(3{x^2} joins unlike terms. {7x^4 - 4x^2} uses {x + x} = {x^2}.)"),
        ("x^2 - 3x + 4 - 4x^2 + x - 6", "-3x^2 - 2x - 2", ["-3x^2 - 2x + 10", "5x^2 - 2x - 2", "-7"],
         "{x^2}-terms: 1 " + M + " 4 = " + M + "3. {x}-terms: " + M + "3 + 1 = " + M + "2. Constants: 4 " + M + " 6 = " + M + "2. "
         "The answer is {-3x^2 - 2x - 2}. ({5x^2} ignores the minus sign of {4x^2}. " + M + "7 joins unlike terms.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((4, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    its.sort(key=lambda t: t[0])
    return {"title": "Terms, degree and like terms", "items": [i for _, i in its]}


# ============================================================ set 2: algebra tiles
def tile_note():
    return "Blue tiles are {x^2}, green tiles are {x} and yellow tiles are 1. Red tiles are negative. "


def set_tiles(rnd):
    its = []
    # A: read the tiles
    rows = [
        ("X X x x x 1 1", ["3x^2 + 2x + 2", "5x + 2", "7"],
         "2 blue tiles, 3 green tiles and 2 yellow tiles: {2x^2 + 3x + 2}. "
         "({3x^2 + 2x + 2} mixes up the large square and the long tiles.)"),
        ("X -x -x -x -x 1 1 1", ["x^2 + 4x + 3", "-3x + 3", "x^2 - 4x - 3"],
         "1 blue tile, 4 red {x}-tiles and 3 yellow tiles: {x^2 - 4x + 3}. ({x^2 + 4x + 3} counts the red tiles as positive.)"),
        ("-X -X x 1 -1 -1 -1 -1", ["2x^2 + x + 5", "-2x^2 + x - 4", "-x^2 - 3"],
         "2 red {x^2}-tiles give {-2x^2}. 1 green tile gives {x}. 1 yellow and 1 red 1-tile make a zero pair, so 3 red 1-tiles are left: "
         + M + "3. The tiles show {-2x^2 + x - 3}. ({-2x^2 + x - 4} forgets the yellow tile.)"),
        ("X X X -X x x -x -x -x 1 1 -1", ["4x^2 + 5x + 3", "2x^2 + x + 1", "x^2 + 1"],
         "{x^2}-tiles: 3 blue and 1 red leave {2x^2}. {x}-tiles: 2 green and 3 red leave {-x}. 1-tiles: 2 yellow and 1 red leave 1. "
         "The tiles show {2x^2 - x + 1}. ({4x^2 + 5x + 3} counts the red tiles as positive.)"),
        ("X -x -x 1 1 1 -1 -1 -1", ["x^2 + 2x", "x^2 - 2x + 3", "-x"],
         "The 3 yellow and 3 red 1-tiles are 3 zero pairs, so they make 0. The tiles show {x^2 - 2x}. "
         "({-x} joins {x^2} and {-2x}, which are not like terms.)"),
    ]
    for g, bad, e in rows:
        good = fmt(tile_value(g))
        q = fig(tiles_svg([g], label="algebra tiles: " + tlabel(g))) + E(tile_note() + "Which polynomial do the tiles show?")
        its.append((0, emcq(q, good, bad, E(e), rnd)))
    # count tiles left
    g = "X X -X x x x -x 1 -1 -1"
    its.append((0, mcq(fig(tiles_svg([g], label="algebra tiles: " + tlabel(g))) +
                       E(tile_note() + "Remove all the zero pairs. How many tiles are left?"), 4, [10, 7, 6],
                       E("There is 1 zero pair of {x^2}-tiles, 1 of {x}-tiles and 1 of 1-tiles: 3 pairs, or 6 tiles. "
                         "10 " + M + " 6 = 4 tiles are left, which show {x^2 + 2x - 1}. (6 is the number of tiles removed. "
                         "7 removes only one tile from each pair.)"), rnd, n)))
    # B: add with tiles
    rows = [
        (P(1, 2, 1), P(1, 1, 3)),
        (P(2, -1, 3), P(1, 3, -1)),
        (P(-1, 2, -2), P(2, 1, 4)),
        (P(1, -3, 0), P(-1, 1, 2)),
        (P(2, 1, -3), P(-1, -2, 1)),
        (P(0, 3, -2), P(1, -1, -2)),
        (P(-2, 0, 3), P(3, -2, -1)),
    ]
    for a, b in rows:
        r = padd(a, b)
        bad, keys = add_wrongs(a, b, extra=[(padd(a, b, P(0, 0, 1)), "count")])
        g1, g2 = ptiles(a), ptiles(b)
        q = (fig(tiles_svg([g1, g2], "+", "algebra tiles: %s, plus %s" % (tlabel(g1), tlabel(g2)))) +
             E(tile_note() + "The tiles show {%s + %s}. What is the sum?" % (B(a), B(b))))
        ph = {"xsq": "uses {x + x} = {x^2}", "sign": "counts the red tiles as positive",
              "unlike": "joins unlike terms", "noconst": "forgets some 1-tiles", "count": "miscounts the 1-tiles"}
        e = ("Group the tiles of the same kind and remove zero pairs. " + steps(a, b) +
             " The sum is {%s}. ({%s} %s.)" % (fmt(r), fmt(bad[0]), ph[keys[0]]))
        its.append((1, pmcq(q, r, bad, E(e), rnd, "%s + %s" % (B(a), B(b)))))
    # C: opposite with tiles
    for a in (P(1, 2, -3), P(-2, 1, 4)):
        g = ptiles(a)
        r = pneg(a)
        bad = [m_first(P(), a), a, pneg(padd(a, {0: -2 * a[0]}))]
        bad = [norm(b) for b in bad]
        q = (fig(tiles_svg([g], label="algebra tiles: " + tlabel(g))) +
             E(tile_note() + "Which polynomial is the <b>opposite</b> of the polynomial shown? (Together they make zero.)"))
        e = ("To make zero, flip every tile to the other colour, so change the sign of every term: "
             "the opposite of {%s} is {%s}. ({%s} changes only the first sign.)" % (fmt(a), fmt(r), fmt(bad[0])))
        its.append((2, pmcq(q, r, bad, E(e), rnd, "-%s" % B(a))))
    # D: subtract with tiles
    rows = [
        ("X X X x x x x 1 1 1 1 1", "X* x* x* 1*", P(3, 4, 5), P(1, 2, 1)),
        ("X X -x -x -x 1 1 1 1", "X* -x* -x* 1*", P(2, -3, 4), P(1, -2, 1)),
    ]
    for start, remove, a, b in rows:
        assert tile_value(start) == a and tile_value(remove.replace("*", "")) == b
        # draw one row: crossed tiles replace the matching ones
        toks = start.split()
        for t in remove.split():
            toks.remove(t.rstrip("*"))
        g = " ".join(toks + remove.split())
        r = psub(a, b)
        assert tile_value(g) == r
        bad, keys = sub_wrongs(a, b, order=("first", "none", "last", "rev"))
        q = (fig(tiles_svg([g], label="algebra tiles: " + tlabel(g) + ", some crossed out")) +
             E(tile_note() + "The tiles show {%s - %s}: the crossed-out tiles are taken away. What is the difference?"
               % (B(a), B(b))))
        e = ("Count the tiles that are left. " + steps(a, pneg(b)) +
             " The difference is {%s}. ({%s} %s.)" % (fmt(r), fmt(bad[0]), SUB_PH[keys[0]]))
        its.append((3, pmcq(q, r, bad, E(e), rnd, "%s - %s" % (B(a), B(b)))))
    # E: subtract with zero pairs
    rows = [
        ("X x x x -x*", P(1, 2, 0), P(0, -1, 0), ["x^2 + x", "x^2 - 3x", "x^2 + 2x"],
         "There is no red {x}-tile to take away, so add a zero pair ({x} and {-x}). Take away the red tile: "
         "{x^2 + 2x - (-x)} = {x^2 + 3x}. Subtracting a negative is the same as adding. ({x^2 + x} subtracts {x} instead.)"),
        ("X X -X* -x -x 1 1 1", P(1, -2, 3), P(-1, 0, 0), ["-2x + 3", "2x^2 + 2x + 3", "x^2 - 2x + 3"],
         "Add a zero pair of {x^2}-tiles, then take away the red one. 2 blue tiles are left: "
         "{x^2 - 2x + 3 - (-x^2)} = {2x^2 - 2x + 3}. ({-2x + 3} subtracts {x^2} instead of adding it.)"),
        ("x x x* 1* 1* 1* 1* -1 -1", P(0, 3, 2), P(0, 1, 4), ["2x + 2", "2x - 6", "4x - 2"],
         "Start with {3x + 2}. To take away 4 yellow tiles, add 2 zero pairs of 1-tiles first. "
         "Take away 1 green tile and 4 yellow tiles: 2 green and 2 red tiles are left, {2x - 2}. "
         "({2x + 2} subtracts 2 from 4 instead of 4 from 2.)"),
    ]
    for g, a, b, bad, e in rows:
        r = psub(a, b)
        assert tile_value(g) == r, (g, r)
        q = (fig(tiles_svg([g], label="algebra tiles: " + tlabel(g) + ", with zero pairs added and some tiles crossed out")) +
             E(tile_note() + "The tiles show {%s - %s}. Zero pairs were added, then the crossed-out tiles were taken away. "
               "What is the difference?" % (B(a), B(b))))
        its.append((4, emcq(q, fmt(r), bad, E(e), rnd, "%s - %s" % (B(a), B(b)))))
    its.sort(key=lambda t: t[0])
    return {"title": "Algebra tiles", "items": [i for _, i in its]}


# ============================================================ set 3: add polynomials
def add_q(a, b, rnd, lvl, extra=(), va="x"):
    r = padd(a, b)
    bad, keys = add_wrongs(a, b, extra)
    e = (steps(a, b, va) + " The sum is {%s}. ({%s} %s.)" % (fmt(r, va), fmt(bad[0], va), ADD_PH[keys[0]]))
    q = E("Add: {%s + %s}" % (B(a, va), B(b, va)))
    return (lvl, pmcq(q, r, bad, E(e), rnd, "%s + %s" % (B(a, va), B(b, va)), va))


def set_add(rnd):
    its = []
    rows = [
        (P(0, 4, 7), P(0, 2, -3)),
        (P(3, 2, 0), P(1, 5, 0)),
        (P(2, -5, 1), P(4, 3, 6)),
        (P(1, 6, -4), P(1, -2, -5)),
        (P(-3, 1, 8), P(5, -4, -2)),
        (P(5, 0, -9), P(-2, 7, 3)),
        (P(-1, -3, 2), P(-4, 3, -7)),
        (P(6, -2, -1), P(-6, 5, 4)),
    ]
    for a, b in rows:
        its.append(add_q(a, b, rnd, 0))
    # terms not in descending order
    rows = [
        ("4 + 3x - x^2", "2x^2 - 5 + x", P(-1, 3, 4), P(2, 1, -5)),
        ("7x - 2x^2", "6 + 2x^2 - 9x", P(-2, 7, 0), P(2, -9, 6)),
        ("-8 + n^2", "3n - 4n^2 + 8", P(1, 0, -8), P(-4, 3, 8)),
    ]
    for sa, sb, a, b in rows:
        v = "n" if "n" in sa else "x"
        assert same(sa, fmt(a, v)) and same(sb, fmt(b, v))
        r = padd(a, b)
        bad, keys = add_wrongs(a, b)
        e = ("Match like terms even when they are in a different order. " + steps(a, b, v) +
             " The sum is {%s}. ({%s} %s.)" % (fmt(r, v), fmt(bad[0], v), ADD_PH[keys[0]].replace("x", v) if keys[0] == "xsq" else ADD_PH[keys[0]]))
        its.append((1, pmcq(E("Add: {(%s) + (%s)}" % (sa, sb)), r, bad, E(e), rnd, "(%s) + (%s)" % (sa, sb), v)))
    # three polynomials
    rows = [
        (P(1, 2, 0), P(2, -1, 3), P(0, 4, -5)),
        (P(3, 0, -1), P(-1, 2, 0), P(-2, -2, 6)),
        (P(0, 2, 5), P(1, -3, 0), P(2, 0, -8)),
    ]
    for a, b, c in rows:
        r = padd(a, b, c)
        bad, keys = pick(r, [(m_xsq(padd(a, b), c), "xsq"), (padd(a, {d: abs(v) for d, v in b.items()}, {d: abs(v) for d, v in c.items()}), "sign"),
                             (m_unlike(r), "unlike"), (padd(a, b), "third"), (padd(r, P(0, 0, 2)), "const")])
        ph = dict(ADD_PH, third="leaves out the third polynomial", const="adds the constants wrongly")
        lines = []
        for d in (2, 1, 0):
            cs = [p.get(d, 0) for p in (a, b, c)]
            if any(cs):
                lb = lab(d, "x")
                lb = lb[0].upper() + lb[1:] if lb[0] != "{" else lb
                lines.append("%s: %s = %s" % (lb, " + ".join([num(cs[0])] + [par(x) for x in cs[1:]]), num(sum(cs))))
        e = ". ".join(lines) + ". The sum is {%s}. ({%s} %s.)" % (fmt(r), fmt(bad[0]), ph[keys[0]])
        src = "%s + %s + %s" % (B(a), B(b), B(c))
        its.append((2, pmcq(E("Add: {%s}" % src), r, bad, E(e), rnd, src)))
    # missing polynomial
    rows = [(P(2, 3, 0), P(5, -1, 4)), (P(-1, 4, 6), P(1, 2, -3)), (P(3, -2, -5), P(0, 1, 2))]
    for a, total in rows:
        r = psub(total, a)
        bad, keys = pick(r, [(padd(total, a), "add"), (m_first(total, a), "first"), (psub(a, total), "rev")])
        ph = {"add": "adds instead of subtracting", "first": "changes only the first sign", "rev": "subtracts in the wrong order"}
        e = ("Subtract: {%s - %s}. " % (B(total), B(a)) + steps(total, pneg(a)) +
             " Check: {%s + %s} = {%s}. ({%s} %s.)" % (B(a), B(r), fmt(total), fmt(bad[0]), ph[keys[0]]))
        assert padd(a, r) == total
        its.append((3, pmcq(E("Which polynomial must be added to {%s} to get {%s}?" % (fmt(a), fmt(total))), r, bad, E(e), rnd)))
    # error analysis
    rows = [
        ("Ji-woo", "his", P(3, 2, -4), P(1, 5, 6), "4x^4 + 7x^2 + 2", "He used " + X("x + x") + " = " + X("x^2") + ".",
         ["He ignored a minus sign.", "He joined unlike terms.", "He made no mistake."],
         "{3x^2 + x^2} = {4x^2}, not {4x^4}, and {2x + 5x} = {7x}, not {7x^2}. Adding like terms does not change the exponents. "
         "The correct sum is {4x^2 + 7x + 2}."),
        ("Nadia", "her", P(5, -3, 1), P(2, 4, -6), "7x^2 + 7x - 5", "She ignored the minus sign of " + X("-3x") + ".",
         ["She added the constants wrongly.", "She joined unlike terms.", "She made no mistake."],
         "{-3x + 4x} = {x}, not {7x}. The other terms are right: {5x^2 + 2x^2} = {7x^2} and 1 + (" + M + "6) = " + M + "5. "
         "The correct sum is {7x^2 + x - 5}."),
        ("Arjun", "his", P(2, 6, 0), P(1, -2, 3), "3x^2 + 4x + 3", "He made no mistake.",
         ["He joined unlike terms.", "He ignored a minus sign.", "He forgot the constant."],
         "{x^2}-terms: 2 + 1 = 3. {x}-terms: 6 + (" + M + "2) = 4. Constant: 3. The sum {3x^2 + 4x + 3} is correct."),
    ]
    for who, pos, a, b, wrote, good, bad, e in rows:
        r = padd(a, b)
        if "no mistake" in good:
            assert same(wrote, fmt(r))
        else:
            assert not same(wrote, fmt(r))
        q = E("%s added {%s + %s} and got {%s}. What did %s do?" % (who, B(a), B(b), wrote,
                                                                  "he" if pos == "his" else "she"))
        its.append((4, mcq(q, good, bad, E(e), rnd)))
    its.sort(key=lambda t: t[0])
    assert len(its) == 20, len(its)
    return {"title": "Add polynomials", "items": [i for _, i in its]}


# ============================================================ set 4: subtract polynomials
def set_subtract(rnd):
    its = []
    # A: opposite
    for a in (P(3, -2, 5), P(-1, 4, -6), P(4, -1, -3)):
        r = pneg(a)
        bad, keys = pick(r, [(m_first(P(), a), "first"), (m_last(P(), a), "last"), (a, "none"),
                             (norm({d: -abs(c) for d, c in a.items()}), "allneg")])
        ph = {"first": "changes only the first sign", "last": "forgets the sign of the last term",
              "none": "does not change any sign", "allneg": "makes every term negative"}
        e = ("The minus sign in front of the brackets changes the sign of <b>every</b> term: {-%s} = {%s}. ({%s} %s.)"
             % (B(a), fmt(r), fmt(bad[0]), ph[keys[0]]))
        its.append((0, pmcq(E("Simplify {-%s}." % B(a)), r, bad, E(e), rnd, "-%s" % B(a))))
    # B: subtract
    rows = [
        (P(0, 7, 5), P(0, 3, 2)),
        (P(0, 6, -1), P(0, 2, 4)),
        (P(4, 3, 0), P(1, -5, 0)),
        (P(5, 3, -4), P(2, -1, 6)),
        (P(2, -6, 1), P(3, 2, -5)),
        (P(-1, 4, 8), P(2, 4, -3)),
        (P(3, 0, -2), P(-1, 5, 7)),
        (P(6, -1, 0), P(6, 2, -9)),
        (P(-4, 2, -3), P(-2, -7, -3)),
        (P(1, 8, 2), P(-3, 1, 9)),
    ]
    for i, (a, b) in enumerate(rows):
        r = psub(a, b)
        bad, keys = sub_wrongs(a, b)
        e = ("Change the sign of every term in the second polynomial and add: {%s - %s} = {%s + %s}. "
             % (B(a), B(b), B(a), B(pneg(b))) + steps(a, pneg(b)) +
             " The difference is {%s}. ({%s} %s.)" % (fmt(r), fmt(bad[0]), SUB_PH[keys[0]]))
        its.append((1 if i < 5 else 2, pmcq(E("Subtract: {%s - %s}" % (B(a), B(b))), r, bad, E(e), rnd,
                                            "%s - %s" % (B(a), B(b)))))
    # C: word order
    rows = [("Subtract", P(1, 2, 0), P(3, -1, 4)), ("Subtract", P(2, -3, 5), P(0, 4, 1)),
            ("Take", P(-1, 0, 6), P(4, 5, 0))]
    for w, sub_, frm in rows:
        r = psub(frm, sub_)
        bad, keys = sub_wrongs(frm, sub_, order=("rev", "first", "none", "last"))
        if w == "Subtract":
            q = E("Subtract {%s} from {%s}." % (fmt(sub_), fmt(frm)))
        else:
            q = E("Take {%s} away from {%s}." % (fmt(sub_), fmt(frm)))
        e = (("“Subtract A from B”" if w == "Subtract" else "“Take A away from B”") + " means B " + M +
             " A. So work out {%s - %s}. " % (B(frm), B(sub_)) + steps(frm, pneg(sub_)) +
             " The answer is {%s}. ({%s} %s.)" % (fmt(r), fmt(bad[0]), SUB_PH[keys[0]]))
        its.append((3, pmcq(q, r, bad, E(e), rnd, "%s - %s" % (B(frm), B(sub_)))))
    # D: error analysis (forgetting to change all signs)
    a, b = P(5, 3, -4), P(2, -1, 6)
    wrote = m_first(a, b)
    assert fmt(wrote) == "3x^2 + 2x + 2"
    its.append((4, mcq(E("Ryan wrote {%s - %s} = {%s}. What mistake did he make?" % (B(a), B(b), fmt(wrote))),
                       "He changed only the sign of " + X("2x^2") + ".",
                       ["He subtracted in the wrong order.", "He joined unlike terms.", "He made no mistake."],
                       E("Every sign in the second polynomial must change: {-%s} = {%s}. Ryan kept {-x} and {+6}. "
                         "The correct answer is {%s}." % (B(b), fmt(pneg(b)), fmt(psub(a, b)))), rnd)))
    a, b = P(4, -2, 7), P(1, 3, -2)
    wrote = m_last(a, b)
    assert fmt(wrote) == "3x^2 - 5x + 5"
    its.append((4, mcq(E("Chloe wrote {%s - %s} = {%s}. Which part is wrong?" % (B(a), B(b), fmt(wrote))),
                       "The constant term", ["The " + X("x^2") + "-term", "The " + X("x") + "-term", "Nothing is wrong"],
                       E("{-%s} = {%s}, so the constants are 7 + 2 = 9, not 7 " % (B(b), fmt(pneg(b))) + M +
                         " 2 = 5. Chloe forgot to change the sign of the last term. The correct answer is {%s}." % fmt(psub(a, b))), rnd)))
    # E: what must be subtracted
    for a, target in ((P(4, 1, 3), P(1, 5, -2)), (P(-2, 6, 0), P(-5, 2, 4))):
        r = psub(a, target)
        assert psub(a, r) == target
        bad, keys = pick(r, [(psub(target, a), "rev"), (padd(a, target), "add"), (m_first(a, target), "first")])
        ph = {"rev": "subtracts in the wrong order", "add": "adds instead of subtracting",
              "first": "changes only the first sign"}
        e = ("{%s} " % B(a) + M + " ? = {%s}, so ? = {%s - %s}. " % (fmt(target), B(a), B(target)) +
             steps(a, pneg(target)) + " Check: {%s - %s} = {%s}. ({%s} %s.)" % (B(a), B(r), fmt(target), fmt(bad[0]), ph[keys[0]]))
        its.append((4, pmcq(E("What must be subtracted from {%s} to get {%s}?" % (fmt(a), fmt(target))), r, bad, E(e), rnd)))
    its.sort(key=lambda t: t[0])
    assert len(its) == 20, len(its)
    return {"title": "Subtract polynomials (change every sign)", "items": [i for _, i in its]}


# ============================================================ set 5: perimeter and word problems
def set_context(rnd):
    its = []
    rows = [
        (rect_svg("x^2 + 3x", "2x - 1", "rectangle with length x^2 + 3x and width 2x - 1"), "rectangle",
         "2(x^2 + 3x) + 2(2x - 1)", "2x^2 + 10x - 2", ["x^2 + 5x - 1", "2x^2 + 10x + 2", "2x^2 + 8x - 1"],
         "Add all four sides: {(x^2 + 3x) + (2x - 1) + (x^2 + 3x) + (2x - 1)}. {x^2}-terms: 1 + 1 = 2. "
         "{x}-terms: 3 + 2 + 3 + 2 = 10. Constants: " + M + "1 " + M + " 1 = " + M + "2. The perimeter is {2x^2 + 10x - 2}. "
         "({x^2 + 5x - 1} adds only two sides. {2x^2 + 8x - 1} adds only three sides.)"),
        (tri_svg("x + 4", "2x - 1", "x^2 + 2", "triangle with sides x + 4, 2x - 1 and x^2 + 2"), "triangle",
         "(x + 4) + (2x - 1) + (x^2 + 2)", "x^2 + 3x + 5", ["x^2 + 3x + 7", "4x^2 + 5", "x^2 + 2x + 5"],
         "{x^2}-terms: 1. {x}-terms: 1 + 2 = 3. Constants: 4 " + M + " 1 + 2 = 5. The perimeter is {x^2 + 3x + 5}. "
         "({x^2 + 3x + 7} ignores the minus sign of 1. {x^2 + 2x + 5} forgets that {x} is {1x}.)"),
        (rect_svg("3x - 2", "3x - 2", "square with sides 3x - 2", 100, 100), "square",
         "4(3x - 2)", "12x - 8", ["12x - 2", "6x - 4", "12x^4 - 8"],
         "A square has 4 equal sides: {(3x - 2) + (3x - 2) + (3x - 2) + (3x - 2)} = {12x - 8}. "
         "({12x - 2} subtracts the 2 only once. {6x - 4} adds only two sides.)"),
        (hex_svg("x^2 + 1", "regular hexagon with sides x^2 + 1"), "regular hexagon",
         "6(x^2 + 1)", "6x^2 + 6", ["6x^2 + 1", "x^2 + 6", "12x^2"],
         "A regular hexagon has 6 equal sides. Adding {x^2 + 1} six times gives {6x^2} and 6 × 1 = 6: {6x^2 + 6}. "
         "({6x^2 + 1} adds the 1 only once.)"),
        (rect_svg("2x^2 + x", "x^2 - 4", "rectangle with length 2x^2 + x and width x^2 - 4"), "rectangle",
         "2(2x^2 + x) + 2(x^2 - 4)", "6x^2 + 2x - 8", ["3x^2 + x - 4", "6x^2 + 2x + 8", "8x^2 - 8"],
         "{x^2}-terms: 2 + 1 + 2 + 1 = 6. {x}-terms: 1 + 1 = 2. Constants: " + M + "4 " + M + " 4 = " + M + "8. "
         "The perimeter is {6x^2 + 2x - 8}. ({3x^2 + x - 4} adds only two sides. {8x^2 - 8} joins unlike terms.)"),
        (trap_svg("x + 3", "3x + 1", "x^2", "2x - 5", "trapezoid with sides x + 3, 3x + 1, x^2 and 2x - 5"), "trapezoid",
         "(x + 3) + (3x + 1) + x^2 + (2x - 5)", "x^2 + 6x - 1", ["x^2 + 6x + 9", "7x^2 - 1", "x^2 + 5x - 1"],
         "{x^2}-terms: 1. {x}-terms: 1 + 3 + 2 = 6. Constants: 3 + 1 " + M + " 5 = " + M + "1. The perimeter is {x^2 + 6x - 1}. "
         "({x^2 + 6x + 9} ignores the minus sign of 5. {7x^2 - 1} joins unlike terms.)"),
        (tri_svg("x^2 + x", "x^2 + x", "3x - 2", "triangle with sides x^2 + x, x^2 + x and 3x - 2"), "triangle",
         "2(x^2 + x) + (3x - 2)", "2x^2 + 5x - 2", ["x^2 + 4x - 2", "2x^2 + 5x + 2", "7x^2 - 2"],
         "{x^2}-terms: 1 + 1 = 2. {x}-terms: 1 + 1 + 3 = 5. Constant: " + M + "2. The perimeter is {2x^2 + 5x - 2}. "
         "({x^2 + 4x - 2} adds the equal side only once.)"),
    ]
    for svg, word, src, good, bad, e in rows:
        its.append((0, emcq(fig(svg) + "Which expression gives the perimeter of the %s?" % word, good, bad, E(e), rnd, src)))
    assert ev("2x^2 + 10x - 2", x=4) == 70
    its.append((0, mcq(E("A rectangle has length ({x^2 + 3x}) m and width ({2x - 1}) m. Its perimeter is ({2x^2 + 10x - 2}) m. "
                         "What is the perimeter when {x} = 4?"), 70, [35, 74, 196],
                       E("2 × 4<sup>2</sup> + 10 × 4 " + M + " 2 = 32 + 40 " + M + " 2 = 70, so 70" + NBSP + "m. "
                         "(35" + NBSP + "m adds only two sides. 74 adds the 2. 196 is length × width, the area.)"),
                       rnd, lambda v: n(v) + NBSP + "m")))
    assert ev("x^2 + 3x", x=4) * ev("2x - 1", x=4) == 196 and ev("2x^2 + 10x + 2", x=4) == 74
    # missing sides
    rows = [
        (E("A rectangle has a perimeter of {4x^2 + 10x + 6}. Its length is {x^2 + 3x + 2}. Which expression gives its width?"),
         "x^2 + 2x + 1", ["3x^2 + 7x + 4", "x^2 + 8x + 5", "2x^2 + 4x + 2"],
         "Length + width is half the perimeter: {2x^2 + 5x + 3}. Width: {(2x^2 + 5x + 3) - (x^2 + 3x + 2)} = {x^2 + 2x + 1}. "
         "({3x^2 + 7x + 4} forgets to halve the perimeter.)", "(2x^2 + 5x + 3) - (x^2 + 3x + 2)"),
        (E("A triangle has a perimeter of {x^2 + 6x + 4}. Two sides are {2x + 5} and {x^2 + x - 3}. Which expression gives the third side?"),
         "3x + 2", ["5x - 4", "x^2 + 3x + 2", "3x - 4"],
         "The two sides add to {x^2 + 3x + 2}. Third side: {(x^2 + 6x + 4) - (x^2 + 3x + 2)} = {3x + 2}. "
         "({5x - 4} changes only the first sign of {x^2 + x - 3}.)", "(x^2 + 6x + 4) - (2x + 5) - (x^2 + x - 3)"),
        (E("A square has a perimeter of {8x + 12}. Which expression gives the length of one side?"),
         "2x + 3", ["4x + 6", "2x + 12", "8x + 8"],
         "A square has 4 equal sides, so divide each term by 4: 8{x} ÷ 4 = {2x} and 12 ÷ 4 = 3. Each side is {2x + 3}. "
         "({2x + 12} divides only the {x}-term. {4x + 6} divides by 2.)", "(8x + 12)/4"),
    ]
    assert same("(x^2 + 6x + 4) - (2x + 5) - x^2 + x - 3", "5x - 4")
    for q, good, bad, e, src in rows:
        its.append((1, emcq(q, good, bad, E(e), rnd, src)))
    # difference of perimeters
    a, b = P(6, 4, 2), P(2, 4, -6)
    r = psub(a, b)
    bad, keys = sub_wrongs(a, b, order=("last", "none", "rev"))
    its.append((2, pmcq(E("A community garden in Victoria has a perimeter of ({%s}) m. A smaller garden has a perimeter of ({%s}) m. "
                          "How much greater is the first perimeter?" % (fmt(a), fmt(b))), r, bad,
                        E("Subtract: {%s - %s} = {%s + %s}. " % (B(a), B(b), B(a), B(pneg(b))) + steps(a, pneg(b)) +
                          " The difference is ({%s}) m. ({%s} %s.)" % (fmt(r), fmt(bad[0]), SUB_PH[keys[0]])), rnd,
                        "%s - %s" % (B(a), B(b)))))
    its.append((2, emcq(E("The school soccer field has a perimeter of ({8x + 140}) m. The lacrosse box has a perimeter of ({6x + 60}) m. "
                          "How much longer is the soccer field perimeter?"), "2x + 80", ["2x + 200", "14x + 200", "-2x - 80"],
                        E("{(8x + 140) - (6x + 60)} = {8x - 6x + 140 - 60} = {2x + 80} metres. "
                          "({2x + 200} forgets to change the sign of 60.)"), rnd, "(8x + 140) - (6x + 60)")))
    # BC word problems
    its.append((3, emcq(E("A Grade 9 leadership class in Surrey sells hoodies. For {n} hoodies, they take in {35n} dollars, and the costs are "
                          "({20n + 150}) dollars. Which expression gives their profit?"),
                        "15n - 150", ["15n + 150", "55n + 150", "-15n + 150"],
                        E("Profit = money in " + M + " costs = {35n - (20n + 150)} = {35n - 20n - 150} = {15n - 150}. "
                          "({15n + 150} forgets to change the sign of 150. {-15n + 150} subtracts in the wrong order.)"),
                        rnd, "35n - (20n + 150)")))
    assert ev("15n - 150", n=40) == 450
    its.append((3, mcq(E("The class’s profit is ({15n - 150}) dollars for {n} hoodies. What is the profit if they sell 40 hoodies?"),
                       450, [750, 2350, -450],
                       E("15 × 40 = 600. Then 600 " + M + " 150 = 450, so the profit is $450.00. "
                         "($750.00 adds the 150. $2350.00 uses {55n + 150}, which adds the costs.)"), rnd, money)))
    a, b = P(2, 5, 3), P(1, 2, 0)
    r = psub(a, b)
    bad, keys = sub_wrongs(a, b, order=("first", "none", "rev"))
    its.append((3, pmcq(E("A backyard deck in Kelowna has an area of ({%s}) m<sup>2</sup>. A hot tub covers ({%s}) m<sup>2</sup> of it. "
                          "Which expression gives the area of the deck that is not covered?" % (fmt(a), fmt(b))), r, bad,
                        E("Subtract: {%s - %s} = {%s + %s}. " % (B(a), B(b), B(a), B(pneg(b))) + steps(a, pneg(b)) +
                          " The area is ({%s}) m<sup>2</sup>. ({%s} %s.)" % (fmt(r), fmt(bad[0]), SUB_PH[keys[0]])), rnd,
                        "%s - %s" % (B(a), B(b)))))
    a, b = P(1, 3, 0), P(2, -1, 6)
    r = padd(a, b)
    bad, keys = add_wrongs(a, b)
    its.append((4, pmcq(E("A school in Burnaby is putting new flooring in the library, with an area of ({%s}) m<sup>2</sup>, "
                          "and a classroom, with an area of ({%s}) m<sup>2</sup>. Which expression gives the total area?" % (fmt(a), fmt(b))),
                        r, bad, E(steps(a, b) + " The total area is ({%s}) m<sup>2</sup>. ({%s} %s.)"
                                  % (fmt(r), fmt(bad[0]), ADD_PH[keys[0]])), rnd, "%s + %s" % (B(a), B(b)))))
    its.append((4, emcq(E("For the food bank drive, Mr. Gill’s class collects ({5x + 12}) cans and Ms. Chen’s class collects ({3x - 4}) cans. "
                          "How many more cans does Mr. Gill’s class collect?"), "2x + 16", ["2x + 8", "8x + 8", "-2x - 16"],
                        E("{(5x + 12) - (3x - 4)} = {5x - 3x + 12 + 4} = {2x + 16}. Subtracting " + M + "4 adds 4. "
                          "({2x + 8} forgets to change the sign of " + M + "4. {8x + 8} adds the two amounts.)"),
                        rnd, "(5x + 12) - (3x - 4)")))
    its.append((4, emcq(E("At a Terry Fox Run, a school raises ({6x + 25}) dollars on Monday, ({4x - 10}) dollars on Tuesday and "
                          "({x + 40}) dollars on Wednesday. Which expression gives the total?"), "11x + 55", ["11x + 75", "10x + 55", "66x"],
                        E("{x}-terms: 6 + 4 + 1 = 11. Constants: 25 " + M + " 10 + 40 = 55. The total is ({11x + 55}) dollars. "
                          "({11x + 75} ignores the minus sign of 10. {10x + 55} forgets that {x} is {1x}.)"),
                        rnd, "(6x + 25) + (4x - 10) + (x + 40)")))
    its.append((4, emcq(E("Mateo drives the Sea-to-Sky Highway. From Vancouver to Squamish is ({3x + 5}) km and from Squamish to Whistler is "
                          "({3x - 2}) km. How much farther is the first part of the trip?"), "7", ["6x + 3", "6x + 7", "3"],
                        E("{(3x + 5) - (3x - 2)} = {3x - 3x + 5 + 2} = 7. The {x}-terms cancel, so the first part is 7" + NBSP + "km longer. "
                          "(3 forgets to change the sign of " + M + "2. {6x + 3} adds the two parts.)"),
                        rnd, "(3x + 5) - (3x - 2)")))
    its.sort(key=lambda t: t[0])
    assert len(its) == 20, len(its)
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
    t0 = tiles_svg(["X -X x -x 1 -1"], (), "algebra tiles: an x-squared tile, an x-tile and a 1-tile, and their negatives")
    a, b = P(2, -1, 3), P(1, 3, -1)
    t1 = tiles_svg([ptiles(a), ptiles(b)], "+", "algebra tiles: 2x^2 - x + 3 plus x^2 + 3x - 1")
    r1 = rect_svg("x^2 + 3x", "2x - 1", "rectangle with length x^2 + 3x and width 2x - 1")
    a2, b2 = P(5, 3, -4), P(2, -1, 6)
    return E(
        "<h2>Terms, degree and like terms</h2>"
        "<p>A <b>polynomial</b> is a sum of terms such as {3x^2 - 2x + 5}. Each sign belongs to the term after it, so the terms are "
        "{3x^2}, {-2x} and 5. One term is a <b>monomial</b>, two terms a <b>binomial</b> and three terms a <b>trinomial</b>.</p>"
        "<p>The <b>degree</b> is the greatest exponent: {3x^2 - 2x + 5} has degree 2. <b>Like terms</b> have the same variable "
        "with the same exponent, such as {4x^2} and {-x^2}. Only like terms can be combined.</p>" +
        table(["Expression", "Add the coefficients", "Result"], [
            ["{3x + 5x}", "3 + 5 = 8", "{8x}"],
            ["{4x^2 - x^2}", "4 " + M + " 1 = 3", "{3x^2}"],
            ["{3x^2 + 2x}", "not like terms", "{3x^2 + 2x}"],
        ]) +
        "<h2>Algebra tiles</h2>"
        "<figure class='sn-fig'>" + t0 +
        "<figcaption>The large square is {x^2}, the long tile is {x} and the small square is 1. Red tiles are negative. "
        "A tile and its red partner make a <b>zero pair</b>.</figcaption></figure>"
        "<h2>Add polynomials</h2>"
        "<p>Remove the brackets, group like terms, and add the coefficients. The exponents do not change.</p>"
        "<figure class='sn-fig'>" + t1 +
        "<figcaption>{(2x^2 - x + 3) + (x^2 + 3x - 1)}: 3 blue tiles, 1 red and 3 green {x}-tiles leave 2 green, "
        "and 3 yellow with 1 red 1-tile leave 2. The sum is {3x^2 + 2x + 2}.</figcaption></figure>" +
        ex("Example 1", "Add {(4 + 3x - x^2) + (2x^2 - 5 + x)}.",
           "Match like terms even when the order is different. {x^2}-terms: " + M + "1 + 2 = 1. {x}-terms: 3 + 1 = 4. "
           "Constants: 4 + (" + M + "5) = " + M + "1.", "{x^2 + 4x - 1}") +
        "<h2>Subtract polynomials</h2>"
        "<p>To subtract, add the opposite: change the sign of <b>every</b> term in the second polynomial, then add.</p>" +
        ex("Example 2", "Subtract {%s - %s}." % (B(a2), B(b2)),
           "{%s - %s} = {%s + %s}. " % (B(a2), B(b2), B(a2), B(pneg(b2))) + steps(a2, pneg(b2)),
           "{%s}" % fmt(psub(a2, b2))) +
        "<h2>Perimeter</h2>"
        "<figure class='sn-fig'>" + r1 +
        "<figcaption>Add all four sides: {(x^2 + 3x) + (2x - 1) + (x^2 + 3x) + (2x - 1)} = {2x^2 + 10x - 2}.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["{x + x} = {x^2}", "{x + x} = {2x}. {x^2} means {x × x}"],
            ["{3x^2 + 2x} = {5x^2}", "{3x^2} and {2x} are not like terms, so they stay apart"],
            ["{(5x^2 + 3x - 4) - (2x^2 - x + 6)} = {3x^2 + 2x + 2}", "Change every sign: {-2x^2 + x - 6}, so the answer is {3x^2 + 4x - 10}"],
            ["“Subtract A from B” written as A " + M + " B", "It means B " + M + " A"],
            ["Adding only two sides for a perimeter", "Add every side of the shape"],
        ]))


FAQ = [
    {"q": "What do Grade 9 students learn about polynomials in the BC math curriculum?",
     "a": "The Mathematics 9 Patterning standard covers operations with polynomials of degree 2 or less. Students often start with algebra tiles, then add and subtract polynomials such as (2x² − x + 3) + (x² + 3x − 1) by combining like terms."},
    {"q": "How do you subtract polynomials?",
     "a": "Change the sign of every term in the second polynomial, then add like terms. For (5x² + 3x − 4) − (2x² − x + 6), write 5x² + 3x − 4 − 2x² + x − 6 = 3x² + 4x − 10."},
    {"q": "Why is x + x equal to 2x and not x²?",
     "a": "x + x means two x’s, so it is 2x. x² means x × x. When x = 3, x + x = 6 but x² = 9, so they are not the same."},
    {"q": "What is the degree of a polynomial?",
     "a": "It is the greatest exponent on the variable in any term. 5x² + 3x − 1 has degree 2, 7x − 4 has degree 1, and a constant such as −6 has degree 0."},
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
    rnd = random.Random(59803)
    sets = [set_terms(rnd), set_tiles(rnd), set_add(rnd), set_subtract(rnd), set_context(rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "adding-and-subtracting-polynomials", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Adding and Subtracting Polynomials",
        "seo_title": "Grade 9 Adding and Subtracting Polynomials Worksheets: Like Terms and Algebra Tiles (Free, Answer Key, BC Curriculum)",
        "short_title": "Adding and Subtracting Polynomials",
        "domain": "Patterning",
        "standard_code": "Grade 9: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Operations with polynomials, of degree less than or equal to 2",
        "meta_desc": "Free Grade 9 math worksheets on adding and subtracting polynomials for the BC curriculum: terms, degree and like terms, algebra tiles and zero pairs, adding polynomials, subtracting by changing every sign, and perimeter word problems. 100 questions with an answer key.",
        "key_big": "Combine only like terms, and keep the exponents: 3x² + 5x² = 8x², and x + x = 2x, not x².",
        "key_sub": "To subtract, change the sign of every term in the second polynomial, then add: (5x² + 3x − 4) − (2x² − x + 6) = 3x² + 4x − 10.",
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
