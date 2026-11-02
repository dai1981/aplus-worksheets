# -*- coding: utf-8 -*-
"""
BC Grade 2 Math: Coins to 100 Cents (BC Mathematics Curriculum, Grade 2, Financial literacy:
"coin combinations to 100 cents, and spending and saving")
  python3 tools/gen_cabc_math_g2_money.py
Grade 2: coin amounts to 100¢, written in cents (75¢). No $1.35-type amounts.
Canadian coins: nickel 5¢, dime 10¢ (the smallest coin), quarter 25¢, loonie $1 = 100¢ (11 sides, gold colour),
toonie $2 (silver ring, gold centre; only named, never counted). No pennies.
Coins are simple labelled shapes (no real designs). Short sentences for 7-8 year olds.
Sets: coin values; count collections to 100¢; the same amount in different ways; fewest coins;
spending and saving for a $1 goal and word problems in BC settings.
Wrong answers come from real mistakes: counting coins instead of their value, a quarter taken as 20¢,
the bigger nickel taken as 10¢ and the small dime as 5¢, missing or double-counting one coin, keeping the
old step when the coin changes, adding when the question takes away, subtracting the smaller digit from
the bigger one in each place, and forgetting to regroup.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Lucas", "Mateo", "Kai", "Owen", "Ryan"]

# ------------------------------------------------------------ money facts
ORDER = ["T", "L", "Q", "D", "N"]   # biggest value first
VAL = {"T": 200, "L": 100, "Q": 25, "D": 10, "N": 5}
ONE = {"T": "toonie", "L": "loonie", "Q": "quarter", "D": "dime", "N": "nickel"}
MANY = {k: (v + "s") for k, v in ONE.items()}
BYVAL = {v: k for k, v in VAL.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius in proportion to the real coins (mm): dime 18, nickel 21.2, quarter 23.9, loonie 26.5, toonie 28
COIN = {"D": (18, SILVER, 14), "N": (21, SILVER, 15), "Q": (24, SILVER, 15), "L": (26, GOLD, 16), "T": (28, SILVER, 16)}


def lab(v):
    """label on a coin: $1, $2 or 5¢, 10¢, 25¢"""
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def C(v):
    """an amount in cents"""
    assert isinstance(v, int) and v > 0, v
    return "%d¢" % v


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
def count_on(toks):
    toks = srt(toks)
    T = total(toks)
    s, run = 0, []
    for t in toks:
        s += VAL[t]
        run.append(C(s))
    if len(toks) == 1:
        return "One %s is <b>%s</b>." % (ONE[toks[0]], C(T))
    if len(set(toks)) == 1:
        t = toks[0]
        return "Each %s is %s. Count by %s: %s. That is <b>%s</b>." % (ONE[t], C(VAL[t]), C(VAL[t]), ", ".join(run), C(T))
    return "Start with the biggest coin and count on: %s. That is <b>%s</b>." % (", ".join(run), C(T))


# ------------------------------------------------------------ typical mistakes (all computed, in cents)
def m_count(toks):
    """counted the coins, not their value"""
    return len(toks)


def m_quarter20(toks):
    return sum(20 if t == "Q" else VAL[t] for t in toks)


def m_swap(toks):
    """the bigger nickel taken as 10¢ and the small dime as 5¢"""
    sw = {"N": 10, "D": 5}
    return sum(sw.get(t, VAL[t]) for t in toks)


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


def m_digits(a, b):
    """a − b, taking the smaller digit from the bigger one in each place (no regrouping)"""
    da, db = "%02d" % a, "%02d" % b
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da[-2:], db[-2:])))


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=str):
    """4 choices: correct + the first 3 usable unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or (fmt is C and c > 300):
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
    r = COIN[t][0]
    return 2 * r, 2 * r


def polygon(cx, cy, r, n, rot=-90):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def draw_tok(t, cx, cy):
    """one coin, labelled with its value"""
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


