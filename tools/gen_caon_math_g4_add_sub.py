# -*- coding: utf-8 -*-
"""
CA-ON Grade 4 Math: Adding and subtracting to 10 000 (Ontario Curriculum 2020, B2.4)
  python3 tools/gen_caon_math_g4_add_sub.py
Mental strategies (compensate, split, count on), column addition and subtraction with regrouping
(also across zeros, like 5000 − 1268), adding and subtracting decimal tenths (4.6 + 2.7), Ontario word problems.
Canadian English. 4-digit numbers have no separator (4536); 10 000 uses a no-break space.
Every answer and every wrong answer is computed in code (decimals are worked in tenths as whole numbers).
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_cabc_math_g4_add_sub.py (same column method, rewritten for Ontario).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]
PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands"]
ONE = ["one", "ten", "hundred", "thousand", "ten thousand"]
TEN_K = "10" + NB + "000"


def f(n):
    """4 digits no separator, 5+ digits a no-break space between groups of three."""
    s = str(n)
    if len(s) <= 4:
        return s
    return "{:,}".format(n).replace(",", NB)


def num(s):
    return int(s.replace(NB, "").replace("$", ""))


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


def digits(n, k=None):
    k = k or nlen(n)
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals):
    return [v for v in vals if v is not None and v > 0]


# ------------------------------------------------------------ picture: split strategy
def parts(n):
    d = digits(n)
    return [d[i] * 10 ** i for i in reversed(range(len(d))) if d[i]]


def split_svg(a, b, op):
    """Both numbers on top, each split into place-value parts underneath."""
    S, m, gap = 58, 10, 40
    pa, pb = parts(a), parts(b)
    gwa, gwb = (len(pa) - 1) * S + 52, (len(pb) - 1) * S + 52
    cxa = m + gwa / 2.0
    cxb = m + gwa + gap + gwb / 2.0
    W = int(m + gwa + gap + gwb + m)
    H = 84
    s = [text(cxa, 24, f(a), 22), text(cxb, 24, f(b), 22),
         text((cxa + cxb) / 2.0, 24, "+" if op == "+" else "−", 22, col=GREEN)]
    for cx, ps in ((cxa, pa), (cxb, pb)):
        x0 = cx - (len(ps) - 1) * S / 2.0
        for k, p in enumerate(ps):
            px = x0 + k * S
            s.append("<line x1='%.1f' y1='32' x2='%.1f' y2='52' stroke='%s' stroke-width='2'/>" % (cx, px, GREEN))
            s.append("<rect x='%.1f' y='54' width='52' height='26' rx='5' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (px - 26, FILL, GREEN))
            s.append(text(px, 73, f(p), 15))
    lab = "split strategy: %s split into %s; %s split into %s" % (
        f(a), ", ".join(map(f, pa)), f(b), ", ".join(map(f, pb)))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ picture: open number line
def jw(j, lab_w):
    j = abs(j)
    w = 130 if j >= 1000 else 110 if j >= 100 else 84 if j >= 10 else 64
    return max(w, lab_w)


def nline_svg(start, jumps, ticks, jlabels=None, startlab=None):
    """Empty number line. Jumps go right for +, left for −. ticks: one label per point (None = no label)."""
    if jlabels is None:
        jlabels = [("+%s" % f(j)) if j > 0 else ("−%s" % f(-j)) for j in jumps]
    lw = max(len(t or "") for t in ticks) * 9 + 14
    m, ry, ly = 34, 24, 50
    ws = [jw(j, lw) for j in jumps]
    W = 2 * m + sum(ws)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j, w in zip(jumps, ws):
        xs.append(xs[-1] + (w if j > 0 else -w))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 22, ly, W - m + 22, ly, INK)]
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
    return svg_wrap(W, H, "".join(s), "open number line starting at %s with jumps of %s" % (
        startlab or f(start), ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


def column_svg(a, b, op, answer=False, marks=False, fs=28, fmt=None):
    """a over b in columns with the sign and a line. The space in a 5-digit number gets its own narrow slot.
    answer: also write the answer.  marks: red regrouping marks
    (+: the regrouped 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
    fmt = fmt or f                 # fd: a, b are tenths, written with a decimal point
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.3
    res = a + b if op == "+" else a - b
    rows = [fmt(a), fmt(b)] + ([fmt(res)] if answer else [])

    def xs(s):                     # x centre of every char, right-aligned
        out, x = [], 0.0
        for ch in reversed(s):
            w = kw if ch in (NB, ".") else cw
            out.append(x + w / 2)
            x += w
        return list(reversed(out)), x

    longest = max(xs(r)[1] for r in rows)
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks and op != "+" else 0)
    s = []

    def put(t, y, color):
        cx, _ = xs(t)
        for ch, x in zip(t, cx):
            if ch == NB:
                continue
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - x, y, fs, color, ch))

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    longrow = max(rows, key=lambda r: xs(r)[1])
    lx, _ = xs(longrow)
    place_x = [right - x for ch, x in zip(reversed(longrow), reversed(lx)) if ch not in (NB, ".")]
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
                         % (place_x[i + 1], yy, sm, RED))
            H = yy + 8
        else:
            nd = regroup_digits(a, b)
            od = digits(a, nlen(a))
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (fmt(a), "plus" if op == "+" else "minus", fmt(b))
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


