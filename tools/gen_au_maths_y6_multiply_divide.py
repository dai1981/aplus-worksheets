# -*- coding: utf-8 -*-
"""
Australia Year 6 Maths: Multiplying and dividing larger numbers (Australian Curriculum v9.0, AC9M6N09)
  python3 tools/gen_au_maths_y6_multiply_divide.py
3- and 4-digit × 2-digit (area model and long multiplication), division by 1- and 2-digit numbers
(short and long division), interpreting the remainder (round up, round down, fraction, decimal),
choosing the operation, and multi-step problems (school camp, fundraising, road trips).
Every answer and every wrong choice is computed here (wrong choices = real student mistakes:
no place-holder zero, a forgotten regrouped digit, a zero missing from the quotient, the remainder
misread, rounding the wrong way, the wrong operation). A wrong choice is never equal in value to another.
Australian style: 4-digit numbers have no separator (4536); 5+ digits use a no-break space (12 350).
Money in $ and c. HTML attributes use single quotes (no backslashes in the JSON). Australian English.
"""
import json, os, random, re
from decimal import Decimal
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
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


# ------------------------------------------------------------ numbers and text
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


def qr(q, r):
    return "%s r %d" % (f(q), r) if r else f(q)


def V(x):
    return Fraction(x)


def R(q, r):
    """Value key of a 'q r r' answer (never equal to a plain number)."""
    return ("r", q, r) if r else Fraction(q)


def dec(x):
    """Exact decimal text of a Fraction with a terminating decimal: 17/4 -> 4.25."""
    x = Fraction(x)
    d = Decimal(x.numerator) / Decimal(x.denominator)
    s = format(d.normalize(), "f")
    assert Fraction(s) == x, (x, s)
    return f(int(s.split(".")[0])) + ("." + s.split(".")[1] if "." in s else "")


def rdot(q, r):
    """The mistake of writing 'r 7' as '.7'."""
    return Fraction("%d.%d" % (q, r))


