# -*- coding: utf-8 -*-
"""
CA Grade 1 Math: Money (Ontario Mathematics Curriculum 2020, Grade 1: F1.1)
  python3 tools/gen_caon_math_g1_money.py
Grade 1: name the Canadian coins up to 50¢ and the coins and bills up to $50, and compare their values.
Simple collections only: nickels by 5s and dimes by 10s to 50¢, bills to $50. Coin amounts in cents (35¢),
bill and dollar-coin amounts in whole dollars ($25).
Canadian coins: nickel 5¢, dime 10¢ (the smallest coin), quarter 25¢, loonie $1 (11 sides, gold colour),
toonie $2 (silver ring, gold centre). No pennies. Bills: $5 blue, $10 purple, $20 green, $50 red.
Coins and bills are simple labelled shapes (no real designs). Very short sentences for 6-7 year olds.
Wrong answers come from real mistakes: the small dime taken as worth less than the bigger nickel, counting
coins (or bills) instead of their value, a quarter taken as 20¢, a toonie taken as $1, counting nickels by 10s
or dimes by 5s, missing or double-counting one coin, more coins taken as more money.
"A-D picture" questions build the picture after the answer position is chosen, so the choices stay A, B, C, D.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

# ------------------------------------------------------------ money facts
ORDER = ["B50", "B20", "B10", "B5", "T", "L", "Q", "D", "N"]   # biggest value first
VAL = {"B50": 5000, "B20": 2000, "B10": 1000, "B5": 500, "T": 200, "L": 100, "Q": 25, "D": 10, "N": 5}
ONE = {"B50": "$50 bill", "B20": "$20 bill", "B10": "$10 bill", "B5": "$5 bill",
       "T": "toonie", "L": "loonie", "Q": "quarter", "D": "dime", "N": "nickel"}
MANY = {k: (v + "s") for k, v in ONE.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius in proportion to the real coins (mm): dime 18, nickel 21.2, quarter 23.9, loonie 26.5, toonie 28
COIN = {"D": (18, SILVER, 14), "N": (21, SILVER, 15), "Q": (24, SILVER, 15), "L": (26, GOLD, 16), "T": (28, SILVER, 16)}
BILL = {"B5": ("#c4dcf2", "#1f5f99"), "B10": ("#ddcbee", "#5b2d8a"), "B20": ("#cbe7c4", "#2f7a2a"),
        "B50": ("#f5c6c6", "#a32020")}
BILL_W, BILL_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def C(v):
    assert isinstance(v, int) and v > 0, v
    return "%d¢" % v


def D(v):
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
        return "Each %s is %s. Count by %s: %s. That is <b>%s</b>." % (
            ONE[t], fmt(VAL[t]), "%ds" % (VAL[t] if VAL[t] < 100 else VAL[t] // 100),
            ", ".join(run), fmt(T))
    return "Start with the biggest one. Count on: %s. That is <b>%s</b>." % (", ".join(run), fmt(T))


# ------------------------------------------------------------ typical mistakes
def m_count(toks):
    return len(toks)


def m_swap(toks):
    """nickel taken as 10¢ and dime as 5¢ (bigger coin = more)"""
    sw = {"N": 10, "D": 5}
    return sum(sw.get(t, VAL[t]) for t in toks)


def m_quarter20(toks):
    return sum(20 if t == "Q" else VAL[t] for t in toks)


def m_toonie1(toks):
    return sum(100 if t == "T" else VAL[t] for t in toks)


def kinds(toks):
    return [t for t, n in counts(toks)]


def m_skip(toks, k=-1):
    return total(toks) - VAL[kinds(toks)[k]]


def m_twice(toks, k=-1):
    return total(toks) + VAL[kinds(toks)[k]]


def m_same_step(toks):
    s, prev = 0, None
    for t in srt(toks):
        s += VAL[prev] if prev is not None and t != prev else VAL[t]
        prev = t
    return s


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=str, cmax=None):
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or (fmt is D and c % 100) or (cmax and c > cmax):
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


def draw_tok(t, cx, cy, hide=False):
    """one coin or one bill, labelled with its value (or '?' when hide)"""
    if t.startswith("B"):
        fill, edge = BILL[t]
        x, y = cx - BILL_W / 2, cy - BILL_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, BILL_W, BILL_H, fill, edge, x + 5, y + 5, BILL_W - 10, BILL_H - 10, edge)
                + text(cx, cy + 7, "?" if hide else lab(VAL[t]), 20, col=edge))
    r, (fill, edge), fs = COIN[t]
    if t == "L":
        shape = ("<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (polygon(cx, cy, r, 11), fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 6, edge))
    elif t == "T":
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (cx, cy, r - 10, GOLD[0], GOLD[1]))
    else:
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, edge))
    if hide:
        return shape + text(cx, cy + 7, "?", 20)
    return shape + text(cx, cy + fs * 0.36, lab(VAL[t]), fs)


def under_w(s):
    return len(s) * 8.6 + 8


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None, hide=False):
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
            s.append(draw_tok(t, x + w / 2, y + hh / 2, hide))
            if under:
                s.append(text(x + w / 2, y + hh + 18, under[k], 15, col=GREEN))
            x += w + gap
            k += 1
        y += rh + gap
    return svg_wrap(int(math.ceil(W)), int(math.ceil(H)), "".join(s), label or ("money: " + group(toks)))


def two_groups(left, right, capl, capr, label):
    """two piles of money side by side, a line between them, a caption under each"""
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


LET = "ABCD"


def abcd(stem, right, others, e, hide=False, names=False):
    """A-D picture: the right one goes to the answer position chosen later"""
    assert len(others) == 3 and right not in others

    def build(t):
        toks = others[:t] + [right] + others[t:]
        under = [(LET[i] + ": " + ONE[x]) if names else LET[i] for i, x in enumerate(toks)]
        lbl = "A, B, C and D: " + ", ".join("%s %s" % (LET[i], ONE[x]) for i, x in enumerate(toks))
        svg = money_svg(toks, per_row=4, gap=10, under=under, hide=hide, label=lbl)
        return {"q": fig(svg) + stem, "c": list(LET), "a": t, "e": e % LET[t]}
    return {"_build": build, "q": stem + "|" + right}


# ============================================================ set 1: names of coins and bills
def set_names(P, rnd):
    its = []

    def s(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    tips = {
        "N": ("nickel", ["dime", "quarter", "toonie"], "This is a <b>nickel</b>. It is worth 5¢."),
        "D": ("dime", ["nickel", "quarter", "loonie"], "This is a <b>dime</b>. It is worth 10¢. It is the smallest coin."),
        "Q": ("quarter", ["dime", "nickel", "loonie"], "This is a <b>quarter</b>. It is worth 25¢."),
        "L": ("loonie", ["toonie", "quarter", "dime"], "This is a <b>loonie</b>. It is gold in colour. It is worth $1."),
        "T": ("toonie", ["loonie", "quarter", "nickel"], "This is a <b>toonie</b>. It has a gold centre. It is worth $2."),
    }
    for t in ["N", "D", "Q", "L", "T"]:
        right, wrong, e = tips[t]
        w, h = tok_size(t)
        svg = svg_wrap(w + 8, h + 8, draw_tok(t, (w + 8) / 2, (h + 8) / 2), "one coin worth " + lab(VAL[t]))
        s(fig(svg) + "What is this coin called?", right, wrong, e)
    its.append(abcd("Which one is the nickel?", "N", ["D", "Q", "L"],
                    "The nickel is worth 5¢. It is <b>%s</b>. The dime is smaller, but it is 10¢."))
    its.append(abcd("Which one is the dime?", "D", ["N", "Q", "T"],
                    "The dime is worth 10¢. It is <b>%s</b>. It is the smallest coin."))
    its.append(abcd("Which one is the quarter?", "Q", ["N", "D", "L"],
                    "The quarter is worth 25¢. It is <b>%s</b>."))
    its.append(abcd("Which one is the loonie?", "L", ["T", "Q", "D"],
                    "The loonie is worth $1. It has 11 sides. It is <b>%s</b>."))
    its.append(abcd("Which one is the toonie?", "T", ["L", "Q", "N"],
                    "The toonie is worth $2. It is <b>%s</b>."))
    its.append(abcd("Which one is a bill?", "B10", ["T", "Q", "L"],
                    "The $10 bill is a bill. It is <b>%s</b>. The toonie, quarter and loonie are coins."))
    s("Which coin has 11 sides?", "the loonie", ["the toonie", "the quarter", "the dime"],
      "The <b>loonie</b> has 11 sides. It is gold in colour.")
    s(fig(money_svg(["T", "L"], gap=14, label="a toonie and a loonie")) + "Which coin has a gold centre?",
      "the toonie", ["the loonie", "the quarter", "the nickel"],
      "The <b>toonie</b> has a silver ring and a gold centre. The loonie is all gold.")
    s(fig(money_svg(["Q", "N", "D", "L"], gap=10, label="a quarter, a nickel, a dime and a loonie"))
      + "Which coin is the smallest?",
      "the dime", ["the nickel", "the quarter", "the loonie"],
      "The <b>dime</b> is the smallest coin. It is worth 10¢.")
    toks = ["Q", "B5", "L", "B20", "D"]
    s(fig(money_svg(toks, label="a quarter, a $5 bill, a loonie, a $20 bill and a dime"))
      + "How many coins are there?", "3", ["5", "2", "4"],
      "The quarter, the loonie and the dime are coins. That is <b>3</b> coins. The $5 and $20 are bills.")
    s("What is the name of the $1 coin?", "loonie", ["toonie", "quarter", "dime"],
      "The $1 coin is the <b>loonie</b>. The $2 coin is the toonie.")
    s("What is the name of the $2 coin?", "toonie", ["loonie", "quarter", "nickel"],
      "The $2 coin is the <b>toonie</b>. “Two” and “toonie” sound alike.")
    s("What is the name of the 25¢ coin?", "quarter", ["dime", "nickel", "loonie"],
      "The 25¢ coin is the <b>quarter</b>.")
    s("What is the name of the 10¢ coin?", "dime", ["nickel", "quarter", "loonie"],
      "The 10¢ coin is the <b>dime</b>. The nickel is bigger, but it is only 5¢.")
    s("What is the name of the 5¢ coin?", "nickel", ["dime", "quarter", "toonie"],
      "The 5¢ coin is the <b>nickel</b>.")
    assert len(its) == 20
    return {"title": "Name the coins and bills", "items": its}


# ============================================================ set 2: what each one is worth
def set_values(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=str):
        its.append(mcq(q, right, wrong, e, fmt))

    def hid(t, name=None):
        name = name or ONE[t]
        return fig(money_svg([t], under=[name], hide=True, label="a %s with its value hidden" % name))

    s(hid("N") + "How much is a nickel worth?", 5, [10, 1, 25],
      "A nickel is worth <b>5¢</b>. It is bigger than a dime, but worth less.", C)
    s(hid("D") + "How much is a dime worth?", 10, [5, 1, 25],
      "A dime is worth <b>10¢</b>. It is small, but it is worth more than a nickel.", C)
    s(hid("Q") + "How much is a quarter worth?", 25, [20, 10, 5],
      "A quarter is worth <b>25¢</b>, not 20¢.", C)
    s(hid("L") + "How much is a loonie worth?", "$1", ["$2", "1¢", "25¢"],
      "A loonie is worth <b>$1</b>. The toonie is $2.")
    s(hid("T") + "How much is a toonie worth?", "$2", ["$1", "2¢", "$20"],
      "A toonie is worth <b>$2</b>. The loonie is $1.")
    its.append(abcd("Which coin is worth 5¢?", "N", ["D", "Q", "L"],
                    "The nickel is worth 5¢. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("Which coin is worth 10¢?", "D", ["N", "Q", "T"],
                    "The dime is worth 10¢. It is <b>%s</b>. Small, but worth more than a nickel.", hide=True, names=True))
    its.append(abcd("Which coin is worth 25¢?", "Q", ["D", "N", "L"],
                    "The quarter is worth 25¢. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("Which coin is worth $1?", "L", ["T", "Q", "N"],
                    "The loonie is worth $1. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("Which coin is worth $2?", "T", ["L", "D", "Q"],
                    "The toonie is worth $2. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("Which bill is worth $20?", "B20", ["B5", "B50", "B10"],
                    "Read the number on the bill. The $20 bill is <b>%s</b>."))
    its.append(abcd("Which bill is worth $50?", "B50", ["B10", "B20", "B5"],
                    "Read the number on the bill. The $50 bill is <b>%s</b>."))
    s(hid("D") + "How do we write the value of a dime?", "10¢", ["$10", "1¢", "100¢"],
      "A dime is ten cents. We write <b>10¢</b>. $10 is ten dollars, much more.")
    s(hid("B5", "five dollars") + "How do we write five dollars?", "$5", ["5¢", "$50", "50¢"],
      "Dollars use the $ sign in front: <b>$5</b>. 5¢ is five cents, much less.")
    s(hid("Q") + "How do we write the value of a quarter?", "25¢", ["$25", "52¢", "20¢"],
      "A quarter is twenty-five cents. Cents use the ¢ sign after the number: <b>25¢</b>.")
    s(fig(money_svg(["N", "N"], gap=12, label="2 nickels")) + "2 nickels make the same as 1 ____.",
      "dime", ["quarter", "loonie", "toonie"],
      "5¢ + 5¢ = 10¢. That is the same as 1 <b>dime</b>.")
    s(fig(money_svg(["L", "L"], gap=12, label="2 loonies")) + "2 loonies make the same as 1 ____.",
      "toonie", ["quarter", "dime", "$5 bill"],
      "$1 + $1 = $2. That is the same as 1 <b>toonie</b>.")
    s(fig(money_svg(["D"], label="a dime")) + "How many nickels make 1 dime?", "2", ["5", "10", "1"],
      "A nickel is 5¢. 5¢, 10¢. So <b>2</b> nickels make a dime.")
    s(fig(money_svg(["N", "D"], gap=14, under=["nickel", "dime"], hide=True, label="a nickel and a smaller dime, values hidden"))
      + "The dime is small. How much is it worth?", 10, [5, 1, 2],
      "Size does not tell the value. The small dime is worth <b>10¢</b>. The bigger nickel is 5¢.", C)
    s(fig(money_svg(["Q", "N"], gap=14, under=["quarter", "nickel"], hide=True, label="a quarter and a nickel, values hidden"))
      + "Which coin is worth 25¢?", "the quarter", ["the nickel", "both coins", "neither coin"],
      "The <b>quarter</b> is worth 25¢. The nickel is worth 5¢.")
    assert len(its) == 20
    return {"title": "What is each coin and bill worth?", "items": its}


# ============================================================ set 3: which is worth more?
def set_compare(P, rnd):
    its = []
    SAME, CANT = "They are worth the same.", "You cannot tell."

    def pair(a, b, more=True):
        hi, lo = (a, b) if VAL[a] > VAL[b] else (b, a)
        right = hi if more else lo
        word = "more" if more else "less"
        q = fig(money_svg([a, b], gap=14, under=[ONE[a], ONE[b]], label="a %s and a %s" % (ONE[a], ONE[b]))) + \
            "Which is worth %s?" % word
        e = "The %s is %s. The %s is %s. So the <b>%s</b> is worth %s." % (
            ONE[a], lab(VAL[a]), ONE[b], lab(VAL[b]), ONE[right], word)
        if set([a, b]) == {"N", "D"}:
            e += " The nickel is bigger, but size does not tell the value."
        other = lo if more else hi
        its.append(mcq(q, "the " + ONE[right], ["the " + ONE[other], SAME, CANT], e))

    pair("N", "D")
    pair("D", "Q")
    pair("Q", "L")
    pair("L", "T")
    pair("Q", "N", more=False)
    pair("L", "D", more=False)
    pair("T", "Q", more=False)
    pair("T", "B5")
    pair("B5", "B10")
    pair("B20", "B10")
    pair("B50", "B20", more=False)
    pair("B5", "L", more=False)

    def most(toks, more=True):
        word = "most" if more else "least"
        best = max(toks, key=VAL.get) if more else min(toks, key=VAL.get)
        others = [x for x in toks if x != best]
        q = fig(money_svg(toks, gap=10, per_row=4, under=[ONE[t] for t in toks], label="money: " + ", ".join(ONE[t] for t in toks))) \
            + "Which is worth the %s?" % word
        e = cap(", ".join("%s %s" % (ONE[t], lab(VAL[t])) for t in srt(toks))) + ". The <b>%s</b> is worth the %s." % (ONE[best], word)
        its.append(mcq(q, "the " + ONE[best], ["the " + ONE[x] for x in others], e))

    most(["Q", "D", "L", "N"])
    most(["N", "D", "Q", "T"], more=False)
    most(["B20", "B5", "B50", "B10"])

    def groups(a, b, ca, cb, more_word="more money"):
        ta, tb = total(a), total(b)
        fmt = C if max(ta, tb) < 100 else D
        q = fig(two_groups(a, b, ca, cb, "%s and %s" % (ca, cb))) + "Which side is %s?" % more_word
        na = "the " + (ONE[a[0]] if len(a) == 1 else ca)
        nb = "the " + (ONE[b[0]] if len(b) == 1 else cb)
        if ta == tb:
            right, wrong = SAME, [na, nb, CANT]
        else:
            hi, lo = (na, nb) if ta > tb else (nb, na)
            right, wrong = hi, [lo, SAME, CANT]
            are = "are" if len(a if ta > tb else b) > 1 else "is"
        e = "%s: %s. %s: %s. " % (cap(ca), fmt(ta), cap(cb), fmt(tb))
        if ta == tb:
            e += "<b>They are worth the same.</b>"
        else:
            e += "So <b>%s</b> %s worth more." % (right, are)
            more_side = na if len(a) > len(b) else nb
            if len(a) != len(b) and right != more_side:
                e += " More coins or bills is not always more money."
        its.append(mcq(q, right, wrong, e))

    groups(["N", "N"], ["D"], "2 nickels", "1 dime", "worth more")
    groups(["D", "D", "D"], ["Q"], "3 dimes", "1 quarter", "worth more")
    groups(["Q"], ["N"] * 4, "1 quarter", "4 nickels", "worth more")
    groups(["L"] * 3, ["T"], "3 loonies", "1 toonie", "worth more")
    groups(["B20", "B20"], ["B50"], "2 $20 bills", "1 $50 bill", "worth more")
    assert len(its) == 20
    return {"title": "Which is worth more?", "items": its}


# ============================================================ set 4: count nickels and dimes to 50¢
def set_count(P, rnd):
    its = []
    groups = [
        [("D", 2)], [("N", 2)], [("D", 3)], [("N", 3)], [("N", 4)], [("D", 4)], [("N", 5)], [("D", 5)],
        [("N", 6)], [("N", 7)], [("N", 8)], [("N", 10)],
        [("D", 1), ("N", 1)], [("D", 1), ("N", 2)], [("D", 2), ("N", 1)], [("D", 3), ("N", 1)],
        [("D", 2), ("N", 3)], [("D", 4), ("N", 1)], [("Q", 1), ("N", 1)], [("Q", 1), ("N", 3)],
    ]
    mixed = {14, 16, 17, 19}
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "What is the total?", "%s finds these coins in %s pocket. How much is it?",
             "%s puts these coins in a piggy bank. How much is in it?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T <= 50
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if i < 2:
            st = "Count by %s. How much money is this?" % ("10s" if toks[0] == "D" else "5s")
        if st.count("%s") == 2:
            st = st % (nm, his if "pocket" in st else he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = ("Put the coins in order, biggest first. " if i in mixed else "") + count_on(toks, C)
        cands = [m_count(toks), m_swap(toks), m_skip(toks, -1), m_twice(toks, -1), m_quarter20(toks),
                 m_same_step(toks), m_skip(toks, 0), m_twice(toks, 0)]
        if i % 3 == 1:
            cands = [m_swap(toks)] + cands
        it = mcq(q, T, cands, e, C, cmax=100)
        notes = []
        if C(len(toks)) in it["c"]:
            notes.append("%s counts the coins, not the cents." % C(len(toks)))
        sw = m_swap(toks)
        if sw != T and C(sw) in it["c"]:
            notes.append("%s mixes up the nickel (5¢) and the dime (10¢)." % C(sw))
        if "Q" in toks and m_quarter20(toks) != T and C(m_quarter20(toks)) in it["c"]:
            notes.append("A quarter is 25¢, not 20¢.")
        if notes:
            it["e"] += " " + " ".join(notes)
        its.append(it)
    assert len(its) == 20
    return {"title": "Count nickels and dimes (to 50¢)", "items": its}


# ============================================================ set 5: bills to $50 and word problems
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=str):
        its.append(mcq(q, right, cands, e, fmt))

    def bills(toks, stem, extra="", more=()):
        toks = srt(toks)
        T = total(toks)
        assert T <= 5000
        fmt = D
        cands = [100 * len(toks), m_toonie1(toks), m_skip(toks, -1), m_twice(toks, -1), m_same_step(toks),
                 m_skip(toks, 0), m_twice(toks, 0)] + list(more)
        e = count_on(toks, fmt)
        it = mcq(fig(money_svg(toks)) + stem, T, cands, e, fmt)
        if D(100 * len(toks)) in it["c"] and 100 * len(toks) != T and "T" not in toks:
            it["e"] += " %s counts the pieces, not the dollars." % D(100 * len(toks))
        if "T" in toks and D(m_toonie1(toks)) in it["c"]:
            it["e"] += " A toonie is $2, not $1."
        it["e"] += extra
        its.append(it)

    bills(["B5", "B5"], "How much money is this?")
    bills(["B10"] * 3, "Count by 10s. How much money is this?")
    bills(["B10", "B5"], "What is the total?")
    bills(["B20", "B5"], "How much money is this?")
    bills(["B20", "B20"], "What is the total?")
    bills(["B20", "B10", "B5"], "How much money is this?")
    bills(["L"] * 4, "How much money is this?", more=[C(4), 800], extra=" 4¢ thinks a loonie is 1¢.")
    bills(["T"] * 3, "Count by 2s. How much money is this?")

    SAME = "They have the same."
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    add(fig(two_groups(["B20", "B20"], ["B50"], nm1, nm2, "%s has two $20 bills. %s has one $50 bill." % (nm1, nm2)))
        + "Who has more money?", nm2, [nm1, SAME, "You cannot tell."],
        "%s has $20, $40. %s has $50. $50 is more, so <b>%s</b> has more. 2 bills is not always more money." % (nm1, nm2, nm2))
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    add(fig(two_groups(["B10", "B10"], ["B5"] * 3, nm1, nm2, "%s has two $10 bills. %s has three $5 bills." % (nm1, nm2)))
        + "Who has more money?", nm1, [nm2, SAME, "You cannot tell."],
        "%s has $10, $20. %s has $5, $10, $15. $20 is more, so <b>%s</b> has more." % (nm1, nm2, nm1))
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    add(fig(two_groups(["D", "D"], ["N"] * 3, nm1, nm2, "%s has 2 dimes. %s has 3 nickels." % (nm1, nm2)))
        + "Who has more money?", nm1, [nm2, SAME, "You cannot tell."],
        "%s has 10¢, 20¢. %s has 5¢, 10¢, 15¢. 20¢ is more, so <b>%s</b> has more. More coins is not always more money."
        % (nm1, nm2, nm1))
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    add(fig(two_groups(["B10"], ["B5", "B5"], nm1, nm2, "%s has a $10 bill. %s has two $5 bills." % (nm1, nm2)))
        + "Who has more money?", SAME, [nm1, nm2, "You cannot tell."],
        "%s has $10. %s has $5, $10. <b>They have the same</b>: $10 each." % (nm1, nm2))
    nm, he, his = P.next()
    add("At the bake sale, a cookie costs 25¢. %s pays with 1 coin. Which coin pays exactly?" % nm,
        "a quarter", ["a dime", "a nickel", "a toonie"],
        "A <b>quarter</b> is 25¢, the same as the cookie.")
    nm, he, his = P.next()
    toks = ["D", "D", "D"]
    add(fig(money_svg(toks, label="3 dimes")) + "%s had 2 dimes. %s found 1 more dime. How much does %s have now?" % (nm, cap(he), he),
        30, [21, 3, 20],
        "Count by 10s: 10¢, 20¢, 30¢. %s has <b>30¢</b>. A dime is 10¢, not 1¢, so 21¢ is wrong." % nm, C)
    nm, he, his = P.next()
    add(fig(money_svg(["N"] * 6, label="6 nickels")) + "%s puts 6 nickels in %s piggy bank. How much is in it?" % (nm, his),
        30, [6, 60, 25],
        "Count by 5s: 5¢, 10¢, 15¢, 20¢, 25¢, 30¢. That is <b>30¢</b>. 60¢ counts nickels by 10s.", C)
    nm, he, his = P.next()
    add(fig(money_svg(["D"] * 4, label="4 dimes")) + "%s has 4 dimes. %s gives 1 dime to %s sister. How much is left?"
        % (nm, cap(he), his), 30, [50, 3, 40],
        "%s has 10¢, 20¢, 30¢, 40¢. Take away 1 dime: 40¢ − 10¢ = <b>30¢</b>. 50¢ adds a dime instead." % nm, C)
    nm, he, his = P.next()
    add(fig(money_svg(["B20", "B10"], label="a $20 bill and a $10 bill"))
        + "For the Terry Fox Run, %s gives this money. How much does %s give?" % (nm, he),
        3000, [200, 2000, 4000],
        "$20, then count on 10: $30. %s gives <b>$30</b>. $2 counts the bills, not the dollars." % nm, D)
    nm, he, his = P.next()
    add(fig(money_svg(["T", "L"], label="a toonie and a loonie"))
        + "Hot chocolate at the rink costs $3. %s has these coins. Does %s have enough?" % (nm, he),
        "Yes, %s has $3." % he, ["No, %s has $2." % he, "No, %s has 2¢." % he, "Yes, %s has $4." % he],
        "Toonie $2, loonie $1: $2, $3. %s has $3, so <b>yes</b>. $2 comes from counting the toonie as $1." % nm)
    nm, he, his = P.next()
    add(fig(money_svg(["B10", "B5"], label="a $10 bill and a $5 bill"))
        + "A book costs $20. %s has this money. Does %s have enough?" % (nm, he),
        "No, %s has $15." % he, ["Yes, %s has $20." % he, "No, %s has $2." % he, "Yes, %s has $25." % he],
        "$10, then count on 5: $15. $15 is less than $20, so <b>no</b>. $2 counts the bills, not the dollars.")
    nm, he, his = P.next()
    add(fig(money_svg(["D"] * 5, label="5 dimes")) + "%s has 50¢ in dimes. How many dimes is that?" % nm,
        "5", ["50", "10", "4"],
        "Count by 10s: 10¢, 20¢, 30¢, 40¢, 50¢. That is <b>5</b> dimes. 10 would be nickels.")
    assert len(its) == 20
    return {"title": "Bills to $50 and word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    bills = ["B5", "B10", "B20", "B50"]
    return (
        "<h2>Canadian coins</h2>"
        "<p>Each coin has a name and a value. Size does not tell the value. "
        "The dime is the smallest coin, but it is worth more than the nickel.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2. There are no pennies.</figcaption></figure>"
        + table(["Coin", "Value", "Look for"], [
            ["nickel", "5¢", "bigger than a dime"],
            ["dime", "10¢", "the smallest coin"],
            ["quarter", "25¢", "bigger than a nickel"],
            ["loonie", "$1", "gold colour, 11 sides"],
            ["toonie", "$2", "silver ring, gold centre"],
        ]) +
        "<h2>Canadian bills</h2>"
        "<p>Read the number on the bill. $50 is the most. $5 is the least.</p>"
        "<figure class='sn-fig'>" + money_svg(bills, per_row=4, label="Canadian bills: $5, $10, $20, $50") +
        "<figcaption>Bills: $5, $10, $20 and $50.</figcaption></figure>"
        "<h2>Which is worth more?</h2>"
        "<p>Look at the value, not the size. 10¢ is more than 5¢, so a dime is worth more than a nickel.</p>"
        "<figure class='sn-fig'>" + two_groups(["D", "D", "D"], ["Q"], "3 dimes: 30¢", "1 quarter: 25¢",
                                               "3 dimes make 30¢, 1 quarter is 25¢") +
        "<figcaption>3 dimes are worth more than 1 quarter.</figcaption></figure>"
        "<h2>Count by 5s and 10s</h2>"
        "<p>Count nickels by 5s. Count dimes by 10s. With both, start with the dimes.</p>"
        "<figure class='sn-fig'>" + money_svg(toks_of(("D", 2), ("N", 2)), gap=10, under=["10¢", "20¢", "25¢", "30¢"],
                                              label="counting on: 10¢, 20¢, 25¢, 30¢") +
        "<figcaption>Dimes: 10¢, 20¢. Nickels: 25¢, 30¢.</figcaption></figure>"
        + ex("Example", "How much are 4 nickels?", "Count by 5s: 5¢, 10¢, 15¢, 20¢.", "20¢")
        + ex("Example", "How much are a $20 bill and a $5 bill?", "$20, then count on 5: $25.", "$25")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The nickel is bigger, so it is worth more", "Look at the value. The small dime is 10¢. The nickel is 5¢"],
            ["4 nickels, so 4¢", "Count the value: 5¢, 10¢, 15¢, 20¢"],
            ["More coins is more money", "3 nickels (15¢) are less than 2 dimes (20¢)"],
            ["A toonie is $1", "A loonie is $1. A toonie is $2"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about money in Ontario?",
     "a": "In the Ontario math curriculum (Financial Literacy, F1.1), Grade 1 students name Canadian coins up to 50¢ and coins and bills up to $50, and compare their values."},
    {"q": "Why does my child think a nickel is worth more than a dime?",
     "a": "The nickel is bigger, so it looks like more. Put a dime and two nickels side by side and say “10¢ is the same as 5¢ and 5¢.” Size does not tell the value."},
    {"q": "How can I help my child learn Canadian coins at home?",
     "a": "Use real coins. Sort them, say each name and value, then count nickels by 5s and dimes by 10s. Let your child pay for something small at the store."},
    {"q": "Do Grade 1 students learn about pennies?",
     "a": "No. Canada stopped giving out pennies in 2013, so the nickel is the smallest value coin. Grade 1 uses the nickel, dime, quarter, loonie and toonie."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(41815)
    P = People(rnd)
    sets = [set_names(P, rnd), set_values(P, rnd), set_compare(P, rnd), set_count(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert set(it) == {"q", "c", "a", "e"}
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
        "country": "ca-on", "subject": "math", "grade": "grade-1", "slug": "money", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Money: Canadian Coins and Bills",
        "seo_title": "Grade 1 Money Worksheets: Canadian Coins and Bills with Answer Key (Ontario)",
        "short_title": "Money",
        "domain": "Financial Literacy",
        "standard_code": "Grade 1: F1.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Identify the various Canadian coins up to 50¢ and coins and bills up to $50, and compare their values",
        "meta_desc": "Free Grade 1 math worksheets on money for the Ontario curriculum: name the nickel, dime, quarter, loonie and toonie, know the $5, $10, $20 and $50 bills, compare values, and count nickels and dimes to 50¢. 100 questions with pictures and an answer key.",
        "key_big": "Look at the value, not the size of the coin.",
        "key_sub": "Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2. The small dime is worth more than the big nickel. Count nickels by 5s and dimes by 10s.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|A, B, C|counting|Canadian|compare)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
