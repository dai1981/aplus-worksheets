# -*- coding: utf-8 -*-
"""
CA Grade 3 Math: Money and Making Change (Ontario Mathematics Curriculum 2020, Grade 3: F1.1)
  python3 tools/gen_ca_math_g3_money.py
Grade 3 works with whole-dollar amounts and amounts of less than one dollar only, so every amount here is
either under $1 (written 45¢) or a whole number of dollars (written $7). There are no $2.35-type amounts.
Canadian coins: nickel 5¢, dime 10¢ (the smallest coin), quarter 25¢, loonie $1 (11 sides, gold colour),
toonie $2 (silver ring, gold centre). No pennies. Bills: $5 blue, $10 purple, $20 green, $50 red, $100 brown.
Coins and bills are simple labelled shapes (no real designs).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

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
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def nat(c):
    """45 -> '45¢', 700 -> '$7'. Grade 3: under $1 or whole dollars only."""
    assert c > 0, c
    assert c < 100 or c % 100 == 0, c
    return lab(c)


def ok_amt(c):
    return isinstance(c, int) and c > 0 and (c < 100 or c % 100 == 0)


def mval(s):
    """value in cents of a money text, or None"""
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^\$(\d+)$", s)
    if m:
        return int(m.group(1)) * 100
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


# ------------------------------------------------------------ explanations
def count_on(toks):
    toks = srt(toks)
    T = total(toks)
    s, run = 0, []
    for t in toks:
        s += VAL[t]
        run.append(lab(s))
    if T >= 100 and T % 100 == 0 and all(VAL[t] >= 100 for t in toks):
        return "Count the dollars, biggest first: %s. That is <b>%s</b>." % (", ".join(run), nat(T))
    if T == 100:
        run[-1] = "100¢"
        return "Start with the biggest coin: %s. 100¢ = <b>$1</b>." % ", ".join(run)
    return "Start with the biggest coin and count on: %s. That is <b>%s</b>." % (", ".join(run), nat(T))


# ------------------------------------------------------------ typical mistakes (all computed)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


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


def m_each_dollar(toks):
    """counted every coin and bill as $1"""
    return 100 * len(toks)


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
            if fmt is nat and not ok_amt(c):
                continue
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


def coin_svg(t):
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
    pts, s = [price], price
    if paid <= 100:
        if s % 10:
            s += 10 - s % 10
            pts.append(s)
    else:
        nxt = s + (1000 - s % 1000) if s % 1000 else s
        if s % 1000 and nxt < paid:
            s = nxt
            pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid
    return pts


def count_up(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (lab(a), lab(b - a), lab(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(lab(j) for j in jumps), nat(ch))
    return "Count up from %s to %s: %s.%s" % (lab(price), lab(paid), ", ".join(steps), tail)


def change_cands(paid, price):
    """real change mistakes, most common first"""
    r = paid - price
    if paid <= 100:
        c = []
        if price % 10:
            c.append(r + 10)        # 65¢ + 45¢ "makes 100": 6 + 4 = 10 and 5 + 5 = 10, but that is 110¢
        c += [price, r - 5, r + 5, r - 10, r + 25]
        return [x for x in c if 0 < x < 100 and x % 5 == 0]
    c = [price, r + 100, paid + price, r - 100]   # cost, counted the start number too, added, one short
    if paid == 2000 and price < 1000:
        c.insert(1, r - 1000)                     # forgot the $10 jump from $10 to $20
    return [x for x in c if x > 0]


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting up; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [130, 160][:len(pts) - 1]
    x0, y0 = 30, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 30
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, lab(p), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + lab(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting up from %s to %s" % (lab(price), lab(paid)))


def price_svg(items, title):
    """a row of price tags: [('cookie', 40), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 18, 70) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, nat(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, nat(p)) for n, p in items))


