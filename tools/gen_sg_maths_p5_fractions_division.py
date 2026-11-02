# -*- coding: utf-8 -*-
"""
Singapore Primary 5 Maths: Fractions and division
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 5: Fractions)
"Dividing a whole number by a whole number with quotient as a fraction; expressing fractions as decimals"
  python3 tools/gen_sg_maths_p5_fractions_division.py
3 ÷ 4 = 3/4 (sharing model), 7 ÷ 3 = 2 1/3, fractions as decimals, decimals correct to 2 decimal places,
word problems with bar models. Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Singapore style: British spelling, $ and ¢, ℓ and ml, names of a Singapore classroom.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re, math
from decimal import Decimal as Dm, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-5")
UPDATED = "2026-11-03"
FILL = "#4fae74"
LIGHT = "#e3f1e7"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#d6453b"
GREEN = "#006633"
PIZ = "#f6d78b"
CRUST = "#b5762a"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, a, b):
    if w == 0:
        return fr(a, b)
    if a == 0:
        return str(w)
    return "%d %s" % (w, fr(a, b))


def mx(v, unit=""):
    """Fraction v as a mixed number (or proper fraction) in simplest form."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    s = mixed(w, r, v.denominator) if r else str(w)
    return s + (" " + unit if unit else "")


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢)?( .+)?$")


def val(c):
    """Value of a choice with its unit, or None for choices that are not a single number."""
    m = FRX.match(c)
    if m:
        return (int(m.group(1) or 0) + F(int(m.group(2)), int(m.group(3))), (m.group(4) or "").strip())
    m = NUM.match(c)
    if not m:
        return None
    v = F(m.group(2))
    if m.group(1):
        return (v, "$")
    if m.group(3):
        return (v / 100, "$")
    return (v, (m.group(4) or "").strip())


def mcq(q, correct, wrong, e, same_ok=False, right_val=None):
    """4 choices: correct first + 3 wrong (positions set later by balance()). No two choices may have the same value.
    right_val: the true value; the correct choice must show exactly that value."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        known = [v for v in vs if v is not None]
        assert len(set(known)) == len(known), (q, ch)
        if right_val is not None:
            assert vs[0] is not None and vs[0][0] == F(right_val), (q, correct, right_val)
            for v in vs[1:]:
                assert v is None or v[0] != F(right_val), (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def dec(v):
    """Exact decimal text of a Fraction with a terminating decimal."""
    v = F(v)
    d = Dm(v.numerator) / Dm(v.denominator)
    assert F(d) == v, v
    return format(d.normalize(), "f")


def dp2(v):
    """Fraction v correct to 2 decimal places (round half up), as text with 2 places."""
    v = F(v)
    d = (Dm(v.numerator) / Dm(v.denominator)).quantize(Dm("0.01"), rounding=ROUND_HALF_UP)
    return format(d, "f")


def dp3_cut(v):
    """First 3 decimal places of v (cut, not rounded), e.g. 2/3 -> 0.666."""
    v = F(v)
    n = math.floor(v * 1000)
    return "%d.%03d" % (n // 1000, n % 1000)


def rem_dec(a, b):
    """The common mistake: 7 ÷ 3 = 2 r 1 written as 2.1."""
    q, r = divmod(a, b)
    assert r and r < 10
    return "%d.%d" % (q, r)


# ------------------------------------------------------------ pictures
def sector(cx, cy, r, a0, a1, fill, stroke, sw):
    """Pie slice from angle a0 to a1 (degrees, 0 = up, clockwise)."""
    def P(a):
        t = math.radians(a)
        return cx + r * math.sin(t), cy - r * math.cos(t)
    x0, y0 = P(a0)
    x1, y1 = P(a1)
    large = 1 if a1 - a0 > 180 else 0
    return ("<path d='M %.1f %.1f L %.1f %.1f A %d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='%s'/>"
            % (cx, cy, x0, y0, r, r, large, x1, y1, fill, stroke, sw))


def pizzas_svg(n, d, R=28):
    """n pizzas, each cut into d equal slices; one slice of every pizza is shaded (one child's share)."""
    G = 14
    W = n * 2 * R + (n - 1) * G + 8
    H = 2 * R + 8
    o = []
    for i in range(n):
        cx, cy = 4 + R + i * (2 * R + G), 4 + R
        if d == 1:
            o.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (cx, cy, R, FILL, CRUST))
            continue
        for k in range(d):
            o.append(sector(cx, cy, R, 360.0 * k / d, 360.0 * (k + 1) / d, FILL if k == 0 else PIZ, CRUST, 2))
        o.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (cx, cy, R, CRUST))
    return svg_wrap(W, H, "".join(o), "%d pizza%s, each cut into %d equal slices, 1 slice of each shaded"
                    % (n, "" if n == 1 else "s", d))


def cakes_svg(n, d, CW=64, CH=36):
    """n rectangular cakes, each cut into d equal parts; one part of every cake is shaded."""
    G = 12
    W = n * CW + (n - 1) * G + 8
    H = CH + 8
    o = []
    for i in range(n):
        x0, y0 = 4 + i * (CW + G), 4
        o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2.5'/>" % (x0, y0, CW, CH, LINE))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s'/>" % (x0, y0, CW / float(d), CH, FILL))
        for k in range(1, d):
            x = x0 + CW * k / float(d)
            o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.6'/>" % (x, y0, x, y0 + CH, LINE))
        o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x0, y0, CW, CH, LINE))
    return svg_wrap(W, H, "".join(o), "%d cake%s, each cut into %d equal parts, 1 part of each shaded"
                    % (n, "" if n == 1 else "s", d))


