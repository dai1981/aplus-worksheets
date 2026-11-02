# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Money (Australian Curriculum v9.0, AC9M3M06)
  python3 tools/gen_au_maths_y3_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Writing money: under $1 as 45c, from $1 as $2.35 (never $2.35c, never $2.5).
Australian coins: 5c, 10c, 20c, 50c (12-sided), $1, $2 (the $2 coin is smaller than the $1 coin).
Notes: $5, $10, $20, $50, $100. No 1c or 2c coins: cash totals are rounded to the nearest 5c.
Coins and notes are simple labelled shapes (no real designs).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
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


# ============================================================ set 1: count the money
def set_count(P, rnd):
    its = []
    groups = [
        [("C10", 5)], [("C5", 6)], [("C20", 4)], [("C50", 1), ("C20", 1), ("C5", 1)],
        [("C20", 2), ("C10", 1), ("C5", 1)], [("C50", 1), ("C20", 1), ("C10", 1), ("C5", 1)],
        [("C50", 2)], "SIZE1", [("C100", 3)], "SIZE2", [("C200", 2), ("C100", 1)],
        [("C100", 1), ("C50", 1)], [("C200", 1), ("C50", 1), ("C20", 1)],
        [("C200", 1), ("C20", 1), ("C10", 1), ("C5", 1)], [("C100", 1), ("C50", 1), ("C20", 2), ("C5", 1)],
        [("C200", 1), ("C5", 1)], [("C100", 2), ("C50", 1), ("C10", 1), ("C5", 1)],
        [("N5", 1), ("C100", 1), ("C50", 1)], [("N10", 1), ("C200", 1), ("C20", 1), ("C5", 1)],
        [("N20", 1), ("N10", 1), ("C200", 1), ("C50", 1), ("C5", 1)],
    ]
    mixed = {5, 12, 14, 16, 18, 19}
    stems = ["How much money is shown?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s pencil case. How much is it?", "What is the total?",
             "%s puts this money in a money box. How much is in the box?"]
    seen_t = set()
    for i, g in enumerate(groups):
        if g == "SIZE1":
            toks = ["C50", "C200", "C20", "C100"]
            q = fig(money_svg(toks, gap=10, label="coins: 50c, $2, 20c, $1")) + "Which coin is worth the most?"
            e = ("The <b>$2</b> coin is worth the most, even though it is one of the smallest coins. "
                 "The 50c coin is the biggest coin, but it is only worth 50 cents. Read the value, not the size.")
            its.append(mcq(q, "$2", ["50c", "$1", "20c"], e))
            continue
        if g == "SIZE2":
            q = (fig(money_svg(["C100", "C200"], gap=14, label="coins: $1 (bigger), $2 (smaller)"))
                 + "The $1 coin is bigger than the $2 coin. Which is worth more?")
            e = ("The <b>$2 coin</b> is worth more. It is smaller than the $1 coin, but $2 is two dollars. "
                 "The size of a coin does not tell you its value.")
            its.append(mcq(q, "the $2 coin", ["the $1 coin", "They are worth the same.", "You cannot tell."], e))
            continue
        toks = toks_of(*g)
        T = total(toks)
        assert T not in seen_t, T
        seen_t.add(T)
        assert len(toks) <= 7
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if any(t.startswith("N") for t in toks) and "coins" in st:
            st = stems[4]
        if st.count("%s") == 2:
            st = st % (nm, his if "pencil" in st else he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = ("Put the money in order, biggest value first. " if i in mixed else "") + count_on(toks)
        if len(set(toks)) == 1:
            t, n = toks[0], len(toks)
            if VAL[t] >= 100:
                e = "Each coin is $1. Count in dollars: %s. That is <b>%s</b>." % (
                    ", ".join("$%d" % k for k in range(1, n + 1)), nat(T))
            else:
                e = "Each coin is %s. Count in %ds: %s. That is <b>%s</b>." % (
                    lab(VAL[t]), VAL[t], ", ".join("%dc" % (VAL[t] * k) for k in range(1, n + 1)), nat(T))
            if T == 100:
                e = e.replace("<b>100c</b>", "100c = <b>$1.00</b>").replace("That is <b>$1.00</b>", "That is 100c = <b>$1.00</b>")
        e += " Count the value of each coin, not the number of coins." if i < 3 else ""
        cands = [m_count(toks), drop_zero(T) if T >= 100 else None, m_dollar_as_c(toks), m_same_step(toks), m_skip(toks, -1),
                 m_twice(toks, 0), m_skip(toks, 0), m_twice(toks, -1)]
        if T >= 100:
            cands = [drop_zero(T), m_dollar_as_c(toks)] + cands[3:][i % 3:] + cands[3:][:i % 3] + [m_count(toks)]
        if T == 100:
            cands = [2, 50, 150, 1000]     # 2 coins; one coin only; counted on one too many; $10.00 (100 read as dollars)
            assert m_count(toks) == 2
        its.append(mcq(q, T, cands, e))
    assert len(its) == 20
    return {"title": "Count the money", "items": its}


# ============================================================ set 2: dollars and cents
def set_convert(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=nat):
        its.append(mcq(q, right, wrong, e, fmt))

    s("How many cents make $1?", "100c", ["10c", "1000c", "50c"],
      "$1 = <b>100c</b>. That is why the cents always have two digits after the point.")
    s("$3 = ? c", 300, [30, 3, 3000], "$1 = 100c, so $3 = 100c + 100c + 100c = <b>300c</b>.", cen)
    s("$10 = ? c", 1000, [100, 10, 110], "$1 = 100c, so $10 = 10 × 100c = <b>1000c</b>. 110c adds 10 + 100.", cen)
    s("How many 10c coins make $1?", "10", ["100", "1", "5"],
      "Count in 10s up to 100c: 10c, 20c, 30c … 100c. That is <b>10</b> coins.")
    s("How many 20c coins make $1?", "5", ["4", "10", "20"],
      "Count in 20s up to 100c: 20c, 40c, 60c, 80c, 100c. That is <b>5</b> coins. 4 coins only make 80c.")
    s("How many 50c coins make $2?", "4", ["2", "3", "50"],
      "Two 50c coins make $1. So $2 needs 2 + 2 = <b>4</b> coins. 2 coins only make $1.")
    s("Write 250c in dollars.", "$2.50", ["$25.00", "$250.00", "$2.05"],
      "250c = 200c + 50c = $2 and 50c. Write <b>$2.50</b>. $25.00 would be 2500c.")
    s("Write 175c in dollars.", "$1.75", ["$17.50", "$175.00", "75c"],
      "175c = 100c + 75c = $1 and 75c. Write <b>$1.75</b>. Do not forget the $1.")
    s("Write 305c in dollars.", "$3.05", ["$3.50", "$30.50", "$305.00"],
      "305c = 300c + 5c = $3 and 5c. The cents need two digits, so 5c is .05: <b>$3.05</b>. $3.50 would be 350c.")
    s("Write 640c in dollars.", "$6.40", ["$64.00", "$6.04", "$640.00"],
      "640c = 600c + 40c = $6 and 40c: <b>$6.40</b>. $6.04 would be 604c.")
    s("Write $1.05 in cents.", 105, [15, 150, 1005],
      "$1.05 is $1 and 5c. $1 = 100c, so 100c + 5c = <b>105c</b>. It is not 15c: the 1 is a whole dollar.", cen)
    s("Write $2.50 in cents.", 250, [25, 205, 2500],
      "$2.50 is $2 and 50c. 200c + 50c = <b>250c</b>.", cen)
    s("Write $4.20 in cents.", 420, [42, 402, 4200],
      "$4.20 is $4 and 20c. 400c + 20c = <b>420c</b>. 42c would be less than $1.", cen)
    s("Write $6.85 in cents.", 685, [85, 658, 6850],
      "$6.85 is $6 and 85c. 600c + 85c = <b>685c</b>. 85c leaves out the $6.", cen)
    s("How do you write 2 dollars and 35 cents?", "$2.35", ["$235.00", "37c", "$23.50"],
      "Write $, the dollars, a point, then two digits for the cents: <b>$2.35</b>. Do not add the 2 and the 35.")
    s("How do you write 3 dollars and 5 cents?", "$3.05", ["$3.50", "$35.00", "8c"],
      "5 cents needs two digits, so it is 05: <b>$3.05</b>. $3.50 would be 3 dollars and 50 cents.")
    s("Leo writes 2 dollars and 50 cents as “$2.5”. What is the right way to write it?", "$2.50", ["$2.05", "$25.00", "25c"],
      "The cents always take two digits, so 50 cents is .50: <b>$2.50</b>. $2.05 would be 2 dollars and 5 cents.")
    s("Which is more: $1.50 or 105c?", "$1.50", ["105c", "They are the same.", "You cannot tell."],
      "Write both in cents: $1.50 = 150c. 150c is more than 105c, so <b>$1.50</b> is more.")
    s("Which is more: 95c or $1.05?", "$1.05", ["95c", "They are the same.", "You cannot tell."],
      "$1.05 = 105c. 105c is more than 95c, so <b>$1.05</b> is more. 95c is less than $1.")
    amts = ["$1.20", "105c", "$1.50"]
    right = ", ".join(sorted(amts, key=mval))
    wl = ["$1.20, $1.50, 105c", "$1.50, $1.20, 105c", "105c, $1.50, $1.20"]
    for w in wl:
        assert w != right and sorted(w.split(", ")) == sorted(amts)
    s("Put these in order, smallest first: $1.20, 105c, $1.50.", right, wl,
      "Write them in cents: $1.20 = 120c, 105c, $1.50 = 150c. Smallest first: <b>%s</b>. "
      "105c is not 105 dollars." % right)
    assert len(its) == 20
    return {"title": "Dollars and cents", "items": its}


# ============================================================ set 3: different ways to make an amount
def gtxt(vals):
    return ", ".join(lab(v) for v in sorted(vals, reverse=True))


def fewest(target):
    """fewest coins (5c to $2) by dynamic programming"""
    coins = [5, 10, 20, 50, 100, 200]
    best = {0: []}
    for a in range(5, target + 1, 5):
        opts = [best[a - c] + [c] for c in coins if a - c in best]
        best[a] = min(opts, key=len)
    return best[target]


def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None, figtoks=None):
        """choices are groups of coins/notes; exactly one makes the target (or, for NOT, exactly one does not)"""
        assert sum(right) == target, (target, right)
        for w in wrong:
            assert sum(w) != target, (target, w)
        q = (stem or "Which coins make %s?") % L(target)
        e = ("<b>%s</b> = %s. " % (gtxt(right), L(target)) + " ".join(
            "%s = %s." % (gtxt(w), L(sum(w))) for w in wrong))
        its.append(mcq(q, gtxt(right), [gtxt(w) for w in wrong], e))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> = %s, not %s. " % (gtxt(right), L(sum(right)), L(target))
             + "The others all make %s." % L(target))
        its.append(mcq("Which of these does <b>not</b> make %s?" % L(target), gtxt(right), [gtxt(w) for w in wrong], e))

    def how_few(target, wrong, extra):
        f = fewest(target)
        n = len(f)
        ch = lambda k: "%d coin" % k if k == 1 else "%d coins" % k
        e = "Use the biggest coin you can each time: %s. That is <b>%s</b>. %s" % (gtxt(f) + " = " + L(target), ch(n), extra)
        its.append(mcq("What is the fewest coins you can use to make %s?" % L(target), ch(n), [ch(k) for k in wrong], e))

    def which_fewest(target, wrong):
        f = fewest(target)
        for w in wrong:
            assert sum(w) == target and len(w) > len(f)
        e = ("All of these make %s. <b>%s</b> uses only %d coins: start with the biggest coin you can."
             % (L(target), gtxt(f), len(f)))
        its.append(mcq("Which uses the fewest coins to make %s?" % L(target), gtxt(f), [gtxt(w) for w in wrong], e))

    def same_as(toks, right, wrong, word="coin"):
        T = total(toks)
        q = fig(money_svg(toks)) + "Which is worth the same as this money?"
        e = count_on(toks) + " One %s %s is worth the same." % (lab(T), word)
        e = e.replace(" One %s %s" % (lab(T), word), " So <b>one %s %s</b>" % (lab(T), word))
        its.append(mcq(q, right, wrong, e))

    which(30, [20, 10], [[20, 5], [10, 10], [20, 20]])
    which(75, [50, 20, 5], [[50, 20, 10], [20, 20, 20, 5], [50, 10, 10]])
    assert total(["C20", "C20", "C10"]) == 50
    same_as(["C20", "C20", "C10"], "one 50c coin", ["one 20c coin", "one $1 coin", "one 10c coin"])
    which(100, [50, 50], [[50, 20, 20], [20, 20, 20, 20], [10, 10, 10, 10, 10]])
    how_few(40, [1, 3, 4], "There is no 40c coin, so 1 coin is not possible.")
    which_not(60, [50, 5], [[50, 10], [20, 20, 20], [20, 20, 10, 10]])
    nm, he, his = P.next()
    which(45, [20, 20, 5], [[20, 10, 5], [20, 20, 10], [10, 10, 5]],
          stem=nm + " has 3 coins. Together they make %s. Which coins does " + he + " have?")
    assert total(["C100", "C50", "C50"]) == 200
    same_as(["C100", "C50", "C50"], "one $2 coin", ["one $1 coin", "one 50c coin", "three $1 coins"])
    which(150, [100, 50], [[100, 20, 20], [50, 50], [100, 20, 20, 5]])
    which_fewest(90, [[50, 20, 10, 10], [20, 20, 20, 20, 10], [50, 10, 10, 10, 10]])
    how_few(85, [3, 5, 2], "5 coins (20c, 20c, 20c, 20c, 5c) works, but it is not the fewest.")
    nm, he, his = P.next()
    which(100, [50, 20, 20, 10], [[50, 20, 20, 5], [20, 20, 20, 20], [50, 20, 10, 10]],
          stem=nm + " has 4 coins. Together they make %s. Which coins does " + he + " have?")
    which_not(200, [100, 50, 20, 20], [[100, 100], [100, 50, 50], [200]])
    which(2000, [1000, 500, 500], [[1000, 500], [500, 500, 500], [1000, 1000, 500]], stem="Which notes make %s?")
    how_few(350, [2, 4, 7], "There is no $3 coin, so 2 coins is not possible. 7 coins would be seven 50c coins.")
    which(225, [200, 20, 5], [[200, 20, 20, 5], [100, 100, 20], [100, 20, 5]])
    which_fewest(470, [[200, 100, 100, 50, 20], [200, 200, 20, 20, 20, 10], [100, 100, 100, 100, 50, 20]])
    which(1000, [500, 200, 200, 100], [[500, 200, 200], [500, 100, 100, 100], [500, 200, 100]],
          stem="Which make the same amount as a %s note?")
    nm, he, his = P.next()
    which(170, [100, 50, 20], [[100, 50, 10], [50, 50, 20], [200, 50, 20]],
          stem=nm + " has 3 coins. Together they make %s. Which coins does " + he + " have?")
    which_not(500, [200, 200, 50, 20, 20], [[200, 200, 100], [200, 100, 100, 100], [200, 200, 50, 50]])
    assert len(its) == 20
    return {"title": "Make the same amount", "items": its}


