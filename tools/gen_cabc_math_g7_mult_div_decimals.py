# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Multiplying and Dividing Decimals (BC Mathematics Curriculum, Computational fluency:
operations with decimals)
  python3 tools/gen_cabc_math_g7_mult_div_decimals.py
Multiply decimals and count the decimal places (0.3 × 0.2 = 0.06, not 0.6), divide decimals by whole numbers
(long division, the point straight above the point), divide by a decimal (move the point the same number of
places in both numbers), estimate to place the decimal point, and word problems in BC contexts (gas price per
litre, sharing a bill). All arithmetic uses decimal.Decimal (never float). Wrong answers are real student
mistakes: counting only the larger number of decimal places, the point one place off, adding instead of
multiplying, dropping a place-holding zero (12.05 -> 12.5), writing a remainder as a digit, moving the point
only in the divisor, and multiplying instead of dividing.
Figures are copied from gen_us_math_g5_mul_div_decimals.py (hundredths grid) and
gen_us_math_g6_decimal_operations.py (columns, long division, moving both points).
BC style: Canadian English, $ and the cent sign, metric units, 4-digit numbers without a separator,
5 or more digits with a no-break space. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written only to hold a place
THIN = "#8a8a8a"
YEL = "#f7e08a"        # columns of the first factor
BLUE = "#a9cbef"       # rows of the second factor
BOTH = "#3f9a63"       # overlap = the product
FONT = "Arial, Helvetica, sans-serif"
NB = " "


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text, BC style: 4536, 12 350 (no-break space), 0.045."""
    d = Dm(str(x).replace(NB, "")).normalize()
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
    """Money: $72, $21.60. None if x is not a whole number of cents (so it cannot be a price)."""
    d = Dm(x)
    if d <= 0 or d != d.quantize(Dm("0.01")):
        return None
    if d == d.to_integral_value() and d >= 10:
        return "$" + N(d)
    return "$" + N(int(d)) + "." + format(d.quantize(Dm("0.01")), "f").split(".")[1]


def places(x):
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


def digits_of(x):
    """'2.35' -> 235 (the number without its point)."""
    return int(str(x).replace(".", ""))


def fixed(x, p):
    return format(Dm(x).quantize(Dm(1).scaleb(-p)), "f")


def pl(k, one, many=None):
    return "%s %s" % (N(k), one if Dm(k) == 1 else (many or one + "s"))


VAL = re.compile(r"^(?:about )?(\$)?([\d" + NB + r"]*\.?\d+)(?: ([a-zA-Z]+))?$")


def val(c):
    """(value, unit) of a choice; None if it is not a single number."""
    m = VAL.match(c)
    if not m:
        return None
    return (Dm(m.group(2).replace(NB, "")), "$" if m.group(1) else (m.group(3) or ""))


# ------------------------------------------------------------ mistakes
def mul_cands(a, b):
    """Counted only the larger number of places (0.3 × 0.2 -> 0.6), point one place off, added, two places off."""
    p = Dm(a) * Dm(b)
    k, m = places(a) + places(b), max(places(a), places(b))
    return [p.scaleb(k - m) if k != m else None, p * 10, p / 10, Dm(a) + Dm(b), p * 100, p / 100]


def drop_zero(q):
    """Skipped a 0 in the quotient: 1.02 -> 1.2."""
    s = format(Dm(q).normalize(), "f")
    i = next(j for j, ch in enumerate(s) if ch not in "0.")
    j = s.find("0", i)
    if j < 0 or j == len(s) - 1:
        return None
    return Dm(s[:j] + s[j + 1:])


def rem_digit(a, d):
    """Stopped at the last digit and wrote the remainder as the next digit: 7.5 ÷ 4 -> 1.83."""
    k = places(a)
    q, r = divmod(digits_of(a), d)
    if r == 0 or r > 9:
        return None
    return Dm(q * 10 + r).scaleb(-k - 1)


def stop_early(a, d):
    k = places(a)
    q, r = divmod(digits_of(a), d)
    return Dm(q).scaleb(-k) if r else None


def divw_cands(a, d):
    q = Dm(a) / d
    return [drop_zero(q), rem_digit(a, d), stop_early(a, d), q * 10, q / 10, Dm(a) * d]


def divd_cands(a, b):
    q = Dm(a) / Dm(b)
    k = places(b)
    c = [q / 10 ** k]                                       # moved the point only in the divisor
    if places(a) < k:
        c.append(q / 10 ** (k - places(a)))                 # did not write zeros in the dividend
    c += [q * 10, q / 10, Dm(a) * Dm(b), q * 100]
    return c


def nums(vals, unit=""):
    return [None if v is None else (N(v) + unit) for v in vals]


def monies(vals):
    return [None if v is None else M(v) for v in vals]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, text_ok=False):
    """4 choices: correct + the first 3 candidates with a different value. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    vals = [val(correct)]
    if not text_ok:
        assert vals[0] is not None and vals[0][0] > 0, (q, correct)
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        v = val(c)
        if c in seen or (v and v in vals) or (v and v[0] <= 0):
            continue
        if not text_ok and v is None:
            continue
        seen.add(c)
        vals.append(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def point_mark(x, y, fs, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, y - fs * 0.06, fs * 0.1, col)


# ------------------------------------------------------------ figure: tenths × tenths on a hundredths grid
def grid_lines(ox, oy, cell):
    s = []
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, INK))
    return "".join(s)


