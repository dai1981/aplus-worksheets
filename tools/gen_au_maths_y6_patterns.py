# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Number Patterns (Australian Curriculum v9.0, AC9M6A01)
  python3 tools/gen_au_maths_y6_patterns.py
Number patterns with whole numbers, decimals and fractions, finding the rule, growing matchstick and
tile patterns with tables, finding the 10th or 20th term, and word problems.
Wrong choices come from real mistakes: using only the first step, mixing up adding and multiplying
rules, counting n jumps instead of n − 1, giving the term number instead of the term, and decimal
place-value slips (1.25 + 0.3 = 1.28). Every answer is checked in code with fractions.Fraction.
HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
WOOD = "#c08a3e"
HEAD = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
MINUS = "−"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ numbers
def F(x):
    """Fraction from an int, a decimal string ('0.25') or a pair (1, 3)."""
    if isinstance(x, tuple):
        return Fr(x[0], x[1])
    return Fr(x)


def whole(n):
    """Australian style: 4536, 10 000 (no-break space)."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NBSP.join(g)
    return (MINUS if n < 0 else "") + s


def dec(v):
    """Exact decimal text for a Fraction with a terminating decimal: 1.25, 3, 0.04."""
    v = Fr(v)
    for k in range(0, 5):
        t = v * 10 ** k
        if t.denominator == 1:
            m = abs(t.numerator)
            w, r = divmod(m, 10 ** k)
            s = whole(w) + ("." + str(r).rjust(k, "0") if k else "")
            return (MINUS if v < 0 else "") + s
    raise ValueError(v)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def frac(v):
    """Fraction text: whole numbers, proper fractions and mixed numerals."""
    v = Fr(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return whole(w)
    return (whole(w) + " " if w else "") + fr(r, v.denominator)


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1 and c.numerator % 5 == 0, v
    return "$%d.%02d" % divmod(c.numerator, 100)


def plain(v):
    """Fraction as plain text for aria labels and plain-text fields: 1 1/3."""
    v = Fr(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    return ("%d " % w if w else "") + "%d/%d" % (r, v.denominator)


def is_dec(v):
    try:
        dec(v)
        return True
    except ValueError:
        return False


def naive_add(a, k, sub=False):
    """The digit-after-the-point mistake: 1.25 + 0.3 = 1.28, 0.75 + 0.5 = 0.80, 1.8 + 0.4 = 1.12."""
    sa, sk = dec(a), dec(k)
    if "." not in sa or "." not in sk:
        return None
    wa, fa = sa.split(".")
    wk, fk = sk.split(".")
    if len(fa) == len(fk) and not sub and int(fa) + int(fk) < 10 ** len(fa):
        return None                      # same length, no carry: the slip gives the right answer
    if sub:
        d = int(fa) - int(fk)
        if d < 0 or len(fa) == len(fk):
            return None
        return Fr(int(wa) - int(wk)) + Fr(d, 10 ** len(str(d)))  # 1.25 − 0.3 = 1.22
    s = int(fa) + int(fk)
    return Fr(int(wa) + int(wk)) + Fr(s, 10 ** len(str(s)))


def naive_frac(a, k):
    """Adding numerators and denominators: 1/4 + 1/2 = 2/6."""
    w, r = divmod(a.numerator, a.denominator)
    if r == 0 or k.denominator == 1 or k >= 1:
        return None
    ra = Fr(r, a.denominator)
    return w + Fr(ra.numerator + k.numerator, ra.denominator + k.denominator)


def ordn(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ patterns
OPS = {"+": lambda x, k: x + k, "−": lambda x, k: x - k, "×": lambda x, k: x * k, "÷": lambda x, k: x / k}
WORDS = {"+": "Add", "−": "Subtract", "×": "Multiply by", "÷": "Divide by"}


def seq(s, op, k, n):
    out = [Fr(s)]
    while len(out) < n:
        out.append(OPS[op](out[-1], Fr(k)))
    return out


class Mode:
    """How numbers in one pattern are written: decimals or fractions."""
    def __init__(self, kind):
        self.kind = kind

    def __call__(self, v):
        return dec(v) if self.kind == "d" else frac(v)


D, FRC = Mode("d"), Mode("f")


def lst(xs, m):
    return ", ".join(m(x) for x in xs)


def showp(xs, m, tail="…"):
    return "<b>" + lst(xs, m) + (", " + tail if tail else "") + "</b>"


def rule(op, k, m):
    k = Fr(k)
    if op in "×÷":
        return "%s %s" % (WORDS[op], dec(k))
    return "%s %s" % (WORDS[op], m(k))


def steps(xs, op, k, m):
    return ", ".join("%s %s %s = %s" % (m(a), op, m(k) if op in "+−" else dec(k), m(b)) for a, b in zip(xs, xs[1:]))


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None):
    """correct and cands are Fractions shown with disp, or strings. Equal values, zero or less are skipped."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pick = {cs}, {cv}, []
    for c in cands:
        if c is None:
            continue
        if disp is not None:
            c = Fr(c)
            if c <= 0 or c in vals:
                continue
            vals.add(c)
            c = disp(c)
        if c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


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


S = 16          # one tile


def sq(x, y, s=S, fill=FILL):
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x, y, s, s, fill, GREEN))


def shp_grid(n):
    """2 rows of n + 1 tiles: 2n + 2 tiles."""
    cols = n + 1
    s = [sq(1 + i * S, 1 + j * S) for i in range(cols) for j in range(2)]
    return cols * S + 2, 2 * S + 2, s, 2 * cols


