# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Decimals (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p4_decimals.py
Decimals up to 3 decimal places: place values (place value charts, hundred squares, number lines),
comparing and ordering, decimals as fractions in simplest form, fractions as decimals (denominator a factor
of 10 or 100), rounding to the nearest whole number, 1 decimal place and 2 decimal places,
then decimals in money and measurement with bar models.
Every answer is checked with fractions.Fraction / decimal.Decimal (never float).
Wrong answers are real student mistakes: 0.45 > 0.5 because 45 > 5, 0.3 = 3/100, dropping a place-holding zero,
rounding the wrong place or rounding twice, 1/4 = 0.4, 1/5 = 0.15, $3.05 = 3 dollars 50 cents.
Singapore style: British spelling, ℓ and ml, $ and ¢. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP, ROUND_FLOOR
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
NB = " "
FILL = "#4fae74"
INK = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
BLUE = "#2f6fb5"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
WATER = "#9fd3f2"
WATER_LINE = "#2a7fb8"
WOOD = "#f6e7b0"
COIN = "#e9d48a"
SILVER = "#d9dde2"
FONT = "Arial, Helvetica, sans-serif"


# ------------------------------------------------------------ helpers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mx(w, a, b):
    """Mixed number 4 2/25."""
    return "%d %s" % (w, fr(a, b))


def V(s):
    return F(Dm(s.replace(NB, "")))


def rnd_to(s, places):
    """Round decimal string s (half up) to `places` decimal places; keeps the places (4.0, 2.40)."""
    q = Dm(1).scaleb(-places)
    return str(Dm(s).quantize(q, rounding=ROUND_HALF_UP))


FRX = re.compile(r"^(?:(\d+) )?<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>( .+)?$")
NUM = re.compile(r"^(\$)?(\d*\.?\d+)(¢)?( .+)?$")


def val(c):
    """(value, unit) of a choice. None for choices that are not one number."""
    c = c.replace(NB, "")
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


def mcq(q, correct, wrong, e, same_ok=False, want=None):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (0.3 vs 0.30).
    want: the true value of the answer (Fraction / str); checked against the correct choice."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(re.sub(r"<[^>]+>", "", x) for x in ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        assert all(v is not None for v in vs), (q, ch)
        assert len(set(vs)) == 4, (q, ch)
        assert len({v[1] for v in vs}) == 1, (q, ch)
    if want is not None:
        w = want if isinstance(want, F) else V(str(want))
        assert val(correct)[0] == w, (q, correct, want)
    return {"q": q, "c": ch, "a": 0, "e": e}


def fixed(q, choices, a, e):
    """Choices are picture labels (A, B, C, D): keep this order; the answer position is fixed."""
    assert len(set(choices)) == 4
    return {"q": q, "c": list(choices), "a": a, "e": e, "fix": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fix"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.get("fix"):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fix", None)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "ℓl1i":
            w += 0.45
        elif ch in "mW×÷?":
            w += 0.85
        else:
            w += 0.6
    return w * fs


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def T(v):
    """Decimal text for v thousandths without trailing zeros: 300 -> '0.3', 247 -> '0.247'."""
    s = format((Dm(v) / 1000).normalize(), "f")
    assert F(Dm(s)) == F(v, 1000)
    return s


# ------------------------------------------------------------ figure: hundred squares
def grid_body(k, ox, oy, cell):
    """10 x 10 hundred square at (ox, oy) with k small squares shaded: full columns first."""
    assert 0 <= k <= 100
    s = []
    for c in range(10):
        for r in range(10):
            if c * 10 + r < k:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox + c * cell, oy + r * cell, cell, cell, FILL))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, INK))
    return "".join(s)


def grid_svg(k, cell=18):
    pad = 4
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, grid_body(k, pad, pad, cell),
                    "hundred square with %s shaded" % ("1 small square" if k == 1 else "%d small squares" % k))


def two_grids(k1, l1, k2, l2):
    """Two hundred squares side by side, labelled under them."""
    return svg_wrap(452, 222, "".join([
        grid_body(k1, 6, 6, 18), text(96, 214, l1, 18),
        grid_body(k2, 266, 6, 18), text(356, 214, l2, 18),
    ]), "two hundred squares compared: %d small squares shaded for %s and %d shaded for %s" % (k1, l1, k2, l2))


# ------------------------------------------------------------ figure: place value chart
PV = [(1, "Tens"), (0, "Ones"), (-1, "Tenths"), (-2, "Hundredths"), (-3, "Thousandths")]
NAMES = {1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


def chart_svg(s_, hi=None):
    """Place value chart: (Tens) | Ones | . | Tenths | Hundredths | Thousandths. hi = place drawn in red."""
    w, _, f = s_.partition(".")
    assert len(w) <= 2 and len(f) <= 3
    cols = PV if len(w) > 1 else PV[1:]
    CW, PW, HEAD, ROW = 104, 16, 30, 44
    x0, y0 = 6, 6
    W = 2 * x0 + len(cols) * CW + PW
    H = 2 * y0 + HEAD + ROW
    xs, x = {}, x0
    for p, _ in cols:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0, y0, W - 2 * x0, HEAD + ROW, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, HEADFILL)]
    for p, name in cols:
        if p != cols[0][0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW, GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, name, 14, col=GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW, GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    digits = {}
    for j, ch in enumerate(w):
        digits[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        digits[-(j + 1)] = ch
    for p, ch in digits.items():
        o.append(text(xs[p] + CW / 2.0, y0 + HEAD + 32, ch, 28, col=RED if hi == p else INK, weight=800))
    if f:
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, y0 + HEAD + 31, INK))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % s_)


# ------------------------------------------------------------ figure: number line (values in thousandths)
def line_svg(a, b, spaces, labels=None, dots=(), W=440):
    """Number line from a to b thousandths with `spaces` equal spaces.
    labels: values written under the line (on a tick). dots: (value, letter or None)."""
    labels = labels if labels is not None else [a, b]
    lettered = any(l for _, l in dots)
    L, R = 34, W - 34
    Y = 46 if lettered else 30
    assert (b - a) % spaces == 0
    step = (b - a) // spaces

    def X(v):
        return L + (R - L) * (v - a) / float(b - a)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, INK)]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in labels
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), INK, "2.5" if big else "1.8"))
    for v in labels:
        assert (v - a) % step == 0
        s.append(text(X(v), Y + 36, T(v), 17))
    xs = []
    for v, l in dots:
        assert a <= v <= b
        xs.append(X(v))
        s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(v), Y, BLUE if l else RED))
        if l:
            s.append(text(X(v), Y - 20, l, 18))
    xs.sort()
    assert all(q - p >= 20 for p, q in zip(xs, xs[1:])), (a, b, dots)
    lx = sorted((X(v), len(T(v))) for v in labels)
    for (x1, n1), (x2, n2) in zip(lx, lx[1:]):
        assert x2 - x1 > 5 * (n1 + n2) + 6, labels
    lab = "number line from %s to %s split into %d equal spaces" % (T(a), T(b), spaces)
    if lettered:
        lab += " with points %s" % ", ".join(l for _, l in dots)
    elif dots:
        lab += " with a red dot"
    return svg_wrap(W, Y + 46, "".join(s), lab)


