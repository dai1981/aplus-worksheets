# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Philippine Money: Coins and Bills up to ₱100 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_money.py
Naming peso coins and bills up to ₱100, counting money, comparing coins and bills, and adding money in shopping
problems up to ₱100 (own makers with drawings of coins and bills).
Wrong answers come from real mistakes: counting the number of coins instead of their value, thinking a bigger coin
is always worth more, and subtracting when the story adds.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)

ph_common.GRADE = "grade-1"

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


from ws_common import svg_wrap, text

COINS = {1: ("#c9c9c9", 22), 5: ("#d4b25a", 25), 10: ("#d9a441", 27), 20: ("#c88a3a", 29)}
BILLS = {20: "#f0a050", 50: "#e06a6a", 100: "#9a7cc8"}


def money_svg(items):
    """items: list of values; 1, 5, 10, 20c are coins, 20b, 50, 100 bills. Use 'c20' for the 20-peso coin."""
    x, b = 10, ""
    H = 70
    for it in items:
        if isinstance(it, str):
            v = int(it[1:])
            col, rad = COINS[v]
            b += "<circle cx='%d' cy='35' r='%d' fill='%s' stroke='#555' stroke-width='2'/>" % (x + rad, rad, col) + text(x + rad, 41, "₱%d" % v, 14)
            x += 2 * rad + 8
        else:
            col = BILLS[it]
            b += "<rect x='%d' y='12' width='92' height='46' rx='4' fill='%s' stroke='#555' stroke-width='2'/>" % (x, col) + text(x + 46, 41, "₱%d" % it, 17)
            x += 100
    return svg_wrap(x + 4, H, b, "Philippine money: " + ", ".join("%s peso %s" % (str(i)[1:] if isinstance(i, str) else i, "coin" if isinstance(i, str) else "bill") for i in items))


def val(it):
    return int(it[1:]) if isinstance(it, str) else it


def name(it):
    return "₱%d %s" % (val(it), "coin" if isinstance(it, str) else "bill")


ALL = ["c1", "c5", "c10", "c20", 20, 50, 100]


def one_name(r):
    it = r.choice(ALL)
    right = name(it)
    wr = [name(x) for x in ALL if x != it]
    r.shuffle(wr)
    return mcq(fig(money_svg([it])) + "What is this?", right, wr[:3], "It says ₱%d. It is a <b>%s</b>." % (val(it), right))


def pick_set(r, lim=100):
    for _ in range(100):
        n = r.randint(2, 5)
        its = sorted([r.choice(ALL) for _ in range(n)], key=lambda x: -val(x))
        tot = sum(val(x) for x in its)
        if tot <= lim:
            return its, tot
    raise AssertionError


def one_count(r):
    its, tot = pick_set(r)
    wr = [tot + 5, tot - 5 if tot > 5 else tot + 10, len(its), tot + 10]
    return mcq(fig(money_svg(its)) + "How much money is this?", "₱%d" % tot, ["₱%d" % x for x in wr if x != tot],
               "%s = <b>₱%d</b>." % (" + ".join("₱%d" % val(x) for x in its), tot))


def one_cmp(r):
    a, b = r.sample(ALL, 2)
    if val(a) == val(b):
        raise AssertionError
    big = a if val(a) > val(b) else b
    if r.random() < 0.5:
        return mcq("Which is worth more: a %s or a %s?" % (name(a), name(b)), name(big), [name(b if big == a else a), "They are worth the same", "You cannot tell"],
                   "₱%d is more than ₱%d. <b>%s</b>." % (val(big), min(val(a), val(b)), name(big)))
    big_v = r.choice([10, 20, 50, 100])
    small = r.choice([v for v in (1, 5, 10, 20, 50) if v < big_v and big_v % v == 0])
    n = big_v // small
    return mcq("How many ₱%d coins make ₱%d?" % (small, big_v) if small <= 20 else "How many ₱%d bills make ₱%d?" % (small, big_v), n, [n + 1, n - 1 if n > 2 else n + 2, big_v],
               "Count by %ds to %d: that is <b>%d</b>." % (small, big_v, n))


