# -*- coding: utf-8 -*-
"""
US Kindergarten Science: How Living Things Change Their Environment (K-ESS2-2)
  python tools/gen_us_science_gk_how_living_things_change_their_environment.py
Construct an argument supported by evidence for how plants and animals (including humans) can change the environment
to meet their needs. Squirrels dig to bury nuts, beavers build dams, birds build nests, worms dig tunnels, tree roots crack
sidewalks, people cut trees and build houses and roads. Very short sentences; almost every question has a picture.
Wrong answers come from real mistakes: "only people change the land", "plants cannot change anything", "animals build things for fun".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, People
import sci_kids as K

U = Unit(9107)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# who, picture, what it does, need it meets, evidence you could see
CH = [("a squirrel", "squirrel", "digs holes to bury nuts", "food", "little holes in the yard"),
      ("a bird", "bird", "builds a nest in a tree", "a home", "a nest made of twigs"),
      ("a beaver", None, "builds a dam of sticks across a stream", "a home", "a pile of sticks blocking a stream"),
      ("a worm", "worm", "digs tunnels in the soil", "a home and food", "small tunnels and loose soil"),
      ("a tree", "tree", "grows roots that crack a sidewalk", "water", "a sidewalk lifted and cracked"),
      ("a rabbit", "rabbit", "digs a burrow in the ground", "a home", "a hole in the ground with dirt around it"),
      ("people", "house", "cut down trees to build houses", "a home", "stumps where trees were"),
      ("a bear", "bear", "tears open a log to find bugs", "food", "a log ripped apart"),
      ("ants", None, "build an anthill", "a home", "a small hill of sand"),
      ("a bee", "bee", "builds a hive", "a home", "a hive full of wax rooms"),
      ("people", None, "plant a garden", "food", "rows of vegetables"),
      ("a deer", None, "eats the leaves off low branches", "food", "bushes with no low leaves"),
      ("a plant", "sprout", "grows through a crack in the pavement", "light and water", "a plant poking out of the pavement"),
      ("a dog", "dog", "digs a hole to bury a bone", "food", "a hole with a bone in it")]


def base(x):
    w, rest = x.split(" ", 1)
    return {"digs": "dig", "builds": "build", "grows": "grow", "tears": "tear", "eats": "eat"}.get(w, w) + " " + rest


def g_how():
    w, pic, does, need, ev = R.choice(CH)
    who = P.next()[0]
    if not once(("h", w, does)):
        return None
    fg = fig(K.card(pic)) if pic else ""
    wrongs = R.sample(sorted({base(x[2]) for x in CH if base(x[2]) != base(does)}), 3)
    return item(fg + "%s wonders: what %s %s do that changes the land?" % (who, "do" if w in ("people", "ants") else "does", w), base(does), wrongs,
                "%s %s." % (w[0].upper() + w[1:], does))


NEEDS = ["food", "a home", "water", "light and water", "a home and food"]


def g_why():
    w, pic, does, need, ev = R.choice(CH)
    who = P.next()[0]
    if not once(("y", w, does)):
        return None
    fg = fig(K.card(pic)) if pic else ""
    sub = "they" if w in ("people", "ants") else "it"
    wr = [x for x in ["food", "a home", "water", "sunlight"] if x not in need and not (x == "sunlight" and "light" in need)][:2] + ["fun only"]
    return item(fg + "%s reads: %s %s. Why?" % (who, w[0].upper() + w[1:], does), "%s need%s %s." % (sub.capitalize(), "" if sub == "they" else "s", need),
                ["%s need%s %s." % (sub.capitalize(), "" if sub == "they" else "s", x) if x != "fun only" else "%s do%s it just for fun." % (sub.capitalize(), "" if sub == "they" else "es") for x in wr][:3],
                "Living things change their environment to meet their needs.")


def g_ev():
    w, pic, does, need, ev = R.choice(CH)
    who = P.next()[0]
    if not once(("e", ev)):
        return None
    near = {"a squirrel": {"a dog", "a rabbit", "a worm"}, "a bird": {"a squirrel"}, "a dog": {"a squirrel", "a rabbit"}, "a rabbit": {"a squirrel", "a dog", "ants"},
            "ants": {"a rabbit", "a worm"}, "a worm": {"ants", "a rabbit"}}.get(w, set())
    wrongs = R.sample(sorted({x[0] for x in CH if x[0] != w and x[4] != ev and x[0] not in near}), 3)
    return item("%s finds %s. Who most likely made this change?" % (who, ev), w, wrongs, "%s %s." % (w[0].upper() + w[1:], does))


def g_pick():
    opts = [("bird", "builds a nest"), ("squirrel", "buries nuts"), ("tree", "cracks a sidewalk with its roots"), ("worm", "digs tunnels in soil"),
            ("bee", "builds a hive"), ("rabbit", "digs a burrow"), ("dog", "digs a hole for a bone")]
    kinds = R.sample(opts, 4)
    a = R.choice(kinds)
    if not once((tuple(k[0] for k in kinds), a[0])):
        return None
    L = "ABCD"
    who = P.next()[0]
    pic = K.row([k[0] for k in kinds], words=["%s. %s" % (L[i], k[0]) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s looks at these. Which one %s?" % (who, a[1]), "%s (%s)" % (L[kinds.index(a)], a[0]), ["%s (%s)" % (L[i], k[0]) for i, k in enumerate(kinds) if k != a],
                "The %s %s." % (a[0], a[1]))


PEOPLE = [("build a bridge over a river", "to get across"), ("dig a well", "to get water"), ("plant rows of corn", "to grow food"),
          ("build a house", "to have a home"), ("pave a road", "to travel"), ("build a fence around a farm", "to keep animals in"),
          ("cut a path through the woods", "to walk easily"), ("build a dam to make a lake", "to store water")]


def g_people():
    a, why = R.choice(PEOPLE)
    who = P.next()[0]
    if not once(a):
        return None
    return item("%s sees people %s. Why do they do it?" % (who, a), why, R.sample([x[1] for x in PEOPLE if x[1] != why], 3), "People change the land to meet their needs.")


B1 = bank([
    ("Can animals change the land?", "Yes. They dig, build and move things.", ["No, never.", "Only people can.", "Only plants can."], "Animals change places to live."),
    ("Can plants change the land?", "Yes. Roots can crack rocks and sidewalks.", ["No, plants do nothing.", "Only flowers can.", "Only in winter."], "Roots push and grow."),
    ("Why does a bird build a nest?", "to have a home for its eggs", ["to play", "to make it rain", "to scare people"], "A nest is a home."),
    ("Why does a squirrel dig holes?", "to bury nuts for food", ["to find toys", "to make a pool", "to sleep in"], "Food for later."),
    ("How do people change the land?", "They build houses, roads and farms.", ["They never change it.", "They only watch it.", "They make it rain."], "People meet their needs too."),
    ("What does a beaver build?", "a dam", ["a nest in a tree", "an anthill", "a hive"], "Beavers block streams."),
    ("What do worms do to the soil?", "dig tunnels", ["build nests", "make dams", "freeze it"], "Worms make tunnels."),
    ("Why do plants grow toward the light?", "to get the sunlight they need", ["to see the sky", "to scare bugs", "to get cold"], "Plants need light."),
])
B5 = bank([
    ("Ava sees a cracked sidewalk with a big tree next to it. What caused the crack?", "the tree's growing roots", ["a worm", "the rain", "a bird"], "Roots push up the sidewalk."),
    ("Leo sees a pile of sticks blocking a stream. What is his evidence?", "A beaver built a dam.", ["The wind piled sticks.", "A fish built it.", "It fell from the sky."], "Beavers build dams."),
    ("Mia sees many holes in the lawn in the fall. Which animal might it be?", "a squirrel burying nuts", ["a fish", "a bird building a nest", "a bee"], "Squirrels dig."),
    ("Kai's town cuts down trees to build a school. How did people change the land?", "They cleared the trees to make room.", ["They planted more trees.", "They made a river.", "They did not change it."], "People change land too."),
    ("Why might a prairie dog dig a big burrow?", "to have a safe home", ["to find candy", "to make it hot", "to stay in the sun"], "A burrow is shelter."),
])


def body():
    pic = K.row(["bird", "squirrel", "tree", "house"], words=["builds a nest", "digs holes", "roots crack rock", "people build"], size=110)
    ex = [("A bird builds a nest. Why?", ["It needs a home."], "for a home"),
          ("A sidewalk is cracked by a tree. How?", ["Roots grow and push."], "the roots")]
    mist = ["Thinking only people change the land.",
            "Thinking plants cannot change anything.",
            "Thinking animals build things only for fun."]
    return kid_lesson(pic, "Living things change where they live.",
                      ["Animals dig and build homes.", "Plant roots can crack rocks.", "People build houses and farms."], ex, mist)


def main():
    sets = U.sets([
        ("Changing the land", B1 + [(g_how, 6), (g_pick, 6)]),
        ("How do they change it?", [(g_how, 8), (g_pick, 6), (g_why, 6)]),
        ("Why do they change it?", [(g_why, 8), (g_ev, 6), (g_people, 6)]),
        ("Find the evidence", [(g_ev, 8), (g_pick, 10), (g_people, 2)]),
        ("Land changers", B5 + [(g_pick, 15)]),
    ])
    make("kindergarten", "how-living-things-change-their-environment", 7, "K-ESS2-2",
         "Construct an argument supported by evidence for how plants and animals (including humans) can change the environment to meet their needs.",
         "Living Things Change Their Environment",
         "Kindergarten Worksheets: How Plants and Animals Change Their Environment",
         "Changing the Environment",
         "Free kindergarten science worksheets (NGSS K-ESS2-2): how squirrels, beavers, birds, worms, tree roots and people change the land to meet their needs. 100 picture questions with answers.",
         "Living things change the land.",
         "Animals dig and build. Roots crack rock. People build too.",
         body(),
         [("How do animals change their environment?", "Squirrels dig holes for nuts, birds build nests, beavers build dams and worms dig tunnels."),
          ("Can plants change the environment?", "Yes. Tree roots can crack sidewalks and rocks as they grow."),
          ("Why do living things change the land?", "To meet their needs: food, water and a safe home.")],
         sets)


if __name__ == "__main__":
    main()
