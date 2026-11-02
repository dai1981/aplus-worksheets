# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Money and financial problems (Australian Curriculum v9.0, AC9M4N08)
  python3 tools/gen_au_maths_y4_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Writing money: under $1 as 45c, from $1 as $2.35 (never $2.35c, never $2.5).
Australian coins: 5c, 10c, 20c, 50c (12-sided), $1, $2. Notes: $5, $10, $20, $50, $100.
No 1c or 2c coins: cash totals are rounded to the nearest 5c.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

# ------------------------------------------------------------ money facts
ORDER = ["N100", "N50", "N20", "N10", "N5", "C200", "C100", "C50", "C20", "C10", "C5"]   # biggest value first
VAL = {"N100": 10000, "N50": 5000, "N20": 2000, "N10": 1000, "N5": 500, "C200": 200, "C100": 100,
       "C50": 50, "C20": 20, "C10": 10, "C5": 5}
TOK = {v: k for k, v in VAL.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius (drawn in proportion to the real coins: $2 smaller than $1; 50c the biggest), colours, label size
COIN = {"C5": (16, SILVER, 14), "C10": (19, SILVER, 14), "C20": (23, SILVER, 15), "C50": (25, SILVER, 15),
        "C100": (20, GOLD, 15), "C200": (17, GOLD, 14)}
NOTE = {"N5": ("#efcfe3", "#8a3a6e"), "N10": ("#c4dcf2", "#1f5f99"), "N20": ("#f5c9b3", "#a33a1c"),
        "N50": ("#f4e3a0", "#7a5f0c"), "N100": ("#cbe7c4", "#2f7a2a")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%dc" % v


def nat(c):
    """45 -> '45c', 345 -> '$3.45' (cents under $1, dollars with two digits after the point from $1)."""
    assert c > 0, c
    return "%dc" % c if c < 100 else "${}.{:02d}".format(c // 100, c % 100)


def aud(c):
    """always in dollars: 75 -> '$0.75'"""
    return "${}.{:02d}".format(c // 100, c % 100)


def cen(c):
    assert c < 10000
    return "%dc" % c


def whole(c):
    assert c % 100 == 0
    return "$%d" % (c // 100)


def mval(s):
    """value in cents of a money text, or None: '$2.5' -> 250, '$3' -> 300, '1000c' -> 1000"""
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^\$(\d+)(?:\.(\d{1,2}))?$", s)
    if m:
        f = m.group(2) or "0"
        return int(m.group(1)) * 100 + int(f.ljust(2, "0"))
    m = re.match(r"^(\d+)c$", s)
    if m:
        return int(m.group(1))
    return None


def total(toks):
    return sum(VAL[t] for t in toks)


def srt(toks):
    return sorted(toks, key=ORDER.index)


def toks_of(*pairs):
    out = []
    for t, n in pairs:
        out += [t] * n
    return srt(out)


def counts(toks):
    return [(t, toks.count(t)) for t in ORDER if t in toks]


def group(toks):
    return ", ".join("%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks))


def cap(s):
    return s[0].upper() + s[1:]


def round5(c):
    """cash rounding: 1c, 2c down; 3c, 4c up to 5c; 6c, 7c down to 5c; 8c, 9c up"""
    r = c % 5
    return c - r if r <= 2 else c + 5 - r


# ------------------------------------------------------------ explanations
def count_on(toks):
    dollars = [t for t in srt(toks) if VAL[t] >= 100]
    cents = [t for t in srt(toks) if VAL[t] < 100]
    out, s = [], 0
    if dollars:
        run = []
        for t in dollars:
            s += VAL[t]
            run.append("$%d" % (s // 100))
        out.append("Count the dollars: %s." % ", ".join(run))
    C = 0
    if cents:
        run = []
        for t in cents:
            C += VAL[t]
            run.append("%dc" % C)
        out.append(("Count on the cents: %s." if dollars else "Start with the biggest coin: %s.") % ", ".join(run))
    T = total(toks)
    if dollars and cents:
        if C >= 100:
            out.append("%dc = %s. $%d + %s = <b>%s</b>." % (C, aud(C), s // 100, aud(C), nat(T)))
        else:
            out.append("$%d and %dc is <b>%s</b>." % (s // 100, C, nat(T)))
    elif dollars:
        out.append("That is <b>%s</b>." % nat(T))
    else:
        out.append("That is <b>%s</b>." % nat(T) if C < 100 else "%dc = <b>%s</b>." % (C, nat(T)))
    return " ".join(out)


def add_e(nums):
    """partition into dollars and cents"""
    T = sum(nums)
    dl = [n // 100 for n in nums if n >= 100]
    ct = [n % 100 for n in nums if n % 100]
    D, c = sum(dl), sum(ct)
    out = []
    if len(dl) > 1:
        out.append("Add the dollars: %s = $%d." % (" + ".join("$%d" % x for x in dl), D))
    elif dl:
        out.append("Dollars: $%d." % D)
    if len(ct) > 1:
        if c >= 100:
            out.append("Add the cents: %s = %dc = %s. Regroup 100c as $1." % (" + ".join("%dc" % x for x in ct), c, aud(c)))
        else:
            out.append("Add the cents: %s = %dc." % (" + ".join("%dc" % x for x in ct), c))
    elif ct:
        out.append("Cents: %dc." % c)
    if D and c:
        out.append("$%d + %s = <b>%s</b>." % (D, nat(c), nat(T)))
    else:
        out.append("Total: <b>%s</b>." % nat(T))
    assert D * 100 + c == T
    return " ".join(out)


# ------------------------------------------------------------ typical mistakes (all computed, in cents)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


def m_dollar_as_c(toks):
    """counted dollar coins and notes as cents ($2 -> 2c)"""
    return sum(VAL[t] // 100 if VAL[t] >= 100 else VAL[t] for t in toks)


def kinds(toks):
    return [t for t, n in counts(toks)]


def m_skip(toks, k=-1):
    return total(toks) - VAL[kinds(toks)[k]]


def m_twice(toks, k=-1):
    return total(toks) + VAL[kinds(toks)[k]]


def m_same_step(toks):
    """kept the old step for the first coin of each new kind"""
    s, prev = 0, None
    for t in srt(toks):
        s += VAL[prev] if prev is not None and t != prev else VAL[t]
        prev = t
    return s


def drop_zero(c):
    """$2.05 written as $2.50 (the 0 placeholder lost)"""
    return (c // 100) * 100 + (c % 100) * 10 if 0 < c % 100 < 10 else None


def digs(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def from_digs(d):
    return sum(x * 10 ** i for i, x in enumerate(d))


def noexch_add(nums):
    """column addition without regrouping: each column mod 10"""
    k = max(len(str(n)) for n in nums)
    return from_digs([sum(digs(n, k)[i] for n in nums) % 10 for i in range(k)])


def forgot_dollar_add(nums):
    """made 100c or more in the cents but did not regroup it as $1"""
    return sum(n // 100 for n in nums) * 100 + sum(n % 100 for n in nums) % 100


def small_from_big(a, b):
    """column subtraction taking the smaller digit from the bigger one"""
    k = len(str(a))
    return from_digs([abs(x - y) for x, y in zip(digs(a, k), digs(b, k))])


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=nat):
    """4 choices: correct + the first 3 unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0:
                continue
            c = fmt(c)
        c = str(c)
        v = mval(c)
        if c in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(c)
        if v is not None:
            seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
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


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def tok_size(t):
    if t.startswith("N"):
        return NOTE_W, NOTE_H
    r = COIN[t][0]
    return 2 * r, 2 * r


def dodecagon(cx, cy, r):
    pts = []
    for i in range(12):
        a = math.radians(15 + 30 * i)
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def draw_tok(t, cx, cy):
    """one coin (circle, or 12-sided for 50c, with its value) or one note (rectangle with its value)"""
    if t.startswith("N"):
        fill, edge = NOTE[t]
        x, y = cx - NOTE_W / 2, cy - NOTE_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, NOTE_W, NOTE_H, fill, edge, x + 5, y + 5, NOTE_W - 10, NOTE_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r, (fill, edge), fs = COIN[t]
    if t == "C50":
        shape = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (dodecagon(cx, cy, r), fill, edge)
                 + "<polygon points='%s' fill='none' stroke='%s' stroke-width='1'/>" % (dodecagon(cx, cy, r - 4), edge))
    else:
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, edge))
    return shape + text(cx, cy + fs * 0.36, lab(VAL[t]), fs)


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    widths = [sum(tok_size(t)[0] for t in r) + gap * (len(r) - 1) for r in rows]
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rw, rh in zip(rows, widths, heights):
        x = pad
        hh = rh - lab_h
        for t in r:
            w, h = tok_size(t)
            s.append(draw_tok(t, x + w / 2, y + hh / 2))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(W, H, "".join(s), label or ("money: " + group(toks)))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def shuffled(toks, rnd):
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


# ------------------------------------------------------------ counting on for change
def L(c):
    """a point on a number line or in an explanation: 40c, $1, $6.40"""
    return nat(c) if c % 100 else whole(c)


def J(j):
    """a jump: 5c, 60c, $3, $1.50"""
    return lab(j) if j < 100 or j % 100 == 0 else nat(j)


def change_pts(price, paid):
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s % 100 and s < paid:
        s += 100 - s % 100
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid
    return pts


def count_up(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (L(a), J(b - a), L(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(J(j) for j in jumps), nat(ch))
    return "Count on from %s to %s: %s.%s" % (L(price), L(paid), ", ".join(steps), tail)


def change_cands(paid, price):
    """real change mistakes, in order of how often they happen"""
    r = paid - price
    c = []
    if paid > 100 and price % 100:
        c.append(r + 100)           # $5 − $3.40: took away the dollars ($2) and kept 60c, forgetting the $1 used for the cents
    if price % 10:
        c.append(r + 10)            # 35c + 75c "makes 100": 3 + 7 = 10 and 5 + 5 = 10, but that is 110c
    c += [price, small_from_big(paid, price), r - 10, r + 5, r - 5, r + 50]
    return [x for x in c if 0 < x < paid and x % 5 == 0]


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting on; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [120, 140, 160][:len(pts) - 1]
    x0, y0 = 44, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 44
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, L(p), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + J(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting on from %s to %s" % (L(price), L(paid)))


def price_svg(items, title):
    """a row of price tags: [('muffin', 250), ...]"""
    gap, pad, h = 10, 6, 62
    ws = [max(len(n) * 9 + 24, 78) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, nat(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, nat(p)) for n, p in items))



# ------------------------------------------------------------ Year 4 helpers
def sub_e(a, b):
    """a − b by counting on from b to a"""
    r = a - b
    pts = change_pts(b, a)
    assert all(x < y for x, y in zip(pts, pts[1:])) and pts[-1] == a
    return count_up(b, a) + " So %s − %s = <b>%s</b>." % (nat(a), nat(b), nat(r))


def sub_cands(a, b):
    r = a - b
    c = [small_from_big(a, b) if len(str(a)) == len(str(b)) else None,
         r + 100 if (a % 100) < (b % 100) else None,   # took away the cents the wrong way and kept the dollar
         a + b, r - 100, r + 10, r - 10, r + 100]
    return c


def mul_e(n, p):
    D, C = p // 100, p % 100
    T = n * p
    if C == 0:
        return "%d × $%d = <b>%s</b>." % (n, D, nat(T))
    if D == 0:
        return "%d × %dc = %dc = <b>%s</b>." % (n, C, n * C, nat(T))
    cc = n * C
    ctxt = ("%d × %dc = %dc = %s" % (n, C, cc, nat(cc))) if cc >= 100 else ("%d × %dc = %dc" % (n, C, cc))
    return ("Split %s into $%d and %dc. %d × $%d = $%d. %s. $%d + %s = <b>%s</b>."
            % (nat(p), D, C, n, D, n * D, ctxt, n * D, nat(cc), nat(T)))


def mul_cands(n, p):
    T = n * p
    D, C = p // 100, p % 100
    return [n * D * 100 + C if C else None,                  # multiplied only the dollars
            n * D * 100 + (n * C) % 100 if n * C >= 100 else None,  # did not regroup the cents
            p + n * 100,                                     # added instead of multiplied
            T // 10 if T % 10 == 0 else None,                # point in the wrong place
            T - p, T + p]


def div_e(A, n):
    q = A // n
    assert q * n == A
    if A % 100 == 0 and q % 100 == 0:
        return "$%d ÷ %d = <b>$%d</b>, because %d × %d = %d." % (A // 100, n, q // 100, n, q // 100, A // 100)
    return ("Change to cents: %s = %dc. %d ÷ %d = %d, so each share is %dc = <b>%s</b>. Check: %d × %s = %s."
            % (nat(A), A, A, n, q, q, nat(q), n, nat(q), nat(A)))


def div_cands(A, n):
    q = A // n
    D, C = A // 100, A % 100
    c = []
    if C and D >= n:
        c.append((D // n) * 100 + C)                         # divided only the dollars, kept the cents
    if D % n:
        c.append((D // n) * 100 + (D % n) * 10 if (D % n) < 10 else None)  # remainder written as cents: 26 ÷ 4 = 6 r 2 -> $6.20
    c += [A - n * 100, A * n if A * n < 100000 else None, q - 100, q + 100, q * 10, q - 50, q + 50]
    return c


def chq(paid):
    return "a %s note" % whole(paid)


# ============================================================ set 1: dollars and cents
def set_dollars(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=nat, novc=False):
        if novc:   # choices are ways of writing the same value: only one is written correctly
            assert len(set([right] + wrong)) == 4
            it = {"q": q, "c": [right] + wrong, "a": 0, "e": e, "_novc": 1}
        else:
            it = mcq(q, right, wrong, e, fmt)
        its.append(it)

    s("Write 435c in dollars.", "$4.35", ["$43.50", "$435.00", "$4.53"],
      "100c = $1, so 435c = 400c + 35c = $4 and 35c: <b>$4.35</b>. $43.50 would be 4350c.")
    s("Write 85c in dollars.", "$0.85", ["$85.00", "$8.50", "$0.58"],
      "85c is less than $1, so there are 0 dollars: <b>$0.85</b>. $85.00 is 85 whole dollars.")
    s("Write 907c in dollars.", "$9.07", ["$9.70", "$90.70", "$97.00"],
      "907c = 900c + 7c = $9 and 7c. The cents need two digits, so 7c is .07: <b>$9.07</b>. $9.70 would be 970c.")
    s("Write 1260c in dollars.", "$12.60", ["$126.00", "$1.26", "$12.06"],
      "1260c = 1200c + 60c = $12 and 60c: <b>$12.60</b>. $1.26 would be only 126c.")
    s("Write $4.65 in cents.", 465, [65, 4650, 456],
      "$4.65 is $4 and 65c. $4 = 400c, so 400c + 65c = <b>465c</b>. 65c leaves out the $4.", cen)
    s("Write $7.05 in cents.", 705, [75, 750, 7050],
      "$7.05 is $7 and 5c. 700c + 5c = <b>705c</b>. 750c would be $7.50.", cen)
    s("Write $10.40 in cents.", 1040, [104, 1004, 140],
      "$10.40 is $10 and 40c. $10 = 1000c, so 1000c + 40c = <b>1040c</b>.", cen)
    s("How do you write 6 dollars and 8 cents?", "$6.08", ["$6.80", "$68.00", "14c"],
      "8 cents needs two digits, so it is 08: <b>$6.08</b>. $6.80 would be 6 dollars and 80 cents. Do not add 6 and 8.")
    s("How do you write 3 dollars and 5 cents?", "$3.05", ["$3.50", "$35.00", "8c"],
      "5 cents is .05: <b>$3.05</b>. $3.50 would be 3 dollars and 50 cents.")
    s("Ruby writes four dollars fifty as “$4.5”. What is the correct way to write it?", "$4.50",
      ["$4.05", "$45.00", "45c"],
      "Cents always take two digits after the point, so fifty cents is .50: <b>$4.50</b>. $4.05 would be four dollars and five cents.")
    s("Which amount is written correctly?", "$3.70", ["$3.7", "$3.70c", "3.70c"],
      "Use $ at the front and two digits after the point: <b>$3.70</b>. Do not write both $ and c, and do not drop the 0.",
      novc=True)
    s("Which is the same as $6.40?", 640, [64, 6040, 604],
      "$6.40 is $6 and 40c. 600c + 40c = <b>640c</b>. 604c would be $6.04.", cen)
    s("Which is more: $2.09 or 210c?", "210c", ["$2.09", "They are the same.", "You cannot tell."],
      "Write both in cents: $2.09 = 209c. 210c is 1c more than 209c, so <b>210c</b> is more.")
    s("Which is more: $3.40 or 304c?", "$3.40", ["304c", "They are the same.", "You cannot tell."],
      "$3.40 = 340c. 340c is more than 304c, so <b>$3.40</b> is more.")
    amts = ["$2.05", "250c", "$2.15"]
    right = ", ".join(sorted(amts, key=mval))
    wl = ["250c, $2.15, $2.05", "$2.05, 250c, $2.15", "$2.15, $2.05, 250c"]
    for w in wl:
        assert w != right and sorted(w.split(", ")) == sorted(amts)
    s("Put these in order, smallest first: $2.05, 250c, $2.15.", right, wl,
      "Write them all in cents: $2.05 = 205c, 250c, $2.15 = 215c. Smallest first: <b>%s</b>." % right)
    amts = ["95c", "$1.10", "$0.99"]
    right = ", ".join(sorted(amts, key=mval, reverse=True))
    wl = ["95c, $0.99, $1.10", "$0.99, 95c, $1.10", "95c, $1.10, $0.99"]
    for w in wl:
        assert w != right and sorted(w.split(", ")) == sorted(amts)
    s("Put these in order, largest first: 95c, $1.10, $0.99.", right, wl,
      "In cents: 95c, $1.10 = 110c, $0.99 = 99c. Largest first: <b>%s</b>. 95 is a big number, but 95c is less than $1." % right)
    s("How many 20c coins make $3?", "15", ["5", "30", "60"],
      "Five 20c coins make $1. $3 is 3 lots of $1, so 3 × 5 = <b>15</b> coins. 5 coins only make $1. 30 coins would be 10c coins.")
    s("How many 50c coins make $4.50?", "9", ["4", "45", "8"],
      "Two 50c coins make $1, so $4 needs 8 coins. One more 50c makes $4.50: 8 + 1 = <b>9</b> coins.")
    toks = toks_of(("C200", 2), ("C50", 1), ("C20", 2), ("C5", 1))
    T = total(toks)
    assert T == 495
    s(fig(money_svg(shuffled(toks, rnd))) + "How much money is shown?", T,
      [m_dollar_as_c(toks), m_skip(toks, -1), m_twice(toks, 0), m_count(toks)],
      "Put the money in order, biggest value first. " + count_on(toks))
    toks = toks_of(("N10", 1), ("N5", 1), ("C200", 1), ("C50", 1), ("C10", 1), ("C5", 1))
    T = total(toks)
    assert T == 1765
    s(fig(money_svg(shuffled(toks, rnd), per_row=6)) + "How much money is shown?", T,
      [m_dollar_as_c(toks), m_skip(toks, 0), m_twice(toks, -1), m_skip(toks, 2)],
      "Put the money in order, biggest value first. " + count_on(toks))
    assert len(its) == 20
    return {"title": "Dollars and cents", "items": its}


# ============================================================ set 2: add and subtract money
SHOP = [("pen", 245), ("ruler", 180), ("glue", 375), ("notebook", 460)]


def set_addsub(P, rnd):
    its = []

    def add(nums, q=None, extra=""):
        T = sum(nums)
        cands = [forgot_dollar_add(nums), noexch_add(nums)]
        if any(n < 100 for n in nums) and any(n >= 100 for n in nums):
            cands.insert(0, sum(n * 100 if n < 100 else n for n in nums))   # 80c read as $80
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        cands += [T - 100, T + 100, T - 10, T + 10]
        if q is None:
            q = " + ".join(nat(n) for n in nums) + " = ?"
        its.append(mcq(q, T, cands, add_e(nums) + extra))

    def sub(a, b, q=None, extra=""):
        if q is None:
            q = "%s − %s = ?" % (nat(a), nat(b))
        its.append(mcq(q, a - b, sub_cands(a, b), sub_e(a, b) + extra))

    add([345, 230])
    add([265, 180])
    add([190, 85])
    add([475, 350])
    add([625, 275])
    add([438, 295])
    add([1450, 375])
    add([1275, 650])
    add([560, 385, 240])
    price = dict(SHOP)
    nm, he, his = P.next()
    add([price["glue"], price["notebook"]], fig(price_svg(SHOP, "newsagent")) +
        "At the newsagent, %s buys glue and a notebook. How much does %s spend?" % (nm, he))
    sub(560, 230)
    sub(725, 380)
    sub(900, 435)
    sub(650, 85)
    sub(1240, 575)
    sub(1005, 260)
    sub(1500, 725)
    sub(2000, 1365)
    nm, he, his = P.next()
    sub(price["notebook"], price["ruler"], fig(price_svg(SHOP, "newsagent")) +
        "How much more does a notebook cost than a ruler?")
    sub(3050, 1875)
    assert len(its) == 20
    return {"title": "Add and subtract money", "items": its}


# ============================================================ set 3: change
def set_change(P, rnd):
    its = []
    jobs = [(1000, 635, "a book", True), (1000, 780, "a pair of goggles", False), (1000, 345, "a box of crayons", False),
            (1000, 915, "a pack of footy cards", False), (2000, 1345, "a netball", True), (2000, 1690, "a lunchbox", False),
            (2000, 1275, "a beach towel", False), (2000, 860, "a pizza", False), (2000, 1555, "a puzzle", True),
            (5000, 3260, "a pair of runners", True), (5000, 4175, "a cricket bat", False), (5000, 2895, "a skateboard helmet", False),
            (5000, 1840, "a board game", False), (5000, 4630, "a backpack", True), (1000, 590, "a frisbee", False),
            (5000, 3705, "a water bottle and a cap", False)]
    for paid, pr, thing, line in jobs:
        nm, he, his = P.next()
        r = paid - pr
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, nat(pr), cap(he), chq(paid), he)
        if line:
            q = fig(change_line(pr, paid, show=False)) + q + " Count on along the number line."
        e = count_up(pr, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (nat(r), nat(pr), nat(r), L(paid))
        its.append(mcq(q, r, change_cands(paid, pr), e))
    rule = ("There are no 1c or 2c coins, so a cash total is rounded to the nearest 5c. "
            "Ends in 1 or 2: round down to 0. Ends in 3 or 4: up to 5. Ends in 6 or 7: down to 5. Ends in 8 or 9: up to the next 10. ")
    for paid, amt in [(1000, 847), (2000, 1392), (5000, 2638), (2000, 1756)]:
        nm, he, his = P.next()
        R = round5(amt)
        other = R + 5 if R < amt else R - 5
        ch = paid - R
        q = ("%s’s shopping comes to %s. %s pays cash with %s, so the total is rounded to the nearest 5c. "
             "How much change does %s get?" % (nm, nat(amt), cap(he), chq(paid), he))
        e = (rule + "%s ends in %d, so it rounds to %s. " % (nat(amt), amt % 10, nat(R)) + count_up(R, paid)
             + " The change is <b>%s</b>." % nat(ch))
        its.append(mcq(q, ch, [paid - amt, paid - other, ch + 100, R], e))
    assert len(its) == 20
    return {"title": "Change from $10, $20 and $50", "items": its}


# ============================================================ set 4: multiply and divide money
def set_muldiv(P, rnd):
    its = []

    def mul(n, p, q):
        its.append(mcq(q, n * p, mul_cands(n, p), mul_e(n, p)))

    def div(A, n, q):
        its.append(mcq(q, A // n, div_cands(A, n), div_e(A, n)))

    mul(3, 250, "3 × $2.50 = ?")
    mul(5, 120, "5 × $1.20 = ?")
    mul(4, 75, "4 × 75c = ?")
    div(2800, 4, "$28 ÷ 4 = ?")
    div(480, 4, "$4.80 ÷ 4 = ?")
    nm, he, his = P.next()
    mul(4, 650, "Movie tickets cost $6.50 each. %s buys 4 tickets. How much does %s pay?" % (nm, he))
    nm, he, his = P.next()
    div(3600, 4, "%s and 3 friends share $36 equally. How much does each person get?" % nm)
    mul(6, 450, "A swimming lesson costs $4.50. How much do 6 lessons cost?")
    div(2400, 3, "3 children share the cost of a $24 present equally. How much does each pay?")
    nm, he, his = P.next()
    mul(8, 250, "%s buys 8 bus tickets at $2.50 each. How much does %s spend?" % (nm, he))
    div(750, 3, "3 rulers cost $7.50 altogether. How much is 1 ruler?")
    mul(3, 375, "A packet of seeds costs $3.75. How much do 3 packets cost?")
    div(840, 4, "4 apples cost $8.40. How much is 1 apple?")
    nm, he, his = P.next()
    mul(5, 340, "%s buys 5 notebooks at $3.40 each. What is the total cost?" % nm)
    div(1500, 6, "6 friends share $15 of pocket money equally. How much does each get?")
    div(930, 3, "Sausages are $9.30 for a pack of 3. How much is 1 sausage?")
    mul(7, 150, "A fruit cup costs $1.50. How much do 7 fruit cups cost?")
    div(2550, 5, "5 students share a $25.50 bill equally. How much does each pay?")
    mul(3, 1275, "A ticket to the aquarium costs $12.75. How much do 3 tickets cost?")
    div(2600, 4, "4 friends share the cost of a $26 pizza equally. How much does each pay?")
    qs = [it["q"] for it in its]
    assert len(set(qs)) == 20
    assert len(its) == 20
    return {"title": "Multiply and divide money", "items": its}


# ============================================================ set 5: budgets and best buys
CANTEEN = [("sausage roll", 350), ("juice", 240), ("banana bread", 280), ("ice block", 160)]


def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    pr = dict(CANTEEN)
    # 1
    nm, he, his = P.next()
    cost = pr["sausage roll"] + pr["banana bread"]
    assert cost == 630
    add(fig(price_svg(CANTEEN, "school canteen")) + "%s has $8. At the canteen %s buys a sausage roll and banana bread. "
        "How much money is left?" % (nm, he), 800 - cost, [forgot_dollar_add([350, 280]) and 800 - forgot_dollar_add([350, 280]),
                                                           small_from_big(800, cost), cost],
        "Cost: " + add_e([350, 280]) + " " + count_up(cost, 800) + " <b>$1.70</b> is left. "
        "$2.70 forgets to regroup 130c as $1.30. $6.30 is the cost, not what is left.")
    # 2
    nm, he, his = P.next()
    assert 5 * 600 == 3000
    add("%s gets $6 pocket money a week and saves it all. After 5 weeks, can %s buy a $32 cricket bat?" % (nm, he),
        "No, %s needs $2 more." % he, ["Yes, with $2 left.", "No, %s needs $21 more." % he, "Yes, with $8 left."],
        "5 × $6 = $30. $30 is less than $32, so <b>no</b>. $30 + $2 = $32, so %s needs <b>$2 more</b>. "
        "$21 comes from adding 6 + 5 = 11." % he)
    # 3
    nm, he, his = P.next()
    sp = 750 + 480
    add("%s has a budget of $20 for the school fete. %s spends $7.50 on rides and $4.80 on food. "
        "How much of the budget is left?" % (nm, cap(he)), 2000 - sp, [2000 - forgot_dollar_add([750, 480]), sp, 2000 - sp - 100],
        "Spent: $7.50 + $4.80 = $12.30 (50c + 80c = 130c = $1.30). " + count_up(sp, 2000)
        + " <b>$7.70</b> is left. $8.70 forgets to regroup 130c. $12.30 is what was spent.")
    # 4
    assert 4 * 140 == 560 and 560 - 500 == 60
    add("Juice boxes cost $1.40 each, or $5 for a pack of 4. Which is the better buy for 4 juice boxes?",
        "the pack of 4, saving 60c", ["4 single boxes, saving 60c", "They cost the same.", "the pack of 4, saving $3.60"],
        "4 single boxes: 4 × $1.40 = $5.60. The pack costs $5. $5.60 − $5 = 60c, so <b>the pack saves 60c</b>. "
        "$3.60 compares the pack with only 1 box.")
    # 5
    assert 300 // 6 == 50 and 450 // 10 == 45
    add("Pencils come in 6 for $3 or 10 for $4.50. Which costs less for each pencil?", "10 for $4.50",
        ["6 for $3", "They cost the same.", "You cannot tell."],
        "6 for $3: 300c ÷ 6 = 50c each. 10 for $4.50: 450c ÷ 10 = 45c each. 45c is less, so <b>10 for $4.50</b>. "
        "The cheaper packet is not always the better buy.")
    # 6
    nm, he, his = P.next()
    add("At the school fete, raffle tickets are $2 each or 3 for $5. %s buys 6 tickets the cheapest way. "
        "How much does %s pay?" % (nm, he), 1000, [1200, 1100, 3000],
        "6 tickets is 2 lots of 3. 2 × $5 = <b>$10</b>. Buying them one at a time costs 6 × $2 = $12. "
        "$11 is one lot of 3 and 3 single tickets.")
    # 7
    assert 40 * 150 == 6000 and 6000 - 2200 == 3800
    add("Year 4 sell cupcakes at the fete for $1.50 each. They sell 40 cupcakes. The ingredients cost $22. "
        "How much money do they make after paying for the ingredients?", 3800, [6000, 8200, 1850],
        "40 × $1 = $40 and 40 × 50c = 2000c = $20. $40 + $20 = $60. $60 − $22 = <b>$38</b>. "
        "$60 forgets the cost of the ingredients. $18.50 comes from 40 × $1 + 50c − $22.")
    # 8
    nm, he, his = P.next()
    add("%s’s mum gives %s $40 for the holidays. %s spends a quarter of it on a book. How much is the book?"
        % (nm, "her" if he == "she" else "him", cap(he)), 1000, [3000, 3600, 400],
        "A quarter means divide by 4. $40 ÷ 4 = <b>$10</b>. $30 is what is left, not the book. $36 takes away 4.")
    # 9
    assert 3 * 1450 == 4350
    add("A child’s ticket to the zoo costs $14.50. How much do 3 child tickets cost?", 4350, mul_cands(3, 1450),
        mul_e(3, 1450) + " $42.50 multiplies only the dollars.")
    # 10
    nm, he, his = P.next()
    assert (4500 - 1800) // 300 == 9
    add("%s wants headphones that cost $45. %s has $18 and saves $3 a week. How many weeks until %s has enough?"
        % (nm, cap(he), he), "9 weeks", ["15 weeks", "6 weeks", "27 weeks"],
        "%s needs $45 − $18 = $27 more. $27 ÷ $3 = <b>9 weeks</b>. 15 weeks forgets the $18 already saved. "
        "27 is dollars, not weeks." % cap(he))
    # 11
    nm, he, his = P.next()
    assert round5(1348) == 1350
    add("At the fete, %s’s total is $13.48. %s pays cash with a $20 note. Cash totals are rounded to the nearest 5c. "
        "How much change does %s get?" % (nm, cap(he), he), 650, [652, 655, 750],
        "$13.48 ends in 8, so it rounds up to $13.50. " + count_up(1350, 2000) + " The change is <b>$6.50</b>. "
        "$6.52 forgets to round the total.")
    # 12
    nm, he, his = P.next()
    assert 5 * 160 == 800
    add("%s has $10 for the canteen this week. %s buys a $1.60 ice block every day from Monday to Friday. "
        "How much is left?" % (nm, cap(he)), 200, [800, 470, 360],
        "5 × $1.60: 5 × $1 = $5 and 5 × 60c = 300c = $3. $5 + $3 = $8. $10 − $8 = <b>$2</b>. "
        "$8 is the amount spent. $3.60 is only 4 days.")
    # 13
    add("Which number sentence finds the change from $50 for 3 books at $12.50 each?", "$50 − 3 × $12.50",
        ["3 × $12.50 − $50", "$50 − $12.50 + 3", "$50 ÷ 3 − $12.50"],
        "First find the cost: 3 × $12.50 = $37.50. Then take it away from $50: <b>$50 − 3 × $12.50</b> = $12.50. "
        "Multiply before you subtract.")
    # 14
    nm, he, his = P.next()
    add("%s buys 2 pies at $4.50 each and a drink for $3. Which number sentence shows the total cost?" % nm,
        "2 × $4.50 + $3", ["2 × ($4.50 + $3)", "$4.50 + $3", "2 + $4.50 + $3"],
        "Two pies is 2 × $4.50. Add one drink: <b>2 × $4.50 + $3</b> = $9 + $3 = $12. "
        "2 × ($4.50 + $3) would buy 2 drinks.")
    # 15
    nm, he, his = P.next()
    assert 2 * 175 - 310 == 40
    add("A 2 L bottle of milk costs $3.10. A 1 L bottle costs $1.75. %s needs 2 L. How much does %s save by buying "
        "the 2 L bottle instead of two 1 L bottles?" % (nm, he), 40, [135, 350, 175],
        "Two 1 L bottles: 2 × $1.75 = $3.50. $3.50 − $3.10 = <b>40c</b>. $1.35 compares the 2 L bottle with just one 1 L bottle.")
    # 16
    nm, he, his = P.next()
    assert 3 * 2850 == 8550
    add("%s’s family buys 3 tickets to a theme park at $28.50 each. They pay with a $100 note. How much change do they get?"
        % nm, 1450, [1550, 8550, 1500],
        mul_e(3, 2850).replace("<b>", "").replace("</b>", "") + " " + count_up(8550, 10000)
        + " The change is <b>$14.50</b>. $15.50 multiplies only the dollars (3 × $28 + 50c = $84.50).")
    # 17
    assert 2400 // 80 == 30
    add("At the fete, Year 4 sell lemonade for 80c a cup. They make $24. How many cups do they sell?", "30 cups",
        ["3 cups", "300 cups", "24 cups"],
        "$24 = 2400c. 2400 ÷ 80 = <b>30 cups</b>. Check: 30 × 80c = 2400c = $24. "
        "3 cups uses 24 ÷ 8 and forgets that $24 is 2400c.")
    # 18
    nm, he, his = P.next()
    assert round5(1297) == 1295
    add("%s has $25. %s buys a book for $12.97 and pays cash, so the price is rounded to the nearest 5c. "
        "How much money does %s have left?" % (nm, cap(he), he), 1205, [1203, 1200, 1305],
        "$12.97 ends in 7, so it rounds down to $12.95. " + count_up(1295, 2500) + " <b>$12.05</b> is left. "
        "$12.00 rounds the price up to $13 by mistake.")
    # 19
    nm, he, his = P.next()
    assert 8 * 250 == 2000
    add("%s earns $2.50 a week for doing jobs at home. How much does %s earn in 8 weeks?" % (nm, he), 2000,
        [1650, 1050, 1750],
        mul_e(8, 250) + " $16.50 multiplies only the dollars. $10.50 adds 8 instead of multiplying. $17.50 is 7 weeks.")
    # 20
    nm, he, his = P.next()
    sp = 1850 + 1275
    assert sp == 3125
    add("%s has $50 for a school excursion. The bus costs $18.50 and entry costs $12.75. The rest is for lunch. "
        "How much is for lunch?" % nm, 5000 - sp, [5000 - forgot_dollar_add([1850, 1275]), sp, small_from_big(5000, sp)],
        "Bus and entry: $18.50 + $12.75 = $31.25 (50c + 75c = 125c = $1.25). " + count_up(sp, 5000)
        + " <b>$18.75</b> is for lunch. $19.75 forgets to regroup 125c.")
    assert len(its) == 20
    return {"title": "Budgets and best buys", "items": its}


# ============================================================ lesson
def body_html():
    walk = toks_of(("N10", 1), ("C200", 1), ("C50", 1), ("C10", 1), ("C5", 1))
    assert total(walk) == 1265
    assert round5(847) == 845 and round5(1392) == 1390 and round5(1348) == 1350
    return (
        "<h2>Dollars and cents</h2>"
        "<p>$1 = 100c. In $4.65, the 4 is the dollars and the 65 is the cents. "
        "Cents always take <b>two digits</b> after the point: write $4.50, not $4.5, and $3.05 for 3 dollars and 5 cents.</p>"
        + table(["Cents", "Dollars and cents", "Write"], [
            ["85c", "$0 and 85c", "$0.85"],
            ["435c", "$4 and 35c", "$4.35"],
            ["907c", "$9 and 7c", "$9.07"],
            ["1260c", "$12 and 60c", "$12.60"],
        ]) +
        "<figure class='sn-fig'>" + money_svg(walk, per_row=5, gap=24, pad=16, under=["$10", "$12", "$12.50", "$12.60", "$12.65"],
                                              label="counting on: $10, $12, $12.50, $12.60, $12.65") +
        "<figcaption>Count the biggest value first: $10, $12, $12.50, $12.60, $12.65.</figcaption></figure>"
        "<h2>Add and subtract money</h2>"
        "<p>Add the dollars, then add the cents. If the cents make 100c or more, regroup 100c as $1.</p>"
        + ex("Example", "$2.75 + $1.50",
             "Dollars: $2 + $1 = $3. Cents: 75c + 50c = 125c = $1.25. $3 + $1.25 = $4.25.", "$4.25") +
        "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Jump to the next 10c, then to the next dollar, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(1345, 2000) +
        "<figcaption>Change from $20 for $13.45: 5c + 50c + $6 = $6.55.</figcaption></figure>"
        + ex("Example", "A cricket bat costs $41.75. Pay with a $50 note. What is the change?",
             "$41.75 + 5c = $41.80. $41.80 + 20c = $42. $42 + $8 = $50. 5c + 20c + $8 = $8.25. "
             "Check: $41.75 + $8.25 = $50.", "$8.25")
        + "<p>Paying cash? There are no 1c or 2c coins, so the total is rounded to the nearest 5c. "
        "$8.47 becomes $8.45, $13.92 becomes $13.90 and $13.48 becomes $13.50. Card payments are not rounded.</p>"
        "<h2>Multiply and divide money</h2>"
        "<p>To multiply, split the price into dollars and cents. To divide, change the amount to cents first.</p>"
        + ex("Example", "4 tickets at $6.50 each",
             "4 × $6 = $24. 4 × 50c = 200c = $2. $24 + $2 = $26.", "$26.00")
        + ex("Example", "Share $4.80 equally between 4",
             "$4.80 = 480c. 480 ÷ 4 = 120. 120c = $1.20. Check: 4 × $1.20 = $4.80.", "$1.20")
        + "<h2>Budgets and best buys</h2>"
        "<p>Write a number sentence for the problem, then work it out. To find the better buy, compare the cost of the "
        "<b>same amount</b>: juice boxes at $1.40 each cost 4 × $1.40 = $5.60, so a 4-pack for $5 saves 60c.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["$4.5", "Cents take two digits: $4.50"],
            ["$2.75 + $1.50 = $3.25", "75c + 50c = 125c = $1.25, so the total is $4.25"],
            ["435c = $43.50", "100c = $1, so 435c = $4.35"],
            ["Change from $5 for $3.40 is $2.60", "Count on: $3.40 + 60c = $4, $4 + $1 = $5. The change is $1.60"],
            ["4 × $6.50 = $24.50", "Multiply the cents too: 4 × 50c = $2, so the total is $26"],
            ["$26 ÷ 4 = $6.20 (6 remainder 2)", "The remainder $2 is 200c. 200c ÷ 4 = 50c, so each share is $6.50"],
        ])
    )


FAQ = [
    {"q": "What do Year 4 students learn about money in the Australian Curriculum?",
     "a": "In Year 4 (AC9M4N08), students solve practical problems with money, including adding, subtracting, multiplying and dividing amounts, working out change and comparing prices. They write number sentences for each problem and choose an efficient way to calculate."},
    {"q": "How do you teach a Year 4 child to work out change?",
     "a": "Count on from the price to the money paid: first to the next 10c, then to the next dollar, then to the note. For $13.45 from $20 that is 5c + 50c + $6 = $6.55."},
    {"q": "Why are cash prices rounded to 5 cents in Australia?",
     "a": "Australia has no 1c or 2c coins, so a cash total is rounded to the nearest 5c: $8.47 becomes $8.45 and $13.48 becomes $13.50. Card payments are charged the exact amount."},
    {"q": "How do you find the best buy?",
     "a": "Compare the cost of the same amount. Pencils at 6 for $3 cost 50c each, and 10 for $4.50 cost 45c each, so the 10-pack is the better buy."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4809)
    P = People(rnd)
    sets = [set_dollars(P, rnd), set_addsub(P, rnd), set_change(P, rnd), set_muldiv(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            if not it.pop("_novc", None):
                vv = [v for v in (mval(c) for c in it["c"]) if v is not None]
                assert len(set(vv)) == len(vv), it["c"]
            for c in it["c"]:
                assert "¢" not in c
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "money-and-financial-problems", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money and Financial Problems: Change, Budgets and Best Buys",
        "seo_title": "Year 4 Money Worksheets: Adding Money, Change, Budgets and Best Buys",
        "short_title": "Money and financial problems",
        "domain": "Number",
        "standard_code": "AC9M4N08",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical problems involving additive and multiplicative situations including financial contexts; formulate the problems using number sentences and choose efficient calculation strategies",
        "meta_desc": "Free Year 4 maths worksheets on money: write dollars and cents ($4.65, 435c), add and subtract money, give change from $10, $20 and $50 by counting on, multiply and divide amounts, and solve canteen, pocket money and school fete budget problems. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "$1 = 100c. Work in dollars and cents, and regroup 100c as $1.",
        "key_sub": "Give change by counting on from the price: $13.45 + 5c + 50c + $6 = $20, so the change is $6.55. Cash totals round to the nearest 5c.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|counting|price)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
