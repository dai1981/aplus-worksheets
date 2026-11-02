# -*- coding: utf-8 -*-
"""
BC Grade 6 Math: Multiplying and dividing decimals (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g6_decimals.py
× and ÷ by 10, 100 and 1000 on a place value chart, decimals × whole numbers (2.35 × 6 = 235 hundredths × 6
= 1410 hundredths = 14.1), decimals ÷ whole numbers (4.08 ÷ 4 = 408 hundredths ÷ 4 = 1.02), estimating to place
the decimal point, then money and measurement word problems in BC contexts.
Every answer is computed with decimal.Decimal (never float). Wrong answers are real student mistakes:
the decimal point in the wrong place or left out, “just add a zero”, multiplying or dividing only the
whole-number part, writing 8 and 12 side by side (2.3 × 4 = 8.12), dropping a place-holding zero (1.02 -> 1.2),
rounding the wrong way when estimating, multiplying instead of dividing, and adding instead of multiplying.
BC style: Canadian English, $ and ¢, metric units. 4-digit numbers have no separator (3050);
5 or more digits use a no-break space (14 500). HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written only to hold an empty place
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, BC style: 4536, 12 350 (no-break space), 0.045."""
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
    """Money: $14, $22.50."""
    d = Dm(x)
    if d == d.to_integral_value():
        return "$" + N(d)
    q = format(d.quantize(Dm("0.01")), "f")
    assert Dm(q) == d, x
    w, _, f = q.partition(".")
    return "$" + N(w) + "." + f


def P10(k):
    return N(10 ** k)


def calc(x, op, k):
    x = Dm(str(x))
    return x * 10 ** k if op == "×" else x / 10 ** k


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
    if rest and not re.match(r"^[a-zA-Z]+$", rest):
        return None
    return (Dm(m.group(2).replace(NB, "")), "$" if m.group(1) else rest)