# ============================================================ set 4: add amounts and give change
CANTEEN = [("ice block", 120), ("fruit cup", 150), ("juice", 180), ("muffin", 250), ("sushi roll", 350)]


def set_change(P, rnd):
    its = []

    def add(nums, q):
        T = sum(nums)
        cands = [noexch_add(nums), forgot_dollar_add(nums)]
        if all(n < 100 for n in nums) and T >= 100:
            cands.append(T * 10)                       # 115c written as $11.50
        if any(n < 100 for n in nums) and any(n >= 100 for n in nums):
            cands.insert(0, sum(n * 100 if n < 100 else n for n in nums))   # 80c read as $80
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        cands += [T - 10, T + 10, T + 100]
        its.append(mcq(q, T, cands, add_e(nums)))

    add([45, 30], "45c + 30c = ?")
    add([60, 55], "60c + 55c = ?")
    price = dict(CANTEEN)
    nm, he, his = P.next()
    add([price["fruit cup"], price["juice"]],
        fig(price_svg(CANTEEN, "school canteen")) + "At the school canteen, %s buys a fruit cup and a juice. "
        "How much does %s spend?" % (nm, he))
    nm, he, his = P.next()
    add([price["ice block"], price["muffin"], price["juice"]],
        fig(price_svg(CANTEEN, "school canteen")) + "At the school canteen, %s buys an ice block, a muffin and a juice. "
        "How much does %s spend?" % (nm, he))
    add([235, 80], "$2.35 + 80c = ?")

    jobs = [(100, 35, "a sticker", True), (100, 70, "a pencil", False), (100, 45, "an eraser", False),
            (200, 125, "a ruler", True), (200, 80, "a bookmark", False),
            (500, 340, "a notebook", True), (500, 275, "a skipping rope", False), (500, 415, "a pack of footy cards", False),
            (1000, 635, "a book", True), (1000, 780, "a jigsaw puzzle", False),
            (2000, 1345, "a netball", True), (2000, 1690, "a lunchbox", False)]
    for paid, pr, thing, line in jobs:
        nm, he, his = P.next()
        money = ("a %s coin" if paid <= 200 else "a %s note") % whole(paid)
        r = paid - pr
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, nat(pr), cap(he), money, he)
        if line:
            q = fig(change_line(pr, paid, show=False)) + q + " Count on along the number line."
        e = count_up(pr, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (nat(r), nat(pr), nat(r), L(paid))
        its.append(mcq(q, r, change_cands(paid, pr), e))

    rule = ("There are no 1c or 2c coins, so a cash total is rounded to the nearest 5c. "
            "Ends in 1 or 2: round down to 0. Ends in 3 or 4: up to 5. Ends in 6 or 7: down to 5. Ends in 8 or 9: up to the next 10. ")
    for amt, cands in [(498, [495, 498, 490]), (342, [345, 342, 350]), (673, [670, 673, 680])]:
        nm, he, his = P.next()
        rr = round5(amt)
        q = ("At the shop, %s’s total is %s. %s pays with cash. Cash totals are rounded to the nearest 5c. "
             "How much does %s pay?" % (nm, nat(amt), cap(he), he))
        e = rule + "%s ends in %d, so %s pays <b>%s</b>." % (nat(amt), amt % 10, he, nat(rr))
        its.append(mcq(q, rr, cands, e))
    assert len(its) == 20
    return {"title": "Add amounts and give change", "items": its}


# ============================================================ set 5: word problems
BOOKFAIR = [("book", 1200), ("poster", 450), ("pen", 250), ("bookmark", 150)]


def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    add("At the school canteen, a fruit cup costs $1.50. %s pays with a $2 coin. How much change does %s get?" % (nm, he),
        50, [150, 350, 60],
        count_up(150, 200) + " The change is <b>50c</b>. $1.50 is the cost, not the change. $3.50 adds the amounts.")
    nm, he, his = P.next()
    assert 2 * 300 + 200 == 800
    add("At the sausage sizzle, a sausage in bread costs $3 and a drink costs $2. %s buys 2 sausages and 1 drink. "
        "How much does %s pay?" % (nm, he), 800, [500, 1000, 600],
        "2 sausages: $3 + $3 = $6. Add the drink: $6 + $2 = <b>$8.00</b>. $5 is only 1 sausage and 1 drink.")
    nm, he, his = P.next()
    add("%s gets $5 pocket money each week. %s saves it for 3 weeks. How much has %s saved?" % (nm, cap(he), he),
        1500, [800, 1000, 2000],
        "$5 + $5 + $5 = <b>$15.00</b>. $8 comes from adding 5 + 3. $10 is only 2 weeks.")
    nm, he, his = P.next()
    assert 150 + 250 == 400
    add("At the book fair, %s buys a bookmark for $1.50 and a pen for $2.50. How much does %s spend?" % (nm, he),
        400, [300, 100, 450],
        add_e([150, 250]) + " $3.00 forgets to regroup the 100c as $1. $1.00 is the difference, not the total.")
    nm, he, his = P.next()
    assert 350 + 180 == 530
    add("%s has $5. %s wants a sushi roll for $3.50 and a juice for $1.80. Does %s have enough?" % (nm, cap(he), he),
        "No, %s needs 30c more." % he, ["Yes, with 30c left.", "Yes, with 70c left.", "No, %s needs $1.30 more." % he],
        "Cost: $3.50 + $1.80 = $5.30 (50c + 80c = 130c = $1.30, and $3 + $1 + $1.30 = $5.30). "
        "$5.30 is more than $5, so <b>no</b>. $5 + 30c = $5.30, so %s needs <b>30c</b> more." % he)
    assert 10 * 300 == 3000
    add("Year 3 sell sausages at a sausage sizzle for $3 each. They sell 10 sausages. How much money do they make?",
        3000, [1300, 300, 30000],
        "10 lots of $3 = <b>$30.00</b>. $13 adds 10 + 3. $3 is only 1 sausage. $300 is far too much for 10 sausages.")
    nm, he, his = P.next()
    assert 1000 - (2 * 300 + 200) == 200
    add("At the sausage sizzle, %s buys 2 sausages for $3 each and a drink for $2. %s pays with a $10 note. "
        "How much change does %s get?" % (nm, cap(he), he), 200, [800, 500, 1800],
        "Cost: $3 + $3 + $2 = $8. Count on from $8 to $10: $2. The change is <b>$2.00</b>. $8 is the cost, not the change.")
    nm, he, his = P.next()
    add("%s has saved $12.50. %s gets $2.50 more pocket money. How much does %s have now?" % (nm, cap(he), he),
        1500, [1400, 1000, 1550],
        add_e([1250, 250]) + " $14.00 forgets to regroup the 100c. $10.00 takes away instead of adding.")
    nm, he, his = P.next()
    add("At the book fair, a book costs $8.50. %s pays with a $10 note. How much change does %s get?" % (nm, he),
        150, change_cands(1000, 850), count_up(850, 1000) + " The change is <b>$1.50</b>. Check: $8.50 + $1.50 = $10.")
    nm, he, his = P.next()
    assert 5 * 120 == 600
    add("An ice block at the canteen costs $1.20. %s buys one every day from Monday to Friday. How much does %s spend?"
        % (nm, he), 600, [520, 480, 1200],
        "5 days: 5 × $1 = $5 and 5 × 20c = 100c = $1. $5 + $1 = <b>$6.00</b>. $5.20 forgets that 5 × 20c is $1. "
        "$4.80 is only 4 days.")
    nm, he, his = P.next()
    assert 4 * 500 == 2000
    add("Tickets for the school disco cost $5 each. %s has a $20 note. How many tickets can %s buy?" % (nm, he),
        "4 tickets", ["5 tickets", "3 tickets", "15 tickets"],
        "Count in fives to $20: $5, $10, $15, $20. That is <b>4 tickets</b>. 15 comes from 20 − 5.")
    nm, he, his = P.next()
    add("%s wants a footy for $25. %s has saved $18.50. How much more money does %s need?" % (nm, cap(he), he),
        650, [750, 700, 4350],
        count_up(1850, 2500) + " %s needs <b>$6.50</b> more. $7.50 takes away the dollars ($25 − $18 = $7) "
        "and then adds the 50c instead of taking it away." % cap(he))
    nm, he, his = P.next()
    assert 1200 + 450 == 1650
    add(fig(price_svg(BOOKFAIR, "book fair")) + "At the book fair, %s buys a book and a poster. %s pays with a $20 note. "
        "How much change does %s get?" % (nm, cap(he), he), 350, [1650] + change_cands(2000, 1650),
        "Cost: $12 + $4.50 = $16.50. " + count_up(1650, 2000) + " The change is <b>$3.50</b>. $16.50 is the cost, not the change.")
    toks = toks_of(("C200", 1), ("C50", 1), ("C20", 2), ("C10", 1))
    assert total(toks) == 300
    nm, he, his = P.next()
    add(fig(money_svg(toks)) + "%s has these coins. %s buys a muffin for $2.50. How much money is left?" % (nm, cap(he)),
        50, [250, 550, 150],
        count_on(toks) + " " + count_up(250, 300) + " <b>50c</b> is left. $2.50 is the cost of the muffin.")
    nm, he, his = P.next()
    assert 4 * 250 == 1000
    add("At the sausage sizzle, sausages cost $2.50 each. %s and %s family buy 4 sausages. How much do they pay?" % (nm, his),
        1000, [850, 800, 1250],
        "4 × $2 = $8 and 4 × 50c = 200c = $2. $8 + $2 = <b>$10.00</b>. $8.50 only adds one 50c. $12.50 would be 5 sausages.")
    nm, he, his = P.next()
    assert 2 * (400 - 150) == 500
    add("%s gets $4 pocket money each week. %s spends $1.50 at the canteen and saves the rest. "
        "How much does %s save in 2 weeks?" % (nm, cap(he), he), 500, [250, 650, 800],
        "Each week: $4 − $1.50 = $2.50 (count on: $1.50 + 50c = $2, $2 + $2 = $4). 2 weeks: $2.50 + $2.50 = <b>$5.00</b>. "
        "$2.50 is only 1 week. $8 forgets the spending.")
    nm, he, his = P.next()
    assert 1500 - (950 + 150) == 400
    add("%s has $15. At the book fair, %s buys a book for $9.50 and a bookmark for $1.50. How much money is left?"
        % (nm, he), 400, [1100, 500, 300],
        "Cost: $9.50 + $1.50 = $11.00 (50c + 50c = $1). Count on from $11 to $15: $4. <b>$4.00</b> is left. "
        "$5.00 forgets to regroup the two 50c as $1.")
    nm, he, his = P.next()
    add("%s’s mum buys fruit at the market. The total is $12.38. She pays with cash, so the total is rounded to the "
        "nearest 5c. How much does she pay?" % nm, 1240, [1235, 1238, 1230],
        "$12.38 ends in 8. 8c rounds up to the next 10c, so she pays <b>$12.40</b>.")
    nm, he, his = P.next()
    assert 3 * 200 + 150 == 750 and 1000 - 750 == 250
    add("At the school fete, %s buys 3 raffle tickets for $2 each and a cupcake for $1.50. %s pays with a $10 note. "
        "How much change does %s get?" % (nm, cap(he), he), 250, [750, 350, 650],
        "Cost: $2 + $2 + $2 + $1.50 = $7.50. " + count_up(750, 1000) + " The change is <b>$2.50</b>. "
        "$6.50 counts only 1 raffle ticket.")
    nm, he, his = P.next()
    assert 500 + 500 + 200 + 3 * 50 == 1350 and 1350 - 1250 == 100
    add("%s has two $5 notes, a $2 coin and three 50c coins. %s wants a book for $12.50. Does %s have enough?"
        % (nm, cap(he), he), "Yes, with $1 left.",
        ["No, %s needs $1 more." % he, "Yes, with $1.50 left.", "No, %s needs 50c more." % he],
        "$5 + $5 + $2 = $12. Three 50c coins = $1.50. $12 + $1.50 = $13.50. $13.50 is more than $12.50, so <b>yes</b>. "
        "$12.50 + $1 = $13.50, so $1 is left.")
    assert len(its) == 20
    return {"title": "Money word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20", "N50", "N100"]
    walk = toks_of(("C200", 1), ("C20", 1), ("C10", 1), ("C5", 1))
    under = ["$2", "$2.20", "$2.30", "$2.35"]
    assert total(walk) == 235
    assert round5(498) == 500 and round5(342) == 340 and round5(673) == 675
    return (
        "<h2>Dollars and cents</h2>"
        "<p>$1 = 100c. In $2.35, the 2 is the dollars and the 35 is the cents. "
        "The cents always have <b>two digits</b> after the point: write $2.50, not $2.5.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=6, label="Australian coins: 5c, 10c, 20c, 50c, $1, $2") +
        "<figcaption>Coins: 5c, 10c, 20c, 50c, $1 and $2. The $2 coin is smaller than the $1 coin, but it is worth more.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, per_row=5, label="Australian notes: $5, $10, $20, $50, $100") +
        "<figcaption>Notes: $5, $10, $20, $50 and $100.</figcaption></figure>"
        + table(["Cents", "Dollars and cents", "Write"], [
            ["100c", "$1 and 0c", "$1.00"],
            ["250c", "$2 and 50c", "$2.50"],
            ["105c", "$1 and 5c", "$1.05"],
            ["235c", "$2 and 35c", "$2.35"],
        ]) +
        "<h2>Count the money, biggest first</h2>"
        "<p>Start with the dollars. Then count on the cents.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=20, under=under, label="counting on: $2, $2.20, $2.30, $2.35") +
        "<figcaption>$2, $2.20, $2.30, $2.35. $2 and 35c = $2.35.</figcaption></figure>"
        + ex("Example", "Add $1.75 + 80c.",
             "Cents: 75c + 80c = 155c = $1.55. Regroup 100c as $1. Dollars: $1 + $1.55 = $2.55.", "$2.55") +
        "<h2>Make the same amount in different ways</h2>"
        "<p>75c can be 50c + 20c + 5c, or 20c + 20c + 20c + 10c + 5c. "
        "For the <b>fewest coins</b>, use the biggest coin you can each time.</p>"
        + "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Jump to the next 10c, then to the next dollar, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(35, 100) +
        "<figcaption>Change from $1 for 35c: 5c + 60c = 65c.</figcaption></figure>"
        + ex("Example", "A kite costs $3.40. Pay with a $5 note. What is the change?",
             "$3.40 + 60c = $4. $4 + $1 = $5. 60c + $1 = $1.60. Check: $3.40 + $1.60 = $5.", "$1.60")
        + "<p>Paying with cash? There are no 1c or 2c coins, so the total is rounded to the nearest 5c. "
        "$4.98 becomes $5.00, $3.42 becomes $3.40 and $6.73 becomes $6.75.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The $1 coin is bigger, so it is worth more", "Read the value: the $2 coin is smaller but worth more"],
            ["4 coins, so 4c", "Count the value of each coin: 50c, 70c, 80c, 85c"],
            ["250c = $25.00", "100c = $1, so 250c = $2.50"],
            ["$2.5", "Cents take two digits: $2.50"],
            ["Change from $5 for $3.40 is $2.60", "Count on: $3.40 + 60c = $4, $4 + $1 = $5. The change is $1.60"],
        ])
    )


