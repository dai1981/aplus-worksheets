# -*- coding: utf-8 -*-
"""
AU Year 2 Maths: Money (Australian Curriculum v9.0, AC9M2N06)
  python3 tools/gen_au_maths_y2_money.py
All amounts are whole numbers of cents (int). Year 2 keeps one unit in a calculation:
cents up to 100c (written 45c; 100c is written $1) or whole dollars up to $20 (written $7).
No $2.35 notation (dollars and cents together is Year 3, AC9M3M06).
Australian coins: 5c, 10c, 20c, 50c (12-sided), $1, $2 (the $2 coin is smaller than the $1 coin;
the 50c coin is the biggest). Notes: $5, $10, $20. No 1c or 2c coins.
Coins and notes are simple labelled shapes (no real designs).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

# ------------------------------------------------------------ money facts
ORDER = ["N20", "N10", "N5", "C200", "C100", "C50", "C20", "C10", "C5"]   # biggest value first
VAL = {"N20": 2000, "N10": 1000, "N5": 500, "C200": 200, "C100": 100, "C50": 50, "C20": 20, "C10": 10, "C5": 5}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius (in proportion to the real coins: $2 smaller than $1; 50c the biggest), colours, label size
COIN = {"C5": (16, SILVER, 14), "C10": (19, SILVER, 14), "C20": (23, SILVER, 15), "C50": (25, SILVER, 15),
        "C100": (20, GOLD, 15), "C200": (17, GOLD, 14)}
NOTE = {"N5": ("#efcfe3", "#8a3a6e"), "N10": ("#c4dcf2", "#1f5f99"), "N20": ("#f5c9b3", "#a33a1c")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%dc" % v


def m(c):
    """Year 2 money text: 45 -> '45c', 100 -> '$1', 700 -> '$7' (never dollars and cents together)"""
    assert c > 0, c
    if c < 100:
        return "%dc" % c
    assert c % 100 == 0 and c <= 2000, c
    return "$%d" % (c // 100)


def mval(s):
    """value in cents of a money text, or None"""
    s = re.sub(r"<[^>]+>", "", s)
    mm = re.match(r"^\$(\d+)$", s)
    if mm:
        return int(mm.group(1)) * 100
    mm = re.match(r"^(\d+)c$", s)
    if mm:
        return int(mm.group(1))
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


def kinds(toks):
    return [t for t, n in counts(toks)]


def group(toks):
    return ", ".join("%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks))


def cap(s):
    return s[0].upper() + s[1:]


def m_same_step(toks):
    """kept the old step for the first coin of each new kind"""
    s, prev = 0, None
    for t in srt(toks):
        s += VAL[prev] if prev is not None and t != prev else VAL[t]
        prev = t
    return s


def fewest(target, coins=(5, 10, 20, 50, 100, 200)):
    best = {0: []}
    step = min(coins)
    for a in range(step, target + 1, step):
        opts = [best[a - c] + [c] for c in coins if a - c in best]
        if opts:
            best[a] = min(opts, key=len)
    return best[target]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=m):
    """4 choices: correct + the first 3 unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or (c > 100 and c % 100) or c > 2000:
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


def one_svg(t):
    """a single coin or note"""
    w, h = tok_size(t)
    kind = "note" if t.startswith("N") else "coin"
    return svg_wrap(w + 12, h + 12, draw_tok(t, w / 2 + 6, h / 2 + 6), "one %s" % kind)


def tag_w(name):
    return max(len(name) * 9 + 24, 78)


def draw_tag(x, y, name, price, h=62):
    w = tag_w(name)
    return ("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
            % (x, y, w, h, INK) + text(x + w / 2, y + 24, name, 15) + text(x + w / 2, y + 50, m(price), 18, col=GREEN))


def price_svg(items, title):
    """a row of price tags: [('popcorn', 50), ...]"""
    gap, pad, h = 10, 6, 62
    ws = [tag_w(n) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append(draw_tag(x, pad, n, p))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, m(p)) for n, p in items))


def pay_svg(name, price, tok):
    """price tag, then the coin or note used to pay"""
    pad, gap, h = 6, 14, 62
    tw = tag_w(name)
    ww, hh = tok_size(tok)
    lw = 50
    W = pad + tw + gap + lw + ww + pad
    H = max(h, hh) + 2 * pad
    cy = H / 2
    b = [draw_tag(pad, cy - h / 2, name, price),
         text(pad + tw + gap, cy + 6, "Pay:", 16, anchor="start"),
         draw_tok(tok, pad + tw + gap + lw + ww / 2, cy)]
    return svg_wrap(W, H, "".join(b), "price tag: %s %s, paid with %s" % (name, m(price), lab(VAL[tok])))


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
def change_pts(price, paid):
    """cents: price -> next 10c -> paid; dollars: price -> paid"""
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid
    return pts


