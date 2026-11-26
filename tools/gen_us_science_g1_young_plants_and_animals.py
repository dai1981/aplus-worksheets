# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Young Plants and Animals (1-LS3-1)
  python tools/gen_us_science_g1_young_plants_and_animals.py
Make observations to construct an evidence-based account that young plants and animals are like, but not exactly like,
their parents. Same kind and body parts; different size, color or spots. Puppies in one litter look different.
Some young look very different at first (tadpole, caterpillar) but grow up to look like their parents.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "babies look exactly like parents", "a kitten can grow into a dog",
"a tadpole is a fish".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text
import sci_kids as K

U = Unit(10107)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ANIM = ["dog", "cat", "bear", "rabbit", "duck", "bird", "frog", "fish", "squirrel"]
BABY = {"dog": "puppy", "cat": "kitten", "bear": "cub", "rabbit": "bunny", "duck": "duckling", "bird": "chick", "frog": "froglet", "fish": "baby fish", "squirrel": "baby squirrel"}


def family_svg(parent, opts):
    s = K.icon(parent, 70, 70, 1.3) + text(70, 140, "parent", 13)
    for i, k in enumerate(opts):
        x = 190 + i * 80
        s += K.icon(k, x, 80, 0.62) + text(x, 140, "ABCD"[i], 15)
    return svg_wrap(190 + 80 * len(opts) - 20, 150, s, "a parent %s and four babies to choose from" % K.name(parent))


def g_match():
    parent = R.choice(ANIM)
    opts = [parent] + R.sample([a for a in ANIM if a != parent], 3)
    R.shuffle(opts)
    who = P.next()[0]
    if not once(("m", parent), 2) or not once(("m", parent, tuple(opts))):
        return None
    i = opts.index(parent)
    return item(fig(family_svg(parent, opts)) + "%s sees a %s. Which baby belongs to it?" % (who, K.name(parent)), "%s (%s)" % ("ABCD"[i], BABY[parent]),
                ["%s (%s)" % ("ABCD"[j], BABY[k]) for j, k in enumerate(opts) if j != i], "A %s looks like its parent: same kind, same body parts." % BABY[parent])


LIKE = {"dog": ("four legs, fur and a tail", "It is smaller and may have a different color."), "cat": ("whiskers, fur and a tail", "It is smaller and its fur may be a different color."),
        "duck": ("feathers, a bill and webbed feet", "It is smaller and its feathers are fluffy and yellow."), "bear": ("fur, claws and four legs", "It is much smaller."),
        "rabbit": ("long ears and soft fur", "It is smaller and may be a different color."), "bird": ("a beak, feathers and wings", "It is smaller and cannot fly yet."),
        "horse": ("four legs, a mane and a tail", "It is smaller and has longer legs for its size."), "cow": ("four legs, hooves and a tail", "It is smaller and may have different spots."),
        "giraffe": ("a long neck and spots", "It is shorter and its spots are a different pattern."), "zebra": ("stripes and hooves", "Its stripes are a little different.")}


def g_like():
    a = R.choice(sorted(LIKE))
    same, diff = LIKE[a]
    nm = {"dog": "puppy", "cat": "kitten", "duck": "duckling", "bear": "cub", "rabbit": "bunny", "bird": "chick", "horse": "foal", "cow": "calf", "giraffe": "baby giraffe", "zebra": "baby zebra"}[a]
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((a, t)):
        return None
    pic = fig(K.card(a)) if a in K.NAMES else ""
    if t:
        w = R.sample([LIKE[x][0] for x in LIKE if x != a], 2) + ["nothing; they look totally different"]
        return item(pic + "%s compares a %s and its parent. How are they the same?" % (who, nm), "Both have " + same + ".", ["Both have " + x + "." if not x.startswith("nothing") else x[0].upper() + x[1:] + "." for x in w],
                    "Young animals have the same body parts as their parents.")
    return item(pic + "%s compares a %s and its parent. How is the %s different?" % (who, nm, nm), diff, ["It is a different kind of animal.", "It has no body parts.", "It is exactly the same."],
                "Young are like their parents, but not exactly.")


LITTER = [("kittens", "a black one, a gray one and an orange one"), ("puppies", "a brown one, a white one and a spotted one"),
          ("bunnies", "a white one, a brown one and a gray one"), ("piglets", "a pink one, a spotted one and a black one"),
          ("chicks", "a yellow one, a brown one and a black one"), ("lambs", "a white one, a black one and a spotted one")]


