# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Multiplication (MOE 2021 Primary Mathematics Syllabus, Standard,
Number and Algebra, Whole Numbers: "Multiplication algorithm up to 4 digits by 1 digit and
up to 3 digits by 2 digits")
  python3 tools/gen_sg_maths_p4_multiplication.py
4-digit × 1-digit with renaming, 2-digit × 2-digit (area model, then the algorithm),
3-digit × 2-digit, estimating to check, and word problems (rows of seats, boxes of eggs, bar models).
Every product and every wrong answer is computed here. Wrong answers are real mistakes:
forgetting the 0 in the second row, not adding the renamed digit, adding the renamed digit before
multiplying, writing the whole product in one column, adding instead of subtracting.
Singapore English, $, MOE number spacing (5+ digits with a no-break space; 4 digits without).
Column layouts are drawn without separators, as students write them. HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
SLUG = "multiplication"
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


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


def money(v):
    return "$" + f(v)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e, rnd, allow_zero=False):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1 if c.startswith(("Yes", "No")) else 0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−"):
            continue
        if lead == "0" and not allow_zero:
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
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def tw(t, fs):
    """Approximate text width in px (Arial bold)."""
    t = plain(str(t))
    return sum(0.36 if ch in " .,()" + NB else 0.62 for ch in t) * fs


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
        base = {1: 62, 2: 100, 3: 120}.get(len(str(t)), 130)
        ws.append(max(need, base))
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 16)
    hs = [70, 46] if len(lefts) == 2 else [62]
    lw = max(tw(t, FS) for t in lefts) + 14
    top_h = 26
    x0, y0 = lw + 4, top_h + 4
    W = x0 + sum(ws) + 6
    H = y0 + sum(hs) + 6
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


def place_parts(a):
    """3746 -> [3000, 700, 40, 6] (zero parts left out)."""
    L = len(str(a))
    return [d * 10 ** (L - 1 - i) for i, d in enumerate(int(c) for c in str(a)) if d]


def area_row(a, d, show=None):
    """n-digit × 1-digit area model: one part for each place, one row."""
    tops = place_parts(a)
    cells = show or [["" for _ in tops]]
    return area_svg([str(t) for t in tops], [str(d)], cells, "area model with %d parts: %d × %d" % (len(tops), a, d))


def area_3x2(a, b, show=None):
    tops = place_parts(a)
    tb, ob = parts(b)
    cells = show or [["" for _ in tops], ["" for _ in tops]]
    return area_svg([str(t) for t in tops], [str(tb), str(ob)], cells, "area model with 6 parts: %d × %d" % (a, b))


# ------------------------------------------------------------ column figure
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


def carries(a, d):
    return len(carry_list(a, d))


def column_svg(rows, rules, label, notes=None, big=False):
    """Multiplication in columns, ones lined up on the right.
    rows = list of (sign, text) or (sign, text, nz): nz = number of zeros at the end drawn green.
    sign 'ex' = a row of small renamed digits: text is a dict {place: digit}.
    text '[?]' = a red dashed box across the row. A '?' digit is drawn red."""
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
        note_w = max(tw(n, nfs) * 0.9 for n in notes if n) + 18
    num_w = cw * slots + 20
    W = num_w + note_w
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
                col = RED if ch == "?" else (GREEN if slot < nz else INK)
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
    H = y + 12
    return svg_wrap(W, H, "".join(s), label, "monospace")


def col_problem(a, b):
    return column_svg([("", str(a)), ("×", str(b))], [1], "%d times %d written in columns" % (a, b))


