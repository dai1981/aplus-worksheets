# -*- coding: utf-8 -*-
"""
BC Grade 3 Math: Money to $100 (BC Mathematics Curriculum, Financial literacy:
fluency with coins and bills to 100 dollars, and earning and payment)
  python3 tools/gen_cabc_math_g3_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Writing money: under $1 as 45¢, whole dollars as $7, other amounts as $7.65 (never $7.6, never $7.65¢).
Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1 (11 sides, gold colour), toonie $2.
No pennies: cash totals are rounded to the nearest 5¢; card payments are exact.
Bills: $5 blue, $10 purple, $20 green, $50 red, $100 brown. Coins and bills are simple labelled shapes.
Coin, bill, number line and receipt drawing copied from gen_cabc_math_g4_money.py.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-3")
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
    """always with cents: 700 -> '$7.00' (price tags and receipts)"""
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


def draw_tok(t, cx, cy, show=True):
    """one coin or one bill, labelled with its value (show=False: no value written on a coin)"""
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
    return shape + (text(cx, cy + fs * 0.36, lab(VAL[t]), fs) if show else "")


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None, show=True):
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
            s.append(draw_tok(t, x + w / 2, y + hh / 2, show))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(W, H, "".join(s), label or ("money: " + group(toks)))


def coin_svg(t):
    """one coin, value written on it (for naming the coin)"""
    w, h = tok_size(t)
    return svg_wrap(w + 8, h + 8, draw_tok(t, (w + 8) / 2, (h + 8) / 2), "one coin worth %s" % lab(VAL[t]))


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


def change_cands(paid, price):
    """real change mistakes, most common first"""
    r = paid - price
    c = []
    if paid > 100 and price % 100:
        c.append(r + 100)           # $5 − $2.75: took $2 from $5 = $3 and kept the cents: forgot the dollar used for the cents
    if price % 10:
        c.append(r + 10)            # 65¢ + 45¢ "makes 100": 6 + 4 = 10 and 5 + 5 = 10, but that is 110¢
    c += [price]                    # gave the price, not the change
    if price % 100 == 0:
        c.append(r + 100)           # counted the start number too: $6, $7, $8, $9, $10 is 5 numbers
    c += [r - 100, r + 25, r - 25, r + 500]
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


def tags_svg(items, kind):
    """a row of tags: [('feed the cat', 25), ...]; kind is 'price list' or 'chore chart'"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 20, 78) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, nat(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), kind + ": " + ", ".join("%s %s" % (n, nat(p)) for n, p in items))


def receipt_svg(amount, how):
    """a small receipt: total and how it was paid"""
    W, H = 200, 92
    b = ["<rect x='4' y='4' width='%d' height='%d' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (W - 8, H - 8, INK),
         text(W / 2, 30, "RECEIPT", 15),
         "<line x1='16' y1='40' x2='%d' y2='40' stroke='%s' stroke-width='1' stroke-dasharray='4 3'/>" % (W - 16, INK),
         text(18, 62, "Total", 16, "start"), text(W - 18, 62, dol(amount), 18, "end", GREEN),
         text(18, 80, "Paid:", 14, "start"), text(W - 18, 80, how, 14, "end")]
    return svg_wrap(W, H, "".join(b), "receipt: total %s, paid %s" % (dol(amount), how))


