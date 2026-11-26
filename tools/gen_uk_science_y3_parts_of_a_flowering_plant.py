# -*- coding: utf-8 -*-
"""
UK Year 3 science: Parts of a Flowering Plant (Plants)
  python tools/gen_uk_science_y3_parts_of_a_flowering_plant.py
The roots, stem (trunk), leaves and flowers of flowering plants and the job of each part, with a labelled plant
diagram, parts we eat, and parts of trees.
Wrong answers come from real mistakes: "roots make the food", "the stem is only for decoration",
"flowers are just there to look pretty", "a tree trunk is not a stem".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, fig, People, once
from uk_sci_pics import plant

U = Unit(61301)
R = U.R
P = People(R)

PART = {"roots": "take in water and nutrients from the soil and hold the plant firmly in the ground",
        "stem": "hold the plant up and carry water from the roots to the leaves",
        "leaf": "use sunlight to make food for the plant",
        "flower": "make seeds so that new plants can grow"}
DOES = {"roots": "takes in water and nutrients from the soil and holds the plant in the ground",
        "stem": "holds the plant up and carries water from the roots to the leaves",
        "leaf": "uses sunlight to make food for the plant",
        "flower": "makes seeds so that new plants can grow"}
NAME = {"roots": "the roots", "stem": "the stem", "leaf": "the leaves", "flower": "the flower"}


def g_job():
    p = R.choice(sorted(PART))
    k = R.random() < 0.5
    if not once(("jb", p, k)):
        return None
    if k:
        return item("What is the job of %s of a plant?" % NAME[p], "to " + PART[p], ["to " + PART[x] for x in sorted(PART) if x != p], "Roots drink, stems hold up, leaves make food, flowers make seeds.")
    return item("Which part of a plant does this job: it %s?" % DOES[p], NAME[p], [NAME[x] for x in sorted(PART) if x != p], "Each part has its own job.")


def g_pic():
    parts = sorted(PART)
    letters = R.sample("ABCD", 4)
    lab = dict(zip(parts, letters))
    p = R.choice(parts)
    k = R.random() < 0.5
    if not once(("pc", tuple(letters), p, k)):
        return None
    pic = fig(plant(lab))
    if k:
        return item(pic + "Look at the plant. Which letter points to %s?" % NAME[p], lab[p], [lab[x] for x in parts if x != p], "The flower is at the top, the leaves come off the stem, and the roots are under the soil.")
    return item(pic + "Look at the plant. Which part is labelled %s?" % lab[p], NAME[p], [NAME[x] for x in parts if x != p], "The flower is at the top, the leaves come off the stem, and the roots are under the soil.")


FOOD = [("a carrot", "the root"), ("lettuce", "the leaves"), ("cabbage", "the leaves"), ("spinach", "the leaves"),
        ("celery", "the stem"), ("broccoli", "the flowers"), ("cauliflower", "the flowers"), ("a parsnip", "the root"), ("a radish", "the root"),
        ("peas", "the seeds"), ("sweetcorn", "the seeds"), ("a beetroot", "the root"), ("asparagus", "the stem"),
        ("baked beans", "the seeds"), ("a turnip", "the root"), ("kale", "the leaves")]
FOODP = ["the root", "the stem", "the leaves", "the flowers", "the seeds"]


def g_food():
    f, p = R.choice(FOOD)
    if not once(("fd", f)):
        return None
    w = [x for x in FOODP if x != p]
    return item("Which part of the plant do we eat when we eat %s?" % f, p, R.sample(w, 3), "We eat many different parts of plants.")


TREE = [("the trunk", "the stem"), ("the branches", "parts of the stem"), ("the leaves", "the leaves"), ("the blossom", "the flowers"), ("the roots under the ground", "the roots")]


def g_tree():
    t, p = R.choice(TREE)
    if not once(("tr", t)):
        return None
    w = [x for x in ["the stem", "the leaves", "the flowers", "the roots", "parts of the stem"] if x != p and not (p == "parts of the stem" and x == "the stem") and not (p == "the stem" and x == "parts of the stem")]
    return item("A tree is a plant. Which plant part is %s of a tree?" % t, p, R.sample(w, 3), "Trees have the same parts as other flowering plants: a trunk is a big, woody stem.")


PROB = [("A plant's roots are cut off.", "It cannot take in water, so it wilts.", "roots"),
        ("All the leaves are picked off a plant.", "It cannot make its food, so it grows weakly.", "leaf"),
        ("A plant's stem is snapped.", "Water cannot reach the leaves, so they dry up.", "stem"),
        ("Every flower is picked off a plant.", "It cannot make seeds for new plants.", "flower"),
        ("A plant is kept in a dark cupboard, so its leaves get no light.", "It cannot make its food, so it grows weakly.", "leaf"),
        ("A plant's roots are left in dry soil for weeks.", "It cannot take in water, so it wilts.", "roots"),
        ("A tree's trunk is badly damaged all the way round.", "Water cannot reach the leaves, so they dry up.", "stem"),
        ("Bees cannot reach the flowers of a plant.", "It cannot make seeds for new plants.", "flower")]


def g_prob():
    s, a, _ = R.choice(PROB)
    who = P.next()[0]
    if not once(("pr", s)):
        return None
    return item("%s What will most likely happen to the plant?" % s, a, sorted({x[1] for x in PROB if x[1] != a}), "Each part does a job the plant needs.")


B1 = bank([
    ("Which part of a plant is usually under the soil?", "the roots", ["the flower", "the leaves", "the stem"], "Roots grow down into the soil."),
    ("Which part of a plant is usually green and flat?", "the leaves", ["the roots", "the seeds", "the petals"], "Leaves catch the sunlight."),
    ("What is the trunk of a tree?", "a thick, woody stem", ["a root", "a big leaf", "a flower"], "It holds the tree up."),
    ("Why are flowers often brightly coloured?", "to attract insects such as bees", ["to scare animals away", "to keep the plant warm", "to make food"], "Insects carry pollen."),
    ("What do roots take in from the soil?", "water and nutrients", ["sunlight", "air only", "seeds"], "They are like straws."),
    ("Which part of a plant makes its food?", "the leaves", ["the roots", "the flowers", "the soil"], "They use sunlight."),
    ("Do plants get their food from the soil?", "No. They make their own food in their leaves using sunlight.", ["Yes, all of it.", "Yes, through their flowers.", "No, they eat insects."], "Soil gives water and nutrients, not food."),
    ("What does a flower make after it has been pollinated?", "seeds", ["roots", "leaves", "soil"], "Seeds grow into new plants."),
])
B5 = bank([
    ("Why do some trees have very deep roots?", "to reach water far underground and hold the tree up in strong winds", ["to make flowers", "to catch sunlight", "to keep warm"], "Big plants need strong roots."),
    ("Why are leaves usually wide and flat?", "to catch as much sunlight as possible", ["to hold water in the soil", "to scare insects", "to make the plant heavy"], "More light, more food."),
    ("A seedling has a weak, thin stem and falls over. What is the stem not doing well?", "holding the plant up", ["making seeds", "taking in nutrients from soil", "attracting insects"], "Stems support plants."),
    ("Why does a gardener water the soil and not the flowers?", "The roots take in the water.", ["Flowers drink the water.", "Leaves drink through the soil.", "Water is not needed."], "Roots drink."),
    ("Is grass a flowering plant?", "Yes. It has small flowers that are hard to notice.", ["No, it has no parts.", "No, it is a tree.", "No, it is a fungus."], "Not all flowers are bright."),
])


def body():
    think = ("<p><b>A flowering plant has four main parts, and each part has a job.</b></p>"
             "<ul><li>Roots take in water and nutrients and hold the plant in the ground.</li>"
             "<li>The stem holds the plant up and carries water to the leaves. A tree trunk is a stem.</li>"
             "<li>Leaves use sunlight to make food. Flowers make seeds.</li></ul>")
    ex = [("Which part takes in water?", ["It is under the soil"], "the roots"),
          ("When we eat a carrot, which part is it?", ["It grows down into the soil"], "the root")]
    mist = ["Thinking plants get their food from the soil.", "Thinking a tree trunk is not a stem.", "Thinking flowers are only there to look pretty."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Plant parts", B1 + [(g_job, 8), (g_pic, 4)]),
        ("Labelled plant", [(g_pic, 10), (g_job, 5), (g_tree, 5)]),
        ("Parts we eat", [(g_food, 14), (g_pic, 6)]),
        ("Jobs of each part", [(g_prob, 5), (g_pic, 8), (g_job, 3), (g_food, 3)]),
        ("Thinking about plants", B5 + [(g_prob, 3), (g_pic, 7), (g_food, 1)]),
    ])
    make_uk(3, "parts-of-a-flowering-plant", 1, "Plants",
            "Identify and describe the functions of different parts of flowering plants: roots, stem/trunk, leaves and flowers.",
            "Parts of a Flowering Plant",
            "Year 3 Science: Parts of a Flowering Plant Worksheets (Roots, Stem, Leaves, Flowers)",
            "Parts of a Plant",
            "Free Year 3 science worksheets on the parts of a flowering plant: roots, stem, leaves and flowers, their jobs, a labelled plant and the parts we eat. 100 questions with answers.",
            "Roots, stem, leaves, flowers.",
            "Roots drink, stems hold up, leaves make food, flowers make seeds.",
            body(),
            [("What are the parts of a flowering plant?", "The main parts are the roots, the stem (a trunk on a tree), the leaves and the flowers."),
             ("What does each part do?", "Roots take in water and hold the plant still. The stem holds it up and carries water. Leaves make food using sunlight. Flowers make seeds."),
             ("Do plants eat soil?", "No. Plants make their own food in their leaves. They take in water and nutrients from the soil through their roots.")],
            sets)


if __name__ == "__main__":
    main()
