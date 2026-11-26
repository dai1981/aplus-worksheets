# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Caring for Earth (K-ESS3-3)
  python tools/gen_us_science_gk_caring_for_earth.py
Communicate solutions that will reduce the impact of humans on the land, water, air, and/or other living things in the
local environment. Reduce, reuse and recycle; turn off water and lights; pick up litter; plant trees; walk or bike;
compost food scraps. Very short sentences for 5-6 year olds; most questions have a picture.
Wrong answers come from real mistakes: "throwing trash on the ground is OK if it is small", "leave the water running",
"everything goes in the trash".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, People
import sci_kids as K

U = Unit(9110)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ACTS = [("turns off the water while brushing teeth", True), ("picks up litter at the park", True), ("plants a tree", True), ("turns off the lights when leaving a room", True),
        ("rides a bike to school", True), ("uses both sides of the paper", True), ("brings a cloth bag to the store", True), ("puts food scraps in a compost bin", True),
        ("recycles a can", True), ("fills a reusable water bottle", True),
        ("throws a wrapper on the ground", False), ("leaves the water running", False), ("leaves the TV on all night", False), ("throws a bottle in the lake", False),
        ("breaks branches off a young tree", False), ("uses a new paper plate for every snack", False), ("pours paint down the storm drain", False)]


def g_help():
    a, good = R.choice(ACTS)
    who = P.next()[0]
    if not once(a):
        return None
    return item("%s %s. Does this help Earth or hurt Earth?" % (who, a), "It helps Earth." if good else "It hurts Earth.",
                ["It hurts Earth." if good else "It helps Earth.", "It does not matter at all.", "It makes it rain."], "Small actions add up.")


BINS = {"paper": "recycle", "cup": "recycle", "apple": "compost", "leaf": "compost", "sock": "reuse", "crayon": "reuse", "spoon": "reuse"}
BIN_NM = {"paper": "a torn, used paper", "cup": "a cracked plastic cup", "apple": "an apple core", "leaf": "dry leaves", "sock": "an old sock", "crayon": "a broken crayon", "spoon": "a metal spoon"}
WHERE = {"recycle": "the recycling bin", "compost": "the compost bin", "reuse": "keep it and use it again"}


def g_bin():
    k = R.choice(sorted(BINS))
    who = P.next()[0]
    if not once(("b", k)):
        return None
    a = WHERE[BINS[k]]
    w = {"recycle": [WHERE["compost"], "throw it on the ground", "throw it in the lake"], "compost": [WHERE["recycle"], "throw it on the ground", "throw it in the lake"],
         "reuse": [WHERE["compost"], "throw it on the ground", "throw it in the lake"]}[BINS[k]]
    return item(fig(K.card(k)) + "%s is done with %s. What is the best thing to do?" % (who, BIN_NM[k]), a, w,
                "Recycle, compost or reuse instead of making trash.")


REUSE = [("an empty jar", "a pencil holder"), ("a cardboard box", "a toy house"), ("an old T-shirt", "a cleaning rag"), ("a milk jug", "a bird feeder"),
         ("an egg carton", "a seed starter"), ("a paper towel tube", "a toy telescope"), ("a cloth bag", "a shopping bag again"), ("old socks", "sock puppets")]


def g_reuse():
    o, use = R.choice(REUSE)
    who = P.next()[0]
    if not once(o):
        return None
    return item("%s wants to reuse %s. What could it become?" % (who, o), use, R.sample([x[1] for x in REUSE if x[1] != use], 3), "Reusing means using it again in a new way.")


PROB = [("There is trash all over the playground.", "pick it up and put it in a trash can"), ("Water drips from the sink all day.", "turn the tap off tight and fix it"),
        ("Cars make smoke near the school.", "walk or bike when you can"), ("Birds have fewer trees to nest in.", "plant more trees"),
        ("The trash can is full of paper.", "recycle the paper instead"), ("Lunch scraps go in the trash.", "compost the food scraps"),
        ("Plastic bags blow into the creek.", "use cloth bags"), ("Lights are on in an empty classroom.", "turn the lights off")]


def g_prob():
    p, a = R.choice(PROB)
    who = P.next()[0]
    if not once(p):
        return None
    return item("%s sees a problem. %s What can %s's class do?" % (who, p, who), a, R.sample([x[1] for x in PROB if x[1] != a], 2) + ["nothing; it is fine"],
                "We can solve problems to care for Earth.")