# ------------------------------------------------------------ figure: ruler in cm
def ruler_svg(length_mm, cm=10, PX=48):
    """Ruler from 0 to `cm` cm (mm marks). A pencil from 0 to length_mm millimetres."""
    X0, TOP = 22, 44
    W = X0 * 2 + cm * PX + 30
    RH = 50
    H = TOP + RH + 6
    X = lambda mm: X0 + PX * mm / 10.0
    o = []
    # pencil: body, tip
    L = X(length_mm)
    o.append("<rect x='%.1f' y='8' width='%.1f' height='22' fill='#f4c542' stroke='%s' stroke-width='2'/>"
             % (X(0), L - X(0) - 18, INK))
    o.append("<polygon points='%.1f,8 %.1f,19 %.1f,30' fill='%s' stroke='%s' stroke-width='2' stroke-linejoin='round'/>"
             % (L - 18, L, L - 18, WOOD, INK))
    o.append("<polygon points='%.1f,15.5 %.1f,19 %.1f,22.5' fill='%s'/>" % (L - 6, L, L - 6, INK))
    o.append("<line x1='%.1f' y1='6' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>"
             % (L, L, TOP, RED))
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
             % (X0 - 14, TOP, cm * PX + 58, RH, WOOD, INK))
    for mm in range(cm * 10 + 1):
        h = 16 if mm % 10 == 0 else 11 if mm % 5 == 0 else 7
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(mm), TOP, X(mm), TOP + h, INK, "1.8" if mm % 10 == 0 else "1.1"))
        if mm % 10 == 0:
            o.append(text(X(mm), TOP + 36, str(mm // 10), 15))
    o.append(text(X0 + cm * PX + 40, TOP + 36, "cm", 15, anchor="end", col=GREEN))
    return svg_wrap(W, H, "".join(o), "ruler in cm with a pencil from 0 to %s cm" % T(length_mm * 100))


# ------------------------------------------------------------ figure: weighing scale in kg
def dial_svg(v, mxv, lab, tick, size=200):
    """Round scale in kg from 0 to mxv: a tick every `tick` kg, a label every `lab` kg. Needle exactly at v."""
    v, mxv, lab, tick = Dm(v), Dm(mxv), Dm(lab), Dm(tick)
    c = size / 2.0
    R = c - 6

    def pt(val_, r):
        a = math.radians(-135 + 270.0 * float(val_ / mxv))
        return c + r * math.sin(a), c - r * math.cos(a)
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='6'/>" % (c, c, R, GREEN)]
    small, big = [], []
    for i in range(int(mxv / tick) + 1):
        val_ = tick * i
        major = (val_ / lab) == (val_ / lab).to_integral_value()
        x1, y1 = pt(val_, R - (17 if major else 10))
        x2, y2 = pt(val_, R - 4)
        (big if major else small).append("M%.1f %.1fL%.1f %.1f" % (x1, y1, x2, y2))
    s.append("<path d='%s' stroke='%s' stroke-width='1.6'/>" % ("".join(small), INK))
    s.append("<path d='%s' stroke='%s' stroke-width='3'/>" % ("".join(big), INK))
    nx, ny = pt(v, R - 9)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3.5' stroke-linecap='round'/>"
             % (c, c, nx, ny, RED))
    s.append("<g font-size='17' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='4' "
             "paint-order='stroke'>" % INK)
    for i in range(int(mxv / lab) + 1):
        x, y = pt(lab * i, R - 36)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (x, y + 6, format((lab * i).normalize(), "f")))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='7' fill='%s'/>" % (c, c, RED))
    s.append(text(c, c + 62, "kg", 22, col=GREEN, weight=800))
    return svg_wrap(size, size, "".join(s), "weighing scale in kg with the needle at %s kg" % format(v.normalize(), "f"))


# ------------------------------------------------------------ figure: measuring jug in litres
def jug_svg(v_ml, mx_ml=1000, lab=200, step=100, size=200):
    """Measuring jug marked in litres: a line every `step` ml, a label every `lab` ml. Water exactly at v_ml."""
    x0, x1 = 92, 168
    yb, yt = 186, 34

    def Y(val_):
        return yb - (yb - yt) * float(val_) / mx_ml
    s = []
    s.append("<path d='M%d %d C%d %d %d %d %d %d' fill='none' stroke='%s' stroke-width='6'/>"
             % (x1, 50, x1 + 28, 50, x1 + 28, 124, x1, 124, INK))
    s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s'/>" % (x0, Y(v_ml), x1 - x0, yb - Y(v_ml), WATER))
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0, Y(v_ml), x1, Y(v_ml), WATER_LINE))
    s.append("<path d='M%d %d L%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d L%d %d' fill='none' stroke='%s' "
             "stroke-width='4' stroke-linejoin='round'/>"
             % (x0 - 8, 14, x0, 22, x0, yb - 4, x0, yb, x0 + 6, yb, x1 - 6, yb, x1, yb, x1, yb - 4, x1, 16, INK))
    s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='end'>" % INK)
    for val_ in range(step, mx_ml + 1, step):
        major = val_ % lab == 0
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='%s'/>"
                 % (x0, Y(val_), x0 + (22 if major else 12), Y(val_), INK, "2.6" if major else "1.6"))
        if major:
            s.append("<text x='%d' y='%.1f'>%s</text>" % (x0 - 7, Y(val_) + 5, T(val_)))
    s.append("</g>")
    s.append(text(x0 - 7, 202, "ℓ", 16, anchor="end", col=GREEN))
    return svg_wrap(size, size + 6, "".join(s), "measuring jug marked in litres with water at %s ℓ" % T(v_ml))


# ------------------------------------------------------------ figure: coins
def coins_svg(coins):
    """A row of Singapore coins. coins = list of cents (5, 10, 20, 50, 100)."""
    R = {5: 22, 10: 26, 20: 29, 50: 33, 100: 35}
    G = 12
    W = sum(2 * R[c] for c in coins) + G * (len(coins) + 1)
    H = 2 * max(R[c] for c in coins) + 12
    o, x = [], G
    cy = H / 2.0
    for c in coins:
        r = R[c]
        cx = x + r
        o.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, COIN if c in (5, 100) else SILVER, INK))
        o.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 5, THIN))
        o.append(text(cx, cy + 6, "$1" if c == 100 else "%d¢" % c, 16 if c != 5 else 15))
        x += 2 * r + G
    lab = "coins: " + ", ".join("$1" if c == 100 else "%d¢" % c for c in coins)
    return svg_wrap(W, int(H), "".join(o), lab)


# ------------------------------------------------------------ figures: bar models
def brace(x1, x2, y, up, lab, col=INK):
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_units(n, total_lab, unit_lab, note, BW=520):
    """One bar of n equal units. Bracket above with total_lab; the first unit is shaded with unit_lab inside."""
    X0, TOP, BH = 10, 34, 38
    uw = BW / float(n)
    assert tw(unit_lab, 16) <= uw - 4, (unit_lab, uw)
    W = X0 * 2 + BW
    H = TOP + BH + 34
    o = [brace(X0, X0 + BW, 22, True, total_lab)]
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s'/>" % (X0, TOP, uw, BH, PARTFILL))
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (X0, TOP, BW, BH, GREEN))
    for i in range(1, n):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>"
                 % (X0 + uw * i, TOP, X0 + uw * i, TOP + BH, GREEN))
    o.append(text(X0 + uw / 2.0, TOP + BH / 2.0 + 6, unit_lab, 16, col=RED if unit_lab == "?" else INK))
    o.append(text(X0, TOP + BH + 24, note, 16, anchor="start", col=GREEN))
    return svg_wrap(W, H, "".join(o), "bar model: %d equal units, total %s, 1 unit %s" % (n, total_lab, unit_lab))


def bar_rows(rows, BW=420):
    """Comparison bar model drawn to scale. rows = [(name, value, label inside)]; the longest bar is BW wide."""
    top = max(Dm(v) for _, v, _ in rows)
    LW = int(max(tw(n, 16) for n, _, _ in rows)) + 16
    X0, TOP, BH, GAP = 6, 8, 36, 12
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + len(rows) * BH + (len(rows) - 1) * GAP + 8
    o = []
    fills = [HEADFILL, PARTFILL, "#e3ecf7", "#f3e3f0"]
    for i, (nm, v, lab) in enumerate(rows):
        y = TOP + i * (BH + GAP)
        w = float(Dm(v) / top) * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fills[i % 4], GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16))
    lab = "bar model comparing " + ", ".join("%s (%s)" % (n, l) for n, _, l in rows)
    return svg_wrap(int(W), H, "".join(o), lab)


# ============================================================ set 1: tenths, hundredths and thousandths
def digit_at(s, place):
    w, _, f = s.partition(".")
    return w[len(w) - 1 - place] if place >= 0 else f[-place - 1]


