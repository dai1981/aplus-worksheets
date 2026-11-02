# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Money (Ontario Mathematics Curriculum 2020, Grade 2: F1.1)
  python3 tools/gen_caon_math_g2_money.py
Grade 2: the same amount of money in different ways, up to 200¢ with coins and up to $200 with
loonies, toonies and $5, $10, $20, $50 and $100 bills. Coin amounts are written in cents (135¢), bill and
dollar-coin amounts in whole dollars ($45). No $1.35-type amounts and no making change (that is Grade 3).
Canadian coins: nickel 5¢, dime 10¢ (the smallest coin), quarter 25¢, loonie $1 (11 sides, gold colour),
toonie $2 (silver ring, gold centre). No pennies. Bills: $5 blue, $10 purple, $20 green, $50 red, $100 brown.
Coins and bills are simple labelled shapes (no real designs). Short sentences for 7-8 year olds.
Wrong answers come from real mistakes: counting coins instead of their value, a quarter taken as 20¢,
the bigger nickel taken as 10¢ and the small dime as 5¢, a toonie counted as $1, counting every coin or bill
as $1, missing or double-counting one coin, keeping the old step when the coin changes, adding when the
question takes away.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
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
BYVAL = {v: k for k, v in VAL.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius in proportion to the real coins (mm): dime 18, nickel 21.2, quarter 23.9, loonie 26.5, toonie 28
COIN = {"D": (18, SILVER, 14), "N": (21, SILVER, 15), "Q": (24, SILVER, 15), "L": (26, GOLD, 16), "T": (28, SILVER, 16)}
BILL = {"B5": ("#c4dcf2", "#1f5f99"), "B10": ("#ddcbee", "#5b2d8a"), "B20": ("#cbe7c4", "#2f7a2a"),
        "B50": ("#f5c6c6", "#a32020"), "B100": ("#e8d6c2", "#7a4a1c")}
BILL_W, BILL_H = 80, 42


def lab(v):
    """label on a coin or bill: $1, $2, $5 … or 5¢, 10¢, 25¢"""
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def C(v):
    """an amount in cents (Grade 2 counts coins in cents, to 200¢)"""
    assert isinstance(v, int) and v > 0, v
    return "%d¢" % v


def D(v):
    """a whole-dollar amount (v in cents)"""
    assert isinstance(v, int) and v > 0 and v % 100 == 0, v
    return "$%d" % (v // 100)


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


def words(vals):
    """[25, 10, 10] -> '1 quarter, 2 dimes'"""
    toks = srt([BYVAL[v] for v in vals])
    return ", ".join(nw(n, t) for t, n in counts(toks))


def vb(vals):
    return "makes" if len(vals) == 1 else "make"


def andw(vals):
    """[25, 10, 10] -> '1 quarter and 2 dimes' (for explanations)"""
    return group(srt([BYVAL[v] for v in vals]))


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ explanations
def count_on(toks, fmt):
    toks = srt(toks)
    T = total(toks)
    s, run = 0, []
    for t in toks:
        s += VAL[t]
        run.append(fmt(s))
    if len(toks) == 1:
        return "One %s is <b>%s</b>." % (ONE[toks[0]], fmt(T))
    if len(set(toks)) == 1:
        t = toks[0]
        return "Each %s is %s. Count by %s: %s. That is <b>%s</b>." % (ONE[t], fmt(VAL[t]), fmt(VAL[t]), ", ".join(run), fmt(T))
    return "Start with the biggest one and count on: %s. That is <b>%s</b>." % (", ".join(run), fmt(T))


# ------------------------------------------------------------ typical mistakes (all computed, in cents)
def m_count(toks):
    """counted the coins, not their value (cents)"""
    return len(toks)


def m_each_dollar(toks):
    """counted every coin and bill as $1"""
    return 100 * len(toks)


def m_quarter20(toks):
    return sum(20 if t == "Q" else VAL[t] for t in toks)


def m_swap(toks):
    """the bigger nickel taken as 10¢ and the small dime as 5¢"""
    sw = {"N": 10, "D": 5}
    return sum(sw.get(t, VAL[t]) for t in toks)


def m_toonie1(toks):
    return sum(100 if t == "T" else VAL[t] for t in toks)


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
def mcq(q, correct, cands, e, fmt):
    """4 choices: correct + the first 3 usable unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or (fmt is D and c % 100) or (fmt is C and c > 400):
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
    return svg_wrap(w + 8, h + 8, draw_tok(t, (w + 8) / 2, (h + 8) / 2), "one coin")


def price_svg(items, title, fmt):
    """a row of price tags: [('apple', 25), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 18, 70) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, fmt(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, fmt(p)) for n, p in items))


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


