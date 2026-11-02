# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Dividing Fractions (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p6_dividing_fractions.py
P6 divides a proper fraction by a whole number, and a whole number or a proper fraction by a proper fraction,
without a calculator. Sets: fraction ÷ whole number with bar models, whole number ÷ fraction ("how many
quarters are there in 3?") with fraction bars, fraction ÷ fraction (multiply by the reciprocal, simplest form),
mixed practice and checking by multiplying, and PSLE-style word problems with bar models (units and parts).
Wrong answers are real mistakes: flipping the first fraction, not flipping (multiplying), flipping both,
dividing the numerator only / the numerator and denominator wrongly, counting the leftover pieces as a part
of a whole, dropping the leftover, simplifying only the numerator or only the denominator.
Every answer is checked with fractions.Fraction; no two choices are equal in value; every explanation shows
the correct choice in bold. Helpers adapted from gen_uk_maths_y6_mult_div_fractions.py and
gen_cabc_math_g8_mult_div_fractions.py. Singapore English, ℓ for litres. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
G1 = "#3f9a63"        # dark part / group colour 1
G2 = "#a6dbb7"        # group colour 2
LIGHT = "#d7ecdf"     # light part
DARKLINE = "#1f6b3e"
PART = "#f3c9c4"      # partial group
LINE = "#2b2b2b"
THIN = "#9a9a9a"
GRAY = "#8a8178"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
PL = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
      10: "tenths", 12: "twelfths"}
