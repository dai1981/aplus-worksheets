# -*- coding: utf-8 -*-
"""
UK Year 4 Maths: Money (National Curriculum in England, Year 4: Measurement)
  python3 tools/gen_uk_maths_y4_money.py
All amounts are whole numbers of pence (int), so every total, change and typical mistake is exact.
Writing money: under £1 as 45p, from £1 as £3.45 (never £3.45p, never £3.5).
Coins and notes are simple labelled shapes (no real coin or note artwork).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-4")
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


def count_up(price, paid):
    """counting on for change: '£6.35 + 5p = £6.40, £6.40 + 60p = £7.00, £7.00 + £3 = £10.00. 5p + 60p + £3 = £3.65.'"""
    steps, s = [], price
    jumps = []
    if s % 10:
        j = 10 - s % 10
        steps.append("%s + %dp = %s" % (gbp(s), j, gbp(s + j)))
        jumps.append(j)
        s += j
    if s % 100 and s < paid:
        j = 100 - s % 100
        steps.append("%s + %dp = %s" % (gbp(s), j, gbp(s + j)))
        jumps.append(j)
        s += j
    if s < paid:
        j = paid - s
        steps.append("%s + %s = %s" % (gbp(s), nat(j) if j % 100 else whole(j), gbp(paid)))
        jumps.append(j)
        s += j
    assert s == paid
    ch = paid - price
    js = " + ".join(lab(j) if j < 100 or j % 100 == 0 else nat(j) for j in jumps)
    tail = "" if len(jumps) == 1 else " %s = %s." % (js, nat(ch))
    return "Count on from %s to %s: %s.%s" % (gbp(price), gbp(paid), ", ".join(steps), tail)


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


def sub_e(a, b):
    """take away the pounds, then the pence"""
    r = a - b
    out = []
    mid = a
    if b >= 100:
        mid = a - (b // 100) * 100
        out.append("Take away the pounds: %s − £%d = %s." % (gbp(a), b // 100, gbp(mid)))
    if b % 100:
        if mid % 100 >= b % 100:
            out.append("Take away the pence: %s − %dp = <b>%s</b>." % (gbp(mid), b % 100, nat(r)))
        else:
            out.append("Take away the pence: %s − %dp. %d − %d is not possible, so exchange £1 for 100p: "
                       "%dp − %dp = %dp = <b>%s</b>." % (gbp(mid), b % 100, mid % 100, b % 100, mid, b % 100, r, nat(r)))
    else:
        out[-1] = out[-1].replace(gbp(mid) + ".", "<b>%s</b>." % nat(r))
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


def change_cands(paid, price):
    """bad number bond to 100 (35 + 75), forgetting the £1 used, both, then others"""
    r = paid - price
    c = []
    if price % 10:
        c += [r + 110, r + 10, r + 100]     # e.g. £10 − £6.35: £4.75, £3.75, £4.65
    else:
        c += [r + 100]
    c += [small_from_big(paid, price), price, r - 10, r + 5]
    return c


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


def change_line_svg(price, paid):
    """empty number line (not to scale) for counting on to give change"""
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s % 100 and s < paid:
        s += 100 - s % 100
        pts.append(s)
    if s < paid:
        pts.append(paid)
    seg = [130, 150, 170][:len(pts) - 1]
    x0, y0 = 40, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 40
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, gbp(p), 15))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        j = pts[i + 1] - pts[i]
        b.append(text(m, y0 - 34, "+" + (lab(j) if j < 100 or j % 100 == 0 else nat(j)), 15, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting on from %s to %s" % (gbp(price), gbp(paid)))


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


# ============================================================ set 1: count coins and notes
def set_count(P, rnd):
    its = []
    groups = [
        # coins under £1
        [("C10", 4)], [("C5", 6)], [("C20", 3), ("C2", 2)], [("C50", 1), ("C20", 1), ("C5", 1), ("C1", 1)],
        [("C20", 2), ("C10", 1), ("C5", 1), ("C2", 1), ("C1", 1)], [("C50", 1), ("C20", 1), ("C10", 2), ("C2", 2), ("C1", 1)],
        # coins from £1
        [("C100", 2), ("C50", 1)], [("C200", 1), ("C100", 1), ("C20", 1), ("C10", 1)],
        [("C200", 2), ("C50", 1), ("C5", 1), ("C1", 1)], [("C100", 1), ("C50", 2), ("C20", 1), ("C2", 1)],
        [("C200", 1), ("C100", 2), ("C20", 2), ("C5", 1)], [("C200", 1), ("C50", 1), ("C20", 1), ("C10", 1), ("C5", 1), ("C2", 1)],
        [("C100", 3), ("C5", 1), ("C2", 1), ("C1", 1)],
        # notes and coins
        [("N5", 1), ("C200", 1), ("C100", 1), ("C50", 1)], [("N10", 1), ("N5", 1), ("C100", 1), ("C20", 1), ("C5", 1)],
        [("N10", 1), ("C200", 2), ("C10", 1), ("C2", 1)], [("N20", 1), ("N5", 1), ("C200", 1), ("C50", 1), ("C1", 1)],
        [("N5", 2), ("C100", 1), ("C20", 2), ("C2", 1)], [("N20", 1), ("N10", 1), ("C200", 1), ("C5", 1)],
        [("N10", 2), ("N5", 1), ("C200", 1), ("C100", 1), ("C50", 1), ("C20", 1), ("C10", 1)],
    ]
    mixed = {4, 9, 11, 17, 19}
    stems = ["How much money is shown?", "%s has this money. How much does %s have?",
             "%s finds these coins in %s pencil case. How much is it?", "What is the total?",
             "%s saves this money in a money box. How much has %s saved?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert len(toks) <= 9
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if "pencil case" in st and any(t.startswith("N") for t in toks):
            st = stems[1]
        if st.count("%s") == 2:
            st = st % (nm, his if "pencil" in st else he)
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = ("Put the money in order, biggest value first. " if i in mixed else "") + count_on(toks)
        if len(set(toks)) == 1:
            t = toks[0]
            e = "Each coin is %s. Count in %ds: %s. That is <b>%s</b>." % (
                lab(VAL[t]), VAL[t], ", ".join("%dp" % (VAL[t] * k) for k in range(1, len(toks) + 1)), nat(T))
        cands = [drop_zero(T), m_count(toks), m_pound_as_p(toks), m_same_step(toks), m_skip(toks, -1),
                 m_twice(toks, 0), m_skip(toks, 0), m_twice(toks, -1)]
        if i >= 6:
            cands = [drop_zero(T), m_pound_as_p(toks)] + cands[3:][i % 3:] + cands[3:][:i % 3] + [m_count(toks)]
        its.append(mcq(q, T, cands, e))
    assert len(its) == 20
    return {"title": "Count coins and notes", "items": its}


# ============================================================ set 2: pounds and pence
def set_convert(P, rnd):
    its = []
    its.append(mcq("How many pence are the same as £1?", "100p", ["10p", "1,000p", "50p"],
                   "£1 = <b>100p</b>. That is why there are always two digits for the pence after the point."))
    its.append(mcq("£6 = ? p", 600, [60, 6, 6000],
                   "£1 = 100p, so £6 = 6 × 100p = <b>600p</b>.", fmt=pen))

    def to_p(p, wrong, extra=""):
        s = gbp(p)
        e = "Multiply by 100: %s × 100 = %s. Or read it: %d pounds and %d pence is %d × 100p + %dp = <b>%s</b>.%s" % (
            s, pen(p), p // 100, p % 100, p // 100, p % 100, pen(p), extra)
        if p < 100:
            e = "%s has 0 pounds and %d pence, so it is <b>%s</b>.%s" % (s, p, pen(p), extra)
        return mcq("Write %s in pence." % s, p, wrong, e, fmt=pen)

    its.append(to_p(345, [3450, 48, 3045], " Adding 3 + 45 = 48p forgets that each pound is 100p."))
    its.append(to_p(407, [47, 470, 4007], " The 0 holds the tens of pence. 47p would lose 4 whole pounds."))
    its.append(to_p(250, [25, 205, 2500], " £2.50 is 2 pounds and 50 pence, not 25p."))
    its.append(to_p(1280, [128, 1208, 12800], ""))
    its.append(to_p(65, [650, 605, 6500], " 650p would be £6.50."))

    def to_l(p, wrong, extra=""):
        e = "Divide by 100: 100p = £1. %s is %d pounds and %d pence, so it is <b>%s</b>. Always write two digits for the pence.%s" % (
            pen(p), p // 100, p % 100, gbp(p), extra)
        if p < 100:
            e = "%s is less than £1, so there are 0 pounds: <b>%s</b>. The pence still take two digits.%s" % (pen(p), gbp(p), extra)
        return mcq("Write %s in pounds." % pen(p), gbp(p), wrong, e)

    its.append(to_l(250, ["£25.00", "£250.00", "£2.05"], " 250p is not £25.0: that would be 2,500p."))
    its.append(to_l(407, ["£4.70", "£40.70", "£0.47"], " £4.70 would be 470p."))
    its.append(to_l(75, ["£75.00", "£7.50", "£7.05"], ""))
    its.append(to_l(1005, ["£1.05", "£10.50", "£100.50"], " £10.50 would be 1,050p."))
    its.append(to_l(9, ["£0.90", "£9.00", "£90.00"], " £0.90 would be 90p."))
    its.append(to_l(1360, ["£1.36", "£136.00", "£13.06"], ""))

    its.append(mcq("How do you write 3 pounds and 45 pence?", "£3.45", ["£345", "£34.50", "£30.45"],
                   "Write £, the pounds, a point, then the two digits for the pence: <b>£3.45</b>. "
                   "Do not add p at the end: £3.45p is not correct."))
    its.append(mcq("How do you write 8 pounds and 6 pence?", "£8.06", ["£8.60", "£806", "£0.86"],
                   "The pence take two digits, so 6 pence is 06: <b>£8.06</b>. £8.60 would be 8 pounds and 60 pence."))
    its.append(mcq("Which is the right way to write 2 pounds and 50 pence?", "£2.50", ["£2.05", "£25.00", "£250"],
                   "50 pence is .50, so it is <b>£2.50</b> (or 250p). We never write £2.5 or £2.50p."))
    its.append(mcq("Which is the right way to write 105p in pounds?", "£1.05", ["£1.5", "£10.50", "£105"],
                   "105p = 100p + 5p = £1 and 5 pence. 5 pence is .05, so it is <b>£1.05</b>. "
                   "£1.5 would mean £1.50."))
    its.append(mcq("Which amount is the same as £5.20?", "520p", ["52p", "502p", "5,200p"],
                   "£5.20 is 5 pounds and 20 pence: 500p + 20p = <b>520p</b>.", fmt=pen))
    its.append(mcq("Write £7.99 in pence.", "799p", ["79p", "7,990p", "709p"],
                   "7 pounds is 700p. 700p + 99p = <b>799p</b>."))
    its.append(mcq("£20 = ? p", 2000, [200, 20000, 20],
                   "£1 = 100p, so £20 = 20 × 100p = <b>2,000p</b>.", fmt=pen))
    # verify the fixed answers
    for it in its:
        v = mval(it["c"][0])
        assert v is not None
    assert len(its) == 20
    return {"title": "Pounds and pence", "items": its}


# ============================================================ set 3: compare, order, estimate
def set_compare(P, rnd):
    its = []
    for a, b in [("£1.09", "190p"), ("£2.50", "205p"), ("75p", "£0.57"), ("£3.40", "304p"), ("£6.05", "650p")]:
        va, vb = mval(a), mval(b)
        assert va != vb
        big = a if va > vb else b
        pa = a if a.endswith("p") else "%s = %s" % (a, pen(va))
        pb = b if b.endswith("p") else "%s = %s" % (b, pen(vb))
        conv = [x for x in (pa, pb) if "=" in x]
        e = "Write both in pence: %s. %s is more than %s, so <b>%s</b> is more." % (
            " and ".join(conv), pen(max(va, vb)), pen(min(va, vb)), big)
        its.append(mcq("Which amount is more: %s or %s?" % (a, b), big,
                       [a if big == b else b, "They are the same.", "You cannot compare £ and p."], e))
    for opts, best, word in [(["£4.50", "405p", "£4.15", "445p"], max, "greatest"),
                             (["£1.20", "102p", "£1.12", "210p"], min, "smallest"),
                             (["£8.09", "890p", "£8.80", "899p"], max, "greatest")]:
        vals = [mval(o) for o in opts]
        assert len(set(vals)) == 4
        b = best(vals)
        right = opts[vals.index(b)]
        e = "Write them all in pence: %s. The %s is <b>%s</b>." % (
            ", ".join(o if o.endswith("p") else "%s = %s" % (o, pen(v)) for o, v in zip(opts, vals)), word, right)
        its.append(mcq("Which amount is the %s: %s?" % (word, ", ".join(opts[:-1]) + " or " + opts[-1]), right, [o for o in opts if o != right], e))
    for amts, wrongs in [(["£2.10", "120p", "£1.02"], [["£1.02", "£2.10", "120p"], ["120p", "£1.02", "£2.10"], ["£2.10", "120p", "£1.02"]]),
                         (["£3.25", "352p", "£3.05", "235p"],
                          [["£3.05", "£3.25", "235p", "352p"], ["235p", "352p", "£3.05", "£3.25"], ["352p", "£3.25", "£3.05", "235p"]]),
                         (["90p", "£0.09", "£9.00"], [["£9.00", "£0.09", "90p"], ["90p", "£0.09", "£9.00"], ["£0.09", "£9.00", "90p"]])]:
        vals = [mval(x) for x in amts]
        assert len(set(vals)) == len(vals)
        order = sorted(amts, key=mval)
        right = ", ".join(order)
        e = "Write them all in pence: %s. Smallest to greatest: <b>%s</b>." % (
            ", ".join(x if x.endswith("p") else "%s = %s" % (x, pen(mval(x))) for x in amts), right)
        wl = [", ".join(w) for w in wrongs]
        for w in wrongs:
            assert sorted(w) == sorted(amts) and w != order
        its.append(mcq("Put these amounts in order, smallest first: %s." % ", ".join(amts), right, wl, e))
    # round to the nearest pound
    for p, wrong in [(349, ["£4", "£3.50", "£3.40"]), (650, ["£6", "£6.50", "£7.50"]), (89, ["£0", "90p", "£9"]),
                     (1251, ["£12", "£12.50", "£12.60"]), (705, ["£8", "£7.10", "£7.50"])]:
        r = (p + 50) // 100 * 100
        pp = p % 100
        e = "Look at the pence: %dp. %s, so round %s. %s rounds to <b>%s</b>." % (
            pp, "50p or more rounds up" if pp >= 50 else "Less than 50p rounds down", "up" if pp >= 50 else "down",
            nat(p), whole(r))
        if p == 650:
            e += " Exactly 50p rounds up."
        its.append(mcq("Round %s to the nearest pound." % nat(p), whole(r), wrong, e))
    # estimate
    items = [299, 495, 110]
    est = sum((x + 50) // 100 * 100 for x in items)
    assert est == 900 and abs(sum(items) - est) < 50
    its.append(mcq("Estimate £2.99 + £4.95 + £1.10 by rounding each price to the nearest pound.", "£9", ["£7", "£10", "£8"],
                   "£2.99 is about £3, £4.95 is about £5, £1.10 is about £1. £3 + £5 + £1 = <b>£9</b>. "
                   "(Exact: %s.) Cutting off the pence gives £2 + £4 + £1 = £7, which is too low." % nat(sum(items))))
    nm, he, his = P.next()
    assert 499 + 599 > 1000
    its.append(mcq("%s has £10. %s wants a book for £4.99 and a game for £5.99. Is £10 enough?" % (nm, cap(he)),
                   "No, they cost about £11.", ["Yes, they cost about £9.", "Yes, they cost about £10.", "No, they cost about £12."],
                   "£4.99 is about £5 and £5.99 is about £6. £5 + £6 = £11, which is more than £10, so <b>no</b>. "
                   "(Exact: £4.99 + £5.99 = £10.98.)"))
    assert (785 + 50) // 100 - (210 + 50) // 100 == 6
    its.append(mcq("Estimate £7.85 − £2.10 by rounding to the nearest pound.", "£6", ["£5", "£10", "£4"],
                   "£7.85 is about £8 and £2.10 is about £2. £8 − £2 = <b>£6</b>. (Exact: £5.75.) "
                   "Cutting off the pence gives £7 − £2 = £5, which is further away. £10 comes from adding instead of subtracting."))
    assert 3 * 195 == 585
    its.append(mcq("A sandwich costs £1.95. About how much do 3 sandwiches cost?", "£6", ["£3", "£2", "£5"],
                   "£1.95 is about £2. 3 × £2 = <b>£6</b>. (Exact: 3 × £1.95 = £5.85.) "
                   "Cutting off the pence gives 3 × £1 = £3, which is far too low."))
    assert len(its) == 20
    return {"title": "Compare, order and estimate", "items": its}


# ============================================================ set 4: add, subtract and give change
def set_calc(P, rnd):
    its = []
    adds = [[230, 145], [365, 248], [475, 80], [199, 299], [120, 85, 250], [638, 347], [1250, 765], [95, 68]]
    for i, nums in enumerate(adds):
        T = sum(nums)
        q = "%s = ?" % " + ".join(nat(n) for n in nums)
        cands = [noexch_add(nums), forgot_pound_add(nums)]
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        if any(n < 100 for n in nums) and any(n >= 100 for n in nums):
            # treated the pence as pounds: £4.75 + 80p -> £4.75 + £80
            cands.insert(0, sum(n * 100 if n < 100 else n for n in nums))
        cands += [T - 10, T + 100, T + 10]
        e = add_e(nums)
        if nums == [199, 299]:
            e += " Or: £2 + £3 = £5, then take away 1p + 1p: £5 − 2p = £4.98."
        its.append(mcq(q, T, cands, e))
    subs = [[580, 230], [852, 327], [600, 245], [420, 75], [1005, 350], [915, 468]]
    for a, b in subs:
        r = a - b
        cands = [small_from_big(a, b), a + b, r + 100, r + 10, r - 10]
        if b < 100:
            cands.insert(0, a - b * 100 if a > b * 100 else None)
        its.append(mcq("%s − %s = ?" % (nat(a), nat(b)), r, cands, sub_e(a, b)))
    for paid, price, thing in [(500, 340, "a toy car"), (1000, 635, "a lunchbox"), (500, 285, "a pencil case"),
                               (2000, 1249, "a board game"), (1000, 718, "a jigsaw"), (2000, 1460, "a football kit")]:
        nm, he, his = P.next()
        r = paid - price
        q = "%s buys %s for %s. %s pays with a %s note. How much change does %s get?" % (
            nm, thing, nat(price), cap(he), whole(paid), he)
        its.append(mcq(q, r, change_cands(paid, price), count_up(price, paid) + " The change is <b>%s</b>." % nat(r)))
    assert len(its) == 20
    return {"title": "Add, subtract and give change", "items": its}


# ============================================================ set 5: word problems
def set_words(P, rnd):
    its = []
    W = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    assert 100 - (35 + 45) == 20
    add("%s buys toast for 35p and a carton of milk for 45p at the tuck shop. %s pays with a £1 coin. How much change does %s get?"
        % (nm, cap(he), he), 20, [80, 10, 30],
        "Total: 35p + 45p = 80p. Change from £1 = 100p: count on from 80p to 100p = <b>20p</b>.")
    nm, he, his = P.next()
    add("A child bus ticket costs £1.20. %s takes the bus to school and back home again. How much does %s pay that day?"
        % (nm, he), 240, [120, 220, 140],
        "Two tickets: £1.20 + £1.20. Pounds: £1 + £1 = £2. Pence: 20p + 20p = 40p. Total <b>£2.40</b>.")
    nm, he, his = P.next()
    assert 5 * 240 == 1200
    add("A return bus ticket to school costs £2.40. %s buys one every school day for 5 days. How much does %s spend?"
        % (nm, he), 1200, [1040, 245, 1020],
        "5 × £2.40: 5 × £2 = £10 and 5 × 40p = 200p = £2. £10 + £2 = <b>£12.00</b>.")
    nm, he, his = P.next()
    assert 3 * 650 == 1950
    add("Cinema tickets cost £6.50 each. %s goes with %s mum and dad. How much do the 3 tickets cost?" % (nm, his),
        1950, [1850, 950, 1800],
        "3 × £6.50: 3 × £6 = £18 and 3 × 50p = 150p = £1.50. £18 + £1.50 = <b>£19.50</b>. "
        "£18.50 forgets to multiply the 50p by 3.")
    nm, he, his = P.next()
    add("At the cinema, popcorn costs £3.75. %s pays with a £5 note. How much change does %s get?" % (nm, he),
        125, change_cands(500, 375), count_up(375, 500) + " The change is <b>£1.25</b>.")
    nm, he, his = P.next()
    assert 4 * 250 == 1000
    add("%s saves £2.50 of %s pocket money each week. How many weeks does it take to save £10?" % (nm, his),
        "4 weeks", ["5 weeks", "3 weeks", "25 weeks"],
        "Count in £2.50s: £2.50, £5.00, £7.50, £10.00. That is <b>4 weeks</b>. "
        "5 weeks would be the answer for £2 a week.")
    nm, he, his = P.next()
    have = 6 * 300
    assert have - 799 == 1001
    add("%s gets £3 pocket money every week. %s saves it all for 6 weeks, then buys a book for £7.99. How much money is left?"
        % (nm, cap(he)), 1001, change_cands(have, 799),
        "Saved: 6 × £3 = £18. " + count_up(799, have) + " <b>£10.01</b> is left.")
    nm, he, his = P.next()
    assert 4 * 45 == 180
    add("Pencils cost 45p each. %s buys 4 pencils. How much does %s pay?" % (nm, he), 180, [165, 49, 160],
        "4 × 45p: 4 × 40p = 160p and 4 × 5p = 20p. 160p + 20p = 180p = <b>£1.80</b>. "
        "£1.65 only multiplies the 40p, not the 5p.")
    nm, he, his = P.next()
    assert 200 - 3 * 65 == 5
    add("A bag of crisps costs 65p. %s buys 3 bags and pays with a £2 coin. How much change does %s get?" % (nm, he),
        5, [195, 15, 35],
        "Cost: 3 × 65p = 195p = £1.95. Change: count on from £1.95 to £2.00 = <b>5p</b>. "
        "15p comes from a wrong number bond (95 + 15 = 110, not 100).")
    nm, he, his = P.next()
    add("%s and %s brother share £7 equally. How much does each of them get?" % (nm, his),
        350, [300, 1400, 305],
        "Half of £7: £7 = 700p. 700p ÷ 2 = 350p = <b>£3.50</b>. £3 forgets the £1 left over, "
        "which is 50p each.")
    nm, he, his = P.next()
    add("%s gets £10 for %s birthday. %s spends %s of it on a comic. How much does the comic cost?"
        % (nm, his, cap(he), frac(1, 4)), 250, [200, 4000, 500],
        "%s of £10 means £10 ÷ 4. £10 = 1,000p. 1,000p ÷ 4 = 250p = <b>£2.50</b>. "
        "£5 would be a half, not a quarter." % frac(1, 4))
    add("A pizza costs £4.50. Three friends share the cost equally. How much does each friend pay?",
        150, [1350, 225, 105],
        "£4.50 ÷ 3: 450p ÷ 3 = 150p = <b>£1.50</b>. £2.25 would be half, for 2 friends.")
    nm, he, his = P.next()
    add("%s has £8. %s spends %s of it on a model kit. How much does %s spend?" % (nm, cap(he), frac(3, 4), he),
        "£6.00", ["£2.00", "£24.00", "£4.00"],
        "First find %s: £8 ÷ 4 = £2. Then %s is 3 × £2 = <b>£6.00</b>. "
        "£2 is only one quarter." % (frac(1, 4), frac(3, 4)))
    nm, he, his = P.next()
    assert 270 - 245 == 25
    add("A comic costs £2.45 in one shop and 270p in another shop. How much cheaper is the first shop?",
        25, [35, 20, 5],
        "270p = £2.70. Count on from £2.45: £2.45 + 5p = £2.50, £2.50 + 20p = £2.70. 5p + 20p = <b>25p</b>. "
        "35p comes from taking the smaller digit from the bigger one in each column (5 − 0 and 7 − 4).")
    nm, he, his = P.next()
    add("%s has £4.35 in %s money box. %s gran gives %s £2.80. How much money does %s have now?"
        % (nm, his, cap(his), "her" if he == "she" else "him", he),
        715, [forgot_pound_add([435, 280]), 155, 725], add_e([435, 280]))
    nm, he, his = P.next()
    spent = 899 + 350
    add("%s buys a football for £8.99 and a pump for £3.50. %s pays with a £20 note. How much change does %s get?"
        % (nm, cap(he), he), 2000 - spent, [spent] + change_cands(2000, spent),
        "Spent: £8.99 + £3.50 = £12.49. " + count_up(spent, 2000) + " The change is <b>£7.51</b>.")
    nm, he, his = P.next()
    add("A school trip costs £12.50. %s has paid £8.75 so far. How much more does %s need to pay?" % (nm, he),
        375, [2125] + change_cands(1250, 875), count_up(875, 1250) + " %s needs to pay <b>£3.75</b> more." % cap(he))
    add("A pack of 4 yoghurts costs £2.40. How much is that for 1 yoghurt?", 60, [960, 6, 120],
        "£2.40 = 240p. 240p ÷ 4 = <b>60p</b>. Check: 4 × 60p = 240p = £2.40.")
    nm, he, his = P.next()
    assert 6 * 70 - 300 == 120
    add("One bag of crisps costs 70p. A multipack of 6 bags costs £3. How much does %s save by buying the multipack instead of 6 single bags?"
        % nm, 120, [420, 230, 40],
        "6 single bags: 6 × 70p = 420p = £4.20. Saving: £4.20 − £3.00 = <b>£1.20</b>.")
    nm, he, his = P.next()
    spent = 675 + 180
    add("%s has £15. %s buys a cinema ticket for £6.75 and a drink for £1.80. How much money does %s have left?"
        % (nm, cap(he), he), 1500 - spent, [spent] + change_cands(1500, spent),
        "Spent: £6.75 + £1.80 = £8.55. " + count_up(spent, 1500) + " %s has <b>£6.45</b> left." % cap(he))
    assert len(its) == 20
    return {"title": "Money word problems", "items": its}


# ============================================================ lesson
def body_html():
    all_coins = ["C1", "C2", "C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20"]
    walk = toks_of(("C200", 1), ("C100", 1), ("C50", 1), ("C20", 1), ("C5", 1))
    under = ["£2", "£3", "£3.50", "£3.70", "£3.75"]
    assert total(walk) == 375
    return (
        "<h2>Pounds and pence</h2>"
        "<p>£1 = 100p. In £3.45, the 3 is the pounds and the 45 is the pence. "
        "The pence always take <b>two digits</b> after the point.</p>"
        "<figure class='sn-fig'>" + money_svg(all_coins, per_row=8, label="UK coins: 1p, 2p, 5p, 10p, 20p, 50p, £1, £2") +
        "<figcaption>Coins: 1p, 2p, 5p, 10p, 20p, 50p, £1 and £2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, label="UK notes: £5, £10, £20") +
        "<figcaption>Notes: £5, £10 and £20.</figcaption></figure>"
        + table(["Pounds", "Pence", "Why"], [
            ["£4.07", "407p", "4 pounds = 400p, plus 7p"],
            ["£2.50", "250p", "2 pounds = 200p, plus 50p"],
            ["£0.65", "65p", "less than £1"],
            ["£10.05", "1,005p", "10 pounds = 1,000p, plus 5p"],
        ]) +
        "<h2>Count the value, biggest first</h2>"
        "<p>Count the notes and pound coins first, then count on the pence.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=20, under=under, label="counting on: £2, £3, £3.50, £3.70, £3.75") +
        "<figcaption>£2, £3, £3.50, £3.70, £3.75. The coins are worth £3.75.</figcaption></figure>"
        + ex("Example", "Add £3.65 + £2.48.",
             "Pounds: £3 + £2 = £5. Pence: 65p + 48p = 113p = £1.13. £5 + £1.13 = £6.13.", "£6.13")
        + "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Jump to the next 10p, then to the next pound, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line_svg(635, 1000) +
        "<figcaption>£10 − £6.35: 5p + 60p + £3 = £3.65 change.</figcaption></figure>"
        + ex("Example", "What is half of £7?", "£7 = 700p. 700p ÷ 2 = 350p.", "£3.50")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["£4.07 = 47p", "Each pound is 100p: £4.07 = 400p + 7p = 407p"],
            ["250p = £25.0", "Divide by 100: 250p = £2.50"],
            ["Writing £2.5 or £2.50p", "Two digits for the pence, and no p after £: £2.50"],
            ["Change from £10 for £6.35 is £4.75 or £3.75", "Count on: 5p + 60p + £3 = £3.65 (35p + 65p = 100p)"],
            ["Counting coins, not value: 4 coins = 4p", "Count the value of each coin: £2, £3, £3.50 …"],
        ])
    )


FAQ = [
    {"q": "What should a Year 4 child know about money?",
     "a": "In the National Curriculum, Year 4 pupils estimate, compare and calculate with money in pounds and pence, and solve money problems with fractions and decimals to two places, such as change from £10 or half of £7."},
    {"q": "How do you change pounds into pence?",
     "a": "Multiply by 100, because £1 = 100p: £4.07 = 407p. To change pence into pounds, divide by 100 and keep two digits for the pence: 250p = £2.50."},
    {"q": "What is the easiest way to work out change?",
     "a": "Count on from the price to the money paid: first to the next 10p, then to the next pound, then to the note. For £6.35 from £10: 5p + 60p + £3 = £3.65."},
    {"q": "Why do we write £2.50 and not £2.5?",
     "a": "Pence always take two digits after the point, so 50 pence is written .50. Write either £2.50 or 250p, never £2.5 or £2.50p."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(4410)
    P = People(rnd)
    sets = [set_count(P, rnd), set_convert(P, rnd), set_compare(P, rnd), set_calc(P, rnd), set_words(P, rnd)]
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
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-4", "slug": "money", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Pounds and Pence, Adding and Giving Change",
        "seo_title": "Year 4 Money Worksheets: Pounds and Pence, Change and Word Problems",
        "short_title": "Money",
        "domain": "Measurement",
        "standard_code": "Year 4: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Estimate, compare and calculate different measures, including money in pounds and pence; solve simple measure and money problems involving fractions and decimals to two decimal places.",
        "meta_desc": "Free Year 4 maths worksheets on money: count UK coins and notes, change pounds to pence (£4.07 = 407p), compare and estimate amounts, add and subtract money, work out change and solve word problems. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "£1 = 100p. The pence always take two digits: £4.07 = 407p, 250p = £2.50.",
        "key_sub": "Count money biggest value first. To give change, count on from the price: £6.35 to £6.40 is 5p, to £7 is 60p, to £10 is £3, so the change from £10 is £3.65.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "money")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
