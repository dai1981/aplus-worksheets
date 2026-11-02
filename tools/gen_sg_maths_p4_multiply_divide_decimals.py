# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Multiplying and dividing decimals (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p4_multiply_divide_decimals.py
Decimals (up to 2 decimal places) × a 1-digit number (2.35 × 4 = 235 hundredths × 4 = 940 hundredths = 9.4),
decimals ÷ a 1-digit number (8.4 ÷ 3 = 84 tenths ÷ 3 = 28 tenths = 2.8), whole numbers divided to give a
decimal quotient (7 ÷ 4 = 7.00 ÷ 4 = 1.75), rounding answers to 1 or 2 decimal places (10 ÷ 3 ≈ 3.33),
then money and measurement word problems with bar models in Singapore contexts.
Every answer is computed with decimal.Decimal (never float); rounding uses ROUND_HALF_UP.
Wrong answers are real student mistakes: the decimal point in the wrong place or left out, writing the parts
side by side (2.3 × 4 = 8.12), multiplying only the whole-number part, dropping a place-holding zero
(4.08 ÷ 4 = 1.2), writing the remainder as decimal digits (7 ÷ 4 = 1 R 3 -> 1.3), reading 1 quarter as 0.4,
dividing the wrong way round, cutting off digits instead of rounding, rounding to the wrong place,
and adding instead of multiplying.
Singapore style: British spelling, $ and ¢, ℓ and m. 4-digit numbers have no separator; 5 or more digits use
a no-break space. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP, getcontext

getcontext().prec = 30
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
INK = "#2b2b2b"
RED = "#c0392b"
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, Singapore style: 4536, 12 350 (no-break space), 0.45."""
    d = Dm(str(x).replace(NB, "").replace(" ", "")).normalize()
    s = format(d, "f")
    w, _, f = s.partition(".")
    if len(w) >= 5:
        g = []
        while w:
            g.insert(0, w[-3:])
            w = w[:-3]
        w = NB.join(g)
    return w + ("." + f if f else "")


def M(x):
    """Money: $22, $8.50."""
    d = Dm(x)
    if d == d.to_integral_value():
        return "$" + N(d)
    q = format(d.quantize(Dm("0.01")), "f")
    assert Dm(q) == d, x
    w, _, f = q.partition(".")
    return "$" + N(w) + "." + f


def R(x, dp):
    """Round half up to dp decimal places and keep the trailing zeros: R(0.95, 1) = '1.0'."""
    return format(Dm(x).quantize(Dm(1).scaleb(-dp), rounding=ROUND_HALF_UP), "f")


def show(x, n):
    """Decimal text with n decimal places and '…' if it goes on: 3.333…"""
    d = Dm(x)
    t = format(d.quantize(Dm(1).scaleb(-n), rounding="ROUND_DOWN"), "f")
    return t + ("…" if Dm(t) != d else "")


def places(x):
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


VAL = re.compile(r"^(\$)?([\d" + NB + r"]*\.?\d+) ?(.*)$")


def val(c):
    """(value, unit) of a choice; None if it is not a single number."""
    m = VAL.match(c)
    if not m:
        return None
    rest = m.group(3).strip()
    if rest and not re.match(r"^([a-zA-Z]+|ℓ)$", rest):
        return None
    return (Dm(m.group(2).replace(NB, "")), "$" if m.group(1) else rest)


def mcq(q, correct, wrong, e, same_ok=False, want=None):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (and unit).
    want: the true value of the correct choice (checked)."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
    if want is not None:
        assert val(correct)[0] == Dm(str(want)), (q, correct, want)
    if not same_ok:
        vs = [val(x) for x in ch]
        assert all(v is not None for v in vs), (q, ch)
        assert len(set(vs)) == 4, (q, ch)
        assert len({v[1] for v in vs}) == 1, (q, ch)
        assert all(v[0] > 0 for v in vs), (q, ch)
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


def frac(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


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
        elif ch in "m×÷?":
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


# ------------------------------------------------------------ figure: number line with equal jumps
def jumps_svg(step, n, end):
    """Number line from 0 to the whole number `end`, tenths ticks, n equal jumps of `step` from 0."""
    step = Dm(step)
    total = step * n
    assert total <= end and end == int(end)
    U = min(400, 600 // int(end))
    L, R_ = 22, 22
    W = L + U * int(end) + R_
    AY = 74
    H = AY + 38
    X = lambda v: L + float(v) * U
    o = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 8, AY, W - R_ + 8, AY, INK)]
    for t in range(int(end) * 10 + 1):
        x = X(Dm(t) / 10)
        big = t % 10 == 0
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, AY - (10 if big else 6), x, AY + (10 if big else 6), INK if big else THIN, "2.5" if big else "1.5"))
        if big:
            o.append(text(x, AY + 30, str(t // 10), 17))
    hgt = 26
    for i in range(n):
        a, b = X(step * i), X(step * (i + 1))
        m = (a + b) / 2.0
        o.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (a, AY - 2, m, AY - 2 - 2 * hgt, b - 2, AY - 4, GREEN))
        o.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (b, AY - 2, b - 9, AY - 10, b - 3, AY - 13, GREEN))
        o.append(text(m, AY - hgt - 8, "+" + N(step), 14, col=GREEN))
    o.append("<circle cx='%.1f' cy='%d' r='5' fill='%s'/>" % (X(0), AY, INK))
    o.append("<circle cx='%.1f' cy='%d' r='5.5' fill='%s'/>" % (X(total), AY, RED))
    lab = "number line from 0 to %s with %d jumps of %s, ending at %s" % (N(end), n, N(step), N(total))
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: split model for decimal × 1-digit number
def split_svg(x, n):
    """Rectangle split into the whole-number part and the decimal part, widths to scale. Each part shows its product."""
    x = Dm(x)
    w = int(x)
    f = x - w
    assert w >= 1 and 0 < f < 1
    U = min(Dm(130), Dm(340) / x)
    WW, WF = float(w * U), float(f * U)
    assert WF >= 36, (x, WF)
    LW, TOP, HH, PAD = 34, 30, 64, 4
    x0 = PAD + LW
    W = int(x0 + WW + WF + PAD + 0.99)
    H = TOP + HH + PAD
    assert tw("%d × %s = %s" % (n, N(w), N(n * w)), 17) <= WW - 6
    assert tw(N(n * f), 15) <= WF - 4
    o = ["<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x0, TOP, WW, HH, HEADFILL, GREEN),
         "<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
         % (x0 + WW, TOP, WF, HH, PARTFILL, ORANGE)]
    o.append(text(x0 + WW / 2, TOP - 9, N(w), 17, col=GREEN))
    o.append(text(x0 + WW + WF / 2, TOP - 9, N(f), 15, col=ORANGE))
    o.append(text(x0 - 10, TOP + HH / 2 + 6, str(n), 17, anchor="end"))
    o.append(text(x0 + WW / 2, TOP + HH / 2 + 7, "%d × %s = %s" % (n, N(w), N(n * w)), 17))
    o.append(text(x0 + WW + WF / 2, TOP + HH / 2 + 6, N(n * f), 15, col=ORANGE))
    lab = ("split model: %s × %d as %s × %d plus %s × %d, parts %s and %s"
           % (N(x), n, N(w), n, N(f), n, N(n * w), N(n * f)))
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: long division
def point_mark(x, y, fs, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, y - fs * 0.06, fs * 0.1, col)


def ld_svg(dividend, d, quot=None, fs=24):
    """Long division of `dividend` (text, e.g. '8.52' or '7.00') by a 1-digit number.
    quot: None, 'digits' (quotient digits, point left out) or 'full'. The quotient point sits above the dividend point."""
    ds = dividend.replace(".", "")
    k = places(dividend)
    pi = len(ds) - 1 - k
    qv = Dm(dividend) / d
    qi = qv * 10 ** k
    assert qi == int(qi), (dividend, d)
    qs = str(int(qi)).rjust(len(ds), "0")
    qcols = [(j, ch) for j, ch in enumerate(qs) if j >= pi or ch != "0" or any(c != "0" for c in qs[:j])]
    cw = fs * 0.95
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18
    rh = fs * 1.25
    top = (rh + 6) if quot else 10
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for i, ch in enumerate(reversed(txt)):
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - i), y, fs, colr, ch))

    by = top + rh - fs * 0.18
    digits_at(ds, len(ds) - 1, by)
    if k:
        s.append(point_mark(x0 + cw * (pi + 1), by, fs))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * len(ds) + 10
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))
    H = top + bh + 8
    if quot:
        for j, ch in qcols:
            digits_at(ch, j, top - 8, GREEN)
        if quot == "full" and k:
            s.append(point_mark(x0 + cw * (pi + 1), top - 8, fs, GREEN))
    label = "%s divided by %d written as long division" % (dividend, d)
    if quot == "digits":
        label += " with the quotient digits but no decimal point"
    elif quot == "full":
        label += ", quotient %s" % N(qv)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


# ------------------------------------------------------------ figure: rounding number line
def rline_svg(lo, step, point, plab=None):
    """Number line from lo to lo + 10 steps. Both ends and the half-way mark are labelled.
    A red arrow marks `point` (it may lie between ticks), labelled plab."""
    lo, step, point = Dm(lo), Dm(step), Dm(point)
    hi = lo + step * 10
    assert lo < point < hi
    L, R_, PX = 40, 40, 52
    W = L + PX * 10 + R_
    AY = 58
    H = AY + 40
    X = lambda v: L + float((Dm(v) - lo) / step) * PX
    o = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 14, AY, W - R_ + 14, AY, INK)]
    for i in range(11):
        x = X(lo + step * i)
        big = i in (0, 10)
        mid = i == 5
        hgt = 12 if big else (9 if mid else 6)
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, AY - hgt, x, AY + hgt, INK if (big or mid) else THIN, "2.5" if big else ("2" if mid else "1.5")))
        if big:
            o.append(text(x, AY + 32, N(lo + step * i), 18))
        elif mid:
            o.append(text(x, AY + 30, N(lo + step * i), 15, col=GREEN))
    xp = X(point)
    o.append("<path d='M%.1f %d L%.1f %d' stroke='%s' stroke-width='3'/>" % (xp, 24, xp, AY - 13, RED))
    o.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (xp, AY - 3, xp - 6, AY - 14, xp + 6, AY - 14, RED))
    t = plab or N(point)
    o.append(text(xp, 18, t, 16, col=RED))
    lab = "rounding number line from %s to %s with the half-way mark %s, an arrow at %s" % (
        N(lo), N(hi), N(lo + step * 5), t)
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figures: bar models
def brace(x1, x2, y, up, lab, col=INK):
    """Bracket from x1 to x2 at y; ticks point to the bar (down if up=True). Label beyond it."""
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_units(n, total_lab, unit_lab, note, BW=540):
    """One bar of n equal units, every unit labelled unit_lab (only the first one when it is '?'). Bracket above with total_lab.
    A note (e.g. '3 units = $25.50') is written under the bar."""
    X0, TOP, BH = 10, 34, 38
    uw = BW / float(n)
    assert tw(unit_lab, 16) <= uw - 4, (unit_lab, uw)
    W = X0 * 2 + BW
    H = TOP + BH + 34
    o = [brace(X0, X0 + BW, 22, True, total_lab, col=RED if total_lab == "?" else INK)]
    for i in range(n):
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s'/>"
                 % (X0 + uw * i, TOP, uw, BH, PARTFILL if i == 0 else HEADFILL))
    o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>"
             % (X0, TOP, BW, BH, GREEN))
    for i in range(1, n):
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5'/>"
                 % (X0 + uw * i, TOP, X0 + uw * i, TOP + BH, GREEN))
    for i in range(1 if unit_lab == "?" else n):
        o.append(text(X0 + uw * (i + 0.5), TOP + BH / 2.0 + 6, unit_lab, 16, col=RED if unit_lab == "?" else INK))
    o.append(text(X0, TOP + BH + 24, note, 16, anchor="start", col=GREEN))
    return svg_wrap(W, H, "".join(o), "bar model: %d equal units, total %s, 1 unit %s" % (n, total_lab, unit_lab))


def bar_parts(parts, total_lab, BW=540):
    """One bar split into parts drawn to scale. parts = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(Dm(v) for v, _ in parts)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [HEADFILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts):
        w = float(Dm(v) / tot) * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts), total_lab))


