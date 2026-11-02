# -*- coding: utf-8 -*-
"""
CA-BC Grade 4 Math: Adding and subtracting to 10 000 (BC Mathematics Curriculum, Computational fluency)
  python3 tools/gen_cabc_math_g4_add_sub.py
Mental strategies (compensate, split, count on), column addition and subtraction with regrouping
(also across zeros, like 5000 − 1268), estimating and checking with the inverse, BC word problems.
Canadian English. 4-digit numbers have no separator (4536); 10 000 uses a no-break space.
Every answer and every wrong answer is computed in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are copied from gen_au_maths_y4_add_sub.py (same column method, rewritten for BC).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
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


def nline_svg(start, jumps, ticks, jlabels=None):
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
        f(start), ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line. The space in a 5-digit number gets its own narrow slot.
    answer: also write the answer.  marks: red regrouping marks
    (+: the regrouped 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.3
    res = a + b if op == "+" else a - b
    rows = [f(a), f(b)] + ([f(res)] if answer else [])

    def xs(s):                     # x centre of every char, right-aligned
        out, x = [], 0.0
        for ch in reversed(s):
            w = kw if ch == NB else cw
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
    place_x = [right - x for ch, x in zip(reversed(longrow), reversed(lx)) if ch != NB]
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
            od = digits(a)
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (f(a), "plus" if op == "+" else "minus", f(b))
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
    its.append(mcq("What is 4350 + 3000?", "7350", ["4650", "4380", "7650"],
                   "Only the thousands digit changes: 4 thousands + 3 thousands = 7 thousands. 4350 + 3000 = <b>7350</b>."))
    its.append(mcq("What is 9625 − 2000?", "7625", ["9605", "9425", "7425"],
                   "Only the thousands digit changes: 9 thousands − 2 thousands = 7 thousands. 9625 − 2000 = <b>7625</b>."))
    assert 4350 + 3000 == 7350 and 9625 - 2000 == 7625
    # (b) split strategy
    for a, b, pic in [(3214, 4562, True), (2635, 5142, False), (3467, 2318, True), (5284, 1653, False)]:
        assert a + b < 10000
        q = (fig(split_svg(a, b, "+")) if pic else "") + "Use the split strategy. What is %s + %s?" % (f(a), f(b))
        its.append(mcq(q, f(a + b), [f(v) for v in split_cands(a, b)], split_e(a, b)))
    # (c) count on in jumps (in words)
    its.append(mcq("Start at 3465. Count on 2000, then 300, then 20, then 4. Where do you land?", "5789",
                   ["5785", "5769", "3789"],
                   "3465 + 2000 = 5465. 5465 + 300 = 5765. 5765 + 20 = 5785. 5785 + 4 = <b>5789</b>. "
                   "This is 3465 + 2324 in jumps."))
    assert 3465 + 2324 == 5789
    its.append(mcq("Start at 8642. Count back 3000, then 400, then 10, then 5. Where do you land?", "5227",
                   ["5232", "5237", f(sub_small_from_big(8642, 3415))],
                   "8642 − 3000 = 5642. 5642 − 400 = 5242. 5242 − 10 = 5232. 5232 − 5 = <b>5227</b>. "
                   "This is 8642 − 3415 in jumps."))
    assert 8642 - 3415 == 5227
    # (d) open number lines
    for a, js in [(2356, [4000, 500, 30]), (5718, [-2000, -600, -40, -3]), (9264, [-3000, -200, -50, -6])]:
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
    its.append(mcq(fig(nline_svg(4275, [3000, 600, 20], ["4275", "7275", "7875", "7895"], ["?", "+600", "+20"])) +
                   "What is the missing jump?", "+3000", ["+300", "+30", "+3620"],
                   "From 4275 to 7275 the thousands digit goes up from 4 to 7, so the jump is <b>+3000</b>. "
                   "Check: 4275 + 3620 = 7895."))
    assert 4275 + 3620 == 7895
    # (e) compensate
    for a, b, big in [(4625, 2999, 3000), (3478, 1998, 2000), (5246, 999, 1000)]:
        d = big - b
        r = a + b
        e = ("%s is %d less than %s. Add %s, then take away the extra %d. %s + %s = %s. %s − %d = <b>%s</b>."
             % (f(b), d, f(big), f(big), d, f(a), f(big), f(a + big), f(a + big), d, f(r)))
        its.append(mcq("Use compensation. %s is %d less than %s. What is %s + %s?" % (f(b), d, f(big), f(a), f(b)), f(r),
                       [f(v) for v in [a + big, a + big + d] + add_cands(a, b)], e))
    for a, b, big in [(7340, 1998, 2000), (8215, 2999, 3000), (6132, 999, 1000)]:
        d = big - b
        r = a - b
        e = ("%s is %d less than %s. Take away %s. You took away %d too many, so add %d back. "
             "%s − %s = %s. %s + %d = <b>%s</b>." % (f(b), d, f(big), f(big), d, d, f(a), f(big), f(a - big), f(a - big), d, f(r)))
        its.append(mcq("Use compensation. %s is %d less than %s. What is %s − %s?" % (f(b), d, f(big), f(a), f(b)), f(r),
                       [f(v) for v in [a - big, a - big - d] + sub_cands(a, b)], e))
    # (f) count on to find a small difference
    for a, b, js in [(5003, 4986, [14, 3]), (7010, 6985, [15, 10])]:
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
LESSON_A = {(4678, 2856), (4567, 382), (3765, 2847)}
LESSON_S = {(5000, 1268), (6152, 2879)}


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
    its.append(item_add(6475, 3525, True))            # regroup in every column: exactly 10 000
    assert 6475 + 3525 == 10000
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
    tops = {5000, 6152}                               # lesson examples
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


# ------------------------------------------------------------ set 4: estimate, then check with the inverse
def rnd_to(n, p):
    return (n + p // 2) // p * p


def down_to(n, p):
    return n // p * p


def set_check(P):
    its = []
    # (a) estimate by rounding
    a, b = 3874, 2156
    assert (rnd_to(a, 1000), rnd_to(b, 1000), a + b) == (4000, 2000, 6030)
    its.append(mcq("Round each number to the nearest thousand to estimate 3874 + 2156.", "6000",
                   ["5000", "7000", "6030"],
                   "3874 rounds up to 4000. 2156 rounds down to 2000. 4000 + 2000 = <b>6000</b>. "
                   "(The exact answer is 6030, which is close.)"))
    a, b = 7215, 2689
    assert (rnd_to(a, 1000), rnd_to(b, 1000), a - b) == (7000, 3000, 4526)
    its.append(mcq("Round each number to the nearest thousand to estimate 7215 − 2689.", "4000",
                   ["5000", "4526", TEN_K],
                   "7215 rounds down to 7000. 2689 rounds up to 3000. 7000 − 3000 = <b>4000</b>. "
                   "(5000 comes from cutting 2689 down to 2000 instead of rounding it.)"))
    a, b = 2468, 1347
    assert (rnd_to(a, 100), rnd_to(b, 100), a + b, down_to(a, 100) + down_to(b, 100)) == (2500, 1300, 3815, 3700)
    its.append(mcq("Round each number to the nearest hundred to estimate 2468 + 1347.", "3800",
                   ["3700", "3815", "3000"],
                   "2468 rounds up to 2500. 1347 rounds down to 1300. 2500 + 1300 = <b>3800</b>. "
                   "(3700 comes from cutting 2468 down to 2400 instead of rounding it.)"))
    a, b = 6352, 2738
    assert (rnd_to(a, 100), rnd_to(b, 100), a - b) == (6400, 2700, 3614)
    assert down_to(a, 100) - down_to(b, 100) == 3600 and rnd_to(a, 1000) - rnd_to(b, 1000) == 3000
    its.append(mcq("Round each number to the nearest hundred to estimate 6352 − 2738.", "3700",
                   ["3600", "3614", "3000"],
                   "6352 rounds up to 6400. 2738 rounds down to 2700. 6400 − 2700 = <b>3700</b>."))
    assert 4985 + 2996 == 7981
    its.append(mcq("Which is the best estimate for 4985 + 2996?", "5000 + 3000 = 8000",
                   ["4000 + 2000 = 6000", "5000 + 2000 = 7000", "4900 + 2900 = 7800"],
                   "4985 is very close to 5000 and 2996 is very close to 3000. <b>5000 + 3000 = 8000</b>. "
                   "The exact answer is 7981."))
    n, he, his = P.next()
    assert add_no_regroup(3765, 2847) == 5502 and 3765 + 2847 == 6612
    its.append(mcq("%s worked out 3765 + 2847 = 5502. Estimate to the nearest thousand. Is %s answer reasonable?" % (n, his),
                   "No. The estimate is 7000", ["Yes. The estimate is 6000", "Yes. The estimate is 5000",
                                                "No. The estimate is 6000"],
                   "3765 rounds to 4000 and 2847 rounds to 3000. 4000 + 3000 = 7000. 5502 is far from 7000, "
                   "so <b>the answer is not reasonable</b>. (%s forgot to regroup. The exact answer is 6612.)" % n))
    n, he, his = P.next()
    assert 8203 - 3596 == 4607 and sub_small_from_big(8200, 3600) == 5400
    its.append(mcq("%s worked out 8203 − 3596 = 4607. Estimate to the nearest hundred. Is %s answer reasonable?" % (n, his),
                   "Yes. The estimate is 4600", ["No. The estimate is 5400", "No. The estimate is 11" + NB + "800",
                                                 "Yes. The estimate is 5400"],
                   "8203 rounds to 8200 and 3596 rounds to 3600. 8200 − 3600 = 4600. 4607 is very close to 4600, "
                   "so <b>the answer is reasonable</b>."))
    assert 3285 + 2940 == 6225 and rnd_to(3285, 100) + rnd_to(2940, 100) == 6200
    its.append(mcq("A class raised $3285 at a bottle drive and $2940 at a bake sale. "
                   "Round to the nearest hundred. About how much did the class raise?", "$6200",
                   ["$6100", "$6225", "$6000"],
                   "$3285 rounds to $3300. $2940 rounds to $2900. $3300 + $2900 = <b>$6200</b>. "
                   "(The exact total is $6225.)"))
    # (b) which calculation checks it?
    for a, b in [(7241, 3586), (8004, 3657)]:
        c = a - b
        its.append(mcq("Which calculation checks <b>%s − %s = %s</b>?" % (f(a), f(b), f(c)),
                       "%s + %s" % (f(c), f(b)),
                       ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)), "%s − %s" % (f(c), f(b)) if c > b else
                        "%s − %s" % (f(b), f(c))],
                       "Addition is the inverse of subtraction. Add the answer to the number you took away: "
                       "%s + %s = %s. You get back to the start, so the answer is right." % (f(c), f(b), f(a))))
    a, b = 3687, 2456
    s = a + b
    its.append(mcq("Which calculation checks <b>%s + %s = %s</b>?" % (f(a), f(b), f(s)),
                   "%s − %s" % (f(s), f(b)),
                   ["%s + %s" % (f(s), f(b)), "%s − %s" % (f(a), f(b)), "%s + %s" % (f(s), f(a))],
                   "Subtraction is the inverse of addition. Take one number away from the answer: "
                   "%s − %s = %s. You get the other number, so the answer is right." % (f(s), f(b), f(a))))
    a, b = 8436, 2758
    c = a - b
    its.append(mcq("%s − %s = %s. Which number sentence is also true?" % (f(a), f(b), f(c)),
                   "%s + %s = %s" % (f(c), f(b), f(a)),
                   ["%s − %s = %s" % (f(c), f(b), f(a)), "%s + %s = %s" % (f(a), f(b), f(c)),
                    "%s + %s = %s" % (f(a), f(c), f(b))],
                   "The three numbers make a fact family. The two smaller numbers add to make the biggest: "
                   "<b>%s + %s = %s</b>." % (f(c), f(b), f(a))))
    # (c) missing numbers
    miss = []
    x, b = 3729, 2486
    s = x + b
    miss.append(("<b>☐ + %s = %s</b>" % (f(b), f(s)), x, [s + b, sub_small_from_big(s, b), sub_forgot_reduce(s, b)],
                 "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(b), f(x), f(x), f(b), f(s))))
    a, s = 2648, 7003
    x = s - a
    miss.append(("<b>%s + ☐ = %s</b>" % (f(a), f(s)), x, [s + a, sub_small_from_big(s, a), sub_zero_as_ten(s, a)],
                 "Use the inverse: %s − %s = %s. Check: %s + %s = %s." % (f(s), f(a), f(x), f(a), f(x), f(s))))
    r, b = 4726, 1395
    x = r + b
    miss.append(("<b>☐ − %s = %s</b>" % (f(b), f(r)), x, [r - b, add_no_regroup(r, b), add_forgot_one(r, b, "first")],
                 "The box is the starting number, so use the inverse and add: %s + %s = %s. Check: %s − %s = %s."
                 % (f(r), f(b), f(x), f(x), f(b), f(r))))
    a, r = 8040, 3578
    x = a - r
    miss.append(("<b>%s − ☐ = %s</b>" % (f(a), f(r)), x, [a + r, sub_small_from_big(a, r), sub_zero_as_ten(a, r)],
                 "Think: %s take away what leaves %s? Work out %s − %s = %s. Check: %s − %s = %s."
                 % (f(a), f(r), f(a), f(r), f(x), f(a), f(x), f(r))))
    for q, x, wrong, e in miss:
        its.append(mcq("What number goes in the box?  " + q, f(x), [f(v) for v in clean(wrong)], e))
    # (d) did they get it right? check with the inverse
    YES = "Yes, it is correct"
    checks = [(6241, 2785, "−", sub_small_from_big(6241, 2785)),
              (4675, 2548, "+", add_no_regroup(4675, 2548)),
              (9004, 3627, "−", sub_zero_skip(9004, 3627)),
              (5368, 3874, "+", 5368 + 3874)]
    for a, b, op, got in checks:
        n, he, his = P.next()
        exact = a + b if op == "+" else a - b
        if op == "−":
            back = got + b
            chk = "%s + %s = %s" % (f(got), f(b), f(back))
        else:
            back = got - b
            chk = "%s − %s = %s" % (f(got), f(b), f(back))
        ok = back == a
        assert ok == (got == exact)
        if ok:
            ans = YES
            why = "The check gives %s, the number %s started with, so the answer is right." % (f(a), he)
            wrong = ["No, it should be %s" % f(v) for v in clean(
                [sub_small_from_big(a, b), sub_forgot_reduce(a, b), exact + 100] if op == "−"
                else [add_no_regroup(a, b), add_forgot_one(a, b, "last"), exact - 100])]
        else:
            ans = "No, it should be %s" % f(exact)
            why = ("The check gives %s, not %s, so the answer is wrong. The correct answer is <b>%s</b>."
                   % (f(back), f(a), f(exact)))
            wrong = [YES, "No, it should be %s" % f(back),
                     "No, it should be %s" % f(exact + 1000), "No, it should be %s" % f(exact - 10)]
        its.append(mcq("%s worked out %s %s %s = %s. Use the inverse to check. Is %s answer correct?"
                       % (n, f(a), op, f(b), f(got), his), ans, wrong,
                       "Check with the inverse: %s. " % chk + why))
    assert len(its) == 20, len(its)
    return {"title": "Estimate, then check with the inverse", "items": its}


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
    e = ("Work backwards. Take away the %s that were added: %s − %s = <b>%s</b>. Check: %s + %s = %s."
         % (f(more), eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
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


def set_story(P):
    n = [P.next() for _ in range(4)]
    its = [
        one_add("Volunteers counted salmon at a viewing spot on the Adams River. They counted 3486 sockeye on Monday "
                "and 4257 on Tuesday. How many sockeye did they count on the two days?", 3486, 4257, "sockeye",
                "Put the two days together, so add."),
        one_add("The Chen family drove 2468 km in July, including a trip to Kelowna. They drove 1795 km in August. "
                "How far did they drive in the two months?", 2468, 1795, "km", "Put the two months together, so add."),
        one_add("Our school’s Terry Fox Run raised $2385. The spring fun fair raised $1947. "
                "How much did the two events raise altogether?", 2385, 1947, "$", "Altogether means add."),
        one_sub("On the Adams River, 6215 sockeye were counted on Saturday and 3878 on Friday. "
                "How many more were counted on Saturday?", 6215, 3878, "sockeye",
                "How many more means find the difference, so subtract."),
        one_sub("Volunteers hope to count " + TEN_K + " salmon at the river this week. So far they have counted 7468. "
                "How many more salmon do they hope to count?", 10000, 7468, "salmon", "Find what is still to come, so subtract."),
        one_sub("The Martin family planned a 2000 km summer road trip to Kelowna and around the Okanagan. "
                "They have driven 1385 km. How many kilometres are left?", 2000, 1385, "km",
                "Find the distance left, so subtract."),
        one_sub("The PAC wants to raise $8000 for a new playground. So far it has raised $5476. How much more does it need?",
                8000, 5476, "$", "Find the difference, so subtract."),
        one_sub("Grouse Mountain had 4206 visitors on Saturday and 2758 visitors on Sunday. "
                "How many more visitors came on Saturday?", 4206, 2758, "visitors",
                "How many more means find the difference, so subtract."),
        start_add("Volunteers counted some salmon in the morning. They counted 2375 more in the afternoon. "
                  "The total for the day was 6012. How many salmon did they count in the morning?", 6012, 2375, "salmon"),
        more_total("On Friday, 2648 salmon were counted at the river. On Saturday, 1875 more were counted than on Friday. "
                   "How many salmon were counted on the two days?", 2648, 1875, "salmon", "Saturday’s count"),
        both_left("A hatchery on Vancouver Island raised 8000 coho salmon fry. It let 3465 go in one creek and 2780 in "
                  "another creek. How many fry are still at the hatchery?", 8000, 3465, 2780, "fry",
                  "fry let go", "fry still at the hatchery"),
        less_total("A tour bus drove 3264 km on trips to Kelowna in June. In July it drove 875 km less. "
                   "How far did it drive in the two months?", 3264, 875, "km", "July"),
        both_left("A truck driver plans to drive 5000 km this month, taking fruit from Kelowna. She drove 1648 km in "
                  "week 1 and 1875 km in week 2. How many kilometres are left?", 5000, 1648, 1875, "km",
                  "kilometres driven", "kilometres left"),
        combine_compare("%s’s family drove 1386 km to Kelowna and back, then 958 km on day trips. %s’s family drove "
                        "3000 km on their holiday. How many more kilometres did %s’s family drive?"
                        % (n[0][0], n[1][0], n[1][0]), 1386, 958, 3000, "km", "%s’s family" % n[0][0]),
        both_left("The school wants to raise " + "$" + TEN_K + " for new library books. The fall fun fair raised $3846 "
                  "and the read-a-thon raised $2675. How much more does the school need?", 10000, 3846, 2675, "$",
                  "money raised", "money still needed"),
        out_then_in("The school had $6325 in its field trip fund. It spent $2958 on buses to Science World. Then a bottle "
                    "drive raised $1475. How much money is in the fund now?", 6325, 2958, 1475, "$", "after spending",
                    "after the bottle drive"),
        more_total("%s’s class raised $1475 at a bottle drive. %s’s class raised $386 more. "
                   "How much did the two classes raise altogether?" % (n[2][0], n[3][0]), 1475, 386, "$",
                   "%s’s class" % n[3][0]),
        one_add("A BC Ferries boat carried 3486 passengers in the morning and 2875 passengers in the afternoon. "
                "How many passengers did it carry that day?", 3486, 2875, "passengers", "Put the two parts of the day together, so add."),
        both_left("The Terry Fox Run had 5000 bottles of water. Runners took 2486 bottles in the morning and 1397 "
                  "at lunch. How many bottles were left?", 5000, 2486, 1397, "bottles", "bottles taken", "bottles left"),
        out_then_in("A food bank in Surrey had 4062 cans of food. It gave out 2785 cans. Then a school food drive brought in "
                    "1938 cans. How many cans does the food bank have now?", 4062, 2785, 1938, "cans", "after giving out",
                    "after the food drive"),
    ]
    assert len(its) == 20
    return {"title": "Word problems: salmon, road trips and fundraisers", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 3546 + 1999 == 5545 and 4678 + 2856 == 7534 and 5000 - 1268 == 3732 and 6152 - 2879 == 3273
    assert 3132 + 2445 == 5577 and 6981 - 4975 == 2006
    assert add_no_regroup(4678, 2856) == 6424
    assert sub_small_from_big(6152, 2879) == 4727
    assert sub_zero_as_ten(5000, 1268) == 3842, sub_zero_as_ten(5000, 1268)
    assert add_misalign(4567, 382) == 8387 and 4567 + 382 == 4949
    assert rnd_to(4678, 1000) + rnd_to(2856, 1000) == 8000
    return (
        "<h2>The idea: use place value</h2>"
        "<p>Numbers to " + TEN_K + " are made of thousands, hundreds, tens and ones. "
        "Add or subtract the same places. When a place gets 10 or more, <b>regroup</b>: 10 ones make 1 ten, "
        "10 tens make 1 hundred, and 10 hundreds make 1 thousand.</p>"
        "<p>First ask: can I do this in my head? If not, use the column method.</p>"
        "<h2>Mental math</h2>"
        "<p><b>Split:</b> break both numbers into thousands, hundreds, tens and ones. Add each place, then put the parts back together.</p>"
        "<figure class='sn-fig'>" + split_svg(3132, 2445, "+") +
        "<figcaption>3000 + 2000 = 5000, 100 + 400 = 500, 30 + 40 = 70, 2 + 5 = 7. Answer: 5577.</figcaption></figure>" +
        ex("Compensate", "What is 3546 + 1999?",
           "1999 is 1 less than 2000. Add 2000: 3546 + 2000 = 5546. You added 1 too many, so take 1 away: 5545.", "5545") +
        "<p><b>Count on:</b> when two numbers are close, count up from the smaller one to find the difference.</p>"
        "<figure class='sn-fig'>" + nline_svg(4975, [25, 1981], ["4975", "5000", "6981"]) +
        "<figcaption>6981 − 4975: from 4975 to 5000 is 25. From 5000 to 6981 is 1981. 25 + 1981 = 2006.</figcaption></figure>"
        "<h2>Column addition</h2>"
        "<p>Put <b>ones under ones</b>, tens under tens, and so on. Start on the right. "
        "If a column makes 10 or more, write the ones digit and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(4678, 2856, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 8 + 6 = 14, write 4, regroup 1. Tens: 7 + 5 + 1 = 13, write 3, regroup 1. "
        "Hundreds: 6 + 8 + 1 = 15, write 5, regroup 1. Thousands: 4 + 2 + 1 = 7. Answer: 7534.</figcaption></figure>"
        "<h2>Column subtraction, including across zeros</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, regroup 1 from the next column. "
        "If the next column is 0, go left to the first digit that is not 0. Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + column_svg(5000, 1268, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 0 − 8. There are 0 tens and 0 hundreds, so regroup 1 thousand as 10 hundreds, 1 hundred as 10 tens "
        "and 1 ten as 10 ones. 5000 becomes 4 thousands, 9 hundreds, 9 tens and 10 ones. "
        "10 − 8 = 2, 9 − 6 = 3, 9 − 2 = 7, 4 − 1 = 3. Answer: 3732.</figcaption></figure>"
        "<h2>Estimate, then check with the inverse</h2>"
        "<p>Before you start, <b>estimate</b>: round each number and work it out in your head. "
        "For 4678 + 2856, 5000 + 3000 = 8000, so the answer should be close to 8000.</p>"
        "<p>When you finish, <b>check with the inverse</b>. Addition and subtraction undo each other. "
        "To check 5000 − 1268 = 3732, add: 3732 + 1268 = 5000. You get back to the start, so the answer is right.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not regrouping (4678 + 2856 = 6424)", "Write the regrouped 1 under the next column and add it in"],
            ["Taking the smaller digit from the larger one (6152 − 2879 = 4727)",
             "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Making each 0 into 10 instead of 9 (5000 − 1268 = 3842)", "Only the last place gets 10. Each 0 you pass gives 1 away, so it becomes 9"],
            ["Lining up the numbers on the left (4567 + 382 = 8387)", "Line up the ones on the right: 4567 + 382 = 4949"],
        ])
    )


FAQ = [
    {"q": "What does Grade 4 learn about adding and subtracting in the BC math curriculum?",
     "a": "Under Computational fluency, Grade 4 students add and subtract whole numbers to 10 000. They use mental strategies, "
          "the column method with regrouping, estimation and the inverse to check their answers."},
    {"q": "What is the compensation strategy?",
     "a": "Round one number to a friendly number, work it out, then fix the difference. For 3546 + 1999, add 2000 to get 5546, "
          "then take away 1 to get 5545."},
    {"q": "How do you subtract across zeros, like 5000 − 1268?",
     "a": "Go left to the first digit that is not 0 and regroup from there; each 0 you pass becomes 9. 5000 becomes 4 thousands, "
          "9 hundreds, 9 tens and 10 ones, so 5000 − 1268 = 3732."},
    {"q": "Does adding and subtracting help with the Grade 4 FSA?",
     "a": "Yes. The FSA numeracy section asks students to solve number problems, and many of them need adding or subtracting. "
          "Estimating first and checking with the inverse helps students catch mistakes."},
]


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    N = r"(\d+(?:" + NB + r"\d{3})*)"
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='" + N + " (plus|minus) " + N + " written in columns'", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"What is " + N + " ([+−]) " + N + r"\?$", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "+" else a - b), it["q"]


def gen():
    rnd = random.Random(34803)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_mental(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_check(P), set_story(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "adding-and-subtracting-to-10000", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Adding and Subtracting to " + TEN_K,
        "seo_title": "Grade 4 Adding and Subtracting to " + TEN_K + " Worksheets: Regrouping and Mental Math (BC)",
        "short_title": "Adding and subtracting to " + TEN_K,
        "domain": "Computational fluency",
        "standard_code": "Grade 4: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Addition and subtraction to 10 000",
        "meta_desc": "Free Grade 4 math worksheets on adding and subtracting to " + TEN_K + ", matched to the BC curriculum: "
                     "mental math, column addition and subtraction with regrouping, subtracting across zeros, estimating, "
                     "checking with the inverse and BC word problems. 100 questions with an answer key. Good FSA practice.",
        "key_big": "Line up the ones. Regroup when you need to. Check with the inverse.",
        "key_sub": "Try mental math first: compensate (1999 is 2000 − 1), split or count on. In columns, start on the right; "
                   "every 0 you regroup across becomes 9. Estimate before you start, and add back what you took away to check.",
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
