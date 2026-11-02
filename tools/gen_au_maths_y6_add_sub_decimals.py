# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Adding and Subtracting Decimals (Australian Curriculum v9.0, AC9M6N04)
  python3 tools/gen_au_maths_y6_add_sub_decimals.py
All arithmetic uses decimal.Decimal (never float). Column work is done on whole numbers of the
smallest place (4.5 + 2.37 -> 450 + 237 hundredths), so every regroup and every typical mistake is exact.
Australian style: maths, metre, litre (L, mL), $ and c, 4-digit numbers without a separator.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
THIN = "#8a8a8a"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
PLACE = ["thousandths", "hundredths", "tenths", "ones", "tens", "hundreds", "thousands"]
ONE = ["thousandth", "hundredth", "tenth", "one", "ten", "hundred", "thousand"]


# ------------------------------------------------------------ numbers
def dec(s):
    """Decimal places as written: '3.6' -> 1, '5' -> 0."""
    return len(s.split(".")[1]) if "." in s else 0


def nice(d):
    """Shortest exact text for a Decimal (Australian style: no separator below 10 000)."""
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


# ============================================================ set 1: same number of places
def set_line_up(P, rnd, seen):
    its = []
    its.append(mcq("You add 3.42 + 5.17 in columns with the decimal points lined up. Which digit of 5.17 goes under the 4?",
                   "1", ["7", "5", "the decimal point"],
                   "The 4 in 3.42 is in the tenths place. Line up the decimal points and tenths sit under tenths: "
                   "the tenths digit of 5.17 is <b>1</b>. (7 is the hundredths digit, so it goes under the 2.)"))
    its.append(mcq("In 26.38 − 4.51, the digits are lined up by place value. Which digit of 26.38 is above the 4?",
                   "6", ["2", "3", "8"],
                   "4 is the ones digit of 4.51. The ones digit of 26.38 is <b>6</b>, so the 4 goes under the 6. "
                   "The 2 is in the tens place and has no digit under it."))
    seen.add(("+", "3.42", "5.17"))
    plan = [("+", (1, 1), (1, 1), "nopt"), ("+", (1, 2), (1, 2), "nopt"), ("+", (2, 1), (1, 1), "nopt"),
            ("-", (1, 2), (1, 2), None), ("-", (2, 1), (1, 1), None),
            ("+", (1, 1), (1, 1), "pt"), ("+", (1, 2), (1, 2), "pt"), ("+", (1, 2), (1, 2), "pt"),
            ("-", (1, 2), (1, 2), None), ("-", (2, 2), (1, 2), None),
            ("+", (2, 2), (1, 2), "pt"), ("+", (2, 2), (2, 2), "pt"), ("-", (2, 2), (2, 2), None),
            ("-", (2, 1), (2, 1), None), ("+", (1, 3), (1, 3), "pt"), ("-", (1, 3), (1, 3), None),
            ("+", (2, 3), (1, 3), "pt"), ("-", (2, 3), (1, 3), None)]
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
    its.append(mcq("To add 4.5 + 2.37, you write 4.5 with two decimal places. Which number is equal to 4.5?",
                   "4.50", ["4.05", "0.45", "45.0"],
                   "A zero at the end of a decimal does not change its value: 4.5 = 4 ones and 5 tenths = <b>4.50</b>. "
                   "4.05 is wrong: it moves the 5 to the hundredths place."))
    n, he, his = P.next()
    a, b = "4.5", "2.37"
    w = add_right_align([a, b])
    assert w == Decimal("2.82")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "6.87", ["2.82", "687", "0.687"],
                   "Line up the <b>decimal points</b>, not the last digits: 4.50 + 2.37. Hundredths: 0 + 7 = 7. "
                   "Tenths: 5 + 3 = 8. Ones: 4 + 2 = 6. Answer: <b>6.87</b>. "
                   "Estimate: 5 + 2 = 7, so 2.82 is far too small."))
    its.append(mcq("To find 12 + 3.48, you can write 12 with a decimal point. Which number is equal to 12?",
                   "12.00", ["0.12", "1.2", "120"],
                   "A whole number has its decimal point after the ones digit, so 12 = <b>12.00</b>. "
                   "Then the 2 ones sit over the 3 ones: 12.00 + 3.48 = 15.48."))
    n, he, his = P.next()
    a, b = "15", "2.38"
    w = add_right_align([a, b])
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "17.38", fmt_all([w, Decimal("3.88"), Decimal("1738")]),
                   "15 is a whole number, so its point is after the 5: 15 = 15.00 (not 1.5). Line up the points: 15.00 + 2.38. "
                   "Hundredths: 0 + 8 = 8. Tenths: 0 + 3 = 3. Ones: 5 + 2 = 7. Tens: bring down 1. Answer: <b>17.38</b>."))
    for k in [("+", "2.37", "4.5"), ("+", "12", "3.48"), ("+", "15", "2.38")]:
        seen.add(k)
    its.append(item_add(["0.6", "0.275"], False))
    its.append(item_add(["3.125", "4.6"], True))
    seen.add(("+", "0.275", "0.6")); seen.add(("+", "3.125", "4.6"))
    plan = [("+", (1, 1), (1, 2)), ("+", (1, 2), (0, 1)), ("+", (2, 1), (1, 2)), ("-", (1, 2), (1, 1)),
            ("+", (1, 0), (1, 2)), ("-", (2, 2), (1, 1)), ("+", (2, 2), (1, 1)), ("-", (1, 3), (1, 1)),
            ("+", (1, 1), (0, 3)), ("-", (2, 3), (1, 2)), ("+", (2, 1), (2, 3)), ("-", (2, 2), (1, 0)),
            ("+", (1, 3), (1, 2)), ("-", (2, 3), (2, 1))]
    for i, (op, sa, sb) in enumerate(plan):
        if op == "+":
            a, b = pick(rnd, seen, "+", sa, sb, lambda a, b: dec(a) != dec(b) and (carry_point(a, b) == (i % 3 != 0) or min(dec(a), dec(b)) == 0))
            its.append(item_add([a, b], i % 2 == 0))
        else:
            a, b = pick(rnd, seen, "-", sa, sb, swap=False)
            its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Different numbers of decimal places", "items": its}


