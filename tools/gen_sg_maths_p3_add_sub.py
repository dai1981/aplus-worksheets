# -*- coding: utf-8 -*-
"""
SG Primary 3 Maths: Addition and subtraction (MOE 2021 Primary Mathematics Syllabus, Whole Numbers)
  python3 tools/gen_sg_maths_p3_add_sub.py
Mental addition and subtraction of two 2-digit numbers, 4-digit column addition with renaming,
4-digit column subtraction with renaming (including across zeros, such as 5000 − 1268),
checking with the inverse, and Singapore word problems with bar models.
Singapore English ("renaming"). Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are adapted from gen_cabc_math_g3_add_sub.py and gen_sg_maths_p4_add_sub_decimals.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
PARTFILL = "#fde3c8"
INK = "#2b2b2b"
RED = "#c0392b"
ORANGE = "#b35900"
NB = " "
FONT = "Arial, Helvetica, sans-serif"
B = "<b>?</b>"
BOX = "<b>☐</b>"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
PLACE = ["ones", "tens", "hundreds", "thousands"]
ONE = ["one", "ten", "hundred", "thousand"]


def num(n):
    """MOE style: 4-digit numbers plain, 5 or more digits with a no-break space."""
    s = str(n)
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
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


def digits(n, k=None):
    k = k or nlen(n)
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals, top=9999):
    return [v for v in vals if v is not None and 0 < v <= top]


# ------------------------------------------------------------ pictures: split (number bonds)
def parts(n):
    d = digits(n, 4)
    return [d[i] * 10 ** i for i in (3, 2, 1, 0) if d[i]]


def split_svg(a, b, op):
    """Both numbers on top, each split into tens and ones underneath."""
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
    lab = "number bonds: %d split into %s; %d split into %s" % (
        a, " and ".join(map(str, pa)), b, " and ".join(map(str, pb)))
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ pictures: number line
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
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")))


# ------------------------------------------------------------ pictures: column layout
def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line.
    answer: also write the answer.  marks: red renaming marks
    (+: the renamed 1s written small under the answer line;  −: old digits crossed out, new digits above)."""
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
            nd = rename_digits(a, b)
            od = digits(a)
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = px(i)
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%d %s %d written in columns" % (a, "plus" if op == "+" else "minus", b)
    return svg_wrap(W, int(H), "".join(s), label)


def misalign_svg(a, b, op, wrong, fs=28):
    """A student's work with the shorter number lined up on the LEFT, and the wrong answer in red."""
    cw = fs * 0.62
    k = max(nlen(a), nlen(b), nlen(wrong))
    pad_l = cw * 1.5 + 8
    left = pad_l + (k - nlen(a)) * cw
    right = pad_l + k * cw
    W = int(right + 12)
    s = []

    def put(t, x0, y, color):
        for n, ch in enumerate(t):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (x0 + cw * n + cw / 2, y, fs, color, ch))
    y1, y2 = 10 + fs, 10 + int(fs * 2.15)
    put(str(a), left, y1, INK)
    put(str(b), left, y2, INK)
    sign_x = pad_l - cw * 0.9 + (k - nlen(a)) * cw
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    put(str(wrong), right - nlen(wrong) * cw, ly + fs + 6, RED)
    H = ly + fs + 14
    label = "%d %s %d written with the digits lined up on the left and the answer %d" % (
        a, "plus" if op == "+" else "minus", b, wrong)
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ pictures: bar models
def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "ℓl1i":
            w += 0.45
        elif ch in "m×÷?$":
            w += 0.85
        else:
            w += 0.6
    return w * fs