def pp_rows(a, b):
    """The rows of the algorithm, ones row first: (digit, place, value)."""
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
    return column_svg(rows, rules, "%d times %d worked in columns" % (a, b))


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
            out.append("%s = %d, write %d, rename %d" % (ex_, p, p % 10, p // 10))
        c = p // 10 if i < len(ds) - 1 else 0
    return "; ".join(out)


def row_text(a, d, i):
    v = a * d * 10 ** i
    if i == 0:
        return "%s × %d = %s" % (f(a), d, f(v))
    return "%s × %s = %s (write 0 in the ones place, then %s × %d = %s)" % (f(a), f(d * 10 ** i), f(v), f(a), d, f(a * d))


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


def pp_row_text(a, d):
    ps = place_parts(a)
    return ("Split %s = %s. %s. Add: %s = %s."
            % (f(a), " + ".join(f(p) for p in ps), ", ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
               " + ".join(f(p * d) for p in ps), f(a * d)))


# ------------------------------------------------------------ typical mistakes
def mult_row(a, d, mode="ok", k=None):
    """a × d (one digit), done with a typical mistake.
    nocarry: forget every renamed digit. skip: forget the one made in place k.
    cfirst: add the renamed digit BEFORE multiplying."""
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
    """No 0 in the second row: the tens row is 10 times too small."""
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
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"), add_cols([v for d, i, v in pr], drop="all")]
    if a < 100:
        more.append(two_pp(a, b))
    more += [total_with(a, b, "nocarry", only=j) for j in range(len(pr))]
    rnd.shuffle(more)
    return out + more + [a * (b % 10), total_with(a, b, "skip", k=0), skip_pp(a, b), one_zero(a, b)]


def concat_1d(a, d):
    """Writes every product in full, no renaming: 236 × 4 -> 8|12|24."""
    return int("".join(str(x * d) for x in reversed(digits(a))))


def cands_1d(a, d):
    return [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", 0),
            mult_row(a, d, "skip", 1), mult_row(a, d, "skip", 2), concat_1d(a, d)]


def pick(rnd, seen, lo=13, hi=89, blo=13, bhi=69):
    """2-digit × 2-digit, no 0 or 1 ones digits, both rows of the algorithm rename."""
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


def pick_3x2(rnd, seen):
    """3-digit × 2-digit, no zero digits, both rows rename, product below 100 000."""
    while True:
        a, b = rnd.randint(123, 987), rnd.randint(13, 89)
        if "0" in str(a) or len(set(str(a))) < 3 or b % 10 < 2 or b // 10 == b % 10:
            continue
        if (a, b) in seen or a * b >= 100000:
            continue
        if carries(a, b % 10) < 1 or carries(a, b // 10) < 1:
            continue
        seen.add((a, b))
        return a, b


def pick_3x1(rnd, seen):
    while True:
        a, d = rnd.randint(124, 879), rnd.randint(3, 9)
        if "0" in str(a) or len(set(str(a))) < 3 or (a, d) in seen:
            continue
        if carries(a, d) < 2:
            continue
        seen.add((a, d))
        return a, d


def pick_4x1(rnd, seen):
    """4-digit × 1-digit, no zero digits, at least 3 renamings."""
    while True:
        a, d = rnd.randint(1234, 9876), rnd.randint(3, 9)
        if "0" in str(a) or len(set(str(a))) < 3 or (a, d) in seen:
            continue
        if carries(a, d) < 3:
            continue
        seen.add((a, d))
        return a, d


# ------------------------------------------------------------ set 1: 4-digit × 1-digit
def compute_1d_item(a, d, rnd, col):
    q = (fig(col_problem(a, d)) + "Find the value.") if col else "Find the value of %s × %d." % (f(a), d)
    e = "%s × %d: start with the ones. %s. So %s × %d = %s." % (f(a), d, cap(steps_1d(a, d)), f(a), d, f(a * d))
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], e, rnd)


def missing_digit_item(a, d, rnd, j=0):
    """The product with one digit shown as a red ?: a column that had a renamed digit added."""
    p = str(a * d)
    cl = carry_list(a, d)
    ks = sorted(cl)
    k = ks[j % len(ks)]                           # place counted from the right
    pos = len(p) - 1 - k
    ans = int(p[pos])
    shown = p[:pos] + "?" + p[pos + 1:]
    cand = []
    for m in (mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", k - 1)):
        s = str(m).zfill(len(p))
        cand.append(int(s[len(s) - 1 - k]))
    x = digits(a)[k]
    cand += [x * d % 10, cl[k], (ans + 1) % 10, (ans + 9) % 10]
    q = (fig(column_svg([("", str(a)), ("×", str(d)), ("", shown)], [1], "%d times %d with one digit missing" % (a, d)))
         + "Which digit is missing from the answer?")
    e = ("Work from the ones: %s. In that column, %d × %d + %d = %d, so the digit is %d. %s × %d = %s."
         % (steps_1d(a, d), x, d, cl[k], x * d + cl[k], ans, f(a), d, f(a * d)))
    return mcq(q, str(ans), [str(c) for c in cand], e, rnd, allow_zero=True)


WHAT1 = ["Did not add the renamed digit", "Added before multiplying", "Did not rename at all",
         "Multiplied only the ones digit"]


def what_1d_item(a, d, kind, rnd, P):
    n, he, his = P.next()
    if kind == 0:
        got = mult_row(a, d, "nocarry")
        why = "%s wrote the ones digit of each product but did not add the renamed digits." % n
    elif kind == 1:
        got = mult_row(a, d, "cfirst")
        x = digits(a)[1]
        c = carry_list(a, d)[1]
        why = ("%s added the renamed digit first: (%d + %d) × %d. Multiply first, then add: %d × %d + %d."
               % (n, x, c, d, x, d, c))
    else:
        got = concat_1d(a, d)
        why = "%s wrote every product in full (%s) instead of renaming the tens into the next column." % (
            n, ", ".join(str(x * d) for x in reversed(digits(a))))
    assert got != a * d
    why += " Correct: %s. So %s × %d = %s." % (steps_1d(a, d), f(a), d, f(a * d))
    q = (fig(column_svg([("", str(a)), ("×", str(d)), ("", str(got))], [1], "%d times %d with a mistake" % (a, d)))
         + "%s worked out %s × %d like this. What mistake did %s make?" % (n, f(a), d, he))
    ans = WHAT1[kind]
    return mcq(q, ans, [w for w in WHAT1 if w != ans], why, rnd)


def set_4x1(rnd, P):
    its = []
    seen3, seen4 = set(), set()
    for i in range(3):
        a, d = pick_3x1(rnd, seen3)
        its.append(compute_1d_item(a, d, rnd, i != 1))
    seen4.update([(3065, 4), (4708, 6)])
    fixed = [(3065, 4), (4708, 6)]
    for i in range(7):
        a, d = fixed[i] if i < len(fixed) else pick_4x1(rnd, seen4)
        its.append(compute_1d_item(a, d, rnd, i % 2 == 0))
    for j in range(4):
        a, d = pick_4x1(rnd, seen4)
        its.append(missing_digit_item(a, d, rnd, j))
    for kind in range(3):
        a, d = pick_4x1(rnd, seen4)
        its.append(what_1d_item(a, d, kind, rnd, P))
    for a, d in [(3746, 4), (5283, 7)]:
        ps = place_parts(a)
        right = " + ".join("%d × %d" % (p, d) for p in ps)
        wrong = ["%d × %d + %s" % (ps[0], d, " + ".join(str(p) for p in ps[1:])),
                 " + ".join("%d × %d" % (int(c), d) for c in str(a)),
                 "%s + %d × %d" % (" + ".join(str(p) for p in ps[:-1]), ps[-1], d)]
        e = ("Split %s by place value: %s. Every part must be multiplied by %d: %s = %s."
             % (f(a), " + ".join(str(p) for p in ps), d, " + ".join(f(p * d) for p in ps), f(a * d)))
        its.append(mcq("Which is equal to %s × %d?" % (f(a), d), right, wrong, e, rnd))
    a, d = 2413, 3
    ps = place_parts(a)
    cells = [[f(p * d) for p in ps]]
    wrong = [add_cols([p * d for p in ps], drop="all"), a * d - ps[1] * d, ps[0] * d + ps[3] * d,
             int("".join(str(int(c) * d) for c in str(a)))]
    its.append(mcq(fig(area_row(a, d, cells)) + "The area model shows %s × %d. What is the product?" % (f(a), d),
                   f(a * d), [f(v) for v in wrong],
                   "Add all the parts: %s = %s." % (" + ".join(f(p * d) for p in ps), f(a * d)), rnd))
    assert len(its) == 20, len(its)
    return {"title": "4-digit × 1-digit with renaming", "items": its}


# ------------------------------------------------------------ set 2: 2-digit × 2-digit
def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Find the value.") if col else "Find the value of %d × %d." % (a, b)
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b, detail=1), rnd)


