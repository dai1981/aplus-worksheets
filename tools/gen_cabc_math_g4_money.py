# -*- coding: utf-8 -*-
"""
BC Grade 4 Math: Money and Making Change (BC Mathematics Curriculum, Financial literacy:
monetary calculations, including making change with amounts to 100 dollars and making simple financial decisions)
  python3 tools/gen_cabc_math_g4_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Writing money: under $1 as 45¢, whole dollars as $7, other amounts as $7.65 (never $7.6, never $7.65¢).
Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1 (11 sides, gold colour), toonie $2.
No pennies: cash totals are rounded to the nearest 5¢; card payments are exact.
Bills: $5 blue, $10 purple, $20 green, $50 red, $100 brown. Coins and bills are simple labelled shapes.
Coin and bill drawing copied from gen_ca_math_g3_money.py, counting up and rounding from gen_au_maths_y4_money.py.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

# ------------------------------------------------------------ money facts
ORDER = ["B100", "B50", "B20", "B10", "B5", "T", "L", "Q", "D", "N"]   # biggest value first
VAL = {"B100": 10000, "B50": 5000, "B20": 2000, "B10": 1000, "B5": 500, "T": 200, "L": 100,
       "Q": 25, "D": 10, "N": 5}
ONE = {"B100": "$100 bill", "B50": "$50 bill", "B20": "$20 bill", "B10": "$10 bill", "B5": "$5 bill",
       "T": "toonie", "L": "loonie", "Q": "quarter", "D": "dime", "N": "nickel"}
MANY = {k: (v + "s") for k, v in ONE.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius in proportion to the real coins (mm): dime 18, nickel 21.2, quarter 23.9, loonie 26.5, toonie 28
COIN = {"D": (18, SILVER, 14), "N": (21, SILVER, 15), "Q": (24, SILVER, 15), "L": (26, GOLD, 16), "T": (28, SILVER, 16)}
BILL = {"B5": ("#c4dcf2", "#1f5f99"), "B10": ("#ddcbee", "#5b2d8a"), "B20": ("#cbe7c4", "#2f7a2a"),
        "B50": ("#f5c6c6", "#a32020"), "B100": ("#e8d6c2", "#7a4a1c")}
BILL_W, BILL_H = 80, 42


def lab(v):
    """a coin or bill value: 25¢, $2, $20"""
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def nat(c):
    """45 -> '45¢', 700 -> '$7', 765 -> '$7.65'"""
    assert c > 0, c
    if c < 100:
        return "%d¢" % c
    if c % 100 == 0:
        return "$%d" % (c // 100)
    return "${}.{:02d}".format(c // 100, c % 100)


def dol(c):
    """always with cents: 700 -> '$7.00' (used where a price list or receipt shows it)"""
    return "${}.{:02d}".format(c // 100, c % 100)


def mval(s):
    """value in cents of a money text, or None"""
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^\$(\d+)(?:\.(\d{1,2}))?$", s)
    if m:
        f = m.group(2) or "0"
        return int(m.group(1)) * 100 + int(f.ljust(2, "0"))
    m = re.match(r"^(\d+)¢$", s)
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


def nw(n, t):
    return "%d %s" % (n, ONE[t] if n == 1 else MANY[t])


def group(toks):
    parts = [nw(n, t) for t, n in counts(toks)]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def cap(s):
    return s[0].upper() + s[1:]


def round5(c):
    """Canadian cash rounding: ends in 1, 2 down to 0; 3, 4 up to 5; 6, 7 down to 5; 8, 9 up to the next 10"""
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
        out.append(("Count the bills and dollar coins, biggest first: %s." if len(dollars) > 1 else "Dollars: %s.") % ", ".join(run))
    C = 0
    if cents:
        run = []
        for t in cents:
            C += VAL[t]
            run.append("%d¢" % C)
        out.append(("Count on the cents: %s." if dollars else "Start with the biggest coin and count on: %s.") % ", ".join(run))
    T = total(toks)
    if dollars and cents:
        if C >= 100:
            out.append("%d¢ = %s. $%d + %s = <b>%s</b>." % (C, nat(C), s // 100, nat(C), nat(T)))
        else:
            out.append("$%d and %d¢ is <b>%s</b>." % (s // 100, C, nat(T)))
    elif dollars:
        out.append("That is <b>%s</b>." % nat(T))
    else:
        out.append("That is <b>%s</b>." % nat(T) if C < 100 else "%d¢ = <b>%s</b>." % (C, nat(T)))
    return " ".join(out)


# ------------------------------------------------------------ typical mistakes (all computed, in cents)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


def m_each_dollar(toks):
    """counted every coin and bill as $1"""
    return 100 * len(toks)


def m_quarter20(toks):
    """thought a quarter is 20¢"""
    return sum(20 if t == "Q" else VAL[t] for t in toks)


def m_swap(toks):
    """the bigger nickel taken as 10¢ and the small dime as 5¢"""
    sw = {"N": 10, "D": 5}
    return sum(sw.get(t, VAL[t]) for t in toks)


def m_toonie1(toks):
    """counted a toonie as $1, like a loonie"""
    return sum(100 if t == "T" else VAL[t] for t in toks)


def m_lost_dollar(toks):
    """the cents came to $1 or more, but the extra dollar was not added"""
    C = sum(VAL[t] for t in toks if VAL[t] < 100)
    if C < 100:
        return None
    return sum(VAL[t] for t in toks if VAL[t] >= 100) + C % 100


def kinds(toks):
    return [t for t, n in counts(toks)]


def m_skip(toks, k=-1):
    return total(toks) - VAL[kinds(toks)[k]]


def m_twice(toks, k=-1):
    return total(toks) + VAL[kinds(toks)[k]]


def digs(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def from_digs(d):
    return sum(x * 10 ** i for i, x in enumerate(d))


def small_from_big(a, b):
    """column subtraction taking the smaller digit from the bigger one"""
    k = len(str(a))
    return from_digs([abs(x - y) for x, y in zip(digs(a, k), digs(b, k))])


def forgot_dollar_add(nums):
    """made 100¢ or more in the cents but did not regroup it as $1"""
    return sum(n // 100 for n in nums) * 100 + sum(n % 100 for n in nums) % 100


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=nat):
    """4 choices: correct + the first 3 usable unique distractors (never equal in value)."""
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
    if t.startswith("B"):
        return BILL_W, BILL_H
    r = COIN[t][0]
    return 2 * r, 2 * r


def polygon(cx, cy, r, n, rot=-90):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def draw_tok(t, cx, cy):
    """one coin or one bill, labelled with its value"""
    if t.startswith("B"):
        fill, edge = BILL[t]
        x, y = cx - BILL_W / 2, cy - BILL_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, BILL_W, BILL_H, fill, edge, x + 5, y + 5, BILL_W - 10, BILL_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r, (fill, edge), fs = COIN[t]
    if t == "L":       # loonie: 11 sides, gold colour
        shape = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (polygon(cx, cy, r, 11), fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 6, edge))
    elif t == "T":     # toonie: silver ring, gold centre
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx, cy, r - 10, GOLD[0], GOLD[1]))
    else:
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, edge))
    return shape + text(cx, cy + fs * 0.36, lab(VAL[t]), fs)


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    widths = []
    for r in rows:
        ws = [max(tok_size(t)[0], 64 if under else 0) for t in r]
        widths.append(sum(ws) + gap * (len(r) - 1))
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rh in zip(rows, heights):
        x = pad
        hh = rh - lab_h
        for t in r:
            w = max(tok_size(t)[0], 64 if under else 0)
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


# ------------------------------------------------------------ counting up for change
def change_pts(price, paid):
    """price -> next 10¢ -> next dollar -> next $10 (for big bills) -> money paid"""
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s % 100 and s < paid:
        s += 100 - s % 100
        pts.append(s)
    if paid >= 5000 and s % 1000 and s + 1000 - s % 1000 < paid:
        s += 1000 - s % 1000
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid and all(a < b for a, b in zip(pts, pts[1:]))
    return pts


def count_up(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (nat(a), nat(b - a), nat(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(nat(j) for j in jumps), nat(ch))
    return "Count up from %s to %s: %s.%s" % (nat(price), nat(paid), ", ".join(steps), tail)


def cents_only(price, paid):
    """counted up to the next dollar and stopped (forgot the big jump)"""
    return (100 - price % 100) % 100 or None


def change_cands(paid, price):
    """real change mistakes, most common first"""
    r = paid - price
    c = []
    if paid > 100 and price % 100:
        c.append(r + 100)           # $10 − $7.65: took $7 from $10 = $3 and kept 35¢: forgot the dollar used for the cents
    if price % 10:
        c.append(r + 10)            # 65¢ + 45¢ "makes 100": 6 + 4 = 10 and 5 + 5 = 10, but that is 110¢
    c += [price, cents_only(price, paid), small_from_big(paid, price), r - 100, r + 5, r - 5, r - 10]
    return [x for x in c if x and 0 < x < paid and x % 5 == 0]


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting up; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [120, 130, 140, 150][:len(pts) - 1]
    x0, y0 = 40, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 40
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, nat(p), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + nat(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting up from %s to %s" % (nat(price), nat(paid)))


def price_svg(items, title):
    """a row of price tags: [('sketchbook', 950), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 20, 78) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, dol(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, dol(p)) for n, p in items))