def brace(x1, x2, y, up, lab, col=INK):
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_parts(parts_, total_lab, BW=500):
    """One bar split into parts drawn to scale. parts_ = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(v for v, _ in parts_)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [FILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts_):
        w = float(v) / tot * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts_), total_lab))


def bar_compare(rows, diff_lab, BW=420):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lab, fill) in enumerate([(n1, BW, l1, FILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fill, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lab)


# ------------------------------------------------------------ column methods
def rename_digits(a, b):
    """Top digits after all the renaming of column subtraction (ones first)."""
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


def sub_rename_cols(a, b):
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
    """True if some renaming has to go across a 0."""
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
        if t >= 10:
            assert i < k - 1, (a, b)
            ps.append("%s: %s = %d. Write %d and rename 10 %s as 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    return "Line up the ones. Start on the right. " + " ".join(ps) + " Answer: <b>%d</b>." % (a + b)


def sub_steps(a, b, check=True):
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
                zeros = [PLACE[m] for m in range(i + 1, j)]
                chain = ", then ".join("1 %s as 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. There are 0 %s, so rename %s. %s %d − %d = %d."
                       % (P, cur, db[i], " and 0 ".join(zeros), chain,
                          "Each 0 becomes 9." if len(zeros) > 1 else "The 0 becomes 9.", d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d. Rename 1 %s as 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            ps.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                ps.append("%s: write %d." % (P, d[i]))
        else:
            ps.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    out = "Line up the ones. Start on the right. " + " ".join(ps) + " Answer: <b>%d</b>." % r
    if check:
        out += " Check: %d + %d = %d." % (r, b, a)
    return out


# ------------------------------------------------------------ typical mistakes
def add_no_rename(a, b):
    """Never adds the renamed 1s."""
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
    """Wrote each column total side by side (7 + 8 = 15 written as 15)."""
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
    """Renaming across zeros: changed the zeros to 10 instead of 9."""
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
    """Did not rename across the zero: took 1 straight from the next non-zero place and left the 0s as 0."""
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
    """Lined up a 3-digit number on the left: 4352 − 216 done as 4352 − 2160."""
    if nlen(b) >= nlen(a) or a - 10 * b <= 0:
        return None
    return a - 10 * b


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_rename(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b), add_side_by_side(a, b)] + every + add_extra_one(a, b) + [abs(a - b), a + b + 10, a + b - 100])


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_misalign(a, b),
                  sub_forgot_reduce(a, b), a + b, a - b + 10, a - b - 10, a - b + 100])


# ============================================================ set 1: mental calculation (two 2-digit numbers)
def m_add_cands(a, b):
    return clean([add_no_rename(a, b), add_side_by_side(a, b), a + b + 10, a + b - 10, abs(a - b)])


def m_sub_cands(a, b):
    return clean([sub_small_from_big(a, b), sub_forgot_reduce(a, b), a + b, a - b - 10, a - b + 10])


def tens_ones_add_e(a, b):
    t, o = b // 10 * 10, b % 10
    s = "Split %d into %d and %d. %d + %d = %d. %d + %d = <b>%d</b>." % (b, t, o, a, t, a + t, a + t, o, a + b)
    if a % 10 + o >= 10:
        s += " (The ones make %d + %d = %d, so 1 more ten.)" % (a % 10, o, a % 10 + o)
    return s


def tens_ones_sub_e(a, b):
    t, o = b // 10 * 10, b % 10
    return "Take away the tens, then the ones. %d − %d = %d. %d − %d = <b>%d</b>." % (a, t, a - t, a - t, o, a - b)


def set_mental(P):
    its = []

    def add(q, a, b, e=None, cands=None):
        assert 10 <= a <= 99 and 10 <= b <= 99
        its.append(mcq(q, a + b, cands or m_add_cands(a, b), e or tens_ones_add_e(a, b)))

    def sub(q, a, b, e=None, cands=None):
        assert 10 <= a <= 99 and 10 <= b <= 99 and a > b
        its.append(mcq(q, a - b, cands or m_sub_cands(a, b), e or tens_ones_sub_e(a, b)))

    # add, no renaming
    add("Add the tens, then the ones. What is 34 + 25?", 34, 25)
    add("What is 52 + 36?", 52, 36)
    # add, renaming
    add(fig(split_svg(47, 35, "+")) + "Use the number bonds. What is 47 + 35?", 47, 35,
        "Tens: 40 + 30 = 70. Ones: 7 + 5 = 12. 70 + 12 = <b>82</b>. "
        "(72 forgets that 12 ones is 1 ten and 2 ones.)")
    add(fig(split_svg(68, 27, "+")) + "Use the number bonds. What is 68 + 27?", 68, 27,
        "Tens: 60 + 20 = 80. Ones: 8 + 7 = 15. 80 + 15 = <b>95</b>. "
        "(815 writes 8 tens and 15 ones side by side.)")
    assert 56 + 38 == 94
    add(fig(nline_svg(56, [30, 8], ["56", "86", "?"])) + "Where does the last jump land? (This is 56 + 38.)", 56, 38,
        "56 + 30 = 86. 86 + 8 = <b>94</b>. (86 + 4 = 90, then 4 more is 94.)", [84, 86, 104])
    add("What is 76 + 58? The answer is more than 100.", 76, 58,
        "Tens: 70 + 50 = 120. Ones: 6 + 8 = 14. 120 + 14 = <b>134</b>. "
        "(124 forgets the ten in 14. 1214 writes 12 tens and 14 ones side by side.)")
    # add, compensate
    assert 46 + 29 == 75 and 58 + 39 == 97
    add("29 is 1 less than 30. What is 46 + 29?", 46, 29,
        "Add 30, then take away the extra 1. 46 + 30 = 76. 76 − 1 = <b>75</b>.", [77, 76, 65])
    add("39 is 1 less than 40. What is 58 + 39?", 58, 39,
        "Add 40, then take away the extra 1. 58 + 40 = 98. 98 − 1 = <b>97</b>.", [99, 98, 87])
    # subtract, no renaming
    sub("Take away the tens, then the ones. What is 87 − 45?", 87, 45)
    sub("What is 69 − 23?", 69, 23)
    # subtract, renaming
    sub("What is 62 − 27?", 62, 27,
        "Take away the tens, then the ones. 62 − 20 = 42. 42 − 7 = <b>35</b>. "
        "(45 takes 2 from 7 instead of 7 from 12.)")
    assert 83 - 46 == 37
    sub(fig(nline_svg(83, [-40, -6], ["83", "43", "?"])) + "Where does the last jump land? (This is 83 − 46.)", 83, 46,
        "83 − 40 = 43. 43 − 6 = <b>37</b>. (43 − 3 = 40, then 3 more back is 37.)", [43, 47, 39])
    sub("What is 91 − 58?", 91, 58,
        "Take away the tens, then the ones. 91 − 50 = 41. 41 − 8 = <b>33</b>. "
        "(47 takes 1 from 8 instead of 8 from 11.)")
    assert 75 - 39 == 36
    sub("39 is 1 less than 40. What is 75 − 39?", 75, 39,
        "Take away 40. You took away 1 too many, so add 1 back. 75 − 40 = 35. 35 + 1 = <b>36</b>.",
        [34, 35, sub_small_from_big(75, 39)])
    # count on to find the difference
    assert 82 - 67 == 15 and sub_small_from_big(82, 67) == 25
    sub(fig(nline_svg(67, [3, 12], ["67", "70", "82"])) + "Count on from 67 to 82. What is 82 − 67?", 82, 67,
        "The numbers are close, so count on. 67 + 3 = 70. 70 + 12 = 82. 3 + 12 = <b>15</b>.", [25, 12, 149])
    # missing numbers
    assert 45 + 47 == 92 and sub_small_from_big(92, 45) == 53 and sub_forgot_reduce(92, 45) == 57
    its.append(mcq("What number goes in the box?  45 + %s = 92" % BOX, 47, [137, 53, 57],
                   "Use subtraction: 92 − 45. 92 − 40 = 52. 52 − 5 = <b>47</b>. Check: 45 + 47 = 92. "
                   "(137 adds instead of subtracting.)"))
    assert 73 - 28 == 45 and 45 - 28 == 17
    its.append(mcq("What number goes in the box?  %s − 28 = 45" % BOX, 73, [17, 63, 83],
                   "Add back what was taken away: 45 + 28. 45 + 20 = 65. 65 + 8 = <b>73</b>. Check: 73 − 28 = 45. "
                   "(17 subtracts instead of adding. 63 forgets that 13 ones is 1 ten and 3 ones.)"))
    sub("Take away the tens, then the ones. What is 64 − 28?", 64, 28,
        "64 − 20 = 44. 44 − 8 = <b>36</b>. (44 takes 4 from 8 instead of 8 from 14.)")
    # short stories
    n, he, his = P.next()
    add("%s has 48 stickers. %s friend gives %s 37 more. How many stickers does %s have now?"
        % (n, cap(his), "her" if he == "she" else "him", n), 48, 37,
        "More stickers come in, so add. 48 + 30 = 78. 78 + 7 = <b>85</b>.")
    n, he, his = P.next()
    sub("%s’s storybook has 93 pages. %s has read 56 pages. How many pages are left?" % (n, cap(he)), 93, 56,
        "Find what is left, so subtract. 93 − 50 = 43. 43 − 6 = <b>37</b>. Check: 37 + 56 = 93.")
    assert len(its) == 20, len(its)
    return {"title": "Mental addition and subtraction of 2-digit numbers", "items": its}


# ============================================================ set 2: 4-digit addition with renaming
LESSON = {(3467, 2585), (5000, 1268), (6327, 2854), (2456, 317)}


def item_add(a, b, col):
    q = (fig(column_svg(a, b, "+")) + "Add. Rename when a column makes 10 or more.") if col else \
        "Use the column method. What is %d + %d?" % (a, b)
    return mcq(q, a + b, add_cands(a, b), add_steps(a, b))


def item_sub(a, b, col):
    q = (fig(column_svg(a, b, "-")) + "Subtract. Rename when the top digit is smaller.") if col else \
        "Use the column method. What is %d − %d?" % (a, b)
    return mcq(q, a - b, sub_cands(a, b), sub_steps(a, b))


def rand_n(rnd, la):
    return rnd.randint(1012, 7980) if la == 4 else rnd.randint(112, 980)


def pick_add(rnd, seen, la, lb, cols):
    while True:
        a, b = rand_n(rnd, la), rand_n(rnd, lb)
        if a + b > 9800 or (a, b) in seen or (b, a) in seen or (a, b) in LESSON or a % 10 == 0 or b % 10 == 0:
            continue
        if add_carry_cols(a, b) != cols or abs(a - b) < 300:
            continue
        seen.add((a, b))
        return a, b


def set_add(rnd, seen, P):
    its = []
    plan = ([(4, 4, [0])] * 2 + [(4, 4, [1])] * 2 + [(4, 4, [2])] * 2 + [(4, 3, [0])] +
            [(4, 4, [0, 1])] * 2 + [(4, 4, [1, 2])] * 2 + [(4, 3, [0, 1])] * 2 + [(4, 4, [0, 2])] +
            [(4, 4, [0, 1, 2])] * 3 + [(4, 3, [0, 1, 2])] * 2)
    for i, (la, lb, cols) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, cols)
        if lb == 3 and rnd.random() < 0.5:
            a, b = b, a
        its.append(item_add(a, b, i % 3 != 2))
    # misaligned columns
    a, b = 2456, 317
    w = add_misalign(a, b)
    assert w == 5626 and a + b == 2773
    n, he, his = P.next()
    its.append(mcq(fig(misalign_svg(a, b, "+", w)) + "%s worked out %d + %d like this. What is the correct answer?" % (n, a, b),
                   a + b, [w, add_no_rename(a, b), a + b + 100],
                   "%s lined up 317 on the left, so the 3 hundreds went under the thousands. "
                   "%s" % (n, add_steps(a, b))))
    assert len(its) == 20
    return {"title": "4-digit addition with renaming", "items": its}


# ============================================================ set 3: 4-digit subtraction with renaming
def pick_sub(rnd, seen, lb, cols):
    while True:
        a = rnd.randint(2100, 9890)
        b = rnd.randint(1012, a - 400) if lb == 4 else rnd.randint(112, 980)
        if (a, b) in seen or (a, b) in LESSON or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if 0 in digits(a)[:3]:
            continue
        if sub_rename_cols(a, b) != cols:
            continue
        seen.add((a, b))
        return a, b


def set_sub(rnd, seen, P):
    its = []
    plan = ([(4, [0])] * 2 + [(4, [1])] + [(4, [2])] + [(3, [0])] + [(4, [0, 1])] * 2 + [(4, [1, 2])] +
            [(3, [0, 1])] + [(4, [0, 2])] + [(4, [0, 1, 2])] * 2 + [(3, [0, 1, 2])])
    for i, (lb, cols) in enumerate(plan):
        a, b = pick_sub(rnd, seen, lb, cols)
        its.append(item_sub(a, b, i % 3 != 2))
    tops = {5000}                                       # 5000 − 1268 is the lesson example
    pats = ["x000", "x00x", "x0xx", "x000", "xx0x", "x00x"]
    for n_, p in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lb = 3 if n_ == 4 else 4
            b = rnd.randint(1012, a - 500) if lb == 4 else rnd.randint(112, 980)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or 0 in digits(b):
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, n_ % 3 != 2))
            break
    a, b = 4352, 216
    w = sub_misalign(a, b)
    assert w == 2192 and a - b == 4136
    n, he, his = P.next()
    its.append(mcq(fig(misalign_svg(a, b, "-", w)) + "%s worked out %d − %d like this. What is the correct answer?" % (n, a, b),
                   a - b, [w, sub_small_from_big(a, b), a - b + 10],
                   "%s lined up 216 on the left, so %s really took away 2160. %s"
                   % (n, he, sub_steps(a, b))))
    assert len(its) == 20
    return {"title": "4-digit subtraction with renaming, including across zeros", "items": its}


# ============================================================ set 4: check with the inverse
def set_check(P):
    its = []
    # T1: which calculation checks it?
    for a, b in [(6214, 2587), (8053, 3476)]:
        r = a - b
        its.append(mcq("Which addition checks %d − %d = %d?" % (a, b, r), "%d + %d" % (r, b),
                       ["%d + %d" % (a, b), "%d − %d" % (r, b), "%d + %d" % (a, r)],
                       "Add the answer to the number you took away. You should get the number you started with: "
                       "%d + %d = %d. So use <b>%d + %d</b>." % (r, b, a, r, b)))
    for a, b in [(3478, 2965), (4569, 1876)]:
        s = a + b
        its.append(mcq("Which subtraction checks %d + %d = %d?" % (a, b, s), "%d − %d" % (s, b),
                       ["%d + %d" % (s, b), "%d − %d" % (a, b), "%d + %d" % (s, a)],
                       "Take one of the numbers you added away from the answer. You should get the other number: "
                       "%d − %d = %d. So use <b>%d − %d</b>." % (s, b, a, s, b)))
    # T2: a wrong answer, found by the check
    rows = [("-", 7003, 2465, sub_zero_as_ten, "changed the 0s to 10 instead of 9"),
            ("-", 6324, 1858, sub_small_from_big, "took the smaller digit from the larger one"),
            ("+", 5246, 2879, add_no_rename, "did not rename"),
            ("-", 8251, 3476, sub_forgot_reduce, "did not take 1 away from the next place after renaming"),
            ("+", 3687, 2456, lambda a, b: add_forgot_one(a, b, "last"), "forgot one renamed 1")]
    for op, a, b, f, why in rows:
        n, he, his = P.next()
        w = f(a, b)
        if op == "-":
            r = a - b
            chk = w + b
            assert w != r and chk != a
            q = "%s worked out %d − %d = %d. Add to check. What is the correct answer?" % (n, a, b, w)
            e = ("Check: %d + %d = %d, not %d, so %s’s answer is wrong. %s %s. %s"
                 % (w, b, chk, a, n, cap(he), why, sub_steps(a, b)))
            cands = [w] + sub_cands(a, b)
        else:
            r = a + b
            chk = w - b
            assert w != r and chk != a and chk > 0
            q = "%s worked out %d + %d = %d. Subtract to check. What is the correct answer?" % (n, a, b, w)
            e = ("Check: %d − %d = %d, not %d, so %s’s answer is wrong. %s %s. %s Check: %d − %d = %d."
                 % (w, b, chk, a, n, cap(he), why, add_steps(a, b), r, b, a))
            cands = [w] + add_cands(a, b)
        its.append(mcq(q, r, cands, e))
    # T3: missing numbers
    assert 3543 + 2457 == 6000 and sub_zero_as_ten(6000, 2457) == 3653 and sub_small_from_big(6000, 2457) == 4457
    its.append(mcq("What number goes in the box?  %s + 2457 = 6000" % BOX, 3543, [8457, 3653, 4457],
                   "Use the inverse: 6000 − 2457. Rename 1 thousand as 10 hundreds, then 1 hundred as 10 tens, "
                   "then 1 ten as 10 ones: 5 thousands, 9 hundreds, 9 tens, 10 ones. "
                   "10 − 7 = 3, 9 − 5 = 4, 9 − 4 = 5, 5 − 2 = 3. Answer: <b>3543</b>. Check: 3543 + 2457 = 6000. "
                   "(8457 adds instead of subtracting.)"))
    assert 2746 + 1385 == 4131 and 2746 - 1385 == 1361 and add_no_rename(2746, 1385) == 3021
    its.append(mcq("What number goes in the box?  %s − 1385 = 2746" % BOX, 4131, [1361, 3021, 4031],
                   "Add back what was taken away: 2746 + 1385. " + add_steps(2746, 1385) +
                   " Check: 4131 − 1385 = 2746. (1361 subtracts instead of adding.)"))
    assert 8000 - 3654 == 4346 and sub_zero_as_ten(8000, 3654) == 4456 and sub_small_from_big(8000, 3654) == 5654
    its.append(mcq("What number goes in the box?  8000 − %s = 3654" % BOX, 4346, [4456, 5654, sub_zero_skip(8000, 3654)],
                   "The box is the part taken away: 8000 − 3654. " + sub_steps(8000, 3654, check=False) +
                   " Check: 8000 − 4346 = 3654. (4456 changes the 0s to 10 instead of 9.)"))
    assert 7105 - 2738 == 4367 and sub_small_from_big(7105, 2738) == 5633 and sub_zero_as_ten(7105, 2738) == 4377
    its.append(mcq("What number goes in the box?  2738 + %s = 7105" % BOX, 4367, [5633, 4377, 9843],
                   "Use the inverse: 7105 − 2738. " + sub_steps(7105, 2738, check=False) +
                   " Check: 2738 + 4367 = 7105. (5633 takes the smaller digit from the larger one. 9843 adds instead of subtracting.)"))
    # T4: bar models with a missing part
    for whole, part in [(7240, 3865), (5300, 2476), (9015, 4628)]:
        miss = whole - part
        model = bar_parts([(part, str(part)), (miss, "?")], str(whole))
        its.append(mcq(fig(model) + "Find the missing part.", miss, sub_cands(whole, part),
                       "Whole − part = missing part: %d − %d. %s Check: %d + %d = %d."
                       % (whole, part, sub_steps(whole, part, check=False), miss, part, whole)))
    # T5: what should the check give?
    n, he, his = P.next()
    its.append(mcq("%s works out 4005 − 1738 = 2267. Then %s checks it by working out 2267 + 1738. "
                   "What answer should the check give?" % (n, he), 4005, [2267, 1738, 5743],
                   "Adding back the number taken away gives the number you started with: 2267 + 1738 = <b>4005</b>. "
                   "So 4005 − 1738 = 2267 is correct."))
    assert 4005 - 1738 == 2267 and 4005 + 1738 == 5743
    n, he, his = P.next()
    assert 3456 + 2789 == 6245 and 6245 + 2789 == 9034
    its.append(mcq("%s works out 3456 + 2789 = 6245. Then %s checks it by working out 6245 − 2789. "
                   "What answer should the check give?" % (n, he), 3456, [6245, 2789, 9034],
                   "Taking away one number you added gives the other number: 6245 − 2789 = <b>3456</b>. "
                   "So 3456 + 2789 = 6245 is correct."))
    assert 5132 - 2764 == 2368
    its.append(mcq("5132 − 2764 = 2368. Which calculation gives 5132?", "2368 + 2764",
                   ["2368 − 2764", "5132 + 2764", "2764 − 2368"],
                   "Answer + the number taken away = the start number: <b>2368 + 2764</b> = 5132."))
    # fact family
    opts = ["3456 − 2789 = 667", "2789 + 3456 = 6245", "6245 − 2789 = 3456", "6245 − 3456 = 2789"]
    assert 3456 - 2789 == 667
    its.append(mcq("Which number sentence is NOT in the same family as 3456 + 2789 = 6245?", opts[0], opts[1:],
                   "A family uses the same three numbers: 3456, 2789 and 6245. <b>3456 − 2789 = 667</b> is true, "
                   "but 667 is not one of the three numbers."))
    assert len(its) == 20, len(its)
    return {"title": "Check with the inverse", "items": its}


# ============================================================ set 5: word problems with bar models
def unit(v, u):
    return "$%d" % v if u == "$" else "%d %s" % (v, u)


def eu(v, u):
    return "$%d" % v if u == "$" else str(v)


def story(q, ans, cands, u, e, model=None):
    q = (fig(model) if model else "") + q
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e)


def one_add(q, a, b, u, lead, model=None):
    s = a + b
    assert s <= 9999
    e = lead + " %s + %s = <b>%s</b>. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
    return story(q, s, add_cands(a, b), u, e, model)


def one_sub(q, a, b, u, lead, model=None):
    r = a - b
    e = lead + " %s − %s = <b>%s</b>. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
    return story(q, r, sub_cands(a, b), u, e, model)


def start_add(q, now, more, u, model=None):
    x = now - more
    e = ("Work backwards. Take away the %s that came later: %s − %s = <b>%s</b>. Check: %s + %s = %s."
         % (eu(more, u), eu(now, u), eu(more, u), eu(x, u), eu(x, u), eu(more, u), eu(now, u)))
    return story(q, x, [now + more] + sub_cands(now, more), u, e, model)


def start_sub(q, now, lost, u, model=None):
    x = now + lost
    assert x <= 9999
    e = ("Work backwards. Add back the %s that were sold: %s + %s = <b>%s</b>. Check: %s − %s = %s."
         % (eu(lost, u), eu(now, u), eu(lost, u), eu(x, u), eu(x, u), eu(lost, u), eu(now, u)))
    return story(q, x, [now - lost] + add_cands(now, lost), u, e, model)


def both_left(q, A, Bv, C, u, s1, s2, model=None):
    """A − (B + C)."""
    t = Bv + C
    r = A - t
    assert r > 0 and r not in (A, Bv, C)
    e = ("Step 1, %s: %s + %s = %s. Step 2, %s: %s − %s = <b>%s</b>."
         % (s1, eu(Bv, u), eu(C, u), eu(t, u), s2, eu(A, u), eu(t, u), eu(r, u)))
    return story(q, r, [A - Bv, t, sub_small_from_big(A, t), sub_zero_as_ten(A, t), sub_forgot_reduce(A, t), A - Bv + C],
                 u, e, model)


def out_then_in(q, A, Bv, C, u, s1, s2, model=None):
    """A − B + C."""
    m = A - Bv
    r = m + C
    e = "Step 1, %s: %d − %d = %d. Step 2, %s: %d + %d = <b>%d</b>." % (s1, A, Bv, m, s2, m, C, r)
    return story(q, r, [m, A - Bv - C, sub_small_from_big(A, Bv) + C, add_forgot_one(m, C, "last"), A + Bv + C], u, e, model)


def more_total(q, A, Bv, u, who2, model=None):
    """A + (A + B)."""
    m = A + Bv
    r = A + m
    assert r <= 9999
    e = ("Step 1, %s: %d + %d = %d. Step 2, both together: %d + %d = <b>%d</b>." % (who2, A, Bv, m, A, m, r))
    return story(q, r, [m, A + Bv + Bv, add_forgot_one(A, m, "last"), A + A], u, e, model)


def less_total(q, A, Bv, u, who2, model=None):
    """A + (A − B)."""
    m = A - Bv
    r = A + m
    e = ("Step 1, %s: %d − %d = %d. Step 2, both together: %d + %d = <b>%d</b>." % (who2, A, Bv, m, A, m, r))
    return story(q, r, [m, A + Bv, A + A + Bv, add_forgot_one(A, m, "last")], u, e, model)


def set_story(P):
    n = [P.next() for _ in range(6)]
    its = [
        one_add("On Saturday, 2548 people visited the Singapore Zoo in the morning and 1876 people visited in the "
                "afternoon. How many people visited the zoo that day?", 2548, 1876, "people",
                "Put the two parts together, so add.",
                bar_parts([(2548, "2548"), (1876, "1876")], "?")),
        one_add("A school library had 3465 books. It bought 1287 new books. How many books does the library have now?",
                3465, 1287, "books", "New books are added, so add."),
        one_add("At the school fair, the P3 classes raised $1365 and the P4 classes raised $1758. "
                "How much money did they raise altogether?", 1365, 1758, "$", "Altogether means add.",
                bar_parts([(1365, "$1365"), (1758, "$1758")], "?")),
        one_add("%s walked 1850 m from %s HDB block to the library. Then %s walked 1375 m to the hawker centre. "
                "How far did %s walk altogether?" % (n[0][0], n[0][2], n[0][1], n[0][1]), 1850, 1375, "m",
                "Put the two parts of the walk together, so add."),
        one_sub("A hall has 1500 seats for the Children’s Day concert. 1268 pupils are seated. How many seats are empty?",
                1500, 1268, "seats", "Find the part that is left, so subtract.",
                bar_parts([(1268, "1268"), (232, "?")], "1500")),
        one_sub("A bakery made 2400 mooncakes for the Mid-Autumn Festival. It sold 1785 of them. "
                "How many mooncakes were left?", 2400, 1785, "mooncakes", "Find what is left, so subtract."),
        one_sub("Hui Min’s school has 1835 pupils. Ethan’s school has 2140 pupils. "
                "How many more pupils does Ethan’s school have?", 2140, 1835, "pupils",
                "How many more means find the difference, so subtract.",
                bar_compare([("Ethan’s", 2140, "2140"), ("Hui Min’s", 1835, "1835")], "?")),
        one_sub("A shop had 3000 red packets before Chinese New Year. It sold 1746 of them. "
                "How many red packets were left?", 3000, 1746, "red packets", "Find what is left, so subtract.",
                bar_parts([(1746, "1746"), (1254, "?")], "3000")),
        one_sub("Mrs Lim wants to buy a laptop that costs $1250. She has saved $875. How much more money does she need?",
                1250, 875, "$", "Find the difference, so subtract."),
        start_add("There were some people at East Coast Park in the morning. In the afternoon, 1385 more people came. "
                  "Then there were 4012 people. How many people were there in the morning?", 4012, 1385, "people",
                  bar_parts([(2627, "?"), (1385, "1385")], "4012")),
        start_sub("A fruit stall had some durians on Saturday morning. It sold 1365 durians and had 1478 left. "
                  "How many durians did it have at the start?", 1478, 1365, "durians",
                  bar_parts([(1365, "sold 1365"), (1478, "left 1478")], "?")),
        both_left("The school aims to collect 6000 cans of food for a charity. P3 pupils collect 1865 cans and "
                  "P4 pupils collect 2348 cans. How many more cans are needed?", 6000, 1865, 2348, "cans",
                  "cans collected", "cans still needed",
                  bar_parts([(1865, "1865"), (2348, "2348"), (1787, "?")], "6000")),
        both_left("Mr Rahman had $4500. He paid $1385 for a television and $968 for a washing machine. "
                  "How much money did he have left?", 4500, 1385, 968, "$", "money spent", "money left",
                  bar_parts([(1385, "$1385"), (968, "$968"), (2147, "?")], "$4500")),
        out_then_in("An MRT train had 1625 passengers. At the next station, 748 passengers got off and 586 passengers "
                    "got on. How many passengers are on the train now?", 1625, 748, 586, "passengers",
                    "after the passengers got off", "after the new passengers got on"),
        more_total("On Saturday, 2365 people visited Gardens by the Bay. On Sunday, 1478 more people visited than on "
                   "Saturday. How many people visited on the two days?", 2365, 1478, "people", "Sunday’s visitors",
                   bar_compare([("Sunday", 3843, "?"), ("Saturday", 2365, "2365")], "1478")),
        less_total("A bubble tea shop sold 1846 cups in June. In July, it sold 379 fewer cups than in June. "
                   "How many cups did it sell in the two months?", 1846, 379, "cups", "July’s cups",
                   bar_compare([("June", 1846, "1846"), ("July", 1467, "?")], "379")),
        one_sub("%s walked 3250 steps in the morning and 4105 steps in the afternoon. How many more steps did %s walk "
                "in the afternoon?" % (n[1][0], n[1][1]), 4105, 3250, "steps",
                "How many more means find the difference, so subtract.",
                bar_compare([("afternoon", 4105, "4105"), ("morning", 3250, "3250")], "?")),
        one_sub("Mdm Wong has 3000 g of flour. She uses 1275 g to bake kueh for Hari Raya Puasa. "
                "How much flour is left?", 3000, 1275, "g", "Find what is left, so subtract."),
        more_total("%s’s class collected 1485 bottles for recycling. %s’s class collected 268 more bottles than %s’s class. "
                   "How many bottles did the two classes collect?" % (n[2][0], n[3][0], n[2][0]), 1485, 268, "bottles",
                   "%s’s class" % n[3][0]),
        one_add("A jug has 1250 ml of water. %s pours in 975 ml more. How much water is in the jug now?" % n[4][0],
                1250, 975, "ml", "More water is poured in, so add."),
    ]
    assert len(its) == 20
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    assert 47 + 35 == 82 and 46 + 29 == 75 and 3467 + 2585 == 6052 and 6327 - 2854 == 3473 and 5000 - 1268 == 3732
    assert add_no_rename(3467, 2585) == 5942 and sub_small_from_big(6327, 2854) == 4533
    assert sub_zero_as_ten(5000, 1268) == 3842 and add_misalign(2456, 317) == 5626 and 2456 + 317 == 2773
    assert 3732 + 1268 == 5000 and 4500 - 1385 - 968 == 2147
    return (
        "<h2>Mental sums with 2-digit numbers</h2>"
        "<p>Split one number into <b>tens and ones</b>. Add or take away the tens first, then the ones.</p>"
        "<figure class='sn-fig'>" + split_svg(47, 35, "+") +
        "<figcaption>47 + 35. Tens: 40 + 30 = 70. Ones: 7 + 5 = 12. 70 + 12 = 82.</figcaption></figure>" +
        ex("Use a near ten", "What is 46 + 29?",
           "29 is 1 less than 30. 46 + 30 = 76. You added 1 too many, so take 1 away: 76 − 1 = 75.", "75") +
        "<h2>4-digit addition: rename when a column makes 10 or more</h2>"
        "<p>Put <b>ones under ones</b>, tens under tens, hundreds under hundreds and thousands under thousands. "
        "Start with the ones on the right. If a column makes 10 or more, write the ones digit and "
        "<b>rename</b>: 10 ones = 1 ten, 10 tens = 1 hundred, 10 hundreds = 1 thousand.</p>"
        "<figure class='sn-fig'>" + column_svg(3467, 2585, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 5 = 12. Write 2, rename 10 ones as 1 ten. Tens: 6 + 8 + 1 = 15. Write 5, "
        "rename 10 tens as 1 hundred. Hundreds: 4 + 5 + 1 = 10. Write 0, rename 10 hundreds as 1 thousand. "
        "Thousands: 3 + 2 + 1 = 6. Answer: 6052.</figcaption></figure>"
        "<h2>4-digit subtraction: rename when the top digit is smaller</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, "
        "rename 1 from the next place as 10.</p>"
        "<figure class='sn-fig'>" + column_svg(6327, 2854, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 − 4 = 3. Tens: 2 − 5. Rename 1 hundred as 10 tens: 12 − 5 = 7. "
        "Hundreds: 2 − 8. Rename 1 thousand as 10 hundreds: 12 − 8 = 4. Thousands: 5 − 2 = 3. "
        "Answer: 3473.</figcaption></figure>"
        "<p><b>Across zeros:</b> in 5000 − 1268 there are no hundreds, tens or ones to rename. "
        "Rename 1 thousand as 10 hundreds, then 1 hundred as 10 tens, then 1 ten as 10 ones. "
        "Each 0 in the middle becomes 9.</p>"
        "<figure class='sn-fig'>" + column_svg(5000, 1268, "-", answer=True, marks=True, fs=34) +
        "<figcaption>5000 becomes 4 thousands, 9 hundreds, 9 tens and 10 ones. "
        "10 − 8 = 2, 9 − 6 = 3, 9 − 2 = 7, 4 − 1 = 3. Answer: 3732.</figcaption></figure>"
        "<h2>Check with the inverse</h2>"
        "<p>Addition and subtraction undo each other. To check a subtraction, add the answer to the number "
        "you took away. To check an addition, take one number away from the answer.</p>" +
        ex("Check", "Is 5000 − 1268 = 3732 right?",
           "Add back: 3732 + 1268 = 5000. You get the number you started with, so it is right.", "Yes") +
        "<h2>Word problems: draw a bar model</h2>"
        "<p>Draw the whole and the parts. Put a ? on the part you need to find. "
        "If you know the whole and a part, subtract. If you know all the parts, add.</p>"
        "<figure class='sn-fig'>" + bar_parts([(1385, "$1385"), (968, "$968"), (2147, "?")], "$4500") +
        "<figcaption>Mr Rahman had $4500. He spent $1385 and $968. Money spent: $1385 + $968 = $2353. "
        "Money left: $4500 − $2353 = $2147.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Not renaming (3467 + 2585 = 5942)", "Write the renamed 1 in the next column and add it in"],
            ["Taking the smaller digit from the larger one (6327 − 2854 = 4533)",
             "Always take the bottom digit from the top digit. Rename when the top digit is smaller"],
            ["Making the 0s into 10s (5000 − 1268 = 3842)", "Only the ones get 10. The 0s in the middle become 9"],
            ["Lining up the columns wrongly (2456 + 317 = 5626)", "Line up the ones on the right: 2456 + 317 = 2773"],
        ])
    )


FAQ = [
    {"q": "What is taught in P3 addition and subtraction?",
     "a": "In Primary 3, students add and subtract numbers up to 4 digits with the column method, and add and subtract "
          "two 2-digit numbers mentally. They check answers with the inverse and solve word problems with bar models."},
    {"q": "How do I explain renaming to my child?",
     "a": "Renaming means changing 10 of one place for 1 of the next place, such as 10 ones for 1 ten. "
          "In subtraction it goes the other way: 1 ten is renamed as 10 ones when the top digit is too small."},
    {"q": "How do you subtract across zeros, like 5000 − 1268?",
     "a": "Rename 1 thousand as 10 hundreds, then 1 hundred as 10 tens, then 1 ten as 10 ones. "
          "5000 becomes 4 thousands, 9 hundreds, 9 tens and 10 ones, so 5000 − 1268 = 3732."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Addition and subtraction up to 4 digits and mental calculation with two 2-digit numbers are part of "
          "Whole Numbers in the MOE 2021 Primary 3 Mathematics Syllabus (Standard Mathematics)."},
]


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    n = 0
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='(\d+) (plus|minus) (\d+) written in columns'", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "plus" else a - b), it["q"]
                n += 1
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "+" else a - b), it["q"]
                n += 1
            m = re.search(r"\(This is (\d+) ([+−]) (\d+)\.\)", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "+" else a - b), it["q"]
                n += 1
            m = re.search(r"aria-label='bar model: parts (\d+), \?, whole (\d+)'", it["q"])
            if m:
                assert int(re.match(r'\$?(\d+)', right).group(1)) == int(m.group(2)) - int(m.group(1)), it["q"]
                n += 1
            vals = []
            for c in it["c"]:
                mm = re.fullmatch(r"\$?(\d+)( [a-z ]+)?", c)
                if mm:
                    vals.append(int(mm.group(1)))
                    assert int(mm.group(1)) <= 9999, c
            if len(vals) == 4:
                assert len(set(vals)) == 4, it
    return n


def gen():
    rnd = random.Random(63802)
    P = People(rnd)
    seen_a, seen_s = set(), set()
    sets = [set_mental(P), set_add(rnd, seen_a, P), set_sub(rnd, seen_s, P), set_check(P), set_story(P)]
    balance(sets, rnd)
    verify(sets)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "addition-and-subtraction", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Addition and Subtraction",
        "seo_title": "P3 Addition and Subtraction Worksheets: Free Primary 3 Maths with Answers (MOE Syllabus)",
        "short_title": "Addition and Subtraction",
        "domain": "Number and Algebra",
        "standard_code": "Primary 3: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Addition and subtraction algorithms (up to 4 digits); mental calculation of two 2-digit numbers",
        "meta_desc": "Free P3 maths practice: mental sums, 4-digit addition and subtraction with renaming, "
                     "checking with the inverse and bar models. 100 questions with answers.",
        "key_big": "Line up the digits by place value. Rename when you need to.",
        "key_sub": "5000 − 1268 = 3732. Check: 3732 + 1268 = 5000.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model|number line|number bonds")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