# ============================================================ set 1: names and values
def set_names(P, rnd):
    its = []

    def s(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    tips = {
        "L": ("loonie", ["toonie", "quarter", "dime"],
              "This is a <b>loonie</b>. It is gold in colour, has 11 sides and is worth $1."),
        "T": ("toonie", ["loonie", "quarter", "nickel"],
              "This is a <b>toonie</b>. It has a silver ring and a gold centre and is worth $2. Loonie is $1, toonie is $2."),
        "D": ("dime", ["nickel", "quarter", "loonie"],
              "This is a <b>dime</b>, worth 10¢. It is the smallest coin, but it is worth more than a nickel."),
        "N": ("nickel", ["dime", "quarter", "toonie"],
              "This is a <b>nickel</b>, worth 5¢. It is bigger than a dime, but worth less."),
        "Q": ("quarter", ["dime", "nickel", "loonie"],
              "This is a <b>quarter</b>, worth 25¢. Four quarters make $1."),
    }
    for t in ["L", "T", "D", "N", "Q"]:
        right, wrong, e = tips[t]
        s(fig(coin_svg(t)) + "What is the name of this coin?", right, wrong, e)
    s("How much is a quarter worth?", 25, [20, 50, 10],
      "A quarter is worth <b>25¢</b>. It is not 20¢: four quarters make 100¢, and 4 × 25¢ = 100¢.")
    s("How much is a dime worth?", 10, [5, 25, 1],
      "A dime is worth <b>10¢</b>. Ten dimes make $1. The nickel (5¢) is bigger, but the dime is worth more.")
    s("How much is a nickel worth?", 5, [10, 25, 1],
      "A nickel is worth <b>5¢</b>. Two nickels make a dime.")
    s("How much is a loonie worth?", 100, [200, 1, 25],
      "A loonie is worth <b>$1</b> (100¢). The toonie is the $2 coin.")
    s("How much is a toonie worth?", 200, [100, 2, 2000],
      "A toonie is worth <b>$2</b>. It is worth the same as two loonies.")
    s("Which coin has 11 sides?", "the loonie", ["the toonie", "the quarter", "the dime"],
      "The <b>loonie</b> has 11 sides and is gold in colour. The other coins are round.")
    s(fig(money_svg(["D", "N"], gap=14, under=["dime", "nickel"], label="coins: a dime (smaller) and a nickel (bigger)"))
      + "The nickel is bigger than the dime. Which coin is worth more?",
      "the dime", ["the nickel", "They are worth the same.", "You cannot tell."],
      "The <b>dime</b> is worth 10¢. The nickel is worth 5¢. Size does not tell you the value.")
    toks = ["Q", "D", "L", "N"]
    s(fig(money_svg(toks, gap=10, under=["quarter", "dime", "loonie", "nickel"], label="coins: quarter, dime, loonie, nickel"))
      + "Which coin is worth the least?",
      "the nickel", ["the dime", "the quarter", "the loonie"],
      "Nickel 5¢, dime 10¢, quarter 25¢, loonie $1. The <b>nickel</b> is worth the least, even though the dime is smaller.")
    s("How many nickels make a dime?", "2", ["5", "10", "1"],
      "A dime is 10¢ and a nickel is 5¢. 5¢ + 5¢ = 10¢, so <b>2</b> nickels make a dime.")
    s("How many nickels make a quarter?", "5", ["25", "4", "2"],
      "Count by 5s to 25: 5¢, 10¢, 15¢, 20¢, 25¢. That is <b>5</b> nickels. 4 nickels make only 20¢.")
    s("How many quarters make $1?", "4", ["5", "25", "10"],
      "Count by 25s: 25¢, 50¢, 75¢, 100¢. 100¢ = $1, so <b>4</b> quarters. 5 would be right only if a quarter were 20¢.")
    s("How many dimes make $1?", "10", ["100", "1", "4"],
      "Count by 10s: 10¢, 20¢, 30¢ … 100¢. That is <b>10</b> dimes.")
    s("How many cents are in $1?", "100", ["10", "1000", "25"],
      "$1 = <b>100</b> cents. That is why 4 quarters (4 × 25¢) or 10 dimes (10 × 10¢) make $1.")
    s("How many loonies make a toonie?", "2", ["1", "20", "200"],
      "A loonie is $1 and a toonie is $2. $1 + $1 = $2, so <b>2</b> loonies make a toonie.")
    s("How many $5 bills make $20?", "4", ["5", "15", "2"],
      "Count by 5s: $5, $10, $15, $20. That is <b>4</b> bills. 15 comes from 20 − 5.")
    assert len(its) == 20
    return {"title": "Coins and bills: names and values", "items": its}


# ============================================================ set 2: count the money
def set_count(P, rnd):
    its = []
    groups = [
        [("D", 4)], [("N", 6)], [("Q", 3)], [("Q", 1), ("D", 2)], [("D", 3), ("N", 1)],
        [("Q", 2), ("D", 1), ("N", 1)], [("Q", 1), ("D", 1), ("N", 3)], [("Q", 1), ("D", 3)],
        [("Q", 1), ("D", 4), ("N", 1)], [("Q", 2), ("D", 3), ("N", 1)], [("Q", 3), ("D", 1), ("N", 2)],
        [("Q", 2), ("D", 4)], [("Q", 3), ("D", 2), ("N", 1)],
        [("L", 3)], [("T", 3)], [("T", 2), ("L", 1)], [("T", 3), ("L", 2)],
        [("B5", 1), ("T", 2), ("L", 1)], [("B10", 1), ("B5", 1), ("T", 1)], [("B20", 1), ("B10", 1), ("B5", 1), ("L", 2)],
    ]
    mixed = {6, 9, 11, 12, 16, 17, 19}
    stems = ["How much money is shown?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s backpack. How much is it?", "What is the total?",
             "%s puts this money in a piggy bank. How much is in the bank?"]
    seen_t = set()
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert ok_amt(T) and T not in seen_t, T
        seen_t.add(T)
        assert len(toks) <= 8
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if any(t.startswith("B") for t in toks) and "coins" in st:
            st = stems[4]
        if st.count("%s") == 2:
            st = st % (nm, his if "backpack" in st else he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = ("Put the money in order, biggest value first. " if i in mixed else "") + count_on(toks)
        if len(set(toks)) == 1:
            t, n = toks[0], len(toks)
            v = VAL[t]
            e = "Each %s is %s. Count by %s: %s. That is <b>%s</b>." % (
                ONE[t], lab(v), lab(v), ", ".join(lab(v * k) for k in range(1, n + 1)), nat(T))
        if i < 3:
            e += " Count the value of each coin, not the number of coins."
        if T < 100 or T == 100:
            cands = [m_quarter20(toks), m_count(toks), m_swap(toks), m_same_step(toks), m_skip(toks, -1),
                     m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
            if i % 2:
                cands = [m_count(toks)] + cands
        else:
            cands = [m_toonie1(toks), m_count(toks), m_each_dollar(toks), m_skip(toks, -1), m_twice(toks, -1),
                     m_same_step(toks), m_skip(toks, 0)]
            if i % 2:
                cands = [m_each_dollar(toks)] + cands
        its.append(mcq(q, T, cands, e))
    assert len(its) == 20
    return {"title": "Count coins and bills", "items": its}


# ============================================================ set 3: different ways to make an amount
def gtxt(vals):
    return ", ".join(lab(v) for v in sorted(vals, reverse=True))


def fewest(target, coins):
    best = {0: []}
    step = min(coins)
    for a in range(step, target + 1, step):
        opts = [best[a - c] + [c] for c in coins if a - c in best]
        best[a] = min(opts, key=len)
    return best[target]


CENT_COINS = [5, 10, 25]
DOLLAR_COINS = [100, 200]
BILLS = [500, 1000, 2000]


def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None):
        assert sum(right) == target, (target, right)
        for w in wrong:
            assert sum(w) != target, (target, w)
        q = (stem or "Which coins make %s?") % lab(target)
        e = ("<b>%s</b> = %s. " % (gtxt(right), lab(target)) + " ".join(
            "%s = %s." % (gtxt(w), lab(sum(w))) for w in wrong))
        its.append(mcq(q, gtxt(right), [gtxt(w) for w in wrong], e))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> = %s, not %s. " % (gtxt(right), lab(sum(right)), lab(target))
             + "The others all make %s." % lab(target))
        its.append(mcq("Which of these does <b>not</b> make %s?" % lab(target), gtxt(right), [gtxt(w) for w in wrong], e))

    def how_few(target, coins, wrong, extra):
        f = fewest(target, coins)
        n = len(f)
        ch = lambda k: "%d coin" % k if k == 1 else "%d coins" % k
        e = "Use the biggest coin you can each time: %s = %s. That is <b>%s</b>. %s" % (gtxt(f), lab(target), ch(n), extra)
        its.append(mcq("What is the fewest coins you can use to make %s?" % lab(target), ch(n), [ch(k) for k in wrong], e))

    def which_fewest(target, coins, wrong, word="coins"):
        f = fewest(target, coins)
        for w in wrong:
            assert sum(w) == target and len(w) > len(f)
        e = ("All of these make %s. <b>%s</b> uses only %d %s: start with the biggest one you can."
             % (lab(target), gtxt(f), len(f), word))
        its.append(mcq("Which uses the fewest %s to make %s?" % (word, lab(target)), gtxt(f), [gtxt(w) for w in wrong], e))

    def same_as(toks, right, wrong):
        T = total(toks)
        q = fig(money_svg(toks)) + "Which is worth the same as this money?"
        e = count_on(toks) + " So <b>%s</b> is worth the same." % right
        its.append(mcq(q, right, wrong, e))

    which(35, [25, 10], [[25, 5], [10, 10, 10], [25, 25]])
    which(50, [25, 25], [[25, 10, 10], [10, 10, 10, 10], [25, 10, 5]])
    assert total(["N", "N"]) == 10
    same_as(["N", "N"], "one dime", ["one nickel", "one quarter", "two dimes"])
    assert total(["Q"] * 4) == 100
    same_as(["Q"] * 4, "one loonie", ["one quarter", "one toonie", "four dimes"])
    assert total(["L", "L"]) == 200
    same_as(["L", "L"], "one toonie", ["one loonie", "two quarters", "one $5 bill"])
    how_few(30, CENT_COINS, [1, 3, 6], "There is no 30¢ coin, so 1 coin is not possible. Three dimes work, but 2 coins is fewer.")
    which_not(60, [25, 25, 5], [[25, 25, 10], [25, 10, 10, 10, 5], [10, 10, 10, 10, 10, 10]])
    nm, he, his = P.next()
    which(45, [25, 10, 10], [[25, 10, 5], [25, 25, 5], [10, 10, 10]],
          stem=nm + " has 3 coins. Together they make %s. Which coins does " + he + " have?")
    which(75, [25, 25, 25], [[25, 25, 10, 10], [25, 25, 10], [25, 10, 10, 10, 10, 5]])
    which_fewest(40, CENT_COINS, [[10, 10, 10, 10], [25, 5, 5, 5], [10, 10, 10, 5, 5]])
    how_few(65, CENT_COINS, [3, 5, 7], "Three coins can make 60¢ or 75¢, but not 65¢. Six dimes and a nickel is 7 coins.")
    nm, he, his = P.next()
    which(70, [25, 25, 10, 10], [[25, 25, 10, 5], [25, 10, 10, 10], [25, 25, 25, 5]],
          stem=nm + " has 4 coins. Together they make %s. Which coins does " + he + " have?")
    which_not(100, [25, 25, 25, 10, 10], [[25, 25, 25, 25], [25, 25, 25, 10, 10, 5], [25, 25, 10, 10, 10, 10, 10]])
    which(90, [25, 25, 25, 10, 5], [[25, 25, 25, 10], [25, 25, 10, 10, 10], [25, 25, 25, 5, 5]])
    which(300, [200, 100], [[200, 200], [100, 100], [100, 100, 100, 100]])
    which_not(500, [200, 200, 200], [[200, 200, 100], [200, 100, 100, 100], [500]])
    assert total(["T"] * 5) == 1000
    same_as(["T"] * 5, "one $10 bill", ["one $5 bill", "one $20 bill", "five loonies"])
    how_few(700, DOLLAR_COINS, [7, 3, 5], "Seven loonies work, but that is 7 coins. Three toonies make only $6.")
    which_fewest(3500, BILLS, [[1000, 1000, 1000, 500], [2000, 500, 500, 500], [1000, 1000, 500, 500, 500]], word="bills")
    nm, he, his = P.next()
    which(2500, [1000, 1000, 500], [[2000, 500, 500], [1000, 500, 500], [2000, 1000, 500]],
          stem=nm + " has 3 bills. Together they make %s. Which bills does " + he + " have?")
    assert len(its) == 20
    return {"title": "Make amounts in different ways", "items": its}


# ============================================================ set 4: make change by counting up
def set_change(P, rnd):
    its = []
    cents = [(65, "a pen", True), (40, "an eraser", False), (85, "a bottle of water", True), (55, "a bag of pretzels", False),
             (20, "a sticker", False), (35, "a pencil topper", True), (70, "a notepad", False), (45, "a glue stick", False),
             (90, "a ruler", False), (15, "a balloon", False)]
    dollars = [(500, 300, "a skipping rope", False), (1000, 600, "a pack of hockey cards", False),
               (1000, 700, "a flying disc", True), (2000, 1300, "a soccer ball", True), (2000, 800, "a pair of mitts", True),
               (2000, 1500, "a board game", False), (1000, 400, "a colouring book", False), (2000, 1100, "a toque", False)]
    money_word = {100: "a loonie", 500: "a $5 bill", 1000: "a $10 bill", 2000: "a $20 bill"}

    def one(paid, pr, thing, line):
        nm, he, his = P.next()
        r = paid - pr
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, nat(pr), cap(he), money_word[paid], he)
        if line:
            q = fig(change_line(pr, paid, show=False)) + q + " Count up on the number line."
        e = count_up(pr, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (nat(r), nat(pr), nat(r), nat(paid))
        it = mcq(q, r, change_cands(paid, pr), e)
        if paid > 100 and r + 100 != pr and nat(r + 100) in it["c"]:
            it["e"] += " Count the jumps from %s. Do not count %s itself: that gives %s." % (nat(pr), nat(pr), nat(r + 100))
        its.append(it)

    for pr, thing, line in cents:
        one(100, pr, thing, line)
    nm, he, his = P.next()
    its.append(mcq("A bag of crackers costs 45¢. %s pays with a loonie. About how much change will %s get?" % (nm, he),
                   "about 50¢", ["about 5¢", "about $1", "about 25¢"],
                   "45¢ is close to 50¢. $1 − 50¢ = 50¢, so the change is <b>about 50¢</b>. (Exactly: 45¢ + 55¢ = $1.)",
                   fmt=str))
    for paid, pr, thing, line in dollars:
        one(paid, pr, thing, line)
    nm, he, his = P.next()
    its.append(mcq("%s buys a book for $9 with a $20 bill. Is the change more or less than $10?" % nm,
                   "more than $10", ["less than $10", "exactly $10", "exactly $9"],
                   "$9 is less than $10, so the change from $20 is more than $10. Exactly: $9 + $1 = $10, $10 + $10 = $20, "
                   "so the change is $11. That is <b>more than $10</b>.", fmt=str))
    assert len(its) == 20
    return {"title": "Make change by counting up", "items": its}


# ============================================================ set 5: shopping problems
SNACKS = [("apple", 25), ("juice box", 50), ("popcorn", 35), ("cookie", 40), ("granola bar", 45)]
BOOKFAIR = [("book", 800), ("poster", 400), ("bookmark", 200), ("pencil", 100)]


def set_words(P, rnd):
    its = []
    sp = dict(SNACKS)
    bp = dict(BOOKFAIR)

    def add(q, right, cands, e, fmt=nat):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    assert sp["popcorn"] + sp["juice box"] == 85
    add(fig(price_svg(SNACKS, "snack sale")) + "At the school snack sale, %s buys popcorn and a juice box. "
        "How much does %s spend?" % (nm, he), 85, [15, 75, 95],
        "35¢ + 50¢: 30¢ + 50¢ = 80¢, and 80¢ + 5¢ = <b>85¢</b>. 15¢ is the difference, not the total.")
    nm, he, his = P.next()
    assert 100 - (sp["cookie"] + sp["apple"]) == 35
    add(fig(price_svg(SNACKS, "snack sale")) + "At the snack sale, %s buys a cookie and an apple. %s pays with a loonie. "
        "How much change does %s get?" % (nm, cap(he), he), 35, [65, 45, 25],
        "Cost: 40¢ + 25¢ = 65¢. " + count_up(65, 100) + " The change is <b>35¢</b>. 65¢ is the cost, not the change.")
    nm, he, his = P.next()
    add("At the snack sale, a granola bar costs 45¢. %s pays with 2 quarters. How much change does %s get?" % (nm, he),
        5, [45, 55, 10],
        "2 quarters = 25¢ + 25¢ = 50¢. Count up: 45¢ + 5¢ = 50¢. The change is <b>5¢</b>. "
        "55¢ is the change from $1, but %s paid only 50¢." % nm)
    nm, he, his = P.next()
    assert 3 * 10 + 2 * 5 == 40 and 3 * 5 + 2 * 10 == 35
    add("%s has 3 dimes and 2 nickels. %s wants a granola bar for 45¢. Does %s have enough money?" % (nm, cap(he), he),
        "No, %s needs 5¢ more." % he, ["Yes, with 5¢ left.", "No, %s needs 10¢ more." % he, "Yes, %s has exactly 45¢." % he],
        "Dimes: 10¢, 20¢, 30¢. Nickels: 35¢, 40¢. %s has 40¢. 40¢ + 5¢ = 45¢, so <b>no, %s needs 5¢ more</b>. "
        "10¢ more comes from mixing up the dime and the nickel." % (nm, he), fmt=str)
    nm, he, his = P.next()
    assert bp["book"] + bp["poster"] == 1200
    add(fig(price_svg(BOOKFAIR, "book fair")) + "At the book fair, %s buys a book and a poster. How much does %s spend?"
        % (nm, he), 1200, [400, 1300, 1100],
        "$8 + $4: $8 + $2 = $10, and $10 + $2 = <b>$12</b>. $4 is the difference, not the total.")
    nm, he, his = P.next()
    assert 2000 - 1200 == 800
    add(fig(price_svg(BOOKFAIR, "book fair")) + "At the book fair, %s buys a book and a poster. %s pays with a $20 bill. "
        "How much change does %s get?" % (nm, cap(he), he), 800, [1200, 900, 3200],
        "Cost: $8 + $4 = $12. " + count_up(1200, 2000) + " The change is <b>$8</b>. $12 is the cost, not the change.")
    nm, he, his = P.next()
    add("At the book fair, bookmarks cost $2 each. %s buys 3 bookmarks. How much does %s pay?" % (nm, he),
        600, [500, 400, 200],
        "3 bookmarks: $2 + $2 + $2 = <b>$6</b>. $5 comes from adding 2 + 3. $4 is only 2 bookmarks.")
    nm, he, his = P.next()
    add("%s has saved $15. %s buys a book for $9. How much money is left?" % (nm, cap(he)),
        600, [2400, 700, 900],
        count_up(900, 1500) + " <b>$6</b> is left. Check: $9 + $6 = $15. $24 adds instead of taking away.")
    nm, he, his = P.next()
    add("%s wants a book that costs $12. %s has $7. How much more money does %s need?" % (nm, cap(he), he),
        500, [1900, 600, 400],
        count_up(700, 1200) + " %s needs <b>$5</b> more. $19 adds the two amounts." % cap(he))
    nm, he, his = P.next()
    add(fig(price_svg(SNACKS, "snack sale")) + "%s has a loonie. Can %s buy a juice box, popcorn and a cookie at the snack sale?"
        % (nm, he), "No, they cost more than $1.",
        ["Yes, they cost less than $1.", "Yes, they cost exactly $1.", "No, they cost more than $2."],
        "Estimate: 50¢ + 35¢ is already 85¢. Add 40¢ more and it is more than 100¢. "
        "So <b>no, they cost more than $1</b> (but less than $2).", fmt=str)
    nm, he, his = P.next()
    toks = toks_of(("Q", 4), ("L", 3))
    assert total(toks) == 400
    add(fig(money_svg(toks, per_row=7)) + "For the Terry Fox Run, %s brings these coins to give. How much does %s give?"
        % (nm, he), 400, [m_count(toks), m_each_dollar(toks), 300],
        "Loonies: $1, $2, $3. Four quarters make $1. $3 + $1 = <b>$4</b>. $7 counts every coin as $1. "
        "$3 forgets the quarters.")
    nm, he, his = P.next()
    add("At the snack sale, %s buys a muffin for 75¢ with a loonie. How much change does %s get?" % (nm, he),
        25, change_cands(100, 75), count_up(75, 100) + " The change is <b>25¢</b>, one quarter.")
    nm, he, his = P.next()
    add("At the book fair, a poster costs $4. %s pays with a $5 bill. How much change does %s get?" % (nm, he),
        100, [900, 400, 200],
        "Count up: $4 + $1 = $5. The change is <b>$1</b>, one loonie. $9 adds instead of taking away.")
    nm, he, his = P.next()
    assert 2 * 40 == 80
    add("At the snack sale, cookies cost 40¢ each. %s buys 2 cookies and pays with a loonie. How much change does %s get?"
        % (nm, he), 20, [80, 60, 30],
        "2 cookies: 40¢ + 40¢ = 80¢. Count up: 80¢ + 20¢ = $1. The change is <b>20¢</b>. 60¢ is the change for only 1 cookie.")
    nm, he, his = P.next()
    assert 2000 - 2 * 600 == 800
    add("At the book fair, %s buys 2 chapter books for $6 each. %s pays with a $20 bill. How much change does %s get?"
        % (nm, cap(he), he), 800, [1400, 1200, 900],
        "Cost: $6 + $6 = $12. " + count_up(1200, 2000) + " The change is <b>$8</b>. $14 is the change for only 1 book.")
    nm, he, his = P.next()
    assert 1000 + 200 - 900 == 300
    add("%s has a $10 bill and a toonie. %s buys a book for $9. How much money does %s have left?" % (nm, cap(he), he),
        300, [100, 400, 2100],
        "A $10 bill and a toonie make $12. Count up: $9 + $1 = $10, $10 + $2 = $12. <b>$3</b> is left. "
        "$1 forgets the toonie.")
    nm, he, his = P.next()
    add("Pizza Day is every Friday. A slice costs $2. %s buys a slice every Friday for 4 weeks. How much does %s spend?"
        % (nm, he), 800, [600, 1000, 200],
        "$2, $4, $6, $8. 4 slices cost <b>$8</b>. $6 comes from adding 2 + 4. $10 would be 5 weeks.")
    nm, he, his = P.next()
    add("The class field trip to the science centre costs $15. %s pays with a $20 bill. How much change does %s get?"
        % (nm, he), 500, [3500, 1500, 600],
        count_up(1500, 2000) + " The change is <b>$5</b>. Check: $15 + $5 = $20.")
    nm, he, his = P.next()
    right = [25, 10, 5]
    wrong = [[25, 10], [10, 10, 10], [25, 25]]
    assert sum(right) == 100 - 60 and all(sum(w) != 40 for w in wrong)
    add("%s buys an orange for 60¢ and pays with a loonie. Which coins could be the change?" % nm,
        gtxt(right), [gtxt(w) for w in wrong],
        "Count up: 60¢ + 40¢ = $1, so the change is 40¢. <b>25¢, 10¢, 5¢</b> = 40¢. "
        "25¢, 10¢ = 35¢. 10¢, 10¢, 10¢ = 30¢. 25¢, 25¢ = 50¢.", fmt=str)
    nm, he, his = P.next()
    assert 6 * 50 == 300
    add("For a class snack sale, %s’s class sells freezies for 50¢ each. They sell 6 freezies. How much money do they make?"
        % nm, 300, [3000, 56, 600],
        "Two freezies make $1. 6 freezies make 3 pairs, so $1 + $1 + $1 = <b>$3</b>. "
        "56¢ adds 50 + 6. $6 counts each freezie as $1.")
    assert len(its) == 20
    return {"title": "Shopping problems: snack sale and book fair", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    bills = ["B5", "B10", "B20", "B50", "B100"]
    walk = toks_of(("Q", 2), ("D", 1), ("N", 1))
    assert total(walk) == 65
    return (
        "<h2>Canadian coins and bills</h2>"
        "<p>Know each coin by its name and its value. Size does not tell you the value: the dime is the smallest coin, "
        "but it is worth more than the nickel.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2. There are no pennies.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(bills, per_row=5, label="Canadian bills: $5, $10, $20, $50, $100") +
        "<figcaption>Bills: $5, $10, $20, $50 and $100.</figcaption></figure>"
        + table(["Coin", "Value", "Good to know"], [
            ["nickel", "5¢", "2 nickels = 1 dime"],
            ["dime", "10¢", "10 dimes = $1"],
            ["quarter", "25¢", "4 quarters = $1"],
            ["loonie", "$1", "11 sides, gold colour"],
            ["toonie", "$2", "2 loonies = 1 toonie"],
        ]) +
        "<h2>Count the money, biggest first</h2>"
        "<p>Put the coins in order, biggest value first. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=10, under=["25¢", "50¢", "60¢", "65¢"],
                                              label="counting on: 25¢, 50¢, 60¢, 65¢") +
        "<figcaption>Quarters 25¢, 50¢. Dime 60¢. Nickel 65¢.</figcaption></figure>"
        + ex("Example", "Count a $5 bill, 2 toonies and a loonie.",
             "$5, then $7, $9, then $10.", "$10") +
        "<h2>Make the same amount in different ways</h2>"
        "<p>50¢ can be 25¢ + 25¢, or 25¢ + 10¢ + 10¢ + 5¢, or 5 dimes. "
        "For the <b>fewest coins</b>, use the biggest coin you can each time.</p>"
        "<h2>Make change by counting up</h2>"
        "<p>Start at the price. Count up to the next 10¢, then to $1. Add the jumps. "
        "For whole dollars, count up to the next $10, then to the money paid.</p>"
        "<figure class='sn-fig'>" + change_line(65, 100) +
        "<figcaption>Change from $1 for 65¢: 5¢ + 30¢ = 35¢.</figcaption></figure>"
        + ex("Example", "A pair of mitts costs $8. Pay with a $20 bill. What is the change?",
             "$8 + $2 = $10. $10 + $10 = $20. $2 + $10 = $12. Check: $8 + $12 = $20.", "$12")
        + "<p><b>Estimate first.</b> 45¢ is about 50¢, so the change from $1 is about 50¢. The exact change is 55¢.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The nickel is bigger, so it is worth more", "Read the value: the small dime is 10¢, the nickel is 5¢"],
            ["4 coins, so 4¢", "Count the value of each coin: 25¢, 50¢, 60¢, 65¢"],
            ["A quarter is 20¢", "A quarter is 25¢. Four quarters make $1"],
            ["Change from $1 for 65¢ is 45¢", "Count up: 65¢ + 5¢ = 70¢, 70¢ + 30¢ = $1. The change is 35¢"],
            ["The change is the price", "The change is what you get back: price + change = money paid"],
        ])
    )


