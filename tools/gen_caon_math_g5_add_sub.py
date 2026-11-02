# -*- coding: utf-8 -*-
"""
CA-ON Grade 5 Math: Adding and Subtracting Whole Numbers and Decimals
(Ontario Curriculum 2020, Number B2.4, with B2.3 estimating decimal sums and differences)
  python3 tools/gen_caon_math_g5_add_sub.py
Whole numbers to 100 000 (column method, regrouping, subtracting across zeros) and decimals to hundredths
(line up the points, write zeros, estimate to check). Money and race-time word problems.
Whole-number helpers (w_*) are copied from gen_cabc_math_g4_add_sub.py; decimal helpers from
gen_caon_math_g6_add_sub_decimals.py (all arithmetic in decimal.Decimal, never float).
Ontario style: 4-digit numbers have no separator (4536); 5+ digits use a no-break space (45 300).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


# ============================================================ common helpers
def cap(s):
    return s[0].upper() + s[1:]


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique sensible distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead in ("0", "0.00", ""):
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


# ============================================================ WHOLE NUMBERS (to 100 000)
W_PLACE = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands"]
W_ONE = ["one", "ten", "hundred", "thousand", "ten thousand", "hundred thousand"]


def f(n):
    """4 digits no separator, 5+ digits a no-break space between groups of three."""
    s = str(n)
    if len(s) <= 4:
        return s
    return "{:,}".format(n).replace(",", NB)


def num(s):
    return int(s.replace(NB, "").replace("$", ""))


def nlen(n):
    return len(str(n))


def w_digits(n, k=None):
    k = k or nlen(n)
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals):
    return [v for v in vals if v is not None and v > 0]


def regroup_digits(a, b):
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
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
    k = max(nlen(a), nlen(b))
    da, db = w_digits(a, k), w_digits(b, k)
    c, cols = 0, []
    for i in range(k):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def w_regroups_sub(a, b):
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
    n = 0
    for i in range(k):
        if d[i] < db[i]:
            n += 1
            d[i] += 10
            d[i + 1] -= 1
    return n


def zero_chain(a, b):
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
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


def w_column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns. The space in a 5- or 6-digit number gets its own narrow slot.
    marks: red regrouping marks (+: regrouped 1s under the answer line; −: crossed digits, new digits above)."""
    cw, kw = fs * (0.82 if marks else 0.62), fs * 0.3
    res = a + b if op == "+" else a - b
    rows = [f(a), f(b)] + ([f(res)] if answer else [])

    def xs(s):
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
            od = w_digits(a)
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = place_x[i]
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%s %s %s written in columns" % (f(a), "plus" if op == "+" else "minus", f(b))
    return svg_wrap(W, int(H), "".join(s), label)


