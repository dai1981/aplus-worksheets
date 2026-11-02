# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Adding and subtracting to 1000 (Ontario Curriculum 2020, B2.3, B2.4, B2.5)
  python3 tools/gen_ca_math_g3_add_sub.py
Mental math (jump, split, compensate), column addition and subtraction with regrouping
(including across zeros), checking with the inverse operation, word problems.
Canadian English. Numbers below 10 000 have no separator.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_au_maths_y3_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
ONE = ["one", "ten", "hundred", "thousand"]


def f(n):
    """Ontario/SI style: 4 digits no separator, 5+ digits a no-break space between groups of three."""
    s = str(n)
    if abs(n) < 10000:
        return s
    out = ""
    while len(s) > 3:
        out = " " + s[-3:] + out
        s = s[:-3]
    return s + out


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique sensible distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$+")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead in ("0", ""):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


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


def nlen(n):
    return len(str(n))


def digits(n, k=3):
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals):
    return [v for v in vals if v is not None and v > 0]


# ------------------------------------------------------------ pictures: split strategy
def parts(n):
    d = digits(n)
    return [d[i] * 10 ** i for i in (2, 1, 0) if d[i]]


def split_svg(a, b, op):
    """Both numbers on top, each split into hundreds, tens and ones underneath."""
    S, m, gap = 50, 12, 56
    pa, pb = parts(a), parts(b)
    gwa, gwb = (len(pa) - 1) * S + 44, (len(pb) - 1) * S + 44
    cxa = m + gwa / 2.0
    cxb = m + gwa + gap + gwb / 2.0
    W = int(m + gwa + gap + gwb + m)
    H = 84
    s = [text(cxa, 24, str(a), 22), text(cxb, 24, str(b), 22),
         text((cxa + cxb) / 2.0, 24, "+" if op == "+" else "−", 22, col=GREEN)]
    for cx, ps in ((cxa, pa), (cxb, pb)):
        x0 = cx - (len(ps) - 1) * S / 2.0
        for k, p in enumerate(ps):
            px = x0 + k * S
            s.append("<line x1='%.1f' y1='32' x2='%.1f' y2='52' stroke='%s' stroke-width='2'/>" % (cx, px, GREEN))
            s.append("<rect x='%.1f' y='54' width='42' height='26' rx='5' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (px - 21, FILL, GREEN))
            s.append(text(px, 73, str(p), 16))
    lab = "split strategy: %d split into %s; %d split into %s" % (
        a, ", ".join(map(str, pa)), b, ", ".join(map(str, pb)))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ pictures: base ten blocks
C = 6
FLAT, ROD_GAP, FLAT_GAP, PART_GAP, CUBE_GAP = 10 * C, 4, 6, 16, 4


def part_widths(h, t, o):
    cols = (o + 4) // 5
    return [h * (FLAT + FLAT_GAP) - FLAT_GAP if h else 0,
            t * (C + ROD_GAP) - ROD_GAP if t else 0,
            cols * (C + CUBE_GAP) - CUBE_GAP if o else 0]


def draw_row(xs, y, h, t, o):
    s = []
    x = xs[0]
    for k in range(h):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, y, FLAT, FLAT, FILL, GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x + g * C, y, x + g * C, y + FLAT, GREEN))
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + g * C, x + FLAT, y + g * C, GREEN))
        x += FLAT + FLAT_GAP
    x = xs[1]
    for k in range(t):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (x, y, C, FLAT, FILL, GREEN))
        for g in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.6'/>"
                     % (x, y + g * C, x + C, y + g * C, GREEN))
        x += C + ROD_GAP
    x = xs[2]
    for k in range(o):
        col, r = divmod(k, 5)
        cx = x + col * (C + CUBE_GAP)
        cy = y + FLAT - C - r * (C + CUBE_GAP)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.3'/>"
                 % (cx, cy, C, C, FILL, GREEN))
    return "".join(s)


def blocks_svg(a, b):
    """a over b in base ten blocks: hundreds (flats), tens (longs), ones (minis) in columns, with + before row 2."""
    rows = [tuple(reversed(digits(a))), tuple(reversed(digits(b)))]
    m, lead = 6, 30
    cw = [max(part_widths(*r)[k] for r in rows) for k in range(3)]
    xs, x = [], m + lead
    for k in range(3):
        xs.append(x)
        if cw[k]:
            x += cw[k] + PART_GAP
    W = x - PART_GAP + m
    H = 2 * m + 2 * FLAT + 14
    s = []
    for i, r in enumerate(rows):
        y = m + i * (FLAT + 14)
        s.append(draw_row(xs, y, *r))
        if i == 1:
            s.append(text(m + 11, y + FLAT / 2 + 9, "+", 28, col=GREEN))
    return svg_wrap(W, H, "".join(s), "base ten blocks showing %d and %d" % (a, b))


# ------------------------------------------------------------ pictures: open number line
def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 80 if j >= 10 else 56