# ============================================================ set 1: coins and bills
def set_names(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=nat):
        its.append(mcq(q, right, wrong, e, fmt))

    tips = {
        "L": ("the loonie", ["the toonie", "the quarter", "the dime"],
              "This is the <b>loonie</b>. It is gold in colour, has 11 sides and is worth $1."),
        "T": ("the toonie", ["the loonie", "the quarter", "the nickel"],
              "This is the <b>toonie</b>. It has a silver ring and a gold centre and is worth $2."),
        "D": ("the dime", ["the nickel", "the quarter", "the loonie"],
              "This is the <b>dime</b>, worth 10¢. It is the smallest coin, but it is worth more than the nickel."),
        "N": ("the nickel", ["the dime", "the quarter", "the toonie"],
              "This is the <b>nickel</b>, worth 5¢. It is bigger than the dime, but worth less."),
        "Q": ("the quarter", ["the nickel", "the dime", "the loonie"],
              "This is the <b>quarter</b>, worth 25¢. It is bigger than the nickel and the dime."),
    }
    for t in ["L", "T", "Q", "D", "N"]:
        right, wrong, e = tips[t]
        s(fig(coin_svg(t)) + "What is the name of this coin?", right, wrong, e, fmt=str)
    s("How much is a quarter worth?", 25, [20, 50, 10],
      "A quarter is worth <b>25¢</b>, not 20¢. Four quarters make $1: 25¢, 50¢, 75¢, 100¢.")
    s("How much is a toonie worth?", 200, [100, 2, 20],
      "A toonie is worth <b>$2</b>. The loonie is the $1 coin. 2¢ and 20¢ are cents, but a toonie is two dollars.")
    s(fig(money_svg(["D", "N"], gap=14, under=["dime", "nickel"], label="coins: a dime (smaller) and a nickel (bigger)"))
      + "The nickel is bigger than the dime. Which coin is worth more?",
      "the dime", ["the nickel", "They are worth the same.", "You cannot tell."],
      "The <b>dime</b> is worth 10¢. The nickel is worth 5¢. The size of a coin does not tell you its value.", fmt=str)
    s(fig(money_svg(["Q", "T", "D", "L"], gap=10, under=["quarter", "toonie", "dime", "loonie"],
                    label="coins: quarter, toonie, dime, loonie"))
      + "Which coin is worth the most?",
      "the toonie", ["the loonie", "the quarter", "the dime"],
      "Dime 10¢, quarter 25¢, loonie $1, toonie $2. The <b>toonie</b> is worth the most.", fmt=str)
    s("How many nickels make a quarter?", "5", ["25", "4", "2"],
      "Count by 5s to 25: 5¢, 10¢, 15¢, 20¢, 25¢. That is <b>5</b> nickels. 4 nickels make only 20¢.", fmt=str)
    s("How many quarters make $1?", "4", ["5", "25", "10"],
      "Count by 25s: 25¢, 50¢, 75¢, 100¢. 100¢ = $1, so <b>4</b> quarters. 5 is right only if a quarter were 20¢.", fmt=str)
    s("How many dimes make $1?", "10", ["100", "4", "5"],
      "$1 is 100¢. Count by 10s: 10¢, 20¢, 30¢ … 100¢. That is <b>10</b> dimes. 100 is the number of cents.", fmt=str)
    s("How many quarters make a toonie?", "8", ["4", "10", "2"],
      "Four quarters make $1. A toonie is $2, so 4 + 4 = <b>8</b> quarters. "
      "4 makes only $1. 10 is right only if a quarter were 20¢.", fmt=str)
    s("How many loonies make $5?", "5", ["1", "500", "10"],
      "A loonie is $1. $1, $2, $3, $4, $5: <b>5</b> loonies. One $5 bill is worth the same.", fmt=str)
    s("How many $5 bills make $20?", "4", ["5", "15", "20"],
      "Count by 5s: $5, $10, $15, $20. That is <b>4</b> bills. 15 comes from 20 − 5.", fmt=str)
    s(fig(money_svg(["B10", "B10"], gap=12, label="two $10 bills"))
      + "Which bill is worth the same as these two bills?",
      "a $20 bill", ["a $10 bill", "a $5 bill", "a $50 bill"],
      "$10 + $10 = $20. So <b>a $20 bill</b> is worth the same.", fmt=str)
    s("How many $10 bills make $100?", "10", ["100", "5", "9"],
      "Count by 10s: $10, $20, $30 … $100. That is <b>10</b> bills. 100 is the dollars, not the number of bills.", fmt=str)
    s("Which coins are worth the same as a quarter?", "2 dimes and 1 nickel",
      ["2 dimes", "1 dime and 1 nickel", "3 dimes"],
      "10¢ + 10¢ + 5¢ = 25¢. So <b>2 dimes and 1 nickel</b> make a quarter. "
      "2 dimes make 20¢: that is the mistake “a quarter is 20¢.” 1 dime and 1 nickel make 15¢. 3 dimes make 30¢.", fmt=str)
    nm, he, his = P.next()
    s(fig(money_svg(["Q", "Q", "Q", "L"], gap=10, label="three quarters and one loonie"))
      + "%s says 3 quarters are worth more than 1 loonie because 3 coins are more than 1 coin. Is %s right?" % (nm, he),
      "No. 3 quarters are 75¢, less than $1.",
      ["Yes. 3 coins are more than 1 coin.", "No. They are worth the same.", "Yes. 3 quarters are $3."],
      "3 quarters: 25¢, 50¢, 75¢. A loonie is $1 = 100¢. 75¢ is less than 100¢. "
      "Count the <b>value</b> of the coins, not how many coins there are.", fmt=str)
    s(fig(money_svg(["B5", "B20", "B10", "B50"], gap=10, label="bills: $5, $20, $10, $50"))
      + "Put these bills in order from least to greatest.",
      "$5, $10, $20, $50", ["$50, $20, $10, $5", "$5, $20, $10, $50", "$10, $5, $20, $50"],
      "$5 is the least, then $10, then $20, then $50: <b>$5, $10, $20, $50</b>.", fmt=str)
    assert len(its) == 20
    return {"title": "Coins and bills: names and values", "items": its}