# ============================================================ set 1: names and values
def set_names(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=str):
        its.append(mcq(q, right, wrong, e, fmt))

    tips = {
        "L": ("loonie", ["toonie", "quarter", "dime"],
              "This is a <b>loonie</b>. It is gold in colour and has 11 sides. It is worth $1."),
        "T": ("toonie", ["loonie", "quarter", "nickel"],
              "This is a <b>toonie</b>. It has a silver ring and a gold centre. It is worth $2."),
        "D": ("dime", ["nickel", "quarter", "loonie"],
              "This is a <b>dime</b>. It is worth 10¢. It is the smallest coin."),
        "N": ("nickel", ["dime", "quarter", "toonie"],
              "This is a <b>nickel</b>. It is worth 5¢. It is bigger than a dime, but worth less."),
        "Q": ("quarter", ["dime", "nickel", "loonie"],
              "This is a <b>quarter</b>. It is worth 25¢."),
    }
    for t in ["N", "D", "Q", "L", "T"]:
        right, wrong, e = tips[t]
        s(fig(coin_svg(t)) + "What is this coin called?", right, wrong, e)
    s("How much is a nickel worth?", 5, [10, 25, 1],
      "A nickel is worth <b>5¢</b>. Two nickels make a dime.", C)
    s("How much is a dime worth?", 10, [5, 25, 1],
      "A dime is worth <b>10¢</b>. It is small, but it is worth more than a nickel.", C)
    s("How much is a quarter worth?", 25, [20, 50, 10],
      "A quarter is worth <b>25¢</b>, not 20¢. Four quarters make 100¢.", C)
    s("A loonie is worth $1. How many cents is that?", 100, [1, 10, 200],
      "$1 is <b>100¢</b>. So a loonie is worth 100¢.", C)
    s("A toonie is worth $2. How many cents is that?", 200, [2, 100, 20],
      "$1 is 100¢, so $2 is 100¢ + 100¢ = <b>200¢</b>.", C)
    s("Which coin has 11 sides?", "the loonie", ["the toonie", "the quarter", "the dime"],
      "The <b>loonie</b> has 11 sides. It is gold in colour.")
    s(fig(money_svg(["D", "N"], gap=14, under=["dime", "nickel"], label="a dime (small) and a nickel (bigger)"))
      + "Which coin is worth more?",
      "the dime", ["the nickel", "They are the same.", "You cannot tell."],
      "The <b>dime</b> is worth 10¢. The nickel is worth 5¢. A bigger coin is not always worth more.")
    s(fig(money_svg(["Q", "D", "L", "N"], gap=10, under=["quarter", "dime", "loonie", "nickel"],
                    label="a quarter, a dime, a loonie and a nickel"))
      + "Which coin is worth the least?",
      "the nickel", ["the dime", "the quarter", "the loonie"],
      "Nickel 5¢, dime 10¢, quarter 25¢, loonie 100¢. The <b>nickel</b> is worth the least.")
    s(fig(money_svg(["T", "B5"], gap=14, under=["toonie", "$5 bill"], label="a toonie and a $5 bill"))
      + "Which is worth more?",
      "the $5 bill", ["the toonie", "They are the same.", "You cannot tell."],
      "A toonie is $2. The bill is $5. $5 is more than $2, so the <b>$5 bill</b> is worth more.")
    s("How many nickels make a dime?", "2", ["5", "10", "1"],
      "A nickel is 5¢. 5¢ + 5¢ = 10¢. So <b>2</b> nickels make a dime.")
    s("How many nickels make a quarter?", "5", ["25", "4", "2"],
      "Count by 5s: 5¢, 10¢, 15¢, 20¢, 25¢. That is <b>5</b> nickels. 4 nickels make only 20¢.")
    s("How many quarters make 100¢?", "4", ["5", "25", "10"],
      "Count by 25s: 25¢, 50¢, 75¢, 100¢. That is <b>4</b> quarters. 5 is right only if a quarter were 20¢.")
    s("How many dimes make 100¢?", "10", ["100", "1", "5"],
      "Count by 10s: 10¢, 20¢, 30¢ … 100¢. That is <b>10</b> dimes.")
    s("How many loonies make a toonie?", "2", ["1", "20", "200"],
      "A loonie is $1. A toonie is $2. $1 + $1 = $2, so <b>2</b> loonies make a toonie.")
    s("How many $10 bills make $100?", "10", ["100", "1", "5"],
      "Count by 10s: $10, $20, $30 … $100. That is <b>10</b> bills.")
    assert len(its) == 20
    return {"title": "Coins and bills: names and values", "items": its}


