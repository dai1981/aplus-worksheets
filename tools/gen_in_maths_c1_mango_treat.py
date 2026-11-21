# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 3: Mango Treat (Numbers 1 to 9)
Counting objects to 9, dot patterns and frames, numerals and number names, before and after (AU Foundation set makers)."""
from in_prim import unit, mod, rn, le, co, mcq


def one_order(r):
    kind = r.choice(["after", "before", "between", "big", "small"])
    a = r.randint(1, 8)
    if kind == "after":
        return mcq("Which number comes just after <b>%d</b>?" % a, a + 1, [a - 1 if a > 1 else a + 2, a, a + 2], "Count on: %d, <b>%d</b>." % (a, a + 1))
    if kind == "before":
        a += 1
        return mcq("Which number comes just before <b>%d</b>?" % a, a - 1, [a + 1, a, a - 2 if a > 2 else a + 2], "Count back: %d, <b>%d</b>." % (a, a - 1))
    if kind == "between":
        a = r.randint(1, 7)
        return mcq("Which number comes between <b>%d</b> and <b>%d</b>?" % (a, a + 2), a + 1, [a, a + 2, a + 3], "%d, <b>%d</b>, %d." % (a, a + 1, a + 2))
    x, y = r.sample(range(1, 10), 2)
    big = max(x, y) if kind == "big" else min(x, y)
    return mcq("Which is %s: <b>%d</b> or <b>%d</b>?" % ("more" if kind == "big" else "less", x, y), str(big), [str(min(x, y) if kind == "big" else max(x, y)), "They are the same", str(x + y)],
               "%d comes %s %d when we count, so <b>%d</b>." % (big, "after" if kind == "big" else "before", min(x, y) if kind == "big" else max(x, y), big))

su = mod("gen_au_maths_f_subitising", 601031)
nu = mod("gen_au_maths_f_numbers_to_20", 601032)
unit(1, "mango-treat", 3, "N", 3, "Mango Treat", "Numbers 1 to 9", "numbers 1 to 9",
     "Numbers 1 to 9: counting objects, matching numerals and quantities, reading and writing numerals, comparing and ordering (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 Mango Treat worksheet (Joyful Mathematics Chapter 3): counting to 9, dot patterns, matching numbers to groups, before and after. 100 picture questions with answers.",
     "Touch each thing once as you count.", "The last number you say tells how many.",
     "<ul><li>Count by touching each object once: 1, 2, 3, ….</li><li>The last number you say is how many there are.</li><li>Dice and frame patterns help you see small numbers quickly.</li></ul>",
     [("How many mangoes: 🥭 drawn 6 times?", ["Count 1 to 6"], "6")],
     [["Counting one object twice", "Move or tick each object as you count it."], ["Writing 6 and 9 the wrong way round", "6 has its circle at the bottom; 9 at the top."]],
     [("How far should a Class 1 child count in this chapter?", "Up to 9, with pictures and real objects."), ("What is subitising?", "Seeing how many there are without counting, like the dots on a dice.")],
     [("Dice patterns", [rn(su, "set_dice", 20)]),
      ("Frames", [rn(su, "set_frames", 16), rn(su, "set_find", 4)]),
      ("Groups", [rn(su, "set_groups", 12), rn(su, "set_parts", 8)]),
      ("Count the objects", [rn(nu, "set_count", 10, keep=le(9)), co(one_order, 10)]),
      ("Before, after and more", [co(one_order, 20)])], 60103)
