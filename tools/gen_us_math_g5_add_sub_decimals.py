# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Add and Subtract Decimals (5.NBT.B.7, addition and subtraction)
  python3 tools/gen_us_math_g5_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (3.6 + 2.45 -> 360 + 245 hundredths), so every regroup and every typical mistake is exact.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
FILL = "#4fae74"       # first number on a grid
FILL2 = "#f4c430"      # second number on a grid
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
PLACE = ["hundredths", "tenths", "ones", "tens", "hundreds", "thousands"]
ONE = ["hundredth", "tenth", "one", "ten", "hundred", "thousand"]


# ------------------------------------------------------------ numbers
def dec(s):
    """Decimal places as written: '3.6' -> 1, '5' -> 0."""
    return len(s.split(".")[1]) if "." in s else 0


def nice(d):
    """Shortest exact text for a Decimal, with commas: 6.05, 3.8, 605, 1,250.5."""
    d = Decimal(d)
    t = format(d.normalize(), "f")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    ip, _, fp = t.partition(".")
    ip = "{:,}".format(int(ip))
    return ip + ("." + fp if fp else "")


def fixed(d, p):
    """Decimal with exactly p places and commas: fixed(5, 2) -> 5.00."""
    t = format(Decimal(d).quantize(Decimal(1).scaleb(-p)), "f")
    ip, _, fp = t.partition(".")
    return "{:,}".format(int(ip)) + ("." + fp if fp else "")


def money(d):
    return "$" + fixed(d, 2)


def scale(nums):
    """Common number of places P and every number as a whole number of the smallest place."""
    P = max(dec(n) for n in nums)
    return P, [int(Decimal(n).scaleb(P)) for n in nums]


def back(i, P):
    return Decimal(i).scaleb(-P)


def nlen(n):
    return len(str(n))


def digits(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]          # smallest place first


def pname(i, P):
    return PLACE[i + 2 - P]


def oname(i, P):
    return ONE[i + 2 - P]


def cap(s):
    return s[0].upper() + s[1:]


def annex_note(nums, P):
    """'Write 3.6 as 3.60.' for every number with fewer places."""
    w = ["%s as %s" % (n, fixed(Decimal(n), P)) for n in nums if dec(n) < P]
    if not w:
        return ""
    return "Write " + " and ".join(w) + "."


# ------------------------------------------------------------ column steps (explanations)
def add_steps(nums, compact=None):
    P, ints = scale(nums)
    k = max(nlen(x) for x in ints)
    if compact is None:
        compact = k >= 5
    ds = [digits(x, k) for x in ints]
    carry, parts, regs = 0, [], []
    for i in range(k):
        col = [d[i] for d, x in zip(ds, ints) if i < nlen(x) or i < P + 1]
        t = sum(col) + carry
        expr = " + ".join(str(c) for c in col) + (" + %d" % carry if carry else "")
        P_ = cap(pname(i, P))
        if t >= 10 and i == k - 1:
            msg = "%s: %s = %d, write %d." % (P_, expr, t, t)
            parts.append(msg); regs.append(msg); carry = 0
        elif t >= 10:
            msg = "%s: %s = %d, write %d and regroup %d %s." % (P_, expr, t, t % 10, t // 10,
                                                               oname(i + 1, P) + ("s" if t >= 20 else ""))
            parts.append(msg); regs.append(msg); carry = t // 10
        else:
            parts.append("%s: %s = %d." % (P_, expr, t) if len(col) > 1 or carry else "%s: bring down %d." % (P_, t))
            carry = 0
    total = back(sum(ints), P)
    head = "Line up the decimal points. " + annex_note(nums, P)
    if len(nums) == 2:
        end = " Answer: %s. Check: %s − %s = %s." % (nice(total), nice(total), nums[1], nums[0])
    else:
        end = " Answer: %s." % nice(total)
    if not compact:
        return (head + " " + " ".join(parts) + end).replace("  ", " ")
    rest = " The other places add without regrouping." if len(regs) < k else ""
    if not regs:
        return (head + " No place makes 10 or more." + end).replace("  ", " ")
    return (head + " " + " ".join(regs) + rest + end).replace("  ", " ")


def sub_steps(a, b, compact=None):
    P, (A, B) = scale([a, b])
    k = nlen(A)
    if compact is None:
        compact = k >= 5
    d, db = digits(A, k), digits(B, k)
    kb = nlen(B)
    parts, regs = [], []
    for i in range(k):
        P_ = cap(pname(i, P))
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                old = d[j]
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d needs a regroup, but the next place is 0. Regroup 1 %s: the %s become %d, "
                       "each 0 becomes 9, and the %s become %d. %d − %d = %d."
                       % (P_, cur, db[i], oname(j, P), pname(j, P), old - 1, pname(i, P), d[i], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d needs a regroup. 1 %s becomes 10 %s: %d − %d = %d."
                       % (P_, cur, db[i], oname(i + 1, P), pname(i, P), d[i], db[i], d[i] - db[i]))
            parts.append(msg); regs.append(msg)
        elif i >= kb and i >= P:
            if d[i] or i < k - 1:
                parts.append("%s: bring down %d." % (P_, d[i]))
        else:
            parts.append("%s: %d − %d = %d." % (P_, d[i], db[i], d[i] - db[i]))
    r = back(A - B, P)
    head = "Line up the decimal points. " + annex_note([a, b], P)
    end = " Answer: %s. Check: %s + %s = %s." % (nice(r), nice(r), b, a)
    if not compact:
        return (head + " " + " ".join(parts) + end).replace("  ", " ")
    rest = " The other places subtract without regrouping." if len(regs) < k else ""
    return (head + " " + " ".join(regs) + rest + end).replace("  ", " ")


