# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Change in Quantity to 10 (BC Mathematics Curriculum, Kindergarten Content: Change in
quantity to 10, using concrete materials — generalizing change by adding 1 or 2)
  python3 tools/gen_cabc_math_k_change_in_quantity_to_10.py
Adding 1 or 2 more, taking 1 or 2 away, hops on a number line, what changed (more or less, and by how much),
and change stories.
Wrong answers come from real mistakes: counting all again and starting at 1 instead of counting on, counting
back one too many, mixing up 1 more and 1 less, and saying the start number.
"""
import random
from k_pics import row_svg, crossed_row_svg, hop_line_svg, two_groups_svg, name, KINDS
from bck_common import Kids, mcq, finish, make, fig, figure, lesson, collect, S

R = random.Random(52501)
W = {1: "1 more", 2: "2 more", -1: "1 less", -2: "2 less"}


def near(n, lo=0, hi=10):
    return [x for x in [n + 1, n - 1, n + 2, n - 2, n + 3] if lo <= x <= hi and x != n]


# ------------------------------------------------------------ set 1: 1 or 2 more
def one_more(r):
    d = r.choice([1, 2])
    n = r.randint(1, 10 - d)
    k = r.choice(KINDS)
    q = fig(two_groups_svg(n, k, d, k, "+")) + "There are %d %s. %d more %s. How many now?" % (n, name(k, n), d, "comes" if d == 1 else "come")
    return mcq(q, n + d, [n, n + d + 1, n + 3 - d, n - 1], "Start at %d and count on %d: %s. There are <b>%d</b>." % (n, d, ", ".join(str(x) for x in range(n + 1, n + d + 1)), n + d))


# ------------------------------------------------------------ set 2: 1 or 2 less
def one_less(r):
    d = r.choice([1, 2])
    n = r.randint(d + 1, 10)
    k = r.choice(KINDS)
    q = fig(crossed_row_svg(n, k, d)) + "There are %d %s. %d %s taken away. How many are left?" % (n, name(k, n), d, "is" if d == 1 else "are")
    return mcq(q, n - d, [n, n - d - 1, n + d if n + d <= 10 else n - d + 1], "Count back %d from %d: %s. <b>%d</b> %s left." % (d, n, ", ".join(str(x) for x in range(n - 1, n - d - 1, -1)), n - d, "is" if n - d == 1 else "are"), allow_zero=True)


# ------------------------------------------------------------ set 3: hops on a number line
def one_hop(r):
    d = r.choice([1, 2, -1, -2])
    s = r.randint(max(0, -d), min(10, 10 - d))
    q = fig(hop_line_svg(s, d)) + "Start at the red dot (%d). Make %d hop%s %s. Where do you land?" % (s, abs(d), "" if abs(d) == 1 else "s", "forward" if d > 0 else "back")
    return mcq(q, s + d, [s, s - d, s + d + (1 if d > 0 else -1)] + near(s + d), "From %d, %d hop%s %s lands on <b>%d</b>." % (s, abs(d), "" if abs(d) == 1 else "s", "forward" if d > 0 else "back", s + d), allow_zero=True)


# ------------------------------------------------------------ set 4: what changed?
def one_what(r):
    d = r.choice([1, 2, -1, -2])
    a = r.randint(max(1, 1 - d), min(10, 10 - d))
    b = a + d
    k = r.choice(KINDS)
    kind = r.choice(["word", "word", "num"])
    pic = fig(two_groups_svg(a, k, b, k, "→"))
    if kind == "word":
        q = pic + "First there %s %d %s. Now there %s %d. What changed?" % ("was" if a == 1 else "were", a, name(k, a), "is" if b == 1 else "are", b)
        right = W[d]
        wr = [W[-d]] + [W[x] for x in (1, 2, -1, -2) if x not in (d, -d)]
        r.shuffle(wr)
        return mcq(q, right, wr, "%d to %d is <b>%s</b>." % (a, b, right))
    q = pic + "First there %s %d. Now there %s %d. Is that more or less, and by how many?" % ("was" if a == 1 else "were", a, "is" if b == 1 else "are", b)
    right = W[d]
    wr = [W[-d], "No change"] + [W[x] for x in (1, 2, -1, -2) if x != d and x != -d]
    return mcq(q, right, wr, "%d to %d is <b>%s</b>." % (a, b, right))


# ------------------------------------------------------------ set 5: change stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    d = r.choice([1, 2, -1, -2])
    n = r.randint(max(1, -d + 1), min(10, 10 - d))
    stories = {
        1: ["%s has %d crayons. %s friend gives %s 1 more. How many crayons now?",
            "There are %d canoes on the lake. 1 more canoe comes. How many canoes now?"],
        2: ["%s has %d stickers. %s gets 2 more. How many stickers now?",
            "There are %d ducks in the pond. 2 more ducks swim over. How many ducks now?"],
        -1: ["%s has %d crackers. %s eats 1. How many are left?",
             "There are %d kayaks on the beach. 1 kayak goes into the water. How many are left on the beach?"],
        -2: ["%s has %d balloons. 2 float away. How many are left?",
             "There are %d eagles in a tree. 2 fly away. How many are left?"],
    }
    t = r.choice(stories[d])
    if t.count("%s") == 3:
        q = t % (k["n"], n, k["His"], "her" if k["he"] == "she" else "him")
    elif t.count("%s") == 2:
        q = t % (k["n"], n, k["He"])
    elif t.count("%s") == 1:
        q = t % (k["n"], n)
    else:
        q = t % n
    return mcq(q, n + d, [n, n - d, n + d + (1 if d > 0 else -1)] + near(n + d),
               "%s %d: <b>%d</b>." % ("Count on %d from" % d if d > 0 else "Count back %d from" % -d, n, n + d), allow_zero=True)


def build():
    sets = [S("1 or 2 more", collect(one_more, 20, R)),
            S("1 or 2 less", collect(one_less, 20, R)),
            S("Hops on a number line", collect(one_hop, 20, R)),
            S("What changed?", collect(one_what, 20, R)),
            S("Change stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li><b>1 more</b>: count on one. 6 and 1 more is 7.</li>"
        "<li><b>2 more</b>: count on two. 6, then 7, 8.</li>"
        "<li><b>1 less</b> or <b>2 less</b>: count back. 6, then 5, 4.</li>"
        "<li>Start at the number you have. You do not need to count everything again.</li></ul>",
        [figure(two_groups_svg(5, "apple", 2, "apple", "+"), "5 and 2 more: 6, 7. There are 7."),
         figure(crossed_row_svg(8, "star", 1), "8 take away 1 is 7.")],
        [["Counting all over again from 1", "Start at the number you have and count on."],
         ["Counting back one too many", "Say the first number to yourself, then count back: 7 … 6, 5."],
         ["Mixing up more and less", "More means the group gets bigger. Less means it gets smaller."]])
    faq = [("What does change in quantity mean in Kindergarten?", "Seeing what happens to a group when some are added or taken away, especially 1 or 2 more and 1 or 2 less, using real objects."),
           ("Why focus on adding 1 or 2?", "Children notice the pattern: 1 more is the next number when counting, and 2 more is two numbers on. This builds early addition."),
           ("How can I practise at home?", "Put out a few toys, add or take away 1 or 2, and ask how many there are now and what changed."),
           ("What is counting on?", "Starting at the number you already have and counting forward, instead of counting everything from 1.")]
    make("change-in-quantity-to-10", 5, "Patterning", "Change in Quantity to 10: 1 or 2 More and Less", "Change in quantity to 10",
         "Change in quantity to 10, using concrete materials: generalizing change by adding 1 or 2; modeling and describing number relationships through change",
         "Free Kindergarten math worksheets on change in quantity to 10 for the BC curriculum: 1 or 2 more, 1 or 2 less, hops on a number line, what changed, and stories. 100 picture questions with answers.",
         "1 more is the next number; 1 less is the number before.", "Start at the number you have and count on or back 1 or 2.",
         body, faq, sets)


if __name__ == "__main__":
    build()
