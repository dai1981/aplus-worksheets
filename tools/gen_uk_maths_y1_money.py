# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Money (National Curriculum in England, Year 1: Measurement)
  python3 tools/gen_uk_maths_y1_money.py
Year 1: recognise coins and notes, know which is worth more, pounds or pence,
count small totals within 20p, simple class-shop problems. No decimals (no £1.50).
Coins and notes are simple labelled shapes (no real coin or note artwork).
Sizes follow the real coins (a 2p coin is bigger than a 5p coin), 20p and 50p have 7 sides, £1 has 12.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
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
# radius (about the real size), (fill, edge), label size, sides (0 = round)
COIN = {"C1": (17, COPPER, 14, 0), "C2": (22, COPPER, 15, 0), "C5": (16, SILVER, 14, 0),
        "C10": (21, SILVER, 15, 0), "C20": (19, SILVER, 14, 7), "C50": (24, SILVER, 15, 7),
        "C100": (20, GOLD, 15, 12), "C200": (24, GOLD, 16, 0)}
NOTE = {"N5": ("#bfe6de", "#1f7a6d"), "N10": ("#f6d2a8", "#a35a12"), "N20": ("#dccbef", "#5b3a8a")}
NOTE_W, NOTE_H = 80, 42
LETTERS = ["A", "B", "C", "D"]


