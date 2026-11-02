# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Multiplying and dividing decimals by powers of 10 (Australian Curriculum v9.0, AC9M6N06)
  python3 tools/gen_au_maths_y6_powers_of_10.py
× and ÷ by 10, 100 and 1000 on a place value chart (the digits move, the decimal point stays still),
multiples of powers of 10 (0.3 × 40 = 12, 2.4 ÷ 20 = 0.12), converting metric units and money,
estimating to check that answers are reasonable, then word problems in Australian contexts.
Every answer is computed with decimal.Decimal (never float). Wrong answers are real student mistakes:
“just add a zero” (2.4 × 10 = 2.40), moving the digits the wrong way or the wrong number of places,
forgetting the × 10 / ÷ 10 step of a multiple, and dropping a place-holding zero.
Australian English, $ and c, metric units. Numbers of 5 or more digits use a no-break space (10 000);
4-digit numbers have no separator (4536). HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written only to hold an empty place
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, Australian style: 4536, 12 350 (no-break space), 0.045."""
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
    """Money: $245, $24.50, $1099."""
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


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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
    Zeros that only hold an empty place are grey. hi: place of a digit of x; that digit is red in the answer row.
    show_answer=False leaves the answer row empty (the arrows still show where the digits go)."""
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
        if p + shift not in bot:      # a zero that is not written in the answer (4.50 -> 45)
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


def mult_q(a, b, wrong, e):
    """a × b with b a multiple of a power of 10. Checked with Decimal."""
    r = Dm(a) * Dm(b)
    return mcq("%s × %s = ?" % (N(a), N(b)), N(r), wrong, e)


def div_q(a, b, wrong, e):
    r = Dm(a) / Dm(b)
    assert r * Dm(b) == Dm(a)
    return mcq("%s ÷ %s = ?" % (N(a), N(b)), N(r), wrong, e)


def split_e(a, b, op):
    """0.3 × 40: 0.3 × 4 = 1.2, then 1.2 × 10 = 12."""
    b = Dm(b)
    k = 0
    m = b
    while m % 10 == 0:
        m /= 10
        k += 1
    m = int(m)
    a = Dm(a)
    if op == "×":
        s1 = a * m
        r = s1 * 10 ** k
        return ("%s = %d × %s. First %s × %d = %s. Then %s × %s = <b>%s</b> (the digits move %s to the left)."
                % (N(b), m, P10(k), N(a), m, N(s1), N(s1), P10(k), N(r), moves(k)))
    s1 = a / m
    r = s1 / 10 ** k
    assert s1 * m == a
    return ("%s = %d × %s. First %s ÷ %d = %s. Then %s ÷ %s = <b>%s</b> (the digits move %s to the right)."
            % (N(b), m, P10(k), N(a), m, N(s1), N(s1), P10(k), N(r), moves(k)))


