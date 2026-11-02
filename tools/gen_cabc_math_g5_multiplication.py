# -*- coding: utf-8 -*-
"""
CA-BC Grade 5 Math: Multiplication to three digits
(BC Mathematics Curriculum, Grade 5, Computational fluency:
 multiplication and division to three digits, including division with remainders;
 also multiplication and division facts to 100)
Facts warm-up, multiplying by 10, 100 and multiples of 10, area models (24 × 13),
the standard algorithm (2-digit × 2-digit and 3-digit × 1-digit) and BC word problems.
  python3 tools/gen_cabc_math_g5_multiplication.py
Every product and every wrong answer is computed here (wrong answers = real student mistakes).
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
BC number style: 4-digit numbers have no separator (4536); 5 or more digits use a
no-break space (34 500). Column layouts are drawn without separators, as students write them.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
NB = "\u00a0"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
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
    hs = [70, 46] if len(lefts) == 2 else [62]
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


def area_3x1(a, d, show=None):
    """3-digit × 1-digit area model: hundreds, tens and ones across the top, one row."""
    tops = [a // 100 * 100, a // 10 % 10 * 10, a % 10]
    cells = show or [["", "", ""]]
    return area_svg([str(t) for t in tops], [str(d)], cells, "area model with 3 parts: %d × %d" % (a, d))


def pp_3x1(a, d):
    h, t, o = a // 100 * 100, a // 10 % 10 * 10, a % 10
    return ("Split %d = %d + %d + %d. %d × %d = %s, %d × %d = %s, %d × %d = %s. Add: %s + %s + %s = %s."
            % (a, h, t, o, h, d, f(h * d), t, d, f(t * d), o, d, f(o * d), f(h * d), f(t * d), f(o * d), f(a * d)))


def concat_1d(a, d):
    """Writes every two-digit product in full, no regrouping: 236 × 4 -> 8|12|24."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def cands_1d(a, d):
    return [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", 0),
            mult_row(a, d, "skip", 1), concat_1d(a, d)]


def pick_3x1(rnd, seen):
    """3-digit × 1-digit, no zero digits, at least two regroupings."""
    while True:
        a, d = rnd.randint(124, 879), rnd.randint(3, 9)
        if "0" in str(a) or len(set(str(a))) < 3 or (a, d) in seen:
            continue
        if carries(a, d) < 2:
            continue
        seen.add((a, d))
        return a, d


# ------------------------------------------------------------ set 1: facts warm-up
def fact_e(x, y):
    p = x * y
    if x == 9 or y == 9:
        o = y if x == 9 else x
        return "%d × %d = %d. Check: 10 × %d = %d, take away one %d: %d − %d = %d." % (x, y, p, o, 10 * o, o, 10 * o, o, p)
    return "%d × %d = %d. Check with a fact you know: %d × %d = %d, and one more group of %d makes %d + %d = %d." % (
        x, y, p, x, y - 1, x * (y - 1), x, x * (y - 1), x, p)


def set_facts(rnd):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, f(ans), [f(w) for w in wrong], e, rnd))

    for x, y in [(6, 7), (7, 8), (8, 9), (6, 8), (7, 9), (4, 8), (9, 6), (8, 8), (7, 7), (3, 9)]:
        near = [x * (y - 1), x * (y + 1), (x + 1) * y, (x - 1) * y]
        rnd.shuffle(near)
        add("What is %d × %d?" % (x, y), x * y, near + [x + y], fact_e(x, y))
    for known, miss, left in [(7, 8, True), (6, 9, False), (9, 7, True), (8, 6, False), (4, 9, True)]:
        tot = known * miss
        q = ("What number goes in the box? □ × %d = %d" % (known, tot)) if left else \
            ("What number goes in the box? %d × □ = %d" % (known, tot))
        add(q, miss, [miss - 1, miss + 1, tot - known, known],
            "Which number times %d makes %d? %d × %d = %d, so the missing number is %d. (This is also %d ÷ %d = %d.)"
            % (known, tot, miss, known, tot, miss, tot, known, miss))
    for tot, dv in [(72, 8), (42, 6), (28, 4), (54, 9), (45, 5)]:
        q = tot // dv
        add("What is %d ÷ %d?" % (tot, dv), q, [q + 1, q - 1, dv, tot - dv],
            "Think of the multiplication fact: %d × %d = %d, so %d ÷ %d = %d." % (q, dv, tot, tot, dv, q))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Multiplication facts warm-up", "items": its}