# ------------------------------------------------------------ typical mistakes (each returns a Decimal or text, or None)
def col_info(ints):
    k = max(nlen(x) for x in ints)
    ds = [digits(x, k) for x in ints]
    sums, carries, c = [], [], 0
    for i in range(k):
        s = sum(d[i] for d in ds)
        sums.append(s)
        t = s + c
        c = t // 10
        carries.append(c)
    return k, sums, carries


def add_right_align(nums):
    """Lined up the last digits instead of the decimal points: 3.6 + 2.45 = 2.81."""
    if len({dec(n) for n in nums}) == 1:
        return None
    P = max(dec(n) for n in nums)
    return back(sum(int(n.replace(".", "")) for n in nums), P)


def add_left_align(nums):
    """Lined up the first digits: 24 + 3.24 read as 2.4 + 3.24 = 5.64 (only two numbers with different whole parts)."""
    if len(nums) != 2:
        return None
    la, lb = [len(n.split(".")[0]) for n in nums]
    if la == lb or Decimal(nums[0]) < 1 or Decimal(nums[1]) < 1:
        return None
    a, b = Decimal(nums[0]), Decimal(nums[1])
    if la > lb:
        a = a.scaleb(lb - la)
    else:
        b = b.scaleb(la - lb)
    r = a + b
    return r if dec(nice(r)) <= 2 else None


def add_forgot_point_carry(nums):
    """Did not regroup 10 tenths as 1 one (forgot the 1 that crosses the decimal point)."""
    P, ints = scale(nums)
    if P == 0:
        return None
    k, sums, carries = col_info(ints)
    c = carries[P - 1]
    if not c:
        return None
    return back(sum(ints) - c * 10 ** P, P)


def add_forgot_carry(nums, which):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints)
    cols = [i for i in range(k - 1) if carries[i] and i != P - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return back(sum(ints) - carries[i] * 10 ** (i + 1), P)


def add_no_carry(nums):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints)
    if not any(carries[:k - 1]):
        return None
    return back(sum((sums[i] % 10 if i < k - 1 else sums[i]) * 10 ** i for i in range(k)), P)


def add_concat(nums):
    """Wrote a two-digit column total in place: 0.8 + 0.45 = 0.125. Only when exactly one column regroups."""
    P, ints = scale(nums)
    if P == 0:
        return None
    k, sums, carries = col_info(ints)
    k2 = max(k, P + 1)
    sums = sums + [0] * (k2 - k)
    over = [i for i in range(k2) if sums[i] >= 10]
    if len(over) != 1 or over[0] == k2 - 1 or any(sums[i] >= 10 for i in range(over[0])):
        return None
    ip = "".join(str(sums[j]) for j in range(k2 - 1, P - 1, -1)).lstrip("0") or "0"
    fp = "".join(str(sums[j]) for j in range(P - 1, -1, -1))
    return ip + "." + fp


def add_extra_one(nums):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints)
    return [back(sum(ints) + 10 ** (i + 1), P) for i in range(k - 1) if not carries[i]]


def point_shift(val, P):
    """Put the point one place off (counted the places of only one number)."""
    return [Decimal(val) * 10, Decimal(val) / 10] if P else []


def no_point(val):
    t = nice(val).replace(",", "")
    return Decimal(t.replace(".", "")) if "." in t else None


def add_cands(nums):
    P, ints = scale(nums)
    total = back(sum(ints), P)
    c = [add_right_align(nums), add_left_align(nums), add_forgot_point_carry(nums), add_concat(nums), add_no_carry(nums),
         add_forgot_carry(nums, "first"), add_forgot_carry(nums, "last")]
    c += add_extra_one(nums)
    if len(nums) == 2:
        c.append(abs(Decimal(nums[0]) - Decimal(nums[1])))
    c += point_shift(total, P)
    return c


def borrow_digits(A, B):
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return d


def sub_no_annex(a, b):
    """Did not write the zeros: brought the extra digits of b down. 5 − 2.37 = 3.37, 8.2 − 3.45 = 4.85."""
    pa, pb = dec(a), dec(b)
    if pa >= pb:
        return None
    bt = Decimal(b).quantize(Decimal(1).scaleb(-pa), rounding="ROUND_DOWN")
    head = Decimal(a) - bt
    if head < 0:
        return None
    return head + (Decimal(b) - bt)


def sub_small_from_big(a, b):
    P, (A, B) = scale([a, b])
    k = nlen(A)
    da, db = digits(A, k), digits(B, k)
    return back(sum(abs(da[i] - db[i]) * 10 ** i for i in range(k)), P)


def sub_forgot_reduce(a, b, only_first=False):
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    out, done = 0, False
    for i in range(k):
        if d[i] < db[i]:
            if only_first and done:
                j = i + 1
                while d[j] == 0:
                    j += 1
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
            else:
                d[i] += 10
                done = True
        out += (d[i] - db[i]) * 10 ** i
    return back(out, P)


def sub_zero_as_ten(a, b):
    """Regrouping across a zero: made the zero 10 instead of 9. 5.00 − 2.37 = 2.73."""
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
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
    return back(sum((d[i] - db[i]) * 10 ** i for i in range(k)), P)


def sub_right_align(a, b):
    if dec(a) == dec(b):
        return None
    P = max(dec(a), dec(b))
    r = int(a.replace(".", "")) - int(b.replace(".", ""))
    return back(r, P) if r > 0 else None


def regroups_sub(a, b):
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    n = 0
    for i in range(k):
        if d[i] < db[i]:
            n += 1
            d[i] += 10
            d[i + 1] -= 1
    return n


def sub_cands(a, b):
    r = Decimal(a) - Decimal(b)
    P = max(dec(a), dec(b))
    return ([sub_no_annex(a, b), sub_small_from_big(a, b), sub_zero_as_ten(a, b), sub_forgot_reduce(a, b),
             sub_forgot_reduce(a, b, only_first=True), sub_right_align(a, b), Decimal(a) + Decimal(b)]
            + point_shift(r, P))


