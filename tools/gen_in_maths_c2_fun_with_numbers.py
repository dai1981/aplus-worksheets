# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 3: Fun with Numbers (Numbers 1 to 100)
Tens and ones, partitioning, number names, comparing and number problems up to 100 (UK Year 2 and US Grade 2 set makers)."""
from in_prim import unit, mod, rn, le, co, mcq, words


def one_cmp(r):
    a, b = r.sample(range(10, 101), 2)
    if r.random() < 0.3:
        b = int(str(a)[::-1]) if a % 10 and a < 100 and a % 11 else b
    if a == b:
        return None
    s = "&gt;" if a > b else "&lt;"
    return mcq("Which sign goes in the box? <b>%d ☐ %d</b>" % (a, b), s, ["&lt;" if s == "&gt;" else "&gt;", "=", "+"],
               "%d is %s than %d, so <b>%s</b>." % (a, "greater" if a > b else "less", b, s))


def one_words(r):
    n = r.randint(11, 99)
    if r.random() < 0.5:
        w = words(n)
        return mcq("Write <b>%s</b> in numbers." % w, n, [int(str(n)[::-1]) if n % 10 and n % 11 else n + 10, n + 1, n - 10 if n > 20 else n + 20], "%s = <b>%d</b>." % (w.capitalize(), n))
    al = [n, int(str(n)[::-1]) if n % 10 and n % 11 else n + 10, n + 1, n - 10 if n > 20 else n + 20]
    return mcq("How do we write <b>%d</b> in words?" % n, words(n), [words(x) for x in al[1:]], "<b>%s</b>." % words(n).capitalize())

pv = mod("gen_uk_maths_y2_place_value", 602031)
ub = mod("gen_us_math_g2_place_value", 602033)
cp = mod("gen_us_math_g2_compare", 602032)
unit(2, "fun-with-numbers", 3, "N", 3, "Fun with Numbers", "Numbers 1 to 100", "numbers to 100",
     "Numbers up to 100: place value (tens and ones), reading and writing numerals and number names, comparing and ordering (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Fun with Numbers worksheet (Joyful Mathematics Chapter 3): tens and ones, number names, comparing and ordering numbers to 100. 100 questions with answers.",
     "68 is 6 tens and 8 ones.", "To compare, look at the tens first.",
     "<ul><li>68 = 6 tens and 8 ones = 60 + 8.</li><li>Number names: 68 is <b>sixty-eight</b>.</li><li>To compare, look at the tens: 71 &gt; 69.</li></ul>",
     [("Write 4 tens and 9 ones.", ["40 + 9"], "49"), ("Which is bigger: 58 or 85?", ["8 tens > 5 tens"], "85")],
     [["Swapping the digits (49 written as 94)", "Tens come first."], ["Reading 70 as seventeen", "Seventy is 7 tens; seventeen is 1 ten and 7 ones."]],
     [("What is a two-digit number?", "A number from 10 to 99 with a tens digit and a ones digit."), ("How are numbers named?", "The tens word and the ones word: forty-three.")],
     [("Tens and ones", [rn(ub, "set_blocks", 14, keep=le(100)), rn(pv, "set_tens_ones", 6)]),
      ("Partitioning", [rn(pv, "set_partition", 12), co(one_words, 8)]),
      ("Number names", [co(one_words, 18), rn(pv, "set_words", 2)]),
      ("Compare", [rn(pv, "set_compare", 10), co(one_cmp, 10)]),
      ("Number problems", [rn(pv, "set_problems", 10), rn(ub, "set_blocks", 10, keep=le(100))])], 60203, max_num=100)
