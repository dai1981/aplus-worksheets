# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Value of Coins and Bills (TEKS 3.4C)
  python3 tools/gen_ustx_math_g3_money.py
Counting coins, counting dollars and cents, collections of $1, $5, $10 and $20 bills with coins, making an amount
in different ways, and money word problems. Sets 1, 2, 4 and half of set 5 use the US Grade 2 money makers with
Texas names and new amounts; the coin and bill pictures are the US Grade 2 drawings ($10 and $20 bills added).
Wrong answers come from real mistakes: counting coins instead of their value, treating a nickel as 10¢ because
it is bigger than a dime, writing $4.5 for $4.05, and adding bills as cents.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run, adopt, People, example)
import gen_us_math_g2_money as usm

adopt(usm)
usm.People = People
usm.ORDER[:0] = ["B20", "B10"]
usm.VAL.update({"B20": 2000, "B10": 1000})
usm.ONE.update({"B20": "$20 bill", "B10": "$10 bill"})
usm.MANY.update({"B20": "$20 bills", "B10": "$10 bills"})
R = random.Random(61401)


def dol(c):
    return "$%d.%02d" % (c // 100, c % 100) if c >= 100 else "%d¢" % c


def collection(r):
    toks = []
    for t, hi in (("B20", 2), ("B10", 2), ("B5", 2), ("B1", 4), ("Q", 3), ("D", 3), ("N", 2), ("P", 4)):
        if r.random() < 0.55:
            toks += [t] * r.randint(1, hi)
    if not any(t.startswith("B") for t in toks) or not any(not t.startswith("B") for t in toks) or len(toks) > 12:
        return None
    return toks


# ------------------------------------------------------------ set 3: bills and coins
def one_bills(r):
    toks = collection(r)
    if not toks:
        return None
    tot = usm.total(toks)
    bills = sum(usm.VAL[t] for t in toks if t.startswith("B"))
    coins = tot - bills
    wrong = [tot + 5 if coins % 10 else tot + 10, bills + len([t for t in toks if not t.startswith("B")]), tot - usm.VAL[toks[0]] + 100 if toks[0] != "B1" else tot + 400, tot + 100]
    pic = fig(usm.money_svg(toks, per_row=6, label="money: %s" % ", ".join(usm.nw(n, t) for t, n in usm.counts(toks))))
    return mcq(pic + "What is the total value?", dol(tot), [dol(w) for w in wrong if w > 0],
               "Count the bills first: %s. Then the coins: %s. Total: <b>%s</b>." % (dol(bills), dol(coins), dol(tot)))


# ------------------------------------------------------------ set 5 (half): word problems
def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["enough", "more", "total"])
    if kind == "enough":
        toks = collection(r)
        if not toks:
            return None
        have = usm.total(toks)
        price = have + r.choice([-1, 1]) * r.choice([25, 50, 100, 105])
        if price <= 100:
            return None
        item = r.choice(["a T-shirt", "a book", "a board game", "a soccer ball", "a backpack"])
        ok = have >= price
        pic = fig(usm.money_svg(toks, per_row=6, label="money"))
        return mcq(pic + "%s has this money. %s costs %s. Does %s have enough?" % (k["n"], item.capitalize(), dol(price), k["he"]),
                   "Yes, %s has %s" % (k["he"], dol(have)) if ok else "No, %s has only %s" % (k["he"], dol(have)),
                   ["No, %s has only %s" % (k["he"], dol(have)) if ok else "Yes, %s has %s" % (k["he"], dol(have)), "Yes, %s has %d bills and coins" % (k["he"], len(toks)), "We cannot tell without counting the coins"],
                   "The money is worth %s. %s is %s %s, so <b>%s</b>." % (dol(have), dol(have), "at least" if ok else "less than", dol(price), "yes" if ok else "no"))
    if kind == "more":
        a = [("B10", 1), ("B5", r.randint(1, 2)), ("Q", r.randint(1, 3))]
        b = [("B20", 1), ("D", r.randint(1, 4))]
        ta = sum(usm.VAL[t] * n for t, n in a)
        tb = sum(usm.VAL[t] * n for t, n in b)
        if ta == tb:
            return None
        k2 = Kid(r).next()
        if k2["n"] == k["n"]:
            return None
        da = " and ".join(usm.nw(n, t) for t, n in a)
        db = " and ".join(usm.nw(n, t) for t, n in b)
        win = k["n"] if ta > tb else k2["n"]
        return mcq("%s has %s. %s has %s. Who has more money?" % (k["n"], da, k2["n"], db), win,
                   [k2["n"] if win == k["n"] else k["n"], "They have the same", "The one with more bills and coins"],
                   "%s has %s. %s has %s. <b>%s</b> has more." % (k["n"], dol(ta), k2["n"], dol(tb), win))
    toks = [("B5", r.randint(1, 3)), ("B1", r.randint(1, 4)), ("Q", r.randint(1, 3)), ("N", r.randint(1, 3))]
    t = sum(usm.VAL[a] * n for a, n in toks)
    d = ", ".join(usm.nw(n, a) for a, n in toks)
    return mcq("%s empties %s piggy bank and finds %s. How much money is that?" % (k["n"], k["his"], d), dol(t), [dol(t + 10), dol(t - 20 if t > 120 else t + 20), dol(sum(n for a, n in toks) * 100), dol(t + 100)],
               "Bills: %s. Coins: %s. Total: <b>%s</b>." % (dol(sum(usm.VAL[a] * n for a, n in toks if a.startswith("B"))), dol(sum(usm.VAL[a] * n for a, n in toks if not a.startswith("B"))), dol(t)))


