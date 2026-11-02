# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Decimal Operations (6.NS.B.3)
  python3 tools/gen_us_math_g6_decimal_operations.py
Fluent standard algorithms with multi-digit decimals (to thousandths): add and subtract with the points
lined up, multiply and count the decimal places, long division with annexed zeros, and dividing by a
decimal divisor. All arithmetic uses decimal.Decimal (never float), so every answer and every typical
mistake is exact. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written as placeholders
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
MINUS = "−"


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text without extra zeros, commas from 1,000: Dm('2800.0') -> '2,800'."""
    return format(Dm(x).normalize(), ",f")


def M(x):
    """Money: $3.75, $1,250.00."""
    return "$" + format(Dm(x).quantize(Dm("0.01")), ",f")


def places(x):
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


def digits_of(x):
    """'2.35' -> 235 (the number without its point)."""
    return int(str(x).replace(".", "").replace(",", ""))


def fixed(x, p):
    return format(Dm(x).quantize(Dm(1).scaleb(-p)), ",f")


def pl(k, one, many=None):
    return "%s %s" % (N(k), one if Dm(k) == 1 else (many or one + "s"))


def scale(nums):
    P = max(places(n) for n in nums)
    return P, [int(Dm(n).scaleb(P)) for n in nums]


def dig(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]          # smallest place first


VAL = re.compile(r"^(?:about )?\$?([\d,]*\.?\d+)(.*)$")


def val(c):
    m = VAL.match(c)
    return (Dm(m.group(1).replace(",", "")), m.group(2)) if m else None


# ------------------------------------------------------------ typical mistakes
def add_right_align(a, b):
    """Lined up the last digits: 12.405 + 3.6 -> 12405 + 36 -> 12.441."""
    if places(a) == places(b):
        return None
    return Dm(digits_of(a) + digits_of(b)).scaleb(-max(places(a), places(b)))


def add_no_carry(a, b):
    P, (A, B) = scale([a, b])
    k = max(len(str(A)), len(str(B)))
    da, db = dig(A, k), dig(B, k)
    if all(da[i] + db[i] < 10 for i in range(k)):
        return None
    return Dm(sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))).scaleb(-P)


def add_forgot_point_carry(a, b):
    """Did not carry the 1 from the tenths into the ones."""
    P, (A, B) = scale([a, b])
    if P == 0:
        return None
    if (A % 10 ** P) + (B % 10 ** P) < 10 ** P:
        return None
    return Dm(A + B - 10 ** P).scaleb(-P)


def sub_no_annex(a, b):
    """Did not write the zeros: brought the extra digits of b down. 45.6 − 7.83 -> 37.83."""
    pa, pb = places(a), places(b)
    if pa >= pb:
        return None
    bt = Dm(b).quantize(Dm(1).scaleb(-pa), rounding="ROUND_DOWN")
    head = Dm(a) - bt
    return head + (Dm(b) - bt) if head > 0 else None


def sub_small_from_big(a, b):
    P, (A, B) = scale([a, b])
    k = len(str(A))
    da, db = dig(A, k), dig(B, k)
    if all(da[i] >= db[i] for i in range(k)):
        return None
    return Dm(sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))).scaleb(-P)


def sub_forgot_reduce(a, b):
    """Regrouped (added 10) but did not take 1 from the next place."""
    P, (A, B) = scale([a, b])
    k = len(str(A))
    da, db = dig(A, k), dig(B, k)
    if all(da[i] >= db[i] for i in range(k)):
        return None
    return Dm(sum(((da[i] - db[i]) % 10) * 10 ** i for i in range(k))).scaleb(-P)


def sub_right_align(a, b):
    if places(a) == places(b):
        return None
    r = digits_of(a) - digits_of(b)
    return Dm(r).scaleb(-max(places(a), places(b))) if r > 0 else None


def add_cands(a, b):
    s = Dm(a) + Dm(b)
    return [add_right_align(a, b), add_forgot_point_carry(a, b), add_no_carry(a, b), s * 10, s / 10]


def sub_cands(a, b):
    r = Dm(a) - Dm(b)
    return [sub_no_annex(a, b), sub_right_align(a, b), sub_small_from_big(a, b), sub_forgot_reduce(a, b),
            Dm(a) + Dm(b), r * 10, r / 10]


def mul_cands(a, b):
    p = Dm(a) * Dm(b)
    k, m = places(a) + places(b), max(places(a), places(b))
    return [p.scaleb(k - m) if k != m else None, p * 10, p / 10, Dm(a) + Dm(b), p * 100, p / 100]


def drop_zero(q):
    """Skipped a 0 in the quotient: 2.06 -> 2.6."""
    s = N(q).replace(",", "")
    i = next(j for j, ch in enumerate(s) if ch not in "0.")
    j = s.find("0", i)
    if j < 0 or j == len(s) - 1:
        return None
    return Dm(s[:j] + s[j + 1:])


def rem_digit(a, d):
    """Stopped at the last digit of the dividend and wrote the remainder as the next digit: 7.5 ÷ 4 -> 1.83."""
    k = places(a)
    q, r = divmod(digits_of(a), d)
    if r == 0 or r > 9:
        return None
    return Dm(q * 10 + r).scaleb(-k - 1)


def stop_early(a, d):
    k = places(a)
    q, r = divmod(digits_of(a), d)
    return Dm(q).scaleb(-k) if r else None


def divw_cands(a, d):
    q = Dm(a) / d
    return [drop_zero(q), rem_digit(a, d), stop_early(a, d), q * 10, q / 10, Dm(a) * d]


def divd_cands(a, b):
    q = Dm(a) / Dm(b)
    k = places(b)
    c = [q / 10 ** k]                                       # moved the point only in the divisor
    if places(a) < k:
        c.append(q / 10 ** (k - places(a)))                 # did not write zeros in the dividend
    c += [q * 10, q / 10, Dm(a) * Dm(b), q * 100]
    return c


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 distractors with a different value. Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    vals = [val(correct)]
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        v = val(c)
        if c in seen or not c or c.startswith("-") or (v and v in vals) or (v and v[0] == 0):
            continue
        seen.add(c)
        vals.append(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def nums(vals):
    return [N(v) for v in vals if v is not None and Dm(v) > 0]


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, font=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, font, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def point_mark(x, y, fs, col=INK):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (x, y - fs * 0.06, fs * 0.1, col)


# ------------------------------------------------------------ figures
def addsub_svg(rows, op, answer=None, ghost=True, fs=28):
    """Numbers in columns with the decimal points in one narrow slot. Missing zeros in gray."""
    allr = list(rows) + ([answer] if answer else [])
    P = max(places(r) for r in allr)
    I = max(len(r.split(".")[0]) for r in allr)
    cw, kw = fs * 0.64, fs * 0.34
    pad_l = cw * 1.3 + 10
    xs, x = {}, pad_l
    for p in range(I - 1, -1, -1):
        xs[p] = x + cw / 2
        x += cw
    xs["pt"] = x + kw / 2
    x += kw
    for p in range(-1, -P - 1, -1):
        xs[p] = x + cw / 2
        x += cw
    W = int(x + 10)
    s = []

    def ch(c, cx, y, color):
        s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                 "font-family='monospace'>%s</text>" % (cx, y, fs, color, c))

    def put(t, y, color):
        ip, _, fp = t.partition(".")
        for n, c in enumerate(reversed(ip)):
            ch(c, xs[n], y, color)
        if "." in t:
            ch(".", xs["pt"], y, color)
        elif ghost:
            ch(".", xs["pt"], y, GHOST)
        for n in range(P):
            if n < len(fp):
                ch(fp[n], xs[-n - 1], y, color)
            elif ghost:
                ch("0", xs[-n - 1], y, GHOST)

    ys = [8 + fs + int(n * fs * 1.15) for n in range(len(rows))]
    for t, y in zip(rows, ys):
        put(t, y, INK)
    sign_x = pad_l - cw * 0.6
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, ys[-1], fs, GREEN, "+" if op == "+" else MINUS))
    ly = ys[-1] + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.5, ly, W - 8, ly, INK))
    H = ly + 10
    if answer:
        put(answer, ly + fs + 6, GREEN)
        H = ly + fs + 14
    label = "%s written in columns with the decimal points lined up" % (" plus " if op == "+" else " minus ").join(rows)
    return svg_wrap(W, H, "".join(s), label)


def wrong_column_svg(rows, op, wrong, fs=28):
    """A student's work with the LAST digits lined up (points not lined up), and the wrong answer."""
    cw, kw = fs * 0.64, fs * 0.34
    allr = list(rows) + [wrong]

    def width(t):
        return sum(kw if c == "." else cw for c in t)
    pad_l = cw * 1.3 + 10
    right = pad_l + max(width(r) for r in allr)
    W = int(right + 10)
    s = []

    def put(t, y, color):
        x = right
        for c in reversed(t):
            w = kw if c == "." else cw
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (x - w / 2, y, fs, color, c))
            x -= w
    ys = [8 + fs + int(n * fs * 1.15) for n in range(len(rows))]
    for t, y in zip(rows, ys):
        put(t, y, INK)
    sign_x = pad_l - cw * 0.6
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, ys[-1], fs, GREEN, "+" if op == "+" else MINUS))
    ly = ys[-1] + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.5, ly, W - 8, ly, INK))
    put(wrong, ly + fs + 6, RED)
    label = "%s written with the last digits lined up and the answer %s" % ((" plus " if op == "+" else " minus ").join(rows), wrong)
    return svg_wrap(W, ly + fs + 14, "".join(s), label)