def nline_svg(start, jumps, ticks, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if jlabels is None:
        jlabels = [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
    m, ry, ly = 30, 24, 50
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 7, jlabels[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16))
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


# ------------------------------------------------------------ pictures: column layout
def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line.
    answer: also write the answer.  marks: red regrouping marks
    (+: the regrouped 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
    cw = fs * (0.82 if marks else 0.62)
    res = a + b if op == "+" else a - b
    rows = [str(a), str(b)] + ([str(res)] if answer else [])
    longest = max(len(r) for r in rows) * cw
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks and op != "+" else 0)
    s = []

    def put(t, y, color):
        for k, ch in enumerate(reversed(t)):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - cw * k - cw / 2, y, fs, color, ch))

    def px(i):
        return right - cw * i - cw / 2

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    sign_x = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    H = ly + 10
    if answer:
        ay = ly + fs + 6
        put(rows[2], ay, GREEN)
        H = ay + 12
        if op == "+":
            ly2 = ay + 11
            s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>"
                     % (sign_x - cw * 0.6, ly2, right, ly2, INK))
            H = ly2 + 8
    if marks:
        sm = int(fs * 0.55)
        if op == "+":
            assert answer
            yy = H + sm - 2
            for i in add_carry_cols(a, b):
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (px(i + 1), yy, sm, RED))
            H = yy + 8
        else:
            nd = regroup_digits(a, b)
            od = digits(a, nlen(a))
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = px(i)
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%d %s %d written in columns" % (a, "plus" if op == "+" else "minus", b)
    return svg_wrap(W, int(H), "".join(s), label)


# ------------------------------------------------------------ column methods
def regroup_digits(a, b):
    """Top digits after all the regrouping of column subtraction (ones first)."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return d


def add_carry_cols(a, b):
    """Columns (ones = 0) that make 10 or more and send 1 to the next column."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    c, cols = 0, []
    for i in range(k):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def sub_regroup_cols(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    cols = []
    for i in range(k):
        if d[i] < db[i]:
            cols.append(i)
            d[i] += 10
            d[i + 1] -= 1
    return cols


def zero_chain(a, b):
    """True if some regrouping has to go across a 0."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    chain = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = True
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return chain


def add_steps(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, ps = 0, []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(PLACE[i])
        if t >= 10 and i == k - 1:
            ps.append("%s: %s = %d. Write %d in front: %d hundreds is 1 thousand and %d hundreds." % (P, expr, t, t, t, t - 10)
                      if i == 2 else "%s: %s = %d. Write %d: that is 1 hundred and %d tens." % (P, expr, t, t, t - 10))
            carry = 0
        elif t >= 10:
            ps.append("%s: %s = %d. Write %d and regroup 10 %s as 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    return "Line up the ones and start on the right. " + " ".join(ps) + " Answer: <b>%d</b>." % s


def sub_steps(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    kb = nlen(b)
    ps = []
    for i in range(k):
        P = cap(PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = ", then ".join("1 %s as 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. There are 0 tens, so regroup %s. The 0 becomes 9. %d − %d = %d."
                       % (P, cur, db[i], chain, d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d. Regroup 1 %s as 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            ps.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                ps.append("%s: write %d." % (P, d[i]))
        else:
            ps.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%d</b>. Check: %d + %d = %d." % (r, r, b, a))


# ------------------------------------------------------------ typical mistakes
def add_no_regroup(a, b):
    """Never adds the regrouped 1s (writes the full sum only in the last column)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def add_forgot_one(a, b, which):
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def add_side_by_side(a, b):
    """Wrote each column total side by side (5 + 8 = 13 written as 13)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    if not add_carry_cols(a, b):
        return None
    v = int("".join(str(da[i] + db[i]) for i in reversed(range(k))))
    return v if v != a + b else None


def add_misalign(a, b):
    if nlen(a) == nlen(b):
        return None
    return max(a, b) + min(a, b) * 10


def add_extra_one(a, b):
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def sub_small_from_big(a, b):
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def sub_forgot_reduce(a, b):
    """Made 10 more but did not take 1 away from the next place."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    out = 0
    for i in range(k):
        if d[i] < db[i]:
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out


def sub_zero_as_ten(a, b):
    """Regrouping across zeros: changed the zeros to 10 instead of 9."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    hit = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            d[j] -= 1
            if j > i + 1:
                hit = True
                for m in range(i + 1, j):
                    d[m] = 10
            d[i] += 10
    if not hit:
        return None
    return sum((d[i] - db[i]) * 10 ** i for i in range(k))


def sub_zero_skip(a, b):
    """Did not regroup across the zero: took 1 straight from the hundreds and left the 0 tens as 0."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    skipped, hit, out = set(), False, 0
    for i in range(k):
        if i in skipped:
            out += abs(d[i] - db[i]) * 10 ** i
            continue
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                hit = True
                skipped |= set(range(i + 1, j))
            d[j] -= 1
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out if hit else None


def sub_write_zero(a, b):
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    if not sub_regroup_cols(a, b):
        return None
    return sum((da[i] - db[i] if da[i] >= db[i] else 0) * 10 ** i for i in range(k))


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_regroup(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b), add_side_by_side(a, b)] + every + add_extra_one(a, b) + [abs(a - b)])


def sub_misalign(a, b):
    """Lined up a 2-digit number under the hundreds and tens: 734 − 46 done as 734 − 460."""
    if nlen(b) >= nlen(a) or a - 10 * b <= 0:
        return None
    return a - 10 * b


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_misalign(a, b),
                  sub_forgot_reduce(a, b), a + b if a + b <= 999 else None, sub_write_zero(a, b), a - b + 10, a - b - 10])



