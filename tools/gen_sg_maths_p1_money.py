# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Money (MOE 2021 Primary Mathematics Syllabus, Standard:
Primary 1 Money, counting amounts of money in cents up to $1 and in dollars up to $100)
  python3 tools/gen_sg_maths_p1_money.py
Singapore money for P1: coins 5¢, 10¢, 20¢, 50¢, $1 (no 1¢) and notes $2, $5, $10, $50.
Amounts in cents stay at or below $1 (100¢ is written $1); amounts in dollars are whole dollars up to $100.
No mixed amounts like $1.20 (that is P2). Every amount is an int number of cents and checked in code.
Very short sentences for 6-7 year olds, a picture in almost every question.
Wrong answers come from real mistakes: counting the coins or notes instead of their value, mixing ¢ and $
(30¢ written as $30, $5 read as more or less than 50¢), missing or double-counting one coin, counting by
the wrong step, "more coins is more money", the price taken as the change, adding instead of taking away.
"A-D picture" questions build the picture after the answer position is chosen, so the choices stay A, B, C, D.
Coin, note and price tag drawing adapted from gen_cabc_math_g1_money.py and gen_sg_maths_p3_money.py.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

# ------------------------------------------------------------ money facts
ORDER = ["N50", "N10", "N5", "N2", "C100", "C50", "C20", "C10", "C5"]     # biggest value first
VAL = {"N50": 5000, "N10": 1000, "N5": 500, "N2": 200,
       "C100": 100, "C50": 50, "C20": 20, "C10": 10, "C5": 5}
COIN = {"C5": 17, "C10": 18, "C20": 20, "C50": 22, "C100": 24}        # radius, in the order of the real sizes
COINFILL, COINEDGE = "#e4e6e9", "#6f767d"
NOTE = {"N2": ("#e3d4ef", "#5b2d8a"), "N5": ("#d3ecd2", "#2f7a2a"), "N10": ("#f6d0cf", "#a32020"),
        "N50": ("#cfe0f3", "#1f5f99")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def ONE(t):
    return lab(VAL[t]) + (" note" if t.startswith("N") else " coin")


def C(v):
    """cents up to $1: 35 -> '35¢', 100 -> '$1'"""
    assert isinstance(v, int) and 0 < v <= 100, v
    return "$1" if v == 100 else "%d¢" % v


def D(v):
    """whole dollars: 1700 -> '$17'"""
    assert isinstance(v, int) and v > 0 and v % 100 == 0, v
    return "$%d" % (v // 100)


def mval(s):
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


def cap(s):
    return s[0].upper() + s[1:]


def count_on(toks, fmt):
    toks = srt(toks)
    T = total(toks)
    s, run = 0, []
    for t in toks:
        s += VAL[t]
        run.append(fmt(s))
    if len(set(toks)) == 1:
        t = toks[0]
        step = VAL[t] if VAL[t] < 100 else VAL[t] // 100
        return "Each one is %s. Count by %ds: %s. That is <b>%s</b>." % (lab(VAL[t]), step, ", ".join(run), fmt(T))
    return "Start with the biggest one. Count on: %s. That is <b>%s</b>." % (", ".join(run), fmt(T))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=str):
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or (fmt is D and c % 100) or (fmt is C and c > 100):
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
        for k, (it, t) in enumerate(zip(s["items"], targets)):
            if "_build" in it:
                s["items"][k] = it["_build"](t)
                assert s["items"][k]["a"] == t
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    assert "'" not in label, label
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures: coins and notes
def tok_size(t):
    if t.startswith("N"):
        return NOTE_W, NOTE_H
    return 2 * COIN[t], 2 * COIN[t]


def draw_tok(t, cx, cy):
    if t.startswith("N"):
        fill, edge = NOTE[t]
        x, y = cx - NOTE_W / 2, cy - NOTE_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, NOTE_W, NOTE_H, fill, edge, x + 5, y + 5, NOTE_W - 10, NOTE_H - 10, edge)
                + text(cx, cy + 7, lab(VAL[t]), 20, col=edge))
    r = COIN[t]
    fs = 15 if t != "C100" else 16
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, COINFILL, COINEDGE)
            + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, COINEDGE)
            + text(cx, cy + fs * 0.36, lab(VAL[t]), fs))


def under_w(s):
    return len(s) * 8.6 + 8


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    k, widths, slot = 0, [], []
    for r in rows:
        ws = []
        for t in r:
            ws.append(max(tok_size(t)[0], under_w(under[k]) if under else 0))
            k += 1
        slot.append(ws)
        widths.append(sum(ws) + gap * (len(r) - 1))
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rh, ws, rw in zip(rows, heights, slot, widths):
        x = pad + (max(widths) - rw) / 2
        hh = rh - lab_h
        for t, w in zip(r, ws):
            s.append(draw_tok(t, x + w / 2, y + hh / 2))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s),
                    label or ("money: " + ", ".join(lab(VAL[t]) for t in toks)))