# ============================================================ set 2: count collections to $100
def set_count(P, rnd):
    its = []
    groups = [
        [("D", 3), ("N", 2)],
        [("Q", 2), ("D", 1)],
        [("Q", 3), ("N", 2)],
        [("Q", 1), ("D", 4), ("N", 1)],
        [("Q", 3), ("D", 2)],
        [("L", 1), ("Q", 2), ("D", 1)],
        [("Q", 4), ("D", 3)],
        [("T", 1), ("Q", 1), ("N", 2)],
        [("T", 2), ("L", 1), ("D", 3)],
        [("B5", 1), ("L", 2), ("Q", 1)],
        [("B5", 1), ("T", 1), ("Q", 3), ("D", 1)],
        [("B10", 1), ("T", 1), ("Q", 2)],
        [("B10", 1), ("B5", 1), ("L", 3)],
        [("B20", 1), ("B5", 1), ("T", 2), ("D", 2)],
        [("B20", 2), ("B10", 1), ("Q", 3)],
        [("B50", 1), ("B10", 1), ("T", 1), ("Q", 1)],
        [("B50", 1), ("B20", 1), ("B5", 1), ("L", 1), ("D", 3)],
        [("B20", 3), ("B10", 1), ("B5", 2), ("T", 2)],
        [("B50", 1), ("B20", 2), ("T", 1), ("Q", 2)],
        [("B50", 1), ("B20", 2), ("B5", 1), ("T", 2)],
    ]
    mixed = {3, 7, 10, 13, 16, 18}
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
        if coins_only and nat(m_count(toks)) in it["c"]:
            it["e"] += " %s counts the coins, not their value." % nat(m_count(toks))
        if not (coins_only and T < 300) and nat(m_each_dollar(toks)) in it["c"]:
            it["e"] += " %s counts every coin and bill as $1." % nat(m_each_dollar(toks))
        if "T" in toks and nat(m_toonie1(toks)) in it["c"]:
            it["e"] += " %s counts a toonie as $1, but a toonie is $2." % nat(m_toonie1(toks))
        its.append(it)
    assert len(its) == 20
    return {"title": "Count coins and bills to $100", "items": its}


# ============================================================ set 3: make amounts in different ways
def gtxt(vals):
    return ", ".join(lab(v) for v in sorted(vals, reverse=True))


def fewest(target, pieces):
    best = {0: []}
    for a in range(5, target + 1, 5):
        opts = [best[a - c] + [c] for c in pieces if a - c in best]
        if opts:
            best[a] = min(opts, key=len)
    return best[target]


COINS = [5, 10, 25, 100, 200]
CENT_COINS = [5, 10, 25]
BILLS = [500, 1000, 2000, 5000]