# ------------------------------------------------------------ helpers
def fmt_all(vals, f=nice):
    out = []
    for v in vals:
        if v is None:
            continue
        if isinstance(v, str):
            out.append(v)
        elif v > 0:
            out.append(f(v))
    return out


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c in ("0", "$0.00"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger (hundredths grids) so every square can be counted."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures: columns with the points lined up
def column_svg(nums, op, answer=None, ghost=False, marks=False, fs=28):
    """Numbers in columns, decimal points in one narrow slot so every place lines up.
    ghost: write the missing zeros (and point) in gray.  answer: write the answer row.
    marks: red regroup marks (carried 1s, or crossed digits with the new digit above)."""
    rows = list(nums) + ([answer] if answer else [])
    for r in rows:
        assert Decimal(r) < 1000, r
    P = max(dec(r) for r in rows)
    I = max(len(r.split(".")[0]) for r in rows)
    cw = fs * (0.82 if marks else 0.64)
    kw = cw * 0.53
    pad_l = cw * 1.3 + 10
    # slot centres: places I-1 .. 0, point, -1 .. -P
    xs, x = {}, pad_l
    for p in range(I - 1, -1, -1):
        xs[p] = x + cw / 2
        x += cw
    if P:
        xs["pt"] = x + kw / 2
        x += kw
        for p in range(-1, -P - 1, -1):
            xs[p] = x + cw / 2
            x += cw
    W = int(x + 10)
    top = 8 + (int(fs * 0.6) if marks else 0)
    s = []

    def ch(c, cx, y, color, size=fs):
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>%s</text>" % (cx, y, size, color, c))

    def put(t, y, color):
        ip, _, fp = t.partition(".")
        for n, c in enumerate(reversed(ip)):
            ch(c, xs[n], y, color)
        if "." in t:
            ch(".", xs["pt"], y, color)
        elif ghost and P:
            ch(".", xs["pt"], y, GHOST)
        for n in range(P):
            if n < len(fp):
                ch(fp[n], xs[-n - 1], y, color)
            elif ghost:
                ch("0", xs[-n - 1], y, GHOST)

    ys = [top + fs + int(n * fs * 1.15) for n in range(len(nums))]
    for t, y in zip(nums, ys):
        put(t, y, INK)
    sign_x = pad_l - cw * 0.6
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, ys[-1], fs, GREEN, "+" if op == "+" else "−"))
    ly = ys[-1] + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.5, ly, W - 8, ly, INK))
    H = ly + 10
    if answer:
        put(answer, ly + fs + 6, GREEN)
        H = ly + fs + 14
    if marks:
        sm = int(fs * 0.55)
        Pn, ints = scale(nums)
        assert Pn == P
        place_x = [xs[i - P] for i in range(I + P)]          # smallest place first
        if op == "+":
            k, sums, carries = col_info(ints)
            for i in range(k - 1):
                if carries[i] and i + 1 < len(place_x):
                    ch(str(carries[i]), place_x[i + 1], top - 4, RED, sm)
        else:
            A, B = ints
            nd = borrow_digits(A, B)
            od = digits(A, nlen(A))
            for i in range(nlen(A)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    y1 = ys[0]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    ch(str(nd[i]), x, top - 4, RED, sm if nd[i] < 10 else int(sm * 0.85))
    label = "%s written in columns with the decimal points lined up" % (" plus " if op == "+" else " minus ").join(nums)
    return svg_wrap(W, H, "".join(s), label)


def wrong_column_svg(nums, op, wrong, fs=28):
    """A student's work with the LAST digits lined up (points not lined up), and the wrong answer."""
    cw, kw = fs * 0.64, fs * 0.34
    rows = list(nums) + [wrong]

    def width(t):
        return sum(kw if c == "." else cw for c in t)
    longest = max(width(r) for r in rows)
    pad_l = cw * 1.3 + 10
    right = pad_l + longest
    W = int(right + 10)
    s = []

    def put(t, y, color):
        x = right
        for c in reversed(t):
            w = kw if c == "." else cw
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (x - w / 2, y, fs, color, c))
            x -= w
    ys = [8 + fs + int(n * fs * 1.15) for n in range(len(nums))]
    for t, y in zip(nums, ys):
        put(t, y, INK)
    sign_x = pad_l - cw * 0.6
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, ys[-1], fs, GREEN, "+" if op == "+" else "−"))
    ly = ys[-1] + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.5, ly, W - 8, ly, INK))
    put(wrong, ly + fs + 6, RED)
    H = ly + fs + 14
    label = "%s written with the last digits lined up and the answer %s" % ((" plus " if op == "+" else " minus ").join(nums), wrong)
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ pictures: hundredths grids
def grid_body(ox, oy, cell, color_of, crossed):
    s = []
    for c in range(10):
        for r in range(10):
            col = color_of(c * 10 + r)
            if col:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (ox + c * cell, oy + r * cell, cell, cell, col))
    for i in range(1, 10):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox + i * cell, oy, ox + i * cell, oy + 10 * cell, THIN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (ox, oy + i * cell, ox + 10 * cell, oy + i * cell, THIN))
    for c in range(10):
        for r in range(10):
            if crossed(c * 10 + r):
                x0, y0 = ox + c * cell + 3, oy + r * cell + 3
                x1, y1 = x0 + cell - 6, y0 + cell - 6
                s.append("<path d='M%d %dL%d %dM%d %dL%d %d' stroke='%s' stroke-width='2'/>"
                         % (x0, y0, x1, y1, x1, y0, x0, y1, RED))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
             % (ox, oy, 10 * cell, 10 * cell, INK))
    return "".join(s)


