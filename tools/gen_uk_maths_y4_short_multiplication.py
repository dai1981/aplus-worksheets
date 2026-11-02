# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Short multiplication (National Curriculum in England, Multiplication and division)
  python3 tools/gen_uk_maths_y4_short_multiplication.py
HTML attributes use single quotes (no backslashes in the JSON).
Year 4 style: numbers 1,000 and above are written with commas (not inside the column layouts).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """Year 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd, zero_ok=False):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("£")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or (lead in ("0", "0p", "0.00") and not zero_ok):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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
    t = str(t)
    return (len(t) - t.count(",") * 0.6) * fs * (0.6 if bold else 0.56)


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def unit_word(k, i):
    w = PLACE[i]
    return "%d %s" % (k, w[:-1] if k == 1 else w)


def parts(n):
    """Partition by place value, biggest first: 236 -> [200, 30, 6] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def carry_list(a, d):
    """Exchanged digit going INTO each column (index = column from the right)."""
    c, out = 0, {}
    for i, x in enumerate(digits(a)):
        p = x * d + c
        c = p // 10
        if c and i < len(digits(a)) - 1:
            out[i + 1] = c
    return out


def carries(a, d):
    return len(carry_list(a, d))


# ------------------------------------------------------------ figures
def grid_svg(tops, d, cells, label):
    """Grid method: a row of partitioned parts across the top, the one-digit number down the side.
    cells = texts in the answer row ('' = empty, '?' = red question mark)."""
    FS = 18
    ws = [max(52, tw("×", FS) + 24)]
    for c, t in enumerate(tops):
        ws.append(max(62, tw(t, FS) + 24, tw(cells[c], FS) + 24))
    hs = [38, 44]
    W = int(sum(ws) + 6)
    H = int(sum(hs) + 6)
    s = []
    x = 3
    for c, w in enumerate(ws):
        y = 3
        for r, h in enumerate(hs):
            head = r == 0 or c == 0
            fill = FILL if head else "#ffffff"
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, fill, GREEN))
            if r == 0:
                t = "×" if c == 0 else tops[c - 1]
            else:
                t = str(d) if c == 0 else cells[c - 1]
            if t:
                s.append(text(x + w / 2, y + h / 2 + 6, t, FS, col=RED if t == "?" else (GREEN if head else INK)))
            y += h
        x += w
    return svg_wrap(W, H, "".join(s), label)


def grid_1d(a, d, show=None, label=None):
    ps = parts(a)
    cells = show if show else [""] * len(ps)
    lab = label or ("grid method with %d parts: %d × %d" % (len(ps), a, d))
    return grid_svg([f(p) for p in ps], d, cells, lab)


def short_svg(a, d, ans="", ex=None, label=None):
    """Short multiplication in columns, ones lined up on the right.
    ans: answer row as a string; ' ' = not written yet, '?' = red dashed box.
    ex: {column from the right: exchanged digit}, written small under the answer."""
    fs = 26
    cw = fs * 0.95
    a_s = str(a)
    nd = max(len(a_s), len(ans))
    slots = nd + 1
    W = int(cw * slots + 16)
    right = W - 8
    gap = fs * 1.22
    s = []

    def col_x(i):            # centre of column i (0 = ones)
        return right - cw * (i + 0.5)

    def row(t, y, col=INK):
        for i, ch in enumerate(reversed(t)):
            if ch == " ":
                continue
            if ch == "?":
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                         "stroke-width='2' stroke-dasharray='4 3'/>" % (col_x(i) - cw * 0.42, y - fs * 0.98, cw * 0.84, fs * 1.14, RED))
                s.append(text(col_x(i), y - 2, "?", fs, col=RED))
            else:
                s.append(text(col_x(i), y - 2, ch, fs, col=col))

    y = 6 + fs
    row(a_s, y)
    y += gap
    row(str(d), y)
    s.append(text(col_x(nd), y - 2, "×", fs, col=GREEN))
    y += 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (right - cw * slots, y, right, y, INK))
    if ans:
        y += fs + 6
        row(ans, y)
    if ex:
        y += 20
        for i, v in ex.items():
            s.append(text(col_x(i), y, str(v), 16, col=GREEN))
    H = int(y + 10)
    lab = label or ("%d times %d written as short multiplication" % (a, d))
    return svg_wrap(W, H, "".join(s), lab, font="monospace")