def receipt_svg(amount, how):
    """a small receipt: total and how it was paid"""
    W, H = 200, 92
    b = ["<rect x='4' y='4' width='%d' height='%d' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (W - 8, H - 8, INK),
         text(W / 2, 30, "RECEIPT", 15),
         "<line x1='16' y1='40' x2='%d' y2='40' stroke='%s' stroke-width='1' stroke-dasharray='4 3'/>" % (W - 16, INK),
         text(18, 62, "Total", 16, "start"), text(W - 18, 62, dol(amount), 18, "end", GREEN),
         text(18, 80, "Paid:", 14, "start"), text(W - 18, 80, how, 14, "end")]
    return svg_wrap(W, H, "".join(b), "receipt: total %s, paid %s" % (dol(amount), how))


# ============================================================ set 1: count collections to $100
def set_count(P, rnd):
    its = []
    groups = [
        [("Q", 3), ("D", 2), ("N", 1)],
        [("L", 2), ("Q", 2), ("D", 1)],
        [("T", 1), ("L", 1), ("Q", 3), ("N", 1)],
        [("T", 2), ("Q", 1), ("D", 3)],
        [("Q", 5), ("D", 3)],
        [("B5", 1), ("L", 2), ("Q", 2)],
        [("B5", 1), ("T", 1), ("D", 4), ("N", 1)],
        [("T", 1), ("Q", 6), ("D", 2)],
        [("B10", 1), ("T", 2), ("Q", 3)],
        [("B10", 1), ("B5", 1), ("L", 3), ("D", 2)],
        [("B10", 1), ("L", 1), ("Q", 4), ("D", 2), ("N", 1)],
        [("B20", 1), ("B5", 1), ("T", 1), ("Q", 1), ("N", 2)],
        [("B20", 1), ("T", 3), ("Q", 3), ("D", 2)],
        [("B20", 1), ("B10", 1), ("L", 1), ("Q", 2), ("D", 1)],
        [("B20", 2), ("T", 2), ("Q", 1), ("D", 2)],
        [("B50", 1), ("B5", 1), ("L", 1), ("Q", 3)],
        [("B50", 1), ("B10", 2), ("T", 1), ("D", 3), ("N", 1)],
        [("B50", 1), ("B20", 1), ("B5", 1), ("T", 2), ("Q", 2)],
        [("B50", 1), ("B20", 1), ("B10", 1), ("B5", 1), ("L", 2), ("Q", 1), ("D", 1), ("N", 1)],
        [("B50", 1), ("B20", 2), ("T", 2), ("Q", 2), ("D", 2)],
    ]
    mixed = {3, 6, 9, 12, 14, 17, 19}
    stems = ["How much money is shown?", "%s has this money. How much does %s have?",
             "%s empties %s piggy bank. How much money is in it?", "What is the total?",
             "%s brings this money to the school book fair. How much does %s bring?"]
    seen_t = set()
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T <= 10000 and T not in seen_t, T
        seen_t.add(T)
        assert len(toks) <= 9, toks
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if st.count("%s") == 2:
            st = st % (nm, his if "piggy" in st else he)
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown, per_row=5 if len(toks) <= 5 else 4)) + st
        e = ("Sort the money first, biggest value first. " if i in mixed else "") + count_on(toks)
        lost = m_lost_dollar(toks)
        coins_only = all(not t.startswith("B") for t in toks)
        cands = []
        if lost:
            cands.append(lost)
        if "Q" in toks:
            cands.append(m_quarter20(toks))
        if coins_only and T < 300:
            cands.append(m_count(toks))
        else:
            cands.append(m_each_dollar(toks))
        if "T" in toks:
            cands.append(m_toonie1(toks))
        if "N" in toks and "D" in toks:
            cands.append(m_swap(toks))
        cands += [m_skip(toks, -1), m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
        it = mcq(q, T, cands, e)
        if lost and nat(lost) in it["c"]:
            it["e"] += " %s forgets the dollar made by the cents." % nat(lost)
        if "Q" in toks and nat(m_quarter20(toks)) in it["c"]:
            it["e"] += " A quarter is 25¢, not 20¢."
        its.append(it)
    assert len(its) == 20
    return {"title": "Count coins and bills to $100", "items": its}


# ============================================================ set 2: make amounts in different ways
def gtxt(vals):
    return ", ".join(lab(v) for v in sorted(vals, reverse=True))


def fewest(target, pieces):
    best = {0: []}
    step = 5
    for a in range(step, target + 1, step):
        opts = [best[a - c] + [c] for c in pieces if a - c in best]
        if opts:
            best[a] = min(opts, key=len)
    return best[target]


COINS = [5, 10, 25, 100, 200]
CENT_COINS = [5, 10, 25]
BILLS = [500, 1000, 2000, 5000]
ALL = COINS + BILLS


def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None):
        assert sum(right) == target, (target, right)
        for w in wrong:
            assert sum(w) != target, (target, w)
        q = (stem or "Which money makes %s?") % nat(target)
        e = ("<b>%s</b> = %s. " % (gtxt(right), nat(target)) + " ".join(
            "%s = %s." % (gtxt(w), nat(sum(w))) for w in wrong))
        its.append(mcq(q, gtxt(right), [gtxt(w) for w in wrong], e))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> = %s, not %s. " % (gtxt(right), nat(sum(right)), nat(target))
             + "The others all make %s." % nat(target))
        its.append(mcq("Which of these does <b>not</b> make %s?" % nat(target), gtxt(right), [gtxt(w) for w in wrong], e))

    def how_few(target, pieces, wrong, extra, word="coins"):
        f = fewest(target, pieces)
        n = len(f)
        one = word[:-1]
        ch = lambda k: "%d %s" % (k, one if k == 1 else word)
        q = "What is the smallest number of %s you can use to make %s?" % (word, nat(target))
        e = "Use the biggest one you can each time: %s = %s. That is <b>%s</b>. %s" % (gtxt(f), nat(target), ch(n), extra)
        its.append(mcq(q, ch(n), [ch(k) for k in wrong], e))

    def which_fewest(target, pieces, wrong, word="coins"):
        f = fewest(target, pieces)
        for w in wrong:
            assert sum(w) == target and len(w) > len(f), (w, f)
        e = ("All of these make %s. <b>%s</b> uses only %d %s: start with the biggest one you can each time."
             % (nat(target), gtxt(f), len(f), word))
        its.append(mcq("Which uses the fewest %s to make %s?" % (word, nat(target)), gtxt(f), [gtxt(w) for w in wrong], e))

    def same_as(toks, right, rv, wrong):
        T = total(toks)
        assert rv == T
        q = fig(money_svg(toks, per_row=6)) + "Which is worth the same as this money?"
        e = count_on(toks) + " So <b>%s</b> is worth the same." % right
        its.append(mcq(q, right, wrong, e, fmt=str))

    def how_many(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, fmt=str))

    which(135, [100, 25, 10], [[100, 25, 5], [100, 10, 10, 10], [25, 25, 25, 10]])
    same_as(["Q"] * 8, "one toonie", 200, ["one loonie", "8 dimes", "two quarters"])
    which(240, [200, 25, 10, 5], [[200, 25, 10], [100, 25, 10, 5], [200, 25, 25]])
    how_many("How many quarters make $3?", "12", ["3", "15", "4"],
             "Four quarters make $1. $3 is 3 dollars, so 4 + 4 + 4 = <b>12</b> quarters. "
             "15 would be right only if a quarter were 20¢.")
    how_few(85, CENT_COINS, [3, 5, 8], "Three quarters make 75¢. Add a dime: 85¢. Using dimes and nickels takes more coins.")
    same_as(["B5"] * 4, "one $20 bill", 2000, ["one $10 bill", "four toonies", "one $50 bill"])
    nm, he, his = P.next()
    which(305, [100, 100, 100, 5], [[100, 100, 100, 10], [200, 25, 25, 5], [100, 100, 25, 5]],
          stem=nm + " has 4 coins. Together they make %s. Which coins does " + he + " have?")
    which_fewest(150, CENT_COINS + [100], [[25] * 6, [100, 25, 10, 10, 5], [100, 10, 10, 10, 10, 10]])
    how_many("How many dimes make $2.50?", "25", ["250", "20", "5"],
             "$2.50 = 250¢. Ten dimes make $1, so $2 is 20 dimes and 50¢ is 5 more: 20 + 5 = <b>25</b>. "
             "250 is the number of cents. 20 forgets the 50¢.")
    which_not(100, [25, 25, 25, 10, 10], [[25, 25, 25, 25], [25, 25, 25, 10, 10, 5], [25, 25, 10, 10, 10, 10, 10]])
    how_few(340, COINS, [4, 6, 8], "4 coins can make $3.35 but not $3.40. Three loonies instead of a toonie and a loonie take more coins.")
    which(1275, [1000, 200, 25, 25, 25], [[1000, 100, 25, 25, 25], [1000, 200, 25, 25], [500, 500, 200, 25, 25, 10]])
    which_not(2000, [1000, 500, 200, 200], [[1000, 500, 500], [1000, 500, 200, 200, 100], [500, 500, 500, 500]])
    which_fewest(280, COINS, [[100, 100, 25, 25, 25, 5], [200, 25, 25, 10, 10, 10], [100, 100, 25, 25, 10, 10, 10]])
    how_few(965, ALL, [5, 9, 12], "$5 + $2 + $2 = $9. Then 25¢ + 25¢ + 10¢ + 5¢ = 65¢. Nine coins and no bill would take more.",
            word="bills and coins")
    nm, he, his = P.next()
    which(7500, [5000, 2000, 500], [[5000, 1000, 500], [5000, 2000, 1000], [2000, 2000, 2000]],
          stem=nm + " has 3 bills. Together they make %s. Which bills does " + he + " have?")
    which_fewest(4500, BILLS, [[2000, 1000, 1000, 500], [1000, 1000, 1000, 1000, 500], [2000, 500, 500, 500, 500, 500]],
                 word="bills")
    how_many("How many $5 bills make $35?", "7", ["30", "5", "6"],
             "Count by 5s: $5, $10, $15, $20, $25, $30, $35. That is <b>7</b> bills. 30 comes from 35 − 5.")
    which_not(500, [200, 200, 25, 25, 25], [[200, 200, 100], [200, 100, 100, 25, 25, 25, 25], [100, 100, 100, 100, 25, 25, 25, 25]])
    nm, he, his = P.next()
    which(4625, [2000, 2000, 500, 100, 25], [[2000, 2000, 500, 25], [2000, 2000, 200, 100, 25], [2000, 1000, 1000, 500, 100, 10, 10]],
          stem=nm + " pays exactly %s for a pair of soccer cleats. Which money could " + he + " use?")
    assert len(its) == 20
    return {"title": "Make amounts in different ways", "items": its}