def grid_svg(first, second=0, cross=0, cell=17):
    """Hundredths grid(s). `first` squares green, then `second` squares yellow (full columns first,
    then down the next column). cross: the last `cross` shaded squares get a red X (taken away).
    More than 100 squares continue on a second grid."""
    total = first + second
    n = max(1, (total + 99) // 100)
    pad, gap = 4, 22
    g = 10 * cell
    W = 2 * pad + n * g + (n - 1) * gap
    H = 2 * pad + g
    s = []
    for k in range(n):
        base = k * 100

        def color_of(i, base=base):
            j = base + i
            return FILL if j < first else (FILL2 if j < total else None)

        def crossed(i, base=base):
            j = base + i
            return total - cross <= j < total

        s.append(grid_body(pad + k * (g + gap), pad, cell, color_of, crossed))
    if cross:
        lab = "hundredths grid%s with %d squares shaded and %d crossed out" % ("s" if n > 1 else "", first, cross)
    elif second:
        lab = "hundredths grid%s with %d green squares and %d yellow squares" % ("s" if n > 1 else "", first, second)
    else:
        lab = "hundredths grid with %d squares shaded" % first
    return svg_wrap(W, H, "".join(s), lab)


# ============================================================ set 1: models
def hund(s):
    h = int(Decimal(s) * 100)
    return "1 hundredth" if h == 1 else "%d hundredths" % h


def set_models(P):
    its = []
    for a, b in [("0.2", "0.56"), ("0.17", "0.6"), ("0.5", "0.38"), ("0.3", "0.09"), ("0.06", "0.7"),
                 ("0.25", "0.5"), ("0.43", "0.3"), ("0.12", "0.8"), ("0.7", "0.24")]:
        A, B = int(Decimal(a) * 100), int(Decimal(b) * 100)
        tot = Decimal(a) + Decimal(b)
        assert tot < 1
        g, y = (a, b) if A % 10 == 0 else (b, a)          # whole columns first, so both parts are easy to count
        q = (fig(grid_svg(int(Decimal(g) * 100), int(Decimal(y) * 100))) +
             "The grid is 1 whole. The green part is %s and the yellow part is %s. What is %s + %s?" % (g, y, a, b))
        ra = add_right_align([a, b])
        tenth = a if dec(a) == 1 else b
        e = ("Each small square is 0.01 and each column is 0.1. %s = %s and %s = %s. Together: %d + %d = %d hundredths = <b>%s</b>. "
             "Do not add the digits as if they were the same place: %s is %s, not %d."
             % (a, hund(a), b, hund(b), A, B, A + B, nice(tot), tenth, hund(tenth), int(Decimal(tenth) * 10)))
        its.append(mcq(q, nice(tot), fmt_all([ra, 1 - tot, tot * 10, no_point(tot)]), e))
    for a, b in [("0.8", "0.45"), ("0.65", "0.7"), ("0.9", "0.36")]:
        A, B = int(Decimal(a) * 100), int(Decimal(b) * 100)
        tot = Decimal(a) + Decimal(b)
        g, y = (a, b) if A % 10 == 0 else (b, a)
        q = (fig(grid_svg(int(Decimal(g) * 100), int(Decimal(y) * 100))) +
             "Each grid is 1 whole. The green part is %s and the yellow part is %s. What is %s + %s?" % (g, y, a, b))
        e = ("%s + %s = %d + %d = %d hundredths. 100 hundredths fill one whole grid, so the sum is 1 whole and %s = <b>%s</b>. "
             "The sum is more than 1, so 0.%d is too small."
             % (hund(a), hund(b), A, B, A + B, hund(nice(tot - 1)), nice(tot), int(add_concat([a, b]).split(".")[1])))
        its.append(mcq(q, nice(tot), fmt_all([add_concat([a, b]), add_right_align([a, b]), tot * 10, 2 - tot]), e))
    for a, b in [("0.75", "0.3"), ("0.9", "0.25"), ("0.68", "0.4"), ("1.2", "0.45")]:
        A, B = int(Decimal(a) * 100), int(Decimal(b) * 100)
        r = Decimal(a) - Decimal(b)
        whole = "Each grid is 1 whole." if A > 100 else "The grid is 1 whole."
        q = (fig(grid_svg(A, 0, cross=B)) + "%s %s is shaded. The squares with an X are taken away. What is %s − %s?"
             % (whole, a, a, b))
        e = ("%s is %s. Taking away %s (%s) leaves %d − %d = %d hundredths: the squares without an X. %s − %s = <b>%s</b>."
             % (a, hund(a), b, hund(b), A, B, A - B, a, b, nice(r)))
        its.append(mcq(q, nice(r), fmt_all(sub_cands(a, b)[:1] + [sub_right_align(a, b), Decimal(b), Decimal(a) + Decimal(b)]
                                           + sub_cands(a, b)), e))
    its.append(mcq("To add 0.6 + 0.27, you can write 0.6 in hundredths. 0.6 is the same as how many hundredths?",
                   "60 hundredths", ["6 hundredths", "600 hundredths", "60 tenths"],
                   "0.6 is 6 tenths, and each tenth is 10 hundredths, so 0.6 = 0.60 = <b>60 hundredths</b>. "
                   "Then 0.6 + 0.27 = 60 + 27 = 87 hundredths = 0.87."))
    its.append(mcq("What number goes in the box?  <b>0.35 + ☐ = 1</b>", "0.65", ["0.75", "0.64", "1.35"],
                   "1 whole is 100 hundredths and 0.35 is 35 hundredths. 100 − 35 = 65 hundredths = <b>0.65</b>. "
                   "Check: 0.35 + 0.65 = 1. (0.75 is wrong: 0.35 + 0.75 = 1.1.)"))
    its.append(mcq("What is 0.6 + 0.4?", "1", ["0.10", "0.2", "10"],
                   "6 tenths + 4 tenths = 10 tenths. 10 tenths make <b>1 whole</b>, so 0.6 + 0.4 = 1. "
                   "Writing 0.10 forgets to regroup: 0.10 is only 1 tenth."))
    its.append(mcq("What is 0.9 + 0.3?", "1.2", ["0.12", "0.6", "12"],
                   "9 tenths + 3 tenths = 12 tenths. 10 tenths make 1 whole, so 12 tenths = 1 whole and 2 tenths = <b>1.2</b>. "
                   "0.12 is wrong: it puts 12 in the tenths place without regrouping."))
    return {"title": "Add and subtract with hundredths grids", "items": its}


# ============================================================ column questions
def item_add(nums, col):
    tot = sum(Decimal(n) for n in nums)
    if col:
        q = fig(column_svg(nums, "+")) + "Add."
    else:
        q = "What is %s?" % " + ".join(nums)
    return mcq(q, nice(tot), fmt_all(add_cands(nums)), add_steps(nums))


def item_sub(a, b, col):
    r = Decimal(a) - Decimal(b)
    q = (fig(column_svg([a, b], "-")) + "Subtract.") if col else "What is %s − %s?" % (a, b)
    return mcq(q, nice(r), fmt_all(sub_cands(a, b)), sub_steps(a, b))


def rnd_num(rnd, ip_digits, places):
    """A random number: ip_digits digits before the point (0 means 0.xx), `places` digits after, last digit not 0."""
    ip = 0 if ip_digits == 0 else rnd.randint(10 ** (ip_digits - 1), 10 ** ip_digits - 1)
    if places == 0:
        return str(ip)
    fp = rnd.randint(1, 10 ** places - 1)
    while fp % 10 == 0:
        fp = rnd.randint(1, 10 ** places - 1)
    return "%d.%0*d" % (ip, places, fp)


def ok_result(v):
    return Decimal(v) == Decimal(nice(v)) and v > 0


def pick_pair(rnd, seen, shapes, cond):
    while True:
        (ia, pa), (ib, pb) = shapes if isinstance(shapes[0][0], int) else rnd.choice(shapes)
        a, b = rnd_num(rnd, ia, pa), rnd_num(rnd, ib, pb)
        if rnd.random() < 0.5:
            a, b = b, a
        if Decimal(a) == 0 or Decimal(b) == 0 or (a, b) in seen or (b, a) in seen:
            continue
        if not cond(a, b):
            continue
        seen.add((a, b))
        return a, b


def tail_ok(a, b, op):
    """The answer must not end in 0 after the point (so 3.80 never has to be compared with 3.8)."""
    P = max(dec(a), dec(b))
    r = Decimal(a) + Decimal(b) if op == "+" else Decimal(a) - Decimal(b)
    if r <= 0:
        return False
    if P == 0:
        return True
    return dec(nice(r)) == P


def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("To add 3.6 + 2.45, you write 3.6 with two decimal places. Which number is equal to 3.6?",
                   "3.60", ["3.06", "0.36", "36.0"],
                   "A zero at the end of a decimal does not change its value: 3.6 = 3 ones and 6 tenths = <b>3.60</b>. "
                   "3.06 is wrong: it moves the 6 to the hundredths place."))
    its.append(mcq("To find 12 + 4.75, you can write 12 with a decimal point. Which number is equal to 12?",
                   "12.00", ["0.12", "1.2", "120"],
                   "A whole number has its decimal point after the ones digit, so 12 = <b>12.00</b>. "
                   "Then the 2 ones sit over the 4 ones."))
    n, he, his = P.next()
    a, b = "3.6", "2.45"
    w = add_right_align([a, b])
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "6.05", fmt_all([w, add_forgot_point_carry([a, b]), Decimal("60.5")]),
                   "Line up the <b>decimal points</b>, not the last digits: 3.60 + 2.45. Hundredths: 0 + 5 = 5. "
                   "Tenths: 6 + 4 = 10, write 0 and regroup 1 one. Ones: 3 + 2 + 1 = 6. Answer: <b>6.05</b>. "
                   "Estimate: 4 + 2 = 6, so %s is far too small." % nice(w)))
    n, he, his = P.next()
    a, b = "15", "2.38"
    w = add_right_align([a, b])
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "17.38", fmt_all([w, Decimal("3.88"), Decimal("173.8")]),
                   "15 is a whole number, so its point is after the 5: 15 = 15.00 (not 1.5). Line up the points: 15.00 + 2.38. "
                   "Hundredths: 0 + 8 = 8. Tenths: 0 + 3 = 3. Ones: 5 + 2 = 7. Tens: bring down 1. Answer: <b>17.38</b>."))
    def cond(a, b):
        P_, ints = scale([a, b])
        k, sums, carries = col_info(ints)
        if dec(a) == dec(b) or not tail_ok(a, b, "+"):
            return False
        if P_ and carries[P_ - 1]:                   # no regroup across the point in this set
            return False
        return Decimal(a) + Decimal(b) < 100
    plan = [((1, 1), (1, 2))] * 3 + [((1, 2), (0, 1))] * 2 + [((0, 2), (1, 1))] * 2 + [((1, 0), (1, 2))] * 2 \
        + [((2, 1), (1, 2))] * 2 + [((2, 2), (1, 1))] * 2 + [((2, 0), (1, 2))] + [((2, 1), (2, 2))] * 2
    for i, sh in enumerate(plan):
        a, b = pick_pair(rnd, seen, sh, cond)
        its.append(item_add([a, b], i % 2 == 0))
    return {"title": "Line up the decimal points", "items": its}


