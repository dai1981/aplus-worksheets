# -*- coding: utf-8 -*-
"""
UK Year 3 Maths: Money (National Curriculum in England, Year 3: Measurement)
  python3 tools/gen_uk_maths_y3_money.py
All amounts are whole numbers of pence (int), so every total, change and typical mistake is exact.
Writing money: under £1 as 45p, from £1 as £2.35 (never £2.35p, never £2.5). Amounts up to about £20.
Coins and notes are simple labelled shapes (no real coin or note artwork).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]

# ------------------------------------------------------------ money facts
ORDER = ["N20", "N10", "N5", "C200", "C100", "C50", "C20", "C10", "C5", "C2", "C1"]   # biggest value first
VAL = {"N20": 2000, "N10": 1000, "N5": 500, "C200": 200, "C100": 100, "C50": 50, "C20": 20,
       "C10": 10, "C5": 5, "C2": 2, "C1": 1}
COPPER = ("#d9915a", "#8a5428")
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius, (fill, edge), label size
COIN = {"C1": (18, COPPER, 14), "C2": (22, COPPER, 15), "C5": (17, SILVER, 14), "C10": (21, SILVER, 14),
        "C20": (20, SILVER, 14), "C50": (23, SILVER, 15), "C100": (21, GOLD, 15), "C200": (24, GOLD, 16)}
NOTE = {"N5": ("#bfe6de", "#1f7a6d"), "N10": ("#f6d2a8", "#a35a12"), "N20": ("#dccbef", "#5b3a8a")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "£%d" % (v // 100) if v >= 100 else "%dp" % v


def nat(p):
    """45 -> '45p', 345 -> '£3.45' (pence under £1, pounds with two digits after the point from £1)."""
    assert p > 0, p
    return "%dp" % p if p < 100 else "£{:,}.{:02d}".format(p // 100, p % 100)


def gbp(p):
    """always in pounds: 75 -> '£0.75'"""
    return "£{:,}.{:02d}".format(p // 100, p % 100)


def pen(p):
    return "{:,}p".format(p)


def whole(p):
    """rounded amounts: 300 -> '£3'"""
    assert p % 100 == 0
    return "£%d" % (p // 100)


def mval(s):
    """value in pence of a money text, or None: '£2.5' -> 250, '£3' -> 300, '1,000p' -> 1000"""
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^£([\d,]+)(?:\.(\d{1,2}))?$", s)
    if m:
        f = m.group(2) or "0"
        return int(m.group(1).replace(",", "")) * 100 + int(f.ljust(2, "0"))
    m = re.match(r"^([\d,]+)p$", s)
    if m:
        return int(m.group(1).replace(",", ""))
    return None


def total(toks):
    return sum(VAL[t] for t in toks)


def toks_of(*pairs):
    """toks_of(('C20', 2), ('C5', 1)) -> sorted biggest first"""
    out = []
    for t, n in pairs:
        out += [t] * n
    return srt(out)


def srt(toks):
    return sorted(toks, key=ORDER.index)


def counts(toks):
    return [(t, toks.count(t)) for t in ORDER if t in toks]


def name_of(t, n=1):
    w = "note" if t.startswith("N") else "coin"
    return "%s %s" % (lab(VAL[t]), w if n == 1 else w + "s")


def group(toks):
    parts = ["%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks)]
    return ", ".join(parts)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ explanations
def count_on(toks):
    """'Count the pounds: £10, £15, £16. Count on the pence: 20p, 40p, 45p. £16 and 45p is £16.45.'"""
    pounds = [t for t in srt(toks) if VAL[t] >= 100]
    pence = [t for t in srt(toks) if VAL[t] < 100]
    out, s = [], 0
    if pounds:
        run = []
        for t in pounds:
            s += VAL[t]
            run.append("£%d" % (s // 100))
        out.append("Count the pounds: %s." % ", ".join(run))
    P = 0
    if pence:
        run = []
        for t in pence:
            P += VAL[t]
            run.append("%dp" % P)
        out.append(("Count on the pence: %s." if pounds else "Start with the biggest coin: %s.") % ", ".join(run))
    T = total(toks)
    if pounds and pence:
        if P >= 100:
            out.append("%dp = %s. £%d + %s = <b>%s</b>." % (P, gbp(P), s // 100, gbp(P), nat(T)))
        else:
            out.append("£%d and %dp is <b>%s</b>." % (s // 100, P, nat(T)))
    elif pounds:
        out.append("That is <b>%s</b>." % nat(T))
    else:
        out.append("That is <b>%s</b>." % nat(T) if P < 100 else "%dp = <b>%s</b>." % (P, nat(T)))
    return " ".join(out)




def add_e(nums):
    """partition into pounds and pence"""
    T = sum(nums)
    pd = [n // 100 for n in nums if n >= 100]
    pc = [n % 100 for n in nums if n % 100]
    Ps, ps = sum(pd), sum(pc)
    out = []
    if len(pd) > 1:
        out.append("Add the pounds: %s = £%d." % (" + ".join("£%d" % x for x in pd), Ps))
    elif pd:
        out.append("Pounds: £%d." % Ps)
    if len(pc) > 1:
        if ps >= 100:
            out.append("Add the pence: %s = %dp = %s. Exchange 100p for £1." % (" + ".join("%dp" % x for x in pc), ps, gbp(ps)))
        else:
            out.append("Add the pence: %s = %dp." % (" + ".join("%dp" % x for x in pc), ps))
    elif pc:
        out.append("Pence: %dp." % ps)
    if Ps and ps:
        out.append("£%d + %s = <b>%s</b>." % (Ps, nat(ps), nat(T)))
    else:
        out.append("Total: <b>%s</b>." % nat(T))
    assert Ps * 100 + ps == T
    return " ".join(out)



# ------------------------------------------------------------ typical mistakes (all computed, in pence)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


def m_pound_as_p(toks):
    """counted £ coins and notes as pence (£2 -> 2p)"""
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


def drop_zero(p):
    """£3.08 written as £3.80 (the 0 placeholder lost): only when pence < 10"""
    return (p // 100) * 100 + (p % 100) * 10 if 0 < p % 100 < 10 else None


def digs(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def from_digs(d):
    return sum(x * 10 ** i for i, x in enumerate(d))


def noexch_add(nums):
    """column addition without exchanging: each column mod 10"""
    k = max(len(str(n)) for n in nums)
    return from_digs([sum(digs(n, k)[i] for n in nums) % 10 for i in range(k)])


def forgot_pound_add(nums):
    """made 100p or more in the pence but did not exchange it for £1"""
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


def draw_tok(t, cx, cy):
    """one coin (circle with its value) or one note (rectangle with its value), centred at cx, cy"""
    if t.startswith("N"):
        fill, edge = NOTE[t]
        x, y = cx - NOTE_W / 2, cy - NOTE_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, NOTE_W, NOTE_H, fill, edge, x + 5, y + 5, NOTE_W - 10, NOTE_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r, (fill, edge), fs = COIN[t]
    inner = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 6, SILVER[0], edge)
             if t == "C200" else
             "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 4, edge))
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
            + inner + text(cx, cy + fs * 0.36, lab(VAL[t]), fs))


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


def coin_svg(t):
    w, h = tok_size(t)
    return svg_wrap(w + 6, h + 6, draw_tok(t, (w + 6) / 2, (h + 6) / 2), "one %s" % name_of(t))



def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def frac(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


def shuffled(toks, rnd):
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


# ------------------------------------------------------------ Year 3 helpers
def L(p):
    """a point on a number line or in an explanation: 40p, £1, £6.40"""
    return nat(p) if p % 100 else whole(p)


def J(j):
    """a jump: 5p, 60p, £3, £1.50"""
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


def count_up3(price, paid):
    """'Count on from 35p: 35p + 5p = 40p, 40p + 60p = £1. 5p + 60p = 65p.'"""
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (L(a), J(b - a), L(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(J(j) for j in jumps), nat(ch))
    return "Count on from %s to %s: %s.%s" % (L(price), L(paid), ", ".join(steps), tail)


def change_cands3(paid, price):
    """real change mistakes, in order of how often they happen"""
    r = paid - price
    c = []
    if price % 10:
        c.append(r + 10)            # 35p + 75p "makes 100": 3 + 7 = 10 and 5 + 5 = 10, but that is 110
    if paid > 100 and price % 100:
        c.append(r + 100)           # took away the pounds, then forgot the pound used to pay the pence
    c += [price, small_from_big(paid, price), r - 10, r + 5, r - 5, r + 1]
    return [x for x in c if 0 < x < paid]


def change_line3(price, paid, show=True):
    """empty number line (not to scale) for counting on; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [120, 140, 160][:len(pts) - 1]
    x0, y0 = 40, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 40
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
    """a row of price tags: [('toast', 35), ...]"""
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