# ------------------------------------------------------------ set 1: mental math (jump, split, compensate)
def part_add_cands(a, b):
    """Split strategy mistakes for a + b."""
    da, db = digits(a), digits(b)
    H, T, O = da[2] + db[2], da[1] + db[1], da[0] + db[0]
    out = []
    if O >= 10:
        out.append(H * 100 + T * 10 + O % 10)                    # 300 + 70 + 12 written as 372
    out.append(a + 100 * db[2] + db[1] + db[0])                   # added the tens as ones
    out.append(a + b - O)                                         # forgot the ones part
    out.append(abs(a - b))
    out.append(a + b + 100)
    return clean(out)


def part_add_e(a, b):
    da, db = digits(a), digits(b)
    H, T, O = (da[2] + db[2]) * 100, (da[1] + db[1]) * 10, da[0] + db[0]
    head = "Split both numbers: %s and %s. " % (" + ".join(map(str, parts(a))), " + ".join(map(str, parts(b))))
    body = "Hundreds: %d + %d = %d. Tens: %d + %d = %d. Ones: %d + %d = %d. " % (
        da[2] * 100, db[2] * 100, H, da[1] * 10, db[1] * 10, T, da[0], db[0], O)
    if O >= 10:
        body += "%d ones is 1 ten and %d ones. " % (O, O - 10)
    return head + body + "%d + %d + %d = <b>%d</b>." % (H, T, O, a + b)


def set_mental():
    its = []
    its.append(mcq("What is 436 + 200?", 636, [456, 438, 236],
                   "Only the hundreds change. 4 hundreds + 2 hundreds = 6 hundreds. 436 + 200 = <b>636</b>."))
    its.append(mcq("What is 758 − 40?", 718, [358, 754, 798],
                   "Only the tens change. 5 tens − 4 tens = 1 ten. 758 − 40 = <b>718</b>."))
    assert 436 + 200 == 636 and 758 - 40 == 718
    # split strategy
    for a, b, pic in [(324, 152, True), (258, 126, True), (368, 427, False)]:
        assert digits(a)[1] + digits(b)[1] + 1 < 10 and a + b <= 999
        q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %d + %d?" % (a, b)
        its.append(mcq(q, a + b, part_add_cands(a, b), part_add_e(a, b)))
    its.append(mcq("Use the split strategy. 356 + 128 = 400 + <b>?</b> + 14", 70, [7, 80, 700],
                   "Tens: 50 + 20 = <b>70</b>. Hundreds: 300 + 100 = 400. Ones: 6 + 8 = 14. 400 + 70 + 14 = 484. "
                   "(80 would count the regrouped ten twice: the 14 already holds it.)"))
    assert 400 + 70 + 14 == 356 + 128
    # base ten blocks
    a, b = 246, 137
    da, db = digits(a), digits(b)
    e = ("Count each kind of block. Hundreds: %d + %d = %d. Tens: %d + %d = %d. Ones: %d + %d = %d. "
         "Regroup 10 ones as 1 ten: %d tens and %d ones. The total is <b>%d</b>."
         % (da[2], db[2], da[2] + db[2], da[1], db[1], da[1] + db[1], da[0], db[0], da[0] + db[0],
            da[1] + db[1] + 1, da[0] + db[0] - 10, a + b))
    its.append(mcq(fig(blocks_svg(a, b)) + "The base ten blocks show two numbers. What is the total?",
                   a + b, part_add_cands(a, b), e))
    # jump strategy in words
    its.append(mcq("Start at 368. Jump forward 200, then 20, then 5. Where do you land?", 593, [588, 575, 693],
                   "368 + 200 = 568. 568 + 20 = 588. 588 + 5 = <b>593</b>. This is the jump strategy for 368 + 225."))
    assert 368 + 225 == 593
    its.append(mcq("Start at 815. Jump back 300, then 60, then 7. Where do you land?", 448,
                   [455, sub_small_from_big(815, 367), 458],
                   "815 − 300 = 515. 515 − 60 = 455. 455 − 7 = <b>448</b>. This is the jump strategy for 815 − 367."))
    assert 815 - 367 == 448
    # open number lines
    a, js = 345, [200, 30, 4]
    s = a + sum(js)
    e = "345 + 200 = 545. 545 + 30 = 575. 575 + 4 = <b>579</b>. So 345 + 234 = 579."
    assert s == 579
    its.append(mcq(fig(nline_svg(a, js, ["345", "545", "575", "?"])) + "Where does the last jump land?", s,
                   [575, 345 + 200 + 3 + 4, 589, 479], e))
    a, js = 742, [-300, -50, -6]
    r = a + sum(js)
    assert r == 386
    e = "742 − 300 = 442. 442 − 50 = 392. 392 − 6 = <b>386</b>. So 742 − 356 = 386."
    its.append(mcq(fig(nline_svg(a, js, ["742", "442", "392", "?"])) + "Where does the last jump land?", r,
                   [392, sub_small_from_big(742, 356), 396, 486], e))
    its.append(mcq(fig(nline_svg(263, [400, 10, 6], ["263", "663", "673", "679"])) + "Which calculation does the number line show?",
                   "263 + 416", ["263 + 461", "679 + 416", "416 − 263"],
                   "It starts at 263 and jumps +400, +10 and +6. 400 + 10 + 6 = 416, so it shows <b>263 + 416</b> = 679."))
    assert 263 + 416 == 679
    its.append(mcq(fig(nline_svg(527, [200, 40, 3], ["527", "727", "767", "770"], ["?", "+40", "+3"])) +
                   "What is the missing jump?", "+200", ["+2", "+20", "+243"],
                   "From 527 to 727 the hundreds digit goes up from 5 to 7, so the jump is <b>+200</b>. "
                   "Check: 527 + 243 = 770."))
    assert 527 + 243 == 770
    # count on to find the difference
    for a, b, js in [(425, 398, [2, 25]), (703, 685, [15, 3])]:
        d = a - b
        assert sum(js) == d and b + js[0] in (400, 700)
        ticks = [str(b), str(b + js[0]), str(a)]
        e = ("The numbers are close, so count on from %d. %d + %d = %d, then %d + %d = %d. %d + %d = <b>%d</b>. "
             "So %d − %d = %d." % (b, b, js[0], b + js[0], b + js[0], js[1], a, js[0], js[1], d, a, b, d))
        its.append(mcq(fig(nline_svg(b, js, ticks)) + "Count on to find the difference. What is %d − %d?" % (a, b), d,
                       clean([sub_zero_as_ten(a, b), sub_small_from_big(a, b), js[1], js[0], d + 10]), e))
    # compensate
    its.append(mcq("199 is 1 less than 200. What is 456 + 199?", 655, [657, 656, add_no_regroup(456, 199)],
                   "Add 200, then take away the extra 1. 456 + 200 = 656. 656 − 1 = <b>655</b>."))
    its.append(mcq("298 is 2 less than 300. What is 347 + 298?", 645, [649, 647, add_no_regroup(347, 298)],
                   "Add 300, then take away the extra 2. 347 + 300 = 647. 647 − 2 = <b>645</b>."))
    its.append(mcq("198 is 2 less than 200. What is 532 − 198?", 334, [330, 332, sub_small_from_big(532, 198)],
                   "Take away 200. You took away 2 too many, so add 2 back. 532 − 200 = 332. 332 + 2 = <b>334</b>."))
    its.append(mcq("99 is 1 less than 100. What is 614 − 99?", 515, [513, 514, 715],
                   "Take away 100. You took away 1 too many, so add 1 back. 614 − 100 = 514. 514 + 1 = <b>515</b>."))
    assert 456 + 199 == 655 and 347 + 298 == 645 and 532 - 198 == 334 and 614 - 99 == 515
    # make a hundred
    its.append(mcq("Add 38 and 62 first to make 100. What is 38 + 145 + 62?", 245, [235, 183, 345],
                   "38 + 62 = 100 (8 + 2 = 10, then 30 + 60 + 10 = 100). 100 + 145 = <b>245</b>."))
    assert 38 + 145 + 62 == 245 and 38 + 145 == 183
    assert len(its) == 20, len(its)
    return {"title": "Mental math: jump, split and compensate", "items": its}


