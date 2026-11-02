# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Equivalent Expressions (6.EE.A.3, 6.EE.A.4)
  python tools/gen_us_math_g6_equivalent_expressions.py
HTML attributes use single quotes (no backslashes in the JSON).
Every expression is written once in a plain form (3(2 + x), 4x^2, 7y - 21), turned into HTML
(italic letters, <sup> exponents, real minus sign) and parsed into a polynomial, so every
"equivalent" answer is checked in code and every wrong answer is checked to be NOT equivalent.
Wrong answers come from real mistakes: distributing to the first term only, combining unlike terms,
x · x = 2x, 4a + 2a = 6a^2 or 8a, dividing only one term when factoring, a common factor that is not the GCF.
"""
import json, os, random, re
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2f6fb0"
FILL1 = "#e8f3ec"
FILL2 = "#e6eef8"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
MINUS = "−"


# ------------------------------------------------------------ polynomial engine
def p_add(a, b, k=1):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + k * c
    return {m: c for m, c in out.items() if c != 0}


def p_mul(a, b):
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(sorted(m1 + m2))
            out[m] = out.get(m, 0) + c1 * c2
    return {m: c for m, c in out.items() if c != 0}


TOK = re.compile(r"\d[\d,]*(?:\.\d+)?|[a-z]|\^\d+|[+\-−×·()]")


def parse(s):
    """Plain expression -> polynomial {('x', 'x'): 4, (): 3}. Implicit multiplication: 3x, 3(x + 1), x(2)."""
    toks = TOK.findall(s)
    assert "".join(toks) == s.replace(" ", ""), s
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def factor():
        t = take()
        if t[0].isdigit():
            p = {(): Fraction(t.replace(",", ""))}
        elif t.isalpha():
            p = {(t,): Fraction(1)}
        elif t == "(":
            p = expr()
            assert take() == ")", s
        else:
            raise ValueError((s, t))
        while peek() and peek()[0] == "^":
            n = int(take()[1:])
            q = {(): Fraction(1)}
            for _ in range(n):
                q = p_mul(q, p)
            p = q
        return p

    def term():
        p = factor()
        while peek() and (peek() in "×·" or peek()[0].isdigit() or peek().isalpha() or peek() == "("):
            if peek() in "×·":
                take()
            p = p_mul(p, factor())
        return p

    def expr():
        neg = False
        if peek() in ("-", MINUS):
            take()
            neg = True
        p = term()
        if neg:
            p = p_mul(p, {(): Fraction(-1)})
        while peek() and peek() in ("+", "-", MINUS):
            op = take()
            p = p_add(p, term(), 1 if op == "+" else -1)
        return p

    p = expr()
    assert pos[0] == len(toks), s
    return p


def same(a, b):
    return parse(a) == parse(b)


def value(s, **v):
    tot = Fraction(0)
    for m, c in parse(s).items():
        t = c
        for x in m:
            t *= v[x]
        tot += t
    return tot


def H(s):
    """Plain -> HTML: italic letters, <sup> exponents, the real minus sign."""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isalpha() and ch.islower() and (i == 0 or not s[i - 1].isalpha()) and (i + 1 == len(s) or not s[i + 1].isalpha()):
            out.append("<i>%s</i>" % ch)
        elif ch == "^":
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            out.append("<sup>%s</sup>" % s[i + 1:j])
            i = j
            continue
        elif ch == "-":
            out.append(MINUS)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def B(s):
    return "<b>%s</b>" % H(s)


def num(n):
    return "{:,}".format(int(n))


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    correct = str(correct)
    seen, pick = {correct}, []
    for c in cands:
        c = str(c)
        if c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def emcq(q, good, bad, e, equal_to=None):
    """Expression choices (plain form). good must equal equal_to; no two choices are equivalent."""
    if equal_to is not None:
        assert same(good, equal_to), (good, equal_to)
    ps = [parse(x) for x in [good] + bad]
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            assert ps[i] != ps[j], (q, ([good] + bad)[i], ([good] + bad)[j])
    return mcq(q, H(good), [H(b) for b in bad], e)


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            rest = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(rest)
            rest.insert(t, c[it["a"]])
            it["c"] = rest
            it["a"] = t


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def S(s):
    """Plain -> SVG text: italic letters as tspans, the real minus sign."""
    out = []
    for i, ch in enumerate(s):
        if ch.isalpha():
            out.append("<tspan font-style='italic'>%s</tspan>" % ch)
        elif ch == "-":
            out.append(MINUS)
        else:
            out.append(ch)
    return "".join(out)


def label_text(s):
    """Aria-label text: plain letters, real minus sign."""
    return s.replace("-", MINUS)


def txt(x, y, t, fs=17, col=INK, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, S(t)))


def tw(t, fs):
    return len(t) * fs * 0.6


def area_svg(h, parts, inside=None, hlabel=None):
    """Area model: a rectangle of height h split into parts [(label, width_px)].
    Lengths above each part, the height on the left, optional area text inside each part."""
    hl = hlabel if hlabel is not None else str(h)
    LP = int(tw(hl, 18)) + 16
    TP = 30
    RH = 76
    x = LP
    out = []
    fills = [FILL1, FILL2]
    cols = [GREEN, BLUE]
    for i, (lab, w) in enumerate(parts):
        out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                   % (x, TP, w, RH, fills[i], INK))
        out.append(txt(x + w / 2, TP - 9, lab, 18, cols[i]))
        if inside:
            out.append(txt(x + w / 2, TP + RH / 2 + 6, inside[i], 17, cols[i]))
        x += w
    out.append(txt(LP - 8, TP + RH / 2 + 6, hl, 18, INK, "end"))
    W, Hh = x + 6, TP + RH + 6
    lab = "area model: a rectangle %s tall split into parts %s long" % (
        label_text(hl), " and ".join(label_text(p[0]) for p in parts))
    return svg_wrap(W, Hh, "".join(out), lab)


def rect_svg(w, h, top, left, label):
    """Rectangle w by h px; labels outside the top side and left side."""
    LP = int(tw(left, 17)) + 14
    TP = 28
    out = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (LP, TP, w, h, FILL1, GREEN),
           txt(LP + w / 2, TP - 9, top),
           txt(LP - 7, TP + h / 2 + 6, left, 17, INK, "end")]
    W = max(LP + w + 6, int(LP + w / 2 + tw(top, 17) / 2) + 4)
    return svg_wrap(W, TP + h + 6, "".join(out), label)


def tri_svg(side, label):
    """Equilateral triangle with the same label on all three sides."""
    s = 120
    hgt = s * 0.866
    lw = tw(side, 17)
    LP = int(lw) + 12
    x0, y0 = LP, 10 + hgt
    pts = [(x0, y0), (x0 + s, y0), (x0 + s / 2, y0 - hgt)]
    out = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.5'/>"
           % (" ".join("%.1f,%.1f" % p for p in pts), FILL1, GREEN),
           txt(x0 + s / 2, y0 + 22, side),
           txt(x0 + s / 4 - 8, y0 - hgt / 2 + 4, side, 17, INK, "end"),
           txt(x0 + 3 * s / 4 + 8, y0 - hgt / 2 + 4, side, 17, INK, "start")]
    W = int(x0 + 3 * s / 4 + 8 + lw) + 6
    return svg_wrap(W, int(y0 + 30), "".join(out), label)


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ set 1: combine like terms
def set_like_terms(rnd, P):
    its = []
    SIMP = ["Simplify %s.", "Which expression is equivalent to %s?", "Combine like terms: %s.", "Write %s in simplest form."]
    k = [0]

    def ask(s):
        k[0] += 1
        return SIMP[k[0] % len(SIMP)] % B(s)

    # repeated addition
    for s, good, bad, e in [
        ("y + y + y", "3y", ["y^3", "3 + y", "2y"],
         "There are 3 <i>y</i>’s added together, so <i>y</i> + <i>y</i> + <i>y</i> = 3<i>y</i>. Not 2<i>y</i>: count the <i>y</i>’s, not the + signs. <i>y</i><sup>3</sup> would mean <i>y</i> · <i>y</i> · <i>y</i>."),
        ("m + m + m + m", "4m", ["m^4", "4 + m", "3m"],
         "4 <i>m</i>’s added together make 4<i>m</i>. Not <i>m</i><sup>4</sup>: that means <i>m</i> · <i>m</i> · <i>m</i> · <i>m</i>, which is multiplying, not adding."),
        ("x + x", "2x", ["x^2", "2 + x", "2x^2"],
         "<i>x</i> + <i>x</i> is 2 <i>x</i>’s, so it is 2<i>x</i>. Not <i>x</i><sup>2</sup>: that is <i>x</i> · <i>x</i>."),
        ("a + a + a + 5", "3a + 5", ["8a", "a^3 + 5", "a + 8"],
         "The 3 <i>a</i>’s make 3<i>a</i>. The 5 is not a like term, so it stays: 3<i>a</i> + 5. Not 8<i>a</i>: 5 has no <i>a</i>, so it cannot join the <i>a</i>-terms."),
    ]:
        its.append(emcq(ask(s), good, bad, e, s))
    # ax + bx and ax - bx
    for s, good, bad in [("4a + 2a", "6a", ["6a^2", "8a", "6"]),
                         ("5x + 3x", "8x", ["8x^2", "15x", "8"]),
                         ("x + 4x", "5x", ["4x", "5x^2", "4x^2"]),
                         ("9b - 3b", "6b", ["12b", "6", "27b"]),
                         ("7n + n - 2n", "6n", ["5n", "6n^2", "10n"])]:
        cs = [c for m, c in parse(s).items()]
        e = {"4a + 2a": "Add the coefficients and keep the variable: 4 + 2 = 6, so 4<i>a</i> + 2<i>a</i> = 6<i>a</i>. Not 6<i>a</i><sup>2</sup>: adding does not change <i>a</i> into <i>a</i><sup>2</sup>. Not 8<i>a</i>: add 4 and 2, do not multiply.",
             "5x + 3x": "5 <i>x</i>’s and 3 more <i>x</i>’s are 8 <i>x</i>’s: 5<i>x</i> + 3<i>x</i> = 8<i>x</i>. Not 15<i>x</i>: the coefficients are added, not multiplied.",
             "x + 4x": "<i>x</i> means 1<i>x</i>. So <i>x</i> + 4<i>x</i> = 1<i>x</i> + 4<i>x</i> = 5<i>x</i>. Not 4<i>x</i>: the <i>x</i> in front counts as 1.",
             "9b - 3b": "Subtract the coefficients: 9 − 3 = 6, so 9<i>b</i> − 3<i>b</i> = 6<i>b</i>. Not 12<i>b</i>: that adds instead of subtracting. Not 6: the <i>b</i> stays.",
             "7n + n - 2n": "<i>n</i> means 1<i>n</i>: 7 + 1 − 2 = 6, so the expression is 6<i>n</i>. Not 5<i>n</i>: the <i>n</i> in the middle counts as 1."}[s]
        its.append(emcq(ask(s), good, bad, e, s))
    # ax + b + cx: the number does not join the x-terms
    for a, b, c in [(5, 3, 2), (2, 9, 6), (4, 1, 3)]:
        s = "%dx + %d + %dx" % (a, b, c)
        good = "%dx + %d" % (a + c, b)
        bad = ["%dx" % (a + b + c), "%dx + %d" % (a, b + c), "%dx^2 + %d" % (a + c, b)]
        e = ("The like terms are %s and %s: %d + %d = %d, so %s = %s. "
             "%s is a constant term, not an <i>x</i>-term, so it stays as it is. Not %s: %s and %s are not like terms."
             % (H("%dx" % a), H("%dx" % c), a, c, a + c, H(s), H(good), b, H(bad[0]), H("%dx" % a), b))
        its.append(emcq(ask(s), good, bad, e, s))
    # ax + b - cx + d
    for a, b, c, d in [(6, 4, 2, 1), (9, 7, 5, 3), (8, 6, 3, 2)]:
        s = "%dn + %d - %dn + %d" % (a, b, c, d)
        good = "%dn + %d" % (a - c, b + d)
        bad = ["%dn + %d" % (a + c, b + d), "%dn" % (a + b - c + d), "%dn + %d" % (a - c, abs(b - d))]
        assert b != d
        e = ("Group the like terms: (%s) + (%d + %d) = %s. The minus sign belongs to %s, so subtract it. "
             "Not %s: that adds %s." % (H("%dn - %dn" % (a, c)), b, d, H(good), H("%dn" % c), H(bad[0]), H("%dn" % c)))
        its.append(emcq(ask(s), good, bad, e, s))
    # two variables
    for s, good, bad, e in [
        ("3x + 2y + x + 4y", "4x + 6y", ["10xy", "3x + 6y", "4x^2 + 6y^2"],
         "Combine the <i>x</i>-terms and the <i>y</i>-terms separately: 3<i>x</i> + <i>x</i> = 4<i>x</i> and 2<i>y</i> + 4<i>y</i> = 6<i>y</i>. "
         "4<i>x</i> and 6<i>y</i> are not like terms, so the answer is 4<i>x</i> + 6<i>y</i>, not 10<i>xy</i>."),
        ("5a + 2b + 3a + b", "8a + 3b", ["13ab", "8a + 2b", "15a + 2b"],
         "<i>a</i>-terms: 5<i>a</i> + 3<i>a</i> = 8<i>a</i>. <i>b</i>-terms: 2<i>b</i> + <i>b</i> = 3<i>b</i> (<i>b</i> is 1<i>b</i>). "
         "So the expression is 8<i>a</i> + 3<i>b</i>. Not 8<i>a</i> + 2<i>b</i>: the lone <i>b</i> counts as 1."),
    ]:
        its.append(emcq(ask(s), good, bad, e, s))
    # like terms
    its.append(mcq("Which two terms are like terms?", "%s and %s" % (H("4x"), H("9x")),
                   ["%s and %s" % (H("4x"), H("4y")), "%s and %s" % (H("4x"), H("x^2")), "%s and %s" % (H("4x"), "4")],
                   "Like terms have the same variable part. 4<i>x</i> and 9<i>x</i> both have just <i>x</i>. "
                   "4<i>x</i> and 4<i>y</i> share the number 4, but the variables are different."))
    its.append(mcq("Which two terms are like terms?", "%s and %s" % (H("3a^2"), H("5a^2")),
                   ["%s and %s" % (H("3a^2"), H("3a")), "%s and %s" % (H("a^2"), H("2a")), "%s and %s" % (H("5a"), "5")],
                   "3<i>a</i><sup>2</sup> and 5<i>a</i><sup>2</sup> both have <i>a</i><sup>2</sup>, so they are like terms. "
                   "<i>a</i><sup>2</sup> and <i>a</i> are different: <i>a</i><sup>2</sup> = <i>a</i> · <i>a</i>."))
    # x · x
    its.append(emcq("Which expression is equivalent to %s?" % B("x · x"), "x^2", ["2x", "2x^2", "2 + x"],
                    "<i>x</i> · <i>x</i> means <i>x</i> times itself, which is <i>x</i><sup>2</sup>. "
                    "2<i>x</i> means <i>x</i> + <i>x</i>. For example, when <i>x</i> = 5: 5 · 5 = 25, but 2 · 5 = 10.", "x · x"))
    assert len(its) == 20, len(its)
    return {"title": "Combine like terms", "items": its}


# ------------------------------------------------------------ set 2: the distributive property (expand)
def set_expand(rnd, P):
    its = []
    ASK = ["Use the distributive property to expand %s.", "Which expression is equivalent to %s?",
           "Expand %s.", "Which expression is equal to %s for every value of the variable?"]
    k = [0]

    def ask(s):
        k[0] += 1
        return ASK[k[0] % len(ASK)] % B(s)

    def dist_e(s, k_, terms, good, first_only):
        parts = " + ".join("%d × %s" % (k_, H(t)) for t in terms)
        return ("Multiply %d by <b>each</b> term inside the parentheses: %s = %s. Not %s: the %d must multiply both terms."
                % (k_, parts.replace("+ %d × %s" % (k_, MINUS), "−"), H(good), H(first_only), k_))

    # k(b + x)
    for kk, b, v in [(3, 2, "x"), (5, 4, "y"), (7, 3, "a"), (4, 9, "m")]:
        s = "%d(%d + %s)" % (kk, b, v)
        good = "%d + %d%s" % (kk * b, kk, v)
        bad = ["%d + %s" % (kk * b, v), "%d + %d%s" % (b, kk, v), "%d%s" % (kk * b + kk, v)]
        e = ("Multiply %d by each term: %d × %d = %d and %d × %s = %s. So %s = %s. "
             "Not %s: the %d must multiply the %s too. Not %s: %d and %s are not like terms."
             % (kk, kk, b, kk * b, kk, H(v), H("%d%s" % (kk, v)), H(s), H(good), H(bad[0]), kk, H(v), H(bad[2]), kk * b, H("%d%s" % (kk, v))))
        its.append(emcq(ask(s), good, bad, e, s))
    # k(x + b)
    for kk, b, v in [(4, 5, "x"), (6, 3, "n"), (8, 2, "b")]:
        s = "%d(%s + %d)" % (kk, v, b)
        good = "%d%s + %d" % (kk, v, kk * b)
        bad = ["%d%s + %d" % (kk, v, b), "%s + %d" % (v, kk * b), "%d%s" % (kk + kk * b, v)]
        e = ("%d × %s = %s and %d × %d = %d, so %s = %s. Not %s: that multiplies only the first term."
             % (kk, H(v), H("%d%s" % (kk, v)), kk, b, kk * b, H(s), H(good), H(bad[0])))
        its.append(emcq(ask(s), good, bad, e, s))
    # k(x - b)
    for kk, b, v in [(6, 2, "x"), (3, 7, "y"), (9, 4, "k")]:
        s = "%d(%s - %d)" % (kk, v, b)
        good = "%d%s - %d" % (kk, v, kk * b)
        bad = ["%d%s - %d" % (kk, v, b), "%d%s + %d" % (kk, v, kk * b), "%s - %d" % (v, kk * b)]
        e = ("%d × %s = %s and %d × %d = %d. The minus sign stays: %s = %s. Not %s: the %d must also multiply the %d."
             % (kk, H(v), H("%d%s" % (kk, v)), kk, b, kk * b, H(s), H(good), H(bad[0]), kk, b))
        its.append(emcq(ask(s), good, bad, e, s))
    # k(ax + b)
    for kk, a, b in [(5, 2, 3), (2, 4, 7), (3, 5, 1)]:
        s = "%d(%dx + %d)" % (kk, a, b)
        good = "%dx + %d" % (kk * a, kk * b)
        bad = ["%dx + %d" % (kk * a, b), "%dx + %d" % (kk + a, kk + b), "%dx" % (kk * a + kk * b)]
        if b == 1:
            s = "%d(%dx + 1)" % (kk, a)
            good = "%dx + %d" % (kk * a, kk)
            bad = ["%dx + 1" % (kk * a), "%dx + %d" % (kk + a, kk + 1), "%dx" % (kk * a + kk)]
        e = ("%d × %s = %s and %d × %d = %d, so %s = %s. Not %s: multiply, do not add, the %d and the coefficients."
             % (kk, H("%dx" % a), H("%dx" % (kk * a)), kk, b, kk * b, H(s), H(good), H(bad[1]), kk))
        its.append(emcq(ask(s), good, bad, e, s))
    # two variables
    for kk, a, b in [(2, 3, 4), (5, 2, 3)]:
        s = "%d(%da + %db)" % (kk, a, b)
        good = "%da + %db" % (kk * a, kk * b)
        bad = ["%da + %db" % (kk * a, b), "%da + %db" % (kk + a, kk + b), "%dab" % (kk * a + kk * b)]
        e = ("%d × %s = %s and %d × %s = %s, so %s = %s. %s and %s are not like terms, so they cannot be combined."
             % (kk, H("%da" % a), H("%da" % (kk * a)), kk, H("%db" % b), H("%db" % (kk * b)), H(s), H(good),
                H("%da" % (kk * a)), H("%db" % (kk * b))))
        its.append(emcq(ask(s), good, bad, e, s))
    # area models
    its.append(emcq(fig(area_svg(4, [("x", 120), ("3", 54)])) +
                    "The area model shows %s. Which expression is equivalent?" % B("4(x + 3)"),
                    "4x + 12", ["4x + 3", "x + 12", "4x + 7"],
                    "The two parts have areas 4 × <i>x</i> = 4<i>x</i> and 4 × 3 = 12. The total area is 4<i>x</i> + 12. "
                    "Not 4<i>x</i> + 3: the 3 is a length, but the part’s area is 4 × 3.", "4(x + 3)"))
    its.append(emcq(fig(area_svg(6, [("y", 120), ("5", 70)])) +
                    "Write the area of the whole rectangle as a sum of the areas of the two parts.",
                    "6y + 30", ["6y + 5", "y + 30", "11y"],
                    "Left part: 6 × <i>y</i> = 6<i>y</i>. Right part: 6 × 5 = 30. Whole rectangle: 6<i>y</i> + 30, which equals 6(<i>y</i> + 5).",
                    "6(y + 5)"))
    its.append(emcq(fig(area_svg(5, [("?", 120), ("?", 60)], inside=["5x", "15"])) +
                    "The two parts have areas %s and 15. Which product gives the area of the whole rectangle?" % B("5x"),
                    "5(x + 3)", ["5(x + 15)", "5(5x + 15)", "15x"],
                    "The height is 5. The lengths are 5<i>x</i> ÷ 5 = <i>x</i> and 15 ÷ 5 = 3. "
                    "So the area is 5(<i>x</i> + 3) = 5<i>x</i> + 15. Not 5(<i>x</i> + 15): that would make the second part 75.",
                    "5x + 15"))
    # distribute, then combine
    its.append(emcq(ask("2(x + 4) + 3x"), "5x + 8", ["5x + 4", "13x", "5x^2 + 8"],
                    "First distribute: 2(<i>x</i> + 4) = 2<i>x</i> + 8. Then combine like terms: 2<i>x</i> + 8 + 3<i>x</i> = 5<i>x</i> + 8. "
                    "Not 5<i>x</i> + 4: the 2 must multiply the 4 too.", "2(x + 4) + 3x"))
    its.append(emcq(ask("3(y + 2) + 4"), "3y + 10", ["3y + 6", "3y + 18", "13y"],
                    "First distribute: 3(<i>y</i> + 2) = 3<i>y</i> + 6. Then add the numbers: 6 + 4 = 10, so the answer is 3<i>y</i> + 10. "
                    "Not 3<i>y</i> + 6: that multiplies only the <i>y</i>. Not 3<i>y</i> + 18: the 4 is outside the parentheses, so it is not multiplied.",
                    "3(y + 2) + 4"))
    assert len(its) == 20, len(its)
    return {"title": "The distributive property: expand", "items": its}


# ------------------------------------------------------------ set 3: factor with the GCF
def gcf_of(*ns):
    g = 0
    for n in ns:
        g = gcd(g, n)
    return g


def set_factor(rnd, P):
    its = []
    ASK = ["Factor %s using the greatest common factor (GCF).", "Use the GCF to write %s as a product.",
           "Factor out the GCF: %s.", "Which expression shows %s factored with the GCF?"]
    k = [0]

    def ask(s):
        k[0] += 1
        return ASK[k[0] % len(ASK)] % B(s)

    def fac(s, good, bad, e):
        coefs = [int(c) for c in parse(s).values()]
        g = gcf_of(*coefs)
        inner = parse(good.split("(", 1)[1].rsplit(")", 1)[0])
        assert int(good.split("(")[0]) == g, (s, good, g)
        assert gcf_of(*[int(c) for c in inner.values()]) == 1, good
        its.append(emcq(ask(s), good, bad, e, s))

    # two terms, one variable
    for s, good, bad, gg in [
        ("12x + 8", "4(3x + 2)", ["4(3x + 8)", "4(12x + 2)", "4x(3 + 2)"], 4),
        ("6 + 3x", "3(2 + x)", ["3(2 + 3x)", "3(6 + x)", "3x(2 + 1)"], 3),
        ("15y + 20", "5(3y + 4)", ["5(3y + 20)", "5(15y + 4)", "5y(3 + 4)"], 5),
        ("7y - 21", "7(y - 3)", ["7(y - 21)", "7(y + 3)", "7y(1 - 3)"], 7),
        ("18a - 12", "6(3a - 2)", ["6(3a - 12)", "6(18a - 2)", "6a(3 - 2)"], 6),
        ("16 + 40m", "8(2 + 5m)", ["8(2 + 40m)", "8(16 + 5m)", "8m(2 + 5)"], 8),
    ]:
        a, b = [abs(int(c)) for c in parse(s).values()]
        e = ("The GCF of %d and %d is %d. Divide each term by %d: %s. Check by distributing: %s = %s. "
             "Not %s: <b>both</b> terms must be divided by %d."
             % (a, b, gg, gg, ", ".join("%s ÷ %d = %s" % (H(t), gg, H(r)) for t, r in zip(terms_of(s), terms_of(inner_of(good)))),
                H(good), H(s), H(bad[0]), gg))
        fac(s, good, bad, e)
    # two variables
    for s, good, bad in [
        ("24x + 18y", "6(4x + 3y)", ["6(4x + 18y)", "6x(4 + 3y)", "6(3x + 4y)"]),
        ("10a + 15b", "5(2a + 3b)", ["5(2a + 15b)", "5a(2 + 3b)", "5(3a + 2b)"]),
        ("36m + 27n", "9(4m + 3n)", ["9(4m + 27n)", "9m(4 + 3n)", "9(3m + 4n)"]),
    ]:
        g = gcf_of(*[int(c) for c in parse(s).values()])
        e = ("The GCF of the coefficients is %d. %s, so %s = %s. "
             "Not %s: the %s is only in the first term, so it cannot be factored out of both."
             % (g, ", ".join("%s ÷ %d = %s" % (H(t), g, H(r)) for t, r in zip(terms_of(s), terms_of(inner_of(good)))),
                H(s), H(good), H(bad[1]), "<i>%s</i>" % [c for c in s if c.isalpha()][0]))
        fac(s, good, bad, e)
    # GCF of the terms (number answers)
    for s, g, bad, why in [("20a + 30", 10, [5, 2, 60], "60 is the least common multiple, not the greatest common factor."),
                           ("16x + 24", 8, [4, 2, 48], "4 is a common factor, but 8 is greater."),
                           ("27y - 18", 9, [3, 6, 54], "3 is a common factor, but 9 is greater. 6 is not a factor of 27."),
                           ("14m + 35n", 7, [5, 14, 70], "5 is not a factor of 14, and 14 is not a factor of 35.")]:
        cs = [abs(int(c)) for c in parse(s).values()]
        assert gcf_of(*cs) == g and all(gcf_of(*cs) != b for b in bad)
        its.append(mcq("What is the greatest common factor (GCF) of the terms in %s?" % B(s), str(g), [str(b) for b in bad],
                       "Factors of %d and %d: the greatest number that divides both is %d. %s So %s = %s."
                       % (cs[0], cs[1], g, why, H(s), H(gcf_form(s)))))
    # missing piece
    for q, good, bad, full, e in [
        ("12x + 20 = 4(3x + ?)", "5", ["20", "16", "8"], "4(3x + 5)",
         "20 ÷ 4 = 5, so 12<i>x</i> + 20 = 4(3<i>x</i> + 5). Check: 4 × 5 = 20. Not 16: divide 20 by 4, do not subtract 4."),
        ("30y + 18 = ?(5y + 3)", "6", ["3", "30", "18"], "6(5y + 3)",
         "30<i>y</i> ÷ 5<i>y</i> = 6 and 18 ÷ 3 = 6, so the factor is 6. Check: 6(5<i>y</i> + 3) = 30<i>y</i> + 18."),
        ("8x + 28 = 4(? + 7)", "2x", ["8x", "2", "4x"], "4(2x + 7)",
         "8<i>x</i> ÷ 4 = 2<i>x</i>, so 8<i>x</i> + 28 = 4(2<i>x</i> + 7). Not 2: the <i>x</i> must stay in the term."),
        ("45a - 35 = 5(9a - ?)", "7", ["35", "30", "8"], "5(9a - 7)",
         "35 ÷ 5 = 7, so 45<i>a</i> − 35 = 5(9<i>a</i> − 7). Check: 5 × 7 = 35."),
    ]:
        lhs = q.split(" = ")[0]
        assert same(lhs, full)
        for b in bad:
            assert not same(lhs, full.replace(good if good in full else "§", b, 1)) or b == good
        its.append(mcq("What goes in the box?<br>%s" % B(q), H(good),
                       [H(b) for b in bad], e))
    # coefficient 1 inside
    its.append(emcq(ask("5x + 5"), "5(x + 1)", ["5x", "5(x + 5)", "10x"],
                    "Both terms have a factor of 5. 5<i>x</i> ÷ 5 = <i>x</i> and 5 ÷ 5 = 1, so 5<i>x</i> + 5 = 5(<i>x</i> + 1). "
                    "Do not forget the 1: 5 · 1 = 5.", "5x + 5"))
    its.append(emcq(ask("9 + 9y"), "9(1 + y)", ["9y", "9(9 + y)", "18y"],
                    "9 ÷ 9 = 1 and 9<i>y</i> ÷ 9 = <i>y</i>, so 9 + 9<i>y</i> = 9(1 + <i>y</i>). "
                    "Not 9<i>y</i>: that leaves out the 9 that was added.", "9 + 9y"))
    # three terms
    its.append(emcq(ask("6x + 9y + 12"), "3(2x + 3y + 4)", ["3(2x + 3y + 12)", "3(2x + 9y + 4)", "6(x + 3y + 2)"],
                    "The GCF of 6, 9 and 12 is 3. Divide each term by 3: 2<i>x</i>, 3<i>y</i> and 4. "
                    "So 6<i>x</i> + 9<i>y</i> + 12 = 3(2<i>x</i> + 3<i>y</i> + 4). 6 is not a factor of 9.", "6x + 9y + 12"))
    assert len(its) == 20, len(its)
    return {"title": "Factor using the GCF", "items": its}


def terms_of(s):
    """'12x + 8' -> ['12x', '8'] ; '7y - 21' -> ['7y', '21'] (signs dropped)."""
    return [t.strip() for t in re.split(r"[+\-−]", s) if t.strip()]


def inner_of(s):
    return s.split("(", 1)[1].rsplit(")", 1)[0]


def gcf_form(s):
    p = parse(s)
    g = gcf_of(*[abs(int(c)) for c in p.values()])
    out = []
    for t, (m, c) in zip(re.findall(r"[+\-]?\s*[^+\-]+", s), p.items()):
        pass
    parts = re.split(r"\s([+\-])\s", s)
    res = []
    for i, t in enumerate(parts):
        if i % 2:
            res.append(" %s " % t)
        else:
            mm = re.match(r"(\d+)([a-z]*)", t)
            n = int(mm.group(1)) // g
            res.append(("%d" % n if (n != 1 or not mm.group(2)) else "") + mm.group(2))
    f = "%d(%s)" % (g, "".join(res))
    assert same(f, s), (f, s)
    return f


# ------------------------------------------------------------ set 4: are they equivalent?
def set_equivalent(rnd, P):
    its = []
    # substitute a value
    for e1, e2, v, var, w2 in [("3(x + 4)", "3x + 4", 2, "x", 36), ("2(y + 5)", "2y + 5", 3, "y", 28),
                               ("4a + 2a", "6a^2", 2, "a", 144), ("5(n - 1)", "5n - 1", 4, "n", 53)]:
        n, pr, po = P.next()
        x1, x2 = value(e1, **{var: v}), value(e2, **{var: v})
        assert x1 != x2
        good = "%s and %s, so they are not equivalent" % (num(x1), num(x2))
        bad = ["%s and %s, so they are equivalent" % (num(x1), num(x1)),
               "%s and %s, so they are equivalent" % (num(x2), num(x2))]
        assert w2 not in (x1, x2)
        bad.append("%s and %s, so they are not equivalent" % (num(x1), num(w2)))
        c = int(e2[0])
        if "^" in e2:
            assert w2 == (c * v) ** 2
            note = "With <i>%s</i> = %d, %s means %d × %d<sup>2</sup>, not (%d × %d)<sup>2</sup> = %s." % (var, v, H(e2), c, v, c, v, num(w2))
        else:
            assert w2 == value(e2.replace(var, "", 1).replace(str(c), str(c * 10 + v), 1), **{var: v})
            note = "With <i>%s</i> = %d, %s is %d × %d = %d, not %d%d." % (var, v, H("%d%s" % (c, var)), c, v, c * v, c, v)
        e = ("Replace <i>%s</i> with %d in both: %s = %s and %s = %s. The values are different, so the expressions are not equivalent. %s"
             % (var, v, H(sub_show(e1, var, v)), num(x1),
                H(sub_show(e2, var, v)), num(x2), note))
        its.append(mcq("%s checks whether %s and %s are equivalent by substituting <i>%s</i> = %d. What does %s find?"
                       % (n, B(e1), B(e2), var, v, pr), good, bad, e))
    n, pr, po = P.next()
    its.append(mcq("%s says %s and %s are equivalent because both equal 4 when <i>x</i> = 2. Is %s right?" % (n, B("2x"), B("x^2"), pr),
                   "No. When <i>x</i> = 3, they are 6 and 9.",
                   ["Yes. They are equal when <i>x</i> = 2.", "Yes. Both have one <i>x</i> and a 2.", "No. They are never equal."],
                   "Equivalent expressions are equal for <b>every</b> value. 2<i>x</i> and <i>x</i><sup>2</sup> match when <i>x</i> = 2, "
                   "but when <i>x</i> = 3, 2 · 3 = 6 and 3 · 3 = 9. So they are not equivalent."))
    assert value("2x", x=3) == 6 and value("x^2", x=3) == 9 and value("2x", x=2) == value("x^2", x=2) == 4
    # which expression is equivalent (a different form)
    for s, good, bad, e in [
        ("4(x + 2)", "2(2x + 4)", ["4x + 2", "2(2x + 2)", "2x + 8"],
         "4(<i>x</i> + 2) = 4<i>x</i> + 8, and 2(2<i>x</i> + 4) = 4<i>x</i> + 8 too. Both are 4<i>x</i> + 8, so they are equivalent."),
        ("12a + 8", "2(6a + 4)", ["4(3a + 8)", "12(a + 8)", "20a"],
         "2(6<i>a</i> + 4) = 12<i>a</i> + 8. It uses a factor of 2, not the GCF 4, but it is still equivalent. "
         "4(3<i>a</i> + 8) = 12<i>a</i> + 32, which is different."),
        ("3(2y + 1) + y", "7y + 3", ["7y + 1", "6y + 4", "10y"],
         "3(2<i>y</i> + 1) = 6<i>y</i> + 3. Add the other <i>y</i>: 6<i>y</i> + 3 + <i>y</i> = 7<i>y</i> + 3."),
        ("x + x + 6", "2(x + 3)", ["x^2 + 6", "2(x + 6)", "8x"],
         "<i>x</i> + <i>x</i> + 6 = 2<i>x</i> + 6 = 2(<i>x</i> + 3). Not <i>x</i><sup>2</sup> + 6: <i>x</i> + <i>x</i> is 2<i>x</i>, not <i>x</i><sup>2</sup>."),
        ("10 - 2x + 4x", "2(5 + x)", ["10 + 6x", "2(5 - x)", "12x"],
         "Combine the <i>x</i>-terms: −2<i>x</i> + 4<i>x</i> = 2<i>x</i>. So the expression is 10 + 2<i>x</i> = 2(5 + <i>x</i>)."),
    ]:
        its.append(emcq("Which expression is equivalent to %s?" % B(s), good, bad, e, s))
    # which pair is equivalent
    for good, bad, e in [
        (("3(x + 2)", "3x + 6"), [("3(x + 2)", "3x + 2"), ("x + x", "x^2"), ("4a + 2a", "6a^2")],
         "3(<i>x</i> + 2) = 3<i>x</i> + 3 · 2 = 3<i>x</i> + 6. The other pairs show common mistakes."),
        (("y + y + y", "3y"), [("y · y · y", "3y"), ("2y + 3", "5y"), ("5(y + 1)", "5y + 1")],
         "<i>y</i> + <i>y</i> + <i>y</i> is 3 <i>y</i>’s, which is 3<i>y</i>. <i>y</i> · <i>y</i> · <i>y</i> is <i>y</i><sup>3</sup>, not 3<i>y</i>."),
        (("8m + 12", "4(2m + 3)"), [("8m + 12", "4(2m + 12)"), ("8m + 12", "20m"), ("8m + 12", "8(m + 12)")],
         "4(2<i>m</i> + 3) = 8<i>m</i> + 12, so this pair is equivalent. 8<i>m</i> and 12 are not like terms, so 20<i>m</i> is wrong."),
    ]:
        assert same(*good)
        for a, b in bad:
            assert not same(a, b)
        its.append(mcq("Which pair of expressions is equivalent?", "%s and %s" % (H(good[0]), H(good[1])),
                       ["%s and %s" % (H(a), H(b)) for a, b in bad], e))
    # which equation is true for every value
    for good, bad, e in [
        ("y + y = 2y", ["y · y = 2y", "2y + 3 = 5y", "3(y + 1) = 3y + 1"],
         "<i>y</i> + <i>y</i> is two <i>y</i>’s, so it always equals 2<i>y</i>. <i>y</i> · <i>y</i> = <i>y</i><sup>2</sup>, not 2<i>y</i>."),
        ("6(a - 2) = 6a - 12", ["6(a - 2) = 6a - 2", "6a - 2a = 4", "a · a = 2a"],
         "Distribute: 6 × <i>a</i> = 6<i>a</i> and 6 × 2 = 12, so 6(<i>a</i> − 2) = 6<i>a</i> − 12 for every value of <i>a</i>."),
    ]:
        l, r = good.split(" = ")
        assert same(l, r)
        for b in bad:
            l, r = b.split(" = ")
            assert not same(l, r)
        its.append(mcq("Which equation is true for every value of the variable?", H(good), [H(b) for b in bad], e))
    # spot the error
    n, pr, po = P.next()
    its.append(mcq("%s wrote %s. What is %s mistake?" % (n, B("5(x + 2) = 5x + 2"), po),
                   "%s did not multiply 2 by 5." % pr.capitalize(),
                   ["%s should have added 5 and <i>x</i>." % pr.capitalize(), "%s should have written 7<i>x</i>." % pr.capitalize(),
                    "There is no mistake."],
                   "The 5 multiplies both terms: 5(<i>x</i> + 2) = 5<i>x</i> + 10, not 5<i>x</i> + 2."))
    n, pr, po = P.next()
    its.append(mcq("%s wrote %s. What is %s mistake?" % (n, B("3x + 2 = 5x"), po),
                   "3<i>x</i> and 2 are not like terms.",
                   ["%s should have written 6<i>x</i>." % pr.capitalize(), "%s should have written 5<i>x</i><sup>2</sup>." % pr.capitalize(),
                    "There is no mistake."],
                   "Only like terms can be combined. 2 has no <i>x</i>, so 3<i>x</i> + 2 is already in simplest form. "
                   "Check with <i>x</i> = 1: 3 + 2 = 5, but with <i>x</i> = 2: 6 + 2 = 8, while 5 · 2 = 10."))
    assert value("3x + 2", x=2) == 8 and value("5x", x=2) == 10
    n, pr, po = P.next()
    its.append(mcq("%s wrote %s. What is %s mistake?" % (n, B("x · x = 2x"), po),
                   "<i>x</i> · <i>x</i> is <i>x</i><sup>2</sup>, not 2<i>x</i>.",
                   ["<i>x</i> · <i>x</i> is <i>x</i>.", "<i>x</i> · <i>x</i> is 2<i>x</i><sup>2</sup>.", "There is no mistake."],
                   "<i>x</i> · <i>x</i> means <i>x</i> times itself, which is <i>x</i><sup>2</sup>. 2<i>x</i> is <i>x</i> + <i>x</i>. "
                   "When <i>x</i> = 4: 4 · 4 = 16, but 2 · 4 = 8."))
    n, pr, po = P.next()
    its.append(mcq("%s was asked to factor %s using the GCF. %s wrote %s. What is wrong?" % (n, B("24x + 18y"), pr.capitalize(), B("3(8x + 6y)")),
                   "3 is not the GCF. The GCF is 6.",
                   ["The two expressions are not equivalent.", "%s should have factored out <i>x</i>." % pr.capitalize(),
                    "There is no mistake."],
                   "3(8<i>x</i> + 6<i>y</i>) is equivalent, but 8 and 6 still share a factor of 2. "
                   "The GCF of 24 and 18 is 6: 24<i>x</i> + 18<i>y</i> = 6(4<i>x</i> + 3<i>y</i>)."))
    assert same("3(8x + 6y)", "24x + 18y") and same("6(4x + 3y)", "24x + 18y")
    n, pr, po = P.next()
    its.append(mcq("%s wrote %s. What is %s mistake?" % (n, B("7(y - 1) = 7y - 7"), po),
                   "There is no mistake.",
                   ["It should be 7<i>y</i> − 1.", "It should be 7<i>y</i> + 7.", "It should be 6<i>y</i>."],
                   "7 × <i>y</i> = 7<i>y</i> and 7 × 1 = 7, and the minus sign stays. So 7(<i>y</i> − 1) = 7<i>y</i> − 7 is correct."))
    assert same("7(y - 1)", "7y - 7")
    assert len(its) == 20, len(its)
    return {"title": "Are the expressions equivalent?", "items": its}


def sub_show(s, var, v):
    """'3x + 4' with x = 2 -> '3 × 2 + 4' ; '6a^2' -> '6 × 2^2'."""
    out = re.sub(r"(\d)%s" % var, lambda m: "%s × %d" % (m.group(1), v), s)
    out = out.replace(var, str(v))
    return out


# ------------------------------------------------------------ set 5: applied problems
def set_applied(rnd, P):
    its = []
    # perimeter
    its.append(emcq(fig(rect_svg(160, 70, "x + 3", "5", "rectangle with sides x + 3 and 5")) +
                    "Which expression gives the perimeter of the rectangle?",
                    "2x + 16", ["2x + 11", "x + 8", "5x + 15"],
                    "Add all four sides: 2(<i>x</i> + 3) + 2 × 5 = 2<i>x</i> + 6 + 10 = 2<i>x</i> + 16. "
                    "Not <i>x</i> + 8: that adds only two sides. Not 5<i>x</i> + 15: that is the area.", "2(x + 3) + 2 × 5"))
    its.append(emcq(fig(rect_svg(100, 100, "y + 2", "y + 2", "square with sides y + 2")) +
                    "The figure is a square. Which expression gives its perimeter?",
                    "4y + 8", ["4y + 2", "y + 8", "8y"],
                    "A square has 4 equal sides: 4(<i>y</i> + 2) = 4<i>y</i> + 8. Not 4<i>y</i> + 2: the 4 must multiply the 2 too.",
                    "4(y + 2)"))
    its.append(emcq(fig(rect_svg(170, 60, "x + 4", "2x", "rectangle with sides x + 4 and 2x")) +
                    "Which expression gives the perimeter of the rectangle?",
                    "6x + 8", ["3x + 4", "6x + 4", "2x^2 + 8x"],
                    "Perimeter = 2(<i>x</i> + 4) + 2(2<i>x</i>) = 2<i>x</i> + 8 + 4<i>x</i> = 6<i>x</i> + 8. "
                    "Not 3<i>x</i> + 4: that adds only two sides. Not 2<i>x</i><sup>2</sup> + 8<i>x</i>: that is the area.",
                    "2(x + 4) + 2(2x)"))
    its.append(emcq(fig(tri_svg("2a + 1", "equilateral triangle with each side 2a + 1")) +
                    "Each side of the triangle is %s. Which expression gives its perimeter?" % B("2a + 1"),
                    "6a + 3", ["6a + 1", "2a + 3", "9a"],
                    "There are 3 equal sides: 3(2<i>a</i> + 1) = 6<i>a</i> + 3. Not 6<i>a</i> + 1: the 3 must multiply the 1 too.",
                    "3(2a + 1)"))
    its.append(emcq(fig(rect_svg(170, 60, "3n - 1", "4", "rectangle with sides 3n − 1 and 4")) +
                    "Which expression gives the perimeter of the rectangle?",
                    "6n + 6", ["6n + 7", "3n + 3", "12n - 4"],
                    "Perimeter = 2(3<i>n</i> − 1) + 2 × 4 = 6<i>n</i> − 2 + 8 = 6<i>n</i> + 6. "
                    "Not 6<i>n</i> + 7: the 2 must multiply the 1 too. Not 12<i>n</i> − 4: that is the area.",
                    "2(3n - 1) + 2 × 4"))
    # area model in a story
    n, pr, po = P.next()
    its.append(emcq(fig(area_svg(6, [("x", 120), ("4", 70)])) +
                    "%s’s garden is 6 m wide. It has a flower part <i>x</i> m long and a vegetable part 4 m long. "
                    "Which expression gives the total area in square meters?" % n,
                    "6(x + 4)", ["6x + 4", "6 + x + 4", "10x"],
                    "The whole garden is 6 by (<i>x</i> + 4), so the area is 6(<i>x</i> + 4) = 6<i>x</i> + 24. "
                    "Not 6<i>x</i> + 4: the vegetable part is 6 × 4 = 24 square meters.", "6x + 24"))
    its.append(emcq(fig(area_svg(3, [("y", 120), ("8", 80)])) +
                    "A wall is 3 m tall. One part is <i>y</i> m long and the other part is 8 m long. Which expression gives the area of the whole wall?",
                    "3y + 24", ["3y + 8", "11y", "3 + y + 8"],
                    "Area of the parts: 3 × <i>y</i> = 3<i>y</i> and 3 × 8 = 24. Whole wall: 3<i>y</i> + 24, which is the same as 3(<i>y</i> + 8).",
                    "3(y + 8)"))
    # costs and groups
    its.append(emcq("A concert ticket costs <i>t</i> dollars plus a $2 fee for each ticket. Which expression gives the cost of 5 tickets?",
                    "5t + 10", ["5t + 2", "t + 10", "7t"],
                    "One ticket costs <i>t</i> + 2 dollars. Five tickets cost 5(<i>t</i> + 2) = 5<i>t</i> + 10 dollars. "
                    "Not 5<i>t</i> + 2: there is a $2 fee on <b>each</b> of the 5 tickets.", "5(t + 2)"))
    n, pr, po = P.next()
    its.append(emcq("%s and 3 friends each buy a sandwich for <i>s</i> dollars and a juice for $3. Which expression gives the total cost?" % n,
                    "4s + 12", ["4s + 3", "s + 12", "3s + 9"],
                    "There are 4 people (%s and 3 friends). Each spends <i>s</i> + 3 dollars, so the total is 4(<i>s</i> + 3) = 4<i>s</i> + 12. "
                    "Not 3<i>s</i> + 9: count %s too." % (n, n), "4(s + 3)"))
    its.append(emcq("Each of 6 teams has <i>g</i> girls and <i>b</i> boys. Which expression gives the number of players?",
                    "6g + 6b", ["6g + b", "g + 6b", "12gb"],
                    "One team has <i>g</i> + <i>b</i> players. 6 teams have 6(<i>g</i> + <i>b</i>) = 6<i>g</i> + 6<i>b</i> players. "
                    "Not 6<i>g</i> + <i>b</i>: every team has boys too.", "6(g + b)"))
    its.append(emcq("A dinner costs <i>m</i> dollars per person plus a $2 tip per person. Which expression gives the cost for 8 people?",
                    "8m + 16", ["8m + 2", "m + 16", "10m"],
                    "Each person pays <i>m</i> + 2 dollars. For 8 people: 8(<i>m</i> + 2) = 8<i>m</i> + 16. "
                    "Not 10<i>m</i>: 8<i>m</i> and 16 are not like terms.", "8(m + 2)"))
    its.append(emcq("A bakery puts <i>b</i> bagels in each box. It sells 7 boxes on Monday and 5 boxes on Tuesday. "
                    "Which expression gives the number of bagels sold?",
                    "12b", ["35b", "12b^2", "7b + 5"],
                    "7<i>b</i> and 5<i>b</i> are like terms: 7 + 5 = 12, so 12<i>b</i> bagels. Not 35<i>b</i>: add the boxes, do not multiply.",
                    "7b + 5b"))
    its.append(emcq("A gym charges $15 a month plus a $5 locker fee each month. Which expression gives the cost for <i>x</i> months?",
                    "20x", ["15x + 5", "15 + 5x", "75x"],
                    "Each month costs 15 + 5 = 20 dollars, so <i>x</i> months cost 15<i>x</i> + 5<i>x</i> = 20<i>x</i> dollars. "
                    "Not 15<i>x</i> + 5: the locker fee is paid every month, not once.", "15x + 5x"))
    n, pr, po = P.next()
    its.append(emcq("%s buys 3 packs of <i>p</i> pencils, then 2 more packs of <i>p</i> pencils and 4 loose pencils. "
                    "Which expression gives the number of pencils %s has?" % (n, pr),
                    "5p + 4", ["9p", "6p + 4", "5p^2 + 4"],
                    "3<i>p</i> + 2<i>p</i> + 4 = 5<i>p</i> + 4. Not 9<i>p</i>: the 4 loose pencils are not packs, so 4 is not a like term.",
                    "3p + 2p + 4"))
    n1, pr1, po1 = P.next()
    n2, pr2, po2 = P.next()
    its.append(mcq("Shirts cost <i>x</i> dollars and hats cost $8. %s says 3 shirts and 3 hats cost %s dollars. "
                   "%s says they cost %s dollars. Who is right?" % (n1, B("3x + 8"), n2, B("3(x + 8)")),
                   n2, [n1, "Both", "Neither"],
                   "3 shirts and 3 hats are 3 groups of (<i>x</i> + 8), so the cost is 3(<i>x</i> + 8) = 3<i>x</i> + 24. "
                   "%s forgot to multiply the $8 by 3." % n1))
    assert same("3(x + 8)", "3x + 24") and not same("3x + 8", "3(x + 8)")
    # simplify, then evaluate
    for s, v, var, mistakes, why in [
        ("3(x + 4) + 2x", 6, "x", ["5x + 4", "3x + 12", "17x"], "multiplies only the first term"),
        ("2(y + 5) - y", 7, "y", ["y + 5", "2y + 10", "3y + 10"], "multiplies only the first term"),
        ("5(n - 2) + 3n", 4, "n", ["8n - 2", "8n + 10", "5n - 10"], "multiplies only the first term"),
        ("6(k + 1) - 2k", 10, "k", ["4k + 1", "8k + 6", "6k + 6"], "multiplies only the first term"),
        ("8 + 3(m + 1)", 4, "m", ["11m + 11", "3m + 9", "3m + 3"], "adds 8 and 3 before multiplying"),
    ]:
        simp = simplest(s)
        ans = value(s, **{var: v})
        assert value(simp, **{var: v}) == ans
        wrong = [value(m, **{var: v}) for m in mistakes]
        assert all(w != ans and w > 0 for w in wrong) and len(set(wrong)) == 3
        e = ("Simplify first: %s = %s. Then substitute <i>%s</i> = %d: %s = %s. Not %s: that %s."
             % (B(s), H(simp), var, v, H(sub_show(simp, var, v)), num(ans), num(wrong[0]), why))
        its.append(mcq("Simplify %s, then find its value when <i>%s</i> = %d." % (B(s), var, v), num(ans), [num(w) for w in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: perimeter, area, cost and evaluating", "items": its}


def simplest(s):
    """Linear polynomial in one variable -> 'ax + b' / 'ax - b'."""
    p = parse(s)
    var = [m[0] for m in p if m][0]
    a, b = p.get((var,), 0), p.get((), 0)
    t = ("%s" % var if a == 1 else "%d%s" % (a, var))
    if b > 0:
        t += " + %d" % b
    elif b < 0:
        t += " - %d" % -b
    assert same(t, s)
    return t


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    assert same("3(x + 2)", "3x + 6") and same("24x + 18y", "6(4x + 3y)") and same("5x + 3 + 2x", "7x + 3")
    assert value("3(x + 4)", x=2) == 18 and value("3x + 4", x=2) == 10
    return (
        "<h2>What are equivalent expressions?</h2>"
        "<p>Two expressions are <b>equivalent</b> if they have the same value for <b>every</b> value of the variable. "
        "For example, <i>y</i> + <i>y</i> + <i>y</i> and 3<i>y</i> are equivalent: three <i>y</i>’s added together is 3 times <i>y</i>. "
        "We use the properties of operations to change an expression into an equivalent one.</p>"
        "<h2>Combine like terms</h2>"
        "<p><b>Like terms</b> have the same variable part, such as 4<i>a</i> and 2<i>a</i>. Add or subtract their coefficients and keep the variable. "
        "A number with no variable (a constant) is not a like term of 4<i>a</i>.</p>" +
        ex("Example", "Simplify 5<i>x</i> + 3 + 2<i>x</i>.",
           "The like terms are 5<i>x</i> and 2<i>x</i>: 5 + 2 = 7. The 3 stays as it is.", "7<i>x</i> + 3 (not 10<i>x</i>)") +
        "<h2>The distributive property: expand</h2>"
        "<p>The number outside the parentheses multiplies <b>each</b> term inside: <i>a</i>(<i>b</i> + <i>c</i>) = <i>ab</i> + <i>ac</i>. "
        "An area model shows why: the rectangle has two parts, and the total area is the sum of their areas.</p>"
        "<figure class='sn-fig'>" + area_svg(3, [("x", 130), ("2", 60)], inside=["3x", "6"]) +
        "<figcaption>3(<i>x</i> + 2): the parts have areas 3 × <i>x</i> = 3<i>x</i> and 3 × 2 = 6, so 3(<i>x</i> + 2) = 3<i>x</i> + 6.</figcaption></figure>" +
        ex("Example", "Expand 4(2<i>y</i> − 5).", "4 × 2<i>y</i> = 8<i>y</i> and 4 × 5 = 20. The minus sign stays.", "8<i>y</i> − 20") +
        "<h2>Factor using the GCF</h2>"
        "<p>Factoring is the distributive property in reverse. Find the greatest common factor (GCF) of the terms, "
        "divide each term by it, and write the GCF outside the parentheses.</p>" +
        ex("Example", "Factor 24<i>x</i> + 18<i>y</i>.",
           "The GCF of 24 and 18 is 6. 24<i>x</i> ÷ 6 = 4<i>x</i> and 18<i>y</i> ÷ 6 = 3<i>y</i>. Check: 6(4<i>x</i> + 3<i>y</i>) = 24<i>x</i> + 18<i>y</i>.",
           "6(4<i>x</i> + 3<i>y</i>)") +
        "<h2>Check whether two expressions are equivalent</h2>"
        "<p>Simplify both expressions and compare, or substitute a number for the variable. "
        "If even one value gives different results, the expressions are <b>not</b> equivalent.</p>" +
        ex("Example", "Are 3(<i>x</i> + 4) and 3<i>x</i> + 4 equivalent?",
           "Try <i>x</i> = 2: 3(2 + 4) = 18, but 3 × 2 + 4 = 10. The values are different.",
           "No. 3(<i>x</i> + 4) = 3<i>x</i> + 12.") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["3(2 + <i>x</i>) = 6 + <i>x</i>", "Multiply both terms: 6 + 3<i>x</i>"],
            ["3<i>x</i> + 2 = 5<i>x</i>", "3<i>x</i> and 2 are not like terms. 3<i>x</i> + 2 is already simplest."],
            ["<i>x</i> · <i>x</i> = 2<i>x</i>", "<i>x</i> · <i>x</i> = <i>x</i><sup>2</sup>. 2<i>x</i> means <i>x</i> + <i>x</i>."],
            ["4<i>a</i> + 2<i>a</i> = 6<i>a</i><sup>2</sup> or 8<i>a</i>", "Add the coefficients, keep the variable: 6<i>a</i>"],
            ["<i>x</i> + 4<i>x</i> = 4<i>x</i>", "<i>x</i> is 1<i>x</i>: 1 + 4 = 5, so 5<i>x</i>"],
            ["24<i>x</i> + 18<i>y</i> = 3(8<i>x</i> + 6<i>y</i>) when asked for the GCF", "Use the greatest factor, 6: 6(4<i>x</i> + 3<i>y</i>)"],
        ])
    )


FAQ = [
    {"q": "What are equivalent expressions in 6th grade math?",
     "a": "Equivalent expressions have the same value for every value of the variable. For example, 3(<i>x</i> + 2) and 3<i>x</i> + 6 are equivalent, and so are <i>y</i> + <i>y</i> + <i>y</i> and 3<i>y</i>."},
    {"q": "How do you use the distributive property to write an equivalent expression?",
     "a": "Multiply the number outside the parentheses by each term inside: 3(2 + <i>x</i>) = 3 × 2 + 3 × <i>x</i> = 6 + 3<i>x</i>. To go the other way, factor out the GCF: 24<i>x</i> + 18<i>y</i> = 6(4<i>x</i> + 3<i>y</i>)."},
    {"q": "How can you tell if two expressions are equivalent?",
     "a": "Simplify both and see if they match, or substitute the same number into both. If any value gives different results, they are not equivalent: 3(<i>x</i> + 4) and 3<i>x</i> + 4 give 18 and 10 when <i>x</i> = 2."},
    {"q": "What are like terms?",
     "a": "Like terms have exactly the same variable part, such as 4<i>a</i> and 2<i>a</i>, or 3<i>x</i><sup>2</sup> and 5<i>x</i><sup>2</sup>. You combine them by adding the coefficients: 4<i>a</i> + 2<i>a</i> = 6<i>a</i>. A term like 3<i>x</i> and a number like 2 cannot be combined."},
]


def gen():
    rnd = random.Random(611)
    P = People(rnd)
    sets = [set_like_terms(rnd, P), set_expand(rnd, P), set_factor(rnd, P), set_equivalent(rnd, P), set_applied(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert not re.search(r"(\d|\s)-(\s|\d)", re.sub(r"<[^>]+>", "", it["q"] + "".join(it["c"]) + it["e"])), it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "equivalent-expressions", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Equivalent Expressions: Like Terms, the Distributive Property and Factoring",
        "seo_title": "Grade 6 Equivalent Expressions Worksheets: Combine Like Terms, Distributive Property, Factor with the GCF",
        "short_title": "Equivalent expressions",
        "domain": "Expressions and Equations",
        "standard_code": "6.EE.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/EE/A/3/",
        "standard_text": "Apply the properties of operations to generate equivalent expressions. For example, apply the distributive property to the expression 3 (2 + x) to produce the equivalent expression 6 + 3x; apply the distributive property to the expression 24x + 18y to produce the equivalent expression 6 (4x + 3y); apply properties of operations to y + y + y to produce the equivalent expression 3y.",
        "meta_desc": "Free Grade 6 equivalent expressions worksheets: combine like terms, expand with the distributive property, factor using the GCF, and test whether two expressions are equivalent. 100 practice questions with an answer key and step-by-step explanations.",
        "key_big": "Equivalent expressions are equal for every value of the variable. The number outside the parentheses multiplies every term inside.",
        "key_sub": "3(2 + <i>x</i>) = 6 + 3<i>x</i>, not 6 + <i>x</i>. 24<i>x</i> + 18<i>y</i> = 6(4<i>x</i> + 3<i>y</i>). <i>y</i> + <i>y</i> + <i>y</i> = 3<i>y</i>, but <i>y</i> · <i>y</i> = <i>y</i><sup>2</sup>.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
