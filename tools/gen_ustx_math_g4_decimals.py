# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Decimals: Tenths and Hundredths, Fractions and Money (TEKS 4.2E, 4.2G)
  python3 tools/gen_ustx_math_g4_decimals.py
Reading tenths bars and hundredths grids, decimals and fractions that name tenths and hundredths, place value of
decimals (the US Grade 4 decimal makers with Texas names), money as decimals of a dollar, and word problems.
Wrong answers come from real mistakes: writing 7/100 as 0.7, reading 0.5 as 5 hundredths, and writing 3 dimes as
$0.03.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_decimals as usd
adopt(usd)
tx_common.GRADE = "grade-4"

COINS = [("penny", "pennies", 1), ("nickel", "nickels", 5), ("dime", "dimes", 10), ("quarter", "quarters", 25)]


def one_money(r):
    kind = r.choice(["coins", "coins", "frac", "words"])
    if kind == "coins":
        picks = r.sample(COINS, r.choice([1, 2]))
        cnt = [r.randint(1, 4) for _ in picks]
        c = sum(v * n for (_, _, v), n in zip(picks, cnt))
        bills = r.randint(0, 9)
        tot = bills * 100 + c
        desc = (["%d dollar bill%s" % (bills, "" if bills == 1 else "s")] if bills else []) + ["%d %s" % (n, one if n == 1 else many) for (one, many, v), n in zip(picks, cnt)]
        right = "$%d.%02d" % (tot // 100, tot % 100)
        wrong = ["$%d.%d" % (tot // 100, c) if c >= 10 else "$%d.%d0" % (tot // 100, c), "$%d.%02d" % (bills + c // 100 + 1, c % 100), "$%d.%02d" % (tot // 100, (c + 10) % 100) if c + 10 < 100 else "$%d.%02d" % (tot // 100, c - 10), "$%d" % (bills + sum(cnt))]
        return mcq("Write the amount as a decimal of a dollar: %s." % ", ".join(desc), right, wrong,
                   "The coins make %d¢, which is %d hundredths of a dollar. <b>%s</b>." % (c, c, right))
    if kind == "frac":
        c = r.randint(1, 99)
        return mcq("What part of a dollar is %d¢, written as a decimal?" % c, "$0.%02d" % c, ["$%d.00" % c, "$0.%d" % c if c >= 10 else "$0.%d0" % c, "$0.%02d" % (100 - c)],
                   "%d¢ is %s of a dollar, so it is <b>$0.%02d</b>." % (c, fr(c, 100), c))
    k = Kid(r).next()
    d, p = r.randint(1, 9), r.randint(1, 9)
    return mcq("%s has %d dimes and %d pennies. Which decimal shows how much money that is in dollars?" % (k["n"], d, p), "0.%d%d" % (d, p), ["%d.%d" % (d, p), "0.%d%d" % (p, d) if p != d else "0.%d" % (d + p), "0.%d" % (d + p) if d + p < 10 else "%d" % (d + p)],
               "A dime is one tenth of a dollar and a penny is one hundredth. %d tenths and %d hundredths is <b>0.%d%d</b>." % (d, p, d, p))


def one_frac_dec(r):
    kind = r.choice(["to_dec", "to_frac", "tenths_hundredths", "word"])
    if kind == "to_dec":
        if r.random() < 0.5:
            n = r.randint(1, 9)
            return mcq("Write %s as a decimal." % fr(n, 10), "0.%d" % n, ["0.0%d" % n, "%d.10" % n, "1.%d" % n], "%s is %d tenths: <b>0.%d</b>." % (fr(n, 10), n, n))
        n = r.randint(1, 99)
        return mcq("Write %s as a decimal." % fr(n, 100), "0.%02d" % n, ["0.%d" % n if n >= 10 else "0.%d" % n, "%d.00" % n, "%d.100" % n], "%s is %d hundredths: <b>0.%02d</b>." % (fr(n, 100), n, n))
    if kind == "to_frac":
        n = r.randint(1, 99)
        return mcq("Which fraction is equal to 0.%02d?" % n, fr(n, 100), [fr(n, 10) if n < 10 else fr(n % 10 or 1, 10), fr(1, n) if n > 1 else fr(10, 100), fr(100, n) if n > 1 else fr(1, 10)],
                   "0.%02d is %d hundredths: <b>%s</b>." % (n, n, fr(n, 100)))
    if kind == "tenths_hundredths":
        n = r.randint(1, 9)
        return mcq("%s is equal to how many hundredths?" % fr(n, 10), "%s" % fr(n * 10, 100), [fr(n, 100), fr(n + 10, 100), fr(n * 100, 10)],
                   "1 tenth = 10 hundredths, so %s = <b>%s</b> = 0.%d0." % (fr(n, 10), fr(n * 10, 100), n))
    a, b = r.randint(1, 9), r.randint(1, 9)
    return mcq("A long jump is %d and %s meters. Which decimal shows this?" % (a, fr(b, 10)), "%d.%d" % (a, b), ["%d.0%d" % (a, b), "%d.%d" % (b, a) if a != b else "%d.%d" % (a + 1, b), "%d.%d" % (a, b + 10)],
               "%d and %d tenths is <b>%d.%d</b>." % (a, b, a, b))


def build():
    sets, R = build_sets([
        ("Read tenths bars and hundredths grids", [("run", usd.set_grids, ("rnd",), 20)]),
        ("Fractions and decimals", [("collect", one_frac_dec, 20)]),
        ("Decimal place value", [("run", usd.set_place, ("rnd",), 20)]),
        ("Money as decimals", [("collect", one_money, 20)]),
        ("Money and measurement word problems", [("run", usd.set_words, ("rnd",), 20)]),
    ], 64003)
    finish(sets, R)
    body = lesson('<ul><li>A <b>tenth</b> is 1 of 10 equal parts: 0.1 = 1/10. A <b>hundredth</b> is 1 of 100 equal parts: 0.01 = 1/100.</li><li>The first place after the decimal point is tenths; the second is hundredths. 0.47 is 4 tenths and 7 hundredths, or 47 hundredths.</li><li>Money uses hundredths of a dollar: a dime is $0.10 and a penny is $0.01.</li></ul>',
        [example("Write 7/100 as a decimal.", ["7 hundredths", "The hundredths place is the second place after the point."], "0.07"), example("3 dimes and 4 pennies", ["30¢ + 4¢ = 34¢", "34 hundredths of a dollar"], "$0.34")],
        [['Writing 7/100 as 0.7', '0.7 is 7 tenths. 7 hundredths is 0.07.'], ['Reading 0.5 as 5 hundredths', '0.5 = 5 tenths = 50 hundredths.'], ['Writing 3 dimes as $0.03', 'A dime is a tenth of a dollar: $0.30.']])
    faq = [('What does TEKS 4.2E ask?', 'Represent decimals, including tenths and hundredths, using concrete and visual models and money.'), ('What does TEKS 4.2G ask?', 'Relate decimals to fractions that name tenths and hundredths, such as 0.3 = 3/10 and 0.25 = 25/100.'), ('Is 0.5 the same as 0.50?', 'Yes. 5 tenths is the same amount as 50 hundredths.'), ('How does money help with decimals?', 'A dollar is the whole. Dimes are tenths and pennies are hundredths, so $0.47 is 4 dimes and 7 pennies.')]
    make('decimals-tenths-and-hundredths', 3, 'Number and Operations', '4.2E, 4.2G',
         '4.2E represent decimals, including tenths and hundredths, using concrete and visual models and money; 4.2G relate decimals to fractions that name tenths and hundredths',
         'Decimals: Tenths and Hundredths, Fractions and Money', 'Decimals: Tenths and Hundredths',
         'Free Grade 4 decimal worksheets for Texas TEKS 4.2E and 4.2G: tenths bars and hundredths grids, fractions and decimals, decimal place value, money as decimals and word problems. 100 questions with answers.',
         '0.1 = 1/10 and 0.01 = 1/100.', 'The first place after the point is tenths, the second is hundredths. A dime is $0.10 and a penny is $0.01.',
         body, faq, sets, seo_title='Grade 4 Decimals Worksheets: Tenths, Hundredths and Money (TEKS 4.2E, 4.2G, STAAR)')


if __name__ == "__main__":
    build()