# ============================================================ set 1: × and ÷ by 10, 100, 1000
def set_p10():
    its = []
    # 0
    its.append(mcq(fig(pv_move("2.4", "×", 1, show_answer=False)) + "The chart shows 2.4 × 10. What is the answer?",
                   "24", ["2.40", "0.24", "240"],
                   p10_e("2.4", "×", 1, "2.40 is wrong: adding a zero at the end of a decimal does not change its value.")))
    # 1
    its.append(mcq(fig(pv_move("3.6", "÷", 1, show_answer=False)) + "The chart shows 3.6 ÷ 10. What is the answer?",
                   "0.36", ["36", "0.036", "3.06"],
                   p10_e("3.6", "÷", 1, "36 moves the digits the wrong way.")))
    # 2
    its.append(p10("0.75", "×", 2, ["0.7500", "7.5", "750"],
                   "0.7500 just adds zeros, so it is still 0.75."))
    # 3
    its.append(p10("45.2", "÷", 2, ["4520", "4.52", "0.0452"],
                   "4520 moves the digits the wrong way."))
    # 4
    its.append(p10("1.08", "×", 3, ["108", "10" + NB + "800", "1.08000"],
                   "Keep the 0 that holds the tenths place: 1080, not 108."))
    # 5
    its.append(p10("6.5", "÷", 3, ["0.065", "6500", "0.65"],
                   "0.065 moves the digits only 2 places."))
    # 6  which calculation
    its.append(mcq(fig(pv_move("3.27", "×", 1)) + "Which calculation does the chart show?",
                   "3.27 × 10", ["3.27 ÷ 10", "3.27 × 100", "3.27 ÷ 100"],
                   "Every digit moved <b>1 place to the left</b>, so the number was multiplied by 10. "
                   "<b>3.27 × 10</b> = 32.7.", same_ok=True))
    # 7
    its.append(mcq(fig(pv_move("58.4", "÷", 2)) + "Which calculation does the chart show?",
                   "58.4 ÷ 100", ["58.4 × 100", "58.4 ÷ 10", "58.4 ÷ 1000"],
                   "Every digit moved <b>2 places to the right</b>, so the number was divided by 100. "
                   "<b>58.4 ÷ 100</b> = 0.584.", same_ok=True))
    # 8  red digit
    its.append(mcq(fig(pv_move("0.046", "×", 2, hi=-3)) +
                   "The chart shows 0.046 × 100 = 4.6. What is the value of the red digit in the answer?",
                   "6 tenths", ["6 thousandths", "6 hundredths", "6 ones"],
                   "The 6 was in the thousandths place. Every digit moved 2 places to the left, so the 6 is now in the "
                   "<b>tenths</b> place. Its value is <b>6 tenths</b> = 0.6.", same_ok=True))
    # 9
    its.append(mcq(fig(pv_move("7.31", "÷", 1, hi=-1)) +
                   "The chart shows 7.31 ÷ 10 = 0.731. What is the value of the red digit in the answer?",
                   "3 hundredths", ["3 tenths", "3 thousandths", "3 ones"],
                   "The 3 was in the tenths place. Every digit moved 1 place to the right, so the 3 is now in the "
                   "<b>hundredths</b> place. Its value is <b>3 hundredths</b> = 0.03.", same_ok=True))
    # 10
    its.append(p10("0.3", "÷", 2, ["0.03", "30", "0.0003"],
                   "0.03 moves the digits only 1 place."))
    # 11
    its.append(p10("12.05", "×", 1, ["12.050", "1205", "120.05"],
                   "120.05 only multiplies the whole number part. Every digit must move, including the 5."))
    # 12
    its.append(p10("260", "÷", 3, ["2.6", "0.026", "260" + NB + "000"],
                   "The last 0 is not needed after the point."))
    # 13  how far do digits move
    its.append(mcq("In <b>6.2 × 1000</b>, how do the digits move?", "3 places to the left",
                   ["3 places to the right", "2 places to the left", "1 place to the left"],
                   "1000 has 3 zeros, so every digit moves <b>3 places</b>. Multiplying makes the number bigger, so they "
                   "move to the <b>left</b>: 6.2 × 1000 = 6200.", same_ok=True))
    assert calc("6.2", "×", 3) == 6200
    # 14 missing numbers
    assert Dm("0.9") * 100 == 90
    its.append(mcq("0.9 × ? = 90", "100", ["10", "1000", "89.1"],
                   "The 9 moves from the tenths to the tens: that is 2 places to the left, so the missing number is "
                   "<b>100</b>. 89.1 is 90 − 0.9, which is subtraction, not multiplication."))
    assert Dm(52) / 1000 == Dm("0.052")
    its.append(mcq("52 ÷ ? = 0.052", "1000", ["100", "10", "10" + NB + "000"],
                   "The 2 moves from the ones to the thousandths: 3 places to the right. So the missing number is <b>1000</b>."))
    assert Dm("3.07") * 100 == 307
    its.append(mcq("? × 100 = 307", "3.07", ["30.7", "0.307", "3.7"],
                   "Use the inverse: 307 ÷ 100 = <b>3.07</b>. Check: 3.07 × 100 = 307. "
                   "3.7 drops the 0 that holds the tenths place."))
    assert Dm("4.8") / 10 == Dm("0.48")
    its.append(mcq("? ÷ 10 = 0.48", "4.8", ["0.048", "48", "4.08"],
                   "Use the inverse: 0.48 × 10 = <b>4.8</b>. Check: 4.8 ÷ 10 = 0.48. 0.048 divides instead of multiplying."))
    # 18 equivalent calculation
    assert Dm("4.5") * 100 == 45 * 10 and Dm("4.5") * 10 != 450 and 45 * 100 != 450 and Dm("0.45") * 10 != 450
    its.append(mcq("Which calculation has the same answer as <b>4.5 × 100</b>?", "45 × 10",
                   ["4.5 × 10", "45 × 100", "0.45 × 10"],
                   "4.5 × 100 = 450. 4.5 × 10 = 45, and 45 × 10 = 450. So <b>45 × 10</b> gives the same answer.", same_ok=True))
    # 19
    assert Dm("0.047") * 1000 == 47
    its.append(mcq("Which number is <b>1000 times</b> as large as 0.047?", "47", ["4.7", "470", "0.047000"],
                   "1000 times as large means × 1000: every digit moves 3 places to the left. 0.047 × 1000 = <b>47</b>. "
                   "0.047000 only adds zeros, so it is still 0.047."))
    order = [0, 1, 2, 3, 6, 7, 10, 13, 4, 5, 8, 9, 11, 12, 14, 16, 15, 17, 18, 19]
    return {"title": "× and ÷ by 10, 100 and 1000", "items": reorder(its, order)}


