# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Adding and subtracting (Australian Curriculum v9.0, AC9M3N03)
  python3 tools/gen_au_maths_y3_add_sub.py
Two- and three-digit numbers: partition (split strategy, MAB), regroup (column layout),
rearrange, jump strategy on an empty number line, word problems.
Australian English; Australian school word "regroup". Numbers below 10 000 have no separator.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_uk_maths_y3_column_add_sub.py and gen_uk_maths_y3_mental_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
ONE = ["one", "ten", "hundred", "thousand"]


def f(n):
    """Australian Curriculum style: 4 digits no separator, 5+ digits a no-break space between groups of three."""
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


# ------------------------------------------------------------ pictures: MAB (base-ten blocks)
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
    """a over b in MAB: hundreds (flats), tens (longs), ones (minis) in columns, with + before row 2."""
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
    return svg_wrap(W, H, "".join(s), "MAB blocks showing %d and %d" % (a, b))


# ------------------------------------------------------------ pictures: empty number line
def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 80 if j >= 10 else 56


def nline_svg(start, jumps, ticks, jlabels=None):
    """Empty number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
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
    return svg_wrap(W, H, "".join(s), "empty number line starting at %d with jumps of %s" % (
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


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_forgot_reduce(a, b),
                  a + b, sub_write_zero(a, b), a - b + 10, a - b - 10])


# ------------------------------------------------------------ set 1: partition (split strategy, MAB)
def part_add_cands(a, b):
    """245 + 132 split strategy mistakes."""
    da, db = digits(a), digits(b)
    H, T, O = da[2] + db[2], da[1] + db[1], da[0] + db[0]
    out = []
    if O >= 10:
        out.append(H * 100 + T * 10 + O % 10)                    # 300 + 70 + 12 written as 372
        out.append(int("%d%d%d" % (H, T, O)))                     # 300 70 12 written side by side: 3712
    out.append(a + 100 * db[2] + db[1] + db[0])                   # added the tens as ones: 245 + 100 + 3 + 2
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


def part_sub_cands(a, b):
    db = digits(b)
    return clean([a - 100 * db[2] - db[1] - db[0],               # took away the tens as ones
                  a - 100 * db[2] - 10 * db[1],                   # forgot to take away the ones
                  a + b if a + b <= 999 else None, a - b + 100, a - b - 10, a - b + 10])


def part_sub_e(a, b):
    da, db = digits(a), digits(b)
    return ("Split %d into %s. Take away each part. Hundreds: %d − %d = %d. Tens: %d − %d = %d. "
            "Ones: %d − %d = %d. %d + %d + %d = <b>%d</b>."
            % (b, " + ".join(map(str, parts(b))), da[2] * 100, db[2] * 100, (da[2] - db[2]) * 100,
               da[1] * 10, db[1] * 10, (da[1] - db[1]) * 10, da[0], db[0], da[0] - db[0],
               (da[2] - db[2]) * 100, (da[1] - db[1]) * 10, da[0] - db[0], a - b))


def set_partition():
    its = []
    # (a) partition a number
    its.append(mcq("Which shows 356 partitioned into hundreds, tens and ones?", "300 + 50 + 6",
                   ["300 + 5 + 6", "30 + 50 + 6", "3 + 5 + 6"],
                   "356 has 3 hundreds, 5 tens and 6 ones: <b>300 + 50 + 6</b>. The 5 is in the tens place, so it is worth 50, not 5."))
    its.append(mcq("Which shows 408 partitioned?", "400 + 8", ["400 + 80", "40 + 8", "4 + 0 + 8"],
                   "408 has 4 hundreds, 0 tens and 8 ones: <b>400 + 8</b>. The 0 holds the tens place, so the 8 is 8 ones."))
    assert 300 + 50 + 6 == 356 and 400 + 8 == 408
    # (b) split strategy, no regrouping
    for a, b, pic in [(324, 152, True), (431, 245, True), (263, 514, False), (542, 36, True), (615, 273, False)]:
        assert not add_carry_cols(a, b) and a + b <= 999
        q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %d + %d?" % (a, b)
        its.append(mcq(q, a + b, part_add_cands(a, b), part_add_e(a, b)))
    # (c) missing part
    its.append(mcq("Use the split strategy. 352 + 236 = 500 + 80 + <b>?</b>", 8, [6, 80, 4],
                   "Ones: 2 + 6 = <b>8</b>. Hundreds: 300 + 200 = 500. Tens: 50 + 30 = 80. 500 + 80 + 8 = 588."))
    assert 352 + 236 == 588
    its.append(mcq("Use the split strategy. 247 + 135 = 300 + <b>?</b> + 12", 70, [7, 80, 700],
                   "Tens: 40 + 30 = <b>70</b>. Hundreds: 200 + 100 = 300. Ones: 7 + 5 = 12. 300 + 70 + 12 = 382. "
                   "(7 adds the tens as if they were ones.)"))
    assert 300 + 70 + 12 == 247 + 135
    # (d) MAB
    for a, b in [(231, 145), (246, 137), (358, 214)]:
        q = fig(blocks_svg(a, b)) + "The MAB show two numbers. What is the total?"
        da, db = digits(a), digits(b)
        O = da[0] + db[0]
        e = ("Count each kind of block. Hundreds: %d + %d = %d. Tens: %d + %d = %d. Ones: %d + %d = %d. "
             % (da[2], db[2], da[2] + db[2], da[1], db[1], da[1] + db[1], da[0], db[0], O))
        if O >= 10:
            e += ("Regroup 10 ones as 1 ten: %d tens and %d ones. " % (da[1] + db[1] + 1, O - 10))
        e += "The total is <b>%d</b>." % (a + b)
        its.append(mcq(q, a + b, part_add_cands(a, b), e))
    # (e) split strategy with regrouping in the ones
    for a, b, pic in [(247, 135, True), (368, 427, False), (159, 326, True), (476, 218, False)]:
        assert digits(a)[0] + digits(b)[0] >= 10 and digits(a)[1] + digits(b)[1] + 1 < 10
        if (a, b) == (247, 135):
            q = fig(split_svg(a, b, "+")) + "What is 247 + 135?"
        else:
            q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %d + %d?" % (a, b)
        its.append(mcq(q, a + b, part_add_cands(a, b), part_add_e(a, b)))
    # (f) split strategy to subtract
    for a, b, pic in [(568, 234, True), (795, 352, False), (687, 425, True), (849, 316, False)]:
        assert not sub_regroup_cols(a, b)
        q = (fig(split_svg(a, b, "−")) if pic else "") + "Partition to subtract. What is %d − %d?" % (a, b)
        its.append(mcq(q, a - b, part_sub_cands(a, b), part_sub_e(a, b)))
    assert len(its) == 20, len(its)
    return {"title": "Partition to add and subtract (split strategy and MAB)", "items": its}


# ------------------------------------------------------------ set 2: column addition with regrouping
LESSON = {(245, 138), (367, 258), (563, 128), (452, 178), (402, 158), (247, 135), (245, 132)}


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
        if add_carry_cols(a, b) != cols:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = ([(3, 3, [], 899)] * 2 + [(3, 3, [0], 999)] * 4 + [(3, 2, [0], 999)] * 2 +
            [(3, 3, [1], 999)] * 4 + [(3, 2, [1], 999)] * 1 + [(3, 3, [0, 1], 999)] * 4 +
            [(3, 2, [0, 1], 999)] * 1 + [(2, 2, [0, 1], 199)] * 2)
    for i, (la, lb, cols, top) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, cols, top)
        its.append(item_add(a, b, i % 3 != 2))
    assert len(its) == 20
    return {"title": "Add with regrouping (column method)", "items": its}


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
    tops = {402}                                       # 402 − 158 is the lesson example
    pats = ["x0x", "x0x", "x00", "x0x", "x00", "x0x"]
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
    return {"title": "Subtract with regrouping, including across a zero", "items": its}


# ------------------------------------------------------------ set 4: rearrange, jump strategy
def set_jump():
    its = []
    its.append(mcq("Which two numbers should you add first to make 100?  47 + 286 + 53", "47 and 53",
                   ["47 and 286", "286 and 53", "It does not matter"],
                   "7 + 3 = 10 and 40 + 50 + 10 = 100, so <b>47 + 53 = 100</b>. Then 100 + 286 = 386 is easy."))
    assert 47 + 53 == 100
    its.append(mcq("Which has the same answer as 156 + 237?", "237 + 156", ["237 − 156", "165 + 237", "156 + 273"],
                   "You can add numbers in any order. <b>237 + 156</b> = 393, the same as 156 + 237. "
                   "165 and 273 have digits swapped, so they are different numbers."))
    for a, b, c, mk in [(38, 145, 62, 100), (27, 356, 73, 100), (25, 468, 75, 100), (64, 219, 36, 100), (150, 387, 50, 200)]:
        assert a + c == mk
        t = a + b + c
        wrong = [t - 10 if mk == 100 else t - 100, a + b, b + c, t + 100]
        e = ("Rearrange: add %d + %d first to make %d. Then %d + %d = <b>%d</b>."
             % (a, c, mk, mk, b, t))
        its.append(mcq("Rearrange to make a friendly number first. What is %d + %d + %d?" % (a, b, c), t, wrong, e))
    # jump strategy in words
    its.append(mcq("Start at 368. Jump forward 200, then 20, then 5. Where do you land?", 593,
                   [588, 575, 693],
                   "368 + 200 = 568. 568 + 20 = 588. 588 + 5 = <b>593</b>. This is the jump strategy for 368 + 225."))
    assert 368 + 225 == 593 and 368 + 200 + 2 + 5 == 575
    its.append(mcq("Start at 815. Jump back 300, then 60, then 7. Where do you land?", 448,
                   [455, sub_small_from_big(815, 367), 458],
                   "815 − 300 = 515. 515 − 60 = 455. 455 − 7 = <b>448</b>. This is the jump strategy for 815 − 367."))
    assert 815 - 367 == 448
    # number lines
    for a, js in [(345, [200, 30, 4]), (468, [300, 20, 5])]:
        b = sum(js)
        s = a + b
        ticks = [str(a), str(a + js[0]), str(a + js[0] + js[1]), "?"]
        e = "%d + %d = %d. %d + %d = %d. %d + %d = <b>%d</b>. So %d + %d = %d." % (
            a, js[0], a + js[0], a + js[0], js[1], a + js[0] + js[1], a + js[0] + js[1], js[2], s, a, b, s)
        db = digits(b)
        its.append(mcq(fig(nline_svg(a, js, ticks)) + "Where does the last jump land?", s,
                       [s - js[2], a + 100 * db[2] + db[1] + db[0], s + 10, s - 100], e))
    for a, js in [(623, [-200, -40, -5]), (754, [-300, -20, -8])]:
        b = -sum(js)
        r = a - b
        ticks = [str(a), str(a + js[0]), str(a + js[0] + js[1]), "?"]
        e = "%d − %d = %d. %d − %d = %d. %d − %d = <b>%d</b>. So %d − %d = %d." % (
            a, -js[0], a + js[0], a + js[0], -js[1], a + js[0] + js[1], a + js[0] + js[1], -js[2], r, a, b, r)
        its.append(mcq(fig(nline_svg(a, js, ticks)) + "Where does the last jump land?", r,
                       [r - js[2], sub_small_from_big(a, b), a + b, r + 10], e))
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
    # near hundreds: jump too far, then back
    its.append(mcq("199 is 1 less than 200. What is 456 + 199?", 655, [657, 656, add_no_regroup(456, 199)],
                   "Add 200, then take away the extra 1. 456 + 200 = 656. 656 − 1 = <b>655</b>."))
    its.append(mcq("298 is 2 less than 300. What is 347 + 298?", 645, [649, 647, add_no_regroup(347, 298)],
                   "Add 300, then take away the extra 2. 347 + 300 = 647. 647 − 2 = <b>645</b>."))
    its.append(mcq("198 is 2 less than 200. What is 532 − 198?", 334, [330, 332, sub_small_from_big(532, 198)],
                   "Take away 200. You took away 2 too many, so add 2 back. 532 − 200 = 332. 332 + 2 = <b>334</b>."))
    assert 456 + 199 == 655 and 347 + 298 == 645 and 532 - 198 == 334
    assert len(its) == 20, len(its)
    return {"title": "Rearrange and use the jump strategy", "items": its}


# ------------------------------------------------------------ set 5: word problems
def unit(v, u):
    return "$%d" % v if u == "$" else "%d %s" % (v, u)


def eu(v, u):
    return "$%d" % v if u == "$" else str(v)


def story(q, ans, cands, u, e):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e)


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
    e = ("Work backwards. Add back the %d that were lost: %s + %s = <b>%s</b>. Check: %s − %s = %s."
         % (lost, eu(now, u), eu(lost, u), eu(x, u), eu(x, u), eu(lost, u), eu(now, u)))
    return story(q, x, [now - lost] + add_cands(now, lost), u, e)


def both_left(q, A, B, C, u, s1, s2):
    """A − (B + C)."""
    t = B + C
    r = A - t
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
    n = [P.next() for _ in range(4)]
    its = [
        one_add("The school canteen sold 236 icy poles in Term 1 and 158 in Term 2. How many icy poles did it sell altogether?",
                236, 158, "icy poles", "Altogether means add."),
        one_add("A junior footy carnival had 347 people on Saturday and 285 people on Sunday. "
                "How many people came over the weekend?", 347, 285, "people", "Put the two days together, so add."),
        one_add("On a road trip, a family drove 268 km on the first day and 345 km on the second day. "
                "How far did they drive altogether?", 268, 345, "km", "Altogether means add."),
        one_add("The school library has 476 picture books and 185 chapter books. How many books is that altogether?",
                476, 185, "books", "Altogether means add."),
        one_sub("The library has 742 books. 158 books are borrowed. How many books are still on the shelves?",
                742, 158, "books", "Borrowed books leave the shelves, so subtract."),
        one_sub("The P&C wants to raise $600 for new sports equipment. It has raised $364. How much more does it need?",
                600, 364, "$", "Find the difference, so subtract."),
        one_sub("A family is driving 450 km to the beach. They have driven 287 km. How many kilometres are left?",
                450, 287, "km", "Find what is left, so subtract."),
        one_sub("The sausage sizzle had 634 sausages. 479 sausages were sold. How many sausages were left?",
                634, 479, "sausages", "Sold ones are taken away, so subtract."),
        one_sub("At the swimming carnival, Red house scored 312 points and Blue house scored 245 points. "
                "How many more points did Red house score?", 312, 245, "points", "How many more means find the difference, so subtract."),
        one_sub("The school concert has 500 tickets. 263 tickets have been sold. How many tickets are left?",
                500, 263, "tickets", "Find what is left, so subtract."),
        one_sub("A road trip is 703 km long. The family stops for lunch after 285 km. How much further do they have to drive?",
                703, 285, "km", "Find the distance left, so subtract."),
        start_add("%s had some footy cards. %s was given 145 more. Now %s has 403 cards. How many cards did %s have at the start?"
                  % (n[0][0], cap(n[0][1]), n[0][1], n[0][1]), 403, 145, "cards"),
        start_sub("%s had some points in a maths game. %s lost 175 points. Now %s has 389 points. "
                  "How many points did %s have at the start?" % (n[1][0], cap(n[1][1]), n[1][1], n[1][1]), 389, 175, "points"),
        both_left("The canteen had 512 bottles of water. It sold 168 at recess and 195 at lunch. How many bottles are left?",
                  512, 168, 195, "bottles", "bottles sold", "bottles left"),
        out_then_in("The library had 625 books. 248 books were borrowed. Then 136 books came back. How many books are there now?",
                    625, 248, 136, "books", "after borrowing", "after the books came back"),
        more_total("Year 3 collected 286 cans for recycling. Year 4 collected 157 more cans than Year 3. "
                   "How many cans did they collect altogether?", 286, 157, "cans", "Year 4’s cans"),
        less_total("On Monday a family drove 374 km. On Tuesday they drove 128 km less. How far did they drive on the two days?",
                   374, 128, "km", "Tuesday"),
        both_left("The school needs $800 for an excursion bus. The disco raised $356 and the sausage sizzle raised $287. "
                  "How much more money is needed?", 800, 356, 287, "$", "money raised", "money still needed"),
        both_left("%s’s book has 400 pages. %s read 132 pages on the weekend and 89 pages on Monday. "
                  "How many pages are left to read?" % (n[2][0], cap(n[2][1])), 400, 132, 89, "pages", "pages read", "pages left"),
        more_total("A cricket club’s junior teams scored 245 runs on Saturday. On Sunday they scored 136 more runs than on Saturday. "
                   "How many runs did they score over the weekend?", 245, 136, "runs", "Sunday’s runs"),
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
    assert 245 + 132 == 377 and 247 + 135 == 382 and 367 + 258 == 625 and 452 - 178 == 274 and 402 - 158 == 244
    assert add_no_regroup(367, 258) == 515 and sub_small_from_big(452, 178) == 326 and sub_zero_skip(402, 158) == 254
    assert 245 + 100 + 3 + 2 == 350 and 623 - 245 == 378
    return (
        "<h2>The idea: partition, then put it back together</h2>"
        "<p>Every number is made of hundreds, tens and ones. <b>Partition</b> (split) the numbers. "
        "Add the hundreds, the tens and the ones. Then put the parts back together.</p>"
        "<figure class='sn-fig'>" + split_svg(245, 132, "+") +
        "<figcaption>245 + 132. Hundreds: 200 + 100 = 300. Tens: 40 + 30 = 70. Ones: 5 + 2 = 7. "
        "300 + 70 + 7 = 377.</figcaption></figure>"
        "<p>If the ones make 10 or more, <b>regroup</b>: 10 ones make 1 ten.</p>"
        "<figure class='sn-fig'>" + blocks_svg(247, 135) +
        "<figcaption>247 + 135 with MAB. 7 + 5 = 12 ones. Regroup 10 ones as 1 ten. "
        "300 + 70 + 12 = 382.</figcaption></figure>"
        "<h2>The column method: regroup when a column makes 10 or more</h2>"
        "<p>Put <b>ones under ones</b>, tens under tens and hundreds under hundreds. Start with the ones on the right. "
        "If a column makes 10 or more, write the ones digit and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(367, 258, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 8 = 15. Write 5, regroup 1 ten. Tens: 6 + 5 + 1 = 12. Write 2, regroup 1 hundred. "
        "Hundreds: 3 + 2 + 1 = 6. Answer: 625.</figcaption></figure>"
        "<h2>Subtracting: regroup when the top digit is smaller</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, "
        "regroup 1 from the next column as 10.</p>"
        "<figure class='sn-fig'>" + column_svg(452, 178, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8. Regroup 1 ten as 10 ones: 12 − 8 = 4. Tens: 4 − 7. "
        "Regroup 1 hundred as 10 tens: 14 − 7 = 7. Hundreds: 3 − 1 = 2. Answer: 274.</figcaption></figure>"
        "<p><b>Across a zero:</b> if there are 0 tens, regroup 1 hundred as 10 tens first. "
        "Then regroup 1 ten as 10 ones. The 0 becomes 9.</p>"
        "<figure class='sn-fig'>" + column_svg(402, 158, "-", answer=True, marks=True, fs=34) +
        "<figcaption>402 becomes 3 hundreds, 9 tens and 12 ones. 12 − 8 = 4, 9 − 5 = 4, 3 − 1 = 2. "
        "Answer: 244.</figcaption></figure>"
        "<h2>The jump strategy on an empty number line</h2>"
        "<p>Start at the first number. Jump the hundreds, then the tens, then the ones.</p>"
        "<figure class='sn-fig'>" + nline_svg(623, [-200, -40, -5], ["623", "423", "383", "378"]) +
        "<figcaption>623 − 245: jump back 200 to 423, back 40 to 383, back 5 to 378.</figcaption></figure>" +
        ex("Rearrange", "What is 38 + 145 + 62?",
           "You can add in any order. 38 + 62 = 100. Then 100 + 145 = 245.", "245") +
        ex("Near a hundred", "What is 456 + 199?", "199 is 1 less than 200. 456 + 200 = 656. Take away the extra 1: 655.", "655") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the regrouped ten (367 + 258 = 515)", "Write the regrouped 1 under the next column and add it in"],
            ["Taking the smaller digit from the larger one (452 − 178 = 326)", "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Not regrouping across a zero (402 − 158 = 254)", "Regroup 1 hundred as 10 tens first. The 0 becomes 9"],
            ["Adding tens as if they were ones (245 + 132 = 350)", "The 3 in 132 is 3 tens, worth 30: 245 + 132 = 377"],
        ])
    )


FAQ = [
    {"q": "What does Year 3 learn about adding and subtracting in the Australian Curriculum?",
     "a": "Students add and subtract two- and three-digit numbers without a calculator. They partition, rearrange and regroup numbers, for example using the split strategy, the jump strategy and the column method."},
    {"q": "What is regrouping in maths?",
     "a": "Regrouping means swapping 10 of one place for 1 of the next, such as 10 ones for 1 ten. It is also called trading, and older books call it carrying or borrowing."},
    {"q": "How do you subtract across a zero, like 402 − 158?",
     "a": "Regroup 1 hundred as 10 tens, then 1 ten as 10 ones. 402 becomes 3 hundreds, 9 tens and 12 ones, and the answer is 244."},
    {"q": "Is adding and subtracting on the Year 3 NAPLAN numeracy test?",
     "a": "Yes. Adding and subtracting with two- and three-digit numbers is part of the Year 3 Australian Curriculum, which the numeracy test is based on, and many questions are word problems."},
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
            m = re.search(r"What is (\d+) ([+−]) (\d+)( [+] (\d+))?\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                v = a + b if op == "+" else a - b
                if m.group(5):
                    v += int(m.group(5))
                assert int(right) == v, it["q"]
            m = re.search(r"aria-label='MAB blocks showing (\d+) and (\d+)'", it["q"])
            if m:
                assert int(right) == int(m.group(1)) + int(m.group(2))


def gen():
    rnd = random.Random(3802)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_partition(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_jump(), set_story(P)]
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
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "adding-and-subtracting", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting 2- and 3-Digit Numbers",
        "seo_title": "Year 3 Adding and Subtracting Worksheets: Partitioning, Regrouping and the Jump Strategy",
        "short_title": "Adding and subtracting",
        "domain": "Number",
        "standard_code": "AC9M3N03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Add and subtract two- and three-digit numbers using place value to partition, rearrange and regroup "
                         "numbers to assist in calculations without a calculator",
        "meta_desc": "Free Year 3 maths worksheets on adding and subtracting two- and three-digit numbers, matched to the "
                     "Australian Curriculum (AC9M3N03): the split strategy, MAB, regrouping, subtracting across a zero, the jump "
                     "strategy and word problems. 100 questions with an answer key. Great NAPLAN practice.",
        "key_big": "Partition into hundreds, tens and ones. Regroup when you need to.",
        "key_sub": "10 ones make 1 ten and 10 tens make 1 hundred. Adding: if a column makes 10 or more, regroup 1 into the "
                   "next column. Subtracting: if the top digit is smaller, regroup 1 from the next column.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "MAB blocks|empty number line|split strategy")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