def set_places():
    its = []
    its.append(mcq(fig(grid_svg(70)) + "The whole square is 1. What decimal is shaded?", "0.7", ["0.07", "7", "0.3"],
                   "Each full column is 1 tenth. 7 full columns are shaded: 7 tenths = %s = <b>0.7</b>. "
                   "0.07 would be only 7 small squares, and 0.3 is the part that is not shaded." % fr(7, 10), want="0.7"))
    its.append(mcq(fig(grid_svg(43)) + "The whole square is 1. What decimal is shaded?", "0.43", ["4.3", "0.34", "0.043"],
                   "4 full columns (4 tenths) and 3 more small squares (3 hundredths) are shaded: "
                   "43 hundredths = %s = <b>0.43</b>." % fr(43, 100), want="0.43"))
    its.append(mcq(fig(grid_svg(5)) + "The whole square is 1. What decimal is shaded?", "0.05", ["0.5", "0.005", "5"],
                   "5 small squares are shaded and there is no full column, so there are 0 tenths. "
                   "5 hundredths = %s = <b>0.05</b>. Write 0 in the tenths place." % fr(5, 100), want="0.05"))
    its.append(mcq("1 whole is divided into <b>1000</b> equal parts. What decimal is 1 part?", "0.001",
                   ["0.01", "0.1", "1000"],
                   "Each part is %s of the whole, 1 <b>thousandth</b>: <b>0.001</b>. "
                   "0.01 is 1 hundredth (100 parts) and 0.1 is 1 tenth (10 parts)." % fr(1, 1000), want="0.001"))
    its.append(mcq(fig(chart_svg("7.06")) + "What decimal is shown in the place value chart?", "7.06",
                   ["7.6", "70.6", "7.006"],
                   "7 ones, 0 tenths and 6 hundredths: <b>7.06</b>. The 0 holds the tenths place. "
                   "7.6 drops the 0, so the 6 moves to the tenths place.", want="7.06"))
    for s, place, wrong in [("2.635", -3, ["5 hundredths", "5 tenths", "5 ones"]),
                            ("0.482", -2, ["8 tenths", "8 thousandths", "8 ones"]),
                            ("14.307", -1, ["3 ones", "3 hundredths", "3 thousandths"])]:
        dg = digit_at(s, place)
        right = "%s %s" % (dg, NAMES[place])
        nth = {-1: "1st", -2: "2nd", -3: "3rd"}[place]
        e = ("The red %s is in the <b>%s</b> place after the decimal point, the %s place. Its value is <b>%s</b> = %s."
             % (dg, nth, NAMES[place], right, format((Dm(dg) * Dm(10) ** place).normalize(), "f")))
        its.append(mcq(fig(chart_svg(s, hi=place)) + "What is the value of the red digit in %s?" % s,
                       right, wrong, e, same_ok=True))
    for dg, s, place, right, wrong in [("4", "3.024", -3, "0.004", ["0.04", "0.4", "4"]),
                                       ("9", "0.951", -1, "0.9", ["0.09", "0.009", "9"]),
                                       ("2", "25.168", 1, "20", ["2", "0.2", "200"])]:
        assert digit_at(s, place) == dg
        where = {1: "the tens place (2 places to the left of the point)",
                 -1: "the tenths place, the 1st place after the point",
                 -3: "the thousandths place, the 3rd place after the point"}[place]
        its.append(mcq("What is the value of the digit <b>%s</b> in <b>%s</b>?" % (dg, s), right, wrong,
                       "In %s the %s is in %s. It stands for <b>%s</b>." % (s, dg, where, right),
                       want=Dm(dg) * Dm(10) ** place))
    its.append(mcq("In <b>6.583</b>, which digit is in the <b>thousandths</b> place?", "3", ["8", "5", "6"],
                   "Count the places after the decimal point: tenths (5), hundredths (8), thousandths (3). "
                   "The answer is <b>3</b>.", same_ok=True))
    its.append(mcq(fig(line_svg(240, 250, 10, dots=[(247, None)])) + "What decimal is at the red dot?", "0.247",
                   ["0.27", "0.253", "0.207"],
                   "From 0.24 to 0.25 there are <b>10 equal spaces</b>, so each space is 1 thousandth (0.001). "
                   "The dot is 7 spaces after 0.24: <b>0.247</b>. 0.253 counts back from the wrong end.", want="0.247"))
    its.append(mcq(fig(line_svg(1300, 1400, 10, dots=[(1380, None)])) + "What decimal is at the red dot?", "1.38",
                   ["1.308", "1.8", "1.48"],
                   "From 1.3 to 1.4 there are 10 equal spaces, so each space is 1 hundredth (0.01). "
                   "The dot is 8 spaces after 1.30: <b>1.38</b>. 1.308 would be very close to 1.3.", want="1.38"))
    its.append(mcq("How many thousandths are there in <b>0.4</b>?", "400", ["4", "40", "4000"],
                   "1 tenth = 100 thousandths, so 4 tenths = <b>400</b> thousandths. 0.4 = 0.400.", want=400))
    its.append(mcq("4 + 0.3 + 0.008 = ?", "4.308", ["4.38", "4.038", "43.08"],
                   "4 ones, 3 tenths, 0 hundredths and 8 thousandths: 4 . 3 0 8 = <b>4.308</b>. "
                   "4.38 drops the 0 that holds the hundredths place.", want=4 + V("0.3") + V("0.008")))
    its.append(mcq("Write <b>3 ones, 4 tenths and 9 thousandths</b> as a decimal.", "3.409",
                   ["3.49", "3.049", "34.09"],
                   "There are 0 hundredths, so write one digit in each place: 3 . 4 0 9 = <b>3.409</b>. "
                   "The 0 holds the hundredths place.", want="3.409"))
    its.append(mcq("Write <b>2 tens, 6 hundredths and 5 thousandths</b> as a decimal.", "20.065",
                   ["20.65", "2.065", "26.5"],
                   "2 tens = 20. There are 0 ones and 0 tenths. Then 6 hundredths and 5 thousandths: <b>20.065</b>.",
                   want=20 + V("0.06") + V("0.005")))
    its.append(mcq("Which is equal to <b>5.274</b>?", "5 + 0.2 + 0.07 + 0.004",
                   ["5 + 0.2 + 0.7 + 0.4", "5 + 2 + 7 + 4", "5 + 0.002 + 0.07 + 0.4"],
                   "5 ones, 2 tenths, 7 hundredths and 4 thousandths: <b>5 + 0.2 + 0.07 + 0.004</b>.", same_ok=True))
    assert 5 + V("0.2") + V("0.07") + V("0.004") == V("5.274")
    its.append(mcq("What is <b>0.01 more</b> than 4.293?", "4.303", ["4.294", "4.393", "5.293"],
                   "0.01 is 1 hundredth. The hundredths digit is 9, and 9 + 1 = 10 hundredths = 1 more tenth. "
                   "So 4.293 + 0.01 = <b>4.303</b>. 4.294 adds 0.001 and 4.393 adds 0.1.", want=V("4.293") + V("0.01")))
    its.append(mcq("What is <b>0.001 more</b> than 2.709?", "2.71", ["2.7010", "2.719", "2.809"],
                   "0.001 is 1 thousandth. 9 thousandths + 1 thousandth = 10 thousandths = 1 hundredth. "
                   "So 2.709 + 0.001 = 2.710 = <b>2.71</b>. 2.7010 writes 10 in one place. 2.719 adds 0.01.",
                   want=V("2.709") + V("0.001")))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Tenths, hundredths and thousandths", "items": its}


# ============================================================ set 2: compare and order
def cmp_item(x, y, e, pre=""):
    a, b = V(x), V(y)
    lt, gt, eq = "%s &lt; %s" % (x, y), "%s &gt; %s" % (x, y), "%s = %s" % (x, y)
    right = lt if a < b else gt if a > b else eq
    wrong = [c for c in (lt, gt, eq) if c != right] + ["Cannot tell"]
    return mcq(pre + "Compare <b>%s</b> and <b>%s</b>. Which is correct?" % (x, y), right, wrong, e, same_ok=True)