# ============================================================ set 2: multiples of powers of 10
def set_multiples():
    its = []
    for a, b, w in [
        ("0.3", 40, ["1.2", "120", "0.12"]),
        ("0.2", 30, ["0.6", "60", "0.06"]),
        ("0.5", 60, ["3", "300", "0.3"]),
        ("1.2", 30, ["3.6", "360", "0.36"]),
        ("0.04", 200, ["0.8", "80", "0.08"]),
        ("0.9", 70, ["6.3", "630", "0.63"]),
        ("0.25", 80, ["2", "200", "0.2"]),
        ("1.6", 50, ["8", "800", "0.8"]),
        ("0.07", 3000, ["21", "2100", "0.21"]),
        ("2.5", 400, ["10", "10" + NB + "000", "100"]),
        ("0.12", 5000, ["60", "6000", "0.6"]),
    ]:
        e = split_e(a, b, "×")
        r = Dm(a) * b
        part = None
        for x in w:
            if Dm(x.replace(NB, "")) == r / 10 ** (len(str(b)) - len(str(b).rstrip("0"))):
                part = x
        assert part is not None, (a, b)
        e += " %s forgets to multiply by %s." % (part, P10(len(str(b)) - len(str(b).rstrip("0"))))
        its.append(mult_q(a, b, w, e))
    for a, b, w in [
        ("2.4", 20, ["1.2", "0.012", "12"]),
        ("0.8", 20, ["0.4", "0.004", "4"]),
        ("3.6", 40, ["0.9", "0.009", "9"]),
        ("1.5", 30, ["0.5", "0.005", "5"]),
        ("7.2", 90, ["0.8", "0.008", "8"]),
        ("4.8", 200, ["2.4", "0.24", "0.0024"]),
        ("56", 700, ["8", "0.8", "0.008"]),
    ]:
        e = split_e(a, b, "÷")
        k = len(str(b)) - len(str(b).rstrip("0"))
        m = Dm(b) / 10 ** k
        e += " %s only divides by %d." % (N(Dm(a) / m), int(m))
        assert N(Dm(a) / m) in w
        its.append(div_q(a, b, w, e))
    # missing number
    assert Dm("0.6") * 30 == 18
    its.append(mcq("0.6 × ? = 18", "30", ["3", "300", "17.4"],
                   "0.6 × 3 = 1.8, and 1.8 × 10 = 18. So 0.6 × <b>30</b> = 18. 0.6 × 3 is only 1.8. "
                   "17.4 is 18 − 0.6, which is subtraction."))
    # same answer
    assert Dm("0.4") * 300 == 4 * 30 == 120
    assert len({Dm(4) * 300, Dm("0.4") * 30, Dm(40) * 300}) == 3 and 120 not in {4 * 300, 12, 40 * 300}
    its.append(mcq("Which calculation has the same answer as <b>0.4 × 300</b>?", "4 × 30",
                   ["4 × 300", "0.4 × 30", "40 × 300"],
                   "0.4 × 300 = 0.4 × 3 × 100 = 1.2 × 100 = 120. Make one number 10 times bigger and the other 10 times "
                   "smaller: 4 × 30 = 120. So <b>4 × 30</b>.", same_ok=True))
    order = [0, 1, 2, 11, 12, 3, 4, 13, 14, 5, 6, 15, 7, 16, 8, 17, 9, 10, 18, 19]
    return {"title": "Multiples of 10, 100 and 1000", "items": reorder(its, order)}


# ============================================================ set 3: converting units
UNAME = {"kg": "Kilograms", "g": "Grams", "m": "Metres", "cm": "Centimetres", "mm": "Millimetres", "km": "Kilometres",
         "L": "Litres", "mL": "Millilitres"}
UNITS = {("kg", "g"): 3, ("m", "cm"): 2, ("cm", "mm"): 1, ("m", "mm"): 3, ("km", "m"): 3, ("L", "mL"): 3}


def conv_q(x, u1, u2, wrong, note=""):
    if (u1, u2) in UNITS:
        k = UNITS[(u1, u2)]
        op = "×"
        r = Dm(x) * 10 ** k
        rel = "1 %s = %s %s" % (u1, P10(k), u2)
        why = "%s are smaller units, so there are more of them: <b>× %s</b>." % (UNAME[u2], P10(k))
    else:
        k = UNITS[(u2, u1)]
        op = "÷"
        r = Dm(x) / 10 ** k
        rel = "1 %s = %s %s" % (u2, P10(k), u1)
        why = "%s are bigger units, so there are fewer of them: <b>÷ %s</b>." % (UNAME[u2], P10(k))
    e = "%s. %s %s %s %s = <b>%s %s</b>." % (rel, why, N(x), op, P10(k), N(r), u2)
    if note:
        e += " " + note
    return mcq("%s %s = ? %s" % (N(x), u1, u2), "%s %s" % (N(r), u2), ["%s %s" % (w, u2) for w in wrong], e)


