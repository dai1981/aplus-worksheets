# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Decimal Place Value, Powers of 10, Comparing and Rounding Decimals (5.NBT.A.1-4)
  python3 tools/gen_us_math_g5_decimal_place_value.py
All numbers are decimal.Decimal (never float), so every answer is exact.
Expanded form uses the Common Core style: 3 × 1 + 4 × (1/10) + 5 × (1/100).
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP, ROUND_DOWN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GRAY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

# place index: 2 = hundreds, 1 = tens, 0 = ones, -1 = tenths, -2 = hundredths, -3 = thousandths
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}
PLACE1 = {3: "thousand", 2: "hundred", 1: "ten", 0: "one", -1: "tenth", -2: "hundredth", -3: "thousandth"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text without extra zeros, commas from 1,000: Dm('2800.0') -> '2,800'."""
    return format(Dm(x).normalize(), ",f")


def K(x):
    """Decimal text that keeps the zeros as written (rounded answers): Dm('4.00') -> '4.00'."""
    return format(Dm(x), ",f")


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def unit(i):
    """The value of 1 in place i, as text for expanded form: 10, 1, 1/10 ..."""
    return "{:,}".format(10 ** i) if i >= 0 else fr(1, "{:,}".format(10 ** -i))


def digit_at(x, i):
    """Digit of Decimal x in place i."""
    return int((Dm(x).scaleb(-i)).to_integral_value(rounding=ROUND_DOWN)) % 10


def plural(n, one, many):
    return one if n == 1 else many


VAL = re.compile(r"^\$?([\d,]*\.?\d+)(\s.*)?$")


def val(c):
    m = VAL.match(c)
    return (Dm(m.group(1).replace(",", "")), m.group(2) or "") if m else None


# ------------------------------------------------------------ number names
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words_999(n):
    out = []
    if n >= 100:
        out.append(ONES[n // 100] + " hundred")
        n %= 100
    if n >= 20:
        out.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n > 0:
        out.append(ONES[n])
    return " ".join(out)


def words_int(n):
    th, rest = divmod(n, 1000)
    if th and rest:
        return words_999(th) + " thousand, " + words_999(rest)
    if th:
        return words_999(th) + " thousand"
    return words_999(rest) if rest else "zero"


def words(s):
    """Word form of a decimal written as text: '3.045' -> 'three and forty-five thousandths'.
    'and' is said only for the decimal point."""
    w, _, f = s.partition(".")
    w = int(w.replace(",", ""))
    if not f or int(f) == 0:
        return words_int(w)
    k = len(f)
    v = int(f)
    part = words_999(v) + " " + (PLACE1[-k] if v == 1 else PLACE[-k])
    return (words_int(w) + " and " + part) if w else part


def expanded(s):
    """Expanded form with unit values: '4.326' -> 4 × 1 + 3 × 1/10 + 2 × 1/100 + 6 × 1/1,000."""
    w, _, f = s.partition(".")
    terms = []
    for j, ch in enumerate(w):
        i = len(w) - 1 - j
        if ch != "0":
            terms.append("%s × %s" % (ch, unit(i)))
    for j, ch in enumerate(f):
        if ch != "0":
            terms.append("%s × %s" % (ch, unit(-(j + 1))))
    return " + ".join(terms)


def exp_terms(pairs):
    """Expanded form from (digit, place) pairs, for wrong answers."""
    return " + ".join("%d × %s" % (d, unit(i)) for d, i in pairs)


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e, same_value_ok=False):
    """4 choices: correct + 3 wrong. Positions are set by balance().
    Wrong answers must be different from the correct one, also in value (4.0 vs 4.00), unless same_value_ok."""
    correct = str(correct)
    wrong = [str(x) for x in wrong]
    assert len(wrong) == 3, (q, wrong)
    ch = [correct] + wrong
    assert len(set(ch)) == 4, (q, ch)
    if not same_value_ok:
        vs = [val(x) for x in ch]
        if all(vs):
            assert len(set(vs)) == 4, (q, ch)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_pick(q, correct, cands, e):
    """Take the first 3 candidates that differ from the correct answer and from each other in value."""
    correct = str(correct)
    seen = {val(correct) or correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        k = val(c) or c
        if k in seen or c.startswith("-") or (val(c) and val(c)[0] == 0):
            continue
        seen.add(k)
        pick.append(c)
        if len(pick) == 3:
            break
    return mcq(q, correct, pick, e)


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


# ------------------------------------------------------------ figures
CW, PW, HEAD, ROW = 96, 18, 30, 48      # chart: column width, point column width, header and digit row height
LABELS = {2: "Hundreds", 1: "Tens", 0: "Ones", -1: "Tenths", -2: "Hundredths", -3: "Thousandths"}


def chart_svg(s, hi=None):
    """Place-value chart for the decimal written as text s (up to 3 decimal places).
    Columns from the left-most whole digit to thousandths, with a narrow column for the point. hi = place to color red."""
    w, _, f = s.partition(".")
    top = max(len(w) - 1, 0)
    places = list(range(top, -4, -1))
    x0, y0 = 6, 6
    W = x0 * 2 + CW * len(places) + PW
    H = y0 * 2 + HEAD + ROW
    xs = {}
    x = x0
    for i in places:
        xs[i] = x
        x += CW + (PW if i == 0 else 0)
    px = xs[0] + CW                                       # left edge of the point column
    out = []
    out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
               % (x0, y0, W - 2 * x0, HEAD + ROW, GREEN))
    out.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0, y0, W - 2 * x0, HEAD, FILL))
    for i in places:
        if i != top:
            out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                       % (xs[i], y0, xs[i], y0 + HEAD + ROW, GREEN))
        out.append(text(xs[i] + CW / 2.0, y0 + 20, LABELS[i], 14))
        j = len(w) - 1 - i if i >= 0 else None
        ch = w[j] if i >= 0 and 0 <= j < len(w) else (f[-i - 1] if i < 0 and -i <= len(f) else None)
        if ch is not None:
            out.append(text(xs[i] + CW / 2.0, y0 + HEAD + 35, ch, 30, col=RED if hi == i else INK, weight=800))
    out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (px + PW, y0, px + PW, y0 + HEAD + ROW, GREEN))
    out.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, y0 + HEAD + 34, INK))
    out.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
               % (x0, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    return svg_wrap(W, H, "".join(out), "place-value chart showing %s" % s)


def number_line_svg(lo, hi, x):
    """Number line from lo to hi with 10 equal spaces, labels at both ends and the halfway point, red dot on x."""
    lo, hi, x = Dm(lo), Dm(hi), Dm(x)
    step = (hi - lo) / 10
    places = max(0, -(hi - lo).normalize().as_tuple().exponent)
    L, R, Y = 50, 390, 52
    W, H = 440, 96

    def X(v):
        return L + float((v - lo) / (hi - lo)) * (R - L)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 12, Y, R + 12, Y, INK)]
    for k in range(11):
        v = lo + step * k
        big = k in (0, 5, 10)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%d'/>"
                 % (X(v), Y - (11 if big else 6), X(v), Y + (11 if big else 6), INK, 2 if big else 1))
        if big:
            kk = places + (1 if k == 5 else 0)          # ends: the rounding place; middle: one place more
            s.append(text(X(v), Y + 32, K(v.quantize(Dm(1).scaleb(-kk))), 15, col=GREEN if k != 5 else GRAY))
    s.append("<circle cx='%.1f' cy='%d' r='7' fill='%s'/>" % (X(x), Y, RED))
    tx = min(max(X(x), 34), W - 34)
    s.append(text(tx, Y - 18, N(x), 16, col=RED, weight=800))
    assert lo <= x <= hi
    return svg_wrap(W, H, "".join(s), "number line from %s to %s" % (K(lo), K(hi)))


# ============================================================ set 1: value of a digit, 10 times and 1/10
def value_item(s, i, chart):
    d = digit_at(s, i)
    assert d != 0
    v = Dm(d).scaleb(i)
    if i >= 0:
        e = "The %d is in the %s place, so its value is %d × %s = <b>%s</b>." % (d, PLACE[i], d, "{:,}".format(10 ** i), N(v))
    else:
        e = ("The %d is the %s digit after the point, in the <b>%s</b> place. Its value is %d %s = %d × %s = <b>%s</b>."
             % (d, ["1st", "2nd", "3rd"][-i - 1], PLACE[i], d, plural(d, PLACE1[i], PLACE[i]), d, unit(i), N(v)))
    cands = [N(Dm(d).scaleb(i - 1)), N(Dm(d).scaleb(i + 1)), str(d), N(Dm(d).scaleb(i - 2)), N(Dm(d).scaleb(i + 2))]
    if chart:
        q = fig(chart_svg(s)) + "What is the value of the digit %d in this number?" % d
    else:
        q = "What is the value of the digit %d in %s?" % (d, s)
    return mcq_pick(q, N(v), cands, e)


def set_value():
    its = []
    for s, i in [("4.38", -1), ("25.746", -2), ("6.159", -3), ("73.204", 1), ("0.582", -2), ("18.637", -3)]:
        its.append(value_item(s, i, True))
    for s, i in [("31.284", -3), ("9.065", -2), ("142.39", 2), ("0.917", -1)]:
        its.append(value_item(s, i, False))
    # name the place (3) - thousands vs thousandths
    for s, d, i, wrong in [("8.305", 5, -3, ["thousands", "hundredths", "tenths"]),
                           ("2,416.7", 4, 2, ["hundredths", "tens", "thousands"]),
                           ("0.628", 2, -2, ["hundreds", "tenths", "thousandths"])]:
        assert digit_at(s.replace(",", ""), i) == d
        e = ("Places to the right of the point end in <b>-ths</b>: tenths, hundredths, thousandths. "
             "Places to the left do not: ones, tens, hundreds, thousands. The %d is in the <b>%s</b> place."
             % (d, PLACE[i]))
        its.append(mcq("In %s, which place is the digit %d in?" % (s, d), PLACE[i], wrong, e))
    # ten times and one tenth (7)
    its.append(mcq("In 5.55, how does the 5 in the tenths place compare to the 5 in the hundredths place?",
                   "10 times as much", ["%s as much" % fr(1, 10), "100 times as much", "the same"],
                   "The tenths 5 is 0.5 and the hundredths 5 is 0.05. 0.5 = 10 × 0.05, so it is worth "
                   "<b>10 times as much</b>. One place to the left is always 10 times as much."))
    its.append(mcq("In 3.333, how does the 3 in the thousandths place compare to the 3 in the hundredths place?",
                   "%s as much" % fr(1, 10), ["10 times as much", "%s as much" % fr(1, 100), "the same"],
                   "The thousandths 3 is 0.003 and the hundredths 3 is 0.03. 0.003 is 0.03 ÷ 10, so it is worth "
                   "<b>%s as much</b>. One place to the right is always %s as much." % (fr(1, 10), fr(1, 10))))
    its.append(mcq("What is 10 times as much as 0.03?", "0.3", ["0.030", "0.003", "3"],
                   "10 times as much moves each digit 1 place to the left: 3 hundredths become 3 tenths, <b>0.3</b>. "
                   "Writing a 0 at the end (0.030) does not change the value."))
    its.append(mcq("What is %s of 0.4?" % fr(1, 10), "0.04", ["4", "0.004", "0.40"],
                   "%s of a number moves each digit 1 place to the right: 4 tenths become 4 hundredths, <b>0.04</b>. "
                   "(4 is 10 times as much, and 0.40 is the same as 0.4.)" % fr(1, 10)))
    its.append(mcq("0.6 is 10 times as much as what number?", "0.06", ["6", "0.006", "0.60"],
                   "10 times what is 0.6? One place to the right of tenths is hundredths: <b>0.06</b>. Check: 10 × 0.06 = 0.6."))
    its.append(mcq("How many hundredths are in 0.3?", "30", ["3", "300", "0.03"],
                   "1 tenth = 10 hundredths, so 3 tenths = <b>30</b> hundredths. 0.3 = 0.30."))
    its.append(mcq("How many thousandths make 1 hundredth?", "10", ["100", "1,000", "0.1"],
                   "Each place is 10 times the place to its right, so <b>10</b> thousandths make 1 hundredth: 10 × 0.001 = 0.01."))
    assert len(its) == 20, len(its)
    return {"title": "Value of a digit, 10 times and 1/10 as much", "items": its}


# ============================================================ set 2: powers of 10
def sup(n):
    return "10<sup>%d</sup>" % n


def p10_e(x, op, n):
    x = Dm(x)
    ans = x.scaleb(n) if op == "×" else x.scaleb(-n)
    word = "1 place" if n == 1 else "%d places" % n
    if op == "×":
        e = ("%s = %s, which has %d %s. Multiplying by %s moves the decimal point <b>%s to the right</b>: %s × %s = <b>%s</b>."
             % (sup(n), "{:,}".format(10 ** n), n, plural(n, "zero", "zeros"), sup(n), word, N(x), sup(n), N(ans)))
        if "." not in N(x) or len(N(x).split(".")[1]) < n:
            e += " Write zeros to fill the empty places."
    else:
        e = ("%s = %s. Dividing by %s moves the decimal point <b>%s to the left</b>: %s ÷ %s = <b>%s</b>."
             % (sup(n), "{:,}".format(10 ** n), sup(n), word, N(x), sup(n), N(ans)))
        if ans < 1:
            e += " Write zeros to hold the empty places."
    return ans, e


def set_powers():
    its = []
    for n, wrong in [(3, ["30", "100", "10,000"]), (4, ["40", "1,000", "100,000"]), (6, ["60", "100,000", "10,000,000"])]:
        e = ("The exponent %d tells how many 10s are multiplied: %s. So %s is 1 followed by %d zeros: <b>%s</b>. "
             "It is not 10 × %d = %d." % (n, " × ".join(["10"] * n), sup(n), n, "{:,}".format(10 ** n), n, 10 * n))
        its.append(mcq("What is %s?" % sup(n), "{:,}".format(10 ** n), wrong, e))
    its.append(mcq("Which shows 100,000 using an exponent?", sup(5), [sup(6), sup(4), "5<sup>10</sup>"],
                   "100,000 is 1 followed by <b>5 zeros</b>, so it is 10 × 10 × 10 × 10 × 10 = <b>%s</b>. "
                   "Count the zeros, not all 6 digits." % sup(5)))
    its.append(mcq("Which is the same as 10 × 10 × 10 × 10?", sup(4), [sup(3), "4<sup>10</sup>", "40"],
                   "Four 10s are multiplied, so the exponent is 4: <b>%s</b> = 10,000. (40 is 10 + 10 + 10 + 10.)" % sup(4)))
    # whole number × power of 10 (4)
    for x, n, extra in [("36", 2, "720"), ("7", 3, "21"), ("450", 2, "900"), ("2.5", 3, "2.5000")]:
        ans, e = p10_e(x, "×", n)
        w = [extra, N(ans / 10), N(ans * 10)]
        if extra == "720":
            e += " (720 comes from thinking %s = 20.)" % sup(2)
        elif extra == "21":
            e += " (21 comes from multiplying by 3 instead of 1,000.)"
        elif extra == "900":
            e += " (900 comes from multiplying by 2 instead of 100.)"
        else:
            e += " (2.5000 only adds zeros after the point, and that does not change the value.)"
        its.append(mcq("What is %s × %s?" % (N(x), sup(n)), N(ans), w, e, same_value_ok=(extra == "2.5000")))
    # decimal × power of 10 (4)
    for x, n, extra in [("0.68", 2, None), ("3.9", 2, "3.900"), ("0.05", 3, None), ("1.24", 1, "1.240")]:
        ans, e = p10_e(x, "×", n)
        w = [N(ans / 10), N(ans * 10), N(Dm(x).scaleb(-n))]
        if extra:
            w = [extra, N(ans / 10), N(Dm(x).scaleb(-n))]
            e += " (%s only adds zeros at the end and does not change the value.)" % extra
        its.append(mcq("What is %s × %s?" % (N(x), sup(n)), N(ans), w, e, same_value_ok=bool(extra)))
    # divide by a power of 10 (4)
    for x, n in [("4.7", 2), ("365", 3), ("82", 2), ("5", 3)]:
        ans, e = p10_e(x, "÷", n)
        w = [N(Dm(x).scaleb(n)), N(ans * 10), N(ans / 10)]
        e += " Check: dividing makes the number smaller."
        its.append(mcq("What is %s ÷ %s?" % (N(x), sup(n)), N(ans), w, e))
    # patterns (3)
    its.append(mcq("How many zeros are at the end of the product 40 × %s?" % sup(3), "4", ["3", "1", "7"],
                   "%s = 1,000 gives 3 zeros, and 40 already has 1 zero. 40 × 1,000 = 40,000, which has <b>4</b> zeros at the end. (7 adds 4 + 3, and 3 forgets the zero in 40.)"
                   % sup(3)))
    its.append(mcq("To find 4.7 ÷ %s, how does the decimal point move?" % sup(2), "2 places to the left",
                   ["2 places to the right", "1 place to the left", "it does not move"],
                   "The exponent 2 means ÷ 100, so the point moves <b>2 places</b>. Dividing makes the number smaller, so it moves "
                   "<b>to the left</b>: 4.7 → 0.47 → 0.047."))
    its.append(mcq("What goes in the box? <b>0.093 × ☐ = 93</b>", sup(3), [sup(2), sup(1), sup(4)],
                   "0.093 → 0.93 → 9.3 → 93: the point moved <b>3 places to the right</b>, so the number was multiplied by "
                   "1,000 = <b>%s</b>. (%s would give 9.3.)" % (sup(3), sup(2))))
    assert len(its) == 20, len(its)
    return {"title": "Powers of 10 and exponents", "items": its}


# ============================================================ set 3: read and write decimals
def set_forms():
    its = []
    # word form -> standard form (6)
    for s, wrong, why in [
            ("12.06", ["12.6", "12.006", "6.12"], "Hundredths need 2 digits after the point, so write a 0 in the tenths place."),
            ("3.045", ["3.45", "3,045", "3.0045"], "Thousandths need 3 digits after the point: 045. “Thousandths” is not “thousands”."),
            ("0.208", ["200.008", "0.28", "208,000"], "There is no “and”, so there is no whole number part. Thousandths need 3 digits: 208."),
            ("50.009", ["50.9", "50.09", "9.05"], "Thousandths need 3 digits after the point, so write two zeros first: 009."),
            ("6.304", ["6.34", "304.006", "6.0304"], "Thousandths need 3 digits after the point: 304."),
            ("6.015", ["6.15", "15.006", "6.0015"], "Thousandths need 3 digits after the point: 015.")]:
        w = words(s)
        e = "“And” marks the decimal point. %s So <b>%s</b> is <b>%s</b>." % (why, w, s)
        if s == "0.208":
            e += " (200.008 would be “two hundred <b>and</b> eight thousandths”.)"
        its.append(mcq("Write in standard form: <b>%s</b>" % w, s, wrong, e))
    # standard form -> word form (5)
    for s, wrong, why in [
            ("0.045", ["forty-five hundredths", "forty-five thousands", "four hundred five thousandths"],
             "The last digit, 5, is in the thousandths place, so read 45 and say <b>thousandths</b>."),
            ("2.07", ["two and seven tenths", "two and seventy hundredths", "two and seven thousandths"],
             "Say the whole number, say “and” for the point, then read 07 as seven and name the last place: hundredths."),
            ("13.502", ["thirteen and fifty-two thousandths", "thirteen and five hundred two hundredths",
                        "thirteen and five hundred twenty thousandths"],
             "Read the digits after the point as a whole number (502), then name the last place: thousandths."),
            ("4.38", ["four and thirty-eight tenths", "forty-three and eight tenths", "four and thirty-eight thousandths"],
             "Read the digits after the point as a whole number (38), then name the last place: hundredths."),
            ("0.909", ["nine hundred and nine thousandths", "ninety-nine thousandths", "nine and nine hundredths"],
             "Read 909, then name the last place: thousandths. Do not say “and” inside 909: “and” means the decimal point, "
             "so “nine hundred and nine thousandths” is 900.009.")]:
        its.append(mcq("Which is <b>%s</b> in word form?" % s, words(s), wrong, why + " So it is <b>%s</b>." % words(s)))
    # standard form -> expanded form (3)
    exp_items = [
        ("4.326", [exp_terms([(4, 1), (3, 0), (2, -1), (6, -2)]),
                   exp_terms([(4, 0), (3, 1), (2, 2), (6, 3)]),
                   exp_terms([(4, 0), (6, -1), (2, -2), (3, -3)])]),
        ("0.507", [exp_terms([(5, -1), (7, -2)]), exp_terms([(5, -2), (7, -3)]), exp_terms([(5, 2), (7, 0)])]),
        ("12.08", [exp_terms([(1, 1), (2, 0), (8, -1)]), exp_terms([(1, 1), (2, 0), (8, 2)]), exp_terms([(1, 0), (2, -1), (8, -3)])]),
    ]
    for s, wrong in exp_items:
        e = ("Write each non-zero digit times the value of its place: %s. A 0 adds nothing, but it still holds its place, "
             "so the digits after it stay in the right places." % expanded(s))
        its.append(mcq("Which shows <b>%s</b> in expanded form?" % s, expanded(s), wrong, e))
    # expanded form -> standard form (3)
    for terms, s, wrong in [([(5, 1), (2, 0), (6, -2)], "52.06", ["52.6", "52.006", "5.206"]),
                            ([(7, 0), (3, -3)], "7.003", ["7.3", "7.03", "7,003"]),
                            ([(9, -1), (4, -3)], "0.904", ["0.94", "0.094", "9.04"])]:
        assert Dm(s) == sum(Dm(d).scaleb(i) for d, i in terms)
        e = ("Put each digit in its place and write 0 in every empty place between them: %s. %s means "
             "thousandths, not thousands." % (" ".join("%s %s" % (d, plural(d, PLACE1[i], PLACE[i])) for d, i in terms) + " = <b>" + s + "</b>",
                                             fr(1, "1,000")))
        if not any(i == -3 for d, i in terms):
            e = ("Put each digit in its place and write 0 in every empty place between them: %s."
                 % (" ".join("%s %s" % (d, plural(d, PLACE1[i], PLACE[i])) for d, i in terms) + " = <b>" + s + "</b>"))
        its.append(mcq("What number is <b>%s</b>?" % exp_terms(terms), s, wrong, e))
    # digits in places (3)
    its.append(mcq("Which number has 2 ones, 0 tenths, 5 hundredths and 8 thousandths?", "2.058", ["2.58", "2.508", "20.58"],
                   "Write the digits in order after the point: 0 tenths, 5 hundredths, 8 thousandths → <b>2.058</b>. "
                   "Keep the 0 in the tenths place."))
    its.append(mcq("Which number has a 6 in the thousandths place?", "5.236", ["5.263", "5.623", "6,235"],
                   "The thousandths place is the <b>3rd</b> digit after the point. In 5.236 it is 6. "
                   "In 6,235 the 6 is in the thousands place, not the thousandths."))
    its.append(mcq("Which number is equal to 0.4?", "0.400", ["0.004", "0.04", "4.0"],
                   "Zeros at the <b>end</b> of a decimal do not change its value: 0.4 = 0.40 = <b>0.400</b>. "
                   "Zeros right after the point do: 0.04 and 0.004 are much smaller.", same_value_ok=True))
    assert len(its) == 20, len(its)
    return {"title": "Read and write decimals: word form and expanded form", "items": its}


# ============================================================ set 4: compare and order
def pad(xs):
    k = max(len(x.split(".")[1]) if "." in x else 0 for x in xs)
    return [format(Dm(x).quantize(Dm(1).scaleb(-k)), "f") for x in xs]


def first_diff(a, b):
    """Place where a and b first differ (same whole part assumed or not)."""
    for i in range(3, -4, -1):
        if digit_at(a, i) != digit_at(b, i):
            return i
    return None


def set_compare(P):
    its = []
    for nums, most in [(["0.7", "0.65", "0.698", "0.069"], True), (["2.35", "2.305", "2.4", "2.399"], True),
                       (["0.5", "0.49", "0.502", "0.499"], True), (["8.09", "8.1", "8.009", "8.099"], True),
                       (["0.3", "0.25", "0.209", "0.31"], False), (["1.08", "1.8", "1.008", "1.081"], False),
                       (["4.6", "4.06", "4.606", "4.066"], False)]:
        srt = sorted(nums, key=Dm)
        ans = srt[-1] if most else srt[0]
        nxt = srt[-2] if most else srt[1]
        big, small = (ans, nxt) if most else (nxt, ans)
        e = ("Line up the decimal points and write zeros so all have 3 places: %s. Then compare from the left. "
             % ", ".join(pad(nums)))
        i = first_diff(big, small)
        pb, ps = pad(nums)[nums.index(big)], pad(nums)[nums.index(small)]
        e += ("%s and %s first differ in the %s place: %d &gt; %d. So <b>%s</b> is the %s."
              % (pb, ps, PLACE[i], digit_at(big, i), digit_at(small, i), ans, "greatest" if most else "least"))
        longest = max(nums, key=len)
        if longest != ans and most:
            e += " More digits does not mean greater."
        its.append(mcq("Which number is the %s?" % ("greatest" if most else "least"), ans, [x for x in nums if x != ans], e))
    # which comparison is true (5)
    for a, b in [("0.125", "0.5"), ("3.07", "3.068"), ("0.9", "0.899"), ("6.42", "6.420"), ("12.305", "12.35")]:
        A, B = Dm(a), Dm(b)
        sign = "&lt;" if A < B else "&gt;" if A > B else "="
        flip = {"&lt;": "&gt;", "&gt;": "&lt;", "=": "&lt;"}
        right = "%s %s %s" % (a, sign, b)
        if sign == "=":
            wrong = ["%s &lt; %s" % (a, b), "%s &gt; %s" % (a, b), "%s &gt; %s" % (b, a)]
            e = "Zeros at the end do not change a decimal: 6.420 is 6 ones, 4 tenths, 2 hundredths, the same as 6.42. So <b>6.42 = 6.420</b>."
        else:
            wrong = ["%s %s %s" % (a, flip[sign], b), "%s = %s" % (a, b), "%s %s %s" % (b, sign, a)]
            big, small = (a, b) if A > B else (b, a)
            pa, pb = pad([a, b])
            i = first_diff(a, b)
            e = ("Write both with the same number of places: %s and %s. The first different place is the %s: %d and %d. "
                 "So <b>%s</b>." % (pa, pb, PLACE[i], digit_at(a, i), digit_at(b, i), right))
            if len(small) > len(big):
                e += " %s has more digits, but it is still less." % small
        its.append(mcq("Which comparison is true?", right, wrong, e))
    # order (5)
    stories = [
        ("Rain fell on three days: %s in., %s in. and %s in.", ["0.35", "0.305", "0.4"], "in.", True),
        ("Three long jumps measured %s m, %s m and %s m.", ["3.08", "3.8", "3.18"], "m", True),
        ("Three beetles are %s cm, %s cm and %s cm long.", ["1.25", "1.205", "1.3"], "cm", True),
        ("In a 60-meter race, three runners finished in %s seconds, %s seconds and %s seconds.", ["9.87", "9.8", "9.807"], "s", True),
        ("Three apples weigh %s kg, %s kg and %s kg.", ["0.215", "0.25", "0.2"], "kg", False),
    ]
    for t, three, u, up in stories:
        order = sorted(three, key=Dm, reverse=not up)
        fmt = lambda l: ", ".join(l)
        by_len = sorted(three, key=lambda x: (len(x), x), reverse=not up)            # "more digits is bigger"
        as_whole = sorted(three, key=lambda x: int(x.replace(".", "")), reverse=not up)   # ignoring the point
        cands = [fmt(by_len), fmt(as_whole), fmt(order[::-1]), fmt([order[1], order[0], order[2]]),
                 fmt([order[0], order[2], order[1]])]
        pick = []
        for cc in cands:
            if cc != fmt(order) and cc not in pick:
                pick.append(cc)
        e = ("Write them with the same number of places: %s. Compare from the left. Order: <b>%s</b>."
             % (", ".join(pad(three)), fmt(order)))
        if fmt(by_len) != fmt(order):
            e += " The number with more digits is not always greater."
        q = (t % tuple(three)) + " Which list shows them from %s?" % ("least to greatest" if up else "greatest to least")
        its.append(mcq(q, fmt(order), pick[:3], e))
    # between, misconception, not equal (3)
    its.append(mcq("Which number is between 0.6 and 0.7?", "0.68", ["0.068", "6.8", "0.076"],
                   "0.6 = 0.60 and 0.7 = 0.70. A number between them has <b>6 tenths</b> and more after it: 0.68 = 6 tenths 8 hundredths. "
                   "0.068 has 0 tenths, so it is less than 0.6."))
    n, he, his = P.next()
    its.append(mcq("%s says 0.125 is greater than 0.5 because 125 is greater than 5. Is %s right?" % (n, he),
                   "No, 0.125 is less", ["Yes, 0.125 is greater", "No, they are equal", "Yes, it has more digits"],
                   "Compare place by place, not the digits as whole numbers. 0.5 = 0.500. Tenths: 1 &lt; 5, so 0.125 &lt; 0.5. "
                   "<b>%s is not right.</b>" % n))
    its.append(mcq("Which number is <b>not</b> equal to 0.7?", "0.07", ["0.70", "0.700", "%s" % fr(7, 10)],
                   "0.70 and 0.700 only add zeros at the end, and %s is 7 tenths, so they all equal 0.7. "
                   "<b>0.07</b> is 7 hundredths, 10 times smaller." % fr(7, 10), same_value_ok=True))
    assert len(its) == 20, len(its)
    return {"title": "Compare and order decimals to thousandths", "items": its}


# ============================================================ set 5: round
QS = {0: Dm("1"), -1: Dm("0.1"), -2: Dm("0.01")}
QNAME = {0: "whole number", -1: "tenth", -2: "hundredth"}


def rd(x, i):
    return Dm(x).quantize(QS[i], rounding=ROUND_HALF_UP)


def round_e(x, i):
    x = Dm(x)
    r = rd(x, i)
    lo = x.quantize(QS[i], rounding=ROUND_DOWN)
    hi = lo + QS[i]
    nd = digit_at(x, i - 1)
    up = r > lo
    e = ("To the nearest %s, %s is between %s and %s. Look at the digit just to the right of the %s place: %d. "
         % (QNAME[i], N(x), K(lo), K(hi), PLACE[i], nd))
    if nd == 5 and x == lo + QS[i] / 2:
        e += "It is exactly halfway, and 5 rounds up. "
    elif up:
        e += "%d is 5 or more, so round up. " % nd
    else:
        e += "%d is less than 5, so round down. " % nd
    if up and digit_at(x, i) == 9:
        e += "The %s digit is 9, so adding 1 regroups: %s + %s = %s. " % (PLACE[i], K(lo), K(QS[i]), K(r))
    e += "Answer: <b>%s</b>." % K(r)
    if i < 0 and K(r).endswith("0"):
        e += " Keep the 0 at the end to show the number is rounded to the %s." % QNAME[i]
    return e


def set_round(P):
    its = []
    # with a number line (5)
    for x, i, wrong in [("3.46", -1, ["3.4", "3.46", "4"]), ("7.38", 0, ["8", "7.4", "7.3"]),
                        ("2.735", -2, ["2.73", "2.7", "2.8"]), ("0.65", -1, ["0.6", "0.66", "1"]),
                        ("4.96", -1, ["4.9", "4.10", "5.9"])]:
        x = Dm(x)
        lo = x.quantize(QS[i], rounding=ROUND_DOWN)
        q = fig(number_line_svg(lo, lo + QS[i], x)) + "Round %s to the nearest %s." % (N(x), QNAME[i])
        r = K(rd(x, i))
        if r in wrong:
            raise AssertionError((x, r))
        e = round_e(x, i)
        its.append(mcq(q, r, wrong, e, same_value_ok=(r == "5.0")))
    # without a picture (6)
    for x, i, wrong, note in [
            ("3.995", -2, ["3.99", "3.910", "3.9"], ""),
            ("6.849", -1, ["6.9", "6.85", "7"], " Do not round in steps (6.849 → 6.85 → 6.9). Look only at the hundredths digit."),
            ("0.462", -2, ["0.47", "0.5", "0.4"], ""),
            ("12.508", 0, ["12", "12.5", "12.51"], ""),
            ("9.96", -1, ["9.9", "9.10", "9.0"], ""),
            ("0.073", -1, ["0.07", "0.7", "0.08"], "")]:
        r = K(rd(x, i))
        same = r in ("4.00", "10.0")
        its.append(mcq("Round %s to the nearest %s." % (x, QNAME[i]), r, wrong, round_e(x, i) + note, same_value_ok=same))
    # word problems (9)
    n1 = P.next()
    words_ = [
        ("A swimmer's time was 14.387 seconds. What is the time rounded to the nearest hundredth of a second?",
         "14.387", -2, " seconds", ["14.38", "14.4", "14.3"]),
        ("Gas costs $3.459 per gallon. What is the price rounded to the nearest cent (hundredth of a dollar)?",
         "3.459", -2, "$", ["3.45", "3.50", "3.40"]),
        ("%s's pencil is 17.65 cm long. How long is it to the nearest whole centimeter?" % n1[0],
         "17.65", 0, " cm", ["17", "17.7", "17.6"]),
        ("A puppy weighs 4.548 kg. What is its weight rounded to the nearest tenth of a kilogram?",
         "4.548", -1, " kg", ["4.6", "4.55", "5"]),
        ("A trail is 2.96 miles long. What is its length to the nearest tenth of a mile?",
         "2.96", -1, " miles", ["2.9", "2.10", "2.0"]),
        ("This month, 3.075 inches of rain fell. What is that rounded to the nearest hundredth of an inch?",
         "3.075", -2, " inches", ["3.07", "3.1", "3.0"]),
        ("A runner finished a race in 58.249 seconds. What is the time to the nearest tenth of a second?",
         "58.249", -1, " seconds", ["58.3", "58.25", "58"]),
    ]
    for q, x, i, u, wrong in words_:
        r = K(rd(x, i))
        f = (lambda v: "$" + v) if u == "$" else (lambda v, u=u: v + u)
        e = round_e(x, i)
        if x == "4.548":
            e += " Do not round in steps (4.548 → 4.55 → 4.6)."
        if x == "58.249":
            e += " Do not round in steps (58.249 → 58.25 → 58.3)."
        if u == "$":
            e = e.replace("Answer: <b>%s</b>." % r, "Answer: <b>$%s</b>." % r)
            e += " A cent is a hundredth of a dollar."
        its.append(mcq(q, f(r), [f(w) for w in wrong], e))
    its.append(mcq("A bag of nuts weighs about 1.3 lb, rounded to the nearest tenth. Which could be the exact weight?",
                   "1.26 lb", ["1.35 lb", "1.24 lb", "1.39 lb"],
                   "Numbers from 1.25 up to (but not including) 1.35 round to 1.3. <b>1.26</b> is in that range. "
                   "1.35 and 1.39 round up to 1.4, and 1.24 rounds down to 1.2."))
    its.append(mcq("A scale shows 6.482 kg. A label rounds it to 6.5 kg. To which place was it rounded?", "nearest tenth",
                   ["nearest hundredth", "nearest whole number", "nearest thousandth"],
                   "6.5 has one digit after the point, so it is rounded to the <b>nearest tenth</b>: 6.482 is between 6.4 and 6.5, and the "
                   "hundredths digit is 8, so it rounds up to 6.5. To the nearest hundredth it would be 6.48, and to the nearest whole number 6."))
    assert len(its) == 20, len(its)
    return {"title": "Round decimals and word problems", "items": its}


# ============================================================ lesson
def body_html():
    f_chart = chart_svg("4.725", hi=-2)
    f_line = number_line_svg("2.73", "2.74", "2.736")
    return (
        "<h2>Each place is 10 times the place to its right</h2>"
        "<p>Moving one place to the <b>left</b> makes a digit worth <b>10 times as much</b>. Moving one place to the "
        "<b>right</b> makes it worth <b>%s as much</b>. This works on both sides of the decimal point.</p>" % fr(1, 10) +
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>In 4.725 the 2 is in the hundredths place, so its value is 2 hundredths = 0.02. "
        "The 7 is worth 0.7, which is 10 times as much as 0.07.</figcaption></figure>"
        "<p>Places to the right of the point end in <b>-ths</b>: tenths, hundredths, thousandths. "
        "A thousandth is tiny (0.001); a thousand is big (1,000).</p>"
        "<h2>Powers of 10 and exponents</h2>"
        "<p>The <b>exponent</b> tells how many 10s are multiplied. It is also the number of zeros.</p>" +
        table(["Power of 10", "Means", "Value", "Multiply: point moves", "Divide: point moves"], [
            [sup(1), "10", "10", "1 place right", "1 place left"],
            [sup(2), "10 × 10", "100", "2 places right", "2 places left"],
            [sup(3), "10 × 10 × 10", "1,000", "3 places right", "3 places left"],
            [sup(4), "10 × 10 × 10 × 10", "10,000", "4 places right", "4 places left"],
        ]) +
        ex("Example", "36 × %s and 4.7 ÷ %s" % (sup(2), sup(2)),
           "× 100: the point moves 2 places right: 36 → 3,600. ÷ 100: the point moves 2 places left: 4.7 → 0.047.",
           "3,600 and 0.047") +
        "<h2>Three ways to write a decimal</h2>" +
        table(["Form", "3.045"], [
            ["Standard form", "3.045"],
            ["Word form", "three and forty-five thousandths"],
            ["Expanded form", expanded("3.045")],
        ]) +
        "<p>In word form, say <b>“and” only for the decimal point</b>. Read the digits after the point as a whole number, "
        "then name the <b>last</b> place: 0.045 is forty-five <b>thousandths</b>.</p>"
        "<h2>Compare decimals</h2>"
        "<p>Line up the decimal points. Write zeros at the end so both numbers have the same number of places. "
        "Then compare from the left.</p>" +
        ex("Compare", "0.5 ☐ 0.502",
           "0.5 = 0.500. Tenths: 5 = 5. Hundredths: 0 = 0. Thousandths: 0 &lt; 2.", "0.5 &lt; 0.502") +
        "<h2>Round decimals</h2>"
        "<ol class='rk-step'><li>Find the place you are rounding to.</li>"
        "<li>Look at the digit <b>just to its right</b>.</li>"
        "<li><b>5 or more</b>: round up. <b>4 or less</b>: keep the digit.</li>"
        "<li>Drop the digits after the rounding place.</li></ol>"
        "<figure class='sn-fig'>" + f_line +
        "<figcaption>2.736 is between 2.73 and 2.74, and closer to 2.74. The thousandths digit is 6, so 2.736 rounds to 2.74.</figcaption></figure>" +
        table(["Round 6.849 to the nearest", "Look at", "Answer"], [
            ["whole number", "8 tenths", "7"],
            ["tenth", "4 hundredths", "6.8"],
            ["hundredth", "9 thousandths", "6.85"],
        ]) +
        ex("Watch the 9s", "Round 3.995 to the nearest hundredth.",
           "The hundredths digit is 9 and the next digit is 5, so round up: 3.99 + 0.01 = 4.00. Keep both zeros.", "4.00") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["0.125 &gt; 0.5 because it has more digits", "Compare place by place: 0.125 &lt; 0.500"],
            ["Reading 0.045 as forty-five hundredths", "Name the last place: forty-five thousandths"],
            ["%s = 30" % sup(3), "%s = 10 × 10 × 10 = 1,000" % sup(3)],
            ["4.7 ÷ 100 = 470", "Dividing makes it smaller: move the point left, 0.047"],
            ["6.849 → 6.85 → 6.9", "Look only at the next digit: 6.8"],
            ["Rounding 3.995 to 3.99 (cutting off digits)", "Round up when the next digit is 5 or more: 4.00"],
        ])
    )


FAQ = [
    {"q": "How do you read decimals to the thousandths?",
     "a": "Say the whole number, say “and” for the decimal point, read the digits after the point as a whole number, then name the last place. 3.045 is “three and forty-five thousandths”."},
    {"q": "How do you compare decimals like 0.5 and 0.49?",
     "a": "Write them with the same number of places (0.50 and 0.49) and compare from the left. 5 tenths is more than 4 tenths, so 0.5 &gt; 0.49, even though 0.49 has more digits."},
    {"q": "What is an exponent in 5th grade math?",
     "a": "An exponent shows how many 10s are multiplied: 10<sup>3</sup> = 10 × 10 × 10 = 1,000. Multiplying by 10<sup>3</sup> moves the decimal point 3 places to the right; dividing moves it 3 places to the left."},
    {"q": "How do you round a decimal to the nearest hundredth?",
     "a": "Look at the thousandths digit. If it is 5 or more, add 1 to the hundredths digit; if it is 4 or less, keep it. 2.736 rounds to 2.74, and 3.995 rounds to 4.00."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (wide charts and number lines) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(511)
    P = People(rnd)
    sets = [set_value(), set_powers(), set_forms(), set_compare(P), set_round(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "decimal-place-value-rounding", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimal Place Value, Powers of 10, Comparing and Rounding Decimals",
        "seo_title": "Grade 5 Decimal Place Value Worksheets: Thousandths, Powers of 10 and Exponents, Comparing and Rounding Decimals",
        "short_title": "Decimal place value and rounding",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "5.NBT.A.1–4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NBT/A/",
        "standard_text": "Recognize that in a multi-digit number, a digit in one place represents 10 times as much as it represents in the place to its right and 1/10 of what it represents in the place to its left. Explain patterns in the number of zeros of the product when multiplying a number by powers of 10, and explain patterns in the placement of the decimal point when a decimal is multiplied or divided by a power of 10. Use whole-number exponents to denote powers of 10. Read, write, and compare decimals to thousandths. Use place value understanding to round decimals to any place.",
        "meta_desc": "Free Grade 5 decimal place value worksheets: value of a digit to thousandths, 10 times and 1/10 as much, powers of 10 with exponents, word form and expanded form, comparing and ordering decimals, and rounding with number lines. 100 practice questions with answers.",
        "key_big": "Each place is worth 10 times the place to its right. Line up the decimal points to compare, and look one place to the right to round.",
        "key_sub": "0.7 is 10 times 0.07. 10<sup>3</sup> = 1,000 moves the point 3 places. 0.5 &gt; 0.125 even with fewer digits, and 3.995 rounds to 4.00 at the nearest hundredth.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(place-value chart|number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
