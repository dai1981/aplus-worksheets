# -*- coding: utf-8 -*-
"""
UK Year 1 science: Parts of a Plant (Plants)
  python tools/gen_uk_science_y1_parts_of_a_plant.py
Identify and describe the basic structure of a variety of common flowering plants, including trees: roots, stem,
leaves, flowers and petals, seeds and fruits, trunk and branches; a labelled plant picture; plant parts we eat.
Wrong answers come from real mistakes: "roots grow above the ground", "a trunk is not a stem", "all leaves are the
same shape", "flowers are only on garden plants".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, fig, People, once
from uk_sci_pics import plant
import sci_kids as K

U = Unit(61103)
R = U.R
P = People(R)

PARTS = ["flower", "leaf", "stem", "roots"]
NM = {"flower": "the flower", "leaf": "a leaf", "stem": "the stem", "roots": "the roots"}


def g_pic():
    lab = dict(zip(PARTS, R.sample("ABCD", 4)))
    p = R.choice(PARTS)
    k = R.random() < 0.5
    if not once(("pc", p, lab[p], k)):
        return None
    pic = fig(plant(lab))
    if k:
        return item(pic + "Which letter points to %s?" % NM[p], lab[p], [lab[x] for x in PARTS if x != p], "Flower at the top, leaves on the stem, roots under the soil.")
    return item(pic + "Which part is labelled %s?" % lab[p], NM[p], [NM[x] for x in PARTS if x != p], "Flower at the top, leaves on the stem, roots under the soil.")


DESC = [("is under the soil", "the roots"), ("is usually green and flat", "the leaves"), ("is often brightly coloured", "the flower"), ("holds the plant up", "the stem"),
        ("grows into a new plant", "a seed"), ("is the colourful part of a flower", "the petals"), ("is the woody stem of a tree", "the trunk"),
        ("holds the seeds of an apple tree", "the fruit (the apple)"), ("are the arms of a tree", "the branches"), ("takes in water from the soil", "the roots"),
        ("makes the plant's food using sunlight", "the leaves"), ("is the tough outside of a tree trunk", "the bark"), ("holds the flower up towards the light", "the stem"),
        ("is a flower that has not opened yet", "a bud"), ("helps the plant stay firmly in the ground", "the roots"), ("is where the seeds are made", "the flower")]
ALL = ["the roots", "the leaves", "the flower", "the stem", "a seed", "the petals", "the trunk", "the fruit (the apple)", "the branches", "the bark", "a bud"]


def g_desc():
    d, a = R.choice(DESC)
    if not once(("de", d)):
        return None
    bad = {"the flower": ["the petals"], "the petals": ["the flower"], "the stem": ["the trunk"], "the trunk": ["the stem"]}.get(a, [])
    return item("Which part of a plant %s?" % d, a, R.sample([x for x in ALL if x != a and x not in bad], 3), "Each part of a plant has a name.")


EAT = [("a carrot", "the root"), ("lettuce", "the leaves"), ("celery", "the stem"), ("broccoli", "the flowers"), ("peas", "the seeds"), ("an apple", "the fruit"),
       ("a parsnip", "the root"), ("cabbage", "the leaves"), ("sweetcorn", "the seeds"), ("a strawberry", "the fruit"), ("a radish", "the root"), ("spinach", "the leaves"),
       ("cauliflower", "the flowers"), ("a pear", "the fruit"), ("beans in a pod", "the seeds"), ("asparagus", "the stem")]
EP = ["the root", "the stem", "the leaves", "the flowers", "the seeds", "the fruit"]


def g_eat():
    f, p = R.choice(EAT)
    if not once(("ea", f)):
        return None
    return item("Which part of a plant is %s?" % f, p, R.sample([x for x in EP if x != p], 3), "We eat many different parts of plants.")


TREE = [("a trunk", "a stem"), ("branches", "parts of the stem"), ("leaves", "leaves"), ("blossom", "flowers"), ("roots", "roots")]


def g_tree():
    t, a = R.choice(TREE)
    if not once(("tr", t)):
        return None
    w = [x for x in ["a stem", "leaves", "flowers", "roots", "seeds"] if x != a and not (a == "parts of the stem" and x == "a stem")]
    return item("A tree is a plant. A tree has %s. What plant part is that?" % t, a, R.sample(w, 3), "Trees have the same parts as other flowering plants.")


def g_grow():
    who = P.next()[0]
    base = R.choice([[2, 4, 6, 8, 10], [2, 3, 5, 7, 9], [2, 4, 5, 7, 10], [2, 3, 4, 6, 8], [2, 4, 7, 9, 12], [2, 5, 7, 10, 13]])
    k = R.choice(["read", "read", "most", "diff"])
    ri = R.randrange(1, 5)
    if not once(("gr", tuple(base), k, ri if k == "read" else 0)):
        return None
    from uk_sci import table
    tab = table(["Week", "Number of leaves"], [[str(i + 1), str(x)] for i, x in enumerate(base)])
    intro = tab + "%s counted the leaves on a sunflower seedling each week. " % who
    if k == "read":
        g = str(base[ri])
        return item(intro + "How many leaves were there in week %d?" % (ri + 1), g, [str(x) for x in base if x != base[ri]][:3], "Read across from week %d." % (ri + 1))
    if k == "most":
        return item(intro + "In which week were there the most leaves?", "week 5", ["week 1", "week 2", "week 3"], "The biggest number is at the end.")
    d = base[4] - base[0]
    g = str(d)
    return item(intro + "How many more leaves were there in week 5 than in week 1?", g, [x for x in dict.fromkeys([str(base[4]), str(base[0]), str(d + 1), str(base[4] + base[0])]) if x != g][:3],
                "%d − %d = %d." % (base[4], base[0], d))


B3 = bank([
    ("Which part of the plant do we eat when we eat a potato?", "a part that grows under the ground", ["the flower", "the leaf", "the petal"], "Potatoes grow underground."),
    ("What is inside an apple?", "seeds (pips)", ["roots", "petals", "bark"], "Fruits hold seeds."),
    ("Which part of a pea plant do we eat?", "the seeds", ["the roots", "the bark", "the petals"], "Peas are seeds."),
    ("What colour are most leaves in summer?", "green", ["blue", "black", "white"], "They turn colours in autumn."),
    ("Which plant part do we use to make a daisy chain?", "the flowers and their stems", ["the roots", "the bark", "the seeds"], "Thread the stems."),
    ("Where do apples grow?", "on apple trees", ["under the ground", "on bushes in the sea", "on rose stems"], "Fruits grow from flowers."),
    ("Which part of a plant is the tough skin on a tree trunk?", "the bark", ["the petal", "the root hair", "the bud"], "It protects the tree."),
    ("Do all plants have the same shaped flowers?", "No. Flowers come in many shapes and colours.", ["Yes, all the same.", "Plants have no flowers.", "Only trees have flowers."], "Compare them."),
])
B1 = bank([
    ("Which part of a plant grows under the ground?", "the roots", ["the flower", "the leaves", "the petals"], "Roots grow down."),
    ("Which part of a plant is green and catches sunlight?", "the leaves", ["the roots", "the seeds", "the soil"], "Leaves make food."),
    ("What is the stem of a tree called?", "the trunk", ["the root", "the petal", "the bud"], "Thick and woody."),
    ("What are the coloured parts of a flower called?", "petals", ["roots", "bark", "trunks"], "They attract insects."),
    ("What does a seed grow into?", "a new plant", ["a rock", "an insect", "a cloud"], "Plant it and water it."),
    ("Do trees have flowers?", "Yes. Many trees have flowers called blossom.", ["No, never.", "Only pine trees.", "Only in winter."], "Apple blossom."),
    ("Which part holds a plant up?", "the stem", ["the petals", "the roots only", "the seeds"], "Like a backbone."),
    ("What is a bud?", "a flower or leaf that has not opened yet", ["a kind of root", "a dead leaf", "a kind of seed"], "Buds open in spring."),
])
B5 = bank([
    ("Why do plants have roots?", "to take in water and hold the plant in the soil", ["to make flowers", "to catch sunlight", "to scare insects"], "Roots drink and hold."),
    ("Are all leaves the same shape?", "No. Different plants have different shaped leaves.", ["Yes, all the same.", "Only trees have leaves.", "Leaves have no shape."], "Look closely."),
    ("How could you find out how many petals a daisy has?", "Look closely with a magnifying glass and count them.", ["Guess.", "Pull the roots up.", "Look at a rose instead."], "Observe."),
    ("Why do flowers have bright petals?", "to attract insects such as bees", ["to keep the plant warm", "to drink water", "to hold the plant up"], "Insects help make seeds."),
    ("Which part of a sunflower do birds like to eat?", "the seeds", ["the roots", "the stem", "the soil"], "Lots of seeds in the middle."),
])


def body():
    pic = plant({"flower": "A", "leaf": "B", "stem": "C", "roots": "D"}, "a flowering plant: A flower, B leaf, C stem, D roots")
    ex = [("Which part is under the soil?", ["It grows down"], "the roots"),
          ("A tree's thick stem is called?", ["Woody"], "the trunk")]
    mist = ["Thinking roots grow above the ground.", "Thinking a tree trunk is not a stem.", "Thinking all leaves are the same shape."]
    return kid_lesson(pic, "Plants have roots, a stem, leaves and flowers.",
                      ["Roots are under the soil.", "Leaves grow on the stem.", "A tree trunk is a big, woody stem."], ex, mist)


def main():
    sets = U.sets([
        ("Plant parts", B1 + [(g_pic, 12)]),
        ("Labelled plant", [(g_pic, 14), (g_desc, 6)]),
        ("Describing parts", [(g_desc, 8), (g_tree, 5), (g_eat, 7)]),
        ("Parts we eat", B3 + [(g_eat, 8), (g_grow, 4)]),
        ("Watching plants grow", B5 + [(g_grow, 15)]),
    ])
    make_uk(1, "parts-of-a-plant", 3, "Plants",
            "Identify and describe the basic structure of a variety of common flowering plants, including trees.",
            "Parts of a Plant",
            "Year 1 Science: Parts of a Plant Worksheets (Roots, Stem, Leaves, Flowers)",
            "Parts of a Plant",
            "Free Year 1 science worksheets on the parts of a plant: roots, stem, leaves, flowers, seeds and fruit, the parts of a tree and plant parts we eat. 100 questions with answers.",
            "Roots, stem, leaves, flowers.",
            "A tree trunk is a stem. Roots are under the soil.",
            body(),
            [("What are the parts of a plant?", "Roots, a stem, leaves and flowers. Many plants also have seeds and fruits."),
             ("Does a tree have the same parts?", "Yes. A tree has roots, a trunk (a big, woody stem), branches, leaves and often blossom (flowers)."),
             ("Which parts of plants do we eat?", "Carrots are roots, lettuce is leaves, celery is a stem, broccoli is flowers, peas are seeds and apples are fruits.")],
            sets)


if __name__ == "__main__":
    main()
