# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Dividing by one-digit numbers (Ontario Mathematics Curriculum 2020, B2.6)
Division as sharing and grouping (with arrays), dividing with base ten blocks and area models,
short division with remainders, remainders as fractions or rounding up, Ontario word problems.
Dividends are two- or three-digit whole numbers; divisors are one-digit.
  python3 tools/gen_caon_math_g4_division.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is computed in code.
Canadian style: Canadian English, metric, $ (whole dollars here), numbers under 10 000 (no separators needed).
"""
import json, os, random, re
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#6b6259"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
NBSP = " "


# ------------------------------------------------------------ helpers
def f(n):
    """Ontario style: 4536, 10 000 (no-break space only from 5 digits)."""
    s = str(n)
    if abs(n) < 10000:
        return s
    return "{:,}".format(n).replace(",", NBSP)


def qr(q, r):
    return "%s R %d" % (f(q), r) if r else f(q)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mixed(w, num, den):
    if num == 0:
        return f(w)
    if w == 0:
        return fr(num, den)
    return "%s %s" % (f(w), fr(num, den))


def mcq(q, correct, cands, e, values=None):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers).
    values: optional function choice -> value, so no two choices are equal in value."""
    correct = str(correct)
    seen = {correct}
    vals = {values(correct)} if values else set()
    pick = []
    for c in cands:
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


def tw(t, fs, bold=True):
    return len(str(t)) * fs * (0.6 if bold else 0.56)


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def unit_word(k, i):
    w = PLACE[i]
    return "%s %s" % (f(k), w[:-1] if k == 1 else w)


def units(k, one, many):
    return "%s %s" % (f(k), one if k == 1 else many)


# ------------------------------------------------------------ division in words
def div_share(n, d, who="group"):
    """Share n into d equal groups with base ten blocks, trading what is left over."""
    ds = [int(c) for c in str(n)]
    L = len(ds)
    carry, out, started = 0, [], False
    for k, x in enumerate(ds):
        i = L - 1 - k
        amt = carry * 10 + x
        if not started and amt < d and k < L - 1:
            if amt:
                out.append("%s %s not enough for %d %ss. Trade %s for %s." % (
                    cap(unit_word(amt, i)), "is" if amt == 1 else "are", d, who, "it" if amt == 1 else "them",
                    unit_word(amt * 10, i - 1)))
            carry = amt
            continue
        started = True
        each, left = divmod(amt, d)
        lead = ("Now there are %s. " % unit_word(amt, i)) if carry else ""
        s = lead + "Share %s: each %s gets %s" % (unit_word(amt, i), who, unit_word(each, i))
        if left and i > 0:
            s += ", %s left. Trade %s for %s." % (unit_word(left, i), "it" if left == 1 else "them",
                                                  unit_word(left * 10, i - 1))
        elif left:
            s += ", %s left over." % unit_word(left, i)
        else:
            s += "."
        out.append(s)
        carry = left
    q, r = divmod(n, d)
    out.append("Each %s gets %s%s." % (who, f(q), (" and %d %s left over: %s" % (r, "is" if r == 1 else "are", qr(q, r))) if r else ""))
    chk = ("Check: %s × %d + %d = %s." % (f(q), d, r, f(n))) if r else ("Check: %s × %d = %s." % (f(q), d, f(n)))
    return " ".join(out) + " " + chk


def short_rows(n, d):
    """Short division: list of (digit index, number divided, quotient digit, remainder carried)."""
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


def short_steps(n, d):
    """Short division in words: divide each digit, carry the remainder to the next digit."""
    rows = short_rows(n, d)
    out = []
    for k, (i, cur, q, r) in enumerate(rows):
        last = k == len(rows) - 1
        nxt = None if last else rows[k + 1][1]
        if q is None:
            out.append("%d is less than %d, so carry it: %d." % (cur, d, nxt))
        elif last:
            out.append("%d ÷ %d = %s." % (cur, d, qr(q, r)))
        elif r:
            out.append("%d ÷ %d = %d R %d: write %d, carry %d to make %d." % (cur, d, q, r, q, r, nxt))
        else:
            out.append("%d ÷ %d = %d: write %d." % (cur, d, q, q))
    q, r = divmod(n, d)
    chk = ("Check: %s × %d + %d = %s." % (f(q), d, r, f(n))) if r else ("Check: %s × %d = %s." % (f(q), d, f(n)))
    return " ".join(out) + " Answer: %s. %s" % (qr(q, r), chk)


# ------------------------------------------------------------ typical mistakes
def digitwise(n, d):
    """Dividing each digit on its own and dropping what is left (52 ÷ 4 -> 1 | 0 -> 10)."""
    return int("".join(str(int(c) // d) for c in str(n)))


def no_carry(n, d):
    """Short division without carrying: every digit divided alone, remainders thrown away, but 0s kept."""
    return digitwise(n, d)


def cands_div(n, d):
    q = n // d
    dw = digitwise(n, d)
    c = ([dw] if dw * 2 > q and dw != q else []) + [q * 10, q + 1, q - 1, q + 10, q - 10, q + 2]
    return [f(x) for x in c]


def cands_rem(n, d):
    q, r = divmod(n, d)
    return [qr(q - 1, r + d), f(q), qr(q, d - r), qr(q + 1, r), qr(q - 1, r), f(q + 1)]


# ------------------------------------------------------------ figures
S = 8                      # size of one unit cube


def blocks(h, t, o, x, y):
    """Base ten blocks: flats, rods, units (units in columns of 5). Returns (svg, width, height)."""
    s = []
    cx = x
    big = 10 * S
    for _ in range(h):
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, y, big, big, FILL, GREEN))
        for k in range(1, 10):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx + k * S, y, cx + k * S, y + big, GREEN))
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx, y + k * S, cx + big, y + k * S, GREEN))
        cx += big + 5
    for _ in range(t):
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, y, S, big, FILL, GREEN))
        for k in range(1, 10):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='0.6'/>" % (cx, y + k * S, cx + S, y + k * S, GREEN))
        cx += S + 4
    hh = big if (h or t) else 0
    ncol = (o + 4) // 5
    for k in range(o):
        col, row = divmod(k, 5)
        uy = y + (hh - (row + 1) * (S + 2) if hh else row * (S + 2))
        s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx + col * (S + 3), uy, S, S, FILL, GREEN))
    w = cx - x + ncol * (S + 3) - (4 if ncol == 0 and (h or t) else 0)
    hgt = hh or min(o, 5) * (S + 2)
    return "".join(s), w, hgt


