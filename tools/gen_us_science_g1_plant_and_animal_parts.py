# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Plant and Animal Parts (1-LS1-1)
  python tools/gen_us_science_g1_plant_and_animal_parts.py
Use materials to design a solution to a human problem by mimicking how plants and/or animals use their external parts
to help them survive, grow, and meet their needs. Roots, stems, leaves, thorns; shells, fur, claws, beaks, fins, webbed feet;
helmets like shells, flippers like duck feet, hook-and-loop tape like burrs.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "roots make food", "a shell is for swimming", "people invent things without copying nature".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, People
import sci_kids as K

U = Unit(10105)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# living thing, part, job, picture
PARTS = [("a tree", "roots", "take in water and stay in the ground", "tree"), ("a tree", "leaves", "use sunlight to make food", "tree"),
         ("a tree", "trunk", "stand up tall", "tree"), ("a cactus", "spines", "keep animals from eating it", "cactus"),
         ("a flower", "bright petals", "bring bees to the flower", "flower"), ("a duck", "webbed feet", "push through water to swim", "duck"),
         ("a fish", "fins", "steer and swim", "fish"), ("a bird", "beak", "pick up and crack seeds", "bird"), ("a bird", "wings", "fly", "bird"),
         ("a bear", "thick fur", "stay warm", "bear"), ("a bear", "sharp claws", "dig and catch food", "bear"), ("a rabbit", "big ears", "hear danger far away", "rabbit"),
         ("a cat", "whiskers", "feel things in the dark", "cat"), ("a frog", "long back legs", "jump far", "frog"), ("a squirrel", "bushy tail", "balance on branches", "squirrel"),
         ("a butterfly", "long mouth tube", "sip nectar from flowers", "butterfly"), ("a turtle", "hard shell", "protect its soft body", None),
         ("a porcupine", "sharp quills", "keep enemies away", None), ("a rose", "thorns", "protect the stem", None), ("an eagle", "sharp eyes", "see food far away", None)]


def g_part():
    who_, part, job, pic = R.choice(PARTS)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((who_, part, t)):
        return None
    fg = fig(K.card(pic)) if pic else ""
    one = part in ("trunk", "beak", "hard shell", "bushy tail", "long mouth tube") or part.endswith("fur")
    the = who_.replace("a ", "the ", 1).replace("an ", "the ", 1)
    if t:
        w = R.sample([x[2] for x in PARTS if x[2] != job and x[1] != part and not ("protect" in job and "protect" in x[2]) and not ("swim" in job and "swim" in x[2])], 3)
        return item(fg + "%s looks at %s. What %s its %s help it do?" % (who, who_, "does" if one else "do", part), job, w,
                    "The %s %s %s %s." % (part, "helps" if one else "help", the, job))
    prot = {"spines", "thorns", "sharp quills", "hard shell"}
    w = R.sample([x[1] for x in PARTS if x[1] != part and x[0] != who_ and not (part in prot and x[1] in prot)], 3)
    return item(fg + "Which part helps %s %s?" % (the, job), part, w, "The %s %s %s %s." % (part, "helps" if one else "help", the, job))


# invention, what it copies, why
MIMIC = [("a bike helmet", "a turtle's hard shell", "It protects your head."), ("swim flippers", "a duck's webbed feet", "They help you push through water."),
         ("hook-and-loop tape", "burrs that stick to fur", "Tiny hooks grab loops."), ("a warm winter coat", "an animal's thick fur", "It keeps you warm."),
         ("snowshoes", "a snowshoe hare's big, wide feet", "Wide feet do not sink in snow."), ("an umbrella", "a big leaf that rain runs off", "It keeps rain off."),
         ("tongs for picking up food", "a bird's beak", "They grab and hold things."), ("a fence with spikes", "a cactus's spines", "It keeps others out."),
         ("a garden rake", "an animal's claws", "It scratches and digs."), ("goggles", "a frog's clear eyelid", "They protect eyes under water."),
("a straw", "a butterfly's long mouth tube", "It sips liquid.")]


def g_mimic():
    inv, copy, why = R.choice(MIMIC)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((inv, t)):
        return None
    if t:
        w = R.sample([x[1] for x in MIMIC if x[1] != copy], 3)
        return item("%s uses %s. Which part of nature gave people this idea?" % (who, inv), copy, w, why)
    w = R.sample([x[0] for x in MIMIC if x[0] != inv], 3)
    return item("%s wants to copy %s. What could %s make?" % (who, copy, who), inv, w, why)


PROB = [("keep your head safe on a bike", "a turtle's hard shell"), ("swim faster in a pool", "a duck's webbed feet"), ("stay warm in the snow", "a polar bear's thick fur"),
        ("walk on deep snow without sinking", "a snowshoe hare's wide feet"), ("keep animals out of a garden", "a rose's thorns"),
        ("hear quiet sounds far away", "a rabbit's big ears"), ("pick up tiny things", "a bird's pointed beak"), ("keep rain off your head", "a big, waxy leaf"),
        ("climb a slippery wall", "a gecko's sticky toes"), ("see in a dark room", "a cat's big eyes")]


def g_design():
    p, a = R.choice(PROB)
    who = P.next()[0]
    if not once(p):
        return None
    w = R.sample([x[1] for x in PROB if x[1] != a], 3)
    return item("%s wants to %s. Which animal or plant part is the best to copy?" % (who, p), a, w, "Match the part to the job.")