SG = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
      10: "tenth", 12: "twelfth"}


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def show(v):
    """A positive Fraction in simplest form, as a mixed number when greater than 1."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%d %s" % (w, fr(r, v.denominator))


def imp(v):
    """Whole number or (possibly improper) fraction."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def tx(v):
    """Plain text for aria labels: 3/4, 1 1/2."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    return ("%d %d/%d" % (w, r, v.denominator)) if w else "%d/%d" % (r, v.denominator)


def lcm(a, b):
    return a * b // gcd(a, b)


def pl(k, one, many):
    return one if k == 1 else many


def cap(s):
    return s[0].upper() + s[1:]


def dv(x, y):
    return "%s ÷ %s" % (show(x), show(y))


def qty(v, one, many=None):
    many = one if many is None else many
    return "%s %s" % (show(v), one if F(v) <= 1 else many)


def mcq(q, correct, cands, e):
    """correct / cands: (html, value). value None = not a number. A candidate equal in value to an
    earlier choice (or not positive) is skipped. Positions are set later by balance()."""
    ch, vals = [correct[0]], ({correct[1]} if correct[1] is not None else set())
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
            continue
        ch.append(h)
        if v is not None:
            vals.add(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e, "_num": correct[1] is not None}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures (bars, fraction bars, bar models) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ figures
def text(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def div_svg(a, b, n, W=250, H=90):
    """a/b ÷ n: a bar (1 whole) cut into b columns, a shaded light; row lines cut it into n rows
    (solid inside the shaded part, dashed outside); the top row of the shaded part is dark."""
    L, T = 4, 4
    cw, rh = W / float(b), H / float(n)
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff'/>" % (L, T, W, H),
         "<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (L, T, a * cw, H, LIGHT),
         "<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='%s'/>" % (L, T, a * cw, rh, G1)]
    for r in range(1, n):
        y = T + r * rh
        s.append("<line x1='%d' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (L, y, L + a * cw, y, LINE))
        if a < b:
            s.append("<line x1='%.1f' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-dasharray='5 4'/>"
                     % (L + a * cw, y, L + W, y, THIN))
    for c in range(1, b):
        x = L + c * cw
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, T, x, T + H, LINE))
    s.append("<rect x='%d' y='%d' width='%.1f' height='%.1f' fill='none' stroke='%s' stroke-width='3.5'/>"
             % (L, T, a * cw, rh, DARKLINE))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (L, T, W, H, LINE))
    return svg_wrap(W + 8, H + 8, "".join(s),
                    "bar split: 1 whole cut into %d columns, %d shaded, the shaded part split into %d equal rows" % (b, a, n))


def groups_svg(a, b, PW=None):
    """Fraction bar: ceil(a) wholes cut into L pieces each (L = common denominator).
    The first a*L pieces are shaded in groups of b*L pieces (two greens); a partial group is pink.
    Brackets above number the full groups. Labels 0, 1, 2 ... under the whole lines (a number line)."""
    a, b = F(a), F(b)
    L = lcm(a.denominator, b.denominator)
    k, m = int(a * L), int(b * L)
    nw = max(1, -(-a.numerator // a.denominator))
    total = nw * L
    if PW is None:
        PW = max(14, min(44, (470 if total > 12 else 380) // total))
    X0, T, BH = 14, 34, 34
    W = X0 * 2 + total * PW
    s = []
    full = k // m
    for i in range(total):
        if i < full * m:
            col = G1 if (i // m) % 2 == 0 else G2
        elif i < k:
            col = PART
        else:
            col = "#ffffff"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.4'/>"
                 % (X0 + i * PW, T, PW, BH, col, LINE))
    for j in range(nw + 1):
        x = X0 + j * L * PW
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3.5'/>" % (x, T - 2, x, T + BH + 8, LINE))
        s.append(text(x, T + BH + 26, str(j), 16))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='3'/>" % (X0, T, total * PW, BH, LINE))
    g = 0
    while g * m < k:
        x0 = X0 + g * m * PW + 2
        x1 = X0 + min(k, (g + 1) * m) * PW - 2
        isfull = (g + 1) * m <= k
        colr = LINE if isfull else RED
        s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x0, T - 4, T - 12, x1, T - 4, colr))
        if isfull:
            s.append(text((x0 + x1) / 2.0, T - 16, str(g + 1), 15 if g < 9 else 14))
        elif (g + 1) * m <= total:          # dashed: how long a full group would be
            xf = X0 + (g + 1) * m * PW - 2
            s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>"
                     % (x0, T - 16, T - 24, xf, T - 16, GRAY))
        g += 1
    label = "fraction bar: %s shaded in groups of %s, %d pieces in each whole" % (tx(a), tx(b), L)
    return svg_wrap(W, T + BH + 32, "".join(s), label)


def lab_w(parts, fs=16):
    w = 0
    for p in parts:
        if isinstance(p, tuple):
            w += max(len(str(p[0])), len(str(p[1]))) * fs * 0.62 + 6
        else:
            w += len(p) * fs * 0.56
    return w


def lab(cx, mid, parts, fs=16, col=LINE):
    """A label centred at cx: plain text and stacked fractions (n, d); the fraction line sits at y = mid."""
    w = lab_w(parts, fs)
    x = cx - w / 2.0
    s = []
    for p in parts:
        if isinstance(p, tuple):
            pw = max(len(str(p[0])), len(str(p[1]))) * fs * 0.62 + 6
            c = x + pw / 2.0
            s.append(text(c, mid - 4, str(p[0]), fs, col))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
                     % (x + 2, mid, x + pw - 2, mid, col))
            s.append(text(c, mid + 16, str(p[1]), fs, col))
            x += pw
        else:
            pw = len(p) * fs * 0.56
            s.append(text(x + pw / 2.0, mid + 6, p.replace(" ", "&#160;") if p.strip() != p else p, fs, col))
            x += pw
    return "".join(s)


def model_svg(units, dark, top=None, bottoms=(), inside=None, W=300, label="bar model"):
    """Bar model: `units` equal boxes; `dark` = indices shaded green. top = (i0, i1, parts) bracket above,
    bottoms = [(i0, i1, parts)] brackets below. parts: list of text and (n, d) fractions."""
    X0 = 10
    U = W / float(units)
    y = 2
    s = []
    if top:
        mid = y + 18
        i0, i1, parts = top
        s.append(lab(X0 + (i0 + i1) * U / 2.0, mid, parts))
        y = mid + 22
        s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (X0 + i0 * U + 2, y + 8, y, X0 + i1 * U - 2, y + 8, LINE))
        y += 12
    bt, BH = y, 34
    for i in range(units):
        col = G1 if i in dark else "#fff"
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (X0 + i * U, bt, U, BH, col, LINE))
        if inside and i in inside:
            s.append(text(X0 + i * U + U / 2.0, bt + 23, inside[i], 15, "#fff" if i in dark else LINE))
    s.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='3'/>"
             % (X0, bt, units * U, BH, LINE))
    y = bt + BH + 4
    if bottoms:
        for i0, i1, parts in bottoms:
            s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (X0 + i0 * U + 2, y, y + 8, X0 + i1 * U - 2, y, LINE))
            hasf = any(isinstance(x, tuple) for x in parts)
            s.append(lab(X0 + (i0 + i1) * U / 2.0, y + (30 if hasf else 20), parts))
        y += 8 + (44 if any(isinstance(x, tuple) for b in bottoms for x in b[2]) else 30)
    else:
        y += 2
    return svg_wrap(W + 2 * X0, y, "".join(s), label)


# ------------------------------------------------------------ explanations
def conv(v):
    v = F(v)
    if v.denominator == 1:
        return "Write %d as %s. " % (v.numerator, fr(v.numerator, 1))
    return ""


def chain(x, y, unit=""):
    """x × y (fractions, improper allowed), cancelling common factors first. Ends in <b>answer</b>."""
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    s = ""
    steps = []
    g1, g2 = gcd(a, d), gcd(c, b)
    for g, p, q in ((g1, a, d), (g2, c, b)):
        if g > 1:
            steps.append(("the %ds cancel" % p) if p == q else ("divide %d and %d by %d" % (p, q, g)))
    a2, d2 = a // g1, d // g1
    c2, b2 = c // g2, b // g2
    v = F(a2 * c2, b2 * d2)
    if steps:
        s += "%s × %s. Cancel common factors first: %s. Now %s × %s = " % (
            imp(x), imp(y), ", and ".join(steps), imp(F(a2, b2)) if b2 != 1 else str(a2),
            imp(F(c2, d2)) if d2 != 1 else str(c2))
        parts = [imp(v)]
    elif b * d == 1:
        s += "%d × %d = " % (a, c)
        parts = [str(a * c)]
    else:
        s += "%s × %s = %s = " % (imp(x), imp(y), fr("%d × %d" % (a, c), "%d × %d" % (b, d)))
        parts = [fr(a * c, b * d)]
    if v.denominator != 1 and v > 1:
        parts.append(show(v))
    last = parts[-1] + (" " + unit if unit else "")
    s += "".join(p + " = " for p in parts[:-1]) + "<b>%s</b>." % last
    return s


def div_e(x, y, unit="", lead="", check=True):
    """x ÷ y: multiply by the reciprocal of the divisor, then check by multiplying."""
    x, y = F(x), F(y)
    q = x / y
    s = lead
    s += "Dividing by %s is the same as multiplying by its reciprocal, %s: " % (imp(y), imp(1 / y))
    s += "%s ÷ %s = " % (imp(x), imp(y)) + chain(x, 1 / y, unit)
    if check:
        s += " Check: %s × %s = %s." % (show(q), show(y), show(x))
    return s


def fw_e(a, b, n, unit=""):
    """a/b ÷ n with a proper fraction and a whole number."""
    v = F(a, b * n)
    u = " " + unit if unit else ""
    if a % n == 0:
        s = ("The numerator %d can be divided by %d: %d ÷ %d = %d. Keep the denominator: %s ÷ %d = <b>%s%s</b>."
             % (a, n, a, n, a // n, fr(a, b), n, show(v), u))
    else:
        s = ("Dividing by %d is the same as multiplying by %s: %s ÷ %d = %s × %s = %s"
             % (n, fr(1, n), fr(a, b), n, fr(a, b), fr(1, n), fr(a, b * n)))
        if gcd(a, b * n) > 1:
            s += ". Simplify: %s = <b>%s%s</b>." % (fr(a, b * n), show(v), u)
        else:
            s = s[:-len(fr(a, b * n))] + "<b>%s%s</b>." % (fr(a, b * n), u)
    back = fr(v.numerator * n, v.denominator)
    s += " Check: %s × %d = %s%s." % (show(v), n, back, "" if back == fr(a, b) else " = " + fr(a, b))
    return s


def e_groups(a, b):
    """How many groups of b fit in a, explained with pieces of a common denominator."""
    a, b = F(a), F(b)
    q = a / b
    L = lcm(a.denominator, b.denominator)
    k, m = int(a * L), int(b * L)
    nm, one = PL[L], SG[L]
    eq = []
    for v, c in ((a, k), (b, m)):
        if not (v.denominator == L and v < 1):
            eq.append("%s = %s" % (show(v), fr(c, L)))
    s = "Count in %s%s. " % (nm, (": " + " and ".join(eq)) if eq else "")
    s += "Each group is %d %s. " % (m, pl(m, one, nm))
    full, r = divmod(k, m)
    if r == 0:
        s += "%d %s make %d ÷ %d = %d %s. " % (k, nm, k, m, full, pl(full, "group", "groups"))
    else:
        s += ("%d %s make %d full %s, with %d %s left over. %s %s of a group. "
              % (k, nm, full, pl(full, "group", "groups"), r, pl(r, one, nm),
                 ("That 1 " + one + " is") if r == 1 else ("Those %d %s are" % (r, nm)), fr(r, m)))
    s += "So %s = <b>%s</b>. Check: %s × %s = %s." % (dv(a, b), show(q), show(q), show(b), show(a))
    return s


# ------------------------------------------------------------ typical wrong answers
def dwr(x, y, order):
    """x ÷ y: values from real mistakes."""
    x, y = F(x), F(y)
    q = x / y
    a, b, c, d = x.numerator, x.denominator, y.numerator, y.denominator
    out = []
    for k in order:
        if k == "nf":                       # did not flip: multiplied
            out.append(x * y)
        elif k == "first":                  # flipped the first number instead of the divisor
            out.append(y / x)
        elif k == "both":                   # flipped both
            out.append(1 / (x * y))
        elif k == "add":                    # fraction ÷ n: added n to the denominator
            if d == 1:
                out.append(F(a, b + c))
        elif k == "part":                   # fraction ÷ n: found 1/n (part of the shaded piece only)
            if d == 1:
                out.append(F(1, c))
        elif k == "divboth":                # fraction ÷ n: divided numerator and denominator by n
            if d == 1 and a % c == 0 and b % c == 0:
                out.append(x)
        elif k == "wdivtop":                # whole ÷ a/b: divided by the numerator only
            if b == 1:
                out.append(F(a, c))
        elif k == "wmulbot":                # whole ÷ a/b: multiplied by the denominator only
            if b == 1 and c > 1:
                out.append(F(a * d))
        elif k == "addwb":                  # whole ÷ 1/b: added
            if b == 1:
                out.append(F(a + d))
        elif k == "bonly":                  # whole ÷ 1/b: pieces in one whole
            if b == 1:
                out.append(F(d))
        elif k == "leftover":               # leftover pieces written as part of a whole
            L = lcm(b, d)
            kk, m = int(x * L), int(y * L)
            if q.denominator != 1 and kk > m:
                out.append(kk // m + F(kk % m, L))
        elif k == "drop":                   # dropped the leftover
            if q.denominator != 1 and q > 1:
                out.append(F(math.floor(q)))
        elif k == "sameden":                # same denominators: divided the numerators, kept the denominator
            if b == d:
                out.append(F(a, c) / b)
        elif k == "addfr":                  # added across
            out.append(F(a + c, b + d))
        elif k in ("topsimp", "botsimp"):   # simplified only the numerator / only the denominator
            n, mm = a * d, b * c
            g = gcd(n, mm)
            if g > 1:
                out.append(F(n // g, mm) if k == "topsimp" else F(n, mm // g))
        else:
            raise ValueError(k)
    return out


def S(v):
    return (show(v), F(v))


def Ss(vals):
    return [S(v) for v in vals if F(v) > 0]


def Q(vals, one, many=None):
    return [(qty(v, one, many), F(v)) for v in vals if F(v) > 0]


def ask(expr, v, simplest=False):
    q = "%s = <b>?</b>" % expr
    v = F(v)
    if v > 1 and v.denominator != 1:
        q += "<br>Give your answer as a mixed number in its simplest form."
    elif simplest:
        q += "<br>Give your answer in its simplest form."
    return q


def fw(a, b, n):
    return "%s ÷ %d" % (fr(a, b), n)


# ============================================================ set 1: proper fraction ÷ whole number
def set_frac_by_whole():
    its = []
    # A) bar models
    for a, b, n, order in [(1, 3, 2, ["nf", "part", "add", "first"]), (1, 2, 4, ["part", "nf", "first", "add"]),
                           (2, 3, 2, ["nf", "add", "part", "first"]), (3, 4, 2, ["add", "nf", "first", "part"]),
                           (2, 5, 3, ["first", "nf", "add", "part"]), (4, 5, 2, ["nf", "part", "first", "add"])]:
        v = F(a, b * n)
        q = (fig(div_svg(a, b, n)) + "The bar is 1 whole. The shaded part is %s. It is divided into %d equal parts. "
             "What fraction of the <b>whole</b> bar is the dark part?<br>%s = <b>?</b>" % (fr(a, b), n, fw(a, b, n)))
        e = ("Follow the lines across the bar: the whole is cut into %d × %d = %d equal parts, and %d of them %s dark: %s%s. "
             % (b, n, b * n, a, "is" if a == 1 else "are", fr(a, b * n),
                "" if v.denominator == b * n else " = " + show(v))) + fw_e(a, b, n)
        its.append(mcq(q, S(v), Ss(dwr(F(a, b), n, order)), e))
    # B) calculate
    for a, b, n, order in [(1, 5, 4, ["nf", "add", "first", "part"]), (4, 7, 2, ["nf", "first", "add", "part"]),
                           (6, 11, 3, ["add", "nf", "first", "part"]), (3, 8, 2, ["nf", "add", "first", "part"]),
                           (2, 9, 4, ["topsimp", "nf", "add", "first"]), (3, 5, 6, ["botsimp", "add", "nf", "first"]),
                           (5, 6, 10, ["topsimp", "nf", "first", "add"]), (8, 9, 4, ["first", "nf", "add", "part"]),
                           (3, 10, 4, ["nf", "add", "first", "part"]), (4, 9, 6, ["botsimp", "nf", "add", "first"])]:
        v = F(a, b * n)
        ws = dwr(F(a, b), n, order)
        if order[0] in ("topsimp", "botsimp"):      # simplifying only one part of a/(b × n)
            g = gcd(a, b * n)
            ws = [F(a // g, b * n) if order[0] == "topsimp" else F(a, b * n // g)] + ws[1:]
        its.append(mcq(ask(fw(a, b, n), v, simplest=gcd(a, b * n) > 1), S(v), Ss(ws), fw_e(a, b, n)))
    # C) the same as multiplying
    q = "Dividing by 5 is the same as …"
    its.append(mcq(q, ("multiplying by %s" % fr(1, 5), None),
                   [("multiplying by 5", None), ("dividing by %s" % fr(1, 5), None), ("subtracting 5", None)],
                   "Sharing into 5 equal parts gives %s of the amount each, so dividing by 5 is the same as "
                   "<b>multiplying by %s</b>. 5 and %s are reciprocals: 5 × %s = 1." % (fr(1, 5), fr(1, 5), fr(1, 5), fr(1, 5))))
    q = "Which multiplication has the same answer as %s?" % fw(3, 4, 6)
    its.append(mcq(q, ("%s × %s" % (fr(3, 4), fr(1, 6)), F(1, 8)),
                   [("%s × 6" % fr(3, 4), F(9, 2)), ("%s × %s" % (fr(4, 3), fr(1, 6)), F(2, 9)),
                    ("%s × 6" % fr(4, 3), F(8))],
                   "Keep %s and multiply by the reciprocal of 6, which is %s: <b>%s × %s</b> = %s = %s. "
                   "Do not flip %s." % (fr(3, 4), fr(1, 6), fr(3, 4), fr(1, 6), fr(3, 24), fr(1, 8), fr(3, 4))))
    # D) find the mistake
    for nm, he, wrote, kind in [("Hui Min", "she", (2, 5, 4, fr(8, 5)), "nf"), ("Zhi Hao", "he", (4, 5, 2, fr(5, 8)), "first")]:
        a, b, n, w = wrote
        q = "%s says %s = %s. What mistake did %s make?" % (nm, fw(a, b, n), w, he)
        M = {"nf": "%s multiplied by %d instead of dividing." % (cap(he), n),
             "first": "%s flipped %s instead of using the reciprocal of %d." % (cap(he), fr(a, b), n),
             "both": "%s multiplied the numerator and the denominator by %d." % (cap(he), n),
             "ok": "Nothing. The answer is correct."}
        v = F(a, b * n)
        if kind == "nf":
            e = ("%s worked out %s × %d = %s. Dividing a fraction by a whole number makes it smaller. "
                 "%s = %s × %s = %s = %s. So <b>%s</b>" % (nm, fr(a, b), n, fr(a * n, b), fw(a, b, n), fr(a, b), fr(1, n),
                                                           fr(a, b * n), show(v), he + M[kind][len(he):-1]) + ".")
        else:
            e = ("%s worked out %s × %s = %s. Only the divisor is flipped: %s = %s × %s = %s = %s. So <b>%s</b>"
                 % (nm, fr(b, a), fr(1, n), fr(b, a * n), fw(a, b, n), fr(a, b), fr(1, n), fr(a, b * n), show(v),
                    he + M[kind][len(he):-1]) + ".")
        its.append(mcq(q, (M[kind], None), [(M[k], None) for k in ["ok", "nf", "first", "both"] if k != kind], e))
    assert len(its) == 20, len(its)
    return {"title": "Divide a fraction by a whole number", "items": its}


# ============================================================ set 2: whole number ÷ proper fraction
def set_whole_by_frac():
    its = []
    # A) unit fractions with a fraction bar
    for w, d, order in [(3, 4, ["nf", "first", "addwb", "bonly"]), (2, 3, ["first", "nf", "bonly", "addwb"]),
                        (4, 2, ["addwb", "nf", "first", "bonly"]), (2, 5, ["nf", "bonly", "first", "addwb"]),
                        (3, 6, ["bonly", "first", "nf", "addwb"]), (5, 3, ["nf", "addwb", "first", "bonly"])]:
        y = F(1, d)
        q = (fig(groups_svg(F(w), y)) + "The bar shows %d %s, each cut into %s. How many %s are there in %d?<br>"
             "%d ÷ %s = <b>?</b>" % (w, pl(w, "whole", "wholes"), PL[d], PL[d], w, w, fr(1, d)))
        e = ("Each whole has %d %s, so %d %s have %d × %d = %d %s. So %d ÷ %s = <b>%d</b>. Check: %d × %s = %d."
             % (d, PL[d], w, pl(w, "whole", "wholes"), w, d, w * d, PL[d], w, fr(1, d), w * d, w * d, fr(1, d), w))
        its.append(mcq(q, S(w * d), Ss(dwr(w, y, order)), e))
    # B) non-unit fractions with a fraction bar
    for w, y, order in [(2, F(2, 3), ["wmulbot", "nf", "first", "wdivtop"]),
                        (3, F(3, 4), ["wmulbot", "wdivtop", "nf", "first"]),
                        (4, F(2, 5), ["wmulbot", "nf", "wdivtop", "first"]),
                        (2, F(4, 5), ["leftover", "drop", "wmulbot", "nf"]),
                        (3, F(2, 3), ["leftover", "drop", "wmulbot", "nf"])]:
        q = (fig(groups_svg(F(w), y)) + "How many groups of %s are there in %d?<br>%d ÷ %s = <b>?</b>"
             % (fr(y.numerator, y.denominator), w, w, fr(y.numerator, y.denominator)))
        v = F(w) / y
        if v.denominator != 1:
            q += "<br>Give your answer as a mixed number."
        its.append(mcq(q, S(v), Ss(dwr(w, y, order)), e_groups(w, y)))
    # C) calculate
    for w, y, order in [(6, F(3, 4), ["wmulbot", "wdivtop", "nf", "first"]),
                        (8, F(2, 3), ["wdivtop", "wmulbot", "nf", "first"]),
                        (4, F(3, 5), ["drop", "wmulbot", "nf", "first", "wdivtop"]),
                        (9, F(3, 7), ["wmulbot", "wdivtop", "first", "nf"]),
                        (5, F(5, 6), ["wdivtop", "wmulbot", "nf", "first"]),
                        (7, F(2, 3), ["drop", "wmulbot", "nf", "first"]),
                        (10, F(5, 8), ["wmulbot", "wdivtop", "nf", "first"])]:
        v = F(w) / y
        its.append(mcq(ask("%d ÷ %s" % (w, fr(y.numerator, y.denominator)), v), S(v), Ss(dwr(w, y, order)),
                       div_e(w, y)))
    # D) "how many … are there in …?"
    q = "How many fifths are there in 4?"
    its.append(mcq(q, S(20), Ss([F(4, 5), F(9), F(5), F(1, 20)]),
                   "Each whole has 5 fifths, so 4 wholes have 4 × 5 = 20 fifths. This is 4 ÷ %s = 4 × 5 = <b>20</b>."
                   % fr(1, 5)))
    q = "How many groups of %s are there in 6?" % fr(2, 3)
    its.append(mcq(q, S(9), Ss([F(4), F(18), F(3), F(1, 9)]),
                   "6 ÷ %s = 6 × %s = %s = <b>9</b>. Check: 9 × %s = %s = 6." % (fr(2, 3), fr(3, 2), fr(18, 2), fr(2, 3),
                                                                             fr(18, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Divide a whole number by a fraction", "items": its}


# ============================================================ set 3: proper fraction ÷ proper fraction
def set_frac_by_frac():
    its = []
    # A) reciprocals
    its.append(mcq("What is the reciprocal of %s?" % fr(3, 5), (fr(5, 3), F(5, 3)),
                   [(fr(3, 5), F(3, 5)), (fr(2, 5), F(2, 5)), ("5", F(5))],
                   "Swap the numerator and the denominator: the reciprocal of %s is <b>%s</b>. Check: %s × %s = %s = 1."
                   % (fr(3, 5), fr(5, 3), fr(3, 5), fr(5, 3), fr(15, 15))))
    its.append(mcq("What is the reciprocal of %s?" % fr(1, 7), ("7", F(7)),
                   [(fr(1, 7), F(1, 7)), (fr(6, 7), F(6, 7)), ("1", F(1))],
                   "Swap the numerator and the denominator: %s becomes %s = <b>7</b>. Check: %s × 7 = 1."
                   % (fr(1, 7), fr(7, 1), fr(1, 7))))
    # B) which multiplication
    for a, b, c, d in [(2, 3, 5, 7), (4, 9, 1, 6)]:
        right = "%s × %s" % (fr(a, b), imp(F(d, c)))
        cands = [("%s × %s" % (fr(b, a), fr(c, d)), F(b, a) * F(c, d)),
                 ("%s × %s" % (fr(b, a), imp(F(d, c))), F(b, a) * F(d, c)),
                 ("%s × %s" % (fr(a, b), fr(c, d)), F(a, b) * F(c, d))]
        e = ("Keep the first fraction and multiply by the reciprocal of the divisor %s, which is %s: <b>%s</b>. "
             "Do not flip %s." % (fr(c, d), imp(F(d, c)), right, fr(a, b)))
        its.append(mcq("Which multiplication has the same answer as %s ÷ %s?" % (fr(a, b), fr(c, d)),
                       (right, F(a, b) * F(d, c)), cands, e))
    # C) fraction bars
    for a, b in [(F(2, 3), F(1, 6)), (F(3, 4), F(3, 8)), (F(5, 6), F(1, 3))]:
        q = (fig(groups_svg(a, b, PW=36 if (a * lcm(a.denominator, b.denominator)) < 8 else None))
             + "The bar shows %s. How many groups of %s are there in %s?<br>%s = <b>?</b>"
             % (show(a), show(b), show(a), dv(a, b)))
        its.append(mcq(q, S(a / b), Ss(dwr(a, b, ["nf", "leftover", "first", "drop", "both"])), e_groups(a, b)))
    # D) calculate
    cases = [((1, 2), (3, 4), ["first", "nf", "addfr", "both"]),
             ((2, 5), (4, 5), ["first", "sameden", "nf", "both"]),
             ((6, 7), (2, 7), ["sameden", "nf", "first", "both"]),
             ((3, 8), (1, 4), ["first", "nf", "drop", "both"]),
             ((5, 9), (2, 3), ["first", "nf", "topsimp", "both"]),
             ((7, 10), (3, 5), ["first", "nf", "botsimp", "drop"]),
             ((5, 8), (5, 6), ["topsimp", "first", "nf", "both"]),
             ((3, 10), (9, 20), ["botsimp", "first", "nf", "both"]),
             ((1, 6), (4, 9), ["first", "botsimp", "nf", "both"]),
             ((8, 9), (2, 3), ["topsimp", "first", "nf", "drop"]),
             ((3, 4), (5, 6), ["first", "nf", "topsimp", "both"]),
             ((9, 10), (3, 4), ["botsimp", "first", "nf", "drop"]),
             ((11, 12), (2, 3), ["first", "nf", "topsimp", "drop"])]
    for (a, b), (c, d), order in cases:
        x, y = F(a, b), F(c, d)
        v = x / y
        its.append(mcq(ask(dv(x, y), v, simplest=True), S(v), Ss(dwr(x, y, order)), div_e(x, y)))
    assert len(its) == 20, len(its)
    return {"title": "Divide a fraction by a fraction", "items": its}


# ============================================================ set 4: mixed practice and checking
def set_mixed():
    its = []
    # A) mixed calculations
    for x, y, order in [(F(5, 6), 5, ["nf", "add", "first", "part"]),
                        (4, F(2, 7), ["wdivtop", "wmulbot", "nf", "first"]),
                        (F(3, 5), F(9, 10), ["first", "nf", "topsimp", "both"]),
                        (F(9, 10), 6, ["nf", "add", "first", "part"]),
                        (12, F(3, 4), ["wmulbot", "wdivtop", "nf", "first"]),
                        (F(2, 9), F(5, 6), ["first", "nf", "botsimp", "both"]),
                        (F(6, 11), F(3, 22), ["first", "nf", "botsimp", "both"]),
                        (3, F(4, 9), ["drop", "wmulbot", "nf", "first"]),
                        (F(5, 12), 10, ["nf", "add", "first", "part"])]:
        x = F(x)
        y = F(y)
        v = x / y
        if y.denominator == 1:
            a, b, n = x.numerator, x.denominator, y.numerator
            its.append(mcq(ask(fw(a, b, n), v, simplest=True), S(v), Ss(dwr(x, y, order)), fw_e(a, b, n)))
        else:
            its.append(mcq(ask(dv(x, y), v, simplest=True), S(v), Ss(dwr(x, y, order)), div_e(x, y)))
    # B) checking by multiplying
    q = "Which multiplication checks that %s ÷ %s = 2?" % (fr(3, 4), fr(3, 8))
    its.append(mcq(q, ("2 × %s" % fr(3, 8), None),
                   [("2 × %s" % fr(3, 4), None), ("%s × %s" % (fr(3, 4), fr(3, 8)), None), ("2 × %s" % fr(8, 3), None)],
                   "Answer × divisor should give the number you started with: <b>2 × %s</b> = %s = %s."
                   % (fr(3, 8), fr(6, 8), fr(3, 4))))
    q = "Wei Ming works out %s ÷ %s = 1 %s. Which calculation checks his answer?" % (fr(5, 6), fr(2, 3), fr(1, 4))
    its.append(mcq(q, ("1 %s × %s" % (fr(1, 4), fr(2, 3)), None),
                   [("1 %s × %s" % (fr(1, 4), fr(5, 6)), None), ("1 %s ÷ %s" % (fr(1, 4), fr(2, 3)), None),
                    ("%s × %s" % (fr(5, 6), fr(2, 3)), None)],
                   "Multiply the answer by the divisor: <b>1 %s × %s</b> = %s × %s = %s = %s. "
                   "This is %s, so his answer is correct." % (fr(1, 4), fr(2, 3), fr(5, 4), fr(2, 3), fr(10, 12),
                                                               fr(5, 6), fr(5, 6))))
    q = "Which multiplication checks that 8 ÷ %s = 12?" % fr(2, 3)
    its.append(mcq(q, ("12 × %s" % fr(2, 3), None),
                   [("8 × %s" % fr(2, 3), None), ("12 × %s" % fr(3, 2), None), ("8 × 12", None)],
                   "Multiply the answer by the divisor: <b>12 × %s</b> = %s = 8." % (fr(2, 3), fr(24, 3))))
    q = "Farah says %s ÷ %s = 1 %s. Is she correct?" % (fr(3, 4), fr(2, 5), fr(7, 8))
    its.append(mcq(q, ("Yes, because 1 %s × %s = %s" % (fr(7, 8), fr(2, 5), fr(3, 4)), None),
                   [("No, because 1 %s × %s = %s" % (fr(7, 8), fr(2, 5), fr(3, 8)), None),
                    ("No, the answer should be %s" % fr(3, 10), None),
                    ("No, the answer should be %s" % fr(8, 15), None)],
                   "Check by multiplying: 1 %s × %s = %s × %s = %s = %s. This is the number she started with, "
                   "so <b>yes, because 1 %s × %s = %s</b>." % (fr(7, 8), fr(2, 5), fr(15, 8), fr(2, 5), fr(30, 40),
                                                               fr(3, 4), fr(7, 8), fr(2, 5), fr(3, 4))))
    q = "Ryan says %s ÷ %s = %s. He checks by multiplying. What does he find?" % (fr(4, 9), fr(2, 3), fr(8, 27))
    its.append(mcq(q, ("%s × %s is not %s, so the answer is %s" % (fr(8, 27), fr(2, 3), fr(4, 9), fr(2, 3)), None),
                   [("%s × %s = %s, so he is correct" % (fr(8, 27), fr(2, 3), fr(4, 9)), None),
                    ("%s × %s is not %s, so the answer is %s" % (fr(8, 27), fr(2, 3), fr(4, 9), fr(3, 2)), None),
                    ("%s × %s is not %s, so the answer is %s" % (fr(8, 27), fr(2, 3), fr(4, 9), fr(9, 4)), None)],
                   "%s × %s = %s, which is not %s, so he made a mistake: he multiplied instead of dividing. "
                   "%s ÷ %s = %s × %s = %s = %s. So <b>%s × %s is not %s, so the answer is %s</b>."
                   % (fr(8, 27), fr(2, 3), fr(16, 81), fr(4, 9), fr(4, 9), fr(2, 3), fr(4, 9), fr(3, 2), fr(12, 18),
                      fr(2, 3), fr(8, 27), fr(2, 3), fr(4, 9), fr(2, 3))))
    # C) missing numbers
    q = "<b>?</b> ÷ %s = 12" % fr(1, 4)
    its.append(mcq(q, S(3), Ss([F(48), F(1, 3), F(16)]),
                   "Undo the division by multiplying: <b>?</b> = 12 × %s = %s = <b>3</b>. Check: 3 ÷ %s = 3 × 4 = 12."
                   % (fr(1, 4), fr(12, 4), fr(1, 4))))
    q = "%s ÷ <b>?</b> = 2 %s" % (fr(5, 6), fr(1, 2))
    its.append(mcq(q, S(F(1, 3)), Ss([F(25, 12), F(3), F(5, 3)]),
                   "The divisor = %s ÷ 2 %s = %s ÷ %s = %s × %s = %s = <b>%s</b>. Check: %s ÷ %s = %s × 3 = %s = 2 %s."
                   % (fr(5, 6), fr(1, 2), fr(5, 6), fr(5, 2), fr(5, 6), fr(2, 5), fr(10, 30), fr(1, 3), fr(5, 6),
                      fr(1, 3), fr(5, 6), fr(15, 6), fr(1, 2))))
    # D) mistakes
    q = "Kavya writes %s ÷ %s = %s × %s = %s. What mistake did she make?" % (fr(2, 3), fr(4, 5), fr(3, 2), fr(4, 5), fr(6, 5))
    its.append(mcq(q, ("She flipped the first fraction instead of the divisor.", None),
                   [("She did not flip either fraction.", None), ("She flipped both fractions.", None),
                    ("Nothing. The answer is correct.", None)],
                   "Only the divisor %s is flipped: %s × %s = %s = %s. So <b>she flipped the first fraction instead "
                   "of the divisor</b>." % (fr(4, 5), fr(2, 3), fr(5, 4), fr(10, 12), fr(5, 6))))
    q = "Arjun writes %s ÷ %s = %s × %s = %s. What mistake did he make?" % (fr(3, 7), fr(3, 4), fr(3, 7), fr(3, 4), fr(9, 28))
    its.append(mcq(q, ("He did not use the reciprocal of %s." % fr(3, 4), None),
                   [("He flipped the first fraction.", None), ("He did not simplify.", None),
                    ("Nothing. The answer is correct.", None)],
                   "He multiplied by %s itself. Multiply by its reciprocal %s: %s × %s = %s. The 3s cancel. "
                   "So <b>he did not use the reciprocal of %s</b>." % (fr(3, 4), fr(4, 3), fr(3, 7), fr(4, 3), fr(4, 7),
                                                                       fr(3, 4))))
    q = "Sarah works out %s ÷ %s and gets %s. What should she do next?" % (fr(5, 8), fr(5, 6), fr(30, 40))
    its.append(mcq(q, ("Simplify it to %s." % fr(3, 4), None),
                   [("Nothing. %s is the final answer." % fr(30, 40), None), ("Flip it to %s." % fr(40, 30), None),
                    ("Simplify it to %s." % fr(3, 10), None)],
                   "%s is correct in value but not in its simplest form. Divide the numerator and the denominator by 10: "
                   "<b>simplify it to %s</b>." % (fr(30, 40), fr(3, 4))))
    q = "Which division has an answer greater than 1?"
    its.append(mcq(q, ("%s ÷ %s" % (fr(3, 4), fr(1, 2)), F(3, 2)),
                   [("%s ÷ %s" % (fr(1, 2), fr(3, 4)), F(2, 3)), ("%s ÷ %s" % (fr(2, 5), fr(4, 5)), F(1, 2)),
                    ("%s ÷ 6" % fr(3, 8), F(1, 16))],
                   "When the number you divide is greater than the divisor, the answer is greater than 1. "
                   "%s is greater than %s, and <b>%s ÷ %s</b> = %s × 2 = %s = 1 %s."
                   % (fr(3, 4), fr(1, 2), fr(3, 4), fr(1, 2), fr(3, 4), fr(6, 4), fr(1, 2))))
    assert len(its) == 20, len(its)
    return {"title": "Mixed practice and checking by multiplying", "items": its}


# ============================================================ set 5: PSLE-style word problems
def set_words():
    its = []

    def wd(q, x, y, one, many=None, lead="", wr=None):
        x, y = F(x), F(y)
        v = x / y
        u = one if v <= 1 else (many or one)
        if y.denominator == 1 and x.denominator != 1:
            e = lead + fw_e(x.numerator, x.denominator, y.numerator, u)
        else:
            e = div_e(x, y, unit=u, lead=lead)
        its.append(mcq(q, (qty(v, one, many), v), Q(wr if wr is not None else dwr(x, y, ["nf", "first", "both"]),
                                                    one, many), e))

    # 1 ribbon ÷ 3
    q = (fig(model_svg(3, {0}, top=(0, 3, [(3, 4), " m"]), bottoms=[(0, 1, ["?"])],
                       label="bar model: 3/4 m in 3 equal pieces"))
         + "Nurul has a ribbon %s m long. She cuts it into 3 equal pieces. How long is each piece?" % fr(3, 4))
    wd(q, F(3, 4), 3, "m", lead="3 units = %s m. 1 unit = %s ÷ 3. " % (fr(3, 4), fr(3, 4)),
       wr=dwr(F(3, 4), 3, ["nf", "add", "first"]))
    # 2 Ethan shares a cake among 4 people
    q = (fig(model_svg(4, {0}, top=(0, 4, [(2, 3), " of a cake"]), bottoms=[(0, 1, ["Ethan"])],
                       label="bar model: 2/3 of a cake in 4 equal shares"))
         + "Ethan has %s of a cake. He shares it equally among himself and 3 friends. "
           "What fraction of the whole cake does each person get?" % fr(2, 3))
    wd(q, F(2, 3), 4, "of the cake",
       lead="Ethan and 3 friends make 4 people, so divide by 4, not 3. 4 units = %s. " % fr(2, 3),
       wr=[F(2, 9), F(1, 4), F(2, 7)])
    # 3 soya bean milk in bottles
    wd("Mdm Wong has 6 ℓ of soya bean milk. She pours all of it into bottles. Each bottle holds %s ℓ. "
       "How many bottles does she fill?" % fr(3, 4), 6, F(3, 4), "bottle", "bottles",
       lead="How many %s ℓ are there in 6 ℓ? " % fr(3, 4), wr=[F(9, 2), F(24), F(2), F(1, 8)])
    # 4 sugar for kueh
    wd("Siti has %s kg of sugar. She uses %s kg of sugar for each tray of kueh. How many trays of kueh can she make?"
       % (fr(3, 4), fr(1, 8)), F(3, 4), F(1, 8), "tray", "trays",
       lead="How many %s kg are there in %s kg? " % (fr(1, 8), fr(3, 4)), wr=[F(24), F(8), F(32)])
    # 5 which expression
    q = ("Devi has 5 ℓ of syrup. She pours it into bottles that each hold %s ℓ. "
         "Which expression gives the number of bottles she fills?" % fr(5, 8))
    its.append(mcq(q, ("5 ÷ %s" % fr(5, 8), None),
                   [("5 × %s" % fr(5, 8), None), ("%s ÷ 5" % fr(5, 8), None), ("5 − %s" % fr(5, 8), None)],
                   "The question asks how many %s ℓ there are in 5 ℓ, so divide: <b>5 ÷ %s</b> = 5 × %s = 8 bottles."
                   % (fr(5, 8), fr(5, 8), fr(8, 5))))
    # 6 cups of water
    wd("Hafiz pours %s ℓ of water equally into some cups. Each cup has %s ℓ of water. How many cups are there?"
       % (fr(3, 4), fr(3, 20)), F(3, 4), F(3, 20), "cup", "cups",
       lead="How many %s ℓ are there in %s ℓ? " % (fr(3, 20), fr(3, 4)),
       wr=[F(15), F(20), F(12)])
    # 7 laps
    wd("One round of a cycling path at East Coast Park is %s km. Ryan cycles 4 km. How many rounds does he cycle?"
       % fr(2, 5), 4, F(2, 5), "round", "rounds", lead="How many %s km are there in 4 km? " % fr(2, 5),
       wr=[F(8, 5), F(2), F(20), F(1, 10)])
    # 8 juice for Children's Day
    wd("Mrs Ng buys 5 ℓ of orange juice for a Children’s Day party. Each student gets %s ℓ. "
       "How many students get a cup of juice?" % fr(1, 8), 5, F(1, 8), "student", "students",
       lead="How many %s ℓ are there in 5 ℓ? " % fr(1, 8), wr=[F(8), F(13), F(3)])
    # 9 two thirds of a bottle (units)
    q = (fig(model_svg(3, {0, 1}, top=(0, 3, ["?"]), bottoms=[(0, 2, [(1, 2), " ℓ"])],
                       label="bar model: 2 of 3 units are 1/2 litre"))
         + "%s of a bottle holds %s ℓ of water. How much water does the full bottle hold?" % (fr(2, 3), fr(1, 2)))
    wd(q, F(1, 2), F(2, 3), "ℓ", lead="2 units = %s ℓ, so 1 unit = %s ℓ and 3 units = %s ℓ. Or divide in one step. "
       % (fr(1, 2), fr(1, 4), fr(3, 4)), wr=[F(1, 3), F(4, 3), F(1, 4), F(1, 6)])
    # 10 garden plot
    wd("A rectangular garden plot at a void deck has an area of %s m². Its width is %s m. What is its length?"
       % (fr(2, 3), fr(4, 5)), F(2, 3), F(4, 5), "m", lead="Length = area ÷ width. ",
       wr=[F(8, 15), F(6, 5), F(15, 8), F(2, 15)])
    # 11 rope: full pieces
    its.append(mcq("Raju has 4 m of rope. He cuts as many pieces as he can, each %s m long. How many pieces does he get?"
                   % fr(3, 5), ("6 pieces", F(6)),
                   [("6 %s pieces" % fr(2, 3), F(20, 3)), ("7 pieces", F(7)), ("2 %s pieces" % fr(2, 5), F(12, 5))],
                   "4 ÷ %s = 4 × %s = %s = 6 %s. Only full pieces count, so he gets <b>6 pieces</b>. "
                   "Check: 6 × %s = %s = 3 %s m, which is less than 4 m, but 7 pieces would need 4 %s m."
                   % (fr(3, 5), fr(5, 3), fr(20, 3), fr(2, 3), fr(3, 5), fr(18, 5), fr(3, 5), fr(1, 5))))
    # 12 wire left over
    its.append(mcq("Kumar has 3 m of wire. He cuts as many pieces as he can, each %s m long. "
                   "What length of wire is left over?" % fr(2, 5),
                   (fr(1, 5) + " m", F(1, 5)),
                   [(fr(1, 2) + " m", F(1, 2)), ("2 %s m" % fr(4, 5), F(14, 5)), (fr(2, 5) + " m", F(2, 5))],
                   "3 ÷ %s = 3 × %s = %s = 7 %s, so he cuts 7 full pieces. 7 × %s = %s = 2 %s m. "
                   "Left over: 3 − 2 %s = <b>%s m</b>. (The %s is half of a piece, not %s m.)"
                   % (fr(2, 5), fr(5, 2), fr(15, 2), fr(1, 2), fr(2, 5), fr(14, 5), fr(4, 5), fr(4, 5), fr(1, 5),
                      fr(1, 2), fr(1, 2))))
    # 13 paint for shelves
    wd("Mr Rahman uses %s of a tin of paint to paint 6 identical shelves. What fraction of a tin of paint does he "
       "use for each shelf?" % fr(3, 4), F(3, 4), 6, "of a tin", lead="Share %s among 6 shelves. " % fr(3, 4),
       wr=[F(9, 2), F(3, 10), F(2, 9), F(1, 6)])
    # 14 beef: before and after
    q = (fig(model_svg(4, {0}, top=(0, 4, [(4, 5), " kg"]), bottoms=[(0, 1, ["cooked"]), (1, 4, ["3 packets"])],
                       inside={1: "?", 2: "?", 3: "?"}, label="bar model: 4/5 kg, 1 unit cooked, 3 units in packets"))
         + "Mrs Lim has %s kg of beef. She cooks %s of it. She divides the rest equally into 3 packets. "
           "What is the mass of the beef in each packet?" % (fr(4, 5), fr(1, 4)))
    its.append(mcq(q, (fr(1, 5) + " kg", F(1, 5)),
                   [(fr(4, 15) + " kg", F(4, 15)), (fr(3, 5) + " kg", F(3, 5)), (fr(1, 4) + " kg", F(1, 4))],
                   "Cut the bar into 4 units: she cooks 1 unit and 3 units are left. 4 units = %s kg, so "
                   "1 unit = %s ÷ 4 = %s kg. Each packet holds 1 unit: <b>%s kg</b>. "
                   "(%s kg is the whole %s kg ÷ 3, but she cooked some first.)"
                   % (fr(4, 5), fr(4, 5), fr(1, 5), fr(1, 5), fr(4, 15), fr(4, 5))))
    # 15 grapes: rest shared
    its.append(mcq("Sarah buys %s kg of grapes. She eats %s kg and shares the rest equally among 7 friends. "
                   "What mass of grapes does each friend get?" % (fr(3, 4), fr(1, 6)),
                   (fr(1, 12) + " kg", F(1, 12)),
                   [(fr(3, 28) + " kg", F(3, 28)), ("4 %s kg" % fr(1, 12), F(49, 12)), (fr(1, 42) + " kg", F(1, 42))],
                   "The rest: %s − %s = %s − %s = %s kg. Share it among 7: %s ÷ 7 = <b>%s kg</b>. "
                   "Check: 7 × %s = %s kg." % (fr(3, 4), fr(1, 6), fr(9, 12), fr(2, 12), fr(7, 12), fr(7, 12),
                                                fr(1, 12), fr(1, 12), fr(7, 12))))
    # 16 Priya ribbon: used 1/3, rest into pieces
    q = (fig(model_svg(3, {0}, top=(0, 3, ["2 m"]), bottoms=[(0, 1, ["used"]), (1, 3, ["?"])],
                       label="bar model: 2 m in 3 units, 1 unit used"))
         + "Priya has a ribbon 2 m long. She uses %s of it to wrap a present. She cuts the rest into pieces, "
           "each %s m long. How many pieces does she get?" % (fr(1, 3), fr(2, 9)))
    its.append(mcq(q, ("6 pieces", F(6)),
                   [("9 pieces", F(9)), ("3 pieces", F(3)), ("7 pieces", F(7))],
                   "She uses %s of 2 m = %s m. The rest is 2 − %s = 1 %s m = %s m. "
                   "%s ÷ %s = %s × %s = %s = <b>6 pieces</b>. (9 pieces would use the whole 2 m, and 3 pieces "
                   "is the part she used.)"
                   % (fr(1, 3), fr(2, 3), fr(2, 3), fr(1, 3), fr(4, 3), fr(4, 3), fr(2, 9), fr(4, 3), fr(9, 2),
                      fr(36, 6))))
    # 17 honey in two jars
    its.append(mcq("Jar A has %s ℓ of honey and Jar B has %s ℓ of honey. All the honey is poured into small bottles "
                   "of %s ℓ each. How many bottles are filled?" % (fr(3, 4), fr(1, 2), fr(1, 8)),
                   ("10 bottles", F(10)),
                   [("6 bottles", F(6)), ("4 bottles", F(4)), ("5 %s bottles" % fr(1, 3), F(16, 3))],
                   "Total honey: %s + %s = %s + %s = %s ℓ. %s ÷ %s = %s × 8 = <b>10 bottles</b>. "
                   "(6 bottles is for Jar A only. Do not add the fractions as %s.)" % (fr(3, 4), fr(1, 2), fr(3, 4), fr(2, 4), fr(5, 4), fr(5, 4),
                                                       fr(1, 8), fr(5, 4), fr(4, 6))))
    # 18 noodles at a hawker stall
    its.append(mcq("A hawker uses %s kg of noodles to cook 4 plates of fried noodles. Each plate has the same "
                   "mass of noodles. How many plates can she cook with 3 kg of noodles?" % fr(3, 5),
                   ("20 plates", F(20)),
                   [("5 plates", F(5)), ("12 plates", F(12)), ("15 plates", F(15))],
                   "Each plate: %s ÷ 4 = %s kg. Number of plates: 3 ÷ %s = 3 × %s = %s = <b>20 plates</b>. "
                   "(5 is the number of times %s kg goes into 3 kg; each of those makes 4 plates: 5 × 4 = 20.)"
                   % (fr(3, 5), fr(3, 20), fr(3, 20), fr(20, 3), fr(60, 3), fr(3, 5))))
    # 19 chairs and paint
    its.append(mcq("Ali uses %s of a tin of paint to paint 3 identical chairs. How many such chairs can he paint "
                   "with 2 tins of paint?" % fr(2, 5),
                   ("15 chairs", F(15)),
                   [("5 chairs", F(5)), ("6 chairs", F(6)), ("10 chairs", F(10))],
                   "Each chair: %s ÷ 3 = %s of a tin. Number of chairs: 2 ÷ %s = 2 × %s = %s = <b>15 chairs</b>. "
                   "Check: 15 × %s = %s = 2 tins." % (fr(2, 5), fr(2, 15), fr(2, 15), fr(15, 2), fr(30, 2), fr(2, 15),
                                                     fr(30, 15))))
    # 20 compare two pieces
    its.append(mcq("Mei Ling cuts a ribbon %s m long into 3 equal pieces. Jun Jie cuts a ribbon %s m long into "
                   "2 equal pieces. How much longer is each of Jun Jie’s pieces than each of Mei Ling’s pieces?"
                   % (fr(3, 4), fr(2, 3)),
                   (fr(1, 12) + " m", F(1, 12)),
                   [(fr(1, 6) + " m", F(1, 6)), (fr(1, 2) + " m", F(1, 2)), (fr(1, 3) + " m", F(1, 3))],
                   "Mei Ling: %s ÷ 3 = %s m. Jun Jie: %s ÷ 2 = %s m. Difference: %s − %s = %s − %s = <b>%s m</b>."
                   % (fr(3, 4), fr(1, 4), fr(2, 3), fr(1, 3), fr(1, 3), fr(1, 4), fr(4, 12), fr(3, 12), fr(1, 12))))
    assert len(its) == 20, len(its)
    # easy → hard order
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19]
    return {"title": "PSLE-style word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    div_fig = ("<figure class='sn-fig'>" + div_svg(2, 3, 4, W=270, H=96) +
               "<figcaption>" + fw(2, 3, 4) + ": divide the shaded " + fr(2, 3) + " into 4 equal rows. The whole bar now "
               "has 3 × 4 = 12 equal parts, and the dark part is 2 of them: " + fr(2, 12) + " = " + fr(1, 6)
               + ".</figcaption></figure>")
    whole_fig = ("<figure class='sn-fig'>" + groups_svg(F(3), F(1, 4)) +
                 "<figcaption>3 ÷ " + fr(1, 4) + ": each whole has 4 quarters, so 3 wholes have 12 quarters."
                 "</figcaption></figure>")
    frac_fig = ("<figure class='sn-fig'>" + groups_svg(F(5, 6), F(1, 3), PW=36) +
                "<figcaption>" + dv(F(5, 6), F(1, 3)) + ": " + fr(1, 3) + " = " + fr(2, 6) + ". 2 full groups fit, and the "
                "1 sixth left over is half a group, so the answer is 2 " + fr(1, 2) + ".</figcaption></figure>")
    model_fig = ("<figure class='sn-fig'>" + model_svg(3, {0, 1}, top=(0, 3, ["?"]), bottoms=[(0, 2, [(1, 2), " ℓ"])],
                                                         label="bar model: 2 of 3 units are 1/2 litre") +
                 "<figcaption>2 units = " + fr(1, 2) + " ℓ, so 1 unit = " + fr(1, 4) + " ℓ and 3 units = " + fr(3, 4)
                 + " ℓ.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p><b>Dividing by a number is the same as multiplying by its reciprocal.</b> The reciprocal of "
        + fr(3, 4) + " is " + fr(4, 3) + ", and the reciprocal of 5 is " + fr(1, 5) + ". "
        "Flip only the divisor, the number after ÷. Then simplify.</p>"
        "<h2>Fraction ÷ whole number</h2>"
        "<p>Dividing by 4 means sharing into 4 equal parts. It is the same as multiplying by " + fr(1, 4) + ".</p>"
        + div_fig
        + ex("Example 1", fw(2, 3, 4) + " = ?",
             fw(2, 3, 4) + " = " + fr(2, 3) + " × " + fr(1, 4) + " = " + fr(2, 12) + ". Simplify by dividing the numerator "
             "and the denominator by 2.", fr(1, 6))
        + "<h2>Whole number ÷ fraction</h2>"
        "<p>3 ÷ " + fr(1, 4) + " asks: how many quarters are there in 3?</p>"
        + whole_fig
        + ex("Example 2", "6 ÷ " + fr(3, 4) + " = ?",
             "Multiply by the reciprocal of " + fr(3, 4) + ": 6 × " + fr(4, 3) + " = " + fr(24, 3) + " = 8. "
             "Check: 8 × " + fr(3, 4) + " = " + fr(24, 4) + " = 6.", "8")
        + "<h2>Fraction ÷ fraction</h2>"
        "<p>Ask how many groups of the divisor fit, or multiply by the reciprocal.</p>"
        + frac_fig
        + ex("Example 3", dv(F(3, 4), F(3, 8)) + " = ?",
             fr(3, 4) + " × " + fr(8, 3) + ". The 3s cancel, and 8 ÷ 4 = 2, so the answer is 2. "
             "Check: 2 × " + fr(3, 8) + " = " + fr(6, 8) + " = " + fr(3, 4) + ".", "2")
        + ex("Example 4", dv(F(1, 2), F(3, 4)) + " = ?",
             fr(1, 2) + " × " + fr(4, 3) + " = " + fr(4, 6) + " = " + fr(2, 3) + ". The answer is less than 1, "
             "because " + fr(3, 4) + " does not fit into " + fr(1, 2) + " even once.", fr(2, 3))
        + "<h2>Word problems: units and parts</h2>"
        "<p>Draw a bar model. Find the value of 1 unit first.</p>"
        + model_fig
        + ex("Example 5", fr(2, 3) + " of a bottle holds " + fr(1, 2) + " ℓ of water. How much does the full bottle hold?",
             "2 units = " + fr(1, 2) + " ℓ. 1 unit = " + fr(1, 2) + " ÷ 2 = " + fr(1, 4) + " ℓ. 3 units = 3 × "
             + fr(1, 4) + " = " + fr(3, 4) + " ℓ. In one step: " + fr(1, 2) + " ÷ " + fr(2, 3) + " = " + fr(1, 2) + " × "
             + fr(3, 2) + " = " + fr(3, 4) + ".", fr(3, 4) + " ℓ")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            [dv(F(2, 3), F(4, 5)) + " = " + fr(3, 2) + " × " + fr(4, 5) + " (flipping the first fraction)",
             "Flip only the divisor: " + fr(2, 3) + " × " + fr(5, 4) + " = " + fr(5, 6)],
            [dv(F(3, 7), F(3, 4)) + " = " + fr(3, 7) + " × " + fr(3, 4) + " (not flipping)",
             "Use the reciprocal: " + fr(3, 7) + " × " + fr(4, 3) + " = " + fr(4, 7)],
            [fw(2, 5, 4) + " = " + fr(8, 5) + " (multiplying the numerator by 4)",
             "Multiply the denominator: " + fr(2, 20) + " = " + fr(1, 10)],
            ["6 ÷ " + fr(3, 4) + " = 2 (dividing by the numerator only)",
             "6 × " + fr(4, 3) + " = 8"],
            [dv(F(5, 8), F(5, 6)) + " = " + fr(30, 40) + " (not in simplest form)",
             "Simplify: " + fr(30, 40) + " = " + fr(3, 4)],
        ])
    )


FAQ = [
    {"q": "How do you divide fractions in Primary 6?",
     "a": "Multiply by the reciprocal of the divisor, then simplify. For example, 3/4 ÷ 3/8 = 3/4 × 8/3 = 2, and 2/3 ÷ 4 = 2/3 × 1/4 = 1/6."},
    {"q": "How do I explain dividing by a fraction to my child?",
     "a": "Ask “how many of these fit?”. 3 ÷ 1/4 asks how many quarters there are in 3, and a bar cut into quarters shows there are 12."},
    {"q": "What is the most common mistake when dividing fractions?",
     "a": "Flipping the wrong fraction. Only the divisor (the number after ÷) is flipped, so 2/3 ÷ 4/5 = 2/3 × 5/4 = 5/6, not 3/2 × 4/5."},
    {"q": "Is dividing fractions tested in the PSLE?",
     "a": "Yes. Dividing a proper fraction by a whole number or by a proper fraction is in the MOE Primary 6 syllabus, and the PSLE tests it in calculations without a calculator and in word problems."},
]


def gen():
    rnd = random.Random(66801)
    sets = [set_frac_by_whole(), set_whole_by_frac(), set_frac_by_frac(), set_mixed(), set_words()]
    for s in sets:
        for it in s["items"]:
            if it.pop("_num"):
                assert ("<b>%s</b>" % it["c"][0]) in it["e"], (it["q"], it["c"][0], it["e"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"].replace("<span class='fd'>", "/"))
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "dividing-fractions",
        "sort": 1, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Dividing Fractions",
        "seo_title": "P6 Dividing Fractions Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE Practice)",
        "short_title": "Dividing Fractions",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Dividing a proper fraction by a whole number, and a whole number or proper fraction by a proper fraction, without calculator",
        "meta_desc": "Free P6 maths practice on dividing fractions for the PSLE: fraction ÷ whole number, whole number ÷ fraction, fraction ÷ fraction. 100 questions with answers.",
        "key_big": "To divide by a fraction or a whole number, multiply by its reciprocal. Flip only the divisor.",
        "key_sub": "3/4 ÷ 3/8 = 3/4 × 8/3 = 2, and 2/3 ÷ 4 = 2/3 × 1/4 = 1/6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(fraction bar|bar split|bar model)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