# ============================================================ set 3: make change by counting up
def money_word(paid):
    return {100: "a loonie", 200: "a toonie", 500: "a $5 bill", 1000: "a $10 bill", 2000: "a $20 bill",
            5000: "a $50 bill", 10000: "a $100 bill"}[paid]


def set_change(P, rnd):
    its = []
    jobs = [(100, 65, "a pencil", True), (500, 320, "a bag of popcorn", False), (1000, 765, "a flying disc", True),
            (1000, 435, "a pack of hockey cards", False), (1000, 890, "a sketchbook", False),
            (2000, 1340, "a pair of swim goggles", True), (2000, 940, "a toque", False), (2000, 1275, "a pair of hiking socks", False),
            (2000, 1615, "a chapter book", False), (2000, 1855, "a puzzle", False),
            (5000, 3260, "a pair of shin pads", True), (5000, 2795, "a backpack", False), (5000, 4120, "a pair of rain boots", False),
            (5000, 1985, "a board game", False), (10000, 6450, "a pair of running shoes", True),
            (10000, 8735, "a hockey stick", False), (10000, 4560, "a skateboard", False), (10000, 2290, "a fishing rod", False)]
    for paid, pr, thing, line in jobs:
        nm, he, his = P.next()
        r = paid - pr
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, nat(pr), cap(he), money_word(paid), he)
        if line:
            q = fig(change_line(pr, paid, show=False)) + q + " Count up on the number line."
        e = count_up(pr, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (nat(r), nat(pr), nat(r), nat(paid))
        it = mcq(q, r, change_cands(paid, pr), e)
        if pr % 100 and paid > 100 and nat(r + 100) in it["c"]:
            it["e"] += " %s forgets that one dollar was used up to make the cents." % nat(r + 100)
        its.append(it)
    nm, he, his = P.next()
    its.append(mcq("A smoothie costs $5.85. %s pays with a $10 bill. About how much change will %s get?" % (nm, he),
                   "about $4", ["about $5", "about $6", "about $3"],
                   "$5.85 is close to $6. $10 − $6 = $4, so the change is <b>about $4</b>. (Exactly: $5.85 + 15¢ = $6, "
                   "$6 + $4 = $10, so $4.15.)", fmt=str))
    nm, he, his = P.next()
    its.append(mcq("%s buys a book for $8.40 with a $20 bill. Is the change more or less than $10?" % nm,
                   "more than $10", ["less than $10", "exactly $10", "exactly $8.40"],
                   "$8.40 is less than $10, so the change from $20 is more than $10. Exactly: $8.40 + 60¢ = $9, "
                   "$9 + $11 = $20, so the change is $11.60. That is <b>more than $10</b>.", fmt=str))
    assert len(its) == 20
    return {"title": "Make change by counting up", "items": its}


# ============================================================ set 4: cash rounding (card is exact)
RULE = ("Canada has no pennies, so a cash total is rounded to the nearest 5¢. "
        "Last digit 1 or 2: round down to 0. 3 or 4: up to 5. 6 or 7: down to 5. 8 or 9: up to the next 10. ")


def set_rounding(P, rnd):
    its = []
    for amt in [347, 1293, 622, 868, 2436, 199, 1504, 4781]:
        R = round5(amt)
        assert R != amt
        other = R + 5 if R < amt else R - 5
        ten = (amt + 5) // 10 * 10
        q = "A total of %s is paid in cash. What is the cash total?" % nat(amt)
        e = RULE + "%s ends in %d, so it rounds %s to <b>%s</b>." % (nat(amt), amt % 10, "up" if R > amt else "down", nat(R))
        cands = [ten, other, amt, (amt + 50) // 100 * 100, amt // 10 * 10, (amt + 9) // 10 * 10]
        it = mcq(q, R, cands, e)
        if nat(ten) in it["c"] and ten != R:
            it["e"] += " %s rounds to the nearest 10¢, but cash rounds to the nearest 5¢." % nat(ten)
        its.append(it)
    nm, he, his = P.next()
    its.append(mcq(fig(receipt_svg(748, "debit card")) + "%s pays for this by debit card. How much does %s pay?" % (nm, he),
                   748, [750, 745, 740],
                   "Card payments are not rounded. Only cash is rounded to the nearest 5¢. %s pays exactly <b>$7.48</b>." % cap(he)))
    nm, he, his = P.next()
    its.append(mcq(fig(receipt_svg(1633, "cash")) + "%s pays for this in cash. How much does %s pay?" % (nm, he),
                   1635, [1633, 1630, 1640],
                   RULE + "$16.33 ends in 3, so it rounds up to <b>$16.35</b>."))
    its.append(mcq("Which total stays the same when it is paid in cash?", "$4.35", ["$4.36", "$4.38", "$4.31"],
                   "A total that already ends in 0 or 5 does not change. <b>$4.35</b> ends in 5. "
                   "$4.36 becomes $4.35, $4.38 becomes $4.40 and $4.31 becomes $4.30.", fmt=str))
    assert round5(508) == 510 and round5(513) == 515 and round5(506) == 505 and round5(504) == 505
    its.append(mcq("Which total becomes $5.10 when it is paid in cash?", "$5.08", ["$5.13", "$5.06", "$5.04"],
                   "$5.08 ends in 8, so it rounds up to <b>$5.10</b>. $5.13 rounds up to $5.15. "
                   "$5.06 and $5.04 both round to $5.05.", fmt=str))
    for paid, amt in [(1000, 748), (2000, 1392), (500, 266), (2000, 1157), (5000, 3651), (10000, 7319)]:
        nm, he, his = P.next()
        R = round5(amt)
        assert R != amt
        other = R + 5 if R < amt else R - 5
        ch = paid - R
        q = ("%s’s total is %s. %s pays cash with %s. How much change does %s get?" % (nm, nat(amt), cap(he), money_word(paid), he))
        e = ("Round first: %s ends in %d, so the cash total is %s. " % (nat(amt), amt % 10, nat(R)) + count_up(R, paid)
             + " The change is <b>%s</b>." % nat(ch))
        it = mcq(q, ch, [paid - amt, paid - other, ch + 100 if R % 100 else None, R, ch + 10], e)
        if nat(paid - amt) in it["c"]:
            it["e"] += " %s forgets to round the total." % nat(paid - amt)
        its.append(it)
    nm, he, his = P.next()
    its.append(mcq("A total is $9.92. How much less does %s pay with cash than by card?" % nm,
                   "2¢", ["8¢", "3¢", "5¢"],
                   "By card: exactly $9.92. In cash: $9.92 ends in 2, so it rounds down to $9.90. "
                   "$9.92 − $9.90 = <b>2¢</b> less. 8¢ comes from rounding up to $10.", fmt=str))
    nm, he, his = P.next()
    its.append(mcq("A total is $6.38. How much more does %s pay with cash than by card?" % nm,
                   "2¢", ["3¢", "7¢", "8¢"],
                   "By card: exactly $6.38. In cash: $6.38 ends in 8, so it rounds up to $6.40. "
                   "$6.40 − $6.38 = <b>2¢</b> more. 3¢ comes from rounding down to $6.35.", fmt=str))
    assert len(its) == 20
    return {"title": "Cash rounding to the nearest 5¢ (card is exact)", "items": its}


# ============================================================ set 5: financial decisions and word problems
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    better = ["the pack", "the single ones", "They cost the same.", "You cannot tell."]

    # 1 better buy: pack
    nm, he, his = P.next()
    assert 4 * 125 == 500 and 500 > 400
    add("Juice boxes cost $1.25 each, or $4 for a pack of 4. %s needs 4 juice boxes. Which is the better buy?" % nm,
        "the pack of 4", ["4 single juice boxes", "They cost the same.", "You cannot tell."],
        "4 single boxes: $1.25 + $1.25 + $1.25 + $1.25 = $5. The pack costs $4. <b>The pack of 4</b> saves $1.", fmt=str)
    # 2 better buy: 2 for $3
    nm, he, his = P.next()
    assert 2 * 175 == 350 and 350 > 300
    add("At the Kelowna farmers’ market, peaches are $1.75 each or 2 for $3. %s wants 2 peaches. Which is the better buy?" % nm,
        "2 for $3", ["2 peaches at $1.75 each", "They cost the same.", "You cannot tell."],
        "2 peaches at $1.75 each: $1.75 + $1.75 = $3.50. 2 for $3 costs $3. <b>2 for $3</b> saves 50¢.", fmt=str)
    # 3 better buy trap: singles cheaper
    nm, he, his = P.next()
    assert 3 * 150 == 450 and 450 < 500
    add("Tennis balls cost $1.50 each, or $5 for a can of 3. %s needs 3 balls. Which is the better buy?" % nm,
        "3 single balls", ["the can of 3", "They cost the same.", "You cannot tell."],
        "3 single balls: $1.50 + $1.50 + $1.50 = $4.50. The can costs $5. <b>3 single balls</b> cost 50¢ less. "
        "A bigger pack is not always cheaper.", fmt=str)
    # 4 hockey cards box
    nm, he, his = P.next()
    assert 3 * 500 == 1500 and 1500 > 1200
    add("Hockey cards come in a pack of 10 for $5 or a box of 30 for $12. %s wants 30 cards. Which is the better buy?" % nm,
        "the box of 30", ["3 packs of 10", "They cost the same.", "1 pack of 10"],
        "30 cards is 3 packs: $5 + $5 + $5 = $15. The box costs $12. <b>The box of 30</b> saves $3. "
        "1 pack of 10 is cheaper, but it has only 10 cards.", fmt=str)
    # 5 add pledges (regroup cents)
    nm, he, his = P.next()
    nums = [500, 1000, 250, 175]
    assert sum(nums) == 1925 and forgot_dollar_add(nums) == 1825
    add("For the Terry Fox Run, %s collects $5, $10, $2.50 and $1.75. How much does %s collect in all?" % (nm, he),
        1925, [1825, 1750, 2025],
        "Dollars: $5 + $10 + $2 + $1 = $18. Cents: 50¢ + 75¢ = 125¢ = $1.25. $18 + $1.25 = <b>$19.25</b>. "
        "$18.25 forgets the dollar in 125¢.")
    # 6 saving: weeks
    nm, he, his = P.next()
    add("%s wants a lacrosse stick that costs $45. %s saves $5 each week. How many weeks will it take?" % (nm, cap(he)),
        "9 weeks", ["40 weeks", "5 weeks", "10 weeks"],
        "Count by 5s to 45: $5, $10, $15, $20, $25, $30, $35, $40, $45. That is <b>9 weeks</b>. "
        "40 comes from 45 − 5.", fmt=str)
    # 7 saving with a start
    nm, he, his = P.next()
    assert (4500 - 1000) // 500 == 7
    add("%s has $10. %s saves $5 each week for a $45 skateboard helmet. How many more weeks until %s can buy it?" % (nm, cap(he), he),
        "7 weeks", ["9 weeks", "35 weeks", "11 weeks"],
        "%s needs $45 − $10 = $35 more. Count by 5s to 35: 7 jumps. That is <b>7 weeks</b>. "
        "9 weeks forgets the $10 %s already has." % (cap(he), he), fmt=str)
    # 8 how much more (subtract with regrouping)
    nm, he, his = P.next()
    assert small_from_big(4500, 2800) == 2300
    add("%s wants a pair of hiking boots for $45. %s has $28. How much more money does %s need?" % (nm, cap(he), he),
        1700, [2300, 1500, 7300],
        "Count up: $28 + $2 = $30, $30 + $15 = $45. $2 + $15 = $17, so %s needs <b>$17</b> more. "
        "$23 takes the smaller digit from the bigger one. $15 forgets the jump from $28 to $30. $73 adds." % he)
    # 9 saving, not exact
    nm, he, his = P.next()
    assert 7 * 600 < 4500 <= 8 * 600
    add("%s saves $6 each week for a $45 soccer ball and jersey. How many weeks until %s has enough?" % (nm, he),
        "8 weeks", ["7 weeks", "39 weeks", "9 weeks"],
        "After 7 weeks: 7 × $6 = $42. That is not enough. After 8 weeks: 8 × $6 = $48. "
        "So it takes <b>8 weeks</b>. 7 weeks leaves %s $3 short." % nm, fmt=str)
    # 10 saving with a start, $4 a week
    nm, he, his = P.next()
    assert (3000 - 1800) // 400 == 3
    add("%s has $18. A bike light costs $30. %s saves $4 each week. After how many weeks can %s buy the light?" % (nm, cap(he), he),
        "3 weeks", ["12 weeks", "8 weeks", "4 weeks"],
        "%s needs $30 − $18 = $12 more. $4, $8, $12: that is <b>3 weeks</b>. 12 is the dollars, not the weeks." % cap(he), fmt=str)
    # 11 budget: two items, change
    nm, he, his = P.next()
    assert 875 + 650 == 1525 and 2000 - 1525 == 475
    add("On a class trip to Grouse Mountain, %s has $20. %s buys lunch for $8.75 and a postcard set for $6.50. "
        "How much money is left?" % (nm, cap(he)),
        475, [575, 1525, 525],
        "Cost: $8 + $6 = $14 and 75¢ + 50¢ = $1.25, so $15.25. " + count_up(1525, 2000) + " <b>$4.75</b> is left. "
        "$15.25 is what %s spent." % he)
    # 12 enough?
    nm, he, his = P.next()
    assert 795 + 350 == 1145 and 1200 - 1145 == 55
    add("%s has $12. %s wants a book for $7.95 and a bookmark for $3.50. Does %s have enough money?" % (nm, cap(he), he),
        "Yes, with 55¢ left.", ["No, %s needs 55¢ more." % he, "Yes, with $1.55 left.", "Yes, with 45¢ left."],
        "$7.95 + $3.50: $7.95 + 5¢ = $8, and $8 + $3.45 = $11.45. $11.45 is less than $12. "
        "$11.45 + 55¢ = $12, so <b>yes, with 55¢ left</b>. $1.55 comes from adding the cents without making a new dollar.", fmt=str)
    # 13 choose items from a price list
    nm, he, his = P.next()
    items = [("sketchbook", 950), ("paint set", 1275), ("brushes", 640), ("easel", 1680)]
    pr = dict(items)
    ok = pr["sketchbook"] + pr["brushes"]
    bad = [pr["sketchbook"] + pr["paint set"], pr["brushes"] + pr["easel"], pr["paint set"] + pr["easel"]]
    assert ok < 2000 and all(b > 2000 for b in bad)
    add(fig(price_svg(items, "art store")) + "%s has $20. Which 2 items can %s buy?" % (nm, he),
        "sketchbook and brushes", ["sketchbook and paint set", "brushes and easel", "paint set and easel"],
        "Sketchbook and brushes: $9.50 + $6.40 = <b>$15.90</b>, less than $20. "
        "Sketchbook and paint set: $22.25. Brushes and easel: $23.20. Paint set and easel: $29.55.", fmt=str)
    # 14 sale vs other store
    nm, he, his = P.next()
    add("A rain jacket costs $40 at one store, with $10 off. Another store sells it for $32. "
        "Where should %s buy it?" % nm,
        "the store with $10 off", ["the $32 store", "It costs the same.", "You cannot tell."],
        "$40 − $10 = $30. $30 is less than $32, so <b>the store with $10 off</b> is cheaper by $2.", fmt=str)
    # 15 BC Ferries snack, change
    nm, he, his = P.next()
    assert 685 + 240 == 925
    add("On the ferry to Vancouver Island, %s buys a sandwich for $6.85 and a juice for $2.40. %s pays with a $20 bill. "
        "How much change does %s get?" % (nm, cap(he), he),
        1075, [1175, 925, 1025],
        "Cost: $6.85 + $2.40 = $9.25. " + count_up(925, 2000) + " The change is <b>$10.75</b>. "
        "$11.75 forgets the dollar used for the cents.")
    # 16 save half
    nm, he, his = P.next()
    add("%s gets $6 each week. %s saves half and spends half. How much does %s save in 4 weeks?" % (nm, cap(he), he),
        1200, [2400, 300, 1000],
        "Half of $6 is $3. 4 weeks: $3 + $3 + $3 + $3 = <b>$12</b>. $24 is all the money, not half of it.")
    # 17 cash rounding at fruit stand
    nm, he, his = P.next()
    assert round5(738) == 740
    add("At an Okanagan fruit stand, %s buys cherries for $7.38. %s pays cash with a $10 bill. How much change does %s get?"
        % (nm, cap(he), he),
        260, [262, 360, 265],
        "Cash: $7.38 rounds up to $7.40. " + count_up(740, 1000) + " The change is <b>$2.60</b>. "
        "$2.62 forgets to round the total.")
    # 18 multiply cost per student
    nm, he, his = P.next()
    assert 23 * 400 == 9200
    add("The bus for a field trip to Stanley Park costs $4 for each student. 23 students go. What is the total cost?",
        9200, [2700, 8300, 9600],
        "23 × $4: 20 × $4 = $80 and 3 × $4 = $12. $80 + $12 = <b>$92</b>. "
        "$83 multiplies only the tens. $27 adds instead of multiplying.")
    # 19 pay with three $20 bills
    nm, he, his = P.next()
    assert 6000 - 4495 == 1505
    add("%s pays for rain boots that cost $44.95 with three $20 bills. How much change does %s get?" % (nm, he),
        1505, [1605, 1595, 2505],
        "Three $20 bills make $60. " + count_up(4495, 6000) + " The change is <b>$15.05</b>. "
        "$16.05 forgets the dollar used for the cents.")
    # 20 save or spend decision
    nm, he, his = P.next()
    assert 2000 + 4 * 500 == 4000
    add("%s has $20 and gets $5 each week. %s wants a $40 game. If %s spends nothing, after how many weeks can %s buy it?"
        % (nm, cap(he), he, he),
        "4 weeks", ["8 weeks", "20 weeks", "5 weeks"],
        "%s needs $40 − $20 = $20 more. $5, $10, $15, $20: that is <b>4 weeks</b>. "
        "8 weeks forgets the $20 %s already has." % (cap(he), he), fmt=str)
    assert len(its) == 20
    return {"title": "Better buys, saving up and word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    bills = ["B5", "B10", "B20", "B50", "B100"]
    walk = toks_of(("B20", 1), ("B5", 1), ("T", 1), ("Q", 2), ("D", 1))
    assert total(walk) == 2760
    return (
        "<h2>Canadian coins and bills</h2>"
        "<p>Know each coin by its value, not its size. The dime is the smallest coin, but it is worth more than the nickel. "
        "Canada has no pennies.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(bills, per_row=5, label="Canadian bills: $5, $10, $20, $50, $100") +
        "<figcaption>Bills: $5, $10, $20, $50 and $100.</figcaption></figure>"
        "<h2>Count money: bills first, then coins</h2>"
        "<p>Sort the money from biggest to smallest. Count the dollars, then count on the cents.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, per_row=6, gap=8, under=["$20", "$25", "$27", "25¢", "50¢", "60¢"],
                                              label="counting on: $20, $25, $27, then 25¢, 50¢, 60¢") +
        "<figcaption>$20, $25, $27. Then 25¢, 50¢, 60¢. Total: $27.60.</figcaption></figure>"
        + ex("Example", "Count 5 quarters and 3 dimes.",
             "25¢, 50¢, 75¢, 100¢, 125¢, then 135¢, 145¢, 155¢. 155¢ = $1.55.", "$1.55") +
        "<h2>Make an amount with the fewest coins and bills</h2>"
        "<p>$1.35 can be a loonie, a quarter and a dime, or 5 quarters and a dime, and more. "
        "For the <b>fewest</b> coins and bills, use the biggest one you can each time.</p>"
        "<h2>Make change by counting up</h2>"
        "<p>Start at the price. Count up to the next 10¢, then to the next dollar, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(765, 1000) +
        "<figcaption>Change from $10 for $7.65: 5¢ + 30¢ + $2 = $2.35.</figcaption></figure>"
        + ex("Example", "A backpack costs $27.95. Pay with a $50 bill. What is the change?",
             "$27.95 + 5¢ = $28. $28 + $2 = $30. $30 + $20 = $50. 5¢ + $2 + $20 = $22.05. Check: $27.95 + $22.05 = $50.", "$22.05")
        + "<h2>Cash rounding</h2>"
        "<p>There are no pennies, so a <b>cash</b> total is rounded to the nearest 5¢. "
        "A <b>card</b> payment (debit or credit) is not rounded.</p>"
        + table(["Total ends in", "Cash rounding", "Example"], [
            ["1 or 2", "down to 0", "$3.42 → $3.40"],
            ["3 or 4", "up to 5", "$3.43 → $3.45"],
            ["6 or 7", "down to 5", "$3.47 → $3.45"],
            ["8 or 9", "up to the next 10", "$3.48 → $3.50"],
            ["0 or 5", "no change", "$3.45 stays $3.45"],
        ]) +
        "<h2>Simple money decisions</h2>"
        "<p><b>Better buy:</b> find the cost of the same number of things. 4 juice boxes at $1.25 each cost $5, "
        "so a pack of 4 for $4 is the better buy. A bigger pack is not always cheaper, so always check.</p>"
        "<p><b>Saving up:</b> find how much more you need, then count by your savings. "
        "With $10 saved and $5 a week, a $45 item needs $35 more: 7 weeks.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["5 coins, so 5¢", "Count the value of each coin: 25¢, 50¢, 60¢, 65¢, 70¢"],
            ["A quarter is 20¢", "A quarter is 25¢. Four quarters make $1"],
            ["5 quarters and 3 dimes is 55¢", "155¢ is $1.55. Do not lose the dollar"],
            ["$10 − $7.65 = $3.35", "Count up: 5¢ + 30¢ + $2 = $2.35. One dollar was used to make the cents"],
            ["Cash change from $10 for $7.48 is $2.52", "Round first: $7.48 → $7.50 in cash, so the change is $2.50"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about money in BC?",
     "a": "The BC Grade 4 math curriculum includes financial literacy: monetary calculations, including making change with amounts to $100, and making simple financial decisions. Students count coins and bills, make change by counting up, and compare prices."},
    {"q": "How does cash rounding work in Canada?",
     "a": "Canada no longer uses pennies, so cash totals are rounded to the nearest 5¢: amounts ending in 1 or 2 round down, 3 or 4 round up to 5, 6 or 7 round down to 5, and 8 or 9 round up. Debit and credit card payments are charged the exact amount."},
    {"q": "How do you teach making change in Grade 4?",
     "a": "Count up from the price to the money paid: for $7.65 from $10, go to $7.70 (5¢), to $8 (30¢), then to $10 ($2), so the change is $2.35. Then check that price + change = money paid."},
    {"q": "Is money on the Grade 4 FSA?",
     "a": "The FSA numeracy section is based on the BC curriculum, which includes financial literacy, so money can appear in word problems. Counting money and making change also practise the adding and subtracting with decimals that students use throughout the test."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(34816)
    P = People(rnd)
    sets = [set_count(P, rnd), set_ways(P, rnd), set_change(P, rnd), set_rounding(P, rnd), set_words(P, rnd)]
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
            for c in it["c"] + [it["q"], it["e"]]:
                assert not re.search(r"\$\d+\.\d(?!\d)", re.sub(r"<[^>]+>", "", c)), c
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "money-and-making-change", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Money and Making Change",
        "seo_title": "Grade 4 Money and Making Change Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Money and making change",
        "domain": "Financial literacy",
        "standard_code": "Grade 4: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Financial literacy – monetary calculations, including making change with amounts to 100 dollars and making simple financial decisions",
        "meta_desc": "Free Grade 4 math worksheets on money for the BC curriculum: count Canadian coins and bills to $100, make amounts with the fewest coins, make change by counting up, round cash totals to the nearest 5¢, and choose the better buy or plan to save. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "To make change, count up from the price to the money paid: $7.65 → $7.70 → $8 → $10 is 5¢ + 30¢ + $2 = $2.35.",
        "key_sub": "Cash totals round to the nearest 5¢ because Canada has no pennies; card payments are exact. A quarter is 25¢, and 125¢ in coins is $1.25.",
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
