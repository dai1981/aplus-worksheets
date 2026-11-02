# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Adding and Subtracting Decimals (BC Mathematics Curriculum, Computational fluency:
addition and subtraction of decimals to thousandths)
  python3 tools/gen_cabc_math_g5_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (4.5 + 2.375 -> 4500 + 2375 thousandths), so every regroup and every typical mistake is exact.
Canadian style: math, metre, litre, $ and the cent sign, no pennies (cash rounds to the nearest 5 cents),
4-digit numbers without a separator. Column helpers are copied from gen_caon_math_g6_add_sub_decimals.py.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
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
    """Shortest exact text for a Decimal (BC style: no separator below 10 000)."""
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


def sub_zeros_not_nine(a, b):
    """Regrouped across zeros but left the zeros as 0 (did not change them to 9): 2 − 0.008 = 1.002.
    Only when the digits of b under those zeros are 0, so the rest of the work is ordinary."""
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    hit = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while j < k and d[j] == 0:
                j += 1
            if j >= k:
                return None
            if j > i + 1:
                if any(db[m] for m in range(i + 1, j)):
                    return None
                hit = True
            else:
                pass
            d[j] -= 1
            d[i] += 10
    if not hit:
        return None
    r = sum((d[i] - db[i]) * 10 ** i for i in range(k))
    return back(r, P) if r > 0 else None


def sub_forgot_one(a, b):
    """Regrouped from the ones but forgot to take 1 from the ones: one too high (10 − 4.28 = 6.72)."""
    P, (A, B) = scale([a, b])
    if P == 0:
        return None
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    if P >= k:                 # no ones digit (0.915 − 0.68)
        return None
    nd = borrow_digits(A, B)
    if nd[P] == d[P]:          # the ones digit was not used in a regroup
        return None
    return Decimal(a) - Decimal(b) + 1


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
    return ([sub_no_annex(a, b), sub_small_from_big(a, b), sub_zeros_not_nine(a, b), sub_forgot_one(a, b),
             sub_right_align(a, b), Decimal(a) + Decimal(b)]
            + point_shift(r, P))


# ------------------------------------------------------------ helpers
def fmt_all(vals, f=nice):
    out = []
    for v in vals:
        if v is None:
            continue
        if isinstance(v, str):
            if dec(v) <= 3:
                out.append(v)
        elif 0 < v < 10000 and dec(nice(v)) <= 3:          # Grade 5 stops at thousandths
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


def carry_point(a, b):
    P, ints = scale([a, b])
    k, sums, carries = col_info(ints)
    return bool(P and carries[P - 1])


def pick(rnd, seen, op, sa, sb, cond=lambda a, b: True, swap=True):
    for _ in range(20000):
        a, b = rnd_num(rnd, *sa), rnd_num(rnd, *sb)
        if op == "+" and swap and rnd.random() < 0.5:
            a, b = b, a
        key = (op,) + tuple(sorted([a, b]))
        if key in seen or not tail_ok(a, b, op):
            continue
        if op == "-" and (Decimal(a) - Decimal(b) < Decimal("0.5") or regroups_sub(a, b) == 0):
            continue
        if not cond(a, b):
            continue
        seen.add(key)
        return a, b
    raise RuntimeError((op, sa, sb))




def crosses_zero(a, b):
    """True when some regroup has to pass through a 0 (5.003 − 1.26, 7 − 2.35)."""
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                return True
            d[j] -= 1
            d[i] += 10
    return False


