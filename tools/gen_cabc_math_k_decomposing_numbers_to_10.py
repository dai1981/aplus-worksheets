# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Decomposing Numbers to 10 (BC Mathematics Curriculum, Kindergarten Content: Decomposition of
numbers to 10)
  python3 tools/gen_cabc_math_k_decomposing_numbers_to_10.py
Part-part-whole with number bonds, finding the hidden part, making 10 on a ten frame, the benchmarks 5 and 10,
and part-part-whole stories.
Wrong answers come from real mistakes: giving the whole instead of the missing part, adding the two numbers
shown instead of finding the part, counting the full boxes instead of the empty ones, and choosing a pair
that makes 9 or 11.
"""
import random
from k_pics import bond_svg, box_svg, tenframe_svg, two_groups_svg, row_svg, cards_svg, name, KINDS
from bck_common import Kids, mcq, finish, make, fig, figure, lesson, collect, S

R = random.Random(52401)


def near(n, lo=0, hi=10):
    return [x for x in [n + 1, n - 1, n + 2, n - 2, n + 3] if lo <= x <= hi and x != n]


# ------------------------------------------------------------ set 1: number bonds
def one_bond(r):
    w = r.randint(4, 10)
    a = r.randint(0, w)
    b = w - a
    kind = r.choice(["part", "part", "whole"])
    if kind == "whole":
        return mcq(fig(bond_svg("?", a, b)) + "What is the whole?", w, [a, b, w + 1 if w < 10 else w - 1] + near(w), "%d and %d make <b>%d</b>." % (a, b, w), allow_zero=True)
    return mcq(fig(bond_svg(w, a, "?")) + "What number is missing?", b, [w, a if a != b else b + 1] + near(b), "%d and <b>%d</b> make %d." % (a, b, w), allow_zero=True)


# ------------------------------------------------------------ set 2: the hidden part
def one_hidden(r):
    w = r.randint(3, 10)
    a = r.randint(1, w - 1)
    k = r.choice(KINDS)
    q = fig(box_svg(a, k)) + "There are %d %s in all. Some are hiding in the box. How many are in the box?" % (w, name(k))
    return mcq(q, w - a, [w, a, w + a] + near(w - a, 1), "You can see %d. %d and <b>%d</b> make %d." % (a, a, w - a, w))


# ------------------------------------------------------------ set 3: making 10
def one_ten(r):
    kind = r.choice(["frame", "frame", "pair", "fingers"])
    if kind == "frame":
        n = r.randint(1, 9)
        return mcq(fig(tenframe_svg(n)) + "How many more dots make <b>10</b>?", 10 - n, [n, 10] + near(10 - n, 1), "Count the empty boxes. %d and <b>%d</b> make 10." % (n, 10 - n))
    if kind == "pair":
        a = r.randint(0, 10)
        right = "%d and %d" % (a, 10 - a)
        wrong = [(a, 9 - a), (a + 1, 10 - a), (a, 11 - a), (a - 1, 10 - a), (a + 2, 9 - a)]
        wr = ["%d and %d" % w for w in wrong if 0 <= w[0] <= 10 and 0 <= w[1] <= 10]
        return mcq("Which two numbers make <b>10</b>?", right, wr, "<b>%s</b> make 10." % right, allow_zero=True)
    a = r.randint(1, 9)
    return mcq("Hold up 10 fingers. Put %d down. How many are still up?" % a, 10 - a, [a, 10] + near(10 - a, 1), "10 is %d and %d. Put %d down and <b>%d</b> are still up." % (a, 10 - a, a, 10 - a))


# ------------------------------------------------------------ set 4: benchmarks 5 and 10
def one_bench(r):
    n = r.randint(1, 10)
    kind = r.choice(["five", "five", "ten", "five_and"])
    if kind == "five":
        if n == 5:
            return None
        right = "more than 5" if n > 5 else "less than 5"
        return mcq(fig(row_svg(n, r.choice(KINDS))) + "Is this <b>more than 5</b> or <b>less than 5</b>?", right, ["less than 5" if n > 5 else "more than 5", "exactly 5", "exactly 10"],
                   "There %s %d. %d is <b>%s</b>." % ("is" if n == 1 else "are", n, n, right))
    if kind == "ten":
        if n == 10:
            return None
        return mcq(fig(cards_svg([str(n)])) + "How many more make <b>10</b>?", 10 - n, [n, 10] + near(10 - n, 1), "Count on from %d to 10: <b>%d</b> more." % (n, 10 - n))
    if n <= 5:
        return None
    return mcq(fig(tenframe_svg(n)) + "%d is 5 and how many more?" % n, n - 5, [n, 5] + near(n - 5, 1), "The top row is 5. %d is 5 and <b>%d</b>." % (n, n - 5))


# ------------------------------------------------------------ set 5: stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    w = r.randint(4, 10)
    a = r.randint(1, w - 1)
    b = w - a
    kind = r.choice(["salmon", "eagle", "boots", "pots"])
    if kind == "salmon":
        q = fig(two_groups_svg(a, "fish", b, "fish")) + "%s sees %d salmon in the river. %d %s big and the rest are small. How many are small?" % (k["n"], w, a, "is" if a == 1 else "are")
    elif kind == "eagle":
        q = "There are %d eagles. %d %s in a tree. The rest fly in the sky. How many fly in the sky?" % (w, a, "sits" if a == 1 else "sit")
    elif kind == "boots":
        q = "%s's family has %d rain boots by the door. %d %s red. The rest are yellow. How many are yellow?" % (k["n"], w, a, "is" if a == 1 else "are")
    else:
        q = "%s plants %d seeds in two pots. %d %s in the first pot. How many go in the second pot?" % (k["n"], w, a, "goes" if a == 1 else "go")
    return mcq(q, b, [w, a] + near(b, 1), "%d and <b>%d</b> make %d." % (a, b, w))


def build():
    sets = [S("Number bonds", collect(one_bond, 20, R)),
            S("The hidden part", collect(one_hidden, 20, R)),
            S("Making 10", collect(one_ten, 20, R)),
            S("Using 5 and 10", collect(one_bench, 20, R)),
            S("Part-part-whole stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>A number can be <b>broken into two parts</b>: 7 is 5 and 2, or 4 and 3.</li>"
        "<li>The two parts join back to make the <b>whole</b>.</li>"
        "<li>On a ten frame, the empty boxes show how many more make <b>10</b>.</li>"
        "<li>Use <b>5</b> and <b>10</b> as helpers: 8 is 5 and 3, and 8 is 2 less than 10.</li></ul>",
        [figure(bond_svg(8, 5, 3), "8 is 5 and 3."),
         figure(tenframe_svg(6), "6 dots and 4 empty boxes: 6 and 4 make 10.")],
        [["Giving the whole instead of the missing part", "Ask: what joins with the part I see to make the whole?"],
         ["Adding the two numbers shown", "If the whole is given, the missing part is smaller than the whole."],
         ["Counting the dots instead of the empty boxes", "To make 10, count the empty boxes."]])
    faq = [("What does decomposing numbers mean?", "Breaking a number into parts, such as 7 into 4 and 3. Putting the parts back together is recomposing."),
           ("What is part-part-whole thinking?", "Seeing that a whole is made of two parts. If you know the whole and one part, you can find the other part."),
           ("Why are 5 and 10 important?", "They are benchmarks. Children see numbers like 7 as 5 and 2, or 3 less than 10, which makes adding and taking away easier later."),
           ("How can I practise making 10 at home?", "Use 10 fingers or 10 small toys. Hide some and ask how many are hidden.")]
    make("decomposing-numbers-to-10", 4, "Computational fluency", "Decomposing Numbers to 10: Number Bonds and Making 10", "Decomposing numbers to 10",
         "Decomposition of numbers to 10: decomposing and recomposing quantities to 10, benchmarks of 5 and 10, making 10, part-part-whole thinking",
         "Free Kindergarten math worksheets on decomposing numbers to 10 for the BC curriculum: number bonds, hidden parts, making 10 on a ten frame, the benchmarks 5 and 10, and part-part-whole stories. 100 picture questions with answers.",
         "A number can be broken into two parts that join back to make it.", "7 is 5 and 2. On a ten frame, the empty boxes show how many more make 10.",
         body, faq, sets)


if __name__ == "__main__":
    build()
