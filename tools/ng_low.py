# -*- coding: utf-8 -*-
"""
Nigeria Primary 1–3 Mathematics: makers written for Nigeria (naira notes and coins with pictures, factors, fractions with the same denominator).
Each maker takes a random.Random and returns one item; AssertionError means "draw again".
MAX sets the largest amount for the money makers (Primary 1: ₦100, Primary 2: ₦500, Primary 3: ₦1,000).
"""
from fractions import Fraction as F
from ng_common import mcq, comma, naira, fig, fr, Kid, svg_wrap, text, GREEN, INK
from ng_p4a import K, ch

NOTES = {5: "#d8c9ec", 10: "#f4c7a8", 20: "#bfe3c3", 50: "#bcd7f0", 100: "#d9d2f2", 200: "#d7e8b4", 500: "#b7e1dc", 1000: "#e6d3b3"}
COINS = {1: "#e8d9a0", 2: "#d9d9d9"}
LEVEL = {"MAX": 100}


def note_svg(v, x, y):
    w, h = 118, 58
    b = "<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, w, h, NOTES[v], INK)
    b += "<rect x='%d' y='%d' width='%d' height='%d' rx='4' fill='none' stroke='%s' stroke-width='1'/>" % (x + 5, y + 5, w - 10, h - 10, INK)
    b += text(x + w / 2, y + h / 2 + 8, "₦%s" % comma(v), 22)
    return b, w


def coin_svg(v, x, y):
    r = 26
    b = "<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x + r, y + 29, r, COINS[v], INK)
    b += "<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='1'/>" % (x + r, y + 29, r - 5, INK)
    b += text(x + r, y + 37, "₦%d" % v, 18)
    return b, 2 * r


def money_svg(vals, label=None):
    """vals: naira values; 1 and 2 are coins, the rest are notes. Wraps after 4 pieces."""
    parts = []
    x, y, row_w, W = 6, 6, 0, 0
    for i, v in enumerate(vals):
        if i and i % 4 == 0:
            x, y = 6, y + 70
        b, w = (coin_svg if v in COINS else note_svg)(v, x, y)
        parts.append(b)
        x += w + 10
        W = max(W, x)
    return svg_wrap(W, y + 70, "".join(parts), label or "money: " + ", ".join("₦%s" % comma(v) for v in vals))


def denoms():
    m = LEVEL["MAX"]
    return [v for v in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000) if v <= m]


def mo_name(r):
    v = ch(r, denoms())
    kind = "coin" if v in COINS else "note"
    others = [x for x in denoms() if x != v]
    r.shuffle(others)
    return mcq("How much money is this %s?" % kind + fig(money_svg([v])), naira(v), [naira(x) for x in others], "This is a <b>%s</b> %s." % (naira(v), kind))


def mo_count(r):
    ds = denoms()
    n = r.randint(2, 4 if LEVEL["MAX"] <= 100 else 5)
    vals = sorted((ch(r, ds) for _ in range(n)), reverse=True)
    t = sum(vals)
    if t > LEVEL["MAX"]:
        raise AssertionError
    w = [t + ch(r, [1, 5, 10]), t - min(vals), max(vals) * n, t + max(vals) if t + max(vals) <= LEVEL["MAX"] * 2 else t - 1]
    return mcq("How much money is there altogether?" + fig(money_svg(vals)), naira(t), [naira(x) for x in w if x > 0],
               "Count on from the biggest: %s = <b>%s</b>." % (" + ".join(naira(v) for v in vals), naira(t)))


SHOP = [("an orange", 20, 100), ("a sweet", 5, 20), ("a pencil", 50, 200), ("a biscuit", 20, 100), ("a balloon", 20, 100), ("a sachet of pure water", 20, 50),
        ("an exercise book", 200, 500), ("a ruler", 100, 300), ("a meat pie", 300, 700), ("a bottle of water", 200, 400), ("a puff-puff", 20, 100),
        ("a packet of chin-chin", 100, 500), ("an eraser", 50, 150), ("a loaf of bread", 500, 1000), ("a pen", 100, 300), ("a bar of soap", 300, 800)]


