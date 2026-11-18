# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Numbers to 10 (BC Mathematics Curriculum, Kindergarten Content: Number concepts to 10)
  python3 tools/gen_cabc_math_k_numbers_to_10.py
Counting objects to 10 (one-to-one, the last number tells how many), zero, linking numerals and words to
groups, counting order (before, after, between), ten frames, and counting stories (the count stays the same
when things are moved).
Wrong answers come from real mistakes: counting one object twice or missing one, mixing up before and after,
thinking a spread-out row has more, and thinking zero is not a number.
"""
import random
from k_pics import row_svg, scatter_svg, plate_svg, cards_svg, number_line_svg, tenframe_svg, lettered_groups_svg, match_svg, name, KINDS
from bck_common import Kids, letters, mcq, finish, make, fig, figure, lesson, collect, S

R = random.Random(52101)
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def near(n, lo=0, hi=10):
    out = [n + 1, n - 1, n + 2, n - 2, n + 3, n - 3]
    return [x for x in out if lo <= x <= hi and x != n]


# ------------------------------------------------------------ set 1: how many?
def one_count(r):
    n = r.randint(1, 10)
    k = r.choice(KINDS)
    how = r.choice(["row", "scatter", "scatter", "plate"])
    if n == 1 and how == "row":
        return None
    svg = row_svg(n, k) if how == "row" else plate_svg(n, k) if how == "plate" else scatter_svg(n, k, r.randint(1, 9999))
    q = fig(svg) + ("How many %s are on the plate?" % name(k, n) if how == "plate" else "How many %s?" % name(k, n))
    e = "Touch each one once and count: %s. The last number you say tells how many: <b>%d</b>." % (", ".join(map(str, range(1, n + 1))), n)
    return mcq(q, n, near(n), e)


def one_zero(r):
    k = r.choice(KINDS)
    q = fig(plate_svg(0, k)) + "How many %s are on the plate?" % name(k)
    return mcq(q, 0, [1, 10, 2], "The plate is empty. There are no %s. The number for none is <b>0</b>." % name(k), allow_zero=True)


def set_count(r):
    return collect(one_count, 18, r) + collect(one_zero, 2, r)


# ------------------------------------------------------------ set 2: numerals, words and groups
def one_link(r):
    kind = r.choice(["word", "word", "which", "card"])
    n = r.randint(1, 10)
    if kind == "word":
        q = "Which number is <b>%s</b>?" % WORDS[n]
        return mcq(q, n, near(n), "%s is <b>%d</b>." % (WORDS[n].capitalize(), n))
    if kind == "card":
        q = fig(cards_svg([str(n)])) + "How do you say this number?"
        return mcq(q, WORDS[n], [WORDS[x] for x in near(n)], "This is %d. We say <b>%s</b>." % (n, WORDS[n]))
    k = r.choice(KINDS)
    others = near(n, 1, 10)
    r.shuffle(others)
    vals = [n] + others[:3]
    r.shuffle(vals)
    letter = "ABCD"[vals.index(n)]
    q = fig(lettered_groups_svg([(v, k) for v in vals])) + "Which group has <b>%d</b> %s?" % (n, name(k, n))
    it = mcq(q, letter, [l for l in "ABCD" if l != letter], "Count each group. Group <b>%s</b> has %d." % (letter, n))
    return letters(it, letter)


# ------------------------------------------------------------ set 3: counting order
def one_order(r):
    kind = r.choice(["after", "before", "between", "next", "back"])
    if kind == "after":
        n = r.randint(0, 9)
        return mcq(fig(cards_svg([str(n), "?"])) + "Which number comes just <b>after</b> %d?" % n, n + 1, [n - 1, n + 2, n], "Count on one: %d, <b>%d</b>." % (n, n + 1), allow_zero=True)
    if kind == "before":
        n = r.randint(1, 10)
        return mcq(fig(cards_svg(["?", str(n)])) + "Which number comes just <b>before</b> %d?" % n, n - 1, [n + 1, n - 2, n], "Count back one: <b>%d</b>, %d." % (n - 1, n), allow_zero=True)
    if kind == "between":
        n = r.randint(1, 9)
        return mcq(fig(cards_svg([str(n - 1), "?", str(n + 1)])) + "Which number goes in the middle?", n, [n + 2, n - 2, n + 1, n - 1], "Count: %d, <b>%d</b>, %d." % (n - 1, n, n + 1), allow_zero=True)
    if kind == "next":
        s = r.randint(1, 6)
        seq = list(range(s, s + 3))
        marks = {v: str(v) for v in seq}
        marks[s + 3] = "?"
        return mcq(fig(number_line_svg(0, 10, marks)) + "Count: %s. What comes next?" % ", ".join(map(str, seq)), s + 3, [s + 2, s + 4, s], "Count up by one: %s, <b>%d</b>." % (", ".join(map(str, seq)), s + 3))
    s = r.randint(5, 10)
    seq = [s, s - 1, s - 2]
    return mcq(fig(cards_svg([str(v) for v in seq] + ["?"])) + "Count back: %s. What comes next?" % ", ".join(map(str, seq)), s - 3, [s - 2, s - 4, s], "Count back by one: %s, <b>%d</b>." % (", ".join(map(str, seq)), s - 3), allow_zero=True)


# ------------------------------------------------------------ set 4: ten frames
def one_frame(r):
    n = r.randint(1, 10)
    kind = r.choice(["count", "count", "count", "empty", "five"])
    if kind == "five":
        if n <= 5:
            return None
        return mcq(fig(tenframe_svg(n)) + "The top row is 5. <b>5 and how many more</b> make %d?" % n, n - 5, near(n - 5, 1, 10), "The bottom row has %d dot%s. 5 and <b>%d</b> more make %d." % (n - 5, "" if n == 6 else "s", n - 5, n))
    if kind == "count":
        e = "The top row holds 5. %s" % ("Count the dots: <b>%d</b>." % n if n <= 5 else "5 and %d more make <b>%d</b>." % (n - 5, n))
        return mcq(fig(tenframe_svg(n)) + "How many dots are in the ten frame?", n, near(n), e)
    if n == 10:
        return None
    return mcq(fig(tenframe_svg(n)) + "How many boxes are <b>empty</b>?", 10 - n, near(10 - n), "A ten frame has 10 boxes. %d are full, so <b>%d</b> are empty." % (n, 10 - n), allow_zero=True)


# ------------------------------------------------------------ set 5: counting stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    kind = r.choice(["more1", "spread", "spread", "last", "twice"])
    kk = r.choice(KINDS)
    if kind == "more1":
        n = r.randint(2, 9)
        q = fig(row_svg(n, kk)) + "%s has %d %s. %s gets 1 more. How many now?" % (k["n"], n, name(kk, n), k["He"])
        return mcq(q, n + 1, [n, n + 2, n - 1], "1 more than %d is <b>%d</b>. Count on: %d, %d." % (n, n + 1, n, n + 1))
    if kind == "spread":
        n = r.randint(4, 9)
        q = fig(match_svg([(n, kk, "", 34), (n, kk, "", 56)])) + "%s counts %d %s in the top row. Then %s spreads them out. How many are there now?" % (k["n"], n, name(kk, n), k["he"])
        return mcq(q, n, [n + 1, n + 2, n - 1], "Moving things does not change how many there are. There are still <b>%d</b>." % n)
    if kind == "last":
        n = r.randint(3, 10)
        q = "%s counts the %s: %s. How many %s are there?" % (k["n"], name(kk), ", ".join(map(str, range(1, n + 1))), name(kk))
        return mcq(q, n, [1, n + 1, n - 1], "The last number you say tells how many: <b>%d</b>." % n)
    n = r.randint(3, 9)
    q = fig(row_svg(n, kk)) + "%s counts %d %s, but %s counted one of them twice. How many are there really?" % (k["n"], n + 1, name(kk), k["he"])
    return mcq(q, n, [n + 1, n + 2, n - 1], "One was counted two times, so %d is one too many. There are <b>%d</b>. Touch each one once." % (n + 1, n))


def build():
    sets = [S("How many? 0 to 10", set_count(R)),
            S("Numbers, words and groups", collect(one_link, 20, R)),
            S("Before, after and between", collect(one_order, 20, R)),
            S("Ten frames", collect(one_frame, 20, R)),
            S("Counting stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>Touch each thing <b>once</b> and say one number for each.</li>"
        "<li>The <b>last number</b> you say tells how many.</li>"
        "<li>Moving things around does not change how many there are.</li>"
        "<li><b>0</b> (zero) is the number for none.</li></ul>",
        [figure(row_svg(7, "apple"), "1, 2, 3, 4, 5, 6, 7. There are 7 apples."),
         figure(tenframe_svg(8), "A full row is 5. 5 and 3 more make 8.")],
        [["Counting one thing twice", "Touch each thing as you count, or move it to one side."],
         ["Thinking a spread-out row has more", "Count both rows. Moving them does not change the number."],
         ["Mixing up before and after", "After means count on one. Before means count back one."]])
    faq = [("What does number concepts to 10 mean in Kindergarten?", "Children count objects to 10 one at a time, know the last number tells how many, put numbers 1 to 10 in order and link each number to a group of objects."),
           ("How can I help my child count accurately?", "Ask your child to touch or move each object as they say one number. Then ask, How many? The last number said is the answer."),
           ("What is a ten frame?", "A box of 10 squares in two rows of 5. Children see quickly that a full row is 5 and a full frame is 10."),
           ("Is zero a number?", "Yes. Zero is the number for none, such as an empty plate.")]
    make("numbers-to-10", 1, "Number", "Numbers to 10: Count, Order and Ten Frames", "Numbers to 10",
         "Number concepts to 10: one-to-one correspondence, conservation, cardinality, stable order counting, sequencing 1-10, linking sets to numerals, subitizing",
         "Free Kindergarten math worksheets on numbers to 10 for the BC curriculum: count objects, zero, numbers and words, before and after, ten frames and counting stories. 100 picture questions with answers.",
         "The last number you say tells how many.", "Touch each thing once as you count. Moving things does not change how many.",
         body, faq, sets)


if __name__ == "__main__":
    build()
