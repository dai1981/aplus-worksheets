# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 8: Fun with Numbers (Numbers 21 to 99)
Tens and ones, reading and writing numbers to 99, comparing, ordering, number before and after, 10 more and 10 less."""
from in_prim import unit, mod, rn, le, co, mcq


def one_ba(r):
    kind = r.choice(["after", "before", "between", "order"])
    a = r.randint(21, 98)
    if kind == "after":
        return mcq("Which number comes just after <b>%d</b>?" % a, a + 1, [a - 1, a + 10 if a + 10 < 100 else a - 10, a + 2], "Count on one: <b>%d</b>." % (a + 1))
    if kind == "before":
        return mcq("Which number comes just before <b>%d</b>?" % a, a - 1, [a + 1, a - 10, a - 2], "Count back one: <b>%d</b>." % (a - 1))
    if kind == "between":
        a = r.randint(21, 96)
        return mcq("Which number comes between <b>%d</b> and <b>%d</b>?" % (a, a + 2), a + 1, [a + 3, a - 1, a + 11 if a + 11 < 100 else a - 9], "%d, <b>%d</b>, %d." % (a, a + 1, a + 2))
    xs = r.sample(range(21, 100), 3)
    s = sorted(xs)
    show = lambda v: ", ".join(map(str, v))
    return mcq("Put in order from smallest to biggest: %s" % show(xs), show(s), [show(s[::-1]), show([s[1], s[0], s[2]]), show([s[0], s[2], s[1]])],
               "Compare the tens first: <b>%s</b>." % show(s))

pv = mod("gen_us_math_g1_place_value", 601081)
to = mod("gen_au_maths_y1_tens_ones", 601082)
cp = mod("gen_us_math_g1_compare", 601083)
tm = mod("gen_us_math_g1_ten_more_less", 601084)
unit(1, "fun-with-numbers", 8, "N", 8, "Fun with Numbers", "Numbers 21 to 99", "numbers 21 to 99",
     "Numbers 21 to 99: grouping in tens and ones, reading and writing numerals and number names, comparing and ordering, number before and after (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Fun with Numbers worksheet (Joyful Mathematics Chapter 8): tens and ones, numbers to 99, comparing, before and after, 10 more and 10 less. 100 questions with answers.",
     "47 is 4 tens and 7 ones.", "Compare the tens first, then the ones.",
     "<ul><li>Group objects in <b>tens</b>: 4 tens and 7 ones make 47.</li><li>To compare, look at the tens: 52 &gt; 48 because 5 tens is more than 4 tens.</li><li>10 more changes the tens digit: 36 → 46.</li></ul>",
     [("What is 6 tens and 3 ones?", ["60 + 3"], "63"), ("Which is bigger: 39 or 41?", ["4 tens is more than 3 tens"], "41")],
     [["Writing 6 tens 3 ones as 36", "Tens come first: 63."], ["Comparing ones first", "Compare the tens digit first."]],
     [("What is place value?", "The value of a digit depends on its place: in 74, the 7 means 7 tens."), ("Up to which number do Class 1 children count?", "Up to 99 in this chapter.")],
     [("Tens and ones", [rn(pv, "set_blocks", 10, keep=le(99)), rn(to, "set_count", 10, keep=le(99))]),
      ("Reading digits", [rn(pv, "set_digits", 10, keep=le(99)), rn(to, "set_partition", 10, keep=le(99))]),
      ("Compare", [rn(cp, "set_symbols", 12, keep=le(99)), rn(cp, "set_blocks", 8, keep=le(99))]),
      ("Before, after and between", [co(one_ba, 20)]),
      ("10 more and 10 less", [rn(tm, "set_more_blocks", 10, keep=le(99)), rn(tm, "set_less_blocks", 10, keep=le(99))])], 60108)
