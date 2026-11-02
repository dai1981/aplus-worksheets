# -*- coding: utf-8 -*-
"""
CA Grade 6 Math: Multiplying and dividing decimals (Ontario Mathematics Curriculum 2020, Number B2)
  python3 tools/gen_ca_math_g6_mult_div_decimals.py
× and ÷ by 10, 100 and 1000 on a place value chart, whole numbers × decimal tenths (24 × 0.3 = 72 tenths = 7.2),
decimals up to thousandths ÷ whole numbers up to 10 (4.56 = 456 hundredths, ÷ 4 = 114 hundredths = 1.14),
whole numbers ÷ decimal tenths (12 ÷ 0.4 = 120 ÷ 4 = 30), then estimating and word problems in Canadian contexts.
Every answer is computed with decimal.Decimal (never float). Wrong answers are real student mistakes:
the decimal point in the wrong place or left out, “just add a zero”, dividing only the whole-number part,
dropping a place-holding zero (1.02 -> 1.2), “multiplying always makes bigger / dividing always makes smaller”,
dividing the wrong way round, and adding instead of multiplying.
Canadian style: Canadian English, $ and ¢, metric units. 4-digit numbers have no separator (2070);
5 or more digits use a no-break space (20 700). HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written only to hold an empty place
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, Ontario style: 4536, 12 350 (no-break space), 0.045."""
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


VAL = re.compile(r"^(\$)?([\d ]*\.?\d+) ?(.*)$")


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


def tenths_word(n):
    return "1 tenth" if n == 1 else "%s tenths" % N(n)


def mul_t_e(w, d, note=""):
    """24 × 0.3: 0.3 is 3 tenths. 24 × 3 = 72, so 24 × 0.3 = 72 tenths = 7.2."""
    w, d = Dm(w), Dm(d)
    t = d * 10
    assert t == int(t)
    p = w * t
    r = w * d
    e = ("%s is %s. %s × %s = %s, so %s × %s = %s = <b>%s</b>."
         % (N(d), tenths_word(t), N(w), N(t), N(p), N(w), N(d), tenths_word(p), N(r)))
    if note:
        e += " " + note
    return e


def mul_t(w, d, wrong, note="", swap=False):
    r = Dm(w) * Dm(d)
    q = "%s × %s = ?" % ((N(d), N(w)) if swap else (N(w), N(d)))
    return mcq(q, N(r), wrong, mul_t_e(w, d, note))


def unit_word(k):
    return {1: "tenths", 2: "hundredths", 3: "thousandths"}[k]


