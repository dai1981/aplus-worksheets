# -*- coding: utf-8 -*-
"""
British Columbia Grade 9 Math: Multi-Step Linear Equations
(BC Mathematics Curriculum, Mathematics 9 — Patterning: multi-step one-variable linear equations)
  python3 tools/gen_cabc_math_g9_linear_equations.py
Two-step review with integers, variables on both sides (pan balances), brackets (the distributive
property, including negative multipliers and subtracted brackets), equations with fractions (clear them
with the LCD) and decimals, and word problems in BC contexts (phone plans, community centre and gym
memberships, a climbing gym in Squamish, a ski hill near Kelowna, a Science World field trip).
Wrong choices come from real mistakes: multiplying only the first term inside the brackets, sign errors
with a negative multiplier or a subtracted bracket, adding the x-terms instead of subtracting them,
using the same operation instead of the inverse, multiplying only some terms by the LCD, and stopping
one step early. Every answer is solved and checked in code with fractions.Fraction.
HTML attributes use single quotes. Canadian English. Real minus sign −.
"""
import json, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-9")
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
    return "(%s)" % num(v) if F(v) < 0 else num(v)


def money(v):
    v = F(v)
    assert v > 0 and (v * 100).denominator == 1, v
    if v.denominator == 1:
        return "$" + num(v)
    return "$%d.%02d" % (int(v), int((v - int(v)) * 100))


def lcm(a, b):
    return a * b // gcd(a, b)


# ------------------------------------------------------------ equations in a mini syntax
# "3x + 8 = -7", "5x + 3 = 2x + 18", "3(x-2) = 15", "5 - 2(x-3) = 1", "2(3x+1) = 4x", "0.4x + 1.2 = 3.6",
# "x/2 + x/3 = 10", "2x/3 = 8", "(x+4)/3 = 5". Tokens are separated by spaces; only the first token of a
# side may carry a minus sign.
TERM = re.compile(r"^(-?)(\d*\.?\d*)([a-z])$")
DIVT = re.compile(r"^(-?)([a-z])/(\d+)$")
FRT = re.compile(r"^(-?)(\d+)([a-z])/(\d+)$")
BDIV = re.compile(r"^(-?)\(([a-z])([+-])(\d+)\)/(\d+)$")
NUMT = re.compile(r"^-?\d+(\.\d+)?$")
BRK = re.compile(r"^(-?)(\d*\.?\d*)\((\d*)([a-z])([+-])(\d+(?:\.\d+)?)\)$")


def V(v):
    return "<i>%s</i>" % v


def frac(top, bot):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (top, bot)


def split(s):
    a, b = s.split(" = ")
    return a, "=", b


def tok_val(tok, sign=1, mode=None):
    """-> (coefficient, constant) of one token, before its sign is applied.
    mode 'one': brackets multiply only their first term; 'sign': with a negative multiplier the
    constant keeps the wrong sign; 'lcd:L': only fraction terms are multiplied by L."""
    m, d, f, bd, b = TERM.match(tok), DIVT.match(tok), FRT.match(tok), BDIV.match(tok), BRK.match(tok)
    L = int(mode[4:]) if mode and mode.startswith("lcd:") else None
    if bd:
        n = int(bd.group(5))
        c = F(bd.group(4)) * (1 if bd.group(3) == "+" else -1)
        a, k = F(1, n), c / n
        if mode == "one":
            k = c
        if bd.group(1):
            a, k = -a, -k
        return (a * L, k * L) if L else (a, k)
    if f:
        a = F(int(f.group(2)), int(f.group(4)))
        a = -a if f.group(1) else a
        return (a * L, F(0)) if L else (a, F(0))
    if d:
        a = F(1, int(d.group(3)))
        a = -a if d.group(1) else a
        return (a * L, F(0)) if L else (a, F(0))
    if m:
        a = F(m.group(2)) if m.group(2) else F(1)
        return (-a if m.group(1) else a), F(0)
    if b:
        k = F(b.group(2)) if b.group(2) else F(1)
        k = -k if b.group(1) else k
        inner = F(b.group(3)) if b.group(3) else F(1)
        c = F(b.group(6)) * (1 if b.group(5) == "+" else -1)
        if mode == "one":
            return k * inner, c
        if mode == "sign" and sign * k < 0:
            return k * inner, -k * c
        return k * inner, k * c
    if NUMT.match(tok):
        return F(0), F(tok)
    raise ValueError(tok)


def side(t, mode=None):
    A, B, sign = F(0), F(0), 1
    for tok in t.split(" "):
        if tok in ("+", "-"):
            sign = 1 if tok == "+" else -1
            continue
        a, b = tok_val(tok, sign, mode)
        A += sign * a
        B += sign * b
    return A, B


def parts(s, mode=None):
    a, r, b = split(s)
    A1, B1 = side(a, mode)
    A2, B2 = side(b, mode)
    return A1, B1, r, A2, B2


def solve(s, mode=None):
    A1, B1, r, A2, B2 = parts(s, mode)
    if A1 == A2:
        return None
    return (B2 - B1) / (A1 - A2)


def holds(s, x):
    A1, B1, r, A2, B2 = parts(s)
    return A1 * x + B1 == A2 * x + B2


def var_of(s):
    return re.search(r"[a-z]", s).group(0)


def R(s):
    """render the mini syntax as HTML"""
    out = []
    for tok in s.split(" "):
        m, d, f, bd, b = TERM.match(tok), DIVT.match(tok), FRT.match(tok), BDIV.match(tok), BRK.match(tok)
        if bd:
            out.append((M if bd.group(1) else "") + frac("%s %s %s" % (V(bd.group(2)), "+" if bd.group(3) == "+" else M,
                                                                          bd.group(4)), bd.group(5)))
        elif f:
            out.append((M if f.group(1) else "") + frac(f.group(2) + V(f.group(3)), f.group(4)))
        elif d:
            out.append((M if d.group(1) else "") + frac(V(d.group(2)), d.group(3)))
        elif m:
            out.append((M if m.group(1) else "") + m.group(2) + V(m.group(3)))
        elif b:
            out.append("%s%s(%s%s %s %s)" % (M if b.group(1) else "", b.group(2), b.group(3), V(b.group(4)),
                                             "+" if b.group(5) == "+" else M, b.group(6)))
        elif NUMT.match(tok):
            out.append(num(F(tok)))
        else:
            out.append({"-": M}.get(tok, tok))
    return " ".join(out)