def set_regroup(P, rnd, seen):
    its = []
    shapes = [((1, 2), (1, 2)), ((1, 1), (1, 2)), ((2, 2), (1, 2)), ((2, 1), (2, 2)), ((1, 2), (0, 2)),
              ((2, 2), (2, 2)), ((1, 1), (1, 1)), ((2, 1), (1, 2)), ((1, 0), (0, 2))]

    def cond(a, b):
        P_, ints = scale([a, b])
        k, sums, carries = col_info(ints)
        if not tail_ok(a, b, "+") or P_ == 0:
            return False
        if not carries[P_ - 1]:                      # must regroup across the point
            return False
        return Decimal(a) + Decimal(b) < 200
    its.append(item_add(["4.78", "2.56"], True))
    seen.add(("4.78", "2.56"))
    for i in range(16):
        a, b = pick_pair(rnd, seen, shapes, cond)
        its.append(item_add([a, b], i % 2 == 1))
    for nums in [["2.5", "1.75", "0.8"], ["6.48", "3.9", "12.35"], ["0.65", "4.7", "2.08"]]:
        assert ok_result(sum(Decimal(n) for n in nums)) and dec(nice(sum(Decimal(n) for n in nums))) == 2
        its.append(item_add(nums, False))
    return {"title": "Add with regrouping", "items": its}


