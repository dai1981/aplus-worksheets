# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Comparing Length, Mass and Capacity (BC Mathematics Curriculum, Kindergarten Content: Direct
comparative measurement — linear, mass, capacity)
  python3 tools/gen_cabc_math_k_comparing_length_mass_and_capacity.py
Longer and shorter, taller and shorter, heavier and lighter on a pan balance, holds more and holds less, and
using a baseline (lining things up at one end) to compare fairly. Sets 1 to 4 reuse the AU Foundation makers
with Canadian names and spelling.
Wrong answers come from real mistakes: comparing the far ends without lining up the start, thinking a bigger
object is always heavier, and thinking a taller container always holds more.
"""
import random
from k_pics import pencils_svg
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_au_maths_f_comparing_length_mass_capacity as au

R = random.Random(52801)
au.Kids = Kids
POS = Cycle()


# ------------------------------------------------------------ set 5: use a baseline
def one_base(r):
    K = Kids(r)
    k = K.next()
    kind = r.choice(["trick", "trick", "lined", "why"])
    if kind == "trick":
        a = r.randint(4, 8)
        b = a - r.randint(1, 3)
        off = a - b + r.randint(1, 2)
        pic = pencils_svg([a, b], offsets=[0, off])
        q = fig(pic) + "Pencil B sticks out further on the right. %s says B is longer. Is %s right?" % (k["n"], k["he"])
        right = "No. Line them up at the start: A is longer"
        return mcq(q, right, ["Yes. B sticks out further, so B is longer", "Yes. They are the same length", "We can never tell"],
                   "The pencils do not start at the same place. Slide B back to the start line and A is longer: <b>%s</b>." % right)
    if kind == "lined":
        n = r.choice([3, 4])
        ls = r.sample(range(3, 10), n)
        pic = pencils_svg(ls)
        word = r.choice(["longest", "shortest"])
        t = max(ls) if word == "longest" else min(ls)
        L = "ABCD"[ls.index(t)]
        cands = [l for l in "ABCD"[:n] if l != L] + (["They are all the same"] if n == 3 else [])
        it = mcq(fig(pic) + "The pencils are lined up at the start. Which pencil is the <b>%s</b>?" % word, L, cands,
                 "They all start at the same line, so look at the other ends. Pencil <b>%s</b> is the %s." % (L, word))
        return letters(it, L, list("ABCD") if n == 4 else ["A", "B", "C", "They are all the same"])
    facts = [("Why do we line things up at one end before comparing length?", "So we can see which one goes further", ["So they look neat", "So they become the same length", "So we do not need to look"]),
             ("Two snakes made of string are curled up. How can we tell which is longer?", "Stretch them out straight and line up the ends", ["The bigger curl is always longer", "Weigh them on a balance", "Count the colours"]),
             ("Two friends compare their heights. What should they do?", "Stand back to back on the same floor", ["One stands on a chair", "Stand far apart", "Compare their shoes"]),
             ("You want to know which book is wider. What do you do?", "Put them side by side with one edge lined up", ["Stack them in any way", "Smell them", "Count the pages"]),
             ("Which word compares mass?", "Heavier", ["Taller", "Longer", "Wider"]),
             ("Which word compares capacity?", "Holds more", ["Heavier", "Longer", "Taller"]),
             ("Which word compares length?", "Longer", ["Heavier", "Holds more", "Lighter"])]
    q, right, wr = r.choice(facts)
    return mcq(q, right, wr, "<b>%s</b>." % right)


def take(fn, n, r):
    return fn(r)["items"][:n]


def build():
    sets = [S("Longer and shorter", take(au.set_length, 20, R)),
            S("Taller and shorter", take(au.set_height, 20, R)),
            S("Heavier and lighter", take(au.set_mass, 20, R)),
            S("Holds more, holds less", take(au.set_capacity, 20, R)),
            S("Use a baseline", collect(one_base, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li><b>Length</b>: line things up at one end (a <b>baseline</b>), then see which goes further: longer, shorter, taller, wider.</li>"
        "<li><b>Mass</b>: on a pan balance, the <b>heavier</b> side goes down. A big thing is not always heavier.</li>"
        "<li><b>Capacity</b>: pour from one container into another to see which <b>holds more</b>.</li></ul>",
        [figure(pencils_svg([6, 4]), "Lined up at the start: A is longer than B."),
         figure(pencils_svg([6, 4], offsets=[0, 4]), "Not lined up: B looks longer, but it is not.")],
        [["Comparing without a baseline", "Line up one end first, then compare the other end."],
         ["Thinking bigger means heavier", "Use a balance. A big beach ball is lighter than a small rock."],
         ["Thinking taller always holds more", "Pour water from one into the other to check."]])
    faq = [("What is direct comparison in measurement?", "Comparing two things by putting them next to each other, without numbers: longer or shorter, heavier or lighter, holds more or holds less."),
           ("Why is a baseline important?", "Lining things up at one end makes the comparison fair. Otherwise a shorter thing can look longer."),
           ("How do children compare mass?", "By holding one in each hand or using a pan balance. The heavier side goes down."),
           ("How do children compare capacity?", "By filling one container and pouring into another. If it overflows, the first holds more.")]
    make("comparing-length-mass-and-capacity", 8, "Geometry and measurement", "Comparing Length, Mass and Capacity", "Comparing length, mass and capacity",
         "Direct comparative measurement (e.g., linear, mass, capacity): using a baseline for direct comparison in linear measurement; height, width, length; heavier than, lighter than, same as; holds more, holds less",
         "Free Kindergarten math worksheets on comparing length, mass and capacity for the BC curriculum: longer and shorter, taller, heavier and lighter on a balance, holds more and less, and using a baseline. 100 picture questions with answers.",
         "Line things up at one end before you compare length.", "The heavier side of a balance goes down. Pour to see which container holds more.",
         body, faq, sets)


if __name__ == "__main__":
    build()
