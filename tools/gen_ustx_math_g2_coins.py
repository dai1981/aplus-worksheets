# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Counting Coins to One Dollar (TEKS 2.5A, 2.5B)
  python3 tools/gen_ustx_math_g2_coins.py
Naming coins, counting collections of coins up to one dollar, writing the value with ¢ and with $ and a decimal
point, making an amount, and money stories (the US Grade 2 makers with Texas names, plus an own notation maker).
Wrong answers come from real mistakes: counting coins instead of their value, writing 45¢ as $45, and thinking a
nickel is worth more than a dime because it is bigger.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_money as mo
adopt(mo)
tx_common.GRADE = "grade-2"

COINS = [("quarter", 25), ("dime", 10), ("nickel", 5), ("penny", 1)]


def one_write(r):
    v = r.randint(5, 99)
    if r.random() < 0.5:
        return mcq("Which shows %d¢ with a dollar sign?" % v, "$0.%02d" % v, ["$%d" % v, "$%d.00" % v, "$0.%d" % (v * 10) if v < 10 else "$%d.%d" % (v // 10, v % 10)],
                   "%d¢ is less than one dollar, so write <b>$0.%02d</b>." % (v, v))
    return mcq("Which is the same as $0.%02d?" % v, "%d¢" % v, ["%d¢" % (v * 10) if v < 10 else "%d¢" % (v + 100), "$%d" % v, "%d¢" % (100 - v)],
               "$0.%02d means %d cents: <b>%d¢</b>." % (v, v, v))



def build():
    sets, R = build_sets([
        ("Name the coins", [("run", mo.set_names, (mo.People, "rnd"), 20)]),
        ("Count coins", [("run", mo.set_count, (mo.People, "rnd"), 20)]),
        ("Write money with ¢ and $", [("collect", one_write, 20)]),
        ("Make an amount", [("run", mo.set_make, (mo.People, "rnd"), 20)]),
        ("Money stories", [("run", mo.set_words, (mo.People, "rnd"), 20)]),
    ], 69210)
    finish(sets, R)
    body = lesson('<ul><li>Penny = 1¢, nickel = 5¢, dime = 10¢, quarter = 25¢.</li><li>Count the coins with the greatest value first, then count on.</li><li>Write cents with ¢ (45¢) or with a dollar sign and a decimal point ($0.45).</li><li>100¢ = $1.00.</li></ul>',
        [example("2 quarters, 1 dime, 3 pennies", ["25, 50, 60, 61, 62, 63"], "63¢ = $0.63")],
        [['Counting coins instead of value', '3 dimes is 30¢, not 3¢.'], ['Writing 45¢ as $45', '45¢ is $0.45.'], ['Thinking a nickel beats a dime', 'A dime is smaller but worth more: 10¢.']])
    faq = [('What does TEKS 2.5A ask?', 'Determine the value of a collection of coins up to one dollar.'), ('What does TEKS 2.5B ask?', 'Use the cent symbol, dollar sign and the decimal point to name the value of a collection of coins.'), ('How many pennies make a dollar?', '100 pennies.'), ('How many quarters make a dollar?', '4 quarters.')]
    make('counting-coins', 10, 'Number and Operations', '2.5A, 2.5B',
         '2.5A determine the value of a collection of coins up to one dollar; 2.5B use the cent symbol, dollar sign, and the decimal point to name the value of a collection of coins',
         'Counting Coins to One Dollar', 'Counting Coins',
         'Free Grade 2 money worksheets for Texas TEKS 2.5A and 2.5B: name coins, count coins to one dollar, write money with ¢ and $, make amounts and money stories. 100 questions with answers.',
         'Count the coins with the greatest value first.', '2 quarters, 1 dime and 3 pennies = 63¢ = $0.63.',
         body, faq, sets, seo_title='Grade 2 Counting Coins Worksheets (TEKS 2.5A, 2.5B)')


if __name__ == "__main__":
    build()
