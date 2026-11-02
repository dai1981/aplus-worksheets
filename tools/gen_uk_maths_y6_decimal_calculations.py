# -*- coding: utf-8 -*-
"""
UK Year 6 Maths: Decimal calculations (National Curriculum in England, Year 6: Fractions (including decimals and percentages))
  python3 tools/gen_uk_maths_y6_decimal_calculations.py
Multiplying and dividing by 10, 100 and 1,000 (the digits move, the decimal point stays still), column addition
and subtraction with different numbers of decimal places, short multiplication of decimals by whole numbers,
short division with decimal answers and rounding answers to a given accuracy.
All arithmetic uses decimal.Decimal (never float), so every answer and every typical mistake is exact.
British English, pounds and pence, metric units. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from decimal import Decimal as Dm, ROUND_HALF_UP, ROUND_DOWN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
HEADFILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
GHOST = "#9a9a9a"      # zeros written to hold empty places
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
MINUS = "−"
PLACE = {3: "thousands", 2: "hundreds", 1: "tens", 0: "ones", -1: "tenths", -2: "hundredths", -3: "thousandths"}


# ------------------------------------------------------------ numbers
def N(x):
    """Exact decimal text without extra zeros, commas from 1,000: Dm('2800.0') -> '2,800'."""
    return format(Dm(x).normalize(), ",f")


def M(x):
    """Money in pounds: £5.40, £1,250.00."""
    return "£" + format(Dm(x).quantize(Dm("0.01")), ",f")


def Pn(x):
    """Pence for an amount under £1: 0.53 -> 53p."""
    p = Dm(x) * 100
    assert p == int(p) and 0 < p < 100, x
    return "%dp" % int(p)


def places(x):
    s = str(x)
    return len(s.split(".")[1]) if "." in s else 0


def digits_of(x):
    """'2.45' -> 245 (the number without its point)."""
    return int(str(x).replace(".", "").replace(",", ""))


def fixed(x, p):
    return format(Dm(x).quantize(Dm(1).scaleb(-p)), ",f")


def scale(nums):
    P = max(places(n) for n in nums)
    return P, [int(Dm(n).scaleb(P)) for n in nums]


def dig(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]          # smallest place first


def round_to(x, p):
    return Dm(x).quantize(Dm(1).scaleb(-p), rounding=ROUND_HALF_UP)


def trunc_to(x, p):
    return Dm(x).quantize(Dm(1).scaleb(-p), rounding=ROUND_DOWN)


VAL = re.compile(r"^(£)?([\d,]*\.?\d+)(p)?(.*)$")


def val(c):
    """(value, unit) of a choice: '£0.53' and '53p' are the same value. None if it is not one number."""
    m = VAL.match(c)
    if not m:
        return None
    v = Dm(m.group(2).replace(",", ""))
    if m.group(1):
        return (v, "£")
    if m.group(3):
        return (v / 100, "£")
    return (v, m.group(4).strip())


# ------------------------------------------------------------ typical mistakes (add / subtract)
def add_right_align(a, b):
    """Lined up the last digits: 4.7 + 1.25 -> 47 + 125 -> 1.72."""
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
    """Did not exchange 10 tenths for 1 one across the point."""
    P, (A, B) = scale([a, b])
    if P == 0 or (A % 10 ** P) + (B % 10 ** P) < 10 ** P:
        return None
    return Dm(A + B - 10 ** P).scaleb(-P)


def sub_no_annex(a, b):
    """Did not write the zeros: brought the extra digits of b straight down. 12.5 − 3.78 -> 8.88."""
    pa, pb = places(a), places(b)
    if pa >= pb:
        return None
    bt = Dm(b).quantize(Dm(1).scaleb(-pa), rounding=ROUND_DOWN)
    head = Dm(a) - bt
    return head + (Dm(b) - bt) if head > 0 else None


def sub_small_from_big(a, b):
    """Took the smaller digit from the bigger one in every column."""
    P, (A, B) = scale([a, b])
    k = len(str(A))
    da, db = dig(A, k), dig(B, k)
    if all(da[i] >= db[i] for i in range(k)):
        return None
    return Dm(sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))).scaleb(-P)


def sub_forgot_reduce(a, b):
    """Exchanged (added 10) but did not take 1 from the next column."""
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


# ------------------------------------------------------------ typical mistakes (multiply / divide)
def mult_wrong(a, d, carry_first=False):
    """Short multiplication of a decimal by a one-digit number with a slip.
    carry_first=False: forgot every exchanged digit. True: added the exchanged digit before multiplying."""
    k = places(a)
    ds = [int(c) for c in reversed(str(digits_of(a)))]
    c, r = 0, 0
    for i, x in enumerate(ds):
        p = (x + c) * d if carry_first else x * d
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
    return Dm(r).scaleb(-k)


def mul_cands(a, d):
    p = Dm(a) * d
    k = places(a)
    raw = digits_of(a) * d
    return [mult_wrong(a, d), Dm(raw), mult_wrong(a, d, carry_first=True), p * 10, p / 10, Dm(a) + d]


def rem_as_decimal(a, d):
    """17 ÷ 4 = 4 r 1, written as 4.1."""
    q, r = divmod(Dm(a), d)
    if r == 0 or r != int(r) or Dm(a) != int(Dm(a)):
        return None
    return Dm("%d.%d" % (q, r))


def stop_one_place(a, d):
    """Stopped after one decimal place: 17 ÷ 4 -> 4.2."""
    q = Dm(a) / d
    t = trunc_to(q, max(1, places(a)))
    return t if t != q else None


def drop_zero(q):
    """Skipped a 0 in the answer: 1.02 -> 1.2."""
    s = N(q).replace(",", "")
    i = next(j for j, ch in enumerate(s) if ch not in "0.")
    j = s.find("0", i)
    if j < 0 or j == len(s) - 1:
        return None
    return Dm(s[:j] + s[j + 1:])


def div_cands(a, d):
    q = Dm(a) / d
    return [rem_as_decimal(a, d), drop_zero(q), stop_one_place(a, d), q * 10, q / 10, Dm(a) * d]


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
        if c in seen or not c or c.startswith("-") or c.startswith(MINUS) or (v and v in vals) or (v and v[0] == 0):
            continue
        seen.add(c)
        vals.append(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def nums(vs, unit="", money=False):
    out = []
    for v in vs:
        if v is None or Dm(v) <= 0:
            out.append(None)
        elif money:
            out.append(M(v))
        else:
            out.append(N(v) + unit)
    return out


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


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


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
def pv_chart(rows, row_labels=None, hi=None):
    """Place value chart from the biggest to the smallest place used. rows: numbers as text ('4.6', '0.046').
    row_labels: text in a column on the left. hi: (row, place) to colour red."""
    def split(s):
        w, _, f = s.replace(",", "").partition(".")
        d = {}
        for j, ch in enumerate(w):
            d[len(w) - 1 - j] = ch
        for j, ch in enumerate(f):
            d[-(j + 1)] = ch
        return d
    ds = [split(r) for r in rows]
    top = max(max(d) for d in ds)
    low = min(min(d) for d in ds)
    low = min(low, -1)
    cols = list(range(top, low - 1, -1))
    CW, PW, HEAD, ROW = 104, 16, 30, 44
    LW = 84 if row_labels else 0
    x0, y0 = 6, 6
    W = 2 * x0 + LW + len(cols) * CW + PW
    H = 2 * y0 + HEAD + ROW * len(rows)
    xs, x = {}, x0 + LW
    for p in cols:
        xs[p] = x
        x += CW + (PW if p == 0 else 0)
    px = xs[0] + CW
    o = ["<rect x='%d' y='%d' width='%d' height='%d' fill='#fff' stroke='%s' stroke-width='2'/>"
         % (x0 + LW, y0, W - 2 * x0 - LW, HEAD + ROW * len(rows), GREEN),
         "<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x0 + LW, y0, W - 2 * x0 - LW, HEAD, HEADFILL)]
    for p in cols:
        if p != cols[0]:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                     % (xs[p], y0, xs[p], y0 + HEAD + ROW * len(rows), GREEN))
        o.append(text(xs[p] + CW / 2.0, y0 + 20, cap(PLACE[p]), 14))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
             % (px + PW, y0, px + PW, y0 + HEAD + ROW * len(rows), GREEN))
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
             % (x0 + LW, y0 + HEAD, W - x0, y0 + HEAD, GREEN))
    for r, s in enumerate(rows):
        yb = y0 + HEAD + ROW * r
        if r:
            o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x0 + LW, yb, W - x0, yb, GREEN))
        if row_labels and row_labels[r]:
            o.append(text(x0 + LW - 8, yb + 29, row_labels[r], 17, anchor="end", col=GREEN))
        for p, ch in ds[r].items():
            o.append(text(xs[p] + CW / 2.0, yb + 32, ch, 28, col=RED if hi == (r, p) else INK, weight=800))
        if "." in s:
            o.append("<circle cx='%.1f' cy='%d' r='4.5' fill='%s'/>" % (px + PW / 2.0, yb + 31, INK))
    return svg_wrap(W, H, "".join(o), "place value chart showing %s" % " and ".join(rows))


def addsub_svg(rows, op, answer=None, fs=28):
    """Column addition / subtraction with the decimal points in one narrow slot. Zeros written to fill empty places are grey."""
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
        ch(".", xs["pt"], y, color if "." in t else GHOST)
        for n in range(P):
            if n < len(fp):
                ch(fp[n], xs[-n - 1], y, color)
            else:
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
    """A pupil’s work with the LAST digits lined up (points not lined up), and the wrong answer in red."""
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


def exchanges(a, d):
    """Exchanged digit written under each column (slot from the right, 0 = last digit)."""
    ds = [int(c) for c in reversed(str(digits_of(a)))]
    c, out = 0, {}
    for i, x in enumerate(ds):
        p = x * d + c
        c = p // 10
        if c and i < len(ds) - 1:
            out[i + 1] = c
    return out


def short_mul_svg(a, d, ans=None, show_ex=False, fs=28):
    """Short multiplication of a decimal by a one-digit number. Numbers lined up on the right; the decimal point
    of the answer sits straight below the point in the question. Exchanged digits small under the answer."""
    cw = fs * 0.9
    top = str(a)
    full = fixed(Dm(a) * d, places(a)).replace(",", "") if ans else ""
    nd = max(len(top.replace(".", "")), len(full.replace(".", "")))
    slots = nd + 1
    W = int(cw * slots + 20)
    right = W - 10
    gap = fs * 1.2
    s = []

    def row(t, y, col=INK):
        slot = 0
        for ch in reversed(t):
            if ch == ".":
                s.append(point_mark(right - cw * slot, y, fs, col))
                continue
            s.append(text(right - cw * (slot + 0.5), y - 2, ch, fs, col=col))
            slot += 1
    y = 8 + fs
    row(top, y)
    y += gap
    row(str(d), y)
    s.append(text(right - cw * (slots - 0.5), y - 2, "×", fs, col=GREEN))
    y += 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (right - cw * slots, y, right, y, INK))
    if ans:
        y += fs + 6
        row(full, y, GREEN)
    if show_ex:
        y += 20
        for i, v in exchanges(a, d).items():
            s.append(text(right - cw * (i + 0.5), y, str(v), 16, col=RED))
    H = int(y + 10)
    lab = "%s times %d written as short multiplication" % (a, d)
    if ans:
        lab += " with the answer %s" % full
    return svg_wrap(W, H, "".join(s), lab, "monospace")


def div_steps(dividend, d):
    """Short division, digit by digit. Returns [(char index, digit, carried-in remainder, number divided, quotient digit, remainder)]."""
    out, rem = [], 0
    for i, ch in enumerate(dividend):
        if ch == ".":
            continue
        cur = rem * 10 + int(ch)
        out.append((i, int(ch), rem, cur, cur // d, cur % d))
        rem = cur % d
    return out, rem


def bus_stop_svg(dividend, d, quot=False, ghost=0, fs=28):
    """Short division (the ‘bus stop’ method). dividend: text such as '17.00'; ghost: zeros at the end shown grey.
    quot=True: show the answer above the line and the small carried remainders."""
    steps, rem = div_steps(dividend, d)
    assert rem == 0, (dividend, d)
    cw, kw = (fs * 1.05, fs * 0.5) if quot else (fs * 0.78, fs * 0.36)
    dw = len(str(d)) * fs * 0.62
    x0 = 10 + dw + 16
    xs, x = [], x0 + 6
    for ch in dividend:
        w = kw if ch == "." else cw
        xs.append(x + w / 2)
        x += w
    W = x + 10
    top = (fs + 16) if quot else 8
    by = top + fs + 6
    s = []
    for i, ch in enumerate(dividend):
        col = GHOST if (ch != "." and i >= len(dividend) - ghost) else INK
        if ch == ".":
            s.append(point_mark(xs[i], by, fs, col))
        else:
            s.append(text(xs[i], by, ch, fs, col=col))
    s.append(text(x0 - 10, by, str(d), fs, anchor="end", col=GREEN))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0, top, x0, by + 10, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x0, top, W - 4, top, INK))
    if quot:
        qy = top - 8
        started = False
        for n, (i, digit, cin, cur, q, r) in enumerate(steps):
            nxt_pt = i + 1 < len(dividend) and dividend[i + 1] == "."
            if q or started or nxt_pt:
                s.append(text(xs[i], qy, str(q), fs, col=GREEN))
                started = True
            if cin:
                s.append(text(xs[i] - fs * 0.46, by - fs * 0.45, str(cin), 15, col=RED))
        if "." in dividend:
            s.append(point_mark(xs[dividend.index(".")], qy, fs, GREEN))
    H = by + 14
    lab = "%s divided by %d written as short division" % (dividend, d)
    if quot:
        lab += " with the answer %s" % N(Dm(dividend) / d)
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s), lab, "monospace")


def line_svg(a, b, spaces, dot, labels, W=400):
    """Number line from a to b (Decimals) with equal spaces, a red dot and labels under some ticks."""
    a, b = Dm(a), Dm(b)
    L, R, Y = 34, W - 34, 30
    step = (b - a) / spaces

    def X(v):
        return L + float((R - L) * (Dm(v) - a) / (b - a))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, INK)]
    lab = [Dm(v) for v in labels]
    for i in range(spaces + 1):
        v = a + i * step
        big = v in lab
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (X(v), Y - (13 if big else 8), X(v), Y + (13 if big else 8), INK, "2.5" if big else "1.8"))
    for v in lab:
        assert (v - a) % step == 0
        s.append(text(X(v), Y + 36, N(v), 17))
    assert (Dm(dot) - a) % step == 0
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='%s'/>" % (X(dot), Y, RED))
    return svg_wrap(W, Y + 46, "".join(s), "number line from %s to %s split into %d equal spaces with a dot at %s"
                    % (N(a), N(b), spaces, N(dot)))


# ------------------------------------------------------------ explanations
def p10_e(x, op, k):
    """× or ÷ by 10, 100, 1,000."""
    m = 10 ** k
    r = Dm(x) * m if op == "×" else Dm(x) / m
    e = ("%s %s %s: every digit moves <b>%s to the %s</b>. The decimal point stays still."
         % (N(x), op, N(m), "1 place" if k == 1 else "%d places" % k, "left" if op == "×" else "right"))
    if op == "÷" and r < 1:
        e += " Write 0 in the empty places up to the ones."
    elif op == "×" and places(x) < k:
        e += " Write 0 in the empty places up to the ones."
    e += " %s %s %s = <b>%s</b>." % (N(x), op, N(m), N(r))
    return r, e


def addsub_e(a, op, b):
    P = max(places(a), places(b))
    fa, fb = fixed(a, P), fixed(b, P)
    r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
    e = "Line up the decimal points. "
    w = ["%s as %s" % (x, fx) for x, fx in ((a, fa), (b, fb)) if fx != x]
    if w:
        e += "Write " + " and ".join(w) + " so every place has a digit. "
    e += "%s %s %s = " % (fa, op, fb)
    if fixed(r, P) != N(r):
        e += "%s = " % fixed(r, P)
    e += "<b>%s</b>." % N(r)
    if op == MINUS:
        e += " Check with the inverse: %s + %s = %s." % (N(r), N(b), N(a))
    return e


def mul_steps(a, d):
    """Short multiplication, column by column, smallest place first."""
    k = places(a)
    ds = [int(c) for c in reversed(str(digits_of(a)))]
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        name = PLACE[i - k]
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        if i == len(ds) - 1 or p < 10:
            out.append("%s: %s = %d. Write %d." % (cap(name), ex_, p, p))
        else:
            out.append("%s: %s = %d. Write %d, exchange %d %s." % (cap(name), ex_, p, p % 10, p // 10,
                                                                    PLACE[i - k + 1][:-1] if p // 10 == 1 else PLACE[i - k + 1]))
        c = p // 10
    return " ".join(out)


def mul_e(a, d):
    r = Dm(a) * d
    full = fixed(r, places(a))
    e = mul_steps(a, d) + " The point goes straight below the point: %s" % full
    if full != N(r):
        e += " = <b>%s</b>." % N(r)
    else:
        e = e[:-len(full)] + "<b>%s</b>." % full
    return e


def div_e(a, d):
    q = Dm(a) / d
    need = max(places(a), places(N(q)))
    dv = fixed(a, need).replace(",", "") if need else str(a)
    steps, _ = div_steps(dv, d)
    e = ""
    if need > places(a):
        e += "Write %s as %s so you can keep dividing. " % (a, dv)
    parts = []
    for i, digit, cin, cur, qd, r in steps:
        if qd == 0 and not parts and not (i + 1 < len(dv) and dv[i + 1] == "."):
            continue
        parts.append("%d ÷ %d = %d%s" % (cur, d, qd, " r %d" % r if r else ""))
    e += "; ".join(parts) + ". Keep the point in line: %s ÷ %d = <b>%s</b>." % (a, d, N(q))
    return e


# ============================================================ set 1: × and ÷ by 10, 100, 1,000
def set_powers():
    its = []

    def p10(x, op, k, cands):
        r, e = p10_e(x, op, k)
        its.append(mcq("%s %s %s = ?" % (N(x), op, N(10 ** k)), N(r), cands, e))

    p10("4.6", "÷", 2, ["0.46", "0.0046", "460"])
    p10("0.37", "×", 1, ["0.370", "37", "0.037"])
    p10("2.58", "×", 2, ["25.8", "2.5800", "2,580"])
    p10("6.1", "×", 3, ["610", "6.1000", "61,000"])
    p10("52", "÷", 3, ["0.52", "0.0052", "5.2"])
    p10("0.4", "÷", 1, ["0.004", "4", "0.40"])
    p10("0.008", "×", 2, ["0.08", "8", "800"])
    p10("309", "÷", 2, ["3.9", "30.9", "0.309"])
    p10("7.25", "÷", 1, ["72.5", "0.0725", "7.250"])
    p10("0.06", "×", 3, ["6", "600", "0.06000"])
    p10("13.4", "÷", 2, ["1.34", "0.0134", "1,340"])
    p10("0.045", "×", 3, ["4.5", "450", "0.045000"])

    # missing numbers
    its.append(mcq("? ÷ 100 = 0.32", "32", ["3.2", "320", "0.0032"],
                   "Use the inverse: 0.32 × 100. The digits move 2 places to the left: <b>32</b>. Check: 32 ÷ 100 = 0.32."))
    its.append(mcq("4.5 × ? = 4,500", "1,000", ["100", "10", "10,000"],
                   "The 4 moved from the ones to the thousands: that is 3 places to the left, so the number is <b>1,000</b>. "
                   "(4.5 × 100 = 450.)"))
    its.append(mcq("18 ÷ ? = 0.018", "1,000", ["100", "10", "10,000"],
                   "The 1 moved from the tens to the hundredths: that is 3 places to the right, so it is ÷ <b>1,000</b>. "
                   "(18 ÷ 100 = 0.18.)"))
    its.append(mcq("Which calculation has the answer <b>0.63</b>?", "630 ÷ 1,000", ["63 ÷ 1,000", "6.3 × 10", "630 ÷ 100"],
                   "630 ÷ 1,000: the digits move 3 places to the right, so <b>630 ÷ 1,000</b> = 0.63. "
                   "63 ÷ 1,000 = 0.063, 6.3 × 10 = 63 and 630 ÷ 100 = 6.3."))

    # charts: value of the red digit after the move
    for x, op, k, place, cands in [
        ("70.5", "÷", 2, -3, ["5 tenths", "5 hundredths", "5 ones"]),
        ("3.42", "×", 1, 0, ["4 tenths", "4 tens", "4 hundredths"]),
        ("86", "÷", 3, -2, ["8 tenths", "8 thousandths", "8 tens"]),
        ("0.29", "×", 2, 1, ["2 ones", "2 tenths", "2 hundreds"]),
    ]:
        r = Dm(x) * 10 ** k if op == "×" else Dm(x) / 10 ** k
        rs = N(r)
        w, _, f = rs.partition(".")
        dg = w[len(w) - 1 - place] if place >= 0 else f[-place - 1]
        right = "%s %s" % (dg, PLACE[place])
        e = ("%s %s %s = %s. Every digit moved %d places to the %s, so the %s is now in the <b>%s</b> place. Its value is <b>%s</b>."
             % (N(x), op, N(10 ** k), rs, k, "left" if op == "×" else "right", dg, PLACE[place], right))
        if k == 1:
            e = e.replace("moved 1 places", "moved 1 place")
        its.append(mcq(fig(pv_chart([x, rs], ["", "%s %s" % (op, N(10 ** k))], hi=(1, place))) +
                       "The chart shows %s %s %s = %s. What is the value of the red digit?" % (N(x), op, N(10 ** k), rs),
                       right, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiply and divide by 10, 100 and 1,000", "items": its}


# ============================================================ set 2: add and subtract
def set_add_sub(P):
    its = []
    for a, op, b in [("3.45", "+", "2.6"), ("12.5", MINUS, "3.78"), ("7.8", "+", "0.56"), ("8", MINUS, "2.35"),
                     ("14.3", "+", "2.95"), ("9.06", MINUS, "3.7")]:
        r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
        c = add_cands(a, b) if op == "+" else sub_cands(a, b)
        word = "Use column addition." if op == "+" else "Use column subtraction."
        its.append(mcq(fig(addsub_svg([a, b], op)) + word + " The grey zeros fill the empty places.", N(r), nums(c),
                       addsub_e(a, op, b)))
    n, he, his = P.next()
    its.append(mcq(fig(wrong_column_svg(["4.7", "1.25"], "+", "1.72")) +
                   "%s worked out 4.7 + 1.25 like this. What is the correct answer?" % n, "5.95",
                   ["1.72", "5.32", "5.9"],
                   "%s lined up the last digits, so the 7 tenths were added to 5 hundredths. Line up the <b>decimal points</b>: "
                   "4.70 + 1.25 = <b>5.95</b>. (5.32 puts the 7 in the hundredths column.)" % n))
    for a, op, b in [("0.75", "+", "0.6"), ("6.07", "+", "3.9"), ("10", MINUS, "4.62"), ("5.3", MINUS, "0.86"),
                     ("15", MINUS, "6.25"), ("4.2", MINUS, "1.375"), ("23.6", "+", "8.475"), ("6.4", MINUS, "1.27"),
                     ("0.9", "+", "0.25")]:
        r = Dm(a) + Dm(b) if op == "+" else Dm(a) - Dm(b)
        c = add_cands(a, b) if op == "+" else sub_cands(a, b)
        its.append(mcq("%s %s %s = ?" % (a, op, b), N(r), nums(c) + [N(r + 1), N(r - Dm("0.1"))], addsub_e(a, op, b)))
    its.append(mcq("0.37 + ? = 1", "0.63", nums([Dm("0.73"), sub_small_from_big("1", "0.37"), sub_forgot_reduce("1", "0.37")]),
                   "Write 1 as 1.00. 1.00 %s 0.37 = <b>0.63</b>. Check: 0.37 + 0.63 = 1.00. "
                   "The hundredths make 10, so the tenths only need to make 9. (0.73 makes each digit up to 10.)" % MINUS))
    its.append(mcq("1 %s 0.45 = ?" % MINUS, "0.55", nums([Dm("0.65"), sub_small_from_big("1", "0.45"), sub_forgot_reduce("1", "0.45")]),
                   "Write 1 as 1.00. 1.00 %s 0.45 = <b>0.55</b>. Check: 0.55 + 0.45 = 1. "
                   "(0.65 makes each digit up to 10, but the tenths only need to make 9.)" % MINUS))
    s = Dm("2.5") + Dm("1.75") + Dm("0.8")
    its.append(mcq("2.5 + 1.75 + 0.8 = ?", N(s), nums([Dm("2.5") + Dm("1.75") + Dm("0.08"), Dm(250 + 175 + 8) / 100, s - 1, s * 10]),
                   "Line up the points and fill the empty places: 2.50 + 1.75 + 0.80. Hundredths: 5. Tenths: 5 + 7 + 8 = 20, "
                   "write 0, exchange 2 ones. Ones: 2 + 1 + 0 + 2 = 5. Answer: <b>%s</b>." % N(s)))
    its.append(mcq("? %s 2.6 = 4.85" % MINUS, "7.45", nums([Dm("4.85") - Dm("2.6"), add_right_align("4.85", "2.6"),
                                                            add_forgot_point_carry("4.85", "2.6")]),
                   "Use the inverse: the missing number is 4.85 + 2.6. 4.85 + 2.60 = <b>7.45</b>. Check: 7.45 %s 2.6 = 4.85." % MINUS))
    assert len(its) == 20, len(its)
    return {"title": "Add and subtract decimals", "items": its}


# ============================================================ set 3: short multiplication
def set_multiply():
    its = []
    for a, d, extra, e in [
        ("0.3", 4, ["0.12", "12", "0.7"], "3 tenths × 4 = 12 tenths. 10 tenths make 1 one, so 12 tenths = <b>1.2</b>."),
        ("0.6", 5, ["0.3", "30", "0.03"], "6 tenths × 5 = 30 tenths. 10 tenths make 1 one, so 30 tenths = <b>3</b>."),
        ("0.08", 7, ["5.6", "0.056", "56"], "8 hundredths × 7 = 56 hundredths = <b>0.56</b>."),
        ("0.04", 3, ["1.2", "0.012", "0.07"], "4 hundredths × 3 = 12 hundredths. 10 hundredths make 1 tenth, so the answer is <b>0.12</b>."),
    ]:
        r = Dm(a) * d
        its.append(mcq("%s × %d = ?" % (a, d), N(r), extra, e))
    for a, d in [("1.4", 3), ("2.6", 4), ("3.7", 6), ("5.8", 7)]:
        r = Dm(a) * d
        its.append(mcq("%s × %d = ?" % (a, d), N(r), nums(mul_cands(a, d)), mul_e(a, d)))
    for a, d in [("2.45", 6), ("1.36", 4), ("3.25", 8), ("4.07", 5), ("6.78", 3), ("9.15", 4)]:
        r = Dm(a) * d
        cands = nums(mul_cands(a, d))
        if a == "2.45":
            cands = ["147", "1.470"] + cands
        its.append(mcq(fig(short_mul_svg(a, d)) + "Use short multiplication. What is %s × %d?" % (a, d), N(r), cands, mul_e(a, d)))
    its.append(mcq("136 × 4 = 544. Use this to work out <b>1.36 × 4</b>.", "5.44", ["54.4", "544", "0.544"],
                   "1.36 is 136 ÷ 100, so 1.36 × 4 = 544 ÷ 100 = <b>5.44</b>. Estimate to check: 1.36 is about 1, and 1 × 4 = 4."))
    its.append(mcq("37 × 6 = 222. What is <b>0.37 × 6</b>?", "2.22", ["22.2", "0.222", "222"],
                   "0.37 is 37 ÷ 100, so 0.37 × 6 = 222 ÷ 100 = <b>2.22</b>. Estimate: 0.37 is less than a half, and half of 6 is 3, "
                   "so the answer is less than 3."))
    its.append(mcq("0.75 × 12 = ?", "9", ["0.9", "90", "7.5"],
                   "Partition 12 into 10 and 2. 0.75 × 10 = 7.5 and 0.75 × 2 = 1.5. 7.5 + 1.5 = <b>9</b>. "
                   "(7.5 forgets the 0.75 × 2 part. Or: three quarters of 12 is 9.)"))
    its.append(mcq("4.6 × 25 = ?", "115", ["11.5", "1,150", "92"],
                   "Partition 25 into 20 and 5. 4.6 × 20 = 92 and 4.6 × 5 = 23. 92 + 23 = <b>115</b>. "
                   "(92 forgets the 4.6 × 5 part.)"))
    its.append(mcq("Which is the best estimate for <b>3.92 × 7</b>?", "28", ["21", "2.8", "280"],
                   "Round 3.92 to the nearest whole number: 4. Then 4 × 7 = <b>28</b>. The exact answer is 27.44."))
    its.append(mcq("Which calculation has the same answer as <b>2.45 × 6</b>?", "245 × 6 ÷ 100",
                   ["245 × 6 ÷ 10", "245 × 6 × 100", "2 × 6 + 45 × 6"],
                   "2.45 = 245 ÷ 100. So 2.45 × 6 = 245 × 6 ÷ 100 = 1,470 ÷ 100 = 14.7. "
                   "(2 × 6 + 45 × 6 treats 0.45 as 45.)"))
    assert Dm("3.92") * 7 == Dm("27.44") and Dm("4.6") * 25 == 115 and Dm("0.75") * 12 == 9
    assert len(its) == 20, len(its)
    return {"title": "Multiply decimals by whole numbers", "items": its}


# ============================================================ set 4: division with decimal answers and rounding
def set_divide():
    its = []
    for a, d in [("8.4", 4), ("9.36", 3), ("7.38", 6), ("4.08", 4)]:
        q = Dm(a) / d
        its.append(mcq(fig(bus_stop_svg(a, d)) + "Use short division. What is %s ÷ %d?" % (a, d), N(q), nums(div_cands(a, d)),
                       div_e(a, d)))
    its.append(mcq(fig(bus_stop_svg("17.00", 4, ghost=2)) + "17 ÷ 4 = ? Give your answer as a decimal.", "4.25",
                   ["4.1", "4.2", "42.5"],
                   "Write 17 as 17.00 (the grey zeros). 17 ÷ 4 = 4 r 1. Exchange the 1 for 10 tenths: 10 ÷ 4 = 2 r 2. "
                   "Exchange the 2 tenths for 20 hundredths: 20 ÷ 4 = 5. Answer: <b>4.25</b>. "
                   "(4.1 writes the remainder 1 as a decimal, but r 1 means 1 left over out of 4, which is 0.25.)"))
    for a, d in [("2.4", 8), ("15.6", 6), ("6.35", 5)]:
        q = Dm(a) / d
        its.append(mcq("%s ÷ %d = ?" % (a, d), N(q), nums(div_cands(a, d)), div_e(a, d)))
    for a, d in [("13", 5), ("23", 4), ("12", 8), ("47", 5), ("39", 6), ("58", 8)]:
        q = Dm(a) / d
        its.append(mcq("%s ÷ %d = ? Give your answer as a decimal." % (a, d), N(q), nums(div_cands(a, d)),
                       div_e(a, d) + " (Not %s: the remainder is not the decimal part.)" % rem_as_decimal(a, d)))

    # rounding
    its.append(mcq(fig(line_svg("3.4", "3.5", 10, "3.45", ["3.4", "3.45", "3.5"])) +
                   "Round <b>3.45</b> to 1 decimal place.", "3.5", ["3.4", "3", "4"],
                   "3.45 is between 3.4 and 3.5. Look at the hundredths digit: 5. 5 or more rounds up, so the answer is <b>3.5</b>. "
                   "3.45 is exactly halfway, and halfway rounds up."))
    its.append(mcq("Round <b>14.27</b> to 1 decimal place.", "14.3", ["14.2", "14", "14.7"],
                   "14.27 is between 14.2 and 14.3. The hundredths digit is 7, so round up: <b>14.3</b>."))
    for a, d, p, cands in [(20, 3, 1, ["6.6", "6.2", "7"]), (10, 6, 1, ["1.6", "1.4", "2"]),
                           (25, 6, 1, ["4.1", "4", "4.17"]), (50, 7, 0, ["8", "7.1", "1"])]:
        q = Dm(a) / d
        r = round_to(q, p)
        t2 = trunc_to(q, p + 1)
        acc = "1 decimal place" if p == 1 else "the nearest whole number"
        look = "hundredths" if p == 1 else "tenths"
        dg = int(str(t2)[-1])
        e = ("%d ÷ %d = %s… (work out one more place than you need). The %s digit is %d, so round %s: <b>%s</b>."
             % (a, d, N(t2), look, dg, "up" if dg >= 5 else "down", N(r)))
        if a == 20:
            e += " (6.6 just stops; it does not round.)"
        if a == 50:
            e += " (1 is the remainder, not the answer.)"
        assert round_to(t2, p) == r
        its.append(mcq("%d ÷ %d = ? Round your answer to %s." % (a, d, acc), N(r), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Divide with decimal answers and round", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def add(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    n, he, his = P.next()
    r = Dm("1.35") * 4
    add("%s buys 4 notebooks for £1.35 each. How much does %s spend?" % (n, he), M(r),
        nums([mult_wrong("1.35", 4), Dm("54"), Dm("1.35") + 4], money=True),
        "£1.35 × 4. " + mul_steps("1.35", 4) + " Keep the point in line: %s spends <b>%s</b>." % (he, M(r)))
    n, he, his = P.next()
    r = Dm("12.50") - Dm("3.78")
    add("%s has £12.50. %s spends £3.78 on a book. How much money does %s have left?" % (n, cap(he), he), M(r),
        nums([sub_small_from_big("12.50", "3.78"), sub_no_annex("12.5", "3.78"), sub_forgot_reduce("12.50", "3.78")], money=True),
        "£12.50 %s £3.78. Line up the points and exchange: 12.50 %s 3.78 = <b>%s</b>. Check: 8.72 + 3.78 = 12.50." % (MINUS, MINUS, M(r)))
    r = Dm("47.60") / 4
    add("Four friends share a restaurant bill of £47.60 equally. How much does each person pay?", M(r),
        nums([Dm("11.30"), r / 10, r * 10], money=True),
        "47.60 ÷ 4: 4 ÷ 4 = 1; 7 ÷ 4 = 1 r 3; 36 ÷ 4 = 9; 0 ÷ 4 = 0. Each person pays <b>%s</b>. Check: 11.90 × 4 = 47.60. (£11.30 writes the remainder 3 as 30p.)" % M(r))
    q = Dm(20) / 3
    add("£20 is shared equally between 3 children. How much does each child get, to the nearest penny?", "£6.67",
        ["£6.66", "£6.20", "£6.70"],
        "20 ÷ 3 = 6.666… The nearest penny is 2 decimal places. Look at the third decimal place: 6, so round up. "
        "Each child gets <b>£6.67</b>. (£6.66 just stops; £6.20 writes the remainder 2 as 20p.)")
    assert round_to(q, 2) == Dm("6.67")
    n, he, his = P.next()
    r = Dm("3.6") / 8
    add("%s cuts a 3.6 m ribbon into 8 equal pieces. How long is each piece?" % n, "0.45 m",
        ["0.44 m", "4.5 m", "0.045 m"],
        "3.6 ÷ 8: 8 does not go into 3, so write 0. 36 tenths ÷ 8 = 4 r 4. Exchange the 4 tenths for 40 hundredths: "
        "40 ÷ 8 = 5. Each piece is <b>0.45 m</b> (45 cm). (0.44 m writes the remainder 4 as the next digit.)")
    assert r == Dm("0.45")
    r = Dm("1.25") * 6
    add("A bag of apples has a mass of 1.25 kg. What is the mass of 6 bags?", "7.5 kg",
        nums(mul_cands("1.25", 6), " kg"),
        "1.25 × 6. " + mul_steps("1.25", 6) + " Keep the point in line: 7.50 kg. The 6 bags have a mass of <b>7.5 kg</b>.")
    assert r == Dm("7.5")
    a, ah, _ = P.next()
    b, bh, _ = P.next()
    r = Dm("3.2") - Dm("2.85")
    add("In the long jump, %s jumps 3.2 m and %s jumps 2.85 m. How much further does %s jump?" % (a, b, a), N(r) + " m",
        nums([sub_no_annex("3.2", "2.85"), sub_small_from_big("3.20", "2.85"), sub_forgot_reduce("3.20", "2.85")], " m"),
        "3.2 %s 2.85. Write 3.2 as 3.20, then subtract: 3.20 %s 2.85 = <b>0.35 m</b>. Check: 2.85 + 0.35 = 3.2." % (MINUS, MINUS))
    add("A pack of 100 pencils costs £18. How much is one pencil?", "18p", ["£1.80", "1.8p", "0.18p"],
        "£18 ÷ 100: the digits move 2 places to the right, so one pencil costs £0.18 = <b>18p</b>. "
        "(£1.80 is £18 ÷ 10.)")
    add("A cycle path is 4.5 km long. How many metres is that?", "4,500 m", ["450 m", "45,000 m", "4.5000 m"],
        "1 km = 1,000 m, so multiply by 1,000. The digits move 3 places to the left: 4.5 × 1,000 = <b>4,500 m</b>.")
    r = Dm("45.50") / 7
    add("7 friends share a £45.50 bill equally. How much does each pay?", M(r), ["£6.30", "£65.00", "£0.65"],
        "45.50 ÷ 7: 45 ÷ 7 = 6 r 3. Exchange the 3 for 30 tenths, with the 5 tenths that makes 35 tenths: 35 ÷ 7 = 5. "
        "0 ÷ 7 = 0. Each pays <b>%s</b>. (£6.30 writes the remainder 3 as 30p.)" % M(r))
    assert r == Dm("6.5")
    n, he, his = P.next()
    q = Dm(8) / 3
    add("%s cuts 8 m of rope into 3 equal pieces. How long is each piece, to 1 decimal place?" % n, "2.7 m",
        ["2.6 m", "2.2 m", "3 m"],
        "8 ÷ 3 = 2.66… To round to 1 decimal place, look at the hundredths digit: 6, so round up. Each piece is <b>2.7 m</b>. "
        "(2.2 m writes the remainder 2 as a decimal.)")
    assert round_to(q, 1) == Dm("2.7")
    n, he, his = P.next()
    t = Dm("1.49") * 3
    ch = 5 - t
    add("%s buys 3 bottles of juice at £1.49 each. %s pays with a £5 note. How much change does %s get?" % (n, cap(he), he),
        Pn(ch), ["63p", M(t), M(sub_small_from_big("5.00", "4.47"))],
        "3 × £1.49 = £4.47. Then £5.00 %s £4.47 = £0.53 = <b>53p</b>. Check: 4.47 + 0.53 = 5. "
        "(63p makes each digit up to 10.)" % MINUS)
    assert ch == Dm("0.53")
    r = Dm("1.86") / 6
    add("A box of 6 eggs costs £1.86. How much does one egg cost?", Pn(r), ["3.1p", "£3.10", "£11.16"],
        "£1.86 ÷ 6: 6 does not go into 1, so write 0. 18 ÷ 6 = 3. 6 ÷ 6 = 1. £0.31 = <b>31p</b>. Check: 31p × 6 = 186p.")
    r = Dm("1.6") - Dm("0.85")
    add("A sunflower grows from 0.85 m to 1.6 m tall. How much does it grow?", N(r) + " m",
        nums([sub_no_annex("1.6", "0.85"), sub_small_from_big("1.60", "0.85"), sub_forgot_reduce("1.60", "0.85")], " m"),
        "1.6 %s 0.85. Write 1.6 as 1.60: 1.60 %s 0.85 = <b>0.75 m</b>. Check: 0.85 + 0.75 = 1.6." % (MINUS, MINUS))
    assert r == Dm("0.75")
    n, he, his = P.next()
    r = Dm("0.4") * 7
    add("One lap of the school field is 0.4 km. %s runs 7 laps. How far does %s run?" % (n, he), "2.8 km",
        ["0.28 km", "28 km", "7.4 km"],
        "4 tenths × 7 = 28 tenths = <b>2.8 km</b>.")
    assert r == Dm("2.8")
    q = Dm("17.30") / 4
    add("A taxi fare of £17.30 is shared equally by 4 people. How much does each person pay, to the nearest penny?", "£4.33",
        ["£4.32", "£4.30", "£43.25"],
        "17.30 ÷ 4 = 4.325. The third decimal place is 5, so round up to the nearest penny: <b>£4.33</b>. "
        "(£4.32 just stops; £4.30 is rounded to the nearest 10p, not the nearest penny.)")
    assert q == Dm("4.325") and round_to(q, 2) == Dm("4.33")
    add("One sheet of paper has a mass of 4.5 g. What is the mass of 1,000 sheets in kilograms?", "4.5 kg",
        ["45 kg", "0.45 kg", "4,500 kg"],
        "4.5 × 1,000 = 4,500 g. 1,000 g = 1 kg, so 4,500 g ÷ 1,000 = <b>4.5 kg</b>.")
    r = Dm("2.35") * 5
    add("Paint costs £2.35 per litre. How much do 5 litres cost?", M(r),
        nums([mult_wrong("2.35", 5), mult_wrong("2.35", 5, carry_first=True), Dm("117.5")], money=True),
        "£2.35 × 5. " + mul_steps("2.35", 5) + " Keep the point in line: 5 litres cost <b>%s</b>." % M(r))
    n, he, his = P.next()
    r = Dm("0.65") + Dm("1.2") + Dm("0.8")
    add("%s buys a drink for 65p, a sandwich for £1.20 and an apple for 80p. How much does %s spend?" % (n, he), M(r),
        ["£146", "£1.46", "£1.93"],
        "Write everything in pounds: £0.65 + £1.20 + £0.80. Line up the points: 0.65 + 1.20 + 0.80 = <b>%s</b>. "
        "(£146 adds 65 + 1 + 80 without changing the pence into pounds; £1.93 writes 80p as £0.08.)" % M(r))
    assert r == Dm("2.65")
    q = Dm("2.5") / 4
    add("A 2.5 litre bottle of water is poured equally into 4 jugs. How much is in each jug, to 1 decimal place?",
        "0.6 litres", ["0.62 litres", "0.7 litres", "0.625 litres"],
        "2.5 ÷ 4 = 0.625. To round to 1 decimal place, look at the hundredths digit: 2, so round down. "
        "Each jug has about <b>0.6 litres</b>. (0.62 and 0.625 are not rounded to 1 decimal place.)")
    assert q == Dm("0.625") and round_to(q, 1) == Dm("0.6")
    assert len(its) == 20, len(its)
    return {"title": "Money and measure word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert Dm("4.6") / 100 == Dm("0.046") and Dm("2.45") * 6 == Dm("14.7") and Dm(17) / 4 == Dm("4.25")
    assert Dm("12.5") - Dm("3.78") == Dm("8.72")
    f_chart = pv_chart(["4.6", "0.046"], ["", "÷ 100"])
    f_add = addsub_svg(["12.5", "3.78"], MINUS, answer="8.72")
    f_mul = short_mul_svg("2.45", 6, ans=True, show_ex=True)
    f_div = bus_stop_svg("17.00", 4, quot=True, ghost=2)
    f_round = line_svg("3.4", "3.5", 10, "3.46", ["3.4", "3.45", "3.5"])
    return (
        "<h2>Multiply and divide by 10, 100 and 1,000</h2>"
        "<p>The <b>digits move</b>; the decimal point stays still. Multiplying moves every digit to the left. "
        "Dividing moves every digit to the right: 1 place for 10, 2 places for 100, 3 places for 1,000. "
        "Fill empty places up to the ones with 0.</p>"
        "<figure class='sn-fig'>" + f_chart +
        "<figcaption>4.6 ÷ 100: the 4 moves from the ones to the hundredths and the 6 from the tenths to the thousandths. "
        "4.6 ÷ 100 = 0.046.</figcaption></figure>"
        + ex("Example", "0.037 × 1,000", "Each digit moves 3 places to the left. The 3 goes to the tens and the 7 to the ones.", "37")
        + "<h2>Add and subtract: line up the points</h2>"
        "<p>Use column addition and column subtraction. Line up the <b>decimal points</b>, not the last digits. "
        "Write zeros in empty places so every column has a digit.</p>"
        "<figure class='sn-fig'>" + f_add +
        "<figcaption>12.5 − 3.78: write 12.5 as 12.50 (grey zero). Exchange as usual: 12.50 − 3.78 = 8.72.</figcaption></figure>"
        "<h2>Multiply a decimal by a whole number</h2>"
        "<p>Use short multiplication. Start with the smallest place. The point in the answer goes straight below the point in the question.</p>"
        "<figure class='sn-fig'>" + f_mul +
        "<figcaption>2.45 × 6. Hundredths: 5 × 6 = 30, write 0, exchange 3 tenths. Tenths: 4 × 6 + 3 = 27, write 7, exchange 2 ones. "
        "Ones: 2 × 6 + 2 = 14. Answer: 14.70 = 14.7.</figcaption></figure>"
        "<p>Estimate first: 2.45 is about 2.5, and 2.5 × 6 = 15. So 14.7 makes sense; 1.47 and 147 do not.</p>"
        "<h2>Divide: keep going past the point</h2>"
        "<p>Use short division. When there is a remainder, write the point and zeros after the number and keep dividing. "
        "The point in the answer goes straight above the point in the number.</p>"
        "<figure class='sn-fig'>" + f_div +
        "<figcaption>17 ÷ 4: 17 ÷ 4 = 4 r 1. Exchange 1 one for 10 tenths: 10 ÷ 4 = 2 r 2. "
        "Exchange 2 tenths for 20 hundredths: 20 ÷ 4 = 5. 17 ÷ 4 = 4.25.</figcaption></figure>"
        "<h2>Round to the accuracy you are asked for</h2>"
        "<p>Work out one more place than you need. Then look at that digit: <b>5 or more</b>, round up; <b>4 or less</b>, round down. "
        "Money is rounded to the nearest penny (2 decimal places).</p>"
        "<figure class='sn-fig'>" + f_round +
        "<figcaption>3.46 is past 3.45, the halfway point, so 3.46 rounds to 3.5 (1 decimal place).</figcaption></figure>"
        + ex("Example", "£10 is shared equally by 3 people. How much does each get, to the nearest penny?",
             "10 ÷ 3 = 3.333… The third decimal place is 3, so round down.", "£3.33")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4.6 ÷ 100 = 0.46 or 0.0046", "÷ 100 moves the digits exactly 2 places: 0.046"],
            ["4.6 × 10 = 4.60 (adding a zero)", "The digits move 1 place left: 46"],
            ["Lining up the last digits: 4.7 + 1.25 = 1.72", "Line up the points: 4.70 + 1.25 = 5.95"],
            ["2.45 × 6 = 147 or 1.470", "Keep the point in line: 14.70 = 14.7"],
            ["17 ÷ 4 = 4.1 (remainder written as a decimal)", "Write 17.00 and keep dividing: 4.25"],
            ["Rounding 3.45 to 1 decimal place as 3.4", "The hundredths digit is 5, so round up: 3.5"],
        ])
    )


FAQ = [
    {"q": "What decimal calculations are in the Year 6 SATs?",
     "a": "The arithmetic paper has questions like 12.5 − 3.78, 2.45 × 6, 4.6 ÷ 100 and 9.36 ÷ 3, and the reasoning papers use decimals in money and measure problems, sometimes with answers rounded to a given accuracy."},
    {"q": "How do you divide a whole number to get a decimal answer?",
     "a": "Use short division and do not stop at the remainder. Write a decimal point and zeros after the number, exchange the remainder into tenths and hundredths and keep dividing: 17 ÷ 4 = 17.00 ÷ 4 = 4.25."},
    {"q": "How do you multiply a decimal by a whole number in Year 6?",
     "a": "Use short multiplication, starting with the smallest place and exchanging as usual, and put the decimal point in the answer straight below the point in the question. 2.45 × 6 = 14.70, which is 14.7."},
    {"q": "Does the decimal point move when you multiply by 10?",
     "a": "In English schools children are taught that the digits move and the decimal point stays still. When you multiply by 10 each digit moves one place to the left, so 3.42 × 10 = 34.2."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (place value charts, number lines) so labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(6610)
    P = People(rnd)
    sets = [set_powers(), set_add_sub(P), set_multiply(), set_divide(), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vs = [val(c) for c in it["c"]]
            known = [v for v in vs if v is not None]
            assert len(set(known)) == len(known), it["c"]
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-6", "slug": "decimal-calculations", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Decimal Calculations",
        "seo_title": "Year 6 Decimal Calculations Worksheets: × and ÷ by 10, 100, 1,000, Short Multiplication and Division with Decimals",
        "short_title": "Decimal calculations",
        "domain": "Fractions (including decimals and percentages)",
        "standard_code": "Year 6: Fractions (including decimals and percentages)",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Multiply and divide numbers by 10, 100 and 1,000 giving answers up to three decimal places; multiply one-digit numbers with up to two decimal places by whole numbers; use written division methods in cases where the answer has up to two decimal places; solve problems which require answers to be rounded to specified degrees of accuracy.",
        "meta_desc": "Free Year 6 maths worksheets on decimal calculations for the National Curriculum and KS2 SATs: multiply and divide by 10, 100 and 1,000, add and subtract decimals, short multiplication and short division with decimal answers, rounding, and money and measure problems. 100 questions with an answer key.",
        "key_big": "The digits move, the decimal point stays still. Line up the points to add and subtract, and keep the point in line when you multiply and divide.",
        "key_sub": "4.6 ÷ 100 = 0.046. 12.5 − 3.78 = 12.50 − 3.78 = 8.72. 2.45 × 6 = 14.7. 17 ÷ 4 = 17.00 ÷ 4 = 4.25, not 4.1. 3.45 to 1 decimal place is 3.5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(place value chart|number line)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
