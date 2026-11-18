# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Concrete Graphs (BC Mathematics Curriculum, Kindergarten Content: Concrete or pictorial
graphs as a visual tool for collecting and representing data)
  python3 tools/gen_cabc_math_k_concrete_graphs.py
Sorting a mixed collection and counting one kind, sorting rules, reading concrete graphs (cube rows and cube
towers on one start line, from the BC Grade 1 graphs unit), comparing the groups, and picture graphs with
questions we can ask the class. All numbers are 10 or less.
Wrong answers come from real mistakes: counting every object instead of one kind, reading the shortest row as
the most, giving one of the two counts instead of how many more, and asking a question nobody can answer by
collecting data.
"""
import random
from k_pics import mixed_svg, name, KINDS
from f_common import pictograph_svg
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_cabc_math_g1_graphs as g1

R = random.Random(53001)
POS = Cycle()


def near(n, lo=0, hi=10):
    return [x for x in [n + 1, n - 1, n + 2, n - 2] if lo <= x <= hi and x != n]


# ------------------------------------------------------------ set 1: sort and count
def one_count(r):
    ks = r.sample(KINDS, r.choice([2, 3]))
    vals = [r.randint(1, 6) for _ in ks]
    if sum(vals) > 10 or len(set(vals)) != len(vals):
        return None
    j = r.randrange(len(ks))
    pic = fig(mixed_svg(list(zip(ks, vals)), r.randint(1, 99999)))
    kind = r.choice(["count", "count", "more"])
    if kind == "count":
        return mcq(pic + "Sort the things. How many <b>%s</b> are there?" % name(ks[j]), vals[j], [sum(vals)] + [v for i, v in enumerate(vals) if i != j] + near(vals[j]),
                   "Look only at the %s. Touch each one as you count. There %s <b>%d</b>." % (name(ks[j]), "is" if vals[j] == 1 else "are", vals[j]))
    big = ks[vals.index(max(vals))]
    return mcq(pic + "Sort the things into groups. Which group has the <b>most</b>?", "The %s" % name(big),
               ["The %s" % name(k) for k in ks if k != big] + ["They are all the same"],
               "Count each group: %s. The most is <b>the %s</b>." % (", ".join("%d %s" % (v, name(k, v)) for k, v in zip(ks, vals)), name(big)))


# ------------------------------------------------------------ set 2: sorting rules
GROUPS = {"fruit": ["apple", "banana", "orange", "pear", "grapes", "blueberries"],
          "pets": ["dog", "cat", "rabbit", "goldfish", "hamster", "parrot"],
          "things that fly": ["kite", "airplane", "rocket", "helicopter", "paper airplane", "hot air balloon"],
          "clothes": ["hat", "sock", "shirt", "mitten", "sweater", "toque"],
          "things with wheels": ["car", "bike", "bus", "skateboard", "stroller", "truck"],
          "sea animals": ["orca", "crab", "octopus", "sea star", "seal", "jellyfish"]}
CATS = list(GROUPS)


def one_rule(r):
    g = r.choice(CATS)
    other = r.choice([c for c in CATS if c != g])
    three = r.sample(GROUPS[g], 3)
    if r.random() < 0.5:
        odd = r.choice(GROUPS[other])
        items = three + [odd]
        r.shuffle(items)
        q = "We sort into <b>%s</b>: %s. Which one does <b>not</b> belong?" % (g, ", ".join(items))
        art = "An" if odd[0] in "aeiou" else "A"
        return mcq(q, odd, [x for x in items if x != odd] + ["They all belong"], "%s %s is not one of the %s. <b>%s</b> does not belong." % (art, odd, g, odd.capitalize()))
    q = "%s, %s and %s are in one group. What is the sorting rule?" % (three[0].capitalize(), three[1], three[2])
    wr = [c.capitalize() for c in CATS if c != g]
    r.shuffle(wr)
    return mcq(q, g.capitalize(), wr[:3], "All three are %s. The rule is <b>%s</b>." % (g, g))


# ------------------------------------------------------------ concrete graphs
def data(r, n=3, hi=8):
    ctx = r.choice(g1.CTXS)
    cats = r.sample(ctx.cats, n)
    vals = r.sample(range(1, hi + 1), n)
    return ctx, cats, vals


def what(ctx, c, v):
    if ctx.fruit:
        return g1.FRUIT_PL[c] if v != 1 else c.lower()
    return "cubes" if v != 1 else "cube"


def one_read(r):
    ctx, cats, vals = data(r)
    style = r.choice(["row", "tower"])
    pic = g1.graph(ctx, cats, vals, style)
    kind = r.choice(["count", "count", "most", "fewest"])
    where = "row" if style == "row" else "tower"
    if kind == "count":
        j = r.randrange(3)
        return mcq(pic + "%s 1 %s is 1. How many for <b>%s</b>?" % (ctx.intro, "fruit" if ctx.fruit else "cube", cats[j]), vals[j],
                   [v for i, v in enumerate(vals) if i != j] + near(vals[j]),
                   "Find the %s %s and count from the %s. There are <b>%d</b>." % (cats[j], where, "start line" if style == "row" else "bottom", vals[j]))
    w = "most" if kind == "most" else "fewest"
    t = max(vals) if w == "most" else min(vals)
    o = min(vals) if w == "most" else max(vals)
    c = cats[vals.index(t)]
    co = cats[vals.index(o)]
    adj = ("longest" if w == "most" else "shortest") if style == "row" else ("tallest" if w == "most" else "shortest")
    return mcq(pic + "%s Which one has the <b>%s</b>?" % (ctx.intro, w), c, [x for x in cats if x != c] + ["They are all the same"],
               "The %s %s has the %s. <b>%s</b> has %d. %s has only %d." % (adj, where, w, c, t, co, o) if w == "most" else
               "The %s %s has the %s. <b>%s</b> has %d. %s has %d." % (adj, where, w, c, t, co, o))


def one_compare(r):
    ctx, cats, vals = data(r, n=3, hi=7)
    style = r.choice(["row", "tower"])
    pic = g1.graph(ctx, cats, vals, style)
    a, b = r.sample(range(3), 2)
    va, vb = vals[a], vals[b]
    kind = r.choice(["more", "more", "both", "which"])
    if kind == "more":
        if va < vb:
            a, b, va, vb = b, a, vb, va
        return mcq(pic + "How many more for <b>%s</b> than for <b>%s</b>?" % (cats[a], cats[b]), va - vb, [va, vb, va - vb + 1, va - vb - 1 if va - vb > 1 else va + vb],
                   "%s has %d and %s has %d. Match them up: %s has <b>%d</b> more." % (cats[a], va, cats[b], vb, cats[a], va - vb))
    if kind == "both":
        if va + vb > 10:
            return None
        return mcq(pic + "How many for <b>%s</b> and <b>%s</b> together?" % (cats[a], cats[b]), va + vb, [va, vb, abs(va - vb), va + vb + 1, va + vb - 1],
                   "%d and %d make <b>%d</b>." % (va, vb, va + vb))
    more = cats[a] if va > vb else cats[b]
    less = cats[b] if va > vb else cats[a]
    return mcq(pic + "Which has more: <b>%s</b> or <b>%s</b>?" % (cats[a], cats[b]), more, [less, "They are the same", "We cannot tell"],
               "%s has %d and %s has %d. <b>%s</b> has more." % (cats[a], va, cats[b], vb, more))


# ------------------------------------------------------------ set 5: picture graphs and questions
QS = [("Ms. Kaur's class wants to find the class's favourite fruit. Which question should they ask everyone?", "Which fruit do you like best?",
       ["Do you like school?", "How old is your teacher?", "What day is it?"]),
      ("The class wants to know how everyone gets to school. What should they do?", "Ask each child and count the answers",
       ["Ask only one child", "Guess", "Count the cars on the road"]),
      ("Which question can you answer by asking your class?", "What colour are your rain boots?",
       ["How far away is the moon?", "How many fish are in the ocean?", "Will it snow next year?"]),
      ("Why do we sort and graph things?", "To count and compare the groups",
       ["To make a mess", "To guess the answer", "Because graphs are pretty"]),
      ("Why do the cube rows start at the same line?", "So we can compare them fairly",
       ["So they look neat", "So they are all the same", "So we do not need to count"]),
      ("Each child votes for one favourite animal. How many times does each child vote?", "1 time",
       ["2 times", "As many as they like", "0 times"])]


def one_pict(r):
    if r.random() < 0.3:
        q, a, wr = r.choice(QS)
        return mcq(q, a, wr, "<b>%s</b>." % a)
    ks = r.sample(KINDS, 3)
    vals = r.sample(range(1, 9), 3)
    pic = fig(pictograph_svg(list(zip(ks, vals))))
    kind = r.choice(["count", "most", "fewest", "more"])
    if kind == "count":
        j = r.randrange(3)
        return mcq(pic + "Each picture is 1 vote. How many votes for the <b>%s</b>?" % name(ks[j], 1), vals[j], [v for i, v in enumerate(vals) if i != j] + near(vals[j]),
                   "Count the %s in that row: <b>%d</b>." % (name(ks[j]), vals[j]))
    if kind in ("most", "fewest"):
        t = max(vals) if kind == "most" else min(vals)
        k = ks[vals.index(t)]
        return mcq(pic + "Each picture is 1 vote. Which got the <b>%s</b> votes?" % kind, "The %s" % name(k, 1), ["The %s" % name(x, 1) for x in ks if x != k] + ["They are all the same"],
                   "The %s row is the %s: <b>the %s</b>, with %d." % (name(k, 1), "longest" if kind == "most" else "shortest", name(k, 1), t))
    a, b = sorted(r.sample(range(3), 2), key=lambda i: -vals[i])
    d = vals[a] - vals[b]
    return mcq(pic + "How many more votes for the <b>%s</b> than the <b>%s</b>?" % (name(ks[a], 1), name(ks[b], 1)), d, [vals[a], vals[b], d + 1, d - 1 if d > 1 else d + 2],
               "%d and %d. The %s row has <b>%d</b> more." % (vals[a], vals[b], name(ks[a], 1), d))


def build():
    sets = [S("Sort and count", collect(one_count, 20, R)),
            S("Sorting rules", collect(one_rule, 20, R)),
            S("Read a concrete graph", collect(one_read, 20, R)),
            S("Compare the groups", collect(one_compare, 20, R)),
            S("Picture graphs and questions", collect(one_pict, 20, R))]
    finish(sets, R, max_num=10)
    ctx = g1.BYKEY["boots"]
    body = lesson(
        "<ul><li><b>Sort</b> the things into groups with one rule, like colour or kind.</li>"
        "<li>Make a <b>concrete graph</b>: put each group in a row or a tower. Start every row at the same line.</li>"
        "<li>1 cube or 1 picture is 1. Count each row.</li>"
        "<li>The longest row or tallest tower has the <b>most</b>. The shortest has the <b>fewest</b>.</li></ul>",
        [figure(g1.tower_graph(ctx, ["Red", "Blue", "Yellow"], [5, 3, 6]), "Yellow has the most (6). Blue has the fewest (3)."),
         figure(g1.row_graph(ctx, ["Red", "Blue", "Yellow"], [5, 3, 6]), "The same data in rows. Red has 2 more than blue.")],
        [["Counting all the things, not one kind", "Sort first. Count only one group."],
         ["Not starting at the same line", "Line up every row at the start, then compare."],
         ["Giving one number for how many more", "Match the rows up and count the extra ones."]])
    faq = [("What is a concrete graph?", "A graph made with real objects, such as cubes, toys or shoes, put in rows or towers so children can count and compare them."),
           ("What is a pictorial graph?", "A graph where each picture stands for one thing, such as one vote. It is the next step after a concrete graph."),
           ("How does a graph help?", "It shows the groups side by side, so you can see which has the most, which has the fewest, and how many more."),
           ("How can I make a graph at home?", "Sort socks, toy cars or snacks into groups, line each group up from one edge, and count each row.")]
    make("concrete-graphs", 10, "Data and probability", "Concrete Graphs: Sort, Count and Compare", "Concrete graphs",
         "Concrete or pictorial graphs as a visual tool for collecting and representing data: collecting data, creating a concrete graph, and describing, comparing, and discussing the findings",
         "Free Kindergarten math worksheets on concrete graphs for the BC curriculum: sort and count, sorting rules, cube rows and towers, compare groups and picture graphs. 100 picture questions with answers.",
         "Line the groups up at one start line, then count and compare.", "1 cube or 1 picture is 1. The longest row has the most.",
         body, faq, sets)


if __name__ == "__main__":
    build()
