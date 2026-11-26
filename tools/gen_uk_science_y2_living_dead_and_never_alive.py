# -*- coding: utf-8 -*-
"""
UK Year 2 science: Living, Dead and Never Alive (Living things and their habitats)
  python tools/gen_uk_science_y2_living_dead_and_never_alive.py
Explore and compare things that are living, dead, and things that have never been alive. What living things do
(move, breathe, feed, grow, have young), and sorting objects into the three groups.
Wrong answers come from real mistakes: "things that move are alive" (a car), "plants are not alive",
"a wooden table was never alive", "fire is alive".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, People, once
from uk_ks1 import card, row, which_of
import sci_kids as K

U = Unit(61201)
R = U.R
P = People(R)

ALIVE = ["a dog", "an oak tree", "a daisy", "a goldfish", "a ladybird", "a rabbit", "a sunflower", "a robin", "a worm", "a frog", "a growing tomato plant", "a horse"]
DEAD = ["a wooden table", "a dead leaf", "a feather that fell off a bird", "a paper book", "a woolly jumper", "a cotton T-shirt", "a leather shoe", "a fallen log",
        "a seashell on the beach", "a twig on the ground", "a cardboard box", "a bone"]
NEVER = ["a rock", "a plastic bottle", "a metal spoon", "a glass marble", "a brick", "a puddle of water", "a toy car", "a coin", "a lump of clay", "a pebble", "a steel can", "a plastic ball"]
G = {"alive": "living (alive now)", "dead": "dead (was once alive)", "never": "never alive"}
WHY = {"alive": "It is living: it can feed, grow and breathe.", "dead": "It came from something that was once alive.", "never": "It was never part of a living thing."}


def g_sort():
    k = R.choice(["alive", "dead", "never"])
    x = R.choice({"alive": ALIVE, "dead": DEAD, "never": NEVER}[k])
    if not once(("so", x)):
        return None
    return item("Is %s living, dead or never alive?" % x, G[k], [G[y] for y in G if y != k] + ["a light source"], WHY[k])


def g_pick():
    k = R.choice(["alive", "dead", "never"])
    pools = {"alive": ALIVE, "dead": DEAD, "never": NEVER}
    other = [x for y in pools if y != k for x in pools[y]]
    q = {"alive": "Which of these is living", "dead": "Which of these is dead (was once alive)", "never": "Which of these was never alive"}[k]
    return which_of(R, once, "pk" + k, q, pools[k], other, WHY[k])


PROC = [("move", "Living things can move by themselves. Plants move slowly, for example turning to the light."), ("breathe", "Living things take in air."),
        ("feed", "Living things need food. Plants make their own."), ("grow", "Living things get bigger as they get older."), ("have young", "Living things make new living things like them.")]


def g_proc():
    p, e = R.choice(PROC)
    k = R.random() < 0.5
    if not once(("pr", p, k)):
        return None
    if k:
        return item("Which of these do ALL living things do?", p, R.sample(["talk", "walk on legs", "have fur", "fly", "swim", "eat meat"], 3), e)
    who = P.next()[0]
    return item("%s says a toy robot is alive because it moves. What is wrong?" % who if p == "move" else "A rock cannot %s. What does this tell us?" % p,
                "A robot cannot feed, grow or have young, so it is not alive." if p == "move" else "A rock is not alive.",
                ["Robots are alive because they move." if p == "move" else "A rock is alive.", "Everything that moves is alive.", "Only animals are alive."], e)


TRICK = [("A car moves. Is it alive?", "No. It cannot feed, grow or have young.", ["Yes, because it moves.", "Yes, because it is loud.", "Yes, at night."]),
         ("A tree does not walk. Is it alive?", "Yes. It feeds, grows and makes seeds.", ["No, because it cannot walk.", "No, it is wood.", "Only in summer."]),
         ("Fire grows and moves. Is it alive?", "No. It does not feed, breathe and have young like living things.", ["Yes, because it grows.", "Yes, because it is hot.", "Yes, because it moves."]),
         ("A wooden chair was made from a tree. Which group is it in?", "dead (was once alive)", ["living", "never alive", "a light source"]),
         ("A seed looks like a tiny stone. Is it alive?", "Yes. It can grow into a new plant.", ["No, it is a stone.", "No, it is dead.", "It was never alive."]),
         ("A cloud moves across the sky. Is it alive?", "No. It is made of water, which was never alive.", ["Yes, because it moves.", "Yes, because it grows.", "Yes, because it rains."]),
         ("A bird's feather fell on the grass. Which group is the feather in?", "dead (was once alive)", ["living", "never alive", "a plant"]),
         ("A woolly jumper is made from sheep's wool. Which group is it in?", "dead (was once alive)", ["living", "never alive", "a rock"])]


def g_trick():
    q, a, w = R.choice(TRICK)
    if not once(("tr", q)):
        return None
    return item(q, a, w, "Living things move, breathe, feed, grow and have young. Things that only move are not alive.")


PICK = [("dog", "living"), ("tree", "living"), ("bird", "living"), ("frog", "living"), ("rabbit", "living"), ("bee", "living"), ("flower", "living"),
        ("rock", "never alive"), ("spoon", "never alive"), ("ball", "never alive"), ("cube", "never alive"), ("button", "never alive")]


def g_picture():
    kind, a = R.choice(PICK)
    if not once(("pi", kind)):
        return None
    from uk_ks1 import name
    return item(card(kind) + "Look at the %s. Is it living or never alive?" % name(kind), a, ["never alive" if a == "living" else "living", "dead", "a light source"],
                "Living things feed, grow and have young.")


B1 = bank([
    ("What does 'living' mean?", "alive now: it feeds, grows, breathes and has young", ["it is very old", "it is hard", "it is made in a factory"], "Animals and plants are living."),
    ("What does 'dead' mean?", "it was once alive but is not alive now", ["it was never alive", "it is sleeping", "it is very small"], "A dead leaf was once alive."),
    ("What does 'never alive' mean?", "it has never been part of a living thing", ["it died a long time ago", "it is asleep", "it is a baby"], "Rocks and plastic were never alive."),
    ("Are plants alive?", "Yes. They feed, grow and make seeds.", ["No, because they cannot walk.", "Only flowers are alive.", "No, plants are like rocks."], "Plants are living things."),
    ("Paper is made from trees. Which group is paper in?", "dead (was once alive)", ["living", "never alive", "a light source"], "Trees were once alive."),
    ("Which group is a rock in?", "never alive", ["living", "dead", "a plant"], "Rocks are not part of living things."),
    ("Do all living things need food?", "Yes. Animals eat; plants make their own food.", ["No, only animals.", "No, only plants.", "No, none of them."], "All living things feed."),
    ("Do all living things grow?", "Yes. They get bigger as they get older.", ["No, only people.", "No, only trees.", "No, living things stay the same."], "Growing is a sign of life."),
])
B5 = bank([
    ("A shell is found on the beach. Why is it in the 'dead' group?", "It was part of a living sea animal.", ["It was never alive.", "It is still alive.", "It is a rock."], "Shells come from animals."),
    ("Why is a toy that walks and talks not alive?", "It cannot feed, grow or have young.", ["It is too small.", "It is the wrong colour.", "It is alive."], "Check all the signs."),
    ("A log in a wood has mushrooms and beetles on it. Which are living?", "the mushrooms and beetles", ["the log", "the log and the soil", "none of them"], "The log was once alive."),
    ("How could you sort objects found in the playground?", "into living, dead and never alive groups", ["into big and small only", "by colour only", "into hot and cold"], "Classifying."),
    ("Is a conker on the ground dead or alive?", "alive: it is a seed that can grow into a tree", ["dead, like a stone", "never alive", "a light source"], "Seeds are living."),
])


def body():
    pic = K.row(["dog", "tree", "rock"], words=["living", "living", "never alive"], size=90, label="a dog and a tree are living; a rock was never alive")
    ex = [("A wooden table?", ["Made from a tree"], "dead (was once alive)"),
          ("A metal spoon?", ["Not from a living thing"], "never alive")]
    mist = ["Thinking things that move are alive, like a car.", "Thinking plants are not alive.", "Thinking a wooden table was never alive."]
    return kid_lesson(pic, "Living things feed, grow and have young.",
                      ["Dead things were once alive, like a dead leaf or paper.", "Never alive things were never part of a living thing, like a rock.", "Something that moves is not always alive."], ex, mist)


def main():
    sets = U.sets([
        ("Alive or not?", B1 + [(g_picture, 8), (g_sort, 4)]),
        ("Living, dead, never alive", [(g_sort, 16), (g_picture, 2), (g_proc, 2)]),
        ("Which one?", [(g_pick, 15), (g_proc, 5)]),
        ("Tricky ones", [(g_trick, 8), (g_sort, 8), (g_proc, 2), (g_pick, 2)]),
        ("Thinking it through", B5 + [(g_pick, 8), (g_sort, 6), (g_picture, 1)]),
    ])
    make_uk(2, "living-dead-and-never-alive", 1, "Living things and their habitats",
            "Explore and compare the differences between things that are living, dead, and things that have never been alive.",
            "Living, Dead and Never Alive",
            "Year 2 Science: Living, Dead and Never Alive Worksheets (Sorting Things)",
            "Living, Dead, Never Alive",
            "Free Year 2 science worksheets on things that are living, dead and never alive: what living things do and sorting everyday things into groups. 100 questions with answers.",
            "Living, dead or never alive?",
            "Living things feed, grow and have young. Dead things were once alive.",
            body(),
            [("How do we know something is alive?", "Living things move, breathe, feed, grow and have young. A plant is alive even though it does not walk."),
             ("What is the difference between dead and never alive?", "Dead things were once alive, like a dead leaf, a feather or a wooden table. Never alive things, like a rock or a plastic bottle, were never part of a living thing."),
             ("Is a car alive because it moves?", "No. A car cannot feed, grow or have young, so it is not alive.")],
            sets)


if __name__ == "__main__":
    main()