def two_groups(left, right, capl, capr, label):
    """two piles of money side by side, a dashed line between them, a caption under each"""
    gap, pad, mid = 6, 6, 26

    def size(g):
        return sum(tok_size(t)[0] for t in g) + gap * (len(g) - 1), max(tok_size(t)[1] for t in g)
    (wl, hl), (wr, hr) = size(left), size(right)
    wl2, wr2 = max(wl, under_w(capl)), max(wr, under_w(capr))
    hh = max(hl, hr)
    W = pad + wl2 + mid + wr2 + pad
    H = pad + hh + 26 + pad
    b = []
    for g, x0, ww, wg, cp in ((left, pad, wl2, wl, capl), (right, pad + wl2 + mid, wr2, wr, capr)):
        x = x0 + (ww - wg) / 2
        for t in g:
            w = tok_size(t)[0]
            b.append(draw_tok(t, x + w / 2, pad + hh / 2))
            x += w + gap
        b.append(text(x0 + ww / 2, pad + hh + 20, cp, 15, col=GREEN))
    lx = pad + wl2 + mid / 2
    b.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#9aa3ab' stroke-width='2' stroke-dasharray='4 4'/>"
             % (lx, pad, lx, H - pad))
    return svg_wrap(int(math.ceil(W)), int(H), "".join(b), "compare: " + label)


def tag_svg(price, item):
    """a price tag: the price big, the item under it"""
    W = int(max(96, under_w(item) + 28))
    H = 66
    b = ("<path d='M 18 4 L %d 4 L %d 62 L 18 62 L 4 33 Z' fill='#fff7d6' stroke='#9a7a1c' stroke-width='2'/>"
         "<circle cx='17' cy='33' r='4' fill='none' stroke='#9a7a1c' stroke-width='2'/>" % (W - 4, W - 4))
    cx = (24 + W - 4) / 2
    b += text(cx, 32, price, 22) + text(cx, 53, item, 14, col=GREEN)
    return svg_wrap(W, H, b, "price tag: %s costs %s" % (item, price))


def tags_svg(pairs):
    """two or three price tags in a row"""
    parts, x, H = [], 0, 66
    for price, item in pairs:
        W = int(max(96, under_w(item) + 28))
        b = ("<path d='M %d 4 L %d 4 L %d 62 L %d 62 L %d 33 Z' fill='#fff7d6' stroke='#9a7a1c' stroke-width='2'/>"
             "<circle cx='%d' cy='33' r='4' fill='none' stroke='#9a7a1c' stroke-width='2'/>"
             % (x + 18, x + W - 4, x + W - 4, x + 18, x + 4, x + 17))
        cx = x + (24 + W - 4) / 2
        parts.append(b + text(cx, 32, price, 22) + text(cx, 53, item, 14, col=GREEN))
        x += W + 10
    lbl = "price tags: " + ", ".join("%s costs %s" % (i, p) for p, i in pairs)
    return svg_wrap(x - 10, H, "".join(parts), lbl)


LET = "ABCD"


def abcd(stem, right, others, e):
    """A-D picture: the right one goes to the answer position chosen later"""
    assert len(others) == 3 and right not in others

    def build(t):
        toks = others[:t] + [right] + others[t:]
        lbl = "A, B, C and D: " + ", ".join("%s %s" % (LET[i], ONE(x)) for i, x in enumerate(toks))
        svg = money_svg(toks, per_row=4, gap=10, under=list(LET), label=lbl)
        return {"q": fig(svg) + stem, "c": list(LET), "a": t, "e": e % LET[t]}
    return {"_build": build, "q": stem + "|" + right}


def one(t):
    w, h = tok_size(t)
    return svg_wrap(w + 12, h + 12, draw_tok(t, (w + 12) / 2, (h + 12) / 2), "one " + ONE(t))


