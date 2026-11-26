# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Plant Structures and Their Functions (4-LS1-1)
  python tools/gen_us_science_g4_plant_structures.py
Plants have internal and external structures that support growth, survival and reproduction:
roots (water, anchor), stems (support, carry water), leaves (make food from sunlight), flowers
(make seeds), fruits (protect and spread seeds), thorns and spines (protection), bark, waxy coatings.
Wrong answers come from real mistakes: "plants get food from the soil through roots",
"flowers are only for decoration", "all leaves do the same job in every plant".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, line, circle, rect, text, classifier, People, INK, LEAF, BROWN, RED, SUN

U = Unit(40109)
R = U.R
P = People(R)

JOB = {"roots": "to take in water and hold the plant in the ground",
       "stem": "to hold the plant up and carry water and food",
       "leaves": "to use sunlight to make food",
       "flower": "to make seeds so new plants can grow",
       "fruit": "to protect seeds and help spread them",
       "thorns": "to protect the plant from animals that eat it",
       "bark": "to protect the trunk of a tree"}
JOB3 = {"roots": "takes in water and holds the plant in the ground", "stem": "holds the plant up and carries water and food",
        "leaves": "uses sunlight to make food", "flower": "makes seeds so new plants can grow", "fruit": "protects seeds and helps spread them",
        "thorns": "protects the plant from animals that eat it", "bark": "protects the trunk of a tree"}
WRONGJOB = ["to take in food from the soil", "to make the plant heavier", "to keep the plant warm at night", "to let the plant walk to water"]


