# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Adding and Subtracting Decimals (MOE 2021 Primary Mathematics Syllabus, Standard:
Primary 4 Decimals, adding and subtracting decimals up to 2 decimal places)
  python3 tools/gen_sg_maths_p4_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (3.5 + 1.25 -> 350 + 125 hundredths), so every renaming step and every typical mistake is exact.
Singapore style: maths, metre, litre (ℓ), renaming, bar models, $ and ¢ (no 1¢), 4-digit numbers without a
separator. Column helpers are adapted from gen_cabc_math_g5_add_sub_decimals.py; bar models from
gen_sg_maths_p5_decimals.py. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
THIN = "#8a8a8a"
HEADFILL = "#cfe6d6"
PARTFILL = "#fde3c8"
ORANGE = "#b35900"
NB = "\u00a0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]
PLACE = ["thousandths", "hundredths", "tenths", "ones", "tens", "hundreds", "thousands"]
ONE = ["thousandth", "hundredth", "tenth", "one", "ten", "hundred", "thousand"]


# ------------------------------------------------------------ numbers
def dec(s):
    """Decimal places as written: '3.6' -> 1, '5' -> 0."""
    return len(s.split(".")[1]) if "." in s else 0


def nice(d):
    """Shortest exact text for a Decimal (no separator below 10 000)."""
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
    k = max(max(nlen(x) for x in ints), P + 1)
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
            msg = "%s: %s = %d, write %d and rename %d %s as %d %s." % (
                P_, expr, t, t % 10, t // 10 * 10, pname(i, P), t // 10, oname(i + 1, P) + ("s" if t >= 20 else ""))
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
    rest = " The other places add without renaming." if len(regs) < k else ""
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
                msg = ("%s: %d − %d needs renaming, but the next place is 0. Rename 1 %s: the %s become %d, "
                       "each 0 becomes 9, and the %s become %d. %d − %d = %d."
                       % (P_, cur, db[i], oname(j, P), pname(j, P), old - 1, pname(i, P), d[i], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d needs renaming. Rename 1 %s as 10 %s: %d − %d = %d."
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
    rest = " The other places subtract without renaming." if len(regs) < k else ""
    return (head + " " + " ".join(regs) + rest + end).replace("  ", " ")


# ------------------------------------------------------------ typical mistakes (each returns a Decimal or text, or None)
def col_info(ints, P=0):
    k = max(max(nlen(x) for x in ints), P + 1)
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
    """Did not rename 10 tenths as 1 one (forgot the 1 that crosses the decimal point)."""
    P, ints = scale(nums)
    if P == 0:
        return None
    k, sums, carries = col_info(ints, P)
    c = carries[P - 1]
    if not c:
        return None
    return back(sum(ints) - c * 10 ** P, P)


def add_forgot_carry(nums, which):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints, P)
    cols = [i for i in range(k - 1) if carries[i] and i != P - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return back(sum(ints) - carries[i] * 10 ** (i + 1), P)


def add_no_carry(nums):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints, P)
    if not any(carries[:k - 1]):
        return None
    return back(sum((sums[i] % 10 if i < k - 1 else sums[i]) * 10 ** i for i in range(k)), P)


def add_concat(nums):
    """Wrote a two-digit column total in place: 0.8 + 0.45 = 0.125. Only when exactly one column renames."""
    P, ints = scale(nums)
    if P == 0:
        return None
    k, sums, carries = col_info(ints, P)
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
    k, sums, carries = col_info(ints, P)
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
    """Renaming across a zero: made the zero 10 instead of 9. 5.00 − 2.37 = 2.73."""
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
    """Renamed across zeros but left the zeros as 0 (did not change them to 9): 2 − 0.008 = 1.002.
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
    """Renamed from the ones but forgot to take 1 from the ones: one too high (10 − 4.28 = 6.72)."""
    P, (A, B) = scale([a, b])
    if P == 0:
        return None
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    if P >= k:                 # no ones digit (0.915 − 0.68)
        return None
    nd = borrow_digits(A, B)
    if nd[P] == d[P]:          # the ones digit was not used in a rename
        return None
    return Decimal(a) - Decimal(b) + 1


def sub_right_align(a, b):
    if dec(a) == dec(b):
        return None
    P = max(dec(a), dec(b))
    r = int(a.replace(".", "")) - int(b.replace(".", ""))
    return back(r, P) if r > 0 else None


def renames_sub(a, b):
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
            if dec(v) <= 2:
                out.append(v)
        elif 0 < v < 10000 and dec(nice(v)) <= 2:          # Primary 4: up to 2 decimal places
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
    marks: red rename marks (carried 1s, or crossed digits with the new digit above)."""
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
            k, sums, carries = col_info(ints, P)
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
    k, sums, carries = col_info(ints, P)
    return bool(P and P - 1 < len(carries) and carries[P - 1])


def pick(rnd, seen, op, sa, sb, cond=lambda a, b: True, swap=True):
    for _ in range(20000):
        a, b = rnd_num(rnd, *sa), rnd_num(rnd, *sb)
        if op == "+" and swap and rnd.random() < 0.5:
            a, b = b, a
        key = (op,) + tuple(sorted([a, b]))
        if key in seen or not tail_ok(a, b, op):
            continue
        if op == "-" and (Decimal(a) - Decimal(b) < Decimal("0.5") or renames_sub(a, b) == 0
                          or Decimal(a) == 2 * Decimal(b)):
            continue
        if not cond(a, b):
            continue
        seen.add(key)
        return a, b
    raise RuntimeError((op, sa, sb))




def crosses_zero(a, b):
    """True when some rename has to pass through a 0 (5.003 − 1.26, 7 − 2.35)."""
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




# ------------------------------------------------------------ figures: bar models (from gen_sg_maths_p5_decimals.py)
def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


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
    """Bracket from x1 to x2 at y; ticks point to the bar (down if up=True). Label beyond it."""
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_parts(parts, total_lab, BW=500):
    """One bar split into parts drawn to scale. parts = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(Decimal(v) for v, _ in parts)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [HEADFILL, PARTFILL, "#fff"]
    for i, (v, lab) in enumerate(parts):
        w = float(Decimal(v) / tot) * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 3], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts), total_lab))


def bar_compare(rows, diff_lab, BW=420):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    v1, v2 = Decimal(v1), Decimal(v2)
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2 / v1) * BW
    o = []
    for i, (nm, w, lab, fill) in enumerate([(n1, BW, l1, HEADFILL), (n2, w2, l2, PARTFILL)]):
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


# ============================================================ set 1: line up the decimal points
def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("You add 4.36 + 2.5 in columns with the decimal points lined up. Which digit of 2.5 goes under the 3?",
                   "5", ["2", "6", "the decimal point"],
                   "The 3 in 4.36 is in the tenths place. Line up the decimal points and tenths sit under tenths: "
                   "the tenths digit of 2.5 is <b>5</b>. The 2 is in the ones place, so it goes under the 4."))
    its.append(mcq("In 37.26 − 5.8, the digits are lined up by place value. Which digit of 37.26 is above the 5?",
                   "7", ["3", "2", "6"],
                   "5 is the ones digit of 5.8. The ones digit of 37.26 is <b>7</b>, so the 5 goes under the 7. "
                   "The 3 is in the tens place and has no digit under it."))
    n, he, his = P.next()
    assert Decimal("0.6") + Decimal("0.5") == Decimal("1.1") and add_concat(["0.6", "0.5"]) == "0.11"
    its.append(mcq("%s says 0.6 + 0.5 = 0.11. What is the correct answer?" % n, "1.1", ["0.11", "11", "1.01"],
                   "6 tenths + 5 tenths = 11 tenths. Rename 10 tenths as 1 one, so 11 tenths = 1 one and 1 tenth = <b>1.1</b>. "
                   "0.11 is only 11 hundredths, which is less than 0.6 alone."))
    seen.add(("+", "0.5", "0.6"))
    plan = [("+", (1, 1), (1, 1), "nopt"), ("+", (1, 2), (1, 2), "nopt"), ("-", (1, 1), (1, 1), None),
            ("+", (0, 1), (0, 1), "pt"), ("-", (2, 1), (1, 1), None),
            ("+", (1, 1), (1, 1), "pt"), ("+", (1, 2), (1, 2), "pt"), ("-", (1, 2), (1, 2), None),
            ("+", (2, 1), (1, 1), "pt"), ("-", (2, 2), (1, 2), None),
            ("+", (0, 2), (0, 2), "pt"), ("-", (2, 1), (2, 1), None), ("+", (2, 2), (2, 2), "pt"),
            ("-", (2, 2), (2, 2), None), ("+", (2, 2), (1, 2), "pt"), ("-", (1, 2), (0, 2), None),
            ("+", (2, 1), (2, 1), "pt")]
    for i, (op, sa, sb, kind) in enumerate(plan):
        if op == "+":
            cond = (lambda a, b: not carry_point(a, b)) if kind == "nopt" else (lambda a, b: carry_point(a, b))
            a, b = pick(rnd, seen, "+", sa, sb, cond)
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb, lambda a, b: not crosses_zero(a, b), swap=False)
            its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Line up the decimal points", "items": its}


# ============================================================ set 2: different numbers of places
def set_places(P, rnd, seen):
    its = []
    its.append(mcq("To add 3.5 + 1.25, you write 3.5 with two decimal places. Which number is equal to 3.5?",
                   "3.50", ["3.05", "0.35", "35.0"],
                   "A zero at the end of a decimal does not change its value: 3.5 = 3 ones and 5 tenths = <b>3.50</b>. "
                   "3.05 is wrong: it moves the 5 to the hundredths place."))
    assert Decimal("3.5") + Decimal("1.25") == Decimal("4.75") and add_right_align(["3.5", "1.25"]) == Decimal("1.6")
    its.append(mcq("What is 3.5 + 1.25?", "4.75", ["1.6", "475", "47.5"],
                   "Line up the decimal points and write 3.5 as 3.50. Hundredths: 0 + 5 = 5. Tenths: 5 + 2 = 7. "
                   "Ones: 3 + 1 = 4. Answer: <b>4.75</b>. 1.6 comes from lining up the last digits (35 + 125 = 160). 475 drops the decimal point."))
    n, he, his = P.next()
    a, b = "5.6", "2.13"
    w = add_right_align([a, b])
    assert w == Decimal("2.69") and Decimal(a) + Decimal(b) == Decimal("7.73")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "7.73", ["2.69", "773", "77.3"],
                   "Line up the <b>decimal points</b>, not the last digits: 5.60 + 2.13. "
                   "Hundredths: 0 + 3 = 3. Tenths: 6 + 1 = 7. Ones: 5 + 2 = 7. Answer: <b>7.73</b>. "
                   "Estimate: 6 + 2 = 8, so 2.69 is far too small."))
    its.append(mcq("To find 9 + 3.47, you can write 9 with a decimal point. Which number is equal to 9?",
                   "9.00", ["0.09", "0.9", "900"],
                   "A whole number has its decimal point after the ones digit, so 9 = <b>9.00</b>. "
                   "Then the 9 ones sit over the 3 ones: 9.00 + 3.47 = 12.47."))
    n, he, his = P.next()
    a, b = "18", "4.25"
    w = add_right_align([a, b])
    assert w == Decimal("4.43") and add_left_align([a, b]) == Decimal("6.05")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "22.25", fmt_all([w, Decimal("6.05"), Decimal("2225")]),
                   "18 is a whole number, so its point is after the 8: 18 = 18.00 (not 1.8). Line up the points: 18.00 + 4.25. "
                   "Hundredths: 0 + 5 = 5. Tenths: 0 + 2 = 2. Ones: 8 + 4 = 12, write 2 and rename 10 ones as 1 ten. "
                   "Tens: 1 + 1 = 2. Answer: <b>22.25</b>."))
    for k in [("+", "1.25", "3.5"), ("+", "2.13", "5.6"), ("+", "3.47", "9"), ("+", "18", "4.25")]:
        seen.add(k)
    its.append(item_add(["0.7", "0.46"], False))
    its.append(item_add(["2.35", "4.8"], True))
    seen.add(("+", "0.46", "0.7")); seen.add(("+", "2.35", "4.8"))
    plan = [("+", (1, 1), (1, 2)), ("+", (1, 2), (0, 1)), ("+", (2, 1), (1, 2)), ("-", (1, 2), (1, 1)),
            ("+", (1, 0), (1, 2)), ("-", (2, 2), (1, 1)), ("+", (2, 2), (1, 1)), ("-", (1, 1), (0, 2)),
            ("+", (1, 1), (0, 2)), ("-", (2, 1), (1, 2)), ("+", (2, 1), (2, 2)), ("-", (2, 2), (1, 0)),
            ("+", (1, 0), (2, 1))]
    for i, (op, sa, sb) in enumerate(plan):
        if op == "+":
            a, b = pick(rnd, seen, "+", sa, sb, lambda a, b: dec(a) != dec(b) and (carry_point(a, b) == (i % 3 != 0) or min(dec(a), dec(b)) == 0))
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb, lambda a, b: dec(a) != dec(b) and not crosses_zero(a, b), swap=False)
            its.append(item_sub(a, b, i % 2 == 0))
    assert len(its) == 20, len(its)
    return {"title": "Different numbers of decimal places", "items": its}


# ============================================================ set 3: renaming and subtracting from whole numbers
def set_zeros(P, rnd, seen):
    its = []
    assert Decimal(7) - Decimal("2.35") == Decimal("4.65")
    its.append(mcq("To find 7 − 2.35, how should you write 7 so both numbers have hundredths?", "7.00",
                   ["0.07", "0.70", "7.35"],
                   "7 is 7 ones, and its decimal point is after the 7. Write <b>7.00</b>: the two zeros hold the tenths "
                   "and hundredths places. Then 7.00 − 2.35 = 4.65."))
    n, he, his = P.next()
    assert Decimal("4.65") - Decimal("2.35") == Decimal("2.3") and Decimal("4.65") + 7 == Decimal("11.65")
    its.append(mcq("%s found 7 − 2.35 = 4.65. Which addition checks %s answer?" % (n, his),
                   "4.65 + 2.35 = 7", ["4.65 − 2.35 = 2.3", "7 + 2.35 = 9.35", "4.65 + 7 = 11.65"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 4.65 + 2.35 = 7.00 = 7. "
                   "You get back the starting number, so %s answer is right." % his))
    n, he, his = P.next()
    assert sub_no_annex("10", "3.45") == Decimal("7.45") and sub_forgot_one("10", "3.45") == Decimal("7.55") and Decimal(10) - Decimal("3.45") == Decimal("6.55")
    its.append(mcq("%s says 10 − 3.45 = 7.45. What is the correct answer?" % n, "6.55", ["7.45", "7.55", "13.45"],
                   "%s did not write the zeros: 10 − 3 = 7, then brought down .45. Write 10 as 10.00 and rename 1 ten: "
                   "0 tens, 9 ones, 9 tenths and 10 hundredths. 10 − 5 = 5, 9 − 4 = 5, 9 − 3 = 6. "
                   "Answer: <b>6.55</b>. Check: 6.55 + 3.45 = 10. "
                   "7.55 forgets to take 1 from the 10 when renaming. 13.45 adds instead of subtracting." % n))
    # pairs used in set 4 (16 − 6.28, 40 − 18.35): keep them out of this set
    seen.add(("-",) + tuple(sorted(["16", "6.28"])))
    seen.add(("-",) + tuple(sorted(["40", "18.35"])))
    seen.add(("-",) + tuple(sorted(["10", "3.45"])))
    # renaming once, then twice, then across zeros and from whole numbers
    fixed_pairs = [("7.32", "2.58"), ("8.4", "3.7"), ("5.16", "2.9"), ("12.5", "4.83"),
                   ("5", "2.37"), ("1", "0.35"), ("20", "6.75"), ("4.05", "1.37"), ("6", "0.25"),
                   ("30.04", "12.67"), ("3", "1.4"), ("8.02", "3.05"), ("2", "0.08")]
    for a, b in fixed_pairs:
        assert tail_ok(a, b, "-") and renames_sub(a, b) >= 1, (a, b)
        key = ("-",) + tuple(sorted([a, b]))
        assert key not in seen, key
        seen.add(key)
    pairs = list(fixed_pairs)
    shapes = [((1, 0), (1, 2)), ((2, 0), (1, 2)), ((2, 0), (2, 1)), ((1, 0), (0, 2))]
    for sa, sb in shapes:
        a, b = pick(rnd, seen, "-", sa, sb, crosses_zero, swap=False)
        pairs.append((a, b))
    for i, (a, b) in enumerate(pairs):
        its.append(item_sub(a, b, i % 2 == 0))
    assert len(its) == 20, len(its)
    return {"title": "Subtract with renaming and from whole numbers", "items": its}


# ============================================================ set 4: estimate first and check
def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def set_estimate(P):
    its = []
    for a, b, op in [("6.82", "3.29", "+"), ("12.15", "4.9", "−"), ("8.47", "5.6", "+"), ("19.7", "6.15", "−"),
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
    rows = [("5.6", "+", "2.13", "2.69", S, "lined up the last digits instead of the decimal points"),
            ("18.6", "+", "7.45", "26.05", R, None),
            ("9.2", "−", "4.65", "45.5", B_, "put the decimal point in the wrong place"),
            ("3.75", "+", "6.8", "1055", B_, "left out the decimal point"),
            ("24.6", "−", "8.75", "15.85", R, None),
            ("31.08", "−", "6.5", "37.58", B_, "added instead of subtracting"),
            ("12.4", "+", "3.65", "16.05", R, None)]
    assert Decimal("31.08") + Decimal("6.5") == Decimal("37.58") and Decimal("9.2") - Decimal("4.65") == Decimal("4.55")
    assert add_right_align(["5.6", "2.13"]) == Decimal("2.69") and no_point(Decimal("10.55")) == Decimal(1055)
    for i, (a, op, b, shown, ans, why) in enumerate(rows):
        n, he, his = P.next()
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        exact = f(Decimal(a), Decimal(b))
        est = f(rnd1(a), rnd1(b))
        assert (Decimal(shown) == exact) == (ans == R)
        assert ans != S or Decimal(shown) < est - 1
        assert ans != B_ or Decimal(shown) > est + 1
        q = "%s worked out %s %s %s and got %s. Use an estimate to check. What does the estimate show?" % (n, a, op, b, shown)
        e = "%s rounds to %d and %s rounds to %d, so the answer should be about %d %s %d = %d. " % (a, rnd1(a), b, rnd1(b), rnd1(a), op, rnd1(b), est)
        if ans == R:
            e += "%s is close to %d, so <b>it is reasonable</b>." % (shown, est)
        else:
            e += ("%s is much %s than %d, so <b>%s</b>. %s probably %s. The correct answer is %s."
                  % (shown, "smaller" if ans == S else "bigger", est, ans.lower(), n, why, nice(exact)))
        its.append(mcq(q, ans, [x for x in [R, S, B_, C] if x != ans], e))
    for a, op, b in [("8.7", "+", "4.56"), ("16", "−", "6.28"), ("9.45", "+", "12.7"), ("40", "−", "18.35"),
                     ("6.07", "+", "2.9"), ("13.4", "−", "5.85"), ("0.85", "+", "2.6")]:
        if op == "+":
            exact = Decimal(a) + Decimal(b)
            cc = cands_add([a, b])
        else:
            exact = Decimal(a) - Decimal(b)
            cc = cands_sub(a, b)
        f = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
        est = f(rnd1(a), rnd1(b))
        far = [v for v in cc if v is not None and not isinstance(v, str) and v > 0 and abs(v - exact) >= Decimal("1.5")
               and dec(nice(v)) <= 2]
        its.append(mcq("Estimate first, then choose the correct answer without working it out exactly: %s %s %s" % (a, op, b),
                       nice(exact), fmt_all(far),
                       "%s %s %s is about %d %s %d = %d. Only <b>%s</b> is close to %d. Check by working it out: %s"
                       % (a, op, b, rnd1(a), op, rnd1(b), est, nice(exact), est,
                          (add_steps([a, b]) if op == "+" else sub_steps(a, b)).replace("Line up the decimal points. ", ""))))
    assert len(its) == 20, len(its)
    return {"title": "Estimate and check", "items": its}


# ============================================================ set 5: word problems (money and measurement)
def story_e(lead, steps, ans, unit, is_money, check):
    """Lead + column steps, with the answer and the check written with $ or the unit."""
    body = steps.split(" Answer: ")[0]
    if is_money:
        return "%s %s Answer: <b>%s</b>. Check: %s." % (lead, body, money(ans), check)
    return "%s %s Answer: <b>%s %s</b>. Check: %s." % (lead, body, nice(ans), unit, check)


def story_add(q, nums, unit, lead, is_money=False, model=None):
    tot = sum(Decimal(n) for n in nums)
    q = (fig(model) if model else "") + q
    a, b = nums
    if is_money:
        c = [money(v) for v in cands_add(nums) if v is not None and not isinstance(v, str) and 0 < v < 10000
             and v == v.quantize(Decimal("0.01"))]
        chk = "%s − %s = %s" % (money(tot), money(b), money(a))
        return mcq(q, money(tot), c, story_e(lead, add_steps(nums), tot, unit, True, chk))
    c = [x for x in fmt_all(cands_add(nums)) if dec(x) <= 2]
    chk = "%s − %s = %s" % (nice(tot), b, a)
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (x, unit) for x in c],
               story_e(lead, add_steps(nums), tot, unit, False, chk))


def story_sub(q, a, b, unit, lead, is_money=False, model=None):
    r = Decimal(a) - Decimal(b)
    q = (fig(model) if model else "") + q
    if is_money:
        c = [money(v) for v in cands_sub(a, b) if v is not None and 0 < v < 10000 and v == v.quantize(Decimal("0.01"))]
        chk = "%s + %s = %s" % (money(r), money(b), money(a))
        return mcq(q, money(r), c, story_e(lead, sub_steps(a, b), r, unit, True, chk))
    c = [x for x in fmt_all(cands_sub(a, b)) if dec(x) <= 2]
    chk = "%s + %s = %s" % (nice(r), b, a)
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (x, unit) for x in c],
               story_e(lead, sub_steps(a, b), r, unit, False, chk))


def set_words(P):
    its = []
    # 1  money, add, bar model
    n, he, his = P.next()
    its.append(story_add("At the hawker centre, %s buys a plate of chicken rice for $4.50 and a cup of lime juice for $1.80. "
                         "How much does %s spend?" % (n, he),
                         ["4.50", "1.80"], "", "Put the two prices together: add.", is_money=True,
                         model=bar_parts([(450, "$4.50"), (180, "$1.80")], "?")))
    # 2  change
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $13.45 storybook with a $20 note. How much change does %s get?" % (n, he),
                         "20", "13.45", "", "Change is what is left: subtract.", is_money=True,
                         model=bar_parts([(1345, "$13.45"), (655, "?")], "$20")))
    # 3  cents and dollars
    n, he, his = P.next()
    assert Decimal("0.85") + Decimal("1.40") == Decimal("2.25")
    its.append(mcq("%s buys a pencil for 85¢ and a ruler for $1.40 at the school bookshop. How much does %s pay?" % (n, he),
                   "$2.25", ["$86.40", "$9.90", "$1.25"],
                   "Write the cents in dollars first: 85¢ = $0.85. $0.85 + $1.40: hundredths 5 + 0 = 5, tenths 8 + 4 = 12, "
                   "write 2 and rename 10 tenths as 1 one, ones 0 + 1 + 1 = 2. Answer: <b>$2.25</b>. "
                   "$86.40 adds 85 dollars. $9.90 uses 85¢ = $8.50. $1.25 forgets the renamed 1 one."))
    # 4  EZ-Link card
    n, he, his = P.next()
    its.append(story_sub("%s’s EZ-Link card has $12.40 on it. After a bus ride to the Singapore Zoo, it has $11.25 left. "
                         "How much was the bus fare?" % n,
                         "12.40", "11.25", "", "The fare is the difference between the two amounts: subtract.", is_money=True))
    # 5  mass, add, bar model
    n, he, his = P.next()
    its.append(story_add("%s’s mother buys 1.35 kg of rambutans and 0.9 kg of mangosteens at the market. "
                         "What is the total mass of the fruit?" % n,
                         ["1.35", "0.9"], "kg", "Total means add.",
                         model=bar_parts([(135, "1.35 kg"), (90, "0.9 kg")], "?")))
    # 6  ribbon left, bar model
    its.append(story_sub("Mrs Lim has a ribbon 4 m long. She cuts off 1.35 m to wrap a present for Children’s Day. "
                         "How much ribbon is left?",
                         "4", "1.35", "m", "Take the part cut off away: subtract.",
                         model=bar_parts([(135, "1.35 m"), (265, "?")], "4 m")))
    # 7  litres
    n, he, his = P.next()
    its.append(story_sub("%s’s water bottle has 1.5 ℓ of water. %s drinks 0.65 ℓ during the CCA session. "
                         "How much water is left?" % (n, cap(he)),
                         "1.5", "0.65", "ℓ", "Take away what %s drank: subtract." % he,
                         model=bar_parts([(65, "0.65 ℓ"), (85, "?")], "1.5 ℓ")))
    # 8  times, comparison
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("On Sports Day, %s ran 100 m in 16.25 s and %s ran it in 15.8 s. How many seconds faster was %s?"
                         % (n1, n2, n2),
                         "16.25", "15.8", "s", "The faster runner has the smaller time. Find the difference: subtract."))
    # 9  comparison, more than
    n1, _, _ = P.next()
    n2, h2, _ = P.next()
    T = Decimal("2.45") + Decimal("0.38")
    assert T == Decimal("2.83")
    its.append(mcq(fig(bar_compare([(n2, 283, "?"), (n1, 245, "2.45 m")], "0.38 m", BW=560)) +
                   "In the long jump, %s jumps 2.45 m. %s jumps 0.38 m farther than %s. How far does %s jump?" % (n1, n2, n1, n2),
                   "2.83 m", ["2.07 m", "2.73 m", "6.25 m"],
                   "%s’s bar is %s’s bar and 0.38 m more, so add: 2.45 + 0.38. Hundredths: 5 + 8 = 13, write 3 and rename "
                   "10 hundredths as 1 tenth. Tenths: 4 + 3 + 1 = 8. Ones: 2. Answer: <b>2.83 m</b>. "
                   "2.07 m subtracts instead of adding. 2.73 m forgets the renamed 1 tenth." % (n2, n1)))
    # 10  hawker, add
    n, he, his = P.next()
    its.append(story_add("%s’s family has breakfast at a coffee shop. A kaya toast set costs $3.80 and a plate of prata costs $5.50. "
                         "What is the total cost?" % n,
                         ["3.80", "5.50"], "", "Total cost means add.", is_money=True))
    # 11  two steps, money left, bar model
    n, he, his = P.next()
    sp = Decimal("4.60") + Decimal("7.85")
    assert sp == Decimal("12.45") and 20 - sp == Decimal("7.55") and sub_no_annex("20", "12.45") == Decimal("8.45")
    its.append(mcq(fig(bar_parts([(460, "$4.60"), (785, "$7.85"), (755, "?")], "$20")) +
                   "%s has $20. %s buys a cup of bubble tea for $4.60 and a book for $7.85. "
                   "How much money does %s have left?" % (n, cap(he), he),
                   "$7.55", ["$12.45", "$8.45", "$15.40"],
                   "Step 1, money spent: $4.60 + $7.85 = $12.45. Step 2, money left: $20.00 − $12.45 = <b>$7.55</b>. "
                   "Check: $7.55 + $12.45 = $20. $12.45 is the money spent, not left. $8.45 forgets to write $20 as $20.00. "
                   "$15.40 takes away only the bubble tea."))
    # 12  distance, add
    n, he, his = P.next()
    its.append(story_add("At Gardens by the Bay, %s’s class walks 2.6 km in the morning and 1.75 km in the afternoon. "
                         "How far do they walk altogether?" % n,
                         ["2.6", "1.75"], "km", "Altogether means add."))
    # 13  litres, add
    its.append(story_add("Mdm Wong has 2.4 ℓ of soup in a pot. She adds 0.85 ℓ of water. How much liquid is in the pot now?",
                         ["2.4", "0.85"], "ℓ", "Put the two amounts together: add."))
    # 14  mass comparison
    T = Decimal("2.15") - Decimal("1.6")
    assert T == Decimal("0.55")
    its.append(story_sub("A durian has a mass of 2.15 kg. A pineapple has a mass of 1.6 kg. How much heavier is the durian?",
                         "2.15", "1.6", "kg", "How much heavier means find the difference: subtract.",
                         model=bar_compare([("durian", 215, "2.15 kg"), ("pineapple", 160, "1.6 kg")], "?")))
    # 15  missing number
    assert Decimal(8) - Decimal("3.65") == Decimal("4.35") and sub_no_annex("8", "3.65") == Decimal("5.65")
    assert sub_forgot_one("8", "3.65") == Decimal("5.35")
    its.append(mcq("What number goes in the box?  <b>☐ + 3.65 = 8</b>", "4.35", ["5.65", "5.35", "11.65"],
                   "Use subtraction: 8 − 3.65 = 8.00 − 3.65 = <b>4.35</b>. Check: 4.35 + 3.65 = 8.00 = 8. "
                   "5.65 forgets to write the zeros: 8 − 3 = 5, then brings down .65. 11.65 adds instead of subtracting."))
    # 16  distance, MRT
    n, he, his = P.next()
    its.append(story_add("%s walks 0.85 km from %s HDB flat to the MRT station. Then %s takes the train 6.4 km to school. "
                         "How far does %s travel in all?" % (n, his, he, he),
                         ["0.85", "6.4"], "km", "In all means add."))
    # 17  mass comparison, bar model
    n, he, his = P.next()
    its.append(story_sub("%s has a mass of 32.5 kg. %s younger brother has a mass of 28.75 kg. "
                         "How much heavier is %s than %s brother?" % (n, cap(his), n, his),
                         "32.5", "28.75", "kg", "How much heavier means find the difference: subtract.",
                         model=bar_compare([(n, 3250, "32.5 kg"), ("brother", 2875, "28.75 kg")], "?")))
    # 18  two steps, less than, total
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    b2 = Decimal("15.30") - Decimal("2.85")
    assert b2 == Decimal("12.45") and b2 + Decimal("15.30") == Decimal("27.75")
    its.append(mcq(fig(bar_compare([(n1, 1530, "$15.30"), (n2, 1245, "?")], "$2.85")) +
                   "%s saves $15.30 in a month. %s saves $2.85 less than %s. How much do they save altogether?" % (n1, n2, n1),
                   "$27.75", ["$12.45", "$18.15", "$33.45"],
                   "Step 1, %s: $15.30 − $2.85 = $12.45. Step 2, altogether: $15.30 + $12.45 = <b>$27.75</b>. "
                   "$12.45 is only what %s saves. $18.15 adds $2.85 instead of taking it away. "
                   "$33.45 adds $15.30, $15.30 and $2.85." % (n2, n2)))
    # 19  ribbon, two pieces cut
    used = Decimal("1.25") + Decimal("2.4")
    assert used == Decimal("3.65") and 5 - used == Decimal("1.35")
    assert sub_no_annex("5", "3.65") == Decimal("2.65") and sub_forgot_one("5", "3.65") == Decimal("2.35")
    its.append(mcq(fig(bar_parts([(125, "1.25 m"), (240, "2.4 m"), (135, "?")], "5 m")) +
                   "A roll of paper for a National Day banner is 5 m long. The class cuts off 1.25 m and then 2.4 m. "
                   "How much paper is left?", "1.35 m", ["3.65 m", "2.65 m", "2.35 m"],
                   "Step 1, paper used: 1.25 m + 2.4 m = 3.65 m. Step 2, paper left: 5.00 m − 3.65 m = <b>1.35 m</b>. "
                   "Check: 1.35 + 3.65 = 5. 3.65 m is the paper used. 2.65 m forgets to write 5 as 5.00. "
                   "2.35 m forgets to take 1 from the ones when renaming."))
    # 20  litres, add
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_add("%s’s water bottle holds 0.75 ℓ. %s’s water bottle holds 1.2 ℓ. "
                         "How much water do the two bottles hold altogether?" % (n1, n2),
                         ["0.75", "1.2"], "ℓ", "Altogether means add."))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("0.6") + Decimal("0.5") == Decimal("1.1") and add_concat(["0.6", "0.5"]) == "0.11"
    assert Decimal("3.5") + Decimal("1.25") == Decimal("4.75") and add_right_align(["3.5", "1.25"]) == Decimal("1.6")
    assert Decimal("3.78") + Decimal("2.54") == Decimal("6.32") and add_forgot_point_carry(["3.78", "2.54"]) == Decimal("5.32")
    assert Decimal(10) - Decimal("3.45") == Decimal("6.55") and sub_no_annex("10", "3.45") == Decimal("7.45")
    assert Decimal("5.03") - Decimal("1.26") == Decimal("3.77") and crosses_zero("5.03", "1.26")
    assert no_point(Decimal("4.75")) == Decimal(475)
    assert Decimal(20) - Decimal("4.60") - Decimal("7.85") == Decimal("7.55")
    f4 = bar_parts([(460, "$4.60"), (785, "$7.85"), (755, "?")], "$20")
    return (
        "<h2>The idea: line up the decimal points</h2>"
        "<p>Add and subtract decimals the same way as whole numbers, but first <b>line up the decimal points</b>. "
        "Then ones are under ones, tenths under tenths and hundredths under hundredths. "
        "You can only add or subtract digits in the same place.</p>"
        "<h2>Different numbers of decimal places</h2>"
        "<p>Write a zero so both numbers have the same number of decimal places. A zero at the end does not change the value: 3.5 = 3.50.</p>"
        "<figure class='sn-fig'>" + column_svg(["3.5", "1.25"], "+", answer="4.75", ghost=True, fs=34) +
        "<figcaption>3.5 + 1.25 = 3.50 + 1.25. Hundredths 0 + 5 = 5, tenths 5 + 2 = 7, ones 3 + 1 = 4. "
        "Answer: 4.75.</figcaption></figure>"
        "<h2>Rename like whole numbers</h2>"
        "<p>10 hundredths = 1 tenth and 10 tenths = 1 one. "
        "When a column makes 10 or more, rename. The 1 can cross the decimal point.</p>"
        "<figure class='sn-fig'>" + column_svg(["3.78", "2.54"], "+", answer="6.32", marks=True, fs=34) +
        "<figcaption>3.78 + 2.54: hundredths 8 + 4 = 12, write 2 and rename 10 hundredths as 1 tenth. "
        "Tenths 7 + 5 + 1 = 13, write 3 and rename 10 tenths as 1 one. "
        "Ones 3 + 2 + 1 = 6. Answer: 6.32.</figcaption></figure>"
        "<h2>Subtract from a whole number</h2>"
        "<p>To take a decimal from a whole number, give the whole number a decimal point and zeros: 10 = 10.00. "
        "When you rename across zeros, each 0 becomes 9 and the place you need gets 10.</p>"
        "<figure class='sn-fig'>" + column_svg(["10", "3.45"], "-", answer="6.55", ghost=True, marks=True, fs=34) +
        "<figcaption>10 − 3.45 = 10.00 − 3.45. Rename 1 ten: 0 tens, 9 ones, 9 tenths and 10 hundredths. "
        "10 − 5 = 5, 9 − 4 = 5, 9 − 3 = 6. Answer: 6.55.</figcaption></figure>"
        + ex("Example 1", "What is 5.03 − 1.26?",
             "Hundredths: 3 − 6 needs renaming, but the tenths digit is 0. "
             "Rename 1 one: 4 ones, 9 tenths, 13 hundredths. 13 − 6 = 7, 9 − 2 = 7, 4 − 1 = 3. "
             "Check: 3.77 + 1.26 = 5.03.", "3.77") +
        "<h2>Estimate first, then check</h2>"
        "<p>Round each number to the nearest whole number and do the easy calculation. "
        "3.5 + 1.25 is about 4 + 1 = 5, so 4.75 makes sense and 1.6 does not. "
        "Check a subtraction by adding back: 6.55 + 3.45 = 10.</p>"
        "<h2>Word problems: draw a bar model</h2>"
        "<p>Draw the whole and the parts. Write money in dollars with 2 decimal places (85¢ = $0.85). "
        "Use the same unit for every number.</p>"
        "<figure class='sn-fig'>" + f4 +
        "<figcaption>Ali has $20. He spends $4.60 and $7.85. Money spent: $4.60 + $7.85 = $12.45. "
        "Money left: $20.00 − $12.45 = $7.55.</figcaption></figure>" +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (3.5 + 1.25 = 1.6)", "Line up the decimal points. Write 3.5 as 3.50"],
            ["Writing 11 tenths as 0.11 (0.6 + 0.5 = 0.11)", "Rename 10 tenths as 1 one: 0.6 + 0.5 = 1.1"],
            ["Not writing the zeros (10 − 3.45 = 7.45)", "Write 10 as 10.00, then rename to subtract"],
            ["Forgetting the 1 that crosses the point (3.78 + 2.54 = 5.32)", "10 tenths = 1 one. Add the 1 to the ones"],
            ["Dropping the decimal point (3.5 + 1.25 = 475)", "Bring the point straight down into the answer"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 adding and subtracting decimals?",
     "a": "In Primary 4, students add and subtract decimals up to 2 decimal places, such as 3.5 + 1.25 and 10 − 3.45. "
          "They estimate to check their answers and solve word problems with money and measurements."},
    {"q": "How do I explain adding decimals like 3.5 + 1.25 to my child?",
     "a": "Line up the decimal points and write 3.5 as 3.50, so every digit has a partner in the same place. "
          "Then add from the right like whole numbers: 3.50 + 1.25 = 4.75."},
    {"q": "What is the most common mistake when adding decimals?",
     "a": "The most common mistake is lining up the last digits instead of the decimal points, so 3.5 + 1.25 becomes 1.6. "
          "Another is writing 0.6 + 0.5 = 0.11: 6 tenths + 5 tenths = 11 tenths = 1.1."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Adding and subtracting decimals up to 2 decimal places is part of the Primary 4 Decimals topic in the "
          "MOE 2021 Primary Mathematics Syllabus (Standard Mathematics)."},
]


def mark_large(u, pattern):
    """Tag bar models so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    """Recompute every 'What is a ± b?' answer and every column picture from its aria-label."""
    n = 0
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is ([\d.]+) ([+−]) ([\d.]+)\?$", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "+" else a - b), it["q"]
                n += 1
            m = re.search(r"aria-label='([\d.]+) (plus|minus) ([\d.]+) written in columns", it["q"])
            if m and ("Add." in it["q"] or "Subtract." in it["q"]):
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "plus" else a - b), it["q"]
                n += 1
            m = re.search(r"without working it out exactly: ([\d.]+) ([+−]) ([\d.]+)$", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "+" else a - b), it["q"]
                n += 1
            for c in it["c"]:
                for num in re.findall(r"\d+\.\d+", c):
                    assert dec(num) <= 2, (it["q"], c)
                if "$" in c:
                    assert re.fullmatch(r"\$\d+\.\d\d", c), c
    return n


def gen():
    rnd = random.Random(64810)
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
            if all(re.fullmatch(r"\$?[\d.]+( [a-zA-Zℓ]+)?", x) for x in it["c"]):
                assert len({Decimal(re.sub(r"[^\d.]", "", x)) for x in it["c"]}) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "adding-and-subtracting-decimals", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Adding and Subtracting Decimals",
        "seo_title": "P4 Adding and Subtracting Decimals Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Adding and Subtracting Decimals",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Decimals",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Adding and subtracting decimals (up to 2 decimal places)",
        "meta_desc": "Free P4 maths: add and subtract decimals up to 2 decimal places, estimate to check, "
                     "and solve money and measurement problems. 100 questions with answers.",
        "key_big": "Line up the decimal points, then add or subtract like whole numbers.",
        "key_sub": "3.5 + 1.25 = 3.50 + 1.25 = 4.75, and 10 − 3.45 = 10.00 − 3.45 = 6.55.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
