# -*- coding: utf-8 -*-
"""
South Africa Grade 4 Maths (CAPS): Solving Problems: Money, Rate and Ratio (Grade 4: 1.1 Whole numbers)
  python3 tools/gen_za_maths_g4_money_rate_ratio.py
Rand and cents, shopping and change at the spaza shop, rates such as rand per kilogram, and sharing in a ratio (own
makers with rand and South African contexts).
Wrong answers come from real mistakes: writing R2,50 as 25c, giving the cost instead of the change, and sharing
equally when the story gives a ratio.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)

za_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


ITEMS = [("a loaf of bread", "loaves of bread", 17, 22), ("a litre of milk", "litres of milk", 18, 25), ("a packet of chips", "packets of chips", 9, 15),
         ("a koeksister", "koeksisters", 6, 9), ("a vetkoek", "vetkoeks", 8, 12), ("a cooldrink", "cooldrinks", 12, 18), ("an exercise book", "exercise books", 15, 28),
         ("a box of crayons", "boxes of crayons", 25, 45), ("a soccer ball", "soccer balls", 120, 250), ("a pair of school socks", "pairs of school socks", 30, 48)]


def one_buy(r):
    k = Kid(r).next()
    (a1, a, la, ha), (b, _, lb, hb) = r.sample(ITEMS, 2)
    pa, pb = r.randint(la, ha), r.randint(lb, hb)
    na = r.randint(2, 4)
    cost = na * pa + pb
    note = min(x for x in (50, 100, 200, 500, 1000) if x > cost)
    if r.random() < 0.5:
        q = "%s buys %d %s at %s each and %s for %s at the spaza shop. How much does %s pay?" % (k["n"], na, a, rand(pa), b, rand(pb), k["he"])
        return mcq(q, rand(cost), [rand(x) for x in (pa + pb, na * (pa + pb), cost + 10)], "%d × %s = %s. %s + %s = <b>%s</b>." % (na, rand(pa), rand(na * pa), rand(na * pa), rand(pb), rand(cost)))
    q = "%s buys %d %s at %s each and %s for %s. %s pays with a %s note. How much change does %s get?" % (k["n"], na, a, rand(pa), b, rand(pb), k["He"], rand(note), k["he"])
    return mcq(q, rand(note - cost), [rand(x) for x in (cost, note - pa - pb, note - cost + 10)], "Cost: %s. Change: %s − %s = <b>%s</b>." % (rand(cost), rand(note), rand(cost), rand(note - cost)))


def one_rc(r):
    kind = r.choice(["r2c", "c2r", "add"])
    if kind == "r2c":
        rr, c = r.randint(1, 25), r.choice([0, 10, 20, 50, 75, 90])
        v = rr * 100 + c
        return mcq("How many cents are there in <b>%s</b>?" % rand(v / 100), "%sc" % comma(v), ["%sc" % comma(x) for x in (rr * 10 + c, rr + c, v * 10)],
                   "R1 = 100c. %d × 100c + %dc = <b>%sc</b>." % (rr, c, comma(v)))
    if kind == "c2r":
        v = r.choice([x for x in range(105, 2500, 5) if x % 100])
        return mcq("Write <b>%sc</b> in rand." % comma(v), rand(v / 100), [rand(x) for x in (v / 10, v, v // 100 + 0.0)] if v // 100 else [rand(v / 10), rand(v), rand(v / 1000)],
                   "100c = R1, so %sc = <b>%s</b>." % (comma(v), rand(v / 100)))
    a, b = r.choice([150, 250, 350, 450, 650, 850]), r.choice([75, 125, 225, 375, 495])
    return mcq("Add <b>%s + %s</b>." % (rand(a / 100), rand(b / 100)), rand((a + b) / 100), [rand(x / 100) for x in (a + b + 100, a + b - 10, (a // 100 + b // 100) * 100)],
               "Rand first, then cents: %s. <b>%s</b>." % ("%dc + %dc = %dc" % (a, b, a + b), rand((a + b) / 100)))


RATE = [("Tomatoes cost %s per kilogram. How much do %d kg cost?", "kg"), ("Petrol costs %s per litre. How much do %d litres cost?", "l"),
        ("A taxi fare is %s per trip. How much do %d trips cost?", "trip"), ("Bananas cost %s per kilogram. How much do %d kg cost?", "kg")]


def one_rate(r):
    t, u = r.choice(RATE)
    p = r.choice([12, 14, 15, 18, 22, 24, 25]) if u != "l" else r.choice([21, 22, 23, 24])
    n = r.randint(2, 9)
    if r.random() < 0.5:
        return mcq(t % (rand(p), n), rand(p * n), [rand(x) for x in (p + n, p * (n + 1), p * n - p // 2)], "%d × %s = <b>%s</b>." % (n, rand(p), rand(p * n)))
    q = "%d kg of potatoes cost %s. What is the price per kilogram?" % (n, rand(p * n))
    return mcq(q, rand(p), [rand(x) for x in (p * n - n, p + n, p * 2)], "%s ÷ %d = <b>%s</b> per kilogram." % (rand(p * n), n, rand(p)))


def one_ratio(r):
    k = Kid(r)
    a, b = k.next(), k.next()
    x, y = r.choice([(1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (2, 5)])
    m = r.randint(2, 9)
    tot = (x + y) * m
    what = r.choice(["sweets", "marbles", "stickers", "rands"])
    q = "%s and %s share %d %s. For every %d %s %s gets, %s gets %d. How many does %s get?" % (a["n"], b["n"], tot, what, x, what if x > 1 else what[:-1], a["n"], b["n"], y, b["n"])
    return mcq(q, y * m, [tot // 2, x * m, y * m + y], "Each round gives out %d + %d = %d. %d ÷ %d = %d rounds. %s gets %d × %d = <b>%d</b>." % (x, y, x + y, tot, x + y, m, b["n"], y, m, y * m))


def build():
    sets, R = build_sets([
        ("Rand and cents", [("collect", uniq(one_rc), 20)]),
        ("Shopping and change", [("collect", uniq(one_buy), 20)]),
        ("Rates", [("collect", uniq(one_rate), 20)]),
        ("Sharing in a ratio", [("collect", uniq(one_ratio), 20)]),
        ("Mixed problems", [("collect", uniq(one_buy), 7), ("collect", uniq(one_rate), 7), ("collect", uniq(one_ratio), 6)]),
    ], 80411)
    finish(sets, R)
    body = lesson('<ul><li>R1 = 100c. R12,50 is 12 rand and 50 cents, or 1 250c.</li><li>To find the cost of several items, multiply; then add. Change = money paid − cost.</li><li>A <b>rate</b> compares two different things: R18 per kilogram. For 3 kg, pay 3 × R18.</li><li>A <b>ratio</b> compares parts: for every 1 sweet Thabo gets, Lerato gets 2.</li></ul>',
        [example("3 kg of apples at R24 per kg; pay with R100", ["3 × R24 = R72", "R100 − R72"], "R28 change")],
        [['R2,50 as 25c', 'R2,50 = 250c.'], ['Cost instead of change', 'Subtract the cost from the money paid.'], ['Sharing equally', 'Use the ratio, not halves.']])
    faq = [('What does CAPS Grade 4 say about problem solving?', 'Solve problems in contexts involving money, measurement and comparing two or more quantities of the same kind (ratio) and of different kinds (rate), and grouping and equal sharing.'), ('How do we write rand and cents?', 'R12,50: rand, then a comma, then the cents.'), ('What is the difference between rate and ratio?', 'A ratio compares the same kind of thing; a rate compares different kinds.'), ('Why use real prices?', 'Learners see maths in everyday shopping.')]
    make('money-rate-and-ratio-problems', 11, 'Numbers, Operations and Relationships', 'Grade 4: 1.1 Whole numbers',
         'Solve problems in contexts involving whole numbers, including financial contexts, measurement contexts, comparing two or more quantities of the same kind (ratio), comparing two quantities of different kinds (rate), and grouping and equal sharing with remainders.',
         'Solving Problems: Money, Rate and Ratio', 'Money, Rate and Ratio',
         'Free CAPS Grade 4 money worksheets: rand and cents, shopping and change, rates such as rand per kilogram, and sharing in a ratio. 100 questions with memos.',
         'R1 = 100c; change = money paid − cost.', 'Rate: R18 per kg, so 3 kg costs 3 × R18.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
