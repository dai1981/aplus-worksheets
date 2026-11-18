# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Multiplication and Division Word Problems: Interpreting Remainders (TEKS 4.4H)
  python3 tools/gen_ustx_math_g4_mult_div_word_problems.py
One- and two-step multiplication and division problems: what to do with a remainder, times as many, and finding
the smaller amount (the US Grade 4 division and comparison makers with Texas names), plus problems that ask for
the remainder itself.
Wrong answers come from real mistakes: ignoring the remainder when you need one more group, rounding up when the
question asks for full groups, and adding instead of multiplying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_division as usd
import gen_us_math_g4_comparison_problems as usc
adopt(usd)
adopt(usc)
tx_common.GRADE = "grade-4"

def one_rem(r):
    k = Kid(r).next()
    d = r.randint(3, 9)
    q = r.randint(12, 99)
    rem = r.randint(1, d - 1)
    n = d * q + rem
    kind = r.choice(["up", "down", "left"])
    if kind == "up":
        return mcq("%d students ride vans to a game. Each van holds %d students. How many vans are needed so every student has a seat?" % (n, d), q + 1, [q, rem, q + rem],
                   "%d ÷ %d = %d R%d. The %d extra student%s need one more van: <b>%d</b>." % (n, d, q, rem, rem, "" if rem == 1 else "s", q + 1))
    if kind == "down":
        return mcq("%s has %d beads. Each bracelet uses %d beads. How many bracelets can %s finish?" % (k["n"], n, d, k["he"]), q, [q + 1, rem, n - d],
                   "%d ÷ %d = %d R%d. Only full bracelets count: <b>%d</b>." % (n, d, q, rem, q))
    return mcq("%d cookies are packed in boxes of %d. How many cookies are left over?" % (n, d), rem, [q, d - rem if d - rem != rem else rem + 1, q + 1],
               "%d ÷ %d = %d R%d. <b>%d</b> cookie%s left over." % (n, d, q, rem, rem, " is" if rem == 1 else "s are"), allow_zero=False)


def build():
    sets, R = build_sets([
        ("What to do with the remainder", [("run", usd.set_story, ("rnd", usd.People), 20)]),
        ("Remainders: round up, drop or answer with it", [("collect", one_rem, 20)]),
        ("Find the bigger amount: multiply", [("run", usc.set_bigger, ("rnd", usc.People), 20)]),
        ("Find the smaller amount or how many times: divide", [("run", usc.set_smaller, ("rnd", usc.People), 20)]),
        ("Times as many or how many more?", [("run", usc.set_more_or_times, ("rnd", usc.People), 20)]),
    ], 64011)
    finish(sets, R)
    body = lesson('<ul><li>Multiply when you know the number of groups and the size of each group, or when one amount is <b>times as many</b> as another.</li><li>Divide when you know the total and need the size of each group or the number of groups.</li><li>A <b>remainder</b> depends on the question: round up when everyone needs a place, drop it when only full groups count, or give the remainder when the question asks how many are left.</li></ul>',
        [example("125 students, 8 per van. How many vans?", ["125 ÷ 8 = 15 R5", "5 students still need a seat."], "16 vans"), example("A tree is 6 times as tall as a 9-foot fence. How tall is the tree?", ["6 × 9"], "54 feet")],
        [['Ignoring a remainder when everyone needs a seat', 'Add one more group for the leftovers.'], ['Rounding up when only full groups count', 'If a bracelet needs 8 beads, a partial bracelet does not count.'], ['Adding for times as many', 'Times as many means multiply.']])
    faq = [('What does TEKS 4.4H ask?', 'Solve with fluency one- and two-step problems involving multiplication and division, including interpreting remainders.'), ('What does interpreting a remainder mean?', 'Deciding what the leftover amount means in the story: one more group, ignore it, or report it.'), ('How do I know whether to multiply or divide?', 'If you need a total from equal groups or times as many, multiply. If you split a total, divide.'), ('Why are remainders tricky on the STAAR?', 'The same division can have different answers depending on the question, so always reread what is asked.')]
    make('multiplication-and-division-word-problems', 11, 'Number and Operations', '4.4H',
         '4.4H solve with fluency one- and two-step problems involving multiplication and division, including interpreting remainders',
         'Multiplication and Division Word Problems: Interpreting Remainders', 'Multiplication and Division Word Problems',
         'Free Grade 4 word problem worksheets for Texas TEKS 4.4H: interpret remainders, times as many, find the smaller amount and one- and two-step multiplication and division problems. 100 STAAR-style questions with answers.',
         'Read the question to decide what the remainder means.', 'Round up when everyone needs a place, drop the remainder when only full groups count, or give the remainder when asked what is left.',
         body, faq, sets, seo_title='Grade 4 Multiplication and Division Word Problems: Remainders (TEKS 4.4H, STAAR)')


if __name__ == "__main__":
    build()