def plant(marks):
    """A flowering plant with lettered arrows pointing to parts. marks: {part: letter}."""
    W, H = 280, 260
    g = 190
    s = [rect(0, g, W, H - g, "#e8d6b5", "none", 0), line(0, g, W, g, BROWN, 2)]
    # roots
    for dx, dy in [(-30, 40), (-10, 55), (15, 50), (35, 35), (0, 30)]:
        s.append("<path d='M140 %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='3'/>" % (g, 140 + dx // 2, g + dy // 2, 140 + dx, g + dy, BROWN))
    s.append(line(140, g, 140, 70, LEAF, 5))
    for side, y in [(-1, 150), (1, 125), (-1, 100)]:
        s.append("<path d='M140 %d Q%d %d %d %d Q%d %d 140 %d Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (y, 140 + side * 30, y - 25, 140 + side * 60, y - 10, 140 + side * 30, y + 8, y, LEAF, INK))
    for k in range(6):
        import math
        a = k * math.pi / 3
        s.append(circle(140 + 14 * math.cos(a), 55 + 14 * math.sin(a), 10, RED, INK, 1))
    s.append(circle(140, 55, 8, SUN, INK, 1))
    pos = {"flower": (140, 40, 220, 30), "leaves": (195, 116, 240, 95), "stem": (142, 170, 220, 175), "roots": (160, 225, 230, 240)}
    for part, letter in marks.items():
        x0, y0, x1, y1 = pos[part]
        s.append(line(x0, y0, x1 - 10, y1, INK, 1.5) + circle(x0, y0, 3, INK, INK, 0) + text(x1, y1 + 6, letter, 18))
    return svg_wrap(W, H, "".join(s), "a flowering plant with parts labeled " + ", ".join(sorted(marks.values())))


def g_label():
    parts = ["flower", "leaves", "stem", "roots"]
    letters = list("ABCD")
    R.shuffle(letters)
    m = dict(zip(parts, letters))
    p = R.choice(parts)
    k = R.choice(["job", "name", "what"])
    if k == "job":
        return item(fig(plant(m)) + "Which part of this plant %s?" % JOB3[p], m[p], [m[x] for x in parts if x != p], "Part %s points to the %s. This part %s." % (m[p], p, JOB3[p]))
    if k == "name":
        return item(fig(plant(m)) + "Which letter points to the %s?" % p, m[p], [m[x] for x in parts if x != p], "Part %s points to the %s. This part %s." % (m[p], p, JOB3[p]))
    return item(fig(plant(m)) + "What is the main job of part %s?" % m[p], JOB[p],
                [JOB[x] for x in parts if x != p][:2] + [R.choice(WRONGJOB)], "Part %s points to the %s. This part %s." % (m[p], p, JOB3[p]))


PARTS = {"roots": ["roots", "a carrot's thick root", "a tree's deep roots", "the roots of a dandelion"],
         "stem": ["a stem", "a tree trunk", "a sunflower's tall stalk", "a celery stalk"],
         "leaves": ["leaves", "a spinach leaf", "a maple leaf", "the needles of a pine tree"],
         "flower": ["a flower", "an apple blossom", "a tulip", "a daisy"],
         "fruit": ["a fruit", "an apple", "a tomato", "a pea pod"],
         "thorns": ["thorns", "the spines of a cactus", "the thorns on a rose stem", "the prickles on a blackberry bush"]}


def f_which():
    k = R.choice(sorted(PARTS))
    a = R.choice(PARTS[k][1:])
    others = [x for c in PARTS if c != k for x in PARTS[c][1:]]
    return item("Which plant structure has the main job %s?" % JOB[k], a, R.sample(others, 3), "%s is a kind of %s. It %s." % (a[0].upper() + a[1:], k, JOB3[k]))


def g_struct_job():
    k = R.choice(sorted(PARTS))
    x = R.choice(PARTS[k][1:])
    wrong = [JOB[j] for j in JOB if j != k and {j, k} != {"thorns", "bark"}]
    return item("What is the main job of %s?" % x, JOB[k], R.sample(wrong, 2) + [R.choice(WRONGJOB)], "%s is a kind of %s. It %s." % (x[0].upper() + x[1:], k, JOB3[k]))


ADAPT = [("a cactus", "thick, waxy stems that store water", "living in a hot, dry desert", ["thin, wide leaves that lose water fast", "no roots", "bright red flowers in winter"]),
         ("a water lily", "wide, flat leaves that float on water", "getting sunlight in a pond", ["sharp thorns under water", "deep roots in sand", "a thick woody trunk"]),
         ("a pine tree", "thin needles with a waxy coating", "surviving cold, snowy winters", ["huge soft leaves", "flowers that float", "no bark"]),
         ("a rose bush", "sharp thorns on its stems", "keeping animals from eating it", ["leaves that float", "roots on top of the soil", "a waxy cactus stem"]),
         ("a mangrove tree", "roots that stick up out of salty mud", "living in wet, salty swamps", ["thin needles", "a thick waxy stem", "thorny flowers"]),
         ("a sunflower", "a tall, strong stem", "growing tall above other plants to get sunlight", ["roots that float", "a waxy needle coating", "underground flowers"]),
         ("a dandelion", "seeds with fluffy parachutes", "spreading seeds far away on the wind", ["heavy seeds that sink", "sharp thorns", "floating leaves"]),
         ("a coconut palm", "fruits that can float on the ocean", "spreading seeds to new islands", ["seeds with hooks", "needles with wax", "underground fruits"]),
         ("a burdock plant", "seeds with tiny hooks", "spreading seeds by sticking to animal fur", ["seeds that float", "waxy leaves", "a tall stalk"]),
         ("a tree", "thick bark on its trunk", "protecting it from insects and fire", ["thin, soft bark", "floating leaves", "no roots"]),
         ("a vine", "curly tendrils that wrap around things", "climbing up fences and trees", ["roots in the air only", "thorny seeds", "a waxy cactus stem"])]


def g_adapt():
    pl, st, why, w = R.choice(ADAPT)
    if R.random() < 0.5:
        return item("Which structure helps %s with %s?" % (pl, why), st, w, "%s has %s. This helps with %s." % (pl[0].upper() + pl[1:], st, why))
    return item("%s has %s. How does this structure help the plant?" % (pl[0].upper() + pl[1:], st), "It helps with %s." % why,
                ["It helps with %s." % x for x in R.sample([a[2] for a in ADAPT if a[0] != pl], 3)], "This structure is suited to %s." % why)


B1 = bank([
    ("Where does a plant make its food?", "mostly in its leaves, using sunlight", ["in its roots, from the soil", "in its flowers", "in its seeds"],
     "Leaves use sunlight, air and water to make food (sugar). Plants do not get food from the soil."),
    ("What do roots take in from the soil?", "water and minerals", ["sunlight", "food that is ready to eat", "seeds"], "Roots also hold the plant in place."),
    ("Which part of a plant carries water from the roots to the leaves?", "the stem", ["the flower", "the seed", "the fruit"],
     "Tiny tubes inside the stem carry water up and food down."),
    ("Which structure is inside the plant (internal)?", "tubes in the stem that carry water", ["thorns", "petals", "bark"], "Some structures are inside and cannot be seen from outside."),
    ("What is the job of the bright petals on many flowers?", "to attract insects and birds that carry pollen", ["to take in water", "to hold the plant up", "to store food for winter"],
     "Pollinators help the flower make seeds."),
    ("What grows inside a fruit?", "seeds", ["roots", "leaves", "bark"], "A fruit protects the seeds and helps spread them."),
    ("What do plant structures help a plant do?", "grow, survive and make new plants", ["walk to water", "make noise", "hunt for food"],
     "Each structure has a job."),
    ("Why does a tree have bark?", "to protect the inside of the trunk", ["to make seeds", "to take in sunlight", "to attract bees"], "Bark is like a tree's skin."),
])
B5 = bank([
    ("Ava pulls out one plant with long roots and one with short roots after a dry week. The long-rooted plant was still green. Why?", "Long roots can reach water deeper in the soil.", ["Short roots make food.", "Long roots block sunlight.", "Roots have nothing to do with water."],
     "Deeper roots reach water that is farther down."),
    ("Leo puts a white carnation in a cup of blue water. A day later the petals have blue streaks. What does this show?", "The stem carries water up to the flower.", ["Flowers make blue color.", "Petals take in water from the air.", "Roots make the flower blue."],
     "Colored water travels up tubes in the stem."),
    ("Mia covers one leaf of a plant with foil for a week. The covered leaf turns pale. Why?", "The leaf could not get sunlight to make food.", ["Foil adds too much water.", "The leaf got too much food.", "Foil makes leaves grow faster."],
     "Leaves need sunlight to make food."),
    ("Why do many desert plants have small leaves or spines instead of large leaves?", "Less water escapes from small leaves and spines.", ["Big leaves would freeze.", "Spines make food faster.", "Small leaves catch more rain."],
     "Large, thin leaves lose a lot of water in hot, dry air."),
    ("Noah grows one bean plant in a sunny window and one in a dark closet. Which structure of the plant in the closet cannot do its job?", "its leaves", ["its roots", "its stem", "its seeds"],
     "Leaves need light to make food."),
])


def body():
    think = ("<p>Plants have <b>structures</b> (parts) that help them grow, survive and make new plants. Each structure has a job:</p>"
             "<ul><li><b>Roots</b>: take in water and minerals and hold the plant in place.</li>"
             "<li><b>Stem</b>: holds the plant up; tubes inside carry water and food.</li>"
             "<li><b>Leaves</b>: use sunlight to make food.</li>"
             "<li><b>Flowers</b>: make seeds. <b>Fruits</b> protect and spread seeds.</li>"
             "<li><b>Thorns, spines and bark</b>: protect the plant.</li></ul>"
             + figure(plant({"flower": "A", "leaves": "B", "stem": "C", "roots": "D"}), "A flower, B leaves, C stem, D roots.")
             + "<p>Plants in different places have structures that fit their surroundings, like the thick, waxy stem of a cactus.</p>")
    ex = [("Which part of a plant makes food?", ["Food is made with sunlight.", "Leaves catch sunlight."], "the leaves"),
          ("How do a cactus's spines help it?", ["Spines are sharp.", "Animals do not want to bite them."], "They protect it from animals that would eat it.")]
    mist = ["Thinking plants get their food from the soil. Roots take in water and minerals; leaves make food.",
            "Thinking flowers are only for decoration. They make seeds.",
            "Forgetting internal structures, like the tubes inside a stem."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a plant", B1 + [(g_label, 6), (g_struct_job, 6)]),
        ("What each part does", [(g_label, 8), (g_struct_job, 8), (f_which, 4)]),
        ("Structures for survival", [(g_adapt, 12), (g_struct_job, 4), (g_label, 4)]),
        ("Plants in different places", [(g_adapt, 10), (f_which, 6), (g_label, 4)]),
        ("Plant investigations", B5 + [g_adapt, g_label, g_struct_job, f_which]),
    ])
    make("grade-4", "plant-structures", 9, "4-LS1-1",
         "Construct an argument that plants and animals have internal and external structures that function to support survival, growth, behavior, and reproduction.",
         "Plant Structures and Their Functions",
         "Grade 4 Plant Structures Worksheets: Roots, Stems, Leaves, Flowers and Adaptations",
         "Plant Structures",
         "Free Grade 4 science worksheets on plant structures (NGSS 4-LS1-1): roots, stems, leaves, flowers, fruits, thorns and bark, labeled plant diagrams and structures that help plants survive. 100 practice questions with answers.",
         "Every plant structure has a job.",
         "Roots take in water, stems hold the plant up, leaves make food, and flowers make seeds.",
         body(),
         [("What are the main parts of a plant?", "Roots, stem, leaves and flowers. Many plants also have fruits and seeds."),
          ("Do plants get food from the soil?", "No. Roots take in water and minerals. Leaves use sunlight, air and water to make the plant's food."),
          ("How do structures help plants survive?", "Thorns and spines protect plants, waxy coatings save water, and fruits help spread seeds to new places.")],
         sets)


if __name__ == "__main__":
    main()