def set_convert():
    its = []
    its.append(conv_q("3.5", "kg", "g", ["350", "35", "35" + NB + "000"], "350 g moves the digits only 2 places."))
    its.append(conv_q("2.4", "m", "cm", ["24", "2400", "2.40"], "2.40 cm just adds a zero, so it is still 2.4."))
    its.append(conv_q("0.75", "L", "mL", ["75", "7500", "7.5"], "75 mL multiplies by 100, but 1 L is 1000 mL."))
    its.append(conv_q("6.2", "cm", "mm", ["620", "0.62", "6.20"], "1 cm is only 10 mm."))
    its.append(conv_q("1.25", "km", "m", ["125", "12" + NB + "500", "0.00125"], "0.00125 divides instead of multiplying."))
    its.append(conv_q("450", "g", "kg", ["4.5", "45", "450" + NB + "000"], "450" + NB + "000 multiplies instead of dividing."))
    its.append(conv_q("85", "cm", "m", ["8.5", "8500", "0.085"], "8.5 m divides by 10, but 1 m is 100 cm."))
    its.append(conv_q("2500", "mL", "L", ["25", "0.25", "250"], "25 L divides by 100, but 1 L is 1000 mL."))
    its.append(conv_q("36", "mm", "cm", ["0.36", "360", "0.036"], "1 cm is 10 mm, so divide by 10, not 100."))
    its.append(conv_q("750", "m", "km", ["7.5", "0.075", "750" + NB + "000"], "7.5 km divides by 100, but 1 km is 1000 m."))
    its.append(conv_q("0.08", "kg", "g", ["8", "800", "0.0008"], "8 g multiplies by 100, but 1 kg is 1000 g."))
    its.append(conv_q("3.05", "m", "cm", ["350", "30.5", "3050"], "350 cm drops the 0 that holds the tenths place."))
    its.append(conv_q("4.2", "m", "mm", ["420", "42", "42" + NB + "000"], "1 m = 100 cm = 1000 mm."))
    its.append(conv_q("9", "mL", "L", ["0.09", "0.9", "9000"], "0.09 L moves the digit only 2 places."))
    its.append(conv_q("0.035", "km", "m", ["3.5", "350", "0.35"], "3.5 m multiplies by 100, but 1 km is 1000 m."))
    # money
    assert Dm("4.35") * 100 == 435
    its.append(mcq("$4.35 = ? cents", "435c", ["43.5c", "4350c", "4.35c"],
                   "$1 = 100c, so × 100: every digit moves 2 places to the left. 4.35 × 100 = 435, so $4.35 = <b>435c</b>. "
                   "4.35c only changes the unit."))
    assert Dm(260) / 100 == Dm("2.6")
    its.append(mcq("260c = ?", "$2.60", ["$26.00", "$0.26", "$2600"],
                   "100c = $1, so ÷ 100: 260 ÷ 100 = 2.6. Write money with 2 decimal places: <b>$2.60</b>. "
                   "$26.00 divides by 10 only."))
    # mixed units and equal lengths
    assert Dm("0.6") * 1000 == 600 and Dm(60) / 1000 != Dm("0.6") and Dm(6) / 100 != Dm("0.6") and Dm(600) / 100 != Dm("0.6")
    its.append(mcq("Which length is equal to <b>0.6 m</b>?", "600 mm", ["60 mm", "6 cm", "600 cm"],
                   "1 m = 1000 mm, so 0.6 m = 0.6 × 1000 = <b>600 mm</b>. (It is also 60 cm.) 600 cm would be 6 m.",
                   same_ok=True))
    assert 3 + Dm(250) / 1000 == Dm("3.25")
    its.append(mcq("Write <b>3 kg 250 g</b> in kilograms.", "3.25 kg", ["3.025 kg", "32.5 kg", "325 kg"],
                   "250 g = 250 ÷ 1000 = 0.25 kg. So 3 kg 250 g = 3 + 0.25 = <b>3.25 kg</b>. "
                   "3.025 kg would be 3 kg 25 g."))
    assert 4 + Dm(5) / 100 == Dm("4.05")
    its.append(mcq("Write <b>4 m 5 cm</b> in metres.", "4.05 m", ["4.5 m", "4.005 m", "45 m"],
                   "5 cm = 5 ÷ 100 = 0.05 m. So 4 m 5 cm = <b>4.05 m</b>. 4.5 m would be 4 m 50 cm."))
    order = [0, 1, 2, 3, 4, 15, 5, 6, 7, 8, 16, 9, 10, 11, 12, 13, 14, 17, 18, 19]
    return {"title": "Converting units and money", "items": reorder(its, order)}


