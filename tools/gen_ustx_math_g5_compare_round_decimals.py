# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Comparing, Ordering and Rounding Decimals (TEKS 5.2B, 5.2C)
  python3 tools/gen_ustx_math_g5_compare_round_decimals.py
Comparing and ordering decimals to thousandths, rounding to the nearest tenth or hundredth (the US Grade 5 makers
with Texas names), comparing with symbols, and rounding in real-world problems.
Wrong answers come from real mistakes: thinking 0.125 > 0.2 because it has more digits, rounding to the wrong
place, and keeping digits after the rounding place.
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


def one_sym(r):
    a = r.randint(1, 9999)
    kind = r.choice(["len", "len", "near"])
    if kind == "len":
        t = r.randint(1, 9)
        b = r.randint(100, 999)
        x, xp = t * 100, 1
        if x == b:
            return None
        sa, sb = strip0(d3(x)), d3(b)
    else:
        x = a
        b = a + r.choice([-10, -1, 1, 10, 100])
        if b <= 0:
            return None
        sa, sb = d3(x), d3(b)
    w = r.randint(0, 9)
    sa, sb = str(w) + sa[1:], str(w) + sb[1:]
    sym = "&gt;" if x > b else "&lt;"
    if r.random() < 0.5:
        sa, sb, sym = sb, sa, "&lt;" if sym == "&gt;" else "&gt;"
    return mcq("Compare: %s ☐ %s" % (sa, sb), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
               "Write both with thousandths and compare from the left: <b>%s %s %s</b>." % (sa, sym, sb))


