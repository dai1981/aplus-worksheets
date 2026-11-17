# -*- coding: utf-8 -*-
"""
US Algebra 1: Factoring Polynomials (Common Core A-SSE.A.2, A-SSE.B.3a)
  python3 tools/gen_us_math_a1_factoring_polynomials.py
Factoring out the greatest common factor, factoring x² + bx + c, factoring ax² + bx + c (the AC method),
differences of squares and perfect square trinomials, and factoring completely.
Wrong answers come from real mistakes: taking out a common factor that is not the greatest, choosing two
numbers that multiply to c but do not add to b, sign errors with a negative c, factoring a sum of squares,
and stopping before the polynomial is factored completely.
"""
import random
from math import gcd
from us_hs import num, B, S, make, lesson, collect, T, expr, MINUS

R = random.Random(91501)
X = "<i>x</i>"
X2 = "<i>x</i><sup>2</sup>"


def lin(a, b, v=X):
    return expr([(a, v), (b, "")])


def br(a, b):
    return "(%s)" % lin(a, b)


def quad(a, b, c):
    return expr([(a, X2), (b, X), (c, "")])


def nz(r, lo, hi):
    while True:
        k = r.randint(lo, hi)
        if k:
            return k


def pair(p, q):
    """(x + p)(x + q) with the smaller constant first for a stable answer."""
    p, q = sorted([p, q])
    return br(1, p) + br(1, q) if p != q else br(1, p) + "<sup>2</sup>"


def uniq(right, wr):
    out = [w for w in dict.fromkeys(wr) if w != right]
    return out[:3] if len(out) >= 3 else None