def mul_svg(rows, rules, label, fs=26, colors=None):
    """Multiplication written in columns, lined up on the RIGHT (points are not lined up)."""
    cw = fs * 0.9
    lens = [len(t.replace(".", "")) for sg, t in rows]
    signed = max([n for (sg, t), n in zip(rows, lens) if sg] or [0])
    sign_slot = max(max(lens), signed + 1)
    slots = sign_slot + 1
    W = int(cw * slots + 20)
    gap = fs * 1.2
    H = int(10 + gap * len(rows) + 4 * len(rules) + 10)
    right = W - 10
    s = []
    y = 10
    for r, (sg, t) in enumerate(rows):
        y += gap
        col = (colors or {}).get(r, INK)
        slot = 0
        for ch in reversed(t):
            if ch == ".":
                s.append(point_mark(right - cw * slot, y, fs, col))
                continue
            s.append(text(right - cw * (slot + 0.5), y - 2, ch, fs, col=col))
            slot += 1
        if sg:
            s.append(text(right - cw * (sign_slot + 0.5), y - 2, sg, fs, col=GREEN))
        if r in rules:
            y += 4
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
                     % (right - cw * slots, y + 5, right, y + 5, INK))
    return svg_wrap(W, H, "".join(s), label, "monospace")


def ld_rows(ds, d):
    cur, steps, started = 0, [], False
    for i, ch in enumerate(ds):
        cur = cur * 10 + int(ch)
        if not started and cur < d and i < len(ds) - 1:
            continue
        started = True
        q = cur // d
        steps.append((i, cur, q))
        cur -= q * d
    return steps, cur


def ld_svg(dividend, d, quot=None, work=False, ghost=0, fs=24):
    """Long division with a decimal dividend and a whole-number divisor.
    quot: None, 'digits' (quotient digits, point left out) or 'full'. ghost: annexed zeros at the end (gray).
    The quotient point sits straight above the dividend point."""
    ds = dividend.replace(".", "")
    k = places(dividend)
    pi = len(ds) - 1 - k
    qv = Dm(dividend) / d
    qi = qv * 10 ** k
    assert qi == int(qi), (dividend, d)
    qs = str(int(qi)).rjust(len(ds), "0")
    qcols = [(j, ch) for j, ch in enumerate(qs) if j >= pi or ch != "0" or any(c != "0" for c in qs[:j])]
    cw = fs * 0.95
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 18
    steps, r = ld_rows(ds, d)
    assert r == 0
    rh = fs * 1.25
    top = (rh + 6) if quot else 10
    s = []

    def col(j):
        return x0 + cw * (j + 0.5)

    def digits_at(txt, last, y, colr=INK):
        for i, ch in enumerate(reversed(txt)):
            c = GHOST if (colr == INK and y == by and last - i >= len(ds) - ghost) else colr
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % (col(last - i), y, fs, c, ch))

    by = top + rh - fs * 0.18
    digits_at(ds, len(ds) - 1, by)
    if k:
        s.append(point_mark(x0 + cw * (pi + 1), by, fs))
    s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%d</text>"
             % (x0 - 14, by, fs, GREEN, d))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * len(ds) + 10
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))
    H = top + bh + 8
    if quot:
        for j, ch in qcols:
            digits_at(ch, j, top - 8, GREEN)
        if quot == "full" and k:
            s.append(point_mark(x0 + cw * (pi + 1), top - 8, fs, GREEN))
    if work:
        y = by
        for n, (i, cur, qd) in enumerate(steps):
            p = qd * d
            y += rh
            digits_at(str(p), i, y)
            left = i - len(str(max(p, cur))) + 1
            s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>−</text>"
                     % (col(left) - cw * 0.85, y, fs, RED))
            ly = y + fs * 0.3
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
                     % (col(left) - cw * 1.2, ly, col(i) + cw * 0.5, ly, INK))
            y += rh
            if n + 1 < len(steps):
                digits_at(str(steps[n + 1][1]), i + 1, y)
            else:
                digits_at(str(cur - p), i, y)
        H = y + 12
    label = "%s divided by %d written as long division" % (dividend, d)
    if quot == "digits":
        label += " with the quotient digits but no decimal point"
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


