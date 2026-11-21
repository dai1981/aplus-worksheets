# -*- coding: utf-8 -*-
"""
Indian money for Classes 1-5 (in_prim): drawings of coins (₹1, ₹2, ₹5, ₹10, ₹20) and notes (₹10 to ₹500), and
question makers for naming, counting, comparing, shopping and change. lim keeps totals within the class's range.
"""
from ws_common import svg_wrap, text, fig
from in_prim import mcq, Kid, rupee

COINS = {1: ("#c9c9c9", 21), 2: ("#bdbdbd", 23), 5: ("#d4b25a", 25), 10: ("#d9a441", 27), 20: ("#c88a3a", 29)}
NOTES = {10: "#c9a27a", 20: "#e5d96a", 50: "#8fd0d6", 100: "#b9a6d8", 200: "#f2b35c", 500: "#bdbdb0"}


def money_svg(items):
    """items: 'c5' is a ₹5 coin, 50 is a ₹50 note."""
    x, b = 10, ""
    for it in items:
        if isinstance(it, str):
            v = int(it[1:])
            col, rad = COINS[v]
            b += "<circle cx='%d' cy='35' r='%d' fill='%s' stroke='#555' stroke-width='2'/>" % (x + rad, rad, col) + text(x + rad, 41, "₹%d" % v, 14)
            x += 2 * rad + 8
        else:
            b += "<rect x='%d' y='12' width='92' height='46' rx='4' fill='%s' stroke='#555' stroke-width='2'/>" % (x, NOTES[it]) + text(x + 46, 41, "₹%d" % it, 17)
            x += 100
    return svg_wrap(x + 4, 70, b, "Indian money: " + ", ".join("%s rupee %s" % (val(i), "coin" if isinstance(i, str) else "note") for i in items))


def val(it):
    return int(it[1:]) if isinstance(it, str) else it


def name(it):
    return "₹%d %s" % (val(it), "coin" if isinstance(it, str) else "note")


def kinds(lim):
    return [x for x in ["c1", "c2", "c5", "c10", "c20", 10, 20, 50, 100, 200, 500] if val(x) <= lim]


def one_name(lim=100):
    def f(r):
        al = kinds(lim)
        it = r.choice(al)
        wr = [name(x) for x in al if x != it]
        r.shuffle(wr)
        return mcq(fig(money_svg([it])) + "What is this?", name(it), wr[:3], "It shows ₹%d. It is a <b>%s</b>." % (val(it), name(it)))
    f.__name__ = "one_name"
    return f


def pick(r, lim, n=(2, 5)):
    al = kinds(lim)
    for _ in range(200):
        its = sorted([r.choice(al) for _ in range(r.randint(*n))], key=lambda x: -val(x))
        tot = sum(val(x) for x in its)
        if tot <= lim:
            return its, tot
    raise AssertionError


def one_count(lim=100, n=(2, 5)):
    def f(r):
        its, tot = pick(r, lim, n)
        step = 5 if tot > 20 else 1
        wr = [tot + step, tot - step if tot > step else tot + 2 * step, len(its), tot + 10]
        return mcq(fig(money_svg(its)) + "How much money is this?", "₹%d" % tot, ["₹%d" % x for x in wr if x != tot],
                   "Start with the biggest: %s = <b>₹%d</b>." % (" + ".join("₹%d" % val(x) for x in its), tot))
    f.__name__ = "one_count"
    return f


def one_cmp(lim=100):
    def f(r):
        al = kinds(lim)
        if r.random() < 0.5:
            a, b = r.sample(al, 2)
            if val(a) == val(b):
                raise AssertionError
            big = a if val(a) > val(b) else b
            return mcq("Which is worth more: a %s or a %s?" % (name(a), name(b)), name(big), [name(b if big == a else a), "They are worth the same", "You cannot tell"],
                       "₹%d is more than ₹%d. <b>%s</b>." % (val(big), min(val(a), val(b)), name(big)))
        big_v = r.choice([v for v in (10, 20, 50, 100, 200, 500) if v <= lim])
        small = r.choice([v for v in (1, 2, 5, 10, 20, 50, 100) if v < big_v and big_v % v == 0 and big_v // v <= 25])
        n = big_v // small
        what = "coins" if small <= 5 else "notes"
        return mcq("How many ₹%d %s make ₹%d?" % (small, what, big_v), n, [n + 1, n - 1 if n > 2 else n + 2, big_v],
                   "Count in %ds up to %d: <b>%d</b>." % (small, big_v, n))
    f.__name__ = "one_cmp"
    return f


ITEMS = [("a pencil", 5), ("an eraser", 3), ("a pen", 10), ("a notebook", 30), ("a bottle of water", 20), ("a banana", 6), ("a box of crayons", 45),
         ("a samosa", 15), ("a kulfi", 25), ("a mango", 20), ("a ball", 40), ("a kite", 12), ("a packet of biscuits", 10), ("a glass of lassi", 30),
         ("a comic book", 60), ("a toy car", 80), ("a water bottle", 120), ("a school bag", 350), ("a pair of slippers", 150), ("a lunch box", 180),
         ("a cricket ball", 90), ("a story book", 125), ("a geometry box", 95), ("a cap", 70)]


def one_buy(lim=100):
    def f(r):
        k = Kid(r).next()
        (a, pa), (b, pb) = r.sample([x for x in ITEMS if x[1] < lim], 2)
        if pa + pb > lim:
            raise AssertionError
        kind = r.random()
        if kind < 0.5:
            q = "%s buys %s for ₹%d and %s for ₹%d. How much does %s pay in all?" % (k["n"], a, pa, b, pb, k["he"])
            return mcq(q, "₹%d" % (pa + pb), ["₹%d" % x for x in (abs(pa - pb), pa + pb + 10, pa + pb - 1)], "₹%d + ₹%d = <b>₹%d</b>." % (pa, pb, pa + pb))
        note = min([v for v in (10, 20, 50, 100, 200, 500) if v > pa] or [0])
        if not note or note > lim:
            raise AssertionError
        q = "%s buys %s for ₹%d and pays with a ₹%d note. How much change does %s get?" % (k["n"], a, pa, note, k["he"])
        return mcq(q, "₹%d" % (note - pa), ["₹%d" % x for x in (note + pa, pa, note - pa + 10)], "₹%d − ₹%d = <b>₹%d</b>." % (note, pa, note - pa))
    f.__name__ = "one_buy"
    return f


def one_make(lim=100):
    def f(r):
        al = kinds(lim)
        its, tot = pick(r, lim, (2, 4))
        other, t2 = pick(r, lim, (2, 4))
        if t2 == tot:
            raise AssertionError
        w1 = sorted(its[:-1], key=lambda x: -val(x)) + ([r.choice(al)] if len(its) < 4 else [])
        alt = [x for x in (other, w1) if sum(val(y) for y in x) != tot]
        if len(alt) < 2:
            raise AssertionError
        third = its[:1] * 2 if val(its[0]) * 2 != tot else its[:1] * 3
        if val(third[0]) * len(third) == tot:
            raise AssertionError
        show = lambda xs: " + ".join("₹%d" % val(x) for x in xs)
        return mcq("Which of these makes exactly ₹%d?" % tot, show(its), [show(x) for x in alt] + [show(third)],
                   "%s = <b>₹%d</b>." % (show(its), tot))
    f.__name__ = "one_make"
    return f