def g_pick():
    kinds = R.sample(["duck", "fish", "bird", "bear", "rabbit", "cactus", "tree", "frog"], 4)
    jobs = {"duck": "webbed feet for swimming", "fish": "fins for swimming", "bird": "a beak for cracking seeds", "bear": "thick fur for staying warm",
            "rabbit": "big ears for hearing", "cactus": "spines for protection", "tree": "roots for taking in water", "frog": "long legs for jumping"}
    a = R.choice(kinds)
    clash = {"duck": {"fish"}, "fish": {"duck"}, "bird": {"duck"}, "frog": {"rabbit"}, "bear": {"rabbit"}}
    if set(kinds) & clash.get(a, set()) or not once((tuple(kinds), a)):
        return None
    L = "ABCD"
    who = P.next()[0]
    pic = K.row(kinds, words=["%s. %s" % (L[i], K.name(k)) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s looks at these. Which one has %s?" % (who, jobs[a]), "%s (%s)" % (L[kinds.index(a)], K.name(a)),
                ["%s (%s)" % (L[i], K.name(k)) for i, k in enumerate(kinds) if k != a], "The %s has %s." % (K.name(a), jobs[a]))


B1 = bank([
    ("What do roots do?", "take in water", ["make food", "make flowers", "fly"], "Roots drink from the soil."),
    ("What do leaves do?", "make food from sunlight", ["take in water from soil", "dig holes", "make seeds fly"], "Leaves make food."),
    ("Why does a turtle have a hard shell?", "to protect its soft body", ["to swim faster", "to fly", "to dig"], "The shell is armor."),
    ("Why does a duck have webbed feet?", "to swim", ["to climb trees", "to dig", "to see"], "Webbed feet push water."),
    ("What do people do when they copy nature?", "make things that work like animal or plant parts", ["make animals", "grow new plants", "stop inventing"], "Nature gives ideas."),
    ("Why do cactuses have spines?", "to keep animals from eating them", ["to make food", "to swim", "to drink rain"], "Spines protect."),
    ("Why do birds have wings?", "to fly", ["to swim", "to dig", "to hear"], "Wings lift birds."),
    ("Why does a bear have thick fur?", "to stay warm", ["to swim fast", "to see far", "to make food"], "Fur keeps heat in."),
])
B5 = bank([
    ("Ava wants mittens that keep her hands warm. What should she copy?", "a bear's thick fur", ["a fish's fins", "a cactus's spines", "a bird's beak"], "Fur is warm."),
    ("Leo's helmet is soft paper. Why is that a bad idea?", "It cannot protect his head like a hard shell.", ["It is too hard.", "It is too heavy.", "It is too warm."], "Copy the hard shell."),
    ("Mia makes swim fins from cardboard. They get soggy. What should she use?", "rubber or plastic", ["paper", "tissue", "bread"], "Choose a waterproof material."),
    ("Kai copies a burr to make shoes stick shut. What does he make?", "hook-and-loop tape", ["a zipper of ice", "glue made of water", "a paper bow"], "Burrs have tiny hooks."),
    ("Why did people copy a turtle shell for a helmet?", "Both protect what is inside.", ["Both swim.", "Both are green.", "Both are soft."], "Same job."),
])


def body():
    pic = K.row(["duck", "cactus", "bear", "tree"], words=["webbed feet", "spines", "thick fur", "roots"], size=95)
    ex = [("What do a duck's webbed feet help it do?", ["Look at the feet."], "swim"),
          ("A helmet copies which animal part?", ["It protects."], "a turtle's hard shell")]
    mist = ["Thinking roots make food. Leaves make food.",
            "Mixing up the job of a part, like a shell for swimming.",
            "Thinking inventions never copy nature."]
    return kid_lesson(pic, "Body parts help plants and animals live.",
                      ["Parts help them eat, move, stay safe and stay warm.", "People copy these parts to solve problems.", "Helmet = turtle shell. Flippers = duck feet."], ex, mist)


def main():
    sets = U.sets([
        ("Plant parts and animal parts", B1 + [(g_part, 6), (g_pick, 6)]),
        ("What does it do?", [(g_part, 14), (g_pick, 6)]),
        ("Copying nature", [(g_mimic, 14), (g_part, 6)]),
        ("Solving problems", [(g_design, 10), (g_mimic, 6), (g_pick, 4)]),
        ("Inventors", B5 + [(g_pick, 6), (g_part, 6), (g_mimic, 3)]),
    ])
    make("grade-1", "plant-and-animal-parts", 5, "1-LS1-1",
         "Use materials to design a solution to a human problem by mimicking how plants and/or animals use their external parts to help them survive, grow, and meet their needs.",
         "Plant and Animal Parts",
         "Grade 1 Plant and Animal Parts Worksheets: How Parts Help, and Copying Nature",
         "Plant and Animal Parts",
         "Free grade 1 science worksheets on plant and animal parts (NGSS 1-LS1-1): roots, leaves, shells, fur and fins, and inventions that copy nature. 100 picture questions with answers.",
         "Parts help living things live.",
         "People copy plant and animal parts to solve problems.",
         body(),
         [("How do parts help plants?", "Roots take in water, stems hold the plant up, leaves make food and thorns or spines protect it."),
          ("How do parts help animals?", "Shells and spines protect, fur keeps them warm, wings help them fly and fins or webbed feet help them swim."),
          ("What inventions copy nature?", "Helmets copy hard shells, swim flippers copy duck feet and hook-and-loop tape copies burrs.")],
         sets)


if __name__ == "__main__":
    main()
