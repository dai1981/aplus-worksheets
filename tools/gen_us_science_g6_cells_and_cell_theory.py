# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Cells and Cell Theory (MS-LS1-1)
  python tools/gen_us_science_g6_cells_and_cell_theory.py
All living things are made of cells; a living thing may be one cell (unicellular) or many different
numbers and types of cells (multicellular). Cell theory; evidence from microscopes; total magnification
(eyepiece × objective); different cell types (nerve, muscle, red blood, skin, leaf cells).
Assessment boundary: no cell parts in detail (MS-LS1-2), no microscope mechanics beyond magnification.
Wrong answers come from real mistakes: "only animals are made of cells", "a virus is a cell",
"bigger organisms have bigger cells", "magnifications add".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(60101)
R = U.R
P = People(R)

UNI = ["bacteria", "an amoeba", "a paramecium", "yeast", "a euglena", "diatoms"]
MULTI = ["a mushroom", "an oak tree", "a human", "a frog", "an earthworm", "moss", "a dog", "a sunflower", "a goldfish", "a honeybee"]
NONLIVING = ["a rock", "a cloud", "a plastic bottle", "a grain of sand", "a drop of water", "a metal spoon", "a candle flame", "a virus"]


def g_uni():
    k = R.choice(["uni", "multi"])
    p = P.next()
    if k == "uni":
        return item("%s looks at pond water under a microscope. Which organism is made of only one cell?" % p[0], R.choice(UNI), R.sample(MULTI, 3),
                    "Unicellular organisms, like bacteria, amoebas and yeast, are made of a single cell.")
    return item("%s makes a list of organisms. Which one is multicellular?" % p[0], R.choice(MULTI), R.sample(UNI, 3),
                "Multicellular organisms are made of many cells, often of different types.")


def g_living():
    p = P.next()
    k = R.choice(["cells", "not"])
    if k == "cells":
        return item("%s says, “If it is made of cells, it is alive.” Which of these is made of cells?" % p[0], R.choice(UNI + MULTI), R.sample(NONLIVING, 3),
                    "All living things are made of one or more cells.")
    return item("%s sorts objects. Which one is NOT made of cells?" % p[0], R.choice(NONLIVING), R.sample(UNI + MULTI, 3),
                "Nonliving things are not made of cells. (A virus is not a cell; it cannot live on its own.)")


def X(n):
    return comma(n) + "×"


def g_mag():
    eye = R.choice([5, 10, 15, 20])
    obj = R.choice([4, 10, 40, 100])
    p = P.next()
    tot = eye * obj
    if R.random() < 0.5:
        return item("%s's microscope has a %s eyepiece and a %s objective lens. What is the total magnification?" % (p[0], X(eye), X(obj)), X(tot),
                    [X(eye + obj), X(obj), X(tot * 10)], "Total magnification = eyepiece × objective = %d × %d = %s." % (eye, obj, X(tot)))
    return item("A microscope with a %s eyepiece shows a total magnification of %s. What objective lens is being used?" % (X(eye), X(tot)), X(obj),
                [X(tot - eye), X(eye), X(tot * eye)] if tot - eye != obj else [X(eye), X(tot * eye), X(obj * 2)],
                "%s ÷ %d = %d." % (comma(tot), eye, obj))


