# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Dividing Decimals by Whole Numbers (TEKS 5.3F, 5.3G)
  python3 tools/gen_ustx_math_g5_divide_decimals.py
Dividing decimals with models and long division (the US Grade 5 maker with Texas names), dividing decimals with
up to four-digit dividends by 2-digit whole numbers, placing the decimal point, and money and measurement word
problems.
Wrong answers come from real mistakes: putting the decimal point in the wrong place, forgetting a zero placeholder,
and dividing the divisor by the dividend.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_mul_div_decimals as usm
adopt(usm)
tx_common.GRADE = "grade-5"

def one_div(r, big=False):
    d = r.randint(11, 39) if big else r.randint(2, 9)
    q = r.randint(11, 999)
    p = r.choice([1, 2])
    n = q * d
    if n >= 10000 or q % 10 == 0 or n % 10 == 0:
        return None
    qs = "%d.%0*d" % (q // 10 ** p, p, q % 10 ** p)
    ns = "%d.%0*d" % (n // 10 ** p, p, n % 10 ** p)
    wrong = ["%d.%0*d" % (q // 10 ** (p - 1), p - 1, q % 10 ** (p - 1)) if p > 1 else str(q), "%d.%0*d" % (q // 10 ** (p + 1), p + 1, q % 10 ** (p + 1)), str(q) if p > 1 else "%d.%02d" % (q // 100, q % 100)]
    return mcq("%s ÷ %d = ?" % (ns, d), qs, wrong, "Divide as with whole numbers and put the decimal point straight above: %s ÷ %d = <b>%s</b>. Check: %s × %d = %s." % (ns, d, qs, qs, d, ns))


def one_model(r):
    d = r.randint(2, 6)
    q = r.randint(2, 9)
    n = d * q
    kind = r.choice(["tenths", "hundredths"])
    if kind == "tenths":
        return mcq("%s tenths are shared equally into %d groups. How much is in each group? (Write as a decimal.)" % (n, d), "0.%d" % q, ["%d" % q, "0.0%d" % q, "0.%d" % n if n < 10 else "%d.%d" % (n // 10, n % 10)],
                   "%d tenths ÷ %d = %d tenths = <b>0.%d</b>." % (n, d, q, q))
    return mcq("A hundredths grid has %d squares shaded. They are split into %d equal groups. What decimal is each group?" % (n, d), "0.%02d" % q, ["0.%d" % q, "0.%02d" % n, "%d" % q],
               "%d hundredths ÷ %d = %d hundredths = <b>0.%02d</b>." % (n, d, q, q))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["split", "rope", "price"])
    if kind == "split":
        n = r.randint(3, 6)
        c = r.randint(305, 2495)
        t = c * n
        return mcq("%d friends share a $%d.%02d pizza bill equally. How much does each pay?" % (n, t // 100, t % 100), "$%d.%02d" % (c // 100, c % 100), ["$%d.%02d" % ((t - n) // 100, (t - n) % 100), "$%d.%02d" % (c // 10 // 100, c // 10 % 100), "$%d.%02d" % ((c + 10) // 100, (c + 10) % 100)],
                   "$%d.%02d ÷ %d = <b>$%d.%02d</b>." % (t // 100, t % 100, n, c // 100, c % 100))
    if kind == "rope":
        n = r.randint(12, 24)
        q = r.randint(11, 95)
        t = q * n
        return mcq("A %d.%d-meter rope is cut into %d equal pieces. How long is each piece?" % (t // 10, t % 10, n), "%d.%d meters" % (q // 10, q % 10), ["%d meters" % q, "0.%02d meters" % q if q < 100 else "x", "%d.%d meters" % ((q + 10) // 10, (q + 10) % 10)],
                   "%d.%d ÷ %d = <b>%d.%d meters</b>." % (t // 10, t % 10, n, q // 10, q % 10))
    n = r.randint(12, 36)
    c = r.randint(105, 499)
    t = c * n
    return mcq("A case of %d water bottles costs $%d.%02d. What is the cost of one bottle?" % (n, t // 100, t % 100), "$%d.%02d" % (c // 100, c % 100), ["$%d.%02d" % (c // 10 // 100, c // 10 % 100), "$%d.%02d" % ((c + 100) // 100, (c + 100) % 100), "$%d.%02d" % ((c + 5) // 100, (c + 5) % 100)],
               "$%d.%02d ÷ %d = <b>$%d.%02d</b>." % (t // 100, t % 100, n, c // 100, c % 100))


def build():
    sets, R = build_sets([
        ("Share tenths and hundredths: models", [("collect", one_model, 20)]),
        ("Divide decimals with long division", [("run", usm.set_divide, (usm.People,), 20)]),
        ("Place the decimal point in the quotient", [("collect", one_div, 20)]),
        ("Dividing by 2-digit whole numbers", [("collect", lambda r: one_div(r, True), 20)]),
        ("Money and measurement word problems", [("collect", one_story, 20)]),
    ], 65007)
    finish(sets, R)
    body = lesson('<ul><li>To divide a decimal by a whole number, divide as with whole numbers and put the <b>decimal point straight up</b> into the quotient.</li><li>Write zeros as placeholders when needed: 0.36 ÷ 4 = 0.09.</li><li>Models: 0.6 is 6 tenths, so 0.6 ÷ 3 is 2 tenths = 0.2.</li><li>Check by multiplying the quotient by the divisor.</li></ul>',
        [example("8.75 ÷ 25", ["875 ÷ 25 = 35", "Decimal point straight up"], "0.35"), example("0.36 ÷ 4", ["36 hundredths ÷ 4 = 9 hundredths"], "0.09")],
        [['Putting the decimal point in the wrong place', 'Line it up straight above the decimal point in the dividend.'], ['Forgetting a zero: 0.36 ÷ 4 = 0.9', '9 hundredths is 0.09.'], ['Dividing the wrong way', 'The total is the dividend; it goes inside.']])
    faq = [('What does TEKS 5.3F ask?', 'Represent quotients of decimals to the hundredths, up to four-digit dividends and two-digit whole number divisors, using objects and pictorial models, including area models.'), ('What does TEKS 5.3G ask?', 'Solve for quotients of decimals to the hundredths, up to four-digit dividends and two-digit whole number divisors, using strategies and the standard algorithm.'), ('Where does the decimal point go?', 'Straight above the decimal point in the dividend.'), ('How do I check a decimal quotient?', 'Multiply it by the divisor. You should get the dividend.')]
    make('dividing-decimals', 7, 'Number and Operations', '5.3F, 5.3G',
         '5.3F represent quotients of decimals to the hundredths, up to four-digit dividends and two-digit whole number divisors, using objects and pictorial models, including area models; 5.3G solve for quotients of decimals to the hundredths, up to four-digit dividends and two-digit whole number divisors, using strategies and algorithms, including the standard algorithm',
         'Dividing Decimals by Whole Numbers', 'Dividing Decimals',
         'Free Grade 5 worksheets for Texas TEKS 5.3F and 5.3G: divide decimals by whole numbers with models and long division, place the decimal point, 2-digit divisors and money word problems. 100 questions with answers.',
         'Divide as with whole numbers; put the decimal point straight up.', '0.36 ÷ 4 = 0.09. Check by multiplying the quotient by the divisor.',
         body, faq, sets, seo_title='Grade 5 Dividing Decimals Worksheets (TEKS 5.3F, 5.3G, STAAR)')


if __name__ == "__main__":
    build()