# ------------------------------------------------------------ set 2: × 10, × 100, multiples of 10
def set_tens(rnd):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, f(ans), [f(w) for w in wrong], e, rnd))

    for n, flip in [(34, False), (58, True), (307, False), (260, False)]:
        ans = n * 10
        e = ("× 10 moves every digit one place to the left: %s ones become %s tens. Write a 0 in the ones place: %s × 10 = %s."
             % (f(n), f(n), f(n), f(ans)))
        if n % 10 == 0:
            e += " The 0 already in %d stays, so the answer has two zeros." % n
        add("What is %s?" % ("10 × %s" % f(n) if flip else "%s × 10" % f(n)), ans, [n, n * 100, n + 10], e)
    for n, flip in [(56, False), (23, True), (408, False), (715, False)]:
        ans = n * 100
        e = ("× 100 moves every digit two places to the left: %s ones become %s hundreds. Write two zeros: %s × 100 = %s."
             % (f(n), f(n), f(n), f(ans)))
        add("What is %s?" % ("100 × %s" % f(n) if flip else "%s × 100" % f(n)), ans, [n * 10, n * 1000, n + 100], e)
    for x, y in [(4, 6), (3, 7), (5, 8), (6, 5), (9, 4)]:
        a, b, p = x * 10, y * 10, x * y
        ans = a * b
        e = ("%d is %d tens and %d is %d tens. %d × %d = %d, and tens × tens = hundreds, so %d × %d = %d hundreds = %s."
             % (a, x, b, y, x, y, p, a, b, p, f(ans)))
        if p % 10 == 0:
            e += " The 0 in %d is part of the fact, so the answer has three zeros." % p
        else:
            e += " There are two zeros, one from each number. %d × %d is not %d." % (a, b, p * 10)
        add("What is %d × %d?" % (a, b), ans, [p * 10, p * 1000, a + b], e)
    for a, m, flip in [(47, 60, False), (36, 40, True), (58, 20, False), (74, 30, True)]:
        d = m // 10
        assert carries(a, d) >= 1
        ans = a * m
        wrong = [a * d, a * d * 100, mult_row(a, d, "nocarry") * 10, a // 10 * 10 * m + a % 10]
        x, y = (m, a) if flip else (a, m)
        e = ("%d = %d × 10, so %d × %d = %d × %d × 10. %d × %d: %s. So %d × %d = %d, then write one 0: %s."
             % (m, d, x, y, a, d, a, d, steps_1d(a, d), a, d, a * d, f(ans)))
        add("What is %d × %d?" % (x, y), ans, wrong, e)
    for d, m in [(4, 300), (6, 500), (8, 400)]:
        ans = d * m
        e = ("%d is %d hundreds. %d × %d hundreds = %d hundreds = %s." % (m, m // 100, d, m // 100, d * m // 100, f(ans)))
        if (d * m // 100) % 10 == 0:
            e += " The 0 in %d is part of the fact, so the answer has three zeros." % (d * m // 100)
        add("What is %d × %d?" % (d, m), ans, [ans // 10, ans * 10, d + m], e)
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Multiply by 10, 100 and multiples of 10", "items": its}


# ------------------------------------------------------------ set 3: area models
def set_area(rnd, seen):
    its = []
    # A: blank area model -> product (24 × 13 first)
    seen.add((24, 13))
    pairs = [(24, 13)] + [pick(rnd, seen, hi=79) for _ in range(3)]
    for a, b in pairs:
        wrong = [two_pp(a, b), skip_pp(a, b), one_zero(a, b), no_zero(a, b), a + b]
        its.append(mcq(fig(area_2d(a, b)) + "Use the area model to find %d × %d." % (a, b), f(a * b),
                       [f(v) for v in wrong], pp_2d(a, b), rnd))
    # A2: 3-digit × 1-digit area model
    for a, d in [(236, 4), (318, 7)]:
        h, t, o = a // 100 * 100, a // 10 % 10 * 10, a % 10
        parts3 = [h * d, t * d, o * d]
        wrong = [a * d - t * d, add_cols(parts3, drop="all"), a * d - h * d + h * d // 10, h * d + o * d + t * d // 10]
        its.append(mcq(fig(area_3x1(a, d)) + "Use the area model to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in wrong], pp_3x1(a, d), rnd))
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
    return {"title": "Area models (24 × 13)", "items": its}


# ------------------------------------------------------------ set 4: standard algorithm
def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Use the standard algorithm.") if col else "Calculate %d × %d." % (a, b)
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b, detail=1), rnd)


def compute_1d_item(a, d, rnd, col):
    q = (fig(col_problem(a, d)) + "Use the standard algorithm.") if col else "Calculate %d × %d." % (a, d)
    e = "%d × %d: start with the ones. %s. So %d × %d = %s." % (a, d, cap(steps_1d(a, d)), a, d, f(a * d))
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], e, rnd)


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


def set_algorithm(rnd, seen, seen3, P):
    its = []
    for i in range(5):
        a, d = pick_3x1(rnd, seen3)
        its.append(compute_1d_item(a, d, rnd, i % 2 == 0))
    for i in range(6):
        a, b = pick(rnd, seen)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen)
        its.append(box_row_item(a, b, 1, rnd))
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


# ------------------------------------------------------------ set 5: word problems
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


# (question, a, b, unit, lead): the answer is a × b. unit '$' = money, else 'x unit'. {n} {he} {his}.
STORIES = [
    ("{n}'s class takes part in the Terry Fox Run. Each of the 27 students raises $35. How much does the class raise?",
     35, 27, "$", "27 students × $35"),
    ("The hockey arena in Kamloops has 24 rows of seats with 38 seats in each row. How many seats are there?",
     38, 24, "seats", "24 rows × 38 seats"),
    ("Volunteers plant cedar seedlings in 37 rows, with 24 seedlings in each row. How many seedlings do they plant?",
     24, 37, "seedlings", "37 rows × 24 seedlings"),
    ("An orchard in the Okanagan packs 48 apples in each box. How many apples are in 26 boxes?",
     48, 26, "apples", "26 boxes × 48 apples"),
    ("A school garden in Surrey is 23 m long and 14 m wide. What is its area?",
     23, 14, "m²", "area = 23 m × 14 m"),
    ("A group snowboard lesson costs $45 for each student. 23 students from {n}'s school sign up. What is the total cost?",
     45, 23, "$", "23 students × $45"),
    ("Each tray at the school bake sale holds 36 cookies. The Grade 5 class fills 18 trays. How many cookies is that?",
     36, 18, "cookies", "18 trays × 36 cookies"),
    ("A lacrosse club in Burnaby buys 16 new sticks for $34 each. How much does the club spend?",
     34, 16, "$", "16 sticks × $34"),
    ("{n} practises the piano for 35 minutes a day. How many minutes does {he} practise in 28 days?",
     35, 28, "minutes", "28 days × 35 minutes"),
    ("A BC Ferries ship carries 236 cars on each sailing. How many cars do 6 sailings carry?",
     236, 6, "cars", "6 sailings × 236 cars"),
    ("A SkyTrain carries 145 riders on one trip. How many riders does it carry on 8 trips?",
     145, 8, "riders", "8 trips × 145 riders"),
    ("4 classes in Nanaimo each raise 175 salmon eggs in a classroom tank. How many eggs is that in all?",
     175, 4, "eggs", "4 classes × 175 eggs"),
    ("Each shelf in the school library holds 128 books. How many books fit on 7 shelves?",
     128, 7, "books", "7 shelves × 128 books"),
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
        if b < 10:
            e = "%s, so multiply %d × %d. %s. Answer: %s." % (cap(lead), a, b, cap(steps_1d(a, b)), fm(a * b))
            cs = cands_1d(a, b)
        else:
            e = "%s, so multiply %d × %d. " % (cap(lead), a, b) + steps(a, b)
            cs = cands(a, b, rnd)
        its.append(mcq(q, fm(a * b), [fm(v) for v in cs], e, rnd))
    # two-step: empty seats
    assert 32 * 45 == 1440 and 1440 - 1218 == 222
    its.append(mcq("The arena in Prince George is set up with 32 rows of 45 seats. 1218 people come to the game. "
                   "How many seats are empty?",
                   "222 seats", ["1440 seats", "2658 seats", "%d seats" % sfl(1440, 1218)],
                   "Step 1: seats: 45 × 32 (row 1: 45 × 2 = 90; row 2: 45 × 30 = 1350; 90 + 1350 = 1440). "
                   "Step 2: empty seats: 1440 − 1218 = 222.", rnd))
    # two-step: field trip
    assert 26 * 23 == 598 and 26 * 14 == 364 and 26 * 9 == 234
    its.append(mcq("A Grade 5 field trip to a museum in Victoria costs $14 a student for entry and $9 a student for the bus. "
                   "26 students go. What is the total cost?", "$598",
                   ["$364", "$234", "$" + str(no_zero(26, 23))],
                   "Each student pays $14 + $9 = $23. 26 × $23: row 1: 26 × 3 = 78; row 2: 26 × 20 = 520. "
                   "78 + 520 = $598. (Or: entry 26 × $14 = $364, bus 26 × $9 = $234, total $598.)", rnd))
    # estimates
    assert 67 * 48 == 3216 and 86 * 29 == 2494
    its.append(estimate_item(67, 48, rnd))
    its.append(estimate_item(86, 29, rnd))
    assert 19 * 42 == 798
    its.append(mcq("A hockey team in Kelowna orders hoodies that cost $42 each. "
                   "What is the best estimate of the cost of 19 hoodies?", "about $800",
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
    return {"title": "Word problems", "items": its}


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


def lesson_fig_1d(a, d, label):
    rows = [("ex", row_regroups(a, d, 0)), ("", str(a)), ("×", str(d)), ("", str(a * d))]
    return column_svg(rows, [2], label, notes=["regrouped", "", "", ""], big=True)


def body_html():
    assert 24 * 13 == 312 and 38 * 24 == 912 and 38 * 4 == 152 and 38 * 20 == 760
    assert 236 * 4 == 944 and 24 * 3 == 72 and 24 * 10 == 240
    return (
        "<h2>Start with the facts</h2>"
        "<p>Every big multiplication is built from facts to 10 × 10. If a fact is slow, use one you know: "
        "7 × 8 is 7 × 7 = 49 plus one more 7, so 56. Division facts come from the same family: 56 ÷ 8 = 7.</p>"
        "<h2>Multiply by 10, 100 and multiples of 10</h2>"
        "<p>× 10 moves every digit one place to the left: 34 × 10 = <b>340</b>. "
        "× 100 moves every digit two places: 34 × 100 = <b>3400</b>.</p>"
        "<p>For 20 × 30, use 2 × 3 = 6. Tens × tens = hundreds, so 20 × 30 = <b>600</b>. "
        "For 47 × 60, find 47 × 6 = 282, then write one 0: <b>2820</b>.</p>"
        "<h2>The area model</h2>"
        "<p>Split each number into tens and ones. Draw a rectangle with one part for each pair. "
        "Multiply each part, then add all the parts.</p>"
        "<figure class='sn-fig'>" + area_2d(24, 13, [["200", "40"], ["60", "12"]]) +
        "<figcaption>24 × 13: 20 × 10 = 200, 4 × 10 = 40, 20 × 3 = 60, 4 × 3 = 12. "
        "200 + 40 + 60 + 12 = 312.</figcaption></figure>"
        "<p>A 3-digit number makes three parts: hundreds, tens and ones.</p>"
        "<figure class='sn-fig'>" + area_3x1(236, 4, [["800", "120", "24"]]) +
        "<figcaption>236 × 4 = 800 + 120 + 24 = 944.</figcaption></figure>"
        "<h2>The standard algorithm</h2>"
        "<p>For 3-digit × 1-digit, start with the ones. Write the ones digit of each product and regroup the tens "
        "into the next column. Multiply first, then add the regrouped digit.</p>"
        "<figure class='sn-fig'>" + lesson_fig_1d(236, 4, "236 times 4 with the standard algorithm") +
        "<figcaption>6 × 4 = 24: write 4, regroup 2. 3 × 4 + 2 = 14: write 4, regroup 1. "
        "2 × 4 + 1 = 9. So 236 × 4 = 944.</figcaption></figure>"
        "<p>For 2-digit × 2-digit, make <b>one row for each digit</b> of the bottom number. Row 1 multiplies by the ones digit. "
        "Row 2 multiplies by the tens digit, so it starts with a <b>placeholder zero</b> (green). Then add the two rows.</p>"
        "<figure class='sn-fig'>" + lesson_fig(38, 24, "38 times 24 with the standard algorithm") +
        "<figcaption>38 × 24: row 1 is 38 × 4 = 152. Row 2 is 38 × 20: write 0, then 38 × 2 = 76, so 760. "
        "152 + 760 = 912.</figcaption></figure>"
        "<p>Each row of the algorithm is one row of the area model. For 24 × 13, row 1 is 24 × 3 = 72 "
        "(the 3 row: 60 + 12). Row 2 is 24 × 10 = 240 (the 10 row: 200 + 40). 72 + 240 = 312, the same answer.</p>" +
        ex("Estimate to check", "Is 38 × 24 = 912 reasonable?",
           "Round to the nearest ten: 40 × 20 = 800. 912 is close to 800, so it makes sense. "
           "An answer like 228 or 9120 is far off.", "Yes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the zero in the tens row (38 × 24 = 152 + 76 = 228)", "Row 2 is × 20, so write 0 first: 760"],
            ["20 × 30 = 60", "Tens × tens = hundreds: 20 × 30 = 600"],
            ["Only two parts (24 × 13 = 200 + 12)", "There are four parts: 200 + 40 + 60 + 12 = 312"],
            ["Not adding a regrouped digit (236 × 4 = 824)", "Write it small and add it: 3 × 4 + 2 = 14"],
            ["Adding the regrouped digit first", "Multiply first, then add: 3 × 4 + 2 = 14, not (3 + 2) × 4"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Grade 5 students learn in the BC math curriculum?",
     "a": "The Grade 5 BC curriculum lists multiplication and division to three digits, plus multiplication and division facts to 100. Students practise questions such as 24 × 13 and 236 × 4 with area models and the standard algorithm."},
    {"q": "How do you teach 2-digit by 2-digit multiplication?",
     "a": "Start with the area model: split both numbers into tens and ones and add the four parts, so 24 × 13 = 200 + 40 + 60 + 12 = 312. Then show the standard algorithm, where each row is one row of the area model."},
    {"q": "Why do you put a zero in the second row?",
     "a": "The second row multiplies by the tens digit. In 38 × 24 the 2 means 2 tens, so the row is 38 × 20 = 760, not 38 × 2 = 76. The zero keeps the digits in the right places."},
    {"q": "Do Grade 5 students in BC still need to know their times tables?",
     "a": "Yes. Multiplication and division facts to 100 are part of the Grade 5 BC curriculum, and quick recall makes 2- and 3-digit multiplication much easier."},
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
    rnd = random.Random(55806)
    P = People(rnd)
    seen, seen3 = set(), set()
    sets = [set_facts(rnd), set_tens(rnd), set_area(rnd, seen), set_algorithm(rnd, seen, seen3, P), set_story(rnd, P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "multiplication-to-three-digits", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication to Three Digits",
        "seo_title": "Grade 5 Multiplication Worksheets: Area Models and the Standard Algorithm (Free, BC Curriculum)",
        "short_title": "Multiplication to three digits",
        "domain": "Computational fluency",
        "standard_code": "Grade 5: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Multiplication and division to three digits, including division with remainders",
        "meta_desc": "Free Grade 5 math worksheets on multiplication for the BC curriculum: facts to 100, multiplying by 10 and 100, area models, the standard algorithm (2-digit × 2-digit and 3-digit × 1-digit) and BC word problems. 100 questions with an answer key.",
        "key_big": "Split the numbers by place value and multiply every part. In the standard algorithm, the tens row starts with a zero.",
        "key_sub": "24 × 13 = 200 + 40 + 60 + 12 = 312. In the algorithm, row 1 is 24 × 3 = 72 and row 2 is 24 × 10 = 240. 236 × 4 = 800 + 120 + 24 = 944.",
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
    mark_large(u, "([0-9]+ times [0-9]+|area model with)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
