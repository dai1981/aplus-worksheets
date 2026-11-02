# -*- coding: utf-8 -*-
"""
BC Grade 9 Math: Exponent laws (BC Mathematics Curriculum, Grade 9: Number —
"Exponents and exponent laws with whole-number exponents")
  python3 tools/gen_cabc_math_g9_exponent_laws.py
Powers with integer, fraction, decimal and variable bases; the product law (a³ × a⁴ = a⁷); the quotient law
(a⁷ ÷ a³ = a⁴); the power of a power, a product and a quotient ((a³)⁴ = a¹², (2x)³ = 8x³); the zero exponent
(a⁰ = 1) with mixed simplification; and word problems in BC contexts.
Expressions are written in a small text form ("3x^2y", "(-2)^4", "({2/3})^5") that is turned into HTML
(italic variables, <sup> exponents, real minus sign) AND evaluated exactly with fractions.Fraction, with the
variables set to awkward fractions. Every correct answer is checked against the question's own expression, and
no two choices are ever equal in value.
Wrong answers come from real student mistakes: multiplying exponents in the product law (a¹²), multiplying or
adding the bases (2³ × 2⁴ = 4⁷), dividing exponents in the quotient law, dividing the bases (1⁴), adding
exponents for a power of a power, raising the exponent ((a³)⁴ = a⁸¹), forgetting that a = a¹, raising only the
variable in (2x)³, a⁰ = 0 or a⁰ = a, −2⁴ = 16, and base × exponent (2⁵ = 10).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
BLUE, BFILL = "#1f5f8b", "#d6e6f2"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "
VARS = "abmnxy"
VAL = {"a": F(13, 4), "b": F(9, 7), "m": F(3, 5), "n": F(11, 6), "x": F(7, 3), "y": F(5, 11)}
SUPS = dict(zip("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"))


# ------------------------------------------------------------ expression text form
def n(v):
    """Whole number, BC style: 4 digits with no separator, 5+ digits with no-break spaces."""
    s = str(abs(v))
    if len(s) > 4:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return (M if v < 0 else "") + s


def frac_html(p, q):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (p, q)


def h(s):
    """Text form -> HTML. x -> <i>x</i>, ^5 -> <sup>5</sup>, {2/3} -> stacked fraction, * -> ×, / -> ÷, - -> −."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "{":
            j = s.index("}", i)
            p, q = s[i + 1:j].split("/")
            out.append(frac_html(h(p), h(q)))
            i = j + 1
        elif c == "^" and s[i + 1] == "(":
            j = s.index(")", i)
            out.append("<sup>%s</sup>" % h(s[i + 2:j]).replace(" + ", "+"))
            i = j + 1
        elif c == "^" and s[i + 1] in VARS:
            out.append("<sup><i>%s</i></sup>" % s[i + 1])
            i += 2
        elif c == "^":
            j = i + 1
            while j < len(s) and (s[j].isdigit() or s[j] == "☐"):
                j += 1
            assert j > i + 1, s
            out.append("<sup>%s</sup>" % s[i + 1:j])
            i = j
        elif c.isdigit():
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == "."):
                j += 1
            t = s[i:j]
            out.append(n(int(t)) if t.isdigit() else t)
            i = j
        elif c in VARS:
            out.append("<i>%s</i>" % c)
            i += 1
        elif c == "*":
            out.append(" × ")
            i += 1
        elif c == "/":
            out.append(" ÷ ")
            i += 1
        elif c == "-":
            out.append(M)
            i += 1
        elif c == "+":
            out.append(" + ")
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out).replace("( ", "(")


def ev(s):
    """Exact value of a text-form expression (variables are fixed fractions). None if it is not an expression."""
    if any(ch in s for ch in "<>=☐ ") or re.search(r"[^abmnxy\d.^*/+\-(){}]", s):
        return None
    t = re.sub(r"\{([^{}/]+)/([^{}]+)\}", r"((\1)/(\2))", s)
    t = re.sub(r"(?<=[\d)a-z])(?=[a-z(])", "*", t)
    t = t.replace("^", "**")
    t = re.sub(r"\d+(\.\d+)?", lambda m_: "F('%s')" % m_.group(0), t)
    return eval(t, {"F": F}, dict(VAL))


def T(s):
    """Explanation / question text: `...` segments are text-form expressions."""
    return re.sub(r"`([^`]+)`", lambda m_: h(m_.group(1)), s)


def ups(s):
    """Plain-text power: a^7 -> a⁷."""
    return re.sub(r"\^([\d+\-]+)", lambda m_: "".join(SUPS[c] for c in m_.group(1)), s).replace("-", M)


assert ev("2^3*2^4") == 128 and ev("-2^4") == -16 and ev("(-2)^4") == 16 and ev("4x^0") == 4
assert ev("({2/3})^3") == F(8, 27) and ev("0.5^2") == F(1, 4) and ev("(2x)^3") == 8 * VAL["x"] ** 3
assert ev("3a^2b") == 3 * VAL["a"] ** 2 * VAL["b"]
assert h("-15m^6") == "−15<i>m</i><sup>6</sup>"