# ============================================================ set 1: line up the decimal points
def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("You add 4.326 + 2.51 in columns with the decimal points lined up. Which digit of 2.51 goes under the 3?",
                   "5", ["1", "2", "the decimal point"],
                   "The 3 in 4.326 is in the tenths place. Line up the decimal points and tenths sit under tenths: "
                   "the tenths digit of 2.51 is <b>5</b>. (1 is the hundredths digit, so it goes under the 2.)"))
    its.append(mcq("In 37.264 − 5.81, the digits are lined up by place value. Which digit of 37.264 is above the 5?",
                   "7", ["3", "2", "6"],
                   "5 is the ones digit of 5.81. The ones digit of 37.264 is <b>7</b>, so the 5 goes under the 7. "
                   "The 3 is in the tens place and has no digit under it."))
    n, he, his = P.next()
    assert Decimal("0.6") + Decimal("0.5") == Decimal("1.1") and add_concat(["0.6", "0.5"]) == "0.11"
    its.append(mcq("%s says 0.6 + 0.5 = 0.11. What is the correct answer?" % n, "1.1", ["0.11", "11", "1.01"],
                   "6 tenths + 5 tenths = 11 tenths. 10 tenths make 1 one, so 11 tenths = 1 one and 1 tenth = <b>1.1</b>. "
                   "0.11 is only 11 hundredths, which is less than 0.6 alone."))
    seen.add(("+", "0.5", "0.6"))
    plan = [("+", (1, 1), (1, 1), "nopt"), ("+", (1, 2), (1, 2), "nopt"), ("-", (1, 2), (1, 2), None),
            ("+", (1, 3), (1, 3), "nopt"), ("-", (2, 1), (1, 1), None),
            ("+", (1, 1), (1, 1), "pt"), ("+", (1, 2), (1, 2), "pt"), ("-", (1, 3), (1, 3), None),
            ("+", (2, 2), (1, 2), "pt"), ("-", (2, 2), (1, 2), None),
            ("+", (1, 3), (1, 3), "pt"), ("-", (2, 3), (1, 3), None), ("+", (2, 2), (2, 2), "pt"),
            ("-", (2, 2), (2, 2), None), ("+", (2, 3), (1, 3), "pt"), ("-", (2, 3), (2, 3), None),
            ("+", (0, 3), (0, 3), "pt")]
    for i, (op, sa, sb, kind) in enumerate(plan):
        if op == "+":
            cond = (lambda a, b: not carry_point(a, b)) if kind == "nopt" else (lambda a, b: carry_point(a, b))
            a, b = pick(rnd, seen, "+", sa, sb, cond)
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb)
            its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Line up the decimal points", "items": its}


# ============================================================ set 2: different numbers of places
def set_places(P, rnd, seen):
    its = []
    its.append(mcq("To add 3.8 + 1.256, you write 3.8 with three decimal places. Which number is equal to 3.8?",
                   "3.800", ["3.008", "0.38", "38.00"],
                   "Zeros at the end of a decimal do not change its value: 3.8 = 3 ones and 8 tenths = <b>3.800</b>. "
                   "3.008 is wrong: it moves the 8 to the thousandths place."))
    n, he, his = P.next()
    a, b = "5.6", "2.143"
    w = add_right_align([a, b])
    assert w == Decimal("2.199") and Decimal(a) + Decimal(b) == Decimal("7.743")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "7.743", ["2.199", "7743", "77.43"],
                   "Line up the <b>decimal points</b>, not the last digits: 5.600 + 2.143. Thousandths: 0 + 3 = 3. "
                   "Hundredths: 0 + 4 = 4. Tenths: 6 + 1 = 7. Ones: 5 + 2 = 7. Answer: <b>7.743</b>. "
                   "Estimate: 6 + 2 = 8, so 2.199 is far too small."))
    its.append(mcq("To find 9 + 3.475, you can write 9 with a decimal point. Which number is equal to 9?",
                   "9.000", ["0.009", "0.9", "900"],
                   "A whole number has its decimal point after the ones digit, so 9 = <b>9.000</b>. "
                   "Then the 9 ones sit over the 3 ones: 9.000 + 3.475 = 12.475."))
    n, he, his = P.next()
    a, b = "18", "4.25"
    w = add_right_align([a, b])
    assert w == Decimal("4.43") and add_left_align([a, b]) == Decimal("6.05")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "22.25", fmt_all([w, Decimal("6.05"), Decimal("2225")]),
                   "18 is a whole number, so its point is after the 8: 18 = 18.00 (not 1.8). Line up the points: 18.00 + 4.25. "
                   "Hundredths: 0 + 5 = 5. Tenths: 0 + 2 = 2. Ones: 8 + 4 = 12, write 2 and regroup 1 ten. "
                   "Tens: 1 + 1 = 2. Answer: <b>22.25</b>."))
    for k in [("+", "1.256", "3.8"), ("+", "2.143", "5.6"), ("+", "3.475", "9"), ("+", "18", "4.25")]:
        seen.add(k)
    its.append(item_add(["0.7", "0.465"], False))
    its.append(item_add(["2.375", "4.8"], True))
    seen.add(("+", "0.465", "0.7")); seen.add(("+", "2.375", "4.8"))
    plan = [("+", (1, 1), (1, 2)), ("+", (1, 2), (0, 1)), ("+", (2, 1), (1, 2)), ("-", (1, 2), (1, 1)),
            ("+", (1, 0), (1, 2)), ("-", (2, 2), (1, 1)), ("+", (2, 2), (1, 1)), ("-", (1, 3), (1, 1)),
            ("+", (1, 1), (0, 3)), ("-", (2, 3), (1, 2)), ("+", (2, 1), (2, 3)), ("-", (2, 2), (1, 0)),
            ("+", (1, 3), (1, 2)), ("-", (2, 3), (2, 1))]
    for i, (op, sa, sb) in enumerate(plan):
        if op == "+":
            a, b = pick(rnd, seen, "+", sa, sb, lambda a, b: dec(a) != dec(b) and (carry_point(a, b) == (i % 3 != 0) or min(dec(a), dec(b)) == 0))
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb, lambda a, b: not crosses_zero(a, b), swap=False)
            its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Different numbers of decimal places", "items": its}