def box_row_item(a, b, rnd):
    d, i, v = pp_rows(a, b)[1]
    q = fig(work_svg(a, b, box=1)) + "What number goes in the dashed box?"
    wrong = [a * d, mult_row(a, d, "nocarry") * 10, mult_row(a, d, "cfirst") * 10, v * 10, a * (b % 10)]
    e = ("The second row multiplies by the tens digit, so it is %s × %d. Write 0 in the ones place first, then %s × %d: %s. "
         "The row is %s, not %s." % (f(a), d * 10, f(a), d, steps_1d(a, d), f(v), f(a * d)))
    e += " Check: %s = %s." % (" + ".join(f(x) for _, _, x in pp_rows(a, b)), f(a * b))
    return mcq(q, f(v), [f(x) for x in wrong], e, rnd)


def sum_box_item(a, b, rnd):
    pr = [v for d, i, v in pp_rows(a, b)]
    cs = add_carries(pr)
    wrong = [add_cols(pr, drop="all")] + [add_cols(pr, drop=k) for k in cs] + \
            [add_cols(pr, extra=k) for k in range(len(str(a * b))) if k not in cs] + [abs(pr[1] - pr[0])]
    q = fig(work_svg(a, b, box="sum")) + "What number goes in the dashed box?"
    e = ("Add the two rows, lining up the ones, and add every renamed digit: %s = %s."
         % (" + ".join(f(v) for v in pr), f(a * b)))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


WHAT = ["Forgot the 0 in the second row", "Did not add the renamed digit", "Added before multiplying",
        "Multiplied by only one digit"]


def what_item(a, b, kind, rnd, P):
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    n, he, his = P.next()
    if kind == 0:
        got = v0 + a * d1
        rows = [("", str(a)), ("×", str(b)), ("", str(v0)), ("+", str(a * d1)), ("", str(got))]
        why = ("The second row should be %s × %d = %s, but %s wrote %s. The 0 in the ones place is missing."
               % (f(a), d1 * 10, f(v1), he, f(a * d1)))
    elif kind == 1:
        r0 = mult_row(a, d0, "nocarry")
        got = r0 + v1
        rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(v1)), ("", str(got))]
        why = "The first row should be %s, not %s: %s. The renamed digit was not added." % (f(v0), f(r0), steps_1d(a, d0))
    else:
        r0 = mult_row(a, d0, "cfirst")
        got = r0 + v1
        rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(v1)), ("", str(got))]
        why = ("The first row should be %s, not %s. %s added the renamed digit before multiplying. "
               "Multiply first, then add: %s." % (f(v0), f(r0), cap(he), steps_1d(a, d0)))
    assert got != a * b and rows[2][1] != rows[3][1]
    why += " The correct answer is %s." % f(a * b)
    q = (fig(column_svg(rows, [1, 3], "%d times %d with a mistake" % (a, b))) +
         "%s worked out %s × %d = %s. What mistake did %s make?" % (n, f(a), b, f(got), he))
    ans = WHAT[kind]
    return mcq(q, ans, [w for w in WHAT if w != ans], why, rnd)


