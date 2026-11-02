# -*- coding: utf-8 -*-
"""
British Columbia Grade 8 Math: Two-Step Equations
(BC Mathematics Curriculum, Grade 8 — Patterning: two-step equations with integer coefficients, constants,
and solutions)
  python3 tools/gen_cabc_math_g8_equations.py
Undoing in reverse order (number machines and pan balances), two-step equations with positive numbers,
with negative constants and negative solutions (3x + 8 = −7), with negative coefficients (−3x + 4 = 19,
8 − 3x = 29, −x/3 + 4 = 9), checking a solution by substitution and finding the step with the mistake,
and word problems in BC contexts (temperatures in Prince George and Whistler, a diver near Nanaimo,
a bike rental near Stanley Park, the Terry Fox Run, a kayak tour in Victoria).
Wrong choices come from real mistakes: undoing the operations in the wrong order (dividing before
subtracting), using the same operation instead of the inverse, sign errors (−9 − 12 = 3, dividing by 3
instead of −3), forgetting the second step, and mixing up the coefficient and the constant.
Every answer is solved and checked in code with fractions.Fraction. HTML attributes use single quotes.
Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia", "Ji-woo"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤", "=": "="}
OPP = {">": "<", "<": ">", ">=": "<=", "<=": ">=", "=": "="}


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
    if FRAC[0] and abs(a.numerator) == 1 and a.denominator > 1:
        return (M if a < 0 else "") + frac(V(v), a.denominator)
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
    if is_div(s) and abs(Ao.numerator) == 1 and Ao.denominator > 1:
        k = num(1 / Ao)
        out.append((Bo - Bv, "forgetting to multiply by %s" % k))
        out.append(((Bo - Bv) * Ao, "dividing by %s instead of multiplying" % k))
        if Bv != 0 and A2 == 0:
            out.append((Bo / Ao - Bv, "multiplying by %s before dealing with the %s" % (k, num(Bv))))
    elif abs(Ao) != 1:
        out.append((Bo - Bv, "forgetting to divide by %s" % num(Ao)))
        if Bv != 0 and (A2 == 0 or A1 == 0):
            out.append((Bo / Ao - Bv, "dividing by %s before dealing with the %s" % (num(Ao), num(Bv))))
        if abs((Bo - Bv) * Ao) <= 200:
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


def flow_svg(start, ops, end, undo=False):
    """Number machine: start -> op -> op -> end. With undo, a second row shows the inverse operations,
    worked from right to left."""
    h, aw = 38, 34
    bw = max(50, int(tw(start, 18) + 18), int(tw(end, 18) + 18))
    ow = max(62, max(int(tw(o, 18) + 18) for o in ops))
    xs, x = [], 8
    widths = [bw] + [ow] * len(ops) + [bw]
    for w in widths:
        xs.append(x)
        x += w + aw
    W = x - aw + 8
    s = []

    def row(y, labels, back):
        for i, (bx, w, t) in enumerate(zip(xs, widths, labels)):
            if i == 0:
                fill, col, it = FILL, RED, t.isalpha()
            elif i == len(widths) - 1:
                fill, col, it = FILL, INK, False
            else:
                fill, col, it = "#fff", (RED if back else INK), False
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (bx, y, w, h, 6 if 0 < i < len(widths) - 1 else 2, fill, RED if back else GREEN))
            s.append(text(bx + w / 2, y + 26, t, 18, col=col, italic=it, bold=True))
        for i in range(len(widths) - 1):
            x1, x2 = xs[i] + widths[i] + 4, xs[i + 1] - 4
            ym = y + h / 2
            if back:
                s.append("<path d='M%d %.1f H%d' stroke='%s' stroke-width='2.5'/>" % (x1 + 8, ym, x2, RED))
                s.append("<path d='M%d %.1f l9 -6 v12 Z' fill='%s'/>" % (x1, ym, RED))
            else:
                s.append("<path d='M%d %.1f H%d' stroke='%s' stroke-width='2.5'/>" % (x1, ym, x2 - 8, INK))
                s.append("<path d='M%d %.1f l-9 -6 v12 Z' fill='%s'/>" % (x2, ym, INK))
    row(8, [start] + ops + [end], False)
    H = 8 + h + 8
    if undo:
        inv = {"×": "÷", "÷": "×", "+": M, M: "+"}
        row(8 + h + 18, [start] + [inv[o[0]] + o[1:] for o in ops] + [end], True)
        H += h + 18
    lab = "number machine: %s, %s, gives %s" % (start, ", then ".join(ops), end)
    if undo:
        lab += ", and the inverse operations back"
    return svg_wrap(W, H, "".join(s), lab)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def keep(it, choices, a):
    """fixed choice order (Step 1, Step 2, ...)"""
    assert it["c"][0] == choices[a] and sorted(it["c"]) == sorted(choices)
    it["c"], it["a"], it["keep"] = list(choices), a, True
    return it


X = V("x")


# ============================================================ set 1: positive numbers
def set_positive(P):
    its = []
    # number machine
    s = "4x + 8 = 36"
    x = solve(s)
    e = ("The machine does × 4, then + 8. Undo in reverse order: 36 − 8 = 28, then 28 ÷ 4 = 7. "
         "Check: 7 × 4 + 8 = 36 ✓.")
    its.append(mcq_n(fig(flow_svg("x", ["× 4", "+ 8"], "36")) + "A number %s goes through this machine and comes out as 36. "
                     "What is %s?" % (X, X), x,
                     [(1, "dividing first: 36 ÷ 4 − 8"), (11, "adding 8 instead of subtracting it"),
                      (28, "forgetting to divide by 4")], e, neg=False))
    # pan balances
    for k, b, c in [(3, 6, 21), (4, 8, 24)]:
        s = "%dx + %d = %d" % (k, b, c)
        x = solve(s)
        svg = scale_svg(["x"] * k + [str(b)], [str(c)], "%d blocks x and %d balance %d" % (k, b, c))
        e = ("The balance shows %s. Take %d off both pans: %d%s = %d. Share %d among the %d blocks: %s = %s. %s."
             % (R(s), b, k, X, c - b, c - b, k, X, num(x), check_text(s, x)))
        its.append(mcq_n(fig(svg) + "The pan balance is level. Each block has the same mass, %s. What is %s?" % (X, X),
                         x, eq_wrongs(s), e, neg=False))
    its.append(mcq("What is the best first step to solve %s?" % R("5x + 7 = 42"),
                   "Subtract 7 from both sides",
                   ["Divide both sides by 5", "Add 7 to both sides", "Subtract 5 from both sides"],
                   "5%s + 7 means “multiply by 5, then add 7.” Undo the last step first: subtract 7 from both sides, "
                   "so 5%s = 35. Then divide by 5: %s = 7. Dividing first leaves the 7 undivided." % (X, X, X)))
    its.append(mcq("Which steps solve %s, in the right order?" % R("x/3 + 4 = 10"),
                   "Subtract 4, then multiply by 3",
                   ["Multiply by 3, then subtract 4", "Subtract 4, then divide by 3", "Add 4, then multiply by 3"],
                   "%s means “divide by 3, then add 4.” Undo + 4 first by subtracting 4: %s = 6. "
                   "Then undo ÷ 3 by multiplying by 3: %s = 18. Check: 18 ÷ 3 + 4 = 10 ✓."
                   % (R("x/3 + 4"), R("x/3"), X)))
    for s in ["2x + 5 = 17", "4x + 7 = 35", "5x - 3 = 22", "6x - 8 = 40", "x/2 + 6 = 13", "x/5 - 2 = 4",
              "7x + 9 = 65", "9 + 2x = 31", "8x - 12 = 60", "40 = 3x + 7", "x/4 + 9 = 15", "11x - 6 = 49",
              "12 + 5x = 72", "x/6 - 3 = 5", "3x - 14 = 31"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Two-step equations with positive numbers", "items": its}


# ============================================================ set 2: negative constants
def set_neg_const(P):
    its = []
    its.append(mcq("What is the best first step to solve %s?" % R("4x + 9 = -15"),
                   "Subtract 9 from both sides",
                   ["Add 9 to both sides", "Divide both sides by 4", "Subtract 4 from both sides"],
                   "Undo + 9 first: subtract 9 from both sides. %s15 − 9 = %s24, so 4%s = %s24. Then divide by 4: %s = %s6. "
                   "Check: 4 × (%s6) + 9 = %s24 + 9 = %s15 ✓." % (M, M, X, M, X, M, M, M, M)))
    its.append(mcq("You subtract 6 from both sides of %s. Which equation do you get?" % R("2x + 6 = -10"),
                   R("2x = -16"), [R("2x = -4"), R("2x = 4"), R("2x = 16")],
                   "%s10 − 6 = %s16: start at %s10 and move 6 more to the left on a number line. So 2%s = %s16 and %s = %s8. "
                   "%s4 comes from a sign error (%s10 + 6)." % (M, M, M, X, M, X, M, M, M)))
    s = "2x + 9 = -5"
    x = solve(s)
    its.append(mcq_n(fig(flow_svg("x", ["× 2", "+ 9"], M + "5")) + "A number %s goes through this machine and comes out as %s5. "
                     "What is %s?" % (X, M, X), x, eq_wrongs(s),
                     "Undo in reverse order: %s5 − 9 = %s14, then %s14 ÷ 2 = %s7. Check: %s7 × 2 + 9 = %s14 + 9 = %s5 ✓."
                     % ((M,) * 7)))
    for s in ["3x + 8 = -7", "2x + 11 = 3", "5x + 12 = -8", "4x - 7 = -31", "2x - 9 = -1", "6x + 20 = -10",
              "3x - 4 = -25", "x/3 + 5 = 2", "x/2 - 4 = -9", "7x + 15 = -20", "-13 = 2x + 7", "8x - 6 = -54",
              "x/4 + 7 = -1", "5x - 18 = -3", "9x + 30 = -15", "-26 = 3x - 5", "x/5 - 6 = -10"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Negative constants and negative solutions", "items": its}


# ============================================================ set 3: negative coefficients
def set_neg_coef(P):
    its = []
    its.append(mcq("You subtract 4 from both sides of %s and get %s. What is the next step?" % (R("-3x + 4 = 19"), R("-3x = 15")),
                   "Divide both sides by %s3" % M,
                   ["Divide both sides by 3", "Add 3 to both sides", "Multiply both sides by %s3" % M],
                   "%s means %s3 × %s. Undo × (%s3) by dividing both sides by %s3: %s = 15 ÷ (%s3) = %s5. "
                   "Dividing by 3 gives 5, the wrong sign. Check: %s3 × (%s5) + 4 = 15 + 4 = 19 ✓."
                   % (R("-3x"), M, X, M, M, X, M, M, M, M)))
    its.append(mcq("Which equation is the same as %s?" % R("8 - 3x = 29"),
                   R("-3x + 8 = 29"), [R("3x - 8 = 29"), R("3x + 8 = 29"), R("-3x - 8 = 29")],
                   "The minus sign in front of 3%s belongs to 3%s, so the term is %s3%s. Changing the order of the terms gives "
                   "%s. Then %s3%s = 21 and %s = %s7. Check: 8 − 3 × (%s7) = 8 + 21 = 29 ✓."
                   % (X, X, M, X, R("-3x + 8 = 29"), M, X, X, M, M)))
    for s in ["-3x + 4 = 19", "-2x + 7 = 15", "-5x + 3 = -22", "-4x - 6 = 18", "-x + 6 = 11", "8 - 3x = 29",
              "-6x + 5 = -19", "-7x - 8 = 34", "10 - 2x = -4", "-x - 9 = -2", "-x/3 + 4 = 9", "-9x + 12 = -24",
              "15 - 4x = 39", "-8x - 5 = 51", "-3 = -2x + 9", "-x/2 - 3 = 4", "-12x + 7 = -53", "20 - 6x = -16"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Negative coefficients", "items": its}


# ============================================================ set 4: check solutions, find mistakes
def which_value(s):
    """Which value is a solution? Distractors come from the usual mistakes; each value is tested."""
    x = solve(s)
    a, r, b = split(s)
    cands = []
    for w, why in eq_wrongs(s):
        if w.denominator == 1 and w != x and w != 0 and w not in [c for c, _ in cands]:
            cands.append((w, why))
    cands = cands[:3]
    assert len(cands) == 3, s
    tests = []
    for t in [x] + [c for c, _ in cands]:
        A1, B1 = side(a)
        val = A1 * t + B1
        tests.append("%s gives %s = %s %s" % (num(t), sub_side(a, t), num(val), "✓" if holds(s, t) else "✗"))
        assert holds(s, t) == (t == x)
    e = "Put each value into the left side; only %s gives %s. %s." % (num(x), num(side(b)[1]), "; ".join(tests))
    return mcq_n("Which value of %s is a solution of %s?" % (X, R(s)), x, cands, e)


def check_item(s, t):
    """Is x = t a solution? Choices state a verdict and a calculation; the wrong ones come from sign errors."""
    a, r, b = split(s)
    A1, B1 = side(a)
    c = side(b)[1]
    assert side(b)[0] == 0
    expr = sub_side(a, t)
    right = A1 * t + B1
    wrongs = [(-(A1 * t) + B1, "a sign error when multiplying"), (A1 * t - B1, "a sign error with the constant"),
              (-(A1 * t) - B1, "two sign errors")]

    def say(v):
        return "%s, because %s = %s" % ("Yes" if v == c else "No", expr, num(v))
    vals = [w for w, _ in wrongs if w != right]
    assert len(set(vals)) == 3, (s, t)
    it = mcq("Is %s = %s a solution of %s? Which check is correct?" % (X, num(t), R(s)), say(right),
             [say(v) for v in vals],
             "Put %s in for %s: %s = %s. The right side is %s, so %s, and %s = %s %s a solution. "
             "Watch the signs: a negative times a negative is positive, and a negative times a positive is negative."
             % (num(t), X, expr, num(right), num(c),
                "both sides are equal" if right == c else "the two sides are not equal",
                X, num(t), "is" if right == c else "is <b>not</b>"))
    return it


STEPS4 = ["Step 1", "Step 2", "Both steps", "There is no mistake"]


def mistake_item(P, s, st1, st2, ans, e):
    nm, he, his = P.next()
    q = ("%s solved %s:<br>Step 1: %s<br>Step 2: %s<br>Which step has a mistake?" % (nm, R(s), st1, st2))
    it = mcq(q, STEPS4[ans], [c for c in STEPS4 if c != STEPS4[ans]], e)
    return keep(it, STEPS4, ans)


def which_eq(k, right, wrongs, how):
    assert holds(right, k), right
    for w in wrongs:
        assert not holds(w, k), w
    return mcq("%s = %s is the solution of which equation?" % (X, num(k)), R(right), [R(w) for w in wrongs],
               "Put %s in for %s in each equation. %s. %s" % (num(k), X, check_text(right, F(k)), how))


def set_check(P):
    its = []
    for s, t in [("4x + 5 = -7", -3), ("-3x + 4 = 19", -5), ("2x - 9 = -1", -4), ("-5x - 6 = 14", 4),
                 ("-2x + 7 = -3", 5)]:
        it = check_item(s, F(t))
        its.append(it)
    for s in ["-2x + 9 = 17", "3x + 14 = -4", "-4x - 3 = 25", "5x - 7 = -42", "-6x + 2 = -40", "x/2 + 8 = 3"]:
        its.append(which_value(s))
    # find the mistake
    its.append(mistake_item(P, "3x + 12 = -9", R("3x = 3"), "%s = 1" % X, 0,
                            "In Step 1, %s9 − 12 = %s21, not 3 (a sign error). Then 3%s = %s21, so %s = %s7. "
                            "Check: 3 × (%s7) + 12 = %s21 + 12 = %s9 ✓." % (M, M, X, M, X, M, M, M, M)))
    its.append(mistake_item(P, "-4x + 6 = 26", R("-4x = 20"), "%s = 5" % X, 1,
                            "Step 1 is right: subtract 6 from both sides. In Step 2, divide by %s4, not 4: "
                            "20 ÷ (%s4) = %s5. Check: %s4 × (%s5) + 6 = 20 + 6 = 26 ✓." % (M, M, M, M, M)))
    its.append(mistake_item(P, "x/2 + 5 = -3", "%s = %s8" % (R("x/2"), M), "%s = %s4" % (X, M), 1,
                            "Step 1 is right: %s3 − 5 = %s8. In Step 2, undo ÷ 2 by <b>multiplying</b> by 2: "
                            "%s = %s16. Check: %s16 ÷ 2 + 5 = %s8 + 5 = %s3 ✓." % (M, M, X, M, M, M, M)))
    its.append(mistake_item(P, "-5x - 4 = 21", R("-5x = 25"), "%s = %s5" % (X, M), 3,
                            "Step 1: add 4 to both sides, 21 + 4 = 25. Step 2: 25 ÷ (%s5) = %s5. Both steps are right. "
                            "Check: %s5 × (%s5) − 4 = 25 − 4 = 21 ✓." % (M, M, M, M)))
    its.append(mistake_item(P, "2x - 6 = 10", "%s − 6 = 5" % X, "%s = 11" % X, 0,
                            "Step 1 divides first, but it divides only 2%s and 10, not the 6: the steps are in the wrong order. "
                            "Add 6 first: 2%s = 16, then divide by 2: %s = 8. Check: 2 × 8 − 6 = 10 ✓." % (X, X, X)))
    its.append(mistake_item(P, "6 - 2x = 14", R("-2x = 20"), "%s = 10" % X, 2,
                            "Step 1: subtract 6, so %s2%s = 14 − 6 = 8, not 20. Step 2: dividing by %s2 must give a negative "
                            "answer, but 10 is positive. Both steps are wrong. The answer is 8 ÷ (%s2) = %s4. "
                            "Check: 6 − 2 × (%s4) = 6 + 8 = 14 ✓." % (M, X, M, M, M, M)))
    assert solve("3x + 12 = -9") == -7 and solve("-4x + 6 = 26") == -5 and solve("x/2 + 5 = -3") == -16
    assert solve("-5x - 4 = 21") == -5 and solve("2x - 6 = 10") == 8 and solve("6 - 2x = 14") == -4
    its.append(which_eq(-4, "-3x + 5 = 17", ["3x + 5 = 17", "-3x - 5 = 17", "-3x + 5 = -7"],
                        "In the other equations, %s3 × (%s4) = 12 is taken as %s12, or the constant has the wrong sign."
                        % (M, M, M)))
    its.append(which_eq(6, "-2x + 20 = 8", ["2x + 20 = 8", "-2x - 20 = 8", "-2x + 20 = 32"],
                        "%s2 × 6 = %s12, and %s12 + 20 = 8." % (M, M, M)))
    its.append(which_eq(-5, "4x - 3 = -23", ["4x + 3 = -23", "4x - 3 = 23", "-4x - 3 = -23"],
                        "4 × (%s5) = %s20, and %s20 − 3 = %s23." % (M, M, M, M)))
    assert len(its) == 20, len(its)
    return {"title": "Check solutions and find mistakes", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    U = lambda a, b: (a, b)

    def word(q, s, extra, intro, after="", unit=None, neg=False):
        e, x, _ = steps(s)
        cands = [c for c in eq_wrongs(s) if not (c[1] or "").startswith("multiplying by")]
        return mcq_n(q, x, list(extra) + cands, "%s: %s. %s%s" % (intro, R(s), e, after), unit=unit, neg=neg)

    its.append(word("At 6:00 a.m. in Prince George, the temperature is %s14 °C. It rises 3 °C each hour. "
                    "After how many hours is it 1 °C?" % M, "-14 + 3h = 1",
                    [(15, "forgetting to divide by 3")], "Let %s be the number of hours" % V("h"),
                    " It is 1 °C at 11:00 a.m.", U("hour", "hours")))
    its.append(word("At 4:00 p.m. in Whistler, the temperature is 3 °C. It falls 2 °C each hour. "
                    "After how many hours is it %s9 °C?" % M, "3 - 2h = -9",
                    [(3, "using %s9 + 3 = %s6 instead of %s9 − 3 = %s12" % (M, M, M, M)), (12, "forgetting to divide by 2")],
                    "Let %s be the number of hours" % V("h"), " It is %s9 °C at 10:00 p.m." % M, U("hour", "hours")))
    its.append(word("A diver near Nanaimo is at %s30 m (30 m below the surface). She rises 4 m each minute. "
                    "After how many minutes is she at %s6 m?" % (M, M), "-30 + 4t = -6",
                    [(24, "forgetting to divide by 4"), (9, "ignoring the minus sign in %s6 (6 + 30 = 36, and 36 ÷ 4 = 9)" % M)],
                    "Let %s be the number of minutes" % V("t"), "", U("minute", "minutes")))
    its.append(word("An underwater camera starts at %s12 m and goes down 5 m each minute. "
                    "After how many minutes is it at %s57 m?" % (M, M), "-12 - 5t = -57",
                    [(45, "forgetting to divide by %s5" % M), (F(69, 5), None)],
                    "Let %s be the number of minutes. Going down 5 m a minute is %s5%s" % (V("t"), M, V("t")), "",
                    U("minute", "minutes")))
    its.append(word("A bike rental near Stanley Park costs $8 plus $6 for each hour. Liam pays $38. For how many hours did he rent the bike?",
                    "6h + 8 = 38", [(4, "mixing up the fee and the hourly rate (8%s + 6 = 38)" % V("h")),
                                    (30, "forgetting to divide by 6")],
                    "Let %s be the number of hours" % V("h"), "", U("hour", "hours")))
    n, he, his = P.next()
    its.append(word("%s has $45 on a school cafeteria card. Each lunch costs $6. After how many lunches will %s have $9 left?"
                    % (n, he), "45 - 6l = 9", [(36, "forgetting to divide by 6"), (9, "adding 9 instead of subtracting it (54 ÷ 6)")],
                    "Let %s be the number of lunches. Each lunch takes away $6, so" % V("l"), "", U("lunch", "lunches")))
    its.append(word("Three times a number, plus 6, is %s9. What is the number?" % M, "3n + 6 = -9",
                    [],
                    "Let %s be the number" % V("n"), "", None, neg=True))
    its.append(word("Multiply a number by %s2, then add 9. The result is 21. What is the number?" % M, "-2n + 9 = 21",
                    [], "Let %s be the number" % V("n"), "", None, neg=True))
    n, he, his = P.next()
    its.append(word("%s’s bank balance is %s$15 because %s owes a service fee. %s deposits $12 each week. "
                    "After how many weeks is the balance $45?" % (n, M, he, cap(he)), "-15 + 12w = 45",
                    [(60, "forgetting to divide by 12"), (F(30, 12), None)],
                    "Let %s be the number of weeks" % V("w"), "", U("week", "weeks")))
    its.append(word("For the Terry Fox Run, a Grade 8 class has raised $85. Each runner will raise $15 more. "
                    "How many runners are needed to reach $400?", "85 + 15r = 400",
                    [(315, "forgetting to divide by 15")], "Let %s be the number of runners" % V("r"),
                    "", U("runner", "runners")))
    its.append(word("A ski shop in Whistler rents skis for a $35 fee plus $28 a day. Kai pays $175. "
                    "For how many days did he rent the skis?", "35 + 28d = 175",
                    [(140, "forgetting to divide by 28")], "Let %s be the number of days" % V("d"), "", U("day", "days")))
    its.append(word("A kayak tour in Victoria costs a $25 booking fee plus $65 for each person. A family pays $350. "
                    "How many people went on the tour?", "25 + 65p = 350",
                    [(325, "forgetting to divide by 65")],
                    "Let %s be the number of people" % V("p"), "", U("person", "people")))
    its.append(word("A field trip to Science World costs $180 for the bus plus $12 for each student. The total is $552. "
                    "How many students went?", "180 + 12s = 552",
                    [(372, "forgetting to divide by 12"), (61, "adding 180 instead of subtracting it (732 ÷ 12)")],
                    "Let %s be the number of students" % V("s"), "", U("student", "students")))
    n, he, his = P.next()
    its.append(mcq("%s has $60 and spends $7 each week on snacks. Which equation finds the number of weeks %s until %s has $11 left?"
                   % (n, V("w"), he),
                   R("60 - 7w = 11"), [R("7w - 60 = 11"), R("60 + 7w = 11"), R("7 - 60w = 11")],
                   "Start with 60 and take away 7 for each week: 60 − 7%s. Set it equal to 11. Solve: %s7%s = %s49, so %s = 7 weeks. "
                   "Check: 60 − 7 × 7 = 11 ✓." % (V("w"), M, V("w"), M, V("w"))))
    assert solve("60 - 7w = 11") == 7
    its.append(mcq("On a winter morning in Kamloops, it is %s8 °C. The temperature rises 2 °C each hour until it is 6 °C. "
                   "Which equation finds the number of hours %s?" % (M, V("h")),
                   R("-8 + 2h = 6"), [R("8 + 2h = 6"), R("-8h + 2 = 6"), R("-8 - 2h = 6")],
                   "Start at %s8 and add 2 for each hour: %s8 + 2%s = 6. Add 8: 2%s = 14, so %s = 7 hours. "
                   "%s8 − 2%s would mean the temperature falls." % (M, M, V("h"), V("h"), V("h"), M, V("h"))))
    assert solve("-8 + 2h = 6") == 7
    its.append(word("After a dry summer, the water level of a lake in the Okanagan is %s4 cm (4 cm below normal). "
                    "It drops 3 cm each week. After how many weeks is it %s25 cm?" % (M, M), "-4 - 3w = -25",
                    [(21, "forgetting to divide by %s3" % M)], "Let %s be the number of weeks" % V("w"), "",
                    U("week", "weeks")))
    n, he, his = P.next()
    its.append(word("%s buys a phone for $120 down plus $35 a month. So far %s has paid $435. For how many months has %s paid?"
                    % (n, he, he), "120 + 35m = 435", [(315, "forgetting to divide by 35"), (F(555, 35), None)],
                    "Let %s be the number of months" % V("m"), "", U("month", "months")))
    its.append(word("A western red cedar seedling is 30 cm tall. It grows 45 cm each year. After how many years is it 300 cm tall?",
                    "30 + 45y = 300", [(270, "forgetting to divide by 45")], "Let %s be the number of years" % V("y"), "",
                    U("year", "years")))
    its.append(word("An isosceles triangle has two equal sides and a base of 14 cm. Its perimeter is 50 cm. How long is each equal side?",
                    "2s + 14 = 50", [(36, "forgetting to divide by 2"), (F(64, 2), "adding 14 instead of subtracting it")],
                    "Let %s be the length of an equal side" % V("s"), "", U("cm", "cm")))
    n, he, his = P.next()
    its.append(word("On a class quiz game, each correct answer is worth 5 points. %s’s team loses 10 points for a late answer. "
                    "The team’s score is 35. How many correct answers did the team give?" % n, "5c - 10 = 35",
                    [(5, "subtracting 10 instead of adding it"), (45, "forgetting to divide by 5")],
                    "Let %s be the number of correct answers" % V("c"), "", U("answer", "answers")))
    assert len(its) == 20, len(its)
    return {"title": "Two-step equation word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    return (
        "<h2>Undo the steps in reverse order</h2>"
        "<p>A <b>two-step equation</b> does two things to the unknown. In " + R("-3x + 4 = 19") + ", you multiply "
        + X + " by −3, then add 4. To find " + X + ", undo the last step first, then the first step. "
        "Whatever you do to one side, do to the other side too.</p>"
        "<figure class='sn-fig'>" + flow_svg("x", ["× (−3)", "+ 4"], "19", undo=True) +
        "<figcaption>Top: build −3" + X + " + 4. Bottom: work back from 19. 19 − 4 = 15, then 15 ÷ (−3) = −5.</figcaption></figure>" +
        ex("Example 1", "Solve " + R("3x + 8 = -7") + ".",
           "Subtract 8 from both sides: 3" + X + " = −15. Divide both sides by 3: " + X + " = −5. "
           "Check: 3 × (−5) + 8 = −15 + 8 = −7 ✓.", X + " = −5") +
        ex("Example 2", "Solve " + R("-3x + 4 = 19") + ".",
           "Subtract 4 from both sides: −3" + X + " = 15. Divide both sides by −3: " + X + " = 15 ÷ (−3) = −5. "
           "Check: −3 × (−5) + 4 = 15 + 4 = 19 ✓.", X + " = −5") +
        ex("Example 3", "Solve " + R("x/4 - 2 = -5") + ".",
           "Add 2 to both sides: " + R("x/4") + " = −3. Multiply both sides by 4: " + X + " = −12. "
           "Check: −12 ÷ 4 − 2 = −3 − 2 = −5 ✓.", X + " = −12") +
        "<h2>Check your solution</h2>"
        "<p>Put your answer back into the <b>original</b> equation. If both sides are equal, it is correct. "
        "Use brackets around negative numbers: −3 × (−5), not −3 × −5.</p>"
        "<figure class='sn-fig'>" + scale_svg(["x", "x", "5"], ["13"], "2 blocks x and 5 balance 13") +
        "<figcaption>2" + X + " + 5 = 13. Take 5 off both pans: 2" + X + " = 8, so " + X + " = 4. "
        "Check: 2 × 4 + 5 = 13 ✓.</figcaption></figure>" +
        table(["Equation", "Step 1", "Step 2", "Check"], [
            [R("2x + 9 = -5"), "− 9: 2" + X + " = −14", "÷ 2: " + X + " = −7", "2 × (−7) + 9 = −5 ✓"],
            [R("8 - 3x = 29"), "− 8: −3" + X + " = 21", "÷ (−3): " + X + " = −7", "8 − 3 × (−7) = 29 ✓"],
            [R("-x + 6 = 11"), "− 6: −" + X + " = 5", "÷ (−1): " + X + " = −5", "−(−5) + 6 = 11 ✓"],
        ]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [R("3x + 12 = -9") + ": divide by 3 first", "Undo + 12 first: 3" + X + " = −21, then " + X + " = −7"],
            [R("5x - 8 = -23") + ": subtract 8", "Use the inverse: add 8, so 5" + X + " = −15"],
            ["−9 − 12 = 3", "−9 − 12 = −21 (move left on a number line)"],
            [R("-3x = 15") + ", so " + X + " = 5", "Divide by −3, not 3: " + X + " = −5"],
            [R("8 - 3x") + " read as 3" + X + " − 8", "The − belongs to 3" + X + ": −3" + X + " + 8"],
            ["Stopping at −3" + X + " = 15", "Do the second step: divide by −3"],
        ])
    )


FAQ = [
    {"q": "How do you solve two-step equations with negative numbers in Grade 8?",
     "a": "Undo the operations in reverse order and watch the signs. For 3x + 8 = −7, subtract 8 from both sides (3x = −15), then divide by 3 (x = −5). Check: 3 × (−5) + 8 = −7."},
    {"q": "Are two-step equations in the BC Grade 8 math curriculum?",
     "a": "Yes. The BC Grade 8 Patterning standard covers two-step equations with integer coefficients, constants and solutions, such as −3x + 4 = 19 and x/4 − 2 = −5."},
    {"q": "How do you solve an equation like −3x + 4 = 19?",
     "a": "Subtract 4 from both sides to get −3x = 15. Then divide both sides by −3, not 3, so x = −5. Check: −3 × (−5) + 4 = 15 + 4 = 19."},
    {"q": "How do you check the solution of a two-step equation?",
     "a": "Put the answer back into the original equation and work out each side. If both sides are equal, the answer is correct; use brackets around negative numbers, as in 4 × (−3) + 5 = −7."},
]


def gen_unit():
    rnd = random.Random(58807)
    P = People(rnd)
    sets = [set_positive(P), set_neg_const(P), set_neg_coef(P), set_check(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "two-step-equations", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Two-Step Equations with Integers",
        "seo_title": "Grade 8 Two-Step Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Two-Step Equations",
        "domain": "Patterning",
        "standard_code": "Grade 8: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Two-step equations with integer coefficients, constants, and solutions",
        "meta_desc": "Free Grade 8 math worksheets on two-step equations for the BC curriculum: equations with negative constants (3x + 8 = −7) and negative coefficients (−3x + 4 = 19), checking solutions, finding mistakes, and word problems. 100 questions with an answer key.",
        "key_big": "Undo the steps in reverse order: undo the + or − first, then the × or ÷. Watch every sign.",
        "key_sub": "−3x + 4 = 19: subtract 4 (−3x = 15), then divide by −3 (x = −5). Check: −3 × (−5) + 4 = 19.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "pan balance|number machine")
    os.makedirs(OUT, exist_ok=True)
    path_ = os.path.join(OUT, u["slug"] + ".json")
    with open(path_, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path_)