def g_litter():
    a, cols = R.choice(LITTER)
    who = P.next()[0]
    if not once(a):
        return None
    return item("%s sees 3 %s from the same mother: %s. What does this show?" % (who, a, cols), "Babies from the same parents can look different.",
                ["All babies look exactly the same.", "They have different kinds of parents.", "They will turn into other animals."], "Same kind, different colors.")


CHANGE = [("tadpole", "frog", "a fish", "It grows legs and loses its tail."), ("caterpillar", "butterfly", "a worm", "It makes a chrysalis and changes."),
          ("chick", "hen", "a duck", "It grows big feathers."), ("seedling", "big plant", "a rock", "It grows taller with more leaves."),
          ("acorn", "oak tree", "a pine tree", "It sprouts and grows for many years."), ("sunflower seed", "sunflower", "a rose", "It sprouts and grows a big flower.")]


def g_change():
    y, a, wrong, how = R.choice(CHANGE)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((y, t)):
        return None
    if t:
        w = [wrong] + R.sample(["a " + c[1] for c in CHANGE if c[1] != a], 2)
        return item("%s watches a %s grow up. What will it become?" % (who, y), "a " + a, w, how)
    return item("A %s does not look like its parent yet. Will it grow up to look like a %s?" % (y, a), "Yes. " + how, ["No. It stays the same forever.", "No. It turns into %s." % wrong, "No. It turns into a rock."],
                "Some young look different at first.")


PLANTS = [("a bean seedling", "a big bean plant", "The leaves have the same shape, but the seedling is small."),
          ("a little pine tree", "a tall pine tree", "Both have needles, but the little one is short."),
          ("a baby sunflower", "a grown sunflower", "Both have the same kind of leaves, but the baby has no flower yet."),
          ("a young apple tree", "an old apple tree", "Both have the same leaves, but the young tree has no apples yet."),
          ("a small cactus", "a big cactus", "Both have spines, but the small one is shorter."),
          ("a young maple tree", "a big maple tree", "The leaves have the same shape, but the young tree is thin.")]


def g_plant():
    y, p, e = R.choice(PLANTS)
    who = P.next()[0]
    if not once(y):
        return None
    return item("%s compares %s and %s. What does %s see?" % (who, y, p, who), e, ["They look exactly the same.", "They are not the same kind of plant.", "The young plant has no leaves at all."],
                "Young plants are like their parents, but not exactly.")


def g_parent():
    baby = R.choice(ANIM)
    opts = [baby] + R.sample([a for a in ANIM if a != baby], 3)
    R.shuffle(opts)
    who = P.next()[0]
    if not once(("p", baby)):
        return None
    sv = K.icon(baby, 60, 90, 0.62) + text(60, 140, BABY[baby], 13)
    for i, k in enumerate(opts):
        x = 170 + i * 92
        sv += K.icon(k, x, 72, 1.05) + text(x, 140, "ABCD"[i], 15)
    pic = svg_wrap(170 + 92 * 4 - 30, 150, sv, "a baby %s and four grown animals to choose from" % K.name(baby))
    i = opts.index(baby)
    return item(fig(pic) + "%s finds a %s. Which one is its parent?" % (who, BABY[baby]), "%s (%s)" % ("ABCD"[i], K.name(baby)),
                ["%s (%s)" % ("ABCD"[j], K.name(k)) for j, k in enumerate(opts) if j != i], "A %s grows up to be a %s." % (BABY[baby], K.name(baby)))


COLS = ["black", "white", "brown", "gray", "spotted", "orange"]


def g_color():
    a = R.choice([("cat", "kitten"), ("dog", "puppy"), ("rabbit", "bunny"), ("horse", "foal"), ("cow", "calf")])
    c1, c2 = R.sample([c for c in COLS if not (c == "orange" and a[0] != "cat")], 2)
    who = P.next()[0]
    if not once((a, c1, c2)) or not once(("c", a), 4):
        return None
    t = R.random() < 0.5
    if t:
        return item("%s sees a %s %s with a %s %s. Is the %s a %s?" % (who, c1, a[0], c2, a[1], a[1], a[0]), "Yes. Babies can be a different color.",
                    ["No. It must be the same color.", "No. It is a different animal.", "Only when it grows up."], "Color can be different. The kind is the same.")
    return item("%s sees a %s %s with a %s %s. How are they the same?" % (who, c1, a[0], c2, a[1]), "They are the same kind of animal.",
                ["They are the same color.", "They are the same size.", "Nothing is the same."], "Same kind, different color and size.")