def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None):
        assert sum(right) == target, (target, right)
        for w in wrong:
            assert sum(w) != target, (target, w)
        q = (stem or "Which money makes %s?") % nat(target)
        e = ("<b>%s</b> = %s. " % (gtxt(right), nat(target)) + " ".join(
            "%s = %s." % (gtxt(w), nat(sum(w))) for w in wrong))
        its.append(mcq(q, gtxt(right), [gtxt(w) for w in wrong], e, fmt=str))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> = %s, not %s. " % (gtxt(right), nat(sum(right)), nat(target))
             + "The others all make %s." % nat(target))
        its.append(mcq("Which of these does <b>not</b> make %s?" % nat(target), gtxt(right), [gtxt(w) for w in wrong], e, fmt=str))

    def how_few(target, pieces, wrong, extra, word="coins"):
        f = fewest(target, pieces)
        n = len(f)
        one = word[:-1]
        ch = lambda k: "%d %s" % (k, one if k == 1 else word)
        q = "What is the smallest number of %s you can use to make %s?" % (word, nat(target))
        e = "Use the biggest one you can each time: %s = %s. That is <b>%s</b>. %s" % (gtxt(f), nat(target), ch(n), extra)
        its.append(mcq(q, ch(n), [ch(k) for k in wrong], e, fmt=str))

    def which_fewest(target, pieces, wrong, word="coins"):
        f = fewest(target, pieces)
        for w in wrong:
            assert sum(w) == target and len(w) > len(f), (w, f)
        e = ("All of these make %s. <b>%s</b> uses only %d %s: start with the biggest one you can each time."
             % (nat(target), gtxt(f), len(f), "pieces of money" if " and " in word else word))
        its.append(mcq("Which uses the fewest %s to make %s?" % (word, nat(target)), gtxt(f), [gtxt(w) for w in wrong], e, fmt=str))

    def same_as(toks, right, rv, wrong):
        assert rv == total(toks)
        q = fig(money_svg(toks, per_row=6)) + "Which is worth the same as this money?"
        e = count_on(toks) + " So <b>%s</b> is worth the same." % right
        its.append(mcq(q, right, wrong, e, fmt=str))

    def how_many(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e, fmt=str))

    which(40, [25, 10, 5], [[25, 10], [10, 10, 10], [25, 25]])
    same_as(["D"] * 5, "two quarters", 50, ["one quarter", "five nickels", "one loonie"])
    how_many("How many quarters make $2?", "8", ["2", "10", "4"],
             "Four quarters make $1. $2 is 2 dollars, so 4 + 4 = <b>8</b> quarters. "
             "10 is right only if a quarter were 20¢.")
    how_few(60, CENT_COINS, [2, 4, 6], "6 dimes also make 60¢, but that is more coins.")
    which_not(50, [25, 10, 10], [[25, 25], [10, 10, 10, 10, 10], [25, 10, 10, 5]])
    which(125, [100, 25], [[100, 10, 10], [25, 25, 25, 25], [100, 25, 10]])
    nm, he, his = P.next()
    which(45, [25, 10, 10], [[25, 10, 5], [25, 25, 5], [10, 10, 5]],
          stem=nm + " has 3 coins. Together they make %s. Which coins does " + he + " have?")
    same_as(["B5", "B5"], "one $10 bill", 1000, ["one $5 bill", "two toonies", "one $20 bill"])
    how_many("How many dimes make $1.50?", "15", ["150", "10", "5"],
             "Ten dimes make $1. 50¢ is 5 more dimes. 10 + 5 = <b>15</b> dimes. "
             "150 is the number of cents. 10 forgets the 50¢.")
    which_fewest(75, CENT_COINS, [[25, 25, 10, 10, 5], [10, 10, 10, 10, 10, 10, 10, 5], [25, 10, 10, 10, 10, 10]])
    how_few(250, COINS, [2, 4, 10], "A toonie is $2. Two quarters make 50¢. Loonies or dimes would take more coins.")
    which(1200, [1000, 200], [[1000, 100], [500, 500, 100], [1000, 200, 200]])
    which_not(2000, [1000, 500, 200, 200], [[1000, 1000], [500, 500, 500, 500], [1000, 500, 200, 200, 100]])
    which_fewest(1500, BILLS + [100, 200], [[500, 500, 500], [1000, 200, 200, 100], [500, 500, 200, 200, 100]],
                 word="bills and coins")
    how_many("How many $10 bills make $60?", "6", ["60", "5", "12"],
             "Count by 10s: $10, $20, $30, $40, $50, $60. That is <b>6</b> bills. "
             "60 is the dollars, not the bills. 12 is the number of $5 bills.")
    nm, he, his = P.next()
    which(3500, [2000, 1000, 500], [[2000, 1000, 200], [1000, 1000, 1000], [2000, 500, 500]],
          stem=nm + " has 3 bills. Together they make %s. Which bills does " + he + " have?")
    same_as(["B20"] * 5, "one $100 bill", 10000, ["one $50 bill", "five $10 bills", "one $20 bill"])
    which_not(500, [200, 200, 25, 25, 25], [[200, 200, 100], [100, 100, 100, 100, 100], [200, 100, 100, 25, 25, 25, 25]])
    how_few(4500, BILLS, [4, 5, 9], "$20 + $20 = $40, and $5 more is $45. Nine $5 bills take more bills.", word="bills")
    nm, he, his = P.next()
    which(5600, [5000, 500, 100], [[5000, 500, 200], [5000, 500], [2000, 2000, 500, 100]],
          stem=nm + " pays exactly %s for a pair of soccer cleats. Which money could " + he + " use?")
    assert len(its) == 20
    return {"title": "Make amounts in different ways", "items": its}


