# -*- coding: utf-8 -*-
"""
US Grade 6 Math: One-Step Equations (6.EE.B.7, with 6.EE.B.5 substitution)
  python tools/gen_us_math_g6_one_step_equations.py
HTML attributes use single quotes (no backslashes in the JSON).
All arithmetic uses fractions.Fraction (exact). Decimals are shown only when they terminate.
Wrong answers come from real mistakes: doing the same operation instead of the inverse (x + 5 = 12 -> 17),
dividing the wrong way (4x = 2 -> 2), multiplying by the fraction instead of dividing (3/4 x = 6 -> 4 1/2),
subtracting without regrouping, a misplaced decimal point, reading 5x as 5 + x, and writing the
equation with the wrong operation.
"""
import json, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
GRAY = "#e4e4e4"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
X = "<i>x</i>"


# ------------------------------------------------------------ numbers
def f(n):
    return "{:,}".format(int(n))


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def terminates(v):
    d = F(v).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dtext(v):
    """Exact decimal text with commas: 2.85, 0.45, 1,250.5."""
    v = F(v)
    assert terminates(v), v
    n, d = v.numerator, v.denominator
    k = 0
    while d * 1 != 1 and (10 ** k) % d:
        k += 1
    s = str(n * (10 ** k) // d).rjust(k + 1, "0")
    ip, fp = (s[:-k], s[-k:]) if k else (s, "")
    return f(int(ip)) + ("." + fp if fp else "")


def ftext(v):
    """Simplest form; mixed number above 1: 2 1/2."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return f(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%s %s" % (f(w), fr(r, v.denominator))


def money(v):
    v = F(v)
    assert (v * 100).denominator == 1, v
    c = int(v * 100)
    return "$%s.%02d" % (f(c // 100), c % 100)


def show(v, style):
    """style: 'd' decimal, 'f' fraction, '$' money. None if it cannot be shown in that style."""
    v = F(v)
    if v <= 0:
        return None
    if style == "$":
        return money(v) if (v * 100).denominator == 1 else None
    if style == "m":                  # money amount inside an equation: 16, 4.30
        if (v * 100).denominator != 1:
            return None
        return f(v) if v.denominator == 1 else money(v)[1:]
    if v.denominator == 1:
        return f(v)
    if style == "d":
        return dtext(v) if terminates(v) else None
    return ftext(v)


def plain(v, style):
    """Text without HTML (for figures)."""
    s = show(v, style)
    assert "<" not in s, s
    return s


def coef(p, style, var=X):
    """4x, 0.5x, (3/4)x"""
    style = "m" if style == "$" else style
    return show(p, style) + var


# ------------------------------------------------------------ mistakes
def digits(a, b):
    """Two nonnegative decimals as whole numbers of the smallest place."""
    k = 0
    while (F(a) * 10 ** k).denominator != 1 or (F(b) * 10 ** k).denominator != 1:
        k += 1
    return int(F(a) * 10 ** k), int(F(b) * 10 ** k), k


def sub_errors(a, b):
    """a − b done in columns. Returns (no regrouping: smaller digit from larger,
    regrouped but did not make the next place 1 less)."""
    A, Bv, k = digits(a, b)
    da, db = str(A)[::-1], str(Bv)[::-1]
    n = max(len(da), len(db))
    da, db = da.ljust(n, "0"), db.ljust(n, "0")
    nb = sum(abs(int(x) - int(y)) * 10 ** i for i, (x, y) in enumerate(zip(da, db)))
    nr = sum(((int(x) - int(y)) % 10) * 10 ** i for i, (x, y) in enumerate(zip(da, db)))
    return F(nb, 10 ** k), F(nr, 10 ** k)


def add_nocarry(a, b):
    """a + b done in columns, forgetting to carry."""
    A, Bv, k = digits(a, b)
    da, db = str(A)[::-1], str(Bv)[::-1]
    n = max(len(da), len(db))
    da, db = da.ljust(n, "0"), db.ljust(n, "0")
    return F(sum(((int(x) + int(y)) % 10) * 10 ** i for i, (x, y) in enumerate(zip(da, db))), 10 ** k)


def whole_frac(v):
    w = v.numerator // v.denominator
    return w, v - w


def add_mistakes(p, q, style):
    """x + p = q (answer q − p): wrong values with the reason."""
    style = "m" if style == "$" else style
    out = [(q + p, "adds %s instead of subtracting it" % show(p, style))]
    if style in ("d", "m") or (p.denominator == 1 and q.denominator == 1):
        nb, nr = sub_errors(q, p)
        out += [(nb, "subtracts the smaller digit from the larger one instead of regrouping"),
                (nr, "regroups but forgets to make the next place 1 less")]
    else:
        wq, fq = whole_frac(q)
        wp, fp = whole_frac(p)
        if wq and wp is not None and fq != fp:
            out.append((wq - wp + abs(fq - fp), "subtracts the whole numbers and the fractions separately without regrouping"))
        if fq.denominator != fp.denominator and fq and fp and fq.denominator > fp.denominator:
            out.append((F(fq.numerator - fp.numerator, fq.denominator - fp.denominator) + wq - wp
                        if fq.numerator > fp.numerator else None, "subtracts the tops and the bottoms"))
        if fq and fp and fq.denominator != fp.denominator and fq.numerator > fp.numerator:
            out.append((F(fq.numerator - fp.numerator, max(fq.denominator, fp.denominator)) + wq - wp,
                        "subtracts the numerators without a common denominator"))
    out.append((q, "forgets to subtract %s" % show(p, style)))
    out.append((p, "copies the number that was added"))
    return out


def sub_mistakes(p, q, style):
    """x − p = q (answer q + p)."""
    style = "m" if style == "$" else style
    out = [(q - p, "subtracts %s instead of adding it" % show(p, style))]
    if style in ("d", "m") or (p.denominator == 1 and q.denominator == 1):
        out.append((add_nocarry(q, p), "adds without carrying"))
    out.append((q, "forgets to add %s" % show(p, style)))
    out.append((p - q, "subtracts the smaller number from the larger"))
    return out


def mul_mistakes(p, q, style):
    """px = q (answer q ÷ p)."""
    style = "m" if style == "$" else style
    ps = show(p, style)
    out = [(p * q, "multiplies by %s instead of dividing by %s" % (ps, ps)),
           (p / q, "divides %s by %s, the wrong way" % (ps, show(q, style)))]
    if p.denominator != 1 and style == "f":
        out.append((q * p.denominator, "multiplies by %d but forgets to divide by %d" % (p.denominator, p.numerator)))
        out.append((q / p.numerator if p.numerator > 1 else None, "divides by %d but forgets to multiply by %d" % (p.numerator, p.denominator)))
    if style in ("d", "m"):
        out.append((q / p * 10, "puts the decimal point in the wrong place"))
        out.append((q / p / 10, "puts the decimal point in the wrong place"))
    out.append((q - p, "subtracts %s instead of dividing" % ps))
    out.append((q + p, "adds %s instead of dividing" % ps))
    return out


# ------------------------------------------------------------ equations
def eq_text(kind, p, q, style, var=X, form=0):
    style = "m" if style == "$" else style
    ps, qs = show(p, style), show(q, style)
    if kind == "add":
        return ["%s + %s = %s" % (var, ps, qs), "%s + %s = %s" % (ps, var, qs), "%s = %s + %s" % (qs, var, ps)][form]
    if kind == "sub":
        return "%s − %s = %s" % (var, ps, qs)
    return ["%s = %s" % (coef(p, style, var), qs), "%s = %s" % (qs, coef(p, style, var))][form]


def solution(kind, p, q):
    return {"add": q - p, "sub": q + p, "mul": q / p}[kind]


def mistakes(kind, p, q, style):
    return {"add": add_mistakes, "sub": sub_mistakes, "mul": mul_mistakes}[kind](p, q, style)


def times(a, b, style):
    """a × b written for an explanation (fraction coefficient in front)."""
    style = "m" if style == "$" else style
    return "%s × %s" % (show(a, style), show(b, style))


def check_text(kind, p, q, v, style):
    style = "m" if style == "$" else style
    if kind == "add":
        return "%s + %s = %s" % (show(v, style), show(p, style), show(q, style))
    if kind == "sub":
        return "%s − %s = %s" % (show(v, style), show(p, style), show(q, style))
    return "%s = %s" % (times(p, v, style), show(q, style))


def solve_text(kind, p, q, style, var=X):
    """Inverse step and the value."""
    style = "m" if style == "$" else style
    v = solution(kind, p, q)
    ps, qs, vs = show(p, style), show(q, style), show(v, style)
    if kind == "add":
        return "Subtract %s from both sides: %s = %s − %s = %s." % (ps, var, qs, ps, vs)
    if kind == "sub":
        return "Add %s to both sides: %s = %s + %s = %s." % (ps, var, qs, ps, vs)
    if p.denominator != 1 and style == "f":
        inv = fr(p.denominator, p.numerator) if p.numerator != 1 else str(p.denominator)
        return ("Divide both sides by %s, which is the same as multiplying by %s: %s = %s × %s = %s."
                % (ps, inv, var, qs, inv, vs))
    return "Divide both sides by %s: %s = %s ÷ %s = %s." % (ps, var, qs, ps, vs)


# ------------------------------------------------------------ question helpers
def mcq(q, correct, cands, e):
    """correct / cands: (html, key). Choices with the same key (value) as one already used are skipped.
    Positions are set later by balance()."""
    seen = {correct[1]}
    pick = []
    for c in cands:
        if c is None or c[0] is None or c[1] is None:
            continue
        if c[1] in seen:
            continue
        seen.add(c[1])
        pick.append(c[0])
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct[0]] + pick, "a": 0, "e": e}


def vals(vs, style, unit=None):
    out = []
    for v in vs:
        v = F(v)
        s = show(v, style)
        if s is None:
            out.append(None)
            continue
        out.append((with_unit(v, s, unit), v))
    return out


def with_unit(v, s, unit):
    if unit is None or unit == "$":
        return s
    one = v == 1 or (v < 1 and "class='fr'" in s)      # 1 batch, 3/4 cup, but 0.45 pounds
    return "%s %s" % (s, unit[0] if one else unit[1])


def wrongs(kind, p, q, style, n_need=3):
    v = solution(kind, p, q)
    out, seen = [], {v}
    for w, why in mistakes(kind, p, q, style):
        if w is None:
            continue
        w = F(w)
        if w <= 0 or w in seen or show(w, style) is None:
            continue
        seen.add(w)
        out.append((w, why))
    assert len(out) >= n_need, (kind, p, q, out)
    return out


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def B(s):
    return "<b>%s</b>" % s


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [c[it["a"]]] + wrong[t:]
            it["a"] = t


def solve_item(kind, p, q, style, ask, form=0):
    p, q = F(p), F(q)
    v = solution(kind, p, q)
    assert v > 0
    ws = wrongs(kind, p, q, style)
    eq = eq_text(kind, p, q, style, form=form)
    e = "%s Check: %s. Not %s: that %s." % (solve_text(kind, p, q, style), check_text(kind, p, q, v, style),
                                           show(ws[0][0], style), ws[0][1])
    return mcq(ask % B(eq), (show(v, style), v), vals([w for w, _ in ws], style), e)


# ------------------------------------------------------------ figures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(".") * 0.6) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK, italic=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, col, anchor, " font-style='italic'" if italic else "", t))


def bracket_top(x0, x1, y, label):
    """Bracket over a bar (ticks down to y), label above it."""
    return ("<path d='M%.1f %.1f v-7 H%.1f v7' fill='none' stroke='%s' stroke-width='2'/>" % (x0, y, x1, INK)
            + text((x0 + x1) / 2, y - 13, label))


def tape_add(p, q, style):
    """Tape diagram for x + p = q, parts drawn to scale."""
    v = q - p
    L = 300.0
    wx, wp = float(v / q) * L, float(p / q) * L
    ps = plain(p, style)
    assert wx >= 30 and wp >= tw(ps, 16) + 12, (p, q)
    x0, y = 8, 34
    s = ["<rect x='%.1f' y='%d' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0, y, wx, FILL, GREEN),
         "<rect x='%.1f' y='%d' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0 + wx, y, wp, GRAY, GREEN),
         text(x0 + wx / 2, y + 23, "x", 18, col=RED, italic=True),
         text(x0 + wx + wp / 2, y + 23, ps),
         bracket_top(x0, x0 + L, y - 4, plain(q, style))]
    return svg_wrap(int(x0 * 2 + L), y + 40, "".join(s), "tape diagram: a part x and a part %s make %s" % (ps, plain(q, style)))


def tape_mul(k, q, style):
    """Tape diagram for kx = q: k equal parts, each x."""
    cw = 40
    x0, y = 8, 34
    s = []
    for i in range(k):
        s.append("<rect x='%d' y='%d' width='%d' height='34' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x0 + i * cw, y, cw, FILL, GREEN))
        s.append(text(x0 + i * cw + cw / 2, y + 23, "x", 18, col=RED, italic=True))
    s.append(bracket_top(x0, x0 + k * cw, y - 4, plain(q, style)))
    W = max(x0 * 2 + k * cw, int(x0 + k * cw / 2 + tw(plain(q, style), 16) / 2 + 8))
    return svg_wrap(W, y + 40, "".join(s), "tape diagram: %d equal parts, each x, make %s" % (k, plain(q, style)))


def scale_svg(left, right, label):
    """A level pan balance. left / right: lists of 'x' or a number label."""
    def item_w(t):
        return 34 if t == "x" else max(34, int(tw(t, 16) + 14))
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
            if t == "x":
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, FILL, GREEN))
                s.append(text(x + iw / 2, top + 24, "x", 18, col=RED, italic=True))
            else:
                s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, top, iw, ih, GRAY, INK))
                s.append(text(x + iw / 2, top + 23, t))
            x += iw + gap
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (c - w / 2, py, w, INK))
        s.append("<rect x='%.1f' y='%d' width='4' height='18' fill='%s'/>" % (c - 2, py + 6, INK))
    by = py + 24
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='6' fill='%s'/>" % (cl - 2, by, cr - cl + 4, INK))
    s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (mid, by + 6, mid - 22, by + 40, mid + 22, by + 40, GREEN))
    s.append("<rect x='%.1f' y='%d' width='80' height='5' fill='%s'/>" % (mid - 40, by + 40, INK))
    W = int(cr + wr / 2 + 8)
    return svg_wrap(W, by + 47, "".join(s), "pan balance: " + label)


# ------------------------------------------------------------ set 1: is it a solution? (6.EE.B.5)
def set_substitute(rnd, P):
    its = []
    # a) which value is a solution?  (kind, p, q, style, form)
    A = [("add", 5, 12, "f", 0), ("add", 38, 91, "f", 1), ("add", F("2.5"), F("8.1"), "d", 0),
         ("add", F(1, 4), F(3, 4), "f", 2), ("mul", 7, 56, "f", 0), ("mul", 6, 3, "f", 0),
         ("mul", F("0.5"), F("4.5"), "d", 0), ("mul", F(2, 3), 8, "f", 1)]
    ASK = ["Which value of %s is a solution of %%s?" % X, "Which number makes %s true?",
           "Which value of %s makes %%s true?" % X, "Which number is a solution of %s?"]
    for k, (kind, p, q, style, form) in enumerate(A):
        p, q = F(p), F(q)
        v = solution(kind, p, q)
        ws = wrongs(kind, p, q, style)
        eq = eq_text(kind, p, q, style, form=form)
        w = ws[0][0]
        wrong_check = check_text(kind, p, q, w, style).rsplit(" = ", 1)[0]
        wrong_val = {"add": w + p, "sub": w - p, "mul": p * w}[kind]
        e = ("Substitute %s for %s: %s is true. If %s = %s, then %s = %s, not %s."
             % (show(v, style), X, check_text(kind, p, q, v, style), X, show(w, style), wrong_check,
                show(wrong_val, style), show(q, style)))
        its.append(mcq(ASK[k % 4] % B(eq), (show(v, style), v), vals([x for x, _ in ws], style), e))

    # b) which equation has x = v as a solution?
    B_ = [(6, 5), (9, 4), (12, 3), (F("1.5"), 4), (F(1, 2), 6), (8, 7)]
    for k, (v, a) in enumerate(B_):
        v, a = F(v), F(a)
        st = "d" if v.denominator in (2, 4, 5, 10) and k == 3 else "f"
        good_kind = "mul" if k % 2 == 0 else "add"
        eqs = {
            "mul": ("mul", a, a * v),
            "add": ("add", a, a + v),
            "read_add": ("mul", a, a + v),           # reads 5x as 5 + x
            "read_mul": ("add", a, a * v),           # reads x + 5 as 5 times x
            "swap": ("add", v, v + a),               # puts the value where the added number goes: x + 6 = 11
            "div": ("mul", a, a / v),                # divides instead of multiplying: 6x = 12 for x = 1/2
        }
        if v.denominator == 1 and v < 10:
            eqs["digits"] = ("mul", a, F(int("%d%d" % (a, v))))   # reads 5x with x = 6 as 56
        good = eqs[good_kind]
        bad_keys = [x for x in ["read_add", "read_mul", "digits", "swap", "div"] if x in eqs]
        bad = []
        for b in bad_keys:
            kd, p, q = eqs[b]
            if solution(kd, p, q) != v and solution(kd, p, q) > 0 and eqs[b] != good:
                bad.append(eqs[b])
        assert len(bad) >= 3, (v, a, bad)
        cands = [(eq_text(kd, p, q, st), eq_text(kd, p, q, st)) for kd, p, q in bad]
        kd, p, q = good
        g = eq_text(kd, p, q, st)
        bk, bp, bq = bad[0]
        e = ("Substitute %s for %s in each equation. %s, so %s is true. In %s, %s, not %s."
             % (show(v, st), X, check_text(kd, p, q, v, st), g, eq_text(bk, bp, bq, st),
                check_text(bk, bp, {"add": v + bp, "mul": bp * v}[bk], v, st).rsplit(" = ", 1)[0] + " = " + show({"add": v + bp, "mul": bp * v}[bk], st),
                show(bq, st)))
        if kd == "mul":
            e += " Remember: %s means %s times %s." % (coef(p, st), show(p, st), X)
        its.append(mcq("Which equation has %s as a solution?" % B("%s = %s" % (X, show(v, st))), (g, g), cands, e))

    # c) is it a solution?
    C = [("add", 9, 23, "f", "yes"), ("mul", 4, 36, "f", "no"), ("add", F("1.6"), F("3.5"), "d", "no"),
         ("mul", 5, 4, "f", "yes"), ("mul", F(3, 4), 6, "f", "no"), ("add", 125, 300, "f", "yes")]
    for kind, p, q, style, yn in C:
        p, q = F(p), F(q)
        v = solution(kind, p, q)
        ws = wrongs(kind, p, q, style)
        test = v if yn == "yes" else ws[0][0]
        eq = eq_text(kind, p, q, style)
        lhs = {"add": test + p, "mul": p * test}[kind]
        chk = check_text(kind, p, q, test, style).rsplit(" = ", 1)[0] + " = " + show(lhs, style)
        no = lambda w: ("No, %s = %s" % (X, show(w, style)), w)
        cands = [("Yes", "yes")] + [no(w) for w, _ in ws]
        if yn == "yes":
            correct = ("Yes", "yes")
            e = "Substitute %s for %s: %s. Both sides are equal, so %s is a solution." % (show(v, style), X, chk, show(v, style))
        else:
            correct = no(v)
            e = ("Substitute %s for %s: %s, not %s, so it is not a solution. The solution is %s, because %s."
                 % (show(test, style), X, chk, show(q, style), show(v, style), check_text(kind, p, q, v, style)))
            cands = [("Yes", "yes")] + [no(w) for w, _ in ws[1:]]
        its.append(mcq("Is %s a solution of %s?" % (B(show(test, style)), B(eq)), correct, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Is it a solution? Substitute and check", "items": its}


# ------------------------------------------------------------ set 2: x + p = q
def set_add(rnd, P):
    its = []
    R = rnd.randint
    ASK = ["Solve %s.", "What is the value of %s in %%s?" % X, "Solve for %s: %%s" % X, "Find %s: %%s" % X]
    used = set()

    def pick(maker, ok):
        for _ in range(5000):
            d = maker()
            if d not in used and ok(*d):
                used.add(d)
                return d
        raise RuntimeError("no numbers for spec %d" % len(its))

    def regroup(p, q):
        nb, nr = sub_errors(q, p)
        return q - p > 0 and nb != q - p and nr != q - p

    specs = [
        # (kind, maker, style, form, ok)
        ("add", lambda: (F(R(5, 9)), F(R(12, 18))), "f", 0, lambda p, q: q - p > 1 and regroup(p, q)),
        ("add", lambda: (F(R(12, 19)), F(R(31, 49))), "f", 1, regroup),
        ("add", lambda: (F(R(25, 69)), F(R(105, 160))), "f", 0, regroup),
        ("add", lambda: (F(R(12, 38) * 10 + R(1, 9)), F(R(4, 7) * 100)), "f", 2, regroup),
        ("add", lambda: (F(R(25, 75) * 15), F(R(10, 15) * 125)), "f", 0, lambda p, q: q > 1000 and regroup(p, q)),
        ("sub", lambda: (F(R(12, 29)), F(R(21, 48))), "f", 0, lambda p, q: q > p and add_nocarry(q, p) != q + p),
        ("add", lambda: (F(R(11, 39), 10), F(R(51, 99), 10)), "d", 0, regroup),
        ("add", lambda: (F(R(51, 99), 100), F(R(2, 6))), "d", 0, regroup),
        ("add", lambda: (F(R(31, 69), 10), F(R(1001, 1499), 100)), "d", 1, regroup),
        ("add", lambda: (F(R(101, 149), 100), F(R(41, 69), 10)), "d", 0, regroup),
        ("add", lambda: (F(R(5, 9), 10), F(R(11, 39), 10)), "d", 2, regroup),
        ("sub", lambda: (F(R(11, 39), 10), F(R(105, 495), 100)), "d", 0, lambda p, q: add_nocarry(q, p) != q + p),
        ("add", lambda: (F(R(81, 179) * 5, 100), F(R(10, 20))), "d", 2, regroup),
    ]
    for k, (kind, mk, style, form, ok) in enumerate(specs):
        p, q = pick(mk, ok)
        its.append(solve_item(kind, p, q, style, ASK[k % 4], form))
    # fractions (hand-picked so the mistakes are real and different)
    FR = [(F(1, 4), F(3, 4), 0), (F(2, 5), F(1), 1), (F(1, 3), F(5, 6), 0), (F(3, 8), F(7, 8), 2),
          (F(3, 2), F(4), 0), (F(2, 3), F(13, 4), 1), (F(5, 4), F(23, 6), 0)]
    for k, (p, q, form) in enumerate(FR):
        its.append(solve_item("add", p, q, "f", ASK[(k + 1) % 4], form))
    assert len(its) == 20, len(its)
    return {"title": "Solve x + p = q (subtract to undo adding)", "items": its}


# ------------------------------------------------------------ set 3: px = q
def set_mul(rnd, P):
    its = []
    R = rnd.randint
    ASK = ["Solve %s.", "What is the value of %s in %%s?" % X, "Solve for %s: %%s" % X, "Find %s: %%s" % X]
    used = set()
    whole = []
    for lo, hi, alo, ahi in [(6, 9, 6, 9), (7, 9, 11, 15), (12, 15, 12, 25), (25, 25, 12, 39)]:
        while True:
            p, v = R(lo, hi), R(alo, ahi)
            if (p, v) not in used and p != v:
                used.add((p, v))
                break
        whole.append((F(p), F(p * v)))
    S = [(p, q, "f", 0) for p, q in whole]
    S += [(F(4), F(2), "f", 0), (F(6), F(15), "f", 1), (F(8), F(6), "f", 0)]
    S += [(F("0.5"), F("4.5"), "d", 0), (F("1.2"), F(6), "d", 0), (F(4), F("9.6"), "d", 1),
          (F("0.25"), F(3), "d", 0), (F(3), F("0.42"), "d", 0), (F("2.5"), F("11.25"), "d", 0)]
    S += [(F(3, 4), F(6), "f", 0), (F(2, 3), F(10), "f", 0), (F(1, 2), F(7), "f", 1), (F(1, 5), F(3, 4), "f", 0),
          (F(5), F(2, 3), "f", 0), (F(2, 5), F(4, 15), "f", 0), (F(3, 8), F(9, 16), "f", 1)]
    for k, (p, q, style, form) in enumerate(S):
        its.append(solve_item("mul", p, q, style, ASK[k % 4], form))
    assert len(its) == 20, len(its)
    return {"title": "Solve px = q (divide to undo multiplying)", "items": its}


# ------------------------------------------------------------ set 4: models and inverse operations
def eq_choices(kind, p, q, style):
    """The matching equation and three that use the wrong operation or the wrong order."""
    ps, qs = show(p, style), show(q, style)
    good = eq_text(kind, p, q, style)
    if kind == "add":
        bad = [eq_text("mul", p, q, style), "%s = %s + %s" % (X, qs, ps), "%s + %s = %s" % (X, qs, ps)]
    else:
        bad = ["%s + %s = %s" % (X, ps, qs), "%s = %s × %s" % (X, qs, ps), "%s = %s" % (coef(q, style), ps)]
    return good, bad


def set_models(rnd, P):
    its = []
    # tape diagrams: which equation?
    for kind, p, q in [("add", 18, 45), ("mul", 5, 35), ("add", F("2.5"), F("6.5")), ("mul", 4, 22)]:
        p, q = F(p), F(q)
        st = "d"
        svg = tape_add(p, q, st) if kind == "add" else tape_mul(int(p), q, st)
        good, bad = eq_choices(kind, p, q, st)
        v = solution(kind, p, q)
        if kind == "add":
            e = ("The parts %s and %s make the whole %s: %s. Not %s: the diagram shows two parts added together, not equal parts." %
                 (X, show(p, st), show(q, st), good, bad[0]))
        else:
            e = ("There are %s equal parts, each %s, and they make %s: %s. Not %s: the parts are equal, so this is multiplication."
                 % (show(p, st), X, show(q, st), good, bad[0]))
        e += " So %s = %s." % (X, show(v, st))
        its.append(mcq(fig(svg) + "Which equation matches the tape diagram?", (good, good), [(b, b) for b in bad], e))
    # tape diagrams: what is x?
    for kind, p, q in [("add", 27, 63), ("mul", 6, 21)]:
        p, q = F(p), F(q)
        st = "d"
        svg = tape_add(p, q, st) if kind == "add" else tape_mul(int(p), q, st)
        v = solution(kind, p, q)
        ws = wrongs(kind, p, q, st)
        e = "The diagram shows %s. %s Not %s: that %s." % (eq_text(kind, p, q, st), solve_text(kind, p, q, st),
                                                         show(ws[0][0], st), ws[0][1])
        its.append(mcq(fig(svg) + "What is the value of %s?" % X, (show(v, st), v), vals([w for w, _ in ws], st), e))
    # balances
    BAL = [("add", 7, 15, ["x", "7"], ["15"], "eq"), ("mul", 3, 18, ["x", "x", "x"], ["18"], "eq"),
           ("add", 26, 40, ["26", "x"], ["40"], "solve"), ("mul", 4, 30, ["x", "x", "x", "x"], ["30"], "solve")]
    for kind, p, q, left, right, mode in BAL:
        p, q = F(p), F(q)
        st = "d"
        svg = scale_svg(left, right, "%s on the left and %s on the right" % (" and ".join(left), " and ".join(right)))
        v = solution(kind, p, q)
        if mode == "eq":
            good, bad = eq_choices(kind, p, q, st)
            if kind == "add":
                e = "The left pan holds %s and %s, and it balances %s: %s. The two sides are equal, so %s = %s." % (X, show(p, st), show(q, st), good, X, show(v, st))
            else:
                e = "The left pan holds %s boxes, each %s, so it is %s. It balances %s: %s. So %s = %s." % (show(p, st), X, coef(p, st), show(q, st), good, X, show(v, st))
            its.append(mcq(fig(svg) + "The scale is balanced. Which equation does it show?", (good, good), [(b, b) for b in bad], e))
        else:
            ws = wrongs(kind, p, q, st)
            if kind == "add":
                how = "Take %s off both pans to keep it balanced: %s = %s − %s = %s." % (show(p, st), X, show(q, st), show(p, st), show(v, st))
            else:
                how = "Split both pans into %s equal groups: %s = %s ÷ %s = %s." % (show(p, st), X, show(q, st), show(p, st), show(v, st))
            e = "The scale shows %s. %s Not %s: that %s." % (eq_text(kind, p, q, st, form=1 if left[0] != "x" else 0),
                                                            how, show(ws[0][0], st), ws[0][1])
            its.append(mcq(fig(svg) + "The scale is balanced. What is the value of %s?" % X, (show(v, st), v),
                           vals([w for w, _ in ws], st), e))
    # first step
    FIRST = [
        ("add", F("4.6"), F(9), "d", 0, "Subtract 4.6 from both sides", ["Add 4.6 to both sides", "Divide both sides by 4.6", "Subtract 9 from both sides"]),
        ("add", F(15), F(32), "d", 1, "Subtract 15 from both sides", ["Add 15 to both sides", "Subtract 32 from both sides", "Divide both sides by 15"]),
        ("mul", F(8), F(56), "d", 0, "Divide both sides by 8", ["Multiply both sides by 8", "Subtract 8 from both sides", "Divide both sides by 56"]),
        ("mul", F("0.4"), F(2), "d", 0, "Divide both sides by 0.4", ["Multiply both sides by 0.4", "Subtract 0.4 from both sides", "Divide both sides by 2"]),
        ("mul", F(2, 5), F(8), "f", 0, "Multiply both sides by " + fr(5, 2), ["Multiply both sides by " + fr(2, 5), "Subtract " + fr(2, 5) + " from both sides", "Divide both sides by 8"]),
        ("sub", F(12), F(30), "d", 0, "Add 12 to both sides", ["Subtract 12 from both sides", "Subtract 30 from both sides", "Divide both sides by 12"]),
    ]
    WHY = {"add": "%s is added to %s, so subtracting %s undoes it.",
           "sub": "%s is subtracted from %s, so adding %s undoes it.",
           "mul": "%s is multiplied by %s, so dividing by %s undoes it."}
    for kind, p, q, st, form, good, bad in FIRST:
        v = solution(kind, p, q)
        ps = show(p, st)
        if kind == "mul":
            why = "%s is multiplied by %s, so dividing by %s undoes it." % (X, ps, ps)
        else:
            why = WHY[kind] % (ps, X, ps) if kind == "add" else WHY[kind] % (ps, X, ps)
        e = "%s %s Check: %s." % (why, solve_text(kind, p, q, st), check_text(kind, p, q, v, st))
        its.append(mcq("What is the best first step to solve %s?" % B(eq_text(kind, p, q, st, form=form)), (good, good),
                       [(b, b) for b in bad], e))
    # find the mistake
    for _ in range(4):
        pass
    ERR = [("add", F(9), F(23), "d", F(32), "added 9 instead of subtracting it",
            ["divided 23 by 9", "subtracted 23 from 9", "made no mistake"]),
           ("mul", F(6), F(3), "f", F(2), "divided 6 by 3 instead of 3 by 6",
            ["multiplied 6 by 3", "subtracted 3 from 6", "made no mistake"]),
           ("mul", F(3, 4), F(6), "f", F(9, 2), "multiplied by %s instead of dividing by it" % fr(3, 4),
            ["divided 6 by 4", "subtracted %s from 6" % fr(3, 4), "made no mistake"]),
           ("mul", F("0.5"), F("4.5"), "d", F("2.25"), "multiplied by 0.5 instead of dividing by it",
            ["subtracted 0.5 from 4.5", "divided 4.5 by 5", "made no mistake"])]
    claims = {"divided 23 by 9": F(23, 9), "subtracted 23 from 9": None, "multiplied 6 by 3": F(18), "subtracted 3 from 6": F(3),
              "divided 6 by 4": F(3, 2), "subtracted %s from 6" % fr(3, 4): F(21, 4), "subtracted 0.5 from 4.5": F(4),
              "divided 4.5 by 5": F("0.9")}
    for kind, p, q, st, got, what, bad in ERR:
        n, he, his = P.next()
        v = solution(kind, p, q)
        assert got != v and got in [w for w, _ in mistakes(kind, p, q, st)]
        for b in bad:
            assert b == "made no mistake" or claims[b] != got, b
        e = ("%s %s. %s Check: %s." % (n, what, solve_text(kind, p, q, st), check_text(kind, p, q, v, st)))
        its.append(mcq("%s solved %s and got %s. What mistake did %s make?"
                       % (n, B(eq_text(kind, p, q, st)), B("%s = %s" % (X, show(got, st))), he),
                       (cap(he) + " " + what, "good"), [(cap(he) + " " + b, b) for b in bad], e))
    assert len(its) == 20, len(its)
    return {"title": "Models and inverse operations: tape diagrams, balances and first steps", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words(rnd, P):
    its = []

    def var(c):
        return "<i>%s</i>" % c

    # (story, letter, kind of the true equation, p, q, style, form)  -> which equation?
    def eq_item(story, c, kind, p, q, st, form=0):
        st = "m" if st == "$" else st
        v_ = var(c)
        p, q = F(p), F(q)
        ps, qs = show(p, st), show(q, st)
        good = eq_text(kind, p, q, st, v_, form)
        if kind == "add":
            bad = [eq_text("mul", p, q, st, v_), "%s = %s + %s" % (v_, qs, ps), "%s + %s = %s" % (v_, qs, ps)]
        else:
            bad = ["%s + %s = %s" % (v_, ps, qs), "%s = %s × %s" % (v_, qs, ps), "%s = %s" % (coef(q, st, v_), ps)]
        v = solution(kind, p, q)
        s = solve_text(kind, p, q, st, v_)
        e = "%s matches the story. %s Not %s: %s." % (good, s, bad[0],
                                                   "the story adds, it does not multiply" if kind == "add" else "the story has equal groups, so it multiplies")
        return mcq(story + " Which equation can you use to find %s?" % v_, (good, good), [(b, b) for b in bad], e)

    n, he, his = P.next()
    sib = "brother" if he == "she" else "sister"
    its.append(eq_item("%s is 13 years old. %s is 4 years older than %s %s. Let %s be %s %s’s age."
                       % (n, cap(he), his, sib, var("s"), his, sib), "s", "add", 4, 13, "d"))
    its.append(eq_item("A book costs $12.50. That is 5 times the cost of a pen. Let %s be the cost of the pen in dollars." % var("p"),
                       "p", "mul", 5, F("12.50"), "$"))
    n, he, his = P.next()
    its.append(eq_item("%s rode %s bike 3.5 miles before lunch. By the end of the day, %s had ridden 9 miles in all. "
                       "Let %s be the miles %s rode after lunch." % (n, his, he, var("m"), he), "m", "add", F("3.5"), 9, "d"))
    n, he, his = P.next()
    its.append(eq_item("A recipe uses %s cup of sugar for each batch of cookies. %s used 6 cups of sugar. Let %s be the number of batches."
                       % (fr(3, 4), n, var("b")), "b", "mul", F(3, 4), 6, "f"))
    its.append(eq_item("8 friends share the cost of a party equally. The party costs $96. Let %s be the amount each friend pays in dollars." % var("d"),
                       "d", "mul", 8, 96, "d"))
    its.append(eq_item("A plant grew 2.4 cm this week. Now it is 15.1 cm tall. Let %s be its height last week in centimeters." % var("h"),
                       "h", "add", F("2.4"), F("15.1"), "d"))
    n, he, his = P.next()
    its.append(eq_item("%s walks at 3 miles per hour. Let %s be the number of hours it takes %s to walk 7.5 miles."
                       % (n, var("t"), "her" if he == "she" else "him"), "t", "mul", 3, F("7.5"), "d"))
    n, he, his = P.next()
    its.append(eq_item("%s has saved $38. %s needs $65 for a jacket. Let %s be how much more money %s needs in dollars."
                       % (n, cap(he), var("m"), he), "m", "add", 38, 65, "d", 1))

    # solve: (question, kind, p, q, style, unit, equation letter, extra wrong values with reasons)
    def solve_story(q_text, kind, p, q, st, unit, c):
        p, q = F(p), F(q)
        v = solution(kind, p, q)
        ws = wrongs(kind, p, q, st)
        U = lambda x: with_unit(x, show(x, st), unit)
        e = "Equation: %s. %s Answer: %s. Not %s: that %s." % (eq_text(kind, p, q, st, var(c)), solve_text(kind, p, q, st, var(c)),
                                                             U(v), U(ws[0][0]), ws[0][1])
        return mcq(q_text, (U(v), v), vals([w for w, _ in ws], st, unit), e)

    its.append(solve_story("A movie ticket and a snack cost $15.25 together. The snack costs $4.50. How much does the ticket cost?",
                           "add", F("4.50"), F("15.25"), "$", "$", "t"))
    n, he, his = P.next()
    its.append(solve_story("%s’s mother is 41 years old. She is 29 years older than %s. How old is %s?" % (n, n, n),
                           "add", 29, 41, "d", ("year old", "years old"), "a"))
    n, he, his = P.next()
    its.append(solve_story("A hiking trail is 8.6 km long. %s has hiked 5.75 km so far. How many more kilometers does %s have to hike?" % (n, he),
                           "add", F("5.75"), F("8.6"), "d", ("km", "km"), "k"))
    n, he, his = P.next()
    its.append(solve_story("Each batch of pancakes needs %s cup of milk. %s has 4 cups of milk. How many batches can %s make?" % (fr(2, 3), n, he),
                           "mul", F(2, 3), 4, "f", ("batch", "batches"), "b"))
    its.append(solve_story("5 notebooks cost $8.75. Each notebook costs the same. How much does 1 notebook cost?",
                           "mul", 5, F("8.75"), "$", "$", "n"))
    its.append(solve_story("A car drives at the same speed for 4 hours and goes 210 miles. How many miles per hour does it drive?",
                           "mul", 4, 210, "d", ("mile per hour", "miles per hour"), "s"))
    n, he, his = P.next()
    its.append(solve_story("%s needs 5 %s feet of ribbon. %s has 2 %s feet. How many more feet of ribbon does %s need?"
                           % (n, fr(1, 2), cap(he), fr(3, 4), he), "add", F(11, 4), F(11, 2), "f", ("foot", "feet"), "r"))
    its.append(solve_story("A bag of 6 apples weighs 2.7 pounds. The apples all weigh the same. How much does 1 apple weigh?",
                           "mul", 6, F("2.7"), "d", ("pound", "pounds"), "a"))
    its.append(solve_story("0.75 pound of cheese costs $6. What is the price for 1 pound?",
                           "mul", F("0.75"), 6, "$", "$", "c"))
    n, he, his = P.next()
    its.append(solve_story("%s’s grandfather is 72 years old. He is 6 times as old as %s. How old is %s?" % (n, n, n),
                           "mul", 6, 72, "d", ("year old", "years old"), "a"))
    n, he, his = P.next()
    its.append(solve_story("%s spent $27.40 at the store and has $18.65 left. How much money did %s have before shopping?" % (n, he),
                           "sub", F("27.40"), F("18.65"), "$", "$", "m"))
    n, he, his = P.next()
    its.append(solve_story("A water tank holds 1,500 gallons when full. It has 1,275 gallons in it now. How many more gallons will fill it?",
                           "add", 1275, 1500, "d", ("gallon", "gallons"), "g"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: write an equation and solve", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    assert solution("mul", F(4), F(10)) == F(5, 2) and solution("mul", F(3, 4), F(6)) == 8
    return (
        "<h2>What does it mean to solve an equation?</h2>"
        "<p>An equation says two amounts are equal, like %s + 5 = 12. A <b>solution</b> is a value of %s that makes it true. "
        "To check a number, <b>substitute</b> it for %s: 7 + 5 = 12 is true, so 7 is the solution.</p>" % (X, X, X) +
        "<p>To solve, get %s alone with the <b>inverse operation</b>, and do the same thing to both sides "
        "so they stay equal.</p>" % X +
        table(["The equation", "Undo it by", "Example"], [
            ["%s + p = q" % X, "subtracting p from both sides", "%s + 5 = 12, so %s = 12 − 5 = 7" % (X, X)],
            ["p%s = q" % X, "dividing both sides by p", "4%s = 10, so %s = 10 ÷ 4 = 2.5" % (X, X)],
        ]) +
        "<h2>A balance shows why it works</h2>"
        "<figure class='sn-fig'>" + scale_svg(["x", "5"], ["12"], "x and 5 on the left and 12 on the right") +
        "<figcaption>%s + 5 = 12. Take 5 off both pans and the scale stays level: %s = 7.</figcaption></figure>" % (X, X) +
        "<h2>Solve x + p = q</h2>" +
        ex("Example", "Solve %s + 2.5 = 8.1." % X,
           "2.5 is added to %s, so subtract 2.5 from both sides: %s = 8.1 − 2.5 = 5.6. Check: 5.6 + 2.5 = 8.1." % (X, X), "%s = 5.6" % X) +
        "<h2>Solve px = q</h2>"
        "<p>4%s means 4 × %s. A tape diagram shows 4 equal parts that make 10.</p>" % (X, X) +
        "<figure class='sn-fig'>" + tape_mul(4, F(10), "d") +
        "<figcaption>4%s = 10. Split 10 into 4 equal parts: %s = 10 ÷ 4 = 2.5.</figcaption></figure>" % (X, X) +
        ex("Example", "Solve %s%s = 6." % (fr(3, 4), X),
           "Divide both sides by %s. Dividing by %s is the same as multiplying by %s: %s = 6 × %s = 8. Check: %s × 8 = 6."
           % (fr(3, 4), fr(3, 4), fr(4, 3), X, fr(4, 3), fr(3, 4)), "%s = 8" % X) +
        "<h2>Word problems</h2>"
        "<p>Choose a letter for the unknown. Write an equation that tells the story, solve it, and check the answer in the story.</p>" +
        ex("Example", "5 notebooks cost $8.75. How much does 1 notebook cost?",
           "Let <i>n</i> be the cost of 1 notebook. 5<i>n</i> = 8.75, so <i>n</i> = 8.75 ÷ 5 = 1.75. Check: 5 × $1.75 = $8.75.", "$1.75") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["%s + 5 = 12, so %s = 17" % (X, X), "Do the opposite: subtract 5. %s = 7" % X],
            ["4%s = 2, so %s = 2 (4 ÷ 2)" % (X, X), "Divide the other side by 4: %s = 2 ÷ 4 = %s" % (X, fr(1, 2))],
            ["%s%s = 6, so %s = 4 %s (6 × %s)" % (fr(3, 4), X, X, fr(1, 2), fr(3, 4)), "Divide by %s: 6 × %s = 8" % (fr(3, 4), fr(4, 3))],
            ["0.5%s = 4.5, so %s = 2.25" % (X, X), "Divide by 0.5: %s = 9. Dividing by a number less than 1 makes it bigger" % X],
            ["“5 times the cost” written as %s + 5" % X, "“Times” means multiply: 5%s" % X],
            ["Not checking", "Substitute the answer back into the equation"],
        ])
    )


FAQ = [
    {"q": "How do you solve a one-step equation?",
     "a": "Use the inverse operation to get the variable alone, and do it to both sides. Subtract to undo adding (x + 5 = 12, so x = 7), and divide to undo multiplying (4x = 10, so x = 2.5)."},
    {"q": "How do you check if a number is a solution of an equation?",
     "a": "Substitute the number for the variable and see if both sides are equal. 7 is a solution of x + 5 = 12 because 7 + 5 = 12."},
    {"q": "How do you solve an equation with a fraction, like 3/4 x = 6?",
     "a": "Divide both sides by 3/4, which is the same as multiplying by its reciprocal, 4/3. 6 × 4/3 = 8, so x = 8."},
    {"q": "What one-step equations do 6th graders learn?",
     "a": "In Grade 6 (Common Core 6.EE.B.7), students solve equations like x + p = q and px = q with whole numbers, decimals and fractions, and write them for word problems."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(609)
    P = People(rnd)
    sets = [set_substitute(rnd, P), set_add(rnd, P), set_mul(rnd, P), set_models(rnd, P), set_words(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "\\" not in it["q"] + "".join(it["c"]) + it["e"]
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "one-step-equations", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "One-Step Equations: x + p = q and px = q",
        "seo_title": "Grade 6 One-Step Equations Worksheets: Solve x + p = q and px = q with Decimals and Fractions",
        "short_title": "One-step equations",
        "domain": "Expressions and Equations",
        "standard_code": "6.EE.B.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/EE/B/7/",
        "standard_text": "Solve real-world and mathematical problems by writing and solving equations of the form x + p = q and px = q for cases in which p, q and x are all nonnegative rational numbers.",
        "meta_desc": "Free Grade 6 one-step equations worksheets: check solutions by substituting, solve x + p = q and px = q with whole numbers, decimals and fractions, use tape diagrams and balances, and write equations for word problems. 100 practice questions with an answer key.",
        "key_big": "Undo the operation, and do the same to both sides: subtract to undo adding, divide to undo multiplying.",
        "key_sub": "x + 5 = 12, so x = 12 − 5 = 7 (not 17). 4x = 10, so x = 10 ÷ 4 = 2.5. Check by substituting: 4 × 2.5 = 10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(tape diagram|pan balance)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
