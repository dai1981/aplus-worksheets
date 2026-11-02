# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Multi-Digit Multiplication with the Standard Algorithm (5.NBT.B.5)
  python3 tools/gen_us_math_g5_multiplication.py
Every product and every wrong answer is computed here (wrong answers = real mistakes).
HTML attributes use single quotes (no backslashes in the JSON).
Grade 5 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
RED = "#c0392b"
INK = "#2b2b2b"
NOTE = "#5a5a5a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[-1 if c.startswith("about") else 0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
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
    """Numbers in columns, ones lined up on the right.
    rows = list of (sign, text) or (sign, text, nz): nz = number of placeholder zeros at the end (drawn green).
    text '[?]' = a red dashed box across the row (the number to find); a '?' inside a number = one red missing digit.
    Commas sit in the gap between digit columns. rules = row indexes with a line under them.
    notes = optional short notes written to the right of the rows (lesson figures)."""
    fs = 28 if big else 26
    cw = fs * 0.78
    rows = [r if len(r) == 3 else (r[0], r[1], 0) for r in rows]
    lens = [0 if t == "[?]" else len(t.replace(",", "")) for sg, t, nz in rows]
    nd = max(lens)
    signed = max([nd if t == "[?]" else n for (sg, t, nz), n in zip(rows, lens) if sg] or [0])
    sign_slot = max(nd, signed + 1)
    slots = sign_slot + 1
    nfs = 16
    note_w = 0
    if notes:
        note_w = max(len(n) * nfs * 0.54 for n in notes if n) + 18
    num_w = cw * slots + 20
    W = int(num_w + note_w + 0.999)
    gap = fs * 1.2
    H = int(10 + gap * len(rows) + 5 * len(rules) + 10)
    right = num_w - 10
    s = []
    y = 10
    for r, (sg, t, nz) in enumerate(rows):
        y += gap
        if t == "[?]":
            x1 = right - cw * nd
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='none' stroke='%s' "
                     "stroke-width='2' stroke-dasharray='5 3'/>" % (x1 + 3, y - fs * 0.86, cw * nd - 3, fs * 0.98, RED))
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (x1 + cw * nd / 2, y - 2, fs, RED))
        else:
            slot = 0
            for ch in reversed(t):
                if ch == ",":
                    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>,</text>"
                             % (right - cw * slot, y + 1, fs, INK))
                    continue
                if ch == "?":
                    cx = right - cw * (slot + 0.5)
                    s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                             "stroke-width='2' stroke-dasharray='4 2'/>" % (cx - cw * 0.38, y - fs * 0.84, cw * 0.76, fs * 0.96, RED))
                    col = RED
                else:
                    col = GREEN if slot < nz else INK
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (right - cw * (slot + 0.5), y - 2, fs, col, ch))
                slot += 1
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
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%s'><g font-family='monospace'>%s</g></svg>" % (W, H, W, H, label, "".join(s)))


def col_problem(a, b):
    return column_svg([("", f(a)), ("×", f(b))], [1], "%d times %d written in columns" % (a, b))


def pp_rows(a, b):
    """Partial-product rows of the standard algorithm, ones row first: (digit, place, value)."""
    return [(d, i, a * d * 10 ** i) for i, d in enumerate(digits(b))]


def work_rows(a, b, box=None, wrong=None, total=True, qdigit=None):
    """Rows for the full written work. box = index of the partial-product row shown as [?];
    box='sum' hides the total. wrong = {row index: value shown instead}. qdigit = place of the total shown as '?'."""
    pr = pp_rows(a, b)
    rows = [("", f(a)), ("×", f(b))]
    for k, (d, i, v) in enumerate(pr):
        sg = "+" if k == len(pr) - 1 else ""
        if box == k:
            rows.append((sg, "[?]"))
        elif wrong and k in wrong:
            rows.append((sg, f(wrong[k]), 0))
        else:
            rows.append((sg, f(v), i))
    rules = [1]
    if total:
        rules.append(len(rows) - 1)
        if box == "sum":
            rows.append(("", "[?]"))
        elif qdigit is not None:
            t = f(a * b)
            ds = list(t)
            # find the char for place qdigit, counting digits from the right
            cnt = -1
            for j in range(len(ds) - 1, -1, -1):
                if ds[j] != ",":
                    cnt += 1
                    if cnt == qdigit:
                        ds[j] = "?"
                        break
            rows.append(("", "".join(ds)))
        else:
            rows.append(("", f(a * b)))
    return rows, rules


