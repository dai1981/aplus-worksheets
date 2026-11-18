# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Division Facts (TEKS 3.4F, 3.4H, 3.4J)
  python3 tools/gen_ustx_math_g3_division_facts.py
Sharing equally and making equal groups (3.4H), division with jumps back on a number line and repeated
subtraction, fact families (the Ontario Grade 4 maker with Texas names), dividing by thinking of a
multiplication fact (3.4J, 3.4F), and word problems.
Wrong answers come from real mistakes: subtracting instead of dividing, giving the number of groups when the
question asks for the size of each group, using the wrong fact in the family, and thinking 0 ÷ 5 is 5.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run, adopt, svg_wrap, text,
                       GREEN, FILL, INK, RED, example)
import gen_caon_math_g4_facts as on
import gen_caon_math_g3_facts as on3

adopt(on)
R = random.Random(60601)


def plates_svg(g, n, show=True):
    """g plates with n counters each (or empty plates when show is False)."""
    cell, pad = 18, 8
    per = min(5, n) if n else 1
    rows = (n + per - 1) // per if n else 1
    bw, bh = per * cell + 2 * pad, rows * cell + 2 * pad
    gap = 12
    per_row = min(g, 5)
    nr = (g + per_row - 1) // per_row
    W, H = per_row * (bw + gap) + 4, nr * (bh + gap) + 4
    s = []
    for i in range(g):
        rr, cc = divmod(i, per_row)
        x, y = 2 + cc * (bw + gap), 2 + rr * (bh + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='14' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, bw, bh, GREEN))
        if show:
            for j in range(n):
                a, b = divmod(j, per)
                s.append("<circle cx='%d' cy='%d' r='6.5' fill='%s'/>" % (x + pad + b * cell + cell / 2, y + pad + a * cell + cell / 2, GREEN))
    return svg_wrap(W, H, "".join(s), "%d plates with %d counters on each" % (g, n) if show else "%d empty plates" % g)


# ------------------------------------------------------------ set 1: share equally
def one_share(r):
    g, n = r.randint(2, 6), r.randint(2, 8)
    t = g * n
    kind = r.choice(["each", "groups", "pic"])
    if kind == "pic":
        return mcq(fig(plates_svg(g, n)) + "%d counters are shared equally on %d plates. Which division fact matches the picture?" % (t, g),
                   "%d ÷ %d = %d" % (t, g, n), ["%d − %d = %d" % (t, g, t - g), "%d ÷ %d = %d" % (t, n, g) if g != n else "%d ÷ %d = %d" % (t, 1, t), "%d × %d = %d" % (g, n, t + n)],
                   "%d shared into %d equal groups gives %d in each group: <b>%d ÷ %d = %d</b>." % (t, g, n, t, g, n))
    if kind == "each":
        return mcq(fig(plates_svg(g, 0, show=False)) +
                   "Share %d counters equally on %d plates. How many counters go on each plate?" % (t, g), n, [g, t - g, n + 1, n - 1],
                   "Deal the counters out one at a time until they are all used. Each plate gets <b>%d</b>, because %d × %d = %d." % (n, g, n, t))
    return mcq("%d counters are put in groups of %d. How many groups are there?" % (t, n), g, [n, t - n, g + 1, g - 1],
               "Count how many groups of %d you can make from %d: %d × %d = %d, so there are <b>%d</b> groups." % (n, t, g, n, t, g))


# ------------------------------------------------------------ set 2: number lines and repeated subtraction
def one_line(r):
    d, q = r.randint(2, 9), r.randint(2, 9)
    t = d * q
    kind = r.choice(["sub", "jumps"])
    if kind == "sub" and q <= 6:
        steps = " − ".join([str(t)] + [str(d)] * q) + " = 0"
        return mcq("%s. Which division fact does this show?" % steps, "%d ÷ %d = %d" % (t, d, q),
                   ["%d ÷ %d = %d" % (t, q, d) if q != d else "%d ÷ %d = %d" % (t, d, q + 1), "%d − %d = %d" % (t, d, t - d), "%d ÷ %d = %d" % (t, d, q + 1) if q != d else "%d ÷ %d = %d" % (t, d, q - 1)],
                   "You took away %d, %d times, to reach 0: <b>%d ÷ %d = %d</b>." % (d, q, t, d, q))
    if t > 90:
        return None
    pic = on3.jumps_svg(d, q, t)
    return mcq(fig(pic) + "The jumps go from 0 to %d in jumps of %d. Which division fact do the jumps show?" % (t, d), "%d ÷ %d = %d" % (t, d, q),
               ["%d ÷ %d = %d" % (t, d, q + 1), "%d − %d = %d" % (t, d, t - d), "%d × %d = %d" % (d, d, d * d) if d != q else "%d ÷ %d = %d" % (t, d, q - 1)],
               "There are %d jumps of %d to reach %d: <b>%d ÷ %d = %d</b>." % (q, d, t, t, d, q))


# ------------------------------------------------------------ set 4: think multiplication
def one_think(r):
    d, q = r.randint(1, 10), r.randint(0, 10)
    if (d == 1 or q in (0, 1)) and r.random() < 0.6:
        return None
    t = d * q
    kind = r.choice(["div", "div", "think"])
    if kind == "think":
        if q == 0:
            return None
        return mcq("To find %d ÷ %d, which multiplication fact can you use?" % (t, d), "%d × %d = %d" % (d, q, t),
                   ["%d × %d = %d" % (d, t, d * t) if d * t <= 100 else "%d + %d = %d" % (d, q, d + q), "%d × %d = %d" % (d, q + 1, d * (q + 1)), "%d − %d = %d" % (t, d, t - d)],
                   "Ask: %d times what is %d? <b>%d × %d = %d</b>, so %d ÷ %d = %d." % (d, t, d, q, t, t, d, q))
    wrong = [t - d, q + 1, q - 1, d, t]
    note = " 0 divided by any number is 0." if q == 0 else " Any number divided by 1 is the number." if d == 1 else ""
    return mcq("%d ÷ %d = ?" % (t, d), q, wrong, "Think: %d × ? = %d. %d × %d = %d, so the answer is <b>%d</b>.%s" % (d, t, d, q, t, q, note), allow_zero=True)