# ============================================================ set 4: estimation checks
def set_estimate():
    its = []
    its.append(mcq("Mia says 4.8 × 10 = 4.80. Is she right?", "No, it is 48",
                   ["Yes, she is right", "No, it is 480", "No, it is 0.48"],
                   "4.80 has the same value as 4.8, so adding a zero did not multiply. Estimate: 5 × 10 = 50. "
                   "The digits move 1 place to the left: <b>4.8 × 10 = 48</b>.", same_ok=True))
    its.append(mcq("Leo says 36.5 ÷ 100 = 3650. What did he do wrong?", "He moved the digits the wrong way",
                   ["He moved the digits too few places", "He forgot to add a zero", "Nothing, he is right"],
                   "Dividing makes the number smaller, but 3650 is bigger than 36.5. <b>He moved the digits the wrong way</b>. "
                   "36.5 ÷ 100 = 0.365.", same_ok=True))
    # best estimates
    for q, right, w, e in [
        ("3.9 × 20", "80", ["8", "800", "60"],
         "Round 3.9 to 4. 4 × 20 = <b>80</b>. 60 rounds 3.9 down to 3, but 3.9 is much closer to 4."),
        ("6.1 × 300", "1800", ["180", "18" + NB + "000", "2100"],
         "Round 6.1 to 6. 6 × 300 = 6 × 3 × 100 = <b>1800</b>."),
        ("0.48 × 50", "25", ["2.5", "250", "20"],
         "Round 0.48 to 0.5. 0.5 × 50 = <b>25</b> (half of 50). 20 uses 0.4, but 0.48 is closer to 0.5."),
        ("59.7 ÷ 20", "3", ["30", "0.3", "1200"],
         "Round 59.7 to 60. 60 ÷ 20 = <b>3</b>. 1200 multiplies instead of dividing."),
        ("8.1 ÷ 40", "0.2", ["2", "0.02", "320"],
         "Round 8.1 to 8. 8 ÷ 4 = 2, and 2 ÷ 10 = <b>0.2</b>. So 8 ÷ 40 = 0.2."),
    ]:
        its.append(mcq("Which is the best estimate for <b>%s</b>?" % q, right, w, e))
    assert abs(Dm("3.9") * 20 - 80) <= 2 and abs(Dm("6.1") * 300 - 1800) < 40
    assert abs(Dm("0.48") * 50 - 25) <= 1 and abs(Dm("59.7") / 20 - 3) < Dm("0.1") and abs(Dm("8.1") / 40 - Dm("0.2")) < Dm("0.01")
    # reasonable answers (exact answer, chosen by estimating)
    for a, op, b, est, w in [
        ("2.9", "×", 40, "3 × 40 = 120", ["11.6", "1160", "1.16"]),
        ("7.8", "×", 30, "8 × 30 = 240", ["23.4", "2340", "2.34"]),
        ("9.6", "÷", 30, "9 ÷ 30 = 0.3", ["3.2", "0.032", "32"]),
        ("15.6", "÷", 40, "16 ÷ 40 = 0.4", ["3.9", "0.039", "39"]),
    ]:
        r = Dm(a) * b if op == "×" else Dm(a) / b
        assert op == "×" or r * b == Dm(a)
        its.append(mcq("Use an estimate to choose the correct answer: <b>%s %s %s</b> = ?" % (a, op, N(b)), N(r), w,
                       "Estimate: %s. Only <b>%s</b> is close to the estimate. The other answers have the digits in the "
                       "wrong places." % (est, N(r))))
    assert Dm("2.31") * 100 == 231
    its.append(mcq("Kai worked out 2.31 × 100 = 23.1. Which is true?", "He is wrong: the answer is about 200",
                   ["He is right", "He is wrong: the answer is about 2", "He is wrong: the answer is about 2000"],
                   "Estimate: 2 × 100 = 200. 23.1 is far too small, because the digits moved only 1 place. "
                   "2.31 × 100 = 231, which is <b>about 200</b>.", same_ok=True))
    vals = {"0.35 × 40": Dm("0.35") * 40, "3.5 × 40": Dm("3.5") * 40, "0.35 × 4": Dm("0.35") * 4, "35 × 40": Dm(35) * 40}
    assert [k for k, v in vals.items() if 10 < v < 20] == ["0.35 × 40"]
    its.append(mcq("Which calculation has an answer <b>between 10 and 20</b>?", "0.35 × 40",
                   ["3.5 × 40", "0.35 × 4", "35 × 40"],
                   "Estimate each one: 0.35 × 40 ≈ 0.35 × 4 × 10 = 1.4 × 10 = 14. 3.5 × 40 = 140, 0.35 × 4 = 1.4 and "
                   "35 × 40 = 1400. So <b>0.35 × 40</b>.", same_ok=True))
    vals = {"4.5 ÷ 50": Dm("4.5") / 50, "45 ÷ 5": Dm(45) / 5, "0.45 × 50": Dm("0.45") * 50, "4.5 × 10": Dm("4.5") * 10}
    assert [k for k, v in vals.items() if v < 1] == ["4.5 ÷ 50"]
    its.append(mcq("Which calculation has an answer <b>less than 1</b>?", "4.5 ÷ 50",
                   ["45 ÷ 5", "0.45 × 50", "4.5 × 10"],
                   "4.5 is less than 50, so 4.5 ÷ 50 is less than 1: 4.5 ÷ 5 = 0.9 and 0.9 ÷ 10 = 0.09. "
                   "The others are 9, 22.5 and 45. So <b>4.5 ÷ 50</b>.", same_ok=True))
    vals = {"0.6 × 300": Dm("0.6") * 300, "2.4 × 50": Dm("2.4") * 50, "17 × 10": Dm(170), "900 ÷ 10": Dm(90)}
    assert max(vals, key=vals.get) == "0.6 × 300"
    its.append(mcq("Which calculation has the <b>greatest</b> answer?", "0.6 × 300",
                   ["2.4 × 50", "17 × 10", "900 ÷ 10"],
                   "0.6 × 300 = 0.6 × 3 × 100 = 180. 2.4 × 50 = 120, 17 × 10 = 170 and 900 ÷ 10 = 90. "
                   "So <b>0.6 × 300</b> is the greatest.", same_ok=True))
    assert Dm("5.06") * 1000 == 5060
    its.append(mcq("5.06 × 1000 is closest to which number?", "5000", ["50", "500", "50" + NB + "000"],
                   "5.06 is a little more than 5, and 5 × 1000 = <b>5000</b>. (5.06 × 1000 = 5060.)"))
    assert Dm("0.38") / 10 == Dm("0.038")
    its.append(mcq("0.38 ÷ 10 is closest to which number?", "0.04", ["0.4", "4", "0.004"],
                   "0.38 is about 0.4, and 0.4 ÷ 10 = <b>0.04</b>. (0.38 ÷ 10 = 0.038.)"))
    assert Dm(32) / 40 == Dm("0.8")
    its.append(mcq("Grace estimates 31.8 ÷ 40 by working out 32 ÷ 40. What is her estimate?", "0.8",
                   ["8", "0.08", "1280"],
                   "32 ÷ 4 = 8, and 8 ÷ 10 = <b>0.8</b>. 1280 multiplies instead of dividing."))
    assert Dm("0.7") * 60 == 42
    its.append(mcq("Ethan says 0.7 × 60 = 4.2. Use the fact 7 × 6 = 42 to check. What is the correct answer?", "42",
                   ["4.2", "420", "0.42"],
                   "0.7 × 6 = 4.2, then × 10 = 42. Ethan forgot to multiply by 10. Estimate: 0.7 is a bit less than 1, and "
                   "1 × 60 = 60, so the answer should be a bit less than 60, not about 4. 0.7 × 60 = <b>42</b>."))
    assert Dm("3.6") / 40 == Dm("0.09")
    its.append(mcq("Charlotte says 3.6 ÷ 40 = 0.9. What is the correct answer?", "0.09", ["0.9", "9", "0.009"],
                   "3.6 ÷ 4 = 0.9, then ÷ 10 = 0.09. Charlotte forgot to divide by 10. Estimate: 4 ÷ 40 = 0.1, so the "
                   "answer is about 0.1. 3.6 ÷ 40 = <b>0.09</b>."))
    order = [0, 1, 2, 3, 4, 5, 6, 15, 16, 7, 8, 9, 10, 11, 17, 18, 19, 12, 13, 14]
    return {"title": "Estimate to check answers", "items": reorder(its, order)}


