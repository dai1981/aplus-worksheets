# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Decimal Numbers to Hundredths: Models, Place Value and Fractions (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_decimals.py
Decimals from tenths bars and hundredths grids (US Grade 4 maker), reading and writing decimals in words, the place
value and value of a digit and the digit in a given place, changing between decimals and fractions with denominators
10 and 100 (US Grade 4 maker and own makers), and pesos and centavos.
Wrong answers come from real mistakes: writing 7 hundredths as 0.7, reading 3.45 as three point forty-five hundredths,
and mixing up the tenths and hundredths places.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_decimals as usd
adopt(usd)
if hasattr(usd, 'R'): usd.R = random.Random(704210)
ph_common.GRADE = "grade-4"

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


def d2(h):
    """hundredths (int) -> decimal string: 347 -> 3.47, 30 -> 0.3, 5 -> 0.05"""
    w, f = divmod(h, 100)
    s = "%d.%02d" % (w, f)
    s = s.rstrip("0").rstrip(".") if f % 10 == 0 else s
    return comma(int(s)) if "." not in s else comma(w) + s[s.index("."):]


def d2k(h):
    """keep two places: 3.40"""
    w, f = divmod(h, 100)
    return "%s.%02d" % (comma(w), f)


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
        "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def say(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    return ONES[n // 100] + " hundred" + (" " + say(n % 100) if n % 100 else "")