def w_add_steps(a, b):
    k = max(nlen(a), nlen(b))
    da, db = w_digits(a, k), w_digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, ps = 0, []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(W_PLACE[i])
        if t >= 10 and i == k - 1:
            ps.append("%s: %s = %d, write %d." % (P, expr, t, t))
            carry = 0
        elif t >= 10:
            ps.append("%s: %s = %d. Write %d and regroup 1 %s." % (P, expr, t, t % 10, W_ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    s = a + b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%s</b>. Check: %s − %s = %s." % (f(s), f(s), f(b), f(a)))


def w_sub_steps(a, b):
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
    kb = nlen(b)
    ps = []
    for i in range(k):
        P = cap(W_PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                zl = ["%s" % W_PLACE[m] for m in range(i + 1, j)]
                zeros = zl[0] if len(zl) == 1 else ", ".join(zl[:-1]) + " and " + zl[-1]
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d. The %s place%s 0, so regroup 1 %s. Each 0 you pass becomes 9. %d − %d = %d."
                       % (P, cur, db[i], zeros, "s are" if len(zl) > 1 else " is", W_ONE[j], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d. Regroup 1 %s as 10 %s: %d − %d = %d."
                       % (P, cur, db[i], W_ONE[i + 1], W_PLACE[i], d[i], db[i], d[i] - db[i]))
            ps.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                ps.append("%s: write %d." % (P, d[i]))
        else:
            ps.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    return ("Line up the ones and start on the right. " + " ".join(ps) +
            " Answer: <b>%s</b>. Check: %s + %s = %s." % (f(r), f(r), f(b), f(a)))


# ---- typical whole-number mistakes
def w_add_no_regroup(a, b):
    k = max(nlen(a), nlen(b))
    da, db = w_digits(a, k), w_digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def w_add_forgot_one(a, b, which):
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def w_add_misalign(a, b):
    """Lined up the shorter number one place too far left."""
    if nlen(a) == nlen(b):
        return None
    return max(a, b) + min(a, b) * 10


def w_add_extra_one(a, b):
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def w_sub_small_from_big(a, b):
    k = nlen(a)
    da, db = w_digits(a, k), w_digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def w_sub_forgot_reduce(a, b):
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
    out = 0
    for i in range(k):
        if d[i] < db[i]:
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out


def w_sub_zero_as_ten(a, b):
    """Regrouping across zeros: changed the zeros to 10 instead of 9."""
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
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


def w_sub_zero_skip(a, b):
    """Took 1 straight from the next non-zero digit, left the zeros as 0 and took smaller from bigger there."""
    k = nlen(a)
    d, db = w_digits(a, k), w_digits(b, k)
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


def w_sub_misalign(a, b):
    if nlen(a) == nlen(b) or a - b * 10 <= 0:
        return None
    return a - b * 10


def w_add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([w_add_no_regroup(a, b), w_add_forgot_one(a, b, "first"), w_add_forgot_one(a, b, "last"),
                  w_add_misalign(a, b)] + every + w_add_extra_one(a, b) + [abs(a - b)])


def w_sub_cands(a, b):
    return clean([w_sub_zero_skip(a, b), w_sub_zero_as_ten(a, b), w_sub_small_from_big(a, b), w_sub_forgot_reduce(a, b),
                  w_sub_misalign(a, b), a - b + 1000, a - b - 1000, a - b + 10, a + b])


def w_item_add(a, b, col):
    q = (fig(w_column_svg(a, b, "+")) + "Add. Regroup when a column makes 10 or more.") if col else \
        "Use column addition. What is %s + %s?" % (f(a), f(b))
    return mcq(q, f(a + b), [f(v) for v in w_add_cands(a, b)], w_add_steps(a, b))


def w_item_sub(a, b, col):
    q = (fig(w_column_svg(a, b, "-")) + "Subtract. Regroup when the top digit is smaller.") if col else \
        "Use column subtraction. What is %s − %s?" % (f(a), f(b))
    return mcq(q, f(a - b), [f(v) for v in w_sub_cands(a, b)], w_sub_steps(a, b))


W_LESSON_A = {(45678, 28547)}
W_LESSON_S = {(60000, 23458)}


def w_pick_add(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 5, 10 ** la - 10 ** (la - 1) // 2)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 5, 10 ** lb - 10 ** (lb - 1) // 2)
        if rnd.random() < 0.3:
            a, b = b, a
        if a + b > 99999 or (a, b) in seen or (b, a) in seen or (a, b) in W_LESSON_A or a % 10 == 0 or b % 10 == 0:
            continue
        if len(add_carry_cols(a, b)) != want:
            continue
        seen.add((a, b))
        return a, b


def w_pick_sub(rnd, seen, la, lb, want):
    while True:
        a = rnd.randint(10 ** (la - 1) + 10 ** (la - 1) // 2, 10 ** la - 1)
        b = rnd.randint(10 ** (lb - 1) + 10 ** (lb - 1) // 10, min(10 ** lb - 1, a - 10 ** (la - 1) // 4))
        if (a, b) in seen or (a, b) in W_LESSON_S or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if w_regroups_sub(a, b) == want:
            seen.add((a, b))
            return a, b


# ============================================================ DECIMALS (to hundredths)
PLACE = ["thousandths", "hundredths", "tenths", "ones", "tens", "hundreds", "thousands"]
ONE = ["thousandth", "hundredth", "tenth", "one", "ten", "hundred", "thousand"]


def dec(s):
    return len(s.split(".")[1]) if "." in s else 0


def nice(d):
    d = Decimal(d)
    assert abs(d) < 10000, d
    t = format(d.normalize(), "f")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t


def fixed(d, p):
    d = Decimal(d)
    assert abs(d) < 10000, d
    return format(d.quantize(Decimal(1).scaleb(-p)), "f")


def money(d):
    return "$" + fixed(d, 2)


def scale(nums):
    P = max(dec(n) for n in nums)
    return P, [int(Decimal(n).scaleb(P)) for n in nums]


def back(i, P):
    return Decimal(i).scaleb(-P)


def digits(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def pname(i, P):
    return PLACE[i + 3 - P]


def oname(i, P):
    return ONE[i + 3 - P]


def annex_note(nums, P):
    w = ["%s as %s" % (n, fixed(Decimal(n), P)) for n in nums if dec(n) < P]
    if not w:
        return ""
    return "Write " + " and ".join(w) + "."


def add_steps(nums):
    P, ints = scale(nums)
    k = max(max(nlen(x) for x in ints), P + 1)
    ds = [digits(x, k) for x in ints]
    carry, parts = 0, []
    for i in range(k):
        col = [d[i] for d, x in zip(ds, ints) if i < nlen(x) or i < P + 1]
        t = sum(col) + carry
        expr = " + ".join(str(c) for c in col) + (" + %d" % carry if carry else "")
        P_ = cap(pname(i, P))
        if t >= 10 and i == k - 1:
            parts.append("%s: %s = %d, write %d." % (P_, expr, t, t)); carry = 0
        elif t >= 10:
            parts.append("%s: %s = %d, write %d and regroup %d %s." % (P_, expr, t, t % 10, t // 10,
                                                                     oname(i + 1, P) + ("s" if t >= 20 else "")))
            carry = t // 10
        else:
            parts.append("%s: %s = %d." % (P_, expr, t) if len(col) > 1 or carry else "%s: bring down %d." % (P_, t))
            carry = 0
    total = back(sum(ints), P)
    head = "Line up the decimal points. " + annex_note(nums, P)
    if len(nums) == 2:
        end = " Answer: <b>%s</b>. Check: %s − %s = %s." % (nice(total), nice(total), nums[1], nums[0])
    else:
        end = " Answer: <b>%s</b>." % nice(total)
    return (head + " " + " ".join(parts) + end).replace("  ", " ")


def sub_steps(a, b):
    P, (A, B) = scale([a, b])
    k = nlen(A)
    d, db = digits(A, k), digits(B, k)
    kb = nlen(B)
    parts = []
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
                parts.append("%s: %d − %d needs a regroup, but the next place is 0. Regroup 1 %s: the %s become %d, "
                             "each 0 becomes 9, and the %s become %d. %d − %d = %d."
                             % (P_, cur, db[i], oname(j, P), pname(j, P), old - 1, pname(i, P), d[i], d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                parts.append("%s: %d − %d needs a regroup. 1 %s becomes 10 %s: %d − %d = %d."
                             % (P_, cur, db[i], oname(i + 1, P), pname(i, P), d[i], db[i], d[i] - db[i]))
        elif i >= kb and i >= P:
            if d[i] or i < k - 1:
                parts.append("%s: bring down %d." % (P_, d[i]))
        else:
            parts.append("%s: %d − %d = %d." % (P_, d[i], db[i], d[i] - db[i]))
    r = back(A - B, P)
    head = "Line up the decimal points. " + annex_note([a, b], P)
    end = " Answer: <b>%s</b>. Check: %s + %s = %s." % (nice(r), nice(r), b, a)
    return (head + " " + " ".join(parts) + end).replace("  ", " ")


# ---- typical decimal mistakes
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
    """Lined up the last digits instead of the decimal points: 6.4 + 3.25 = 3.89."""
    if len({dec(n) for n in nums}) == 1:
        return None
    P = max(dec(n) for n in nums)
    return back(sum(int(n.replace(".", "")) for n in nums), P)


def add_forgot_point_carry(nums):
    """Did not regroup 10 tenths as 1 one."""
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


def add_extra_one(nums):
    P, ints = scale(nums)
    k, sums, carries = col_info(ints)
    return [back(sum(ints) + 10 ** (i + 1), P) for i in range(k - 1) if not carries[i]]


def point_shift(val, P):
    return [Decimal(val) * 10, Decimal(val) / 10] if P else []


def no_point(val):
    t = nice(val)
    return Decimal(t.replace(".", "")) if "." in t else None


def add_cands(nums):
    P, ints = scale(nums)
    total = back(sum(ints), P)
    c = [add_right_align(nums), add_forgot_point_carry(nums), add_no_carry(nums),
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
    """Did not write the zeros: brought the extra digits of b down. 8 − 2.35 = 6.35."""
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


def sub_forgot_one(a, b):
    """Regrouped from the ones but did not take 1 from the ones: one too high."""
    P, (A, B) = scale([a, b])
    if P == 0:
        return None
    k = nlen(A)
    d = digits(A, k)
    nd = borrow_digits(A, B)
    if nd[P] == d[P]:
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
    return ([sub_no_annex(a, b), sub_small_from_big(a, b), sub_forgot_one(a, b),
             sub_right_align(a, b), Decimal(a) + Decimal(b), r + 1, r - Decimal("0.1")]
            + point_shift(r, P))


def fmt_all(vals):
    """Text for each wrong answer. Grade 5 works to hundredths, so anything with thousandths is left out."""
    out = []
    for v in vals:
        if v is None:
            continue
        if isinstance(v, str):
            t = v
        elif 0 < v < 10000:
            t = nice(v)
        else:
            continue
        if dec(t) <= 2:
            out.append(t)
    return out


def column_svg(nums, op, answer=None, ghost=False, marks=False, fs=28):
    """Numbers in columns, decimal points in one narrow slot so every place lines up.
    ghost: write the missing zeros (and point) in grey.  answer: write the answer row.  marks: red regroup marks."""
    rows = list(nums) + ([answer] if answer else [])
    for r in rows:
        assert Decimal(r) < 1000, r
    P = max(dec(r) for r in rows)
    I = max(len(r.split(".")[0]) for r in rows)
    cw = fs * (0.82 if marks else 0.64)
    kw = cw * 0.53
    pad_l = cw * 1.3 + 10
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
        place_x = [xs[i - P] for i in range(I + P)]
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
        if key in seen or a == b or not tail_ok(a, b, op):
            continue
        if op == "-" and (Decimal(a) - Decimal(b) < Decimal("0.5") or regroups_sub(a, b) == 0):
            continue
        if not cond(a, b):
            continue
        seen.add(key)
        return a, b
    raise RuntimeError((op, sa, sb))


def rnd1(x):
    return int(Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP"))


def rnd_to(n, p):
    return (n + p // 2) // p * p


# ============================================================ set 1: column addition to 100 000
def set_w_add(rnd, P, seen):
    its = []
    a, b = 45386, 2479
    its.append(mcq("You add %s + %s in columns. Which digit of %s goes under the 5 in %s?" % (f(a), f(b), f(b), f(a)),
                   "2", ["4", "7", "9"],
                   "The 5 in %s is in the thousands place. Line up the ones on the right, so thousands sit under thousands: "
                   "the thousands digit of 2479 is <b>2</b>. (If you line up the numbers on the left, the 4 would go there, "
                   "which is wrong.)" % f(a)))
    n, he, his = P.next()
    a, b = 36254, 4718
    w = w_add_misalign(a, b)
    assert w == 83434 and a + b == 40972
    its.append(mcq("%s added %s + %s. %s lined up the numbers on the left, not on the right, and got %s. "
                   "What is the correct sum?" % (n, f(a), f(b), cap(he), f(w)),
                   f(a + b), [f(v) for v in [w] + w_add_cands(a, b)],
                   "Line up the <b>ones</b> on the right: 4718 has no ten thousands digit. " + w_add_steps(a, b)
                   .replace("Line up the ones and start on the right. ", "")))
    seen.add((a, b)); seen.add((45386, 2479))
    plan = ([(5, 4, 1)] * 2 + [(5, 3, 1)] + [(5, 4, 2)] * 3 + [(5, 5, 2)] * 2 + [(5, 4, 3)] * 2 + [(5, 5, 3)] * 3 +
            [(5, 4, 4)] * 2 + [(5, 5, 4)] * 2)
    for i, (la, lb, want) in enumerate(plan):
        a, b = w_pick_add(rnd, seen, la, lb, want)
        its.append(w_item_add(a, b, i % 3 != 2))
    assert 64375 + 35625 == 100000
    its.append(w_item_add(64375, 35625, True))       # regroup in every column: exactly 100 000
    assert len(its) == 20, len(its)
    return {"title": "Column addition to 100 000", "items": its}


# ============================================================ set 2: column subtraction across zeros
def set_w_sub(rnd, P, seen):
    its = []
    its.append(mcq("To subtract 40 000 − 12 345, you must regroup across the zeros. What does 40 000 become?",
                   "3 ten thousands, 9 thousands, 9 hundreds, 9 tens, 10 ones",
                   ["3 ten thousands, 10 thousands, 10 hundreds, 10 tens, 10 ones",
                    "4 ten thousands, 9 thousands, 9 hundreds, 9 tens, 10 ones",
                    "3 ten thousands, 0 thousands, 0 hundreds, 0 tens, 10 ones"],
                   "The ones need a regroup, but the tens, hundreds and thousands are 0. Go left to the 4 ten thousands and take 1: "
                   "4 becomes 3. Each 0 you pass gives 1 away to the right, so it becomes <b>9</b>, and the ones get 10. "
                   "Then 40 000 − 12 345 = 27 655."))
    assert 40000 - 12345 == 27655
    seen.add((40000, 12345))
    plan = [(5, 4, 1), (5, 5, 1), (5, 4, 2), (5, 5, 2), (5, 5, 3), (5, 5, 4)]
    for i, (la, lb, want) in enumerate(plan):
        a, b = w_pick_sub(rnd, seen, la, lb, want)
        its.append(w_item_sub(a, b, i % 3 != 2))
    tops = {60000, 40000}
    pats = [("x0000", 4), ("xx000", 5), ("x00xx", 5), ("x000x", 4), ("x0000", 5), ("xx00x", 5),
            ("x0x00", 5), ("xx000", 4), ("x000x", 5), ("x0000", 5), ("100000", 5), ("100000", 4)]
    for k, (p, lb) in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lo = 10 ** (lb - 1) + 10 ** (lb - 1) // 10
            hi = min(10 ** lb - 1, a - 10 ** (len(p) - 1) // 5)
            if hi <= lo:
                continue
            b = rnd.randint(lo, hi)
            if (a in tops and a != 100000) or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b) or w_regroups_sub(a, b) < 2:
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(w_item_sub(a, b, k % 3 != 2))
            break
    n, he, his = P.next()
    a, b = 70204, 36587
    c = a - b
    assert c == 33617
    its.append(mcq("%s worked out %s − %s = %s. Which calculation checks %s answer?" % (n, f(a), f(b), f(c), his),
                   "%s + %s" % (f(c), f(b)),
                   ["%s + %s" % (f(a), f(b)), "%s + %s" % (f(a), f(c)), "%s − %s" % (f(b), f(c))],
                   "Addition undoes subtraction. Add the answer to the number taken away: %s + %s = %s. "
                   "You get back the starting number, so the answer is right." % (f(c), f(b), f(a))))
    assert len(its) == 20, len(its)
    return {"title": "Column subtraction, including across zeros", "items": its}


# ============================================================ set 3: add decimals
def best_estimate(a, b, op):
    A, B = Decimal(a), Decimal(b)
    ra, rb = rnd1(a), rnd1(b)
    fn = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
    est, exact = fn(ra, rb), fn(A, B)
    fa, fb = int(A), int(B)
    trunc = fn(fa, fb)
    other = ra - rb if op == "+" else ra + rb
    assert est != trunc and est != other and rnd1(exact) == est, (a, b)
    return mcq("Round each number to the nearest whole number. Which is the best estimate for %s %s %s?" % (a, op, b),
               "about %d" % est, ["about %d" % v for v in [trunc, other, fn(fa + 1, fb + 1), fn(fa + 1, fb), fn(fa, fb + 1)]],
               "%s rounds to %d and %s rounds to %d. %d %s %d = <b>%d</b>. The exact answer, %s, is close to %d."
               % (a, ra, b, rb, ra, op, rb, est, nice(exact), est))


def choose_by_estimate(a, op, b):
    if op == "+":
        exact = Decimal(a) + Decimal(b)
        cc = cands_add([a, b])
        steps = add_steps([a, b])
    else:
        exact = Decimal(a) - Decimal(b)
        cc = cands_sub(a, b)
        steps = sub_steps(a, b)
    fn = (lambda x, y: x + y) if op == "+" else (lambda x, y: x - y)
    est = fn(rnd1(a), rnd1(b))
    far = [v for v in cc if v is not None and not isinstance(v, str) and v > 0 and abs(v - exact) >= Decimal("1.5")]
    return mcq("Estimate first, then choose the correct answer without working it out exactly: %s %s %s" % (a, op, b),
               nice(exact), fmt_all(far),
               "%s %s %s is about %d %s %d = %d. Only <b>%s</b> is close to %d. Check by working it out: %s"
               % (a, op, b, rnd1(a), op, rnd1(b), est, nice(exact), est, steps.replace("Line up the decimal points. ", "")))


def set_d_add(rnd, P, seen):
    its = []
    its.append(mcq("To add 6.4 + 3.25, you write 6.4 with two decimal places. Which number is equal to 6.4?",
                   "6.40", ["6.04", "0.64", "64.0"],
                   "A zero at the end of a decimal does not change its value: 6.4 = 6 ones and 4 tenths = <b>6.40</b>. "
                   "6.04 is wrong: it moves the 4 to the hundredths place."))
    n, he, his = P.next()
    a, b = "6.4", "3.25"
    w = add_right_align([a, b])
    assert w == Decimal("3.89") and Decimal(a) + Decimal(b) == Decimal("9.65")
    its.append(mcq(fig(wrong_column_svg([a, b], "+", nice(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum?" % (n, nice(w)),
                   "9.65", ["3.89", "965", "6.65"],
                   "Line up the <b>decimal points</b>, not the last digits: 6.40 + 3.25. Hundredths: 0 + 5 = 5. "
                   "Tenths: 4 + 2 = 6. Ones: 6 + 3 = 9. Answer: <b>9.65</b>. "
                   "Estimate: 6 + 3 = 9, so 3.89 is far too small."))
    its.append(mcq("To find 15 + 2.38, you can write 15 with a decimal point. Which number is equal to 15?",
                   "15.00", ["1.50", "0.15", "150"],
                   "A whole number has its decimal point after the ones digit, so 15 = <b>15.00</b>. "
                   "Then the 5 ones sit over the 2 ones: 15.00 + 2.38 = 17.38."))
    its.append(mcq("In 23.6 + 4.85, the decimal points are lined up. Which digit of 4.85 is under the 3?",
                   "4", ["8", "5", "no digit"],
                   "The 3 in 23.6 is in the ones place. With the points lined up, ones sit under ones: "
                   "the ones digit of 4.85 is <b>4</b>. The 8 goes under the 6 (tenths), and the 5 has no digit above it."))
    for k in [("+", "3.25", "6.4"), ("+", "15", "2.38"), ("+", "23.6", "4.85"), ("+", "2.37", "4.5"), ("+", "2.56", "4.78")]:
        seen.add(k)
    plan = [((1, 1), (1, 1), "nopt"), ((1, 2), (1, 2), "nopt"), ((1, 1), (1, 1), "pt"), ((1, 2), (1, 2), "pt"),
            ((1, 1), (1, 2), "any"), ((2, 2), (1, 1), "any"), ((1, 0), (1, 2), "any"), ((2, 1), (1, 2), "pt"),
            ((2, 2), (2, 2), "pt"), ((0, 2), (0, 1), "pt"), ((2, 0), (2, 2), "any"), ((3, 1), (2, 2), "pt")]
    for i, (sa, sb, kind) in enumerate(plan):
        if kind == "nopt":
            cond = lambda a, b: not carry_point(a, b)
        elif kind == "pt":
            cond = lambda a, b: carry_point(a, b)
        else:
            cond = lambda a, b: True
        if sa[1] != sb[1]:
            c0 = cond
            cond = lambda a, b, c0=c0: c0(a, b) and dec(a) != dec(b)
        a, b = pick(rnd, seen, "+", sa, sb, cond)
        its.append(item_add([a, b], i % 2 == 0))
    its.append(best_estimate("5.78", "2.36", "+"))
    its.append(best_estimate("13.42", "4.75", "+"))
    its.append(best_estimate("26.8", "9.45", "+"))
    its.append(choose_by_estimate("6.8", "+", "4.75"))
    assert len(its) == 20, len(its)
    return {"title": "Add decimals: line up the decimal points", "items": its}


# ============================================================ set 4: subtract decimals and estimate to check
def set_d_sub(rnd, P, seen):
    its = []
    its.append(mcq("To find 8 − 2.35, how should you write 8 so both numbers have hundredths?", "8.00",
                   ["0.08", "0.80", "8.35"],
                   "8 is 8 ones, and its decimal point is after the 8. Write <b>8.00</b>: two zeros hold the tenths "
                   "and hundredths places. Then 8.00 − 2.35 = 5.65."))
    assert Decimal(8) - Decimal("2.35") == Decimal("5.65")
    n, he, his = P.next()
    its.append(mcq("%s found 9.2 − 3.75 = 5.45. Which addition checks %s answer?" % (n, his),
                   "5.45 + 3.75 = 9.2", ["5.45 + 9.2 = 14.65", "9.2 + 3.75 = 12.95", "3.75 + 9.2 = 12.95"],
                   "Addition undoes subtraction. Add the answer to the number taken away: 5.45 + 3.75 = 9.20 = 9.2. "
                   "You get back the starting number, so %s answer is right." % his))
    assert Decimal("9.2") - Decimal("3.75") == Decimal("5.45") and Decimal("5.45") + Decimal("9.2") == Decimal("14.65")
    for k in [("8", "2.35"), ("3.75", "9.2"), ("12.4", "5.75"), ("15.2", "6.47"), ("18.6", "4.35"), ("3.8", "7.25"),
              ("0.46", "10"), ("3.46", "10")]:
        seen.add(("-",) + tuple(sorted(k)))
    plan = [((1, 1), (1, 1)), ((1, 2), (1, 2)), ((2, 2), (1, 2)), ((1, 1), (1, 2)), ((2, 1), (1, 2)),
            ((2, 2), (1, 1)), ((2, 2), (2, 2)), ((2, 1), (2, 2))]
    for i, (sa, sb) in enumerate(plan):
        a, b = pick(rnd, seen, "-", sa, sb, swap=False)
        its.append(item_sub(a, b, i % 2 == 0))
    for i, (a, b) in enumerate([("5", "1.75"), ("20", "7.36"), ("1", "0.45"), ("30", "12.8"), ("100", "36.45")]):
        assert tail_ok(a, b, "-")
        key = ("-",) + tuple(sorted([a, b]))
        assert key not in seen, key
        seen.add(key)
        its.append(item_sub(a, b, i % 2 == 1))
    # is it reasonable?
    R, S, B_, C = "It is reasonable", "It is too small", "It is too big", "You cannot tell without working it out"
    assert sub_small_from_big("15.2", "6.47") == Decimal("11.27") and no_point(Decimal("3.45")) == Decimal(345)
    rows = [("12.4", "5.75", "6.65", R, None, False),
            ("15.2", "6.47", "11.27", B_, "took the smaller digit from the bigger one in each place", False),
            ("18.6", "4.35", "22.95", B_, "pressed + instead of −", True),
            ("7.25", "3.8", "345", B_, "left out the decimal point", False)]
    for a, b, shown, ans, why, calc in rows:
        n, he, his = P.next()
        exact = Decimal(a) - Decimal(b)
        est = rnd1(a) - rnd1(b)
        assert (Decimal(shown) == exact) == (ans == R)
        assert ans != S or Decimal(shown) < est - 1
        assert ans != B_ or Decimal(shown) > est + 1
        tool = " on a calculator" if calc else ""
        q = "%s worked out %s − %s%s and got %s. Use an estimate to check. What does the estimate show?" % (n, a, b, tool, shown)
        e = "%s rounds to %d and %s rounds to %d, so the answer should be about %d − %d = %d. " % (a, rnd1(a), b, rnd1(b), rnd1(a), rnd1(b), est)
        if ans == R:
            e += "%s is close to %d, so <b>it is reasonable</b>." % (shown, est)
        else:
            e += ("%s is much bigger than %d, so <b>it is too big</b>. %s probably %s. The correct answer is %s."
                  % (shown, est, n, why, nice(exact)))
        its.append(mcq(q, ans, [x for x in [R, S, B_, C] if x != ans], e))
    its.append(choose_by_estimate("14.3", "−", "5.68"))
    assert len(its) == 20, len(its)
    return {"title": "Subtract decimals and estimate to check", "items": its}


# ============================================================ set 5: word problems
def cash(d):
    """Canada has no pennies: a cash total is rounded to the nearest 5 cents."""
    cents = int(Decimal(d) * 100)
    assert Decimal(cents) / 100 == Decimal(d)
    return Decimal((cents + 2) // 5 * 5) / 100


def is5(d):
    return int(Decimal(d) * 100) % 5 == 0


def story_add(q, nums, unit, lead, is_money=False):
    tot = sum(Decimal(n) for n in nums)
    if is_money:
        c = [money(v) for v in cands_add(nums) if v is not None and not isinstance(v, str) and v > 0
             and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(tot), c, lead + " " + add_steps(nums))
    return mcq(q, "%s %s" % (nice(tot), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_add(nums))], lead + " " + add_steps(nums))


def story_sub(q, a, b, unit, lead, is_money=False):
    r = Decimal(a) - Decimal(b)
    if is_money:
        c = [money(v) for v in cands_sub(a, b) if v is not None and v > 0 and v == v.quantize(Decimal("0.01"))]
        return mcq(q, money(r), c, lead + " " + sub_steps(a, b))
    return mcq(q, "%s %s" % (nice(r), unit), ["%s %s" % (c, unit) for c in fmt_all(cands_sub(a, b))], lead + " " + sub_steps(a, b))


def w_story_add(q, a, b, unit, lead):
    return mcq(q, "%s %s" % (f(a + b), unit), ["%s %s" % (f(v), unit) for v in w_add_cands(a, b)], lead + " " + w_add_steps(a, b))


def w_story_sub(q, a, b, unit, lead):
    return mcq(q, "%s %s" % (f(a - b), unit), ["%s %s" % (f(v), unit) for v in w_sub_cands(a, b)], lead + " " + w_sub_steps(a, b))


def set_words(P):
    its = []
    # ---- money
    n, he, his = P.next()
    its.append(story_add("At the sports store, %s buys a hockey stick for $34.99 and a roll of tape for $4.75. "
                         "How much does %s spend?" % (n, he), ["34.99", "4.75"], "", "Put the two prices together: add.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("%s pays for a $27.86 order at the bookstore with a $50 bill. How much change does %s get?" % (n, he),
                         "50", "27.86", "", "Change is what is left: subtract.", is_money=True))
    n, he, his = P.next()
    its.append(story_sub("Winter boots cost $64.50 at one store and $48.95 at another. How much more do they cost at the first store?",
                         "64.5", "48.95", "", "How much more means find the difference: subtract.", is_money=True))
    n, he, his = P.next()
    t = Decimal("4.37") + Decimal("2.85")
    assert t == Decimal("7.22") and cash(t) == Decimal("7.20")
    assert add_forgot_point_carry(["4.37", "2.85"]) == Decimal("6.22")
    its.append(mcq("There are no pennies in Canada, so a cash total is rounded to the nearest 5¢. %s buys a sandwich for $4.37 "
                   "and a juice for $2.85. %s pays with cash. How much does %s pay?" % (n, cap(he), he),
                   "$7.20", ["$7.22", "$7.25", "$6.20"],
                   "Step 1, add: $4.37 + $2.85. Hundredths: 7 + 5 = 12, write 2 and regroup 1 tenth. Tenths: 3 + 8 + 1 = 12, "
                   "write 2 and regroup 1 one. Ones: 4 + 2 + 1 = 7. Total: $7.22. Step 2, cash: $7.22 is 2¢ from $7.20 "
                   "and 3¢ from $7.25, so %s pays <b>$7.20</b>. ($7.22 is what a card would pay.)" % he))
    n, he, his = P.next()
    A, B, C = Decimal(40), Decimal("12.45"), Decimal("9.8")
    assert B + C == Decimal("22.25") and A - B - C == Decimal("17.75") and sub_no_annex("40", "22.25") == Decimal("18.25")
    its.append(mcq("%s has $40. %s buys mitts for $12.45 and a toque for $9.80. How much money does %s have left?" % (n, cap(he), he),
                   "$17.75", ["$18.25", "$22.25", "$27.55"],
                   "Step 1, money spent: $12.45 + $9.80 = $22.25. Step 2, money left: $40.00 − $22.25 = <b>$17.75</b>. "
                   "Check: $17.75 + $22.25 = $40.00. ($18.25 forgets to write $40 as $40.00 before subtracting.)"))
    assert A - B == Decimal("27.55")
    n, he, his = P.next()
    vals = ["7.85", "6.4", "4.95"]
    est = sum(rnd1(v) for v in vals)
    trunc = sum(int(Decimal(v)) for v in vals)
    exact = sum(Decimal(v) for v in vals)
    assert est == 19 and trunc == 17 and exact == Decimal("19.20")
    its.append(mcq("%s has $20. %s wants a book for $7.85, a puzzle for $6.40 and a card for $4.95. "
                   "Round each price to the nearest dollar. About how much is the total, and does %s have enough?" % (n, cap(he), he),
                   "About $19, so yes", ["About $17, so yes", "About $21, so no", "About $22, so no"],
                   "$7.85 rounds to $8, $6.40 rounds to $6 and $4.95 rounds to $5. $8 + $6 + $5 = <b>$19</b>, which is less than $20, "
                   "so %s has enough. (The exact total is $19.20.) $17 comes from dropping the cents instead of rounding." % he))
    # ---- race times
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("At the track and field meet, %s ran the 100 m in 15.42 seconds and %s ran it in 14.87 seconds. "
                         "How many seconds faster was %s?" % (n1, n2, n2), "15.42", "14.87", "seconds",
                         "The faster runner has the smaller time. Find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_sub("At a swim meet, %s swam 50 m backstroke in 48.65 seconds. Last year %s time was 52.3 seconds. "
                         "By how many seconds did %s improve?" % (n, his, he), "52.3", "48.65", "seconds",
                         "The improvement is the difference between the two times: subtract."))
    its.append(story_add("A 4 × 100 m relay team ran its four parts in 16.25 s, 15.8 s, 17.04 s and 15.36 s. "
                         "What was the team’s total time?", ["16.25", "15.8", "17.04", "15.36"], "s",
                         "Total means add all four parts."))
    n, he, his = P.next()
    its.append(story_add("In a ski race, %s finished the first run in 48.76 seconds and the second run in 51.39 seconds. "
                         "What was %s total time?" % (n, his), ["48.76", "51.39"], "seconds", "Total means add the two runs."))
    n1, _, _ = P.next()
    n2, _, _ = P.next()
    its.append(story_sub("At the skating rink, %s skated one lap in 43.9 seconds. %s took 45.08 seconds. "
                         "How much longer did %s take?" % (n1, n2, n2), "45.08", "43.9", "seconds",
                         "How much longer means find the difference: subtract."))
    n, he, his = P.next()
    its.append(story_add("In the long jump, %s jumped 2.85 m. %s second jump was 0.4 m longer. How long was the second jump?" % (n, cap(his)),
                         ["2.85", "0.4"], "m", "Longer means more: add."))
    its.append(story_add("A family biked 12.75 km on a trail in the morning and 8.6 km in the afternoon. How far did they bike altogether?",
                         ["12.75", "8.6"], "km", "Altogether means add."))
    # ---- large whole numbers
    its.append(w_story_add("A hockey arena had 17 485 fans on Friday and 18 362 fans on Saturday. "
                           "How many fans came on the two nights?", 17485, 18362, "fans", "Put the two nights together: add."))
    its.append(w_story_sub("A food bank hopes to collect 50 000 cans of food this winter. So far it has 32 768 cans. "
                           "How many more cans does it need?", 50000, 32768, "cans", "Find what is still needed: subtract."))
    its.append(w_story_sub("One town has 63 205 people. Another town has 47 890 people. How many more people live in the first town?",
                           63205, 47890, "people", "How many more means find the difference: subtract."))
    its.append(w_story_add("A truck driver drove 38 476 km last year and 46 958 km this year. "
                           "How far did the driver go in the two years?", 38476, 46958, "km", "Put the two years together: add."))
    A, B, C = 45000, 28754, 9386
    t = B + C
    assert t == 38140 and A - t == 6860
    its.append(mcq("A stadium has 45 000 seats. For a soccer game, 28 754 adult tickets and 9386 student tickets were sold. "
                   "How many seats are still empty?", "6860 seats",
                   ["%s seats" % f(v) for v in clean([A - B, t, w_sub_zero_as_ten(A, t), w_sub_small_from_big(A, t)])],
                   "Step 1, tickets sold: 28 754 + 9386 = 38 140. Step 2, empty seats: 45 000 − 38 140 = <b>6860</b>. "
                   "Check: 6860 + 38 140 = 45 000."))
    a, b = 38760, 24395
    assert (rnd_to(a, 1000), rnd_to(b, 1000), a + b) == (39000, 24000, 63155)
    its.append(mcq("A school collected 38 760 bottle caps last year and 24 395 this year. Round each number to the nearest thousand. "
                   "About how many bottle caps is that altogether?", "about 63" + NB + "000",
                   ["about 62" + NB + "000", "about 64" + NB + "000", "about 15" + NB + "000"],
                   "38 760 rounds up to 39 000. 24 395 rounds down to 24 000. 39 000 + 24 000 = <b>63 000</b>. "
                   "(The exact total is 63 155, which is close.) 62 000 comes from cutting 38 760 down to 38 000 instead of rounding."))
    assert 38000 + 24000 == 62000
    # ---- missing number
    assert Decimal(10) - Decimal("3.65") == Decimal("6.35") and sub_no_annex("10", "3.65") == Decimal("7.65")
    n, he, his = P.next()
    its.append(mcq("%s needs a 10 m rope for a canoe trip. %s has a 3.65 m piece. What number goes in the box to show how many "
                   "more metres %s needs?  <b>3.65 + ☐ = 10</b>" % (n, cap(he), he), "6.35", ["7.65", "6.45", "13.65"],
                   "Use subtraction: 10 − 3.65 = 10.00 − 3.65 = <b>6.35</b>. Check: 3.65 + 6.35 = 10.00 = 10. "
                   "(7.65 forgets to write the zeros: 10 − 3 = 7, then brings down .65. 13.65 adds instead of subtracting.)"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: money, race times and big numbers", "items": its}


# ============================================================ lesson
def body_html():
    assert 45678 + 28547 == 74225 and w_add_no_regroup(45678, 28547) == 63115
    assert 60000 - 23458 == 36542 and w_sub_zero_as_ten(60000, 23458) == 37652
    assert Decimal("4.5") + Decimal("2.37") == Decimal("6.87") and add_right_align(["4.5", "2.37"]) == Decimal("2.82")
    assert Decimal(10) - Decimal("3.46") == Decimal("6.54") and sub_no_annex("10", "3.46") == Decimal("7.46")
    assert Decimal("4.78") + Decimal("2.56") == Decimal("7.34") and add_forgot_point_carry(["4.78", "2.56"]) == Decimal("6.34")
    return (
        "<h2>The idea: add and subtract the same places</h2>"
        "<p>Every digit has a place: ten thousands, thousands, hundreds, tens, ones, tenths and hundredths. "
        "You can only add or subtract digits in the <b>same place</b>. When a place gets 10 or more, "
        "<b>regroup</b>: 10 ones make 1 ten, 10 tenths make 1 one, and so on.</p>"
        "<h2>Big numbers: line up the ones</h2>"
        "<p>Put ones under ones, tens under tens, and so on. Start on the right. "
        "If a column makes 10 or more, write the ones digit and regroup 1 into the next column.</p>"
        "<figure class='sn-fig'>" + w_column_svg(45678, 28547, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 8 + 7 = 15, write 5, regroup 1. Tens: 7 + 4 + 1 = 12, write 2, regroup 1. "
        "Hundreds: 6 + 5 + 1 = 12, write 2, regroup 1. Thousands: 5 + 8 + 1 = 14, write 4, regroup 1. "
        "Ten thousands: 4 + 2 + 1 = 7. Answer: 74 225.</figcaption></figure>"
        "<h2>Subtracting across zeros</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, regroup from the next place. "
        "If that place is 0, go left to the first digit that is not 0. Every 0 you pass becomes <b>9</b>.</p>"
        "<figure class='sn-fig'>" + w_column_svg(60000, 23458, "-", answer=True, marks=True, fs=34) +
        "<figcaption>60 000 becomes 5 ten thousands, 9 thousands, 9 hundreds, 9 tens and 10 ones. "
        "10 − 8 = 2, 9 − 5 = 4, 9 − 4 = 5, 9 − 3 = 6, 5 − 2 = 3. Answer: 36 542.</figcaption></figure>"
        "<h2>Decimals: line up the decimal points</h2>"
        "<p>With decimals, line up the <b>decimal points</b>, not the last digits. Then tenths are under tenths and hundredths "
        "under hundredths. Write zeros so both numbers have the same number of places. A zero at the end does not change "
        "the value: 4.5 = 4.50.</p>"
        "<figure class='sn-fig'>" + column_svg(["4.5", "2.37"], "+", answer="6.87", ghost=True, fs=34) +
        "<figcaption>4.5 + 2.37 = 4.50 + 2.37. Hundredths 0 + 7 = 7, tenths 5 + 3 = 8, ones 4 + 2 = 6. Answer: 6.87.</figcaption></figure>"
        "<p>Regrouping works the same way. 10 hundredths make 1 tenth, and 10 tenths make 1 one, "
        "so a regrouped 1 can cross the decimal point.</p>"
        + ex("Example", "What is 4.78 + 2.56?",
             "Hundredths: 8 + 6 = 14, write 4 and regroup 1 tenth. Tenths: 7 + 5 + 1 = 13, write 3 and regroup 1 one. "
             "Ones: 4 + 2 + 1 = 7.", "7.34") +
        "<p>To take a decimal from a whole number, write the whole number with a point and zeros: 10 = 10.00.</p>"
        "<figure class='sn-fig'>" + column_svg(["10", "3.46"], "-", answer="6.54", ghost=True, marks=True, fs=34) +
        "<figcaption>10 − 3.46 = 10.00 − 3.46. Regroup: 0 tens, 9 ones, 9 tenths and 10 hundredths. "
        "10 − 6 = 4, 9 − 4 = 5, 9 − 3 = 6. Answer: 6.54.</figcaption></figure>"
        "<h2>Estimate first, then check</h2>"
        "<p>Round each decimal to the nearest whole number and work it out in your head. "
        "4.5 + 2.37 is about 5 + 2 = 7, so 6.87 makes sense and 2.82 does not. "
        "For big numbers, round to the nearest thousand: 45 678 + 28 547 is about 46 000 + 29 000 = 75 000. "
        "When you finish, check with the inverse: 6.54 + 3.46 = 10.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Lining up the last digits (4.5 + 2.37 = 2.82)", "Line up the decimal points. Write 4.5 as 4.50"],
            ["Not regrouping (45 678 + 28 547 = 63 115)", "Write the regrouped 1 in the next column and add it in"],
            ["Making each 0 into 10 instead of 9 (60 000 − 23 458 = 37 652)", "Each 0 you pass gives 1 away, so it becomes 9"],
            ["Not writing the zeros (10 − 3.46 = 7.46)", "Write 10 as 10.00, then regroup to subtract"],
            ["Forgetting the 1 that crosses the point (4.78 + 2.56 = 6.34)", "10 tenths make 1 one. Add the 1 to the ones"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about adding and subtracting in Ontario?",
     "a": "In the Ontario math curriculum, Grade 5 students add and subtract whole numbers up to 100 000 and decimals to hundredths "
          "(expectation B2.4). They also estimate decimal sums and differences (B2.3) to check their answers."},
    {"q": "How do you add decimals with different numbers of decimal places?",
     "a": "Line up the decimal points and write zeros in the empty places, then add from the right like whole numbers: "
          "4.5 + 2.37 = 4.50 + 2.37 = 6.87."},
    {"q": "How do you subtract across zeros, like 60 000 − 23 458?",
     "a": "Go left to the first digit that is not 0 and regroup from there; each 0 you pass becomes 9. "
          "60 000 becomes 5 ten thousands, 9 thousands, 9 hundreds, 9 tens and 10 ones, so 60 000 − 23 458 = 36 542."},
    {"q": "How can my child check an addition or subtraction answer?",
     "a": "Estimate first by rounding (4.5 + 2.37 is about 7), then compare. After subtracting, add the answer to the number "
          "taken away: if 10 − 3.46 = 6.54, then 6.54 + 3.46 should give 10."},
]


def verify(sets):
    """Recompute every plain calculation answer and every column picture from the question."""
    N = r"(\d+(?:" + NB + r"\d{3})*)"
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"What is ([\d.]+) ([+−]) ([\d.]+)\?$", it["q"])
            if m:
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"aria-label='([\d.]+) (plus|minus) ([\d.]+) written in columns with", it["q"])
            if m and ("Add." in it["q"] or "Subtract." in it["q"]):
                a, op, b = Decimal(m.group(1)), m.group(2), Decimal(m.group(3))
                assert Decimal(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"aria-label='" + N + " (plus|minus) " + N + " written in columns'", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"Use column (?:addition|subtraction)\. What is " + N + " ([+−]) " + N + r"\?$", it["q"])
            if m:
                a, op, b = num(m.group(1)), m.group(2), num(m.group(3))
                assert num(right) == (a + b if op == "+" else a - b), it["q"]
            if "$" in right and "with cash" in it["q"]:
                assert is5(right.lstrip("$")), it["q"]
            for x in it["c"]:
                t = re.sub(r"^\$|\s.*$", "", x.replace(NB, ""))
                if re.fullmatch(r"\d+(\.\d+)?", t):
                    assert dec(t) <= 2, x


def gen():
    rnd = random.Random(45803)
    P = People(rnd)
    seen_wa, seen_ws, seen_d = set(), set(), set()
    sets = [set_w_add(rnd, P, seen_wa), set_w_sub(rnd, P, seen_ws), set_d_add(rnd, P, seen_d),
            set_d_sub(rnd, P, seen_d), set_words(P)]
    balance(sets, rnd)
    verify(sets)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            ms = [re.fullmatch(r"(?:about )?\$?(\d+(?:" + NB + r"\d{3})*(?:\.\d+)?)(?: [a-zA-Z]+)?", x) for x in it["c"]]
            if all(ms):
                assert len({Decimal(m.group(1).replace(NB, "")) for m in ms}) == 4, it
            assert it["q"] not in keys, it["q"]
            keys.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-5",
        "slug": "adding-and-subtracting-whole-numbers-and-decimals", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Adding and Subtracting Whole Numbers and Decimals",
        "seo_title": "Grade 5 Adding and Subtracting Whole Numbers and Decimals Worksheets: Free Math with Answer Key (Ontario)",
        "short_title": "Adding and Subtracting Whole Numbers and Decimals",
        "domain": "Number",
        "standard_code": "Grade 5: B2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Represent and solve problems involving the addition and subtraction of whole numbers that add up to "
                         "no more than 100 000, and of decimal numbers up to hundredths, using appropriate tools, strategies, and algorithms",
        "meta_desc": "Free Grade 5 math worksheets on adding and subtracting whole numbers to 100 000 and decimals to hundredths, "
                     "matched to the Ontario curriculum: column addition with regrouping, subtracting across zeros, lining up "
                     "decimal points, estimating to check, and money and race-time word problems. 100 questions with an answer key.",
        "key_big": "Line up the places, then add or subtract from the right.",
        "key_sub": "Big numbers: ones under ones, and every 0 you regroup across becomes 9 (60 000 − 23 458 = 36 542). "
                   "Decimals: line up the decimal points and write zeros (4.5 = 4.50, 10 = 10.00). "
                   "Estimate to check: 4.5 + 2.37 is about 7, so the answer is 6.87, not 2.82.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return nb_fix(u)


def nb_fix(o):
    """Hand-typed numbers like 45 000 get a no-break space (only in text, never inside tags)."""
    if isinstance(o, dict):
        return {k: nb_fix(v) for k, v in o.items()}
    if isinstance(o, list):
        return [nb_fix(v) for v in o]
    if isinstance(o, str):
        parts = re.split(r"(<[^>]*>)", o)
        return "".join(t if t.startswith("<") else re.sub(r"(?<=\d) (?=\d{3}(?!\d))", NB, t) for t in parts)
    return o


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
