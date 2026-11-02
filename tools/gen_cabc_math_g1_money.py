# -*- coding: utf-8 -*-
"""
BC Grade 1 Math: Coins and Money (BC Mathematics Curriculum, Grade 1: Financial literacy)
  python3 tools/gen_cabc_math_g1_money.py
Content standard: "Financial literacy – values of coins, and monetary exchanges".
Grade 1: name the coins (nickel, dime, quarter, loonie, toonie), know each value, compare values,
count small collections of one kind of coin (nickels by 5s, dimes by 10s, loonies by 1s, toonies by 2s),
and make simple trades and purchases (2 loonies = 1 toonie, 2 nickels = 1 dime).
Canadian coins: nickel 5¢, dime 10¢ (the smallest coin), quarter 25¢, loonie $1 (11 sides, gold colour),
toonie $2 (silver ring, gold centre). No pennies. Coins are simple labelled shapes (no real designs).
Very short sentences for 6-7 year olds, a picture in almost every question.
Wrong answers come from real mistakes: the small dime taken as worth less than the bigger nickel, counting
coins instead of their value, a quarter taken as 20¢, a toonie taken as $1, a loonie taken as 1¢, counting
nickels by 10s or dimes by 5s, missing or double-counting one coin, more coins taken as more money,
"1 coin for 1 coin" taken as a fair trade.
"A-D picture" questions build the picture after the answer position is chosen, so the choices stay A, B, C, D.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]

# ------------------------------------------------------------ coin facts
ORDER = ["T", "L", "Q", "D", "N"]   # biggest value first
VAL = {"T": 200, "L": 100, "Q": 25, "D": 10, "N": 5}
ONE = {"T": "toonie", "L": "loonie", "Q": "quarter", "D": "dime", "N": "nickel"}
MANY = {k: (v + "s") for k, v in ONE.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius in proportion to the real coins (mm): dime 18, nickel 21.2, quarter 23.9, loonie 26.5, toonie 28
COIN = {"D": (18, SILVER, 14), "N": (21, SILVER, 15), "Q": (24, SILVER, 15), "L": (26, GOLD, 16), "T": (28, SILVER, 16)}


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def C(v):
    assert isinstance(v, int) and 0 < v < 100, v
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
            if c <= 0 or (fmt is D and c % 100) or (fmt is C and c >= 100):
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
    r = COIN[t][0]
    return 2 * r, 2 * r


def polygon(cx, cy, r, n, rot=-90):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def draw_tok(t, cx, cy, hide=False):
    """one coin, labelled with its value (or '?' when hide)"""
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


def two_groups(left, right, capl, capr, label, arrow=False):
    """two piles of coins side by side, a line (or a trade arrow) between them, a caption under each"""
    gap, pad = 6, 6
    mid = 44 if arrow else 26

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
    if arrow:
        y = pad + hh / 2
        x1, x2 = pad + wl2 + 6, pad + wl2 + mid - 6
        b.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (x1 + 6, y, x2 - 6, y, GREEN))
        b.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x2, y, x2 - 9, y - 6, x2 - 9, y + 6, GREEN))
        b.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (x1, y, x1 + 9, y - 6, x1 + 9, y + 6, GREEN))
    else:
        b.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#9aa3ab' stroke-width='2' stroke-dasharray='4 4'/>"
                 % (lx, pad, lx, H - pad))
    return svg_wrap(int(math.ceil(W)), int(H), "".join(b), ("trade: " if arrow else "compare: ") + label)


def tag_svg(price, item):
    """a price tag: the price big, the item under it"""
    W = int(max(96, under_w(item) + 28))
    H = 66
    b = ("<path d='M 18 4 L %d 4 L %d 62 L 18 62 L 4 33 Z' fill='#fff7d6' stroke='#9a7a1c' stroke-width='2'/>"
         "<circle cx='17' cy='33' r='4' fill='none' stroke='#9a7a1c' stroke-width='2'/>" % (W - 4, W - 4))
    cx = (24 + W - 4) / 2
    b += text(cx, 32, price, 22) + text(cx, 53, item, 14, col=GREEN)
    return svg_wrap(W, H, b, "price tag: %s costs %s" % (item, price))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


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


def one_coin(t):
    w, h = tok_size(t)
    return svg_wrap(w + 8, h + 8, draw_tok(t, (w + 8) / 2, (h + 8) / 2), "one coin worth " + lab(VAL[t]))


# ============================================================ set 1: name the coin
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
        s(fig(one_coin(t)) + "What is this coin called?", right, wrong, e)
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
    s(fig(money_svg(["L", "T", "Q"], gap=12, label="a loonie, a toonie and a quarter"))
      + "Which coin has 11 sides?", "the loonie", ["the toonie", "the quarter", "the dime"],
      "The <b>loonie</b> has 11 sides. It is gold in colour.")
    s(fig(money_svg(["T", "L"], gap=14, label="a toonie and a loonie")) + "Which coin has a gold centre?",
      "the toonie", ["the loonie", "the quarter", "the nickel"],
      "The <b>toonie</b> has a silver ring and a gold centre. The loonie is all gold.")
    s(fig(money_svg(["N", "L", "D", "Q"], gap=12, label="a nickel, a loonie, a dime and a quarter"))
      + "Which coin is all gold in colour?",
      "the loonie", ["the toonie", "the quarter", "the nickel"],
      "The <b>loonie</b> is all gold in colour. The toonie is only gold in the centre.")
    s(fig(money_svg(["Q", "N", "D", "L"], gap=10, label="a quarter, a nickel, a dime and a loonie"))
      + "Which coin is the smallest?",
      "the dime", ["the nickel", "the quarter", "the loonie"],
      "The <b>dime</b> is the smallest coin. It is worth 10¢.")
    s(fig(money_svg(["D", "T", "Q", "N"], gap=10, label="a dime, a toonie, a quarter and a nickel"))
      + "Which coin is the biggest?",
      "the toonie", ["the quarter", "the nickel", "the dime"],
      "The <b>toonie</b> is the biggest coin. It is worth $2.")
    s(fig(one_coin("L")) + "What is the name of the $1 coin?", "loonie", ["toonie", "quarter", "dime"],
      "The $1 coin is the <b>loonie</b>. The $2 coin is the toonie.")
    s(fig(one_coin("T")) + "What is the name of the $2 coin?", "toonie", ["loonie", "quarter", "nickel"],
      "The $2 coin is the <b>toonie</b>. “Two” and “toonie” sound alike.")
    s(fig(one_coin("Q")) + "What is the name of the 25¢ coin?", "quarter", ["dime", "nickel", "loonie"],
      "The 25¢ coin is the <b>quarter</b>.")
    s(fig(one_coin("D")) + "What is the name of the 10¢ coin?", "dime", ["nickel", "quarter", "loonie"],
      "The 10¢ coin is the <b>dime</b>. The nickel is bigger, but it is only 5¢.")
    s(fig(one_coin("N")) + "What is the name of the 5¢ coin?", "nickel", ["dime", "quarter", "toonie"],
      "The 5¢ coin is the <b>nickel</b>.")
    assert len(its) == 20
    return {"title": "Name the coin", "items": its}


# ============================================================ set 2: what each coin is worth
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
    s(hid("D") + "How do we write the value of a dime?", "10¢", ["$10", "1¢", "100¢"],
      "A dime is ten cents. We write <b>10¢</b>. $10 is ten dollars, much more.")
    s(hid("Q") + "How do we write the value of a quarter?", "25¢", ["$25", "52¢", "20¢"],
      "A quarter is twenty-five cents. Cents use the ¢ sign after the number: <b>25¢</b>.")
    s(hid("L") + "How do we write the value of a loonie?", "$1", ["1¢", "$10", "11¢"],
      "A loonie is one dollar. Dollars use the $ sign in front: <b>$1</b>. 1¢ is only one cent.")
    s(hid("T") + "How do we write the value of a toonie?", "$2", ["2¢", "$20", "20¢"],
      "A toonie is two dollars. We write <b>$2</b>. 2¢ is two cents, much less.")
    s(fig(money_svg(["N", "D"], gap=14, under=["nickel", "dime"], hide=True, label="a nickel and a smaller dime, values hidden"))
      + "The dime is small. How much is it worth?", 10, [5, 1, 2],
      "Size does not tell the value. The small dime is worth <b>10¢</b>. The bigger nickel is 5¢.", C)
    s(fig(money_svg(["Q", "N"], gap=14, under=["quarter", "nickel"], hide=True, label="a quarter and a nickel, values hidden"))
      + "Which coin is worth 25¢?", "the quarter", ["the nickel", "both coins", "neither coin"],
      "The <b>quarter</b> is worth 25¢. The nickel is worth 5¢.")
    s(fig(money_svg(["D", "N", "Q", "L"], gap=10, under=["dime", "nickel", "quarter", "loonie"], hide=True,
                    label="a dime, a nickel, a quarter and a loonie, values hidden"))
      + "Which coin is worth less than a dime?", "the nickel", ["the quarter", "the loonie", "none of them"],
      "A dime is 10¢. The <b>nickel</b> is 5¢. 5¢ is less than 10¢.")
    s(fig(money_svg(["Q", "D", "N", "T"], gap=10, under=["quarter", "dime", "nickel", "toonie"], hide=True,
                    label="a quarter, a dime, a nickel and a toonie, values hidden"))
      + "Which coin is worth more than a loonie?", "the toonie", ["the quarter", "the dime", "the nickel"],
      "A loonie is $1. The <b>toonie</b> is $2. $2 is more than $1.")
    s(fig(money_svg(["N", "D", "L", "T"], gap=10, under=["nickel", "dime", "loonie", "toonie"], hide=True,
                    label="a nickel, a dime, a loonie and a toonie, values hidden"))
      + "Which two coins are worth dollars?", "loonie and toonie", ["nickel and dime", "dime and loonie", "nickel and toonie"],
      "The <b>loonie</b> is $1 and the <b>toonie</b> is $2. The nickel and dime are worth cents.")
    s(fig(money_svg(["N", "D", "Q"], gap=12, under=["nickel", "dime", "quarter"], hide=True,
                    label="a nickel, a dime and a quarter, values hidden"))
      + "Which list goes from least to most?",
      "nickel, dime, quarter", ["dime, nickel, quarter", "quarter, dime, nickel", "nickel, quarter, dime"],
      "Nickel 5¢, dime 10¢, quarter 25¢. So <b>nickel, dime, quarter</b>. Do not order by size.")
    assert len(its) == 20
    return {"title": "What is each coin worth?", "items": its}


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
    pair("D", "N", more=False)
    pair("Q", "N", more=False)
    pair("L", "D", more=False)
    pair("T", "Q", more=False)
    pair("N", "L")
    pair("T", "D", more=False)

    def most(toks, more=True):
        word = "most" if more else "least"
        best = max(toks, key=VAL.get) if more else min(toks, key=VAL.get)
        others = [x for x in toks if x != best]
        q = fig(money_svg(toks, gap=10, per_row=4, under=[ONE[t] for t in toks], label="money: " + ", ".join(ONE[t] for t in toks))) \
            + "Which is worth the %s?" % word
        e = cap(", ".join("%s %s" % (ONE[t], lab(VAL[t])) for t in srt(toks))) + ". The <b>%s</b> is worth the %s." % (ONE[best], word)
        its.append(mcq(q, "the " + ONE[best], ["the " + ONE[x] for x in others], e))

    most(["Q", "D", "L", "N"])
    most(["D", "N", "Q", "T"], more=False)
    most(["L", "Q", "T", "D"], more=False)

    def groups(a, b, ca, cb):
        ta, tb = total(a), total(b)
        q = fig(two_groups(a, b, ca, cb, "%s and %s" % (ca, cb))) + "Which side is worth more?"
        na = "the " + (ONE[a[0]] if len(a) == 1 else ca)
        nb = "the " + (ONE[b[0]] if len(b) == 1 else cb)
        e = "%s: %s. %s: %s. " % (cap(ca), lab(ta), cap(cb), lab(tb))
        if ta == tb:
            right, wrong = SAME, [na, nb, CANT]
            e += "<b>They are worth the same.</b>"
        else:
            hi, lo = (na, nb) if ta > tb else (nb, na)
            right, wrong = hi, [lo, SAME, CANT]
            are = "are" if len(a if ta > tb else b) > 1 else "is"
            e += "So <b>%s</b> %s worth more." % (right, are)
            more_side = na if len(a) > len(b) else nb
            if len(a) != len(b) and right != more_side:
                e += " More coins is not always more money."
        its.append(mcq(q, right, wrong, e))

    groups(["N", "N"], ["D"], "2 nickels", "1 dime")
    groups(["N"] * 3, ["D"], "3 nickels", "1 dime")
    groups(["D", "D", "D"], ["Q"], "3 dimes", "1 quarter")
    groups(["Q"], ["N"] * 4, "1 quarter", "4 nickels")
    groups(["L"] * 3, ["T"], "3 loonies", "1 toonie")
    groups(["D"] * 4, ["L"], "4 dimes", "1 loonie")
    groups(["T"], ["L", "L"], "1 toonie", "2 loonies")
    assert len(its) == 20
    return {"title": "Which is worth more?", "items": its}


# ============================================================ set 4: count nickels by 5s and dimes by 10s
def set_count(P, rnd):
    its = []
    groups = [("N", 2), ("D", 2), ("N", 3), ("D", 3), ("L", 3), ("T", 2), ("N", 4), ("D", 4), ("L", 4),
              ("T", 3), ("N", 5), ("D", 5), ("L", 5), ("T", 4), ("N", 6)]
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "What is the total?", "%s finds these coins in %s pocket. How much is it?",
             "%s puts these coins in a piggy bank. How much is in it?"]
    step = {"N": "5s", "D": "10s", "L": "1s", "T": "2s"}
    for i, (t, n) in enumerate(groups):
        toks = [t] * n
        T = total(toks)
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if i < 2:
            st = "Count by %s. How much money is this?" % step[t]
        if st.count("%s") == 2:
            st = st % (nm, his if "pocket" in st else he)
        elif "%s" in st:
            st = st % nm
        q = fig(money_svg(toks)) + st
        e = count_on(toks, C if T < 100 else D)
        notes = []
        if t in "ND":
            other = 10 if t == "N" else 5          # counting by the wrong step
            cands = [n, n * other, T - VAL[t], T + VAL[t]]
            it = mcq(q, T, cands, e, C)
            if C(n) in it["c"]:
                notes.append("%s counts the coins, not the cents." % C(n))
            if C(n * other) in it["c"]:
                notes.append("%s counts %s by %ds." % (C(n * other), MANY[t], other))
        elif t == "L":
            cands = ["%d¢" % n, 200 * n, T - 100, T + 100]
            it = mcq(q, T, cands, e, D)
            if "%d¢" % n in it["c"]:
                notes.append("A loonie is $1, not 1¢.")
            if D(200 * n) in it["c"]:
                notes.append("%s counts by 2s, like toonies." % D(200 * n))
        else:
            cands = [100 * n, T - 200, T + 200, "%d¢" % (2 * n)]
            it = mcq(q, T, cands, e, D)
            if D(100 * n) in it["c"]:
                notes.append("%s counts the coins. A toonie is $2, not $1." % D(100 * n))
        if notes:
            it["e"] += " " + " ".join(notes)
        its.append(it)

    its.append(mcq(fig(money_svg(["N"] * 4, under=["5¢", "10¢", "15¢", "?"], label="counting nickels: 5¢, 10¢, 15¢, ?"))
                   + "Count the nickels by 5s. What is the next number?", 20, [16, 25, 30],
                   "Count by 5s: 5¢, 10¢, 15¢, <b>20¢</b>. 16¢ counts by 1s.", C))
    its.append(mcq(fig(money_svg(["D"] * 4, under=["10¢", "20¢", "30¢", "?"], label="counting dimes: 10¢, 20¢, 30¢, ?"))
                   + "Count the dimes by 10s. What is the next number?", 40, [31, 35, 50],
                   "Count by 10s: 10¢, 20¢, 30¢, <b>40¢</b>. 35¢ counts by 5s.", C))
    its.append(mcq(fig(money_svg(["T"] * 4, under=["$2", "$4", "$6", "?"], label="counting toonies: $2, $4, $6, ?"))
                   + "Count the toonies by 2s. What is the next number?", "$8", ["$7", "$10", "$4"],
                   "Count by 2s: $2, $4, $6, <b>$8</b>. $7 counts by 1s."))
    nm, he, his = P.next()
    its.append(mcq(fig(tag_svg("20¢", "eraser")) + "An eraser costs 20¢. How many nickels make 20¢?",
                   "4", ["20", "2", "5"],
                   "Count by 5s: 5¢, 10¢, 15¢, 20¢. That is <b>4</b> nickels. 2 would be dimes."))
    its.append(mcq(fig(tag_svg("40¢", "pencil")) + "A pencil costs 40¢. How many dimes make 40¢?",
                   "4", ["40", "8", "3"],
                   "Count by 10s: 10¢, 20¢, 30¢, 40¢. That is <b>4</b> dimes. 8 would be nickels."))
    assert len(its) == 20
    return {"title": "Count by 5s, 10s, 1s and 2s", "items": its}


# ============================================================ set 5: trading and buying (word problems)
def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=str):
        its.append(mcq(q, right, cands, e, fmt))

    nm, he, his = P.next()
    add(fig(money_svg(["L", "L"], gap=12, label="2 loonies")) + "%s trades 2 loonies for 1 coin. It is worth the same. Which coin?" % nm,
        "a toonie", ["a loonie", "a quarter", "a dime"],
        "$1 + $1 = $2. One <b>toonie</b> is $2. 2 loonies = 1 toonie.")
    nm, he, his = P.next()
    add(fig(one_coin("D")) + "%s trades 1 dime for nickels. How many nickels does %s get?" % (nm, he),
        "2", ["1", "5", "10"],
        "A dime is 10¢. Nickels: 5¢, 10¢. That is <b>2</b> nickels. 1 nickel is only 5¢.")
    nm, he, his = P.next()
    add(fig(one_coin("T")) + "%s trades 1 toonie for loonies. How many loonies does %s get?" % (nm, he),
        "2", ["1", "4", "20"],
        "A toonie is $2. Loonies: $1, $2. That is <b>2</b> loonies. 1 loonie is only $1.")
    add(fig(money_svg(["N"] * 5, label="5 nickels")) + "5 nickels are worth the same as 1 ____.",
        "quarter", ["dime", "loonie", "nickel"],
        "Count by 5s: 5¢, 10¢, 15¢, 20¢, 25¢. 25¢ is 1 <b>quarter</b>.")
    nm, he, his = P.next()
    add(fig(money_svg(["T", "T"], gap=12, label="2 toonies")) + "%s trades 2 toonies for loonies. How many loonies?" % nm,
        "4", ["2", "3", "1"],
        "2 toonies: $2, $4. Loonies: $1, $2, $3, $4. That is <b>4</b> loonies. 2 loonies is only $2.")
    nm, he, his = P.next()
    add(fig(two_groups(["N", "N"], ["D"], "2 nickels", "1 dime", "%s gives 2 nickels and gets 1 dime" % nm, arrow=True))
        + "%s trades 2 nickels for 1 dime. Is it fair?" % nm,
        "Yes, both are 10¢.", ["No, the dime is smaller.", "No, 2 coins is more.", "No, 2 nickels are 2¢."],
        "5¢ + 5¢ = 10¢. A dime is 10¢. <b>Yes, it is fair.</b> Size and number of coins do not tell the value.")
    nm, he, his = P.next()
    add(fig(two_groups(["N"], ["D"], "1 nickel", "1 dime", "%s gives 1 nickel and gets 1 dime" % nm, arrow=True))
        + "%s trades 1 nickel for 1 dime. Is it fair?" % nm,
        "No, 10¢ is more than 5¢.", ["Yes, it is 1 coin for 1 coin.", "Yes, the nickel is bigger.", "No, the nickel is worth more."],
        "A nickel is 5¢. A dime is 10¢. <b>No, it is not fair.</b> 1 coin for 1 coin is not always the same value.")
    its.append(abcd("A pencil at the school store costs 10¢. Which coin pays exactly?", "D", ["N", "Q", "L"],
                    "A dime is 10¢. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("A sticker costs 5¢. Which coin pays exactly?", "N", ["D", "Q", "T"],
                    "A nickel is 5¢. It is <b>%s</b>. The dime is smaller, but it is 10¢.", hide=True, names=True))
    its.append(abcd("A cookie at the bake sale costs 25¢. Which coin pays exactly?", "Q", ["N", "D", "L"],
                    "A quarter is 25¢. It is <b>%s</b>.", hide=True, names=True))
    its.append(abcd("A juice box costs $2. Which coin pays exactly?", "T", ["L", "Q", "D"],
                    "A toonie is $2. It is <b>%s</b>. A loonie is only $1.", hide=True, names=True))
    its.append(abcd("A peach at the Kelowna farmers' market costs $1. Which coin pays exactly?", "L", ["T", "Q", "N"],
                    "A loonie is $1. It is <b>%s</b>.", hide=True, names=True))
    nm, he, his = P.next()
    add(fig(money_svg(["T", "L"], label="a toonie and a loonie"))
        + "Hot chocolate costs $3. %s has these coins. Is it enough?" % nm,
        "Yes, %s has $3." % he, ["No, %s has $2." % he, "No, %s has 2¢." % he, "Yes, %s has $4." % he],
        "Toonie $2, loonie $1: $2, $3. %s has $3, so <b>yes</b>. $2 comes from counting the toonie as $1." % nm)
    nm, he, his = P.next()
    add(fig(one_coin("L")) + "A granola bar costs $2. %s has 1 loonie. Is it enough?" % nm,
        "No, %s needs $1 more." % he, ["Yes, a loonie is $2.", "Yes, %s has 1 coin." % he, "No, %s needs $2 more." % he],
        "A loonie is $1. The bar is $2. $1 + $1 = $2, so <b>%s needs $1 more</b>." % he)
    nm, he, his = P.next()
    add(fig(money_svg(["L"] * 3, label="3 loonies")) + "%s has 3 loonies. %s buys a $2 freezie. How much is left?" % (nm, cap(he)),
        "$1", ["$5", "$3", "$2"],
        "3 loonies are $3. Take away $2: $3 − $2 = <b>$1</b>. $5 adds instead of taking away.")
    nm, he, his = P.next()
    add(fig(money_svg(["T"] * 3, label="3 toonies")) + "For the Terry Fox Run, %s gives 3 toonies. How much is that?" % nm,
        "$6", ["$3", "$5", "$8"],
        "Count by 2s: $2, $4, $6. That is <b>$6</b>. $3 counts each toonie as $1.")
    nm, he, his = P.next()
    add(fig(money_svg(["D"] * 4, label="4 dimes")) + "%s has 4 dimes. %s buys a 10¢ pencil. How much is left?" % (nm, cap(he)),
        30, [50, 3, 40],
        "4 dimes: 10¢, 20¢, 30¢, 40¢. Take away 10¢: 40¢ − 10¢ = <b>30¢</b>. 50¢ adds a dime instead.", C)
    nm, he, his = P.next()
    add(fig(tag_svg("15¢", "sticker")) + "%s pays for this sticker with nickels. How many nickels?" % nm,
        "3", ["15", "2", "5"],
        "Count by 5s: 5¢, 10¢, 15¢. That is <b>3</b> nickels. 15 counts the cents, not the coins.")
    nm, he, his = P.next()
    add(fig(tag_svg("20¢", "bookmark")) + "%s pays for this bookmark with dimes. How many dimes?" % nm,
        "2", ["20", "4", "1"],
        "Count by 10s: 10¢, 20¢. That is <b>2</b> dimes. 4 would be nickels.")
    nm1, _, _ = P.next()
    nm2, _, _ = P.next()
    add(fig(two_groups(["D", "D"], ["N"] * 3, nm1, nm2, "%s has 2 dimes. %s has 3 nickels." % (nm1, nm2)))
        + "Who has more money?", nm1, [nm2, "They have the same.", "You cannot tell."],
        "%s has 10¢, 20¢. %s has 5¢, 10¢, 15¢. 20¢ is more, so <b>%s</b> has more. More coins is not always more money."
        % (nm1, nm2, nm1))
    assert len(its) == 20
    return {"title": "Trade and buy (word problems)", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
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
        "<h2>Which is worth more?</h2>"
        "<p>Look at the value, not the size. 10¢ is more than 5¢, so a dime is worth more than a nickel.</p>"
        "<figure class='sn-fig'>" + two_groups(["D", "D", "D"], ["Q"], "3 dimes: 30¢", "1 quarter: 25¢",
                                               "3 dimes make 30¢, 1 quarter is 25¢") +
        "<figcaption>3 dimes are worth more than 1 quarter.</figcaption></figure>"
        "<h2>Count by 5s and 10s</h2>"
        "<p>Count nickels by 5s. Count dimes by 10s. Count loonies by 1s and toonies by 2s.</p>"
        "<figure class='sn-fig'>" + money_svg(["N"] * 4, gap=10, under=["5¢", "10¢", "15¢", "20¢"],
                                              label="counting nickels: 5¢, 10¢, 15¢, 20¢") +
        "<figcaption>4 nickels: 5¢, 10¢, 15¢, 20¢.</figcaption></figure>"
        + ex("Example", "How much are 3 dimes?", "Count by 10s: 10¢, 20¢, 30¢.", "30¢")
        + "<h2>Trade coins</h2>"
        "<p>A fair trade gives the same value. 2 loonies are $2, so they trade for 1 toonie.</p>"
        "<figure class='sn-fig'>" + two_groups(["L", "L"], ["T"], "2 loonies: $2", "1 toonie: $2",
                                               "2 loonies for 1 toonie", arrow=True) +
        "<figcaption>2 loonies = 1 toonie. 2 nickels = 1 dime.</figcaption></figure>"
        + ex("Example", "A sticker costs 15¢. How many nickels pay for it?", "Count by 5s: 5¢, 10¢, 15¢.", "3 nickels")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["The dime is small, so it is worth less", "Look at the value. The small dime is 10¢. The nickel is 5¢"],
            ["4 nickels, so 4¢", "Count the value: 5¢, 10¢, 15¢, 20¢"],
            ["More coins is more money", "3 nickels (15¢) are less than 2 dimes (20¢)"],
            ["A toonie is $1", "A loonie is $1. A toonie is $2"],
        ])
    )


FAQ = [
    {"q": "What do Grade 1 students learn about money in BC?",
     "a": "The BC Grade 1 math curriculum includes financial literacy: the values of coins and simple monetary exchanges. Students name the nickel, dime, quarter, loonie and toonie, count coins of one kind, and make trades such as 2 loonies for 1 toonie."},
    {"q": "Why does my child think a nickel is worth more than a dime?",
     "a": "The nickel is bigger, so it looks like more. Put a dime next to two nickels and say “10¢ is the same as 5¢ and 5¢.” Size does not tell the value."},
    {"q": "How can I help my child learn Canadian coins at home?",
     "a": "Use real coins. Sort them, say each name and value, then count nickels by 5s and dimes by 10s. Play store and trade coins, like 2 loonies for a toonie."},
    {"q": "Do Grade 1 students learn about pennies?",
     "a": "No. Canada stopped giving out pennies in 2013, so the nickel is the coin with the least value. Grade 1 uses the nickel, dime, quarter, loonie and toonie."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(51811)
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
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-1", "slug": "coins-and-money", "sort": 11,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 1 Coins and Money",
        "seo_title": "Grade 1 Coins and Money Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Coins and money",
        "domain": "Financial literacy",
        "standard_code": "Grade 1: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/1/core",
        "standard_text": "Financial literacy – values of coins, and monetary exchanges",
        "meta_desc": "Free Grade 1 math worksheets on Canadian coins for the BC curriculum: name the nickel, dime, quarter, loonie and toonie, learn what each coin is worth, compare values, count nickels by 5s and dimes by 10s, and trade 2 loonies for a toonie. 100 questions with pictures and an answer key.",
        "key_big": "Look at the value, not the size of the coin.",
        "key_sub": "Nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2. The small dime is worth more than the big nickel. A fair trade has the same value: 2 loonies = 1 toonie.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|A, B, C|counting|Canadian|compare|trade)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
