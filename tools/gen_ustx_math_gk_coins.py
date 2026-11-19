# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Naming Coins: Penny, Nickel, Dime and Quarter (TEKS K.4)
  python3 tools/gen_ustx_math_gk_coins.py
Coin names and values (the US Grade 2 maker with Texas names; amounts in dollars left out), plus naming a coin from a
picture, finding a coin, counting one kind of coin in a group, and coin stories (own makers).
Wrong answers come from real mistakes: mixing up a nickel and a dime, and thinking the biggest coin is worth the most.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_money as mo
adopt(mo)
tx_common.GRADE = "kindergarten"

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
PL = {"P": "pennies", "N": "nickels", "D": "dimes", "Q": "quarters"}
VAL = {"P": 1, "N": 5, "D": 10, "Q": 25}


def no_dollar(it):
    return "$" not in it["q"] + " ".join(it["c"]) + it["e"] and "bill" not in it["q"]


def one_pic(r):
    t = r.choice("PNDQ")
    k = Kid(r).next()
    pic = mo.fig(mo.coin_svg(t))
    v = r.choice(["finds", "has", "drops", "picks up"])
    return mcq(pic + "%s %s this coin. What is it called?" % (k["n"], v), "A " + NAME[t], ["A " + NAME[x] for x in "PNDQ" if x != t],
               "This coin is worth %d¢. It is <b>a %s</b>." % (VAL[t], NAME[t]))


def one_find(r):
    t = r.choice("PNDQ")
    toks = list("PNDQ")
    r.shuffle(toks)
    pic = mo.fig(mo.money_svg(toks))
    k = Kid(r).next()
    i = toks.index(t)
    return mcq(pic + "%s wants the %s. Which coin is it, counting from the left?" % (k["n"], NAME[t]), ["1st", "2nd", "3rd", "4th"][i], [x for j, x in enumerate(["1st", "2nd", "3rd", "4th"]) if j != i],
               "The %s is worth %d¢. It is the <b>%s</b> coin." % (NAME[t], VAL[t], ["1st", "2nd", "3rd", "4th"][i]))


def one_count(r):
    toks = [r.choice("PNDQ") for _ in range(r.randint(4, 8))]
    t = r.choice(sorted(set(toks)))
    n = toks.count(t)
    pic = mo.fig(mo.money_svg(toks))
    return mcq(pic + "How many %s are there?" % PL[t], str(n), [str(len(toks)), str(n + 1), str(n - 1) if n > 1 else str(n + 2)],
               "Find each %s and count: <b>%d</b>." % (NAME[t], n))


def one_story(r):
    a, b = r.sample("PNDQ", 2)
    k1 = Kid(r).next()
    k2 = Kid(r).next()
    if k1["n"] == k2["n"]:
        raise AssertionError
    big = a if VAL[a] > VAL[b] else b
    who = k1["n"] if big == a else k2["n"]
    other = k2["n"] if big == a else k1["n"]
    return mcq("%s has a %s. %s has a %s. Whose coin is worth more?" % (k1["n"], NAME[a], k2["n"], NAME[b]), who, [other, "They are worth the same", "Nobody"],
               "A %s is %d¢ and a %s is %d¢, so <b>%s</b>'s coin is worth more." % (NAME[a], VAL[a], NAME[b], VAL[b], who))


def build():
    sets, R = build_sets([
        ("Coin names and values", [("run", mo.set_names, (mo.People, "rnd"), 16, no_dollar), ("collect", uniq(one_pic), 4)]),
        ("Name the coin", [("collect", uniq(one_pic), 20)]),
        ("Find the coin", [("collect", uniq(one_find), 20)]),
        ("How many of each coin?", [("collect", uniq(one_count), 20)]),
        ("Coin stories", [("collect", uniq(one_story), 20)]),
    ], 69011)
    finish(sets, R)
    body = lesson('<ul><li><b>Penny</b>: 1 cent, brown. <b>Nickel</b>: 5 cents.</li><li><b>Dime</b>: 10 cents, the smallest coin. <b>Quarter</b>: 25 cents, the biggest.</li><li>A small coin can be worth more: a dime is worth more than a nickel.</li></ul>',
        [example("A small silver coin worth 10 cents", ["smallest coin"], "dime")],
        [['Mixing up a nickel and a dime', 'The dime is smaller but worth more.'], ['Thinking bigger means more money', 'Look at the coin, not its size.'], ['Calling every brown coin a nickel', 'The brown coin is a penny.']])
    faq = [('What does TEKS K.4 ask?', 'Identify U.S. coins by name, including pennies, nickels, dimes, and quarters.'), ('Which coin is the smallest?', 'The dime.'), ('Which coin is worth the most?', 'The quarter.'), ('How can I help at home?', 'Sort real coins by name together.')]
    make('naming-coins', 11, 'Number and Operations', 'K.4',
         'K.4 identify U.S. coins by name, including pennies, nickels, dimes, and quarters',
         'Naming Coins: Penny, Nickel, Dime and Quarter', 'Naming Coins',
         'Free kindergarten coin worksheets for Texas TEKS K.4: name pennies, nickels, dimes and quarters, find and count coins, and coin stories. 100 questions with answers.',
         'Penny, nickel, dime, quarter.', 'The dime is smallest but worth more than a nickel.',
         body, faq, sets, seo_title='Kindergarten Naming Coins Worksheets (TEKS K.4)')


if __name__ == "__main__":
    build()
