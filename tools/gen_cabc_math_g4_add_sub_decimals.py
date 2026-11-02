# -*- coding: utf-8 -*-
"""
BC Grade 4 Math: Adding and Subtracting Decimals (BC Mathematics Curriculum, Computational fluency:
addition and subtraction of decimals to hundredths)
  python3 tools/gen_cabc_math_g4_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (4.5 + 2.37 -> 450 + 237 hundredths), so every regroup and every typical mistake is exact.
Canadian style: math, metre, litre, $ and the cent sign, no pennies (cash rounds to the nearest 5 cents),
4-digit numbers without a separator. Column helpers are copied from gen_ca_math_g6_add_sub_decimals.py,
grid pictures from gen_us_math_g5_add_sub_decimals.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
FILL = "#4fae74"       # first number on a model
FILL2 = "#f4c430"      # second number on a model
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]
PLACE = ["thousandths", "hundredths", "tenths", "ones", "tens", "hundreds", "thousands"]
ONE = ["thousandth", "hundredth", "tenth", "one", "ten", "hundred", "thousand"]


# ------------------------------------------------------------ numbers
def dec(s):
    """Decimal places as written: '3.6' -> 1, '5' -> 0."""
    return len(s.split(".")[1]) if "." in s else 0


def nice(d):
    """Shortest exact text for a Decimal (BC style: no separator below 10 000)."""
    d = Decimal(d)
    assert abs(d) < 10000, d
    t = format(d.normalize(), "f")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t


def fixed(d, p):
    """Decimal with exactly p places: fixed(5, 2) -> 5.00."""
    d = Decimal(d)
    assert abs(d) < 10000, d
    return format(d.quantize(Decimal(1).scaleb(-p)), "f")


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
    return PLACE[i + 3 - P]


def oname(i, P):
    return ONE[i + 3 - P]


def cap(s):
    return s[0].upper() + s[1:]


def annex_note(nums, P):
    """'Write 4.5 as 4.50.' for every number with fewer places."""
    w = ["%s as %s" % (n, fixed(Decimal(n), P)) for n in nums if dec(n) < P]
    if not w:
        return ""
    return "Write " + " and ".join(w) + "."


# ------------------------------------------------------------ column steps (explanations)
def add_steps(nums, compact=None):
    P, ints = scale(nums)
    k = max(nlen(x) for x in ints)
    if compact is None:
        compact = k >= 6
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
        compact = k >= 6
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
            if dec(v) <= 2:
                out.append(v)
        elif 0 < v < 10000 and dec(nice(v)) <= 2:      # Grade 4: tenths and hundredths only
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
    ghost: write the missing zeros (and point) in grey.  answer: write the answer row.
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



# ------------------------------------------------------------ pictures: tenths bars
def bars_svg(first, second=0, cross=0, cell=30, bh=34):
    """Tenths bars: each bar is 1 whole cut into 10 equal parts. `first` parts green, then `second` parts yellow.
    cross: the last `cross` shaded parts get a red X (taken away). More than 10 parts continue on the next bar."""
    total = first + second
    n = max(1, (total + 9) // 10)
    pad, gap = 4, 10
    W = 2 * pad + 10 * cell
    H = 2 * pad + n * bh + (n - 1) * gap
    s = []
    for k in range(n):
        oy = pad + k * (bh + gap)
        for i in range(10):
            j = k * 10 + i
            col = FILL if j < first else (FILL2 if j < total else None)
            x = pad + i * cell
            if col:
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x, oy, cell, bh, col))
        for i in range(1, 10):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>"
                     % (pad + i * cell, oy, pad + i * cell, oy + bh, THIN))
        for i in range(10):
            j = k * 10 + i
            if total - cross <= j < total:
                x0, y0 = pad + i * cell + 6, oy + 7
                x1, y1 = x0 + cell - 12, oy + bh - 7
                s.append("<path d='M%d %dL%d %dM%d %dL%d %d' stroke='%s' stroke-width='2.5'/>"
                         % (x0, y0, x1, y1, x1, y0, x0, y1, RED))
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (pad, oy, 10 * cell, bh, INK))
    if cross:
        lab = "tenths bar%s with %d parts shaded and %d crossed out" % ("s" if n > 1 else "", first, cross)
    elif second:
        lab = "tenths bar%s with %d green part%s and %d yellow part%s" % ("s" if n > 1 else "", first, "s" if first > 1 else "",
                                                                         second, "s" if second > 1 else "")
    else:
        lab = "tenths bar with %d parts shaded" % first
    return svg_wrap(W, H, "".join(s), lab)


def numline_svg(start, jump, op):
    """Number line 0 to 2 in tenths with one jump arc from start (tenths as integers)."""
    unit, pad = 18, 22
    W = 2 * pad + 20 * unit
    y = 70
    H = y + 34
    end = start + jump if op == "+" else start - jump
    assert 0 <= end <= 20 and 0 <= start <= 20
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (pad, y, pad + 20 * unit, y, INK)]
    for i in range(21):
        x = pad + i * unit
        big = i % 10 == 0
        mid = i % 5 == 0
        tl = 10 if big else (8 if mid else 6)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>" % (x, y - tl, x, y + tl, INK, "2.5" if big else "1.5"))
        if mid:
            lab = nice(Decimal(i) / 10)
            s.append("<text x='%d' y='%d' font-size='%d' fill='%s' text-anchor='middle' font-weight='%s'>%s</text>"
                     % (x, y + 30, 16, INK, "700" if big else "400", lab))
    x0, x1 = pad + start * unit, pad + end * unit
    xm = (x0 + x1) / 2
    top = y - 14 - 34
    s.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (x0, y - 4, xm, top, x1, y - 4, GREEN))
    d = 1 if x1 > x0 else -1
    s.append("<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (x1, y - 3, x1 - d * 11, y - 12, x1 - d * 2, y - 15, GREEN))
    s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (x0, y, GREEN))
    s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' fill='%s' text-anchor='middle'>%s%s</text>"
             % (xm, top + 10, GREEN, "+" if op == "+" else "−", nice(Decimal(jump) / 10)))
    lab = "number line from 0 to 2 in tenths with a jump of %s %s from %s" % (
        "plus" if op == "+" else "minus", nice(Decimal(jump) / 10), nice(Decimal(start) / 10))
    return svg_wrap(W, H, "".join(s), lab)


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
    """Hundredths grid(s), filled column by column. More than 100 squares continue on a second grid."""
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


# ============================================================ question builders
def cands_add(nums):
    tot = sum(Decimal(n) for n in nums)
    return add_cands(nums) + [no_point(tot)]


def cands_sub(a, b):
    r = Decimal(a) - Decimal(b)
    return sub_cands(a, b) + [no_point(r)]


def item_add(nums, col):
    tot = sum(Decimal(n) for n in nums)
    q = (fig(column_svg(nums, "+")) + "Add.") if col else "What is %s?" % " + ".join(nums)
    return mcq(q, nice(tot), fmt_all(cands_add(nums)), add_steps(nums))


def item_sub(a, b, col):
    r = Decimal(a) - Decimal(b)
    q = (fig(column_svg([a, b], "-")) + "Subtract.") if col else "What is %s − %s?" % (a, b)
    return mcq(q, nice(r), fmt_all(cands_sub(a, b)), sub_steps(a, b))


def rnd_num(rnd, ip_digits, places):
    """ip_digits digits before the point (0 means 0.xx), `places` digits after, last digit not 0."""
    ip = 0 if ip_digits == 0 else rnd.randint(10 ** (ip_digits - 1), 10 ** ip_digits - 1)
    if places == 0:
        return str(ip)
    fp = rnd.randint(1, 10 ** places - 1)
    while fp % 10 == 0:
        fp = rnd.randint(1, 10 ** places - 1)
    return "%d.%0*d" % (ip, places, fp)


def tail_ok(a, b, op):
    """The answer has exactly as many places as the longer number (no trailing zero to drop)."""
    P = max(dec(a), dec(b))
    r = Decimal(a) + Decimal(b) if op == "+" else Decimal(a) - Decimal(b)
    if r <= 0:
        return False
    return P == 0 or dec(nice(r)) == P


def add_regroups(nums):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints)
    return sum(1 for c in carries[:k - 1] if c)


def carry_point(a, b):
    P, ints = scale([a, b])
    k, sums, carries = col_info(ints)
    return bool(P and carries[P - 1])


def pick(rnd, seen, op, sa, sb, regroup, cond=lambda a, b: True):
    """A new pair. regroup False: no place needs a regroup. True: at least one place does."""
    for _ in range(20000):
        a, b = rnd_num(rnd, *sa), rnd_num(rnd, *sb)
        if op == "+" and rnd.random() < 0.5:
            a, b = b, a
        key = (op,) + tuple(sorted([a, b]))
        if key in seen or not tail_ok(a, b, op):
            continue
        if op == "-":
            if Decimal(a) - Decimal(b) < Decimal("0.5"):
                continue
            if (regroups_sub(a, b) > 0) != regroup:
                continue
        else:
            if Decimal(a) + Decimal(b) >= 100:
                continue
            if (add_regroups([a, b]) > 0) != regroup:
                continue
            if not regroup and max(col_info(scale([a, b])[1])[1]) >= 10:      # no column makes 10, not even the last
                continue
        if not cond(a, b):
            continue
        seen.add(key)
        return a, b
    raise RuntimeError((op, sa, sb, regroup))


def tenths(s):
    t = int(Decimal(s) * 10)
    return "1 tenth" if t == 1 else "%d tenths" % t


def hund(s):
    h = int(Decimal(s) * 100)
    return "1 hundredth" if h == 1 else "%d hundredths" % h


# ============================================================ set 1: tenths with models
def set_tenths(P):
    its = []
    # sums up to 1 with one bar
    for a, b in [("0.3", "0.4"), ("0.2", "0.5"), ("0.6", "0.3"), ("0.1", "0.7"), ("0.4", "0.4")]:
        A, B = int(Decimal(a) * 10), int(Decimal(b) * 10)
        tot = Decimal(a) + Decimal(b)
        assert tot < 1
        q = (fig(bars_svg(A, B)) + "The bar is 1 whole cut into 10 equal parts. The green part is %s and the yellow part is %s. "
             "What is %s + %s?" % (a, b, a, b))
        e = ("Each part is 1 tenth, or 0.1. %s is %s and %s is %s. Together: %d + %d = %d tenths = <b>%s</b>."
             % (a, tenths(a), b, tenths(b), A, B, A + B, nice(tot)))
        its.append(mcq(q, nice(tot), fmt_all([no_point(tot), tot / 10, abs(Decimal(a) - Decimal(b)), tot + Decimal("0.1"),
                                              tot - Decimal("0.1")]), e))
    # sums more than 1: two bars (the 0.6 + 0.5 = 0.11 mistake)
    for a, b in [("0.6", "0.5"), ("0.8", "0.7"), ("0.9", "0.4"), ("0.7", "0.6")]:
        A, B = int(Decimal(a) * 10), int(Decimal(b) * 10)
        tot = Decimal(a) + Decimal(b)
        assert 1 < tot < 2
        q = (fig(bars_svg(A, B)) + "Each bar is 1 whole. The green part is %s and the yellow part is %s. What is %s + %s?" % (a, b, a, b))
        e = ("%s + %s = %d + %d = %d tenths. 10 tenths fill one whole bar, so the sum is 1 whole and %s = <b>%s</b>. "
             "It is not %s: the sum is more than 1 whole, and %s is less than 1."
             % (tenths(a), tenths(b), A, B, A + B, tenths(nice(tot - 1)), nice(tot), add_concat([a, b]), add_concat([a, b])))
        its.append(mcq(q, nice(tot), fmt_all([add_concat([a, b]), no_point(tot), abs(Decimal(a) - Decimal(b)), tot + Decimal("0.1")]), e))
    # take away on bars
    for a, b in [("0.8", "0.3"), ("0.9", "0.4"), ("1.2", "0.5"), ("1.4", "0.6")]:
        A, B = int(Decimal(a) * 10), int(Decimal(b) * 10)
        r = Decimal(a) - Decimal(b)
        whole = "Each bar is 1 whole." if A > 10 else "The bar is 1 whole."
        q = (fig(bars_svg(A, 0, cross=B)) + "%s %s is shaded. The parts with an X are taken away. What is %s − %s?" % (whole, a, a, b))
        e = ("%s is %s. Take away %s (%s). The parts without an X are left: %d − %d = %d tenths. %s − %s = <b>%s</b>."
             % (a, tenths(a), b, tenths(b), A, B, A - B, a, b, nice(r)))
        if A > 10:
            e += " (Do not take the smaller digit from the bigger one: %s − %s is not %s.)" % (a, b, nice(sub_small_from_big(a, b)))
        its.append(mcq(q, nice(r), fmt_all([sub_small_from_big(a, b) if A > 10 else None, Decimal(a) + Decimal(b),
                                            no_point(r), r / 10, r + Decimal("0.1")]), e))
    # number lines
    assert Decimal("0.8") + Decimal("0.5") == Decimal("1.3")
    its.append(mcq(fig(numline_svg(8, 5, "+")) + "Start at 0.8 and jump 0.5 to the right. Where do you land? What is 0.8 + 0.5?",
                   "1.3", ["0.13", "1.2", "0.3"],
                   "Count on 5 tenths from 0.8: 0.9, 1, 1.1, 1.2, <b>1.3</b>. A jump of 0.2 gets to 1, then 0.3 more gets to 1.3. "
                   "(1.2 counts 0.8 as the first jump. 0.13 forgets that 10 tenths make 1.)"))
    assert Decimal("1.5") - Decimal("0.7") == Decimal("0.8")
    its.append(mcq(fig(numline_svg(15, 7, "-")) + "Start at 1.5 and jump 0.7 to the left. Where do you land? What is 1.5 − 0.7?",
                   "0.8", ["1.2", "2.2", "0.9"],
                   "Jump back 0.5 from 1.5 to get to 1. Then jump back 0.2 more: 1 − 0.2 = <b>0.8</b>. "
                   "Check: 0.8 + 0.7 = 1.5. (1.2 takes 5 from 7 instead of 7 from 15 tenths.)"))
    # ideas
    n, he, his = P.next()
    its.append(mcq("%s says 0.6 + 0.5 = 0.11. What is the correct answer?" % n, "1.1", ["0.11", "11", "1.01"],
                   "6 tenths + 5 tenths = 11 tenths. 10 tenths make 1 whole, so 11 tenths = 1 whole and 1 tenth = <b>1.1</b>. "
                   "0.11 is only 11 hundredths, which is less than 0.6 alone."))
    its.append(mcq("How many tenths are in 1.3?", "13 tenths", ["3 tenths", "130 tenths", "31 tenths"],
                   "1 whole is 10 tenths. 1.3 = 10 tenths + 3 tenths = <b>13 tenths</b>."))
    assert Decimal(1) - Decimal("0.4") == Decimal("0.6")
    its.append(mcq("What number goes in the box?  <b>0.4 + ☐ = 1</b>", "0.6", ["0.06", "1.4", "0.5"],
                   "1 whole is 10 tenths and 0.4 is 4 tenths. 10 − 4 = 6 tenths = <b>0.6</b>. Check: 0.4 + 0.6 = 1."))
    assert Decimal("2.4") + Decimal("1.3") == Decimal("3.7")
    its.append(mcq("What is 2.4 + 1.3?", "3.7", ["37", "0.37", "1.1"],
                   "Add ones to ones and tenths to tenths. Ones: 2 + 1 = 3. Tenths: 4 + 3 = 7 tenths. Answer: <b>3.7</b>. "
                   "Keep the decimal point: 37 drops it."))
    assert Decimal("3.5") - Decimal("1.8") == Decimal("1.7")
    its.append(mcq("What is 3.5 − 1.8?", "1.7", ["2.3", "5.3", "17"],
                   "Tenths: 5 − 8 needs a regroup. 1 one becomes 10 tenths: 15 − 8 = 7. Ones: 2 − 1 = 1. Answer: <b>1.7</b>. "
                   "Check: 1.7 + 1.8 = 3.5. (2.3 takes 5 from 8 instead of regrouping.)"))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract tenths with models", "items": its}


# ============================================================ set 2: line up the decimal points
def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("You add 3.42 + 5.17 in columns with the decimal points lined up. Which digit of 5.17 goes under the 4?",
                   "1", ["7", "5", "the decimal point"],
                   "The 4 in 3.42 is in the tenths place. Tenths go under tenths: the tenths digit of 5.17 is <b>1</b>. "
                   "(7 is the hundredths digit, so it goes under the 2.)"))
    its.append(mcq("To add 2.3 + 1.45, you write 2.3 with two decimal places. Which number is equal to 2.3?",
                   "2.30", ["2.03", "0.23", "23.0"],
                   "A zero at the end of a decimal does not change its value: 2.3 = 2 ones and 3 tenths = <b>2.30</b>. "
                   "2.03 is wrong: it moves the 3 to the hundredths place."))
    n, he, his = P.next()
    a, b = "4.5", "2.32"
    w = add_right_align([a, b])
    assert w == Decimal("2.77") and Decimal(a) + Decimal(b) == Decimal("6.82")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "6.82", ["2.77", "682", "6.37"],
                   "Line up the <b>decimal points</b>, not the last digits: 4.50 + 2.32. Hundredths: 0 + 2 = 2. "
                   "Tenths: 5 + 3 = 8. Ones: 4 + 2 = 6. Answer: <b>6.82</b>. Estimate: 5 + 2 = 7, so 2.77 is far too small."))
    its.append(mcq("To find 12 + 3.45, you can write 12 with a decimal point. Which number is equal to 12?",
                   "12.00", ["0.12", "1.2", "120"],
                   "A whole number has its decimal point after the ones digit, so 12 = <b>12.00</b>. "
                   "Then the 2 ones sit over the 3 ones: 12.00 + 3.45 = 15.45."))
    n, he, his = P.next()
    a, b = "13", "2.45"
    w = add_right_align([a, b])
    assert w == Decimal("2.58")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "15.45", ["2.58", "3.75", "1545"],
                   "13 is a whole number, so its point is after the 3: 13 = 13.00 (not 0.13). Line up the points: 13.00 + 2.45. "
                   "Hundredths: 0 + 5 = 5. Tenths: 0 + 4 = 4. Ones: 3 + 2 = 5. Tens: bring down 1. Answer: <b>15.45</b>."))
    for k in [("+", "3.42", "5.17"), ("+", "1.45", "2.3"), ("+", "2.32", "4.5"), ("+", "12", "3.45"), ("+", "13", "2.45")]:
        seen.add(k)
    its.append(mcq("Which shows 6.4 − 2.3 with the decimal points lined up?",
                   "6.4 over 2.3, point under point", ["6.4 over 2.3, 2 under the 4", "6.4 over 2.3, 3 under the 6",
                                                      "2.3 over 6.4, point under point"],
                   "Write the number you start with on top and the number you take away below it. Put point under point, "
                   "so ones are under ones and tenths under tenths. Then 6.4 − 2.3 = <b>4.1</b>."))
    plan = [("+", (1, 1), (1, 1)), ("-", (1, 1), (1, 1)), ("+", (1, 2), (1, 2)), ("-", (1, 2), (1, 2)),
            ("+", (1, 1), (1, 2)), ("-", (1, 2), (1, 1)), ("+", (2, 1), (1, 1)), ("-", (2, 1), (1, 1)),
            ("+", (2, 2), (1, 2)), ("-", (2, 2), (2, 2)), ("+", (2, 1), (1, 2)), ("-", (2, 2), (1, 1)),
            ("+", (1, 0), (1, 2)), ("+", (2, 2), (2, 1))]
    for i, (op, sa, sb) in enumerate(plan):
        a, b = pick(rnd, seen, op, sa, sb, False)
        its.append(item_add([a, b], i % 2 == 0) if op == "+" else item_sub(a, b, i % 2 == 0))
    assert len(its) == 20, len(its)
    return {"title": "Line up the decimal points", "items": its}


# ============================================================ set 3: hundredths with regrouping
def set_regroup(P, rnd, seen):
    its = []
    for a, b in [("0.45", "0.38"), ("0.27", "0.56")]:
        A, B = int(Decimal(a) * 100), int(Decimal(b) * 100)
        tot = Decimal(a) + Decimal(b)
        q = (fig(grid_svg(A, B)) + "The grid is 1 whole. The green part is %s and the yellow part is %s. What is %s + %s?" % (a, b, a, b))
        e = ("Each small square is 0.01 and each column is 0.1. %s = %s and %s = %s. Together: %d + %d = %d hundredths = <b>%s</b>. "
             "In columns: hundredths %s, so regroup 1 tenth."
             % (a, hund(a), b, hund(b), A, B, A + B, nice(tot), "%d + %d = %d" % (A % 10, B % 10, A % 10 + B % 10)))
        its.append(mcq(q, nice(tot), fmt_all(cands_add([a, b])), e))
    a, b = "0.7", "0.65"
    tot = Decimal(a) + Decimal(b)
    assert tot == Decimal("1.35")
    its.append(mcq(fig(grid_svg(70, 65)) + "Each grid is 1 whole. The green part is 0.7 and the yellow part is 0.65. What is 0.7 + 0.65?",
                   "1.35", fmt_all(cands_add([a, b])),
                   "0.7 = 70 hundredths and 0.65 = 65 hundredths. 70 + 65 = 135 hundredths. 100 hundredths fill one whole grid, "
                   "so the sum is 1 whole and 35 hundredths = <b>1.35</b>. (0.72 lines up the last digits: 0.7 is 0.70, not 0.07.)"))
    a, b = "0.82", "0.35"
    assert Decimal(a) - Decimal(b) == Decimal("0.47")
    its.append(mcq(fig(grid_svg(82, 0, cross=35)) + "The grid is 1 whole. 0.82 is shaded. The squares with an X are taken away. What is 0.82 − 0.35?",
                   "0.47", fmt_all(cands_sub(a, b)),
                   "0.82 is 82 hundredths. Take away 35 hundredths: 82 − 35 = 47 hundredths = <b>0.47</b>. "
                   "In columns: 2 − 5 needs a regroup, so 1 tenth becomes 10 hundredths: 12 − 5 = 7, then 7 − 3 = 4."))
    for k in [("+", "0.38", "0.45"), ("+", "0.27", "0.56"), ("+", "0.65", "0.7"), ("-", "0.35", "0.82")]:
        seen.add(k)
    its.append(mcq("10 hundredths make 1 tenth. What is 0.08 + 0.05?", "0.13", ["0.03", "1.3", "13"],
                   "8 hundredths + 5 hundredths = 13 hundredths = 1 tenth and 3 hundredths = <b>0.13</b>. "
                   "(0.03 forgets the regrouped tenth. 1.3 puts the point in the wrong place.)"))
    seen.add(("+", "0.05", "0.08"))
    plan = [("+", (1, 2), (1, 2)), ("-", (1, 2), (1, 2)), ("+", (1, 2), (1, 1)), ("-", (1, 2), (1, 1)),
            ("+", (2, 2), (1, 2)), ("-", (2, 2), (1, 2)), ("+", (1, 2), (0, 2)), ("-", (2, 1), (1, 2)),
            ("+", (2, 2), (2, 2)), ("-", (2, 2), (2, 2))]
    for i, (op, sa, sb) in enumerate(plan):
        cond = (lambda a, b: carry_point(a, b)) if (op == "+" and i % 4 == 0) else (lambda a, b: True)
        a, b = pick(rnd, seen, op, sa, sb, True, cond)
        its.append(item_add([a, b], i % 2 == 0) if op == "+" else item_sub(a, b, i % 2 == 0))
    for i, (a, b) in enumerate([("5", "2.35"), ("10", "4.28"), ("3", "1.6"), ("6.05", "2.37"), ("20", "7.45")]):
        key = ("-",) + tuple(sorted([a, b]))
        assert key not in seen and tail_ok(a, b, "-"), (a, b)
        seen.add(key)
        its.append(item_sub(a, b, i % 2 == 0))
    assert len(its) == 20, len(its)
    return {"title": "Hundredths with regrouping", "items": its}


# ============================================================ set 4: estimate and check
def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def set_estimate(P):
    its = []
    for a, b, op in [("5.83", "3.29", "+"), ("14.15", "4.8", "−"), ("7.46", "5.7", "+"), ("18.7", "5.12", "−"),
                     ("26.6", "8.45", "+"), ("42.08", "9.7", "−")]:
        A, B = Decimal(a), Decimal(b)
        ra, rb = rnd1(a), rnd1(b)
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        est, exact = f(ra, rb), f(A, B)
        fa, fb = int(A), int(B)
        trunc = f(fa, fb)
        other = ra - rb if op == "+" else ra + rb
        assert est != trunc and est != other and rnd1(exact) == est, (a, b)
        its.append(mcq("Round each number to the nearest whole number. Which is the best estimate for %s %s %s?" % (a, op, b),
                       "about %d" % est, ["about %d" % v for v in [trunc, other, f(fa + 1, fb + 1), f(fa + 1, fb), f(fa, fb + 1)]],
                       "%s rounds to %d and %s rounds to %d. %d %s %d = <b>%d</b>. The exact answer, %s, is close to %d."
                       % (a, ra, b, rb, ra, op, rb, est, nice(exact), est)))
    R, S, B_, C = "It is reasonable", "It is too small", "It is too big", "You cannot tell without working it out"
    rows = [("5.5", "+", "2.34", "2.89", S, "lined up the last digits"),
            ("16.8", "+", "7.45", "24.25", R, None),
            ("9.3", "−", "4.6", "47", B_, "left out the decimal point"),
            ("0.7", "+", "0.6", "0.13", S, "wrote 13 tenths as 0.13 instead of 1.3"),
            ("24.6", "−", "8.75", "15.85", R, None),
            ("27.06", "−", "4.5", "26.61", B_, "lined up the last digits"),
            ("12.4", "+", "3.65", "16.05", R, None)]
    for i, (a, op, b, shown, ans, why) in enumerate(rows):
        n, he, his = P.next()
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        exact = f(Decimal(a), Decimal(b))
        est = f(rnd1(a), rnd1(b))
        assert (Decimal(shown) == exact) == (ans == R)
        assert ans != S or Decimal(shown) < est - 1
        assert ans != B_ or Decimal(shown) > est + 1
        tool = " on a calculator" if ans == R and i % 2 else ""     # a calculator does not line up digits wrongly
        q = "%s worked out %s %s %s%s and got %s. Use an estimate to check. What does the estimate show?" % (n, a, op, b, tool, shown)
        e = "%s rounds to %d and %s rounds to %d, so the answer should be about %d %s %d = %d. " % (a, rnd1(a), b, rnd1(b), rnd1(a), op, rnd1(b), est)
        if ans == R:
            e += "%s is close to %d, so <b>it is reasonable</b>." % (shown, est)
        else:
            e += ("%s is much %s than %d, so <b>%s</b>. %s probably %s. The correct answer is %s."
                  % (shown, "smaller" if ans == S else "bigger", est, ans.lower(), n, why, nice(exact)))
        its.append(mcq(q, ans, [x for x in [R, S, B_, C] if x != ans], e))
    for a, op, b in [("7.8", "+", "4.56"), ("15", "−", "6.28"), ("9.45", "+", "12.7"), ("40", "−", "18.35"),
                     ("6.07", "+", "2.9"), ("13.4", "−", "5.82"), ("0.85", "+", "2.6")]:
        if op == "+":
            exact = Decimal(a) + Decimal(b)
            cc = cands_add([a, b])
        else:
            exact = Decimal(a) - Decimal(b)
            cc = cands_sub(a, b)
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        est = f(rnd1(a), rnd1(b))
        far = [v for v in cc if v is not None and not isinstance(v, str) and v > 0 and abs(v - exact) >= Decimal("1.5")]
        its.append(mcq("Estimate first, then choose the correct answer without working it out exactly: %s %s %s" % (a, op, b),
                       nice(exact), fmt_all(far),
                       "%s %s %s is about %d %s %d = %d. Only <b>%s</b> is close to %d. Check by working it out: %s"
                       % (a, op, b, rnd1(a), op, rnd1(b), est, nice(exact), est,
                          (add_steps([a, b]) if op == "+" else sub_steps(a, b)).replace("Line up the decimal points. ", ""))))
    assert len(its) == 20, len(its)
    return {"title": "Estimate and check", "items": its}


# ============================================================ set 5: money and measurement
def cash(d):
    """Canada has no pennies: a cash total is rounded to the nearest 5 cents (1, 2, 6, 7 down; 3, 4, 8, 9 up)."""
    cents = int(Decimal(d) * 100)
    assert Decimal(cents) / 100 == Decimal(d)
    return Decimal((cents + 2) // 5 * 5) / 100


def is5(d):
    return int(Decimal(d) * 100) % 5 == 0


def story_add(q, nums, unit, lead, is_money=False):
    tot = sum(Decimal(n) for n in nums)
    if is_money:
        c = [money(v) for v in cands_add(nums) if v is not None and not isinstance(v, str) and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(tot), c, lead + " " + add_steps(nums))
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_add(nums))], lead + " " + add_steps(nums))


def story_sub(q, a, b, unit, lead, is_money=False):
    r = Decimal(a) - Decimal(b)
    if is_money:
        c = [money(v) for v in cands_sub(a, b) if v is not None and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(r), c, lead + " " + sub_steps(a, b))
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_sub(a, b))], lead + " " + sub_steps(a, b))


def set_words(P):
    its = []
    n, he, his = P.next()
    assert cash("4.62") == Decimal("4.60")
    its.append(mcq("There are no pennies in Canada, so a cash total is rounded to the nearest 5¢. "
                   "%s’s total at the corner store is $4.62. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$4.60", ["$4.65", "$4.70", "$4.62"],
                   "The nearest multiples of 5¢ are $4.60 and $4.65. $4.62 is 2¢ from $4.60 and 3¢ from $4.65, "
                   "so it rounds down to <b>$4.60</b>. (Totals ending in 1, 2, 6 or 7 cents round down; 3, 4, 8 or 9 round up.)"))
    n, he, his = P.next()
    its.append(story_add("At the hockey rink snack bar, %s buys a hot dog for $3.75 and a hot chocolate for $2.50. How much does %s spend?" % (n, he),
                         ["3.75", "2.5"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    t = Decimal("2.69") + Decimal("1.48")
    assert t == Decimal("4.17") and cash(t) == Decimal("4.15")
    its.append(mcq("On a BC Ferries trip to Vancouver Island, %s buys a muffin for $2.69 and a carton of milk for $1.48. "
                   "%s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$4.15", ["$4.17", "$4.20", "$3.15"],
                   "Step 1, add: $2.69 + $1.48. Hundredths: 9 + 8 = 17, write 7 and regroup 1 tenth. Tenths: 6 + 4 + 1 = 11, "
                   "write 1 and regroup 1 one. Ones: 2 + 1 + 1 = 4. Total: $4.17. Step 2, cash: $4.17 is 2¢ from $4.15 "
                   "and 3¢ from $4.20, so %s pays <b>$4.15</b>. ($4.17 is what a card would pay.)" % he))
    n, he, his = P.next()
    t = Decimal("5.49") + Decimal("2.29")
    assert t == Decimal("7.78") and cash(t) == Decimal("7.80") and add_no_carry(["5.49", "2.29"]) == Decimal("7.68")
    its.append(mcq("%s buys a sandwich for $5.49 and a juice for $2.29. %s pays with a debit card. How much is %s charged?" % (n, cap(he), he),
                   "$7.78", ["$7.80", "$7.75", "$7.68"],
                   "Card and debit payments are charged the <b>exact</b> amount; only cash is rounded to 5¢. "
                   "$5.49 + $2.29: hundredths 9 + 9 = 18, write 8 and regroup 1 tenth. Tenths 4 + 2 + 1 = 7. Ones 5 + 2 = 7. "
                   "Answer: <b>$7.78</b>. ($7.80 is the cash price.)"))
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $6.35 lunch with a $10 bill. How much change does %s get?" % (n, he),
                         "10", "6.35", "", "Change is what is left: subtract.", is_money=True))
    n, he, his = P.next()
    assert cash("13.83") == Decimal("13.85") and Decimal(20) - Decimal("13.85") == Decimal("6.15")
    assert Decimal(20) - Decimal("13.83") == Decimal("6.17") and sub_no_annex("20", "13.85") == Decimal("7.85")
    its.append(mcq("%s’s groceries come to $13.83. %s pays cash with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                   "$6.15", ["$6.17", "$6.20", "$7.85"],
                   "Step 1, cash total: $13.83 is 2¢ from $13.85 and 3¢ from $13.80, so it rounds to $13.85. "
                   "Step 2, change: $20.00 − $13.85 = <b>$6.15</b>. Check: $6.15 + $13.85 = $20.00. "
                   "($6.17 forgets the cash rounding.)"))
    its.append(story_add("It rained in Vancouver on Monday and Tuesday. 12.4 mm of rain fell on Monday and 8.9 mm fell on Tuesday. "
                         "How much rain fell over the two days?", ["12.4", "8.9"], "mm", "Put the two days together: add."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("On Sports Day, %s ran the 60 m dash in 11.42 seconds and %s ran it in 10.87 seconds. "
                         "How many seconds faster was %s?" % (n1, n2, n2),
                         "11.42", "10.87", "seconds", "The faster runner has the smaller time. Find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("At swimming lessons, %s swam 25 m in 31.05 seconds. Last month %s time was 33.4 seconds. "
                         "By how many seconds did %s improve?" % (n, his, he),
                         "33.4", "31.05", "seconds", "The improvement is the difference between the two times: subtract."))
    n, he, his = P.next()
    its.append(story_add("In the long jump, %s jumped 2.4 m. %s second jump was 0.35 m longer. How long was the second jump?" % (n, cap(his)),
                         ["2.4", "0.35"], "m", "Longer means more: add."))
    its.append(story_sub("A coho salmon in the Fraser River is 0.64 m long. A chinook salmon is 0.92 m long. "
                         "How much longer is the chinook salmon?",
                         "0.92", "0.64", "m", "How much longer means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("A water bottle holds 1 L. %s drinks 0.45 L on a hike at Grouse Mountain. How much water is left?" % n,
                         "1", "0.45", "L", "Take away what %s drank: subtract." % he))
    its.append(story_sub("A roll of ribbon is 3 m long. The class cuts off 1.25 m for a banner. How much ribbon is left?",
                         "3", "1.25", "m", "Take the part cut off away: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s’s family walks 3.6 km on the Stanley Park seawall before lunch and 2.85 km after lunch. "
                         "How far do they walk altogether?" % n, ["3.6", "2.85"], "km", "Altogether means add."))
    n, he, his = P.next()
    its.append(story_sub("The Terry Fox Run at %s’s school is 2.5 km long. %s has run 1.75 km so far. How much farther does %s have to run?"
                         % (n, cap(he), he), "2.5", "1.75", "km", "How much farther means find what is left: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s pays by card for a book at $12.99 and a pencil case at $4.49. What is the total?" % n,
                         ["12.99", "4.49"], "", "Total means add. A card pays the exact amount.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("%s’s backpack has a mass of 3.2 kg. %s takes out a lunch bag with a mass of 0.65 kg. "
                         "What is the mass of the backpack now?" % (n, cap(he)),
                         "3.2", "0.65", "kg", "Take away what was taken out: subtract."))
    a, b, c = Decimal("20"), Decimal("8.45"), Decimal("6.75")
    assert a - b - c == Decimal("4.80") and b + c == Decimal("15.20")
    assert sub_no_annex("20", "15.2") == Decimal("5.2") and a - b == Decimal("11.55")
    n, he, his = P.next()
    its.append(mcq("%s has $20 at the school spring fair. %s buys a plant for $8.45 and a pie for $6.75. How much money does %s have left?" % (n, cap(he), he),
                   "$4.80", [money(sub_no_annex("20", "15.2")), money(b + c), money(a - b)],
                   "Step 1, money spent: $8.45 + $6.75 = $15.20. Step 2, money left: $20.00 − $15.20 = <b>$4.80</b>. "
                   "Check: $4.80 + $15.20 = $20.00."))
    n, he, his = P.next()
    its.append(story_add("%s measures the new snow at school in Prince George on three days: 12.4 cm, 9.8 cm and 4.6 cm. "
                         "What is the total snowfall?" % n,
                         ["12.4", "9.8", "4.6"], "cm", "Total means add all three days."))
    assert Decimal(6) - Decimal("2.45") == Decimal("3.55") and sub_no_annex("6", "2.45") == Decimal("4.45")
    its.append(mcq("What number goes in the box?  <b>☐ + 2.45 = 6</b>", "3.55", ["4.45", "3.65", "8.45"],
                   "Use subtraction: 6 − 2.45 = 6.00 − 2.45 = <b>3.55</b>. Check: 3.55 + 2.45 = 6.00 = 6. "
                   "(4.45 forgets to write the zeros: 6 − 2 = 4, then brings down .45. 8.45 adds instead of subtracting.)"))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("0.6") + Decimal("0.5") == Decimal("1.1") and add_concat(["0.6", "0.5"]) == "0.11"
    assert Decimal("4.5") + Decimal("2.37") == Decimal("6.87") and add_right_align(["4.5", "2.37"]) == Decimal("2.82")
    assert Decimal("4.78") + Decimal("2.56") == Decimal("7.34") and add_forgot_point_carry(["4.78", "2.56"]) == Decimal("6.34")
    assert Decimal(10) - Decimal("3.46") == Decimal("6.54") and sub_no_annex("10", "3.46") == Decimal("7.46")
    assert no_point(Decimal("6.87")) == Decimal(687)
    assert cash("7.42") == Decimal("7.40") and cash("7.43") == Decimal("7.45") and cash("7.47") == Decimal("7.45") and cash("7.48") == Decimal("7.50")
    assert Decimal("1.89") + Decimal("1.48") == Decimal("3.37") and cash("3.37") == Decimal("3.35")
    return (
        "<h2>The idea: add tenths to tenths, hundredths to hundredths</h2>"
        "<p>A decimal is made of ones, tenths and hundredths. You can only add or subtract parts of the same size. "
        "So add tenths to tenths and hundredths to hundredths, just like ones to ones.</p>"
        "<figure class='sn-fig'>" + bars_svg(6, 5) +
        "<figcaption>0.6 + 0.5: 6 tenths + 5 tenths = 11 tenths. 10 tenths fill one whole bar, so 0.6 + 0.5 = 1.1 (not 0.11).</figcaption></figure>"
        "<h2>Line up the decimal points</h2>"
        "<p>In columns, put point under point. Then ones are under ones, tenths under tenths and hundredths under hundredths. "
        "If one number has fewer places, write a zero: 4.5 = 4.50. A zero at the end does not change the value.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.5", "2.37"], "+", answer="6.87", ghost=True, fs=34) +
        "<figcaption>4.5 + 2.37 = 4.50 + 2.37. Hundredths 0 + 7 = 7, tenths 5 + 3 = 8, ones 4 + 2 = 6. Answer: 6.87.</figcaption></figure>"
        "<h2>Regroup like whole numbers</h2>"
        "<p>10 hundredths make 1 tenth, and 10 tenths make 1 one. When a column makes 10 or more, regroup. "
        "The 1 can cross the decimal point.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.78", "2.56"], "+", answer="7.34", marks=True, fs=34) +
        "<figcaption>4.78 + 2.56: hundredths 8 + 6 = 14, write 4 and regroup 1 tenth. "
        "Tenths 7 + 5 + 1 = 13, write 3 and regroup 1 one. Ones 4 + 2 + 1 = 7. Answer: 7.34.</figcaption></figure>"
        "<p>To take a decimal from a whole number, write the whole number with a point and zeros: 10 = 10.00.</p>"
        "<figure class='sn-fig'>" + column_svg(["10", "3.46"], "-", answer="6.54", ghost=True, marks=True, fs=34) +
        "<figcaption>10 − 3.46 = 10.00 − 3.46. Regroup: 0 tens, 9 ones, 9 tenths and 10 hundredths. "
        "10 − 6 = 4, 9 − 4 = 5, 9 − 3 = 6. Answer: 6.54.</figcaption></figure>"
        "<h2>Estimate first, then check</h2>"
        "<p>Round each number to the nearest whole number. 4.5 + 2.37 is about 5 + 2 = 7, so 6.87 makes sense and 2.82 does not. "
        "Check a subtraction by adding back: 6.54 + 3.46 = 10.</p>"
        "<h2>Money in Canada: cash and card</h2>"
        "<p>Canada has no pennies. When you pay with <b>cash</b>, the total is rounded to the nearest 5¢. "
        "When you pay by <b>debit or credit card</b>, you pay the exact amount.</p>" +
        table(["Total ends in", "Cash total", "Example"], [
            ["1¢ or 2¢", "Round down to 0¢", "$7.42 → $7.40"],
            ["3¢ or 4¢", "Round up to 5¢", "$7.43 → $7.45"],
            ["6¢ or 7¢", "Round down to 5¢", "$7.47 → $7.45"],
            ["8¢ or 9¢", "Round up to the next 10¢", "$7.48 → $7.50"],
        ]) +
        ex("Example", "A muffin costs $1.89 and milk costs $1.48. How much do you pay with cash? With a card?",
           "Add: $1.89 + $1.48 = $3.37. Card: the exact amount, $3.37. Cash: $3.37 is closer to $3.35 than to $3.40.",
           "cash $3.35, card $3.37") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (4.5 + 2.37 = 2.82)", "Line up the decimal points. Write 4.5 as 4.50"],
            ["Dropping the decimal point (4.5 + 2.37 = 687)", "Bring the point straight down into the answer"],
            ["Writing 11 tenths as 0.11 (0.6 + 0.5 = 0.11)", "10 tenths make 1 one: 0.6 + 0.5 = 1.1"],
            ["Not writing the zeros (10 − 3.46 = 7.46)", "Write 10 as 10.00, then regroup to subtract"],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract decimals in Grade 4?",
     "a": "Line up the decimal points, write zeros in empty places, then add or subtract from the right like whole numbers: 4.5 + 2.37 = 4.50 + 2.37 = 6.87."},
    {"q": "Why is 0.6 + 0.5 not 0.11?",
     "a": "0.6 + 0.5 is 6 tenths + 5 tenths = 11 tenths, and 10 tenths make 1 whole, so the answer is 1.1. 0.11 is only 11 hundredths, which is less than 0.6."},
    {"q": "How is cash rounded in Canada without pennies?",
     "a": "A cash total is rounded to the nearest 5¢: totals ending in 1, 2, 6 or 7 cents round down, and totals ending in 3, 4, 8 or 9 cents round up. Debit and credit card payments are charged the exact amount."},
    {"q": "Is adding and subtracting decimals on the Grade 4 FSA?",
     "a": "It can be. The Grade 4 FSA numeracy section is based on the BC curriculum, and adding and subtracting decimals to hundredths is a Grade 4 learning standard, often met in money and measurement problems."},
]


def verify(sets):
    """Recompute every 'What is a ± b?' answer and every column picture from its aria-label."""
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is ([\d.]+) ([+−]) ([\d.]+)\?$", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"aria-label='([\d.]+) (plus|minus) ([\d.]+) written in columns", it["q"])
            if m and ("Add." in it["q"] or "Subtract." in it["q"]):
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "plus" else a - b), it["q"]
            if "$" in right and "with cash" in it["q"]:
                assert is5(right.lstrip("$")), it["q"]
            for c in it["c"]:
                for num in re.findall(r"\d+\.\d+", c):
                    assert dec(num) <= 2, (it["q"], c)


def gen():
    rnd = random.Random(34807)
    P = People(rnd)
    seen = set()
    sets = [set_tenths(P), set_line_up(P, rnd, seen), set_regroup(P, rnd, seen), set_estimate(P), set_words(P)]
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"\$?[\d.]+( [a-zA-Z]+)?", x) for x in it["c"]):
                assert len({Decimal(re.sub(r"[^\d.]", "", x)) for x in it["c"]}) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "adding-and-subtracting-decimals", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Adding and Subtracting Decimals",
        "seo_title": "Grade 4 Adding and Subtracting Decimals Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Adding and Subtracting Decimals",
        "domain": "Computational fluency",
        "standard_code": "Grade 4: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Addition and subtraction of decimals to hundredths",
        "meta_desc": "Free Grade 4 math worksheets on adding and subtracting decimals to hundredths, matched to the BC curriculum: "
                     "tenths with models, lining up the decimal points, regrouping, estimating to check, and money problems "
                     "with cash rounded to 5¢. 100 questions with an answer key. Great FSA practice.",
        "key_big": "Line up the decimal points, then add or subtract like whole numbers.",
        "key_sub": "Tenths go with tenths and hundredths with hundredths. 10 tenths make 1 whole, so 0.6 + 0.5 = 1.1, not 0.11. "
                   "Estimate to check: 4.5 + 2.37 is about 7, so the answer is 6.87.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    for pat in ("tenths bar", "number line", "hundredths grids"):
        mark_large(u, pat)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