def one_buy(r):
    k = Kid(r).next()
    items = [("a pencil", 8), ("an eraser", 5), ("a ballpen", 12), ("a notebook", 25), ("a bottle of water", 15), ("a banana", 7), ("a pack of crayons", 35), ("pandesal", 3), ("an ice candy", 10), ("a mango", 20)]
    (a, pa), (b, pb) = r.sample(items, 2)
    if pa + pb > 100:
        raise AssertionError
    if r.random() < 0.6:
        q = "%s buys %s for ₱%d and %s for ₱%d. How much does %s pay in all?" % (k["n"], a, pa, b, pb, k["he"])
        return mcq(q, "₱%d" % (pa + pb), ["₱%d" % x for x in (abs(pa - pb), pa + pb + 10, pa + pb - 1)], "₱%d + ₱%d = <b>₱%d</b>." % (pa, pb, pa + pb))
    its, tot = pick_set(r, 60)
    q = fig(money_svg(its)) + "%s has this money. %s gets ₱%d more from %s lola. How much does %s have now?" % (k["n"], k["He"], pa, k["his"], k["he"])
    if tot + pa > 100:
        raise AssertionError
    return mcq(q, "₱%d" % (tot + pa), ["₱%d" % x for x in (tot, tot + pa + 10, abs(tot - pa) if tot != pa else tot + 1)], "₱%d + ₱%d = <b>₱%d</b>." % (tot, pa, tot + pa))


def build():
    sets, R = build_sets([
        ("Name the coin or bill", [("collect", one_name, 7), ("collect", uniq(one_cmp), 13)]),
        ("Count the money", [("collect", uniq(one_count), 20)]),
        ("More money", [("collect", uniq(one_count), 20)]),
        ("Compare money", [("collect", uniq(one_cmp), 20)]),
        ("Shopping problems", [("collect", uniq(one_buy), 20)]),
    ], 70121)
    finish(sets, R)
    body = lesson('<ul><li>Peso coins: ₱1, ₱5, ₱10 and ₱20. Bills: ₱20, ₱50 and ₱100. The sign for peso is ₱.</li><li>To count money, start with the biggest value and count on: ₱50, ₱60, ₱65, ₱66.</li><li>Count the value, not the number of coins: three ₱1 coins are less than one ₱5 coin.</li><li>To find the total cost, add the prices.</li></ul>',
        [example("₱50 bill, ₱10 coin, ₱5 coin", ["50, 60, 65"], "₱65")],
        [['Counting coins, not value', 'Add the values.'], ['Bigger coin, more money', 'Read the number on it.'], ['Subtracting', '“In all” means add.']])
    faq = [('What does MATATAG Math 1 ask about money?', 'Recognize coins (excluding centavo coins) and bills up to ₱100, determine the value of bills and coins up to ₱100, compare denominations, and solve 1-step addition problems with money up to ₱100.'), ('What coins are used in the Philippines?', '₱1, ₱5, ₱10 and ₱20 coins, plus centavo coins.'), ('Is there a ₱20 bill?', 'Yes, and a ₱20 coin too.'), ('How can children practice?', 'Play store with real or toy coins.')]
    make('philippine-money', 21, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Recognize coins (excluding centavo coins) and bills up to ₱100 and their notations; determine the value of a number of bills and/or a number of coins (excluding centavo coins) up to ₱100; compare different denominations of peso coins and bills up to ₱100; solve 1-step problems (given orally or in pictures) involving addition of money where the sum is up to ₱100.',
         'Philippine Money: Coins and Bills up to ₱100', 'Philippine Money',
         'Free Grade 1 Philippine money worksheets for the DepEd MATATAG curriculum: peso coins and bills up to ₱100, counting, comparing and shopping problems. 100 questions with pictures and answers.',
         'Count the value, not the number of coins.', 'Start with the biggest value and count on.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