def work_svg(a, b, **kw):
    rows, rules = work_rows(a, b, **kw)
    return column_svg(rows, rules, "%d times %d with partial products" % (a, b))


# ------------------------------------------------------------ explanations
def row_text(a, d, i):
    v = a * d * 10 ** i
    if i == 0:
        return "%s × %d = %s" % (f(a), d, f(v))
    z = "0" * i
    return "%s × %s = %s (write %s, then %s × %d = %s)" % (f(a), f(d * 10 ** i), f(v), z, f(a), d, f(a * d))


def steps(a, b, detail=None):
    """detail = row index whose place-by-place work is shown too."""
    pr = pp_rows(a, b)
    out = []
    for k, (d, i, v) in enumerate(pr):
        if k == detail:
            if i == 0:
                out.append("Row %d: %s × %d = %s (%s)." % (k + 1, f(a), d, f(v), steps_1d(a, d)))
            else:
                out.append("Row %d: %s × %s = %s (write %s, then %s × %d: %s)." % (
                    k + 1, f(a), f(d * 10 ** i), f(v), "0" * i, f(a), d, steps_1d(a, d)))
        else:
            out.append("Row %d: %s." % (k + 1, row_text(a, d, i)))
    out.append("Add: %s = %s." % (" + ".join(f(v) for d, i, v in pr), f(a * b)))
    return " ".join(out)