def one_round_story(r):
    k = Kid(r).next()
    kind = r.choice(["gas", "time", "mass", "price"])
    n = r.randint(1001, 99999)
    if kind == "gas":
        n = r.randint(2001, 4999)
        v = "%d.%03d" % (n // 1000, n % 1000)
        if n % 10 == 5:
            return None
        return mcq("Gas costs $%s a gallon. What is the price rounded to the nearest cent (hundredth)?" % v, "$%.2f" % round(n / 1000 + 1e-9, 2), ["$%.2f" % (n // 10 / 100), "$%.1f" % round(n / 1000 + 1e-9, 1), "$%.2f" % (round(n / 1000 + 1e-9, 2) + 0.01)],
                   "Look at the thousandths digit to round to hundredths: <b>$%.2f</b>." % round(n / 1000 + 1e-9, 2))
    if kind == "time":
        if n % 100 in (0, 50) or (n // 10) % 10 == 5:
            return None
        v = "%d.%03d" % (n // 1000, n % 1000)
        right = round(n / 1000 + 1e-9, 1)
        return mcq("%s swims a lap in %s seconds. Round the time to the nearest tenth." % (k["n"], v), "%.1f" % right, ["%.1f" % (right + 0.1 if n // 100 / 10 == right else n // 100 / 10), "%.2f" % round(n / 1000 + 1e-9, 2), "%.1f" % (right - 0.1)],
                   "Look at the hundredths digit: <b>%.1f</b>." % right)
    m = r.randint(201, 999)
    v = "%d.%02d" % (m // 100, m % 100)
    if m % 10 == 5 or m % 10 == 0:
        return None
    return mcq("A bag of oranges weighs %s pounds. Round the weight to the nearest tenth of a pound." % v, "%.1f pounds" % round(m / 100 + 1e-9, 1), ["%.1f pounds" % (m // 10 / 10) if m // 10 / 10 != round(m / 100 + 1e-9, 1) else "%.1f pounds" % (round(m / 100 + 1e-9, 1) + 0.1), "%d pounds" % round(m / 100), "%s pounds" % v],
               "The hundredths digit is %d, so round %s: <b>%.1f pounds</b>." % (m % 10, "up" if m % 10 >= 5 else "down", round(m / 100 + 1e-9, 1)))


def one_order(r):
    vals = set()
    w = r.randint(0, 9)
    while len(vals) < 4:
        vals.add(r.choice([r.randint(1, 9) * 100, r.randint(10, 99) * 10, r.randint(100, 999)]))
    vals = sorted(vals)
    t = [str(w) + "." + d3(v)[2:].rstrip("0") for v in vals]
    up = r.random() < 0.5
    order = t if up else t[::-1]
    shown = t[:]
    while shown in (t, t[::-1]):
        r.shuffle(shown)
    bylen = sorted(t, key=lambda s: (len(s), s))
    wrong = [t[::-1] if up else t, bylen if bylen != order else bylen[::-1], [t[1], t[0], t[2], t[3]] if up else [t[2], t[3], t[1], t[0]]]
    J = lambda L: "; ".join(L)
    return mcq("Order from %s: %s" % ("least to greatest" if up else "greatest to least", J(shown)), J(order), [J(x) for x in wrong if x != order],
               "Write each with thousandths, then compare: <b>%s</b>." % J(order))


def build():
    sets, R = build_sets([
        ("Compare with symbols", [("collect", one_sym, 20)]),
        ("Compare and order decimals to thousandths", [("run", usp.set_compare, (usp.People,), 10), ("collect", one_order, 10)]),
        ("Round decimals", [("run", usp.set_round, (usp.People,), 20)]),
        ("Round in real-world problems", [("collect", one_round_story, 20)]),
        ("Order decimals", [("collect", one_order, 20)]),
    ], 65002)
    finish(sets, R)
    body = lesson('<ul><li>To compare decimals, line up the decimal points and compare place by place from the left. Write zeros so they have the same number of places: 0.2 = 0.200 &gt; 0.125.</li><li>To <b>round</b> to the nearest tenth, look at the hundredths digit; to the nearest hundredth, look at the thousandths digit. 5 or more rounds up.</li><li>After rounding, drop the digits to the right of the rounding place.</li></ul>',
        [example("Compare 0.2 and 0.125.", ["0.200 and 0.125", "2 tenths &gt; 1 tenth"], "0.2 &gt; 0.125"), example("Round 3.468 to the nearest hundredth.", ["Hundredths digit: 6", "Next digit 8 ≥ 5, round up"], "3.47")],
        [['Thinking a longer decimal is greater: 0.125 &gt; 0.2', 'Compare place by place, not by how many digits.'], ['Rounding to the wrong place', 'Find the rounding place first, then look one place to the right.'], ['Keeping extra digits: 3.468 → 3.478', 'Drop every digit after the rounding place.']])
    faq = [('What does TEKS 5.2B ask?', 'Compare and order two decimals to thousandths and represent comparisons using &gt;, &lt; or =.'), ('What does TEKS 5.2C ask?', 'Round decimals to tenths or hundredths.'), ('Is 0.50 the same as 0.5?', 'Yes. Zeros at the end of a decimal do not change its value.'), ('Why round decimals?', 'Prices, times and measurements are often rounded to make them easier to use, such as gas prices to the nearest cent.')]
    make('comparing-and-rounding-decimals', 2, 'Number and Operations', '5.2B, 5.2C',
         '5.2B compare and order two decimals to thousandths and represent comparisons using the symbols >, <, or =; 5.2C round decimals to tenths or hundredths',
         'Comparing, Ordering and Rounding Decimals', 'Comparing and Rounding Decimals',
         'Free Grade 5 decimal worksheets for Texas TEKS 5.2B and 5.2C: compare and order decimals to thousandths, round to tenths and hundredths, and real-world rounding. 100 questions with answers.',
         'Line up the decimal points and compare from the left.', 'Round to tenths by looking at hundredths; round to hundredths by looking at thousandths.',
         body, faq, sets, seo_title='Grade 5 Comparing and Rounding Decimals Worksheets (TEKS 5.2B, 5.2C, STAAR)')


if __name__ == "__main__":
    build()