def overlap_svg(a, b, cell=18):
    """a tenths (columns, yellow) × b tenths (rows, blue). The overlap (a·b squares, dark green) is the product."""
    L, T = 44, 30
    s = []
    for c in range(10):
        for r in range(10):
            col = BOTH if (c < a and r < b) else YEL if c < a else BLUE if r < b else None
            if col:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (L + c * cell, T + r * cell, cell, cell, col))
    s.append(grid_lines(L, T, cell))
    x1, x2 = L, L + a * cell
    s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x1, T - 2, T - 8, x2, T - 2, INK))
    s.append(text((x1 + x2) / 2.0, T - 12, "0.%d" % a, 16))
    y1, y2 = T, T + b * cell
    s.append("<path d='M%d %d H%d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (L - 2, y1, L - 8, y2, L - 2, INK))
    s.append(text(L - 11, (y1 + y2) / 2.0 + 6, "0.%d" % b, 16, "end"))
    W, H = L + 10 * cell + 4, T + 10 * cell + 4
    return svg_wrap(W, H, "".join(s), "hundredths grid: 0.%d of the columns and 0.%d of the rows shaded, overlap %d squares"
                    % (a, b, a * b))


# ------------------------------------------------------------ figure: multiplication in columns
def mul_svg(rows, rules, label, fs=26, colors=None):
    """Multiplication written in columns, lined up on the RIGHT (points are not lined up)."""
    cw = fs * 0.9
    lens = [len(t.replace(".", "")) for sg, t in rows]
    signed = max([n for (sg, t), n in zip(rows, lens) if sg] or [0])
    sign_slot = max(max(lens), signed + 1)
    slots = sign_slot + 1
    W = int(cw * slots + 20)
    gap = fs * 1.2
    H = int(10 + gap * len(rows) + 4 * len(rules) + 10)
    right = W - 10
    s = []
    y = 10
    for r, (sg, t) in enumerate(rows):
        y += gap
        col = (colors or {}).get(r, INK)
        slot = 0
        for ch in reversed(t):
            if ch == ".":
                s.append(point_mark(right - cw * slot, y, fs, col))
                continue
            s.append(text(right - cw * (slot + 0.5), y - 2, ch, fs, col=col))
            slot += 1
        if sg:
            s.append(text(right - cw * (sign_slot + 0.5), y - 2, sg, fs, col=GREEN))
        if r in rules:
            y += 4
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
    return svg_wrap(W, H, "".join(s), label, "monospace")


def mul_digits_svg(a, b):
    """a × b in columns with the whole-number product written but no decimal point in it."""
    raw = digits_of(a) * digits_of(b)
    return mul_svg([("", a), ("×", b), ("", str(raw))], [1],
                   "%s times %s written in columns, with the product digits %d but no decimal point" % (a, b, raw),
                   colors={2: GREEN})


# ------------------------------------------------------------ figure: long division
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


# ------------------------------------------------------------ figure: move both decimal points
def shift_svg(a, b, fs=24):
    """a ÷ b as long division. Both decimal points hop the same number of places to the right
    (red arrows below the digits). Zeros written to make room are grey. Under it: the new problem."""
    k = places(b)
    A, B = Dm(a) * 10 ** k, Dm(b) * 10 ** k
    assert B == int(B)
    need = max(places(a), k)
    da = fixed(a, need)
    ghost_a = need - places(a)
    dda = da.replace(".", "")
    ddb = b.replace(".", "")
    pa = len(da.split(".")[0])
    pb = len(b.split(".")[0])
    cw = fs * 0.95
    rh = fs * 1.25
    top = 10
    by = top + rh - fs * 0.18
    s = []
    bx = 12
    x0 = bx + cw * len(ddb) + 22
    for j, ch in enumerate(ddb):
        s.append(text(bx + cw * (j + 0.5), by, ch, fs, col=GREEN))
    for j, ch in enumerate(dda):
        s.append(text(x0 + cw * (j + 0.5), by, ch, fs, col=GHOST if j >= len(dda) - ghost_a else INK))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * len(dda) + 12
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))

    def hop(xl, n, show_old=True):
        x1, x2 = xl, xl + cw * n
        yb = by + 6
        if show_old:
            s.append(point_mark(x1, by, fs, GHOST))
        s.append(point_mark(x2, by, fs, RED))
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (x1, yb, (x1 + x2) / 2, yb + 16, x2 - 2, yb + 3, RED))
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>"
                 % (x2 + 1, yb + 1, x2 - 8, yb + 1, x2 - 3, yb + 8, RED))
    hop(bx + cw * pb, k)
    hop(x0 + cw * pa, k, show_old=places(a) > 0)
    ty = by + 26 + fs
    s.append(text(W / 2.0, ty, "%s ÷ %s" % (N(A), N(B)), fs, col=GREEN))
    H = ty + 10
    label = "%s divided by %s: both decimal points move %s to the right, giving %s divided by %s" % (
        a, b, pl(k, "place"), N(A), N(B))
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


# ------------------------------------------------------------ explanations
def mul_e(a, b, tail=""):
    ra, rb = digits_of(a), digits_of(b)
    raw = ra * rb
    k = places(a) + places(b)
    ans = Dm(a) * Dm(b)
    e = "Multiply as whole numbers: %s × %s = %s. " % (N(ra), N(rb), N(raw))
    if k == 0:
        return e + tail
    written = str(raw).rjust(k + 1, "0")
    written = written[:-k] + "." + written[-k:]
    e += "Count the decimal places: %d + %d = %d. " % (places(a), places(b), k)
    e += "Count %s from the right" % pl(k, "place")
    if len(str(raw)) <= k:
        e += " (write zeros in front to make room)"
    if N(ans) != written:
        e += ": %s = <b>%s</b>." % (written, N(ans))
    else:
        e += ": <b>%s</b>." % written
    return e + (" " + tail if tail else "")


def divw_e(a, d, tail=""):
    q = Dm(a) / d
    need = max(places(a), places(N(q)))
    e = "Divide as with whole numbers. Put the point in the quotient straight above the point in the dividend. "
    if need > places(a):
        e += "When the digits run out, write zeros (%s = %s) and keep dividing. " % (a, fixed(a, need))
    if drop_zero(q) is not None:
        e += "When %d does not fit, write 0 in the quotient. " % d
    e += "%s ÷ %d = <b>%s</b>. Check: %s × %d = %s." % (a, d, N(q), N(q), d, a)
    return e + (" " + tail if tail else "")


def divd_e(a, b, tail=""):
    k = places(b)
    m = 10 ** k
    A, B = Dm(a) * m, Dm(b) * m
    q = Dm(a) / Dm(b)
    zeros = ""
    if places(a) < k:
        zeros = " (write %s in %s)" % ("a zero" if k - places(a) == 1 else "zeros", a)
    e = ("%s has %s, so move <b>both</b> decimal points %s to the right%s. "
         "%s ÷ %s = %s ÷ %s = <b>%s</b>. Check: %s × %s = %s."
         % (b, pl(k, "decimal place"), pl(k, "place"), zeros, N(a), b, N(A), N(B), N(q), N(q), b, N(a)))
    return e + (" " + tail if tail else "")