def set_2x2(rnd, seen, P):
    its = []
    # area model -> product
    for _ in range(4):
        a, b = pick(rnd, seen, hi=79)
        wrong = [two_pp(a, b), skip_pp(a, b), one_zero(a, b), no_zero(a, b), a + b]
        its.append(mcq(fig(area_2d(a, b)) + "Use the area model to find %d × %d." % (a, b), f(a * b),
                       [f(v) for v in wrong], pp_2d(a, b), rnd))
    # the missing part
    for k in range(3):
        a, b = pick(rnd, seen, hi=79)
        grid = area_cells(a, b)
        ta, oa = parts(a)
        tb, ob = parts(b)
        lab = [[(ta, tb), (oa, tb)], [(ta, ob), (oa, ob)]]
        r, c = [(0, 0), (0, 1), (1, 0)][k]
        show = [[f(grid[i][j]) for j in range(2)] for i in range(2)]
        show[r][c] = "?"
        x, y = lab[r][c]
        ans = x * y
        if x % 10 == 0 and y % 10 == 0:
            wrong = [ans // 10, ans * 10, x + y]
        else:
            wrong = [(x // 10 if x % 10 == 0 else x) * (y // 10 if y % 10 == 0 else y), ans * 10, x + y]
        e = "The ? part is %d wide and %d tall: %d × %d = %s." % (x, y, x, y, f(ans))
        if x % 10 == 0 and y % 10 == 0:
            e += " Think: %d tens × %d tens = %d hundreds." % (x // 10, y // 10, ans // 100)
        e += " All four parts add up to %d × %d = %s." % (a, b, f(a * b))
        its.append(mcq(fig(area_2d(a, b, show)) + "What number goes in the part marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # all parts filled in -> add
    k = 0
    while k < 2:
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
    # which expression
    a, b = pick(rnd, seen, hi=89)
    ta, oa = parts(a)
    tb, ob = parts(b)
    right = "%d × %d + %d × %d" % (a, tb, a, ob)
    wrong = ["%d × %d + %d × %d" % (a, tb // 10, a, ob), "%d × %d + %d × %d" % (ta, tb, oa, ob), "%d × %d + %d" % (a, tb, ob)]
    e = ("Split %d into %d + %d. Multiply %d by both parts: %d × %d + %d × %d = %s + %s = %s. "
         "These are the two rows of the algorithm." % (b, tb, ob, a, a, tb, a, ob, f(a * tb), f(a * ob), f(a * b)))
    its.append(mcq("Which is equal to %d × %d?" % (a, b), right, wrong, e, rnd))
    # algorithm
    for i in range(4):
        a, b = pick(rnd, seen)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(3):
        a, b = pick(rnd, seen)
        its.append(box_row_item(a, b, rnd))
    while True:
        a, b = pick(rnd, seen)
        if len(add_carries([v for d, i, v in pp_rows(a, b)])) >= 2:
            break
    its.append(sum_box_item(a, b, rnd))
    for kind in (0, 1):
        a, b = pick(rnd, seen)
        its.append(what_item(a, b, kind, rnd, P))
    assert len(its) == 20, len(its)
    return {"title": "2-digit × 2-digit: area model, then the algorithm", "items": its}


# ------------------------------------------------------------ set 3: 3-digit × 2-digit
def set_3x2(rnd, seen, P):
    its = []
    for _ in range(2):
        a, b = pick_3x2(rnd, seen)
        ps = place_parts(a)
        tb, ob = parts(b)
        cells = [[f(p * tb) for p in ps], [f(p * ob) for p in ps]]
        allp = [p * tb for p in ps] + [p * ob for p in ps]
        wrong = [a * b - ps[1] * tb, add_cols(allp, drop="all"), a * b - ps[0] * ob, no_zero(a, b)]
        e = "Add all six parts: %s = %s. So %d × %d = %s." % (" + ".join(f(p) for p in allp), f(a * b), a, b, f(a * b))
        its.append(mcq(fig(area_3x2(a, b, cells)) + "The area model shows %d × %d. What is the product?" % (a, b),
                       f(a * b), [f(v) for v in wrong], e, rnd))
    a, b = pick_3x2(rnd, seen)
    tb, ob = parts(b)
    h = a // 100 * 100
    right = "%d × %d + %d × %d" % (a, tb, a, ob)
    wrong = ["%d × %d + %d × %d" % (a, tb // 10, a, ob), "%d × %d + %d × %d" % (h, tb, a - h, ob),
             "%d × %d + %d" % (a, tb, ob)]
    e = ("Split %d into %d + %d. Multiply all of %d by each part: %d × %d + %d × %d = %s + %s = %s."
         % (b, tb, ob, a, a, tb, a, ob, f(a * tb), f(a * ob), f(a * b)))
    its.append(mcq("Which is equal to %d × %d?" % (a, b), right, wrong, e, rnd))
    for i in range(8):
        a, b = pick_3x2(rnd, seen)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick_3x2(rnd, seen)
        its.append(box_row_item(a, b, rnd))
    k = 0
    while k < 2:
        a, b = pick_3x2(rnd, seen)
        if len(add_carries([v for d, i, v in pp_rows(a, b)])) >= 2:
            its.append(sum_box_item(a, b, rnd))
            k += 1
    for kind in (0, 1, 2):
        a, b = pick_3x2(rnd, seen)
        its.append(what_item(a, b, kind, rnd, P))
    assert len(its) == 20, len(its)
    return {"title": "3-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 4: estimate to check
def rnd_to(n, p):
    return (n + p // 2) // p * p


def other_way(n, p):
    r = rnd_to(n, p)
    return r - p if r > n else r + p


def eq(x, y, v):
    return "%s × %s = %s" % (f(x), f(y), f(v))


def round_item(a, b, rnd):
    if b < 10:
        ra, rb = rnd_to(a, 1000), b
        q = "Round %s to the nearest thousand to estimate %s × %d." % (f(a), f(a), b)
        right = eq(ra, rb, ra * rb)
        oa = other_way(a, 1000)
        wrong = [eq(oa, rb, oa * rb), eq(ra, rb, ra * rb // 10), eq(ra, rb, ra * rb * 10)]
        e = ("%s has %d hundreds, so it rounds %s to %s. %s × %d = %s. The exact answer is %s."
             % (f(a), a // 100 % 10, "up" if ra > a else "down", f(ra), f(ra), b, f(ra * rb), f(a * b)))
    else:
        pa = 100 if a >= 100 else 10
        ra, rb = rnd_to(a, pa), rnd_to(b, 10)
        if pa == 100:
            q = "Round %d to the nearest hundred and %d to the nearest ten to estimate %d × %d." % (a, b, a, b)
        else:
            q = "Round each number to the nearest ten to estimate %d × %d." % (a, b)
        right = eq(ra, rb, ra * rb)
        oa, ob = other_way(a, pa), other_way(b, 10)
        wrong = [eq(oa, ob, oa * ob), eq(ra, ob, ra * ob), eq(ra, rb, ra * rb // 10)]
        e = ("%d rounds %s to %d and %d rounds %s to %d. %d × %d = %s. The exact answer is %s, close to the estimate."
             % (a, "up" if ra > a else "down", ra, b, "up" if rb > b else "down", rb, ra, rb, f(ra * rb), f(a * b)))
    return mcq(q, right, wrong, e, rnd)


def est_of(a, b):
    return (rnd_to(a, 100) if a >= 100 else rnd_to(a, 10)), rnd_to(b, 10)


def check_item(a, b, claim, rnd, P):
    n, he, his = P.next()
    ra, rb = est_of(a, b)
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
             "%s forgot the 0 in the second row. The correct answer is %s."
             % (a, b, ra, rb, f(est), f(claim), f(est), n, f(a * b)))
    q = "%s worked out %d × %d = %s. Estimate to check. Is %s answer reasonable?" % (n, a, b, f(claim), his)
    return mcq(q, right, wrong, e, rnd)


def could_item(a, b, rnd):
    ra, rb = est_of(a, b)
    est = ra * rb
    wrong = [no_zero(a, b), a * b * 10, a + b]
    e = ("Estimate: %d × %d is about %d × %d = %s. Only %s is close to %s. (%s forgot the 0 in the second row; "
         "%s has one 0 too many; %s comes from adding.)"
         % (a, b, ra, rb, f(est), f(a * b), f(est), f(wrong[0]), f(wrong[1]), f(wrong[2])))
    return mcq("Use an estimate. Which of these is the value of %d × %d?" % (a, b), f(a * b), [f(w) for w in wrong], e, rnd)


def set_estimate(rnd, P):
    its = []
    tests = [(3746, 4), (6281, 3), (67, 48), (83, 26), (487, 32), (624, 58)]
    for a, b in tests:
        assert rnd_to(a, 1000 if b < 10 else (100 if a >= 100 else 10)) != a
        its.append(round_item(a, b, rnd))
    assert 72 * 39 == 2808 and 487 * 32 != 0
    for a, b, ok in [(72, 39, True), (58, 34, False), (46, 27, False), (318, 42, True), (563, 28, False)]:
        its.append(check_item(a, b, a * b if ok else no_zero(a, b), rnd, P))
    for a, b in [(59, 47), (84, 33), (392, 61), (706, 49)]:
        its.append(could_item(a, b, rnd))
    # estimates in context
    assert 19 * 42 == 798
    its.append(mcq("A school orders 19 boxes of exercise books at $42 a box. About how much is the total cost?",
                   "about $800", ["about $80", "about $8000", "about $1000"],
                   "Round 19 to 20 and $42 to $40. 20 × $40 = $800. The exact cost is 19 × $42 = $798, very close. "
                   "(Rounding $42 up to $50 gives $1000, which is too far off.)", rnd))
    assert 312 * 8 == 2496
    its.append(mcq("The school canteen sells 312 plates of fried rice each week. About how many plates does it sell in 8 weeks?",
                   "about 2400 plates", ["about 240 plates", "about 24" + NB + "000 plates", "about 3000 plates"],
                   "Round 312 to the nearest hundred: 300. 300 × 8 = 2400. Do not round 8 to 10: that gives 3000, "
                   "which is too far off. The exact answer is 312 × 8 = 2496.", rnd))
    assert 1985 * 4 == 7940
    its.append(mcq("A theatre sells 1985 tickets for each show. About how many tickets does it sell for 4 shows?",
                   "about 8000 tickets", ["about 800 tickets", "about 80" + NB + "000 tickets", "about 4000 tickets"],
                   "Round 1985 to the nearest thousand: 2000. 2000 × 4 = 8000. (Rounding 1985 down to 1000 gives 4000, "
                   "far too small.) The exact answer is 1985 × 4 = 7940.", rnd))
    assert 215 * 48 == 10320
    its.append(mcq("A stadium has 48 rows with 215 seats in each row. About how many seats are there?",
                   "about 10" + NB + "000 seats", ["about 1000 seats", "about 100" + NB + "000 seats", "about 8000 seats"],
                   "Round 215 to 200 and 48 to 50. 200 × 50 = 10" + NB + "000. (Rounding 48 down to 40 gives 8000.) "
                   "The exact answer is 215 × 48 = 10" + NB + "320.", rnd))
    assert 28 * 31 == 868
    its.append(mcq("Kavya reads 28 pages of a storybook each day. About how many pages does she read in 31 days?",
                   "about 900 pages", ["about 90 pages", "about 9000 pages", "about 600 pages"],
                   "Round 28 to 30 and 31 to 30. 30 × 30 = 900. (Using 20 × 30 = 600 rounds 28 the wrong way.) "
                   "The exact answer is 28 × 31 = 868.", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Estimate to check", "items": its}


# ------------------------------------------------------------ bar model figure (drawn to scale)
def model_svg(rows, label, W=440):
    """rows: list of dicts
         name:  text at the left of the bar ('' for none)
         segs:  [(length, text inside, shaded)] drawn left to right
         over:  [(start, end, text)] brackets above the bar
         under: [(start, end, text)] brackets below the bar
       Text containing '?' is drawn red."""
    names = [r.get("name", "") for r in rows]
    nw = (max(tw(n, 15) for n in names) + 12) if any(names) else 0
    L = 8 + nw
    R = W - 10
    tot = max(sum(F(a) for a, _, _ in r["segs"]) for r in rows)
    sc = (R - L) / float(tot)
    s = []
    y = 4
    for r in rows:
        over, under = r.get("over", []), r.get("under", [])
        if over:
            y += 24
            for a, b, t in over:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 6, x1, y, x2, y, x2, y + 6, col))
                half = tw(t, 15) / 2 + 2
                assert half * 2 <= x2 - x1 + 30 or len(over) == 1, ("bracket text too wide", t)
                cx = min(max((x1 + x2) / 2, half + 2), W - half - 2)
                s.append(text(cx, y - 6, t, 15, col=col))
            y += 8
        y0 = y
        bh = 34
        x = L
        for a, t, sh in r["segs"]:
            w = float(a) * sc
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y0, w, bh, FILL if sh else "#ffffff", INK))
            if t:
                assert tw(t, 14) + 4 <= w, ("text too wide for segment", t, w)
                s.append(text(x + w / 2, y0 + bh / 2 + 5, t, 14, col=RED if "?" in t else INK))
            x += w
        if r.get("name"):
            s.append(text(8, y0 + bh / 2 + 5, r["name"], 15, "start"))
        y = y0 + bh
        if under:
            for a, b, t in under:
                x1, x2 = L + float(a) * sc, L + float(b) * sc
                col = RED if "?" in t else INK
                s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (x1, y + 4, x1, y + 10, x2, y + 10, x2, y + 4, col))
                half = tw(t, 15) / 2 + 2
                cx = min(max((x1 + x2) / 2, half + 2), W - half - 2)
                s.append(text(cx, y + 28, t, 15, col=col))
            y += 32
        y += 10
    return svg_wrap(W, y - 4, "".join(s), label)


def units(n, each=""):
    return [(1, each, True) for _ in range(n)]


# ------------------------------------------------------------ set 5: word problems
def sfl(a, b):
    """'Smaller from larger' subtraction mistake in every column."""
    r, i = 0, 0
    while a or b:
        r += abs(a % 10 - b % 10) * 10 ** i
        a, b, i = a // 10, b // 10, i + 1
    return r


# (question, a, b, unit, lead): the answer is a × b. unit '$' = money. {n} {he} {his}.
STORIES = [
    ("The school hall has 28 rows of seats. There are 36 seats in each row. How many seats are there in the hall?",
     36, 28, "seats", "28 rows × 36 seats"),
    ("A box holds 12 eggs. A supermarket sells 365 boxes of eggs in a week. How many eggs does it sell?",
     365, 12, "eggs", "365 boxes × 12 eggs"),
    ("A carton holds 18 eggs. A shop has 245 cartons of eggs. How many eggs does the shop have?",
     245, 18, "eggs", "245 cartons × 18 eggs"),
    ("A stadium has 46 rows with 128 seats in each row. How many seats are there?",
     128, 46, "seats", "46 rows × 128 seats"),
    ("A bakery bakes 1475 kaya buns each day. How many kaya buns does it bake in 6 days?",
     1475, 6, "kaya buns", "6 days × 1475 buns"),
    ("A train carries 1286 passengers on each trip. How many passengers does it carry on 7 trips?",
     1286, 7, "passengers", "7 trips × 1286 passengers"),
    ("A school buys 9 laptops at $1245 each. How much does the school pay?",
     1245, 9, "$", "9 laptops × $1245"),
    ("For Chinese New Year, a shop packs mandarin oranges in boxes of 24. It packs 156 boxes. "
     "How many mandarin oranges are there?", 156, 24, "mandarin oranges", "156 boxes × 24 oranges"),
    ("A bus can take 42 students. For Sports Day, the school books 17 buses. How many students can the buses take?",
     42, 17, "students", "17 buses × 42 students"),
    ("A fruit seller has 27 baskets of rambutans. There are 48 rambutans in each basket. How many rambutans are there?",
     48, 27, "rambutans", "27 baskets × 48 rambutans"),
    ("{n}'s school has 213 students in Primary 4. Each student gets 14 worksheets for the holidays. "
     "How many worksheets must the school print?", 213, 14, "worksheets", "213 students × 14 worksheets"),
    ("The school library has 135 shelves. Each shelf holds 64 books. How many books can the shelves hold?",
     135, 64, "books", "135 shelves × 64 books"),
]


def set_story(rnd, P):
    its = []
    for t, a, b, unit, lead in STORIES:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his)
        fm = money if unit == "$" else (lambda v, u=unit: "%s %s" % (f(v), u))
        big, small = (a, b) if a > b else (b, a)
        if small < 10:
            e = "%s, so multiply %s × %d. %s. Answer: %s." % (cap(lead), f(big), small, cap(steps_1d(big, small)), fm(a * b))
            cs = cands_1d(big, small)
        else:
            e = "%s, so multiply %s × %d. " % (cap(lead), f(big), small) + steps(big, small)
            cs = cands(big, small, rnd)
        its.append(mcq(q, fm(a * b), [fm(v) for v in cs], e, rnd))

    # bar models
    assert 1356 * 4 == 5424
    m = model_svg([{"name": "Ali", "segs": [(1, "$1356", True)]},
                   {"name": "Nurul", "segs": units(4), "over": [(0, 4, "?")]}],
                  "bar model: Ali 1 unit, Nurul 4 units")
    its.append(mcq(fig(m) + "Ali saved $1356. His sister Nurul saved 4 times as much as Ali. How much did Nurul save?",
                   "$5424", ["$1360", "$6780", money(mult_row(1356, 4, "nocarry")), money(mult_row(1356, 4, "cfirst"))],
                   "1 unit = $1356. Nurul has 4 units: 4 × $1356 = $5424 (6 × 4 = 24, rename 2; 5 × 4 + 2 = 22, rename 2; "
                   "3 × 4 + 2 = 14, rename 1; 1 × 4 + 1 = 5).", rnd))
    assert 236 * 4 == 944 and 236 * 5 == 1180
    m = model_svg([{"name": "Kumar", "segs": [(1, "236", True)]},
                   {"name": "Raju", "segs": units(5), "over": [(1, 5, "?")]}],
                  "bar model: Kumar 1 unit, Raju 5 units")
    its.append(mcq(fig(m) + "Kumar has 236 stamps. Raju has 5 times as many stamps as Kumar. "
                   "How many more stamps does Raju have than Kumar?",
                   "944 stamps", ["1180 stamps", "1416 stamps", "%s stamps" % f(mult_row(236, 4, "nocarry")), "241 stamps"],
                   "Raju has 5 units and Kumar has 1 unit, so Raju has 4 units more. 1 unit = 236. "
                   "4 units = 4 × 236 = 944. (5 × 236 = 1180 is how many stamps Raju has.)", rnd))
    assert 1275 * 4 == 5100 and 1275 * 3 == 3825
    m = model_svg([{"name": "", "segs": [(1, "1275", True)] + [(1, "", False)] * 3,
                    "over": [(0, 1, "Monday"), (1, 4, "Saturday")], "under": [(0, 4, "?")]}],
                  "bar model: Monday 1 unit, Saturday 3 units")
    its.append(mcq(fig(m) + "There were 1275 visitors at a museum on Monday. There were 3 times as many visitors "
                   "on Saturday. How many visitors were there on the two days altogether?",
                   "5100 visitors", ["3825 visitors", "1278 visitors", "%s visitors" % f(mult_row(1275, 4, "nocarry")), "6375 visitors"],
                   "Monday is 1 unit and Saturday is 3 units, so the two days are 4 units. 1 unit = 1275. "
                   "4 units = 4 × 1275 = 5100. (3825 is Saturday only.)", rnd))
    assert 1248 * 6 == 7488
    m = model_svg([{"name": "", "segs": units(6, "1248"), "over": [(0, 6, "?")]}],
                  "bar model: 6 units of 1248")
    its.append(mcq(fig(m) + "Each of the 6 Primary 4 classes collected 1248 cans for recycling. "
                   "How many cans did they collect altogether?",
                   "7488 cans", ["1254 cans", "%s cans" % f(mult_row(1248, 6, "nocarry")), "%s cans" % f(mult_row(1248, 6, "cfirst")),
                                 "%s cans" % f(mult_row(1248, 6, "skip", 0))],
                   "6 units, 1 unit = 1248. 6 × 1248: 8 × 6 = 48, write 8, rename 4; 4 × 6 + 4 = 28, write 8, rename 2; "
                   "2 × 6 + 2 = 14, write 4, rename 1; 1 × 6 + 1 = 7. Answer: 7488 cans.", rnd))
    assert 7 * 145 == 1015 and 1015 - 238 == 777 and sfl(1015, 238) == 1223
    m = model_svg([{"name": "", "segs": [(238, "238", True), (777, "?", False)],
                    "over": [(0, 1015, "7 boxes of 145")]}],
                  "bar model: 7 boxes of 145 books, 238 given out")
    its.append(mcq(fig(m) + "Mdm Wong bought 7 boxes of exercise books with 145 books in each box. "
                   "She gave out 238 books. How many books did she have left?",
                   "777 books", ["1015 books", "1253 books", "1223 books"],
                   "Step 1: 7 × 145 = 1015 books (5 × 7 = 35, rename 3; 4 × 7 + 3 = 31, rename 3; 1 × 7 + 3 = 10). "
                   "Step 2: books left: 1015 − 238 = 777.", rnd))
    # two-step
    assert 24 * 35 == 840 and 840 - 768 == 72 and sfl(840, 768) == 128
    its.append(mcq("For the school concert, the hall is set up with 24 rows of 35 chairs. 768 parents come. "
                   "How many chairs are empty?", "72 chairs", ["840 chairs", "1608 chairs", "128 chairs"],
                   "Step 1: chairs: 35 × 24 (first row: 35 × 4 = 140; second row: 35 × 20 = 700; 140 + 700 = 840). "
                   "Step 2: empty chairs: 840 − 768 = 72.", rnd))
    assert 15 * 36 == 540 and no_zero(36, 15) == 216
    its.append(mcq("Mr Rahman buys 15 tickets for a school show at $36 each. He pays with $600. "
                   "How much change does he get?", "$60", ["$540", "$1140", "$384"],
                   "Step 1: cost: 36 × 15 (first row: 36 × 5 = 180; second row: 36 × 10 = 360; 180 + 360 = 540), so $540. "
                   "Step 2: change: $600 − $540 = $60.", rnd))
    assert 125 * 12 == 1500 and 84 * 30 == 2520 and add_cols([1500, 2520], drop="all") == 3020
    its.append(mcq("A farm packs 125 boxes of 12 eggs and 84 trays of 30 eggs. How many eggs does it pack altogether?",
                   "4020 eggs", ["1500 eggs", "2520 eggs", "3020 eggs"],
                   "Boxes: 125 × 12 = 1500 eggs. Trays: 84 × 30 = 2520 eggs. Altogether: 1500 + 2520 = 4020 eggs. "
                   "(5 hundreds + 5 hundreds = 10 hundreds: rename 1 thousand.)", rnd))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


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
    add(("ex", row_regroups(a, d0, 0)), "renamed")
    add(("+", str(v1), 1), "%d × %d" % (a, d1 * 10))
    add(("ex", row_regroups(a, d1, 1)), "renamed")
    rule2 = len(rows) - 1
    add(("", str(a * b)), "add the rows")
    add(("ex", add_regroups([v0, v1])), "renamed when adding")
    return column_svg(rows, [1, rule2], label, notes=notes, big=True)


def lesson_fig_1d(a, d, label):
    rows = [("ex", row_regroups(a, d, 0)), ("", str(a)), ("×", str(d)), ("", str(a * d))]
    return column_svg(rows, [2], label, notes=["renamed", "", "", ""], big=True)


def body_html():
    assert 2367 * 4 == 9468 and 23 * 14 == 322 and 38 * 24 == 912 and 243 * 36 == 8748
    assert 243 * 6 == 1458 and 243 * 30 == 7290 and 325 * 3 == 975
    model = model_svg([{"name": "Siti", "segs": [(1, "325", True)]},
                       {"name": "Wei Ming", "segs": units(4), "over": [(0, 4, "?")]}],
                      "bar model: Siti 1 unit, Wei Ming 4 units")
    return (
        "<h2>4-digit × 1-digit: multiply, then rename</h2>"
        "<p>Start with the ones. Multiply one digit at a time. If a product is 10 or more, write the ones digit "
        "and <b>rename</b> the tens into the next column. Multiply first, then add the renamed digit.</p>"
        "<figure class='sn-fig'>" + lesson_fig_1d(2367, 4, "2367 times 4 worked in columns") +
        "<figcaption>2367 × 4: 7 × 4 = 28, write 8, rename 2. 6 × 4 + 2 = 26, write 6, rename 2. "
        "3 × 4 + 2 = 14, write 4, rename 1. 2 × 4 + 1 = 9. So 2367 × 4 = 9468.</figcaption></figure>"
        "<h2>2-digit × 2-digit: the area model</h2>"
        "<p>Split both numbers into tens and ones. Multiply each part, then add all four parts.</p>"
        "<figure class='sn-fig'>" + area_2d(23, 14, [["200", "30"], ["80", "12"]]) +
        "<figcaption>23 × 14: 20 × 10 = 200, 3 × 10 = 30, 20 × 4 = 80, 3 × 4 = 12. "
        "200 + 30 + 80 + 12 = 322.</figcaption></figure>"
        "<h2>The algorithm: one row for each digit</h2>"
        "<p>The first row multiplies by the ones digit. The second row multiplies by the tens digit, so it "
        "<b>starts with 0</b> in the ones place (green). Then add the two rows.</p>"
        "<figure class='sn-fig'>" + lesson_fig(38, 24, "38 times 24 worked in columns") +
        "<figcaption>38 × 24: first row 38 × 4 = 152. Second row 38 × 20: write 0, then 38 × 2 = 76, so 760. "
        "152 + 760 = 912.</figcaption></figure>"
        "<h2>3-digit × 2-digit</h2>"
        "<p>It works the same way. The rows are just longer.</p>"
        "<figure class='sn-fig'>" + lesson_fig(243, 36, "243 times 36 worked in columns") +
        "<figcaption>243 × 36: first row 243 × 6 = 1458. Second row 243 × 30 = 7290. "
        "1458 + 7290 = 8748.</figcaption></figure>" +
        ex("Estimate to check", "Is 243 × 36 = 8748 reasonable?",
           "Round 243 to the nearest hundred and 36 to the nearest ten: 200 × 40 = 8000. "
           "8748 is close to 8000, so it makes sense. 2187 (no 0 in the second row) is far off.", "Yes") +
        "<h2>Word problems: draw a model</h2>"
        "<p>“4 times as many” means 4 equal units. Find 1 unit, then multiply.</p>"
        "<figure class='sn-fig'>" + model +
        "<figcaption>Siti has 325 stickers. Wei Ming has 4 times as many. 1 unit = 325, so 4 units = 4 × 325 = 1300."
        "</figcaption></figure>" +
        ex("How many more?", "Siti has 325 stickers. Wei Ming has 4 times as many. How many more stickers does Wei Ming have?",
           "Wei Ming has 4 units and Siti has 1 unit, so the difference is 3 units: 3 × 325 = 975.", "975 stickers") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the 0 in the second row (38 × 24 = 152 + 76 = 228)", "The second row is × 20, so write 0 first: 760"],
            ["Not adding the renamed digit (2367 × 4 = 8248)", "Write it small above the next column and add it: 6 × 4 + 2 = 26"],
            ["Adding before multiplying ((6 + 2) × 4 = 32)", "Multiply first, then add: 6 × 4 + 2 = 26"],
            ["Only two parts in the area model (23 × 14 = 200 + 12)", "There are four parts: 200 + 30 + 80 + 12 = 322"],
        ])
    )


FAQ = [
    {"q": "What multiplication is taught in P4 maths?",
     "a": "In Primary 4, students multiply up to a 4-digit number by a 1-digit number and up to a 3-digit number by a 2-digit number, such as 2367 × 4 and 243 × 36. They also estimate to check their answers and solve word problems."},
    {"q": "How do I explain 2-digit by 2-digit multiplication to my child?",
     "a": "Start with the area model: split both numbers into tens and ones and add the four parts, so 23 × 14 = 200 + 30 + 80 + 12 = 322. Then show the algorithm, where each row is one row of the area model."},
    {"q": "What is the most common mistake in P4 multiplication?",
     "a": "Forgetting the 0 at the start of the second row. In 38 × 24 the 2 means 2 tens, so the row is 38 × 20 = 760, not 76. Not adding the renamed digit is the next most common mistake."},
    {"q": "Is multiplication by 2-digit numbers in the MOE Primary 4 syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics syllabus has the multiplication algorithm up to 4 digits by 1 digit and up to 3 digits by 2 digits in Primary 4. These skills are used in every later topic and in the PSLE."},
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


def mark_large(u, pattern):
    """Tag column, area and bar model pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(64804)
    P = People(rnd)
    seen = set()
    sets = [set_4x1(rnd, P), set_2x2(rnd, seen, P), set_3x2(rnd, seen, P), set_estimate(rnd, P), set_story(rnd, P)]
    keys = set()
    for s in sets:
        if s["title"] != "Word problems with bar models":
            rnd.shuffle(s["items"])
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(plain(x) for x in it["c"])) == 4, it
            assert it["e"], it["q"]
            assert it["q"].count("<svg") <= 1, it["q"]
            k = plain(it["q"])
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": SLUG, "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Multiplication",
        "seo_title": "P4 Multiplication Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Multiplication",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Four Operations",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Multiplication algorithm up to 4 digits by 1 digit and up to 3 digits by 2 digits",
        "meta_desc": "Free P4 multiplication worksheets: 4-digit × 1-digit, 2-digit × 2-digit and 3-digit × 2-digit, renaming, estimates and bar models. 100 questions with answers.",
        "key_big": "Multiply from the ones, add the renamed digit after multiplying, and start the second row with 0.",
        "key_sub": "243 × 36: 243 × 6 = 1458, 243 × 30 = 7290, and 1458 + 7290 = 8748.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "([0-9]+ times [0-9]+|area model with|bar model)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