def shift_svg(a, b, fs=24):
    """a ÷ b as long division. Both decimal points hop the same number of places to the right
    (red arrows below the digits). Zeros written to make room are gray. Under it: the new problem."""
    k = places(b)
    A, B = Dm(a) * 10 ** k, Dm(b) * 10 ** k
    assert B == int(B)
    need = max(places(a), k)
    da = fixed(a, need).replace(",", "")
    ghost_a = need - places(a)
    dda = da.replace(".", "")
    ddb = b.replace(".", "")
    pa = len(da.split(".")[0])                     # digits before the point in the dividend
    pb = len(b.split(".")[0])
    cw = fs * 0.95
    rh = fs * 1.25
    top = 10
    by = top + rh - fs * 0.18
    s = []
    bx = 12
    x0 = bx + cw * len(ddb) + 22                   # left edge of the dividend cells
    for j, ch in enumerate(ddb):
        s.append(text(bx + cw * (j + 0.5), by, ch, fs, col=GREEN))
    for j, ch in enumerate(dda):
        s.append(text(x0 + cw * (j + 0.5), by, ch, fs, col=GHOST if j >= len(dda) - ghost_a else INK))
    bh = rh + 2
    s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='3'/>"
             % (x0 - 6, top, x0 + 3, top + bh / 2, x0 - 6, top + bh, INK))
    W = x0 + cw * len(dda) + 12
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0 - 6, top, W - 4, top, INK))

    def hop(xl, n):
        x1, x2 = xl + cw * 0, xl + cw * n
        yb = by + 6
        s.append(point_mark(x1, by, fs, GHOST))
        s.append(point_mark(x2, by, fs, RED))
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
                 % (x1, yb, (x1 + x2) / 2, yb + 16, x2 - 2, yb + 3, RED))
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>"
                 % (x2 + 1, yb + 1, x2 - 8, yb + 1, x2 - 3, yb + 8, RED))
    hop(bx + cw * pb, k)
    hop(x0 + cw * pa, k)
    ty = by + 26 + fs
    s.append(text(W / 2.0, ty, "%s ÷ %s" % (N(A), N(B)), fs, col=GREEN))
    H = ty + 10
    label = "%s divided by %s: both decimal points move %s to the right, giving %s divided by %s" % (
        a, b, pl(k, "place"), N(A), N(B))
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), label, "monospace")


# ------------------------------------------------------------ explanations
def addsub_e(a, op, b):
    P = max(places(a), places(b))
    fa, fb = fixed(a, P), fixed(b, P)
    r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
    e = "Line up the decimal points. "
    w = ["%s as %s" % (x, fx) for x, fx in ((a, fa), (b, fb)) if fx != x]
    if w:
        e += "Write " + " and ".join(w) + " so every place has a digit. "
    e += "%s %s %s = <b>%s</b>." % (fa, op, fb, N(r))
    if fixed(r, P) != N(r):
        e = e[:-len("<b>%s</b>." % N(r))] + "%s = <b>%s</b>." % (fixed(r, P), N(r))
    if op == MINUS:
        e += " Check: %s + %s = %s." % (N(r), b, a)
    return e


def mul_e(a, b):
    ra, rb = digits_of(a), digits_of(b)
    raw = ra * rb
    k = places(a) + places(b)
    ans = Dm(a) * Dm(b)
    written = str(raw).rjust(k + 1, "0")
    written = written[:-k] + "." + written[-k:]
    e = "Multiply as whole numbers: %s × %s = %s. " % (N(ra), N(rb), N(raw))
    e += "Count the decimal places: %d + %d = %d. " % (places(a), places(b), k)
    e += "Count %d places from the right" % k
    if len(str(raw)) <= k:
        e += " (write zeros in front to make room)"
    e += ": %s" % written
    if N(ans) != written:
        e += " = <b>%s</b>." % N(ans)
    else:
        e = e[:-len(written)] + "<b>%s</b>." % written
    return e


def divw_e(a, d):
    q = Dm(a) / d
    need = max(places(a), places(N(q)))
    e = "Divide as with whole numbers. Put the point in the quotient straight above the point in the dividend. "
    if need > places(a):
        e += "When digits run out, write zeros (%s = %s) and keep dividing until nothing is left. " % (a, fixed(a, need))
    if drop_zero(q) is not None:
        e += "When %d does not fit, write 0 in the quotient. " % d
    e += "%s ÷ %d = <b>%s</b>. Check: %s × %d = %s." % (a, d, N(q), N(q), d, a)
    return e


def divd_e(a, b, tail=""):
    k = places(b)
    m = 10 ** k
    A, B = Dm(a) * m, Dm(b) * m
    q = Dm(a) / Dm(b)
    e = ("%s has %s, so multiply <b>both</b> numbers by %s (move both points %s right)%s. "
         "%s ÷ %s = %s ÷ %s = <b>%s</b>. Check: %s × %s = %s."
         % (b, pl(k, "decimal place"), N(m), pl(k, "place"),
            " and write a zero in %s" % a if places(a) < k and k - places(a) == 1 else
            " and write zeros in %s" % a if places(a) < k else "",
            a, b, N(A), N(B), N(q), N(q), b, a))
    return e + tail


