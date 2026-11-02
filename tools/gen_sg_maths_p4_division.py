# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Division (MOE 2021 Primary Mathematics Syllabus, Four Operations)
"Division algorithm up to 4 digits by 1 digit."
  python3 tools/gen_sg_maths_p4_division.py
Division facts, 3-digit and 4-digit numbers divided by 1-digit numbers (long division, renaming,
zeros in the quotient), remainders and what they mean, and Singapore word problems with bar models.
Wrong answers come from real mistakes: a missing 0 in the quotient (6024 ÷ 6 = 104), not renaming,
a remainder bigger than the divisor, ignoring the remainder, not rounding up for buses.
Helpers adapted from gen_cabc_math_g5_division.py and gen_sg_maths_p5_order_of_operations.py.
Singapore English. 4-digit numbers have no separator; 5+ digits use a no-break space.
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
"""
import json, os, random, re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
GREY = "#6b6259"
INK = "#2b2b2b"
BLUE = "#2f6fb0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Nurul", "Mei Ling", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ahmad", "Hafiz", "Wei Ming", "Zhi Hao", "Raju", "Arjun", "Ethan", "Ryan"]
NBSP = " "
PLACES = ["ten thousands", "thousands", "hundreds", "tens", "ones"]
ONE = {"ten thousands": "ten thousand", "thousands": "thousand", "hundreds": "hundred", "tens": "ten", "ones": "one"}


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


def mcq(q, correct, cands, e, values=None):
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
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
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


def svg_wrap(w, h, body, label):
    w, h = int(round(w + 0.49)), int(round(h + 0.49))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def T(x, y, s, size=16, fill=INK, anchor="middle", weight="700", mono=False):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, size, weight, fill, anchor, " font-family='monospace'" if mono else "", s))


def tw(s, size=15):
    return len(s) * size * 0.58


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


# ------------------------------------------------------------ long division in words (place value)
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


# ------------------------------------------------------------ typical mistakes
def digitwise(n, d):
    """Each digit divided on its own, nothing renamed (468 ÷ 4 -> 112)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def zero_slips(q):
    """A 0 inside the quotient left out (1004 -> 104, 14)."""
    s = str(q)
    out = []
    for i in range(1, len(s)):
        if s[i] == "0":
            t = s[:i] + s[i + 1:]
            out.append(int(t))
    if s.count("0") > 1:
        out.append(int(s.replace("0", "")))
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
    return c + [qr(q - 1, r + d),          # remainder bigger than the divisor
                f(q),                      # remainder ignored
                qr(q, d - r) if d - r != r else None,   # wrote how many more are needed
                qr(q + 1, r), qr(q - 1, r), qr(q * 10, r)]


# ------------------------------------------------------------ figures
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
            last = k == len(rows) - 1
            if last:
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


def array_svg(rows, cols, label=None):
    R, gap = 7, 20
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (6 + R + j * gap, 6 + R + i * gap, R, GREEN))
    return svg_wrap(12 + 2 * R + (cols - 1) * gap, 12 + 2 * R + (rows - 1) * gap, "".join(s),
                    label or "array of %d rows of %d dots" % (rows, cols))


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


SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, under=(), right=None, BW=340, label="bar model"):
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


