# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Multiplication and Division (MOE 2021 Primary Mathematics Syllabus, Standard,
Number and Algebra, Whole Numbers: "Division with remainder; multiplication and division algorithms
(up to 3 digits by 1 digit)")
  python3 tools/gen_sg_maths_p3_mult_div.py
2- and 3-digit × 1-digit with renaming, division with remainder (with pictures), 2- and 3-digit ÷ 1-digit
(long division), what the remainder means, and word problems with bar models.
Wrong answers come from real mistakes: not adding the renamed digit, adding it before multiplying,
writing every product in full, a remainder bigger than the divisor, ignoring the remainder,
not renaming in division, a missing 0 in the quotient, not rounding up.
Helpers adapted from gen_sg_maths_p4_division.py and gen_sg_maths_p4_multiplication.py
(themselves from gen_cabc_math_g4_mult_div.py and gen_uk_maths_y4_short_multiplication.py).
Singapore English. Numbers up to 10 000 (4 digits without a separator). HTML attributes use single quotes.
Every answer is computed in code.
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
GREY = "#6b6259"
INK = "#2b2b2b"
BLUE = "#2f6fb0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
NBSP = " "
PLACES = ["thousands", "hundreds", "tens", "ones"]
ONE = {"thousands": "thousand", "hundreds": "hundred", "tens": "ten", "ones": "one"}


# ------------------------------------------------------------ helpers
def f(n):
    """Singapore style: 4536, 10 000 (no-break space only from 5 digits)."""
    if abs(n) < 10000:
        return str(n)
    return "{:,}".format(n).replace(",", NBSP)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def cval(c):
    """Value of a choice: '12 boxes' -> 12, '8 R 1' -> ('R', 8, 1), '$216' -> 216."""
    t = re.sub(r"<[^>]+>", " ", c).replace("$", " ")
    m = re.match(r"^\s*(\d+) R (\d+)\s*$", t)
    if m:
        return ("R", int(m.group(1)), int(m.group(2)))
    v, found = Fraction(0), False
    for tok in t.split():
        if re.match(r"^\d+$", tok):
            v += Fraction(tok)
            found = True
    return v if found else c


def mcq(q, correct, cands, e, values=None, allow_zero=False):
    """4 choices: correct + the first 3 usable distractors (no zero or negative leads, no equal values)."""
    correct = str(correct)
    seen = {correct}
    vals = {values(correct)} if values else set()
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or (lead == "0" and not allow_zero):
            continue
        if values:
            v = values(c)
            if v in vals:
                continue
            vals.add(v)
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcqv(q, correct, cands, e):
    return mcq(q, correct, cands, e, values=cval)


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


def units(k, one, many):
    return "%s %s" % (f(k), one if k == 1 else many)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, family=FONT):
    w, h = int(round(w + 0.49)), int(round(h + 0.49))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def T(x, y, s, size=16, fill=INK, anchor="middle", weight="700", mono=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, size, weight, fill, anchor, " font-family='monospace'" if mono else "", s))


def tw(s, size=15):
    return len(s) * size * 0.58


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


# ------------------------------------------------------------ multiplication: steps and mistakes
def carry_list(a, d):
    """Renamed digit going INTO each column (index = column from the right)."""
    c, out = 0, {}
    ds = digits(a)
    for i, x in enumerate(ds):
        p = x * d + c
        c = p // 10
        if c and i < len(ds) - 1:
            out[i + 1] = c
    return out