# ============================================================ set 1: add and subtract
def set_add_sub(P):
    its = []
    for a, op, b in [("12.405", "+", "3.6"), ("45.6", MINUS, "7.83"), ("8.07", "+", "15.968"), ("30", MINUS, "4.256")]:
        r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
        c = add_cands(a, b) if op == "+" else sub_cands(a, b)
        word = "Add." if op == "+" else "Subtract."
        its.append(mcq(fig(addsub_svg([a, b], op)) + word + " The gray zeros hold the empty places.", N(r), nums(c),
                       addsub_e(a, op, b)))
    n, he, his = P.next()
    w = add_right_align("6.25", "13.8")
    assert w == Dm("7.63") and Dm("6.25") + Dm("13.8") == Dm("20.05")
    its.append(mcq(fig(wrong_column_svg(["6.25", "13.8"], "+", N(w))) +
                   "%s lined up the last digits and got %s. What is the correct sum of 6.25 + 13.8?" % (n, N(w)),
                   "20.05", nums([w] + add_cands("6.25", "13.8")),
                   "%s lined up the last digits, so the 8 tenths were added to the 5 hundredths. Line up the decimal points instead "
                   "and write 13.8 as 13.80: 6.25 + 13.80 = <b>20.05</b>. Estimate: 6 + 14 = 20." % n))
    for a, op, b in [("27.36", "+", "8.9"), ("5.704", "+", "12.85"), ("63.2", MINUS, "18.47"), ("9", MINUS, "3.62"),
                     ("104.5", "+", "26.875"), ("50.03", MINUS, "7.6"), ("0.875", "+", "2.4"), ("18.06", MINUS, "9.358"),
                     ("120.4", MINUS, "35.75"), ("7.008", "+", "3.99"), ("246.1", "+", "58.29"), ("15", MINUS, "0.025")]:
        r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
        c = add_cands(a, b) if op == "+" else sub_cands(a, b)
        its.append(mcq("%s %s %s = ?" % (a, op, b), N(r), nums(c), addsub_e(a, op, b)))
    its.append(mcq("To find 6.3 %s 2.875, how should you write 6.3?" % MINUS, "6.300", ["6.003", "6.030", "63.000"],
                   "2.875 has 3 decimal places, so give 6.3 three places too. Zeros at the <b>end</b> do not change the value: "
                   "6.3 = <b>6.300</b>. (6.003 puts the zeros in front of the 3, which changes 3 tenths into 3 thousandths.)"))
    its.append(mcq("Which is the best estimate for 48.92 + 31.075?", "about 80", ["about 8", "about 800", "about 52"],
                   "Round to whole numbers: 48.92 ≈ 49 and 31.075 ≈ 31. 49 + 31 = <b>80</b>. "
                   "(About 52 comes from lining up the last digits.) The exact sum is 79.995."))
    assert Dm("10.1") - Dm("2.75") == Dm("7.35")
    its.append(mcq("What number goes in the box?  <b>☐ + 2.75 = 10.1</b>", "7.35",
                   nums([Dm("12.85"), sub_no_annex("10.1", "2.75"), sub_small_from_big("10.1", "2.75")]),
                   "Find the missing addend by subtracting: 10.1 %s 2.75. Write 10.1 as 10.10: 10.10 %s 2.75 = <b>7.35</b>. "
                   "Check: 7.35 + 2.75 = 10.10 = 10.1. (12.85 adds instead of subtracting.)" % (MINUS, MINUS)))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract multi-digit decimals", "items": its}


# ============================================================ set 2: multiply
def set_multiply(P):
    its = []
    for a, b in [("2.35", "1.4"), ("3.08", "2.5"), ("12.6", "0.45")]:
        p = Dm(a) * Dm(b)
        q = fig(mul_svg([("", a), ("×", b)], [1], "%s times %s written in columns, lined up on the right" % (a, b))) + "Multiply."
        its.append(mcq(q, N(p), nums(mul_cands(a, b)), mul_e(a, b)))
    for a, b in [("21.75", "0.36"), ("0.438", "2.5")]:
        ra, rb = digits_of(a), digits_of(b)
        p = Dm(a) * Dm(b)
        its.append(mcq("%s × %s = %s. What is %s × %s?" % (N(ra), N(rb), N(ra * rb), a, b), N(p),
                       nums([Dm(ra * rb)] + mul_cands(a, b)), mul_e(a, b)))
    for a, b in [("0.06", "0.3"), ("4.7", "0.08"), ("1.25", "3.6"), ("0.45", "0.2"), ("15.6", "2.5"), ("7.05", "0.04"),
                 ("3.14", "2.5"), ("24.8", "1.5"), ("0.9", "0.007"), ("102.5", "0.6"), ("6.25", "0.16")]:
        p = Dm(a) * Dm(b)
        its.append(mcq("%s × %s = ?" % (a, b), N(p), nums(mul_cands(a, b)), mul_e(a, b)))
    its.append(mcq("Without multiplying, how many decimal places does 3.125 × 0.04 have before you drop any zeros?", "5",
                   ["3", "2", "6"],
                   "3.125 has 3 decimal places and 0.04 has 2. The product has <b>3 + 2 = 5</b> places: "
                   "3,125 × 4 = 12,500, so 3.125 × 0.04 = 0.12500 = 0.125."))
    its.append(mcq("Which product is less than 5.2?", "5.2 × 0.98", ["5.2 × 1.02", "5.2 × 1", "5.2 × 2.5"],
                   "Compare the other factor with 1. Only 0.98 is less than 1, so only <b>5.2 × 0.98</b> is less than 5.2 "
                   "(it is 5.096). 5.2 × 1 is exactly 5.2."))
    assert Dm("19.8") * Dm("3.05") == Dm("60.39")
    its.append(mcq("Which is the product of 19.8 × 3.05? Use an estimate.", "60.39", ["6.039", "603.9", "22.85"],
                   "Estimate: 19.8 ≈ 20 and 3.05 ≈ 3, so the product is about 20 × 3 = 60. Only <b>60.39</b> is close to 60. "
                   "(22.85 is the sum.)"))
    assert Dm("8.5") * Dm("0.6") == Dm("5.1")
    its.append(mcq("85 × 6 = 510. What is 8.5 × 0.6?", "5.1", ["51", "0.51", "0.051"],
                   "1 + 1 = 2 decimal places: count 2 places from the right in 510 → 5.10. The zero at the end can be dropped: "
                   "<b>5.1</b>. Count the places <b>before</b> you drop the zero, or you get 0.51."))
    assert len(its) == 20, len(its)
    return {"title": "Multiply decimals", "items": its}