# ============================================================ set 3: subtract across zeros
def set_zeros(P, rnd, seen):
    its = []
    assert Decimal(7) - Decimal("2.358") == Decimal("4.642")
    its.append(mcq("To find 7 − 2.358, how should you write 7 so both numbers have thousandths?", "7.000",
                   ["0.007", "0.700", "7.358"],
                   "7 is 7 ones, and its decimal point is after the 7. Write <b>7.000</b>: three zeros hold the tenths, "
                   "hundredths and thousandths places. Then 7.000 − 2.358 = 4.642."))
    n, he, his = P.next()
    assert Decimal("4.642") - Decimal("2.358") == Decimal("2.284") and Decimal("4.642") + 7 == Decimal("11.642")
    its.append(mcq("%s found 7 − 2.358 = 4.642. Which addition checks %s answer?" % (n, his),
                   "4.642 + 2.358 = 7", ["4.642 − 2.358 = 2.284", "7 + 2.358 = 9.358", "4.642 + 7 = 11.642"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 4.642 + 2.358 = 7.000 = 7. "
                   "You get back the starting number, so %s answer is right." % his))
    # pairs used in set 4 (16 − 6.28, 40 − 18.35): keep them out of this set
    seen.add(("-",) + tuple(sorted(["16", "6.28"])))
    seen.add(("-",) + tuple(sorted(["40", "18.35"])))
    fixed_pairs = [("10", "4.28"), ("5", "2.37"), ("1", "0.365"), ("20", "6.75"), ("4.005", "1.367"), ("6", "0.125"),
                   ("30.04", "12.67"), ("3", "1.475"), ("8.002", "3.005"), ("2", "0.008")]
    for a, b in fixed_pairs:
        assert tail_ok(a, b, "-") and crosses_zero(a, b), (a, b)
        key = ("-",) + tuple(sorted([a, b]))
        assert key not in seen, key
        seen.add(key)
    pairs = list(fixed_pairs)
    shapes = [((1, 0), (1, 2)), ((2, 0), (1, 2)), ((1, 0), (0, 3)), ((2, 0), (2, 2)), ((1, 0), (1, 3)),
              ((2, 0), (1, 3)), ((2, 0), (2, 1)), ((1, 0), (0, 2))]
    for sa, sb in shapes:
        a, b = pick(rnd, seen, "-", sa, sb, crosses_zero, swap=False)
        pairs.append((a, b))
    for i, (a, b) in enumerate(pairs):
        assert crosses_zero(a, b), (a, b)
        its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Subtract across zeros", "items": its}


# ============================================================ set 4: estimate first and check
def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def set_estimate(P):
    its = []
    for a, b, op in [("6.82", "3.294", "+"), ("12.15", "4.9", "−"), ("8.475", "5.6", "+"), ("19.7", "6.125", "−"),
                     ("23.6", "7.45", "+"), ("31.08", "6.7", "−")]:
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
    rows = [("5.6", "+", "2.143", "2.199", S, "lined up the last digits instead of the decimal points", False),
            ("18.6", "+", "7.45", "26.05", R, None, True),
            ("9.2", "−", "4.65", "0.455", S, "put the decimal point in the wrong place", False),
            ("3.75", "+", "6.8", "1055", B_, "left out the decimal point", False),
            ("24.6", "−", "8.705", "15.895", R, None, False),
            ("31.08", "−", "6.5", "37.58", B_, "pressed + instead of −", True),
            ("12.4", "+", "3.625", "16.025", R, None, True)]
    assert Decimal("31.08") + Decimal("6.5") == Decimal("37.58")
    assert add_right_align(["5.6", "2.143"]) == Decimal("2.199") and no_point(Decimal("10.55")) == Decimal(1055)
    for i, (a, op, b, shown, ans, why, calc) in enumerate(rows):
        n, he, his = P.next()
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        exact = f(Decimal(a), Decimal(b))
        est = f(rnd1(a), rnd1(b))
        assert (Decimal(shown) == exact) == (ans == R)
        assert ans != S or Decimal(shown) < est - 1
        assert ans != B_ or Decimal(shown) > est + 1
        tool = " on a calculator" if calc else " by hand"
        q = "%s worked out %s %s %s%s and got %s. Use an estimate to check. What does the estimate show?" % (n, a, op, b, tool, shown)
        e = "%s rounds to %d and %s rounds to %d, so the answer should be about %d %s %d = %d. " % (a, rnd1(a), b, rnd1(b), rnd1(a), op, rnd1(b), est)
        if ans == R:
            e += "%s is close to %d, so <b>it is reasonable</b>." % (shown, est)
        else:
            e += ("%s is much %s than %d, so <b>%s</b>. %s probably %s. The correct answer is %s."
                  % (shown, "smaller" if ans == S else "bigger", est, ans.lower(), n, why, nice(exact)))
        its.append(mcq(q, ans, [x for x in [R, S, B_, C] if x != ans], e))
    for a, op, b in [("8.7", "+", "4.56"), ("16", "−", "6.28"), ("9.45", "+", "12.7"), ("40", "−", "18.35"),
                     ("6.075", "+", "2.9"), ("13.4", "−", "5.825"), ("0.85", "+", "2.6")]:
        if op == "+":
            exact = Decimal(a) + Decimal(b)
            cc = cands_add([a, b])
        else:
            exact = Decimal(a) - Decimal(b)
            cc = cands_sub(a, b)
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        est = f(rnd1(a), rnd1(b))
        far = [v for v in cc if v is not None and not isinstance(v, str) and v > 0 and abs(v - exact) >= Decimal("1.5")
               and dec(nice(v)) <= 3]
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
        return mcq(q, money(tot), c, lead + " " + add_steps(nums).replace("Answer: %s." % nice(tot), "Answer: %s." % money(tot)))
    c = [x for x in fmt_all(cands_add(nums)) if dec(x) <= 3]
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (x, unit) for x in c], lead + " " + add_steps(nums))