FRAC = [False]


def is_div(s):
    return bool(re.search(r"[a-z]/\d", s))


def needs_lcd(s):
    return bool(re.search(r"\d[a-z]/\d", s) or re.search(r"\)/\d", s) or len(re.findall(r"/\d", s)) >= 2)


def T(a, v):
    a = F(a)
    if a == 1:
        return V(v)
    if a == -1:
        return M + V(v)
    if FRAC[0] and abs(a.numerator) == 1 and a.denominator > 1:
        return (M if a < 0 else "") + frac(V(v), a.denominator)
    return num(a) + V(v)


def lin(A, B, v):
    if A == 0:
        return num(B)
    if B == 0:
        return T(A, v)
    return "%s %s %s" % (T(A, v), "+" if B > 0 else M, num(abs(B)))


def mini(A, B, v):
    """A·v + B in the mini syntax"""
    A, B = F(A), F(B)
    out = ""
    if A != 0:
        out = ("" if A == 1 else "-" if A == -1 else num(A).replace(M, "-")) + v
    if B != 0:
        if out:
            out += (" + " if B > 0 else " - ") + num(abs(B))
        else:
            out = num(B).replace(M, "-")
    return out or "0"


def ntoks(t):
    toks = [x for x in t.split(" ") if x not in ("+", "-")]
    return (len([x for x in toks if TERM.match(x) or DIVT.match(x) or BRK.match(x)]),
            len([x for x in toks if NUMT.match(x)]), any(BRK.match(x) for x in toks))


# ------------------------------------------------------------ solving steps and checks
def sub_tok(tok, x, first):
    m, d, f, bd, b = TERM.match(tok), DIVT.match(tok), FRT.match(tok), BDIV.match(tok), BRK.match(tok)
    if bd:
        return "%s(%s %s %s) ÷ %s" % (M if bd.group(1) else "", num(x), "+" if bd.group(3) == "+" else M,
                                       bd.group(4), bd.group(5))
    if f:
        return "%s%s × %s ÷ %s" % (M if f.group(1) else "", f.group(2), par(x), f.group(4))
    if d:
        return "%s%s ÷ %s" % (M if d.group(1) else "", par(x), d.group(3))
    if m:
        neg = M if m.group(1) else ""
        if m.group(2):
            return "%s%s × %s" % (neg, m.group(2), par(x))
        if neg or not first:
            return neg + par(x)
        return num(x)
    if b:
        inner = ("%s × %s" % (b.group(3), par(x))) if b.group(3) else num(x)
        return "%s%s(%s %s %s)" % (M if b.group(1) else "", b.group(2), inner,
                                   "+" if b.group(5) == "+" else M, b.group(6))
    return num(F(tok))


def sub_side(t, x):
    out = []
    for tok in t.split(" "):
        if tok in ("+", "-"):
            out.append({"-": M}.get(tok, tok))
        else:
            out.append(sub_tok(tok, x, not out))
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


def expansions(t, v):
    """'3(x − 2) = 3x − 6' for each bracket of one side; a minus in front belongs to the multiplier"""
    out, sign = [], 1
    for tok in t.split(" "):
        if tok in ("+", "-"):
            sign = 1 if tok == "+" else -1
            continue
        if BRK.match(tok):
            a, b = tok_val(tok, sign)
            shown = (M + R(tok)) if sign < 0 else R(tok)
            out.append("%s = %s" % (shown, lin(sign * a, sign * b, v)))
    return out


def steps(s, check=True):
    """Step-by-step explanation for an equation. Returns (text, x)."""
    v = var_of(s)
    if needs_lcd(s):
        return lcd_steps(s)
    FRAC[0] = is_div(s)
    a, r, b = split(s)
    A1, B1 = side(a)
    A2, B2 = side(b)
    out = []
    ta, ca, ba = ntoks(a)
    tb, cb, bb = ntoks(b)
    if ba or bb:
        exps = expansions(a, v) + expansions(b, v)
        out.append("Expand the brackets (multiply <b>both</b> terms inside): %s." % "; ".join(exps))
    if ta + ca > 2 or tb + cb > 2 or ba or bb:
        out.append("Simplify each side: %s = %s." % (lin(A1, B1, v), lin(A2, B2, v)))
    left, Ao, Bv, Bo = orient(s)
    if A1 != 0 and A2 != 0:
        mv = A2 if left else A1
        how = ("Subtract %s from both sides" % T(mv, v)) if mv > 0 else ("Add %s to both sides" % T(-mv, v))
        if left:
            out.append("%s: %s = %s." % (how, lin(Ao, Bv, v), num(Bo)))
        else:
            out.append("%s: %s = %s." % (how, num(Bo), lin(Ao, Bv, v)))
    Co = Bo - Bv
    if Bv != 0:
        how = ("Subtract %s from both sides" % num(Bv)) if Bv > 0 else ("Add %s to both sides" % num(-Bv))
        if left:
            out.append("%s: %s = %s." % (how, T(Ao, v), num(Co)))
        else:
            out.append("%s: %s = %s." % (how, num(Co), T(Ao, v)))
    x = Co / Ao
    if Ao != 1:
        if FRAC[0] and Ao.numerator == 1 and Ao.denominator > 1:
            how = "Multiply both sides by %d: %s × %d = %s" % (Ao.denominator, par(Co), Ao.denominator, num(x))
        elif FRAC[0] and Ao.numerator == -1 and Ao.denominator > 1:
            how = "Multiply both sides by %s: %s × %s = %s" % (num(-Ao.denominator), par(Co), par(-Ao.denominator), num(x))
        else:
            how = "Divide both sides by %s: %s ÷ %s = %s" % (num(Ao), par(Co), par(Ao), num(x))
        out.append(how + ".")
    if left and Ao == 1 and out:
        out[-1] = out[-1][:-1].replace("%s = %s" % (V(v), num(x)), "<b>%s = %s</b>" % (V(v), num(x))) + "."
    else:
        out.append("So <b>%s = %s</b>." % (V(v), num(x)))
    assert holds(s, x), s
    if check:
        out.append(check_text(s, x) + ".")
    FRAC[0] = False
    return " ".join(out), x