# ------------------------------------------------------------ set 5: word problems
STORIES = [("{k} has {t} stickers. {He} gives them all away, sharing them equally among {d} friends. How many stickers does each friend get?", "each", "stickers"),
           ("A coach puts {t} players into teams of {d}. How many teams are there?", "groups", "teams"),
           ("{t} students ride in vans. Each van holds {d} students. How many vans are needed?", "groups", "vans"),
           ("{k} has {t} tortillas. {He} puts {d} tortillas in each bag. How many bags does {he} fill?", "groups", "bags"),
           ("{t} muffins are shared equally on {d} trays. How many muffins are on each tray?", "each", "muffins"),
           ("A garden has {t} plants in {d} equal rows. How many plants are in each row?", "each", "plants"),
           ("{k} reads {t} pages in {d} days. {He} reads the same number each day. How many pages a day?", "each", "pages"),
           ("Pencils come in boxes of {d}. The teacher needs {t} pencils. How many boxes does she need?", "groups", "boxes")]


def one_story(r):
    t_, mode, unit = r.choice(STORIES)
    d, q = r.randint(2, 10), r.randint(2, 10)
    t = d * q
    k = Kid(r).next()
    s = t_.format(t=t, d=d, k=k["n"], He=k["He"], he=k["he"])
    return mcq(s, "%d %s" % (q, unit), ["%d %s" % (t - d, unit), "%d %s" % (q + 1, unit), "%d %s" % (t + d, unit), "%d %s" % (d, unit) if d != q else "%d %s" % (q - 1, unit)],
               "%d ÷ %d = %d, because %d × %d = %d. The answer is <b>%d %s</b>." % (t, d, q, d, q, t, q, unit))


def build():
    s3 = run(on.set_division, "rnd", seed=81)["items"]
    sets = [S("Share equally and make groups", collect(one_share, 20, R)),
            S("Jumps back and repeated subtraction", collect(one_line, 20, R)),
            S("Fact families", s3),
            S("Divide by thinking of a multiplication fact", collect(one_think, 20, R, avoid=[s3])),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Division splits a total into <b>equal groups</b>. 24 ÷ 4 can mean 4 groups (how many in each?) or groups of 4 (how many groups?).</li>"
        "<li>Every division fact has a multiplication fact. To find 56 ÷ 7, ask: 7 times what is 56? 7 × 8 = 56, so 56 ÷ 7 = 8.</li>"
        "<li>A <b>fact family</b> uses the same three numbers: 4 × 6 = 24, 6 × 4 = 24, 24 ÷ 4 = 6, 24 ÷ 6 = 4.</li>"
        "<li>0 ÷ 5 = 0. 5 ÷ 1 = 5. 5 ÷ 5 = 1.</li></ul>",
        [figure(plates_svg(4, 6), "24 counters shared on 4 plates: 6 on each plate. 24 ÷ 4 = 6."),
         example("Find 42 ÷ 6.", ["Think: 6 × ? = 42", "6 × 7 = 42"], "42 ÷ 6 = 7")],
        [["Subtracting: 24 ÷ 4 = 20", "Division makes equal groups. Use the multiplication fact."],
         ["Giving the number of groups when the question asks how many in each", "Read the question again: is it asking for each group or the number of groups?"],
         ["Thinking 0 ÷ 5 = 5", "If there is nothing to share, each group gets 0."]])
    faq = [("What does TEKS 3.4H ask?", "Find the number of objects in each group when a set of objects is shared or partitioned into equal groups."),
           ("How do I learn division facts?", "Use multiplication. Every fact like 7 × 8 = 56 gives two division facts: 56 ÷ 7 = 8 and 56 ÷ 8 = 7 (TEKS 3.4F, 3.4J)."),
           ("What are the two meanings of division?", "Sharing (how many in each group) and grouping (how many groups). Both use the same fact."),
           ("Why can't you divide by 0?", "You cannot share something into 0 groups. Grade 3 students learn that 0 divided by a number is 0.")]
    make("division-facts", 6, "Number and Operations", "3.4F, 3.4H, 3.4J",
         "3.4F recall facts to multiply up to 10 by 10 with automaticity and recall the corresponding division facts; 3.4H determine the number of objects in each group when a set of objects is partitioned into equal shares or a set of objects is shared equally; 3.4J determine a quotient using the relationship between multiplication and division",
         "Division Facts: Equal Shares, Fact Families and Thinking Multiplication", "Division Facts",
         "Free Grade 3 division worksheets for Texas TEKS 3.4F, 3.4H and 3.4J: share equally, make equal groups, number lines, fact families, divide using multiplication facts and word problems. 100 questions with answers.",
         "Division splits a total into equal groups.", "To divide, think of the multiplication fact: 56 ÷ 7 = 8 because 7 × 8 = 56.",
         body, faq, sets, seo_title="Grade 3 Division Facts Worksheets: Equal Shares and Fact Families (TEKS 3.4H, STAAR)")


if __name__ == "__main__":
    build()