def g_pick():
    good = R.choice([("paper", "can be recycled"), ("cup", "can be recycled"), ("apple", "can go in the compost"), ("leaf", "can go in the compost")])
    others = [("rock", None), ("drum", None), ("hat", None), ("ball", None)]
    kinds = [good[0]] + [o[0] for o in R.sample(others, 3)]
    R.shuffle(kinds)
    if not once((tuple(kinds), good[0])) or not once(("pk", good[0]), 5):
        return None
    L = "ABCD"
    who = P.next()[0]
    nm = {"paper": "paper", "cup": "plastic cup", "apple": "apple core", "leaf": "leaf", "rock": "rock", "drum": "toy drum", "hat": "hat", "ball": "ball"}
    pic = K.row(kinds, words=["%s. %s" % (L[i], nm[k]) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s cleans up. Which one %s?" % (who, good[1]), "%s (%s)" % (L[kinds.index(good[0])], nm[good[0]]),
                ["%s (%s)" % (L[i], nm[k]) for i, k in enumerate(kinds) if k != good[0]], "The %s %s." % (nm[good[0]], good[1]))


def g_better():
    g = R.choice([x for x in ACTS if x[1]])
    b = R.choice([x for x in ACTS if not x[1]])
    who = P.next()[0]
    if not once((g[0], b[0])) or not once("better", 40) or not once(("bg", g[0]), 6):
        return None
    x, y = (g, b) if R.random() < 0.5 else (b, g)
    return item("Which choice is better for Earth?<br>1. %s %s.<br>2. %s %s." % (who, x[0], who, y[0]), "%d" % (1 if x is g else 2),
                ["%d" % (2 if x is g else 1), "Both are the same.", "Neither one matters."], "%s %s. That helps Earth." % (who, g[0]))


B1 = bank([
    ("What does recycle mean?", "make old things into new things", ["throw things away", "burn things", "hide things"], "Cans and paper can be made new."),
    ("What does reuse mean?", "use something again", ["throw it out", "break it", "buy a new one"], "Use it again."),
    ("What does reduce mean?", "use less", ["use more", "throw more away", "buy more"], "Use less water, paper and power."),
    ("Where should a banana peel go?", "the compost bin", ["the street", "the lake", "the recycling bin for cans"], "Food scraps become soil."),
    ("How can you save water?", "turn off the tap when you brush", ["leave it running", "take very long baths", "spray the sidewalk"], "Use less water."),
    ("How can you help the air stay clean?", "walk or bike instead of driving", ["leave the car running", "burn trash", "drive everywhere"], "Less smoke."),
    ("What should you do with litter you see at the park?", "pick it up and throw it away safely", ["kick it", "leave it", "throw more"], "Keep land clean."),
    ("Why do we plant trees?", "Trees give homes to animals and clean the air.", ["Trees make trash.", "Trees make noise.", "Trees are not useful."], "Trees help Earth."),
])
B5 = bank([
    ("Ava's class makes a poster to save water. What should it say?", "Turn off the tap!", ["Leave the water on!", "Use more water!", "Water the sidewalk!"], "Share solutions."),
    ("Leo finds a plastic bottle by the creek. What should he do?", "pick it up and recycle it", ["throw it in the creek", "leave it", "bury it in the sand"], "Keep water clean."),
    ("Mia uses a cloth bag at the store. How does this help?", "It means fewer plastic bags.", ["It makes more trash.", "It uses more paper.", "It does not help."], "Reusing reduces trash."),
    ("Kai's family puts food scraps in a compost bin. What does the compost become?", "rich soil for plants", ["plastic", "trash", "metal"], "Compost feeds gardens."),
    ("Zoe turns off the lights when she leaves. What does she save?", "electricity (energy)", ["water", "paper", "food"], "Less power used."),
])


def body():
    pic = K.row(["paper", "apple", "tree", "drop"], words=["recycle", "compost", "plant trees", "save water"], size=100)
    ex = [("Where does used paper go?", ["Paper can be made new."], "the recycling bin"),
          ("Water is running while you brush. What should you do?", ["Use less water."], "turn it off")]
    mist = ["Thinking small trash on the ground is OK.",
            "Leaving the water running.",
            "Putting everything in the trash."]
    return kid_lesson(pic, "We can take care of Earth.",
                      ["Reduce: use less.", "Reuse: use it again. Recycle: make it new.", "Pick up litter and plant trees."], ex, mist)


def main():
    sets = U.sets([
        ("Helping Earth", B1 + [(g_help, 6), (g_bin, 6)]),
        ("Help or hurt?", [(g_help, 11), (g_pick, 5), (g_reuse, 4)]),
        ("Reduce, reuse, recycle", [(g_reuse, 4), (g_pick, 8), (g_prob, 4), (g_better, 4)]),
        ("Solving problems", [(g_prob, 4), (g_better, 10), (g_pick, 6)]),
        ("Earth helpers", B5 + [(g_better, 14), (g_bin, 1)]),
    ])
    make("kindergarten", "caring-for-earth", 10, "K-ESS3-3",
         "Communicate solutions that will reduce the impact of humans on the land, water, air, and/or other living things in the local environment.",
         "Caring for Earth",
         "Kindergarten Caring for Earth Worksheets: Reduce, Reuse, Recycle",
         "Caring for Earth",
         "Free kindergarten science worksheets on caring for Earth (NGSS K-ESS3-3): reduce, reuse and recycle, saving water and energy, and solving problems in your neighborhood. 100 picture questions with answers.",
         "We can take care of Earth.",
         "Reduce, reuse, recycle. Save water. Pick up litter.",
         body(),
         [("What do reduce, reuse and recycle mean?", "Reduce means use less, reuse means use something again, and recycle means make old things into new things."),
          ("How can kids help Earth?", "Turn off water and lights, pick up litter, plant trees, compost food scraps and use cloth bags."),
          ("Why does it matter?", "People change the land, water and air. Small choices help keep them clean for people, plants and animals.")],
         sets)


if __name__ == "__main__":
    main()
