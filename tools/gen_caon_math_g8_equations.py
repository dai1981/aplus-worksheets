# -*- coding: utf-8 -*-
"""
CA Grade 8 Math: Equations and Inequalities (Ontario Mathematics Curriculum 2020, Grade 8: Algebra, C2.3 and C2.4)
  python3 tools/gen_caon_math_g8_equations.py
Two-step equations with integers (3x + 8 = −7, −2x + 7 = 15, x/3 + 4 = −2), equations with the variable on
both sides (3x + 4 = x + 10), with brackets (3(x − 2) = x + 8) and with decimal numbers (0.4x + 1.2 = 3.6),
inequalities with integers solved, verified and graphed on a number line, and word problems in Ontario and
Canadian contexts (phone plans, winter temperatures, a bike-share bike, a canoe rental, electricity plans).
Wrong choices come from real mistakes: using the same operation instead of the inverse (a sign error when a
term moves to the other side), adding the x-terms instead of subtracting them, a sign error in the last
division, dividing before dealing with the constant, forgetting the last step, expanding 3(x − 2) as 3x − 2,
a misplaced decimal point, reversing the inequality sign when nothing negative was multiplied or divided,
an open circle for ≤ / ≥ (or a closed one for < / >), and the arrow the wrong way.
Every answer is solved and checked in code with fractions.Fraction. HTML attributes use single quotes.
Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤", "=": "="}
OPP = {">": "<", "<": ">", ">=": "<=", "<=": ">=", "=": "="}     # arrow the other way / read from the right
SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}               # open <-> closed circle
RIGHT = {">": True, ">=": True, "<": False, "<=": False}
CLOSED = {">": False, "<": False, ">=": True, "<=": True}
WORDS = {">": "greater than", "<": "less than", ">=": "greater than or equal to", "<=": "less than or equal to"}


# ------------------------------------------------------------ numbers
def num(v):
    """Fraction -> '12', '2.75', '10 000', '−3'. Only terminating decimals are allowed."""
    v = F(v)
    neg = v < 0
    v = abs(v)
    if v.denominator == 1:
        s = str(v.numerator)
        if v >= 10000:
            s = "{:,}".format(v.numerator).replace(",", NB)
    else:
        for dp in range(1, 5):
            if (v * 10 ** dp).denominator == 1:
                n = v * 10 ** dp
                s = str(n.numerator).rjust(dp + 1, "0")
                s = s[:-dp] + "." + s[-dp:]
                break
        else:
            raise ValueError(v)
    return (M if neg else "") + s


def par(v):
    """a number inside a calculation: negatives in brackets"""
    return "(%s)" % num(v) if F(v) < 0 else num(v)


def money(v):
    v = F(v)
    assert v > 0 and (v * 100).denominator == 1, v
    if v.denominator == 1:
        return "$" + num(v)
    return "$%d.%02d" % (int(v), int((v - int(v)) * 100))


def terminating(v):
    v = F(v)
    d = v.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


# ------------------------------------------------------------ equations in a mini syntax
# "3x + 8 = -7", "-2x + 7 = 15", "8 - 3x = 23", "x/3 + 4 = -2", "3(x-2) = x + 8", "2x - 3 < 5x + 9".
# Tokens are separated by spaces; only the first token of a side may carry a minus sign.
TERM = re.compile(r"^(-?)(\d*\.?\d*)([a-z])$")
DIVT = re.compile(r"^(-?)([a-z])/(\d+)$")
NUMT = re.compile(r"^-?\d+(\.\d+)?$")
BRK = re.compile(r"^(-?)(\d*\.?\d*)\(([a-z])([+-])(\d+(?:\.\d+)?)\)$")
RELS = ("<=", ">=", "<", ">", "=")


def V(v):
    return "<i>%s</i>" % v


def frac(top, bot):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (top, bot)


def split(s):
    for r in RELS:
        if " %s " % r in s:
            a, b = s.split(" %s " % r)
            return a, r, b
    raise ValueError(s)


def tok_val(tok):
    """-> (coefficient, constant) of one token"""
    m, d, b = TERM.match(tok), DIVT.match(tok), BRK.match(tok)
    if m:
        a = F(m.group(2)) if m.group(2) else F(1)
        return (-a if m.group(1) else a), F(0)
    if d:
        a = F(1, int(d.group(3)))
        return (-a if d.group(1) else a), F(0)
    if b:
        k = F(b.group(2)) if b.group(2) else F(1)
        k = -k if b.group(1) else k
        c = F(b.group(5)) * (1 if b.group(4) == "+" else -1)
        return k, k * c
    if NUMT.match(tok):
        return F(0), F(tok)
    raise ValueError(tok)


def side(t):
    """-> (coefficient of the letter, constant)"""
    A, B, sign = F(0), F(0), 1
    for tok in t.split(" "):
        if tok in ("+", "-"):
            sign = 1 if tok == "+" else -1
            continue
        a, b = tok_val(tok)
        A += sign * a
        B += sign * b
    return A, B


def parts(s):
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    return A1, B1, r, A2, B2


def solve(s):
    A1, B1, r, A2, B2 = parts(s)
    assert A1 != A2, s
    return (B2 - B1) / (A1 - A2)


def holds(s, x):
    A1, B1, r, A2, B2 = parts(s)
    l, rr = A1 * x + B1, A2 * x + B2
    return {"=": l == rr, "<": l < rr, ">": l > rr, "<=": l <= rr, ">=": l >= rr}[r]


def var_of(s):
    return re.search(r"[a-z]", s).group(0)


def R(s):
    """render the mini syntax as HTML"""
    out = []
    for tok in s.split(" "):
        m, d, b = TERM.match(tok), DIVT.match(tok), BRK.match(tok)
        if d:
            out.append((M if d.group(1) else "") + frac(V(d.group(2)), d.group(3)))
        elif m:
            out.append((M if m.group(1) else "") + m.group(2) + V(m.group(3)))
        elif b:
            out.append("%s%s(%s %s %s)" % (M if b.group(1) else "", b.group(2), V(b.group(3)),
                                           "+" if b.group(4) == "+" else M, b.group(5)))
        elif tok in SYM:
            out.append(SYM[tok])
        elif NUMT.match(tok):
            out.append(num(F(tok)))
        else:
            out.append({"-": M}.get(tok, tok))
    return " ".join(out)


FRAC = [False]      # True while explaining an equation written with x/3 (then 1/3 of x is shown as a fraction)


def is_div(s):
    return bool(re.search(r"[a-z]/\d", s))


def T(a, v):
    """A·v as HTML: 'x', '5x', '0.5x', '−x', '−3x'"""
    a = F(a)
    if a == 1:
        return V(v)
    if a == -1:
        return M + V(v)
    if FRAC[0] and a.numerator == 1 and a.denominator > 1:
        return frac(V(v), a.denominator)
    return num(a) + V(v)


def lin(A, B, v):
    """A·v + B as HTML"""
    if A == 0:
        return num(B)
    if B == 0:
        return T(A, v)
    return "%s %s %s" % (T(A, v), "+" if B > 0 else M, num(abs(B)))


def ntoks(t):
    toks = [x for x in t.split(" ") if x not in ("+", "-")]
    return (len([x for x in toks if TERM.match(x) or DIVT.match(x) or BRK.match(x)]),
            len([x for x in toks if NUMT.match(x)]), any(BRK.match(x) for x in toks))


# ------------------------------------------------------------ solving steps and checks
def sub_side(t, x):
    """'4 × (−5) + 9' for one side with the letter replaced by x"""
    out = []
    for tok in t.split(" "):
        m, d, b = TERM.match(tok), DIVT.match(tok), BRK.match(tok)
        if m:
            neg = M if m.group(1) else ""
            if m.group(2):
                out.append("%s%s × %s" % (neg, m.group(2), par(x)))
            elif neg or out:
                out.append(neg + par(x))
            else:
                out.append(num(x))
        elif d:
            out.append("%s%s ÷ %s" % (M if d.group(1) else "", par(x), d.group(3)))
        elif b:
            out.append("%s%s(%s %s %s)" % (M if b.group(1) else "", b.group(2), num(x),
                                           "+" if b.group(4) == "+" else M, b.group(5)))
        elif tok in ("+", "-"):
            out.append({"-": M}.get(tok, tok))
        else:
            out.append(num(F(tok)))
    return " ".join(out)


def check_text(s, x):
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    l, rr = A1 * x + B1, A2 * x + B2
    if A2 == 0 and len(b.split(" ")) == 1:
        return "Check: %s = %s ✓" % (sub_side(a, x), num(l))
    if A1 == 0 and len(a.split(" ")) == 1:
        return "Check: %s = %s ✓" % (sub_side(b, x), num(rr))
    return "Check: left side %s = %s; right side %s = %s ✓" % (sub_side(a, x), num(l), sub_side(b, x), num(rr))


def orient(s):
    """Which side the letter ends on. -> (left?, Ao, Bv, Bo): Ao·x + Bv on the letter side, Bo on the other,
    after the letter terms have been collected on one side."""
    A1, B1, r, A2, B2 = parts(s)
    if A2 == 0:
        left = True
    elif A1 == 0:
        left = False
    else:
        left = A1 > A2
    if left:
        return True, A1 - A2, B1, B2
    return False, A2 - A1, B2, B1


def steps(s):
    """Step-by-step explanation for an equation or inequality. Returns (text, x or k)."""
    v = var_of(s)
    FRAC[0] = is_div(s)
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    out = []
    ta, ca, ba = ntoks(a)
    tb, cb, bb = ntoks(b)
    if ba or bb:
        exps = []
        for tok in (a + " " + b).split(" "):
            m = BRK.match(tok)
            if m:
                k, c = tok_val(tok)
                exps.append("%s = %s" % (R(tok), lin(k, c, v)))
        out.append("Expand the brackets: %s (multiply <b>both</b> terms inside)." % "; ".join(exps))
    if ta + ca > 2 or tb + cb > 2 or (ba and ta + ca > 1) or (bb and tb + cb > 1) or ba or bb:
        out.append("Simplify each side: %s %s %s." % (lin(A1, B1, v), SYM[r], lin(A2, B2, v)))
    left, Ao, Bv, Bo = orient(s)
    rel = r
    if A1 != 0 and A2 != 0:
        mv = A2 if left else A1
        how = ("Subtract %s from both sides" % T(mv, v)) if mv > 0 else ("Add %s to both sides" % T(-mv, v))
        if left:
            out.append("%s: %s %s %s." % (how, lin(Ao, Bv, v), SYM[r], num(Bo)))
        else:
            out.append("%s: %s %s %s." % (how, num(Bo), SYM[r], lin(Ao, Bv, v)))
    Co = Bo - Bv
    if Bv != 0:
        how = ("Subtract %s from both sides" % num(Bv)) if Bv > 0 else ("Add %s to both sides" % num(-Bv))
        if left:
            out.append("%s: %s %s %s." % (how, T(Ao, v), SYM[r], num(Co)))
        else:
            out.append("%s: %s %s %s." % (how, num(Co), SYM[r], T(Ao, v)))
    x = Co / Ao
    if r != "=":
        assert Ao > 0, s
    final_rel = r if left else OPP[r]
    if Ao != 1:
        if FRAC[0] and Ao.numerator == 1 and Ao.denominator > 1:
            how = "Multiply both sides by %d: %s × %d = %s" % (Ao.denominator, par(Co), Ao.denominator, num(x))
        elif FRAC[0] and Ao.numerator == -1 and Ao.denominator > 1:
            how = "Multiply both sides by %s: %s × %s = %s" % (num(-Ao.denominator), par(Co), par(-Ao.denominator), num(x))
        else:
            how = "Divide both sides by %s: %s ÷ %s = %s" % (num(Ao), par(Co), par(Ao), num(x))
        out.append(how + ".")
    if left and Ao == 1:
        out[-1] = out[-1][:-1].replace("%s %s %s" % (V(v), SYM[r], num(x)), "<b>%s %s %s</b>" % (V(v), SYM[r], num(x))) + "."
    elif left:
        out.append("So <b>%s %s %s</b>." % (V(v), SYM[r], num(x)))
    else:
        if r == "=":
            out.append("So <b>%s = %s</b>." % (V(v), num(x)))
        else:
            out.append("%s %s %s is the same as <b>%s %s %s</b>." % (num(x), SYM[r], V(v), V(v), SYM[final_rel], num(x)))
    if r == "=":
        assert holds(s, x)
        out.append(check_text(s, x) + ".")
    FRAC[0] = False
    return " ".join(out), x, final_rel


def eq_wrongs(s, extra=None):
    """Answers from real mistakes for an equation, most common first. -> [(value, why)]"""
    A1, B1, r, A2, B2 = parts(s)
    left, Ao, Bv, Bo = orient(s)
    x = (Bo - Bv) / Ao
    v = var_of(s)
    out = list(extra or [])
    if A1 != 0 and A2 != 0 and A1 + A2 != 0:
        out.append(((B2 - B1) / (A1 + A2), "adding the %s-terms instead of subtracting them" % v))
    if Bv != 0:
        out.append(((Bo + Bv) / Ao, "using the wrong inverse: %s %s instead of %s it"
                    % ("subtracting" if Bv < 0 else "adding", num(abs(Bv)), "adding" if Bv < 0 else "subtracting")))
    out.append((-x, "a sign error in the last step"))
    if is_div(s) and Ao.numerator == 1 and Ao.denominator > 1:
        out.append((Bo - Bv, "forgetting to multiply by %d" % Ao.denominator))
        out.append(((Bo - Bv) / Ao.denominator ** 2, "dividing by %d instead of multiplying" % Ao.denominator))
        if Bv != 0 and A2 == 0:
            out.append((Bo / Ao - Bv, "multiplying by %d before dealing with the %s" % (Ao.denominator, num(Bv))))
    elif abs(Ao) != 1:
        out.append((Bo - Bv, "forgetting to divide by %s" % num(Ao)))
        if Bv != 0 and (A2 == 0 or A1 == 0):
            out.append((Bo / Ao - Bv, "dividing by %s before dealing with the %s" % (num(Ao), num(Bv))))
        out.append(((Bo - Bv) * Ao, "multiplying by %s instead of dividing" % num(Ao)))
    out.append((x + 1, None))
    out.append((x - 1, None))
    return out


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
    """correct + the first 3 unique distractors (strings). Positions are set later by balance()."""
    seen, pick = {plain(correct)}, []
    for c in cands:
        if c is None or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def fmt(v, unit=None):
    if unit is None:
        return num(v)
    if unit == "$":
        return money(v)
    sing, plur = unit
    return "%s %s" % (num(v), sing if v == 1 else plur)


def mcq_n(q, x, cands, e, unit=None, whole=True, neg=True, notes=True):
    """cands: (value, why) pairs or plain values. Only nice new values are used (whole numbers, or
    terminating decimals with at most 2 places when whole=False); the reasons are added to the explanation."""
    x = F(x)
    used, add = {x}, []
    for c in cands:
        val, why = c if isinstance(c, tuple) else (c, None)
        val = F(val)
        if val in used or val == 0 or (val < 0 and not neg):
            continue
        if whole and val.denominator != 1:
            continue
        if not whole and (val * 100).denominator != 1:
            continue
        used.add(val)
        add.append((val, why))
        if len(add) == 3:
            break
    assert len(add) == 3, (q, x, cands)
    it = mcq(q, fmt(x, unit), [fmt(w, unit) for w, _ in add], e)
    why = ["%s comes from %s" % (fmt(w, unit), t) for w, t in add if t]
    if notes and why:
        it["e"] += " Wrong answers: " + "; ".join(why) + "."
    return it


def solve_item(s, extra=None, whole=True, q=None):
    e, x, _ = steps(s)
    w = eq_wrongs(s, extra)
    if not whole:
        w = w[:-2] + [(x * 10, "misplacing the decimal point"), (x / 10, "misplacing the decimal point")] + w[-2:]
    return mcq_n(q or ("Solve: %s" % R(s)), x, w, e, whole=whole)


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("keep"):          # choices in a fixed order (Step 1, Step 2, ...)
                targets.remove(it["a"])
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.pop("keep", None)]
        for it, t in zip(free, targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [y for i, y in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, col=INK, italic=False, bold=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s%s fill='%s' text-anchor='middle'>%s</text>"
            % (x, y, fs, " font-style='italic'" if italic else "", " font-weight='700'" if bold else "", col, t))


def scale_svg(left, right, label):
    """A level pan balance. left / right: lists of a letter (a block of unknown mass) or a number (a weight)."""
    def item_w(t):
        return 34 if t.isalpha() else max(34, int(tw(t, 18) + 14))
    gap = 6

    def pan_w(items):
        return max(80, sum(item_w(t) for t in items) + gap * (len(items) - 1) + 16)
    wl, wr = pan_w(left), pan_w(right)
    cl = 8 + wl / 2
    cr = cl + wl / 2 + 44 + wr / 2
    mid = (cl + cr) / 2
    top, ih = 10, 34
    py = top + ih
    s = []
    for items, c, w in ((left, cl, wl), (right, cr, wr)):
        tot = sum(item_w(t) for t in items) + gap * (len(items) - 1)
        x = c - tot / 2
        for t in items:
            iw = item_w(t)
            if t.isalpha():
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, FILL, GREEN))
                s.append(text(x + iw / 2, top + 24, t, 18, col=RED, italic=True, bold=True))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, GREY, INK))
                s.append(text(x + iw / 2, top + 24, t, 18, bold=True))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    return svg_wrap(cr + wr / 2 + 8, by + 47, "".join(s), "pan balance: " + label)


GAP, PAD, FS = 30, 30, 15


def nline(lo, rel, k, v="x"):
    """Number line from lo to lo + 10 (integers, negatives with −). Circle at k: open for > <, closed for >= <=.
    A thick green arrow shows the solutions."""
    hi = lo + 10
    assert lo <= k <= hi
    W = 2 * PAD + GAP * 10
    Y, H = 24, 56
    X = lambda q: PAD + GAP * (q - lo)
    L, Rr = PAD - 22, W - PAD + 22
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (L + 2, Y, Rr - 2, Y, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (L, Y, L + 9, Y - 5, L + 9, Y + 5, INK),
         "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (Rr, Y, Rr - 9, Y - 5, Rr - 9, Y + 5, INK)]
    for q in range(lo, hi + 1):
        x = X(q)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, Y - (9 if q == 0 else 6), x, Y + (9 if q == 0 else 6), INK, "2.4" if q == 0 else "1.6"))
        s.append(text(x, Y + 26, num(q), FS))
    xc = X(k)
    end = Rr - 1 if RIGHT[rel] else L + 1
    tip = 12 if RIGHT[rel] else -12
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='5'/>" % (xc, Y, end - tip, Y, GREEN))
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (end, Y, end - tip, Y - 8, end - tip, Y + 8, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (xc, Y, GREEN if CLOSED[rel] else "#ffffff", GREEN))
    lab = "number line graph of %s %s %s" % (v, WORDS[rel], ("minus %d" % -k) if k < 0 else str(k))
    return svg_wrap(W, H, "".join(s), lab)


def window(rnd, k):
    return k - rnd.choice([3, 4, 5, 6, 7])


def sol(v, rel, k):
    return "%s %s %s" % (V(v), SYM[rel], num(k))


def describe(rel, k):
    return "%s circle at %s, arrow to the %s" % ("Closed" if CLOSED[rel] else "Open", num(k), "right" if RIGHT[rel] else "left")


def why_graph(rel, k, v="x"):
    circ = ("a closed (filled-in) circle, because %s is a solution" if CLOSED[rel]
            else "an open circle, because %s is not a solution") % num(k)
    side_ = "right, toward greater numbers" if RIGHT[rel] else "left, toward lesser numbers"
    return "%s has %s, and the arrow points %s." % (sol(v, rel, k), circ, side_)


def ineq(s):
    """-> (explanation, k, final relation) with k a whole number"""
    e, k, rel = steps(s)
    assert k.denominator == 1, s
    k = int(k)
    # verify: the boundary and its neighbours
    for t in (k - 1, k, k + 1):
        want = {">": t > k, "<": t < k, ">=": t >= k, "<=": t <= k}[rel]
        assert holds(s, t) == want, (s, t)
    return e, k, rel


NO_FLIP = ("You only reverse the sign when you multiply or divide both sides by a negative number. "
           "Here you divide by a positive number, so the sign stays the same, even though the answer is negative.")


# ------------------------------------------------------------ set 1: two-step equations with integers
def set_two_step(P):
    its = []
    its.append(mcq("What is the best first step to solve %s?" % R("5x - 8 = -23"),
                   "Add 8 to both sides",
                   ["Subtract 8 from both sides", "Divide both sides by 5", "Add 5 to both sides"],
                   "5%s − 8 means “multiply by 5, then subtract 8.” Undo the last step first: add 8 to both sides, "
                   "so 5%s = −15. Then divide by 5: %s = −3. Subtracting 8 uses the same operation instead of the inverse."
                   % (V("x"), V("x"), V("x"))))
    its.append(mcq("After you subtract 4 from both sides of %s, you get %s. What is the next step?"
                   % (R("-3x + 4 = 19"), R("-3x = 15")),
                   "Divide both sides by %s3" % M,
                   ["Divide both sides by 3", "Add 3 to both sides", "Multiply both sides by %s3" % M],
                   "%s means %s3 × %s. Undo × (%s3) by dividing both sides by %s3: %s = 15 ÷ (%s3) = %s5. "
                   "Dividing by 3 instead gives 5, the wrong sign. Check: %s3 × (%s5) + 4 = 15 + 4 = 19."
                   % (R("-3x"), M, V("x"), M, M, V("x"), M, M, M, M)))
    its.append(mcq("Is %s = %s3 a solution of %s? Which check is correct?" % (V("x"), M, R("4x + 5 = -7")),
                   "Yes, because 4 × (%s3) + 5 = %s7" % (M, M),
                   ["No, because 4 × (%s3) + 5 = %s17" % (M, M), "No, because 4 × 3 + 5 = 17",
                    "No, because 4 + (%s3) + 5 = 6" % M],
                   "Put %s3 in for %s: 4 × (%s3) = %s12, and %s12 + 5 = %s7. Both sides are %s7, so %s3 is a solution. "
                   "%s12 + 5 is %s7, not %s17: you move 5 to the right from %s12 on a number line. 4%s means 4 × %s, not 4 + %s."
                   % (M, V("x"), M, M, M, M, M, M, M, M, M, M, V("x"), V("x"), V("x"))))
    for s in ["2x + 9 = 3", "3x - 5 = -20", "4x + 11 = -13", "5x - 2 = 18", "-2x + 7 = 15", "-x + 6 = 11",
              "-3x - 4 = 14", "8 - 3x = 23", "-6x + 5 = -19", "7x + 20 = -1", "12 - 5x = -8", "x/3 + 4 = -2",
              "-9 = 2x + 5", "x/4 - 6 = -9", "-4x - 10 = -2", "6x - 15 = -45", "-26 = -5x + 4"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Two-step equations with integers", "items": its}


# ------------------------------------------------------------ set 2: variables on both sides
def set_both_sides(P):
    its = []
    for s, l, r in [("3x + 4 = x + 10", ["x", "x", "x", "4"], ["x", "10"]),
                    ("4x + 2 = 2x + 12", ["x", "x", "x", "x", "2"], ["x", "x", "12"])]:
        x = solve(s)
        A1, B1, _, A2, B2 = parts(s)
        svg = scale_svg(l, r, "%d blocks x and %d balance %d blocks x and %d" % (A1, B1, A2, B2))
        e = ("The balance shows %s. Take %s off both pans: %s = %s. Then take %d off both pans: %s = %s. "
             "So each block is %s ÷ %s = %s. %s."
             % (R(s), T(A2, "x"), lin(A1 - A2, B1, "x"), num(B2), B1, T(A1 - A2, "x"), num(B2 - B1),
                num(B2 - B1), num(A1 - A2), num(x), check_text(s, x)))
        its.append(mcq_n(fig(svg) + "The pan balance is level. Each block has the same mass, %s. What is %s?" % (V("x"), V("x")),
                         x, eq_wrongs(s), e, neg=False))
    its.append(mcq("What is a good first step to solve %s?" % R("7x + 3 = 4x - 12"),
                   "Subtract 4%s from both sides" % V("x"),
                   ["Add 4%s to both sides" % V("x"), "Divide both sides by 7", "Subtract 3 from the left side only"],
                   "Get the %s-terms on one side. Subtract 4%s from both sides: 3%s + 3 = %s12. Then subtract 3: 3%s = %s15, "
                   "so %s = %s5. Adding 4%s gives 11%s, which does not remove the %s-term on the right. "
                   "Whatever you do, do it to <b>both</b> sides."
                   % (V("x"), V("x"), V("x"), M, V("x"), M, V("x"), M, V("x"), V("x"), V("x"))))
    br = {"3(x-2) = x + 8": [(5, "expanding 3(%s − 2) as 3%s − 2" % (V("x"), V("x")))],
          "5(x+2) = 3(x-4)": [(-3, "expanding as 5%s + 2 = 3%s − 4" % (V("x"), V("x")))]}
    for s in ["5x - 7 = 2x + 8", "x + 14 = 3x + 2", "4x + 9 = x - 6", "6x + 1 = 2x - 11", "2x - 5 = 6x + 11",
              "9 - 2x = x + 21", "3x + 2 - x = 14", "-3x + 8 = x - 12", "7x - 4 = 3x + 24", "3(x-2) = x + 8",
              "2(x+5) = 4x - 6", "-2(x-4) = 3x - 7", "4x + 3 - x + 5 = 2x + 1", "5(x+2) = 3(x-4)"]:
        its.append(solve_item(s, br.get(s)))
    # check a solution
    s = "4x - 1 = x - 13"
    assert holds(s, -4)
    its.append(mcq("Is %s = %s4 a solution of %s? Which check is correct?" % (V("x"), M, R(s)),
                   "Yes: both sides equal %s17" % M,
                   ["No: the left side is %s15 and the right side is %s17" % (M, M),
                    "No: the left side is %s17 and the right side is %s9" % (M, M),
                    "Yes: both sides equal 15"],
                   "Left side: 4 × (%s4) − 1 = %s16 − 1 = %s17. Right side: %s4 − 13 = %s17. Both sides are equal, so %s4 is a solution. "
                   "%s16 − 1 is %s17, not %s15, and %s4 − 13 is %s17, not %s9." % ((M,) * 12)))
    # find the step with the mistake
    its.append(mcq("Noah solved %s:<br>Step 1: %s<br>Step 2: %s<br>Step 3: %s = 2<br>Which step has a mistake?"
                   % (R("6x - 4 = 2x + 12"), R("4x - 4 = 12"), R("4x = 8"), V("x")),
                   "Step 2", ["Step 1", "Step 3", "There is no mistake"],
                   "Step 1 is right: subtract 2%s from both sides. In Step 2, undo − 4 by <b>adding</b> 4: 4%s = 16, not 8. "
                   "Then %s = 4. Check: 6 × 4 − 4 = 20 and 2 × 4 + 12 = 20 ✓." % (V("x"), V("x"), V("x"))))
    its[-1]["c"] = ["Step 1", "Step 2", "Step 3", "There is no mistake"]
    its[-1]["a"] = 1
    its[-1]["keep"] = True
    assert solve("3(x+4) = x - 6") == -9
    its.append(mcq("Emma solved %s:<br>Step 1: %s<br>Step 2: %s<br>Step 3: %s<br>Step 4: %s = %s5<br>Which step has a mistake?"
                   % (R("3(x+4) = x - 6"), R("3x + 4 = x - 6"), R("2x + 4 = -6"), R("2x = -10"), V("x"), M),
                   "Step 1", ["Step 2", "Step 3", "Step 4"],
                   "In Step 1 the 3 must multiply <b>both</b> terms in the brackets: 3(%s + 4) = 3%s + 12. "
                   "Then 2%s + 12 = %s6, so 2%s = %s18 and %s = %s9. Check: 3(%s9 + 4) = 3 × (%s5) = %s15 and %s9 − 6 = %s15 ✓."
                   % (V("x"), V("x"), V("x"), M, V("x"), M, V("x"), M, M, M, M, M, M)))
    its[-1]["c"] = ["Step 1", "Step 2", "Step 3", "Step 4"]
    its[-1]["a"] = 0
    its[-1]["keep"] = True
    assert len(its) == 20, len(its)
    return {"title": "Variables on both sides", "items": its}


# ------------------------------------------------------------ set 3: decimals
def set_decimals(P):
    its = []
    its.append(mcq("Multiply every term of %s by 10. Which equation do you get?" % R("0.3x + 1.5 = 2.4"),
                   R("3x + 15 = 24"), [R("3x + 1.5 = 2.4"), R("3x + 15 = 2.4"), R("0.3x + 15 = 24")],
                   "Multiply <b>every</b> term by 10: 0.3%s × 10 = 3%s, 1.5 × 10 = 15 and 2.4 × 10 = 24. "
                   "The new equation has no decimals and the same solution: 3%s = 9, so %s = 3. "
                   "Check: 0.3 × 3 + 1.5 = 0.9 + 1.5 = 2.4 ✓." % (V("x"), V("x"), V("x"), V("x"))))
    its.append(mcq("What is the best first step to solve %s?" % R("0.5x - 1.2 = 3.8"),
                   "Add 1.2 to both sides",
                   ["Subtract 1.2 from both sides", "Divide both sides by 5", "Multiply both sides by 0.5"],
                   "Undo − 1.2 first by adding 1.2 to both sides: 0.5%s = 5. Then divide by 0.5: %s = 10. "
                   "Multiplying by 0.5 does not undo × 0.5, and 0.5%s is not 5%s." % (V("x"), V("x"), V("x"), V("x"))))
    br = {"2.5(x-2) = 6": [(F(16, 5), "expanding 2.5(%s − 2) as 2.5%s − 2" % (V("x"), V("x")))]}
    for s in ["0.4x + 1.2 = 3.6", "0.5x - 1.2 = 3.8", "0.2x - 1.4 = 1.2", "1.5x - 2 = 4.75", "2.5x + 3.5 = -6.5",
              "-0.8x + 2 = 6", "4.2 - 0.3x = 6", "0.25x + 1.75 = 4", "x/2 + 1.5 = -3.5", "3x + 0.8 = x + 5.6",
              "1.2x + 4 = 0.7x + 6.5", "0.6x - 2.5 = 0.1x + 1", "2.4x = 1.6x + 6", "2.5(x-2) = 6",
              "3.2x - 1.5 = 1.2x + 4.5", "-1.5x + 0.5 = -5.5", "0.9x + 4.2 = 0.3x", "5x - 3.75 = 2x + 4.5"]:
        its.append(solve_item(s, br.get(s), whole=False))
    assert len(its) == 20, len(its)
    return {"title": "Equations with decimals", "items": its}


# ------------------------------------------------------------ set 4: inequalities with integers
def set_ineq(rnd, P):
    its = []
    # a) solve
    for s in ["2x + 7 < 1", "3x - 4 >= -16", "5x + 12 > 2", "x/3 + 5 >= 3", "4x + 3 <= x - 9", "2x - 3 < 5x + 9"]:
        e, k, rel = ineq(s)
        left, Ao, Bv, Bo = orient(s)
        kw = (Bo + Bv) / Ao
        cands = [sol("x", OPP[rel], k), sol("x", SWAP[rel], k)]
        if kw.denominator == 1 and kw != k:
            cands.append(sol("x", rel, kw))
        cands.append(sol("x", rel, -k))
        if not left:
            e += " Do not write %s: the sign stays the same, you only read it from the other side." % sol("x", OPP[rel], k)
        else:
            e += " The sign stays %s: you only reverse it when you multiply or divide by a negative number." % SYM[rel]
        its.append(mcq("Solve: %s" % R(s), sol("x", rel, k), cands, e))
    # b) graph -> which inequality
    for s, alt in [("3x + 5 > -4", "3x + 5 > -1"), ("2x - 1 <= -9", "2x + 1 <= -9"),
                   ("4x + 10 < 2", "4x - 10 < 2"), ("5x - 8 >= 2x + 1", "5x - 8 >= 2x - 2")]:
        e, k, rel = ineq(s)
        ea, ka, ra = ineq(alt)
        assert ka != k
        a, r, b = split(s)
        svg = nline(window(rnd, k), rel, k)
        right = R(s)
        wrong = [R("%s %s %s" % (a, SWAP[r], b)), R("%s %s %s" % (a, OPP[r], b)), R(alt)]
        e2 = ("The graph shows %s: %s circle at %s, arrow to the %s. Solve %s: %s %s gives %s instead."
              % (sol("x", rel, k), "a closed" if CLOSED[rel] else "an open", num(k), "right" if RIGHT[rel] else "left",
                 R(s), e, R(alt), sol("x", ra, ka)))
        its.append(mcq(fig(svg) + "The graph shows the solution of which inequality?", right, wrong, e2))
    # c) how to graph
    for s in ["6x + 4 <= -14", "x + 8 > 3x + 2"]:
        e, k, rel = ineq(s)
        right = describe(rel, k)
        wrong = [describe(SWAP[rel], k), describe(OPP[rel], k), describe(OPP[SWAP[rel]], k)]
        its.append(mcq("How do you graph the solution of %s on a number line?" % R(s), right, wrong,
                       "First solve: %s %s" % (e, why_graph(rel, k))))
    # d) which number is (not) a solution
    for s, r_, ws, want in [("3x + 5 > -4", -2, [-3, -4, -6], True),
                            ("2x - 6 <= -10", -2, [-1, 1, 3], True),
                            ("4x + 1 < 2x - 7", -4, [-5, -6, -8], False)]:
        e, k, rel = ineq(s)
        assert holds(s, r_) == want and all(holds(s, w) != want for w in ws)
        A1, B1, _, A2, B2 = parts(s)
        a, r, b = split(s)
        tests = "; ".join("%s: %s %s %s is %s" % (num(t), num(A1 * t + B1), SYM[r], num(A2 * t + B2),
                                                 "true" if holds(s, t) else "false") for t in [r_] + ws)
        q = "Which number is %sa solution of %s?" % ("" if want else "<b>not</b> ", R(s))
        it = mcq_n(q, r_, ws, "Test each number in both sides. %s. Solving gives %s." % (tests, sol("x", rel, k)), notes=False)
        its.append(it)
    # e) reversing the sign when it should not be reversed
    for s, nm_wrote in [("3x + 6 < -9", None), ("2x - 5 >= -11", None)]:
        nm, he, his = P.next()
        e, k, rel = ineq(s)
        wrote = sol("x", OPP[rel], k)
        right = "The sign should stay %s" % SYM[rel]
        wrong = ["The answer should be %s" % sol("x", OPP[rel], -k), "The answer should be %s" % sol("x", SWAP[OPP[rel]], k),
                 "Nothing is wrong"]
        its.append(mcq("%s solved %s and wrote %s. What is wrong?" % (nm, R(s), wrote), right, wrong,
                       "%s %s The answer is %s." % (e, NO_FLIP, sol("x", rel, k))))
    # f) find the mistake in a graph
    for s, drawn, kd, why in [("2x + 9 > 1", "<", -4, "flip"), ("3x - 2 <= -11", "<", -3, "circle"),
                              ("4x + 7 >= -5", ">=", 3, "place")]:
        nm, he, his = P.next()
        e, k, rel = ineq(s)
        svg = nline(window(rnd, min(k, kd)) if kd != k else window(rnd, k), drawn, kd)
        if why == "flip":
            right = "The arrow should point right"
            wrong = ["The circle should be closed", "The circle should be at %s" % num(-k), "Nothing is wrong"]
            why_t = "%s reversed the sign because the answer is negative. %s" % (nm, NO_FLIP)
        elif why == "circle":
            right = "The circle should be closed"
            wrong = ["The arrow should point right", "The circle should be at %s" % num(k - 1), "Nothing is wrong"]
            why_t = "%s used an open circle, but ≤ includes %s." % (nm, num(k))
        else:
            right = "The circle should be at %s" % num(k)
            wrong = ["The circle should be open", "The arrow should point left", "Nothing is wrong"]
            why_t = "%s made a sign error: %s5 − 7 = %s12, not 12, and %s12 ÷ 4 = %s3." % (cap(he), M, M, M, M)
        q = fig(svg) + "%s solved %s and drew this graph. What is wrong?" % (nm, R(s))
        its.append(mcq(q, right, wrong, "%s %s %s" % (e, why_graph(rel, k), why_t)))
    assert len(its) == 20, len(its)
    return {"title": "Inequalities with integers and graphs", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(P):
    its = []
    X = V
    # 1 phone plans
    s = "5g + 30 = 2g + 45"
    e, x, _ = steps(s)
    its.append(mcq_n("Phone plan A costs $30 a month plus $5 for each GB of data. Plan B costs $45 a month plus $2 for each GB. "
                     "For how many GB do the plans cost the same?",
                     x, [(F(75, 3), "adding 30 and 45 instead of subtracting"), (15, "forgetting to divide by 3"),
                         (F(15, 7), None), (3, "leaving out plan B’s $2 per GB (5%s + 30 = 45)" % X("g"))],
                     "Let %s be the number of GB: %s. %s Both plans cost $55." % (X("g"), R(s), e), unit=("GB", "GB"), neg=False))
    # 2 Winnipeg morning
    s = "-18 + 3h = -3"
    e, x, _ = steps(s)
    its.append(mcq_n("At 6:00 a.m. in Winnipeg, the temperature is %s18 °C. It rises 3 °C each hour. "
                     "After how many hours is it %s3 °C?" % (M, M), x,
                     [(7, "subtracting 18 instead of adding it (%s21 ÷ 3 = %s7)" % (M, M)), (15, "forgetting to divide by 3"),
                      (6, "dividing 18 by 3 and ignoring the %s3 °C" % M)],
                     "Let %s be the number of hours: %s. %s So it is %s3 °C at 11:00 a.m." % (X("h"), R(s), e, M),
                     unit=("hour", "hours"), neg=False))
    # 3 temperature falling
    s = "4 - 2h = -10"
    e, x, _ = steps(s)
    its.append(mcq_n("At noon the temperature in Ottawa is 4 °C. It falls 2 °C each hour. After how many hours is it %s10 °C?" % M,
                     x, [(3, "using 10 − 4 = 6 instead of %s10 − 4 = %s14" % (M, M)), (14, "forgetting to divide by 2"),
                         (5, "dividing 10 by 2")],
                     "Let %s be the number of hours: %s. %s So it is %s10 °C at 7:00 p.m." % (X("h"), R(s), e, M),
                     unit=("hour", "hours"), neg=False))
    # 4 gym
    s = "6v + 40 = 10v"
    e, x, _ = steps(s)
    its.append(mcq_n("A community centre gym charges members $40 a year plus $6 a visit. Non-members pay $10 a visit. "
                     "For how many visits is the cost the same?", x,
                     [(F(40, 16), None), (4, "dividing 40 by 10"), (40, "forgetting to divide by 4"), (100, "giving the cost in dollars")],
                     "Let %s be the number of visits: %s. %s Both cost $100." % (X("v"), R(s), e), unit=("visit", "visits"), neg=False))
    # 5 hockey cards
    n1, he1, his1 = P.next()
    n2, he2, his2 = P.next()
    s = "4w + 48 = 7w + 12"
    e, x, _ = steps(s)
    its.append(mcq_n("%s has 48 hockey cards and adds 4 each week. %s has 12 cards and adds 7 each week. "
                     "After how many weeks will they have the same number of cards?" % (n1, n2), x,
                     [(36, "forgetting to divide by 3"), (F(60, 3), "adding 48 and 12 instead of subtracting"),
                      (F(36, 11), None), (96, "giving the number of cards")],
                     "Let %s be the number of weeks: %s. %s They each have 96 cards." % (X("w"), R(s), e),
                     unit=("week", "weeks"), neg=False))
    # 6 taxi
    s = "2.25k + 4.5 = 27"
    e, x, _ = steps(s)
    its.append(mcq_n("A taxi charges $4.50 plus $2.25 for each kilometre. A ride costs $27.00. How long is the ride?", x,
                     [(14, "adding 4.50 instead of subtracting it (31.50 ÷ 2.25)"), (12, "dividing 27 by 2.25 and forgetting the $4.50"),
                      (F(225, 10), "forgetting to divide by 2.25")],
                     "Let %s be the number of kilometres: %s. %s" % (X("k"), R(s), e), unit=("km", "km"), whole=False, neg=False))
    # 7 bike share
    s = "0.12m + 1 = 4.6"
    e, x, _ = steps(s)
    n, he, his = P.next()
    its.append(mcq_n("A bike-share bike costs $1.00 to unlock plus $0.12 a minute. %s’s ride costs $4.60. How many minutes did %s ride?"
                     % (n, he), x,
                     [(300, "misplacing the decimal point (3.6 ÷ 0.012)"), (F(36, 10), "forgetting to divide by 0.12"),
                      (3, "misplacing the decimal point (3.6 ÷ 1.2)")],
                     "Let %s be the number of minutes: %s. %s" % (X("m"), R(s), e), unit=("minute", "minutes"), whole=False, neg=False))
    # 8 garden
    its.append(mcq_n("A rectangular garden is 3 m longer than twice its width. Its perimeter is 54 m. What is its width?",
                     8, [(19, "giving the length"), (17, "using only one width and one length (3%s + 3 = 54)" % X("w")),
                         (9, "dividing 54 by 6 and forgetting the 3 m")],
                     "Let %s be the width. The length is 2%s + 3. Perimeter: 2(%s + 2%s + 3) = 54, so 6%s + 6 = 54. "
                     "Subtract 6: 6%s = 48. Divide by 6: %s = 8 m. The length is 19 m. Check: 2 × (8 + 19) = 54 ✓."
                     % ((X("w"),) * 7), unit=("m", "m"), neg=False))
    # 9 consecutive integers
    s = "3n + 3 = -33"
    e, x, _ = steps(s)
    its.append(mcq_n("The sum of three consecutive integers is %s33. What is the least of the three integers?" % M, x,
                     [(-11, "giving the middle integer"), (-10, "giving the greatest integer"), (12, "a sign error in the last step")],
                     "Let the integers be %s, %s + 1 and %s + 2. Their sum is 3%s + 3 = %s33. %s The integers are %s12, %s11 and %s10."
                     % (X("n"), X("n"), X("n"), X("n"), M, e, M, M, M)))
    # 10 owes money
    n, he, his = P.next()
    s = "6w - 12 = 36"
    e, x, _ = steps(s)
    its.append(mcq_n("%s owes %s sister $12, so %s balance is %s$12. %s saves $6 each week. After how many weeks will %s balance be $36?"
                     % (n, his, his, M, cap(he), his), x,
                     [(4, "subtracting 12 instead of adding it"), (48, "forgetting to divide by 6"),
                      (6, "ignoring the $12 owed")],
                     "Let %s be the number of weeks: %s12 + 6%s = 36. %s" % (X("w"), M, X("w"), e), unit=("week", "weeks"), neg=False))
    # 11 bus budget (inequality)
    s = "15s + 350 <= 800"
    e, k, rel = ineq(s)
    its.append(mcq_n("A Grade 8 field trip costs $350 for the bus plus $15 for each student. The budget is at most $800. "
                     "What is the greatest number of students who can go?", k,
                     [(450, "forgetting to divide by 15"), (F(1150, 15), None), (29, "using &lt; instead of ≤"),
                      (53, "dividing 800 by 15")],
                     "Let %s be the number of students: %s. %s So at most 30 students can go. Check: 15 × 30 + 350 = 800, which is allowed."
                     % (X("s"), R(s), e), unit=("student", "students"), neg=False))
    # 12 savings (inequality)
    n, he, his = P.next()
    s = "12w + 56 >= 200"
    e, k, rel = ineq(s)
    its.append(mcq_n("%s has $56 and saves $12 each week. %s wants at least $200 for a new pair of skates. "
                     "What is the least number of weeks %s must save?" % (n, cap(he), he), k,
                     [(144, "forgetting to divide by 12"), (F(256, 12), None), (11, "stopping one week short"),
                      (17, "dividing 200 by 12 and rounding")],
                     "Let %s be the number of weeks: %s. %s After 12 weeks %s has 12 × 12 + 56 = $200."
                     % (X("w"), R(s), e, he), unit=("week", "weeks"), neg=False))
    # 13 canoe rental: which equation
    its.append(mcq("To rent a canoe, Outfitter A charges $60 plus $20 a day. Outfitter B charges $35 a day. "
                   "Which equation finds the number of days %s when the costs are the same?" % X("d"),
                   R("60 + 20d = 35d"), [R("60d + 20 = 35d"), R("60 + 20d + 35d = 0"), R("60 + 20 = 35d")],
                   "Outfitter A: 60 + 20%s. Outfitter B: 35%s. Same cost: 60 + 20%s = 35%s. "
                   "Subtract 20%s: 60 = 15%s, so %s = 4 days (both cost $140)." % ((X("d"),) * 7)))
    assert solve("60 + 20d = 35d") == 4
    # 14 ages
    n, he, his = P.next()
    s = "3a + 12 = 2(a+12)"
    e, x, _ = steps(s)
    its.append(mcq_n("%s’s mother is 3 times as old as %s. In 12 years, she will be twice as old as %s. How old is %s now?"
                     % (n, n, n, n), x,
                     [(24, "giving %s’s age in 12 years" % n), (36, "giving the mother’s age now"),
                      (48, "giving the mother’s age in 12 years")],
                     "Let %s be %s’s age now. Mother: 3%s. In 12 years: 3%s + 12 = 2(%s + 12). %s"
                     % (X("a"), n, X("a"), X("a"), X("a"), e), unit=("years old", "years old"), neg=False))
    # 15 maple syrup
    n, he, his = P.next()
    s = "4p + 6.5 = 56.5"
    e, x, _ = steps(s)
    its.append(mcq_n("At a sugar bush, %s buys 4 bottles of maple syrup at the same price and a $6.50 box of maple candy. "
                     "%s pays $56.50. What does one bottle cost?" % (n, cap(he)), x,
                     [(50, "forgetting to divide by 4"), (F(63, 4), "adding 6.50 instead of subtracting it"),
                      (F(125, 100), "misplacing the decimal point")],
                     "Let %s be the price of one bottle: %s. %s" % (X("p"), R(s), e), unit="$", whole=False, neg=False))
    # 16 balloons
    s = "1200 - 35t = 450 + 40t"
    e, x, _ = steps(s)
    its.append(mcq_n("A hot-air balloon at 1200 m comes down 35 m each minute. A second balloon at 450 m goes up 40 m each minute. "
                     "After how many minutes are they at the same height?", x,
                     [(150, "subtracting the rates instead of adding them (750 ÷ 5)"),
                      (750, "forgetting to divide by 75"), (22, "adding 1200 and 450 instead of subtracting (1650 ÷ 75)")],
                     "Let %s be the number of minutes: %s. %s Both are at 850 m." % (X("t"), R(s), e),
                     unit=("minute", "minutes"), neg=False))
    # 17 which inequality: temperature
    its.append(mcq("On a cold morning the temperature is %s14 °C. It rises 3 °C each hour. Which inequality shows when the "
                   "temperature is above 4 °C after %s hours?" % (M, X("h")),
                   R("-14 + 3h > 4"), [R("-14 + 3h < 4"), R("14 + 3h > 4"), R("-14h + 3 > 4")],
                   "Start at %s14 and add 3 for each hour: %s14 + 3%s. “Above 4” means &gt; 4. Solving: 3%s &gt; 18, so %s &gt; 6. "
                   "After 6 hours it is exactly 4 °C." % (M, M, X("h"), X("h"), X("h"))))
    assert ineq("3h - 14 > 4")[1] == 6
    # 18 transit card (inequality, round down)
    n, he, his = P.next()
    s = "3.25r + 10 <= 40"
    A = F(30) / F("3.25")
    assert 9 < A < 10
    its.append(mcq_n("%s has $40 on a transit card. Each ride costs $3.25. %s wants to keep at least $10 on the card, so "
                     "3.25%s + 10 ≤ 40. What is the greatest number of rides %s can take?" % (n, cap(he), X("r"), he), 9,
                     [(10, "rounding 9.23 up instead of down"), (30, "forgetting to divide by 3.25"),
                      (15, "adding 10 instead of subtracting it (50 ÷ 3.25 ≈ 15.4)")],
                     "Subtract 10: 3.25%s ≤ 30. Divide by 3.25: %s ≤ 9.23… Rides are whole numbers, so the greatest is 9. "
                     "Check: 9 rides cost $29.25 and leave $10.75. 10 rides cost $32.50 and leave only $7.50."
                     % (X("r"), X("r")), unit=("rides", "rides"), neg=False))
    # 19 hoodies
    n, he, his = P.next()
    s = "3(p-8) = 96"
    e, x, _ = steps(s)
    its.append(mcq_n("%s buys 3 hoodies on sale. Each one is $8 off the regular price %s. %s pays $96 in all. What is the regular price?"
                     % (n, X("p"), cap(he)), x,
                     [(24, "subtracting 8 instead of adding it"), (32, "giving the sale price"), (104, "forgetting to divide by 3"),
                      (F(104, 3), None)],
                     "3(%s − 8) = 96. Divide both sides by 3: %s − 8 = 32. Add 8: %s = 40. Check: 3 × (40 − 8) = 3 × 32 = 96 ✓."
                     % (X("p"), X("p"), X("p")), unit="$", neg=False))
    assert solve(s) == 40
    # 20 electricity plans
    s = "0.12k + 35 = 0.15k + 20"
    e, x, _ = steps(s)
    its.append(mcq_n("Electricity plan A costs $35 a month plus $0.12 per kWh. Plan B costs $20 a month plus $0.15 per kWh. "
                     "For how many kWh do the plans cost the same?", x,
                     [(50, "misplacing the decimal point"), (5000, "misplacing the decimal point"), (15, "forgetting to divide by 0.03"),
                      (F(55, 3) * 100, None)],
                     "Let %s be the number of kWh: %s. %s Both plans cost $95." % (X("k"), R(s), e), unit=("kWh", "kWh"), neg=False))
    assert len(its) == 20, len(its)
    return {"title": "Equation and inequality word problems", "items": its}


# ------------------------------------------------------------ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    X = V("x")
    return (
        "<h2>Solve two-step equations with integers</h2>"
        "<p>To solve an equation, find the value of the variable that makes both sides equal. "
        "<b>Undo the operations in reverse order</b>, and do the same thing to both sides. "
        "Integers do not change the steps, but watch every sign.</p>" +
        ex("Example 1", "Solve " + R("3x + 8 = -7") + ".",
           "Subtract 8 from both sides: 3" + X + " = −15. Divide both sides by 3: " + X + " = −5. "
           "Check: 3 × (−5) + 8 = −15 + 8 = −7 ✓.", X + " = −5") +
        ex("Example 2", "Solve " + R("-2x + 7 = 15") + ".",
           "Subtract 7: −2" + X + " = 8. Divide both sides by −2: " + X + " = 8 ÷ (−2) = −4. "
           "Check: −2 × (−4) + 7 = 8 + 7 = 15 ✓.", X + " = −4") +
        "<h2>Variables on both sides</h2>"
        "<p>First get all the variable terms on one side. Subtract the smaller variable term from both sides. "
        "Then move the numbers and divide, as before.</p>"
        "<figure class='sn-fig'>" + scale_svg(["x", "x", "x", "4"], ["x", "10"], "3 blocks x and 4 balance 1 block x and 10") +
        "<figcaption>3" + X + " + 4 = " + X + " + 10. Take one " + X + " off both pans: 2" + X + " + 4 = 10. "
        "Take 4 off both pans: 2" + X + " = 6, so " + X + " = 3.</figcaption></figure>" +
        ex("Example 3", "Solve " + R("7x + 3 = 4x - 12") + ".",
           "Subtract 4" + X + " from both sides: 3" + X + " + 3 = −12. Subtract 3: 3" + X + " = −15. Divide by 3: " + X + " = −5. "
           "Check: left 7 × (−5) + 3 = −32; right 4 × (−5) − 12 = −32 ✓.", X + " = −5") +
        ex("Example 4", "Solve " + R("3(x-2) = x + 8") + ".",
           "Expand: the 3 multiplies both terms, so 3" + X + " − 6 = " + X + " + 8. Subtract " + X + ": 2" + X + " − 6 = 8. "
           "Add 6: 2" + X + " = 14, so " + X + " = 7. Check: 3(7 − 2) = 15 and 7 + 8 = 15 ✓.", X + " = 7") +
        "<h2>Equations with decimals</h2>"
        "<p>Use the same steps. If the decimals get in the way, multiply <b>every</b> term by 10 or 100 first.</p>" +
        ex("Example 5", "Solve " + R("0.4x + 1.2 = 3.6") + ".",
           "Multiply every term by 10: 4" + X + " + 12 = 36. Subtract 12: 4" + X + " = 24. Divide by 4: " + X + " = 6. "
           "Check: 0.4 × 6 + 1.2 = 2.4 + 1.2 = 3.6 ✓.", X + " = 6") +
        "<h2>Inequalities with integers</h2>"
        "<p>An <b>inequality</b> uses &lt;, &gt;, ≤ or ≥. Solve it with the same steps; the answer is a range of numbers. "
        "A negative answer does <b>not</b> change the sign. The sign only reverses if you multiply or divide both sides "
        "by a negative number. To avoid that, collect the variable on the side with the greater coefficient.</p>" +
        ex("Example 6", "Solve " + R("2x + 7 < 1") + " and graph the solution.",
           "Subtract 7: 2" + X + " &lt; −6. Divide by 2 (a positive number, so the sign stays): " + X + " &lt; −3. "
           "Test −4: 2 × (−4) + 7 = −1, and −1 &lt; 1 is true ✓.", X + " &lt; −3") +
        "<figure class='sn-fig'>" + nline(-8, "<", -3) +
        "<figcaption>" + X + " &lt; −3: open circle at −3 (−3 is not a solution), arrow to the left.</figcaption></figure>" +
        ex("Example 7", "Solve " + R("2x - 3 < 5x + 9") + ".",
           "Subtract 2" + X + " from both sides: −3 &lt; 3" + X + " + 9. Subtract 9: −12 &lt; 3" + X + ". "
           "Divide by 3: −4 &lt; " + X + ", which is the same as " + X + " &gt; −4.", X + " &gt; −4") +
        "<figure class='sn-fig'>" + nline(-7, ">", -4) +
        "<figcaption>" + X + " &gt; −4: open circle at −4, arrow to the right (toward −3, −2, −1, …).</figcaption></figure>" +
        table(["Symbol", "Circle", "Arrow"], [
            ["&lt;", "open", "left"], ["≤", "closed (filled in)", "left"],
            ["&gt;", "open", "right"], ["≥", "closed (filled in)", "right"]]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [R("5x - 8 = -23") + ": subtract 8", "Use the inverse: add 8, so 5" + X + " = −15"],
            [R("-2x = 8") + ", so " + X + " = 4", "Divide by −2: " + X + " = −4"],
            [R("5x - 7 = 2x + 8") + " becomes 7" + X + " − 7 = 8", "Subtract 2" + X + " from both sides: 3" + X + " − 7 = 8"],
            ["3(" + X + " − 2) = 3" + X + " − 2", "Multiply both terms: 3" + X + " − 6"],
            [R("2x + 7 < 1") + " gives " + X + " &gt; −3", "Keep the sign: " + X + " &lt; −3"],
            ["−4 &lt; " + X + " read as " + X + " &lt; −4", "−4 &lt; " + X + " means " + X + " &gt; −4"],
        ])
    )


FAQ = [
    {"q": "What equations do Grade 8 students solve in the Ontario math curriculum?",
     "a": "In Grade 8 Algebra (C2.3), students solve equations with several terms, integers and decimal numbers, such as 3x + 8 = −7 or 3x + 4 = x + 10, and verify their solutions. They also solve inequalities with integers (C2.4) and graph the solutions on a number line."},
    {"q": "How do you solve an equation with the variable on both sides, like 3x + 4 = x + 10?",
     "a": "Subtract x from both sides to get 2x + 4 = 10. Subtract 4 to get 2x = 6, then divide by 2, so x = 3. Check: 3 × 3 + 4 = 13 and 3 + 10 = 13."},
    {"q": "When do you reverse the sign of an inequality?",
     "a": "Only when you multiply or divide both sides by a negative number. A negative answer does not reverse it: 2x + 7 < 1 gives 2x < −6, so x < −3."},
    {"q": "How do you solve an equation with decimals, like 0.4x + 1.2 = 3.6?",
     "a": "Use the same steps, or multiply every term by 10 first to get 4x + 12 = 36. Either way, x = 6. Check: 0.4 × 6 + 1.2 = 3.6."},
]


def gen_unit():
    rnd = random.Random(48811)
    P = People(rnd)
    sets = [set_two_step(P), set_both_sides(P), set_decimals(P), set_ineq(rnd, P), set_words(P)]
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
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-8", "slug": "equations-and-inequalities", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Equations and Inequalities: Integers, Variables on Both Sides, Decimals and Graphs",
        "seo_title": "Grade 8 Equations and Inequalities Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equations and Inequalities",
        "domain": "Algebra",
        "standard_code": "Grade 8: C2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve equations that involve multiple terms, integers, and decimal numbers in various contexts, and verify solutions",
        "meta_desc": "Free Grade 8 math worksheets on equations and inequalities for the Ontario curriculum: two-step equations with integers, variables on both sides (3x + 4 = x + 10), equations with decimals, and inequalities graphed on a number line. 100 questions with an answer key.",
        "key_big": "Get the variable on one side and the numbers on the other, then divide: 3x + 4 = x + 10 gives 2x = 6, so x = 3.",
        "key_sub": "Check by substituting: 3 × 3 + 4 = 13 and 3 + 10 = 13. Inequalities use the same steps; a negative answer does not reverse the sign, only multiplying or dividing by a negative number does.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    rx = re.compile(r"<svg (?=[^>]*aria-label='number line)")
    for s_ in u["sets"]:
        for it_ in s_["items"]:
            it_["q"] = rx.sub("<svg data-pf='lg' ", it_["q"])
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