# ============================================================ set 4: make change by counting up
def money_word(paid):
    return {100: "a loonie", 200: "a toonie", 500: "a $5 bill", 1000: "a $10 bill", 2000: "a $20 bill",
            5000: "a $50 bill", 10000: "a $100 bill"}[paid]


def set_change(P, rnd):
    its = []
    jobs = [(100, 40, "a pencil", True), (100, 65, "an apple", False), (100, 85, "a freezie", False),
            (200, 145, "a granola bar", False), (500, 350, "a bag of popcorn", True), (500, 275, "a hot chocolate", False),
            (1000, 600, "a chapter book", False), (1000, 725, "a kite", True), (1000, 480, "a skipping rope", False),
            (2000, 1500, "a puzzle", False), (2000, 1250, "a toque", True), (2000, 1675, "a pair of swim goggles", False),
            (5000, 3500, "a pair of shin pads", True), (5000, 4200, "a backpack", False), (5000, 2850, "a board game", False),
            (10000, 6500, "a pair of running shoes", True), (10000, 8800, "a pair of skates", False),
            (10000, 7450, "a scooter", False)]
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
        if pr % 100 == 0 and nat(r + 100) in it["c"]:
            it["e"] += " %s counts the starting number as a jump." % nat(r + 100)
        if nat(pr) in it["c"]:
            it["e"] += " %s is the price, not the change." % nat(pr)
        its.append(it)
    nm, he, his = P.next()
    assert 25 + 10 + 5 == 40 and 20 + 20 == 40
    its.append(mcq("%s buys an orange for 60¢ and pays with a loonie. Which coins could be the change?" % nm,
                   "a quarter, a dime and a nickel", ["a quarter and two dimes", "a quarter and a nickel", "two quarters"],
                   "Count up from 60¢: 60¢ + 40¢ = $1, so the change is 40¢. 25¢ + 10¢ + 5¢ = <b>40¢</b>. "
                   "A quarter and two dimes is 45¢, not 40¢: a quarter is 25¢, not 20¢.", fmt=str))
    nm, he, his = P.next()
    its.append(mcq("A sandwich costs $4.90. %s pays with a $10 bill. About how much change will %s get?" % (nm, he),
                   "about $5", ["about $6", "about $4", "about $1"],
                   "$4.90 is close to $5. $10 − $5 = $5, so the change is <b>about $5</b>. "
                   "(Exactly: $4.90 + 10¢ = $5, $5 + $5 = $10, so $5.10.)", fmt=str))
    assert len(its) == 20
    return {"title": "Make change by counting up", "items": its}


