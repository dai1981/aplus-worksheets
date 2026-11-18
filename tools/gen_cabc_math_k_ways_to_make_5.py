# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Ways to Make 5 (BC Mathematics Curriculum, Kindergarten Content: Ways to make 5)
  python3 tools/gen_cabc_math_k_ways_to_make_5.py
Seeing small amounts at a glance (perceptual subitizing: I see 5), seeing parts (conceptual subitizing: I see
4 and 1), five frames with two colours, number bonds for 5, and pairs that make 5 in stories.
Wrong answers come from real mistakes: counting one dot twice, giving one part instead of the whole, and
choosing a pair that makes 4 or 6.
"""
import random
from k_pics import dice_svg, two_groups_svg, tenframe_mix_svg, bond_svg, row_svg, name, KINDS
from bck_common import Kids, mcq, finish, make, fig, figure, lesson, collect, S

R = random.Random(52201)
PAIRS = [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]


def near(n, lo=0, hi=10):
    return [x for x in [n + 1, n - 1, n + 2, n - 2, n + 3] if lo <= x <= hi and x != n]


def frame5(a, b, blue_first=False):
    """a red and b blue dots in the top row of a ten frame (5 boxes)."""
    cells = (["b"] * b + ["r"] * a if blue_first else ["r"] * a + ["b"] * b) + [""] * (5 - a - b) + [""] * 5
    return tenframe_mix_svg(cells)


# ------------------------------------------------------------ set 1: I see it at a glance
def one_glance(r):
    v = r.randint(1, 6)
    kind = r.choice(["one", "one", "two", "frame"])
    if kind == "frame":
        from k_pics import tenframe_svg
        return mcq(fig(tenframe_svg(v)) + "Look quickly at the ten frame. How many dots?", v, near(v, 1, 6), ("A full top row is 5, so there are <b>5</b>." if v == 5 else "5 and 1 more make <b>6</b>." if v == 6 else "You can see the dots at a glance: <b>%d</b>." % v))
    if kind == "one":
        return mcq(fig(dice_svg([v])) + "Look quickly. How many dots do you see?", v, near(v, 1, 6), "The dots make a pattern you can see at a glance: <b>%d</b>." % v)
    a, b = r.randint(1, 5), r.randint(1, 5)
    if a + b > 6:
        return None
    return mcq(fig(dice_svg([a, b])) + "How many dots on both cubes together?", a + b, [a, b, a + b + 1, a + b - 1], "I see %d and %d. Together they make <b>%d</b>." % (a, b, a + b))


# ------------------------------------------------------------ set 2: I see the parts
def one_parts(r):
    a, b = r.randint(1, 4), r.randint(1, 4)
    if a + b > 5:
        return None
    k1, k2 = r.sample(KINDS, 2)
    kind = r.choice(["all", "all", "part"])
    if kind == "all":
        return mcq(fig(two_groups_svg(a, k1, b, k2)) + "I see %d and %d. How many in all?" % (a, b), a + b, [a, b, a + b + 1], "%d and %d make <b>%d</b>." % (a, b, a + b))
    return mcq(fig(two_groups_svg(a, k1, b, k1)) + "There are %d %s in all. I see %d on one side. How many on the other side?" % (a + b, name(k1), a), b, [a + b, a, b + 1], "%d and <b>%d</b> make %d." % (a, b, a + b))


# ------------------------------------------------------------ set 3: five frames
def one_frame(r):
    a = r.randint(0, 5)
    b = 5 - a
    bf = r.random() < 0.5
    frame5_ = lambda x, y: frame5(x, y, bf)
    kind = r.choice(["blue", "red", "full", "more"])
    if kind == "blue":
        if b == 0:
            return None
        return mcq(fig(frame5_(a, b)) + "The top row is full: 5 dots. How many dots are <b>blue</b>?", b, near(b, 0, 5) + [5], "%d red and <b>%d</b> blue make 5." % (a, b), allow_zero=True)
    if kind == "red":
        if a == 0:
            return None
        return mcq(fig(frame5_(a, b)) + "The top row is full: 5 dots. How many dots are <b>red</b>?", a, near(a, 0, 5) + [5], "<b>%d</b> red and %d blue make 5." % (a, b), allow_zero=True)
    if kind == "full":
        return mcq(fig(frame5_(a, b)) + "How many dots are in the top row altogether?", 5, [a if a != 5 else 4, b if b != 5 else 6, 4, 6], "%d and %d make <b>5</b>. A full row is always 5." % (a, b), allow_zero=True)
    c = r.randint(1, 4)
    return mcq(fig(frame5(c, 0) if bf else frame5(0, c)) + "How many more dots fill the top row to make 5?", 5 - c, near(5 - c, 0, 5) + [c], "There are %d dots. %d and <b>%d</b> more make 5." % (c, c, 5 - c), allow_zero=True)


# ------------------------------------------------------------ set 4: number bonds for 5
def one_bond(r):
    a, b = r.choice(PAIRS)
    if r.random() < 0.5:
        return mcq(fig(bond_svg(5, a, "?")) + "What number is missing?", b, near(b, 0, 5) + [5], "%d and <b>%d</b> make 5." % (a, b), allow_zero=True)
    pair = r.choice(PAIRS)
    wrong = [(1, 3), (2, 2), (3, 3), (4, 2), (1, 5), (2, 4), (0, 4), (3, 1)]
    r.shuffle(wrong)
    right = "%d and %d" % pair
    return mcq("Which two numbers make <b>5</b>?", right, ["%d and %d" % w for w in wrong], "<b>%s</b> make 5." % right, allow_zero=True)


# ------------------------------------------------------------ set 5: stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    a = r.randint(1, 4)
    b = 5 - a
    kind = r.choice(["hands", "pond", "bus", "hidden"])
    if kind == "hands":
        return mcq("%s holds up 5 fingers on one hand. %s puts down %d. How many fingers are still up?" % (k["n"], k["He"], a),
                   b, near(b, 0, 5) + [5], "5 is %d and %d. %d down leaves <b>%d</b> up." % (a, b, a, b), allow_zero=True)
    if kind == "pond":
        q = fig(two_groups_svg(a, "duck", b, "duck")) + "There are 5 ducks. %d %s on the grass. The rest are in the pond. How many are in the pond?" % (a, "is" if a == 1 else "are")
        return mcq(q, b, near(b, 0, 5) + [5], "%d and <b>%d</b> make 5." % (a, b), allow_zero=True)
    if kind == "bus":
        return mcq("5 children ride the bus to school. %d %s at the front. The rest sit at the back. How many sit at the back?" % (a, "sits" if a == 1 else "sit"), b, near(b, 0, 5) + [5], "%d and <b>%d</b> make 5." % (a, b), allow_zero=True)
    kk = r.choice(KINDS)
    q = fig(row_svg(a, kk)) + "%s has 5 %s. You can see %d. The rest are in a bag. How many are in the bag?" % (k["n"], name(kk), a)
    return mcq(q, b, near(b, 0, 5) + [5], "%d and <b>%d</b> make 5." % (a, b), allow_zero=True)


def build():
    sets = [S("I see it at a glance", collect(one_glance, 20, R)),
            S("I see the parts", collect(one_parts, 20, R)),
            S("Five frames", collect(one_frame, 20, R)),
            S("Number bonds for 5", collect(one_bond, 20, R)),
            S("Ways to make 5 in stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>Small groups can be seen <b>at a glance</b> without counting: I see 5.</li>"
        "<li>You can also see the <b>parts</b>: I see 4 and 1, so there are 5.</li>"
        "<li>5 can be made in many ways: 0 and 5, 1 and 4, 2 and 3, 3 and 2, 4 and 1, 5 and 0.</li></ul>",
        [figure(frame5(3, 2), "3 red and 2 blue make 5."),
         figure(bond_svg(5, 4, 1), "4 and 1 make 5.")],
        [["Giving one part instead of the whole", "Ask: How many in all? Put both parts together."],
         ["Counting one dot twice", "Look for a pattern you know, like the 5 on a dot cube."],
         ["Thinking 2 and 2 make 5", "Count them: 1, 2, 3, 4. 2 and 3 make 5."]])
    faq = [("What is subitizing?", "Seeing how many are in a small group without counting. Perceptual subitizing is seeing 5 at once; conceptual subitizing is seeing parts, like 4 and 1, and knowing the total is 5."),
           ("What are the ways to make 5?", "0 and 5, 1 and 4, 2 and 3, 3 and 2, 4 and 1, and 5 and 0."),
           ("How can I practise ways to make 5 at home?", "Hold up 5 fingers and fold some down, or hide some of 5 small toys under a cup and ask how many are hidden."),
           ("Why learn ways to make 5 before 10?", "Five is a benchmark. Knowing its parts helps children see 6 as 5 and 1, and later make 10.")]
    make("ways-to-make-5", 2, "Number", "Ways to Make 5: Subitizing and Number Bonds", "Ways to make 5",
         "Ways to make 5: perceptual subitizing (e.g., I see 5), conceptual subitizing (e.g., I see 4 and 1), using concrete materials to show ways to make 5",
         "Free Kindergarten math worksheets on ways to make 5 for the BC curriculum: subitizing dot patterns, seeing parts, five frames, number bonds and stories. 100 picture questions with answers.",
         "5 can be made in many ways: 1 and 4, 2 and 3, 3 and 2, 4 and 1.", "Look for parts you know. I see 4 and 1, so I know there are 5.",
         body, faq, sets)


if __name__ == "__main__":
    build()
