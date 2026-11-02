# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Ratio word problems (MOE 2021 Primary Mathematics Syllabus, Primary 6: Ratio)
  python3 tools/gen_sg_maths_p6_ratio_word_problems.py
Sharing a total in a ratio, finding the other part or the total from one part, problems where the
difference is given, before-and-after problems (unchanged total, unchanged difference, one quantity
unchanged) with bar models and units, and PSLE-style problems with three-part ratios.
Wrong answers come from real mistakes: dividing the total by one number of the ratio, giving one unit,
giving the other share, treating the difference as one unit, keeping the difference instead of the ratio,
changing the quantity that stays the same, and adding ratios whose totals are different.
Every choice carries its value; no two choices are equal in value. Every before-and-after problem is
checked with the real amounts. HTML attributes use single quotes (no backslashes in the JSON).
Singapore English, Singapore dollars, numbers with 5+ digits use a no-break space.
"""
import json, math, os, random, re
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
GREEN = "#2e7d4f"
FILL_L = "#cfe6d6"
FILL_Y = "#fde7bd"
FILL_B = "#d6e4f5"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


def lcm(a, b):
    return a * b // gcd(a, b)


# ------------------------------------------------------------ numbers and choices
def num(n):
    if isinstance(n, F):
        n = float(n) if n.denominator != 1 else n.numerator
    if isinstance(n, float):
        s = ("%.2f" % n).rstrip("0").rstrip(".")
        whole, _, dec = s.partition(".")
        return num(int(whole)) + ("." + dec if dec else "")
    s = str(n)
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NBSP.join(g)
    return s


def R(*xs):
    return " : ".join(num(x) for x in xs)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def money(v):
    v = F(v)
    if v.denominator == 1:
        return "$" + num(v.numerator)
    cents = int(v * 100)
    assert cents == v * 100
    return "$%s.%02d" % (num(cents // 100), cents % 100)


def Rc(*xs):
    return (R(*xs), ("ratio",) + tuple(xs))


def Fc(a, b):
    return (fr(a, b), F(a, b))


def Nc(n, u=""):
    return ("%s%s" % (num(n), u), F(n))


def Mc(v):
    return (money(v), F(v))


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, right, cands, e):
    """right / cands are (html, value). First 3 usable wrong choices are kept: positive, whole where
    the answer is whole, different text and value from the answer and from each other. Answer at 0."""
    seen, vals, pick = {plain(right[0])}, {right[1]}, []
    for c in cands:
        if c is None:
            continue
        s, v = c
        if plain(s) in seen or v in vals:
            continue
        if isinstance(v, F) and v <= 0:
            continue
        seen.add(plain(s))
        vals.add(v)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, right, cands)
    return {"q": q, "c": [right[0]] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][0]
            wrong = it["c"][1:]
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

    def two(self):
        a = self.next()
        b = self.next()
        return a, b


def cap(s):
    return s[0].upper() + s[1:]


def unit(n, one, many=None):
    return "%s %s" % (num(n), one if n == 1 else (many or one + "s"))


def coprime_pair(rnd, lo=1, hi=9, maxsum=12):
    while True:
        p, q = rnd.randint(lo, hi), rnd.randint(lo, hi)
        if p != q and gcd(p, q) == 1 and p + q <= maxsum:
            return p, q


def units(n):
    return "1 unit" if n == 1 else "%d units" % n


# ------------------------------------------------------------ html helpers
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(" ") * 0.3 - t.count(NBSP) * 0.3 - t.count(".") * 0.5 - t.count(",") * 0.5) * fs * 0.6


def text(x, y, t, fs=15, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag pictures that must print larger so their parts and labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ bar model
COLS = [FILL_L, FILL_Y, FILL_B]


def bar_svg(rows, total=None, brace=None, label="bar model", cw=None):
    """rows: [(label, boxes, cell_text, right_text, colour)].
    total: text for a bracket on the right of all rows.
    brace: (row, first_box, last_box, text) - a bracket below that row's boxes (only for the last row)
    or above them (only for the first row). Every box has the same width, so the model is exact."""
    fs = 15
    lw = max(tw(r[0], fs) for r in rows) + 12
    x0 = 6 + lw
    if cw is None:
        cw = max([30] + [tw(r[2], fs) + 12 for r in rows if r[2]])
    bh, gap = 28, 10
    top = 4
    if brace and brace[0] == 0:
        top = 30
    s, ends = [], []
    for i, (lab, n, cell, right, col) in enumerate(rows):
        y = top + i * (bh + gap)
        s.append(text(x0 - 8, y + bh / 2 + 5.5, lab, fs, "end"))
        for j in range(n):
            x = x0 + j * cw
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, cw, bh, col, INK))
            if cell:
                s.append(text(x + cw / 2, y + bh / 2 + 5.5, cell, fs, col=RED if cell == "?" else INK))
        xe = x0 + n * cw
        if right:
            s.append(text(xe + 8, y + bh / 2 + 5.5, right, fs, "start", RED if right == "?" else INK))
            xe += 8 + tw(right, fs)
        ends.append(xe)
    ybot = top + len(rows) * (bh + gap) - gap
    H = ybot + 4
    W = max(ends) + 6
    if brace:
        r, a, b, t = brace
        xa, xb = x0 + a * cw, x0 + (b + 1) * cw
        xm = (xa + xb) / 2
        col = RED if t == "?" else INK
        if r == 0:
            y = top - 4
            s.append("<path d='M%.1f %d v-7 H%.1f v7' fill='none' stroke='%s' stroke-width='2'/>" % (xa, y, xb, INK))
            s.append(text(xm, y - 11, t, fs, "middle", col))
        else:
            assert r == len(rows) - 1
            y = ybot + 4
            s.append("<path d='M%.1f %d v7 H%.1f v-7' fill='none' stroke='%s' stroke-width='2'/>" % (xa, y, xb, INK))
            s.append(text(xm, y + 24, t, fs, "middle", col))
            H = ybot + 34
        W = max(W, xm + tw(t, fs) / 2 + 6)
    if total:
        xb = max(ends) + 10
        s.append("<path d='M%.1f %d h8 V%d h-8' fill='none' stroke='%s' stroke-width='2'/>" % (xb, top, ybot, INK))
        s.append(text(xb + 14, (top + ybot) / 2 + 5.5, total, fs, "start", RED if total == "?" else INK))
        W = max(W, xb + 14 + tw(total, fs) + 6)
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ contexts
# (plural noun, singular noun) for things people collect; money is handled separately
THINGS = [("stickers", "sticker"), ("marbles", "marble"), ("stamps", "stamp"), ("cards", "card"),
          ("beads", "bead"), ("seashells", "seashell"), ("erasers", "eraser"), ("storybooks", "storybook")]


class Ctx:
    """How to talk about one kind of amount: money or a count of things."""

    def __init__(self, kind, many="", one=""):
        self.kind, self.many, self.one = kind, many, one

    def amt(self, v):
        return money(v) if self.kind == "money" else unit(v, self.one, self.many)

    def c(self, v):
        return (self.amt(v), F(v))

    def poss(self, name):
        return "%s’s %s" % (name, "money" if self.kind == "money" else self.many)

    def more(self, d, word="more"):
        if self.kind == "money":
            return "%s %s" % (money(d), word if word == "more" else "less")
        return "%s %s %s" % (num(d), word, self.many if d != 1 else self.one)

    def how(self, name, verb="have"):
        if self.kind == "money":
            return "How much money does %s %s?" % (name, verb)
        return "How many %s does %s %s?" % (self.many, name, verb)

    def how_tog(self):
        if self.kind == "money":
            return "How much money do they have altogether?"
        return "How many %s do they have altogether?" % self.many


# ============================================================ set 1: sharing a total in a ratio
def set_share(rnd, P):
    its = []
    seen = set()

    def pqu(maxsum, ulo, uhi, ok=lambda p, q, u: True):
        for _ in range(10000):
            p, q = coprime_pair(rnd, 1, 9, maxsum)
            u = rnd.randint(ulo, uhi)
            if (p, q) not in seen and p > 1 and q > 1 and ok(p, q, u):
                seen.add((p, q))
                return p, q, u
        raise AssertionError("no ratio left")

    # 1) share money or things between two people (8), bar models on half
    for i in range(8):
        askA = i % 2 == 0
        p, q, u = pqu(11, 4, 15, lambda p, q, u: ((p + q) * u) % (p if askA else q) == 0 or True)
        T = (p + q) * u
        (A, _, _), (B, _, _) = P.two()
        n = p if askA else q
        ans = n * u
        who = A if askA else B
        if i < 4:
            cx = Ctx("money")
            q_ = "%s and %s share %s in the ratio %s. How much money does %s get?" % (A, B, money(T), R(p, q), who)
        else:
            many, one = THINGS[i - 4]
            cx = Ctx("things", many, one)
            q_ = "%s and %s share %s in the ratio %s. How many %s does %s get?" % (A, B, unit(T, one, many), R(p, q), many, who)
        c = [cx.c(T // n) if T % n == 0 else None, cx.c(u), cx.c((p + q - n) * u),
             cx.c(T // (p + q - n)) if T % (p + q - n) == 0 else None, cx.c(T // 2) if T % 2 == 0 else None,
             cx.c(ans + u), cx.c(ans - u)]
        if i % 4 < 2:
            tl = money(T) if cx.kind == "money" else num(T)
            rows = [(A, p, "", "?" if askA else "", FILL_L), (B, q, "", "" if askA else "?", FILL_Y)]
            q_ = fig(bar_svg(rows, tl, None, "bar model: %s %d units, %s %d units, total %s" % (A, p, B, q, tl))) + q_
        e = ("%d + %d = %d units. %s: %d units = %s, so 1 unit = %s ÷ %d = %s. %s gets %s: %d × %s = <b>%s</b>. "
             "Do not divide %s by %d: find the total units first."
             % (p, q, p + q, "Total", p + q, cx.amt(T), num(T) if cx.kind != "money" else money(T), p + q,
                cx.amt(u), who, units(n), n, cx.amt(u), cx.amt(ans), money(T) if cx.kind == "money" else num(T), n))
        e = e.replace("Total: %d units = %s, so" % (p + q, cx.amt(T)), "%d units = %s, so" % (p + q, cx.amt(T)))
        its.append(mcq(q_, cx.c(ans), c, e))

    # 2) a group in a ratio: how many in one part (3)
    GROUPS = [("boys", "girls", "pupils", "a CCA"), ("adults", "children", "people", "a hawker centre"),
              ("cats", "dogs", "animals", "an animal shelter")]
    for X, Y, W, pl in GROUPS:
        p, q, u = pqu(12, 4, 12)
        T = (p + q) * u
        ans = q * u
        c = [Nc(T // q) if T % q == 0 else None, Nc(p * u), Nc(u), Nc(T // p) if T % p == 0 else None,
             Nc(T - q), Nc(ans + u)]
        q_ = "The ratio of the number of %s to the number of %s in %s is %s. There are %d %s. How many %s are there?" % (
            X, Y, pl, R(p, q), T, W, Y)
        e = ("%d + %d = %d units. %d units = %d, so 1 unit = %d ÷ %d = %d. %s: %d × %d = <b>%d</b>. "
             "%d is the number of %s." % (p, q, p + q, p + q, T, T, p + q, u, cap(Y), q, u, ans, p * u, X))
        its.append(mcq(q_, Nc(ans), c, e))

    # 3) how many more (3)
    MORE = [("girls", "boys", "pupils", "a choir"), ("red balloons", "blue balloons", "balloons", "a Children’s Day party"),
            ("chicken wings", "fish balls", "pieces", "a party")]
    for X, Y, W, pl in MORE:
        p, q, u = pqu(13, 4, 9, lambda p, q, u: p - q >= 2)
        T = (p + q) * u
        ans = (p - q) * u
        c = [Nc(p - q), Nc(p * u), Nc(q * u), Nc(u), Nc(T // (p - q)) if T % (p - q) == 0 else None]
        q_ = "The ratio of %s to %s at %s is %s. There are %d %s altogether. How many more %s than %s are there?" % (
            X, Y, pl, R(p, q), T, W, X, Y)
        if X == "girls":
            q_ = "The ratio of girls to boys in %s is %s. There are %d %s altogether. How many more girls than boys are there?" % (
                pl, R(p, q), T, W)
        e = ("1 unit = %d ÷ %d = %d. The difference is %d − %d = %s: %d × %d = <b>%d</b>. "
             "%d is only the difference in the ratio, not the number of %s."
             % (T, p + q, u, p, q, units(p - q), p - q, u, ans, p - q, W))
        its.append(mcq(q_, Nc(ans), c, e))

    # 4) fraction of the total (2)
    for i in range(2):
        p, q, u = pqu(11, 2, 3)
        (A, _, _), (B, _, _) = P.two()
        if i == 0:
            right, c = Fc(p, p + q), [Fc(p, q), Fc(q, p + q), Fc(q, p)]
            who, n = A, p
        else:
            right, c = Fc(q, p + q), [Fc(q, p), Fc(p, p + q), Fc(p, q)]
            who, n = B, q
        q_ = "%s and %s share some money in the ratio %s. What fraction of the money does %s get?" % (A, B, R(p, q), who)
        e = ("The whole is %d + %d = %d units. %s gets %s out of %d: <b>%s</b>. "
             "%s compares the two shares, not one share with the whole." % (p, q, p + q, who, units(n), p + q,
                                                                          fr(n, p + q), c[0][0]))
        its.append(mcq(q_, right, c, e))

    # 5) measures (4)
    its.append(mcq("Mrs Lim makes 2 ℓ of lime juice. She mixes lime syrup and water in the ratio 1 : 4. "
                   "How much water does she use?", Nc(1600, " ml"),
                   [Nc(400, " ml"), Nc(500, " ml"), Nc(1500, " ml"), Nc(8000, " ml")],
                   "2 ℓ = 2000 ml. 1 + 4 = 5 units, so 1 unit = 2000 ÷ 5 = 400 ml. Water: 4 × 400 = <b>1600 ml</b>. "
                   "400 ml is the syrup."))
    its.append(mcq("A ribbon 3 m long is cut into two pieces in the ratio 2 : 3. How long is the shorter piece?",
                   Nc(120, " cm"), [Nc(180, " cm"), Nc(150, " cm"), Nc(100, " cm"), Nc(60, " cm")],
                   "3 m = 300 cm. 2 + 3 = 5 units, so 1 unit = 300 ÷ 5 = 60 cm. Shorter piece: 2 × 60 = <b>120 cm</b>. "
                   "Do not divide 300 by 2 or by 3."))
    its.append(mcq("Mr Rahman pours 1 ℓ 500 ml of soya bean milk into a big jug and a small jug in the ratio 2 : 1. "
                   "How much milk is in the big jug?", Nc(1000, " ml"),
                   [Nc(500, " ml"), Nc(750, " ml"), Nc(3000, " ml"), Nc(1300, " ml")],
                   "1 ℓ 500 ml = 1500 ml. 2 + 1 = 3 units, so 1 unit = 1500 ÷ 3 = 500 ml. "
                   "Big jug: 2 × 500 = <b>1000 ml</b>. 750 ml shares the milk equally."))
    its.append(mcq("A 2.4 kg bag of nuts has peanuts and cashew nuts in the ratio 5 : 3 by mass. "
                   "What is the mass of the cashew nuts?", Nc(900, " g"),
                   [Nc(1500, " g"), Nc(300, " g"), Nc(800, " g"), Nc(480, " g")],
                   "2.4 kg = 2400 g. 5 + 3 = 8 units, so 1 unit = 2400 ÷ 8 = 300 g. "
                   "Cashew nuts: 3 × 300 = <b>900 g</b>. 800 g is 2400 ÷ 3, which forgets the peanuts."))
    assert len(its) == 20, len(its)
    return {"title": "Sharing a total in a ratio", "items": its}


# ============================================================ set 2: one part known
def set_one_part(rnd, P):
    its = []
    seen = set()

    def pqu(maxsum, ulo, uhi):
        for _ in range(10000):
            p, q = coprime_pair(rnd, 2, 9, maxsum)
            u = rnd.randint(ulo, uhi)
            if (p, q) not in seen:
                seen.add((p, q))
                return p, q, u
        raise AssertionError

    # 1) one share known -> the other share (7)
    for i in range(7):
        p, q, u = pqu(13, 4, 15)
        (A, _, _), (B, _, _) = P.two()
        cx = Ctx("money") if i < 4 else Ctx("things", *THINGS[i])
        X = p * u
        ans = q * u
        c = [cx.c(X + q - p) if X + q - p > 0 else None, cx.c(u), cx.c((p + q) * u), cx.c(X * q),
             cx.c(X * p // q) if (X * p) % q == 0 else None, cx.c(X + q)]
        q_ = ("The ratio of %s to %s is %s. %s has %s. %s" % (cx.poss(A), cx.poss(B), R(p, q), A, cx.amt(X), cx.how(B)))
        e = ("%s has %s = %s, so 1 unit = %s ÷ %d = %s. %s has %s: %d × %s = <b>%s</b>. "
             "Do not just add %d to %s: a ratio is about multiplying and dividing."
             % (A, units(p), cx.amt(X), num(X) if cx.kind != "money" else money(X), p, cx.amt(u), B, units(q), q,
                cx.amt(u), cx.amt(ans), q - p if q > p else p - q, money(X) if cx.kind == "money" else num(X)))
        if q < p:
            e = e.replace("just add %d to" % (p - q), "just take %d from" % (p - q))
        its.append(mcq(q_, cx.c(ans), c, e))

    # 2) one share known -> the total (6), bar models on 3
    for i in range(6):
        p, q, u = pqu(13, 4, 12)
        (A, _, _), (B, _, _) = P.two()
        cx = Ctx("money") if i % 2 else Ctx("things", *THINGS[(i + 3) % 8])
        X = p * u
        ans = (p + q) * u
        c = [cx.c(q * u), cx.c(X * (p + q)), cx.c(X + p + q), cx.c(X * q), cx.c(u)]
        if cx.kind == "money":
            q_ = "%s and %s share some money in the ratio %s. %s gets %s. How much money do they share?" % (
                A, B, R(p, q), A, money(X))
        else:
            q_ = "%s and %s share some %s in the ratio %s. %s gets %s. How many %s do they share?" % (
                A, B, cx.many, R(p, q), A, cx.amt(X), cx.many)
        if i < 3:
            lab = money(X) if cx.kind == "money" else num(X)
            q_ = fig(bar_svg([(A, p, "", lab, FILL_L), (B, q, "", "", FILL_Y)], "?", None,
                             "bar model: %s %d units is %s, %s %d units, total unknown" % (A, p, lab, B, q))) + q_
        e = ("%s = %s, so 1 unit = %s. The total is %d + %d = %d units: %d × %s = <b>%s</b>. "
             "%s is only %s’s share." % (units(p), cx.amt(X), cx.amt(u), p, q, p + q, p + q, cx.amt(u), cx.amt(ans),
                                          cx.amt(q * u), B))
        its.append(mcq(q_, cx.c(ans), c, e))

    # 3) fraction -> ratio (4)
    FR = [("Ali", "Siti", "savings", 3, 5, "of"), ("Raju", "Kumar", "height", 4, 5, "of"),
          (None, None, "boys", 3, 8, "class"), (None, None, "red", 5, 12, "beads")]
    for A, B, what, a, b, kind in FR:
        if kind == "of":
            nounA = "%s’s %s" % (A, what)
            q_ = "%s %s %s of %s’s %s. What is the ratio of %s’s %s to %s’s %s?" % (
                cap(nounA), "are" if what == "savings" else "is", fr(a, b), B, what, A, what, B, what)
            right = Rc(a, b)
            c = [Rc(b, a), Rc(a, a + b), Rc(a, b - a), Rc(b, a + b)]
            vb = "are" if what == "savings" else "is"
            e = ("If %s’s %s %s %s, then %s’s %s %s %s. So the ratio is <b>%s</b>. "
                 "%s is the wrong way round." % (B, what, vb, units(b), A, what, vb, units(a), R(a, b), R(b, a)))
        elif kind == "class":
            q_ = "In a class, %s of the pupils are boys. What is the ratio of the number of boys to the number of girls?" % fr(a, b)
            right = Rc(a, b - a)
            c = [Rc(a, b), Rc(b - a, a), Rc(b, a), Rc(b, b - a)]
            e = ("Out of %d units, %d units are boys and %d − %d = %d units are girls. Boys : girls = <b>%s</b>. "
                 "%s compares boys with the whole class." % (b, a, b, a, b - a, R(a, b - a), R(a, b)))
        else:
            q_ = "A box has red beads and yellow beads. %s of the beads are red. What is the ratio of yellow beads to red beads?" % fr(a, b)
            right = Rc(b - a, a)
            c = [Rc(a, b - a), Rc(b - a, b), Rc(a, b), Rc(b, a)]
            e = ("Red is %s, so yellow is %d − %d = %s. Yellow : red = <b>%s</b>. Yellow is named first, so it goes first."
                 % (units(a), b, a, units(b - a), R(b - a, a)))
        its.append(mcq(q_, right, c, e))

    # 4) ratio from two amounts in simplest form (3)
    AM = [(24, 36, "money", None), (45, 60, "stamps", None), (560, 420, "ml", "apple juice")]
    for x, y, kind, extra in AM:
        g = gcd(x, y)
        a, b = x // g, y // g
        g2 = [d for d in range(2, g) if g % d == 0 and d != g]
        half = g2[-1] if g2 else 2
        (A, _, _), (B, _, _) = P.two()
        if kind == "money":
            q_ = "%s has $%d and %s has $%d. What is the ratio of %s’s money to %s’s money in its simplest form?" % (A, x, B, y, A, B)
            c = [Rc(b, a), Rc(x // half, y // half), Rc(a, a + b), Rc(y - x, x)]
            who = (A, B)
        elif kind == "stamps":
            q_ = "%s has %d stamps and %s has %d stamps. What is the ratio of %s’s stamps to the total number of stamps in its simplest form?" % (A, x, B, y, A)
            a, b = x // g, (x + y) // g
            c = [Rc(x // g, y // g), Rc(x // half, (x + y) // half), Rc(b, a), Rc(y // g, b)]
            who = (A, "the total")
        else:
            q_ = ("Mdm Wong mixes %d ml of apple juice with %d ml of orange juice. What is the ratio of the volume of orange juice "
                  "to the volume of apple juice in its simplest form?" % (x, y))
            a, b = y // g, x // g
            c = [Rc(b, a), Rc(y // half, x // half), Rc(a, a + b), Rc(x - y, y)]
            who = ("orange juice", "apple juice")
        e = ("%sThe highest common factor is %d. Divide both numbers by %d: <b>%s</b>. "
             "%s is equal in value, but it is not accepted: the question asks for the simplest form, and both numbers can still be divided by %d."
             % ("The total is %d + %d = %d, so the ratio is %d : %d. " % (x, y, x + y, x, x + y) if kind == "stamps" else "",
                g, g, R(a, b), R(a * g // half, b * g // half), g // half))
        its.append(mcq(q_, Rc(a, b), c, e))
    assert len(its) == 20, len(its)
    return {"title": "Finding the other part or the total", "items": its}


# ============================================================ set 3: difference given
def set_difference(rnd, P):
    its = []
    seen = set()
    MODES = ["small", "large", "total", "small", "large"] * 4
    for i in range(20):
        mode = MODES[i]
        for _ in range(10000):
            p, q = coprime_pair(rnd, 1, 9, 13)
            u = rnd.randint(3, 14)
            if (p, q) not in seen and abs(p - q) >= 2 and min(p, q) >= 2 and max(p, q) * u <= 120:
                seen.add((p, q))
                break
        (A, _, _), (B, _, _) = P.two()
        cx = Ctx("money") if i % 3 == 0 else Ctx("things", *THINGS[i % 8])
        d = abs(q - p) * u
        k = abs(q - p)
        big, small = (B, A) if q > p else (A, B)
        nb, ns = max(p, q), min(p, q)
        fewer = i % 4 == 3
        if fewer:
            rel = "%s has %s than %s." % (small, cx.more(d, "fewer"), big)
        else:
            rel = "%s has %s than %s." % (big, cx.more(d), small)
        if mode == "small":
            ans, ask, n = ns * u, cx.how(small), ns
            c = [cx.c(d * ns), cx.c(d), cx.c(nb * u), cx.c(u), cx.c(d // ns) if d % ns == 0 else None, cx.c(ans + d)]
        elif mode == "large":
            ans, ask, n = nb * u, cx.how(big), nb
            c = [cx.c(d * nb), cx.c(d), cx.c(ns * u), cx.c(d + nb), cx.c(u)]
        else:
            ans, ask, n = (p + q) * u, cx.how_tog(), p + q
            c = [cx.c(d * (p + q)), cx.c(nb * u), cx.c(d + p + q), cx.c(d), cx.c(ns * u + d * 2)]
        q_ = "The ratio of %s to %s is %s. %s %s" % (cx.poss(A), cx.poss(B), R(p, q), rel, ask)
        if i % 2 == 0:
            dl = money(d) if cx.kind == "money" else num(d)
            if q > p:
                rows = [(A, p, "", "", FILL_L), (B, q, "", "", FILL_Y)]
                br = (1, p, q - 1, dl)
            else:
                rows = [(A, p, "", "", FILL_L), (B, q, "", "", FILL_Y)]
                br = (0, q, p - 1, dl)
            q_ = fig(bar_svg(rows, None, br, "bar model: %s %d units, %s %d units, difference %s" % (A, p, B, q, dl))) + q_
        e = ("The difference is %d − %d = %s. %s = %s, so 1 unit = %s ÷ %d = %s. "
             % (nb, ns, units(k), units(k), cx.amt(d), money(d) if cx.kind == "money" else num(d), k, cx.amt(u)))
        if mode == "total":
            e += "Altogether: %d + %d = %d units = %d × %s = <b>%s</b>." % (p, q, p + q, p + q, cx.amt(u), cx.amt(ans))
        else:
            e += "%s: %s = %d × %s = <b>%s</b>." % (big if mode == "large" else small, units(n), n, cx.amt(u), cx.amt(ans))
        e += " The difference is %s, not 1 unit." % units(k)
        its.append(mcq(q_, cx.c(ans), c, e))
    assert len(its) == 20, len(its)
    return {"title": "When the difference is given", "items": its}


# ============================================================ set 4: before and after
def rat(x, y):
    g = gcd(x, y)
    return x // g, y // g


def eqr(a, b, x, y):
    return R(a, b) if (a, b) == (x, y) else "%s = %s" % (R(a, b), R(x, y))


def unit_step(k, given, w):
    """'3 units = 24, so 1 unit = 8' or '1 unit = 8'."""
    if k == 1:
        return "1 unit = %s" % given
    return "%s = %s, so 1 unit = %s" % (units(k), given, w)


def set_before_after(rnd, P):
    its = []
    seen = set()

    def model(rows, lab):
        assert max(r[1] for r in rows) <= 12
        return fig(bar_svg(rows, None, None, lab, cw=26))

    def counted(noun):
        return lambda v: Nc(v, " " + noun)

    # ---- one quantity unchanged (7): A changes by N, B stays the same
    U_STORIES = [("hall", -1), ("money", -1), ("things", 1), ("hall", 1), ("money", 1), ("things", -1), ("hall", -1)]
    for i, (story, sign) in enumerate(U_STORIES):
        easy = i < 2
        for _ in range(100000):
            a, b = coprime_pair(rnd, 1, 9, 13)
            c_, d_ = coprime_pair(rnd, 1, 9, 13)
            if (a, b) == (c_, d_) or ("U", a, b, c_, d_) in seen:
                continue
            if easy != (b == d_):
                continue
            L = lcm(b, d_)
            A1, A2 = a * L // b, c_ * L // d_
            if (A2 - A1) * sign <= 0 or L > 12 or max(A1, A2) > 12:
                continue
            if not easy and a == c_:
                continue
            w = rnd.randint(3, 12)
            k = abs(A2 - A1)
            N = k * w
            if L * w > 150 or N < 6:
                continue
            seen.add(("U", a, b, c_, d_))
            break
        else:
            raise AssertionError("no U")
        A0, B0 = A1 * w, L * w
        Af = A2 * w
        assert rat(A0, B0) == (a, b) and rat(Af, B0) == (c_, d_) and abs(Af - A0) == N
        nm, he, his = P.next()
        if story == "hall":
            X, Y = ("boys", "girls") if i % 2 else ("adults", "children")
            act = ("After %d %s left the hall" if sign < 0 else "After %d more %s came into the hall") % (N, X)
            q0 = "The ratio of the number of %s to the number of %s in a hall was %s. %s, the ratio became %s. " % (
                X, Y, R(a, b), act, R(c_, d_))
            fa = num
            asks = [("How many %s were in the hall?" % Y, B0, L, cap(Y), Y),
                    ("How many %s were in the hall at first?" % X, A0, A1, "%s at first" % cap(X), X),
                    ("How many people were in the hall at first?", A0 + B0, A1 + L, "People at first", "people")]
            nmA, nmB = cap(X), cap(Y)
            same = "The number of %s does not change" % Y
            whoA = "The number of %s" % X
            whoB = "the %s" % Y
        elif story == "money":
            (B, _, _) = P.next()
            act = ("After %s spent %s" % (nm, money(N))) if sign < 0 else (
                "After %s’s grandmother gave %s %s" % (nm, "her" if he == "she" else "him", money(N)))
            q0 = "The ratio of %s’s money to %s’s money was %s. %s, the ratio became %s. " % (nm, B, R(a, b), act, R(c_, d_))
            fa = money
            asks = [("How much money does %s have?" % B, B0, L, B, None),
                    ("How much money did %s have at first?" % nm, A0, A1, "%s at first" % nm, None),
                    ("How much money does %s have now?" % nm, Af, A2, "%s now" % nm, None)]
            nmA, nmB = nm, B
            same = "%s’s money does not change" % B
            whoA = "%s’s money" % nm
            whoB = B
        else:
            (B, _, _) = P.next()
            many, one = THINGS[(i + 2) % 8]
            act = ("After %s gave away %d %s" % (nm, N, many)) if sign < 0 else ("After %s bought %d more %s" % (nm, N, many))
            q0 = "The ratio of %s’s %s to %s’s %s was %s. %s, the ratio became %s. " % (nm, many, B, many, R(a, b), act, R(c_, d_))
            fa = num
            asks = [("How many %s does %s have?" % (many, B), B0, L, B, many),
                    ("How many %s did %s have at first?" % (many, nm), A0, A1, "%s at first" % nm, many),
                    ("How many %s did they have altogether at first?" % many, A0 + B0, A1 + L, "Altogether at first", many)]
            nmA, nmB = nm, B
            same = "%s’s %s do not change" % (B, many)
            whoA = "%s’s %s" % (nm, many)
            whoB = B
        ask, ans, m, what, noun = asks[i % 3]
        fm = Mc if noun is None else counted(noun)
        raw = {B0: b, A0: a, A0 + B0: a + b, Af: c_}[ans]
        bad = []
        if a != c_ and N % abs(a - c_) == 0:
            bad.append(fm(N // abs(a - c_) * raw))
        bad += [fm(w), fm(N * raw), fm(B0), fm(A0), fm(Af), fm(A0 + B0), fm(N)]
        if easy:
            e = "%s, and it is %s in both ratios. " % (same, units(L))
        else:
            e = "%s, so use the same number of units for %s in both ratios. Before: %s. After: %s. " % (
                same, whoB, eqr(a, b, A1, L), eqr(c_, d_, A2, L))
        e += ("%s went from %s to %s, a change of %s. %s. %s: %s = <b>%s</b>."
              % (whoA, units(A1), units(A2), units(k), unit_step(k, fa(N), fa(w)), what, units(m), fm(ans)[0]))
        if not easy:
            e += " Do not compare %s and %s as they are: %s %s %s in one and %s in the other." % (
                R(a, b), R(c_, d_), whoB, "are" if story == "hall" else "has", units(b), units(d_))
        lab = "bar model: before %s %s, after %s, %s %s unchanged" % (nmA, units(A1), units(A2), nmB, units(L))
        f = model([("%s, before" % nmA, A1, "", "", FILL_L), ("%s, after" % nmA, A2, "", "", FILL_B),
                   (nmB, L, "", "", FILL_Y)], lab) if i in (0, 2, 4) else ""
        its.append(mcq(f + q0 + ask, fm(ans), bad, e))

    # ---- total unchanged (7): A gives B some
    T_STORIES = ["things", "money", "things", "water", "things", "money", "things"]
    for i, story in enumerate(T_STORIES):
        easy = i < 2
        for _ in range(100000):
            a, b = coprime_pair(rnd, 1, 9, 12)
            c_, d_ = coprime_pair(rnd, 1, 9, 12)
            if a <= b or ("T", a, b, c_, d_) in seen:
                continue
            S1, S2 = a + b, c_ + d_
            if easy != (S1 == S2):
                continue
            L = lcm(S1, S2)
            A1, A2 = a * L // S1, c_ * L // S2
            if A1 <= A2 or L > 12:
                continue
            w = rnd.randint(3, 15)
            k = A1 - A2
            N = k * w
            if L * w > 160 or N < 6:
                continue
            seen.add(("T", a, b, c_, d_))
            break
        else:
            raise AssertionError("no T")
        B1, B2 = L - A1, L - A2
        A0, B0, Af, Bf = A1 * w, B1 * w, A2 * w, B2 * w
        assert rat(A0, B0) == (a, b) and rat(Af, Bf) == (c_, d_) and A0 - Af == N and A0 + B0 == Af + Bf
        (nm, he, his), (B, _, _) = P.two()
        if story == "money":
            fa, noun = money, None
            q0 = "The ratio of %s’s money to %s’s money was %s. After %s gave %s %s, the ratio became %s. " % (
                nm, B, R(a, b), nm, B, money(N), R(c_, d_))
            asks = [("How much money did %s have at first?" % nm, A0, A1, "%s at first" % nm),
                    ("How much money does %s have now?" % B, Bf, B2, "%s now" % B),
                    ("How much money do they have altogether?", L * w, L, "Altogether")]
            A, Bn = nm, B
        elif story == "water":
            fa, noun = (lambda v: num(v) + " ℓ"), "ℓ"
            q0 = ("The ratio of the volume of water in Tank A to the volume of water in Tank B was %s. "
                  "After %d ℓ of water was poured from Tank A into Tank B, the ratio became %s. " % (R(a, b), N, R(c_, d_)))
            asks = [("How much water was in Tank A at first?", A0, A1, "Tank A at first"),
                    ("How much water is in Tank B now?", Bf, B2, "Tank B now"),
                    ("How much water is there in the two tanks altogether?", L * w, L, "Altogether")]
            A, Bn = "Tank A", "Tank B"
        else:
            many, one = THINGS[(i + 5) % 8]
            fa, noun = num, many
            q0 = "The ratio of %s’s %s to %s’s %s was %s. After %s gave %s %d %s, the ratio became %s. " % (
                nm, many, B, many, R(a, b), nm, B, N, many, R(c_, d_))
            asks = [("How many %s did %s have at first?" % (many, nm), A0, A1, "%s at first" % nm),
                    ("How many %s did %s have at first?" % (many, B), B0, B1, "%s at first" % B),
                    ("How many %s does %s have now?" % (many, B), Bf, B2, "%s now" % B),
                    ("How many %s do they have altogether?" % many, L * w, L, "Altogether")]
            A, Bn = nm, B
        fm = Mc if noun is None else counted(noun)
        ask, ans, m, what = asks[i % len(asks)]
        raw = {A0: a, B0: b, Bf: d_, L * w: a + b}.get(ans, a)
        bad = []
        if a > c_ and N % (a - c_) == 0:
            bad.append(fm(N // (a - c_) * raw))
        bad += [fm(w), fm(N * raw), fm(A0), fm(B0), fm(Af), fm(Bf), fm(L * w), fm(N)]
        if easy:
            e = "The total does not change: %s and %s both have %s. " % (R(a, b), R(c_, d_), units(L))
        else:
            e = ("The total does not change, so give both ratios the same total. Before: %s (%s). After: %s (%s). "
                 % (eqr(a, b, A1, B1), units(L), eqr(c_, d_, A2, B2), units(L)))
        e += ("%s went from %s to %s, so %s gave away %s. %s. %s: %s = <b>%s</b>."
              % (A, units(A1), units(A2), A, units(k), unit_step(k, fa(N), fa(w)), what, units(m), fm(ans)[0]))
        if not easy:
            e += " Do not compare %s and %s as they are: their totals are %d and %d units." % (R(a, b), R(c_, d_), a + b, c_ + d_)
        lab = "bar model: before %s %s and %s %s, after %s and %s" % (A, units(A1), Bn, units(B1), units(A2), units(B2))
        f = model([("Before: " + A, A1, "", "", FILL_L), (Bn, B1, "", "", FILL_Y),
                   ("After: " + A, A2, "", "", FILL_L), (Bn + " ", B2, "", "", FILL_Y)], lab) if i in (1, 3, 5) else ""
        its.append(mcq(f + q0 + ask, fm(ans), bad, e))

    # ---- difference unchanged (6): both change by the same amount
    D_STORIES = ["age", "spend", "age", "save", "age", "spend"]
    ADULTS = ["Mr Tan", "Mrs Lim", "Mrs Ng"]
    for i, story in enumerate(D_STORIES):
        for _ in range(200000):
            a, b = coprime_pair(rnd, 1, 9, 13)
            c_, d_ = coprime_pair(rnd, 1, 9, 13)
            if a >= b or c_ >= d_ or ("D", a, b, c_, d_) in seen:
                continue
            D1, D2 = b - a, d_ - c_
            L = lcm(D1, D2)
            A1, A2 = a * L // D1, c_ * L // D2
            sign = -1 if story == "spend" else 1
            if (A2 - A1) * sign <= 0 or (D1 == D2 and i > 1):
                continue
            if max(A1 + L, A2 + L) > 14:
                continue
            w = rnd.randint(2, 12)
            k = abs(A2 - A1)
            N = k * w
            A0, B0, Af, Bf = A1 * w, (A1 + L) * w, A2 * w, (A2 + L) * w
            if story == "age":
                if not (5 <= A0 <= 14 and 28 <= B0 <= 48 and 2 <= N <= 20 and B0 - A0 >= 22):
                    continue
            else:
                if not (B0 <= 150 and N >= 5 and min(Af, A0) >= 4):
                    continue
            seen.add(("D", a, b, c_, d_))
            break
        else:
            raise AssertionError("no D " + story)
        assert rat(A0, B0) == (a, b) and rat(Af, Bf) == (c_, d_) and Bf - Af == B0 - A0 and abs(Af - A0) == N
        if story == "age":
            A = P.next()[0]
            Bn = ADULTS[i // 2]
            fm = counted("years old")
            fa = lambda v: "%s years" % num(v)
            q0 = ("The ratio of %s’s age to %s’s age is %s now. In %d years’ time, the ratio will be %s. "
                  % (A, Bn, R(a, b), N, R(c_, d_)))
            asks = [("How old is %s now?" % A, A0, A1, "%s now" % A),
                    ("How old is %s now?" % Bn, B0, A1 + L, "%s now" % Bn),
                    ("How old will %s be in %d years’ time?" % (Bn, N), Bf, A2 + L, "%s then" % Bn)]
            ask, ans, m, what = asks[i // 2]
            change = "%s’s age went up from %s to %s, that is %s" % (A, units(A1), units(A2), units(k))
            both = "Both people get %d years older, so the difference in their ages does not change" % N
        else:
            (A, _, _), (Bn, _, _) = P.two()
            fm, fa = Mc, money
            if story == "spend":
                q0 = ("The ratio of %s’s money to %s’s money was %s. They each spent %s at a book fair. "
                      "Then the ratio became %s. " % (A, Bn, R(a, b), money(N), R(c_, d_)))
                asks = [("How much money did %s have at first?" % A, A0, A1, "%s at first" % A),
                        ("How much money did %s have at first?" % Bn, B0, A1 + L, "%s at first" % Bn),
                        ("How much money does %s have now?" % Bn, Bf, A2 + L, "%s now" % Bn)]
                both = "They spent the same amount, so the difference between them does not change"
                change = "%s’s money went down from %s to %s, that is %s" % (A, units(A1), units(A2), units(k))
            else:
                q0 = ("The ratio of %s’s savings to %s’s savings was %s. They each saved another %s. "
                      "Then the ratio became %s. " % (A, Bn, R(a, b), money(N), R(c_, d_)))
                asks = [("How much did %s have in savings at first?" % A, A0, A1, "%s at first" % A),
                        ("How much did %s have in savings at first?" % Bn, B0, A1 + L, "%s at first" % Bn),
                        ("How much does %s have in savings now?" % Bn, Bf, A2 + L, "%s now" % Bn)]
                both = "They saved the same amount, so the difference between them does not change"
                change = "%s’s savings went up from %s to %s, that is %s" % (A, units(A1), units(A2), units(k))
            ask, ans, m, what = asks[i % 3]
        raw = {A0: a, B0: b, Bf: d_}.get(ans, a)
        bad = []
        if a != c_ and N % abs(a - c_) == 0:
            bad.append(fm(N // abs(a - c_) * raw))
        bad += [fm(w), fm(N * raw), fm(A0), fm(B0), fm(Af), fm(Bf), fm(B0 - A0), fm(ans + N), fm(abs(ans - N))]
        if D1 == D2:
            e = "%s. The difference is %s in both ratios. " % (both, units(L))
        else:
            e = ("%s. Give the difference the same number of units. Before: %s (difference %s). "
                 "After: %s (difference %s). " % (both, eqr(a, b, A1, A1 + L), units(L), eqr(c_, d_, A2, A2 + L), units(L)))
        e += "%s. %s. %s: %s = <b>%s</b>." % (change, unit_step(k, fa(N), fa(w)), what, units(m), fm(ans)[0])
        if D1 != D2:
            e += " Do not compare %s and %s as they are: their differences are %d and %d units." % (R(a, b), R(c_, d_), D1, D2)
        lab = "bar model: before %s %s and %s %s, after %s and %s" % (A, units(A1), Bn, units(A1 + L), units(A2), units(A2 + L))
        f = model([("Before: " + A, A1, "", "", FILL_L), (Bn, A1 + L, "", "", FILL_Y),
                   ("After: " + A, A2, "", "", FILL_L), (Bn + " ", A2 + L, "", "", FILL_Y)], lab) if i in (1, 4) else ""
        its.append(mcq(f + q0 + ask, fm(ans), bad, e))
    assert len(its) == 20, len(its)
    return {"title": "Before and after: same total, same difference or one part unchanged", "items": its}


# ============================================================ set 5: PSLE-style problems
def set_psle(rnd, P):
    its = []

    def add(q, right, c, e, check=True):
        assert check
        its.append(mcq(q, right, c, e))

    M = Mc
    n = lambda v, u="": Nc(v, u)
    # 1 three-part share
    (A, _, _), (B, _, _) = P.two()
    (C, _, _) = P.next()
    f = fig(bar_svg([(A, 2, "", "", FILL_L), (B, 3, "", "", FILL_Y), (C, 4, "", "?", FILL_B)], "$360", None,
                    "bar model: %s 2 units, %s 3 units, %s 4 units, total $360" % (A, B, C)))
    add(f + "%s, %s and %s shared $360 in the ratio 2 : 3 : 4. How much money did %s get?" % (A, B, C, C),
        M(160), [M(90), M(120), M(40), M(200)],
        "2 + 3 + 4 = 9 units. 9 units = $360, so 1 unit = $40. %s: 4 units = 4 × $40 = <b>$160</b>. "
        "$90 is $360 ÷ 4, which forgets the other two shares." % C, 9 * 40 == 360)
    # 2 three-part with difference
    add("A box has red, blue and green beads in the ratio 3 : 5 : 7. There are 24 more green beads than red beads. "
        "How many beads are there in the box?", n(90, " beads"),
        [n(360, " beads"), n(42, " beads"), n(30, " beads"), n(18, " beads")],
        "Green − red = 7 − 3 = 4 units. 4 units = 24, so 1 unit = 6. Total: 3 + 5 + 7 = 15 units = 15 × 6 = <b>90 beads</b>. "
        "360 treats the difference 24 as 1 unit.", 15 * 6 == 90 and 4 * 6 == 24)
    # 3 combine two ratios
    (A, _, _), (B, _, _) = P.two()
    (C, _, _) = P.next()
    add("The ratio of %s’s money to %s’s money is 2 : 3. The ratio of %s’s money to %s’s money is 4 : 5. "
        "They have $350 altogether. How much money does %s have?" % (A, B, B, C, C),
        M(150), [M(175), M(120), M(80), M(50)],
        "Make %s’s units the same: 2 : 3 = 8 : 12 and 4 : 5 = 12 : 15. So %s : %s : %s = 8 : 12 : 15 = 35 units. "
        "1 unit = $350 ÷ 35 = $10. %s: 15 × $10 = <b>$150</b>. $175 comes from 2 : 3 : 5, which joins ratios "
        "where %s’s units are different." % (B, A, B, C, C, B), 80 + 120 + 150 == 350 and F(80, 120) == F(2, 3) and F(120, 150) == F(4, 5))
    # 4 combine two ratios with difference
    add("At a fruit stall, the ratio of apples to oranges is 3 : 2. The ratio of oranges to pears is 5 : 4. "
        "There are 42 more apples than pears. How many oranges are there?", n(60, " oranges"),
        [n(90, " oranges"), n(48, " oranges"), n(198, " oranges"), n(42, " oranges")],
        "Make the oranges the same: 3 : 2 = 15 : 10 and 5 : 4 = 10 : 8. Apples : oranges : pears = 15 : 10 : 8. "
        "Apples − pears = 7 units = 42, so 1 unit = 6. Oranges: 10 × 6 = <b>60</b>. 90 is the number of apples.",
        90 - 48 == 42 and F(90, 60) == F(3, 2) and F(60, 48) == F(5, 4))
    # 5 notes
    add("Mr Tan has some $5 notes and $10 notes in the ratio 3 : 2. The total value of the notes is $280. "
        "How many $10 notes does he have?", n(16, " notes"), [n(24, " notes"), n(8, " notes"), n(40, " notes"), n(11, " notes")],
        "1 group = 3 notes of $5 and 2 notes of $10 = $15 + $20 = $35. $280 ÷ $35 = 8 groups. "
        "$10 notes: 8 × 2 = <b>16</b>. 24 is the number of $5 notes.", 24 * 5 + 16 * 10 == 280 and F(24, 16) == F(3, 2))
    # 6 fraction of remainder
    nm, he, his = P.next()
    add("%s spent %s of %s money on a book and %s of the remainder on a bag. What is the ratio of the money spent on the bag "
        "to the money %s had left?" % (nm, fr(1, 4), his, fr(2, 5), he), Rc(2, 3),
        [Rc(2, 5), Rc(3, 2), Rc(3, 10), Rc(1, 4)],
        "Let %s money be 20 units. Book: 5 units. Remainder: 15 units. Bag: %s of 15 = 6 units. Left: 15 − 6 = 9 units. "
        "Bag : left = 6 : 9 = <b>2 : 3</b>." % (his, fr(2, 5)), F(1, 4) * 20 == 5 and F(2, 5) * 15 == 6)
    # 7 transfer, same total
    (A, _, _), (B, _, _) = P.two()
    f = fig(bar_svg([("Before: " + A, 5, "", "", FILL_L), (B, 3, "", "", FILL_Y),
                     ("After: " + A, 3, "", "", FILL_L), (B + " ", 5, "", "", FILL_Y)], None, None,
                    "bar model: before %s 5 units and %s 3 units, after 3 units and 5 units" % (A, B), cw=30))
    add(f + "%s and %s had 120 marbles altogether in the ratio 5 : 3. %s gave some marbles to %s. "
        "Then the ratio became 3 : 5. How many marbles did %s give to %s?" % (A, B, A, B, A, B),
        n(30, " marbles"), [n(15, " marbles"), n(45, " marbles"), n(75, " marbles"), n(60, " marbles")],
        "The total stays 8 units. 8 units = 120, so 1 unit = 15. %s went from 5 units to 3 units, so %s gave "
        "2 units = 2 × 15 = <b>30 marbles</b>." % (A, A), 75 - 30 == 45 and 45 + 75 == 120)
    # 8 both spend the same
    (A, _, _), (B, _, _) = P.two()
    add("%s had $80 and %s had $50. They each spent the same amount of money. Then the ratio of %s’s money to %s’s money "
        "became 5 : 2. How much money did each of them spend?" % (A, B, A, B), M(30), [M(10), M(50), M(20), M(40)],
        "The difference stays $80 − $50 = $30. After: 5 − 2 = 3 units = $30, so 1 unit = $10. %s has 5 units = $50 left. "
        "Each spent $80 − $50 = <b>$30</b>." % A, F(80 - 30, 50 - 30) == F(5, 2))
    # 9 ages
    kid = P.next()
    while kid[1] != "he":
        kid = P.next()
    kid = kid[0]
    add("Mdm Wong is 40 years old. Her son, %s, is 10 years old. In how many years will the ratio of Mdm Wong’s age "
        "to %s’s age be 5 : 2?" % (kid, kid), n(10, " years"), [n(20, " years"), n(50, " years"), n(30, " years"), n(3, " years")],
        "The difference in age never changes: 40 − 10 = 30 years. 5 − 2 = 3 units = 30 years, so 1 unit = 10 years. "
        "%s will be 2 units = 20 years old, which is in 20 − 10 = <b>10 years</b>. 20 is his age then." % kid,
        F(50, 20) == F(5, 2))
    # 10 one quantity unchanged
    add("The ratio of the number of boys to the number of girls in a choir was 3 : 4. After 14 boys left the choir, "
        "the ratio became 1 : 2. How many boys were in the choir at first?", n(42, " boys"),
        [n(21, " boys"), n(28, " boys"), n(56, " boys"), n(98, " boys")],
        "The number of girls does not change. Make the girls the same: 3 : 4 and 1 : 2 = 2 : 4. "
        "Boys went from 3 units to 2 units, so 1 unit = 14. Boys at first: 3 × 14 = <b>42</b>. "
        "21 comes from 3 − 1 = 2 units, which changes the girls’ units.", F(42 - 14, 56) == F(1, 2) and F(42, 56) == F(3, 4))
    # 11 three-part mass
    add("A baker mixes flour, sugar and butter in the ratio 4 : 1 : 3 by mass. She uses 450 g of butter. "
        "How much flour does she use?", n(600, " g"), [n(1200, " g"), n(150, " g"), n(1800, " g"), n(1350, " g")],
        "Butter: 3 units = 450 g, so 1 unit = 150 g. Flour: 4 units = 4 × 150 = <b>600 g</b>. "
        "1800 g is 450 × 4, which uses 450 g as 1 unit.", 3 * 150 == 450)
    # 12 both change differently
    (A, _, _), (B, _, _) = P.two()
    f = fig(bar_svg([(A, 2, "", "+ 6", FILL_L), (B, 5, "", "− 18", FILL_Y)], None, None,
                    "bar model: %s 2 units, %s 5 units" % (A, B), cw=30))
    add(f + "The ratio of %s’s stickers to %s’s stickers was 2 : 5. %s bought 6 more stickers and %s gave away 18 stickers. "
        "Then they had the same number of stickers. How many stickers did %s have at first?" % (A, B, A, B, A),
        n(16, " stickers"), [n(22, " stickers"), n(40, " stickers"), n(8, " stickers"), n(56, " stickers")],
        "2 units + 6 = 5 units − 18. So 3 units = 6 + 18 = 24 and 1 unit = 8. %s at first: 2 × 8 = <b>16 stickers</b>. "
        "Check: 16 + 6 = 22 and 40 − 18 = 22." % A, 16 + 6 == 40 - 18)
    # 13 fraction equal fraction -> ratio
    (A, _, _), (B, _, _) = P.two()
    add("%s of %s’s marbles is equal to %s of %s’s marbles. What is the ratio of %s’s marbles to %s’s marbles?"
        % (fr(2, 3), A, fr(1, 2), B, A, B), Rc(3, 4), [Rc(4, 3), Rc(2, 1), Rc(2, 3), Rc(1, 2)],
        "Make the numerators the same: %s = %s. So 2 units are %s of %s’s marbles and %s of %s’s marbles. "
        "%s has 3 units and %s has 4 units: <b>3 : 4</b>. 4 : 3 is the wrong way round."
        % (fr(1, 2), fr(2, 4), fr(2, 3), A, fr(2, 4), B, A, B), F(2, 3) * 3 == F(1, 2) * 4)
    # 14 fraction equal fraction with total
    (A, _, _), (B, _, _) = P.two()
    add("%s of %s’s beads is equal to %s of %s’s beads. They have 132 beads altogether. How many beads does %s have?"
        % (fr(2, 5), A, fr(1, 3), B, B), n(72, " beads"), [n(60, " beads"), n(66, " beads"), n(24, " beads"), n(12, " beads")],
        "%s = %s, so %s has 5 units and %s has 6 units. 11 units = 132, so 1 unit = 12. %s: 6 × 12 = <b>72</b>. "
        "Check: %s of 60 = 24 and %s of 72 = 24." % (fr(1, 3), fr(2, 6), A, B, B, fr(2, 5), fr(1, 3)),
        F(2, 5) * 60 == F(1, 3) * 72 and 60 + 72 == 132)
    # 15 transfer to equal
    (A, _, _), (B, _, _) = P.two()
    add("The ratio of %s’s cards to %s’s cards was 7 : 5. After %s gave %s 9 cards, they had the same number of cards. "
        "How many cards did they have altogether?" % (A, B, A, B), n(108, " cards"),
        [n(18, " cards"), n(63, " cards"), n(45, " cards"), n(54, " cards")],
        "The total stays the same. 7 : 5 is 12 units. After, they are equal: 6 units each. %s gave 7 − 6 = 1 unit, "
        "so 1 unit = 9. Total: 12 × 9 = <b>108 cards</b>. 63 is what %s had at first." % (A, A), 63 - 9 == 45 + 9)
    # 16 transfer, totals different
    (A, _, _), (B, _, _) = P.two()
    add("The ratio of %s’s stamps to %s’s stamps was 5 : 3. After %s gave %s 21 stamps, the ratio became 1 : 3. "
        "How many stamps did %s have at first?" % (A, B, A, B, B), n(21, " stamps"),
        [n(42, " stamps"), n(35, " stamps"), n(56, " stamps"), n(7, " stamps")],
        "The total does not change. 5 : 3 has 8 units and 1 : 3 has 4 units, so make it 2 : 6 (8 units). "
        "%s went from 5 units to 2 units: 3 units = 21, so 1 unit = 7. %s at first: 3 × 7 = <b>21 stamps</b>. "
        "42 is the number %s has now." % (A, B, B), F(35 - 21, 21 + 21) == F(1, 3) and F(35, 21) == F(5, 3))
    # 17 tanks
    f = fig(bar_svg([("Tank A", 3, "", "?", FILL_B), ("Tank B", 1, "", "", FILL_Y)], None, None,
                    "bar model: Tank A 3 units, Tank B 1 unit", cw=40))
    add(f + "The ratio of the volume of water in Tank A to the volume of water in Tank B is 3 : 1. "
        "After 12 ℓ of water is poured from Tank A into Tank B, both tanks have the same volume of water. "
        "How much water was in Tank A at first?", n(36, " ℓ"), [n(24, " ℓ"), n(12, " ℓ"), n(48, " ℓ"), n(18, " ℓ")],
        "4 units in all, so each tank ends with 2 units. Tank A gives 3 − 2 = 1 unit = 12 ℓ. "
        "Tank A at first: 3 × 12 = <b>36 ℓ</b>. 24 ℓ is the volume in each tank after.", 36 - 12 == 12 + 12)
    # 18 three people, giving away a fraction
    (A, _, _), (B, _, _) = P.two()
    (C, _, _) = P.next()
    add("%s, %s and %s shared some stickers in the ratio 2 : 3 : 5. Then %s gave %s of %s stickers to %s. "
        "What is the new ratio of %s’s stickers to %s’s stickers to %s’s stickers?" % (A, B, C, C, fr(1, 5), "her" if C in GIRLS else "his", A, A, B, C),
        Rc(3, 3, 4), [Rc(2, 3, 4), Rc(3, 3, 5), Rc(3, 2, 4), Rc(2, 4, 4)],
        "%s of 5 units is 1 unit. %s: 2 + 1 = 3 units, %s: 3 units, %s: 5 − 1 = 4 units. New ratio: <b>3 : 3 : 4</b>. "
        "Remember to add the unit to %s too." % (fr(1, 5), A, B, C, A))
    # 19 prices
    nm, he, his = P.next()
    add("The ratio of the price of a pen to the price of a file is 2 : 3. %s paid $12 for 3 pens and 2 files. "
        "How much does one file cost?" % nm, M(3), [M(F(36, 5)), M(2), M(6), M(4)],
        "1 pen = 2 units and 1 file = 3 units. 3 pens + 2 files = 6 units + 6 units = 12 units = $12, so 1 unit = $1. "
        "1 file: 3 units = <b>$3</b>. $7.20 shares $12 in the ratio 2 : 3, which ignores how many of each were bought.",
        3 * 2 + 2 * 3 == 12)
    # 20 one quantity unchanged, find total at first
    add("At a magic show, the ratio of adults to children was 2 : 5. After 30 children left, the ratio became 4 : 7. "
        "How many people were at the show at first?", n(140, " people"),
        [n(110, " people"), n(100, " people"), n(40, " people"), n(70, " people")],
        "The number of adults does not change. Make the adults the same: 2 : 5 = 4 : 10, and after it is 4 : 7. "
        "Children went from 10 units to 7 units: 3 units = 30, so 1 unit = 10. "
        "At first: 4 + 10 = 14 units = <b>140 people</b>. 110 is the number of people after.",
        F(40, 100) == F(2, 5) and F(40, 70) == F(4, 7))
    assert len(its) == 20, len(its)
    return {"title": "PSLE-style ratio word problems", "items": its}


# ============================================================ lesson
def lesson():
    share = bar_svg([("Ali", 2, "$12", "$24", FILL_L), ("Siti", 3, "$12", "$36", FILL_Y)], "$60", None,
                    "bar model: Ali 2 units, Siti 3 units, total $60, each unit $12")
    diff = bar_svg([("Ali", 3, "", "", FILL_L), ("Siti", 5, "", "", FILL_Y)], None, (1, 3, 4, "$24"),
                   "bar model: Ali 3 units, Siti 5 units, difference $24")
    unch = bar_svg([("Ahmad, before", 3, "", "", FILL_L), ("Ahmad, after", 5, "", "", FILL_B), ("Mei Ling", 4, "", "", FILL_Y)],
                   None, None, "bar model: Ahmad 3 units before and 5 units after, Mei Ling 4 units unchanged", cw=30)
    tot = bar_svg([("Before: Wei Ming", 3, "", "", FILL_L), ("Hui Min", 1, "", "", FILL_Y),
                   ("After: Wei Ming", 2, "", "", FILL_L), ("Hui Min ", 2, "", "", FILL_Y)], None, None,
                  "bar model: before 3 units and 1 unit, after 2 units and 2 units", cw=30)
    return (
        "<h2>Units: the key to every ratio problem</h2>"
        "<p>A ratio tells you how many equal <b>units</b> each person has. In 2 : 3, the first person has 2 units and "
        "the second has 3 units. Every unit has the same value.</p>"
        "<p>The plan is always the same: <b>find what 1 unit is worth, then multiply</b>.</p>"
        + ex("Sharing a total", "Ali and Siti share $60 in the ratio 2 : 3. How much does each get?",
             "2 + 3 = 5 units. 5 units = $60, so 1 unit = $12. Ali: 2 × $12 = $24. Siti: 3 × $12 = $36.",
             "Ali $24, Siti $36")
        + "<figure class='sn-fig'>" + share + "<figcaption>5 equal units make $60. Check: $24 + $36 = $60.</figcaption></figure>"
        "<h2>When one part or the difference is given</h2>"
        "<p>Match the number you know with the right number of units.</p>"
        + ex("Difference given", "The ratio of Ali’s money to Siti’s money is 3 : 5. Siti has $24 more than Ali. How much does Ali have?",
             "The difference is 5 − 3 = 2 units. 2 units = $24, so 1 unit = $12. Ali: 3 × $12 = $36.", "$36")
        + "<figure class='sn-fig'>" + diff + "<figcaption>Siti’s 2 extra units are the $24 difference.</figcaption></figure>"
        "<h2>Before and after</h2>"
        "<p>First ask: <b>what stays the same?</b> Then make its units the same in both ratios.</p>"
        + table(["What happens", "What stays the same", "Make the same"], [
            ["One person buys, spends or gives away", "The other person’s amount", "That person’s units"],
            ["One person gives some to the other", "The total", "The total units"],
            ["Both get older, or both spend the same amount", "The difference", "The difference in units"],
        ])
        + ex("One quantity unchanged", "The ratio of Ahmad’s stickers to Mei Ling’s stickers was 3 : 4. Ahmad bought 16 more "
             "stickers and the ratio became 5 : 4. How many stickers does Mei Ling have?",
             "Mei Ling’s stickers do not change, and she has 4 units in both ratios. Ahmad went from 3 units to 5 units, "
             "so 2 units = 16 and 1 unit = 8. Mei Ling: 4 × 8 = 32.", "32 stickers")
        + "<figure class='sn-fig'>" + unch + "<figcaption>Mei Ling’s bar is the same before and after.</figcaption></figure>"
        + ex("Total unchanged", "The ratio of Wei Ming’s marbles to Hui Min’s marbles was 3 : 1. Wei Ming gave Hui Min 10 marbles. "
             "Then they had the same number. How many marbles did Wei Ming have at first?",
             "The total stays 4 units, so after they have 2 units each. Wei Ming gave 3 − 2 = 1 unit = 10. "
             "At first: 3 × 10 = 30.", "30 marbles")
        + "<figure class='sn-fig'>" + tot + "<figcaption>4 units before and 4 units after: the total is the same.</figcaption></figure>"
        "<p>If the units do not match, change one ratio first. For 2 : 3 before and 1 : 2 after, with the first amount "
        "unchanged, write 1 : 2 as 2 : 4.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Sharing $60 in 2 : 3 by working out $60 ÷ 2 or $60 ÷ 3", "Add the units first: 5 units = $60, so 1 unit = $12"],
            ["Treating the difference as 1 unit: “Siti has $24 more” so 1 unit = $24",
             "Count the units in the difference: 5 − 3 = 2 units = $24"],
            ["Changing the amount that stays the same", "Find what does not change and give it the same units in both ratios"],
            ["Comparing 5 : 3 and 1 : 3 directly when the total stays the same",
             "The totals are 8 and 4 units. Write 1 : 3 as 2 : 6 first"],
            ["Joining 2 : 3 and 4 : 5 into 2 : 3 : 5", "Make the shared amount the same: 8 : 12 and 12 : 15 give 8 : 12 : 15"],
        ])
    )


FAQ = [
    {"q": "How do you solve ratio word problems in P6?",
     "a": "Turn the ratio into units, find what 1 unit is worth, then multiply. For $60 shared in the ratio 2 : 3, 5 units = $60, so 1 unit = $12 and the shares are $24 and $36."},
    {"q": "What are before-and-after ratio questions?",
     "a": "They are problems where an amount changes and the ratio changes with it. Find what stays the same (one person’s amount, the total or the difference), give it the same number of units in both ratios, then compare."},
    {"q": "What is the most common mistake in ratio word problems?",
     "a": "Treating a given difference or total as 1 unit. If Siti has $24 more and the ratio is 3 : 5, the $24 is 2 units, so 1 unit is $12."},
    {"q": "Is ratio tested in the PSLE?",
     "a": "Yes. Ratio is part of the MOE Primary 6 syllabus, and PSLE Paper 2 often has multi-step ratio problems, including before-and-after and three-part ratios, that are best solved with bar models."},
]


def gen():
    rnd = random.Random(66805)
    P = People(rnd)
    sets = [set_share(rnd, P), set_one_part(rnd, P), set_difference(rnd, P), set_before_after(rnd, P), set_psle(rnd, P)]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            cnt[it["a"]] += 1
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "ratio-word-problems", "sort": 5,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Ratio Word Problems",
        "seo_title": "P6 Ratio Word Problems Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE)",
        "short_title": "Ratio word problems",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Ratio",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Solving word problems involving ratio",
        "meta_desc": "Free P6 ratio word problems: sharing, difference given, before-and-after and 3-part ratios with bar models. 100 PSLE-style questions with answers.",
        "key_big": "Change the ratio into units, find 1 unit, then multiply.",
        "key_sub": "Ratio 3 : 5 and Siti has $24 more: 2 units = $24, so 1 unit = $12 and Ali has 3 × $12 = $36.",
        "body_html": lesson(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "bar model")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