def lcd_of(s):
    L = 1
    for d in re.findall(r"/(\d+)", s):
        L = lcm(L, int(d))
    return L


def tok_html(tok):
    return R(tok)


def lcd_steps(s):
    v = var_of(s)
    L = lcd_of(s)
    a, r, b = split(s)
    prods = []
    for t in (a, b):
        for tok in t.split(" "):
            if tok in ("+", "-"):
                continue
            ca, cb = tok_val(tok.lstrip("-") if not BRK.match(tok) else tok)
            prods.append("%d × %s = %s" % (L, R(tok.lstrip("-")), lin(L * ca, L * cb, v)))
    A1, B1 = side(a)
    A2, B2 = side(b)
    ieq = "%s = %s" % (mini(L * A1, L * B1, v), mini(L * A2, L * B2, v))
    dens = sorted(set(int(d) for d in re.findall(r"/(\d+)", s)))
    why = ("the LCD of %s" % " and ".join(str(d) for d in dens)) if len(dens) > 1 else "the denominator"
    out = ["Multiply <b>every</b> term on both sides by %d (%s): %s. So %s." % (L, why, "; ".join(prods), R(ieq))]
    e, x = steps(ieq, check=False)
    out.append(e)
    assert holds(s, x), s
    out.append(check_text(s, x) + ".")
    return " ".join(out), x


def int_eq(s):
    v = var_of(s)
    L = lcd_of(s)
    A1, B1, r, A2, B2 = parts(s)
    return "%s = %s" % (mini(L * A1, L * B1, v), mini(L * A2, L * B2, v))


def eq_wrongs(s, extra=None):
    """Answers from real mistakes for an equation, most common first. -> [(value, why)]"""
    v = var_of(s)
    out = list(extra or [])
    if needs_lcd(s):
        L = lcd_of(s)
        w = solve(s, "lcd:%d" % L)
        if w is not None:
            out.append((w, "multiplying only the fractions by %d, not the whole numbers" % L))
        if BDIV.search(s.replace(" = ", " ").split(" ")[0]) or re.search(r"\)/\d", s):
            w = solve(s, "one")
            if w is not None:
                out.append((w, "dividing only %s by the denominator, not the whole top" % v))
        return out + eq_wrongs(int_eq(s))
    if "(" in s:
        w = solve(s, "one")
        if w is not None:
            out.append((w, "multiplying only the first term inside the brackets"))
        w = solve(s, "sign")
        if w is not None:
            out.append((w, "a sign error when expanding with a negative multiplier"))
    A1, B1, r, A2, B2 = parts(s)
    left, Ao, Bv, Bo = orient(s)
    x = (Bo - Bv) / Ao
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
    elif abs(Ao) != 1:
        out.append((Bo - Bv, "forgetting to divide by %s" % num(Ao)))
        if Bv != 0 and (A2 == 0 or A1 == 0) and "(" not in s:
            out.append((Bo / Ao - Bv, "dividing by %s before dealing with the %s" % (num(Ao), num(Bv))))
    out.append((x + 1, None))
    out.append((x - 1, None))
    out.append((x + 2, None))
    return out


# ------------------------------------------------------------ question helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
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
    x = F(x)
    used, add = {x}, []
    for c in cands:
        val, why = c if isinstance(c, tuple) else (c, None)
        if val is None:
            continue
        val = F(val)
        if val in used or val == 0 or (val < 0 and not neg):
            continue
        if whole and val.denominator != 1:
            continue
        if not whole and (val * 100).denominator != 1:
            continue
        if unit == "$" and val < 0:
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
    e, x = steps(s)
    w = eq_wrongs(s, extra)
    if not whole:
        w = w[:-3] + [(x * 10, "misplacing the decimal point"), (x / 10, "misplacing the decimal point")] + w[-3:]
    return mcq_n(q or ("Solve: %s" % R(s)), x, w, e, whole=whole)


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("keep"):
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


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, col=INK, italic=False, bold=False, anchor="middle"):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-style='italic'" if italic else "", " font-weight='700'" if bold else "", col, anchor, t))


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


def flow_svg(start, ops, end):
    """Number machine: start -> op -> op -> end."""
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
    labels = [start] + ops + [end]
    y = 8
    for i, (bx, w, t) in enumerate(zip(xs, widths, labels)):
        fill = FILL if i in (0, len(widths) - 1) else "#fff"
        col = RED if i == 0 else INK
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (bx, y, w, h, 6 if 0 < i < len(widths) - 1 else 2, fill, GREEN))
        s.append(text(bx + w / 2, y + 26, t, 18, col=col, italic=(i == 0 and t.isalpha()), bold=True))
    for i in range(len(widths) - 1):
        x1, x2 = xs[i] + widths[i] + 4, xs[i + 1] - 4
        ym = y + h / 2
        s.append("<path d='M%d %.1f H%d' stroke='%s' stroke-width='2.5'/>" % (x1, ym, x2 - 8, INK))
        s.append("<path d='M%d %.1f l-9 -6 v12 Z' fill='%s'/>" % (x2, ym, INK))
    lab = "number machine: %s, %s, gives %s" % (start, ", then ".join(ops), end)
    return svg_wrap(W, y + h + 8, "".join(s), lab)


