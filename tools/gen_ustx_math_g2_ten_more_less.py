# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: 10 More, 10 Less, 100 More and 100 Less (TEKS 2.7B)
  python3 tools/gen_ustx_math_g2_ten_more_less.py
Counting by 10s and 100s from any number (the US Grade 2 makers with Texas names), 10 more or 10 less, 100 more or
100 less, and number puzzles up to 1,200 (own makers).
Wrong answers come from real mistakes: changing the ones digit, changing the wrong place, and forgetting to
regroup across a hundred.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g2_skip_counting as sk
adopt(sk)
tx_common.GRADE = "grade-2"

def one_10(r):
    n = r.randint(15, 1185)
    more = r.random() < 0.5
    v = n + 10 if more else n - 10
    w = [n + 1 if more else n - 1, n + 100 if more and n + 100 <= 1200 else n - 100 if n > 100 else n + 100, n - 10 if more else n + 10]
    w = [comma(x) for x in dict.fromkeys(w) if x != v and 0 < x <= 1200]
    return mcq("What is 10 %s than %s?" % ("more" if more else "less", comma(n)), comma(v), w, "Change the <b>tens</b> digit by 1: <b>%s</b>." % comma(v))


def one_100(r):
    n = r.randint(110, 1100)
    more = r.random() < 0.5
    v = n + 100 if more else n - 100
    w = [n + 10 if more else n - 10, n - 100 if more else n + 100, n + 1 if more else n - 1]
    w = [comma(x) for x in dict.fromkeys(w) if x != v and 0 < x <= 1200]
    return mcq("What is 100 %s than %s?" % ("more" if more else "less", comma(n)), comma(v), w, "Change the <b>hundreds</b> digit by 1: <b>%s</b>." % comma(v))


def one_puzzle(r):
    n = r.randint(120, 1080)
    kind = r.choice(["start10", "start100", "chain"])
    if kind == "start10":
        v = n + 10
        return mcq("10 more than a number is %s. What is the number?" % comma(v), comma(n), [comma(v + 10), comma(v - 1), comma(v - 100)], "Go back 10: %s − 10 = <b>%s</b>." % (comma(v), comma(n)))
    if kind == "start100":
        v = n - 100
        return mcq("100 less than a number is %s. What is the number?" % comma(v), comma(n), [comma(v - 100) if v > 100 else comma(v + 10), comma(v + 10), comma(v + 1)], "Go up 100: %s + 100 = <b>%s</b>." % (comma(v), comma(n)))
    v = n + 100 - 10
    return mcq("Start at %s. Go 100 more, then 10 less. Where do you end?" % comma(n), comma(v), [comma(n + 110), comma(n - 90), comma(n + 100)], "%s + 100 = %s. %s − 10 = <b>%s</b>." % (comma(n), comma(n + 100), comma(n + 100), comma(v)))


def build():
    sets, R = build_sets([
        ("Count by 10s from any number", [("run", sk.set_tens, ("rnd", sk.People), 20)]),
        ("10 more and 10 less", [("collect", one_10, 20)]),
        ("Count by 100s from any number", [("run", sk.set_hundreds, ("rnd", sk.People), 20)]),
        ("100 more and 100 less", [("collect", one_100, 20)]),
        ("Number puzzles", [("collect", one_puzzle, 20)]),
    ], 69204)
    finish(sets, R)
    body = lesson('<ul><li><b>10 more</b> or <b>10 less</b> changes the <b>tens</b> digit by 1: 347 → 357 → 337.</li><li><b>100 more</b> or <b>100 less</b> changes the <b>hundreds</b> digit by 1: 347 → 447 → 247.</li><li>When the tens go past 9, regroup: 395 + 10 = 405.</li></ul>',
        [example("10 more than 496", ["9 tens + 1 ten = 10 tens", "Regroup to 5 hundreds"], "506"), example("100 less than 1,082", ["1 thousand 0 hundreds → 9 hundreds"], "982")],
        [['Changing the ones digit', '10 more changes the tens, not the ones.'], ['Changing the wrong place', '100 more changes the hundreds.'], ['Forgetting to regroup', '395 + 10 = 405, not 3,105.']])
    faq = [('What does TEKS 2.7B ask?', 'Use an understanding of place value to determine the number that is 10 or 100 more or less than a given number up to 1,200.'), ('Do I need to count by ones?', 'No. Just change the tens or hundreds digit.'), ('What is 10 more than 1,195?', '1,205.'), ('How is 100 more like 10 more?', 'Both change one place by 1: the hundreds or the tens.')]
    make('10-more-10-less-100-more-100-less', 4, 'Algebraic Reasoning', '2.7B',
         '2.7B use an understanding of place value to determine the number that is 10 or 100 more or less than a given number up to 1,200',
         '10 More, 10 Less, 100 More and 100 Less', '10 More and 100 More',
         'Free Grade 2 worksheets for Texas TEKS 2.7B: count by 10s and 100s, find 10 more, 10 less, 100 more and 100 less up to 1,200, and number puzzles. 100 questions with answers.',
         '10 more changes the tens; 100 more changes the hundreds.', '347 + 10 = 357. 347 + 100 = 447.',
         body, faq, sets, seo_title='Grade 2 10 More, 10 Less, 100 More, 100 Less Worksheets (TEKS 2.7B)')


if __name__ == "__main__":
    build()
