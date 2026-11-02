# -*- coding: utf-8 -*-
"""
Australia Year 5 Maths: Multiplication (Australian Curriculum v9.0, AC9M5N06)
  python3 tools/gen_au_maths_y5_multiplication.py
Mental strategies (doubling and halving, × 10 and × 100, changing the order, 99 × 6 = 600 − 6),
the area model / partitioning, short multiplication (3- and 4-digit × 1-digit), long multiplication
(2- and 3-digit × 2-digit) with estimating to check, then word problems in Australian contexts.
Every product and every wrong answer is computed here (wrong answers = real student mistakes).
HTML attributes use single quotes (no backslashes in the JSON). Australian English ("regroup").
Numbers of 5 or more digits use a no-break space between groups of three (12 350); 4-digit numbers
have no separator (4536). Column layouts are drawn without separators, as students write them.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4536, 12350 -> 12 350 (no-break space)."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def mcq(q, correct, cands, e, rnd, zero_ok=False):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1 if c.startswith(("Yes", "No")) else 0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or (lead == "0" and not zero_ok):
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


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def unit_word(k, i):
    w = PLACE[i]
    return "%d %s" % (k, w[:-1] if k == 1 else w)


def parts(n):
    """Expanded form, biggest place first: 236 -> [200, 30, 6] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def svg_wrap(w, h, body, label, family=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def tw(t, fs):
    """Approximate text width in px (Arial bold). Spaces are narrow."""
    t = str(t)
    return (len(t) - t.count(NB) * 0.55) * fs * 0.6


def text(x, y, t, fs=17, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


# ------------------------------------------------------------ area model figure
def area_svg(tops, lefts, cells, label):
    """Area model. tops = labels over the columns, lefts = labels beside the rows,
    cells[r][c] = text in each part ('' = empty, '?' = red question mark)."""
    FS = 17
    ws = []
    for c, t in enumerate(tops):
        need = max([tw(t, FS)] + [tw(cells[r][c], FS) for r in range(len(lefts))]) + 22
        base = {1: 62, 2: 100, 3: 130}.get(len(str(t)), 150)
        ws.append(max(need, base))
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 20)
    hs = [58] if len(lefts) == 1 else [70, 46]
    lw = max(tw(t, FS) for t in lefts) + 14
    top_h = 26
    x0, y0 = lw + 4, top_h + 4
    W = int(x0 + sum(ws) + 6)
    H = int(y0 + sum(hs) + 6)
    s = []
    x = x0
    for c, w in enumerate(ws):
        s.append(text(x + w / 2, top_h - 4, tops[c], FS))
        y = y0
        for r, h in enumerate(hs):
            fill = FILL if (r + c) % 2 == 0 else FILL2
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>"
                     % (x, y, w, h, fill, GREEN))
            t = cells[r][c]
            if t:
                s.append(text(x + w / 2, y + h / 2 + 6, t, FS, col=RED if t == "?" else INK))
            y += h
        x += w
    y = y0
    for r, h in enumerate(hs):
        s.append(text(lw - 2, y + h / 2 + 6, lefts[r], FS, anchor="end"))
        y += h
    return svg_wrap(W, H, "".join(s), label)


def area_1d(a, d, show=None):
    ps = parts(a)
    cells = [show if show else [""] * len(ps)]
    return area_svg([f(p) for p in ps], [str(d)], cells, "area model with %d parts: %d × %d" % (len(ps), a, d))


def area_2d(a, b, show=None):
    ta, oa = parts(a)
    tb, ob = parts(b)
    cells = show or [["", ""], ["", ""]]
    return area_svg([str(ta), str(oa)], [str(tb), str(ob)], cells, "area model with 4 parts: %d × %d" % (a, b))


# ------------------------------------------------------------ short multiplication figure
def short_svg(a, d, ans="", ex=None, label=None):
    """Short multiplication in columns, ones lined up on the right.
    ans: answer row as a string; '?' = red dashed box. ex: {column from the right: regrouped digit}."""
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

    def txt(x, y, t, size, col):
        return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                % (x, y, size, col, t))

    def row(t, y):
        for i, ch in enumerate(reversed(t)):
            if ch == " ":
                continue
            if ch == "?":
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                         "stroke-width='2' stroke-dasharray='4 3'/>" % (col_x(i) - cw * 0.42, y - fs * 0.98, cw * 0.84, fs * 1.14, RED))
                s.append(txt(col_x(i), y - 2, "?", fs, RED))
            else:
                s.append(txt(col_x(i), y - 2, ch, fs, INK))

    y = 6 + fs
    row(a_s, y)
    y += gap
    row(str(d), y)
    s.append(txt(col_x(nd), y - 2, "×", fs, GREEN))
    y += 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (right - cw * slots, y, right, y, INK))
    if ans:
        y += fs + 6
        row(ans, y)
    if ex:
        y += 20
        for i, v in sorted(ex.items()):
            s.append(txt(col_x(i), y, str(v), 16, GREEN))
    H = int(y + 10)
    lab = label or ("%d times %d written as short multiplication" % (a, d))
    return svg_wrap(W, H, "".join(s), lab, "monospace")


def carry_list(a, d):
    """Regrouped digit going INTO each column (index = column from the right)."""
    c, out = 0, {}
    ds = digits(a)
    for i, x in enumerate(ds):
        p = x * d + c
        c = p // 10
        if c and i < len(ds) - 1:
            out[i + 1] = c
    return out


def carries(a, d):
    return len(carry_list(a, d))