def bar_times(rows, unit_lab, a, b, q_lab, UW=130):
    """Comparison model of equal units. rows = [(name, units)]. Every unit shows unit_lab.
    A bracket under units a..b-1 of the last row shows q_lab."""
    LW = int(max(tw(nm, 16) for nm, _ in rows)) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 14
    x0 = X0 + LW
    W = x0 + UW * max(u for _, u in rows) + 10
    H = TOP + len(rows) * BH + (len(rows) - 1) * GAP + 40
    assert tw(unit_lab, 16) <= UW - 6
    o = []
    for r, (nm, units) in enumerate(rows):
        y = TOP + r * (BH + GAP)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        for i in range(units):
            o.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x0 + UW * i, y, UW, BH, HEADFILL if r == 0 else PARTFILL, GREEN))
            o.append(text(x0 + UW * (i + 0.5), y + BH / 2.0 + 6, unit_lab, 16))
    yb = TOP + len(rows) * BH + (len(rows) - 1) * GAP + 8
    o.append(brace(x0 + UW * a, x0 + UW * b, yb, False, q_lab, col=RED if q_lab == "?" else INK))
    lab = "bar model: " + ", ".join("%s %d unit%s" % (nm, u, "" if u == 1 else "s") for nm, u in rows) + \
          ", each unit %s, bracket %s" % (unit_lab, q_lab)
    return svg_wrap(int(W), H, "".join(o), lab)


# ------------------------------------------------------------ explanations
def unit_word(k, n=2):
    return {0: ("one", "ones"), 1: ("tenth", "tenths"), 2: ("hundredth", "hundredths"),
            3: ("thousandth", "thousandths")}[k][0 if n == 1 else 1]


def mul_e(x, n, note=""):
    """2.35 × 4: 2.35 is 235 hundredths. 235 × 4 = 940, so 2.35 × 4 = 940 hundredths = 9.4."""
    k = places(x)
    whole = int(Dm(x) * 10 ** k)
    p = whole * n
    r = Dm(x) * n
    e = ("%s is %s %s. %s × %d = %s, so %s × %d = %s %s = <b>%s</b>."
         % (x, N(whole), unit_word(k, whole), N(whole), n, N(p), x, n, N(p), unit_word(k, p), N(r)))
    if note:
        e += " " + note
    return e


def mul(x, n, wrong, note=""):
    r = Dm(x) * n
    return mcq("%s × %d = ?" % (x, n), N(r), wrong, mul_e(x, n, note), want=r)