# ============================================================ set 3: subtract with zeros
def set_zeros(P, rnd, seen):
    its = []
    its.append(mcq("To find 10 − 3.46, how should you write 10 so both numbers have hundredths?", "10.00",
                   ["1.00", "0.10", "10.46"],
                   "10 is 1 ten and 0 ones, and its decimal point is after the 0. Write <b>10.00</b>: two zeros hold the tenths "
                   "and hundredths places. Then 10.00 − 3.46 = 6.54."))
    n, he, his = P.next()
    its.append(mcq("%s found 10 − 3.46 = 6.54. Which addition checks %s answer?" % (n, his),
                   "6.54 + 3.46 = 10", ["6.54 − 3.46 = 3.08", "10 + 3.46 = 13.46", "6.54 + 10 = 16.54"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 6.54 + 3.46 = 10.00 = 10. "
                   "You get back the starting number, so %s answer is right." % his))
    fixed_pairs = [("10", "3.46"), ("5", "2.37"), ("8.2", "3.45"), ("1", "0.36"), ("20", "6.75"), ("7.05", "2.38"),
                   ("6", "0.125"), ("40.3", "12.67"), ("3.2", "1.475"), ("100", "45.6")]
    for a, b in fixed_pairs:
        assert tail_ok(a, b, "-"), (a, b)
        seen.add(("-",) + tuple(sorted([a, b])))
    pairs = list(fixed_pairs)
    shapes = [((1, 0), (1, 2)), ((2, 0), (1, 2)), ((1, 1), (1, 2)), ((2, 1), (1, 2)), ((1, 0), (0, 3)),
              ((2, 1), (2, 2)), ((1, 1), (1, 3)), ((2, 0), (2, 1))]
    for sa, sb in shapes:
        a, b = pick(rnd, seen, "-", sa, sb, lambda a, b: dec(a) < dec(b) or "0" in a.split(".")[-1], swap=False)
        pairs.append((a, b))
    for i, (a, b) in enumerate(pairs):
        its.append(item_sub(a, b, i % 2 == 0))
    return {"title": "Subtract with zeros", "items": its}


# ============================================================ set 4: estimate first and check
def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def set_estimate(P):
    its = []
    # best estimate
    for a, b, op in [("6.82", "3.29", "+"), ("12.15", "4.9", "−"), ("8.47", "5.6", "+"), ("19.7", "6.12", "−"),
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
    # is it reasonable?
    R, S, B_, C = "It is reasonable", "It is too small", "It is too big", "You cannot tell without working it out"
    rows = [("4.5", "+", "2.37", "2.82", S, "lined up the last digits"),
            ("18.6", "+", "7.45", "26.05", R, None),
            ("9.2", "−", "4.65", "0.455", S, "put the decimal point in the wrong place"),
            ("3.75", "+", "6.8", "1055", B_, "left out the decimal point"),
            ("24.6", "−", "8.75", "15.85", R, None),
            ("31.08", "−", "6.5", "30.43", B_, "lined up the last digits"),
            ("12.4", "+", "3.65", "16.05", R, None)]
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
    # use an estimate to choose the answer
    for a, op, b in [("7.8", "+", "4.56"), ("15", "−", "6.28"), ("9.45", "+", "12.7"), ("50", "−", "18.35"),
                     ("6.075", "+", "2.9"), ("13.4", "−", "5.825"), ("0.85", "+", "2.6")]:
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
    return {"title": "Estimate first and check", "items": its}


# ============================================================ set 5: money and measurement
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
    its.append(story_add("At the school canteen, %s buys a sausage roll for $3.80 and a juice for $2.45. How much does %s spend?" % (n, he),
                         ["3.8", "2.45"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $13.65 lunch with a $20 note. How much change does %s get?" % (n, he),
                         "20", "13.65", "", "Change is what is left: subtract.", is_money=True))
    its.append(story_add("A rain gauge at a Darwin school measured 38.6 mm of rain on Monday and 24.8 mm on Tuesday. "
                         "How much rain fell over the two days?", ["38.6", "24.8"], "mm", "Put the two days together: add."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("At the athletics carnival, %s ran the 100 m in 14.62 seconds and %s ran it in 13.87 seconds. "
                         "How many seconds faster was %s?" % (n1, n2, n2),
                         "14.62", "13.87", "seconds", "The faster runner has the smaller time. Find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("At the swimming carnival, %s swam 50 m freestyle in 41.36 seconds. Last year %s time was 44.08 seconds. "
                         "By how many seconds did %s improve?" % (n, his, he),
                         "44.08", "41.36", "seconds", "The improvement is the difference between the two times: subtract."))
    n, he, his = P.next()
    its.append(story_add("In the long jump, %s jumped 3.4 m. %s second jump was 0.25 m longer. How long was the second jump?" % (n, cap(his)),
                         ["3.4", "0.25"], "m", "Longer means more: add."))
    n, he, his = P.next()
    its.append(story_sub("A bottle holds 1.5 L of water. %s drinks 0.35 L at recess. How much water is left?" % n,
                         "1.5", "0.35", "L", "Take away what %s drank: subtract." % he))
    its.append(story_sub("A ribbon is 2 m long. The class cuts off 0.85 m for a banner. How much ribbon is left?",
                         "2", "0.85", "m", "Take the part cut off away: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s's puppy had a mass of 4.6 kg. In a month it gained 0.85 kg. What is its mass now?" % n,
                         ["4.6", "0.85"], "kg", "The puppy got heavier: add."))
    its.append(story_sub("Perth had 152.6 mm of rain in July and 78.4 mm in September. How much more rain fell in July?",
                         "152.6", "78.4", "mm", "How much more means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_add("%s pays by card for a book at $14.99 and a pencil case at $6.49. What is the total?" % n,
                         ["14.99", "6.49"], "", "Total means add.", is_money=True))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_add("In a relay at the swimming carnival, %s swam the first leg in 32.48 seconds and %s swam the second leg in 29.75 seconds. "
                         "What was their total time?" % (n1, n2), ["32.48", "29.75"], "seconds", "Total time means add the two legs."))
    its.append(story_add("On a road trip, a family drove 125.6 km before lunch and 87.45 km after lunch. How far did they drive altogether?",
                         ["125.6", "87.45"], "km", "Altogether means add."))
    n, he, his = P.next()
    its.append(story_sub("A watermelon has a mass of 3.2 kg. %s cuts off a piece with a mass of 1.475 kg. What is the mass of the rest?" % n,
                         "3.2", "1.475", "kg", "Take away the piece: subtract."))
    # two-step stories
    a, b, c = Decimal("25"), Decimal("8.45"), Decimal("6.75")
    assert a - b - c == Decimal("9.80") and b + c == Decimal("15.20")
    n, he, his = P.next()
    its.append(mcq("%s has $25 at the school fete. %s buys a plant for $8.45 and a cake for $6.75. How much money does %s have left?" % (n, cap(he), he),
                   "$9.80", [money(sub_no_annex("25", "15.2")), money(b + c), money(a - b), money(sub_right_align("25", "15.2") or 0)],
                   "Step 1, money spent: $8.45 + $6.75 = $15.20. Step 2, money left: $25.00 − $15.20 = <b>$9.80</b>. "
                   "Check: $9.80 + $15.20 = $25.00."))
    assert Decimal("3.2") - Decimal("1.45") - Decimal("0.9") == Decimal("0.85")
    assert Decimal("1.45") + Decimal("0.09") == Decimal("1.54") and Decimal("3.2") - Decimal("1.54") == Decimal("1.66")
    its.append(mcq("A relay is 3.2 km long. The first runner runs 1.45 km and the second runs 0.9 km. "
                   "How far does the third runner have to run?", "0.85 km", ["2.35 km", "1.75 km", "1.66 km"],
                   "Step 1, first two runners: 1.45 + 0.9 = 2.35 km. Step 2, the rest: 3.20 − 2.35 = <b>0.85 km</b>. "
                   "(1.66 lines up the last digits, 1.45 + 0.9 = 1.54, instead of the decimal points. 2.35 km stops after step 1.)"))
    n, he, his = P.next()
    its.append(story_add("%s records the rain at school for three days: 12.4 mm, 9.8 mm and 4.6 mm. What is the total rainfall?" % n,
                         ["12.4", "9.8", "4.6"], "mm", "Total means add all three days."))
    # missing numbers
    assert Decimal(6) - Decimal("2.45") == Decimal("3.55") and sub_no_annex("6", "2.45") == Decimal("4.45")
    its.append(mcq("What number goes in the box?  <b>☐ + 2.45 = 6</b>", "3.55", ["4.45", "3.65", "8.45"],
                   "Use subtraction: 6 − 2.45 = 6.00 − 2.45 = <b>3.55</b>. Check: 3.55 + 2.45 = 6.00 = 6. "
                   "(4.45 forgets to write the zeros: 6 − 2 = 4, then brings down .45.)"))
    n, he, his = P.next()
    assert Decimal("50") - Decimal("37.85") == Decimal("12.15")
    its.append(mcq("%s has $50. %s wants a pair of sport shoes that cost $37.85. After buying them, how much money will %s have left?"
                   % (n, cap(he), he),
                   "$12.15", [money(v) for v in cands_sub("50", "37.85") if v and 0 < v < 1000 and v == v.quantize(Decimal("0.01"))],
                   "Write $50 as $50.00. $50.00 − $37.85: regroup to get 4 tens, 9 ones, 9 tenths and 10 hundredths. "
                   "10 − 5 = 5, 9 − 8 = 1, 9 − 7 = 2, 4 − 3 = 1. Answer: <b>$12.15</b>. Check: $12.15 + $37.85 = $50.00."))
    n, he, his = P.next()
    its.append(story_sub("A water tank had 85.6 L in it. %s used 27.85 L to water the vegetable garden. How much water is left?" % n,
                         "85.6", "27.85", "L", "Take away the water used: subtract."))
    assert len(its) == 20, len(its)
    return {"title": "Money and measurement problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Decimal("4.5") + Decimal("2.37") == Decimal("6.87") and add_right_align(["4.5", "2.37"]) == Decimal("2.82")
    assert Decimal("4.78") + Decimal("2.56") == Decimal("7.34") and add_forgot_point_carry(["4.78", "2.56"]) == Decimal("6.34")
    assert Decimal(10) - Decimal("3.46") == Decimal("6.54") and sub_no_annex("10", "3.46") == Decimal("7.46")
    assert Decimal("8.2") - Decimal("3.45") == Decimal("4.75") and sub_small_from_big("8.2", "3.45") == Decimal("5.25")
    return (
        "<h2>The idea: line up the decimal points</h2>"
        "<p>Add and subtract decimals the same way as whole numbers, but first <b>line up the decimal points</b>. "
        "Then ones are under ones, tenths under tenths and hundredths under hundredths. "
        "You can only add or subtract digits in the same place.</p>"
        "<h2>Different numbers of decimal places</h2>"
        "<p>Write zeros so both numbers have the same number of places. A zero at the end does not change the value: 4.5 = 4.50.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.5", "2.37"], "+", answer="6.87", ghost=True, fs=34) +
        "<figcaption>4.5 + 2.37 = 4.50 + 2.37. Hundredths 0 + 7 = 7, tenths 5 + 3 = 8, ones 4 + 2 = 6. Answer: 6.87.</figcaption></figure>"
        "<p>When a column makes 10 or more, regroup just as with whole numbers. 10 hundredths make 1 tenth, "
        "and 10 tenths make 1 one, so the 1 can cross the decimal point.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.78", "2.56"], "+", answer="7.34", marks=True, fs=34) +
        "<figcaption>4.78 + 2.56: hundredths 8 + 6 = 14, write 4 and regroup 1 tenth. "
        "Tenths 7 + 5 + 1 = 13, write 3 and regroup 1 one. Ones 4 + 2 + 1 = 7. Answer: 7.34.</figcaption></figure>"
        "<h2>Subtract with zeros</h2>"
        "<p>To take a decimal from a whole number, give the whole number a decimal point and zeros: 10 = 10.00. "
        "Then every digit underneath has a digit above it, and you can regroup.</p>"
        "<figure class='sn-fig'>" + column_svg(["10", "3.46"], "-", answer="6.54", ghost=True, marks=True, fs=34) +
        "<figcaption>10 − 3.46 = 10.00 − 3.46. Regroup the 1 ten: 0 tens, 9 ones, 9 tenths and 10 hundredths. "
        "10 − 6 = 4, 9 − 4 = 5, 9 − 3 = 6. Answer: 6.54.</figcaption></figure>"
        + ex("Example", "What is 8.2 − 3.45?",
             "Write 8.2 as 8.20. Hundredths: 0 − 5 needs a regroup, so 10 − 5 = 5. Tenths: 1 − 4 needs a regroup, so 11 − 4 = 7. "
             "Ones: 7 − 3 = 4. Check: 4.75 + 3.45 = 8.20.", "4.75") +
        "<h2>Estimate first, then check</h2>"
        "<p>Round each number to the nearest whole number and do the easy calculation. "
        "4.5 + 2.37 is about 5 + 2 = 7, so 6.87 makes sense and 2.82 does not. "
        "Do this even when you use a calculator: one wrong key or a missed decimal point gives an answer far from the estimate. "
        "You can also check a subtraction by adding back: 6.54 + 3.46 = 10.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (4.5 + 2.37 = 2.82)", "Line up the decimal points. Write 4.5 as 4.50"],
            ["Dropping the decimal point (4.5 + 2.37 = 687)", "Bring the point straight down into the answer"],
            ["Not writing the zeros (10 − 3.46 = 7.46)", "Write 10 as 10.00, then regroup to subtract"],
            ["Forgetting to regroup across the point (4.78 + 2.56 = 6.34)", "10 tenths make 1 one. Add the 1 to the ones"],
            ["Taking the smaller digit from the bigger one (8.2 − 3.45 = 5.25)", "Always take the bottom digit from the top digit. Regroup when the top is smaller"],
        ])
    )