FAQ = [
    {"q": "What do Year 3 students learn about money in the Australian Curriculum?",
     "a": "In Year 3 (AC9M3M06), students recognise that 100 cents make $1 and show the same amount in different ways, such as 75c as 50c + 20c + 5c. Classes also count collections of coins and notes and work out change."},
    {"q": "Is the $2 coin bigger than the $1 coin?",
     "a": "No. The $2 coin is smaller than the $1 coin, but it is worth more. The 50c coin is the biggest Australian coin, so size never tells you the value."},
    {"q": "Why are cash prices rounded to 5 cents in Australia?",
     "a": "Australia has no 1c or 2c coins, so a cash total is rounded to the nearest 5c: $4.98 becomes $5.00 and $3.42 becomes $3.40. Card payments are charged the exact amount."},
    {"q": "How do you work out change from $5?",
     "a": "Count on from the price to $5: first to the next 10c, then to the next dollar, then to $5. For $3.40: 60c + $1 = $1.60. Check: $3.40 + $1.60 = $5."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3807)
    P = People(rnd)
    sets = [set_count(P, rnd), set_convert(P, rnd), set_ways(P, rnd), set_change(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [mval(c) for c in it["c"]]
            vv = [v for v in vals if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            for c in it["c"]:
                assert not re.search(r"\$[\d.]+c", c), c
                assert "¢" not in c
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "money", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Dollars and Cents, Making Amounts and Giving Change",
        "seo_title": "Year 3 Money Worksheets: Dollars and Cents, Counting Coins and Change",
        "short_title": "Money",
        "domain": "Measurement",
        "standard_code": "AC9M3M06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise the relationships between dollars and cents and represent money values in different ways",
        "meta_desc": "Free Year 3 maths worksheets on money: count Australian coins and notes, change cents into dollars (250c = $2.50), make the same amount in different ways, give change from $5, $10 and $20 by counting on, and solve canteen and sausage sizzle word problems. 100 questions with an answer key, following the Australian Curriculum and useful for NAPLAN practice.",
        "key_big": "$1 = 100c. So 250c = $2 and 50c = $2.50.",
        "key_sub": "Count money biggest value first (the small $2 coin is worth more than the big $1 coin). To give change, count on from the price: $3.40 to $4 is 60c, $4 to $5 is $1, so the change from $5 is $1.60.",
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
