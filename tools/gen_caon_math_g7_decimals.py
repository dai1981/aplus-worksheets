# -*- coding: utf-8 -*-
"""
Ontario Grade 7 Math: Multiplying and Dividing Decimals (Ontario Curriculum 2020, B2.9: multiply and divide
decimal numbers by decimal numbers, in various contexts)
  python3 tools/gen_caon_math_g7_decimals.py
Decimal × decimal (count the decimal places; hundredths grid for 0.3 × 0.2 = 0.06, not 0.6), estimating to place
the decimal point, dividing by a decimal (move the point the same number of places in both numbers), mixed
practice, and word problems in Ontario contexts (gas price per litre, price per kilogram).
All arithmetic uses decimal.Decimal (never float). Wrong answers are real student mistakes: counting only the
larger number of decimal places, dropping zeros before counting, the point one place off, adding instead of
multiplying, moving the point only in the divisor, and multiplying instead of dividing.
Helpers and figures are copied from gen_cabc_math_g7_mult_div_decimals.py (hundredths grid, columns, moving both
points). Ontario style: Canadian English, $ and the cent sign, metric units, 4-digit numbers without a separator,
5 or more digits with a no-break space. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-7")
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
    """Exact decimal text, Ontario style: 4536, 12 350 (no-break space), 0.045."""
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




def ord_q(qtext, right, wrong, e):
    return mcq(qtext, right, wrong, e, text_ok=True)


# ============================================================ set 1: decimal × decimal
def set_multiply():
    its = []
    assert Dm("0.3") * Dm("0.2") == Dm("0.06")
    its.append(mcq(fig(overlap_svg(3, 2)) + "The dark squares show 0.3 × 0.2. What is 0.3 × 0.2?", "0.06",
                   ["0.6", "0.5", "0.006"],
                   "3 tenths × 2 tenths = 6 <b>hundredths</b>: 6 of the 100 small squares are dark. 0.3 × 0.2 = <b>0.06</b>. "
                   "0.6 is the common mistake: 1 + 1 = 2 decimal places, so the answer needs 2 places. 0.5 adds."))
    assert Dm("0.6") * Dm("0.4") == Dm("0.24")
    its.append(mcq(fig(overlap_svg(6, 4)) + "The dark squares show 0.6 × 0.4. What is 0.6 × 0.4?", "0.24",
                   ["2.4", "1", "0.024"],
                   "6 columns × 4 rows = 24 dark squares out of 100, so 0.6 × 0.4 = <b>0.24</b>. "
                   "The answer is less than both 0.6 and 0.4, so 2.4 cannot be right. 1 adds 0.6 + 0.4."))
    assert Dm("0.8") * Dm("0.5") == Dm("0.4")
    its.append(mcq(fig(overlap_svg(8, 5)) + "The dark squares show 0.8 × 0.5. What is 0.8 × 0.5?", "0.4",
                   ["4", "0.04", "1.3"],
                   "40 dark squares out of 100 is 0.40 = <b>0.4</b>. 8 × 5 = 40, then count 2 places: 0.40. "
                   "0.04 drops the zero first and then counts 2 places: count before you drop zeros."))
    assert Dm("0.7") * Dm("0.03") == Dm("0.021")
    its.append(mcq("How many decimal places does the answer to 0.7 × 0.03 have?", "3", ["2", "1", "4"],
                   "0.7 has 1 decimal place and 0.03 has 2. The product has <b>1 + 2 = 3</b> places: "
                   "7 × 3 = 21, so 0.7 × 0.03 = 0.021. 2 uses only the larger number of places."))
    its.append(mcq("0.7 × 0.03 = ?", "0.021", nums(mul_cands("0.7", "0.03")),
                   mul_e("0.7", "0.03", "0.21 counts only 2 places.")))
    for a, b in [("0.4", "0.9"), ("1.3", "0.2"), ("2.4", "0.3"), ("0.05", "0.6")]:
        its.append(mcq("%s × %s = ?" % (a, b), N(Dm(a) * Dm(b)), nums(mul_cands(a, b)), mul_e(a, b)))
    assert Dm("3.25") * Dm("1.6") == Dm("5.2") and 325 * 16 == 5200
    its.append(mcq(fig(mul_digits_svg("3.25", "1.6")) + "325 × 16 = 5200. Where does the decimal point go in 3.25 × 1.6?",
                   "5.2", nums([Dm(52), Dm("0.52"), Dm("0.052")]),
                   mul_e("3.25", "1.6", "Estimate: 3 × 1.5 = 4.5, so 5.2 makes sense. 52 counts only 2 places.")))
    assert Dm("0.45") * Dm("2.7") == Dm("1.215") and 45 * 27 == 1215
    its.append(mcq(fig(mul_digits_svg("0.45", "2.7")) + "45 × 27 = 1215. What is 0.45 × 2.7?", "1.215",
                   nums([Dm("12.15"), Dm("0.1215"), Dm("121.5")]),
                   mul_e("0.45", "2.7", "Estimate: half of 2.7 is about 1.35, so 1.215 makes sense.")))
    for a, b in [("4.6", "0.35"), ("0.12", "0.8"), ("6.25", "0.4"), ("1.08", "2.5")]:
        its.append(mcq("%s × %s = ?" % (a, b), N(Dm(a) * Dm(b)), nums(mul_cands(a, b)), mul_e(a, b)))
    assert 37 * 54 == 1998 and Dm("3.7") * Dm("0.54") == Dm("1.998")
    its.append(mcq("37 × 54 = 1998. Use this to find 3.7 × 0.54.", "1.998", ["19.98", "0.1998", "199.8"],
                   "3.7 has 1 decimal place and 0.54 has 2, so the product has 3: <b>1.998</b>. "
                   "Estimate: 4 × 0.5 = 2, which is close."))
    assert Dm("0.2") * Dm("0.3") * Dm("0.5") == Dm("0.03")
    its.append(mcq("0.2 × 0.3 × 0.5 = ?", "0.03", ["0.3", "0.003", "1"],
                   "2 × 3 × 5 = 30. Each number has 1 decimal place, so the answer has 1 + 1 + 1 = 3: 0.030 = <b>0.03</b>. "
                   "0.3 counts only 2 places. 1 adds the numbers."))
    vals = {"0.6 × 0.9": Dm("0.54"), "0.6 × 1.2": Dm("0.72"), "0.6 × 1": Dm("0.6"), "0.6 × 2.5": Dm("1.5")}
    assert all(Dm(k.split(" × ")[0]) * Dm(k.split(" × ")[1]) == v for k, v in vals.items())
    assert [k for k, v in vals.items() if v < Dm("0.6")] == ["0.6 × 0.9"]
    its.append(ord_q("Without multiplying, which product is <b>less than 0.6</b>?", "0.6 × 0.9",
                     ["0.6 × 1.2", "0.6 × 1", "0.6 × 2.5"],
                     "Compare the other number with 1. Only 0.9 is less than 1, so only <b>0.6 × 0.9</b> is less than 0.6 "
                     "(it is 0.54). 0.6 × 1 is exactly 0.6."))
    opts = {"0.6 × 0.8": Dm("0.48"), "6 × 0.8": Dm("4.8"), "0.06 × 0.8": Dm("0.048"), "0.06 × 0.08": Dm("0.0048")}
    assert all(Dm(k.split(" × ")[0]) * Dm(k.split(" × ")[1]) == v for k, v in opts.items())
    its.append(ord_q("Which product equals <b>0.48</b>?", "0.6 × 0.8", ["6 × 0.8", "0.06 × 0.8", "0.06 × 0.08"],
                     "6 × 8 = 48, and 0.48 has 2 decimal places, so the two numbers need 1 + 1 places: "
                     "<b>0.6 × 0.8</b> = 0.48. 6 × 0.8 = 4.8, 0.06 × 0.8 = 0.048 and 0.06 × 0.08 = 0.0048."))
    assert Dm("0.8") * Dm("0.7") == Dm("0.56")
    its.append(mcq("Zoe says 0.8 × 0.7 = 5.6. What is the correct answer?", "0.56", ["5.6", "0.056", "1.5"],
                   "8 × 7 = 56, and 1 + 1 = 2 decimal places, so 0.8 × 0.7 = <b>0.56</b>. "
                   "Zoe counted only 1 place. Two numbers less than 1 have a product less than both of them."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 18, 9, 10, 11, 12, 13, 14, 16, 15, 17, 19]
    return {"title": "Decimal × decimal: count the decimal places", "items": [its[i] for i in order]}


# ============================================================ set 2: estimate to place the decimal point
def set_estimate():
    its = []

    def place_q(expr, ans, digits, wrong, est):
        assert str(digits_of(N(ans))) == digits.lstrip("0"), (expr, ans, digits)
        return mcq("The digits of %s are %s. Use an estimate to place the decimal point. What is %s?" % (expr, digits, expr),
                   N(ans), wrong, "Estimate: %s. Only <b>%s</b> is close to that." % (est, N(ans)))

    assert Dm("5.9") * Dm("4.2") == Dm("24.78")
    its.append(place_q("5.9 × 4.2", Dm("24.78"), "2478", ["2.478", "247.8", "0.2478"], "6 × 4 = 24"))
    assert Dm("7.92") / Dm("0.9") == Dm("8.8")
    its.append(place_q("7.92 ÷ 0.9", Dm("8.8"), "88", ["0.88", "88", "880"],
                       "7.92 is about 8 and 0.9 is about 1, so the answer is about 8 ÷ 1 = 8 (a bit more, because 0.9 is less than 1)"))
    assert Dm("46.8") / Dm("1.8") == 26
    its.append(place_q("46.8 ÷ 1.8", Dm(26), "26", ["2.6", "260", "0.26"], "50 ÷ 2 = 25"))
    assert Dm("8.1") * Dm("0.52") == Dm("4.212")
    its.append(place_q("8.1 × 0.52", Dm("4.212"), "4212", ["42.12", "0.4212", "421.2"],
                       "0.52 is about 0.5 (one half), and half of 8 is 4"))
    assert Dm("18.9") / Dm("4.5") == Dm("4.2")
    its.append(place_q("18.9 ÷ 4.5", Dm("4.2"), "42", ["42", "0.42", "420"], "20 ÷ 5 = 4"))
    assert Dm("0.48") * Dm("0.6") == Dm("0.288")
    its.append(place_q("0.48 × 0.6", Dm("0.288"), "288", ["2.88", "0.0288", "28.8"],
                       "0.48 is about 0.5, and half of 0.6 is 0.3"))
    assert Dm("152.1") / Dm("3.9") == 39
    its.append(place_q("152.1 ÷ 3.9", Dm(39), "39", ["3.9", "390", "0.39"], "160 ÷ 4 = 40"))
    # best estimate
    assert abs(Dm("59.6") * Dm("0.52") - 30) < 2
    its.append(mcq("Which is the best estimate for <b>59.6 × 0.52</b>?", "30", ["3", "300", "120"],
                   "59.6 ≈ 60 and 0.52 ≈ 0.5. 60 × 0.5 = half of 60 = <b>30</b>. "
                   "120 is 60 ÷ 0.5: it divides instead of multiplying."))
    assert abs(Dm("63.7") / Dm("8.1") - 8) < Dm("0.2")
    its.append(mcq("Which is the best estimate for <b>63.7 ÷ 8.1</b>?", "8", ["0.8", "80", "56"],
                   "63.7 ≈ 64 and 8.1 ≈ 8. 64 ÷ 8 = <b>8</b>. 56 is 64 − 8: it subtracts instead of dividing."))
    assert abs(Dm("0.99") * Dm("74.2") - 74) < 1
    its.append(mcq("Which is the best estimate for <b>0.99 × 74.2</b>?", "74", ["7.4", "740", "0.74"],
                   "0.99 is almost 1, and 1 × 74.2 = 74.2. So the answer is just under 74.2: about <b>74</b>."))
    assert abs(Dm("7.2") / Dm("0.48") - 14) <= 1
    its.append(mcq("Which is the best estimate for <b>7.2 ÷ 0.48</b>?", "14", ["1.4", "3.5", "140"],
                   "7.2 ≈ 7 and 0.48 ≈ 0.5. There are 2 halves in every whole, so 7 ÷ 0.5 = <b>14</b>. "
                   "(The exact answer is 15.) 3.5 is 7 × 0.5: it multiplies instead of dividing."))
    assert abs(Dm("3.02") * Dm("5.9") - 18) < 1
    its.append(mcq("Which is the best estimate for <b>3.02 × 5.9</b>?", "18", ["1.8", "180", "9"],
                   "3.02 ≈ 3 and 5.9 ≈ 6. 3 × 6 = <b>18</b>. 9 is 3 + 6: it adds instead of multiplying."))
    # is it reasonable?
    assert Dm("0.6") * Dm("0.5") == Dm("0.3")
    its.append(ord_q("Nathan says 0.6 × 0.5 = 3. Which statement is true?", "No: the answer must be less than 0.6",
                     ["Yes: 6 × 5 = 30", "No: the answer must be 30", "Yes: 0.6 + 0.5 is about 1"],
                     "0.5 is less than 1, so 0.6 × 0.5 is less than 0.6. <b>3 cannot be right.</b> "
                     "6 × 5 = 30 and 1 + 1 = 2 decimal places, so 0.6 × 0.5 = 0.30 = 0.3."))
    assert Dm("9.6") / Dm("0.8") == 12
    its.append(ord_q("Without dividing, which is true about 9.6 ÷ 0.8?", "It is greater than 9.6",
                     ["It is less than 9.6", "It equals 9.6", "It is less than 1"],
                     "0.8 is less than 1, so more than 9.6 groups of 0.8 fit into 9.6. The answer is "
                     "<b>greater than 9.6</b>: 9.6 ÷ 0.8 = 96 ÷ 8 = 12."))
    vals = {"5.6 × 1.1": Dm("6.16"), "5.6 × 0.99": Dm("5.544"), "5.6 × 0.5": Dm("2.8"), "5.6 × 1": Dm("5.6")}
    assert all(Dm(k.split(" × ")[0]) * Dm(k.split(" × ")[1]) == v for k, v in vals.items())
    assert [k for k, v in vals.items() if v > Dm("5.6")] == ["5.6 × 1.1"]
    its.append(ord_q("Without multiplying, which product is <b>greater than 5.6</b>?", "5.6 × 1.1",
                     ["5.6 × 0.99", "5.6 × 0.5", "5.6 × 1"],
                     "Only 1.1 is greater than 1, so only <b>5.6 × 1.1</b> is greater than 5.6 (it is 6.16). "
                     "5.6 × 1 is exactly 5.6, and 0.99 is just under 1."))
    vals = {"4.2 ÷ 1.5": Dm("2.8"), "4.2 ÷ 0.6": Dm(7), "4.2 ÷ 0.8": Dm("5.25"), "4.2 ÷ 1": Dm("4.2")}
    assert all(Dm(k.split(" ÷ ")[0]) / Dm(k.split(" ÷ ")[1]) == v for k, v in vals.items())
    assert [k for k, v in vals.items() if v < Dm("4.2")] == ["4.2 ÷ 1.5"]
    its.append(ord_q("Without dividing, which quotient is <b>less than 4.2</b>?", "4.2 ÷ 1.5",
                     ["4.2 ÷ 0.6", "4.2 ÷ 0.8", "4.2 ÷ 1"],
                     "Dividing by a number greater than 1 makes the answer smaller. Only 1.5 is greater than 1, so "
                     "<b>4.2 ÷ 1.5</b> = 2.8 is less than 4.2. Dividing by 0.6 or 0.8 makes it bigger (7 and 5.25)."))
    assert Dm("8.4") * Dm("3.6") == Dm("30.24")
    its.append(mcq("Mei works out 8.4 × 3.6 and gets 3.024. Use an estimate. What is the correct answer?", "30.24",
                   ["3.024", "302.4", "12"],
                   "Estimate: 8 × 4 = 32, so the answer is about 30. 84 × 36 = 3024, and 1 + 1 = 2 decimal places: "
                   "<b>30.24</b>. Mei counted 3 places. 12 is the sum."))
    assert Dm("16.8") / Dm("0.42") == 40
    its.append(mcq("Arjun works out 16.8 ÷ 0.42 and gets 4. Use an estimate. What is the correct answer?", "40",
                   ["4", "0.4", "400"],
                   "Estimate: 0.42 is about 0.4, and 16 ÷ 0.4 = 160 ÷ 4 = 40. Move both points 2 places: "
                   "16.8 ÷ 0.42 = 1680 ÷ 42 = <b>40</b>. Arjun moved the point in 16.8 only 1 place (168 ÷ 42 = 4)."))
    assert Dm("0.25") * Dm("23.6") == Dm("5.9")
    its.append(mcq("Which is the best estimate for <b>0.25 × 23.6</b>?", "6", ["60", "0.6", "94"],
                   "0.25 is one quarter. A quarter of 23.6 is about a quarter of 24 = <b>6</b> (exactly 5.9). "
                   "94 is about 23.6 ÷ 0.25: it divides instead of multiplying."))
    assert abs(Dm("71.4") / Dm("9.8") - 7) < Dm("0.3")
    its.append(mcq("Which is the best estimate for <b>71.4 ÷ 9.8</b>?", "7", ["0.7", "70", "62"],
                   "71.4 ≈ 70 and 9.8 ≈ 10. 70 ÷ 10 = <b>7</b>. 62 is about 71.4 − 9.8 = 61.6: it subtracts instead of dividing."))
    assert len(its) == 20
    order = [7, 8, 11, 9, 0, 2, 4, 10, 12, 6, 1, 3, 5, 13, 14, 18, 15, 19, 16, 17]
    return {"title": "Estimate to place the decimal point", "items": [its[i] for i in order]}


# ============================================================ set 3: divide by a decimal
def set_div_dec():
    its = []
    for a, b in [("2.72", "0.17"), ("2.1", "0.35"), ("3.84", "0.6"), ("9", "0.6")]:
        q = Dm(a) / Dm(b)
        its.append(mcq(fig(shift_svg(a, b)) + "Both decimal points move the same number of places. What is %s ÷ %s?" % (a, b),
                       N(q), nums(divd_cands(a, b)), divd_e(a, b)))
    for a, b, right, wrong in [("8.46", "0.3", "84.6 ÷ 3", ["8.46 ÷ 3", "846 ÷ 3", "84.6 ÷ 0.3"]),
                               ("0.24", "0.008", "240 ÷ 8", ["24 ÷ 8", "0.24 ÷ 8", "2.4 ÷ 8"]),
                               ("15", "0.25", "1500 ÷ 25", ["15 ÷ 25", "150 ÷ 25", "1500 ÷ 0.25"])]:
        k = places(b)
        A, B = Dm(a) * 10 ** k, Dm(b) * 10 ** k
        assert right == "%s ÷ %s" % (N(A), N(B))
        q = Dm(a) / Dm(b)
        for w in wrong:
            x, y = w.split(" ÷ ")
            assert Dm(x) / Dm(y) != q
        e = ("%s has %s, so multiply both numbers by %s: %s → %s and %s → %s. %s ÷ %s = <b>%s</b> = %s. "
             "Move the point the <b>same</b> number of places in both numbers."
             % (b, pl(k, "decimal place"), N(10 ** k), a, N(A), b, N(B), a, b, right, N(q)))
        its.append(ord_q("Which problem has the same answer as %s ÷ %s?" % (a, b), right, wrong, e))
    for a, b in [("8.4", "0.7"), ("19.2", "3.2"), ("4.25", "1.7"), ("0.168", "0.14"), ("0.42", "0.6"),
                 ("36", "0.48"), ("7.8", "0.12"), ("43.2", "0.8"), ("3.15", "0.07"), ("5.4", "0.012")]:
        its.append(mcq("%s ÷ %s = ?" % (a, b), N(Dm(a) / Dm(b)), nums(divd_cands(a, b)), divd_e(a, b)))
    assert Dm("2.85") * 100 == 285 and Dm("0.15") * 100 == 15
    its.append(mcq("To find 2.85 ÷ 0.15, you multiply both numbers by the same number so the divisor is a whole number. "
                   "Which number?", "100", ["10", "1000", "15"],
                   "0.15 has 2 decimal places, so multiply both by <b>100</b>: 285 ÷ 15 = 19. "
                   "× 10 gives 1.5, which is still a decimal. × 1000 also works but is more than you need."))
    assert Dm("5.25") / 5 == Dm("1.05") and Dm("5.25") / Dm("0.5") == Dm("10.5")
    its.append(ord_q("Emma wrote 5.25 ÷ 0.5 = 1.05. What mistake did she make?", "She moved the point only in 0.5",
                     ["She moved the point in both numbers", "She multiplied instead of dividing", "She made no mistake"],
                     "Emma changed 0.5 to 5 but left 5.25 as it was: 5.25 ÷ 5 = 1.05. <b>She moved the point only in 0.5</b>. "
                     "Move both: 5.25 ÷ 0.5 = 52.5 ÷ 5 = 10.5."))
    assert Dm("6.72") / Dm("0.24") == Dm(672) / 24 == 28
    its.append(ord_q("Why does 6.72 ÷ 0.24 have the same answer as 672 ÷ 24?", "Both numbers were multiplied by 100",
                     ["Only 0.24 was multiplied by 100", "Both numbers were divided by 100", "The zeros were dropped"],
                     "6.72 × 100 = 672 and 0.24 × 100 = 24. When <b>both numbers are multiplied by 100</b>, the answer does not "
                     "change, just as 6 ÷ 2 = 60 ÷ 20 = 3. Both give 28."))
    assert len(its) == 20
    order = [0, 3, 1, 2, 4, 7, 8, 17, 5, 9, 10, 11, 6, 12, 13, 18, 14, 15, 16, 19]
    return {"title": "Divide by a decimal: move both points", "items": [its[i] for i in order]}


# ============================================================ set 4: mixed practice
def set_mixed():
    its = []
    its.append(mcq("0.9 × 0.04 = ?", "0.036", nums(mul_cands("0.9", "0.04")), mul_e("0.9", "0.04")))
    its.append(mcq("1.44 ÷ 0.6 = ?", "2.4", nums(divd_cands("1.44", "0.6")), divd_e("1.44", "0.6")))
    its.append(mcq("2.6 × 0.15 = ?", N(Dm("2.6") * Dm("0.15")), nums(mul_cands("2.6", "0.15")), mul_e("2.6", "0.15")))
    its.append(mcq("0.072 ÷ 0.9 = ?", N(Dm("0.072") / Dm("0.9")), nums(divd_cands("0.072", "0.9")), divd_e("0.072", "0.9")))
    its.append(ord_q("Which words give the value of 0.3 × 0.2?", "6 hundredths", ["6 tenths", "6 thousandths", "5 tenths"],
                     "Tenths × tenths = hundredths (like 1/10 of 1/10 = 1/100). 3 × 2 = 6, so 0.3 × 0.2 = "
                     "<b>6 hundredths</b> = 0.06. 6 tenths (0.6) is the common mistake. 5 tenths adds."))
    # missing numbers
    assert Dm("0.4") * Dm("0.3") == Dm("0.12")
    its.append(mcq("0.4 × ? = 0.12", "0.3", ["3", "0.03", "0.048"],
                   "Think: 0.12 ÷ 0.4 = 1.2 ÷ 4 = <b>0.3</b>. Check: 0.4 × 0.3 = 0.12. "
                   "3 gives 1.2. 0.048 multiplies 0.4 × 0.12."))
    assert Dm("1.3") / Dm("0.5") == Dm("2.6")
    its.append(mcq("? ÷ 0.5 = 2.6", "1.3", ["5.2", "0.13", "13"],
                   "The missing number is 2.6 × 0.5 = <b>1.3</b>. Check: 1.3 ÷ 0.5 = 13 ÷ 5 = 2.6. "
                   "5.2 divides 2.6 ÷ 0.5 instead of multiplying."))
    assert Dm("1.2") * Dm("0.5") == Dm("0.6")
    its.append(mcq("1.2 × ? = 0.6", "0.5", ["2", "5", "0.05"],
                   "The answer 0.6 is less than 1.2, so the missing number is less than 1. 0.6 ÷ 1.2 = 6 ÷ 12 = <b>0.5</b>. "
                   "2 is 1.2 ÷ 0.6, the wrong way round."))
    assert Dm("5.2") * Dm("0.4") == Dm("2.08")
    its.append(ord_q("Which multiplication checks that 2.08 ÷ 0.4 = 5.2?", "5.2 × 0.4",
                     ["2.08 × 0.4", "5.2 × 2.08", "5.2 × 4"],
                     "Quotient × divisor = dividend. <b>5.2 × 0.4</b> = 2.08, so the division is right. "
                     "5.2 × 4 = 20.8 forgets that the divisor is 0.4."))
    for a, op, b in [("0.25", "×", "0.36"), ("12.6", "÷", "0.035"), ("4.8", "×", "0.125"), ("0.81", "÷", "0.09"),
                     ("7.05", "×", "0.6"), ("1.95", "÷", "1.3"), ("3.5", "×", "2.8"), ("11.7", "÷", "0.39")]:
        if op == "×":
            its.append(mcq("%s × %s = ?" % (a, b), N(Dm(a) * Dm(b)), nums(mul_cands(a, b)), mul_e(a, b)))
        else:
            its.append(mcq("%s ÷ %s = ?" % (a, b), N(Dm(a) / Dm(b)), nums(divd_cands(a, b)), divd_e(a, b)))
    # order of operations
    assert Dm("0.5") * Dm("0.4") + Dm("1.2") == Dm("1.4")
    its.append(mcq("0.5 × 0.4 + 1.2 = ?", "1.4", ["0.8", "3.2", "1.22"],
                   "Multiply first: 0.5 × 0.4 = 0.2. Then add: 0.2 + 1.2 = <b>1.4</b>. "
                   "0.8 adds first (0.5 × 1.6). 3.2 uses 0.5 × 0.4 = 2. 1.22 uses 0.5 × 0.4 = 0.02."))
    assert Dm("2.4") / Dm("0.6") * Dm("0.5") == 2
    its.append(mcq("2.4 ÷ 0.6 × 0.5 = ?", "2", ["8", "0.2", "4"],
                   "Work from left to right. 2.4 ÷ 0.6 = 24 ÷ 6 = 4. Then 4 × 0.5 = <b>2</b>. "
                   "8 multiplies first: 2.4 ÷ 0.3. 0.2 moves the point only in 0.6 (2.4 ÷ 6 = 0.4, then 0.4 × 0.5 = 0.2). 4 stops after one step."))
    assert Dm("3.6") / Dm("0.04") == 90
    its.append(mcq("Kai says 3.6 ÷ 0.04 = 9. What is the correct answer?", "90", ["9", "0.9", "900"],
                   "0.04 has 2 decimal places, so move both points 2 places. 3.6 needs a zero: 3.60 → 360. "
                   "360 ÷ 4 = <b>90</b>. Kai moved the point in 3.6 only 1 place (36 ÷ 4 = 9). Check: 90 × 0.04 = 3.6."))
    assert len(its) == 20
    order = [0, 1, 4, 2, 3, 9, 10, 5, 6, 11, 12, 7, 8, 13, 14, 15, 16, 17, 18, 19]
    return {"title": "Mixed practice: multiply and divide decimals", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words():
    its = []
    D = Dm
    T = 40 * D("1.45")
    assert T == 58
    its.append(mcq("Gas costs $1.45 per litre in Ottawa. Liam’s mom buys 40 L. How much does she pay?", M(T),
                   ["$580", "$5.80", "$41.45"],
                   "40 × $1.45 = 40 × 145¢ = 5800¢ = <b>$58</b>. Estimate: 40 × $1.50 = $60. $41.45 adds instead of multiplying."))
    T = D("0.4") * D("18.50")
    assert T == D("7.40")
    its.append(mcq("Old cheddar costs $18.50 per kilogram. Maya buys 0.4 kg. How much does it cost?", M(T),
                   ["$74", "$0.74", "$18.90"],
                   "185 × 4 = 740. $18.50 has 2 decimal places and 0.4 has 1, so count 3 places: 7.400 = <b>$7.40</b>. "
                   "Estimate: 0.4 is less than half, and half of $18.50 is about $9. $18.90 adds."))
    T = D("1.5") * D("12.80")
    assert T == D("19.20")
    its.append(mcq("Ground beef costs $12.80 per kilogram. Noah’s dad buys 1.5 kg for a barbecue. How much does he pay?", M(T),
                   ["$192", "$1.92", "$14.30"],
                   "128 × 15 = 1920. Count 2 + 1 = 3 places: 19.200 = <b>$19.20</b>. "
                   "Estimate: 1.5 × $13 = $19.50. $14.30 adds."))
    T = D("35.5") * D("1.52")
    assert T == D("53.96")
    its.append(mcq("Gas costs $1.52 per litre in Sudbury. Priya’s aunt pumps 35.5 L. How much does the gas cost?", M(T),
                   ["$539.60", "$37.02", "$5396"],
                   "355 × 152 = 53" + NB + "960. Count 1 + 2 = 3 decimal places: 53.960 = <b>$53.96</b>. "
                   "Estimate: 35 × $1.50 = $52.50. $539.60 counts only 2 places. $37.02 adds."))
    T = D("62.64") / D("43.5")
    assert T == D("1.44")
    its.append(mcq("Ethan’s dad pays $62.64 for 43.5 L of gas. What is the price per litre?", M(T),
                   ["$14.40", "$19.14", "$106.14"],
                   "Price per litre = cost ÷ litres: 62.64 ÷ 43.5 = 626.4 ÷ 435 = <b>$1.44</b>. "
                   "Check: 43.5 × $1.44 = $62.64. $19.14 subtracts and $106.14 adds."))
    T = D("8.75") / D("2.5")
    assert T == D("3.50")
    its.append(mcq("A 2.5 kg bag of Ontario apples costs $8.75. What is the price per kilogram?", M(T),
                   ["$35", "$0.35", "$6.25"],
                   "$8.75 ÷ 2.5 = 87.5 ÷ 25 = <b>$3.50</b> per kilogram. Check: 2.5 × $3.50 = $8.75. "
                   "$6.25 subtracts 8.75 − 2.5."))
    T = D("8.40") / D("0.35")
    assert T == 24 and D("8.40") / 35 == D("0.24") and D("8.4") * D("0.35") == D("2.94")
    its.append(mcq("A 0.35 kg piece of Gouda costs $8.40. What is the price per kilogram?", M(T),
                   ["$0.24", "$2.94", "$240"],
                   "$8.40 ÷ 0.35 = 840 ÷ 35 = <b>$24</b> per kilogram. Check: 0.35 × $24 = $8.40. "
                   "$0.24 moves the point only in 0.35. $2.94 multiplies."))
    T = D(60) / D("1.50")
    assert T == 40
    its.append(mcq("Gas costs $1.50 per litre. How many litres can you buy for $60?", "40 L",
                   ["4 L", "400 L", "90 L"],
                   "$60 ÷ $1.50 = 600 ÷ 15 = <b>40 L</b>. Check: 40 × $1.50 = $60. 90 L multiplies 60 × 1.5."))
    T = 450 * D("0.075")
    assert T == D("33.75")
    its.append(mcq("A car uses 0.075 L of gas per kilometre. The drive from Toronto to Ottawa is about 450 km. "
                   "How much gas does the car use?", N(T) + " L", ["337.5 L", "3.375 L", "6000 L"],
                   "450 × 0.075: 450 × 75 = 33" + NB + "750, and count 3 decimal places: 33.750 = <b>33.75 L</b>. "
                   "Estimate: 450 × 0.08 = 36 L. 6000 L divides 450 ÷ 0.075."))
    T = D("4.5") / D("0.25")
    assert T == 18
    its.append(mcq("A sugar shack pours 4.5 L of maple syrup into bottles that hold 0.25 L each. How many bottles does it fill?",
                   "18 bottles", ["1.8 bottles", "180 bottles", "1.125 bottles"],
                   "4.5 ÷ 0.25 = 450 ÷ 25 = <b>18 bottles</b>. Check: 18 × 0.25 = 4.5. 1.125 multiplies 4.5 × 0.25."))
    T = D("1.8") * D("6.5")
    assert T == D("11.7")
    its.append(mcq("During a snowstorm in Barrie, 1.8 cm of snow fell every hour for 6.5 hours. How much snow fell in all?",
                   N(T) + " cm", ["117 cm", "1.17 cm", "8.3 cm"],
                   "18 × 65 = 1170. Count 1 + 1 = 2 places: 11.70 = <b>11.7 cm</b>. Estimate: 2 × 6 = 12. 8.3 cm adds."))
    T = D("6.3") / D("0.45")
    assert T == 14
    its.append(mcq("Hana cuts 6.3 m of ribbon into pieces that are 0.45 m long for a class project. How many pieces does she get?",
                   "14 pieces", ["1.4 pieces", "140 pieces", "2.835 pieces"],
                   "6.3 ÷ 0.45 = 630 ÷ 45 = <b>14 pieces</b>. Check: 14 × 0.45 = 6.3. 2.835 multiplies 6.3 × 0.45."))
    T = D("10.8") / D("2.4")
    assert T == D("4.5")
    its.append(mcq("A family hikes a 10.8 km trail in Algonquin Park at 2.4 km per hour. How many hours does the hike take?",
                   N(T) + " hours", ["45 hours", "0.45 hours", "25.92 hours"],
                   "10.8 ÷ 2.4 = 108 ÷ 24 = <b>4.5 hours</b>. Estimate: 10 ÷ 2 = 5. 25.92 multiplies."))
    p1, p2 = D("3.30") / D("1.5"), D("5.25") / D("2.5")
    assert p1 == D("2.20") and p2 == D("2.10")
    its.append(ord_q("Which is the better buy for carrots?", "2.5 kg for $5.25",
                     ["1.5 kg for $3.30", "They cost the same per kilogram", "You cannot tell"],
                     "Find the price per kilogram. $3.30 ÷ 1.5 = $2.20 per kilogram. $5.25 ÷ 2.5 = $2.10 per kilogram. "
                     "<b>2.5 kg for $5.25</b> costs less per kilogram."))
    T = D("17.60") * D("4.5")
    assert T == D("79.20")
    its.append(mcq("Owen’s sister earns $17.60 per hour at a bakery in London, Ontario. She works 4.5 hours on Saturday. "
                   "How much does she earn?", M(T), ["$792", "$7.92", "$22.10"],
                   "176 × 45 = 7920. Count 2 + 1 = 3 decimal places: 79.200 = <b>$79.20</b>. "
                   "Estimate: 4.5 × $18 = $81. $22.10 adds."))
    assert abs(D("51.2") * D("1.48") - 75) < 1
    its.append(mcq("Gas costs $1.48 per litre. Which is the best estimate of the cost of 51.2 L?", "$75",
                   ["$7.50", "$750", "$52.68"],
                   "$1.48 ≈ $1.50 and 51.2 L ≈ 50 L. 50 × $1.50 = <b>$75</b>. (The exact cost is $75.78 after rounding "
                   "to the cent.) $52.68 adds 51.2 + 1.48."))
    T = D(486) / D("40.5")
    assert T == 12
    its.append(mcq("Leah’s family drives 486 km to a cottage near Sault Ste. Marie and uses 40.5 L of gas. "
                   "How many kilometres do they drive per litre?", "12 km", ["1.2 km", "120 km", "445.5 km"],
                   "Kilometres per litre = km ÷ L: 486 ÷ 40.5 = 4860 ÷ 405 = <b>12 km</b>. "
                   "Estimate: 480 ÷ 40 = 12. 445.5 subtracts."))
    T = D("5.94") / D("4.40")
    assert T == D("1.35") and D("5.94") - D("4.40") == D("1.54")
    its.append(mcq("Grapes cost $4.40 per kilogram. Ava pays $5.94 for a bunch. How many kilograms of grapes does she buy?",
                   "1.35 kg", ["13.5 kg", "0.135 kg", "1.54 kg"],
                   "Kilograms = cost ÷ price per kilogram: 5.94 ÷ 4.4 = 59.4 ÷ 44 = <b>1.35 kg</b>. "
                   "Check: 1.35 × $4.40 = $5.94. 1.54 subtracts 5.94 − 4.40."))
    cost = 35 * D("1.39")
    T = 60 - cost
    assert cost == D("48.65") and T == D("11.35") and (cost * 100) % 5 == 0
    its.append(mcq("Gas costs $1.39 per litre. Kai’s grandpa buys 35 L and pays with three $20 bills. How much change does he get?",
                   M(T), ["$48.65", "$12.65", "$23.61"],
                   "Cost: 35 × $1.39 = $48.65. Change: $60 − $48.65 = <b>$11.35</b>. $48.65 is the cost, not the change. "
                   "$12.65 subtracts only the dollars (60 − 48) and keeps the 65¢. $23.61 subtracts 35 and 1.39 from 60 "
                   "instead of multiplying first."))
    c1, c2 = D("1.2") * D("8.50"), D("0.8") * D("11.25")
    assert c1 == D("10.20") and c2 == 9 and c1 + c2 == D("19.20")
    its.append(mcq("At a farmers’ market, cherries cost $8.50 per kilogram and blueberries cost $11.25 per kilogram. "
                   "Sofia buys 1.2 kg of cherries and 0.8 kg of blueberries. How much does she pay?", M(c1 + c2),
                   ["$19.75", "$10.20", "$1.92"],
                   "Cherries: 1.2 × $8.50 = $10.20. Blueberries: 0.8 × $11.25 = $9. Total: $10.20 + $9 = <b>$19.20</b>. "
                   "$19.75 adds the two prices. $10.20 forgets the blueberries."))
    assert len(its) == 20
    order = [0, 1, 2, 10, 7, 5, 3, 9, 13, 6, 4, 14, 12, 15, 11, 8, 16, 17, 18, 19]
    return {"title": "Word problems: gas prices and price per kilogram", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    f1 = overlap_svg(3, 2)
    f2 = mul_svg([("", "2.35"), ("×", "1.4"), ("", "3.290")], [1],
                 "2.35 times 1.4 written in columns, product 3.290", colors={2: GREEN})
    f3 = shift_svg("4.92", "0.12")
    return (
        "<h2>Work with whole numbers, then place the decimal point</h2>"
        "<p>To multiply or divide decimals, work as if there were no decimal points. Then use a rule to put the point "
        "in the right place, and check it with an estimate.</p>"
        "<h2>Multiply: count the decimal places</h2>"
        "<p>Add the number of decimal places in the two numbers. The answer has that many places. "
        "Count them <b>before</b> you drop any zeros at the end.</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>0.3 × 0.2: 3 tenths of 2 tenths is 6 squares out of 100, so 0.3 × 0.2 = 0.06, not 0.6.</figcaption></figure>"
        + ex("Example 1", "2.35 × 1.4",
             "235 × 14 = 3290. 2.35 has 2 decimal places and 1.4 has 1, so the answer has 3: 3.290 = 3.29. "
             "Estimate: 2 × 1.5 = 3.", "3.29")
        + "<figure class='sn-fig'>" + f2 +
        "<figcaption>Line the numbers up on the right. You do not line up the points when you multiply.</figcaption></figure>"
        "<h2>Divide by a decimal: move both points</h2>"
        "<p>Make the divisor a whole number. Move its decimal point to the right, then move the point in the dividend "
        "the <b>same</b> number of places. Write zeros if you need more places. Both numbers are multiplied by the same "
        "power of 10, so the answer does not change.</p>"
        "<figure class='sn-fig'>" + f3 +
        "<figcaption>4.92 ÷ 0.12: both points move 2 places, so 4.92 ÷ 0.12 = 492 ÷ 12 = 41.</figcaption></figure>"
        + ex("Example 2", "3.6 ÷ 0.04",
             "0.04 has 2 decimal places. Move both points 2 places, writing a zero in 3.6: 3.6 ÷ 0.04 = 360 ÷ 4 = 90. "
             "Check: 90 × 0.04 = 3.6.", "90")
        + "<h2>Estimate to check the point</h2>"
        "<p>Round to easy numbers. 5.9 × 4.2 is about 6 × 4 = 24, so the answer is 24.78, not 2.478 or 247.8. "
        "Multiplying by a number less than 1 makes the answer smaller. Dividing by a number less than 1 makes it bigger.</p>"
        + ex("Example 3", "Gas costs $1.52 per litre. How much do 35.5 L cost?",
             "355 × 152 = 53" + NB + "960. Count 1 + 2 = 3 decimal places: 53.960. Estimate: 35 × $1.50 = $52.50.", "$53.96")
        + ex("Example 4", "A 0.35 kg piece of cheese costs $8.40. What is the price per kilogram?",
             "Price per kilogram = cost ÷ mass. $8.40 ÷ 0.35 = 840 ÷ 35 = 24. Check: 0.35 × $24 = $8.40.", "$24 per kilogram")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.3 × 0.2 = 0.6", "1 + 1 = 2 decimal places: 0.3 × 0.2 = 0.06"],
            ["Lining up the points to multiply", "Line up on the right, then count the decimal places"],
            ["0.8 × 0.5 = 0.04 (dropping the zero first)", "Count 2 places in 40 first: 0.40 = 0.4"],
            ["5.25 ÷ 0.5 = 1.05 (moving the point only in the divisor)", "Move both points: 52.5 ÷ 5 = 10.5"],
            ["3.6 ÷ 0.04 = 9 (moving the points different amounts)", "Move both 2 places: 360 ÷ 4 = 90"],
            ["8.4 × 3.6 = 3.024 (point in the wrong place)", "Estimate 8 × 4 = 32, so the answer is 30.24"],
        ])
    )


FAQ = [
    {"q": "What does the Ontario Grade 7 math curriculum say about multiplying and dividing decimals?",
     "a": "In Grade 7, students multiply and divide decimal numbers by decimal numbers, like 2.35 × 1.4 and 4.92 ÷ 0.12, in different contexts such as money and measurement. In Grade 6 they only worked with whole numbers and decimal tenths."},
    {"q": "Why is 0.3 × 0.2 equal to 0.06 and not 0.6?",
     "a": "0.3 × 0.2 means 3 tenths of 2 tenths, which is 6 hundredths. Both numbers have 1 decimal place, so the answer needs 2: 0.06. It must also be less than 0.2, and 0.6 is not."},
    {"q": "How do you divide a decimal by a decimal, like 4.92 ÷ 0.12?",
     "a": "Move the decimal point in the divisor to make it a whole number, and move the point in the dividend the same number of places: 4.92 ÷ 0.12 = 492 ÷ 12 = 41. Check by multiplying: 41 × 0.12 = 4.92."},
    {"q": "Does multiplying by a decimal always make a number smaller?",
     "a": "Only when the decimal is less than 1: 8 × 0.5 = 4. Multiplying by a decimal greater than 1 makes it bigger (8 × 1.5 = 12), and dividing by a decimal less than 1 makes it bigger (8 ÷ 0.5 = 16)."},
]


def mark_large(u, pattern):
    """Tag hundredths grids so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Recompute every plain 'a × b = ?' / 'a ÷ b = ?' answer and every 'What is a op b?' answer."""
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
    rnd = random.Random(47809)
    sets = [set_multiply(), set_estimate(), set_div_dec(), set_mixed(), set_words()]
    assert verify(sets) >= 40
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
        "country": "ca-on", "subject": "math", "grade": "grade-7", "slug": "multiplying-and-dividing-decimals",
        "sort": 9, "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying and Dividing Decimals",
        "seo_title": "Grade 7 Multiplying and Dividing Decimals Worksheets (Free, Ontario, Answer Key)",
        "short_title": "Multiplying and dividing decimals",
        "domain": "Number",
        "standard_code": "Grade 7: B2.9",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Multiply and divide decimal numbers by decimal numbers, in various contexts",
        "meta_desc": "Free Grade 7 math worksheets on multiplying and dividing decimals by decimals for the Ontario "
                     "curriculum: counting decimal places, estimating to place the decimal point, dividing by a decimal, "
                     "mixed practice and word problems with gas prices and price per kilogram. 100 questions with an answer key.",
        "key_big": "Multiply or divide like whole numbers, then place the decimal point and check with an estimate.",
        "key_sub": "To multiply, add the decimal places: 0.3 × 0.2 = 0.06, not 0.6. To divide by a decimal, move both "
                   "points the same number of places: 4.92 ÷ 0.12 = 492 ÷ 12 = 41.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "hundredths grid")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
