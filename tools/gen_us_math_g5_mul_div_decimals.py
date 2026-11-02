# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Multiply and Divide Decimals (5.NBT.B.7)
  python3 tools/gen_us_math_g5_mul_div_decimals.py
All arithmetic uses decimal.Decimal (never float), so every answer is exact.
Every grid is drawn from the numbers in the question: the overlap of a × b is a·10 columns by b·10 rows.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FILL_A = "#4fae74"     # group colors in the "groups" grid
FILL_B = "#f2b134"
YEL = "#f7e08a"        # columns of the first factor
BLUE = "#a9cbef"       # rows of the second factor
BOTH = "#3f9a63"       # overlap = the product
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text without extra zeros, commas from 1,000: Dm('2800.0') -> '2,800'."""
    x = Dm(x)
    s = format(x.normalize(), ",f")
    return s


def M(x):
    """Money: $3.75, $1,250.00."""
    return "$" + format(Dm(x).quantize(Dm("0.01")), ",f")


def places(x):
    """Number of decimal places as written: '2.36' -> 2."""
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


def digits_of(x):
    """'2.36' -> 236 (the number without its point)."""
    return int(str(x).replace(".", ""))


def pl(k, one, many=None):
    return "%s %s" % (N(k), one if Dm(k) == 1 else (many or one + "s"))


VAL = re.compile(r"^(?:about )?\$?([\d,]*\.?\d+)(.*)$")


def val(c):
    m = VAL.match(c)
    return (Dm(m.group(1).replace(",", "")), m.group(2)) if m else None


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 distractors with a different value. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    vals = [val(correct)]
    pick = []
    for c in cands:
        c = str(c)
        v = val(c)
        if c in seen or not c or c.startswith("-") or (v and v in vals) or (v and v[0] == 0):
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


# ------------------------------------------------------------ figures
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


def groups_svg(n, k, cell=18):
    """One hundredths grid: n groups of k squares, colors take turns. Squares fill column by column."""
    assert n * k <= 100
    pad = 4
    s = []
    for g in range(n):
        for j in range(g * k, (g + 1) * k):
            c, r = j // 10, j % 10
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>"
                     % (pad + c * cell, pad + r * cell, cell, cell, FILL_A if g % 2 == 0 else FILL_B))
    s.append(grid_lines(pad, pad, cell))
    w = 10 * cell + 2 * pad
    return svg_wrap(w, w, "".join(s), "hundredths grid with %d groups of %d squares shaded" % (n, k))


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
    # bracket and label over the columns
    x1, x2 = L, L + a * cell
    s.append("<path d='M%d %d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2'/>" % (x1, T - 2, T - 8, x2, T - 2, INK))
    s.append(text((x1 + x2) / 2.0, T - 12, "0.%d" % a, 16))
    y1, y2 = T, T + b * cell
    s.append("<path d='M%d %d H%d V%d H%d' fill='none' stroke='%s' stroke-width='2'/>" % (L - 2, y1, L - 8, y2, L - 2, INK))
    s.append(text(L - 11, (y1 + y2) / 2.0 + 6, "0.%d" % b, 16, "end"))
    W, H = L + 10 * cell + 4, T + 10 * cell + 4
    return svg_wrap(W, H, "".join(s), "hundredths grid: 0.%d of the columns and 0.%d of the rows shaded, overlap %d squares" % (a, b, a * b))


def point_mark(x, y, fs, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, y - fs * 0.06, fs * 0.1, col)


def column_svg(rows, rules, label, fs=27):
    """Numbers in columns, lined up on the right (as decimal multiplication is written).
    A decimal point sits in the gap between two digit columns."""
    cw = fs * 0.9
    lens = [len(t.replace(".", "").replace(",", "")) for sg, t in rows]
    nd = max(lens)
    signed = max([n for (sg, t), n in zip(rows, lens) if sg] or [0])
    sign_slot = max(nd, signed + 1)
    slots = sign_slot + 1
    W = int(cw * slots + 20)
    gap = fs * 1.2
    H = int(10 + gap * len(rows) + 4 * len(rules) + 10)
    right = W - 10
    s = []
    y = 10
    for r, (sg, t) in enumerate(rows):
        y += gap
        slot = 0
        for ch in reversed(t):
            if ch == ".":
                s.append(point_mark(right - cw * slot, y, fs))
                continue
            if ch == ",":
                s.append(text(right - cw * slot, y + 1, ",", fs))
                continue
            s.append(text(right - cw * (slot + 0.5), y - 2, ch, fs))
            slot += 1
        if sg:
            s.append(text(right - cw * (sign_slot + 0.5), y - 2, sg, fs, col=GREEN))
        if r in rules:
            y += 4
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
    return svg_wrap(W, H, "".join(s), label, "monospace")


def ld_rows(ds, d):
    """Long division on a digit string: list of (column, partial dividend, quotient digit), remainder."""
    cur, steps, started = 0, [], False
    for i, ch in enumerate(ds):
        cur = cur * 10 + int(ch)
        if not started and cur < d and i < len(ds) - 1:
            continue
        started = True
        q = cur // d
        steps.append((i, cur, q))
        cur -= q * d
    return steps, cur


def ld_svg(dividend, d, quot=None, work=False, fs=24):
    """Long division with a decimal dividend and a whole-number divisor.
    quot: None (no quotient), 'digits' (quotient digits, point left out) or 'full'.
    The quotient point sits straight above the dividend point."""
    ds = dividend.replace(".", "")
    k = places(dividend)
    pi = len(ds) - 1 - k                                     # column of the ones digit
    qv = Dm(dividend) / d
    qi = qv * 10 ** k
    assert qi == int(qi), (dividend, d)
    qs = str(int(qi)).rjust(len(ds), "0")
    qcols = [(j, ch) for j, ch in enumerate(qs) if j >= pi or ch != "0" or any(c != "0" for c in qs[:j])]
    cw = fs * 0.95
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18
    steps, r = ld_rows(ds, d)
    assert r == 0
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
    if work:
        y = by
        for n, (i, cur, qd) in enumerate(steps):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(left) - cw * 0.85, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.2, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            if n + 1 < len(steps):
                digits_at(str(steps[n + 1][1]), i + 1, y)
            else:
                digits_at(str(cur - p), i, y)
        H = y + 12
    label = "%s divided by %d written as long division" % (dividend, d)
    if quot == "digits":
        label += " with the quotient digits but no decimal point"
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


# ============================================================ set 1: powers of 10
def p10_item(x, op, p):
    x, p = Dm(x), Dm(p)
    F = p if op == "×" else 1 / p                       # what the number is really multiplied by
    ans = x * F
    k = len(str(int(F))) - 1 if F >= 1 else -places(N(F))
    side = "right" if k > 0 else "left"
    n = abs(k)
    word = "1 place" if n == 1 else "%d places" % n
    if op == "×" and p >= 1:
        why = "Multiplying by %s makes every digit %s times as big, so each digit moves %s to the left." % (N(p), N(p), word)
    elif op == "÷":
        why = "Dividing by %s makes every digit %s times smaller, so each digit moves %s to the right." % (N(p), N(p), word)
    else:
        why = "Multiplying by %s is the same as dividing by %s, so each digit moves %s to the right." % (N(p), N(1 / p), word)
    e = why + " That means the decimal point moves <b>%s to the %s</b>: %s → <b>%s</b>." % (word, side, N(x), N(ans))
    if k > 0 and places(N(x)) < k:
        e += " Write zeros to fill the empty places."
    if k < 0 and ans < 1:
        e += " Write a 0 in the ones place." if ans >= Dm("0.1") else " Write zeros to hold the empty places."
    e += " Check: the answer must be %s than %s." % ("bigger" if k > 0 else "smaller", N(x))
    cands = []
    if k > 0 and "." in N(x) and x >= 1:
        cands.append(N(x) + "0" * n)                     # added zeros after the point instead of moving it
    cands += [N(x / F), N(ans * 10), N(ans / 10), N(x)]
    return mcq("%s %s %s = ?" % (N(x), op, N(p)), N(ans), cands, e)


def set_powers():
    its = []
    for x, op, p in [("3.45", "×", 10), ("0.8", "×", 10), ("12.6", "×", 10),
                     ("0.67", "×", 100), ("4.2", "×", 100), ("0.05", "×", 100),
                     ("2.8", "×", 1000), ("0.36", "×", 1000),
                     ("45.6", "÷", 10), ("7", "÷", 10), ("73", "÷", 100), ("350", "÷", 100), ("1250", "÷", 1000),
                     ("36", "×", "0.1"), ("4.5", "×", "0.1"), ("250", "×", "0.01"), ("8", "×", "0.01")]:
        its.append(p10_item(x, op, p))
    its.append(mcq("To find 0.52 × 1,000, how does the decimal point move?", "3 places right",
                   ["3 places left", "2 places right", "1 place right"],
                   "1,000 has <b>3 zeros</b>, and multiplying makes the number bigger, so the point moves <b>3 places to the right</b>: "
                   "0.52 → 520. Write a zero to fill the empty place."))
    its.append(mcq("What number goes in the box?  <b>4.7 × ☐ = 470</b>", "100", ["10", "1,000", "0.01"],
                   "4.7 → 470: the point moved 2 places to the right (4.7 → 47 → 470). Moving 2 places right is "
                   "multiplying by <b>100</b>. Check: 4.7 × 100 = 470."))
    its.append(mcq("Multiplying by 0.1 is the same as …", "dividing by 10", ["multiplying by 10", "dividing by 100", "dividing by 0.1"],
                   "0.1 is 1 tenth. Taking 1 tenth of a number is <b>dividing by 10</b>: 36 × 0.1 = 3.6 = 36 ÷ 10. "
                   "(Dividing by 0.1 does the opposite: it is the same as multiplying by 10.)"))
    assert len(its) == 20
    return {"title": "Multiply and divide by 10, 100, 1,000, 0.1 and 0.01", "items": its}


# ============================================================ set 2: decimal × whole number
def split_mistake(a, d):
    """Multiplying the whole part and the decimal part on their own, without regrouping: 6 × 1.25 -> 6.150."""
    w, f = a.split(".")
    fd = int(f) * d
    if len(str(fd)) <= len(f):
        return None
    return "%s.%d" % (N(int(w) * d), fd)


def mul_e(a, d):
    """Estimate, multiply as whole numbers, place the point."""
    A = Dm(a)
    ans = A * d
    k = places(a)
    raw = digits_of(a) * d
    written = format(Dm(raw).scaleb(-k), ",f")
    if A < 1:
        e = "Estimate: %s is less than 1, so the answer is less than %d. " % (a, d)
    else:
        r = A.quantize(Dm("1"), rounding="ROUND_HALF_EVEN")
        e = "Estimate: %s is about %s, and %d × %s = %s. " % (a, N(r), d, N(r), N(r * d))
    e += "Multiply as whole numbers: %d × %s = %s. " % (d, N(digits_of(a)), N(raw))
    e += "%s has %s, so the product has %s too: " % (a, pl(k, "decimal place"), "it" if k == 1 else "them")
    e += ("%s = <b>%s</b>." % (written, N(ans))) if written != N(ans) else "<b>%s</b>." % written
    return e


def set_mul_whole():
    its = []
    # grid models: n groups of k hundredths
    for n, k, wrong in [(3, 25, ["0.075", "7.5", "3.25"]), (4, 20, ["0.08", "8", "4.2"]),
                        (2, 35, ["0.07", "7", "2.35"]), (5, 12, ["0.06", "6", "5.12"])]:
        a = N(Dm(k) / 100)
        p = Dm(n * k) / 100
        e = ("The grid is 1 whole, so each square is 0.01 and %s is %d squares. %d groups of %d squares: %d × %d = %d squares. "
             "%d hundredths = %s%s, so %d × %s = <b>%s</b>. It is less than 1 because all the groups fit in one grid."
             % (a, k, n, k, n, k, n * k, n * k, "0.%02d" % (n * k), "" if "0.%02d" % (n * k) == N(p) else " = " + N(p), n, a, N(p)))
        its.append(mcq(fig(groups_svg(n, k)) + "The grid shows %d groups of %s in two colors. What is %d × %s?" % (n, a, n, a),
                       N(Dm(n * k) / 100), wrong, e))
    # place the point after multiplying whole numbers
    for d, a in [(4, "2.36"), (7, "3.08")]:
        raw = digits_of(a) * d
        ans = Dm(a) * d
        r = Dm(a).quantize(Dm("1"), rounding="ROUND_HALF_EVEN")
        e = ("Estimate: %s is about %s, and %d × %s = %s, so the answer is about %s. "
             "%s has 2 decimal places, so the product has 2: %s → <b>%s</b>." % (a, N(r), d, N(r), N(r * d), N(r * d), a, N(raw), N(ans)))
        its.append(mcq("%d × %s = %s. What is %d × %s?" % (d, N(digits_of(a)), N(raw), d, a), N(ans),
                       [N(ans * 10), N(ans / 10), N(raw)], e))
    # compute (column figure for the first five)
    for i, (d, a) in enumerate([(6, "1.25"), (3, "4.67"), (8, "0.45"), (5, "2.38"), (9, "0.7"),
                                (4, "3.6"), (7, "0.08"), (6, "12.5"), (2, "5.06"), (3, "0.9")]):
        ans = Dm(a) * d
        cands = [split_mistake(a, d), N(ans / 10), N(ans * 10), N(ans / 100), N(ans * 100)]
        if i < 5:
            q = fig(column_svg([("", a), ("×", str(d))], [1], "%s times %d written in columns" % (a, d))) + "Multiply."
        else:
            q = "What is %d × %s?" % (d, a)
        its.append(mcq(q, N(ans), [c for c in cands if c], mul_e(a, d)))
    # size of the product
    its.append(mcq("Without multiplying, which is true about 8 × 0.5?", "It is less than 8",
                   ["It is more than 8", "It equals 8.5", "It equals 80"],
                   "0.5 is less than 1, so 8 × 0.5 is less than 8 × 1 = 8. Multiplying by a number less than 1 makes it "
                   "<b>smaller</b>. (8 × 0.5 is half of 8: 4.)"))
    its.append(mcq("Which product is greater than 6?", "6 × 1.2", ["6 × 0.9", "6 × 0.5", "6 × 1"],
                   "Compare the other factor with 1. Only 1.2 is more than 1, so only <b>6 × 1.2</b> is more than 6 (it is 7.2). "
                   "6 × 1 is exactly 6, and 6 × 0.9 and 6 × 0.5 are less than 6."))
    # two-digit whole numbers
    its.append(mcq("What is 12 × 0.75?", "9", ["0.9", "90", "0.09"],
                   "Estimate: 0.75 is a bit less than 1, so the answer is a bit less than 12. Multiply as whole numbers: "
                   "12 × 75 = 900. 0.75 has 2 decimal places: 9.00 = <b>9</b>."))
    its.append(mcq("What is 25 × 1.6?", "40", ["4", "400", "0.4"],
                   "Estimate: 1.6 is about 2, and 25 × 2 = 50, so the answer is a bit less than 50. Multiply as whole numbers: "
                   "25 × 16 = 400. 1.6 has 1 decimal place: 40.0 = <b>40</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply a decimal by a whole number", "items": its}


# ============================================================ set 3: decimal × decimal
def set_mul_dec(P):
    its = []
    for a, b, add in [(3, 4, "0.7"), (6, 5, "1.1"), (2, 7, "0.9"), (8, 4, "1.2"), (9, 3, "1.2")]:
        p = Dm(a * b) / 100
        e = ("The grid is 1 whole. 0.%d is %d columns and 0.%d is %d rows. The overlap is %d × %d = <b>%d squares</b>, "
             "and each square is 0.01. So 0.%d × 0.%d = %s<b>%s</b>."
             % (a, a, b, b, a, b, a * b, a, b, "0.%02d = " % (a * b) if (a * b) % 10 == 0 else "", N(p)))
        e += " Tenths × tenths = hundredths, so the product has 2 decimal places."
        its.append(mcq(fig(overlap_svg(a, b)) + "The dark squares show where the two parts overlap. What is 0.%d × 0.%d?" % (a, b),
                       N(p), [N(p * 10), N(p / 10), add], e))
    # tenths × tenths with wholes
    for a, b, wrong, est in [("1.2", "0.3", ["3.6", "0.036", "1.5"], "1.2 is about 1, and 1 × 0.3 = 0.3"),
                             ("2.5", "0.4", ["10", "0.1", "2.9"], "0.4 is a bit less than half, and half of 2.5 is 1.25"),
                             ("3.4", "1.2", ["40.8", "0.408", "4.8"], "3 × 1 = 3, so the answer is a bit more than 3"),
                             ("1.5", "2.6", ["39", "0.39", "4.1"], "1.5 × 3 = 4.5, so a bit less than 4.5")]:
        ans = Dm(a) * Dm(b)
        raw = digits_of(a) * digits_of(b)
        e = ("Estimate: %s. Multiply as whole numbers: %d × %d = %d. Count the decimal places: 1 + 1 = 2, so the product has 2: "
             "%s" % (est, digits_of(a), digits_of(b), raw, "%d.%02d" % (raw // 100, raw % 100)))
        if N(ans) != "%d.%02d" % (raw // 100, raw % 100):
            e += " = <b>%s</b>." % N(ans)
        else:
            e = e[:-len(N(ans))] + "<b>%s</b>." % N(ans)
        if a == "3.4":
            e += " Keep the 0 in the tenths place: 4.08, not 4.8."
        if a == "1.5":
            e += " (4.1 is 1.5 + 2.6, the sum, not the product.)"
        its.append(mcq("What is %s × %s?" % (a, b), N(ans), wrong, e))
    # place the point after multiplying whole numbers
    for a, b, wrong in [("2.3", "1.4", ["32.2", "0.322", "322"]), ("1.5", "3.6", ["54", "0.54", "540"]),
                        ("1.25", "0.4", ["5", "50", "0.05"])]:
        ra, rb = digits_of(a), digits_of(b)
        raw = ra * rb
        k = places(a) + places(b)
        ans = Dm(a) * Dm(b)
        written = str(raw).rjust(k + 1, "0")
        written = written[:-k] + "." + written[-k:]
        e = ("%s has %s and %s has %s, so the product has %d + %d = %d decimal places. Count %d places from the right in %d: %s"
             % (a, pl(places(a), "decimal place"), b, pl(places(b), "decimal place"), places(a), places(b), k, k, raw, written))
        e += (" = <b>%s</b>." % N(ans)) if N(ans) != written else ""
        if N(ans) == written:
            e = e[:-len(written)] + "<b>%s</b>." % written
        e += " Estimate to check: %s." % {"2.3": "2 × 1.5 = 3", "1.5": "1.5 × 4 = 6", "1.25": "about 1 × 0.5 = 0.5"}[a]
        its.append(mcq("%d × %d = %s. What is %s × %s?" % (ra, rb, N(raw), a, b), N(ans), wrong, e))
    # estimates
    its.append(mcq("Which is the best estimate for 2.9 × 4.1?", "about 12", ["about 1.2", "about 120", "about 7"],
                   "Round each factor to the nearest whole number: 2.9 ≈ 3 and 4.1 ≈ 4. 3 × 4 = <b>12</b>. "
                   "(About 7 is the sum, 2.9 + 4.1.)"))
    its.append(mcq("Without multiplying, which is the product of 4.8 × 3.1?", "14.88", ["1.488", "148.8", "7.9"],
                   "Estimate: 4.8 ≈ 5 and 3.1 ≈ 3, so the product is about 5 × 3 = 15. Only <b>14.88</b> is close to 15. "
                   "(7.9 is the sum.)"))
    its.append(mcq("Which is the best estimate for 6.2 × 0.48?", "about 3", ["about 0.3", "about 30", "about 7"],
                   "6.2 ≈ 6 and 0.48 ≈ 0.5 (one half). Half of 6 is <b>3</b>. The product is less than 6 because 0.48 is less than 1."))
    # size of the product
    its.append(mcq("Which is true about 0.4 × 0.9?", "It is less than 0.4",
                   ["It is more than 0.9", "It is between 0.4 and 0.9", "It equals 1.3"],
                   "0.9 is less than 1, so 0.4 × 0.9 is less than 0.4. Check: 4 × 9 = 36, so 0.4 × 0.9 = 0.36, "
                   "and <b>0.36 &lt; 0.4</b>."))
    n, he, his = P.next()
    its.append(mcq("%s says 2.5 × 0.6 is greater than 2.5 because multiplying always makes a number bigger. Is %s right?" % (n, he),
                   "No, it is less than 2.5", ["Yes, it is greater", "No, it equals 2.5", "Yes, it is 15"],
                   "0.6 is less than 1, so 2.5 × 0.6 is less than 2.5. 25 × 6 = 150, and 2 decimal places give 1.50 = 1.5. "
                   "<b>%s is not right</b>: multiplying by a number less than 1 makes it smaller." % n))
    # tenths × hundredths
    for a, b, wrong in [("0.5", "0.12", ["0.6", "0.006", "0.62"]), ("0.2", "0.35", ["0.7", "0.007", "0.55"])]:
        raw = digits_of(a) * digits_of(b)
        ans = Dm(a) * Dm(b)
        e = ("Estimate: %s is %s, so the answer is small, less than %s. Multiply as whole numbers: %d × %d = %d. "
             "1 + 2 = 3 decimal places: %s = <b>%s</b>. Keep the 0 of %d when you count the places."
             % (a, "half" if a == "0.5" else "a fifth", b, digits_of(a), digits_of(b), raw, "0.%03d" % raw, N(ans), raw))
        its.append(mcq("What is %s × %s?" % (a, b), N(ans), wrong, e))
    its.append(mcq("0.7 × 0.6 = 0.42. Why does the product have 2 decimal places?", "tenths × tenths = hundredths",
                   ["because 42 has 2 digits", "tenths × tenths = tenths", "the point never moves"],
                   "1 tenth of 1 tenth is 1 hundredth (one square of a hundredths grid). So <b>tenths × tenths = hundredths</b>: "
                   "7 tenths × 6 tenths = 42 hundredths = 0.42."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply a decimal by a decimal", "items": its}


# ============================================================ set 4: dividing decimals
def div_e(a, d, est, extra=""):
    ans = Dm(a) / d
    raw = digits_of(a)
    e = ("Estimate: %s. Divide as if there were no point: %d ÷ %d = %d. Put the point in the quotient straight above the point "
         "in the dividend: <b>%s</b>. %sCheck: %s × %d = %s." % (est, raw, d, raw // d, N(ans), extra, N(ans), d, a))
    return e


def set_divide(P):
    its = []
    # long division layout, no quotient
    for a, d, wrong, est, extra in [
            ("7.2", 3, ["24", "0.24", "21.6"], "7.2 is between 6 and 9, so the answer is between 2 and 3", ""),
            ("0.84", 4, ["21", "2.1", "0.021"], "0.84 is about 0.8, and 0.8 ÷ 4 = 0.2", "4 does not fit into 0 ones, so write 0 in the ones place. "),
            ("8.16", 4, ["2.4", "204", "20.4"], "8 ÷ 4 = 2", "4 does not fit into 1 tenth, so write 0 in the tenths place. "),
            ("5.25", 5, ["1.5", "105", "10.5"], "5 ÷ 5 = 1", "5 does not fit into 2 tenths, so write 0 in the tenths place. ")]:
        its.append(mcq(fig(ld_svg(a, d)) + "Divide.", N(Dm(a) / d), wrong, div_e(a, d, est, extra)))
    # quotient digits done, place the point
    for a, d, est in [("9.36", 4, "9.36 is between 8 and 12, so the answer is between 2 and 3"),
                      ("1.35", 5, "1.35 is less than 5, so the quotient is less than 1"),
                      ("12.6", 3, "12 ÷ 3 = 4")]:
        ans = Dm(a) / d
        raw = digits_of(a) // d
        its.append(mcq(fig(ld_svg(a, d, quot="digits")) + "The quotient digits are written, but the point is missing. What is %s ÷ %d?" % (a, d),
                       N(ans), [N(raw), N(ans * 10), N(ans / 10), N(ans * 100)], div_e(a, d, est)))
    its.append(mcq("What is 4.5 ÷ 9?", "0.5", ["5", "0.05", "2"],
                   "Estimate: 4.5 is less than 9, so the answer is less than 1. 45 ÷ 9 = 5. Put the point above the point "
                   "in 4.5: 4.5 ÷ 9 = <b>0.5</b>. Check: 0.5 × 9 = 4.5. (2 is 9 ÷ 4.5, the wrong order.)"))
    its.append(mcq("What is 6.3 ÷ 7?", "0.9", ["9", "0.09", "44.1"],
                   "Estimate: 6.3 is less than 7, so the answer is less than 1. 63 ÷ 7 = 9. Put the point above the point "
                   "in 6.3: <b>0.9</b>. Check: 0.9 × 7 = 6.3. (44.1 is 6.3 × 7.)"))
    # dividing by a decimal: make the divisor whole
    for a, b, wrong in [("4.8", "0.6", ["0.8", "80", "0.08"]), ("2.7", "0.3", ["0.9", "90", "0.81"]),
                        ("0.56", "0.08", ["0.7", "70", "0.07"]), ("1.2", "0.04", ["3", "0.3", "300"]),
                        ("4", "0.2", ["2", "0.8", "200"]), ("7.5", "2.5", ["0.3", "30", "18.75"])]:
        k = places(b)
        m = 10 ** k
        A, B = Dm(a) * m, Dm(b) * m
        ans = Dm(a) / Dm(b)
        e = ("Make the divisor a whole number: multiply <b>both</b> numbers by %s. %s ÷ %s = %s ÷ %s = <b>%s</b>. "
             "Check: %s × %s = %s." % (N(m), a, b, N(A), N(B), N(ans), N(ans), b, a))
        if Dm(b) < 1:
            e += " Dividing by a number less than 1 gives an answer bigger than %s." % a
        its.append(mcq("What is %s ÷ %s?" % (a, b), N(ans), wrong, e))
    its.append(mcq("3 ÷ 0.5 asks: how many halves are in 3? What is 3 ÷ 0.5?", "6", ["1.5", "0.6", "60"],
                   "Each whole has 2 halves, so 3 wholes have 3 × 2 = <b>6</b> halves. Or make the divisor whole: "
                   "3 ÷ 0.5 = 30 ÷ 5 = 6. (1.5 is 3 × 0.5.)"))
    its.append(mcq("Which problem has the same answer as 3.6 ÷ 0.4?", "36 ÷ 4", ["3.6 ÷ 4", "36 ÷ 0.4", "360 ÷ 4"],
                   "Multiply both numbers by 10: 3.6 × 10 = 36 and 0.4 × 10 = 4. So 3.6 ÷ 0.4 = <b>36 ÷ 4</b> = 9. "
                   "Move the point the same number of places in <b>both</b> numbers."))
    its.append(mcq("Which problem has the same answer as 1.75 ÷ 0.25?", "175 ÷ 25", ["17.5 ÷ 25", "175 ÷ 2.5", "1.75 ÷ 25"],
                   "0.25 has 2 decimal places, so multiply both numbers by 100: 1.75 → 175 and 0.25 → 25. "
                   "1.75 ÷ 0.25 = <b>175 ÷ 25</b> = 7."))
    its.append(mcq("Without dividing, which is true about 9 ÷ 0.3?", "It is greater than 9",
                   ["It is less than 9", "It equals 3", "It equals 0.3"],
                   "0.3 is less than 1, and many 0.3s fit into 9, so the answer is <b>greater than 9</b>. "
                   "9 ÷ 0.3 = 90 ÷ 3 = 30. (3 is 9 ÷ 3.)"))
    its.append(mcq("4.2 ÷ 6 = 0.7. Which product should equal 4.2 to check this?", "0.7 × 6",
                   ["0.7 × 4.2", "4.2 × 6", "6 ÷ 0.7"],
                   "Quotient × divisor = dividend. <b>0.7 × 6</b> = 4.2, so the answer is right."))
    assert len(its) == 20, len(its)
    return {"title": "Divide decimals", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    n, he, his = P.next()
    its.append(mcq("A notebook costs $2.75. %s buys 4 notebooks. How much does %s pay?" % (n, he), "$11.00",
                   ["$8.75", "$1.10", "$110.00"],
                   "Equal groups, so multiply: 4 × $2.75. Estimate: $2.75 is about $3, and 4 × $3 = $12. "
                   "4 × 275 = 1,100, and 2 decimal places give <b>$11.00</b>. ($8.75 multiplies only the dollars: 4 × 2 + 0.75.)"))
    its.append(mcq("A pack of 6 juice boxes costs $4.50. Each box costs the same. How much is one juice box?", "$0.75",
                   ["$7.50", "$27.00", "$75.00"],
                   "Share $4.50 equally into 6 parts: 4.50 ÷ 6. Estimate: $4.50 is less than $6, so each box costs less than $1. "
                   "450 ÷ 6 = 75. Put the point above the point: <b>$0.75</b>. Check: 6 × $0.75 = $4.50."))
    n, he, his = P.next()
    its.append(mcq("%s cuts a ribbon 3.6 m long into 4 equal pieces. How long is each piece?" % n, "0.9 m",
                   ["9 m", "0.09 m", "14.4 m"],
                   "Divide: 3.6 ÷ 4. Estimate: 3.6 is a bit less than 4, so each piece is a bit less than 1 m. "
                   "36 ÷ 4 = 9, and the point goes above the point: <b>0.9 m</b>. Check: 4 × 0.9 = 3.6."))
    its.append(mcq("A jug holds 2 L of lemonade. How many 0.25 L cups can be filled from it?", "8 cups",
                   ["0.5 cup", "80 cups", "0.125 cup"],
                   "How many 0.25s are in 2? Divide: 2 ÷ 0.25 = 200 ÷ 25 = <b>8</b>. Or: 4 cups make 1 L, so 2 L fill 8 cups. "
                   "(0.5 is 2 × 0.25.)"))
    n, he, his = P.next()
    its.append(mcq("Fabric costs $3.40 per meter. %s buys 2.5 meters. How much does %s pay?" % (n, he), "$8.50",
                   ["$85.00", "$0.85", "$5.90"],
                   "Multiply: 2.5 × $3.40. Estimate: 2.5 × 3 = 7.5, so a bit more than $7.50. 25 × 34 = 850, and 1 + 2 = 3 "
                   "decimal places give 8.500 = <b>$8.50</b>. ($5.90 is the sum.)"))
    n, he, his = P.next()
    its.append(mcq("%s runs 2.4 km every day. How far does %s run in 5 days?" % (n, he), "12 km",
                   ["1.2 km", "120 km", "7.4 km"],
                   "Multiply: 5 × 2.4. Estimate: 5 × 2 = 10, so a bit more than 10 km. 5 × 24 = 120, and 1 decimal place gives "
                   "12.0 = <b>12 km</b>."))
    its.append(mcq("A bag holds 4.5 kg of rice. A family uses 0.4 of the bag in a week. How much rice is that?", "1.8 kg",
                   ["18 kg", "0.18 kg", "4.1 kg"],
                   "“0.4 of” means multiply: 0.4 × 4.5. Estimate: 0.4 is a bit less than half, and half of 4.5 is about 2. "
                   "4 × 45 = 180, and 2 decimal places give 1.80 = <b>1.8 kg</b>. The answer is less than 4.5 because 0.4 &lt; 1."))
    n, he, his = P.next()
    its.append(mcq("A recipe needs 0.75 cup of flour. %s makes 3 batches. How much flour does %s need?" % (n, he), "2.25 cups",
                   ["22.5 cups", "0.225 cup", "3.75 cups"],
                   "Multiply: 3 × 0.75. Estimate: 0.75 is about 1, so a bit less than 3 cups. 3 × 75 = 225, and 2 decimal places "
                   "give <b>2.25 cups</b>. (3.75 adds 3 instead of multiplying.)"))
    its.append(mcq("Five friends share $12 equally. How much does each friend get?", "$2.40",
                   ["$24.00", "$0.24", "$60.00"],
                   "Divide: $12 ÷ 5. Estimate: $10 ÷ 5 = $2, so a bit more than $2. Write 12 as 12.00: 1,200 ÷ 5 = 240, "
                   "so each friend gets <b>$2.40</b>. Check: 5 × $2.40 = $12.00."))
    n, he, his = P.next()
    its.append(mcq("Pencils cost $0.35 each. %s has $2.80. How many pencils can %s buy?" % (n, he), "8",
                   ["80", "0.8", "0.98"],
                   "How many $0.35s are in $2.80? Divide: 2.80 ÷ 0.35 = 280 ÷ 35 = <b>8</b>. Check: 8 × $0.35 = $2.80. "
                   "(0.98 is 2.80 × 0.35: multiplying instead of dividing.)"))
    its.append(mcq("How many 0.5 L bottles can be filled with 6 L of water?", "12",
                   ["3", "1.2", "120"],
                   "Each liter fills 2 bottles of 0.5 L. 6 ÷ 0.5 = 60 ÷ 5 = <b>12</b>. (3 is 6 × 0.5.)"))
    n, he, his = P.next()
    its.append(mcq("%s has a board 2.5 m long. %s cuts it into pieces 0.5 m long. How many pieces does %s get?" % (n, cap(he), he),
                   "5 pieces", ["1.25 pieces", "50 pieces", "0.5 piece"],
                   "Divide: 2.5 ÷ 0.5 = 25 ÷ 5 = <b>5</b>. Check: 5 × 0.5 = 2.5. (1.25 is 2.5 × 0.5.)"))
    its.append(mcq("A garden is 3.5 m long and 2.4 m wide. What is its area?", "8.4 m²",
                   ["84 m²", "0.84 m²", "11.8 m²"],
                   "Area = length × width = 3.5 × 2.4. Estimate: 3.5 × 2 = 7, so a bit more than 7. 35 × 24 = 840, and 2 decimal "
                   "places give 8.40 = <b>8.4 m²</b>. (11.8 is the perimeter.)"))
    n, he, his = P.next()
    its.append(mcq("%s multiplies 4.2 × 3.8 and gets 159.6. Is the answer reasonable?" % n, "No, it should be about 16",
                   ["Yes, it is close", "No, it should be about 1.6", "No, it should be about 8"],
                   "Estimate: 4.2 ≈ 4 and 3.8 ≈ 4, so the product is about 16. 159.6 is 10 times too big: the point is in the wrong place. "
                   "The answer is 15.96."))
    its.append(mcq("Grapes cost $2.40 per pound. How much do 1.5 pounds of grapes cost?", "$3.60",
                   ["$36.00", "$0.36", "$3.90"],
                   "Multiply: 1.5 × $2.40. Estimate: half of 2.40 is 1.20, so 1.5 pounds cost about $2.40 + $1.20. 15 × 24 = 360, "
                   "and 1 + 1 = 2 decimal places give <b>$3.60</b>. ($3.90 is the sum.)"))
    n, he, his = P.next()
    its.append(mcq("%s spends $18.60 on 6 books. Each book costs the same. How much does one book cost?" % n, "$3.10",
                   ["$31.00", "$0.31", "$3.01"],
                   "Divide: 18.60 ÷ 6. Estimate: 18 ÷ 6 = 3, so about $3. 1,860 ÷ 6 = 310, so one book costs <b>$3.10</b>. "
                   "Check: 6 × $3.10 = $18.60."))
    its.append(mcq("A pitcher holds 1.8 L of juice. It is poured equally into 6 glasses. How much juice is in each glass?", "0.3 L",
                   ["3 L", "0.03 L", "10.8 L"],
                   "Divide: 1.8 ÷ 6. Estimate: 1.8 is less than 6, so each glass gets less than 1 L. 18 ÷ 6 = 3, and the point "
                   "goes above the point: <b>0.3 L</b>. Check: 6 × 0.3 = 1.8."))
    its.append(mcq("A nickel is 1.95 mm thick. How tall is a stack of 10 nickels?", "19.5 mm",
                   ["195 mm", "0.195 mm", "11.95 mm"],
                   "Multiply by 10: the point moves 1 place to the right. 1.95 × 10 = <b>19.5 mm</b>. Check: 10 × 2 = 20, so about 20 mm."))
    its.append(mcq("A sheet of paper is 0.1 mm thick. How thick is a stack of 500 sheets?", "50 mm",
                   ["5 mm", "500.1 mm", "5,000 mm"],
                   "Multiply: 500 × 0.1. Multiplying by 0.1 is dividing by 10: 500 ÷ 10 = <b>50 mm</b>."))
    n, he, his = P.next()
    its.append(mcq("%s walks 0.8 km to school each morning and the same way home. How far does %s walk in 5 school days?" % (n, he),
                   "8 km", ["4 km", "80 km", "0.8 km"],
                   "Each day: 0.8 + 0.8 = 1.6 km. In 5 days: 5 × 1.6 = <b>8 km</b>. (4 km counts only the walk to school.)"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: money, length and capacity", "items": its}


# ============================================================ lesson
def body_html():
    f_groups = groups_svg(3, 25, cell=20)
    f_col = column_svg([("", "2.36"), ("×", "4"), ("", "9.44")], [1], "2.36 times 4 worked out in columns: 9.44")
    f_over = overlap_svg(3, 4, cell=20)
    f_div = ld_svg("7.2", 3, quot="full", work=True, fs=26).replace(
        "written as long division", "worked out with long division: 2.4")
    return (
        "<h2>The big idea</h2>"
        "<p>Multiply or divide as if there were <b>no decimal point</b>. Then put the point back in the right place. "
        "An estimate tells you where it goes.</p>"
        "<h2>Multiply and divide by 10, 100 and 1,000</h2>"
        "<p>Each place is 10 times the place to its right. So multiplying by 10 moves every digit one place left, "
        "and the decimal point moves one place right.</p>"
        + table(["Multiply or divide by", "The point moves", "Example"], [
            ["× 10", "1 place right", "3.45 × 10 = 34.5"],
            ["× 100", "2 places right", "0.67 × 100 = 67"],
            ["× 1,000", "3 places right", "2.8 × 1,000 = 2,800"],
            ["÷ 10 (or × 0.1)", "1 place left", "45.6 ÷ 10 = 4.56"],
            ["÷ 100 (or × 0.01)", "2 places left", "73 ÷ 100 = 0.73"],
        ]) +
        "<p>Fill empty places with zeros: 2.8 × 1,000 = 2,800, and 8 × 0.01 = 0.08.</p>"
        "<h2>Decimal × whole number</h2>"
        "<figure class='sn-fig'>" + f_groups +
        "<figcaption>3 × 0.25: three groups of 25 hundredths make 75 hundredths, so 3 × 0.25 = 0.75.</figcaption></figure>"
        "<p>With bigger numbers, multiply as whole numbers, then count the decimal places.</p>"
        "<figure class='sn-fig'>" + f_col +
        "<figcaption>4 × 236 = 944. 2.36 has 2 decimal places, so 4 × 2.36 = 9.44.</figcaption></figure>"
        + ex("Example", "What is 6 × 1.25?",
             "Estimate: 6 × 1 = 6, so a bit more than 6. 6 × 125 = 750. 1.25 has 2 decimal places: 7.50.", "7.5")
        + "<h2>Decimal × decimal</h2>"
        "<p>On a hundredths grid, shade 0.3 of the columns and 0.4 of the rows. The overlap is the product.</p>"
        "<figure class='sn-fig'>" + f_over +
        "<figcaption>3 columns × 4 rows = 12 squares overlap. Each square is 0.01, so 0.3 × 0.4 = 0.12. Tenths × tenths = hundredths.</figcaption></figure>"
        "<p><b>Count the decimal places</b> in both factors. The product has that many.</p>"
        + table(["Problem", "Whole numbers", "Decimal places", "Product"], [
            ["0.3 × 0.4", "3 × 4 = 12", "1 + 1 = 2", "0.12"],
            ["2.3 × 1.4", "23 × 14 = 322", "1 + 1 = 2", "3.22"],
            ["0.5 × 0.12", "5 × 12 = 60", "1 + 2 = 3", "0.060 = 0.06"],
        ]) +
        "<h2>Dividing decimals</h2>"
        "<p>To divide by a whole number, divide as usual and put the point in the quotient <b>straight above</b> "
        "the point in the dividend.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>7.2 ÷ 3: 7 ÷ 3 = 2, 1 left. Bring down 2: 12 ÷ 3 = 4. The point goes above the point: 2.4.</figcaption></figure>"
        "<p>To divide by a decimal, first <b>make the divisor a whole number</b>. Multiply both numbers by 10 (or 100). "
        "The answer does not change.</p>"
        + ex("Example", "What is 4.8 ÷ 0.6?",
             "Multiply both by 10: 4.8 ÷ 0.6 = 48 ÷ 6 = 8. Check: 8 × 0.6 = 4.8.", "8")
        + "<h2>Estimate to check</h2>"
        "<p>Round to easy numbers first. 2.9 × 4.1 is about 3 × 4 = 12, so 11.89 makes sense and 118.9 does not. "
        "Multiplying by a number less than 1 makes the answer <b>smaller</b>; dividing by a number less than 1 makes it <b>bigger</b>.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["0.3 × 0.4 = 1.2", "Count the decimal places: 1 + 1 = 2, so 0.12"],
            ["3.45 × 10 = 3.450", "Move the point: 34.5. Adding a zero at the end does not change the value"],
            ["Thinking 8 × 0.5 is more than 8", "Multiplying by less than 1 makes it smaller: 8 × 0.5 = 4"],
            ["8.16 ÷ 4 = 2.4", "Write 0 when the divisor does not fit: 2.04"],
            ["4.8 ÷ 0.6 = 4.8 ÷ 6", "Move the point in both numbers: 48 ÷ 6 = 8"],
        ])
    )


FAQ = [
    {"q": "How do you multiply decimals in 5th grade?",
     "a": "Multiply as if there were no decimal points, then count the decimal places in both factors and give the product that many. For 2.3 × 1.4: 23 × 14 = 322, and 1 + 1 = 2 places gives 3.22."},
    {"q": "How do you divide a decimal by a decimal?",
     "a": "Multiply both numbers by 10 or 100 so the divisor becomes a whole number, then divide. 4.8 ÷ 0.6 = 48 ÷ 6 = 8."},
    {"q": "Why does multiplying by a decimal make a number smaller?",
     "a": "Multiplying by a number less than 1 takes only part of the number. 8 × 0.5 is half of 8, which is 4."},
    {"q": "What does 5.NBT.B.7 mean?",
     "a": "It is the Common Core Grade 5 standard for adding, subtracting, multiplying and dividing decimals to hundredths, using models, place value and properties, and explaining the reasoning."},
]


def gen():
    rnd = random.Random(505)
    P = People(rnd)
    sets = [set_powers(), set_mul_whole(), set_mul_dec(P), set_divide(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "multiply-divide-decimals", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiply and Divide Decimals",
        "seo_title": "Grade 5 Multiplying and Dividing Decimals Worksheets: Powers of 10, Decimal Grids, Placing the Decimal Point and Word Problems",
        "short_title": "Multiply and divide decimals",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "5.NBT.B.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NBT/B/7/",
        "standard_text": "Add, subtract, multiply, and divide decimals to hundredths, using concrete models or drawings and strategies based on place value, properties of operations, and/or the relationship between addition and subtraction; relate the strategy to a written method and explain the reasoning used.",
        "meta_desc": "Free Grade 5 worksheets on multiplying and dividing decimals: multiply and divide by 10, 100 and 0.1, decimal × whole number, decimal × decimal on a hundredths grid, long division with decimals, dividing by a decimal and money word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Multiply or divide as if there were no point. Then put the point where an estimate says it belongs.",
        "key_sub": "Multiplying: the product has as many decimal places as both factors together (0.3 × 0.4 = 0.12). Dividing: put the point straight above the point, and make a decimal divisor whole first (4.8 ÷ 0.6 = 48 ÷ 6).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundredths grids) so the small squares stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "hundredths grid")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