def order_q(nums, how, right, wrong, e):
    vs = sorted((V(x) for x in nums), reverse="greatest to" in how)
    assert [V(x) for x in right.split(", ")] == vs, right
    for w in wrong:
        assert sorted(w.split(", ")) == sorted(nums)
        assert w != right
    return mcq("Arrange from <b>%s</b>: <b>%s</b>" % (how, ", ".join(nums)), right, wrong, e, same_ok=True)


def set_compare():
    its = []
    its.append(cmp_item("0.45", "0.5", "0.5 = 0.50, so the second square has 50 hundredths shaded. 45 hundredths &lt; 50 hundredths, "
                        "so <b>0.45 &lt; 0.5</b>. Do not compare 45 with 5: the 5 in 0.5 is 5 <b>tenths</b>.",
                        pre=fig(two_grids(45, "0.45", 50, "0.5"))))
    its.append(cmp_item("0.7", "0.70", "A zero at the <b>end</b> of a decimal does not change its value: "
                        "7 tenths = 70 hundredths. So <b>0.7 = 0.70</b>."))
    its.append(cmp_item("2.305", "2.35", "Both have 2 ones and 3 tenths. Compare the hundredths: 0 &lt; 5. "
                        "So <b>2.305 &lt; 2.35</b>, even though 2.305 has more digits."))
    its.append(cmp_item("0.089", "0.1", "Compare the tenths: 0.089 has 0 tenths and 0.1 has 1 tenth. "
                        "So <b>0.089 &lt; 0.1</b>, even though 89 &gt; 1."))
    its.append(cmp_item("6.42", "6.402", "Write 6.42 as 6.420. Both have 6 ones and 4 tenths. Compare the hundredths: 2 &gt; 0. "
                        "So <b>6.42 &gt; 6.402</b>."))
    its.append(cmp_item("13.1", "9.999", "Compare the whole numbers first: 13 &gt; 9. So <b>13.1 &gt; 9.999</b>, "
                        "even though 9.999 has more digits."))
    its.append(mcq("Which decimal is the <b>greatest</b>?", "0.6", ["0.594", "0.599", "0.06"],
                   "Compare the tenths: 6, 5, 5 and 0. <b>0.6</b> has the most tenths, so it is the greatest, "
                   "even though 0.594 and 0.599 have more digits.", want="0.6"))
    its.append(mcq("Which decimal is the <b>smallest</b>?", "0.305", ["0.35", "0.351", "0.53"],
                   "0.53 has 5 tenths, so it is the greatest. The others have 3 tenths: compare the hundredths 0, 5 and 5. "
                   "<b>0.305</b> has 0 hundredths, so it is the smallest.", want="0.305"))
    its.append(mcq("Which number is <b>greater than 0.25</b>?", "0.3", ["0.205", "0.025", "0.249"],
                   "0.25 = 0.250 and 0.3 = 0.300. 300 thousandths &gt; 250 thousandths, so <b>0.3</b> &gt; 0.25. "
                   "0.249 is 1 thousandth less than 0.25.", want="0.3"))
    assert all(V(x) < V("0.25") for x in ("0.205", "0.025", "0.249"))
    its.append(mcq("Which decimal is <b>equal to 0.4</b>?", "0.400", ["0.004", "0.04", "4.00"],
                   "0.4 = 4 tenths = 400 thousandths = <b>0.400</b>. Zeros at the end do not change the value. "
                   "0.04 and 0.004 move the 4 to a smaller place.", want="0.4"))
    its.append(mcq("Which number is <b>between 1.25 and 1.26</b>?", "1.257", ["1.275", "1.205", "1.52"],
                   "1.25 = 1.250 and 1.26 = 1.260. <b>1.257</b> is between 1.250 and 1.260.", want="1.257"))
    assert V("1.25") < V("1.257") < V("1.26") and not V("1.25") < V("1.275") < V("1.26")
    its.append(fixed(fig(line_svg(300, 400, 10, labels=[300, 350, 400], dots=[(320, "A"), (355, "B"), (370, "C"), (395, "D")],
                              W=500)) +
                     "Which letter shows <b>0.355</b>?", ["A", "B", "C", "D"], 1,
                     "Each space is 0.01. 0.355 is halfway between 0.35 and 0.36. That is point <b>B</b>. "
                     "A is 0.32, C is 0.37 and D is 0.395."))
    its.append(mcq("Which statement is <b>true</b>?", "0.8 &gt; 0.79",
                   ["0.08 &gt; 0.8", "0.125 &gt; 0.2", "0.3 &lt; 0.296"],
                   "0.8 = 0.80, and 80 hundredths &gt; 79 hundredths. So <b>0.8 &gt; 0.79</b> is true.", same_ok=True))
    assert V("0.8") > V("0.79") and not V("0.08") > V("0.8") and not V("0.125") > V("0.2") and not V("0.3") < V("0.296")
    its.append(mcq("Hui Min says 0.125 &gt; 0.2 because 125 &gt; 2. Which is correct?", "0.125 &lt; 0.2",
                   ["0.125 &gt; 0.2", "0.125 = 0.2", "Cannot tell"],
                   "Compare the tenths first: 0.125 has 1 tenth and 0.2 has 2 tenths. So <b>0.125 &lt; 0.2</b>. "
                   "Or write 0.2 as 0.200: 125 thousandths &lt; 200 thousandths.", same_ok=True))
    its.append(order_q(["0.5", "0.45", "0.405"], "the smallest to the greatest", "0.405, 0.45, 0.5",
                       ["0.5, 0.45, 0.405", "0.45, 0.405, 0.5", "0.405, 0.5, 0.45"],
                       "Write them with 3 decimal places: 0.500, 0.450, 0.405. 405 &lt; 450 &lt; 500, so the order is "
                       "<b>0.405, 0.45, 0.5</b>. The longest number is not the greatest."))
    its.append(order_q(["3.2", "3.02", "3.202", "3.022"], "the smallest to the greatest", "3.02, 3.022, 3.2, 3.202",
                       ["3.2, 3.02, 3.202, 3.022", "3.02, 3.2, 3.022, 3.202", "3.202, 3.2, 3.022, 3.02"],
                       "All have 3 ones. Write them with 3 decimal places: 3.200, 3.020, 3.202, 3.022. "
                       "20 &lt; 22 &lt; 200 &lt; 202 thousandths, so <b>3.02, 3.022, 3.2, 3.202</b>."))
    its.append(order_q(["0.9", "0.09", "0.909", "0.099"], "the greatest to the smallest", "0.909, 0.9, 0.099, 0.09",
                       ["0.9, 0.909, 0.09, 0.099", "0.09, 0.099, 0.9, 0.909", "0.909, 0.099, 0.9, 0.09"],
                       "Write them with 3 decimal places: 0.900, 0.090, 0.909, 0.099. Greatest first: 909, 900, 99, 90. "
                       "So <b>0.909, 0.9, 0.099, 0.09</b>."))
    its.append(mcq("Which digit can go in the box to make this true?<br><b>0.6□4 &gt; 0.67</b>", "8", ["6", "2", "0"],
                   "Write 0.67 as 0.670. Both numbers have 6 tenths, so compare the hundredths. "
                   "The box must be 7 or more: 0.684 &gt; 0.670. So <b>8</b> works. With 6, 0.664 &lt; 0.670.", want=8))
    assert V("0.684") > V("0.67") and all(V("0.6%s4" % d) < V("0.67") for d in "620")
    its.append(mcq("Use the digits 4, 0 and 7 once each to fill 0.□□□. What is the <b>greatest</b> decimal you can make?",
                   "0.740", ["0.704", "0.047", "0.470"],
                   "Put the greatest digit in the greatest place: 7 tenths, then 4 hundredths, then 0 thousandths. "
                   "The greatest decimal is <b>0.740</b>.", want="0.74"))
    its.append(mcq("What is the <b>smallest</b> number with 3 decimal places that is greater than 2.39?", "2.391",
                   ["2.4", "2.389", "2.390"],
                   "2.39 = 2.390. The next thousandth after 2.390 is <b>2.391</b>. 2.390 is equal to 2.39, not greater, "
                   "and 2.389 is smaller.", want="2.391"))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order decimals", "items": its}