def set_subtract(P, rnd, seen):
    its = []
    its.append(mcq("To find 5 − 2.37, how should you write 5 so both numbers have hundredths?", "5.00",
                   ["0.05", "5.37", "500"],
                   "5 is 5 ones, and its decimal point is after the 5. Write <b>5.00</b>: two zeros hold the tenths and "
                   "hundredths places. Then 5.00 − 2.37 = 2.63."))
    n, he, his = P.next()
    its.append(mcq("%s found 8.2 − 3.45 = 4.75. Which addition checks %s answer?" % (n, his),
                   "4.75 + 3.45 = 8.2", ["4.75 − 3.45 = 1.3", "8.2 + 3.45 = 11.65", "4.75 + 8.2 = 12.95"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 4.75 + 3.45 = 8.20 = 8.2. "
                   "You get back the starting number, so %s answer is right." % his))
    fixed_pairs = [("5", "2.37"), ("8.2", "3.45"), ("10", "4.65"), ("6.03", "2.48"), ("7.4", "2.85"), ("12", "7.08")]
    for a, b in fixed_pairs:
        seen.add((a, b))
    shapes = [((1, 2), (1, 2)), ((1, 1), (1, 2)), ((2, 1), (1, 2)), ((2, 2), (1, 2)), ((1, 0), (1, 2)),
              ((2, 0), (1, 1)), ((2, 2), (2, 2)), ((1, 1), (0, 2)), ((2, 1), (1, 1))]

    def cond(a, b):
        if Decimal(a) <= Decimal(b) or not tail_ok(a, b, "-"):
            return False
        return regroups_sub(a, b) >= 1 and Decimal(a) - Decimal(b) > Decimal("0.5")
    pairs = list(fixed_pairs)
    while len(pairs) < 18:
        a, b = pick_pair(rnd, seen, shapes, cond)
        pairs.append((a, b))
    for i, (a, b) in enumerate(pairs):
        its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Subtract decimals and write zeros", "items": its}


# ============================================================ set 5: word problems
def story_add(q, nums, unit, lead, is_money=False):
    tot = sum(Decimal(n) for n in nums)
    if is_money:
        c = [money(v) for v in add_cands(nums) if v is not None and not isinstance(v, str) and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(tot), c, lead + " " + add_steps(nums))
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (c, unit) for c in fmt_all(add_cands(nums))], lead + " " + add_steps(nums))


def story_sub(q, a, b, unit, lead, is_money=False):
    r = Decimal(a) - Decimal(b)
    if is_money:
        c = [money(v) for v in sub_cands(a, b) if v is not None and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(r), c, lead + " " + sub_steps(a, b))
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (c, unit) for c in fmt_all(sub_cands(a, b))], lead + " " + sub_steps(a, b))


