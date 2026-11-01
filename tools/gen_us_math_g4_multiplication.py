# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Multi-Digit Multiplication (4.NBT.B.5)
  python tools/gen_us_math_g4_multiplication.py
HTML attributes use single quotes (no backslashes in the JSON).
Grade 4 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """Grade 4 style: 4536 -> 4,536."""
    return "{:,}".format(n)


def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
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


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=True):
    """Approximate text width in px (Arial). Commas are narrow."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6) * fs * (0.6 if bold else 0.56)


def text(x, y, t, fs=17, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def unit_word(k, i):
    """'1 ten', '4 tens', '1 hundred', '2 thousands'."""
    w = PLACE[i]
    return "%d %s" % (k, w[:-1] if k == 1 else w)


def parts(n):
    """Expanded form, biggest place first: 236 -> [200, 30, 6] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


# ------------------------------------------------------------ figures
def area_svg(tops, lefts, cells, label):
    """Area model. tops = labels over the columns, lefts = labels beside the rows,
    cells[r][c] = text in each part ('' = empty, '?' = red question mark).
    Bigger places get wider columns and taller rows; every column is wide enough for its text."""
    FS = 17
    ws = []
    for c, t in enumerate(tops):
        need = max([tw(t, FS)] + [tw(cells[r][c], FS) for r in range(len(lefts))]) + 22
        base = {1: 62, 2: 100, 3: 130}.get(len(str(t).replace(",", "")), 150)
        ws.append(max(need, base))
    # wider columns for bigger places: keep widths in order
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 20)
    if len(lefts) == 1:
        hs = [58]
    else:
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


def area_1d(a, d, show=None, label=None):
    """Area model for a (2 or 3 digits) × d. show = list of cell texts (None = labels only)."""
    ps = parts(a)
    cells = [show if show else [""] * len(ps)]
    lab = label or ("area model with %d parts: %d × %d" % (len(ps), a, d))
    return area_svg([f(p) for p in ps], [str(d)], cells, lab)


def area_2d(a, b, show=None):
    """2-digit × 2-digit area model: a across the top, b down the side."""
    ta, oa = parts(a)
    tb, ob = parts(b)
    cells = show or [["", ""], ["", ""]]
    return area_svg([str(ta), str(oa)], [str(tb), str(ob)], cells, "area model with 4 parts: %d × %d" % (a, b))


def column_svg(rows, rules, label, big=False):
    """Numbers written in columns, ones lined up on the right.
    rows = list of (sign, text). text '[?]' is a red box across the whole row (the number to find).
    Commas sit in the gap between digit columns. The sign keeps one empty column from its own number.
    rules = row indexes that get a line under them."""
    fs = 30 if big else 27
    cw = fs * 0.8
    lens = [0 if t == "[?]" else len(t.replace(",", "")) for sg, t in rows]
    nd = max(lens)
    signed = max([n for (sg, t), n in zip(rows, lens) if sg] or [0])
    sign_slot = max(nd, signed + 1)
    slots = sign_slot + 1
    W = int(cw * slots + 20)
    gap = fs * 1.2
    H = int(10 + gap * len(rows) + 4 * len(rules) + 10)
    right = W - 10
    s = []
    y = 10
    for r, (sg, t) in enumerate(rows):
        y += gap
        if t == "[?]":
            x1 = right - cw * nd
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='4' fill='none' stroke='%s' "
                     "stroke-width='2' stroke-dasharray='5 3'/>" % (x1 + 4, y - fs * 0.86, cw * nd - 4, fs * 0.98, RED))
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>?</text>"
                     % (x1 + cw * nd / 2, y - 2, fs, RED))
        else:
            slot = 0
            for ch in reversed(t):
                if ch == ",":
                    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>,</text>"
                             % (right - cw * slot, y + 1, fs, INK))
                    continue
                s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (right - cw * (slot + 0.5), y - 2, fs, INK, ch))
                slot += 1
        if sg:
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (right - cw * (sign_slot + 0.5), y - 2, fs, GREEN, sg))
        if r in rules:
            y += 4
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%s'><g font-family='monospace'>%s</g></svg>" % (W, H, W, H, label, "".join(s)))


def col_problem(a, b, big=False):
    return column_svg([("", f(a)), ("×", f(b))], [1], "%d times %d written in columns" % (a, b), big)


