# -*- coding: utf-8 -*-
"""
UK Year 5 Maths: Multiplication (National Curriculum in England, Multiplication and division)
  python3 tools/gen_uk_maths_y5_multiplication.py
Mental multiplication from known facts, short multiplication (up to 4 digits × 1 digit) and
long multiplication (2-, 3- and 4-digit × 2-digit), then word problems with rates and scaling.
Every product and every wrong answer is computed here (wrong answers = real pupil mistakes).
HTML attributes use single quotes (no backslashes in the JSON).
Numbers 1,000 and above are written with commas in text (not inside the column layouts).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd, zero_ok=False):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1 if c.startswith(("Yes", "No")) else 0].lstrip("£")
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


# ------------------------------------------------------------ short multiplication figure
def short_svg(a, d, ans="", ex=None, label=None):
    """Short multiplication in columns, ones lined up on the right.
    ans: answer row as a string; '?' = red dashed box. ex: {column from the right: exchanged digit}."""
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
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%s'><g font-family='monospace'>%s</g></svg>" % (W, H, W, H, lab, "".join(s)))


def carry_list(a, d):
    """Exchanged digit going INTO each column (index = column from the right)."""
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
    """Long multiplication in columns, ones lined up on the right (no commas, as pupils write it).
    rows = list of (sign, text) or (sign, text, nz): nz = number of place-holder zeros at the end (drawn green).
    sign 'ex' = a row of small exchanged digits: text is a dict {place: digit}.
    text '[?]' = a red dashed box across the row; a '?' inside a number = one red missing digit.
    rules = row indexes with a line under them. notes = short notes to the right of the rows (lesson figures)."""
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
                if ch == "?":
                    cx = right - cw * (slot + 0.5)
                    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                             "stroke-width='2' stroke-dasharray='4 2'/>" % (cx - cw * 0.42, y - fs * 0.84, cw * 0.84, fs * 0.96, RED))
                    col = RED
                else:
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
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%s'><g font-family='monospace'>%s</g></svg>" % (W, H, W, H, label, "".join(s)))


def col_problem(a, b):
    return column_svg([("", str(a)), ("×", str(b))], [1], "%d times %d written as long multiplication" % (a, b))


def pp_rows(a, b):
    """The rows of long multiplication, ones row first: (digit, place, value)."""
    return [(d, i, a * d * 10 ** i) for i, d in enumerate(digits(b))]


def work_rows(a, b, box=None, total=True, qdigit=None, rowq=None):
    """Rows for the full written work. box = index of the row shown as [?]; box='sum' hides the total.
    qdigit = place of the total shown as '?'. rowq = (row index, place) shown as '?' in that row."""
    pr = pp_rows(a, b)
    rows = [("", str(a)), ("×", str(b))]
    for k, (d, i, v) in enumerate(pr):
        sg = "+" if k == len(pr) - 1 else ""
        if box == k:
            rows.append((sg, "[?]"))
        elif rowq and rowq[0] == k:
            ds = list(str(v))
            ds[len(ds) - 1 - rowq[1]] = "?"
            rows.append((sg, "".join(ds), i))
        else:
            rows.append((sg, str(v), i))
    rules = [1]
    if total:
        rules.append(len(rows) - 1)
        if box == "sum":
            rows.append(("", "[?]"))
        elif qdigit is not None:
            ds = list(str(a * b))
            ds[len(ds) - 1 - qdigit] = "?"
            rows.append(("", "".join(ds)))
        else:
            rows.append(("", str(a * b)))
    return rows, rules


def work_svg(a, b, **kw):
    rows, rules = work_rows(a, b, **kw)
    return column_svg(rows, rules, "%d times %d as long multiplication" % (a, b))


# ------------------------------------------------------------ explanations
def steps_short(a, d):
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
            out.append("%s: %s = %d. Write %d, exchange %d." % (cap(PLACE[i]), ex_, p, p % 10, p // 10))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def steps_1d(a, d):
    """Inside one row of long multiplication."""
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        if i == len(ds) - 1 or p < 10:
            out.append("%s = %d, write %d" % (ex_, p, p))
        else:
            out.append("%s = %d, write %d, exchange %d" % (ex_, p, p % 10, p // 10))
        c = p // 10 if i < len(ds) - 1 else 0
    return "; ".join(out)


def row_text(a, d, i):
    v = a * d * 10 ** i
    if i == 0:
        return "%s × %d = %s" % (f(a), d, f(v))
    return "%s × %s = %s (write the place-holder 0, then %s × %d = %s)" % (f(a), f(d * 10 ** i), f(v), f(a), d, f(a * d))


def steps(a, b, detail=None):
    """Long multiplication. detail = row index whose digit-by-digit work is shown too."""
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


# ------------------------------------------------------------ typical mistakes
def mult_row(a, d, mode="ok", k=None):
    """a × d (one digit), done with a typical mistake.
    nocarry: forget every exchanged digit. skip: forget the one made in place k.
    cfirst: add the exchanged digit BEFORE multiplying. zero_d: think 0 × d = d."""
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
    """Real mistakes for short multiplication a × d, the most common first."""
    n = len(str(a))
    out = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst")]
    out += [mult_row(a, d, "skip", k) for k in range(n - 1)]
    out += [a * d * 10, a * (d - 1), a + d]
    return out


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


def one_digit(a, b):
    return a * (b % 10)


def add_cols(nums, drop=None, extra=None):
    """Column addition. drop='all': forget every exchanged digit; int k: forget the one from place k.
    extra = int k: exchange 1 too many out of place k. The last column is written whole."""
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
    """Only ones × ones and tens × tens (2-digit × 2-digit)."""
    return (a // 10) * (b // 10) * 100 + (a % 10) * (b % 10)


def cands(a, b, rnd):
    """Real mistakes for long multiplication a × b, the most common first."""
    pr = pp_rows(a, b)
    out = [no_zero(a, b)]
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"), add_cols([v for d, i, v in pr], drop="all")]
    more += [total_with(a, b, "nocarry", only=j) for j in range(len(pr))]
    if len(str(a)) == 2:
        more.append(two_pp(a, b))
    rnd.shuffle(more)
    return out + more + [one_digit(a, b), total_with(a, b, "skip", k=0), total_with(a, b, "skip", k=1)]


# ------------------------------------------------------------ set 1: mental multiplication
def set_mental(rnd):
    its = []

    def add(q, ans, wrong, e):
        its.append(mcq(q, f(ans), [f(w) for w in wrong], e, rnd))

    # multiples of 10, 100, 1,000 × a one-digit number
    for t, z, d, nb in [(6, 1, 7, 8), (4, 2, 6, 5), (9, 2, 8, 7), (5, 1, 8, None), (3, 3, 7, 8)]:
        a = t * 10 ** z
        ans = a * d
        wrong = [t * d * 10 ** (z - 1) if t * d % 10 else t * d * 10 ** (z + 1),   # one zero too few / too many
                 t * d * 10 ** (z + 1) if t * d % 10 else t * d * 10 ** (z - 1)]
        wrong.append(t * nb * 10 ** z if nb else a + d)
        assert ans == t * d * 10 ** z
        zw = {1: "tens", 2: "hundreds", 3: "thousands"}[z]
        e = "%s is %d %s. %d × %d = %d, so %d %s × %d = %d %s = %s." % (
            f(a), t, zw, t, d, t * d, t, zw, d, t * d, zw, f(ans))
        if t * d % 10 == 0:
            e += " The 0 in %d is part of the fact, so do not drop it." % (t * d)
        add("What is %s × %d?" % (f(a), d), ans, wrong, e)
    # two multiples of 10
    for x, y in [(70, 80), (30, 400)]:
        ans = x * y
        bx, by = x // 10, y // 10 ** (len(str(y)) - 1)
        nz_ = len(str(x)) - 1 + len(str(y)) - 1
        add("What is %s × %s?" % (f(x), f(y)), ans, [ans // 10, ans * 10, x + y],
            "Use %d × %d = %d, then put back all %d zeros (one in %d%s): %s × %s = %s." % (
                bx, by, bx * by, nz_, x, ", two in %d" % y if y >= 100 else ", one in %d" % y, f(x), f(y), f(ans)))
    # change the order to make 100 or 10
    for p, q_, r, wrong, how in [
            (25, 4, 9, [225, 9000, 38], "25 × 4 = 100, then 100 × 9 = 900"),
            (4, 19, 25, [76, 19000, 190], "change the order: 4 × 25 = 100, then 100 × 19 = 1,900"),
            (5, 17, 2, [85, 1700, 24], "change the order: 5 × 2 = 10, then 10 × 17 = 170"),
            (2, 36, 5, [72, 3600, 180], "change the order: 2 × 5 = 10, then 10 × 36 = 360")]:
        ans = p * q_ * r
        assert str(ans) in how.replace(",", "")
        add("What is %d × %d × %d?" % (p, q_, r), ans, wrong,
            "You can multiply in any order. %s. Multiply all three numbers, not just two." % cap(how))
    # doubling and halving
    add("Double, then double again, to find 37 × 4.", 148, [74, 296, 1480],
        "× 4 is double, double. Double 37 = 74. Double 74 = 148. Doubling only once gives 74; three times gives 296.")
    add("Multiply by 10, then halve, to find 46 × 5.", 230, [460, 23, 2300],
        "× 5 is the same as × 10, then halve. 46 × 10 = 460. Half of 460 = 230.")
    add("What is 16 × 25? (Hint: halve one number and double the other.)", 400, [800, 200, 4000],
        "Halve 16 and double 25: 16 × 25 = 8 × 50 = 4 × 100 = 400. If you double one number you must halve the other.")
    add("What is 18 × 50?", 900, [1800, 90, 9000],
        "× 50 is the same as × 100, then halve. 18 × 100 = 1,800. Half of 1,800 = 900.")
    assert 12 * 7 == 84
    add("12 × 7 = 84. What is 24 × 7?", 168, [42, 336, 91],
        "24 is double 12, so 24 × 7 is double 84 = 168.")
    # near a multiple of 10
    add("What is 19 × 6? (Hint: 19 is 1 less than 20.)", 114, [119, 126, 120],
        "19 × 6 = 20 × 6 − 1 × 6 = 120 − 6 = 114. Take away one 6, not 1.")
    add("What is 99 × 7?", 693, [699, 707, 700],
        "99 × 7 = 100 × 7 − 7 = 700 − 7 = 693. Take away one 7, not 1.")
    # using a known fact
    assert 12 * 9 == 108 and 8 * 25 == 200
    add("12 × 9 = 108. What is 120 × 9?", 1080, [108, 10800, 117],
        "120 is 10 times 12, so the answer is 10 times 108: 1,080.")
    add("8 × 25 = 200. What is 8 × 24?", 192, [199, 175, 208],
        "24 is one less than 25, so take away one 8: 200 − 8 = 192.")
    assert len(its) == 20
    rnd.shuffle(its)
    return {"title": "Mental multiplication from known facts", "items": its}


# ------------------------------------------------------------ set 2: short multiplication
def pick_short(rnd, seen, n, zero=None):
    while True:
        a, d = rnd.randint(10 ** (n - 1) + 1, 10 ** n - 1), rnd.randint(3, 9)
        ds = digits(a)
        if (a, d) in seen:
            continue
        if zero is not None:
            # a 0 in place `zero`, and an exchange lands on it
            if ds[zero] != 0 or 0 in ds[:zero] + ds[zero + 1:] or ds[zero - 1] * d < 10:
                continue
        elif 0 in ds or carries(a, d) < n - 1 or len(set(ds)) < n - 1:
            continue
        seen.add((a, d))
        return a, d


def short_item(a, d, rnd, col):
    q = (fig(short_svg(a, d)) + "Use short multiplication.") if col else "Calculate %s × %d" % (f(a), d)
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
        e = steps_short(a, d) + " 0 × %d = 0, but you still add the exchanged %d." % (d, c)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if z == 1 else "Calculate %s × %d" % (f(a), d)
        its.append(mcq(q, f(a * d), [f(v) for v in wrong], e, rnd))
    # a missing digit in the answer (4-digit × 1-digit)
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
        e = ("%s column: %d × %d = %d, then add the exchanged %d: %d. Write %d%s. "
             % (cap(PLACE[pos]), x, d, x * d, c, p, p if last else p % 10,
                ", exchange %d" % (p // 10) if p >= 10 and not last else ""))
        if last:
            e += "The ? is the %s digit, %d. " % (PLACE[pos], right)
        e += "Full working: " + steps_short(a, d)
        its.append(mcq(fig(short_svg(a, d, "".join(show), ex)) + "What digit goes in the box marked ?",
                       str(right), [str(v) for v in wr], e, rnd, zero_ok=True))
        k += 1
    rnd.shuffle(its)
    return {"title": "Short multiplication: 3- and 4-digit × 1-digit", "items": its}


# ------------------------------------------------------------ long multiplication: choosing numbers
def pick(rnd, seen, na, add_reg=0, bmax=99):
    """a has na digits (no 0), b is 2-digit (digits 2-9, different, b <= bmax). Every row exchanges."""
    while True:
        a = rnd.randint(10 ** (na - 1) + 1, 10 ** na - 1)
        bd = rnd.sample(range(2, 10), 2)
        b = bd[0] * 10 + bd[1]
        da = digits(a)
        if b > bmax or 0 in da or len(set(da)) < len(da) - 1 or (a, b) in seen:
            continue
        if any(carries(a, d) == 0 for d in digits(b)):
            continue
        if len(add_carries([v for d, i, v in pp_rows(a, b)])) < add_reg:
            continue
        seen.add((a, b))
        return a, b


def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Use long multiplication.") if col else "Calculate %s × %d" % (f(a), b)
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b, detail=1 if len(str(a)) > 2 else None), rnd)


def box_row_item(a, b, k, rnd):
    d, i, v = pp_rows(a, b)[k]
    q = fig(work_svg(a, b, box=k)) + "What number goes in the dashed box?"
    if i == 0:
        wrong = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", k=0),
                 mult_row(a, d, "skip", k=1), v * 10]
        e = "Row 1 is %s × %d: %s. So the row is %s." % (f(a), d, steps_1d(a, d), f(v))
    else:
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
    e = ("Add the two rows with column addition, and add every exchanged digit: %s = %s."
         % (" + ".join(f(v) for v in pr), f(a * b)))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


WHAT = ["Forgot the place-holder zero", "Did not add an exchanged digit", "Added the two rows wrongly",
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
        why = "Row 1 should be %s, not %s: %s. The exchanged digits were not added." % (f(v0), f(r0), steps_1d(a, d0))
    assert got != a * b
    why += " The correct answer is %s." % f(a * b)
    q = (fig(column_svg(rows, [1, 3], "%d times %d: working with a mistake" % (a, b))) +
         "%s got %s × %d = %s. What mistake did %s make?" % (n, f(a), b, f(got), he))
    ans = WHAT[kind]
    return mcq(q, ans, [w for w in WHAT if w != ans], why, rnd)


# ------------------------------------------------------------ set 3: long multiplication 2-digit × 2-digit
def set_2x2(rnd, seen, P):
    its = []
    for i in range(8):
        a, b = pick(rnd, seen, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 2)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(3):
        a, b = pick(rnd, seen, 2)
        its.append(box_row_item(a, b, 0, rnd))
    for k in range(3):
        a, b = pick(rnd, seen, 2)
        o, t = b % 10, b // 10
        ta, oa = a // 10 * 10, a % 10
        q = fig(work_svg(a, b))
        if k % 2 == 0:
            v = a * t * 10
            right = "%d × %d" % (a, t * 10)
            wrong = ["%d × %d" % (a, t), "%d × %d" % (ta, t * 10), "%d × %d" % (oa, t * 10)]
            q += "Which calculation gives the second row, %s?" % f(v)
            e = ("The %d in %d means %d tens, so the second row is %d × %d = %s. That is why it starts with a place-holder 0. "
                 "%d × %d would be only %d." % (t, b, t, a, t * 10, f(v), a, t, a * t))
        else:
            v = a * o
            right = "%d × %d" % (a, o)
            wrong = ["%d × %d" % (oa, o), "%d × %d" % (ta, o), "%d × %d" % (a, o * 10)]
            q += "Which calculation gives the first row, %s?" % f(v)
            e = ("The first row multiplies all of %d by the ones digit, %d: %d × %d = %s. "
                 "Then the second row is %d × %d = %s." % (a, o, a, o, f(v), a, t * 10, f(a * t * 10)))
        its.append(mcq(q, right, wrong, e, rnd))
    for kind in (0, 1):
        a, b = pick(rnd, seen, 2)
        its.append(what_item(a, b, kind, rnd, P))
    rnd.shuffle(its)
    return {"title": "Long multiplication: 2-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 4: 3- and 4-digit × 2-digit, missing digits
def missing_total_item(a, b, rnd):
    pr = [v for d, i, v in pp_rows(a, b)]
    tot = a * b
    for k in range(1, len(str(tot)) - 1):
        cin = sum(v % 10 ** k for v in pr) // 10 ** k
        col = [v // 10 ** k % 10 for v in pr]
        S = sum(col) + cin
        right = S % 10
        if cin == 0 or S < 10 or 0 in col:
            continue
        wrong = [(S - cin) % 10, S // 10] + [(S - x) % 10 for x in col] + [(S + 1) % 10]
        ws = []
        for w in wrong:
            if w != right and w not in ws:
                ws.append(w)
        if len(ws) < 3:
            continue
        e = ("Add the %s column: %s = %d, plus %d exchanged from the %s = %d. Write %d and exchange %d. "
             "The full answer is %s."
             % (PLACE[k], " + ".join(str(x) for x in col), sum(col), cin, PLACE[k - 1], S, right, S // 10, f(tot)))
        q = fig(column_svg(*work_rows(a, b, qdigit=k), label="%d times %d as long multiplication" % (a, b))) + \
            "What digit goes in the box marked ?"
        return mcq(q, str(right), [str(w) for w in ws], e, rnd, zero_ok=True)
    return None


def missing_row_item(a, b, j, rnd):
    d, i, v = pp_rows(a, b)[j]
    ds = digits(a)
    c = 0
    spots = []
    for p, x in enumerate(ds):
        prod = x * d + c
        if c and p < len(ds) - 1:
            spots.append((p, x, c, prod))
        c = prod // 10
    for p, x, c, prod in spots:
        place = p + i
        right = v // 10 ** place % 10
        cand = [(x * d) % 10, mult_row(a, d, "cfirst") * 10 ** i // 10 ** place % 10,
                (x * d + c) // 10 % 10, (x + c) * d % 10, (right + 1) % 10]
        ws = []
        for w in cand:
            if w != right and w not in ws:
                ws.append(w)
        if len(ws) < 3:
            continue
        rows, rules = work_rows(a, b, total=False, rowq=(j, place))
        q = fig(column_svg(rows, rules, "%d times %d as long multiplication" % (a, b))) + \
            "What digit goes in the box marked ?"
        e = ("Row %d is %s × %s. The ? comes from %d × %d = %d, plus the exchanged %d = %d. Write %d. "
             "Full row: %s%s. Row %d is %s." % (j + 1, f(a), f(d * 10 ** i), x, d, x * d, c, prod, right,
                                           "place-holder 0, then " if i else "", steps_1d(a, d), j + 1, f(v)))
        return mcq(q, str(right), [str(w) for w in ws], e, rnd, zero_ok=True)
    return None


def set_big(rnd, seen):
    its = []
    for i in range(6):
        a, b = pick(rnd, seen, 3)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for i in range(4):
        a, b = pick(rnd, seen, 4, bmax=39)
        its.append(compute_item(a, b, rnd, i % 2 == 1))
    for _ in range(3):
        a, b = pick(rnd, seen, 3, add_reg=2)
        its.append(sum_box_item(a, b, rnd))
    n = 0
    while n < 4:
        a, b = pick(rnd, seen, 3)
        it = missing_row_item(a, b, n % 2, rnd)
        if it:
            its.append(it)
            n += 1
    n = 0
    while n < 3:
        a, b = pick(rnd, seen, 3 if n < 2 else 4, add_reg=2, bmax=99 if n < 2 else 39)
        it = missing_total_item(a, b, rnd)
        if it:
            its.append(it)
            n += 1
    rnd.shuffle(its)
    return {"title": "Long multiplication: 3- and 4-digit × 2-digit, missing digits", "items": its}


# ------------------------------------------------------------ set 5: word problems
def money(v):
    return "£" + f(v)


# (question, a, b, unit, lead). unit '£' = money, else 'x unit'. {n} {he} {his}.
STORIES = [
    ("A gardener is paid £12 an hour. She works for 15 hours this week. How much does she earn?",
     12, 15, "£", "15 hours × £12"),
    ("A box holds 144 pencils. The school office orders 23 boxes. How many pencils is that?",
     144, 23, "pencils", "23 boxes × 144 pencils"),
    ("A train travels 125 km every hour. How far does it travel in 3 hours?",
     125, 3, "km", "3 hours × 125 km"),
    ("A printer prints 36 pages a minute. How many pages does it print in 25 minutes?",
     36, 25, "pages", "25 minutes × 36 pages"),
    ("A dripping tap wastes 45 ml of water every hour. How much water does it waste in 24 hours?",
     45, 24, "ml", "24 hours × 45 ml"),
    ("A glass holds 250 ml. A jug holds 6 times as much. How much does the jug hold?",
     250, 6, "ml", "6 times as much, so 250 ml × 6"),
    ("A crate holds 24 bottles of milk. The school orders 35 crates this term. How many bottles is that?",
     24, 35, "bottles", "35 crates × 24 bottles"),
    ("A school trip costs £8 for each pupil. 316 pupils go. How much money is collected?",
     316, 8, "£", "316 pupils × £8"),
    ("The school hall has 27 rows of chairs with 18 chairs in each row. How many chairs are there?",
     27, 18, "chairs", "27 rows × 18 chairs"),
    ("A theatre sells 1,236 tickets for a show at £15 each. How much money does it take?",
     1236, 15, "£", "1,236 tickets × £15"),
    ("{n} cycles 18 km every day for 14 days. How far does {he} cycle altogether?",
     18, 14, "km", "14 days × 18 km"),
    ("A bakery bakes 2,350 bread rolls every day. How many rolls does it bake in 6 days?",
     2350, 6, "rolls", "6 days × 2,350 rolls"),
    ("A lorry carries 32 crates. Each crate has a mass of 145 kg. What is the total mass of the crates?",
     145, 32, "kg", "32 crates × 145 kg"),
    ("A family uses 165 litres of water a day. How much water do they use in a week?",
     165, 7, "litres", "7 days × 165 litres"),
    ("A swimming coach is paid £45 an hour. He teaches for 26 hours this half-term. How much is he paid?",
     45, 26, "£", "26 hours × £45"),
]


def set_story(rnd, P):
    its = []
    for t, a, b, unit, lead in STORIES:
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his)
        fm = money if unit == "£" else (lambda v, u=unit: "%s %s" % (f(v), u))
        if b < 10:
            wrong = cands_1d(a, b)
            work = steps_short(a, b)
            e = "%s: %s × %d. %s" % (cap(lead), f(a), b, work) if "times" in lead else \
                "Equal groups: %s, so multiply %s × %d. %s" % (lead, f(a), b, work)
        else:
            wrong = cands(a, b, rnd)
            e = "Equal groups: %s, so multiply %s × %d. " % (lead, f(a), b) + steps(a, b)
        its.append(mcq(q, fm(a * b), [fm(v) for v in wrong], e, rnd))

    # scaling: a recipe for more people
    assert 175 * 3 == 525
    its.append(mcq("A recipe for 4 people uses 175 g of flour. How much flour is needed for 12 people?", "525 g",
                   ["2,100 g", "700 g", "315 g"],
                   "12 people is 3 times as many as 4 people (4 × 3 = 12), so use 3 times as much flour: "
                   "175 × 3 = 525 g. Do not multiply by 12: the recipe is for 4 people, not 1.", rnd))
    # scaling by a simple fraction
    assert 2400 // 4 == 600
    its.append(mcq("A rabbit has a mass of 2,400 g. A guinea pig is <span class='fr'><span class='fn'>1</span>"
                   "<span class='fd'>4</span></span> as heavy. What is the mass of the guinea pig?", "600 g",
                   ["9,600 g", "1,200 g", "1,800 g"],
                   "“<span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span> as heavy” means "
                   "divide into 4 equal parts: 2,400 ÷ 4 = 600 g. Multiplying by 4 gives 9,600 g, which is heavier, not lighter.", rnd))
    # two-step problems
    assert 28 * 7 + 3 * 15 == 241 and mult_row(28, 7, "nocarry") + 45 == 191
    its.append(mcq("A school buys 28 reading books at £7 each and 3 dictionaries at £15 each. What is the total cost?",
                   "£241", ["£196", "£191", "£211"],
                   "Books: 28 × £7 = £196 (8 × 7 = 56, write 6, exchange 5; 2 × 7 + 5 = 19). "
                   "Dictionaries: 3 × £15 = £45. Total: £196 + £45 = £241.", rnd))
    assert 6 * 49 - (250 + 22) == 22
    its.append(mcq("A school books 6 coaches with 49 seats each. 250 pupils and 22 adults go on the trip. "
                   "How many seats are empty?", "22 seats", ["294 seats", "44 seats", "272 seats"],
                   "Step 1: seats: 6 × 49 = 294 (9 × 6 = 54, write 4, exchange 5; 4 × 6 + 5 = 29). "
                   "Step 2: people: 250 + 22 = 272. Step 3: empty seats: 294 − 272 = 22.", rnd))
    # estimate to check
    n, he, his = P.next()
    a, b = 286, 34
    claim = no_zero(a, b)
    assert claim == 2002 and a * b == 9724
    its.append(mcq("%s says 286 × 34 = %s. Estimate to check. Is %s answer sensible?" % (n, f(claim), his),
                   "No, it should be about 9,000",
                   ["Yes, it is close to 9,000", "Yes, it is close to 900", "No, it should be about 90,000"],
                   "286 rounds to 300 and 34 rounds to 30. 300 × 30 = 9,000. %s is far from 9,000, so it cannot be right. "
                   "%s forgot the place-holder 0 in the second row. The correct answer is 9,724." % (f(claim), n), rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems: rates, scaling and two steps", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def row_exchanges(a, d, shift):
    out, c = {}, 0
    for i, x in enumerate(digits(a)[:-1]):
        c = (x * d + c) // 10
        if c:
            out[i + 1 + shift] = c
    return out


def add_exchanges(nums):
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
    add(("ex", row_exchanges(a, d0, 0)), "exchanged")
    add(("+", str(v1), 1), "%s × %d" % (f(a), d1 * 10))
    add(("ex", row_exchanges(a, d1, 1)), "exchanged")
    rule2 = len(rows) - 1
    add(("", str(a * b)), "add the rows")
    add(("ex", add_exchanges([v0, v1])), "exchanged when adding")
    return column_svg(rows, [1, rule2], label, notes=notes, big=True)


def body_html():
    assert 4736 * 6 == 28416 and 38 * 24 == 912 and 243 * 36 == 8748
    return (
        "<h2>Mental multiplication: use facts you know</h2>"
        "<p>Many big multiplications are a times table fact in disguise. 60 is 6 tens, so 60 × 7 is 6 × 7 = 42 tens = <b>420</b>.</p>"
        "<p>Other quick ways: <b>change the order</b> (25 × 7 × 4 = 25 × 4 × 7 = 100 × 7 = 700), "
        "<b>double and halve</b> (16 × 25 = 8 × 50 = 400), and <b>× 5 is × 10, then halve</b> (46 × 5 = 460 ÷ 2 = 230).</p>"
        "<h2>Short multiplication: up to 4 digits × 1 digit</h2>"
        "<p>Line up the ones. Start with the ones column. When a product is 10 or more, write the ones digit and "
        "<b>exchange</b> the tens into the next column as a small digit. <b>Multiply first, then add</b> the exchanged digit.</p>"
        "<figure class='sn-fig'>" + short_svg(4736, 6, "28416", carry_list(4736, 6), "4736 times 6 as short multiplication") +
        "<figcaption>4,736 × 6: 6 × 6 = 36, write 6, exchange 3. 3 × 6 + 3 = 21, write 1, exchange 2. "
        "7 × 6 + 2 = 44, write 4, exchange 4. 4 × 6 + 4 = 28. Answer: 28,416.</figcaption></figure>"
        "<h2>Long multiplication: × a 2-digit number</h2>"
        "<p>Make <b>one row for each digit</b>. Row 1 multiplies by the ones digit. Row 2 multiplies by the tens digit, "
        "so it starts with a <b>place-holder zero</b> (green). Then add the two rows.</p>"
        "<figure class='sn-fig'>" + lesson_fig(38, 24, "38 times 24 as long multiplication") +
        "<figcaption>38 × 24: row 1 is 38 × 4 = 152. Row 2 is 38 × 20: write 0, then 38 × 2 = 76, so 760. "
        "152 + 760 = 912.</figcaption></figure>" +
        ex("3-digit × 2-digit", "243 × 36 = ?",
           "Row 1: 243 × 6 = 1,458. Row 2: write 0, then 243 × 3 = 729, so 7,290. Add: 1,458 + 7,290 = 8,748. "
           "Check: 243 × 36 is about 200 × 40 = 8,000.", "8,748") +
        "<h2>Rates and scaling</h2>"
        "<p>A <b>rate</b> is an amount for each one: £12 an hour for 15 hours is 15 × £12 = £180. "
        "<b>Scaling</b> means making something a number of times bigger: a jug that holds 6 times as much as a 250 ml glass "
        "holds 250 × 6 = 1,500 ml.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Losing or adding a zero (60 × 7 = 42 or 4,200)", "60 is 6 tens: 6 × 7 = 42 tens = 420"],
            ["No place-holder zero (38 × 24 = 152 + 76 = 228)", "Row 2 is × 20, so write 0 first: 760"],
            ["Forgetting an exchanged digit (38 × 4 = 122)", "Write it small and add it: 3 × 4 + 3 = 15, so 152"],
            ["Adding the exchanged digit first", "Multiply first, then add: 3 × 4 + 3 = 15, not (3 + 3) × 4"],
            ["Multiplying by only one digit (38 × 24 = 152)", "Make a row for the ones and a row for the tens"],
        ])
    )


FAQ = [
    {"q": "What multiplication do Year 5 children learn?",
     "a": "They multiply numbers up to 4 digits by a one-digit number with short multiplication, and by a two-digit number with long multiplication. They also multiply mentally using known facts, such as 60 × 7 = 420."},
    {"q": "How do you teach long multiplication in Year 5?",
     "a": "Start with 2-digit × 2-digit. Multiply by the ones digit to make row 1, write a place-holder zero and multiply by the tens digit to make row 2, then add the rows: 38 × 24 = 152 + 760 = 912."},
    {"q": "What is the difference between short and long multiplication?",
     "a": "Short multiplication is for multiplying by a one-digit number and gives one row. Long multiplication is for a two-digit number: you make one row for each digit and then add the rows."},
    {"q": "Why do you put a zero in long multiplication?",
     "a": "In 38 × 24 the 2 means 2 tens, so row 2 is 38 × 20, not 38 × 2. The place-holder zero in the ones column makes the row 760 instead of 76."},
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
    rnd = random.Random(5506)
    P = People(rnd)
    seen = set()
    sets = [set_mental(rnd), set_short(rnd, seen), set_2x2(rnd, seen, P), set_big(rnd, seen), set_story(rnd, P)]
    balance(sets, rnd)
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
        "country": "uk", "subject": "maths", "grade": "year-5", "slug": "multiplication", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication",
        "seo_title": "Year 5 Multiplication Worksheets: Short and Long Multiplication, Mental Methods",
        "short_title": "Multiplication",
        "domain": "Multiplication and division",
        "standard_code": "Year 5: Multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply numbers up to 4 digits by a one- or two-digit number using a formal written method, including long multiplication for two-digit numbers; multiply and divide numbers mentally drawing upon known facts; solve problems involving multiplication and division, including scaling by simple fractions and problems involving simple rates.",
        "meta_desc": "Free Year 5 maths worksheets on multiplication: mental methods from known facts, short multiplication of 4-digit numbers, long multiplication by 2-digit numbers, missing digits, and word problems with rates and scaling. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Multiply by one digit at a time. For a 2-digit number, make two rows and start row 2 with a place-holder zero.",
        "key_sub": "38 × 24 = 38 × 4 + 38 × 20 = 152 + 760 = 912. Use known facts for mental work: 60 × 7 is 6 × 7 = 42 tens = 420.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag column pictures so the digits print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "[0-9]+ times [0-9]+")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
