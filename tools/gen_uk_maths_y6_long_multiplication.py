# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Long multiplication (National Curriculum in England, Addition, subtraction, multiplication and division)
  python3 tools/gen_uk_maths_y6_long_multiplication.py
Every product and every wrong answer is computed here (wrong answers = real pupil mistakes).
HTML attributes use single quotes (no backslashes in the JSON).
Numbers 1,000 and above are written with commas in text (not inside the column layouts).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
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
        lead = c.split(" ")[-1 if c.startswith("about") else 0].lstrip("£")
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


# ------------------------------------------------------------ column figure
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
def steps_1d(a, d):
    """Inside one row: multiply digit by digit, then add the exchanged digit."""
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
    """detail = row index whose digit-by-digit work is shown too."""
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
    """One row, a × d, done with a typical mistake.
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


def total_with(a, b, mode, only=None, k=None):
    """Whole product where the rows (or only row `only`) are done with mode."""
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
    """Multiplied by the ones digit only."""
    return a * (b % 10)


def add_cols(nums, drop=None, extra=None):
    """Column addition. drop=None: correct; 'all': forget every exchanged digit; int k: forget the one from place k.
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
    """Places (not the last column) where adding the rows exchanges."""
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
    """Real mistakes for a × b, the most common first."""
    pr = pp_rows(a, b)
    out = [no_zero(a, b)]
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"),
            add_cols([v for d, i, v in pr], drop="all")]
    more += [total_with(a, b, "nocarry", only=j) for j in range(len(pr))]
    if len(str(a)) == 2:
        more.append(two_pp(a, b))
    rnd.shuffle(more)
    return out + more + [one_digit(a, b), total_with(a, b, "skip", k=0), total_with(a, b, "skip", k=1)]


def carries(a, d):
    """Exchanges inside one row (the last digit's product is written whole, so it does not count)."""
    c, n = 0, 0
    for x in digits(a)[:-1]:
        p = x * d + c
        c = p // 10
        n += 1 if c else 0
    return n


# ------------------------------------------------------------ choosing numbers
def pick(rnd, seen, na, zero=None, add_reg=0):
    """a has na digits, b is 2-digit (digits 2-9, different). Every row exchanges at least once.
    zero='in': a has one 0 inside; zero='end': a ends in 0.
    add_reg = how many exchanges adding the rows must have at least."""
    while True:
        a = rnd.randint(10 ** (na - 1) + 1, 10 ** na - 1)
        bd = rnd.sample(range(2, 10), 2)
        b = bd[0] * 10 + bd[1]
        da = digits(a)
        if zero == "in":
            if da[0] == 0 or da[-1] == 0 or da[1:-1].count(0) != 1:
                continue
            z = da.index(0)
            if not any(da[z - 1] * d >= 10 for d in digits(b)):        # an exchange must land on the 0
                continue
        elif zero == "end":
            if da[0] != 0 or 0 in da[1:]:
                continue
        elif 0 in da:
            continue
        if len(set(da)) < len(da) - 1:
            continue
        if (a, b) in seen:
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
    """The k-th row is a dashed box."""
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