def lab(v):
    return "£%d" % (v // 100) if v >= 100 else "%dp" % v


def mval(s):
    """value in pence of a money text, or None"""
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


def kind(t):
    return "note" if t.startswith("N") else "coin"


def name_of(t):
    return "%s %s" % (lab(VAL[t]), kind(t))


def a_name(t):
    return "a " + name_of(t)


def group(toks):
    return ", ".join("%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks))


def cap(s):
    return s[0].upper() + s[1:]


def coin_list(vals):
    """[5, 2, 1] -> '5p, 2p and 1p'"""
    w = [lab(v) for v in vals]
    return w[0] if len(w) == 1 else ", ".join(w[:-1]) + " and " + w[-1]


def count_on(toks):
    """'Start with the biggest coin: 10p, 15p, 17p. That is 17p.'"""
    toks = srt(toks)
    if len(set(toks)) == 1:
        v, n = VAL[toks[0]], len(toks)
        if v == 1:
            return "Each coin is 1p. Count: %s. That is <b>%dp</b>." % (", ".join("%dp" % k for k in range(1, n + 1)), n)
        return "Each coin is %dp. Count in %ds: %s. That is <b>%dp</b>." % (
            v, v, ", ".join("%dp" % (v * k) for k in range(1, n + 1)), v * n)
    run, s = [], 0
    for t in toks:
        s += VAL[t]
        run.append("%dp" % s)
    return "Start with the biggest coin: %s. That is <b>%dp</b>." % (", ".join(run), s)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (never equal in value)."""
    correct = lab(correct) if isinstance(correct, int) else str(correct)
    seen_t, seen_v = {correct}, {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0:
                continue
            c = lab(c)
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


def letter_q(stem, right, others, e):
    """A-D picture question: built in balance() so the right one lands on the chosen letter.
    e may use {L} for the letter of the answer."""
    assert len(others) == 3 and right not in others
    return {"_lt": (stem, right, list(others), e)}


def build_letter(it, t, rnd):
    stem, right, others, e = it.pop("_lt")
    o = list(others)
    rnd.shuffle(o)
    arr = o[:t] + [right] + o[t:]
    svg = money_svg(arr, gap=14, under=LETTERS, label="pictures A to D: " + ", ".join(
        "%s %s" % (L, name_of(x)) for L, x in zip(LETTERS, arr)))
    it.update({"q": fig(svg) + stem, "c": list(LETTERS), "a": t, "e": e.format(L=LETTERS[t])})


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_lt" in it:
                build_letter(it, t, rnd)
                continue
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

    def girl(self):
        while True:
            p = self.next()
            if p[1] == "she":
                return p

    def boy(self):
        while True:
            p = self.next()
            if p[1] == "he":
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


def poly(cx, cy, r, n):
    pts = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def shape(cx, cy, r, n, fill, edge, sw):
    if n:
        return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='%s'/>" % (poly(cx, cy, r, n), fill, edge, sw)
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%s'/>" % (cx, cy, r, fill, edge, sw)


def draw_tok(t, cx, cy):
    """one coin or one note, centred at cx, cy"""
    if t.startswith("N"):
        fill, edge = NOTE[t]
        x, y = cx - NOTE_W / 2, cy - NOTE_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, NOTE_W, NOTE_H, fill, edge, x + 5, y + 5, NOTE_W - 10, NOTE_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r, (fill, edge), fs, n = COIN[t]
    out = shape(cx, cy, r, n, fill, edge, 2)
    if t in ("C100", "C200"):
        # two-colour coins: £1 has a silver centre, £2 has a silver centre and a gold ring
        out += shape(cx, cy, r - 6, 0, SILVER[0], edge, 1)
    else:
        out += shape(cx, cy, r - 4, 0 if not n else n, "none", edge, 1)
    return out + text(cx, cy + fs * 0.36, lab(VAL[t]), fs)


def money_svg(toks, per_row=6, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    widths = [sum(max(tok_size(t)[0], 24 if under else 0) for t in r) + gap * (len(r) - 1) for r in rows]
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rw, rh in zip(rows, widths, heights):
        x = pad
        hh = rh - lab_h
        for t in r:
            w = max(tok_size(t)[0], 24 if under else 0)
            s.append(draw_tok(t, x + w / 2, y + hh / 2))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(W, H, "".join(s), label or ("money: " + group(toks)))


def one_svg(t):
    w, h = tok_size(t)
    return svg_wrap(w + 6, h + 6, draw_tok(t, (w + 6) / 2, (h + 6) / 2), "one %s" % name_of(t))


def price_svg(items, title):
    gap, pad, h = 10, 6, 62
    ws = [max(len(n) * 9 + 24, 70) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, lab(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, lab(p)) for n, p in items))


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


# ============================================================ set 1: name the coins and notes
def set_name(P, rnd):
    its = []
    coin_c = {
        "C1": ["£1", "10p", "2p"], "C2": ["£2", "20p", "1p"], "C5": ["50p", "£5", "2p"],
        "C10": ["£10", "1p", "20p"], "C20": ["£20", "2p", "10p"], "C50": ["5p", "£5", "20p"],
        "C100": ["1p", "10p", "£10"], "C200": ["2p", "20p", "£20"],
    }
    words = {"C1": "one penny", "C2": "two pence", "C5": "five pence", "C10": "ten pence", "C20": "twenty pence",
             "C50": "fifty pence", "C100": "one pound", "C200": "two pounds"}
    for t in ["C1", "C2", "C5", "C10", "C20", "C50", "C100", "C200"]:
        v = lab(VAL[t])
        sym = ("The £ sign means pounds." if VAL[t] >= 100 else "The p means pence.")
        its.append(mcq(fig(one_svg(t)) + "What is this coin?", VAL[t], coin_c[t],
                       "It is the <b>%s</b> coin (%s). %s" % (v, words[t], sym)))
    note_c = {"N5": ["5p", "50p", "£10"], "N10": ["10p", "£1", "£20"], "N20": ["20p", "£2", "£10"]}
    nw = {"N5": "five pounds", "N10": "ten pounds", "N20": "twenty pounds"}
    for t in ["N5", "N10", "N20"]:
        its.append(mcq(fig(one_svg(t)) + "What is this note?", VAL[t], note_c[t],
                       "It is the <b>%s</b> note (%s). A note is flat. Coins are made of metal." % (lab(VAL[t]), nw[t])))
    its.append(letter_q("Which one is a note?", "N5", ["C100", "C200", "C50"],
                        "<b>{L}</b> is the £5 note. The others are coins. A note is a flat rectangle you can fold."))
    its.append(letter_q("Which one is a note?", "N10", ["C10", "C200", "C1"],
                        "<b>{L}</b> is the £10 note. 10p is a coin, not a note."))
    its.append(letter_q("Which one is a coin?", "C200", ["N5", "N10", "N20"],
                        "<b>{L}</b> is the £2 coin. The others are notes."))
    its.append(letter_q("Find the 50p coin.", "C50", ["C5", "C20", "C100"],
                        "<b>{L}</b> says 50p. The 5p coin is much smaller and worth much less."))
    its.append(letter_q("Find the 2p coin.", "C2", ["C20", "C200", "C1"],
                        "<b>{L}</b> says 2p. 20p and £2 also have a 2 in them, but they are different coins."))
    its.append(letter_q("Find the £1 coin.", "C100", ["C1", "C10", "C200"],
                        "<b>{L}</b> says £1. The £ sign comes first. 1p is a penny, not a pound."))
    its.append(mcq(fig(one_svg("C50")) + "Count the sides of the 50p coin. How many sides does it have?",
                   "7", ["5", "6", "8"], "Count round the edge: 1, 2, 3, 4, 5, 6, 7. The 50p coin has <b>7</b> sides. "
                   "The 20p coin has 7 sides too."))
    its.append(mcq("This coin has 12 sides. It is gold and silver. Which coin is it?",
                   "£1", ["50p", "20p", "£2"],
                   "The <b>£1</b> coin has 12 sides. The 20p and 50p coins have 7 sides. The £2 coin is round."))
    its.append(mcq("Which one means “two pence”?", 2, [200, 20, 12],
                   "Pence are written with a p after the number: <b>2p</b>. £2 means two pounds."))
    assert len(its) == 20
    return {"title": "Name the coins and notes", "items": its}


# ============================================================ set 2: which is worth more?
SAME, CANT = "They are the same.", "You cannot tell."


def set_more(P, rnd):
    its = []
    def pair(a, b, more):
        """a, b drawn left to right; more=True asks for more, False for less"""
        hi, lo = (a, b) if VAL[a] > VAL[b] else (b, a)
        ans = hi if more else lo
        wrong = lo if more else hi
        size_trap = (not a.startswith("N") and not b.startswith("N") and tok_size(lo)[0] > tok_size(hi)[0])
        q = fig(money_svg([a, b], gap=16)) + ("Which is worth more?" if more else "Which is worth less?")
        e = "%s is worth more than %s, so the answer is <b>%s</b>." % (lab(VAL[hi]), lab(VAL[lo]), lab(VAL[ans]))
        if size_trap:
            e += " The %s coin is bigger, but size does not show the value. Read the number." % lab(VAL[lo])
        elif VAL[hi] >= 100 and VAL[lo] < 100:
            e += " %s is %dp, so it is worth more." % (lab(VAL[hi]), VAL[hi])
        its.append(mcq(q, VAL[ans], [VAL[wrong], SAME, CANT], e))

    pair("C10", "C2", True)
    pair("C2", "C5", True)
    pair("C50", "C100", True)
    pair("C10", "C20", True)
    pair("C20", "C50", True)
    pair("C1", "C5", False)
    pair("C200", "N10", True)
    pair("C20", "C5", False)
    pair("N20", "N10", True)
    pair("C50", "C200", False)
    pair("N5", "C200", False)
    pair("C100", "C20", False)
    its.append(letter_q("Which is worth the most?", "C10", ["C2", "C5", "C1"],
                        "10p is worth the most, so it is <b>{L}</b>. The 2p coin is bigger, but 2p is less than 10p."))
    its.append(letter_q("Which is worth the most?", "C100", ["C50", "C20", "C10"],
                        "£1 is worth the most, so it is <b>{L}</b>. The 50p coin is bigger, but £1 = 100p."))
    its.append(letter_q("Which is worth the least?", "C2", ["C5", "C10", "C20"],
                        "2p is worth the least, so it is <b>{L}</b>. The 5p coin is smaller, but 5p is more than 2p."))
    its.append(letter_q("Which is worth the least?", "C20", ["C100", "C50", "C200"],
                        "20p is worth the least, so it is <b>{L}</b>."))
    its.append(letter_q("Which is worth the most?", "N5", ["C200", "C50", "C100"],
                        "The £5 note is worth the most, so it is <b>{L}</b>. £5 is more than £2."))
    right = "2p, 5p, 10p"
    its.append(mcq("Put the coins in order. Start with the one worth the least: 10p, 2p, 5p.", right,
                   ["5p, 10p, 2p", "10p, 5p, 2p", "2p, 10p, 5p"],
                   "Look at the numbers, not the sizes: 2 is less than 5, and 5 is less than 10. So: <b>2p, 5p, 10p</b>. "
                   "5p, 10p, 2p is the order of size (smallest coin first)."))
    its.append(mcq("Which is worth more: one £1 coin or three 10p coins?", "one £1 coin",
                   ["three 10p coins", SAME, CANT],
                   "Three 10p coins make 10p, 20p, 30p. £1 is 100p, so <b>one £1 coin</b> is worth more. More coins does not mean more money."))
    its.append(mcq("Which is worth more: one 10p coin or five 1p coins?", "one 10p coin",
                   ["five 1p coins", SAME, CANT],
                   "Five 1p coins make 5p. 10p is more than 5p, so <b>one 10p coin</b> is worth more."))
    assert len(its) == 20, len(its)
    return {"title": "Which is worth more?", "items": its}


# ============================================================ set 3: pounds or pence?
def set_pounds(P, rnd):
    its = []
    UNIT = ["pence", "pounds", "coins", "notes"]
    for t, w in [("C2", 2), ("C200", 2), ("C50", 50), ("N5", 5)]:
        unit = "pounds" if VAL[t] >= 100 else "pence"
        its.append(mcq(fig(one_svg(t)) + "This %s is worth %d ___." % (kind(t), w), unit,
                       [u for u in UNIT if u != unit],
                       "It says %s. %s, so it is %d <b>%s</b>." % (
                           lab(VAL[t]), "The £ sign means pounds" if unit == "pounds" else "The p means pence", w, unit)))
    its.append(mcq("What does the £ sign mean?", "pounds", ["pence", "coins", "notes"],
                   "£ means <b>pounds</b>. £3 is three pounds."))
    its.append(mcq("What does the p in 20p mean?", "pence", ["pounds", "coins", "notes"],
                   "p means <b>pence</b>. 20p is twenty pence."))
    its.append(mcq("How many pence make £1?", "100p", ["1p", "10p", "50p"],
                   "<b>100p</b> make £1. So £1 is worth much more than 1p."))
    its.append(mcq("How do you write two pounds?", "£2", ["2p", "£20", "2£"],
                   "Write the £ sign first, then the number: <b>£2</b>. 2p is two pence."))
    its.append(mcq("How do you write fifty pence?", "50p", ["£50", "5p", "p50"],
                   "Write the number, then p: <b>50p</b>."))
    its.append(mcq("How do you write ten pounds?", "£10", ["10p", "10£", "£1"],
                   "The £ sign goes before the number: <b>£10</b>."))
    its.append(mcq("Which coins are all pence coins?", "1p, 5p, 20p", ["1p, £1, 20p", "£2, 5p, 10p", "£1, £2, 50p"],
                   "Pence coins have a p: 1p, 2p, 5p, 10p, 20p and 50p. So <b>1p, 5p, 20p</b>."))
    its.append(mcq("Which are all pounds?", "£1, £2, £5", ["£1, 2p, £5", "10p, £2, £5", "£1, 50p, £10"],
                   "Pounds have the £ sign: £1 and £2 coins, and £5, £10 and £20 notes. So <b>£1, £2, £5</b>."))
    its.append(letter_q("Which one is worth pence, not pounds?", "C20", ["C100", "C200", "N5"],
                        "<b>{L}</b> is 20p. It has a p, so it is pence. The others have the £ sign."))
    its.append(letter_q("Which one is worth pounds?", "C200", ["C50", "C20", "C10"],
                        "<b>{L}</b> is £2. It has the £ sign, so it is pounds. 50p is pence."))
    its.append(mcq("How many 1p coins make 10p?", "10", ["1", "100", "5"],
                   "Count in 1s: 1p, 2p, 3p … 10p. That is <b>10</b> coins. One 1p coin is only 1p."))
    for a, b in [(200, 20), (500, 50), (1000, 10)]:
        its.append(mcq("Which is worth more: %s or %s?" % (lab(a), lab(b)), a, [b, SAME, CANT],
                       "%s is pounds: %s = %sp. %s is only %d pence. So <b>%s</b> is worth more." % (lab(a), lab(a), "{:,}".format(a), lab(b), b, lab(a))))
    nm, he, his = P.girl()
    nm2, he2, his2 = P.boy()
    its.append(mcq("%s has a £1 coin. %s has a 1p coin. Do they have the same amount?" % (nm, nm2),
                   "No. £1 is more.", ["Yes. Both are 1.", "No. 1p is more.", CANT],
                   "£1 is one pound = 100p. 1p is one penny. <b>No. £1 is more.</b>"))
    nm, he, his = P.next()
    its.append(mcq("%s has three coins: £1, £2 and 20p. How many are pound coins?" % nm,
                   "2", ["3", "1", "0"],
                   "£1 and £2 have the £ sign. 20p is pence. So <b>2</b> are pound coins."))
    assert len(its) == 20, len(its)
    return {"title": "Pounds or pence?", "items": its}


# ============================================================ set 4: count the coins
def m_count(toks):
    return len(toks)


def m_skip(toks, k=-1):
    ks = [t for t, n in counts(toks)]
    return total(toks) - VAL[ks[k]]


def m_twice(toks, k=-1):
    ks = [t for t, n in counts(toks)]
    return total(toks) + VAL[ks[k]]


def m_same_step(toks):
    """kept the old step for the first coin of each new kind"""
    s, prev = 0, None
    for t in srt(toks):
        s += VAL[prev] if prev is not None and t != prev else VAL[t]
        prev = t
    return s


def set_count(P, rnd):
    its = []
    groups = [
        [("C1", 4)], [("C2", 3)], [("C5", 2)], [("C10", 2)], [("C2", 5)], [("C5", 3)],
        [("C10", 1), ("C5", 1)], [("C10", 1), ("C2", 1)], [("C5", 1), ("C1", 2)], [("C5", 1), ("C2", 1), ("C1", 1)],
        [("C10", 1), ("C2", 2)], [("C10", 1), ("C1", 3)], [("C5", 2), ("C2", 1)],
        [("C10", 1), ("C5", 1), ("C1", 1)], [("C2", 4), ("C1", 1)], [("C10", 1), ("C5", 1), ("C2", 1), ("C1", 1)],
        [("C5", 2), ("C2", 1), ("C1", 1)],
    ]
    mixed = {13, 14, 15, 16}
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s pocket. How much is it?", "What is the total?",
             "%s puts these coins in a money box. How much is in the box?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T <= 20 and len(toks) <= 5
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if st.count("%s") == 2:
            st = st % (nm, his if "pocket" in st else he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i in mixed else toks
        e = ("Put the coins in order, biggest value first. " if i in mixed else "") + count_on(toks)
        if i < 6 or len(toks) > 3:
            e += " Count the value of each coin, not the number of coins."
        cands = [m_count(toks), m_same_step(toks), m_skip(toks, -1), m_twice(toks, -1), m_skip(toks, 0),
                 T - 1, T + 1, T + 2]
        its.append(mcq(fig(money_svg(shown, gap=10)) + st, T, cands, e))
    # which coins make an amount?
    for amt, right, wrongs in [
        (7, [5, 2], [[5, 1], [2, 2, 2], [5, 2, 1]]),
        (9, [5, 2, 2], [[5, 2], [5, 2, 1], [5, 5]]),
        (13, [10, 2, 1], [[10, 2], [10, 5], [5, 5, 2]]),
    ]:
        assert sum(right) == amt and all(sum(w) != amt for w in wrongs)
        e = "%s = %dp, so the answer is <b>%s</b>." % (" + ".join(lab(v) for v in right), amt, coin_list(right))
        its.append(mcq("Which coins make %dp?" % amt, coin_list(right), [coin_list(w) for w in wrongs], e))
    assert len(its) == 20, len(its)
    return {"title": "Count the coins", "items": its}


# ============================================================ set 5: shopping
SHOP = [("banana", 6), ("apple", 4), ("cake", 9), ("drink", 8)]


def set_shop(P, rnd):
    its = []

    def add(q, right, cands, e):
        its.append(mcq(q, right, cands, e))

    price = dict(SHOP)
    board = fig(price_svg(SHOP, "class shop"))
    nm, he, his = P.girl()
    add("%s has a 10p coin. A sweet costs 7p. Can %s buy it?" % (nm, he), "Yes. 10p is more.",
        ["No. 7p is more.", "No. She has 1 coin.", "No. She needs 17p."],
        "10p is more than 7p, so <b>yes</b>. One 10p coin is worth 10p, not 1p.")
    nm, he, his = P.boy()
    nm2, he2, his2 = P.girl()
    add("%s has three 1p coins. %s has one 5p coin. Who has more money?" % (nm, nm2), nm2, [nm, SAME, CANT],
        "%s has 1p, 2p, 3p = 3p. %s has 5p. 5p is more, so <b>%s</b>. More coins does not mean more money." % (nm, nm2, nm2))
    nm, he, his = P.girl()
    nm2, he2, his2 = P.boy()
    add("%s has one 10p coin. %s has four 2p coins. Who has more money?" % (nm, nm2), nm, [nm2, SAME, CANT],
        "%s has 2p, 4p, 6p, 8p = 8p. 10p is more than 8p, so <b>%s</b>." % (nm2, nm))
    nm, he, his = P.next()
    add("A pencil costs 5p. %s buys 2 pencils. How much does %s pay?" % (nm, he), 10, [7, 5, 2, 12],
        "5p + 5p = <b>10p</b>. 7p is 5 + 2, but 2 is the number of pencils, not pence.")
    nm, he, his = P.next()
    add("A toy car costs 8p. %s pays with a 10p coin. How much change does %s get?" % (nm, he), 2, [18, 8, 1],
        "Count on from 8p to 10p: 9p, 10p. That is 2 steps, so the change is <b>2p</b>. Check: 8p + 2p = 10p.")
    nm, he, his = P.boy()
    add("%s has a 5p coin and a 2p coin. A rubber costs 9p. How much more does %s need?" % (nm, he), 2, [4, 7, 16],
        "%s has 5p + 2p = 7p. Count on from 7p to 9p: 8p, 9p. %s needs <b>2p</b> more. "
        "4p forgets the 2p coin." % (nm, cap(he)))
    add("A sticker costs 5p. Which coins make exactly 5p?", "2p, 2p and 1p",
        ["2p and 2p", "2p, 2p and 2p", "1p, 1p and 1p"],
        "2p + 2p + 1p = 5p, so <b>2p, 2p and 1p</b>. 2p and 2p only make 4p.")
    nm, he, his = P.boy()
    add("%s has a £1 coin. A ball costs £2. Can %s buy it?" % (nm, he), "No. £2 is more.",
        ["Yes. He has a coin.", "Yes. £1 is more.", CANT],
        "£2 is more than £1, so <b>no</b>. %s needs one more pound." % nm)
    nm, he, his = P.girl()
    add("A book costs £5. %s has a £5 note. Can %s buy it?" % (nm, he), "Yes. It is just right.",
        ["No. She needs 5 coins.", "No. £5 is too little.", CANT],
        "The note is worth £5 and the book costs £5. So <b>yes</b>. One note can be worth a lot.")
    nm, he, his = P.next()
    T = price["apple"] + price["banana"]
    add(board + "In the class shop, %s buys an apple and a banana. How much does %s pay?" % (nm, he), T, [2, 9, 11],
        "Start with the bigger number: 6p, then count on 4: 7p, 8p, 9p, 10p. That is <b>10p</b>. 2p is the difference, not the total.")
    nm, he, his = P.next()
    T = price["cake"] + price["apple"]
    add(board + "In the class shop, %s buys a cake and an apple. How much does %s pay?" % (nm, he), T, [5, 12, 14],
        "9p + 4p: count on from 9p: 10p, 11p, 12p, 13p. That is <b>13p</b>.")
    nm, he, his = P.girl()
    add(board + "%s has a 5p coin. Which one can %s buy?" % (nm, he), "the apple",
        ["the banana", "the cake", "the drink"],
        "Only the apple costs less than 5p (4p). So %s can buy <b>the apple</b>." % nm)
    nm, he, his = P.next()
    add(board + "%s buys a banana. %s pays with a 10p coin. How much change does %s get?" % (nm, cap(he), he), 4, [16, 6, 5],
        "Count on from 6p to 10p: 7p, 8p, 9p, 10p. That is 4 steps, so the change is <b>4p</b>. 6p is the price, not the change.")
    nm, he, his = P.girl()
    add(board + "%s has two 5p coins. Can %s buy the cake?" % (nm, he), "Yes. She has 10p.",
        ["No. She has 2 coins.", "No. 5p is too little.", CANT],
        "5p + 5p = 10p. The cake is 9p, and 10p is more than 9p. So <b>yes</b>.")
    nm, he, his = P.next()
    add("Pencils cost 2p each. %s has 6p. How many pencils can %s buy?" % (nm, he), "3 pencils",
        ["6 pencils", "2 pencils", "4 pencils"],
        "Count in 2s: 2p, 4p, 6p. That is 3 jumps, so <b>3 pencils</b>.")
    nm, he, his = P.boy()
    add("%s has 20p. He spends 10p on a toy. How much does %s have left?" % (nm, he), 10, [30, 20, 9],
        "20p take away 10p is <b>10p</b>. 30p adds instead of taking away.")
    nm, he, his = P.boy()
    toks = toks_of(("C10", 1), ("C5", 1), ("C1", 1))
    add("%s has a 10p coin, a 5p coin and a 1p coin. How much money does %s have?" % (nm, he), 16, [3, 15, 17],
        count_on(toks) + " 3p counts the coins, not their values.")
    nm, he, his = P.girl()
    add("%s gets a £1 coin from Mum and a £2 coin from Gran. How much does %s have now?" % (nm, he), 300, [3, 200, 100],
        "£1 + £2 = <b>£3</b>. These are pound coins, so it is £3, not 3p.")
    nm, he, his = P.boy()
    add("%s has a £5 note and a £10 note. How much money does %s have?" % (nm, he), 1500, [200, 15, 1000],
        "£10 + £5 = <b>£15</b>. £2 counts the notes, not their values.")
    nm, he, his = P.girl()
    nm2, he2, his2 = P.boy()
    add("%s has 12p. %s has 15p. How much more does %s have?" % (nm, nm2, nm2), 3, [27, 15, 12],
        "Count on from 12p to 15p: 13p, 14p, 15p. That is 3 steps, so %s has <b>3p</b> more." % nm2)
    assert len(its) == 20, len(its)
    return {"title": "Shopping", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C1", "C2", "C5", "C10", "C20", "C50", "C100", "C200"]
    notes = ["N5", "N10", "N20"]
    walk = toks_of(("C10", 1), ("C5", 1), ("C2", 1))
    assert total(walk) == 17
    return (
        "<h2>Coins and notes</h2>"
        "<p>We pay with coins and notes. Each one shows its value. "
        "<b>p</b> means pence. <b>£</b> means pounds.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=8, label="UK coins: 1p, 2p, 5p, 10p, 20p, 50p, £1, £2") +
        "<figcaption>Coins: 1p, 2p, 5p, 10p, 20p, 50p, £1 and £2.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(notes, label="UK notes: £5, £10, £20") +
        "<figcaption>Notes: £5, £10 and £20.</figcaption></figure>"
        "<h2>Read the number, not the size</h2>"
        "<p>A big coin is not always worth more. The 2p coin is bigger than the 5p coin, but 5p is worth more.</p>"
        "<figure class='sn-fig'>" + money_svg(["C2", "C5"], gap=20, label="money: a 2p coin and a 5p coin") +
        "<figcaption>2p is bigger. 5p is worth more.</figcaption></figure>"
        "<p>£1 is worth 100p. So a £1 coin is worth much more than a 1p coin.</p>"
        "<h2>Count the coins, biggest first</h2>"
        "<p>Start with the coin worth the most. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=20, under=["10p", "15p", "17p"], label="counting on: 10p, 15p, 17p") +
        "<figcaption>10p, 15p, 17p. There are 3 coins, but the total is 17p.</figcaption></figure>"
        + ex("Example", "A lolly costs 8p. You have a 10p coin. Can you buy it?",
             "10p is more than 8p.", "Yes")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The 2p coin is bigger, so it is worth more than 5p", "Read the number on the coin: 5p is more than 2p"],
            ["3 coins, so 3p", "Add the value of each coin: 10p, 15p, 17p"],
            ["£1 is the same as 1p", "£1 = 100p, so £1 is worth much more"],
        ])
    )


FAQ = [
    {"q": "What money does a Year 1 child need to know?",
     "a": "In the National Curriculum, Year 1 pupils recognise and know the value of all the UK coins (1p, 2p, 5p, 10p, 20p, 50p, £1, £2) and notes (£5, £10, £20)."},
    {"q": "Why is a 2p coin bigger than a 5p coin?",
     "a": "The size of a coin does not show its value. Children need to read the number on the coin: 5p is worth more than 2p, even though it is smaller."},
    {"q": "What is the difference between pounds and pence?",
     "a": "£ means pounds and p means pence. There are 100 pence in £1, so a £1 coin is worth much more than a 1p coin."},
    {"q": "How can I help my child learn about money at home?",
     "a": "Let them sort real coins, find the one worth the most, and play shop with prices up to 20p. Ask them to count the coins starting with the biggest value."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1107)
    P = People(rnd)
    sets = [set_name(P, rnd), set_more(P, rnd), set_pounds(P, rnd), set_count(P, rnd), set_shop(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [v for v in (mval(c) for c in it["c"]) if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "money", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Coins and Notes, Pounds and Pence",
        "seo_title": "Year 1 Money Worksheets: UK Coins and Notes, Pounds and Pence",
        "short_title": "Money",
        "domain": "Measurement",
        "standard_code": "Year 1: Measurement",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Recognise and know the value of different denominations of coins and notes.",
        "meta_desc": "Free Year 1 maths worksheets on money: name UK coins and notes, find which is worth more (a 2p coin is bigger but 5p is worth more), tell pounds from pence, count coins up to 20p and shop in the class shop. 100 questions with an answer key, following the National Curriculum.",
        "key_big": "Read the number on the coin, not its size.",
        "key_sub": "p means pence and £ means pounds. A 5p coin is worth more than a bigger 2p coin, and £1 is 100p. Count coins starting with the one worth the most.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|pictures|price)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