FAQ = [
    {"q": "How do you add decimals with different numbers of decimal places?",
     "a": "Line up the decimal points and write zeros in the empty places, then add from the right like whole numbers: 4.5 + 2.37 = 4.50 + 2.37 = 6.87."},
    {"q": "Why is 4.5 + 2.37 not 2.82?",
     "a": "2.82 comes from lining up the last digits, which adds 5 tenths to 7 hundredths. An estimate of 5 + 2 = 7 shows the answer must be about 7, and the correct sum is 6.87."},
    {"q": "How do you subtract a decimal from a whole number, like 10 − 3.46?",
     "a": "Write the whole number with a decimal point and zeros: 10 = 10.00. Then regroup and subtract: 10.00 − 3.46 = 6.54. Check by adding: 6.54 + 3.46 = 10."},
    {"q": "What does AC9M6N04 cover in Year 6 maths?",
     "a": "In the Australian Curriculum v9.0, Year 6 students add and subtract decimals using place value, using digital tools where appropriate, and use estimation and rounding to check that answers are reasonable."},
]


def gen():
    rnd = random.Random(6805)
    P = People(rnd)
    seen = set()
    sets = [set_line_up(P, rnd, seen), set_places(P, rnd, seen), set_zeros(P, rnd, seen), set_estimate(P), set_words(P)]
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "adding-and-subtracting-decimals", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Adding and Subtracting Decimals",
        "seo_title": "Year 6 Adding and Subtracting Decimals Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Adding and Subtracting Decimals",
        "domain": "Number",
        "standard_code": "AC9M6N04",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Apply knowledge of place value to add and subtract decimals, using digital tools where appropriate; use estimation and rounding to check the reasonableness of answers",
        "meta_desc": "Free Year 6 maths worksheets on adding and subtracting decimals, aligned to the Australian Curriculum (AC9M6N04): line up the decimal points, add numbers with different decimal places, subtract from whole numbers with zeros, estimate to check, and solve money, race time and rainfall problems. 100 questions with an answer key.",
        "key_big": "Line up the decimal points, then add or subtract like whole numbers.",
        "key_sub": "Write zeros in empty places (4.5 = 4.50, 10 = 10.00) so every digit has a partner. Bring the point straight down, then estimate to check: 4.5 + 2.37 is about 7, so the answer is 6.87, not 2.82.",
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