def price_svg(items, title):
    """a row of price tags: [('apple', 35), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 18, 70) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, C(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, C(p)) for n, p in items))


def goal_svg(saved, goal=100):
    """a savings bar from 0¢ to 100¢ in 10¢ steps, shaded up to the amount saved"""
    pad, step, bh = 22, 30, 30
    W = 2 * pad + step * 10
    H = 82
    y0 = 24
    b = [text(pad, 16, "Saved: %s" % C(saved), 15, "start", GREEN), text(W - pad, 16, "Goal: %s" % C(goal), 15, "end")]
    b.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (pad, y0, step * 10, bh, INK))
    b.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='#9fd3a8' stroke='%s' stroke-width='2'/>"
             % (pad, y0, step * 10 * saved / goal, bh, GREEN))
    for i in range(11):
        x = pad + i * step
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y0, x, y0 + bh + 5, INK))
        if i % 2 == 0:
            b.append(text(x, y0 + bh + 21, C(i * 10) if i else "0¢", 14))
    return svg_wrap(W, H, "".join(b), "savings bar: %s saved of a %s goal" % (C(saved), C(goal)))


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


# ============================================================ set 1: coin values
def set_values(P, rnd):
    its = []

    def s(q, right, wrong, e, fmt=str):
        its.append(mcq(q, right, wrong, e, fmt))

    tips = {
        "N": ("nickel", ["dime", "quarter", "loonie"],
              "This is a <b>nickel</b>. It is worth 5¢. It is bigger than a dime, but worth less."),
        "D": ("dime", ["nickel", "quarter", "toonie"],
              "This is a <b>dime</b>. It is worth 10¢. It is the smallest coin."),
        "Q": ("quarter", ["dime", "nickel", "loonie"],
              "This is a <b>quarter</b>. It is worth 25¢."),
        "L": ("loonie", ["toonie", "quarter", "nickel"],
              "This is a <b>loonie</b>. It is gold in colour and has 11 sides. It is worth $1, or 100¢."),
        "T": ("toonie", ["loonie", "quarter", "dime"],
              "This is a <b>toonie</b>. It has a silver ring and a gold centre. It is worth $2."),
    }
    for t in ["N", "D", "Q", "L", "T"]:
        right, wrong, e = tips[t]
        s(fig(coin_svg(t)) + "What is this coin called?", right, wrong, e)
    s("How much is a nickel worth?", 5, [10, 1, 25],
      "A nickel is worth <b>5¢</b>. Two nickels make a dime.", C)
    s("How much is a dime worth?", 10, [5, 1, 25],
      "A dime is worth <b>10¢</b>. It is small, but it is worth more than a nickel.", C)
    s("How much is a quarter worth?", 25, [20, 50, 10],
      "A quarter is worth <b>25¢</b>, not 20¢. Four quarters make 100¢.", C)
    s("A loonie is worth $1. How many cents is that?", 100, [1, 10, 200],
      "$1 is <b>100¢</b>. So a loonie is worth 100¢.", C)
    s("Which coin is worth 25¢?", "a quarter", ["a dime", "a nickel", "a loonie"],
      "A <b>quarter</b> is worth 25¢.")
    s("Which coin is worth 100¢?", "a loonie", ["a toonie", "a quarter", "a dime"],
      "100¢ is $1. A <b>loonie</b> is worth $1. A toonie is worth $2, or 200¢.")
    s(fig(money_svg(["D", "N"], gap=14, under=["dime", "nickel"], label="a dime (small) and a nickel (bigger)"))
      + "Which coin is worth more?",
      "the dime", ["the nickel", "They are the same.", "You cannot tell."],
      "The <b>dime</b> is worth 10¢. The nickel is worth 5¢. A bigger coin is not always worth more.")
    s(fig(money_svg(["Q", "D", "L", "N"], gap=10, under=["quarter", "dime", "loonie", "nickel"],
                    label="a quarter, a dime, a loonie and a nickel"))
      + "Which coin is worth the least?",
      "the nickel", ["the dime", "the quarter", "the loonie"],
      "Nickel 5¢, dime 10¢, quarter 25¢, loonie 100¢. The <b>nickel</b> is worth the least.")
    s(fig(money_svg(["N", "Q", "D"], gap=10, under=["nickel", "quarter", "dime"],
                    label="a nickel, a quarter and a dime"))
      + "Which coin is worth the most?",
      "the quarter", ["the nickel", "the dime", "They are all the same."],
      "Nickel 5¢, dime 10¢, quarter 25¢. The <b>quarter</b> is worth the most.")
    s("How many nickels make a dime?", "2", ["5", "10", "1"],
      "A nickel is 5¢. 5¢ + 5¢ = 10¢. So <b>2</b> nickels make a dime.")
    s("How many nickels make a quarter?", "5", ["25", "4", "2"],
      "Count by 5s: 5¢, 10¢, 15¢, 20¢, 25¢. That is <b>5</b> nickels. 4 nickels make only 20¢.")
    s("How many dimes make 50¢?", "5", ["50", "2", "10"],
      "Count by 10s: 10¢, 20¢, 30¢, 40¢, 50¢. That is <b>5</b> dimes.")
    s("How many quarters make 100¢?", "4", ["5", "25", "10"],
      "Count by 25s: 25¢, 50¢, 75¢, 100¢. That is <b>4</b> quarters. 5 is right only if a quarter were 20¢.")
    s("How many dimes make 100¢?", "10", ["100", "1", "5"],
      "Count by 10s: 10¢, 20¢, 30¢ … 100¢. That is <b>10</b> dimes.")
    s(fig(money_svg(["Q", "D", "D"], gap=10, label="1 quarter, then 2 dimes"))
      + "Which is worth more: 1 quarter or 2 dimes?",
      "1 quarter", ["2 dimes", "They are the same.", "You cannot tell."],
      "1 quarter is 25¢. 2 dimes are 10¢ + 10¢ = 20¢. 25¢ is more, so <b>1 quarter</b> is worth more. "
      "2 coins are not always worth more than 1 coin.")
    assert len(its) == 20
    return {"title": "Coin values", "items": its}


# ============================================================ set 2: count collections to 100¢
def set_count(P, rnd):
    groups = [
        [("D", 3)], [("N", 4)], [("Q", 2)], [("D", 6)], [("N", 7)], [("Q", 3)],
        [("D", 2), ("N", 3)], [("Q", 1), ("D", 2)], [("Q", 1), ("N", 3)], [("D", 4), ("N", 2)],
        [("Q", 2), ("D", 1), ("N", 1)], [("Q", 1), ("D", 3), ("N", 1)], [("Q", 2), ("D", 3)], [("Q", 3), ("N", 2)],
        [("Q", 1), ("D", 4), ("N", 2)], [("Q", 3), ("D", 1), ("N", 1)], [("Q", 4)], [("Q", 2), ("D", 4), ("N", 2)],
        [("Q", 3), ("D", 2)], [("Q", 2), ("D", 3), ("N", 2)],
    ]
    mixed = {8, 11, 14, 15, 17, 19}
    stems = ["How much money is this?", "%s has these coins. How much does %s have?",
             "%s finds these coins in %s backpack. How much is it?", "What is the total?",
             "%s puts these coins in a piggy bank. How much is in the bank?"]
    its, seen = [], set()
    for i, g in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T <= 100 and len(toks) <= 8 and tuple(toks) not in seen
        seen.add(tuple(toks))
        nm, he, his = P.next()
        st = stems[i % len(stems)]
        if st.count("%s") == 2:
            st = st % (nm, his if "backpack" in st else he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i in mixed else toks
        q = fig(money_svg(shown)) + st
        e = ("Put the coins in order, biggest first. " if i in mixed else "") + count_on(toks)
        if i < 3:
            e += " Count the value of each coin, not the number of coins."
        cands = [m_count(toks), m_quarter20(toks), m_swap(toks), m_same_step(toks), m_skip(toks, -1),
                 m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
        if i % 2:
            cands = [m_quarter20(toks)] + cands
        it = mcq(q, T, cands, e, C)
        if C(len(toks)) in it["c"]:
            it["e"] += " %s counts the coins, not the cents." % C(len(toks))
        if "Q" in toks and C(m_quarter20(toks)) in it["c"]:
            it["e"] += " A quarter is 25¢, not 20¢."
        its.append(it)
    assert len(its) == 20
    return {"title": "Count coins to 100¢", "items": its}


# ============================================================ set 3: the same amount in different ways
def set_ways(P, rnd):
    its = []

    def which(target, right, wrong, stem=None):
        assert sum(right) == target, (target, right)
        vs = {sum(w) for w in wrong}
        assert len(vs) == 3 and target not in vs, (target, wrong)
        q = (stem or "Which coins make %s?") % C(target)
        e = ("<b>%s</b> %s %s. " % (cap(andw(right)), vb(right), C(target)) + " ".join(
            "%s %s %s." % (cap(andw(w)), vb(w), C(sum(w))) for w in wrong))
        its.append(mcq(q, words(right), [words(w) for w in wrong], e))

    def which_not(target, right, wrong):
        assert sum(right) != target
        for w in wrong:
            assert sum(w) == target
        e = ("<b>%s</b> %s %s, not %s. The others all make %s."
             % (cap(andw(right)), vb(right), C(sum(right)), C(target), C(target)))
        its.append(mcq("Which does <b>not</b> make %s?" % C(target), words(right), [words(w) for w in wrong], e))

    def same_as(toks, right, wrong):
        T = total(toks)
        assert sum(right) == T and all(sum(w) != T for w in wrong) and len({sum(w) for w in wrong}) == 3
        q = fig(money_svg(toks)) + "Which is worth the same as these coins?"
        e = count_on(toks) + " <b>%s</b> also %s %s." % (cap(andw(right)), vb(right), C(T))
        its.append(mcq(q, words(right), [words(w) for w in wrong], e))

    def missing(stem, right, wrong, e):
        its.append(mcq(stem, right, wrong, e))

    same_as(["N", "N"], [10], [[5], [25], [10, 10]])
    which(20, [10, 5, 5], [[10, 5], [5] * 5, [10, 10, 10]])
    same_as(["D"] * 5, [25, 25], [[5] * 5, [100], [25, 25, 25]])
    which(35, [25, 10], [[25, 5], [10, 10, 10, 10], [25, 25]])
    which(50, [25, 25], [[25, 10, 10], [10, 10, 10], [25, 25, 5]])
    which_not(25, [10, 10, 10], [[25], [10, 10, 5], [5] * 5])
    nm, he, his = P.next()
    which(45, [25, 10, 10], [[25, 10, 5], [25, 25, 5], [10, 10, 10]],
          stem=nm + " has 3 coins. They make %s. Which coins does " + he + " have?")
    same_as(toks_of(("Q", 2), ("D", 1)), [10] * 6, [[5] * 6, [25, 10, 10, 10], [25, 25, 25]])
    which_not(60, [25, 25, 5], [[25, 25, 10], [25, 10, 10, 10, 5], [10] * 6])
    which(65, [25, 25, 10, 5], [[25, 25, 10], [25, 10, 10, 5], [25, 25, 25, 5]])
    which(75, [25, 25, 25], [[25, 25, 10, 10], [25, 25, 10], [25] * 4])
    missing("2 quarters and some dimes make 70¢. How many dimes?", "2", ["7", "3", "1"],
            "2 quarters: 25¢, 50¢. From 50¢ to 70¢ is 20¢. 20¢ is <b>2</b> dimes. "
            "3 dimes comes from counting a quarter as 20¢.")
    which_not(80, [25, 25, 25], [[25, 25, 10, 10, 10], [10] * 8, [25, 25, 25, 5]])
    nm, he, his = P.next()
    which(55, [25, 10, 10, 10], [[25, 10, 10, 5], [10, 10, 10, 10], [25, 25, 10]],
          stem=nm + " has 4 coins. They make %s. Which coins does " + he + " have?")
    which(90, [25, 25, 25, 10, 5], [[25, 25, 25, 10], [25, 25, 25, 5], [25] * 4])
    a, b = P.next(), P.next()
    assert 25 + 5 * 10 == 75 == 3 * 25
    missing("%s has 1 quarter and 5 dimes. %s has 3 quarters. Who has more money?" % (a[0], b[0]),
            "They have the same.", [a[0], b[0], "You cannot tell."],
            "%s: 25¢, then 35¢, 45¢, 55¢, 65¢, 75¢. %s: 25¢, 50¢, 75¢. Both have 75¢, so <b>they have the same</b>. "
            "%s has more coins, but not more money." % (a[0], b[0], a[0]))
    missing("3 quarters and some nickels make 100¢. How many nickels?", "5", ["25", "8", "4"],
            "3 quarters: 25¢, 50¢, 75¢. From 75¢ to 100¢ is 25¢. Count by 5s: 80¢, 85¢, 90¢, 95¢, 100¢. "
            "That is <b>5</b> nickels. 8 comes from counting a quarter as 20¢.")
    same_as(["L"], [10] * 10, [[10] * 5, [10] * 9, [25, 25, 25]])
    which_not(100, [25, 25, 25, 10, 10], [[25] * 4, [25, 25, 25, 10, 10, 5], [10] * 10])
    which(100, [25, 25, 10, 10, 10, 10, 10], [[25, 25, 10, 10, 10, 10], [25, 25, 25, 10], [25, 10, 10, 10, 10, 10]],
          stem="Which coins make %s, the same as a loonie?")
    assert len(its) == 20
    return {"title": "Make the same amount in different ways", "items": its}


# ============================================================ set 4: fewest coins
def fewest(target, coins):
    best = {0: []}
    step = min(coins)
    for a in range(step, target + 1, step):
        opts = [best[a - c] + [c] for c in coins if a - c in best]
        if opts:
            best[a] = min(opts, key=len)
    return best[target]


CO = [5, 10, 25, 100]


def set_fewest(P, rnd):
    its = []

    def ncoins(k):
        return "%d %s" % (k, "coin" if k == 1 else "coins")

    def how_few(target, wrong, extra, coins=CO, stem=None):
        f = fewest(target, coins)
        n = len(f)
        e = ("Use the biggest coin you can each time: %s %s %s. That is <b>%s</b>. %s"
             % (andw(f), vb(f), C(target), ncoins(n), extra))
        its.append(mcq((stem or "What is the smallest number of coins you can use to make %s?") % C(target),
                       ncoins(n), [ncoins(k) for k in wrong], e))

    def which_fewest(target, wrong):
        f = fewest(target, CO)
        for x in wrong:
            assert sum(x) == target and len(x) > len(f)
        e = ("All of these make %s. <b>%s</b> %s only %s. Start with the biggest coin you can."
             % (C(target), cap(andw(f)), "uses" if len(f) == 1 else "use", ncoins(len(f))))
        its.append(mcq("Which uses the fewest coins to make %s?" % C(target), words(f), [words(x) for x in wrong], e))

    how_few(15, [3, 1, 15], "Three nickels work, but that is 3 coins. 15 coins counts cents, not coins.")
    how_few(20, [4, 1, 3], "Four nickels work, but 2 dimes is fewer.")
    which_fewest(25, [[10, 10, 5], [5] * 5, [10, 5, 5, 5]])
    how_few(30, [3, 1, 6], "There is no 30¢ coin. Three dimes work, but 2 coins is fewer.")
    how_few(35, [3, 4, 7], "Three dimes and a nickel work, but that is 4 coins.")
    how_few(40, [4, 2, 8], "Four dimes work, but a quarter, a dime and a nickel is only 3 coins.")
    which_fewest(45, [[10, 10, 10, 10, 5], [25, 10, 5, 5], [25, 5, 5, 5, 5]])
    how_few(50, [5, 3, 10], "Five dimes work, but 2 quarters is fewer.")
    how_few(55, [4, 2, 6], "Two coins make only 50¢. You need 1 more coin, a nickel.")
    how_few(60, [6, 4, 2], "Six dimes work, but that is 6 coins.")
    which_fewest(65, [[25, 10, 10, 10, 10], [25, 25, 5, 5, 5], [10] * 6 + [5]])
    how_few(70, [7, 3, 5], "Seven dimes work, but that is 7 coins. Three coins can make 60¢ or 75¢, but not 70¢.")
    how_few(75, [4, 7, 2], "Seven dimes and a nickel work, but that is 8 coins. 4 is right only if a quarter were 20¢.")
    which_fewest(80, [[25, 25, 10, 10, 10], [10] * 8, [25, 25, 10, 10, 5, 5]])
    how_few(85, [5, 3, 8], "Three quarters make 75¢. Add 1 dime: 85¢. Without quarters you need many more coins.")
    which_fewest(90, [[25, 25, 10, 10, 10, 10], [25, 25, 25, 5, 5, 5], [10] * 9])
    how_few(95, [4, 6, 9], "Three quarters make 75¢. Add 2 dimes: 85¢, 95¢.")
    how_few(100, [10, 5, 1], "Ten dimes work, but that is 10 coins. A loonie is 1 coin, but this time you have no loonie.",
            coins=[5, 10, 25], stem="You have no loonie. What is the smallest number of coins you can use to make %s?")
    which_fewest(100, [[25] * 4, [10] * 10, [25, 25, 10, 10, 10, 10, 10]])
    its.append(mcq("You want to make 70¢ with the fewest coins. Which coin do you use first?",
                   "a quarter", ["a nickel", "a dime", "a loonie"],
                   "Use the biggest coin that is not more than 70¢. A loonie is 100¢, too much. "
                   "So start with <b>a quarter</b>: 25¢, 50¢, then 2 dimes: 60¢, 70¢."))
    assert len(its) == 20
    return {"title": "Use the fewest coins", "items": its}


# ============================================================ set 5: spending, saving and word problems
SNACKS = [("apple", 35), ("granola bar", 45), ("juice box", 50), ("freezie", 25)]


def set_words(P, rnd):
    its = []

    def add(q, right, cands, e, fmt=C):
        its.append(mcq(q, right, cands, e, fmt))

    add("What does <b>saving</b> money mean?", "keeping it to use later",
        ["spending it all now", "counting the coins", "giving it to a store"],
        "Saving means <b>keeping money to use later</b>, so you can buy something you want.", str)
    nm, he, his = P.next()
    add("%s’s saving goal is $1. How many cents is that?" % nm, 100, [1, 10, 200],
        "$1 = <b>100¢</b>. That is the same as 4 quarters or 10 dimes.")
    nm, he, his = P.next()
    assert 100 - 60 == 40
    add(fig(goal_svg(60)) + "%s is saving for a $1 goal. %s has 60¢. How much more does %s need?" % (nm, cap(he), he),
        40, [160, 50, 60],
        "Count up from 60¢: 70¢, 80¢, 90¢, 100¢. That is 4 tens. %s needs <b>40¢</b> more. "
        "160¢ adds instead of finding the difference." % cap(he))
    nm, he, his = P.next()
    toks = toks_of(("Q", 2), ("D", 2))
    assert total(toks) == 70 and m_quarter20(toks) == 60
    add(fig(money_svg(toks)) + "%s is saving for a $1 goal. %s has these coins. How much more does %s need?" % (nm, cap(he), he),
        30, [40, 70, 170],
        "Count: 25¢, 50¢, 60¢, 70¢. %s has 70¢. 70¢ + 30¢ = 100¢, so %s needs <b>30¢</b> more. "
        "40¢ comes from counting a quarter as 20¢." % (nm, he))
    nm, he, his = P.next()
    add("%s saves 1 quarter each week. How many weeks until %s has $1?" % (nm, he), "4 weeks",
        ["5 weeks", "25 weeks", "3 weeks"],
        "25¢, 50¢, 75¢, 100¢. After <b>4 weeks</b> %s has $1. 5 weeks comes from counting a quarter as 20¢." % he, str)
    nm, he, his = P.next()
    add("%s saves 1 dime each day. How many days until %s has $1?" % (nm, he), "10 days",
        ["100 days", "1 day", "5 days"],
        "Count by 10s: 10¢, 20¢ … 100¢. That is <b>10 days</b>. 5 days would give only 50¢.", str)
    nm, he, his = P.next()
    assert 80 - 35 == 45 and m_digits(80, 35) == 55
    add("%s has 80¢. %s spends 35¢ on a freezie. How much does %s have left?" % (nm, cap(he), he), 45, [115, 55, 35],
        "80¢ − 35¢: 80¢ − 30¢ = 50¢. 50¢ − 5¢ = <b>45¢</b>. Check: 35¢ + 45¢ = 80¢. "
        "55¢ comes from taking 0 − 5 as 5. 115¢ adds instead of taking away.")
    nm, he, his = P.next()
    add("%s has 100¢. %s is saving it for a $1 comic book. If %s spends 50¢ on gum today, can %s still buy the comic book?"
        % (nm, cap(he), he, he),
        "No, %s will have only 50¢." % he,
        ["Yes, %s still has 100¢." % he, "Yes, 50¢ is enough.", "No, %s will have 0¢." % he],
        "100¢ − 50¢ = 50¢. The comic book costs 100¢, so <b>no, %s will have only 50¢</b>. "
        "Spending now means less for the goal." % he, str)
    sp = dict(SNACKS)
    nm, he, his = P.next()
    assert sp["granola bar"] + sp["freezie"] == 70
    add(fig(price_svg(SNACKS, "field trip snacks")) + "%s buys a granola bar and a freezie. How much does %s spend?" % (nm, he),
        70, [20, 60, 80],
        "45¢ + 25¢: 40¢ + 20¢ = 60¢. 5¢ + 5¢ = 10¢. 60¢ + 10¢ = <b>70¢</b>. "
        "60¢ forgets the extra 10¢. 20¢ is the difference, not the total.")
    nm, he, his = P.next()
    sums = {(a, b): sp[a] + sp[b] for a in sp for b in sp if a < b}
    assert [k for k, v in sums.items() if v == 75] == [("freezie", "juice box")]
    add(fig(price_svg(SNACKS, "field trip snacks")) + "%s has 75¢. Which two snacks cost exactly 75¢?" % nm,
        "juice box and freezie", ["apple and granola bar", "apple and freezie", "granola bar and juice box"],
        "Juice box and freezie: 50¢ + 25¢ = <b>75¢</b>. Apple and granola bar make 80¢. "
        "Apple and freezie make 60¢. Granola bar and juice box make 95¢.", str)
    nm, he, his = P.next()
    toks = toks_of(("Q", 1), ("D", 3), ("N", 1))
    assert total(toks) == 60 and m_quarter20(toks) == 55
    add(fig(money_svg(toks)) + "%s has these coins. A juice box costs 50¢. Can %s buy it?" % (nm, he),
        "Yes, with 10¢ left.", ["No, %s needs 10¢ more." % he, "Yes, with 5¢ left.", "Yes, %s has exactly 50¢." % he],
        "Count: 25¢, 35¢, 45¢, 55¢, 60¢. %s has 60¢. 60¢ − 50¢ = 10¢, so <b>yes, with 10¢ left</b>. "
        "5¢ left comes from counting the quarter as 20¢." % nm, str)
    nm, he, his = P.next()
    add("For the Terry Fox Run, %s gives 3 quarters. How much does %s give?" % (nm, he), 75, [3, 60, 100],
        "Count by 25s: 25¢, 50¢, 75¢. %s gives <b>75¢</b>. 60¢ counts a quarter as 20¢. 3¢ counts the coins." % nm)
    nm, he, his = P.next()
    add("At %s’s lemonade stand, a cup costs 20¢. %s sells 4 cups. How much money does %s get?" % (nm, cap(he), he),
        80, [24, 60, 100],
        "Count by 20s: 20¢, 40¢, 60¢, 80¢. 4 cups make <b>80¢</b>. 24¢ adds 20 + 4. 60¢ is only 3 cups.")
    nm, he, his = P.next()
    assert 45 + 50 == 95 and 45 + 40 == 85
    add("%s has saved 45¢. %s grandpa gives %s 2 quarters. Does %s reach %s $1 goal?" % (nm, cap(his), "her" if he == "she" else "him", he, his),
        "No, %s needs 5¢ more." % he,
        ["Yes, %s has exactly $1." % he, "Yes, with 5¢ extra.", "No, %s needs 15¢ more." % he],
        "2 quarters are 50¢. 45¢ + 50¢ = 95¢. 95¢ + 5¢ = 100¢, so <b>no, %s needs 5¢ more</b>. "
        "15¢ more comes from counting a quarter as 20¢." % he, str)
    nm, he, his = P.next()
    assert 40 + 3 * 20 == 100
    add("%s wants a $1 bouncy ball. %s has 40¢. %s saves 20¢ each week. How many weeks until %s has $1?"
        % (nm, cap(he), cap(he), he),
        "3 weeks", ["5 weeks", "2 weeks", "4 weeks"],
        "Count on by 20s from 40¢: 60¢, 80¢, 100¢. That is <b>3 weeks</b>. "
        "5 weeks forgets the 40¢ %s already has." % he, str)
    nm, he, his = P.next()
    assert 100 - 65 == 35
    add("%s has a loonie. %s spends 65¢ at the school bake sale. How much is left?" % (nm, cap(he)), 35, [45, 165, 25],
        "A loonie is 100¢. Count up from 65¢: 70¢ is 5¢, then 100¢ is 30¢ more. 5¢ + 30¢ = <b>35¢</b>. "
        "45¢ is a regrouping mistake. 165¢ adds instead of taking away.")
    nm, he, his = P.next()
    add("%s saves 1 dime every day for 7 days. How much has %s saved?" % (nm, he), 70, [7, 35, 17],
        "Count by 10s: 10¢, 20¢, 30¢, 40¢, 50¢, 60¢, 70¢. %s has <b>70¢</b>. "
        "35¢ counts the dimes as nickels. 7¢ counts the coins." % cap(he))
    nm, he, his = P.next()
    assert 85 - 25 == 60 and 100 - 60 == 40
    add(fig(goal_svg(85)) + "%s has 85¢ for a $1 goal. %s spends 25¢ on a treat. How much more does %s need now?"
        % (nm, cap(he), he),
        40, [15, 60, 35],
        "85¢ − 25¢ = 60¢. From 60¢ to 100¢ is <b>40¢</b>. Before the treat, %s needed only 15¢. "
        "Spending moves you away from your goal." % he)
    nm, he, his = P.next()
    assert 90 - 55 == 35 and m_digits(90, 55) == 45
    add("On a class trip to the Vancouver Aquarium, %s has 90¢ for the gift shop. %s buys a pencil for 55¢. "
        "How much is left?" % (nm, cap(he)), 35, [145, 45, 25],
        "90¢ − 55¢: 90¢ − 50¢ = 40¢. 40¢ − 5¢ = <b>35¢</b>. Check: 55¢ + 35¢ = 90¢. "
        "45¢ comes from taking 0 − 5 as 5. 145¢ adds instead of taking away.")
    nm, he, his = P.next()
    toks = toks_of(("Q", 3), ("D", 1), ("N", 2))
    assert total(toks) == 95 and m_quarter20(toks) == 80
    add(fig(money_svg(toks)) + "%s is saving for a $1 kite. %s has these coins. How much more does %s need?" % (nm, cap(he), he),
        5, [20, 95, 15],
        "Count: 25¢, 50¢, 75¢, 85¢, 90¢, 95¢. %s has 95¢. 95¢ + 5¢ = 100¢, so %s needs <b>5¢</b> more. "
        "20¢ comes from counting a quarter as 20¢." % (nm, he))
    assert len(its) == 20
    return {"title": "Spending, saving and word problems", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["N", "D", "Q", "L", "T"]
    walk = toks_of(("Q", 2), ("D", 1), ("N", 1))
    assert total(walk) == 65
    return (
        "<h2>Canadian coins</h2>"
        "<p>Learn the name and the value of each coin. Size does not tell you the value. "
        "The dime is the smallest coin, but it is worth more than the nickel.</p>"
        "<figure class='sn-fig'>" + money_svg(coins, per_row=5, gap=8, under=["nickel", "dime", "quarter", "loonie", "toonie"],
                                              label="Canadian coins: nickel 5¢, dime 10¢, quarter 25¢, loonie $1, toonie $2") +
        "<figcaption>Nickel 5¢, dime 10¢, quarter 25¢, loonie $1 (100¢), toonie $2. There are no pennies.</figcaption></figure>"
        + table(["Coin", "Value", "Good to know"], [
            ["nickel", "5¢", "2 nickels = 1 dime"],
            ["dime", "10¢", "10 dimes = 100¢"],
            ["quarter", "25¢", "4 quarters = 100¢"],
            ["loonie", "$1 = 100¢", "11 sides, gold colour"],
        ]) +
        "<h2>Count the coins, biggest first</h2>"
        "<p>Put the coins in order, biggest value first. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=10, under=["25¢", "50¢", "60¢", "65¢"],
                                              label="counting on: 25¢, 50¢, 60¢, 65¢") +
        "<figcaption>Quarters: 25¢, 50¢. Dime: 60¢. Nickel: 65¢.</figcaption></figure>"
        + ex("Example", "Count 3 quarters and 2 dimes.", "25¢, 50¢, 75¢, then 85¢, 95¢.", "95¢")
        + "<h2>The same amount in different ways</h2>"
        "<p>50¢ can be 2 quarters, or 5 dimes, or 1 quarter, 2 dimes and 1 nickel. "
        "100¢ can be 1 loonie, 4 quarters or 10 dimes.</p>"
        "<p>For the <b>fewest coins</b>, use the biggest coin you can each time. "
        "30¢ is 1 quarter and 1 nickel: only 2 coins.</p>"
        + ex("Example", "Show 75¢ in two ways.", "3 quarters: 25¢, 50¢, 75¢. Or 7 dimes and 1 nickel: 70¢, 75¢.",
             "3 quarters, or 7 dimes and 1 nickel")
        + "<h2>Spending and saving</h2>"
        "<p>Spending means using money to buy something now. Saving means keeping money to use later. "
        "A saving goal tells you how much you need. To find how much more you need, count up to the goal.</p>"
        "<figure class='sn-fig'>" + goal_svg(70) +
        "<figcaption>70¢ saved. Count up: 80¢, 90¢, 100¢. 30¢ more reaches the $1 goal.</figcaption></figure>"
        + ex("Example", "Kai has 60¢ for a $1 goal. He spends 20¢ on a sticker. How much more does he need now?",
             "60¢ − 20¢ = 40¢. From 40¢ to 100¢ is 60¢.", "60¢")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["4 coins, so 4¢", "Count the value of each coin: 25¢, 50¢, 60¢, 65¢"],
            ["A quarter is 20¢", "A quarter is 25¢. Four quarters make 100¢"],
            ["The nickel is bigger, so it is worth more", "The small dime is 10¢. The nickel is 5¢"],
            ["Start with the small coins", "Start with the biggest coin, then count on"],
            ["Add to find how much more you need", "Count up from what you have to the goal"],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about money in BC?",
     "a": "The BC Grade 2 math curriculum lists “coin combinations to 100 cents, and spending and saving” under Financial literacy. Students count nickels, dimes, quarters and loonies to 100¢, make the same amount in different ways and talk about spending and saving."},
    {"q": "How do I help my child count coins?",
     "a": "Sort the coins and start with the biggest value, then count on: 25¢, 50¢, 60¢, 65¢. Use real coins at home and say the value of each one, not just the number of coins."},
    {"q": "Why are there no pennies in Canada?",
     "a": "Canada stopped giving out pennies in 2013. Cash totals are rounded to the nearest 5¢, so the nickel is the smallest coin children count."},
    {"q": "How can I teach my child about saving money?",
     "a": "Choose a small goal, like $1 for a toy, and use a jar or piggy bank. Each week, count the coins together and ask how much more is needed to reach the goal."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=xmlns='[^']*' viewBox='0 0 (?:[2-9]\d\d|\d{4}) [^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(52812)
    P = People(rnd)
    sets = [set_values(P, rnd), set_count(P, rnd), set_ways(P, rnd), set_fewest(P, rnd), set_words(P, rnd)]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-2", "slug": "coins-to-100-cents", "sort": 12,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 2 Money: Coins to 100¢, Spending and Saving",
        "seo_title": "Grade 2 Money Worksheets: Canadian Coins to 100¢, Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Coins to 100¢",
        "domain": "Financial literacy",
        "standard_code": "Grade 2: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/2/core",
        "standard_text": "Financial literacy – coin combinations to 100 cents, and spending and saving",
        "meta_desc": "Free Grade 2 math worksheets on Canadian coins for the BC curriculum: learn coin values, count nickels, dimes, quarters and loonies to 100¢, make the same amount in different ways, use the fewest coins and save for a $1 goal. 100 questions with an answer key.",
        "key_big": "Count coins by value, not by the number of coins.",
        "key_sub": "Start with the biggest coin and count on: 25¢, 50¢, 60¢, 65¢. A quarter is 25¢, not 20¢. To reach a $1 goal, count up to 100¢.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(money|counting|price|savings)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
