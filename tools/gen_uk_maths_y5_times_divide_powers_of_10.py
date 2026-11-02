# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Multiply and divide by 10, 100 and 1,000 (National Curriculum in England, Year 5: Multiplication and division)
  python3 tools/gen_uk_maths_y5_times_divide_powers_of_10.py
Whole numbers and decimals × and ÷ by 10, 100 and 1,000: the digits move, the decimal point stays still.
Place value charts with arrows show the move. Missing numbers use the inverse. Word problems use pounds and pence
and metric measures. All arithmetic uses decimal.Decimal (never float), so every answer and mistake is exact.
British English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written to fill empty places
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
MINUS = "−"
PLACE = {5: "hundred thousands", 4: "ten thousands", 3: "thousands", 2: "hundreds", 1: "tens", 0: "ones",
         -1: "tenths", -2: "hundredths", -3: "thousandths"}
SHORT = {5: "HTh", 4: "TTh", 3: "Th", 2: "H", 1: "T", 0: "O", -1: "Tth", -2: "Hth", -3: "Thth"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text without extra zeros, commas from 1,000: Dm('2800.0') -> '2,800'."""
    return format(Dm(str(x).replace(",", "")).normalize(), ",f")


def M(x):
    """Money in pounds: £5.40, £1,250.00."""
    return "£" + format(Dm(x).quantize(Dm("0.01")), ",f")


def P10(k):
    return N(10 ** k)


def calc(x, op, k):
    x = Dm(str(x).replace(",", ""))
    return x * 10 ** k if op == "×" else x / 10 ** k


VAL = re.compile(r"^(£)?([\d,]*\.?\d+)(p)?(.*)$")


def val(c):
    """(value, unit) of a choice: '£0.53' and '53p' are the same value. None if it is not one number."""
    m = VAL.match(c)
    if not m:
        return None
    v = Dm(m.group(2).replace(",", ""))
    if m.group(1):
        return (v, "£")
    if m.group(3):
        return (v / 100, "£")
    return (v, m.group(4).strip())


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    """4 choices: correct + 3 wrong answers (all different values). Positions are set by balance()."""
    c = [str(correct)] + [str(w) for w in wrong]
    assert len(c) == 4 and len(set(c)) == 4, (q, c)
    vs = [val(x) for x in c if val(x) is not None]
    assert len(set(vs)) == len(vs), (q, c)
    return {"q": q, "c": c, "a": 0, "e": e}


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
    """'4,500' -> {3: '4', 2: '5', 1: '0', 0: '0'}; '0.032' -> {0: '0', -1: '0', -2: '3', -3: '2'}."""
    w, _, f = s.replace(",", "").partition(".")
    d = {}
    for j, ch in enumerate(w):
        d[len(w) - 1 - j] = ch
    for j, ch in enumerate(f):
        d[-(j + 1)] = ch
    return d


def pv_move(x, op, k, hi=None, show_answer=True, CW=62):
    """Two-row place value chart: x on top, the answer below, arrows from each digit to its new place.
    Zeros that only fill empty places are grey. hi: place of a digit in x; it is red in the answer row."""
    r = N(calc(x, op, k))
    top, bot = split_digits(N(x)), split_digits(r)
    shift = k if op == "×" else -k
    moved = {p + shift for p in top}
    hi_place = None if hi is None else hi + shift
    has_pt = min(min(top), min(bot)) < 0
    cols = list(range(max(max(top), max(bot)), min(min(top), min(bot), 0) - 1, -1))
    PW = 16 if has_pt else 0
    HEAD, ROW, BAND, LW = 30, 44, 46, 74
    x0, y0 = 4, 4
    W = 2 * x0 + LW + len(cols) * CW + PW
    gw = len(cols) * CW + PW
    yt = y0 + HEAD               # top row
    yb = yt + ROW + BAND         # bottom row
    H = yb + ROW + y0
    xs, xx = {}, x0 + LW
    for p in cols:
        xs[p] = xx
        xx += CW + (PW if p == 0 else 0)
    cx = {p: xs[p] + CW / 2.0 for p in cols}
    gy = y0 + HEAD + ROW + BAND + ROW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, gw, gy - y0, GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, gw, HEAD, HEADFILL)]
    for p in cols:
        if p != cols[0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], gy, GREEN))
        o.append(text(cx[p], y0 + 21, SHORT[p], 16, col=GREEN))
    if has_pt:
        o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (xs[0] + CW + PW, y0, xs[0] + CW + PW, gy, GREEN))
    for yy in (yt, yt + ROW, yb):
        o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (x0 + LW, yy, x0 + LW + gw, yy, GREEN, 2 if yy == yt else 1))
    # digits
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
    # arrows
    y1, y2 = yt + ROW + 5, yb - 5
    for p in top:
        if p + shift not in bot:      # a 0 that is not needed after the point (450 ÷ 100 = 4.5)
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
def p10_e(x, op, k, note=""):
    r = calc(x, op, k)
    e = ("%s %s %s: every digit moves <b>%s to the %s</b>. The decimal point stays still."
         % (N(x), op, P10(k), "1 place" if k == 1 else "%d places" % k, "left" if op == "×" else "right"))
    if op == "×" and Dm(N(x).replace(",", "")) == int(Dm(N(x).replace(",", ""))) or op == "×" and len(N(x).partition(".")[2]) < k:
        e += " Write 0 in the empty places up to the ones."
    elif op == "÷" and r < 1:
        e += " Write 0 in the empty places, starting with the ones."
    e += " %s %s %s = <b>%s</b>." % (N(x), op, P10(k), N(r))
    if note:
        e += " " + note
    return e


def p10(its, x, op, k, wrong, note=""):
    its.append(mcq("%s %s %s = ?" % (N(x), op, P10(k)), N(calc(x, op, k)), wrong, p10_e(x, op, k, note)))


def which_calc(its, x, op, k, wrong):
    r = N(calc(x, op, k))
    e = ("Every digit moved %s to the <b>%s</b>, so it is %s %s. <b>%s %s %s</b> = %s."
         % ("1 place" if k == 1 else "%d places" % k, "left" if op == "×" else "right",
            op, P10(k), N(x), op, P10(k), r))
    its.append(mcq(fig(pv_move(x, op, k)) + "Which calculation does the chart show?",
                   "%s %s %s" % (N(x), op, P10(k)), wrong, e))


def red_digit(its, x, op, k, src, wrong):
    r = N(calc(x, op, k))
    shift = k if op == "×" else -k
    p = src + shift
    dg = split_digits(r)[p]
    right = "%s %s" % (dg, PLACE[p])
    e = ("%s %s %s = %s. Every digit moved %s to the %s, so the %s is now in the <b>%s</b> place. Its value is <b>%s</b>."
         % (N(x), op, P10(k), r, "1 place" if k == 1 else "%d places" % k, "left" if op == "×" else "right",
            dg, PLACE[p], right))
    its.append(mcq(fig(pv_move(x, op, k, hi=src)) +
                   "The chart shows %s %s %s = %s. What is the value of the red digit?" % (N(x), op, P10(k), r),
                   right, wrong, e))


def add0(w, x):
    return "(%s is still %s: adding zeros does not multiply.)" % (w, x)


# ============================================================ set 1: whole numbers × 10, 100, 1,000
def set_whole_times():
    its = []
    p10(its, "45", "×", 1, ["4,500", "55", "405"], "(55 adds 10, it does not multiply.)")
    p10(its, "72", "×", 2, ["720", "72,000", "172"])
    p10(its, "9", "×", 3, ["900", "90,000", "1,009"])
    p10(its, "130", "×", 1, ["13,000", "140", "13"], "(13 is 130 ÷ 10.)")
    p10(its, "64", "×", 3, ["6,400", "640,000", "1,064"])
    p10(its, "258", "×", 1, ["25,800", "268", "25.8"])
    which_calc(its, "36", "×", 2, ["36 × 10", "36 × 1,000", "36 ÷ 100"])
    p10(its, "306", "×", 2, ["3,060", "306,000", "36,000"], "(Keep the 0 in the tens of 306: it holds a place.)")
    its.append(mcq("63 × ? = 6,300", "100", ["10", "1,000", "10,000"],
                   "6,300 is 63 with two zeros in the empty places: the digits moved 2 places to the left. "
                   "So it is × <b>100</b>."))
    which_calc(its, "405", "×", 1, ["405 × 100", "405 ÷ 10", "405 × 1,000"])
    p10(its, "470", "×", 3, ["47,000", "4,700,000", "4,700"], "(The 0 in 470 is not one of the 3 places.)")
    p10(its, "2,500", "×", 1, ["250,000", "2,510", "250"])
    its.append(mcq("? × 10 = 5,200", "520", ["52", "52,000", "5,190"],
                   "Use the inverse: 5,200 ÷ 10. Every digit moves 1 place to the right: <b>520</b>. Check: 520 × 10 = 5,200."))
    which_calc(its, "7", "×", 3, ["7 × 100", "7 + 1,000", "7 × 10,000"])
    p10(its, "8,040", "×", 2, ["80,400", "8,040,000", "84,000"], "(Keep the 0 in the hundreds of 8,040.)")
    its.append(mcq("? × 1,000 = 39,000", "39", ["390", "3,900", "38,000"],
                   "Use the inverse: 39,000 ÷ 1,000. Every digit moves 3 places to the right: <b>39</b>. Check: 39 × 1,000 = 39,000."))
    its.append(mcq("715 × ? = 71,500", "100", ["10", "1,000", "10,000"],
                   "715 became 71,500: the 7 moved from the hundreds to the ten thousands. That is 2 places to the left, so it is × <b>100</b>."))
    red_digit(its, "284", "×", 2, 2, ["2 hundreds", "2 thousands", "2 tens"])
    its.append(mcq("Which number is 100 times bigger than 3,070?", "307,000", ["30,700", "3,070,000", "3,170"],
                   "100 times bigger means × 100. Every digit moves 2 places to the left: 3,070 × 100 = <b>307,000</b>. "
                   "(3,170 adds 100.)"))
    its.append(mcq("Which calculation has the answer 4,000?", "40 × 100", ["400 × 100", "4 × 100", "40 × 1,000"],
                   "40 × 100: the 4 moves from the tens to the thousands, so <b>40 × 100</b> = 4,000. "
                   "400 × 100 = 40,000, 4 × 100 = 400 and 40 × 1,000 = 40,000."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply whole numbers by 10, 100 and 1,000", "items": its}


# ============================================================ set 2: whole numbers ÷ 10, 100, 1,000
def set_whole_divide():
    its = []
    p10(its, "370", "÷", 1, ["3.7", "3,700", "360"])
    p10(its, "5,600", "÷", 2, ["560", "5.6", "5,500"])
    p10(its, "8,000", "÷", 3, ["80", "0.8", "7,000"])
    p10(its, "450", "÷", 2, ["45", "0.45", "350"], "(45 moves only 1 place; 0.45 moves 3 places.)")
    p10(its, "63", "÷", 1, ["0.63", "630", "53"])
    p10(its, "29", "÷", 2, ["2.9", "0.029", "29.00"], "(29.00 is still 29: writing zeros does not divide.)")
    p10(its, "7", "÷", 1, ["0.07", "70", "7.0"], "(7.0 is still 7.)")
    which_calc(its, "6,200", "÷", 3, ["6,200 ÷ 100", "6,200 ÷ 10", "6,200 × 1,000"])
    p10(its, "3,250", "÷", 3, ["32.5", "0.325", "325"])
    p10(its, "806", "÷", 2, ["8.6", "80.6", "0.806"], "(Keep the 0: it holds the tenths place.)")
    p10(its, "52", "÷", 3, ["0.52", "0.0052", "5.2"])
    p10(its, "4,000", "÷", 2, ["400", "4", "0.4"])
    which_calc(its, "145", "÷", 2, ["145 ÷ 10", "145 ÷ 1,000", "145 × 100"])
    p10(its, "9", "÷", 2, ["0.9", "0.009", "900"])
    p10(its, "2,705", "÷", 1, ["27.05", "275", "2.705"])
    its.append(mcq("? ÷ 100 = 3.4", "340", ["34", "3,400", "0.034"],
                   "Use the inverse: 3.4 × 100. Every digit moves 2 places to the left: <b>340</b>. Check: 340 ÷ 100 = 3.4."))
    its.append(mcq("760 ÷ ? = 7.6", "100", ["10", "1,000", "10,000"],
                   "The 7 moved from the hundreds to the ones. That is 2 places to the right, so it is ÷ <b>100</b>."))
    p10(its, "18", "÷", 3, ["0.18", "0.0018", "18,000"])
    its.append(mcq("? ÷ 10 = 0.5", "5", ["50", "0.05", "500"],
                   "Use the inverse: 0.5 × 10. The 5 moves from the tenths to the ones: <b>5</b>. Check: 5 ÷ 10 = 0.5."))
    red_digit(its, "3,047", "÷", 2, 0, ["7 tenths", "7 ones", "7 thousandths"])
    assert len(its) == 20, len(its)
    return {"title": "Divide whole numbers by 10, 100 and 1,000", "items": its}


# ============================================================ set 3: decimals × 10, 100, 1,000
def set_decimal_times(P):
    its = []
    p10(its, "3.2", "×", 1, ["3.20", "320", "0.32"], add0("3.20", "3.2"))
    p10(its, "0.36", "×", 2, ["0.3600", "3.6", "360"], add0("0.3600", "0.36"))
    p10(its, "4.5", "×", 1, ["4.50", "450", "0.45"], add0("4.50", "4.5"))
    p10(its, "0.8", "×", 1, ["0.80", "80", "0.08"], add0("0.80", "0.8"))
    p10(its, "1.7", "×", 2, ["17", "1.700", "1,700"])
    p10(its, "2.35", "×", 2, ["23.5", "2.3500", "2,350"])
    p10(its, "0.6", "×", 2, ["6", "0.600", "600"])
    which_calc(its, "0.53", "×", 2, ["0.53 × 10", "0.53 × 1,000", "0.53 ÷ 100"])
    p10(its, "0.25", "×", 1, ["0.250", "25", "0.025"], add0("0.250", "0.25"))
    p10(its, "0.07", "×", 2, ["0.0700", "70", "0.7"])
    p10(its, "5.4", "×", 3, ["540", "5.4000", "54,000"])
    p10(its, "3.06", "×", 1, ["3.060", "306", "0.306"], "(Keep the 0: it holds the tenths place.)")
    red_digit(its, "0.47", "×", 1, -1, ["4 hundredths", "4 tenths", "4 tens"])
    p10(its, "0.9", "×", 3, ["90", "9,000", "0.9000"])
    p10(its, "12.4", "×", 2, ["124", "12,400", "12.400"])
    which_calc(its, "1.6", "×", 3, ["1.6 × 100", "1.6 × 10", "1.6 ÷ 1,000"])
    p10(its, "0.125", "×", 3, ["12.5", "1,250", "0.125000"])
    p10(its, "7.08", "×", 3, ["708", "70,800", "7,800"], "(Keep the 0 in the hundreds.)")
    n, he, his = P.next()
    its.append(mcq("%s says 4.6 × 10 = 4.60. What is the mistake?" % n,
                   "4.60 = 4.6; the answer is 46",
                   ["%s should write 4.600" % n, "The answer is 0.46", "There is no mistake"],
                   "4.60 has the same value as 4.6, so adding a zero does not multiply. "
                   "The digits move 1 place to the left: 4.6 × 10 = <b>46</b>."))
    its.append(mcq("Which calculation has the answer 52?", "0.52 × 100", ["5.2 × 100", "0.52 × 10", "0.052 × 100"],
                   "0.52 × 100: the 5 moves from the tenths to the tens, so <b>0.52 × 100</b> = 52. "
                   "5.2 × 100 = 520, 0.52 × 10 = 5.2 and 0.052 × 100 = 5.2."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply decimals by 10, 100 and 1,000", "items": its}


# ============================================================ set 4: decimals ÷ 10, 100 and missing numbers
def set_decimal_divide():
    its = []
    p10(its, "4.5", "÷", 1, ["0.045", "45", "4.50"], "(4.50 is still 4.5.)")
    p10(its, "3.2", "÷", 2, ["0.32", "0.0032", "320"])
    p10(its, "0.6", "÷", 1, ["0.006", "6", "0.60"], "(0.60 is still 0.6.)")
    p10(its, "27.5", "÷", 1, ["275", "0.275", "27.50"])
    p10(its, "8.4", "÷", 2, ["0.84", "0.0084", "840"])
    p10(its, "0.9", "÷", 2, ["0.09", "0.0009", "90"])
    which_calc(its, "3.2", "÷", 2, ["3.2 ÷ 10", "3.2 ÷ 1,000", "3.2 × 100"])
    p10(its, "15.6", "÷", 2, ["1.56", "0.0156", "1,560"])
    p10(its, "0.38", "÷", 1, ["0.0038", "3.8", "0.380"], "(0.380 is still 0.38.)")
    p10(its, "60.2", "÷", 1, ["6.2", "0.602", "602"], "(Keep the 0: it holds the ones place.)")
    p10(its, "125.4", "÷", 2, ["12.54", "0.1254", "12,540"])
    red_digit(its, "41.6", "÷", 2, -1, ["6 hundredths", "6 tenths", "6 tens"])
    its.append(mcq("? × 100 = 470", "4.7", ["47", "0.47", "47,000"],
                   "Use the inverse: 470 ÷ 100. Every digit moves 2 places to the right: <b>4.7</b>. Check: 4.7 × 100 = 470."))
    its.append(mcq("? ÷ 10 = 0.36", "3.6", ["0.036", "36", "360"],
                   "Use the inverse: 0.36 × 10. Every digit moves 1 place to the left: <b>3.6</b>. Check: 3.6 ÷ 10 = 0.36."))
    its.append(mcq("2.9 × ? = 290", "100", ["10", "1,000", "10,000"],
                   "The 2 moved from the ones to the hundreds. That is 2 places to the left, so it is × <b>100</b>."))
    its.append(mcq("5.3 ÷ ? = 0.53", "10", ["100", "1,000", "10,000"],
                   "The 5 moved from the ones to the tenths. That is 1 place to the right, so it is ÷ <b>10</b>."))
    its.append(mcq("? × 1,000 = 6,800", "6.8", ["68", "0.68", "680"],
                   "Use the inverse: 6,800 ÷ 1,000. Every digit moves 3 places to the right: <b>6.8</b>. Check: 6.8 × 1,000 = 6,800."))
    its.append(mcq("? ÷ 100 = 0.07", "7", ["0.7", "70", "0.0007"],
                   "Use the inverse: 0.07 × 100. The 7 moves from the hundredths to the ones: <b>7</b>. Check: 7 ÷ 100 = 0.07."))
    its.append(mcq("Which is the same as 0.4 ÷ 10?", "4 ÷ 100", ["4 ÷ 10", "40 ÷ 10", "0.4 × 10"],
                   "0.4 ÷ 10 = 0.04, and 4 ÷ 100 = 0.04 too. So <b>4 ÷ 100</b>. "
                   "4 ÷ 10 = 0.4, 40 ÷ 10 = 4 and 0.4 × 10 = 4."))
    its.append(mcq("Which calculation does <b>not</b> equal 48?", "4.8 ÷ 10", ["480 ÷ 10", "0.48 × 100", "4.8 × 10"],
                   "480 ÷ 10 = 48, 0.48 × 100 = 48 and 4.8 × 10 = 48. But <b>4.8 ÷ 10</b> = 0.48."))
    assert len(its) == 20, len(its)
    return {"title": "Divide decimals and find missing numbers", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    add("A bag of potatoes has a mass of 3.5 kg. What is its mass in grams?", "3,500 g", ["350 g", "35,000 g", "3.500 g"],
        "1 kg = 1,000 g, so multiply by 1,000. The digits move 3 places to the left: 3.5 × 1,000 = <b>3,500 g</b>.")
    add("A school buys 100 notebooks at £2.45 each. How much do they cost altogether?", "£245.00",
        ["£24.50", "£2,450.00", "£102.45"],
        "£2.45 × 100: the digits move 2 places to the left. 2.45 × 100 = 245, so they cost <b>£245.00</b>. "
        "(£102.45 adds 100.)")
    add("A garden path has 100 paving slabs in a row. Each slab is 0.45 m long. How long is the path?", "45 m",
        ["4.5 m", "450 m", "100.45 m"],
        "0.45 × 100: the digits move 2 places to the left. The path is <b>45 m</b> long.")
    add("A plant is 250 cm tall. How tall is it in metres?", "2.5 m", ["25 m", "0.25 m", "2,500 m"],
        "100 cm = 1 m, so divide by 100. The digits move 2 places to the right: 250 ÷ 100 = <b>2.5 m</b>.")
    add("A watering can holds 4.2 litres of water. How many millilitres is that?", "4,200 ml",
        ["420 ml", "42,000 ml", "4.200 ml"],
        "1 litre = 1,000 ml, so multiply by 1,000: 4.2 × 1,000 = <b>4,200 ml</b>.")
    n, he, his = P.next()
    add("%s uses 750 g of flour to make bread. How many kilograms is that?" % n, "0.75 kg",
        ["7.5 kg", "0.075 kg", "750,000 kg"],
        "1,000 g = 1 kg, so divide by 1,000. The digits move 3 places to the right: 750 ÷ 1,000 = <b>0.75 kg</b>.")
    add("A pack of 10 bags of crisps costs £6.50. How much is one bag?", "65p", ["6.5p", "£65.00", "650p"],
        "£6.50 ÷ 10: the digits move 1 place to the right. £0.65 = <b>65p</b>. Check: 65p × 10 = 650p = £6.50.")
    add("A box of 100 stickers costs £3. How much is one sticker?", "3p", ["30p", "0.3p", "£300.00"],
        "£3 ÷ 100: the digits move 2 places to the right. £0.03 = <b>3p</b>. (30p is £3 ÷ 10.)")
    n, he, his = P.next()
    add("%s runs 0.8 km every day for 10 days. How far does %s run altogether?" % (n, he), "8 km",
        ["0.80 km", "80 km", "0.08 km"],
        "0.8 × 10: the 8 moves from the tenths to the ones. %s runs <b>8 km</b>. (0.80 km just adds a zero.)" % n)
    add("A lorry carries 1,000 boxes. Each box has a mass of 2.4 kg. What is the total mass?", "2,400 kg",
        ["240 kg", "24,000 kg", "1,002.4 kg"],
        "2.4 × 1,000: the digits move 3 places to the left. The total mass is <b>2,400 kg</b>.")
    add("A 3.6 m length of ribbon is cut into 10 equal pieces. How long is each piece?", "0.36 m",
        ["36 m", "0.036 m", "360 m"],
        "3.6 ÷ 10: the digits move 1 place to the right. Each piece is <b>0.36 m</b> (36 cm).")
    add("A PE teacher buys 10 footballs at £8.99 each. How much does she pay?", "£89.90",
        ["£899.00", "£18.99", "£80.99"],
        "£8.99 × 10: the digits move 1 place to the left. 8.99 × 10 = 89.9, so she pays <b>£89.90</b>. (£80.99 multiplies only the pounds.)")
    add("A 5,600 m cycle route goes round the park. How many kilometres is that?", "5.6 km",
        ["56 km", "0.56 km", "560 km"],
        "1,000 m = 1 km, so divide by 1,000: 5,600 ÷ 1,000 = <b>5.6 km</b>.")
    add("Fabric for the school play costs £4.75 per metre. How much do 100 m cost?", "£475.00",
        ["£47.50", "£4,750.00", "£104.75"],
        "£4.75 × 100: the digits move 2 places to the left. 100 m cost <b>£475.00</b>.")
    add("A real car is 100 times as long as a model car. The model is 4.3 cm long. How long is the real car?", "430 cm",
        ["43 cm", "4,300 cm", "0.043 cm"],
        "The real car is 100 times as long: 4.3 × 100 = <b>430 cm</b>, which is 4.3 m.")
    add("A class pays £245 for 100 museum tickets. How much is one ticket?", "£2.45",
        ["£24.50", "£24,500.00", "£2,450.00"],
        "£245 ÷ 100: the digits move 2 places to the right. One ticket costs <b>£2.45</b>. (£24.50 is £245 ÷ 10.)")
    add("A shop has 1,000 bottles of water. Each holds 1.5 litres. How much water is that altogether?", "1,500 litres",
        ["150 litres", "15,000 litres", "1.5000 litres"],
        "1.5 × 1,000: the digits move 3 places to the left: <b>1,500 litres</b>.")
    n, he, his = P.next()
    t = Dm("0.35") * 10
    assert 5 - t == Dm("1.5")
    add("%s buys 10 pencils at 35p each. %s pays with a £5 note. How much change does %s get?" % (n, cap(he), he), "£1.50",
        ["£3.50", "£4.65", "£2.50"],
        "10 × 35p = 350p = £3.50. Then £5.00 %s £3.50 = <b>£1.50</b>. Check: £3.50 + £1.50 = £5. "
        "(£3.50 is the cost, not the change.)" % MINUS)
    add("A cook uses 0.35 kg of rice for 10 school dinners. How much rice is needed for 1,000 school dinners?", "35 kg",
        ["350 kg", "3.5 kg", "0.35 kg"],
        "1,000 dinners is 100 lots of 10 dinners. So multiply by 100: 0.35 × 100 = <b>35 kg</b>. "
        "(350 kg multiplies by 1,000, but 0.35 kg is for 10 dinners, not 1.)")
    assert Dm("0.35") / 10 * 1000 == 35
    add("A pile of 1,000 sheets of paper is 95 mm tall. How thick is one sheet?", "0.095 mm",
        ["0.95 mm", "0.0095 mm", "95,000 mm"],
        "95 ÷ 1,000: the digits move 3 places to the right. Write 0 in the ones and tenths: one sheet is <b>0.095 mm</b> thick.")
    assert len(its) == 20, len(its)
    return {"title": "Word problems: money and measures", "items": its}


# ============================================================ lesson
def body_html():
    f1 = pv_move("45", "×", 2, CW=70)
    f2 = pv_move("450", "÷", 2, CW=70)
    f3 = pv_move("0.36", "×", 2, CW=70)
    f4 = pv_move("3.2", "÷", 2, CW=70)
    return (
        "<h2>The digits move, the point stays still</h2>"
        "<p>When you multiply by 10, 100 or 1,000, every digit moves to the <b>left</b>. "
        "When you divide, every digit moves to the <b>right</b>.</p>"
        + table(["Calculation", "Every digit moves"], [
            ["× 10 or ÷ 10", "1 place"], ["× 100 or ÷ 100", "2 places"], ["× 1,000 or ÷ 1,000", "3 places"]])
        + "<p>The decimal point does not move. Write 0 in any empty place up to the ones.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>45 × 100: the 4 moves from the tens to the thousands, the 5 from the ones to the hundreds. "
        "The grey zeros fill the empty places. 45 × 100 = 4,500. "
        "(Th = thousands, H = hundreds, T = tens, O = ones, Tth = tenths, Hth = hundredths, Thth = thousandths.)</figcaption></figure>"
        "<h2>Dividing can give a decimal</h2>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>450 ÷ 100: every digit moves 2 places to the right. The 5 crosses the point into the tenths. "
        "450 ÷ 100 = 4.5 (the 0 in the tenths is not needed).</figcaption></figure>"
        + ex("Example", "7,000 ÷ 1,000", "Every digit moves 3 places to the right. The 7 goes from the thousands to the ones.", "7")
        + "<h2>Decimals work the same way</h2>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>0.36 × 100: the 3 moves from the tenths to the tens and the 6 from the hundredths to the ones. "
        "0.36 × 100 = 36.</figcaption></figure>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>3.2 ÷ 100: the 3 moves from the ones to the hundredths. Write 0 in the ones and the tenths. "
        "3.2 ÷ 100 = 0.032.</figcaption></figure>"
        "<h2>Missing numbers: use the inverse</h2>"
        "<p>× and ÷ undo each other. To find ? in ? × 100 = 470, work out 470 ÷ 100 = 4.7. "
        "Then check: 4.7 × 100 = 470.</p>"
        + ex("Example", "A pen costs £1.25. How much do 100 pens cost?",
             "1.25 × 100: every digit moves 2 places to the left. 1.25 × 100 = 125.", "£125")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3.2 × 10 = 3.20 (just adding a zero)", "3.20 is the same as 3.2. Move the digits 1 place: 32"],
            ["450 ÷ 100 = 45 or 0.45", "÷ 100 moves the digits exactly 2 places: 4.5"],
            ["0.36 × 100 = 0.3600", "The digits move 2 places to the left: 36"],
            ["306 × 100 = 36,000", "Keep the 0 that holds a place: 30,600"],
            ["Moving the digits the wrong way", "× makes the number bigger (left); ÷ makes it smaller (right)"],
        ])
    )


FAQ = [
    {"q": "How do you multiply by 10, 100 and 1,000 in Year 5?",
     "a": "Move every digit 1, 2 or 3 places to the left and keep the decimal point still. Write 0 in empty places up to the ones, so 45 × 100 = 4,500 and 0.36 × 100 = 36."},
    {"q": "How do you divide a decimal by 100?",
     "a": "Move every digit 2 places to the right and write 0 in the empty places up to the ones. For example, 3.2 ÷ 100 = 0.032."},
    {"q": "Why is “just add a zero” wrong?",
     "a": "It only works for whole numbers. With decimals it gives the wrong answer: 3.2 × 10 is 32, not 3.20, because 3.20 has the same value as 3.2."},
    {"q": "Where is multiplying by 10, 100 and 1,000 used in real life?",
     "a": "Converting units (3.5 kg = 3,500 g, 250 cm = 2.5 m) and working out prices for 10, 100 or 1,000 items. It is part of the Year 5 National Curriculum for multiplication and division."},
]


def mark_large(u, pattern):
    """Tag place value charts so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def check_answers(sets):
    """Re-check every plain '× / ÷' question with Decimal."""
    rx = re.compile(r"^([\d,.]+) ([×÷]) ([\d,]+) = \?$")
    n = 0
    for s in sets:
        for it in s["items"]:
            m = rx.match(it["q"])
            if m:
                a, op, b = (Dm(m.group(1).replace(",", "")), m.group(2), Dm(m.group(3).replace(",", "")))
                r = a * b if op == "×" else a / b
                assert val(it["c"][it["a"]])[0] == r, it["q"]
                n += 1
    return n


def gen():
    rnd = random.Random(5508)
    P = People(rnd)
    sets = [set_whole_times(), set_whole_divide(), set_decimal_times(P), set_decimal_divide(), set_words(P)]
    check_answers(sets)
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "multiply-and-divide-by-10-100-1000", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiply and Divide by 10, 100 and 1,000",
        "seo_title": "Year 5 Multiply and Divide by 10, 100 and 1,000 Worksheets: Whole Numbers and Decimals",
        "short_title": "× and ÷ by 10, 100, 1,000",
        "domain": "Multiplication and division",
        "standard_code": "Year 5: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply and divide whole numbers and those involving decimals by 10, 100 and 1,000.",
        "meta_desc": "Free Year 5 maths worksheets on multiplying and dividing by 10, 100 and 1,000 for the National Curriculum: whole numbers and decimals, place value charts, missing numbers, unit conversions and money problems. 100 questions with an answer key.",
        "key_big": "The digits move, the decimal point stays still: left to multiply, right to divide.",
        "key_sub": "1 place for 10, 2 places for 100, 3 places for 1,000. 45 × 100 = 4,500, 450 ÷ 100 = 4.5, 0.36 × 100 = 36, 3.2 ÷ 100 = 0.032. Adding a zero to 3.2 gives 3.20, which is still 3.2.",
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