def regroups_sub(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    n = 0
    for i in range(k):
        if d[i] < db[i]:
            n += 1
            d[i] += 10
            d[i + 1] -= 1
    return n


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
            ps.append("%s: %s = %d, write %d." % (P, expr, t, t))
            carry = 0
        elif t >= 10:
            ps.append("%s: %s = %d. Write %d and regroup 10 %s as 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%s</b>. Check with the inverse: %s − %s = %s." % (f(s), f(s), f(b), f(a)))


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
                zl = ["0 %s" % PLACE[m] for m in range(i + 1, j)]
                zeros = zl[0] if len(zl) == 1 else ", ".join(zl[:-1]) + " and " + zl[-1]
                chain = ", then ".join("1 %s as 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. There are %s, so regroup %s. Each 0 becomes 9. %d − %d = %d."
                       % (P, cur, db[i], zeros, chain, d[i], db[i], d[i] - db[i]))
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
            " Answer: <b>%s</b>. Check with the inverse: %s + %s = %s." % (f(r), f(r), f(b), f(a)))


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


def add_misalign(a, b):
    """Lined up the shorter number one place too far left."""
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
    """Did not regroup across the zero: took 1 straight from the next non-zero digit, left the zeros as 0,
    then took the smaller digit from the bigger one in those zero columns."""
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


def sub_misalign(a, b):
    if nlen(a) == nlen(b) or a - b * 10 <= 0:
        return None
    return a - b * 10


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_regroup(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b)] + every + add_extra_one(a, b) + [abs(a - b)])


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_forgot_reduce(a, b),
                  sub_misalign(a, b), a - b + 10, a - b - 10, a - b + 100, a + b])


