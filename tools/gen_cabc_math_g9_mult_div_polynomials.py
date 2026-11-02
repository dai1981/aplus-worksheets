# -*- coding: utf-8 -*-
"""
British Columbia Grade 9 Math: Multiplying and Dividing Polynomials by a Monomial
(BC Mathematics Curriculum, Mathematics 9 — Patterning: operations with polynomials, of degree less than or equal to 2)
  python3 tools/gen_cabc_math_g9_mult_div_polynomials.py
Monomial × monomial ((2x)(3x) = 6x²), monomial × binomial with the distributive property (3(x + 4) = 3x + 12,
−2x(x − 5) = −2x² + 10x), area models (find the area, a missing cell, the side or the binomial), dividing a polynomial
by a monomial ((6x² + 9x) ÷ 3x = 2x + 3), and area word problems in BC contexts.
Wrong answers come from real student mistakes: 3(x + 4) = 3x + 4 (multiplying only the first term), 2x × 3x = 6x
(forgetting x × x = x²), adding coefficients instead of multiplying, sign errors with negative monomials, dividing only
the first term, 7x ÷ 7x = 0 instead of 1, perimeter instead of area, forgetting the 1/2 in a triangle's area.
Every answer is checked in code with fractions.Fraction (expressions are compared at several values).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
ASK = "#fff1b8"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """BC style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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
    """Plain expression '-3x(x + 4)' -> HTML: letters in italics, ^2 as a superscript, real minus sign."""
    s = s.replace("-", M).replace("*", "×").replace("/", "÷")
    s = re.sub(r"[a-z]", lambda m: "<i>%s</i>" % m.group(), s)
    return re.sub(r"\^(\d)", r"<sup>\1</sup>", s)


def E(s):
    """Text with expressions in braces: 'Expand {3(x + 4)}' -> the braces become X(...)."""
    return re.sub(r"\{([^{}]*)\}", lambda m: X(m.group(1)), s.replace(" - ", " " + M + " "))


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
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2), -5):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


def D(num, den):
    """A division written as a fraction bar (HTML)."""
    return fr(X(num), X(den))


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
    """Expression choices (plain text). good must equal src (when given); no two choices may be equivalent."""
    if src is not None:
        assert same(good, src), (src, good)
    allc = [good] + list(bad)
    for i in range(4):
        for j in range(i + 1, 4):
            assert not same(allc[i], allc[j]), (q, allc[i], allc[j])
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
    """Expression inside an SVG text: letters in italics with a tspan, ^2 as ², real minus sign."""
    s = s.replace("^2", "²").replace("-", M)
    return re.sub(r"[a-z]", lambda m: "<tspan font-style='italic'>%s</tspan>" % m.group(), s)


def tw(s, fs=17):
    """Rough width of an SVG label (bold Arial)."""
    s = s.replace("^2", "²")
    return sum(0.62 * fs if ch not in " ²" else 0.35 * fs for ch in s)


def area_svg(side, tops, cells, label):
    """Area model: one row (side label on the left), one column per top label. '?' cells are shaded yellow."""
    fs = 17
    L = max(tw(side), 14) + 16
    T = 32
    H = 76
    ws = [max(84, tw(t) + 30, tw(c) + 30) for t, c in zip(tops, cells)]
    s = []
    x = L
    for t, c, w in zip(tops, cells, ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, T, w, H, ASK if c == "?" else FILL, GREEN))
        s.append(text(x + w / 2, T - 10, SX(t), fs))
        if c:
            s.append(text(x + w / 2, T + H / 2 + 6, SX(c), fs))
        x += w
    s.append(text(L - 8, T + H / 2 + 6, SX(side), fs, "end"))
    return svg_wrap(x + 6, T + H + 6, "".join(s), label)