B1 = bank([
    ("Do baby animals look exactly like their parents?", "No. They look alike, but not exactly.", ["Yes, always.", "No, they never look alike.", "Only on Sundays."], "Alike, not the same."),
    ("What does a kitten grow up to be?", "a cat", ["a dog", "a bear", "a bird"], "Kittens become cats."),
    ("What does a puppy grow up to be?", "a dog", ["a cat", "a duck", "a fish"], "Puppies become dogs."),
    ("How are most babies different from their parents?", "They are smaller.", ["They are a different kind.", "They have no legs.", "They are always bigger."], "Babies grow."),
    ("What does a tadpole grow up to be?", "a frog", ["a fish", "a duck", "a snake"], "Tadpoles grow legs."),
    ("What does a caterpillar grow up to be?", "a butterfly", ["a bee", "a bird", "a worm"], "It changes in a chrysalis."),
    ("What does an acorn grow into?", "an oak tree", ["a rose", "a cactus", "a pumpkin"], "Seeds grow into plants like their parents."),
    ("Why do young animals look like their parents?", "They are the same kind of animal.", ["They copy their parents.", "They eat the same food.", "They live in the same house."], "Same kind."),
])
B5 = bank([
    ("Ava sees a black dog with a brown puppy. Is the puppy still a dog?", "Yes. It can be a different color.", ["No, it is a cat.", "No, it is a fox.", "Only when it grows black."], "Color can be different."),
    ("Leo plants seeds from a red flower. Some new flowers are pink. What does this show?", "Young plants can be a little different.", ["They are a new kind of plant.", "The seeds were rocks.", "Pink flowers are not flowers."], "Alike, not exactly."),
    ("Mia says, “A tadpole is a fish.” Is she right?", "No. It is a baby frog.", ["Yes.", "No, it is a snake.", "No, it is a bug."], "It grows into a frog."),
    ("Kai sees 2 baby giraffes. Their spots are different. Are they both giraffes?", "Yes.", ["No.", "Only one is.", "They are zebras."], "Spots can differ."),
    ("What evidence shows a duckling is like its parent?", "It has a bill, feathers and webbed feet.", ["It is small and yellow.", "It cannot fly yet.", "It lives in a box."], "Same body parts."),
])


def body():
    pic = svg_wrap(380, 150, K.icon("dog", 80, 70, 1.3) + text(80, 140, "parent", 13) + K.icon("dog", 220, 84, 0.7) + text(220, 140, "puppy", 13)
                                                        + K.icon("cat", 320, 70, 1.0) + text(320, 140, "not its baby", 13), "a dog, its puppy, and a cat that is not its baby")
    ex = [("How is a puppy like its parent?", ["Look at the body parts."], "four legs, fur and a tail"),
          ("How is a puppy different?", ["Look at size and color."], "It is smaller and may be a different color.")]
    mist = ["Thinking babies look exactly like their parents.",
            "Thinking a kitten can grow into a dog.",
            "Thinking a tadpole is a fish."]
    return kid_lesson(pic, "Babies are like their parents, but not exactly.",
                      ["Same: kind of animal, body parts.", "Different: size, color, spots.", "Tadpoles and caterpillars change as they grow."], ex, mist)


def main():
    sets = U.sets([
        ("Like their parents", B1 + [(g_match, 6), (g_like, 6)]),
        ("Which baby? Which parent?", [(g_match, 8), (g_parent, 8), (g_litter, 4)]),
        ("Alike and different", [(g_like, 10), (g_plant, 6), (g_color, 4)]),
        ("Growing up", [(g_change, 12), (g_color, 8)]),
        ("Family detectives", B5 + [(g_like, 3), (g_match, 3), (g_parent, 1), (g_litter, 2), (g_color, 6)]),
    ])
    make("grade-1", "young-plants-and-animals", 7, "1-LS3-1",
         "Make observations to construct an evidence-based account that young plants and animals are like, but not exactly like, their parents.",
         "Young Plants and Animals",
         "Grade 1 Young Plants and Animals Worksheets: Like Their Parents, But Not Exactly",
         "Young and Parents",
         "Free grade 1 science worksheets on young plants and animals (NGSS 1-LS3-1): how babies are like their parents but not exactly, matching babies to parents, and growing up. 100 picture questions with answers.",
         "Babies look like their parents.",
         "Same kind and body parts. Different size, color or spots.",
         body(),
         [("How are young animals like their parents?", "They are the same kind of animal with the same body parts, like four legs, fur and a tail."),
          ("How are they different?", "They are smaller, and they may have a different color, spots or stripes."),
          ("Do all babies look like their parents at first?", "Not all. A tadpole and a caterpillar look different, but they grow up to look like a frog and a butterfly.")],
         sets)


if __name__ == "__main__":
    main()