# ============================================================ set 2: count coins in cents
def count_set(P, rnd, groups, mixed, fmt, cents, title):
    its = []
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "%s finds this money in %s backpack. How much is it?", "What is the total?",
             "%s puts this money in a piggy bank. How much is in the bank?"]
    seen_t = set()
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T not in seen_t, T
        seen_t.add(T)
        assert len(toks) <= 8
        if cents:
            assert T <= 200
        else:
            assert T <= 20000 and T % 100 == 0
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
        e = ("Put the money in order, biggest first. " if i in mixed else "") + count_on(toks, fmt)
        if i < 3 and cents:
            e += " Count the value of each coin, not the number of coins."
        if cents:
            cands = [m_count(toks), m_quarter20(toks), m_swap(toks), m_same_step(toks), m_skip(toks, -1),
                     m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
            if i % 2:
                cands = [m_quarter20(toks)] + cands
        else:
            cands = [m_each_dollar(toks), m_toonie1(toks), m_skip(toks, -1), m_twice(toks, -1),
                     m_same_step(toks), m_skip(toks, 0), m_twice(toks, 0), T - 200, T + 200, C(len(toks))]
            if i % 2:
                cands = [m_toonie1(toks)] + cands
        it = mcq(q, T, cands, e, fmt)
        if cents and C(len(toks)) in it["c"]:
            it["e"] += " %s counts the coins, not the cents." % C(len(toks))
        if cents and "Q" in toks and C(m_quarter20(toks)) in it["c"] and m_quarter20(toks) != T:
            it["e"] += " A quarter is 25¢, not 20¢."
        if not cents and m_each_dollar(toks) != T and D(m_each_dollar(toks)) in it["c"]:
            it["e"] += " %s counts each piece as $1." % D(m_each_dollar(toks))
        its.append(it)
    assert len(its) == 20
    return {"title": title, "items": its}


def set_cents(P, rnd):
    groups = [
        [("D", 4)], [("N", 6)], [("Q", 3)], [("Q", 1), ("D", 2)], [("D", 3), ("N", 1)],
        [("Q", 2), ("D", 1), ("N", 1)], [("Q", 1), ("D", 1), ("N", 3)], [("Q", 1), ("D", 3)],
        [("Q", 2), ("D", 3), ("N", 1)], [("Q", 3), ("D", 1), ("N", 2)], [("Q", 4)], [("Q", 5)],
        [("L", 1), ("Q", 2)], [("L", 1), ("D", 3), ("N", 1)], [("Q", 3), ("D", 3), ("N", 2)],
        [("L", 1), ("Q", 1), ("D", 1), ("N", 1)], [("L", 1), ("Q", 2), ("D", 2)], [("L", 1), ("Q", 3), ("D", 1)],
        [("L", 1), ("Q", 2), ("D", 4)], [("L", 2)],
    ]
    return count_set(P, rnd, groups, {6, 9, 14, 15, 17, 18}, C, True, "Count coins in cents (to 200¢)")


def set_dollars(P, rnd):
    groups = [
        [("L", 4)], [("T", 3)], [("T", 2), ("L", 1)], [("B5", 1), ("L", 2)], [("B5", 1), ("T", 2)],
        [("B10", 1), ("T", 1), ("L", 1)], [("B10", 1), ("B5", 1)], [("B5", 6)], [("B20", 1), ("B10", 1), ("B5", 1)],
        [("B20", 2), ("T", 2)], [("B10", 5)], [("B50", 1), ("B10", 2)], [("B20", 4)],
        [("B50", 1), ("B20", 1), ("B5", 1), ("L", 2)], [("B50", 1), ("B20", 2), ("B5", 1), ("T", 1)],
        [("B100", 1), ("B20", 1)], [("B100", 1), ("B20", 2), ("B5", 1)], [("B100", 1), ("B50", 1), ("B10", 1)],
        [("B100", 1), ("B50", 1), ("B20", 1), ("T", 2), ("L", 1)], [("B100", 1), ("B50", 1), ("B20", 2), ("B10", 1)],
    ]
    return count_set(P, rnd, groups, {5, 9, 13, 14, 16, 18}, D, False, "Count dollars (to $200)")


# ============================================================ set 4: the same amount in different ways
def fewest(target, coins):
    best = {0: []}
    step = min(coins)
    for a in range(step, target + 1, step):
        opts = [best[a - c] + [c] for c in coins if a - c in best]
        if opts:
            best[a] = min(opts, key=len)
    return best[target]


def fm(v):
    return C(v) if v <= 200 or v % 100 else D(v)


def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None, fmt=C):
        assert sum(right) == target, (target, right)
        vs = {sum(w) for w in wrong}
        assert len(vs) == 3 and target not in vs, (target, wrong)
        q = (stem or "Which makes %s?") % fmt(target)
        e = ("<b>%s</b> %s %s. " % (cap(andw(right)), vb(right), fmt(target)) + " ".join(
            "%s %s %s." % (cap(andw(w)), vb(w), fmt(sum(w))) for w in wrong))
        its.append(mcq(q, words(right), [words(w) for w in wrong], e, str))

    def which_not(target, right, wrong, fmt=C):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> %s %s, not %s. The others all make %s."
             % (cap(andw(right)), vb(right), fmt(sum(right)), fmt(target), fmt(target)))
        its.append(mcq("Which does <b>not</b> make %s?" % fmt(target), words(right), [words(w) for w in wrong], e, str))

    def same_as(toks, right, wrong, fmt=C):
        T = total(toks)
        assert sum(right) == T and all(sum(w) != T for w in wrong) and len({sum(w) for w in wrong}) == 3
        q = fig(money_svg(toks)) + "Which is worth the same as this money?"
        e = count_on(toks, fmt) + " <b>%s</b> also %s %s." % (cap(andw(right)), vb(right), fmt(T))
        its.append(mcq(q, words(right), [words(w) for w in wrong], e, str))

    same_as(["N", "N"], [10], [[5], [25], [10, 10]])
    same_as(["D"] * 5, [25, 25], [[5] * 5, [100], [25, 25, 25]])
    same_as(["Q"] * 4, [100], [[25], [200], [10] * 4])
    which(35, [25, 10], [[25, 5], [10, 10, 10, 10], [25, 25]])
    which(50, [25, 25], [[25, 10, 10], [10, 10, 10], [25, 25, 5]])
    which_not(60, [25, 25, 5], [[25, 25, 10], [25, 10, 10, 10, 5], [10] * 6])
    nm, he, his = P.next()
    which(45, [25, 10, 10], [[25, 10, 5], [25, 25, 5], [10, 10, 10]],
          stem=nm + " has 3 coins. They make %s. Which coins does " + he + " have?")
    which(75, [25, 25, 25], [[25, 25, 10, 10], [25, 25, 10], [25] * 4])
    which_not(100, [25, 25, 25, 10, 10], [[25] * 4, [25, 25, 25, 10, 10, 5], [10] * 10])
    same_as(toks_of(("L", 1), ("Q", 2)), [25] * 6, [[200], [25] * 5, [100, 10, 10, 10, 10]])
    which(120, [100, 10, 10], [[100, 5, 5], [100, 25, 25], [25, 25, 25, 25, 5]])
    which(200, [25] * 8, [[25] * 7, [100, 25, 25], [100] + [10] * 9],
          stem="Which makes %s, the same as a toonie?")
    same_as(["L", "L"], [200], [[100], [25, 25], [500]])
    which(500, [200, 200, 100], [[200, 200], [200] * 5, [200, 100]], fmt=D)
    same_as(["B10"], [200] * 5, [[100] * 5, [200] * 10, [200, 200]], fmt=D)
    which(2000, [500] * 4, [[500, 500], [500] * 5, [500] * 3], fmt=D)
    which_not(5000, [2000, 2000, 500], [[1000] * 5, [2000, 2000, 1000], [2000, 1000, 1000, 1000]], fmt=D)
    which(10000, [2000] * 5, [[2000] * 4, [5000, 2000], [500] * 10], fmt=D)
    same_as(["B50", "B50"], [10000], [[5000], [10000, 10000], [2000]], fmt=D)
    nm, he, his = P.next()
    which(7000, [5000, 1000, 1000], [[2000] * 3, [2000, 2000, 1000], [5000, 2000, 500]], fmt=D,
          stem=nm + " has 3 bills. They make %s. Which bills does " + he + " have?")
    assert len(its) == 20
    return {"title": "Make the same amount in different ways", "items": its}