def pile_svg(n, label=None):
    """The base ten blocks for one number."""
    h, rest = divmod(n, 100)
    t, o = divmod(rest, 10)
    body, w, hgt = blocks(h, t, o, 4, 4)
    return svg_wrap(int(w + 8), int(hgt + 8), body, label or "base ten blocks showing %d" % n)


def area_svg(side, tops, inside, label, wsum=220):
    """Area model: a rectangle split into parts. tops = labels above each part ('?' = red),
    inside = text inside each part, side = label on the left."""
    FS = 18
    vals = [int(t) if str(t).isdigit() else 1 for t in inside]
    tot = float(sum(vals))
    ws = [max(56, tw(tops[k], FS) + 18, tw(inside[k], FS) + 18, wsum * vals[k] / tot) for k in range(len(tops))]
    x0, y0, h = 34, 30, 62
    s = []
    x = x0
    for k, w in enumerate(ws):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>" % (x, y0, w, h, FILL, GREEN))
        t = inside[k]
        if t:
            s.append(text(x + w / 2, y0 + h / 2 + 6, t, FS, col=RED if t == "?" else INK))
        s.append(text(x + w / 2, y0 - 9, tops[k], FS, col=RED if tops[k] == "?" else GREEN))
        x += w
    s.append(text(x0 - 15, y0 + h / 2 + 6, str(side), FS, col=GREEN))
    return svg_wrap(int(x + 4), y0 + h + 4, "".join(s), label)


def dots_svg(n, d, label=None):
    """n counters put in groups of d: each group is a column; leftovers in red at the end."""
    q, r = divmod(n, d)
    R, gap = 7, 19
    s = []
    x = 6
    for g in range(q + (1 if r else 0)):
        k = d if g < q else r
        col = GREEN if g < q else RED
        if g < q:
            s.append("<rect x='%.1f' y='3' width='%d' height='%d' rx='9' fill='none' stroke='%s' stroke-width='1.8'/>"
                     % (x - 3, 2 * R + 6, d * gap + 2, GREY))
        for j in range(k):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + R, 4 + gap / 2 + 1 + j * gap, R, col))
        x += 2 * R + 6 + (8 if g == q - 1 else 5)
    return svg_wrap(int(x), int(d * gap + 8), "".join(s), label or "%d counters in groups of %d" % (n, d))


def share_svg(n, d, label=None):
    """n counters shared into d plates: each plate is a box with n/d counters in rows of 3."""
    q = n // d
    R, gap = 6, 16
    per = 3
    rows = (q + per - 1) // per
    bw, bh = per * gap + 10, rows * gap + 10
    s = []
    x = 4
    for g in range(d):
        s.append("<rect x='%.1f' y='4' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='1.8'/>"
                 % (x, bw, bh, FILL2, GREY))
        for j in range(q):
            rr, cc = divmod(j, per)
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + 5 + gap / 2 + cc * gap, 9 + gap / 2 + rr * gap, R, GREEN))
        x += bw + 8
    return svg_wrap(int(x - 4), int(bh + 8), "".join(s), label or "%d counters shared into %d groups" % (n, d))


def array_svg(rows, cols, label=None):
    R, gap = 7, 20
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (6 + R + j * gap, 6 + R + i * gap, R, GREEN))
    return svg_wrap(int(12 + 2 * R + (cols - 1) * gap), int(12 + 2 * R + (rows - 1) * gap), "".join(s),
                    label or "array of %d rows of %d dots" % (rows, cols))


def pizza_svg(n, d, label=None):
    """n round pizzas; the leftover ones (n mod d) are cut into d equal slices."""
    q, r = divmod(n, d)
    R = 19
    s = []
    for k in range(n):
        cx, cy = 6 + R + k * (2 * R + 8), 6 + R
        cut = k >= n - r
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, FILL, GREEN))
        if cut:
            import math
            for j in range(d):
                a = -math.pi / 2 + 2 * math.pi * j / d
                s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.8'/>"
                         % (cx, cy, cx + R * math.cos(a), cy + R * math.sin(a), RED))
    W = 12 + n * (2 * R) + (n - 1) * 8
    return svg_wrap(int(W), 2 * R + 12, "".join(s), label or "%d pizzas, the last %d cut into %d equal slices" % (n, r, d))


def short_svg(n, d, work=False, label=None):
    """Short division: divisor, bracket and dividend. With work=True, the quotient and the small
    carried remainders are written in."""
    fs = 26
    cw = fs * 1.05
    ds = str(n)
    L = len(ds)
    x0 = 12 + fs * 0.62 + 18
    rh = fs * 1.25
    top = (rh + 8) if work else 10
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    by = top + rh - fs * 0.18
    for j, ch in enumerate(ds):
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>%s</text>" % (col(j), by, fs, INK, ch))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end' "
             "font-family='monospace'>%d</text>" % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * L + 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))
    H = top + bh + 6
    if work:
        rows = short_rows(n, d)
        for k, (i, cur, q, r) in enumerate(rows):
            if q is not None:
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                         "font-family='monospace'>%d</text>" % (col(i), top - 8, fs, GREEN, q))
            if k < len(rows) - 1 and r:
                s.append("<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (col(i + 1) - cw * 0.42, by - fs * 0.45, RED, r))
        q, r = divmod(n, d)
        if r:
            rt = "R %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' font-family='monospace'>%s</text>"
                     % (x0 + cw * L + 10, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 10 + len(rt) * fs * 0.62 + 6)
    lab = label or ("%d divided by %d worked out with short division" if work else "%d divided by %d written as short division") % (n, d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), lab)