# ------------------------------------------------------------ long multiplication figure
def column_svg(rows, rules, label, notes=None, big=False):
    """Long multiplication in columns, ones lined up on the right.
    rows = list of (sign, text) or (sign, text, nz): nz = number of place-holder zeros at the end (drawn green).
    sign 'ex' = a row of small regrouped digits: text is a dict {place: digit}.
    text '[?]' = a red dashed box across the row; a '?' inside a number = one red missing digit."""
    fs = 28 if big else 26
    cw = fs * 0.78
    efs = 15
    rows = [r if len(r) == 3 else (r[0], r[1], 0) for r in rows]
    lens = []
    for sg, t, nz in rows:
        if sg == "ex":
            lens.append(max(t) + 1 if t else 0)
        else:
            lens.append(0 if t == "[?]" else len(t))
    nd = max(lens)
    signed = max([nd if t == "[?]" else n for (sg, t, nz), n in zip(rows, lens) if sg and sg != "ex"] or [0])
    sign_slot = max(nd, signed + 1)
    slots = sign_slot + 1
    nfs = 16
    note_w = 0
    if notes:
        note_w = max(len(n) * nfs * 0.54 for n in notes if n) + 18
    num_w = cw * slots + 20
    W = int(num_w + note_w + 0.999)
    gap = fs * 1.2
    egap = efs + 4
    right = num_w - 10
    s = []
    y = 10
    for r, (sg, t, nz) in enumerate(rows):
        if sg == "ex":
            y += egap
            for i, v in sorted(t.items()):
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                         % (right - cw * (i + 0.5), y - 2, efs, GREEN, v))
            if notes and r < len(notes) and notes[r]:
                s.append("<text x='%.1f' y='%.1f' font-size='%d' fill='%s' font-family='%s'>%s</text>"
                         % (num_w + 8, y - 2, 14, NOTE, FONT, notes[r]))
            continue
        y += gap
        if t == "[?]":
            x1 = right - cw * nd
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='none' stroke='%s' "
                     "stroke-width='2' stroke-dasharray='5 3'/>" % (x1 + 3, y - fs * 0.86, cw * nd - 3, fs * 0.98, RED))
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (x1 + cw * nd / 2, y - 2, fs, RED))
        else:
            for slot, ch in enumerate(reversed(t)):
                col = GREEN if slot < nz else INK
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (right - cw * (slot + 0.5), y - 2, fs, col, ch))
        if sg:
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (right - cw * (sign_slot + 0.5), y - 2, fs, GREEN, sg))
        if notes and r < len(notes) and notes[r]:
            s.append("<text x='%.1f' y='%.1f' font-size='%d' fill='%s' font-family='%s'>%s</text>"
                     % (num_w + 8, y - 4, nfs, NOTE, FONT, notes[r]))
        if r in rules:
            y += 5
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
            y += 5
    H = int(y + 12)
    return svg_wrap(W, H, "".join(s), label, "monospace")


def col_problem(a, b):
    return column_svg([("", str(a)), ("×", str(b))], [1], "%d times %d written as long multiplication" % (a, b))


def pp_rows(a, b):
    """The rows of long multiplication, ones row first: (digit, place, value)."""
    return [(d, i, a * d * 10 ** i) for i, d in enumerate(digits(b))]


def work_rows(a, b, box=None):
    pr = pp_rows(a, b)
    rows = [("", str(a)), ("×", str(b))]
    for k, (d, i, v) in enumerate(pr):
        sg = "+" if k == len(pr) - 1 else ""
        rows.append((sg, "[?]") if box == k else (sg, str(v), i))
    rules = [1, len(rows) - 1]
    rows.append(("", "[?]") if box == "sum" else ("", str(a * b)))
    return rows, rules


def work_svg(a, b, **kw):
    rows, rules = work_rows(a, b, **kw)
    return column_svg(rows, rules, "%d times %d as long multiplication" % (a, b))