def set_words(P):
    its = []
    n, he, his = P.next()
    its.append(story_add("%s bought a book for $8.75 and a pen for $1.49. How much did %s spend?" % (n, he),
                         ["8.75", "1.49"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("%s paid for a $13.68 lunch with a $20 bill. How much change did %s get?" % (n, he),
                         "20", "13.68", "", "Change is what is left: subtract.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("A ribbon is 2.5 meters long. %s cuts off 0.75 meters for a bow. How much ribbon is left?" % n,
                         "2.5", "0.75", "meters", "Take the part cut off away: subtract."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("In a 100-meter race, %s ran it in 14.62 seconds and %s ran it in 13.9 seconds. "
                         "How many seconds faster was %s?" % (n1, n2, n2),
                         "14.62", "13.9", "seconds", "The faster runner has the smaller time. Find the difference: subtract."))
    its.append(story_add("It rained 2.36 inches on Monday and 1.8 inches on Tuesday. How much did it rain on the two days?",
                         ["2.36", "1.8"], "inches", "Put the two days together: add."))
    n, he, his = P.next()
    its.append(story_add("%s's puppy weighed 4.6 kilograms. In a month, it gained 0.85 kilograms. How much does the puppy weigh now?" % n,
                         ["4.6", "0.85"], "kilograms", "The puppy got heavier: add."))
    n, he, his = P.next()
    its.append(story_sub("In the long jump, %s jumped 3.8 meters on %s first try and 3.45 meters on %s second try. "
                         "How much longer was the first jump?" % (n, his, his),
                         "3.8", "3.45", "meters", "How much longer means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_add("In gymnastics, %s scored 9.35 on the beam and 8.9 on the floor. What was %s total score?" % (n, his),
                         ["9.35", "8.9"], "points", "Total means add."))
    n, he, his = P.next()
    its.append(story_sub("A bottle holds 1.5 liters of water. %s drinks 0.35 liters. How much water is left in the bottle?" % n,
                         "1.5", "0.35", "liters", "Take away what %s drank: subtract." % he))
    its.append(story_add("A family drove 125.6 miles before lunch and 87.45 miles after lunch. How far did they drive in all?",
                         ["125.6", "87.45"], "miles", "In all means add."))
    n, he, his = P.next()
    its.append(story_sub("A normal body temperature is 98.6°F. %s has a fever of 101.2°F. How many degrees above normal is %s temperature?" % (n, his),
                         "101.2", "98.6", "degrees", "How many degrees above means find the difference: subtract."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_add("In a relay race, %s ran the first lap in 32.48 seconds and %s ran the second lap in 29.75 seconds. "
                         "What was their total time?" % (n1, n2), ["32.48", "29.75"], "seconds", "Total time means add the two laps."))
    # two-step stories
    a, b, c = Decimal("25"), Decimal("8.49"), Decimal("6.75")
    n, he, his = P.next()
    its.append(mcq("%s has $25. %s buys a puzzle for $8.49 and a kite for $6.75. How much money does %s have left?" % (n, cap(he), he),
                   money(a - b - c), [money(sub_no_annex("25", "15.24")), money(b + c), money(a - b)],
                   "Step 1, money spent: $8.49 + $6.75 = $15.24. Step 2, money left: $25.00 − $15.24 = $9.76. "
                   "Check: $9.76 + $15.24 = $25.00."))
    assert a - b - c == Decimal("9.76") and b + c == Decimal("15.24")
    a, b, c = Decimal("3.2"), Decimal("1.45"), Decimal("0.9")
    assert a - b - c == Decimal("0.85")
    its.append(mcq("A swim team relay is 3.2 kilometers in all. The first swimmer swims 1.45 kilometers and the second swims 0.9 kilometers. "
                   "How far does the third swimmer have to swim?", "0.85 kilometers",
                   ["2.35 kilometers", "1.75 kilometers", "1.66 kilometers"],
                   "Step 1, first two swimmers: 1.45 + 0.9 = 2.35 kilometers. Step 2, the rest: 3.20 − 2.35 = <b>0.85 kilometers</b>. "
                   "(1.66 is wrong: it lines up the last digits, 1.45 + 0.9 = 1.54, instead of the decimal points.)"))
    assert Decimal("3.2") - (Decimal("1.45") + Decimal("0.09")) == Decimal("1.66")
    # missing numbers
    assert sub_no_annex("6", "2.45") == Decimal("4.45") and sub_zero_as_ten("6", "2.45") == Decimal("3.65")
    its.append(mcq("What number goes in the box?  <b>☐ + 2.45 = 6</b>", "3.55", ["4.45", "3.65", "8.45"],
                   "Use subtraction: 6 − 2.45 = 6.00 − 2.45 = <b>3.55</b>. Check: 3.55 + 2.45 = 6.00 = 6. "
                   "(4.45 forgets to write the zeros: 6 − 2 = 4, then brings down .45.)"))
    assert Decimal(6) - Decimal("2.45") == Decimal("3.55")
    its.append(mcq("What number goes in the box?  <b>7.3 − ☐ = 4.68</b>", "2.62", fmt_all(sub_cands("7.3", "4.68")),
                   "Think: 7.3 − ? = 4.68. The missing part is 7.30 − 4.68 = <b>2.62</b>. Check: 7.3 − 2.62 = 4.68."))
    assert Decimal("7.3") - Decimal("4.68") == Decimal("2.62") and Decimal("7.3") - Decimal("2.62") == Decimal("4.68")
    # estimate to check (nearest whole number)
    for a, b, op in [("6.82", "3.29", "+"), ("12.15", "4.9", "−"), ("8.47", "5.6", "+")]:
        A, B = Decimal(a), Decimal(b)
        ra, rb = int(A.quantize(Decimal(1), rounding="ROUND_HALF_UP")), int(B.quantize(Decimal(1), rounding="ROUND_HALF_UP"))
        est = ra + rb if op == "+" else ra - rb
        exact = A + B if op == "+" else A - B
        fa, fb, ca, cb = int(A), int(B), int(A) + 1, int(B) + 1
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        trunc, other = f(fa, fb), (ra - rb if op == "+" else ra + rb)
        assert est != trunc and est != other
        its.append(mcq("Round each number to the nearest whole number. Which is the best estimate for %s %s %s?" % (a, op, b),
                       "about %d" % est, ["about %d" % v for v in [trunc, other, f(ca, cb), f(ca, fb), f(fa, cb)]],
                       "%s rounds to %d and %s rounds to %d. %d %s %d = <b>%d</b>. The exact answer, %s, is close to %d."
                       % (a, ra, b, rb, ra, op, rb, est, nice(exact), est)))
    n, he, his = P.next()
    w = add_right_align(["3.6", "2.45"])
    its.append(mcq("%s added 3.6 + 2.45 and got %s. Round each number to the nearest whole number to check. What does the estimate show?"
                   % (n, nice(w)), "It is too small", ["It is reasonable", "It is too big", "It is exactly right"],
                   "3.6 rounds to 4 and 2.45 rounds to 2, so the sum should be about 4 + 2 = 6. %s is much smaller than 6, "
                   "so it is <b>too small</b>. %s lined up the last digits. The correct sum is 3.60 + 2.45 = 6.05." % (nice(w), n)))
    assert len(its) == 20, len(its)
    return {"title": "Word problems and estimating", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("0.4") + Decimal("0.35") == Decimal("0.75")
    assert Decimal("3.6") + Decimal("2.45") == Decimal("6.05") and add_right_align(["3.6", "2.45"]) == Decimal("2.81")
    assert Decimal("4.78") + Decimal("2.56") == Decimal("7.34") and add_forgot_point_carry(["4.78", "2.56"]) == Decimal("6.34")
    assert Decimal(5) - Decimal("2.37") == Decimal("2.63") and sub_no_annex("5", "2.37") == Decimal("3.37")
    assert sub_zero_as_ten("5", "2.37") == Decimal("2.73")
    return (
        "<h2>The idea: line up the decimal points</h2>"
        "<p>Add and subtract decimals the same way as whole numbers, but first <b>line up the decimal points</b>. "
        "Then ones are under ones, tenths under tenths and hundredths under hundredths. "
        "You can only add digits that are the same place.</p>"
        "<h2>See it on a hundredths grid</h2>"
        "<p>A hundredths grid is 1 whole. One column is 0.1 and one small square is 0.01.</p>"
        "<figure class='sn-fig'>" + grid_svg(40, 35, cell=18) +
        "<figcaption>0.4 + 0.35: green 0.4 = 40 hundredths, yellow 0.35 = 35 hundredths. "
        "Together 40 + 35 = 75 hundredths = 0.75. Adding 4 + 35 = 39 would be wrong: 0.4 is 40 hundredths, not 4.</figcaption></figure>"
        "<h2>Write it in columns</h2>"
        "<p>Put the decimal points in one straight line. Then add from the right, just like whole numbers, "
        "and bring the decimal point straight down into the answer.</p>"
        "<figure class='sn-fig'>" + column_svg(["3.6", "2.45"], "+", answer="6.05", ghost=True, marks=True, fs=34) +
        "<figcaption>3.6 + 2.45: hundredths 0 + 5 = 5. Tenths 6 + 4 = 10, write 0 and regroup 1 one. "
        "Ones 3 + 2 + 1 = 6. Answer: 6.05.</figcaption></figure>"
        "<p>When a column makes 10 or more, regroup just as with whole numbers. 10 hundredths make 1 tenth, "
        "and 10 tenths make 1 one, so the 1 can cross the decimal point.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.78", "2.56"], "+", answer="7.34", marks=True, fs=34) +
        "<figcaption>4.78 + 2.56: hundredths 8 + 6 = 14, write 4 and regroup 1 tenth. "
        "Tenths 7 + 5 + 1 = 13, write 3 and regroup 1 one. Ones 4 + 2 + 1 = 7. Answer: 7.34.</figcaption></figure>"
        "<h2>Zeros hold the empty places</h2>"
        "<p>A zero at the end of a decimal does not change its value: 3.6 = 3.60 and 5 = 5.00. "
        "Write these zeros when a place is empty, most of all when you subtract. Then every digit on the bottom has a digit above it.</p>"
        "<figure class='sn-fig'>" + column_svg(["5", "2.37"], "-", answer="2.63", ghost=True, marks=True, fs=34) +
        "<figcaption>5 − 2.37 = 5.00 − 2.37. Regroup 1 one into 10 tenths, then 1 tenth into 10 hundredths: "
        "4 ones, 9 tenths and 10 hundredths. 10 − 7 = 3, 9 − 3 = 6, 4 − 2 = 2. Answer: 2.63.</figcaption></figure>"
        + ex("Example", "What is 8.2 − 3.45?",
             "Write 8.2 as 8.20. Hundredths: 0 − 5 needs a regroup, so 10 − 5 = 5. Tenths: 1 − 4 needs a regroup, so 11 − 4 = 7. "
             "Ones: 7 − 3 = 4.", "4.75") +
        "<h2>Estimate to check</h2>"
        "<p>Round each number to the nearest whole number and do the easy problem. "
        "3.6 + 2.45 is about 4 + 2 = 6, so 6.05 makes sense and 2.81 does not. "
        "You can also check a subtraction by adding back: 2.63 + 2.37 = 5.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (3.6 + 2.45 = 2.81)", "Line up the decimal points. Write 3.6 as 3.60"],
            ["Not writing the zeros (5 − 2.37 = 3.37)", "Write 5 as 5.00, then regroup to subtract"],
            ["Forgetting to regroup across the point (4.78 + 2.56 = 6.34)", "10 tenths make 1 one. Add the 1 to the ones"],
            ["Taking the smaller digit from the bigger one (8.2 − 3.45 = 5.25)", "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
            ["Writing 12 tenths after the point (0.8 + 0.45 = 0.125)", "10 tenths make 1 whole: 0.8 + 0.45 = 1.25"],
            ["Leaving out the decimal point (3.6 + 2.45 = 605)", "Bring the point straight down into the answer"],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract decimals?",
     "a": "Write the numbers in columns with the decimal points lined up, fill empty places with zeros, and add or subtract from the right like whole numbers. Then bring the decimal point straight down: 3.60 + 2.45 = 6.05."},
    {"q": "Why do you line up the decimal points?",
     "a": "Lining up the points puts ones under ones, tenths under tenths and hundredths under hundredths, so you only add digits of the same place. Lining up the last digits instead gives 3.6 + 2.45 = 2.81, which is wrong."},
    {"q": "How do you subtract a decimal from a whole number, like 5 − 2.37?",
     "a": "Write the whole number with a decimal point and zeros: 5 = 5.00. Then regroup and subtract: 5.00 − 2.37 = 2.63. Check by adding: 2.63 + 2.37 = 5."},
    {"q": "What does 5.NBT.B.7 mean for adding and subtracting decimals?",
     "a": "It is the Common Core standard for Grade 5: add, subtract, multiply and divide decimals to hundredths using models, place value and the link between addition and subtraction. This page covers adding and subtracting."},
]


def gen():
    rnd = random.Random(504)
    P = People(rnd)
    seen = set()
    sets = [set_models(P), set_line_up(P, rnd, seen), set_regroup(P, rnd, seen), set_subtract(P, rnd, set()), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "add-subtract-decimals", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add and Subtract Decimals",
        "seo_title": "Grade 5 Adding and Subtracting Decimals Worksheets: Line Up the Decimal Points, Regrouping, Zeros and Word Problems",
        "short_title": "Add and subtract decimals",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "5.NBT.B.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/NBT/B/7/",
        "standard_text": "Add, subtract, multiply, and divide decimals to hundredths, using concrete models or drawings and strategies based on place value, properties of operations, and/or the relationship between addition and subtraction; relate the strategy to a written method and explain the reasoning used.",
        "meta_desc": "Free Grade 5 worksheets for adding and subtracting decimals to hundredths: hundredths grid models, lining up the decimal points, regrouping, writing zeros like 5 = 5.00, estimating to check and money, measurement and sports word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Line up the decimal points. Then add or subtract like whole numbers.",
        "key_sub": "Write zeros in empty places (3.6 = 3.60, 5 = 5.00) so every digit has a partner. Regroup across the point when you need to, bring the point straight down, and estimate to check.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "hundredths grid")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