# ------------------------------------------------------------ set 1: sharing and grouping
def set_groups(rnd):
    its = []
    # A: sharing pictures (d groups, how many in each)
    for n, d, thing in [(24, 4, "stickers"), (18, 3, "marbles"), (30, 5, "crackers"), (28, 4, "beads")]:
        q = n // d
        e = ("Sharing: there are %d groups, and each group gets the same number. Count one group: %d. "
             "%d ÷ %d = %d. Check: %d × %d = %d." % (d, q, n, d, q, d, q, n))
        its.append(mcq(fig(share_svg(n, d)) + "%d %s are shared equally into %d groups. How many %s are in each group?" % (n, thing, d, thing),
                       str(q), [str(d), str(q + 1), str(n), str(q - 1)], e))
    # B: grouping pictures (groups of d, how many groups)
    for n, d in [(21, 3), (32, 4), (35, 5), (24, 6)]:
        q = n // d
        e = ("Grouping: each group has %d counters. Count the groups: %d. %d ÷ %d = %d. Check: %d × %d = %d."
             % (d, q, n, d, q, q, d, n))
        its.append(mcq(fig(dots_svg(n, d)) + "%d counters are put in groups of %d. How many groups are there?" % (n, d),
                       str(q), [str(d), str(q + 1), str(n - d), str(q - 1)], e))
    # C: arrays
    for rows, cols, thing in [(4, 7, "chairs"), (3, 9, "cupcakes")]:
        n = rows * cols
        e = ("The array has %d equal rows. %d ÷ %d = %d, so each row has %d %s. Check: %d × %d = %d."
             % (rows, n, rows, cols, cols, thing, rows, cols, n))
        its.append(mcq(fig(array_svg(rows, cols)) + "These %d %s are set out in %d equal rows. How many %s are in each row?" % (n, thing, rows, thing),
                       str(cols), [str(rows), str(cols + 1), str(n - rows), str(cols - 1)], e))
    rows, cols = 6, 8
    n = rows * cols
    its.append(mcq(fig(array_svg(rows, cols)) + "Which division matches this array of %d dots?" % n,
                   "%d ÷ %d = %d" % (n, rows, cols),
                   ["%d ÷ %d = %d" % (rows, n, cols), "%d ÷ %d = %d" % (n, rows, rows), "%d − %d = %d" % (n, rows, n - rows)],
                   "There are %d rows of %d dots. Start with the total: %d ÷ %d = %d. "
                   "Writing %d ÷ %d divides the wrong way." % (rows, cols, n, rows, cols, rows, n)))
    # D: which division matches the story (dividing the wrong way)
    for t, n, d in [("Aiden puts 36 hockey cards into piles of 4. How many piles does he make?", 36, 4),
                    ("Amira shares 45 grapes equally among 5 friends. How many grapes does each friend get?", 45, 5),
                    ("A coach has 42 pylons. She puts 7 pylons on each line. How many lines does she make?", 42, 7)]:
        its.append(mcq(t + " Which division shows this?", "%d ÷ %d" % (n, d),
                       ["%d ÷ %d" % (d, n), "%d × %d" % (n, d), "%d − %d" % (n, d)],
                       "Start with the total, %d, and divide by %d: %d ÷ %d = %d. "
                       "%d ÷ %d divides the wrong way: the total always comes first." % (n, d, n, d, n // d, d, n)))
    # E: think multiplication
    for n, d in [(56, 7), (72, 9), (54, 6)]:
        q = n // d
        its.append(mcq("Which multiplication fact helps you find %d ÷ %d?" % (n, d), "%d × %d = %d" % (q, d, n),
                       ["%d × %d = %d" % (d, d, d * d), "%d × %d = %d" % (q + 1, d, (q + 1) * d), "%d × %d = %d" % (q - 1, d, (q - 1) * d),
                    "%d + %d = %d" % (n, d, n + d)],
                       "Division undoes multiplication. Ask: what number times %d is %d? %d × %d = %d, so %d ÷ %d = %d."
                       % (d, n, q, d, n, n, d, q)))
    # F: facts
    for n, d in [(63, 9), (48, 8), (81, 9)]:
        q = n // d
        cands = [str(q + 1), str(q - 1), str(n - d), str(d + 1)]
        its.append(mcq("What is %d ÷ %d?" % (n, d), str(q), cands,
                       "Think: %d × ? = %d. %d × %d = %d, so %d ÷ %d = %d." % (d, n, d, q, n, n, d, q)))
    return {"title": "Division as sharing and grouping", "items": its}


# ------------------------------------------------------------ set 2: base ten blocks and area models
def set_blocks():
    its = []
    for n, d in [(64, 4), (78, 3), (69, 3), (92, 4), (156, 3), (224, 4)]:
        its.append(mcq(fig(pile_svg(n)) + "Share these blocks equally into %d groups. How many are in each group?" % d,
                       f(n // d), cands_div(n, d), div_share(n, d)))
    its.append(mcq("You share 7 tens equally into 3 groups. Each group gets 2 tens. What do you do with the 1 ten that is left?",
                   "Trade it for 10 ones", ["Leave it out", "Trade it for 1 one", "Give it to one group"],
                   "Every group must get the same amount, so do not leave it out or give it to one group. "
                   "Trade 1 ten for 10 ones and keep sharing. For 78 ÷ 3: 10 + 8 = 18 ones, so each group gets 6 more ones. 78 ÷ 3 = 26."))
    its.append(mcq("You share 2 hundreds, 2 tens and 4 ones equally into 4 groups. There are not enough hundreds. What do you do first?",
                   "Trade 2 hundreds for 20 tens", ["Trade 2 hundreds for 20 ones", "Leave the hundreds out", "Give 1 hundred to 2 groups"],
                   "Every group needs the same amount, so trade the hundreds for tens. " + div_share(224, 4)))
    its.append(mcq("To find 85 ÷ 5, you share 8 tens: each group gets 1 ten and 3 tens are left. "
                   "You trade the 3 tens for ones. How many ones are there to share now?",
                   "35 ones", ["3 ones", "30 ones", "8 ones"],
                   "3 tens = 30 ones. Add the 5 ones you already had: 30 + 5 = 35 ones. 35 ÷ 5 = 7, so 85 ÷ 5 = 17."))
    for n, d in [(84, 6), (135, 3), (296, 4), (245, 5)]:
        ps, rest = [], n
        for scale in (100, 10):
            k = (rest // scale) // d * d * scale
            if k:
                ps.append(k)
                rest -= k
        if rest:
            ps.append(rest)
        pq = [p // d for p in ps]
        q = n // d
        svg = area_svg(d, ["?"] * len(ps), [f(p) for p in ps], "area model for %d divided by %d" % (n, d))
        e = ("The model splits %d into %s. Divide each part by %d: %s. Add: %s = %d. Check: %d × %d = %d."
             % (n, " + ".join(f(p) for p in ps), d, ", ".join("%d ÷ %d = %d" % (p, d, x) for p, x in zip(ps, pq)),
                " + ".join(str(x) for x in pq), q, q, d, n))
        cands = [f(q - pq[-1]), f(q - pq[0]), f(q * 10), f(q + 10), f(q + 1)]
        its.append(mcq(fig(svg) + "Use the area model to find %d ÷ %d." % (n, d), f(q), cands, e))
    for n, d in [(96, 8), (172, 4), (378, 6), (459, 9)]:
        its.append(mcq("What is %d ÷ %d?" % (n, d), f(n // d), cands_div(n, d), div_share(n, d)))
    for n, d, a in [(84, 4, 80), (93, 3, 90), (155, 5, 150)]:
        b = n - a
        right = "%d ÷ %d + %d ÷ %d" % (a, d, b, d)
        wrong = ["%d ÷ %d + %d" % (a, d, b), "%d ÷ %d + %d ÷ %d" % (a // 10, d, b, d), "%d ÷ %d + %d ÷ %d" % (n, d, n, d)]
        e = ("Split %d into %d + %d. Divide <b>both</b> parts by %d, then add: %d ÷ %d + %d ÷ %d = %d + %d = %d."
             % (n, a, b, d, a, d, b, d, a // d, b // d, n // d))
        its.append(mcq("Which is the same as %d ÷ %d?" % (n, d), right, wrong, e))
    return {"title": "Divide with base ten blocks", "items": its}


# ------------------------------------------------------------ set 3: short division with remainders
def pick_rem(rnd, used, lo, hi, dlo=3, dhi=9):
    while True:
        d = rnd.randint(dlo, dhi)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if r == 0 or n in used or q < 10 or "0" in str(q) or r == q % 10 or q % 10 == d - r:
            continue
        used.add(n)
        return n, d


def set_short(rnd, used, P):
    its = []
    for n, d in [(23, 5), (29, 4), (38, 6), (25, 3)]:
        used.add(n)
        q, r = divmod(n, d)
        e = ("Make groups of %d. There are %d full groups and %s left over (in red). "
             "%d is less than %d, so it cannot make another group. %d ÷ %d = %s. Check: %d × %d + %d = %d."
             % (d, q, units(r, "counter", "counters"), r, d, n, d, qr(q, r), q, d, r, n))
        its.append(mcq(fig(dots_svg(n, d)) + "The picture shows %d counters in groups of %d. What is %d ÷ %d?" % (n, d, n, d),
                       qr(q, r), cands_rem(n, d), e))
    for i in range(8):
        n, d = pick_rem(rnd, used, 41, 98) if i < 3 else pick_rem(rnd, used, 112, 989)
        q, r = divmod(n, d)
        qq = (fig(short_svg(n, d)) + "Divide.") if i % 2 == 1 else "What is %d ÷ %d?" % (n, d)
        cands = cands_rem(n, d)
        nc = digitwise(n, d)
        if nc != q and int(str(n)[0]) >= d:
            cands.insert(1, qr(nc, r))
        its.append(mcq(qq, qr(q, r), cands, short_steps(n, d)))
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980, 4)
        q, r = divmod(n, d)
        its.append(mcq("What is the remainder when %d is divided by %d?" % (n, d), str(r),
                       [f(q), str(d - r), str(r + d), str(d)],
                       "The question asks for the remainder, not the quotient. " + short_steps(n, d)))
    for _ in range(2):
        n, d = pick_rem(rnd, used, 120, 980)
        q, r = divmod(n, d)
        its.append(mcq("%d ÷ %d = %s. Which expression checks this answer? It should equal %d." % (n, d, qr(q, r), n),
                       "%d × %d + %d" % (q, d, r),
                       ["%d × %d − %d" % (q, d, r), "%d × %d + %d" % (q, r, d), "%d + %d + %d" % (q, d, r)],
                       "Multiply the quotient by the divisor, then add the remainder: %d × %d = %d, %d + %d = %d. "
                       "It matches, so the answer is right." % (q, d, q * d, q * d, r, n)))
    for _ in range(2):
        name, he, his = P.next()
        n, d = pick_rem(rnd, used, 50, 99, 4, 8)
        q, r = divmod(n, d)
        its.append(mcq("%s says %d ÷ %d = %s. What mistake did %s make?" % (name, n, d, qr(q - 1, r + d), he),
                       "The remainder is too big",
                       ["%s left out the remainder" % cap(he), "%s divided the wrong way" % cap(he), "There is no mistake"],
                       "The remainder must be less than the divisor. %d is more than %d, so one more group of %d fits: "
                       "%d − %d = %d. The answer is %s. Check: %d × %d + %d = %d." % (r + d, d, d, r + d, d, r, qr(q, r), q, d, r, n)))
    name, he, his = P.next()
    n, d = 47, 5
    its.append(mcq("%s says 47 ÷ 5 = 9. What mistake did %s make?" % (name, he),
                   "%s left out the remainder" % cap(he),
                   ["The remainder is too big", "%s divided the wrong way" % cap(he), "There is no mistake"],
                   "9 × 5 = 45, and 47 − 45 = 2. The 2 left over is part of the answer: 47 ÷ 5 = 9 R 2."))
    its.append(mcq("You divide a number by 7. Which of these could be the remainder?", "6", ["7", "8", "9"],
                   "A remainder is always less than the divisor. When you divide by 7, the remainder can only be 0 to 6. "
                   "So 6 is the only possible one."))
    return {"title": "Short division with remainders", "items": its}


# ------------------------------------------------------------ set 4: remainder as a fraction or one more
def fval(c):
    """Value of a choice like '3 <fr 1/2> pizzas', '3.1 pizzas', '4 vans' (used to keep values unique)."""
    t = re.sub(r"<span class='fn'>(\d+)</span><span class='fd'>(\d+)</span>", r" \1/\2 ", c)
    t = re.sub(r"<[^>]+>", " ", t)
    v = Fraction(0)
    for tok in t.split():
        if re.match(r"^\d+/\d+$", tok):
            v += Fraction(tok)
        elif re.match(r"^\d+(\.\d+)?$", tok):
            v += Fraction(tok)
        elif tok == "R":
            return c
    return v


def frac_item(t, n, d, one, many, cut, figure=False):
    """Share n things among d; the leftovers are cut. Answer as a mixed number."""
    q, r = divmod(n, d)
    assert r and q >= 1 and gcd(r, d) == 1
    U = lambda s: s + " " + (one if s == "1" else many)
    ans = U(mixed(q, r, d))
    cands = [U(mixed(q, r, n)) if r < n else None, U("%d.%d" % (q, r)), U(f(q)), U(mixed(q, 1, d)) if r > 1 else None,
             U(mixed(q, d - r, d)) if d - r != r else None, U(f(q + 1)), U(mixed(q, 1, r)) if r > 1 else None]
    cands = [c for c in cands if c]
    if r == 1:
        how = ("%d ÷ %d = %d R 1. Each gets %s. The 1 %s left over is %s into %d equal pieces, so each gets %s more. "
               % (n, d, q, units(q, one, many), one, cut, d, fr(1, d)))
    else:
        how = ("%d ÷ %d = %d R %d. Each gets %s. Each of the %d %s left over is %s into %d equal pieces. "
               "That makes %d pieces, so each gets %d pieces: %s more. "
               % (n, d, q, r, units(q, one, many), r, many, cut, d, r * d, r, fr(r, d)))
    e = how + "Answer: %s. (Do not write the remainder as a decimal: %d R %d is not %d.%d.)" % (ans, q, r, q, r)
    q_html = (fig(pizza_svg(n, d)) if figure else "") + t
    return mcq(q_html, ans, cands, e, values=fval)


def set_fraction(P):
    its = []
    its.append(frac_item("7 pizzas are shared equally by 2 friends. The leftover pizza is cut in half. How many pizzas does each friend get?",
                         7, 2, "pizza", "pizzas", "cut", True))
    its.append(frac_item("5 pizzas are shared equally by 4 students. The leftover pizza is cut into 4 equal slices. How many pizzas does each student get?",
                         5, 4, "pizza", "pizzas", "cut", True))
    its.append(frac_item("8 pizzas are shared equally by 3 friends. The leftover pizzas are cut into 3 equal slices. How many pizzas does each friend get?",
                         8, 3, "pizza", "pizzas", "cut", True))
    for t, n, d, one, many, cut in [
        ("9 granola bars are shared equally by 2 hikers. How many granola bars does each hiker get?", 9, 2, "granola bar", "granola bars", "cut"),
        ("11 sandwiches are shared equally by 4 friends at the cottage. How many sandwiches does each friend get?", 11, 4, "sandwich", "sandwiches", "cut"),
        ("16 muffins are shared equally by 5 students. How many muffins does each student get?", 16, 5, "muffin", "muffins", "cut"),
        ("13 m of ribbon is cut into 2 equal pieces. How long is each piece?", 13, 2, "metre", "m", "cut"),
        ("A 25 m rope is cut into 3 equal pieces. How long is each piece?", 25, 3, "metre", "m", "cut"),
        ("19 pancakes are shared equally by 6 campers. How many pancakes does each camper get?", 19, 6, "pancake", "pancakes", "cut"),
        ("17 cookies are shared equally by 3 friends. How many cookies does each friend get?", 17, 3, "cookie", "cookies", "broken"),
        ("23 L of water is poured equally into 5 coolers. How much water is in each cooler?", 23, 5, "litre", "L", "split"),
    ]:
        if many in ("m", "L"):
            # the unit is a measure: the leftover metres/litres are split, not cut objects
            q, r = divmod(n, d)
            ans = mixed(q, r, d) + " " + many
            cands = [mixed(q, r, n) + " " + many, "%d.%d %s" % (q, r, many), "%d %s" % (q, many),
                     mixed(q, 1, d) + " " + many if r > 1 else None, "%d %s" % (q + 1, many), mixed(q, d - r, d) + " " + many]
            cands = [c for c in cands if c]
            word = "metre" if many == "m" else "litre"
            if r == 1:
                how = "%d ÷ %d = %d R 1. The 1 %s left over is split into %d equal parts: %s %s each. " % (n, d, q, word, d, fr(1, d), many)
            else:
                how = ("%d ÷ %d = %d R %d. The %d %ss left over are split into %d equal parts: %d ÷ %d = %s %s each. "
                       % (n, d, q, r, r, word, d, r, d, fr(r, d), many))
            e = how + "Answer: %s. (Do not write the remainder as a decimal: %d R %d is not %d.%d.)" % (ans, q, r, q, r)
            its.append(mcq(t, ans, cands, e, values=fval))
        else:
            its.append(frac_item(t, n, d, one, many, cut))
    # which story uses a fraction / round up
    its.append(mcq("In which story does it make sense to write the remainder as a fraction?",
                   "9 pies shared by 2 families",
                   ["9 people, 2 in each canoe", "9 balls, 2 in each bag", "9 kids in teams of 2"],
                   "A pie can be cut, so each family gets 4 and a half pies: 9 ÷ 2 = 4 " + fr(1, 2) +
                   ". You cannot cut a person or a ball, so in the other stories the remainder stays a whole number."))
    its.append(mcq("In which story should you round up to the next whole number?",
                   "26 people, 4 in each car",
                   ["26 crackers shared by 4", "Full piles of 4 from 26 cards", "26 m of rope cut into 4"],
                   "26 ÷ 4 = 6 R 2. With 6 cars, 2 people still need a ride, so you need 7 cars. "
                   "The crackers and rope can be cut, and the cards question asks only for full piles."))
    # round up
    for t, n, d, one, many, who in [
        ("28 students go on a field trip. Each van holds 6 students. How many vans are needed?", 28, 6, "van", "vans", "students"),
        ("A class has 31 students. Each table seats 4 students. How many tables are needed?", 31, 4, "table", "tables", "students"),
        ("50 players come to a ringette tournament. Each change room holds 8 players. How many change rooms are needed?", 50, 8, "change room", "change rooms", "players"),
        ("A teacher prints 43 name tags. 5 name tags fit on each sheet of paper. How many sheets are needed?", 43, 5, "sheet", "sheets", "name tags"),
    ]:
        q, r = divmod(n, d)
        ans = units(q + 1, one, many)
        e = ("%d ÷ %d = %d R %d. %s hold only %d %s, so %d %s still %s room. Add 1 more: %s."
             % (n, d, q, r, cap(units(q, one, many)), q * d, who, r, who if r > 1 else who[:-1], "need" if r > 1 else "needs", ans))
        its.append(mcq(t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e))
    # leftover / full groups
    its.append(mcq("Leah has 38 cookies. She packs them in boxes of 6. How many boxes can she fill completely?",
                   "6 boxes", ["7 boxes", "6 R 2", "2 boxes"],
                   "38 ÷ 6 = 6 R 2. 6 boxes hold 36 cookies. The 2 cookies left over cannot fill another box, so the answer is 6 boxes."))
    its.append(mcq("A coach has 45 hockey pucks. He puts 8 pucks in each bucket. How many buckets can he fill completely?",
                   "5 buckets", ["6 buckets", "5 R 5", "4 buckets"],
                   "45 ÷ 8 = 5 R 5. 5 buckets hold 40 pucks. The 5 pucks left over cannot fill another bucket, so the answer is 5 buckets."))
    its.append(mcq("Zoe has 29 stickers. She puts 4 stickers on each page of her book. How many stickers are left over?",
                   "1 sticker", ["7 stickers", "3 stickers", "7 R 1"],
                   "29 ÷ 4 = 7 R 1. 7 pages use 28 stickers, and 29 − 28 = 1 sticker is left over."))
    return {"title": "Remainders as fractions or one more", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story(P):
    its = []
    D = lambda v: "$" + f(v)
    nm, he, his = P.next()
    DIV = [
        ("For the Terry Fox Run, 4 classes raise $356 together. Each class raises the same amount. How much does each class raise?", 356, 4, "$"),
        ("A hockey arena has 594 seats in 9 equal sections. How many seats are in each section?", 594, 9, "{} seats"),
        ("A sugar bush makes 128 L of maple syrup. It is poured equally into 8 large pails. How much syrup is in each pail?", 128, 8, "{} L"),
        ("%s reads a 175-page book in 7 days. %s reads the same number of pages each day. How many pages does %s read each day?"
         % (nm, cap(he), he), 175, 7, "{} pages"),
        ("A Grade 4 class collects 252 cans for the food bank. They pack the cans equally into 6 boxes. How many cans go in each box?", 252, 6, "{} cans"),
        ("A path in a park in Ottawa is 96 m long. It is split into 3 equal parts. How long is each part?", 96, 3, "{} m"),
    ]
    for t, n_, d, fmt in DIV:
        fm = D if fmt == "$" else (lambda v, s=fmt: s.format(f(v)))
        e = "Share equally, so divide: %d ÷ %d. " % (n_, d) + short_steps(n_, d) + " So the answer is %s." % fm(n_ // d)
        cands = [fm(int(x)) for x in cands_div(n_, d)]
        cands.insert(1, fm(n_ * d))
        its.append(mcq(t, fm(n_ // d), cands, e))
    # which number sentence
    for t, n, d in [("A school has 144 skates. They are put in pairs. How many pairs are there?", 144, 2),
                    ("84 students are put into teams of 7 for a soccer day. How many teams are there?", 84, 7),
                    ("A farmer packs 96 eggs in cartons of 6. How many cartons does the farmer fill?", 96, 6)]:
        its.append(mcq(t + " Which number sentence solves it?", "%d ÷ %d = %d" % (n, d, n // d),
                       ["%d ÷ %d = %d" % (d, n, n // d), "%d × %d = %d" % (n, d, n * d), "%d − %d = %d" % (n, d, n - d)],
                       "You know the total (%d) and the size of each group (%d), so divide the total by %d: %d ÷ %d = %d. "
                       "%d ÷ %d divides the wrong way." % (n, d, d, n, d, n // d, d, n)))
    # two steps
    its.append(mcq("A school buys 6 boxes of 24 freezies. The freezies are shared equally among 8 classes. How many freezies does each class get?",
                   "18 freezies", ["144 freezies", "3 freezies", "24 freezies"],
                   "Step 1: 6 × 24 = 144 freezies. Step 2: 144 ÷ 8 = 18 (14 ÷ 8 = 1 R 6, carry 6 to make 64; 64 ÷ 8 = 8). Each class gets 18 freezies."))
    nm, he, his = P.next()
    its.append(mcq("%s has $95. %s spends $11 on a book, then shares the rest equally among 3 charities. How much does each charity get?" % (nm, cap(he)),
                   "$28", ["$84", "$32", "$27"],
                   "Step 1: $95 − $11 = $84. Step 2: $84 ÷ 3 = $28 (8 ÷ 3 = 2 R 2, carry 2 to make 24; 24 ÷ 3 = 8). Each charity gets $28."))
    # round up
    for t, n, d, one, many, who in [
        ("75 people go on a canoe trip in Algonquin Park. Each canoe holds 2 people. How many canoes are needed?", 75, 2, "canoe", "canoes", "people"),
        ("A Grade 4 class goes to the skating rink. 29 students need skates, and each bin holds 4 pairs of skates. How many bins are needed?", 29, 4, "bin", "bins", "pairs"),
        ("118 campers go on an overnight trip. Each cabin sleeps 8 campers. How many cabins are needed?", 118, 8, "cabin", "cabins", "campers"),
    ]:
        q, r = divmod(n, d)
        ans = units(q + 1, one, many)
        left = units(r, who[:-1] if who != "people" else "person", who)
        e = ("%d ÷ %d = %s. %s are not enough: %s %s left. Round up to %s."
             % (n, d, qr(q, r), cap(units(q, one, many)), left, "is" if r == 1 else "are", ans))
        its.append(mcq(t, ans, [units(q, one, many), qr(q, r), units(r, one, many), units(q + 2, one, many)], e))
    # round down
    nm, he, his = P.next()
    its.append(mcq("%s has $50. A ticket to the science centre costs $8. How many tickets can %s buy?" % (nm, he),
                   "6 tickets", ["7 tickets", "6 R 2", "2 tickets"],
                   "50 ÷ 8 = 6 R 2. 6 tickets cost $48. The $2 left over is not enough for another ticket, so the answer is 6 tickets."))
    its.append(mcq("A farm stand has 230 apples. It packs them in bags of 4. How many bags can it fill completely?",
                   "57 bags", ["58 bags", "57 R 2", "2 bags"],
                   "230 ÷ 4: 23 ÷ 4 = 5 R 3, carry 3 to make 30; 30 ÷ 4 = 7 R 2. So 230 ÷ 4 = 57 R 2. "
                   "The 2 apples left over cannot fill a bag, so the answer is 57 bags."))
    # left over
    its.append(mcq("A teacher shares 75 pencil crayons equally among 9 tables. Each table gets as many as possible. How many pencil crayons are left over?",
                   "3 pencil crayons", ["8 pencil crayons", "6 pencil crayons", "8 R 3"],
                   "75 ÷ 9 = 8 R 3 (8 × 9 = 72, 75 − 72 = 3). The question asks how many are left over: 3 pencil crayons."))
    nm, he, his = P.next()
    its.append(mcq("%s has 100 loonies in a jar. %s puts them in stacks of 6. How many loonies are not in a full stack?" % (nm, cap(he)),
                   "4 loonies", ["16 loonies", "2 loonies", "16 R 4"],
                   "100 ÷ 6: 10 ÷ 6 = 1 R 4, carry 4 to make 40; 40 ÷ 6 = 6 R 4. So 100 ÷ 6 = 16 R 4. "
                   "16 stacks use 96 loonies, and 4 loonies are left over."))
    # fraction
    its.append(frac_item("At a class party, 11 pizzas are shared equally by 4 tables. How many pizzas does each table get?",
                         11, 4, "pizza", "pizzas", "cut"))
    its.append(frac_item("Grandma bakes 7 loaves of bannock. She shares them equally among 3 families. How many loaves does each family get?",
                         7, 3, "loaf", "loaves", "cut"))
    return {"title": "Division word problems", "items": its}


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
        "<h2>Sharing and grouping</h2>"
        "<p>Division splits a total into equal groups. There are two kinds of questions. "
        "<b>Sharing</b>: you know the number of groups and find how many go in each. "
        "<b>Grouping</b>: you know how many go in each group and find the number of groups. "
        "An <b>array</b> shows both at once.</p>"
        "<figure class='sn-fig'>" + array_svg(4, 7, "array of 4 rows of 7 dots") +
        "<figcaption>28 dots in 4 equal rows: 28 ÷ 4 = 7 in each row. Check: 4 × 7 = 28.</figcaption></figure>"
        "<p>Always start with the total: 28 ÷ 4, not 4 ÷ 28.</p>"
        "<h2>Divide with base ten blocks</h2>"
        "<p>To divide a bigger number, share the biggest blocks first. "
        "When some are left, <b>trade</b> them for 10 of the next smaller block and keep sharing.</p>"
        "<figure class='sn-fig'>" + pile_svg(78, "base ten blocks showing 78") +
        "<figcaption>78 ÷ 3: share 7 tens, each group gets 2 tens and 1 ten is left. Trade it for 10 ones: now there are 18 ones. "
        "Share 18 ones: each group gets 6. Each group gets 2 tens and 6 ones = 26.</figcaption></figure>"
        "<h2>Short division</h2>"
        "<p>Short division writes the same steps in a small space. Divide one digit at a time, from the left. "
        "Write the answer digit above. If something is left, carry it to the next digit as a small number.</p>"
        "<figure class='sn-fig'>" + short_svg(157, 4, True, "157 divided by 4 worked out with short division") +
        "<figcaption>1 is less than 4, so carry it: 15. 15 ÷ 4 = 3 R 3: write 3, carry 3 to make 37. "
        "37 ÷ 4 = 9 R 1. Answer: 39 R 1. Check: 39 × 4 + 1 = 157.</figcaption></figure>"
        "<h2>Remainders</h2>"
        "<p>The <b>remainder</b> is what is left when no more full groups can be made. "
        "We write it with R. The remainder is always <b>less than the number you divide by</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(23, 5, "23 counters in groups of 5") +
        "<figcaption>23 ÷ 5 = 4 R 3: 4 full groups of 5, and 3 left over (red). Check: 4 × 5 + 3 = 23.</figcaption></figure>"
        "<h2>What to do with the remainder</h2>"
        "<p>In a story, think about what the remainder means. If the leftovers can be cut, like pizza, "
        "the remainder becomes a <b>fraction</b>: share the leftovers into equal pieces too.</p>"
        "<figure class='sn-fig'>" + pizza_svg(7, 2, "7 pizzas, the last one cut in half") +
        "<figcaption>7 pizzas shared by 2 friends: 7 ÷ 2 = 3 R 1. Cut the last pizza in half. "
        "Each friend gets 3 " + fr(1, 2) + " pizzas.</figcaption></figure>" +
        table(["The question asks", "Use the remainder like this", "Example"], [
            ["Things that can be cut", "Write it as a fraction", "7 pizzas, 2 friends: 3 " + fr(1, 2) + " each"],
            ["How many are needed for everyone?", "Add 1 to the answer", "28 students, 6 per van: 5 vans"],
            ["How many full groups?", "Leave the remainder out", "38 cookies, boxes of 6: 6 boxes"],
            ["How many are left over?", "The remainder is the answer", "75 crayons, 9 tables: 3 left"],
        ]) +
        ex("Field trip", "28 students go on a field trip. Each van holds 6 students. How many vans are needed?",
           "28 ÷ 6 = 4 R 4. 4 vans hold 24 students, and 4 students still need a seat. Add 1 more van.", "5 vans") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Ignoring the remainder (47 ÷ 5 = 9)", "Write what is left: 47 ÷ 5 = 9 R 2"],
            ["Dividing the wrong way (4 ÷ 28)", "Start with the total: 28 ÷ 4 = 7"],
            ["Forgetting to carry (78 ÷ 3 = 22)", "Carry the 1 ten to the ones: 18 ÷ 3 = 6, so 26"],
            ["A remainder that is too big (23 ÷ 5 = 3 R 8)", "If the remainder is 5 or more, make one more group: 4 R 3"],
            ["Writing R as a decimal (7 ÷ 2 = 3.1)", "3 R 1 means 1 left of 2: 3 " + fr(1, 2)],
            ["28 students need 4 vans", "4 students are still waiting, so 5 vans are needed"],
        ])
    )


FAQ = [
    {"q": "What division do Grade 4 students learn in Ontario?",
     "a": "The Ontario math curriculum asks Grade 4 students to divide two- and three-digit whole numbers by one-digit numbers, using tools such as base ten blocks and arrays, and to write remainders as fractions when that makes sense."},
    {"q": "How do you write a remainder as a fraction?",
     "a": "Put the remainder over the number you divided by. 7 ÷ 2 = 3 R 1, so each person gets 3 and 1/2 pizzas. Only do this when the leftovers can be cut into equal pieces."},
    {"q": "When do you round up the answer to a division word problem?",
     "a": "Round up when everyone or everything must fit, such as people in vans or students at tables. 28 students in vans of 6 is 4 R 4, so you need 5 vans."},
    {"q": "What division facts should a Grade 4 student know?",
     "a": "In Grade 4, Ontario students are expected to recall multiplication facts up to 10 × 10 and the related division facts, such as 56 ÷ 7 = 8. These facts make dividing bigger numbers much faster."},
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


def gen():
    rnd = random.Random(44806)
    P = People(rnd)
    used = set()
    sets = [set_groups(rnd), set_blocks(), set_short(rnd, used, P), set_fraction(P), set_story(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "dividing-by-one-digit-numbers", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Dividing by One-Digit Numbers",
        "seo_title": "Grade 4 Dividing by One-Digit Numbers Worksheets: Remainders, Base Ten Blocks, Word Problems (Free, Ontario)",
        "short_title": "Dividing by one-digit numbers",
        "domain": "Number",
        "standard_code": "Grade 4: B2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the division of two- or three-digit whole numbers by one-digit whole numbers, expressing remainders as fractions when appropriate, using appropriate tools, including arrays",
        "meta_desc": "Free Grade 4 math worksheets on dividing by one-digit numbers for the Ontario curriculum: sharing and grouping, arrays, base ten blocks, short division, remainders as fractions, rounding up and word problems. 100 questions with an answer key.",
        "key_big": "Start with the total and share it into equal groups. What is left over is the remainder, and it is always less than the number you divide by.",
        "key_sub": "78 ÷ 3: share the tens, trade what is left for ones, then share the ones: 26. In a story, decide what the remainder means: cut it into a fraction (3 1/2 pizzas), add one more van, or leave it out.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(area model|[0-9]+ counters|base ten blocks showing [0-9]{3}|[0-9]+ pizzas)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
