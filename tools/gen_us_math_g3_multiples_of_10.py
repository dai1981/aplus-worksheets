# -*- coding: utf-8 -*-
"""
US Grade 3 Math: Multiply by Multiples of 10 (3.NBT.A.3)
  python tools/gen_us_math_g3_multiples_of_10.py
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-11-01"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
GRAY = "#8a8a8a"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead == "0":
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    ch = pick + [correct]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(correct), "e": e}


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


def tens(n):
    return "1 ten" if n == 1 else "%d tens" % n


def rods_svg(groups, per, big=False):
    """`groups` circled groups, each with `per` base-ten rods (a rod = 10 small squares)."""
    sq = 12 if big else 10                       # one small square
    gap, pad, ggap, m = 4, 7, 10, 4
    gw = 2 * pad + per * sq + (per - 1) * gap
    gh = 2 * pad + 10 * sq
    W = 2 * m + groups * gw + (groups - 1) * ggap
    H = 2 * m + gh
    s = []
    for g in range(groups):
        gx = m + g * (gw + ggap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='2' "
                 "stroke-dasharray='5 3'/>" % (gx, m, gw, gh, GRAY))
        for r in range(per):
            x = gx + pad + r * (sq + gap)
            y = m + pad
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, sq, 10 * sq, FILL, GREEN))
            for k in range(1, 10):
                s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='0.8'/>"
                         % (x, y + k * sq, x + sq, y + k * sq, GREEN))
    label = "%d group%s of %s" % (groups, "" if groups == 1 else "s", tens(per))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='%s'>%s</svg>" % (W, H, W, H, label, "".join(s)))


# ------------------------------------------------------------ reasoning and typical mistakes
def expr(a, m, first):
    """a is the one-digit factor, m the multiple of 10. first=True writes the multiple first (70 × 3)."""
    return "%d × %d" % (m, a) if first else "%d × %d" % (a, m)


def tens_e(a, m, first=False):
    t = m // 10
    p = a * m
    s = "%s = %d × %s = %s = %d." % (expr(a, m, first), a, tens(t), tens(a * t), p)
    if first:
        s = "%d is %s. " % (m, tens(t)) + s
    if (a * t) % 10 == 0:
        s += (" The fact %d × %d = %d already ends in 0, but the answer counts tens: %d tens = %d. "
              "So %d has two zeros." % (a, t, a * t, a * t, p, p))
    return s


def mult_cands(a, m, rnd):
    """Wrong products from real mistakes. The first one is always the 'forgot the tens' answer."""
    t = m // 10
    p = a * m
    near = [a * (t + 1) * 10 if t < 9 else a * (t - 1) * 10,      # wrong basic fact (neighbor)
            (a + 1) * m if a < 9 else (a - 1) * m]
    rest = [p * 10, a + m] + near                               # extra zero, added instead
    rnd.shuffle(rest)
    return [a * t] + rest


# ------------------------------------------------------------ set 1: base-ten rods
def set_rods(rnd):
    pool = [(g, t) for g in range(1, 7) for t in range(1, 7) if g * t <= 16 and (g, t) != (1, 1)
            and not (g == 1 and t < 4) and not (t == 1 and g < 3)]
    rnd.shuffle(pool)
    ones = [x for x in pool if x[0] == 1][:2]
    rest = [x for x in pool if x[0] != 1][:18]
    pairs = ones + rest
    rnd.shuffle(pairs)
    its = []
    for i, (g, t) in enumerate(pairs):
        p = g * t * 10
        picture = fig(rods_svg(g, t))
        look = ("Each rod is 1 ten. There is 1 group of %s. " % tens(t)) if g == 1 else (
            "Each rod is 1 ten. There are %d groups with %s in each group. " % (g, tens(t)))
        kind = i % 3
        if kind == 0:
            its.append(mcq(picture + "How many squares are there in all?", p,
                           [g * t, (g + t) * 10, p * 10, g * (t + 1) * 10, (g + 1) * t * 10],
                           look + "%d × %s = %s = %d." % (g, tens(t), tens(g * t), p), rnd))
        elif kind == 1:
            its.append(mcq(picture + "How many tens are there in all?", tens(g * t),
                           [tens(g + t), tens(g * t * 10), tens(t), tens(g * (t + 1))],
                           look + "%d × %s = %s. That is %d." % (g, tens(t), tens(g * t), p), rnd))
        else:
            its.append(mcq(picture + "Which multiplication matches this picture?", "%d × %d" % (g, t * 10),
                           ["%d × %d" % (g, t), "%d + %d" % (g, t * 10), "%d × %d" % (g * 10, t * 10),
                            "%d × %d" % (g + 1, t * 10)],
                           look + "%s is %d, so the picture shows %d × %d = %d." % (cap(tens(t)), t * 10, g, t * 10, p), rnd))
    return {"title": "Groups of tens with base-ten rods", "items": its}


# ------------------------------------------------------------ set 2: think in tens
def set_think(rnd, seen):
    its = []
    # a × t tens = ? tens
    pairs = [(a, t) for a in range(2, 10) for t in range(2, 10)]
    rnd.shuffle(pairs)
    for a, t in pairs[:7]:
        its.append(mcq("%d × %s = ☐ tens" % (a, tens(t)), tens(a * t),
                       [tens(a + t), tens(a * t * 10), tens(a * (t + 1) if t < 9 else a * (t - 1))],
                       "%d groups of %s is %d × %d = %s. So %d × %d = %d." % (a, tens(t), a, t, tens(a * t), a, t * 10, a * t * 10),
                       rnd))
    # N tens = ?
    ns = [12, 15, 18, 20, 21, 24, 27, 28, 30, 32, 35, 36, 42, 45, 48, 54, 56, 63, 64, 72, 81]
    for n in rnd.sample(ns, 6):
        h, r = divmod(n, 10)
        split = ("%d tens = %d hundreds = %d." % (n, h, n * 10)) if r == 0 else (
            "%d tens = %d tens + %s = %d + %d = %d." % (n, h * 10, tens(r), h * 100, r * 10, n * 10))
        its.append(mcq("%d tens = ☐" % n, n * 10, [n, n * 100, n + 10],
                       "10 tens make 100. " + split, rnd))
    # a × m with the tens hint
    k = 0
    for a, t in pairs[7:]:
        if (a * t) % 10 == 0 or (a, t) in seen:
            continue
        seen.add((a, t))
        m = t * 10
        its.append(mcq("Think in tens. What is %d × %d?" % (a, m), a * m, mult_cands(a, m, rnd), tens_e(a, m), rnd))
        k += 1
        if k == 7:
            break
    rnd.shuffle(its)
    return {"title": "Think in tens", "items": its}


# ------------------------------------------------------------ set 3: facts, either order
def set_facts(rnd, seen):
    zero = [(2, 5), (4, 5), (6, 5), (8, 5), (5, 2), (5, 4), (5, 6), (5, 8)]
    rnd.shuffle(zero)
    pairs = zero[:7]
    tens10 = [(a, 1) for a in rnd.sample(range(3, 10), 2)]
    one = [(1, t) for t in rnd.sample(range(3, 10), 2)]
    pairs += tens10 + one
    others = [(a, t) for a in range(2, 10) for t in range(2, 10)
              if (a * t) % 10 and (a, t) not in seen and a != t]
    rnd.shuffle(others)
    # spread: make sure every a and t from 2 to 9 appears at least once
    need_a, need_t = set(range(2, 10)), set(range(2, 10))
    for a, t in pairs:
        need_a.discard(a)
        need_t.discard(t)
    chosen = []
    for a, t in others:
        if len(chosen) == 9:
            break
        if a in need_a or t in need_t or (not need_a and not need_t):
            chosen.append((a, t))
            need_a.discard(a)
            need_t.discard(t)
    assert not need_a and not need_t and len(chosen) == 9, (need_a, need_t, chosen)
    pairs += chosen
    rnd.shuffle(pairs)
    its = []
    for i, (a, t) in enumerate(pairs):
        m = t * 10
        first = i % 2 == 1
        seen.add((a, t))
        its.append(mcq("%s = ?" % expr(a, m, first), a * m, mult_cands(a, m, rnd), tens_e(a, m, first), rnd))
    return {"title": "Multiply by 10, 20, 30 … 90", "items": its}


# ------------------------------------------------------------ set 4: missing factors and comparing
def set_missing(rnd):
    its = []
    pairs = [(a, t) for a in range(2, 10) for t in range(2, 10) if a != t]
    rnd.shuffle(pairs)
    pi = iter(pairs)
    for _ in range(5):                       # ☐ × 60 = 420
        a, t = next(pi)
        m, p = t * 10, a * t * 10
        its.append(mcq("What number goes in the box?  <b>☐ × %d = %d</b>" % (m, p), a,
                       [a * 10, p // 10, a + 1 if a < 9 else a - 1, a - 1 if a > 2 else a + 2],
                       "%d is %s and %d is %s. ☐ × %d tens = %d tens, and %d × %d = %d. So the missing number is %d. "
                       "Check: %d × %d = %d." % (m, tens(t), p, tens(a * t), t, a * t, a, t, a * t, a, a, m, p), rnd))
    for _ in range(5):                       # 8 × ☐ = 560
        a, t = next(pi)
        m, p = t * 10, a * t * 10
        its.append(mcq("What number goes in the box?  <b>%d × ☐ = %d</b>" % (a, p), m,
                       [t, m * 10, m + 10 if t < 9 else m - 10, m - 10 if t > 2 else m + 20],
                       "%d is %s. %d × ☐ tens = %d tens, and %d × %d = %d. So the missing number is %s = %d. "
                       "Check: %d × %d = %d." % (p, tens(a * t), a, a * t, a, t, a * t, tens(t), m, a, m, p), rnd))
    # which is equal
    by_p = {}
    for a in range(2, 10):
        for t in range(2, 10):
            by_p.setdefault(a * t, []).append((a, t))
    multi = sorted(p for p, v in by_p.items() if len(v) >= 3)
    for P in rnd.sample(multi, 5):
        opts = by_p[P][:]
        rnd.shuffle(opts)
        (a, t), (b, u) = opts[0], [o for o in opts[1:] if o != (opts[0][1], opts[0][0])][0]
        m, n = t * 10, u * 10
        right = "%d × %d" % (b, n)
        wrong = ["%d × %d" % (a, t), "%d × %d" % (b, n + 10 if u < 9 else n - 10),
                 "%d × %d" % (a * 10, m), "%d × %d" % (b + 1, n)]
        its.append(mcq("Which is equal to %d × %d?" % (a, m), right, wrong,
                       "%d × %d = %s = %d. %d × %d = %s = %d. Both are %d." % (a, m, tens(a * t), a * m, b, n, tens(b * u), b * n, a * m),
                       rnd))
    # greatest / least: the trap is choosing the biggest-looking factor
    for kind in ["greatest", "greatest", "greatest", "least", "least"]:
        while True:
            four = rnd.sample([(a, t) for a in range(2, 10) for t in range(2, 10)], 4)
            prods = [a * t for a, t in four]
            if len(set(prods)) < 4 or max(prods) - min(prods) > 30:
                continue
            best = max(four, key=lambda x: x[0] * x[1]) if kind == "greatest" else min(four, key=lambda x: x[0] * x[1])
            looks = max(four, key=lambda x: x[1]) if kind == "greatest" else min(four, key=lambda x: x[1])
            if looks != best and len({x[1] for x in four}) == 4:
                break
        exs = ["%d × %d" % (a, t * 10) for a, t in four]
        listing = ", ".join("%d × %d = %d" % (a, t * 10, a * t * 10) for a, t in sorted(four, key=lambda x: -x[0] * x[1]))
        right = "%d × %d" % (best[0], best[1] * 10)
        its.append(mcq("Which product is the %s?" % kind, right, [x for x in exs if x != right],
                       "Think in tens to find each product: %s. The %s is %s = %d." % (listing, kind, right, best[0] * best[1] * 10),
                       rnd))
    rnd.shuffle(its)
    return {"title": "Missing factors and comparing products", "items": its}


# ------------------------------------------------------------ set 5: word problems
# (story with {n} {he} {his} {He} {a} {m}, unit word, explanation lead, allowed a, allowed m)
STORIES = [
    ("{n} buys {a} boxes of crayons. Each box has {m} crayons. How many crayons does {he} buy?",
     "crayons", "{a} boxes of {m} crayons", range(2, 7), [20, 30, 40, 50]),
    ("A school sends {a} buses on a field trip. Each bus has {m} seats. How many seats are there in all?",
     "seats", "{a} buses with {m} seats each", range(2, 8), [40, 50, 60]),
    ("{n} practices piano for {m} minutes a day for {a} days. How many minutes does {he} practice in all?",
     "minutes", "{a} days of {m} minutes", range(3, 8), [10, 20, 30, 40]),
    ("{n} saves ${m} each month for {a} months. How much money does {he} save?",
     "$", "{a} months of ${m}", range(3, 10), [10, 20, 30]),
    ("Tickets for a show cost ${m} each. {n} buys {a} tickets for {his} family. How much does {he} pay?",
     "$", "{a} tickets at ${m} each", range(2, 7), [20, 30, 40, 50]),
    ("A farmer plants {a} rows of corn. There are {m} plants in each row. How many plants are there in all?",
     "plants", "{a} rows of {m} plants", range(4, 10), [30, 40, 50, 60, 70, 80, 90]),
    ("Stickers come in packs of {m}. {n} buys {a} packs. How many stickers does {he} get?",
     "stickers", "{a} packs of {m} stickers", range(3, 10), [10, 20]),
    ("A bakery puts {m} cookies on each tray. It bakes {a} trays. How many cookies does it bake?",
     "cookies", "{a} trays of {m} cookies", range(3, 10), [20, 30, 40]),
    ("A train travels {m} miles each hour. How many miles does it travel in {a} hours?",
     "miles", "{a} hours of {m} miles", range(2, 6), [50, 60, 70, 80, 90]),
    ("{n} reads {m} pages of a book every day. How many pages does {he} read in {a} days?",
     "pages", "{a} days of {m} pages", range(3, 8), [10, 20, 30]),
    ("A theater has {a} rows. Each row has {m} seats. How many seats does the theater have?",
     "seats", "{a} rows of {m} seats", range(5, 10), [20, 30, 40]),
    ("A store gets {a} cases of water. Each case has {m} bottles. How many bottles does the store get?",
     "bottles", "{a} cases of {m} bottles", range(4, 10), [20, 30, 40]),
    ("A photo album has {a} pages. Each page holds {m} photos. How many photos fit in the album?",
     "photos", "{a} pages of {m} photos", range(5, 10), [10, 20]),
    ("{n} walks {his} dog for {m} minutes every morning. How many minutes is that in {a} days?",
     "minutes", "{a} days of {m} minutes", range(5, 8), [20, 30, 40]),
    ("A school buys {a} packs of pencils. Each pack has {m} pencils. How many pencils does the school buy?",
     "pencils", "{a} packs of {m} pencils", range(4, 10), [10, 20, 30]),
    ("A garden has {a} flower beds. Each bed has {m} tulips. How many tulips are there in all?",
     "tulips", "{a} beds of {m} tulips", range(2, 10), [30, 40, 50, 60, 70, 80, 90]),
    ("A pet store has {a} fish tanks with {m} fish in each tank. How many fish are there in all?",
     "fish", "{a} tanks of {m} fish", range(2, 10), [10, 20, 30, 40]),
]

# missing factor stories: (text with {n} {he} {p} {m}, unit of the answer, explanation)
MISSING = [
    ("{n} needs {p} paper cups for a party. Cups come in packs of {m}. How many packs does {he} need?", "packs"),
    ("A class collected {p} cans. They put {m} cans in each bag. How many bags did they fill?", "bags"),
    ("Chairs are set up in rows of {m}. There are {p} chairs. How many rows are there?", "rows"),
]


def money(v):
    return "$%d" % v


def set_story(rnd, P):
    its = []
    used = set()
    fact_count = {}
    for i, (t, unit, lead, arange, mrange) in enumerate(STORIES):
        while True:
            a, m = rnd.choice(list(arange)), rnd.choice(mrange)
            if (a, m) not in used and fact_count.get(a, 0) < 3:
                break
        used.add((a, m))
        fact_count[a] = fact_count.get(a, 0) + 1
        n, he, his = P.next()
        q = t.format(n=n, he=he, his=his, a=a, m=m)
        p = a * m
        fmt = money if unit == "$" else (lambda v, u=unit: "%d %s" % (v, u))
        e = "Equal groups: %s. " % lead.format(a=a, m=m) + tens_e(a, m) + " The answer is %s." % fmt(p)
        its.append(mcq(q, fmt(p), [fmt(v) for v in mult_cands(a, m, rnd)], e, rnd))
    for t, unit in MISSING:
        while True:
            a, m = rnd.randint(3, 9), rnd.choice([20, 30, 40, 50, 60])
            if (a, m) not in used:
                break
        used.add((a, m))
        n, he, his = P.next()
        p = a * m
        q = t.format(n=n, he=he, p=p, m=m)
        e = ("Think: ☐ × %d = %d. %d is %s and %d is %s. ☐ × %d = %d, so the answer is %d %s. Check: %d × %d = %d."
             % (m, p, m, tens(m // 10), p, tens(p // 10), m // 10, p // 10, a, unit, a, m, p))
        its.append(mcq(q, "%d %s" % (a, unit),
                       ["%d %s" % (v, unit) for v in [a * 10, p // 10, a + 1, a - 1]], e, rnd))
    assert len(its) == 20, len(its)
    rnd.shuffle(its)
    return {"title": "Word problems with tens", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>40 is 4 tens</h2>"
        "<p>A multiple of 10 is a number of <b>tens</b>: 40 is 4 tens and 70 is 7 tens. "
        "So <b>3 × 40</b> means 3 groups of 4 tens. Multiply the tens: 3 × 4 tens = <b>12 tens</b>. "
        "12 tens is 120.</p>"
        "<figure class='sn-fig'>" + rods_svg(3, 4, big=True) +
        "<figcaption>3 groups of 4 tens. Count the rods: 12 tens. Each rod is 10, so the total is 120. "
        "3 × 40 = 120.</figcaption></figure>"
        "<h2>See the pattern</h2>"
        "<p>Use the basic fact, then remember that you counted <b>tens</b>. That is why the product ends in 0.</p>" +
        table(["Basic fact", "Think in tens", "Product"], [
            ["3 × 4 = 12", "3 × 4 tens = 12 tens", "3 × 40 = <b>120</b>"],
            ["8 × 7 = 56", "8 × 7 tens = 56 tens", "8 × 70 = <b>560</b>"],
            ["9 × 1 = 9", "9 × 1 ten = 9 tens", "9 × 10 = <b>90</b>"],
            ["6 × 5 = 30", "6 × 5 tens = 30 tens", "6 × 50 = <b>300</b>"],
        ]) +
        ex("Example", "7 × 60 = ?", "60 is 6 tens. 7 × 6 tens = 42 tens. 42 tens = 420.", "420") +
        ex("Facts that end in 0", "5 × 80 = ?",
           "5 × 8 = 40, so 5 × 8 tens = 40 tens. 40 tens = 400. The answer has two zeros: one from the fact and one from the tens.", "400") +
        ex("Either order", "90 × 4 = ?",
           "The order of the factors does not change the product: 90 × 4 = 4 × 90. 4 × 9 tens = 36 tens = 360.", "360") +
        ex("Missing factor", "☐ × 30 = 240",
           "240 is 24 tens and 30 is 3 tens. ☐ × 3 = 24, so ☐ = 8. Check: 8 × 30 = 240.", "8") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting the tens (6 × 40 = 24)", "24 is the number of tens. 24 tens = 240"],
            ["Dropping a zero when the fact ends in 0 (5 × 80 = 40)", "5 × 8 tens = 40 tens = 400"],
            ["Writing too many zeros (6 × 40 = 2400)", "Only one factor is tens, so the answer is tens, not hundreds"],
            ["Adding the numbers (6 × 40 = 46)", "× means groups: 6 groups of 40"],
        ])
    )


FAQ = [
    {"q": "How do you multiply by multiples of 10 in 3rd grade?",
     "a": "Think of the multiple of 10 as tens. For 6 × 40, 40 is 4 tens, so 6 × 4 tens = 24 tens, and 24 tens is 240."},
    {"q": "Why does the answer end in zero when you multiply by 10, 20 or 30?",
     "a": "Because you are counting tens. 3 × 20 is 3 × 2 tens = 6 tens, and 6 tens is 60. The zero shows that the answer is a number of tens, not ones."},
    {"q": "Why does 5 × 80 equal 400 and not 40?",
     "a": "5 × 8 = 40, so 5 × 8 tens = 40 tens. 40 tens is 400. The fact already ends in 0, and the tens add one more zero."},
    {"q": "What does 3.NBT.A.3 mean?",
     "a": "It is the Common Core Grade 3 standard for multiplying a one-digit number by a multiple of 10 from 10 to 90, such as 9 × 80 or 5 × 60, using place value and properties of operations."},
]


def gen_multiples_of_10():
    rnd = random.Random(44)
    P = People(rnd)
    seen = set()
    sets = [set_rods(rnd), set_think(rnd, seen), set_facts(rnd, seen), set_missing(rnd), set_story(rnd, P)]
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
    return {
        "country": "us", "subject": "math", "grade": "grade-3", "slug": "multiply-by-multiples-of-10", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiply by Multiples of 10",
        "seo_title": "Grade 3 Multiply by Multiples of 10 Worksheets: 10–90, Base-Ten Rods and Word Problems",
        "short_title": "Multiply by multiples of 10",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "3.NBT.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/3/NBT/A/3/",
        "standard_text": "Multiply one-digit whole numbers by multiples of 10 in the range 10–90 (e.g., 9 × 80, 5 × 60) using strategies based on place value and properties of operations.",
        "meta_desc": "Free Grade 3 worksheets for multiplying by multiples of 10 (10–90): base-ten rod pictures, thinking in tens, facts like 5 × 80, missing factors, comparing products and word problems. 100 practice questions with step-by-step answers.",
        "key_big": "40 is 4 tens. So 6 × 40 = 6 × 4 tens = 24 tens = 240.",
        "key_sub": "Use the basic fact and count in tens. When the fact already ends in 0, keep both zeros: 5 × 80 = 40 tens = 400.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_multiples_of_10()
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
