# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Multiplication Facts to 10 × 10 (TEKS 3.4D, 3.4E, 3.4F)
  python3 tools/gen_ustx_math_g3_multiplication_facts.py
Equal groups and arrays (3.4D), many ways to show a fact: repeated addition, jumps on a number line, skip
counting and area models (3.4E), strategies for the 6s to 9s, mixed facts to 10 × 10 (3.4F), and word problems.
Sets 1 and 3 reuse the Ontario Grade 4 fact makers with Texas names and new numbers.
Wrong answers come from real mistakes: adding the factors, counting one group too many or too few, mixing up
neighbouring facts (7 × 8 and 7 × 7), and thinking anything times 0 is the other number.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, run, adopt, number_line,
                       svg_wrap, GREEN, FILL, INK, text, example)
import gen_caon_math_g4_facts as on
import gen_caon_math_g3_facts as on3

adopt(on)
R = random.Random(60501)


def area_svg(rows, cols, cell=22):
    o = 4
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (o + j * cell, o + i * cell, cell, cell, FILL, GREEN))
    return svg_wrap(cols * cell + 2 * o, rows * cell + 2 * o, "".join(s), "area model with %d rows of %d squares" % (rows, cols))


# ------------------------------------------------------------ set 2: many ways to show a fact
def one_show(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    kind = r.choice(["repeated", "jumps", "skip", "area", "which"])
    if kind == "repeated":
        add = " + ".join([str(b)] * a)
        return mcq("Which multiplication matches %s?" % add, "%d × %d" % (a, b), ["%d + %d" % (a, b), "%d × %d" % (a + 1, b), "%d × %d" % (b, b) if a != b else "%d × %d" % (a, a + 1)],
                   "There are %d groups of %d: <b>%d × %d</b> = %d." % (a, b, a, b, a * b))
    if kind == "jumps":
        pic = on3.jumps_svg(b, a, (a + 1) * b if (a + 1) * b <= 100 else a * b)
        return mcq(fig(pic) + "Which multiplication fact do the jumps show?", "%d × %d = %d" % (a, b, a * b),
                   ["%d × %d = %d" % (b, b, b * b) if a != b else "%d × %d = %d" % (a + 1, b, (a + 1) * b), "%d + %d = %d" % (a, b, a + b), "%d × %d = %d" % (a + 1, b, (a + 1) * b) if a != b else "%d × %d = %d" % (a - 1, b, (a - 1) * b)],
                   "There are %d jumps of %d, landing on %d: <b>%d × %d = %d</b>." % (a, b, a * b, a, b, a * b))
    if kind == "skip":
        seq = [b * i for i in range(1, a + 1)]
        return mcq("Skip count by %ds: %s. Which fact does this show?" % (b, ", ".join(str(x) for x in seq)), "%d × %d = %d" % (a, b, a * b),
                   ["%d × %d = %d" % (a + 1, b, (a + 1) * b), "%d + %d = %d" % (a, b, a + b), "%d × %d = %d" % (b, b, b * b) if a != b else "%d × %d = %d" % (a - 1, b, (a - 1) * b)],
                   "You said %d numbers, counting by %d: <b>%d × %d = %d</b>." % (a, b, a, b, a * b))
    if kind == "area":
        return mcq(fig(area_svg(a, b)) + "What multiplication fact does the area model show?", "%d × %d = %d" % (a, b, a * b),
                   ["%d × %d = %d" % (a, b + 1, a * (b + 1)), "%d + %d = %d" % (a, b, a + b), "%d × %d = %d" % (a - 1, b, (a - 1) * b)],
                   "%d rows with %d squares in each row: <b>%d × %d = %d</b>." % (a, b, a, b, a * b))
    return mcq(fig(on3.array_svg(a, b)) + "Which number sentence matches the array?", "%d × %d = %d" % (a, b, a * b),
               ["%d + %d = %d" % (a, b, a + b), "%d × %d = %d" % (a, b, a * b + b), "%d × %d = %d" % (a + 1, b + 1, (a + 1) * (b + 1))],
               "%d rows of %d dots: <b>%d × %d = %d</b>." % (a, b, a, b, a * b))


# ------------------------------------------------------------ set 4: facts to 10 × 10
def one_fact(r):
    a = r.randint(0, 10)
    b = r.randint(0, 10)
    if (a in (0, 1) or b in (0, 1)) and r.random() < 0.6:
        return None
    p = a * b
    wrong = [a + b, a * (b + 1), a * (b - 1) if b > 0 else 2 * a + 1, (a + 1) * b, p + 1 if p > 0 else 1]
    if a == 0 or b == 0:
        wrong = [max(a, b), a + b + 1, 1, 10]
    form = r.choice(["%d × %d = ?", "What is %d × %d?", "%d groups of %d is how many?"])
    return mcq(form % (a, b), p, wrong,
               "%d × %d = <b>%d</b>.%s" % (a, b, p, " Anything times 0 is 0." if 0 in (a, b) else " Anything times 1 is itself." if 1 in (a, b) else ""), allow_zero=True)


# ------------------------------------------------------------ set 5: word problems
STORIES = [("Each row in the band has {b} players. There are {a} rows. How many players are in the band?", "players"),
           ("A pack has {b} juice boxes. {k} buys {a} packs. How many juice boxes is that?", "juice boxes"),
           ("{k} plants {a} rows of tomatoes. Each row has {b} plants. How many tomato plants are there?", "plants"),
           ("A spider has 8 legs. How many legs do {a} spiders have?", "legs"),
           ("Tacos come {b} to a plate. {k}'s family orders {a} plates. How many tacos is that?", "tacos"),
           ("Each table in the cafeteria seats {b} students. How many students can sit at {a} tables?", "students"),
           ("A carton holds {b} eggs. How many eggs are in {a} cartons?", "eggs"),
           ("Each relay team has {b} runners. {a} teams run in a race. How many runners is that?", "runners"),
           ("{k} reads {b} pages each night for {a} nights. How many pages is that?", "pages"),
           ("A bike has 2 wheels. How many wheels do {a} bikes have?", "wheels")]


def one_story(r):
    t, unit = r.choice(STORIES)
    a, b = r.randint(3, 10), r.randint(3, 10)
    if "spider" in t:
        b = 8
    if "bike" in t:
        b = 2
    if "eggs" in t:
        b = r.choice([6, 10])
    k = Kid(r).next()
    q = t.format(a=a, b=b, k=k["n"])
    return mcq(q, "%d %s" % (a * b, unit), ["%d %s" % (a + b, unit), "%d %s" % (a * b - b, unit), "%d %s" % (a * b + b, unit), "%d %s" % (a * (b + 1) + 1, unit)],
               "%d groups of %d: %d × %d = <b>%d %s</b>." % (a, b, a, b, a * b, unit))


def build():
    s1 = run(on.set_facts, "rnd", seed=71)["items"]
    s3 = run(on.set_strategies, "rnd", seed=72)["items"]
    sets = [S("Equal groups and arrays", s1),
            S("Many ways to show a fact", collect(one_show, 20, R)),
            S("Strategies for 6, 7, 8 and 9", s3),
            S("Facts to 10 × 10", collect(one_fact, 20, R, avoid=[s1, s3])),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Multiplication puts together <b>equal groups</b>. 4 × 6 means 4 groups of 6.</li>"
        "<li>You can show a fact many ways: equal groups, an <b>array</b>, an <b>area model</b>, repeated addition (6 + 6 + 6 + 6), jumps on a number line, or skip counting (6, 12, 18, 24).</li>"
        "<li>Use facts you know: double the 3s to get the 6s, use 10s to get the 9s (9 × 7 = 70 − 7), and turn facts around (3 × 8 = 8 × 3).</li>"
        "<li>Any number times 0 is 0. Any number times 1 is the number.</li></ul>",
        [figure(area_svg(4, 6), "4 rows of 6 squares: 4 × 6 = 24."),
         example("Find 7 × 8.", ["7 × 4 = 28 (a fact you know)", "8 is double 4, so double 28.", "28 + 28 = 56"], "7 × 8 = 56")],
        [["Adding the factors: 6 × 4 = 10", "× means equal groups. 6 groups of 4 is 24."],
         ["Mixing up nearby facts: 7 × 8 = 49", "Check with a fact you know: 7 × 8 = 7 × 7 + 7 = 56."],
         ["Thinking 5 × 0 = 5", "0 groups of 5, or 5 groups of 0, is 0."]])
    faq = [("Which multiplication facts must Grade 3 students know in Texas?", "TEKS 3.4F asks students to recall facts up to 10 × 10 with automaticity, and the related division facts."),
           ("What does representing multiplication mean?", "Showing a fact with equal groups, arrays, area models, equal jumps on a number line or skip counting (TEKS 3.4E)."),
           ("What is the best way to learn the hard facts?", "Use a strategy, then practice. For example, 6s are double the 3s, and 9s are 10s minus one group."),
           ("How are facts tested on the STAAR?", "Students use facts inside word problems, arrays and area questions, so quick recall saves time on every part of the test.")]
    make("multiplication-facts", 5, "Number and Operations", "3.4D, 3.4E, 3.4F",
         "3.4D determine the total number of objects when equally-sized groups of objects are combined or arranged in arrays up to 10 by 10; 3.4E represent multiplication facts by using a variety of approaches such as repeated addition, equal-sized groups, arrays, area models, equal jumps on a number line, and skip counting; 3.4F recall facts to multiply up to 10 by 10 with automaticity and recall the corresponding division facts",
         "Multiplication Facts to 10 × 10: Arrays, Area Models and Strategies", "Multiplication Facts",
         "Free Grade 3 multiplication facts worksheets for Texas TEKS 3.4D, 3.4E and 3.4F: equal groups, arrays, area models, number line jumps, skip counting, strategies for 6s to 9s, facts to 10 × 10 and word problems. 100 questions with answers.",
         "Multiplication puts together equal groups.", "Show a fact with groups, arrays, area models, jumps or skip counting. Use facts you know to find harder ones.",
         body, faq, sets, seo_title="Grade 3 Multiplication Facts Worksheets: Arrays and Strategies (TEKS 3.4F, STAAR)")


if __name__ == "__main__":
    build()