def div_w_e(x, n, note=""):
    """4.56 ÷ 4: 4.56 is 456 hundredths. 456 ÷ 4 = 114, so 4.56 ÷ 4 = 114 hundredths = 1.14."""
    k = places(x)
    whole = int(Dm(x) * 10 ** k)
    r = Dm(x) / n
    assert r * n == Dm(x) and whole % n == 0
    e = ("%s is %s %s. %s ÷ %d = %s, so %s ÷ %d = %s %s = <b>%s</b>. Check: %s × %d = %s."
         % (x, N(whole), unit_word(k), N(whole), n, N(whole // n), x, n, N(whole // n), unit_word(k), N(r), N(r), n, x))
    if note:
        e += " " + note
    return e


def div_w(x, n, wrong, note=""):
    return mcq("%s ÷ %d = ?" % (x, n), N(Dm(x) / n), wrong, div_w_e(x, n, note))


def div_t_e(w, d, note=""):
    """12 ÷ 0.4: multiply both numbers by 10. 120 ÷ 4 = 30. Check: 30 × 0.4 = 12."""
    w, d = Dm(w), Dm(d)
    r = w / d
    assert r * d == w
    e = ("Multiply both numbers by 10 so you divide by a whole number: %s ÷ %s = %s ÷ %s = <b>%s</b>. "
         "Check: %s × %s = %s." % (N(w), N(d), N(w * 10), N(d * 10), N(r), N(r), N(d), N(w)))
    if note:
        e += " " + note
    return e


def div_t(w, d, wrong, note=""):
    return mcq("%s ÷ %s = ?" % (N(w), N(d)), N(Dm(w) / Dm(d)), wrong, div_t_e(w, d, note))


# ============================================================ set 1: × and ÷ by 10, 100, 1000
def set_p10():
    its = []
    # 0
    its.append(mcq(fig(pv_move("3.7", "×", 1, show_answer=False)) + "The chart shows 3.7 × 10. What is the answer?",
                   "37", ["3.70", "0.37", "370"],
                   p10_e("3.7", "×", 1, "3.70 is wrong: a zero at the end of a decimal does not change its value.")))
    # 1
    its.append(mcq(fig(pv_move("5.2", "÷", 1, show_answer=False)) + "The chart shows 5.2 ÷ 10. What is the answer?",
                   "0.52", ["52", "0.052", "5.02"],
                   p10_e("5.2", "÷", 1, "52 moves the digits the wrong way: dividing makes the number smaller.")))
    # 2
    its.append(p10("0.64", "×", 2, ["0.6400", "6.4", "640"], "0.6400 only adds zeros, so it is still 0.64."))
    # 3
    its.append(p10("38.5", "÷", 2, ["3850", "3.85", "0.0385"], "3850 moves the digits the wrong way."))
    # 4
    its.append(p10("2.07", "×", 3, ["207", "20" + NB + "700", "2.07000"],
                   "Keep the 0 that holds the hundreds place: 2070, not 207."))
    # 5
    its.append(p10("83", "÷", 3, ["0.83", "8.3", "83" + NB + "000"], "0.83 moves the digits only 2 places."))
    # 6 which calculation
    assert calc("4.15", "×", 1) == Dm("41.5")
    its.append(mcq(fig(pv_move("4.15", "×", 1)) + "Which calculation does the chart show?",
                   "4.15 × 10", ["4.15 ÷ 10", "4.15 × 100", "4.15 ÷ 100"],
                   "Every digit moved <b>1 place to the left</b>, so the number was multiplied by 10. "
                   "<b>4.15 × 10</b> = 41.5.", same_ok=True))
    # 7
    assert calc("72.6", "÷", 2) == Dm("0.726")
    its.append(mcq(fig(pv_move("72.6", "÷", 2)) + "Which calculation does the chart show?",
                   "72.6 ÷ 100", ["72.6 × 100", "72.6 ÷ 10", "72.6 ÷ 1000"],
                   "Every digit moved <b>2 places to the right</b>, so the number was divided by 100. "
                   "<b>72.6 ÷ 100</b> = 0.726.", same_ok=True))
    # 8 red digit
    assert calc("0.038", "×", 2) == Dm("3.8")
    its.append(mcq(fig(pv_move("0.038", "×", 2, hi=-3)) +
                   "The chart shows 0.038 × 100 = 3.8. What is the value of the red digit in the answer?",
                   "8 tenths", ["8 thousandths", "8 hundredths", "8 ones"],
                   "The 8 was in the thousandths place. Every digit moved 2 places to the left, so the 8 is now in the "
                   "<b>tenths</b> place. Its value is <b>8 tenths</b> = 0.8.", same_ok=True))
    # 9
    assert calc("6.24", "÷", 1) == Dm("0.624")
    its.append(mcq(fig(pv_move("6.24", "÷", 1, hi=-1)) +
                   "The chart shows 6.24 ÷ 10 = 0.624. What is the value of the red digit in the answer?",
                   "2 hundredths", ["2 tenths", "2 thousandths", "2 ones"],
                   "The 2 was in the tenths place. Every digit moved 1 place to the right, so the 2 is now in the "
                   "<b>hundredths</b> place. Its value is <b>2 hundredths</b> = 0.02.", same_ok=True))
    # 10
    its.append(p10("0.5", "÷", 2, ["0.05", "50", "0.0005"], "0.05 moves the digit only 1 place."))
    # 11
    its.append(p10("14.06", "×", 1, ["14.060", "1406", "140.06"],
                   "140.06 only multiplies the whole-number part. Every digit must move, including the 6."))
    # 12
    its.append(p10("470", "÷", 3, ["4.7", "0.047", "470" + NB + "000"],
                   "The last 0 is not needed after the decimal point: 0.470 = 0.47."))
    # 13
    assert calc("3.8", "÷", 2) == Dm("0.038")
    its.append(mcq("In <b>3.8 ÷ 100</b>, how do the digits move?", "2 places to the right",
                   ["2 places to the left", "3 places to the right", "1 place to the right"],
                   "100 has 2 zeros, so every digit moves <b>2 places</b>. Dividing makes the number smaller, so they "
                   "move to the <b>right</b>: 3.8 ÷ 100 = 0.038.", same_ok=True))
    # 14 missing numbers
    assert Dm("0.7") * 100 == 70
    its.append(mcq("0.7 × ? = 70", "100", ["10", "1000", "69.3"],
                   "The 7 moves from the tenths to the tens: that is 2 places to the left, so the missing number is "
                   "<b>100</b>. 69.3 is 70 − 0.7, which is subtraction, not multiplication."))
    assert Dm(63) / 1000 == Dm("0.063")
    its.append(mcq("63 ÷ ? = 0.063", "1000", ["100", "10", "10" + NB + "000"],
                   "The 3 moves from the ones to the thousandths: 3 places to the right. So the missing number is <b>1000</b>."))
    assert Dm("5.09") * 100 == 509
    its.append(mcq("? × 100 = 509", "5.09", ["50.9", "0.509", "5.9"],
                   "Use the inverse: 509 ÷ 100 = <b>5.09</b>. Check: 5.09 × 100 = 509. "
                   "5.9 drops the 0 that holds the tenths place."))
    assert Dm("3.6") / 10 == Dm("0.36")
    its.append(mcq("? ÷ 10 = 0.36", "3.6", ["0.036", "36", "3.06"],
                   "Use the inverse: 0.36 × 10 = <b>3.6</b>. Check: 3.6 ÷ 10 = 0.36. 0.036 divides instead of multiplying."))
    # 18 equivalent calculation
    assert Dm("2.5") * 100 == 25 * 10 == 250
    assert 250 not in {Dm("2.5") * 10, 25 * 100, Dm("0.25") * 10}
    its.append(mcq("Which calculation has the same answer as <b>2.5 × 100</b>?", "25 × 10",
                   ["2.5 × 10", "25 × 100", "0.25 × 10"],
                   "2.5 × 100 = 250. 2.5 × 10 = 25, and 25 × 10 = 250. So <b>25 × 10</b> gives the same answer.", same_ok=True))
    # 19
    assert Dm("0.029") * 1000 == 29
    its.append(mcq("Which number is <b>1000 times</b> as large as 0.029?", "29", ["2.9", "290", "0.029000"],
                   "1000 times as large means × 1000: every digit moves 3 places to the left. 0.029 × 1000 = <b>29</b>. "
                   "0.029000 only adds zeros, so it is still 0.029."))
    order = [0, 1, 2, 3, 6, 7, 10, 13, 4, 5, 8, 9, 11, 12, 14, 16, 15, 17, 18, 19]
    return {"title": "× and ÷ by 10, 100 and 1000", "items": reorder(its, order)}


# ============================================================ set 2: whole number × decimal tenths
def set_mul_tenths():
    its = []
    # 0-1 number lines
    assert 4 * Dm("0.3") == Dm("1.2")
    its.append(mcq(fig(jumps_svg("0.3", 4, 2)) + "The number line shows 4 jumps of 0.3. What is 4 × 0.3?",
                   "1.2", ["12", "0.12", "4.3"],
                   mul_t_e(4, "0.3", "The red dot is 2 small ticks past 1, at 1.2. 4.3 adds the numbers instead of multiplying.")))
    assert 6 * Dm("0.4") == Dm("2.4")
    its.append(mcq(fig(jumps_svg("0.4", 6, 3)) + "The number line shows 6 jumps of 0.4. What is 6 × 0.4?",
                   "2.4", ["24", "0.24", "6.4"],
                   mul_t_e(6, "0.4", "The red dot is 4 small ticks past 2, at 2.4.")))
    # 2-3 small facts
    its.append(mul_t(6, "0.2", ["12", "0.12", "6.2"], "12 forgets that 0.2 is only 2 tenths."))
    its.append(mul_t(7, "0.5", ["35", "0.35", "7.5"], "0.35 puts the decimal point one place too far left."))
    # 4 tenths language
    assert 8 * Dm("0.3") == Dm("2.4")
    its.append(mcq("8 × 0.3 means 8 groups of 3 tenths, which is 24 tenths. What is 24 tenths as a decimal?",
                   "2.4", ["24", "0.24", "20.4"],
                   "10 tenths make 1 whole, so 24 tenths = 2 wholes and 4 tenths = <b>2.4</b>. 0.24 is 24 hundredths."))
    # 5-11 bigger whole numbers
    its.append(mul_t(24, "0.3", ["72", "0.72", "8"],
                     "72 forgets to divide by 10. 8 is 24 ÷ 3: you multiply here, you do not divide."))
    its.append(mul_t(15, "0.6", ["90", "0.9", "15.6"], "90 forgets that 0.6 is less than 1, so the answer must be less than 15."))
    its.append(mul_t(32, "0.4", ["128", "1.28", "8"], "8 is 32 ÷ 4. 128 forgets to divide by 10."))
    its.append(mul_t(45, "0.2", ["90", "0.9", "45.2"], "45.2 adds 0.2 to 45 instead of multiplying."))
    its.append(mul_t(9, "0.7", ["63", "0.63", "9.7"], "You can multiply in any order: 0.7 × 9 = 9 × 0.7.", swap=True))
    its.append(mul_t(125, "0.8", ["1000", "10", "125.8"],
                     "1000 forgets that 0.8 is less than 1, so the answer must be less than 125."))
    its.append(mul_t(230, "0.6", ["1380", "13.8", "230.6"], "13.8 divides by 100, but 0.6 is tenths, so divide by 10."))
    its.append(mul_t(250, "0.8", ["2000", "20", "250.8"], "Think: 0.8 of 250 is a bit less than 250. 2000 is far too big.",
                     swap=True))
    # 13-14 tenths greater than 1
    assert 12 * Dm("2.5") == 30 and 12 * 2 + Dm("0.5") == Dm("24.5")
    its.append(mul_t(12, "2.5", ["300", "3", "24.5"],
                     "Or split it: 12 × 2 = 24 and 12 × 0.5 = 6, so 24 + 6 = 30. 24.5 forgets to multiply the 0.5 by 12."))
    assert 16 * Dm("1.5") == 24 and 16 + Dm("0.5") == Dm("16.5")
    its.append(mul_t(16, "1.5", ["240", "2.4", "16.5"],
                     "Or split it: 16 × 1 = 16 and 16 × 0.5 = 8, so 16 + 8 = 24. 16.5 forgets to multiply the 0.5 by 16."))
    # 15-16 multiplying does not always make bigger
    assert 36 * Dm("0.5") == 18
    its.append(mcq("Without working it out, which is true about <b>36 × 0.5</b>?", "It is less than 36",
                   ["It is greater than 36", "It is equal to 36", "It is greater than 360"],
                   "0.5 is less than 1, so 36 × 0.5 is less than 36 × 1 = 36. Multiplying by a decimal less than 1 makes "
                   "the number smaller. In fact 36 × 0.5 = 18 (half of 36).", same_ok=True))
    vals = {"50 × 0.9": 50 * Dm("0.9"), "50 × 1.2": 50 * Dm("1.2"), "50 × 2.5": 50 * Dm("2.5"), "50 × 1.1": 50 * Dm("1.1")}
    assert [k for k, v in vals.items() if v < 50] == ["50 × 0.9"]
    its.append(mcq("Which product is <b>less than 50</b>?", "50 × 0.9", ["50 × 1.2", "50 × 2.5", "50 × 1.1"],
                   "Only 0.9 is less than 1, so only <b>50 × 0.9</b> is less than 50 (it is 45). "
                   "Multiplying by a number greater than 1 makes 50 bigger.", same_ok=True))
    # 17 use a fact
    assert 26 * 4 == 104 and 26 * Dm("0.4") == Dm("10.4")
    its.append(mcq("Use 26 × 4 = 104 to find <b>26 × 0.4</b>.", "10.4", ["104", "1.04", "26.4"],
                   "0.4 is 4 ÷ 10, so the answer is 104 ÷ 10 = <b>10.4</b>. 1.04 divides by 100."))
    # 18 missing number
    assert 40 * Dm("0.3") == 12
    its.append(mcq("40 × ? = 12", "0.3", ["3", "0.03", "30"],
                   "40 × 3 = 120, which is 10 times too big. So the missing number is 3 ÷ 10 = <b>0.3</b>. "
                   "Check: 40 × 0.3 = 120 tenths = 12."))
    # 19 error
    assert 14 * Dm("0.5") == 7
    its.append(mcq("Amira says 14 × 0.5 = 70. What is the correct answer?", "7", ["70", "0.7", "14.5"],
                   "14 × 5 = 70, but 0.5 is 5 tenths, so 14 × 0.5 = 70 tenths = <b>7</b>. "
                   "Amira thought multiplying always makes a number bigger. Half of 14 is 7."))
    order = [0, 1, 2, 3, 4, 5, 6, 9, 8, 7, 17, 15, 16, 11, 10, 12, 13, 14, 18, 19]
    return {"title": "Whole numbers × decimal tenths", "items": reorder(its, order)}


# ============================================================ set 3: decimal ÷ whole number up to 10
def set_div_whole():
    its = []
    its.append(div_w("0.8", 2, ["4", "0.04", "1.6"], "1.6 multiplies instead of dividing."))
    assert Dm(6) / Dm("2.4") == Dm("2.5")
    its.append(div_w("2.4", 6, ["4", "0.04", "2.5"], "2.5 is 6 ÷ 2.4: it divides the wrong way round."))
    its.append(div_w("6.3", 3, ["21", "0.21", "2.3"], "2.3 divides only the 6 and forgets the 3 tenths."))
    its.append(div_w("8.4", 4, ["21", "0.21", "2.4"], "2.4 divides only the 8 and forgets the 4 tenths."))
    its.append(div_w("4.56", 4, ["114", "11.4", "1.56"], "1.56 divides only the 4 ones. 11.4 puts the point in the wrong place."))
    its.append(div_w("7.25", 5, ["145", "14.5", "1.25"], "14.5 is 10 times too big: 7.25 ÷ 5 must be less than 2."))
    its.append(div_w("9.36", 3, ["312", "31.2", "3.36"], "3.36 divides only the 9 ones."))
    assert Dm("5.6") * 8 == Dm("44.8")
    its.append(div_w("5.6", 8, ["7", "0.07", "44.8"], "5.6 is less than 8, so the answer is less than 1. 44.8 multiplies."))
    its.append(div_w("4.08", 4, ["1.2", "102", "10.2"],
                     "1.2 drops the 0 that holds the tenths place: 4 ÷ 4 = 1 one, 0 ÷ 4 = 0 tenths, 8 ÷ 4 = 2 hundredths."))
    its.append(div_w("12.6", 7, ["18", "0.18", "88.2"], "88.2 multiplies instead of dividing."))
    its.append(div_w("15.75", 7, ["22.5", "225", "0.225"], "22.5 puts the point in the wrong place: 14 ÷ 7 = 2, so the answer is about 2."))
    its.append(div_w("3.015", 3, ["1.05", "1.5", "1005"],
                     "1.05 and 1.5 drop the zeros that hold the tenths and hundredths places."))
    its.append(div_w("2.736", 8, ["3.42", "342", "0.0342"], "2.736 is less than 8, so the answer is less than 1."))
    its.append(div_w("1.845", 9, ["0.25", "2.05", "0.0205"], "0.25 drops the 0 that holds the hundredths place."))
    # long division: place the point
    assert Dm("7.38") / 3 == Dm("2.46")
    its.append(mcq(fig(ld_svg("7.38", 3, "digits")) +
                   "The quotient digits for 7.38 ÷ 3 are 2, 4, 6. Where does the decimal point go?",
                   "2.46", ["24.6", "246", "0.246"],
                   "Put the decimal point in the quotient straight above the point in 7.38. "
                   "Estimate: 6 ÷ 3 = 2 and 9 ÷ 3 = 3, so the answer is between 2 and 3. 7.38 ÷ 3 = <b>2.46</b>."))
    assert Dm("5.85") / 5 == Dm("1.17")
    its.append(mcq(fig(ld_svg("5.85", 5, "digits")) +
                   "The quotient digits for 5.85 ÷ 5 are 1, 1, 7. What is 5.85 ÷ 5?",
                   "1.17", ["11.7", "117", "0.117"],
                   "The point in the quotient goes straight above the point in 5.85. Estimate: 5 ÷ 5 = 1. "
                   "5.85 ÷ 5 = <b>1.17</b>. Check: 1.17 × 5 = 5.85."))
    assert Dm("0.954") / 9 == Dm("0.106")
    its.append(mcq(fig(ld_svg("0.954", 9, "digits")) +
                   "The quotient digits for 0.954 ÷ 9 are 0, 1, 0, 6. What is 0.954 ÷ 9?",
                   "0.106", ["1.06", "0.16", "10.6"],
                   "The point goes straight above the point in 0.954. 9 tenths ÷ 9 = 1 tenth, 5 hundredths ÷ 9 = 0 hundredths (keep the 0), "
                   "54 thousandths ÷ 9 = 6 thousandths. 0.954 ÷ 9 = <b>0.106</b>. 0.16 drops the 0."))
    # place value thinking
    its.append(mcq("4.56 is 456 hundredths. What is 456 hundredths ÷ 4?", "114 hundredths",
                   ["114 tenths", "114 ones", "114 thousandths"],
                   "456 ÷ 4 = 114, and the unit stays the same: <b>114 hundredths</b> = 1.14. "
                   "So 4.56 ÷ 4 = 1.14.", same_ok=True))
    # estimate and error
    assert abs(Dm("23.8") / 6 - 4) < Dm("0.1")
    its.append(mcq("Which is the best estimate for <b>23.8 ÷ 6</b>?", "4", ["40", "0.4", "143"],
                   "23.8 is close to 24, and 24 ÷ 6 = <b>4</b>. 143 is about 23.8 × 6: it multiplies instead of dividing."))
    assert Dm("9.45") / 5 == Dm("1.89")
    its.append(mcq("Lucas says 9.45 ÷ 5 = 18.9. Use an estimate to check. What is the correct answer?", "1.89",
                   ["18.9", "0.189", "189"],
                   "Estimate: 10 ÷ 5 = 2, so the answer is about 2, not about 19. 945 hundredths ÷ 5 = 189 hundredths, "
                   "so 9.45 ÷ 5 = <b>1.89</b>."))
    order = [0, 1, 2, 3, 7, 4, 17, 5, 6, 14, 15, 9, 8, 10, 11, 16, 12, 13, 18, 19]
    return {"title": "Decimals ÷ whole numbers", "items": reorder(its, order)}


# ============================================================ set 4: whole number ÷ decimal tenths
def set_div_tenths():
    its = []
    # 0-2 number lines
    assert Dm(2) / Dm("0.4") == 5
    its.append(mcq(fig(jumps_svg("0.4", 5, 2)) + "How many jumps of 0.4 make 2? Use the number line to find 2 ÷ 0.4.",
                   "5", ["0.5", "50", "0.8"],
                   "Count the jumps from 0 to 2: there are 5. So 2 ÷ 0.4 = <b>5</b>. Check: 5 × 0.4 = 2. "
                   "0.8 is 2 × 0.4: it multiplies instead of dividing."))
    assert Dm(3) / Dm("0.5") == 6
    its.append(mcq(fig(jumps_svg("0.5", 6, 3)) + "How many jumps of 0.5 make 3? Use the number line to find 3 ÷ 0.5.",
                   "6", ["0.6", "60", "1.5"],
                   "Count the jumps from 0 to 3: there are 6 (2 in each whole). So 3 ÷ 0.5 = <b>6</b>. "
                   "1.5 is 3 × 0.5: it multiplies instead of dividing."))
    assert Dm(1) / Dm("0.2") == 5
    its.append(mcq(fig(jumps_svg("0.2", 5, 1)) + "How many jumps of 0.2 make 1? Use the number line to find 1 ÷ 0.2.",
                   "5", ["0.5", "50", "0.2"],
                   "Count the jumps from 0 to 1: there are 5. So 1 ÷ 0.2 = <b>5</b>. Check: 5 × 0.2 = 1."))
    # 3-14 calculations
    its.append(div_t(6, "0.3", ["2", "200", "1.8"], "2 is 6 ÷ 3: it forgets that 0.3 is 3 tenths, not 3."))
    its.append(div_t(12, "0.4", ["3", "300", "4.8"], "4.8 is 12 × 0.4. Dividing by a number less than 1 gives a bigger answer."))
    its.append(div_t(8, "0.2", ["4", "400", "1.6"], "4 is 8 ÷ 2: it forgets that 0.2 is 2 tenths."))
    its.append(div_t(15, "0.5", ["3", "7.5", "300"], "7.5 is 15 × 0.5 (half of 15). How many halves are in 15? 30."))
    its.append(div_t(9, "0.1", ["0.9", "9", "900"], "0.9 is 9 × 0.1. There are 10 tenths in each whole, so 90 tenths in 9."))
    its.append(div_t(14, "0.7", ["2", "9.8", "200"], "9.8 is 14 × 0.7: it multiplies instead of dividing."))
    its.append(div_t(36, "0.9", ["4", "32.4", "400"], "4 is 36 ÷ 9: it forgets to multiply 36 by 10 as well."))
    its.append(div_t(7, "0.5", ["3.5", "1.4", "140"], "3.5 is 7 × 0.5. There are 2 halves in each whole, so 14 halves in 7."))
    its.append(div_t(24, "0.6", ["4", "14.4", "400"], "14.4 is 24 × 0.6: it multiplies instead of dividing."))
    its.append(div_t(5, "0.4", ["1.25", "125", "2"], "2 is 5 × 0.4: it multiplies instead of dividing."))
    its.append(div_t(18, "1.2", ["1.5", "150", "21.6"], "21.6 is 18 × 1.2: it multiplies instead of dividing."))
    its.append(div_t(9, "1.5", ["0.6", "60", "13.5"], "13.5 is 9 × 1.5. Count by 1.5: 1.5, 3, 4.5, 6, 7.5, 9 is 6 jumps."))
    # 15 same answer
    assert Dm(12) / Dm("0.4") == Dm(120) / 4 == 30
    assert 30 not in {Dm(12) / 4, Dm("1.2") / 4, Dm(120) / 40}
    its.append(mcq("Which calculation has the same answer as <b>12 ÷ 0.4</b>?", "120 ÷ 4",
                   ["12 ÷ 4", "1.2 ÷ 4", "120 ÷ 40"],
                   "Multiply <b>both</b> numbers by 10: 12 ÷ 0.4 = <b>120 ÷ 4</b> = 30. 12 ÷ 4 = 3 changes only the 0.4.",
                   same_ok=True))
    # 16 dividing makes smaller?
    assert Dm(20) / Dm("0.5") == 40
    its.append(mcq("Without working it out, which is true about <b>20 ÷ 0.5</b>?", "It is greater than 20",
                   ["It is less than 20", "It is equal to 20", "It is equal to 10"],
                   "0.5 is less than 1, so there are more than 20 halves in 20. Dividing by a decimal less than 1 makes "
                   "the answer bigger. In fact 20 ÷ 0.5 = 40. 10 is half of 20, which is 20 × 0.5.", same_ok=True))
    # 17 tenths thinking
    assert Dm(3) / Dm("0.6") == 5
    its.append(mcq("3 is 30 tenths and 0.6 is 6 tenths. How many groups of 6 tenths are in 30 tenths? (This is 3 ÷ 0.6.)",
                   "5", ["0.5", "50", "1.8"],
                   "30 tenths ÷ 6 tenths = 30 ÷ 6 = <b>5</b>. Check: 5 × 0.6 = 3. 1.8 is 3 × 0.6."))
    # 18 missing number
    assert Dm(7) / Dm("0.2") == 35
    its.append(mcq("? ÷ 0.2 = 35", "7", ["175", "70", "0.7"],
                   "Use the inverse: 35 × 0.2 = 70 tenths = <b>7</b>. Check: 7 ÷ 0.2 = 70 ÷ 2 = 35. "
                   "175 is 35 ÷ 0.2: it divides instead of multiplying."))
    # 19 error
    assert Dm(16) / Dm("0.8") == 20
    its.append(mcq("Ethan says 16 ÷ 0.8 = 2. What is the correct answer?", "20", ["2", "12.8", "200"],
                   "16 ÷ 0.8 = 160 ÷ 8 = <b>20</b>. Ethan worked out 16 ÷ 8 and forgot to multiply 16 by 10 as well. "
                   "Check: 20 × 0.8 = 16, but 2 × 0.8 is only 1.6."))
    order = [0, 2, 1, 3, 5, 7, 4, 6, 10, 17, 16, 8, 11, 9, 15, 12, 13, 14, 18, 19]
    return {"title": "Whole numbers ÷ decimal tenths", "items": reorder(its, order)}


# ============================================================ set 5: estimate and word problems
def set_problems():
    its = []
    T = 4 * Dm("3.5")
    assert T == 14
    its.append(mcq("Apples cost $4 per kilogram. Olivia buys 3.5 kg. How much does she pay?", M(T),
                   ["$1.40", "$140", "$7.50"],
                   "4 × 3.5 = 4 × 35 tenths = 140 tenths = <b>%s</b>. Check: 4 × 3 = 12 and 4 × 0.5 = 2. "
                   "$7.50 adds 4 + 3.5 instead of multiplying." % M(T)))
    T = Dm("2.25") / 5
    assert T == Dm("0.45")
    its.append(mcq("A 2.25 L bottle of juice is shared equally among 5 friends. How much juice does each friend get?",
                   N(T) + " L", ["4.5 L", "0.045 L", "11.25 L"],
                   "2.25 L is 225 hundredths. 225 ÷ 5 = 45, so each friend gets 45 hundredths = <b>0.45 L</b> (450 mL). "
                   "11.25 L multiplies: each friend cannot get more than the whole bottle."))
    T = Dm(12) / Dm("0.5")
    assert T == 24
    its.append(mcq("A sugar shack pours 12 L of maple syrup into bottles that hold 0.5 L each. How many bottles does it fill?",
                   "%s bottles" % N(T), ["6 bottles", "60 bottles", "240 bottles"],
                   "12 ÷ 0.5 = 120 ÷ 5 = <b>24 bottles</b>. Each litre fills 2 bottles, so 12 L fill 24. "
                   "6 bottles divides by 2 instead of 0.5."))
    T = Dm(6) / Dm("0.4")
    assert T == 15
    its.append(mcq("One lap of the school field is 0.4 km. How many laps make 6 km for the Terry Fox Run?",
                   "%s laps" % N(T), ["24 laps", "150 laps", "60 laps"],
                   "6 ÷ 0.4 = 60 ÷ 4 = <b>15 laps</b>. Check: 15 × 0.4 = 6. "
                   "24 laps is 6 × 4: it forgets that 0.4 is 4 tenths."))
    T = 15 * Dm("0.8")
    assert T == 12
    its.append(mcq("Priya runs 0.8 km every day for 15 days. How far does she run in all?", N(T) + " km",
                   ["120 km", "1.2 km", "15.8 km"],
                   "15 × 0.8 = 15 × 8 tenths = 120 tenths = <b>12 km</b>. 120 km forgets to divide by 10. "
                   "15.8 km adds instead of multiplying."))
    T = Dm("4.5") / 9
    assert T == Dm("0.5")
    its.append(mcq("Zoe cuts a 4.5 m ribbon into 9 equal pieces for the class banner. How long is each piece?",
                   N(T) + " m", ["5 m", "0.05 m", "2 m"],
                   "4.5 is 45 tenths. 45 ÷ 9 = 5, so each piece is 5 tenths = <b>0.5 m</b> (50 cm). "
                   "2 m is 9 ÷ 4.5: it divides the wrong way round."))
    T = Dm("4.86") / 6
    assert T == Dm("0.81")
    its.append(mcq("A pack of 6 juice boxes costs $4.86. How much is one juice box?", M(T),
                   ["$8.10", "$29.16", "$10.86"],
                   "486 cents ÷ 6 = 81 cents, so one box costs <b>%s</b> (81¢). $8.10 puts the point in the wrong place. "
                   "$29.16 multiplies by 6." % M(T)))
    T = Dm("1.35") / 9
    assert T == Dm("0.15")
    its.append(mcq("On a canoe trip, 9 campers share a 1.35 kg bag of trail mix equally. How much does each camper get?",
                   N(T) + " kg", ["1.5 kg", "0.015 kg", "12.15 kg"],
                   "1.35 is 135 hundredths. 135 ÷ 9 = 15, so each camper gets 15 hundredths = <b>0.15 kg</b> (150 g). "
                   "1.5 kg is more than the whole bag."))
    T = 14 * Dm("0.3")
    assert T == Dm("4.2")
    its.append(mcq("Each batch of pancakes uses 0.3 L of milk. How much milk is needed for 14 batches?", N(T) + " L",
                   ["42 L", "0.42 L", "14.3 L"],
                   "14 × 0.3 = 14 × 3 tenths = 42 tenths = <b>4.2 L</b>. 42 L forgets to divide by 10."))
    T = Dm(3) / Dm("0.2")
    assert T == 15
    its.append(mcq("A 3 L jug of water fills paper cups that hold 0.2 L each. How many cups can be filled?",
                   "%s cups" % N(T), ["0.6 cups", "1.5 cups", "150 cups"],
                   "3 ÷ 0.2 = 30 ÷ 2 = <b>15 cups</b>. Each litre fills 5 cups. 0.6 is 3 × 0.2: it multiplies instead of dividing."))
    T = 8 * Dm("2.4")
    assert T == Dm("19.2")
    its.append(mcq("During a snowstorm, 2.4 cm of snow fell every hour for 8 hours. How much snow fell in all?",
                   N(T) + " cm", ["192 cm", "1.92 cm", "10.4 cm"],
                   "8 × 2.4 = 8 × 24 tenths = 192 tenths = <b>19.2 cm</b>. Check: 8 × 2 = 16 and 8 × 0.4 = 3.2. "
                   "10.4 cm adds instead of multiplying."))
    T = Dm("7.2") / 8
    assert T == Dm("0.9")
    its.append(mcq("A 7.2 km hiking trail is split into 8 equal sections. How long is each section?", N(T) + " km",
                   ["9 km", "0.09 km", "57.6 km"],
                   "7.2 is 72 tenths. 72 ÷ 8 = 9, so each section is 9 tenths = <b>0.9 km</b>. "
                   "9 km is longer than the whole trail."))
    T = Dm(12) / Dm("0.4")
    assert T == 30
    its.append(mcq("Leah’s dog eats 0.4 kg of food a day. How many days does a 12 kg bag last?",
                   "%s days" % N(T), ["3 days", "4.8 days", "300 days"],
                   "12 ÷ 0.4 = 120 ÷ 4 = <b>30 days</b>. Check: 30 × 0.4 = 12. 4.8 days is 12 × 0.4."))
    T = 9 * Dm("2.5")
    assert T == Dm("22.5")
    its.append(mcq("Fabric for a team banner costs $9 per metre. Owen buys 2.5 m. How much does he pay?", M(T),
                   ["$225", "$2.25", "$11.50"],
                   "9 × 2.5 = 9 × 25 tenths = 225 tenths = 22.5, so he pays <b>%s</b>. Check: 9 × 2 = 18 and 9 × 0.5 = 4.5. "
                   "$11.50 adds 9 + 2.5." % M(T)))
    # estimates
    assert abs(18 * Dm("2.9") - 54) < 2
    its.append(mcq("Canoe rental costs $18 per hour. Which is the best estimate of the cost for 2.9 hours?", "$54",
                   ["$5.40", "$540", "$36"],
                   "2.9 hours is close to 3 hours. $18 × 3 = <b>$54</b>. $36 rounds 2.9 down to 2, but 2.9 is much closer to 3."))
    assert abs(Dm("4.9") * 2 - 10) < Dm("0.3")
    its.append(mcq("Potatoes cost $2 per kilogram. Which is the best estimate of the cost of 4.9 kg?", "$10",
                   ["$1", "$100", "$8"],
                   "4.9 kg is about 5 kg, and 5 × $2 = <b>$10</b>. (The exact cost is 4.9 × 2 = $9.80.) "
                   "$8 rounds 4.9 down to 4."))
    assert abs(Dm("7.92") / 4 - 2) < Dm("0.1")
    its.append(mcq("Four friends share a $7.92 bill for snacks at the skating rink. About how much does each friend pay?",
                   "$2", ["$20", "$0.20", "$32"],
                   "$7.92 is close to $8, and $8 ÷ 4 = <b>$2</b> each. (Exactly: 792¢ ÷ 4 = 198¢ = $1.98.) "
                   "$32 multiplies by 4 instead of dividing."))
    assert 6 * Dm("3.5") == 21
    its.append(mcq("Kai works out the cost of 3.5 kg of grapes at $6 per kilogram and gets $210. "
                   "What is the correct cost?", "$21", ["$2.10", "$210", "$9.50"],
                   "6 × 35 = 210, but 3.5 is 35 tenths, so 6 × 3.5 = 210 tenths = <b>$21</b>. "
                   "Estimate: 6 × 3 = 18 and 6 × 4 = 24, so the cost is between $18 and $24."))
    # multi-step
    T = 20 - 4 * Dm("3.5")
    assert T == 6
    its.append(mcq("Maya buys 3.5 kg of apples at $4 per kilogram. She pays with a $20 bill. How much change does she get?",
                   M(T), ["$14", "$18.60", "$12.50"],
                   "Cost: 4 × 3.5 = $14. Change: $20 − $14 = <b>%s</b>. $14 is the cost, not the change. "
                   "$12.50 adds 4 + 3.5 instead of multiplying." % M(T)))
    cups = Dm(3) / Dm("0.2")
    T = cups * Dm("0.5")
    assert cups == 15 and T == Dm("7.5")
    its.append(mcq("Noah makes 3 L of lemonade for a stand. He pours it into cups that hold 0.2 L each and sells every cup "
                   "for 50¢. How much money does he collect?", M(T), ["$75", "$1.50", "$15"],
                   "Cups: 3 ÷ 0.2 = 30 ÷ 2 = 15. Money: 15 × 50¢ = 750¢ = <b>%s</b>. "
                   "$15 is the number of cups, and $1.50 is 3 × 50¢." % M(T)))
    order = [0, 1, 4, 2, 8, 5, 3, 9, 14, 15, 10, 11, 13, 6, 7, 12, 16, 17, 18, 19]
    return {"title": "Estimate and solve word problems", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    f1 = pv_move("2.4", "×", 1)
    f2 = jumps_svg("0.3", 4, 2, show_end_label=True)
    f3 = ld_svg("4.56", 4, "full")
    f4 = jumps_svg("0.4", 5, 2)
    return (
        "<h2>Work with whole numbers, then place the decimal point</h2>"
        "<p>Think of a decimal as a number of tenths, hundredths or thousandths. Do the calculation with whole numbers. "
        "Then change the answer back to a decimal. Estimate to check that the decimal point is in the right place.</p>"
        "<h2>× and ÷ by 10, 100 and 1000</h2>"
        "<p>When you multiply, every digit moves to the <b>left</b>. When you divide, every digit moves to the <b>right</b>. "
        "1 place for 10, 2 places for 100, 3 places for 1000. The decimal point stays still.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>2.4 × 10: the 2 moves from the ones to the tens and the 4 from the tenths to the ones. "
        "2.4 × 10 = 24, not 2.40.</figcaption></figure>"
        "<h2>Whole number × decimal tenths</h2>"
        "<p>0.3 is 3 tenths. So 4 × 0.3 is 4 groups of 3 tenths = 12 tenths = 1.2.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>4 jumps of 0.3 end at 1.2. The answer is less than 4, because 0.3 is less than 1.</figcaption></figure>"
        + ex("Example 1", "24 × 0.3", "0.3 is 3 tenths. 24 × 3 = 72, so 24 × 0.3 = 72 tenths = 7.2. "
             "Check: 0.3 is a bit less than half, and half of 24 is 12, so 7.2 makes sense.", "7.2")
        + "<h2>Decimal ÷ whole number</h2>"
        "<p>4.56 is 456 hundredths. 456 ÷ 4 = 114, so 4.56 ÷ 4 = 114 hundredths = 1.14. "
        "In long division, put the point in the answer straight above the point in the number you divide.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4.56 ÷ 4 = 1.14. The decimal point in the answer sits above the decimal point in 4.56.</figcaption></figure>"
        + ex("Example 2", "4.08 ÷ 4", "4 ones ÷ 4 = 1 one. 0 tenths ÷ 4 = 0 tenths. 8 hundredths ÷ 4 = 2 hundredths.",
             "1.02 (keep the 0 in the tenths place)")
        + "<h2>Whole number ÷ decimal tenths</h2>"
        "<p>2 ÷ 0.4 asks: how many jumps of 0.4 make 2? Or multiply both numbers by 10 and divide by a whole number.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>5 jumps of 0.4 make 2, so 2 ÷ 0.4 = 5.</figcaption></figure>"
        + ex("Example 3", "12 ÷ 0.4", "Multiply both numbers by 10: 12 ÷ 0.4 = 120 ÷ 4 = 30. Check: 30 × 0.4 = 12.", "30")
        + ex("Example 4", "Apples cost $4 per kilogram. How much do 3.5 kg cost?",
             "4 × 3.5 = 4 × 35 tenths = 140 tenths = 14. Estimate: between 4 × 3 = $12 and 4 × 4 = $16.", "$14")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["24 × 0.3 = 72 (forgetting the decimal point)", "0.3 is 3 tenths: 72 tenths = 7.2"],
            ["“Multiplying always makes bigger”", "× a number less than 1 makes it smaller: 36 × 0.5 = 18"],
            ["“Dividing always makes smaller”", "÷ a number less than 1 makes it bigger: 12 ÷ 0.4 = 30"],
            ["12 ÷ 0.4 = 3 (dividing by 4 instead of 0.4)", "Multiply both numbers by 10: 120 ÷ 4 = 30"],
            ["4.56 ÷ 4 = 1.56 (dividing only the ones)", "Divide every digit: 4.56 ÷ 4 = 1.14"],
            ["4.08 ÷ 4 = 1.2 (dropping a zero)", "Keep the 0 that holds the tenths place: 1.02"],
            ["2.4 × 10 = 2.40 (“just add a zero”)", "Move every digit 1 place to the left: 24"],
        ])
    )


FAQ = [
    {"q": "What does the Ontario Grade 6 math curriculum say about multiplying and dividing decimals?",
     "a": "Grade 6 students multiply and divide whole numbers by decimal tenths, like 24 × 0.3 and 12 ÷ 0.4, and divide decimals up to thousandths by whole numbers up to 10, like 4.56 ÷ 4. They also multiply and divide by 10, 100 and 1000 and use tools and strategies to explain their thinking."},
    {"q": "Does multiplying always make a number bigger?",
     "a": "No. Multiplying by a number less than 1 makes it smaller: 36 × 0.5 = 18. In the same way, dividing by a number less than 1 makes it bigger: 12 ÷ 0.4 = 30."},
    {"q": "How do you divide a whole number by a decimal, like 12 ÷ 0.4?",
     "a": "Multiply both numbers by 10 so you divide by a whole number: 12 ÷ 0.4 = 120 ÷ 4 = 30. Check by multiplying: 30 × 0.4 = 12."},
    {"q": "Is multiplying and dividing decimals on the Grade 6 EQAO math test?",
     "a": "The Grade 6 EQAO math assessment is based on the Ontario curriculum, and decimal multiplication and division are part of the Number strand. Word problems with money and measurement like the ones on this page are good practice."},
]


def mark_large(u, pattern):
    """Tag place value charts and number lines so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every plain 'a × b = ?' / 'a ÷ b = ?' question with Decimal."""
    rx = re.compile(r"^([\d .]+) ([×÷]) ([\d .]+) = \?$")
    n = 0
    for s in sets:
        for it in s["items"]:
            m = rx.match(it["q"])
            if m:
                a, op, b = Dm(m.group(1).replace(NB, "")), m.group(2), Dm(m.group(3).replace(NB, ""))
                r = a * b if op == "×" else a / b
                assert val(it["c"][it["a"]])[0] == r, it["q"]
                n += 1
    return n


def gen():
    rnd = random.Random(36806)
    sets = [set_p10(), set_mul_tenths(), set_div_whole(), set_div_tenths(), set_problems()]
    assert check_answers(sets) >= 45
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
        "country": "ca-on", "subject": "math", "grade": "grade-6", "slug": "multiplying-and-dividing-decimals",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing Decimals",
        "seo_title": "Grade 6 Multiplying and Dividing Decimals Worksheets (Free, Ontario, Answer Key)",
        "short_title": "Multiplying and dividing decimals",
        "domain": "Number",
        "standard_code": "Grade 6: Number, B2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide whole numbers by decimal tenths, and divide decimal numbers up to thousandths by whole numbers up to 10, using appropriate tools and strategies",
        "meta_desc": "Free Grade 6 math worksheets on multiplying and dividing decimals for the Ontario curriculum: × and ÷ by 10, 100 and 1000, whole numbers × tenths, decimals ÷ whole numbers, whole numbers ÷ tenths and word problems. 100 questions with an answer key, great for EQAO practice.",
        "key_big": "Work with whole numbers, then place the decimal point: 24 × 0.3 = 72 tenths = 7.2.",
        "key_sub": "4.56 ÷ 4 = 456 hundredths ÷ 4 = 1.14. 12 ÷ 0.4 = 120 ÷ 4 = 30. Multiplying by a number less than 1 makes the answer smaller, and dividing by it makes the answer bigger.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "place value chart|number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