# ------------------------------------------------------------ set 1: mental strategies
def split_cands(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    out = [add_no_regroup(a, b) if add_carry_cols(a, b) else None,   # dropped the regrouped ten
           a + b - (da[0] + db[0]),                                   # forgot the ones part
           a + b - 10 * (da[1] + db[1]),                              # forgot the tens part
           a + b - 100 * (da[2] + db[2]),                             # forgot the hundreds part
           a + b + 1000]
    return clean(out)


def split_e(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    head = "Split both numbers: %s and %s. " % (" + ".join(map(f, parts(a))), " + ".join(map(f, parts(b))))
    body = []
    tot = []
    for i in reversed(range(k)):
        x, y = da[i] * 10 ** i, db[i] * 10 ** i
        if x or y:
            body.append("%s: %s + %s = %s." % (cap(PLACE[i]), f(x), f(y), f(x + y)))
            tot.append(x + y)
    return head + " ".join(body) + " " + " + ".join(map(f, tot)) + " = <b>%s</b>." % f(a + b)




def set_mental():
    its = []
    # (a) add or take away thousands
    assert 5260 + 4000 == 9260 and 8473 - 5000 == 3473
    its.append(mcq("What is 5260 + 4000?", "9260", ["5660", "5300", "1260"],
                   "Only the thousands digit changes: 5 thousands + 4 thousands = 9 thousands. 5260 + 4000 = <b>9260</b>."))
    its.append(mcq("What is 8473 − 5000?", "3473", ["8423", "7973", f(8473 + 5000)],
                   "Only the thousands digit changes: 8 thousands − 5 thousands = 3 thousands. 8473 − 5000 = <b>3473</b>."))
    # (b) split strategy
    for a, b, pic in [(2143, 5326, True), (4512, 3264, False), (2758, 4136, True), (6327, 1548, False)]:
        assert a + b < 10000
        q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %s + %s?" % (f(a), f(b))
        its.append(mcq(q, f(a + b), [f(v) for v in split_cands(a, b)], split_e(a, b)))
    # (c) count on / back in jumps (in words)
    assert 2538 + 4251 == 6789
    its.append(mcq("Start at 2538. Count on 4000, then 200, then 50, then 1. Where do you land?", "6789",
                   ["6788", "6739", "2789"],
                   "2538 + 4000 = 6538. 6538 + 200 = 6738. 6738 + 50 = 6788. 6788 + 1 = <b>6789</b>. "
                   "This is 2538 + 4251 in jumps."))
    assert 9375 - 4236 == 5139 and sub_small_from_big(9375, 4236) == 5141
    its.append(mcq("Start at 9375. Count back 4000, then 200, then 30, then 6. Where do you land?", "5139",
                   ["5145", "5169", f(sub_small_from_big(9375, 4236))],
                   "9375 − 4000 = 5375. 5375 − 200 = 5175. 5175 − 30 = 5145. 5145 − 6 = <b>5139</b>. "
                   "This is 9375 − 4236 in jumps."))
    # (d) open number lines
    for a, js in [(3142, [5000, 300, 40]), (6829, [-3000, -500, -60, -2]), (8513, [-4000, -300, -20, -7])]:
        pts = [a]
        for j in js:
            pts.append(pts[-1] + j)
        r = pts[-1]
        ticks = [f(p) for p in pts[:-1]] + ["?"]
        steps = " ".join("%s %s %s = %s." % (f(pts[k]), "+" if j > 0 else "−", f(abs(j)), f(pts[k + 1]))
                         for k, j in enumerate(js))
        b = abs(sum(js))
        op = "+" if js[0] > 0 else "−"
        e = steps.rsplit(" = ", 1)[0] + " = <b>%s</b>. So %s %s %s = %s." % (f(r), f(a), op, f(b), f(r))
        wrong = ([r - js[-1], r + 100, r - 1000, add_no_regroup(a, b)] if op == "+"
                 else [r - js[-1], sub_small_from_big(a, b), r + 100, r - 1000])
        its.append(mcq(fig(nline_svg(a, js, ticks)) + "Where does the last jump land?", f(r), [f(v) for v in wrong], e))
    assert 2163 + 5430 == 7593
    its.append(mcq(fig(nline_svg(2163, [5000, 400, 30], ["2163", "7163", "7563", "7593"], ["?", "+400", "+30"])) +
                   "What is the missing jump?", "+5000", ["+500", "+50", "+5430"],
                   "From 2163 to 7163 the thousands digit goes up from 2 to 7, so the jump is <b>+5000</b>. "
                   "Check: 2163 + 5430 = 7593."))
    # (e) compensate
    for a, b, big in [(3718, 2999, 3000), (5264, 1998, 2000), (4387, 999, 1000)]:
        d = big - b
        r = a + b
        e = ("%s is %d less than %s. Add %s, then take away the extra %d. %s + %s = %s. %s − %d = <b>%s</b>."
             % (f(b), d, f(big), f(big), d, f(a), f(big), f(a + big), f(a + big), d, f(r)))
        its.append(mcq("Use compensation. %s is %d less than %s. What is %s + %s?" % (f(b), d, f(big), f(a), f(b)), f(r),
                       [f(v) for v in [a + big, a + big + d] + add_cands(a, b)], e))
    for a, b, big in [(8125, 2998, 3000), (6450, 1999, 2000), (7213, 999, 1000)]:
        d = big - b
        r = a - b
        e = ("%s is %d less than %s. Take away %s. You took away %d too many, so add %d back. "
             "%s − %s = %s. %s + %d = <b>%s</b>." % (f(b), d, f(big), f(big), d, d, f(a), f(big), f(a - big), f(a - big), d, f(r)))
        its.append(mcq("Use compensation. %s is %d less than %s. What is %s − %s?" % (f(b), d, f(big), f(a), f(b)), f(r),
                       [f(v) for v in [a - big, a - big - d] + sub_cands(a, b)], e))
    # (f) count on to find a small difference
    for a, b, js in [(6004, 5987, [13, 4]), (8020, 7975, [25, 20])]:
        d = a - b
        assert sum(js) == d and (b + js[0]) % 1000 == 0
        ticks = [f(b), f(b + js[0]), f(a)]
        e = ("The numbers are close, so count on from %s. %s + %d = %s, then %s + %d = %s. %d + %d = <b>%d</b>."
             % (f(b), f(b), js[0], f(b + js[0]), f(b + js[0]), js[1], f(a), js[0], js[1], d))
        its.append(mcq(fig(nline_svg(b, js, ticks)) + "Count on to find the difference. What is %s − %s?" % (f(a), f(b)),
                       f(d), [f(v) for v in clean([sub_zero_as_ten(a, b), sub_small_from_big(a, b), js[0], d + 10])], e))
    assert len(its) == 20, len(its)
    return {"title": "Mental math: compensate, split and count on", "items": its}


# ------------------------------------------------------------ set 2: column addition
LESSON_A = {(3769, 2485), (5236, 471)}
LESSON_S = {(5000, 1268), (7243, 3586)}


def item_add(a, b, col):
    q = (fig(column_svg(a, b, "+")) + "Add. Regroup when a column makes 10 or more.") if col else \
        "Use column addition. What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in add_cands(a, b)], add_steps(a, b))


def item_sub(a, b, col):
    q = (fig(column_svg(a, b, "-")) + "Subtract. Regroup when the top digit is smaller.") if col else \
        "Use column subtraction. What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in sub_cands(a, b)], sub_steps(a, b))


def pick_add(rnd, seen, la, lb, want, top):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if a + b > top or (a, b) in seen or (b, a) in seen or (a, b) in LESSON_A or a % 10 == 0 or b % 10 == 0:
            continue
        if len(add_carry_cols(a, b)) != want:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = ([(4, 4, 1, 9999)] * 3 + [(4, 3, 1, 9999)] + [(4, 2, 1, 9999)] * 2 + [(3, 3, 3, 1999)] * 2 +
            [(4, 4, 2, 9999)] * 3 + [(4, 3, 2, 9999)] * 2 + [(4, 4, 3, 9999)] * 4 + [(4, 3, 3, 9999)] * 2)
    for i, (la, lb, want, top) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, want, top)
        its.append(item_add(a, b, i % 3 != 2))
    its.append(item_add(4386, 5614, True))            # regroup in every column: exactly 10 000
    assert 4386 + 5614 == 10000
    assert len(its) == 20
    return {"title": "Column addition with regrouping", "items": its}


# ------------------------------------------------------------ set 3: column subtraction
def pick_sub(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 2, 10 ** la - 1)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 10, min(10 ** lb - 1, a - 10 ** (la - 1) // 4))
        if (a, b) in seen or (a, b) in LESSON_S or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if regroups_sub(a, b) == want:
            seen.add((a, b))
            return a, b


def set_sub(rnd, seen):
    its = []
    plan = [(4, 4, 1)] * 2 + [(4, 3, 1)] + [(4, 2, 1)] + [(4, 4, 2)] * 2 + [(4, 3, 2)] + [(4, 4, 3)] * 3
    for i, (la, lb, want) in enumerate(plan):
        a, b = pick_sub(rnd, seen, la, lb, want)
        its.append(item_sub(a, b, i % 3 != 2))
    # across zeros
    tops = {5000, 7243}                               # lesson examples
    pats = [("x00x", 4), ("x0xx", 4), ("x00x", 3), ("x000", 4), ("xx0x", 3),
            ("x0xx", 4), ("x000", 4), ("x00x", 4), ("x000", 4), ("10000", 4)]
    for n, (p, lb) in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - 10 ** (len(p) - 1) // 5)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or regroups_sub(a, b) < 2:
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, n % 3 != 2))
            break
    assert len(its) == 20
    return {"title": "Column subtraction with regrouping, including across zeros", "items": its}


