# -*- coding: utf-8 -*-
"""
CA Grade 7 Math: Equations and Inequalities (Ontario Mathematics Curriculum 2020, Grade 7: Algebra, C2.3 and C2.4)
  python3 tools/gen_caon_math_g7_equations.py
Two-step equations (4x + 9 = 41, x/3 + 7 = 12), equations with several terms where like terms are
collected first (3x + 2x = 35, 9 + 2n + 5 + 3n = 64), equations with decimal numbers (0.5x + 3 = 7),
inequalities with several terms solved, verified and graphed on a number line, and word problems in
Ontario contexts (phone plans, memberships, a school trip, a taxi in Ottawa, a canoe trip in Algonquin Park).
Wrong choices come from real mistakes: undoing the operations in the wrong order (dividing first), using the
same operation instead of the inverse, forgetting the second step, multiplying instead of dividing,
multiplying the coefficients (2x + 3x = 6x), forgetting that x means 1x, a misplaced decimal point,
an open circle for ≤ / ≥ (or a closed one for < / >), the arrow the wrong way, and rounding down
when a word problem needs the next whole number.
Every answer is solved and checked in code with fractions.Fraction. HTML attributes use single quotes.
Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GREY = "#e4e4e4"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
M = "−"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

SYM = {">": "&gt;", "<": "&lt;", ">=": "≥", "<=": "≤"}
OPP = {">": "<", "<": ">", ">=": "<=", "<=": ">="}          # arrow the other way
SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}          # open <-> closed circle
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


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "$" + num(v)
    assert (v * 100).denominator == 1, v
    return "$%d.%02d" % (int(v), int((v - int(v)) * 100))


def nice(v, whole_only):
    v = F(v)
    if v <= 0:
        return False
    if whole_only:
        return v.denominator == 1
    return (v * 100).denominator == 1


# ------------------------------------------------------------ equations in a mini syntax
# "0.5x + 3 = 7", "x/4 + 1.5 = 3.25", "9 + 2n + 5 + 3n = 64", "2x + 5 < 17". Tokens are separated by spaces.
TERM = re.compile(r"^(\d*\.?\d*)([a-z])$")
DIVT = re.compile(r"^([a-z])/(\d+)$")
NUMT = re.compile(r"^\d+(\.\d+)?$")
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


def side(t):
    """-> (coefficient of the letter, constant)"""
    A, B, sign = F(0), F(0), 1
    for tok in t.split(" "):
        if tok in ("+", "-"):
            sign = 1 if tok == "+" else -1
            continue
        m, d = TERM.match(tok), DIVT.match(tok)
        if m:
            A += sign * (F(m.group(1)) if m.group(1) else 1)
        elif d:
            A += sign * F(1, int(d.group(2)))
        elif NUMT.match(tok):
            B += sign * F(tok)
        else:
            raise ValueError(tok)
    return A, B


def solve(s):
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    assert A1 != A2, s
    return (B2 - B1) / (A1 - A2), r


def holds(s, x):
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    l, rr = A1 * x + B1, A2 * x + B2
    return {"=": l == rr, "<": l < rr, ">": l > rr, "<=": l <= rr, ">=": l >= rr}[r]


def var_of(s):
    return re.search(r"[a-z]", s).group(0)


def R(s):
    """render the mini syntax as HTML"""
    out = []
    for tok in s.split(" "):
        m, d = TERM.match(tok), DIVT.match(tok)
        if d:
            out.append(frac(V(d.group(1)), d.group(2)))
        elif m:
            out.append(m.group(1) + V(m.group(2)))
        elif tok in SYM:
            out.append(SYM[tok])
        else:
            out.append({"-": M}.get(tok, tok))
    return " ".join(out)


def T(a, v):
    """A·v as HTML: 'x', '5x', '0.5x'"""
    return V(v) if a == 1 else num(a) + V(v)


def lin(A, B, v):
    """A·v + B as HTML"""
    if B == 0:
        return T(A, v)
    return "%s %s %s" % (T(A, v), "+" if B > 0 else M, num(abs(B)))


def lin_s(A, B, v):
    """A·v + B in the mini syntax"""
    a = v if A == 1 else num(A) + v
    if B == 0:
        return a
    return "%s %s %s" % (a, "+" if B > 0 else "-", num(abs(B)))


def is_div(s):
    return bool(re.search(r"[a-z]/\d", s))


# ------------------------------------------------------------ explanations and mistakes
def undo_text(B):
    return ("Subtract %s from both sides" % num(B)) if B > 0 else ("Add %s to both sides" % num(-B))


def check_text(s, x):
    """'4 × 8 + 9 = 41' for the left side of s (letters replaced by x)."""
    a, r, b = split(s)
    parts = []
    for tok in a.split(" "):
        m, d = TERM.match(tok), DIVT.match(tok)
        if m:
            parts.append(("%s × %s" % (m.group(1), num(x))) if m.group(1) else num(x))
        elif d:
            parts.append("%s ÷ %s" % (num(x), d.group(2)))
        else:
            parts.append({"-": M}.get(tok, tok))
    A, B = side(a)
    return "%s = %s" % (" ".join(parts), num(A * x + B))


def steps(s, x=None):
    """Explanation for a linear equation whose letter terms are all on the left and constant on the right."""
    v = var_of(s)
    a, r, b = split(s)
    A, B = side(a)
    A2, C = side(b)
    if A == 0:      # "47 = 6x + 11": swap
        return steps("%s = %s" % (b, a), x)
    assert A2 == 0
    x = solve(s)[0]
    out = []
    terms = len([t for t in a.split(" ") if TERM.match(t) or DIVT.match(t)])
    consts = len([t for t in a.split(" ") if NUMT.match(t)])
    if terms > 1 or consts > 1:
        out.append("Collect like terms: %s becomes %s, so %s = %s." % (R(a), lin(A, B, v), lin(A, B, v), num(C)))
    mid = C - B
    if B != 0:
        out.append("%s: %s = %s." % (undo_text(B), T(A, v) if not (is_div(s) and terms == 1) else frac(V(v), A.denominator), num(mid)))
    if A != 1:
        if is_div(s) and terms == 1:
            out.append("Multiply both sides by %d: %s = %s × %d = <b>%s</b>." % (A.denominator, V(v), num(mid), A.denominator, num(x)))
        else:
            out.append("Divide both sides by %s: %s = %s ÷ %s = <b>%s</b>." % (num(A), V(v), num(mid), num(A), num(x)))
    else:
        out[-1] = out[-1][:-1].replace("%s = %s" % (V(v), num(mid)), "%s = <b>%s</b>" % (V(v), num(mid))) + "."
    out.append("Check: %s." % check_text(s if A2 == 0 else s, x))
    return " ".join(out)


def two_step_wrongs(A, B, C, d=None):
    """Mistakes for A·x + B = C (or x/d + B = C), most common first. -> [(value, why)]"""
    mid = C - B
    inv = C + B
    nb = num(abs(B))
    if d:
        if B > 0:
            return [(C * d - B, "multiplying by %d before subtracting %s" % (d, nb)),
                    (F(mid, d), "dividing by %d instead of multiplying" % d),
                    (inv * d, "adding %s instead of subtracting it" % nb), (mid, "forgetting to multiply by %d" % d)]
        return [(C * d - B, "multiplying by %d before adding %s" % (d, nb)),
                (F(mid, d), "dividing by %d instead of multiplying" % d),
                (inv * d, "subtracting %s instead of adding it" % nb), (mid, "forgetting to multiply by %d" % d)]
    na = num(A)
    if B > 0:
        return [(C / A - B, "dividing by %s before subtracting %s" % (na, nb)),
                (inv / A, "adding %s instead of subtracting it" % nb),
                (mid, "forgetting to divide by %s" % na), (mid * A, "multiplying by %s instead of dividing" % na)]
    if B < 0:
        return [(C / A - B, "dividing by %s before adding %s" % (na, nb)),
                (inv / A, "subtracting %s instead of adding it" % nb),
                (mid, "forgetting to divide by %s" % na), (mid * A, "multiplying by %s instead of dividing" % na)]
    return [(mid * A, "multiplying by %s instead of dividing" % na)]


def auto_wrongs(s):
    v = var_of(s)
    a, r, b = split(s)
    A, B = side(a)
    A2, C = side(b)
    if A == 0:
        A, B, C = A2, C, B
    d = A.denominator if (is_div(s) and A.numerator == 1) else None
    return two_step_wrongs(A, B, C, d)


def near(x, k=1):
    return [x + k, x - k, x + 2 * k, x - 2 * k]


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


def mcq_n(q, x, cands, e, unit=None, whole_only=True, notes=True, limit=None):
    """cands: (value, why) pairs or plain values. Only nice, positive, new values are used; the reasons
    for the wrong answers used are added to the explanation."""
    x = F(x)
    used, add = {x}, []
    for c in cands:
        val, why = c if isinstance(c, tuple) else (c, None)
        val = F(val)
        if not nice(val, whole_only) or val in used or (limit and val > limit):
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


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
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


def bal(k, b, c, v="x"):
    return scale_svg([v] * k + [str(b)], [str(c)], "%d blocks %s and %d balance %d" % (k, v, b, c))


def flow_svg(start, ops, end, undo=False):
    """Number machine: start -> op -> op -> end. With undo, a second row shows the inverse operations
    from right to left."""
    bw, ow, aw, h = 50, 62, 34, 38
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


GAP, PAD, FS = 30, 30, 15


def nline(lo, rel, k, v="x"):
    """Number line from lo to lo + 10. Circle at k: open for > <, closed for >= <=.
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
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(text(x, Y + 26, str(q), FS))
    xc = X(k)
    end = Rr - 1 if RIGHT[rel] else L + 1
    tip = 12 if RIGHT[rel] else -12
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='5'/>" % (xc, Y, end - tip, Y, GREEN))
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (end, Y, end - tip, Y - 8, end - tip, Y + 8, GREEN))
    s.append("<circle cx='%d' cy='%d' r='7' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (xc, Y, GREEN if CLOSED[rel] else "#ffffff", GREEN))
    return svg_wrap(W, H, "".join(s), "number line graph of %s %s %d" % (v, WORDS[rel], k))


def window(rnd, k):
    return max(0, k - rnd.choice([3, 4, 5, 6, 7]))


def sol(v, rel, k):
    return "%s %s %s" % (V(v), SYM[rel], num(k))


def describe(rel, k):
    return "%s circle at %d, arrow to the %s" % ("Closed" if CLOSED[rel] else "Open", k, "right" if RIGHT[rel] else "left")


def why_graph(rel, k, v="x"):
    circ = ("a closed (filled-in) circle, because %d is a solution" if CLOSED[rel]
            else "an open circle, because %d is not a solution") % k
    side_ = "right, toward greater numbers" if RIGHT[rel] else "left, toward lesser numbers"
    return "%s has %s, and the arrow points %s." % (sol(v, rel, k), circ, side_)


def ineq_parts(s):
    a, r, b = split(s)
    A, B = side(a)
    _, C = side(b)
    k = (C - B) / A
    assert k.denominator == 1 and k > 0, s
    return A, B, C, r, int(k)


def ineq_steps(s):
    v = var_of(s)
    a, r, b = split(s)
    A, B, C, r, k = ineq_parts(s)
    out = []
    terms = len([t for t in a.split(" ") if TERM.match(t)])
    consts = len([t for t in a.split(" ") if NUMT.match(t)])
    if terms > 1 or consts > 1:
        out.append("Collect like terms: %s %s %s." % (lin(A, B, v), SYM[r], num(C)))
    if B != 0:
        out.append("%s: %s %s %s." % (undo_text(B), T(A, v), SYM[r], num(C - B)))
    if A != 1:
        out.append("Divide both sides by %s: <b>%s</b>." % (num(A), sol(v, r, k)))
    return " ".join(out)


# ============================================================ set 1: two-step equations
def set_two_step(P):
    its = []
    # A. pan balances
    for k, b, c in [(3, 5, 26), (4, 7, 39)]:
        s = "%dx + %d = %d" % (k, b, c)
        x = solve(s)[0]
        e = ("The balance shows %s. Take %d off both pans: %s = %d. %d equal blocks make %d, so each block is "
             "%d ÷ %d = <b>%s</b>. Check: %s." % (R(s), b, T(k, "x"), c - b, k, c - b, c - b, k, num(x), check_text(s, x)))
        its.append(mcq_n("The pan balance is level. Each block has the same mass, %s. What is %s?" % (V("x"), V("x"))
                         + fig(bal(k, b, c)), x, auto_wrongs(s) + near(x), e))
    # B. best first step
    its.append(mcq("What is the best first step to solve %s?" % R("3x + 8 = 29"),
                   "Subtract 8 from both sides",
                   ["Divide both sides by 3", "Add 8 to both sides", "Subtract 3 from both sides"],
                   "3%s + 8 means “multiply by 3, then add 8”. Undo the last operation first: <b>subtract 8 from both sides</b> "
                   "to get 3%s = 21, then divide by 3: %s = 7. Dividing 29 by 3 first does not give a whole number."
                   % (V("x"), V("x"), V("x"))))
    assert solve("3x + 8 = 29")[0] == 7
    its.append(mcq("What is the best first step to solve %s?" % R("n/5 - 2 = 4"),
                   "Add 2 to both sides",
                   ["Multiply both sides by 5", "Subtract 2 from both sides", "Divide both sides by 5"],
                   "%s means “divide by 5, then subtract 2”. Undo the − 2 first: <b>add 2 to both sides</b> to get %s = 6, "
                   "then multiply by 5: %s = 30. Subtracting 2 is the same operation, not the inverse."
                   % (R("n/5 - 2"), R("n/5"), V("n"))))
    assert solve("n/5 - 2 = 4")[0] == 30
    # C. reverse order
    its.append(mcq("To build 6%s − 4, start with %s, multiply by 6, then subtract 4. Which order undoes it?" % (V("x"), V("x"))
                   + fig(flow_svg("x", ["× 6", M + " 4"], "?")),
                   "Add 4, then divide by 6",
                   ["Divide by 6, then add 4", "Subtract 4, then multiply by 6", "Add 6, then divide by 4"],
                   "Undo the steps in <b>reverse order</b>, like taking off your boots before your socks. The last step was − 4, "
                   "so add 4 first. Then undo × 6 by dividing by 6. Dividing first would divide only part of the expression."))
    # D. solve, easier to harder
    for s in ["4x + 9 = 41", "6n - 5 = 31", "x/3 + 7 = 12", "7y + 12 = 75", "n/5 - 4 = 3", "9k - 14 = 58",
              "15 + 8m = 95", "47 = 6x + 11", "x/6 + 13 = 21", "12p - 25 = 107", "25t + 40 = 340", "82 = y/4 + 65"]:
        x = solve(s)[0]
        assert x.denominator == 1 and x > 0, s
        e = steps(s)
        a, r, b = split(s)
        if side(a)[0] == 0:
            e = "The = sign can come first: %s means %s. " % (R(s), R("%s = %s" % (b, a))) + e
        elif NUMT.match(a.split(" ")[0]):
            A, B = side(a)
            e = "%s is the same as %s. " % (R(a), lin(A, B, var_of(s))) + e
        its.append(mcq_n("Solve: %s" % R(s), x, auto_wrongs(s) + near(x, 1 if not is_div(s) else 2), e,
                         limit=4 * max(x, side(split(s)[0])[1], side(split(s)[2])[1])))
    # E. dividing-first mistake
    nm, he, his = P.next()
    s = "4x + 12 = 60"
    assert solve(s)[0] == 12
    its.append(mcq_n("%s solves %s. %s divides first: 60 ÷ 4 = 15, then 15 − 12 = 3. What is the correct value of %s?"
                     % (nm, R(s), cap(he), V("x")), 12,
                     [(3, "dividing before subtracting 12"), (18, "adding 12 instead of subtracting it"),
                      (48, "forgetting to divide by 4")],
                     "Check 3: 4 × 3 + 12 = 24, not 60. Dividing first divides the 60 but not the 12. Undo in reverse order: "
                     "subtract 12 first, 4%s = 48. Then divide by 4: %s = <b>12</b>. Check: 4 × 12 + 12 = 60." % (V("x"), V("x"))))
    # F. verify
    s = "5x - 10 = 40"
    assert holds(s, 10)
    its.append(mcq_n("Which value of %s makes %s true?" % (V("x"), R(s)), 10,
                     [(50, "forgetting to divide by 5"), (6, "subtracting 10 instead of adding it"),
                      (18, "dividing by 5 before adding 10")],
                     "Put the value in: 5 × 10 − 10 = 50 − 10 = 40, so <b>10</b> works. Or solve: add 10 to get 5%s = 50, "
                     "then divide by 5." % V("x")))
    s = "3x + 7 = 25"
    assert holds(s, 6)
    its.append(mcq("Which work correctly checks that %s = 6 solves %s?" % (V("x"), R(s)),
                   "3 × 6 + 7 = 18 + 7 = 25", ["36 + 7 = 43", "3 + 6 + 7 = 16", "3 × (6 + 7) = 39"],
                   "3%s means 3 × %s. Multiply first, then add: <b>3 × 6 + 7 = 18 + 7 = 25</b>. The left side equals 25, so "
                   "%s = 6 is correct. 3%s is not the number 36, and the + 7 is not multiplied by 3." % (V("x"), V("x"), V("x"), V("x"))))
    assert len(its) == 20, len(its)
    return {"title": "Two-step equations", "items": its}


# ============================================================ set 2: collect like terms first
def set_terms(P):
    its = []

    def alt(s2):
        return solve(s2)[0]

    def item(s, extra, note=""):
        x = solve(s)[0]
        assert x.denominator == 1 and x > 0, s
        cands = [(alt(t), why) for t, why in extra] + auto_wrongs(collected(s)) + near(x)
        its.append(mcq_n("Solve: %s" % R(s), x, cands, steps(s) + note, limit=2 * side(split(s)[2])[1]))

    # simplify
    its.append(mcq("Simplify: 3%s + 2%s + 7" % (V("x"), V("x")), "5%s + 7" % V("x"),
                   ["12%s" % V("x"), "6%s + 7" % V("x"), "5%s" % V("x")],
                   "3%s and 2%s are like terms: 3 + 2 = 5, so <b>5%s + 7</b>. The 7 has no %s, so it is not added to the %s terms. "
                   "Do not multiply 3 × 2." % ((V("x"),) * 5)))
    its.append(mcq("Simplify: 6%s − 2%s + 9 − 4" % (V("n"), V("n")), "4%s + 5" % V("n"),
                   ["8%s + 5" % V("n"), "4%s + 13" % V("n"), "9%s" % V("n")],
                   "6%s − 2%s = 4%s and 9 − 4 = 5, so <b>4%s + 5</b>. Watch each sign: − 2%s is taken away, and − 4 is taken away."
                   % ((V("n"),) * 5)))
    its.append(mcq("Simplify: %s + 4%s − 3 + 10" % (V("y"), V("y")), "5%s + 7" % V("y"),
                   ["4%s + 7" % V("y"), "5%s + 13" % V("y"), "12%s" % V("y")],
                   "%s means 1%s, so %s + 4%s = 5%s. Then −3 + 10 = 7: <b>5%s + 7</b>." % ((V("y"),) * 6)))
    # ax + bx = c
    item("3x + 2x = 30", [("6x = 30", "multiplying 3 × 2 instead of adding"), ("3x = 30", "leaving out 2x"),
                          ("2x = 30", "leaving out 3x")])
    item("4n + 5n = 180", [("20n = 180", "multiplying 4 × 5 instead of adding"), ("4n = 180", "leaving out 5n"),
                           ("5n = 180", "leaving out 4n")])
    item("x + 5x = 60", [("5x = 60", "forgetting that x means 1x"), ("x + 5 = 60", "treating 5x as the number 5")],
         " Remember that %s means 1%s, so %s + 5%s = 6%s." % ((V("x"),) * 5))
    item("6m - 2m = 48", [("8m = 48", "adding 2m instead of subtracting it"), ("12m = 48", "multiplying 6 × 2"),
                          ("6m = 48", "leaving out 2m")])
    item("15x + 5x = 300", [("75x = 300", "multiplying 15 × 5 instead of adding"), ("15x = 300", "leaving out 5x"),
                            ("5x = 300", "leaving out 15x")])
    # collect, then two steps
    item("2x + 4x + 5 = 47", [("8x + 5 = 47", "multiplying 2 × 4 instead of adding"), ("2x + 5 = 47", "leaving out 4x")])
    item("3n + n - 6 = 30", [("3n - 6 = 30", "forgetting that n means 1n"), ("4n + 6 = 30", "subtracting 6 instead of adding it")],
         " Remember that %s means 1%s, so 3%s + %s = 4%s." % ((V("n"),) * 5))
    item("6y - 2y + 9 = 45", [("8y + 9 = 45", "adding 2y instead of subtracting it"), ("6y + 9 = 45", "leaving out 2y")])
    item("5k + 3 + 2k = 38", [("10k + 3 = 38", "multiplying 5 × 2"), ("5k + 3 = 38", "leaving out 2k")])
    item("8m - 3m - 7 = 33", [("11m - 7 = 33", "adding 3m instead of subtracting it"), ("8m - 7 = 33", "leaving out 3m")])
    # several constants
    item("9 + 2n + 5 + 3n = 64", [("5n + 9 = 64", "leaving out the 5"), ("5n + 5 = 64", "leaving out the 9")])
    item("4x + 12 - 2x - 5 = 25", [("2x + 17 = 25", "adding the 5 instead of subtracting it"),
                                   ("6x + 7 = 25", "adding 2x instead of subtracting it")])
    # three letter terms
    item("x + 2x + 4x = 168", [("6x = 168", "forgetting that x means 1x"), ("8x = 168", "multiplying 2 × 4")])
    item("3w + 2w + 5w - 10 = 90", [("30w - 10 = 90", "multiplying 3 × 2 × 5"), ("5w - 10 = 90", "using only 3w + 2w")])
    # which equation is the same
    s = "5x + 2 + 3x - 7 = 35"
    x = solve(s)[0]
    wr = ["8x + 9 = 35", "15x - 5 = 35", "8x - 5 = 30"]
    assert x == 5 and all(not holds(w, x) for w in wr)
    its.append(mcq("Which equation is the same as %s after you collect like terms?" % R(s), R("8x - 5 = 35"), [R(w) for w in wr],
                   "Letter terms: 5%s + 3%s = 8%s. Numbers: 2 − 7 = −5. So <b>%s</b>, and then %s = 5. "
                   "%s adds the 7 instead of subtracting it, and %s multiplies 5 × 3."
                   % (V("x"), V("x"), V("x"), R("8x - 5 = 35"), V("x"), R("8x + 9 = 35"), R("15x - 5 = 35"))))
    # verify
    s = "3x + 4x - 5 = 44"
    assert holds(s, 7) and not holds(s, 6)
    its.append(mcq("Is %s = 7 a solution of %s? Which check is correct?" % (V("x"), R(s)),
                   "Yes, because 3 × 7 + 4 × 7 − 5 = 21 + 28 − 5 = 44",
                   ["No, because 37 + 47 − 5 = 79", "No, because 12 × 7 − 5 = 79", "No, because 3 + 4 + 7 − 5 = 9"],
                   "Put 7 in for each %s: 3 × 7 + 4 × 7 − 5 = 21 + 28 − 5 = 44. Both sides are 44, so <b>yes</b>. "
                   "Or collect like terms first: 7%s − 5 = 44, and 7 × 7 − 5 = 49 − 5 = 44. 3%s means 3 × %s, not 37, "
                   "and 3%s + 4%s is 7%s, not 12%s." % ((V("x"),) * 8)))
    # mistake
    nm, he, his = P.next()
    s = "4x + 2x + 3 = 51"
    assert solve(s)[0] == 8 and solve("8x + 3 = 51")[0] == 6
    its.append(mcq("%s solves %s and gets %s = 6. What went wrong?" % (nm, R(s), V("x")),
                   "%s multiplied 4 × 2 instead of adding" % cap(he),
                   ["%s should divide 51 by 6 first" % cap(he), "%s should add 3 to both sides" % cap(he), "Nothing, 6 is right"],
                   "%s wrote 8%s + 3 = 51, so 8%s = 48 and %s = 6. But 4%s + 2%s = 6%s, because 4 + 2 = 6. "
                   "Then 6%s + 3 = 51, 6%s = 48 and %s = <b>8</b>. Check: 32 + 16 + 3 = 51." % ((nm,) + (V("x"),) * 9)))
    assert len(its) == 20, len(its)
    return {"title": "Collect like terms first", "items": its}


def collected(s):
    a, r, b = split(s)
    A, B = side(a)
    if A == 0:
        a, b = b, a
        A, B = side(a)
    _, C = side(b)
    assert C > 0
    return "%s = %s" % (lin_s(A, B, var_of(s)), num(C))


# ============================================================ set 3: equations with decimals
def set_decimals(P):
    its = []

    def item(s, extra=(), unit=None):
        x = solve(s)[0]
        assert nice(x, False), s
        cands = [(solve(t)[0], why) for t, why in extra] + auto_wrongs(collected(s) if not is_div(s) else s)[:3]
        cands += [(x * 10, "misplacing the decimal point"), (x / 10, "misplacing the decimal point")] + near(x)
        e = steps(s)
        a, r, b = split(s)
        if side(a)[0] == 0:
            e = "The = sign can come first: %s means %s. " % (R(s), R("%s = %s" % (b, a))) + e
        elif NUMT.match(a.split(" ")[0]):
            A, B = side(a)
            e = "%s is the same as %s. " % (R(a), lin(A, B, var_of(s))) + e
        its.append(mcq_n("Solve: %s" % R(s), x, cands, e, unit, whole_only=False))

    item("0.25x = 6")
    item("0.5x + 3 = 7")
    item("2x + 1.5 = 9.5")
    item("4x - 2.6 = 9.4")
    item("1.5n + 4 = 13")
    item("0.2y - 1 = 3")
    # mistake: dividing by 0.5
    nm, he, his = P.next()
    assert solve("0.5x = 4")[0] == 8
    its.append(mcq("%s solves %s and writes %s = 2. What went wrong?" % (nm, R("0.5x = 4"), V("x")),
                   "%s multiplied by 0.5 instead of dividing" % cap(he),
                   ["%s should subtract 0.5" % cap(he), "%s should divide by 5" % cap(he), "Nothing, 2 is right"],
                   "0.5%s means 0.5 × %s, so divide both sides by 0.5. 4 ÷ 0.5 = 8, because there are 8 halves in 4. "
                   "So %s = <b>8</b>. Check: 0.5 × 8 = 4. Check 2: 0.5 × 2 = 1, not 4." % (V("x"), V("x"), V("x"))))
    item("2.5k - 1.5 = 8.5")
    item("x/4 + 1.5 = 3.25")
    item("x/2 - 0.5 = 4.5")
    item("1.6 + 0.3x = 4.6")
    item("3x + 2.4 = 10.5")
    item("5x + 0.75 = 13.25")
    item("6.5 = 2x - 3.5")
    item("0.75t - 2.5 = 5")
    # like terms with decimals
    item("0.4x + 0.6x = 9", [("0.24x = 9", "multiplying 0.4 × 0.6 instead of adding"), ("0.4x = 9", "leaving out 0.6x")])
    item("1.2m + 0.8m + 3 = 15", [("0.96m + 3 = 15", "multiplying 1.2 × 0.8")])
    item("3.5x + 1.5x - 2 = 18", [("5x + 2 = 18", "adding the 2 instead of subtracting it")])
    # first step and verify
    assert solve("0.3x + 1.2 = 3")[0] == 6
    its.append(mcq("What is the best first step to solve %s?" % R("0.3x + 1.2 = 3"),
                   "Subtract 1.2 from both sides",
                   ["Divide both sides by 0.3", "Add 1.2 to both sides", "Multiply both sides by 0.3"],
                   "Decimals do not change the plan: undo the + 1.2 first. <b>Subtract 1.2 from both sides</b>: 0.3%s = 1.8. "
                   "Then divide by 0.3: %s = 6. Check: 0.3 × 6 + 1.2 = 1.8 + 1.2 = 3." % (V("x"), V("x"))))
    s = "1.5x - 2 = 7"
    assert holds(s, 6)
    its.append(mcq_n("Which value of %s makes %s true?" % (V("x"), R(s)), 6,
                     [(9, "forgetting to divide by 1.5"), (F(10, 3) + 0, None), (60, "misplacing the decimal point"),
                      (F(13, 1), None), (F(27, 2), "multiplying by 1.5 instead of dividing"), (F(7, 1), None)],
                     "Put the value in: 1.5 × 6 − 2 = 9 − 2 = 7, so <b>6</b> works. Or solve: add 2 to get 1.5%s = 9, then "
                     "divide by 1.5: 9 ÷ 1.5 = 6." % V("x"), whole_only=False))
    assert len(its) == 20, len(its)
    return {"title": "Equations with decimals", "items": its}


# ============================================================ set 4: inequalities and number-line graphs
def set_ineq(rnd, P):
    its = []
    # A. solve
    for s in ["2x + 5 < 17", "3x - 4 >= 11", "4x + 3x > 42", "5n + 2n - 3 <= 32", "x + 3x + 7 > 31", "6y - 2y + 10 >= 50"]:
        v = var_of(s)
        A, B, C, r, k = ineq_parts(s)
        wrongk = (C + B) / A
        cands = [(sol(v, OPP[r], k), None), (sol(v, SWAP[r], k), None)]
        if wrongk.denominator == 1 and wrongk != k:
            cands.append((sol(v, r, wrongk), None))
        cands.append((sol(v, r, C - B), None))
        cands.append((sol(v, r, k + 1), None))
        e = ("Solve it like an equation. %s Check a number: %s = %s %s %s is %s. The sign stays %s, and %s %s the number %d itself."
             % (ineq_steps(s), check_text(s, k + (1 if RIGHT[r] else -1)), num(A * (k + (1 if RIGHT[r] else -1)) + B),
                SYM[r], num(C), "true", SYM[r], sol(v, r, k), "includes" if CLOSED[r] else "does not include", k))
        e = e.replace("%s = %s %s" % (check_text(s, k + (1 if RIGHT[r] else -1)), num(A * (k + (1 if RIGHT[r] else -1)) + B), SYM[r]),
                      "%s, and %s %s" % (check_text(s, k + (1 if RIGHT[r] else -1)), num(A * (k + (1 if RIGHT[r] else -1)) + B), SYM[r]))
        assert holds(s, k + (1 if RIGHT[r] else -1))
        its.append(mcq("Solve: %s" % R(s), sol(v, r, k), [c for c, _ in cands], e))
    # B. graph -> which inequality
    for s, alt in [("3x + 2 < 20", "3x + 2 < 26"), ("2x + 2x - 4 >= 12", "2x + 2x + 4 >= 12"),
                   ("4x + 1 > 33", "4x + 9 > 33"), ("5x - 2x + 5 <= 26", "5x + 2x + 5 <= 26")]:
        A, B, C, r, k = ineq_parts(s)
        _, _, _, _, ka = ineq_parts(alt)
        assert ka != k
        a_, _, b_ = split(s)
        right = R(s)
        wrong = [R("%s %s %s" % (a_, SWAP[r], b_)), R("%s %s %s" % (a_, OPP[r], b_)), R(alt)]
        e = ("The graph shows %s: %s circle at %d, arrow to the %s. Solve %s: %s So the answer is <b>%s</b>. %s gives %s instead."
             % (sol("x", r, k), "a closed" if CLOSED[r] else "an open", k, "right" if RIGHT[r] else "left",
                right, ineq_steps(s).replace("<b>", "").replace("</b>", ""), right, R(alt), sol("x", r, ka)))
        its.append(mcq("The graph shows the solution of which inequality?" + fig(nline(window(rnd, k), r, k)), right, wrong, e))
    # C. how to graph
    for s in ["4x + 3 >= 23", "2x + 5x < 49", "3x - 5 > 13"]:
        A, B, C, r, k = ineq_parts(s)
        right = describe(r, k)
        wrong = [describe(SWAP[r], k), describe(OPP[r], k), describe(OPP[SWAP[r]], k)]
        e = "First solve: %s %s" % (ineq_steps(s), why_graph(r, k))
        its.append(mcq("How do you graph the solution of %s on a number line?" % R(s), right, wrong, e))
    # D. verify: which number is (not) a solution
    for s, rr, ws, want in [("3x + 4 > 19", 6, [5, 4, 2], True),
                            ("2x + 3x - 5 >= 30", 7, [6, 5, 3], True),
                            ("4x - x + 2 < 26", 7, [8, 9, 12], True),
                            ("5x + 3 + x <= 51", 9, [8, 7, 2], False)]:
        a_, r, b_ = split(s)
        assert holds(s, rr) == want
        for x in ws:
            assert holds(s, x) != want
        tests = "; ".join("%s, and %s %s %s is %s" % (check_text(s, x), num(side(a_)[0] * x + side(a_)[1]), SYM[r], b_,
                                                      "true" if holds(s, x) else "false") for x in [rr] + ws)
        A, B, C, r, k = ineq_parts(s)
        q = "Which number is %sa solution of %s?" % ("" if want else "<b>not</b> ", R(s))
        e = "Test each number. %s. The solution is %s, so the answer is <b>%d</b>." % (tests, sol("x", r, k), rr)
        its.append(mcq_n(q, rr, ws, e))
    # E. find the mistake in a graph
    for s, drawn, kdrawn in [("2x + 7 <= 21", "<", 7), ("3x - 1 > 14", "<", 5), ("x + 3x + 2 >= 30", ">=", 8)]:
        nm, he, his = P.next()
        A, B, C, r, k = ineq_parts(s)
        svg = nline(window(rnd, min(k, kdrawn)), drawn, kdrawn)
        if kdrawn != k:
            right = "The circle should be at %d" % k
            wrong = ["The circle should be open", "The arrow should point left", "Nothing is wrong"]
            why = "%s added %d instead of subtracting it: (%d + %d) ÷ %d = %d." % (nm, B, C, B, A, kdrawn)
            assert (C + B) / A == kdrawn
        elif CLOSED[drawn] != CLOSED[r]:
            right = "The circle should be %s" % ("closed (filled in)" if CLOSED[r] else "open")
            wrong = ["The arrow should point %s" % ("left" if RIGHT[drawn] else "right"), "The circle should be at %d" % (k + 1),
                     "Nothing is wrong"]
            why = "%s used the wrong kind of circle." % nm
        else:
            right = "The arrow should point %s" % ("right" if RIGHT[r] else "left")
            wrong = ["The circle should be closed (filled in)", "The circle should be at %d" % (k + 1), "Nothing is wrong"]
            why = "%s drew the arrow the wrong way." % nm
        q = "%s solved %s and drew this graph. What is wrong?" % (nm, R(s)) + fig(svg)
        e = "%s %s %s" % (ineq_steps(s), why_graph(r, k), why)
        its.append(mcq(q, right, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Inequalities and number-line graphs", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def word(q, s, x_expect, cands, why="", unit=None, whole_only=True, intro=""):
        x = solve(s)[0]
        assert x == F(x_expect), (s, x)
        e = "%sEquation: %s. %s" % (intro, R(s), steps(s))
        if why:
            e += " " + why
        its.append(mcq_n(q, x, cands + auto_wrongs(collected(s)) + near(x), e, unit, whole_only=whole_only,
                         limit=max(side(split(s)[2])[1], 4 * x, side(split(s)[2])[1] - side(split(s)[0])[1])))

    MO = ("month", "months")
    # 1 phone plan
    nm, he, his = P.next()
    word("%s’s phone plan costs $30 per month, plus $5 for each extra GB of data. This month’s bill is $55. "
         "How many extra GB did %s use?" % (nm, he), "5g + 30 = 55", 5,
         [(11, "forgetting the $30 monthly cost (55 ÷ 5)"), (17, "adding 30 instead of subtracting it")],
         unit=("GB", "GB"))
    # 2 prepaid plan with decimals
    nm, he, his = P.next()
    word("A prepaid phone plan costs $15, plus $0.10 for each minute of long-distance calls. %s’s bill is $27. "
         "How many minutes of long-distance calls did %s make?" % (nm, he), "0.1m + 15 = 27", 120,
         [(12, "forgetting to divide by 0.10"), (F(6, 5), "multiplying by 0.10 instead of dividing")],
         "Dividing by 0.10 is the same as multiplying by 10.", ("minute", "minutes"))
    # 3 gym membership
    nm, he, his = P.next()
    word("A gym charges a $50 sign-up fee, plus $35 per month. %s has paid $260 in all. How many months has %s been a member?"
         % (nm, he), "35m + 50 = 260", 6, [(210, "forgetting to divide by 35")], unit=MO)
    # 4 which equation: climbing gym
    nm, he, his = P.next()
    s = "12v + 45 = 129"
    x = solve(s)[0]
    wr = ["45v + 12 = 129", "12v - 45 = 129", "v + 12 + 45 = 129"]
    assert x == 7 and all(not holds(w, x) for w in wr)
    its.append(mcq("A climbing gym charges a $45 membership fee, plus $12 per visit. %s has spent $129. "
                   "Which equation gives the number of visits, %s?" % (nm, V("v")), R(s), [R(w) for w in wr],
                   "Each visit costs $12, so %s visits cost 12%s. The fee is paid once, so add 45: <b>%s</b>. "
                   "Then 12%s = 84 and %s = 7 visits." % (V("v"), V("v"), R(s), V("v"), V("v"))))
    # 5 pool with decimals
    nm, he, his = P.next()
    word("A community centre pool in Mississauga charges $12 for a membership card, plus $4.50 for each swim. "
         "%s spends $57. How many times does %s swim?" % (nm, he), "4.5s + 12 = 57", 10,
         [(45, "forgetting to divide by 4.50")], unit=("time", "times"))
    # 6 like terms: summer earnings
    nm, he, his = P.next()
    word("%s earned some money cutting grass in July, and twice as much in August. %s earned $450 in all. "
         "How much did %s earn in July?" % (nm, cap(he), he), "x + 2x = 450", 150,
         [(225, "forgetting that x means 1x (2x = 450)"), (300, "giving the August amount"),
          (448, "reading 2x as 2 (x + 2 = 450)")],
         "August was 2 × $150 = $300.", "$", intro="Let %s be the July amount. " % V("x"))
    # 7 rectangle
    word("A rectangular garden is 3 times as long as it is wide. Its perimeter is 64 m. What is its width?",
         "w + 3w + w + 3w = 64", 8, [(16, "using only one width and one length (4w = 64)"), (24, "giving the length"),
                                       (32, "halving the perimeter and stopping (64 ÷ 2)")],
         "The length is 3 × 8 = 24 m.", ("m", "m"),
         intro="Let %s be the width. The sides are %s, 3%s, %s and 3%s. " % ((V("w"),) * 5))
    # 8 triangle
    word("A triangle has sides %s cm, (%s + 4) cm and 2%s cm. Its perimeter is 44 cm. What is %s?" % (V("x"), V("x"), V("x"), V("x")),
         "x + x + 4 + 2x = 44", 10, [(12, "adding the 4 instead of subtracting it"), (20, "giving the longest side")],
         "The sides are 10 cm, 14 cm and 20 cm.", ("cm", "cm"))
    # 9 museum trip
    word("A Grade 7 class goes to the Royal Ontario Museum in Toronto. It costs $12.50 per student, plus $180 for the bus. "
         "The total is $555. How many students go?", "12.5s + 180 = 555", 30,
         [(375, "forgetting to divide by 12.50"), (F(735, 1) / F(25, 2), "adding 180 instead of subtracting it")],
         unit=("student", "students"))
    # 10 taxi in Ottawa
    nm, he, his = P.next()
    word("A taxi in Ottawa charges $4.25 to start, plus $1.95 for each kilometre. %s’s ride costs $23.75. "
         "How long was the ride?" % nm, "1.95k + 4.25 = 23.75", 10,
         [(F(195, 10), "forgetting to divide by 1.95")],
         unit=("km", "km"), whole_only=False)
    # 11 snow shovelling
    nm, he, his = P.next()
    word("%s shovels driveways after a snowstorm for $15 each. %s spent $12 on a new shovel. After paying for the shovel, "
         "%s has made $78. How many driveways did %s shovel?" % (nm, cap(he), he, he), "15d - 12 = 78", 6,
         [(90, "forgetting to divide by 15")], unit=("driveway", "driveways"))
    # 12 bike rental
    nm, he, his = P.next()
    word("A bike rental on Toronto Island costs $8.50 per hour, plus $5 for a helmet. %s pays $39. "
         "For how many hours did %s rent the bike?" % (nm, he), "8.5h + 5 = 39", 4,
         [(34, "forgetting to divide by 8.50")], unit=("hour", "hours"))
    # 13 inequality: snacks
    nm, he, his = P.next()
    s = "4s + 12 <= 40"
    A, B, C, r, k = ineq_parts(s)
    assert k == 7 and holds(s, 7) and not holds(s, 8)
    its.append(mcq_n("%s has $40 to spend at a hockey game. The ticket costs $12, and snacks cost $4 each. "
                     "%s writes 4%s + 12 ≤ 40. What is the greatest number of snacks %s can buy?" % (nm, cap(he), V("s"), he), 7,
                     [(10, "forgetting the $12 ticket (40 ÷ 4)"), (28, "giving the money left for snacks"),
                      (13, "adding 12 instead of subtracting it")],
                     "%s Check: 4 × 7 + 12 = 40, which is allowed. 8 snacks would cost 4 × 8 + 12 = 44, too much."
                     % ineq_steps(s), ("snack", "snacks")))
    # 14 inequality: Terry Fox, round up
    nm, he, his = P.next()
    s = "8k + 45 >= 100"
    assert not holds(s, 6) and holds(s, 7)
    its.append(mcq_n("For the Terry Fox Run, %s has collected $45. %s neighbour will give $8 for each kilometre %s runs. "
                     "%s wants at least $100 in all, so 8%s + 45 ≥ 100. What is the least whole number of kilometres %s must run?"
                     % (nm, cap(his), he, cap(he), V("k"), he), 7,
                     [(6, "rounding 6.875 down instead of up"), (55, "giving the money still needed"),
                      (18, "adding 45 instead of subtracting it (145 ÷ 8, rounded down)")],
                     "Subtract 45: 8%s ≥ 55. Divide by 8: %s ≥ 6.875. The answer must be a whole number that is at least 6.875, "
                     "so round <b>up</b> to 7. Check: 8 × 7 + 45 = 101, which is at least 100. 8 × 6 + 45 = 93 is not enough."
                     % (V("k"), V("k")), ("km", "km")))
    # 15 which inequality: elevator
    a = ["40b + 80 <= 1000", "40b + 80 >= 1000", "40b + 80 < 1000", "80b + 40 <= 1000"]
    its.append(mcq("An elevator can carry at most 1000 kg. A worker who weighs 80 kg is moving boxes of paper that weigh "
                   "40 kg each. Which inequality shows the number of boxes, %s, the worker can take in one trip?" % V("b"),
                   R(a[0]), [R(w) for w in a[1:]],
                   "%s boxes weigh 40%s kg. Add the worker’s 80 kg. “At most 1000” means 1000 is allowed, so use ≤: <b>%s</b>. "
                   "Solving it: 40%s ≤ 920, so %s ≤ 23 boxes." % (V("b"), V("b"), R(a[0]), V("b"), V("b"))))
    assert ineq_parts(a[0])[4] == 23
    # 16 ski hill
    nm, he, his = P.next()
    word("At Blue Mountain near Collingwood, %s rents a snowboard for the season for $40 and buys lift tickets at $65 per day. "
         "%s spends $365 in all. How many days does %s go snowboarding?" % (nm, cap(he), he), "65d + 40 = 365", 5,
         [(325, "forgetting to divide by 65")], unit=("day", "days"))
    # 17 age
    nm, he, his = P.next()
    word("%s’s mom is 41. That is 2 more than 3 times %s’s age. How old is %s?" % (nm, nm, nm), "3a + 2 = 41", 13,
         [(39, "forgetting to divide by 3")], unit=("year old", "years old"), intro="Let %s be %s’s age. " % (V("a"), nm))
    # 18 consecutive numbers
    word("The sum of three consecutive whole numbers is 72. What is the smallest number?",
         "n + n + 1 + n + 2 = 72", 23, [(24, "giving the middle number"), (25, "giving the largest number"),
                                        (F(69, 1), "forgetting to divide by 3")],
         "The numbers are 23, 24 and 25, and 23 + 24 + 25 = 72.",
         intro="Let %s be the smallest number. The next two are %s + 1 and %s + 2. " % (V("n"), V("n"), V("n")))
    # 19 inequality graph
    nm, he, his = P.next()
    s = "3w + 10 >= 40"
    assert ineq_parts(s)[4] == 10
    its.append(mcq("%s’s ringette team has 10 points and gets 3 points for each win. The team needs at least 40 points to make "
                   "the playoffs, so 3%s + 10 ≥ 40. How do you graph the solution?" % (nm, V("w")),
                   describe(">=", 10), [describe(">", 10), describe("<=", 10), describe("<", 10)],
                   "3%s ≥ 30, so %s ≥ 10. %s 10 wins gives exactly 40 points, which counts as “at least 40”."
                   % (V("w"), V("w"), why_graph(">=", 10, "w"))))
    # 20 canoe trip with a decimal answer
    word("A group paddles a 42 km canoe route in Algonquin Park. They paddle the same distance on each of the first 3 days, "
         "then 7.5 km on the last morning. How far do they paddle on each of the first 3 days?", "3d + 7.5 = 42",
         F(23, 2), [(F(345, 10), "forgetting to divide by 3"), (F(495, 30), "adding 7.5 instead of subtracting it"),
                    (14, "dividing 42 by 3 and forgetting the 7.5 km")],
         unit=("km", "km"), whole_only=False)
    assert len(its) == 20, len(its)
    return {"title": "Equation and inequality word problems", "items": its}


# ============================================================ lesson
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
        "<h2>Solve two-step equations</h2>"
        "<p>An <b>equation</b> says two sides are equal. To solve it, find the value of the letter that makes it true. "
        "In " + R("4x + 9 = 41") + ", you multiply " + X + " by 4, then add 9. "
        "<b>Undo the steps in reverse order</b>: undo the + 9 first, then undo the × 4. Do the same to both sides.</p>"
        "<figure class='sn-fig'>" + flow_svg("x", ["× 4", "+ 9"], "41", undo=True) +
        "<figcaption>Top: build 4" + X + " + 9. Bottom: work back from 41. 41 − 9 = 32, then 32 ÷ 4 = 8.</figcaption></figure>" +
        ex("Example 1", "Solve " + R("x/3 + 7 = 12") + ".",
           "Undo + 7 first: " + R("x/3") + " = 5. Then undo ÷ 3 by multiplying: " + X + " = 5 × 3 = 15. "
           "Check: 15 ÷ 3 + 7 = 12.", X + " = 15") +
        "<h2>Collect like terms first</h2>"
        "<p><b>Like terms</b> have the same letter. Add or subtract the numbers in front: 3" + X + " + 2" + X + " = 5" + X + ". "
        "A letter on its own means 1 of it. Combine the plain numbers too. Then solve the two-step equation.</p>"
        "<figure class='sn-fig'>" + scale_svg(["x", "x", "x", "x", "x", "6"], ["41"], "5 blocks x and 6 balance 41") +
        "<figcaption>3" + X + " + 2" + X + " + 6 = 41 is 5" + X + " + 6 = 41. Take 6 off both pans: 5" + X + " = 35, so " + X + " = 7."
        "</figcaption></figure>" +
        ex("Example 2", "Solve " + R("9 + 2n + 5 + 3n = 64") + ".",
           "Collect like terms: 5" + V("n") + " + 14 = 64. Subtract 14: 5" + V("n") + " = 50. Divide by 5: " + V("n") + " = 10. "
           "Check: 9 + 20 + 5 + 30 = 64.", V("n") + " = 10") +
        "<h2>Equations with decimals</h2>"
        "<p>Decimals do not change the steps. Line up the decimal points when you add or subtract, and divide carefully.</p>" +
        ex("Example 3", "Solve " + R("0.5x + 3 = 7") + ".",
           "Subtract 3: 0.5" + X + " = 4. Divide by 0.5: " + X + " = 4 ÷ 0.5 = 8 (there are 8 halves in 4). "
           "Check: 0.5 × 8 + 3 = 7.", X + " = 8") +
        "<h2>Inequalities and number-line graphs</h2>"
        "<p>An <b>inequality</b> uses &lt;, &gt;, ≤ or ≥. Solve it with the same steps. The answer is a range of numbers. "
        "Graph it with a circle and an arrow.</p>" +
        ex("Example 4", "Solve " + R("4x + 3x > 42") + " and graph the solution.",
           "Collect like terms: 7" + X + " &gt; 42. Divide by 7: " + X + " &gt; 6. Check 7: 4 × 7 + 3 × 7 = 49, and 49 &gt; 42 is true. "
           "Check 6: 42 &gt; 42 is false, so 6 is not a solution.", X + " &gt; 6") +
        "<figure class='sn-fig'>" + nline(1, ">", 6) +
        "<figcaption>" + X + " &gt; 6: open circle at 6 (6 is not a solution), arrow to the right.</figcaption></figure>" +
        table(["Symbol", "Circle", "Arrow"], [
            ["&lt;", "open", "left"], ["≤", "closed (filled in)", "left"],
            ["&gt;", "open", "right"], ["≥", "closed (filled in)", "right"]]) +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [R("4x + 12 = 60") + ": 60 ÷ 4 first, so " + X + " = 3", "Undo + 12 first: 4" + X + " = 48, so " + X + " = 12"],
            [R("6n - 5 = 31") + ": subtract 5", "Use the inverse: add 5, so 6" + V("n") + " = 36"],
            ["3" + X + " + 2" + X + " = 6" + X, "Add like terms: 3" + X + " + 2" + X + " = 5" + X],
            [X + " + 5" + X + " = 5" + X, X + " means 1" + X + ": " + X + " + 5" + X + " = 6" + X],
            ["0.5" + X + " = 4, so " + X + " = 2", "Divide by 0.5: " + X + " = 8"],
            ["A closed circle for &lt; or &gt;", "Closed circles are only for ≤ and ≥"],
        ])
    )


