# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Biology): Cell Division
  python tools/gen_uk_science_y10_cell_division.py
Chromosomes, the cell cycle and mitosis, growth and repair, differentiation, stem cells (embryonic, adult bone marrow,
plant meristems), therapeutic cloning, and the benefits and risks of stem cell treatments. Reuses the cell-division
questions of the US Biology unit in British English.
Wrong answers come from real mistakes: "mitosis makes sex cells", "daughter cells have half the chromosomes",
"adult stem cells can become any cell", "cells differentiate before they divide".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62002)
CD = "bio_cell_division_and_differentiation"
us_cells, us_chrom, us_count, us_diff, us_order, us_phase = [us(CD, "g_" + n) for n in ("cells", "chrom", "count", "diff", "order", "phase")]

STEM = [("embryonic stem cells", "can become almost any type of cell", "There are ethical objections because embryos are destroyed."),
        ("adult stem cells from bone marrow", "can become only some types of cell, such as blood cells", "They are taken from the patient or a donor."),
        ("meristem tissue in plants", "can become any type of plant cell throughout the plant's life", "It is found at the tips of roots and shoots.")]


def g_stem():
    s, can, note = R.choice(STEM)
    k = R.random() < 0.5
    if not once(("st", s, k)):
        return None
    if k:
        return item("Which statement about %s is true?" % s, "They " + can + ".", ["They " + x[1] + "." for x in STEM if x[0] != s] + ["They cannot divide at all."], note)
    return item("Which type of stem cell %s?" % can, s, [x[0] for x in STEM if x[0] != s] + ["red blood cells"], note)


USE = [("treating diabetes by making insulin-producing cells", "a possible future use of stem cells"), ("cloning rare plants quickly and cheaply from meristems", "a use of plant stem cells"),
       ("treating paralysis by replacing damaged nerve cells", "a possible future use of stem cells"), ("growing crops with special features, such as disease resistance", "a use of plant stem cells"),
       ("a bone marrow transplant for leukaemia", "a current use of adult stem cells")]


def g_use():
    u, a = R.choice(USE)
    if not once(("us", u)):
        return None
    return item("What is %s?" % u, a, [x for x in ["a possible future use of stem cells", "a use of plant stem cells", "a current use of adult stem cells", "an example of meiosis"] if x != a][:3], "Stem cells can divide and differentiate.")


B1 = bank([
    ("Where are chromosomes found in a cell?", "in the nucleus", ["in the cytoplasm only", "in the cell membrane", "in the ribosomes"], "Made of DNA."),
    ("How many chromosomes are in a human body cell?", "46 (23 pairs)", ["23", "92", "44"], "Half from each parent."),
    ("What is mitosis used for?", "growth, repair and asexual reproduction", ["making sex cells", "digesting food", "making proteins only"], "Two identical daughter cells."),
    ("What happens before a cell divides by mitosis?", "It grows, copies its DNA and makes more sub-cellular structures such as ribosomes and mitochondria.", ["It loses its nucleus.", "It halves its chromosomes.", "It stops respiring."], "The cell cycle."),
    ("How do the daughter cells made by mitosis compare with the parent cell?", "They are genetically identical, with the same number of chromosomes.", ["They have half the chromosomes.", "They are all different.", "They have double the chromosomes."], "Clones."),
    ("What is a stem cell?", "an undifferentiated cell that can divide and become many types of cell", ["a cell in a plant stem only", "a fully specialised cell", "a dead cell"], "Differentiation."),
])
B5 = bank([
    ("What is therapeutic cloning?", "making an embryo with the same genes as the patient so its stem cells are not rejected", ["cloning a whole person", "copying plants by cuttings", "taking bone marrow from a donor"], "No rejection."),
    ("What is one risk of using stem cells from a lab?", "They could be infected with a virus and pass it to the patient.", ["They always cure the disease.", "They have no risks.", "They turn into bones only."], "Risks must be weighed."),
    ("Why is cancer linked to cell division?", "It is caused by uncontrolled cell division.", ["Cells stop dividing.", "Cells divide by meiosis.", "Cells lose their DNA."], "Tumours."),
    ("Why do most animal cells differentiate early?", "Most animal cells lose the ability to differentiate once they specialise; plants keep it all their life.", ["Animals cannot grow.", "Plant cells never differentiate.", "Differentiation stops mitosis."], "Animals vs plants."),
])

if __name__ == "__main__":
  build(U, 10, "cell-division", 2, "Biology", "Cell biology",
      "The role of the cell cycle and mitosis in growth and repair; chromosomes in the nucleus; the function of stem cells in embryos, in adult animals and in the meristems of plants; the use of stem cells in medicine and agriculture, including therapeutic cloning, and the potential benefits and risks.",
      "Cell Division", "Cell Division",
      "Free Year 10 GCSE Combined Science worksheets on cell division: chromosomes, the cell cycle and mitosis, differentiation, stem cells, meristems and therapeutic cloning. 100 questions with answers.",
      "Mitosis makes two identical cells.",
      "Stem cells can divide and differentiate into many types of cell.",
      "<p><b>Cells divide by mitosis for growth and repair.</b></p><ul><li>Before dividing, the cell grows and copies its chromosomes. Mitosis then makes two genetically identical daughter cells.</li>"
      "<li>Stem cells are undifferentiated: embryonic stem cells can become almost any cell; adult stem cells only some; plant meristems any plant cell.</li>"
      "<li>Stem cells may treat diseases such as diabetes, but there are risks and ethical issues.</li></ul>",
      [("46 chromosomes divide by mitosis. Each daughter cell?", ["Identical copies"], "46"), ("Which stem cells can become almost any cell?", ["From embryos"], "embryonic stem cells")],
      ["Thinking mitosis makes sex cells.", "Thinking daughter cells have half the chromosomes.", "Thinking adult stem cells can become any cell."],
      [("What is mitosis?", "Cell division that makes two genetically identical daughter cells, each with the same number of chromosomes as the parent cell. It is used for growth and repair."),
       ("What are stem cells?", "Undifferentiated cells that can divide and become specialised cells. Embryonic stem cells can become almost any cell; adult and plant meristem stem cells have narrower or plant-only uses."),
       ("What is therapeutic cloning?", "Making an embryo with the patient's own genes. Its stem cells could treat the patient without being rejected by the immune system.")],
      [("Chromosomes", B1 + [(us_chrom, 8), (us_count, 6)]),
       ("Mitosis", [(us_phase, 7), (us_order, 8), (us_count, 5)]),
       ("Differentiation", [(us_diff, 7), (us_cells, 9), (g_stem, 4)]),
       ("Stem cells", [(g_use, 4), (us_cells, 8), (us_chrom, 8)]),
       ("Uses and risks", B5 + [(us_count, 8), (us_chrom, 6), (us_phase, 2)])])