# ============================================================ set 3: decimals and fractions
def set_fractions():
    its = []
    its.append(mcq("Write %s as a decimal." % fr(3, 10), "0.3", ["0.03", "3.1", "0.003"],
                   "%s is 3 tenths. Tenths are the 1st place after the point: <b>0.3</b>. "
                   "0.03 is 3 hundredths." % fr(3, 10), want=F(3, 10)))
    its.append(mcq("Write %s as a decimal." % fr(7, 100), "0.07", ["0.7", "0.007", "7"],
                   "%s is 7 hundredths. Hundredths need 2 places, so write 0 in the tenths place: <b>0.07</b>."
                   % fr(7, 100), want=F(7, 100)))
    its.append(mcq("Which fraction is equal to <b>0.3</b>?", fr(3, 10), [fr(3, 100), fr(1, 3), fr(3, 1000)],
                   "0.3 has 1 digit after the point, so it means tenths: 0.3 = <b>%s</b>. "
                   "%s is 0.03, not 0.3." % (fr(3, 10), fr(3, 100)), want=V("0.3")))
    its.append(mcq("Which fraction is equal to <b>0.09</b>?", fr(9, 100), [fr(9, 10), fr(1, 9), fr(9, 1000)],
                   "0.09 has 2 digits after the point, so it means hundredths: 9 hundredths = <b>%s</b>." % fr(9, 100),
                   want=V("0.09")))
    its.append(mcq("Write <b>0.047</b> as a fraction.", fr(47, 1000), [fr(47, 100), fr(47, 10), fr(4, 7)],
                   "0.047 has 3 digits after the point, so it means thousandths: <b>%s</b>. "
                   "%s would be 0.47." % (fr(47, 1000), fr(47, 100)), want=V("0.047")))
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 2), "0.5", ["1.2", "0.12", "0.2"],
                   "Make tenths: %s = %s (multiply the numerator and denominator by 5). 5 tenths = <b>0.5</b>. "
                   "1.2 just writes the digits 1 and 2." % (fr(1, 2), fr(5, 10)), want=F(1, 2)))
    its.append(mcq("Which decimal is equal to %s?" % fr(1, 5), "0.2", ["1.5", "0.15", "0.5"],
                   "Make tenths: %s = %s (multiply the numerator and denominator by 2). 2 tenths = <b>0.2</b>. "
                   "0.15 just writes the 1 and the 5 after the point." % (fr(1, 5), fr(2, 10)), want=F(1, 5)))
    its.append(mcq("Which decimal is equal to %s?" % fr(3, 4), "0.75", ["3.4", "0.34", "0.25"],
                   "Make hundredths: %s = %s (multiply the numerator and denominator by 25). 75 hundredths = <b>0.75</b>. "
                   "0.25 is %s, the part that is left." % (fr(3, 4), fr(75, 100), fr(1, 4)), want=F(3, 4)))
    its.append(mcq("Express <b>0.5</b> as a fraction in its simplest form.", fr(1, 2), [fr(1, 5), fr(5, 100), fr(5, 1000)],
                   "0.5 = %s. Divide the numerator and denominator by 5: %s = <b>%s</b>. "
                   "%s is 0.2, not 0.5." % (fr(5, 10), fr(5, 10), fr(1, 2), fr(1, 5)), want=V("0.5")))
    its.append(mcq("Express <b>0.6</b> as a fraction in its simplest form.", fr(3, 5), [fr(6, 100), fr(1, 6), fr(2, 5)],
                   "0.6 = %s. Divide the numerator and denominator by 2: <b>%s</b>. "
                   "%s is 0.06, and %s is 0.4." % (fr(6, 10), fr(3, 5), fr(6, 100), fr(2, 5)), want=V("0.6")))
    its.append(mcq("Express <b>0.25</b> as a fraction in its simplest form.", fr(1, 4), [fr(25, 1000), fr(1, 25), fr(2, 5)],
                   "0.25 = %s. Divide the numerator and denominator by 25: <b>%s</b>. "
                   "%s just uses the digits 2 and 5." % (fr(25, 100), fr(1, 4), fr(2, 5)), want=V("0.25")))
    its.append(mcq("Express <b>0.04</b> as a fraction in its simplest form.", fr(1, 25), [fr(1, 4), fr(2, 5), fr(1, 250)],
                   "0.04 = %s. Divide the numerator and denominator by 4: <b>%s</b>. "
                   "%s is 0.25 and %s is 0.4." % (fr(4, 100), fr(1, 25), fr(1, 4), fr(2, 5)), want=V("0.04")))
    its.append(mcq("Express %s as a decimal." % fr(3, 20), "0.15", ["0.32", "3.2", "0.015"],
                   "20 × 5 = 100, so make hundredths: %s = %s = <b>0.15</b>. "
                   "0.32 and 3.2 just write the digits 3 and 2." % (fr(3, 20), fr(15, 100)), want=F(3, 20)))
    its.append(mcq("Express %s as a decimal." % fr(9, 25), "0.36", ["9.25", "0.925", "0.18"],
                   "25 × 4 = 100, so make hundredths: %s = %s = <b>0.36</b>. "
                   "0.18 multiplies the numerator by 2 instead of 4." % (fr(9, 25), fr(36, 100)), want=F(9, 25)))
    its.append(mcq("Express %s as a decimal." % fr(7, 50), "0.14", ["0.07", "7.5", "0.75"],
                   "50 × 2 = 100, so make hundredths: %s = %s = <b>0.14</b>. "
                   "0.07 forgets to multiply the numerator by 2." % (fr(7, 50), fr(14, 100)), want=F(7, 50)))
    its.append(mcq("Express %s as a decimal." % mx(2, 3, 5), "2.6", ["2.35", "2.06", "2.3"],
                   "%s = %s, so %s = 2 + 0.6 = <b>2.6</b>. 2.35 just writes the digits 3 and 5."
                   % (fr(3, 5), fr(6, 10), mx(2, 3, 5)), want=2 + F(3, 5)))
    its.append(mcq("Express <b>4.08</b> as a mixed number in its simplest form.", mx(4, 2, 25),
                   [mx(4, 4, 5), mx(4, 1, 8), mx(4, 1, 125)],
                   "4.08 = 4 + %s. Divide the numerator and denominator by 4: %s = %s. So 4.08 = <b>%s</b>. "
                   "%s is 4.8 (it drops the 0 in the tenths place)." % (fr(8, 100), fr(8, 100), fr(2, 25), mx(4, 2, 25),
                                                                         mx(4, 4, 5)), want=V("4.08")))
    its.append(mcq(fig(grid_svg(40)) + "The whole square is 1. Which is <b>not</b> equal to the shaded part?", "0.04",
                   ["0.4", fr(4, 10), fr(2, 5)],
                   "4 full columns are shaded: 4 tenths. 0.4 = %s = %s, so they all match. "
                   "<b>0.04</b> is only 4 small squares." % (fr(4, 10), fr(2, 5)), same_ok=True))
    assert V("0.4") == F(4, 10) == F(2, 5) != V("0.04")
    right = "0.45, " + fr(1, 2) + ", 0.6"
    its.append(mcq("Arrange from <b>the smallest to the greatest</b>: <b>0.6, %s, 0.45</b>" % fr(1, 2), right,
                   ["0.6, 0.45, " + fr(1, 2), fr(1, 2) + ", 0.45, 0.6", "0.45, 0.6, " + fr(1, 2)],
                   "Change %s to a decimal: 0.5. Now compare 0.60, 0.50 and 0.45: <b>0.45, %s, 0.6</b>. "
                   "%s is not the smallest just because 1 and 2 are small digits." % (fr(1, 2), fr(1, 2), fr(1, 2)),
                   same_ok=True))
    assert V("0.45") < F(1, 2) < V("0.6")
    its.append(mcq("Ryan says 0.3 = %s. Which is correct?" % fr(3, 100), "0.3 is 3 tenths, so 0.3 = " + fr(3, 10),
                   ["0.3 = " + fr(3, 1000), "0.3 = " + fr(1, 3), "Ryan is right: 0.3 = " + fr(3, 100)],
                   "The 3 is in the 1st place after the point, the tenths place. So <b>0.3 = %s</b>. "
                   "%s is 0.03 (2 places)." % (fr(3, 10), fr(3, 100)), same_ok=True))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 17, 12, 13, 14, 15, 19, 16, 18]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Decimals and fractions", "items": its}