def count_up(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (m(a), m(b - a), m(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(m(j) for j in jumps), m(ch))
    return "Count on from %s to %s: %s.%s" % (m(price), m(paid), ", ".join(steps), tail)


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting on; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [120, 160][:len(pts) - 1]
    x0, y0 = 44, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 44
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, m(p), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        mid = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, mid, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(mid, y0 - 34, ("+" + m(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting on from %s to %s" % (m(price), m(paid)))


# ============================================================ set 1: coins and notes
def set_coins(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    s(fig(one_svg("C5")) + "How much is this coin worth?", "5c", ["$5", "50c", "10c"],
      "The coin says 5c. The c means cents. It is worth <b>5c</b>, our smallest coin.")
    s(fig(one_svg("C20")) + "How much is this coin worth?", "20c", ["$20", "$2", "10c"],
      "The coin says 20c. It is worth <b>20c</b> (20 cents). $20 is a note.")
    s(fig(one_svg("C50")) + "How much is this coin worth?", "50c", ["$50", "5c", "20c"],
      "This 12-sided coin says 50c. It is worth <b>50c</b> (50 cents). There is no $50 coin.")
    s(fig(one_svg("C100")) + "How much is this gold coin worth?", "$1", ["10c", "$10", "50c"],
      "This gold coin is <b>$1</b> (one dollar). $1 is worth 100c.")
    s(fig(one_svg("C200")) + "How much is this gold coin worth?", "$2", ["20c", "$20", "$1"],
      "This small gold coin is <b>$2</b> (two dollars). It is not 20c.")
    s(fig(one_svg("N5")) + "How much is this note worth?", "$5", ["5c", "$50", "$2"],
      "This note says $5. It is worth <b>$5</b> (five dollars).")
    s(fig(one_svg("N10")) + "How much is this note worth?", "$10", ["10c", "$1", "$20"],
      "This note says $10. It is worth <b>$10</b> (ten dollars).")
    s("How do you write 20 cents?", "20c", ["$20", "20", "$2"],
      "Write the number, then c for cents: <b>20c</b>. $20 would be 20 dollars.")
    s("How do you write 5 dollars?", "$5", ["5c", "5$", "$50"],
      "Write the $ sign first, then the number: <b>$5</b>. 5c would be 5 cents.")
    s("How many cents make $1?", "100c", ["10c", "1000c", "50c"],
      "$1 = <b>100c</b>. Two 50c coins or ten 10c coins make $1.")
    t = ["C50", "C200", "C20", "C100"]
    s(fig(money_svg(t, gap=10, label="coins: 50c, $2, 20c, $1")) + "Which coin is worth the most?", "$2", ["50c", "$1", "20c"],
      "The <b>$2</b> coin is worth the most, even though it is one of the smallest coins. "
      "The 50c coin is the biggest, but it is only worth 50 cents. Read the number, not the size.")
    t = ["C20", "C5", "C50", "C10"]
    s(fig(money_svg(t, gap=10, label="coins: 20c, 5c, 50c, 10c")) + "Which coin is worth the least?", "5c", ["10c", "20c", "50c"],
      "The smallest number is 5. The <b>5c</b> coin is worth the least.")
    s(fig(money_svg(["C100", "C200"], gap=16, label="coins: $1 (bigger), $2 (smaller)")) +
      "The $1 coin is bigger than the $2 coin. Which coin is worth more?",
      "the $2 coin", ["the $1 coin", "They are worth the same.", "You cannot tell."],
      "Size does not tell you the value. $2 is more than $1, so <b>the $2 coin</b> is worth more.")
    s(fig(money_svg(["C50", "C100"], gap=16, label="coins: 50c (bigger), $1 (smaller)")) +
      "The 50c coin is bigger than the $1 coin. Which coin is worth more?",
      "the $1 coin", ["the 50c coin", "They are worth the same.", "You cannot tell."],
      "$1 = 100c, and 100c is more than 50c. So <b>the $1 coin</b> is worth more, even though it is smaller.")
    s("Which coin has 12 sides?", "50c", ["$1", "20c", "$2"],
      "The <b>50c</b> coin has 12 sides. All the other coins are round.")
    s("Which of these is a note?", "$10", ["$2", "$1", "50c"],
      "Notes are made of plastic: $5, $10, $20, $50 and $100. <b>$10</b> is a note. $1 and $2 are coins.")
    s("Which is worth more: 50c or $1?", "$1", ["50c", "They are the same.", "You cannot tell."],
      "$1 = 100c. 100c is more than 50c, so <b>$1</b> is worth more.")
    s("Which coin is worth the same as two 50c coins?", "$1", ["$2", "50c", "20c"],
      "50c + 50c = 100c = $1. Two 50c coins are worth the same as one <b>$1</b> coin.")
    right = "20c, 50c, $1, $2"
    wl = ["$2, $1, 20c, 50c", "$1, $2, 20c, 50c", "50c, 20c, $2, $1"]
    s(fig(money_svg(["C100", "C50", "C200", "C20"], gap=10, label="coins: $1, 50c, $2, 20c")) +
      "Put these coins in order. Start with the least.", right, wl,
      "Cents come first: 20c is less than 50c. Then dollars: $1, then $2. Order: <b>%s</b>. "
      "Do not order them by size." % right)
    right = "$20, $10, $5, $2"
    wl = ["$2, $5, $10, $20", "$20, $10, $2, $5", "$10, $20, $5, $2"]
    s(fig(money_svg(["N5", "N20", "C200", "N10"], per_row=4, gap=10, label="money: $5, $20, $2, $10")) +
      "Put this money in order. Start with the most.", right, wl,
      "The biggest number is worth the most: <b>%s</b>." % right)
    assert len(its) == 20
    return {"title": "Coins and notes", "items": its}


# ============================================================ set 2: count the money
def count_e(toks):
    toks = srt(toks)
    T = total(toks)
    run, s = [], 0
    for t in toks:
        s += VAL[t]
        run.append(m(s) if T > 100 else "%dc" % s)
    if len(set(toks)) == 1:
        v = VAL[toks[0]]
        step = v // 100 if v >= 100 else v
        e = "Each coin is %s. Count in %ds: %s." % (lab(v), step, ", ".join(run))
    else:
        w = "Start with the biggest note" if any(t.startswith("N") for t in toks) else "Start with the biggest coin"
        e = "%s and count on: %s." % (w, ", ".join(run))
    if T == 100:
        e += " 100c = <b>$1</b>."
    else:
        e += " That is <b>%s</b>." % m(T)
    return e


def set_count(P, rnd):
    its = []
    groups = [
        [("C10", 4)], [("C5", 6)], [("C20", 3)], [("C10", 2), ("C5", 1)], [("C20", 1), ("C10", 1), ("C5", 1)],
        [("C20", 4)], [("C50", 1), ("C10", 2)], [("C20", 2), ("C5", 1)], [("C50", 1), ("C20", 2)],
        [("C50", 1), ("C20", 1), ("C5", 1)], [("C20", 2), ("C10", 1), ("C5", 1)], [("C50", 1), ("C5", 3)],
        [("C50", 1), ("C20", 1), ("C10", 1), ("C5", 1)], [("C50", 2)],
        [("C100", 3)], [("C200", 3)], [("C200", 2), ("C100", 1)], [("N5", 1), ("C200", 1), ("C100", 1)],
        [("N10", 1), ("N5", 1), ("C200", 1)], [("N10", 1), ("N5", 1), ("C200", 1), ("C100", 1)],
    ]
    mixed = {10, 11, 12, 17, 19}
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s pencil case. How much is it?", "What is the total?",
             "%s puts this money in %s money box. How much is in the box?"]
    seen = set()
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T not in seen, T
        seen.add(T)
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if any(t.startswith("N") for t in toks) and "coins" in st:
            st = stems[4]
        if st.count("%s") == 2:
            st = st % (nm, he if "does" in st else his)
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = count_e(toks)
        if i in mixed:
            e = "Put the money in order, biggest first. " + e
        if i < 3:
            e += " Count the value of each coin, not the number of coins."
        n = len(toks)
        last, first = VAL[kinds(toks)[-1]], VAL[kinds(toks)[0]]
        if T < 100:
            cands = [n, m_same_step(toks), T - last, T + last, T - first, T + 10, T - 10]
            its.append(mcq(q, T, cands, e))
        elif T == 100:
            # one coin only; counted each 50c coin as $1; added the digits 5 + 5
            its.append(mcq(q, T, ["50c", "$2", "10c"], e + " $2 counts each 50c coin as $1."))
        else:
            cands = ["%dc" % (T // 100), "$%d" % n, m_same_step(toks), T - last, T + last, T - first]
            e += " Dollars are not cents: %s is not %dc." % (m(T), T // 100)
            its.append(mcq(q, T, cands, e))
    assert len(its) == 20
    return {"title": "Count the money", "items": its}


# ============================================================ set 3: make an amount
def gtxt(vals):
    return ", ".join(lab(v) for v in sorted(vals, reverse=True))


def gplus(vals):
    return " + ".join(lab(v) for v in sorted(vals, reverse=True))


def tag_svg(amount):
    w, h, pad = 96, 50, 6
    b = ("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (pad, pad, w, h, INK) + text(pad + w / 2, pad + h / 2 + 8, m(amount), 22, col=GREEN))
    return svg_wrap(w + 2 * pad, h + 2 * pad, b, "amount: %s" % m(amount))


def set_make(P, rnd):
    its = []

    def which(target, right, wrong, stem="Which coins make %s?"):
        assert sum(right) == target, (target, right)
        for w in wrong:
            assert sum(w) != target, (target, w)
        q = fig(tag_svg(target)) + stem % m(target)
        e = ("<b>%s</b> = %s. " % (gplus(right), m(target)) + " ".join(
            "%s = %s." % (gplus(w), m(sum(w))) for w in wrong))
        its.append(mcq(q, gtxt(right), [gtxt(w) for w in wrong], e))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> = %s, not %s. " % (gplus(right), m(sum(right)), m(target))
             + "The others all make %s." % m(target))
        its.append(mcq(fig(tag_svg(target)) + "Which of these does <b>not</b> make %s?" % m(target),
                       gtxt(right), [gtxt(w) for w in wrong], e))

    def how_few(target, wrong, extra, coins=(5, 10, 20, 50, 100, 200), word="coins", one="coin"):
        f = fewest(target, coins)
        n = len(f)
        ch = lambda k: "%d %s" % (k, one if k == 1 else word)
        e = "Use the biggest one you can each time: %s = %s. That is <b>%s</b>. %s" % (gplus(f), m(target), ch(n), extra)
        its.append(mcq(fig(tag_svg(target)) + "What is the fewest %s you can use to make %s?" % (word, m(target)),
                       ch(n), [ch(k) for k in wrong], e))

    def which_fewest(target, wrong):
        f = fewest(target)
        for w in wrong:
            assert sum(w) == target and len(w) > len(f)
        e = ("All of these make %s. <b>%s</b> uses only %d coins. Start with the biggest coin you can."
             % (m(target), gplus(f), len(f)))
        its.append(mcq(fig(tag_svg(target)) + "Which uses the fewest coins to make %s?" % m(target),
                       gtxt(f), [gtxt(w) for w in wrong], e))

    def same_as(toks, right, wrong, word="coin"):
        T = total(toks)
        q = fig(money_svg(toks)) + "Which is worth the same as this money?"
        e = count_e(toks) + " So <b>one %s %s</b> is worth the same." % (lab(T), word)
        its.append(mcq(q, right, wrong, e))

    which(30, [20, 10], [[20, 5], [10, 10], [20, 20]])
    which(50, [20, 20, 10], [[20, 20, 5], [20, 10, 10], [50, 10]])
    same_as(["C20", "C20", "C10"], "one 50c coin", ["one 20c coin", "one $1 coin", "one 10c coin"])
    which(100, [50, 50], [[50, 20, 20], [20, 20, 20, 20], [50, 10, 10, 10]])
    which_not(40, [20, 10, 5], [[20, 20], [10, 10, 10, 10], [20, 10, 10]])
    how_few(60, [1, 3, 6], "There is no 60c coin, so 1 coin is not possible. Six 10c coins also make 60c, but that is more coins.")
    nm, he, his = P.next()
    which(45, [20, 20, 5], [[20, 10, 5], [20, 20, 10], [10, 10, 5]],
          stem=nm + " has 3 coins. Together they make %s. Which coins does " + he + " have?")
    same_as(["C100", "C100"], "one $2 coin", ["one $1 coin", "one 20c coin", "one $5 note"])
    which(75, [50, 20, 5], [[50, 20, 10], [20, 20, 20, 5], [50, 10, 10]])
    which_fewest(70, [[20, 20, 20, 10], [50, 10, 10], [10] * 7])
    how_few(90, [2, 4, 9], "Two coins cannot make 90c: 50c + 50c = $1 is too much.")
    same_as(["C200", "C200", "C100"], "one $5 note", ["one $2 coin", "one $10 note", "one $1 coin"], word="note")
    which(1000, [500, 500], [[500, 200, 200], [500, 200], [200, 200, 200, 200]], stem="Which make %s?")
    which(1500, [1000, 500], [[500, 500], [1000, 200, 200], [1000, 500, 500]], stem="Which make %s?")
    nm, he, his = P.next()
    which(80, [50, 10, 10, 10], [[20, 20, 20, 10], [50, 10, 10, 5], [50, 20, 20, 10]],
          stem=nm + " has 4 coins. Together they make %s. Which coins does " + he + " have?")
    which_not(100, [50, 20, 20, 5], [[50, 50], [50, 20, 20, 10], [20, 20, 20, 20, 20]])
    how_few(800, [2, 4, 8], "No two of them make $8 ($5 + $2 = $7, $5 + $5 = $10). Eight $1 coins also make $8, but that is a lot.",
            coins=(100, 200, 500, 1000), word="coins and notes", one="coin or note")
    which_not(500, [200, 200, 200], [[200, 200, 100], [200, 100, 100, 100], [100] * 5])
    which(1200, [1000, 200], [[1000, 100], [500, 200, 200], [1000, 200, 200]], stem="Which make %s?")
    which(95, [50, 20, 20, 5], [[50, 20, 10, 5], [50, 20, 20, 10], [20, 20, 20, 20, 5]])
    assert len(its) == 20
    return {"title": "Make an amount in different ways", "items": its}


# ============================================================ set 4: change
def change_cands(paid, price):
    r = paid - price
    if paid <= 100:
        # took the tens wrongly (100 − 35 as 75), gave the price, off by a jump
        c = [r + 10 if price % 10 else None, price, r - 10, r + 5, r - 5, r + 20]
        return [x for x in c if x is not None and 0 < x < 100]
    # dollars: gave the price, added instead of taking away, off by one dollar
    c = [price, paid + price, r + 100, r - 100, r + 200, 50]
    return [x for x in c if 0 < x <= 2000]


def set_change(P, rnd):
    its = []
    things = {35: "a sticker", 40: "an apple", 45: "a pencil", 50: "a bag of popcorn", 60: "a cheese stick",
              70: "an eraser", 75: "a fruit cup", 80: "a balloon", 85: "a bookmark", 90: "a ruler", 95: "a party hat",
              100: "a pen", 200: "a drink", 300: "a sausage roll", 400: "a sushi roll"}

    def change(price, paid_tok, mode):
        paid = VAL[paid_tok]
        nm, he, his = P.next()
        r = paid - price
        thing = things[price]
        money = ("a %s coin" if paid <= 200 else "a %s note") % m(paid)
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, m(price), cap(he), money, he)
        if mode == "line":
            q = fig(change_line(price, paid, show=False)) + q + " Count on along the number line."
        else:
            q = fig(pay_svg(thing.split(" ", 1)[1].replace("bag of ", ""), price, paid_tok)) + q
        e = count_up(price, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (m(r), m(price), m(r), m(paid))
        its.append(mcq(q, r, change_cands(paid, price), e))

    change(90, "C100", "pay")
    change(80, "C100", "line")
    change(50, "C100", "pay")
    change(70, "C100", "line")
    change(60, "C100", "pay")
    change(40, "C100", "line")
    change(100, "C200", "pay")
    change(300, "N5", "pay")
    change(400, "N5", "pay")
    change(200, "N5", "line")
    change(100, "N5", "line")
    change(95, "C100", "line")
    change(75, "C100", "pay")
    change(45, "C100", "line")
    change(35, "C100", "pay")
    change(85, "C100", "line")

    nm, he, his = P.next()
    assert 100 - 70 == 30 and 20 + 10 == 30
    its.append(mcq(fig(pay_svg("eraser", 70, "C100")) + "%s buys an eraser for 70c. %s pays with a $1 coin. "
                   "Which coins could %s get as change?" % (nm, cap(he), he), "20c, 10c",
                   ["20c, 20c", "50c, 20c", "20c, 5c"],
                   "$1 = 100c. Count on from 70c to 100c: 30c. 20c + 10c = 30c, so <b>20c, 10c</b>. "
                   "20c + 20c = 40c is too much."))
    nm, he, his = P.next()
    assert 100 - 45 == 55 and 50 + 5 == 55
    its.append(mcq(fig(pay_svg("pencil", 45, "C100")) + "%s buys a pencil for 45c. %s pays with a $1 coin. "
                   "Which coins could %s get as change?" % (nm, cap(he), he), "50c, 5c",
                   ["50c, 10c", "20c, 20c, 5c", "50c, 20c, 5c"],
                   "Count on from 45c: 45c + 5c = 50c, 50c + 50c = 100c. The change is 55c. "
                   "50c + 5c = 55c, so <b>50c, 5c</b>."))
    nm, he, his = P.next()
    its.append(mcq(fig(one_svg("C100")) + "%s pays with a $1 coin and gets 30c change. How much did %s spend?" % (nm, he),
                   70, [30, 80, 60],
                   "Count on from 30c to 100c: 30c + 70c = 100c. %s spent <b>70c</b>. Check: 70c + 30c = 100c = $1." % cap(he)))
    nm, he, his = P.next()
    its.append(mcq(fig(one_svg("N5")) + "%s pays with a $5 note and gets $2 change. How much did %s spend?" % (nm, he),
                   300, [200, 700, 400],
                   "$2 + $3 = $5, so %s spent <b>$3</b>. $7 adds the change instead of taking it away." % he))
    assert len(its) == 20
    return {"title": "Change from $1, $2 and $5", "items": its}


# ============================================================ set 5: shopping at the school canteen
SNACKS = [("apple", 30), ("popcorn", 50), ("cheese stick", 60), ("ice block", 70)]
LUNCH = [("pie", 500), ("sushi roll", 400), ("sausage roll", 300), ("juice", 200)]


def set_canteen(P, rnd):
    its = []
    S, L_ = dict(SNACKS), dict(LUNCH)
    snack_fig = fig(price_svg(SNACKS, "school canteen snacks"))
    lunch_fig = fig(price_svg(LUNCH, "school canteen lunch"))

    def add(q, right, cands, e, fmt=m):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    assert S["apple"] + S["popcorn"] == 80
    add(snack_fig + "%s buys an apple and popcorn. How much does %s spend?" % (nm, he), 80, [20, 8, 35],
        "30c + 50c: 3 tens + 5 tens = 8 tens. That is <b>80c</b>. 20c is the difference, not the total. 35c just puts the 3 and the 5 together.")
    nm, he, his = P.next()
    assert 2 * S["popcorn"] == 100
    add(snack_fig + "%s buys 2 bags of popcorn. How much does %s spend?" % (nm, he), 100, ["50c", "10c", "$2"],
        "50c + 50c = 100c. 100c = <b>$1</b>. 50c is only 1 bag.")
    nm, he, his = P.next()
    assert L_["pie"] + L_["juice"] == 700
    add(lunch_fig + "%s orders a pie and a juice. How much does it cost?" % nm, 700, [300, 600, 800],
        "$5 + $2 = <b>$7</b>. $3 is the difference, not the total.")
    nm, he, his = P.next()
    assert L_["sushi roll"] + L_["juice"] == 600
    add(lunch_fig + "%s orders a sushi roll and a juice. How much does it cost?" % nm, 600, [200, 500, 700],
        "$4 + $2 = <b>$6</b>.")
    nm, he, his = P.next()
    add(snack_fig + "%s buys an ice block. %s pays with a $1 coin. How much change does %s get?" % (nm, cap(he), he),
        30, [70, 40, 20], count_up(70, 100) + " The change is <b>30c</b>. 70c is the price, not the change.")
    nm, he, his = P.next()
    add(snack_fig + "%s buys a cheese stick. %s pays with a $1 coin. How much change does %s get?" % (nm, cap(he), he),
        40, [60, 50, 30], count_up(60, 100) + " The change is <b>40c</b>. 60c is the price, not the change.")
    nm, he, his = P.next()
    add(lunch_fig + "%s buys a sushi roll. %s pays with a $5 note. How much change does %s get?" % (nm, cap(he), he),
        100, [400, 900, 200], "$4 + $1 = $5. The change is <b>$1</b>. $9 adds the money instead of taking it away.")
    nm, he, his = P.next()
    assert L_["sausage roll"] + L_["juice"] == 500
    add(lunch_fig + "%s buys a sausage roll and a juice. %s pays with a $10 note. How much change does %s get?" % (nm, cap(he), he),
        500, [700, 1000, 600],
        "Cost: $3 + $2 = $5. Count on from $5 to $10: $5. The change is <b>$5</b>. $7 forgets the juice.")
    nm, he, his = P.next()
    add(snack_fig + "%s has 50c. %s wants an ice block. How much more money does %s need?" % (nm, cap(he), he),
        20, [70, 30, 10],
        "Count on from 50c to 70c: 50c + 20c = 70c. %s needs <b>20c</b> more. 30c is the change from $1." % cap(he))
    nm, he, his = P.next()
    add(lunch_fig + "%s has $5. %s wants a pie and a juice. Does %s have enough?" % (nm, cap(he), he),
        "No, %s needs $2 more." % he, ["Yes, with $2 left.", "Yes, with $3 left.", "No, %s needs $7 more." % he],
        "Cost: $5 + $2 = $7. $7 is more than $5, so <b>no</b>. $5 + $2 = $7, so %s needs <b>$2</b> more." % he)
    nm, he, his = P.next()
    assert 3 * S["apple"] == 90
    add(snack_fig + "%s buys 3 apples. How much does %s spend?" % (nm, he), 90, [33, 60, 30],
        "3 lots of 30c: 30c, 60c, 90c. That is <b>90c</b>. 33c adds 30 and 3. 60c is only 2 apples.")
    nm, he, his = P.next()
    assert 4 * 200 == 800
    add("At the sausage sizzle, a sausage costs $2. %s buys 4 sausages. How much does %s pay?" % (nm, he),
        800, [600, 200, 1000],
        "Count in 2s: $2, $4, $6, $8. That is <b>$8</b>. $6 adds 2 + 4. $10 would be 5 sausages.")
    nm, he, his = P.next()
    assert 3 * 30 <= 100 < 4 * 30
    add(snack_fig + "%s has $1. How many apples can %s buy?" % (nm, he), "3 apples",
        ["4 apples", "2 apples", "10 apples"],
        "$1 = 100c. Count in 30s: 30c, 60c, 90c. That is <b>3 apples</b>, with 10c left. 4 apples would cost 120c, which is too much.")
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    assert S["apple"] + S["popcorn"] == 80 > S["ice block"]
    add(snack_fig + "%s buys an apple and popcorn. %s buys an ice block. Who spends more?" % (nm1, nm2), nm1,
        [nm2, "They spend the same.", "You cannot tell."],
        "%s: 30c + 50c = 80c. %s: 70c. 80c is more than 70c, so <b>%s</b> spends more." % (nm1, nm2, nm1))
    toks = toks_of(("C50", 1), ("C20", 2))
    assert total(toks) == 90
    nm, he, his = P.next()
    add(fig(money_svg(toks)) + "%s has these coins. %s buys an ice block for 70c. How much money is left?" % (nm, cap(he)),
        20, [70, 30, 90],
        count_e(toks) + " " + count_up(70, 90) + " <b>20c</b> is left. 70c is the cost of the ice block.")
    nm, he, his = P.next()
    assert S["apple"] + S["ice block"] == 100
    add(snack_fig + "%s buys an apple and an ice block. %s pays with a $2 coin. How much change does %s get?" % (nm, cap(he), he),
        100, [200, 300, 30],
        "Cost: 30c + 70c = 100c = $1. Count on from $1 to $2: $1. The change is <b>$1</b>. $2 is the coin, not the change. 30c is the change from $1 for the ice block only.")
    nm, he, his = P.next()
    assert 2 * L_["sushi roll"] == 800
    add(lunch_fig + "%s buys 2 sushi rolls. %s pays with a $10 note. How much change does %s get?" % (nm, cap(he), he),
        200, [600, 800, 400],
        "Cost: $4 + $4 = $8. Count on from $8 to $10: $2. The change is <b>$2</b>. $6 is the change for only 1 sushi roll.")
    nm, he, his = P.next()
    add(lunch_fig + "%s’s mum puts a $10 note in %s lunch order bag. The order is a pie and a juice. How much change comes back?" % (nm, his),
        300, [700, 500, 400],
        "Cost: $5 + $2 = $7. Count on from $7 to $10: $3. The change is <b>$3</b>. $7 is the cost, not the change. $5 forgets the juice.")
    nm1, he1, his1 = P.next()
    nm2, he2, his2 = P.next()
    assert L_["sushi roll"] // 2 == 200
    add(lunch_fig + "%s and %s share a sushi roll. They each pay the same amount. How much does each one pay?" % (nm1, nm2),
        200, [400, 100, 600],
        "Share $4 into 2 equal parts: $2 and $2. Each one pays <b>$2</b>. $4 is the whole sushi roll.")
    nm, he, his = P.next()
    toks = toks_of(("C200", 2), ("C100", 1))
    assert total(toks) == 500
    add(fig(money_svg(toks)) + "%s has these coins. %s wants a sausage roll for $3. How much will be left?" % (nm, cap(he)),
        200, [300, 800, 100],
        count_e(toks) + " Count on from $3 to $5: $2. <b>$2</b> will be left. $3 is the cost, not what is left. "
        "$1 forgets the $1 coin.")
    assert len(its) == 20
    return {"title": "Shopping at the school canteen", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20"]
    walk = toks_of(("C50", 1), ("C20", 1), ("C10", 1), ("C5", 1))
    under = ["50c", "70c", "80c", "85c"]
    assert total(walk) == 85
    return (
        "<h2>Coins and notes</h2>"
        "<p>We write cents with a small c: 50c. We write dollars with the $ sign in front: $5. "
        "$1 is the same as 100c.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=6, label="Australian coins: 5c, 10c, 20c, 50c, $1, $2") +
        "<figcaption>Coins: 5c, 10c, 20c, 50c, $1 and $2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, per_row=3, label="Australian notes: $5, $10, $20") +
        "<figcaption>Notes: $5, $10 and $20.</figcaption></figure>"
        "<p>A big coin is not always worth more. The 50c coin is the biggest coin. "
        "The $2 coin is smaller than the $1 coin, but it is worth more. Always read the number.</p>"
        "<h2>Count the money, biggest first</h2>"
        "<p>Put the coins in order. Start with the biggest value and count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=18, under=under, label="counting on: 50c, 70c, 80c, 85c") +
        "<figcaption>50c, 70c, 80c, 85c. The total is 85c.</figcaption></figure>"
        + ex("Example", "Count $10, $5 and $2.", "Start with the note worth the most: $10, $15, $17.", "$17")
        + "<h2>Make an amount in different ways</h2>"
        "<p>50c can be 20c + 20c + 10c, or 10c + 10c + 10c + 10c + 10c, or one 50c coin. "
        "For the fewest coins, use the biggest coin you can each time.</p>"
        + ex("Example", "Find two ways to make 30c.",
             "20c + 10c = 30c. 10c + 10c + 10c = 30c. 20c + 10c uses the fewest coins.", "20c + 10c or 10c + 10c + 10c")
        + "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Count on to the money you paid. The jumps are the change.</p>"
        "<figure class='sn-fig'>" + change_line(35, 100) +
        "<figcaption>Change from $1 for 35c: 5c + 60c = 65c.</figcaption></figure>"
        + ex("Example", "A sushi roll costs $4. You pay with a $5 note. What is the change?",
             "Count on: $4 + $1 = $5.", "$1")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 coins, so 4c", "Count the value of each coin: 50c, 70c, 80c, 85c"],
            ["The 50c coin is the biggest, so it is worth the most", "Read the number: $1 and $2 are worth more"],
            ["The $1 coin is bigger than the $2 coin, so it is worth more", "$2 is two dollars. Size does not tell you the value"],
            ["$5 is the same as 5c", "$5 is five dollars. $1 alone is 100c"],
            ["Change from $1 for 35c is 75c", "Count on: 35c + 5c = 40c, 40c + 60c = 100c. The change is 65c"],
        ])
    )


FAQ = [
    {"q": "What do Year 2 students learn about money in the Australian Curriculum?",
     "a": "In Year 2 (AC9M2N06), students count collections of coins and notes, make the same amount in different ways and solve simple shopping problems, such as working out change from $1, $2 or $5."},
    {"q": "Is the $2 coin bigger than the $1 coin?",
     "a": "No. The $2 coin is smaller than the $1 coin, but it is worth more. The 12-sided 50c coin is the biggest Australian coin, so size never tells you the value."},
    {"q": "How do you teach a Year 2 child to give change?",
     "a": "Count on from the price to the money paid. For 35c paid with $1: 35c to 40c is 5c, 40c to 100c is 60c, so the change is 65c."},
    {"q": "Why does my child say 4 coins make 4c?",
     "a": "Young children often count the coins instead of their value. Ask them to read the number on each coin, put the coins in order from biggest value and count on: 50c, 70c, 80c, 85c."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(2807)
    P = People(rnd)
    sets = [set_coins(P, rnd), set_count(P, rnd), set_make(P, rnd), set_change(P, rnd), set_canteen(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [mval(c) for c in it["c"] if mval(c) is not None]
            assert len(set(vv)) == len(vv), it["c"]
            for c in it["c"]:
                assert not re.search(r"\$\d+c|\.\d|¢|\b[12]c\b", c), c
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "au", "subject": "maths", "grade": "year-2", "slug": "money", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Coins, Notes, Counting and Giving Change",
        "seo_title": "Year 2 Money Worksheets: Australian Coins, Notes and Change",
        "short_title": "Money",
        "domain": "Number",
        "standard_code": "AC9M2N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical additive and multiplicative problems, including money transactions, representing the situation and choosing calculation strategies; interpret and communicate solutions in terms of the situation",
        "meta_desc": "Free Year 2 maths worksheets on money: name and order Australian coins and notes, count collections of cents and dollars, make 50c or $10 in different ways, give change from $1, $2 and $5 by counting on, and solve school canteen shopping problems. 100 questions with an answer key, following the Australian Curriculum.",
        "key_big": "Read the number on each coin, then count on from the biggest.",
        "key_sub": "Size is not value: the 50c coin is the biggest, and the small $2 coin is worth more than the $1 coin. $1 = 100c. To give change, count on from the price: 35c to 40c to $1 is 5c + 60c = 65c.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|counting|price|coins)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