def g_size():
    cell = R.choice([("a red blood cell", 8), ("a bacterium", 2), ("a human skin cell", 30), ("an amoeba", 400), ("a plant leaf cell", 50), ("a human egg cell", 100)])
    mag = R.choice([100, 400, 1000])
    looks = cell[1] * mag // 1000
    if looks < 1:
        return None
    p = P.next()
    return item("%s is about %d micrometers wide. Under a %s microscope, about how wide does it appear?" % (cell[0][0].upper() + cell[0][1:], cell[1], X(mag)),
                "%d millimeters" % looks, ["%d millimeters" % (looks * 10), "%d micrometers" % cell[1], "%d millimeters" % max(1, looks // 10) if looks >= 10 else "%d centimeters" % (looks * 10)],
                "%d micrometers × %s = %s micrometers, or about %d mm (1 mm = 1,000 micrometers)." % (cell[1], comma(mag), comma(cell[1] * mag), looks))


TYPES = [("nerve cell", "long branches that carry messages through the body"), ("muscle cell", "long, thin shape that can contract to move the body"),
         ("red blood cell", "small disk shape that carries oxygen"), ("skin cell", "flat shape that covers and protects the body"),
         ("leaf cell", "many chloroplasts that capture sunlight"), ("root hair cell", "long thin extension that takes in water"),
         ("sperm cell", "tail that helps it swim"), ("white blood cell", "can change shape to surround germs")]


def g_type():
    t, f = R.choice(TYPES)
    k = R.choice(["shape", "which"])
    if k == "shape":
        return item("Which feature helps a %s do its job?" % t, f, [x[1] for x in R.sample([y for y in TYPES if y[0] != t], 3)], "A %s has a %s." % (t, f))
    return item("Which type of cell has a %s?" % f, "a " + t, ["a " + x[0] for x in R.sample([y for y in TYPES if y[0] != t], 3)], "The shape of a cell fits its job.")


B1 = bank([
    ("What does the cell theory say?", "All living things are made of cells, cells are the basic unit of life, and new cells come from existing cells.", ["Only animals are made of cells.", "Cells come from nonliving things.", "Cells are found only in plants."],
     "These three ideas were built from many microscope observations."),
    ("What is a cell?", "the smallest unit that can carry out all the processes of life", ["a kind of tissue", "an organ", "a nonliving particle"], "Cells are the building blocks of living things."),
    ("What does unicellular mean?", "made of only one cell", ["made of many cells", "made of no cells", "made of two kinds of cells"], "Bacteria are unicellular."),
    ("Why were microscopes important for discovering cells?", "Most cells are too small to see without magnification.", ["Microscopes make cells.", "Cells are very large.", "Microscopes kill germs."],
     "Robert Hooke and Antonie van Leeuwenhoek used microscopes in the 1600s."),
    ("Do larger animals have larger cells?", "No. Larger animals usually have more cells, not bigger cells.", ["Yes, always.", "Only elephants.", "Only plants."], "An elephant has many more cells than a mouse."),
    ("Is a virus a living cell?", "No. A virus is not a cell and cannot reproduce on its own.", ["Yes, it is the smallest cell.", "Yes, it is a plant cell.", "Only in winter."],
     "Viruses need a host cell to make copies."),
    ("Where do new cells come from?", "from existing cells that divide", ["from rocks", "from air", "from water only"], "Cells divide to make new cells."),
    ("A human body is made of about", "tens of trillions of cells of many types", ["one very large cell", "about 100 cells", "cells of only one type"], "There are about 200 types of human cells."),
])
B5 = bank([
    ("Ava looks at onion skin and cheek cells under a microscope. What evidence supports cell theory?", "Both the plant and the animal sample are made of cells.", ["Only the onion has cells.", "Only the cheek has cells.", "Neither has cells."],
     "Different living things are all made of cells."),
    ("Leo sees tiny moving things in pond water. How can he tell if they are living?", "Check whether they are made of cells and show signs of life like growing and responding.", ["See if they are green.", "Count them.", "See if they are round."],
     "Living things are made of cells."),
    ("Mia switches from the 10× to the 40× objective. What happens to the image?", "It looks larger, and she sees a smaller area of the slide.", ["It looks smaller.", "It looks the same.", "The cells disappear."],
     "Higher magnification shows less of the slide in more detail."),
    ("Why do scientists stain cells before looking at them?", "to make cell parts easier to see", ["to kill all the cells", "to make cells bigger", "to turn cells into plants"],
     "Many cells are nearly clear."),
    ("A student sees no cells in a sample of salt crystals. What does this suggest?", "Salt is not a living thing.", ["Salt is a unicellular organism.", "The microscope is broken for sure.", "Salt cells are invisible."],
     "Nonliving things are not made of cells."),
])


def body():
    think = ("<p>The <b>cell theory</b> says:</p><ol><li>All living things are made of one or more <b>cells</b>.</li><li>The cell is the basic unit of life.</li><li>New cells come from existing cells.</li></ol>"
             "<p><b>Unicellular</b> organisms (bacteria, yeast, amoebas) are a single cell. <b>Multicellular</b> organisms (plants, animals, mushrooms) are made of many cells, "
             "often of different types, such as nerve, muscle and blood cells. Each cell type has a shape that fits its job.</p>"
             "<p>Most cells are too small to see, so we use a <b>microscope</b>. Total magnification = eyepiece × objective (10× × 40× = 400×).</p>")
    ex = [("Is yeast unicellular or multicellular?", ["Yeast is one cell."], "unicellular"),
          ("A 10× eyepiece and a 100× objective give what magnification?", ["10 × 100"], "1,000×")]
    mist = ["Thinking only animals are made of cells. Plants, fungi and bacteria are too.",
            "Adding magnifications. Multiply them.",
            "Thinking bigger organisms have bigger cells. They have more cells."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Cell theory", B1 + [(g_uni, 6), (g_living, 6)]),
        ("One cell or many?", [(g_uni, 12), (g_living, 8)]),
        ("Microscopes and magnification", [(g_mag, 14), (g_size, 6)]),
        ("Types of cells", [(g_type, 14), (g_living, 6)]),
        ("Investigating cells", B5 + [g_mag, g_type, g_uni, g_size]),
    ])
    make("grade-6", "cells-and-cell-theory", 1, "MS-LS1-1",
         "Conduct an investigation to provide evidence that living things are made of cells; either one cell or many different numbers and types of cells.",
         "Cells and Cell Theory",
         "Grade 6 Cells Worksheets: Cell Theory, Unicellular and Multicellular Organisms, Microscopes",
         "Cells and Cell Theory",
         "Free middle school science worksheets on cells and cell theory (NGSS MS-LS1-1): unicellular and multicellular organisms, types of cells, microscopes and total magnification. 100 practice questions with answers.",
         "All living things are made of cells.",
         "Some organisms are one cell; others are made of trillions of cells of many types. Microscopes let us see them.",
         body(),
         [("What are the three parts of the cell theory?", "All living things are made of cells, the cell is the basic unit of life, and new cells come from existing cells."),
          ("What is the difference between unicellular and multicellular organisms?", "Unicellular organisms are made of one cell. Multicellular organisms are made of many cells, often of different types."),
          ("How do you find total magnification?", "Multiply the eyepiece magnification by the objective magnification. For example, 10× × 40× = 400×.")],
         sets)


if __name__ == "__main__":
    main()
