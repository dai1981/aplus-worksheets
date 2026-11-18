# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Adding and Subtracting Whole Numbers and Decimals (TEKS 4.4A)
  python3 tools/gen_ustx_math_g4_add_subtract.py
4- to 6-digit addition and subtraction with the standard algorithm, subtracting across zeros (the US Grade 4 makers
with Texas names), and adding and subtracting decimals to hundredths, including money.
Wrong answers come from real mistakes: lining up the last digits of decimals instead of the decimal points,
forgetting to regroup, and dropping a zero placeholder.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_add_sub as usa
adopt(usa)
tx_common.GRADE = "grade-4"

def dec(c):
    return "%d.%02d" % (c // 100, c % 100)


def one_decimal(r):
    kind = r.choice(["add", "sub", "add1", "money", "money_sub"])
    if kind in ("add", "sub"):
        a, b = r.randint(105, 9899), r.randint(105, 4999)
        if kind == "sub" and a < b:
            a, b = b, a
        res = a + b if kind == "add" else a - b
        op = "+" if kind == "add" else "−"
        wrong = [res + 100 if kind == "add" else res - 100, res + 10, (a // 10 + b) if kind == "add" else abs(a - b * 10) if abs(a - b * 10) != res else res + 1, res - 1 if res > 1 else res + 2]
        return mcq("%s %s %s = ?" % (dec(a), op, dec(b)), dec(res), [dec(w) for w in wrong if w > 0],
                   "Line up the decimal points, then %s each place, regrouping as needed: <b>%s</b>." % ("add" if kind == "add" else "subtract", dec(res)))
    if kind == "add1":
        a, b = r.randint(11, 99), r.randint(101, 999)
        res = a * 10 + b
        wa = "%d.%d" % (a // 10, a % 10)
        return mcq("%s + %s = ?" % (wa, dec(b)), dec(res), [dec(a + b), dec(res + 10), dec(res - 1)],
                   "Write %s as %s.%d0 so both have hundredths. Then add: <b>%s</b>." % (wa, a // 10, a % 10, dec(res)))
    k = Kid(r).next()
    a, b = r.randint(150, 4999), r.randint(105, 2999)
    if kind == "money":
        return mcq("%s buys a book for $%s and a poster for $%s. How much does %s spend?" % (k["n"], dec(a), dec(b), k["he"]), "$" + dec(a + b),
                   ["$" + dec(a + b + 100), "$" + dec(a + b - 10), "$" + dec(a + b + 1)], "$%s + $%s = <b>$%s</b>." % (dec(a), dec(b), dec(a + b)))
    pay = ((a // 100) + 1) * 100 if r.random() < 0.5 else 2000 if a < 2000 else 5000
    if pay <= a:
        return None
    return mcq("%s pays for a $%s game with $%s. How much change does %s get?" % (k["n"], dec(a), dec(pay), k["he"]), "$" + dec(pay - a),
               ["$" + dec(pay - a + 100), "$" + dec(pay - a + 10), "$" + dec(pay + a)], "$%s − $%s = <b>$%s</b>." % (dec(pay), dec(a), dec(pay - a)))


def build():
    sets, R = build_sets([
        ("Add 4-digit numbers", [("run", usa.set_add4, ("rnd", "seen"), 20)]),
        ("Add 5- and 6-digit numbers", [("run", usa.set_add56, ("rnd", "seen"), 20)]),
        ("Subtract, including across zeros", [("run", usa.set_sub4, ("rnd", "seen"), 10), ("run", usa.set_zeros, ("rnd", "seen"), 10)]),
        ("Add and subtract decimals", [("collect", one_decimal, 20)]),
        ("Word problems, missing numbers and estimates", [("run", usa.set_story, ("rnd",), 20)]),
    ], 64005)
    finish(sets, R)
    body = lesson('<ul><li>Line up the digits by place value. For decimals, <b>line up the decimal points</b>.</li><li>Add or subtract from the right. Regroup when a place has 10 or more, or when the top digit is too small.</li><li>Write a zero to fill an empty place: 4.5 = 4.50.</li></ul>',
        [example("4.5 + 2.37", ["Write 4.5 as 4.50.", "4.50 + 2.37 = 6.87"], "6.87"), example("6,003 − 2,458", ["Regroup across the zeros: 5 thousands, 9 hundreds, 9 tens, 13 ones.", "13 − 8 = 5, 9 − 5 = 4, 9 − 4 = 5, 5 − 2 = 3."], "3,545")],
        [['Lining up the last digits of 4.5 and 2.37', 'Line up the decimal points.'], ['Forgetting to regroup', 'Check each place: is the top digit big enough?'], ['Dropping a zero: 6,003 − 2,458 = 3,455', 'Regroup across every zero.']])
    faq = [('What does TEKS 4.4A ask?', 'Add and subtract whole numbers and decimals to the hundredths place using the standard algorithm.'), ('Why line up the decimal points?', 'So tenths are added to tenths and hundredths to hundredths.'), ('How do you subtract across zeros?', 'Regroup from the first nonzero place: 6,003 becomes 5 thousands, 9 hundreds, 9 tens and 13 ones.'), ('How can I check my answer?', 'Estimate by rounding, or add the difference back to the number you subtracted.')]
    make('adding-and-subtracting-whole-numbers-and-decimals', 5, 'Number and Operations', '4.4A',
         '4.4A add and subtract whole numbers and decimals to the hundredths place using the standard algorithm',
         'Adding and Subtracting Whole Numbers and Decimals', 'Adding and Subtracting Whole Numbers and Decimals',
         'Free Grade 4 worksheets for Texas TEKS 4.4A: add and subtract 4- to 6-digit numbers with the standard algorithm, subtract across zeros, add and subtract decimals and money, and word problems. 100 questions with answers.',
         'Line up the places. For decimals, line up the decimal points.', 'Regroup when needed. Write 4.5 as 4.50 to add hundredths.',
         body, faq, sets, seo_title='Grade 4 Adding and Subtracting Whole Numbers and Decimals (TEKS 4.4A, STAAR)')


if __name__ == "__main__":
    build()