# ============================================================ set 1: count the coins
def set_count(P, rnd):
    its = []
    groups = [
        [("C10", 5)], [("C5", 4)], [("C2", 4), ("C1", 1)], [("C20", 3)], [("C50", 1), ("C20", 1), ("C5", 1)],
        [("C20", 2), ("C10", 1), ("C2", 1), ("C1", 1)], [("C50", 1), ("C10", 2), ("C5", 1), ("C2", 1)],
        [("C100", 3)], [("C200", 1), ("C100", 1)], [("C100", 1), ("C50", 1)], [("C200", 1), ("C50", 1), ("C20", 1)],
        [("C100", 1), ("C20", 1), ("C10", 1), ("C5", 1)], [("C200", 1), ("C100", 1), ("C10", 1), ("C5", 1)],
        [("C200", 1), ("C2", 2), ("C1", 1)], [("C100", 2), ("C50", 1), ("C20", 1), ("C2", 1)],
        [("C200", 2), ("C50", 1), ("C5", 1)],
        [("N5", 1), ("C100", 1), ("C50", 1)], [("N5", 1), ("C200", 1), ("C20", 1), ("C5", 1)],
        [("N10", 1), ("C200", 1), ("C10", 1)], [("N10", 1), ("N5", 1), ("C100", 1), ("C50", 1), ("C2", 1)],
    ]
    mixed = {6, 11, 14, 17, 19}
    stems = ["How much money is shown?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s pencil case. How much is it?", "What is the total?",
             "%s puts this money in a money box. How much is in the box?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert len(toks) <= 7 and T <= 2000
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
        e = ("Put the money in order, biggest value first. " if i in mixed and T >= 100 else "") + count_on(toks)
        if len(set(toks)) == 1:
            t, n = toks[0], len(toks)
            if VAL[t] >= 100:
                e = "Each coin is £1. Count in pounds: %s. That is <b>%s</b>." % (
                    ", ".join("£%d" % k for k in range(1, n + 1)), nat(T))
            else:
                e = "Each coin is %s. Count in %ds: %s. That is <b>%s</b>." % (
                    lab(VAL[t]), VAL[t], ", ".join("%dp" % (VAL[t] * k) for k in range(1, n + 1)), nat(T))
        e += " Count the value of each coin, not the number of coins." if i < 3 else ""
        cands = [m_count(toks), drop_zero(T) if T >= 100 else None, m_pound_as_p(toks), m_same_step(toks), m_skip(toks, -1),
                 m_twice(toks, 0), m_skip(toks, 0), m_twice(toks, -1)]
        if i >= 7:
            cands = [drop_zero(T), m_pound_as_p(toks)] + cands[3:][i % 3:] + cands[3:][:i % 3] + [m_count(toks)]
        its.append(mcq(q, T, cands, e))
    assert len(its) == 20
    return {"title": "Count the coins", "items": its}


# ============================================================ set 2: pounds and pence
def set_convert(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=nat):
        its.append(mcq(q, right, wrong, e, fmt))

    s("How many pence make £1?", "100p", ["10p", "1,000p", "50p"],
      "£1 = <b>100p</b>. That is why the pence always have two digits after the point.")
    s("£3 = ? p", 300, [30, 3, 3000], "£1 = 100p, so £3 = 100p + 100p + 100p = <b>300p</b>.", pen)
    s("£10 = ? p", 1000, [100, 10, 10000], "£1 = 100p, so £10 = 10 × 100p = <b>1,000p</b>.", pen)
    assert 10 * 10 == 100 and 4 * 50 == 200
    s("How many 10p coins make £1?", "10", ["100", "1", "5"],
      "Count in 10s up to 100p: 10p, 20p, 30p … 100p. That is <b>10</b> coins.")
    s("How many 50p coins make £2?", "4", ["2", "3", "50"],
      "Two 50p coins make £1. So £2 needs 2 + 2 = <b>4</b> coins. 2 coins only make £1.")
    s("150p = £1 and ?", "50p", ["150p", "5p", "15p"],
      "150p = 100p + 50p. 100p is £1, so 150p = £1 and <b>50p</b>.")
    s("Write 150p in pounds.", "£1.50", ["£150", "£15.00", "£1.05"],
      "150p = 100p + 50p = £1 and 50p. Write <b>£1.50</b>. £150 would be 15,000p.")
    s("Write 275p in pounds.", "£2.75", ["£275", "£27.50", "£0.75"],
      "275p = 200p + 75p = £2 and 75p. Write <b>£2.75</b>. Do not forget the £2.")
    s("Write 309p in pounds.", "£3.09", ["£3.90", "£30.90", "£309"],
      "309p = 300p + 9p = £3 and 9p. The pence need two digits, so 9p is .09: <b>£3.09</b>. £3.90 would be 390p.")
    s("Write 640p in pounds.", "£6.40", ["£64.00", "£6.04", "£640"],
      "640p = 600p + 40p = £6 and 40p: <b>£6.40</b>. £6.04 would be 604p.")
    s("Write £1.05 in pence.", 105, [15, 150, 1005],
      "£1.05 is £1 and 5p. £1 = 100p, so 100p + 5p = <b>105p</b>. It is not 15p: the 1 is a whole pound.", pen)
    s("Write £2.50 in pence.", 250, [25, 205, 2500],
      "£2.50 is £2 and 50p. 200p + 50p = <b>250p</b>.", pen)
    s("Write £4.20 in pence.", 420, [42, 402, 4200],
      "£4.20 is £4 and 20p. 400p + 20p = <b>420p</b>. 42p would be less than £1.", pen)
    s("Write £8.99 in pence.", 899, [107, 8990, 99],
      "£8.99 is £8 and 99p. 800p + 99p = <b>899p</b>. Adding 8 + 99 = 107 forgets that £1 is 100p.", pen)
    s("How do you write 2 pounds and 35 pence?", "£2.35", ["£235", "37p", "£23.50"],
      "Write £, the pounds, a point, then two digits for the pence: <b>£2.35</b>. Do not add the 2 and the 35.")
    s("How do you write 3 pounds and 7 pence?", "£3.07", ["£3.70", "£37", "10p"],
      "7 pence needs two digits, so it is 07: <b>£3.07</b>. £3.70 would be 3 pounds and 70 pence.")
    s("How do you write 5 pounds and 50 pence?", "£5.50", ["£5.05", "£550", "55p"],
      "50 pence is .50, so it is <b>£5.50</b> (or 550p). £5.05 would be 5 pounds and 5 pence.")
    s("Which is more: £1.50 or 105p?", "£1.50", ["105p", "They are the same.", "You cannot tell."],
      "Write both in pence: £1.50 = 150p. 150p is more than 105p, so <b>£1.50</b> is more.")
    s("Which is more: 99p or £1.09?", "£1.09", ["99p", "They are the same.", "You cannot tell."],
      "£1.09 = 109p. 109p is more than 99p, so <b>£1.09</b> is more. 99p is less than £1.")
    amts = ["£1.20", "102p", "£2.10"]
    order = sorted(amts, key=mval)
    right = ", ".join(order)
    wl = ["£1.20, 102p, £2.10", "£2.10, £1.20, 102p", "102p, £2.10, £1.20"]
    for w in wl:
        assert w != right and sorted(w.split(", ")) == sorted(amts)
    s("Put these in order, smallest first: £1.20, 102p, £2.10.", right, wl,
      "Write them in pence: £1.20 = 120p, 102p, £2.10 = 210p. Smallest first: <b>%s</b>." % right)
    assert len(its) == 20
    return {"title": "Pounds and pence", "items": its}


# ============================================================ set 3: add amounts
TUCK = [("toast", 35), ("apple", 30), ("juice", 45), ("flapjack", 60), ("crisps", 55)]
FAIR = [("cake", 120), ("book", 250), ("toy car", 175), ("badge", 80), ("plant", 340)]


def set_add(P, rnd):
    its = []
    plain = [[40, 30], [25, 50], [35, 48], [65, 70], [75, 48], [120, 250], [145, 230], [175, 80], [250, 250],
             [365, 125], [480, 260]]
    tuck = [("toast", "juice"), ("flapjack", "crisps"), ("apple", "toast", "juice"), ("flapjack", "juice", "apple")]
    fair = [("book", "badge"), ("cake", "toy car"), ("toy car", "plant"), ("cake", "book", "badge"),
            ("plant", "toy car", "cake")]
    jobs = ([("p", x) for x in plain[:3]] + [("t", tuck[0])] + [("p", plain[3])] + [("t", tuck[1]), ("t", tuck[2])]
            + [("p", x) for x in plain[4:7]] + [("t", tuck[3])] + [("f", fair[0])] + [("p", x) for x in plain[7:9]]
            + [("f", fair[1])] + [("p", x) for x in plain[9:]] + [("f", x) for x in fair[2:]])
    assert len(jobs) == 20
    for kind, x in jobs:
        if kind == "p":
            nums = x
            q = "%s = ?" % " + ".join(nat(n) for n in nums)
        else:
            board, title = (TUCK, "tuck shop") if kind == "t" else (FAIR, "school fair")
            price = dict(board)
            nums = [price[n] for n in x]
            nm, he, his = P.next()
            what = ", ".join(x[:-1]) + " and " + x[-1]
            what = what.replace("toast", "some toast").replace("juice", "a juice").replace("apple", "an apple") \
                .replace("flapjack", "a flapjack").replace("crisps", "a bag of crisps").replace("cake", "a cake") \
                .replace("book", "a book").replace("toy car", "a toy car").replace("badge", "a badge").replace("plant", "a plant")
            q = fig(price_svg(board, title)) + "At the %s, %s buys %s. How much does %s spend?" % (title, nm, what, he)
        T = sum(nums)
        cands = [noexch_add(nums), forgot_pound_add(nums)]
        if all(n < 100 for n in nums) and T >= 100:
            cands.append(T * 10)                       # 115p written as £11.50
        if any(n < 100 for n in nums) and any(n >= 100 for n in nums):
            cands.insert(0, sum(n * 100 if n < 100 else n for n in nums))   # 80p read as £80
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        cands += [T - 10, T + 10, T + 100]
        its.append(mcq(q, T, cands, add_e(nums)))
    assert len(its) == 20
    return {"title": "Add amounts", "items": its}


# ============================================================ set 4: give change
THINGS = {100: ["a pencil", "a rubber", "a sticker", "a lolly", "a bookmark", "a pen"],
          200: ["a ruler", "a notebook", "a bag of sweets", "a comic"],
          500: ["a sticker book", "a ball", "a toy car", "a kite", "a puzzle"],
          1000: ["a lunchbox", "a book", "a board game", "a pencil case", "a T-shirt"]}


def set_change(P, rnd):
    its = []
    jobs = {100: [35, 60, 45, 72, 18, 85], 200: [150, 125, 80, 165], 500: [340, 275, 410, 385, 199],
            1000: [635, 850, 480, 725, 945]}
    line_q = {(100, 35), (100, 72), (200, 125), (500, 275), (1000, 635), (1000, 480)}
    k = 0
    for paid in (100, 200, 500, 1000):
        for j, price in enumerate(jobs[paid]):
            nm, he, his = P.next()
            thing = THINGS[paid][j]
            money = ("a %s coin" if paid <= 200 else "a %s note") % whole(paid)
            r = paid - price
            q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (
                nm, thing, nat(price), cap(he), money, he)
            if (paid, price) in line_q:
                q = fig(change_line3(price, paid, show=False)) + q + " Count on along the number line."
            e = count_up3(price, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (
                nat(r), nat(price), nat(r), L(paid))
            its.append(mcq(q, r, change_cands3(paid, price), e))
            k += 1
    assert k == 20
    return {"title": "Give change", "items": its}


# ============================================================ set 5: word problems
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    add("The bus fare is 85p. %s pays with a £1 coin. How much change does %s get?" % (nm, he),
        15, [25, 85, 5], count_up3(85, 100) + " The change is <b>15p</b>. 25p is wrong: 85p + 25p = 110p.")
    nm, he, his = P.next()
    assert 100 - (35 + 40) == 25
    add("At the tuck shop, %s buys toast for 35p and milk for 40p. %s pays with a £1 coin. How much change does %s get?"
        % (nm, cap(he), he), 25, [75, 35, 15],
        "Cost: 35p + 40p = 75p. Change: 75p + 25p = 100p, so the change is <b>25p</b>. 75p is the cost, not the change.")
    nm, he, his = P.next()
    add("A child bus ticket costs 90p. %s takes the bus to school and back home. How much does %s pay?" % (nm, he),
        180, [90, 1800, 170],
        "Two tickets: 90p + 90p = 180p. 180p = 100p + 80p = <b>£1.80</b>. 90p is only one way.")
    nm, he, his = P.next()
    add("Raffle tickets at the school fair cost 50p each. %s buys 3 tickets. How much does %s pay?" % (nm, he),
        150, [53, 1500, 100],
        "50p + 50p + 50p = 150p = <b>£1.50</b>. 53p adds 50 + 3. £15.00 would be 1,500p.")
    nm, he, his = P.next()
    assert 5 * 20 == 100
    add("Badges cost 20p each. How many badges can %s buy with £1?" % nm,
        "5 badges", ["4 badges", "10 badges", "20 badges"],
        "£1 = 100p. Count in 20s: 20p, 40p, 60p, 80p, 100p. That is <b>5 badges</b>.")
    nm, he, his = P.next()
    assert 10 * 30 == 300
    add("Year 3 sell cakes at the school fair for 30p each. They sell 10 cakes. How much money do they make?",
        300, [40, 3000, 270],
        "10 lots of 30p = 300p. 300p = <b>£3.00</b>. 40p adds 30 + 10. 270p would be only 9 cakes.")
    nm, he, his = P.next()
    add("The bus fare is £1.40. %s pays with a £2 coin. How much change does %s get?" % (nm, he),
        60, [160, 40, 340], count_up3(140, 200) + " The change is <b>60p</b>. 40p is the pence in the price, not the change.")
    nm, he, his = P.next()
    add("%s gets £2 pocket money every week. %s saves it for 4 weeks. How much has %s saved?" % (nm, cap(he), he),
        800, [600, 200, 1000],
        "£2 + £2 + £2 + £2 = <b>£8.00</b>. £6 comes from adding 2 + 4.")
    nm, he, his = P.next()
    add("%s has £3. %s wants a book for £4.50. How much more money does %s need?" % (nm, cap(he), he),
        150, [750, 50, 100], count_up3(300, 450) + " %s needs <b>£1.50</b> more. £7.50 adds the amounts." % cap(he))
    nm, he, his = P.next()
    add("%s has £5 of pocket money. %s buys a comic for £3.50. How much money is left?" % (nm, cap(he)),
        150, [250, 850, 350], count_up3(350, 500) + " <b>£1.50</b> is left. £2.50 takes away the pounds (£5 − £3 = £2) "
        "and then adds the 50p instead of taking it away.")
    a, b = 420, 350
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    add("%s has £4.20. %s has £3.50. How much more money does %s have?" % (nm, nm2, nm),
        a - b, [a + b, small_from_big(a, b), a - b + 100],
        count_up3(b, a) + " %s has <b>70p</b> more." % nm)
    nm, he, his = P.next()
    assert 60 + 45 == 105 and 200 - 105 == 95
    add("At the school fair, %s buys a cake for 60p and a drink for 45p. %s pays with a £2 coin. How much change does %s get?"
        % (nm, cap(he), he), 95, [105, 185, 85],
        "Cost: 60p + 45p = 105p = £1.05. " + count_up3(105, 200) + " The change is <b>95p</b>. "
        "£1.85 comes from reading £1.05 as 15p.")
    nm, he, his = P.next()
    assert 2 * 75 == 150
    add("A fruit pot at the tuck shop costs 75p. %s buys one on Monday and one on Tuesday. %s pays with a £2 coin. "
        "How much change does %s get?" % (nm, cap(he), he), 50, [150, 25, 125],
        "Cost: 75p + 75p = 150p = £1.50. " + count_up3(150, 200) + " The change is <b>50p</b>. "
        "25p is the change for only one fruit pot.")
    nm, he, his = P.next()
    add("At the school fair, %s buys an ice cream for £1.25. %s pays with a £5 note. How much change does %s get?"
        % (nm, cap(he), he), 375, change_cands3(500, 125), count_up3(125, 500) + " The change is <b>£3.75</b>.")
    nm, he, his = P.next()
    assert 2 * 150 - 80 == 220
    add("%s gets £1.50 pocket money each week. After 2 weeks, %s spends 80p on sweets. How much money is left?"
        % (nm, he), 220, [300, 70, 380],
        "Saved: £1.50 + £1.50 = £3.00. " + count_up3(80, 300) + " <b>£2.20</b> is left. "
        "70p only uses one week of pocket money.")
    nm, he, his = P.next()
    assert 250 + 120 == 370
    add("A bus ticket costs £2.50 for an adult and £1.20 for a child. %s and %s mum pay with a £5 note. "
        "How much change do they get?" % (nm, his), 130, [370, 230, 120],
        "Cost: £2.50 + £1.20 = £3.70. " + count_up3(370, 500) + " The change is <b>£1.30</b>. £3.70 is the cost, not the change.")
    nm, he, his = P.next()
    add("%s wants a football for £9. %s has saved £6.50. How much more does %s need?" % (nm, cap(he), he),
        250, [1550, 350, 300], count_up3(650, 900) + " %s needs <b>£2.50</b> more. £3.50 takes away the pounds "
        "(£9 − £6 = £3) and then adds the 50p." % cap(he))
    nm, he, his = P.next()
    assert 4 * 50 + 30 == 230
    add("At the book stall, books cost 50p each and bookmarks cost 30p. %s buys 4 books and 1 bookmark. How much does %s spend?"
        % (nm, he), 230, [80, 200, 180],
        "4 books: 50p + 50p + 50p + 50p = 200p = £2. Add the bookmark: £2 + 30p = <b>£2.30</b>. "
        "80p is only one book and the bookmark.")
    nm, he, his = P.next()
    assert 275 + 180 == 455 and 500 - 455 == 45
    add("%s has £5. %s wants a book for £2.75 and a pen for £1.80. Does %s have enough?" % (nm, cap(he), he),
        "Yes, with 45p left.", ["No, 45p more is needed.", "Yes, with £1.45 left.", "Yes, with 55p left."],
        "Cost: £2.75 + £1.80 = £4.55 (75p + 80p = 155p = £1.55, and £2 + £1 + £1.55 = £4.55). £4.55 is less than £5, so <b>yes</b>. "
        + count_up3(455, 500) + " 45p is left.")
    nm, he, his = P.next()
    spent = 450 + 225
    add("%s has £10. %s buys a model for £4.50 and a magazine for £2.25. How much money is left?" % (nm, cap(he)),
        1000 - spent, [spent] + change_cands3(1000, spent),
        "Spent: £4.50 + £2.25 = £6.75. " + count_up3(spent, 1000) + " <b>£3.25</b> is left.")
    assert len(its) == 20
    return {"title": "Money word problems", "items": its}


# ============================================================ lesson
def body_html():
    all_coins = ["C1", "C2", "C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20"]
    walk = toks_of(("C200", 1), ("C20", 1), ("C10", 1), ("C5", 1))
    under = ["£2", "£2.20", "£2.30", "£2.35"]
    assert total(walk) == 235
    return (
        "<h2>Pounds and pence</h2>"
        "<p>£1 = 100p. In £2.35, the 2 is the pounds and the 35 is the pence. "
        "The pence always have <b>two digits</b> after the point.</p>"
        "<figure class='sn-fig'>" + money_svg(all_coins, per_row=8, label="UK coins: 1p, 2p, 5p, 10p, 20p, 50p, £1, £2") +
        "<figcaption>Coins: 1p, 2p, 5p, 10p, 20p, 50p, £1 and £2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, label="UK notes: £5, £10, £20") +
        "<figcaption>Notes: £5, £10 and £20.</figcaption></figure>"
        + table(["Pence", "Pounds and pence", "Write"], [
            ["100p", "£1 and 0p", "£1.00"],
            ["150p", "£1 and 50p", "£1.50"],
            ["105p", "£1 and 5p", "£1.05"],
            ["235p", "£2 and 35p", "£2.35"],
        ]) +
        "<h2>Count the coins, biggest first</h2>"
        "<p>Start with the pounds. Then count on the pence.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=20, under=under, label="counting on: £2, £2.20, £2.30, £2.35") +
        "<figcaption>£2, £2.20, £2.30, £2.35. £2 and 35p = £2.35.</figcaption></figure>"
        + ex("Example", "Add £1.75 + 80p.",
             "Pence: 75p + 80p = 155p = £1.55. Pounds: £1 + £1.55 = £2.55.", "£2.55")
        + "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Jump to the next 10p, then to the next pound, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line3(35, 100) +
        "<figcaption>Change from £1 for 35p: 5p + 60p = 65p.</figcaption></figure>"
        + ex("Example", "A kite costs £3.40. Pay with a £5 note. What is the change?",
             "£3.40 + 60p = £4. £4 + £1 = £5. 60p + £1 = £1.60. Check: £3.40 + £1.60 = £5.", "£1.60")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 coins, so 4p", "Count the value of each coin: 20p, 40p, 50p, 52p"],
            ["150p = £150 or £15.0", "100p = £1, so 150p = £1.50"],
            ["£1.05 = 15p", "£1 = 100p, so £1.05 = 105p"],
            ["Change from £1 for 35p is 75p", "Count on: 35p + 5p = 40p, 40p + 60p = £1. The change is 65p"],
        ])
    )