def mcq(q, correct, wrong, e, same_ok=False):
    """4 choices: correct first + 3 wrong. No two choices may have the same value (and unit)."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
    if not same_ok:
        vs = [val(x) for x in ch]
        assert all(v is not None for v in vs), (q, ch)
        assert len(set(vs)) == 4, (q, ch)
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


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ figure: place value chart with arrows
def split_digits(s):
    """'32.7' -> {1: '3', 0: '2', -1: '7'}."""
    w, _, f = s.replace(NB, "").partition(".")
    d = {}
    for j, ch in enumerate(w):
        d[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        d[-(j + 1)] = ch
    return d


def pv_move(x, op, k, hi=None, show_answer=True, CW=106):
    """Two-row place value chart: x on top, x op 10^k below, red arrows from each digit to its new place.
    Zeros that only hold an empty place are grey. hi: place of a digit of x; that digit is red in the answer row."""
    r = N(calc(x, op, k))
    top, bot = split_digits(N(x)), split_digits(r)
    shift = k if op == "×" else -k
    moved = {p + shift for p in top}
    hi_place = None if hi is None else hi + shift
    cols = list(range(max(max(top), max(bot)), min(min(top), min(bot), -1) - 1, -1))
    assert all(p in PLACE for p in cols), (x, op, k)
    PW = 16
    HEAD, ROW, BAND, LW = 30, 44, 46, 76
    x0, y0 = 4, 4
    gw = len(cols) * CW + PW
    W = 2 * x0 + LW + gw
    yt = y0 + HEAD
    yb = yt + ROW + BAND
    gy = yb + ROW
    H = gy + y0
    xs, xx = {}, x0 + LW
    for p in cols:
        xs[p] = xx
        xx += CW + (PW if p == 0 else 0)
    cx = {p: xs[p] + CW / 2.0 for p in cols}
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, gw, gy - y0, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, gw, HEAD, HEADFILL)]
    for p in cols:
        if p != cols[0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], gy, GREEN))
        o.append(text(cx[p], y0 + 21, cap(PLACE[p]), 14, col=GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (xs[0] + CW + PW, y0, xs[0] + CW + PW, gy, GREEN))
    for yy in (yt, yt + ROW, yb):
        o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x0 + LW, yy, x0 + LW + gw, yy, GREEN, 2 if yy == yt else 1))
    for p, ch in top.items():
        o.append(text(cx[p], yt + 32, ch, 28, weight=800))
    if show_answer:
        for p, ch in bot.items():
            col = INK if p in moved else GHOST
            if hi_place == p:
                col = RED
            o.append(text(cx[p], yb + 32, ch, 28, col=col, weight=800))
    ptx = xs[0] + CW + PW / 2.0
    if "." in N(x):
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (ptx, yt + 31, INK))
    if show_answer and "." in r:
        o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (ptx, yb + 31, INK))
    y1, y2 = yt + ROW + 5, yb - 5
    for p in top:
        if p + shift not in bot:
            continue
        xa, xb = cx[p], cx[p + shift]
        L = math.hypot(xb - xa, y2 - y1)
        ux, uy = (xb - xa) / L, (y2 - y1) / L
        hx, hy = xb - ux * 11, y2 - uy * 11
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (xa, y1, hx, hy, RED))
        o.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                 % (xb, y2, hx - uy * 5.5, hy + ux * 5.5, hx + uy * 5.5, hy - ux * 5.5, RED))
    o.append(text(x0 + LW - 10, yt + ROW + BAND / 2.0 + 6, "%s %s" % (op, P10(k)), 17, anchor="end", col=GREEN))
    lab = "place value chart: %s %s %s, every digit moves %d place%s to the %s" % (
        N(x), "times" if op == "×" else "divided by", P10(k), k, "" if k == 1 else "s", "left" if op == "×" else "right")
    if show_answer:
        lab += ", giving %s" % r
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: number line with equal jumps
def jumps_svg(step, n, end, show_end_label=False):
    """Number line from 0 to the whole number `end`, tenths ticks, n equal jumps of `step` from 0.
    Whole numbers are labelled; the jumps are labelled +step. The end of the last jump has a red dot."""
    step = Dm(step)
    total = step * n
    assert total <= end and end == int(end)
    U = min(400, 600 // int(end))          # pixels per 1
    L, R = 22, 22
    W = L + U * int(end) + R
    AY = 74
    H = AY + 38
    X = lambda v: L + float(v) * U
    o = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 8, AY, W - R + 8, AY, INK)]
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
    if show_end_label:
        o.append(text(X(total), AY + 30, N(total), 15, col=RED))
    lab = "number line from 0 to %s with %d jumps of %s, ending at %s" % (N(end), n, N(step), N(total))
    return svg_wrap(W, H, "".join(o), lab)


# ------------------------------------------------------------ figure: split (area) model for decimal × whole
def split_svg(x, n):
    """Rectangle n tall and x wide, split into the whole-number part and the decimal part.
    The widths are drawn to scale. Each part shows its product."""
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


# ------------------------------------------------------------ figure: long division (decimal ÷ whole number)
def point_mark(x, y, fs, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, y - fs * 0.06, fs * 0.1, col)


def ld_svg(dividend, d, quot=None, fs=24):
    """Long division with a decimal dividend and a whole-number divisor.
    quot: None (no quotient), 'digits' (quotient digits, point left out) or 'full'.
    The quotient point sits straight above the dividend point."""
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


# ------------------------------------------------------------ explanations
def moves(k):
    return "1 place" if k == 1 else "%d places" % k


def p10_e(x, op, k, note=""):
    r = calc(x, op, k)
    e = ("%s %s %s: every digit moves <b>%s to the %s</b>. The decimal point stays still."
         % (N(x), op, P10(k), moves(k), "left" if op == "×" else "right"))
    if op == "×" and len(N(x).partition(".")[2]) < k:
        e += " Write 0 in the empty places up to the ones."
    elif op == "÷" and r < 1:
        e += " Write 0 in the empty places, starting with the ones."
    e += " %s %s %s = <b>%s</b>." % (N(x), op, P10(k), N(r))
    if note:
        e += " " + note
    return e


def p10(x, op, k, wrong, note=""):
    return mcq("%s %s %s = ?" % (N(x), op, P10(k)), N(calc(x, op, k)), wrong, p10_e(x, op, k, note))


def unit_word(k, n=2):
    return {1: ("tenth", "tenths"), 2: ("hundredth", "hundredths"), 3: ("thousandth", "thousandths")}[k][0 if n == 1 else 1]


def mul_e(x, n, note=""):
    """2.35 × 6: 2.35 is 235 hundredths. 235 × 6 = 1410, so 2.35 × 6 = 1410 hundredths = 14.1."""
    k = places(x)
    whole = int(Dm(x) * 10 ** k)
    p = whole * n
    r = Dm(x) * n
    e = ("%s is %s %s. %s × %d = %s, so %s × %d = %s %s = <b>%s</b>."
         % (x, N(whole), unit_word(k, whole), N(whole), n, N(p), x, n, N(p), unit_word(k, p), N(r)))
    if note:
        e += " " + note
    return e


def mul(x, n, wrong, note="", swap=False):
    r = Dm(x) * n
    q = "%d × %s = ?" % (n, x) if swap else "%s × %d = ?" % (x, n)
    return mcq(q, N(r), wrong, mul_e(x, n, note))


def div_e(x, n, note=""):
    """4.56 ÷ 4: 4.56 is 456 hundredths. 456 ÷ 4 = 114, so 4.56 ÷ 4 = 114 hundredths = 1.14."""
    k = places(x)
    whole = int(Dm(x) * 10 ** k)
    r = Dm(x) / n
    assert r * n == Dm(x) and whole % n == 0
    e = ("%s is %s %s. %s ÷ %d = %s, so %s ÷ %d = %s %s = <b>%s</b>. Check: %s × %d = %s."
         % (x, N(whole), unit_word(k), N(whole), n, N(whole // n), x, n, N(whole // n),
            unit_word(k, whole // n), N(r), N(r), n, x))
    if note:
        e += " " + note
    return e


def div(x, n, wrong, note=""):
    return mcq("%s ÷ %d = ?" % (x, n), N(Dm(x) / n), wrong, div_e(x, n, note))


# ============================================================ set 1: × and ÷ by 10, 100, 1000
def set_p10():
    its = []
    # 0-1 charts, answer hidden
    its.append(mcq(fig(pv_move("4.6", "×", 1, show_answer=False)) + "The chart shows 4.6 × 10. What is the answer?",
                   "46", ["4.60", "0.46", "460"],
                   p10_e("4.6", "×", 1, "4.60 is wrong: a zero at the end of a decimal does not change its value.")))
    its.append(mcq(fig(pv_move("7.3", "÷", 1, show_answer=False)) + "The chart shows 7.3 ÷ 10. What is the answer?",
                   "0.73", ["73", "0.073", "7.03"],
                   p10_e("7.3", "÷", 1, "73 moves the digits the wrong way: dividing by 10 makes the number smaller.")))
    # 2-5
    its.append(p10("0.58", "×", 2, ["0.5800", "5.8", "580"], "0.5800 only adds zeros, so it is still 0.58."))
    its.append(p10("26.4", "÷", 2, ["2640", "2.64", "0.0264"], "2640 moves the digits the wrong way."))
    its.append(p10("3.05", "×", 3, ["305", "30" + NB + "500", "3.05000"],
                   "Keep the 0 that holds the hundreds place: 3050, not 305."))
    its.append(p10("57", "÷", 3, ["0.57", "5.7", "57" + NB + "000"], "0.57 moves the digits only 2 places."))
    # 6-7 which calculation
    assert calc("6.25", "×", 1) == Dm("62.5")
    its.append(mcq(fig(pv_move("6.25", "×", 1)) + "Which calculation does the chart show?",
                   "6.25 × 10", ["6.25 ÷ 10", "6.25 × 100", "6.25 ÷ 100"],
                   "Every digit moved <b>1 place to the left</b>, so the number was multiplied by 10. "
                   "<b>6.25 × 10</b> = 62.5.", same_ok=True))
    assert calc("48.3", "÷", 2) == Dm("0.483")
    its.append(mcq(fig(pv_move("48.3", "÷", 2)) + "Which calculation does the chart show?",
                   "48.3 ÷ 100", ["48.3 × 100", "48.3 ÷ 10", "48.3 ÷ 1000"],
                   "Every digit moved <b>2 places to the right</b>, so the number was divided by 100. "
                   "<b>48.3 ÷ 100</b> = 0.483.", same_ok=True))
    # 8-9 red digit
    assert calc("0.046", "×", 2) == Dm("4.6")
    its.append(mcq(fig(pv_move("0.046", "×", 2, hi=-3)) +
                   "The chart shows 0.046 × 100 = 4.6. What is the value of the red digit in the answer?",
                   "6 tenths", ["6 thousandths", "6 hundredths", "6 ones"],
                   "The 6 was in the thousandths place. Every digit moved 2 places to the left, so the 6 is now in the "
                   "<b>tenths</b> place. Its value is <b>6 tenths</b> = 0.6.", same_ok=True))
    assert calc("8.17", "÷", 1) == Dm("0.817")
    its.append(mcq(fig(pv_move("8.17", "÷", 1, hi=-1)) +
                   "The chart shows 8.17 ÷ 10 = 0.817. What is the value of the red digit in the answer?",
                   "1 hundredth", ["1 tenth", "1 thousandth", "1 one"],
                   "The 1 was in the tenths place. Every digit moved 1 place to the right, so the 1 is now in the "
                   "<b>hundredths</b> place. Its value is <b>1 hundredth</b> = 0.01.", same_ok=True))
    # 10-12
    its.append(p10("0.9", "÷", 2, ["0.09", "90", "0.0009"], "0.09 moves the digit only 1 place."))
    its.append(p10("12.08", "×", 1, ["12.080", "1208", "120.08"],
                   "120.08 only multiplies the whole-number part. Every digit must move, including the 8."))
    its.append(p10("640", "÷", 3, ["6.4", "0.064", "640" + NB + "000"],
                   "The last 0 is not needed after the decimal point: 0.640 = 0.64."))
    # 13
    assert calc("5.2", "×", 3) == 5200
    its.append(mcq("In <b>5.2 × 1000</b>, how do the digits move?", "3 places to the left",
                   ["3 places to the right", "2 places to the left", "1 place to the left"],
                   "1000 has 3 zeros, so every digit moves <b>3 places</b>. Multiplying makes the number bigger, so they "
                   "move to the <b>left</b>: 5.2 × 1000 = 5200.", same_ok=True))
    # 14-17 missing numbers
    assert Dm("0.4") * 1000 == 400
    its.append(mcq("0.4 × ? = 400", "1000", ["100", "10", "399.6"],
                   "The 4 moves from the tenths to the hundreds: that is 3 places to the left, so the missing number is "
                   "<b>1000</b>. 399.6 is 400 − 0.4, which is subtraction, not multiplication."))
    assert Dm(92) / 100 == Dm("0.92")
    its.append(mcq("92 ÷ ? = 0.92", "100", ["10", "1000", "10" + NB + "000"],
                   "The 2 moves from the ones to the hundredths: 2 places to the right. So the missing number is <b>100</b>."))
    assert Dm("3.06") * 100 == 306
    its.append(mcq("? × 100 = 306", "3.06", ["30.6", "0.306", "3.6"],
                   "Use the inverse: 306 ÷ 100 = <b>3.06</b>. Check: 3.06 × 100 = 306. "
                   "3.6 drops the 0 that holds the tenths place."))
    assert Dm(45) / 100 == Dm("0.45")
    its.append(mcq("? ÷ 100 = 0.45", "45", ["0.0045", "4.5", "4500"],
                   "Use the inverse: 0.45 × 100 = <b>45</b>. Check: 45 ÷ 100 = 0.45. 0.0045 divides instead of multiplying."))
    # 18 equivalent calculation
    assert Dm("0.6") * 1000 == 6 * 100 == 600
    assert 600 not in {6 * 1000, Dm("0.6") * 100, 60 * 100}
    its.append(mcq("Which calculation has the same answer as <b>0.6 × 1000</b>?", "6 × 100",
                   ["6 × 1000", "0.6 × 100", "60 × 100"],
                   "0.6 × 1000 = 600. 0.6 × 10 = 6, and 6 × 100 = 600. So <b>6 × 100</b> gives the same answer.",
                   same_ok=True))
    # 19
    assert Dm("0.073") * 100 == Dm("7.3")
    its.append(mcq("Which number is <b>100 times</b> as large as 0.073?", "7.3", ["73", "0.73", "0.07300"],
                   "100 times as large means × 100: every digit moves 2 places to the left. 0.073 × 100 = <b>7.3</b>. "
                   "0.07300 only adds zeros, so it is still 0.073."))
    order = [0, 1, 2, 3, 6, 7, 10, 13, 4, 5, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19]
    return {"title": "× and ÷ by 10, 100 and 1000", "items": reorder(its, order)}


# ============================================================ set 2: decimal × whole number
def set_mul():
    its = []
    # 0-1 number lines
    assert 3 * Dm("0.6") == Dm("1.8")
    its.append(mcq(fig(jumps_svg("0.6", 3, 2)) + "The number line shows 3 jumps of 0.6. What is 0.6 × 3?",
                   "1.8", ["18", "0.18", "3.6"],
                   mul_e("0.6", 3, "The red dot is 8 small ticks past 1, at 1.8. 3.6 adds 3 + 0.6 instead of multiplying.")))
    assert 4 * Dm("0.7") == Dm("2.8")
    its.append(mcq(fig(jumps_svg("0.7", 4, 3)) + "The number line shows 4 jumps of 0.7. What is 0.7 × 4?",
                   "2.8", ["28", "0.28", "4.7"],
                   mul_e("0.7", 4, "The red dot is 8 small ticks past 2, at 2.8.")))
    # 2-3 split models
    assert Dm("2.3") * 4 == Dm("9.2")
    its.append(mcq(fig(split_svg("2.3", 4)) + "The model splits 2.3 × 4 into 2 × 4 and 0.3 × 4. What is 2.3 × 4?",
                   "9.2", ["8.12", "92", "8.3"],
                   "2 × 4 = 8 and 0.3 × 4 = 1.2. Add the parts: 8 + 1.2 = <b>9.2</b>. "
                   "8.12 writes 8 and 12 side by side instead of adding. 8.3 forgets to multiply the 0.3."))
    assert Dm("5.6") * 3 == Dm("16.8")
    its.append(mcq(fig(split_svg("5.6", 3)) + "The model splits 5.6 × 3 into 5 × 3 and 0.6 × 3. What is 5.6 × 3?",
                   "16.8", ["15.18", "168", "15.6"],
                   "5 × 3 = 15 and 0.6 × 3 = 1.8. Add the parts: 15 + 1.8 = <b>16.8</b>. "
                   "15.18 writes 15 and 18 side by side instead of adding. 15.6 forgets to multiply the 0.6."))
    # 4-14 calculations
    its.append(mul("0.8", 7, ["56", "0.56", "7.8"], "0.56 puts the decimal point one place too far left."))
    its.append(mul("1.2", 4, ["48", "0.48", "5.2"], "5.2 adds 1.2 + 4 instead of multiplying."))
    its.append(mul("0.05", 6, ["30", "3", "0.03"], "30 hundredths is the same as 3 tenths. 0.03 is only 3 hundredths."))
    its.append(mul("2.35", 6, ["1.41", "141", "12.35"],
                   "1410 hundredths = 14.10 = 14.1. Estimate: 2 × 6 = 12, so the answer is a bit more than 12. "
                   "12.35 multiplies only the 2."))
    its.append(mul("0.125", 8, ["0.1", "10", "8.125"],
                   "1000 thousandths make 1 whole. 0.1 puts the point in the wrong place."))
    its.append(mul("3.6", 5, ["180", "1.8", "15.30"],
                   "Or split it: 3 × 5 = 15 and 0.6 × 5 = 3, so 15 + 3 = 18. 15.30 writes 15 and 30 side by side.",
                   swap=True))
    its.append(mul("4.75", 4, ["1.9", "190", "16.75"],
                   "Estimate: 5 × 4 = 20, so 19 makes sense. 16.75 multiplies only the 4 ones."))
    its.append(mul("0.36", 9, ["32.4", "0.324", "9.36"], "9.36 adds instead of multiplying. 0.36 × 9 must be less than 9."))
    its.append(mul("12.4", 3, ["372", "3.72", "36.12"],
                   "Or split it: 12 × 3 = 36 and 0.4 × 3 = 1.2, so 36 + 1.2 = 37.2. 36.12 writes 36 and 12 side by side."))
    its.append(mul("6.08", 5, ["34", "3.04", "304"],
                   "34 forgets the 0 in the tenths place: it works out 6.8 × 5 instead of 6.08 × 5."))
    its.append(mul("1.205", 4, ["48.2", "0.482", "4.205"],
                   "4820 thousandths = 4.820 = 4.82. Estimate: 1 × 4 = 4. 4.205 multiplies only the 1."))
    # 15 multiplying by a decimal less than 1
    assert Dm("0.9") * 24 < 24
    its.append(mcq("Without working it out, which is true about <b>0.9 × 24</b>?", "It is less than 24",
                   ["It is greater than 24", "It is equal to 24", "It is greater than 240"],
                   "0.9 is less than 1, so 0.9 × 24 is less than 1 × 24 = 24. In fact 0.9 × 24 = 21.6. "
                   "Multiplying by a decimal less than 1 makes the number smaller.", same_ok=True))
    # 16-17 use a fact
    assert 47 * 6 == 282 and Dm("4.7") * 6 == Dm("28.2")
    its.append(mcq("Use 47 × 6 = 282 to find <b>4.7 × 6</b>.", "28.2", ["282", "2.82", "0.282"],
                   "4.7 is 47 ÷ 10, so the answer is 282 ÷ 10 = <b>28.2</b>. Estimate: 5 × 6 = 30. 2.82 divides by 100."))
    assert 135 * 7 == 945 and Dm("1.35") * 7 == Dm("9.45")
    its.append(mcq("Use 135 × 7 = 945 to find <b>1.35 × 7</b>.", "9.45", ["94.5", "0.945", "945"],
                   "1.35 is 135 ÷ 100, so the answer is 945 ÷ 100 = <b>9.45</b>. Estimate: 1 × 7 = 7 and 2 × 7 = 14, "
                   "so the answer is between 7 and 14."))
    # 18 missing number
    assert Dm("0.7") * 4 == Dm("2.8")
    its.append(mcq("? × 4 = 2.8", "0.7", ["7", "0.07", "11.2"],
                   "Use the inverse: 2.8 ÷ 4. 2.8 is 28 tenths, and 28 ÷ 4 = 7, so the answer is 7 tenths = <b>0.7</b>. "
                   "Check: 0.7 × 4 = 2.8. 11.2 is 2.8 × 4."))
    # 19 error
    assert Dm("0.25") * 4 == 1
    its.append(mcq("Simran says 0.25 × 4 = 0.1. What is the correct answer?", "1", ["0.1", "100", "4.25"],
                   "0.25 is 25 hundredths. 25 × 4 = 100, so 0.25 × 4 = 100 hundredths = <b>1</b>. "
                   "Think of money: 4 quarters make $1. Simran put the point in the wrong place."))
    order = [0, 1, 4, 5, 2, 3, 6, 9, 12, 16, 7, 17, 10, 11, 13, 15, 8, 14, 18, 19]
    return {"title": "Decimals × whole numbers", "items": reorder(its, order)}


# ============================================================ set 3: decimal ÷ whole number
def set_div():
    its = []
    its.append(div("0.9", 3, ["3", "0.03", "2.7"], "2.7 multiplies instead of dividing."))
    its.append(div("4.8", 4, ["12", "0.12", "1.8"], "1.8 divides only the 4 ones and forgets the 8 tenths."))
    its.append(div("6.6", 2, ["33", "0.33", "13.2"], "13.2 multiplies instead of dividing."))
    assert Dm(7) / Dm("3.5") == 2
    its.append(div("3.5", 7, ["5", "0.05", "2"], "2 is 7 ÷ 3.5: it divides the wrong way round. 3.5 is less than 7, so the answer is less than 1."))
    its.append(div("8.55", 5, ["17.1", "0.171", "42.75"],
                   "Estimate: 10 ÷ 5 = 2, so the answer is a bit less than 2. 42.75 multiplies by 5."))
    its.append(div("9.24", 4, ["23.1", "0.231", "36.96"],
                   "Estimate: 8 ÷ 4 = 2, so the answer is a bit more than 2. 36.96 multiplies by 4."))
    its.append(div("6.18", 6, ["1.3", "103", "10.3"],
                   "1.3 drops the 0 that holds the tenths place: 1 tenth ÷ 6 is 0 tenths, so write 0."))
    its.append(div("2.4", 8, ["3", "0.03", "19.2"], "2.4 is less than 8, so the answer is less than 1. 19.2 multiplies."))
    its.append(div("12.48", 6, ["2.8", "20.8", "208"],
                   "2.8 drops the 0 that holds the tenths place: 4 tenths ÷ 6 is 0 tenths, so write 0."))
    its.append(div("0.72", 9, ["0.8", "8", "6.48"], "0.8 is 8 tenths, but the answer is 8 hundredths."))
    its.append(div("13.5", 9, ["15", "0.15", "121.5"], "Estimate: 9 ÷ 9 = 1 and 18 ÷ 9 = 2, so the answer is between 1 and 2."))
    its.append(div("5.004", 4, ["12.51", "0.1251", "1251"], "Estimate: 4 ÷ 4 = 1, so the answer is a bit more than 1."))
    its.append(div("3.208", 8, ["0.41", "4.01", "0.0401"],
                   "0.41 drops the 0 that holds the hundredths place: 0 hundredths ÷ 8 is 0 hundredths, so write 0."))
    its.append(div("16.2", 6, ["27", "0.27", "97.2"], "Estimate: 18 ÷ 6 = 3, so the answer is a bit less than 3."))
    # 14-16 long division: place the point
    assert Dm("8.52") / 4 == Dm("2.13")
    its.append(mcq(fig(ld_svg("8.52", 4, "digits")) +
                   "The quotient digits for 8.52 ÷ 4 are 2, 1, 3. Where does the decimal point go?",
                   "2.13", ["21.3", "213", "0.213"],
                   "Put the decimal point in the quotient straight above the point in 8.52. "
                   "Estimate: 8 ÷ 4 = 2, so the answer is about 2. 8.52 ÷ 4 = <b>2.13</b>."))
    assert Dm("6.95") / 5 == Dm("1.39")
    its.append(mcq(fig(ld_svg("6.95", 5, "digits")) +
                   "The quotient digits for 6.95 ÷ 5 are 1, 3, 9. What is 6.95 ÷ 5?",
                   "1.39", ["13.9", "139", "0.139"],
                   "The point in the quotient goes straight above the point in 6.95. Estimate: 5 ÷ 5 = 1 and 10 ÷ 5 = 2, "
                   "so the answer is between 1 and 2. 6.95 ÷ 5 = <b>1.39</b>. Check: 1.39 × 5 = 6.95."))
    assert Dm("0.728") / 8 == Dm("0.091")
    its.append(mcq(fig(ld_svg("0.728", 8, "digits")) +
                   "The quotient digits for 0.728 ÷ 8 are 0, 0, 9, 1. What is 0.728 ÷ 8?",
                   "0.091", ["0.91", "9.1", "0.0091"],
                   "The point goes straight above the point in 0.728. 7 tenths ÷ 8 = 0 tenths (keep the 0), "
                   "72 hundredths ÷ 8 = 9 hundredths, 8 thousandths ÷ 8 = 1 thousandth. 0.728 ÷ 8 = <b>0.091</b>. "
                   "0.91 drops the 0."))
    # 17 place value thinking
    assert Dm("7.35") / 5 == Dm("1.47")
    its.append(mcq("7.35 is 735 hundredths. What is 735 hundredths ÷ 5?", "147 hundredths",
                   ["147 tenths", "147 ones", "147 thousandths"],
                   "735 ÷ 5 = 147, and the unit stays the same: <b>147 hundredths</b> = 1.47. "
                   "So 7.35 ÷ 5 = 1.47.", same_ok=True))
    # 18 error
    assert Dm("7.2") / 6 == Dm("1.2")
    its.append(mcq("Mateo says 7.2 ÷ 6 = 12. What is the correct answer?", "1.2", ["12", "0.12", "43.2"],
                   "7.2 is 72 tenths. 72 ÷ 6 = 12, so 7.2 ÷ 6 = 12 tenths = <b>1.2</b>. "
                   "Estimate: 6 ÷ 6 = 1, so the answer is about 1, not about 12. Mateo left out the decimal point."))
    # 19 which is less than 1
    vals = {"5.6 ÷ 8": Dm("5.6") / 8, "9.6 ÷ 8": Dm("9.6") / 8, "8.8 ÷ 8": Dm("8.8") / 8, "16.8 ÷ 8": Dm("16.8") / 8}
    assert [k for k, v in vals.items() if v < 1] == ["5.6 ÷ 8"]
    its.append(mcq("Which quotient is <b>less than 1</b>?", "5.6 ÷ 8", ["9.6 ÷ 8", "8.8 ÷ 8", "16.8 ÷ 8"],
                   "A quotient is less than 1 when the number you divide is less than the divisor. "
                   "Only 5.6 is less than 8, so only <b>5.6 ÷ 8</b> is less than 1 (it is 0.7).", same_ok=True))
    order = [0, 1, 2, 3, 7, 9, 10, 13, 4, 5, 14, 15, 17, 6, 8, 18, 11, 12, 16, 19]
    return {"title": "Decimals ÷ whole numbers", "items": reorder(its, order)}


# ============================================================ set 4: estimate to place the decimal point
def digits_q(a, op, b, wrong, est):
    """The digits of a op b are given without a point. Use an estimate to place it."""
    r = Dm(a) * b if op == "×" else Dm(a) / b
    w = int(Dm(a) * 10 ** places(a))
    assert w % b == 0 or op == "×"
    dig = str(w * b if op == "×" else w // b)
    return mcq("The digits of %s %s %d are <b>%s</b>. Use an estimate to place the decimal point. What is %s %s %d?"
               % (a, op, b, dig, a, op, b), N(r), wrong,
               "Estimate: %s. So %s %s %d = <b>%s</b>." % (est, a, op, b, N(r)))


def set_estimate():
    its = []
    # 0
    assert Dm("6.9") * 4 == Dm("27.6")
    its.append(mcq("Which is the best estimate for <b>6.9 × 4</b>?", "28", ["2.8", "280", "24"],
                   "6.9 is close to 7, and 7 × 4 = <b>28</b>. (Exactly: 27.6.) 24 rounds 6.9 down to 6, "
                   "but 6.9 is much closer to 7."))
    # 1
    assert Dm("19.8") / 5 == Dm("3.96")
    its.append(mcq("Which is the best estimate for <b>19.8 ÷ 5</b>?", "4", ["40", "0.4", "99"],
                   "19.8 is close to 20, and 20 ÷ 5 = <b>4</b>. (Exactly: 3.96.) 99 is 19.8 × 5: it multiplies instead of dividing."))
    # 2-3
    assert Dm("3.8") * 7 == Dm("26.6")
    its.append(digits_q("3.8", "×", 7, ["2.66", "266", "0.266"], "4 × 7 = 28, so the answer is close to 28"))
    assert Dm("41.6") / 8 == Dm("5.2")
    its.append(digits_q("41.6", "÷", 8, ["52", "0.52", "520"], "40 ÷ 8 = 5, so the answer is close to 5"))
    # 4
    assert Dm("3.1") * 9 == Dm("27.9")
    its.append(mcq("Which is the best estimate for <b>3.1 × 9</b>?", "27", ["2.7", "270", "36"],
                   "3.1 is close to 3, and 3 × 9 = <b>27</b>. (Exactly: 27.9.) 36 rounds 3.1 up to 4."))
    # 5
    assert Dm("48.6") / 6 == Dm("8.1")
    its.append(mcq("Use an estimate to choose the correct answer to <b>48.6 ÷ 6</b>.", "8.1", ["81", "0.81", "810"],
                   "48.6 is close to 48, and 48 ÷ 6 = 8. Only <b>8.1</b> is close to 8. Check: 8.1 × 6 = 48.6."))
    # 6
    assert Dm("5.25") * 4 == 21
    its.append(digits_q("5.25", "×", 4, ["2.1", "210", "0.21"],
                        "5 × 4 = 20, so the answer is close to 20. The digits 2100 mean 21.00, which is 21"))
    # 7 between
    assert 42 < Dm("7.3") * 6 < 48
    its.append(mcq("<b>7.3 × 6</b> is between which two numbers?", "42 and 48",
                   ["7 and 8", "4.2 and 4.8", "420 and 480"],
                   "7.3 is between 7 and 8. 7 × 6 = 42 and 8 × 6 = 48, so 7.3 × 6 is between <b>42 and 48</b>. "
                   "(Exactly: 43.8.)", same_ok=True))
    # 8
    assert Dm("0.48") * 30 == Dm("14.4")
    its.append(mcq("Which is the best estimate for <b>0.48 × 30</b>?", "15", ["1.5", "150", "12"],
                   "0.48 is close to 0.5, which is one half. Half of 30 is <b>15</b>. (Exactly: 14.4.) "
                   "12 uses 0.4, but 0.48 is much closer to 0.5."))
    # 9
    assert Dm("9.45") / 7 == Dm("1.35")
    its.append(digits_q("9.45", "÷", 7, ["13.5", "0.135", "135"],
                        "7 ÷ 7 = 1 and 14 ÷ 7 = 2, so the answer is between 1 and 2"))
    # 10-11 errors
    assert Dm("4.2") * 9 == Dm("37.8")
    its.append(mcq("Mei says 4.2 × 9 = 3.78. Use an estimate to check. What is the correct answer?", "37.8",
                   ["3.78", "378", "36.18"],
                   "Estimate: 4 × 9 = 36, so the answer is close to 36, not close to 4. 42 tenths × 9 = 378 tenths = <b>37.8</b>. "
                   "36.18 writes 36 and 18 side by side instead of adding 36 + 1.8."))
    assert Dm("52.8") / 4 == Dm("13.2")
    its.append(mcq("Harjot says 52.8 ÷ 4 = 1.32. Use an estimate to check. What is the correct answer?", "13.2",
                   ["1.32", "132", "211.2"],
                   "Estimate: 52 ÷ 4 = 13, so the answer is close to 13. 528 tenths ÷ 4 = 132 tenths = <b>13.2</b>. "
                   "211.2 is 52.8 × 4."))
    # 12 which product
    vals = {"4.6 × 5": Dm("4.6") * 5, "0.46 × 5": Dm("0.46") * 5, "46 × 5": Dm(46) * 5, "4.6 × 9": Dm("4.6") * 9}
    assert [k for k, v in vals.items() if 20 < v < 30] == ["4.6 × 5"]
    its.append(mcq("Which product is <b>between 20 and 30</b>?", "4.6 × 5", ["0.46 × 5", "46 × 5", "4.6 × 9"],
                   "4.6 is about 5, and 5 × 5 = 25, so <b>4.6 × 5</b> is between 20 and 30 (it is 23). "
                   "0.46 × 5 = 2.3, 46 × 5 = 230 and 4.6 × 9 = 41.4.", same_ok=True))
    # 13 money
    assert Dm("3.95") * 6 == Dm("23.70")
    its.append(mcq("Which is the best estimate for <b>$3.95 × 6</b>?", "$24", ["$2.40", "$240", "$18"],
                   "$3.95 is close to $4, and $4 × 6 = <b>$24</b>. (Exactly: $23.70.) $18 rounds $3.95 down to $3."))
    # 14-15
    assert Dm("0.64") * 7 == Dm("4.48")
    its.append(digits_q("0.64", "×", 7, ["44.8", "0.448", "448"],
                        "0.64 is a bit more than 0.6, and 0.6 × 7 = 4.2, so the answer is a bit more than 4"))
    assert Dm("0.84") / 6 == Dm("0.14")
    its.append(digits_q("0.84", "÷", 6, ["1.4", "0.014", "14"],
                        "0.84 is less than 6, so the answer is less than 1. 0.6 ÷ 6 = 0.1 and 1.2 ÷ 6 = 0.2, "
                        "so the answer is between 0.1 and 0.2"))
    # 16 between
    assert 4 < Dm("38.4") / 8 < 5
    its.append(mcq("<b>38.4 ÷ 8</b> is between which two numbers?", "4 and 5",
                   ["5 and 6", "40 and 50", "0.4 and 0.5"],
                   "32 ÷ 8 = 4 and 40 ÷ 8 = 5. 38.4 is between 32 and 40, so 38.4 ÷ 8 is between <b>4 and 5</b> "
                   "(it is 4.8). For 5 and 6, the number would have to be between 40 and 48, but 38.4 is less than 40.",
                   same_ok=True))
    # 17
    assert Dm("61.2") / 3 == Dm("20.4")
    its.append(mcq("Which is the best estimate for <b>61.2 ÷ 3</b>?", "20", ["2", "200", "180"],
                   "61.2 is close to 60, and 60 ÷ 3 = <b>20</b>. (Exactly: 20.4.) 180 is about 61.2 × 3: "
                   "it multiplies instead of dividing."))
    # 18 calculator
    assert Dm("3.68") * 4 == Dm("14.72")
    its.append(mcq("Ji-woo types 3.68 × 4 on a calculator but misses the decimal point key. The screen shows 1472. "
                   "What is 3.68 × 4?", "14.72", ["147.2", "1.472", "1472"],
                   "Estimate: 4 × 4 = 16, so the answer is close to 16. Only <b>14.72</b> is close to 16. "
                   "(The calculator worked out 368 × 4.)"))
    # 19 better estimate
    assert Dm("8.9") * 6 == Dm("53.4")
    its.append(mcq("Leah estimates 8.9 × 6 as 8 × 6 = 48. Which estimate is closer to the exact answer?",
                   "9 × 6 = 54", ["8 × 6 = 48", "10 × 6 = 60", "89 × 6 = 534"],
                   "8.9 is much closer to 9 than to 8, so <b>9 × 6 = 54</b> is the better estimate. "
                   "The exact answer is 53.4.", same_ok=True))
    order = [0, 1, 4, 8, 13, 17, 2, 3, 5, 6, 9, 14, 15, 7, 16, 12, 10, 11, 18, 19]
    return {"title": "Estimate to place the decimal point", "items": reorder(its, order)}


# ============================================================ set 5: money and measurement problems
def set_problems():
    its = []
    # 0
    T = Dm("2.85") * 4
    assert T == Dm("11.40")
    its.append(mcq("On a BC Ferries trip to Vancouver Island, Liam buys 4 muffins for $2.85 each. How much does he pay?",
                   M(T), ["$114", "$1.14", "$8.85"],
                   "2.85 × 4: 285 × 4 = 1140, so 1140 hundredths = 11.40. He pays <b>%s</b>. "
                   "Estimate: $3 × 4 = $12. $8.85 multiplies only the dollars." % M(T)))
    # 1
    T = Dm("1.5") / 6
    assert T == Dm("0.25")
    its.append(mcq("Six hikers share a 1.5 L bottle of water equally on a trail near Squamish. How much water does each hiker get?",
                   N(T) + " L", ["2.5 L", "0.025 L", "9 L"],
                   "1.5 L is 150 hundredths. 150 ÷ 6 = 25, so each hiker gets 25 hundredths = <b>0.25 L</b> (250 mL). "
                   "9 L multiplies: each hiker cannot get more than the whole bottle."))
    # 2
    T = Dm("2.4") * 3
    assert T == Dm("7.2")
    its.append(mcq("Ava’s family buys 3 bags of Okanagan apples. Each bag has a mass of 2.4 kg. What is the total mass?",
                   N(T) + " kg", ["72 kg", "0.72 kg", "5.4 kg"],
                   "2.4 × 3 = 24 tenths × 3 = 72 tenths = <b>7.2 kg</b>. 5.4 kg adds 2.4 + 3 instead of multiplying."))
    # 3
    T = Dm("12.6") / 3
    assert T == Dm("4.2")
    its.append(mcq("A 12.6 km bike path in Kelowna is split into 3 equal sections. How long is each section?",
                   N(T) + " km", ["42 km", "0.42 km", "37.8 km"],
                   "12.6 is 126 tenths. 126 ÷ 3 = 42, so each section is 42 tenths = <b>4.2 km</b>. "
                   "42 km is longer than the whole path."))
    # 4
    T = Dm("0.75") * 24
    assert T == 18
    its.append(mcq("Salmon costs $24 per kilogram at a market in Richmond. Noah buys 0.75 kg. How much does he pay?",
                   M(T), ["$180", "$1.80", "$24.75"],
                   "0.75 × 24 = 75 hundredths × 24 = 1800 hundredths = <b>$18</b>. Estimate: 0.75 is three quarters, "
                   "and three quarters of $24 is $18. $24.75 adds instead of multiplying."))
    # 5
    T = Dm("2.5") * 6
    assert T == 15
    its.append(mcq("To train for the Terry Fox Run, Arjun walks 2.5 km every day for 6 days. How far does he walk in all?",
                   N(T) + " km", ["150 km", "1.5 km", "8.5 km"],
                   "2.5 × 6 = 25 tenths × 6 = 150 tenths = <b>15 km</b>. Check: 2 × 6 = 12 and 0.5 × 6 = 3. "
                   "8.5 km adds instead of multiplying."))
    # 6
    T = Dm("3.6") / 4
    assert T == Dm("0.9")
    its.append(mcq("A cedar board 3.6 m long is cut into 4 equal pieces for a garden box. How long is each piece?",
                   N(T) + " m", ["9 m", "0.09 m", "14.4 m"],
                   "3.6 is 36 tenths. 36 ÷ 4 = 9, so each piece is 9 tenths = <b>0.9 m</b> (90 cm). "
                   "9 m is longer than the whole board."))
    # 7
    T = Dm("5.20") / 8
    assert T == Dm("0.65")
    its.append(mcq("A box of 8 granola bars costs $5.20. What is the cost of one granola bar?",
                   M(T), ["$6.50", "$41.60", "$65"],
                   "520¢ ÷ 8 = 65¢, so one bar costs <b>%s</b> (65¢). $6.50 puts the point in the wrong place: "
                   "one bar cannot cost more than the box. $41.60 multiplies by 8." % M(T)))
    # 8
    T = Dm("18.75") * 5
    assert T == Dm("93.75")
    its.append(mcq("A school in Surrey buys 5 soccer balls for $18.75 each. What is the total cost?",
                   M(T), ["$937.50", "$90.75", "$23.75"],
                   "1875 hundredths × 5 = 9375 hundredths = <b>%s</b>. Estimate: $19 × 5 = $95. "
                   "$90.75 multiplies only the dollars, and $23.75 adds 5." % M(T)))
    # 9
    T = Dm("4.25") * 8
    assert T == 34
    its.append(mcq("On a farm in the Okanagan, each of 8 students picks 4.25 kg of cherries. How many kilograms do they pick in all?",
                   N(T) + " kg", ["3.4 kg", "340 kg", "32.25 kg"],
                   "4.25 × 8 = 425 hundredths × 8 = 3400 hundredths = <b>34 kg</b>. Check: 4 × 8 = 32 and 0.25 × 8 = 2. "
                   "32.25 kg multiplies only the 4."))
    # 10
    T = Dm("2.4") / 8
    assert T == Dm("0.3") and T * 1000 == 300
    its.append(mcq("A 2.4 L jug of orange juice is poured equally into 8 cups. How many millilitres are in each cup?",
                   "300 mL", ["30 mL", "3000 mL", "3 mL"],
                   "2.4 ÷ 8 = 24 tenths ÷ 8 = 3 tenths = 0.3 L. 1 L = 1000 mL, so 0.3 × 1000 = <b>300 mL</b>. "
                   "30 mL multiplies by 100 instead of 1000."))
    # 11
    T = Dm("1.8") * 6
    assert T == Dm("10.8")
    its.append(mcq("At Whistler, Kai rides a chairlift that is 1.8 km long. He rides it 6 times. How far does he ride on the chairlift?",
                   N(T) + " km", ["108 km", "1.08 km", "6.48 km"],
                   "1.8 × 6 = 18 tenths × 6 = 108 tenths = <b>10.8 km</b>. Check: 1 × 6 = 6 and 0.8 × 6 = 4.8, "
                   "so 6 + 4.8 = 10.8. 6.48 writes 6 and 48 side by side instead of adding."))
    # 12
    T = Dm("9.6") / 4
    assert T == Dm("2.4")
    its.append(mcq("Emma’s family cycles 9.6 km around the Stanley Park seawall. They split the ride into 4 equal parts. How long is each part?",
                   N(T) + " km", ["24 km", "0.24 km", "38.4 km"],
                   "9.6 is 96 tenths. 96 ÷ 4 = 24, so each part is 24 tenths = <b>2.4 km</b>. "
                   "Estimate: 8 ÷ 4 = 2. 38.4 km multiplies by 4."))
    # 13 multi-step
    T = (24 // 6) * Dm("4.50")
    assert T == 18
    its.append(mcq("A bag of 6 bagels costs $4.50. Wei needs 24 bagels for a class breakfast. How much do the bagels cost?",
                   M(T), ["$108", "$1.80", "$16.50"],
                   "Bags: 24 ÷ 6 = 4. Cost: 4.50 × 4 = 450 hundredths × 4 = 1800 hundredths = <b>%s</b>. "
                   "$108 is 24 × $4.50: it pays for 24 bags, not 24 bagels. $16.50 multiplies only the dollars." % M(T)))
    # 14 × 1000
    T = Dm("2.5") * 1000
    assert T == 2500
    its.append(mcq("A bag of rice has a mass of 2.5 kg. How many grams is that? (1 kg = 1000 g)",
                   N(T) + " g", ["250 g", "25 g", "25" + NB + "000 g"],
                   "Multiply by 1000: every digit moves 3 places to the left. 2.5 × 1000 = <b>2500 g</b>. "
                   "250 g multiplies by 100 only."))
    # 15 ÷ 100
    T = Dm(28) / 100
    assert T == Dm("0.28")
    its.append(mcq("Hana’s class buys a box of 100 pencils for $28. How much does one pencil cost?",
                   "28¢", ["$2.80", "$28", "2.8¢"],
                   "Divide by 100: $28 ÷ 100 = $0.28, which is <b>28¢</b>. $2.80 divides by 10 only. "
                   "2.8¢ is $0.028: it divides by 1000.", same_ok=True))
    # 16 change
    cost = Dm("2.35") * 3
    T = 10 - cost
    assert cost == Dm("7.05") and T == Dm("2.95")
    its.append(mcq("Nadia buys 3 notebooks for $2.35 each. She pays with a $10 bill. How much change does she get?",
                   M(T), ["$7.05", "$7.65", "$3.05"],
                   "Cost: 2.35 × 3 = $7.05. Change: $10.00 − $7.05 = <b>%s</b>. $7.05 is the cost, not the change. "
                   "$7.65 forgets to multiply by 3. $3.05 subtracts the smaller digit from the bigger one in each place "
                   "instead of regrouping." % M(T)))
    # 17
    T = Dm("0.35") * 7
    assert T == Dm("2.45")
    its.append(mcq("Owen’s dog eats 0.35 kg of food every day. How much food does it eat in one week?",
                   N(T) + " kg", ["24.5 kg", "0.245 kg", "7.35 kg"],
                   "One week is 7 days. 0.35 × 7 = 35 hundredths × 7 = 245 hundredths = <b>2.45 kg</b>. "
                   "7.35 kg adds instead of multiplying."))
    # 18 × 100
    T = Dm("14.50") * 100
    assert T == 1450
    its.append(mcq("Tickets for a field trip to the Vancouver Aquarium cost $14.50 per student. How much do tickets cost for 100 students?",
                   M(T), ["$145", "$14" + NB + "500", "$114.50"],
                   "Multiply by 100: every digit moves 2 places to the left. $14.50 × 100 = <b>%s</b>. "
                   "$145 multiplies by 10 only. $114.50 adds 100." % M(T)))
    # 19 two steps
    tot = Dm("1.75") * 3
    T = tot / 5
    assert tot == Dm("5.25") and T == Dm("1.05")
    its.append(mcq("Ryan pours 3 bottles of water, each 1.75 L, into a cooler for his lacrosse team. "
                   "The water is shared equally among 5 players. How much water does each player get?",
                   N(T) + " L", ["1.5 L", "10.5 L", "5.25 L"],
                   "Total: 1.75 × 3 = 5.25 L. Each player: 5.25 ÷ 5 = 525 hundredths ÷ 5 = 105 hundredths = <b>1.05 L</b>. "
                   "1.5 L drops the 0 that holds the tenths place. 5.25 L is the total, not each player’s share."))
    order = [0, 1, 2, 3, 5, 6, 14, 17, 4, 7, 8, 9, 10, 11, 12, 15, 18, 13, 16, 19]
    return {"title": "Money and measurement problems", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    f1 = pv_move("3.7", "×", 2)
    f2 = split_svg("1.4", 6)
    f3 = ld_svg("4.56", 4, "full")
    return (
        "<h2>Work with whole numbers, then place the decimal point</h2>"
        "<p>Think of a decimal as a number of tenths, hundredths or thousandths. Multiply or divide as if it were a "
        "whole number. Then change the answer back to a decimal. Use an estimate to check that the decimal point is "
        "in the right place.</p>"
        "<h2>× and ÷ by 10, 100 and 1000</h2>"
        "<p>When you multiply, every digit moves to the <b>left</b>. When you divide, every digit moves to the <b>right</b>. "
        "1 place for 10, 2 places for 100, 3 places for 1000. The decimal point stays still.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>3.7 × 100: every digit moves 2 places to the left. Write 0 in the empty ones place. "
        "3.7 × 100 = 370, not 3.700.</figcaption></figure>"
        "<h2>Decimal × whole number</h2>"
        "<p>Split the decimal into its whole-number part and its decimal part. Multiply each part, then add.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>1.4 × 6 = 6 + 2.4 = 8.4. Add the parts: do not write 6.24.</figcaption></figure>"
        + ex("Example 1", "2.35 × 6", "2.35 is 235 hundredths. 235 × 6 = 1410, so 2.35 × 6 = 1410 hundredths = 14.10. "
             "Estimate: 2 × 6 = 12, so 14.1 makes sense.", "14.1")
        + "<h2>Decimal ÷ whole number</h2>"
        "<p>4.56 is 456 hundredths. 456 ÷ 4 = 114, so 4.56 ÷ 4 = 114 hundredths = 1.14. "
        "In long division, put the point in the answer straight above the point in the number you divide.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4.56 ÷ 4 = 1.14. The decimal point in the answer sits above the decimal point in 4.56.</figcaption></figure>"
        + ex("Example 2", "4.08 ÷ 4", "4 ones ÷ 4 = 1 one. 0 tenths ÷ 4 = 0 tenths. 8 hundredths ÷ 4 = 2 hundredths.",
             "1.02 (keep the 0 in the tenths place)")
        + "<h2>Estimate to place the decimal point</h2>"
        "<p>Round to easy numbers first. 3.8 × 7 is about 4 × 7 = 28. The digits of the answer are 266, "
        "so the answer must be 26.6, not 2.66 or 266.</p>"
        + ex("Example 3", "A box of 8 granola bars costs $5.20. How much is one bar?",
             "520¢ ÷ 8 = 65¢. Estimate: $4 ÷ 8 = 50¢ and $8 ÷ 8 = $1, so the answer is between 50¢ and $1.", "$0.65 (65¢)")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3.7 × 10 = 3.70 (“just add a zero”)", "Move every digit 1 place to the left: 37"],
            ["2.3 × 4 = 8.12 (writing 8 and 12 side by side)", "Add the parts: 8 + 1.2 = 9.2"],
            ["2.35 × 6 = 12.35 (multiplying only the whole number)", "Multiply every digit: 14.1"],
            ["7.2 ÷ 6 = 12 (leaving out the point)", "72 tenths ÷ 6 = 12 tenths = 1.2"],
            ["4.08 ÷ 4 = 1.2 (dropping a zero)", "Keep the 0 that holds the tenths place: 1.02"],
            ["4.2 × 9 = 3.78 (point in the wrong place)", "Estimate 4 × 9 = 36, so the answer is 37.8"],
        ])
    )


FAQ = [
    {"q": "What does the BC Grade 6 math curriculum say about multiplying and dividing decimals?",
     "a": "Multiplication and division of decimals is a Grade 6 Computational fluency learning standard in the BC curriculum. On this page students multiply and divide decimals by whole numbers and by 10, 100 and 1000, and use estimates to place the decimal point."},
    {"q": "How do you multiply a decimal by a whole number?",
     "a": "Multiply as if there were no decimal point, then put the point back: 2.35 × 6 → 235 × 6 = 1410 → 14.10 = 14.1. Check with an estimate: 2 × 6 = 12, so the answer should be a bit more than 12."},
    {"q": "How do you divide a decimal by a whole number?",
     "a": "Divide as usual and put the decimal point in the answer straight above the point in the number you divide: 8.52 ÷ 4 = 2.13. Check by multiplying: 2.13 × 4 = 8.52."},
    {"q": "Why is 4.08 ÷ 4 equal to 1.02 and not 1.2?",
     "a": "There are 0 tenths in 4.08, and 0 tenths ÷ 4 is 0 tenths, so you must write a 0 in the tenths place. 1.2 is 1 and 2 tenths, which is 4.8 ÷ 4, not 4.08 ÷ 4."},
]


def mark_large(u, pattern):
    """Tag place value charts, number lines and split models so they print larger."""
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
    rnd = random.Random(56807)
    sets = [set_p10(), set_mul(), set_div(), set_estimate(), set_problems()]
    assert check_answers(sets) >= 45
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "multiplying-and-dividing-decimals",
        "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Multiplying and Dividing Decimals",
        "seo_title": "Grade 6 Multiplying and Dividing Decimals Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Multiplying and Dividing Decimals",
        "domain": "Computational fluency",
        "standard_code": "Grade 6: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Multiplication and division of decimals",
        "meta_desc": "Free Grade 6 math worksheets on multiplying and dividing decimals, matched to the BC curriculum: "
                     "× and ÷ by 10, 100 and 1000, decimals × whole numbers, decimals ÷ whole numbers, estimating to "
                     "place the decimal point, and money and measurement word problems. 100 questions with an answer key.",
        "key_big": "Multiply or divide as if the decimal were a whole number, then use an estimate to place the decimal point.",
        "key_sub": "2.35 × 6: 235 × 6 = 1410, and 2 × 6 = 12, so the answer is 14.1. "
                   "4.08 ÷ 4 = 1.02: keep the 0 in the tenths place.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "place value chart|number line|split model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