# ============================================================ set 5: earning and paying, word problems
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    # 1 earning: what it means
    add("Which of these is a way to <b>earn</b> money?",
        "doing chores for pay", ["buying a snack", "paying with a debit card", "putting money in a piggy bank"],
        "To earn money is to get money for work. <b>Doing chores for pay</b> is earning. "
        "Buying and paying are spending. A piggy bank keeps money you already have.", fmt=str)
    # 2 paying: ways to pay
    add("Which of these can you use to pay at a store?",
        "a debit card", ["a price tag", "a receipt", "a shopping list"],
        "You can pay with cash (coins and bills) or with a card. <b>A debit card</b> takes the money from a bank account. "
        "A price tag shows the cost. A receipt shows what you paid.", fmt=str)
    # 3 repeated earning
    nm, he, his = P.next()
    add("%s earns $2 each time %s walks the neighbour’s dog. %s walks the dog 4 times. How much does %s earn?"
        % (nm, he, cap(he), he),
        800, [600, 400, 1000],
        "$2 + $2 + $2 + $2 = <b>$8</b>. $6 comes from adding 2 + 4.")
    # 4 allowance by weeks
    nm, he, his = P.next()
    add("%s gets $5 each week for helping at home. How much does %s get in 3 weeks?" % (nm, he),
        1500, [800, 500, 2000],
        "Count by 5s: $5, $10, $15. That is <b>$15</b>. $8 comes from adding 5 + 3.")
    # 5 lemonade stand
    nm, he, his = P.next()
    add("%s sells lemonade for 50¢ a cup. %s sells 6 cups. How much money does %s earn?" % (nm, cap(he), he),
        300, [30, 250, 600],
        "Two cups make $1. 6 cups is 3 pairs: <b>$3</b>. 30¢ counts each cup as 5¢. $2.50 is only 5 cups. $6 counts each cup as $1.")
    # 6 chore chart total
    chores = [("make the bed", 50), ("feed the cat", 25), ("take out recycling", 100), ("water plants", 25)]
    tot = sum(p for n, p in chores)
    assert tot == 200 and 50 + 20 + 100 + 20 == 190
    nm, he, his = P.next()
    add(fig(tags_svg(chores, "chore chart")) + "%s does each chore on the chart once. How much does %s earn?" % (nm, he),
        tot, [190, 4, 175],
        "50¢ + 25¢ + $1 + 25¢: the two quarters make 50¢, and 50¢ + 50¢ = $1. $1 + $1 = <b>$2</b>. "
        "$1.90 counts a quarter as 20¢. 4¢ counts the chores, not the money.")
    # 7 earn two jobs, add
    nm, he, his = P.next()
    add("%s earns $10 for raking leaves and $7.50 for washing the car. How much does %s earn in all?" % (nm, he),
        1750, [1700, 250, 850],
        "$10 + $7 = $17. Add the 50¢: <b>$17.50</b>. $17 forgets the cents. $2.50 subtracts. "
        "$8.50 adds $1 instead of $10.")
    # 8 cash rounding up
    nm, he, his = P.next()
    assert round5(498) == 500
    add(fig(receipt_svg(498, "cash")) + "%s pays for this in cash. How much does %s pay?" % (nm, he),
        500, [498, 495, 490],
        "Canada has no pennies, so a cash total is rounded to the nearest 5¢. "
        "$4.98 ends in 8, so it rounds up to <b>$5</b>.")
    # 9 card exact
    nm, he, his = P.next()
    add(fig(receipt_svg(637, "debit card")) + "%s pays for this by debit card. How much does %s pay?" % (nm, he),
        637, [635, 640, 630],
        "Card payments are not rounded. Only cash is rounded to the nearest 5¢. %s pays exactly <b>$6.37</b>." % cap(he))
    # 10 cash rounding down
    nm, he, his = P.next()
    assert round5(342) == 340
    add("%s buys a bag of apples for $3.42. %s pays in cash. How much does %s pay?" % (nm, cap(he), he),
        340, [342, 345, 350],
        "Cash totals are rounded to the nearest 5¢. $3.42 ends in 2, so it rounds down to <b>$3.40</b>.")
    # 11 cash rounding up to 5
    nm, he, his = P.next()
    assert round5(853) == 855
    add("At a Kamloops farmers’ market, %s’s total is $8.53. %s pays in cash. How much does %s pay?" % (nm, cap(he), he),
        855, [853, 850, 860],
        "Cash totals are rounded to the nearest 5¢. $8.53 ends in 3, so it rounds up to <b>$8.55</b>.")
    # 12 how much more
    nm, he, his = P.next()
    assert small_from_big(2400, 1500) == 1100
    add("%s wants a book set for $24. %s has saved $15. How much more money does %s need?" % (nm, cap(he), he),
        900, [1100, 3900, 1000],
        "Count up: $15 + $5 = $20, $20 + $4 = $24. $5 + $4 = <b>$9</b>. "
        "$11 takes the smaller digit from the bigger one. $39 adds.")
    # 13 saving weeks
    nm, he, his = P.next()
    add("%s saves $5 each week for a $30 lacrosse ball and net. How many weeks will it take?" % nm,
        "6 weeks", ["25 weeks", "5 weeks", "7 weeks"],
        "Count by 5s to 30: $5, $10, $15, $20, $25, $30. That is <b>6 weeks</b>. 25 comes from 30 − 5.", fmt=str)
    # 14 total of two items (regroup cents)
    nm, he, his = P.next()
    assert 475 + 250 == 725
    add("At the PNE in Vancouver, %s buys a hot dog for $4.75 and a drink for $2.50. How much does %s spend?" % (nm, he),
        725, [625, 225, 775],
        "Dollars: $4 + $2 = $6. Cents: 75¢ + 50¢ = 125¢ = $1.25. $6 + $1.25 = <b>$7.25</b>. "
        "$6.25 forgets the dollar in 125¢.")
    # 15 change at a bakery
    nm, he, his = P.next()
    add("At a bakery in Victoria, %s buys a muffin for $2.85. %s pays with a $5 bill. How much change does %s get?"
        % (nm, cap(he), he),
        215, [315, 225, 285],
        count_up(285, 500) + " The change is <b>$2.15</b>. $3.15 forgets the dollar used to make the cents.")
    # 16 earn then spend
    nm, he, his = P.next()
    add("%s earns $12 at a family garage sale. %s spends $7.50 on a book. How much money is left?" % (nm, cap(he)),
        450, [550, 1950, 750],
        count_up(750, 1200) + " <b>$4.50</b> is left. $5.50 forgets the dollar used to make the cents. $19.50 adds.")
    # 17 class collection
    add("For a field trip to Science World, each student brings $3 for the bus. 8 students bring their money. How much is that?",
        2400, [1100, 2100, 2700],
        "8 groups of $3: $3, $6, $9, $12, $15, $18, $21, $24. That is <b>$24</b>. $11 adds 8 + 3.")
    # 18 hockey stick change from two $20 bills
    nm, he, his = P.next()
    assert 4000 - 3450 == 550
    add("%s pays for a hockey stick that costs $34.50 with two $20 bills. How much change does %s get?" % (nm, he),
        550, [650, 1450, 3450],
        "Two $20 bills make $40. " + count_up(3450, 4000) + " The change is <b>$5.50</b>. "
        "$6.50 forgets the dollar used to make the cents. $14.50 uses one $20 bill only.")
    # 19 toonies and loonies, enough?
    nm, he, his = P.next()
    assert 7 * 200 + 3 * 100 == 1700 and 7 * 100 + 3 * 100 == 1000
    add("%s has 7 toonies and 3 loonies. Can %s buy a $16 kite?" % (nm, he),
        "Yes, with $1 left.", ["No, %s needs $6 more." % he, "Yes, with $4 left.", "No, %s needs $1 more." % he],
        "7 toonies: $2, $4, $6, $8, $10, $12, $14. Add 3 loonies: $15, $16, $17. $17 is more than $16, "
        "so <b>yes, with $1 left</b>. “No, %s needs $6 more” counts each toonie as $1." % he, fmt=str)
    # 20 earn weekly, how many weeks (not exact)
    nm, he, his = P.next()
    assert 6 * 300 < 2000 <= 7 * 300
    add("%s earns $3 each week for chores. %s wants a $20 model kit. How many weeks until %s has enough?" % (nm, cap(he), he),
        "7 weeks", ["6 weeks", "17 weeks", "5 weeks"],
        "Count by 3s: $3, $6, $9, $12, $15, $18. After 6 weeks %s has $18, not enough. "
        "After 7 weeks %s has $21. So it takes <b>7 weeks</b>. 17 comes from 20 − 3." % (he, he), fmt=str)
    assert len(its) == 20
    return {"title": "Earning and paying: chores, cash or card", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    bills = ["B5", "B10", "B20", "B50", "B100"]
    walk = toks_of(("B10", 1), ("T", 1), ("Q", 2), ("D", 1))
    assert total(walk) == 1260
    return (
        "<h2>Canadian coins and bills</h2>"
        "<p>Know each coin by its value, not its size. The dime is the smallest coin, but it is worth more than the nickel. "
        "Canada has no pennies.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(bills, per_row=5, label="Canadian bills: $5, $10, $20, $50, $100") +
        "<figcaption>Bills: $5, $10, $20, $50 and $100.</figcaption></figure>"
        + table(["To make $1", "To make $2"], [
            ["4 quarters", "8 quarters or 1 toonie"],
            ["10 dimes", "20 dimes"],
            ["20 nickels", "2 loonies"],
        ]) +
        "<h2>Count money: biggest first</h2>"
        "<p>Sort the money from biggest to smallest. Count the dollars. Then count on the cents.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, per_row=5, gap=8, under=["$10", "$12", "25¢", "50¢", "60¢"],
                                              label="counting on: $10, $12, then 25¢, 50¢, 60¢") +
        "<figcaption>$10, $12. Then 25¢, 50¢, 60¢. Total: $12.60.</figcaption></figure>"
        + ex("Example", "Count 4 quarters and 3 dimes.",
             "25¢, 50¢, 75¢, 100¢. Then 110¢, 120¢, 130¢. 130¢ = $1.30.", "$1.30") +
        "<h2>Make an amount in different ways</h2>"
        "<p>50¢ can be 2 quarters, or 5 dimes, or 1 quarter, 2 dimes and 1 nickel. "
        "For the <b>fewest</b> coins, use the biggest coin you can each time.</p>"
        "<h2>Make change by counting up</h2>"
        "<p>Start at the price. Count up to the next 10¢, then to the next dollar, then to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(275, 500) +
        "<figcaption>Change from $5 for $2.75: 5¢ + 20¢ + $2 = $2.25.</figcaption></figure>"
        + ex("Example", "A toque costs $12.50. Pay with a $20 bill. What is the change?",
             "$12.50 + 50¢ = $13. $13 + $7 = $20. 50¢ + $7 = $7.50. Check: $12.50 + $7.50 = $20.", "$7.50")
        + "<h2>Earning and paying</h2>"
        "<p>To <b>earn</b> money is to get money for work, like doing chores or selling lemonade. "
        "To <b>pay</b>, you can use cash (coins and bills) or a card (debit or credit).</p>"
        "<p>There are no pennies, so a <b>cash</b> total is rounded to the nearest 5¢. "
        "A <b>card</b> payment is not rounded.</p>"
        + table(["Total ends in", "Cash rounding", "Example"], [
            ["1 or 2", "down to 0", "$3.42 → $3.40"],
            ["3 or 4", "up to 5", "$3.43 → $3.45"],
            ["6 or 7", "down to 5", "$3.47 → $3.45"],
            ["8 or 9", "up to the next 10", "$3.48 → $3.50"],
            ["0 or 5", "no change", "$3.45 stays $3.45"],
        ]) +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["5 coins, so 5¢", "Count the value of each coin: 25¢, 50¢, 60¢, 65¢, 70¢"],
            ["A quarter is 20¢", "A quarter is 25¢. Four quarters make $1"],
            ["The nickel is bigger, so it is worth more", "A dime (10¢) is worth more than a nickel (5¢)"],
            ["4 quarters and 3 dimes is 30¢", "130¢ is $1.30. Do not lose the dollar"],
            ["$5 − $2.75 = $3.25", "Count up: 5¢ + 20¢ + $2 = $2.25. One dollar was used to make the cents"],
        ])
    )