CW = {"(": 0.333, ")": 0.333, " ": 0.278, "+": 0.584, M: 0.584, "=": 0.584, "x": 0.5}


def swidth(t, fs):
    return sum(CW.get(ch, 0.556) for ch in t) * fs


def dist_svg(k, a, op, c, rk, rop, rc):
    """k(a op c) with an arrow from k to each term inside, and the expanded result rk·a rop rc below."""
    fs = 26
    x0, base = 16.0, 92
    pieces = [(k, INK, False, True), ("(", INK, False, False), (a, RED, True, False), (" " + op + " ", INK, False, False),
              (c, INK, False, False), (")", INK, False, False)]
    pos, x = [], x0
    for t, col, it, bold in pieces:
        w = swidth(t, fs) * (1.08 if bold else 1)
        pos.append((x, w))
        x += w
    s = []
    for (px, w), (t, col, it, bold) in zip(pos, pieces):
        if t.strip():
            s.append(text(px + w / 2, base, t.strip(), fs, col=col, italic=it, bold=bold))
    kx = pos[0][0] + pos[0][1] / 2
    for idx, top in ((2, 34), (4, 12)):
        tx = pos[idx][0] + pos[idx][1] / 2
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (kx, base - 26, (kx + tx) / 2, top, tx, base - 32, GREEN))
        s.append("<path d='M%.1f %d l-6 -10 h12 Z' fill='%s'/>" % (tx, base - 22, GREEN))
    res = ("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s'>= %s<tspan font-style='italic' fill='%s'>%s</tspan>"
           " %s %s</text>" % (x0, base + 42, fs, INK, rk, RED, a, rop, rc))
    s.append(res)
    W = max(x, x0 + swidth("= " + rk + a + " " + rop + " " + rc, fs) * 1.08) + 16
    return svg_wrap(W, base + 54, "".join(s), "distributing %s to both terms in the brackets" % k)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def keep(it, choices, a):
    assert it["c"][0] == choices[a] and sorted(it["c"]) == sorted(choices)
    it["c"], it["a"], it["keep"] = list(choices), a, True
    return it


X = V("x")
STEPS4 = ["Step 1", "Step 2", "Both steps", "There is no mistake"]


def mistake_item(P, s, st1, st2, ans, e):
    nm, he, his = P.next()
    q = ("%s solved %s:<br>Step 1: %s<br>Step 2: %s<br>Which step has a mistake?" % (nm, R(s), st1, st2))
    it = mcq(q, STEPS4[ans], [c for c in STEPS4 if c != STEPS4[ans]], e)
    return keep(it, STEPS4, ans)