# ------------------------------------------------------------ set 1: 2-digit × 2-digit
def set_2x2(rnd, seen):
    its = []
    for i in range(8):
        a, b = pick(rnd, seen, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 2)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(4):
        a, b = pick(rnd, seen, 2)
        its.append(box_row_item(a, b, 0, rnd))
    for k in range(4):
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
    rnd.shuffle(its)
    return {"title": "Long multiplication: 2-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 2: 3-digit × 2-digit
def set_3x2(rnd, seen):
    its = []
    for i in range(10):
        a, b = pick(rnd, seen, 3)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 3)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(3):
        a, b = pick(rnd, seen, 3)
        its.append(box_row_item(a, b, 0, rnd))
    for _ in range(3):
        a, b = pick(rnd, seen, 3, add_reg=2)
        its.append(sum_box_item(a, b, rnd))
    rnd.shuffle(its)
    return {"title": "Long multiplication: 3-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 3: 4-digit × 2-digit (SATs style)
def drop_inner_zero(a):
    s = str(a)
    return int(s[0] + s[1:-1].replace("0", "") + s[-1])


def zero_item(a, b, rnd, col):
    """a has a 0 inside."""
    q = (fig(col_problem(a, b)) + "Use long multiplication.") if col else "Calculate %s × %d" % (f(a), b)
    z = digits(a).index(0)
    lost = sum(mult_row(a, d, "skip", k=z - 1) * 10 ** i for d, i, v in pp_rows(a, b))
    wrong = [lost, total_with(a, b, "zero_d"), drop_inner_zero(a) * b, no_zero(a, b)]
    j = [k for k, r in enumerate(pp_rows(a, b)) if digits(a)[z - 1] * r[0] >= 10][0]
    e = "Do not skip the 0: 0 × a digit = 0, then add the exchanged digit. " + steps(a, b, detail=j)
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


def end_zero_item(a, b, rnd):
    s = a // 10
    q = "Calculate %s × %d" % (f(a), b)
    wrong = [s * b, a * b * 10, no_zero(a, b), total_with(a, b, "nocarry")]
    e = ("Shortcut: %s = %s × 10. Work out %s × %d = %s, then multiply by 10: %s. Or use the rows: "
         % (f(a), f(s), f(s), b, f(s * b), f(a * b)) + steps(a, b))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


def set_4x2(rnd, seen):
    its = []
    for i in range(10):
        a, b = pick(rnd, seen, 4)
        its.append(compute_item(a, b, rnd, i % 2 == 1))
    for _ in range(3):
        a, b = pick(rnd, seen, 4)
        its.append(box_row_item(a, b, 1, rnd))
    for i in range(3):
        a, b = pick(rnd, seen, 4, zero="in")
        its.append(zero_item(a, b, rnd, i % 2 == 0))
    for _ in range(2):
        a, b = pick(rnd, seen, 4, add_reg=3)
        its.append(sum_box_item(a, b, rnd))
    for _ in range(2):
        a, b = pick(rnd, seen, 4, zero="end")
        its.append(end_zero_item(a, b, rnd))
    rnd.shuffle(its)
    return {"title": "Long multiplication: 4-digit × 2-digit (SATs style)", "items": its}


# ------------------------------------------------------------ set 4: find the mistake, missing digits
WHERE = ["Row 1", "Row 2", "The total", "There is no mistake"]


def where_item(a, b, kind, rnd, P):
    """Full working with (maybe) one mistake. The total is what the pupil got from the rows shown."""
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    r0, r1 = v0, v1
    n, he, his = P.next()
    if kind == "zero":
        r1 = a * d1
        ans = "Row 2"
        why = ("Row 2 has no place-holder 0. It should be %s × %d = %s, not %s. The row is 10 times too small."
               % (f(a), d1 * 10, f(v1), f(r1)))
    elif kind == "cfirst":
        r1 = mult_row(a, d1, "cfirst") * 10
        ans = "Row 2"
        why = ("In row 2 the exchanged digit was added before multiplying. Multiply first, then add: %s. Row 2 should be %s."
               % (steps_1d(a, d1), f(v1)))
    elif kind == "nocarry":
        r0 = mult_row(a, d0, "nocarry")
        ans = "Row 1"
        why = "In row 1 the exchanged digits were not added: %s. Row 1 should be %s, not %s." % (steps_1d(a, d0), f(v0), f(r0))
    elif kind == "add":
        ans = "The total"
        why = "Both rows are right, but an exchanged digit was missed when adding: %s + %s = %s." % (f(v0), f(v1), f(a * b))
    else:
        ans = "There is no mistake"
        why = "Both rows and the total are right. " + steps(a, b)
    tot = r0 + r1 if kind != "add" else add_cols([v0, v1], drop="all")
    assert (tot == a * b) == (kind == "ok"), (a, b, kind)
    if kind not in ("ok", "add"):
        why += " The correct answer is %s." % f(a * b)
    rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(r1)), ("", str(tot))]
    q = (fig(column_svg(rows, [1, 3], "%d times %d: working to check" % (a, b))) +
         "%s worked out %s × %d. Where is %s mistake?" % (n, f(a), b, his))
    return mcq(q, ans, [w for w in WHERE if w != ans], why, rnd)