def mcq(q, correct, wrong, e, check=None, distinct=True):
    """Choices are text-form expressions ("!" prefix = raw HTML). check: text form whose value must equal the
    correct choice. With distinct=True no two choices may be equal in value."""
    ch = [correct] + list(wrong)
    assert len(ch) == 4, (q, ch)
    html = [c[1:] if c.startswith("!") else h(c) for c in ch]
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in html)) == 4, (q, html)
    vals = [None if c.startswith("!") else ev(c) for c in ch]
    if check is not None:
        assert vals[0] is not None and ev(check) == vals[0], (q, check, correct)
    if distinct:
        known = [v for v in vals if v is not None]
        assert len(set(known)) == len(known), (q, ch, vals)
    return {"q": T(q), "c": html, "a": 0, "e": T(e)}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions (5 each per set)."""
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
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, hgt, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, hgt, w, hgt, label, FONT, body))


def stext(s):
    """Text form -> SVG text content: italic tspans for variables, Unicode superscripts, real minus sign."""
    def word(w):
        w = w.group(0)
        if all(c in VARS for c in w):
            return "".join("<tspan font-style='italic'>%s</tspan>" % c for c in w)
        return w
    s = re.sub(r"[A-Za-z]+", word, s.replace("-", M))
    parts = re.split(r"\^(\d+)", s)
    out = parts[0]
    for k in range(1, len(parts), 2):
        out += "<tspan dy='-7' font-size='14'>%s</tspan>" % parts[k]
        rest = parts[k + 1]
        out += "<tspan dy='7'>%s</tspan>" % rest if rest else "<tspan dy='7'> </tspan>"
    return out


def text(x, y, s, fs=16, anchor="middle", col=INK, bold=False, raw=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, s if raw else stext(s)))


def box(x, y, sz, lab, fill, col):
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='1.6'/>"
            % (x, y, sz, sz, fill, col) + text(x + sz / 2, y + sz / 2 + 6, lab, 17, col=INK))


def brace(x0, x1, y, lab, col, up=False):
    d = -7 if up else 7
    s = ("<path d='M%.1f %.1f v%d H%.1f v%d' fill='none' stroke='%s' stroke-width='1.6'/>"
         % (x0, y, d, x1, -d, col))
    return s + text((x0 + x1) / 2, y + (-12 if up else 26), lab, 16, col=col, bold=True)


def product_svg(b, m, k, answer=True):
    """b^m × b^k as two groups of factor boxes, with braces under each group and the total above."""
    sz, gap, sep = 32, 4, 30
    x0, y0 = 10, 40 if answer else 8
    s = []
    xs = []
    x = x0
    for i in range(m):
        s.append(box(x, y0, sz, b, FILL, GREEN))
        x += sz + gap
    g1 = (x0, x - gap)
    x += sep - gap
    s.append(text(x - sep / 2, y0 + sz / 2 + 6, "×", 20))
    gx = x
    for i in range(k):
        s.append(box(x, y0, sz, b, BFILL, BLUE))
        x += sz + gap
    g2 = (gx, x - gap)
    W = int(x - gap + x0)
    s.append(brace(g1[0], g1[1], y0 + sz + 5, "%s^%d" % (b, m), GREEN))
    s.append(brace(g2[0], g2[1], y0 + sz + 5, "%s^%d" % (b, k), BLUE))
    if answer:
        s.append(brace(g1[0], g2[1], y0 - 5, "%d factors of %s: %s^%d" % (m + k, b, b, m + k), INK, up=True))
    return svg_wrap(W, y0 + sz + 42, "".join(s),
                    "%d factors of %s times %d factors of %s makes %d factors" % (m, b, k, b, m + k))


def quotient_svg(b, m, k, answer=True):
    """b^m ÷ b^k as a fraction of factor boxes; k pairs are crossed out (each pair makes 1)."""
    sz, gap = 32, 4
    x0, y0 = 10, 8
    s = []
    for i in range(m):
        x = x0 + i * (sz + gap)
        s.append(box(x, y0, sz, b, FILL, GREEN))
        if i < k:
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4'/>"
                     % (x + 3, y0 + sz - 3, x + sz - 3, y0 + 3, RED))
    wtop = m * (sz + gap) - gap
    yb = y0 + sz + 8
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.4'/>" % (x0, yb, x0 + wtop, yb, INK))
    y1 = yb + 8
    for i in range(k):
        x = x0 + i * (sz + gap)
        s.append(box(x, y1, sz, b, BFILL, BLUE))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.4'/>"
                 % (x + 3, y1 + sz - 3, x + sz - 3, y1 + 3, RED))
    lx = x0 + wtop + 14
    if answer:
        s.append(text(lx, yb + 6, "= %s^%d" % (b, m - k), 20, anchor="start", bold=True))
        W = int(lx + 14 + 11 * (len(b) + 3) + 10)
    else:
        W = int(x0 + wtop + x0)
    return svg_wrap(W, y1 + sz + 8, "".join(s),
                    "%d factors of %s over %d factors of %s; %d pairs cancel, %d factors are left" % (m, b, k, b, k, m - k))


def square_svg(expr, unit):
    """Square plot with the side length labelled on two sides."""
    lab = stext(expr) + " " + unit
    sd, x0, y0 = 96, 12, 12
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x0, y0, sd, sd, FILL, GREEN)]
    s.append(text(x0 + sd / 2, y0 + sd + 22, lab, 16, raw=True))
    s.append(text(x0 + sd + 8, y0 + sd / 2 + 6, lab, 16, anchor="start", raw=True))
    W = int(x0 + sd + 8 + 9.5 * len(ups(expr) + unit) + 18)
    return svg_wrap(W, y0 + sd + 32, "".join(s), "square with side length %s %s" % (ups(expr), unit))


def rect_svg(ew, eh, unit):
    lw, lh = stext(ew) + " " + unit, stext(eh) + " " + unit
    w, ht, x0, y0 = 150, 70, 12, 12
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x0, y0, w, ht, FILL, GREEN)]
    s.append(text(x0 + w / 2, y0 + ht + 22, lw, 16, raw=True))
    s.append(text(x0 + w + 8, y0 + ht / 2 + 6, lh, 16, anchor="start", raw=True))
    W = int(x0 + w + 8 + 9.5 * len(ups(eh) + unit) + 18)
    return svg_wrap(W, y0 + ht + 32, "".join(s), "rectangle %s by %s %s" % (ups(ew), ups(eh), unit))


def cube_svg(expr, unit):
    """Cube drawn in oblique view, edges labelled."""
    lab = stext(expr) + " " + unit
    e, dx, dy = 80, 34, 26
    x0, y0 = 12, 12 + dy
    front = [(x0, y0), (x0 + e, y0), (x0 + e, y0 + e), (x0, y0 + e)]
    top = [(x0, y0), (x0 + dx, y0 - dy), (x0 + e + dx, y0 - dy), (x0 + e, y0)]
    side = [(x0 + e, y0), (x0 + e + dx, y0 - dy), (x0 + e + dx, y0 + e - dy), (x0 + e, y0 + e)]
    s = []
    for pts, f in [(front, FILL), (top, "#e6f2e9"), (side, "#a9d3b6")]:
        s.append("<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.8' stroke-linejoin='round'/>"
                 % (" ".join("%d,%d" % p for p in pts), f, GREEN))
    s.append(text(x0 + e / 2, y0 + e + 22, lab, 16, raw=True))
    s.append(text(x0 + e + dx + 8, y0 + e / 2 - dy / 2 + 6, lab, 16, anchor="start", raw=True))
    W = int(x0 + e + dx + 8 + 9.5 * len(ups(expr) + unit) + 18)
    return svg_wrap(W, y0 + e + 32, "".join(s), "cube with edge length %s %s" % (ups(expr), unit))


def doubling_svg(rows=4):
    """Cells that double every hour: 1, 2, 4, 8 (= 2⁰, 2¹, 2², 2³)."""
    r, gap, rowh = 8, 22, 28
    s = []
    for k in range(rows):
        y = 18 + k * rowh
        s.append(text(46, y + 5, "%d h" % k, 15, anchor="end"))
        for j in range(2 ** k):
            s.append("<circle cx='%.1f' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                     % (62 + r + j * gap, y, r, FILL, GREEN))
        s.append(text(62 + 2 * r + (2 ** (rows - 1) - 1) * gap + 14, y + 5, "2^%d = %d" % (k, 2 ** k), 15,
                      anchor="start", col=GREEN))
    W = 62 + 2 * r + (2 ** (rows - 1) - 1) * gap + 14 + 80
    return svg_wrap(W, 18 + (rows - 1) * rowh + 16, "".join(s), "cells that double every hour: 1, 2, 4, 8")


# ============================================================ set 1: powers, bases and exponents
def set_powers():
    its = []
    its.append(mcq("In `7^4`, which number is the base?", "7", ["4", "28", "2401"],
                   "The base is the number that is multiplied: 7. The small raised 4 is the exponent. "
                   "`7^4 = 7*7*7*7 = 2401` is the value of the power."))
    its.append(mcq("Which power means `5*5*5*5`?", "5^4", ["4^5", "5^3", "5*4"],
                   "5 is used as a factor 4 times, so the base is 5 and the exponent is 4: `5^4`. "
                   "Count the factors (4), not the × signs (3).", check="5*5*5*5"))
    its.append(mcq("Evaluate `2^6`.", "64", ["12", "36", "32"],
                   "`2^6 = 2*2*2*2*2*2`: 2, 4, 8, 16, 32, 64. Not 12: that is 2 × 6. Not 36: that is `6^2`.",
                   check="2^6"))
    its.append(mcq("Evaluate `3^4`.", "81", ["12", "64", "27"],
                   "`3^4 = 3*3*3*3 = 81`. Not 12: that is 3 × 4. Not 64: that is `4^3`. Not 27: that uses only three 3s.",
                   check="3^4"))
    its.append(mcq("Write `x*x*x*x*x` as a power.", "x^5", ["5x", "x^4", "x+5"],
                   "<i>x</i> is used as a factor 5 times: `x^5`. `5x` means `x+x+x+x+x`, which is repeated addition, "
                   "not repeated multiplication.", check="x*x*x*x*x"))
    its.append(mcq("Which means the same as `a^3`?", "a*a*a", ["3a", "a*a", "3*3*3"],
                   "The exponent 3 tells you to use the base <i>a</i> as a factor 3 times: `a^3 = a*a*a`. "
                   "It is not `3a`, which is `3*a`."))
    its.append(mcq("Evaluate `10^5`.", "100000", ["50", "10000", "1000000"],
                   "`10^5` is a 1 followed by 5 zeros: 100 000. Not 50: that is 10 × 5.", check="10^5"))
    its.append(mcq("Evaluate `(-2)^4`.", "16", ["-16", "-8", "8"],
                   "The brackets make −2 the base: `(-2)*(-2)*(-2)*(-2) = 16`. An even number of negative "
                   "factors gives a positive answer.", check="(-2)^4"))
    its.append(mcq("Evaluate `-2^4`.", "-16", ["16", "-8", "8"],
                   "With no brackets the base is 2, not −2: `-2^4 = -(2*2*2*2) = -16`. Compare `(-2)^4 = 16`.",
                   check="-2^4"))
    its.append(mcq("Evaluate `(-3)^3`.", "-27", ["27", "-9", "9"],
                   "`(-3)*(-3)*(-3)`: (−3) × (−3) = 9, then 9 × (−3) = −27. An odd number of negative factors gives "
                   "a negative answer. Not −9: that is (−3) × 3.", check="(-3)^3"))
    its.append(mcq("Evaluate `(-1)^8`.", "1", ["-1", "-8", "8"],
                   "Eight factors of −1: every pair multiplies to 1, so `(-1)^8 = 1`. "
                   "Not −8: that is (−1) × 8.", check="(-1)^8"))
    its.append(mcq("Which power has a negative value?", "(-5)^3", ["(-5)^2", "(-5)^4", "5^3"],
                   "`(-5)^3 = -125` has an odd number of negative factors. `(-5)^2 = 25` and `(-5)^4 = 625` have an "
                   "even number, and `5^3 = 125` has no negative factors."))
    its.append(mcq("Which power means `(-6)*(-6)*(-6)`?", "(-6)^3", ["6^3", "(-3)^6", "-6*3"],
                   "The factor −6 is used 3 times, so the base is −6 in brackets and the exponent is 3: `(-6)^3 = -216`. "
                   "`-6*3 = -18` is not repeated multiplication.", check="(-6)*(-6)*(-6)"))
    its.append(mcq("Evaluate `({2/3})^3`.", "{8/27}", ["{8/3}", "{2/27}", "{6/9}"],
                   "Cube the numerator and the denominator: `{2/3}*{2/3}*{2/3} = {8/27}`. "
                   "Not `{6/9}`: that multiplies by 3 instead of cubing. Not `{8/3}`: cube the denominator too.",
                   check="({2/3})^3"))
    its.append(mcq("Evaluate `0.5^2`.", "0.25", ["1", "2.5", "0.025"],
                   "`0.5^2 = 0.5*0.5 = 0.25`. Not 1: that is 0.5 × 2. Count the decimal places: 1 + 1 = 2 places.",
                   check="0.5^2"))
    its.append(mcq("Evaluate `(-0.3)^2`.", "0.09", ["-0.09", "0.9", "-0.6"],
                   "`(-0.3)*(-0.3) = 0.09`. Two negative factors give a positive answer, and 3 × 3 = 9 with 2 decimal "
                   "places. Not −0.6: that is (−0.3) × 2.", check="(-0.3)^2"))
    its.append(mcq("Compare `2^5` and `5^2`.", "!2<sup>5</sup> &gt; 5<sup>2</sup>",
                   ["!2<sup>5</sup> &lt; 5<sup>2</sup>", "!2<sup>5</sup> = 5<sup>2</sup>", "!You can’t tell"],
                   "`2^5 = 32` and `5^2 = 25`, so `2^5` is greater. Swapping the base and the exponent changes the value."))
    its.append(mcq("Evaluate `3*2^4`.", "48", ["1296", "24", "96"],
                   "Powers come before multiplication: `2^4 = 16`, then 3 × 16 = 48. Not 1296: that is `(3*2)^4`. "
                   "Not 24: that is 3 × 2 × 4. Not 96: that uses `2^5 = 32`.", check="3*2^4"))
    its.append(mcq("Evaluate `x^3` when <i>x</i> = −2.", "-8", ["8", "-6", "6"],
                   "`(-2)^3 = (-2)*(-2)*(-2) = -8`. Put a negative value in brackets before you raise it to a power. "
                   "Not −6: that is (−2) × 3.", check="(-2)^3"))
    its.append(mcq("Evaluate `2a^2` when <i>a</i> = 3.", "18", ["36", "12", "11"],
                   "Only <i>a</i> is squared: `2*3^2 = 2*9 = 18`. Not 36: that is `(2*3)^2`. "
                   "Not 12: that is 2 × 3 × 2.", check="2*3^2"))
    order = [0, 1, 2, 3, 6, 4, 5, 7, 8, 16, 9, 10, 14, 11, 12, 15, 13, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Powers, bases and exponents", "items": its}


# ============================================================ set 2: product law
def set_product():
    its = []
    its.append(mcq(fig(product_svg("2", 3, 4, answer=False)) + "The picture shows `2^3*2^4` as factors. Which single power is it "
                   "equal to?", "2^7", ["2^12", "4^7", "2^6"],
                   "Count all the factors of 2: 3 + 4 = 7, so `2^3*2^4 = 2^7`. Keep the base. "
                   "Not `2^12`: do not multiply the exponents. Not `4^7`: do not multiply the bases.",
                   check="2^3*2^4"))
    its.append(mcq("Simplify `5^2*5^4`.", "5^6", ["5^8", "25^6", "10^6"],
                   "Same base, so add the exponents: 2 + 4 = 6. `5^2*5^4 = 5^6`. The base stays 5.", check="5^2*5^4"))
    its.append(mcq("Simplify `x^3*x^4`.", "x^7", ["x^12", "2x^7", "x^6"],
                   "`x^3*x^4 = (x*x*x)*(x*x*x*x) = x^7`. Add the exponents: 3 + 4 = 7. "
                   "Multiplying them (3 × 4 = 12) is the most common mistake.", check="x^3*x^4"))
    its.append(mcq("Simplify `a*a^5`.", "a^6", ["a^5", "2a^5", "a^7"],
                   "<i>a</i> on its own means `a^1`. So add 1 + 5 = 6: `a*a^5 = a^6`. "
                   "Not `a^5`: the <i>a</i> on its own still counts as one factor.",
                   check="a*a^5"))
    its.append(mcq("Simplify `3^4*3^5`.", "3^9", ["3^20", "9^9", "9^20"],
                   "Keep the base 3 and add the exponents: 4 + 5 = 9. `3^4*3^5 = 3^9`.", check="3^4*3^5"))
    its.append(mcq("Simplify `10^3*10^4`.", "10^7", ["10^12", "100^7", "10^1"],
                   "Add the exponents: 3 + 4 = 7. `10^3*10^4 = 1000*10000 = 10000000 = 10^7`.", check="10^3*10^4"))
    its.append(mcq("Simplify `(-2)^3*(-2)^2`.", "(-2)^5", ["(-2)^6", "4^5", "(-4)^5"],
                   "The base is −2 in both powers, so add the exponents: 3 + 2 = 5. `(-2)^5 = -32`.",
                   check="(-2)^3*(-2)^2"))
    its.append(mcq("Simplify `y^4*y^2*y^3`.", "y^9", ["y^24", "3y^9", "y^8"],
                   "Add all the exponents: 4 + 2 + 3 = 9. `y^4*y^2*y^3 = y^9`. Not `y^24`: that multiplies them.",
                   check="y^4*y^2*y^3"))
    its.append(mcq("`7^2*7^☐ = 7^8`. Which exponent goes in the box?", "6", ["4", "10", "16"],
                   "The exponents add: 2 + ☐ = 8, so ☐ = 6. Check: `7^2*7^6 = 7^8`. "
                   "Not 4: 2 × 4 = 8 multiplies the exponents."))
    its.append(mcq("Which product is equal to `2^10`?", "2^4*2^6", ["2^2*2^5", "2^8*2^3", "2^5+2^5"],
                   "4 + 6 = 10, so `2^4*2^6 = 2^10`. `2^2*2^5 = 2^7` (2 × 5 = 10 is the multiplying "
                   "mistake). `2^5+2^5 = 2*2^5 = 2^6`: adding powers is not the same as multiplying them.",
                   check="2^10"))
    its.append(mcq("Simplify `({1/2})^2*({1/2})^3`.", "({1/2})^5", ["({1/2})^6", "({1/4})^5", "({1/4})^6"],
                   "The base is `{1/2}` in both powers, so add the exponents: 2 + 3 = 5. `({1/2})^5 = {1/32}`.",
                   check="({1/2})^2*({1/2})^3"))
    its.append(mcq("Evaluate `2^3*3^2`.", "72", ["6^5", "6^6", "5^5"],
                   "The bases are different, so the product law does not apply. Evaluate each power: "
                   "`2^3 = 8` and `3^2 = 9`, then 8 × 9 = 72.", check="2^3*3^2"))
    its.append(mcq("Which is <b>not</b> equal to `x^8`?", "x^2*x^4", ["x^4*x^4", "x^2*x^6", "x*x^7"],
                   "Add the exponents in each product: 4 + 4 = 8, 2 + 6 = 8, 1 + 7 = 8, but 2 + 4 = 6. "
                   "So `x^2*x^4 = x^6`, not `x^8`. (2 × 4 = 8 is the multiplying mistake.)", distinct=False))
    its.append(mcq("Simplify `2x^3*4x^5`.", "8x^8", ["6x^8", "8x^15", "6x^15"],
                   "Multiply the coefficients and add the exponents: 2 × 4 = 8 and 3 + 5 = 8. So the answer is `8x^8`. "
                   "Not `6x^8`: do not add the coefficients.", check="2x^3*4x^5"))
    its.append(mcq("Simplify `-3m^2*5m^4`.", "-15m^6", ["15m^6", "2m^6", "-15m^8"],
                   "Coefficients: (−3) × 5 = −15. Exponents: 2 + 4 = 6. So the answer is `-15m^6`. "
                   "Not `-15m^8`: that multiplies the exponents.", check="-3m^2*5m^4"))
    its.append(mcq("`x^☐*x^4*x = x^10`. Which exponent goes in the box?", "5", ["6", "14", "10"],
                   "<i>x</i> means `x^1`, so ☐ + 4 + 1 = 10 and ☐ = 5. Not 6: that forgets the exponent 1 on <i>x</i>."))
    its.append(mcq("Simplify `a^2b^3*a^4b`.", "a^6b^4", ["a^8b^3", "a^6b^3", "3b^4"],
                   "Work with each base on its own. <i>a</i>: 2 + 4 = 6. <i>b</i>: 3 + 1 = 4 (<i>b</i> means `b^1`). "
                   "So the answer is `a^6b^4`.", check="a^2b^3*a^4b"))
    its.append(mcq("Simplify `4n^2*n^3*3n`.", "12n^6", ["7n^6", "12n^5", "7n^5"],
                   "Coefficients: 4 × 3 = 12 (the middle factor has coefficient 1). Exponents: 2 + 3 + 1 = 6. "
                   "So the answer is `12n^6`.", check="4n^2*n^3*3n"))
    its.append(mcq("Simplify `-2a^3b*3ab^4`.", "-6a^4b^5", ["-6a^3b^4", "6a^4b^5", "a^4b^5"],
                   "Coefficients: (−2) × 3 = −6. <i>a</i>: 3 + 1 = 4. <i>b</i>: 1 + 4 = 5. So the answer is `-6a^4b^5`. "
                   "Not `-6a^3b^4`: <i>a</i> and <i>b</i> on their own have exponent 1, not 0.", check="-2a^3b*3ab^4"))
    its.append(mcq("Write `8*2^5` as a single power of 2.", "2^8", ["16^5", "2^15", "2^6"],
                   "First write 8 as a power of 2: `8 = 2^3`. Then `2^3*2^5 = 2^8 = 256`. "
                   "Not `16^5`: do not multiply 8 × 2. Not `2^6`: 8 is three factors of 2, not one.",
                   check="8*2^5"))
    order = [0, 1, 2, 4, 3, 5, 6, 8, 7, 11, 10, 9, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Product law: add the exponents", "items": its}


# ============================================================ set 3: quotient law
def fr(p, q):
    """Fraction-bar division in HTML (text forms for top and bottom)."""
    return frac_html(h(p), h(q))


def set_quotient():
    its = []
    its.append(mcq(fig(quotient_svg("3", 6, 2, answer=False)) + "The picture shows `3^6/3^2`. Each crossed-out pair of 3s "
                   "divides to 1. Which power is left?", "3^4", ["3^3", "3^8", "1^4"],
                   "6 factors on top, 2 on the bottom. Each pair cancels, so 6 − 2 = 4 factors are left: `3^6/3^2 = 3^4`. "
                   "Not `3^3`: do not divide the exponents (6 ÷ 2 = 3).", check="3^6/3^2"))
    its.append(mcq("Simplify `5^6/5^2`.", "5^4", ["5^3", "1^4", "5^8"],
                   "Same base, so subtract the exponents: 6 − 2 = 4. `5^6/5^2 = 5^4`. "
                   "Not `1^4`: keep the base, do not divide 5 ÷ 5.", check="5^6/5^2"))
    its.append(mcq("Simplify `x^9/x^3`.", "x^6", ["x^3", "x^12", "1"],
                   "Subtract the exponents: 9 − 3 = 6. `x^9/x^3 = x^6`. Not `x^3`: that divides 9 ÷ 3.",
                   check="x^9/x^3"))
    its.append(mcq("Simplify `2^10/2^5`.", "2^5", ["2^2", "1^5", "2^15"],
                   "10 − 5 = 5, so `2^10/2^5 = 2^5 = 32`. Not `2^2`: 10 ÷ 5 = 2 divides the exponents.",
                   check="2^10/2^5"))
    its.append(mcq("Simplify `a^8/a`.", "a^7", ["a^8", "a^9", "a^6"],
                   "<i>a</i> means `a^1`, so subtract 1: 8 − 1 = 7. `a^8/a = a^7`.", check="a^8/a"))
    its.append(mcq("Simplify %s." % fr("y^8", "y^2"), "y^6", ["y^4", "y^10", "y^16"],
                   "A fraction bar means divide. Subtract the exponents: 8 − 2 = 6, so the answer is `y^6`. "
                   "Not `y^4`: that divides 8 ÷ 2.", check="y^8/y^2"))
    its.append(mcq("Evaluate `7^5/7^3`.", "49", ["14", "1", "343"],
                   "`7^5/7^3 = 7^2 = 49`. Not 14: that is 7 × 2. Not 1: that divides the bases 7 ÷ 7.",
                   check="7^5/7^3"))
    its.append(mcq("Evaluate `10^8/10^5`.", "1000", ["1", "30", "10000"],
                   "`10^8/10^5 = 10^3 = 1000`. Not 30: that is 10 × 3. Not 1: keep the base 10.",
                   check="10^8/10^5"))
    its.append(mcq("Simplify `(-4)^7/(-4)^4`.", "(-4)^3", ["(-4)^11", "1", "4^3"],
                   "Keep the base −4 and subtract: 7 − 4 = 3. `(-4)^3 = -64`. Not `4^3 = 64`: the base is still negative.",
                   check="(-4)^7/(-4)^4"))
    its.append(mcq("`6^☐/6^3 = 6^5`. Which exponent goes in the box?", "8", ["2", "15", "3"],
                   "The exponents subtract: ☐ − 3 = 5, so ☐ = 8. Check: `6^8/6^3 = 6^5`. "
                   "Not 2: that subtracts 5 − 3. Not 15: that multiplies 5 × 3."))
    its.append(mcq("Simplify `({2/3})^5/({2/3})^2`.", "({2/3})^3", ["({2/3})^7", "1", "({2/3})^10"],
                   "Same base `{2/3}`, so subtract the exponents: 5 − 2 = 3. The answer is `({2/3})^3 = {8/27}`.",
                   check="({2/3})^5/({2/3})^2"))
    its.append(mcq("Which quotient is equal to `3^4`?", "3^12/3^8", ["3^12/3^3", "3^8/3^2", "9^8/9^4"],
                   "12 − 8 = 4, so `3^12/3^8 = 3^4`. `3^12/3^3 = 3^9` (12 ÷ 3 = 4 is the dividing mistake). "
                   "`3^8/3^2 = 3^6` and `9^8/9^4 = 9^4`.", check="3^4"))
    its.append(mcq("Simplify `12x^7/4x^2`.", "3x^5", ["8x^5", "3x^9", "48x^5"],
                   "Divide the coefficients: 12 ÷ 4 = 3. Subtract the exponents: 7 − 2 = 5. So the answer is `3x^5`. "
                   "Not `8x^5`: do not subtract 12 − 4.", check="(12x^7)/(4x^2)"))
    its.append(mcq("Simplify %s." % fr("-20a^6", "5a^3"), "-4a^3", ["4a^3", "-4a^2", "-15a^3"],
                   "(−20) ÷ 5 = −4 and 6 − 3 = 3, so the answer is `-4a^3`. Not `-4a^2`: that divides 6 ÷ 3.",
                   check="(-20a^6)/(5a^3)"))
    its.append(mcq("Simplify %s." % fr("a^5b^6", "a^2b"), "a^3b^5", ["a^3b^6", "a^7b^7", "3b^5"],
                   "Work with each base. <i>a</i>: 5 − 2 = 3. <i>b</i>: 6 − 1 = 5 (<i>b</i> means `b^1`). "
                   "So the answer is `a^3b^5`.", check="(a^5b^6)/(a^2b)"))
    its.append(mcq("Simplify `x^4*x^6/x^3`.", "x^7", ["x^21", "x^8", "x^13"],
                   "Work left to right: `x^4*x^6 = x^10` (add), then `x^10/x^3 = x^7` (subtract). "
                   "Not `x^21`: that multiplies 4 × 6 first. Not `x^13`: that adds all three exponents.",
                   check="x^4*x^6/x^3"))
    its.append(mcq("Evaluate `(5^4*5^3)/5^5`.", "25", ["78125", "10", "1"],
                   "Top: `5^4*5^3 = 5^7`. Then `5^7/5^5 = 5^2 = 25`. Not 78 125: that is `5^12/5^5 = 5^7`. "
                   "Not 10: that is 5 × 2.", check="(5^4*5^3)/5^5"))
    its.append(mcq("Evaluate `(-3)^9/(-3)^6`.", "-27", ["27", "-9", "1"],
                   "9 − 6 = 3, so the answer is `(-3)^3 = -27`. Three negative factors give a negative answer. "
                   "Not −9: that is (−3) × 3.", check="(-3)^9/(-3)^6"))
    its.append(mcq("Simplify %s." % fr("18m^8n^5", "6m^2n^5"), "3m^6", ["3m^6n", "12m^6", "3m^4"],
                   "18 ÷ 6 = 3. <i>m</i>: 8 − 2 = 6. <i>n</i>: `n^5/n^5 = 1`, so no <i>n</i> is left. "
                   "So the answer is `3m^6`. Not `3m^4`: that divides 8 ÷ 2.", check="(18m^8n^5)/(6m^2n^5)"))
    its.append(mcq("`48y^☐/8y^3 = 6y^4`. Which exponent goes in the box?", "7", ["1", "12", "4"],
                   "48 ÷ 8 = 6 checks the coefficient. For the exponents: ☐ − 3 = 4, so ☐ = 7. "
                   "Not 1: that is 4 − 3. Not 12: that is 4 × 3."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Quotient law: subtract the exponents", "items": its}


# ============================================================ set 4: power of a power
def set_power():
    its = []
    its.append(mcq("Simplify `(2^3)^2`.", "2^6", ["2^5", "2^9", "4^6"],
                   "`(2^3)^2 = 2^3*2^3 = 2^6`. Multiply the exponents: 3 × 2 = 6. "
                   "Not `2^5`: do not add them. Not `2^9`: that uses `3^2 = 9` as the exponent.",
                   check="(2^3)^2"))
    its.append(mcq("Which means the same as `(x^4)^3`?", "x^4*x^4*x^4", ["3x^4", "x^4*x^3", "x^4*x^4"],
                   "The outside exponent 3 says to use `x^4` as a factor 3 times: `x^4*x^4*x^4 = x^12`. "
                   "It is not `3x^4`, which is `x^4+x^4+x^4`.", check="(x^4)^3"))
    its.append(mcq("Simplify `(a^5)^2`.", "a^10", ["a^7", "a^25", "2a^5"],
                   "Multiply the exponents: 5 × 2 = 10. `(a^5)^2 = a^5*a^5 = a^10`. Not `a^7`: that adds 5 + 2.",
                   check="(a^5)^2"))
    its.append(mcq("Simplify `(5^2)^4`.", "5^8", ["5^6", "5^16", "10^4"],
                   "2 × 4 = 8, so `(5^2)^4 = 5^8`. Not `10^4`: `5^2` is 25, not 10. Not `5^16`: that uses `2^4 = 16` as the exponent.",
                   check="(5^2)^4"))
    its.append(mcq("Simplify `(y^3)^5`.", "y^15", ["y^8", "y^243", "5y^3"],
                   "3 × 5 = 15, so `(y^3)^5 = y^15`. Not `y^8`: that adds. Not `y^243`: that is `3^5` in the exponent.",
                   check="(y^3)^5"))
    its.append(mcq("Evaluate `(2^2)^3`.", "64", ["32", "256", "12"],
                   "`(2^2)^3 = 2^6 = 64`. You can also work inside first: `2^2 = 4` and `4^3 = 64`. "
                   "Not 32: that is `2^5`. Not 12: that is 4 × 3.", check="(2^2)^3"))
    its.append(mcq("Evaluate `(10^2)^3`.", "1000000", ["100000", "100000000", "600"],
                   "2 × 3 = 6, so `(10^2)^3 = 10^6 = 1000000`. Not 100 000: that is `10^5` (adding). "
                   "Not 100 000 000: that is `10^8`, because `2^3 = 8`.", check="(10^2)^3"))
    its.append(mcq("`(7^☐)^4 = 7^20`. Which exponent goes in the box?", "5", ["16", "80", "24"],
                   "The exponents multiply: ☐ × 4 = 20, so ☐ = 5. Check: `(7^5)^4 = 7^20`. "
                   "Not 16: that is 20 − 4, as if the exponents were added."))
    its.append(mcq("Which is equal to `2^12`?", "(2^3)^4", ["(2^8)^4", "(2^6)^6", "(2^9)^3"],
                   "3 × 4 = 12, so `(2^3)^4 = 2^12`. The others add to 12 but multiply to 32, 36 and 27.",
                   check="2^12"))
    its.append(mcq("Write `4^5` as a power of 2.", "2^10", ["2^7", "2^5", "8^5"],
                   "`4 = 2^2`, so `4^5 = (2^2)^5 = 2^10`. Not `2^7`: that adds 2 + 5. "
                   "Not `8^5`: 4 is not 8.", check="4^5"))
    its.append(mcq("Simplify `(2x)^3`.", "8x^3", ["2x^3", "6x^3", "8x"],
                   "`(2x)^3 = 2x*2x*2x`. Every factor inside the brackets is cubed: `2^3x^3 = 8x^3`. "
                   "Not `2x^3`: the 2 must be cubed too. Not `6x^3`: `2^3` is 8, not 2 × 3.", check="(2x)^3"))
    its.append(mcq("Simplify `(3a^2)^2`.", "9a^4", ["3a^4", "6a^4", "9a^2"],
                   "Square the 3 and the `a^2`: `3^2 = 9` and `(a^2)^2 = a^4`. So the answer is `9a^4`. "
                   "Not `6a^4`: `3^2` is 9, not 3 × 2.", check="(3a^2)^2"))
    its.append(mcq("Simplify `(-2y^3)^2`.", "4y^6", ["-4y^6", "4y^5", "-2y^6"],
                   "`(-2)^2 = 4` (two negative factors) and `(y^3)^2 = y^6`. So the answer is `4y^6`. "
                   "Not `4y^5`: multiply 3 × 2, do not add.", check="(-2y^3)^2"))
    its.append(mcq("Simplify `(-2y^3)^3`.", "-8y^9", ["8y^9", "-6y^9", "-8y^6"],
                   "`(-2)^3 = -8` (three negative factors) and `(y^3)^3 = y^9`. So the answer is `-8y^9`.",
                   check="(-2y^3)^3"))
    its.append(mcq("Evaluate `({2/5})^2`.", "{4/25}", ["{4/5}", "{2/25}", "{4/10}"],
                   "Square the top and the bottom: `({2/5})^2 = {2^2/5^2} = {4/25}`. "
                   "Not `{4/10}`: that multiplies by 2 instead of squaring.", check="({2/5})^2"))
    its.append(mcq("Simplify `({x/y})^3`.", "{x^3/y^3}", ["{x^3/y}", "{x/y^3}", "{3x/3y}"],
                   "The exponent applies to the top and the bottom: `({x/y})^3 = {x/y}*{x/y}*{x/y} = {x^3/y^3}`.",
                   check="({x/y})^3"))
    its.append(mcq("Simplify `(a^2b^3)^4`.", "a^8b^12", ["a^6b^7", "a^8b^3", "a^2b^12"],
                   "Raise each factor: `(a^2)^4 = a^8` and `(b^3)^4 = b^12`. So the answer is `a^8b^12`. "
                   "Not `a^6b^7`: that adds 4 to each exponent.", check="(a^2b^3)^4"))
    its.append(mcq("Simplify `(x^3)^2*x^4`.", "x^10", ["x^9", "x^24", "x^13"],
                   "Power of a power first: `(x^3)^2 = x^6`. Then the product law: `x^6*x^4 = x^10`. "
                   "Not `x^9`: that adds all three. Not `x^13`: that uses `3^2 = 9`.", check="(x^3)^2*x^4"))
    its.append(mcq("Simplify `(2a^3b)^4`.", "16a^12b^4", ["8a^12b^4", "2a^12b^4", "16a^7b^5"],
                   "Raise every factor to the 4th power: `2^4 = 16`, `(a^3)^4 = a^12` and `b^4`. "
                   "So the answer is `16a^12b^4`. Not `8a^12b^4`: `2^4` is 16, not 2 × 4.", check="(2a^3b)^4"))
    its.append(mcq("Simplify %s." % fr("(m^2n^3)^3", "m^4n^5"), "m^2n^4", ["mn", "m^6n^9", "m^10n^14"],
                   "Top: `(m^2n^3)^3 = m^6n^9`. Divide: <i>m</i>: 6 − 4 = 2, <i>n</i>: 9 − 5 = 4. "
                   "So the answer is `m^2n^4`. Not `mn`: that adds 3 to each exponent inside "
                   "instead of multiplying. Not `m^10n^14`: that adds the bottom exponents instead of subtracting.",
                   check="((m^2n^3)^3)/(m^4n^5)"))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Power of a power, product and quotient", "items": its}


# ============================================================ set 5: zero exponent, mixed and word problems
def set_zero():
    its = []
    its.append(mcq("Evaluate `7^0`.", "1", ["0", "7", "{1/7}"],
                   "Any non-zero number to the power 0 is 1, so `7^0 = 1`. It is not 0: "
                   "`7^0 = 7^2/7^2 = 49/49 = 1`.", check="7^0"))
    its.append(mcq("Simplify `x^5/x^5` (<i>x</i> ≠ 0).", "1", ["0", "x", "x^10"],
                   "A number divided by itself is 1. With the quotient law: `x^5/x^5 = x^0`, and `x^0 = 1`. "
                   "So `x^0` is 1, not 0.", check="x^5/x^5"))
    its.append(mcq("Evaluate `(-5)^0`.", "1", ["-1", "0", "-5"],
                   "The base is −5 (in brackets), and any non-zero base to the power 0 is 1.", check="(-5)^0"))
    its.append(mcq("Evaluate `-5^0`.", "-1", ["1", "0", "-5"],
                   "With no brackets the base is 5: `-5^0 = -(5^0) = -1`. Compare `(-5)^0 = 1`.", check="-5^0"))
    its.append(mcq("Simplify `4x^0` (<i>x</i> ≠ 0).", "4", ["1", "0", "4x"],
                   "Only <i>x</i> has the exponent 0: `4x^0 = 4*1 = 4`. Not 1: the 4 is not raised to the power 0.",
                   check="4x^0"))
    its.append(mcq("Simplify `(4x)^0` (<i>x</i> ≠ 0).", "1", ["4", "0", "4x"],
                   "Now the brackets make `4x` the base, and any non-zero base to the power 0 is 1. Compare `4x^0 = 4`.",
                   check="(4x)^0"))
    its.append(mcq("Evaluate `2^0+3^0`.", "2", ["0", "5", "1"],
                   "`2^0 = 1` and `3^0 = 1`, so the sum is 1 + 1 = 2. Not 0: that uses `a^0 = 0`. "
                   "Not 5: that uses `a^0 = a`.", check="2^0+3^0"))
    its.append(mcq("Evaluate `2^3*2^4/2^5`.", "4", ["128", "1", "32"],
                   "`2^3*2^4 = 2^7`, then `2^7/2^5 = 2^2 = 4`. Not 128: that is `2^12/2^5 = 2^7`. "
                   "Not 32: that stops at `2^5`.", check="2^3*2^4/2^5"))
    its.append(mcq("Simplify `(x^4)^2/x^6`.", "x^2", ["1", "0", "x^14"],
                   "`(x^4)^2 = x^8`, then `x^8/x^6 = x^2`. Not 1: that adds 4 + 2 = 6 and gets `x^0`. "
                   "Not `x^14`: that adds instead of subtracting.", check="((x^4)^2)/(x^6)"))
    its.append(mcq("Simplify `3x^4*2x^3/x^7` (<i>x</i> ≠ 0).", "6", ["0", "6x", "1"],
                   "Coefficients: 3 × 2 = 6. Exponents: 4 + 3 − 7 = 0, and `x^0 = 1`. So the answer is `6*1 = 6`. "
                   "Not 0 and not `6x`: `x^0` is 1.", check="3x^4*2x^3/x^7"))
    its.append(mcq("Simplify `(a^2b)^3/a^6`.", "b^3", ["0", "ab^3", "b"],
                   "`(a^2b)^3 = a^6b^3`. Then `a^6/a^6 = a^0 = 1`, so `b^3` is left. Not `ab^3`: `a^0` is 1, not <i>a</i>. "
                   "Not <i>b</i>: the <i>b</i> is cubed too.", check="((a^2b)^3)/(a^6)"))
    its.append(mcq("Evaluate `(2^3)^2/2^4+5^0`.", "5", ["4", "9", "3"],
                   "`(2^3)^2 = 2^6`, `2^6/2^4 = 2^2 = 4`, and `5^0 = 1`. So 4 + 1 = 5. Not 4: that uses `5^0 = 0`. "
                   "Not 9: that uses `5^0 = 5`. Not 3: that adds the exponents, `(2^3)^2 = 2^5`.",
                   check="((2^3)^2)/(2^4)+5^0"))
    # word problems
    its.append(mcq("In a science class in Burnaby, a sample of bacteria doubles every hour. After 3 hours it is "
                   "`2^3` times its first size. After 5 more hours, how many times its first size is it?",
                   "256", ["32768", "16", "128"],
                   "It doubles 3 times, then 5 more times: `2^3*2^5 = 2^8 = 256`. Not 32 768: that is `2^15` "
                   "(multiplying the exponents). Not 16: that is 2 × 8.", check="2^3*2^5"))
    its.append(mcq("Ji-woo’s tablet has `2^8` GB of storage. Each movie he downloads uses `2^2` GB. "
                   "How many movies fit on the tablet?", "64", ["16", "128", "6"],
                   "`2^8/2^2 = 2^6 = 64` movies. Not 16: that is `2^4` (8 ÷ 2 divides the exponents). "
                   "Not 6: that is only the exponent.", check="2^8/2^2"))
    its.append(mcq(fig(square_svg("5x^3", "m")) + "A square plot in a Kelowna community garden has sides of "
                   "`5x^3` m. Which expression gives its area in square metres?", "25x^6", ["5x^6", "10x^6", "20x^3"],
                   "Area = side × side = `(5x^3)^2 = 5^2*(x^3)^2 = 25x^6`. Not `5x^6`: square the 5 too. "
                   "Not `20x^3`: that is the perimeter, 4 × `5x^3`.", check="(5x^3)^2"))
    its.append(mcq(fig(cube_svg("2x^2", "cm")) + "Leah builds a planter box shaped like a cube with edges of "
                   "`2x^2` cm. Which expression gives its volume in cubic centimetres?", "8x^6", ["2x^6", "6x^6", "8x^5"],
                   "Volume = edge × edge × edge = `(2x^2)^3 = 2^3*(x^2)^3 = 8x^6`. Not `6x^6`: `2^3` is 8, not 2 × 3. "
                   "Not `8x^5`: multiply the exponents 2 × 3, do not add.", check="(2x^2)^3"))
    its.append(mcq(fig(rect_svg("4x^3", "3x^2", "m")) + "A rectangular garden bed at a Surrey school is `4x^3` m long "
                   "and `3x^2` m wide. Which expression gives its area in square metres?", "12x^5",
                   ["7x^5", "12x^6", "7x^6"],
                   "Area = length × width = `4x^3*3x^2`. Multiply the coefficients (4 × 3 = 12) and add the "
                   "exponents (3 + 2 = 5): `12x^5`. Not `7x^5`: do not add 4 + 3.", check="4x^3*3x^2"))
    its.append(mcq("A salmon hatchery on Vancouver Island has `10^6` eggs. It splits them equally into `10^2` trays. "
                   "How many eggs go in each tray?", "10^4", ["10^3", "10^8", "1^4"],
                   "`10^6/10^2 = 10^4 = 10000` eggs per tray. Subtract the exponents: 6 − 2 = 4. "
                   "Not `10^3`: that divides 6 ÷ 2.", check="10^6/10^2"))
    its.append(mcq(fig(doubling_svg()) + "The number of cells in a sample is 300 × 2<sup><i>t</i></sup>, where <i>t</i> is the time "
                   "in hours. How many cells are there at the start, when <i>t</i> = 0?", "300", ["0", "600", "1"],
                   "At <i>t</i> = 0 the number is `300*2^0 = 300*1 = 300`. Not 0: `2^0` is 1, not 0. "
                   "Not 600: `2^0` is not 2. Not 1: `2^0 = 1` is only the factor; multiply it by 300.", check="300*2^0"))
    its.append(mcq("A recycling bin at a Victoria school is a cube with edges of `10^2` cm. How many small cubes "
                   "with edges of 10 cm would fill it?", "1000", ["100", "10", "1000000"],
                   "Volume of the bin: `(10^2)^3 = 10^6` cm³. Volume of a small cube: `10^3` cm³. "
                   "`10^6/10^3 = 10^3 = 1000`. Not 1 000 000: that forgets to divide by the small cube’s volume.",
                   check="((10^2)^3)/(10^3)"))
    assert len(its) == 20
    return {"title": "Zero exponent, mixed practice and word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, T(q), T(s), T(a)))


def table(head, rows):
    hd = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % T(x) for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (hd, b)


def body_html():
    return T(
        "<h2>Powers</h2>"
        "<p>A <b>power</b> is a short way to write repeated multiplication. In `a^4`, <i>a</i> is the <b>base</b> "
        "and 4 is the <b>exponent</b>: `a^4 = a*a*a*a`. Watch the brackets: in `(-2)^4` the base is −2, "
        "but in `-2^4` the base is 2.</p>"
        + ex("Negative bases", "Evaluate `(-2)^4` and `-2^4`.",
             "`(-2)^4 = (-2)*(-2)*(-2)*(-2) = 16`. `-2^4 = -(2*2*2*2) = -16`.", "16 and −16")
        + "<h2>Product law</h2>"
        "<p>When you <b>multiply</b> powers with the <b>same base</b>, keep the base and <b>add</b> the exponents: "
        "`a^m*a^n = a^(m+n)`.</p>"
        "<figure class='sn-fig'>" + product_svg("a", 3, 4) +
        "<figcaption>`a^3*a^4`: 3 factors of <i>a</i> and 4 more make 7 factors, so `a^3*a^4 = a^7`."
        "</figcaption></figure>"
        + ex("Product law", "Simplify `2x^3*4x^5`.",
             "Multiply the coefficients: 2 × 4 = 8. Add the exponents: 3 + 5 = 8.", "`8x^8`")
        + "<h2>Quotient law</h2>"
        "<p>When you <b>divide</b> powers with the same base, keep the base and <b>subtract</b> the exponents: "
        "`a^m/a^n = a^(m-n)`.</p>"
        "<figure class='sn-fig'>" + quotient_svg("a", 6, 2) +
        "<figcaption>Each crossed-out pair divides to 1. 6 − 2 = 4 factors are left: `a^6/a^2 = a^4`."
        "</figcaption></figure>"
        + ex("Quotient law", "Simplify `12x^7/4x^2`.",
             "Divide the coefficients: 12 ÷ 4 = 3. Subtract the exponents: 7 − 2 = 5.", "`3x^5`")
        + "<h2>Power of a power</h2>"
        "<p>For a power raised to a power, <b>multiply</b> the exponents: `(a^m)^n = a^(mn)`. "
        "An exponent outside brackets applies to every factor inside: `(ab)^n = a^nb^n`.</p>"
        + ex("Power of a power", "Simplify `(2a^3)^4`.",
             "`(2a^3)^4 = 2a^3*2a^3*2a^3*2a^3`. Raise each factor: `2^4 = 16` and `(a^3)^4 = a^12`.", "`16a^12`")
        + "<h2>Zero exponent</h2>"
        "<p>Any non-zero number to the power 0 is <b>1</b>. Each step down the table divides by 2, so `2^0 = 2/2 = 1`."
        " The quotient law agrees: `a^3/a^3 = a^0`, and anything divided by itself is 1.</p>"
        + table(["Power", "Value"], [["`2^3`", "8"], ["`2^2`", "4"], ["`2^1`", "2"], ["`2^0`", "1"]])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["`a^3*a^4 = a^12` (multiplying the exponents)", "Add them: `a^3*a^4 = a^7`"],
            ["`2^3*2^4 = 4^7` (multiplying the bases)", "Keep the base: `2^3*2^4 = 2^7`"],
            ["`a^8/a^2 = a^4` (dividing the exponents)", "Subtract them: `a^8/a^2 = a^6`"],
            ["`(a^3)^4 = a^7` (adding)", "Multiply them: `(a^3)^4 = a^12`"],
            ["`(2x)^3 = 2x^3`", "Cube every factor: `(2x)^3 = 8x^3`"],
            ["`a^0 = 0`", "`a^0 = 1` for any <i>a</i> ≠ 0"],
            ["`-2^4 = 16`", "The base is 2: `-2^4 = -16`, but `(-2)^4 = 16`"],
        ])
    )


FAQ = [
    {"q": "What exponent laws are in Grade 9 math in BC?",
     "a": "Mathematics 9 in BC covers exponents and exponent laws with whole-number exponents: the product law "
          "aᵐ × aⁿ = aᵐ⁺ⁿ, the quotient law aᵐ ÷ aⁿ = aᵐ⁻ⁿ, the power of a power (aᵐ)ⁿ = aᵐⁿ, "
          "the power of a product (ab)ⁿ = aⁿbⁿ, and the zero exponent a⁰ = 1."},
    {"q": "Why is a³ × a⁴ = a⁷ and not a¹²?",
     "a": "a³ is 3 factors of a and a⁴ is 4 more, so together there are 3 + 4 = 7 factors. You add the exponents "
          "when you multiply powers; you multiply them only for a power of a power, like (a³)⁴ = a¹²."},
    {"q": "Why is any number to the power of zero equal to 1?",
     "a": "Look at the pattern 2³ = 8, 2² = 4, 2¹ = 2: each step divides by 2, so 2⁰ = 1. The quotient law also "
          "gives a³ ÷ a³ = a⁰, and any non-zero number divided by itself is 1."},
    {"q": "What is the difference between (−2)⁴ and −2⁴?",
     "a": "In (−2)⁴ the base is −2, so (−2)⁴ = 16. In −2⁴ the base is 2 and the negative sign is applied after, "
          "so −2⁴ = −16."},
]


SVG = re.compile(r"(<svg.*?</svg>)", re.S)
GAP = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")


def nbsp(s):
    """No-break space between digit groups (78 125) everywhere outside SVG markup."""
    return "".join(p if p.startswith("<svg") else GAP.sub(NB, p) for p in SVG.split(s))


def fix_spaces(u):
    for k in ("meta_desc", "key_big", "key_sub", "body_html"):
        u[k] = nbsp(u[k])
    for f in u["faq"]:
        f["q"], f["a"] = nbsp(f["q"]), nbsp(f["a"])
    for s in u["sets"]:
        for it in s["items"]:
            it["q"], it["e"] = nbsp(it["q"]), nbsp(it["e"])
            it["c"] = [nbsp(c) for c in it["c"]]
    return u


def mark_large(u, pattern):
    """Tag wide pictures (rows of factor boxes) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(59801)
    sets = [set_powers(), set_product(), set_quotient(), set_power(), set_zero()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            assert "`" not in it["q"] + it["e"] + "".join(it["c"]), it
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "exponent-laws", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Exponent Laws",
        "seo_title": "Grade 9 Exponent Laws Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Exponent laws",
        "domain": "Number",
        "standard_code": "Grade 9: Number",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Exponents and exponent laws with whole-number exponents",
        "meta_desc": "Free Grade 9 math worksheets on exponent laws for the BC curriculum: powers with negative and "
                     "fraction bases, the product law (a³ × a⁴ = a⁷), the quotient law, the power of a power, "
                     "the zero exponent, and word problems. 100 questions with an answer key.",
        "key_big": "Multiply powers with the same base: add the exponents. Divide: subtract them. "
                   "Power of a power: multiply them.",
        "key_sub": "a³ × a⁴ = a⁷ (not a¹²), a⁷ ÷ a³ = a⁴, (a³)⁴ = a¹², and a⁰ = 1 (not 0) for any a ≠ 0.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(fix_spaces(u), "[0-9]+ factors of")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
