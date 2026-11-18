# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Comparing and Ordering Numbers to 1,200 (TEKS 2.2C, 2.2D)
  python3 tools/gen_ustx_math_g2_compare_numbers.py
Comparing with base-ten blocks, comparing place by place, the symbols >, < and =, ordering numbers, and word
problems (the US Grade 2 makers with Texas names), plus greater and less numbers (own maker).
Wrong answers come from real mistakes: comparing the ones first, flipping the symbol, and thinking a number with
more 9s is bigger.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_compare as cmp
adopt(cmp)
tx_common.GRADE = "grade-2"

def one_more(r):
    n = r.randint(105, 1150)
    want = r.choice(["greater", "less"])
    if want == "greater":
        right = n + r.choice([1, 10, 100, 25, 50])
        if right > 1200:
            return None
        w = [n - r.choice([1, 10, 100]), n, n - 50]
    else:
        right = n - r.choice([1, 10, 100, 25, 50])
        w = [n + r.choice([1, 10, 100]), n, n + 50]
    w = [str(x) for x in dict.fromkeys(w) if x != right and 0 < x <= 1200]
    return mcq("Which number is <b>%s than %s</b>?" % (want, n), str(right), w, "%d is %s than %d. <b>%d</b>." % (right, want, n, right))


def build():
    sets, R = build_sets([
        ("Compare with base-ten blocks", [("run", cmp.set_blocks, ("rnd", "seen"), 20)]),
        ("Compare place by place", [("run", cmp.set_places, ("rnd", "seen"), 20)]),
        ("Use >, < and =", [("run", cmp.set_symbols, ("rnd", "seen"), 20)]),
        ("Order numbers and find greater or less", [("run", cmp.set_order, ("rnd", "seen"), 10), ("collect", one_more, 10)]),
        ("Word problems", [("run", cmp.set_words, ("rnd", "seen", cmp.People), 20)]),
    ], 69202)
    finish(sets, R)
    body = lesson('<ul><li>Compare the <b>biggest place first</b>: thousands, then hundreds, then tens, then ones.</li><li>&gt; means greater than; &lt; means less than. The open side faces the bigger number.</li><li>To order numbers, compare them two at a time.</li></ul>',
        [example("Compare 482 and 428.", ["Hundreds are the same: 4 = 4", "Tens: 8 > 2"], "482 > 428"), example("Compare 1,015 and 998.", ["1,015 has 1 thousand", "998 has 0 thousands"], "1,015 > 998")],
        [['Comparing the ones first', 'Start with the biggest place.'], ['Flipping the symbol', 'The open side faces the bigger number.'], ['Thinking more 9s means bigger', '1,000 > 999, because 1 thousand is more than 9 hundreds.']])
    faq = [('What does TEKS 2.2C ask?', 'Generate a number that is greater than or less than a given whole number up to 1,200.'), ('What does TEKS 2.2D ask?', 'Use place value to compare and order whole numbers up to 1,200 using comparative language, numbers and symbols.'), ('What does = mean?', 'Both sides have the same value.'), ('How do I order 3 numbers?', 'Find the least one first, then the next, then the greatest.')]
    make('comparing-and-ordering-numbers', 2, 'Number and Operations', '2.2C, 2.2D',
         '2.2C generate a number that is greater than or less than a given whole number up to 1,200; 2.2D use place value to compare and order whole numbers up to 1,200 using comparative language, numbers, and symbols (>, <, or =)',
         'Comparing and Ordering Numbers to 1,200', 'Comparing and Ordering Numbers',
         'Free Grade 2 worksheets for Texas TEKS 2.2C and 2.2D: compare numbers to 1,200 with base-ten blocks and place value, use >, < and =, order numbers and word problems. 100 questions with answers.',
         'Compare the biggest place first.', '482 > 428 because 8 tens > 2 tens.',
         body, faq, sets, seo_title='Grade 2 Comparing and Ordering Numbers Worksheets (TEKS 2.2C, 2.2D)')


if __name__ == "__main__":
    build()
