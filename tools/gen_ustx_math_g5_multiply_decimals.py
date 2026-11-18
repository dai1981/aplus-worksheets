# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Multiplying Decimals (TEKS 5.3D, 5.3E)
  python3 tools/gen_ustx_math_g5_multiply_decimals.py
A decimal times a whole number and a decimal times a decimal with grid models, multiplying by powers of 10
(the US Grade 5 makers with Texas names), placing the decimal point, and money and measurement word problems.
Wrong answers come from real mistakes: lining up decimal points as in addition, counting decimal places wrongly,
and thinking a product is always bigger than both factors.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_mul_div_decimals as usm
adopt(usm)
tx_common.GRADE = "grade-5"

def fmt(n, p):
    s = "%d.%0*d" % (n // 10 ** p, p, n % 10 ** p) if p else str(n)
    return s


def one_place(r):
    a = r.randint(11, 99)
    b = r.randint(2, 9) if r.random() < 0.5 else r.randint(11, 99)
    pa, pb = r.choice([1, 2]), r.choice([0, 1]) if b < 10 else r.choice([0, 1, 2])
    if pa + pb > 2 or (pb and b % 10 == 0) or a % 10 == 0 or (a * b) % 10 == 0:
        return None
    prod = a * b
    p = pa + pb
    sa, sb = fmt(a, pa), fmt(b, pb)
    right = fmt(prod, p)
    wrong = [fmt(prod, k) for k in range(0, p + 3) if k != p][:3] if p < 2 else [fmt(prod, k) for k in (p - 2, p - 1, p + 1)]
    return mcq("%s × %s = ?" % (sa, sb), right, wrong, "%d × %d = %s. The factors have %d decimal place%s in all, so the product has %d: <b>%s</b>." % (a, b, comma(prod), p, "" if p == 1 else "s", p, right))


def one_money(r):
    k = Kid(r).next()
    c = r.randint(105, 1295)
    n = r.randint(3, 12)
    t = c * n
    item = r.choice(["notebook", "bag of chips", "movie ticket", "pound of pecans", "box of crayons"])
    return mcq("A %s costs $%d.%02d. %s buys %d. How much does %s pay?" % (item, c // 100, c % 100, k["n"], n, k["he"]), "$%d.%02d" % (t // 100, t % 100), ["$%d.%02d" % ((c + n) // 100, (c + n) % 100), "$%s" % comma(t), "$%d.%02d" % ((t + 100) // 100, (t + 100) % 100)],
               "%d × $%d.%02d = <b>$%d.%02d</b>." % (n, c // 100, c % 100, t // 100, t % 100))


def build():
    sets, R = build_sets([
        ("A decimal times a whole number", [("run", usm.set_mul_whole, (), 20)]),
        ("A decimal times a decimal with models", [("run", usm.set_mul_dec, (usm.People,), 20)]),
        ("Place the decimal point", [("collect", one_place, 20)]),
        ("Multiply by 10, 100, 1,000, 0.1 and 0.01", [("run", usm.set_powers, (), 20)]),
        ("Money and measurement word problems", [("collect", one_money, 10), ("run", usm.set_words, (usm.People,), 10)]),
    ], 65006)
    finish(sets, R)
    body = lesson('<ul><li>Multiply as if there were no decimal points: 2.4 × 0.3 → 24 × 3 = 72.</li><li>Count the decimal places in both factors (1 + 1 = 2). The product has that many: 0.72.</li><li>A hundredths grid shows tenths × tenths as hundredths.</li><li>Multiplying by a number less than 1 gives a product smaller than the other factor.</li></ul>',
        [example("2.4 × 0.3", ["24 × 3 = 72", "1 + 1 = 2 decimal places"], "0.72"), example("4 × $3.65", ["4 × 365 = 1,460", "2 decimal places"], "$14.60")],
        [['Lining up the decimal points as in addition', 'For multiplication, multiply first, then count decimal places.'], ['Counting decimal places wrongly', 'Add the places in both factors.'], ['Thinking a product is always bigger', '0.3 × 24 = 7.2, which is smaller than 24.']])
    faq = [('What does TEKS 5.3D ask?', 'Represent multiplication of decimals with products to the hundredths using objects and pictorial models, including area models.'), ('What does TEKS 5.3E ask?', 'Solve for products of decimals to the hundredths, including money, using place value, properties of operations and whole-number multiplication.'), ('How do I place the decimal point?', 'Count the total number of decimal places in the factors. The product has the same number.'), ('Why is 0.5 × 8 smaller than 8?', '0.5 is half, so 0.5 × 8 = 4.')]
    make('multiplying-decimals', 6, 'Number and Operations', '5.3D, 5.3E',
         '5.3D represent multiplication of decimals with products to the hundredths using objects and pictorial models, including area models; 5.3E solve for products of decimals to the hundredths, including situations involving money, using strategies based on place-value understandings, properties of operations, and the relationship to the multiplication of whole numbers',
         'Multiplying Decimals', 'Multiplying Decimals',
         'Free Grade 5 worksheets for Texas TEKS 5.3D and 5.3E: multiply decimals by whole numbers and decimals with grid models, place the decimal point, powers of 10 and money word problems. 100 questions with answers.',
         'Multiply as whole numbers, then count the decimal places.', '2.4 × 0.3: 24 × 3 = 72, 2 decimal places, so 0.72.',
         body, faq, sets, seo_title='Grade 5 Multiplying Decimals Worksheets (TEKS 5.3D, 5.3E, STAAR)')


if __name__ == "__main__":
    build()
