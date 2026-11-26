# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Biology): Specialised Cells and Organisation
  python tools/gen_uk_science_y7_specialised_cells_and_organisation.py
The hierarchical organisation of multicellular organisms (cells, tissues, organs, organ systems, organisms);
specialised cells and how their features fit their jobs; the role of diffusion in the movement of materials in and
between cells; and unicellular organisms.
Wrong answers come from real mistakes: "an organ is smaller than a tissue", "all cells look the same", "diffusion
goes from low to high concentration", "unicellular organisms are not alive".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, People, once

U = Unit(61702)
R = U.R
P = People(R)

LEV = ["cell", "tissue", "organ", "organ system", "organism"]
EX = [("a muscle cell", "cell"), ("a red blood cell", "cell"), ("a root hair cell", "cell"), ("muscle tissue", "tissue"), ("blood", "tissue"),
      ("the lining of the stomach", "tissue"), ("the heart", "organ"), ("the stomach", "organ"), ("a leaf", "organ"), ("the brain", "organ"),
      ("the lungs", "organ"), ("the digestive system", "organ system"), ("the circulatory system", "organ system"), ("the nervous system", "organ system"),
      ("a human", "organism"), ("an oak tree", "organism"), ("a dog", "organism"), ("a nerve cell", "cell"), ("an egg cell", "cell"), ("nerve tissue", "tissue"),
      ("the kidney", "organ"), ("the skin", "organ"), ("the respiratory system", "organ system"), ("the skeletal system", "organ system"), ("a sunflower", "organism"),
      ("a goldfish", "organism"), ("fat tissue", "tissue")]


def g_level():
    k = R.random() < 0.6
    if k:
        x, l = R.choice(EX)
        if not once(("lv", x)):
            return None
        return item("%s %s a cell, a tissue, an organ, an organ system or an organism?" % ("Are" if x == "the lungs" else "Is", x), "an " + l if l[0] in "aeiou" else "a " + l,
                    [("an " + y if y[0] in "aeiou" else "a " + y) for y in R.sample([y for y in LEV if y != l], 3)], "Cells → tissues → organs → organ systems → organisms.")
    i = R.randrange(len(LEV) - 1)
    b = R.random() < 0.5
    if not once(("lo", i, b)):
        return None
    if b:
        a = LEV[i + 1]
        return item("Which level of organisation comes after %s?" % LEV[i], a, R.sample([y for y in LEV if y not in (a, LEV[i])], 3), "Cells → tissues → organs → organ systems → organisms.")
    a = LEV[i]
    return item("Which level of organisation comes just before %s?" % LEV[i + 1], a, R.sample([y for y in LEV if y not in (a, LEV[i + 1])], 3), "Cells → tissues → organs → organ systems → organisms.")


SPEC = [("a red blood cell", "has no nucleus and a dimpled shape to carry lots of oxygen"), ("a nerve cell", "is long with branches to carry electrical messages"),
        ("a sperm cell", "has a tail to swim to the egg"), ("an egg cell", "is large and contains a food store for the growing embryo"),
        ("a root hair cell", "has a long, thin hair to take in water from the soil"), ("a palisade leaf cell", "is packed with chloroplasts for photosynthesis"),
        ("a ciliated cell", "has tiny hairs that sweep mucus out of the airways"), ("a muscle cell", "has lots of mitochondria and can contract")]


def g_spec():
    c, f = R.choice(SPEC)
    k = R.random() < 0.5
    if not once(("sp", c, k)):
        return None
    if k:
        return item("How is %s adapted for its job?" % c, "It " + f + ".", ["It " + x[1] + "." for x in R.sample([x for x in SPEC if x[0] != c], 3)], "Specialised cells have features that suit their jobs.")
    return item("Which specialised cell %s?" % f, c, R.sample([x[0] for x in SPEC if x[0] != c], 3), "Specialised cells have features that suit their jobs.")


DIFF = [("oxygen", "from the air in the lungs", "into the blood"), ("carbon dioxide", "from the blood", "into the air in the lungs"), ("glucose", "from the blood", "into body cells"),
        ("oxygen", "from the blood", "into muscle cells"), ("the smell of perfume", "from near the bottle", "across the room"), ("ink", "from the drop", "through the water"),
        ("oxygen", "from inside a leaf", "out into the air in sunlight"), ("carbon dioxide", "from muscle cells", "into the blood")]


def g_diff():
    k = R.random() < 0.5
    if k:
        s, a, b = R.choice(DIFF)
        if not once(("di", s, a)):
            return None
        return item("By diffusion, which way does %s move here: %s or %s?" % (s, a, b), "%s %s" % (a, b), ["%s %s" % (b.replace("into", "from"), a.replace("from", "into")), "it does not move at all", "only when we exercise"],
                    "Particles diffuse from where there are a lot of them (high concentration) to where there are fewer (low concentration).")
    c1, c2 = R.sample(range(2, 30), 2)
    s = R.choice(["oxygen", "glucose", "carbon dioxide", "a dye"])
    if not once(("dn", c1, c2, s)) or not once(("ds", s), 12):
        return None
    a = "from cell A to cell B" if c1 > c2 else "from cell B to cell A"
    return item("Cell A has %d units of %s and cell B has %d units. Which way will %s diffuse?" % (c1, s, c2, s.replace("a dye", "the dye")), a,
                ["from cell B to cell A" if c1 > c2 else "from cell A to cell B", "it will not move", "it will move both ways equally for ever"], "Diffusion goes from high to low concentration.")