# ------------------------------------------------------------ the methods, step by step
def steps_1d(a, d):
    """Standard algorithm for a × one-digit d, place by place."""
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        last = i == len(ds) - 1
        if last:
            out.append("%s: %s = %d. Write %d." % (cap(PLACE[i]), ex_, p, p))
        elif p >= 10:
            out.append("%s: %s = %d. Write %d, regroup %s." % (cap(PLACE[i]), ex_, p, p % 10, unit_word(p // 10, i + 1)))
        else:
            out.append("%s: %s = %d. Write %d." % (cap(PLACE[i]), ex_, p, p))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def pp_1d(a, d):
    """Partial products: 47 × 6 = 240 + 42."""
    ps = parts(a)
    prods = [p * d for p in ps]
    return ("Break apart %s = %s. %s. Add: %s = %s." %
            (f(a), " + ".join(f(p) for p in ps),
             ". ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
             " + ".join(f(p) for p in prods), f(a * d)))


def pp_2d(a, b):
    ta, oa = parts(a)
    tb, ob = parts(b)
    pr = [ta * tb, ta * ob, oa * tb, oa * ob]
    return ("Break apart %d = %d + %d and %d = %d + %d. %d × %d = %s, %d × %d = %s, %d × %d = %s, %d × %d = %s. "
            "Add: %s = %s." % (a, ta, oa, b, tb, ob, ta, tb, f(pr[0]), ta, ob, f(pr[1]), oa, tb, f(pr[2]), oa, ob, f(pr[3]),
                               " + ".join(f(p) for p in pr), f(a * b)))


def steps_2d(a, b):
    """Standard algorithm for 2-digit × 2-digit."""
    o, t = b % 10, b // 10
    p1, p2 = a * o, a * t * 10
    return ("Step 1: multiply by the ones: %d × %d = %s. Step 2: multiply by the tens: %d × %d = %s "
            "(write a 0 in the ones place, then %d × %d = %s). Step 3: add: %s + %s = %s."
            % (a, o, f(p1), a, t * 10, f(p2), a, t, f(a * t), f(p1), f(p2), f(a * b)))


# ------------------------------------------------------------ typical mistakes
def mult_wrong(a, d, skip=None, carry_first=False):
    """Column multiplication done with a typical mistake.
    skip=None: forget every regrouped digit; skip=k: forget only the one made in place k.
    carry_first=True: add the regrouped digit BEFORE multiplying."""
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


def tens_as_ones(a, d):
    """Treating every digit as ones: 47 × 6 -> 4 × 6 + 7 × 6 = 66."""
    return sum(x * d for x in digits(a))


def cands_1d(a, d):
    ds = digits(a)
    out = [mult_wrong(a, d), mult_wrong(a, d, carry_first=True)]
    out += [mult_wrong(a, d, skip=k) for k in range(len(ds) - 1)]
    if len(ds) == 2:
        out.insert(1, tens_as_ones(a, d))
    out.append(a + d)
    return out


def two_pp(a, b):
    """Only tens × tens and ones × ones: 34 × 27 -> 600 + 28."""
    return (a // 10) * (b // 10) * 100 + (a % 10) * (b % 10)


def no_zero(a, b):
    """Forgot the zero in the second partial product: 34 × 7 + 34 × 2."""
    return a * (b % 10) + a * (b // 10)


def std_no_carry(a, b):
    return mult_wrong(a, b % 10) + mult_wrong(a, b // 10) * 10


def skip_pp(a, b):
    """Left out one partial product (ones of a × tens of b)."""
    return a * b - (a % 10) * (b // 10) * 10


def one_zero(a, b):
    """tens × tens written with one zero: 30 × 20 = 60."""
    return a * b - (a // 10) * (b // 10) * 90


def cands_2d(a, b, area=False):
    if area:
        return [two_pp(a, b), skip_pp(a, b), one_zero(a, b), a + b, no_zero(a, b)]
    return [no_zero(a, b), two_pp(a, b), std_no_carry(a, b), skip_pp(a, b), a + b]


def carries(a, d):
    c, n = 0, 0
    for x in digits(a):
        p = x * d + c
        c = p // 10
        n += 1 if c else 0
    return n


# ------------------------------------------------------------ set 1: area model, 2-digit × 1-digit
def pick_2x1(rnd, seen, lo=12, hi=98):
    while True:
        a, d = rnd.randint(lo, hi), rnd.randint(3, 9)
        if a % 10 == 0 or (a, d) in seen or a // 10 == a % 10:
            continue
        if (a % 10) * d < 10:                          # want a regroup in the ones
            continue
        seen.add((a, d))
        return a, d


def set_area1(rnd, seen):
    its = []
    # A: use the area model (labels only)
    for _ in range(5):
        a, d = pick_2x1(rnd, seen)
        its.append(mcq(fig(area_1d(a, d)) + "Use the area model to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in cands_1d(a, d)], pp_1d(a, d), rnd))
    # B: one part is missing
    for k in range(4):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        if k % 2 == 0:
            show, ans, x = ["?", f(o * d)], t * d, t
            wrong = [t // 10 * d, t * d * 10, t + d]
        else:
            show, ans, x = [f(t * d), "?"], o * d, o
            wrong = [o + d, int("%d%d" % (o, d)), o * d * 10]
        e = "The ? part is %d wide and %d tall: %d × %d = %s." % (x, d, x, d, f(ans))
        if x == t:
            e += " Think: %d × %d tens = %d tens = %s." % (d, t // 10, d * t // 10, f(ans))
        e += " The whole model shows %d × %d = %s + %s = %s." % (a, d, f(t * d), f(o * d), f(a * d))
        its.append(mcq(fig(area_1d(a, d, show)) + "What number goes in the part marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    # C: which equation matches the area model?
    for _ in range(4):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        right = "%s + %s = %s" % (f(t * d), f(o * d), f(a * d))
        wrong = ["%d + %d = %d" % (t // 10 * d, o * d, tens_as_ones(a, d)),
                 "%d + %d + %d = %d" % (t, o, d, t + o + d),
                 "%s + %d = %s" % (f(t * d), o, f(t * d + o))]
        e = ("Each part is width × height: %d × %d = %s and %d × %d = %s. Add the parts: %s."
             % (t, d, f(t * d), o, d, f(o * d), right))
        its.append(mcq(fig(area_1d(a, d)) + "Which equation matches the area model for %d × %d?" % (a, d),
                       right, wrong, e, rnd))
    # D: break apart without a picture
    for _ in range(3):
        a, d = pick_2x1(rnd, seen)
        t, o = parts(a)
        right = "(%d × %d) + (%d × %d)" % (t, d, o, d)
        wrong = ["(%d × %d) + %d" % (t, d, o), "(%d × %d) + (%d × %d)" % (t // 10, d, o, d), "(%d × %d) + %d" % (o, d, t)]
        e = ("%d = %d + %d. Multiply both parts by %d, then add: (%d × %d) + (%d × %d) = %s + %s = %s."
             % (a, t, o, d, t, d, o, d, f(t * d), f(o * d), f(a * d)))
        its.append(mcq("Which shows %d × %d broken apart by place value?" % (a, d), right, wrong, e, rnd))
    rnd.shuffle(its)
    # E: 3-digit × 1-digit, three parts (harder, at the end)
    for _ in range(4):
        while True:
            a, d = rnd.randint(112, 789), rnd.randint(3, 8)
            ds = digits(a)
            if 0 in ds or (a, d) in seen or carries(a, d) < 2:
                continue
            break
        seen.add((a, d))
        its.append(mcq(fig(area_1d(a, d)) + "Use the area model to find %d × %d." % (a, d), f(a * d),
                       [f(v) for v in cands_1d(a, d)], pp_1d(a, d), rnd))
    return {"title": "Area models: 2- and 3-digit × 1-digit", "items": its}


# ------------------------------------------------------------ set 2: standard algorithm, 3- and 4-digit × 1-digit
def pick_big(rnd, seen, nd, zero=False):
    while True:
        a = rnd.randint(10 ** (nd - 1) + 1, 10 ** nd - 1)
        d = rnd.randint(3, 9)
        ds = digits(a)
        if zero:
            if ds[1] != 0 or ds[0] == 0 or ds[-1] == 0:
                continue
            if nd == 4 and ds[2] == 0:
                continue
        elif 0 in ds:
            continue
        if (a, d) in seen or carries(a, d) < nd - 1:
            continue
        if zero and ds[0] * d < 10:
            continue
        seen.add((a, d))
        return a, d


def item_1d(a, d, rnd, col):
    q = (fig(col_problem(a, d)) + "Multiply.") if col else "What is %s × %d?" % (f(a), d)
    return mcq(q, f(a * d), [f(v) for v in cands_1d(a, d)], steps_1d(a, d), rnd)


def set_std1(rnd, seen):
    its = []
    for i in range(7):
        a, d = pick_big(rnd, seen, 3, zero=(i == 6))
        its.append(item_1d(a, d, rnd, i % 2 == 0))
    for i in range(9):
        a, d = pick_big(rnd, seen, 4, zero=(i in (7, 8)))
        its.append(item_1d(a, d, rnd, i % 2 == 1))
    # what to write and what to regroup
    for k in range(4):
        while True:
            nd = 3 if k < 2 else 4
            a, d = pick_big(rnd, seen, nd)
            ds = digits(a)
            p0 = ds[0] * d
            p1 = ds[1] * d + p0 // 10
            if p0 >= 10 and p1 >= 10 and p0 % 10 != p0 // 10 and p1 % 10 != p1 // 10:
                break
        fig_ = fig(col_problem(a, d))
        if k % 2 == 0:
            q = fig_ + "Start with the ones: %d × %d = %d. What do you do?" % (ds[0], d, p0)
            right = "write %d, regroup %d" % (p0 % 10, p0 // 10)
            wrong = ["write %d, regroup %d" % (p0 // 10, p0 % 10), "write %d" % p0, "write %d only" % (p0 % 10)]
            e = ("%d ones = %s and %s. Write %d in the ones place and regroup %s to the tens column. "
                 % (p0, unit_word(p0 // 10, 1), unit_word(p0 % 10, 0), p0 % 10, unit_word(p0 // 10, 1)) +
                 "Then: " + steps_1d(a, d))
        else:
            c = p0 // 10
            right = "write %d, regroup %d" % (p1 % 10, p1 // 10)
            nc = ds[1] * d
            cf = (ds[1] + c) * d
            wrong = ["write %d, regroup %d" % (nc % 10, nc // 10),
                     "write %d, regroup %d" % (cf % 10, cf // 10),
                     "write %d, regroup %d" % (p1 // 10, p1 % 10)]
            q = (fig_ + "The ones gave %d: write %d, regroup %d. Now the tens: %d × %d. What do you do?"
                 % (p0, p0 % 10, c, ds[1], d))
            e = ("Multiply first, then add the regrouped %d: %d × %d + %d = %d. Write %d in the tens place and regroup %s. "
                 % (c, ds[1], d, c, p1, p1 % 10, unit_word(p1 // 10, 2)) + "Full answer: " + steps_1d(a, d))
        its.append(mcq(q, right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Standard algorithm: 3- and 4-digit × 1-digit", "items": its}


# ------------------------------------------------------------ set 3: area model, 2-digit × 2-digit
def pick_2x2(rnd, seen, lo=12, hi=98):
    while True:
        a, b = rnd.randint(lo, hi), rnd.randint(12, 89)
        if a % 10 == 0 or b % 10 == 0 or a // 10 == a % 10 or b // 10 == b % 10 or a == b:
            continue
        if (a, b) in seen or (b, a) in seen:
            continue
        if carries(a, b % 10) == 0 or carries(a, b // 10) == 0:
            continue
        seen.add((a, b))
        return a, b


def set_area2(rnd, seen):
    its = []
    for _ in range(8):
        a, b = pick_2x2(rnd, seen, hi=79)
        its.append(mcq(fig(area_2d(a, b)) + "Use the area model to find %d × %d." % (a, b), f(a * b),
                       [f(v) for v in cands_2d(a, b, area=True)], pp_2d(a, b), rnd))
    for k in range(6):
        a, b = pick_2x2(rnd, seen, hi=79)
        ta, oa = parts(a)
        tb, ob = parts(b)
        grid = [[ta * tb, oa * tb], [ta * ob, oa * ob]]
        lab = [[(tb, ta), (tb, oa)], [(ob, ta), (ob, oa)]]
        r, c = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 0), (0, 1)][k]
        show = [[f(grid[i][j]) for j in range(2)] for i in range(2)]
        show[r][c] = "?"
        x, y = lab[r][c]
        ans = x * y
        wrong = [x + y, ans * 10]
        if ans % 10 == 0 and (x % 10 == 0 or y % 10 == 0):
            wrong.insert(0, ans // 10 if x % 10 == 0 and y % 10 == 0 else (x // 10 if x % 10 == 0 else x) * (y // 10 if y % 10 == 0 else y))
        else:
            wrong.append(int("%d%d" % (y, x)))
        e = "The ? part is %d wide and %d tall: %d × %d = %s." % (y, x, y, x, f(ans))
        if x % 10 == 0 and y % 10 == 0:
            e += " Think: %d tens × %d tens = %d hundreds." % (y // 10, x // 10, ans // 100)
        e += " All four parts add to %d × %d = %s." % (a, b, f(a * b))
        its.append(mcq(fig(area_2d(a, b, show)) + "What number goes in the part marked ?", f(ans),
                       [f(v) for v in wrong], e, rnd))
    for _ in range(6):
        a, b = pick_2x2(rnd, seen)
        ta, oa = parts(a)
        tb, ob = parts(b)
        pr = [ta * tb, ta * ob, oa * tb, oa * ob]
        right = " + ".join(f(p) for p in pr)
        wrong = [" + ".join(f(p) for p in [ta * tb, oa * ob]),
                 " + ".join(str(p) for p in [ta * tb // 100, ta * ob // 10, oa * tb // 10, oa * ob]),
                 " + ".join(f(p) for p in [ta * tb, ta * ob, oa * ob])]
        e = ("Each part of one number multiplies each part of the other, so there are 4 partial products. " + pp_2d(a, b))
        its.append(mcq("Which partial products add up to %d × %d?" % (a, b), right, wrong, e, rnd))
    rnd.shuffle(its)
    return {"title": "Area models: 2-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 4: standard algorithm, 2-digit × 2-digit
def set_std2(rnd, seen):
    its = []
    for i in range(12):
        a, b = pick_2x2(rnd, seen, lo=23)
        q = (fig(col_problem(a, b)) + "Multiply.") if i % 2 == 0 else "What is %d × %d?" % (a, b)
        its.append(mcq(q, f(a * b), [f(v) for v in cands_2d(a, b)], steps_2d(a, b), rnd))
    for k in range(4):
        a, b = pick_2x2(rnd, seen, lo=23)
        o, t = b % 10, b // 10
        p1, p2 = a * o, a * t * 10
        if k % 2 == 0:
            rows = [("", str(a)), ("×", str(b)), ("", f(p1)), ("+", "[?]"), ("", f(a * b))]
            ans = p2
            wrong = [a * t, p2 * 10, mult_wrong(a, t) * 10, a * b]
            q = fig(column_svg(rows, [1, 3], "%d times %d with partial products" % (a, b))) + \
                "What number goes in the dashed box?"
            e = ("The second row is %d × %d. Write a 0 in the ones place first, because you are multiplying by tens. "
                 "%d × %d = %s, so the row is %s. Check: %s + %s = %s." % (a, t * 10, a, t, f(a * t), f(p2), f(p1), f(p2), f(a * b)))
        else:
            rows = [("", str(a)), ("×", str(b)), ("", "[?]"), ("+", f(p2)), ("", f(a * b))]
            ans = p1
            wrong = [mult_wrong(a, o), mult_wrong(a, o, carry_first=True), a + o, a * b - p2 + 10]
            q = fig(column_svg(rows, [1, 3], "%d times %d with partial products" % (a, b))) + \
                "What number goes in the dashed box?"
            e = ("The first row is %d × %d (the ones). " % (a, o) + steps_1d(a, o) +
                 " Check: %s + %s = %s." % (f(p1), f(p2), f(a * b)))
        its.append(mcq(q, f(ans), [f(v) for v in wrong], e, rnd))
    for k in range(4):
        a, b = pick_2x2(rnd, seen, lo=23)
        ta, oa = parts(a)
        tb, ob = parts(b)
        if k == 0:
            q, ans, wrong = "(%d × %d) + (%d × ☐)" % (a, tb, a, ), ob, [tb // 10, b, tb]
            bk = "%d = %d + %d, so %d × %d = (%d × %d) + (%d × %d)." % (b, tb, ob, a, b, a, tb, a, ob)
        elif k == 1:
            q, ans, wrong = "(%d × ☐) + (%d × %d)" % (a, a, ob), tb, [tb // 10, b, tb * 10]
            bk = "%d = %d + %d, so %d × %d = (%d × %d) + (%d × %d)." % (b, tb, ob, a, b, a, tb, a, ob)
        elif k == 2:
            q, ans, wrong = "(%d × %d) + (☐ × %d)" % (ta, b, b), oa, [ta // 10, a, ta]
            bk = "%d = %d + %d, so %d × %d = (%d × %d) + (%d × %d)." % (a, ta, oa, a, b, ta, b, oa, b)
        else:
            q, ans, wrong = "(☐ × %d) + (%d × %d)" % (b, oa, b), ta, [ta // 10, a, ta * 10]
            bk = "%d = %d + %d, so %d × %d = (%d × %d) + (%d × %d)." % (a, ta, oa, a, b, ta, b, oa, b)
        if k < 2:
            chk = "%s + %s = %s" % (f(a * tb), f(a * ob), f(a * b))
        else:
            chk = "%s + %s = %s" % (f(ta * b), f(oa * b), f(a * b))
        e = bk + " The missing number is %d. Check: %s." % (ans, chk)
        its.append(mcq("What number goes in the box?  <b>%d × %d = %s</b>" % (a, b, q), str(ans),
                       [str(v) for v in wrong], e, rnd))
    rnd.shuffle(its)
    return {"title": "Standard algorithm: 2-digit × 2-digit", "items": its}


# ------------------------------------------------------------ set 5: word problems and estimates
def money(v):
    return "$" + f(v)


# (story, kind, a-range, b-range, unit, lead). kind "1d" = up to 4 digits × 1 digit, "2d" = 2-digit × 2-digit.
# {n} name, {he} pronoun, {his} possessive, {a} {b} the numbers (already with commas).
STORIES = [
    ("A theater has {b} rows of seats. Each row has {a} seats. How many seats are in the theater?",
     "2d", (24, 38), (18, 32), "seats", "{b} rows × {a} seats"),
    ("A school orders {b} boxes of pencils. Each box holds {a} pencils. How many pencils does the school order?",
     "2d", (24, 48), (12, 26), "pencils", "{b} boxes × {a} pencils"),
    ("{n} puts {a} stamps on each page of an album. The album has {b} full pages. How many stamps are in the album?",
     "2d", (12, 18), (24, 46), "stamps", "{b} pages × {a} stamps"),
    ("A farmer plants {b} rows of corn with {a} plants in each row. How many corn plants are there?",
     "2d", (32, 58), (16, 28), "plants", "{b} rows × {a} plants"),
    ("A factory packs {a} bottles each hour. How many bottles does it pack in {b} hours?",
     "1d", (1125, 1890), (6, 8), "bottles", "{b} hours × {a} bottles"),
    ("A pilot flies a route that is {a} miles long. She flies it {b} times this month. How many miles is that?",
     "1d", (1215, 2460), (3, 4), "miles", "{b} trips × {a} miles"),
    ("A new bike costs ${a}. A bike club buys {b} bikes. How much does the club pay?",
     "1d$", (238, 489), (5, 8), "$", "{b} bikes × ${a}"),
    ("There are {a} eggs in each crate. A grocery store gets {b} crates. How many eggs is that?",
     "2d", (24, 36), (14, 29), "eggs", "{b} crates × {a} eggs"),
    ("{n} swims {a} meters every day. How many meters does {he} swim in {b} days?",
     "1d", (1250, 1650), (5, 7), "meters", "{b} days × {a} meters"),
    ("A video game level has {a} coins. {n} plays it {b} times and collects every coin. How many coins does {he} collect?",
     "1d", (346, 879), (4, 9), "coins", "{b} times × {a} coins"),
]


def set_story(rnd, P):
    its = []
    used = set()
    for t, kind, ar, br, unit, lead in STORIES:
        while True:
            a, b = rnd.randint(*ar), rnd.randint(*br)
            if kind == "2d":
                if a % 10 == 0 or b % 10 == 0 or carries(a, b % 10) == 0 or carries(a, b // 10) == 0:
                    continue
            else:
                if 0 in digits(a) or carries(a, b) < len(str(a)) - 1:
                    continue
            if (a, b) not in used:
                break
        used.add((a, b))
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=f(a), b=b)
        fm = money if unit == "$" else (lambda v, u=unit: "%s %s" % (f(v), u))
        if kind == "2d":
            steps, cands = steps_2d(a, b), cands_2d(a, b)
        else:
            steps, cands = steps_1d(a, b), cands_1d(a, b)
        e = "Equal groups: %s, so multiply. " % lead.format(a=f(a), b=b) + steps
        its.append(mcq(q, fm(a * b), [fm(v) for v in cands], e, rnd))

    # two-step problems
    n, he, his = P.next()
    k, price = 26, 13
    cost = k * price
    its.append(mcq("%d students go to a science museum. A ticket costs $%d. The teacher pays with $400. "
                   "How much change does the teacher get?" % (k, price),
                   money(400 - cost), [money(v) for v in [cost, 400 - no_zero(k, price), 400 - two_pp(k, price), 400 - k - price]],
                   "Step 1: cost of the tickets: %d × $%d = $%d (%d × %d = %d, %d × %d = %d, and %d + %d = %d). "
                   "Step 2: change: $400 − $%d = $%d." % (k, price, cost, k, price % 10, k * (price % 10), k, price - price % 10,
                                                          k * (price - price % 10), k * (price % 10), k * (price - price % 10), cost,
                                                          cost, 400 - cost), rnd))
    n, he, his = P.next()
    per, days, book = 25, 14, 420
    its.append(mcq("%s reads %d pages a day for %d days. %s book has %d pages. How many pages does %s still have to read?"
                   % (n, per, days, cap(his), book, he),
                   "%d pages" % (book - per * days),
                   ["%d pages" % v for v in [per * days, book - no_zero(per, days),
                                             book - two_pp(per, days), book + per * days]],
                   "Step 1: pages read: %d × %d = %d. Step 2: pages left: %d − %d = %d." % (per, days, per * days, book, per * days, book - per * days),
                   rnd))
    box, k, have = 185, 6, 1500
    sold = box * k
    its.append(mcq("A café has %s paper cups. It uses %d packs of %d cups this week. How many cups are left?" % (f(have), k, box),
                   "%d cups" % (have - sold),
                   ["%s cups" % f(v) for v in [sold, have - mult_wrong(box, k), have - mult_wrong(box, k, carry_first=True), have + sold]],
                   "Step 1: cups used: %d × %d = %s (%s). Step 2: cups left: %s − %s = %d."
                   % (box, k, f(sold), " + ".join(f(p * k) for p in parts(box)), f(have), f(sold), have - sold), rnd))
    r1, r2, per = 32, 18, 12
    tot = (r1 + r2) * per
    its.append(mcq("A store has %d packs of red markers and %d packs of blue markers. Every pack has %d markers. "
                   "How many markers does the store have?" % (r1, r2, per),
                   "%d markers" % tot,
                   ["%d markers" % v for v in [r1 * per, r1 * per + r2, r1 + r2 + per, r1 * r2]],
                   "Step 1: packs in all: %d + %d = %d. Step 2: markers: %d × %d = %d. "
                   "Or: %d × %d = %d red and %d × %d = %d blue, and %d + %d = %d."
                   % (r1, r2, r1 + r2, r1 + r2, per, tot, r1, per, r1 * per, r2, per, r2 * per, r1 * per, r2 * per, tot), rnd))

    # estimate to check
    for a, d in [(487, 6), (2_915, 4), (68, 31)]:
        if a < 100:
            ra, rd = round(a, -1), round(d, -1)
            how = "Round both numbers to the nearest ten"
            wrong = [ra * rd // 10, ra * rd * 10, ra + rd]
        else:
            ra, rd = int(round(a, -(len(str(a)) - 1))), d
            how = "Round %s to the nearest %s" % (f(a), "hundred" if a < 1000 else "thousand")
            wrong = [(ra - 10 ** (len(str(a)) - 1)) * rd, ra * rd // 10, ra + rd]
        est = ra * rd
        its.append(mcq("Which is the best estimate for %s × %d?" % (f(a), d),
                       "about %s" % f(est), ["about %s" % f(v) for v in wrong],
                       "%s: %s × %d = %s. The exact answer, %s, is close to %s." % (
                           how + (" (%s and %d)" % (ra, rd) if a < 100 else " (%s)" % f(ra)), f(ra), rd, f(est), f(a * d), f(est)), rnd))
    checks = [("Ava", "she", 47, 23, 235), ("Owen", "he", 38, 42, 1596), ("Grace", "she", 3_104, 6, 18_624)]
    for n, he, a, b, claim in checks:
        if b < 10:
            ra, rb = int(round(a, -(len(str(a)) - 1))), b
            how = "%s rounds to %s, and %s × %d = %s" % (f(a), f(ra), f(ra), rb, f(ra * rb))
        else:
            ra, rb = round(a, -1), round(b, -1)
            how = "%d rounds to %d and %d rounds to %d, and %d × %d = %s" % (a, ra, b, rb, ra, rb, f(ra * rb))
        est = ra * rb
        ok = claim == a * b
        right = ("Yes, about %s" if ok else "No, about %s") % f(est)
        wrong = [("No, about %s" if ok else "Yes, about %s") % f(est),
                 ("Yes, about %s" if ok else "No, about %s") % f(est // 10),
                 ("Yes, about %s" % f(est * 10))]
        if ok:
            tail = " %s is close to %s, so the answer is reasonable. (It is also exact: %s × %d = %s.)" % (f(claim), f(est), f(a), b, f(a * b))
        else:
            tail = (" %s is much too small, so the answer is not reasonable. The exact answer is %s; "
                    "%s forgot the zero in the second partial product." % (f(claim), f(a * b), n))
        its.append(mcq("%s says %s × %d = %s. Use an estimate. Is %s answer reasonable?" % (n, f(a), b, f(claim), "her" if he == "she" else "his"),
                       right, wrong, cap(how) + "." + tail, rnd))
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


def body_html():
    return (
        "<h2>Break the number apart by place value</h2>"
        "<p>A big multiplication is a few small ones. Split each number into <b>tens and ones</b> "
        "(or thousands, hundreds, tens and ones). Multiply each part, then <b>add the partial products</b>.</p>"
        "<figure class='sn-fig'>" + area_1d(47, 6, ["240", "42"], "area model: 47 times 6") +
        "<figcaption>47 × 6: 47 = 40 + 7. 40 × 6 = 240 and 7 × 6 = 42. 240 + 42 = 282.</figcaption></figure>"
        "<h2>The standard algorithm</h2>"
        "<p>Write the numbers in columns and start with the <b>ones</b>. When a product is 10 or more, "
        "write the ones digit and <b>regroup</b> the rest to the next column. Multiply first, "
        "then add the regrouped digit.</p>"
        "<figure class='sn-fig'>" + column_svg([("", "1,346"), ("×", "7"), ("", "9,422")], [1],
                                               "1346 times 7 in columns", big=True) +
        "<figcaption>Ones: 6 × 7 = 42, write 2, regroup 4 tens. Tens: 4 × 7 + 4 = 32, write 2, regroup 3 hundreds. "
        "Hundreds: 3 × 7 + 3 = 24, write 4, regroup 2 thousands. Thousands: 1 × 7 + 2 = 9. Answer: 9,422.</figcaption></figure>"
        "<h2>Two-digit × two-digit: 4 partial products</h2>"
        "<p>Each part of one number multiplies each part of the other. Two parts × two parts = <b>4 partial products</b>.</p>"
        "<figure class='sn-fig'>" + area_svg(["30", "4"], ["20", "7"], [["600", "80"], ["210", "28"]],
                                             "area model: 34 times 27") +
        "<figcaption>34 × 27: 600 + 80 + 210 + 28 = 918.</figcaption></figure>" +
        ex("Standard algorithm", "34 × 27 = ?",
           "Step 1: 34 × 7 = 238. Step 2: 34 × 20 = 680. Write a 0 in the ones place first, then 34 × 2 = 68. "
           "Step 3: 238 + 680 = 918.", "918") +
        "<h2>Check with an estimate</h2>"
        "<p>Round, multiply in your head, and compare. 34 × 27 is about 30 × 30 = 900, so 918 makes sense. "
        "An answer like 306 or 9,180 would be far off.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the regrouped digit (47 × 6 = 242)", "Write the small digit above the next column and add it"],
            ["Adding the regrouped digit first (47 × 6 = 482)", "Multiply first: 4 × 6 = 24, then add 4: 28"],
            ["No zero in the second row (34 × 27 = 306)", "The 2 means 20. Write 0 in the ones place, then multiply"],
            ["Only 2 partial products (34 × 27 = 600 + 28)", "Multiply every part by every part: 4 partial products"],
            ["Treating 40 as 4 (47 × 6 = 24 + 42)", "40 × 6 = 240, not 24"],
        ])
    )


FAQ = [
    {"q": "How do you teach multi-digit multiplication in 4th grade?",
     "a": "Start with the area model or partial products, so children see that 47 × 6 is 40 × 6 plus 7 × 6. Then move to the standard algorithm, which is a short way to write the same partial products."},
    {"q": "Why do you put a zero in the second row when multiplying 2-digit numbers?",
     "a": "In 34 × 27, the 2 means 2 tens, so the second row is 34 × 20, not 34 × 2. The zero in the ones place shows that this row counts tens: 680, not 68."},
    {"q": "What is an area model for multiplication?",
     "a": "It is a rectangle split by place value. For 34 × 27, the sides are 30 + 4 and 20 + 7, so there are 4 parts: 600, 80, 210 and 28. Their sum, 918, is the product."},
    {"q": "What does 4.NBT.B.5 mean?",
     "a": "It is the Common Core Grade 4 standard for multiplying up to a four-digit number by a one-digit number, and a two-digit number by a two-digit number, using place value strategies and explaining the work with equations, arrays or area models."},
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


def gen_multiplication():
    rnd = random.Random(101)
    P = People(rnd)
    seen1, seen2 = set(), set()
    sets = [set_area1(rnd, seen1), set_std1(rnd, seen1), set_area2(rnd, seen2), set_std2(rnd, seen2), set_story(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "multi-digit-multiplication", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multi-Digit Multiplication",
        "seo_title": "Grade 4 Multi-Digit Multiplication Worksheets: Area Model, Partial Products and Standard Algorithm",
        "short_title": "Multi-digit multiplication",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "4.NBT.B.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/NBT/B/5/",
        "standard_text": "Multiply a whole number of up to four digits by a one-digit whole number, and multiply two two-digit numbers, using strategies based on place value and the properties of operations. Illustrate and explain the calculation by using equations, rectangular arrays, and/or area models.",
        "meta_desc": "Free Grade 4 multiplication worksheets: area models and partial products, the standard algorithm for 3- and 4-digit × 1-digit and 2-digit × 2-digit numbers, word problems and estimating to check. 100 practice questions with step-by-step answers.",
        "key_big": "Break the numbers apart by place value. Multiply each part, then add.",
        "key_sub": "47 × 6 = 240 + 42 = 282. For 2-digit × 2-digit there are 4 partial products, and the second row of the standard algorithm starts with a 0 because it multiplies by tens.",
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
    u = gen_multiplication()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        mark_large(u, "(area model with (3|4) parts|[0-9]+ times [0-9]+ with partial products)")
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