def outfits_svg(left, right, label):
    """Every item on the left joined to every item on the right."""
    FS = 15
    bw = max(tw(t, FS, False) for t in left + right) + 18
    bh, gapy = 28, 10
    n = max(len(left), len(right))
    H = int(n * (bh + gapy) + 10)
    W = int(bw * 2 + 110)
    x1, x2 = 6, W - 6 - bw

    def ys(k):
        off = (n - k) * (bh + gapy) / 2
        return [6 + off + i * (bh + gapy) for i in range(k)]

    s = []
    for yl in ys(len(left)):
        for yr in ys(len(right)):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6'/>"
                     % (x1 + bw, yl + bh / 2, x2, yr + bh / 2, GREEN))
    for xs, items in ((x1, left), (x2, right)):
        for t, y in zip(items, ys(len(items))):
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%d' rx='5' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (xs, y, bw, bh, FILL, GREEN))
            s.append(text(xs + bw / 2, y + bh / 2 + 5, t, FS, bold=False))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ the methods, step by step
def steps_1d(a, d):
    """Short multiplication, column by column."""
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        last = i == len(ds) - 1
        if last or p < 10:
            out.append("%s: %s = %d. Write %d." % (cap(PLACE[i]), ex_, p, p))
        else:
            out.append("%s: %s = %d. Write %d, exchange %s." % (cap(PLACE[i]), ex_, p, p % 10, unit_word(p // 10, i + 1)))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def grid_steps(a, d):
    ps = parts(a)
    return ("Partition %s = %s. %s. Add: %s = %s." %
            (f(a), " + ".join(f(p) for p in ps),
             ". ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
             " + ".join(f(p * d) for p in ps), f(a * d)))


# ------------------------------------------------------------ typical mistakes
def mult_wrong(a, d, skip=None, carry_first=False):
    """Short multiplication with a typical mistake.
    skip=None: forget every exchanged digit; skip=k: forget only the one made in column k.
    carry_first=True: add the exchanged digit BEFORE multiplying."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        p = (x + c) * d if carry_first else x * d + c
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
            if not carry_first and (skip is None or skip == i):
                c = 0
    return r


def concat(a, d):
    """Writing each column's product side by side: 23 × 4 -> 8 | 12 -> 812."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def tens_as_ones(a, d):
    """Place-value slip: 20 × 4 = 8, so 23 × 4 = 8 + 12 = 20."""
    return sum(x * d for x in digits(a))


def cands_1d(a, d):
    ds = digits(a)
    out = [mult_wrong(a, d)]
    if len(ds) == 2:
        out.append(concat(a, d))
    out.append(mult_wrong(a, d, carry_first=True))
    out += [mult_wrong(a, d, skip=k) for k in range(len(ds) - 1)]
    out.append(tens_as_ones(a, d))
    if len(ds) == 3:
        out.append(concat(a, d))
    out.append(a + d)
    return out


# ------------------------------------------------------------ set 1: partitioning and the grid method
def pick_2x1(rnd, seen, lo=12, hi=98, ones_ex=True):
    while True:
        a, d = rnd.randint(lo, hi), rnd.randint(3, 9)
        if a % 10 == 0 or (a, d) in seen or a // 10 == a % 10:
            continue
        if ones_ex and (a % 10) * d < 10:
            continue
        seen.add((a, d))
        return a, d


def set_grid(rnd, seen):
    its = []
    # A: use the grid (labels only)
    for _ in range(5):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        e = grid_steps(a, d) + " Think: %d × %d = %d, so %s × %d = %d." % (t // 10, d, t // 10 * d, unit_word(t // 10, 1), d, t * d)
        its.append(mcq(fig(grid_1d(a, d)) + "Use the grid method to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in [concat(a, d), tens_as_ones(a, d), t * d + o, a + d, mult_wrong(a, d)]], e, rnd))
    # B: one box of the grid is missing
    for k in range(5):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        if k % 2 == 0:
            show, ans, x = ["?", f(o * d)], t * d, t
            wrong = [t // 10 * d, t * d * 10, t + d]
            e = "The ? box is %d × %d. %d × %d = %d, so %s × %d = %d tens = %d." % (
                t, d, t // 10, d, t // 10 * d, unit_word(t // 10, 1), d, t // 10 * d, t * d)
        else:
            show, ans, x = [f(t * d), "?"], o * d, o
            wrong = [o + d, (o - 1) * d if o > 2 else (o + 2) * d, (o + 1) * d, o * 10 + d]
            e = "The ? box is %d × %d = %d." % (o, d, o * d)
        e += " The whole grid: %d × %d = %s + %s = %s." % (a, d, f(t * d), f(o * d), f(a * d))
        its.append(mcq(fig(grid_1d(a, d, show)) + "What number goes in the box marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # C: which partitioning is right?
    for _ in range(4):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d × %d" % (t // 10, d, o, d), "%d × %d + %d" % (t, d, o), "%d + %d × %d" % (t, o, d)]
        e = ("Partition %d into %d + %d. Multiply <b>both</b> parts by %d, then add: %d × %d + %d × %d = %s + %s = %s."
             % (a, t, o, d, t, d, o, d, f(t * d), f(o * d), f(a * d)))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e, rnd))
    # D: missing number in the partitioning
    for k in range(3):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        if k == 0:
            q = "%d × %d = %d × %d + ☐ × %d" % (a, d, t, d, d)
            ans, wrong = o, [t // 10, a, o * d]
            e = "%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is %d." % (a, t, o, a, d, t, d, o, d, o)
        elif k == 1:
            q = "%d × %d = ☐ × %d + %d × %d" % (a, d, d, o, d)
            ans, wrong = t, [t // 10, a, t * d]
            e = "%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is %d (%s, not %d)." % (
                a, t, o, a, d, t, d, o, d, t, unit_word(t // 10, 1), t // 10)
        else:
            q = "%d × %d = %d + ☐" % (a, d, t * d)
            ans, wrong = o * d, [o, o + d, (o + 1) * d]
            e = "%d × %d = %d × %d + %d × %d = %d + %d. The missing number is %d × %d = %d." % (
                a, d, t, d, o, d, t * d, o * d, o, d, o * d)
        its.append(mcq("What number goes in the box?  <b>%s</b>" % q, str(ans), [str(v) for v in wrong], e, rnd))
    rnd.shuffle(its)
    # E: 3-digit × 1-digit grids (harder, at the end)
    for _ in range(3):
        while True:
            a, d = rnd.randint(112, 789), rnd.randint(3, 8)
            if 0 in digits(a) or (a, d) in seen or carries(a, d) < 2:
                continue
            break
        seen.add((a, d))
        its.append(mcq(fig(grid_1d(a, d)) + "Use the grid method to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in [tens_as_ones(a, d), mult_wrong(a, d), sum(parts(a)[:2]) * d + a % 10,
                                       mult_wrong(a, d, carry_first=True), a + d]], grid_steps(a, d), rnd))
    return {"title": "Partitioning and the grid method", "items": its}


# ------------------------------------------------------------ set 2: short multiplication, 2-digit × 1-digit
def item_1d(a, d, rnd, col):
    q = (fig(short_svg(a, d)) + "Use short multiplication.") if col else "What is %d × %d?" % (a, d)
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], steps_1d(a, d), rnd)


def set_short2(rnd, seen):
    its = []
    # no exchanging
    for i in range(4):
        while True:
            a, d = rnd.randint(11, 44), rnd.randint(2, 4)
            t, o = divmod(a, 10)
            if o == 0 or t == o or o * d >= 10 or t * d >= 10 or (a, d) in seen:
                continue
            break
        seen.add((a, d))
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if i % 2 == 0 else "What is %d × %d?" % (a, d)
        wrong = [t * 10 + o * d, t * d * 10 + o, a + d, int(str(a * d)[::-1])]
        e = "Ones: %d × %d = %d. Tens: %d × %d = %d. Multiply <b>both</b> digits. Answer: %d." % (o, d, o * d, t, d, t * d, a * d)
        its.append(mcq(q, str(a * d), [str(v) for v in wrong], e, rnd))
    # exchange from the ones, 2-digit answer
    for i in range(4):
        while True:
            a, d = pick_2x1(rnd, seen, 12, 49)
            if a * d < 100:
                break
            seen.discard((a, d))
        its.append(item_1d(a, d, rnd, i % 2 == 1))
    # exchange, 3-digit answer
    for i in range(8):
        while True:
            a, d = pick_2x1(rnd, seen, 23, 98)
            if a * d >= 100:
                break
            seen.discard((a, d))
        its.append(item_1d(a, d, rnd, i % 2 == 0))
    # what do you write, what do you exchange?
    for k in range(4):
        while True:
            a, d = pick_2x1(rnd, seen, 23, 98)
            t, o = divmod(a, 10)
            p0 = o * d
            p1 = t * d + p0 // 10
            if p0 % 10 != p0 // 10 and p1 >= 10 and p1 % 10 and p0 % 10 and (t + p0 // 10) * d != p1:
                break
            seen.discard((a, d))
        c = p0 // 10
        if k % 2 == 0:
            q = fig(short_svg(a, d)) + "Start with the ones: %d × %d = %d. What do you do?" % (o, d, p0)
            right = "write %d, exchange %d" % (p0 % 10, c)
            wrong = ["write %d, exchange %d" % (c, p0 % 10), "write %d" % p0, "write %d only" % (p0 % 10)]
            e = ("%d ones = %s and %s. Write %d in the ones column. Exchange %s: write a small %d under the tens column. "
                 % (p0, unit_word(c, 1), unit_word(p0 % 10, 0), p0 % 10, unit_word(c, 1), c) + steps_1d(a, d))
        else:
            q = (fig(short_svg(a, d, " " + str(p0 % 10), {1: c})) +
                 "The ones are done. Now the tens: %d × %d, then add the exchanged %d. What is the full answer?" % (t, d, c))
            right = f(a * d)
            wrong = [f(t * d * 10 + p0 % 10), f((t + c) * d * 10 + p0 % 10), f((p1 % 10) * 10 + p0 % 10)]
            e = ("Multiply first, then add: %d × %d + %d = %d. The tens are the last column, so write all of %d. "
                 % (t, d, c, p1, p1) + "Answer: %s." % f(a * d))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Short multiplication: 2-digit × 1-digit", "items": its}


# ------------------------------------------------------------ set 3: short multiplication, 3-digit × 1-digit
def pick_3x1(rnd, seen, zero=False):
    while True:
        a, d = rnd.randint(112, 989), rnd.randint(3, 9)
        ds = digits(a)
        if zero:
            if ds[1] != 0 or ds[0] == 0 or ds[0] * d < 10:
                continue
        elif 0 in ds or carries(a, d) < 2:
            continue
        if (a, d) in seen:
            continue
        seen.add((a, d))
        return a, d


def set_short3(rnd, seen):
    its = []
    for i in range(13):
        a, d = pick_3x1(rnd, seen)
        its.append(item_1d(a, d, rnd, i % 2 == 0))
    # a zero in the tens
    for i in range(2):
        a, d = pick_3x1(rnd, seen, zero=True)
        c = (a % 10) * d // 10
        wrong = [mult_wrong(a, d), a * d + (d - c) * 10, (a // 100) * d * 100 + (a % 10) * d + d * 10, a + d]
        e = steps_1d(a, d) + " 0 × %d = 0, but you still add the exchanged %d." % (d, c)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if i == 0 else "What is %d × %d?" % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in wrong], e, rnd))
    # a missing digit in the answer
    for k in range(5):
        while True:
            a, d = pick_3x1(rnd, seen)
            ans = str(a * d)
            pos = 1 if k % 2 == 0 else 2
            right = int(ans[-1 - pos])
            ex = carry_list(a, d)
            cand = []
            for w in [mult_wrong(a, d, skip=pos - 1), mult_wrong(a, d, carry_first=True)]:
                ws = str(w)
                if len(ws) > pos:
                    cand.append(int(ws[-1 - pos]))
            cand += [ex.get(pos, 0), (digits(a)[pos] * d) % 10, right + ex.get(pos, 0)]
            wr = []
            for v in cand:
                if 0 <= v <= 9 and v != right and v not in wr:
                    wr.append(v)
            if len(wr) >= 3 and pos in ex:
                break
            seen.discard((a, d))
        show = list(ans)
        show[-1 - pos] = "?"
        fig_ = fig(short_svg(a, d, "".join(show), ex))
        x = digits(a)[pos]
        c = ex[pos]
        p = x * d + c
        e = ("%s column: %d × %d + %d (the exchanged digit) = %d. Write %d. "
             % (cap(PLACE[pos]), x, d, c, p, p % 10 if pos < len(digits(a)) - 1 else p))
        if pos == len(digits(a)) - 1:
            e += "The ? is the hundreds digit of %d: %d. " % (p, right)
        e += "Full working: " + steps_1d(a, d)
        its.append({"q": fig_ + "What digit goes in the box marked ?", "c": None, "_r": str(right),
                    "_w": [str(v) for v in wr], "e": e})
    out = []
    for it in its:
        if it.get("c") is None:
            out.append(mcq(it["q"], it["_r"], it["_w"], it["e"], rnd, zero_ok=True))
        else:
            out.append(it)
    rnd.shuffle(out)
    return {"title": "Short multiplication: 3-digit × 1-digit", "items": out}


# ------------------------------------------------------------ set 4: scaling, correspondence, multiply then add
def pounds(p):
    """Pence -> '£2.70' or '85p'."""
    return "%dp" % p if p < 100 else "£%d.%02d" % divmod(p, 100)


def set_scaling(rnd, P):
    its = []
    # integer scaling: (story, a, d, unit format)
    n1 = P.next()
    n2 = P.next()
    n3 = P.next()
    scal = [
        ("%s builds a tower of bricks %%s tall. %s’s tower is %%d times as tall. How tall is %s’s tower?" % (n1[0], n2[0], n2[0]),
         23, 4, lambda v: "%d cm" % v),
        ("%s has %%s stickers. %s brother has %%d times as many. How many stickers does %s brother have?" % (n3[0], cap(n3[2]), n3[2]),
         46, 3, lambda v: "%d" % v),
        ("A rabbit hutch is %s long. The run in the garden is %d times as long. How long is the run?",
         75, 3, lambda v: "%d cm" % v),
        ("A small car has a mass of %s. A lorry is %d times as heavy. What is the mass of the lorry?",
         925, 8, lambda v: "%s kg" % f(v)),
        ("A jug holds %s. A bucket holds %d times as much. How much does the bucket hold?",
         750, 4, lambda v: "%s ml" % f(v)),
        ("A chocolate bar costs %s. A big box of chocolates costs %d times as much. How much is the big box?",
         85, 6, pounds),
    ]
    for t, a, d, fm in scal:
        q = t % (fm(a), d)
        e = "“%d times as …” means multiply: %s × %d. " % (d, fm(a), d) + steps_1d(a, d)
        if fm is pounds:
            e += " %dp = %s." % (a * d, pounds(a * d))
        else:
            e += " So the answer is %s." % fm(a * d)
        cands = [mult_wrong(a, d), a + d, mult_wrong(a, d, carry_first=True), concat(a, d), a * (d + 1)]
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands], e, rnd))

    # correspondence (every one with every one)
    combos = [
        ("Isla has %d tops and %d skirts. An outfit is one top and one skirt. How many different outfits can she make?",
         3, 4, "outfits", "top", "skirts"),
        ("A café sells %d kinds of sandwich and %d kinds of drink. A meal deal is one sandwich and one drink. "
         "How many different meal deals are there?", 5, 4, "meal deals", "sandwich", "drinks"),
        ("An ice cream van has %d flavours and %d toppings. Each ice cream has one flavour and one topping. "
         "How many different ice creams can you choose?", 6, 3, "ice creams", "flavour", "toppings"),
        ("There are %d paths from the school to the park and %d paths from the park to the library. "
         "How many different ways can you walk from the school to the library through the park?", 2, 5, "ways", "path to the park", "paths on to the library"),
    ]
    for k, (t, n, m, unit, one, many) in enumerate(combos):
        q = t % (n, m)
        e = "Each %s goes with all %d %s: %s = %d × %d = %d %s. Adding (%d + %d) is a common mistake." % (
            one, m, many, " + ".join([str(m)] * n), n, m, n * m, unit, n, m)
        its.append(mcq(q, "%d" % (n * m), ["%d" % v for v in [n + m, max(n, m), 2 * (n + m), n * (m + 1)]], e, rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has some T-shirts and 3 pairs of shorts. %s can make 15 different outfits of one T-shirt and one pair of shorts. "
                   "How many T-shirts does %s have?" % (nm, cap(he), he), "5", ["12", "18", "45"],
                   "Each T-shirt makes 3 outfits. ☐ × 3 = 15, and 5 × 3 = 15, so %s has 5 T-shirts." % he, rnd))
    its.append(mcq("A school lunch menu has 4 main meals, 3 puddings and 2 drinks. Each child picks one main, one pudding and one drink. "
                   "How many different lunches are there?", "24", ["9", "12", "14"],
                   "Main and pudding: 4 × 3 = 12. Each of those goes with 2 drinks: 12 × 2 = 24.", rnd))

    # multiply then add
    nm, he, his = P.next()
    its.append(mcq("%s buys 3 packs of 24 stickers. %s already has 15 stickers. How many stickers does %s have now?" % (nm, cap(he), he),
                   "87", ["72", "42", "77"],
                   "Multiply first: 3 × 24 = 72. Then add: 72 + 15 = 87.", rnd))
    its.append(mcq("In the bike shed there are 7 bicycles and 4 tricycles. How many wheels are there altogether?",
                   "26", ["11", "22", "33"],
                   "Bicycles: 7 × 2 = 14. Tricycles: 4 × 3 = 12. Add: 14 + 12 = 26.", rnd))
    its.append(mcq("A coach has 52 seats and a minibus has 16 seats. A school hires 1 coach and 3 minibuses. How many seats is that?",
                   "100", ["68", "71", "172"],
                   "Minibuses: 3 × 16 = 48. Add the coach: 52 + 48 = 100.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s plants 4 rows of 13 tulips. Then %s plants 26 daffodils. How many flowers does %s plant?" % (nm, he, he),
                   "78", ["52", "43", "156"],
                   "Tulips: 4 × 13 = 52. Add the daffodils: 52 + 26 = 78.", rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has 6 bags of 45 marbles and 18 loose marbles. How many marbles does %s have?" % (nm, he),
                   "288", ["270", "258", "69"],
                   "Bags: 6 × 45 = 270 (5 × 6 = 30, write 0, exchange 3; 4 × 6 + 3 = 27). Add: 270 + 18 = 288.", rnd))
    its.append(mcq("Which is the same as 23 × 4 + 23 × 2?", "23 × 6", ["23 × 8", "46 × 6", "23 + 6"],
                   "4 lots of 23 and 2 more lots of 23 make 6 lots of 23: 23 × 4 + 23 × 2 = 23 × 6 = 138.", rnd))
    its.append(mcq("What number goes in the box?  <b>14 × 7 + 6 × 7 = ☐ × 7</b>", "20", ["8", "13", "98"],
                   "14 lots of 7 and 6 lots of 7 make 20 lots of 7. So ☐ = 20. Check: 98 + 42 = 140 = 20 × 7.", rnd))
    its.append(mcq("25 × 4 = 100. What is 25 × 8?", "200", ["104", "108", "400"],
                   "8 is double 4, so 25 × 8 is double 25 × 4: 100 × 2 = 200.", rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Scaling, correspondence and multiplying then adding", "items": its}


# ------------------------------------------------------------ set 5: word problems
# (story, a, d, format). {n} name, {he} pronoun, {his} possessive.
STORIES = [
    ("A coach has {a} seats. The school books {d} coaches for a trip. How many seats is that?", 52, 5, "{} seats"),
    ("A box holds {a} pencils. The school orders {d} boxes. How many pencils is that?", 144, 6, "{} pencils"),
    ("A ticket to the farm park costs £{a}. {n} buys {d} tickets for {his} family. How much does {he} pay?", 14, 6, "£{}"),
    ("A bag of crisps costs {a}p. {n} buys {d} bags for a class party. How much does {he} pay?", 45, 6, "p"),
    ("There are {a} children in each class. The juniors have {d} classes. How many junior children are there?", 28, 7, "{} children"),
    ("Each crate on a lorry has a mass of {a} kg. The lorry carries {d} crates. What is their total mass?", 136, 7, "{} kg"),
    ("A train has {d} carriages. Each carriage has {a} seats. How many seats are on the train?", 74, 6, "{} seats"),
    ("A school uses {a} sheets of paper every day. How many sheets does it use in {d} school days?", 248, 5, "{} sheets"),
    ("A swimming pool is {a} m long. {n} swims {d} lengths. How far does {he} swim?", 25, 8, "{} m"),
    ("A jar holds {a} sweets. A shop has {d} full jars. How many sweets is that?", 95, 4, "{} sweets"),
    ("{n} walks {a} m to school. How far does {he} walk to school in {d} days?", 875, 5, "{} m"),
    ("A packet has {a} biscuits. The teacher buys {d} packets for the school fair. How many biscuits is that?", 18, 7, "{} biscuits"),
    ("The school hall has {d} rows of chairs with {a} chairs in each row. How many chairs are there?", 23, 9, "{} chairs"),
    ("{n}’s book has {a} pages. A dictionary has {d} times as many pages. How many pages does the dictionary have?", 168, 6, "{} pages"),
    ("A family ticket to the zoo costs £{a}. {d} families go together. How much do they pay altogether?", 56, 3, "£{}"),
    ("The cook bakes {d} trays of {a} cupcakes for sports day. How many cupcakes is that?", 24, 9, "{} cupcakes"),
]


def set_story(rnd, P):
    its = []
    for t, a, d, fmt in STORIES:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=a, d=d)
        if fmt == "p":
            fm = pounds
        else:
            fm = lambda v, s=fmt: s.format(f(v))
        e = "Equal groups, so multiply: %d × %s. " % (d, fm(a) if fmt != "p" else "%dp" % a) + steps_1d(a, d)
        if fmt == "p":
            e += " %dp = %s." % (a * d, pounds(a * d))
        else:
            e += " So the answer is %s." % fm(a * d)
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands_1d(a, d)], e, rnd))

    # two-step problems
    n, he, his = P.next()
    its.append(mcq("%s buys 6 cinema tickets at £14 each. %s pays with £100. How much change does %s get?" % (n, cap(he), he),
                   "£16", ["£84", "£18", "£86"],
                   "Step 1: cost: 6 × £14 = £84 (4 × 6 = 24, write 4, exchange 2; 1 × 6 + 2 = 8). "
                   "Step 2: change: £100 − £84 = £16.", rnd))
    its.append(mcq("A school books 4 coaches with 54 seats each. 187 people go on the trip. How many seats are empty?",
                   "29 seats", ["216 seats", "19 seats", "403 seats"],
                   "Step 1: seats: 4 × 54 = 216 (4 × 4 = 16, write 6, exchange 1; 5 × 4 + 1 = 21). "
                   "Step 2: empty seats: 216 − 187 = 29.", rnd))
    its.append(mcq("A school has 6 boxes of 144 pencils. It gives out 500 pencils. How many pencils are left?",
                   "364 pencils", ["864 pencils", "1,364 pencils", "144 pencils"],
                   "Step 1: pencils: 6 × 144 = 864 (4 × 6 = 24, write 4, exchange 2; 4 × 6 + 2 = 26, write 6, exchange 2; "
                   "1 × 6 + 2 = 8). Step 2: 864 − 500 = 364.", rnd))
    its.append(mcq("32 children and 4 adults go to the theatre. A child’s ticket costs £7 and an adult’s ticket costs £9. "
                   "What is the total cost?", "£260", ["£224", "£252", "£324"],
                   "Children: 32 × £7 = £224. Adults: 4 × £9 = £36. Add: £224 + £36 = £260.", rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems", "items": its}


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
        "<h2>Partition, multiply, add</h2>"
        "<p>A big multiplication is a few small ones. <b>Partition</b> the bigger number into tens and ones "
        "(or hundreds, tens and ones). Multiply each part. Then add the answers.</p>"
        "<figure class='sn-fig'>" + grid_1d(23, 4, ["80", "12"], "grid method: 23 times 4") +
        "<figcaption>The grid method for 23 × 4: 20 × 4 = 80 and 3 × 4 = 12. 80 + 12 = 92.</figcaption></figure>"
        "<p>This is the same as 23 × 4 = 20 × 4 + 3 × 4. Remember that 20 × 4 is 2 tens × 4 = 8 tens = 80, not 8.</p>"
        "<h2>Short multiplication</h2>"
        "<p>Short multiplication is the formal written method. Write the numbers in columns with the ones lined up. "
        "Start with the <b>ones</b>. When an answer is 10 or more, write the ones digit and <b>exchange</b> the tens: "
        "write a small digit under the answer in the next column. <b>Multiply first, then add</b> the exchanged digit.</p>"
        "<figure class='sn-fig'>" + short_svg(346, 7, "2422", {1: 4, 2: 3}, "346 times 7 as short multiplication") +
        "<figcaption>Ones: 6 × 7 = 42, write 2, exchange 4 tens. Tens: 4 × 7 + 4 = 32, write 2, exchange 3 hundreds. "
        "Hundreds: 3 × 7 + 3 = 24, write 24. Answer: 2,422.</figcaption></figure>" +
        ex("Short multiplication", "47 × 6 = ?",
           "Ones: 7 × 6 = 42. Write 2, exchange 4 tens. Tens: 4 × 6 = 24, then add the 4: 28. Write 28.", "282") +
        "<p>Check with an estimate: 47 is close to 50, and 50 × 6 = 300. So 282 makes sense.</p>"
        "<h2>Times as many, and every one with every one</h2>"
        "<p><b>Scaling:</b> “4 times as tall” means multiply by 4. A tower 4 times as tall as 23 cm is 23 × 4 = 92 cm.</p>"
        "<p><b>Correspondence:</b> 3 tops and 4 skirts. Each top goes with every skirt, so there are 3 × 4 = 12 outfits, not 3 + 4.</p>"
        "<figure class='sn-fig'>" + outfits_svg(["Top A", "Top B", "Top C"], ["Skirt 1", "Skirt 2", "Skirt 3", "Skirt 4"],
                                              "3 tops each joined to 4 skirts") +
        "<figcaption>Every top is joined to every skirt: 12 lines, 12 outfits.</figcaption></figure>"
        "<p><b>Multiply, then add:</b> 3 packs of 24 stickers and 15 more is 3 × 24 + 15 = 72 + 15 = 87.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the exchanged digit (23 × 4 = 82)", "Write the small digit under the next column and add it: 92"],
            ["Adding the exchanged digit first (47 × 6 = 482)", "Multiply first: 4 × 6 = 24, then add 4: 28"],
            ["Writing each answer side by side (23 × 4 = 812)", "12 ones = 1 ten and 2 ones. Write 2, exchange 1 ten: 8 tens + 1 ten = 9 tens"],
            ["Treating 20 as 2 in the grid (20 × 4 = 8)", "20 × 4 = 2 tens × 4 = 8 tens = 80"],
            ["Adding in a correspondence problem (3 tops, 4 skirts = 7)", "Each top goes with every skirt: 3 × 4 = 12"],
        ])
    )