def div_e(x, n, note=""):
    """8.4 ÷ 3: 8.4 is 84 tenths. 84 ÷ 3 = 28, so 8.4 ÷ 3 = 28 tenths = 2.8.
    If the tenths do not share equally, rename as hundredths first: 4.5 = 4.50 = 450 hundredths."""
    k = places(x)
    while int(Dm(x) * 10 ** k) % n:
        k += 1
    whole = int(Dm(x) * 10 ** k)
    r = Dm(x) / n
    assert r * n == Dm(x) and k <= 2
    pre = ""
    if k > places(x):
        xs = format(Dm(x).quantize(Dm(1).scaleb(-k)), "f")
        pre = "Write %s as %s. " % (x, xs)
        x_show = xs
    else:
        x_show = x
    e = (pre + "%s is %s %s. %s ÷ %d = %s, so %s ÷ %d = %s %s = <b>%s</b>. Check: %s × %d = %s."
         % (x_show, N(whole), unit_word(k), N(whole), n, N(whole // n), x, n, N(whole // n),
            unit_word(k, whole // n), N(r), N(r), n, x))
    if note:
        e += " " + note
    return e


def div(x, n, wrong, note=""):
    r = Dm(x) / n
    return mcq("%s ÷ %d = ?" % (x, n), N(r), wrong, div_e(x, n, note), want=r)


def wd_e(a, b, note=""):
    """7 ÷ 4 = 1 R 3. Rename 3 ones as 30 tenths ... = 1.75."""
    q, r = divmod(a, b)
    v = Dm(a) / b
    k = places(N(v))
    assert v * b == a and 1 <= k <= 2 and r > 0
    xs = format(Dm(a).quantize(Dm(1).scaleb(-k)), "f")
    e = ("%d ÷ %d = %d R %d. Do not stop at the remainder: write %d as %s and keep dividing. "
         "The %d one%s left over make%s %d tenths. %d ÷ %d = <b>%s</b>. Check: %s × %d = %d."
         % (a, b, q, r, a, xs, r, "" if r == 1 else "s", "s" if r == 1 else "", r * 10, a, b, N(v), N(v), b, a))
    if note:
        e += " " + note
    return e


def wd(a, b, wrong, note=""):
    v = Dm(a) / b
    return mcq("%d ÷ %d = ?" % (a, b), N(v), wrong, wd_e(a, b, note), want=v)


def rnd_e(x, dp, shown=None, note=""):
    """Look at the next digit: 5 or more, round up; less than 5, keep."""
    x = Dm(x)
    nxt = int(show(x, dp + 1).rstrip("…")[-1])
    r = R(x, dp)
    place = {1: "tenths", 2: "hundredths"}[dp]
    look = {1: "hundredths", 2: "thousandths"}[dp]
    s = shown or (N(x) if places(N(x)) <= 3 else show(x, dp + 1))
    e = ("To round to %d decimal place%s, look at the %s digit of %s: it is %d. "
         % (dp, "" if dp == 1 else "s", look, s, nxt))
    if nxt >= 5:
        e += "It is 5 or more, so round the %s digit up. " % place
    else:
        e += "It is less than 5, so the %s digit stays the same. " % place
    e += "%s ≈ <b>%s</b>." % (s, r)
    if note:
        e += " " + note
    return e


# ============================================================ set 1: decimal × 1-digit number
def set_mul():
    its = []
    assert Dm("0.4") * 3 == Dm("1.2")
    its.append(mcq(fig(jumps_svg("0.4", 3, 2)) + "The number line shows 3 jumps of 0.4. What is 0.4 × 3?",
                   "1.2", ["12", "0.12", "3.4"],
                   mul_e("0.4", 3, "The red dot is 2 small marks past 1, at 1.2. 3.4 adds 3 + 0.4 instead of multiplying."),
                   want="1.2"))
    assert Dm("0.6") * 4 == Dm("2.4")
    its.append(mcq(fig(jumps_svg("0.6", 4, 3)) + "The number line shows 4 jumps of 0.6. What is 0.6 × 4?",
                   "2.4", ["24", "0.24", "4.6"],
                   mul_e("0.6", 4, "The red dot is 4 small marks past 2, at 2.4."), want="2.4"))
    its.append(mul("0.3", 2, ["6", "0.06", "2.3"], "0.06 is 6 hundredths, not 6 tenths."))
    its.append(mul("0.7", 5, ["35", "0.35", "5.7"], "35 leaves out the decimal point. 5.7 adds instead of multiplying."))
    its.append(mul("1.2", 3, ["36", "0.36", "4.2"], "4.2 adds 1.2 + 3 instead of multiplying."))
    assert Dm("2.3") * 4 == Dm("9.2")
    its.append(mcq(fig(split_svg("2.3", 4)) + "The model splits 2.3 × 4 into 2 × 4 and 0.3 × 4. What is 2.3 × 4?",
                   "9.2", ["8.12", "92", "8.3"],
                   "2 × 4 = 8 and 0.3 × 4 = 1.2. Add the parts: 8 + 1.2 = <b>9.2</b>. "
                   "8.12 writes 8 and 12 side by side instead of adding. 8.3 forgets to multiply the 0.3.", want="9.2"))
    assert Dm("3.6") * 2 == Dm("7.2")
    its.append(mcq(fig(split_svg("3.6", 2)) + "The model splits 3.6 × 2 into 3 × 2 and 0.6 × 2. What is 3.6 × 2?",
                   "7.2", ["6.12", "72", "6.6"],
                   "3 × 2 = 6 and 0.6 × 2 = 1.2. Add the parts: 6 + 1.2 = <b>7.2</b>. "
                   "6.12 writes 6 and 12 side by side. 6.6 forgets to multiply the 0.6.", want="7.2"))
    its.append(mul("0.08", 6, ["4.8", "0.048", "6.08"], "4.8 is 48 tenths, but the answer is 48 hundredths."))
    its.append(mul("2.35", 4, ["8.14", "94", "0.94"],
                   "8.14 writes 2 × 4 = 8 and 0.35 × 4 = 1.4 side by side: add them, 8 + 1.4 = 9.4. "
                   "Estimate: 2 × 4 = 8, so the answer is a bit more than 8."))
    its.append(mul("4.5", 6, ["2.7", "270", "24.3"],
                   "24.3 writes 4 × 6 = 24 and 0.5 × 6 = 3 side by side: add them, 24 + 3 = 27."))
    its.append(mul("1.25", 3, ["37.5", "0.375", "4.25"], "4.25 adds 1.25 + 3 instead of multiplying."))
    its.append(mul("0.45", 7, ["31.5", "0.315", "7.45"], "0.45 × 7 must be less than 7, so 31.5 cannot be right."))
    assert Dm("0.7") * 4 == Dm("2.8")
    its.append(mcq("? × 4 = 2.8", "0.7", ["7", "0.07", "11.2"],
                   "Use the inverse: 2.8 ÷ 4. 2.8 is 28 tenths, and 28 ÷ 4 = 7, so the answer is 7 tenths = <b>0.7</b>. "
                   "Check: 0.7 × 4 = 2.8. 11.2 is 2.8 × 4.", want="0.7"))
    assert 47 * 6 == 282 and Dm("4.7") * 6 == Dm("28.2")
    its.append(mcq("Use 47 × 6 = 282 to find <b>4.7 × 6</b>.", "28.2", ["282", "2.82", "0.282"],
                   "4.7 is 47 tenths, so the answer is 282 tenths = <b>28.2</b>. Estimate: 5 × 6 = 30.", want="28.2"))
    assert 135 * 7 == 945 and Dm("1.35") * 7 == Dm("9.45")
    its.append(mcq("Use 135 × 7 = 945 to find <b>1.35 × 7</b>.", "9.45", ["94.5", "0.945", "945"],
                   "1.35 is 135 hundredths, so the answer is 945 hundredths = <b>9.45</b>. "
                   "Estimate: 1 × 7 = 7 and 2 × 7 = 14, so the answer is between 7 and 14.", want="9.45"))
    its.append(mul("3.08", 5, ["154", "1.54", "19"],
                   "19 drops the 0 in the tenths place: it works out 3.8 × 5 instead of 3.08 × 5."))
    its.append(mul("6.7", 8, ["48.56", "536", "5.36"],
                   "48.56 writes 6 × 8 = 48 and 0.7 × 8 = 5.6 side by side: add them, 48 + 5.6 = 53.6."))
    its.append(mul("5.06", 9, ["455.4", "4.554", "50.4"],
                   "50.4 drops the 0 in the tenths place: it works out 5.6 × 9. Estimate: 5 × 9 = 45."))
    assert Dm("1.4") * 3 == Dm("4.2")
    its.append(mcq("Ali says 1.4 × 3 = 3.12. What is the correct answer?", "4.2", ["3.12", "42", "0.42"],
                   "1 × 3 = 3 and 0.4 × 3 = 1.2. Ali wrote 3 and 12 side by side. Add the parts: "
                   "3 + 1.2 = <b>4.2</b>.", want="4.2"))
    assert 21 < Dm("3.8") * 7 < 28
    its.append(mcq("Without working it out, between which two numbers is <b>3.8 × 7</b>?", "21 and 28",
                   ["2 and 3", "210 and 280", "28 and 35"],
                   "3.8 is between 3 and 4, so 3.8 × 7 is between 3 × 7 = 21 and 4 × 7 = 28. "
                   "In fact 3.8 × 7 = 26.6.", same_ok=True))
    return {"title": "Decimals × a 1-digit number", "items": its}


# ============================================================ set 2: decimal ÷ 1-digit number
def set_div():
    its = []
    its.append(div("0.9", 3, ["3", "0.03", "2.7"], "2.7 multiplies instead of dividing."))
    its.append(div("4.8", 4, ["12", "0.12", "1.8"], "1.8 divides only the 4 ones and forgets the 8 tenths."))
    its.append(div("6.6", 2, ["33", "0.33", "13.2"], "13.2 multiplies instead of dividing."))
    its.append(div("8.4", 3, ["28", "0.28", "25.2"],
                   "In long division: 8 ones ÷ 3 = 2 ones R 2 ones. Rename 2 ones as 20 tenths: 20 + 4 = 24 tenths. "
                   "24 tenths ÷ 3 = 8 tenths."))
    its.append(div("2.4", 8, ["3", "0.03", "19.2"], "2.4 is less than 8, so the answer is less than 1."))
    assert Dm(7) / Dm("3.5") == 2
    its.append(div("3.5", 7, ["5", "0.05", "2"],
                   "2 is 7 ÷ 3.5: it divides the wrong way round. 3.5 is less than 7, so the answer is less than 1."))
    its.append(div("9.6", 4, ["24", "0.24", "38.4"], "Estimate: 8 ÷ 4 = 2, so the answer is a bit more than 2."))
    assert Dm("7.2") / 6 == Dm("1.2")
    its.append(mcq("Hui Min says 7.2 ÷ 6 = 12. What is the correct answer?", "1.2", ["12", "0.12", "43.2"],
                   "7.2 is 72 tenths. 72 ÷ 6 = 12, so 7.2 ÷ 6 = 12 tenths = <b>1.2</b>. "
                   "Estimate: 6 ÷ 6 = 1, so the answer is about 1, not about 12. Hui Min left out the decimal point.",
                   want="1.2"))
    its.append(div("13.5", 9, ["15", "0.15", "121.5"], "Estimate: 9 ÷ 9 = 1 and 18 ÷ 9 = 2, so the answer is between 1 and 2."))
    its.append(div("16.2", 6, ["27", "0.27", "97.2"], "Estimate: 18 ÷ 6 = 3, so the answer is a bit less than 3."))
    its.append(div("4.08", 4, ["1.2", "10.2", "0.102"],
                   "1.2 drops the 0 that holds the tenths place: 0 tenths ÷ 4 is 0 tenths, so write 0."))
    its.append(div("6.18", 6, ["1.3", "10.3", "103"],
                   "1.3 drops the 0 that holds the tenths place: 1 tenth ÷ 6 is 0 tenths R 1 tenth, so write 0."))
    its.append(div("0.72", 9, ["0.8", "8", "6.48"], "0.8 is 8 tenths, but the answer is 8 hundredths."))
    its.append(div("8.55", 5, ["17.1", "0.171", "42.75"],
                   "Estimate: 10 ÷ 5 = 2, so the answer is a bit less than 2. 42.75 multiplies by 5."))
    its.append(div("9.24", 4, ["23.1", "0.231", "36.96"],
                   "Estimate: 8 ÷ 4 = 2, so the answer is a bit more than 2. 36.96 multiplies by 4."))
    assert Dm("8.52") / 4 == Dm("2.13")
    its.append(mcq(fig(ld_svg("8.52", 4, "digits")) +
                   "The quotient digits for 8.52 ÷ 4 are 2, 1, 3. Where does the decimal point go?",
                   "2.13", ["21.3", "213", "0.213"],
                   "Put the decimal point in the quotient straight above the point in 8.52. "
                   "Estimate: 8 ÷ 4 = 2, so the answer is about 2. 8.52 ÷ 4 = <b>2.13</b>.", want="2.13"))
    assert Dm("6.95") / 5 == Dm("1.39")
    its.append(mcq(fig(ld_svg("6.95", 5, "digits")) +
                   "The quotient digits for 6.95 ÷ 5 are 1, 3, 9. What is 6.95 ÷ 5?",
                   "1.39", ["13.9", "139", "0.139"],
                   "The point in the quotient goes straight above the point in 6.95. Estimate: 5 ÷ 5 = 1 and 10 ÷ 5 = 2, "
                   "so the answer is between 1 and 2. 6.95 ÷ 5 = <b>1.39</b>. Check: 1.39 × 5 = 6.95.", want="1.39"))
    its.append(div("4.5", 2, ["2.2", "2.21", "22.5"],
                   "2.2 stops too early: 4.5 ÷ 2 = 2.2 R 0.1. 2.21 writes the remainder 1 as a digit. "
                   "Rename the 1 tenth left over as 10 hundredths and keep dividing: 10 hundredths ÷ 2 = 5 hundredths."))
    assert Dm("7.35") / 5 == Dm("1.47")
    its.append(mcq("7.35 is 735 hundredths. What is 735 hundredths ÷ 5?", "147 hundredths",
                   ["147 tenths", "147 ones", "147 thousandths"],
                   "735 ÷ 5 = 147, and the unit stays the same: <b>147 hundredths</b> = 1.47. "
                   "So 7.35 ÷ 5 = 1.47.", same_ok=True))
    vals = {"5.6 ÷ 8": Dm("5.6") / 8, "9.6 ÷ 8": Dm("9.6") / 8, "8.8 ÷ 8": Dm("8.8") / 8, "16.8 ÷ 8": Dm("16.8") / 8}
    assert [k for k, v in vals.items() if v < 1] == ["5.6 ÷ 8"]
    its.append(mcq("Which answer is <b>less than 1</b>?", "5.6 ÷ 8", ["9.6 ÷ 8", "8.8 ÷ 8", "16.8 ÷ 8"],
                   "The answer is less than 1 when the number you divide is less than the number you divide by. "
                   "Only 5.6 is less than 8, so only <b>5.6 ÷ 8</b> is less than 1 (it is 0.7).", same_ok=True))
    return {"title": "Decimals ÷ a 1-digit number", "items": its}


# ============================================================ set 3: whole number ÷ whole number as a decimal
def set_whole():
    its = []
    its.append(wd(9, 2, ["4.1", "45", "0.45"], "4.1 writes the remainder 1 as a decimal digit."))
    its.append(wd(1, 2, ["0.1", "2", "5"], "0.1 writes the remainder 1 as a decimal digit. 2 divides the wrong way round."))
    its.append(wd(6, 5, ["1.1", "12", "0.12"], "1.1 writes the remainder 1 as a decimal digit."))
    its.append(wd(3, 4, ["0.3", "7.5", "0.075"],
                   "3 is less than 4, so the answer is less than 1. 0.3 writes the remainder 3 as a decimal digit."))
    assert Dm(7) / 4 == Dm("1.75")
    its.append(mcq(fig(ld_svg("7.00", 4, "digits")) +
                   "To find 7 ÷ 4, Siti writes 7 as 7.00. The quotient digits are 1, 7, 5. What is 7 ÷ 4?",
                   "1.75", ["1.3", "17.5", "0.175"],
                   wd_e(7, 4, "1.3 writes the remainder 3 as a decimal digit. The point in the quotient goes straight "
                              "above the point in 7.00."), want="1.75"))
    its.append(wd(13, 5, ["2.3", "26", "0.26"], "2.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(9, 6, ["1.3", "15", "0.15"], "1.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(3, 5, ["0.3", "6", "0.06"], "0.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(11, 4, ["2.3", "27.5", "0.275"], "2.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(27, 6, ["4.3", "45", "0.45"], "4.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(9, 4, ["2.1", "22.5", "0.225"], "2.1 writes the remainder 1 as a decimal digit."))
    its.append(wd(21, 4, ["5.1", "5.4", "52.5"],
                   "5.1 writes the remainder 1 as a decimal digit. 5.4 reads 1 quarter as 0.4, but "
                   "1 quarter = 0.25."))
    assert Dm(13) / 4 == Dm("3.25")
    its.append(mcq(fig(ld_svg("13.00", 4, "digits")) +
                   "13 ÷ 4 is written as 13.00 ÷ 4. The quotient digits are 3, 2, 5. Where does the decimal point go?",
                   "3.25", ["32.5", "325", "0.325"],
                   "The point in the quotient goes straight above the point in 13.00. Estimate: 12 ÷ 4 = 3, "
                   "so the answer is about 3. 13 ÷ 4 = <b>3.25</b>.", want="3.25"))
    its.append(wd(19, 4, ["4.3", "47.5", "0.475"], "4.3 writes the remainder 3 as a decimal digit."))
    its.append(wd(30, 8, ["3.6", "37.5", "0.375"], "3.6 writes the remainder 6 as a decimal digit."))
    assert Dm(5) / 4 == Dm("1.25")
    its.append(mcq("5 ÷ 4 = 1 R 1. Kumar writes 5 ÷ 4 = 1.1. What is the correct answer?", "1.25",
                   ["1.1", "1.4", "12.5"],
                   wd_e(5, 4, "Kumar wrote the remainder 1 as a decimal digit. 1.4 reads 1 quarter as 0.4."), want="1.25"))
    assert Dm(1) / 4 == Dm("0.25")
    its.append(mcq(frac(1, 4) + " = 1 ÷ 4. Write " + frac(1, 4) + " as a decimal.", "0.25", ["0.4", "0.14", "4"],
                   "1 ÷ 4: write 1 as 1.00. 100 hundredths ÷ 4 = 25 hundredths, so " + frac(1, 4) + " = <b>0.25</b>. "
                   "0.4 and 0.14 copy the digits of the fraction. 4 is 4 ÷ 1.", want="0.25"))
    assert Dm(2) / 5 == Dm("0.4")
    its.append(mcq(frac(2, 5) + " = 2 ÷ 5. Write " + frac(2, 5) + " as a decimal.", "0.4", ["2.5", "0.25", "0.2"],
                   "2 ÷ 5: write 2 as 2.0. 20 tenths ÷ 5 = 4 tenths, so " + frac(2, 5) + " = <b>0.4</b>. "
                   "2.5 is 5 ÷ 2: it divides the wrong way round. 0.25 copies the digits. 0.2 uses only the 2.", want="0.4"))
    assert Dm(5) / 2 == Dm("2.5")
    its.append(mcq("Which division has the answer <b>2.5</b>?", "5 ÷ 2", ["2 ÷ 5", "10 ÷ 5", "7 ÷ 2"],
                   "5 ÷ 2 = 2 R 1, and 1 one = 10 tenths, 10 tenths ÷ 2 = 5 tenths. So <b>5 ÷ 2</b> = 2.5. "
                   "2 ÷ 5 = 0.4, 10 ÷ 5 = 2 and 7 ÷ 2 = 3.5.", same_ok=True))
    assert Dm(15) / 4 == Dm("3.75")
    its.append(mcq("Which is the same as 15 ÷ 4?", "3.75", ["3.3", "3.4", "37.5"],
                   wd_e(15, 4, "3.3 writes the remainder 3 as a decimal digit. 3.4 is 3 and 4 tenths, not 3 and "
                               "3 quarters."), want="3.75"))
    order = [0, 1, 2, 3, 4, 5, 7, 6, 8, 10, 9, 13, 12, 14, 15, 16, 17, 18, 11, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Whole numbers ÷ a 1-digit number: answers as decimals", "items": [its[i] for i in order]}


# ============================================================ set 4: rounding answers
def set_round():
    its = []

    def rq(q, x, dp, wrong, shown=None, note="", figure=""):
        r = R(x, dp)
        return mcq(figure + q, r, wrong, rnd_e(x, dp, shown, note), want=r)

    its.append(rq("The arrow is at 2.67. Round 2.67 to 1 decimal place.", "2.67", 1, ["2.6", "3", "2.67"],
                  note="2.6 cuts off the 7 instead of rounding. On the number line, 2.67 is nearer to 2.7 than to 2.6.",
                  figure=fig(rline_svg("2.6", "0.01", "2.67"))))
    its.append(rq("The arrow is at 4.32. Round 4.32 to 1 decimal place.", "4.32", 1, ["4.4", "4", "4.32"],
                  note="4.32 is before the half-way mark 4.35, so it is nearer to 4.3.",
                  figure=fig(rline_svg("4.3", "0.01", "4.32"))))
    its.append(rq("Round 5.48 to 1 decimal place.", "5.48", 1, ["5.4", "5", "5.48"],
                  note="5.4 cuts off the 8 instead of rounding. 5 rounds to the nearest whole number."))
    its.append(rq("Round 3.456 to 2 decimal places.", "3.456", 2, ["3.45", "3.5", "3.4"],
                  note="3.45 cuts off the 6. 3.5 is rounded to 1 decimal place, not 2."))
    its.append(rq("Round 7.249 to 1 decimal place.", "7.249", 1, ["7.3", "7.25", "7"],
                  note="7.3 rounds twice (7.249 → 7.25 → 7.3). Only look at the hundredths digit, 4."))
    its.append(rq("Round 0.95 to 1 decimal place.", "0.95", 1, ["0.9", "0.10", "0.95"],
                  note="9 tenths + 1 tenth = 10 tenths = 1 whole, so the answer is 1.0. Write the 0 to show 1 decimal place."))
    its.append(rq("Round 12.051 to 2 decimal places.", "12.051", 2, ["12.06", "12.1", "12.5"],
                  note="12.06 rounds up even though the next digit is only 1. 12.5 drops the 0 in the tenths place."))
    assert R("5.136", 2) == "5.14"
    its.append(rq("The arrow is at 5.136. Round 5.136 to 2 decimal places.", "5.136", 2, ["5.13", "5.1", "5.2"],
                  note="5.136 is past the half-way mark 5.135, so it is nearer to 5.14.",
                  figure=fig(rline_svg("5.13", "0.001", "5.136"))))
    assert show(Dm(10) / 3, 3) == "3.333…"
    its.append(rq("10 ÷ 3 = 3.333… Round the answer to 1 decimal place.", Dm(10) / 3, 1, ["3.4", "3", "3.33"],
                  shown="3.333…", note="3.33 is rounded to 2 decimal places, not 1.",
                  figure=fig(rline_svg("3.3", "0.01", Dm(10) / 3, "3.333…"))))
    its.append(rq("Find 10 ÷ 3. Round your answer to 2 decimal places.", Dm(10) / 3, 2, ["3.3", "3.34", "3.1"],
                  shown="3.333…", note="10 ÷ 3 = 3 R 1, so 3.1 writes the remainder as a digit. Divide to 3 decimal "
                                       "places (3.333), then round."))
    its.append(rq("Find 2 ÷ 3. Round your answer to 2 decimal places.", Dm(2) / 3, 2, ["0.66", "0.7", "1.5"],
                  shown="0.666…", note="0.66 cuts off the digits instead of rounding. 1.5 is 3 ÷ 2."))
    its.append(rq("Find 5 ÷ 3. Round your answer to 1 decimal place.", Dm(5) / 3, 1, ["1.6", "1.2", "0.6"],
                  shown="1.66…", note="1.6 cuts off the digits. 1.2 writes the remainder 2 as a digit. 0.6 is 3 ÷ 5."))
    its.append(rq("Find 7 ÷ 6. Round your answer to 1 decimal place.", Dm(7) / 6, 1, ["1.1", "1.17", "0.9"],
                  shown="1.16…", note="1.1 cuts off the digits (or writes the remainder 1 as a digit). "
                                      "1.17 is rounded to 2 decimal places."))
    its.append(rq("Find 8 ÷ 7. Round your answer to 2 decimal places.", Dm(8) / 7, 2, ["1.1", "1.15", "0.88"],
                  shown="1.142…", note="0.88 is 7 ÷ 8, which divides the wrong way round."))
    its.append(rq("Find 4.7 ÷ 3. Round your answer to 2 decimal places.", Dm("4.7") / 3, 2, ["1.56", "1.6", "14.1"],
                  shown="1.566…", note="1.56 cuts off the digits. 14.1 multiplies instead of dividing."))
    its.append(rq("Find 5.2 ÷ 6. Round your answer to 1 decimal place.", Dm("5.2") / 6, 1, ["0.8", "0.87", "31.2"],
                  shown="0.86…", note="0.8 cuts off the digits. 0.87 is rounded to 2 decimal places."))
    assert Dm("0.85") * 3 == Dm("2.55")
    its.append(rq("Find 0.85 × 3. Round your answer to 1 decimal place.", "2.55", 1, ["2.5", "2.55", "3"],
                  shown="2.55", note="0.85 × 3 = 2.55 exactly. 2.5 cuts off the 5 instead of rounding. 3 is rounded to the nearest whole number."))
    opts = {"4.26": "4.26", "4.35": "4.35", "4.24": "4.24", "4.36": "4.36"}
    assert [k for k in opts if R(k, 1) == "4.3"] == ["4.26"]
    its.append(mcq("Which number is <b>4.3</b> when it is rounded to 1 decimal place?", "4.26",
                   ["4.35", "4.24", "4.36"],
                   "4.26 → look at the hundredths digit, 6: round up to <b>4.3</b>. 4.35 and 4.36 round to 4.4. "
                   "4.24 rounds to 4.2.", same_ok=True))
    assert R(Dm(10) / 3, 2) == "3.33"
    its.append(mcq("Mrs Ng shares $10 equally among 3 children. How much does each child get, to the nearest cent?",
                   "$3.33", ["$3.34", "$3.10", "$3.30"],
                   "$10 ÷ 3 = $3.333… To the nearest cent means to 2 decimal places. The thousandths digit is 3, "
                   "so the hundredths digit stays: <b>$3.33</b>. $3.10 writes the remainder 1 as a digit. "
                   "$3.30 is rounded to 1 decimal place.", want="3.33"))
    assert R(Dm(50) / 7, 2) == "7.14"
    its.append(mcq("Mr Tan shares $50 equally among 7 people. How much does each person get, to the nearest cent?",
                   "$7.14", ["$7.15", "$7.10", "$71.40"],
                   "$50 ÷ 7 = $7.142… The thousandths digit is 2, so the hundredths digit stays: <b>$7.14</b>. "
                   "$7.10 writes the remainder 1 as a digit. $71.40 puts the decimal point in the wrong place.",
                   want="7.14"))
    return {"title": "Rounding answers to 1 or 2 decimal places", "items": its}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    T = Dm("25.50") / 3
    assert T == Dm("8.50")
    its.append(mcq(fig(bar_units(3, "$25.50", "?", "3 units = $25.50")) +
                   "Three friends share $25.50 equally. How much money does each friend get?",
                   M(T), ["$85", "$76.50", "$0.85"],
                   "3 units = $25.50, so 1 unit = $25.50 ÷ 3 = <b>%s</b>. 2550¢ ÷ 3 = 850¢. "
                   "$76.50 multiplies by 3 instead of dividing." % M(T), want=T))
    T = Dm("1.40") * 4
    assert T == Dm("5.60")
    its.append(mcq(fig(bar_units(4, "?", "$1.40", "1 unit = $1.40")) +
                   "Mei Ling buys 4 curry puffs at the school canteen. Each curry puff costs $1.40. How much does she pay?",
                   M(T), ["$56", "$5.40", "$0.56"],
                   "4 units = $1.40 × 4 = <b>%s</b>. 140¢ × 4 = 560¢. $5.40 adds 4 instead of multiplying." % M(T),
                   want=T))
    T = Dm("1.25") * 6
    assert T == Dm("7.50")
    its.append(mcq("Mrs Ng pays $1.25 for each bus ride with her EZ-Link card. She takes 6 bus rides in a week. "
                   "How much does she pay in all?", M(T), ["$75", "$0.75", "$7.25"],
                   "1.25 × 6: 125 hundredths × 6 = 750 hundredths = <b>%s</b>. "
                   "$7.25 adds 6 instead of multiplying." % M(T), want=T))
    T = Dm("4.8") / 6
    assert T == Dm("0.8")
    its.append(mcq(fig(bar_units(6, "4.8 m", "?", "6 units = 4.8 m")) +
                   "A ribbon 4.8 m long is cut into 6 equal pieces. How long is each piece?",
                   N(T) + " m", ["8 m", "0.08 m", "28.8 m"],
                   "6 units = 4.8 m. 4.8 is 48 tenths. 48 ÷ 6 = 8, so 1 unit = 8 tenths = <b>0.8 m</b>. "
                   "8 m is longer than the whole ribbon.", want=T))
    T = Dm("13.50") / 3
    assert T == Dm("4.50")
    its.append(mcq(fig(bar_units(3, "$13.50", "?", "3 units = $13.50")) +
                   "Mr Tan pays $13.50 for 3 plates of chicken rice at a hawker centre. Each plate costs the same. "
                   "How much does 1 plate cost?", M(T), ["$45", "$40.50", "$4.05"],
                   "1 unit = $13.50 ÷ 3. 13 ÷ 3 = 4 R 1. Rename 1 one as 10 tenths: 10 + 5 = 15 tenths, and 15 tenths ÷ 3 "
                   "= 5 tenths. So 1 plate costs <b>%s</b>. $4.05 puts the 5 in the wrong place." % M(T), want=T))
    T = Dm("2.75") * 8
    assert T == 22
    its.append(mcq("Siti saves $2.75 every week. How much does she save in 8 weeks?",
                   M(T), ["$16.75", "$220", "$2.20"],
                   "2.75 × 8: 275 hundredths × 8 = 2200 hundredths = <b>%s</b>. Check: 2 × 8 = 16 and 0.75 × 8 = 6, "
                   "so 16 + 6 = 22. $16.75 multiplies only the dollars." % M(T), want=T))
    T = Dm("1.5") * 3
    assert T == Dm("4.5")
    its.append(mcq("Raju buys 3 bottles of water for Sports Day. Each bottle holds 1.5 ℓ. "
                   "How much water is there in all?", N(T) + " ℓ", ["45 ℓ", "0.45 ℓ", "3.15 ℓ"],
                   "1.5 × 3 = 15 tenths × 3 = 45 tenths = <b>4.5 ℓ</b>. "
                   "3.15 ℓ writes 1 × 3 = 3 and 0.5 × 3 = 1.5 side by side instead of adding.", want=T))
    T = Dm("2.4") * 5
    assert T == 12
    its.append(mcq("Kumar runs 2.4 km at East Coast Park every day. How far does he run in 5 days?",
                   N(T) + " km", ["1.2 km", "120 km", "10.4 km"],
                   "2.4 × 5 = 24 tenths × 5 = 120 tenths = <b>12 km</b>. "
                   "10.4 km multiplies only the 2 and forgets the 0.4.", want=T))
    T = Dm(7) / 4
    assert T == Dm("1.75")
    its.append(mcq(fig(bar_units(4, "7 m", "?", "4 units = 7 m")) +
                   "Mrs Lim cuts a 7 m rope into 4 equal pieces. How long is each piece?",
                   N(T) + " m", ["1.3 m", "17.5 m", "28 m"],
                   "4 units = 7 m, so 1 unit = 7 ÷ 4. 7 ÷ 4 = 1 R 3. Write 7 as 7.00 and keep dividing: "
                   "7 ÷ 4 = <b>1.75 m</b>. 1.3 m writes the remainder 3 as a decimal digit.", want=T))
    T = Dm(9) / 4
    assert T == Dm("2.25")
    its.append(mcq("Mdm Wong pays $9 for 4 kg of rambutans. What is the cost of 1 kg?",
                   M(T), ["$2.10", "$22.50", "$36"],
                   "$9 ÷ 4 = 2 R 1. Write 9 as 9.00 and keep dividing: 9 ÷ 4 = 2.25, so 1 kg costs <b>%s</b>. "
                   "$2.10 writes the remainder 1 as a digit. $36 multiplies." % M(T), want=T))
    T = Dm("3.80") * 3
    assert T == Dm("11.40")
    its.append(mcq("A cup of bubble tea costs $3.80. Chloe buys 3 cups for her family. How much does she pay?",
                   M(T), ["$9.24", "$114", "$6.80"],
                   "3.80 × 3: 380¢ × 3 = 1140¢ = <b>%s</b>. $9.24 writes 3 × 3 = 9 and 0.80 × 3 = 2.40 side by side "
                   "instead of adding: 9 + 2.40 = 11.40. $6.80 adds 3." % M(T), want=T))
    T = Dm("0.65") * 5
    assert T == Dm("3.25")
    its.append(mcq("Priya walks 0.65 km from her HDB block to school every morning. "
                   "How far does she walk to school in 5 days?", N(T) + " km", ["32.5 km", "0.325 km", "5.65 km"],
                   "0.65 × 5 = 65 hundredths × 5 = 325 hundredths = <b>3.25 km</b>. 5.65 km adds instead of multiplying.",
                   want=T))
    T = Dm("27.60") / 6
    assert T == Dm("4.60")
    its.append(mcq("Mr Rahman pays $27.60 for 6 kg of durians. What is the cost of 1 kg?",
                   M(T), ["$46", "$165.60", "$4.06"],
                   "$27.60 ÷ 6: 2760¢ ÷ 6 = 460¢ = <b>%s</b>. Estimate: $30 ÷ 6 = $5. "
                   "$4.06 puts the 6 in the hundredths place instead of the tenths place." % M(T), want=T))
    T = Dm("2.4") / 8
    assert T == Dm("0.3")
    its.append(mcq("Kavya pours 2.4 ℓ of orange juice equally into 8 cups. How much juice is in each cup?",
                   N(T) + " ℓ", ["3 ℓ", "0.03 ℓ", "19.2 ℓ"],
                   "2.4 ÷ 8 = 24 tenths ÷ 8 = 3 tenths = <b>0.3 ℓ</b>. 3 ℓ is more than the whole 2.4 ℓ.", want=T))
    T = R(Dm(10) / 6, 1)
    assert T == "1.7"
    its.append(mcq("Ryan pours 10 ℓ of water equally into 6 pails. How much water is in each pail? "
                   "Round your answer to 1 decimal place.", T + " ℓ", ["1.6 ℓ", "1.4 ℓ", "0.6 ℓ"],
                   "10 ÷ 6 = 1.66… The hundredths digit is 6, so round up: <b>1.7 ℓ</b>. 1.6 ℓ cuts off the digits. "
                   "1.4 ℓ writes the remainder 4 as a digit. 0.6 ℓ is 6 ÷ 10.", want=T))
    T = R(Dm(20) / 3, 2)
    assert T == "6.67"
    its.append(mcq("Ahmad shares $20 equally among 3 friends. How much does each friend get, to the nearest cent?",
                   "$" + T, ["$6.66", "$6.20", "$6.70"],
                   "$20 ÷ 3 = $6.666… To the nearest cent means 2 decimal places. The thousandths digit is 6, so round up: "
                   "<b>$6.67</b>. $6.66 cuts off the digits. $6.20 writes the remainder 2 as a digit.", want=T))
    big, diff = Dm("4.65") * 3, Dm("4.65") * 2
    assert big - Dm("4.65") == diff == Dm("9.30")
    its.append(mcq(fig(bar_times([("Ethan", 1), ("Sarah", 3)], "$4.65", 1, 3, "?")) +
                   "Ethan’s pencil case costs $4.65. Sarah’s pencil case costs 3 times as much. "
                   "How much more does Sarah’s pencil case cost than Ethan’s?",
                   M(diff), ["$13.95", "$18.60", "$1.55"],
                   "Sarah has 2 more units than Ethan. 2 units = $4.65 × 2 = <b>%s</b>. "
                   "$13.95 is the cost of Sarah’s pencil case, not the difference. $18.60 is the total of both. "
                   "$1.55 divides by 3." % M(diff), want=diff))
    T = Dm("15.20") / 4
    assert T == Dm("3.80")
    its.append(mcq(fig(bar_units(4, "$15.20", "?", "4 units = $15.20")) +
                   "Raju and 3 friends share the cost of a $15.20 birthday cake equally. How much does each of them pay?",
                   M(T), ["$5.07", "$60.80", "$38"],
                   "Raju and 3 friends are 4 people, so 4 units = $15.20. 1 unit = $15.20 ÷ 4 = <b>%s</b>. "
                   "$5.07 divides by 3 and forgets Raju. $60.80 multiplies." % M(T), want=T))
    cost = Dm("1.65") * 3
    T = 10 - cost
    assert cost == Dm("4.95") and T == Dm("5.05")
    its.append(mcq("Nurul buys 3 files at $1.65 each. She pays with a $10 note. How much change does she get?",
                   M(T), ["$4.95", "$8.35", "$6.05"],
                   "Cost: 1.65 × 3 = $4.95. Change: $10.00 − $4.95 = <b>%s</b>. $4.95 is the cost, not the change. "
                   "$8.35 forgets to multiply by 3. $6.05 forgets to rename a dollar when subtracting." % M(T), want=T))
    cost = Dm("2.85") * 3
    T = Dm("18.50") - cost
    assert cost == Dm("8.55") and T == Dm("9.95")
    its.append(mcq(fig(bar_parts([(cost, "3 × $2.85"), (T, "?")], "$18.50")) +
                   "Zhi Hao has $18.50. He buys 3 notebooks at $2.85 each. How much money does he have left?",
                   M(T), ["$8.55", "$15.65", "$10.95"],
                   "Cost: 2.85 × 3 = 285¢ × 3 = 855¢ = $8.55. Left: $18.50 − $8.55 = <b>%s</b>. "
                   "$8.55 is the cost, not the money left. $15.65 forgets to multiply by 3. "
                   "$10.95 forgets to rename when subtracting." % M(T), want=T))
    return {"title": "Word problems with money and measures", "items": its}


# ============================================================ lesson
def body_html():
    f1 = split_svg("2.3", 4)
    f2 = ld_svg("8.4", 3, "full")
    f3 = ld_svg("7.00", 4, "full")
    f4 = rline_svg("3.3", "0.01", Dm(10) / 3, "3.333…")
    f5 = bar_units(3, "$25.50", "?", "3 units = $25.50")
    return (
        "<h2>Work in tenths and hundredths</h2>"
        "<p>Think of a decimal as a number of tenths or hundredths. 2.35 is 235 hundredths. "
        "Multiply or divide the whole number, then write the answer in the same unit. "
        "Estimate to check that the decimal point is in the right place.</p>"
        "<h2>Decimal × a 1-digit number</h2>"
        "<p>Split the decimal into its whole-number part and its decimal part. Multiply each part, then add.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>2.3 × 4 = 8 + 1.2 = 9.2. Add the parts: do not write 8.12.</figcaption></figure>"
        + ex("Example 1", "2.35 × 4", "2.35 is 235 hundredths. 235 × 4 = 940, so 2.35 × 4 = 940 hundredths = 9.40. "
             "Estimate: 2 × 4 = 8, so 9.4 makes sense.", "9.4")
        + "<h2>Decimal ÷ a 1-digit number</h2>"
        "<p>Divide from the left, as with whole numbers. Put the decimal point in the answer straight above the "
        "decimal point in the number you divide. Rename what is left over: 2 ones = 20 tenths.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>8.4 ÷ 3: 8 ones ÷ 3 = 2 R 2. 2 ones + 4 tenths = 24 tenths, and 24 tenths ÷ 3 = 8 tenths. "
        "8.4 ÷ 3 = 2.8.</figcaption></figure>"
        + ex("Example 2", "4.08 ÷ 4", "4 ones ÷ 4 = 1 one. 0 tenths ÷ 4 = 0 tenths. 8 hundredths ÷ 4 = 2 hundredths.",
             "1.02 (keep the 0 in the tenths place)")
        + "<h2>Whole number ÷ whole number as a decimal</h2>"
        "<p>Do not stop at the remainder. Write the whole number with zeros after a decimal point and keep dividing.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>7 ÷ 4 = 1 R 3. Write 7 as 7.00. 3 ones = 30 tenths, 30 ÷ 4 = 7 R 2. 2 tenths = 20 hundredths, "
        "20 ÷ 4 = 5. 7 ÷ 4 = 1.75, not 1.3.</figcaption></figure>"
        + "<h2>Rounding the answer</h2>"
        "<p>Some divisions never end: 10 ÷ 3 = 3.333… To round to 1 decimal place, look at the hundredths digit. "
        "To round to 2 decimal places, look at the thousandths digit. 5 or more: round up. Less than 5: keep it.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>3.333… is before the half-way mark 3.35, so 10 ÷ 3 ≈ 3.3 (1 decimal place). "
        "To 2 decimal places, 10 ÷ 3 ≈ 3.33.</figcaption></figure>"
        + "<h2>Word problems: draw a model</h2>"
        "<figure class='sn-fig'>" + f5 +
        "<figcaption>Three friends share $25.50 equally. 3 units = $25.50, so 1 unit = $25.50 ÷ 3 = $8.50.</figcaption>"
        "</figure>"
        + ex("Example 3", "Mrs Ng shares $10 equally among 3 children. How much does each child get, to the nearest cent?",
             "$10 ÷ 3 = $3.333… The nearest cent is 2 decimal places. The thousandths digit is 3, so keep it.", "$3.33")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["2.3 × 4 = 8.12 (writing 8 and 12 side by side)", "Add the parts: 8 + 1.2 = 9.2"],
            ["2.35 × 4 = 8.35 (multiplying only the whole number)", "Multiply every digit: 9.4"],
            ["7.2 ÷ 6 = 12 (leaving out the point)", "72 tenths ÷ 6 = 12 tenths = 1.2"],
            ["4.08 ÷ 4 = 1.2 (dropping a zero)", "Keep the 0 that holds the tenths place: 1.02"],
            ["7 ÷ 4 = 1 R 3 = 1.3 (remainder as decimal digits)", "Write 7 as 7.00 and keep dividing: 1.75"],
            ["2 ÷ 3 ≈ 0.66 (cutting off digits)", "Look at the next digit: 0.666… ≈ 0.67"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 multiplying and dividing decimals?",
     "a": "In Primary 4, students multiply and divide decimals with up to 2 decimal places by a 1-digit whole number, such as 2.35 × 4 and 8.4 ÷ 3. They also divide whole numbers to get a decimal answer (7 ÷ 4 = 1.75) and round answers to 1 or 2 decimal places."},
    {"q": "How do I explain 7 ÷ 4 = 1.75 to my child?",
     "a": "Tell your child not to stop at the remainder: write 7 as 7.00 and keep dividing. 3 ones left over make 30 tenths, 30 tenths ÷ 4 = 7 tenths with 2 tenths left, and 20 hundredths ÷ 4 = 5 hundredths, so 7 ÷ 4 = 1.75."},
    {"q": "What is the most common mistake?",
     "a": "The most common mistake is putting the decimal point in the wrong place, for example 2.3 × 4 = 8.12 instead of 9.2, or writing the remainder as decimal digits (7 ÷ 4 = 1.3). Estimating first (2 × 4 = 8, so the answer is about 9) catches most of these."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Multiplying and dividing decimals by a 1-digit whole number, dividing whole numbers with a decimal quotient and rounding answers are part of the Primary 4 Decimals topic in the MOE 2021 Primary Mathematics Syllabus (Standard)."},
]


def mark_large(u, pattern):
    """Tag number lines, split models and bar models so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every 'a × b = ?' / 'a ÷ b = ?' and 'What is a op b?' question with Decimal."""
    rxs = [re.compile(r"^([\d.]+) ([×÷]) ([\d.]+) = \?$"), re.compile(r"What is ([\d.]+) ([×÷]) ([\d.]+)\?$")]
    n = 0
    for s in sets:
        for it in s["items"]:
            for rx in rxs:
                m = rx.search(it["q"])
                if m:
                    a, op, b = Dm(m.group(1)), m.group(2), Dm(m.group(3))
                    r = a * b if op == "×" else a / b
                    assert val(it["c"][it["a"]])[0] == r, it["q"]
                    n += 1
                    break
            for c in it["c"]:
                v = val(c)
                if v and v[1] == "$":
                    assert v[0] == v[0].quantize(Dm("0.01")), (it["q"], c)
    return n


def gen():
    rnd = random.Random(64811)
    sets = [set_mul(), set_div(), set_whole(), set_round(), set_problems()]
    assert check_answers(sets) >= 40
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "multiplying-and-dividing-decimals",
        "sort": 11, "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Multiplying and Dividing Decimals",
        "seo_title": "P4 Multiplying and Dividing Decimals Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplying and Dividing Decimals",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Decimals",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplying and dividing decimals (up to 2 decimal places) by a 1-digit whole number; "
                         "dividing whole numbers with quotient as a decimal; rounding answers",
        "meta_desc": "Free P4 maths practice: decimals × and ÷ a 1-digit number, 7 ÷ 4 = 1.75, rounding to 1 or 2 "
                     "decimal places, money word problems. 100 questions with answers.",
        "key_big": "Work in tenths or hundredths, then check the decimal point with an estimate.",
        "key_sub": "2.35 × 4 = 235 hundredths × 4 = 940 hundredths = 9.4; 7 ÷ 4 = 7.00 ÷ 4 = 1.75, not 1.3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "number line|rounding number line|split model|bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
