# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Part-Part-Whole to 10 (Australian Curriculum v9.0, AC9MFN04)
  python3 tools/gen_au_maths_f_part_part_whole.py
Two parts make a whole, finding the hidden part, number bonds, the ways to make 5 and 10 on a ten-frame,
and part-part-whole stories.
Wrong answers come from real mistakes: giving the whole when a part is asked, giving the part you can see,
adding when a part is missing, and an off-by-one count.
"""
import random
from k_pics import two_groups_svg, box_svg, bond_svg, tenframe_mix_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99401)


# ------------------------------------------------------------ set 1: put the parts together
def set_join(rnd):
    its = []
    plan = [(2, 1), (3, 2), (1, 4), (4, 2), (5, 3), (2, 6), (3, 4), (6, 1), (4, 4), (5, 5),
            (7, 2), (3, 5), (1, 8), (6, 3), (2, 7), (4, 5), (8, 2), (3, 6), (7, 3), (5, 4)]
    for i, (a, b) in enumerate(plan):
        ka, kb = KINDS[i % len(KINDS)], KINDS[(i + 3) % len(KINDS)]
        same = i % 3 != 2
        if same:
            kb = ka
            q = fig(two_groups_svg(a, ka, b, kb, "and")) + "One part has %d. The other part has %d. How many %s in the whole group?" % (a, b, name(ka))
        else:
            q = fig(two_groups_svg(a, ka, b, kb, "and")) + "How many things altogether?"
        t = a + b
        its.append(mcq(q, t, [a, b, t + 1, t - 1, t + 2], "Part %d and part %d make the whole: <b>%d</b>." % (a, b, t)))
    return {"title": "Parts make the whole", "items": its}


# ------------------------------------------------------------ set 2: the hidden part
def set_hidden(rnd):
    K = Kids(rnd)
    its = []
    plan = [(5, 3), (4, 1), (6, 2), (7, 4), (5, 1), (8, 5), (6, 4), (9, 6), (7, 2), (10, 7),
            (8, 3), (9, 4), (10, 5), (6, 5), (4, 2), (10, 3), (7, 6), (9, 2), (8, 7), (10, 8)]
    for i, (w, seen) in enumerate(plan):
        k = KINDS[i % len(KINDS)]
        kid = K.next()
        h = w - seen
        q = fig(box_svg(seen, k)) + "%s has %d %s. Some are hidden in the box. How many are in the box?" % (kid["n"], w, name(k))
        its.append(mcq(q, h, [w, seen, w + seen, h + 1, h - 1], "The whole is %d. You can see %d. %d and <b>%d</b> make %d." % (w, seen, seen, h, w)))
    return {"title": "Find the hidden part", "items": its}


# ------------------------------------------------------------ set 3: number bonds
def set_bonds(rnd):
    its = []
    plan = [(5, 2, 3, "w"), (6, 4, 2, "b"), (7, 3, 4, "a"), (8, 5, 3, "w"), (4, 1, 3, "b"), (9, 6, 3, "a"), (10, 4, 6, "w"),
            (6, 1, 5, "b"), (8, 2, 6, "a"), (10, 7, 3, "b"), (3, 2, 1, "a"), (9, 4, 5, "w"), (7, 5, 2, "b"), (10, 2, 8, "a"),
            (5, 0, 5, "b"), (8, 4, 4, "w"), (6, 3, 3, "a"), (9, 1, 8, "b"), (10, 5, 5, "a"), (7, 7, 0, "b")]
    for w, a, b, hide in plan:
        vals = {"w": ("?", a, b), "a": (w, "?", b), "b": (w, a, "?")}[hide]
        ans = {"w": w, "a": a, "b": b}[hide]
        q = fig(bond_svg(*vals)) + ("What is the whole?" if hide == "w" else "What is the missing part?")
        if hide == "w":
            e = "The parts are %d and %d. Together they make <b>%d</b>." % (a, b, w)
            wr = [a, b, w + 1, w - 1]
        else:
            known = b if hide == "a" else a
            e = "The whole is %d and one part is %d. %d and <b>%d</b> make %d." % (w, known, known, ans, w)
            wr = [w, known, w + known, ans + 1, ans + 2]
        its.append(mcq(q, ans, wr, e, allow_zero=True))
    return {"title": "Number bonds", "items": its}


# ------------------------------------------------------------ set 4: ways to make 5 and 10
def set_ways(rnd):
    its = []
    for i, (r_, total) in enumerate([(3, 5), (1, 5), (4, 5), (2, 5), (6, 10), (3, 10), (8, 10), (5, 10), (7, 10), (1, 10)]):
        b = total - r_
        cells = ["r"] * r_ + ["b"] * b + [""] * (10 - total)
        q = fig(tenframe_mix_svg(cells)) + "How many red dots and how many blue dots?"
        ans = "%d red and %d blue" % (r_, b)
        wr = ["%d red and %d blue" % (b, r_), "%d red and %d blue" % (r_, b + 1), "%d red and %d blue" % (r_ + 1, b)]
        if r_ == b:
            wr = ["%d red and %d blue" % (r_ + 1, b - 1), "%d red and %d blue" % (r_, b + 1), "%d red and %d blue" % (r_ - 1, b + 1)]
        its.append(mcq(q, ans, wr, "Count each colour: %d red and %d blue. Together they make %d. <b>%s</b>." % (r_, b, total, ans)))
    for i, total in enumerate([5, 10, 5, 10, 10, 5, 10, 10, 5, 10]):
        a = [2, 6, 4, 3, 9, 1, 5, 7, 0, 2][i]
        b = total - a
        q = "Which two numbers make <b>%d</b>?" % total
        ans = "%d and %d" % (a, b)
        wr = ["%d and %d" % (a, b + 1), "%d and %d" % (a + 2, b + 1), "%d and %d" % (a, a) if a + a != total else "%d and %d" % (a + 1, a)]
        if b - 1 >= 0:
            wr.append("%d and %d" % (a, b - 1))
        its.append(mcq(q, ans, wr, "%d and %d make %d. <b>%s</b>." % (a, b, total, ans), allow_zero=True))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Ways to make 5 and 10", "items": order}


# ------------------------------------------------------------ set 5: part-part-whole stories
def set_story(rnd):
    K = Kids(rnd)
    its = []
    stories = [
        ("{n} has {w} balloons. {a} are red and the rest are blue. How many are blue?", 8, 3, "part"),
        ("{n} sees {a} birds in a tree and {b} birds on the grass. How many birds does {he} see?", None, (4, 3), "whole"),
        ("There are {w} children in the group. {a} are girls. How many are boys?", 9, 5, "part"),
        ("{n} has {a} red pencils and {b} green pencils. How many pencils does {he} have?", None, (2, 6), "whole"),
        ("{n} has {w} grapes. {a} are green and the rest are purple. How many are purple?", 7, 4, "part"),
        ("A plate has {a} sandwiches and {b} pieces of fruit. How many things are on the plate?", None, (5, 5), "whole"),
        ("{n} has {w} toy cars. {a} are in the box. The rest are on the mat. How many are on the mat?", 10, 6, "part"),
        ("{n} puts {a} shells in one bucket and {b} shells in another. How many shells are there?", None, (3, 4), "whole"),
        ("There are {w} ducks. {a} are in the pond. How many are out of the pond?", 6, 2, "part"),
        ("{n} has {a} big blocks and {b} small blocks. How many blocks is that?", None, (6, 2), "whole"),
        ("{n} has {w} socks. {a} are spotty and the rest are striped. How many are striped?", 8, 5, "part"),
        ("{n} counts {a} cats and {b} dogs at the park. How many animals is that?", None, (1, 7), "whole"),
        ("A bus has {w} people. {a} are sitting. The rest are standing. How many are standing?", 10, 9, "part"),
        ("{n} picks {a} flowers and then {b} more flowers. How many flowers does {he} have?", None, (4, 4), "whole"),
        ("There are {w} apples. {a} are in the bowl and the rest are in the bag. How many are in the bag?", 5, 1, "part"),
        ("{n} has {a} stickers on one page and {b} on the next page. How many stickers is that?", None, (7, 3), "whole"),
        ("There are {w} frogs. {a} are on a log. The rest are in the water. How many are in the water?", 9, 3, "part"),
        ("{n} has {a} yellow beads and {b} white beads. How many beads altogether?", None, (2, 8), "whole"),
        ("{n} has {w} biscuits. {a} are chocolate. How many are not chocolate?", 7, 7, "part"),
        ("There are {a} kangaroos near the tree and {b} kangaroos on the hill. How many kangaroos?", None, (5, 3), "whole"),
    ]
    for t, w, x, kind in stories:
        k = K.next()
        if kind == "part":
            a = x
            ans = w - a
            q = t.format(n=k["n"], he=k["he"], w=w, a=a)
            e = "The whole is %d. One part is %d. %d and <b>%d</b> make %d." % (w, a, a, ans, w)
            wr = [w, a, w + a, ans + 1, ans + 2]
        else:
            a, b = x
            ans = a + b
            q = t.format(n=k["n"], he=k["he"], a=a, b=b)
            e = "The parts are %d and %d. The whole is <b>%d</b>." % (a, b, ans)
            wr = [a, b, ans + 1, ans - 1]
        its.append(mcq(q, ans, wr, e, allow_zero=True))
    return {"title": "Part-part-whole stories", "items": its}


def body():
    return (
        "<h2>Two parts make a whole</h2>"
        "<p>A group can be split into two <b>parts</b>. Put the parts together to get the <b>whole</b>.</p>"
        + figure(two_groups_svg(4, "apple", 3, "apple", "and"), "Part 4 and part 3 make the whole: 7.")
        + "<h2>Number bonds</h2><p>A number bond shows the whole on top and the two parts below. If one part is missing, think: what goes with this part to make the whole?</p>"
        + figure(bond_svg(7, 4, "?"), "4 and 3 make 7, so the missing part is 3.")
        + "<h2>Ways to make 10</h2><p>A ten-frame shows two parts of 10: 6 red and 4 blue. Other ways: 9 and 1, 8 and 2, 7 and 3, 5 and 5.</p>"
        + figure(tenframe_mix_svg(["r"] * 6 + ["b"] * 4), "6 and 4 make 10.")
        + mistakes([["Giving the whole when a part is missing", "Find what goes with the part you know"],
                    ["Giving the part you can see", "Some are hidden: count on to the whole"],
                    ["Adding the whole and the part", "The parts are always smaller than the whole"]]))


FAQ = [("What is part-part-whole?",
        "It is the idea that a whole group can be split into two parts, and the parts join back to make the whole. Foundation students partition and combine collections up to 10 (AC9MFN04)."),
       ("What is a number bond?",
        "A diagram with the whole at the top and two parts underneath, such as 7 split into 4 and 3. It shows how numbers are made of other numbers."),
       ("Why practise the ways to make 10?",
        "Knowing pairs like 6 and 4 or 7 and 3 helps children add and subtract quickly in Year 1 and Year 2."),
       ("How can I practise at home?",
        "Hide some of 10 pegs under a cup and ask how many are hidden. Split a handful of grapes into two plates and say the parts and the whole.")]


def build():
    sets = [set_join(R), set_hidden(R), set_bonds(R), set_ways(R), set_story(R)]
    finish(sets, R, max_num=20)
    make("part-part-whole-to-10", 4, "AC9MFN04", "Number",
         "Part-Part-Whole: Splitting and Joining to 10",
         "Foundation Part-Part-Whole Worksheets: Number Bonds and Ways to Make 10 (Free, with Answers)",
         "Part-part-whole",
         "Partition and combine collections up to 10 using part-part-whole relationships and subitising to recognise and name the parts.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on part-part-whole to 10, matched to the Australian Curriculum (AC9MFN04): parts make the whole, hidden parts, number bonds and ways to make 5 and 10. 100 picture questions with answers.",
         "Two parts make the whole. The parts are smaller than the whole.",
         "Number bonds show the whole and its parts. 6 and 4, 7 and 3, 5 and 5 all make 10.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