# ============================================================ set 4: rounding
PLACE_NAME = {0: "the nearest whole number", 1: "1 decimal place", 2: "2 decimal places"}


def round_e(x, places):
    """Explanation for rounding decimal string x to `places` decimal places."""
    q = Dm(1).scaleb(-places)
    lo = Dm(x).quantize(q, rounding=ROUND_FLOOR)
    hi = lo + q
    r = Dm(rnd_to(x, places))
    nxt = {0: "tenths", 1: "hundredths", 2: "thousandths"}[places]
    f = x.partition(".")[2]
    d = int(f[places])
    return ("%s is between %s and %s. Look at the %s digit: %d. It is %s, so round %s to <b>%s</b>."
            % (x, lo, hi, nxt, d, "5 or more" if d >= 5 else "4 or less", "up" if r > lo else "down", r))


def rq(x, places, wrong, extra="", stem=None, figure="", unit="", right=None):
    right = (right or rnd_to(x, places)) + unit
    assert V(right.replace(unit, "")) == V(rnd_to(x, places)), (x, right)
    q = figure + (stem or "Round <b>%s</b> to %s." % (x, PLACE_NAME[places]))
    return mcq(q, right, [w + unit for w in wrong], round_e(x, places) + extra)


def set_round():
    its = []
    its.append(rq("4.65", 0, ["4", "4.7", "4.6"], " The nearest whole number has no decimal places, so 4.7 is not the answer."))
    its.append(rq("7.38", 0, ["8", "7.4", "7.3"], " 7.38 is closer to 7 than to 8."))
    its.append(rq("12.6", 0, ["12", "12.5", "12.7"], " The dot is closer to 13 than to 12.",
                  figure=fig(line_svg(12000, 13000, 10, labels=[12000, 12500, 13000], dots=[(12600, None)])),
                  stem="Round the number at the red dot (12.6) to the nearest whole number."))
    its.append(rq("2.47", 1, ["2.4", "3", "2"], " The dot is closer to 2.5 than to 2.4.",
                  figure=fig(line_svg(2400, 2500, 10, labels=[2400, 2450, 2500], dots=[(2470, None)])),
                  stem="Round the number at the red dot (2.47) to 1 decimal place."))
    its.append(rq("15.55", 0, ["15", "15.6", "15.5"], " Rounding to the nearest whole number gives an answer with no decimal places."))
    its.append(rq("8.47", 0, ["9", "8.5", "8.4"], " 9 comes from rounding twice (8.47 → 8.5 → 9). "
                  "Round only once, using the tenths digit."))
    its.append(rq("6.32", 1, ["6.4", "6", "6.2"], " 6.4 rounds up when the digit is only 2."))
    its.append(rq("0.746", 2, ["0.74", "0.7", "0.8"], " 0.7 rounds to 1 decimal place instead of 2."))
    its.append(rq("6.381", 2, ["6.39", "6.4", "6.3"], " 6.4 rounds to 1 decimal place instead of 2."))
    its.append(rq("7.049", 1, ["7.1", "7.05", "7.4"], " The answer is written 7.0 to show 1 decimal place. "
                  "Do not round the 9 first: 7.049 is closer to 7.0 than to 7.1.", right="7.0"))
    its.append(rq("3.952", 1, ["3.9", "3.10", "3.95"], " The answer is written 4.0 to show 1 decimal place. "
                  "3.10 is wrong: 10 tenths make 1 whole.", right="4.0"))
    its.append(rq("12.045", 2, ["12.04", "12.1", "12.45"], " 12.45 drops the 0 in the tenths place."))
    its.append(mcq("To round <b>8.274</b> to 2 decimal places, which digit do you look at?", "the 4 (thousandths)",
                   ["the 7 (hundredths)", "the 2 (tenths)", "the 8 (ones)"],
                   "To round to 2 decimal places, look one place to the right of the hundredths: the thousandths digit. "
                   "It is <b>4</b>, so 8.274 rounds down to 8.27.", same_ok=True))
    assert rnd_to("8.274", 2) == "8.27"
    its.append(mcq("Which number rounds to <b>5.3</b> when it is rounded to 1 decimal place?", "5.348",
                   ["5.351", "5.249", "5.36"],
                   "Look at the hundredths digit. 5.348 has 4 hundredths, so it rounds down to <b>5.3</b> "
                   "(do not round the 8 first). 5.351 and 5.36 round up to 5.4, and 5.249 rounds to 5.2.", want="5.348"))
    assert [rnd_to(x, 1) for x in ("5.348", "5.351", "5.249", "5.36")] == ["5.3", "5.4", "5.2", "5.4"]
    its.append(mcq("Which number becomes <b>6</b> when it is rounded to the nearest whole number?", "5.5",
                   ["6.5", "5.49", "6.51"],
                   "5.5 is between 5 and 6. The tenths digit is 5, so it rounds up to <b>6</b>. "
                   "6.5 and 6.51 round to 7, and 5.49 rounds to 5.", want="5.5"))
    assert [rnd_to(x, 0) for x in ("5.5", "6.5", "5.49", "6.51")] == ["6", "7", "5", "7"]
    its.append(mcq("A number was rounded to 1 decimal place. The answer is <b>3.6</b>. Which could be the number?", "3.58",
                   ["3.65", "3.54", "3.67"],
                   "3.58 is between 3.5 and 3.6. The hundredths digit is 8, so it rounds up to <b>3.6</b>. "
                   "3.65 and 3.67 round to 3.7, and 3.54 rounds to 3.5.", want="3.58"))
    assert [rnd_to(x, 1) for x in ("3.58", "3.65", "3.54", "3.67")] == ["3.6", "3.7", "3.5", "3.7"]
    its.append(rq("9.96", 1, ["9.9", "9.10", "9.0"], " The answer is written 10.0 to show 1 decimal place. "
                  "9 tenths and 1 more make 10 tenths, which is 1 whole.", right="10.0"))
    its.append(rq("2.396", 2, ["2.39", "2.310", "2.30"], " The answer is written 2.40 to show 2 decimal places. "
                  "9 hundredths and 1 more make 10 hundredths, which is 1 more tenth.", right="2.40"))
    its.append(mcq("A number with 1 decimal place is rounded to the nearest whole number. The answer is <b>8</b>. "
                   "What is the <b>smallest</b> the number can be?", "7.5", ["7.4", "8.4", "8.5"],
                   "7.5 is the smallest number with 1 decimal place that rounds up to 8 (the tenths digit is 5). "
                   "7.4 rounds down to 7. 8.4 is the <b>greatest</b> it can be, and 8.5 rounds to 9.", want="7.5"))
    assert rnd_to("7.5", 0) == "8" and rnd_to("7.4", 0) == "7" and rnd_to("8.5", 0) == "9"
    its.append(rq("0.999", 2, ["0.99", "0.910", "0.100"], " The answer is written 1.00 to show 2 decimal places.",
                  right="1.00"))
    order = [0, 1, 2, 3, 4, 6, 5, 7, 8, 12, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Rounding decimals", "items": its}


# ============================================================ set 5: money and measurement
def set_problems():
    its = []
    its.append(mcq(fig(ruler_svg(74)) + "How long is the pencil?", "7.4 cm", ["7.04 cm", "74 cm", "7.3 cm"],
                   "The pencil ends 4 small marks after 7 cm. Each small mark is 1 mm = 0.1 cm, so the length is "
                   "<b>7.4 cm</b>. 7.04 cm would be only a tiny bit more than 7 cm. 7.3 cm counts the 7 cm line as the first small mark.", want="7.4"))
    its.append(mcq(fig(dial_svg("2.7", "3", "1", "0.1")) + "What is the mass of the bag of rice on the scale?", "2.7 kg",
                   ["2.07 kg", "27 kg", "2.3 kg"],
                   "There are 10 small marks between 2 kg and 3 kg, so each small mark is 0.1 kg. "
                   "The needle is 7 small marks after 2 kg: <b>2.7 kg</b>. 2.3 kg counts back from 3 kg.", want="2.7"))
    its.append(mcq(fig(jug_svg(600)) + "How much water is in the jug?", "0.6 ℓ", ["0.06 ℓ", "6 ℓ", "0.4 ℓ"],
                   "Each small mark is 0.1 ℓ. The water level is at the line labelled 0.6: <b>0.6 ℓ</b>. "
                   "0.4 ℓ is the empty part of the jug.", want="0.6"))
    its.append(mcq("Write <b>5 dollars 40 cents</b> in dollars.", "$5.40", ["$5.04", "$540", "$0.54"],
                   "40 cents = 40 hundredths of a dollar = $0.40. So 5 dollars 40 cents = <b>$5.40</b>. "
                   "$5.04 is 5 dollars 4 cents.", want="5.4"))
    its.append(mcq("Write <b>85¢</b> in dollars.", "$0.85", ["$8.50", "$85", "$0.08"],
                   "100¢ = $1, so 85¢ = 85 hundredths of a dollar = <b>$0.85</b>. $8.50 is 850¢ and $0.08 is only 8¢.", want="0.85"))
    its.append(mcq("A packet of chicken rice costs <b>$3.05</b>. Which is the same amount?", "3 dollars 5 cents",
                   ["3 dollars 50 cents", "30 dollars 5 cents", "305 dollars"],
                   "In $3.05 the 0 is in the tenths place and the 5 is in the hundredths place. "
                   "So $3.05 is <b>3 dollars 5 cents</b>. 3 dollars 50 cents is $3.50.", same_ok=True))
    assert V("3.05") == 3 + F(5, 100)
    its.append(mcq(fig(coins_svg([100, 50, 20, 5])) + "Ali has these coins in his pocket. How much money does he have?",
                   "$1.75", ["$76", "$1.57", "$17.50"],
                   "$1 + 50¢ + 20¢ + 5¢ = 100¢ + 75¢ = 175¢. 175¢ = <b>$1.75</b>. "
                   "$76 adds 1 + 50 + 20 + 5 as if they were all dollars.", want=1 + F(75, 100)))
    its.append(mcq("A bowl of laksa at a hawker centre costs $4.85. What is the price to the nearest dollar?",
                   "$5", ["$4", "$4.90", "$4.80"],
                   "$4.85 is between $4 and $5. Look at the tenths digit: 8. It is 5 or more, so round up to <b>$5</b>. "
                   "$4.90 rounds to the nearest 10¢, not the nearest dollar.", want=5))
    assert rnd_to("4.85", 0) == "5"
    its.append(mcq("Wei Ming’s EZ-Link card has $12.45 left on it. What is this amount to the nearest dollar?",
                   "$12", ["$13", "$12.50", "$12.40"],
                   "$12.45 is between $12 and $13. The tenths digit is 4, so round down to <b>$12</b>. "
                   "$13 comes from rounding twice ($12.45 → $12.50 → $13).", want=12))
    assert rnd_to("12.45", 0) == "12"
    its.append(mcq(fig(bar_rows([("Siti", "1.25", "1.25 m"), ("Farah", "1.3", "1.3 m")])) +
                   "Siti’s ribbon is 1.25 m long. Farah’s ribbon is 1.3 m long. Whose ribbon is longer?", "Farah’s",
                   ["Siti’s", "They are the same length", "Cannot tell"],
                   "1.3 m = 1.30 m. 30 hundredths &gt; 25 hundredths, so <b>Farah’s</b> ribbon is longer. "
                   "The bar model shows Farah’s bar is longer. 1.25 has more digits, but that does not make it greater.",
                   same_ok=True))
    assert V("1.3") > V("1.25")
    its.append(mcq("On Sports Day, Ahmad jumps 2.45 m and Ryan jumps 2.405 m in the long jump. Who jumps farther?",
                   "Ahmad", ["Ryan", "They jump the same distance", "Cannot tell"],
                   "Write both with 3 decimal places: 2.450 m and 2.405 m. 450 &gt; 405 thousandths, so <b>Ahmad</b> "
                   "jumps farther. 2.405 has more digits, but that does not make it greater.", same_ok=True))
    assert V("2.45") > V("2.405")
    its.append(mcq("In a 100 m race, Wei Ming takes 15.36 s, Jun Jie takes 15.4 s, Hafiz takes 15.29 s and Ethan takes "
                   "15.3 s. Who is the fastest?", "Hafiz", ["Wei Ming", "Jun Jie", "Ethan"],
                   "The fastest runner takes the <b>least</b> time. Write the times with 2 decimal places: 15.36, 15.40, "
                   "15.29 and 15.30. 15.29 is the smallest, so <b>Hafiz</b> is the fastest. "
                   "Jun Jie’s 15.4 s is the slowest, not the fastest.", same_ok=True))
    assert min(V("15.36"), V("15.4"), V("15.29"), V("15.3")) == V("15.29")
    its.append(mcq("Mrs Ng buys three durians with masses of 2.5 kg, 2.35 kg and 2.475 kg. "
                   "Arrange the masses from <b>the lightest to the heaviest</b>.", "2.35 kg, 2.475 kg, 2.5 kg",
                   ["2.5 kg, 2.35 kg, 2.475 kg", "2.475 kg, 2.35 kg, 2.5 kg", "2.5 kg, 2.475 kg, 2.35 kg"],
                   "Write them with 3 decimal places: 2.500, 2.350 and 2.475. 350 &lt; 475 &lt; 500, so the order is "
                   "<b>2.35 kg, 2.475 kg, 2.5 kg</b>.", same_ok=True))
    assert V("2.35") < V("2.475") < V("2.5")
    its.append(mcq(fig(bar_units(4, "1 m", "?", "4 units = 1 m")) +
                   "Mr Tan cuts a 1 m ribbon into 4 equal pieces. How long is each piece? Give your answer as a decimal.",
                   "0.25 m", ["0.4 m", "0.14 m", "4 m"],
                   "4 units = 1 m, so 1 unit = %s m. %s = %s = <b>0.25 m</b>. "
                   "0.4 m is a common mistake: %s is not 0.4." % (fr(1, 4), fr(1, 4), fr(25, 100), fr(1, 4)),
                   want=F(1, 4)))
    its.append(mcq(fig(bar_units(5, "1 ℓ", "?", "5 units = 1 ℓ")) +
                   "Chloe pours 1 ℓ of orange juice equally into 5 cups. How much juice is in each cup? "
                   "Give your answer as a decimal.", "0.2 ℓ", ["0.5 ℓ", "0.15 ℓ", "5 ℓ"],
                   "5 units = 1 ℓ, so 1 unit = %s ℓ. %s = %s = <b>0.2 ℓ</b>. "
                   "0.5 ℓ would fill only 2 cups." % (fr(1, 5), fr(1, 5), fr(2, 10)), want=F(1, 5)))
    its.append(mcq("Mdm Wong uses %s kg of flour to bake kueh for Hari Raya Puasa. Write this mass as a decimal." % fr(3, 4),
                   "0.75 kg", ["0.34 kg", "3.4 kg", "0.25 kg"],
                   "%s = %s = <b>0.75 kg</b>. 0.34 kg just writes the digits 3 and 4." % (fr(3, 4), fr(75, 100)),
                   want=F(3, 4)))
    its.append(mcq("Kavya’s water bottle holds 0.6 ℓ. What fraction of a litre is that? Give your answer in its simplest form.",
                   fr(3, 5) + " ℓ", [fr(6, 100) + " ℓ", fr(1, 6) + " ℓ", fr(2, 5) + " ℓ"],
                   "0.6 = %s = <b>%s</b>. %s ℓ is only 0.06 ℓ." % (fr(6, 10), fr(3, 5), fr(6, 100)), want=V("0.6")))
    its.append(rq("1.846", 1, ["1.9", "1.85", "2"], " So the durian is about 1.8 kg. 1.9 kg comes from rounding twice "
                  "(1.846 → 1.85 → 1.9).", unit=" kg",
                  stem="A durian has a mass of 1.846 kg. What is its mass, rounded to 1 decimal place?"))
    its.append(rq("1.376", 2, ["1.37", "1.4", "1.3"], " So Kumar is about 1.38 m tall.", unit=" m",
                  stem="Kumar is 1.376 m tall. What is his height, rounded to 2 decimal places?"))
    its.append(mcq(fig(bar_rows([("Devi", "0.6", "0.6 ℓ"), ("Raju", "0.58", "0.58 ℓ")])) +
                   "At recess, Devi drinks 0.6 ℓ of water and Raju drinks 0.58 ℓ. "
                   "Raju says he drank more because 58 &gt; 6. Who drank more?", "Devi",
                   ["Raju", "They drank the same amount", "Cannot tell"],
                   "0.6 ℓ = 0.60 ℓ. 60 hundredths &gt; 58 hundredths, so <b>Devi</b> drank more. "
                   "Compare place by place: 6 tenths &gt; 5 tenths.", same_ok=True))
    assert V("0.6") > V("0.58")
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 11, 12, 17, 18, 19]
    assert sorted(order) == list(range(20))
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Decimals in money and measurement", "items": its}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg("2.635")
    f_cmp = two_grids(45, "0.45", 50, "0.5 = 0.50")
    f_line = line_svg(240, 250, 10, dots=[(247, None)])
    f_round = line_svg(2400, 2500, 10, labels=[2400, 2450, 2500], dots=[(2470, None)])
    f_bar = bar_units(4, "1 m", "0.25 m", "4 units = 1 m, 1 unit = 0.25 m")
    return (
        "<h2>Tenths, hundredths and thousandths</h2>"
        "<p>Divide 1 whole into 10 equal parts: each part is 1 <b>tenth</b> (0.1). "
        "Divide it into 100 parts: each part is 1 <b>hundredth</b> (0.01). "
        "Divide it into 1000 parts: each part is 1 <b>thousandth</b> (0.001). "
        "Each place is worth 10 times the place to its right.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>2.635 = 2 ones, 6 tenths, 3 hundredths and 5 thousandths = 2 + 0.6 + 0.03 + 0.005.</figcaption></figure>"
        "<p>Between two hundredths there are 10 thousandths. From 0.24 to 0.25, each small space is 0.001.</p>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>The dot is 7 thousandths after 0.24, so it shows 0.247.</figcaption></figure>"
        + ex("Example 1", "Write 3 ones, 4 tenths and 9 thousandths as a decimal.",
             "There are 0 hundredths. Write 0 to hold the hundredths place: 3 . 4 0 9.", "3.409")
        + "<h2>Comparing and ordering</h2>"
        "<p>Compare the whole numbers first, then the tenths, then the hundredths, then the thousandths. "
        "It helps to give the numbers the same number of decimal places: 0.5 = 0.50 = 0.500.</p>"
        "<figure class='sn-fig'>" + f_cmp +
        "<figcaption>0.45 = 45 hundredths and 0.5 = 50 hundredths. So 0.45 &lt; 0.5, even though 45 is more than 5."
        "</figcaption></figure>"
        + ex("Example 2", "Arrange 0.5, 0.45 and 0.405 from the smallest to the greatest.",
             "Write them with 3 decimal places: 0.500, 0.450, 0.405.", "0.405, 0.45, 0.5")
        + "<h2>Decimals and fractions</h2>"
        "<p>The number of decimal places tells you the denominator: 1 place is tenths, 2 places is hundredths, "
        "3 places is thousandths. 0.3 = " + fr(3, 10) + ", 0.03 = " + fr(3, 100) + " and 0.003 = " + fr(3, 1000) + ". "
        "Then write the fraction in its simplest form.</p>"
        + ex("Example 3", "Express 0.25 as a fraction in its simplest form.",
             "0.25 = " + fr(25, 100) + ". Divide the numerator and denominator by 25.", fr(1, 4))
        + "<p>To change a fraction to a decimal, make an equivalent fraction with denominator 10 or 100.</p>"
        + ex("Example 4", "Express " + fr(3, 20) + " as a decimal.",
             "20 × 5 = 100, so " + fr(3, 20) + " = " + fr(15, 100) + ".", "0.15")
        + table(["Fraction", fr(1, 2), fr(1, 4), fr(3, 4), fr(1, 5), fr(1, 20), fr(1, 25)],
                [["Decimal", "0.5", "0.25", "0.75", "0.2", "0.05", "0.04"]])
        + "<figure class='sn-fig'>" + f_bar +
        "<figcaption>A 1 m ribbon cut into 4 equal pieces: each piece is " + fr(1, 4) + " m = 0.25 m.</figcaption></figure>"
        + "<h2>Rounding decimals</h2>"
        "<p>Find the two numbers it is between. Look at the digit <b>one place to the right</b> of the place you are "
        "rounding to: 5 or more rounds up, 4 or less rounds down. Round only once.</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>2.47 is between 2.4 and 2.5. The hundredths digit is 7, so 2.47 rounded to 1 decimal place is 2.5."
        "</figcaption></figure>"
        + table(["Round 6.381 to", "Look at", "Answer"], [
            ["the nearest whole number", "the tenths digit (3)", "6"],
            ["1 decimal place", "the hundredths digit (8)", "6.4"],
            ["2 decimal places", "the thousandths digit (1)", "6.38"]])
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.45 &gt; 0.5 because 45 &gt; 5", "Use the same places: 0.45 &lt; 0.50"],
            ["0.3 = " + fr(3, 100), "1 place after the point is tenths: 0.3 = " + fr(3, 10)],
            [fr(1, 4) + " = 0.4 and " + fr(1, 5) + " = 0.15", "Make 10 or 100 the denominator: 0.25 and 0.2"],
            ["Rounding 5.348 to 5.4 by rounding the 8 first", "Look only at the hundredths digit: 5.348 → 5.3"],
            ["Rounding 3.952 to 1 decimal place as 3.10", "10 tenths make 1 whole: 4.0"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 decimals?",
     "a": "In Primary 4, students learn place values of decimals up to 3 decimal places, compare and order decimals, change decimals to fractions and fractions to decimals, and round decimals to the nearest whole number, 1 decimal place or 2 decimal places."},
    {"q": "How do I explain why 0.5 is greater than 0.45?",
     "a": "Write 0.5 as 0.50: it is 50 hundredths, and 0.45 is only 45 hundredths. Shading both on a hundred square shows this clearly."},
    {"q": "How do you round a decimal to 2 decimal places?",
     "a": "Look at the 3rd digit after the decimal point: if it is 5 or more, round up; if it is 4 or less, round down. For example, 6.381 rounded to 2 decimal places is 6.38."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Decimals up to 3 decimal places, decimals and fractions, and rounding are part of the Primary 4 Decimals topic in the MOE 2021 Primary Mathematics Syllabus. The next P4 topics add, subtract, multiply and divide decimals."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64809)
    sets = [set_places(), set_compare(), set_fractions(), set_round(), set_problems()]
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
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "decimals", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Decimals",
        "seo_title": "P4 Decimals Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Decimals",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Decimals",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Decimals up to 3 decimal places: place values, comparing and ordering, decimals as fractions, "
                         "fractions as decimals (denominator a factor of 10 or 100), rounding",
        "meta_desc": "Free P4 maths practice on decimals: place value to 3 decimal places, comparing, "
                     "decimals and fractions, and rounding. 100 questions with answers.",
        "key_big": "Compare decimals place by place, not by how many digits they have.",
        "key_sub": "0.45 < 0.50, so 0.45 < 0.5; 0.25 = 25/100 = 1/4; 6.381 ≈ 6.38 (2 decimal places).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "place value chart|number line|bar model|ruler|coins|two hundred squares")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