# ------------------------------------------------------------ set 1: division facts
def set_facts():
    its = []
    for n, d in [(63, 9), (48, 6), (56, 8), (42, 7), (72, 8), (54, 9), (36, 4), (81, 9)]:
        q = n // d
        its.append(mcq("Find the value of %d ÷ %d." % (n, d), str(q), [str(q + 1), str(q - 1), str(q + 2), str(n - d)],
                       "Think of the multiplication table of %d: %d × ? = %d. %d × %d = %d, so %d ÷ %d = %d." % (d, d, n, d, q, n, n, d, q)))
    for d, q in [(6, 8), (7, 9)]:
        n = d * q
        its.append(mcq("Find the missing number: ? ÷ %d = %d" % (d, q), str(n),
                       [str(d + q), str(n - d), str(n + d), str(q - d) if q > d else None],
                       "The missing number is the total. Multiply: %d × %d = %d. Check: %d ÷ %d = %d. "
                       "Adding %d + %d = %d is a common mistake." % (q, d, n, n, d, q, d, q, d + q)))
    for n, q in [(72, 9), (48, 8)]:
        d = n // q
        its.append(mcq("Find the missing number: %d ÷ ? = %d" % (n, q), str(d),
                       [str(d + 1), str(d - 1), str(n - q), str(q)],
                       "Ask: what number times %d makes %d? %d × %d = %d, so %d ÷ %d = %d." % (q, n, d, q, n, n, d, q)))
    for n, d in [(64, 8), (49, 7)]:
        q = n // d
        its.append(mcq("Which multiplication fact helps you find %d ÷ %d?" % (n, d), "%d × %d = %d" % (q, d, n),
                       ["%d × %d = %d" % (q - 1, d, (q - 1) * d), "%d × %d = %d" % (q + 1, d, (q + 1) * d),
                        "%d + %d = %d" % (n, d, n + d)],
                       "Division is the inverse of multiplication. %d × %d = %d, so %d ÷ %d = %d." % (q, d, n, n, d, q)))
    its.append(mcq("Which is NOT in the same family of facts as 6 × 7 = 42?", "6 ÷ 42 = 7",
                   ["42 ÷ 6 = 7", "7 × 6 = 42", "42 ÷ 7 = 6"],
                   "In a division fact the total, 42, comes first: 42 ÷ 6 = 7 and 42 ÷ 7 = 6. "
                   "6 ÷ 42 divides the wrong way, so it does not belong."))
    for n, d in [(420, 7), (360, 4)]:
        q = n // d
        its.append(mcq("Find the value of %d ÷ %d." % (n, d), str(q), [str(q // 10), str(q * 10), str(q + 10), str(q - 10)],
                       "%d is %d tens. %d tens ÷ %d = %d tens = %d. Check: %d × %d = %d."
                       % (n, n // 10, n // 10, d, q // 10, q, q, d, n)))
    for n, d in [(4800, 6), (2700, 9)]:
        q = n // d
        its.append(mcq("Find the value of %d ÷ %d." % (n, d), str(q), [str(q // 10), str(q * 10), str(q // 100), str(q + 100)],
                       "%d is %d hundreds. %d hundreds ÷ %d = %d hundreds = %d. Check: %d × %d = %d."
                       % (n, n // 100, n // 100, d, q // 100, q, q, d, n)))
    its.append(mcq(fig(array_svg(6, 9, "array of 6 rows of 9 chairs")) +
                   "54 chairs are set out in the school hall in 6 equal rows. How many chairs are in each row?",
                   "9", ["6", "8", "48"],
                   "The array has 6 equal rows. 54 ÷ 6 = 9, so each row has 9 chairs. Check: 6 × 9 = 54."))
    return {"title": "Division facts", "items": its}


# ------------------------------------------------------------ set 2: 3-digit by 1-digit
def set_three_digit(P):
    its = []
    for n, d in [(468, 4), (735, 5), (852, 6), (296, 8), (581, 7), (912, 3)]:
        assert n % d == 0
        its.append(mcq(fig(long_svg(n, d)) + "Divide.", f(n // d), cands_div(n, d), pv_steps(n, d)))
    for n, d in [(624, 6), (945, 9), (384, 8), (672, 4)]:
        assert n % d == 0
        its.append(mcq("Find the value of %d ÷ %d." % (n, d), f(n // d), cands_div(n, d), pv_steps(n, d)))
    for n, d in [(369, 3), (484, 4), (156, 3)]:
        q = n // d
        assert n % d == 0
        its.append(mcq(fig(discs_svg(n)) + "The place-value discs show %d. Share them equally into %d groups. "
                       "What number is in each group?" % (n, d), f(q),
                       [f(q + 10), f(q + 100) if q > 100 else f(q + 1), f(n - q), f(q - 1)],
                       pv_steps(n, d)))
    for n, d, near in [(487, 6, 480), (358, 9, 360)]:
        est = near // d
        e = ("Find a number close to %d that is easy to divide by %d: %d. %d ÷ %d = %d (think %d ÷ %d = %d). "
             "So %d ÷ %d is about %d." % (n, d, near, near, d, est, near // 10, d, est // 10, n, d, est))
        its.append(mcqv("Which is the best estimate for %d ÷ %d?" % (n, d), "about %d" % est,
                        ["about %d" % (est // 10), "about %d" % (est * 10), "about %d" % (est + 10)], e))
    for n, d in [(816, 4), (648, 3)]:
        q = n // d
        its.append(mcq("Which multiplication checks that %d ÷ %d = %d?" % (n, d, q), "%d × %d = %d" % (q, d, n),
                       ["%d × %d = %d" % (n, d, n * d), "%d × %d = %d" % (d, d, d * d), "%d + %d = %d" % (q, d, q + d)],
                       "Multiply the answer by the number you divided by: %d × %d = %d. That is the number you started with, "
                       "so the answer is correct." % (q, d, n)))
    nm, he, his = P.next()
    its.append(mcq("%s says 618 ÷ 6 = 13. What mistake did %s make?" % (nm, he), "%s left out the 0 in the tens place" % cap(he),
                   ["%s divided the wrong way" % cap(he), "%s ignored a remainder" % cap(he), "There is no mistake"],
                   "6 hundreds ÷ 6 = 1 hundred. 1 ten ÷ 6 = 0: write 0 in the tens place. Rename 1 ten as 10 ones: 18 ones. "
                   "18 ones ÷ 6 = 3 ones. The answer is 103, not 13. Check: 103 × 6 = 618."))
    its.append(mcq("How many digits does the answer to 256 ÷ 8 have?", "2 digits", ["3 digits", "1 digit", "4 digits"],
                   "2 hundreds ÷ 8: not enough to share, so there are no hundreds in the answer. Rename as 20 tens: 25 tens. "
                   "25 tens ÷ 8 = 3 tens, 1 ten left. Rename as 10 ones: 16 ones. 16 ÷ 8 = 2. 256 ÷ 8 = 32, which has 2 digits."))
    opts = [(312, 4), (314, 4), (310, 4), (315, 4)]
    e = "Divide each one: " + "; ".join("%d ÷ 4 = %s" % (n, qr(*divmod(n, 4))) for n, _ in opts) + \
        ". Only 312 ÷ 4 = 78 has no remainder. Check: 78 × 4 = 312."
    its.append(mcq("Which division has no remainder?", "312 ÷ 4", ["314 ÷ 4", "310 ÷ 4", "315 ÷ 4"], e))
    return {"title": "Divide 3-digit numbers by 1-digit numbers", "items": its}


# ------------------------------------------------------------ set 3: 4-digit by 1-digit, zeros in the quotient
def set_four_digit(P):
    its = []
    for n, d in [(6048, 6), (4832, 4), (3618, 6), (8056, 8), (5430, 5), (2135, 7)]:
        assert n % d == 0 and "0" in str(n // d)
        its.append(mcq(fig(long_svg(n, d)) + "Divide.", f(n // d), cands_div(n, d), pv_steps(n, d)))
    for n, d in [(7035, 7), (2412, 4), (9027, 9), (4520, 4), (1648, 8)]:
        assert n % d == 0 and "0" in str(n // d)
        its.append(mcq("Find the value of %d ÷ %d." % (n, d), f(n // d), cands_div(n, d), pv_steps(n, d)))
    for n, d in [(6029, 6), (3205, 8), (5017, 5)]:
        q, r = divmod(n, d)
        assert r and "0" in str(q)
        its.append(mcqv("Find the value of %d ÷ %d." % (n, d), qr(q, r), cands_rem(n, d), pv_steps(n, d)))
    nm, he, his = P.next()
    its.append(mcq("%s worked out 6024 ÷ 6 and got 104. What is the correct answer?" % nm, "1004",
                   ["1040", "14", "1400"],
                   "6 thousands ÷ 6 = 1 thousand. 0 hundreds ÷ 6 = 0: write 0 in the hundreds place. "
                   "2 tens ÷ 6 = 0: write 0 in the tens place, then rename 2 tens as 20 ones: 24 ones. 24 ones ÷ 6 = 4 ones. "
                   "The answer is 1004. %s left out one 0. Check: 1004 × 6 = 6024." % nm))
    nm, he, his = P.next()
    its.append(mcq("%s says 4816 ÷ 8 = 62. What mistake did %s make?" % (nm, he), "%s left out the 0 in the tens place" % cap(he),
                   ["%s left out the 0 in the ones place" % cap(he), "%s ignored a remainder" % cap(he), "There is no mistake"],
                   "48 hundreds ÷ 8 = 6 hundreds. 1 ten ÷ 8 = 0: write 0 in the tens place. Rename 1 ten as 10 ones: 16 ones. "
                   "16 ones ÷ 8 = 2 ones. The answer is 602, not 62. Check: 602 × 8 = 4816."))
    its.append(mcq("How many digits does the answer to 2416 ÷ 4 have?", "3 digits", ["4 digits", "2 digits", "1 digit"],
                   "2 thousands ÷ 4: not enough to share, so there are no thousands in the answer. "
                   "Rename as 20 hundreds: 24 hundreds. 24 hundreds ÷ 4 = 6 hundreds. 1 ten ÷ 4 = 0: write 0. "
                   "16 ones ÷ 4 = 4. 2416 ÷ 4 = 604, which has 3 digits."))
    opts = [4836, 4884, 4848, 4864]
    e = "Divide each one: " + "; ".join("%d ÷ 4 = %d" % (n, n // 4) for n in opts) + \
        ". Only 4836 ÷ 4 = 1209 has a 0 in the tens place: 3 tens ÷ 4 = 0, so write 0 and rename 3 tens as 30 ones."
    assert all(n % 4 == 0 for n in opts) and str(4836 // 4)[2] == "0"
    its.append(mcq("Which division has a 0 in the tens place of the answer?", "4836 ÷ 4", ["4884 ÷ 4", "4848 ÷ 4", "4864 ÷ 4"], e))
    assert 3045 // 5 == 609 and 3045 % 5 == 0
    its.append(mcq("Which multiplication checks that 3045 ÷ 5 = 609?", "609 × 5 = 3045",
                   ["69 × 5 = 345", "3045 × 5 = 15" + NBSP + "225", "609 + 5 = 614"],
                   "Multiply the answer by the divisor: 609 × 5 = 3045. That is the number you started with, so 609 is correct."))
    assert 7056 // 7 == 1008 and 7056 % 7 == 0
    its.append(mcq("Find the missing digit: 7056 ÷ 7 = 1?08", "0", ["1", "7", "8"],
                   "7 thousands ÷ 7 = 1 thousand. 0 hundreds ÷ 7 = 0: write 0 in the hundreds place. "
                   "5 tens ÷ 7 = 0: write 0 in the tens place, and rename 5 tens as 50 ones: 56 ones. 56 ÷ 7 = 8. "
                   "7056 ÷ 7 = 1008, so the missing digit is 0."))
    return {"title": "Divide 4-digit numbers: zeros in the quotient", "items": its}


# ------------------------------------------------------------ set 4: remainders and what they mean
def pick_rem(rnd, used, lo, hi, dlo=3, dhi=9):
    while True:
        d = rnd.randint(dlo, dhi)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r == 0 or n in used or q < 10 or "0" in str(q) or r == q % 10 or q % 10 == d - r:
            continue
        used.add(n)
        return n, d


def up_item(t, n, d, one, many, who, who1, svg=None):
    q, r = divmod(n, d)
    ans = units(q + 1, one, many)
    e = ("%d ÷ %d = %s. %s are not enough: %s still %s a place. Round up to %s."
         % (n, d, qr(q, r), cap(units(q, one, many)), units(r, who1, who), "needs" if r == 1 else "need", ans))
    return mcqv((fig(svg) if svg else "") + t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e)


def down_item(t, n, d, one, many, why):
    q, r = divmod(n, d)
    ans = units(q, one, many)
    e = "%d ÷ %d = %s. %s Leave the remainder out: the answer is %s." % (n, d, qr(q, r), why, ans)
    return mcqv(t, ans, [units(q + 1, one, many), qr(q, r), units(r, one, many), units(q - 1, one, many)], e)


def left_item(t, n, d, one, many):
    q, r = divmod(n, d)
    ans = units(r, one, many)
    e = ("%d ÷ %d = %s (%d × %d = %d, %d − %d = %d). The question asks how many are left over, so the answer is the remainder: %s."
         % (n, d, qr(q, r), q, d, q * d, n, q * d, r, ans))
    return mcqv(t, ans, [units(q, one, many), units(d - r, one, many) if d - r != r else None, qr(q, r),
                         units(d, one, many), units(r + d, one, many)], e)


def set_remainders(rnd, used, P):
    its = []
    for n, d in [(26, 4), (31, 6), (29, 5)]:
        used.add(n)
        q, r = divmod(n, d)
        e = ("There are %d full groups of %d and %s left over (in red). %d is less than %d, so it cannot make another group. "
             "%d ÷ %d = %s. %s" % (q, d, units(r, "counter", "counters"), r, d, n, d, qr(q, r), check_txt(n, d)))
        its.append(mcqv(fig(dots_svg(n, d)) + "The picture shows %d counters in groups of %d. Find the value of %d ÷ %d." % (n, d, n, d),
                        qr(q, r), cands_rem(n, d), e))
    for i in range(4):
        n, d = pick_rem(rnd, used, 41, 98) if i < 2 else pick_rem(rnd, used, 112, 989)
        q, r = divmod(n, d)
        qq = (fig(long_svg(n, d)) + "Divide.") if i % 2 == 1 else "Find the value of %d ÷ %d." % (n, d)
        cands = cands_rem(n, d)
        dw = digitwise(n, d)
        if dw != q and int(str(n)[0]) >= d:
            cands.insert(1, qr(dw, r))
        its.append(mcqv(qq, qr(q, r), cands, pv_steps(n, d)))
    n, d = 2347, 5
    its.append(mcqv(fig(long_svg(n, d)) + "Divide.", qr(*divmod(n, d)), cands_rem(n, d), pv_steps(n, d)))
    n, d = pick_rem(rnd, used, 120, 980, 4)
    q, r = divmod(n, d)
    its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                   [f(q), str(d - r) if d - r != r else None, str(r + d), str(d)],
                   "The question asks for the remainder, not the quotient. " + pv_steps(n, d)))
    n, d = pick_rem(rnd, used, 120, 980)
    q, r = divmod(n, d)
    its.append(mcq("%d ÷ %d = %s. Which expression checks this answer? It should equal %d." % (n, d, qr(q, r), n),
                   "%d × %d + %d" % (q, d, r),
                   ["%d × %d − %d" % (q, d, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (q, d, r)],
                   "Multiply the quotient by the divisor, then add the remainder: %d × %d = %d, %d + %d = %d. "
                   "It matches, so the answer is correct." % (q, d, q * d, q * d, r, n)))
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick_rem(rnd, used, 50, 99, 4, 8)
        q, r = divmod(n, d)
        its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                       "The remainder is too big",
                       ["%s ignored the remainder" % cap(he), "%s divided the wrong way" % cap(he), "There is no mistake"],
                       "The remainder must be smaller than the divisor. %d is not smaller than %d, so one more group of %d fits: "
                       "%d − %d = %d. The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    name, he, his = P.next()
    its.append(mcq("%s says 47 ÷ 5 = 9. What mistake did %s make?" % (name, he),
                   "%s ignored the remainder" % cap(he),
                   ["The remainder is too big", "%s divided the wrong way" % cap(he), "There is no mistake"],
                   "9 × 5 = 45, and 47 − 45 = 2. The 2 left over is part of the answer: 47 ÷ 5 = 9 R 2."))
    its.append(mcq("You divide a number by 6. Which of these could be the remainder?", "5", ["6", "7", "9"],
                   "A remainder is always smaller than the divisor. When you divide by 6, the remainder can only be 0, 1, 2, 3, 4 or 5. "
                   "So 5 is the only possible one."))
    q, d, r = 47, 5, 3
    n = q * d + r
    its.append(mcq("In a division, the quotient is 47, the divisor is 5 and the remainder is 3. What number was divided?",
                   str(n), [str(q * d), str(q * d - r), str(q + d + r), str(q * d + d)],
                   "Work backwards: multiply, then add the remainder. 47 × 5 = 235, and 235 + 3 = 238. "
                   "Check: 238 ÷ 5 = 47 R 3."))
    its.append(up_item("A class of 38 pupils goes kayaking at East Coast Park. Each kayak holds 3 pupils. How many kayaks are needed?",
                       38, 3, "kayak", "kayaks", "pupils", "pupil"))
    its.append(up_item("Farah has 75 photos for an album. Each page holds 6 photos. How many pages does she need for all of them?",
                       75, 6, "page", "pages", "photos", "photo"))
    its.append(down_item("Mrs Ng has 50 kueh. She packs them in boxes of 8. How many boxes can she fill?",
                         50, 8, "box", "boxes", "The 2 kueh left over cannot fill another box."))
    its.append(down_item("Jun Jie has $45. A movie ticket costs $7. How many tickets can he buy?",
                         45, 7, "ticket", "tickets", "6 tickets cost $42. The $3 left over is not enough for another ticket."))
    pool = ["30 pupils, 4 in each boat", "Full packs of 6 from 40 pens", "Buns left when 50 go on 6 trays", "8 cm pieces cut from 100 cm"]
    its.append(mcq("In which story should you round up to the next whole number?", pool[0], pool[1:],
                   "30 ÷ 4 = 7 R 2. With 7 boats, 2 pupils still need a place, so you need 8 boats. "
                   "Round up when everyone must fit."))
    return {"title": "Remainders and what they mean", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)
    for t, n_, d, fm, svg in [
        ("Mrs Lim shares 852 stickers equally among 6 groups. How many stickers does each group get?",
         852, 6, lambda v: "%s stickers" % f(v), share_model("852", 6)),
        ("A school raised $2136 at a charity fair. It shares the money equally among 3 charities. How much does each charity get?",
         2136, 3, D, share_model("$2136", 3)),
        ("A bakery made 1056 curry puffs. It put them equally on 8 trays. How many curry puffs are on each tray?",
         1056, 8, lambda v: "%s curry puffs" % f(v), share_model("1056", 8)),
        ("Mr Tan cuts a 945 cm rope into 5 equal pieces. How long is each piece?",
         945, 5, lambda v: "%s cm" % f(v), None),
        ("Hui Min reads a 416-page book in 8 days. She reads the same number of pages each day. How many pages does she read each day?",
         416, 8, lambda v: "%s pages" % f(v), None),
    ]:
        assert n_ % d == 0
        e = "Share equally, so divide: %d ÷ %d. " % (n_, d)
        if svg:
            e = "%d units = %s, so 1 unit = %d ÷ %d. " % (d, fm(n_), n_, d)
        e += pv_steps(n_, d, end=False) + " %s %s. %s" % ("1 unit =" if svg else "So the answer is", fm(n_ // d), check_txt(n_, d))
        cands = [fm(int(x)) for x in cands_div(n_, d)]
        its.append(mcqv((fig(svg) if svg else "") + t, fm(n_ // d), cands, e))
    assert 2408 // 8 == 301 and 2408 % 8 == 0
    its.append(mcqv("A factory packs 2408 cans of drinks into cartons of 8. How many cartons does it fill?",
                    "301 cartons", ["31 cartons", "310 cartons", "300 cartons"],
                    "Find how many 8s are in 2408: 2408 ÷ 8. " + pv_steps(2408, 8, end=False) +
                    " Answer: 301 cartons. Check: 301 × 8 = 2408."))
    its.append(down_item("A fruit seller packs 3460 mandarin oranges for Chinese New Year into bags of 8. How many full bags does he get?",
                         3460, 8, "bag", "bags", "The 4 oranges left over cannot fill another bag."))
    nm, he, his = P.next()
    its.append(down_item("%s has 230 stamps. Each page of %s album holds 9 stamps. How many pages can %s fill?" % (nm, his, he),
                         230, 9, "page", "pages", "The 5 stamps left over cannot fill another page."))
    its.append(down_item("A farm packs 1250 eggs into boxes of 6. How many boxes can it fill?",
                         1250, 6, "box", "boxes", "The 2 eggs left over cannot fill another box."))
    its.append(up_item("93 pupils and teachers go to Gardens by the Bay in vans. Each van holds 8 people. How many vans are needed?",
                       93, 8, "van", "vans", "people", "person"))
    its.append(up_item("A canteen stall has 245 bottles of water to pack into crates of 6. How many crates are needed to pack all the bottles?",
                       245, 6, "crate", "crates", "bottles", "bottle"))
    its.append(up_item("Mdm Wong needs 150 cupcakes for Children's Day. The cupcakes are sold in boxes of 4. How many boxes must she buy?",
                       150, 4, "box", "boxes", "cupcakes", "cupcake"))
    its.append(up_item("1340 people queue for a boat ride. Each boat trip carries 9 people. How many boat trips are needed to take everyone?",
                       1340, 9, "trip", "trips", "people", "person"))
    its.append(left_item("A library has 1234 books to put on shelves. Each shelf holds 9 books. "
                         "How many books are on the last shelf, which is not full?", 1234, 9, "book", "books"))
    svg = model_svg([("Ali", [(1, "", "u")]), ("Siti", [(1, "", "u")] * 3)], under=[(0, 0, 1, "?")], right="1248",
                    BW=300, label="bar model: Ali 1 unit, Siti 3 units, 1248 altogether")
    its.append(mcqv(fig(svg) + "Siti has 3 times as many stickers as Ali. They have 1248 stickers altogether. How many stickers does Ali have?",
                    "312 stickers", ["416 stickers", "936 stickers", "4992 stickers"],
                    "Ali has 1 unit and Siti has 3 units, so 4 units = 1248. 1 unit = 1248 ÷ 4 = 312. Ali has 312 stickers. "
                    "(1248 ÷ 3 = 416 forgets Ali’s unit.) Check: 312 × 4 = 1248."))
    svg = model_svg([("Fri", [(1, "", "u")]), ("Sat", [(1, "", "u")] * 2)], under=[(1, 0, 2, "?")], right="1365",
                    BW=300, label="bar model: Friday 1 unit, Saturday 2 units, 1365 altogether")
    its.append(mcqv(fig(svg) + "A shop sold twice as many cups of bubble tea on Saturday as on Friday. It sold 1365 cups on the two days. "
                    "How many cups did it sell on Saturday?", "910 cups", ["455 cups", "2730 cups", "1820 cups"],
                    "3 units = 1365, so 1 unit = 1365 ÷ 3 = 455 (Friday). Saturday has 2 units: 455 × 2 = 910 cups. "
                    "(455 is only 1 unit.) Check: 455 + 910 = 1365."))
    its.append(mcqv("Mr Rahman buys 4 boxes of 36 mandarin oranges. He shares them equally among 6 relatives. How many oranges does each relative get?",
                    "24 oranges", ["144 oranges", "6 oranges", "36 oranges"],
                    "Step 1: 4 × 36 = 144 oranges. Step 2: 144 ÷ 6 = 24 (14 tens ÷ 6 = 2 tens, 2 tens left; rename as 20 ones: 24 ones; "
                    "24 ÷ 6 = 4). Each relative gets 24 oranges."))
    its.append(mcqv("Mr Kumar had $1000. He spent $136 on a bicycle and shared the rest equally among 4 charities. How much did each charity get?",
                    "$216", ["$250", "$864", "$284"],
                    "Step 1: $1000 − $136 = $864. Step 2: $864 ÷ 4 = $216. Each charity got $216. "
                    "($1000 ÷ 4 = $250 forgets to take away the $136 first.) Check: 216 × 4 = 864."))
    its.append(mcqv("Two P4 classes have 38 and 37 pupils. They go to the Science Centre in vans that hold 8 pupils each. How many vans are needed?",
                    "10 vans", ["9 vans", "9 R 3", "5 vans"],
                    "Step 1: 38 + 37 = 75 pupils. Step 2: 75 ÷ 8 = 9 R 3. 9 vans hold 72 pupils, and 3 pupils still need a place, "
                    "so round up to 10 vans."))
    its.append(mcq("315 pupils are put into 9 equal teams for Sports Day. Which number sentence finds the number of pupils in each team?",
                   "315 ÷ 9 = 35", ["9 ÷ 315 = 35", "315 × 9 = 2835", "315 − 9 = 306"],
                   "You know the total (315) and the number of teams (9), so divide: 315 ÷ 9 = 35. "
                   "9 ÷ 315 divides the wrong way. Check: 35 × 9 = 315."))
    return {"title": "Word problems: sharing, packing and buses", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Division facts</h2>"
        "<p>Division shares a total into equal groups. Every division fact comes from a multiplication fact. "
        "To find 54 ÷ 6, ask: 6 times what makes 54? 6 × 9 = 54, so 54 ÷ 6 = 9.</p>"
        "<p>Facts also help with tens and hundreds: 420 ÷ 7 is 42 tens ÷ 7 = 6 tens = 60. 4800 ÷ 6 is 48 hundreds ÷ 6 = 800.</p>"
        "<h2>Divide place by place</h2>"
        "<p>Start with the biggest place on the left. Share it, write the answer on top, and rename what is left "
        "as the next place.</p>"
        "<figure class='sn-fig'>" + discs_svg(156, "place-value discs showing 156") +
        "<figcaption>156 ÷ 3: 1 hundred cannot be shared by 3, so rename it as 10 tens: 15 tens. "
        "15 tens ÷ 3 = 5 tens. 6 ones ÷ 3 = 2 ones. Answer: 52.</figcaption></figure>"
        "<figure class='sn-fig'>" + long_svg(157, 4, True, "157 divided by 4 worked out with long division") +
        "<figcaption>Long division of 157 ÷ 4: 15 tens ÷ 4 = 3 tens, 3 tens left. Rename as 30 ones: 37 ones. "
        "37 ÷ 4 = 9 R 1. Answer: 39 R 1. Check: 39 × 4 + 1 = 157.</figcaption></figure>"
        "<h2>Zeros in the quotient</h2>"
        "<p>When a place is too small to share, write <b>0</b> in that place of the answer. Do not skip it.</p>"
        "<figure class='sn-fig'>" + long_svg(6024, 6, True, "6024 divided by 6 worked out with long division") +
        "<figcaption>6024 ÷ 6: 6 thousands ÷ 6 = 1 thousand. 0 hundreds ÷ 6 = 0. 2 tens ÷ 6 = 0, so rename them: 24 ones. "
        "24 ÷ 6 = 4. Answer: 1004, not 104.</figcaption></figure>" +
        ex("Check by multiplying", "Is 6024 ÷ 6 = 1004?", "Multiply the answer by the divisor: 1004 × 6 = 6024.", "Yes") +
        "<h2>Remainders</h2>"
        "<p>The <b>remainder</b> is what is left when no more equal groups can be made. We write it with R. "
        "The remainder is always <b>smaller than the divisor</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(23, 5, "23 counters in groups of 5") +
        "<figcaption>23 ÷ 5 = 4 R 3: 4 full groups of 5, and 3 left over (red). Check: 4 × 5 + 3 = 23.</figcaption></figure>"
        "<h2>What the remainder means</h2>"
        "<p>In a word problem, read the question and decide what to do with the remainder.</p>" +
        table(["The question asks", "Do this", "Example"], [
            ["Everyone or everything must fit", "Round up: add 1", "93 people, 8 per van: 12 vans"],
            ["How many full boxes or groups?", "Leave the remainder out", "50 kueh, boxes of 8: 6 boxes"],
            ["How many are left over?", "The remainder is the answer", "67 beads, 8 per bracelet: 3 left"],
        ]) +
        "<h2>Word problems with a bar model</h2>"
        "<figure class='sn-fig'>" + share_model("852", 6, "bar model: 852 shared into 6 equal units") +
        "<figcaption>852 stickers shared equally among 6 groups. 6 units = 852, so 1 unit = 852 ÷ 6 = 142.</figcaption></figure>" +
        ex("Field trip", "93 pupils and teachers go to Gardens by the Bay. Each van holds 8 people. How many vans are needed?",
           "93 ÷ 8 = 11 R 5. 11 vans hold 88 people, and 5 people still need a place. Add 1 more van.", "12 vans") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Missing a 0 in the quotient (6024 ÷ 6 = 104)", "When a place is too small, write 0: 1004"],
            ["A remainder bigger than the divisor (29 ÷ 4 = 6 R 5)", "If the remainder is 4 or more, make one more group: 7 R 1"],
            ["Ignoring the remainder (47 ÷ 5 = 9)", "Write what is left: 47 ÷ 5 = 9 R 2"],
            ["Not renaming (468 ÷ 4 = 112)", "Rename what is left as the next place: 117"],
            ["93 people need 11 vans", "5 people are still waiting, so 12 vans are needed"],
        ])
    )


FAQ = [
    {"q": "What division is taught in Primary 4 maths?",
     "a": "In the MOE syllabus, Primary 4 pupils use the division algorithm to divide numbers up to 4 digits by a 1-digit number, such as 6024 ÷ 6, with and without remainders. They also solve word problems, often with bar models."},
    {"q": "How do I explain zeros in the quotient to my child?",
     "a": "Divide one place at a time and write 0 whenever a place is too small to share. In 6024 ÷ 6 the hundreds and tens are too small, so the answer is 1004, not 104."},
    {"q": "What is the most common mistake in division?",
     "a": "Leaving out a 0 in the quotient is the most common mistake, followed by a remainder that is bigger than the divisor. Checking with multiplication (quotient × divisor + remainder) catches both."},
    {"q": "When do you round up in a division word problem?",
     "a": "Round up when everyone or everything must fit, such as pupils in vans or bottles in crates. 93 people in vans of 8 is 11 R 5, so 12 vans are needed. Long division also prepares pupils for the PSLE in Primary 6."},
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
    """Recompute every 'Find the value of n ÷ d' / 'Divide.' answer from the question."""
    for s in sets:
        for it in s["items"]:
            m = re.search(r"aria-label='(\d+) divided by (\d+) written", it["q"]) or \
                re.search(r"Find the value of (\d+) ÷ (\d+)\.", it["q"])
            if m:
                n, d = int(m.group(1)), int(m.group(2))
                want = qr(*divmod(n, d))
                assert it["c"][it["a"]] == want, (it["q"], it["c"], want)


def gen():
    rnd = random.Random(64805)
    P = People(rnd)
    used = set()
    sets = [set_facts(), set_three_digit(P), set_four_digit(P), set_remainders(rnd, used, P), set_story(P)]
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
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "division", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Division",
        "seo_title": "P4 Division Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Division",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Four Operations",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Division algorithm up to 4 digits by 1 digit",
        "meta_desc": "Free P4 division practice: facts, long division up to 4 digits by 1 digit, zeros in the quotient, remainders and word problems. 100 questions with answers.",
        "key_big": "Divide one place at a time from the left. If a place is too small to share, write 0 in the answer.",
        "key_sub": "6024 ÷ 6 = 1004 (not 104). Check: 1004 × 6 = 6024.",
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
    mark_large(u, "bar model|[0-9]+ counters|array of|place-value discs")
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