def one_read(r):
    w = r.choice([0, 0, r.randint(1, 99)])
    if r.random() < 0.35:
        t = r.randint(1, 9)
        h, word = w * 100 + t * 10, "%s tenth%s" % (say(t), "" if t == 1 else "s")
    else:
        f = r.randint(1, 99)
        if f % 10 == 0:
            raise AssertionError
        h, word = w * 100 + f, "%s hundredth%s" % (say(f), "" if f == 1 else "s")
    words = (say(w) + " and " if w else "") + word
    if r.random() < 0.5:
        right = d2(h)
        f = h % 100
        wr = [d2(w * 100 + (f // 10 if f % 10 == 0 else f * 10 if f < 10 else f // 10)) if True else "", "%s.%s" % (w, f), d2(h * 10) if h < 1000 else d2(h + 100)]
        wr = [x for x in wr if x != right]
        return mcq("Write in numbers: <b>%s</b>" % words, right, wr + [d2(h + 1)], "%s → <b>%s</b>." % (words.capitalize(), right))
    right = words
    f = h % 100
    if f % 10 == 0:
        alt = (say(w) + " and " if w else "") + "%s hundredths" % say(f // 10)
    else:
        alt = (say(w) + " and " if w else "") + "%s tenths" % say(f) if f < 20 else (say(w) + " and " if w else "") + "%s thousandths" % say(f)
    wr = [alt, (say(w) + " point " if w else "point ") + say(f if f % 10 else f // 10), (say(w) + " and " if w else "") + word.replace("hundredth", "tenth") if "hundredth" in word else (say(w) + " and " if w else "") + word.replace("tenth", "hundredth")]
    return mcq("How do you read <b>%s</b>?" % d2(h), right, wr, "The last digit is in the %s place, so read it as <b>%s</b>." % ("tenths" if f % 10 == 0 else "hundredths", words))


PL = ["ones", "tenths", "hundredths", "tens"]


def one_pv(r):
    h = r.randint(1000, 9999)
    if len(set(str(h))) < 4:
        raise AssertionError
    s = d2k(h)
    digits = {"tens": h // 1000, "ones": h // 100 % 10, "tenths": h // 10 % 10, "hundredths": h % 10}
    val = {"tens": lambda d: str(d * 10), "ones": lambda d: str(d), "tenths": lambda d: d2(d * 10), "hundredths": lambda d: d2(d)}
    kind = r.choice(["place", "value", "digit"])
    p = r.choice(["ones", "tenths", "hundredths", "tens"])
    d = digits[p]
    if d == 0:
        raise AssertionError
    if kind == "place":
        return mcq("In <b>%s</b>, what is the place value of the digit %d?" % (s, d), p, [x for x in PL if x != p],
                   "In %s: %s. The %d is in the <b>%s</b> place." % (s, ", ".join("%d %s" % (digits[x], x[:-1] if digits[x] == 1 else x) for x in ("tens", "ones", "tenths", "hundredths")), d, p))
    if kind == "value":
        right = val[p](d)
        wr = [val[x](d) for x in PL if x != p]
        return mcq("In <b>%s</b>, what is the value of the digit %d?" % (s, d), right, wr, "The %d is in the %s place, so its value is <b>%s</b>." % (d, p, right))
    right = d
    wr = [digits[x] for x in PL if x != p]
    return mcq("Which digit is in the <b>%s</b> place in %s?" % (p, s), right, wr + [d + 1 if d < 9 else d - 1], "%s: the %s digit is <b>%d</b>." % (s, p, d), allow_zero=False)


def one_fd(r):
    if r.random() < 0.5:
        if r.random() < 0.5:
            n, d = r.randint(1, 9), 10
            right, wr = d2(n * 10), [d2(n), "%d.10" % n, "%d.0" % n]
        else:
            n, d = r.randint(1, 99), 100
            if n % 10 == 0:
                raise AssertionError
            right, wr = d2(n), [d2(n * 10) if n < 10 else "%d.%d" % (n // 10, n % 10), "%d.100" % n, d2(n * 10 % 1000 + 1) if n < 10 else "0.%03d" % n]
        return mcq("Write %s as a decimal." % fr(n, d), right, wr, "%s means %d %s, so it is <b>%s</b>." % (fr(n, d), n, "tenths" if d == 10 else "hundredths", right))
    w = r.randint(0, 9)
    f = r.randint(1, 99)
    if f % 10 == 0:
        raise AssertionError
    h = w * 100 + f
    right = ("%d %s" % (w, fr(f, 100))) if w else fr(f, 100)
    wr = [("%d %s" % (w, fr(f, 10))) if w else fr(f, 10), fr(h, 10), ("%d %s" % (f, fr(w, 100))) if w else fr(f, 1000)]
    return mcq("Which fraction or mixed number is equal to <b>%s</b>?" % d2(h), right, wr, "%s has %d hundredths after the decimal point, so it is <b>%s</b>." % (d2(h), f, right))


def one_money(r):
    k = Kid(r).next()
    kind = r.choice(["c2p", "p2c", "coins", "meter"])
    if kind == "c2p":
        c = r.randint(5, 99)
        if c % 5:
            c = c // 5 * 5 or 5
        q = "%s has %d centavos. ₱1 = 100 centavos. How do you write %d centavos in pesos?" % (k["n"], c, c)
        right = "₱" + d2k(c)
        wr = ["₱%d.00" % c, "₱%s" % d2k(c * 10) if c < 10 else "₱0.0%d" % (c // 10), "₱%d.%d" % (c // 100, c)]
        return mcq(q, right, wr, "%d centavos = %s of a peso = <b>%s</b>." % (c, fr(c, 100), right))
    if kind == "p2c":
        w, c = r.randint(1, 9), r.choice([5, 10, 25, 50, 75])
        q = "A pencil costs ₱%d.%02d. How many centavos is that?" % (w, c)
        right = w * 100 + c
        return mcq(q, "%d centavos" % right, ["%d centavos" % x for x in (w + c, w * 10 + c, right * 10)], "₱%d = %d centavos. %d + %d = <b>%d centavos</b>." % (w, w * 100, w * 100, c, right))
    if kind == "coins":
        a, b = r.randint(1, 3), r.randint(1, 4)
        q = "%s has %d twenty-five-centavo coin%s and %d one-peso coin%s. How much money is that?" % (k["n"], a, "" if a == 1 else "s", b, "" if b == 1 else "s")
        h = a * 25 + b * 100
        right = "₱" + d2k(h)
        wr = ["₱%d.%02d" % (a + b, 0), "₱%d.%d" % (b, a * 25 // 10), "₱" + d2k(a * 100 + b * 25)]
        return mcq(q, right, [x for x in wr if x != right], "%d × 25 centavos = %d centavos, and %d × ₱1 = ₱%d. Together: <b>%s</b>." % (a, a * 25, b, b, right))
    cm = r.randint(101, 299)
    if cm % 10 == 0:
        raise AssertionError
    q = "%s is %d cm tall. 1 m = 100 cm. How tall is %s in meters?" % (k["n"], cm, k["he"])
    right = d2(cm) + " m"
    return mcq(q, right, ["%d.%d m" % (cm // 100, cm % 100 // 10), "%s m" % comma(cm), "%d.%02d m" % (cm // 10, cm % 10)], "%d cm = %d hundredths of a meter = <b>%s</b>." % (cm, cm, right))


def build():
    sets, R = build_sets([
        ("Decimals from models", [("run", usd.set_grids, ("rnd",), 20)]),
        ("Read and write decimals", [("collect", uniq(one_read), 20)]),
        ("Place value of decimals", [("collect", uniq(one_pv), 20)]),
        ("Decimals and fractions", [("run", usd.set_place, ("rnd",), 10), ("collect", uniq(one_fd), 10)]),
        ("Pesos, centavos and meters", [("collect", uniq(one_money), 20)]),
    ], 70421)
    finish(sets, R)
    body = lesson("<ul><li>A <b>decimal</b> is another way to write a fraction with a denominator of 10 or 100. 0.3 = <span class='fr'><span class='fn'>3</span><span class='fd'>10</span></span> and 0.47 = <span class='fr'><span class='fn'>47</span><span class='fd'>100</span></span>.</li><li>After the decimal point come the <b>tenths</b>, then the <b>hundredths</b>.</li><li>Read the whole number, say <b>and</b> for the point, then read the decimal part with the name of its last place: 3.45 is three and forty-five hundredths.</li><li>₱1 = 100 centavos, so ₱0.25 is 25 centavos.</li></ul>",
        [example("7 hundredths", ["0 ones, 0 tenths, 7 hundredths"], "0.07"), example("2.38", ["2 ones, 3 tenths, 8 hundredths"], "two and thirty-eight hundredths")],
        [['7 hundredths as 0.7', '0.7 is 7 tenths; 7 hundredths is 0.07.'], ['Reading “point forty-five”', 'Say “and”, then forty-five hundredths.'], ['Mixing up the places', 'Tenths come first after the point.']])
    faq = [('What does MATATAG Math 4 ask about decimals?', 'Represent decimal numbers using models to show the relationship to fractions, read and write decimals to hundredths, find the place value and value of a digit, and convert between decimals and fractions with denominators 10 or 100.'), ('Is 0.5 the same as 0.50?', 'Yes. 5 tenths = 50 hundredths.'), ('How many centavos are in ₱2.50?', '250 centavos.'), ('What is the value of 6 in 3.16?', '6 hundredths, or 0.06.')]
    make('decimal-numbers-to-hundredths', 21, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Represent decimal numbers using models and manipulatives to show the relationship to fractions; read and write decimal numbers with decimal parts to hundredths; determine the place value to hundredths of a digit in a given decimal number, the value of a digit, and the digit of a number, given its place value; convert decimal numbers to fractions, and fractions with denominators 10 or 100 to decimals.',
         'Decimal Numbers to Hundredths: Models, Place Value and Fractions', 'Decimals to Hundredths',
         'Free Grade 4 decimals worksheets for the DepEd MATATAG curriculum: tenths and hundredths models, reading and writing decimals, place value, decimals and fractions, pesos and centavos. 100 questions with answers.',
         'Tenths come first after the point, then hundredths.', '0.47 = 47/100: forty-seven hundredths.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