def rect_svg(top, side, label, inside="", w=190, h=84):
    L = max(tw(side), 14) + 16
    T = 30
    s = ["<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, SX(top), 17))
    s.append(text(L - 8, T + h / 2 + 6, SX(side), 17, "end"))
    if inside:
        s.append(text(L + w / 2, T + h / 2 + 6, inside, 16))
    return svg_wrap(L + w + 8, T + h + 8, "".join(s), label)


def tri_svg(base, height, label):
    """Triangle with the base labelled below and a dashed height from the apex."""
    P = [(20, 120), (240, 120), (90, 16)]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (
        " ".join("%d,%d" % p for p in P), FILL, GREEN)]
    s.append("<line x1='90' y1='16' x2='90' y2='120' stroke='%s' stroke-width='2' stroke-dasharray='6 4'/>" % INK)
    s.append("<rect x='90' y='108' width='12' height='12' fill='none' stroke='%s' stroke-width='1.5'/>" % INK)
    s.append(text(98, 70, SX(height), 17, "start"))
    s.append(text(130, 143, SX(base), 17))
    return svg_wrap(250, 152, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ============================================================ set 1: monomial × monomial
def set_monomials(rnd):
    its = []
    rows = [
        ("4 * 5x", "20x", ["9x", "20x^2", "20"],
         "Multiply the numbers and keep the variable: 4 × 5 = 20, so {4 * 5x} = {20x}. (9{x} adds 4 and 5.)"),
        ("-3 * 6x", "-18x", ["18x", "3x", "-18"],
         M + "3 × 6 = " + M + "18, so the answer is {-18x}. (3{x} adds " + M + "3 and 6. " + M + "18 drops the variable.)"),
        ("(-2)(-7y)", "14y", ["-14y", "-9y", "14"],
         "A negative times a negative is positive: (" + M + "2)(" + M + "7) = 14, so the answer is {14y}. (" + M + "9{y} adds the numbers.)"),
        ("x * x", "x^2", ["2x", "x", "2x^2"],
         "{x * x} means {x} times itself, which is {x^2}. (2{x} is {x + x}, which is adding, not multiplying.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((0, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("(2x)(3x)", "6x^2", ["6x", "5x^2", "5x"],
         "Multiply the coefficients: 2 × 3 = 6. Multiply the variables: {x * x} = {x^2}. So {(2x)(3x)} = {6x^2}. "
         "(6{x} forgets that {x * x} = {x^2}. 5{x}<sup>2</sup> adds 2 and 3.)"),
        ("(4x)(5x)", "20x^2", ["20x", "9x^2", "9x"],
         "4 × 5 = 20 and {x * x} = {x^2}, so the answer is {20x^2}. (20{x} forgets the second {x}. 9{x}<sup>2</sup> adds 4 and 5.)"),
        ("(-3x)(2x)", "-6x^2", ["6x^2", "-6x", "-x^2"],
         M + "3 × 2 = " + M + "6 and {x * x} = {x^2}, so the answer is {-6x^2}. (" + M + "{x}<sup>2</sup> adds " + M + "3 and 2.)"),
        ("(-5n)(-4n)", "20n^2", ["-20n^2", "20n", "-9n^2"],
         "(" + M + "5)(" + M + "4) = 20, because negative × negative is positive. {n * n} = {n^2}, so the answer is {20n^2}. "
         "(" + M + "20{n}<sup>2</sup> is a sign error.)"),
        ("(7x)(-x)", "-7x^2", ["7x^2", "-7x", "6x^2"],
         "{-x} means {-1x}. 7 × (" + M + "1) = " + M + "7 and {x * x} = {x^2}, so the answer is {-7x^2}. "
         "(6{x}<sup>2</sup> adds 7 and " + M + "1.)"),
        ("(-x)(-x)", "x^2", ["-x^2", "-2x", "2x"],
         "(" + M + "1)(" + M + "1) = 1 and {x * x} = {x^2}, so {(-x)(-x)} = {x^2}. (" + M + "{x}<sup>2</sup> is a sign error. "
         + M + "2{x} adds the terms.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((1, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("(0.5x)(8x)", "4x^2", ["4x", "8.5x^2", "16x^2"],
         "0.5 × 8 = 4 and {x * x} = {x^2}, so the answer is {4x^2}. (8.5{x}<sup>2</sup> adds. 16{x}<sup>2</sup> divides 8 by 0.5.)"),
        ("3(-4x^2)", "-12x^2", ["12x^2", "-12x", "-x^2"],
         "Multiply the coefficients: 3 × (" + M + "4) = " + M + "12. The {x^2} stays, so the answer is {-12x^2}. "
         "(" + M + "12{x} loses the square. " + M + "{x}<sup>2</sup> adds 3 and " + M + "4.)"),
        ("(2x)(-4)(x)", "-8x^2", ["-8x", "8x^2", "-2x^2"],
         "Numbers: 2 × (" + M + "4) = " + M + "8. Variables: {x * x} = {x^2}. The product is {-8x^2}. (" + M + "8{x} misses one {x}.)"),
        ("(3x)^2", "9x^2", ["3x^2", "6x^2", "9x"],
         "{(3x)^2} = {(3x)(3x)}: 3 × 3 = 9 and {x * x} = {x^2}, so {9x^2}. (3{x}<sup>2</sup> squares only the {x}. "
         "6{x}<sup>2</sup> doubles the 3.)"),
        ("(-2x)^2", "4x^2", ["-4x^2", "4x", "-2x^2"],
         "{(-2x)^2} = {(-2x)(-2x)}: (" + M + "2)(" + M + "2) = 4 and {x * x} = {x^2}, so {4x^2}. "
         "(" + M + "4{x}<sup>2</sup> forgets that negative × negative is positive.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((2, emcq(E("Simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    its.append((3, emcq(E("Which product is equal to {12x^2}?"), "(3x)(4x)", ["(3x)(4)", "(6x)(6x)", "(5x)(7x)"],
                        E("{(3x)(4x)}: 3 × 4 = 12 and {x * x} = {x^2}. ({(3x)(4)} = {12x}. {(6x)(6x)} = {36x^2}. "
                          "{(5x)(7x)} = {35x^2}: 5 + 7 = 12, but the coefficients must be multiplied.)"), rnd, "12x^2")))
    its.append((3, emcq(E("What monomial goes in the box? {4x} × ☐ = {20x^2}"), "5x", ["5", "16x", "5x^2"],
                        E("20 ÷ 4 = 5, and {x * x} = {x^2}, so the box needs {5x}. Check: {(4x)(5x)} = {20x^2}. "
                          "(5 gives only {20x}. 16{x} subtracts 4 from 20.)"), rnd, "(20x^2)/(4x)")))
    its.append((3, emcq(E("What monomial goes in the box? ☐ × {(-3x)} = {18x^2}"), "-6x", ["6x", "-6", "-6x^2"],
                        E("18 ÷ (" + M + "3) = " + M + "6, and {x * x} = {x^2}, so the box needs {-6x}. Check: "
                          "{(-6x)(-3x)} = {18x^2}. (6{x} gives " + M + "18{x}<sup>2</sup>.)"), rnd, "(18x^2)/(-3x)")))
    assert ev("(4x)(2x)", x=3) == 72 and ev("8x", x=3) == 24
    its.append((4, mcq(E("Owen says {(4x)(2x)} = {8x}. To test it, he uses {x} = 3. What is the value of {(4x)(2x)} when {x} = 3?"),
                       72, [24, 54, 18],
                       E("{4x} = 12 and {2x} = 6, so 12 × 6 = 72. But {8x} = 24, so Owen is wrong: the product is {8x^2} = 8 × 9 = 72. "
                         "(24 uses Owen’s {8x}. 54 uses {6x^2}.)"), rnd, n)))
    its.append((4, emcq(E("Simplify {(-5x)(2x) + 4x^2}."), "-6x^2", ["-14x^2", "6x^2", "-10x^2"],
                        E("Multiply first: {(-5x)(2x)} = {-10x^2}. Then combine like terms: {-10x^2 + 4x^2} = {-6x^2}. "
                          "(" + M + "10{x}<sup>2</sup> forgets the {4x^2}. " + M + "14{x}<sup>2</sup> subtracts 4.)"),
                        rnd, "(-5x)(2x) + 4x^2")))
    its.sort(key=lambda t: t[0])
    return {"title": "Multiply monomials", "items": [i for _, i in its]}


# ============================================================ set 2: monomial × binomial (distributive property)
def set_distribute(rnd):
    its = []
    rows = [
        ("3(x + 4)", "3x + 12", ["3x + 4", "3x + 7", "x + 12"],
         "Multiply both terms by 3: 3 × {x} = {3x} and 3 × 4 = 12. So {3(x + 4)} = {3x + 12}. "
         "(3{x} + 4 multiplies only the first term.)"),
        ("5(2x - 3)", "10x - 15", ["10x - 3", "10x + 15", "7x - 15"],
         "5 × {2x} = {10x} and 5 × (" + M + "3) = " + M + "15. So the answer is {10x - 15}. (10{x} " + M + " 3 multiplies only the first term.)"),
        ("-2(x + 6)", "-2x - 12", ["-2x + 6", "-2x + 12", "2x - 12"],
         M + "2 × {x} = {-2x} and " + M + "2 × 6 = " + M + "12. So the answer is {-2x - 12}. "
         "(" + M + "2{x} + 12 forgets that " + M + "2 × 6 is negative.)"),
        ("-4(3x - 5)", "-12x + 20", ["-12x - 20", "-12x - 5", "12x - 20"],
         M + "4 × {3x} = {-12x} and " + M + "4 × (" + M + "5) = 20. So the answer is {-12x + 20}. "
         "(" + M + "12{x} " + M + " 20 forgets that negative × negative is positive.)"),
        ("-(x - 7)", "-x + 7", ["-x - 7", "x + 7", "x - 7"],
         "{-(x - 7)} means " + M + "1 × {(x - 7)}: " + M + "1 × {x} = {-x} and " + M + "1 × (" + M + "7) = 7. So the answer is {-x + 7}. "
         "(" + M + "{x} " + M + " 7 changes the sign of the first term only.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((0, emcq(E("Expand {%s}." % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("x(x + 3)", "x^2 + 3x", ["x^2 + 3", "2x + 3", "4x^2"],
         "{x * x} = {x^2} and {x} × 3 = {3x}. So {x(x + 3)} = {x^2 + 3x}. ({x}<sup>2</sup> + 3 multiplies only the first term. "
         "4{x}<sup>2</sup> joins unlike terms.)"),
        ("2x(x - 5)", "2x^2 - 10x", ["2x^2 - 5", "2x^2 + 10x", "-8x^2"],
         "{2x * x} = {2x^2} and {2x} × (" + M + "5) = {-10x}. So the answer is {2x^2 - 10x}. "
         "(2{x}<sup>2</sup> " + M + " 5 multiplies only the first term.)"),
        ("3x(2x + 4)", "6x^2 + 12x", ["6x^2 + 4", "5x^2 + 7x", "18x^2"],
         "{3x * 2x} = {6x^2} and {3x} × 4 = {12x}. So the answer is {6x^2 + 12x}. (5{x}<sup>2</sup> + 7{x} adds instead of multiplying.)"),
        ("-x(x - 8)", "-x^2 + 8x", ["-x^2 - 8x", "x^2 - 8x", "-x^2 - 8"],
         "{-x * x} = {-x^2} and {-x} × (" + M + "8) = {8x}. So the answer is {-x^2 + 8x}. "
         "(" + M + "{x}<sup>2</sup> " + M + " 8{x} forgets that negative × negative is positive.)"),
        ("-3x(2x + 1)", "-6x^2 - 3x", ["-6x^2 + 1", "-6x^2 + 3x", "6x^2 + 3x"],
         "{-3x * 2x} = {-6x^2} and {-3x} × 1 = {-3x}. So the answer is {-6x^2 - 3x}. "
         "(" + M + "6{x}<sup>2</sup> + 1 multiplies only the first term.)"),
        ("4x(5 - x)", "20x - 4x^2", ["20x - x", "20x + 4x^2", "20 - 4x^2"],
         "{4x} × 5 = {20x} and {4x} × {(-x)} = {-4x^2}. So the answer is {20x - 4x^2}. "
         "(20{x} " + M + " {x} multiplies only the first term.)"),
        ("-5x(-2x + 3)", "10x^2 - 15x", ["-10x^2 - 15x", "10x^2 + 3", "10x^2 + 15x"],
         "{-5x * (-2x)} = {10x^2} and {-5x} × 3 = {-15x}. So the answer is {10x^2 - 15x}. "
         "(10{x}<sup>2</sup> + 15{x} gets the sign of the second term wrong.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((1, emcq(E("Expand {%s}." % s_), good, bad, E(e), rnd, s_)))
    rows = [
        ("2(x^2 - 3x + 4)", "2x^2 - 6x + 8", ["2x^2 - 3x + 4", "2x^2 - 6x + 4", "2x^2 + 6x + 8"],
         "Multiply all three terms by 2: {2x^2}, {-6x} and 8. The answer is {2x^2 - 6x + 8}. (2{x}<sup>2</sup> " + M +
         " 6{x} + 4 forgets the last term.)"),
        ("-3(2x^2 + x - 5)", "-6x^2 - 3x + 15", ["-6x^2 + x - 5", "-6x^2 - 3x - 15", "6x^2 + 3x - 15"],
         "Multiply all three terms by " + M + "3: {-6x^2}, {-3x} and +15. The answer is {-6x^2 - 3x + 15}. "
         "(" + M + "15 forgets that " + M + "3 × (" + M + "5) is positive.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((2, emcq(E("Expand {%s}." % s_), good, bad, E(e), rnd, s_)))
    its.append((2, emcq(E("Expand " + fr(1, 2) + "{(4x + 6)}."), "2x + 3", ["2x + 6", "8x + 12", "4x + 3"],
                        E("Multiplying by " + fr(1, 2) + " halves each term: {4x} ÷ 2 = {2x} and 6 ÷ 2 = 3. The answer is {2x + 3}. "
                          "(2{x} + 6 halves only the first term. 8{x} + 12 doubles instead.)"), rnd, "0.5(4x + 6)")))
    rows = [
        ("2(x + 3) + 4x", "6x + 6", ["6x + 3", "5x + 6", "12x"],
         "Expand first: {2(x + 3)} = {2x + 6}. Then {2x + 6 + 4x} = {6x + 6}. (6{x} + 3 forgets to multiply 3 by 2. "
         "12{x} joins unlike terms.)"),
        ("x(x + 5) - 2x", "x^2 + 3x", ["x^2 - 2x + 5", "x^2 + 7x", "4x^2"],
         "Expand first: {x(x + 5)} = {x^2 + 5x}. Then {5x - 2x} = {3x}, so the answer is {x^2 + 3x}. "
         "({x}<sup>2</sup> " + M + " 2{x} + 5 multiplies only the first term.)"),
        ("3(x - 2) - 2(x - 4)", "x + 2", ["x - 14", "x - 10", "x - 2"],
         "{3(x - 2)} = {3x - 6} and {-2(x - 4)} = {-2x + 8}. Then {3x - 2x} = {x} and " + M + "6 + 8 = 2. The answer is {x + 2}. "
         "({x} " + M + " 14 uses " + M + "2 × (" + M + "4) = " + M + "8.)"),
    ]
    for s_, good, bad, e in rows:
        its.append((3, emcq(E("Expand and simplify {%s}." % s_), good, bad, E(e), rnd, s_)))
    its.append((4, mcq(E("Ji-woo wrote {4(x + 5)} = {4x + 5}. What mistake did she make?"),
                       "She did not multiply 5 by 4.",
                       ["She should have added 4 and 5.", "She should not multiply " + X("x") + " by 4.", "She made no mistake."],
                       E("The 4 multiplies every term in the brackets: {4(x + 5)} = {4x + 20}. Ji-woo multiplied only the first term."),
                       rnd)))
    its.append((4, emcq(E("Expand {-2x(3 - x)}."), "-6x + 2x^2", ["-6x - 2x^2", "6x - 2x^2", "-6x + 2x"],
                        E("{-2x} × 3 = {-6x} and {-2x} × {(-x)} = {2x^2}. The answer is {-6x + 2x^2}, which can also be written "
                          "{2x^2 - 6x}. (" + M + "6{x} " + M + " 2{x}<sup>2</sup> forgets that negative × negative is positive.)"),
                        rnd, "-2x(3 - x)")))
    its.sort(key=lambda t: t[0])
    return {"title": "Multiply a monomial by a binomial", "items": [i for _, i in its]}


# ============================================================ set 3: area models
def area_q(side, tops, cells, ask):
    lab = "area model: side %s, top %s, cells %s" % (side, ", ".join(tops), ", ".join(c or "blank" for c in cells))
    lab = lab.replace("^2", " squared").replace("-", "minus ")
    return fig(area_svg(side, tops, cells, lab)) + ask


def set_area(rnd):
    its = []
    q = area_q("3", ["x", "2"], ["", ""], "Which multiplication does the area model show?")
    its.append((0, emcq(q, "3(x + 2)", ["3 + (x + 2)", "2(x + 3)", "3x + 2"],
                        E("The side is 3 and the top is {x} + 2, so the area is {3(x + 2)}. "
                          "(3{x} + 2 multiplies only the {x}. {2(x + 3)} swaps the 2 and the 3. {3 + (x + 2)} adds instead of multiplying.)"), rnd)))
    q = area_q("x", ["x", "5"], ["", ""], "Which expression gives the total area of the model?")
    its.append((0, emcq(q, "x(x + 5)", ["2x + 5", "5x", "x^2 + 5"],
                        E("Area = side × top = {x(x + 5)}, which expands to {x^2 + 5x}. ({x}<sup>2</sup> + 5 multiplies only the {x}.)"),
                        rnd)))
    rows = [
        ("2", ["x", "5"], "2x + 10", ["2x + 5", "2x + 7", "12x"],
         "The two cells are 2 × {x} = {2x} and 2 × 5 = 10. The total area is {2x + 10}. (2{x} + 5 forgets to multiply 5 by 2.)"),
        ("x", ["x", "4"], "x^2 + 4x", ["x^2 + 4", "2x + 4", "5x^2"],
         "The cells are {x * x} = {x^2} and {x} × 4 = {4x}. The total area is {x^2 + 4x}. (2{x} + 4 adds {x + x}.)"),
        ("2x", ["x", "3"], "2x^2 + 6x", ["2x^2 + 3", "3x^2 + 5x", "8x^2"],
         "The cells are {2x * x} = {2x^2} and {2x} × 3 = {6x}. The total area is {2x^2 + 6x}. "
         "(8{x}<sup>2</sup> joins unlike terms.)"),
        ("3x", ["2x", "1"], "6x^2 + 3x", ["6x^2 + 1", "6x + 3", "9x^2"],
         "The cells are {3x * 2x} = {6x^2} and {3x} × 1 = {3x}. The total area is {6x^2 + 3x}. "
         "(6{x}<sup>2</sup> + 1 multiplies only the first cell.)"),
    ]
    for side, tops, good, bad, e in rows:
        q = area_q(side, tops, ["", ""], "What is the total area of the model?")
        its.append((0, emcq(q, good, bad, E(e), rnd, "(%s)(%s + %s)" % (side, tops[0], tops[1]))))
    # missing cell
    rows = [
        ("4", ["x", "6"], ["4x", "?"], "24", ["10", "6", "24x"], "4 × 6",
         "The yellow cell is side × top: 4 × 6 = 24. (10 adds 4 and 6. 24{x} adds a variable that is not there.)"),
        ("2x", ["x", "7"], ["2x^2", "?"], "14x", ["9x", "14", "14x^2"], "2x * 7",
         "The yellow cell is {2x} × 7 = {14x}. (9{x} adds. 14 forgets the {x}.)"),
        ("x", ["3x", "-2"], ["?", "-2x"], "3x^2", ["3x", "4x", "3"], "x * 3x",
         "The yellow cell is {x * 3x} = {3x^2}. (3{x} forgets that {x * x} = {x^2}.)"),
        ("-2x", ["x", "5"], ["-2x^2", "?"], "-10x", ["10x", "3x", "-10x^2"], "-2x * 5",
         "The yellow cell is {-2x} × 5 = {-10x}. (10{x} loses the negative sign. 3{x} adds " + M + "2 and 5.)"),
        ("3", ["x^2", "-4x", "2"], ["3x^2", "?", "6"], "-12x", ["12x", "-x", "-12"], "3 * (-4x)",
         "The yellow cell is 3 × {(-4x)} = {-12x}. (12{x} loses the negative sign. " + M + "{x} adds 3 and " + M + "4.)"),
    ]
    for side, tops, cells, good, bad, src, e in rows:
        q = area_q(side, tops, cells, "What goes in the yellow cell of the area model?")
        its.append((1, emcq(q, good, bad, E(e), rnd, src)))
    # reverse: find the side
    rows = [
        ("?", ["x", "3"], ["4x^2", "12x"], "4x", ["4", "4x^2", "3x"], "(4x^2)/x",
         "The side times {x} gives {4x^2}, so the side is {4x}. Check: {4x} × 3 = {12x}. (4 would give only {4x} in the first cell.)"),
        ("?", ["x", "5"], ["2x", "10"], "2", ["2x", "5", "10x"], "(2x)/x",
         "The side times {x} gives {2x}, so the side is 2. Check: 2 × 5 = 10. (2{x} would give {2x^2} in the first cell.)"),
        ("?", ["x", "-6"], ["-3x^2", "18x"], "-3x", ["3x", "-3", "-3x^2"], "(-3x^2)/x",
         "The side times {x} gives {-3x^2}, so the side is {-3x}. Check: {-3x} × (" + M + "6) = {18x}. (3{x} gives the wrong signs.)"),
    ]
    for side, tops, cells, good, bad, src, e in rows:
        q = area_q(side, tops, cells, "What is the missing side length of the area model?")
        its.append((2, emcq(q, good, bad, E(e), rnd, src)))
    # reverse: find the binomial on top
    rows = [
        ("3x", ["?", "?"], ["6x^2", "15x"], "2x + 5", ["2x^2 + 5x", "6x + 15", "2x + 15"], "(6x^2 + 15x)/(3x)",
         "Divide each cell by the side {3x}: {6x^2} ÷ {3x} = {2x} and {15x} ÷ {3x} = 5. The top is {2x + 5}. "
         "(2{x} + 15 divides only the first cell.)"),
        ("5x", ["?", "?"], ["10x^2", "-20x"], "2x - 4", ["2x + 4", "2x^2 - 4x", "2x - 20"], "(10x^2 - 20x)/(5x)",
         "Divide each cell by {5x}: {10x^2} ÷ {5x} = {2x} and {-20x} ÷ {5x} = " + M + "4. The top is {2x - 4}. "
         "(2{x} + 4 loses the negative sign.)"),
    ]
    for side, tops, cells, good, bad, src, e in rows:
        q = area_q(side, tops, cells, "Which binomial is missing along the top of the area model?")
        its.append((2, emcq(q, good, bad, E(e), rnd, src)))
    # harder
    q = area_q("2", ["x^2", "3x", "-1"], ["", "", ""], "What is the total area of the model?")
    its.append((3, emcq(q, "2x^2 + 6x - 2", ["2x^2 + 3x - 1", "2x^2 + 6x - 1", "2x^2 + 6x + 2"],
                        E("Multiply each part by 2: {2x^2}, {6x} and " + M + "2. The total is {2x^2 + 6x - 2}. "
                          "(2{x}<sup>2</sup> + 6{x} " + M + " 1 forgets the last cell.)"), rnd, "2(x^2 + 3x - 1)")))
    q = area_q("-x", ["x", "4"], ["", ""], "What is the total area of the model?")
    its.append((3, emcq(q, "-x^2 - 4x", ["-x^2 + 4x", "x^2 + 4x", "-x^2 - 4"],
                        E("The cells are {-x * x} = {-x^2} and {-x} × 4 = {-4x}. The total is {-x^2 - 4x}. "
                          "(" + M + "{x}<sup>2</sup> " + M + " 4 forgets the {x} in the second cell.)"), rnd, "-x(x + 4)")))
    q = area_q("-3", ["x^2", "-2x", "5"], ["", "", ""], "What is the total area of the model?")
    its.append((3, emcq(q, "-3x^2 + 6x - 15", ["-3x^2 - 2x + 5", "-3x^2 - 6x - 15", "-3x^2 + 6x + 15"],
                        E("Multiply each part by " + M + "3: {-3x^2}, " + M + "3 × {(-2x)} = {6x} and " + M + "3 × 5 = " + M + "15. "
                          "The total is {-3x^2 + 6x - 15}. (" + M + "3{x}<sup>2</sup> " + M + " 6{x} " + M + " 15 forgets that "
                          "negative × negative is positive.)"), rnd, "-3(x^2 - 2x + 5)")))
    q = area_q("4x", ["x", "-3"], ["4x^2", "-12"],
               E("Arjun filled in this area model for {4x(x - 3)}. One cell is wrong. What should the second cell be?"))
    its.append((3, emcq(q, "-12x", ["12x", "-12", "-7x"],
                        E("The second cell is {4x} × (" + M + "3) = {-12x}. Arjun forgot to multiply by the {x} in {4x}. "
                          "(12{x} loses the negative sign.)"), rnd, "4x * (-3)")))
    its.sort(key=lambda t: t[0])
    return {"title": "Use area models", "items": [i for _, i in its]}


# ============================================================ set 4: divide a polynomial by a monomial
def set_divide(rnd):
    its = []
    rows = [
        ("12x^2", "3x", "4x", ["4x^2", "9x", "4"],
         "12 ÷ 3 = 4 and {x^2} ÷ {x} = {x}, so the quotient is {4x}. Check: {(3x)(4x)} = {12x^2}. "
         "(4{x}<sup>2</sup> forgets to divide the variable. 9{x} subtracts.)"),
        ("20x", "5", "4x", ["4", "15x", "100x"],
         "20 ÷ 5 = 4 and the {x} stays, so the quotient is {4x}. (4 drops the {x}. 100{x} multiplies.)"),
        ("15x", "5x", "3", ["3x", "10", "75x^2"],
         "15 ÷ 5 = 3 and {x} ÷ {x} = 1, so the quotient is 3. Check: {(5x)(3)} = {15x}. (3{x} forgets that {x} ÷ {x} = 1.)"),
        ("-18x^2", "6x", "-3x", ["3x", "-3x^2", "-12x"],
         M + "18 ÷ 6 = " + M + "3 and {x^2} ÷ {x} = {x}, so the quotient is {-3x}. (3{x} loses the negative sign.)"),
        ("-24x^2", "-8x", "3x", ["-3x", "3x^2", "-16x"],
         M + "24 ÷ (" + M + "8) = 3, because negative ÷ negative is positive. {x^2} ÷ {x} = {x}, so the quotient is {3x}."),
        ("7x^2", "7x", "x", ["1", "7x", "x^2"],
         "7 ÷ 7 = 1 and {x^2} ÷ {x} = {x}, so the quotient is {1x} = {x}. (1 cancels every {x}.)"),
    ]
    for i, (num, den, good, bad, e) in enumerate(rows):
        if i % 2:
            q = "Simplify " + D(num, den) + "."
        else:
            q = E("Simplify {%s} ÷ {%s}." % (num, den)) if not den.startswith("-") else E("Simplify {%s} ÷ {(%s)}." % (num, den))
        its.append((0, emcq(q, good, bad, E(e), rnd, "(%s)/(%s)" % (num, den))))
    rows = [
        ("8x + 12", "4", "2x + 3", ["2x + 12", "8x + 3", "5x"],
         "Divide each term by 4: {8x} ÷ 4 = {2x} and 12 ÷ 4 = 3. The quotient is {2x + 3}. (2{x} + 12 divides only the first term.)"),
        ("10x - 15", "5", "2x - 3", ["2x - 15", "2x + 3", "5x - 10"],
         "Divide each term by 5: {10x} ÷ 5 = {2x} and " + M + "15 ÷ 5 = " + M + "3. The quotient is {2x - 3}. "
         "(5{x} " + M + " 10 subtracts 5 instead of dividing.)"),
        ("6x^2 + 9x", "3x", "2x + 3", ["2x + 9", "2x^2 + 3x", "5x"],
         "Divide each term by {3x}: {6x^2} ÷ {3x} = {2x} and {9x} ÷ {3x} = 3. The quotient is {2x + 3}. "
         "(2{x} + 9 divides only the first term. 2{x}<sup>2</sup> + 3{x} divides only the numbers.)"),
        ("10x^2 - 15x", "5x", "2x - 3", ["2x - 15", "2x^2 - 3x", "2x + 3"],
         "{10x^2} ÷ {5x} = {2x} and {-15x} ÷ {5x} = " + M + "3. The quotient is {2x - 3}. Check: {5x(2x - 3)} = {10x^2 - 15x}."),
        ("14x^2 - 7x", "7x", "2x - 1", ["2x", "2x - 7", "2x^2 - x"],
         "{14x^2} ÷ {7x} = {2x} and {-7x} ÷ {7x} = " + M + "1. The quotient is {2x - 1}. "
         "(2{x} treats {7x} ÷ {7x} as 0, but any non-zero term divided by itself is 1.)"),
        ("-12x^2 + 8x", "4x", "-3x + 2", ["3x + 2", "-3x + 8", "-3x - 2"],
         "{-12x^2} ÷ {4x} = {-3x} and {8x} ÷ {4x} = 2. The quotient is {-3x + 2}. (" + M + "3{x} + 8 divides only the first term.)"),
        ("12x^2 - 8x", "-4x", "-3x + 2", ["-3x - 2", "3x - 2", "-3x^2 + 2x"],
         "Divide each term by {-4x}: {12x^2} ÷ {(-4x)} = {-3x} and {-8x} ÷ {(-4x)} = 2. The quotient is {-3x + 2}. "
         "(" + M + "3{x} " + M + " 2 forgets that negative ÷ negative is positive.)"),
        ("x^2 - 4x", "x", "x - 4", ["x^2 - 4", "x - 4x", "x + 4"],
         "{x^2} ÷ {x} = {x} and {-4x} ÷ {x} = " + M + "4. The quotient is {x - 4}. ({x} " + M + " 4{x} divides only the first term.)"),
    ]
    for i, (num, den, good, bad, e) in enumerate(rows):
        if i % 2 == 0:
            q = "Divide: " + D(num, den)
        else:
            q = E("Divide: {(%s)} ÷ {%s}" % (num, den)) if not den.startswith("-") else E("Divide: {(%s)} ÷ {(%s)}" % (num, den))
        its.append((1, emcq(q, good, bad, E(e), rnd, "(%s)/(%s)" % (num, den))))
    rows = [
        ("9x^2 + 6x - 3", "3", "3x^2 + 2x - 1", ["3x^2 + 6x - 3", "3x^2 + 2x - 3", "3x^2 + 2x"],
         "Divide all three terms by 3: {3x^2}, {2x} and " + M + "1. The quotient is {3x^2 + 2x - 1}. "
         "(3{x}<sup>2</sup> + 2{x} treats " + M + "3 ÷ 3 as 0.)"),
        ("4x^2 - 8x + 2", "2", "2x^2 - 4x + 1", ["2x^2 - 8x + 2", "2x^2 - 4x", "2x^2 - 4x + 2"],
         "Divide all three terms by 2: {2x^2}, {-4x} and 1. The quotient is {2x^2 - 4x + 1}. "
         "(2{x}<sup>2</sup> " + M + " 8{x} + 2 divides only the first term.)"),
        ("-6x^2 + 3x - 9", "-3", "2x^2 - x + 3", ["-2x^2 + x - 3", "2x^2 + x + 3", "2x^2 - x - 9"],
         "Divide all three terms by " + M + "3: {-6x^2} ÷ (" + M + "3) = {2x^2}, {3x} ÷ (" + M + "3) = {-x} and " + M +
         "9 ÷ (" + M + "3) = 3. The quotient is {2x^2 - x + 3}. (" + M + "2{x}<sup>2</sup> + {x} " + M + " 3 divides by +3.)"),
    ]
    for num, den, good, bad, e in rows:
        its.append((2, emcq("Divide: " + D(num, den), good, bad, E(e), rnd, "(%s)/(%s)" % (num, den))))
    its.append((3, emcq(E("What binomial goes in the box? {4x} × ☐ = {12x^2 - 20x}"), "3x - 5", ["3x - 20", "3x^2 - 5x", "3x + 5"],
                        E("Divide each term by {4x}: {12x^2} ÷ {4x} = {3x} and {-20x} ÷ {4x} = " + M + "5. The box is {3x - 5}. "
                          "Check: {4x(3x - 5)} = {12x^2 - 20x}."), rnd, "(12x^2 - 20x)/(4x)")))
    its.append((3, emcq(E("Simran says {(8x^2 + 4x)} ÷ {4x} = {2x}. She checks by multiplying {4x} by {2x} and gets only {8x^2}. "
                          "What is the correct quotient?"), "2x + 1", ["2x", "2x + 4", "2x^2 + x"],
                        E("{8x^2} ÷ {4x} = {2x} and {4x} ÷ {4x} = 1, so the quotient is {2x + 1}. Check: {4x(2x + 1)} = {8x^2 + 4x}. "
                          "Simran treated {4x} ÷ {4x} as 0."), rnd, "(8x^2 + 4x)/(4x)")))
    good = "(6x^2 - 8x) / 2x"
    bad = ["(6x^2 - 8x) / 2", "(6x^2 - 4x) / 2x", "(3x^2 - 4x) / 2x"]
    tgt = "3x - 4"
    assert same("(6x^2 - 8x)/(2x)", tgt)
    for b, chk in zip(bad, ["(6x^2 - 8x)/2", "(6x^2 - 4x)/(2x)", "(3x^2 - 4x)/(2x)"]):
        assert not same(chk, tgt)
    its.append((4, mcq(E("Which division has the quotient {3x - 4}?"), X(good), [X(b) for b in bad],
                       E("Check each one: {(6x^2 - 8x) / 2x} = {3x - 4}. {(6x^2 - 8x) / 2} = {3x^2 - 4x}. "
                         "{(6x^2 - 4x) / 2x} = {3x - 2}. {(3x^2 - 4x) / 2x} = 1.5{x} " + M + " 2."), rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Divide a polynomial by a monomial", "items": [i for _, i in its]}


# ============================================================ set 5: area word problems
def set_words(rnd):
    its = []
    m2 = lambda v: n(v) + NBSP + "m²"
    its.append((0, emcq(E("A school garden in Surrey is ({x + 6}) m long and 4 m wide. Which expression gives its area in square metres?"),
                        "4x + 24", ["4x + 6", "x + 24", "2x + 20"],
                        E("Area = length × width = {4(x + 6)} = {4x + 24}. (4{x} + 6 multiplies only the {x}. "
                          "2{x} + 20 is the perimeter, not the area.)"), rnd, "4(x + 6)")))
    q = (fig(rect_svg("x + 3", "x", "rectangle with length x + 3 and width x")) +
         "Olivia’s poster for the Terry Fox Run is a rectangle with these side lengths in centimetres. Which expression gives its area?")
    its.append((0, emcq(q, "x^2 + 3x", ["x^2 + 3", "2x + 3", "4x + 6"],
                        E("Area = {x(x + 3)} = {x^2 + 3x}. ({x}<sup>2</sup> + 3 multiplies only the {x}. 4{x} + 6 is the perimeter.)"),
                        rnd, "x(x + 3)")))
    its.append((0, emcq(E("A cedar deck in Kelowna is {2x} m wide and ({x + 5}) m long. Which expression gives its area in square metres?"),
                        "2x^2 + 10x", ["2x^2 + 5", "6x + 10", "2x^2 + 5x"],
                        E("Area = {2x(x + 5)} = {2x^2 + 10x}. (6{x} + 10 is the perimeter. 2{x}<sup>2</sup> + 5{x} forgets to "
                          "multiply 5 by 2.)"), rnd, "2x(x + 5)")))
    its.append((0, emcq(E("Ava’s vegetable bed in Nanaimo is ({x - 1}) m wide and 6 m long. Which expression gives its area in square metres?"),
                        "6x - 6", ["6x - 1", "2x + 10", "5x"],
                        E("Area = {6(x - 1)} = {6x - 6}. (6{x} " + M + " 1 multiplies only the {x}. 2{x} + 10 is the perimeter.)"),
                        rnd, "6(x - 1)")))
    its.append((0, emcq(E("A square patio has sides of {3x} m. Which expression gives its area in square metres?"),
                        "9x^2", ["3x^2", "6x^2", "12x"],
                        E("Area = {(3x)(3x)} = {9x^2}. (3{x}<sup>2</sup> squares only the {x}. 12{x} is the perimeter.)"), rnd, "(3x)^2")))
    its.append((0, emcq(E("An outdoor hockey rink in Kamloops is {5x} m long and ({2x + 2}) m wide. Which expression gives its area in square metres?"),
                        "10x^2 + 10x", ["10x^2 + 2", "14x + 4", "10x^2 + 2x"],
                        E("Area = {5x(2x + 2)} = {10x^2 + 10x}. (10{x}<sup>2</sup> + 2 multiplies only the first term. "
                          "14{x} + 4 is the perimeter.)"), rnd, "5x(2x + 2)")))
    q = (fig(tri_svg("4x", "x + 3", "triangle with base 4x and height x + 3")) +
         E("A triangular sail has a base of {4x} m and a height of ({x + 3}) m. Use A = " + fr(1, 2) + "{bh}. "
           "Which expression gives its area in square metres?"))
    its.append((0, emcq(q, "2x^2 + 6x", ["4x^2 + 12x", "2x^2 + 3", "2x^2 + 3x"],
                        E(fr(1, 2) + " × {4x} = {2x}. Then {2x(x + 3)} = {2x^2 + 6x}. (4{x}<sup>2</sup> + 12{x} forgets the " +
                          fr(1, 2) + ".)"), rnd, "0.5(4x)(x + 3)")))
    its.append((0, emcq(E("A parking area at a BC Ferries terminal is {2x} m wide and ({x + 8}) m long. Which expression gives its area in square metres?"),
                        "2x^2 + 16x", ["2x^2 + 8", "6x + 16", "2x^2 + 8x"],
                        E("Area = {2x(x + 8)} = {2x^2 + 16x}. (2{x}<sup>2</sup> + 8{x} multiplies 8 by {x} but not by 2. "
                          "6{x} + 16 is the perimeter.)"), rnd, "2x(x + 8)")))
    # evaluate
    assert ev("2x^2 + 10x", x=3) == 48
    its.append((1, mcq(E("The deck’s area is ({2x^2 + 10x}) m². What is the area when {x} = 3?"), 48, [66, 42, 31],
                       E("Square first: 3<sup>2</sup> = 9, so 2 × 9 = 18. Then 10 × 3 = 30, and 18 + 30 = 48. The deck is 6" + NBSP +
                         "m by 8" + NBSP + "m. (66 uses (2 × 3)<sup>2</sup>. 42 uses 2 × 3 × 2 for {2x^2}.)"), rnd, m2)))
    assert ev("10x^2 + 10x", x=12) == 1560
    its.append((1, mcq(E("The rink’s area is ({10x^2 + 10x}) m². What is the area when {x} = 12?"), 1560, [172, 1442, 14520],
                       E("10 × 12<sup>2</sup> = 10 × 144 = 1440 and 10 × 12 = 120, so the area is 1560" + NBSP + "m². "
                         "The rink is 60" + NBSP + "m by 26" + NBSP + "m. (172 is the perimeter. 1442 uses {10x^2 + 2}. 14" + NBSP + "520 squares 10 × 12.)"),
                       rnd, m2)))
    assert ev("8(x^2 + 6x)", x=5) == 440
    its.append((1, emcq(E("Sod for a lawn in Burnaby costs $8 per square metre. The lawn’s area is ({x^2 + 6x}) m². "
                          "Which expression gives the cost in dollars?"), "8x^2 + 48x", ["8x^2 + 6x", "x^2 + 48x", "8x^2 + 14x"],
                        E("Cost = 8 × area = {8(x^2 + 6x)} = {8x^2 + 48x}. (8{x}<sup>2</sup> + 6{x} multiplies only the first term.)"),
                        rnd, "8(x^2 + 6x)")))
    its.append((1, mcq(E("The sod costs ({8x^2 + 48x}) dollars. What is the cost when {x} = 5?"), 440, [230, 55, 365],
                       E("8 × 25 = 200 and 48 × 5 = 240, so the cost is $440.00. ($55.00 is only the area in square metres. "
                         "$230.00 uses {8x^2 + 6x}.)"), rnd, money)))
    # division
    its.append((2, emcq(E("A mural in Vancouver has an area of ({12x^2 + 18x}) m². Its height is {6x} m. Which expression gives its length in metres?"),
                        "2x + 3", ["2x + 18", "2x^2 + 3x", "6x^2 + 12x"],
                        E("Length = area ÷ height: {12x^2} ÷ {6x} = {2x} and {18x} ÷ {6x} = 3, so {2x + 3}. "
                          "Check: {6x(2x + 3)} = {12x^2 + 18x}. (2{x} + 18 divides only the first term. 6{x}<sup>2</sup> + 12{x} subtracts.)"),
                        rnd, "(12x^2 + 18x)/(6x)")))
    its.append((2, emcq(E("A plot at a community garden in Victoria has an area of ({5x^2 - 10x}) m². It is {5x} m long. Which expression gives its width in metres?"),
                        "x - 2", ["x - 10", "x^2 - 2x", "x + 2"],
                        E("Width = area ÷ length: {5x^2} ÷ {5x} = {x} and {-10x} ÷ {5x} = " + M + "2, so {x - 2}. "
                          "({x} " + M + " 10 divides only the first term.)"), rnd, "(5x^2 - 10x)/(5x)")))
    q = (fig(rect_svg("?", "3x", "rectangle with width 3x and area 6x squared plus 9x", "Area = " + SX("6x^2 + 9x"))) +
         "The rectangle has a width of " + X("3x") + " cm. What is its length?")
    its.append((2, emcq(q, "2x + 3", ["2x + 9", "2x^2 + 3x", "3x + 9"],
                        E("Length = area ÷ width: {6x^2} ÷ {3x} = {2x} and {9x} ÷ {3x} = 3, so {2x + 3} cm. "
                          "(2{x} + 9 divides only the first term. 3{x} + 9 subtracts {3x} from {6x^2}.)"), rnd, "(6x^2 + 9x)/(3x)")))
    its.append((2, emcq(E("A triangular sign has an area of ({3x^2 + 6x}) cm² and a base of {2x} cm. Use A = " + fr(1, 2) +
                          "{bh}. Which expression gives its height in centimetres?"),
                        "3x + 6", ["1.5x + 3", "3x + 12", "6x^2 + 12x"],
                        E("Double the area to undo the " + fr(1, 2) + ": {6x^2 + 12x}. Then divide by the base {2x}: {3x + 6}. "
                          "Check: " + fr(1, 2) + " × {2x} × {(3x + 6)} = {3x^2 + 6x}. (1.5{x} + 3 forgets to double the area.)"),
                        rnd, "2(3x^2 + 6x)/(2x)")))
    # two steps
    its.append((3, emcq(E("A Grade 9 class in Whistler makes 2 rectangular banners for a ski race. Each banner is {3x} m long and "
                          "({x + 2}) m wide. Which expression gives the total area of the 2 banners in square metres?"),
                        "6x^2 + 12x", ["3x^2 + 6x", "6x^2 + 2", "6x^2 + 12"],
                        E("One banner: {3x(x + 2)} = {3x^2 + 6x}. Two banners: {2(3x^2 + 6x)} = {6x^2 + 12x}. "
                          "(3{x}<sup>2</sup> + 6{x} is only one banner. 6{x}<sup>2</sup> + 12 drops the {x} in {6x}.)"),
                        rnd, "2 * 3x(x + 2)")))
    its.append((3, emcq(E("Mei’s bedroom floor is ({x + 4}) m long and 3 m wide. A rug covers {2x} m² of it. "
                          "Which expression gives the area of floor that is not covered?"),
                        "x + 12", ["x + 4", "5x + 12", "3x + 10"],
                        E("Floor area: {3(x + 4)} = {3x + 12}. Subtract the rug: {3x + 12 - 2x} = {x + 12}. "
                          "({x} + 4 forgets to multiply 4 by 3. 5{x} + 12 adds the rug.)"), rnd, "3(x + 4) - 2x")))
    its.append((3, emcq(E("Two flower beds are in a park in Prince George. Bed A is {x} m by ({x + 5}) m. Bed B is {2x} m by 2 m. "
                          "How much greater is the area of Bed A, in square metres?"),
                        "x^2 + x", ["x^2 + 9x", "x^2 + 1", "x^2 + 5x"],
                        E("Bed A: {x(x + 5)} = {x^2 + 5x}. Bed B: {2x} × 2 = {4x}. Difference: {x^2 + 5x - 4x} = {x^2 + x}. "
                          "({x}<sup>2</sup> + 9{x} adds the areas.)"), rnd, "x(x + 5) - 4x")))
    its.append((3, emcq(E("Liam puts a square photo with sides of {4x} cm on a mat that is {4x} cm wide and ({4x + 3}) cm long. "
                          "Which expression gives the area of the mat that shows around the photo?"),
                        "12x", ["16x^2 + 12x", "12", "12x^2"],
                        E("Mat: {4x(4x + 3)} = {16x^2 + 12x}. Photo: {(4x)^2} = {16x^2}. Mat showing: {16x^2 + 12x - 16x^2} = {12x}. "
                          "(16{x}<sup>2</sup> + 12{x} forgets to subtract the photo.)"), rnd, "4x(4x + 3) - (4x)^2")))
    its.sort(key=lambda t: t[0])
    return {"title": "Area word problems", "items": [i for _, i in its]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    a1 = area_svg("2x", ["x", "3"], ["2x^2", "6x"], "area model: side 2x, top x and 3, cells 2x squared and 6x")
    a2 = area_svg("3x", ["2x", "5"], ["6x^2", "15x"], "area model: side 3x, top 2x and 5, cells 6x squared and 15x")
    return E(
        "<h2>Multiply monomials</h2>"
        "<p>To multiply monomials, multiply the coefficients, then multiply the variables. "
        "{x * x} = {x^2}, because {x^2} means {x} times itself. Use integer rules for the signs.</p>" +
        table(["Product", "Coefficients", "Variables", "Result"], [
            ["{(2x)(3x)}", "2 × 3 = 6", "{x * x} = {x^2}", "{6x^2}"],
            ["{(-5n)(-4n)}", "(" + M + "5)(" + M + "4) = 20", "{n * n} = {n^2}", "{20n^2}"],
            ["{4 * 5x}", "4 × 5 = 20", "{x}", "{20x}"],
        ]) +
        "<h2>Multiply a monomial by a binomial</h2>"
        "<p>Use the <b>distributive property</b>: multiply the monomial by <b>every</b> term in the brackets. "
        "An area model shows why: the side times each part of the top gives one cell, and the cells add up to the whole area.</p>"
        "<figure class='sn-fig'>" + a1 +
        "<figcaption>{2x(x + 3)}: the cells are {2x * x} = {2x^2} and {2x} × 3 = {6x}. "
        "So {2x(x + 3)} = {2x^2 + 6x}.</figcaption></figure>" +
        ex("Example 1", "Expand {-3x(2x - 5)}.",
           "{-3x * 2x} = {-6x^2}. {-3x} × (" + M + "5) = {15x}, because negative × negative is positive.", "{-6x^2 + 15x}") +
        "<h2>Divide a polynomial by a monomial</h2>"
        "<p>Divide <b>every</b> term by the monomial. Divide the coefficients, then the variables: {x^2} ÷ {x} = {x} and {x} ÷ {x} = 1. "
        "Check by multiplying the quotient by the monomial.</p>"
        "<figure class='sn-fig'>" + a2 +
        "<figcaption>{(6x^2 + 15x)} ÷ {3x}: divide each cell by the side {3x} to find the top, {2x + 5}.</figcaption></figure>" +
        ex("Example 2", "Divide: " + D("14x^2 - 7x", "7x"),
           "{14x^2} ÷ {7x} = {2x}. {-7x} ÷ {7x} = " + M + "1. Check: {7x(2x - 1)} = {14x^2 - 7x}.", "{2x - 1}") +
        "<h2>Area problems</h2>"
        "<p>The area of a rectangle is length × width, so a rectangle {2x} m wide and ({x + 5}) m long has an area of "
        "{2x(x + 5)} = {2x^2 + 10x} m². To find a missing side, divide the area by the side you know.</p>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["{3(x + 4)} = {3x + 4}", "Multiply every term: {3x + 12}"],
            ["{2x * 3x} = {6x}", "{x * x} = {x^2}, so {6x^2}"],
            ["{2x * 3x} = {5x^2}", "Multiply the coefficients, do not add them"],
            ["{-2(x - 5)} = {-2x - 10}", M + "2 × (" + M + "5) = +10, so {-2x + 10}"],
            ["{(6x^2 + 9x)} ÷ {3x} = {2x + 9}", "Divide every term: {2x + 3}"],
            ["{7x} ÷ {7x} = 0", "A non-zero term divided by itself is 1"],
            ["Using the perimeter for an area", "Area is length × width"],
        ]))


FAQ = [
    {"q": "Do BC Grade 9 students multiply and divide polynomials?",
     "a": "Yes. The Mathematics 9 Patterning standard covers operations with polynomials of degree 2 or less, which includes multiplying and dividing a polynomial by a monomial, such as 3x(2x − 5) = 6x² − 15x."},
    {"q": "Why is 2x × 3x equal to 6x² and not 6x?",
     "a": "Multiply the numbers (2 × 3 = 6) and the variables (x × x = x²). 6x would be correct only if one of the factors had no x."},
    {"q": "How do you use the distributive property with a monomial?",
     "a": "Multiply the monomial by every term in the brackets. For 3(x + 4), 3 × x = 3x and 3 × 4 = 12, so the answer is 3x + 12, not 3x + 4."},
    {"q": "How do you divide a polynomial by a monomial?",
     "a": "Divide each term by the monomial. For (6x² + 9x) ÷ 3x, 6x² ÷ 3x = 2x and 9x ÷ 3x = 3, so the quotient is 2x + 3. Multiply 3x(2x + 3) to check."},
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
    rnd = random.Random(59804)
    sets = [set_monomials(rnd), set_distribute(rnd), set_area(rnd), set_divide(rnd), set_words(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "multiplying-and-dividing-polynomials", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Multiplying and Dividing Polynomials by a Monomial",
        "seo_title": "Grade 9 Multiplying and Dividing Polynomials Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Multiplying and Dividing Polynomials",
        "domain": "Patterning",
        "standard_code": "Grade 9: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Operations with polynomials, of degree less than or equal to 2",
        "meta_desc": "Free Grade 9 math worksheets on multiplying and dividing polynomials for the BC curriculum: multiplying monomials, the distributive property, area models, dividing a polynomial by a monomial, and area word problems. 100 questions with an answer key.",
        "key_big": "Multiply or divide every term: 3(x + 4) = 3x + 12, and (6x² + 9x) ÷ 3x = 2x + 3.",
        "key_sub": "Multiply the coefficients and the variables: 2x × 3x = 6x², not 6x. Check a quotient by multiplying it back.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "area model")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
