# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Cells (Systems)
  python tools/gen_sg_science_p5_cells.py
The cell is the basic unit of life. Parts of a cell: cell wall (plant cells only, gives shape and support), cell membrane
(controls what enters and leaves), cytoplasm (where most activities take place), nucleus (controls the cell's activities and
contains genetic material), chloroplasts (plant cells, contain chlorophyll to make food). Not all plant cells have chloroplasts
(onion and root cells). Using a microscope. UK Year 7 cell diagrams and microscope questions are reused (no vacuole or mitochondria).
Wrong answers come from real mistakes: "animal cells have a cell wall", "all plant cells have chloroplasts",
"the cell membrane gives the cell its shape", "cells can be seen with our eyes".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63505)
R = U.R
P = People(R)
CE = use(U, "gen_uk_science_y7_cells", drop=["vacuole", "mitochondri", "cellulose", "chemical reaction", "respiration", "magnification", "×", "DNA", "ribosome"])

PARTS = {"cell wall": ("gives the plant cell a regular shape and supports it", "plant cells only"),
         "cell membrane": ("controls what enters and leaves the cell", "both plant and animal cells"),
         "cytoplasm": ("is a jelly-like substance where most of the cell's activities take place", "both plant and animal cells"),
         "nucleus": ("controls all the activities of the cell and contains genetic material", "both plant and animal cells"),
         "chloroplast": ("contains chlorophyll to trap light energy for making food", "some plant cells only")}
WHERE = ["plant cells only", "both plant and animal cells", "animal cells only", "some plant cells only"]


def g_func():
    p = R.choice(sorted(PARTS))
    k = R.choice(["job", "name"])
    if not once(("fn", p, k)):
        return None
    job = PARTS[p][0]
    others = [x for x in sorted(PARTS) if x != p]
    if k == "job":
        return item("What is the function of the %s?" % p, "It " + job + ".", ["It " + PARTS[x][0] + "." for x in R.sample(others, 3)], "The %s %s." % (p, job))
    return item("Which part of a cell %s?" % job, "the " + p, ["the " + x for x in R.sample(others, 3)], "The %s %s." % (p, job))


def g_where():
    p = R.choice(sorted(PARTS))
    if not once(("wh", p)):
        return None
    a = PARTS[p][1]
    return item("Where is the %s found?" % p, "in " + a, ["in " + x for x in WHERE if x != a], {"cell wall": "Animal cells have no cell wall.",
                "chloroplast": "Only plant cells in the green parts, such as leaf cells, have chloroplasts."}.get(p, "Both plant and animal cells have a %s." % p))


CELLS = [("a leaf cell", True, True), ("an onion skin cell", True, False), ("a root hair cell", True, False), ("a cheek cell", False, False),
         ("a muscle cell", False, False), ("a cell from a green stem", True, True), ("a nerve cell", False, False), ("a cell from a potato", True, False)]


def g_has():
    c, plant, chl = R.choice(CELLS)
    k = R.choice(["wall", "chl"])
    if not once(("hs", c, k)):
        return None
    if k == "wall":
        return item("Does %s have a cell wall?" % c, "Yes, because it is a plant cell." if plant else "No, because it is an animal cell.",
                    ["No, because it is a plant cell.", "Yes, because it is an animal cell.", "Yes, all cells have a cell wall."] if plant else
                    ["Yes, because it is an animal cell.", "No, because it is a plant cell.", "Yes, all cells have a cell wall."], "Only plant cells have a cell wall.")
    if chl:
        return item("Does %s have chloroplasts?" % c, "Yes. It is in a green part of the plant that gets light.", ["No. No plant cells have chloroplasts.", "No. It is an animal cell.", "Only at night."],
                    "Cells in green parts have chloroplasts to make food.")
    if plant:
        return item("Does %s have chloroplasts?" % c, "No. It is a plant cell, but it is not in a green part that makes food.",
                    ["Yes. All plant cells have chloroplasts.", "No. It is an animal cell.", "Yes, but only in the day."], "Not all plant cells have chloroplasts.")
    return item("Does %s have chloroplasts?" % c, "No. It is an animal cell.", ["Yes. All cells have chloroplasts.", "Yes. It is a plant cell.", "Only in the day."],
                "Animal cells never have chloroplasts.")