def numline_svg(hi, den, dot, W=420):
    """Number line from 0 to hi (whole numbers labelled), every 1/den marked, red dot at the Fraction dot."""
    L, R, Y = 20, W - 20, 26
    parts = hi * den

    def X(i):
        return L + (R - L) * i / float(parts)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for i in range(parts + 1):
        big = i % den == 0
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(i), Y - (13 if big else 8), X(i), Y + (13 if big else 8), LINE, "2.5" if big else "1.8"))
        if big:
            s.append(text(X(i), Y + 34, str(i // den), 17))
    k = F(dot) * den
    assert k.denominator == 1
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(int(k)), Y, RED))
    return svg_wrap(W, Y + 44, "".join(s), "number line from 0 to %d with each whole split into %d equal parts" % (hi, den))


def grid_svg(k, cell=18):
    """10 x 10 hundred square with k squares shaded, full columns first."""
    pad = 4
    w = 10 * cell + 2 * pad
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (pad + c * cell, pad + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad + i * cell, pad, pad + i * cell, pad + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (pad, pad + i * cell, pad + 10 * cell, pad + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (pad, pad, 10 * cell, 10 * cell, LINE))
    return svg_wrap(w, w, "".join(s), "hundred square with %d of 100 squares shaded" % k)


def div_svg(a, b, places, hide=False):
    """Division of a ÷ b written to `places` decimal places, drawn from the real working (remainders carried in red).
    hide=True draws the digits after the decimal point as empty boxes."""
    w = str(a)
    cells = list(w) + ["."] + ["0"] * places
    q, carry, rem = [], {}, 0
    for i, ch in enumerate(cells):
        if ch == ".":
            q.append(".")
            continue
        cur = rem * 10 + int(ch)
        q.append(str(cur // b))
        rem = cur % b
        nxt = i + 1 if i + 1 < len(cells) and cells[i + 1] != "." else i + 2
        if rem and nxt < len(cells):
            carry[nxt] = str(rem)
    qs = "".join(q)
    assert F(Dm(qs)) == F(math.floor(F(a, b) * 10 ** places), 10 ** places), (qs, a, b)
    lead = 0
    while lead < len(w) - 1 and q[lead] == "0":
        lead += 1
    CW, DW = 30, 14
    xs, x = [], 62
    for ch in cells:
        xs.append(x)
        x += DW if ch == "." else CW
    W = x + 10
    ytop, ybar, ydig = 34, 46, 78
    o = []
    for i, ch in enumerate(cells):
        cx = xs[i] + (DW if ch == "." else CW) / 2.0
        if ch == ".":
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ydig - 2, LINE))
            o.append("<circle cx='%.1f' cy='%d' r='3.5' fill='%s'/>" % (cx, ytop - 2, LINE))
            continue
        o.append(text(cx + 3, ydig, ch, 26))
        if i in carry:
            o.append(text(xs[i] + 5, ydig - 14, carry[i], 15, col=RED))
        if i < lead:
            continue
        if hide and i > len(w):
            o.append("<rect x='%.1f' y='%d' width='20' height='24' fill='#fff' stroke='%s' stroke-width='1.8' rx='3'/>"
                     % (cx - 10, ytop - 22, LINE))
        else:
            o.append(text(cx + 3, ytop, q[i], 26))
    o.append("<line x1='54' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (ybar, W - 6, ybar, LINE))
    o.append("<path d='M 54 %d Q 62 %d 54 %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (ybar, ybar + 22, ybar + 44, LINE))
    o.append(text(30, ydig, str(b), 26))
    return svg_wrap(W, ybar + 50, "".join(o), "division of %s by %d" % ("".join(cells), b))


def bar_svg(rows, total=None, q=None, W=300):
    """Bar model. rows: [(name, [(value, label or None), ...])], each pair one box of a bar (drawn to scale).
    total: label of the whole (a bracket above a single bar, a brace on the right of 2 bars).
    q: (row, first box, last box, label) bracket drawn under those boxes."""
    multi = len(rows) > 1
    names = any(n for n, _ in rows)
    X0 = 92 if names else 14
    unit_max = max(sum(v for v, _ in segs) for _, segs in rows)
    sc = W / float(unit_max)
    BH, GAP = 34, 30
    top = 12 if multi or total is None else 40
    o = []
    ys = []
    y = top
    for ri, (name, segs) in enumerate(rows):
        ys.append(y)
        if name:
            o.append(text(X0 - 10, y + BH / 2.0 + 6, name, 16, anchor="end"))
        x = X0
        for v, lab in segs:
            w = v * sc
            o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, w, BH, LIGHT, GREEN))
            if lab:
                o.append(text(x + w / 2.0, y + BH / 2.0 + 6, lab, 15))
            x += w
        y += BH + GAP
    right = X0 + W
    Wsvg = right + 14
    if total is not None and not multi:
        yb = top - 10
        o.append("<path d='M %d %d L %d %d L %d %d L %d %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (X0, yb + 6, X0, yb, right, yb, right, yb + 6, LINE))
        o.append(text((X0 + right) / 2.0, yb - 8, total, 16))
    if total is not None and multi:
        y1, y2 = ys[0], ys[-1] + BH
        xr = max(X0 + sum(v for v, _ in segs) * sc for _, segs in rows) + 10
        o.append("<path d='M %.1f %d L %.1f %d L %.1f %d L %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xr, y1, xr + 8, y1, xr + 8, y2, xr, y2, LINE))
        o.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                 % (xr + 8, (y1 + y2) / 2.0, xr + 14, (y1 + y2) / 2.0, LINE))
        o.append(text(xr + 18, (y1 + y2) / 2.0 + 6, total, 16, anchor="start"))
        Wsvg = int(xr + 18 + 9 * len(total) + 8)
    Hsvg = y - GAP + 8
    if q is not None:
        r, a, b, lab = q
        segs = rows[r][1]
        xa = X0 + sum(v for v, _ in segs[:a]) * sc
        xb = X0 + sum(v for v, _ in segs[:b + 1]) * sc
        yq = ys[r] + BH + 4
        o.append("<path d='M %.1f %d L %.1f %d L %.1f %d L %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, yq, xa, yq + 6, xb, yq + 6, xb, yq, RED))
        o.append(text((xa + xb) / 2.0, yq + 23, lab, 17, col=RED))
        Hsvg = max(Hsvg, yq + 30)
    return svg_wrap(Wsvg, Hsvg, "".join(o), "bar model")


# ============================================================ set 1: a ÷ b = a/b
def set_proper():
    its = []
    its.append(mcq(fig(pizzas_svg(1, 3)) + "1 pizza is shared equally among 3 children. The shaded slice is one child’s share. "
                   "How much pizza does each child get?",
                   fr(1, 3) + " of a pizza", ["3 pizzas", fr(2, 3) + " of a pizza", "0.3 of a pizza"],
                   "1 pizza cut into 3 equal slices: each child gets 1 slice = %s. So 1 ÷ 3 = <b>%s</b>. "
                   "0.3 is not %s: it is %s." % (fr(1, 3), fr(1, 3), fr(1, 3), fr(3, 10)), right_val=F(1, 3)))
    its.append(mcq(fig(pizzas_svg(3, 4)) + "3 pizzas are shared equally among 4 children. The shaded slices are one child’s share. "
                   "How much pizza does each child get?",
                   fr(3, 4) + " of a pizza", [fr(4, 3) + " of a pizza", fr(1, 4) + " of a pizza", fr(1, 3) + " of a pizza"],
                   "Cut each pizza into 4 equal slices. Each child gets 1 slice from each of the 3 pizzas: "
                   "3 quarters = %s. So 3 ÷ 4 = <b>%s</b>, not %s." % (fr(3, 4), fr(3, 4), fr(4, 3)), right_val=F(3, 4)))
    its.append(mcq(fig(pizzas_svg(2, 3)) + "2 pizzas are shared equally among 3 children. How much pizza does each child get?",
                   fr(2, 3) + " of a pizza", [fr(3, 2) + " of a pizza", fr(1, 3) + " of a pizza", fr(2, 5) + " of a pizza"],
                   "Each pizza is cut into 3 equal slices. Each child gets 1 slice of each pizza: 2 thirds = <b>%s</b>. "
                   "2 ÷ 3 = %s. %s counts the slices of only one pizza." % (fr(2, 3), fr(2, 3), fr(1, 3)), right_val=F(2, 3)))
    its.append(mcq(fig(cakes_svg(2, 5)) + "2 cakes are shared equally among 5 friends. The shaded parts are one friend’s share. "
                   "How much cake does each friend get?",
                   fr(2, 5) + " of a cake", [fr(5, 2) + " of a cake", fr(1, 5) + " of a cake", fr(2, 7) + " of a cake"],
                   "Cut each cake into 5 equal parts. Each friend gets 1 part of each of the 2 cakes: 2 fifths = <b>%s</b>. "
                   "Do not add 2 and 5: the denominator is the number of friends." % fr(2, 5), right_val=F(2, 5)))
    its.append(mcq(fig(cakes_svg(4, 5)) + "4 cakes are shared equally among 5 friends. How much cake does each friend get?",
                   fr(4, 5) + " of a cake", [fr(5, 4) + " of a cake", fr(1, 5) + " of a cake", fr(1, 4) + " of a cake"],
                   "Each friend gets 1 fifth of each of the 4 cakes: 4 fifths. 4 ÷ 5 = <b>%s</b>. "
                   "%s is 5 ÷ 4, the wrong way round." % (fr(4, 5), fr(5, 4)), right_val=F(4, 5)))
    its.append(mcq("3 ÷ 5 = ?", fr(3, 5), [fr(5, 3), fr(1, 5), fr(2, 5)],
                   "The number being divided goes on top: 3 ÷ 5 = <b>%s</b>. %s is 5 ÷ 3." % (fr(3, 5), fr(5, 3)),
                   right_val=F(3, 5)))
    its.append(mcq("5 ÷ 8 = ?", fr(5, 8), [fr(8, 5), fr(1, 8), fr(3, 8)],
                   "5 ÷ 8 = <b>%s</b>. The 5 is divided, so it is the numerator. %s comes from 8 − 5." % (fr(5, 8), fr(3, 8)),
                   right_val=F(5, 8)))
    its.append(mcq("1 ÷ 6 = ?", fr(1, 6), ["6", "0.6", "0.16"],
                   "1 whole shared into 6 equal parts: each part is <b>%s</b>. 6 is 6 ÷ 1, and 0.16 just writes the digits." % fr(1, 6),
                   right_val=F(1, 6)))
    its.append(mcq("7 ÷ 10 = ?", fr(7, 10), [fr(10, 7), fr(1, 7), "0.07"],
                   "7 ÷ 10 = <b>%s</b> = 0.7. 0.07 is %s." % (fr(7, 10), fr(7, 100)), right_val=F(7, 10)))
    its.append(mcq("Which division is the same as %s?" % fr(5, 9), "5 ÷ 9", ["9 ÷ 5", "5 × 9", "9 − 5"],
                   "A fraction is a division: numerator ÷ denominator. %s = <b>5 ÷ 9</b>." % fr(5, 9)))
    its.append(mcq("Which fraction is equal to 4 ÷ 7?", fr(4, 7), [fr(7, 4), fr(1, 7), fr(1, 4)],
                   "4 ÷ 7 = <b>%s</b>. Sharing 4 wholes among 7 gives each share 4 sevenths. %s is 7 ÷ 4." % (fr(4, 7), fr(7, 4)),
                   right_val=F(4, 7)))
    its.append(mcq("11 ÷ 12 = ?", fr(11, 12), [fr(12, 11), fr(1, 11), fr(1, 12)],
                   "11 ÷ 12 = <b>%s</b>. 11 is less than 12, so the answer is less than 1." % fr(11, 12), right_val=F(11, 12)))
    its.append(mcq("Find the missing number: 6 ÷ ? = %s" % fr(6, 11), "11", ["6", "5", "17"],
                   "The denominator is the number we divide by: 6 ÷ <b>11</b> = %s." % fr(6, 11), right_val=11))
    its.append(mcq("Find the missing number: ? ÷ 9 = %s" % fr(4, 9), "4", ["9", "36", "5"],
                   "The numerator is the number being divided: <b>4</b> ÷ 9 = %s. 36 is 4 × 9." % fr(4, 9), right_val=4))
    its.append(mcq("Which is <b>not</b> equal to 2 ÷ 3?", fr(3, 2), [fr(2, 3), fr(4, 6), "4 ÷ 6"],
                   "2 ÷ 3 = %s = %s, and 4 ÷ 6 = %s = %s. <b>%s</b> is 3 ÷ 2, which is more than 1."
                   % (fr(2, 3), fr(4, 6), fr(4, 6), fr(2, 3), fr(3, 2)), same_ok=True))
    its.append(mcq("6 ÷ 8 = ? Give the answer in simplest form.", fr(3, 4), [fr(4, 3), fr(3, 8), fr(1, 8)],
                   "6 ÷ 8 = %s. Divide the numerator and the denominator by 2: <b>%s</b>. "
                   "%s divides only the numerator." % (fr(6, 8), fr(3, 4), fr(3, 8)), right_val=F(3, 4)))
    its.append(mcq("4 ÷ 10 = ? Give the answer in simplest form.", fr(2, 5), [fr(5, 2), fr(4, 5), "0.04"],
                   "4 ÷ 10 = %s. Divide the top and the bottom by 2: <b>%s</b>. "
                   "%s divides only the denominator." % (fr(4, 10), fr(2, 5), fr(4, 5)), right_val=F(2, 5)))
    its.append(mcq("8 ÷ 12 = ? Give the answer in simplest form.", fr(2, 3), [fr(3, 2), fr(2, 12), fr(4, 12)],
                   "8 ÷ 12 = %s. Divide the top and the bottom by 4: <b>%s</b>. "
                   "Whatever you divide the numerator by, divide the denominator by the same number." % (fr(8, 12), fr(2, 3)),
                   right_val=F(2, 3)))
    its.append(mcq("Which gives each person <b>more</b>: 2 cakes shared among 5 people, or 2 cakes shared among 3 people?",
                   "Among 3 people", ["Among 5 people", "They get the same", "You cannot tell"],
                   "2 ÷ 5 = %s and 2 ÷ 3 = %s. Thirds are bigger than fifths, so %s &gt; %s. "
                   "Fewer people means a bigger share: <b>among 3 people</b>." % (fr(2, 5), fr(2, 3), fr(2, 3), fr(2, 5))))
    its.append(mcq("Each child gets %s of a pizza. Which sharing gives this?" % fr(3, 8),
                   "3 pizzas among 8 children", ["8 pizzas among 3 children", "3 pizzas among 5 children",
                                                 "1 pizza among 8 children"],
                   "%s = 3 ÷ 8, so <b>3 pizzas are shared among 8 children</b>. 8 pizzas among 3 children gives %s each."
                   % (fr(3, 8), fr(8, 3))))
    assert len(its) == 20, len(its)
    return {"title": "Division as a fraction: 3 ÷ 4 = 3/4", "items": its}


# ============================================================ set 2: improper results as mixed numbers
def div_mixed(a, b, extra_e=""):
    """Question a ÷ b = ? with the mistakes b/a, q.r and q r/a."""
    q, r = divmod(a, b)
    v = F(a, b)
    e = ("%d ÷ %d = %d remainder %d. The remainder %d is still shared among %d, so it is %s. "
         "%d ÷ %d = %s = <b>%s</b>. The remainder is not the decimal .%d." % (a, b, q, r, r, b, fr(r, b), a, b, fr(a, b), mx(v), r))
    return mcq("%d ÷ %d = ? Give the answer as a mixed number." % (a, b), mx(v),
               [fr(b, a), rem_dec(a, b), mixed(q, r, a)], e + extra_e, right_val=v)


def set_mixed():
    its = []
    its.append(mcq(fig(pizzas_svg(5, 2)) + "5 pizzas are shared equally between 2 children. The shaded halves are one child’s share. "
                   "How much pizza does each child get?",
                   mixed(2, 1, 2) + " pizzas", [fr(2, 5) + " of a pizza", "2.1 pizzas", fr(1, 2) + " of a pizza"],
                   "Each child gets 1 half of each of the 5 pizzas: 5 halves = %s = <b>%s</b>. "
                   "5 ÷ 2 = 2 remainder 1, and the 1 pizza left over is cut into halves. It is not 2.1." % (fr(5, 2), mixed(2, 1, 2)),
                   right_val=F(5, 2)))
    its.append(mcq(fig(cakes_svg(5, 4, CW=56, CH=32)) + "5 cakes are shared equally among 4 friends. How much cake does each friend get?",
                   mixed(1, 1, 4) + " cakes", [fr(4, 5) + " of a cake", "1.1 cakes", mixed(1, 1, 5) + " cakes"],
                   "Each friend gets 1 quarter of each of the 5 cakes: 5 quarters = %s = <b>%s</b>. "
                   "%s is 4 ÷ 5." % (fr(5, 4), mixed(1, 1, 4), fr(4, 5)), right_val=F(5, 4)))
    its.append(div_mixed(7, 3))
    its.append(div_mixed(9, 2))
    its.append(div_mixed(13, 5))
    its.append(mcq(fig(numline_svg(3, 4, F(11, 4))) + "Each whole on the number line is split into 4 equal parts. "
                   "The red dot shows 11 ÷ 4. What number is at the red dot?",
                   mixed(2, 3, 4), ["2.3", fr(4, 11), mixed(3, 1, 4)],
                   "Each part is %s. The dot is 11 parts from 0: %s. That is 2 wholes and 3 more parts = <b>%s</b>. "
                   "%s is 1 part after 3, but the dot is 1 part before 3." % (fr(1, 4), fr(11, 4), mixed(2, 3, 4), mixed(3, 1, 4)),
                   right_val=F(11, 4)))
    its.append(div_mixed(17, 6))
    its.append(div_mixed(23, 4))
    its.append(mcq("Write 10 ÷ 3 as an improper fraction.", fr(10, 3), [fr(3, 10), "3.1", fr(7, 3)],
                   "10 ÷ 3 = <b>%s</b> (= %s). %s is 3 ÷ 10, and 3.1 writes the remainder as a decimal." % (fr(10, 3), mixed(3, 1, 3), fr(3, 10)),
                   right_val=F(10, 3)))
    its.append(mcq("Which division has the answer %s?" % mixed(3, 2, 5), "17 ÷ 5", ["32 ÷ 5", "13 ÷ 5", "5 ÷ 17"],
                   "%s = 3 wholes and 2 fifths. 3 × 5 + 2 = 17 fifths, so %s = %s = <b>17 ÷ 5</b>."
                   % (mixed(3, 2, 5), mixed(3, 2, 5), fr(17, 5))))
    its.append(mcq("Which division has the answer %s?" % mixed(4, 1, 3), "13 ÷ 3", ["41 ÷ 3", "12 ÷ 3", "7 ÷ 3"],
                   "4 × 3 + 1 = 13, so %s = %s = <b>13 ÷ 3</b>. 12 ÷ 3 = 4 forgets the remainder." % (mixed(4, 1, 3), fr(13, 3))))
    its.append(mcq("Between which two whole numbers is 19 ÷ 4?", "4 and 5", ["3 and 4", "19 and 20", "0 and 1"],
                   "4 × 4 = 16 and 5 × 4 = 20, so 19 ÷ 4 = %s is <b>between 4 and 5</b>." % mixed(4, 3, 4)))
    its.append(mcq("29 ÷ 5 = 5 remainder 4. Which mixed number is 29 ÷ 5?", mixed(5, 4, 5), ["5.4", mixed(5, 4, 29), fr(4, 5)],
                   "The remainder 4 is shared among 5, so it is %s. 29 ÷ 5 = <b>%s</b>. Do not put the remainder over 29."
                   % (fr(4, 5), mixed(5, 4, 5)), right_val=F(29, 5)))
    its.append(mcq("Find the missing number: ? ÷ 4 = %s" % mixed(3, 3, 4), "15", ["12", "33", "21"],
                   "%s = 3 wholes and 3 quarters. 3 × 4 + 3 = 15, so <b>15</b> ÷ 4 = %s. 12 ÷ 4 is only 3."
                   % (mixed(3, 3, 4), mixed(3, 3, 4)), right_val=15))
    its.append(mcq("Write %s as a division of two whole numbers." % mixed(2, 3, 8), "19 ÷ 8", ["23 ÷ 8", "16 ÷ 8", "8 ÷ 19"],
                   "2 × 8 + 3 = 19, so %s = %s = <b>19 ÷ 8</b>. 23 ÷ 8 just joins the digits 2 and 3." % (mixed(2, 3, 8), fr(19, 8))))
    its.append(mcq("15 ÷ 6 = ? Give the answer in simplest form.", mixed(2, 1, 2), ["2.3", fr(2, 5), mixed(2, 3, 15)],
                   "15 ÷ 6 = 2 remainder 3 = %s. Simplify: %s = %s, so the answer is <b>%s</b>."
                   % (mixed(2, 3, 6), fr(3, 6), fr(1, 2), mixed(2, 1, 2)), right_val=F(5, 2)))
    its.append(mcq("26 ÷ 8 = ? Give the answer in simplest form.", mixed(3, 1, 4), ["3.2", fr(4, 13), mixed(3, 2, 26)],
                   "26 ÷ 8 = 3 remainder 2 = %s. Simplify: %s = %s, so the answer is <b>%s</b>."
                   % (mixed(3, 2, 8), fr(2, 8), fr(1, 4), mixed(3, 1, 4)), right_val=F(13, 4)))
    its.append(mcq("14 ÷ 4 = ? Give the answer in simplest form.", mixed(3, 1, 2), ["3.2", fr(2, 7), mixed(3, 2, 14)],
                   "14 ÷ 4 = 3 remainder 2 = %s = <b>%s</b>. %s is 4 ÷ 14 in simplest form." % (mixed(3, 2, 4), mixed(3, 1, 2), fr(2, 7)),
                   right_val=F(7, 2)))
    its.append(mcq("Which is greater: 9 ÷ 4 or 11 ÷ 5?", "9 ÷ 4", ["11 ÷ 5", "They are equal", "You cannot tell"],
                   "9 ÷ 4 = %s and 11 ÷ 5 = %s. Both have 2 wholes, and %s &gt; %s, so <b>9 ÷ 4</b> is greater."
                   % (mixed(2, 1, 4), mixed(2, 1, 5), fr(1, 4), fr(1, 5))))
    its.append(mcq("Some cakes are shared equally among 3 children. Each child gets %s cakes. How many cakes are there?" % mixed(1, 2, 3),
                   "5", [mixed(3, 2, 3), "6", mixed(4, 2, 3)],
                   "%s = %s, and %s × 3 = %s = <b>5</b> cakes. Check: 5 ÷ 3 = %s. %s multiplies only the whole number."
                   % (mixed(1, 2, 3), fr(5, 3), fr(5, 3), fr(15, 3), mixed(1, 2, 3), mixed(3, 2, 3)), right_val=5))
    # easy -> hard
    order = [0, 1, 2, 3, 4, 8, 5, 6, 7, 12, 11, 9, 10, 14, 13, 15, 17, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Answers greater than 1: 7 ÷ 3 = 2 1/3", "items": its}


# ============================================================ set 3: fractions as decimals
def fd(n, d, right, wrong, e, q=None):
    v = F(n, d)
    assert F(Dm(right)) == v, (n, d, right)
    return mcq(q or ("Write %s as a decimal." % fr(n, d)), right, wrong, e, right_val=v)


def set_decimals():
    its = []
    its.append(fd(1, 4, "0.25", ["0.14", "0.4", "2.5"],
                  "25 of the 100 squares are shaded. %s = %s = <b>0.25</b>. 0.14 just writes the digits 1 and 4." % (fr(1, 4), fr(25, 100)),
                  q=fig(grid_svg(25)) + "The shaded part is %s of the hundred square. Write %s as a decimal." % (fr(1, 4), fr(1, 4))))
    its.append(fd(3, 5, "0.6", ["0.35", "0.06", "0.3"],
                  "60 of the 100 squares are shaded. %s = %s = %s = <b>0.6</b>. 0.06 would be only 6 squares." % (fr(3, 5), fr(6, 10), fr(60, 100)),
                  q=fig(grid_svg(60)) + "The shaded part is %s of the hundred square. Write %s as a decimal." % (fr(3, 5), fr(3, 5))))
    its.append(fd(1, 2, "0.5", ["0.12", "1.2", "0.2"],
                  "%s = %s = <b>0.5</b>. (1 ÷ 2 = 0.5.) 0.12 just writes the digits." % (fr(1, 2), fr(5, 10))))
    its.append(fd(7, 10, "0.7", ["0.07", "7.1", "0.17"],
                  "%s is 7 tenths = <b>0.7</b>. 0.07 is 7 hundredths." % fr(7, 10)))
    its.append(fd(37, 100, "0.37", ["3.7", "0.037", "37"],
                  "%s is 37 hundredths. Hundredths are the second place after the decimal point: <b>0.37</b>." % fr(37, 100)))
    its.append(fd(2, 5, "0.4", ["0.25", "2.5", "0.2"],
                  "Make the denominator 10: %s = %s = <b>0.4</b>. 2.5 is 5 ÷ 2, the wrong way round." % (fr(2, 5), fr(4, 10))))
    its.append(fd(3, 4, "0.75", ["0.34", "0.25", "1.33"],
                  "Make the denominator 100: %s = %s = <b>0.75</b>. 0.34 just writes the digits 3 and 4." % (fr(3, 4), fr(75, 100))))
    its.append(fd(9, 20, "0.45", ["0.92", "0.9", "4.5"],
                  "20 × 5 = 100, so multiply the top by 5 too: %s = %s = <b>0.45</b>." % (fr(9, 20), fr(45, 100))))
    its.append(fd(6, 25, "0.24", ["0.625", "0.6", "2.4"],
                  "25 × 4 = 100, so %s = %s = <b>0.24</b>. 0.625 just writes the digits." % (fr(6, 25), fr(24, 100))))
    its.append(fd(1, 8, "0.125", ["0.8", "0.18", "1.8"],
                  "1 ÷ 8: 10 ÷ 8 = 1 r 2, 20 ÷ 8 = 2 r 4, 40 ÷ 8 = 5. So %s = <b>0.125</b>. "
                  "0.8 is %s, not %s." % (fr(1, 8), fr(8, 10), fr(1, 8))))
    its.append(fd(3, 8, "0.375", ["0.38", "3.8", "0.83"],
                  "30 ÷ 8 = 3 r 6, 60 ÷ 8 = 7 r 4, 40 ÷ 8 = 5. So 3 ÷ 8 = <b>0.375</b>. Keep dividing until nothing is left.",
                  q=fig(div_svg(3, 8, 3, hide=True)) + "The working shows 3 ÷ 8. What is %s as a decimal?" % fr(3, 8)))
    its.append(fd(7, 4, "1.75", ["1.3", "0.57", "7.4"],
                  "7 ÷ 4 = 1 remainder 3. The 3 left over is %s = 0.75. So 7 ÷ 4 = <b>1.75</b>. "
                  "1.3 writes the remainder as a decimal." % fr(3, 4), q="7 ÷ 4 = ? Give the answer as a decimal."))
    its.append(fd(9, 5, "1.8", ["1.4", "0.56", "9.5"],
                  "9 ÷ 5 = 1 remainder 4, and %s = %s = 0.8. So 9 ÷ 5 = <b>1.8</b>, not 1.4." % (fr(4, 5), fr(8, 10)),
                  q="9 ÷ 5 = ? Give the answer as a decimal."))
    its.append(fd(11, 4, "2.75", ["2.34", "2.25", "0.75"],
                  "The 2 wholes stay. %s = 0.75, so %s = <b>2.75</b>." % (fr(3, 4), mixed(2, 3, 4)),
                  q="Write %s as a decimal." % mixed(2, 3, 4)))
    its.append(fd(27, 20, "1.35", ["1.72", "1.7", "0.35"],
                  "%s = %s = 0.35, so %s = <b>1.35</b>. 1.72 just writes the digits." % (fr(7, 20), fr(35, 100), mixed(1, 7, 20)),
                  q="Write %s as a decimal." % mixed(1, 7, 20)))
    its.append(fd(13, 8, "1.625", ["1.38", "1.5", "0.625"],
                  "13 ÷ 8 = 1 remainder 5, and %s = 5 ÷ 8 = 0.625. So %s = <b>1.625</b>. 1.5 writes the remainder as a decimal."
                  % (fr(5, 8), fr(13, 8))))
    its.append(fd(3, 20, "0.15", ["0.32", "6.67", "1.5"],
                  "3 ÷ 20 = %s = %s = <b>0.15</b>. 6.67 is about 20 ÷ 3, the wrong way round." % (fr(3, 20), fr(15, 100)),
                  q="3 ÷ 20 = ? Give the answer as a decimal."))
    its.append(mcq("Which fraction is equal to 0.6?", fr(3, 5), [fr(1, 6), fr(6, 100), fr(2, 3)],
                   "0.6 = %s = <b>%s</b> (divide the top and the bottom by 2). %s = 0.06." % (fr(6, 10), fr(3, 5), fr(6, 100)),
                   right_val=F(3, 5)))
    its.append(mcq("Which fraction is equal to 0.08?", fr(2, 25), [fr(4, 5), fr(1, 8), fr(8, 1000)],
                   "0.08 = 8 hundredths = %s = <b>%s</b> (divide by 4). %s = 0.8." % (fr(8, 100), fr(2, 25), fr(4, 5)),
                   right_val=F(2, 25)))
    its.append(mcq("Which is the <b>greatest</b>?", fr(5, 8), [fr(3, 5), "0.55", "0.59"],
                   "Change to decimals: %s = 0.625, %s = 0.6, 0.55 and 0.59. The greatest is <b>%s</b>." % (fr(5, 8), fr(3, 5), fr(5, 8))))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 9, 10, 18, 11, 12, 16, 13, 14, 15, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Fractions as decimals", "items": its}


# ============================================================ set 4: correct to 2 decimal places
def r2(n, d, wrong, e, q=None):
    v = F(n, d)
    right = dp2(v)
    for w in wrong:
        assert w != right
    exact = (Dm(v.numerator) / Dm(v.denominator)).quantize(Dm("0.0001")) == Dm(v.numerator) / Dm(v.denominator)
    shown = dec(v) + "." if exact else dp3_cut(v) + "…"
    return mcq(q or ("Write %s as a decimal correct to 2 decimal places." % fr(n, d)), right, wrong,
               "%d ÷ %d = %s " % (n, d, shown) + e)


def set_rounding():
    its = []
    its.append(r2(1, 3, ["0.3", "0.13", "3"],
                  "The 3rd decimal place is 3, which is less than 5, so round down: <b>0.33</b>. 0.3 has only 1 decimal place."))
    its.append(mcq(fig(div_svg(2, 3, 3)) + "The working shows 2 ÷ 3 to 3 decimal places. What is %s correct to 2 decimal places?" % fr(2, 3),
                   "0.67", ["0.66", "0.23", "1.5"],
                   "2 ÷ 3 = 0.666… The 3rd decimal place is 6, which is 5 or more, so round up: <b>0.67</b>. "
                   "0.66 cuts off the digits without rounding."))
    its.append(r2(1, 6, ["0.16", "0.6", "6"],
                  "Look at the 3rd decimal place: 6 is 5 or more, so round up: <b>0.17</b>. 0.16 forgets to round."))
    its.append(r2(3, 8, ["0.37", "0.83", "0.4"],
                  "The 3rd decimal place is 5, so round up: <b>0.38</b>. "
                  "0.4 is correct to only 1 decimal place."))
    its.append(r2(7, 8, ["0.87", "0.78", "0.9"],
                  "The 3rd decimal place is 5, so round up: <b>0.88</b>."))
    its.append(r2(5, 6, ["0.56", "1.2", "0.8"],
                  "The 3rd decimal place is 3, so the 2nd place stays: <b>0.83</b>. 1.2 is 6 ÷ 5, the wrong way round."))
    its.append(r2(1, 7, ["0.17", "0.15", "7"],
                  "The 3rd decimal place is 2, which is less than 5, so round down: <b>0.14</b>. 0.17 just writes the digits."))
    its.append(r2(5, 7, ["0.57", "1.4", "0.72"],
                  "The 3rd decimal place is 4, which is less than 5, so round down: <b>0.71</b>. 1.4 is 7 ÷ 5."))
    its.append(r2(4, 9, ["0.49", "0.45", "2.25"],
                  "The 4s go on for ever. The 3rd decimal place is 4, so round down: <b>0.44</b>."))
    its.append(r2(5, 9, ["0.55", "1.8", "0.59"],
                  "The 5s go on for ever. The 3rd decimal place is 5, so round up: <b>0.56</b>. 0.55 forgets to round."))
    its.append(r2(2, 7, ["0.28", "3.5", "0.3"],
                  "The 3rd decimal place is 5, so round up: <b>0.29</b>. 3.5 is 7 ÷ 2, the wrong way round."))
    its.append(r2(7, 12, ["0.59", "1.71", "0.6"],
                  "The 3rd decimal place is 3, so round down: <b>0.58</b>. 0.6 is correct to only 1 decimal place."))
    its.append(r2(1, 16, ["0.16", "0.07", "0.6"],
                  "The 3rd decimal place is 2, so round down: <b>0.06</b>. 0.16 just writes the digits."))
    its.append(r2(10, 3, ["3.1", "0.3", "3.34"],
                  "The remainder 1 is not .1: keep dividing. The 3rd decimal place is 3, so round down: <b>3.33</b>.",
                  q="Find the value of 10 ÷ 3 correct to 2 decimal places."))
    its.append(r2(17, 6, ["2.5", "2.84", "0.35"],
                  "The 3rd decimal place is 3, so round down: <b>2.83</b>. 2.5 writes the remainder 5 as a decimal.",
                  q="Find the value of 17 ÷ 6 correct to 2 decimal places."))
    its.append(r2(25, 7, ["3.4", "3.58", "0.28"],
                  "The 3rd decimal place is 1, so round down: <b>3.57</b>. 3.4 writes the remainder 4 as a decimal, and 0.28 is 7 ÷ 25.",
                  q="Find the value of 25 ÷ 7 correct to 2 decimal places."))
    its.append(r2(23, 9, ["2.59", "2.55", "2.6"],
                  "The 3rd decimal place is 5, so round up: <b>2.56</b>. 2.59 just writes the digits.",
                  q="Write %s as a decimal correct to 2 decimal places." % mixed(2, 5, 9)))
    its.append(r2(11, 6, ["1.5", "0.55", "1.8"],
                  "The 3rd decimal place is 3, so round down: <b>1.83</b>. 1.5 writes the remainder 5 as a decimal, and 0.55 is 6 ÷ 11."))
    its.append(mcq("Which fraction is <b>0.43</b> when written as a decimal correct to 2 decimal places?", fr(3, 7),
                   [fr(4, 9), fr(2, 5), fr(4, 3)],
                   "%s = 3 ÷ 7 = 0.428… ≈ <b>0.43</b>. %s ≈ 0.44, %s = 0.4 and %s ≈ 1.33."
                   % (fr(3, 7), fr(4, 9), fr(2, 5), fr(4, 3))))
    its.append(mcq("Siti wrote: %s = 0.66 (correct to 2 decimal places). What did she do wrong?" % fr(2, 3),
                   "She did not round up", ["She divided 3 by 2", "She should write 0.6", "She made no mistake"],
                   "2 ÷ 3 = 0.666… The 3rd decimal place is 6, which is 5 or more, so the answer rounds up to 0.67. "
                   "<b>She did not round up.</b>"))
    assert dp2(F(3, 7)) == "0.43" and dp2(F(4, 9)) == "0.44"
    order = [0, 1, 2, 6, 7, 5, 8, 9, 10, 11, 3, 4, 12, 19, 13, 14, 15, 16, 17, 18]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Fractions as decimals correct to 2 decimal places", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    its.append(mcq(fig(bar_svg([("", [(1, None), (1, None), (1, None), (1, None)])], total="9 m", q=(0, 0, 0, "?"))) +
                   "Mrs Lim cuts a 9 m ribbon into 4 equal pieces. How long is each piece?",
                   mixed(2, 1, 4) + " m", [fr(4, 9) + " m", "2.1 m", mixed(2, 1, 9) + " m"],
                   "4 units = 9 m, so 1 unit = 9 ÷ 4 = %s m = <b>%s m</b>. 9 ÷ 4 = 2 remainder 1, and the 1 m left over is "
                   "cut into quarters, so it is not 2.1 m." % (fr(9, 4), mixed(2, 1, 4)), right_val=F(9, 4)))
    its.append(mcq("Ali pours 3 ℓ of water equally into 4 bottles. How much water is in each bottle?",
                   fr(3, 4) + " ℓ", [fr(4, 3) + " ℓ", fr(1, 4) + " ℓ", fr(1, 3) + " ℓ"],
                   "3 ℓ shared among 4 bottles: 3 ÷ 4 = <b>%s ℓ</b>. %s ℓ would be 4 ℓ in 3 bottles." % (fr(3, 4), fr(4, 3)),
                   right_val=F(3, 4)))
    its.append(mcq("Mdm Wong packs 2 kg of rice equally into 5 bags. How much rice is in each bag?",
                   "0.4 kg", ["2.5 kg", "0.25 kg", "0.04 kg"],
                   "2 ÷ 5 = %s = %s = <b>0.4 kg</b>. 2.5 kg is 5 ÷ 2, the wrong way round." % (fr(2, 5), fr(4, 10)),
                   right_val=F(2, 5)))
    its.append(mcq(fig(bar_svg([("", [(1, None), (1, None), (1, None), (1, None)])], total="$18", q=(0, 0, 0, "?"))) +
                   "Mr Kumar paid $18 for 4 bowls of laksa. Each bowl cost the same. How much did one bowl cost?",
                   "$4.50", ["$4.20", "$0.22", "$14"],
                   "4 units = $18, so 1 unit = $18 ÷ 4 = $%s = <b>$4.50</b>. 18 ÷ 4 = 4 remainder 2, and the $2 left over "
                   "is $0.50 for each bowl, not 20¢." % mixed(4, 1, 2), right_val=F(9, 2)))
    its.append(mcq("Hui Min runs 4 rounds of the school track and covers 3 km. How long is one round?",
                   "0.75 km", ["1.33 km", "0.34 km", "0.25 km"],
                   "3 ÷ 4 = %s km = <b>0.75 km</b>. 1.33 km is about 4 ÷ 3, the wrong way round." % fr(3, 4), right_val=F(3, 4)))
    its.append(mcq("A 2 ℓ bottle of soya bean milk is poured equally into 8 cups. How much milk is in each cup?",
                   "250 ml", ["25 ml", "400 ml", "2500 ml"],
                   "2 ÷ 8 = %s ℓ. 1 ℓ = 1000 ml, so %s ℓ = 1000 ÷ 4 = <b>250 ml</b>. 25 ml forgets that 1 ℓ is 1000 ml."
                   % (fr(1, 4), fr(1, 4)), right_val=250))
    its.append(mcq(fig(bar_svg([("Raju", [(1, None), (1, None), (1, None)]), ("Arjun", [(1, None)])], total="10 m",
                               q=(1, 0, 0, "?"))) +
                   "Raju’s rope is 3 times as long as Arjun’s rope. The two ropes are 10 m long altogether. "
                   "How long is Arjun’s rope?",
                   mixed(2, 1, 2) + " m", [mixed(3, 1, 3) + " m", "2.2 m", mixed(7, 1, 2) + " m"],
                   "4 units = 10 m, so 1 unit = 10 ÷ 4 = %s m = <b>%s m</b>. Arjun has 1 unit. "
                   "%s m is 10 ÷ 3: the model has 4 units, not 3." % (fr(10, 4), mixed(2, 1, 2), mixed(3, 1, 3)),
                   right_val=F(5, 2)))
    its.append(mcq("8 pizzas are shared equally among 6 children. How much pizza does each child get?",
                   mixed(1, 1, 3) + " pizzas", [fr(3, 4) + " of a pizza", "1.2 pizzas", mixed(1, 2, 8) + " pizzas"],
                   "8 ÷ 6 = 1 remainder 2 = %s = <b>%s</b>. Put the remainder over 6, the number of children, not over 8."
                   % (mixed(1, 2, 6), mixed(1, 1, 3)), right_val=F(4, 3)))
    its.append(mcq("A baker uses 7 kg of flour for 8 equal batches of curry puffs. How much flour is in each batch?",
                   fr(7, 8) + " kg", [mixed(1, 1, 7) + " kg", fr(1, 8) + " kg", "0.78 kg"],
                   "7 ÷ 8 = <b>%s kg</b> (= 0.875 kg). %s kg is 8 ÷ 7, the wrong way round." % (fr(7, 8), mixed(1, 1, 7)),
                   right_val=F(7, 8)))
    its.append(mcq(fig(bar_svg([("", [(1, "1 kg"), (4.0 / 3, None), (4.0 / 3, None), (4.0 / 3, None)])], total="5 kg",
                               q=(0, 1, 1, "?"))) +
                   "Mrs Ng bought 5 kg of sugar. She used 1 kg and packed the rest equally into 3 containers. "
                   "How much sugar is in each container?",
                   mixed(1, 1, 3) + " kg", [mixed(1, 2, 3) + " kg", "1.1 kg", fr(3, 4) + " kg"],
                   "5 kg − 1 kg = 4 kg. 3 units = 4 kg, so 1 unit = 4 ÷ 3 = <b>%s kg</b>. "
                   "%s kg shares all 5 kg and forgets the 1 kg used." % (mixed(1, 1, 3), mixed(1, 2, 3)), right_val=F(4, 3)))
    its.append(mcq("7 durians are shared equally among 4 families. How many durians does each family get?",
                   mixed(1, 3, 4), [fr(4, 7), "1.3", mixed(1, 3, 7)],
                   "7 ÷ 4 = 1 remainder 3 = <b>%s</b> durians. The 3 left over are shared among 4 families, so %s each."
                   % (mixed(1, 3, 4), fr(3, 4)), right_val=F(7, 4)))
    its.append(mcq("8 friends share the cost of a $50 birthday cake equally. How much does each friend pay?",
                   "$6.25", ["$6.20", "$0.16", "$42"],
                   "$50 ÷ 8 = 6 remainder 2 = $%s = <b>$6.25</b>. The $2 left over is 25¢ each, not 20¢." % mixed(6, 1, 4),
                   right_val=F(25, 4)))
    its.append(mcq(fig(bar_svg([("Xin Yi", [(3.5, None), (2, "2 ℓ")]), ("Mei Ling", [(3.5, None)])], total="9 ℓ",
                               q=(1, 0, 0, "?"))) +
                   "Xin Yi and Mei Ling have 9 ℓ of water altogether. Xin Yi has 2 ℓ more than Mei Ling. "
                   "How much water does Mei Ling have?",
                   mixed(3, 1, 2) + " ℓ", [mixed(5, 1, 2) + " ℓ", mixed(4, 1, 2) + " ℓ", "3.1 ℓ"],
                   "Take away the extra 2 ℓ: 9 − 2 = 7 ℓ. 2 units = 7 ℓ, so 1 unit = 7 ÷ 2 = <b>%s ℓ</b>. "
                   "%s ℓ is Xin Yi’s share, and %s ℓ forgets the extra 2 ℓ." % (mixed(3, 1, 2), mixed(5, 1, 2), mixed(4, 1, 2)),
                   right_val=F(7, 2)))
    its.append(mcq("Farah cuts 3 m of cloth into 8 equal pieces. How long is each piece in centimetres?",
                   "37.5 cm", ["3.75 cm", "375 cm", "0.375 cm"],
                   "3 ÷ 8 = %s m = 0.375 m. 1 m = 100 cm, so 0.375 m = <b>37.5 cm</b>." % fr(3, 8), right_val=F(75, 2)))
    its.append(mcq("Sarah’s mother divides 3 kg of prawns equally into 4 bags. How many grams of prawns are in each bag?",
                   "750 g", ["75 g", "1333 g", "250 g"],
                   "3 ÷ 4 = %s kg = 0.75 kg. 1 kg = 1000 g, so 0.75 kg = <b>750 g</b>. 250 g is only %s kg." % (fr(3, 4), fr(1, 4)),
                   right_val=750))
    its.append(mcq("Each child gets %s of a pizza. There are 12 children. How many pizzas are there?" % fr(3, 4),
                   "9", ["16", "3", "12"],
                   "Each child gets 3 quarters, so 12 children get 12 × 3 = 36 quarters. 36 ÷ 4 = <b>9</b> pizzas. "
                   "Check: 9 ÷ 12 = %s = %s." % (fr(9, 12), fr(3, 4)), right_val=9))
    its.append(mcq(fig(bar_svg([("", [(1, None), (1, None), (1, None), (1, None), (1, None)])], total="4 ℓ",
                               q=(0, 2, 4, "?"))) +
                   "Kavya pours 4 ℓ of juice equally into 5 jugs. She serves 2 jugs to her guests. "
                   "How much juice is left in the other jugs?",
                   "2.4 ℓ", ["1.6 ℓ", "2 ℓ", "0.8 ℓ"],
                   "5 units = 4 ℓ, so 1 unit = 4 ÷ 5 = 0.8 ℓ. 3 jugs are left: 3 × 0.8 = <b>2.4 ℓ</b>. "
                   "1.6 ℓ is the 2 jugs she served.", right_val=F(12, 5)))
    its.append(mcq("Mr Tan cuts a 10 m plank into 7 equal pieces. How long is each piece, correct to 2 decimal places?",
                   "1.43 m", ["1.42 m", "1.3 m", "0.7 m"],
                   "10 ÷ 7 = 1.428… m. The 3rd decimal place is 8, so round up: <b>1.43 m</b>. "
                   "1.3 m writes the remainder 3 as a decimal."))
    its.append(mcq("Wei Ming cycles 5 km in 3 equal laps at East Coast Park. How long is one lap, correct to 2 decimal places?",
                   "1.67 km", ["1.66 km", "1.2 km", "0.6 km"],
                   "5 ÷ 3 = 1.666… km. The 3rd decimal place is 6, so round up: <b>1.67 km</b>. 0.6 km is 3 ÷ 5."))
    its.append(mcq("Mrs Lim shares 4 cakes equally among 5 tables at a party. At each table, the cake is shared equally "
                   "among 4 children. What fraction of a cake does each child get?",
                   fr(1, 5), [fr(4, 5), fr(1, 20), mixed(1, 1, 4)],
                   "There are 5 × 4 = 20 children. 4 cakes shared among 20 children: 4 ÷ 20 = %s = <b>%s</b> of a cake. "
                   "%s is the share of one table, and %s forgets that there are 4 cakes." % (fr(4, 20), fr(1, 5), fr(4, 5), fr(1, 20)),
                   right_val=F(1, 5)))
    assert dp2(F(10, 7)) == "1.43" and dp2(F(5, 3)) == "1.67"
    order = [1, 2, 0, 4, 5, 3, 7, 8, 10, 13, 14, 11, 6, 9, 12, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f_piz = pizzas_svg(3, 4)
    f_line = numline_svg(3, 3, F(7, 3))
    f_div = div_svg(3, 8, 3)
    f_div2 = div_svg(2, 3, 3)
    f_bar = bar_svg([("", [(1, None), (1, None), (1, None), (1, None)])], total="9 m", q=(0, 0, 0, "?"))
    return (
        "<h2>A division is a fraction</h2>"
        "<p>When a whole number is divided by a whole number, the answer can be a fraction. "
        "The number being divided is the <b>numerator</b>. The number we divide by is the <b>denominator</b>.</p>"
        "<p><b>3 ÷ 4 = " + fr(3, 4) + "</b></p>"
        "<figure class='sn-fig'>" + f_piz +
        "<figcaption>3 pizzas shared equally among 4 children. Cut each pizza into 4 equal slices. "
        "Each child gets 1 slice of each pizza: 3 quarters = " + fr(3, 4) + ".</figcaption></figure>"
        "<h2>Answers greater than 1</h2>"
        "<p>If the number being divided is bigger, the answer is more than 1. Write it as a mixed number. "
        "The remainder is shared too, so it goes over the number we divide by.</p>"
        + ex("Example", "7 ÷ 3 = ?",
             "7 ÷ 3 = 2 remainder 1. The 1 left over is shared among 3, so it is " + fr(1, 3) + ". "
             "7 ÷ 3 = " + fr(7, 3) + " = " + mixed(2, 1, 3) + ".",
             mixed(2, 1, 3))
        + "<figure class='sn-fig'>" + f_line +
        "<figcaption>Each whole is split into thirds. 7 thirds is 2 wholes and 1 more third: " + mixed(2, 1, 3) + ".</figcaption></figure>"
        "<h2>Fractions as decimals</h2>"
        "<p>If the denominator goes into 10 or 100, make an equivalent fraction. "
        "Otherwise, divide the numerator by the denominator.</p>"
        + ex("Example", "Write " + fr(9, 20) + " as a decimal.",
             "20 × 5 = 100, so multiply the top by 5 too: " + fr(9, 20) + " = " + fr(45, 100) + ".", "0.45")
        + "<figure class='sn-fig'>" + f_div +
        "<figcaption>3 ÷ 8: 30 ÷ 8 = 3 r 6, 60 ÷ 8 = 7 r 4, 40 ÷ 8 = 5. So " + fr(3, 8) + " = 0.375.</figcaption></figure>"
        + table(["Fraction", fr(1, 2), fr(1, 4), fr(3, 4), fr(1, 5), fr(1, 8), fr(1, 10), fr(1, 20), fr(1, 25)],
                [["Decimal", "0.5", "0.25", "0.75", "0.2", "0.125", "0.1", "0.05", "0.04"]])
        + "<h2>Correct to 2 decimal places</h2>"
        "<p>Some divisions never end. Divide to <b>3 decimal places</b>, then look at the 3rd digit. "
        "If it is 5 or more, round up. If it is less than 5, round down.</p>"
        "<figure class='sn-fig'>" + f_div2 +
        "<figcaption>2 ÷ 3 = 0.666… The 3rd decimal place is 6, so " + fr(2, 3) + " ≈ 0.67 (correct to 2 decimal places).</figcaption></figure>"
        "<h2>Word problems with a model</h2>"
        + "<figure class='sn-fig'>" + f_bar +
        "<figcaption>A 9 m ribbon is cut into 4 equal pieces. 4 units = 9 m, so 1 unit = 9 ÷ 4 = " + mixed(2, 1, 4) +
        " m = 2.25 m.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 ÷ 4 = " + fr(4, 3), "The number being divided goes on top: 3 ÷ 4 = " + fr(3, 4)],
            ["7 ÷ 3 = 2 r 1 = 2.1", "The remainder is shared too: " + mixed(2, 1, 3) + " ≈ 2.33"],
            ["7 ÷ 3 = " + mixed(2, 1, 7), "Put the remainder over 3, the number you divide by"],
            [fr(1, 8) + " = 0.8", "Divide: 1 ÷ 8 = 0.125"],
            [fr(2, 3) + " = 0.66 (2 d.p.)", "Look at the 3rd place: 0.666… rounds up to 0.67"],
        ])
    )


FAQ = [
    {"q": "What is taught in P5 fractions and division?",
     "a": "Primary 5 students learn that dividing one whole number by another gives a fraction, such as 3 ÷ 4 = 3/4 and 7 ÷ 3 = 2 1/3. They also write fractions as decimals, such as 3/8 = 0.375, and give answers correct to 2 decimal places."},
    {"q": "How do I explain 3 ÷ 4 = 3/4 to my child?",
     "a": "Share 3 pizzas among 4 people: cut every pizza into quarters and give each person 1 quarter of each pizza, so each person gets 3 quarters. Drawing the pizzas or a bar model makes the idea easy to see."},
    {"q": "What is the most common mistake in fractions and division?",
     "a": "Writing the remainder as a decimal, such as 7 ÷ 3 = 2.1. The remainder 1 is shared among 3 too, so 7 ÷ 3 = 2 1/3, which is about 2.33. Turning the fraction upside down (3 ÷ 4 = 4/3) is the other common slip."},
    {"q": "Is fractions and division in the MOE Primary 5 syllabus?",
     "a": "Yes. The 2021 MOE Primary Mathematics syllabus for Primary 5 includes dividing a whole number by a whole number with the quotient as a fraction, and expressing fractions as decimals. These skills are used again in Primary 6 and the PSLE."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (rows of pizzas and cakes, number lines, bar models, hundred squares)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(65804)
    sets = [set_proper(), set_mixed(), set_decimals(), set_rounding(), set_problems()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-5", "slug": "fractions-and-division", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 5 Fractions and Division",
        "seo_title": "P5 Fractions and Division Worksheets: Free Primary 5 Maths with Answers (MOE Syllabus)",
        "short_title": "Fractions and division",
        "domain": "Number and Algebra",
        "standard_code": "Primary 5: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Dividing a whole number by a whole number with quotient as a fraction; expressing fractions as decimals",
        "meta_desc": "Free P5 maths practice: 3 ÷ 4 = 3/4, 7 ÷ 3 = 2 1/3, fractions as decimals, rounding to 2 decimal places and bar model problems. 100 questions with answers.",
        "key_big": "A division is a fraction: 3 ÷ 4 = 3/4.",
        "key_sub": "7 ÷ 3 = 2 remainder 1 = 2 1/3 (not 2.1), and 3/8 = 3 ÷ 8 = 0.375.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(pizza|cake|number line|bar model|hundred square)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