def thing(r, top=None):
    top = top or LEVEL["MAX"]
    ok = [(n, lo, hi) for n, lo, hi in SHOP if lo <= top]
    n, lo, hi = ch(r, ok)
    step = 5 if hi <= 100 else 10 if hi <= 300 else 50
    return n, r.randint(lo // step, min(hi, top) // step) * step


def mo_add(r):
    k = K(r)
    a, pa = thing(r, LEVEL["MAX"] // 2)
    b, pb = thing(r, LEVEL["MAX"] // 2)
    if a == b:
        raise AssertionError
    t = pa + pb
    return mcq("%s buys %s for %s and %s for %s. How much does %s spend?" % (k["n"], a, naira(pa), b, naira(pb), k["he"]), naira(t),
               [naira(abs(pa - pb)) if pa != pb else naira(t + 10), naira(t + 10), naira(t - 5 if t > 5 else t + 20), naira(t + 100)],
               "%s + %s = <b>%s</b>." % (naira(pa), naira(pb), naira(t)))


def mo_change(r):
    k = K(r)
    a, p = thing(r)
    pay = min(x for x in denoms() + [LEVEL["MAX"]] if x > p) if p < LEVEL["MAX"] else None
    if not pay or pay == p:
        raise AssertionError
    c = pay - p
    return mcq("%s buys %s for %s. %s pays with a %s note. How much change does %s get?" % (k["n"], a, naira(p), k["He"], naira(pay), k["he"]), naira(c),
               [naira(pay + p), naira(c + 10), naira(c - 5) if c > 5 else naira(c + 20), naira(p)],
               "Change = %s − %s = <b>%s</b>." % (naira(pay), naira(p), naira(c)))


def mo_mult(r):
    k = K(r)
    a, p = thing(r, LEVEL["MAX"] // 4)
    n = r.randint(2, 6)
    plural = {"an orange": "oranges", "a sweet": "sweets", "a pencil": "pencils", "a biscuit": "biscuits", "a balloon": "balloons", "a sachet of pure water": "sachets of pure water",
              "a puff-puff": "puff-puffs", "an eraser": "erasers", "a ruler": "rulers", "a pen": "pens", "an exercise book": "exercise books", "a meat pie": "meat pies",
              "a bottle of water": "bottles of water", "a packet of chin-chin": "packets of chin-chin", "a bar of soap": "bars of soap", "a loaf of bread": "loaves of bread"}[a]
    return mcq("%s costs %s. %s buys %d %s. How much does %s pay?" % (a[0].upper() + a[1:], naira(p), k["n"], n, plural, k["he"]), naira(n * p),
               [naira(n + p), naira(n * p + p), naira((n - 1) * p), naira(n * p + 10)],
               "%d × %s = <b>%s</b>." % (n, naira(p), naira(n * p)))


def mo_which(r):
    ds = [x for x in denoms() if x >= 5]
    a, b = r.sample(ds, 2)
    big = max(a, b)
    return mcq("Which is worth more?" + fig(money_svg([a, b])), naira(big), [naira(min(a, b)), "They are the same", "You cannot tell"],
               "<b>%s</b> is more than %s." % (naira(big), naira(min(a, b))))


def mo_make(r):
    ds = [x for x in denoms() if x >= 5]
    t = ch(r, [x for x in ds if x >= 20])
    smaller = [x for x in ds if x < t]
    a = ch(r, smaller)
    rest = t - a
    k = rest // a if rest % a == 0 else None
    if not k or k > 4:
        raise AssertionError
    n = k + 1
    return mcq("How many %s notes make %s?" % (naira(a), naira(t)), n, [n + 1, n - 1 if n > 2 else n + 2, t // 10 if t // 10 not in (n,) else n + 3, t],
               "%s ÷ %s = <b>%d</b>." % (naira(t), naira(a), n))


# ============================================================ factors (Primary 3: up to 48)
def facs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def fac_is(r):
    n = r.randint(6, 48)
    fs = facs(n)
    if len(fs) < 3:
        raise AssertionError
    good = ch(r, [d for d in fs if 1 < d < n])
    bad = [d for d in range(2, n) if n % d]
    r.shuffle(bad)
    return mcq("Which number is a factor of %d?" % n, good, bad, "%d ÷ %d = %d exactly, so <b>%d</b> is a factor of %d." % (n, good, n // good, good, n))


def fac_missing(r):
    a, b = r.randint(2, 8), r.randint(2, 9)
    n = a * b
    if n > 48:
        raise AssertionError
    return mcq("Find the missing factor: %d × □ = %d" % (a, n), b, [n - a, b + 1, b - 1, n], "%d ÷ %d = <b>%d</b>." % (n, a, b))


def fac_list(r):
    n = r.randint(8, 48)
    fs = facs(n)
    if len(fs) < 4:
        raise AssertionError
    good = ", ".join(map(str, fs))
    w1 = ", ".join(map(str, fs[1:-1]))
    w2 = ", ".join(map(str, [n * i for i in range(1, 5)]))
    w3 = ", ".join(map(str, fs[:-1] + [fs[-1] + 1]))
    return mcq("Which list shows all the factors of %d?" % n, good, [w1, w2, w3], "Pairs that multiply to %d: %s. All the factors: <b>%s</b>." % (n, ", ".join("%d × %d" % (d, n // d) for d in fs if d * d <= n), good))


def fac_count(r):
    n = r.randint(6, 48)
    fs = facs(n)
    return mcq("How many factors does %d have?" % n, len(fs), [len(fs) + 1, len(fs) - 1, n // 2, 2 if len(fs) != 2 else 3], "The factors of %d are %s: <b>%d</b> factors." % (n, ", ".join(map(str, fs)), len(fs)))


def fac_not(r):
    n = r.randint(10, 48)
    fs = [d for d in facs(n) if d > 1]
    if len(fs) < 4:
        raise AssertionError
    good = ch(r, [d for d in range(2, n) if n % d])
    return mcq("Which number is <b>not</b> a factor of %d?" % n, good, r.sample(fs, 3), "%d ÷ %d leaves a remainder, so <b>%d</b> is not a factor." % (n, good, good))


# ============================================================ fractions with the same denominator (Primary 3)
def fr_same(r):
    d = ch(r, [3, 4, 5, 6, 8, 10])
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    add = r.random() < 0.5
    if add and a + b > d:
        raise AssertionError
    if not add and a <= b:
        raise AssertionError
    n = a + b if add else a - b
    ans = fr(n, d) if n < d else "1"
    w = [fr(n, 2 * d) if add else fr(n, d + 1), fr(a + b if not add else abs(a - b) or 1, d), fr(n + 1, d) if n + 1 < d else fr(n, d + 2), fr(n, d - 1) if n < d - 1 else fr(1, d)]
    return mcq("%s %s %s = ?" % (fr(a, d), "+" if add else "−", fr(b, d)), ans, [x for x in w if x != ans],
               "The bottom numbers are the same, so %s the top numbers: %d %s %d = %d. The answer is <b>%s</b>." % ("add" if add else "subtract", a, "+" if add else "−", b, n, ans if n < d else "%d/%d = 1" % (n, d)))


def fr_same_word(r):
    k = K(r)
    d = ch(r, [4, 5, 6, 8])
    a, b = r.randint(1, d - 2), r.randint(1, d - 2)
    if a + b >= d:
        raise AssertionError
    food = ch(r, ["an orange", "a cake", "a loaf of bread", "a pizza", "a bar of chocolate"])
    return mcq("%s cut %s into %d equal parts. %s ate %s and %s sister ate %s. What fraction did they eat altogether?" % (k["n"], food, d, k["He"], fr(a, d), k["his"], fr(b, d)),
               fr(a + b, d), [fr(a + b, 2 * d), fr(d - a - b, d), fr(a * b, d) if a * b < d and a * b != a + b else fr(a + b + 1, d), fr(1, d)],
               "%s + %s = <b>%s</b>." % (fr(a, d), fr(b, d), fr(a + b, d)))


def fr_left(r):
    d = ch(r, [4, 5, 6, 8, 10])
    a = r.randint(1, d - 1)
    food = ch(r, ["the cake", "the bread", "the pizza", "the watermelon"])
    return mcq("%s of %s has been eaten. What fraction is left?" % (fr(a, d), food), fr(d - a, d), [fr(a, d) if a != d - a else fr(1, d), fr(d - a, 2 * d), "1", fr(d, d - a) if d - a > 1 else fr(2, d)],
               "The whole is %s. %s − %s = <b>%s</b>." % (fr(d, d), fr(d, d), fr(a, d), fr(d - a, d)))


# ============================================================ Primary 1 pictures (k_pics)
import k_pics as KP

KIND1 = ["apple", "star", "ball", "button", "fish", "flower", "heart", "duck", "cup"]


def nm(kind, n):
    return KP.name(kind, n)


def p1_count(r):
    kind = ch(r, KIND1)
    n = r.randint(3, 20)
    pic = KP.scatter_svg(n, kind, r.randint(1, 10 ** 6)) if r.random() < 0.5 else KP.row_svg(n, kind)
    return mcq("How many %s are there?" % nm(kind, 2) + fig(pic), n, [n + 1, n - 1, n + 2, n - 2 if n > 3 else n + 3], "Count each one once: <b>%d</b>." % n)


def p1_next(r):
    a = r.randint(1, 96)
    k = r.randint(0, 2)
    if k == 0:
        seq = [a, a + 1, a + 2]
        ans = a + 3
        q = "What number comes next? %d, %d, %d, ?" % tuple(seq)
    elif k == 1:
        a = max(a, 2)
        ans = a - 1
        q = "What number comes just before %d?" % a
    else:
        ans = a + 1
        q = "What number is between %d and %d?" % (a, a + 2)
    if ans > 100:
        raise AssertionError
    return mcq(q, ans, [ans + 1, ans - 1, ans + 10 if ans + 10 <= 100 else ans - 10, ans + 2], "Count on in ones: <b>%d</b>." % ans)


def p1_rods(r):
    t, o = r.randint(1, 9), r.randint(0, 9)
    n = 10 * t + o
    w = [10 * o + t if o else n + 1, n + 10 if n + 10 < 100 else n - 10, t + o, n + 1 if o else n - 1]
    return mcq("How many cubes are there? Each tall rod is 1 ten." + fig(KP.rods_svg(t, o)), n, w, "%d tens and %d units make <b>%d</b>." % (t, o, n))


def p1_cmp(r):
    k1, k2 = r.sample(KIND1, 2)
    a, b = r.sample(range(2, 11), 2)
    more = r.random() < 0.5
    ans = nm(k1, 2) if (a > b) == more else nm(k2, 2)
    other = nm(k2, 2) if ans == nm(k1, 2) else nm(k1, 2)
    return mcq(("Which group has more?" if more else "Which group has fewer?") + fig(KP.two_groups_svg(a, k1, b, k2, word="and")),
               ans.capitalize(), [other.capitalize(), "They are the same", "You cannot tell"],
               "There are %d %s and %d %s. The %s %s." % (a, nm(k1, a), b, nm(k2, b), ans, "are more" if more else "are fewer"))


def p1_add(r):
    kind = ch(r, KIND1)
    a, b = r.randint(1, 10), r.randint(1, 10)
    if a + b > 20:
        raise AssertionError
    return mcq("%d + %d = ?" % (a, b) + fig(KP.two_groups_svg(a, kind, b, kind, word="+")), a + b, [a + b + 1, a + b - 1, abs(a - b) if a != b else a + b + 2, a + b + 2],
               "Put them together and count: %d + %d = <b>%d</b>." % (a, b, a + b))


def p1_sub(r):
    kind = ch(r, KIND1)
    n = r.randint(3, 15)
    k = r.randint(1, n - 1)
    return mcq("%d − %d = ?" % (n, k) + fig(KP.crossed_row_svg(n, kind, k)), n - k, [n - k + 1, n - k - 1 if n - k > 1 else n - k + 2, n + k if n + k <= 20 else n, k],
               "%d take away %d leaves <b>%d</b>." % (n, k, n - k))


def p1_ten(r):
    n = r.randint(1, 9)
    return mcq("How many more dots are needed to make 10?" + fig(KP.tenframe_svg(n)), 10 - n, [n, 10 - n + 1, 10 - n - 1 if 10 - n > 1 else 10 - n + 2, 10],
               "There are %d dots. %d + %d = 10, so <b>%d</b> more." % (n, n, 10 - n, 10 - n))


def p1_bond(r):
    w = r.randint(5, 20)
    a = r.randint(1, w - 1)
    return mcq("%d and □ make %d. What is □?" % (a, w), w - a, [w + a, w - a + 1, w - a - 1 if w - a > 1 else w - a + 2, a],
               "%d + %d = %d, so □ = <b>%d</b>." % (a, w - a, w, w - a))


def p1_twos(r):
    st = ch(r, [2, 5, 10])
    a = st * r.randint(1, 6)
    seq = [a + st * i for i in range(4)]
    ans = seq[-1] + st
    if ans > 100:
        raise AssertionError
    return mcq("Count in %ds. What comes next? %s, ?" % (st, ", ".join(map(str, seq))), ans, [seq[-1] + 1, ans + st, ans - 1, seq[-1]],
               "Add %d each time: %d + %d = <b>%d</b>." % (st, seq[-1], st, ans))


def p1_chart(r):
    ncols, nrows = 3, 3
    c0 = r.randint(0, 10 - ncols)
    r0 = r.randint(0, 10 - nrows)
    tl = r0 * 10 + c0 + 1
    tr, tc = r.randrange(nrows), r.randrange(ncols)
    if (tr, tc) == (1, 1) and r.random() < 0.5:
        raise AssertionError
    ans = tl + 10 * tr + tc
    return mcq("This is part of a hundred square. Which number goes in the box with the ?" + fig(KP.chart_svg(tl, nrows, ncols, target=(tr, tc))), ans,
               [ans + 1, ans - 1, ans + 10 if ans + 10 <= 100 else ans - 10, ans - 10 if ans > 10 else ans + 2],
               "Across, numbers go up by 1. Down, they go up by 10. The missing number is <b>%d</b>." % ans)


def p1_word(r):
    from ng_common import words
    n = r.randint(11, 100)
    if r.random() < 0.5:
        w = [n + 10 if n <= 90 else n - 10, int(str(n)[::-1]) if n % 10 and n < 100 else n + 1, n + 1, n - 1]
        return mcq("Write <b>%s</b> in figures." % words(n), n, w, "%s = <b>%d</b>." % (words(n).capitalize(), n))
    good = words(n)
    w = [words(x) for x in (n + 10 if n <= 90 else n - 10, n + 1, n - 1, int(str(n)[::-1]) if n % 10 and n < 100 and int(str(n)[::-1]) != n else n - 2)]
    return mcq("How do we write %d in words?" % n, good, w, "%d = <b>%s</b>." % (n, good))


def p1_tu_word(r):
    k = K(r)
    t, o = r.randint(1, 9), r.randint(1, 9)
    n = 10 * t + o
    what = ch(r, [("bundles of 10 sticks", "loose sticks", "sticks"), ("crates of 10 eggs", "single eggs", "eggs"), ("bags of 10 sweets", "loose sweets", "sweets"),
                  ("packs of 10 pencils", "single pencils", "pencils"), ("boxes of 10 chalk", "loose pieces of chalk", "pieces of chalk")])
    if r.random() < 0.5:
        return mcq("%s has %d %s and %d %s. How many %s are there?" % (k["n"], t, what[0], o, what[1], what[2]), n, [10 * o + t if o != t else n + 1, t + o, n + 10 if n < 90 else n - 10, n - 1],
                   "%d tens and %d units = <b>%d</b>." % (t, o, n))
    return mcq("%s has %d %s. How many full tens can %s make?" % (k["n"], n, what[2], k["he"]), t, [o, t + 1, n, t - 1 if t > 1 else t + 2],
               "%d = %d tens and %d units, so <b>%d</b> tens." % (n, t, o, t))