# ============================================================ set 1: two-step review
def set_review(P):
    its = []
    s = "3x - 7 = -19"
    x = solve(s)
    its.append(mcq_n(fig(flow_svg("x", ["× 3", M + " 7"], M + "19")) + "A number %s goes through this machine and comes out "
                     "as %s19. What is %s?" % (X, M, X), x, eq_wrongs(s),
                     "Undo in reverse order: %s19 + 7 = %s12, then %s12 ÷ 3 = %s4. Check: 3 × (%s4) − 7 = %s12 − 7 = %s19 ✓."
                     % ((M,) * 7)))
    its.append(mcq("What is the best first step to solve %s?" % R("4x - 9 = 23"),
                   "Add 9 to both sides",
                   ["Subtract 9 from both sides", "Divide both sides by 4", "Add 9 to the left side only"],
                   "4%s − 9 means “multiply by 4, then subtract 9.” Undo the last step first: add 9 to both sides, "
                   "so 4%s = 32. Then divide by 4: %s = 8. Whatever you do to one side, do to the other side too."
                   % (X, X, X)))
    its.append(mcq("You subtract 5 from both sides of %s. Which equation do you get?" % R("-6x + 5 = 29"),
                   R("-6x = 24"), [R("-6x = 34"), R("6x = 24"), R("-x = 24")],
                   "29 − 5 = 24, and %s6%s stays the same, so %s. Then divide by %s6: %s = %s4. "
                   "Check: %s6 × (%s4) + 5 = 24 + 5 = 29 ✓." % (M, X, R("-6x = 24"), M, X, M, M, M)))
    for s in ["5x + 8 = 43", "2x - 13 = -5", "-3x + 4 = 25", "x/4 + 6 = 1", "7 - 2x = 19", "6x + 15 = -21",
              "-5x - 8 = 27", "x/3 - 7 = -2", "9x - 4 = 50", "-28 = 4x + 8", "12 - 5x = -18", "-x/2 + 3 = 8",
              "8x + 11 = -29", "-7x - 6 = -48", "15 = 3 - 4x", "x/6 + 9 = 4", "-9x + 14 = -40"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Two-step equations review", "items": its}


# ============================================================ set 2: variables on both sides
def set_both(P):
    its = []
    for left, right, s in [(["x"] * 5 + ["3"], ["x", "x", "18"], "5x + 3 = 2x + 18"),
                           (["x"] * 4 + ["2"], ["x", "17"], "4x + 2 = x + 17")]:
        x = solve(s)
        A1, B1, _, A2, B2 = parts(s)
        e = ("The balance shows %s. Take %s off both pans: %s = %s. Take %s off both pans: %s = %s. "
             "Share %s among the %s blocks: %s = %s. %s."
             % (R(s), ("%d blocks" % A2) if A2 != 1 else "one block", lin(A1 - A2, B1, "x"), num(B2), num(B1),
                T(A1 - A2, "x"), num(B2 - B1), num(B2 - B1), num(A1 - A2), X, num(x), check_text(s, x)))
        svg = scale_svg(left, right, R(s).replace("<i>", "").replace("</i>", ""))
        its.append(mcq_n(fig(svg) + "The pan balance is level. Each block has the same mass, %s. What is %s?" % (X, X),
                         x, eq_wrongs(s), e, neg=False))
    its.append(mcq("Which step gets the %s-terms on one side of %s?" % (X, R("7x + 4 = 3x + 24")),
                   "Subtract 3%s from both sides" % X,
                   ["Add 3%s to both sides" % X, "Subtract 3%s from the right side only" % X, "Divide both sides by 3%s" % X],
                   "Subtracting 3%s from both sides keeps the equation balanced and leaves %s on one side only: "
                   "4%s + 4 = 24. Then 4%s = 20 and %s = 5. Check: 7 × 5 + 4 = 39 and 3 × 5 + 24 = 39 ✓." % (X, X, X, X, X)))
    its.append(mcq("You subtract 2%s from both sides of %s. Which equation do you get?" % (X, R("6x - 5 = 2x + 11")),
                   R("4x - 5 = 11"), [R("8x - 5 = 11"), R("4x - 5 = 2x + 11"), R("4x + 5 = 11")],
                   "6%s − 2%s = 4%s and 2%s − 2%s = 0, so %s. Subtracting from only one side breaks the balance; "
                   "adding gives 8%s. Next: 4%s = 16, so %s = 4." % (X, X, X, X, X, R("4x - 5 = 11"), X, X, X)))
    for s in ["7x - 4 = 3x + 20", "9x + 2 = 4x - 23", "6x - 7 = 2x - 31", "-3x + 8 = x - 12", "2x - 9 = 5x + 6",
              "12 - x = 2x + 3", "4 - 2x = 3x - 21", "8x + 5 = 3x - 25", "3x + 5 - x = 4x - 7", "10x - 3 = 4x + 27",
              "-5x + 6 = -2x - 15", "5x + 4 = 9x", "x + 18 = -2x", "2x + 7 + 3x = x - 13", "11 - 4x = -x - 10",
              "6x - 8 = -2x + 24"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Variables on both sides", "items": its}


# ============================================================ set 3: brackets
def set_brackets(P):
    its = []
    its.append(mcq("Expand %s." % R("3(x-4)"), lin(3, -12, "x"),
                   [lin(3, -4, "x"), lin(3, 12, "x"), lin(1, -12, "x")],
                   "Multiply <b>both</b> terms inside the brackets by 3: 3 × %s = 3%s and 3 × (%s4) = %s12. "
                   "3%s − 4 comes from multiplying only the first term." % (X, X, M, M, X)))
    its.append(mcq("Expand %s." % R("-2(x-5)"), lin(-2, 10, "x"),
                   [lin(-2, -10, "x"), lin(-2, -5, "x"), lin(2, -10, "x")],
                   "Multiply both terms by %s2: %s2 × %s = %s2%s and %s2 × (%s5) = +10. A negative times a negative "
                   "is positive, so the answer is %s. %s comes from a sign error."
                   % (M, M, X, M, X, M, M, lin(-2, 10, "x"), lin(-2, -10, "x"))))
    its.append(mcq("Which is the same as %s?" % R("9 - (x-4)"), lin(-1, 13, "x"),
                   [lin(-1, 5, "x"), lin(1, 5, "x"), lin(-1, -13, "x")],
                   "The minus in front of the brackets multiplies <b>both</b> terms by %s1: %s(%s %s 4) = %s%s + 4. "
                   "So 9 %s %s + 4 = 13 %s %s, which is %s. %s comes from changing only the sign of %s."
                   % (M, M, X, M, M, X, M, X, M, X, lin(-1, 13, "x"), lin(-1, 5, "x"), X)))
    for s in ["3(x-2) = 15", "4(x+5) = 8", "-2(x-3) = 14", "5(x+1) = 3x + 17", "2(x-4) = 4x + 6",
              "6(x-1) - 2x = 18", "5 - 2(x-3) = 1", "2(x+3) = 3(x-1)", "4(x-2) - (x+1) = 9", "-3(x+2) = 2(x-8)",
              "7 - 3(x+1) = -8", "2(3x-1) = 4(x+2)", "5(x-2) - 3(x-4) = 10", "8 = -2(x+1)", "3(x-5) + 4 = x - 1"]:
        its.append(solve_item(s))
    its.append(mistake_item(P, "4(x+3) = 32", R("4x + 3 = 32"), "4%s = 29, so %s = 7.25" % (X, X), 0,
                            "Step 1 multiplies only %s by 4. Both terms must be multiplied: 4%s + 12 = 32. "
                            "Then 4%s = 20, so %s = 5. Check: 4(5 + 3) = 4 × 8 = 32 ✓." % (X, X, X, X)))
    its.append(mistake_item(P, "-3(x-2) = 21", R("-3x + 6 = 21"), "%s3%s = 15, so %s = %s5" % (M, X, X, M), 3,
                            "Step 1: %s3 × %s = %s3%s and %s3 × (%s2) = +6. Step 2: subtract 6, then divide by %s3. "
                            "Both steps are right. Check: %s3(%s5 %s 2) = %s3 × (%s7) = 21 ✓."
                            % (M, X, M, X, M, M, M, M, M, M, M, M)))
    assert solve("4(x+3) = 32") == 5 and solve("-3(x-2) = 21") == -5
    assert len(its) == 20, len(its)
    return {"title": "Equations with brackets", "items": its}


# ============================================================ set 4: fractions and decimals
def set_fracdec(P):
    its = []
    its.append(mcq("Multiply every term of %s by 10. Which equation do you get?" % R("0.3x + 1.2 = 2.7"),
                   R("3x + 12 = 27"), [R("3x + 1.2 = 27"), R("3x + 12 = 2.7"), R("30x + 12 = 27")],
                   "10 × 0.3%s = 3%s, 10 × 1.2 = 12 and 10 × 2.7 = 27. Every term must be multiplied. "
                   "Then 3%s = 15, so %s = 5. Check: 0.3 × 5 + 1.2 = 2.7 ✓." % (X, X, X, X)))
    its.append(mcq("What is the best number to multiply every term of %s by to clear the fractions?" % R("x/4 + x/6 = 5"),
                   "12", ["24", "10", "4"],
                   "Use the lowest common denominator (LCD) of 4 and 6, which is 12. 12 × %s = 3%s and 12 × %s = 2%s, "
                   "so 3%s + 2%s = 60 and %s = 12. 24 also works but gives bigger numbers; 10 (4 + 6) does not clear "
                   "both fractions." % (R("x/4"), X, R("x/6"), X, X, X, X)))
    for s in ["0.4x + 1.2 = 3.6", "1.5x - 2 = 0.5x + 3", "0.2x + 3.5 = 4.7", "2.5x - 1.5 = 6", "1.2x + 0.8 = 0.4x + 4",
              "0.6(x-5) = 1.8", "3.2 - 0.4x = 1.6", "0.25x + 1.5 = 0.75x - 2.5", "2x + 1.3 = 6.1"]:
        its.append(solve_item(s, whole=False))
    for s in ["x/2 + x/3 = 10", "2x/3 = 8", "3x/4 - 2 = 7", "(x+4)/3 = 5", "(x-2)/5 = 3", "x/3 - 1 = x/4 + 1",
              "(x+1)/2 = (x+7)/4", "2x/5 + 1 = 7", "x/2 - 3 = x/5"]:
        its.append(solve_item(s))
    assert len(its) == 20, len(its)
    return {"title": "Equations with fractions and decimals", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    U = lambda a, b: (a, b)

    def word(q, s, extra, intro, unit=None, after="", whole=True):
        e, x = steps(s)
        cands = list(extra) + eq_wrongs(s)
        return mcq_n(q, x, cands, "%s: %s. %s%s" % (intro, R(s), e, after), unit=unit, neg=False, whole=whole)

    its.append(word("Phone plan A costs $30 a month plus $5 for each GB of data. Plan B costs $45 a month plus $2 for each GB. "
                    "For how many GB do the two plans cost the same?", "30 + 5g = 45 + 2g",
                    [(15, "forgetting to divide by 3")],
                    "Let %s be the number of GB. Set the two costs equal" % V("g"), U("GB", "GB"),
                    " Both plans cost $55."))
    its.append(word("Phone A costs $300 up front plus $40 a month. Phone B costs nothing up front but $65 a month. "
                    "After how many months is the total cost the same?", "300 + 40m = 65m",
                    [(25, "giving the difference in the monthly cost, $65 − $40")],
                    "Let %s be the number of months" % V("m"), U("month", "months"), " Both phones cost $780."))
    its.append(word("A community centre in Surrey charges $8 for each drop-in swim. A membership costs $40 plus $3 a swim. "
                    "For how many swims do both options cost the same?", "40 + 3v = 8v",
                    [(5, "dividing 40 by 8 and ignoring the $3 a swim")],
                    "Let %s be the number of swims" % V("v"), U("swim", "swims"), " Both cost $64."))
    its.append(word("A climbing gym in Squamish charges $15 a visit, or $90 for a membership plus $6 a visit. "
                    "For how many visits do both options cost the same?", "15v = 90 + 6v",
                    [(6, "dividing 90 by 15 and ignoring the $6 a visit")],
                    "Let %s be the number of visits" % V("v"), U("visit", "visits"), " Both cost $150."))
    its.append(word("Gym A charges a $60 sign-up fee plus $25 a month. Gym B charges $40 a month and no sign-up fee. "
                    "After how many months is the total cost the same?", "60 + 25m = 40m",
                    [(15, "giving the difference in the monthly cost, $40 − $25")],
                    "Let %s be the number of months" % V("m"), U("month", "months"), " Both cost $160."))
    n, he, his = P.next()
    its.append(mcq("Phone plan A costs $25 a month plus $4 for each GB of data. Plan B costs $40 a month plus $1 for each GB. "
                   "Which equation finds the number of GB, %s, when the plans cost the same?" % V("g"),
                   R("25 + 4g = 40 + g"), [R("25g + 4 = 40g + 1"), R("25 + 4g + 40 + g = 0"), R("4g - 25 = g - 40")],
                   "Each plan costs its monthly fee plus its price per GB times %s: 25 + 4%s and 40 + %s. Set them equal. "
                   "Solve: 3%s = 15, so %s = 5 GB. Check: 25 + 20 = 45 and 40 + 5 = 45 ✓."
                   % (V("g"), V("g"), V("g"), V("g"), V("g"))))
    assert solve("25 + 4g = 40 + g") == 5
    its.append(word("A ski hill near Kelowna sells day tickets for $85. A season pass costs $480 plus $25 for each day. "
                    "After how many days does the season pass cost the same as day tickets?", "85d = 480 + 25d",
                    [(60, "giving the difference in the daily cost, $85 − $25")],
                    "Let %s be the number of days" % V("d"), U("day", "days"), " Both cost $680."))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(word("%s has $150 saved and adds $20 each week. %s has $310 and spends $20 each week. "
                    "After how many weeks will they have the same amount?" % (n1, n2), "150 + 20w = 310 - 20w",
                    [(8, "using 20%s − 20%s = 0 instead of adding: 160 ÷ 20" % (V("w"), V("w")))],
                    "Let %s be the number of weeks" % V("w"), U("week", "weeks"), " They both have $230."))
    its.append(word("Tank A holds 500 L of water and drains 15 L a minute. Tank B holds 200 L and fills 10 L a minute. "
                    "After how many minutes do the tanks hold the same amount?", "500 - 15t = 200 + 10t",
                    [(60, "subtracting 10%s instead of adding 15%s (300 ÷ 5)" % (V("t"), V("t")))],
                    "Let %s be the number of minutes" % V("t"), U("minute", "minutes"), " Both tanks hold 320 L."))
    its.append(word("For a fundraiser, a Grade 9 class pays $120 to set up a T-shirt printer plus $4 for each shirt. "
                    "They sell each shirt for $10. How many shirts must they sell to break even?", "10s = 120 + 4s",
                    [(12, "dividing 120 by 10 and ignoring the $4 cost"), (30, "dividing 120 by 4")],
                    "Let %s be the number of shirts. Break even means money in = money out" % V("s"),
                    U("shirt", "shirts")))
    n, he, his = P.next()
    its.append(word("%s is choosing a summer job in the Okanagan. Job A pays $18 an hour. Job B pays $16 an hour plus a "
                    "$40 bonus each week. For how many hours a week do the jobs pay the same?" % n, "18h = 16h + 40",
                    [(F(40, 34), None), (40, "forgetting to divide by 2")],
                    "Let %s be the number of hours" % V("h"), U("hour", "hours"), " Both jobs pay $360."))
    its.append(word("The sum of three consecutive whole numbers is 141. What is the smallest number?", "n + n + 1 + n + 2 = 141",
                    [(47, "giving the middle number"), (48, "giving the largest number"), (F(141, 3) - 1, None)],
                    "Let %s be the smallest number. The numbers are %s, %s + 1 and %s + 2" % (V("n"), V("n"), V("n"), V("n")),
                    None, " The numbers are 46, 47 and 48."))
    its.append(word("A rectangular garden is 3 m longer than twice its width. Its perimeter is 54 m. How wide is it?",
                    "2(2w+3) + 2w = 54", [(9, "using only one width in the perimeter (2(2%s + 3) + %s = 54)" % (V("w"), V("w"))),
                                          (19, "giving the length, not the width")],
                    "Let %s be the width. The length is 2%s + 3, and the perimeter is 2 × length + 2 × width"
                    % (V("w"), V("w")), U("m", "m"), " The garden is 8 m wide and 19 m long."))
    n, he, his = P.next()
    its.append(word("%s’s aunt is 3 times as old as %s. In 12 years, she will be twice as old as %s. How old is %s now?"
                    % (n, n, n, n), "3a + 12 = 2(a+12)",
                    [(36, "giving the aunt’s age")],
                    "Let %s be %s’s age now. In 12 years, %s is %s + 12 and the aunt is 3%s + 12"
                    % (V("a"), n, n, V("a"), V("a")), U("year old", "years old")))
    its.append(word("Four friends each buy a movie ticket and an $8 snack combo. They pay $96 in total. "
                    "How much is one ticket?", "4(t+8) = 96",
                    [(24, "dividing 96 by 4 and forgetting the snack"), (22, "multiplying only %s by 4 (4%s + 8 = 96)" % (V("t"), V("t")))],
                    "Let %s be the price of one ticket" % V("t"), "$"))
    its.append(word("Bike rental A charges $12 plus $8 an hour. Bike rental B charges $20 plus $6 an hour. "
                    "For how many hours do they cost the same?", "12 + 8h = 20 + 6h",
                    [(F(8, 14), None)],
                    "Let %s be the number of hours" % V("h"), U("hour", "hours"), " Both cost $44."))
    its.append(mcq("A community centre in Burnaby charges $9 for each yoga class, or $50 for a membership plus $4 a class. "
                   "Which equation finds the number of classes, %s, when both options cost the same?" % V("c"),
                   R("9c = 50 + 4c"), [R("9 + c = 50 + 4c"), R("9c = 54c"), R("9c + 50 = 4c")],
                   "Drop-in: 9 for each class, so 9%s. Membership: 50 plus 4 for each class, so 50 + 4%s. Set them equal. "
                   "Solve: 5%s = 50, so %s = 10 classes. Check: 9 × 10 = 90 and 50 + 40 = 90 ✓."
                   % (V("c"), V("c"), V("c"), V("c"))))
    assert solve("9c = 50 + 4c") == 10
    its.append(word("A bike share in Vancouver has two plans. Plan A costs $1.50 to unlock plus $0.30 a minute. "
                    "Plan B costs $0.40 a minute with no unlock fee. For how many minutes do the plans cost the same?",
                    "1.5 + 0.3m = 0.4m",
                    [(F(15, 7), None), (150, "misplacing the decimal point"), (5, "dividing 1.50 by 0.30")],
                    "Let %s be the number of minutes" % V("m"), U("minute", "minutes"), " Both cost $6.00."))
    its.append(word("A trip to Science World costs a school $250 for the bus plus $9 for each student. A tour company "
                    "offers $14 a student with the bus included. For how many students do the options cost the same?",
                    "250 + 9s = 14s", [(5, "giving the difference in the cost per student, $14 − $9")],
                    "Let %s be the number of students" % V("s"), U("student", "students"), " Both cost $700."))
    its.append(word("A hockey team gets 2 points for a win and 1 point for a tie. This season the team has 4 ties and "
                    "38 points. How many games has the team won?", "2w + 4 = 38",
                    [(19, "forgetting to subtract the 4 tie points"), (F(42, 2), "adding the 4 tie points")],
                    "Let %s be the number of wins" % V("w"), U("win", "wins")))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: phone plans, memberships and more", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    G = lambda s: R(s)
    return (
        "<h2>Keep the equation balanced</h2>"
        "<p>An equation is like a level balance. You can add, subtract, multiply or divide, as long as you do the "
        "same thing to <b>both sides</b>. To solve a multi-step equation, follow the same order every time:</p>"
        "<ol><li>Expand any brackets.</li><li>Clear fractions or decimals (optional).</li>"
        "<li>Collect the " + X + "-terms on one side.</li><li>Collect the numbers on the other side.</li>"
        "<li>Divide by the coefficient of " + X + ". Then check.</li></ol>"
        "<figure class='sn-fig'>" + scale_svg(["x"] * 5 + ["3"], ["x", "x", "18"], "5x + 3 = 2x + 18") +
        "<figcaption>5" + X + " + 3 = 2" + X + " + 18. Take 2 blocks off both pans: 3" + X + " + 3 = 18. "
        "Take 3 off both pans: 3" + X + " = 15, so " + X + " = 5.</figcaption></figure>" +
        ex("Example 1: variables on both sides", "Solve " + G("7x - 4 = 3x + 20") + ".",
           "Subtract 3" + X + " from both sides: 4" + X + " − 4 = 20. Add 4: 4" + X + " = 24. Divide by 4: " + X + " = 6. "
           "Check: 7 × 6 − 4 = 38 and 3 × 6 + 20 = 38 ✓.", X + " = 6") +
        "<h2>Brackets: multiply both terms</h2>"
        "<p>The number in front of the brackets multiplies <b>every</b> term inside. A minus sign in front belongs to "
        "that number, so it changes the sign of both terms.</p>"
        "<figure class='sn-fig'>" + dist_svg(M + "2", "x", M, "3", M + "2", "+", "6") +
        "<figcaption>" + M + "2 × " + X + " = " + M + "2" + X + " and " + M + "2 × (" + M + "3) = +6.</figcaption></figure>" +
        ex("Example 2: brackets", "Solve " + G("5 - 2(x-3) = 1") + ".",
           "Expand: " + M + "2(" + X + " " + M + " 3) = " + M + "2" + X + " + 6, so 5 " + M + " 2" + X + " + 6 = 1. "
           "Simplify: 11 " + M + " 2" + X + " = 1. Subtract 11: " + M + "2" + X + " = " + M + "10. Divide by " + M + "2: "
           + X + " = 5. Check: 5 " + M + " 2(5 " + M + " 3) = 5 " + M + " 4 = 1 ✓.", X + " = 5") +
        "<h2>Fractions and decimals</h2>"
        "<p>Multiply <b>every</b> term on both sides by the lowest common denominator (LCD). The fractions disappear. "
        "With decimals, multiply every term by 10 or 100.</p>" +
        ex("Example 3: fractions", "Solve " + G("x/2 + x/3 = 10") + ".",
           "The LCD of 2 and 3 is 6. Multiply every term by 6: 3" + X + " + 2" + X + " = 60. So 5" + X + " = 60 and "
           + X + " = 12. Check: 12 ÷ 2 + 12 ÷ 3 = 6 + 4 = 10 ✓.", X + " = 12") +
        ex("Example 4: decimals", "Solve " + G("0.4x + 1.2 = 3.6") + ".",
           "Multiply every term by 10: 4" + X + " + 12 = 36. Subtract 12: 4" + X + " = 24. Divide by 4: " + X + " = 6. "
           "Check: 0.4 × 6 + 1.2 = 2.4 + 1.2 = 3.6 ✓.", X + " = 6") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            [G("3(x-4)") + " = 3" + X + " " + M + " 4", "Multiply both terms: 3" + X + " " + M + " 12"],
            [M + "2(" + X + " " + M + " 3) = " + M + "2" + X + " " + M + " 6", M + "2 × (" + M + "3) = +6, so " + M + "2" + X + " + 6"],
            ["9 " + M + " (" + X + " " + M + " 4) = 9 " + M + " " + X + " " + M + " 4", "The minus changes both signs: 9 " + M + " " + X + " + 4"],
            [G("7x + 4 = 3x + 24") + ": add 3" + X, "Subtract 3" + X + " from both sides: 4" + X + " + 4 = 24"],
            [G("x/2 + 3 = x/5") + ": 5" + X + " + 3 = 2" + X, "Multiply every term by 10, including 3: 5" + X + " + 30 = 2" + X],
            ["Checking in a changed equation", "Always check in the <b>original</b> equation"],
        ])
    )


FAQ = [
    {"q": "How do you solve multi-step linear equations in Grade 9?",
     "a": "Expand any brackets, collect the x-terms on one side and the numbers on the other, then divide by the coefficient of x. For 7x − 4 = 3x + 20, subtract 3x (4x − 4 = 20), add 4 (4x = 24) and divide by 4 (x = 6)."},
    {"q": "Are multi-step equations part of the BC Math 9 curriculum?",
     "a": "Yes. The BC Mathematics 9 Patterning standard includes multi-step one-variable linear equations, with brackets, variables on both sides, fractions and decimals."},
    {"q": "How do you solve an equation with variables on both sides?",
     "a": "Subtract the smaller x-term from both sides so x is on one side only. Then solve the two-step equation that is left and check your answer in the original equation."},
    {"q": "How do you solve linear equations with fractions?",
     "a": "Multiply every term on both sides by the lowest common denominator. For x/2 + x/3 = 10, multiply by 6 to get 3x + 2x = 60, so x = 12."},
]


def gen_unit():
    rnd = random.Random(59805)
    P = People(rnd)
    sets = [set_review(P), set_both(P), set_brackets(P), set_fracdec(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-9", "slug": "linear-equations", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 9 Multi-Step Linear Equations",
        "seo_title": "Grade 9 Linear Equations Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Linear Equations",
        "domain": "Patterning",
        "standard_code": "Grade 9: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/9/core",
        "standard_text": "Multi-step one-variable linear equations",
        "meta_desc": "Free Grade 9 math worksheets on multi-step linear equations for the BC curriculum: variables on both sides, brackets, fractions and decimals, and word problems with phone plans and memberships. 100 questions with an answer key.",
        "key_big": "Do the same thing to both sides: expand the brackets, collect the x-terms on one side, then the numbers on the other.",
        "key_sub": "7x − 4 = 3x + 20: subtract 3x (4x − 4 = 20), add 4 (4x = 24), divide by 4 (x = 6). Check: 7 × 6 − 4 = 38 = 3 × 6 + 20.",
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