# ============================================================ set 1: name the coins and notes
def set_names(P, rnd):
    its = []

    def s(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    s(fig(one("C5")) + "What is this?", "5¢ coin", ["$5 note", "50¢ coin", "5¢ note"],
      "It is round and says 5¢. It is a <b>5¢ coin</b>. A $5 note is paper money.")
    s(fig(one("C20")) + "What is this?", "20¢ coin", ["$20 coin", "2¢ coin", "$2 note"],
      "It says 20¢. The ¢ sign means cents. It is a <b>20¢ coin</b>.")
    s(fig(one("C50")) + "What is this?", "50¢ coin", ["$50 note", "5¢ coin", "$5 note"],
      "It says 50¢. It is a <b>50¢ coin</b>. A $50 note is worth much more.")
    s(fig(one("N2")) + "What is this?", "$2 note", ["2¢ coin", "$2 coin", "20¢ coin"],
      "It is paper money that says $2. It is a <b>$2 note</b>. There is no $2 coin.")
    s(fig(one("N10")) + "What is this?", "$10 note", ["10¢ coin", "$1 coin", "$100 note"],
      "It says $10. The $ sign means dollars. It is a <b>$10 note</b>.")
    its.append(abcd("Which one is the $5 note?", "N5", ["C5", "N50", "C50"],
                    "The $5 note says $5. It is <b>%s</b>. 5¢ and 50¢ are coins."))
    its.append(abcd("Which one is the 10¢ coin?", "C10", ["N10", "C100", "C20"],
                    "The 10¢ coin says 10¢. It is <b>%s</b>. $10 is a note."))
    its.append(abcd("Which one is the $1 coin?", "C100", ["N2", "C10", "N10"],
                    "The $1 coin says $1. It is <b>%s</b>."))
    its.append(abcd("Which one is the 50¢ coin?", "C50", ["C5", "N50", "C20"],
                    "The 50¢ coin says 50¢. It is <b>%s</b>. $50 is a note."))
    its.append(abcd("Which one is the $50 note?", "N50", ["N5", "C50", "N10"],
                    "The $50 note says $50. It is <b>%s</b>."))
    mix = ["N5", "C10", "C50", "N2", "C20", "C5", "C100"]
    s(fig(money_svg(mix, per_row=4, label="money: 2 notes and 5 coins")) + "How many coins are there?",
      "5", ["7", "2", "4"],
      "Coins are round. Count only the round ones: <b>5</b> coins. 7 counts the notes too.")
    mix2 = ["C20", "N10", "C5", "N2", "N50", "C100"]
    s(fig(money_svg(mix2, per_row=3, label="money: 3 notes and 3 coins")) + "How many notes are there?",
      "3", ["6", "2", "4"],
      "Notes are paper money. They are long. There are <b>3</b> notes: $10, $2 and $50. The $1 is a coin.")
    s(fig(money_svg(["N2", "C100", "C50", "C20"], gap=12, label="money: $2, $1, 50¢, 20¢")) + "Which one is a note?",
      "$2", ["$1", "50¢", "20¢"],
      "The <b>$2</b> is a note. The $1 is a coin, not a note.")
    s(fig(money_svg(["C20", "C5", "C100", "C10", "C50"], gap=8, label="money: 20¢, 5¢, $1, 10¢, 50¢ coins"))
      + "Which coin is the smallest?",
      "5¢ coin", ["10¢ coin", "50¢ coin", "$1 coin"],
      "The <b>5¢ coin</b> is the smallest. It is also worth the least.")
    s(fig(money_svg(["C50", "C10", "C100", "C5", "C20"], gap=8, label="money: 50¢, 10¢, $1, 5¢, 20¢ coins"))
      + "Which coin is worth the most?",
      "$1 coin", ["50¢ coin", "20¢ coin", "5¢ coin"],
      "$1 is 100¢. That is more than 50¢. The <b>$1 coin</b> is worth the most.")
    s(fig(money_svg(["N10", "N2", "N50", "N5"], per_row=2, gap=10, label="money: $10, $2, $50, $5 notes"))
      + "Which note is worth the most?",
      "$50 note", ["$10 note", "$5 note", "$2 note"],
      "50 is the biggest number. The <b>$50 note</b> is worth the most.")
    s(fig(one("C20")) + "How do we say 20¢?", "twenty cents", ["twenty dollars", "two cents", "two dollars"],
      "The ¢ sign means cents. 20¢ is <b>twenty cents</b>.")
    s(fig(one("N50")) + "How do we say $50?", "fifty dollars", ["fifty cents", "five dollars", "fifteen dollars"],
      "The $ sign means dollars. $50 is <b>fifty dollars</b>.")
    s(fig(one("C100")) + "How many cents make $1?", "100¢", ["10¢", "1¢", "50¢"],
      "$1 is the same as <b>100¢</b>. Two 50¢ coins also make $1.")
    s(fig(one("C10")) + "How do we write ten cents?", "10¢", ["$10", "10$", "¢10"],
      "Write the number, then the ¢ sign: <b>10¢</b>. $10 is ten dollars.")
    assert len(its) == 20
    return {"title": "Name the coins and notes", "items": its}


# ============================================================ set 2: count coins in cents (up to $1)
def set_cents(P, rnd):
    its = []
    groups = [
        ["C10"] * 3, ["C5"] * 4, ["C20"] * 3, ["C10"] * 6, ["C50", "C50"],
        ["C20", "C10", "C5"], ["C50", "C10", "C10"], ["C20", "C20", "C10", "C5"],
        ["C50", "C20", "C5"], ["C10", "C10", "C5", "C5", "C5"], ["C50", "C20", "C20", "C10"],
        ["C20", "C20", "C20", "C5", "C5"], ["C50", "C10", "C5", "C5"], ["C20", "C10", "C10", "C10", "C5"],
        ["C50", "C20", "C10", "C5", "C5"], ["C20", "C20", "C20", "C20", "C10"],
    ]
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "What is the total?", "%s finds these coins in %s bag. How much is it?",
             "%s puts these coins in a money box. How much is in it?"]
    for i, g in enumerate(groups):
        toks = srt(g)
        if len(set(toks)) > 1 and i % 3 == 2:
            rnd.shuffle(toks)
        T = total(toks)
        n = len(toks)
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if st.count("%s") == 2:
            st = st % (nm, his if "bag" in st else he)
        elif "%s" in st:
            st = st % nm
        q = fig(money_svg(toks)) + st
        e = count_on(toks, C)
        small = min(VAL[t] for t in toks)
        big = max(VAL[t] for t in toks)
        cands = [("%d¢" % n), ("$%d" % T if T < 100 else "$100"), T - small, T + small, T + big, T - big]
        it = mcq(q, T, cands, e, C)
        notes = []
        if "%d¢" % n in it["c"]:
            notes.append("%d¢ counts the coins, not the cents." % n)
        mix = "$%d" % T if T < 100 else "$100"
        if mix in it["c"]:
            notes.append("%s is dollars. Coins under $1 are cents (¢)." % mix if T < 100 else
                         "$100 is dollars. 100¢ is only $1.")
        it["e"] += " " + " ".join(notes) if notes else ""
        its.append(it)
    its.append(mcq(fig(money_svg(["C10"] * 4, under=["10¢", "20¢", "30¢", "?"], label="counting 10¢ coins: 10¢, 20¢, 30¢, ?"))
                   + "Count by 10s. What comes next?", 40, [31, 50, 4],
                   "Count by 10s: 10¢, 20¢, 30¢, <b>40¢</b>. 31¢ counts by 1s.", C))
    its.append(mcq(fig(money_svg(["C20"] * 4, under=["20¢", "40¢", "60¢", "?"], label="counting 20¢ coins: 20¢, 40¢, 60¢, ?"))
                   + "Count by 20s. What comes next?", 80, [70, 61, 100],
                   "Count by 20s: 20¢, 40¢, 60¢, <b>80¢</b>. 70¢ counts by 10s.", C))
    its.append(mcq(fig(one("C100")) + "How many 10¢ coins make $1?", "10", ["1", "100", "5"],
                   "Count by 10s: 10¢, 20¢, … 100¢. That is <b>10</b> coins. 100¢ = $1."))
    its.append(mcq(fig(one("C50")) + "Which coins make 50¢?",
                   "five 10¢ coins", ["five 5¢ coins", "two 20¢ coins", "fifty 10¢ coins"],
                   "10¢, 20¢, 30¢, 40¢, 50¢. <b>Five 10¢ coins</b> make 50¢. Five 5¢ coins make only 25¢."))
    assert len(its) == 20
    return {"title": "Count coins in cents (up to $1)", "items": its}