B1 = bank([
    ("What is a tissue?", "a group of similar cells working together", ["a single cell", "a whole organism", "a group of organs"], "Muscle tissue."),
    ("What is an organ?", "a group of different tissues working together", ["a single cell", "one type of cell only", "a whole animal"], "The heart, the stomach."),
    ("What is an organ system?", "a group of organs working together", ["a single tissue", "a single cell", "a type of food"], "The digestive system."),
    ("What does multicellular mean?", "made of many cells", ["made of one cell", "made of no cells", "made of metal"], "Humans, trees, dogs."),
    ("What is diffusion?", "the spreading out of particles from high to low concentration", ["particles moving from low to high concentration", "a kind of cell", "the way muscles contract"], "Smells spreading."),
    ("Why are some cells called specialised?", "They have special features for a particular job.", ["They are all identical.", "They are very old.", "They have no nucleus at all."], "Shape fits job."),
    ("Which organ system includes the heart and blood vessels?", "the circulatory system", ["the digestive system", "the nervous system", "the skeletal system"], "It moves blood."),
    ("Which organ system breaks down food?", "the digestive system", ["the circulatory system", "the respiratory system", "the nervous system"], "Mouth to intestines."),
])
B5 = bank([
    ("What is an amoeba?", "a unicellular organism that moves and feeds by changing shape", ["a multicellular animal", "a type of tissue", "a plant organ"], "One cell does everything."),
    ("Why does euglena have both a chloroplast and an eyespot?", "It can make food in light and swims towards light.", ["It is a plant cell only.", "It needs no light.", "It is an organ."], "A unicellular organism."),
    ("Why does diffusion happen faster when it is warmer?", "Particles move faster.", ["Particles move slower.", "Warm cells have no membrane.", "It does not change."], "Temperature affects diffusion."),
    ("Why do the lungs have a huge surface area?", "so lots of oxygen can diffuse into the blood quickly", ["to make the lungs heavy", "to store food", "to stop diffusion"], "Bigger surface, faster diffusion."),
    ("A red blood cell has no nucleus. What is the advantage?", "There is more room to carry oxygen.", ["It can divide faster.", "It can photosynthesise.", "It is stronger."], "Adaptation."),
])


def body():
    think = ("<p><b>Multicellular organisms are organised in levels.</b></p>"
             "<ul><li>Cells → tissues → organs → organ systems → organism.</li>"
             "<li>Specialised cells have features for their jobs, such as the tail of a sperm cell or the long hair of a root hair cell.</li>"
             "<li>Substances move in and out of cells by diffusion, from high to low concentration.</li></ul>")
    ex = [("The stomach is an?", ["Made of several tissues"], "organ"),
          ("Oxygen in the lungs moves which way?", ["High to low"], "into the blood")]
    mist = ["Thinking an organ is smaller than a tissue.", "Thinking diffusion goes from low to high concentration.", "Thinking all cells look the same."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Levels of organisation", B1 + [(g_level, 12)]),
        ("Cells, tissues and organs", [(g_level, 12), (g_spec, 8)]),
        ("Specialised cells", [(g_spec, 8), (g_diff, 12)]),
        ("Diffusion", [(g_diff, 16), (g_level, 4)]),
        ("Thinking about cells", B5 + [(g_diff, 10), (g_level, 5)]),
    ])
    make_ks3(7, "specialised-cells-and-organisation", 2, "Biology", "Cells and organisation",
             "The hierarchical organisation of multicellular organisms: from cells to tissues to organs to systems to organisms; the role of diffusion in the movement of materials in and between cells; the structural adaptations of some unicellular organisms.",
             "Specialised Cells and Organisation",
             "Year 7 Science: Specialised Cells, Tissues, Organs and Diffusion Worksheets",
             "Specialised Cells",
             "Free Year 7 science worksheets on specialised cells and organisation: cells, tissues, organs and organ systems, adapted cells, diffusion and unicellular organisms. 100 questions with answers.",
             "Cells → tissues → organs → systems.",
             "Specialised cells suit their jobs; substances diffuse from high to low concentration.",
             body(),
             [("What are the levels of organisation?", "Cells group into tissues, tissues into organs, organs into organ systems, and organ systems make up an organism."),
              ("What is a specialised cell?", "A cell with features suited to a particular job, such as a nerve cell that is long to carry messages."),
              ("What is diffusion?", "The spreading of particles from where there are many (high concentration) to where there are fewer (low concentration).")],
             sets)


if __name__ == "__main__":
    main()