def steps_1d(a, d):
    ds = digits(a)
    names = ["ones", "tens", "hundreds"]
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d %s × %d" % (x, ONE[names[i]] if x == 1 else names[i], d) + (" + %d" % c if c else "")
        if i == len(ds) - 1 or p < 10:
            out.append("%s = %d" % (ex_, p))
        else:
            out.append("%s = %d, write %d and rename %d %s" % (ex_, p, p % 10, p // 10,
                                                                ONE[names[i + 1]] if p // 10 == 1 else names[i + 1]))
        c = p // 10 if i < len(ds) - 1 else 0
    return "; ".join(out)


def mult_row(a, d, mode="ok", k=None):
    """a × d done with a typical mistake.
    nocarry: forget every renamed digit. skip: forget the one made in place k.
    cfirst: add the renamed digit BEFORE multiplying."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        p = (x + c) * d if mode == "cfirst" else x * d + c
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
            if mode == "nocarry" or (mode == "skip" and k == i):
                c = 0
    return r


def concat_1d(a, d):
    """Writes every product in full, no renaming: 49 × 6 -> 24|54."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def cands_1d(a, d):
    p = a * d
    return [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", 0),
            mult_row(a, d, "skip", 1), concat_1d(a, d), a + d, p + 10, p - 10, p + 100]


def place_parts(a):
    s = str(a)
    return [int(ch) * 10 ** (len(s) - 1 - i) for i, ch in enumerate(s) if ch != "0"]


# ------------------------------------------------------------ division: steps and mistakes
def div_rows(n, d):
    """Long division: list of (digit index, number divided, quotient digit or None, remainder)."""
    ds = [int(c) for c in str(n)]
    cur, rows, started = 0, [], False
    for i, x in enumerate(ds):
        cur = cur * 10 + x
        if not started and cur < d and i < len(ds) - 1:
            rows.append((i, cur, None, cur))
            continue
        started = True
        q, r = divmod(cur, d)
        rows.append((i, cur, q, r))
        cur = r
    return rows


def pl(k, place):
    return "%d %s" % (k, ONE[place] if k == 1 else place)


def pv_steps(n, d, end=True):
    """Divide place by place from the left; rename what is left as the next place."""
    L = len(str(n))
    names = PLACES[-L:]
    rows = div_rows(n, d)
    out = []
    for k, (i, cur, q, r) in enumerate(rows):
        last = k == len(rows) - 1
        place = names[i]
        if not last:
            nxt_place = names[i + 1]
            nxt = rows[k + 1][1]
            tail = "" if nxt == (cur if q is None else r) * 10 else ": " + pl(nxt, nxt_place)
        if q is None:
            out.append("%s ÷ %d: not enough to share. Rename as %s%s." % (pl(cur, place), d, pl(cur * 10, nxt_place), tail))
        elif last:
            out.append("%s ÷ %d = %s." % (pl(cur, place), d, ("%d R %d" % (q, r)) if r else pl(q, place)))
        elif q == 0:
            if r:
                out.append("%s ÷ %d = 0: write 0 in the %s place. Rename %s as %s%s."
                           % (pl(cur, place), d, place, pl(r, place), pl(r * 10, nxt_place), tail))
            else:
                out.append("0 %s ÷ %d = 0: write 0 in the %s place." % (place, d, place))
        elif r:
            out.append("%s ÷ %d = %s, %s left. Rename %s as %s%s."
                       % (pl(cur, place), d, pl(q, place), pl(r, place), pl(r, place), pl(r * 10, nxt_place), tail))
        else:
            out.append("%s ÷ %d = %s." % (pl(cur, place), d, pl(q, place)))
    q, r = divmod(n, d)
    if end:
        return " ".join(out) + " Answer: %s. %s" % (qr(q, r), check_txt(n, d))
    return " ".join(out)


def digitwise(n, d):
    """Each digit divided on its own, nothing renamed (72 ÷ 4 -> 10)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def zero_slips(q):
    """A 0 inside the quotient left out (103 -> 13)."""
    s = str(q)
    out = []
    for i in range(1, len(s)):
        if s[i] == "0":
            out.append(int(s[:i] + s[i + 1:]))
    return [x for x in out if x != q]


def cands_div(n, d):
    q = n // d
    c = list(zero_slips(q))
    dw = digitwise(n, d)
    if dw != q and dw * 2 > q:
        c.append(dw)
    c += [q * 10, q + 1, q - 1, q + 10, q - 10, q + 2]
    return [f(x) for x in c]


def cands_rem(n, d):
    q, r = divmod(n, d)
    c = [qr(z, r) for z in zero_slips(q)]
    return c + [qr(q - 1, r + d) if q > 1 else None,   # remainder bigger than the divisor
                f(q),                                  # remainder ignored
                qr(q, d - r) if d - r != r else None,  # wrote how many more are needed
                qr(q + 1, r), qr(q - 1, r) if q > 1 else None, qr(q * 10, r)]


# ------------------------------------------------------------ figures
def column_svg(rows, rule, label):
    """Multiplication in columns, ones lined up on the right.
    rows = list of (sign, text); sign 'ex' = a row of small renamed digits: text is a dict {place: digit}.
    A '?' digit is drawn red. A line is drawn under row index `rule`."""
    fs = 26
    cw = fs * 0.78
    efs = 15
    lens = [(max(t) + 1 if t else 0) if sg == "ex" else len(t) for sg, t in rows]
    nd = max(lens)
    signed = max([n for (sg, t), n in zip(rows, lens) if sg and sg != "ex"] or [0])
    sign_slot = max(nd, signed + 1)
    slots = sign_slot + 1
    W = cw * slots + 20
    right = W - 10
    s = []
    y = 10
    for r, (sg, t) in enumerate(rows):
        if sg == "ex":
            y += efs + 4
            for i, v in sorted(t.items()):
                s.append(T(right - cw * (i + 0.5), y - 2, str(v), efs, GREEN))
            continue
        y += fs * 1.2
        for slot, ch in enumerate(reversed(t)):
            s.append(T(right - cw * (slot + 0.5), y - 2, ch, fs, RED if ch == "?" else INK))
        if sg:
            s.append(T(right - cw * (sign_slot + 0.5), y - 2, sg, fs, GREEN))
        if r == rule:
            y += 5
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
            y += 5
    return svg_wrap(W, y + 12, "".join(s), label, "monospace")


def col_problem(a, d):
    return column_svg([("", str(a)), ("×", str(d))], 1, "%d times %d written in columns" % (a, d))


def long_svg(n, d, work=False, label=None):
    """Long division: divisor, bracket and dividend. With work=True the quotient and every step are shown."""
    fs, cw, rh = 22, 17, 29
    ds = str(n)
    L = len(ds)
    x0 = 10 + len(str(d)) * 14 + 16
    top = (rh + 4) if work else 6
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def put(num, end_col, y, colr=INK):
        t = str(num)
        for k, ch in enumerate(t):
            s.append(T(col(end_col - len(t) + 1 + k), y, ch, fs, colr, mono=True))

    by = top + rh - 7
    put(n, L - 1, by)
    s.append(T(x0 - 12, by, str(d), fs, GREEN, "end", mono=True))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (x0 - 6, top, x0 + 2, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 6
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>" % (x0 - 6, top, W - 2, top, INK))
    H = top + bh + 6
    if work:
        rows = div_rows(n, d)
        y = by
        for k, (i, cur, q, r) in enumerate(rows):
            if q is None:
                continue
            s.append(T(col(i), top - 8, str(q), fs, GREEN, mono=True))
            p = q * d
            y += rh
            put(p, i, y)
            a = col(i - len(str(cur)) + 1) - cw / 2
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (a, y + 6, col(i) + cw / 2, y + 6, INK))
            y += rh
            if k == len(rows) - 1:
                put(r, i, y, RED if r else INK)
            else:
                put(r * 10 + int(ds[i + 1]), i + 1, y)
        q, r = divmod(n, d)
        if r:
            rt = "R %d" % r
            s.append(T(x0 + cw * L + 8, top - 8, rt, fs, RED, "start", mono=True))
            W = max(W, x0 + cw * L + 8 + len(rt) * fs * 0.62 + 4)
        H = y + 10
    lab = label or ("%d divided by %d worked out with long division" if work else "%d divided by %d written as long division") % (n, d)
    return svg_wrap(W, H, "".join(s), lab)


def dots_svg(n, d, label=None):
    """n counters put in groups of d: each group is a column; leftovers in red at the end."""
    q, r = divmod(n, d)
    R, gap = 7, 19
    s = []
    x = 6
    for g in range(q + (1 if r else 0)):
        k = d if g < q else r
        colr = GREEN if g < q else RED
        if g < q:
            s.append("<rect x='%.1f' y='3' width='%d' height='%d' rx='9' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (x - 3, 2 * R + 6, d * gap + 2, GREY))
        for j in range(k):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + R, 4 + gap / 2 + 1 + j * gap, R, colr))
        x += 2 * R + 6 + (8 if g == q - 1 else 5)
    return svg_wrap(x, d * gap + 8, "".join(s), label or "%d counters in groups of %d" % (n, d))


DISC = {100: ("#cfe6d6", GREEN), 10: ("#d7e6f5", BLUE), 1: ("#fbe8c8", "#9a6a12")}


def discs_svg(n, label=None):
    """Place-value discs: one row each for hundreds, tens and ones."""
    R, gap = 16, 37
    s = []
    digs = [int(c) for c in "%03d" % n]
    y = 6 + R
    maxk = max(digs)
    for val, k in zip((100, 10, 1), digs):
        fill, stroke = DISC[val]
        for j in range(k):
            cx = 6 + R + j * gap
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, y, R, fill, stroke))
            s.append(T(cx, y + 5, str(val), 14, stroke))
        y += 2 * R + 6
    return svg_wrap(12 + 2 * R + (maxk - 1) * gap, y - R, "".join(s),
                    label or "place-value discs showing %d" % n)


def groups_svg(a, k, label=None):
    """k equal groups of a (2-digit), each a row of ten-discs and one-discs."""
    R, gap = 15, 35
    tens, ones = a // 10, a % 10
    s = []
    y = 6 + R
    for g in range(k):
        x = 6 + R
        for val, cnt in ((10, tens), (1, ones)):
            fill, stroke = DISC[val]
            for j in range(cnt):
                s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, R, fill, stroke))
                s.append(T(x, y + 5, str(val), 14, stroke))
                x += gap
            x += 10
        y += 2 * R + 6
    W = 12 + 2 * R + (tens + ones - 1) * gap + 10
    return svg_wrap(W, y - R + 2, "".join(s), label or "%d groups of %d in place-value discs" % (k, a))


SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=320, label="bar model"):
    """Bar model drawn to scale.
    rows: [(name, [(value, text, style)])], style u (unit, green), o (other, grey), w (white).
    top: (v0, v1, text) bracket over row 0; under: [(row, v0, v1, text)] brackets under a row;
    right: text for a bracket on the right joining all rows. Text '?' is drawn in red."""
    names = [n for n, _ in rows]
    nw = max([tw(n, 15) for n in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 34
    out = []
    y = 38 if top else 8
    ys = []
    for i, (n, segs) in enumerate(rows):
        ys.append(y)
        y += bh + (38 if any(u[0] == i for u in under) else 16)
    Hh = y - 16 + 8 if not any(u[0] == len(rows) - 1 for u in under) else y - 38 + 44

    def col(t):
        return RED if t == "?" else INK

    for i, (n, segs) in enumerate(rows):
        ry = ys[i]
        if n:
            out.append(T(8, ry + 23, n, 15, INK, "start"))
        x = x0
        for v, t, st in segs:
            w = v * sc
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, ry, w, bh, SEGFILL[st], GREEN))
            if t:
                assert tw(t, 15) + 4 <= w, (t, w)
                out.append(T(x + w / 2, ry + 23, t, 15, col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(T((a + b) / 2, ry - 16, t, 16, col(t)))
    for r, v0, v1, t in under:
        a, b = x0 + v0 * sc, x0 + v1 * sc
        yb = ys[r] + bh
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, yb + 4, yb + 11, b, yb + 4, RED if t == "?" else INK))
        out.append(T((a + b) / 2, yb + 30, t, 16, col(t)))
    W = x0 + BW + 8
    if right:
        xr = x0 + BW + 8
        y0, y1 = ys[0], ys[-1] + bh
        out.append("<path d='M%.1f %d H%.1f V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (xr, y0, xr + 8, y1, xr, INK))
        out.append(T(xr + 14, (y0 + y1) / 2 + 6, right, 16, col(right), "start"))
        W = xr + 14 + tw(right, 16) + 8
    return svg_wrap(W, Hh, "".join(out), label)


def share_model(total, d, label=None):
    """Total shared into d equal units; '?' under one unit."""
    return model_svg([("", [(1, "", "u")] * d)], top=(0, d, total), under=[(0, 0, 1, "?")],
                     label=label or "bar model: %s shared into %d equal units" % (total, d))


def groups_model(each, k, label=None):
    """k equal units of `each`; '?' for the total over the top."""
    return model_svg([("", [(1, each, "u")] * k)], top=(0, k, "?"),
                     label=label or "bar model: %d units of %s" % (k, each))


# ------------------------------------------------------------ set 1: multiplication with renaming
WHAT1 = ["Did not add the renamed digit", "Added before multiplying", "Did not rename at all",
         "Multiplied only the ones digit"]


def compute_1d_item(a, d, col):
    q = (fig(col_problem(a, d)) + "Multiply.") if col else "Find the value of %d × %d." % (a, d)
    e = "Start with the ones. %s. So %d × %d = %s." % (cap(steps_1d(a, d)), a, d, f(a * d))
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], e)


def missing_digit_item(a, d):
    """The product with one digit shown as a red ?: a column that had a renamed digit added."""
    p = str(a * d)
    cl = carry_list(a, d)
    k = max(cl)
    pos = len(p) - 1 - k
    ans = int(p[pos])
    shown = p[:pos] + "?" + p[pos + 1:]
    cand = []
    for m in (mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", k - 1)):
        s = str(m).zfill(len(p))
        cand.append(int(s[len(s) - 1 - k]))
    x = digits(a)[k]
    cand += [x * d % 10, cl[k], (ans + 1) % 10, (ans + 9) % 10]
    q = (fig(column_svg([("", str(a)), ("×", str(d)), ("", shown)], 1, "%d times %d with one digit missing" % (a, d)))
         + "Which digit is missing from the answer?")
    e = ("Work from the ones: %s. In that column, %d × %d + %d = %d, so the missing digit is %d. %d × %d = %s."
         % (steps_1d(a, d), x, d, cl[k], x * d + cl[k], int(str(x * d + cl[k])[-1]), a, d, f(a * d)))
    assert int(str(x * d + cl[k])[-1]) == ans or k == len(str(a)) - 1
    return mcq(q, str(ans), [str(c) for c in cand], e, allow_zero=True)


def what_1d_item(a, d, kind, P):
    n, he, his = P.next()
    if kind == 0:
        got = mult_row(a, d, "nocarry")
        why = "%s wrote the ones digit of each product but did not add the renamed digit." % n
    elif kind == 1:
        got = mult_row(a, d, "cfirst")
        x = digits(a)[1]
        c = carry_list(a, d)[1]
        why = ("%s added the renamed digit first: (%d + %d) × %d. Multiply first, then add: %d × %d + %d."
               % (n, x, c, d, x, d, c))
    else:
        got = concat_1d(a, d)
        why = "%s wrote each product in full (%s) instead of renaming the tens into the next column." % (
            n, ", ".join(str(x * d) for x in reversed(digits(a))))
    assert got != a * d
    why += " Correct: %s. So %d × %d = %s." % (steps_1d(a, d), a, d, f(a * d))
    q = (fig(column_svg([("", str(a)), ("×", str(d)), ("", str(got))], 1, "%d times %d with a mistake" % (a, d)))
         + "%s worked out %d × %d like this. What mistake did %s make?" % (n, a, d, he))
    ans = WHAT1[kind]
    return mcq(q, ans, [w for w in WHAT1 if w != ans], why)


def set_multiply(P):
    its = []
    for i, (a, d) in enumerate([(47, 6), (38, 4), (69, 3), (86, 7), (58, 9), (74, 8)]):
        assert carry_list(a, d)
        its.append(compute_1d_item(a, d, i % 2 == 0))
    for i, (a, d) in enumerate([(236, 4), (158, 6), (347, 5), (469, 7), (673, 9)]):
        assert len(carry_list(a, d)) >= 1
        its.append(compute_1d_item(a, d, i % 2 == 1))
    for a, d in [(57, 8), (264, 7)]:
        its.append(missing_digit_item(a, d))
    for kind, (a, d) in enumerate([(68, 7), (256, 3), (49, 6)]):
        its.append(what_1d_item(a, d, kind, P))
    for a, d in [(47, 6), (325, 4)]:
        ps = place_parts(a)
        right = " + ".join("%d × %d" % (p, d) for p in ps)
        wrong = ["%d × %d + %s" % (ps[0], d, " + ".join(str(p) for p in ps[1:])),
                 " + ".join("%d × %d" % (int(c), d) for c in str(a)),
                 "%s + %d × %d" % (" + ".join(str(p) for p in ps[:-1]), ps[-1], d)]
        e = ("Split %d by place value: %s. Every part must be multiplied by %d: %s = %s."
             % (a, " + ".join(str(p) for p in ps), d, " + ".join(f(p * d) for p in ps), f(a * d)))
        its.append(mcq("Which is equal to %d × %d?" % (a, d), right, wrong, e))
    a, k = 26, 3
    its.append(mcq(fig(groups_svg(a, k)) + "The discs show 3 groups of 26. Find the value of 26 × 3.", "78",
                   ["618", "68", "69", "29"],
                   "Ones: 3 × 6 ones = 18 ones. Rename 10 ones as 1 ten: 1 ten 8 ones. "
                   "Tens: 3 × 2 tens = 6 tens, and 6 + 1 = 7 tens. So 26 × 3 = 78."))
    assert 26 * 3 == 78 and mult_row(26, 3, "nocarry") == 68 and concat_1d(26, 3) == 618
    its.append(mcq("Find the value of 60 × 7.", "420", ["42", "4200", "67"],
                   "6 tens × 7 = 42 tens = 420. Think of the fact 6 × 7 = 42, then add the 0 for tens."))
    return {"title": "Multiply 2- and 3-digit numbers by 1-digit numbers", "items": its}


# ------------------------------------------------------------ set 2: division with remainder (pictures)
def set_remainder_pictures(P):
    its = []
    for n, d in [(13, 4), (17, 5), (22, 3), (26, 4), (19, 6), (23, 5), (31, 6)]:
        q, r = divmod(n, d)
        assert r
        e = ("There are %d groups of %d and %s left over (in red). %d is less than %d, so it cannot make another group. "
             "%d ÷ %d = %s. %s" % (q, d, units(r, "counter", "counters"), r, d, n, d, qr(q, r), check_txt(n, d)))
        its.append(mcqv(fig(dots_svg(n, d)) + "The picture shows %d counters in groups of %d. Find the value of %d ÷ %d." % (n, d, n, d),
                        qr(q, r), cands_rem(n, d), e))
    for n, d in [(14, 3), (27, 5)]:
        q, r = divmod(n, d)
        its.append(mcq(fig(dots_svg(n, d)) + "Which division does the picture show?",
                       "%d ÷ %d = %s" % (n, d, qr(q, r)),
                       ["%d ÷ %d = %d" % (n, d, q), "%d ÷ %d = %s" % (n, d, qr(q - 1, r + d)), "%d ÷ %d = %d" % (q * d, d, q)],
                       "%d counters make %d groups of %d, with %d left over. So %d ÷ %d = %s. %s"
                       % (n, q, d, r, n, d, qr(q, r), check_txt(n, d))))
    for n, d, thing in [(20, 6, "buttons"), (25, 4, "marbles")]:
        q, r = divmod(n, d)
        its.append(mcq(fig(dots_svg(n, d, "%d counters in groups of %d" % (n, d))) +
                       "%s %d %s are put into bags of %d. How many %s are left over?" % ("The picture shows how", n, thing, d, thing),
                       str(r), [str(q), str(d - r), str(d), str(r + d)],
                       "%d ÷ %d = %s. There are %d full bags and %d left over (in red)." % (n, d, qr(q, r), q, r)))
    for n, d in [(29, 6), (38, 7), (50, 8)]:
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                       [str(q), str(d - r) if d - r != r else None, str(d), str(r + d)],
                       "%d × %d = %d, and %d − %d = %d. So %d ÷ %d = %s. The question asks for the remainder: %d."
                       % (q, d, q * d, n, q * d, r, n, d, qr(q, r), r)))
    for n, d in [(44, 7), (58, 9), (35, 8)]:
        q, r = divmod(n, d)
        its.append(mcqv("Find the value of %d ÷ %d." % (n, d), qr(q, r), cands_rem(n, d),
                        "Use the multiplication table of %d. %d × %d = %d is the biggest product not more than %d. "
                        "%d − %d = %d left over. So %d ÷ %d = %s. %s"
                        % (d, q, d, q * d, n, n, q * d, r, n, d, qr(q, r), check_txt(n, d))))
    name, he, his = P.next()
    its.append(mcq("%s says 30 ÷ 4 = 6 R 6. What mistake did %s make?" % (name, he), "The remainder is too big",
                   ["%s ignored the remainder" % cap(he), "%s divided the wrong way" % cap(he), "There is no mistake"],
                   "The remainder must be smaller than the divisor. 6 is bigger than 4, so one more group of 4 fits. "
                   "30 ÷ 4 = 7 R 2. Check: 7 × 4 + 2 = 30."))
    its.append(mcq("You divide a number by 4. Which of these could be the remainder?", "3", ["4", "5", "6"],
                   "A remainder is always smaller than the divisor. When you divide by 4, the remainder can only be 0, 1, 2 or 3."))
    q, d, r = 7, 5, 2
    n = q * d + r
    its.append(mcq("In a division, the quotient is 7, the divisor is 5 and the remainder is 2. What number was divided?",
                   str(n), [str(q * d), str(q * d - r), str(q + d + r)],
                   "Work backwards: multiply, then add the remainder. 7 × 5 = 35, and 35 + 2 = 37. Check: 37 ÷ 5 = 7 R 2."))
    return {"title": "Division with remainder", "items": its}


# ------------------------------------------------------------ set 3: 2- and 3-digit ÷ 1-digit
def set_long_division(P):
    its = []
    for i, (n, d) in enumerate([(72, 4), (84, 6), (96, 8), (75, 3)]):
        assert n % d == 0
        its.append(mcq((fig(long_svg(n, d)) + "Divide.") if i < 2 else "Find the value of %d ÷ %d." % (n, d),
                       f(n // d), cands_div(n, d), pv_steps(n, d)))
    for i, (n, d) in enumerate([(87, 5), (65, 4)]):
        q, r = divmod(n, d)
        its.append(mcqv((fig(long_svg(n, d)) + "Divide.") if i == 0 else "Find the value of %d ÷ %d." % (n, d),
                        qr(q, r), cands_rem(n, d), pv_steps(n, d)))
    for i, (n, d) in enumerate([(536, 4), (918, 6), (672, 7), (424, 8)]):
        assert n % d == 0
        its.append(mcq((fig(long_svg(n, d)) + "Divide.") if i % 2 == 0 else "Find the value of %d ÷ %d." % (n, d),
                       f(n // d), cands_div(n, d), pv_steps(n, d)))
    for i, (n, d) in enumerate([(547, 4), (835, 6), (293, 5)]):
        q, r = divmod(n, d)
        assert r
        cands = cands_rem(n, d)
        dw = digitwise(n, d)
        if dw != q and int(str(n)[0]) >= d:
            cands.insert(1, qr(dw, r))
        its.append(mcqv((fig(long_svg(n, d)) + "Divide.") if i == 1 else "Find the value of %d ÷ %d." % (n, d),
                        qr(q, r), cands, pv_steps(n, d)))
    for n, d in [(156, 3), (348, 3)]:
        q = n // d
        assert n % d == 0
        its.append(mcq(fig(discs_svg(n)) + "The place-value discs show %d. Share them equally into %d groups. "
                       "What number is in each group?" % (n, d), f(q),
                       [f(digitwise(n, d)), f(q + 10), f(q - 1), f(n - q)], pv_steps(n, d)))
    n, d, q = 952, 7, 136
    assert n // d == q and n % d == 0
    its.append(mcq("Which multiplication checks that 952 ÷ 7 = 136?", "136 × 7 = 952",
                   ["952 × 7 = 6664", "136 × 9 = 1224", "136 + 7 = 143"],
                   "Multiply the answer by the number you divided by: 136 × 7 = 952. "
                   "That is the number you started with, so the answer is correct."))
    assert 952 * 7 == 6664 and 136 * 9 == 1224
    nm, he, his = P.next()
    assert 618 // 6 == 103
    its.append(mcq("%s says 618 ÷ 6 = 13. What mistake did %s make?" % (nm, he), "%s left out the 0 in the tens place" % cap(he),
                   ["%s divided the wrong way" % cap(he), "%s ignored a remainder" % cap(he), "There is no mistake"],
                   "6 hundreds ÷ 6 = 1 hundred. 1 ten ÷ 6 = 0: write 0 in the tens place. Rename 1 ten as 10 ones: 18 ones. "
                   "18 ones ÷ 6 = 3 ones. The answer is 103, not 13. Check: 103 × 6 = 618."))
    assert 256 // 8 == 32
    its.append(mcq("How many digits does the answer to 256 ÷ 8 have?", "2 digits", ["3 digits", "1 digit", "4 digits"],
                   "2 hundreds ÷ 8: not enough to share, so there are no hundreds in the answer. Rename as 20 tens: 25 tens. "
                   "25 tens ÷ 8 = 3 tens, 1 ten left. Rename as 10 ones: 16 ones. 16 ÷ 8 = 2. 256 ÷ 8 = 32, which has 2 digits."))
    opts = [234, 235, 236, 233]
    assert [n % 6 == 0 for n in opts] == [True, False, False, False]
    e = "Divide each one: " + "; ".join("%d ÷ 6 = %s" % (n, qr(*divmod(n, 6))) for n in opts) + \
        ". Only 234 ÷ 6 = 39 has no remainder. Check: 39 × 6 = 234."
    its.append(mcq("Which division has no remainder?", "234 ÷ 6", ["235 ÷ 6", "236 ÷ 6", "233 ÷ 6"], e))
    its.append(mcq("To find 75 ÷ 3, Kavya writes 7 tens ÷ 3 = 2 tens, with 1 ten left. What should she do with the 1 ten?",
                   "Rename it as 10 ones", ["Write it as the remainder", "Leave it out", "Add it to the 2 tens"],
                   "The 1 ten left over must still be shared. Rename it as 10 ones: 10 + 5 = 15 ones. "
                   "15 ones ÷ 3 = 5 ones. So 75 ÷ 3 = 25."))
    return {"title": "Divide 2- and 3-digit numbers by 1-digit numbers", "items": its}


# ------------------------------------------------------------ set 4: what the remainder means
def up_item(t, n, d, one, many, who, who1, svg=None):
    q, r = divmod(n, d)
    ans = units(q + 1, one, many)
    e = ("%d ÷ %d = %s. %s are not enough: %s still %s a place. Round up to %s."
         % (n, d, qr(q, r), cap(units(q, one, many)), units(r, who1, who), "needs" if r == 1 else "need", ans))
    return mcqv((fig(svg) if svg else "") + t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e)


def down_item(t, n, d, one, many, why, svg=None):
    q, r = divmod(n, d)
    ans = units(q, one, many)
    e = "%d ÷ %d = %s. %s Leave the remainder out: the answer is %s." % (n, d, qr(q, r), why, ans)
    return mcqv((fig(svg) if svg else "") + t, ans,
                [units(q + 1, one, many), qr(q, r), units(r, one, many), units(q - 1, one, many)], e)


def left_item(t, n, d, one, many, svg=None):
    q, r = divmod(n, d)
    ans = units(r, one, many)
    e = ("%d ÷ %d = %s (%d × %d = %d, %d − %d = %d). The question asks how many are left over, so the answer is the remainder: %s."
         % (n, d, qr(q, r), q, d, q * d, n, q * d, r, ans))
    return mcqv((fig(svg) if svg else "") + t, ans,
                [units(q, one, many), units(d - r, one, many) if d - r != r else None, qr(q, r),
                 units(d, one, many), units(r + d, one, many)], e)


def set_meaning(P):
    its = []
    its.append(up_item("34 pupils go kayaking at East Coast Park. Each kayak holds 4 pupils. How many kayaks are needed?",
                       34, 4, "kayak", "kayaks", "pupils", "pupil"))
    its.append(up_item("Farah has 45 photos for an album. Each page holds 6 photos. How many pages does she need for all of them?",
                       45, 6, "page", "pages", "photos", "photo"))
    its.append(up_item("There are 39 guests at a Hari Raya open house. Each table seats 4 guests. How many tables are needed?",
                       39, 4, "table", "tables", "guests", "guest"))
    its.append(up_item("Mr Tan needs to carry 50 chairs to the hall. He can carry 3 chairs on each trip. How many trips must he make?",
                       50, 3, "trip", "trips", "chairs", "chair"))
    its.append(up_item("Mrs Lim has 22 pencils. A pencil case holds 5 pencils. How many pencil cases does she need for all the pencils?",
                       22, 5, "pencil case", "pencil cases", "pencils", "pencil", svg=dots_svg(22, 5, "22 counters in groups of 5")))
    its.append(down_item("Mdm Wong bakes 30 kueh. She packs them in boxes of 8. How many boxes can she fill?",
                         30, 8, "box", "boxes", "The 6 kueh left over cannot fill another box."))
    its.append(down_item("Jun Jie has $40. A movie ticket costs $7. How many tickets can he buy?",
                         40, 7, "ticket", "tickets", "5 tickets cost $35. The $5 left over is not enough for another ticket."))
    its.append(down_item("A ribbon is 75 cm long. Hui Min cuts it into pieces of 9 cm. How many 9 cm pieces can she cut?",
                         75, 9, "piece", "pieces", "The 3 cm left over is too short for another piece."))
    its.append(down_item("Wei Ming has 27 stickers. He makes rows of 6 stickers. How many full rows can he make?",
                         27, 6, "row", "rows", "The 3 stickers left over cannot make another full row.",
                         svg=dots_svg(27, 6, "27 counters in groups of 6")))
    its.append(down_item("A fruit seller packs 92 rambutans into bags of 8. How many full bags does she get?",
                         92, 8, "bag", "bags", "The 4 rambutans left over cannot fill another bag."))
    its.append(left_item("Devi shares 35 sweets equally among 4 friends. How many sweets are left over?",
                         35, 4, "sweet", "sweets"))
    its.append(left_item("A teacher puts 58 books on shelves. Each shelf holds 9 books. How many books are left over after the shelves are full?",
                         58, 9, "book", "books"))
    its.append(left_item("Ahmad puts 23 eggs into boxes of 6. How many eggs are left over?",
                         23, 6, "egg", "eggs", svg=dots_svg(23, 6, "23 counters in groups of 6")))
    its.append(left_item("Nurul makes bracelets with 8 beads each. She has 70 beads. How many beads are left over?",
                         70, 8, "bead", "beads"))
    its.append(left_item("93 mandarin oranges are packed into bags of 7 for Chinese New Year. How many oranges are left over?",
                         93, 7, "orange", "oranges"))
    q, r = divmod(50, 8)
    its.append(mcqv("Ryan has $50. A storybook costs $8. He buys as many as he can. How much money does he have left?",
                    "$%d" % r, ["$%d" % q, "$%d" % (q * 8), "$%d" % (50 - 8)],
                    "50 ÷ 8 = %s. 6 books cost 6 × $8 = $48. $50 − $48 = $2. He has $2 left. ($6 is the number of books, not the money.)" % qr(q, r)))
    pool = ["30 pupils, 4 in each boat", "Full packs of 6 from 40 pens", "Buns left when 50 go on 6 trays", "8 cm pieces cut from 60 cm"]
    its.append(mcq("In which story should you round up to the next whole number?", pool[0], pool[1:],
                   "30 ÷ 4 = 7 R 2. With 7 boats, 2 pupils still need a place, so you need 8 boats. "
                   "Round up when everyone must fit."))
    name, he, his = P.next()
    its.append(mcq("%s says 47 ÷ 5 = 9. What mistake did %s make?" % (name, he),
                   "%s ignored the remainder" % cap(he),
                   ["The remainder is too big", "%s divided the wrong way" % cap(he), "There is no mistake"],
                   "9 × 5 = 45, and 47 − 45 = 2. The 2 left over is part of the answer: 47 ÷ 5 = 9 R 2."))
    assert divmod(56, 9) == (6, 2)
    its.append(mcq("56 pupils go on a trip. Each van holds 9 pupils. Siti says 6 vans are needed. Ali says 7 vans are needed. Who is correct?",
                   "Ali, because 2 pupils still need a place", ["Siti, because 56 ÷ 9 = 6 R 2", "Both are correct",
                                                                 "Neither: 8 vans are needed"],
                   "56 ÷ 9 = 6 R 2. 6 vans hold 54 pupils, and 2 pupils still need a place. So 7 vans are needed. Ali is correct."))
    assert divmod(29, 4) == (7, 1)
    its.append(mcq("29 pupils sit at tables of 4. 29 ÷ 4 = 7 R 1. What does the 1 mean?",
                   "1 pupil has no table yet", ["1 table is empty", "Each table has 1 more pupil", "There is 1 table"],
                   "7 tables of 4 seat 28 pupils. 29 − 28 = 1, so 1 pupil still needs a seat. "
                   "The remainder tells you what is left over."))
    return {"title": "What the remainder means", "items": its}


# ------------------------------------------------------------ set 5: word problems with bar models
def set_story(P):
    its = []
    # multiplication
    for t, each, k, one, svg in [
        ("A box has 128 crayons. How many crayons are there in 6 boxes?", 128, 6, "crayons", True),
        ("Each bus has 45 seats. How many seats are there in 8 buses?", 45, 8, "seats", True),
        ("A zoo ticket for a child costs $27. Mr Kumar buys 4 tickets for his children. How much does he pay?", 27, 4, "$", False),
        ("A packet of rice weighs 5 kg. How many kilograms do 136 packets weigh?", 136, 5, "kg", False),
    ]:
        tot = each * k
        fm = (lambda v: "$%s" % f(v)) if one == "$" else (lambda v: "%s %s" % (f(v), one))
        c = [fm(v) for v in cands_1d(each, k) if v > 0] + [fm(each + k)]
        e = "Multiply: %d × %d. %s. Answer: %s." % (each, k, cap(steps_1d(each, k)), fm(tot))
        if svg:
            e = "%d units of %d. %d × %d: %s. Answer: %s." % (k, each, each, k, steps_1d(each, k), fm(tot))
        its.append(mcqv((fig(groups_model(str(each), k)) if svg else "") + t, fm(tot), c, e))
    # division
    for t, n_, d, fm, svg in [
        ("Mrs Ng shares 252 stickers equally among 7 pupils. How many stickers does each pupil get?",
         252, 7, lambda v: "%s stickers" % f(v), share_model("252", 7)),
        ("A school canteen sold 96 plates of chicken rice in 4 days. It sold the same number each day. How many plates did it sell each day?",
         96, 4, lambda v: "%s plates" % f(v), share_model("96", 4)),
        ("Mr Rahman cuts a 345 cm rope into 5 equal pieces. How long is each piece?",
         345, 5, lambda v: "%s cm" % f(v), None),
        ("Raju packs 168 durian puffs equally into 8 boxes. How many durian puffs are in each box?",
         168, 8, lambda v: "%s durian puffs" % f(v), None),
    ]:
        assert n_ % d == 0
        if svg:
            e = "%d units = %d, so 1 unit = %d ÷ %d. " % (d, n_, n_, d)
        else:
            e = "Share equally, so divide: %d ÷ %d. " % (n_, d)
        e += pv_steps(n_, d, end=False) + " Answer: %s. %s" % (fm(n_ // d), check_txt(n_, d))
        cands = [fm(int(x)) for x in cands_div(n_, d)] + [fm(n_ * d)]
        its.append(mcqv((fig(svg) if svg else "") + t, fm(n_ // d), cands, e))
    assert 144 // 6 == 24 and 144 % 6 == 0 and 144 * 6 == 864
    its.append(mcqv("Mdm Wong bakes 144 cupcakes for Children’s Day. She puts 6 cupcakes in each box. How many boxes does she fill?",
                    "24 boxes", ["864 boxes", "138 boxes", "25 boxes"],
                    "Find how many 6s are in 144: 144 ÷ 6. " + pv_steps(144, 6, end=False) +
                    " Answer: 24 boxes. (144 × 6 = 864 multiplies instead of dividing.) Check: 24 × 6 = 144."))
    # times as many
    svg = model_svg([("Ali", [(1, "47", "u")]), ("Siti", [(1, "", "u")] * 3)], under=[(1, 0, 3, "?")],
                    label="bar model: Ali 1 unit of 47, Siti 3 units")
    its.append(mcqv(fig(svg) + "Ali has 47 marbles. Siti has 3 times as many marbles as Ali. How many marbles does Siti have?",
                    "141 marbles", ["50 marbles", "121 marbles", "188 marbles"],
                    "Siti has 3 units. 1 unit = 47. 3 units = 47 × 3 = 141 (7 × 3 = 21, write 1 and rename 2 tens; "
                    "4 tens × 3 + 2 = 14 tens). Siti has 141 marbles. (47 + 3 = 50 adds instead of multiplying.)"))
    assert 47 * 3 == 141 and mult_row(47, 3, "nocarry") == 121
    svg = model_svg([("Hafiz", [(1, "", "u")]), ("Zhi Hao", [(1, "", "u")] * 4)], under=[(0, 0, 1, "?")], right="245",
                    label="bar model: Hafiz 1 unit, Zhi Hao 4 units, 245 altogether")
    its.append(mcqv(fig(svg) + "Zhi Hao has 4 times as many cards as Hafiz. They have 245 cards altogether. How many cards does Hafiz have?",
                    "49 cards", ["61 cards", "196 cards", "980 cards"],
                    "Hafiz has 1 unit and Zhi Hao has 4 units, so 5 units = 245. 1 unit = 245 ÷ 5 = 49. Hafiz has 49 cards. "
                    "(245 ÷ 4 = 61 R 1 forgets Hafiz’s unit, and 980 multiplies instead of dividing.) Check: 49 × 5 = 245."))
    assert 245 // 5 == 49 and 49 * 4 == 196
    svg = model_svg([("Mon", [(1, "136", "u")]), ("Tue", [(1, "", "u")] * 2)], right="?",
                    label="bar model: Monday 1 unit of 136, Tuesday 2 units, total unknown")
    its.append(mcqv(fig(svg) + "A shop sold 136 cups of bubble tea on Monday. On Tuesday it sold twice as many cups. "
                    "How many cups did it sell on the two days altogether?", "408 cups", ["272 cups", "138 cups", "398 cups"],
                    "Monday is 1 unit and Tuesday is 2 units: 3 units altogether. 136 × 3 = 408 cups. "
                    "(272 is Tuesday only, and 398 forgets the renamed ten.) Check: 136 + 272 = 408."))
    assert 136 * 3 == 408 and mult_row(136, 3, "nocarry") == 398
    svg = model_svg([("Priya", [(1, "36", "u")]), ("Ethan", [(1, "", "u")] * 5)], under=[(1, 1, 5, "?")],
                    label="bar model: Priya 1 unit of 36, Ethan 5 units")
    its.append(mcqv(fig(svg) + "Priya has 36 stamps. Ethan has 5 times as many stamps as Priya. How many more stamps does Ethan have than Priya?",
                    "144 stamps", ["180 stamps", "41 stamps", "216 stamps"],
                    "Ethan has 4 more units than Priya. 1 unit = 36, so 4 units = 36 × 4 = 144. "
                    "(180 is all of Ethan’s stamps.) Check: 36 × 5 − 36 = 180 − 36 = 144."))
    # two-step
    its.append(mcqv("Mrs Lim buys 6 packets of 24 rambutans. She shares them equally among 8 neighbours. How many rambutans does each neighbour get?",
                    "18 rambutans", ["144 rambutans", "24 rambutans", "3 rambutans"],
                    "Step 1: 6 × 24 = 144 rambutans. Step 2: 144 ÷ 8 = 18 (14 tens ÷ 8 = 1 ten, 6 tens left; "
                    "rename as 60 ones: 64 ones; 64 ÷ 8 = 8). Each neighbour gets 18 rambutans."))
    assert 6 * 24 // 8 == 18 and 24 // 8 == 3
    its.append(mcqv("Chloe buys 4 bowls of laksa at $6 each. She pays with a $50 note. How much change does she get?",
                    "$26", ["$24", "$44", "$46"],
                    "Step 1: 4 × $6 = $24. Step 2: $50 − $24 = $26. Chloe gets $26 change. "
                    "($24 is the cost, not the change.)"))
    its.append(mcqv("A hawker sold 85 plates of prata in the morning and 83 plates in the afternoon. "
                    "Each plate has 2 pieces of prata. How many pieces of prata did he sell?",
                    "336 pieces", ["168 pieces", "84 pieces", "226 pieces"],
                    "Step 1: 85 + 83 = 168 plates. Step 2: 168 × 2 = 336 pieces "
                    "(8 × 2 = 16, rename 1 ten; 6 tens × 2 + 1 = 13 tens, rename 1 hundred; 1 hundred × 2 + 1 = 3 hundreds). "
                    "(226 forgets the renamed digits.)"))
    assert (85 + 83) * 2 == 336 and mult_row(168, 2, "nocarry") == 226
    its.append(mcqv("Mr Tan had 400 cm of wire. He cut off 4 pieces of 75 cm each. How much wire was left?",
                    "100 cm", ["300 cm", "325 cm", "120 cm"],
                    "Step 1: 4 × 75 = 300 cm. Step 2: 400 − 300 = 100 cm left. "
                    "(325 cm takes away only one piece. 120 cm comes from 4 × 75 = 280, which forgets the renamed 2 tens.)"))
    assert mult_row(75, 4, "nocarry") == 280
    # remainder stories
    its.append(up_item("Mrs Lim packs 38 goodie bags for Children’s Day. A carton holds 5 goodie bags. "
                       "How many cartons does she need to pack all the bags?", 38, 5, "carton", "cartons", "goodie bags", "goodie bag"))
    its.append(down_item("Sarah has 100 cm of ribbon. Each bow needs 8 cm. How many bows can she make?",
                         100, 8, "bow", "bows", "The 4 cm left over is not enough for another bow."))
    # number sentence
    its.append(mcq("312 pupils are put into 6 equal teams for Sports Day. Which number sentence finds the number of pupils in each team?",
                   "312 ÷ 6 = 52", ["6 ÷ 312 = 52", "312 × 6 = 1872", "312 − 6 = 306"],
                   "You know the total (312) and the number of teams (6), so divide: 312 ÷ 6 = 52. "
                   "6 ÷ 312 divides the wrong way. Check: 52 × 6 = 312."))
    assert 312 // 6 == 52 and 312 % 6 == 0 and 312 * 6 == 1872
    return {"title": "Word problems with bar models", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    worked = column_svg([("ex", {1: 4}), ("", "47"), ("×", "6"), ("", "282")], 2, "47 times 6 worked in columns")
    return (
        "<h2>Multiply with renaming</h2>"
        "<p>Start with the ones. If a product is 10 or more, write the ones digit and rename the tens. "
        "Add the renamed digit <b>after</b> you multiply the next place.</p>"
        "<figure class='sn-fig'>" + worked +
        "<figcaption>47 × 6: 7 ones × 6 = 42 ones. Write 2 and rename 4 tens (small green 4). "
        "4 tens × 6 = 24 tens, and 24 + 4 = 28 tens. Answer: 282.</figcaption></figure>" +
        ex("3-digit × 1-digit", "Find the value of 236 × 4.",
           "6 × 4 = 24: write 4, rename 2 tens. 3 × 4 + 2 = 14 tens: write 4, rename 1 hundred. 2 × 4 + 1 = 9 hundreds.", "944") +
        "<h2>Division with remainder</h2>"
        "<p>Division puts a total into equal groups. What is left over is the <b>remainder</b>. We write it with R. "
        "The remainder is always <b>smaller than the divisor</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(13, 4, "13 counters in groups of 4") +
        "<figcaption>13 ÷ 4 = 3 R 1: 3 groups of 4, and 1 left over (red). Check: 3 × 4 + 1 = 13.</figcaption></figure>"
        "<h2>Long division</h2>"
        "<p>Start with the biggest place on the left. Share it, write the answer on top, and rename what is left "
        "as the next place.</p>"
        "<figure class='sn-fig'>" + long_svg(75, 3, True, "75 divided by 3 worked out with long division") +
        "<figcaption>75 ÷ 3: 7 tens ÷ 3 = 2 tens, 1 ten left. Rename it as 10 ones: 15 ones. "
        "15 ÷ 3 = 5. Answer: 25.</figcaption></figure>"
        "<figure class='sn-fig'>" + long_svg(547, 4, True, "547 divided by 4 worked out with long division") +
        "<figcaption>547 ÷ 4 = 136 R 3. Check: 136 × 4 + 3 = 547.</figcaption></figure>"
        "<h2>What the remainder means</h2>"
        "<p>In a word problem, read the question and decide what to do with the remainder.</p>" +
        table(["The question asks", "Do this", "Example"], [
            ["Everyone or everything must fit", "Round up: add 1", "34 pupils, 4 per kayak: 9 kayaks"],
            ["How many full boxes or groups?", "Leave the remainder out", "30 kueh, boxes of 8: 3 boxes"],
            ["How many are left over?", "The remainder is the answer", "35 sweets, 4 friends: 3 left"],
        ]) +
        "<h2>Word problems with a bar model</h2>"
        "<figure class='sn-fig'>" + model_svg([("Ali", [(1, "47", "u")]), ("Siti", [(1, "", "u")] * 3)],
                                             under=[(1, 0, 3, "?")], label="bar model: Ali 1 unit of 47, Siti 3 units") +
        "<figcaption>Siti has 3 times as many marbles as Ali. 1 unit = 47, so 3 units = 47 × 3 = 141.</figcaption></figure>" +
        ex("Sharing", "Mrs Ng shares 252 stickers equally among 7 pupils. How many does each pupil get?",
           "7 units = 252. 1 unit = 252 ÷ 7 = 36.", "36 stickers") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not adding the renamed digit (47 × 6 = 242)", "Add the renamed 4 tens: 24 + 4 = 28 tens, so 282"],
            ["A remainder bigger than the divisor (30 ÷ 4 = 6 R 6)", "If the remainder is 4 or more, make one more group: 7 R 2"],
            ["Ignoring the remainder (47 ÷ 5 = 9)", "Write what is left: 47 ÷ 5 = 9 R 2"],
            ["Not renaming (72 ÷ 4 = 10)", "Rename the 3 tens left as 30 ones: 32 ÷ 4 = 8, so 18"],
            ["34 pupils need 8 kayaks", "2 pupils are still waiting, so 9 kayaks are needed"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division is taught in Primary 3 maths?",
     "a": "In the MOE syllabus, Primary 3 pupils multiply and divide numbers up to 3 digits by a 1-digit number, such as 236 × 4 and 547 ÷ 4. They also learn division with remainder and the multiplication tables of 6, 7, 8 and 9."},
    {"q": "How do I explain remainders to my child?",
     "a": "Use real objects: put 13 counters into groups of 4 and count what is left. There are 3 groups and 1 left over, so 13 ÷ 4 = 3 R 1, and the remainder is always smaller than 4."},
    {"q": "What is the most common mistake in P3 multiplication and division?",
     "a": "Forgetting to add the renamed digit when multiplying is the most common, followed by a remainder that is bigger than the divisor. Checking with quotient × divisor + remainder catches division mistakes."},
    {"q": "Why do P3 word problems use bar models?",
     "a": "A bar model shows equal units, so pupils can see when to multiply and when to divide, for example 3 units = 141, 1 unit = 47. The model method is used all the way to the PSLE in Primary 6."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def verify(sets):
    """Recompute every arithmetic answer that can be read from the question."""
    for s in sets:
        for it in s["items"]:
            ans = it["c"][it["a"]]
            m = re.search(r"aria-label='(\d+) divided by (\d+) written", it["q"]) or \
                re.search(r"Find the value of (\d+) ÷ (\d+)\.", it["q"]) or \
                re.search(r"counters in groups of \d+\. Find the value of (\d+) ÷ (\d+)\.", it["q"])
            if m:
                n, d = int(m.group(1)), int(m.group(2))
                assert ans == qr(*divmod(n, d)), (it["q"], it["c"], ans)
            m = re.search(r"aria-label='(\d+) times (\d+) written", it["q"]) or \
                re.search(r"Find the value of (\d+) × (\d+)\.", it["q"])
            if m:
                assert ans == f(int(m.group(1)) * int(m.group(2))), (it["q"], ans)
            # no choice repeats the value of the answer, and no remainder in the answer is >= the divisor
            for c in it["c"]:
                mm = re.search(r"(\d+) ÷ (\d+) = (\d+) R (\d+)$", c)
                if mm and c == ans:
                    assert int(mm.group(4)) < int(mm.group(2))


def gen():
    rnd = random.Random(63804)
    P = People(rnd)
    sets = [set_multiply(P), set_remainder_pictures(P), set_long_division(P), set_meaning(P), set_story(P)]
    verify(sets)
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            pos[it["a"]] += 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
        assert pos == [5, 5, 5, 5], pos
    return {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "multiplication-and-division", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Multiplication and Division",
        "seo_title": "P3 Multiplication and Division Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplication and Division",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Division with remainder; multiplication and division algorithms (up to 3 digits by 1 digit)",
        "meta_desc": "Free P3 practice: multiply and divide up to 3 digits by 1 digit, renaming, remainders and bar model word problems. 100 questions with answers.",
        "key_big": "Work one place at a time and rename what is left; a remainder is always smaller than the divisor.",
        "key_sub": "47 × 6 = 282 (7 × 6 = 42, rename 4 tens) and 13 ÷ 4 = 3 R 1 (3 × 4 + 1 = 13).",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "bar model|[0-9]+ counters|[0-9]+ groups of|place-value discs")
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