# ============================================================ set 3: count notes in dollars (up to $100)
def set_dollars(P, rnd):
    its = []
    groups = [
        ["N2"] * 3, ["N5"] * 4, ["N10"] * 5, ["N50", "N50"], ["N2"] * 6, ["N10"] * 7, ["N5"] * 3,
        ["N10", "N5", "N2"], ["N50", "N5", "N2", "N2"], ["N10", "N10", "N5", "N5", "N2"], ["N50", "N10", "N5"],
        ["N10", "N5", "N5", "N2", "N2"], ["N50", "N10", "N10", "N10", "N5", "N2"], ["N10"] * 4 + ["N5"],
        ["N50", "N2", "N2", "N2"], ["N50", "N10", "N10"],
    ]
    stems = ["How much money is this?", "%s has these notes. How much does %s have?",
             "What is the total?", "%s keeps these notes in %s wallet. How much is it?",
             "%s puts these notes in a red packet. How much is in it?"]
    for i, g in enumerate(groups):
        toks = srt(g)
        T = total(toks)
        n = len(toks)
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if st.count("%s") == 2:
            st = st % (nm, his if "wallet" in st else he)
        elif "%s" in st:
            st = st % nm
        q = fig(money_svg(toks, per_row=4)) + st
        e = count_on(toks, D)
        small = min(VAL[t] for t in toks)
        big = max(VAL[t] for t in toks)
        cents = "%d¢" % (T // 100) if T < 10000 else None
        cands = ["$%d" % n, cents, T - small, T + small, T - big]
        it = mcq(q, T, cands, e, D)
        notes = []
        if "$%d" % n in it["c"]:
            notes.append("$%d counts the notes, not the dollars." % n)
        if cents and cents in it["c"]:
            notes.append("Notes are dollars ($), not cents (¢).")
        it["e"] += " " + " ".join(notes) if notes else ""
        its.append(it)
    its.append(mcq(fig(money_svg(["N5"] * 4, per_row=4, under=["$5", "$10", "$15", "?"], label="counting $5 notes: $5, $10, $15, ?"))
                   + "Count by 5s. What comes next?", "$20", ["$16", "$25", "$50"],
                   "Count by 5s: $5, $10, $15, <b>$20</b>. $16 counts by 1s."))
    its.append(mcq(fig(one("N50")) + "How many $10 notes make $50?", "5", ["50", "10", "4"],
                   "Count by 10s: $10, $20, $30, $40, $50. That is <b>5</b> notes."))
    its.append(mcq(fig(one("N10")) + "How many $5 notes make $10?", "2", ["5", "10", "1"],
                   "$5 + $5 = $10. That is <b>2</b> notes."))
    its.append(mcq(fig(one("N10")) + "How many $2 notes make $10?", "5", ["2", "10", "8"],
                   "Count by 2s: $2, $4, $6, $8, $10. That is <b>5</b> notes."))
    assert len(its) == 20
    return {"title": "Count notes in dollars (up to $100)", "items": its}


# ============================================================ set 4: which is more?
def set_compare(P, rnd):
    its = []
    SAME, CANT = "They are the same.", "You cannot tell."

    def pair(a, b, more=True, note=""):
        hi, lo = (a, b) if VAL[a] > VAL[b] else (b, a)
        right = hi if more else lo
        other = lo if more else hi
        word = "more" if more else "less"
        q = fig(money_svg([a, b], gap=16, label="%s and %s" % (ONE(a), ONE(b)))) + "Which is worth %s?" % word
        e = "%s is %s than %s. So the <b>%s</b> is worth %s.%s" % (lab(VAL[right]), word, lab(VAL[other]), ONE(right), word, note)
        its.append(mcq(q, "the " + ONE(right), ["the " + ONE(other), SAME, CANT], e))

    pair("C20", "C50")
    pair("C10", "C5")
    pair("C50", "C100", note=" $1 is 100¢.")
    pair("C100", "N2")
    pair("C50", "N5", note=" 50 is a bigger number, but 50¢ is cents. $5 is dollars.")
    pair("N10", "N5", more=False)
    pair("N2", "C20", more=False, note=" Cents are worth less than dollars.")
    pair("N50", "N10", more=False)

    def groups(a, b, ca, cb, fmt):
        ta, tb = total(a), total(b)
        q = fig(two_groups(a, b, ca, cb, "%s and %s" % (ca, cb))) + "Which side is worth more?"
        na = "the " + (ONE(a[0]) if len(a) == 1 else ca)
        nb = "the " + (ONE(b[0]) if len(b) == 1 else cb)
        e = "%s make %s. %s %s %s. " % (cap(ca), fmt(ta), cap(cb), "make" if len(b) > 1 else "is", fmt(tb))
        if len(a) == 1:
            e = "%s is %s. %s %s %s. " % (cap(ca), fmt(ta), cap(cb), "make" if len(b) > 1 else "is", fmt(tb))
        if ta == tb:
            right, wrong = SAME, [na, nb, CANT]
            e += "<b>They are the same.</b>"
        else:
            hi, lo = (na, nb) if ta > tb else (nb, na)
            right, wrong = hi, [lo, SAME, CANT]
            are = "are" if len(a if ta > tb else b) > 1 else "is"
            e += "So <b>%s</b> %s worth more." % (right, are)
            more_side = na if len(a) > len(b) else nb
            if len(a) != len(b) and right != more_side:
                e += " More coins or notes is not always more money."
        its.append(mcq(q, right, wrong, e))

    groups(["C5"] * 4, ["C50"], "four 5¢ coins", "one 50¢ coin", C)
    groups(["C10"] * 5, ["C50"], "five 10¢ coins", "one 50¢ coin", C)
    groups(["C20"] * 3, ["C50"], "three 20¢ coins", "one 50¢ coin", C)
    groups(["N10"], ["N5", "N5"], "one $10 note", "two $5 notes", D)
    groups(["N2"] * 3, ["N5"], "three $2 notes", "one $5 note", D)
    groups(["N2"] * 4, ["N10"], "four $2 notes", "one $10 note", D)
    groups(["N50"], ["N5"] * 6, "one $50 note", "six $5 notes", D)

    def amounts(a, b, more, e):
        word = "more" if more else "less"
        q = fig(tags_svg([(a, "drink"), (b, "snack")])) + "Which costs %s?" % word
        its.append(mcq(q, "the %s" % e[0], ["the %s" % e[1], SAME, CANT], e[2]))

    amounts("80¢", "$1", True, ("snack", "drink",
            "$1 is 100¢. 100¢ is more than 80¢. So <b>the snack</b> costs more. Do not just compare 80 and 1."))
    amounts("90¢", "$9", False, ("drink", "snack",
            "90¢ is less than $1. $9 is nine dollars. So <b>the drink</b> costs less."))
    q = fig(tags_svg([("$1", "drink"), ("100¢", "snack")])) + "Which costs more?"
    its.append(mcq(q, SAME, ["the drink", "the snack", CANT],
                   "$1 is the same as 100¢. <b>They are the same.</b> 100 is a big number, but it is cents."))

    def most(toks, more=True):
        word = "most" if more else "least"
        best = max(toks, key=VAL.get) if more else min(toks, key=VAL.get)
        others = [x for x in toks if x != best]
        q = fig(money_svg(toks, gap=10, per_row=4, label="money: " + ", ".join(ONE(t) for t in toks))) \
            + "Which is worth the %s?" % word
        e = "In order: %s. The <b>%s</b> is worth the %s." % (", ".join(lab(VAL[t]) for t in srt(toks)[::-1]), ONE(best), word)
        if not more and best == "C50":
            e += " 50¢ is less than $1."
        its.append(mcq(q, "the " + ONE(best), ["the " + ONE(x) for x in others], e))

    most(["C50", "N5", "C20", "N2"])
    most(["N2", "C100", "C50", "N10"], more=False)
    assert len(its) == 20, len(its)
    return {"title": "Which is more?", "items": its}


# ============================================================ set 5: buying a snack (word problems)
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=str):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    add(fig(money_svg(["C50", "C10"], gap=12, label="money: 50¢ and 10¢"))
        + "A packet of milk costs 60¢. %s has these coins. Is it enough?" % nm,
        "Yes, %s has 60¢." % he, ["No, %s has 2¢." % he, "No, %s has 50¢." % he, "No, %s needs $60." % he],
        "50¢, 60¢. %s has 60¢. <b>Yes, it is enough.</b> 2¢ counts the coins." % nm)
    nm, he, his = P.next()
    add(fig(money_svg(["C20"] * 2, gap=12, label="money: 20¢ and 20¢"))
        + "A bun costs 50¢. %s has these coins. Is it enough?" % nm,
        "No, %s needs 10¢ more." % he, ["Yes, %s has 50¢." % he, "Yes, %s has 2 coins." % he, "No, %s needs 30¢ more." % he],
        "20¢, 40¢. %s has 40¢. 40¢ + 10¢ = 50¢. <b>%s needs 10¢ more.</b>" % (nm, cap(he)))
    nm, he, his = P.next()
    add(fig(tags_svg([("60¢", "bun"), ("30¢", "drink")])) + "%s buys a bun and a drink. How much does %s spend?" % (nm, he),
        90, [30, "$90", 80, 9],
        "60¢ + 30¢ = <b>90¢</b>. 30¢ takes away instead of adding.", C)
    nm, he, his = P.next()
    add(fig(money_svg(["C50", "C20", "C10"], gap=10, label="money: 50¢, 20¢, 10¢"))
        + "%s has 80¢. %s buys biscuits for 50¢. How much is left?" % (nm, cap(he)),
        30, [50, "$30", 20, 3],
        "80¢ − 50¢ = <b>30¢</b>. 50¢ is the price, not what is left.", C)
    nm, he, his = P.next()
    add(fig(one("N5")) + "%s has $5. %s buys a toy car for $3. How much is left?" % (nm, cap(he)),
        "$2", ["$8", "2¢", "$3"],
        "$5 − $3 = <b>$2</b>. $8 adds instead of taking away.")
    nm, he, his = P.next()
    add(fig(tag_svg("$7", "storybook")) + "%s pays for this book with a $10 note. What is %s change?" % (nm, his),
        "$3", ["$7", "$17", "3¢"],
        "$10 − $7 = <b>$3</b>. $7 is the price, not the change.")
    nm, he, his = P.next()
    add(fig(tags_svg([("$4", "chicken rice"), ("$2", "drink")]))
        + "At the hawker centre, %s buys both. How much is that?" % nm,
        "$6", ["$2", "6¢", "$8"],
        "$4 + $2 = <b>$6</b>. $2 takes away instead of adding.")
    add(fig(tag_svg("70¢", "ice pop")) + "Which two coins pay exactly 70¢?",
        "50¢ and 20¢", ["50¢ and 10¢", "20¢ and 5¢", "$50 and 20¢"],
        "50¢ + 20¢ = <b>70¢</b>. 50¢ + 10¢ is only 60¢.")
    its.append(abcd("A sweet costs 20¢. Which one pays exactly?", "C20", ["C10", "N2", "C50"],
                    "The 20¢ coin pays exactly 20¢. It is <b>%s</b>. The $2 note is dollars, not cents."))
    its.append(abcd("A book costs $5. Which one pays exactly?", "N5", ["C5", "N2", "C50"],
                    "The $5 note pays exactly $5. It is <b>%s</b>. 5¢ and 50¢ are cents."))
    nm, he, his = P.next()
    add(fig(money_svg(["C20"] * 3, gap=12, label="money: three 20¢ coins"))
        + "%s has these coins. A drink costs 50¢. Can %s buy it?" % (nm, he),
        "Yes, %s has 60¢." % he, ["No, %s has 3¢." % he, "No, %s has 30¢." % he, "Yes, %s has $60." % he],
        "Count by 20s: 20¢, 40¢, 60¢. 60¢ is more than 50¢, so <b>yes</b>. 30¢ counts by 10s.")
    nm, he, his = P.next()
    add(fig(money_svg(["N2"] * 4, per_row=4, label="money: four $2 notes"))
        + "%s saves a $2 note each week for 4 weeks. How much?" % nm,
        "$8", ["$4", "$6", "8¢"],
        "Count by 2s: $2, $4, $6, $8. That is <b>$8</b>. $4 counts the notes.")
    nm, he, his = P.next()
    add(fig(money_svg(["N10", "N5", "N2"], gap=10, label="money: $10, $5 and $2 notes"))
        + "At Chinese New Year, %s gets these in red packets. How much?" % nm,
        "$17", ["$3", "$15", "$27"],
        "$10, $15, $17. That is <b>$17</b>. $3 counts the notes.")
    nm, he, his = P.next()
    add(fig(money_svg(["C50", "C20", "C20"], gap=10, label="money: 50¢, 20¢, 20¢"))
        + "An ice cream costs $1. %s has these coins. How much more does %s need?" % (nm, he),
        10, [90, 30, "$9"],
        "50¢, 70¢, 90¢. %s has 90¢. $1 is 100¢. 90¢ + 10¢ = 100¢. %s needs <b>10¢</b> more. 90¢ is what %s has."
        % (nm, cap(he), he), C)
    nm, he, his = P.next()
    add(fig(tag_svg("40¢", "packet of milk")) + "%s buys 2 packets of milk. How much is that?" % nm,
        80, [40, 60, "$80"],
        "40¢ + 40¢ = <b>80¢</b>. 40¢ is the price of only 1 packet.", C)
    nm, he, his = P.next()
    add(fig(money_svg(["N5", "N2", "N2"], gap=10, label="money: $5, $2 and $2 notes"))
        + "A book at the book fair costs $9. %s has these notes. Is it enough?" % nm,
        "Yes, %s has $9." % he, ["No, %s has $3." % he, "No, %s has $7." % he, "Yes, %s has $10." % he],
        "$5, $7, $9. %s has $9. <b>Yes, it is enough.</b> $3 counts the notes." % nm)
    nm, he, his = P.next()
    add(fig(tags_svg([("90¢", "drink"), ("$2", "sandwich")])) + "%s looks at the canteen. Which costs more?" % nm,
        "the sandwich", ["the drink", "They are the same.", "You cannot tell."],
        "90¢ is less than $1. $2 is more than $1. So <b>the sandwich</b> costs more. Do not compare 90 and 2.")
    nm, he, his = P.next()
    add(fig(money_svg(["N10"], label="money: one $10 note")) + "Mrs Lim buys mandarin oranges for $20. How many $10 notes does she pay?",
        "2", ["20", "1", "10"],
        "$10, $20. That is <b>2</b> notes. 20 is the dollars, not the notes.")
    nm, he, his = P.next()
    add(fig(money_svg(["C50", "C20", "C20", "C5"], gap=10, label="money: 50¢, 20¢, 20¢, 5¢"))
        + "%s has these coins. %s buys a 75¢ snack. How much is left?" % (nm, cap(he)),
        20, [75, 95, "$20"],
        "50¢, 70¢, 90¢, 95¢. %s has 95¢. 95¢ − 75¢ = <b>20¢</b>. 75¢ is the price." % nm, C)
    nm, he, his = P.next()
    add(fig(tags_svg([("$5", "pencil case"), ("$3", "eraser set")]))
        + "%s buys both. %s pays with a $10 note. What is the change?" % (nm, cap(he)),
        "$2", ["$8", "$5", "2¢"],
        "$5 + $3 = $8. $10 − $8 = <b>$2</b>. $8 is the cost, not the change.")
    assert len(its) == 20, len(its)
    return {"title": "Buying a snack (word problems)", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Singapore coins and notes</h2>"
        "<p>Coins are round. Notes are paper money. Each one shows its value. "
        "The ¢ sign means cents. The $ sign means dollars.</p>"
        "<figure class='sn-fig'>" + money_svg(["C5", "C10", "C20", "C50", "C100"], gap=10,
                                              label="Singapore coins: 5¢, 10¢, 20¢, 50¢, $1") +
        "<figcaption>Coins: 5¢, 10¢, 20¢, 50¢ and $1.</figcaption></figure>"
        "<figure class='sn-fig'>" + money_svg(["N2", "N5", "N10", "N50"], per_row=4, gap=10,
                                              label="Singapore notes: $2, $5, $10, $50") +
        "<figcaption>Notes: $2, $5, $10 and $50.</figcaption></figure>"
        + table(["We write", "We say"], [
            ["20¢", "twenty cents"],
            ["$1", "one dollar = 100¢"],
            ["$5", "five dollars"],
            ["$50", "fifty dollars"],
        ]) +
        "<h2>Count coins in cents</h2>"
        "<p>Start with the coin worth the most. Count on with each coin. Write ¢ after the number.</p>"
        "<figure class='sn-fig'>" + money_svg(["C50", "C20", "C10", "C5"], gap=10, under=["50¢", "70¢", "80¢", "85¢"],
                                              label="counting coins: 50¢, 70¢, 80¢, 85¢") +
        "<figcaption>50¢, 70¢, 80¢, 85¢. That is 85¢.</figcaption></figure>"
        + ex("Example", "How much are three 20¢ coins?", "Count by 20s: 20¢, 40¢, 60¢.", "60¢")
        + "<h2>Count notes in dollars</h2>"
        "<p>Count notes the same way. Write $ before the number.</p>"
        "<figure class='sn-fig'>" + money_svg(["N10", "N10", "N5", "N2"], per_row=4, gap=10,
                                              under=["$10", "$20", "$25", "$27"],
                                              label="counting notes: $10, $20, $25, $27") +
        "<figcaption>$10, $20, $25, $27. That is $27.</figcaption></figure>"
        + ex("Example", "Siti buys a book for $6. She pays with a $10 note. What is her change?",
             "$10 − $6 = $4.", "$4")
        + "<h2>Which is more?</h2>"
        "<p>Look at the value, not the number of coins. One 50¢ coin is more than four 5¢ coins.</p>"
        "<figure class='sn-fig'>" + two_groups(["C5"] * 4, ["C50"], "four 5¢: 20¢", "one 50¢: 50¢",
                                               "four 5¢ coins make 20¢, one 50¢ coin is 50¢") +
        "<figcaption>4 coins make 20¢. 1 coin is 50¢. 50¢ is more.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Three 10¢ coins, so 3¢", "Count the value: 10¢, 20¢, 30¢"],
            ["Writing 30¢ as $30", "Coins under $1 are cents. Write 30¢"],
            ["50¢ is more than $5", "$5 is dollars. Cents are worth less than $1"],
            ["More coins is more money", "Four 5¢ coins (20¢) are less than one 50¢ coin"],
        ])
    )