def story_sub(q, a, b, unit, lead, is_money=False):
    r = Decimal(a) - Decimal(b)
    if is_money:
        c = [money(v) for v in cands_sub(a, b) if v is not None and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(r), c, lead + " " + sub_steps(a, b).replace("Answer: %s." % nice(r), "Answer: %s." % money(r)))
    c = [x for x in fmt_all(cands_sub(a, b)) if dec(x) <= 3]
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (x, unit) for x in c], lead + " " + sub_steps(a, b))


def set_words(P):
    its = []
    n, he, his = P.next()
    assert cash("6.43") == Decimal("6.45")
    its.append(mcq("There are no pennies in Canada, so a cash total is rounded to the nearest 5¢. "
                   "%s’s total at the corner store is $6.43. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$6.45", ["$6.40", "$6.50", "$6.43"],
                   "The nearest multiples of 5¢ are $6.40 and $6.45. $6.43 is 3¢ from $6.40 and 2¢ from $6.45, "
                   "so it rounds up to <b>$6.45</b>. (Totals ending in 1, 2, 6 or 7 cents round down; 3, 4, 8 or 9 round up.)"))
    n, he, his = P.next()
    its.append(story_add("At the hockey rink snack bar in Kamloops, %s buys a slice of pizza for $3.85 and a hot chocolate for $2.65. "
                         "How much does %s spend?" % (n, he),
                         ["3.85", "2.65"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    t = Decimal("2.79") + Decimal("1.68")
    assert t == Decimal("4.47") and cash(t) == Decimal("4.45") and add_forgot_point_carry(["2.79", "1.68"]) == Decimal("3.47")
    its.append(mcq("On a BC Ferries trip to Vancouver Island, %s buys a muffin for $2.79 and a carton of milk for $1.68. "
                   "%s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$4.45", ["$4.47", "$4.50", "$3.45"],
                   "Step 1, add: $2.79 + $1.68. Hundredths: 9 + 8 = 17, write 7 and regroup 1 tenth. Tenths: 7 + 6 + 1 = 14, "
                   "write 4 and regroup 1 one. Ones: 2 + 1 + 1 = 4. Total: $4.47. Step 2, cash: $4.47 is 2¢ from $4.45 "
                   "and 3¢ from $4.50, so %s pays <b>$4.45</b>. ($4.47 is what a card would pay.)" % he))
    n, he, his = P.next()
    t = Decimal("6.59") + Decimal("2.39")
    assert t == Decimal("8.98") and cash(t) == Decimal("9.00") and add_no_carry(["6.59", "2.39"]) == Decimal("8.88")
    its.append(mcq("%s buys a sandwich for $6.59 and a juice for $2.39. %s pays with a debit card. How much is %s charged?" % (n, cap(he), he),
                   "$8.98", ["$9.00", "$8.95", "$8.88"],
                   "Card and debit payments are charged the <b>exact</b> amount; only cash is rounded to 5¢. "
                   "$6.59 + $2.39: hundredths 9 + 9 = 18, write 8 and regroup 1 tenth. Tenths 5 + 3 + 1 = 9. Ones 6 + 2 = 8. "
                   "Answer: <b>$8.98</b>. ($9.00 is the cash price.)"))
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $13.45 book with a $20 bill. How much change does %s get?" % (n, he),
                         "20", "13.45", "", "Change is what is left: subtract.", is_money=True))
    n, he, his = P.next()
    assert cash("27.38") == Decimal("27.40") and Decimal(50) - Decimal("27.40") == Decimal("22.60")
    assert Decimal(50) - Decimal("27.38") == Decimal("22.62") and sub_no_annex("50", "27.4") == Decimal("23.4")
    its.append(mcq("%s’s groceries come to $27.38. %s pays cash with a $50 bill. How much change does %s get?" % (n, cap(he), he),
                   "$22.60", ["$22.62", "$22.65", "$23.40"],
                   "Step 1, cash total: $27.38 is 2¢ from $27.40 and 3¢ from $27.35, so it rounds to $27.40. "
                   "Step 2, change: $50.00 − $27.40 = <b>$22.60</b>. Check: $22.60 + $27.40 = $50.00. "
                   "($22.62 forgets the cash rounding.)"))
    its.append(story_add("It rained in Vancouver on Monday and Tuesday. 23.6 mm of rain fell on Monday and 17.8 mm fell on Tuesday. "
                         "How much rain fell over the two days?", ["23.6", "17.8"], "mm", "Put the two days together: add."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("At the track and field meet, %s ran the 100 m in 15.48 seconds and %s ran it in 14.92 seconds. "
                         "How many seconds faster was %s?" % (n1, n2, n2),
                         "15.48", "14.92", "seconds", "The faster runner has the smaller time. Find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("At a swim meet in Burnaby, %s swam 50 m freestyle in 44.85 seconds. Last year %s time was 46.3 seconds. "
                         "By how many seconds did %s improve?" % (n, his, he),
                         "46.3", "44.85", "seconds", "The improvement is the difference between the two times: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s buys two bags of Okanagan apples. One bag has a mass of 2.35 kg and the other has a mass of 1.875 kg. "
                         "What is the total mass?" % n, ["2.35", "1.875"], "kg", "Total means add."))
    its.append(story_sub("A chinook salmon in the Fraser River is 0.915 m long. A coho salmon is 0.68 m long. "
                         "How much longer is the chinook salmon?",
                         "0.915", "0.68", "m", "How much longer means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("A water bottle holds 1 L. %s drinks 0.375 L on a hike at Grouse Mountain. How much water is left?" % n,
                         "1", "0.375", "L", "Take away what %s drank: subtract." % he))
    its.append(story_sub("A roll of paper is 4 m long. The class cuts off 1.35 m for a Terry Fox Run banner. How much paper is left?",
                         "4", "1.35", "m", "Take the part cut off away: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s’s family walks 4.25 km on the Stanley Park seawall before lunch and 3.8 km after lunch. "
                         "How far do they walk altogether?" % n, ["4.25", "3.8"], "km", "Altogether means add."))
    n, he, his = P.next()
    its.append(story_sub("The Terry Fox Run at %s’s school is 5 km long. %s has run 3.275 km so far. How much farther does %s have to run?"
                         % (n, cap(he), he), "5", "3.275", "km", "How much farther means find what is left: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s pays by card for a book at $14.99 and a pencil case at $7.49. What is the total?" % n,
                         ["14.99", "7.49"], "", "Total means add. A card pays the exact amount.", is_money=True))
    its.append(story_sub("The art class has 1.25 kg of modelling clay. The students use 0.875 kg to make salmon and orca models. "
                         "How much clay is left?", "1.25", "0.875", "kg", "Take away what was used: subtract."))
    a, b, c = Decimal("30"), Decimal("9.45"), Decimal("7.85")
    assert a - b - c == Decimal("12.70") and b + c == Decimal("17.30")
    assert sub_no_annex("30", "17.3") == Decimal("13.3") and a - b == Decimal("20.55")
    n, he, his = P.next()
    its.append(mcq("%s has $30 at the school spring fair. %s buys a plant for $9.45 and a pie for $7.85. How much money does %s have left?" % (n, cap(he), he),
                   "$12.70", [money(sub_no_annex("30", "17.3")), money(b + c), money(a - b)],
                   "Step 1, money spent: $9.45 + $7.85 = $17.30. Step 2, money left: $30.00 − $17.30 = <b>$12.70</b>. "
                   "Check: $12.70 + $17.30 = $30.00."))
    n, he, his = P.next()
    its.append(story_add("%s measures the new snow at Whistler on three days: 18.5 cm, 9.7 cm and 6.4 cm. "
                         "What is the total snowfall?" % n,
                         ["18.5", "9.7", "6.4"], "cm", "Total means add all three days."))
    assert Decimal(8) - Decimal("3.625") == Decimal("4.375") and sub_no_annex("8", "3.625") == Decimal("5.625")
    assert sub_forgot_one("8", "3.625") == Decimal("5.375")
    its.append(mcq("What number goes in the box?  <b>☐ + 3.625 = 8</b>", "4.375", ["5.625", "5.375", "11.625"],
                   "Use subtraction: 8 − 3.625 = 8.000 − 3.625 = <b>4.375</b>. Check: 4.375 + 3.625 = 8.000 = 8. "
                   "(5.625 forgets to write the zeros: 8 − 3 = 5, then brings down .625. 11.625 adds instead of subtracting.)"))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("0.6") + Decimal("0.5") == Decimal("1.1") and add_concat(["0.6", "0.5"]) == "0.11"
    assert Decimal("4.5") + Decimal("2.375") == Decimal("6.875") and add_right_align(["4.5", "2.375"]) == Decimal("2.42")
    assert Decimal("3.786") + Decimal("2.548") == Decimal("6.334") and add_forgot_point_carry(["3.786", "2.548"]) == Decimal("5.334")
    assert Decimal(6) - Decimal("2.375") == Decimal("3.625") and sub_no_annex("6", "2.375") == Decimal("4.375")
    assert Decimal("5.003") - Decimal("1.26") == Decimal("3.743") and crosses_zero("5.003", "1.26")
    assert no_point(Decimal("6.875")) == Decimal(6875)
    assert cash("7.42") == Decimal("7.40") and cash("7.43") == Decimal("7.45") and cash("7.47") == Decimal("7.45") and cash("7.48") == Decimal("7.50")
    assert Decimal("2.79") + Decimal("1.68") == Decimal("4.47") and cash("4.47") == Decimal("4.45")
    return (
        "<h2>The idea: line up the decimal points</h2>"
        "<p>Add and subtract decimals the same way as whole numbers, but first <b>line up the decimal points</b>. "
        "Then ones are under ones, tenths under tenths, hundredths under hundredths and thousandths under thousandths. "
        "You can only add or subtract digits in the same place.</p>"
        "<h2>Different numbers of decimal places</h2>"
        "<p>Write zeros so both numbers have the same number of places. Zeros at the end do not change the value: 4.5 = 4.500.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.5", "2.375"], "+", answer="6.875", ghost=True, fs=34) +
        "<figcaption>4.5 + 2.375 = 4.500 + 2.375. Thousandths 0 + 5 = 5, hundredths 0 + 7 = 7, tenths 5 + 3 = 8, "
        "ones 4 + 2 = 6. Answer: 6.875.</figcaption></figure>"
        "<h2>Regroup like whole numbers</h2>"
        "<p>10 thousandths make 1 hundredth, 10 hundredths make 1 tenth, and 10 tenths make 1 one. "
        "When a column makes 10 or more, regroup. The 1 can cross the decimal point.</p>"
        "<figure class='sn-fig'>" + column_svg(["3.786", "2.548"], "+", answer="6.334", marks=True, fs=34) +
        "<figcaption>3.786 + 2.548: thousandths 6 + 8 = 14, write 4 and regroup 1 hundredth. "
        "Hundredths 8 + 4 + 1 = 13, write 3 and regroup 1 tenth. Tenths 7 + 5 + 1 = 13, write 3 and regroup 1 one. "
        "Ones 3 + 2 + 1 = 6. Answer: 6.334.</figcaption></figure>"
        "<h2>Subtract across zeros</h2>"
        "<p>To take a decimal from a whole number, give the whole number a decimal point and zeros: 6 = 6.000. "
        "When you regroup across zeros, each 0 becomes 9 and the place you need gets 10.</p>"
        "<figure class='sn-fig'>" + column_svg(["6", "2.375"], "-", answer="3.625", ghost=True, marks=True, fs=34) +
        "<figcaption>6 − 2.375 = 6.000 − 2.375. Regroup 1 one: 5 ones, 9 tenths, 9 hundredths and 10 thousandths. "
        "10 − 5 = 5, 9 − 7 = 2, 9 − 3 = 6, 5 − 2 = 3. Answer: 3.625.</figcaption></figure>"
        + ex("Example", "What is 5.003 − 1.26?",
             "Write 1.26 as 1.260. Thousandths: 3 − 0 = 3. Hundredths: 0 − 6 needs a regroup, and the tenths digit is 0 too. "
             "Regroup 1 one: 4 ones, 9 tenths, 10 hundredths. 10 − 6 = 4, 9 − 2 = 7, 4 − 1 = 3. "
             "Check: 3.743 + 1.26 = 5.003.", "3.743") +
        "<h2>Estimate first, then check</h2>"
        "<p>Round each number to the nearest whole number and do the easy calculation. "
        "4.5 + 2.375 is about 5 + 2 = 7, so 6.875 makes sense and 2.42 does not. "
        "Check a subtraction by adding back: 3.625 + 2.375 = 6.</p>"
        "<h2>Money in Canada: cash and card</h2>"
        "<p>Canada has no pennies. When you pay with <b>cash</b>, the total is rounded to the nearest 5¢. "
        "When you pay by <b>debit or credit card</b>, you pay the exact amount.</p>" +
        table(["Total ends in", "Cash total", "Example"], [
            ["1¢ or 2¢", "Round down to 0¢", "$7.42 → $7.40"],
            ["3¢ or 4¢", "Round up to 5¢", "$7.43 → $7.45"],
            ["6¢ or 7¢", "Round down to 5¢", "$7.47 → $7.45"],
            ["8¢ or 9¢", "Round up to the next 10¢", "$7.48 → $7.50"],
        ]) +
        ex("Example", "A muffin costs $2.79 and milk costs $1.68. How much do you pay with cash? With a card?",
           "Add: $2.79 + $1.68 = $4.47. Card: the exact amount, $4.47. Cash: $4.47 is closer to $4.45 than to $4.50.",
           "cash $4.45, card $4.47") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (4.5 + 2.375 = 2.42)", "Line up the decimal points. Write 4.5 as 4.500"],
            ["Writing 11 tenths as 0.11 (0.6 + 0.5 = 0.11)", "10 tenths make 1 one: 0.6 + 0.5 = 1.1"],
            ["Not writing the zeros (6 − 2.375 = 4.375)", "Write 6 as 6.000, then regroup to subtract"],
            ["Forgetting to regroup across the point (3.786 + 2.548 = 5.334)", "10 tenths make 1 one. Add the 1 to the ones"],
            ["Dropping the decimal point (4.5 + 2.375 = 6875)", "Bring the point straight down into the answer"],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract decimals to thousandths in Grade 5?",
     "a": "Line up the decimal points, write zeros in empty places, then add or subtract from the right like whole numbers: 4.5 + 2.375 = 4.500 + 2.375 = 6.875."},
    {"q": "Why is 0.6 + 0.5 not 0.11?",
     "a": "0.6 + 0.5 is 6 tenths + 5 tenths = 11 tenths, and 10 tenths make 1 whole, so the answer is 1.1. 0.11 is only 11 hundredths, which is less than 0.6."},
    {"q": "How do you subtract a decimal from a whole number, like 6 − 2.375?",
     "a": "Write the whole number with a decimal point and zeros: 6 = 6.000. Regroup across the zeros (each 0 becomes 9) and subtract: 6.000 − 2.375 = 3.625. Check by adding: 3.625 + 2.375 = 6."},
    {"q": "How is cash rounded in Canada without pennies?",
     "a": "A cash total is rounded to the nearest 5¢: totals ending in 1, 2, 6 or 7 cents round down, and totals ending in 3, 4, 8 or 9 cents round up. Debit and credit card payments are charged the exact amount."},
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
                    assert dec(num) <= 3, (it["q"], c)


def gen():
    rnd = random.Random(55808)
    P = People(rnd)
    seen = set()
    sets = [set_line_up(P, rnd, seen), set_places(P, rnd, seen), set_zeros(P, rnd, seen), set_estimate(P), set_words(P)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "adding-and-subtracting-decimals", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Adding and Subtracting Decimals",
        "seo_title": "Grade 5 Adding and Subtracting Decimals Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Adding and Subtracting Decimals",
        "domain": "Computational fluency",
        "standard_code": "Grade 5: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Addition and subtraction of decimals to thousandths",
        "meta_desc": "Free Grade 5 math worksheets on adding and subtracting decimals to thousandths, matched to the BC curriculum: "
                     "line up the decimal points, add numbers with different decimal places, subtract across zeros, "
                     "estimate to check, and solve money problems with cash rounded to 5¢ and measurement problems. "
                     "100 questions with an answer key.",
        "key_big": "Line up the decimal points, then add or subtract like whole numbers.",
        "key_sub": "Write zeros in empty places (4.5 = 4.500, 6 = 6.000) so every digit has a partner. 10 tenths make 1 whole, "
                   "so 0.6 + 0.5 = 1.1, not 0.11. Estimate to check: 4.5 + 2.375 is about 7, so the answer is 6.875.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