def g_size():
    k = R.choice(["mm", "count"])
    if k == "mm":
        n = R.choice([10, 20, 25, 40, 50])
        if not once(("sz", n)):
            return None
        return item("A row of %d identical cells measures 1 mm. How wide is one cell?" % n, "%s mm" % ("%.2f" % (1.0 / n)).rstrip("0").rstrip("."),
                    ["%d mm" % n, "1 mm", "%s mm" % ("%.3f" % (1.0 / (n * 10))).rstrip("0").rstrip(".")], "1 ÷ %d = %s mm." % (n, ("%.2f" % (1.0 / n)).rstrip("0").rstrip(".")))
    w = R.choice([0.02, 0.05, 0.1])
    L = R.choice([1, 2, 5])
    n = int(round(L / w))
    if not once(("ct", w, L)):
        return None
    return item("Each cell is %s mm wide. How many cells would fit in a row %d mm long?" % (("%g" % w), L), str(n), [str(n * 10), str(max(1, n // 10)), str(n + L)], "%d ÷ %g = %d." % (L, w, n))


B1 = bank([
    ("What is a cell?", "the basic unit of life that all living things are made of", ["a large organ of the body", "a part of the stomach", "a kind of food"], "All living things are made of one or more cells."),
    ("Which instrument do we use to see cells?", "a microscope", ["a magnifying mirror", "a telescope", "a thermometer"], "Most cells are too small to see with our eyes."),
    ("Which parts are found in both plant and animal cells?", "cell membrane, cytoplasm and nucleus", ["cell wall and chloroplasts", "chloroplasts and nucleus", "cell wall and cell membrane only"], "Plant cells also have a cell wall and may have chloroplasts."),
    ("Which part do plant cells have that animal cells never have?", "a cell wall", ["a nucleus", "a cell membrane", "cytoplasm"], "Some plant cells also have chloroplasts."),
    ("Which part of a cell contains genetic material?", "the nucleus", ["the cell wall", "the cell membrane", "the cytoplasm"], "Genetic material is passed from parents to offspring."),
    ("Why do plant cells have a more regular shape than animal cells?", "They have a cell wall.", ["They have a nucleus.", "They have cytoplasm.", "They have no cell membrane."], "The cell wall is firm and gives shape."),
    ("Which living thing is made of only one cell?", "an amoeba", ["a cat", "a mango tree", "a mushroom"], "Some living things, such as some bacteria and amoebae, are single cells."),
    ("Why do leaf cells have many chloroplasts?", "to trap light energy to make food", ["to protect the cell", "to control the cell", "to let water in"], "Chloroplasts contain chlorophyll."),
])
B2 = bank([
    ("A cell has a cell wall but no chloroplasts. What could it be?", "an onion skin cell", ["a cheek cell", "a leaf cell", "a muscle cell"], "Onion skin cells do not get light, so they have no chloroplasts."),
    ("A cell has no cell wall and no chloroplasts. What could it be?", "a cheek cell", ["a leaf cell", "an onion cell", "a root hair cell"], "Animal cells have neither."),
    ("A cell has a cell wall and chloroplasts. What could it be?", "a leaf cell", ["a cheek cell", "a root hair cell", "a muscle cell"], "Leaf cells make food."),
    ("Why do root hair cells not have chloroplasts?", "They are under the soil and do not get light.", ["They are animal cells.", "They have no nucleus.", "They make food in the dark."], "Chloroplasts are not needed without light."),
    ("What would happen to a cell with a damaged nucleus?", "It could not control its activities properly.", ["It would make more food.", "It would grow a cell wall.", "Nothing would happen."], "The nucleus controls the cell."),
    ("What would happen if the cell membrane of a cell was damaged?", "Substances could enter and leave the cell without control.", ["The cell would make more food.", "The cell would become a plant cell.", "Nothing would happen."], "The membrane controls movement in and out."),
    ("Which part of a plant cell supports it so that the plant can stand upright?", "the cell wall", ["the nucleus", "the chloroplast", "the cytoplasm"], "Rigid cell walls help to support the plant."),
    ("How are plant and animal cells similar?", "Both have a cell membrane, cytoplasm and a nucleus.", ["Both have a cell wall.", "Both have chloroplasts.", "Neither has a nucleus."], "These parts are common to both."),
])
B3 = bank([
    ("When using a microscope, which objective lens should you start with?", "the lowest power", ["the highest power", "any lens", "no lens"], "It is easier to find the cells first at low power."),
    ("Why is iodine added to an onion cell slide?", "to stain the cells so their parts are easier to see", ["to kill the cells", "to make the cells grow", "to make the slide stick"], "The nucleus shows up clearly."),
    ("Why must the onion skin be very thin for a microscope slide?", "so that light can pass through it", ["so that it is easier to cut", "so that it tastes better", "so that it is heavier"], "Light passes through thin samples to show the cells."),
    ("Why should you never point a microscope mirror at the Sun?", "Strong sunlight can damage your eyes.", ["It makes the cells move.", "It makes the image too dark.", "It breaks the slide."], "Use a lamp or daylight instead."),
    ("Which part of the microscope holds the slide?", "the stage", ["the eyepiece", "the objective lens", "the fine focusing knob"], "The slide is clipped onto the stage."),
])
B5 = bank([
    ("Siti looked at cells from a green leaf and from an onion under a microscope. Which part did she see only in the leaf cells?", "chloroplasts", ["a nucleus", "a cell wall", "cytoplasm"], "Both are plant cells; only the leaf cells have chloroplasts."),
    ("Ravi looked at cheek cells and onion cells. Which part did he see only in the onion cells?", "a cell wall", ["a nucleus", "a cell membrane", "cytoplasm"], "Cheek cells are animal cells."),
    ("Cell X has a nucleus, a cell membrane, cytoplasm and a cell wall. Cell Y has a nucleus, a cell membrane and cytoplasm only. Which statement is correct?", "X is a plant cell and Y is an animal cell.", ["X is an animal cell and Y is a plant cell.", "Both are animal cells.", "Both are leaf cells."], "Only plant cells have a cell wall."),
    ("A cell has a nucleus, cytoplasm, a cell membrane, a cell wall and chloroplasts. Where in a plant is it most likely from?", "the leaf", ["the root", "inside the potato", "the seed coat"], "Leaf cells are exposed to light and make food."),
    ("A pupil drew a cheek cell with a cell wall. What mistake did she make?", "Animal cells do not have a cell wall.", ["Cheek cells have chloroplasts.", "Cheek cells have no nucleus.", "Cheek cells have no cell membrane."], "Only plant cells have a cell wall."),
])


def body():
    think = ("<p><b>All living things are made of cells. The cell is the basic unit of life.</b></p>"
             "<ul><li><b>Cell membrane</b>: controls what enters and leaves the cell.</li>"
             "<li><b>Cytoplasm</b>: jelly-like; most activities happen here.</li>"
             "<li><b>Nucleus</b>: controls the cell's activities; contains genetic material.</li>"
             "<li><b>Cell wall</b> (plant cells only): gives a regular shape and support.</li>"
             "<li><b>Chloroplasts</b> (plant cells in green parts): contain chlorophyll to make food.</li></ul>")
    ex = [("A cell has a cell wall but no chloroplasts. Is it a plant or an animal cell?", ["Only plant cells have a cell wall", "It may be from a root or an onion"], "A plant cell."),
          ("Why can we not see cells with our eyes?", ["Most cells are very small", "We need a microscope"], "They are too small.")]
    mist = ["Thinking animal cells have a cell wall. Only plant cells do.",
            "Thinking all plant cells have chloroplasts. Root and onion cells do not.",
            "Mixing up the cell wall and the cell membrane. The membrane controls movement in and out; the wall gives shape.",
            "Starting with the high-power lens on a microscope. Start with low power."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a cell", B1 + [(g_func, 8), (CE.g_pic, 4)]),
        ("Plant and animal cells", B2 + [(g_where, 5), (g_has, 7)]),
        ("Cell diagrams", CE.B1 + [(CE.g_pic, 8), (g_func, 2), (g_has, 5)]),
        ("Using a microscope", B3 + CE.B5 + [(CE.g_mic, 6), (g_size, 3), (g_has, 2)]),
        ("PSLE-style questions", B5 + [(g_has, 4), (CE.g_pic, 5), (g_size, 3), (g_where, 3)]),
    ])
    make_sg(5, "cells", 5, "Systems", "Cell system",
            "Recognise that the cell is the basic unit of life. Identify the parts of plant and animal cells (cell wall, cell membrane, cytoplasm, nucleus, chloroplasts) "
            "and their functions, and compare plant and animal cells (summary of the MOE Primary Science Syllabus).",
            "Cells: Plant and Animal Cells",
            "Primary 5 Science: Cells Worksheets – Plant and Animal Cells (with Answers)",
            "Cells",
            "Free Primary 5 science worksheets for Singapore pupils on cells: cell wall, cell membrane, cytoplasm, nucleus and chloroplasts, plant and animal cells, and using a microscope. 100 questions with answers.",
            "The cell is the basic unit of life.",
            "Plant cells have a cell wall and may have chloroplasts.",
            body(),
            [("What is the difference between plant and animal cells?", "Plant cells have a cell wall and many have chloroplasts. Animal cells have neither. Both have a cell membrane, cytoplasm and a nucleus."),
             ("Do all plant cells have chloroplasts?", "No. Only cells in the green parts that get light, such as leaf cells. Root cells and onion cells do not have chloroplasts."),
             ("What does the nucleus do?", "It controls all the activities of the cell and contains the genetic material.")],
            sets)


if __name__ == "__main__":
    main()