# ============================================================ set 3: divide by a whole number
def set_div_whole(P):
    its = []
    for a, d in [("18.72", 6), ("0.936", 4), ("25.38", 9), ("41.65", 7)]:
        its.append(mcq(fig(ld_svg(a, d)) + "Divide.", N(Dm(a) / d), nums(divw_cands(a, d)), divw_e(a, d)))
    for a, d in [("9.144", 3), ("2.385", 5), ("63.6", 12)]:
        q = Dm(a) / d
        raw = int(q * 10 ** places(a))
        its.append(mcq(fig(ld_svg(a, d, quot="digits")) + "The quotient digits are written, but the point is missing. "
                       "What is %s ÷ %d?" % (a, d), N(q), nums([Dm(raw)] + divw_cands(a, d)), divw_e(a, d)))
    for a, d in [("7.5", 4), ("3.3", 6), ("9", 8), ("13.4", 8), ("2.1", 4)]:
        its.append(mcq("%s ÷ %d = ?" % (a, d), N(Dm(a) / d), nums(divw_cands(a, d)), divw_e(a, d)))
    for a, d in [("45.6", 12), ("86.4", 24), ("17.25", 15), ("0.912", 16), ("8.24", 4), ("30.15", 5)]:
        its.append(mcq("%s ÷ %d = ?" % (a, d), N(Dm(a) / d), nums(divw_cands(a, d)), divw_e(a, d)))
    n, he, his = P.next()
    its.append(mcq("%s is dividing 7.5 ÷ 4. %s has written 1.8 in the quotient, and 3 tenths are left. What should %s do next?"
                   % (n, cap(he), he), "Write a 0 and keep dividing",
                   ["Write the answer as 1.83", "Stop: the answer is 1.8", "Start again with 4 ÷ 7.5"],
                   "7.5 = 7.50 = 7.500, so writing zeros does not change the dividend. <b>Write a 0 and keep dividing</b>: "
                   "30 hundredths ÷ 4 = 7, 2 left; 20 thousandths ÷ 4 = 5. So 7.5 ÷ 4 = 1.875. (1.83 writes the remainder as a digit.)"))
    its.append(mcq("Which multiplication checks that 18.72 ÷ 6 = 3.12?", "3.12 × 6", ["18.72 × 6", "3.12 × 18.72", "6 × 6"],
                   "Quotient × divisor = dividend. <b>3.12 × 6</b> = 18.72, so the division is right."))
    assert len(its) == 20, len(its)
    return {"title": "Divide a decimal by a whole number (long division)", "items": its}