# ============================================================ set 5: fewest coins and word problems
SNACKS = [("apple", 25), ("juice box", 50), ("popcorn", 35), ("cookie", 40)]


def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=C):
        its.append(mcq(q, right, cands, e, fmt))

    def ncoins(k, w="coin"):
        return "%d %s" % (k, w if k == 1 else w + "s")

    def how_few(target, coins, wrong, extra, fmt=C, w="coins"):
        f = fewest(target, coins)
        n = len(f)
        e = ("Use the biggest one you can each time: %s %s %s. That is <b>%s</b>. %s"
             % (andw(f), vb(f), fmt(target), ncoins(n, w[:-1]), extra))
        its.append(mcq("What is the smallest number of %s you can use to make %s?" % (w, fmt(target)),
                       ncoins(n, w[:-1]), [ncoins(k, w[:-1]) for k in wrong], e, str))

    def which_fewest(target, coins, wrong, w="coins", fmt=C):
        f = fewest(target, coins)
        for x in wrong:
            assert sum(x) == target and len(x) > len(f)
        e = ("All of these make %s. <b>%s</b> use only %d %s. Start with the biggest one you can."
             % (fmt(target), cap(andw(f)), len(f), w))
        its.append(mcq("Which uses the fewest %s to make %s?" % (w, fmt(target)), words(f), [words(x) for x in wrong], e, str))

    CO = [5, 10, 25, 100, 200]
    how_few(30, CO, [1, 3, 6], "There is no 30¢ coin. Three dimes work, but 2 coins is fewer.")
    which_fewest(40, CO, [[10] * 4, [25, 5, 5, 5], [10, 10, 10, 5, 5]])
    how_few(65, CO, [3, 5, 7], "Three coins can make 60¢ or 75¢, but not 65¢.")
    how_few(150, CO, [6, 2, 15], "6 quarters also make 150¢, but that is 6 coins.")
    how_few(700, [100, 200], [7, 3, 5], "Seven loonies work, but that is 7 coins. Three toonies make only $6.", fmt=D)
    which_fewest(3500, [500, 1000, 2000], [[1000, 1000, 1000, 500], [2000, 500, 500, 500], [500] * 7], w="bills", fmt=D)
    how_few(8000, [500, 1000, 2000, 5000, 10000], [4, 8, 2], "4 $20 bills also make $80, but 3 bills is fewer.",
            fmt=D, w="bills")

    sp = dict(SNACKS)
    nm, he, his = P.next()
    assert sp["popcorn"] + sp["juice box"] == 85
    add(fig(price_svg(SNACKS, "snack sale", C)) + "%s buys popcorn and a juice box. How much does %s spend?" % (nm, he),
        85, [15, 75, 95],
        "35¢ + 50¢: 30¢ + 50¢ = 80¢. 80¢ + 5¢ = <b>85¢</b>. 15¢ is the difference, not the total.")
    nm, he, his = P.next()
    assert 25 * 2 + 10 == 60 and 60 - 45 == 15
    add("%s has 2 quarters and 1 dime. An apple costs 45¢. Can %s buy it?" % (nm, he),
        "Yes, with 15¢ left.", ["No, %s needs 15¢ more." % he, "Yes, with 5¢ left.", "Yes, %s has exactly 45¢." % he],
        "Count: 25¢, 50¢, 60¢. %s has 60¢. 60¢ is more than 45¢. 45¢ + 15¢ = 60¢, so <b>yes, with 15¢ left</b>. "
        "5¢ left comes from counting a quarter as 20¢." % nm, str)
    nm, he, his = P.next()
    assert 3 * 10 + 2 * 5 == 40
    add("%s has 3 dimes and 2 nickels. A cookie costs 45¢. Can %s buy it?" % (nm, he),
        "No, %s needs 5¢ more." % he, ["Yes, with 5¢ left.", "No, %s needs 10¢ more." % he, "Yes, %s has exactly 45¢." % he],
        "Dimes: 10¢, 20¢, 30¢. Nickels: 35¢, 40¢. %s has 40¢. 40¢ + 5¢ = 45¢, so <b>no, %s needs 5¢ more</b>." % (nm, he), str)
    nm, he, his = P.next()
    add("A muffin costs 75¢. %s has 50¢. How much more does %s need?" % (nm, he), 25, [125, 35, 20],
        "Count up from 50¢: 50¢ + 25¢ = 75¢. %s needs <b>25¢</b> more. 125¢ adds instead of finding the difference." % cap(he))
    nm, he, his = P.next()
    toks = toks_of(("L", 1), ("Q", 2), ("D", 3))
    assert total(toks) == 180
    add(fig(money_svg(toks)) + "For the Terry Fox Run, %s gives these coins. How much does %s give?" % (nm, he),
        180, [m_count(toks), m_quarter20(toks), 80],
        count_on(toks, C) + " 6¢ counts the coins. 80¢ forgets that the loonie is 100¢.")
    nm, he, his = P.next()
    add("%s has 90¢. %s buys a pencil for 40¢. How much does %s have left?" % (nm, cap(he), he), 50, [130, 60, 40],
        "Take away: 90¢ − 40¢ = <b>50¢</b>. Check: 40¢ + 50¢ = 90¢. 130¢ adds instead of taking away.")
    nm, he, his = P.next()
    add("Lemonade costs 25¢ a cup. %s buys 4 cups. How much does %s pay?" % (nm, he), 100, [80, 29, 75],
        "Count by 25s: 25¢, 50¢, 75¢, 100¢. 4 cups cost <b>100¢</b>, or $1. 80¢ counts a quarter as 20¢.")
    nm, he, his = P.next()
    add("At the book fair, a book costs $8 and a poster costs $4. %s buys both. How much does %s spend?" % (nm, he),
        1200, [400, 1300, 1100],
        "$8 + $4: $8 + $2 = $10. $10 + $2 = <b>$12</b>. $4 is the difference, not the total.", D)
    nm, he, his = P.next()
    add("%s has saved $15. %s buys a book for $9. How much money is left?" % (nm, cap(he)), 600, [2400, 700, 400],
        "Count up from $9: $9 + $1 = $10. $10 + $5 = $15. $1 + $5 = <b>$6</b>. $24 adds instead of taking away.", D)
    nm, he, his = P.next()
    add("A hockey stick costs $35. %s has $20. How much more does %s need?" % (nm, he), 1500, [5500, 2500, 500],
        "Count up from $20: $20 + $10 = $30. $30 + $5 = $35. $10 + $5 = <b>$15</b>. $55 adds the two amounts.", D)
    nm, he, his = P.next()
    toks = toks_of(("T", 2), ("L", 3))
    assert total(toks) == 700 and m_toonie1(toks) == 500
    add(fig(money_svg(toks)) + "%s has these coins. A toque costs $8. How much more does %s need?" % (nm, he),
        100, [300, 1500, 200],
        "Toonies: $2, $4. Loonies: $5, $6, $7. %s has $7. $7 + $1 = $8, so %s needs <b>$1</b> more. "
        "$3 comes from counting each toonie as $1." % (nm, he), D)
    nm, he, his = P.next()
    toks = toks_of(("B20", 1), ("B10", 1), ("B5", 1))
    add(fig(money_svg(toks)) + "%s has this money. %s pays $10 to rent skates at the rink. How much is left?" % (nm, cap(he)),
        2500, [4500, 1500, 3500],
        "%s has $20 + $10 + $5 = $35. Take away $10: $35 − $10 = <b>$25</b>. $45 adds instead of taking away." % cap(he), D)
    nm, he, his = P.next()
    add("Pizza Day is every Friday. A slice costs $2. %s buys a slice every Friday for 4 weeks. How much does %s spend?"
        % (nm, he), 800, [600, 1000, 200],
        "$2, $4, $6, $8. 4 slices cost <b>$8</b>. $6 comes from adding 2 + 4.", D)
    assert len(its) == 20
    return {"title": "Fewest coins or bills and word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    bills = ["B5", "B10", "B20", "B50", "B100"]
    walk = toks_of(("Q", 2), ("D", 1), ("N", 1))
    assert total(walk) == 65
    return (
        "<h2>Canadian coins and bills</h2>"
        "<p>Learn the name and the value of each coin. Size does not tell you the value. "
        "The dime is the smallest coin, but it is worth more than the nickel.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1 (100¢), toonie $2 (200¢). There are no pennies.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(bills, per_row=5, label="Canadian bills: $5, $10, $20, $50, $100") +
        "<figcaption>Bills: $5, $10, $20, $50 and $100.</figcaption></figure>"
        + table(["Coin", "Value", "Good to know"], [
            ["nickel", "5¢", "2 nickels = 1 dime"],
            ["dime", "10¢", "10 dimes = 100¢"],
            ["quarter", "25¢", "4 quarters = 100¢"],
            ["loonie", "$1 = 100¢", "11 sides, gold colour"],
            ["toonie", "$2 = 200¢", "2 loonies = 1 toonie"],
        ]) +
        "<h2>Count the money, biggest first</h2>"
        "<p>Put the coins in order, biggest value first. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=10, under=["25¢", "50¢", "60¢", "65¢"],
                                              label="counting on: 25¢, 50¢, 60¢, 65¢") +
        "<figcaption>Quarters: 25¢, 50¢. Dime: 60¢. Nickel: 65¢.</figcaption></figure>"
        + ex("Example", "Count a loonie, 2 quarters and 1 dime.",
             "100¢, then 125¢, 150¢, then 160¢.", "160¢")
        + ex("Example", "Count a $20 bill, a $5 bill and 2 toonies.",
             "$20, then $25, then $27, $29.", "$29") +
        "<h2>The same amount in different ways</h2>"
        "<p>50¢ can be 2 quarters, or 5 dimes, or 1 quarter, 2 dimes and 1 nickel. "
        "$10 can be a $10 bill, 2 $5 bills or 5 toonies.</p>"
        "<p>For the <b>fewest coins</b>, use the biggest coin you can each time. "
        "30¢ is 1 quarter and 1 nickel: only 2 coins.</p>"
        + ex("Example", "Show 75¢ in two ways.", "3 quarters: 25¢, 50¢, 75¢. Or 7 dimes and 1 nickel: 70¢, 75¢.",
             "3 quarters, or 7 dimes and 1 nickel")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 coins, so 4¢", "Count the value of each coin: 25¢, 50¢, 60¢, 65¢"],
            ["A quarter is 20¢", "A quarter is 25¢. Four quarters make 100¢"],
            ["The nickel is bigger, so it is worth more", "The small dime is 10¢. The nickel is 5¢"],
            ["A toonie is $1", "A loonie is $1. A toonie is $2"],
            ["Start with the small coins", "Start with the biggest coin, then count on"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about money in Ontario?",
     "a": "In the Ontario math curriculum (Financial Literacy, F1.1), Grade 2 students show the same amount of money in different ways: up to 200¢ with Canadian coins, and up to $200 with loonies, toonies and $5, $10, $20, $50 and $100 bills."},
    {"q": "How do I help my child count coins?",
     "a": "Sort the coins and start with the biggest value, then count on: 25¢, 50¢, 60¢, 65¢. Use real coins at home and say the value of each one, not just the number of coins."},
    {"q": "Why are there no pennies in Canada?",
     "a": "Canada stopped giving out pennies in 2013. Cash totals are rounded to the nearest 5¢, so the nickel is the smallest coin children count."},
    {"q": "Do Grade 2 students make change?",
     "a": "Not yet. Making change for simple cash purchases starts in Grade 3. In Grade 2, children count money, make the same amount in different ways and solve simple adding and subtracting problems with money."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(42816)
    P = People(rnd)
    sets = [set_names(P, rnd), set_cents(P, rnd), set_dollars(P, rnd), set_ways(P, rnd), set_words(P, rnd)]
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
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "money", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Canadian Coins and Bills to 200¢ and $200",
        "seo_title": "Grade 2 Money Worksheets: Canadian Coins and Bills, Free with Answer Key (Ontario)",
        "short_title": "Money",
        "domain": "Financial Literacy",
        "standard_code": "Grade 2: F1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify different ways of representing the same amount of money up to 200¢ using various combinations of Canadian coins, and up to $200 using $1 and $2 coins and $5, $10, $20, $50, and $100 bills",
        "meta_desc": "Free Grade 2 math worksheets on money for the Ontario curriculum: name Canadian coins and bills, count nickels, dimes, quarters, loonies and toonies to 200¢, count bills to $200, make the same amount in different ways and use the fewest coins. 100 questions with an answer key.",
        "key_big": "Count money by value, not by the number of coins.",
        "key_sub": "Start with the biggest coin and count on: 25¢, 50¢, 60¢, 65¢. A quarter is 25¢, not 20¢. The same amount can be made in many ways: 2 quarters = 5 dimes = 50¢.",
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