# ============================================================ set 5: word problems
def set_problems():
    its = []
    T = Dm("2.45") * 100
    its.append(mcq("The school canteen buys 100 bags of popcorn at $2.45 each. What is the total cost?", M(T),
                   ["$24.50", "$2450", "$24" + NB + "500"],
                   "2.45 × 100: every digit moves 2 places to the left. 2.45 × 100 = 245, so the total is <b>%s</b>. "
                   "$24.50 is the cost of only 10 bags." % M(T)))
    T = Dm("0.1") * 1000
    its.append(mcq("A sheet of paper is about 0.1 mm thick. How thick is a stack of 1000 sheets?", N(T) + " mm",
                   ["10 mm", "1000 mm", "0.0001 mm"],
                   "0.1 × 1000 = <b>100 mm</b> (10 cm). 0.0001 mm divides instead of multiplying, but 1000 sheets "
                   "must be thicker than 1 sheet."))
    T = Dm(450) / 1000
    its.append(mcq("A box of 1000 paper clips has a mass of 450 g. What is the mass of one paper clip?", N(T) + " g",
                   ["4.5 g", "0.045 g", "450" + NB + "000 g"],
                   "450 ÷ 1000: every digit moves 3 places to the right. 450 ÷ 1000 = <b>0.45 g</b>."))
    T = Dm("3.5") * 100
    its.append(mcq("At the sausage sizzle, 100 sausages in bread are sold for $3.50 each. How much money is collected?",
                   M(T), ["$35", "$3500", "$103.50"],
                   "3.5 × 100 = <b>%s</b>. $103.50 adds 100 instead of multiplying." % M(T)))
    T = Dm("2.85") * 10
    its.append(mcq("A teacher buys 10 boxes of tissues at $2.85 each. What is the total cost?", M(T),
                   ["$285", "$12.85", "$2850"],
                   "2.85 × 10: every digit moves 1 place to the left. The total is <b>%s</b>. $12.85 adds 10 instead of "
                   "multiplying." % M(T)))
    T = Dm(65) / 10
    its.append(mcq("10 students share the cost of a $65 gift for their teacher equally. How much does each student pay?",
                   M(T), ["$650", "$0.65", "$6.05"],
                   "65 ÷ 10 = 6.5, so each student pays <b>%s</b>. $6.05 puts the 5 in the wrong place." % M(T)))
    T = Dm("2.5") * 1000
    its.append(mcq("The school cross-country course is 2.5 km long. How many metres is that?", N(T) + " m",
                   ["250 m", "25 m", "25" + NB + "000 m"],
                   "1 km = 1000 m, so 2.5 × 1000 = <b>2500 m</b>. 250 m multiplies by 100 only."))
    T = Dm("0.35") * 20
    its.append(mcq("One lap of the school oval is 0.35 km. Isla runs 20 laps for the fun run. How far does she run?",
                   N(T) + " km", ["0.7 km", "70 km", "0.07 km"],
                   "0.35 × 2 = 0.7, then 0.7 × 10 = <b>7 km</b>. 0.7 km forgets the × 10."))
    T = Dm("0.04") * 100
    its.append(mcq("A leaking tap drips 0.04 L of water every minute. How much water drips in 100 minutes?", N(T) + " L",
                   ["0.4 L", "40 L", "0.0004 L"],
                   "0.04 × 100: every digit moves 2 places to the left. 0.04 × 100 = <b>4 L</b>."))
    T = Dm("0.18") * 1000
    its.append(mcq("A pencil is 0.18 m long. How long would 1000 pencils be if they were laid end to end?", N(T) + " m",
                   ["18 m", "1800 m", "1.8 m"],
                   "0.18 × 1000: every digit moves 3 places to the left. 0.18 × 1000 = <b>180 m</b>."))
    T = Dm("1.95") * 40
    its.append(mcq("Petrol costs $1.95 per litre. Mum buys 40 L. How much does she pay?", M(T),
                   ["$7.80", "$780", "$0.78"],
                   "1.95 × 4 = 7.8, then 7.8 × 10 = 78. She pays <b>%s</b>. Check with an estimate: $2 × 40 = $80." % M(T)))
    T = Dm("0.5") * 30
    its.append(mcq("A koala eats about 0.5 kg of eucalyptus leaves a day. About how much does it eat in 30 days?",
                   N(T) + " kg", ["1.5 kg", "150 kg", "0.15 kg"],
                   "0.5 × 3 = 1.5, then 1.5 × 10 = <b>15 kg</b>. 1.5 kg forgets the × 10."))
    T = Dm("4.8") / 20
    its.append(mcq("A 4.8 m length of ribbon is cut into 20 equal pieces. How long is each piece?", N(T) + " m",
                   ["2.4 m", "0.024 m", "96 m"],
                   "4.8 ÷ 2 = 2.4, then 2.4 ÷ 10 = <b>0.24 m</b> (24 cm). 2.4 m forgets the ÷ 10."))
    T = Dm("6.3") / 70
    its.append(mcq("A 6.3 kg bag of potting mix is shared equally between 70 pots in the school garden. "
                   "How much potting mix goes in each pot?", N(T) + " kg", ["0.9 kg", "0.009 kg", "9 kg"],
                   "6.3 ÷ 7 = 0.9, then 0.9 ÷ 10 = <b>0.09 kg</b> (90 g). 0.9 kg forgets the ÷ 10."))
    T = Dm("0.1") * 1000
    its.append(mcq("Harper’s class collects 1000 cans for recycling. Each can is worth 10c at the recycling depot. "
                   "How much money do they get?", M(T), ["$10", "$1000", "$10" + NB + "000"],
                   "10c = $0.10. 0.1 × 1000 = 100, so they get <b>%s</b>. (1000 × 10c = 10" % M(T) + NB + "000c = $100.)"))
    T = Dm("0.75") * 100
    its.append(mcq("A water bottle holds 0.75 L. How many litres do 100 full bottles hold?", N(T) + " L",
                   ["7.5 L", "750 L", "0.0075 L"],
                   "0.75 × 100: every digit moves 2 places to the left. 0.75 × 100 = <b>75 L</b>."))
    T = Dm("2.4") * 30
    its.append(mcq("Kai’s dad buys 30 m of garden hose at $2.40 per metre. What is the total cost?", M(T),
                   ["$7.20", "$720", "$0.72"],
                   "2.4 × 3 = 7.2, then 7.2 × 10 = 72. The total is <b>%s</b>. Estimate: $2 × 30 = $60, so $7.20 is far "
                   "too small." % M(T)))
    T = Dm(4) / 100
    assert T == Dm("0.04")
    its.append(mcq("A packet of 100 stickers costs $4. How much is one sticker?", "4c", ["40c", "0.4c", "$4"],
                   "$4 ÷ 100 = $0.04 = <b>4c</b>. 40c divides by 10 only."))
    its.append(mcq("Ava buys 20 books at $9.95 each for the class library. Which is the best estimate of the total?",
                   "$200", ["$20", "$2000", "$180"],
                   "Round $9.95 to $10. $10 × 20 = <b>$200</b>. $180 rounds $9.95 down to $9."))
    assert abs(Dm("9.95") * 20 - 200) <= 1
    T = Dm("8.5") * 100 + Dm("24.9") * 10
    assert T == 1099
    its.append(mcq("The school buys 100 recorders at $8.50 each and 10 music stands at $24.90 each. "
                   "What is the total cost?", M(T), ["$874.90", "$334", "$8749"],
                   "Recorders: 8.5 × 100 = $850. Music stands: 24.9 × 10 = $249. Total: 850 + 249 = <b>%s</b>. "
                   "$874.90 forgets to multiply the music stands by 10." % M(T)))
    assert Dm(850) + Dm("24.9") == Dm("874.9") and Dm(85) + 249 == 334 and Dm(8500) + 249 == 8749
    order = [1, 0, 2, 8, 4, 3, 5, 6, 9, 15, 7, 11, 17, 12, 13, 10, 16, 14, 18, 19]
    return {"title": "Word problems with powers of 10", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    f1 = pv_move("2.4", "×", 1)
    f2 = pv_move("3.6", "÷", 2)
    return (
        "<h2>The digits move, the decimal point stays still</h2>"
        "<p>When you multiply by 10, 100 or 1000, every digit moves to the <b>left</b>. "
        "When you divide, every digit moves to the <b>right</b>. Count the zeros to know how far.</p>"
        + table(["Calculation", "Every digit moves"], [
            ["× 10 or ÷ 10", "1 place"], ["× 100 or ÷ 100", "2 places"], ["× 1000 or ÷ 1000", "3 places"]])
        + "<figure class='sn-fig'>" + f1 +
        "<figcaption>2.4 × 10: the 2 moves from the ones to the tens and the 4 from the tenths to the ones. "
        "2.4 × 10 = 24, not 2.40.</figcaption></figure>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>3.6 ÷ 100: every digit moves 2 places to the right. The grey zeros hold the empty places. "
        "3.6 ÷ 100 = 0.036.</figcaption></figure>"
        "<h2>Multiples of 10, 100 and 1000</h2>"
        "<p>Split the multiple into a multiplication fact and a power of 10. 40 = 4 × 10, 200 = 2 × 100.</p>"
        + ex("Example 1", "0.3 × 40", "0.3 × 4 = 1.2. Then 1.2 × 10 = 12.", "12")
        + ex("Example 2", "2.4 ÷ 20", "2.4 ÷ 2 = 1.2. Then 1.2 ÷ 10 = 0.12.", "0.12")
        + "<h2>Converting units</h2>"
        "<p>To change to a <b>smaller</b> unit, multiply. To change to a <b>bigger</b> unit, divide.</p>"
        + table(["Fact", "Example"], [
            ["1 kg = 1000 g", "3.5 kg = 3.5 × 1000 = 3500 g"],
            ["1 m = 100 cm", "85 cm = 85 ÷ 100 = 0.85 m"],
            ["1 L = 1000 mL", "0.75 L = 750 mL"],
            ["$1 = 100c", "$4.35 = 435c"],
        ])
        + "<h2>Estimate to check</h2>"
        "<p>Round to an easy number first. 3.9 × 20 is about 4 × 20 = 80, so 78 is reasonable but 7.8 or 780 is not.</p>"
        + ex("Example 3", "The canteen buys 100 bags of popcorn at $2.45 each. What is the total cost?",
             "2.45 × 100: every digit moves 2 places to the left. Estimate: about $2 × 100 = $200.", "$245")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["2.4 × 10 = 2.40 (“just add a zero”)", "2.40 is still 2.4. Move the digits 1 place to the left: 24"],
            ["45.2 ÷ 100 = 4520", "Dividing makes the number smaller: move the digits to the right, 0.452"],
            ["0.3 × 40 = 1.2", "Do both steps: 0.3 × 4 = 1.2, then × 10 = 12"],
            ["3.05 × 100 = 350", "Keep the 0 that holds a place: 305"],
            ["0.75 L = 75 mL", "1 L = 1000 mL, so × 1000: 750 mL"],
        ])
    )