FAQ = [
    {"q": "What is short multiplication?",
     "a": "It is the formal written method for multiplying by a one-digit number. You write the numbers in columns, multiply the ones first, and write any exchanged digit small in the next column so you can add it after multiplying."},
    {"q": "What is the grid method in maths?",
     "a": "You partition the number into hundreds, tens and ones, write the parts across a grid and multiply each one. For 23 × 4 the grid shows 20 × 4 = 80 and 3 × 4 = 12, and 80 + 12 = 92."},
    {"q": "What times tables should a Year 4 child know?",
     "a": "All of them up to 12 × 12. The National Curriculum expects children to recall multiplication and division facts for every table up to 12 × 12 by the end of Year 4."},
    {"q": "What is the Multiplication Tables Check?",
     "a": "It is a short online check that Year 4 children in England take in June. There are 25 times tables questions up to 12 × 12, with 6 seconds to answer each one."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            c[it["a"]], c[t] = c[t], c[it["a"]]
            it["a"] = t


def gen():
    rnd = random.Random(4407)
    P = People(rnd)
    seen = set()
    sets = [set_grid(rnd, seen), set_short2(rnd, seen), set_short3(rnd, seen), set_scaling(rnd, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            pos[it["a"]] += 1
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
        assert pos == [5, 5, 5, 5], pos
    return {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "short-multiplication", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Short Multiplication",
        "seo_title": "Year 4 Short Multiplication Worksheets: Grid Method and Formal Written Method",
        "short_title": "Short multiplication",
        "domain": "Multiplication and division",
        "standard_code": "Year 4: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply two-digit and three-digit numbers by a one-digit number using formal written layout; solve problems involving multiplying and adding, including using the distributive law to multiply two digit numbers by one digit, integer scaling problems and harder correspondence problems such as n objects are connected to m objects.",
        "meta_desc": "Free Year 4 maths worksheets on short multiplication: partitioning and the grid method, 2-digit and 3-digit × 1-digit numbers with exchanging, scaling and correspondence problems, and word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Multiply the ones first. Exchange the tens and add them after you multiply the next column.",
        "key_sub": "47 × 6: 7 × 6 = 42, write 2 and exchange 4. Then 4 × 6 = 24, add the 4 to make 28. Answer: 282. The grid method shows why: 40 × 6 + 7 × 6 = 240 + 42.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "grid method with 3 parts")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
