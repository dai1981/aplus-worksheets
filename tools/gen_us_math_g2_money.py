# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Counting Money (2.MD.C.8)
  python tools/gen_us_math_g2_money.py
Amounts under $1 are written with ¢ (45¢). Amounts of $1 or more are written with $ and a decimal point ($1.50).
Every total, choice and coin picture is computed from the same coin list and checked in code.
Coins and bills are simple labeled shapes (no real coin artwork).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]

# ------------------------------------------------------------ money facts
ORDER = ["B5", "B1", "Q", "D", "N", "P"]          # biggest value first
VAL = {"B5": 500, "B1": 100, "Q": 25, "D": 10, "N": 5, "P": 1}
ONE = {"B5": "$5 bill", "B1": "$1 bill", "Q": "quarter", "D": "dime", "N": "nickel", "P": "penny"}
MANY = {"B5": "$5 bills", "B1": "$1 bills", "Q": "quarters", "D": "dimes", "N": "nickels", "P": "pennies"}
# coin look: radius (dime smallest, then penny, nickel, quarter), fill, edge, label size
COIN = {"D": (19, "#dfe3e7", "#7a828a", 14), "P": (20, "#d9915a", "#8a5428", 15),
        "N": (23, "#dfe3e7", "#7a828a", 16), "Q": (27, "#dfe3e7", "#7a828a", 17)}
BILL_W, BILL_H = 78, 40


