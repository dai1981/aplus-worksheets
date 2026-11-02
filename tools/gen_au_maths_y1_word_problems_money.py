# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Word Problems and Money (Australian Curriculum v9.0, AC9M1N05)
  python3 tools/gen_au_maths_y1_word_problems_money.py
Year 1: adding and taking away within 20, "how many more", Australian coins, counting small
amounts and simple buying. Very short sentences for 6-7 year olds, a picture in almost every question.
Money is kept in one unit: cents up to 100c (written 45c; 100c is written $1) or whole dollars up to $10.
Australian coins: 5c, 10c, 20c, 50c (12-sided, the biggest), $1, $2 (gold; the $2 coin is smaller
than the $1 coin). No 1c or 2c coins. Coins are simple labelled shapes (no real designs).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"
LETTERS = ["A", "B", "C", "D"]
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]

# object colours
C = dict(red="#d9443a", blue="#3b7dd8", green="#3fa34d", yellow="#f2c230", orange="#f08a24",
         purple="#8e5bc7", gold="#e8b21c", pink="#e86aa6", brown="#c68a4a")

# ------------------------------------------------------------ money facts
ORDER = ["N10", "N5", "C200", "C100", "C50", "C20", "C10", "C5"]   # biggest value first
VAL = {"N10": 1000, "N5": 500, "C200": 200, "C100": 100, "C50": 50, "C20": 20, "C10": 10, "C5": 5}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius (in proportion to the real coins: 50c the biggest, $2 smaller than $1), colours, label size
COIN = {"C5": (16, SILVER, 14), "C10": (19, SILVER, 14), "C20": (23, SILVER, 15), "C50": (25, SILVER, 15),
        "C100": (20, GOLD, 15), "C200": (17, GOLD, 14)}