def money(x):
    x = Fraction(x)
    assert (x * 100).denominator == 1
    c = int(x * 100)
    if c % 100 == 0:
        return "$" + f(c // 100)
    return "$%s.%02d" % (f(c // 100), c % 100)


def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def mixed(x):
    x = Fraction(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return f(w)
    return (f(w) + " " if w else "") + fr(r, x.denominator)


def mx(w, n, d):
    return f(w) + " " + fr(n, d)


def positive(v):
    if isinstance(v, tuple):
        return v[1] > 0 and v[2] > 0
    if isinstance(v, str):
        return True
    return v > 0


def mcq(q, correct, cands, e):
    """correct and cands are (label, value). 4 choices with 4 different labels and values."""
    lab, val = correct
    seen_l, seen_v = {lab}, {val}
    pick = []
    for c, v in cands:
        if c in seen_l or v in seen_v or not positive(v):
            continue
        seen_l.add(c)
        seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [lab] + pick, "a": 0, "e": e}


def nmcq(q, ans, wrongs, e, unit=None, pre=""):
    """Number answer. unit = (one, many) or a plain suffix string; pre = '$'."""
    def lab(x):
        if isinstance(unit, tuple):
            return units(x, *unit)
        return pre + f(x) + ((" " + unit) if unit else "")
    return mcq(q, (lab(ans), V(ans)), [(lab(w), V(w)) for w in wrongs if w > 0], e)


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


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


def units(k, one, many):
    return "%s %s" % (f(k), one if k == 1 else many)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def parts(n):
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def svg_wrap(w, h, body, label, family=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(NB) * 0.55) * fs * 0.6


def text(x, y, t, fs=17, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def check_txt(n, d):
    q, r = divmod(n, d)
    if r:
        return "Check: %s × %d + %d = %s." % (f(q), d, r, f(n))
    return "Check: %s × %d = %s." % (f(q), d, f(n))


# ============================================================ multiplication figures
def area_svg(tops, lefts, cells, label):
    """Area model. cells[r][c] = text in each part ('' = empty, '?' = red question mark)."""
    FS = 17
    ws = []
    for c, t in enumerate(tops):
        need = max([tw(t, FS)] + [tw(cells[r][c], FS) for r in range(len(lefts))]) + 22
        base = {1: 62, 2: 92, 3: 120}.get(len(str(t)), 140)
        ws.append(max(need, base))
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 16)
    hs = [66, 46]
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


def area_cells(a, b):
    return [[p * q for p in parts(a)] for q in parts(b)]


def area_fig(a, b, show=None):
    pa = parts(a)
    cells = show or [[""] * len(pa) for _ in range(2)]
    return area_svg([f(p) for p in pa], [str(q) for q in parts(b)], cells,
                    "area model with %d parts: %d × %d" % (len(pa) * 2, a, b))


def column_svg(rows, rules, label, notes=None, big=False):
    """Long multiplication in columns, ones lined up on the right.
    rows = (sign, text[, nz]); nz = place-holder zeros at the end (green). sign 'ex' = small regrouped digits {place: digit}.
    text '[?]' = a red dashed box across the row."""
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
    return [(d, i, a * d * 10 ** i) for i, d in enumerate(digits(b))]


def work_svg(a, b, box=None):
    pr = pp_rows(a, b)
    rows = [("", str(a)), ("×", str(b))]
    for k, (d, i, v) in enumerate(pr):
        sg = "+" if k == len(pr) - 1 else ""
        rows.append((sg, "[?]") if box == k else (sg, str(v), i))
    rules = [1, len(rows) - 1]
    rows.append(("", str(a * b)))
    return column_svg(rows, rules, "%d times %d as long multiplication" % (a, b))


def wrong_work_svg(a, b, r0, r1, total, nz1):
    rows = [("", str(a)), ("×", str(b)), ("", str(r0)), ("+", str(r1), nz1), ("", str(total))]
    return column_svg(rows, [1, 3], "%d times %d as long multiplication with a mistake" % (a, b))


# ------------------------------------------------------------ multiplication text
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


def mult_row(a, d, mode="ok", k=None):
    """a × d (one digit) with a typical mistake. nocarry: forget every regrouped digit.
    skip: forget the one made in place k. cfirst: add the regrouped digit before multiplying."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        p = (x + c) * d if mode == "cfirst" else x * d + c
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
        t += (mult_row(a, d, mode, k) if only is None or only == j else a * d) * 10 ** i
    return t


def no_zero(a, b):
    return sum(a * d for d in digits(b))


def add_cols(nums, drop=None):
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


def carries(a, d):
    c, n = 0, 0
    for x in digits(a)[:-1]:
        c = (x * d + c) // 10
        n += 1 if c else 0
    return n


def mult_cands(a, b, rnd):
    pr = pp_rows(a, b)
    more = [total_with(a, b, "nocarry"), total_with(a, b, "cfirst"), add_cols([v for d, i, v in pr], drop="all")]
    more += [total_with(a, b, "nocarry", only=j) for j in range(2)]
    rnd.shuffle(more)
    return [no_zero(a, b)] + more + [a * (b % 10), total_with(a, b, "skip", k=0), total_with(a, b, "skip", k=1)]


def pick_m(rnd, seen, na, inner_zero=False):
    """a has na digits (no zeros, or one zero inside), b is 2-digit (digits 2-9, different). Every row regroups."""
    while True:
        a = rnd.randint(10 ** (na - 1) + 1, 10 ** na - 1)
        bd = rnd.sample(range(2, 10), 2)
        b = bd[0] * 10 + bd[1]
        da = digits(a)
        if inner_zero:
            if da[0] == 0 or da[-1] == 0 or da[1:-1].count(0) != 1:
                continue
        elif 0 in da:
            continue
        if len(set(da)) < len(da) - 1 or (a, b) in seen:
            continue
        if any(carries(a, d) == 0 for d in digits(b)):
            continue
        seen.add((a, b))
        return a, b


# ============================================================ set 1: multiplying
def area_compute(a, b, rnd):
    cells = area_cells(a, b)
    pa, pb = parts(a), parts(b)
    flat = [x for row in cells for x in row]
    tot = a * b
    wrong = [tot - cells[0][0] + cells[0][0] // 10,        # hundreds × tens with one zero too few
             tot - cells[0][-1],                            # left out a part
             tot - cells[1][0],
             no_zero(a, b), add_cols(flat, drop="all")]
    e = ("Partition %s = %s and %d = %d + %d. Multiply each pair: %s. Add the parts: %s = %s."
         % (f(a), " + ".join(f(p) for p in pa), b, pb[0], pb[1],
            ", ".join("%s × %d = %s" % (f(p), q, f(p * q)) for q in pb for p in pa),
            " + ".join(f(x) for x in flat), f(tot)))
    return nmcq(fig(area_fig(a, b)) + "Use the area model to find %s × %d." % (f(a), b), tot, wrong, e)


def area_missing(a, b, r, c):
    cells = area_cells(a, b)
    show = [[f(x) for x in row] for row in cells]
    show[r][c] = "?"
    p, q = parts(a)[c], parts(b)[r]
    v = p * q
    dp, dq = int(str(p)[0]), int(str(q)[0])
    zeros = len(str(p)) - 1 + len(str(q)) - 1
    e = ("This part is %s × %d. Use the fact %d × %d = %d, then write %d zero%s: %s × %d = %s."
         % (f(p), q, dp, dq, dp * dq, zeros, "" if zeros == 1 else "s", f(p), q, f(v)))
    return nmcq(fig(area_fig(a, b, show)) + "This area model shows %s × %d. What number goes in the part marked ?" % (f(a), b),
                v, [v // 10, v * 10, p + q, dp * dq, v + p], e)


def compute_item(a, b, rnd, col):
    q = (fig(col_problem(a, b)) + "Use long multiplication.") if col else "Use long multiplication to work out %s × %d." % (f(a), b)
    return nmcq(q, a * b, mult_cands(a, b, rnd), steps(a, b, detail=1))


def row2_item(a, b):
    d, i, v = pp_rows(a, b)[1]
    wrong = [a * d, mult_row(a, d, "nocarry") * 10, mult_row(a, d, "cfirst") * 10, v * 10]
    e = ("Row 2 multiplies by the tens digit, so it is %s × %d. Write the place-holder 0 first, then %s × %d: %s. "
         "The row is %s, not %s. Check: %s + %s = %s."
         % (f(a), d * 10, f(a), d, steps_1d(a, d), f(v), f(a * d), f(pp_rows(a, b)[0][2]), f(v), f(a * b)))
    return nmcq(fig(work_svg(a, b, box=1)) + "What number goes in the dashed box?", v, wrong, e)


MULT_WHY = ["Forgot the place-holder zero", "Forgot a regrouped digit", "Added the rows wrongly", "There is no mistake"]


def mult_mistake(a, b, kind, P):
    name, he, his = P.next()
    (d0, _, v0), (d1, _, v1) = pp_rows(a, b)
    if kind == 0:
        r0, r1, nz = v0, a * d1, 0
        tot = r0 + r1
        e = ("Row 2 multiplies by %d tens, so it must start with a place-holder 0: %s × %d = %s, not %s. "
             "The answer is %s + %s = %s." % (d1, f(a), d1 * 10, f(v1), f(a * d1), f(v0), f(v1), f(a * b)))
    else:
        r0, r1, nz = mult_row(a, d0, "nocarry"), v1, 1
        tot = r0 + r1
        e = ("Row 1 should be %s × %d = %s (%s). %s did not add the regrouped digits, so row 1 says %s. "
             "The answer is %s + %s = %s." % (f(a), d0, f(v0), steps_1d(a, d0), name, f(r0), f(v0), f(v1), f(a * b)))
    assert tot != a * b and r0 + r1 == tot
    q = fig(wrong_work_svg(a, b, r0, r1, tot, nz)) + "%s worked out %s × %d like this. What mistake did %s make?" % (name, f(a), b, he)
    return mcq(q, (MULT_WHY[kind], MULT_WHY[kind]), [(w, w) for i, w in enumerate(MULT_WHY) if i != kind], e)


def est_item(a, b):
    ra = rhu(a, 10 ** (len(str(a)) - 1))
    rb = rhu(b, 10)
    est = ra * rb
    e = ("Round each number: %s is about %s and %d is about %d. %s × %d = %s. The exact answer, %s, is close to it."
         % (f(a), f(ra), b, rb, f(ra), rb, f(est), f(a * b)))
    return mcq("Which is the best estimate for %s × %d?" % (f(a), b), ("about " + f(est), V(est)),
               [("about " + f(est // 10), V(est // 10)), ("about " + f(est * 10), V(est * 10)),
                ("about " + f(ra + rb), V(ra + rb))], e)


def set_multiply(rnd, seen, P):
    its = []
    for _ in range(3):
        a, b = pick_m(rnd, seen, 3)
        its.append(area_compute(a, b, rnd))
    for r, c in ((0, 0), (0, 1)):
        a, b = pick_m(rnd, seen, 3)
        its.append(area_missing(a, b, r, c))
    for i in range(4):
        a, b = pick_m(rnd, seen, 3)
        its.append(compute_item(a, b, rnd, i % 2 == 0))
    a, b = pick_m(rnd, seen, 3, inner_zero=True)
    its.append(compute_item(a, b, rnd, False))
    for i in range(4):
        a, b = pick_m(rnd, seen, 4)
        its.append(compute_item(a, b, rnd, i % 2 == 1))
    a, b = pick_m(rnd, seen, 4, inner_zero=True)
    its.append(compute_item(a, b, rnd, True))
    for na in (3, 4):
        a, b = pick_m(rnd, seen, na)
        its.append(row2_item(a, b))
    for kind in (0, 1):
        a, b = pick_m(rnd, seen, 3)
        its.append(mult_mistake(a, b, kind, P))
    a, b = pick_m(rnd, seen, 4)
    its.append(est_item(a, b))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "3- and 4-digit numbers × 2-digit numbers: area model and long multiplication", "items": its}


# ============================================================ division figures and text
def sd_rows(n, d):
    rows, carry, started = [], 0, False
    ds = str(n)
    for i, ch in enumerate(ds):
        cur = carry * 10 + int(ch)
        q, carry = divmod(cur, d)
        if q or started or i == len(ds) - 1:
            started = True
            rows.append((i, cur, q, carry))
        else:
            rows.append((i, cur, None, carry))
    return rows


def sd_steps(n, d):
    rows = sd_rows(n, d)
    L = len(rows)
    parts_ = []
    for i, cur, q, c in rows:
        if q is None:
            parts_.append("%d does not go into %d, so carry the %d to make %d" % (d, cur, cur, rows[i + 1][1]))
        elif q == 0 and i < L - 1:
            parts_.append("%d does not go into %d, so write 0 in the quotient%s"
                          % (d, cur, (" and carry the %d to make %d" % (c, rows[i + 1][1])) if c else ""))
        elif q == 0:
            parts_.append("%d does not go into %d, so write 0 in the quotient and the remainder is %d" % (d, cur, c))
        elif c and i < L - 1:
            parts_.append("%d ÷ %d = %d r %d, carry the %d to make %d" % (cur, d, q, c, c, rows[i + 1][1]))
        elif c:
            parts_.append("%d ÷ %d = %d r %d" % (cur, d, q, c))
        else:
            parts_.append("%d ÷ %d = %d" % (cur, d, q))
    q, r = divmod(n, d)
    return "; ".join(parts_) + ". Answer: %s. %s" % (qr(q, r), check_txt(n, d))


def bus_svg(n, d, fs=24):
    """Short division ('bus stop') layout, not worked."""
    ds = str(n)
    L = len(ds)
    cw = fs * 0.78
    dw = len(str(d)) * fs * 0.62
    x0 = 8 + dw + 14
    top = 6
    bh = fs * 1.3
    by = top + bh - fs * 0.3
    s = []
    for j, ch in enumerate(ds):
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x0 + fs * 0.62 + cw * j, by, fs, INK, ch))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 8, by, fs, GREEN, d))
    right = x0 + fs * 0.62 + cw * (L - 1) + fs * 0.5
    s.append("<path d='M%.1f %.1f V%.1f M%.1f %.1f H%.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0, top + bh, top, x0 - 1.5, top, right, INK))
    return svg_wrap(int(right + 7), int(top + bh + 7), "".join(s), "%s divided by %d written as short division" % (f(n), d), "monospace")


def ld_rows(n, d):
    ds = [int(c) for c in str(n)]
    cur, out, started = 0, [], False
    for i, x in enumerate(ds):
        cur = cur * 10 + x
        if not started and cur < d and i < len(ds) - 1:
            continue
        started = True
        q = cur // d
        out.append((i, cur, q))
        cur -= q * d
    return out, cur


def ld_steps(n, d):
    ds = str(n)
    rows, r = ld_rows(n, d)
    q = n // d
    out = []
    for k, (i, cur, qd) in enumerate(rows):
        if k == 0:
            head = ("%d is less than %d, so start with %d. " % (int(ds[:i]), d, cur)) if i > 0 else ""
            out.append(head + "%d ÷ %d = %d: %d × %d = %d, %d − %d = %d."
                       % (cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
        elif cur == 0:
            out.append("Bring down %s: there is nothing to divide, so write 0 in the quotient." % ds[i])
        elif qd == 0:
            out.append("Bring down %s to make %d: %d does not go into %d, so write 0 in the quotient." % (ds[i], cur, d, cur))
        else:
            out.append("Bring down %s to make %d: %d ÷ %d = %d: %d × %d = %d, %d − %d = %d."
                       % (ds[i], cur, cur, d, qd, qd, d, qd * d, cur, qd * d, cur - qd * d))
    if r:
        out.append("Nothing is left to bring down, so the remainder is %d." % r)
    out.append("Answer: %s. %s" % (qr(q, r), check_txt(n, d)))
    return " ".join(out)


def div_steps(n, d):
    return sd_steps(n, d) if d < 10 else ld_steps(n, d)


def ld_svg(n, d, fs=24, work=False):
    """Long division layout. With work=True the full worked example is drawn."""
    cw = fs * 0.85
    ds = str(n)
    L = len(ds)
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18 + (cw if work else 0)
    rows, r = ld_rows(n, d)
    q = n // d
    rh = fs * 1.25
    top = (rh + 6) if work else 6
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for k, ch in enumerate(reversed(txt)):
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - k), y, fs, colr, ch))

    bh = rh + 2
    by = top + bh - fs * 0.3
    digits_at(ds, L - 1, by)
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    W = x0 + cw * L + 8
    H = top + bh + 6
    if work:
        digits_at(str(q), L - 1, top - 8, GREEN)
        if r:
            rt = "r %d" % r
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>"
                     % (x0 + cw * L + 10, top - 8, fs, GREEN, rt))
            W = max(W, x0 + cw * L + 10 + len(rt) * fs * 0.62 + 8)
        y = by
        for k, (i, cur, qd) in enumerate(rows):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(left) - cw * 0.9, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.3, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            if k + 1 < len(rows):
                digits_at(str(rows[k + 1][1]), rows[k + 1][0], y)
                for j in range(i + 1, rows[k + 1][0] + 1):
                    s.append("<path d='M%.1f %.1f V%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 3' "
                             "marker-end='url(#ah)'/>" % (col(j), by + fs * 0.3, y - fs * 0.95, GREEN))
            else:
                digits_at(str(cur - p), i, y, GREEN if cur - p else INK)
        H = y + 12
        s.insert(0, "<defs><marker id='ah' viewBox='0 0 10 10' refX='10' refY='5' markerWidth='6' markerHeight='6' "
                    "orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='%s'/></marker></defs>" % GREEN)
    s.append("<path d='M%.1f %.1f V%.1f M%.1f %.1f H%.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 8, top + bh, top, x0 - 9.5, top, x0 + cw * L + 4, INK))
    label = ("%s divided by %d worked out with long division" if work else "%s divided by %d written as long division") % (f(n), d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


def rhu(x, p):
    """Round half up to a multiple of p (Python's round() rounds 25 to 20)."""
    return (x + p // 2) // p * p


def drop_zero(q):
    s = str(q).replace("0", "")
    return int(s) if s else 0


def div_cands(n, d):
    q, r = divmod(n, d)
    c = []
    if "0" in str(q):
        c.append((qr(drop_zero(q), r), R(drop_zero(q), r)))           # missed a zero in the quotient
    if r:
        c += [(qr(q - 1, r + d), R(q - 1, r + d)),                    # remainder bigger than the divisor
              (f(q), V(q)),                                           # left the remainder out
              (qr(q, d - r), R(q, d - r))]                            # wrote what is missing
    c += [(qr(q * 10, r), R(q * 10, r)), (qr(q + 1, r), R(q + 1, r)), (qr(q - 1, r), R(q - 1, r)),
          (qr(q + 10, r), R(q + 10, r))]
    return c


def div_item(n, d, figure):
    q, r = divmod(n, d)
    how = "short division" if d < 10 else "long division"
    if figure:
        qt = fig(bus_svg(n, d) if d < 10 else ld_svg(n, d)) + "Use %s." % how
    else:
        qt = "Use %s to work out %s ÷ %d." % (how, f(n), d)
    return mcq(qt, (qr(q, r), R(q, r)), div_cands(n, d), div_steps(n, d))


def pick_div(rnd, used, lo, hi, ds, rem, zero=False, rmin=2):
    while True:
        d = rnd.choice(ds)
        if rem:
            n = rnd.randint(lo, hi)
        else:
            n = rnd.randint(-(-lo // d), hi // d) * d
        q, r = divmod(n, d)
        if not (lo <= n <= hi) or n in used or n % 10 == 0 or q < 10:
            continue
        if bool(r) != rem or (rem and (r < rmin or r == q % 10)):
            continue
        if ("0" in str(q)) != zero:
            continue
        if d < 10 and sum(1 for row in sd_rows(n, d)[:-1] if row[3]) < 2:
            continue
        used.add(n)
        return n, d


TWO = [d for d in range(13, 49) if d % 10 and d not in (20, 25, 30, 40)]


# ============================================================ set 2: dividing
def set_divide(rnd, used, P):
    its = []
    for i, (rem, zero) in enumerate([(False, False), (False, False), (False, True), (True, False), (True, True)]):
        n, d = pick_div(rnd, used, 1000, 9999, [3, 4, 6, 7, 8, 9], rem, zero)
        its.append(div_item(n, d, i % 2 == 0))
    for i, (lo, hi, rem) in enumerate([(300, 999, False), (300, 999, False), (300, 999, True), (300, 999, True),
                                       (1000, 9999, False), (1000, 9999, False), (1000, 9999, True)]):
        n, d = pick_div(rnd, used, lo, hi, TWO, rem)
        its.append(div_item(n, d, i % 2 == 1))
    # the remainder only
    n, d = pick_div(rnd, used, 1000, 9999, TWO, True)
    q, r = divmod(n, d)
    its.append(mcq("What is the remainder when %s is divided by %d?" % (f(n), d), (str(r), V(r)),
                   [(str(d - r), V(d - r)), (str(r + d), V(r + d)), (f(q), V(q)), (str(d), V(d))],
                   "The question asks for the remainder, not the quotient. " + ld_steps(n, d)))
    # check with the inverse
    n, d = pick_div(rnd, used, 1000, 9999, TWO, True)
    q, r = divmod(n, d)
    its.append(mcq("%s ÷ %d = %s. Which calculation checks this answer?" % (f(n), d, qr(q, r)),
                   ("%s × %d + %d" % (f(q), d, r), "ok"),
                   [("%s × %d − %d" % (f(q), d, r), "m"), ("%s × %d + %d" % (f(q), r, d), "s"), ("%s × %d + %d" % (f(n), d, r), "n")],
                   "Multiply the quotient by the divisor, then add the remainder: %s × %d = %s and %s + %d = %s."
                   % (f(q), d, f(q * d), f(q * d), r, f(n))))
    n, d = pick_div(rnd, used, 1000, 9999, [6, 7, 8, 9], False)
    q = n // d
    its.append(mcq("%s ÷ %d = %s. Which calculation checks this answer?" % (f(n), d, f(q)), ("%s × %d" % (f(q), d), "ok"),
                   [("%s × %d" % (f(n), d), "n"), ("%s ÷ %d" % (f(q), d), "d"), ("%s + %d" % (f(q), d), "a")],
                   "Multiplication is the inverse of division: %s × %d = %s, so the answer is right." % (f(q), d, f(n))))
    # missed a zero in the quotient
    WHY = ["Missed a 0 in the quotient", "The remainder is too big", "Left out the remainder", "There is no mistake"]
    for ds, lo, hi in (([4, 6, 7], 1000, 9999), (TWO, 1000, 9999)):
        name, he, his = P.next()
        while True:
            n, d = pick_div(rnd, used, lo, hi, ds, False, zero=True)
            if drop_zero(n // d) >= 10:
                break
        q = n // d
        wq = drop_zero(q)
        its.append(mcq("%s works out %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, f(wq), he), (WHY[0], WHY[0]),
                       [(w, w) for i, w in enumerate(WHY) if i],
                       "Check: %s × %d = %s, not %s. When %d does not go into the number, write 0 in the quotient. "
                       % (f(wq), d, f(wq * d), f(n), d) + div_steps(n, d)))
    # remainder too big
    name, he, his = P.next()
    while True:
        n, d = pick_div(rnd, used, 1000, 9999, TWO, True)
        q, r = divmod(n, d)
        if r + d < 100:
            break
    its.append(mcq("%s works out %s ÷ %d = %s. What mistake did %s make?" % (name, f(n), d, qr(q - 1, r + d), he), (WHY[1], WHY[1]),
                   [(w, w) for i, w in enumerate(WHY) if i != 1],
                   "A remainder must be less than the divisor. %d is more than %d, so %d goes in once more: %d − %d = %d. "
                   "The answer is %s. %s" % (r + d, d, d, r + d, d, r, qr(q, r), check_txt(n, d))))
    # estimate
    for D, k in ((30, 2), (40, 3)):
        while True:
            d = D + rnd.choice([-2, -1, 1, 2])
            n = k * D * 100 + rnd.randint(-150, 150)
            if n not in used and n % 10 and n % d:
                break
        used.add(n)
        est = k * 100
        its.append(mcq("Which is the best estimate for %s ÷ %d?" % (f(n), d), ("about " + f(est), V(est)),
                       [("about " + f(k * 10), V(k * 10)), ("about " + f(k * 1000), V(k * 1000)),
                        ("about " + f(k * D * 100), V(k * D * 100))],
                       "Round to numbers that divide easily: %s is about %s and %d is about %d. %s ÷ %d = %s. "
                       "The exact answer is %s." % (f(n), f(k * D * 100), d, D, f(k * D * 100), D, f(est), qr(n // d, n % d))))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Dividing by 1- and 2-digit numbers: short and long division", "items": its}


# ============================================================ set 3: interpret the remainder
def ctx(rnd, used, lo, hi, ds, frac=False, money5=False, rmin=2):
    while True:
        d = rnd.choice(ds)
        n = rnd.randint(lo, hi)
        q, r = divmod(n, d)
        if n in used or r < rmin or r in (q, q + 1, q - 1, q % 10) or n % 10 == 0 or q < 3:
            continue
        if frac and Fraction(r, d).denominator != d:
            continue
        if money5 and (Fraction(n, d) * 20).denominator != 1:
            continue
        used.add(n)
        return n, d


UP = [
    ("{n} students and teachers are going to the Year 6 camp. Each coach has {d} seats.", "How many coaches are needed?",
     "coach", "coaches", "person", "people", [45, 48, 53, 57], (150, 260)),
    ("{n} people are coming to the school musical. The chairs are set out in rows of {d}.", "How many rows are needed so everyone has a seat?",
     "row", "rows", "person", "people", [18, 22, 24], (300, 600)),
    ("A school needs {n} exercise books for next year. They come in boxes of {d}.", "How many boxes must the school order?",
     "box", "boxes", "book", "books", [36, 48], (700, 1500)),
    ("{n} Year 6 students are going to the swimming carnival. Each minibus has {d} seats for students.", "How many minibuses are needed?",
     "minibus", "minibuses", "student", "students", [12, 14], (80, 170)),
]
DOWN = [
    ("A farm has {n} eggs. It packs them into trays of {d}.", "How many full trays can it pack?",
     "tray", "trays", "egg", "eggs", "fill", [30, 36], (500, 1200)),
    ("A bakery makes {n} lamingtons. Each box holds {d} lamingtons.", "How many boxes can be filled?",
     "box", "boxes", "lamington", "lamingtons", "fill", [12, 16], (300, 700)),
    ("A school has ${n} to spend on new basketballs. Each basketball costs ${d}.", "How many basketballs can the school buy?",
     "basketball", "basketballs", "dollar", "dollars", "buy", [27, 34, 38], (500, 999)),
    ("{n} students sign up for the summer cricket competition. Each team needs exactly {d} players.", "How many full teams can be made?",
     "team", "teams", "student", "students", "make", [11], (150, 300)),
]


def set_remainders(rnd, used, P):
    its = []
    for text_, qtxt, one, many, lo1, lom, ds, (lo, hi) in UP:
        n, d = ctx(rnd, used, lo, hi, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        e = ("%s ÷ %d = %s. %s hold %s × %d = %s %s. %s still %s a place, so you need 1 more: %s. Round up."
             % (f(n), d, qr(q, r), U(q), f(q), d, f(q * d), lom, cap(units(r, lo1, lom)), "needs" if r == 1 else "need", U(q + 1)))
        if one == "box":
            e = ("%s ÷ %d = %s. %s hold %s × %d = %s books. The school still needs %d more %s, so it must order 1 more box: %s. Round up."
                 % (f(n), d, qr(q, r), U(q), f(q), d, f(q * d), r, lo1 if r == 1 else lom, U(q + 1)))
        its.append(mcq(text_.format(n=f(n), d=d) + " " + qtxt, (U(q + 1), V(q + 1)),
                       [(U(q), V(q)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q + 2), V(q + 2))], e))
    for text_, qtxt, one, many, lo1, lom, verb, ds, (lo, hi) in DOWN:
        n, d = ctx(rnd, used, lo, hi, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        left = ("$%d" % r, "is") if lo1 == "dollar" else (units(r, lo1, lom), "is" if r == 1 else "are")
        e = ("%s ÷ %d = %s. The %s left over %s not enough to %s another %s, so ignore the remainder. Round down: %s."
             % (f(n), d, qr(q, r), left[0], left[1], verb, one, U(q)))
        its.append(mcq(text_.format(n=f(n), d=d) + " " + qtxt, (U(q), V(q)),
                       [(U(q + 1), V(q + 1)), (qr(q, r), R(q, r)), (U(r), V(r)), (U(q - 1), V(q - 1))], e))
    # the remainder is the answer
    for text_, one, many, ds, (lo, hi) in [
        ("A coach shares {n} tennis balls equally between {d} schools. Each school gets as many as possible. How many balls are left over?",
         "ball", "balls", [14, 16], (300, 600)),
        ("{n} students line up in rows of {d} for the school photo. How many students are in the last row, which is not full?",
         "student", "students", [18, 24], (300, 600))]:
        n, d = ctx(rnd, used, lo, hi, ds)
        q, r = divmod(n, d)
        U = lambda k: units(k, one, many)
        its.append(mcq(text_.format(n=f(n), d=d), (U(r), V(r)),
                       [(U(q), V(q)), (U(d - r), V(d - r)), (qr(q, r), R(q, r)), (U(r + d), V(r + d))],
                       "%s ÷ %d = %s. The question asks how many are left over, so the remainder is the answer: %s."
                       % (f(n), d, qr(q, r), U(r))))
    # as a mixed numeral
    for ds, lo, hi in (([6, 7], 100, 300), ([8], 100, 300), ([12], 100, 300)):
        n, d = ctx(rnd, used, lo, hi, ds, frac=True)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        cands = [(mx(q, r, 10), q + Fraction(r, 10)), (mixed(q + Fraction(d - r, d)), q + Fraction(d - r, d)),
                 (mixed(q + 1 + Fraction(r, d)), q + 1 + Fraction(r, d))]
        if r < q:
            cands.insert(1, (mx(q, r, q), q + Fraction(r, q)))
        its.append(mcq("Work out %d ÷ %d. Give your answer as a mixed numeral." % (n, d), (mixed(x), x), cands,
                       "%s The remainder %d is %d out of %d, so it is %s. Answer: %s."
                       % (div_steps(n, d).split(" Check")[0].replace("Answer: ", "So the quotient is "), r, r, d, fr(r, d), mixed(x))))
    # as a decimal (money)
    for text_, ds, (lo, hi) in [
        ("{d} friends share a ${n} prize from the school art show equally. How much does each friend get?", [4, 8], (101, 399)),
        ("The Year 6 class raised ${n} at a cake stall. It is shared equally between {d} charities. How much does each charity get?", [5, 4], (301, 899)),
        ("A family pays ${n} for {d} nights at a caravan park. Each night costs the same. How much is one night?", [20, 8], (301, 899))]:
        n, d = ctx(rnd, used, lo, hi, ds, money5=True)
        q, r = divmod(n, d)
        x = Fraction(n, d)
        rf = Fraction(r, d)
        cands = [(money(rdot(q, r)), rdot(q, r)),
                 ("$" + qr(q, r), R(q, r)), (money(q), V(q)), (money(q + 1 - rf), q + 1 - rf)]
        its.append(mcq(text_.format(n=f(n), d=d), (money(x), x), cands,
                       "%s ÷ %d = %s. Dollars can be shared as cents, so share the $%d left over: $%d ÷ %d = %dc. "
                       "Each share is %s, not %s." % (f(n), d, qr(q, r), r, r, d, int(rf * 100), money(x), cands[0][0])))
    # which way?
    WAYS = ["Round up", "Round down", "The remainder is the answer", "Share it as a decimal"]
    for text_, k, why, ds, (lo, hi), money5 in [
        ("{n} people are going to a footy final by bus. Each bus seats {d}. {n} ÷ {d} = {qr}. To find how many buses are needed,", 0,
         "Everyone needs a seat, so the left-over people need 1 more bus. Round up: {res}.", [52, 57], (300, 700), False),
        ("A nursery has {n} seedlings. It plants them in trays of {d}. {n} ÷ {d} = {qr}. To find how many trays are full,", 1,
         "A tray with fewer than {d} seedlings is not full, so ignore the remainder. Round down: {res}.", [24, 32], (500, 900), False),
        ("{d} friends split a ${n} restaurant bill equally. {n} ÷ {d} = {qr}. To find how much each person pays,", 3,
         "Money can be split into cents, so the left-over dollars are shared too. Each person pays {res}.", [4], (101, 199), True)]:
        n, d = ctx(rnd, used, lo, hi, ds, money5=money5)
        q, r = divmod(n, d)
        res = units(q + 1, "bus", "buses") if k == 0 else units(q, "full tray", "full trays") if k == 1 else money(Fraction(n, d))
        its.append(mcq(text_.format(n=f(n), d=d, qr=qr(q, r)) + " what should you do with the remainder?", (WAYS[k], WAYS[k]),
                       [(w, w) for i, w in enumerate(WAYS) if i != k], why.format(d=d, res=res)))
    # rounded the wrong way
    name, he, his = P.next()
    n, d = ctx(rnd, used, 300, 600, [42, 46])
    q, r = divmod(n, d)
    its.append(mcq("%s students are going on a school excursion. Each bus has %d seats. %s works out %s ÷ %d = %s "
                   "and says %d buses are needed. What is the right answer?" % (f(n), d, name, f(n), d, qr(q, r), q),
                   ("Round up: %d buses" % (q + 1), "u"),
                   [("%s is right: %d buses" % (name, q), "k"), ("Use the remainder: %s" % units(r, "bus", "buses"), "r"),
                    ("Round down: %d buses" % (q - 1), "d")],
                   "%d buses only seat %d × %d = %s students. The other %d students still need seats, so %s rounded the wrong way. "
                   "Round up: %d buses." % (q, q, d, f(q * d), r, name, q + 1)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "What does the remainder mean? Round up, round down, fraction or decimal", "items": its}


# ============================================================ set 4: choose the operation
NS = [  # (text, op, a range, b range)
    ("The school hall has {a} rows of chairs with {b} chairs in each row. Which number sentence gives the number of chairs?",
     "×", (18, 32), (14, 26)),
    ("A vineyard has {a} rows of grapevines with {b} vines in each row. Which number sentence gives the number of vines?",
     "×", (120, 240), (35, 68)),
    ("The canteen sold {a} sausage rolls in Term 1. It sold {b} times as many in the whole year. Which number sentence gives how many it sold in the whole year?",
     "×", (215, 380), (3, 4)),
    ("A school buys {b} new netballs at ${a} each. Which number sentence gives the total cost?",
     "×", (23, 39), (12, 18)),
    ("{a} students are split into equal teams of {b}. Which number sentence gives the number of teams?",
     "÷", (12, 24), (12, 16)),
    ("A {a} m roll of fencing wire is cut into {b} equal pieces. Which number sentence gives the length of each piece?",
     "÷", (14, 32), (16, 24)),
    ("A school pays ${a} for {b} new chairs. Each chair costs the same. Which number sentence gives the cost of one chair?",
     "÷", (45, 95), (24, 36)),
    ("{name} runs laps of a {b} m track. How many laps must {he} run to cover {a} m? Which number sentence gives the answer?",
     "÷", (8, 15), (400, 400)),
    ("A plane has {a} seats. {b} seats are taken. Which number sentence gives the number of empty seats?",
     "−", (280, 420), (150, 260)),
    ("{a} people watch the first cricket match and {b} people watch the second. Which number sentence gives how many people watched altogether?",
     "+", (1200, 3800), (1400, 3600)),
]


def ns_item(rnd, P, text_, op, ar, br):
    name, he, his = P.next()
    b = rnd.randint(*br)
    if op == "÷":
        a = rnd.randint(*ar) * b
    else:
        a = rnd.randint(*ar)
    assert op != "−" or b < a
    labs = {"×": "%s × %s" % (f(a), f(b)), "÷": "%s ÷ %s" % (f(a), f(b)), "r": "%s ÷ %s" % (f(b), f(a)),
            "+": "%s + %s" % (f(a), f(b)), "−": "%s − %s" % (f(a), f(b))}
    order = {"×": ["÷", "+", "−"], "÷": ["r", "×", "−"], "+": ["×", "−", "÷"], "−": ["+", "÷", "×"]}[op]
    q_txt = text_.format(a=f(a), b=f(b), name=name, he=he)
    if op == "×":
        why = "Equal groups put together, so multiply: %s = %s." % (labs["×"], f(a * b))
        if "times as many" in text_:
            why = "“%d times as many” means multiply: %s = %s." % (b, labs["×"], f(a * b))
    elif op == "÷":
        why = ("You know the total and the size of each group (or the number of groups), so divide. Put the total first: %s = %s. "
               "%s ÷ %s is the wrong way round." % (labs["÷"], f(a // b), f(b), f(a)))
    elif op == "−":
        why = "Find the difference between all the seats and the taken seats, so subtract: %s = %s." % (labs["−"], f(a - b))
    else:
        why = "Two different amounts are put together, so add: %s = %s." % (labs["+"], f(a + b))
    return mcq(q_txt, (labs[op], op), [(labs[o], o) for o in order], why)


SOLVE = [
    ("÷", "{a} students sign up for summer cricket. They are put into equal teams of {b}. How many teams are there?",
     "team", "teams", (14, 24), [11]),
    ("÷", "The P&C raises ${a} at the school fete. It shares the money equally between {b} classes. How much does each class get?",
     "$", None, (115, 245), [12, 14, 16]),
    ("÷", "A {a} km road trip is driven in {b} days, the same distance each day. How far is driven each day?",
     "km", "km", (215, 385), [6, 7, 8]),
    ("×", "A school buys {a} boxes of pencils. Each box holds {b} pencils. How many pencils is that?",
     "pencil", "pencils", (124, 286), [24, 36, 48]),
    ("×", "An excursion to the aquarium costs ${b} for each student. {a} students are going. What is the total cost?",
     "$", None, (64, 96), [27, 32]),
    ("÷", "{name} read {a} pages over the holidays. {his_c} brother read {b} pages. How many times as many pages did {name} read?",
     "time", "times", (4, 9), [125, 138, 146]),
]


def solve_item(rnd, P, op, text_, one, many, ar, bs):
    name, he, his = P.next()
    b = rnd.choice(bs)
    k = rnd.randint(*ar)
    if op == "÷":
        a, ans = k * b, k
    else:
        a, ans = k, k * b
    if "times as many pages" in text_:
        e = ("“How many times as many” means divide the bigger number by the smaller one: %s ÷ %d = %d. "
             "So %s read %d times as many pages. %s − %d = %s finds how many more pages, not how many times as many."
             % (f(a), b, ans, name, ans, f(a), b, f(a - b)))
        wrong = [a - b, ans + 1, a + b]
        q_txt = text_.format(a=f(a), b=f(b), name=name, his_c=cap(his))
        return mcq(q_txt, (units(ans, one, many), V(ans)), [(units(w, one, many), V(w)) for w in wrong], e)
    q_txt = text_.format(a=f(a), b=f(b), name=name, he=he)
    if op == "÷":
        wrong = [a * b, a - b, ans * 10 if "0" not in str(ans) else drop_zero(ans), ans + 1]
        e = "Share or group the total, so divide: " + div_steps(a, b)
    else:
        wrong = [a + b, no_zero(a, b) if b > 9 else a * b * 10, total_with(a, b, "nocarry") if b > 9 else a * b + b, a * (b % 10)]
        e = "Equal groups put together, so multiply. " + (steps(a, b) if b > 9 else "%s × %d = %s." % (f(a), b, f(a * b)))
    if one == "$":
        return nmcq(q_txt, ans, wrong, e, pre="$")
    if one == many:
        return nmcq(q_txt, ans, wrong, e, unit=one)
    return nmcq(q_txt, ans, wrong, e, unit=(one, many))


OP_WHY = ["Should have divided", "Should have multiplied", "Forgot the place-holder zero", "There is no mistake"]


def set_operation(rnd, used, P):
    its = []
    for t in NS:
        its.append(ns_item(rnd, P, *t))
    for t in SOLVE:
        its.append(solve_item(rnd, P, *t))
    # what mistake?
    name, he, his = P.next()
    b = rnd.choice([24, 28, 32])
    k = rnd.randint(13, 19)
    a = k * b
    its.append(mcq("%s chocolates are packed into boxes of %d. %s works out %s × %d = %s boxes. What mistake did %s make?"
                   % (f(a), b, name, f(a), b, f(a * b), he), (OP_WHY[0], OP_WHY[0]), [(w, w) for i, w in enumerate(OP_WHY) if i],
                   "Packing a total into groups of %d is division, not multiplication. %s ÷ %d = %d boxes. "
                   "%s boxes is far more than the number of chocolates, so it cannot be right." % (b, f(a), b, k, f(a * b))))
    name, he, his = P.next()
    b = rnd.choice([26, 34, 38])
    k = rnd.randint(14, 22)
    tot = k * b
    its.append(mcq("A footy club pays $%d for each of its %d players to go to a training camp. %s works out the total cost as "
                   "%d ÷ %d = %s. What mistake did %s make?" % (b, k, name, b, k, qr(b // k, b % k), he),
                   (OP_WHY[1], OP_WHY[1]), [(w, w) for i, w in enumerate(OP_WHY) if i != 1],
                   "Each player costs the same amount, so the total is equal groups put together: multiply. "
                   "$%d × %d = $%s." % (b, k, f(tot))))
    name, he, his = P.next()
    a, b = pick_m(rnd, set(), 3)
    its.append(mcq("A school orders %d packs of paper. Each pack has %s sheets. %s works out %d × %s = %s sheets. What mistake did %s make?"
                   % (b, f(a), name, b, f(a), f(no_zero(a, b)), he), (OP_WHY[2], OP_WHY[2]), [(w, w) for i, w in enumerate(OP_WHY) if i != 2],
                   "Multiplying is right, but the answer is too small: %d × %s is about %d × %s = %s. "
                   % (b, f(a), rhu(b, 10), f(rhu(a, 100)), f(rhu(b, 10) * rhu(a, 100))) + steps(a, b)))
    name, he, his = P.next()
    b = rnd.choice([14, 16, 18])
    k = rnd.randint(21, 38)
    a = k * b
    its.append(mcq("%s students are split into %d equal groups for a science excursion. %s works out %s ÷ %d = %d students in each group. "
                   "What mistake did %s make?" % (f(a), b, name, f(a), b, k, he), (OP_WHY[3], OP_WHY[3]), [(w, w) for i, w in enumerate(OP_WHY) if i != 3],
                   "Sharing the students equally into groups is division, and %d × %d = %s, so %s is right." % (k, b, f(a), name)))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Choose the operation: multiply or divide?", "items": its}


# ============================================================ set 5: multi-step problems
def ceil(n, d):
    return -(-n // d)


def set_multistep(rnd, used, P):
    its = []
    R_ = rnd

    # 1 camp: cost per student plus coach hire
    s, c, bus = R_.randint(54, 88), R_.choice([185, 215, 245, 265]), R_.choice([1450, 1680, 1860])
    tot = s * c + bus
    its.append(nmcq("Year 6 camp costs $%d for each student, plus $%d to hire the coaches. %d students are going. What is the total cost?"
                    % (c, bus, s), tot, [s * c, s * (c + bus), no_zero(c, s) + bus, s * c - bus],
                    "Step 1: %d × $%d = $%s. Step 2: add the coach hire: $%s + $%d = $%s." % (s, c, f(s * c), f(s * c), bus, f(tot)), pre="$"))

    # 2 camp: coaches for students and teachers
    while True:
        s, t, k = R_.randint(130, 190), R_.randint(8, 12), R_.choice([45, 48, 53])
        if ceil(s + t, k) != ceil(s, k) and (s + t) % k:
            break
    ans = ceil(s + t, k)
    its.append(nmcq("%d students and %d teachers are going to camp. Each coach has %d seats. How many coaches are needed?"
                    % (s, t, k), ans, [ceil(s, k), (s + t) // k, (s + t) % k, ans + 1],
                    "Step 1: %d + %d = %d people. Step 2: %d ÷ %d = %s. The %d people left over still need seats, "
                    "so round up: %d coaches." % (s, t, s + t, s + t, k, qr((s + t) // k, (s + t) % k), (s + t) % k, ans),
                    unit=("coach", "coaches")))

    # 3 camp: share the cost per student
    s = R_.choice([56, 64, 72])
    per = R_.randint(9, 15)
    bus = s * per
    entry = R_.choice([18, 22, 26])
    ans = entry + per
    its.append(nmcq("On camp, %d students visit a wildlife park. Entry is $%d for each student, and the bus costs $%s for the group. "
                    "The bus cost is shared equally between the students. How much does each student pay altogether?"
                    % (s, entry, f(bus)), ans, [entry + bus, per, entry * s + bus, entry],
                    "Step 1: share the bus: $%s ÷ %d = $%d each. Step 2: add the entry: $%d + $%d = $%d."
                    % (f(bus), s, per, entry, per, ans), pre="$"))

    # 4 camp: tents (round up), then the cost
    while True:
        s, k, c = R_.randint(110, 170), R_.choice([4, 6]), R_.choice([18, 24, 35])
        if s % k:
            break
    tents = ceil(s, k)
    its.append(nmcq("%d students are going on camp. Each tent sleeps %d students. Each tent costs $%d to hire. What is the cost of the tents?"
                    % (s, k, c), tents * c, [(s // k) * c, s * c, tents + c, (tents + 1) * c],
                    "Step 1: %d ÷ %d = %s, so round up: %d tents. Step 2: %d × $%d = $%s."
                    % (s, k, qr(s // k, s % k), tents, tents, c, f(tents * c)), pre="$"))

    # 5 fundraising: sales minus costs
    n, p, cost = R_.randint(136, 248), R_.choice([3, 4, 5]), R_.choice([185, 240, 295])
    ans = n * p - cost
    its.append(nmcq("The Year 6 class sells %d cupcakes at $%d each at a cake stall. The ingredients cost $%d. How much money does the class make after paying for the ingredients?"
                    % (n, p, cost), ans, [n * p, n * p + cost, ans + 100],
                    "Step 1: %d × $%d = $%s taken. Step 2: subtract the cost: $%s − $%d = $%s."
                    % (n, p, f(n * p), f(n * p), cost, f(ans)), pre="$"))

    # 6 fundraising: two days shared between charities
    while True:
        a, b, k = R_.randint(1200, 2400), R_.randint(900, 1900), R_.choice([4, 6, 8])
        if (a + b) % k == 0 and a % k and a % 10 and b % 10:
            break
    ans = (a + b) // k
    its.append(nmcq("A school fun run raises $%s on Friday and $%s on Saturday. The money is shared equally between %d charities. How much does each charity get?"
                    % (f(a), f(b), k), ans, [a + b, a // k + b, (a + b) * k, ans + 100],
                    "Step 1: $%s + $%s = $%s. Step 2: $%s ÷ %d = $%s. %s" % (f(a), f(b), f(a + b), f(a + b), k, f(ans), check_txt(a + b, k)),
                    pre="$"))

    # 7 fundraising target
    w, per, target = R_.randint(18, 28), R_.choice([145, 165, 185]), R_.choice([5000, 6000])
    got = w * per
    ans = target - got
    its.append(nmcq("The school wants to raise $%d for new library books. It raises $%d each week for %d weeks. How much more does it still need?"
                    % (target, per, w), ans, [got, target + got, target - no_zero(per, w), target - per],
                    "Step 1: %d × $%d = $%s raised. Step 2: $%d − $%s = $%s still needed."
                    % (w, per, f(got), target, f(got), f(ans)), pre="$"))

    # 8 raffle books
    bks, per, p = R_.choice([32, 34, 36, 38, 42, 44, 46]), 25, R_.choice([2, 3])
    tickets = bks * per
    its.append(nmcq("Raffle tickets come in books of %d. The class sells %d full books. Each ticket costs $%d. How much money is raised?"
                    % (per, bks, p), tickets * p, [tickets, bks * p, no_zero(bks, per) * p],
                    "Step 1: %d × %d = %s tickets. Step 2: %s × $%d = $%s." % (bks, per, f(tickets), f(tickets), p, f(tickets * p)), pre="$"))

    # 9 sausage sizzle packs
    while True:
        need, k, c = R_.randint(300, 460), R_.choice([24, 30]), R_.choice([14, 16])
        if need % k and need % 10:
            break
    packs = ceil(need, k)
    its.append(nmcq("For a sausage sizzle, the P&C needs %d sausages. Sausages come in packs of %d, and each pack costs $%d. How much do the sausages cost?"
                    % (need, k, c), packs * c, [(need // k) * c, need * c, packs + c, (packs + 1) * c],
                    "Step 1: %d ÷ %d = %s, so round up: %d packs. Step 2: %d × $%d = $%d."
                    % (need, k, qr(need // k, need % k), packs, packs, c, packs * c), pre="$"))

    # 10 book order and change
    sets_, c, budget = R_.randint(14, 19), R_.choice([235, 245, 265]), 5000
    spend = sets_ * c
    its.append(nmcq("A school buys %d sets of readers at $%d a set. It pays from a budget of $%d. How much of the budget is left?"
                    % (sets_, c, budget), budget - spend, [spend, budget - no_zero(c, sets_), budget - c, budget - spend + c],
                    "Step 1: %d × $%d = $%s. Step 2: $%d − $%s = $%s." % (sets_, c, f(spend), budget, f(spend), f(budget - spend)), pre="$"))

    # 11 road trip: the rest in equal days
    while True:
        T, D, k = R_.randint(3600, 4800), R_.randint(1400, 2100), R_.choice([6, 7, 8])
        if (T - D) % k == 0 and T % 10 and D % 10 and T % k:
            break
    ans = (T - D) // k
    its.append(nmcq("A family's road trip is %d km long. They have already driven %d km. They drive the rest in %d days, the same distance each day. How far do they drive each day?"
                    % (T, D, k), ans, [T // k, D // k, (T + D) // k, ans * 10],
                    "Step 1: %d − %d = %d km left. Step 2: %d ÷ %d = %d km each day. %s"
                    % (T, D, T - D, T - D, k, ans, check_txt(T - D, k)), unit="km"))

    # 12 road trip: fuel and caravan park
    fills, fc, nights, nc = R_.randint(11, 16), R_.choice([86, 94, 98]), R_.randint(12, 18), R_.choice([45, 52, 58])
    ans = fills * fc + nights * nc
    its.append(nmcq("On a road trip, a family fills the car %d times at $%d each time and stays %d nights at a caravan park at $%d a night. What is the total cost?"
                    % (fills, fc, nights, nc), ans, [fills * fc, (fills + nights) * (fc + nc), fills * fc + nc, ans + 100],
                    "Step 1: fuel: %d × $%d = $%s. Step 2: caravan park: %d × $%d = $%s. Step 3: $%s + $%s = $%s."
                    % (fills, fc, f(fills * fc), nights, nc, f(nights * nc), f(fills * fc), f(nights * nc), f(ans)), pre="$"))

    # 13 road trip: km per hour × hours × days
    sp, h, d = R_.choice([88, 92, 96]), R_.choice([5, 6, 7]), R_.choice([3, 4])
    ans = sp * h * d
    its.append(nmcq("On a road trip, a family drives an average of %d km each hour. They drive for %d hours a day for %d days. How far do they drive?"
                    % (sp, h, d), ans, [sp * h, sp * (h + d), sp * h + d, sp * d],
                    "Step 1: one day: %d × %d = %d km. Step 2: %d days: %d × %d = %s km."
                    % (sp, h, sp * h, d, sp * h, d, f(ans)), unit="km"))

    # 14 road trip: split costs between people
    while True:
        fuel, cabin, k = R_.randint(310, 480), R_.randint(420, 690), R_.choice([4, 6])
        if (fuel + cabin) % k == 0 and fuel % k and cabin % k and fuel % 10 and cabin % 10:
            break
    ans = (fuel + cabin) // k
    its.append(nmcq("%d friends go on a road trip. Fuel costs $%d and the cabin costs $%d. They share the total cost equally. How much does each person pay?"
                    % (k, fuel, cabin), ans, [fuel + cabin, (fuel + cabin) * k, fuel // k + cabin, ans + 10],
                    "Step 1: $%d + $%d = $%s. Step 2: $%s ÷ %d = $%d each." % (fuel, cabin, f(fuel + cabin), f(fuel + cabin), k, ans), pre="$"))

    # 15 school savings for a trip
    while True:
        wk, sv, cost = R_.randint(32, 44), R_.choice([75, 85, 95]), R_.choice([2400, 2650, 2800])
        got = wk * sv
        if got - cost >= 250:
            break
    its.append(nmcq("%s's family saves $%d a week for %d weeks for a holiday. The holiday costs $%d. How much money is left over?"
                    % (P.next()[0], sv, wk, cost), got - cost, [got, got + cost, got - sv - cost],
                    "Step 1: %d × $%d = $%s saved. Step 2: $%s − $%d = $%s left over." % (wk, sv, f(got), f(got), cost, f(got - cost)), pre="$"))

    # 16 canteen: boxes of juice
    bx, per, p = R_.randint(18, 28), R_.choice([24, 30]), 2
    n = bx * per
    sold = n - R_.randint(23, 57)
    its.append(nmcq("The canteen buys %d boxes of juice with %d bottles in each box. It sells all but %d of the bottles for $%d each. How much money does it take?"
                    % (bx, per, n - sold, p), sold * p, [n * p, sold, (n + (n - sold)) * p, bx * p],
                    "Step 1: %d × %d = %d bottles. Step 2: %d − %d = %d sold. Step 3: %d × $%d = $%s."
                    % (bx, per, n, n, n - sold, sold, sold, p, f(sold * p)), pre="$"))

    # 17 garden seedlings
    rows, per, died = R_.randint(24, 38), R_.choice([16, 18, 22]), R_.randint(35, 75)
    n = rows * per
    its.append(nmcq("The school garden club plants %d rows of seedlings with %d in each row. %d seedlings do not survive. How many seedlings are left?"
                    % (rows, per, died), n - died, [n, n + died, no_zero(rows, per) - died, n - per - died],
                    "Step 1: %d × %d = %d seedlings. Step 2: %d − %d = %d." % (rows, per, n, n, died, n - died), unit="seedlings"))

    # 18 swimming lessons
    s, les, c = R_.randint(112, 148), R_.choice([8, 10]), R_.choice([12, 14, 16])
    per_s = les * c
    its.append(nmcq("%d students do swimming lessons in Term 4. Each student has %d lessons, and each lesson costs $%d. What is the total cost?"
                    % (s, les, c), s * per_s, [s * c, per_s, s * les, s * (les + c)],
                    "Step 1: one student: %d × $%d = $%d. Step 2: %d × $%d = $%s." % (les, c, per_s, s, per_s, f(s * per_s)), pre="$"))

    # 19 laptops: buy and divide among classes
    while True:
        lap, cost, cls = R_.choice([96, 112, 120, 144]), R_.choice([385, 420, 465]), R_.choice([6, 8])
        if lap % cls == 0:
            break
    its.append(nmcq("A school buys %d laptops at $%d each. The laptops are shared equally between %d classes. What is the value of the laptops each class gets?"
                    % (lap, cost, cls), lap // cls * cost, [lap * cost, lap // cls, (lap // cls + 1) * cost, (lap // cls) + cost],
                    "Step 1: %d ÷ %d = %d laptops each. Step 2: %d × $%d = $%s. (Or: %d × $%d = $%s, then ÷ %d.)"
                    % (lap, cls, lap // cls, lap // cls, cost, f(lap // cls * cost), lap, cost, f(lap * cost), cls), pre="$"))

    # 20 excursion: buses and cost per student
    while True:
        s, k, c = R_.randint(150, 230), R_.choice([45, 50]), R_.choice([480, 520, 560])
        if s % k >= 3 and s % 10:
            break
    nb = ceil(s, k)
    tot = nb * c
    its.append(nmcq("%d students go on an excursion. Each bus seats %d students and costs $%d to hire. How much do the buses cost altogether?"
                    % (s, k, c), tot, [(s // k) * c, s * c, nb + c, (nb + 1) * c],
                    "Step 1: %d ÷ %d = %s, so round up: %d buses. Step 2: %d × $%d = $%s."
                    % (s, k, qr(s // k, s % k), nb, nb, c, f(tot)), pre="$"))
    rnd.shuffle(its)
    assert len(its) == 20, len(its)
    return {"title": "Multi-step problems: school camp, fundraising and road trips", "items": its}


# ============================================================ lesson
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
    assert 243 * 36 == 8748 and 1426 * 27 == 38502 and 8748 == 7290 + 1458
    assert divmod(9542, 23) == (414, 20) and divmod(250, 48) == (5, 10)
    area = area_svg(["200", "40", "3"], ["30", "6"], [["6000", "1200", "90"], ["1200", "240", "18"]],
                    "area model with 6 parts: 243 × 36")
    return (
        "<h2>The big idea</h2>"
        "<p>To multiply by a 2-digit number, split it into tens and ones. Multiply by each part, then add. "
        "To divide, work from the left and ask “how many groups fit?” at each step. "
        "In a word problem, decide first: are you putting equal groups together (multiply) or splitting a total into equal groups (divide)?</p>"
        "<h2>Multiplying: the area model</h2>"
        "<figure class='sn-fig'>" + area +
        "<figcaption>243 × 36: split 243 into 200 + 40 + 3 and 36 into 30 + 6. Multiply each pair and add: "
        "6000 + 1200 + 90 + 1200 + 240 + 18 = 8748.</figcaption></figure>"
        "<h2>Multiplying: long multiplication</h2>"
        "<p>Long multiplication is the same idea in columns. Row 1 multiplies by the ones. "
        "Row 2 multiplies by the tens, so it starts with a place-holder zero (green).</p>"
        "<figure class='sn-fig'>" + lesson_fig(1426, 27, "1426 times 27 as long multiplication") +
        "<figcaption>1426 × 27: row 1 is 1426 × 7 = 9982. Row 2 is 1426 × 20 = 28" + NB + "520. "
        "9982 + 28" + NB + "520 = 38" + NB + "502.</figcaption></figure>"
        "<h2>Dividing by a 2-digit number: long division</h2>"
        "<figure class='sn-fig'>" + ld_svg(9542, 23, fs=26, work=True) +
        "<figcaption>9542 ÷ 23: 95 ÷ 23 = 4 (4 × 23 = 92, 95 − 92 = 3). Bring down 4: 34 ÷ 23 = 1, 34 − 23 = 11. "
        "Bring down 2: 112 ÷ 23 = 4, 112 − 92 = 20. Answer: 414 r 20.</figcaption></figure>"
        + ex("Check with the inverse", "9542 ÷ 23 = 414 r 20. Is it right?",
             "Multiply the quotient by the divisor, then add the remainder: 414 × 23 = 9522 and 9522 + 20 = 9542.", "Yes")
        + "<h2>What does the remainder mean?</h2>"
        + table(["The question asks", "Do this", "250 students, 48 seats a bus: 250 ÷ 48 = 5 r 10"], [
            ["How many are needed for everyone?", "Round up", "6 buses"],
            ["How many are full?", "Round down", "5 full buses"],
            ["How many are left over?", "The remainder is the answer", "10 students"],
        ])
        + "<p>When the amount can be split, such as money or a length, share the remainder too: "
        "$347 ÷ 4 = 86 r 3, and $3 ÷ 4 = 75c, so each share is $86.75 (not $86.30). As a fraction, 347 ÷ 4 = 86 " + fr(3, 4) + ".</p>"
        "<h2>Choose the operation</h2>"
        + table(["The words say", "Operation", "Example"], [
            ["equal groups, “each”, “times as many”", "Multiply", "36 boxes of 24 pens: 36 × 24"],
            ["share equally, “groups of”, “how many times as many”", "Divide", "864 pens in boxes of 24: 864 ÷ 24"],
        ])
        + "<p>Multi-step problems need two or more steps. Write each step and its answer before you go on, "
        "and estimate to check the final answer makes sense.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["No place-holder zero (243 × 36 = 1458 + 729)", "Row 2 is × 30, so write 0 first: 7290"],
            ["Forgetting a regrouped digit", "Write it small and add it after you multiply"],
            ["Missing a zero in the quotient (6216 ÷ 3 = 272)", "If the divisor does not go in, write 0: 2072"],
            ["Writing r 3 as .3 ($347 ÷ 4 = $86.30)", "r 3 means 3 out of 4: " + fr(3, 4) + " = 0.75, so $86.75"],
            ["Rounding the wrong way (5 buses for 250 students)", "Ask: does everyone need a place? Then round up to 6"],
            ["The wrong operation (864 pens in boxes of 24: 864 × 24)", "Grouping a total is division: 864 ÷ 24 = 36"],
        ])
    )


FAQ = [
    {"q": "What multiplication and division do Year 6 students learn in Australia?",
     "a": "Year 6 students solve practical problems with larger whole numbers, such as 3- and 4-digit numbers × 2-digit numbers and division by 1- and 2-digit numbers. They choose efficient strategies and explain what the answer, including any remainder, means in the situation (AC9M6N09)."},
    {"q": "Why do you put a zero in the second row of long multiplication?",
     "a": "In 243 × 36 the 3 means 3 tens, so row 2 is 243 × 30, not 243 × 3. The place-holder zero makes the row 7290 instead of 729."},
    {"q": "How do you know whether to round a remainder up or down?",
     "a": "Round up when everyone or everything needs a place, such as buses or boxes to hold all the items. Round down when the question asks how many full groups you can make or how many you can afford."},
    {"q": "Does Year 6 sit NAPLAN?",
     "a": "No. NAPLAN is held in Years 3, 5, 7 and 9. Practising multi-step multiplication and division problems in Year 6 is good preparation for high school and the Year 7 numeracy test."},
]


def gen():
    rnd = random.Random(6809)
    P = People(rnd)
    used, seen = set(), set()
    sets = [set_multiply(rnd, seen, P), set_divide(rnd, used, P), set_remainders(rnd, used, P),
            set_operation(rnd, used, P), set_multistep(rnd, used, P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(re.sub(r"<[^>]+>", "", c) for c in it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
    return {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "multiplying-and-dividing-larger-numbers", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Multiplying and Dividing Larger Numbers",
        "seo_title": "Year 6 Multiplying and Dividing Larger Numbers: Free Maths Worksheets with Answer Key (Australian Curriculum)",
        "short_title": "Multiplying and dividing",
        "domain": "Number",
        "standard_code": "AC9M6N09",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical problems involving natural and rational numbers and percentages, including in financial contexts; formulate the problems, choosing efficient calculation strategies and using digital tools where appropriate; interpret and communicate solutions in terms of the situation, justifying choices made",
        "meta_desc": "Free Year 6 maths worksheets on multiplying and dividing larger numbers, aligned to the Australian Curriculum (AC9M6N09): the area model and long multiplication, short and long division, what to do with a remainder, choosing the operation, and multi-step problems about school camp, fundraising and road trips. 100 questions with an answer key.",
        "key_big": "Multiply by the ones, then by the tens with a place-holder zero. Divide from the left, then decide what the remainder means.",
        "key_sub": "243 × 36 = 1458 + 7290 = 8748. 250 students, 48 seats a bus: 250 ÷ 48 = 5 r 10, so round up to 6 buses.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "([0-9]+ times [0-9]+|area model with 6 parts)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