# ------------------------------------------------------------ set 2: column addition with regrouping
LESSON = {(245, 132), (247, 135), (367, 258), (452, 178), (500, 168), (346, 52)}


def item_add(a, b, col):
    q = (fig(column_svg(a, b, "+")) + "Add. Regroup when a column makes 10 or more.") if col else \
        "Use the column method. What is %d + %d?" % (a, b)
    return mcq(q, a + b, add_cands(a, b), add_steps(a, b))


def item_sub(a, b, col):
    q = (fig(column_svg(a, b, "-")) + "Subtract. Regroup when the top digit is smaller.") if col else \
        "Use the column method. What is %d − %d?" % (a, b)
    return mcq(q, a - b, sub_cands(a, b), sub_steps(a, b))


def pick_add(rnd, seen, la, lb, cols, top=999):
    while True:
        a = rnd.randint(112, 880) if la == 3 else rnd.randint(23, 98)
        b = rnd.randint(112, 880) if lb == 3 else rnd.randint(23, 98)
        if a + b > top or (a, b) in seen or (b, a) in seen or (a, b) in LESSON or a % 10 == 0 or b % 10 == 0:
            continue
        if add_carry_cols(a, b) != cols or abs(a - b) < 50:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = ([(3, 3, [], 899)] * 2 + [(3, 3, [0], 999)] * 4 + [(3, 2, [0], 999)] * 2 +
            [(3, 3, [1], 999)] * 4 + [(3, 2, [1], 999)] * 1 + [(3, 3, [0, 1], 999)] * 4 +
            [(3, 2, [0, 1], 999)] * 3)
    for i, (la, lb, cols, top) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, cols, top)
        its.append(item_add(a, b, i % 3 != 2))
    assert len(its) == 20
    return {"title": "Column addition with regrouping", "items": its}


# ------------------------------------------------------------ set 3: column subtraction with regrouping
def pick_sub(rnd, seen, lb, cols):
    while True:
        a = rnd.randint(150, 989)
        b = rnd.randint(112, a - 25) if lb == 3 else rnd.randint(12, 96)
        if b >= a or (a, b) in seen or (a, b) in LESSON or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if lb == 3 and b < 112:
            continue
        if sub_regroup_cols(a, b) != cols or (a - b) < 100 and lb == 3 and rnd.random() < 0.7:
            continue
        seen.add((a, b))
        return a, b