# ============================================================ set 1: multiply decimals
def set_multiply():
    its = []
    # grid models
    assert Dm("0.3") * Dm("0.2") == Dm("0.06")
    its.append(mcq(fig(overlap_svg(3, 2)) + "The dark squares show 0.3 × 0.2. What is 0.3 × 0.2?", "0.06",
                   ["0.6", "0.5", "0.006"],
                   "3 tenths × 2 tenths = 6 <b>hundredths</b>: 6 of the 100 small squares are dark. 0.3 × 0.2 = <b>0.06</b>. "
                   "0.6 is the common mistake: 1 + 1 = 2 decimal places, so the answer needs 2 places. 0.5 adds."))
    assert Dm("0.4") * Dm("0.7") == Dm("0.28")
    its.append(mcq(fig(overlap_svg(4, 7)) + "The dark squares show 0.4 × 0.7. What is 0.4 × 0.7?", "0.28",
                   ["2.8", "1.1", "0.028"],
                   "4 columns × 7 rows = 28 dark squares out of 100, so 0.4 × 0.7 = <b>0.28</b>. "
                   "The answer is less than both 0.4 and 0.7, so 2.8 cannot be right. 1.1 adds."))
    # whole × decimal
    its.append(mcq("6 × 0.4 = ?", "2.4", nums([Dm(24), Dm("0.24"), Dm("6.4")]),
                   mul_e("6", "0.4", "24 forgets the decimal point. 6.4 adds instead of multiplying.")))
    its.append(mcq("9 × 0.07 = ?", "0.63", nums([Dm("6.3"), Dm("0.063"), Dm("9.07")]),
                   mul_e("9", "0.07", "6.3 counts only 1 place, but 0.07 has 2.")))
    its.append(mcq("25 × 0.32 = ?", "8", nums(mul_cands("25", "0.32")),
                   mul_e("25", "0.32", "Count the places before you drop the zeros: 8.00 = 8.")))
    # decimal × decimal
    assert Dm("0.5") * Dm("0.8") == Dm("0.4")
    its.append(mcq("0.5 × 0.8 = ?", "0.4", ["4", "0.04", "1.3"],
                   mul_e("0.5", "0.8", "0.04 drops the zero first and then counts 2 places: count before you drop zeros. "
                         "Or think: half of 0.8 is 0.4.")))
    its.append(mcq("How many decimal places does 2.35 × 0.4 have before you drop any zeros?", "3", ["2", "1", "4"],
                   "2.35 has 2 decimal places and 0.4 has 1. The product has <b>2 + 1 = 3</b> places: "
                   "235 × 4 = 940, so 2.35 × 0.4 = 0.940 = 0.94. 2 only uses the larger number of places."))
    for a, b in [("1.2", "0.3"), ("0.06", "0.4"), ("2.5", "1.4"), ("0.07", "0.9")]:
        its.append(mcq("%s × %s = ?" % (a, b), N(Dm(a) * Dm(b)), nums(mul_cands(a, b)), mul_e(a, b)))
    # columns: product digits given
    assert Dm("2.35") * Dm("1.4") == Dm("3.29")
    its.append(mcq(fig(mul_digits_svg("2.35", "1.4")) + "235 × 14 = 3290. Where does the decimal point go in 2.35 × 1.4?",
                   "3.29", nums([Dm("32.9"), Dm("0.329"), Dm("329")]),
                   mul_e("2.35", "1.4", "Estimate: 2 × 1.5 = 3, so 3.29 makes sense. 32.9 counts only 2 places.")))
    assert Dm("1.6") * Dm("0.35") == Dm("0.56")
    its.append(mcq(fig(mul_digits_svg("1.6", "0.35")) + "16 × 35 = 560. What is 1.6 × 0.35?", "0.56",
                   nums([Dm("5.6"), Dm("0.056"), Dm("56")]),
                   mul_e("1.6", "0.35", "0.056 drops the zero before counting: count 3 places in 560 first.")))
    for a, b in [("3.6", "0.25"), ("4.05", "1.2"), ("12.5", "0.08"), ("0.15", "0.6")]:
        its.append(mcq("%s × %s = ?" % (a, b), N(Dm(a) * Dm(b)), nums(mul_cands(a, b)), mul_e(a, b)))
    assert Dm(48) * 26 == 1248 and Dm("4.8") * Dm("0.26") == Dm("1.248")
    its.append(mcq("48 × 26 = 1248. Use this to find 4.8 × 0.26.", "1.248", ["12.48", "0.1248", "124.8"],
                   "4.8 has 1 decimal place and 0.26 has 2, so the product has 3: <b>1.248</b>. "
                   "Estimate: 5 × 0.25 = 1.25, which is close."))
    vals = {"7.5 × 0.96": Dm("7.5") * Dm("0.96"), "7.5 × 1.04": Dm("7.5") * Dm("1.04"),
            "7.5 × 1": Dm("7.5"), "7.5 × 2.3": Dm("7.5") * Dm("2.3")}
    assert [k for k, v in vals.items() if v < Dm("7.5")] == ["7.5 × 0.96"]
    its.append(mcq("Without multiplying, which product is <b>less than 7.5</b>?", "7.5 × 0.96",
                   ["7.5 × 1.04", "7.5 × 1", "7.5 × 2.3"],
                   "Compare the other number with 1. Only 0.96 is less than 1, so only <b>7.5 × 0.96</b> is less than 7.5 "
                   "(it is 7.2). 7.5 × 1 is exactly 7.5.", text_ok=True))
    assert Dm("0.9") * Dm("0.5") == Dm("0.45")
    its.append(mcq("Jasleen says 0.9 × 0.5 = 4.5. What is the correct answer?", "0.45", ["4.5", "0.045", "1.4"],
                   "9 × 5 = 45, and 1 + 1 = 2 decimal places, so 0.9 × 0.5 = <b>0.45</b>. "
                   "Half of 0.9 is 0.45. Jasleen counted only 1 place. A product of two numbers less than 1 is less than both."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 5, 6, 7, 4, 8, 10, 9, 11, 12, 13, 14, 16, 15, 17, 18, 19]
    return {"title": "Multiply decimals: count the decimal places", "items": [its[i] for i in order]}


# ============================================================ set 2: divide by a whole number
def set_div_whole():
    its = []
    its.append(mcq("0.8 ÷ 4 = ?", "0.2", ["2", "0.02", "3.2"], divw_e("0.8", 4, "3.2 multiplies instead of dividing.")))
    its.append(mcq("6.3 ÷ 3 = ?", "2.1", ["21", "0.21", "2.3"], divw_e("6.3", 3, "2.3 divides only the 6 and forgets the 3 tenths.")))
    its.append(mcq("9.6 ÷ 4 = ?", "2.4", nums(divw_cands("9.6", 4)), divw_e("9.6", 4)))
    its.append(mcq("4.08 ÷ 4 = ?", "1.02", nums(divw_cands("4.08", 4)),
                   divw_e("4.08", 4, "1.2 drops the 0 that holds the tenths place.")))
    for a, d in [("7.38", 3), ("5.85", 5), ("0.954", 9)]:
        q = Dm(a) / d
        raw = int(q * 10 ** places(a))
        its.append(mcq(fig(ld_svg(a, d, quot="digits")) + "The quotient digits are written, but the point is missing. "
                       "What is %s ÷ %d?" % (a, d), N(q), nums([q * 10, q / 10, Dm(raw), drop_zero(q)]),
                       divw_e(a, d, "The point goes straight above the point in %s." % a)))
    for a, d in [("18.72", 6), ("25.38", 9)]:
        its.append(mcq(fig(ld_svg(a, d)) + "Divide.", N(Dm(a) / d), nums(divw_cands(a, d)), divw_e(a, d)))
    for a, d in [("7.5", 4), ("3.3", 6), ("9", 8), ("45.6", 12), ("86.4", 24), ("0.912", 16), ("30.15", 5), ("2.736", 8)]:
        its.append(mcq("%s ÷ %d = ?" % (a, d), N(Dm(a) / d), nums(divw_cands(a, d)), divw_e(a, d)))
    assert Dm("2.1") / 4 == Dm("0.525")
    its.append(mcq("Kai is dividing 2.1 ÷ 4. He has written 0.5 in the quotient, and 1 tenth is left. What should he do next?",
                   "Write a 0 and keep dividing",
                   ["Write the answer as 0.51", "Stop: the answer is 0.5", "Start again with 4 ÷ 2.1"],
                   "2.1 = 2.10 = 2.100, so writing zeros does not change the number. <b>Write a 0 and keep dividing</b>: "
                   "10 hundredths ÷ 4 = 2, 2 left; 20 thousandths ÷ 4 = 5. So 2.1 ÷ 4 = 0.525. "
                   "0.51 writes the remainder as a digit.", text_ok=True))
    assert Dm("4.55") * 3 == Dm("13.65")
    its.append(mcq("Which multiplication checks that 13.65 ÷ 3 = 4.55?", "4.55 × 3",
                   ["13.65 × 3", "4.55 × 13.65", "3 × 3"],
                   "Quotient × divisor = dividend. <b>4.55 × 3</b> = 13.65, so the division is right.", text_ok=True))
    assert Dm("9.45") / 5 == Dm("1.89")
    its.append(mcq("Ryan says 9.45 ÷ 5 = 18.9. Use an estimate to check. What is the correct answer?", "1.89",
                   ["18.9", "0.189", "47.25"],
                   "Estimate: 10 ÷ 5 = 2, so the answer is about 2, not about 19. 9.45 ÷ 5 = <b>1.89</b>. "
                   "Check: 1.89 × 5 = 9.45. 47.25 multiplies."))
    assert len(its) == 20
    order = [0, 1, 2, 4, 5, 3, 6, 7, 8, 18, 9, 10, 11, 12, 17, 13, 14, 16, 15, 19]
    return {"title": "Divide decimals by whole numbers", "items": [its[i] for i in order]}


# ============================================================ set 3: divide by a decimal
def set_div_dec():
    its = []
    for a, b in [("3.36", "0.14"), ("1.5", "0.25"), ("2.24", "0.7"), ("6", "0.4")]:
        q = Dm(a) / Dm(b)
        its.append(mcq(fig(shift_svg(a, b)) + "Both decimal points move the same number of places. What is %s ÷ %s?" % (a, b),
                       N(q), nums(divd_cands(a, b)), divd_e(a, b)))
    for a, b, right, wrong in [("7.35", "0.5", "73.5 ÷ 5", ["7.35 ÷ 5", "735 ÷ 5", "73.5 ÷ 0.5"]),
                               ("0.18", "0.006", "180 ÷ 6", ["18 ÷ 6", "0.18 ÷ 6", "1.8 ÷ 6"]),
                               ("12", "0.75", "1200 ÷ 75", ["12 ÷ 75", "120 ÷ 75", "1200 ÷ 0.75"])]:
        k = places(b)
        A, B = Dm(a) * 10 ** k, Dm(b) * 10 ** k
        assert right == "%s ÷ %s" % (N(A), N(B))
        q = Dm(a) / Dm(b)
        e = ("%s has %s, so multiply both numbers by %s: %s → %s and %s → %s. %s ÷ %s = <b>%s</b> = %s. "
             "Move the point the <b>same</b> number of places in both numbers."
             % (b, pl(k, "decimal place"), N(10 ** k), a, N(A), b, N(B), a, b, right, N(q)))
        its.append(mcq("Which problem has the same answer as %s ÷ %s?" % (a, b), right, wrong, e, text_ok=True))
    for a, b in [("9.6", "0.8"), ("14.4", "2.4"), ("3.75", "1.5"), ("0.144", "0.12"), ("0.51", "0.3"),
                 ("27", "0.45"), ("6.5", "0.13"), ("52.2", "0.9"), ("2.85", "0.05"), ("7.2", "0.016")]:
        its.append(mcq("%s ÷ %s = ?" % (a, b), N(Dm(a) / Dm(b)), nums(divd_cands(a, b)), divd_e(a, b)))
    assert Dm(8) / Dm("0.4") == 20
    its.append(mcq("Without dividing, which is true about 8 ÷ 0.4?", "It is greater than 8",
                   ["It is less than 8", "It equals 2", "It equals 3.2"],
                   "0.4 is less than 1, and many groups of 0.4 fit into 8, so the answer is <b>greater than 8</b>. "
                   "8 ÷ 0.4 = 80 ÷ 4 = 20. (2 is 8 ÷ 4, and 3.2 is 8 × 0.4.)", text_ok=True))
    assert Dm("4.85") / 5 == Dm("0.97") and Dm("4.85") / Dm("0.5") == Dm("9.7")
    its.append(mcq("Wei wrote 4.85 ÷ 0.5 = 0.97. What mistake did he make?", "He moved the point only in 0.5",
                   ["He moved the point in both numbers", "He multiplied instead of dividing", "He made no mistake"],
                   "Wei changed 0.5 to 5 but left 4.85 as it was: 4.85 ÷ 5 = 0.97. <b>He moved the point only in 0.5</b>. "
                   "Move both: 4.85 ÷ 0.5 = 48.5 ÷ 5 = 9.7.", text_ok=True))
    assert Dm("4.56") / Dm("0.12") == Dm(456) / 12 == 38
    its.append(mcq("Why does 4.56 ÷ 0.12 have the same answer as 456 ÷ 12?", "Both numbers were multiplied by 100",
                   ["Only 0.12 was multiplied by 100", "Both numbers were divided by 100", "The zeros were dropped"],
                   "4.56 × 100 = 456 and 0.12 × 100 = 12. When <b>both numbers are multiplied by 100</b>, the answer does not "
                   "change, just as 6 ÷ 2 = 60 ÷ 20 = 3. Both give 38.", text_ok=True))
    assert len(its) == 20
    order = [0, 3, 1, 2, 4, 7, 8, 17, 5, 9, 10, 11, 6, 12, 13, 18, 14, 15, 16, 19]
    return {"title": "Divide by a decimal: move both points", "items": [its[i] for i in order]}


# ============================================================ set 4: estimate to place the decimal point
def set_estimate():
    its = []

    def place_q(expr, ans, digits, wrong, est):
        assert digits_of(N(ans)) == int(digits) or str(digits_of(N(ans))) == digits.lstrip("0"), (expr, ans, digits)
        return mcq("The digits of %s are %s. Use an estimate to place the decimal point. What is %s?" % (expr, digits, expr),
                   N(ans), wrong, "Estimate: %s. Only <b>%s</b> is close to that." % (est, N(ans)))

    assert Dm("4.8") * Dm("3.1") == Dm("14.88")
    its.append(place_q("4.8 × 3.1", Dm("14.88"), "1488", ["1.488", "148.8", "0.1488"], "5 × 3 = 15"))
    assert Dm("6.24") / Dm("0.8") == Dm("7.8")
    its.append(place_q("6.24 ÷ 0.8", Dm("7.8"), "78", ["0.78", "78", "780"],
                       "6.24 is about 6.4, and 6.4 ÷ 0.8 = 64 ÷ 8 = 8"))
    assert Dm("38.4") / Dm("1.6") == 24
    its.append(place_q("38.4 ÷ 1.6", Dm(24), "24", ["2.4", "240", "0.24"], "40 ÷ 2 = 20"))
    assert Dm("9.2") * Dm("0.48") == Dm("4.416")
    its.append(place_q("9.2 × 0.48", Dm("4.416"), "4416", ["44.16", "0.4416", "441.6"],
                       "9.2 is about 9 and 0.48 is about 0.5 (one half). Half of 9 is 4.5"))
    assert Dm("21.6") / Dm("4.5") == Dm("4.8")
    its.append(place_q("21.6 ÷ 4.5", Dm("4.8"), "48", ["48", "0.48", "480"], "20 ÷ 5 = 4"))
    assert Dm("0.36") * Dm("0.5") == Dm("0.18")
    its.append(place_q("0.36 × 0.5", Dm("0.18"), "18", ["1.8", "0.018", "18"],
                       "× 0.5 means half. Half of 0.36 is less than 0.36, and half of 0.4 is 0.2"))
    assert Dm("125.4") / Dm("3.8") == 33
    its.append(place_q("125.4 ÷ 3.8", Dm(33), "33", ["3.3", "330", "0.33"], "120 ÷ 4 = 30"))
    # best estimate
    assert abs(Dm("39.8") * Dm("0.49") - 20) < 1
    its.append(mcq("Which is the best estimate for <b>39.8 × 0.49</b>?", "20", ["2", "200", "80"],
                   "39.8 ≈ 40 and 0.49 ≈ 0.5. 40 × 0.5 = half of 40 = <b>20</b>. "
                   "80 is 40 ÷ 0.5: it divides instead of multiplying."))
    assert abs(Dm("31.8") / Dm("7.9") - 4) < Dm("0.1")
    its.append(mcq("Which is the best estimate for <b>31.8 ÷ 7.9</b>?", "4", ["0.4", "40", "24"],
                   "31.8 ≈ 32 and 7.9 ≈ 8. 32 ÷ 8 = <b>4</b>. 24 is 32 − 8: it subtracts instead of dividing."))
    assert abs(Dm("0.98") * Dm("52.3") - 52) < 2
    its.append(mcq("Which is the best estimate for <b>0.98 × 52.3</b>?", "52", ["5.2", "520", "0.52"],
                   "0.98 is almost 1, and 1 × 52.3 = 52.3. So the answer is just under 52.3: about <b>52</b>."))
    assert abs(Dm("5.1") / Dm("0.49") - 10) < 1
    its.append(mcq("Which is the best estimate for <b>5.1 ÷ 0.49</b>?", "10", ["1", "2.5", "100"],
                   "5.1 ≈ 5 and 0.49 ≈ 0.5. How many halves are in 5? <b>10</b>. "
                   "2.5 is 5 × 0.5: it multiplies instead of dividing."))
    assert abs(Dm("2.03") * Dm("7.9") - 16) < 1
    its.append(mcq("Which is the best estimate for <b>2.03 × 7.9</b>?", "16", ["1.6", "160", "10"],
                   "2.03 ≈ 2 and 7.9 ≈ 8. 2 × 8 = <b>16</b>. 10 is 2 + 8: it adds instead of multiplying."))
    # is it reasonable?
    assert Dm("0.4") * Dm("0.3") == Dm("0.12")
    its.append(mcq("Harjot says 0.4 × 0.3 = 1.2. Which statement is true?", "No: the answer must be less than 0.4",
                   ["Yes: 4 × 3 = 12", "No: the answer must be 12", "Yes: 0.4 + 0.3 is about 1"],
                   "0.3 is less than 1, so 0.4 × 0.3 is less than 0.4. <b>1.2 cannot be right.</b> "
                   "4 × 3 = 12 and 1 + 1 = 2 decimal places, so 0.4 × 0.3 = 0.12.", text_ok=True))
    assert Dm("12.6") / Dm("0.9") == 14
    its.append(mcq("Without dividing, which is true about 12.6 ÷ 0.9?", "It is greater than 12.6",
                   ["It is less than 12.6", "It equals 12.6", "It is less than 1"],
                   "0.9 is less than 1, so more than 12.6 groups of 0.9 fit into 12.6. The answer is "
                   "<b>greater than 12.6</b>: 12.6 ÷ 0.9 = 126 ÷ 9 = 14.", text_ok=True))
    vals = {"3.4 × 1.05": Dm("3.4") * Dm("1.05"), "3.4 × 0.95": Dm("3.4") * Dm("0.95"),
            "3.4 × 0.5": Dm("3.4") * Dm("0.5"), "3.4 × 1": Dm("3.4")}
    assert [k for k, v in vals.items() if v > Dm("3.4")] == ["3.4 × 1.05"]
    its.append(mcq("Without multiplying, which product is <b>greater than 3.4</b>?", "3.4 × 1.05",
                   ["3.4 × 0.95", "3.4 × 0.5", "3.4 × 1"],
                   "Only 1.05 is greater than 1, so only <b>3.4 × 1.05</b> is greater than 3.4 (it is 3.57). "
                   "3.4 × 1 is exactly 3.4.", text_ok=True))
    vals = {"6.3 ÷ 1.4": Dm("6.3") / Dm("1.4"), "6.3 ÷ 0.7": Dm("6.3") / Dm("0.7"),
            "6.3 ÷ 0.9": Dm("6.3") / Dm("0.9"), "6.3 ÷ 1": Dm("6.3")}
    assert [k for k, v in vals.items() if v < Dm("6.3")] == ["6.3 ÷ 1.4"]
    its.append(mcq("Without dividing, which quotient is <b>less than 6.3</b>?", "6.3 ÷ 1.4",
                   ["6.3 ÷ 0.7", "6.3 ÷ 0.9", "6.3 ÷ 1"],
                   "Dividing by a number greater than 1 makes the answer smaller. Only 1.4 is greater than 1, so "
                   "<b>6.3 ÷ 1.4</b> = 4.5 is less than 6.3. Dividing by 0.7 or 0.9 makes it bigger (9 and 7).", text_ok=True))
    assert Dm("7.6") * Dm("4.9") == Dm("37.24")
    its.append(mcq("Chloe works out 7.6 × 4.9 and gets 3.724. Use an estimate. What is the correct answer?", "37.24",
                   ["3.724", "372.4", "12.5"],
                   "Estimate: 8 × 5 = 40, so the answer is about 40. 76 × 49 = 3724, and 1 + 1 = 2 decimal places: "
                   "<b>37.24</b>. Chloe counted 3 places. 12.5 is the sum."))
    assert Dm("13.5") / Dm("0.45") == 30
    its.append(mcq("Owen works out 13.5 ÷ 0.45 and gets 3. Use an estimate. What is the correct answer?", "30",
                   ["3", "0.3", "300"],
                   "Estimate: 0.45 is about 0.5, and there are about 2 × 13.5 = 27 halves in 13.5, so the answer is "
                   "about 27. 13.5 ÷ 0.45 = 1350 ÷ 45 = <b>30</b>. Owen moved the point in 13.5 only 1 place."))
    assert Dm("0.25") * Dm("16.8") == Dm("4.2")
    its.append(mcq("Which is the best estimate for <b>0.25 × 16.8</b>?", "4", ["40", "0.4", "67"],
                   "0.25 is one quarter. A quarter of 16.8 is about a quarter of 16 = <b>4</b> (exactly 4.2). "
                   "67 is about 16.8 ÷ 0.25: it divides instead of multiplying."))
    assert abs(Dm("47.6") / Dm("12.2") - 4) < Dm("0.1")
    its.append(mcq("Which is the best estimate for <b>47.6 ÷ 12.2</b>?", "4", ["0.4", "40", "35"],
                   "47.6 ≈ 48 and 12.2 ≈ 12. 48 ÷ 12 = <b>4</b>. 35 is about 47.6 − 12.2 = 35.4: it subtracts instead of dividing."))
    assert len(its) == 20
    order = [7, 8, 11, 9, 0, 2, 4, 10, 12, 6, 1, 3, 5, 18, 19, 14, 15, 13, 16, 17]
    return {"title": "Estimate to place the decimal point", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words():
    its = []
    D = Dm
    # 1 gas: whole number of litres
    T = 40 * D("1.80")
    assert T == 72
    its.append(mcq("Gas costs $1.80 per litre. Liam’s dad buys 40 L. How much does he pay?", M(T),
                   ["$720", "$7.20", "$41.80"],
                   "40 × $1.80 = 40 × 180¢ = 7200¢ = <b>$72</b>. Estimate: 40 × $2 = $80, so $72 makes sense. "
                   "$41.80 adds instead of multiplying."))
    # 2 Terry Fox
    T = D("0.6") * 5
    assert T == 3
    its.append(mcq("The Terry Fox Run route at Nadia’s school is 5 km. She has run 0.6 of the route. How far has she run?",
                   N(T) + " km", ["30 km", "0.3 km", "5.6 km"],
                   "0.6 of 5 km means 0.6 × 5 = 6 tenths × 5 = 30 tenths = <b>3 km</b>. "
                   "30 km forgets that 0.6 is tenths. 5.6 km adds."))
    # 3 sharing a bill
    T = D("86.40") / 4
    assert T == D("21.60")
    its.append(mcq("Four friends share an $86.40 restaurant bill equally. How much does each friend pay?", M(T),
                   ["$2.16", "$216", "$345.60"],
                   "$86.40 ÷ 4: 8 ÷ 4 = 2, 6 ÷ 4 = 1 r 2, 24 ÷ 4 = 6, 0 ÷ 4 = 0. Each pays <b>$21.60</b>. "
                   "Estimate: $80 ÷ 4 = $20. $345.60 multiplies by 4."))
    # 4 salmon
    T = D("2.4") * D("24.50")
    assert T == D("58.80")
    its.append(mcq("Fresh sockeye salmon costs $24.50 per kilogram. Simran buys 2.4 kg. How much does it cost?", M(T),
                   ["$588", "$5.88", "$26.90"],
                   "245 × 24 = 5880. $24.50 has 2 decimal places and 2.4 has 1, so count 3 places: 58.800 = <b>$58.80</b>. "
                   "Estimate: 2.4 × $25 = $60. $26.90 adds."))
    # 5 gas: decimal litres
    T = D("42.4") * D("1.85")
    assert T == D("78.44")
    its.append(mcq("Gas costs $1.85 per litre in Kamloops. Mateo’s mom pumps 42.4 L. How much does the gas cost?", M(T),
                   ["$784.40", "$7.84", "$44.25"],
                   "424 × 185 = 78" + NB + "440. Count 1 + 2 = 3 decimal places: 78.440 = <b>$78.44</b>. "
                   "Estimate: 40 × $2 = $80. $44.25 adds 42.4 + 1.85."))
    # 6 bill with zero in quotient
    T = D("72.30") / 6
    assert T == D("12.05") and drop_zero(T) == D("12.5")
    its.append(mcq("Six teammates split a $72.30 pizza bill after a soccer game in Surrey. How much does each person pay?",
                   M(T), ["$12.50", "$120.50", "$433.80"],
                   "$72.30 ÷ 6: 7 ÷ 6 = 1 r 1, 12 ÷ 6 = 2, 3 ÷ 6 = 0 (write the 0), 30 ÷ 6 = 5. Each pays <b>$12.05</b>. "
                   "$12.50 drops the 0 in the tenths place. Check: $12.05 × 6 = $72.30."))
    # 7 price per litre
    T = D("64.80") / 36
    assert T == D("1.80")
    its.append(mcq("Ji-woo’s dad pays $64.80 for 36 L of gas. What is the price per litre?", M(T),
                   ["$18", "$0.18", "$28.80"],
                   "Price per litre = cost ÷ litres: $64.80 ÷ 36 = <b>$1.80</b>. Check: 36 × $1.80 = $64.80. "
                   "$28.80 subtracts 64.80 − 36."))
    # 8 how many litres for $50
    T = D(50) / D("1.60")
    assert T == D("31.25")
    its.append(mcq("Gas costs $1.60 per litre. How many litres can you buy for $50?", N(T) + " L",
                   ["312.5 L", "3.125 L", "80 L"],
                   "$50 ÷ $1.60 = 500 ÷ 16 = <b>31.25 L</b>. Estimate: $50 ÷ $2 = 25 L, a bit more because $1.60 is less than $2. "
                   "80 L multiplies 50 × 1.6."))
    # 9 Sea-to-Sky
    T = 120 * D("0.08")
    assert T == D("9.6")
    its.append(mcq("A car uses 0.08 L of gas per kilometre. The drive from Vancouver to Whistler is about 120 km. "
                   "About how much gas does the car use?", N(T) + " L", ["96 L", "0.96 L", "1500 L"],
                   "120 × 0.08 = 120 × 8 hundredths = 960 hundredths = <b>9.6 L</b>. "
                   "96 L counts only 1 decimal place. 1500 L divides 120 ÷ 0.08."))
    # 10 cedar board
    T = D("4.5") / D("0.75")
    assert T == 6
    its.append(mcq("A 4.5 m cedar board is cut into pieces that are 0.75 m long. How many pieces are there?", "6 pieces",
                   ["0.6 pieces", "60 pieces", "3.375 pieces"],
                   "4.5 ÷ 0.75 = 450 ÷ 75 = <b>6 pieces</b>. Check: 6 × 0.75 = 4.5. 3.375 multiplies 4.5 × 0.75."))
    # 11 hiking
    T = D("13.2") / D("2.4")
    assert T == D("5.5")
    its.append(mcq("A family hikes a 13.2 km trail on Vancouver Island at 2.4 km per hour. How many hours does the hike take?",
                   N(T) + " hours", ["55 hours", "0.55 hours", "31.68 hours"],
                   "13.2 ÷ 2.4 = 132 ÷ 24 = <b>5.5 hours</b>. Estimate: 12 ÷ 2 = 6. 31.68 multiplies."))
    # 12 blueberries
    T = D("13.75") / D("2.5")
    assert T == D("5.50")
    its.append(mcq("A 2.5 kg flat of Fraser Valley blueberries costs $13.75. What is the price per kilogram?", M(T),
                   ["$55", "$0.55", "$11.25"],
                   "$13.75 ÷ 2.5 = 137.5 ÷ 25 = <b>$5.50</b> per kilogram. Check: 2.5 × $5.50 = $13.75. "
                   "$11.25 subtracts 13.75 − 2.5."))
    # 13 rain
    T = 7 * D("6.4")
    assert T == D("44.8")
    its.append(mcq("In November, 6.4 mm of rain fell in Vancouver every day for 7 days. How much rain fell in all?",
                   N(T) + " mm", ["448 mm", "4.48 mm", "13.4 mm"],
                   "7 × 6.4 = 7 × 64 tenths = 448 tenths = <b>44.8 mm</b>. Estimate: 7 × 6 = 42. 13.4 mm adds."))
    # 14 bill with taxes
    T = D("54.60") / 3
    assert T == D("18.20")
    its.append(mcq("Three cousins share a $54.60 bill (taxes included) at a café in Victoria. How much does each pay?", M(T),
                   ["$18.02", "$182", "$163.80"],
                   "$54.60 ÷ 3: 5 ÷ 3 = 1 r 2, 24 ÷ 3 = 8, 6 ÷ 3 = 2, 0 ÷ 3 = 0. Each pays <b>$18.20</b>. "
                   "$18.02 puts the 2 in the wrong place. $163.80 multiplies."))
    # 15 better buy
    p1, p2 = D("2.85") / D("1.5"), D("3.60") / 2
    assert p1 == D("1.90") and p2 == D("1.80")
    its.append(mcq("Which is the better buy for apple juice?", "2 L for $3.60",
                   ["1.5 L for $2.85", "They cost the same per litre", "You cannot tell"],
                   "Find the price per litre. $2.85 ÷ 1.5 = $1.90 per litre. $3.60 ÷ 2 = $1.80 per litre. "
                   "<b>2 L for $3.60</b> costs less per litre.", text_ok=True))
    # 16 wage
    T = D("18.40") * D("3.5")
    assert T == D("64.40")
    its.append(mcq("Owen’s sister earns $18.40 per hour at a Kelowna bakery. She works 3.5 hours on Saturday. "
                   "How much does she earn?", M(T), ["$644", "$6.44", "$21.90"],
                   "184 × 35 = 6440. Count 2 + 1 = 3 decimal places: 64.400 = <b>$64.40</b>. "
                   "Estimate: 3.5 × $18 = $63. $21.90 adds."))
    # 17 estimate gas
    assert abs(D("39.6") * D("1.89") - 80) < 6
    its.append(mcq("Gas costs $1.89 per litre. Which is the best estimate of the cost of 39.6 L?", "$80",
                   ["$8", "$800", "$41"],
                   "$1.89 ≈ $2 and 39.6 L ≈ 40 L. 40 × $2 = <b>$80</b>. (The exact cost is $74.84 after rounding to the cent.) $41 adds 39.6 + 1.89."))
    # 18 km per litre
    T = D(582) / D("48.5")
    assert T == 12
    its.append(mcq("Leah’s family drives 582 km on a road trip through the Okanagan and uses 48.5 L of gas. "
                   "How many kilometres do they drive per litre?", "12 km", ["1.2 km", "120 km", "533.5 km"],
                   "Kilometres per litre = km ÷ L: 582 ÷ 48.5 = 5820 ÷ 485 = <b>12 km</b>. "
                   "Estimate: 600 ÷ 50 = 12. 533.5 subtracts."))
    # 19 gas and change (card-free: the total ends in 5, so cash needs no rounding)
    cost = 45 * D("1.79")
    T = 100 - cost
    assert cost == D("80.55") and T == D("19.45") and (cost * 100) % 5 == 0
    its.append(mcq("Gas costs $1.79 per litre. Ava’s grandpa buys 45 L and pays with a $100 bill. How much change does he get?",
                   M(T), ["$80.55", "$53.21", "$20.55"],
                   "Cost: 45 × $1.79 = $80.55. Change: $100 − $80.55 = <b>$19.45</b>. $80.55 is the cost, not the change. "
                   "$53.21 subtracts 45 and 1.79 from 100 instead of multiplying first. $20.55 forgets to regroup when subtracting the cents."))
    # 20 two steps: bill plus tip, shared
    total = D("47.25") + D("8.50")
    T = total / 5
    assert total == D("55.75") and T == D("11.15")
    its.append(mcq("Five friends eat at a restaurant in Nanaimo. The bill is $47.25 and they add an $8.50 tip. "
                   "They share the total equally. How much does each friend pay?", M(T), ["$9.45", "$55.75", "$111.50"],
                   "Total: $47.25 + $8.50 = $55.75. Each: $55.75 ÷ 5 = <b>$11.15</b>. $9.45 forgets the tip "
                   "($47.25 ÷ 5). $55.75 is the total, not each share."))
    assert len(its) == 20
    order = [0, 1, 2, 12, 6, 3, 8, 4, 5, 13, 9, 16, 15, 7, 11, 10, 17, 14, 18, 19]
    return {"title": "Word problems: gas prices and sharing a bill", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    f1 = overlap_svg(3, 2)
    f2 = mul_svg([("", "2.35"), ("×", "1.4"), ("", "3.290")], [1],
                 "2.35 times 1.4 written in columns, product 3.290", colors={2: GREEN})
    f3 = ld_svg("7.38", 3, "full")
    f4 = shift_svg("1.44", "0.12")
    return (
        "<h2>Work with whole numbers, then place the decimal point</h2>"
        "<p>Multiply or divide as if there were no decimal points. Then use a rule, and an estimate, to put the point "
        "in the right place.</p>"
        "<h2>Multiply: count the decimal places</h2>"
        "<p>Add the number of decimal places in the two numbers. The answer has that many places. "
        "Count them <b>before</b> you drop any zeros at the end.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>0.3 × 0.2: 3 tenths of 2 tenths is 6 squares out of 100, so 0.3 × 0.2 = 0.06, not 0.6.</figcaption></figure>"
        + ex("Example 1", "2.35 × 1.4",
             "235 × 14 = 3290. 2.35 has 2 decimal places and 1.4 has 1, so the answer has 3: 3.290 = 3.29. "
             "Estimate: 2 × 1.5 = 3.", "3.29")
        + "<figure class='sn-fig'>" + f2 +
        "<figcaption>Line the numbers up on the right. Do not line up the points when you multiply.</figcaption></figure>"
        "<h2>Divide by a whole number</h2>"
        "<p>Use long division. Put the point in the answer straight above the point in the number you divide. "
        "If digits run out, write zeros and keep going: 7.5 = 7.50 = 7.500.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>7.38 ÷ 3 = 2.46. The point in the answer sits above the point in 7.38.</figcaption></figure>"
        + ex("Example 2", "4.08 ÷ 4", "4 ÷ 4 = 1. 0 ÷ 4 = 0, so write 0 in the tenths place. 8 ÷ 4 = 2.",
             "1.02 (not 1.2)")
        + "<h2>Divide by a decimal: move both points</h2>"
        "<p>Make the divisor a whole number. Move its decimal point to the right, then move the point in the other number "
        "the <b>same</b> number of places. Write zeros if you need more places. The answer does not change.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>1.44 ÷ 0.12: both points move 2 places, so 1.44 ÷ 0.12 = 144 ÷ 12 = 12.</figcaption></figure>"
        + ex("Example 3", "6 ÷ 0.4", "Move both points 1 place: 6 ÷ 0.4 = 60 ÷ 4 = 15. Check: 15 × 0.4 = 6.", "15")
        + "<h2>Estimate to check the point</h2>"
        "<p>Round to easy numbers. 4.8 × 3.1 is about 5 × 3 = 15, so the answer is 14.88, not 1.488 or 148.8. "
        "Multiplying by a number less than 1 makes the answer smaller. Dividing by a number less than 1 makes it bigger.</p>"
        + ex("Example 4", "Gas costs $1.85 per litre. How much do 42.4 L cost?",
             "424 × 185 = 78" + NB + "440. Count 1 + 2 = 3 decimal places: 78.440. Estimate: 40 × $2 = $80.", "$78.44")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.3 × 0.2 = 0.6", "1 + 1 = 2 decimal places: 0.3 × 0.2 = 0.06"],
            ["Lining up the points to multiply", "Line up on the right, then count the decimal places"],
            ["1.6 × 0.35 = 0.056 (dropping the zero first)", "Count 3 places in 560 first: 0.560 = 0.56"],
            ["4.08 ÷ 4 = 1.2 (skipping the 0)", "Write 0 when the divisor does not fit: 1.02"],
            ["4.85 ÷ 0.5 = 0.97 (moving only one point)", "Move both points: 48.5 ÷ 5 = 9.7"],
            ["7.6 × 4.9 = 3.724 (point in the wrong place)", "Estimate 8 × 5 = 40, so the answer is 37.24"],
        ])
    )


FAQ = [
    {"q": "How do you multiply decimals in Grade 7?",
     "a": "Multiply as if there were no decimal points, then count the decimal places in both numbers and give the answer that many places: 2.35 × 1.4 → 235 × 14 = 3290 → 3.290 = 3.29. Estimate to check: 2 × 1.5 = 3."},
    {"q": "Why is 0.3 × 0.2 equal to 0.06 and not 0.6?",
     "a": "0.3 × 0.2 means 3 tenths of 2 tenths, which is 6 hundredths. Both numbers have 1 decimal place, so the answer needs 2: 0.06. It must also be less than 0.2, and 0.6 is not."},
    {"q": "How do you divide by a decimal, like 4.56 ÷ 0.12?",
     "a": "Move the decimal point in the divisor to make it a whole number, and move the point in the other number the same number of places: 4.56 ÷ 0.12 = 456 ÷ 12 = 38. Check by multiplying: 38 × 0.12 = 4.56."},
    {"q": "Is multiplying and dividing decimals on the Grade 7 FSA?",
     "a": "It can be. The Grade 7 FSA numeracy section is based on the BC curriculum, and decimal operations are a Grade 7 learning standard, often used in money and measurement problems like the ones on this page."},
]


def verify(sets):
    """Recompute every plain 'a × b = ?' / 'a ÷ b = ?' answer and every 'The digits of ...' answer."""
    n = 0
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.match(r"^([\d.]+) ([×÷]) ([\d.]+) = \?$", it["q"])
            if not m:
                m = re.search(r"What is ([\d.]+) ([×÷]) ([\d.]+)\?$", it["q"])
            if m:
                a, op, b = Dm(m.group(1)), m.group(2), Dm(m.group(3))
                assert val(right)[0] == (a * b if op == "×" else a / b), it["q"]
                n += 1
            for c in it["c"]:
                v = val(c)
                if v and v[1] == "$":
                    assert v[0] == v[0].quantize(Dm("0.01")), (it["q"], c)
    return n


def gen():
    rnd = random.Random(37805)
    sets = [set_multiply(), set_div_whole(), set_div_dec(), set_estimate(), set_words()]
    assert verify(sets) >= 50
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vs = [val(x) for x in it["c"]]
            if all(vs):
                assert len(set(vs)) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "multiplying-and-dividing-decimals",
        "sort": 5, "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Multiplying and Dividing Decimals",
        "seo_title": "Grade 7 Multiplying and Dividing Decimals Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Multiplying and Dividing Decimals",
        "domain": "Computational fluency",
        "standard_code": "Grade 7: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Operations with decimals (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 7 math worksheets on multiplying and dividing decimals, matched to the BC curriculum: "
                     "counting decimal places, dividing by whole numbers and by decimals, estimating to place the decimal "
                     "point, and word problems with gas prices and shared bills. 100 questions with an answer key. "
                     "Great FSA practice.",
        "key_big": "Multiply or divide like whole numbers, then place the decimal point and check with an estimate.",
        "key_sub": "To multiply, add the decimal places: 0.3 × 0.2 = 0.06, not 0.6. To divide by a decimal, move both "
                   "points the same number of places: 4.56 ÷ 0.12 = 456 ÷ 12 = 38.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