FAQ = [
    {"q": "What equations do Grade 7 students solve in the Ontario math curriculum?",
     "a": "In Grade 7 Algebra (C2.3), students solve equations with several terms, whole numbers and decimal numbers, such as 3x + 2x = 35 or 0.5x + 3 = 7, and verify their solutions. They also solve inequalities with several terms (C2.4) and graph the solutions on a number line."},
    {"q": "How do you solve an equation like 3x + 2x + 6 = 41?",
     "a": "Collect like terms first: 3x + 2x = 5x, so 5x + 6 = 41. Subtract 6 from both sides (5x = 35), then divide by 5 (x = 7). Check: 21 + 14 + 6 = 41."},
    {"q": "Why do you undo addition before multiplication when solving 4x + 9 = 41?",
     "a": "4x + 9 means multiply by 4, then add 9, so you undo the steps in reverse order. Dividing first would divide the 41 but not the 9, which gives a wrong answer."},
    {"q": "How do you graph an inequality like x ≥ 5 on a number line?",
     "a": "Put a closed (filled-in) circle at 5, because 5 is a solution, and draw an arrow to the right. For < and > use an open circle, because the number itself is not a solution."},
]


def gen_unit():
    rnd = random.Random(47814)
    P = People(rnd)
    sets = [set_two_step(P), set_terms(P), set_decimals(P), set_ineq(rnd, P), set_words(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "equations-and-inequalities", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Equations and Inequalities: Like Terms, Decimals and Number-Line Graphs",
        "seo_title": "Grade 7 Equations and Inequalities Worksheets: Free Math with Answer Key (Ontario Curriculum)",
        "short_title": "Equations and Inequalities",
        "domain": "Algebra",
        "standard_code": "Grade 7: C2.3",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Solve equations that involve multiple terms, whole numbers, and decimal numbers in various contexts, and verify solutions",
        "meta_desc": "Free Grade 7 math worksheets on equations and inequalities for the Ontario curriculum: two-step equations, collecting like terms (3x + 2x = 35), equations with decimals (0.5x + 3 = 7), inequalities graphed on a number line, and word problems. 100 questions with an answer key.",
        "key_big": "Collect like terms, then undo the steps in reverse order: undo the + or − first, then the × or ÷.",
        "key_sub": "3x + 2x + 6 = 41 becomes 5x + 6 = 41, so 5x = 35 and x = 7. Check by putting 7 back in. Inequalities use the same steps, and the answer is a range of numbers.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:number line|pan balance|number machine))")
    for s_ in u["sets"]:
        for it_ in s_["items"]:
            it_["q"] = rx.sub("<svg data-pf='lg' ", it_["q"])
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
