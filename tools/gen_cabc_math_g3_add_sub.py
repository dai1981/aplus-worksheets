# -*- coding: utf-8 -*-
"""
CA-BC Grade 3 Math: Adding and subtracting to 1000 (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g3_add_sub.py
Facts to 20 warm-up (ten frames, make ten, think addition), mental strategies (jump, split,
compensate, count on), column addition with regrouping, column subtraction including across zeros,
and British Columbia word problems (BC Ferries passengers, salmon counts).
Canadian English. Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_caon_math_g3_add_sub.py and gen_cabc_math_g2_facts.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
BLUE = "#2e6fb7"
FONT = "Arial, Helvetica, sans-serif"
B = "<b>?</b>"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
ONE = ["one", "ten", "hundred", "thousand"]


def holds(eq, ans=None):
    """'8 + ? = 15' is true with ? = ans (real minus sign allowed)."""
    s = eq.replace(B, "?")
    if ans is not None:
        s = s.replace("?", str(ans))
    s = s.replace("−", "-")
    vals = [eval(p.strip(), {"__builtins__": {}}) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def wrong_way(a, b):
    """'Smaller from larger' for a teen number minus a one-digit number: 13 − 5 -> 10 + (5 − 3) = 12."""
    t, o = divmod(a, 10)
    assert t == 1 and b < 10 and b > o
    return 10 * t + (b - o)

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

# ------------------------------------------------------------ pictures: ten frames
CELL = 30
FW, FH = 5 * CELL, 2 * CELL     # one ten frame: 150 x 60


def cross(cx, cy, r=12):
    return ("<path d='M %d %d L %d %d M %d %d L %d %d' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            % (cx - r, cy - r, cx + r, cy + r, cx - r, cy + r, cx + r, cy - r, INK))


def frame(x0, y0, colors, crossed=0):
    """One ten frame. colors: up to 10 counter colours, top row first. The last `crossed` counters get an X."""
    assert len(colors) <= 10
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='3'/>"
         % (x0, y0, FW, FH, INK)]
    for i in range(1, 5):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                 % (x0 + i * CELL, y0, x0 + i * CELL, y0 + FH, INK))
    s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0, y0 + CELL, x0 + FW, y0 + CELL, INK))
    for k, col in enumerate(colors):
        r, c = divmod(k, 5)
        cx, cy = x0 + c * CELL + CELL // 2, y0 + r * CELL + CELL // 2
        s.append("<circle cx='%d' cy='%d' r='10' fill='%s'/>" % (cx, cy, col))
        if k >= len(colors) - crossed:
            s.append(cross(cx, cy))
    return "".join(s)


def ten_frame_svg(colors, label, crossed=0):
    o = 6
    return svg_wrap(FW + 2 * o, FH + 2 * o, frame(o, o, colors, crossed), label)


def two_frames_svg(top, bottom, label):
    """Two ten frames stacked (compact for print)."""
    o, gap = 6, 12
    body = frame(o, o, top) + frame(o, o + FH + gap, bottom)
    return svg_wrap(FW + 2 * o, 2 * FH + gap + 2 * o, body, label)


def frames_fill(a, b):
    """a red then b blue counters, filling the top frame first (shows make ten)."""
    cols = [RED] * a + [BLUE] * b
    return two_frames_svg(cols[:10], cols[10:], "two ten frames with %d red and %d blue counters" % (a, b))


def frames_split(a, b, extra_b=0):
    """a red counters in the top frame, b counters in the bottom frame (the last extra_b of them blue)."""
    return two_frames_svg([RED] * a, [RED] * (b - extra_b) + [BLUE] * extra_b,
                          "two ten frames with %d and %d counters" % (a, b))


# ------------------------------------------------------------ pictures: part-whole model
def part_whole_svg(whole, p1, p2):
    """Whole on top, two parts below. Values are numbers or '?'."""
    r = 28
    W, H = 184, 148
    cw, cy0 = W / 2, 6 + r
    c1, c2, cy1 = 8 + r, W - 8 - r, H - 6 - r
    s = []
    for cx in (c1, c2):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (cw, cy0 + r - 2, cx, cy1 - r + 2, INK))
    for cx, cy, v, fill in [(cw, cy0, whole, FILL), (c1, cy1, p1, "#fff"), (c2, cy1, p2, "#fff")]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    if "?" not in (whole, p1, p2):
        assert p1 + p2 == whole
    return svg_wrap(W, H, "".join(s), "part-whole model: whole %s, parts %s and %s" % (whole, p1, p2))


# ------------------------------------------------------------ pictures: number line
def hop_line_svg(lo, hi, label="?"):
    """Number line from lo to hi, one tick per number, one hop from lo to hi."""
    L, step, Y = 22, 36, 70
    W = 2 * L + (hi - lo) * step
    X = lambda v: L + (v - lo) * step
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 12, Y, W - L + 12, Y, INK)]
    for v in range(lo, hi + 1):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), Y - 7, X(v), Y + 7, INK))
        s.append(text(X(v), Y + 27, str(v), 15))
    x1, x2 = X(lo), X(hi)
    s.append("<path d='M %d %d A %.1f %d 0 0 1 %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (x1, Y - 2, (x2 - x1) / 2, 40, x2, Y - 2, GREEN))
    s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
             "stroke-linejoin='round'/>" % (x2 - 6, Y - 12, x2, Y - 3, x2 + 6, Y - 12, GREEN))
    s.append(text((x1 + x2) / 2, Y - 48, label, 17, col=RED if label == "?" else GREEN))
    return svg_wrap(W, Y + 36, "".join(s), "number line from %d to %d with one hop" % (lo, hi))

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



# ------------------------------------------------------------ set 1: facts to 20 warm-up
def set_facts(P):
    its = []

    def add(q, right, wrong, e, eq=None):
        if eq:
            assert holds(eq, right), eq
            for w in wrong:
                assert not holds(eq, w), (eq, w)
        its.append(mcq(q, right, wrong, e))

    # make ten with two ten frames
    for a, b in [(9, 5), (8, 7), (7, 6), (9, 8)]:
        need = 10 - a
        add(fig(frames_fill(a, b)) + "Fill the top frame first. What is %d + %d?" % (a, b), a + b,
            [a + b - 1, a + b + 1, 10 + b, a - b],
            "%d needs %d more to make 10. Take %d from the %d: %d %s left. 10 + %d = <b>%d</b>."
            % (a, need, need, b, b - need, "is" if b - need == 1 else "are", b - need, a + b), "%d + %d = ?" % (a, b))
    # how many more to make 20
    add(fig(two_frames_svg([RED] * 10, [RED] * 3, "two ten frames with 13 counters")) +
        "How many more counters fill both frames to make 20?", 7, [3, 6, 8, 33],
        "The frames hold 20. There are 13 counters. 13 + 7 = 20, so <b>7</b> more make 20.", "13 + ? = 20")
    # doubles and near doubles
    add("Use double 7. What is 7 + 8?", 15, [14, 16, 1],
        "Double 7 is 14. 8 is 1 more than 7, so add 1: <b>15</b>.", "7 + 8 = ?")
    # subtraction facts: think addition (smaller-from-larger mistake)
    for a, b in [(14, 6), (12, 5), (16, 9)]:
        d = a - b
        add("What is %d − %d?" % (a, b), d, [wrong_way(a, b), d + 1, a + b],
            "Think addition: %d + %s = %d. %d + %d = %d, so %d − %d = <b>%d</b>." % (b, "?", a, b, d, a, a, b, d),
            "%d − %d = ?" % (a, b))
    for a, b in [(13, 8), (17, 9)]:
        d = a - b
        add(fig(hop_line_svg(b, a)) + "Count up from %d to %d. What is %d − %d?" % (b, a, a, b), d,
            [d + 1, a + b, wrong_way(a, b)],
            "Count the steps from %d to %d: there are %d. %d + %d = %d, so %d − %d = <b>%d</b>."
            % (b, a, d, b, d, a, a, b, d), "%d − %d = ?" % (a, b))
    # missing numbers
    add("What number goes in the box?  8 + %s = 15" % B, 7, [23, 8, 6],
        "Think: 8 and how many more make 15? 8 + 2 = 10, 10 + 5 = 15. 2 + 5 = <b>7</b>. "
        "(23 adds 8 + 15 instead.)", "8 + ? = 15")
    add("What number goes in the box?  %s + 6 = 13" % B, 7, [19, 6, 8],
        "13 − 6 = <b>7</b>. Check: 7 + 6 = 13. (19 adds instead of taking away.)", "? + 6 = 13")
    # fact family
    opts = ["16 − 9 = 7", "16 + 9 = 25", "9 − 7 = 2", "7 + 16 = 23"]
    assert all(holds(o) for o in opts)
    add("Which fact is in the same fact family as 7 + 9 = 16?", opts[0], opts[1:],
        "A fact family uses the same three numbers: 7, 9 and 16. <b>16 − 9 = 7</b> uses all three.")
    # facts help with bigger numbers
    add("9 + 6 = 15. Use this fact. What is 90 + 60?", 150, [15, 1500, 96],
        "9 tens + 6 tens = 15 tens. 15 tens is <b>150</b>.", "90 + 60 = ?")
    add("14 − 8 = 6. Use this fact. What is 140 − 80?", 60, [6, 600, 140 - 8],
        "14 tens − 8 tens = 6 tens. 6 tens is <b>60</b>.", "140 − 80 = ?")
    # short stories
    p = P.next()
    add("%s saw 8 bald eagles by the river in the morning and 7 more in the afternoon. "
        "How many bald eagles did %s see?" % (p[0], p[1]), 15, [1, 14, 16],
        "Put the two groups together, so add. 8 + 2 = 10, 10 + 5 = 15. 8 + 7 = <b>15</b>.", "8 + 7 = ?")
    p = P.next()
    add("%s had 13 stickers. %s gave 5 stickers to a friend. How many stickers does %s have now?"
        % (p[0], cap(p[1]), p[1]), 8, [18, wrong_way(13, 5), 9],
        "Giving away means subtract. 13 − 3 = 10, 10 − 2 = 8. 13 − 5 = <b>8</b>.", "13 − 5 = ?")
    p = P.next()
    assert wrong_way(15, 7) == 12 and 15 - 7 == 8
    add("%s says 15 − 7 = 12. What did %s do wrong?" % (p[0], p[1]), "%s did 7 − 5" % cap(p[1]),
        ["%s added 7" % cap(p[1]), "%s counted back 2" % cap(p[1]), "Nothing. %s is right." % cap(p[1])],
        "15 − 7 = 8. %s saw 5 and 7 and took the smaller digit from the larger one: 7 − 5 = 2, "
        "so %s wrote 12. Think addition instead: 7 + 8 = 15. <b>%s did 7 − 5</b>." % (p[0], p[1], cap(p[1])))
    add("Which one does NOT make 20?", "11 + 8", ["12 + 8", "15 + 5", "10 + 10"],
        "11 + 8 = 19, not 20. So <b>11 + 8</b> does not make 20. 12 + 8, 15 + 5 and 10 + 10 all make 20.")
    assert 11 + 8 != 20 and 12 + 8 == 20 and 15 + 5 == 20 and 10 + 10 == 20
    assert len(its) == 20, len(its)
    return {"title": "Warm-up: addition and subtraction facts to 20", "items": its}


# ------------------------------------------------------------ set 2: mental strategies
def part_add_cands(a, b):
    """Split strategy mistakes for a + b."""
    da, db = digits(a), digits(b)
    H, T, O = da[2] + db[2], da[1] + db[1], da[0] + db[0]
    out = []
    if O >= 10:
        out.append(H * 100 + T * 10 + O % 10)                    # forgot the regrouped ten
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
    assert 527 + 300 == 827 and 864 - 50 == 814
    its.append(mcq("What is 527 + 300?", 827, [557, 530, 227],
                   "Only the hundreds change. 5 hundreds + 3 hundreds = 8 hundreds. 527 + 300 = <b>827</b>."))
    its.append(mcq("What is 864 − 50?", 814, [364, 859, 914],
                   "Only the tens change. 6 tens − 5 tens = 1 ten. 864 − 50 = <b>814</b>."))
    for a, b, pic in [(231, 154, True), (347, 128, True), (456, 239, False)]:
        assert digits(a)[1] + digits(b)[1] + 1 < 10 and a + b <= 999
        q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %d + %d?" % (a, b)
        its.append(mcq(q, a + b, part_add_cands(a, b), part_add_e(a, b)))
    assert 400 + 70 + 12 == 345 + 137
    its.append(mcq("Use the split strategy. 345 + 137 = 400 + <b>?</b> + 12", 70, [7, 80, 700],
                   "Tens: 40 + 30 = <b>70</b>. Hundreds: 300 + 100 = 400. Ones: 5 + 7 = 12. 400 + 70 + 12 = 482. "
                   "(80 counts the regrouped ten twice: the 12 already holds it.)"))
    a, b = 236, 148
    da, db = digits(a), digits(b)
    e = ("Count each kind of block. Hundreds: %d + %d = %d. Tens: %d + %d = %d. Ones: %d + %d = %d. "
         "Regroup 10 ones as 1 ten: %d tens and %d ones. The total is <b>%d</b>."
         % (da[2], db[2], da[2] + db[2], da[1], db[1], da[1] + db[1], da[0], db[0], da[0] + db[0],
            da[1] + db[1] + 1, da[0] + db[0] - 10, a + b))
    its.append(mcq(fig(blocks_svg(a, b)) + "The base ten blocks show two numbers. What is the total?",
                   a + b, part_add_cands(a, b), e))
    assert 254 + 343 == 597
    its.append(mcq("Start at 254. Jump forward 300, then 40, then 3. Where do you land?", 597, [594, 557, 697],
                   "254 + 300 = 554. 554 + 40 = 594. 594 + 3 = <b>597</b>. This is the jump strategy for 254 + 343."))
    assert 924 - 478 == 446 and sub_small_from_big(924, 478) == 554
    its.append(mcq("Start at 924. Jump back 400, then 70, then 8. Where do you land?", 446, [454, 554, 456],
                   "924 − 400 = 524. 524 − 70 = 454. 454 − 8 = <b>446</b>. This is the jump strategy for 924 − 478."))
    assert 426 + 352 == 778
    its.append(mcq(fig(nline_svg(426, [300, 50, 2], ["426", "726", "776", "?"])) + "Where does the last jump land?",
                   778, [776, 788, 678],
                   "426 + 300 = 726. 726 + 50 = 776. 776 + 2 = <b>778</b>. So 426 + 352 = 778."))
    assert 851 - 427 == 424 and sub_small_from_big(851, 427) == 436
    its.append(mcq(fig(nline_svg(851, [-400, -20, -7], ["851", "451", "431", "?"])) + "Where does the last jump land?",
                   424, [431, 436, 524],
                   "851 − 400 = 451. 451 − 20 = 431. 431 − 7 = <b>424</b>. So 851 − 427 = 424."))
    assert 318 + 527 == 845
    its.append(mcq(fig(nline_svg(318, [500, 20, 7], ["318", "818", "838", "845"])) +
                   "Which calculation does the number line show?", "318 + 527", ["318 + 572", "845 + 527", "527 − 318"],
                   "It starts at 318 and jumps +500, +20 and +7. 500 + 20 + 7 = 527, so it shows <b>318 + 527</b> = 845."))
    assert 465 + 324 == 789
    its.append(mcq(fig(nline_svg(465, [300, 20, 4], ["465", "765", "785", "789"], ["?", "+20", "+4"])) +
                   "What is the missing jump?", "+300", ["+3", "+30", "+324"],
                   "From 465 to 765 the hundreds digit goes up from 4 to 7, so the jump is <b>+300</b>. "
                   "Check: 465 + 324 = 789."))
    for a, b, js in [(512, 497, [3, 12]), (804, 788, [12, 4])]:
        d = a - b
        assert sum(js) == d and (b + js[0]) % 100 == 0
        ticks = [str(b), str(b + js[0]), str(a)]
        e = ("The numbers are close, so count on from %d. %d + %d = %d, then %d + %d = %d. %d + %d = <b>%d</b>. "
             "So %d − %d = %d." % (b, b, js[0], b + js[0], b + js[0], js[1], a, js[0], js[1], d, a, b, d))
        its.append(mcq(fig(nline_svg(b, js, ticks)) + "Count on to find the difference. What is %d − %d?" % (a, b), d,
                       clean([sub_zero_as_ten(a, b), sub_small_from_big(a, b), js[1], js[0], d + 10]), e))
    assert 538 + 199 == 737 and 426 + 398 == 824 and 645 - 298 == 347 and 723 - 99 == 624
    its.append(mcq("199 is 1 less than 200. What is 538 + 199?", 737, [739, 738, add_no_regroup(538, 199)],
                   "Add 200, then take away the extra 1. 538 + 200 = 738. 738 − 1 = <b>737</b>."))
    its.append(mcq("398 is 2 less than 400. What is 426 + 398?", 824, [828, 826, add_no_regroup(426, 398)],
                   "Add 400, then take away the extra 2. 426 + 400 = 826. 826 − 2 = <b>824</b>."))
    its.append(mcq("298 is 2 less than 300. What is 645 − 298?", 347, [343, 345, sub_small_from_big(645, 298)],
                   "Take away 300. You took away 2 too many, so add 2 back. 645 − 300 = 345. 345 + 2 = <b>347</b>."))
    its.append(mcq("99 is 1 less than 100. What is 723 − 99?", 624, [622, 623, sub_small_from_big(723, 99)],
                   "Take away 100. You took away 1 too many, so add 1 back. 723 − 100 = 623. 623 + 1 = <b>624</b>."))
    assert 47 + 236 + 53 == 336 and 47 + 236 == 283
    its.append(mcq("Add 47 and 53 first to make 100. What is 47 + 236 + 53?", 336, [326, 283, 436],
                   "47 + 53 = 100 (7 + 3 = 10, then 40 + 50 + 10 = 100). 100 + 236 = <b>336</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Mental strategies: jump, split, compensate and count on", "items": its}


# ------------------------------------------------------------ set 5: BC word problems
def set_story(P):
    n = [P.next() for _ in range(5)]
    its = [
        one_add("A BC Ferries sailing to Nanaimo carried 386 passengers on Saturday morning. The next sailing "
                "carried 457 passengers. How many passengers did the two sailings carry?",
                386, 457, "passengers", "Put the two sailings together, so add."),
        one_add("Students counted 248 salmon in a creek on Monday and 175 salmon on Tuesday. "
                "How many salmon did they count in the two days?", 248, 175, "salmon", "Put the two days together, so add."),
        one_add("At our school’s Terry Fox Run, Grade 3 raised $165 and Grade 2 raised $278. "
                "How much money did the two grades raise?", 165, 278, "$", "Put the two amounts together, so add."),
        one_add("On Saturday, 356 people rode the Skyride up Grouse Mountain in the morning and 287 people rode it "
                "in the afternoon. How many people rode it that day?", 356, 287, "people",
                "Put the morning and the afternoon together, so add."),
        one_add("On a trip in BC, the Singh family drove 276 km on Friday and 358 km on Saturday. "
                "How far did they drive in the two days?", 276, 358, "km", "Put the two parts of the trip together, so add."),
        one_sub("A ferry can carry 600 passengers. 437 passengers are on board. How many more passengers can get on?",
                600, 437, "passengers", "Find how many more fit, so subtract."),
        one_sub("Last fall, volunteers counted 812 salmon in a river. This fall they counted 547. "
                "How many fewer salmon did they count this fall?", 812, 547, "salmon",
                "How many fewer means find the difference, so subtract."),
        one_sub("Volunteers counted 436 coho salmon and 289 chinook salmon at a counting fence. "
                "How many more coho salmon did they count?", 436, 289, "salmon",
                "How many more means find the difference, so subtract."),
        one_sub("%s’s chapter book has 304 pages. %s has read 128 pages. How many pages are left?"
                % (n[0][0], cap(n[0][1])), 304, 128, "pages", "Find what is left, so subtract."),
        one_sub("The class wants $500 for a field trip to the Vancouver Aquarium. It has $368 so far. "
                "How much more money does it need?", 500, 368, "$", "Find the difference, so subtract."),
        one_sub("The school library has 750 books. 286 books are checked out. How many books are on the shelves?",
                750, 286, "books", "Books checked out are taken away, so subtract."),
        start_add("%s had some hockey cards. %s got 135 more for %s birthday. Now %s has 402 cards. "
                  "How many cards did %s have at the start?" % (n[1][0], cap(n[1][1]), n[1][2], n[1][1], n[1][1]),
                  402, 135, "cards"),
        start_sub("A ferry stopped at Salt Spring Island and 168 passengers got off. Now 279 passengers are on the ferry. "
                  "How many passengers were on the ferry before the stop?", 279, 168, "passengers"),
        both_left("The school’s Terry Fox Run goal is $800. Grade 3 raised $276 and Grade 4 raised $348. "
                  "How much more money is needed?", 800, 276, 348, "$", "money raised", "money still needed"),
        both_left("A trail through the cedar trees in Stanley Park is 900 m long. %s walked 345 m, rested, "
                  "then walked 278 m. How many metres are left?" % n[2][0], 900, 345, 278, "m", "metres walked",
                  "metres left"),
        out_then_in("A ferry to the Gulf Islands left with 534 passengers. At the first island, 185 passengers got off "
                    "and 98 passengers got on. How many passengers are on the ferry now?", 534, 185, 98, "passengers",
                    "after the passengers got off", "after the new passengers got on"),
        more_total("On Saturday, students counted 268 salmon in a creek. On Sunday they counted 149 more than on "
                   "Saturday. How many salmon did they count on the two days?", 268, 149, "salmon", "Sunday’s salmon"),
        less_total("In the first hour, 386 people got on the SkyTrain at one station. In the second hour, 127 fewer "
                   "people got on. How many people got on in the two hours?", 386, 127, "people", "the second hour"),
        more_total("%s read 236 pages over Spring Break. %s read 148 more pages than %s. "
                   "How many pages did they read together?" % (n[3][0], n[4][0], n[3][0]), 236, 148, "pages",
                   "the second reader’s pages"),
        one_sub("The ferry from Tsawwassen had 905 passengers on board. 368 of them were in cars. "
                "The rest walked on. How many passengers walked on?", 905, 368, "passengers",
                "Take the passengers in cars away from all the passengers, so subtract."),
    ]
    assert len(its) == 20
    return {"title": "BC word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 245 + 132 == 377 and 367 + 258 == 625 and 452 - 178 == 274 and 500 - 168 == 332 and 8 + 5 == 13
    assert add_no_regroup(367, 258) == 515 and sub_small_from_big(452, 178) == 326 and sub_zero_as_ten(500, 168) == 342
    assert add_misalign(346, 52) == 866 and 346 + 52 == 398 and 623 - 245 == 378 and 375 + 198 == 573
    assert wrong_way(13, 5) == 12
    return (
        "<h2>Start with facts to 20</h2>"
        "<p>Big sums are built from small facts. <b>Make ten</b> to add. <b>Think addition</b> to subtract.</p>"
        "<figure class='sn-fig'>" + frames_fill(8, 5) +
        "<figcaption>8 + 5: move 2 counters to fill the top frame. 10 + 3 = 13.</figcaption></figure>"
        "<p>For 13 − 5, think: 5 + what = 13? 5 + 8 = 13, so 13 − 5 = 8.</p>"
        "<h2>Split into hundreds, tens and ones</h2>"
        "<p><b>Split</b> both numbers. Add the hundreds, the tens and the ones. Then put the parts back together.</p>"
        "<figure class='sn-fig'>" + split_svg(245, 132, "+") +
        "<figcaption>245 + 132. Hundreds: 200 + 100 = 300. Tens: 40 + 30 = 70. Ones: 5 + 2 = 7. "
        "300 + 70 + 7 = 377.</figcaption></figure>"
        "<h2>Mental strategies: jump and compensate</h2>"
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
        "Answer: 332.</figcaption></figure>" +
        ex("Check with the inverse", "Is 500 − 168 = 332 right?", "Add back what you took away: 332 + 168 = 500. "
           "You get the starting number, so it is right.", "Yes") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not regrouping (367 + 258 = 515)", "Write the regrouped 1 in the next column and add it in"],
            ["Taking the smaller digit from the larger one (452 − 178 = 326, 13 − 5 = 12)",
             "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Making the 0 tens into 10 tens (500 − 168 = 342)", "One ten moves to the ones, so 10 tens become 9 tens"],
            ["Lining up the columns wrongly (346 + 52 = 866)", "Line up the ones on the right: 346 + 52 = 398"],
        ])
    )


FAQ = [
    {"q": "What does Grade 3 learn about adding and subtracting in the BC math curriculum?",
     "a": "Under Computational fluency, Grade 3 students add and subtract to 1000 and become fluent with addition and subtraction facts to 20. They use mental strategies, base ten blocks, number lines and the column method."},
    {"q": "What is regrouping in Grade 3 math?",
     "a": "Regrouping means trading 10 of one place for 1 of the next, such as 10 ones for 1 ten. Older books call it carrying or borrowing."},
    {"q": "How do you subtract across zeros, like 500 − 168?",
     "a": "Regroup 1 hundred as 10 tens, then 1 ten as 10 ones. 500 becomes 4 hundreds, 9 tens and 10 ones, so 500 − 168 = 332."},
    {"q": "Do Grade 3 students in BC write a provincial math test?",
     "a": "No. BC students write the Foundation Skills Assessment (FSA) in Grades 4 and 7. Strong adding and subtracting in Grade 3 is a good base for it."},
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
            m = re.search(r"aria-label='base ten blocks showing (\d+) and (\d+)'", it["q"])
            if m:
                assert int(right) == int(m.group(1)) + int(m.group(2))


def gen():
    rnd = random.Random(53803)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_facts(P), set_mental(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_story(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "adding-and-subtracting-to-1000", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to 1000",
        "seo_title": "Grade 3 Adding and Subtracting to 1000 Worksheets: Regrouping and Mental Math (BC)",
        "short_title": "Adding and subtracting to 1000",
        "domain": "Computational fluency",
        "standard_code": "Grade 3: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Addition and subtraction to 1000",
        "meta_desc": "Free Grade 3 math worksheets on adding and subtracting to 1000, matched to the BC curriculum: "
                     "facts to 20, mental strategies, column addition and subtraction with regrouping, subtracting "
                     "across zeros and BC word problems. 100 questions with an answer key.",
        "key_big": "Know your facts to 20. Line up hundreds, tens and ones. Regroup when you need to.",
        "key_sub": "Adding: if a column makes 10 or more, regroup 1 into the next column. Subtracting: if the top digit "
                   "is smaller, regroup 1 from the next column. Check: add back what you took away.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "base ten blocks|open number line|split strategy|number line from")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
