# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Coins: Pennies, Nickels, Dimes and Quarters (TEKS 1.4A, 1.4B, 1.4C)
  python3 tools/gen_ustx_math_g1_coins.py
Coin names and values and money stories (the US Grade 2 makers with Texas names; amounts in dollars left out), plus
the cent symbol, how coins relate, and counting pennies, nickels and dimes by 1s, 5s and 10s (own makers).
Wrong answers come from real mistakes: counting coins instead of cents, thinking a bigger coin is worth more, and
counting a dime as 5.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_money as mo
adopt(mo)
tx_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


NAME = {"P": "penny", "N": "nickel", "D": "dime", "Q": "quarter"}
VAL = {"P": 1, "N": 5, "D": 10, "Q": 25}
PL = {"P": "pennies", "N": "nickels", "D": "dimes", "Q": "quarters"}


def no_dollar(it):
    return "$" not in it["q"] + " ".join(it["c"]) + it["e"] and "bill" not in it["q"]


def one_cent(r):
    t = r.choice("PNDQ")
    v = VAL[t]
    if r.random() < 0.5:
        return mcq("How do you write the value of 1 %s?" % NAME[t], "%d¢" % v, ["$%d" % v, "%d" % (v * 10), "1¢" if v != 1 else "5¢"],
                   "A %s is worth %d cents. Write <b>%d¢</b>." % (NAME[t], v, v))
    pic = mo.fig(mo.coin_svg(t))
    return mcq(pic + "What is this coin worth?", "%d¢" % v, ["%d¢" % x for x in VAL.values() if x != v], "This is a %s. It is worth <b>%d¢</b>." % (NAME[t], v))


REL = [("How many pennies are worth the same as 1 nickel?", "5", ["1", "10", "2"], "1 nickel = 5¢ = <b>5 pennies</b>."),
       ("How many pennies are worth the same as 1 dime?", "10", ["5", "1", "2"], "1 dime = 10¢ = <b>10 pennies</b>."),
       ("How many nickels are worth the same as 1 dime?", "2", ["5", "10", "1"], "5¢ + 5¢ = 10¢, so <b>2 nickels</b>."),
       ("How many nickels are worth the same as 1 quarter?", "5", ["2", "4", "25"], "5¢ + 5¢ + 5¢ + 5¢ + 5¢ = 25¢, so <b>5 nickels</b>."),
       ("Which coins are worth the same as 1 quarter?", "2 dimes and 1 nickel", ["2 dimes", "3 nickels", "1 dime and 1 nickel"], "10¢ + 10¢ + 5¢ = <b>25¢</b>."),
       ("Which coin is the smallest but is worth more than a penny and a nickel?", "A dime", ["A quarter", "A nickel", "A penny"], "A dime is small but worth <b>10¢</b>."),
       ("Which coin is worth the most?", "A quarter", ["A dime", "A nickel", "A penny"], "A quarter is worth <b>25¢</b>."),
       ("Which coin is worth the least?", "A penny", ["A nickel", "A dime", "A quarter"], "A penny is worth <b>1¢</b>."),
       ("A nickel is bigger than a dime. Which is worth more?", "The dime", ["The nickel", "They are the same", "You cannot tell"], "Size does not tell value. A dime is 10¢; a nickel is 5¢.")]


def one_rel(r):
    q, a, w, e = r.choice(REL)
    return mcq(q, a, w, e)


def one_more(r):
    a, b = r.sample("PND", 2)
    na, nb = r.randint(1, 6), r.randint(1, 6)
    va, vb = na * VAL[a], nb * VAL[b]
    if va == vb:
        raise AssertionError
    big = "%d %s" % (na, PL[a] if na > 1 else NAME[a]) if va > vb else "%d %s" % (nb, PL[b] if nb > 1 else NAME[b])
    sa, sb = "%d %s" % (na, PL[a] if na > 1 else NAME[a]), "%d %s" % (nb, PL[b] if nb > 1 else NAME[b])
    return mcq("Which is worth more: %s or %s?" % (sa, sb), big, [sa if big == sb else sb, "They are the same", "You cannot tell"],
               "%s = %d¢ and %s = %d¢, so <b>%s</b> is worth more." % (sa, va, sb, vb, big))