def steps_1d(a, d):
    """Inside one row: multiply place by place, then add the regrouped digit."""
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        if i == len(ds) - 1 or p < 10:
            out.append("%s = %d, write %d" % (ex_, p, p if i == len(ds) - 1 else p))
        else:
            out.append("%s = %d, write %d, regroup %d" % (ex_, p, p % 10, p // 10))
        c = p // 10 if i < len(ds) - 1 else 0
    return "; ".join(out)


# ------------------------------------------------------------ typical mistakes
def mult_row(a, d, mode="ok", k=None):
    """One row, a × d, done with a typical mistake.
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
    """No placeholder zeros: the rows are not shifted."""
    return sum(a * d for d in digits(b))


def short_zero(a, b):
    """3-digit multiplier: the hundreds row gets only one zero."""
    h = digits(b)[2]
    return a * b - a * h * 100 + a * h * 10


def skip_last(a, b):
    """Left out the last partial product when adding."""
    pr = pp_rows(a, b)
    return a * b - pr[-1][2]


def add_cols(nums, drop=None, extra=None):
    """Column addition. drop = None: correct; 'all': forget every regrouped digit; int k: forget only the one from place k.
    extra = int k: regroup 1 too many out of place k. The last column is written whole."""
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
    """Places (not the last column) where the column addition regroups."""
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
    if len(pr) == 3:
        more += [short_zero(a, b), skip_last(a, b)]
    elif len(str(a)) == 2:
        more.append(two_pp(a, b))
    rnd.shuffle(more)
    return out + more + [skip_last(a, b), total_with(a, b, "skip", k=0)]


def carries(a, d):
    """Regroups that move to a next digit (the last digit's product is written whole, so it does not count)."""
    c, n = 0, 0
    for x in digits(a)[:-1]:
        p = x * d + c
        c = p // 10
        n += 1 if c else 0
    return n


# ------------------------------------------------------------ choosing numbers
def pick(rnd, seen, na, nb, zero=None, add_reg=0):
    """a has na digits, b has nb digits (2-9, all different). Every row regroups at least once.
    zero='in': a has a 0 inside (not first, not last); zero='end': a ends in 0 (one 0, inside digits nonzero).
    add_reg = how many regroups the addition of the rows must have at least."""
    while True:
        a = rnd.randint(10 ** (na - 1) + 1, 10 ** na - 1)
        bd = rnd.sample(range(2, 10), nb)
        b = int("".join(map(str, bd)))
        da = digits(a)
        if zero == "in":
            if da[0] == 0 or da[-1] == 0 or da[1:-1].count(0) != 1:
                continue
            z = da.index(0)
            if not any(da[z - 1] * d >= 10 for d in digits(b)):        # a regroup must land on the 0
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
    q = (fig(col_problem(a, b)) + "Multiply.") if col else "What is %s × %s?" % (f(a), f(b))
    return mcq(q, f(a * b), [f(v) for v in cands(a, b, rnd)], steps(a, b), rnd)


def box_row_item(a, b, k, rnd):
    """The k-th partial-product row is a dashed box."""
    d, i, v = pp_rows(a, b)[k]
    q = fig(work_svg(a, b, box=k)) + "What number goes in the dashed box?"
    if i == 0:
        wrong = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst"), mult_row(a, d, "skip", k=0),
                 mult_row(a, d, "skip", k=1), v * 10]
        e = "Row 1 is %s × %d: %s. So the row is %s." % (f(a), d, steps_1d(a, d), f(v))
    else:
        wrong = [a * d, a * d * 10 ** (i - 1) if i > 1 else v * 10, mult_row(a, d, "nocarry") * 10 ** i,
                 mult_row(a, d, "cfirst") * 10 ** i, v * 10]
        zs = "a 0" if i == 1 else "two 0s"
        e = ("Row %d multiplies by the %s digit, so it is %s × %s. Write %s first, then %s × %d = %s. The row is %s."
             % (k + 1, PLACE[i], f(a), f(d * 10 ** i), zs, f(a), d, f(a * d), f(v)))
    e += " Check: %s = %s." % (" + ".join(f(x) for _, _, x in pp_rows(a, b)), f(a * b))
    return mcq(q, f(v), [f(x) for x in wrong], e, rnd)


def place_name(i):
    return PLACE[i]


def sum_box_item(a, b, rnd):
    pr = [v for d, i, v in pp_rows(a, b)]
    cs = add_carries(pr)
    wrong = [add_cols(pr, drop="all")] + [add_cols(pr, drop=k) for k in cs] + \
            [add_cols(pr, extra=k) for k in range(len(str(a * b))) if k not in cs]
    q = fig(work_svg(a, b, box="sum")) + "What number goes in the dashed box?"
    e = ("Add the partial products column by column and carry each regrouped digit: %s = %s."
         % (" + ".join(f(v) for v in pr), f(a * b)))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


# ------------------------------------------------------------ set 1: 2-digit × 2-digit warm-up
def set_warm(rnd, seen):
    its = []
    for i in range(8):
        a, b = pick(rnd, seen, 2, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 2, 2)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(4):
        a, b = pick(rnd, seen, 2, 2)
        its.append(box_row_item(a, b, 0, rnd))
    for k in range(4):
        a, b = pick(rnd, seen, 2, 2)
        o, t = b % 10, b // 10
        ta, oa = a // 10 * 10, a % 10
        q = fig(work_svg(a, b))
        if k % 2 == 0:
            v = a * t * 10
            right = "%d × %d" % (a, t * 10)
            wrong = ["%d × %d" % (a, t), "%d × %d" % (ta, t * 10), "%d × %d" % (oa, t * 10)]
            q += "Which multiplication gives the second row, %s?" % f(v)
            e = ("The %d in %d means %d tens, so the second row is %d × %d = %s. That is why it ends in 0. "
                 "%d × %d would be only %d." % (t, b, t, a, t * 10, f(v), a, t, a * t))
        else:
            v = a * o
            right = "%d × %d" % (a, o)
            wrong = ["%d × %d" % (oa, o), "%d × %d" % (ta, o), "%d × %d" % (a, o * 10)]
            q += "Which multiplication gives the first row, %s?" % f(v)
            e = ("The first row multiplies all of %d by the ones digit, %d: %d × %d = %s. "
                 "Then the second row is %d × %d = %s." % (a, o, a, o, f(v), a, t * 10, f(a * t * 10)))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Warm-up: 2-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 2: 3-digit × 2-digit
def set_3x2(rnd, seen):
    its = []
    for i in range(10):
        a, b = pick(rnd, seen, 3, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 3, 2)
        its.append(box_row_item(a, b, 1, rnd))
    for _ in range(3):
        a, b = pick(rnd, seen, 3, 2)
        its.append(box_row_item(a, b, 0, rnd))
    for _ in range(3):
        a, b = pick(rnd, seen, 3, 2, add_reg=2)
        its.append(sum_box_item(a, b, rnd))
    rnd.shuffle(its)
    return {"title": "3-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 3: 4-digit × 2-digit and zeros
def drop_inner_zero(a):
    s = str(a)
    return int(s[0] + s[1:-1].replace("0", "") + s[-1])


def zero_item(a, b, rnd, col):
    """a has a 0 inside."""
    q = (fig(col_problem(a, b)) + "Multiply.") if col else "What is %s × %s?" % (f(a), f(b))
    z = digits(a).index(0)
    lost = sum(mult_row(a, d, "skip", k=z - 1) * 10 ** i for d, i, v in pp_rows(a, b))
    wrong = [lost, total_with(a, b, "zero_d"), drop_inner_zero(a) * b, no_zero(a, b)]
    # the row where a regroup lands on the 0
    j = [k for k, r in enumerate(pp_rows(a, b)) if digits(a)[z - 1] * r[0] >= 10][0]
    e = "Do not skip the 0: 0 times a digit is 0, then add the regrouped digit. " + steps(a, b, detail=j)
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


def end_zero_item(a, b, rnd):
    s = a // 10
    q = "What is %s × %s?" % (f(a), f(b))
    wrong = [s * b, a * b * 10, no_zero(a, b), total_with(a, b, "nocarry")]
    e = ("Shortcut: %s = %s × 10. Multiply %s × %s = %s, then write the 0 back: %s. Or use the rows: "
         % (f(a), f(s), f(s), f(b), f(s * b), f(a * b)) + steps(a, b))
    return mcq(q, f(a * b), [f(x) for x in wrong], e, rnd)


def set_4x2(rnd, seen):
    its = []
    for i in range(8):
        a, b = pick(rnd, seen, 4, 2)
        its.append(compute_item(a, b, rnd, i % 2 == 1))
    for _ in range(2):
        a, b = pick(rnd, seen, 4, 2)
        its.append(box_row_item(a, b, 1, rnd))
    for i in range(6):
        a, b = pick(rnd, seen, 3 if i < 3 else 4, 2, zero="in")
        its.append(zero_item(a, b, rnd, i % 2 == 0))
    for i in range(4):
        a, b = pick(rnd, seen, 3 if i < 2 else 4, 2, zero="end")
        its.append(end_zero_item(a, b, rnd))
    rnd.shuffle(its)
    return {"title": "4-digit × 2-digit and numbers with zeros", "items": its}


# ------------------------------------------------------------ set 4: 3-digit × 3-digit
def missing_digit_item(a, b, rnd):
    """One digit of the total is '?'. Returns None if the mistakes do not give 3 different digits."""
    pr = [v for d, i, v in pp_rows(a, b)]
    tot = a * b
    for k in range(2, len(str(tot)) - 1):
        cin = sum(v % 10 ** k for v in pr) // 10 ** k
        col = [v // 10 ** k % 10 for v in pr]
        S = sum(col) + cin
        right = S % 10
        if cin == 0 or S < 10:
            continue
        wrong = [(S - cin) % 10, S // 10] + [(S - x) % 10 for x in col if x]
        ws = []
        for w in wrong:
            if w != right and w not in ws:
                ws.append(w)
        if len(ws) < 3:
            continue
        shown = " + ".join(str(x) for x in col if x) or "0"
        e = ("Add the %s column of the partial products: %s = %d, plus %d regrouped from the %s = %d. "
             "Write %d. The full product is %s."
             % (PLACE[k], shown, sum(col), cin, PLACE[k - 1], S, right, f(tot)))
        if sum(1 for x in col if x) == 1:
            e = e.replace(": %s = %d, plus" % (shown, sum(col)), ": %s, plus" % shown)
        q = fig(column_svg(*work_rows(a, b, qdigit=k), label="%d times %d with partial products" % (a, b))) + \
            "What digit goes in the box?"
        return mcq(q, str(right), [str(w) for w in ws], e, rnd)
    return None


def wrong_row_item(a, b, kind, rnd, P):
    """One partial product has a typical mistake. Rows only, no total."""
    pr = pp_rows(a, b)
    if kind == 0:          # forgot the zero in row 2
        j = 1
        val = a * pr[1][0]
        why = "The 0 in the ones place is missing, so the row is 10 times too small."
    elif kind == 1:        # one zero in row 3
        j = 2
        val = a * pr[2][0] * 10
        why = "Row 3 multiplies by hundreds, so it needs two 0s, not one."
    elif kind == 2:        # forgot a regrouped digit in row 1
        j = 0
        val = mult_row(a, pr[0][0], "nocarry")
        why = "The regrouped digits were not added: %s." % steps_1d(a, pr[0][0])
    else:                  # added the regrouped digit first in row 2
        j = 1
        val = mult_row(a, pr[1][0], "cfirst") * 10
        why = "The regrouped digit was added before multiplying. Multiply first, then add: %s." % steps_1d(a, pr[1][0])
    d, i, v = pr[j]
    rows = [("", f(a)), ("×", f(b))]
    for k, (dd, ii, vv) in enumerate(pr):
        sg = "+" if k == 2 else ""
        rows.append((sg, f(val) if k == j else f(vv), 0))       # no green zeros: colors must not give the answer away
    n, he, his = P.next()
    q = (fig(column_svg(rows, [1], "%d times %d: three partial products" % (a, b))) +
         "%s wrote the partial products for %s × %s. Which one is wrong?" % (n, f(a), f(b)))
    right = f(val)
    others = [f(vv) for k, (dd, ii, vv) in enumerate(pr) if k != j] + ["None is wrong"]
    e = ("Row %d should be %s. It shows %s. %s The product is %s."
         % (j + 1, row_text(a, d, i), f(val), why, f(a * b)))
    assert val != v
    return mcq(q, right, others, e, rnd)


def set_3x3(rnd, seen, P):
    its = []
    for i in range(8):
        a, b = pick(rnd, seen, 3, 3)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    for _ in range(4):
        a, b = pick(rnd, seen, 3, 3)
        its.append(box_row_item(a, b, 2, rnd))
    n = 0
    while n < 4:
        a, b = pick(rnd, seen, 3, 3, add_reg=3)
        it = missing_digit_item(a, b, rnd)
        if it:
            its.append(it)
            n += 1
    for k in range(4):
        while True:
            a, b = pick(rnd, seen, 3, 3)
            d1 = digits(b)[1]
            if k == 3 and mult_row(a, d1, "cfirst") == a * d1:
                continue
            if k == 2 and mult_row(a, digits(b)[0], "nocarry") == a * digits(b)[0]:
                continue
            break
        its.append(wrong_row_item(a, b, k, rnd, P))
    rnd.shuffle(its)
    return {"title": "3-digit × 3-digit", "items": its}


# ------------------------------------------------------------ set 5: word problems and estimates
def money(v):
    return "$" + f(v)


# (story, a-digits, b-digits, unit, lead)  {n} name, {he} pronoun, {his} possessive, {a} {b} numbers with commas.
STORIES = [
    ("A bakery bakes {a} muffins every day. How many muffins does it bake in {b} days?",
     (126, 348), (14, 28), "muffins", "{b} days × {a} muffins"),
    ("A stadium has {b} sections. Each section has {a} seats. How many seats are in the stadium?",
     (215, 468), (24, 38), "seats", "{b} sections × {a} seats"),
    ("A gym has {a} members. Each member pays ${b} a month. How much do the members pay in all each month?",
     (245, 689), (24, 49), "$", "{a} members × ${b}"),
    ("{n}'s school collects {a} cans each week for a food drive. How many cans does it collect in {b} weeks?",
     (125, 248), (12, 36), "cans", "{b} weeks × {a} cans"),
    ("A toy factory makes {a} toy cars each hour. How many toy cars does it make in {b} hours?",
     (1245, 2860), (24, 48), "toy cars", "{b} hours × {a} toy cars"),
    ("A plane flies {a} miles on each flight. How many miles does it fly in {b} flights?",
     (1245, 2480), (12, 28), "miles", "{b} flights × {a} miles"),
    ("A roll has {a} tickets. A county fair uses {b} rolls. How many tickets is that?",
     (1125, 1875), (12, 26), "tickets", "{b} rolls × {a} tickets"),
    ("A warehouse has {b} shelves. Each shelf holds {a} cans of soup. How many cans fit on all the shelves?",
     (144, 368), (124, 286), "cans", "{b} shelves × {a} cans"),
    ("A hotel has {b} rooms. One night every room is booked at ${a}. How much does the hotel take in that night?",
     (129, 289), (124, 268), "$", "{b} rooms × ${a}"),
    ("A city library lends {a} books each day. How many books does it lend in {b} days?",
     (234, 468), (125, 365), "books", "{b} days × {a} books"),
]


def nz(n):
    return 0 not in digits(n)


def set_story(rnd, P):
    its = []
    used = set()
    for t, ar, br, unit, lead in STORIES:
        while True:
            a, b = rnd.randint(*ar), rnd.randint(*br)
            if not (nz(a) and nz(b)) or 1 in digits(b) or (a, b) in used:
                continue
            m, mm = (a, b) if "{a} members" in lead else (a, b)
            if any(carries(m, d) == 0 for d in digits(mm)):
                continue
            break
        used.add((a, b))
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=f(a), b=f(b))
        fm = money if unit == "$" else (lambda v, u=unit: "%s %s" % (f(v), u))
        e = "Equal groups: %s, so multiply %s × %s. " % (lead.format(a=f(a), b=f(b)), f(a), f(b)) + steps(a, b)
        its.append(mcq(q, fm(a * b), [fm(v) for v in cands(a, b, rnd)], e, rnd))

    # two-step problems
    k, price, have = 28, 249, 8000
    cost = k * price
    its.append(mcq("A school buys %d tablets for $%d each. It has %s to spend. How much money is left?" % (k, price, money(have)),
                   money(have - cost),
                   [money(v) for v in [cost, have - total_with(price, k, "nocarry"), have - (no_zero(price, k)), have + cost]],
                   "Step 1: cost: " + steps(price, k).replace("Add:", "Add the rows:") +
                   " So the tablets cost %s. Step 2: %s − %s = %s left." % (money(cost), money(have), money(cost), money(have - cost)), rnd))
    per, d1, d2 = 144, 26, 38
    tot = per * (d1 + d2)
    its.append(mcq("A farm packs %d eggs in each case. It ships %d cases on Monday and %d cases on Tuesday. "
                   "How many eggs does it ship in all?" % (per, d1, d2),
                   "%s eggs" % f(tot),
                   ["%s eggs" % f(v) for v in [per * d1 + d2, per * d2, no_zero(per, d1 + d2), per * d1 * d2]],
                   "Step 1: cases: %d + %d = %d. Step 2: eggs: %d × %d. " % (d1, d2, d1 + d2, per, d1 + d2) + steps(per, d1 + d2),
                   rnd))

    # estimate (round each number to its greatest place)
    def lead_round(x):
        p = 10 ** (len(str(x)) - 1)
        return (x + p // 2) // p * p

    def trunc(x):
        p = 10 ** (len(str(x)) - 1)
        return x // p * p

    for a, b in [(487, 32), (3215, 48), (612, 287), (2876, 19)]:
        ra, rb = lead_round(a), lead_round(b)
        est = ra * rb
        wrong = [est // 10, est * 10, trunc(a) * trunc(b), ra * rb // 100]
        its.append(mcq("Round each number to its greatest place. Which is the best estimate for %s × %s?" % (f(a), f(b)),
                       "about %s" % f(est), ["about %s" % f(v) for v in wrong],
                       "%s rounds to %s and %s rounds to %s. %s × %s = %s. (The exact product, %s, is close to it.)"
                       % (f(a), f(ra), f(b), f(rb), f(ra), f(rb), f(est), f(a * b)), rnd))
    checks = [(538, 46, "no_zero"), (724, 389, "ok"), (2_143, 67, "skip_last"), (356, 241, "short_zero")]
    for a, b, kind in checks:
        n, he, his = P.next()
        claim = {"no_zero": no_zero, "ok": lambda x, y: x * y, "skip_last": skip_last, "short_zero": short_zero}[kind](a, b)
        ra, rb = lead_round(a), lead_round(b)
        est = ra * rb
        ok = claim == a * b
        if not ok:
            assert not 0.5 < claim / est < 2, (a, b, claim, est)
        right = ("Yes, about %s" if ok else "No, about %s") % f(est)
        wrong = [("No, about %s" if ok else "Yes, about %s") % f(est),
                 ("Yes, about %s" % f(est // 10)),
                 ("No, about %s" % f(est * 10))]
        how = "%s rounds to %s and %s rounds to %s, and %s × %s = %s." % (f(a), f(ra), f(b), f(rb), f(ra), f(rb), f(est))
        if ok:
            tail = " %s is close to %s, so the answer is reasonable. (It is also exact.)" % (f(claim), f(est))
        else:
            reason = {"no_zero": "%s forgot the 0 in the second row" % n,
                      "skip_last": "%s left out the second row when adding" % n,
                      "short_zero": "%s wrote only one 0 in the hundreds row" % n}[kind]
            tail = " %s is far from %s, so the answer is not reasonable. The exact product is %s; %s." % (
                f(claim), f(est), f(a * b), reason)
        its.append(mcq("%s says %s × %s = %s. Use an estimate. Is %s answer reasonable?" % (n, f(a), f(b), f(claim), his),
                       right, wrong, how + tail, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems and estimates", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def lesson_fig(a, b, label):
    rows, rules = work_rows(a, b)
    notes = ["", ""] + ["%s × %s" % (f(a), f(d * 10 ** i)) for d, i, v in pp_rows(a, b)] + ["add the rows"]
    return column_svg(rows, rules, label, notes=notes, big=True)


def body_html():
    return (
        "<h2>One row for each digit</h2>"
        "<p>The standard algorithm multiplies the top number by <b>one digit of the bottom number at a time</b>. "
        "Each digit gives one row, called a <b>partial product</b>. Then you add the rows.</p>"
        "<h2>3-digit × 2-digit</h2>"
        "<p>Row 1 multiplies by the ones digit. Row 2 multiplies by the tens digit, so it starts with a "
        "<b>placeholder zero</b> (green) in the ones place.</p>"
        "<figure class='sn-fig'>" + lesson_fig(346, 27, "346 times 27 in columns") +
        "<figcaption>346 × 27: row 1 is 346 × 7 = 2,422. Row 2 is 346 × 20: write 0, then 346 × 2 = 692, so 6,920. "
        "2,422 + 6,920 = 9,342.</figcaption></figure>"
        "<h2>3-digit × 3-digit</h2>"
        "<p>A 3-digit bottom number gives <b>three rows</b>. The hundreds row starts with <b>two zeros</b>.</p>"
        "<figure class='sn-fig'>" + lesson_fig(253, 146, "253 times 146 in columns") +
        "<figcaption>253 × 146 = 1,518 + 10,120 + 25,300 = 36,938.</figcaption></figure>" +
        ex("Zero inside a number", "405 × 32 = ?",
           "Row 1: 5 × 2 = 10, write 0, regroup 1. 0 × 2 + 1 = 1. 4 × 2 = 8. So 405 × 2 = 810. "
           "Row 2: write 0, then 405 × 3 = 1,215, so 12,150. Add: 810 + 12,150 = 12,960.", "12,960") +
        "<h2>Estimate to check</h2>"
        "<p>Round each number to its greatest place and multiply in your head. 346 × 27 is about 300 × 30 = 9,000, "
        "so 9,342 makes sense. An answer like 3,114 or 93,420 is far off.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["No zero in row 2 (346 × 27 = 2,422 + 692)", "Row 2 is × 20, so write 0 first: 6,920"],
            ["Only one zero in the hundreds row", "× 100s needs two zeros: 253 × 100 = 25,300"],
            ["Forgetting a regrouped digit (346 × 7 = 2,182)", "Write it above the next column and add it"],
            ["Adding the regrouped digit first", "Multiply first, then add: 4 × 7 + 4 = 32"],
            ["Skipping the 0 in 405 (405 × 2 = 90)", "0 × 2 = 0, then add the regrouped 1: 810"],
        ])
    )


FAQ = [
    {"q": "How do you teach multi-digit multiplication in 5th grade?",
     "a": "Use the standard algorithm: one row for each digit of the bottom number, a placeholder zero for the tens row and two for the hundreds row, then add the rows. Ask children to estimate first so they can check the answer."},
    {"q": "Why do you add a zero when multiplying by a 2-digit number?",
     "a": "In 346 × 27 the 2 means 2 tens, so the second row is 346 × 20, not 346 × 2. The zero in the ones place makes the row 6,920 instead of 692."},
    {"q": "How do you multiply a 3-digit number by a 3-digit number?",
     "a": "Write three rows: the number times the ones digit, times the tens digit (one zero first), and times the hundreds digit (two zeros first). Add the three rows, for example 253 × 146 = 1,518 + 10,120 + 25,300 = 36,938."},
    {"q": "What does 5.NBT.B.5 mean?",
     "a": "It is the Common Core Grade 5 standard for fluently multiplying multi-digit whole numbers with the standard algorithm, for example a 3- or 4-digit number by a 2-digit number."},
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
    rnd = random.Random(509)
    P = People(rnd)
    seen = set()
    sets = [set_warm(rnd, seen), set_3x2(rnd, seen), set_4x2(rnd, seen), set_3x3(rnd, seen, P), set_story(rnd, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + it["e"]
            assert k not in keys, it["q"]
            keys.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "multi-digit-multiplication", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multi-Digit Multiplication: The Standard Algorithm",
        "seo_title": "Grade 5 Multi-Digit Multiplication Worksheets: Standard Algorithm for 3-Digit by 2-Digit and 3-Digit by 3-Digit",
        "short_title": "Multi-digit multiplication",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "5.NBT.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NBT/B/5/",
        "standard_text": "Fluently multiply multi-digit whole numbers using the standard algorithm.",
        "meta_desc": "Free Grade 5 multiplication worksheets: the standard algorithm for 3-digit by 2-digit, 4-digit by 2-digit and 3-digit by 3-digit numbers, placeholder zeros, zeros inside numbers, word problems and estimating to check. 100 practice questions with step-by-step answers.",
        "key_big": "Multiply by one digit at a time, one row per digit. Then add the rows.",
        "key_sub": "The tens row starts with one placeholder zero and the hundreds row with two: 346 × 27 = 2,422 + 6,920 = 9,342. Estimate first to check the answer.",
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
    mark_large(u, "[0-9]+ times [0-9]+(:| with partial products)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
