# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Multiplication and division (National Curriculum in England)
2-digit × 1-digit (partitioning, grid method, short multiplication), 2-digit ÷ 1-digit by partitioning,
scaling and correspondence problems, word problems and missing numbers.
  python3 tools/gen_uk_maths_y3_mult_div.py
HTML attributes use single quotes (no backslashes in the JSON).
Year 3 style: numbers up to 1,000, short sentences, the 2, 3, 4, 5, 8 and 10 times tables.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
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
TABLES = [3, 4, 5, 8]          # Year 3 tables (2 and 10 are kept for the easy questions)


# ------------------------------------------------------------ helpers
def f(n):
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd, zero_ok=False):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    def _c(v):          # whole numbers of 1,000 and above get a comma
        v = str(v)
        return "{:,}".format(int(v)) if v.isdigit() and len(v) > 3 else v
    correct = _c(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = _c(c)
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
    """Partition by place value, biggest first: 23 -> [20, 3] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def carry_list(a, d):
    c, out = 0, {}
    for i, x in enumerate(digits(a)):
        p = x * d + c
        c = p // 10
        if c and i < len(digits(a)) - 1:
            out[i + 1] = c
    return out


def pounds(p):
    """Pence -> '£1.95' or '85p'."""
    return "%dp" % p if p < 100 else "£%d.%02d" % divmod(p, 100)


# ------------------------------------------------------------ figures
def grid_svg(tops, d, cells, label):
    """Grid method: partitioned parts across the top, the one-digit number down the side."""
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
    lab = label or ("grid method: %d × %d" % (a, d))
    return grid_svg([f(p) for p in ps], d, cells, lab)


def short_svg(a, d, ans="", ex=None, label=None):
    """Short multiplication in columns, ones lined up on the right.
    ans: answer row; ' ' = not written yet, '?' = red dashed box. ex: {column: exchanged digit}."""
    fs = 26
    cw = fs * 0.95
    a_s = str(a)
    nd = max(len(a_s), len(ans))
    slots = nd + 1
    W = int(cw * slots + 16)
    right = W - 8
    gap = fs * 1.22
    s = []

    def col_x(i):
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


def split_svg(whole, a, b, d=None, label=None):
    """Part-whole diagram: the whole on top, two parts below. With d: '÷ d = …' written under each part."""
    FS = 18
    bw = max(64, tw(f(whole), FS) + 26)
    pw = max(64, tw(f(max(a, b)), FS) + 26)
    gap = 40 if d is None else 70
    W = int(max(bw, 2 * pw + gap) + 8)
    cx = W / 2
    s = []
    s.append("<rect x='%.1f' y='4' width='%.1f' height='38' rx='6' fill='%s' stroke='%s' stroke-width='2.5'/>"
             % (cx - bw / 2, bw, FILL, GREEN))
    s.append(text(cx, 29, f(whole), FS))
    xs = [cx - gap / 2 - pw / 2, cx + gap / 2 + pw / 2]
    for x, v in zip(xs, (a, b)):
        s.append("<line x1='%.1f' y1='42' x2='%.1f' y2='72' stroke='%s' stroke-width='2.5'/>" % (cx, x, GREEN))
        s.append("<rect x='%.1f' y='72' width='%.1f' height='38' rx='6' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
                 % (x - pw / 2, pw, GREEN))
        s.append(text(x, 97, f(v), FS))
        if d is not None:
            s.append(text(x, 134, "÷ %d = %d" % (d, v // d), 17, col=GREEN))
    H = 116 if d is None else 142
    if d is not None:
        W = int(max(W, xs[1] + tw("÷ %d = %d" % (d, b // d), 17) / 2 + 6))
    lab = label or ("%d partitioned into %d and %d" % (whole, a, b))
    return svg_wrap(W, H, "".join(s), lab)


def dots_svg(n, group=None, label=None):
    """n counters. group=None: rows of 10. group=k: groups of k in boxes, leftovers on their own."""
    R, STEP = 8, 21
    s = []
    if group is None:
        rows = (n + 9) // 10
        W = int(10 * STEP + 10)
        H = int(rows * STEP + 10)
        for i in range(n):
            r, c = divmod(i, 10)
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (5 + STEP / 2 + c * STEP, 5 + STEP / 2 + r * STEP, R, GREEN))
    else:
        g, rem = divmod(n, group)
        gw = group * STEP + 10
        x = 4
        y0 = 4
        for _ in range(g):
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='10' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y0, gw, STEP + 12, FILL2, GREEN))
            for k in range(group):
                s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + 5 + STEP / 2 + k * STEP, y0 + 6 + STEP / 2, R, GREEN))
            x += gw + 10
        for k in range(rem):
            s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s'/>" % (x + 5 + STEP / 2 + k * STEP, y0 + 6 + STEP / 2, R, RED))
        x += rem * STEP + 10
        W = int(x + 4)
        H = int(y0 + STEP + 12 + 4)
    lab = label or ("%d counters" % n + (" in groups of %d" % group if group else ""))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ the methods, step by step
def steps_1d(a, d):
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
    return ("Partition %d = %s. %s. Add: %s = %d." %
            (a, " + ".join(str(p) for p in ps),
             ". ".join("%d × %d = %d" % (p, d, p * d) for p in ps),
             " + ".join(str(p * d) for p in ps), a * d))


# ------------------------------------------------------------ typical mistakes
def mult_wrong(a, d, skip=None, carry_first=False):
    """Short multiplication with a typical mistake (forgetting the exchange, or adding it before multiplying)."""
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
    """Each column's answer written side by side: 23 × 4 -> 8 | 12 -> 812."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def tens_as_ones(a, d):
    """Place-value slip: 20 × 4 = 8, so 23 × 4 = 8 + 12 = 20."""
    return sum(x * d for x in digits(a))


def cands_1d(a, d):
    out = [mult_wrong(a, d)]
    if concat(a, d) < 1000:
        out.append(concat(a, d))
    out.append(mult_wrong(a, d, carry_first=True))
    out.append(tens_as_ones(a, d))
    out.append(a + d)
    out.append(a * (d + 1))
    return out


# ------------------------------------------------------------ set 1: partitioning and the grid method
def pick_2x1(rnd, seen, lo=12, hi=98, ones_ex=True, tables=TABLES):
    while True:
        a, d = rnd.randint(lo, hi), rnd.choice(tables)
        if a % 10 == 0 or (a, d) in seen or a // 10 == a % 10:
            continue
        if ones_ex and (a % 10) * d < 10:
            continue
        seen.add((a, d))
        return a, d


def set_grid(rnd, seen):
    its = []
    # A: tens × 1-digit (the 20 × 4 = 8 mistake)
    for t, d in [(20, 4), (30, 5), (40, 3), (60, 8)]:
        k = t // 10
        e = "%d is %s. %s × %d = %d tens = %d." % (t, unit_word(k, 1), unit_word(k, 1), d, k * d, t * d)
        if k * d < 10:
            e += " Not %d: that would be ones, not tens." % (k * d)
        else:
            e += (" %d tens = %s and %s." % (k * d, unit_word(k * d // 10, 2), unit_word(k * d % 10, 1))) if k * d % 10 else ""
        its.append(mcq("What is %d × %d?  <i>Think: %d × %d = %d.</i>" % (t, d, k, d, k * d), str(t * d),
                       [str(k * d), str(t * d * 10), str(t + d)], e, rnd))
    # B: use the grid
    for _ in range(6):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        e = grid_steps(a, d) + " Remember: %d × %d = %d, not %d." % (t, d, t * d, t // 10 * d)
        cand = [mult_wrong(a, d), tens_as_ones(a, d), t * d + o, a + d]
        if concat(a, d) < 1000:
            cand.insert(0, concat(a, d))
        its.append(mcq(fig(grid_1d(a, d)) + "Use the grid method to find %d × %d." % (a, d), str(a * d),
                       [str(v) for v in cand], e, rnd))
    # C: one box of the grid is missing
    for k in range(4):
        a, d = pick_2x1(rnd, seen, ones_ex=False)
        t, o = parts(a)
        if k % 2 == 0:
            show, ans = ["?", str(o * d)], t * d
            wrong = [t // 10 * d, t * d * 10, t + d]
            e = "The ? box is %d × %d. %d × %d = %d, so %s × %d = %d tens = %d." % (
                t, d, t // 10, d, t // 10 * d, unit_word(t // 10, 1), d, t // 10 * d, t * d)
        else:
            show, ans = [str(t * d), "?"], o * d
            wrong = [o + d, (o - 1) * d if o > 2 else (o + 2) * d, (o + 1) * d, o * 10 + d]
            e = "The ? box is %d × %d = %d." % (o, d, o * d)
        e += " The whole grid: %d × %d = %d + %d = %d." % (a, d, t * d, o * d, a * d)
        its.append(mcq(fig(grid_1d(a, d, show)) + "What number goes in the box marked ?", str(ans),
                       [str(v) for v in wrong], e, rnd))
    # D: which partitioning is right?
    for _ in range(3):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d × %d" % (t // 10, d, o, d), "%d × %d + %d" % (t, d, o), "%d + %d × %d" % (t, o, d)]
        e = ("Partition %d into %d + %d. Multiply <b>both</b> parts by %d, then add: %d × %d + %d × %d = %d + %d = %d."
             % (a, t, o, d, t, d, o, d, t * d, o * d, a * d))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e, rnd))
    # E: missing number in the partitioning
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
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Partitioning and the grid method", "items": its}


# ------------------------------------------------------------ set 2: short multiplication
def item_1d(a, d, rnd, col):
    q = (fig(short_svg(a, d)) + "Use short multiplication.") if col else "What is %d × %d?" % (a, d)
    return mcq(q, str(a * d), [str(v) for v in cands_1d(a, d)], steps_1d(a, d), rnd)


def set_short(rnd, seen):
    its = []
    # no exchanging
    for i in range(4):
        while True:
            a, d = rnd.randint(11, 44), rnd.choice([2, 3, 4])
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
            a, d = pick_2x1(rnd, seen, 12, 32)
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
            right = str(a * d)
            wrong = [str(t * d * 10 + p0 % 10), str((t + c) * d * 10 + p0 % 10), str((p1 % 10) * 10 + p0 % 10)]
            e = ("Multiply first, then add: %d × %d + %d = %d. The tens are the last column, so write all of %d. "
                 % (t, d, c, p1, p1) + "Answer: %d." % (a * d))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Short multiplication: 2-digit × 1-digit", "items": its}


# ------------------------------------------------------------ set 3: division
def rev(n):
    return int(str(n)[::-1])


def set_divide(rnd):
    its = []
    # A: tens ÷ 1-digit with a known fact
    for a, d in [(80, 4), (60, 3), (40, 2), (90, 3)]:
        k = a // 10
        e = "%d ÷ %d = %d, so %s ÷ %d = %s = %d. Not %d: the answer is tens, not ones." % (
            k, d, k // d, unit_word(k, 1), d, unit_word(k // d, 1), a // d, k // d)
        its.append(mcq("What is %d ÷ %d?" % (a, d), str(a // d), [str(k // d), str(a * d), str(a - d)], e, rnd))
    # B: partition into tens and ones, both divide exactly
    easy = [(48, 4), (69, 3), (86, 2), (36, 3), (84, 4), (93, 3)]
    for i, (a, d) in enumerate(easy):
        t, o = parts(a)
        ans = a // d
        e = ("Partition %d = %d + %d. %d ÷ %d = %d and %d ÷ %d = %d. Add: %d + %d = %d. Check: %d × %d = %d."
             % (a, t, o, t, d, t // d, o, d, o // d, t // d, o // d, ans, ans, d, a))
        wrong = [t // d + o, t // 10 // d + o // d, rev(ans), a - d]
        q = "What is %d ÷ %d?" % (a, d)
        if i < 3:
            q = fig(split_svg(a, t, o)) + "Partition %d to help you. What is %d ÷ %d?" % (a, a, d)
        its.append(mcq(q, str(ans), [str(v) for v in wrong], e, rnd))
    # C: partition into a multiple of 10 × d and the rest
    hard = [(72, 3), (56, 4), (75, 5), (96, 8)]
    for i, (a, d) in enumerate(hard):
        k = a // (10 * d)
        big, rest = 10 * d * k, a - 10 * d * k
        ans = a // d
        e = ("%d does not split well into %d + %d, so partition %d = %d + %d. %d ÷ %d = %d and %d ÷ %d = %d. "
             "Add: %d + %d = %d. Check: %d × %d = %d."
             % (a, a // 10 * 10, a % 10, a, big, rest, big, d, big // d, rest, d, rest // d, big // d, rest // d, ans, ans, d, a))
        wrong = [big // d + rest, k + rest // d, rev(ans), a - d, ans + 10]
        q = "What is %d ÷ %d?" % (a, d)
        if i % 2 == 0:
            q = fig(split_svg(a, big, rest)) + "%d is partitioned like this. What is %d ÷ %d?" % (a, a, d)
        its.append(mcq(q, str(ans), [str(v) for v in wrong], e, rnd))
    # D: remainders (light)
    for i, (a, d) in enumerate([(17, 5), (23, 4), (38, 5), (29, 3)]):
        q_, r = divmod(a, d)
        right = "%d r %d" % (q_, r)
        over = (q_ + 1) * d - a
        wrong = ["%d r %d" % (q_ - 1, r + d), "%d r %d" % (q_ + 1, over), "%d r %d" % (q_, d - r), str(q_)]
        e = ("%d × %d = %d and %d × %d = %d, which is too many. So %d groups of %d, and %d − %d = %d left over. "
             "The remainder must be less than %d." % (q_, d, q_ * d, q_ + 1, d, (q_ + 1) * d, q_, d, a, q_ * d, r, d))
        q = "What is %d ÷ %d?" % (a, d)
        if i < 2:
            q = fig(dots_svg(a)) + "Put %d counters into groups of %d. What is %d ÷ %d?" % (a, d, a, d)
        its.append(mcq(q, right, wrong, e, rnd))
    # E: missing numbers with the inverse
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 4 = 12</b>", "48", ["3", "16", "8"],
                   "Use the inverse: ☐ = 12 × 4 = 48. Check: 48 ÷ 4 = 12.", rnd))
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 3 = 21</b>", "63", ["7", "24", "18"],
                   "Use the inverse: ☐ = 21 × 3 = 63. Check: 63 ÷ 3 = 21.", rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Dividing by partitioning", "items": its}


# ------------------------------------------------------------ set 4: scaling and correspondence
def set_scaling(rnd, P):
    its = []
    n1, n2, n3 = P.next(), P.next(), P.next()
    scal = [
        ("%s builds a tower of bricks %%s tall. %s’s tower is %%d times as tall. How tall is %s’s tower?" % (n1[0], n2[0], n2[0]),
         23, 4, lambda v: "%d cm" % v),
        ("%s has %%s stickers. %s brother has %%d times as many. How many stickers does %s brother have?" % (n3[0], cap(n3[2]), n3[2]),
         46, 3, lambda v: "%d" % v),
        ("A hamster cage is %s long. A rabbit hutch is %d times as long. How long is the rabbit hutch?",
         45, 3, lambda v: "%d cm" % v),
        ("A sunflower seedling is %s tall. A month later it is %d times as tall. How tall is it now?",
         15, 4, lambda v: "%d cm" % v),
        ("A red ribbon is %s long. A blue ribbon is %d times as long. How long is the blue ribbon?",
         18, 5, lambda v: "%d cm" % v),
        ("A comic costs %s. A book costs %d times as much. How much does the book cost?",
         65, 3, pounds),
    ]
    for t, a, d, fm in scal:
        q = t % (fm(a), d)
        e = "“%d times as …” means multiply: %s × %d. " % (d, fm(a), d) + steps_1d(a, d)
        if fm is pounds:
            e += " %dp = %s." % (a * d, pounds(a * d))
        else:
            e += " So the answer is %s." % fm(a * d)
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands_1d(a, d)], e, rnd))
    # how many times as …?
    its.append(mcq("A pencil is 8 cm long. A ruler is 24 cm long. How many times as long as the pencil is the ruler?",
                   "3 times", ["16 times", "32 times", "4 times"],
                   "How many 8s make 24? 8 × 3 = 24, so 24 ÷ 8 = 3. The ruler is 3 times as long. "
                   "(24 − 8 = 16 tells you how much longer, not how many times.)", rnd))
    nm, he, his = P.next()
    nm2 = P.next()[0]
    its.append(mcq("%s has 5 marbles. %s has 40 marbles. How many times as many marbles does %s have?" % (nm, nm2, nm2),
                   "8 times", ["35 times", "45 times", "10 times"],
                   "40 ÷ 5 = 8, because 8 × 5 = 40. (40 − 5 = 35 is how many more, not how many times.)", rnd))
    # scaling back
    nm, he, his = P.next()
    nm2 = P.next()
    its.append(mcq("%s has 36 stickers. That is 3 times as many as %s. How many stickers does %s have?" % (nm, nm2[0], nm2[0]),
                   "12", ["108", "33", "39"],
                   "%s has 3 times as many, so %s has 36 ÷ 3. 30 ÷ 3 = 10 and 6 ÷ 3 = 2, so 36 ÷ 3 = 12. "
                   "Check: 12 × 3 = 36." % (nm, nm2[0]), rnd))
    its.append(mcq("A big box holds 72 crayons. That is 4 times as many as a small box. How many crayons does a small box hold?",
                   "18", ["288", "68", "76"],
                   "Divide: 72 ÷ 4. Partition 72 = 40 + 32. 40 ÷ 4 = 10 and 32 ÷ 4 = 8, so 72 ÷ 4 = 18. Check: 18 × 4 = 72.", rnd))
    # correspondence: every one with every one
    combos = [
        ("%s has %d hats and %d scarves. An outfit is one hat and one scarf. How many different outfits can %s make?",
         2, 4, "outfits", "hat", "scarves", ["Hat 1", "Hat 2"], ["Scarf 1", "Scarf 2", "Scarf 3", "Scarf 4"]),
        ("%s has %d tops and %d skirts. An outfit is one top and one skirt. How many different outfits can %s make?",
         3, 5, "outfits", "top", "skirts", ["Top A", "Top B", "Top C"], ["Skirt 1", "Skirt 2", "Skirt 3", "Skirt 4", "Skirt 5"]),
        ("A café sells %d kinds of sandwich and %d kinds of drink. A meal deal is one sandwich and one drink. "
         "How many different meal deals are there?", 4, 3, "meal deals", "sandwich", "drinks", None, None),
        ("An ice cream van has %d flavours and %d kinds of cone. Each ice cream has one flavour and one cone. "
         "How many different ice creams can you choose?", 5, 2, "ice creams", "flavour", "cones", None, None),
        ("There are %d paths from the school to the park and %d paths from the park to the library. "
         "How many different ways can you walk from the school to the library through the park?", 3, 3, "ways",
         "path to the park", "paths on to the library", None, None),
        ("For a card, each child picks one colour of paper and one colour of pen. There are %d colours of paper and "
         "%d colours of pen. How many different cards can be made?", 4, 8, "cards", "colour of paper", "colours of pen", None, None),
    ]
    for t, n, m, unit, one, many, L, R in combos:
        if L:
            nm, he, his = P.next()
            q = fig(outfits_svg(L, R, "%d %ss each joined to %d %s" % (n, one, m, many))) + t % (nm, n, m, he)
        else:
            q = t % (n, m)
        e = "Each %s goes with all %d %s: %s = %d × %d = %d %s. Adding (%d + %d = %d) is a common mistake." % (
            one, m, many, " + ".join([str(m)] * n), n, m, n * m, unit, n, m, n + m)
        its.append(mcq(q, str(n * m), [str(v) for v in [n + m, max(n, m), 2 * (n + m), n * (m + 1)]], e, rnd))
    nm, he, his = P.next()
    its.append(mcq("%s has some hats and 4 scarves. %s can make 12 different outfits of one hat and one scarf. "
                   "How many hats does %s have?" % (nm, cap(he), he), "3", ["8", "16", "48"],
                   "Each hat makes 4 outfits. ☐ × 4 = 12, and 3 × 4 = 12, so %s has 3 hats." % he, rnd))
    its.append(mcq("A café makes 15 different meal deals from 5 kinds of sandwich and some drinks. "
                   "Each meal deal is one sandwich and one drink. How many kinds of drink are there?", "3", ["10", "20", "75"],
                   "Each sandwich goes with every drink. 5 × ☐ = 15, and 5 × 3 = 15, so there are 3 kinds of drink.", rnd))
    # n objects connected to m objects
    its.append(mcq("A car has 4 wheels. How many wheels do 17 cars have?", "68", [str(v) for v in cands_1d(17, 4)],
                   "Each car has 4 wheels, so multiply: 17 × 4. " + steps_1d(17, 4) + " Or: 10 × 4 = 40 and 7 × 4 = 28, 40 + 28 = 68.", rnd))
    its.append(mcq("Each child needs 3 pencils. There are 27 children in the class. How many pencils are needed?", "81",
                   [str(v) for v in cands_1d(27, 3)],
                   "Each child has 3 pencils, so multiply: 27 × 3. " + steps_1d(27, 3), rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Scaling and correspondence", "items": its}


# ------------------------------------------------------------ set 5: word problems and missing numbers
STORIES = [
    ("A box holds {a} pencils. The school orders {d} boxes. How many pencils is that?", 36, 4, "{} pencils"),
    ("A bag of crisps costs {a}p. {n} buys {d} bags. How much does {he} pay?", 35, 3, "p"),
    ("There are {a} children in each class. Year 3 has {d} classes. How many Year 3 children are there?", 28, 3, "{} children"),
    ("A minibus has {a} seats. The school books {d} minibuses for a trip. How many seats is that?", 16, 5, "{} seats"),
    ("A swimming pool is {a} m long. {n} swims {d} lengths. How far does {he} swim?", 25, 8, "{} m"),
    ("A packet has {a} biscuits. The teacher buys {d} packets for the class party. How many biscuits is that?", 18, 4, "{} biscuits"),
    ("The school hall has {d} rows of chairs. There are {a} chairs in each row. How many chairs are there?", 23, 8, "{} chairs"),
    ("A tub has {a} counters. The teacher has {d} tubs. How many counters is that?", 64, 3, "{} counters"),
    ("Each crate of apples has a mass of {a} kg. A lorry carries {d} crates. What is their total mass?", 32, 8, "{} kg"),
    ("A ticket to the farm park costs £{a}. {n} buys {d} tickets for {his} family. How much does {he} pay?", 13, 4, "£{}"),
]


def set_story(rnd, P):
    its = []
    for t, a, d, fmt in STORIES:
        n, he, his = P.next()
        q = cap(t.format(n=n, he=he, his=his, a=a, d=d))
        fm = pounds if fmt == "p" else (lambda v, s=fmt: s.format(v))
        e = "Equal groups, so multiply: %s × %d. " % (fm(a), d) + steps_1d(a, d)
        e += (" %dp = %s." % (a * d, pounds(a * d))) if fmt == "p" else (" So the answer is %s." % fm(a * d))
        its.append(mcq(q, fm(a * d), [fm(v) for v in cands_1d(a, d)], e, rnd))
    # division stories
    its.append(mcq("84 children are split into 4 equal teams for sports day. How many children are in each team?",
                   "21", ["24", "3", "12", "80"],
                   "84 ÷ 4. Partition: 80 ÷ 4 = 20 and 4 ÷ 4 = 1. Add: 20 + 1 = 21. Check: 21 × 4 = 84.", rnd))
    its.append(mcq("64 crayons are shared equally between 4 tables. How many crayons does each table get?",
                   "16", ["34", "7", "61", "60"],
                   "64 ÷ 4. Partition 64 = 40 + 24. 40 ÷ 4 = 10 and 24 ÷ 4 = 6. Add: 10 + 6 = 16. Check: 16 × 4 = 64.", rnd))
    its.append(mcq("A teacher has 65 cards. She puts them in packs of 5. How many packs does she make?",
                   "13", ["25", "4", "31", "60"],
                   "65 ÷ 5. Partition 65 = 50 + 15. 50 ÷ 5 = 10 and 15 ÷ 5 = 3. Add: 10 + 3 = 13.", rnd))
    its.append(mcq("26 children go to lunch. 4 children can sit at each table. How many tables are needed so every child has a seat?",
                   "7 tables", ["6 tables", "8 tables", "22 tables"],
                   "26 ÷ 4 = 6 r 2. 6 tables seat 24 children. The 2 children left over need one more table, so 7 tables.", rnd))
    # missing numbers
    its.append(mcq("What number goes in the box?  <b>☐ × 3 = 78</b>", "26", ["234", "75", "81"],
                   "Use the inverse: ☐ = 78 ÷ 3. 60 ÷ 3 = 20 and 18 ÷ 3 = 6, so ☐ = 26. Check: 26 × 3 = 78.", rnd))
    its.append(mcq("What number goes in the box?  <b>4 × ☐ = 92</b>", "23", ["368", "88", "96"],
                   "Use the inverse: ☐ = 92 ÷ 4. 80 ÷ 4 = 20 and 12 ÷ 4 = 3, so ☐ = 23. Check: 4 × 23 = 92.", rnd))
    its.append(mcq("What number goes in the box?  <b>85 ÷ ☐ = 17</b>", "5", ["68", "102", "4"],
                   "How many 17s make 85? 17 × 5 = 85 (7 × 5 = 35, write 5, exchange 3; 1 × 5 + 3 = 8). So ☐ = 5.", rnd))
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 5 = 14</b>", "70", ["9", "19", "50"],
                   "Use the inverse: ☐ = 14 × 5. Ones: 4 × 5 = 20, write 0, exchange 2 tens. Tens: 1 × 5 + 2 = 7. So ☐ = 70.", rnd))
    # two-step
    nm, he, his = P.next()
    its.append(mcq("%s buys 3 comics at 24p each. %s pays with £1. How much change does %s get?" % (nm, cap(he), he),
                   "28p", ["72p", "38p", "76p"],
                   "Step 1: cost: 3 × 24p = 72p (4 × 3 = 12, write 2, exchange 1; 2 × 3 + 1 = 7). "
                   "Step 2: change: £1 = 100p, and 100p − 72p = 28p.", rnd))
    its.append(mcq("A school buys 4 boxes of 24 pens. It gives out 50 pens. How many pens are left?",
                   "46", ["96", "36", "146"],
                   "Step 1: 4 × 24 = 96 (4 × 4 = 16, write 6, exchange 1; 2 × 4 + 1 = 9). Step 2: 96 − 50 = 46.", rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems and missing numbers", "items": its}


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
        "<p>You know your times tables. Use them to multiply bigger numbers. <b>Partition</b> the 2-digit number "
        "into tens and ones. Multiply each part. Then add.</p>"
        "<figure class='sn-fig'>" + grid_1d(23, 4, ["80", "12"], "grid method: 23 times 4") +
        "<figcaption>The grid method for 23 × 4: 20 × 4 = 80 and 3 × 4 = 12. 80 + 12 = 92.</figcaption></figure>"
        "<p>20 × 4 is 2 tens × 4 = 8 tens = 80. It is not 8.</p>"
        "<h2>Short multiplication</h2>"
        "<p>Write the numbers in columns. Start with the <b>ones</b>. If the answer is 10 or more, write the ones digit "
        "and <b>exchange</b> the ten: write a small digit under the tens column. Multiply the tens, then add it.</p>"
        "<figure class='sn-fig'>" + short_svg(47, 3, "141", {1: 2}, "47 times 3 as short multiplication") +
        "<figcaption>Ones: 7 × 3 = 21, write 1, exchange 2 tens. Tens: 4 × 3 + 2 = 14, write 14. Answer: 141.</figcaption></figure>" +
        ex("Short multiplication", "26 × 4 = ?",
           "Ones: 6 × 4 = 24. Write 4, exchange 2 tens. Tens: 2 × 4 = 8, then add the 2: 10. Write 10.", "104") +
        "<h2>Divide by partitioning</h2>"
        "<p>Partition the number into parts you can divide. Divide each part. Then add.</p>"
        "<figure class='sn-fig'>" + split_svg(48, 40, 8, 4, "48 partitioned into 40 and 8, each divided by 4") +
        "<figcaption>48 ÷ 4: 40 ÷ 4 = 10 and 8 ÷ 4 = 2. 10 + 2 = 12.</figcaption></figure>"
        "<p>Sometimes the tens do not divide. For 72 ÷ 3, use 72 = 60 + 12. 60 ÷ 3 = 20 and 12 ÷ 3 = 4, so 72 ÷ 3 = 24.</p>"
        "<p>Some numbers do not divide exactly. The amount left over is the <b>remainder</b>.</p>"
        "<figure class='sn-fig'>" + dots_svg(17, 5, "17 counters: 3 groups of 5 and 2 left over") +
        "<figcaption>17 ÷ 5 = 3 r 2: 3 groups of 5, with 2 left over.</figcaption></figure>"
        "<h2>Times as many, and every one with every one</h2>"
        "<p><b>Scaling:</b> “4 times as tall” means multiply by 4. A tower 4 times as tall as 23 cm is 23 × 4 = 92 cm.</p>"
        "<p><b>Correspondence:</b> 2 hats and 4 scarves. Each hat goes with every scarf, so there are 2 × 4 = 8 outfits, not 2 + 4.</p>"
        "<figure class='sn-fig'>" + outfits_svg(["Hat 1", "Hat 2"], ["Scarf 1", "Scarf 2", "Scarf 3", "Scarf 4"],
                                              "2 hats each joined to 4 scarves") +
        "<figcaption>Every hat is joined to every scarf: 8 lines, 8 outfits.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the exchange (23 × 4 = 82)", "Write the small 1 under the tens and add it: 8 + 1 = 9 tens, so 92"],
            ["Writing each answer side by side (23 × 4 = 812)", "12 ones = 1 ten and 2 ones. Write 2 and exchange 1 ten"],
            ["Treating 20 as 2 (20 × 4 = 8)", "20 × 4 = 2 tens × 4 = 8 tens = 80"],
            ["Dividing only the tens (48 ÷ 4 = 18)", "Divide both parts: 40 ÷ 4 = 10 and 8 ÷ 4 = 2, so 12"],
            ["Adding in a correspondence problem (2 hats, 4 scarves = 6)", "Each hat goes with every scarf: 2 × 4 = 8"],
        ])
    )


FAQ = [
    {"q": "What times tables should a Year 3 child know?",
     "a": "The 3, 4 and 8 times tables, as well as the 2, 5 and 10 times tables from Year 2. Children use these facts to multiply and divide bigger numbers, such as 23 × 4 or 48 ÷ 4."},
    {"q": "Do Year 3 children learn short multiplication?",
     "a": "Yes. Year 3 pupils multiply a 2-digit number by a 1-digit number. They start with mental methods such as partitioning and the grid method, then move on to formal written methods like short multiplication."},
    {"q": "How do you divide a 2-digit number by partitioning?",
     "a": "Split the number into parts that are easy to divide, divide each part, then add. For 48 ÷ 4: 40 ÷ 4 = 10 and 8 ÷ 4 = 2, so 48 ÷ 4 = 12."},
    {"q": "What is a correspondence problem in maths?",
     "a": "It is a problem where every item in one group is matched with every item in another. With 2 hats and 4 scarves, each hat goes with all 4 scarves, so there are 2 × 4 = 8 outfits."},
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
    rnd = random.Random(3305)
    P = People(rnd)
    seen = set()
    sets = [set_grid(rnd, seen), set_short(rnd, seen), set_divide(rnd), set_scaling(rnd, P), set_story(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "multiplication-and-division", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division",
        "seo_title": "Year 3 Multiplication and Division Worksheets: Grid Method, Short Multiplication and Scaling",
        "short_title": "Multiplication and division",
        "domain": "Multiplication and division",
        "standard_code": "Year 3: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Write and calculate mathematical statements for multiplication and division using the multiplication tables that they know, including for two-digit numbers times one-digit numbers, using mental and progressing to formal written methods; solve problems, including missing number problems, involving multiplication and division, including positive integer scaling problems and correspondence problems in which n objects are connected to m objects.",
        "meta_desc": "Free Year 3 maths worksheets on multiplication and division, following the National Curriculum: 2-digit × 1-digit numbers with partitioning, the grid method and short multiplication, dividing by partitioning, scaling, correspondence and word problems. 100 questions with an answer key.",
        "key_big": "Partition the 2-digit number. Multiply or divide each part, then add the answers.",
        "key_sub": "23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92. 48 ÷ 4 = 40 ÷ 4 + 8 ÷ 4 = 10 + 2 = 12. “3 times as long” means multiply by 3.",
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
    mark_large(u, "(\\d+ \\w+ each joined|\\d+ counters)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