def set_sub(rnd, seen):
    its = []
    plan = [(3, [0])] * 4 + [(2, [0])] * 1 + [(3, [1])] * 3 + [(2, [1])] * 1 + [(3, [0, 1])] * 4 + [(2, [0, 1])] * 1
    for i, (lb, cols) in enumerate(plan):
        a, b = pick_sub(rnd, seen, lb, cols)
        its.append(item_sub(a, b, i % 3 != 2))
    tops = {500}                                       # 500 − 168 is the lesson example
    pats = ["x0x", "x0x", "x00", "x0x", "x00", "x00"]
    for n, p in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lb = 2 if n == 3 else 3
            b = rnd.randint(112, a - 60) if lb == 3 else rnd.randint(12, 96)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b):
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, n % 3 != 2))
            break
    assert len(its) == 20
    return {"title": "Column subtraction with regrouping, including across zeros", "items": its}


# ------------------------------------------------------------ set 4: check with the inverse
def set_inverse(P):
    its = []
    assert 523 - 168 == 355 and 523 + 168 == 691 and 355 - 168 == 187 and 523 + 355 == 878
    its.append(mcq("Which addition checks 523 − 168 = 355?", "355 + 168 = 523",
                   ["523 + 168 = 691", "355 − 168 = 187", "523 + 355 = 878"],
                   "To check a subtraction, add the answer and the number you took away. "
                   "You should get the number you started with: <b>355 + 168 = 523</b>."))
    assert 384 + 279 == 663 and 384 - 279 == 105 and 663 + 279 == 942 and 663 - 297 == 366
    its.append(mcq("Which subtraction checks 384 + 279 = 663?", "663 − 279 = 384",
                   ["384 − 279 = 105", "663 + 279 = 942", "663 − 297 = 366"],
                   "To check an addition, start with the total and take away one of the numbers. "
                   "You should get the other number: <b>663 − 279 = 384</b>."))
    assert 245 + 318 == 563 and 563 - 318 == 245 and 318 - 245 == 73 and 563 + 245 == 808
    its.append(mcq("Which fact is in the same fact family as 245 + 318 = 563?", "563 − 245 = 318",
                   ["563 − 318 = 254", "318 − 245 = 73", "563 + 245 = 808"],
                   "A fact family uses the same three numbers: 245, 318 and 563. The total minus one part gives the other part: "
                   "<b>563 − 245 = 318</b>. (563 − 318 is 245, not 254.)"))
    m = P.next()
    assert 368 + 457 == 825 and 825 - 457 == 368 and 457 - 368 == 89 and 825 - 368 == 457
    its.append(mcq("%s adds 368 + 457 and gets 825. Which subtraction checks %s answer?" % (m[0], m[2]),
                   "825 − 457 = 368", ["825 − 457 = 386", "457 − 368 = 89", "825 − 368 = 547"],
                   "Start with the total and take away 457. You should get the first number: <b>825 − 457 = 368</b>. "
                   "It works, so 825 is right."))
    # check a subtraction by adding
    for a, b, w in [(543, 278, 265), (702, 356, sub_small_from_big(702, 356)), (600, 245, sub_zero_as_ten(600, 245)),
                    (914, 387, 527), (821, 465, sub_forgot_reduce(821, 465)), (734, 46, sub_misalign(734, 46))]:
        p = P.next()
        r = a - b
        S = w + b
        assert S <= 999 and (w == r) == (S == a)
        q = "%s says %d − %d = %d. Check with addition. What is %d + %d?" % (p[0], a, b, w, w, b)
        e = "Add the answer and the number taken away: %d + %d = <b>%d</b>. " % (w, b, S)
        if S == a:
            e += "That is the number %s started with, so %s answer is right." % (p[1], p[2])
        else:
            e += "That is not %d, so %s answer is wrong. The correct answer is %d − %d = %d." % (a, p[2], a, b, r)
        cands = ([a] if S != a else []) + [add_no_regroup(w, b), add_forgot_one(w, b, "last"), S + 10, S - 10, S + 100]
        its.append(mcq(q, S, clean(cands), e))
    # pick the correct answer
    for a, b in [(614, 287), (805, 467)]:
        r = a - b
        its.append(mcq("Use addition to check. Which is the correct answer to %d − %d?" % (a, b), r, sub_cands(a, b),
                       "Check each answer by adding %d. %d + %d = %d, so <b>%d</b> is correct." % (b, r, b, a, r)))
    for a, b in [(476, 358), (289, 547)]:
        s = a + b
        assert s <= 999
        its.append(mcq("Use subtraction to check. Which is the correct answer to %d + %d?" % (a, b), s, add_cands(a, b),
                       "Check each answer by taking away %d. %d − %d = %d, so <b>%d</b> is correct." % (b, s, b, a, s)))
    # missing numbers
    its.append(mcq("What number goes in the box?  <b>?</b> + 268 = 541", 273, [541 + 268] + sub_cands(541, 268),
                   "Use the inverse. Subtract: 541 − 268 = <b>273</b>. Check: 273 + 268 = 541."))
    assert 273 + 268 == 541
    its.append(mcq("What number goes in the box?  306 + <b>?</b> = 724", 418, sub_cands(724, 306),
                   "Use the inverse. Subtract: 724 − 306 = <b>418</b>. Check: 306 + 418 = 724."))
    assert 306 + 418 == 724
    its.append(mcq("What number goes in the box?  <b>?</b> − 158 = 276", 434, [276 - 158] + add_cands(276, 158),
                   "Use the inverse. Add back the 158: 276 + 158 = <b>434</b>. Check: 434 − 158 = 276."))
    assert 434 - 158 == 276
    its.append(mcq("What number goes in the box?  475 − <b>?</b> = 219", 256, [475 + 219] + sub_cands(475, 219),
                   "The part taken away is the difference: 475 − 219 = <b>256</b>. Check: 475 − 256 = 219."))
    assert 475 - 256 == 219
    # right or wrong
    p = P.next()
    w = sub_forgot_reduce(830, 275)
    assert w == 665 and w + 275 == 940 and 830 - 275 == 555 and w - 275 == 390
    its.append(mcq("%s says 830 − 275 = 665. Is %s right?" % (p[0], p[1]), "No. 665 + 275 = 940",
                   ["Yes. 665 + 275 = 830", "No. 665 − 275 = 390", "Yes. 665 + 275 = 940"],
                   "Check by adding: 665 + 275 = 940, not 830. So the answer is wrong. "
                   "(The correct answer is 830 − 275 = 555.) <b>No. 665 + 275 = 940</b>."))
    p = P.next()
    assert 457 + 286 == 743 and 743 - 286 == 457 and sub_small_from_big(743, 286) == 543 and 457 - 286 == 171
    its.append(mcq("%s says 457 + 286 = 743. Is %s right?" % (p[0], p[1]), "Yes. 743 − 286 = 457",
                   ["No. 743 − 286 = 543", "No. 457 − 286 = 171", "Yes. 743 − 286 = 543"],
                   "Check by subtracting: 743 − 286 = 457. That is the first number, so the answer is right. "
                   "<b>Yes. 743 − 286 = 457</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Check with the inverse operation", "items": its}


# ------------------------------------------------------------ set 5: word problems
def unit(v, u):
    return "$%d" % v if u == "$" else "%d %s" % (v, u)


def eu(v, u):
    return "$%d" % v if u == "$" else str(v)


def story(q, ans, cands, u, e):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans and v <= 999], e)