def amt(c):
    """45 -> '45¢', 150 -> '$1.50' (the Grade 2 rule: ¢ under $1, $ with a point from $1)."""
    assert c > 0, c
    return "%d¢" % c if c < 100 else "$%d.%02d" % (c // 100, c % 100)


def total(toks):
    return sum(VAL[t] for t in toks)


def toks_of(**k):
    """toks_of(Q=1, D=2) -> ['Q', 'D', 'D'] (biggest first)."""
    out = []
    for t in ORDER:
        out += [t] * k.get(t, 0)
    return out


def srt(toks):
    return sorted(toks, key=ORDER.index)


def nw(n, t):
    return "%d %s" % (n, ONE[t] if n == 1 else MANY[t])


def counts(toks):
    return [(t, toks.count(t)) for t in ORDER if t in toks]


def group(toks):
    """'1 quarter, 2 dimes and 1 penny'"""
    parts = [nw(n, t) for t, n in counts(toks)]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def group_list(toks):
    """short choice text: '1 quarter, 2 dimes'"""
    return ", ".join(nw(n, t) for t, n in counts(toks))


def coins_word(n):
    return "1 coin" if n == 1 else "%d coins" % n


def run(toks, start=0):
    """running totals while counting on: [25, 35, 45, 46]"""
    out, s = [], start
    for t in srt(toks):
        s += VAL[t]
        out.append(s)
    return out


def count_on(toks):
    """'Quarter: 25. Dimes: 35, 45. Penny: 46.' for coins only (under or over $1)."""
    out, s = [], 0
    for t, n in counts(toks):
        nums = []
        for _ in range(n):
            s += VAL[t]
            nums.append(amt(s) if s >= 100 else str(s))
        nm = ONE[t] if n == 1 else MANY[t]
        out.append("%s: %s." % (cap(nm), ", ".join(nums)))
    return " ".join(out)


def bills_coins_e(toks, last=False):
    bills = [t for t in srt(toks) if t.startswith("B")]
    coins = [t for t in srt(toks) if not t.startswith("B")]
    d = total(bills) // 100
    c = total(coins)
    steps = ", ".join("$%d" % (x // 100) for x in run(bills))
    if not coins:
        return "Count the dollars: %s. That is <b>%s</b>." % (steps, amt(total(toks)))
    return ("%s: %s. Then count on the coins: %s. $%d and %d¢ is <b>%s</b>."
            % ("The bills come last, but count them first" if last else "Count the dollars first", steps, ", ".join(str(x) for x in run(coins)), d, c, amt(total(toks))))


# ------------------------------------------------------------ typical mistakes (all computed)
def m_each_one(toks):
    """counted every coin or bill as 1¢"""
    return len(toks)


def m_swap(toks):
    """thought the bigger nickel is worth more than the dime (nickel 10¢, dime 5¢)"""
    sw = {"N": 10, "D": 5}
    return sum(sw.get(t, VAL[t]) for t in toks)


def m_same_step(toks):
    """kept counting by the old step for the first coin of each new kind (25, 35, 45, 55 instead of 46)"""
    s, prev = 0, None
    for t in srt(toks):
        if prev is not None and t != prev:
            s += VAL[prev]
        else:
            s += VAL[t]
        prev = t
    return s


def m_skip(toks, k=-1):
    """lost track and skipped one coin (k picks which kind)"""
    kinds = [t for t, n in counts(toks)]
    return total(toks) - VAL[kinds[k]]


def m_twice(toks, k=-1):
    """counted one coin twice"""
    kinds = [t for t, n in counts(toks)]
    return total(toks) + VAL[kinds[k]]


def m_bill_cent(toks):
    """counted each bill as 1¢ but the coins right"""
    return sum(1 if t.startswith("B") else VAL[t] for t in toks)


def m_coins_as_pennies(toks):
    """dollars right, then counted each coin as 1¢ ($1 and 2 quarters -> $1.02)"""
    return sum(VAL[t] if t.startswith("B") else 1 for t in toks)


def cents_sign(c):
    """wrong symbol: $1.50 written as 1.50¢"""
    return "%d.%02d¢" % (c // 100, c % 100)


def no_point(c):
    """wrong: $1.50 written as $150"""
    return "$%d" % c


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if isinstance(c, int):
            if c <= 0:
                continue
            c = amt(c)
        c = str(c)
        if c in seen or not c or c.startswith("-"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
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


def cap(s):
    return s[0].upper() + s[1:]


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


def draw_tok(t, cx, cy):
    """one coin (circle with its value) or one bill (green rectangle with its value), centered at cx, cy"""
    if t.startswith("B"):
        x, y = cx - BILL_W / 2, cy - BILL_H / 2
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
                "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
                % (x, y, BILL_W, BILL_H, FILL, GREEN, x + 5, y + 5, BILL_W - 10, BILL_H - 10, GREEN)
                + text(cx, cy + 7, "$%d" % (VAL[t] // 100), 20, col=GREEN))
    r, fill, edge, fs = COIN[t]
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='1'/>"
            % (cx, cy, r, fill, edge, cx, cy, r - 4, edge)
            + text(cx, cy + fs * 0.36, "%d¢" % VAL[t], fs))


def money_svg(toks, per_row=5, gap=8, pad=6, label=None, under=None):
    """Coins and bills in rows (at most per_row in a row). under: list of labels written below each item."""
    nrow = -(-len(toks) // per_row)
    per = -(-len(toks) // nrow)                     # balanced rows: 7 items -> 4 + 3
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
    return svg_wrap(w + 6, h + 6, draw_tok(t, (w + 6) / 2, (h + 6) / 2), "one %s, worth %s" % (ONE[t], amt(VAL[t])))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def shuffled(toks, rnd):
    """mixed-up order, but never already sorted biggest first"""
    t = list(toks)
    for _ in range(50):
        rnd.shuffle(t)
        if t != srt(t):
            return t
    return t


# ============================================================ set 1: coin names and values
def set_names(P, rnd):
    its = []
    names = ["penny", "nickel", "dime", "quarter"]
    tips = {"P": "The penny is the copper coin. It is worth <b>1¢</b>.",
            "N": "The nickel is worth <b>5¢</b>. It is bigger than a dime, but it is worth less.",
            "D": "The dime is worth <b>10¢</b>. It is the smallest coin, but it is worth more than a penny or a nickel.",
            "Q": "The quarter is the biggest coin. It is worth <b>25¢</b>."}
    for t in ["D", "N", "Q", "P"]:
        its.append(mcq("Which coin is worth %s?" % amt(VAL[t]), ONE[t], [n for n in names if n != ONE[t]], tips[t]))
    for t in ["N", "D", "P", "Q"]:
        wrong = {"N": [10, 1, 25], "D": [5, 1, 25], "P": [5, 10, 25], "Q": [10, 5, 1]}[t]
        its.append(mcq(fig(coin_svg(t)) + "This coin is a %s. How much is it worth?" % ONE[t], amt(VAL[t]), wrong, tips[t]))
    its.append(mcq(fig(money_svg(["N", "D"], label="a nickel and a dime")) + "The dime is smaller than the nickel. Which coin is worth more?",
                   "The dime", ["The nickel", "They are worth the same.", "It depends on the size."],
                   "The dime is worth 10¢ and the nickel is worth 5¢. 10 is more than 5, so the <b>dime</b> is worth more. "
                   "A bigger coin is not always worth more."))
    its.append(mcq("Which coin is the biggest?", "quarter", ["dime", "nickel", "penny"],
                   "The <b>quarter</b> is the biggest coin, and it is also worth the most: 25¢."))
    its.append(mcq("Which coin is the smallest?", "dime", ["penny", "nickel", "quarter"],
                   "The <b>dime</b> is the smallest coin. The penny is worth the least (1¢), but it is bigger than the dime."))
    its.append(mcq("Which coin is worth the least?", "penny", ["dime", "nickel", "quarter"],
                   "Penny 1¢, nickel 5¢, dime 10¢, quarter 25¢. The <b>penny</b> is worth the least. "
                   "The dime is the smallest coin, but it is worth 10¢."))
    make = [("pennies", 1, "nickel", 5, [1, 10, 2]), ("pennies", 1, "dime", 10, [5, 1, 100]),
            ("nickels", 5, "dime", 10, [5, 10, 1]), ("nickels", 5, "quarter", 25, [25, 2, 4]),
            ("dimes", 10, "dollar", 100, [100, 4, 5]), ("quarters", 25, "dollar", 100, [25, 5, 10]),
            ("pennies", 1, "dollar", 100, [10, 25, 1000])]
    for small, sv, big, bv, wrong in make:
        n = bv // sv
        assert n * sv == bv and n not in wrong
        steps = ", ".join(str(sv * k) for k in range(1, n + 1)) if n <= 10 else "1, 2, 3 … 100"
        e = ("A %s is %s. Count by %ds: %s. That is <b>%d %s</b>."
             % (big, amt(bv) if big != "dollar" else "100¢", sv, steps, n, small))
        its.append(mcq("How many %s make a %s?" % (small, big), n, [str(w) for w in wrong], e))
    its.append(mcq("How do you write five cents?", "5¢", ["$5", "5$", "50¢"],
                   "Write the number, then the cent sign: <b>5¢</b>. $5 means five dollars, which is much more."))
    assert len(its) == 20, len(its)
    return {"title": "Coin names and values", "items": its}


# ============================================================ set 2: count coins
ASK = ["How much money is shown?", "How many cents are there?", "How much money is this?"]


def coin_count_q(P, toks, mixed, rnd, i):
    shown = shuffled(toks, rnd) if mixed else srt(toks)
    nm, he, his = P.next()
    stems = ["%s has these coins. How much money does %s have?" % (nm, he),
             "How much money is shown?",
             "%s finds these coins in %s pocket. How much money is it?" % (nm, his),
             "How many cents are there?",
             "%s puts these coins in a piggy bank. How much money is that?" % nm,
             "How much money is this?"]
    q = fig(money_svg(shown)) + stems[i % len(stems)]
    T = total(toks)
    e = ("Put the coins in order from biggest to smallest. " if mixed else "Start with the biggest coin. ") + count_on(toks)
    e += " That is <b>%s</b>." % amt(T)
    return q, T, e


def set_count(P, rnd):
    its = []
    one = [("D", 3, "Count by 10s"), ("N", 4, "Count by 5s"), ("P", 6, "Count by 1s"),
           ("Q", 3, "Count by 25s"), ("D", 7, "Count by 10s"), ("N", 7, "Count by 5s")]
    for i, (t, n, how) in enumerate(one):
        toks = [t] * n
        T = total(toks)
        q = fig(money_svg(toks)) + ["How much money is shown?", "How many cents are there?", "How much money is this?"][i % 3]
        e = "Each %s is %s. %s: %s. %s are <b>%s</b>." % (ONE[t], amt(VAL[t]), how, ", ".join(str(x) for x in run(toks)),
                                                          cap(nw(n, t)), amt(T))
        if t == "P":
            wrong = [T * 5, T - 1, T + 1, T * 10]
        elif t == "Q":
            wrong = [m_each_one(toks), n * 10, T - 25, T + 25]
        else:
            wrong = [m_each_one(toks), m_swap(toks) if t in "ND" else T - 5, T - VAL[t], T + VAL[t]]
        its.append(mcq(q, amt(T), wrong, e))
    groups = [dict(D=2, P=3), dict(D=1, N=2), dict(N=3, P=4), dict(Q=1, D=1), dict(Q=1, N=2, P=1),
              dict(D=3, N=1, P=2), dict(Q=2, D=1), dict(Q=1, D=2, P=1), dict(Q=2, N=1, P=3),
              dict(Q=1, D=2, N=1, P=2), dict(Q=3, D=1, N=1), dict(Q=2, D=2, N=1, P=2), dict(D=4, N=2, P=3),
              dict(Q=1, D=1, N=1, P=4)]
    for i, g in enumerate(groups):
        toks = toks_of(**g)
        assert total(toks) < 100 and len(toks) <= 10
        q, T, e = coin_count_q(P, toks, i % 2 == 1, rnd, i)
        cands = [m_swap(toks), m_same_step(toks), m_each_one(toks), m_skip(toks, -1), m_twice(toks, 0), m_skip(toks, 0)]
        rot = i % 3
        cands = cands[rot:] + cands[:rot]
        its.append(mcq(q, amt(T), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Count coins", "items": its}


# ============================================================ set 3: dollars and cents
def set_dollars(P, rnd):
    its = []
    toks = toks_of(B1=3)
    its.append(mcq(fig(money_svg(toks)) + "How much money is shown?", "$3.00", ["3¢", "$300", "$2.00"],
                   bills_coins_e(toks) + " With no cents, write .00 after the dollars."))
    toks = toks_of(B5=1, B1=2)
    its.append(mcq(fig(money_svg(toks)) + "How much money is shown?", "$7.00", ["$3.00", "$6.00", "$8.00"],
                   "Start with the $5 bill: $5. Count on the $1 bills: $6, $7. That is <b>$7.00</b>. "
                   "There are 3 bills, but the $5 bill is worth 5 dollars."))
    its.append(mcq("How many cents are in 1 dollar?", "100 cents", ["10 cents", "25 cents", "50 cents"],
                   "1 dollar = <b>100 cents</b>. So $1 is the same as 4 quarters, 10 dimes or 100 pennies."))
    its.append(mcq("How do you write 1 dollar and 50 cents?", "$1.50", ["1.50¢", "$150", "$1.05"],
                   "Write the $ sign, then the dollars, then a point, then the cents: <b>$1.50</b>. "
                   "Don’t use the ¢ sign when you have a dollar or more."))
    its.append(mcq("How do you write 2 dollars and 5 cents?", "$2.05", ["$2.50", "2.05¢", "$205"],
                   "The cents always use 2 places after the point. 5 cents is written 05, so the answer is <b>$2.05</b>. "
                   "$2.50 would be 2 dollars and 50 cents."))
    its.append(mcq("How do you write 45 cents?", "45¢", ["$45", "45$", "4.5¢"],
                   "45 cents is less than 1 dollar, so write the number and the cent sign: <b>45¢</b>. "
                   "$45 would be 45 dollars."))
    toks = toks_of(Q=4)
    its.append(mcq(fig(money_svg(toks)) + "How much money is shown?", "$1.00", ["4¢", "$4.00", "$100"],
                   "Count by 25s: 25, 50, 75, 100. 100¢ is 1 dollar, so 4 quarters are <b>$1.00</b>."))
    toks = toks_of(Q=3, D=3)
    its.append(mcq(fig(money_svg(toks)) + "How much money is shown?", "$1.05", ["$1.50", "6¢", "90¢"],
                   "Quarters: 25, 50, 75. Dimes: 85, 95, 105. 105¢ is 1 dollar and 5 cents: <b>$1.05</b>. "
                   "Write 5 cents as .05, not .50."))
    groups = [dict(B1=1, Q=2), dict(B1=1, D=3), dict(B1=2, Q=1), dict(B1=1, Q=1, D=1, P=2), dict(B5=1, Q=1),
              dict(B5=1, B1=1, D=2, N=1), dict(B1=1, Q=3, P=1), dict(B1=3, N=3), dict(B5=1, D=1, N=1, P=3),
              dict(B1=1, Q=2, D=2, N=1), dict(B1=2, Q=1, D=1, N=1, P=1), dict(B5=1, B1=2, Q=2, P=4)]
    stems = ["How much money is shown?", "%s has this money. How much does %s have?",
             "How much money is this? Write it with $.", "%s saved this money. How much did %s save?"]
    for i, g in enumerate(groups):
        toks = toks_of(**g)
        T = total(toks)
        assert T >= 100 and len(toks) <= 10
        nm, he, his = P.next()
        stem = stems[i % 4]
        if "%s" in stem:
            stem = stem % (nm, he)
        shown = srt(toks) if i % 3 != 2 else [t for t in srt(toks) if not t.startswith("B")] + [t for t in srt(toks) if t.startswith("B")]
        q = fig(money_svg(shown)) + stem
        wrong_sets = [
            [m_coins_as_pennies(toks), cents_sign(T), m_skip(toks, -1)],
            [no_point(T), m_swap(toks), m_bill_cent(toks)],
            [m_same_step(toks), cents_sign(T), m_coins_as_pennies(toks)],
            [m_skip(toks, -1), no_point(T), m_swap(toks)],
        ]
        cands = wrong_sets[i % 4] + [m_twice(toks, -1), m_skip(toks, 0), m_bill_cent(toks), cents_sign(T)]
        e = bills_coins_e(toks, i % 3 == 2)
        its.append(mcq(q, amt(T), cands, e))
    assert len(its) == 20, len(its)
    return {"title": "Count dollars and cents", "items": its}


# ============================================================ set 4: make an amount
def parse_group(s):
    toks = []
    for part in s.split(", "):
        n, word = part.split(" ", 1)
        t = [k for k in ONE if ONE[k] == word or MANY[k] == word][0]
        assert (int(n) == 1) == (ONE[t] == word), s
        toks += [t] * int(n)
    return toks


def set_make(P, rnd):
    its = []
    shows = [(45, "1 quarter, 2 dimes", ["4 dimes, 5 nickels", "4 nickels, 5 pennies", "1 quarter, 2 nickels"]),
             (30, "1 quarter, 1 nickel", ["3 nickels", "1 quarter, 1 penny", "2 dimes, 1 nickel"]),
             (62, "2 quarters, 1 dime, 2 pennies", ["6 dimes, 2 nickels", "6 nickels, 2 pennies", "2 quarters, 1 nickel, 2 pennies"]),
             (81, "3 quarters, 1 nickel, 1 penny", ["8 nickels, 1 penny", "8 dimes, 1 nickel", "3 quarters, 1 dime, 1 penny"]),
             (56, "5 dimes, 1 nickel, 1 penny", ["5 dimes, 6 nickels", "5 nickels, 6 pennies", "2 quarters, 1 nickel"]),
             (90, "3 quarters, 1 dime, 1 nickel", ["9 nickels", "3 quarters, 1 dime", "2 quarters, 3 dimes"])]
    for target, right, wrong in shows:
        rt = parse_group(right)
        assert total(rt) == target and all(total(parse_group(w)) != target for w in wrong)
        w0 = parse_group(wrong[0])
        e = "%s So %s make <b>%s</b>. %s make %s." % (count_on(rt), group(rt), amt(target), cap(group(w0)), amt(total(w0)))
        its.append(mcq("Which coins make %s?" % amt(target), right, wrong, e))

    def fewest(c):
        out = []
        for t in ["Q", "D", "N", "P"]:
            k, c = divmod(c, VAL[t])
            out += [t] * k
        return out

    for c, wrong in [(30, [3, 6, 30]), (40, [4, 8, 2]), (50, [5, 10, 3]), (15, [3, 15, 1]),
                     (60, [6, 12, 4])]:
        best = fewest(c)
        assert len(best) not in wrong
        e = ("Use the biggest coin you can first. %s = %s. That is <b>%s</b>."
             % (group(best), amt(c), coins_word(len(best))))
        if c % 10 == 0:
            e += " %s would also work, but that is more coins." % nw(c // 10, "D")
        its.append(mcq("What is the fewest number of coins that make %s?" % amt(c), coins_word(len(best)),
                       [coins_word(w) for w in wrong], e))

    for g, need in [(dict(Q=1, D=2), 50), (dict(D=3, N=1), 60), (dict(Q=2, N=1, P=4), 60), (dict(Q=1, D=1, N=1), 50)]:
        toks = toks_of(**g)
        have = total(toks)
        miss = [t for t in "PNDQ" if VAL[t] == need - have]
        assert len(miss) == 1
        nm, he, his = P.next()
        q = (fig(money_svg(shuffled(toks, rnd))) + "%s has these coins. %s needs %s. Which one coin does %s need?"
             % (nm, cap(he), amt(need), he))
        e = "%s %s has %s. %s + %d = %d, so %s needs <b>1 %s</b>." % (
            count_on(toks), cap(he), amt(have), have, need - have, need, he, ONE[miss[0]])
        its.append(mcq(q, "1 " + ONE[miss[0]], ["1 " + ONE[t] for t in "PNDQ" if t != miss[0]], e))

    its.append(mcq("Which coins are worth the same as 1 quarter?", "5 nickels", ["5 pennies", "2 dimes", "3 dimes"],
                   "Count the nickels by 5s: 5, 10, 15, 20, 25. <b>5 nickels</b> = 25¢, the same as 1 quarter. "
                   "2 dimes are only 20¢."))
    its.append(mcq("Which coins are worth the same as 1 dollar?", "4 quarters", ["10 nickels", "4 dimes", "100 dimes"],
                   "Count the quarters: 25, 50, 75, 100. <b>4 quarters</b> = 100¢ = $1.00. 10 nickels are only 50¢."))
    for q, opts, best in [("Which coins are worth the most?", ["3 dimes", "5 nickels", "8 pennies", "1 quarter"], max),
                          ("Which coins are worth the most?", ["1 quarter", "4 nickels", "9 pennies", "1 dime"], max),
                          ("Which coins are worth the least?", ["4 nickels", "1 quarter", "3 dimes", "6 nickels"], min)]:
        vals = [total(parse_group(o)) for o in opts]
        b = best(vals)
        assert vals.count(b) == 1
        right = opts[vals.index(b)]
        e = "%s. So <b>%s</b> %s worth the %s." % (
            ", ".join("%s = %s" % (o, amt(v)) for o, v in zip(opts, vals)), right,
            "is" if right.startswith("1 ") else "are", "most" if best is max else "least")
        if best is max and "pennies" in " ".join(opts):
            e += " More coins do not always mean more money."
        if best is min:
            e += " One coin can be worth more than many coins."
        its.append(mcq(q, right, [o for o in opts if o != right], e))
    assert len(its) == 20, len(its)
    return {"title": "Make an amount", "items": its}


# ============================================================ set 5: word problems
def upsteps(a, b):
    """count up from a to b: '35 + 5 = 40, 40 + 10 = 50'"""
    out, s = [], a
    if s % 10:
        n = min(10 - s % 10, b - s)
        out.append("%d + %d = %d" % (s, n, s + n))
        s += n
    while s < b:
        n = min(10, b - s)
        out.append("%d + %d = %d" % (s, n, s + n))
        s += n
    return ", ".join(out)


def set_words(P, rnd):
    its = []

    def who():
        return P.next()

    # enough money?
    for g, price, thing in [(dict(D=2, N=1), 30, "a pencil"), (dict(Q=1, D=2), 40, "an eraser"),
                            (dict(Q=2, D=1, P=3), 65, "a toy car")]:
        toks = toks_of(**g)
        have = total(toks)
        nm, he, his = who()
        q = ("%s has %s. %s costs %s. Does %s have enough money?" % (nm, group(toks), cap(thing), amt(price), he))
        if have >= price:
            right = "Yes. %s has %s." % (cap(he), amt(have))
            wrong = ["No. %s has %s." % (cap(he), amt(m_each_one(toks))),
                     "No. %s has %s." % (cap(he), amt(m_swap(toks))),
                     "No. %s has %s." % (cap(he), amt(m_skip(toks, 0)))]
            e = "%s %s has <b>%s</b>. That is enough for %s." % (count_on(toks), cap(he), amt(have), amt(price))
            if have > price:
                e = "%s %s has %s. %s is more than %s, so <b>yes</b>, it is enough." % (
                    count_on(toks), cap(he), amt(have), amt(have), amt(price))
        else:
            right = "No. %s has %s." % (cap(he), amt(have))
            wrong = ["Yes. %s has %s." % (cap(he), amt(price)),
                     "Yes. %s has %s." % (cap(he), coins_word(len(toks))),
                     "No. %s has %s." % (cap(he), amt(m_each_one(toks)))]
            e = "%s %s has only %s. %s is less than %s, so <b>no</b>. %s needs %s more." % (
                count_on(toks), cap(he), amt(have), amt(have), amt(price), cap(he), amt(price - have))
        its.append(mcq(q, right, wrong, e))

    # how much more?
    for g, price, thing in [(dict(D=3, N=1), 50, "a bag of grapes"), (dict(Q=2), 75, "a jump rope"),
                            (dict(Q=1, D=1, P=2), 60, "a ruler"), (dict(Q=2, D=3), 90, "a ball")]:
        toks = toks_of(**g)
        have = total(toks)
        nm, he, his = who()
        need = price - have
        q = (fig(money_svg(toks)) + "%s has these coins. %s wants %s that costs %s. How much more money does %s need?"
             % (nm, cap(he), thing, amt(price), he))
        e = ("%s %s has %s. Count up from %d to %d: %s. That is %d more. %s needs <b>%s</b> more."
             % (count_on(toks), cap(he), amt(have), have, price, upsteps(have, price), need, cap(he), amt(need)))
        its.append(mcq(q, amt(need), [have + price, need + 10, price, need - 5 if need > 5 else need + 5], e))

    # total of two items
    items = [("a pear", 45, "an apple", 30), ("a sticker", 15, "a pencil", 25),
             ("a cookie", 35, "a juice box", 40), ("a notebook", 65, "a pen", 50)]
    for a, pa, b, pb in items:
        nm, he, his = who()
        T = pa + pb
        q = "%s costs %s. %s costs %s. %s buys both. How much does %s pay?" % (cap(a), amt(pa), cap(b), amt(pb), nm, he)
        tens = (pb // 10) * 10
        e = "Add: %d + %d. Count on from %d: %s." % (pa, pb, pa, ", ".join(str(pa + 10 * k) for k in range(1, pb // 10 + 1)))
        if pb % 10:
            e += " Then add %d more: %d." % (pb % 10, T)
        e += " %s pays <b>%s</b>." % (cap(he), amt(T))
        if T >= 100:
            e += " That is more than 100¢, so write it with $."
            cands = [cents_sign(T), pa - pb, T - 10, no_point(T)]
        else:
            cands = [abs(pa - pb), T - 10, T + 10]
        its.append(mcq(q, amt(T), cands, e))

    # change from $1
    for price, thing in [(75, "a juice"), (60, "a muffin"), (85, "a bag of popcorn"), (45, "a bookmark")]:
        nm, he, his = who()
        ch = 100 - price
        q = "%s pays with a $1 bill for %s that costs %s. How much change does %s get back?" % (nm, thing, amt(price), he)
        steps, s = [], price
        if s % 10:
            s += 10 - s % 10
            steps.append(str(s))
        while s < 100:
            s += 10
            steps.append(str(s))
        e = ("$1 is 100¢. Count up from %d to 100: %s. That is %d more, so the change is <b>%s</b>."
             % (price, ", ".join(steps), ch, amt(ch)))
        its.append(mcq(q, amt(ch), [100 + price, price, ch + 10, ch - 5], e))

    # spend from coins, then left
    nm, he, his = who()
    toks = toks_of(Q=1, D=3)
    its.append(mcq("%s has 1 quarter and 3 dimes. %s buys gum for 40¢. How much money does %s have left?" % (nm, cap(he), he),
                   "15¢", ["95¢", "45¢", "25¢"],
                   "%s %s has 55¢. Take away 40¢: 55 − 40 = 15. %s has <b>15¢</b> left." % (count_on(toks), cap(he), cap(he))))
    nm, he, his = who()
    its.append(mcq("%s has a $1 bill and 2 quarters. %s buys a book for $1.25. How much money is left?" % (nm, cap(he)),
                   "25¢", ["$2.75", "75¢", "$1.25"],
                   "%s has $1.00 + 50¢ = $1.50. Take away $1.25: the $1 bill and 1 quarter are spent. "
                   "1 quarter is left: <b>25¢</b>." % cap(he)))
    nm, he, his = who()
    toks = toks_of(Q=3, D=2)
    its.append(mcq("%s saves 3 quarters and 2 dimes in a jar. How much money is in the jar?" % nm,
                   "95¢", ["5¢", "85¢", "$1.05"],
                   "%s That is <b>95¢</b>." % count_on(toks)))
    nm, he, his = who()
    its.append(mcq("Stickers cost 10¢ each. %s has 2 quarters. How many stickers can %s buy?" % (nm, he),
                   "5 stickers", ["2 stickers", "4 stickers", "25 stickers"],
                   "2 quarters are 25, 50: that is 50¢. Count by 10s to 50: 10, 20, 30, 40, 50. That is <b>5 stickers</b>."))
    nm, he, his = who()
    nm2, he2, his2 = who()
    a, b = toks_of(D=3, P=4), toks_of(Q=2)
    assert total(b) - total(a) == 16
    its.append(mcq("%s has 3 dimes and 4 pennies. %s has 2 quarters. How much more money does %s have than %s?"
                   % (nm, nm2, nm2, nm), "16¢", ["84¢", "24¢", "5¢"],
                   "%s: 10, 20, 30, 31, 32, 33, 34. That is 34¢. %s: 25, 50. That is 50¢. "
                   "Count up from 34 to 50: 34 + 6 = 40, 40 + 10 = 50. 6 + 10 = <b>16¢</b>. "
                   "%s has fewer coins, but more money." % (nm, nm2, nm2)))
    assert len(its) == 20, len(its)
    return {"title": "Money word problems", "items": its}


# ============================================================ lesson
def body_html():
    coin_rows = [[coin_svg(t), ONE[t], amt(VAL[t]), d] for t, d in
                 [("P", "copper color"), ("N", "bigger than a penny"), ("D", "smallest coin"), ("Q", "biggest coin")]]
    walk = toks_of(Q=1, D=2, P=1)
    bill = toks_of(B1=1, Q=2)
    return (
        "<h2>Every coin has a value</h2>"
        "<p>To count money, you count the <b>value</b> of each coin, not the number of coins. "
        "Size does not tell you the value: the dime is the smallest coin, but it is worth more than a penny or a nickel.</p>"
        + table(["Coin", "Name", "Value", "Look for"], coin_rows) +
        "<p>1 dollar = 100¢. That is the same as 4 quarters, 10 dimes, 20 nickels or 100 pennies.</p>"
        "<h2>Count on from the biggest coin</h2>"
        "<p>Put the coins in order from biggest value to smallest. Start with the biggest. "
        "Then count on: by 25s for quarters, by 10s for dimes, by 5s for nickels and by 1s for pennies.</p>"
        "<figure class='sn-fig'>" + money_svg(walk, under=[str(x) for x in run(walk)], label="counting on: 25, 35, 45, 46") +
        "<figcaption>Quarter 25. Dimes 35, 45. Penny 46. The coins are worth 46¢.</figcaption></figure>"
        + ex("Example", "You have 2 dimes and 3 pennies. How many cents do you have?",
             "Start with the dimes: 10, 20. Count on the pennies: 21, 22, 23.", "23¢")
        + "<h2>Dollars and cents</h2>"
        "<p>Under $1, write the number and the cent sign: <b>45¢</b>. "
        "For $1 or more, write the dollar sign, the dollars, a point and the cents: <b>$1.50</b>. "
        "Count the bills first, then count on the coins.</p>"
        "<figure class='sn-fig'>" + money_svg(bill, under=["$1.00", "$1.25", "$1.50"], label="counting on: $1.00, $1.25, $1.50") +
        "<figcaption>A $1 bill and 2 quarters: $1.00, $1.25, $1.50.</figcaption></figure>"
        + ex("Example", "Ella has a $5 bill, 1 quarter and 1 nickel. How much money does she have?",
             "Dollars: $5. Coins: 25, 30. $5 and 30¢ is $5.30.", "$5.30")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting coins, not value: 3 dimes = 3¢", "Count by the coin’s value: 10, 20, 30. 3 dimes = 30¢"],
            ["Thinking the bigger nickel is worth more than the dime", "Nickel 5¢, dime 10¢. The small dime is worth more"],
            ["Starting with the pennies and losing track", "Start with the biggest coin and count on"],
            ["Not changing the step: 25, 35, 45, 55 for 1 quarter, 2 dimes, 1 penny", "Count by 1 for the penny: 25, 35, 45, 46"],
            ["Writing 1.50¢ or $150", "Use $ with a point for $1 or more: $1.50"],
            ["Writing 2 dollars and 5 cents as $2.50", "Cents use 2 places: $2.05"],
        ])
    )


FAQ = [
    {"q": "How do you teach a 2nd grader to count coins?",
     "a": "Sort the coins from biggest value to smallest, then count on: by 25s for quarters, 10s for dimes, 5s for nickels and 1s for pennies. For 1 quarter, 2 dimes and 1 penny, say 25, 35, 45, 46."},
    {"q": "Why is a dime worth more than a nickel if it is smaller?",
     "a": "A coin’s value is not set by its size. A dime is worth 10¢ and a nickel is worth 5¢, so 1 dime is worth the same as 2 nickels."},
    {"q": "When do you use the $ sign and when do you use the ¢ sign?",
     "a": "Use ¢ for amounts under one dollar, like 45¢. Use $ with a decimal point for one dollar or more, like $1.50, and never write both signs together."},
    {"q": "What money should a 2nd grader know?",
     "a": "Common Core standard 2.MD.C.8 asks children to count and solve word problems with dollar bills, quarters, dimes, nickels and pennies, using $ and ¢ correctly."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(205)
    P = People(rnd)
    sets = [set_names(P, rnd), set_count(P, rnd), set_dollars(P, rnd), set_make(P, rnd), set_words(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "¢¢" not in it["q"] and "$$" not in it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "counting-money", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting Money: Coins, Dollars and Cents",
        "seo_title": "Grade 2 Counting Money Worksheets: Pennies, Nickels, Dimes, Quarters and Dollar Bills",
        "short_title": "Counting money",
        "domain": "Measurement and Data",
        "standard_code": "2.MD.C.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/MD/C/8/",
        "standard_text": "Solve word problems involving dollar bills, quarters, dimes, nickels, and pennies, using $ and ¢ symbols appropriately. Example: If you have 2 dimes and 3 pennies, how many cents do you have?",
        "meta_desc": "Free Grade 2 counting money worksheets: learn coin values, count pennies, nickels, dimes and quarters, count dollar bills and coins, write $ and ¢ the right way, make amounts with the fewest coins, and solve money word problems. 100 practice questions with step-by-step answers.",
        "key_big": "Count the value, not the coins. Start with the biggest coin and count on.",
        "key_sub": "Penny 1¢, nickel 5¢, dime 10¢, quarter 25¢. 1 quarter, 2 dimes and 1 penny: 25, 35, 45, 46¢. For $1 or more, use $ and a point: a $1 bill and 2 quarters is $1.50.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "money")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