def shp_L(n):
    """L shape: a corner tile with an arm of n tiles going up and n going right: 2n + 1 tiles."""
    s = [sq(1, 1 + j * S) for j in range(n + 1)] + [sq(1 + i * S, 1 + n * S) for i in range(1, n + 1)]
    return (n + 1) * S + 2, (n + 1) * S + 2, s, 2 * n + 1


def shp_cross(n):
    """Plus sign: a centre tile with 4 arms of n tiles: 4n + 1 tiles."""
    C = 14
    s = []
    for i in range(2 * n + 1):
        s.append(sq(1 + i * C, 1 + n * C, C))
        if i != n:
            s.append(sq(1 + n * C, 1 + i * C, C))
    s.append(sq(1 + n * C, 1 + n * C, C, FILL2))
    return (2 * n + 1) * C + 2, (2 * n + 1) * C + 2, s, 4 * n + 1


def stick(x1, y1, x2, y2):
    """One matchstick, a little shorter than the side so every stick can be counted, with a red head."""
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5
    t = 6.0 / L
    ax, ay, bx, by = x1 + dx * t, y1 + dy * t, x2 - dx * t, y2 - dy * t
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='4' stroke-linecap='round'/>"
            "<circle cx='%.1f' cy='%.1f' r='2.5' fill='%s'/>" % (ax, ay, bx, by, WOOD, bx, by, HEAD))


L_ST = 32


def shp_sticks_sq(n):
    """Row of n squares: 3n + 1 matchsticks."""
    s = []
    for i in range(n):
        s.append(stick(3 + i * L_ST, 3, 3 + (i + 1) * L_ST, 3))
        s.append(stick(3 + i * L_ST, L_ST + 3, 3 + (i + 1) * L_ST, L_ST + 3))
    for i in range(n + 1):
        s.append(stick(3 + i * L_ST, 3, 3 + i * L_ST, L_ST + 3))
    assert len(s) == 3 * n + 1
    return n * L_ST + 6, L_ST + 6, s, 3 * n + 1


def shp_sticks_tri(n):
    """Strip of n triangles, the first pointing up: 2n + 1 matchsticks."""
    L, h = L_ST, L_ST * 0.866
    tris = []
    for i in range(n):
        k = i // 2
        if i % 2 == 0:
            tris.append([(k * L, h), ((k + 1) * L, h), (k * L + L / 2, 0)])
        else:
            tris.append([(k * L + L / 2, 0), ((k + 1) * L + L / 2, 0), ((k + 1) * L, h)])
    s, seen = [], set()
    for tr in tris:
        for a in range(3):
            e = tuple(sorted([tr[a], tr[(a + 1) % 3]]))
            if e not in seen:
                seen.add(e)
                s.append(stick(e[0][0] + 3, e[0][1] + 3, e[1][0] + 3, e[1][1] + 3))
    assert len(seen) == 2 * n + 1
    w = ((n + 1) // 2) * L + (L / 2 if n % 2 == 0 else 0)
    return w + 6, h + 6, s, 2 * n + 1


def shp_house(n):
    """Row of n houses (a square with a triangle roof) sharing walls: 5n + 1 matchsticks."""
    L, h = L_ST, L_ST * 0.866
    s = []
    for i in range(n):
        x = 3 + i * L
        s.append(stick(x + L / 2, 3, x, 3 + h))
        s.append(stick(x + L / 2, 3, x + L, 3 + h))
        s.append(stick(x, 3 + h, x + L, 3 + h))
        s.append(stick(x, 3 + h + L, x + L, 3 + h + L))
    for i in range(n + 1):
        s.append(stick(3 + i * L, 3 + h, 3 + i * L, 3 + h + L))
    assert len(s) == 5 * n + 1
    return n * L + 6, h + L + 6, s, 5 * n + 1


SHAPES = {"grid": shp_grid, "L": shp_L, "cross": shp_cross, "sticks_sq": shp_sticks_sq,
          "sticks_tri": shp_sticks_tri, "house": shp_house}


def thing(kind):
    return "matchstick" if kind in ("sticks_sq", "sticks_tri", "house") else "tile"


def count(kind, n):
    return SHAPES[kind](n)[3]


def pattern_svg(kind, figs=(1, 2, 3)):
    """Figures side by side, bottoms lined up, each with 'Figure n' under it."""
    parts = [SHAPES[kind](n) for n in figs]
    LBW = 64
    gap, pad = 22, 6
    hmax = max(p[1] for p in parts)
    x = pad
    out = []
    for n, (w, h, s, c) in zip(figs, parts):
        col = max(w, LBW)
        out.append("<g transform='translate(%.1f,%.1f)'>%s</g>" % (x + (col - w) / 2, pad + hmax - h, "".join(s)))
        out.append(text(x + col / 2, pad + hmax + 21, "Figure %d" % n, 15))
        x += col + gap
    W = x - gap + pad
    H = pad + hmax + 28
    return svg_wrap(W, H, "".join(out), "growing pattern of %ss: figures %s" % (thing(kind), ", ".join(map(str, figs))))


def table_svg(top, bot, heads, label):
    """Two-row table: heads[0] row with the top values, heads[1] row with the bottom values."""
    CW, LW, RH = 50, 106, 32
    n = len(top)
    W, H = LW + CW * n + 4, RH * 2 + 4
    s = []
    for r, (name, row) in enumerate([(heads[0], top), (heads[1], bot)]):
        y = 2 + r * RH
        s.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (y, LW, RH, FILL, GREEN))
        s.append(text(2 + LW / 2, y + RH / 2 + 5, name, 15))
        for i, v in enumerate(row):
            x = 2 + LW + i * CW
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, CW, RH, GREEN))
            s.append(text(x + CW / 2, y + RH / 2 + 6, v, 16, col=RED if v == "?" else INK))
    return svg_wrap(W, H, "".join(s), label)