def build():
    sets = [S("Count coins", run(usm.set_count, People, "rnd", seed=151)["items"]),
            S("Count dollars and cents", run(usm.set_dollars, People, "rnd", seed=152)["items"]),
            S("Bills and coins", collect(one_bills, 20, R)),
            S("Make an amount", run(usm.set_make, People, "rnd", seed=153)["items"]),
            S("Money word problems", run(usm.set_words, People, "rnd", seed=154)["items"][:10] + collect(one_story, 10, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Coins: penny 1¢, nickel 5¢, dime 10¢, quarter 25¢. Bills: $1, $5, $10, $20. 100¢ = $1.00.</li>"
        "<li>Size does not tell the value: a dime is smaller than a nickel but worth more.</li>"
        "<li>To count a collection, start with the bills, from greatest to least. Then count on with the coins: quarters, dimes, nickels, pennies.</li>"
        "<li>Write dollars and cents with a point: $12.05 means 12 dollars and 5 cents.</li></ul>",
        [figure(usm.money_svg(["B10", "B5", "B1", "Q", "Q", "D", "P"], per_row=7, label="a $10 bill, a $5 bill, a $1 bill, 2 quarters, 1 dime and 1 penny"), "$10, $15, $16, then $16.25, $16.50, $16.60, $16.61."),
         example("What is 3 quarters, 2 dimes and 4 pennies worth?", ["25, 50, 75", "85, 95", "96, 97, 98, 99"], "99¢")],
        [["Counting the coins, not their value", "Say the value as you count: 25, 50, 60, 70 …"],
         ["Thinking a nickel is worth more than a dime because it is bigger", "A dime is 10¢ and a nickel is 5¢."],
         ["Writing $4.5 for 4 dollars and 5 cents", "Cents always use two digits: $4.05."]])
    faq = [("What does TEKS 3.4C ask?", "Determine the value of a collection of coins and bills."),
           ("Which coins and bills do Grade 3 students count?", "Pennies, nickels, dimes and quarters, and $1, $5, $10 and $20 bills."),
           ("What is the best order to count money?", "Start with the bills from greatest to least, then count on with the coins from greatest to least."),
           ("How do you write money amounts?", "Use a dollar sign and a decimal point with two digits for the cents: $7.40, $12.05. Amounts under a dollar can be written with the cent sign: 85¢.")]
    make("value-of-coins-and-bills", 14, "Number and Operations", "3.4C",
         "3.4C determine the value of a collection of coins and bills",
         "Value of Coins and Bills: Counting Money to $100", "Value of Coins and Bills",
         "Free Grade 3 money worksheets for Texas TEKS 3.4C: count coins, count dollars and cents, collections of $1, $5, $10 and $20 bills with coins, make an amount and money word problems. 100 questions with answers.",
         "Count bills first, then count on with the coins.", "Coins: 1¢, 5¢, 10¢, 25¢. Bills: $1, $5, $10, $20. Write cents with two digits: $4.05.",
         body, faq, sets, seo_title="Grade 3 Money Worksheets: Value of Coins and Bills (TEKS 3.4C, STAAR)")


if __name__ == "__main__":
    build()