FAQ = [
    {"q": "What do Grade 3 students learn about money in Ontario?",
     "a": "In the Ontario math curriculum (Financial Literacy, F1.1), Grade 3 students estimate and calculate the change for simple cash purchases, using whole-dollar amounts and amounts under $1. They also name Canadian coins and bills and count collections of money."},
    {"q": "Why are there no pennies in Canada?",
     "a": "Canada stopped giving out pennies in 2013. When you pay with cash, the total is rounded to the nearest 5¢, so the nickel is the smallest coin students count."},
    {"q": "How do you teach making change in Grade 3?",
     "a": "Count up from the price to the money paid: for 65¢ from $1, go 65¢ to 70¢ (5¢), then 70¢ to $1 (30¢), so the change is 35¢. Then check that price + change = money paid."},
    {"q": "Is money on the Grade 3 EQAO math test?",
     "a": "The Grade 3 EQAO math assessment is based on the Ontario math curriculum, which includes Financial Literacy. Counting money and making change also practises the adding and subtracting skills students need for the test."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(33809)
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
                assert not re.search(r"\$\d+\.\d", re.sub(r"<[^>]+>", "", c)), c
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-3", "slug": "money-and-making-change", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money and Making Change: Canadian Coins, Bills and Counting Up",
        "seo_title": "Grade 3 Money Worksheets: Canadian Coins and Making Change (Ontario)",
        "short_title": "Money and Making Change",
        "domain": "Financial Literacy",
        "standard_code": "Grade 3: F1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Estimate and calculate the change required for various simple cash transactions involving whole-dollar amounts and amounts of less than one dollar",
        "meta_desc": "Free Grade 3 math worksheets on money: name Canadian coins and bills, count nickels, dimes, quarters, loonies and toonies, make amounts in different ways, and make change from $1, $5, $10 and $20 by counting up. Snack sale and book fair word problems, 100 questions with an answer key. Follows the Ontario curriculum and helps with EQAO practice.",
        "key_big": "To make change, count up from the price to the money paid.",
        "key_sub": "For 65¢ paid with a loonie: 65¢ to 70¢ is 5¢, 70¢ to $1 is 30¢, so the change is 35¢. Count coins by value, not size: the small dime (10¢) is worth more than the bigger nickel (5¢).",
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