# ------------------------------------------------------------ set 4: decimal tenths
# Decimals are worked as whole numbers of tenths: 4.6 is 46 tenths.
def fd(t):
    """Tenths to a decimal: 46 -> 4.6, 80 -> 8.0."""
    return "%d.%d" % divmod(t, 10)


def fw(t):
    """Like fd, but a whole number is written without .0 (80 -> 8)."""
    return str(t // 10) if t % 10 == 0 else fd(t)


def dec_check(t, a, b, op):
    from decimal import Decimal
    da, db = Decimal(fw(a)), Decimal(fw(b))
    assert Decimal(fw(t)) == (da + db if op == "+" else da - db), (t, a, b, op)


def thirteen_tenths(a, b):
    """Wrote the tenths total as it is (6 + 7 = 13 tenths written as .13): 4.6 + 2.7 = 6.13."""
    ta, tb = a % 10, b % 10
    if ta + tb < 10:
        return None
    return "%d.%d" % (a // 10 + b // 10, ta + tb)


def dec_add_cands(a, b):
    out = [thirteen_tenths(a, b)]
    out += [fd(v) for v in clean([add_no_regroup(a, b) if add_carry_cols(a, b) else None,
                                  a + b + 10, a + b - 10, abs(a - b), a + b + 1])]
    return [c for c in out if c]


def dec_sub_cands(a, b):
    return [fd(v) for v in clean([sub_small_from_big(a, b), sub_forgot_reduce(a, b), sub_zero_as_ten(a, b),
                                  a - b + 10, a - b - 10, a + b, a - b + 1])]


def bring_down(a, b):
    """Whole number minus a decimal: subtracted the wholes and brought the tenths down (8 − 2.7 = 6.7)."""
    return fd((a // 10 - b // 10) * 10 + b % 10)


def dec_add_e(a, b):
    ta, tb = a % 10, b % 10
    wa, wb = a // 10, b // 10
    s = "Line up the decimal points. "
    if ta + tb >= 10:
        s += ("Tenths: %d + %d = %d tenths. 10 tenths make 1 whole, so write %d and regroup 1 whole. "
              "Wholes: %d + %d + 1 = %d. " % (ta, tb, ta + tb, ta + tb - 10, wa, wb, wa + wb + 1))
    else:
        s += "Tenths: %d + %d = %d. Wholes: %d + %d = %d. " % (ta, tb, ta + tb, wa, wb, wa + wb)
    return s + "%s + %s = <b>%s</b>." % (fw(a), fw(b), fd(a + b))


def dec_sub_e(a, b):
    ta, tb = a % 10, b % 10
    wa, wb = a // 10, b // 10
    s = "Line up the decimal points. "
    if a % 10 == 0 and b % 10:
        s += "Write %s as %s. " % (fw(a), fd(a))
    if ta < tb:
        s += ("Tenths: %d − %d. Regroup 1 whole as 10 tenths: %d − %d = %d. Wholes: %d − %d = %d. "
              % (ta, tb, ta + 10, tb, ta + 10 - tb, wa - 1, wb, wa - 1 - wb))
    else:
        s += "Tenths: %d − %d = %d. Wholes: %d − %d = %d. " % (ta, tb, ta - tb, wa, wb, wa - wb)
    return s + "%s − %s = <b>%s</b>. Check: %s + %s = %s." % (fw(a), fw(b), fd(a - b), fd(a - b), fw(b), fw(a))


def item_dadd(a, b, col):
    q = (fig(column_svg(a, b, "+", fmt=fd)) + "Add. Line up the decimal points.") if col else \
        "What is %s + %s?" % (fw(a), fw(b))
    dec_check(a + b, a, b, "+")
    return mcq(q, fd(a + b), dec_add_cands(a, b), dec_add_e(a, b))


def item_dsub(a, b, col):
    q = (fig(column_svg(a, b, "-", fmt=fd)) + "Subtract. Line up the decimal points.") if col else \
        "What is %s − %s?" % (fw(a), fw(b))
    dec_check(a - b, a, b, "−")
    cands = dec_sub_cands(a, b)
    if a % 10 == 0:
        cands = [bring_down(a, b)] + cands
    return mcq(q, fd(a - b), cands, dec_sub_e(a, b))


def set_dec():
    its = [
        item_dadd(32, 45, False),       # 3.2 + 4.5, no regrouping
        item_dsub(68, 23, True),        # 6.8 − 2.3
        item_dadd(51, 36, True),        # 5.1 + 3.6
        item_dsub(97, 45, False),       # 9.7 − 4.5
        item_dadd(38, 54, True),        # 3.8 + 5.4, 10 tenths make 1 whole
        item_dadd(65, 29, False),       # 6.5 + 2.9
        item_dadd(76, 48, True),        # 7.6 + 4.8
        item_dadd(157, 65, True),       # 15.7 + 6.5
        item_dadd(284, 139, False),     # 28.4 + 13.9
        item_dsub(52, 27, True),        # 5.2 − 2.7
        item_dsub(91, 46, False),       # 9.1 − 4.6
        item_dsub(123, 58, True),       # 12.3 − 5.8
        item_dsub(304, 127, True),      # 30.4 − 12.7, across a zero
        item_dsub(412, 189, False),     # 41.2 − 18.9
        item_dsub(80, 27, False),       # 8 − 2.7
        item_dsub(100, 36, False),      # 10 − 3.6
    ]
    # whole number + decimal: line up the decimal points, not the right-hand digits
    a, b = 120, 46
    dec_check(a + b, a, b, "+")
    its.append(mcq("What is 12 + 4.6?", fd(a + b), [fd(12 + 46)] + dec_add_cands(a, b),
                   "12 is 12.0. Line up the decimal points: 12.0 + 4.6. Tenths: 0 + 6 = 6. Wholes: 12 + 4 = 16. "
                   "12 + 4.6 = <b>16.6</b>. (5.8 comes from lining up the 2 under the 6, as if 12 were 1.2.)"))
    # number line in tenths
    nl = nline_svg(37, [3, 2], ["3.7", "4", "?"], ["+0.3", "+0.2"], startlab="3.7")
    dec_check(42, 37, 5, "+")
    its.append(mcq(fig(nl) + "Use the number line. What is 3.7 + 0.5?", "4.2", ["3.12", "8.7", "4"],
                   "Split 0.5 into 0.3 and 0.2. 3.7 + 0.3 = 4. 4 + 0.2 = <b>4.2</b>. "
                   "(3.12 comes from writing 7 + 5 = 12 tenths as .12. 12 tenths is 1 whole and 2 tenths.)"))
    # missing number
    s, b = 61, 25
    x = s - b
    dec_check(x, s, b, "−")
    its.append(mcq("What number goes in the box?  <b>☐ + 2.5 = 6.1</b>", fd(x),
                   [fd(v) for v in clean([s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b), x + 10])],
                   "Use the inverse: 6.1 − 2.5. Tenths: 1 − 5, so regroup 1 whole as 10 tenths: 11 − 5 = 6. "
                   "Wholes: 5 − 2 = 3. The box is <b>3.6</b>. Check: 3.6 + 2.5 = 6.1."))
    # which number is lined up correctly?
    a, b = 254, 37
    dec_check(a + b, a, b, "+")
    its.append(mcq("What is 25.4 + 3.7?", fd(a + b), [fd(254 + 370)] + dec_add_cands(a, b),
                   "Line up the decimal points: 25.4 + 3.7. Tenths: 4 + 7 = 11 tenths. Write 1 and regroup 1 whole. "
                   "Wholes: 25 + 3 + 1 = 29. 25.4 + 3.7 = <b>29.1</b>. "
                   "(62.4 comes from lining up 3.7 under 25 as if it were 37.)"))
    assert len(its) == 20, len(its)
    return {"title": "Adding and subtracting decimal tenths", "items": its}


# ------------------------------------------------------------ set 5: word problems
def unit(v, u):
    return "$" + f(v) if u == "$" else "%s %s" % (f(v), u)


def eu(v, u):
    return "$" + f(v) if u == "$" else f(v)


def story(q, ans, cands, u, e):
    assert ans <= 10000
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e)


def one_add(q, a, b, u, lead):
    s = a + b
    e = lead + " %s + %s = <b>%s</b>. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
    return story(q, s, add_cands(a, b), u, e)


def one_sub(q, a, b, u, lead):
    r = a - b
    e = lead + " %s − %s = <b>%s</b>. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
    return story(q, r, sub_cands(a, b), u, e)


def start_add(q, now, more, u):
    x = now - more
    e = ("Work backwards. Take away what was added: %s − %s = <b>%s</b>. Check: %s + %s = %s."
         % (eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
    return story(q, x, [now + more] + sub_cands(now, more), u, e)


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
    e = "Step 1, %s: %s − %s = %s. Step 2, %s: %s + %s = <b>%s</b>." % (
        s1, eu(A, u), eu(B, u), eu(m, u), s2, eu(m, u), eu(C, u), eu(r, u))
    return story(q, r, [m, A - B - C, sub_small_from_big(A, B) + C, add_forgot_one(m, C, "last"), A + B + C], u, e)


def more_total(q, A, B, u, who2):
    """A + (A + B)."""
    m = A + B
    r = A + m
    e = ("Step 1, %s: %s + %s = %s. Step 2, both together: %s + %s = <b>%s</b>."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B + B, add_forgot_one(A, m, "last"), A + A], u, e)


def less_total(q, A, B, u, who2):
    """A + (A − B)."""
    m = A - B
    r = A + m
    e = ("Step 1, %s: %s − %s = %s. Step 2, both together: %s + %s = <b>%s</b>."
         % (who2, eu(A, u), eu(B, u), eu(m, u), eu(A, u), eu(m, u), eu(r, u)))
    return story(q, r, [m, A + B, A + A + B, add_forgot_one(A, m, "last")], u, e)


def combine_compare(q, B, C, D, u, s1):
    """|(B + C) − D|."""
    t = B + C
    r = abs(t - D)
    big, small = max(t, D), min(t, D)
    e = ("Step 1, %s: %s + %s = %s. Step 2, find the difference: %s − %s = <b>%s</b>."
         % (s1, eu(B, u), eu(C, u), eu(t, u), eu(big, u), eu(small, u), eu(r, u)))
    return story(q, r, [t, sub_small_from_big(big, small), t + D, sub_zero_as_ten(big, small), abs(B - D)], u, e)


def dstory(q, ans, cands, u, e):
    """Decimal word problem. ans in tenths, cands are decimal strings."""
    return mcq(q, "%s %s" % (fd(ans), u), ["%s %s" % (c, u) for c in cands if c], e)


def set_story(P):
    n = [P.next() for _ in range(7)]
    its = [
        one_add("The Patel family drove 1786 km on a summer road trip from Toronto to Halifax. On the way home they took "
                "a different road and drove 1849 km. How far did they drive altogether?", 1786, 1849, "km",
                "Put the two parts of the trip together, so add."),
        one_add("Our school’s Terry Fox Run raised $2736. The spring fun fair raised $1895. "
                "How much did the two events raise altogether?", 2736, 1895, "$", "Altogether means add."),
        one_add("A tour bus drove 3678 km in May and 2945 km in June. How far did it drive in the two months?",
                3678, 2945, "km", "Put the two months together, so add."),
        one_sub("The Nguyen family’s road trip from Toronto to Vancouver is 4420 km long. They have driven 2675 km so far. "
                "How many kilometres are left?", 4420, 2675, "km", "Find the distance left, so subtract."),
        one_sub("The school council wants to raise $8000 for a new playground. So far it has raised $5347. "
                "How much more does it need?", 8000, 5347, "$", "Find what is still needed, so subtract."),
        one_sub("The school read-a-thon goal is " + TEN_K + " minutes of reading. Students have read 6852 minutes so far. "
                "How many more minutes do they need to read?", 10000, 6852, "minutes", "Find what is still to come, so subtract."),
        one_sub("A museum in Ottawa had 6214 visitors on Saturday and 3785 visitors on Monday. "
                "How many more visitors came on Saturday?", 6214, 3785, "visitors",
                "How many more means find the difference, so subtract."),
        start_add("A Grade 4 class had some money in its field trip fund. A bake sale added $1375. Now the fund has $3020. "
                  "How much was in the fund before the bake sale?", 3020, 1375, "$"),
        more_total("A school collected 2465 cans of food for the food bank in October. In November it collected 1758 more "
                   "cans than in October. How many cans did it collect in the two months?", 2465, 1758, "cans",
                   "November’s cans"),
        both_left("The Okafor family planned a 5000 km road trip around Ontario and Quebec. They drove 1876 km in week 1 "
                  "and 1659 km in week 2. How many kilometres are left?", 5000, 1876, 1659, "km",
                  "kilometres driven", "kilometres left"),
        less_total("A tour bus drove 3426 km on trips to Niagara Falls in June. In July it drove 968 km less. "
                   "How far did it drive in the two months?", 3426, 968, "km", "July"),
        combine_compare("%s’s family drove 1487 km to get to Thunder Bay, then 869 km on day trips. %s’s family drove "
                        "3000 km on their summer holiday. How many more kilometres did %s’s family drive?"
                        % (n[0][0], n[1][0], n[1][0]), 1487, 869, 3000, "km", "%s’s family" % n[0][0]),
        both_left("The school wants to raise $" + TEN_K + " for new library books. The fall fun fair raised $3957 "
                  "and the spring carnival raised $2864. How much more does the school need?", 10000, 3957, 2864, "$",
                  "money raised", "money still needed"),
        out_then_in("The school had $5436 in its field trip fund. It spent $2867 on buses for a trip to Ottawa. Then a "
                    "bake sale raised $1385. How much money is in the fund now?", 5436, 2867, 1385, "$", "after spending",
                    "after the bake sale"),
        more_total("%s’s class raised $1268 at a pizza lunch fundraiser. %s’s class raised $475 more. "
                   "How much did the two classes raise altogether?" % (n[2][0], n[3][0]), 1268, 475, "$",
                   "%s’s class" % n[3][0]),
        both_left("The Terry Fox Run had 4000 bottles of water. Runners took 1875 bottles in the morning and 1468 "
                  "at lunch. How many bottles were left?", 4000, 1875, 1468, "bottles", "bottles taken", "bottles left"),
        out_then_in("A food bank in Hamilton had 5073 cans of food. It gave out 2896 cans. Then a school food drive brought in "
                    "1749 cans. How many cans does the food bank have now?", 5073, 2896, 1749, "cans", "after giving out",
                    "after the food drive"),
    ]
    # decimal tenths
    nm, he, his = n[4]
    a, b = 58, 36
    dec_check(a + b, a, b, "+")
    its.append(dstory("On a canoe trip in Algonquin Park, %s’s group paddled 5.8 km in the morning and 3.6 km in the "
                      "afternoon. How far did they paddle that day?" % nm, a + b, dec_add_cands(a, b), "km",
                      "Put the morning and the afternoon together, so add. " + dec_add_e(a, b)))
    a, b = 124, 78
    dec_check(a - b, a, b, "−")
    its.append(dstory("A hiking trail is 12.4 km long. %s’s family has hiked 7.8 km. How much farther do they have to go?"
                      % n[5][0], a - b, dec_sub_cands(a, b), "km", "Find the distance left, so subtract. " + dec_sub_e(a, b)))
    A, B, C = 50, 25, 18
    t = B + C
    dec_check(t, B, C, "+")
    dec_check(A - t, A, t, "−")
    assert (bring_down(A, t), fd(sub_forgot_reduce(A, t))) == ("1.3", "1.7")
    its.append(dstory("%s bought 2.5 kg of apples and 1.8 kg of pears at the farmers’ market. %s bag can hold 5 kg. "
                      "How many more kilograms can the bag hold?" % (n[6][0], cap(n[6][2])), A - t,
                      [fd(t), bring_down(A, t), fd(sub_forgot_reduce(A, t)), fd(A + t)], "kg",
                      "Step 1, the fruit: 2.5 + 1.8 = 4.3 kg (5 + 8 = 13 tenths, so write 3 and regroup 1 whole). "
                      "Step 2, the space left: write 5 as 5.0. 5.0 − 4.3 = <b>0.7 kg</b>. Check: 0.7 + 4.3 = 5.0."))
    assert len(its) == 20
    return {"title": "Word problems: road trips and fundraisers", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 4628 + 2999 == 7627 and 3769 + 2485 == 6254 and 5000 - 1268 == 3732 and 7243 - 3586 == 3657
    assert 2413 + 5264 == 7677 and 7012 - 6985 == 27
    assert add_no_regroup(3769, 2485) == 5144
    assert sub_small_from_big(7243, 3586) == 4343
    assert sub_zero_as_ten(5000, 1268) == 3842, sub_zero_as_ten(5000, 1268)
    assert add_misalign(5236, 471) == 9946 and 5236 + 471 == 5707
    assert rnd_to(3769, 1000) + rnd_to(2485, 1000) == 6000
    assert thirteen_tenths(46, 27) == "6.13" and fd(46 + 27) == "7.3" and fd(62 - 35) == "2.7" and fd(12 + 46) == "5.8"
    return (
        "<h2>The idea: use place value</h2>"
        "<p>Numbers to " + TEN_K + " are made of thousands, hundreds, tens and ones. "
        "Add or subtract the same places. When a place gets 10 or more, <b>regroup</b>: 10 ones make 1 ten, "
        "10 tens make 1 hundred, and 10 hundreds make 1 thousand. With decimals, <b>10 tenths make 1 whole</b>.</p>"
        "<p>First ask: can I do this in my head? If not, use the column method.</p>"
        "<h2>Mental math</h2>"
        "<p><b>Split:</b> break both numbers into thousands, hundreds, tens and ones. Add each place, then put the parts back together.</p>"
        "<figure class='sn-fig'>" + split_svg(2413, 5264, "+") +
        "<figcaption>2000 + 5000 = 7000, 400 + 200 = 600, 10 + 60 = 70, 3 + 4 = 7. Answer: 7677.</figcaption></figure>" +
        ex("Compensate", "What is 4628 + 2999?",
           "2999 is 1 less than 3000. Add 3000: 4628 + 3000 = 7628. You added 1 too many, so take 1 away: 7627.", "7627") +
        "<p><b>Count on:</b> when two numbers are close, count up from the smaller one to find the difference.</p>"
        "<figure class='sn-fig'>" + nline_svg(6985, [15, 12], ["6985", "7000", "7012"]) +
        "<figcaption>7012 − 6985: from 6985 to 7000 is 15. From 7000 to 7012 is 12. 15 + 12 = 27.</figcaption></figure>"
        "<h2>Column addition</h2>"
        "<p>Put <b>ones under ones</b>, tens under tens, and so on. Start on the right. "
        "If a column makes 10 or more, write the ones digit and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(3769, 2485, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 9 + 5 = 14, write 4, regroup 1. Tens: 6 + 8 + 1 = 15, write 5, regroup 1. "
        "Hundreds: 7 + 4 + 1 = 12, write 2, regroup 1. Thousands: 3 + 2 + 1 = 6. Answer: 6254.</figcaption></figure>"
        "<p>Estimate first to see if your answer makes sense: 4000 + 2000 = 6000, and 6254 is close.</p>"
        "<h2>Column subtraction, including across zeros</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, regroup 1 from the next column. "
        "If the next column is 0, go left to the first digit that is not 0. Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(5000, 1268, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 0 − 8. There are 0 tens and 0 hundreds, so regroup 1 thousand as 10 hundreds, 1 hundred as 10 tens "
        "and 1 ten as 10 ones. 5000 becomes 4 thousands, 9 hundreds, 9 tens and 10 ones. "
        "10 − 8 = 2, 9 − 6 = 3, 9 − 2 = 7, 4 − 1 = 3. Answer: 3732.</figcaption></figure>"
        "<p>Check with the inverse: 3732 + 1268 = 5000. You get back to the start, so the answer is right.</p>"
        "<h2>Adding and subtracting decimal tenths</h2>"
        "<p>Line up the <b>decimal points</b>, so tenths are under tenths. Then add or subtract just like whole numbers. "
        "Put the decimal point in the answer right under the others.</p>"
        "<figure class='sn-fig'>" + column_svg(46, 27, "+", answer=True, marks=True, fs=34, fmt=fd) +
        "<figcaption>Tenths: 6 + 7 = 13 tenths. 10 tenths make 1 whole, so write 3 and regroup 1. "
        "Wholes: 4 + 2 + 1 = 7. Answer: 7.3.</figcaption></figure>" +
        ex("Subtract tenths", "What is 6.2 − 3.5?",
           "Tenths: 2 − 5. Regroup 1 whole as 10 tenths: 12 − 5 = 7. Wholes: 5 − 3 = 2. Check: 2.7 + 3.5 = 6.2.", "2.7") +
        "<p>For a whole number, write <b>.0</b>: 8 − 2.7 is 8.0 − 2.7 = 5.3.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not regrouping (3769 + 2485 = 5144)", "Write the regrouped 1 under the next column and add it in"],
            ["Taking the smaller digit from the larger one (7243 − 3586 = 4343)",
             "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Making each 0 into 10 instead of 9 (5000 − 1268 = 3842)", "Only the last place gets 10. Each 0 you pass gives 1 away, so it becomes 9"],
            ["Lining up the numbers on the left (5236 + 471 = 9946)", "Line up the ones on the right: 5236 + 471 = 5707"],
            ["Writing 13 tenths as .13 (4.6 + 2.7 = 6.13)", "10 tenths make 1 whole: 4.6 + 2.7 = 7.3"],
            ["Not lining up the decimal points (12 + 4.6 = 5.8)", "Write 12 as 12.0 and line up the points: 12.0 + 4.6 = 16.6"],
        ])
    )


def rnd_to(n, p):
    return (n + p // 2) // p * p


FAQ = [
    {"q": "What does Grade 4 learn about adding and subtracting in the Ontario math curriculum?",
     "a": "Students add and subtract whole numbers that add up to no more than 10 000, and decimal tenths. They use mental "
          "math, tools like number lines, and algorithms such as the column method to solve problems."},
    {"q": "How do you subtract across zeros, like 5000 − 1268?",
     "a": "Go left to the first digit that is not 0 and regroup from there; each 0 you pass becomes 9. 5000 becomes 4 thousands, "
          "9 hundreds, 9 tens and 10 ones, so 5000 − 1268 = 3732."},
    {"q": "How do you add and subtract decimals in Grade 4?",
     "a": "Line up the decimal points and work like whole numbers, remembering that 10 tenths make 1 whole. For example, "
          "4.6 + 2.7 = 7.3, and 8 − 2.7 is worked as 8.0 − 2.7 = 5.3."},
    {"q": "What mental math strategies help with adding and subtracting big numbers?",
     "a": "Compensation (for 4628 + 2999, add 3000 and take 1 away), splitting numbers by place value, and counting on "
          "along a number line to find a difference. Estimating first helps catch mistakes."},
]


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    from decimal import Decimal
    N = r"(\d+(?:" + NB + r"\d{3})*)"
    D = r"(\d+(?:\.\d)?)"
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='" + N + " (plus|minus) " + N + " written in columns'", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"aria-label='(\d+\.\d) (plus|minus) (\d+\.\d) written in columns'", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"What is " + N + " ([+−]) " + N + r"\?$", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"What is " + D + " ([+−]) " + D + r"\?$", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "+" else a - b), it["q"]


def gen():
    rnd = random.Random(44804)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_mental(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_dec(), set_story(P)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "adding-and-subtracting-to-10000", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to " + TEN_K,
        "seo_title": "Grade 4 Adding and Subtracting to " + TEN_K + " Worksheets: Regrouping and Decimals (Ontario)",
        "short_title": "Adding and subtracting to " + TEN_K,
        "domain": "Number",
        "standard_code": "Grade 4: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the addition and subtraction of whole numbers that add up "
                         "to no more than 10 000 and of decimal tenths, using appropriate tools, strategies, and algorithms",
        "meta_desc": "Free Grade 4 math worksheets on adding and subtracting to " + TEN_K + " and decimal tenths, matched to "
                     "the Ontario curriculum: mental math, column addition and subtraction with regrouping, subtracting "
                     "across zeros and word problems. 100 questions with an answer key.",
        "key_big": "Line up the places (and the decimal points). Regroup when you need to.",
        "key_sub": "Try mental math first: compensate, split or count on. In columns, start on the right; every 0 you "
                   "regroup across becomes 9. With decimals, 10 tenths make 1 whole, so 4.6 + 2.7 = 7.3.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "open number line|split strategy")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