WHAT = ["Forgot the place-holder zero", "Did not add an exchanged digit", "Added the two rows wrongly",
        "Multiplied by only one digit"]


def what_item(a, b, kind, rnd, P):
    """Working with a typical mistake: which mistake is it?"""
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    n, he, his = P.next()
    if kind == 0:
        rows = [("", str(a)), ("×", str(b)), ("", str(v0)), ("+", str(a * d1)), ("", str(v0 + a * d1))]
        rules, got = [1, 3], v0 + a * d1
        why = "Row 2 should be %s × %d = %s, but %s wrote %s. The place-holder 0 is missing." % (f(a), d1 * 10, f(v1), he, f(a * d1))
    elif kind == 1:
        r0 = mult_row(a, d0, "nocarry")
        rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(v1)), ("", str(r0 + v1))]
        rules, got = [1, 3], r0 + v1
        why = "Row 1 should be %s, not %s: %s. The exchanged digits were not added." % (f(v0), f(r0), steps_1d(a, d0))
    elif kind == 2:
        got = add_cols([v0, v1], drop="all")
        rows = [("", str(a)), ("×", str(b)), ("", str(v0)), ("+", str(v1)), ("", str(got))]
        rules = [1, 3]
        why = "Both rows are right. The mistake is in the adding: %s + %s = %s." % (f(v0), f(v1), f(a * b))
    else:
        got = v0
        rows = [("", str(a)), ("×", str(b)), ("", str(v0))]
        rules = [1]
        why = ("%s only multiplied by the ones digit, %d. %s also needs the row for %d tens: %s × %d = %s. "
               "Add the rows: %s + %s = %s." % (cap(he), d0, f(b), d1, f(a), d1 * 10, f(v1), f(v0), f(v1), f(a * b)))
    assert got != a * b
    q = (fig(column_svg(rows, rules, "%d times %d: working with a mistake" % (a, b))) +
         "%s got %s × %d = %s. What mistake did %s make?" % (n, f(a), b, f(got), he))
    ans = WHAT[kind]
    if kind != 2:
        why += " The correct answer is %s." % f(a * b)
    return mcq(q, ans, [w for w in WHAT if w != ans], why, rnd)


def missing_total_item(a, b, rnd):
    """One digit of the total is '?'. None if the mistakes do not give 3 different digits."""
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
    """One digit inside row j is '?' (a place where an exchanged digit is added). No total shown."""
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


