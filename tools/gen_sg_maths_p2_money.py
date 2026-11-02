# -*- coding: utf-8 -*-
"""
SG Primary 2 Maths: Money (MOE 2021 Primary Mathematics Syllabus, Standard Mathematics, Primary 2: Money)
  python3 tools/gen_sg_maths_p2_money.py
Counting money in dollars and cents, decimal notation ($3.05), comparing amounts,
converting dollars and cents to cents only and back ($2.40 = 240¢), and word problems at the school canteen
(adding and subtracting in dollars only or cents only), with bar models.
Singapore coins 5¢, 10¢, 20¢, 50¢, $1 and notes $2, $5, $10, drawn as simple labelled shapes (no real artwork).
All amounts are whole numbers of cents (int); every answer and every wrong answer is computed and checked in code.
Wrong answers come from real mistakes: $3.5 for $3.05, 240¢ = $24.0, counting coins instead of their value,
missing or double-counting one coin, no decimal point ($305), adding when the question takes away,
taking the smaller digit from the bigger one in each place, and forgetting to rename.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are adapted from gen_cabc_math_g2_money.py, gen_uk_maths_y2_money.py and gen_sg_maths_p3_add_sub.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
PARTFILL = "#fde3c8"
INK = "#2b2b2b"
RED = "#c0392b"
ORANGE = "#b35900"
NB = " "
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]

# ------------------------------------------------------------ money facts
ORDER = ["N10", "N5", "N2", "C100", "C50", "C20", "C10", "C5"]   # biggest value first
VAL = {"N10": 1000, "N5": 500, "N2": 200, "C100": 100, "C50": 50, "C20": 20, "C10": 10, "C5": 5}
BYVAL = {v: k for k, v in VAL.items()}
SILVER = ("#dfe3e7", "#7a828a")
GOLD = ("#f1d77a", "#9a7a1c")
# radius, (fill, edge), label size  (in proportion to the real coins: 5¢ 16.75 mm ... $1 24.65 mm)
COIN = {"C5": (17, GOLD, 14), "C10": (19, SILVER, 14), "C20": (21, SILVER, 15), "C50": (23, SILVER, 15),
        "C100": (25, GOLD, 16)}
NOTE = {"N2": ("#dccbef", "#5b3a8a"), "N5": ("#c9e8c4", "#2e6b28"), "N10": ("#f6c9c4", "#a1302a")}
NOTE_W, NOTE_H = 80, 42


def lab(v):
    """label on a coin or note: $1, $2 ... or 5¢ ... 50¢"""
    return "$%d" % (v // 100) if v >= 100 else "%d¢" % v


def c(v):
    """cents only: 240 -> '240¢'"""
    assert isinstance(v, int) and v > 0, v
    return "%d¢" % v


def d(v):
    """decimal notation: 305 -> '$3.05', 500 -> '$5', 85 -> '$0.85'"""
    assert isinstance(v, int) and v > 0, v
    if v % 100 == 0:
        return "$%d" % (v // 100)
    return "$%d.%02d" % (v // 100, v % 100)


def d2(v):
    """always two decimal places: 800 -> '$8.00'"""
    return "$%d.%02d" % (v // 100, v % 100)


def dc(v):
    """dollars and cents in words: 370 -> '$3 and 70¢'"""
    assert v % 100 and v > 100
    return "$%d and %d¢" % (v // 100, v % 100)


def mval(s):
    """value in cents of a money text, or None. '$3.5' (a common mistake) is read as 350."""
    s = re.sub(r"<[^>]+>", "", s).strip()
    m = re.match(r"^\$(\d+)$", s)
    if m:
        return int(m.group(1)) * 100
    m = re.match(r"^\$(\d+)\.(\d+)$", s)
    if m:
        f = m.group(2)
        assert len(f) <= 2, s
        return int(m.group(1)) * 100 + int((f + "0")[:2])
    m = re.match(r"^(\d+)¢$", s)
    if m:
        return int(m.group(1))
    m = re.match(r"^\$(\d+) and (\d+)¢$", s)
    if m:
        return int(m.group(1)) * 100 + int(m.group(2))
    return None


def total(toks):
    return sum(VAL[t] for t in toks)


def srt(toks):
    return sorted(toks, key=ORDER.index)


def toks_of(*pairs):
    out = []
    for t, n in pairs:
        out += [BYVAL[t]] * n
    return srt(out)


def counts(toks):
    return [(t, toks.count(t)) for t in ORDER if t in toks]


def kinds(toks):
    return [t for t, n in counts(toks)]


def cap(s):
    return s[0].upper() + s[1:]


def fmt_amt(v):
    return c(v) if v < 100 else d(v)


def count_on(toks):
    toks = srt(toks)
    s, run = 0, []
    for t in toks:
        s += VAL[t]
        run.append(fmt_amt(s))
    if len(set(toks)) == 1:
        t = toks[0]
        return "Count in steps of %s: %s. That is <b>%s</b>." % (lab(VAL[t]), ", ".join(run), run[-1])
    return "Start with the biggest note or coin and count on: %s. That is <b>%s</b>." % (", ".join(run), run[-1])


def m_skip(toks, k=-1):
    return total(toks) - VAL[kinds(toks)[k]]


def m_twice(toks, k=-1):
    return total(toks) + VAL[kinds(toks)[k]]


def m_digits(a, b):
    """a − b, taking the smaller digit from the bigger one in each place (no renaming)"""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def no_point(v):
    """$3.05 written without the point: '$305'"""
    return "$%d" % v


# ------------------------------------------------------------ helpers
def mcq(q, right, wrongs, e):
    """4 choices: right + the first 3 usable unique wrong answers (never equal in value to another choice)."""
    right = str(right)
    seen_t = {right}
    seen_v = {mval(right)} - {None}
    pick = []
    for w in wrongs:
        if w is None:
            continue
        w = str(w)
        v = mval(w)
        if w in seen_t or (v is not None and v in seen_v) or v == 0:
            continue
        seen_t.add(w)
        if v is not None:
            seen_v.add(v)
        pick.append(w)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, wrongs)
    return {"q": q, "c": [right] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            ch = it["c"]
            right = ch[it["a"]]
            wrong = [x for i, x in enumerate(ch) if i != it["a"]]
            rnd.shuffle(wrong)
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


def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: " + NB:
            w += 0.3
        elif ch in "l1i":
            w += 0.32
        elif ch.isupper() or ch in "$¢?mw":
            w += 0.72
        else:
            w += 0.58
    return w * fs


# ------------------------------------------------------------ pictures
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
    if t == "C100":     # $1: gold centre, silver ring
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, SILVER[0], SILVER[1])
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r - 6, fill, edge))
    else:
        shape = ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, r, fill, edge)
                 + "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (cx, cy, r - 3, edge))
    return shape + text(cx, cy + fs * 0.36, lab(VAL[t]), fs)


def group(toks):
    return ", ".join("%d × %s" % (n, lab(VAL[t])) if n > 1 else lab(VAL[t]) for t, n in counts(toks))


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None):
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)
    rows = [toks[i:i + per] for i in range(0, len(toks), per)]
    lab_h = 22 if under else 0
    cw = lambda t: max(tok_size(t)[0], 60 if under else 0)
    widths = [sum(cw(t) for t in r) + gap * (len(r) - 1) for r in rows]
    heights = [max(tok_size(t)[1] for t in r) + lab_h for r in rows]
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(rows) - 1) + 2 * pad
    s, y, k = [], pad, 0
    for r, rh in zip(rows, heights):
        x = pad
        hh = rh - lab_h
        for t in r:
            w = cw(t)
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
    return svg_wrap(w + 8, h + 8, draw_tok(t, (w + 8) / 2, (h + 8) / 2), "one %s %s" % (lab(VAL[t]), word))


def shuffled(toks, rnd):
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


def compare_svg(people):
    """two rows of money, each with a name on the left: [(name, toks), (name, toks)]"""
    pad, gap, rgap = 6, 8, 12
    LW = int(max(tw(n, 16) for n, _ in people)) + 14
    rows_w = [sum(tok_size(t)[0] for t in tk) + gap * (len(tk) - 1) for _, tk in people]
    rows_h = [max(tok_size(t)[1] for t in tk) for _, tk in people]
    W = pad + LW + max(rows_w) + pad
    H = pad * 2 + sum(rows_h) + rgap * (len(people) - 1)
    s, y = [], pad
    for (nm, tk), rh in zip(people, rows_h):
        s.append(text(pad + LW - 12, y + rh / 2 + 6, nm, 16, anchor="end"))
        x = pad + LW
        for t in tk:
            w, h = tok_size(t)
            s.append(draw_tok(t, x + w / 2, y + rh / 2))
            x += w + gap
        y += rh + rgap
    if len(people) > 1:
        ym = pad + rows_h[0] + rgap / 2
        s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='#b9c2bc' stroke-width='1'/>" % (pad, ym, W - pad, ym))
    return svg_wrap(int(W), int(H), "".join(s), "money of " + " and ".join("%s: %s" % (n, group(tk)) for n, tk in people))


def price_svg(items, title):
    """a row of price tags: [('curry puff', '60¢'), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(int(tw(n, 15)) + 18, 76) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, p, 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, p) for n, p in items))


