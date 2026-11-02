# -*- coding: utf-8 -*-
"""
UK Year 2 Maths: Money (National Curriculum in England, Year 2: Measurement)
  python3 tools/gen_uk_maths_y2_money.py
All amounts are whole numbers of pence (int). Year 2 keeps one unit in a calculation:
pence up to 100p (written 45p) or whole pounds up to £20 (written £7). No £2.35 notation.
Coins and notes are simple labelled shapes (no real coin or note artwork).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-2")
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
# radius, (fill, edge), label size  (2p is drawn bigger than 5p and 10p, as in real life)
COIN = {"C1": (18, COPPER, 14), "C2": (22, COPPER, 15), "C5": (17, SILVER, 14), "C10": (21, SILVER, 14),
        "C20": (20, SILVER, 14), "C50": (23, SILVER, 15), "C100": (21, GOLD, 15), "C200": (24, GOLD, 16)}
NOTE = {"N5": ("#bfe6de", "#1f7a6d"), "N10": ("#f6d2a8", "#a35a12"), "N20": ("#dccbef", "#5b3a8a")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "£%d" % (v // 100) if v >= 100 else "%dp" % v


def p(x):
    """pence: 45 -> '45p'"""
    assert 0 < x <= 100, x
    return "%dp" % x


def pd(x):
    """whole pounds, given in pence: 700 -> '£7'"""
    assert x > 0 and x % 100 == 0 and x <= 2000, x
    return "£%d" % (x // 100)


def mval(s):
    """value in pence of a money text, or None: '£3' -> 300, '45p' -> 45"""
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^£(\d+)$", s)
    if m:
        return int(m.group(1)) * 100
    m = re.match(r"^(\d+)p$", s)
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


def kinds(toks):
    return [t for t, n in counts(toks)]


def cap(s):
    return s[0].upper() + s[1:]


def fewest(amount):
    """fewest UK coins and notes (greedy is exact for UK money)"""
    out, r = [], amount
    for t in ORDER:
        while VAL[t] <= r:
            out.append(t)
            r -= VAL[t]
    return out


def small_from_big(a, b):
    """column subtraction taking the smaller digit from the bigger one: 50 - 35 -> 25"""
    k = len(str(a))
    da = [(a // 10 ** i) % 10 for i in range(k)]
    db = [(b // 10 ** i) % 10 for i in range(k)]
    return sum(abs(x - y) * 10 ** i for i, (x, y) in enumerate(zip(da, db)))


def noexch_add(nums):
    """added the ones but did not exchange 10 ones for a ten: 38 + 25 -> 53"""
    ones = sum(n % 10 for n in nums) % 10
    tens = sum(n // 10 for n in nums)
    return tens * 10 + ones


# ------------------------------------------------------------ helpers
def mcq(q, right, wrongs, e):
    """right and wrongs are texts; keep the first 3 wrongs that differ in text and in money value."""
    seen_t = {right}
    seen_v = {mval(right)} - {None}
    pick = []
    for c in wrongs:
        if c is None or c in seen_t:
            continue
        v = mval(c)
        if v is not None and v in seen_v:
            continue
        seen_t.add(c)
        if v is not None:
            seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, wrongs)
    return {"q": q, "c": [right] + pick, "a": 0, "e": e}


def pc(xs):
    """pence candidates -> texts (only real amounts from 1p to 100p)"""
    return [p(x) for x in xs if x is not None and 0 < x <= 100]


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
        x = self.pool[self.i % len(self.pool)]
        self.i += 1
        return x


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


def group(toks):
    return ", ".join("%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks))


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
    word = "note" if t.startswith("N") else "coin"
    return svg_wrap(w + 6, h + 6, draw_tok(t, (w + 6) / 2, (h + 6) / 2), "one %s %s" % (lab(VAL[t]), word))


def shuffled(toks, rnd):
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


def price_svg(items, title, fmt):
    """a row of price tags: [('apple', 20), ...]"""
    gap, pad, h = 10, 6, 62
    ws = [max(len(n) * 9 + 24, 70) for n, x in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, v), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, fmt(v), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, fmt(v)) for n, v in items))


def change_pts(price, paid):
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid
    return pts


def count_on(price, paid):
    """'Count on from 35p to 50p: 35p + 5p = 40p, 40p + 10p = 50p. 5p + 10p = 15p.'"""
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (p(a), p(b - a), p(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    assert sum(jumps) == paid - price
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(p(j) for j in jumps), p(paid - price))
    return "Count on from %s to %s: %s.%s" % (p(price), p(paid), ", ".join(steps), tail)


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting on in pence; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [110, 150][:len(pts) - 1]
    x0, y0 = 40, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 40
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 20, y0, xs[-1] + 20, y0, INK)]
    for x, v in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, p(v), 16))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + p(pts[i + 1] - pts[i])) if show else "+ ?", 16, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting on from %s to %s" % (p(price), p(paid)))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ============================================================ set 1: coins, notes and symbols
def set_symbols(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    s(fig(coin_svg("C10")) + "How much is this coin worth?", "10p", ["£10", "1p", "20p"],
      "The coin says 10p. The p means pence. It is worth <b>10p</b>.")
    s(fig(coin_svg("C2")) + "How much is this coin worth?", "2p", ["£2", "20p", "5p"],
      "The coin says 2p. It is worth <b>2p</b> (2 pence). The £2 coin is gold and silver.")
    s(fig(coin_svg("C50")) + "How much is this coin worth?", "50p", ["£50", "5p", "20p"],
      "The coin says 50p. It is worth <b>50p</b> (50 pence). There is no £50 coin.")
    s(fig(coin_svg("C100")) + "How much is this coin worth?", "£1", ["1p", "£10", "10p"],
      "This gold coin is <b>£1</b> (one pound). £1 is worth 100p.")
    s(fig(coin_svg("C200")) + "How much is this coin worth?", "£2", ["2p", "£20", "20p"],
      "This gold and silver coin is <b>£2</b> (two pounds). It is not 2p.")
    s(fig(coin_svg("N5")) + "How much is this note worth?", "£5", ["5p", "£50", "£2"],
      "This note says £5. It is worth <b>£5</b> (five pounds).")
    s("How do you write 20 pence?", "20p", ["£20", "20", "2p"],
      "Write the number, then p for pence: <b>20p</b>. £20 would be 20 pounds.")
    s("How do you write 5 pounds?", "£5", ["5p", "5£", "£50"],
      "Write the £ sign first, then the number: <b>£5</b>. 5p would be 5 pence.")
    s("In £5, what does the £ sign mean?", "pounds", ["pence", "plus", "price"],
      "£ means <b>pounds</b>. p means pence. £5 is five pounds.")
    s("How many pence make £1?", "100p", ["10p", "1p", "50p"],
      "£1 = <b>100p</b>. A £1 coin is worth the same as one hundred 1p coins.")
    t = ["C2", "C20", "C1", "C5"]
    s(fig(money_svg(t, label="coins: 2p, 20p, 1p, 5p")) + "Which coin is worth the most?", "20p", ["2p", "5p", "1p"],
      "Look at the numbers, not the size. 20p is worth the most: <b>20p</b>. The 2p coin is big, but it is only worth 2p.")
    t = ["C50", "C200", "C20", "C100"]
    s(fig(money_svg(t, label="coins: 50p, £2, 20p, £1")) + "Which coin is worth the most?", "£2", ["50p", "£1", "20p"],
      "Pounds are worth more than pence. £2 = 200p, which is more than 50p. The answer is <b>£2</b>.")
    t = ["C5", "C10", "C1", "C2"]
    s(fig(money_svg(t, label="coins: 5p, 10p, 1p, 2p")) + "Which coin is worth the least?", "1p", ["2p", "5p", "10p"],
      "The smallest number is 1. The <b>1p</b> coin is worth the least.")
    s(fig(money_svg(["C2", "C5"], gap=20, label="coins: a big 2p and a small 5p")) +
      "The 2p coin is bigger than the 5p coin. Which coin is worth more?",
      "the 5p coin", ["the 2p coin", "They are worth the same.", "You cannot tell."],
      "Size does not matter. 5p is more than 2p, so <b>the 5p coin</b> is worth more.")
    s("Which of these is a note?", "£10", ["£2", "£1", "50p"],
      "Notes are made of paper or plastic: £5, £10 and £20. <b>£10</b> is a note. £1 and £2 are coins.")
    s("Which is worth more: 50p or £1?", "£1", ["50p", "They are the same.", "You cannot tell."],
      "£1 = 100p. 100p is more than 50p, so <b>£1</b> is worth more.")
    s("Which is worth more: £2 or 20p?", "£2", ["20p", "They are the same.", "You cannot tell."],
      "20 is a bigger number, but £2 is two pounds. £1 is already more than 20p, so <b>£2</b> is worth more.")
    s("Which coin is worth the same as two 5p coins?", "10p", ["5p", "2p", "55p"],
      "5p + 5p = 10p. Two 5p coins are worth the same as one <b>10p</b> coin.")
    s("How many 10p coins make £1?", "10", ["100", "1", "5"],
      "£1 = 100p. Count in 10s: 10p, 20p, 30p … 100p. That is <b>10</b> coins.")
    right = "5p, 50p, £2"
    wl = ["£2, 5p, 50p", "50p, 5p, £2", "5p, £2, 50p"]
    s("Put these in order. Start with the least: £2, 5p, 50p.", right, wl,
      "Pence come first: 5p is less than 50p. £2 is two pounds, so it is the most. Order: <b>%s</b>." % right)
    assert len(its) == 20
    return {"title": "Coins, notes, £ and p", "items": its}


# ============================================================ set 2: count the money
def m_same_step(toks):
    """kept the old step for the first coin of each new kind"""
    s, prev = 0, None
    for t in srt(toks):
        s += VAL[prev] if prev is not None and t != prev else VAL[t]
        prev = t
    return s


def count_e(toks):
    toks = srt(toks)
    T = total(toks)
    run, s = [], 0
    for t in toks:
        s += VAL[t]
        run.append("%dp" % s if T <= 100 else pd(s))
    if len(set(toks)) == 1:
        v = VAL[toks[0]]
        if v >= 100:
            return "Each coin is %s. Count in %ds: %s. That is <b>%s</b>." % (lab(v), v // 100, ", ".join(run), lab(T))
        return "Each coin is %s. Count in %ds: %s. That is <b>%s</b>." % (lab(v), v, ", ".join(run), p(T))
    w = "Start with the biggest note" if any(t.startswith("N") for t in toks) else "Start with the biggest coin"
    return "%s and count on: %s. That is <b>%s</b>." % (w, ", ".join(run), lab(T) if T > 100 else p(T))


def set_count(P, rnd):
    its = []
    groups = [
        [("C10", 4)], [("C5", 5)], [("C2", 4)], [("C20", 3)], [("C10", 2), ("C1", 3)],
        [("C20", 1), ("C10", 1), ("C5", 1)], [("C50", 1), ("C10", 2)], [("C20", 2), ("C5", 1), ("C2", 1)],
        [("C50", 1), ("C20", 1), ("C5", 1), ("C1", 1)], [("C10", 3), ("C2", 2)],
        [("C50", 1), ("C20", 2), ("C2", 1), ("C1", 1)], [("C50", 1), ("C5", 2), ("C2", 1)],
        [("C20", 2), ("C10", 1), ("C5", 1), ("C2", 2)], [("C50", 2)], [("C50", 1), ("C20", 2), ("C10", 1)],
        [("C100", 3)], [("C200", 2), ("C100", 1)], [("N5", 1), ("C200", 1), ("C100", 1)],
        [("N10", 1), ("N5", 1), ("C200", 1)], [("N10", 1), ("N5", 1), ("C200", 1), ("C100", 2)],
    ]
    mixed = {11, 12, 14, 19}
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s pencil case. How much is it?", "What is the total?",
             "%s puts this money in %s money box. How much is in the box?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if any(t.startswith("N") for t in toks) and "coins" in st:
            st = stems[4]
        if st.count("%s") == 2:
            st = st % (nm, he if "does" in st else his)
        if T == 100:
            st = "How many pence is this?"
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = count_e(toks)
        if i < 3:
            e += " Count the value of each coin, not the number of coins."
        if T <= 100:
            cands = pc([len(toks), m_same_step(toks), T - VAL[kinds(toks)[-1]], T + VAL[kinds(toks)[-1]],
                        T - VAL[kinds(toks)[0]], T + 10, T - 10, T + 1])
            if T == 100:
                cands = ["£100"] + cands
                e += " 100p is the same as £1."
            its.append(mcq(q, p(T), cands, e))
        else:
            n = len(toks)
            cands = ["%dp" % (T // 100), "£%d" % n, pd(m_same_step(toks)) if m_same_step(toks) <= 2000 else None,
                     pd(T - VAL[kinds(toks)[-1]]), pd(T + VAL[kinds(toks)[-1]])]
            e += " %s is %d pounds, not %dp." % (pd(T), T // 100, T // 100)
            its.append(mcq(q, pd(T), cands, e))
    assert len(its) == 20
    return {"title": "Count the money", "items": its}


# ============================================================ set 3: make an amount
def combo(toks):
    return " + ".join(lab(VAL[t]) for t in srt(toks))


def C(*labels):
    m = {lab(v): k for k, v in VAL.items()}
    return [m[x] for x in labels]


def set_make(P, rnd):
    its = []

    def which(target, right, wrongs, e, neg=False):
        if neg:
            assert total(right) != target and all(total(w) == target for w in wrongs)
            q = "Which of these does NOT make %s?" % lab(target)
        else:
            assert total(right) == target and all(total(w) != target for w in wrongs)
            q = "Which %s make %s?" % ("notes and coins" if target >= 500 else "coins", lab(target))
        its.append(mcq(q, combo(right), [combo(w) for w in wrongs], e))

    which(25, C("20p", "5p"), [C("20p", "2p", "1p"), C("10p", "5p"), C("2p", "5p")],
          "20p + 5p = <b>25p</b>. 20p + 2p + 1p is only 23p.")
    which(30, C("20p", "10p"), [C("10p", "10p"), C("20p", "5p"), C("20p", "2p", "1p")],
          "20p + 10p = <b>30p</b>. 10p + 10p is only 20p.")
    which(50, C("20p", "20p", "10p"), [C("20p", "20p", "5p"), C("10p", "10p", "10p"), C("20p", "20p", "2p")],
          "20p + 20p = 40p. 40p + 10p = <b>50p</b>.")
    which(17, C("10p", "5p", "2p"), [C("10p", "5p", "1p"), C("10p", "2p", "2p", "1p"), C("5p", "5p", "2p")],
          "10p + 5p = 15p. 15p + 2p = <b>17p</b>.")
    which(64, C("50p", "10p", "2p", "2p"), [C("50p", "10p", "2p"), C("50p", "10p", "5p"), C("50p", "20p", "2p", "2p")],
          "50p + 10p = 60p. 60p + 2p + 2p = <b>64p</b>.")
    which(20, C("10p", "5p", "2p"), [C("10p", "10p"), C("10p", "5p", "5p"), C("5p", "5p", "5p", "5p")],
          "10p + 5p + 2p = 17p, not 20p. The others all make 20p. So the answer is <b>10p + 5p + 2p</b>.", neg=True)
    which(40, C("20p", "10p", "5p"), [C("20p", "20p"), C("20p", "10p", "10p"), C("10p", "10p", "10p", "10p")],
          "20p + 10p + 5p = 35p, not 40p. There are many ways to make 40p, but not <b>20p + 10p + 5p</b>.", neg=True)
    which(1000, C("£5", "£2", "£2"), [C("£5", "£5"), C("£5", "£2", "£2", "£1"), C("£2", "£2", "£2", "£2", "£2")],
          "£5 + £2 + £2 = £9, not £10. So the answer is <b>£5 + £2 + £2</b>.", neg=True)
    which(1500, C("£10", "£5"), [C("£10", "£2", "£2"), C("£5", "£5"), C("£10", "£5", "£1")],
          "£10 + £5 = <b>£15</b>.")
    which(2000, C("£10", "£10"), [C("£10", "£5", "£2"), C("£5", "£5", "£5"), C("£10", "£5", "£1", "£1")],
          "£10 + £10 = <b>£20</b>. There is also a £20 note.")

    # missing coin
    def missing(have, target, right, wrongs, e):
        toks = srt(have)
        assert total(toks) + VAL[right] == target
        for w in wrongs:
            assert total(toks) + VAL[w] != target
        q = fig(money_svg(toks)) + "Which coin do you add to make %s?" % lab(target)
        its.append(mcq(q, lab(VAL[right]), [lab(VAL[w]) for w in wrongs], e))

    missing(C("20p", "10p"), 35, "C5", ["C20", "C10", "C2"],
            "20p + 10p = 30p. 30p + 5p = 35p. Add a <b>5p</b> coin.")
    missing(C("50p", "20p"), 75, "C5", ["C20", "C10", "C2"],
            "50p + 20p = 70p. 70p + 5p = 75p. Add a <b>5p</b> coin.")
    missing(C("10p", "10p", "5p"), 27, "C2", ["C5", "C1", "C10"],
            "10p + 10p + 5p = 25p. 25p + 2p = 27p. Add a <b>2p</b> coin.")
    missing(C("50p", "20p", "20p"), 100, "C10", ["C50", "C20", "C5"],
            "£1 = 100p. 50p + 20p + 20p = 90p. 90p + 10p = 100p. Add a <b>10p</b> coin.")
    missing(C("£10", "£2", "£2"), 1500, "C100", ["N5", "C200", "N10"],
            "£10 + £2 + £2 = £14. £14 + £1 = £15. Add a <b>£1</b> coin.")

    # fewest coins
    for amt, wr in [(30, [3, 1, 6]), (70, [3, 1, 7]), (9, [2, 4, 9]), (80, [2, 4, 8]), (800, [4, 2, 8])]:
        best = fewest(amt)
        n = len(best)
        assert n not in wr
        unit = "notes and coins" if amt >= 100 else "coins"
        q = "What is the fewest %s you need to make %s?" % (unit, lab(amt))
        bits = combo(best)
        e = "Use the biggest %s you can first: %s = %s. That is <b>%d %s</b>." % (
            "note or coin" if amt >= 100 else "coin", bits, lab(amt), n, unit)
        if amt == 30:
            e += " There is no 30p coin, so 1 coin cannot work."
        if amt == 9:
            e += " There is no 4p coin, so you need two 2p coins."
        its.append(mcq(q, "%d %s" % (n, unit), ["%d %s" % (x, unit if x != 1 else unit[:-1]) for x in wr], e))
    assert len(its) == 20
    return {"title": "Make an amount", "items": its}


# ============================================================ set 4: add money
TUCK = [("apple", 20), ("toast", 25), ("milk", 30), ("biscuit", 15), ("juice", 40)]
TOYS = [("ball", 400), ("kite", 700), ("car", 300), ("book", 500), ("game", 900)]
A_THING = {"apple": "an apple", "toast": "some toast", "milk": "a carton of milk", "biscuit": "a biscuit", "juice": "a juice",
           "ball": "a ball", "kite": "a kite", "car": "a toy car", "book": "a book", "game": "a game"}


def add_e_p(nums):
    T = sum(nums)
    if len(nums) == 2:
        a, b = nums
        tens, ones = b // 10 * 10, b % 10
        steps = []
        s = a
        if tens:
            steps.append("%s + %s = %s" % (p(s), p(tens), p(s + tens)))
            s += tens
        if ones:
            steps.append("%s + %s = %s" % (p(s), p(ones), p(s + ones)))
            s += ones
        assert s == T
        return "Add the tens, then the ones: %s. The total is <b>%s</b>." % (", ".join(steps), p(T))
    run, s = [], 0
    for n in nums:
        s += n
        run.append(p(s))
    return "Add one price at a time: %s. The total is <b>%s</b>." % (", ".join(run), p(T))


def set_add(P, rnd):
    its = []
    plain = [[20, 30], [15, 10], [40, 25], [35, 20], [38, 25], [47, 36], [55, 45], [12, 15, 20]]
    for nums in plain:
        T = sum(nums)
        assert T <= 100
        q = "%s = ?" % " + ".join(p(n) for n in nums)
        cands = [noexch_add(nums) if noexch_add(nums) != T else None]
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        cands += [T + 10, T - 10, T + 1, T - 1]
        w = pc(cands)
        if T == 100:
            w = ["£100"] + w
        e = add_e_p(nums) + (" 100p is the same as £1." if T == 100 else "")
        if noexch_add(nums) != T:
            e += " The ones make more than 10, so exchange 10 ones for 1 ten."
        its.append(mcq(q, p(T), w, e))
    shop = [("apple", "milk"), ("toast", "biscuit"), ("juice", "toast"), ("milk", "juice"),
            ("apple", "toast", "biscuit"), ("biscuit", "milk", "juice")]
    price = dict(TUCK)
    for x in shop:
        nums = [price[n] for n in x]
        T = sum(nums)
        assert T <= 100
        nm, he, his = P.next()
        what = ", ".join(A_THING[n] for n in x[:-1]) + " and " + A_THING[x[-1]]
        q = fig(price_svg(TUCK, "tuck shop", p)) + "At the tuck shop, %s buys %s. How much does %s spend?" % (nm, what, he)
        cands = [noexch_add(nums) if noexch_add(nums) != T else None]
        if len(nums) == 2:
            cands.append(abs(nums[0] - nums[1]))
        else:
            cands.append(T - nums[-1])
        cands += [T + 10, T - 10, T - 5, T + 5]
        its.append(mcq(q, p(T), pc(cands), add_e_p(nums)))
    for nums in ([600, 800], [1000, 500]):
        T = sum(nums)
        q = "%s = ?" % " + ".join(pd(n) for n in nums)
        e = "Add the pounds: %d + %d = %d. The total is <b>%s</b>." % (nums[0] // 100, nums[1] // 100, T // 100, pd(T))
        its.append(mcq(q, pd(T), ["%dp" % (T // 100), pd(abs(nums[0] - nums[1])), pd(T + 100), pd(T - 100)],
                       e + " The answer is in pounds, not pence."))
    price = dict(TOYS)
    for x in [("ball", "car"), ("kite", "book"), ("game", "kite"), ("car", "game", "book")]:
        nums = [price[n] for n in x]
        T = sum(nums)
        assert T <= 2000
        nm, he, his = P.next()
        what = ", ".join(A_THING[n] for n in x[:-1]) + " and " + A_THING[x[-1]]
        q = fig(price_svg(TOYS, "toy shop", pd)) + "At the toy shop, %s buys %s. How much does %s spend?" % (nm, what, he)
        run, s = [], 0
        for n in nums:
            s += n
            run.append(pd(s))
        e = "Add the prices: %s = <b>%s</b>." % (" + ".join(pd(n) for n in nums), pd(T))
        if len(nums) == 3:
            e = "Add one price at a time: %s. The total is <b>%s</b>." % (", ".join(run), pd(T))
        cands = ["%dp" % (T // 100)]
        cands.append(pd(abs(nums[0] - nums[1])) if len(nums) == 2 else pd(T - nums[-1]))
        cands += [pd(T + 100), pd(T - 100)]
        its.append(mcq(q, pd(T), cands, e))
    assert len(its) == 20
    return {"title": "Add amounts of money", "items": its}


# ============================================================ set 5: change and word problems
def set_words(P, rnd):
    its = []

    def add(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    def change(price, paid, thing, coin, extra=None, line=False):
        nm, he, his = P.next()
        r = paid - price
        q = "%s buys %s for %s. %s pays with %s. How much change does %s get?" % (nm, thing, p(price), cap(he), coin, he)
        if line:
            q = fig(change_line(price, paid, show=False)) + q
        pre = "£1 = 100p. " if paid == 100 else ""
        e = pre + count_on(price, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (p(r), p(price), p(r), p(paid))
        if extra:
            e += " " + extra
        w = [price + paid if price + paid <= 100 else None, small_from_big(paid, price) if paid < 100 else None,
             r + 10, price, r - 10, r + 1, r - 1]
        add(q, p(r), pc(w), e)

    change(6, 10, "a sweet", "a 10p coin")
    change(15, 20, "a sticker", "a 20p coin")
    change(35, 50, "a lolly", "a 50p coin", "It is not 25p: 35p + 25p = 60p.", line=True)
    change(40, 100, "an apple", "a £1 coin")
    change(65, 100, "a bag of crisps", "a £1 coin", "It is not 45p: 65p + 45p = 110p.", line=True)
    change(72, 100, "a bottle of water", "a £1 coin")

    nm, he, his = P.next()
    add("%s gets £2 pocket money each week. How much does %s have after 5 weeks?" % (nm, he), "£10",
        ["£7", "10p", "£12"], "Count in 2s: £2, £4, £6, £8, £10. That is <b>£10</b>. £7 comes from adding 2 + 5.")
    nm, he, his = P.next()
    add("%s has £10. %s buys a book for £6. How much money is left?" % (nm, cap(he)), "£4",
        ["£16", "4p", "£6"], "£10 − £6 = £4. Count on: £6 to £10 is <b>£4</b>. £16 adds instead of taking away.")
    nm, he, his = P.next()
    add("A toy car costs £8. %s has £5. How much more money does %s need?" % (nm, he), "£3",
        ["£13", "£5", "3p"], "Count on from £5 to £8: £6, £7, £8. That is <b>£3</b> more.")
    nm, he, his = P.next()
    add("%s has 45p. %s gran gives %s 30p. How much does %s have now?" % (nm, cap(his), "her" if he == "she" else "him", he),
        "75p", ["15p", "65p", "£75"], "45p + 30p: 45p, 55p, 65p, 75p. That is <b>75p</b>. 15p takes away instead of adding.")
    nm, he, his = P.next()
    assert 15 + 30 == 45 and 50 - 45 == 5
    add("At the tuck shop, %s buys a biscuit for 15p and a carton of milk for 30p. %s pays with a 50p coin. How much change does %s get?"
        % (nm, cap(he), he), "5p", ["45p", "35p", "20p"],
        "Cost: 15p + 30p = 45p. Count on from 45p to 50p: <b>5p</b>. 45p is the cost, not the change.")
    nm, he, his = P.next()
    add("Apples cost 20p each. %s buys 2 apples. How much does %s pay?" % (nm, he), "40p",
        ["22p", "20p", "£40"], "20p + 20p = <b>40p</b>. 22p adds 20 + 2.")
    nm, he, his = P.next()
    add("Pencils cost 10p each. How many pencils can %s buy with 50p?" % nm, "5 pencils",
        ["50 pencils", "10 pencils", "4 pencils"], "Count in 10s to 50p: 10p, 20p, 30p, 40p, 50p. That is <b>5 pencils</b>.")
    nm, he, his = P.next()
    assert 3 * 20 - 45 == 15
    add("%s has three 20p coins. %s spends 45p. How much money is left?" % (nm, cap(he)), "15p",
        ["25p", "45p", "60p"], "Three 20p coins: 20p, 40p, 60p. Count on from 45p to 60p: 45p + 5p = 50p, 50p + 10p = 60p. "
        "5p + 10p = <b>15p</b> is left.")
    nm, he, his = P.next()
    add("A comic costs £4. %s pays with a £10 note. How much change does %s get?" % (nm, he), "£6",
        ["£14", "6p", "£5"], "£10 − £4 = £6. Check: £4 + £6 = £10. The change is <b>£6</b>.")
    nm, he, his = P.next()
    assert 2000 - 1200 - 500 == 300
    add("%s has £20. %s buys a game for £12 and a ball for £5. How much money is left?" % (nm, cap(he)), "£3",
        ["£8", "£17", "£15"], "Spent: £12 + £5 = £17. Count on from £17 to £20: <b>£3</b> is left. "
        "£8 only takes away the game.")
    nm, he, his = P.next()
    assert 25 + 25 + 30 == 80
    add("At the school fair, cakes cost 25p each. %s buys 2 cakes and a juice for 30p. How much does %s spend?" % (nm, he),
        "80p", ["55p", "50p", "£80"], "Cakes: 25p + 25p = 50p. Add the juice: 50p + 30p = <b>80p</b>. 55p is only 1 cake.")
    nm, he, his = P.next()
    assert 30 + 25 == 55
    add("%s has 50p. Crisps cost 30p and a juice costs 25p. Can %s buy both?" % (nm, he),
        "No, %s needs 5p more." % he, ["Yes, with 5p left.", "Yes, with 20p left.", "No, %s needs 15p more." % he],
        "Cost: 30p + 25p = 55p. 55p is more than 50p, so <b>no</b>. 50p + 5p = 55p, so %s needs 5p more." % he)
    nm, he, his = P.next()
    assert 500 + 500 + 300 == 1300
    add("%s has two £5 notes and three £1 coins. How much money does %s have?" % (nm, he), "£13",
        ["£5", "£8", "13p"], "£5 + £5 = £10. Then £11, £12, £13. That is <b>£13</b>. £5 counts the notes and coins, not their value.")
    nm, he, his = P.next()
    assert 100 - 30 == 70
    add("%s buys a drink for 30p. %s pays with a £1 coin. Which coins could %s get as change?" % (nm, cap(he), he), "50p + 20p",
        ["50p + 10p + 5p", "20p + 20p + 20p", "50p + 20p + 10p"],
        "£1 = 100p. Count on from 30p to 100p: 70p. 50p + 20p = 70p, so <b>50p + 20p</b>.")
    assert len(its) == 20
    return {"title": "Change and money word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C1", "C2", "C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20"]
    walk = toks_of(("C20", 2), ("C10", 1), ("C5", 1), ("C2", 1))
    under = ["20p", "40p", "50p", "55p", "57p"]
    assert total(walk) == 57
    return (
        "<h2>Pounds and pence</h2>"
        "<p>We write pence with a small p: 50p. We write pounds with the £ sign in front: £5. "
        "£1 is the same as 100p.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=8, label="UK coins: 1p, 2p, 5p, 10p, 20p, 50p, £1, £2") +
        "<figcaption>Coins: 1p, 2p, 5p, 10p, 20p, 50p, £1 and £2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, label="UK notes: £5, £10, £20") +
        "<figcaption>Notes: £5, £10 and £20.</figcaption></figure>"
        "<p>A big coin is not always worth more. The 2p coin is bigger than the 5p coin, but 5p is worth more. "
        "Always read the number.</p>"
        "<h2>Count the coins, biggest first</h2>"
        "<p>Put the coins in order. Start with the biggest value and count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=18, under=under, label="counting on: 20p, 40p, 50p, 55p, 57p") +
        "<figcaption>20p, 40p, 50p, 55p, 57p. The total is 57p.</figcaption></figure>"
        + ex("Example", "Find two ways to make 30p.",
             "20p + 10p = 30p. 10p + 10p + 10p = 30p. 20p + 10p uses the fewest coins.", "20p + 10p or 10p + 10p + 10p")
        + ex("Example", "Add 35p + 20p.", "Add the tens: 35p, 45p, 55p.", "55p")
        + "<h2>Give change by counting on</h2>"
        "<p>Start at the price. Count on to the money you paid. The jumps are the change.</p>"
        "<figure class='sn-fig'>" + change_line(35, 50) +
        "<figcaption>Change from 50p for 35p: 5p + 10p = 15p.</figcaption></figure>"
        + ex("Example", "A drink costs 65p. You pay with a £1 coin. What is the change?",
             "£1 = 100p. 65p + 5p = 70p. 70p + 30p = 100p. 5p + 30p = 35p.", "35p")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 coins, so 4p", "Count the value of each coin: 20p, 40p, 50p, 52p"],
            ["£5 is the same as 5p", "£5 is five pounds. £1 alone is 100p"],
            ["85p written as £85", "Pence have p after the number: 85p"],
            ["Change from 50p for 35p is 25p", "Count on: 35p + 5p = 40p, 40p + 10p = 50p. The change is 15p"],
        ])
    )


FAQ = [
    {"q": "What should a Year 2 child know about money?",
     "a": "In the National Curriculum, Year 2 pupils use the £ and p symbols, count coins and notes, find different ways to make the same amount, and add and subtract money to work out change."},
    {"q": "How many pence are in £1?",
     "a": "There are 100 pence in £1. So two 50p coins, five 20p coins or ten 10p coins all make £1."},
    {"q": "How do you teach a Year 2 child to give change?",
     "a": "Count on from the price to the money paid. For 35p paid with 50p: 35p to 40p is 5p, 40p to 50p is 10p, so the change is 15p."},
    {"q": "Why does my child think the 2p coin is worth more than the 5p coin?",
     "a": "The 2p coin is bigger, and young children often judge by size. Ask them to read the number on each coin before they count."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(2208)
    P = People(rnd)
    sets = [set_symbols(P, rnd), set_count(P, rnd), set_make(P, rnd), set_add(P, rnd), set_words(P, rnd)]
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
                assert not re.search(r"£\d+p|\.\d", c), c
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "uk", "subject": "maths", "grade": "year-2", "slug": "money", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Coins, Notes and Giving Change",
        "seo_title": "Year 2 Money Worksheets: Coins, £ and p, Adding and Change",
        "short_title": "Money",
        "domain": "Measurement",
        "standard_code": "Year 2: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise and use symbols for pounds (£) and pence (p); combine amounts to make a particular value; find different combinations of coins that equal the same amounts of money; solve simple problems in a practical context involving addition and subtraction of money of the same unit, including giving change.",
        "meta_desc": "Free Year 2 maths worksheets on money: recognise UK coins and notes, use £ and p, count coins, find different ways to make 25p or £15, add prices at the tuck shop and give change from 50p or £1 by counting on. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Read the number on each coin, then count on from the biggest.",
        "key_sub": "£1 = 100p. Write pence as 50p and pounds as £5. To give change, count on from the price: 35p to 50p is 15p.",
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