# ------------------------------------------------------------ set 1: GCF
def one_gcf(r):
    g = r.choice([2, 3, 4, 5, 6, 8])
    k = r.randint(0, 2)
    vk = ["", X, X2][k]
    a, b, c = nz(r, 1, 6), nz(r, -7, 7), r.randint(-7, 7)
    if gcd(gcd(a, abs(b)), abs(c) if c else 0) != 1:
        return None
    terms = [(g * a, "<i>x</i><sup>%d</sup>" % (k + 2) if k + 2 > 1 else X), (g * b, "<i>x</i><sup>%d</sup>" % (k + 1) if k + 1 > 1 else X), (g * c, vk)]
    full = expr(terms)
    inner = expr([(a, X2), (b, X), (c, "")])
    gf = num(g) + vk
    right = "%s(%s)" % (gf, inner)
    small = [d for d in (2, 3) if g % d == 0 and d < g]
    wr = ["%s(%s)" % (num(g), expr([(a, "<i>x</i><sup>%d</sup>" % (k + 2) if k + 2 > 1 else X), (b, "<i>x</i><sup>%d</sup>" % (k + 1) if k + 1 > 1 else X), (c, vk)])) if k else "%s(%s)" % (num(g), expr([(a, X2), (b, X), (c * g, "")])),
          "%s(%s)" % (num(small[0]) + vk if small else num(g * 2) + vk, expr([(g * a // small[0], X2), (g * b // small[0], X), (g * c // small[0], "")])) if small else "%s(%s)" % (gf, expr([(a, X2), (b, X), (c * g, "")])),
          "%s(%s)" % (gf, expr([(a, X2), (b, X), (-c, "")])) if c else "%s(%s)" % (gf, expr([(a, X2), (-b, X)]))]
    if c == 0:
        return None
    q = "Factor out the greatest common factor: %s." % B(full)
    e = "The GCF of the numbers is %d%s. Divide every term by %s: <b>%s</b>." % (g, " and every term has %s" % vk if vk else "", gf, right)
    wr = uniq(right, wr)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 2: x² + bx + c
def one_simple(r):
    p, q_ = nz(r, -9, 9), nz(r, -9, 9)
    b, c = p + q_, p * q_
    if b == 0:
        return None
    q = "Factor %s." % B(quad(1, b, c))
    right = pair(p, q_)
    cands = []
    for u in range(-12, 13):
        if u and c % u == 0:
            v = c // u
            if u + v != b and u <= v:
                cands.append(pair(u, v))
    r.shuffle(cands)
    wr = [pair(-p, -q_)] + cands
    wr = uniq(right, wr)
    if not wr:
        return None
    e = "Find two numbers that multiply to %s and add to %s: %s and %s. <b>%s</b>." % (num(c), num(b), num(p), num(q_), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 3: ax² + bx + c
def one_ac(r):
    a1, a2 = r.choice([1, 2, 3]), r.choice([2, 3, 5])
    b1, b2 = nz(r, -7, 7), nz(r, -7, 7)
    if gcd(a1, abs(b1)) != 1 or gcd(a2, abs(b2)) != 1:
        return None
    A, Bc, C = a1 * a2, a1 * b2 + a2 * b1, b1 * b2
    if Bc == 0:
        return None
    q = "Factor %s." % B(quad(A, Bc, C))
    right = br(a1, b1) + br(a2, b2)
    wr = [br(a1, b2) + br(a2, b1), br(a1, -b1) + br(a2, -b2), br(a1, b1) + br(a2, -b2)]
    wr = uniq(right, wr)
    if not wr:
        return None
    e = ("<i>ac</i> = %s × %s = %s. Find two numbers that multiply to %s and add to %s: %s and %s. Split the middle term and group: <b>%s</b>. "
         "Check by multiplying back." % (num(A), num(C), num(A * C), num(A * C), num(Bc), num(a1 * b2), num(a2 * b1), right))
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: special patterns
def one_special(r):
    kind = r.choice(["dos", "dos", "ps+", "ps-", "sum"])
    a, b = r.choice([1, 1, 2, 3, 4, 5]), r.randint(1, 10)
    if gcd(a, b) != 1:
        return None
    if kind == "dos":
        q = "Factor %s." % B(expr([(a * a, X2), (-b * b, "")]))
        right = br(a, b) + br(a, -b) if True else ""
        right = br(a, -b) + br(a, b)
        wr = [br(a, -b) + "<sup>2</sup>", br(a, b) + "<sup>2</sup>", br(a, -b * b) + br(a, b * b) if b > 1 else br(a * a, -1) + br(1, 1)]
        e = "This is a difference of squares, <i>A</i><sup>2</sup> − <i>B</i><sup>2</sup> = (<i>A</i> − <i>B</i>)(<i>A</i> + <i>B</i>), with <i>A</i> = %s and <i>B</i> = %d: <b>%s</b>." % (lin(a, 0), b, right)
    elif kind in ("ps+", "ps-"):
        s = 1 if kind == "ps+" else -1
        q = "Factor %s." % B(quad(a * a, s * 2 * a * b, b * b))
        right = br(a, s * b) + "<sup>2</sup>"
        wr = [br(a, -s * b) + "<sup>2</sup>", br(a, b) + br(a, -b), br(a, s * b * b) + br(a, s)]
        e = "The first and last terms are squares and the middle term is 2 × %s × %d, so it is a perfect square trinomial: <b>%s</b>." % (lin(a, 0), b, right)
    else:
        q = "Factor %s, if possible." % B(expr([(a * a, X2), (b * b, "")]))
        right = "It cannot be factored (a sum of squares)"
        wr = [br(a, b) + "<sup>2</sup>", br(a, b) + br(a, -b), br(a, -b) + "<sup>2</sup>"]
        e = "A <b>sum</b> of squares cannot be factored with real numbers. Check: (%s)(%s) gives −%d, and (%s)<sup>2</sup> gives a middle term." % (lin(a, b), lin(a, -b), b * b, lin(a, b))
    wr = uniq(right, wr)
    if not wr:
        return None
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: factor completely and applications
def one_complete(r):
    g = r.choice([2, 3, 4, 5, -2, -1])
    kind = r.choice(["tri", "dos", "xgcf"])
    if kind == "tri":
        p, q_ = nz(r, -6, 6), nz(r, -6, 6)
        if p + q_ == 0:
            return None
        full = quad(g, g * (p + q_), g * p * q_)
        right = (num(g) if g != -1 else MINUS) + pair(p, q_)
        wr = [(num(g) if g != -1 else MINUS) + "(%s)" % quad(1, p + q_, p * q_), pair(g * p, q_) if g * p != q_ else pair(g * p, q_ + 1), (num(-g) if g != 1 else MINUS) + pair(p, q_)]
        e = "First take out %s: %s(%s). Then factor the trinomial: <b>%s</b>." % (num(g), num(g) if g != -1 else MINUS, quad(1, p + q_, p * q_), right)
    elif kind == "dos":
        b = r.randint(1, 7)
        k = abs(g) if abs(g) > 1 else 2
        full = expr([(k, X2), (-k * b * b, "")])
        right = num(k) + br(1, -b) + br(1, b)
        wr = [num(k) + "(%s)" % expr([(1, X2), (-b * b, "")]), br(k, -b) + br(1, b), num(k) + br(1, -b) + "<sup>2</sup>"]
        e = "Take out %d: %d(%s). Then use the difference of squares: <b>%s</b>." % (k, k, expr([(1, X2), (-b * b, "")]), right)
    else:
        p, q_ = nz(r, -5, 5), nz(r, -5, 5)
        if p + q_ == 0:
            return None
        full = expr([(1, "<i>x</i><sup>3</sup>"), (p + q_, X2), (p * q_, X)])
        right = X + pair(p, q_)
        wr = [X + "(%s)" % quad(1, p + q_, p * q_), pair(p, q_), X2 + br(1, p + q_)]
        e = "Every term has an <i>x</i>: <i>x</i>(%s). Then factor the trinomial: <b>%s</b>." % (quad(1, p + q_, p * q_), right)
    wr = uniq(right, wr)
    if not wr:
        return None
    return T("Factor completely: %s." % B(full), right, wr, e)


def problems():
    data = [
        ("The area of a rectangle is <i>x</i><sup>2</sup> + 7<i>x</i> + 12. Its width is <i>x</i> + 3. What is its length?", "<i>x</i> + 4", ["<i>x</i> + 9", "<i>x</i> + 12", "<i>x</i> + 7"], "<i>x</i><sup>2</sup> + 7<i>x</i> + 12 = (<i>x</i> + 3)(<i>x</i> + 4), so the length is <b><i>x</i> + 4</b>."),
        ("A square has area 9<i>x</i><sup>2</sup> + 30<i>x</i> + 25. What is its side length?", "3<i>x</i> + 5", ["9<i>x</i> + 5", "3<i>x</i> + 25", "9<i>x</i> + 25"], "9<i>x</i><sup>2</sup> + 30<i>x</i> + 25 = (3<i>x</i> + 5)<sup>2</sup>: <b>3<i>x</i> + 5</b>."),
        ("Use factoring to find 51<sup>2</sup> − 49<sup>2</sup>.", "200", ["4", "2", "400"], "(51 − 49)(51 + 49) = 2 × 100 = <b>200</b>."),
        ("Which is a factor of <i>x</i><sup>2</sup> − 5<i>x</i> − 14?", "<i>x</i> − 7", ["<i>x</i> + 7", "<i>x</i> − 2", "<i>x</i> + 14"], "−7 × 2 = −14 and −7 + 2 = −5, so it is (<i>x</i> − 7)(<i>x</i> + 2). <b><i>x</i> − 7</b>."),
        ("Grace factors 4<i>x</i><sup>2</sup> − 16 as (2<i>x</i> − 4)(2<i>x</i> + 4). Is it factored completely?", "No, it is 4(<i>x</i> − 2)(<i>x</i> + 2)", ["Yes", "No, it is (4<i>x</i> − 4)(<i>x</i> + 4)", "No, it is 4(<i>x</i><sup>2</sup> − 4)"],
         "Each binomial still has a common factor of 2. Taking out the GCF first gives <b>4(<i>x</i> − 2)(<i>x</i> + 2)</b>."),
        ("Which value of <i>b</i> makes <i>x</i><sup>2</sup> + <i>bx</i> + 36 a perfect square trinomial?", "12", ["6", "36", "18"], "(<i>x</i> + 6)<sup>2</sup> = <i>x</i><sup>2</sup> + 12<i>x</i> + 36, so <b><i>b</i> = 12</b>."),
        ("Which polynomial is prime (cannot be factored with integers)?", "<i>x</i><sup>2</sup> + 3<i>x</i> + 5", ["<i>x</i><sup>2</sup> + 5<i>x</i> + 6", "<i>x</i><sup>2</sup> − 9", "<i>x</i><sup>2</sup> − <i>x</i> − 6"], "No two integers multiply to 5 and add to 3: <b><i>x</i><sup>2</sup> + 3<i>x</i> + 5</b>."),
        ("What is the GCF of 12<i>x</i><sup>3</sup> and 18<i>x</i><sup>2</sup>?", "6<i>x</i><sup>2</sup>", ["6<i>x</i><sup>3</sup>", "3<i>x</i><sup>2</sup>", "36<i>x</i><sup>5</sup>"], "GCF of 12 and 18 is 6; the lower power of <i>x</i> is <i>x</i><sup>2</sup>: <b>6<i>x</i><sup>2</sup></b>."),
        ("How can you check a factorization?", "Multiply the factors back together", ["Add the factors", "Check one term only", "Substitute 0 for every variable"], "Multiplying the factors should give the original polynomial: <b>multiply back</b>."),
        ("Factor <i>x</i><sup>4</sup> − 16 completely.", "(<i>x</i><sup>2</sup> + 4)(<i>x</i> − 2)(<i>x</i> + 2)", ["(<i>x</i><sup>2</sup> − 4)(<i>x</i><sup>2</sup> + 4)", "(<i>x</i> − 2)<sup>4</sup>", "(<i>x</i> − 4)(<i>x</i> + 4)"],
         "<i>x</i><sup>4</sup> − 16 = (<i>x</i><sup>2</sup> − 4)(<i>x</i><sup>2</sup> + 4), and <i>x</i><sup>2</sup> − 4 factors again: <b>(<i>x</i><sup>2</sup> + 4)(<i>x</i> − 2)(<i>x</i> + 2)</b>."),
        ("Factor by grouping: <i>x</i><sup>3</sup> + 2<i>x</i><sup>2</sup> + 3<i>x</i> + 6.", "(<i>x</i><sup>2</sup> + 3)(<i>x</i> + 2)", ["(<i>x</i><sup>2</sup> + 2)(<i>x</i> + 3)", "<i>x</i>(<i>x</i><sup>2</sup> + 2<i>x</i> + 9)", "(<i>x</i> + 3)(<i>x</i> + 2)"],
         "<i>x</i><sup>2</sup>(<i>x</i> + 2) + 3(<i>x</i> + 2) = <b>(<i>x</i><sup>2</sup> + 3)(<i>x</i> + 2)</b>."),
        ("A ball's height is <i>h</i> = −16<i>t</i><sup>2</sup> + 32<i>t</i>. Which is the factored form?", "−16<i>t</i>(<i>t</i> − 2)", ["16<i>t</i>(<i>t</i> − 2)", "−16(<i>t</i> − 2)", "−16<i>t</i>(<i>t</i> + 2)"], "Take out −16<i>t</i>: <b>−16<i>t</i>(<i>t</i> − 2)</b>."),
        ("Which expression is equivalent to 2<i>x</i><sup>2</sup> + 7<i>x</i> + 3?", "(2<i>x</i> + 1)(<i>x</i> + 3)", ["(2<i>x</i> + 3)(<i>x</i> + 1)", "(2<i>x</i> + 1)(<i>x</i> + 6)", "2(<i>x</i> + 1)(<i>x</i> + 3)"], "Check: (2<i>x</i> + 1)(<i>x</i> + 3) = 2<i>x</i><sup>2</sup> + 6<i>x</i> + <i>x</i> + 3 ✓."),
        ("Find two numbers that multiply to −24 and add to 5.", "8 and −3", ["−8 and 3", "6 and −4", "12 and −2"], "8 × (−3) = −24 and 8 + (−3) = <b>5</b>."),
        ("The area of a rectangle is 3<i>x</i><sup>2</sup> − 12<i>x</i>. Its length is 3<i>x</i>. What is its width?", "<i>x</i> − 4", ["<i>x</i> − 12", "3<i>x</i> − 4", "<i>x</i> + 4"], "3<i>x</i><sup>2</sup> − 12<i>x</i> = 3<i>x</i>(<i>x</i> − 4): <b><i>x</i> − 4</b>."),
        ("Which is the factored form of <i>x</i><sup>2</sup> − 10<i>x</i> + 25?", "(<i>x</i> − 5)<sup>2</sup>", ["(<i>x</i> + 5)<sup>2</sup>", "(<i>x</i> − 5)(<i>x</i> + 5)", "(<i>x</i> − 25)(<i>x</i> − 1)"], "−5 × −5 = 25 and −5 + −5 = −10: <b>(<i>x</i> − 5)<sup>2</sup></b>."),
        ("Factor <i>x</i><sup>2</sup> − <i>y</i><sup>2</sup>.", "(<i>x</i> − <i>y</i>)(<i>x</i> + <i>y</i>)", ["(<i>x</i> − <i>y</i>)<sup>2</sup>", "(<i>x</i> + <i>y</i>)<sup>2</sup>", "It cannot be factored"], "Difference of squares: <b>(<i>x</i> − <i>y</i>)(<i>x</i> + <i>y</i>)</b>."),
        ("Why is (<i>x</i> + 2)(2<i>x</i> + 4) not completely factored?", "2<i>x</i> + 4 still has a common factor of 2", ["The binomials should be the same", "It should have three factors of <i>x</i>", "It is completely factored"], "2<i>x</i> + 4 = 2(<i>x</i> + 2), so it is <b>2(<i>x</i> + 2)<sup>2</sup></b>."),
        ("Which expression shows 6<i>x</i><sup>2</sup> − <i>x</i> − 2 factored?", "(3<i>x</i> − 2)(2<i>x</i> + 1)", ["(3<i>x</i> + 2)(2<i>x</i> − 1)", "(6<i>x</i> − 2)(<i>x</i> + 1)", "(3<i>x</i> − 1)(2<i>x</i> + 2)"], "<i>ac</i> = −12: −4 and 3. 6<i>x</i><sup>2</sup> − 4<i>x</i> + 3<i>x</i> − 2 = <b>(3<i>x</i> − 2)(2<i>x</i> + 1)</b>."),
        ("A rectangular garden has area <i>x</i><sup>2</sup> + 2<i>x</i> − 15 m². Which could be its dimensions?", "(<i>x</i> + 5) m by (<i>x</i> − 3) m", ["(<i>x</i> − 5) m by (<i>x</i> + 3) m", "(<i>x</i> + 15) m by (<i>x</i> − 1) m", "(<i>x</i> + 2) m by (<i>x</i> − 15) m"], "5 × (−3) = −15 and 5 + (−3) = 2: <b>(<i>x</i> + 5)(<i>x</i> − 3)</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p><b>Always take out the greatest common factor (GCF) first.</b> Then look at what is left:</p>"
        "<ul><li><i>x</i><sup>2</sup> + <i>bx</i> + <i>c</i>: find two numbers that <b>multiply to <i>c</i></b> and <b>add to <i>b</i></b>.</li>"
        "<li><i>ax</i><sup>2</sup> + <i>bx</i> + <i>c</i>: find two numbers that multiply to <i>ac</i> and add to <i>b</i>, split the middle term and group.</li>"
        "<li><i>A</i><sup>2</sup> − <i>B</i><sup>2</sup> = (<i>A</i> − <i>B</i>)(<i>A</i> + <i>B</i>); <i>A</i><sup>2</sup> ± 2<i>AB</i> + <i>B</i><sup>2</sup> = (<i>A</i> ± <i>B</i>)<sup>2</sup>.</li></ul>"
        "<p>Check by multiplying back. A sum of squares like <i>x</i><sup>2</sup> + 9 cannot be factored.</p>",
        [("Factor <i>x</i><sup>2</sup> − 3<i>x</i> − 18.", ["Multiply to −18, add to −3: −6 and 3."], "(<i>x</i> − 6)(<i>x</i> + 3)"),
         ("Factor 3<i>x</i><sup>2</sup> + 10<i>x</i> + 8.", ["<i>ac</i> = 24: 6 and 4.", "3<i>x</i><sup>2</sup> + 6<i>x</i> + 4<i>x</i> + 8 = 3<i>x</i>(<i>x</i> + 2) + 4(<i>x</i> + 2)."], "(3<i>x</i> + 4)(<i>x</i> + 2)"),
         ("Factor completely 2<i>x</i><sup>2</sup> − 50.", ["GCF 2: 2(<i>x</i><sup>2</sup> − 25).", "Difference of squares."], "2(<i>x</i> − 5)(<i>x</i> + 5)")],
        ["Taking out a common factor that is not the greatest: 12<i>x</i> + 18 = 6(2<i>x</i> + 3), not 2(6<i>x</i> + 9).",
         "Choosing numbers that multiply to <i>c</i> but do not add to <i>b</i>.",
         "Sign errors when <i>c</i> is negative: one number must be positive and one negative.",
         "Stopping too early: 2<i>x</i><sup>2</sup> − 50 = 2(<i>x</i><sup>2</sup> − 25) still factors."])


def main():
    sets = [S("Greatest common factor", collect(one_gcf, 20, R)),
            S("Factor x² + bx + c", collect(one_simple, 20, R)),
            S("Factor ax² + bx + c", collect(one_ac, 20, R)),
            S("Difference of squares and perfect squares", collect(one_special, 20, R)),
            S("Factor completely and apply", collect(one_complete, 8, R) + problems()[:12])]
    make("factoring-polynomials", 15, "A-SSE.A.2",
         "Factoring Polynomials: GCF, Trinomials and Special Patterns",
         "Algebra 1 Factoring Worksheets: GCF, Trinomials, Difference of Squares and Perfect Squares (Free, Answer Key)",
         "Factoring polynomials",
         "Use the structure of an expression to identify ways to rewrite it. For example, see x⁴ − y⁴ as (x²)² − (y²)², thus recognizing it as "
         "a difference of squares that can be factored as (x² − y²)(x² + y²).",
         "Free Algebra 1 factoring worksheets (A-SSE.A.2): greatest common factor, factoring x² + bx + c and ax² + bx + c, difference of "
         "squares, perfect square trinomials and factoring completely. 100 questions with an answer key.",
         "Take out the GCF first. Then find two numbers that multiply to c and add to b.",
         "A² − B² = (A − B)(A + B). Check every answer by multiplying back.",
         body(),
         [("How do you factor x² + bx + c?", "Find two numbers that multiply to c and add to b. If they are p and q, the factored form is (x + p)(x + q)."),
          ("How do you factor when the leading coefficient is not 1?", "Use the AC method: multiply a and c, find two numbers that multiply to ac and add to b, split the middle term and factor by grouping."),
          ("What is a difference of squares?", "An expression like A² − B². It factors as (A − B)(A + B), for example x² − 49 = (x − 7)(x + 7)."),
          ("What does factor completely mean?", "Keep factoring until no factor can be broken down further, always starting with the greatest common factor.")],
         sets, R, domain="Polynomials & Factoring")


if __name__ == "__main__":
    main()