FAQ = [
    {"q": "What money skills are in the BC Grade 3 math curriculum?",
     "a": "Grade 3 financial literacy in BC is fluency with coins and bills to $100, and earning and payment. Students count Canadian coins and bills, make the same amount in different ways, make change and talk about how people earn and pay."},
    {"q": "How can I help my child count Canadian coins?",
     "a": "Sort the coins from biggest value to smallest, then count on: by 25s for quarters, by 10s for dimes and by 5s for nickels. Remind them that the small dime is worth more than the bigger nickel, and a quarter is 25¢, not 20¢."},
    {"q": "Why are cash totals rounded to the nearest 5 cents in Canada?",
     "a": "Canada stopped making pennies, so cash totals are rounded to the nearest 5¢: endings 1 and 2 round down, 3 and 4 round up to 5, 6 and 7 round down to 5, and 8 and 9 round up. Debit and credit card payments are charged the exact amount."},
    {"q": "What does “earning and payment” mean in Grade 3?",
     "a": "Earning is getting money for work, such as doing chores or running a lemonade stand. Payment is how we pay for things, with cash (coins and bills) or with a debit or credit card."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(53812)
    P = People(rnd)
    sets = [set_names(P, rnd), set_count(P, rnd), set_ways(P, rnd), set_change(P, rnd), set_words(P, rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-3", "slug": "money-to-100-dollars", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money to $100: Coins, Bills, Making Change and Earning",
        "seo_title": "Grade 3 Money to $100 Math Worksheets (BC Curriculum, Free, Answer Key)",
        "short_title": "Money to $100",
        "domain": "Financial literacy",
        "standard_code": "Grade 3: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/3/core",
        "standard_text": "Financial literacy – fluency with coins and bills to 100 dollars, and earning and payment",
        "meta_desc": "Free Grade 3 math worksheets on money for the BC curriculum: name Canadian coins and bills, count money to $100, make amounts in different ways, make change by counting up, and solve earning and paying problems with cash or card. 100 questions with an answer key.",
        "key_big": "Count money by value, not by the number of coins: biggest first, then count on. A quarter is 25¢.",
        "key_sub": "To make change, count up from the price: $2.75 → $2.80 → $3 → $5 is 5¢ + 20¢ + $2 = $2.25. Cash totals round to the nearest 5¢; card payments are exact.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|counting|price|chore|bills|coins|two|three)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
