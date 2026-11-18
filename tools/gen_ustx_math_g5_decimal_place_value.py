# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Decimal Place Value to Thousandths (TEKS 5.2A)
  python3 tools/gen_ustx_math_g5_decimal_place_value.py
The value of a digit, reading and writing decimals in word form and expanded form (the US Grade 5 makers with
Texas names), expanded notation with fractions and decimals, and thousandths in measurement and money.
Wrong answers come from real mistakes: reading 0.035 as thirty-five hundredths, putting a digit in the wrong place,
and leaving out a zero placeholder.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_decimal_place_value as usp
adopt(usp)
tx_common.GRADE = "grade-5"

def d3(n, places=3):
    """n thousandths -> text with the given number of decimal places."""
    s = "%d.%03d" % (n // 1000, n % 1000)
    return s[:len(s) - (3 - places)] if places < 3 else s


def strip0(s):
    return s.rstrip("0").rstrip(".") if "." in s else s


PL = [(1, "tenths", 10), (2, "hundredths", 100), (3, "thousandths", 1000)]


def one_expand(r):
    w = r.randint(0, 99)
    digs = [r.randint(0, 9) for _ in range(3)]
    if digs[2] == 0:
        digs[2] = r.randint(1, 9)
    n = w * 1000 + digs[0] * 100 + digs[1] * 10 + digs[2]
    parts_d = ([str(w // 10 * 10)] if w >= 10 else []) + ([str(w % 10)] if w % 10 else []) + ["0.%s%d" % ("0" * i, d) for i, d in enumerate(digs) if d]
    parts_f = ([str(w // 10 * 10)] if w >= 10 else []) + ([str(w % 10)] if w % 10 else []) + ["%d × %s" % (d, fr(1, 10 ** (i + 1))) for i, d in enumerate(digs) if d]
    kind = r.choice(["dec", "frac", "back"])
    if kind == "dec":
        right = " + ".join(parts_d)
        wrong = [" + ".join(([str(w)] if w else []) + ["0.%d" % d for d in digs if d]), " + ".join(([str(w)] if w else []) + ["0.%s%d" % ("0" * (i + 1), d) for i, d in enumerate(digs) if d]), right.replace("0.0", "0.", 1) if "0.0" in right else right + " + 0.1"]
        return mcq("Which is %s in expanded form?" % d3(n), right, wrong, "Each digit times its place value: <b>%s</b>." % right)
    if kind == "frac":
        right = " + ".join(parts_f)
        wrong = [" + ".join(([str(w)] if w else []) + ["%d × %s" % (d, fr(1, 10 ** (3 - i))) for i, d in enumerate(digs) if d]), " + ".join(([str(w)] if w else []) + ["%d × %s" % (d, fr(1, 10)) for i, d in enumerate(digs) if d]), " + ".join(([str(w)] if w else []) + ["%d × %s" % (d, fr(1, 10 ** (i + 2))) for i, d in enumerate(digs) if d])]
        return mcq("Which is %s in expanded notation?" % d3(n), right, wrong, "Tenths, hundredths and thousandths: <b>%s</b>." % right)
    return mcq("What number is %s?" % " + ".join(parts_f), d3(n), [strip0(d3(n)).replace(".", ".0", 1), d3((n % 1000) * 10 + (n // 1000) * 1000) if n % 1000 < 100 else d3(n + 100), "%d.%d%d%d" % (w, digs[2], digs[1], digs[0]) if digs[0] != digs[2] else d3(n + 1)],
               "Put each digit in its place: <b>%s</b>." % d3(n))


def one_context(r):
    k = Kid(r).next()
    kind = r.choice(["kg", "km", "race", "digit"])
    if kind == "kg":
        g = r.randint(1, 999)
        return mcq("A bag of seeds has a mass of %d grams. 1 gram is one thousandth of a kilogram. What is the mass in kilograms?" % g, "%s kg" % strip0(d3(g)), ["%d kg" % g, "%s kg" % strip0(d3(g * 10)) if g * 10 < 10000 else "%s kg" % strip0(d3(g + 1)), "%s kg" % strip0(d3(g // 10)) if g >= 10 else "%s kg" % strip0(d3(g + 10))],
                   "%d thousandths = <b>%s kg</b>." % (g, strip0(d3(g))))
    if kind == "km":
        m = r.randint(1001, 9999)
        return mcq("%s runs %s meters. 1 meter is one thousandth of a kilometer. How many kilometers is that?" % (k["n"], comma(m)), "%s km" % strip0(d3(m)), ["%s km" % strip0("%d.%04d" % (m // 10000, m % 10000)), "%s km" % comma(m), "%s km" % strip0(d3(m * 10))],
                   "%s thousandths of a kilometer = <b>%s km</b>." % (comma(m), strip0(d3(m))))
    if kind == "race":
        t = r.randint(10000, 15999)
        ds = [t % 10, t // 10 % 10, t // 100 % 10, t // 1000 % 10]
        if len(set(ds)) < 4:
            return None
        return mcq("A runner's time is %s seconds. Which digit is in the thousandths place?" % d3(t), str(ds[0]), [str(x) for x in ds[1:]],
                   "The third digit after the decimal point is thousandths: <b>%d</b>." % ds[0])
    n = r.randint(1000, 99999)
    if len(set(str(n))) < len(str(n)):
        return None
    p = r.choice(PL)
    s = d3(n)
    digit = s[s.index(".") + p[0]]
    return mcq("In %s, which digit is in the %s place?" % (s, p[1]), digit, [c for c in dict.fromkeys(s.replace(".", "")) if c != digit], "Count places after the decimal point: tenths, hundredths, thousandths. <b>%s</b>." % digit)


def build():
    sets, R = build_sets([
        ("Value of a digit, 10 times and 1/10 as much", [("run", usp.set_value, (), 20)]),
        ("Read and write decimals", [("run", usp.set_forms, (), 20)]),
        ("Expanded form and expanded notation", [("collect", one_expand, 20)]),
        ("Thousandths in measurement", [("collect", one_context, 20)]),
        ("Powers of 10", [("run", usp.set_powers, (), 20)]),
    ], 65001)
    finish(sets, R)
    body = lesson('<ul><li>After the decimal point come <b>tenths</b>, <b>hundredths</b> and <b>thousandths</b>. 4.375 = 4 + 0.3 + 0.07 + 0.005.</li><li>Each place is 10 times the place to its right and 1/10 of the place to its left.</li><li><b>Expanded notation</b> can use fractions: 4 + 3 × 1/10 + 7 × 1/100 + 5 × 1/1,000.</li><li>Read 4.375 as four and three hundred seventy-five thousandths.</li></ul>',
        [example("Write 12.046 in expanded form.", ["10 + 2", "0 tenths", "0.04 + 0.006"], "10 + 2 + 0.04 + 0.006"), example("Write seven and nine thousandths.", ["7 ones", "0 tenths, 0 hundredths, 9 thousandths"], "7.009")],
        [['Writing 7.9 for seven and nine thousandths', 'Thousandths is the third place: 7.009.'], ['Reading 0.035 as thirty-five hundredths', 'The last digit is in the thousandths place: thirty-five thousandths.'], ['Leaving out zeros in expanded form', 'Skip a place with 0, but keep every other digit in its own place.']])
    faq = [('What does TEKS 5.2A ask?', 'Represent the value of the digit in decimals through the thousandths using expanded notation and numerals.'), ('How do you read 3.042?', "Three and forty-two thousandths. Say the word 'and' for the decimal point."), ('What is expanded notation for decimals?', 'Each digit times its place value, such as 3 + 4 × 1/100 + 2 × 1/1,000 for 3.042.'), ('How are thousandths used?', 'In metric measurement (1 g = 0.001 kg, 1 m = 0.001 km) and in race times.')]
    make('decimal-place-value-to-thousandths', 1, 'Number and Operations', '5.2A',
         '5.2A represent the value of the digit in decimals through the thousandths using expanded notation and numerals',
         'Decimal Place Value to Thousandths', 'Decimal Place Value',
         'Free Grade 5 decimal place value worksheets for Texas TEKS 5.2A: value of a digit to thousandths, word form, expanded form and expanded notation, thousandths in measurement and powers of 10. 100 questions with answers.',
         'Tenths, hundredths, thousandths: 4.375 = 4 + 0.3 + 0.07 + 0.005.', 'Each place is 10 times the place to its right. The third place after the point is thousandths.',
         body, faq, sets, seo_title='Grade 5 Decimal Place Value to Thousandths Worksheets (TEKS 5.2A, STAAR)')


if __name__ == "__main__":
    build()