FAQ = [
    {"q": "What do Primary 1 students learn about money?",
     "a": "In Primary 1, students name Singapore coins and notes, count coins in cents up to $1, and count notes in dollars up to $100. They also compare amounts and solve simple buying problems."},
    {"q": "How can I help my child count money at home?",
     "a": "Use real coins and notes. Sort them, then count on from the one worth the most, such as 50¢, 70¢, 80¢. Let your child pay for a small snack and check the change."},
    {"q": "What is the most common mistake with money in P1?",
     "a": "Counting the coins instead of their value, so three 10¢ coins become 3¢. Many children also mix up cents and dollars, writing 30¢ as $30."},
    {"q": "Is money in the MOE Primary 1 syllabus?",
     "a": "Yes. Money is part of Number and Algebra in the MOE 2021 Primary Mathematics Syllabus for Primary 1. Amounts like $1.20 with dollars and cents together come in Primary 2."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(61807)
    P = People(rnd)
    sets = [set_names(P, rnd), set_cents(P, rnd), set_dollars(P, rnd), set_compare(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert set(it) == {"q", "c", "a", "e"}
            assert len(set(it["c"])) == 4, it
            vv = [v for v in (mval(c) for c in it["c"]) if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "money", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Money",
        "seo_title": "P1 Money Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Money",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Money",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Counting amounts of money in cents up to $1 and in dollars up to $100",
        "meta_desc": "Free P1 money practice: name Singapore coins and notes, count cents up to $1 and dollars up to $100, compare and buy. 100 questions with answers.",
        "key_big": "Count the value of each coin or note, not how many there are.",
        "key_sub": "50¢, 20¢ and 10¢ coins: 50¢, 70¢, 80¢. That is 80¢.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "(money|A, B, C|counting|Singapore|compare|price tags)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