def one_add(q, a, b, u, lead):
    s = a + b
    assert s <= 999
    e = lead + " %s + %s = <b>%s</b>. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
    return story(q, s, add_cands(a, b), u, e)


def one_sub(q, a, b, u, lead):
    r = a - b
    e = lead + " %s − %s = <b>%s</b>. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
    return story(q, r, sub_cands(a, b), u, e)


def start_add(q, now, more, u):
    x = now - more
    e = ("Work backwards. Take away the %d that were added: %s − %s = <b>%s</b>. Check: %s + %s = %s."
         % (more, eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
    return story(q, x, [now + more] + sub_cands(now, more), u, e)


def start_sub(q, now, lost, u):
    x = now + lost
    assert x <= 999
    e = ("Work backwards. Add back the %d that were taken away: %s + %s = <b>%s</b>. Check: %s − %s = %s."
         % (lost, eu(now, u), eu(lost, u), eu(x, u), eu(x, u), eu(lost, u), eu(now, u)))
    return story(q, x, [now - lost] + add_cands(now, lost), u, e)


def both_left(q, A, B, C, u, s1, s2):
    """A − (B + C)."""
    t = B + C
    r = A - t
    assert r not in (A, B, C)
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = <b>%s</b>."
         % (s1, eu(B, u), eu(C, u), eu(t, u), s2, eu(A, u), eu(t, u), eu(r, u)))
    return story(q, r, [A - B, t, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - B + C], u, e)


def out_then_in(q, A, B, C, u, s1, s2):
    """A − B + C."""
    m = A - B
    r = m + C
    e = "Step 1, %s: %d − %d = %d. Step 2, %s: %d + %d = <b>%d</b>." % (s1, A, B, m, s2, m, C, r)
    return story(q, r, [m, A - B - C, sub_small_from_big(A, B) + C, add_forgot_one(m, C, "last")], u, e)


def more_total(q, A, B, u, who2):
    """A + (A + B)."""
    m = A + B
    r = A + m
    assert r <= 999
    e = ("Step 1, %s: %d + %d = %d. Step 2, both together: %d + %d = <b>%d</b>." % (who2, A, B, m, A, m, r))
    return story(q, r, [m, A + B + B, add_forgot_one(A, m, "last"), A + A], u, e)


def less_total(q, A, B, u, who2):
    """A + (A − B)."""
    m = A - B
    r = A + m
    e = ("Step 1, %s: %d − %d = %d. Step 2, both together: %d + %d = <b>%d</b>." % (who2, A, B, m, A, m, r))
    return story(q, r, [m, A + B, A + A + B, add_forgot_one(A, m, "last")], u, e)


def set_story(P):
    n = [P.next() for _ in range(5)]
    its = [
        one_add("The Grade 3 bake sale sold 168 muffins and 254 cookies. How many treats did it sell altogether?",
                168, 254, "treats", "Altogether means add."),
        one_add("On the way to the cottage, the Chen family drove 186 km before lunch and 147 km after lunch. "
                "How far did they drive?", 186, 147, "km", "Put the two parts of the trip together, so add."),
        one_add("%s read 245 pages in October and 178 pages in November. How many pages did %s read in the two months?"
                % (n[0][0], n[0][1]), 245, 178, "pages", "Put the two months together, so add."),
        one_add("Our school’s Terry Fox Run raised $286 from Grade 3 and $347 from Grade 4. "
                "How much money did the two grades raise?", 286, 347, "$", "Put the two amounts together, so add."),
        one_add("On Canada Day, 375 people came to the park in the morning and 448 people came in the afternoon. "
                "How many people came that day?", 375, 448, "people", "Put the morning and the afternoon together, so add."),
        one_sub("%s’s book has 312 pages. %s has read 148 pages. How many pages are left?" % (n[1][0], cap(n[1][1])),
                312, 148, "pages", "Find what is left, so subtract."),
        one_sub("The school wants to raise $750 for new gym equipment. It has raised $468 so far. How much more does it need?",
                750, 468, "$", "Find the difference, so subtract."),
        one_sub("The cottage is 403 km from home. The family has driven 165 km. How many kilometres are left?",
                403, 165, "km", "Find the distance left, so subtract."),
        one_sub("The school bought 600 freezies for the fun fair. 437 freezies were sold. How many freezies were left?",
                600, 437, "freezies", "Sold ones are taken away, so subtract."),
        one_sub("At the hockey arena, 924 people watched the game on Saturday and 657 people watched on Sunday. "
                "How many more people came on Saturday?", 924, 657, "people",
                "How many more means find the difference, so subtract."),
        one_sub("A maple syrup farm had 520 bottles of syrup. It sold 284 bottles in March. How many bottles are left?",
                520, 284, "bottles", "Sold bottles are taken away, so subtract."),
        start_add("%s had some hockey cards. %s got 145 more for %s birthday. Now %s has 403 cards. "
                  "How many cards did %s have at the start?" % (n[2][0], cap(n[2][1]), n[2][2], n[2][1], n[2][1]),
                  403, 145, "cards"),
        start_sub("The food drive box had some cans. 175 cans were taken to the food bank. Now 389 cans are left. "
                  "How many cans were in the box at the start?", 389, 175, "cans"),
        both_left("The school’s Terry Fox Run goal is $900. Grade 3 raised $356 and Grade 4 raised $287. "
                  "How much more money is needed?", 900, 356, 287, "$", "money raised", "money still needed"),
        both_left("%s’s book has 400 pages. %s read 132 pages on the weekend and 89 pages on Monday. "
                  "How many pages are left to read?" % (n[3][0], cap(n[3][1])), 400, 132, 89, "pages", "pages read",
                  "pages left"),
        both_left("The drive to the cottage is 500 km. The family drove 168 km in the morning and 145 km after lunch. "
                  "How many kilometres are left?", 500, 168, 145, "km", "kilometres driven", "kilometres left"),
        out_then_in("The school library had 625 books. 248 books were borrowed. Then 136 books came back. "
                    "How many books are in the library now?", 625, 248, 136, "books", "after borrowing",
                    "after the books came back"),
        more_total("Grade 3 collected 286 cans for the food drive. Grade 4 collected 157 more cans than Grade 3. "
                   "How many cans did the two grades collect altogether?", 286, 157, "cans", "Grade 4’s cans"),
        less_total("On the first day of a road trip to Ottawa, the Patel family drove 374 km. On the second day they drove "
                   "128 km less. How far did they drive in the two days?", 374, 128, "km", "the second day"),
        more_total("%s read 245 pages over March Break. %s read 136 more pages than %s. How many pages did they read together?"
                   % (n[4][0], P.next()[0], n[4][0]), 245, 136, "pages", "the second reader’s pages"),
    ]
    assert len(its) == 20
    return {"title": "Word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 245 + 132 == 377 and 247 + 135 == 382 and 367 + 258 == 625 and 452 - 178 == 274 and 500 - 168 == 332
    assert add_no_regroup(367, 258) == 515 and sub_small_from_big(452, 178) == 326 and sub_zero_as_ten(500, 168) == 342
    assert add_misalign(346, 52) == 866 and 346 + 52 == 398 and 623 - 245 == 378 and 375 + 198 == 573
    return (
        "<h2>The idea: hundreds, tens and ones</h2>"
        "<p>Every number is made of hundreds, tens and ones. <b>Split</b> the numbers. "
        "Add the hundreds, the tens and the ones. Then put the parts back together.</p>"
        "<figure class='sn-fig'>" + split_svg(245, 132, "+") +
        "<figcaption>245 + 132. Hundreds: 200 + 100 = 300. Tens: 40 + 30 = 70. Ones: 5 + 2 = 7. "
        "300 + 70 + 7 = 377.</figcaption></figure>"
        "<p>If the ones make 10 or more, <b>regroup</b>: 10 ones make 1 ten.</p>"
        "<figure class='sn-fig'>" + blocks_svg(247, 135) +
        "<figcaption>247 + 135 with base ten blocks. 7 + 5 = 12 ones. Regroup 10 ones as 1 ten. "
        "300 + 70 + 12 = 382.</figcaption></figure>"
        "<h2>Mental math: jump and compensate</h2>"
        "<p>On an open number line, start at the first number. Jump the hundreds, then the tens, then the ones.</p>"
        "<figure class='sn-fig'>" + nline_svg(623, [-200, -40, -5], ["623", "423", "383", "378"]) +
        "<figcaption>623 − 245: jump back 200 to 423, back 40 to 383, back 5 to 378.</figcaption></figure>" +
        ex("Compensate", "What is 375 + 198?",
           "198 is 2 less than 200. 375 + 200 = 575. You added 2 too many, so take 2 away: 575 − 2 = 573.", "573") +
        "<h2>Column addition: regroup when a column makes 10 or more</h2>"
        "<p>Put <b>ones under ones</b>, tens under tens and hundreds under hundreds. Start with the ones on the right. "
        "If a column makes 10 or more, write the ones digit and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(367, 258, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 8 = 15. Write 5, regroup 1 ten. Tens: 6 + 5 + 1 = 12. Write 2, regroup 1 hundred. "
        "Hundreds: 3 + 2 + 1 = 6. Answer: 625.</figcaption></figure>"
        "<h2>Column subtraction: regroup when the top digit is smaller</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, "
        "regroup 1 from the next column as 10.</p>"
        "<figure class='sn-fig'>" + column_svg(452, 178, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8. Regroup 1 ten as 10 ones: 12 − 8 = 4. Tens: 4 − 7. "
        "Regroup 1 hundred as 10 tens: 14 − 7 = 7. Hundreds: 3 − 1 = 2. Answer: 274.</figcaption></figure>"
        "<p><b>Across zeros:</b> if there are 0 tens, regroup 1 hundred as 10 tens first. "
        "Then regroup 1 ten as 10 ones. The 0 tens become 9 tens.</p>"
        "<figure class='sn-fig'>" + column_svg(500, 168, "-", answer=True, marks=True, fs=34) +
        "<figcaption>500 becomes 4 hundreds, 9 tens and 10 ones. 10 − 8 = 2, 9 − 6 = 3, 4 − 1 = 3. "
        "Answer: 332.</figcaption></figure>"
        "<h2>Check with the inverse</h2>"
        "<p>Addition and subtraction undo each other. To check a subtraction, add the answer and the number you took away. "
        "To check an addition, subtract one number from the total.</p>" +
        ex("Check", "Is 500 − 168 = 332 right?", "Add back what you took away: 332 + 168 = 500. "
           "You get the starting number, so it is right.", "Yes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not regrouping (367 + 258 = 515)", "Write the regrouped 1 in the next column and add it in"],
            ["Taking the smaller digit from the larger one (452 − 178 = 326)",
             "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Lining up the columns wrongly (346 + 52 = 866)", "Line up the ones on the right: 346 + 52 = 398"],
            ["Making the 0 tens into 10 tens (500 − 168 = 342)", "One ten moves to the ones, so 10 tens become 9 tens"],
        ])
    )


FAQ = [
    {"q": "What does Grade 3 learn about adding and subtracting in the Ontario math curriculum?",
     "a": "Students add and subtract whole numbers that add up to no more than 1000. They use mental math, tools like base ten blocks and number lines, and algorithms such as the column method to solve problems."},
    {"q": "What is regrouping in Grade 3 math?",
     "a": "Regrouping means trading 10 of one place for 1 of the next, such as 10 ones for 1 ten. Older books call it carrying or borrowing."},
    {"q": "How do you subtract across zeros, like 500 − 168?",
     "a": "Regroup 1 hundred as 10 tens, then 1 ten as 10 ones. 500 becomes 4 hundreds, 9 tens and 10 ones, so 500 − 168 = 332."},
    {"q": "Is adding and subtracting on the Grade 3 EQAO math assessment?",
     "a": "Yes. The Grade 3 EQAO math assessment is based on the Ontario curriculum, and adding and subtracting whole numbers is part of the Grade 3 Number strand. Many questions are word problems."},
]


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='(\d+) (plus|minus) (\d+) written in columns'", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"(?:What is|correct answer to) (\d+) ([+−]) (\d+)( [+] (\d+))?\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                if m.group(5):
                    v += int(m.group(5))
                assert int(right) == v, it["q"]
            m = re.search(r"aria-label='base ten blocks showing (\d+) and (\d+)'", it["q"])
            if m:
                assert int(right) == int(m.group(1)) + int(m.group(2))


def gen():
    rnd = random.Random(33803)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_mental(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_inverse(P), set_story(P)]
    balance(sets, rnd)
    verify(sets)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "adding-and-subtracting-to-1000", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to 1000",
        "seo_title": "Grade 3 Adding and Subtracting to 1000 Worksheets: Regrouping and Mental Math (Ontario)",
        "short_title": "Adding and subtracting to 1000",
        "domain": "Number",
        "standard_code": "Grade 3: B2.5",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the addition and subtraction of whole numbers that add up "
                         "to no more than 1000, using various tools and algorithms",
        "meta_desc": "Free Grade 3 math worksheets on adding and subtracting to 1000, matched to the Ontario curriculum: "
                     "mental math, column addition and subtraction with regrouping, subtracting across zeros, checking "
                     "with the inverse and word problems. 100 questions with an answer key. Great EQAO practice.",
        "key_big": "Line up hundreds, tens and ones. Regroup when you need to.",
        "key_sub": "Adding: if a column makes 10 or more, regroup 1 into the next column. Subtracting: if the top digit "
                   "is smaller, regroup 1 from the next column. Check with the inverse: add back what you took away.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base ten blocks|open number line|split strategy")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
