# -*- coding: utf-8 -*-
"""
UK Year 1 science: Deciduous and Evergreen Trees (Plants)
  python tools/gen_uk_science_y1_deciduous_and_evergreen_trees.py
Identify and name common deciduous and evergreen trees: trees that lose their leaves in autumn and trees that keep
them all year, naming trees from their leaves, seeds and fruits (acorns, conkers, helicopter seeds, holly berries,
pine cones), the parts of a tree, and a tree survey.
Wrong answers come from real mistakes: "evergreen trees never lose any leaves", "a deciduous tree is dead in winter",
"conkers come from oak trees", "pine needles are not leaves".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61102)
R = U.R
P = People(R)

DEC = ["an oak tree", "a beech tree", "a horse chestnut tree", "a sycamore tree", "an ash tree", "a silver birch", "an apple tree", "a cherry tree", "a willow tree"]
EVG = ["a holly tree", "a pine tree", "a fir tree", "a yew tree", "a Christmas tree (spruce)", "a cedar tree", "a Scots pine", "a monkey puzzle tree"]
DEF = {"deciduous": "loses its leaves in autumn and grows new ones in spring", "evergreen": "keeps its leaves all year round"}


def g_type():
    k = R.random() < 0.5
    t = R.choice(DEC if k else EVG)
    if not once(("ty", t)):
        return None
    a = "deciduous" if k else "evergreen"
    return item("Is %s deciduous or evergreen?" % t, a, ["evergreen" if k else "deciduous", "a flower", "a weed"], "A %s tree %s." % (a, DEF[a]))


def g_pick():
    k = R.random() < 0.5
    pool, other = (DEC, EVG) if k else (EVG, DEC)
    a = R.choice(pool)
    if not once(("pk", a)):
        return None
    w = R.sample(other, 3)
    o = sorted([a] + w)
    return item("Which of these trees is %s: %s or %s?" % ("deciduous" if k else "evergreen", ", ".join(o[:3]), o[3]), a, w, "Deciduous trees lose their leaves in autumn; evergreens keep them.")


SEED = [("acorns", "an oak tree"), ("conkers", "a horse chestnut tree"), ("helicopter seeds that spin", "a sycamore tree"), ("red berries and prickly leaves", "a holly tree"),
        ("pine cones and long needles", "a pine tree"), ("apples", "an apple tree"), ("cherries in summer and pink blossom in spring", "a cherry tree"),
        ("beech nuts in spiky cases", "a beech tree"), ("bunches of keys (winged seeds)", "an ash tree"), ("white, papery bark", "a silver birch")]


def g_seed():
    s, t = R.choice(SEED)
    k = R.random() < 0.5
    if not once(("se", s, k)):
        return None
    if k:
        return item("Which tree has %s?" % s, t, R.sample([x[1] for x in SEED if x[1] != t], 3), "Seeds, fruits, leaves and bark help us name trees.")
    return item("What could you find on %s?" % t, s, R.sample([x[0] for x in SEED if x[0] != s], 3), "Seeds, fruits, leaves and bark help us name trees.")


PART = [("the trunk", "the thick, woody stem that holds the tree up"), ("the branches", "the arms of the tree that hold the leaves"), ("the bark", "the tough outer skin of the trunk"),
        ("the roots", "the parts under the ground that take in water"), ("the leaves", "the parts that use sunlight to make food"), ("the blossom", "the flowers of the tree")]


def g_part():
    p, d = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    if k:
        return item("What is %s of a tree?" % p, d, R.sample([x[1] for x in PART if x[1] != d], 3), "A tree has roots, a trunk, branches, leaves and often blossom.")
    return item("Which part of a tree is %s?" % d, p, R.sample([x[0] for x in PART if x[0] != p], 3), "A tree has roots, a trunk, branches, leaves and often blossom.")


def g_survey():
    who = P.next()[0]
    trees = R.sample(["oak", "holly", "sycamore", "pine", "beech", "yew", "birch", "fir"], 4)
    v = R.sample(range(1, 9), 4)
    evg = {"holly", "pine", "yew", "fir"}
    k = R.choice(["most", "read", "evg", "dec"])
    ri = R.randrange(4)
    if not once(("su", tuple(trees), tuple(v), k)):
        return None
    tab = table(["Tree", "Number in the park"], [[t, str(x)] for t, x in zip(trees, v)])
    intro = tab + "%s counted the trees in the park. " % who
    if k == "most":
        a = trees[v.index(max(v))]
        return item(intro + "Which tree was there most of?", a, [x for x in trees if x != a], "The biggest number.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many %s trees were there?" % trees[ri], g, [str(x) for x in v if x != v[ri]][:3], "Read the row.")
    if k == "evg":
        n = sum(x for t, x in zip(trees, v) if t in evg)
        if n == 0:
            return None
        g = str(n)
        w = list(dict.fromkeys([str(sum(v)), str(sum(v) - n), str(n + 1), str(max(0, n - 1))]))
        return item(intro + "How many evergreen trees were there altogether?", g, [x for x in w if x != g][:3], "Holly, pine, yew and fir are evergreen. Add them up.")
    n = sum(x for t, x in zip(trees, v) if t not in evg)
    if n == 0:
        return None
    g = str(n)
    w = list(dict.fromkeys([str(sum(v)), str(sum(v) - n), str(n + 1), str(max(0, n - 1))]))
    return item(intro + "How many deciduous trees were there altogether?", g, [x for x in w if x != g][:3], "Oak, sycamore, beech and birch are deciduous. Add them up.")


B1 = bank([
    ("What does deciduous mean?", "loses its leaves in autumn", ["keeps its leaves all year", "has no leaves ever", "grows only in summer"], "Bare branches in winter."),
    ("What does evergreen mean?", "keeps its leaves all year round", ["loses all its leaves in autumn", "is always flowering", "is made of plastic"], "Green in winter."),
    ("Which tree is green all through winter?", "a holly tree", ["an oak tree", "a horse chestnut tree", "a sycamore tree"], "Holly is evergreen."),
    ("What happens to an oak tree's leaves in autumn?", "They turn brown and fall off.", ["They stay green all winter.", "They turn into acorns.", "They grow bigger."], "Oaks are deciduous."),
    ("Are pine needles leaves?", "Yes. They are thin, tough leaves.", ["No, they are seeds.", "No, they are bark.", "No, they are flowers."], "Needle-shaped leaves."),
    ("Is a deciduous tree dead in winter?", "No. It is resting and will grow new leaves in spring.", ["Yes, it has died.", "Yes, until it is replanted.", "It turns into an evergreen."], "Alive but bare."),
    ("Where do conkers come from?", "a horse chestnut tree", ["an oak tree", "a pine tree", "a holly tree"], "Shiny brown seeds."),
    ("Where do acorns come from?", "an oak tree", ["a horse chestnut tree", "an apple tree", "a fir tree"], "Little cups."),
])
B5 = bank([
    ("Do evergreen trees ever lose leaves?", "Yes, a few at a time all through the year, but never all at once.", ["No, never a single leaf.", "Yes, all in autumn.", "Only when they are cut down."], "Always green."),
    ("Why do deciduous trees look bare in winter?", "They dropped their leaves in autumn.", ["Someone cut the leaves off.", "The leaves turned into snow.", "They are dead."], "Seasonal change."),
    ("How could you tell an oak from a holly in winter?", "The holly still has green leaves; the oak is bare.", ["They look exactly the same.", "The oak has red berries.", "The holly has acorns."], "Observe."),
    ("How could you find out which trees grow in the school grounds?", "Walk round, look at leaves and bark, and record each tree.", ["Guess.", "Cut them all down.", "Look at one tree only."], "Tree survey."),
    ("Why do birds like holly trees in winter?", "They give berries to eat and leafy shelter.", ["Holly is warm like a fire.", "Birds eat holly leaves.", "There is no reason."], "Food and shelter."),
])


def body():
    pic = K.row(["tree", "tree"], words=["deciduous (oak)", "evergreen (holly)"], size=90, label="a deciduous tree and an evergreen tree")
    ex = [("An oak in winter?", ["It loses its leaves in autumn"], "bare: deciduous"),
          ("A pine in winter?", ["It keeps its needles"], "green: evergreen")]
    mist = ["Thinking evergreen trees never lose a single leaf.", "Thinking a bare tree in winter is dead.", "Thinking conkers come from oak trees."]
    return kid_lesson(pic, "Deciduous trees lose their leaves in autumn.",
                      ["Evergreen trees keep their leaves all year.", "Oak, beech and sycamore are deciduous.", "Holly, pine and fir are evergreen."], ex, mist)


def main():
    sets = U.sets([
        ("Deciduous or evergreen?", B1 + [(g_type, 12)]),
        ("Which tree?", [(g_type, 5), (g_pick, 10), (g_part, 5)]),
        ("Seeds, fruits and leaves", [(g_seed, 14), (g_part, 6)]),
        ("Tree survey", [(g_survey, 16), (g_seed, 4)]),
        ("Thinking about trees", B5 + [(g_survey, 9), (g_pick, 6)]),
    ])
    make_uk(1, "deciduous-and-evergreen-trees", 2, "Plants",
            "Identify and name a variety of common wild and garden plants, including deciduous and evergreen trees.",
            "Deciduous and Evergreen Trees",
            "Year 1 Science: Deciduous and Evergreen Trees Worksheets (Naming Trees)",
            "Trees",
            "Free Year 1 science worksheets on trees: deciduous and evergreen trees, naming trees from acorns, conkers, cones and leaves, the parts of a tree and a tree survey. 100 questions with answers.",
            "Deciduous trees lose their leaves.",
            "Evergreen trees keep their leaves all year round.",
            body(),
            [("What is a deciduous tree?", "A tree that loses its leaves in autumn and grows new ones in spring, such as an oak, beech or sycamore."),
             ("What is an evergreen tree?", "A tree that keeps its leaves all year, such as a holly, pine or fir. It drops a few old leaves at a time, never all at once."),
             ("How can we name a tree?", "Look at its leaves, bark, seeds and fruits. Acorns come from oaks, conkers from horse chestnuts and cones from pines.")],
            sets)


if __name__ == "__main__":
    main()