FAQ = [
    {"q": "What do Year 6 students learn about multiplying and dividing decimals by powers of 10?",
     "a": "In Year 6 (AC9M6N06) students multiply and divide decimals by 10, 100, 1000 and their multiples, such as 0.3 × 40, without a calculator, and use estimation and rounding to check that answers are reasonable."},
    {"q": "Why is “just add a zero” wrong when you multiply a decimal by 10?",
     "a": "Adding a zero to the end of a decimal does not change its value: 2.40 is the same as 2.4. The digits must move 1 place to the left, so 2.4 × 10 = 24."},
    {"q": "How do you multiply a decimal by a multiple of 10, like 0.3 × 40?",
     "a": "Split 40 into 4 × 10. Work out 0.3 × 4 = 1.2, then multiply by 10 to get 12. Divide the same way: 2.4 ÷ 20 = 2.4 ÷ 2 ÷ 10 = 0.12."},
    {"q": "How do you check a decimal answer is reasonable?",
     "a": "Round the numbers to make an easy estimate. For 2.9 × 40, estimate 3 × 40 = 120, so 116 is reasonable but 11.6 or 1160 is not."},
]


def mark_large(u, pattern):
    """Tag place value charts so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every plain 'a × b = ?' / 'a ÷ b = ?' question with Decimal."""
    rx = re.compile(r"^([\d .]+) ([×÷]) ([\d ]+) = \?$")
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
    rnd = random.Random(6806)
    sets = [set_p10(), set_multiples(), set_convert(), set_estimate(), set_problems()]
    assert check_answers(sets) >= 25
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
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "multiplying-and-dividing-decimals-by-powers-of-10",
        "sort": 6, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing Decimals by Powers of 10",
        "seo_title": "Year 6 Multiplying and Dividing Decimals by 10, 100 and 1000 Worksheets (Free, Answer Key)",
        "short_title": "× and ÷ decimals by powers of 10",
        "domain": "Number",
        "standard_code": "AC9M6N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Multiply and divide decimals by multiples of powers of 10 without a calculator, applying knowledge of place value and proficiency with multiplication facts; using estimation and rounding to check the reasonableness of answers",
        "meta_desc": "Free Year 6 maths worksheets for the Australian Curriculum (AC9M6N06): multiply and divide decimals by 10, 100, 1000 and their multiples, convert units, and estimate to check answers. 100 questions with an answer key.",
        "key_big": "The digits move, the decimal point stays still: left to multiply, right to divide.",
        "key_sub": "1 place for 10, 2 for 100, 3 for 1000. For multiples, split them: 0.3 × 40 = 0.3 × 4 × 10 = 12. 2.4 × 10 is 24, not 2.40.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "place value chart")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