# ============================================================ set 1: continue the pattern
def set_continue(rnd):
    its = []
    # A: add a decimal
    for s, k in [("0.25", "0.25"), ("0.5", "0.5"), ("0.6", "0.4"), ("1.75", "0.75"), ("0.9", "0.8"),
                 ("0.05", "0.15"), ("1.5", "1.25"), ("0.35", "0.3")]:
        s, k = F(s), F(k)
        xs = seq(s, "+", k, 5)
        last, ans = xs[3], xs[4]
        nv = naive_add(last, k)
        q = "What is the next term?<br>%s" % showp(xs[:4], D, "?")
        e = "The rule is %s: %s. So the next term is %s + %s = %s." % (
            rule("+", k, D), steps(xs[:2], "+", k, D), dec(last), dec(k), dec(ans))
        if nv is not None and nv != ans:
            e += " Line up the decimal points: %s + %s is not %s." % (dec(last), dec(k), dec(nv))
        its.append((0, mcq(q, ans, [nv, last + 2 * k, last + k / 10, last + s if s != k else None, last - k], e, rnd, D)))
    # B: subtract a decimal
    for s, k in [("3", "0.4"), ("10", "0.75"), ("6.2", "0.7")]:
        s, k = F(s), F(k)
        xs = seq(s, "−", k, 5)
        last, ans = xs[3], xs[4]
        q = "What is the next term?<br>%s" % showp(xs[:4], D, "?")
        e = ("The terms get smaller, so the rule subtracts: %s − %s = %s. Next: %s − %s = %s."
             % (dec(xs[0]), dec(k), dec(xs[1]), dec(last), dec(k), dec(ans)))
        its.append((1, mcq(q, ans, [last - 2 * k, last - k / 10, last + k, last - 1], e, rnd, D)))
    # C: add or subtract a fraction
    for s, op, k in [((1, 3), "+", (1, 3)), ((1, 4), "+", (1, 4)), ((2, 3), "+", (2, 3)), (5, "−", (1, 4)),
                     ((1, 2), "+", (3, 2))]:
        s, k = F(s), F(k)
        xs = seq(s, op, k, 5)
        last, ans = xs[3], xs[4]
        q = "What is the next term?<br>%s" % showp(xs[:4], FRC, "?")
        e = "The rule is %s: %s. Next: %s %s %s = %s." % (
            rule(op, k, FRC), steps(xs[:2], op, k, FRC), frac(last), op, frac(k), frac(ans))
        if op == "+":
            cands = [last + 2 * k, last + 1, last + (k - int(k)), last - k]
        else:
            cands = [last - 2 * k, last + k, last - 1]
        its.append((2, mcq(q, ans, cands, e, rnd, FRC)))
    # D: multiply (the first jump is a trap)
    for s, k in [("0.5", 2), ("1.5", 2), ("0.1", 3), ("0.2", 2)]:
        s, k = F(s), Fr(k)
        xs = seq(s, "×", k, 5)
        last, ans = xs[3], xs[4]
        d0, d2 = xs[1] - xs[0], xs[3] - xs[2]
        q = "What is the next term?<br>%s" % showp(xs[:4], D, "?")
        e = ("The jumps are %s, so the rule is not adding the same amount. Each term is %d times the one before: "
             "%s. Next: %s × %d = %s." % (", ".join(dec(b - a) for a, b in zip(xs, xs[1:4])), k,
                                           steps(xs[:4], "×", k, D), dec(last), k, dec(ans)))
        its.append((3, mcq(q, ans, [last + d0, last + d2, last * k * k, last + k], e, rnd, D)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Continue the pattern: decimals and fractions", "items": [i for _, i in its]}


# ============================================================ set 2: find the rule
def set_rule(rnd):
    its = []
    # A: add or subtract a decimal
    for s, op, k in [("1.2", "+", "0.4"), ("0.3", "+", "0.25"), ("2.5", "+", "0.75"), ("0.08", "+", "0.04"),
                     ("3.6", "+", "1.2"), ("5", "−", "0.6")]:
        s, k = F(s), F(k)
        xs = seq(s, op, k, 4)
        other = "−" if op == "+" else "+"
        q = "Which rule makes this pattern?<br>%s" % showp(xs, D)
        diffs = ", ".join("%s − %s = %s" % ((dec(b), dec(a), dec(b - a)) if op == "+" else (dec(a), dec(b), dec(a - b)))
                          for a, b in zip(xs, xs[1:]))
        e = "Find the difference between each pair of terms: %s. The difference is always %s, so the rule is %s." % (
            diffs, dec(k), rule(op, k, D))
        cands = [rule(other, k, D), rule(op, k * 10, D), rule(op, k / 10, D)]
        if s != k and s != 2 * k:
            cands.append(rule(op, s, D))
        if op == "+" and s == 2 * k:
            cands.append("Multiply by 2")
        cands.append(rule(op, 2 * k, D))
        its.append((0, mcq(q, rule(op, k, D), cands, e, rnd)))
    # B: add or subtract a fraction
    for s, op, k in [((1, 3), "+", (1, 3)), (3, "−", (1, 4)), ((1, 2), "+", (1, 4)), ((2, 3), "+", (2, 3)),
                     (4, "−", (3, 4)), ((1, 5), "+", (2, 5))]:
        s, k = F(s), F(k)
        xs = seq(s, op, k, 4)
        other = "−" if op == "+" else "+"
        q = "Which rule makes this pattern?<br>%s" % showp(xs, FRC)
        e = "Each term is %s %s than the one before: %s. The rule is %s." % (
            frac(k), "more" if op == "+" else "less", steps(xs, op, k, FRC), rule(op, k, FRC))
        cands = []
        if op == "+" and s == k:
            cands.append("Multiply by 2")
            e += " Multiply by 2 works only for the first step (%s × 2 = %s); %s × 2 is not %s." % (
                frac(xs[0]), frac(xs[1]), frac(xs[1]), frac(xs[2]))
        cands += [rule(other, k, FRC)]
        if s != k and s < 1:
            cands.append(rule(op, s, FRC))
        cands += [rule(op, 2 * k, FRC), rule(op, 1, FRC), rule(op, k + 1, FRC)]
        its.append((1, mcq(q, rule(op, k, FRC), cands, e, rnd)))
    # C: multiply or divide
    for s, op, k, m in [("0.5", "×", 2, D), ("0.2", "×", 3, D), (80, "÷", 2, D), ("0.03", "×", 10, D), (6, "÷", 2, FRC)]:
        s = F(s)
        xs = seq(s, op, k, 4)
        d0, d2 = xs[1] - xs[0], xs[3] - xs[2]
        q = "Which rule makes this pattern?<br>%s" % showp(xs, m)
        wd = "+" if d0 > 0 else "−"
        e = ("The differences are %s, so the rule is not adding or subtracting the same amount. %s. The rule is %s."
             % (", ".join(m(abs(b - a)) for a, b in zip(xs, xs[1:])), cap(steps(xs, op, k, m)), rule(op, k, m)))
        cands = [rule(wd, abs(d0), m), rule(wd, abs(d2), m)]
        cands.append(rule(op, k + 1, m) if k != 10 else rule(op, 100, m))
        its.append((2, mcq(q, rule(op, k, m), cands, e, rnd)))
    # D: a missing term in the middle
    cases = [("2.5", "+", "0.75", D), ((1, 4), "+", (1, 2), FRC), ("0.4", "×", 3, D)]
    for s, op, k, m in cases:
        s, k = F(s), Fr(F(k))
        xs = seq(s, op, k, 5)
        prev, ans, nxt = xs[1], xs[2], xs[3]
        shown = [m(x) if i != 2 else "<span style='color:%s'>?</span>" % RED for i, x in enumerate(xs)]
        q = "What is the missing term?<br><b>%s</b>" % ", ".join(shown)
        if op == "×":
            e = ("The jumps grow, so look for multiplying: %s × %d = %s. The missing term is %s × %d = %s. "
                 "Check: %s × %d = %s." % (dec(xs[0]), k, dec(xs[1]), dec(prev), k, dec(ans), dec(ans), k, dec(nxt)))
            cands = [prev + (xs[1] - xs[0]), (prev + nxt) / 2, prev * 2]
        else:
            e = ("The rule is %s (%s). The missing term is %s + %s = %s. Check: %s + %s = %s."
                 % (rule(op, k, m), steps(xs[:2], op, k, m), m(prev), m(k), m(ans), m(ans), m(k), m(nxt)))
            if m is D:
                cands = [naive_add(prev, k), xs[-1] + k, prev + k / 10, prev + Fr(1, 4)]
            else:
                cands = [naive_frac(prev, k), xs[-1] + k, prev + Fr(1, 4)]
                e += " Do not add the tops and the bottoms: %s + %s is not %s." % (m(prev), m(k), fr(4, 6))
        its.append((3, mcq(q, ans, cands, e, rnd, m)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Find the rule and the missing term", "items": [i for _, i in its]}


# ============================================================ set 3: growing patterns
def set_growing(rnd):
    its = []
    # A: next figure
    for kind in ["sticks_sq", "sticks_tri", "house", "L", "cross"]:
        a, b, c = [count(kind, n) for n in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = c + k
        q = fig(pattern_svg(kind)) + "How many %ss will Figure 4 need?" % w
        e = "Count each figure: %d, %d, %d. Each figure adds %d %ss. Figure 4: %d + %d = %d." % (a, b, c, k, w, c, k, ans)
        its.append((0, mcq(q, ans, [c + 1, 4 * a, c + 2 * k, c + a], e, rnd, D)))
    # B: how it grows (recursive) and the rule from the figure number
    for kind in ["house", "grid"]:
        a, b, c = [count(kind, n) for n in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        q = fig(pattern_svg(kind)) + "Which rule describes how the pattern grows?"
        ans = "Start with %d, add %d each time" % (a, k)
        cands = ["Start with %d, add %d each time" % (a, a), "Start with %d, multiply by 2" % a,
                 "Start with %d, add %d each time" % (k, k)]
        e = ("Count the %ss: %d, %d, %d. Figure 1 has %d, and each new figure adds %d (%d − %d = %d). "
             "Adding %d each time would give %d, not %d, for Figure 2." % (w, a, b, c, a, k, b, a, k, a, 2 * a, b))
        its.append((1, mcq(q, ans, cands, e, rnd)))
    for kind in ["sticks_sq", "cross"]:
        a, b, c = [count(kind, n) for n in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        r = a - k
        q = fig(pattern_svg(kind)) + "Which rule gives the number of %ss for any figure?" % w
        ans = "%d × figure number + %d" % (k, r)
        cands = ["%d × figure number" % a, "%d × figure number" % k, "figure number + %d" % k]
        e = ("Each figure adds %d, so multiply the figure number by %d. Figure 1: %d × 1 = %d, and it has %d, so add %d. "
             "Check Figure 3: %d × 3 + %d = %d. (%d × figure number works only for Figure 1.)"
             % (k, k, k, k, a, r, k, r, c, a))
        its.append((1, mcq(q, ans, cands, e, rnd)))
    # C: tables
    for vals, N, w in [((5, 3), 10, "Tiles"), ((6, 5), 10, "Matchsticks"), ((3, 2), 20, "Tiles"), ((4, 2), 20, "Matchsticks")]:
        a, k = vals
        top = ["1", "2", "3", "4", str(N)]
        row = [a + i * k for i in range(4)]
        bot = [str(v) for v in row] + ["?"]
        ans = a + (N - 1) * k
        q = (fig(table_svg(top, bot, ["Figure", w], "table: figure number and number of %s" % w.lower())) +
             "The pattern keeps growing in the same way. What number goes in the box under Figure %d?" % N)
        e = ("Each figure adds %d. From Figure 1 to Figure %d there are %d jumps: %d + %d × %d = %d. "
             "(Adding %d to the last number gives Figure 5, not Figure %d.)" % (k, N, N - 1, a, N - 1, k, ans, k, N))
        its.append((2, mcq(q, ans, [row[-1] + k, a * N, a + N * k, k * N], e, rnd, D)))
    # D: far figures from the picture
    for kind, N in [("sticks_tri", 10), ("L", 20), ("house", 10), ("cross", 10)]:
        a, b, c = [count(kind, n) for n in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        ans = a + (N - 1) * k
        assert ans == count(kind, N)
        q = fig(pattern_svg(kind)) + "How many %ss will Figure %d need?" % (w, N)
        e = ("Figure 1 has %d and each figure adds %d. From Figure 1 to Figure %d there are %d jumps: "
             "%d + %d × %d = %d." % (a, k, N, N - 1, a, N - 1, k, ans))
        its.append((3, mcq(q, ans, [a + N * k, N * a, N * k, c * (N // 3)], e, rnd, D)))
    # E: which figure (term number vs number of pieces)
    for kind, N in [("sticks_sq", 10), ("house", 8), ("L", 12)]:
        a, b, c = [count(kind, n) for n in (1, 2, 3)]
        k = b - a
        w = thing(kind)
        V = count(kind, N)
        q = fig(pattern_svg(kind)) + "Which figure will use exactly %d %ss?" % (V, w)
        ans = "Figure %d" % N
        e = ("After Figure 1 there are %d − %d = %d more %ss, which is %d ÷ %d = %d jumps. "
             "1 + %d = %d, so it is Figure %d. Check: %d + %d × %d = %d."
             % (V, a, V - a, w, V - a, k, N - 1, N - 1, N, N, a, N - 1, k, V))
        its.append((4, mcq(q, ans, ["Figure %d" % v for v in [N - 1, N + 1, V // a, V]], e, rnd)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Growing matchstick and tile patterns", "items": [i for _, i in its]}


# ============================================================ set 4: the 10th or 20th term
def set_far(rnd):
    its = []
    # A: start and rule
    for s, op, k, n, m in [("0.5", "+", "0.25", 10, D), ("1.2", "+", "0.4", 10, D), ("3", "+", "1.5", 20, D),
                           ((1, 3), "+", (1, 3), 20, FRC), (2, "+", (3, 4), 10, FRC), (20, "−", "0.75", 10, D)]:
        s, k = F(s), F(k)
        xs = seq(s, op, k, n)
        ans = xs[-1]
        sg = 1 if op == "+" else -1
        q = "Start at <b>%s</b>. The rule is <b>%s</b>. What is the %s term?" % (m(s), rule(op, k, m), ordn(n))
        e = ("From the 1st term to the %s term there are %d jumps, not %d. %d × %s = %s, and %s %s %s = %s."
             % (ordn(n), n - 1, n, n - 1, m(k), m((n - 1) * k), m(s), op, m((n - 1) * k), m(ans)))
        cands = [s + sg * n * k, n * k if op == "+" else (n - 1) * k, s + sg * (n - 2) * k, s + sg * (n + 1) * k]
        its.append((0, mcq(q, ans, cands, e, rnd, m)))
    # B: from a list
    for s, op, k, n, m in [("2.4", "+", "0.4", 20, D), ((1, 4), "+", (1, 4), 20, FRC), ((3, 2), "+", (1, 2), 10, FRC),
                           ("9.6", "−", "0.4", 10, D)]:
        s, k = F(s), F(k)
        xs = seq(s, op, k, n)
        ans = xs[-1]
        sg = 1 if op == "+" else -1
        q = "%s<br>What is the %s term?" % (showp(xs[:4], m), ordn(n))
        e = ("The rule is %s. The %s term is %d jumps after the 1st term: %s %s %d × %s = %s %s %s = %s."
             % (rule(op, k, m), ordn(n), n - 1, m(s), op, n - 1, m(k), m(s), op, m((n - 1) * k), m(ans)))
        cands = [s + sg * n * k, Fr(n), s + sg * (n - 2) * k, xs[4]]
        it = mcq(q, ans, cands, e, rnd, m)
        if m(Fr(n)) in it["c"]:
            it["e"] += " %d is the term number, not the term." % n
        its.append((1, it))
    # C: tables (position → term)
    for k, c, N in [("0.4", 0, 20), ("0.75", 0, 10), ("2", "0.5", 10), ("0.3", 0, 20)]:
        k, c = F(k), F(c)
        row = [k * p + c for p in range(1, 5)]
        ans = k * N + c
        top = ["1", "2", "3", "4", str(N)]
        bot = [dec(v) for v in row] + ["?"]
        q = (fig(table_svg(top, bot, ["Position", "Term"], "table: position and term")) +
             "The pattern continues. What is the term in position %d?" % N)
        if c == 0:
            e = ("Each term is the position × %s (1 × %s = %s, 4 × %s = %s). So position %d: %d × %s = %s."
                 % (dec(k), dec(k), dec(row[0]), dec(k), dec(row[3]), N, N, dec(k), dec(ans)))
            cands = [row[3] + k, N + k, N * k * 10, (N - 1) * k]
        else:
            e = ("The terms go up by %s, so multiply the position by %s, then add %s (1 × %s + %s = %s). "
                 "Position %d: %d × %s + %s = %s." % (dec(k), dec(k), dec(c), dec(k), dec(c), dec(row[0]),
                                                       N, N, dec(k), dec(c), dec(ans)))
            cands = [N * row[0], row[3] + k, row[0] + N * k, N * k]
        its.append((2, mcq(q, ans, cands, e, rnd, D)))
    # D: position rule written out (order of operations)
    q = ("The rule for the term is <b>position × 1.5 + 2</b>.<br>What is the 20th term?")
    e = "Multiply first, then add: 20 × 1.5 = 30, and 30 + 2 = 32."
    its.append((2, mcq(q, Fr(32), [Fr(33), Fr(30), Fr(47, 2)], e, rnd, D)))
    # E: which term is it?
    for s, k, v, m in [("3", "0.5", "10", D), ("1.5", "0.75", "9", D), ((1, 4), (1, 2), (19, 4), FRC)]:
        s, k, v = F(s), F(k), F(v)
        pos = (v - s) / k + 1
        assert pos.denominator == 1
        pos = int(pos)
        xs = seq(s, "+", k, 4)
        q = "%s<br>Which term is %s?" % (showp(xs, m), m(v))
        ans = "the %s term" % ordn(pos)
        e = ("%s − %s = %s, and %s ÷ %s = %d jumps. The 1st term plus %d jumps is the %s term. "
             "Check: %s + %d × %s = %s." % (m(v), m(s), m(v - s), m(v - s), m(k), pos - 1, pos - 1, ordn(pos),
                                             m(s), pos - 1, m(k), m(v)))
        alt = [pos - 1, int(v) if v.denominator == 1 else v.numerator, int(v / k), pos + 1]
        cands = ["the %s term" % ordn(x) for x in alt if x > 0]
        its.append((3, mcq(q, ans, cands, e, rnd)))
    # F: multiplying patterns
    q = "%s<br>What is the 10th term?" % showp([1, 2, 4, 8], D)
    e = "The rule is Multiply by 2. Keep doubling: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512. The 10th term is 512."
    its.append((4, mcq(q, Fr(512), [Fr(1024), Fr(20), Fr(10)], e, rnd, D)))
    q = "Start at <b>0.1</b>. The rule is <b>Multiply by 10</b>. What is the 6th term?"
    e = ("0.1, 1, 10, 100, 1000, 10%s000. From the 1st to the 6th term there are 5 jumps, so multiply by 10 five times."
         % NBSP)
    its.append((4, mcq(q, Fr(10000), [Fr(100000), Fr(1000), Fr("0.6")], e, rnd, D)))
    rnd.shuffle(its)
    its.sort(key=lambda t: t[0])
    return {"title": "Find the 10th or 20th term", "items": [i for _, i in its]}


# ============================================================ set 5: word problems
def set_words(rnd, P):
    its = []
    M = money

    def add(q, ans, cands, e, disp):
        its.append(mcq(q, ans, cands, e, rnd, disp))

    n, he, his = P.next()
    add("%s has $12 in %s money box. %s saves $2.50 a week. How much money will %s have after 8 weeks?" % (n, his, cap(he), he),
        F("32"), [F("34.5"), F("20"), F("28")],
        "8 weeks of $2.50 is 8 × $2.50 = $20. $12 + $20 = $32.00. ($34.50 counts 9 weeks of saving.)", M)
    n, he, his = P.next()
    add("%s starts with nothing and saves $2.50 a week. After how many weeks will %s have $40?" % (n, he),
        "16 weeks", ["15 weeks", "17 weeks", "20 weeks"],
        "Count by $2.50: $10 is 4 weeks, so $40 is 4 × 4 = 16 weeks. Check: 16 × $2.50 = $40.", None)
    n, he, his = P.next()
    add("%s runs 1.5 km on day 1 of %s training. Each day %s runs 0.25 km more. How far does %s run on day 10?" % (n, his, he, he),
        F("3.75"), [F("4"), F("2.5"), F("3.5")],
        "From day 1 to day 10 there are 9 jumps: 9 × 0.25 = 2.25 km. 1.5 + 2.25 = 3.75 km.",
        lambda v: dec(v) + " km")
    add("A seedling is 4.5 cm tall. It grows 1.2 cm each week. How tall is it after 6 weeks?",
        F("11.7"), [F("12.9"), F("7.2"), F("5.7")],
        "6 weeks of growth: 6 × 1.2 = 7.2 cm. 4.5 + 7.2 = 11.7 cm.", lambda v: dec(v) + " cm")
    add("A rainwater tank holds 250 L. The garden uses 12.5 L a day and no rain falls. How much water is left after 8 days?",
        F("150"), [F("100"), F("137.5"), F("162.5")],
        "8 × 12.5 = 100 L used. 250 − 100 = 150 L left. (100 L is the amount used, not the amount left.)",
        lambda v: dec(v) + " L")
    add("A taxi trip costs $4.20 to start plus $1.60 for each kilometre. How much is a 10 km trip?",
        F("20.2"), [F("58"), F("16"), F("21.8")],
        "10 × $1.60 = $16. Add the start cost once: $16 + $4.20 = $20.20. ($58 adds $4.20 to every kilometre.)", M)
    add("Square tables are pushed together in a row for a class party. 1 table seats 4 students, and each extra "
        "table adds 2 seats. How many students can sit at 15 tables?",
        Fr(32), [Fr(60), Fr(30), Fr(34)],
        "The pattern is 4, 6, 8, … (add 2). 15 tables: 4 + 14 × 2 = 32. It is not 15 × 4 = 60, because seats are lost where tables touch.",
        lambda v: "%d students" % v)
    add("A jug holds 3 L of cordial. Each glass uses %s L. How much is left after 7 glasses?" % fr(1, 4),
        F((5, 4)), [F((7, 4)), F((3, 4)), F((5, 2))],
        "7 glasses use 7 × " + fr(1, 4) + " = " + fr(7, 4) + " = 1 " + fr(3, 4) + " L. 3 − 1 " + fr(3, 4) + " = 1 " + fr(1, 4) + " L.",
        lambda v: frac(v) + " L")
    n, he, his = P.next()
    add("In week 1, %s walks 2 km to school and back each day. Each week %s adds %s km. How far does %s walk each day in week 5?"
        % (n, he, fr(3, 4), he),
        Fr(5), [F((23, 4)), F((15, 4)), F((9, 2))],
        "Week 1 to week 5 is 4 jumps: 4 × " + fr(3, 4) + " = 3 km. 2 + 3 = 5 km.", lambda v: frac(v) + " km")
    add("A sheet of paper is folded in half again and again. After 1 fold there are 2 layers, after 2 folds there are 4 layers. "
        "How many layers are there after 6 folds?",
        Fr(64), [Fr(12), Fr(32), Fr(128)],
        "Each fold doubles the layers: 2, 4, 8, 16, 32, 64. Adding 2 each time (12) uses the wrong kind of rule.",
        lambda v: "%d layers" % v)
    add("A 64 cm ribbon is cut in half. One half is cut in half again, and so on. How long is the piece after 5 cuts?",
        Fr(2), [Fr(4), Fr(1), Fr(54)],
        "Each cut halves the length: 32, 16, 8, 4, 2 cm. (54 cm subtracts 2 each time instead of halving.)",
        lambda v: dec(v) + " cm")
    add("At 6 pm it is 24°C. The temperature falls 1.5°C each hour. What is the temperature at 11 pm?",
        F("16.5"), [F("15"), F("7.5"), F("22.5")],
        "6 pm to 11 pm is 5 hours. 5 × 1.5 = 7.5°C. 24 − 7.5 = 16.5°C.", lambda v: dec(v) + "°C")
    n, he, his = P.next()
    add("%s has $150 in the bank and spends $12.50 each week. After how many weeks will %s have $50 left?" % (n, he),
        "8 weeks", ["12 weeks", "4 weeks", "9 weeks"],
        "%s spends $150 − $50 = $100. $100 ÷ $12.50 = 8 weeks. ($150 ÷ $12.50 = 12 weeks would leave $0.)" % n, None)
    add("At an outdoor concert, row 1 has 18 seats. Each row has 2 more seats than the row in front. How many seats are in row 20?",
        Fr(56), [Fr(58), Fr(40), Fr(360)],
        "Row 1 to row 20 is 19 jumps: 19 × 2 = 38. 18 + 38 = 56 seats.", lambda v: "%d seats" % v)
    n, he, his = P.next()
    add("For footy pre-season, %s runs 2.5 km in week 1 and 0.5 km more each week. In which week will %s run 6 km?" % (n, he),
        "week 8", ["week 7", "week 12", "week 6"],
        "6 − 2.5 = 3.5 km more. 3.5 ÷ 0.5 = 7 jumps. Week 1 + 7 jumps is week 8. Check: 2.5 + 7 × 0.5 = 6.", None)
    add("Netball finals tickets cost $7.50 each. 1 ticket costs $7.50, 2 tickets cost $15. How much do 12 tickets cost?",
        F("90"), [F("97.5"), F("82.5"), F("19.5")],
        "Each ticket adds $7.50, so multiply: 12 × $7.50 = $90.00. ($19.50 adds 12 instead of multiplying.)", M)
    n, he, his = P.next()
    add("%s builds a fence. 1 section uses 2 posts and 3 rails (5 pieces). Each extra section adds 1 post and 3 rails. "
        "How many pieces are needed for 12 sections?" % n,
        Fr(49), [Fr(60), Fr(48), Fr(53)],
        "Each extra section adds 4 pieces, because it shares a post. 5 + 11 × 4 = 49. (12 × 5 = 60 counts shared posts twice.)",
        lambda v: "%d pieces" % v)
    n, he, his = P.next()
    add("One lap of the school oval is 0.4 km. How many laps does %s need to run 6 km?" % n,
        "15 laps", ["150 laps", "24 laps", "16 laps"],
        "Count by 0.4: 2 km is 5 laps, so 6 km is 3 × 5 = 15 laps. Check: 15 × 0.4 = 6.", None)
    add("A candle is 24 cm tall. It burns down 1.5 cm each hour. How tall is it after 8 hours?",
        F("12"), [F("10.5"), F("13.5"), F("22.5")],
        "8 × 1.5 = 12 cm burns away. 24 − 12 = 12 cm left.", lambda v: dec(v) + " cm")
    n, he, his = P.next()
    add("%s gets $5 pocket money a week at age 6. It goes up by $0.50 each birthday. How much does %s get a week at age 12?" % (n, he),
        F("8"), [F("8.5"), F("11"), F("3")],
        "Age 6 to age 12 is 6 birthdays: 6 × $0.50 = $3. $5 + $3 = $8.00. ($11 adds $1 a year instead of $0.50.)", M)
    rnd.shuffle(its)
    return {"title": "Pattern word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    t = table_svg(["1", "2", "3", "4", "10"], ["4", "7", "10", "13", "31"], ["Figure", "Matchsticks"],
                  "table: figure number and number of matchsticks")
    return (
        "<h2>A rule makes the pattern</h2>"
        "<p>Each number in a pattern is a <b>term</b>. Its place in the pattern is the <b>term number</b> "
        "(1st, 2nd, 3rd …). A <b>rule</b> tells you how to get the next term, such as <b>Add 0.25</b>, "
        "<b>Subtract " + fr(1, 4) + "</b> or <b>Multiply by 2</b>.</p>" +
        ex("Decimals", "0.35, 0.65, 0.95, 1.25, ?",
           "The difference is 0.3 each time. Line up the decimal points: 1.25 + 0.30 = 1.55.", "1.55") +
        ex("Fractions", fr(1, 3) + ", " + fr(2, 3) + ", 1, 1 " + fr(1, 3) + ", ?",
           "The rule is Add " + fr(1, 3) + ". 1 " + fr(1, 3) + " + " + fr(1, 3) + " = 1 " + fr(2, 3) + ".", "1 " + fr(2, 3)) +
        "<h2>Check every step to find the rule</h2>"
        "<p>Work out the difference between each pair of terms. If it is always the same, the rule adds or "
        "subtracts it. If the jumps keep growing, try multiplying.</p>" +
        ex("Find the rule", "0.5, 1, 2, 4, …",
           "The jumps are 0.5, 1, 2, so it is not Add 0.5. Each term is 2 times the one before.", "Multiply by 2") +
        "<h2>Growing patterns</h2>"
        "<p>Count the pieces in each figure, then find how many are added each time. Put the counts in a table.</p>"
        "<figure class='sn-fig'>" + pattern_svg("sticks_sq") +
        "<figcaption>4, 7, 10 matchsticks: each new square adds 3 matchsticks, because it shares a side.</figcaption></figure>"
        "<figure class='sn-fig'>" + t +
        "<figcaption>Figure 10: 4 + 9 × 3 = 31. The rule from the figure number is 3 × figure number + 1.</figcaption></figure>"
        "<h2>Jump to the 10th or 20th term</h2>"
        "<p>From the 1st term to the 10th term there are <b>9 jumps</b>. Add the start and the jumps.</p>" +
        ex("10th term", "Start at 0.5. The rule is Add 0.25. What is the 10th term?",
           "9 jumps: 9 × 0.25 = 2.25. 0.5 + 2.25 = 2.75.", "2.75") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["1.25 + 0.3 = 1.28", "Line up the decimal points: 1.25 + 0.30 = 1.55"],
            ["Using only the first step: 0.5, 1, 2, 4 is Add 0.5", "Check every step. Growing jumps mean multiply"],
            ["10th term = start + 10 jumps", "From the 1st to the 10th term there are 9 jumps"],
            ["4 matchsticks for Figure 1, so 4 × 10 = 40 for Figure 10", "Each figure adds 3, not 4: 4 + 9 × 3 = 31"],
            ["“Which term is 10?” answered with the 10th term", "The term number and the term are different. Find how many jumps make 10"],
        ])
    )


FAQ = [
    {"q": "What are number patterns in Year 6 maths?",
     "a": "In the Australian Curriculum (AC9M6A01), Year 6 students use rules to continue patterns with whole numbers, decimals and fractions, such as 0.25, 0.5, 0.75, 1, and growing patterns made from matchsticks or tiles. They also find the rule and use it to work out terms further along."},
    {"q": "How do you find the rule for a number pattern?",
     "a": "Work out the difference between each pair of terms. If it is always the same, the rule adds or subtracts it (for example Add 0.4); if the jumps keep growing, check whether each term is multiplied by the same number, such as Multiply by 2."},
    {"q": "How do you find the 20th term of a pattern?",
     "a": "Count the jumps from the 1st term: there are 19. Multiply the rule by 19 and add it to the 1st term, so for 2.4, 2.8, 3.2, … the 20th term is 2.4 + 19 × 0.4 = 10."},
    {"q": "Is there NAPLAN in Year 6?",
     "a": "No. NAPLAN is sat in Years 3, 5, 7 and 9. Patterns and rules are part of the Year 7 NAPLAN numeracy test, so Year 6 is a good time to practise them."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen_unit():
    rnd = random.Random(6810)
    P = People(rnd)
    sets = [set_continue(rnd), set_rule(rnd), set_growing(rnd), set_far(rnd), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    return {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "number-patterns", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Number Patterns",
        "seo_title": "Year 6 Number Patterns Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Number Patterns",
        "domain": "Algebra",
        "standard_code": "AC9M6A01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise and use rules that generate visually growing patterns and number patterns involving rational numbers",
        "meta_desc": "Free Year 6 maths worksheets on number patterns, aligned to the Australian Curriculum (AC9M6A01): continue patterns with decimals and fractions, find the rule, growing matchstick and tile patterns, the 10th and 20th term, and word problems. 100 questions with an answer key.",
        "key_big": "Find the rule by checking every step. To reach the 10th term, add 9 jumps to the 1st term.",
        "key_sub": "0.5, 1, 2, 4 is Multiply by 2, not Add 0.5. Start at 0.5 and add 0.25: the 10th term is 0.5 + 9 × 0.25 = 2.75.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(growing pattern|table)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
