# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Multiplying two-digit numbers (Ontario Mathematics Curriculum 2020, B2.6)
Multiplying by multiples of 10 (20 × 30), the area model (23 × 14), partial products,
the standard algorithm (and how it connects to the area model), estimating and word problems.
Two-digit × two-digit whole numbers only.
  python3 tools/gen_caon_math_g5_multiplication.py
Every product and every wrong answer is computed here (wrong answers = real student mistakes).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
Ontario number style: 4-digit numbers have no separator (4536); 5 or more digits use a
no-break space (28 200). Column layouts are drawn without separators, as students write them.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4536, 28200 -> 28 200 (no-break space)."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1 if c.startswith(("Yes", "No")) else 0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead == "0":
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


def parts(n):
    """Tens and ones: 23 -> [20, 3]."""
    return [n // 10 * 10, n % 10]


def svg_wrap(w, h, body, label, family=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def tw(t, fs):
    """Approximate text width in px (Arial bold)."""
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
        base = {1: 62, 2: 100}.get(len(str(t)), 130)
        ws.append(max(need, base))
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 20)
    hs = [70, 46]
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


def area_2d(a, b, show=None):
    """a across the top (columns), b down the side (rows: tens row first)."""
    ta, oa = parts(a)
    tb, ob = parts(b)
    cells = show or [["", ""], ["", ""]]
    return area_svg([str(ta), str(oa)], [str(tb), str(ob)], cells, "area model with 4 parts: %d × %d" % (a, b))


def area_cells(a, b):
    ta, oa = parts(a)
    tb, ob = parts(b)
    return [[ta * tb, oa * tb], [ta * ob, oa * ob]]


# ------------------------------------------------------------ column figure
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


def column_svg(rows, rules, label, notes=None, big=False):
    """Multiplication in columns, ones lined up on the right.
    rows = list of (sign, text) or (sign, text, nz): nz = number of placeholder zeros at the end (drawn green).
    sign 'ex' = a row of small regrouped digits: text is a dict {place: digit}.
    text '[?]' = a red dashed box across the row (w = digits wide, default the widest row)."""
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
    return column_svg([("", str(a)), ("×", str(b))], [1], "%d times %d written in columns" % (a, b))


def pp_rows(a, b):
    """The rows of the standard algorithm, ones row first: (digit, place, value)."""
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
    return column_svg(rows, rules, "%d times %d with the standard algorithm" % (a, b))


def pp4_list(a, b):
    """The four partial products, smallest first: (text, value)."""
    ta, oa = parts(a)
    tb, ob = parts(b)
    return [("%d × %d" % (oa, ob), oa * ob), ("%d × %d" % (ta, ob), ta * ob),
            ("%d × %d" % (oa, tb), oa * tb), ("%d × %d" % (ta, tb), ta * tb)]


def pp4_svg(a, b, box=None):
    """Partial products in columns: four rows with notes, then the total. box = row index or 'sum'."""
    pl = pp4_list(a, b)
    rows = [("", str(a)), ("×", str(b))]
    notes = ["", ""]
    for k, (t, v) in enumerate(pl):
        sg = "+" if k == 3 else ""
        rows.append((sg, "[?]") if box == k else (sg, str(v)))
        notes.append(t)
    rows.append(("", "[?]") if box == "sum" else ("", str(a * b)))
    notes.append("")
    return column_svg(rows, [1, 5], "%d times %d with partial products" % (a, b), notes=notes)


# ------------------------------------------------------------ explanations
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
    return "%s × %s = %s (write the placeholder 0, then %s × %d = %s)" % (f(a), f(d * 10 ** i), f(v), f(a), d, f(a * d))


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


def pp_2d(a, b):
    ta, oa = parts(a)
    tb, ob = parts(b)
    pr = [ta * tb, oa * tb, ta * ob, oa * ob]
    return ("Split %d = %d + %d and %d = %d + %d. %d × %d = %s, %d × %d = %s, %d × %d = %s, %d × %d = %s. "
            "Add: %s = %s." % (a, ta, oa, b, tb, ob, ta, tb, f(pr[0]), oa, tb, f(pr[1]), ta, ob, f(pr[2]), oa, ob, f(pr[3]),
                               " + ".join(f(p) for p in pr), f(a * b)))


# ------------------------------------------------------------ typical mistakes
def mult_row(a, d, mode="ok", k=None):
    """a × d (one digit), done with a typical mistake.
    nocarry: forget every regrouped digit. skip: forget the one made in place k.
    cfirst: add the regrouped digit BEFORE multiplying."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        if mode == "cfirst":
            p = (x + c) * d
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


def total_with(a, b, mode, only=None, k=None):
    t = 0
    for j, (d, i, v) in enumerate(pp_rows(a, b)):
        if only is None or only == j:
            t += mult_row(a, d, mode, k) * 10 ** i
        else:
            t += v
    return t


def no_zero(a, b):
    """No placeholder zero: the tens row is 10 times too small."""
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
    """tens × tens written with one zero: 20 × 30 = 60."""
    return a * b - (a // 10) * (b // 10) * 90


def cands(a, b, rnd):
    pr = pp_rows(a, b)
    out = [no_zero(a, b)]
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"), add_cols([v for d, i, v in pr], drop="all"),
            two_pp(a, b)]
    more += [total_with(a, b, "nocarry", only=j) for j in range(len(pr))]
    rnd.shuffle(more)
    return out + more + [a * (b % 10), total_with(a, b, "skip", k=0), skip_pp(a, b), one_zero(a, b)]


def pick(rnd, seen, lo=13, hi=89, blo=13, bhi=69):
    """2-digit × 2-digit, no 0 or 1 ones digits, both rows of the algorithm regroup."""
    while True:
        a, b = rnd.randint(lo, hi), rnd.randint(blo, bhi)
        if a % 10 < 2 or b % 10 < 2 or a // 10 == a % 10 or b // 10 == b % 10 or a == b:
            continue
        if (a, b) in seen or (b, a) in seen:
            continue
        if carries(a, b % 10) == 0 or carries(a, b // 10) == 0:
            continue
        seen.add((a, b))
        return a, b


# ------------------------------------------------------------ set 1: multiples of 10
def set_tens(rnd):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, f(ans), [f(w) for w in wrong], e, rnd))

    # tens × tens
    for x, y in [(2, 3), (4, 6), (3, 7), (5, 8), (6, 5), (9, 4), (8, 7)]:
        a, b, p = x * 10, y * 10, x * y
        ans = a * b
        wrong = [p * 10, p * 1000, a + b]
        e = ("%d is %d tens and %d is %d tens. %d × %d = %d, and tens × tens = hundreds, so %d × %d = %d hundreds = %s."
             % (a, x, b, y, x, y, p, a, b, p, f(ans)))
        if p % 10 == 0:
            e += " The 0 in %d is part of the fact, so the answer has three zeros." % p
        else:
            e += " There are two zeros, one from each number. %d × %d is not %d." % (a, b, p * 10)
        add("What is %d × %d?" % (a, b), ans, wrong, e)
    # use a fact
    for x, y in [(8, 9), (7, 6)]:
        a, b, p = x * 10, y * 10, x * y
        add("%d × %d = %d. What is %d × %d?" % (x, y, p, a, b), a * b, [p * 10, p * 1000, a + b],
            "%d × %d is %d tens × %d tens = %d hundreds. Put back two zeros: %d × %d = %s." % (a, b, x, y, p, a, b, f(a * b)))
    # 2-digit × a multiple of 10
    for a, m, flip in [(23, 30, False), (47, 60, False), (36, 40, True), (58, 20, False), (74, 30, True),
                       (29, 50, False), (65, 80, True)]:
        d = m // 10
        assert carries(a, d) >= 1 or a == 23
        ans = a * m
        wrong = [a * d, a * d * 100, mult_row(a, d, "nocarry") * 10, a // 10 * 10 * m + a % 10]
        x, y = (m, a) if flip else (a, m)
        e = ("%d = %d × 10, so %d × %d = %d × %d × 10. %d × %d: %s. So %d × %d = %d, then write one 0: %s."
             % (m, d, x, y, a, d, a, d, steps_1d(a, d), a, d, a * d, f(ans)))
        q = "What is %d × %d?" % (x, y)
        add(q, ans, wrong, e)
    # which is equal
    for x, y in [(3, 4), (5, 6)]:
        a, b = x * 10, y * 10
        right = "%d × %d × 100" % (x, y)
        wrong = ["%d × %d × 10" % (x, y), "%d × %d + 100" % (x, y), "%d × %d × 1000" % (x, y)]
        its.append(mcq("Which is equal to %d × %d?" % (a, b), right, wrong,
                       "%d = %d × 10 and %d = %d × 10. So %d × %d = %d × %d × 10 × 10 = %d × %d × 100 = %s."
                       % (a, x, b, y, a, b, x, y, x, y, f(a * b)), rnd))
    # missing factor
    for known, miss in [(30, 80), (40, 70)]:
        tot = known * miss
        add("What number goes in the box? □ × %d = %s" % (known, f(tot)), miss, [miss // 10, miss * 10, tot - known],
            "Think: %d × %d = %d, so %d × %d = %s. The missing number is %d." % (miss // 10, known // 10, tot // 100,
                                                                                  miss, known, f(tot), miss))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Multiply by multiples of 10 (20 × 30)", "items": its}


# ------------------------------------------------------------ set 2: area model
def set_area(rnd, seen):
    its = []
    # A: blank area model -> product (23 × 14 first)
    pairs = [(23, 14)] + [pick(rnd, seen, hi=79) for _ in range(5)]
    seen.add((23, 14))
    for a, b in pairs:
        wrong = [two_pp(a, b), skip_pp(a, b), one_zero(a, b), no_zero(a, b), a + b]
        its.append(mcq(fig(area_2d(a, b)) + "Use the area model to find %d × %d." % (a, b), f(a * b),
                       [f(v) for v in wrong], pp_2d(a, b), rnd))
    # B: the missing part
    for k in range(5):
        a, b = pick(rnd, seen, hi=79)
        grid = area_cells(a, b)
        ta, oa = parts(a)
        tb, ob = parts(b)
        lab = [[(ta, tb), (oa, tb)], [(ta, ob), (oa, ob)]]
        r, c = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 0)][k]
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
            e += " Think: %d tens × %d tens = %d hundreds." % (x // 10, y // 10, ans // 100)
        e += " All four parts add up to %d × %d = %s." % (a, b, f(a * b))
        its.append(mcq(fig(area_2d(a, b, show)) + "What number goes in the part marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # C: one row of the area model
    for _ in range(3):
        a, b = pick(rnd, seen, hi=79)
        ta, oa = parts(a)
        tb, ob = parts(b)
        ans = a * tb
        wrong = [a * (tb // 10), ta * tb, ta * tb + oa, a * ob]
        e = ("The top row is %d tall: %d × %d = %s and %d × %d = %s. %s + %s = %s. That is %d × %d."
             % (tb, ta, tb, f(ta * tb), oa, tb, f(oa * tb), f(ta * tb), f(oa * tb), f(ans), a, tb))
        its.append(mcq(fig(area_2d(a, b)) + "What is the total of the top row of this area model?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # D: all parts filled in -> add
    k = 0
    while k < 4:
        a, b = pick(rnd, seen, hi=89)
        g = area_cells(a, b)
        pr = [g[0][0], g[0][1], g[1][0], g[1][1]]
        if len(add_carries(pr)) < 1:
            continue
        show = [[f(v) for v in row] for row in g]
        wrong = [add_cols(pr, drop="all"), pr[0] + pr[3], a * b - pr[1], a * b - pr[2]]
        e = "Add all four parts: %s = %s. So %d × %d = %s." % (" + ".join(f(p) for p in pr), f(a * b), a, b, f(a * b))
        its.append(mcq(fig(area_2d(a, b, show)) + "The area model shows %d × %d. What is the product?" % (a, b),
                       f(a * b), [f(v) for v in wrong], e, rnd))
        k += 1
    # E: which expression
    for _ in range(2):
        a, b = pick(rnd, seen, hi=89)
        ta, oa = parts(a)
        tb, ob = parts(b)
        right = "%d × %d + %d × %d" % (ta, b, oa, b)
        wrong = ["%d × %d + %d" % (ta, b, oa), "%d × %d + %d × %d" % (ta, tb, oa, ob), "%d × %d + %d × %d" % (ta // 10, b, oa, b)]
        e = ("Split %d into %d + %d. Both parts must be multiplied by all of %d: %d × %d + %d × %d = %s + %s = %s."
             % (a, ta, oa, b, ta, b, oa, b, f(ta * b), f(oa * b), f(a * b)))
        its.append(mcq("Which is equal to %d × %d?" % (a, b), right, wrong, e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Area model (23 × 14)", "items": its}


# ------------------------------------------------------------ set 3: partial products
def set_partial(rnd, seen):
    its = []
    # A: a missing partial product in the column layout
    for k in range(6):
        a, b = pick(rnd, seen)
        j = [3, 1, 2, 3, 2, 1][k]
        t, v = pp4_list(a, b)[j]
        x, y = [int(z) for z in t.split(" × ")]
        if x % 10 == 0 and y % 10 == 0:
            wrong = [v // 10, v * 10, x + y]
            e = "%s is %d tens × %d tens = %d hundreds = %s." % (t, x // 10, y // 10, v // 100, f(v))
        else:
            big, small = (x, y) if x % 10 == 0 else (y, x)
            wrong = [big // 10 * small, v * 10, x + y]
            e = "%s: %d × %d = %d, and %d is %s, so %s = %s." % (
                t, big // 10, small, big // 10 * small, big, "1 ten" if big == 10 else "%d tens" % (big // 10), t, f(v))
        e += " The four partial products add up to %d × %d = %s." % (a, b, f(a * b))
        its.append(mcq(fig(pp4_svg(a, b, box=j)) + "What number goes in the dashed box?", f(v), [f(w) for w in wrong], e, rnd))
    # B: compute with partial products
    for k in range(5):
        a, b = pick(rnd, seen)
        ta, oa = parts(a)
        tb, ob = parts(b)
        if k < 2:
            q = "Find %d × %d by adding the partial products: %d × %d + %d × %d + %d × %d + %d × %d" % (
                a, b, ta, tb, oa, tb, ta, ob, oa, ob)
        else:
            q = "Use partial products to find %d × %d." % (a, b)
        wrong = [two_pp(a, b), one_zero(a, b), skip_pp(a, b), no_zero(a, b)]
        its.append(mcq(q, f(a * b), [f(v) for v in wrong], pp_2d(a, b), rnd))
    # C: total of the four partial products
    k = 0
    while k < 2:
        a, b = pick(rnd, seen)
        pr = [v for t, v in pp4_list(a, b)]
        cs = add_carries(pr)
        if len(cs) < 2:
            continue
        wrong = [add_cols(pr, drop="all")] + [add_cols(pr, drop=c) for c in cs] + [a * b - pr[2]]
        e = "Add the four partial products, lining up the ones: %s = %s." % (" + ".join(f(v) for v in pr), f(a * b))
        its.append(mcq(fig(pp4_svg(a, b, box="sum")) + "What number goes in the dashed box?", f(a * b),
                       [f(v) for v in wrong], e, rnd))
        k += 1
    # D: which parts
    for _ in range(4):
        a, b = pick(rnd, seen)
        ta, oa = parts(a)
        tb, ob = parts(b)
        pr = [ta * tb, oa * tb, ta * ob, oa * ob]
        right = " + ".join(f(p) for p in pr)
        wrong = [" + ".join(f(p) for p in [ta * tb, oa * ob]),
                 " + ".join(f(p) for p in [ta * tb // 10, oa * tb, ta * ob, oa * ob]),
                 " + ".join(f(p) for p in [ta * tb, oa * tb, oa * ob])]
        e = "Each part of one number multiplies each part of the other, so there are 4 partial products. " + pp_2d(a, b)
        its.append(mcq("Which partial products add up to %d × %d?" % (a, b), right, wrong, e, rnd))
    # E: one number times the tens
    used_e = set()
    for _ in range(3):
        while True:
            a, b = pick(rnd, seen)
            tb, ob = parts(b)
            if (a, tb) not in used_e:
                break
        used_e.add((a, tb))
        d = tb // 10
        v = a * tb
        wrong = [a * d, a * tb * 10, mult_row(a, d, "nocarry") * 10, a // 10 * 10 * tb]
        e = ("%d × %d = %d × %d × 10. %d × %d = %d, then write one 0: %s. "
             "Then %d × %d = %s + %s = %s." % (a, tb, a, d, a, d, a * d, f(v), a, b, f(a * ob), f(v), f(a * b)))
        its.append(mcq("%d × %d = %d × %d + %d × %d. What is %d × %d?" % (a, b, a, ob, a, tb, a, tb),
                       f(v), [f(w) for w in wrong], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Partial products", "items": its}


# ------------------------------------------------------------ set 4: standard algorithm
def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Use the standard algorithm.") if col else "Calculate %d × %d." % (a, b)
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b, detail=1), rnd)


def box_row_item(a, b, k, rnd):
    d, i, v = pp_rows(a, b)[k]
    q = fig(work_svg(a, b, box=k)) + "What number goes in the dashed box?"
    if k == 1:
        wrong = [a * d, mult_row(a, d, "nocarry") * 10, mult_row(a, d, "cfirst") * 10, v * 10]
        e = ("Row 2 multiplies by the tens digit, so it is %d × %d. Write the placeholder 0 first, then %d × %d: %s. "
             "The row is %s, not %s." % (a, d * 10, a, d, steps_1d(a, d), f(v), f(a * d)))
    else:
        wrong = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), v * 10, a + d]
        e = "Row 1 is %d × %d: %s. The row is %s." % (a, d, steps_1d(a, d), f(v))
    e += " Check: %s = %s." % (" + ".join(f(x) for _, _, x in pp_rows(a, b)), f(a * b))
    return mcq(q, f(v), [f(x) for x in wrong], e, rnd)


def sum_box_item(a, b, rnd):
    pr = [v for d, i, v in pp_rows(a, b)]
    cs = add_carries(pr)
    wrong = [add_cols(pr, drop="all")] + [add_cols(pr, drop=k) for k in cs] + \
            [add_cols(pr, extra=k) for k in range(len(str(a * b))) if k not in cs] + [abs(pr[1] - pr[0])]
    q = fig(work_svg(a, b, box="sum")) + "What number goes in the dashed box?"
    e = ("Add the two rows, lining up the ones, and add every regrouped digit: %s = %s."
         % (" + ".join(f(v) for v in pr), f(a * b)))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


WHAT = ["Forgot the zero in the tens row", "Did not add a regrouped digit", "Added the two rows wrongly",
        "Multiplied by only one digit"]


def what_item(a, b, kind, rnd, P):
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    n, he, his = P.next()
    if kind == 0:
        got = v0 + a * d1
        rows = [("", str(a)), ("×", str(b)), ("", str(v0)), ("+", str(a * d1)), ("", str(got))]
        why = "Row 2 should be %d × %d = %s, but %s wrote %s. The placeholder 0 is missing." % (a, d1 * 10, f(v1), he, f(a * d1))
    else:
        r0 = mult_row(a, d0, "nocarry")
        got = r0 + v1
        rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(v1)), ("", str(got))]
        why = "Row 1 should be %s, not %s: %s. The regrouped digit was not added." % (f(v0), f(r0), steps_1d(a, d0))
    assert got != a * b
    why += " The correct answer is %s." % f(a * b)
    q = (fig(column_svg(rows, [1, 3], "%d times %d: work with a mistake" % (a, b))) +
         "%s got %d × %d = %s. What mistake did %s make?" % (n, a, b, f(got), he))
    ans = WHAT[kind]
    return mcq(q, ans, [w for w in WHAT if w != ans], why, rnd)


def connect_item(a, b, k, rnd):
    """Which parts of the area model make row k of the algorithm?"""
    ta, oa = parts(a)
    tb, ob = parts(b)
    d, i, v = pp_rows(a, b)[k]
    m = tb if k == 1 else ob
    other = ob if k == 1 else tb
    right = "%d × %d + %d × %d" % (ta, m, oa, m)
    wrong = ["%d × %d + %d × %d" % (ta, other, oa, other), "%d × %d + %d × %d" % (ta, tb, oa, ob),
             "%d × %d + %d × %d" % (ta, ob, oa, tb)]
    q = (fig(work_svg(a, b)) +
         "In the standard algorithm for %d × %d, row %d is %s. Which parts of the area model make row %d?" % (a, b, k + 1, f(v), k + 1))
    e = ("Row %d is %d × %d. In the area model that is the %d row: %d × %d = %s and %d × %d = %s. %s + %s = %s."
         % (k + 1, a, m, m, ta, m, f(ta * m), oa, m, f(oa * m), f(ta * m), f(oa * m), f(v)))
    return mcq(q, right, wrong, e, rnd)


def set_algorithm(rnd, seen, P):
    its = []
    for i in range(9):
        a, b = pick(rnd, seen)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(2):
        a, b = pick(rnd, seen)
        its.append(box_row_item(a, b, 0, rnd))
    while True:
        a, b = pick(rnd, seen)
        if len(add_carries([v for d, i, v in pp_rows(a, b)])) >= 2:
            break
    its.append(sum_box_item(a, b, rnd))
    for kind in (0, 1):
        a, b = pick(rnd, seen)
        its.append(what_item(a, b, kind, rnd, P))
    for k in (1, 0):
        a, b = pick(rnd, seen)
        its.append(connect_item(a, b, k, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Standard algorithm", "items": its}


# ------------------------------------------------------------ set 5: estimate and word problems
def money(v):
    return "$" + f(v)


def round10(n):
    return (n + 5) // 10 * 10


def estimate_item(a, b, rnd):
    ra, rb = round10(a), round10(b)
    da, db = a // 10 * 10, b // 10 * 10
    assert ra != da and rb != db
    est = ra * rb
    right = "%d × %d = %s" % (ra, rb, f(est))
    wrong = ["%d × %d = %s" % (da, db, f(da * db)),
             "%d × %d = %s" % (ra, db, f(ra * db)),
             "%d × %d = %s" % (ra, rb, f(est // 10))]
    e = ("Round each number to the nearest ten. %d has %d ones, so it rounds up to %d. %d has %d ones, so it rounds up to %d. "
         "%d × %d = %s (tens × tens = hundreds). The exact answer is %s, close to %s."
         % (a, a % 10, ra, b, b % 10, rb, ra, rb, f(est), f(a * b), f(est)))
    return mcq("Which is the best estimate for %d × %d?" % (a, b), right, wrong, e, rnd)


def check_item(a, b, claim, rnd, P):
    n, he, his = P.next()
    ra, rb = round10(a), round10(b)
    est = ra * rb
    if claim == a * b:
        right = "Yes, it is close to %s" % f(est)
        wrong = ["No, it should be about %s" % f(est * 10), "No, it should be about %s" % f(est // 10),
                 "Yes, it is close to %s" % f(est // 10)]
        e = ("Estimate: %d × %d is about %d × %d = %s. %s is close to %s, so the answer is reasonable."
             % (a, b, ra, rb, f(est), f(claim), f(est)))
    else:
        right = "No, it should be about %s" % f(est)
        wrong = ["Yes, it is close to %s" % f(est), "Yes, it is close to %s" % f(est // 10),
                 "No, it should be about %s" % f(est * 10)]
        e = ("Estimate: %d × %d is about %d × %d = %s. %s is far from %s, so it cannot be right. "
             "%s forgot the placeholder 0 in the tens row. The correct answer is %s."
             % (a, b, ra, rb, f(est), f(claim), f(est), n, f(a * b)))
    q = "%s works out %d × %d = %s. Estimate to check. Is %s answer reasonable?" % (n, a, b, f(claim), his)
    return mcq(q, right, wrong, e, rnd)


# (question, a, b, unit, lead). a × b. unit '$' = money, else 'x unit'. {n} {he} {his}.
STORIES = [
    ("The hockey arena in {n}'s town has 24 rows of seats. Each row has 38 seats. How many seats are there?",
     38, 24, "seats", "24 rows × 38 seats"),
    ("A sugar bush fills 46 boxes with bottles of maple syrup. Each box holds 12 bottles. How many bottles is that?",
     46, 12, "bottles", "46 boxes × 12 bottles"),
    ("A field trip to a pioneer village costs $18 for each student. 56 students go. What is the total cost?",
     18, 56, "$", "56 students × $18"),
    ("In the Terry Fox Run, each of the 27 students in {n}'s class raises $35. How much does the class raise?",
     35, 27, "$", "27 students × $35"),
    ("Each coach bus seats 56 people. The school books 14 coach buses for a trip to Ottawa. How many people can ride?",
     56, 14, "people", "14 buses × 56 people"),
    ("A food drive collects 37 boxes of soup. Each box holds 24 cans. How many cans is that?",
     24, 37, "cans", "37 boxes × 24 cans"),
    ("A community garden is 23 m long and 14 m wide. What is its area?",
     23, 14, "m²", "area = 23 m × 14 m"),
    ("A classroom floor is covered with square tiles in 32 rows of 28 tiles. How many tiles are there?",
     28, 32, "tiles", "32 rows × 28 tiles"),
    ("Winter mitts cost $16 a pair. The school buys 45 pairs for a winter clothing drive. How much does it spend?",
     16, 45, "$", "45 pairs × $16"),
    ("A bakery makes 48 butter tarts each hour. How many butter tarts does it make in 12 hours?",
     48, 12, "butter tarts", "12 hours × 48 tarts"),
    ("{n} practises piano for 35 minutes a day. How many minutes does {he} practise in 28 days?",
     35, 28, "minutes", "28 days × 35 minutes"),
    ("A farm stand packs 87 cartons of eggs. Each carton holds 12 eggs. How many eggs is that?",
     87, 12, "eggs", "87 cartons × 12 eggs"),
    ("A skating rink rents skates to 64 people each hour. How many people rent skates in 13 hours?",
     64, 13, "people", "13 hours × 64 people"),
]


def sfl(a, b):
    """'Smaller from larger' subtraction mistake: subtract the smaller digit from the larger in every column."""
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
        e = "%s, so multiply %d × %d. " % (cap(lead), a, b) + steps(a, b)
        its.append(mcq(q, fm(a * b), [fm(v) for v in cands(a, b, rnd)], e, rnd))
    # two-step: empty seats
    assert 32 * 45 == 1440 and 1440 - 1218 == 222
    its.append(mcq("A hockey arena has 32 rows of 45 seats. 1218 people are at the game. How many seats are empty?",
                   "222 seats", ["1440 seats", "2658 seats", "%d seats" % sfl(1440, 1218)],
                   "Step 1: seats: 45 × 32 (row 1: 45 × 2 = 90; row 2: 45 × 30 = 1350; 90 + 1350 = 1440). "
                   "Step 2: empty seats: 1440 − 1218 = 222.", rnd))
    # two-step: field trip
    assert 26 * 23 == 598 and 26 * 14 == 364 and 26 * 9 == 234
    its.append(mcq("A Grade 5 field trip costs $14 a student for entry and $9 a student for the bus. "
                   "26 students go. What is the total cost?", "$598",
                   ["$364", "$234", "$" + str(no_zero(26, 23))],
                   "Each student pays $14 + $9 = $23. 26 × $23: row 1: 26 × 3 = 78; row 2: 26 × 20 = 520. "
                   "78 + 520 = $598. (Or: entry 26 × $14 = $364, bus 26 × $9 = $234, total $598.)", rnd))
    # estimates
    assert 67 * 48 == 3216 and 86 * 29 == 2494
    its.append(estimate_item(67, 48, rnd))
    its.append(estimate_item(86, 29, rnd))
    assert 19 * 42 == 798
    its.append(mcq("Hockey tickets cost $42 each. What is the best estimate of the cost of 19 tickets?", "about $800",
                   ["about $80", "about $8000", "about $1000"],
                   "Round 19 to 20 and $42 to $40. 20 × $40 = $800. The exact cost is 19 × $42 = $798, very close. "
                   "(Rounding $42 up to $50 gives $1000, which is too far off.)", rnd))
    # checks
    assert no_zero(58, 34) == 406 and 58 * 34 == 1972
    its.append(check_item(58, 34, no_zero(58, 34), rnd, P))
    assert 72 * 39 == 2808
    its.append(check_item(72, 39, 72 * 39, rnd, P))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Estimate and word problems", "items": its}


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
    add(("", str(v0), 0), "%d × %d" % (a, d0))
    add(("ex", row_regroups(a, d0, 0)), "regrouped")
    add(("+", str(v1), 1), "%d × %d" % (a, d1 * 10))
    add(("ex", row_regroups(a, d1, 1)), "regrouped")
    rule2 = len(rows) - 1
    add(("", str(a * b)), "add the rows")
    add(("ex", add_regroups([v0, v1])), "regrouped when adding")
    return column_svg(rows, [1, rule2], label, notes=notes, big=True)


def body_html():
    assert 23 * 14 == 322 and 38 * 24 == 912 and 38 * 4 == 152 and 38 * 20 == 760
    return (
        "<h2>Multiply by multiples of 10</h2>"
        "<p>Use a fact you know. 20 is 2 tens and 30 is 3 tens. 2 × 3 = 6, and tens × tens = hundreds, "
        "so 20 × 30 = 6 hundreds = <b>600</b>. Two zeros, one from each number.</p>"
        "<p>For 23 × 30, find 23 × 3 = 69, then write one 0: 23 × 30 = <b>690</b>.</p>"
        "<h2>The area model</h2>"
        "<p>Split each number into tens and ones. Draw a rectangle with one part for each pair. "
        "Multiply each part, then add all four parts.</p>"
        "<figure class='sn-fig'>" + area_2d(23, 14, [["200", "30"], ["80", "12"]]) +
        "<figcaption>23 × 14: 20 × 10 = 200, 3 × 10 = 30, 20 × 4 = 80, 3 × 4 = 12. "
        "200 + 30 + 80 + 12 = 322.</figcaption></figure>"
        "<h2>Partial products</h2>"
        "<p>Write the same four parts in columns, lined up by place value, and add them.</p>"
        "<figure class='sn-fig'>" + pp4_svg(23, 14) +
        "<figcaption>12 + 80 + 30 + 200 = 322.</figcaption></figure>"
        "<h2>The standard algorithm</h2>"
        "<p>Make <b>one row for each digit</b> of the bottom number. Row 1 multiplies by the ones digit. "
        "Row 2 multiplies by the tens digit, so it starts with a <b>placeholder zero</b> (green). Then add the two rows.</p>"
        "<figure class='sn-fig'>" + lesson_fig(38, 24, "38 times 24 with the standard algorithm") +
        "<figcaption>38 × 24: row 1 is 38 × 4 = 152. Row 2 is 38 × 20: write 0, then 38 × 2 = 76, so 760. "
        "152 + 760 = 912.</figcaption></figure>"
        "<h2>How the two methods connect</h2>"
        "<p>Each row of the algorithm is one row of the area model. For 23 × 14, row 1 is 23 × 4 = 92 "
        "(the 4 row: 80 + 12). Row 2 is 23 × 10 = 230 (the 10 row: 200 + 30). 92 + 230 = 322, the same answer.</p>" +
        ex("Estimate to check", "Is 38 × 24 = 912 reasonable?",
           "Round to the nearest ten: 40 × 20 = 800. 912 is close to 800, so it makes sense. "
           "An answer like 228 or 9120 is far off.", "Yes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["20 × 30 = 60", "Tens × tens = hundreds: 20 × 30 = 600"],
            ["Forgetting the zero in the tens row (38 × 24 = 152 + 76 = 228)", "Row 2 is × 20, so write 0 first: 760"],
            ["Only two parts (23 × 14 = 200 + 12)", "There are four parts: 200 + 30 + 80 + 12 = 322"],
            ["Not adding a regrouped digit (38 × 4 = 122)", "Write it small and add it: 3 × 4 + 3 = 15, so 152"],
            ["Adding the regrouped digit first", "Multiply first, then add: 3 × 4 + 3 = 15, not (3 + 3) × 4"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Grade 5 students learn in the Ontario math curriculum?",
     "a": "Expectation B2.6 asks Grade 5 students to multiply two-digit whole numbers by two-digit whole numbers using the area model and algorithms, and to explain how the two methods connect."},
    {"q": "How do you teach 2-digit by 2-digit multiplication?",
     "a": "Start with the area model: split both numbers into tens and ones and add the four parts, so 23 × 14 = 200 + 30 + 80 + 12 = 322. Then show the standard algorithm, where each row is one row of the area model."},
    {"q": "Why do you put a zero in the second row?",
     "a": "The second row multiplies by the tens digit. In 38 × 24 the 2 means 2 tens, so the row is 38 × 20 = 760, not 38 × 2 = 76. The zero keeps the digits in the right places."},
    {"q": "What is 20 × 30?",
     "a": "20 × 30 = 600. 2 tens × 3 tens = 6 hundreds. A common mistake is 60, which forgets that tens × tens makes hundreds."},
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
    rnd = random.Random(45804)
    P = People(rnd)
    seen = set()
    sets = [set_tens(rnd), set_area(rnd, seen), set_partial(rnd, seen), set_algorithm(rnd, seen, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in keys, it["q"]
            keys.add(k)
    return {
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "multiplying-two-digit-numbers", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplying Two-Digit Numbers",
        "seo_title": "Grade 5 Multiplying Two-Digit Numbers Worksheets: Area Model and Standard Algorithm (Free, Ontario)",
        "short_title": "Multiplying two-digit numbers",
        "domain": "Number",
        "standard_code": "Grade 5: B2.6",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the multiplication of two-digit whole numbers by two-digit whole numbers using the area model and using algorithms, and make connections between the two methods",
        "meta_desc": "Free Grade 5 math worksheets on multiplying two-digit numbers for the Ontario curriculum: multiples of 10, the area model, partial products, the standard algorithm, estimating and word problems. 100 questions with an answer key.",
        "key_big": "Split both numbers into tens and ones and multiply every part. The area model and the standard algorithm give the same answer.",
        "key_sub": "23 × 14 = 200 + 30 + 80 + 12 = 322. In the algorithm, row 1 is 23 × 4 = 92 and row 2 is 23 × 10 = 230 (start it with a zero). 20 × 30 = 600, not 60.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
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
    mark_large(u, "([0-9]+ times [0-9]+|area model with 4 parts)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