NOTE = {"N5": ("#efcfe3", "#8a3a6e"), "N10": ("#c4dcf2", "#1f5f99")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    return "$%d" % (v // 100) if v >= 100 else "%dc" % v


def m(c):
    """45 -> '45c', 100 -> '$1', 700 -> '$7' (never dollars and cents together)"""
    assert c > 0, c
    if c < 100:
        return "%dc" % c
    assert c % 100 == 0 and c <= 2000, c
    return "$%d" % (c // 100)


def mval(s):
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


def coin_list(vals):
    """[20, 20, 10] -> '20c, 20c and 10c'"""
    ls = [lab(v) for v in vals]
    return ls[0] if len(ls) == 1 else ", ".join(ls[:-1]) + " and " + ls[-1]


# ------------------------------------------------------------ typical coin-counting mistakes (cents)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


def m_dollar_as_c(toks):
    """read $2 as 2c"""
    return sum(VAL[t] // 100 if VAL[t] >= 100 else VAL[t] for t in toks)


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


# ------------------------------------------------------------ choices
def pick3(correct, cands, ok):
    seen_t, seen_v = {correct}, {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if not isinstance(c, str):
            c = ok(c)
            if c is None:
                continue
        if c in ("1c", "2c"):
            continue      # no 1c or 2c coins: never offer them
        v = mval(c)
        if c in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(c)
        if v is not None:
            seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (correct, cands)
    return pick


def mcq_n(q, correct, cands, e):
    """number choices (no units): wrong numbers below 1 are dropped"""
    pick = pick3(str(correct), cands, lambda v: str(v) if v >= 1 else None)
    return {"q": q, "c": [str(correct)] + pick, "a": 0, "e": e}


def ok_money(c):
    if c <= 0 or (c > 100 and c % 100) or c > 2000:
        return None
    return m(c)


def mcq_m(q, correct, cands, e):
    """money choices: ints are cents"""
    corr = m(correct) if isinstance(correct, int) else correct
    pick = pick3(corr, cands, ok_money)
    return {"q": q, "c": [corr] + pick, "a": 0, "e": e}


def mcq_t(q, correct, wrongs, e):
    """text choices, given in full"""
    assert len(wrongs) == 3 and correct not in wrongs and len(set(wrongs)) == 3
    return {"q": q, "c": [correct] + list(wrongs), "a": 0, "e": e}


def letter_q(stem, right, others, e):
    """A-D picture question: built in balance() so the right coin lands on the chosen letter.
    e may use {L} for the letter of the answer."""
    assert len(others) == 3 and right not in others
    return {"_lt": (stem, right, list(others), e)}


def build_letter(it, t, rnd):
    stem, right, others, e = it.pop("_lt")
    o = list(others)
    rnd.shuffle(o)
    arr = o[:t] + [right] + o[t:]
    svg = money_svg(arr, gap=16, under=LETTERS, label="pictures A to D: " + ", ".join(
        "%s %s" % (L, lab(VAL[x])) for L, x in zip(LETTERS, arr)))
    it.update({"q": fig(svg) + stem, "c": list(LETTERS), "a": t, "e": e.format(L=LETTERS[t])})


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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
        self.rnd = rnd
        self.pool = [(n, "she", "her", "her") for n in GIRLS] + [(n, "he", "his", "him") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def one(self):
        n, he, his, him = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(N=n, he=he, He=cap(he), his=his, His=cap(his), him=him)

    def two(self):
        a, b = self.rnd.sample(self.pool, 2)
        return a[0], b[0]


def say(t, p, **k):
    d = dict(p)
    d.update(k)
    return t.format(**d)


# ------------------------------------------------------------ SVG helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """approximate width of bold Arial text"""
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


# ------------------------------------------------------------ objects (each fits in a 28 x 28 cell)
PITCH = 28
DEF_COL = dict(apple="red", star="gold", fish="orange", ball="blue", flower="pink", block="green",
               biscuit="brown", balloon="red", car="blue", duck="yellow")
WORD = dict(apple=("apple", "apples"), star=("sticker", "stickers"), fish=("fish", "fish"), ball=("ball", "balls"),
            flower=("flower", "flowers"), block=("block", "blocks"), biscuit=("biscuit", "biscuits"),
            balloon=("balloon", "balloons"), car=("car", "cars"), duck=("duck", "ducks"))


def plural(n, kind):
    return WORD[kind][0 if n == 1 else 1]


def obj(kind, cx, cy, col=None):
    col = C[col or DEF_COL[kind]]
    s = "<g data-o='1'>"
    if kind == "apple":
        s += ("<path d='M%.1f %.1f q1 -4 3 -5' fill='none' stroke='#7a4a1e' stroke-width='2'/>" % (cx, cy - 7)
              + "<ellipse cx='%.1f' cy='%.1f' rx='4' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
              % (cx + 5, cy - 10, C["green"], cx + 5, cy - 10)
              + "<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy + 1, col, INK))
    elif kind == "star":
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 4.6
            a = math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy - r * math.sin(a) + 1))
        s += "<polygon points='%s' fill='%s' stroke='%s' stroke-width='1.2'/>" % (" ".join(pts), col, INK)
    elif kind == "fish":
        s += ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx + 3, cy, cx + 11, cy - 6.5, cx + 11, cy + 6.5, col, INK)
              + "<ellipse cx='%.1f' cy='%.1f' rx='8' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 3, cy, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx - 7, cy - 1.5, INK))
    elif kind == "ball":
        s += ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
              + "<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.8'/>"
              % (cx - 9, cy - 2, cx, cy + 5, cx + 9, cy - 2))
    elif kind == "flower":
        for k in range(5):
            a = -math.pi / 2 + k * 2 * math.pi / 5
            s += "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='0.8'/>" % (
                cx + 5.6 * math.cos(a), cy + 5.6 * math.sin(a), col, INK)
        s += "<circle cx='%.1f' cy='%.1f' r='3.4' fill='%s' stroke='%s' stroke-width='0.8'/>" % (
            cx, cy, C["orange"] if col == C["yellow"] else C["yellow"], INK)
    elif kind == "block":
        s += ("<rect x='%.1f' y='%.1f' width='19' height='19' rx='3' fill='%s' stroke='%s' stroke-width='1.4'/>"
              % (cx - 9.5, cy - 9.5, col, INK))
    elif kind == "biscuit":
        s += "<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy, col, INK)
        for dx, dy in [(-4, -3), (3, -4), (0, 3), (5, 3), (-4, 4)]:
            s += "<circle cx='%.1f' cy='%.1f' r='1.3' fill='#8a5a2a'/>" % (cx + dx, cy + dy)
    elif kind == "balloon":
        s += ("<path d='M%.1f %.1f q-2 4 1 7' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy + 6, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (cx, cy + 4, cx - 2, cy + 7, cx + 2, cy + 7, col)
              + "<ellipse cx='%.1f' cy='%.1f' rx='7' ry='8.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx, cy - 3, col, INK))
    elif kind == "car":
        s += ("<rect x='%.1f' y='%.1f' width='10' height='6' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 5, cy - 7, col, INK)
              + "<rect x='%.1f' y='%.1f' width='21' height='8' rx='2' fill='%s' stroke='%s' stroke-width='1.2'/>"
              % (cx - 10.5, cy - 2, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx - 6, cy + 6.5, INK)
              + "<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (cx + 6, cy + 6.5, INK))
    elif kind == "duck":
        s += ("<ellipse cx='%.1f' cy='%.1f' rx='9' ry='6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx + 2, cy + 4, col, INK)
              + "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='0.8'/>"
              % (cx - 7.5, cy - 6, cx - 11.5, cy - 4.5, cx - 7.5, cy - 3, C["orange"], INK)
              + "<circle cx='%.1f' cy='%.1f' r='4.6' fill='%s' stroke='%s' stroke-width='1.2'/>" % (cx - 4, cy - 5, col, INK)
              + "<circle cx='%.1f' cy='%.1f' r='1.1' fill='%s'/>" % (cx - 4.5, cy - 6, INK))
    else:
        raise ValueError(kind)
    return s + "</g>"


def cross(cx, cy):
    return ("<g data-x='1'><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.6' stroke-linecap='round'/></g>"
            % (cx - 10, cy - 10, cx + 10, cy + 10, RED, cx - 10, cy + 10, cx + 10, cy - 10, RED))


def group_body(x0, y0, n, kind, col=None, cols=5, gap5=0):
    """n objects in rows of `cols`; an extra gap after every 5 in a row (like a ten-frame)."""
    s, centers = [], []
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * PITCH + PITCH / 2 + gap5 * (c // 5)
        cy = y0 + r * PITCH + PITCH / 2
        centers.append((cx, cy))
        s.append(obj(kind, cx, cy, col))
    ncol = min(n, cols)
    w = ncol * PITCH + gap5 * ((ncol - 1) // 5)
    h = ((n + cols - 1) // cols) * PITCH
    return "".join(s), w, h, centers


def join_svg(a, b, kind):
    """add to: a objects, then b more inside a dashed box"""
    o, gap = 6, 26
    b1, w1, h1, _ = group_body(o, o + 4, a, kind)
    b2, w2, h2, _ = group_body(o + w1 + gap + 6, o + 4, b, kind)
    box = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='8' fill='none' stroke='%s' stroke-width='1.6' "
           "stroke-dasharray='5 3'/>" % (o + w1 + gap, o, w2 + 12, h2 + 8, GREEN))
    plus = text(o + w1 + gap / 2, o + 4 + PITCH / 2 + 7, "+", 20, col=GREEN)
    W, H = o + w1 + gap + w2 + 12 + o, o + max(h1 + 4, h2 + 8) + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + plus + box + b2,
                   "picture: %d %s and %d more" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def take_svg(a, b, kind):
    """take away: a objects in rows of 10; the last b are crossed out"""
    o = 6
    body, w, h, cen = group_body(o, o, a, kind, cols=10, gap5=8)
    xs = "".join(cross(cx, cy) for cx, cy in cen[a - b:])
    svg = svg_wrap(int(w + 2 * o + 0.99), int(h + 2 * o + 0.99), body + xs,
                   "picture: %d %s, %d crossed out" % (a, plural(a, kind), b))
    assert svg.count("<g data-o='1'>") == a and svg.count("<g data-x='1'>") == b
    return svg


def two_colour_svg(a, b, kind, c1, c2):
    """put together: a of one colour and b of another, side by side"""
    o, gap = 6, 22
    b1, w1, h1, _ = group_body(o, o, a, kind, c1)
    b2, w2, h2, _ = group_body(o + w1 + gap, o, b, kind, c2)
    W, H = o + w1 + gap + w2 + o, o + max(h1, h2) + o
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), b1 + b2,
                   "picture: %d %s %s and %d %s %s" % (a, c1, plural(a, kind), b, c2, plural(b, kind)))
    assert svg.count("<g data-o='1'>") == a + b
    return svg


def rows_svg(n1, n2, name1, name2, kind, lines=False):
    """compare: two rows lined up one under the other, names at the left"""
    fs = 16
    lw = max(tw(name1, fs), tw(name2, fs))
    x0 = 8 + lw + 10
    gap5 = 0 if lines else 6
    s = [text(x0 - 10, 6 + PITCH / 2 + 6, name1, fs, anchor="end"),
         text(x0 - 10, 6 + PITCH + 10 + PITCH / 2 + 6, name2, fs, anchor="end")]
    b1, w1, _, c1 = group_body(x0, 6, n1, kind, cols=20, gap5=gap5)
    b2, w2, _, c2 = group_body(x0, 6 + PITCH + 10, n2, kind, cols=20, gap5=gap5)
    if lines:
        for (xa, ya), (xb, yb) in zip(c1, c2):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5' stroke-dasharray='3 2'/>"
                     % (xa, ya + 11, xb, yb - 11, GREEN))
    W = x0 + max(w1, w2) + 8
    H = 6 + 2 * PITCH + 10 + 6
    svg = svg_wrap(int(W + 0.99), int(H + 0.99), "".join(s) + b1 + b2,
                   "picture: %s %d %s in a row, %s %d %s in a row" % (name1, n1, plural(n1, kind), name2, n2, plural(n2, kind)))
    assert svg.count("<g data-o='1'>") == n1 + n2
    return svg


def need_svg(have, want, kind):
    """a chart with `want` spaces in rows of 5; `have` spaces are filled, the rest are empty circles"""
    o = 6
    body, w, h, cen = group_body(o, o, have, kind, cols=5)
    s = [body]
    for i in range(have, want):
        r, c = divmod(i, 5)
        s.append("<circle cx='%.1f' cy='%.1f' r='10' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='4 3'/>"
                 % (o + c * PITCH + PITCH / 2, o + r * PITCH + PITCH / 2, GREEN))
    W = o + 5 * PITCH + o
    H = o + ((want + 4) // 5) * PITCH + o
    svg = svg_wrap(W, H, "".join(s), "picture: %d spaces, %d %s filled" % (want, have, plural(have, kind)))
    assert svg.count("<g data-o='1'>") == have
    return svg


# ------------------------------------------------------------ money pictures
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
    for r, rh in zip(rows, heights):
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
    w, h = tok_size(t)
    kind = "note" if t.startswith("N") else "coin"
    return svg_wrap(w + 12, h + 12, draw_tok(t, w / 2 + 6, h / 2 + 6), "one %s" % kind)


def tag_w(name):
    return max(int(tw(name, 15)) + 24, 78)


def draw_tag(x, y, name, price, h=62):
    w = tag_w(name)
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
            % (x, y, w, h, INK) + text(x + w / 2, y + 24, name, 15) + text(x + w / 2, y + 50, m(price), 18, col=GREEN))


def price_svg(items, title):
    """a row of price tags: [('apple', 50), ...]"""
    gap, pad, h = 10, 6, 62
    ws = [tag_w(n) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append(draw_tag(x, pad, n, p))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, m(p)) for n, p in items))


def has_svg(name, price, toks):
    """a price tag, then the coins someone has"""
    pad, gap, h = 6, 18, 62
    tw_ = tag_w(name)
    cw = [tok_size(t)[0] for t in toks]
    ch = max(tok_size(t)[1] for t in toks)
    lw = 44
    W = pad + tw_ + gap + lw + sum(cw) + 8 * (len(toks) - 1) + pad
    H = max(h, ch) + 2 * pad
    cy = H / 2
    b = [draw_tag(pad, cy - h / 2, name, price), text(pad + tw_ + gap, cy + 6, "Has:", 16, anchor="start")]
    x = pad + tw_ + gap + lw
    for t, w in zip(toks, cw):
        b.append(draw_tok(t, x + w / 2, cy))
        x += w + 8
    return svg_wrap(int(W + 0.99), int(H + 0.99), "".join(b),
                    "price tag and money: %s %s, has %s" % (name, m(price), group(toks)))


def two_purses_svg(n1, t1, n2, t2):
    """two people and their coins, one row each"""
    fs, pad, gap = 16, 6, 8
    lw = max(tw(n1, fs), tw(n2, fs)) + 12
    rows = []
    y = pad
    for n, toks in [(n1, t1), (n2, t2)]:
        hh = max(tok_size(t)[1] for t in toks)
        rows.append((n, toks, y, hh))
        y += hh + 10
    H = y - 10 + pad
    b, Wmax = [], 0
    for n, toks, y0, hh in rows:
        cy = y0 + hh / 2
        b.append(text(pad + lw - 12, cy + 6, n, fs, anchor="end"))
        x = pad + lw
        for t in toks:
            w = tok_size(t)[0]
            b.append(draw_tok(t, x + w / 2, cy))
            x += w + gap
        Wmax = max(Wmax, x - gap + pad)
    return svg_wrap(int(Wmax + 0.99), int(H + 0.99), "".join(b),
                    "money: %s has %s, %s has %s" % (n1, group(t1), n2, group(t2)))


def shuffled(toks, rnd):
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


# ============================================================ set 1: picture story problems
JOIN = [
    ("apple", "{N} picked {a} apples. Then {he} picked {b} more. How many apples does {he} have now?"),
    ("star", "{N} has {a} stickers. {His} teacher gives {him} {b} more. How many stickers does {he} have now?"),
    ("duck", "{a} ducks are on the dam. {b} more ducks land. How many ducks are there now?"),
    ("fish", "{a} fish are in a rock pool. {b} more fish swim in. How many fish are there now?"),
    ("block", "{N} has a tower of {a} blocks. {He} adds {b} more. How many blocks are there now?"),
    ("biscuit", "There are {a} Anzac biscuits on a plate. Dad bakes {b} more. How many biscuits are there now?"),
    ("car", "{N} has {a} toy cars. {He} gets {b} more for {his} birthday. How many toy cars does {he} have now?"),
    ("balloon", "There are {a} balloons at the party. {N} blows up {b} more. How many balloons are there now?"),
    ("flower", "{N} planted {a} flowers. Then {he} planted {b} more. How many flowers are there now?"),
]
TAKE = [
    ("balloon", "{N} had {a} balloons. {b} popped. How many balloons are left?"),
    ("biscuit", "There were {a} biscuits in the tin. The class ate {b}. How many biscuits are left?"),
    ("duck", "{a} ducks were on the dam. {b} flew away. How many ducks are left?"),
    ("star", "{N} had {a} stickers. {He} gave {b} to {his} friends. How many stickers does {he} have left?"),
    ("fish", "{a} fish were in the rock pool. {b} swam away. How many fish are left?"),
    ("ball", "There were {a} balls in the sport bag. {b} rolled away. How many balls are left?"),
    ("car", "{a} cars were in the car park. {b} drove away. How many cars are left?"),
    ("apple", "{N} had {a} apples. {He} ate {b} at recess and lunch. How many apples are left?"),
]
TOGETHER = [
    ("ball", "red", "blue", "In the sport shed there are {a} red balls and {b} blue balls. How many balls are there in all?"),
    ("flower", "yellow", "pink", "{N} has {a} yellow flowers and {b} pink flowers. How many flowers does {he} have in all?"),
    ("block", "green", "blue", "{N} has {a} green blocks and {b} blue blocks. How many blocks does {he} have in all?"),
]


def join_item(P, kind, tpl, a, b):
    c = a + b
    q = fig(join_svg(a, b, kind)) + say(tpl, P.one(), a=a, b=b)
    e = ("Some more came, so add. Start at %d and count on %d: %s. %d + %d = <b>%d</b>."
         % (a, b, ", ".join(str(a + i) for i in range(1, b + 1)), a, b, c))
    return mcq_n(q, c, [a - b if a > b else b - a, c + 1, c - 1, a, b, c + 2], e)


def take_item(P, kind, tpl, a, b):
    c = a - b
    q = fig(take_svg(a, b, kind)) + say(tpl, P.one(), a=a, b=b)
    e = ("Some went away, so take away. Count the ones not crossed out. %d %s %d = <b>%d</b>. Do not add."
         % (a, MINUS, b, c))
    return mcq_n(q, c, [a + b, c + 1, c - 1, b, a, c + 2], e)


def together_item(P, kind, c1, c2, tpl, a, b):
    c = a + b
    q = fig(two_colour_svg(a, b, kind, c1, c2)) + say(tpl, P.one(), a=a, b=b)
    big, small = max(a, b), min(a, b)
    e = ("Put the two groups together, so add. Start with the bigger number, %d. Count on %d: %s. "
         "%d + %d = <b>%d</b>." % (big, small, ", ".join(str(big + i) for i in range(1, small + 1)), a, b, c))
    return mcq_n(q, c, [big - small, c + 1, c - 1, big, small, c + 2], e)


def set_story(P, rnd):
    J, T, G = list(JOIN), list(TAKE), list(TOGETHER)
    rnd.shuffle(J)
    rnd.shuffle(T)
    plan = [("J", 3, 2), ("T", 6, 2), ("J", 4, 3), ("T", 8, 3), ("J", 5, 4), ("G", 6, 3), ("T", 9, 5),
            ("J", 6, 3), ("T", 10, 4), ("J", 7, 5), ("G", 7, 5), ("T", 12, 3), ("J", 8, 5), ("T", 13, 5),
            ("J", 9, 4), ("T", 15, 6), ("J", 9, 6), ("G", 9, 8), ("T", 17, 8), ("J", 8, 7)]
    its = []
    for kind, a, b in plan:
        if kind == "J":
            k, tpl = J.pop()
            its.append(join_item(P, k, tpl, a, b))
        elif kind == "T":
            k, tpl = T.pop()
            its.append(take_item(P, k, tpl, a, b))
        else:
            k, c1, c2, tpl = G.pop(0)
            its.append(together_item(P, k, c1, c2, tpl, a, b))
        assert b >= 2 and (a <= 20 and a - b >= 2 if kind == "T" else a + b <= 20)
    assert len(its) == 20
    return {"title": "Picture story problems", "items": its}


# ============================================================ set 2: how many more?
CMP = [
    ("apple", "{A} has {x} apples. {B} has {y} apples."),
    ("star", "{A} has {x} stickers. {B} has {y} stickers."),
    ("ball", "{A} kicked {x} balls into the net. {B} kicked {y}."),
    ("fish", "{A} caught {x} fish off the jetty. {B} caught {y}."),
    ("flower", "{A} picked {x} flowers. {B} picked {y} flowers."),
    ("block", "{A} has {x} blocks. {B} has {y} blocks."),
    ("car", "{A} has {x} toy cars. {B} has {y} toy cars."),
    ("biscuit", "{A} baked {x} biscuits. {B} baked {y} biscuits."),
    ("balloon", "{A} has {x} balloons. {B} has {y} balloons."),
    ("duck", "{A} saw {x} ducks at the dam. {B} saw {y} ducks."),
]
NEED = [
    ("star", "{N} needs {w} stickers to fill {his} chart. {He} has {h}. How many more stickers does {he} need?"),
    ("flower", "{N} wants to plant {w} flowers. {He} has planted {h}. How many more flowers does {he} need to plant?"),
    ("block", "{N} needs {w} blocks for a tower. {He} has {h}. How many more blocks does {he} need?"),
    ("apple", "The fruit box holds {w} apples. {N} has put in {h}. How many more apples fit in the box?"),
]


def cmp_item(P, ctx, x, y, lines, fewer=False):
    kind, tpl = ctx
    A, B = P.two()
    d = x - y
    w = WORD[kind][1]
    if fewer:
        qq = "How many fewer %s does %s have than %s?" % (w, B, A)
        if kind in ("ball", "fish", "flower", "biscuit", "duck"):
            verb = {"ball": "kick", "fish": "catch", "flower": "pick", "biscuit": "bake", "duck": "see"}[kind]
            qq = "How many fewer %s did %s %s than %s?" % (w, B, verb, A)
    else:
        qq = "How many more %s does %s have than %s?" % (w, A, B)
        if kind in ("ball", "fish", "flower", "biscuit", "duck"):
            verb = {"ball": "kick", "fish": "catch", "flower": "pick", "biscuit": "bake", "duck": "see"}[kind]
            qq = "How many more %s did %s %s than %s?" % (w, A, verb, B)
    q = fig(rows_svg(x, y, A, B, kind, lines)) + tpl.format(A=A, B=B, x=x, y=y) + " " + qq
    if lines:
        e = "Match them one to one. %d of %s’s %s have no match. %d %s %d = <b>%d</b>. Do not add." % (
            d, A, w, x, MINUS, y, d)
    else:
        e = "Count on from %d to %d: %s. That is %d. %d %s %d = <b>%d</b>. Do not add." % (
            y, x, ", ".join(str(y + i) for i in range(1, d + 1)), d, x, MINUS, y, d)
    return mcq_n(q, d, [x + y, x, y, d + 1, d - 1], e)


def need_item(P, ctx, h, w):
    kind, tpl = ctx
    d = w - h
    q = fig(need_svg(h, w, kind)) + say(tpl, P.one(), w=w, h=h)
    e = "Count on from %d to %d: %s. That is %d. Or count the empty spaces. %d + <b>%d</b> = %d." % (
        h, w, ", ".join(str(h + i) for i in range(1, d + 1)), d, h, d, w)
    return mcq_n(q, d, [w + h, w, h, d + 1, d - 1], e)


def set_more(P, rnd):
    cx = list(CMP)
    rnd.shuffle(cx)
    its = []
    k = 0

    def nxt():
        nonlocal k
        c = cx[k % len(cx)]
        k += 1
        return c

    for x, y in [(5, 3), (6, 4), (7, 2), (8, 5), (6, 3), (9, 6)]:
        its.append(cmp_item(P, nxt(), x, y, True))
    for x, y in [(9, 5), (8, 6)]:
        its.append(cmp_item(P, nxt(), x, y, True, fewer=True))
    nd = list(NEED)
    for h, w in [(6, 10), (7, 10), (4, 10), (8, 10)]:
        its.append(need_item(P, nd.pop(0), h, w))
    for x, y in [(10, 7), (11, 7)]:
        its.append(cmp_item(P, nxt(), x, y, True))
    its.append(cmp_item(P, nxt(), 12, 8, True, fewer=True))
    for x, y in [(14, 9), (16, 8), (13, 7)]:
        its.append(cmp_item(P, nxt(), x, y, False))
    its.append(cmp_item(P, nxt(), 15, 11, False, fewer=True))
    its.append(cmp_item(P, nxt(), 18, 11, False))
    assert len(its) == 20, len(its)
    return {"title": "How many more?", "items": its}


# ============================================================ set 3: Australian coins
def set_coins(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq_t(q, right, wrongs, e))

    s(fig(one_svg("C5")) + "How much is this coin worth?", "5c", ["$5", "50c", "10c"],
      "The coin says 5c. The c means cents. It is worth <b>5c</b>. It is our smallest coin.")
    s(fig(one_svg("C10")) + "How much is this coin worth?", "10c", ["$10", "$1", "5c"],
      "The coin says 10c. It is worth <b>10c</b> (10 cents). $10 is a note.")
    s(fig(one_svg("C20")) + "How much is this coin worth?", "20c", ["$20", "$2", "10c"],
      "The coin says 20c. It is worth <b>20c</b> (20 cents). $2 is a gold coin.")
    s(fig(one_svg("C50")) + "How much is this coin worth?", "50c", ["$50", "5c", "20c"],
      "This coin has 12 sides. It says 50c. It is worth <b>50c</b> (50 cents).")
    s(fig(one_svg("C100")) + "How much is this gold coin worth?", "$1", ["10c", "$10", "$2"],
      "This gold coin says $1. It is worth <b>$1</b> (one dollar). The $ sign means dollars.")
    s(fig(one_svg("C200")) + "How much is this gold coin worth?", "$2", ["20c", "$20", "$1"],
      "This small gold coin says $2. It is worth <b>$2</b> (two dollars), not 20c.")
    s(fig(one_svg("N5")) + "How much is this note worth?", "$5", ["5c", "$50", "$2"],
      "The note says $5. It is worth <b>$5</b> (five dollars).")
    s(fig(money_svg(["C50", "C20", "C10", "C5"], gap=10, label="money: coins 50c, 20c, 10c, 5c")) +
      "Which coin has 12 sides?", "50c", ["20c", "10c", "5c"],
      "The <b>50c</b> coin has 12 sides. The other coins are round.")
    s(fig(money_svg(["C100", "C200", "C50", "C20"], gap=10, label="money: coins $1, $2, 50c, 20c")) +
      "Which two coins are gold?", "$1 and $2", ["50c and $1", "20c and $2", "50c and 20c"],
      "The <b>$1 and $2</b> coins are gold. The cents coins are silver.")
    s("How do you write 20 cents?", "20c", ["$20", "20", "$2"],
      "Write the number, then c for cents: <b>20c</b>. $20 would be 20 dollars.")
    s("How do you write 2 dollars?", "$2", ["20c", "2$", "$20"],
      "Write the $ sign first, then the number: <b>$2</b>. 20c would be 20 cents.")
    s(fig(money_svg(["C100", "C200"], gap=16, label="money: coins $1 (bigger), $2 (smaller)")) +
      "The $1 coin is bigger than the $2 coin. Which coin is worth more?",
      "the $2 coin", ["the $1 coin", "They are the same.", "We cannot tell."],
      "Size does not tell you the value. Read the number. $2 is more than $1, so <b>the $2 coin</b> is worth more.")
    s(fig(money_svg(["C50", "C100"], gap=16, label="money: coins 50c (bigger), $1 (smaller)")) +
      "The 50c coin is bigger than the $1 coin. Which coin is worth more?",
      "the $1 coin", ["the 50c coin", "They are the same.", "We cannot tell."],
      "$1 is 100 cents. 100c is more than 50c. So <b>the $1 coin</b> is worth more, even though it is smaller.")
    A, B = P.two()
    s(fig(two_purses_svg(A, ["C20"], B, ["C200"])) +
      "%s has a 20c coin. %s has a $2 coin. Who has more money?" % (A, B), B, [A, "They are the same.", "We cannot tell."],
      "The 20c coin is bigger, but $2 is worth more than 20c. <b>%s</b> has more money." % B)
    its.append(letter_q("Which coin is worth the most?", "C200", ["C50", "C20", "C100"],
                        "<b>{L}</b> is the $2 coin. It is worth the most. The 50c coin is the biggest, "
                        "but it is only worth 50 cents."))
    its.append(letter_q("Which coin is worth the least?", "C5", ["C10", "C20", "C200"],
                        "<b>{L}</b> is the 5c coin. 5 cents is the least. The $2 coin is small, "
                        "but it is worth a lot."))
    s(fig(money_svg(["C20", "C200", "C10", "C50"], gap=10, label="money: coins 20c, $2, 10c, 50c")) +
      "Which coin is worth the most?", "$2", ["50c", "20c", "10c"],
      "The <b>$2</b> coin is worth the most, even though it is small. The 50c coin is the biggest, but it is worth less.")
    s(fig(money_svg(["C50", "C50"], gap=16)) +
      "Two 50c coins are worth the same as which coin?", "$1", ["$2", "50c", "20c"],
      "50c and 50c make 100c. 100c is the same as <b>$1</b>.")
    s(fig(money_svg(["C10", "C10"], gap=16)) +
      "Two 10c coins are worth the same as which coin?", "20c", ["$2", "10c", "50c"],
      "10c and 10c make <b>20c</b>. One 20c coin is worth the same.")
    s(fig(money_svg(["C100", "C50", "C200", "C20"], gap=10, label="money: coins $1, 50c, $2, 20c")) +
      "Put these coins in order. Start with the least.", "20c, 50c, $1, $2",
      ["$2, $1, 50c, 20c", "20c, $2, $1, 50c", "$2, 20c, $1, 50c"],
      "Cents come first: 20c, then 50c. Then dollars: $1, then $2. The order is <b>20c, 50c, $1, $2</b>. "
      "Do not order them by size.")
    assert len(its) == 20, len(its)
    return {"title": "Australian coins", "items": its}


# ============================================================ set 4: count the coins
def count_e(toks):
    toks = srt(toks)
    T = total(toks)
    run, s = [], 0
    for t in toks:
        s += VAL[t]
        run.append(m(s) if T >= 100 else "%dc" % s)
    if len(set(toks)) == 1:
        v = VAL[toks[0]]
        step = v // 100 if v >= 100 else v
        e = "Each coin is %s. Count in %ds: %s." % (lab(v), step, ", ".join(run))
    else:
        e = "Start with the coin worth the most. Count on: %s." % ", ".join(run)
    return e + " That is <b>%s</b>." % m(T)


def set_count(P, rnd):
    its = []
    groups = [
        [("C10", 2)], [("C5", 3)], [("C10", 3)], [("C20", 2)], [("C10", 1), ("C5", 1)],
        [("C10", 2), ("C5", 1)], [("C20", 1), ("C10", 1)], [("C20", 1), ("C5", 1)], [("C10", 4)],
        [("C20", 1), ("C10", 1), ("C5", 1)], [("C20", 2), ("C10", 1)], [("C50", 1), ("C10", 1)],
        [("C50", 1), ("C20", 1)], [("C20", 1), ("C10", 2), ("C5", 1)], [("C50", 1), ("C20", 1), ("C5", 1)],
        [("C10", 1), ("C5", 2)], [("C50", 2)], [("C100", 2)], [("C200", 1), ("C100", 1)], [("C200", 2), ("C100", 1)],
    ]
    mixed = {13, 14, 15}
    stems = ["How much money is this?", "{N} has these coins. How much does {he} have?",
             "{N} finds these coins in {his} pocket. How much is it?", "What is the total?",
             "{N} puts these coins in {his} money box. How much is that?"]
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T <= 500 and len(toks) <= 4
        st = say(stems[i % len(stems)], P.one())
        shown = shuffled(toks, rnd) if i in mixed else toks
        e = count_e(toks)
        if i in mixed:
            e = "Put the coins in order, the most first. " + e
        dollars = T >= 100
        if dollars:
            e += " Count the value of each coin, not the number of coins."
            n = len(toks)
            cands = ["%dc" % m_dollar_as_c(toks), "%dc" % n if n != m_dollar_as_c(toks) else None,
                     m_skip(toks, -1), m_twice(toks, -1), "$%d" % n, T + 100, T - 100, "$100" if T == 100 else None,
                     T // 10]   # $2 mixed up with 20c   # 50c + 50c = 100, written as $100
        else:
            if len(toks) >= 2:
                e += " There are %d coins, but they are worth %s." % (len(toks), m(T))
            cands = [m_count(toks), m_same_step(toks), m_skip(toks, -1), m_twice(toks, -1), m_skip(toks, 0),
                     T + 5, T - 5, T + 10]
        its.append(mcq_m(fig(money_svg(shown, gap=10)) + st, T, cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Count the coins", "items": its}


# ============================================================ set 5: buying things
SHOP = [("apple", 50), ("banana", 40), ("pencil", 30), ("sticker", 20)]


def set_buy(P, rnd):
    its = []
    price = dict(SHOP)
    board = fig(price_svg(SHOP, "class shop"))

    def tq(q, right, wrongs, e):
        its.append(mcq_t(q, right, wrongs, e))

    def mq(q, right, cands, e):
        its.append(mcq_m(q, right, cands, e))

    p = P.one()
    tq(fig(has_svg("apple", 50, ["C50"])) + say("An apple costs 50c. {N} has a 50c coin. Can {he} buy the apple?", p),
       "Yes. It is just right.", ["No. 50c is too little.", "No. {He} needs 2 coins.".format(**p), "We cannot tell."],
       "The coin is worth 50c. The apple costs 50c. So <b>yes</b>, it is just right.")
    p = P.one()
    tq(fig(has_svg("pencil", 30, ["C20"])) + say("A pencil costs 30c. {N} has a 20c coin. Can {he} buy the pencil?", p),
       "No. 20c is less than 30c.", ["Yes. {He} has a coin.".format(**p), "Yes. 20c is more.", "We cannot tell."],
       "20c is less than 30c. So <b>no</b>. %s needs 10c more." % p["N"])
    p = P.one()
    tq(fig(has_svg("sticker", 20, ["C10", "C10", "C10"])) +
       say("A sticker costs 20c. {N} has three 10c coins. Can {he} buy the sticker?", p),
       "Yes. {He} has 30c.".format(**p), ["No. {He} has 3c.".format(**p), "No. {He} needs a 20c coin.".format(**p),
                                          "We cannot tell."],
       "Count in tens: 10c, 20c, 30c. 30c is more than 20c, so <b>yes</b>. Count the value, not the coins.")
    p = P.one()
    tq(fig(has_svg("juice", 200, ["C100"])) + say("A juice costs $2. {N} has a $1 coin. Can {he} buy the juice?", p),
       "No. $1 is less than $2.", ["Yes. The $1 coin is bigger.", "Yes. {He} has a coin.".format(**p), "We cannot tell."],
       "The $1 coin is bigger, but it is worth less. $1 is less than $2, so <b>no</b>.")
    tq(fig(price_svg([("apple", 50)], "apple")) + "An apple costs 50c. Which coins make 50c?",
       coin_list([20, 20, 10]), [coin_list([20, 20, 20]), coin_list([20, 10, 10]), coin_list([10, 10, 5])],
       "20c + 20c = 40c. 40c + 10c = 50c. So <b>20c, 20c and 10c</b> make 50c.")
    assert sum([20, 20, 10]) == 50 and len({60, 40, 25, 50}) == 4
    tq(fig(price_svg([("koala sticker", 25)], "koala sticker")) + "A koala sticker costs 25c. Which coins make 25c?",
       coin_list([20, 5]), [coin_list([20, 10]), coin_list([10, 5]), coin_list([10, 10])],
       "20c and 5c more is 25c. So <b>20c and 5c</b> make 25c.")
    assert len({25, 30, 15, 20}) == 4
    assert sum([20, 10, 10]) == 40 and sum([20, 20, 20]) == 60 and sum([10, 10, 5]) == 25
    # class shop
    p = P.one()
    T = price["pencil"] + price["sticker"]
    mq(board + say("At the class shop, {N} buys a pencil and a sticker. How much does {he} pay?", p), T,
       [10, 5, 60, 40],
       "Buying two things, so add. 30c + 20c: count on in tens from 30c: 40c, 50c. That is <b>50c</b>. "
       "10c is what you get if you take away.")
    p = P.one()
    T = price["banana"] + price["sticker"]
    mq(board + say("At the class shop, {N} buys a banana and a sticker. How much does {he} pay?", p), T,
       [20, 6, 50, 70],
       "40c + 20c: count on in tens from 40c: 50c, 60c. That is <b>60c</b>.")
    p = P.one()
    mq(board + say("{N} has 40c. {He} buys a pencil. How much money does {he} have left?", p),
       40 - price["pencil"], [70, 30, 40, 20],
       "{N} spends money, so take away. Count on from 30c to 40c: 10c more. 40c %s 30c = <b>10c</b>.".format(**p) % MINUS)
    p = P.one()
    mq(board + say("{N} has 30c. How much more does {he} need to buy the apple?", p), 20, [80, 30, 50, 10],
       "Count on from 30c to 50c: 40c, 50c. That is 2 tens, so <b>20c</b> more. Do not add.")
    p = P.one()
    mq(board + say("{N} buys 2 stickers. How much does {he} pay?", p), 40, [22, 20, 4],
       "Each sticker is 20c. 20c + 20c = <b>40c</b>. 22c adds the 2 to 20. 4c forgets that 2 tens is 20c.")
    tq(board + "Which two things cost 70c in all?", "the apple and the sticker",
       ["the banana and the sticker", "the pencil and the sticker", "the apple and the pencil"],
       "Apple 50c + sticker 20c = 70c. The answer is <b>the apple and the sticker</b>.")
    assert price["apple"] + price["sticker"] == 70
    assert len({price["banana"] + price["sticker"], price["pencil"] + price["sticker"],
                price["apple"] + price["pencil"], 70}) == 4
    # whole dollars
    p = P.one()
    mq(fig(price_svg([("icy pole", 200), ("juice", 300)], "school canteen")) +
       say("At the canteen, {N} buys an icy pole and a juice. How much does {he} pay?", p), 500, [100, "5c", 600, 400],
       "Buying both, so add. $3 + $2 = <b>$5</b>. $1 is what you get if you take away.")
    p = P.one()
    mq(fig(money_svg(["N5"], label="money: one $5 note")) +
       say("{N} has $5. {He} buys an icy pole for $2. How much does {he} have left?", p), 300, [700, 200, 400],
       "{He} spends $2, so take away. $5 %s $2 = <b>$3</b>. Count back from 5: 4, 3.".format(**p) % MINUS)
    p = P.one()
    mq(fig(money_svg(["C200", "C100", "C100"], gap=10)) +
       say("Mum gives {N} a $2 coin and two $1 coins. How much money is that?", p), 400, [300, "4c", 500, 200],
       "Start with $2. Count on $1, $1: $3, $4. That is <b>$4</b>. There are 3 coins, but they are worth $4.")
    p = P.one()
    mq(fig(money_svg(["C200", "C200", "C200", "C200"], gap=10)) +
       say("{N} has four $2 coins. How much money does {he} have?", p), 800, [400, "8c", 600, 1000],
       "Count in twos: $2, $4, $6, $8. That is <b>$8</b>. $4 counts the coins, not their value.")
    p = P.one()
    mq(fig(price_svg([("sausage sizzle", 300)], "sausage sizzle")) +
       say("A sausage sizzle costs $3. {N} buys 2. How much does {he} pay?", p), 600, [500, 300, 100],
       "2 lots of $3: $3 + $3 = <b>$6</b>. $5 adds 3 and 2, but %s buys 2 lots of $3." % p["N"])
    p = P.one()
    mq(fig(price_svg([("koala toy", 1000)], "koala toy")) +
       say("A koala toy costs $10. {N} has $6. How much more does {he} need?", p), 400, [1600, 600, 500],
       "Count on from $6 to $10: $7, $8, $9, $10. That is <b>$4</b> more. Do not add: $16 is too much.")
    A, B = P.two()
    mq(fig(two_purses_svg(A, ["C20", "C10"], B, ["C50"])) +
       "%s has 30c. %s has 50c. How much more money does %s have?" % (A, B, B), 20, [80, 50, 30, 10],
       "Count on from 30c to 50c: 40c, 50c. That is <b>20c</b> more. %s has 1 coin, but it is worth more." % B)
    p = P.one()
    mq(fig(money_svg(["N5", "C200", "C200"], gap=10, label="money: one $5 note and two $2 coins")) +
       say("{N} has $9. {He} spends $5 at the school fete. How much does {he} have left?", p), 400,
       [1400, 500, 300],
       "{He} spends money, so take away. $9 %s $5 = <b>$4</b>. Count on from $5 to $9: $6, $7, $8, $9. That is 4.".format(**p)
       % MINUS)
    assert len(its) == 20, len(its)
    return {"title": "Buying things", "items": its}


# ============================================================ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    walk = toks_of(("C20", 1), ("C10", 1), ("C5", 1))
    assert total(walk) == 35
    return (
        "<h2>Picture the story</h2>"
        "<p>Read the story. Ask: what happens? Do some <b>come</b>, or do some <b>go away</b>? "
        "Draw it. Then add or take away.</p>"
        "<figure class='sn-fig'>" + join_svg(5, 3, "apple") +
        "<figcaption>Mia picked 5 apples. Then she picked 3 more. Count on from 5: 6, 7, 8. 5 + 3 = 8 apples.</figcaption></figure>"
        "<figure class='sn-fig'>" + take_svg(9, 4, "balloon") +
        "<figcaption>Leo had 9 balloons. 4 popped. Cross out 4. 5 are left. 9 − 4 = 5 balloons.</figcaption></figure>"
        "<h2>How many more?</h2>"
        "<p>Line up the two rows. Match them one to one. The extra ones are the answer.</p>"
        "<figure class='sn-fig'>" + rows_svg(8, 5, "Ava", "Jack", "star", lines=True) +
        "<figcaption>Ava has 8 stickers. Jack has 5. Ava has 3 more. 8 − 5 = 3. Do not add.</figcaption></figure>" +
        ex("Count on", "Isla needs 10 stickers. She has 7. How many more does she need?",
           "Count on from 7: 8, 9, 10. That is 3 jumps.", "3 more stickers") +
        "<h2>Australian coins</h2>"
        "<p>Our coins are 5c, 10c, 20c, 50c, $1 and $2. <b>c</b> means cents. <b>$</b> means dollars. "
        "The $1 and $2 coins are gold.</p>"
        "<figure class='sn-fig'>" + money_svg(["C5", "C10", "C20", "C50", "C100", "C200"], per_row=6,
                                              label="Australian coins: 5c, 10c, 20c, 50c, $1, $2") +
        "<figcaption>5c, 10c, 20c, 50c, $1 and $2.</figcaption></figure>"
        "<p><b>Size is not value.</b> The 50c coin is the biggest. The $2 coin is small, but it is worth the most. "
        "Read the number on the coin.</p>"
        "<h2>Count coins, biggest value first</h2>"
        "<p>Start with the coin worth the most. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=20, under=["20c", "30c", "35c"],
                                              label="counting on: 20c, 30c, 35c") +
        "<figcaption>20c, 30c, 35c. There are 3 coins, but they are worth 35c.</figcaption></figure>" +
        ex("Buying", "An apple costs 50c. Which coins can you use?",
           "20c + 20c = 40c. 40c + 10c = 50c.", "20c, 20c and 10c") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding when some go away", "Ask: do they come or go? If they go, take away."],
            ["Adding for “how many more”", "Line them up. Count the extra ones: 8 − 5 = 3."],
            ["3 coins, so 3c", "Add the value of each coin: 20c, 30c, 35c."],
            ["The 50c coin is biggest, so it is worth the most", "Read the number: $2 is worth the most."],
            ["Mixing up $2 and 20c", "$ means dollars. c means cents. $2 is much more than 20c."],
        ])
    )


FAQ = [
    {"q": "What word problems do Year 1 students solve in Australia?",
     "a": "In the Australian Curriculum (AC9M1N05), Year 1 students solve adding and taking-away problems, including simple buying with money. They show the story with pictures, objects or drawings, then add or subtract."},
    {"q": "Which coins does my Year 1 child need to know?",
     "a": "The Australian coins are 5c, 10c, 20c, 50c, $1 and $2. Children read the number on each coin and count small amounts, such as 20c + 10c + 5c = 35c."},
    {"q": "Why is the 50c coin bigger than the $2 coin?",
     "a": "The size of a coin does not show its value. The 50c coin is the biggest, but the small gold $2 coin is worth the most, so children should read the number."},
    {"q": "How can I help my child with “how many more” questions?",
     "a": "Line up two rows of objects and match them one to one. The extra objects are the answer, so 8 stickers and 5 stickers means 3 more."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so the objects and coins stay easy to count."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1805)
    P = People(rnd)
    sets = [set_story(P, rnd), set_more(P, rnd), set_coins(P, rnd), set_count(P, rnd), set_buy(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [v for v in (mval(c) for c in it["c"]) if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"].count("<svg") <= 1
            plain = re.sub(r"<[^>]+>", " ", it["q"])
            assert plain not in seen, plain
            seen.add(plain)
            for t in [plain, it["e"]] + it["c"]:
                assert "\\" not in t and ".." not in t
                assert not re.search(r"(?<![\d$])1 (apples|stickers|balls|flowers|blocks|biscuits|balloons|cars|ducks|coins)\b", t), t
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "word-problems-and-money", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Word Problems and Money: Add, Take Away and Count Coins",
        "seo_title": "Year 1 Word Problems and Money Worksheets: Australian Coins, Free with Answer Key",
        "short_title": "Word problems and money",
        "domain": "Number",
        "standard_code": "AC9M1N05",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical problems involving additive situations including simple money transactions; represent the situations with diagrams, physical and virtual materials, and use calculation strategies to solve the problem",
        "meta_desc": "Free Year 1 maths worksheets for the Australian Curriculum: picture story problems within 20, how many more, Australian coins (size is not value), counting small amounts of coins and simple buying at the class shop and canteen. 100 questions with an answer key.",
        "key_big": "Picture the story. Do some come or go? Then add or take away.",
        "key_sub": "For “how many more”, line them up and count the extra ones. With coins, read the number, not the size, and count the value of each coin: 20c, 30c, 35c.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "picture|money|pictures|price")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