def set_errors(rnd, seen, P):
    its = []
    for kind in ["zero", "nocarry", "cfirst", "add", "ok"]:
        while True:
            a, b = pick(rnd, seen, 3, add_reg=1)
            (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
            if kind == "cfirst" and mult_row(a, d1, "cfirst") == a * d1:
                continue
            if kind == "add" and add_cols([v0, v1], drop="all") == a * b:
                continue
            break
        its.append(where_item(a, b, kind, rnd, P))
    for kind in [0, 1, 2, 3, 0]:
        while True:
            a, b = pick(rnd, seen, 3 if kind != 3 else 4, add_reg=1)
            if kind == 2 and add_cols([v for _, _, v in pp_rows(a, b)], drop="all") == a * b:
                continue
            break
        its.append(what_item(a, b, kind, rnd, P))
    n = 0
    while n < 5:
        a, b = pick(rnd, seen, 3 if n < 2 else 4, add_reg=2)
        it = missing_total_item(a, b, rnd)
        if it:
            its.append(it)
            n += 1
    n = 0
    while n < 5:
        a, b = pick(rnd, seen, 3 if n < 2 else 4)
        it = missing_row_item(a, b, n % 2, rnd)
        if it:
            its.append(it)
            n += 1
    rnd.shuffle(its)
    return {"title": "Find the mistake and missing digits", "items": its}


# ------------------------------------------------------------ set 5: word problems
def money(v):
    return "£" + f(v)


# (story, a, b, unit, lead)  {n} name, {he} pronoun, {his} possessive. a = the bigger number.
STORIES = [
    ("A coach has 53 seats. It is full on every one of its {b} trips to the seaside this summer. "
     "How many passengers is that altogether?", 53, 24, "passengers", "{b} trips × {a} passengers"),
    ("A ticket for a theme park costs £125. A school buys {b} tickets for a Year 6 trip. How much does it pay?",
     125, 36, "£", "{b} tickets × £{a}"),
    ("A box holds 144 pencils. The school office orders {b} boxes. How many pencils is that?",
     144, 26, "pencils", "{b} boxes × {a} pencils"),
    ("The school kitchen serves {a} lunches each week. How many lunches does it serve in 38 weeks?",
     None, 38, "lunches", "38 weeks × {a} lunches"),
    ("A cinema screen has {b} rows of seats with {a} seats in each row. How many seats are there?",
     None, None, "seats", "{b} rows × {a} seats"),
    ("A lorry carries {b} crates. Each crate has a mass of {a} kg. What is the total mass of the crates?",
     None, None, "kg", "{b} crates × {a} kg"),
    ("A bakery bakes {a} loaves of bread every day. How many loaves does it bake in 28 days?",
     None, 28, "loaves", "28 days × {a} loaves"),
    ("A concert hall sells {a} tickets at £{b} each. How much money does it take?",
     None, None, "£", "{a} tickets × £{b}"),
    ("A factory makes {a} toy cars each day. How many toy cars does it make in {b} days?",
     None, None, "toy cars", "{b} days × {a} toy cars"),
    ("A delivery driver drives {a} km each week. How far does {he} drive in {b} weeks?",
     None, None, "km", "{b} weeks × {a} km"),
    ("{n} swims {a} lengths of a 25 m pool over a term. How far does {he} swim?",
     64, 25, "m", "{a} lengths × 25 m"),
    ("A theatre has {a} seats. Every seat is sold for all {b} shows of the Christmas pantomime. How many tickets are sold?",
     None, None, "tickets", "{b} shows × {a} tickets"),
    ("A garden centre has {b} trays of plants. Each tray holds {a} plants. How many plants is that?",
     None, None, "plants", "{b} trays × {a} plants"),
    ("A family pays £{a} a month for their flat. How much do they pay in {b} months?",
     None, 24, "£", "{b} months × £{a}"),
]
RANGES = {   # story index: (a range, b range)
    3: ((245, 389), None), 4: ((24, 36), (14, 28)), 5: ((125, 480), (14, 28)), 6: ((135, 289), None),
    7: ((1245, 2875), (24, 58)), 8: ((1245, 3480), (12, 28)), 9: ((1125, 1680), (12, 26)),
    11: ((1125, 1875), (23, 36)), 12: ((24, 48), (32, 65)), 13: ((725, 975), None),
}


def nz(n):
    return 0 not in digits(n)


def set_story(rnd, P):
    its = []
    used = set()
    for k, (t, a, b, unit, lead) in enumerate(STORIES):
        if k in RANGES:
            ar, br = RANGES[k]
            while True:
                aa = rnd.randint(*ar) if ar else a
                bb = rnd.randint(*br) if br else b
                if not (nz(aa) and nz(bb)) or 1 in digits(bb) or bb % 11 == 0 or (aa, bb) in used:
                    continue
                if any(carries(aa, d) == 0 for d in digits(bb)):
                    continue
                break
            a, b = aa, bb
        used.add((a, b))
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=f(a), b=b)
        fm = money if unit == "£" else (lambda v, u=unit: "%s %s" % (f(v), u))
        e = "Equal groups: %s, so multiply %s × %d. " % (lead.format(a=f(a), b=b), f(a), b) + steps(a, b)
        its.append(mcq(q, fm(a * b), [fm(v) for v in cands(a, b, rnd)], e, rnd))

    # two-step problems
    k, price, have = 24, 235, 6000
    cost = k * price
    its.append(mcq("A school has %s to spend. It buys %d laptops at £%d each. How much money is left?" % (money(have), k, price),
                   money(have - cost),
                   [money(v) for v in [cost, have - no_zero(price, k), have - total_with(price, k, "nocarry"), have + cost]],
                   "Step 1: the cost. " + steps(price, k) + " So the laptops cost %s. Step 2: %s − %s = %s left."
                   % (money(cost), money(have), money(cost), money(have - cost)), rnd))
    per, d1, d2 = 144, 26, 38
    tot = per * (d1 + d2)
    its.append(mcq("A farm packs %d eggs in each crate. It sends %d crates on Monday and %d crates on Tuesday. "
                   "How many eggs does it send altogether?" % (per, d1, d2),
                   "%s eggs" % f(tot),
                   ["%s eggs" % f(v) for v in [per * d1 + d2, no_zero(per, d1 + d2), per * d2, per * d1 * d2]],
                   "Step 1: crates: %d + %d = %d. Step 2: eggs: %d × %d. " % (d1, d2, d1 + d2, per, d1 + d2) + steps(per, d1 + d2),
                   rnd))

    # estimate checks (round each number to its greatest place)
    def lead_round(x):
        p = 10 ** (len(str(x)) - 1)
        return (x + p // 2) // p * p

    for a, b, kind in [(2345, 28, "no_zero"), (3164, 47, "ok"), (4127, 63, "one_digit"), (689, 52, "ok")]:
        n, he, his = P.next()
        claim = {"no_zero": no_zero, "ok": lambda x, y: x * y, "one_digit": one_digit}[kind](a, b)
        ra, rb = lead_round(a), lead_round(b)
        est = ra * rb
        ok = claim == a * b
        if not ok:
            assert not 0.5 < claim / est < 2, (a, b, claim, est)
        right = ("Yes, it is close to %s" if ok else "No, it should be about %s") % f(est)
        wrong = [("No, it should be about %s" if ok else "Yes, it is close to %s") % f(est),
                 "Yes, it is close to %s" % f(est // 10),
                 "No, it should be about %s" % f(est * 10)]
        how = "%s rounds to %s and %d rounds to %d. %s × %d = %s." % (f(a), f(ra), b, rb, f(ra), rb, f(est))
        if ok:
            tail = " %s is close to %s, so the answer is sensible. (It is also exactly right.)" % (f(claim), f(est))
        else:
            reason = {"no_zero": "%s forgot the place-holder 0 in the second row" % n,
                      "one_digit": "%s only multiplied by the ones digit" % n}[kind]
            tail = " %s is far from %s, so the answer cannot be right. The correct answer is %s; %s." % (
                f(claim), f(est), f(a * b), reason)
        its.append(mcq("%s says %s × %d = %s. Estimate to check. Is %s answer sensible?" % (n, f(a), b, f(claim), his),
                       right, wrong, how + tail, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems and estimating to check", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def row_exchanges(a, d, shift):
    """Exchanged digits written while multiplying a by d: {place in the row: digit}."""
    out, c = {}, 0
    ds = digits(a)
    for i, x in enumerate(ds[:-1]):
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
    return (
        "<h2>One row for each digit</h2>"
        "<p>Long multiplication is the formal written method for multiplying by a 2-digit number. "
        "You multiply the top number by <b>one digit at a time</b>, so you get <b>two rows</b>. Then you add the rows.</p>"
        "<p>Row 1 multiplies by the <b>ones</b> digit. Row 2 multiplies by the <b>tens</b> digit, so it starts with a "
        "<b>place-holder zero</b> (green) in the ones column. Write the exchanged digits small, and add them after you multiply.</p>"
        "<figure class='sn-fig'>" + lesson_fig(47, 36, "47 times 36 as long multiplication") +
        "<figcaption>47 × 36: row 1 is 47 × 6 = 282. Row 2 is 47 × 30: write 0, then 47 × 3 = 141, so 1,410. "
        "282 + 1,410 = 1,692.</figcaption></figure>"
        "<h2>4-digit × 2-digit, as in the SATs</h2>"
        "<figure class='sn-fig'>" + lesson_fig(2345, 28, "2345 times 28 as long multiplication") +
        "<figcaption>2,345 × 28: row 1 is 2,345 × 8 = 18,760. Row 2 is 2,345 × 20 = 46,900. "
        "18,760 + 46,900 = 65,660.</figcaption></figure>" +
        ex("A zero inside the number", "405 × 32 = ?",
           "Row 1: 5 × 2 = 10, write 0, exchange 1. 0 × 2 + 1 = 1. 4 × 2 = 8. So 405 × 2 = 810. "
           "Row 2: write 0, then 405 × 3 = 1,215, so 12,150. Add: 810 + 12,150 = 12,960.", "12,960") +
        "<h2>Estimate to check</h2>"
        "<p>Round each number and multiply in your head. 2,345 × 28 is about 2,000 × 30 = 60,000, "
        "so 65,660 makes sense. An answer like 23,450 is far too small.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["No place-holder zero (47 × 36 = 282 + 141 = 423)", "Row 2 is × 30, so write 0 first: 1,410"],
            ["Forgetting an exchanged digit (47 × 6 = 242)", "Write it small and add it: 4 × 6 + 4 = 28, so 282"],
            ["Adding the exchanged digit first", "Multiply first, then add: 4 × 6 + 4 = 28, not (4 + 4) × 6"],
            ["Multiplying by only one digit (47 × 36 = 282)", "Make a row for the ones and a row for the tens"],
            ["Adding the rows wrongly", "Use column addition and add every exchanged digit"],
        ])
    )


FAQ = [
    {"q": "How do you do long multiplication in Year 6?",
     "a": "Multiply the top number by the ones digit to make row 1. Write a place-holder zero, then multiply by the tens digit to make row 2. Add the two rows with column addition, for example 47 × 36 = 282 + 1,410 = 1,692."},
    {"q": "Why do you put a zero in long multiplication?",
     "a": "In 47 × 36 the 3 means 3 tens, so row 2 is 47 × 30, not 47 × 3. The place-holder zero in the ones column makes the row 1,410 instead of 141."},
    {"q": "What is the difference between short and long multiplication?",
     "a": "Short multiplication is for multiplying by a one-digit number and gives one row. Long multiplication is for a two-digit number: you make one row for each digit and then add the rows."},
    {"q": "Is long multiplication in the Year 6 SATs?",
     "a": "Yes. Paper 1 (arithmetic) usually has long multiplication questions such as 4-digit × 2-digit. They are worth 2 marks, and a pupil can still get 1 mark for using the formal method with no more than one arithmetic error."},
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
    rnd = random.Random(6602)
    P = People(rnd)
    seen = set()
    sets = [set_2x2(rnd, seen), set_3x2(rnd, seen), set_4x2(rnd, seen), set_errors(rnd, seen, P), set_story(rnd, P)]
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
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "long-multiplication", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Long Multiplication",
        "seo_title": "Year 6 Long Multiplication Worksheets: 4-Digit by 2-Digit (KS2 SATs)",
        "short_title": "Long multiplication",
        "domain": "Multiplication and division",
        "standard_code": "Year 6: Addition, subtraction, multiplication and division",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply multi-digit numbers up to 4 digits by a two-digit whole number using the formal written method of long multiplication.",
        "meta_desc": "Free Year 6 maths worksheets on long multiplication: 2-digit, 3-digit and 4-digit numbers × 2-digit numbers, the place-holder zero, finding mistakes and missing digits, and SATs-style word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Make one row for each digit: multiply by the ones, then by the tens. Then add the rows.",
        "key_sub": "Row 2 starts with a place-holder zero because it multiplies by tens: 47 × 36 = 282 + 1,410 = 1,692. Estimate first to check your answer.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag pictures that must print larger so the digits stay readable."""
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
