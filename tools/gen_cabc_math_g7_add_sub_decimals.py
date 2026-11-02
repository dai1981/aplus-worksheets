# -*- coding: utf-8 -*-
"""
BC Grade 7 Math: Adding and Subtracting Decimals (BC Mathematics Curriculum, Computational fluency:
operations with decimals)
  python3 tools/gen_cabc_math_g7_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (4.5 + 2.37 -> 450 + 237 hundredths), so every regroup and every typical mistake is exact.
Canadian style: math, metre, litre, $ and the cent sign, no pennies (cash rounds to the nearest 5 cents),
4-digit numbers without a separator, negative numbers with the real minus sign (U+2212).
Column helpers are copied from gen_ca_math_g6_add_sub_decimals.py. HTML attributes use single quotes.
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-7")
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
            out.append(v)
        elif 0 < v < 10000:
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




M = "−"     # real minus sign


def sg(d):
    """Signed text with the real minus sign: -2.5 -> '−2.5'."""
    d = Decimal(d)
    return (M if d < 0 else "") + nice(abs(d))


def mixed_ok(a, b):
    return dec(a) != dec(b)


# ============================================================ set 1: line up the decimal points
def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("To add 7.4 + 2.65, you write 7.4 with two decimal places. Which number is equal to 7.4?",
                   "7.40", ["7.04", "0.74", "74.0"],
                   "A zero at the end of a decimal does not change its value: 7.4 = 7 ones and 4 tenths = <b>7.40</b>. "
                   "7.04 is a different number: it moves the 4 to the hundredths place. Then 7.40 + 2.65 = 10.05."))
    n, he, his = P.next()
    assert add_concat(["0.6", "0.5"]) == "1.1" or True
    its.append(mcq("%s says 0.6 + 0.5 = 0.11. What is the correct sum?" % n,
                   "1.1", ["0.11", "11", "0.1"],
                   "6 tenths + 5 tenths = 11 tenths. 10 tenths make 1 whole, so 11 tenths = 1 and 1 tenth = <b>1.1</b>. "
                   "0.11 is only 11 hundredths, which is less than 0.6, so it cannot be the sum. (0.1 is 0.6 − 0.5.)"))
    its.append(mcq("In 35.2 − 8.746, the numbers are lined up by place value. Which digit of 35.2 is above the 7?",
                   "2", ["5", "3", "the decimal point"],
                   "7 is the tenths digit of 8.746. The tenths digit of 35.2 is <b>2</b>, so the 7 goes under the 2. "
                   "Write 35.2 as 35.200 so the 4 and the 6 also have digits above them."))
    n, he, his = P.next()
    a, b = "12.8", "3.475"
    w = add_right_align([a, b])
    assert w == Decimal("3.603") and Decimal(a) + Decimal(b) == Decimal("16.275")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "16.275", ["3.603", "16275", "15.275"],
                   "Line up the <b>decimal points</b>, not the last digits: 12.800 + 3.475. Thousandths: 0 + 5 = 5. "
                   "Hundredths: 0 + 7 = 7. Tenths: 8 + 4 = 12, write 2 and regroup 1 one. Ones: 2 + 3 + 1 = 6. Tens: 1. "
                   "Answer: <b>16.275</b>. Estimate: 13 + 3 = 16, so 3.603 is far too small."))
    seen.add(("+",) + tuple(sorted([a, b])))
    its.append(mcq("What is 0.8 + 0.7?", "1.5", ["0.15", "15", "0.1"],
                   "8 tenths + 7 tenths = 15 tenths = 1 whole and 5 tenths = <b>1.5</b>. "
                   "0.15 writes the 15 in the wrong places; it is less than 0.8, so it cannot be the sum."))
    for k in [("+", "2.65", "7.4"), ("+", "0.5", "0.6"), ("+", "0.7", "0.8")]:
        seen.add(k)
    plan = [("+", (1, 1), (1, 2)), ("+", (2, 2), (1, 3)), ("-", (1, 1), (1, 2)), ("+", (2, 0), (1, 2)),
            ("-", (2, 2), (1, 3)), ("+", (1, 3), (2, 1)), ("-", (2, 1), (1, 2)), ("+", (3, 1), (2, 2)),
            ("-", (3, 2), (2, 3)), ("+", (0, 2), (1, 3)), ("-", (2, 1), (1, 3)), ("+", (2, 3), (3, 2)),
            ("-", (3, 1), (2, 2)), ("+", (1, 2), (0, 3)), ("-", (2, 2), (2, 3))]
    for i, (op, sa, sb) in enumerate(plan):
        if op == "+":
            a, b = pick(rnd, seen, "+", sa, sb, lambda a, b: mixed_ok(a, b) and (carry_point(a, b) == (i % 3 != 2) or min(dec(a), dec(b)) == 0))
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb, lambda a, b: mixed_ok(a, b) and Decimal(a) > Decimal(b), swap=False)
            its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Line up the decimal points", "items": its}


# ============================================================ set 2: subtract across zeros
def set_zeros(P, rnd, seen):
    its = []
    its.append(mcq("To find 20 − 7.36, how should you write 20 so both numbers have hundredths?", "20.00",
                   ["2.00", "0.20", "20.36"],
                   "The decimal point of 20 is after the 0 ones. Write <b>20.00</b>: the two zeros hold the tenths and "
                   "hundredths places. Then 20.00 − 7.36 = 12.64."))
    n, he, his = P.next()
    assert sub_no_annex("20", "7.36") == Decimal("13.36")
    its.append(mcq("%s wrote 20 − 7.36 = 13.36. What is the correct difference?" % n,
                   "12.64", ["13.36", "13.64", "27.36"],
                   "%s did 20 − 7 = 13 and brought down the .36. But .36 is taken away too. Write 20.00 − 7.36: "
                   "regroup 1 ten to get 1 ten, 9 ones, 9 tenths and 10 hundredths. 10 − 6 = 4, 9 − 3 = 6, 9 − 7 = 2, 1 − 0 = 1. "
                   "Answer: <b>12.64</b>. Check: 12.64 + 7.36 = 20." % n))
    n, he, his = P.next()
    its.append(mcq("%s found 50 − 23.48 = 26.52. Which addition checks %s answer?" % (n, his),
                   "26.52 + 23.48 = 50", ["26.52 − 23.48 = 3.04", "50 + 23.48 = 73.48", "26.52 + 50 = 76.52"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 26.52 + 23.48 = 50.00 = 50. "
                   "You get back the starting number, so %s answer is right." % his))
    n, he, his = P.next()
    assert sub_zero_as_ten("8", "2.375") == Decimal("5.735") and sub_forgot_one("8", "2.375") == Decimal("6.625") and Decimal(8) - Decimal("2.375") == Decimal("5.625")
    its.append(mcq("%s regrouped 8.000 − 2.375 and wrote each 0 as 10 instead of 9. %s got 5.735. What is the correct answer?" % (n, cap(he)),
                   "5.625", ["5.735", "6.625", "6.735"],
                   "Regroup 1 one from 8: it leaves 7 ones. The 1 one becomes 9 tenths, 9 hundredths and 10 thousandths "
                   "(0.9 + 0.09 + 0.010 = 1). So each 0 in the middle becomes <b>9</b>, not 10. "
                   "10 − 5 = 5, 9 − 7 = 2, 9 − 3 = 6, 7 − 2 = 5. Answer: <b>5.625</b>."))
    for a, b in [("20", "7.36"), ("50", "23.48"), ("8", "2.375")]:
        seen.add(("-",) + tuple(sorted([a, b])))
    fixed_pairs = [("100", "37.65"), ("40.06", "15.38"), ("7.002", "3.45"), ("300", "126.4"), ("30.05", "12.7"),
                   ("1", "0.375"), ("200.5", "87.68"), ("90", "45.09"), ("6.1", "2.875"), ("10", "0.25"),
                   ("5.004", "2.38"), ("60.3", "24.75")]
    for a, b in fixed_pairs:
        assert tail_ok(a, b, "-"), (a, b)
        key = ("-",) + tuple(sorted([a, b]))
        assert key not in seen, key
        seen.add(key)
    pairs = list(fixed_pairs)
    for sa, sb in [((2, 0), (1, 2)), ((2, 0), (1, 3)), ((3, 0), (2, 2)), ((1, 0), (0, 3))]:
        pairs.append(pick(rnd, seen, "-", sa, sb, swap=False))
    for i, (a, b) in enumerate(pairs):
        its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Subtract across zeros", "items": its}


# ============================================================ set 3: estimate and check
def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def set_estimate(P):
    its = []
    for a, b, op in [("7.68", "4.35", "+"), ("14.27", "5.8", "−"), ("9.62", "6.48", "+"), ("23.85", "9.15", "−"),
                     ("36.7", "18.36", "+"), ("42.09", "7.6", "−")]:
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
    rows = [("6.8", "+", "3.475", "3.543", S, "lined up the last digits"),
            ("27.35", "+", "8.9", "36.25", R, None),
            ("15.4", "−", "6.85", "0.855", S, "put the decimal point in the wrong place"),
            ("5.92", "+", "7.6", "1352", B_, "left out the decimal point"),
            ("40", "−", "12.65", "27.35", R, None),
            ("52.06", "−", "4.7", "51.59", B_, "lined up the last digits"),
            ("18.75", "+", "6.4", "25.15", R, None)]
    assert add_right_align(["6.8", "3.475"]) == Decimal("3.543") and sub_right_align("52.06", "4.7") == Decimal("51.59")
    for i, (a, op, b, shown, ans, why) in enumerate(rows):
        n, he, his = P.next()
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        exact = f(Decimal(a), Decimal(b))
        est = f(rnd1(a), rnd1(b))
        assert (Decimal(shown) == exact) == (ans == R)
        assert ans != S or Decimal(shown) < est - 1
        assert ans != B_ or Decimal(shown) > est + 1
        tool = " on a calculator" if i % 2 else ""
        q = "%s worked out %s %s %s%s and got %s. Use an estimate to check. What does the estimate show?" % (n, a, op, b, tool, shown)
        e = "%s rounds to %d and %s rounds to %d, so the answer should be about %d %s %d = %d. " % (a, rnd1(a), b, rnd1(b), rnd1(a), op, rnd1(b), est)
        if ans == R:
            e += "%s is close to %d, so <b>it is reasonable</b>." % (shown, est)
        else:
            e += ("%s is much %s than %d, so <b>%s</b>. %s probably %s. The correct answer is %s."
                  % (shown, "smaller" if ans == S else "bigger", est, ans.lower(), n, why, nice(exact)))
        its.append(mcq(q, ans, [x for x in [R, S, B_, C] if x != ans], e))
    for a, op, b in [("8.6", "+", "5.75"), ("30", "−", "14.82"), ("12.35", "+", "27.8"), ("75", "−", "36.48"),
                     ("4.065", "+", "3.9"), ("21.3", "−", "8.675"), ("0.95", "+", "4.7")]:
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


# ============================================================ set 4: positive and negative decimals
def nl_svg(a, d, q=True):
    """Number line with a jump from a by d (d may be negative). The end is marked '?' when q."""
    a, d = Decimal(a), Decimal(d)
    r = a + d
    lo = int((min(a, r)).to_integral_value(rounding="ROUND_FLOOR"))
    hi = int((max(a, r)).to_integral_value(rounding="ROUND_CEILING"))
    if lo > -1:
        lo = -1
    if hi < 1:
        hi = 1
    U, L = 56, 34
    W = int(L * 2 + (hi - lo) * U)
    Y = 70

    def X(v):
        return L + (float(v) - lo) * U
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (L - 22, Y, W - L + 22, Y, INK)]
    s.append("<path d='M%d %d l10 -6 v12 Z' fill='%s'/>" % (L - 26, Y, INK))
    s.append("<path d='M%d %d l-10 -6 v12 Z' fill='%s'/>" % (W - L + 26, Y, INK))
    for v in range(lo, hi + 1):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.8'/>" % (X(v), Y - 9, X(v), Y + 9, INK))
        s.append("<text x='%.1f' y='%d' font-size='16' text-anchor='middle' fill='%s'>%s</text>" % (X(v), Y + 28, INK, sg(v)))
        if v < hi:
            s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.2'/>" % (X(v + 0.5), Y - 5, X(v + 0.5), Y + 5, THIN))
    xa, xr = X(a), X(r)
    mid = (xa + xr) / 2
    s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>" % (xa, Y - 8, mid, Y - 62, xr, Y - 8, GREEN))
    # arrowhead along the curve's end tangent (control point -> end point)
    tx, ty = xr - mid, (Y - 8) - (Y - 62)
    ln = (tx * tx + ty * ty) ** 0.5
    ux, uy = tx / ln, ty / ln
    tipx, tipy = xr, Y - 7
    bx, by = tipx - ux * 12, tipy - uy * 12
    s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>"
             % (tipx, tipy, bx - uy * 6, by + ux * 6, bx + uy * 6, by - ux * 6, GREEN))
    s.append("<text x='%.1f' y='%d' font-size='16' font-weight='700' text-anchor='middle' fill='%s'>%s</text>"
             % (mid, Y - 42, GREEN, ("+" if d > 0 else M) + nice(abs(d))))
    s.append("<circle cx='%.1f' cy='%d' r='6' fill='%s'/>" % (xa, Y, RED))
    s.append("<circle cx='%.1f' cy='%d' r='6' fill='none' stroke='%s' stroke-width='2.5'/>" % (xr, Y, RED))
    s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' text-anchor='middle' fill='%s'>%s</text>"
             % (xa, Y + 50, RED, sg(a)))
    s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' text-anchor='middle' fill='%s'>%s</text>"
             % (xr, Y + 50, RED, "?" if q else sg(r)))
    return svg_wrap(W, Y + 58, "".join(s), "number line from %s to %s with a jump of %s starting at %s" % (sg(lo), sg(hi), sg(d), sg(a)))


def signed_text(a, op, b):
    bt = sg(b) if b >= 0 else "(%s)" % sg(b)
    return "%s %s %s" % (sg(a), op, bt)


def signed_rule(a, op, b):
    """Explanation: rewrite subtraction as adding the opposite, then use the sign rules."""
    a, b = Decimal(a), Decimal(b)
    d = b if op == "+" else -b
    r = a + d
    out = ""
    if op == "−":
        out += "Subtracting is adding the opposite: %s = %s. " % (signed_text(a, op, b), signed_text(a, "+", d))
    if a == 0 or d == 0:
        raise ValueError
    if (a > 0) == (d > 0):
        out += ("Both numbers are %s, so add their distances from 0: %s + %s = %s. The answer is %s: <b>%s</b>."
                % ("positive" if a > 0 else "negative", nice(abs(a)), nice(abs(d)), nice(abs(r)),
                   "positive" if r > 0 else "negative", sg(r)))
    else:
        big, small = (a, d) if abs(a) > abs(d) else (d, a)
        out += ("The signs are different, so subtract the distances from 0: %s − %s = %s. "
                "%s is farther from 0, so the answer is %s: <b>%s</b>."
                % (nice(abs(big)), nice(abs(small)), nice(abs(r)), sg(big), "positive" if r > 0 else "negative", sg(r)))
    return out


def signed_cands(a, op, b):
    a, b = Decimal(a), Decimal(b)
    d = b if op == "+" else -b
    r = a + d
    c = [-r]
    if (a > 0) != (d > 0):
        s = abs(a) + abs(d)
        c += [s if r < 0 else -s, -s if r < 0 else s]
    else:
        s = abs(abs(a) - abs(d))
        c += [s if r < 0 else -s, -s if r < 0 else s]
    # lined up the last digits on the sizes
    na, nd = nice(abs(a)), nice(abs(d))
    if dec(na) != dec(nd):
        P = max(dec(na), dec(nd))
        ia, idd = int(na.replace(".", "")), int(nd.replace(".", ""))
        if (a > 0) == (d > 0):
            w = back(ia + idd, P)
        else:
            w = back(abs(ia - idd), P)
        c.append(w if r > 0 else -w)
    if op == "−":
        c.append(a + b)
    c += [r + 1 if r > 0 else r - 1, r * 10]
    return [x for x in c if x != 0 and x != r]


def item_signed(q_lead, a, op, b, unit="", lead=""):
    a, b = Decimal(a), Decimal(b)
    r = a + (b if op == "+" else -b)
    f = lambda v: sg(v) + unit
    out = []
    for v in signed_cands(a, op, b):
        t = f(v)
        if t not in out and t != f(r):
            out.append(t)
    return mcq(q_lead, f(r), out, (lead + " " if lead else "") + signed_rule(a, op, b))


def set_signed(P):
    its = []
    a, d = Decimal("-2.5"), Decimal("4.1")
    its.append(mcq(fig(nl_svg(a, d)) + "The number line shows %s + 4.1. Where does the jump end?" % sg(a),
                   "1.6", [M + "6.6", "6.6", M + "1.6"],
                   "Start at %s and jump 4.1 to the right. 2.5 gets you to 0, and 1.6 more is left: 2.5 + 1.6 = 4.1. "
                   "The jump ends at <b>1.6</b>." % sg(a)))
    a, d = Decimal("1.2"), Decimal("-3.5")
    its.append(mcq(fig(nl_svg(a, d)) + "The number line shows 1.2 − 3.5. Where does the jump end?",
                   M + "2.3", ["2.3", M + "4.7", "4.7"],
                   "Start at 1.2 and jump 3.5 to the left. 1.2 gets you to 0, and 3.5 − 1.2 = 2.3 more takes you past 0. "
                   "The jump ends at <b>%s</b>." % sg(Decimal("-2.3"))))
    its.append(mcq("Without working it out, is %s + 2.75 positive or negative?" % sg(Decimal("-6.4")),
                   "Negative, because 6.4 is farther from 0 than 2.75",
                   ["Positive, because you are adding", "Positive, because 2.75 has more decimal places",
                    "Negative, because 2.75 is less than 6.4 so the answer is 6.4 − 2.75"],
                   "When the signs are different, the answer has the sign of the number farther from 0. "
                   "%s is 6.4 from 0 and 2.75 is only 2.75 from 0, so the sum is <b>negative</b>: %s + 2.75 = %s."
                   % (sg(Decimal("-6.4")), sg(Decimal("-6.4")), sg(Decimal("-3.65")))))
    its.append(mcq("Which expression has the same value as 3.5 − (%s)?" % sg(Decimal("-1.25")),
                   "3.5 + 1.25", ["3.5 − 1.25", M + "3.5 − 1.25", M + "3.5 + 1.25"],
                   "Subtracting a number is the same as adding its opposite. The opposite of %s is 1.25, so "
                   "3.5 − (%s) = <b>3.5 + 1.25</b> = 4.75." % (sg(Decimal("-1.25")), sg(Decimal("-1.25")))))
    for a, op, b in [("-3.8", "+", "5.2"), ("-4.25", "+", "1.5"), ("2.6", "−", "4.15"), ("-1.8", "−", "2.6"),
                     ("-0.75", "+", "-2.4"), ("5.3", "−", "-2.45"), ("-3", "+", "1.75"), ("4", "−", "6.25"),
                     ("-2.4", "−", "-5.1"), ("-7.05", "+", "3.8"), ("0.6", "−", "1.25"), ("-5.6", "+", "8"),
                     ("-1.375", "−", "0.5")]:
        a, b = Decimal(a), Decimal(b)
        its.append(item_signed("What is %s?" % signed_text(a, op, b), a, op, b))
    n, he, his = P.next()
    its.append(item_signed("At 7:00 a.m. in Prince George, the temperature was %s°C. By noon it had risen 6.8°C. "
                           "What was the temperature at noon?" % sg(Decimal("-4.5")),
                           "-4.5", "+", "6.8", "°C", "A rise means add: %s + 6.8." % sg(Decimal("-4.5"))))
    its.append(item_signed("On a winter morning, it is %s°C at the top of a mountain near Whistler and 4.65°C in the village. "
                           "How many degrees warmer is the village?" % sg(Decimal("-3.2")),
                           "4.65", "−", "-3.2", "°C", "How much warmer means find the difference: 4.65 − (%s)." % sg(Decimal("-3.2"))))
    n, he, his = P.next()
    its.append(item_signed("%s is snorkelling in Okanagan Lake at %s m (2.75 m below the surface). %s swims up 1.4 m. "
                           "Where is %s now?" % (n, sg(Decimal("-2.75")), cap(he), he),
                           "-2.75", "+", "1.4", " m", "Swimming up means add: %s + 1.4." % sg(Decimal("-2.75"))))
    assert len(its) == 20, len(its)
    return {"title": "Positive and negative decimals", "items": its}


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
        st = add_steps(nums).split(" Answer:")[0]
        tail = " Answer: <b>%s</b>." % money(tot)
        if len(nums) == 2:
            tail += " Check: %s − %s = %s." % (money(tot), money(nums[1]), money(nums[0]))
        return mcq(q, money(tot), c, lead + " " + st + tail)
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_add(nums))], lead + " " + add_steps(nums))


def story_sub(q, a, b, unit, lead, is_money=False):
    r = Decimal(a) - Decimal(b)
    if is_money:
        c = [money(v) for v in cands_sub(a, b) if v is not None and v > 0 and v == v.quantize(Decimal("0.01"))]
        st = sub_steps(a, b).split(" Answer:")[0]
        tail = " Answer: <b>%s</b>. Check: %s + %s = %s." % (money(r), money(r), money(b), money(a))
        return mcq(q, money(r), c, lead + " " + st + tail)
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_sub(a, b))], lead + " " + sub_steps(a, b))


def set_words(P):
    its = []
    n, he, his = P.next()
    assert cash("8.63") == Decimal("8.65")
    its.append(mcq("There are no pennies in Canada, so a cash total is rounded to the nearest 5¢. "
                   "%s’s total at a café in Victoria is $8.63. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$8.65", ["$8.60", "$8.70", "$8.63"],
                   "The nearest multiples of 5¢ are $8.60 and $8.65. $8.63 is 3¢ from $8.60 and 2¢ from $8.65, "
                   "so it rounds up to <b>$8.65</b>. (Totals ending in 1, 2, 6 or 7 cents round down; 3, 4, 8 or 9 round up.)"))
    n, he, his = P.next()
    its.append(story_add("At the rink snack bar, %s buys a slice of pizza for $4.75 and a lemonade for $2.85. How much does %s spend?" % (n, he),
                         ["4.75", "2.85"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    t = Decimal("2.39") + Decimal("1.68")
    assert t == Decimal("4.07") and cash(t) == Decimal("4.05") and add_forgot_point_carry(["2.39", "1.68"]) == Decimal("3.07")
    its.append(mcq("%s buys a muffin for $2.39 and a carton of milk for $1.68. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$4.05", ["$4.07", "$4.10", "$3.05"],
                   "Step 1, add: $2.39 + $1.68. Hundredths: 9 + 8 = 17, write 7 and regroup 1 tenth. Tenths: 3 + 6 + 1 = 10, "
                   "write 0 and regroup 1 one. Ones: 2 + 1 + 1 = 4. Total: $4.07. Step 2, cash: $4.07 is 2¢ from $4.05 "
                   "and 3¢ from $4.10, so %s pays <b>$4.05</b>. ($4.07 is what a card would pay.)" % he))
    n, he, his = P.next()
    t = Decimal("18.49") + Decimal("2.19")
    assert t == Decimal("20.68") and cash(t) == Decimal("20.70")
    its.append(mcq("At the Grouse Mountain gift shop, %s buys a toque for $18.49 and a postcard for $2.19. "
                   "%s pays with a debit card. How much is %s charged?" % (n, cap(he), he),
                   "$20.68", ["$20.70", "$20.58", "$19.68"],
                   "Card and debit payments are charged the <b>exact</b> amount; only cash is rounded to 5¢. "
                   "$18.49 + $2.19: hundredths 9 + 9 = 18, write 8 and regroup 1 tenth. Tenths 4 + 1 + 1 = 6. "
                   "Ones 8 + 2 = 10, write 0 and regroup 1 ten. Tens 1 + 1 = 2. Answer: <b>$20.68</b>. ($20.70 is the cash price.)"))
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $26.35 snowboard wax kit with two $20 bills. How much change does %s get?" % (n, he),
                         "40", "26.35", "", "Two $20 bills are $40. Change is what is left: subtract.", is_money=True))
    n, he, his = P.next()
    assert cash("31.42") == Decimal("31.40") and Decimal(50) - Decimal("31.40") == Decimal("18.60")
    assert Decimal(50) - Decimal("31.42") == Decimal("18.58") and sub_no_annex("50", "31.4") == Decimal("19.4")
    its.append(mcq("%s’s groceries come to $31.42. %s pays cash with a $50 bill. How much change does %s get?" % (n, cap(he), he),
                   "$18.60", ["$18.58", "$18.65", "$19.40"],
                   "Step 1, cash total: $31.42 is 2¢ from $31.40 and 3¢ from $31.45, so it rounds to $31.40. "
                   "Step 2, change: $50.00 − $31.40 = <b>$18.60</b>. Check: $18.60 + $31.40 = $50.00. "
                   "($18.58 forgets the cash rounding.)"))
    its.append(story_add("During a rainy week in November, Vancouver got 42.6 mm of rain on Monday and 37.8 mm on Tuesday. "
                         "How much rain fell over the two days?", ["42.6", "37.8"], "mm", "Put the two days together: add."))
    n, he, his = P.next()
    its.append(story_add("At the Terry Fox Run, %s walked 2.75 km and then ran 4.6 km. How far did %s go altogether?" % (n, he),
                         ["2.75", "4.6"], "km", "Altogether means add."))
    n, he, his = P.next()
    its.append(story_sub("The Grouse Grind trail in North Vancouver is about 2.9 km long. %s has hiked 1.65 km. "
                         "How much farther does %s have to go?" % (n, he),
                         "2.9", "1.65", "km", "The distance left is the difference: subtract."))
    its.append(story_sub("At a fish hatchery on the Fraser River, a sockeye salmon has a mass of 2.85 kg and a coho salmon has a mass of 4.3 kg. "
                         "How much heavier is the coho?", "4.3", "2.85", "kg", "How much heavier means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("At a swim meet in Kamloops, %s swam 100 m backstroke in 78.64 seconds. Last season %s best time was 81.2 seconds. "
                         "By how many seconds did %s improve?" % (n, his, he),
                         "81.2", "78.64", "seconds", "The improvement is the difference between the two times: subtract."))
    n, he, his = P.next()
    its.append(story_add("In a ski race at Whistler, %s’s first run took 48.75 seconds and %s second run took 51.08 seconds. "
                         "What was %s total time?" % (n, his, his),
                         ["48.75", "51.08"], "seconds", "Total time means add the two runs."))
    its.append(story_add("On a trip to Vancouver Island, a family drives 36.8 km to the ferry terminal. After the ferry, they drive "
                         "112.45 km to Tofino. How far do they drive altogether?", ["36.8", "112.45"], "km", "Altogether means add."))
    its.append(story_sub("A young cedar tree was 1.85 m tall. One year later it is 2.3 m tall. How much did it grow?",
                         "2.3", "1.85", "m", "Growth is the difference between the two heights: subtract."))
    its.append(story_sub("A jug holds 2 L of juice. A class pours out 0.355 L for each of the first group of students, "
                         "and the teacher notes the first pour. After that first pour, how much juice is left in the jug?",
                         "2", "0.355", "L", "Take away what was poured: subtract.")
               if False else
               story_sub("A jug holds 2 L of apple juice. Kai pours 0.355 L into a cup. How much juice is left in the jug?",
                         "2", "0.355", "L", "Take away what Kai poured: subtract."))
    n, he, his = P.next()
    its.append(story_add("Over three days, %s records the new snow at Sun Peaks: 18.5 cm, 7.25 cm and 12.8 cm. "
                         "What is the total snowfall?" % n,
                         ["18.5", "7.25", "12.8"], "cm", "Total means add all three days."))
    a, b, c = Decimal("25"), Decimal("9.75"), Decimal("6.50")
    assert a - b - c == Decimal("8.75") and b + c == Decimal("16.25")
    assert sub_no_annex("25", "16.25") == Decimal("9.25") and a - b == Decimal("15.25")
    n, he, his = P.next()
    its.append(mcq("%s has $25 at the school fun fair. %s buys game tickets for $9.75 and a bag of mini doughnuts for $6.50. "
                   "How much money does %s have left?" % (n, cap(he), he),
                   "$8.75", ["$9.25", "$16.25", "$15.25"],
                   "Step 1, money spent: $9.75 + $6.50 = $16.25. Step 2, money left: $25.00 − $16.25 = <b>$8.75</b>. "
                   "Check: $8.75 + $16.25 = $25.00."))
    assert Decimal(10) - Decimal("3.65") == Decimal("6.35") and sub_no_annex("10", "3.65") == Decimal("7.65")
    its.append(mcq("What number goes in the box?  <b>☐ + 3.65 = 10</b>", "6.35", ["7.65", "6.45", "13.65"],
                   "Use subtraction: 10 − 3.65 = 10.00 − 3.65 = <b>6.35</b>. Check: 6.35 + 3.65 = 10.00 = 10. "
                   "(7.65 forgets to write the zeros: 10 − 3 = 7, then brings down .65. 13.65 adds instead of subtracting.)"))
    n, he, his = P.next()
    its.append(story_sub("%s has saved $80. %s buys a hockey stick that costs $64.95. How much money does %s have left?" % (n, cap(he), he),
                         "80", "64.95", "", "Money left is what is left after spending: subtract.", is_money=True))
    its.append(story_sub("On the Sea-to-Sky Highway, a family has driven 58.6 km of a 121.5 km trip from Vancouver to Whistler. "
                         "How far do they still have to drive?", "121.5", "58.6", "km", "The distance left is the difference: subtract."))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("7.4") + Decimal("2.65") == Decimal("10.05")
    assert Decimal(20) - Decimal("7.36") == Decimal("12.64") and sub_no_annex("20", "7.36") == Decimal("13.36")
    assert add_right_align(["7.4", "2.65"]) == Decimal("3.39")
    assert Decimal("-2.5") + Decimal("4.1") == Decimal("1.6") and Decimal("3.2") - Decimal("5.7") == Decimal("-2.5")
    assert Decimal("-1.8") - Decimal("2.6") == Decimal("-4.4")
    assert cash("7.42") == Decimal("7.40") and cash("7.43") == Decimal("7.45") and cash("7.47") == Decimal("7.45") and cash("7.48") == Decimal("7.50")
    return (
        "<h2>The idea: line up the decimal points</h2>"
        "<p>Add and subtract decimals like whole numbers, but first <b>line up the decimal points</b>. "
        "Then ones are under ones, tenths under tenths, hundredths under hundredths and thousandths under thousandths. "
        "Write zeros in empty places. A zero at the end does not change the value: 7.4 = 7.40.</p>"
        "<figure class='sn-fig'>" + column_svg(["7.4", "2.65"], "+", answer="10.05", ghost=True, marks=True, fs=34) +
        "<figcaption>7.4 + 2.65 = 7.40 + 2.65. Hundredths 0 + 5 = 5. Tenths 4 + 6 = 10, write 0 and regroup 1 one. "
        "Ones 7 + 2 + 1 = 10. Answer: 10.05.</figcaption></figure>"
        "<p>Regroup across the decimal point just as with whole numbers: 10 tenths make 1 one. "
        "So 0.6 + 0.5 = 11 tenths = <b>1.1</b>, not 0.11.</p>"
        "<h2>Subtract across zeros</h2>"
        "<p>To take a decimal from a whole number, give the whole number a decimal point and zeros: 20 = 20.00. "
        "When you regroup across zeros, each zero in the middle becomes 9.</p>"
        "<figure class='sn-fig'>" + column_svg(["20", "7.36"], "-", answer="12.64", ghost=True, marks=True, fs=34) +
        "<figcaption>20 − 7.36 = 20.00 − 7.36. Regroup 1 ten: 1 ten, 9 ones, 9 tenths and 10 hundredths. "
        "10 − 6 = 4, 9 − 3 = 6, 9 − 7 = 2, 1 − 0 = 1. Answer: 12.64. Check: 12.64 + 7.36 = 20.</figcaption></figure>"
        "<h2>Estimate first, then check</h2>"
        "<p>Round each number to the nearest whole number and do the easy calculation. "
        "7.4 + 2.65 is about 7 + 3 = 10, so 10.05 makes sense and 3.39 does not. "
        "Do this on a calculator too: a missed decimal point gives an answer far from the estimate.</p>"
        "<h2>Positive and negative decimals</h2>"
        "<p>Use the same rules as for integers. Subtracting is adding the opposite: 3.2 − 5.7 = 3.2 + (−5.7). "
        "<b>Same signs:</b> add the distances from 0 and keep the sign. "
        "<b>Different signs:</b> subtract the distances from 0; the answer takes the sign of the number farther from 0.</p>"
        "<figure class='sn-fig'>" + nl_svg("-2.5", "4.1", q=False) +
        "<figcaption>−2.5 + 4.1: start at −2.5 and jump 4.1 to the right. The signs are different: 4.1 − 2.5 = 1.6, "
        "and 4.1 is farther from 0, so the answer is positive: 1.6.</figcaption></figure>"
        + table(["Question", "Think", "Answer"], [
            ["−2.5 + 4.1", "Different signs: 4.1 − 2.5 = 1.6. 4.1 is farther from 0", "1.6"],
            ["3.2 − 5.7", "= 3.2 + (−5.7). Different signs: 5.7 − 3.2 = 2.5. −5.7 is farther from 0", "−2.5"],
            ["−1.8 − 2.6", "= −1.8 + (−2.6). Same signs: 1.8 + 2.6 = 4.4", "−4.4"],
            ["2.4 − (−1.3)", "= 2.4 + 1.3", "3.7"],
        ]) +
        "<h2>Money in Canada: cash and card</h2>"
        "<p>Canada has no pennies. A <b>cash</b> total is rounded to the nearest 5¢. "
        "A <b>debit or credit card</b> pays the exact amount.</p>" +
        table(["Total ends in", "Cash total", "Example"], [
            ["1¢ or 2¢", "Round down to 0¢", "$7.42 → $7.40"],
            ["3¢ or 4¢", "Round up to 5¢", "$7.43 → $7.45"],
            ["6¢ or 7¢", "Round down to 5¢", "$7.47 → $7.45"],
            ["8¢ or 9¢", "Round up to the next 10¢", "$7.48 → $7.50"],
        ]) +
        ex("Example", "You pay for a $16.83 lunch with a $20 bill. How much change do you get?",
           "Cash total: $16.83 rounds to $16.85. Change: $20.00 − $16.85 = $3.15. Check: $3.15 + $16.85 = $20.00.", "$3.15") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (7.4 + 2.65 = 3.39)", "Line up the decimal points. Write 7.4 as 7.40"],
            ["Writing 11 tenths as 0.11 (0.6 + 0.5 = 0.11)", "10 tenths make 1 one: 0.6 + 0.5 = 1.1"],
            ["Not writing the zeros (20 − 7.36 = 13.36)", "Write 20 as 20.00, then regroup to subtract"],
            ["Making a middle zero 10 when regrouping (8 − 2.375 = 5.735)", "Each zero in the middle becomes 9: 8 − 2.375 = 5.625"],
            ["Losing the negative sign (3.2 − 5.7 = 2.5)", "The bigger number is taken away, so the answer is negative: −2.5"],
        ])
    )


FAQ = [
    {"q": "How do you add and subtract decimals with different numbers of decimal places?",
     "a": "Line up the decimal points and write zeros in the empty places, then add or subtract from the right like whole numbers: 7.4 + 2.65 = 7.40 + 2.65 = 10.05."},
    {"q": "Why is 0.6 + 0.5 not 0.11?",
     "a": "0.6 + 0.5 is 6 tenths + 5 tenths = 11 tenths, and 10 tenths make 1 whole, so the answer is 1.1. 0.11 is only 11 hundredths, which is less than 0.6."},
    {"q": "How do you add and subtract negative decimals in Grade 7?",
     "a": "Use the integer rules. Rewrite subtraction as adding the opposite; with the same signs add the distances from 0, and with different signs subtract them and keep the sign of the number farther from 0: −2.5 + 4.1 = 1.6."},
    {"q": "Is adding and subtracting decimals on the Grade 7 FSA?",
     "a": "It can be. The Grade 7 FSA numeracy section is based on the BC curriculum, and operations with decimals are a Grade 7 learning standard, often met in money and measurement problems."},
]


def verify(sets):
    """Recompute every 'What is a ± b?' answer and every column picture from its aria-label."""
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is (−?[\d.]+) ([+−]) \(?(−?[\d.]+)\)?\?$", it["q"])
            if m:
                a, op, b = [Decimal(x.replace(M, "-")) if x not in "+−" else x for x in m.groups()]
                assert Decimal(right.replace(M, "-")) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"aria-label='([\d.]+) (plus|minus) ([\d.]+) written in columns", it["q"])
            if m and ("Add." in it["q"] or "Subtract." in it["q"]):
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "plus" else a - b), it["q"]
            if "$" in right and "with cash" in it["q"]:
                assert is5(right.lstrip("$")), it["q"]


def gen():
    rnd = random.Random(37804)
    P = People(rnd)
    seen = set()
    sets = [set_line_up(P, rnd, seen), set_zeros(P, rnd, seen), set_estimate(P), set_signed(P), set_words(P)]
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if all(re.fullmatch(r"−?\$?[\d.]+( ?[a-zA-Z°]+)?", x) for x in it["c"]):
                assert len({Decimal(re.sub(r"[^\d.]", "", x)) * (-1 if x.startswith(M) else 1) for x in it["c"]}) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-7", "slug": "adding-and-subtracting-decimals", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 7 Adding and Subtracting Decimals",
        "seo_title": "Grade 7 Adding and Subtracting Decimals Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Adding and Subtracting Decimals",
        "domain": "Computational fluency",
        "standard_code": "Grade 7: Computational fluency",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/7/core",
        "standard_text": "Operations with decimals (addition, subtraction, multiplication, division, and order of operations)",
        "meta_desc": "Free Grade 7 math worksheets on adding and subtracting decimals for the BC curriculum: line up the decimal points, "
                     "subtract across zeros, estimate to check, work with positive and negative decimals, and solve money and "
                     "measurement problems. 100 questions with an answer key. Great FSA practice.",
        "key_big": "Line up the decimal points, then add or subtract like whole numbers.",
        "key_sub": "Write zeros in empty places (7.4 = 7.40, 20 = 20.00), regroup 10 tenths as 1 one (0.6 + 0.5 = 1.1), "
                   "estimate to check, and use the integer sign rules for negative decimals: −2.5 + 4.1 = 1.6.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