# ============================================================ set 4: divide by a decimal
def set_div_dec(P):
    its = []
    for a, b in [("4.56", "0.12"), ("1.5", "0.25"), ("2.24", "0.7"), ("0.63", "0.009")]:
        q = Dm(a) / Dm(b)
        its.append(mcq(fig(shift_svg(a, b)) + "Both decimal points move the same number of places. What is %s ÷ %s?" % (a, b),
                       N(q), nums(divd_cands(a, b)), divd_e(a, b)))
    for a, b, right, wrong in [("7.35", "0.5", "73.5 ÷ 5", ["7.35 ÷ 5", "735 ÷ 5", "73.5 ÷ 0.5"]),
                               ("0.18", "0.006", "180 ÷ 6", ["18 ÷ 6", "0.18 ÷ 6", "1.8 ÷ 6"]),
                               ("12", "0.75", "1,200 ÷ 75", ["12 ÷ 75", "120 ÷ 75", "1,200 ÷ 0.75"])]:
        k = places(b)
        A, B = Dm(a) * 10 ** k, Dm(b) * 10 ** k
        assert right == "%s ÷ %s" % (N(A), N(B))
        q = Dm(a) / Dm(b)
        e = ("%s has %s, so multiply both numbers by %s: %s → %s and %s → %s. %s ÷ %s = <b>%s</b> = %s. "
             "Move the point the <b>same</b> number of places in both numbers."
             % (b, pl(k, "decimal place"), N(10 ** k), a, N(A), b, N(B), a, b, right, N(q)))
        its.append(mcq("Which problem has the same quotient as %s ÷ %s?" % (a, b), right, wrong, e))
    for a, b in [("9.6", "0.8"), ("0.144", "0.12"), ("3.75", "1.5"), ("27", "0.45"), ("0.51", "0.3"),
                 ("6.5", "0.13"), ("14.4", "2.4"), ("0.0084", "0.07"), ("52.2", "0.9"), ("7.2", "0.016")]:
        its.append(mcq("%s ÷ %s = ?" % (a, b), N(Dm(a) / Dm(b)), nums(divd_cands(a, b)), divd_e(a, b)))
    its.append(mcq("Without dividing, which is true about 8 ÷ 0.4?", "It is greater than 8",
                   ["It is less than 8", "It equals 2", "It equals 3.2"],
                   "0.4 is less than 1, and many 0.4s fit into 8, so the quotient is <b>greater than 8</b>. "
                   "8 ÷ 0.4 = 80 ÷ 4 = 20. (2 is 8 ÷ 4, and 3.2 is 8 × 0.4.)"))
    n, he, his = P.next()
    its.append(mcq("%s wrote 4.85 ÷ 0.5 = 0.97. What mistake did %s make?" % (n, he), "Moved the point only in the divisor",
                   ["Moved the point in both numbers", "Multiplied instead of dividing", "Made no mistake"],
                   "%s changed 0.5 to 5 but left 4.85 as it was: 4.85 ÷ 5 = 0.97. %s <b>moved the point only in the divisor</b>. "
                   "Move both: 4.85 ÷ 0.5 = 48.5 ÷ 5 = 9.7." % (n, cap(he))))
    assert Dm("4.85") / 5 == Dm("0.97") and Dm("4.85") / Dm("0.5") == Dm("9.7")
    its.append(mcq("Why does 4.56 ÷ 0.12 have the same answer as 456 ÷ 12?", "Both numbers were multiplied by 100",
                   ["Only the divisor was multiplied by 100", "Both numbers were divided by 100", "The zeros were dropped"],
                   "4.56 × 100 = 456 and 0.12 × 100 = 12. When <b>both numbers are multiplied by 100</b>, the quotient does not "
                   "change, just as 6 ÷ 2 = 60 ÷ 20 = 3. Both give 38."))
    assert len(its) == 20, len(its)
    return {"title": "Divide by a decimal", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []
    D = Dm
    n, he, his = P.next()
    assert D("3.48") * D("12.5") == D("43.5")
    its.append(mcq("Gas costs $3.48 per gallon. %s buys 12.5 gallons. How much does %s pay?" % (n, he), "$43.50",
                   ["$435.00", "$4.35", "$15.98"],
                   "Multiply: 12.5 × $3.48. 125 × 348 = 43,500, and 1 + 2 = 3 decimal places give 43.500 = <b>$43.50</b>. "
                   "Estimate: 12 × $3.50 = $42. ($15.98 is the sum.)"))
    assert D("4.35") / D("2.5") == D("1.74")
    its.append(mcq("A 2.5-pound bag of apples costs $4.35. What is the price per pound?", "$1.74",
                   ["$17.40", "$1.85", "$6.85"],
                   "Price per pound = cost ÷ pounds = 4.35 ÷ 2.5. Move both points 1 place: 43.5 ÷ 25 = <b>1.74</b>. "
                   "Check: 2.5 × $1.74 = $4.35. ($1.85 subtracts, and $6.85 adds.)"))
    n, he, his = P.next()
    assert D("6.75") / D("0.45") == 15
    its.append(mcq("%s has 6.75 m of ribbon. %s cuts it into pieces 0.45 m long. How many pieces does %s get?" % (n, cap(he), he),
                   "15", ["1.5", "150", "6.3"],
                   "How many 0.45s are in 6.75? Divide: 6.75 ÷ 0.45 = 675 ÷ 45 = <b>15</b>. Check: 15 × 0.45 = 6.75. "
                   "(6.3 subtracts.)"))
    assert (D("86.40") + D("13.60")) / 4 == 25
    its.append(mcq("Four friends eat dinner. The bill is $86.40 and they add a $13.60 tip. They split the total equally. "
                   "How much does each friend pay?", "$25.00", ["$21.60", "$3.40", "$250.00"],
                   "Step 1: total = $86.40 + $13.60 = $100.00. Step 2: $100.00 ÷ 4 = <b>$25.00</b>. "
                   "($21.60 forgets the tip: 86.40 ÷ 4.)"))
    n, he, his = P.next()
    assert D("0.4") * D("7.5") == 3
    its.append(mcq("One lap of a track is 0.4 km. %s runs 7.5 laps. How far does %s run?" % (n, he), "3 km",
                   ["30 km", "0.3 km", "7.9 km"],
                   "Multiply: 7.5 × 0.4. 75 × 4 = 300, and 1 + 1 = 2 decimal places give 3.00 = <b>3 km</b>. (7.9 km is the sum.)"))
    n, he, his = P.next()
    assert D("27.5") / 5 == D("5.5")
    its.append(mcq("%s runs 5 km in 27.5 minutes at a steady pace. How many minutes does each kilometer take?" % n,
                   "5.5 minutes", ["55 minutes", "0.55 minute", "22.5 minutes"],
                   "Divide: 27.5 ÷ 5. 275 ÷ 5 = 55, and the point goes above the point: <b>5.5 minutes</b>. "
                   "Check: 5 × 5.5 = 27.5. (22.5 subtracts.)"))
    assert D("31.5") * D("8.4") == D("264.6")
    its.append(mcq("A car goes 31.5 miles on 1 gallon of gas. How far can it go on 8.4 gallons?", "264.6 miles",
                   ["2,646 miles", "26.46 miles", "39.9 miles"],
                   "Multiply: 31.5 × 8.4. 315 × 84 = 26,460, and 1 + 1 = 2 decimal places give 264.60 = <b>264.6 miles</b>. "
                   "Estimate: 30 × 8 = 240."))
    assert D("283.5") / D("13.5") == 21
    its.append(mcq("A truck drove 283.5 miles and used 13.5 gallons of gas. How many miles did it go per gallon?", "21",
                   ["2.1", "210", "270"],
                   "Miles per gallon = miles ÷ gallons = 283.5 ÷ 13.5. Move both points 1 place: 2,835 ÷ 135 = <b>21</b>. "
                   "Check: 21 × 13.5 = 283.5. (270 subtracts.)"))
    n, he, his = P.next()
    assert 20 - (3 * D("2.85") + D("1.49")) == D("9.96")
    its.append(mcq("%s buys 3 notebooks for $2.85 each and a pen for $1.49. %s pays with a $20 bill. How much change does %s get?"
                   % (n, cap(he), he), "$9.96", ["$10.04", "$11.45", "$15.66"],
                   "Step 1: 3 × $2.85 = $8.55. Step 2: $8.55 + $1.49 = $10.04. Step 3: $20.00 %s $10.04 = <b>$9.96</b>. "
                   "($10.04 is the cost, not the change. $11.45 forgets the pen.)" % MINUS))
    n, he, his = P.next()
    assert D("0.75") * D("2.5") == D("1.875")
    its.append(mcq("One batch of granola needs 0.75 cup of honey. %s makes 2.5 batches. How much honey does %s need?" % (n, he),
                   "1.875 cups", ["18.75 cups", "0.1875 cup", "3.25 cups"],
                   "Multiply: 2.5 × 0.75. 25 × 75 = 1,875, and 1 + 2 = 3 decimal places give <b>1.875 cups</b>. "
                   "(3.25 is the sum.)"))
    assert D("3.48") / 12 == D("0.29") and D("4.86") / 18 == D("0.27")
    its.append(mcq("Store A sells 12 oz of cereal for $3.48. Store B sells 18 oz for $4.86. Which is the better buy per ounce?",
                   "Store B, by $0.02", ["Store A, by $0.02", "Store A, by $1.38", "Store B, by $0.20"],
                   "Unit price = cost ÷ ounces. A: $3.48 ÷ 12 = $0.29 per ounce. B: $4.86 ÷ 18 = $0.27 per ounce. "
                   "$0.29 %s $0.27 = $0.02, so <b>Store B is cheaper by $0.02</b> per ounce. ($1.38 compares the box prices.)" % MINUS))
    n, he, his = P.next()
    assert D("6.40") * D("2.75") == D("17.6")
    its.append(mcq("Fabric costs $6.40 per yard. %s needs 2.75 yards for a costume. How much does the fabric cost?" % n,
                   "$17.60", ["$176.00", "$1.76", "$9.15"],
                   "Multiply: 2.75 × $6.40. 275 × 64 = 17,600, and 2 + 1 = 3 decimal places give 17.600 = <b>$17.60</b>. "
                   "Estimate: 3 × $6 = $18. ($9.15 is the sum.)"))
    assert D("47.25") / 3 == D("15.75")
    its.append(mcq("Three friends share a pizza order that costs $47.25. They split it equally. How much does each friend pay?",
                   "$15.75", ["$157.50", "$141.75", "$44.25"],
                   "Divide: $47.25 ÷ 3. 4,725 ÷ 3 = 1,575, and the point goes above the point: <b>$15.75</b>. "
                   "Check: 3 × $15.75 = $47.25. ($141.75 multiplies, and $44.25 subtracts.)"))
    n, he, his = P.next()
    assert D(15) / D("1.25") == 12
    its.append(mcq("Each lap of the pool takes %s 1.25 minutes. %s swims for 15 minutes. How many laps does %s swim?" % (n, cap(he), he),
                   "12 laps", ["18.75 laps", "120 laps", "1.2 laps"],
                   "Divide: 15 ÷ 1.25. Move both points 2 places: 1,500 ÷ 125 = <b>12</b>. Check: 12 × 1.25 = 15. "
                   "(18.75 multiplies.)"))
    assert D("37.8") / D("0.6") == 63
    its.append(mcq("A tank holds 37.8 L of water. How many 0.6 L bottles can be filled from it?", "63",
                   ["6.3", "630", "22.68"],
                   "Divide: 37.8 ÷ 0.6 = 378 ÷ 6 = <b>63</b>. Check: 63 × 0.6 = 37.8. (22.68 multiplies.)"))
    n, he, his = P.next()
    assert 30 - (D("12.6") + D("8.75")) == D("8.65")
    its.append(mcq("%s wants to bike 30 km this week. %s rides 12.6 km on Monday and 8.75 km on Tuesday. How many more kilometers "
                   "does %s need to ride?" % (n, cap(he), he), "8.65 km", ["21.35 km", "19.99 km", "11.35 km"],
                   "Step 1: 12.60 + 8.75 = 21.35 km so far. Step 2: 30.00 %s 21.35 = <b>8.65 km</b>. "
                   "(21.35 km is the distance already ridden. 19.99 km comes from lining up the last digits.)" % MINUS))
    assert D("3.60") / 8 == D("0.45") and D("4.80") / 12 == D("0.4")
    its.append(mcq("A pack of 8 pencils costs $3.60. A pack of 12 pencils costs $4.80. How much less does one pencil cost "
                   "in the 12-pack?", "$0.05", ["$1.20", "$0.85", "$0.40"],
                   "8-pack: $3.60 ÷ 8 = $0.45 per pencil. 12-pack: $4.80 ÷ 12 = $0.40 per pencil. "
                   "$0.45 %s $0.40 = <b>$0.05</b>. ($1.20 compares the pack prices.)" % MINUS))
    n, he, his = P.next()
    assert D(3) / D("0.25") * D("2.4") == D("28.8")
    its.append(mcq("%s runs 0.25 mile in 2.4 minutes. At the same pace, how long does it take %s to run 3 miles?" % (n, "her" if he == "she" else "him"),
                   "28.8 minutes", ["7.2 minutes", "2.88 minutes", "288 minutes"],
                   "Step 1: 3 ÷ 0.25 = 300 ÷ 25 = 12 quarter miles. Step 2: 12 × 2.4 = <b>28.8 minutes</b>. "
                   "(7.2 minutes multiplies 3 × 2.4, as if the 2.4 minutes were for a whole mile.)"))
    assert D("0.04") * 185 == D("7.4") and D("7.4") * D("3.50") == D("25.9")
    its.append(mcq("A car uses 0.04 gallon of gas per mile. Gas costs $3.50 per gallon. How much does the gas cost for a "
                   "185-mile trip?", "$25.90", ["$7.40", "$259.00", "$2.59"],
                   "Step 1: 185 × 0.04 = 7.4 gallons. Step 2: 7.4 × $3.50 = <b>$25.90</b>. ($7.40 stops after step 1: that is "
                   "gallons, not dollars.)"))
    n, he, his = P.next()
    assert D("4.8") - 6 * D("0.75") == D("0.3") and D("4.8") / D("0.75") == D("6.4")
    its.append(mcq("%s has 4.8 m of fabric. Each costume needs 0.75 m. How many costumes can %s make, and how much fabric is left?"
                   % (n, he), "6 costumes, 0.3 m left", ["6 costumes, 0.4 m left", "6.4 costumes, 0 m left", "64 costumes, 0 m left"],
                   "4.8 ÷ 0.75 = 480 ÷ 75 = 6.4, so only <b>6</b> whole costumes fit. They use 6 × 0.75 = 4.5 m, and "
                   "4.8 %s 4.5 = <b>0.3 m</b> is left. (0.4 m reads the .4 of 6.4 as meters, but 0.4 of a costume is 0.4 × 0.75 = 0.3 m.)" % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Multi-step word problems: money, fuel, fabric and running", "items": its}


# ============================================================ lesson
def body_html():
    assert Dm("12.405") + Dm("3.6") == Dm("16.005")
    assert Dm("2.35") * Dm("1.4") == Dm("3.29") and 235 * 4 == 940 and 235 * 10 == 2350
    assert Dm("7.5") / 4 == Dm("1.875")
    assert Dm("4.56") / Dm("0.12") == 38
    f_add = addsub_svg(["12.405", "3.6"], "+", answer="16.005", fs=30)
    f_mul = mul_svg([("", "2.35"), ("×", "1.4"), ("", "940"), ("+", "2350"), ("", "3.290")], [1, 3],
                    "2.35 times 1.4 worked out in columns: 940 plus 2350 is 3290, so the product is 3.290", fs=26,
                    colors={4: GREEN})
    f_div = ld_svg("7.500", 4, quot="full", work=True, ghost=2, fs=24).replace(
        "written as long division", "worked out with long division: 1.875")
    f_shift = shift_svg("4.56", "0.12", fs=26)
    return (
        "<h2>The big idea</h2>"
        "<p>In Grade 6 you use the <b>standard algorithm</b> for all four operations. The digits work just like whole numbers. "
        "The only new job is to put the decimal point in the right place, and each operation has its own rule.</p>"
        + table(["Operation", "Rule for the decimal point"], [
            ["Add or subtract", "Line up the decimal points. Write zeros in empty places"],
            ["Multiply", "Do not line up the points. Count the decimal places in both factors"],
            ["Divide by a whole number", "Put the point in the quotient straight above the point in the dividend"],
            ["Divide by a decimal", "Move the point in both numbers until the divisor is whole"],
        ]) +
        "<h2>Add and subtract: line up the points</h2>"
        "<figure class='sn-fig'>" + f_add +
        "<figcaption>12.405 + 3.6: write 3.6 as 3.600 (gray zeros). Now thousandths are under thousandths. "
        "Add from the right and bring the point straight down: 16.005.</figcaption></figure>"
        + ex("Example", "What is 45.6 %s 7.83?" % MINUS,
             "Write 45.6 as 45.60. Then subtract and regroup like whole numbers: 45.60 %s 7.83 = 37.77. "
             "Check: 37.77 + 7.83 = 45.60." % MINUS, "37.77") +
        "<h2>Multiply: count the decimal places</h2>"
        "<p>Multiply as if there were no points. Then count the decimal places in <b>both</b> factors. "
        "The product has that many.</p>"
        "<figure class='sn-fig'>" + f_mul +
        "<figcaption>235 × 14 = 3,290. 2.35 has 2 places and 1.4 has 1 place, so the product has 3: 3.290 = 3.29.</figcaption></figure>"
        + ex("Example", "What is 0.06 × 0.3?",
             "6 × 3 = 18. Decimal places: 2 + 1 = 3. 18 has only 2 digits, so write a zero in front: 0.018.", "0.018") +
        "<h2>Divide by a whole number: point straight up</h2>"
        "<p>Use long division. Put the point in the quotient straight above the point in the dividend. "
        "If there is a remainder, <b>write a zero</b> and keep dividing.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>7.5 ÷ 4: write 7.5 as 7.500 (gray zeros) and keep dividing until nothing is left. "
        "The point goes straight up: 1.875.</figcaption></figure>"
        "<h2>Divide by a decimal: make the divisor whole</h2>"
        "<p>Move the point in the divisor to the end. Move the point in the dividend <b>the same number of places</b>. "
        "This multiplies both numbers by 10, 100 or 1,000, so the quotient stays the same.</p>"
        "<figure class='sn-fig'>" + f_shift +
        "<figcaption>4.56 ÷ 0.12: both points move 2 places right. 456 ÷ 12 = 38. Check: 38 × 0.12 = 4.56.</figcaption></figure>"
        + ex("Example", "What is 1.5 ÷ 0.25?",
             "0.25 has 2 decimal places, so move both points 2 places. 1.5 needs a zero: 1.50 → 150. 150 ÷ 25 = 6.", "6") +
        "<h2>Estimate to check</h2>"
        "<p>Round first. 19.8 × 3.05 is about 20 × 3 = 60, so 60.39 makes sense and 6.039 does not. "
        "Dividing by a number less than 1 gives an answer <b>bigger</b> than the dividend.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["12.405 + 3.6 = 12.441 (last digits lined up)", "Line up the points: 12.405 + 3.600 = 16.005"],
            ["45.6 %s 7.83 = 37.83 (no zero written)" % MINUS, "Write 45.60, then regroup: 37.77"],
            ["2.35 × 1.4 = 32.9 (points lined up)", "Count places: 2 + 1 = 3, so 3.29"],
            ["8.24 ÷ 4 = 2.6", "Write 0 when the divisor does not fit: 2.06"],
            ["7.5 ÷ 4 = 1.83 (remainder written as a digit)", "Write a zero and keep dividing: 1.875"],
            ["4.56 ÷ 0.12 = 0.38 (only the divisor changed)", "Move both points: 456 ÷ 12 = 38"],
        ])
    )


FAQ = [
    {"q": "How do you divide a decimal by a decimal?",
     "a": "Move the decimal point in the divisor to the end to make it a whole number, then move the point in the dividend the same number of places. Divide as usual: 4.56 ÷ 0.12 = 456 ÷ 12 = 38."},
    {"q": "How do you know where the decimal point goes when you multiply decimals?",
     "a": "Add up the decimal places in both factors; the product has that many. 2.35 × 1.4: 235 × 14 = 3,290, and 2 + 1 = 3 places gives 3.290 = 3.29."},
    {"q": "What do you do when a decimal division has a remainder?",
     "a": "Write zeros at the end of the dividend and keep dividing until the remainder is 0 (or you reach the place you need). 7.5 ÷ 4 = 7.500 ÷ 4 = 1.875."},
    {"q": "What does 6.NS.B.3 mean?",
     "a": "It is the Common Core Grade 6 standard for fluently adding, subtracting, multiplying and dividing multi-digit decimals using the standard algorithm for each operation."},
]


def gen():
    rnd = random.Random(619)
    P = People(rnd)
    sets = [set_add_sub(P), set_multiply(P), set_div_whole(P), set_div_dec(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            k = re.sub(r"<[^>]+>", "", it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "decimal-operations", "sort": 19,
        "updated": UPDATED, "pdf_url": "",
        "title": "Add, Subtract, Multiply and Divide Decimals",
        "seo_title": "Grade 6 Decimal Operations Worksheets: Add, Subtract, Multiply and Divide Multi-Digit Decimals with Answer Key",
        "short_title": "Decimal operations",
        "domain": "The Number System",
        "standard_code": "6.NS.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/NS/B/3/",
        "standard_text": "Fluently add, subtract, multiply, and divide multi-digit decimals using the standard algorithm for each operation.",
        "meta_desc": "Free Grade 6 decimal operations worksheets: add and subtract multi-digit decimals to thousandths, multiply by counting decimal places, long division with zeros, dividing by a decimal, and multi-step money and measurement word problems. 100 practice questions with an answer key and step-by-step explanations.",
        "key_big": "Each operation has one rule for the decimal point: line up the points to add or subtract, count the places to multiply, and make the divisor whole to divide.",
        "key_sub": "12.405 + 3.6 = 12.405 + 3.600. 2.35 × 1.4: 235 × 14 = 3,290, 3 places → 3.29. 7.5 ÷ 4: write zeros and keep dividing → 1.875. 4.56 ÷ 0.12 = 456 ÷ 12 = 38.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