def one_same(r):
    t = r.choice("PND")
    n = r.randint(2, 10) if t != "P" else r.randint(3, 12)
    v = n * VAL[t]
    pic = mo.fig(mo.money_svg([t] * n))
    step = {"P": "1s", "N": "5s", "D": "10s"}[t]
    seq = ", ".join(str(VAL[t] * i) for i in range(1, n + 1))
    return mcq(pic + "Count by %s. How much money is this?" % step, "%d¢" % v, ["%d¢" % (n if t != "P" else v + 2), "%d¢" % (v + VAL[t]), "%d¢" % (v - VAL[t]) if v > VAL[t] else "%d¢" % (v + 2 * VAL[t])],
               "%d %s. Count by %s: %s. That is <b>%d¢</b>." % (n, PL[t], step, seq, v))


def one_mixed(r):
    d, n, p = r.randint(0, 5), r.randint(0, 4), r.randint(0, 4)
    if (d > 0) + (n > 0) + (p > 0) < 2:
        raise AssertionError
    v = 10 * d + 5 * n + p
    toks = ["D"] * d + ["N"] * n + ["P"] * p
    pic = mo.fig(mo.money_svg(toks))
    k = Kid(r).next()
    parts = []
    run = 0
    for t, c in (("D", d), ("N", n), ("P", p)):
        for _ in range(c):
            run += VAL[t]
            parts.append(str(run))
    return mcq(pic + "%s has these coins. How much money does %s have?" % (k["n"], k["he"]), "%d¢" % v, ["%d¢" % (d + n + p), "%d¢" % (v + 5), "%d¢" % (10 * (d + n) + p)],
               "Count the dimes by 10s, then the nickels by 5s, then the pennies by 1s: %s. That is <b>%d¢</b>." % (", ".join(parts), v))


def build():
    sets, R = build_sets([
        ("Coin names and values", [("run", mo.set_names, (mo.People, "rnd"), 16, no_dollar), ("collect", uniq(one_more), 4)]),
        ("Write cents and compare coins", [("collect", uniq(one_cent), 8), ("collect", uniq(one_rel), 8), ("collect", uniq(one_more), 4)]),
        ("Count pennies, nickels or dimes", [("collect", uniq(one_same), 20)]),
        ("Count dimes, nickels and pennies", [("collect", uniq(one_mixed), 20)]),
        ("Money stories", [("collect", uniq(one_more), 8), ("run", mo.set_words, (mo.People, "rnd"), 12, no_dollar)]),
    ], 69108)
    finish(sets, R)
    body = lesson('<ul><li>Penny 1¢, nickel 5¢, dime 10¢, quarter 25¢.</li><li>Write cents with the <b>¢</b> symbol: 10¢.</li><li>Count pennies by 1s, nickels by 5s and dimes by 10s.</li><li>Start with the coins worth the most. A big coin is not always worth more: a dime is small but worth 10¢.</li></ul>',
        [example("2 dimes and 3 pennies", ["10, 20, 21, 22, 23"], "23¢")],
        [['Counting coins instead of cents', '3 dimes is 30¢, not 3¢.'], ['Thinking a bigger coin is worth more', 'A dime is smaller than a nickel but worth more.'], ['Counting a dime as 5', 'A dime is 10¢.']])
    faq = [('What does TEKS 1.4A ask?', 'Identify U.S. coins, including pennies, nickels, dimes, and quarters, by value and describe the relationships among them.'), ('What does TEKS 1.4B ask?', 'Write a number with the cent symbol to describe the value of a coin.'), ('What does TEKS 1.4C ask?', 'Use relationships to count by twos, fives, and tens to determine the value of a collection of pennies, nickels, and/or dimes.'), ('How many nickels make a dime?', '2.')]
    make('counting-coins', 8, 'Number and Operations', '1.4A, 1.4B, 1.4C',
         '1.4A identify U.S. coins, including pennies, nickels, dimes, and quarters, by value and describe the relationships among them; 1.4B write a number with the cent symbol to describe the value of a coin; 1.4C use relationships to count by twos, fives, and tens to determine the value of a collection of pennies, nickels, and/or dimes',
         'Coins: Pennies, Nickels, Dimes and Quarters', 'Counting Coins',
         'Free Grade 1 coin worksheets for Texas TEKS 1.4: pennies, nickels, dimes and quarters, the cent symbol, coin relationships and counting coins by 1s, 5s and 10s. 100 questions with answers.',
         'Penny 1¢, nickel 5¢, dime 10¢, quarter 25¢.', 'Count dimes by 10s, then nickels by 5s, then pennies.',
         body, faq, sets, seo_title='Grade 1 Counting Coins Worksheets: Pennies, Nickels and Dimes (TEKS 1.4)')


if __name__ == "__main__":
    build()