# ------------------------------------------------------------ explanations
def steps_short(a, d):
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        last = i == len(ds) - 1
        if last or p < 10:
            out.append("%s: %s = %d. Write %d." % (cap(PLACE[i]), ex_, p, p))
        else:
            out.append("%s: %s = %d. Write %d, regroup %d." % (cap(PLACE[i]), ex_, p, p % 10, p // 10))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def steps_1d(a, d):
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        if i == len(ds) - 1 or p < 10:
            out.append("%s = %d, write %d" % (ex_, p, p))
        else:
            out.append("%s = %d, write %d, regroup %d" % (ex_, p, p % 10, p // 10))
        c = p // 10 if i < len(ds) - 1 else 0
    return "; ".join(out)


def row_text(a, d, i):
    v = a * d * 10 ** i
    if i == 0:
        return "%s × %d = %s" % (f(a), d, f(v))
    return "%s × %s = %s (write the place-holder 0, then %s × %d = %s)" % (f(a), f(d * 10 ** i), f(v), f(a), d, f(a * d))


def steps(a, b, detail=None):
    pr = pp_rows(a, b)
    out = []
    for k, (d, i, v) in enumerate(pr):
        if k == detail:
            if i == 0:
                out.append("Row %d: %s × %d = %s (%s)." % (k + 1, f(a), d, f(v), steps_1d(a, d)))
            else:
                out.append("Row %d: %s × %s = %s (write 0, then %s)." % (k + 1, f(a), f(d * 10 ** i), f(v), steps_1d(a, d)))
        else:
            out.append("Row %d: %s." % (k + 1, row_text(a, d, i)))
    out.append("Add: %s = %s." % (" + ".join(f(v) for d, i, v in pr), f(a * b)))
    return " ".join(out)


def pp_1d(a, d):
    ps = parts(a)
    prods = [p * d for p in ps]
    return ("Partition %s = %s. %s. Add: %s = %s." %
            (f(a), " + ".join(f(p) for p in ps),
             ". ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
             " + ".join(f(p) for p in prods), f(a * d)))


def pp_2d(a, b):
    ta, oa = parts(a)
    tb, ob = parts(b)
    pr = [ta * tb, oa * tb, ta * ob, oa * ob]
    return ("Partition %d = %d + %d and %d = %d + %d. %d × %d = %s, %d × %d = %s, %d × %d = %s, %d × %d = %s. "
            "Add: %s = %s." % (a, ta, oa, b, tb, ob, ta, tb, f(pr[0]), oa, tb, f(pr[1]), ta, ob, f(pr[2]), oa, ob, f(pr[3]),
                               " + ".join(f(p) for p in pr), f(a * b)))


# ------------------------------------------------------------ typical mistakes
def mult_row(a, d, mode="ok", k=None):
    """a × d (one digit), done with a typical mistake.
    nocarry: forget every regrouped digit. skip: forget the one made in place k.
    cfirst: add the regrouped digit BEFORE multiplying. zero_d: think 0 × d = d."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        if mode == "cfirst":
            p = (x + c) * d
        elif mode == "zero_d" and x == 0:
            p = d + c
        else:
            p = x * d + c
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
            if mode == "nocarry" or (mode == "skip" and k == i):
                c = 0
    return r


def cands_1d(a, d):
    n = len(str(a))
    out = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst")]
    out += [mult_row(a, d, "skip", k) for k in range(n - 1)]
    out += [a * d * 10, a * (d - 1), a + d]
    return out


def tens_as_ones(a, d):
    """Treating every digit as ones: 47 × 6 -> 4 × 6 + 7 × 6 = 66."""
    return sum(x * d for x in digits(a))


def total_with(a, b, mode, only=None, k=None):
    t = 0
    for j, (d, i, v) in enumerate(pp_rows(a, b)):
        if only is None or only == j:
            t += mult_row(a, d, mode, k) * 10 ** i
        else:
            t += v
    return t


def no_zero(a, b):
    """No place-holder zero: the tens row is 10 times too small."""
    return sum(a * d for d in digits(b))


def add_cols(nums, drop=None, extra=None):
    L = max(len(str(n)) for n in nums)
    c, r = 0, 0
    for i in range(L):
        s = sum(n // 10 ** i % 10 for n in nums) + c
        if i == L - 1:
            return r + s * 10 ** i
        r += (s % 10) * 10 ** i
        c = s // 10
        if drop == "all" or drop == i:
            c = 0
        if extra == i:
            c += 1


def add_carries(nums):
    out, c = [], 0
    for i in range(max(len(str(n)) for n in nums) - 1):
        s = sum(n // 10 ** i % 10 for n in nums) + c
        c = s // 10
        if c:
            out.append(i)
    return out


def two_pp(a, b):
    """Only tens × tens and ones × ones: 34 × 26 -> 600 + 24."""
    return (a // 10) * (b // 10) * 100 + (a % 10) * (b % 10)


def skip_pp(a, b):
    """Left out one part (ones of a × tens of b)."""
    return a * b - (a % 10) * (b // 10) * 10


def one_zero(a, b):
    """tens × tens written with one zero: 30 × 20 = 60."""
    return a * b - (a // 10) * (b // 10) * 90


def cands(a, b, rnd):
    pr = pp_rows(a, b)
    out = [no_zero(a, b)]
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"), add_cols([v for d, i, v in pr], drop="all")]
    more += [total_with(a, b, "nocarry", only=j) for j in range(len(pr))]
    if len(str(a)) == 2:
        more.append(two_pp(a, b))
    rnd.shuffle(more)
    return out + more + [a * (b % 10), total_with(a, b, "skip", k=0), total_with(a, b, "skip", k=1)]


# ------------------------------------------------------------ set 1: mental strategies
def set_mental(rnd):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, f(ans), [f(w) for w in wrong], e, rnd))

    # multiples of 10, 100, 1000 × a one-digit number
    for t, z, d, nb in [(6, 1, 7, 8), (4, 2, 6, 5), (9, 2, 8, 7), (5, 1, 8, None), (3, 3, 7, 8)]:
        a = t * 10 ** z
        ans = a * d
        wrong = [t * d * 10 ** (z - 1) if t * d % 10 else t * d * 10 ** (z + 1),
                 t * d * 10 ** (z + 1) if t * d % 10 else t * d * 10 ** (z - 1)]
        wrong.append(t * nb * 10 ** z if nb else a + d)
        zw = {1: "tens", 2: "hundreds", 3: "thousands"}[z]
        e = "%s is %d %s. %d × %d = %d, so %d %s × %d = %d %s = %s." % (
            f(a), t, zw, t, d, t * d, t, zw, d, t * d, zw, f(ans))
        if t * d % 10 == 0:
            e += " The 0 in %d is part of the fact, so do not drop it." % (t * d)
        add("What is %s × %d?" % (f(a), d), ans, wrong, e)
    # × 100 and × 1000
    add("What is 58 × 100?", 5800, [580, 58000, 158],
        "× 100 makes every digit 100 times bigger: the 8 ones become 8 hundreds. 58 × 100 = 5800 (two zeros on the end).")
    add("What is 27 × 1000?", 27000, [2700, 270000, 1027],
        "× 1000 moves every digit three places to the left: 27 × 1000 = 27 000 (three zeros on the end).")
    # two multiples of 10
    add("What is 70 × 80?", 5600, [560, 56000, 150],
        "Use 7 × 8 = 56. 70 has one zero and 80 has one zero, so put back two zeros: 70 × 80 = 5600.")
    add("What is 30 × 400?", 12000, [1200, 120000, 430],
        "Use 3 × 4 = 12. 30 has one zero and 400 has two zeros, so put back three zeros: 30 × 400 = 12 000.")
    # change the order to make 100 or 10
    for p, q_, r, wrong, how in [
            (25, 4, 7, [175, 7000, 36], "25 × 4 = 100, then 100 × 7 = 700"),
            (5, 17, 2, [85, 1700, 24], "change the order: 5 × 2 = 10, then 10 × 17 = 170"),
            (2, 36, 5, [72, 3600, 180], "change the order: 2 × 5 = 10, then 10 × 36 = 360")]:
        ans = p * q_ * r
        assert str(ans) in how
        add("What is %d × %d × %d?" % (p, q_, r), ans, wrong,
            "You can multiply in any order. %s. Multiply all three numbers, not just two." % cap(how))
    # doubling and halving
    add("Double, then double again, to find 37 × 4.", 148, [74, 296, 1480],
        "× 4 is double, then double again. Double 37 = 74. Double 74 = 148. Doubling only once gives 74; three times gives 296.")
    add("Multiply by 10, then halve, to find 46 × 5.", 230, [460, 23, 2300],
        "× 5 is the same as × 10, then halve. 46 × 10 = 460. Half of 460 = 230.")
    add("What is 16 × 25? (Hint: halve one number and double the other.)", 400, [800, 200, 4000],
        "Halve 16 and double 25: 16 × 25 = 8 × 50 = 4 × 100 = 400. If you double one number, you must halve the other.")
    add("What is 18 × 50?", 900, [1800, 90, 9000],
        "× 50 is the same as × 100, then halve. 18 × 100 = 1800. Half of 1800 = 900.")
    assert 12 * 7 == 84 and 24 * 7 == 168
    add("12 × 7 = 84. What is 24 × 7?", 168, [42, 336, 91],
        "24 is double 12, so 24 × 7 is double 84 = 168.")
    # near a multiple of 10 or 100
    add("What is 99 × 6? (Hint: 99 is 1 less than 100.)", 594, [599, 606, 600],
        "99 × 6 = 100 × 6 − 1 × 6 = 600 − 6 = 594. Take away one 6, not 1.")
    add("What is 19 × 8?", 152, [159, 168, 160],
        "19 × 8 = 20 × 8 − 8 = 160 − 8 = 152. Take away one 8, not 1.")
    assert 8 * 25 == 200 and 8 * 24 == 192
    add("8 × 25 = 200. What is 8 × 24?", 192, [199, 175, 208],
        "24 is one less than 25, so take away one 8: 200 − 8 = 192.")
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Mental strategies: doubling, halving, × 10 and × 100", "items": its}


# ------------------------------------------------------------ set 2: area model and partitioning
def pick_2x1(rnd, seen, nd):
    while True:
        a, d = rnd.randint(10 ** (nd - 1) + 1, 10 ** nd - 1), rnd.randint(3, 9)
        if 0 in digits(a) or (a, d) in seen or carries(a, d) < nd - 1:
            continue
        seen.add((a, d))
        return a, d


def pick_2x2(rnd, seen, hi=89):
    while True:
        a, b = rnd.randint(13, hi), rnd.randint(13, 69)
        if a % 10 < 2 or b % 10 < 2 or a // 10 == a % 10 or b // 10 == b % 10 or a == b:
            continue
        if (a, b) in seen or (b, a) in seen or (a, b) == (34, 26):
            continue
        if carries(a, b % 10) == 0 or carries(a, b // 10) == 0:
            continue
        seen.add((a, b))
        return a, b


def set_area(rnd, seen):
    its = []
    # A: area model, 2- and 3-digit × 1-digit
    for nd in (2, 2, 3, 3):
        a, d = pick_2x1(rnd, seen, nd)
        ps = parts(a)
        lost = (ps[0] // 10) * d + sum(p * d for p in ps[1:])          # dropped a zero in the biggest part
        wrong = [tens_as_ones(a, d), lost, mult_row(a, d, "nocarry"), a + d]
        its.append(mcq(fig(area_1d(a, d)) + "Use the area model to find %s × %d." % (f(a), d), f(a * d),
                       [f(v) for v in wrong], pp_1d(a, d), rnd))
    # B: area model, 2-digit × 2-digit (34 × 26 first)
    pairs = [(34, 26)] + [pick_2x2(rnd, seen, hi=79) for _ in range(5)]
    for a, b in pairs:
        wrong = [two_pp(a, b), skip_pp(a, b), one_zero(a, b), no_zero(a, b), a + b]
        its.append(mcq(fig(area_2d(a, b)) + "Use the area model to find %d × %d." % (a, b), f(a * b),
                       [f(v) for v in wrong], pp_2d(a, b), rnd))
    # C: the missing part of an area model
    for k in range(4):
        a, b = pick_2x2(rnd, seen, hi=79)
        ta, oa = parts(a)
        tb, ob = parts(b)
        grid = [[ta * tb, oa * tb], [ta * ob, oa * ob]]
        lab = [[(ta, tb), (oa, tb)], [(ta, ob), (oa, ob)]]
        r, c = [(0, 0), (0, 1), (1, 0), (1, 1)][k]
        show = [[f(grid[i][j]) for j in range(2)] for i in range(2)]
        show[r][c] = "?"
        x, y = lab[r][c]
        ans = x * y
        if x % 10 == 0 and y % 10 == 0:
            wrong = [ans // 10, ans * 10, x + y]
        elif x % 10 == 0 or y % 10 == 0:
            wrong = [(x // 10 if x % 10 == 0 else x) * (y // 10 if y % 10 == 0 else y), ans * 10, x + y]
        else:
            wrong = [x + y, ans * 10, int("%d%d" % (x, y))]
        e = "The ? part is %d wide and %d tall: %d × %d = %s." % (x, y, x, y, f(ans))
        if x % 10 == 0 and y % 10 == 0:
            e += " Think: %s × %s = %d hundreds." % (unit_word(x // 10, 1), unit_word(y // 10, 1), ans // 100)
        e += " All four parts add to %d × %d = %s." % (a, b, f(a * b))
        its.append(mcq(fig(area_2d(a, b, show)) + "What number goes in the part marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # D: which partial products
    for _ in range(3):
        a, b = pick_2x2(rnd, seen)
        ta, oa = parts(a)
        tb, ob = parts(b)
        pr = [ta * tb, oa * tb, ta * ob, oa * ob]
        right = " + ".join(f(p) for p in pr)
        wrong = [" + ".join(f(p) for p in [ta * tb, oa * ob]),
                 " + ".join(f(p) for p in [ta * tb // 100, oa * tb // 10, ta * ob // 10, oa * ob]),
                 " + ".join(f(p) for p in [ta * tb, oa * tb, oa * ob])]
        e = "Each part of one number multiplies each part of the other, so there are 4 parts. " + pp_2d(a, b)
        its.append(mcq("Which parts add up to %d × %d?" % (a, b), right, wrong, e, rnd))
    # E: partitioning number sentence
    for _ in range(3):
        a, d = pick_2x1(rnd, seen, 2)
        t, o = a // 10 * 10, a % 10
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d" % (t, d, o), "%d × %d + %d × %d" % (t // 10, d, o, d), "%d × %d + %d" % (o, d, t)]
        e = ("Partition %d into %d + %d. Both parts must be multiplied by %d: %d × %d + %d × %d = %d + %d = %d."
             % (a, t, o, d, t, d, o, d, t * d, o * d, a * d))
        its.append(mcq("Which is equal to %d × %d?" % (a, d), right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area model and partitioning", "items": its}


# ------------------------------------------------------------ set 3: short multiplication
def pick_short(rnd, seen, n, zero=None):
    while True:
        a, d = rnd.randint(10 ** (n - 1) + 1, 10 ** n - 1), rnd.randint(3, 9)
        ds = digits(a)
        if (a, d) in seen:
            continue
        if zero is not None:
            if ds[zero] != 0 or 0 in ds[:zero] + ds[zero + 1:] or ds[zero - 1] * d < 10:
                continue
        elif 0 in ds or carries(a, d) < n - 1 or len(set(ds)) < n - 1:
            continue
        seen.add((a, d))
        return a, d


def short_item(a, d, rnd, col):
    q = (fig(short_svg(a, d)) + "Use short multiplication.") if col else "Calculate %s × %d." % (f(a), d)
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], steps_short(a, d), rnd)


def set_short(rnd, seen):
    its = []
    for i in range(6):
        a, d = pick_short(rnd, seen, 3)
        its.append(short_item(a, d, rnd, i % 2 == 0))
    for i in range(8):
        a, d = pick_short(rnd, seen, 4)
        its.append(short_item(a, d, rnd, i % 2 == 1))
    for z in (1, 2):
        a, d = pick_short(rnd, seen, 4, zero=z)
        c = carry_list(a, d)[z]
        wrong = [mult_row(a, d, "skip", z - 1), mult_row(a, d, "zero_d"), int(str(a).replace("0", "")) * d,
                 mult_row(a, d, "nocarry")]
        e = steps_short(a, d) + " 0 × %d = 0, but you still add the regrouped %d." % (d, c)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if z == 1 else "Calculate %s × %d." % (f(a), d)
        its.append(mcq(q, f(a * d), [f(v) for v in wrong], e, rnd))
    k = 0
    while k < 4:
        a, d = pick_short(rnd, seen, 4)
        ans = str(a * d)
        pos = 1 + k % 2 if k < 2 else 2 + k % 2
        ex = carry_list(a, d)
        if pos not in ex:
            continue
        right = int(ans[-1 - pos])
        x = digits(a)[pos]
        c = ex[pos]
        p = x * d + c
        cand = []
        for w in [mult_row(a, d, "skip", pos - 1), mult_row(a, d, "cfirst")]:
            ws = str(w)
            if len(ws) > pos:
                cand.append(int(ws[-1 - pos]))
        cand += [(x * d) % 10, p // 10 % 10, (x + c) * d % 10, c]
        wr = []
        for v in cand:
            if v != right and v not in wr:
                wr.append(v)
        if len(wr) < 3:
            continue
        show = list(ans)
        show[-1 - pos] = "?"
        last = pos == len(digits(a)) - 1
        e = ("%s column: %d × %d = %d, then add the regrouped %d: %d. Write %d%s. "
             % (cap(PLACE[pos]), x, d, x * d, c, p, p if last else p % 10,
                ", regroup %d" % (p // 10) if p >= 10 and not last else ""))
        if last:
            e += "The ? is the %s digit, %d. " % (PLACE[pos], right)
        e += "Full working: " + steps_short(a, d)
        its.append(mcq(fig(short_svg(a, d, "".join(show), ex)) + "What digit goes in the box marked ?",
                       str(right), [str(v) for v in wr], e, rnd, zero_ok=True))
        k += 1
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Short multiplication: 3- and 4-digit × 1-digit", "items": its}


# ------------------------------------------------------------ set 4: long multiplication and estimating
def pick(rnd, seen, na, bmax=99):
    while True:
        a = rnd.randint(10 ** (na - 1) + 1, 10 ** na - 1)
        bd = rnd.sample(range(2, 10), 2)
        b = bd[0] * 10 + bd[1]
        da = digits(a)
        if b > bmax or 0 in da or len(set(da)) < len(da) - 1 or (a, b) in seen:
            continue
        if any(carries(a, d) == 0 for d in digits(b)):
            continue
        seen.add((a, b))
        return a, b


def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Use long multiplication.") if col else "Calculate %s × %d." % (f(a), b)
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b, detail=1 if len(str(a)) > 2 else None), rnd)


def box_row_item(a, b, rnd):
    d, i, v = pp_rows(a, b)[1]
    q = fig(work_svg(a, b, box=1)) + "What number goes in the dashed box?"
    wrong = [a * d, mult_row(a, d, "nocarry") * 10, mult_row(a, d, "cfirst") * 10, v * 10]
    e = ("Row 2 multiplies by the tens digit, so it is %s × %d. Write the place-holder 0 first, then %s × %d: %s. "
         "The row is %s, not %s." % (f(a), d * 10, f(a), d, steps_1d(a, d), f(v), f(a * d)))
    e += " Check: %s = %s." % (" + ".join(f(x) for _, _, x in pp_rows(a, b)), f(a * b))
    return mcq(q, f(v), [f(x) for x in wrong], e, rnd)


def sum_box_item(a, b, rnd):
    pr = [v for d, i, v in pp_rows(a, b)]
    cs = add_carries(pr)
    wrong = [add_cols(pr, drop="all")] + [add_cols(pr, drop=k) for k in cs] + \
            [add_cols(pr, extra=k) for k in range(len(str(a * b))) if k not in cs] + [abs(pr[1] - pr[0])]
    q = fig(work_svg(a, b, box="sum")) + "What number goes in the dashed box?"
    e = ("Add the two rows with column addition, and add every regrouped digit: %s = %s."
         % (" + ".join(f(v) for v in pr), f(a * b)))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


WHAT = ["Forgot the place-holder zero", "Did not add a regrouped digit", "Added the two rows wrongly",
        "Multiplied by only one digit"]


def what_item(a, b, kind, rnd, P):
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    n, he, his = P.next()
    if kind == 0:
        got = v0 + a * d1
        rows = [("", str(a)), ("×", str(b)), ("", str(v0)), ("+", str(a * d1)), ("", str(got))]
        why = "Row 2 should be %s × %d = %s, but %s wrote %s. The place-holder 0 is missing." % (f(a), d1 * 10, f(v1), he, f(a * d1))
    else:
        r0 = mult_row(a, d0, "nocarry")
        got = r0 + v1
        rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(v1)), ("", str(got))]
        why = "Row 1 should be %s, not %s: %s. The regrouped digits were not added." % (f(v0), f(r0), steps_1d(a, d0))
    assert got != a * b
    why += " The correct answer is %s." % f(a * b)
    q = (fig(column_svg(rows, [1, 3], "%d times %d: working with a mistake" % (a, b))) +
         "%s got %s × %d = %s. What mistake did %s make?" % (n, f(a), b, f(got), he))
    ans = WHAT[kind]
    return mcq(q, ans, [w for w in WHAT if w != ans], why, rnd)


def round_to(n, p):
    return (n + p // 2) // p * p


def estimate_item(a, b, rnd):
    """Best estimate: round a to its leading place and b to the nearest 10."""
    pa = 10 ** (len(str(a)) - 1)
    ra, rb = round_to(a, pa), round_to(b, 10)
    down_a = a // pa * pa
    assert ra != down_a
    rb_bad = b // 10 * 10 if rb != b // 10 * 10 else rb + 10
    est = ra * rb
    right = "%s × %d = %s" % (f(ra), rb, f(est))
    wrong = ["%s × %d = %s" % (f(down_a), rb, f(down_a * rb)),
             "%s × %d = %s" % (f(ra), rb_bad, f(ra * rb_bad)),
             "%s × %d = %s" % (f(ra), rb, f(est // 10))]

    def how(n, r):
        return "round up" if r > n else "round down"
    e = ("Round %s to the nearest %s: %s (the next digit is %d, so round up). Round %d to the nearest ten: %d (%s). "
         "%s × %d = %s. The exact answer is %s, close to %s."
         % (f(a), "ten" if pa == 10 else "hundred", f(ra), digits(a)[-2], b, rb, how(b, rb),
            f(ra), rb, f(est), f(a * b), f(est)))
    return mcq("Which is the best estimate for %s × %d?" % (f(a), b), right, wrong, e, rnd)


def check_item(a, b, claim, rnd, P):
    n, he, his = P.next()
    pa = 10 ** (len(str(a)) - 1)
    ra, rb = round_to(a, pa), round_to(b, 10)
    est = ra * rb
    if claim == a * b:
        right = "Yes, it is close to %s" % f(est)
        wrong = ["No, it should be about %s" % f(est * 10), "No, it should be about %s" % f(est // 10),
                 "Yes, it is close to %s" % f(est // 10)]
        e = ("Estimate: %s × %d is about %s × %d = %s. %s is close to %s, so the answer is reasonable."
             % (f(a), b, f(ra), rb, f(est), f(claim), f(est)))
    else:
        right = "No, it should be about %s" % f(est)
        wrong = ["Yes, it is close to %s" % f(est), "Yes, it is close to %s" % f(est // 10),
                 "No, it should be about %s" % f(est * 10)]
        e = ("Estimate: %s × %d is about %s × %d = %s. %s is far from %s, so it cannot be right. "
             "%s forgot the place-holder 0 in row 2. The correct answer is %s."
             % (f(a), b, f(ra), rb, f(est), f(claim), f(est), n, f(a * b)))
    q = "%s works out %s × %d = %s. Estimate to check. Is %s answer reasonable?" % (n, f(a), b, f(claim), his)
    return mcq(q, right, wrong, e, rnd)


def set_long(rnd, seen, P):
    its = []
    for i in range(6):
        a, b = pick(rnd, seen, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for i in range(4):
        a, b = pick(rnd, seen, 3)
        its.append(compute_item(a, b, rnd, i % 2 == 1))
    for _ in range(3):
        a, b = pick(rnd, seen, 2 if _ < 2 else 3)
        its.append(box_row_item(a, b, rnd))
    while True:
        a, b = pick(rnd, seen, 3)
        if len(add_carries([v for d, i, v in pp_rows(a, b)])) >= 2:
            break
    its.append(sum_box_item(a, b, rnd))
    for kind in (0, 1):
        a, b = pick(rnd, seen, 2)
        its.append(what_item(a, b, kind, rnd, P))
    assert 386 * 42 == 16212 and 67 * 48 == 3216
    its.append(estimate_item(386, 42, rnd))
    its.append(estimate_item(67, 48, rnd))
    assert no_zero(286, 34) == 2002 and 286 * 34 == 9724
    its.append(check_item(286, 34, no_zero(286, 34), rnd, P))
    assert 712 * 29 == 20648
    its.append(check_item(712, 29, 712 * 29, rnd, P))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Long multiplication and checking by estimating", "items": its}


# ------------------------------------------------------------ set 5: word problems
def money(v):
    return "$" + f(v)


# (question, a, b, unit, lead). unit '$' = money, else 'x unit'. {n} {he} {his}.
STORIES = [
    ("A section of a footy stadium has 48 rows with 36 seats in each row. How many seats are in the section?",
     36, 48, "seats", "48 rows × 36 seats"),
    ("A school excursion to the zoo costs $35 for each student. 28 students in Year 5 are going. What is the total cost?",
     35, 28, "$", "28 students × $35"),
    ("{n}'s family drives 245 km every week to visit {his} grandparents' farm. How far do they drive in 12 weeks?",
     245, 12, "km", "12 weeks × 245 km"),
    ("A bakery makes 1365 sausage rolls every day. How many sausage rolls does it make in 6 days?",
     1365, 6, "sausage rolls", "6 days × 1365 sausage rolls"),
    ("The school canteen sells 136 meat pies each week. How many pies does it sell in 9 weeks?",
     136, 9, "pies", "9 weeks × 136 pies"),
    ("A box holds 144 pencils. The school office orders 23 boxes. How many pencils is that?",
     144, 23, "pencils", "23 boxes × 144 pencils"),
    ("At swimming training, {n} swims 36 laps of a 50 m pool. How far does {he} swim?",
     50, 36, "m", "36 laps × 50 m"),
    ("A cricket club buys 24 new cricket balls at $18 each. How much does it spend?",
     18, 24, "$", "24 balls × $18"),
    ("Each school bus seats 57 students. How many students can 14 buses carry?",
     57, 14, "students", "14 buses × 57 students"),
    ("A mango farm in Queensland packs 1235 trays in a week. Each tray holds 18 mangoes. How many mangoes is that?",
     1235, 18, "mangoes", "1235 trays × 18 mangoes"),
    ("The school library orders 165 new books at $14 each. What is the total cost?",
     165, 14, "$", "165 books × $14"),
    ("A delivery truck drives 386 km every week. How far does it drive in 7 weeks?",
     386, 7, "km", "7 weeks × 386 km"),
    ("The school hall is set up with 32 rows of chairs. Each row has 26 chairs. How many chairs are there?",
     26, 32, "chairs", "32 rows × 26 chairs"),
    ("A netball club buys 9 new netballs at $47 each. How much does it spend?",
     47, 9, "$", "9 netballs × $47"),
    ("For the athletics carnival, the school orders 35 boxes of water bottles. Each box holds 24 bottles. How many bottles is that?",
     24, 35, "bottles", "35 boxes × 24 bottles"),
]


def sfl(a, b):
    """'Smaller from larger' subtraction mistake (a > b): subtract the smaller digit from the larger in every column."""
    r, i = 0, 0
    while a or b:
        r += abs(a % 10 - b % 10) * 10 ** i
        a, b, i = a // 10, b // 10, i + 1
    return r


def set_story(rnd, P):
    its = []
    for t, a, b, unit, lead in STORIES:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his)
        fm = money if unit == "$" else (lambda v, u=unit: "%s %s" % (f(v), u))
        if b < 10:
            wrong = cands_1d(a, b)
            e = "Equal groups: %s, so multiply %s × %d. %s" % (lead, f(a), b, steps_short(a, b))
        else:
            wrong = cands(a, b, rnd)
            e = "Equal groups: %s, so multiply %s × %d. " % (lead, f(a), b) + steps(a, b)
        its.append(mcq(q, fm(a * b), [fm(v) for v in wrong], e, rnd))

    # "times as many"
    assert 6250 * 8 == 50000
    its.append(mcq("The town's footy ground holds 6250 people. The city stadium holds 8 times as many. "
                   "How many people does the stadium hold?", "50 000 people",
                   ["5000 people", "6258 people", "500 000 people"],
                   "8 times as many means multiply: 6250 × 8. Think 6000 × 8 = 48 000 and 250 × 8 = 2000. "
                   "48 000 + 2000 = 50 000 people.", rnd))
    # two-step excursion
    assert 28 * 14 + 28 * 9 == 644 and 28 * 14 == 392 and 28 * 9 == 252
    its.append(mcq("A Year 5 excursion costs $14 a student for entry and $9 a student for the bus. "
                   "28 students go. What is the total cost?", "$644",
                   ["$392", "$252", "$51"],
                   "Each student pays $14 + $9 = $23. 28 × $23: row 1: 28 × 3 = 84; row 2: 28 × 20 = 560. "
                   "84 + 560 = $644. (Or: entry 28 × $14 = $392, bus 28 × $9 = $252, total $644.)", rnd))
    # two-step empty seats
    assert 24 * 45 == 1080 and 1080 - 958 == 122
    its.append(mcq("A stand at the cricket ground has 24 rows of 45 seats. 958 people are sitting in the stand. "
                   "How many seats are empty?", "122 seats",
                   ["1080 seats", "2038 seats", "%d seats" % sfl(1080, 958)],
                   "Step 1: seats: 24 × 45 = 1080 (row 1: 24 × 5 = 120; row 2: 24 × 40 = 960; 120 + 960 = 1080). "
                   "Step 2: empty seats: 1080 − 958 = 122.", rnd))
    # estimate a cost
    assert 19 * 42 == 798
    its.append(mcq("Tickets to a show cost $42 each. The best estimate of the cost of 19 tickets is …", "about $800",
                   ["about $80", "about $8000", "about $1000"],
                   "Round 19 to 20 and $42 to $40. 20 × $40 = $800. The exact cost is 19 × $42 = $798, very close. "
                   "(Rounding 42 up to 50 gives $1000, which is too far off.)", rnd))
    # check a total by estimating
    n, he, his = P.next()
    assert 312 * 27 == 8424 and no_zero(312, 27) == 2808
    its.append(mcq("A school buys 27 tablets at $312 each. %s says the total is $2808. Is %s answer reasonable?" % (n, his),
                   "No, it should be about $9000",
                   ["Yes, it is close to $3000", "Yes, it is close to $900", "No, it should be about $90 000"],
                   "Estimate: $312 is about $300 and 27 is about 30. 30 × $300 = $9000. $2808 is far too small. "
                   "%s forgot the place-holder 0 in row 2. The correct total is 27 × $312 = $8424." % n, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems: seats, excursions, money and distance", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def row_regroups(a, d, shift):
    out, c = {}, 0
    for i, x in enumerate(digits(a)[:-1]):
        c = (x * d + c) // 10
        if c:
            out[i + 1 + shift] = c
    return out


def add_regroups(nums):
    out, c = {}, 0
    for i in range(max(len(str(n)) for n in nums) - 1):
        c = (sum(n // 10 ** i % 10 for n in nums) + c) // 10
        if c:
            out[i + 1] = c
    return out


def lesson_fig(a, b, label):
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    rows, notes = [], []

    def add(r, n):
        if r[0] == "ex" and not r[1]:
            return
        rows.append(r)
        notes.append(n)

    add(("", str(a)), "")
    add(("×", str(b)), "")
    add(("", str(v0), 0), "%s × %d" % (f(a), d0))
    add(("ex", row_regroups(a, d0, 0)), "regrouped")
    add(("+", str(v1), 1), "%s × %d" % (f(a), d1 * 10))
    add(("ex", row_regroups(a, d1, 1)), "regrouped")
    rule2 = len(rows) - 1
    add(("", str(a * b)), "add the rows")
    add(("ex", add_regroups([v0, v1])), "regrouped when adding")
    return column_svg(rows, [1, rule2], label, notes=notes, big=True)


def body_html():
    assert 34 * 26 == 884 and 4736 * 6 == 28416 and 38 * 24 == 912 and 243 * 36 == 8748
    return (
        "<h2>Mental strategies: use facts you know</h2>"
        "<p>Many big multiplications are a multiplication fact in disguise. 60 is 6 tens, so 60 × 7 is 6 × 7 = 42 tens = <b>420</b>.</p>"
        "<p>Other quick strategies: <b>change the order</b> (25 × 7 × 4 = 25 × 4 × 7 = 100 × 7 = 700), "
        "<b>double and halve</b> (16 × 25 = 8 × 50 = 400), <b>× 5 is × 10, then halve</b> (46 × 5 = 460 ÷ 2 = 230) "
        "and <b>use a near number</b> (99 × 6 = 600 − 6 = 594).</p>"
        "<h2>The area model: partition by place value</h2>"
        "<p>Split each number into tens and ones. Draw a rectangle with one part for each pair. "
        "Multiply each part, then add all the parts.</p>"
        "<figure class='sn-fig'>" + area_2d(34, 26, [["600", "80"], ["180", "24"]]) +
        "<figcaption>34 × 26: 30 × 20 = 600, 4 × 20 = 80, 30 × 6 = 180, 4 × 6 = 24. "
        "600 + 80 + 180 + 24 = 884.</figcaption></figure>"
        "<h2>Short multiplication: up to 4 digits × 1 digit</h2>"
        "<p>Line up the ones. Start with the ones column. When a product is 10 or more, write the ones digit and "
        "<b>regroup</b> the tens into the next column as a small digit. <b>Multiply first, then add</b> the regrouped digit.</p>"
        "<figure class='sn-fig'>" + short_svg(4736, 6, "28416", carry_list(4736, 6), "4736 times 6 as short multiplication") +
        "<figcaption>4736 × 6: 6 × 6 = 36, write 6, regroup 3. 3 × 6 + 3 = 21, write 1, regroup 2. "
        "7 × 6 + 2 = 44, write 4, regroup 4. 4 × 6 + 4 = 28. Answer: 28 416.</figcaption></figure>"
        "<h2>Long multiplication: × a 2-digit number</h2>"
        "<p>Make <b>one row for each digit</b>. Row 1 multiplies by the ones digit. Row 2 multiplies by the tens digit, "
        "so it starts with a <b>place-holder zero</b> (green). Then add the two rows.</p>"
        "<figure class='sn-fig'>" + lesson_fig(38, 24, "38 times 24 as long multiplication") +
        "<figcaption>38 × 24: row 1 is 38 × 4 = 152. Row 2 is 38 × 20: write 0, then 38 × 2 = 76, so 760. "
        "152 + 760 = 912.</figcaption></figure>" +
        ex("3-digit × 2-digit", "243 × 36 = ?",
           "Row 1: 243 × 6 = 1458. Row 2: write 0, then 243 × 3 = 729, so 7290. Add: 1458 + 7290 = 8748.",
           "8748") +
        "<h2>Check that your answer is reasonable</h2>"
        "<p>Round each number, then multiply. 243 × 36 is about 200 × 40 = 8000, so 8748 makes sense. "
        "An answer like 2187 (no place-holder zero) is far too small.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Losing or adding a zero (60 × 7 = 42 or 4200)", "60 is 6 tens: 6 × 7 = 42 tens = 420"],
            ["No place-holder zero (38 × 24 = 152 + 76 = 228)", "Row 2 is × 20, so write 0 first: 760"],
            ["Not adding a regrouped digit (38 × 4 = 122)", "Write it small and add it: 3 × 4 + 3 = 15, so 152"],
            ["Adding the regrouped digit first", "Multiply first, then add: 3 × 4 + 3 = 15, not (3 + 3) × 4"],
            ["Only two parts in the area model (34 × 26 = 600 + 24)", "There are four parts: 600 + 80 + 180 + 24 = 884"],
            ["Estimating with the wrong rounding (386 → 300)", "386 is closer to 400: 400 × 40 = 16 000"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Year 5 students learn in Australia?",
     "a": "Under the Australian Curriculum (AC9M5N06) they multiply larger numbers by one- or two-digit numbers, choose efficient strategies such as the area model or long multiplication, and check that answers are reasonable by estimating."},
    {"q": "How do you teach long multiplication in Year 5?",
     "a": "Start with 2-digit × 2-digit. Multiply by the ones digit for row 1, write a place-holder zero and multiply by the tens digit for row 2, then add the rows: 38 × 24 = 152 + 760 = 912."},
    {"q": "What is the area model for multiplication?",
     "a": "It partitions both numbers by place value and draws a rectangle with a part for each pair. For 34 × 26 the parts are 600, 80, 180 and 24, which add to 884."},
    {"q": "Is multiplication on the Year 5 NAPLAN numeracy test?",
     "a": "Yes. NAPLAN numeracy is based on the Australian Curriculum, so Year 5 students meet multiplication questions and word problems. Practising written methods and estimating helps them work accurately."},
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


SPACED = re.compile(r"(?<![\d.])(\d{1,3}) (\d{3})(?![\d])")


def nb_text(t):
    """Write a no-break space in numbers typed with a plain space (27 000 -> 27&nbsp;000)."""
    parts_ = re.split(r"(<[^>]*>)", t)
    return "".join(x if x.startswith("<") else SPACED.sub(lambda m: m.group(1) + NB + m.group(2), x) for x in parts_)


def nbsp(obj):
    for s in obj:
        s["title"] = nb_text(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = nb_text(it["q"]), nb_text(it["e"])
            it["c"] = [nb_text(c) for c in it["c"]]


def gen():
    rnd = random.Random(5806)
    P = People(rnd)
    seen, seen2 = set(), set()
    sets = [set_mental(rnd), set_area(rnd, seen2), set_short(rnd, seen), set_long(rnd, seen, P), set_story(rnd, P)]
    balance(sets, rnd)
    nbsp(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["e"]
            assert k not in keys, it["q"]
            keys.add(k)
    return {
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "multiplication", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication",
        "seo_title": "Year 5 Multiplication Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Multiplication",
        "domain": "Number",
        "standard_code": "AC9M5N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Solve problems involving multiplication of larger numbers by one- or two-digit numbers, choosing efficient calculation strategies and using digital tools where appropriate; check the reasonableness of answers",
        "meta_desc": "Free Year 5 maths worksheets on multiplication, aligned to the Australian Curriculum (AC9M5N06): mental strategies, the area model, short multiplication, long multiplication with a place-holder zero, estimating to check, and word problems. 100 questions with an answer key, great for NAPLAN practice.",
        "key_big": "Multiply one digit at a time. For a 2-digit number, make two rows and start row 2 with a place-holder zero.",
        "key_sub": "38 × 24 = 38 × 4 + 38 × 20 = 152 + 760 = 912. Then estimate to check: 40 × 20 = 800, so 912 is reasonable.",
        "body_html": nb_text(body_html()), "faq": [{"q": nb_text(x["q"]), "a": nb_text(x["a"])} for x in FAQ], "sets": sets,
    }


def mark_large(u, pattern):
    """Tag column and area pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "([0-9]+ times [0-9]+|area model with (3|4) parts)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