def brace(x1, x2, y, up, lab_, col=INK):
    dd = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + dd, x1, y, x2, y, x2, y + dd, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab_, 16, col=col))
    return "".join(o)


def bar_parts(parts_, total_lab, BW=360, fills=None):
    """One bar split into parts drawn to scale. parts_ = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(v for v, _ in parts_)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = fills or [FILL, PARTFILL, "#fff"]
    for i, (v, lab_) in enumerate(parts_):
        w = float(v) / tot * BW
        assert tw(lab_, 16) <= w - 6, (lab_, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % len(fills)], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab_, 16, col=RED if lab_ == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts_), total_lab))


def bar_units(n, unit_lab, total_lab, BW=360):
    """n equal units, each labelled, bracket below with the total."""
    return bar_parts([(1, unit_lab)] * n, total_lab, BW, fills=[FILL]).replace(
        "aria-label='bar model: parts", "aria-label='bar model: %d equal units, parts" % n, 1)


def bar_compare(rows, diff_lab, BW=300):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lab_, fl) in enumerate([(n1, BW, l1, FILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab_, 16) <= w - 6, (lab_, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fl, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab_, 16, col=RED if lab_ == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab_ = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lab_)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ============================================================ set 1: count coins and notes
def set_count(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    s(fig(coin_svg("C20")) + "How much is this coin worth?", "20¢", ["$20", "10¢", "50¢"],
      "The coin says 20¢. It is worth <b>20¢</b> (20 cents). $20 would be 20 dollars.")
    s(fig(coin_svg("C100")) + "How much is this coin worth?", "$1", ["1¢", "10¢", "$10"],
      "The coin says $1. It is worth <b>$1</b> (1 dollar). 1 dollar is the same as 100¢.")
    s(fig(coin_svg("N5")) + "How much is this note worth?", "$5", ["5¢", "50¢", "$50"],
      "The note says $5. It is worth <b>$5</b> (5 dollars).")
    s("Which of these is a note?", "$10", ["$1", "50¢", "20¢"],
      "Our notes are $2, $5 and $10. So <b>$10</b> is a note. $1, 50¢ and 20¢ are coins.")
    assert 10 * 10 == 100 and 5 * 20 == 100
    s("How many 10¢ coins make $1?", "10", ["100", "1", "5"],
      "$1 = 100¢. Count in tens: 10¢, 20¢, 30¢ … 100¢. That is <b>10</b> coins.")
    s("How many $2 notes make $10?", "5", ["2", "10", "8"],
      "Count in twos: $2, $4, $6, $8, $10. That is <b>5</b> notes. 8 comes from 10 − 2.")

    groups = [
        ([(10, 4)], False), ([(20, 3)], False), ([(50, 1), (20, 1), (10, 1)], False),
        ([(50, 1), (10, 2), (5, 1)], True), ([(20, 2), (10, 1), (5, 2)], True), ([(50, 1), (20, 2), (5, 1)], True),
    ]
    stems = ["How much money is this?", "%s has these coins. How much does %s have?", "What is the total?",
             "%s finds these coins in %s pencil case. How much is it?", "How much money is this?",
             "%s puts these coins in a money box. How much is in the box?"]
    for i, (g, mixed) in enumerate(groups):
        toks = toks_of(*g)
        T = total(toks)
        assert T < 100
        nm, he, his = P.next()
        st = stems[i]
        if "pencil case" in st:
            st = st % (nm, his)
        elif st.count("%s") == 2:
            st = st % (nm, he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if mixed else toks
        e = ("Put the coins in order, biggest first. " if mixed else "") + count_on(toks)
        cands = [len(toks), m_skip(toks, -1), m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
        it = mcq(fig(money_svg(shown)) + st, c(T), [c(x) for x in cands], e)
        if c(len(toks)) in it["c"]:
            it["e"] += " %s counts the coins, not their value." % c(len(toks))
        its.append(it)

    right = [20, 20, 10]
    wrong = [[20, 20, 5], [10, 10, 10], [20, 10, 10, 10, 5]]
    assert sum(right) == 50 and len({sum(w) for w in wrong} | {50}) == 4
    s("Which coins make 50¢?", "20¢, 20¢, 10¢", [", ".join("%d¢" % x for x in w) for w in wrong],
      "20¢ + 20¢ + 10¢: 20¢, 40¢, <b>50¢</b>. The others make 45¢, 30¢ and 55¢.")

    notes = [
        [(200, 3)], [(500, 1), (200, 2)], [(1000, 1), (500, 1), (100, 1)],
        [(1000, 2), (500, 1), (200, 1)], [(500, 2), (200, 1), (100, 2)],
    ]
    nstems = ["How much money is this?", "%s has these notes. How much does %s have?", "What is the total?",
              "%s gets these notes in red packets. How much is it?", "How much money is this?"]
    for i, g in enumerate(notes):
        toks = toks_of(*g)
        T = total(toks)
        nm, he, his = P.next()
        st = nstems[i]
        if st.count("%s") == 2:
            st = st % (nm, he)
        elif "%s" in st:
            st = st % nm
        shown = shuffled(toks, rnd) if i >= 3 else toks
        e = ("Put them in order, biggest first. " if i >= 3 else "") + count_on(toks)
        cands = [100 * len(toks), m_skip(toks, -1), m_twice(toks, -1), m_skip(toks, 0), m_twice(toks, 0)]
        it = mcq(fig(money_svg(shown)) + st, d(T), [d(x) for x in cands], e)
        if d(100 * len(toks)) in it["c"]:
            it["e"] += " %s counts the %s, not their value." % (
                d(100 * len(toks)), "notes" if all(t.startswith("N") for t in toks) else "notes and coins")
        its.append(it)

    toks = toks_of((200, 1), (100, 1), (50, 1), (20, 1))
    T = total(toks)
    assert T == 370
    s(fig(money_svg(shuffled(toks, rnd))) + "How much money is this?", dc(T),
      [dc(T - 20), dc(T - 100), dc(T + 100)],
      "Dollars first: $2 + $1 = $3. Then cents: 50¢ + 20¢ = 70¢. That is <b>$3 and 70¢</b>.")
    s(fig(money_svg(["C20", "C5", "C50", "C10"], gap=12, label="coins 20¢, 5¢, 50¢ and 10¢"))
      + "Which coin is worth the least?", "5¢", ["10¢", "20¢", "50¢"],
      "5¢ is less than 10¢, 20¢ and 50¢. The <b>5¢</b> coin is worth the least.")
    assert len(its) == 20
    return {"title": "Count coins and notes", "items": its}


# ============================================================ set 2: decimal notation
def set_decimal(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    def write(v, wrongs, extra=""):
        dl, ct = v // 100, v % 100
        e = ("Write the dollars, then a point, then the cents with 2 digits: <b>%s</b>." % d(v))
        if ct < 10:
            e += " %d¢ is written as 0%d after the point." % (ct, ct)
        s("How do you write $%d and %d¢ with a point?" % (dl, ct), d(v), wrongs, e + extra)

    write(235, [no_point(235), "$2.53", "$0.35"], " $235 has no point. $0.35 forgets the $2.")
    write(450, ["$4.05", no_point(450), "$0.50"], " $4.05 would be $4 and 5¢.")
    write(305, ["$3.5", no_point(305), "$5.03"], " $3.5 means $3.50, which is $3 and 50¢.")
    write(110, ["$1.01", no_point(110), "$11"], " $1.01 would be $1 and 1¢.")
    write(675, [no_point(675), "$6.57", "$0.75"], " $675 has no point.")
    write(905, ["$9.5", no_point(905), "$95"], " $9.5 means $9.50, which is $9 and 50¢.")
    write(1020, ["$10.02", no_point(1020), "$12"], " $12 adds 10 and 2.")
    s("Write 8 dollars 60 cents in dollars.", "$8.60", ["$8.06", "$86", "$860"],
      "8 dollars, a point, then 60 cents: <b>$8.60</b>. $8.06 would be 8 dollars 6 cents.")
    s("Write 5 dollars 15 cents in dollars.", "$5.15", ["$515", "$15.05", "$5.51"],
      "5 dollars, a point, then 15 cents: <b>$5.15</b>.")
    s("How do you read $6.20?", "6 dollars 20 cents", ["6 dollars 2 cents", "62 dollars", "20 dollars 6 cents"],
      "The number before the point is the dollars. The 2 digits after it are the cents. "
      "$6.20 is <b>6 dollars 20 cents</b>.")
    s("$4.08 is 4 dollars and ___ cents.", "8", ["80", "48", "408"],
      "The 2 digits after the point are 08. That is <b>8</b> cents. 80 cents would be $4.80.")
    s("$7.40 is ___ dollars and 40 cents.", "7", ["74", "4", "740"],
      "The number before the point is the dollars: <b>7</b>.")

    pics = [
        ([(200, 1), (50, 1), (20, 1)], ["NP", "SKIP", "NODOL"]),
        ([(500, 1), (100, 1), (10, 1), (5, 1)], ["NP", "ONECENT", "SKIP"]),
        ([(200, 1), (5, 1)], ["POINT5", "NP", "FIVEDOL"]),
        ([(1000, 1), (200, 1), (20, 2), (5, 1)], ["NP", "SKIP", "SKIP0"]),
        ([(500, 1), (200, 1), (10, 1)], ["SWAP0", "NP", "SKIP0"]),
        ([(100, 2), (50, 1), (5, 1)], ["NP", "SKIP", "SKIP0"]),
    ]
    stems = ["Write this amount in dollars.", "%s has this money. How much is it in dollars?",
             "Write this amount in dollars.", "%s saved this money. How much is it in dollars?",
             "How much money is this? Write it in dollars.", "%s finds these coins. How much is it in dollars?"]
    for i, (g, kinds_) in enumerate(pics):
        toks = toks_of(*g)
        T = total(toks)
        dl, ct = T // 100, T % 100
        st = stems[i]
        if "%s" in st:
            st = st % P.next()[0]
        wr, notes = [], []
        for k in kinds_:
            if k == "NP":
                wr.append(no_point(T)); notes.append("%s has no point." % no_point(T))
            elif k == "SKIP":
                wr.append(d(m_skip(toks, -1))); notes.append("%s misses the %s coin." % (wr[-1], lab(VAL[kinds(toks)[-1]])))
            elif k == "SKIP0":
                k0 = kinds(toks)[0]
                wr.append(d(m_skip(toks, 0)))
                notes.append("%s misses the %s %s." % (wr[-1], lab(VAL[k0]), "note" if k0.startswith("N") else "coin"))
            elif k == "NODOL":
                wr.append(d(ct)); notes.append("%s forgets the dollars." % d(ct))
            elif k == "ONECENT":
                v = T - 100 + 1
                wr.append(d(v)); notes.append("%s takes the $1 coin as 1¢." % d(v))
            elif k == "POINT5":
                wr.append("$%d.%d" % (dl, ct)); notes.append("$%d.%d means $%d.%d0." % (dl, ct, dl, ct))
            elif k == "FIVEDOL":
                wr.append(d(dl * 100 + ct * 100)); notes.append("%s takes the 5¢ coin as $5." % wr[-1])
            elif k == "SWAP0":
                wr.append("$%d.0%d" % (dl, ct // 10)); notes.append("%s would be $%d and %d¢." % (wr[-1], dl, ct // 10))
        dol = sum(VAL[t] for t in toks if VAL[t] >= 100) // 100
        e = ("Dollars: $%d. Cents: %d¢. Write <b>%s</b>. " % (dol, ct, d(T))) + " ".join(notes)
        it = mcq(fig(money_svg(shuffled(toks, rnd) if i % 2 else toks)) + st, d(T), wr, e)
        its.append(it)

    s("Which is the correct way to write 3 dollars 9 cents?", "$3.09", ["$3.9", "$39", "$309"],
      "Cents always take 2 digits after the point. 9 cents is 09. So it is <b>$3.09</b>. $3.9 means $3.90.")
    nm, he, his = P.next()
    s("%s writes $5.7 for 5 dollars 7 cents. What should %s write?" % (nm, he), "$5.07", ["$5.70", "$57", "$507"],
      "7 cents is 07 after the point: <b>$5.07</b>. $5.7 is the same as $5.70, which is 5 dollars 70 cents.")
    assert len(its) == 20
    return {"title": "Write money in decimal notation", "items": its}


# ============================================================ set 3: dollars and cents <-> cents
def set_convert(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    def to_c(v, wrongs, extra=""):
        s("%s = ___" % d(v), c(v), wrongs,
          "$1 = 100¢. %s is $%d and %d¢: %d¢ + %d¢ = <b>%s</b>.%s"
          % (d(v), v // 100, v % 100, (v // 100) * 100, v % 100, c(v), extra)
          if v % 100 else ("1 dollar is 100 cents: $1 = <b>100¢</b>." if v == 100 else
                           "$1 = 100¢. So %s = %d × 100¢ = <b>%s</b>.%s" % (d(v), v // 100, c(v), extra)))

    def to_d(v, wrongs, extra=""):
        if v % 100 == 0:
            e = "100¢ = $1. So %s = <b>%s</b>." % (c(v), d(v))
        elif v < 100:
            e = "%s is less than $1. It is 0 dollars and %d cents: <b>%s</b>." % (c(v), v, d(v))
        else:
            e = "%s = %d¢ + %d¢ = $%d and %d¢. Write <b>%s</b>." % (c(v), (v // 100) * 100, v % 100, v // 100, v % 100, d(v))
        s("%s = ___" % c(v), d(v), wrongs, e + extra)

    to_c(100, ["10¢", "1¢", "1000¢"])
    to_c(200, ["20¢", "2¢", "2000¢"])
    to_c(240, ["24¢", "204¢", "2040¢"], " 24¢ drops the 0.")
    to_c(305, ["35¢", "350¢", "3005¢"], " 350¢ would be $3.50.")
    to_c(175, ["75¢", "1075¢", "157¢"], " 75¢ forgets the $1.")
    to_c(650, ["65¢", "605¢", "6050¢"], " 605¢ would be $6.05.")
    to_c(409, ["49¢", "490¢", "4009¢"], " 490¢ would be $4.90.")
    to_c(520, ["52¢", "502¢", "5020¢"], " 5020¢ writes 5 and 020.")
    to_d(300, ["$30", "$0.30", "$300"])
    to_d(240, ["$24.0", "$0.24", "$2.04"], " $24.0 puts the point in the wrong place. That is 24 dollars!")
    to_d(150, ["$15.0", "$1.05", "$150"], " $15.0 is 15 dollars.")
    to_d(405, ["$4.5", "$40.5", "$405"], " $4.5 means $4.50.")
    to_d(85, ["$85", "$8.5", "$0.58"], " $85 is 85 dollars, not 85 cents.")
    to_d(60, ["$60", "$6.0", "$0.06"], " $0.06 is only 6 cents.")
    to_d(725, ["$72.5", "$725", "$7.52"], " $72.5 puts the point in the wrong place.")
    to_d(1000, ["$100", "$1", "$1000"])
    toks = toks_of((200, 1), (100, 1), (50, 1), (10, 1))
    T = total(toks)
    assert T == 360
    s(fig(money_svg(toks)) + "How many cents is this?", c(T), ["36¢", "306¢", c(len(toks))],
      "$2 + $1 = $3 = 300¢. 50¢ + 10¢ = 60¢. 300¢ + 60¢ = <b>360¢</b>. %s counts the notes and coins." % c(len(toks)))
    s("Which is the same as $5.05?", "505¢", ["55¢", "550¢", "5005¢"],
      "$5 = 500¢. 500¢ + 5¢ = <b>505¢</b>. 550¢ would be $5.50.")
    nm, he, his = P.next()
    s("%s has 250¢. How much is that in dollars?" % nm, "$2.50", ["$25.0", "$2.05", "$250"],
      "250¢ = 200¢ + 50¢ = $2 and 50¢ = <b>$2.50</b>. $25.0 is 25 dollars.")
    nm, he, his = P.next()
    assert 3 * 100 + 4 * 20 == 380
    s("%s has three $1 coins and four 20¢ coins. How many cents does %s have?" % (nm, he), "380¢",
      ["7¢", "308¢", "340¢"],
      "Three $1 coins = 300¢. Four 20¢ coins: 20¢, 40¢, 60¢, 80¢. 300¢ + 80¢ = <b>380¢</b>. "
      "7¢ counts the coins. 340¢ takes the 20¢ coins as 10¢.")
    assert len(its) == 20
    return {"title": "Dollars and cents to cents, and back", "items": its}


# ============================================================ set 4: compare amounts
def set_compare(P, rnd):
    its = []
    SAME, CANT = "They are the same.", "You cannot tell."

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    def more(a, b, fa, fb, less=False):
        """a and b in cents, shown as fa(a), fb(b)"""
        assert a != b
        big = (a > b) != less
        right, wrong = (fa(a), fb(b)) if big else (fb(b), fa(a))
        word = "less" if less else "more"
        conv = ["%s = %s" % (f(v), c(v)) for f, v in ((fa, a), (fb, b)) if f is d]
        e = ("In cents: %s. " % ", ".join(conv)) if conv else ""
        e += "%s is %s than %s. The answer is <b>%s</b>." % (
            c(min(a, b) if less else max(a, b)), word, c(max(a, b) if less else min(a, b)), right)
        s("Which is %s: %s or %s?" % (word, fa(a), fb(b)), right, [wrong, SAME, CANT], e)

    more(350, 305, d, d)
    more(90, 100, c, d, less=True)
    more(250, 205, c, d)
    more(480, 408, d, d)
    more(610, 601, d, c, less=True)
    more(995, 1000, d, d)

    pics = [
        ("C", [(10, 5)], [(20, 3)]),
        ("A", [(500, 1), (50, 1)], [(200, 2), (100, 1)]),
        ("S", [(200, 1), (20, 3)], [(100, 2), (50, 1), (10, 1)]),
    ]
    for kind, ga, gb in pics:
        (na, _, _), (nb, _, _) = P.next(), P.next()
        ta, tb = toks_of(*ga), toks_of(*gb)
        va, vb = total(ta), total(tb)
        if kind == "S":
            assert va == vb
            right, wr = SAME, [na, nb, CANT]
        else:
            assert va != vb
            right, wr = (na, [nb, SAME, CANT]) if va > vb else (nb, [na, SAME, CANT])
        e = "%s: %s. %s: %s. " % (na, ", ".join(fmt_amt(sum(VAL[t] for t in srt(ta)[:k + 1])) for k in range(len(ta))),
                                  nb, ", ".join(fmt_amt(sum(VAL[t] for t in srt(tb)[:k + 1])) for k in range(len(tb))))
        if kind == "S":
            e += "Both have %s, so <b>they are the same</b>." % fmt_amt(va)
        else:
            e += "%s is more than %s, so <b>%s</b> has more." % (fmt_amt(max(va, vb)), fmt_amt(min(va, vb)), right)
        if len(ta) != len(tb):
            e += " More coins and notes do not always mean more money."
        s(fig(compare_svg([(na, ta), (nb, tb)])) + "Who has more money?", right, wr, e)

    s("Which is the greatest: $4.05, 445¢ or $4.50?", "$4.50", ["$4.05", "445¢", "They are all the same."],
      "In cents: $4.05 = 405¢, 445¢, $4.50 = 450¢. <b>$4.50</b> is the greatest.")
    s("Which is the least: $1.20, 112¢ or $1.02?", "$1.02", ["$1.20", "112¢", "They are all the same."],
      "In cents: $1.20 = 120¢, 112¢, $1.02 = 102¢. <b>$1.02</b> is the least.")
    s("Which is the greatest: 95¢, $0.59 or $1.05?", "$1.05", ["95¢", "$0.59", "They are all the same."],
      "In cents: 95¢, $0.59 = 59¢, $1.05 = 105¢. <b>$1.05</b> is the greatest. It is more than $1.")
    vals = {"$3.05": 305, "$3.50": 350, "330¢": 330}
    order = sorted(vals, key=vals.get)
    assert order == ["$3.05", "330¢", "$3.50"]
    s("Order from the least to the greatest: $3.50, $3.05, 330¢", ", ".join(order),
      ["$3.50, 330¢, $3.05", "330¢, $3.05, $3.50", "$3.05, $3.50, 330¢"],
      "In cents: $3.05 = 305¢, 330¢, $3.50 = 350¢. From the least: <b>$3.05, 330¢, $3.50</b>.")
    vals = {"$8": 800, "790¢": 790, "$8.20": 820}
    order = sorted(vals, key=vals.get, reverse=True)
    assert order == ["$8.20", "$8", "790¢"]
    s("Order from the greatest to the least: $8, 790¢, $8.20", ", ".join(order),
      ["790¢, $8, $8.20", "$8, $8.20, 790¢", "790¢, $8.20, $8"],
      "In cents: $8 = 800¢, 790¢, $8.20 = 820¢. From the greatest: <b>$8.20, $8, 790¢</b>. "
      "790 is a big number, but 790¢ is less than $8.")
    s("How much more is $9 than $4?", "$5", ["$13", "$4", "$6"],
      "$9 − $4 = <b>$5</b>. $13 adds instead of finding the difference.")
    assert m_digits(80, 35) == 55
    s("How much more is 80¢ than 35¢?", "45¢", ["115¢", "55¢", "35¢"],
      "80¢ − 35¢: 80 − 30 = 50, 50 − 5 = <b>45¢</b>. 55¢ takes 0 − 5 as 5. 115¢ adds.")
    s("$1 is how much more than 65¢?", "35¢", ["45¢", "165¢", "65¢"],
      "$1 = 100¢. Count on from 65¢: 70¢ is 5¢ more, 100¢ is 30¢ more. 5¢ + 30¢ = <b>35¢</b>. "
      "45¢ counts one ten too many. 165¢ adds.")
    s(fig(price_svg([("pencil", "$1.20"), ("ruler", "95¢")], "bookshop")) + "Which costs more?",
      "the pencil", ["the ruler", SAME, CANT],
      "$1.20 = 120¢. 120¢ is more than 95¢, so <b>the pencil</b> costs more.")
    (na, _, _), (nb, _, _) = P.next(), P.next()
    s("%s has 3 coins. %s has 6 coins. Who has more money?" % (na, nb), CANT, [nb, na, SAME],
      "<b>You cannot tell.</b> We need to know which coins they have. Three 50¢ coins ($1.50) are more than "
      "six 10¢ coins (60¢), but three 5¢ coins (15¢) are less.")
    s("Which amount is between $2 and $3?", "$2.65", ["$3.20", "190¢", "$0.25"],
      "$2 = 200¢ and $3 = 300¢. $2.65 = 265¢ is between them, so the answer is <b>$2.65</b>. 190¢ is less than $2.")
    assert len(its) == 20
    return {"title": "Compare amounts of money", "items": its}


# ============================================================ set 5: canteen word problems
def set_canteen(P, rnd):
    its = []

    def s(q, right, wrongs, e):
        its.append(mcq(q, right, wrongs, e))

    snacks = [("curry puff", 60), ("milk", 70), ("apple", 50), ("kaya toast", 90)]
    menu = price_svg([(n, c(p)) for n, p in snacks], "school canteen")
    sp = dict(snacks)

    nm, he, his = P.next()
    assert sp["curry puff"] + sp["milk"] == 130
    s(fig(menu) + "%s buys a curry puff and a packet of milk. How much does %s spend?" % (nm, he), "$1.30",
      ["30¢", "$13", "$1.03"],
      "60¢ + 70¢ = 130¢. 130¢ = <b>$1.30</b>. 30¢ forgets to rename 10 tens as 100¢. $13 has the point in the wrong place. "
      "$1.03 would be 103¢.")
    nm, he, his = P.next()
    s(fig(bar_parts([(6, "$6"), (4, "$4")], "?")) +
      "At the school book fair, %s buys a storybook for $6 and a puzzle book for $4. How much does %s spend?" % (nm, he),
      "$10", ["$2", "$64", "$11"],
      "The model shows 2 parts. Whole = $6 + $4 = <b>$10</b>. $2 is the difference, not the total.")
    nm, he, his = P.next()
    s(fig(bar_parts([(3, "$3"), (2, "?")], "$5")) +
      "%s had $5. %s spent $3 on chicken rice. How much did %s have left?" % (nm, cap(he), he),
      "$2", ["$8", "$3", "$1"],
      "Whole $5, one part $3. The other part is $5 − $3 = <b>$2</b>. $8 adds instead of taking away.")
    nm, he, his = P.next()
    s("A packet of milk costs 70¢. %s pays with a $1 coin. How much change does %s get?" % (nm, he), "30¢",
      ["170¢", "70¢", "3¢"],
      "$1 = 100¢. 100¢ − 70¢ = <b>30¢</b>. Count on: 80¢, 90¢, 100¢ is 3 tens. 3¢ forgets that 3 tens is 30¢. 170¢ adds.")
    nm, he, his = P.next()
    s(fig(menu) + "%s buys 2 apples. How much does %s pay?" % (nm, he), "$1",
      ["50¢", "52¢", "$10"],
      "50¢ + 50¢ = 100¢ = <b>$1</b>. 52¢ adds 50 and 2. 50¢ is the price of only 1 apple. $10 would be 1000¢.")
    nm1, he1, _ = P.next()
    nm2, he2, _ = P.next()
    assert 90 - 65 == 25 and m_digits(90, 65) == 35
    s(fig(bar_compare([(nm1, 90, "90¢"), (nm2, 65, "65¢")], "?")) +
      "%s has 90¢. %s has 65¢. How much more money does %s have?" % (nm1, nm2, nm1), "25¢",
      ["155¢", "35¢", "65¢"],
      "Find the difference: 90¢ − 65¢. 90 − 60 = 30, 30 − 5 = <b>25¢</b>. "
      "35¢ takes 0 − 5 as 5. 155¢ adds.")
    nm, he, his = P.next()
    s(fig(menu) + "%s has $1. %s buys kaya toast. How much money is left?" % (nm, cap(he)), "10¢",
      ["190¢", "90¢", "1¢"],
      "$1 = 100¢. 100¢ − 90¢ = <b>10¢</b>. Count on: 90¢ to 100¢ is 1 ten. 1¢ forgets that 1 ten is 10¢. 190¢ adds. 90¢ is the price, not the change.")
    nm, he, his = P.next()
    assert 5 * 2 == 10
    s(fig(bar_units(5, "$2", "?")) +
      "%s gets $2 for recess each school day. How much does %s get in 5 days?" % (nm, he), "$10",
      ["$7", "$25", "$12"],
      "1 unit = $2. 5 units = $2 + $2 + $2 + $2 + $2 = <b>$10</b>. $7 adds 5 and 2.")
    nm, he, his = P.next()
    s("%s has $10. %s buys a book for $7 at the school bookshop. How much does %s have left?" % (nm, cap(he), he),
      "$3", ["$17", "$7", "$4"],
      "$10 − $7 = <b>$3</b>. Check: $7 + $3 = $10. $17 adds instead of taking away.")
    s(fig(bar_compare([("chicken rice", 3, "$3"), ("noodles", 2, "?")], "$1")) +
      "Chicken rice costs $3. Noodles cost $1 less than chicken rice. How much do the noodles cost?", "$2",
      ["$4", "$3", "$1"],
      "Less means take away: $3 − $1 = <b>$2</b>. $4 adds the $1 instead.")
    assert sp["kaya toast"] + sp["milk"] == 160
    nm, he, his = P.next()
    s(fig(menu) + "%s buys kaya toast and a packet of milk. How much does %s spend?" % (nm, he), "$1.60",
      ["60¢", "$16", "$1.06"],
      "90¢ + 70¢ = 160¢ = <b>$1.60</b>. 60¢ forgets to rename. $1.06 would be 106¢.")
    nm, he, his = P.next()
    assert 120 - 95 == 25
    s("A bun costs $1.20. %s has 95¢. How much more money does %s need?" % (nm, he), "25¢",
      ["35¢", "215¢", "95¢"],
      "$1.20 = 120¢. 120¢ − 95¢: count on from 95¢: 100¢ is 5¢ more, 120¢ is 20¢ more. "
      "5¢ + 20¢ = <b>25¢</b>. 215¢ adds.")
    nm, he, his = P.next()
    assert 200 - 60 == 140
    s(fig(menu) + "%s pays for a curry puff with two $1 coins. How much change does %s get?" % (nm, he), "$1.40",
      ["$2.60", "$14", "40¢"],
      "Two $1 coins = 200¢. 200¢ − 60¢ = 140¢ = <b>$1.40</b>. 40¢ uses only one $1 coin. $2.60 adds.")
    nm, he, his = P.next()
    nm2, he2, his2 = P.next()
    s(fig(bar_compare([(nm2, 11, "?"), (nm, 8, "$8")], "$3")) +
      "%s saved $8. %s saved $3 more than %s. How much did %s save?" % (nm, nm2, nm, nm2), "$11",
      ["$5", "$8", "$3"],
      "More means add: $8 + $3 = <b>$11</b>. $5 takes away instead.")
    nm, he, his = P.next()
    toks = toks_of((20, 3), (10, 2))
    assert total(toks) == 80
    s(fig(money_svg(toks)) + "%s has these coins. A packet of milk costs 70¢. Can %s buy it?" % (nm, he),
      "Yes, with 10¢ left.", ["No, %s needs 10¢ more." % he, "Yes, with no money left.", "No, %s has only 5¢." % he],
      "Count: 20¢, 40¢, 60¢, 70¢, 80¢. %s has 80¢. 80¢ − 70¢ = 10¢, so <b>yes, with 10¢ left</b>. "
      "5¢ counts the coins." % nm)
    nm, he, his = P.next()
    s("%s has $5. %s buys fried rice for $2 and a drink for $1. How much money is left?" % (nm, cap(he)), "$2",
      ["$8", "$3", "$4"],
      "Spent: $2 + $1 = $3. Left: $5 − $3 = <b>$2</b>. $3 forgets the drink. $4 forgets the fried rice. $8 adds everything.")
    a, b, cc = P.next(), P.next(), P.next()
    s("At recess, %s spent 85¢, %s spent $1.05 and %s spent 98¢. Who spent the most?" % (a[0], b[0], cc[0]),
      b[0], [cc[0], a[0], "They spent the same."],
      "In cents: 85¢, $1.05 = 105¢, 98¢. 105¢ is the most, so <b>%s</b> spent the most." % b[0])
    nm, he, his = P.next()
    assert 45 + 35 == 80
    s(fig(bar_parts([(45, "45¢"), (35, "35¢")], "?")) +
      "%s spent 45¢ on a drink and 35¢ on a bun. How much did %s spend in all?" % (nm, he), "80¢",
      ["10¢", "70¢", "$8"],
      "45¢ + 35¢: 40 + 30 = 70, 5 + 5 = 10, 70 + 10 = <b>80¢</b>. 70¢ forgets the 10 from the ones. 10¢ is the difference.")
    nm, he, his = P.next()
    s(fig(bar_parts([(5, "?"), (4, "$4")], "$9")) +
      "%s had $9. After buying a storybook, %s had $4 left. How much did the storybook cost?" % (nm, he), "$5",
      ["$13", "$4", "$9"],
      "Whole $9, one part $4. The storybook is the other part: $9 − $4 = <b>$5</b>. $13 adds.")
    nm, he, his = P.next()
    assert 10 + 8 - 6 == 12
    s("At Chinese New Year, %s got $10 in one red packet and $8 in another. %s spent $6 at the book fair. "
      "How much money does %s have left?" % (nm, cap(he), he), "$12",
      ["$24", "$18", "$4"],
      "$10 + $8 = $18. $18 − $6 = <b>$12</b>. $18 forgets the spending. $4 is $10 − $6, which forgets the $8.")
    assert len(its) == 20
    return {"title": "Word problems at the school canteen", "items": its}


# ============================================================ lesson
def body_html():
    coins = ["C5", "C10", "C20", "C50", "C100"]
    notes = ["N2", "N5", "N10"]
    walk = toks_of((200, 1), (50, 1), (20, 1), (5, 1))
    assert total(walk) == 275
    return (
        "<h2>Our coins and notes</h2>"
        "<p>Singapore coins are 5¢, 10¢, 20¢, 50¢ and $1. Notes are $2, $5 and $10. "
        "100 cents make 1 dollar: <b>$1 = 100¢</b>.</p>"
        "<figure class='sn-fig'>" + money_svg(coins + notes, per_row=5, gap=10,
                                              label="Singapore coins 5¢, 10¢, 20¢, 50¢, $1 and notes $2, $5, $10") +
        "<figcaption>Coins: 5¢, 10¢, 20¢, 50¢, $1. Notes: $2, $5, $10.</figcaption></figure>"
        "<h2>Count the money, biggest first</h2>"
        "<p>Start with the note or coin of the greatest value. Then count on.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, gap=10, under=["$2", "$2.50", "$2.70", "$2.75"],
                                              label="counting on: $2, $2.50, $2.70, $2.75") +
        "<figcaption>$2, then $2.50, $2.70, $2.75. The total is $2.75.</figcaption></figure>"
        "<h2>Write money with a point</h2>"
        "<p>Write the dollars, then a point, then the cents. The cents <b>always</b> take 2 digits.</p>"
        + table(["Dollars and cents", "Write", "Not"], [
            ["$3 and 45¢", "$3.45", "$345"],
            ["$3 and 50¢", "$3.50", "$3.05"],
            ["$3 and 5¢", "$3.05", "$3.5"],
            ["85¢", "$0.85", "$85"],
        ]) +
        "<h2>Change to cents, or back</h2>"
        "<p>$1 = 100¢, so $2 = 200¢. To change $2.40 to cents, put the dollars and cents together: "
        "$2.40 = 200¢ + 40¢ = 240¢.</p>"
        + ex("Example", "Write 305¢ in dollars.", "305¢ = 300¢ + 5¢ = $3 and 5¢.", "$3.05")
        + "<h2>Compare amounts</h2>"
        "<p>Change both amounts to cents. Then compare the numbers. $2.05 = 205¢, so 250¢ is more.</p>"
        "<h2>Word problems with a model</h2>"
        "<p>Draw a bar model. Find the whole or the missing part. Add or subtract in dollars only or in cents only.</p>"
        "<figure class='sn-fig'>" + bar_parts([(60, "60¢"), (40, "?")], "$1 = 100¢") +
        "<figcaption>Siti has $1. A curry puff costs 60¢. 100¢ − 60¢ = 40¢ left.</figcaption></figure>"
        + ex("Example", "Ali gets $2 for recess each day. How much does he get in 3 days?",
             "1 unit = $2. 3 units = $2 + $2 + $2 = $6.", "$6")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["$3 and 5¢ written as $3.5", "5¢ is 05 after the point: $3.05"],
            ["240¢ = $24.0", "240¢ = 200¢ + 40¢ = $2.40"],
            ["4 coins, so 4¢", "Count the value of each coin, biggest first"],
            ["More coins means more money", "Count both amounts, then compare"],
            ["Comparing $2.05 and 250¢ by the digits", "Change both to cents first: 205¢ and 250¢"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 money?",
     "a": "In Primary 2, students count coins and notes in dollars and cents, write money in decimal notation such as "
          "$3.05, compare amounts, and change dollars and cents to cents only and back. They also solve word problems "
          "in dollars only or cents only."},
    {"q": "How do I explain $3.05 and $3.50 to my child?",
     "a": "Tell your child that cents always take 2 digits after the point. $3.05 is 3 dollars and 5 cents, and "
          "$3.50 is 3 dollars and 50 cents, so $3.50 is more."},
    {"q": "What is the most common mistake in P2 money?",
     "a": "The most common mistake is writing $3 and 5¢ as $3.5, which really means $3.50. Another is writing 240¢ "
          "as $24.0 instead of $2.40."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Money is part of Number and Algebra in the MOE 2021 Primary 2 Mathematics Syllabus (Standard "
          "Mathematics): counting money, decimal notation, comparing amounts and converting between dollars and cents."},
]


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=xmlns='[^']*' viewBox='0 0 (?:[2-9]\d\d|\d{4}) [^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def verify(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [mval(x) for x in it["c"]]
            vv = [v for v in vv if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x


def gen():
    rnd = random.Random(62808)
    P = People(rnd)
    sets = [set_count(P, rnd), set_decimal(P, rnd), set_convert(P, rnd), set_compare(P, rnd), set_canteen(P, rnd)]
    balance(sets, rnd)
    verify(sets)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "money", "sort": 8,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Money: Dollars and Cents",
        "seo_title": "P2 Money Worksheets: Free Primary 2 Maths Dollars and Cents Practice with Answers (MOE Syllabus)",
        "short_title": "Money",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Money",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Counting money in dollars and cents; decimal notation; comparing amounts; converting to cents only and vice versa",
        "meta_desc": "Free P2 maths money practice: count coins and notes, write $3.05, change $2.40 to 240¢, "
                     "compare amounts and solve canteen problems. 100 questions with answers.",
        "key_big": "$1 = 100¢, and cents always take 2 digits after the point.",
        "key_sub": "$3 and 5¢ = $3.05 = 305¢, not $3.5.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "money|bar model|price")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