FAQ = [
    {"q": "What should a Year 3 child know about money?",
     "a": "In the National Curriculum, Year 3 pupils add and subtract amounts of money and give change, using both £ and p in real-life situations, such as the change from £1 or £5."},
    {"q": "How many pence are in £1?",
     "a": "There are 100 pence in £1. So 150p is £1 and 50p, written £1.50, and £1.05 is 105p."},
    {"q": "How do you work out change from £1?",
     "a": "Count on from the price to £1: first to the next 10p, then to £1. For 35p: 5p + 60p = 65p change. Check: 35p + 65p = 100p."},
    {"q": "Why do we write £1.05 and not £1.5?",
     "a": "The pence always take two digits after the point, so 5 pence is .05. £1.5 would be read as £1.50, which is 150p."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(3310)
    P = People(rnd)
    sets = [set_count(P, rnd), set_convert(P, rnd), set_add(P, rnd), set_change(P, rnd), set_words(P, rnd)]
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
                assert not re.search(r"£[\d.,]+p", c), c
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-3", "slug": "money", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Pounds and Pence, Adding and Giving Change",
        "seo_title": "Year 3 Money Worksheets: Pounds and Pence, Adding and Giving Change",
        "short_title": "Money",
        "domain": "Measurement",
        "standard_code": "Year 3: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Add and subtract amounts of money to give change, using both £ and p in practical contexts.",
        "meta_desc": "Free Year 3 maths worksheets on money: count UK coins, change pence into pounds (150p = £1.50), add prices at the tuck shop, give change from £1, £2, £5 and £10 by counting on, and solve money word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "£1 = 100p. So 150p = £1 and 50p = £1.50.",
        "key_sub": "Count coins biggest first. To give change, count on from the price: 35p to 40p is 5p, 40p to £1 is 60p, so the change from £1 is 65p.",
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
