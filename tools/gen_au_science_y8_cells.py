# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U01: cells as the basic units of living things - cell theory, plant and animal
cell structures and their functions, specialised cells, and using light microscopes.
  python tools/gen_au_science_y8_cells.py
Reuses the UK Year 7 cell makers, the US Grade 6 cell makers and the SG Secondary 1 cell makers with Australian names.
Wrong answers come from real mistakes: thinking all cells have a cell wall and chloroplasts, mixing up the cell membrane and the
cell wall, and calculating magnification by adding instead of multiplying the lens values.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

C7 = "gen_uk_science_y7_cells"
SC = "gen_uk_science_y7_specialised_cells_and_organisation"
G6 = "gen_us_science_g6_cells_and_cell_theory"
PC = "gen_us_science_g6_parts_of_a_cell"
S1 = "gen_sg_science_s1_cells"
c_pic = limit(src(C7, "g_pic"), 6)
c_mic = src(C7, "g_mic")
c_mag = limit(src(C7, "g_mag"), 4)
c_where = src(C7, "g_where")
c_b1 = src.B(C7, "B1")
c_b5 = src.B(C7, "B5")
s_spec = src(SC, "g_spec")
s_diff = src(SC, "g_diff")
g_living = limit(src(G6, "g_living"), 5)
g_size = limit(src(G6, "g_size"), 4)
g_uni = limit(src(G6, "g_uni"), 5)
g_b1 = src.B(G6, "B1")
p_job = src(PC, "g_job", drop=["part a stiff"])
p_label = limit(src(PC, "g_label", drop=["part a stiff"]), 5)
p_pa = src(PC, "g_plantanimal", drop=["part a stiff"])
p_which = src(PC, "g_which", drop=["part a stiff"])
p_b5 = src.B(PC, "B5")
s1_inf = src(S1, "g_infer")
s1_b1 = src.B(S1, "B1")
s1_b5 = src.B(S1, "B5")

POOL1 = pool(R, [
    ("What does cell theory state?", "All living things are made of cells, cells are the basic unit of life, and new cells come from existing cells.", ["All cells are the same.", "Only animals have cells.", "Cells are made of living things."], "Cell theory came from many scientists' observations."),
    ("Which structures are found in plant cells but not animal cells?", "cell wall, chloroplasts and a large permanent vacuole", ["nucleus and cell membrane", "mitochondria and cytoplasm", "only the nucleus"], "Both have a nucleus, cytoplasm, membrane and mitochondria."),
    ("What is the job of the cell membrane?", "controls what enters and leaves the cell", ["makes food from sunlight", "gives the plant cell a rigid shape", "stores genetic information"], "The membrane is selectively permeable."),
    ("What is the job of the nucleus?", "contains genetic information (DNA) and controls the cell", ["makes energy from glucose", "makes food", "lets light in"], "It is the control centre."),
    ("Where does respiration take place in a cell?", "in the mitochondria", ["in the chloroplasts", "in the cell wall", "in the vacuole"], "Mitochondria release energy from glucose."),
    ("Where does photosynthesis take place?", "in the chloroplasts", ["in the mitochondria", "in the nucleus", "in the cell membrane"], "Chloroplasts contain green chlorophyll."),
    ("A microscope has a 10× eyepiece and a 40× objective lens. What is the total magnification?", "400×", ["50×", "40×", "4000×"], "Multiply the two values: 10 × 40 = 400."),
    ("Why do we stain cells before looking at them under a microscope?", "to make parts such as the nucleus easier to see", ["to kill harmful bacteria", "to make the cells bigger", "to make them move"], "Iodine and methylene blue are common stains."),
    ("Why is a cover slip placed on a slide?", "to hold the specimen flat and stop it drying out", ["to make it magnetic", "to make it bigger", "to stain it"], "Lower it carefully to avoid air bubbles."),
    ("Which specialised cell carries oxygen around the body?", "red blood cell", ["nerve cell", "root hair cell", "sperm cell"], "It has no nucleus and is packed with haemoglobin."),
    ("Which part of a microscope should you use first to focus on a specimen?", "the coarse focus knob with the lowest power objective", ["the fine focus with the highest power", "the light switch only", "the stage clips"], "Start with low power, then increase."),
    ("Who first described cells in cork in 1665?", "Robert Hooke", ["Isaac Newton", "Charles Darwin", "Marie Curie"], "He named them 'cells' because they looked like small rooms."),
])
POOL5 = pool(R, [
    ("Mia sees cells with a green colour, a thick outer edge and a large central space. What are they most likely to be?", "plant leaf cells", ["human cheek cells", "red blood cells", "bacteria"], "Chloroplasts, a cell wall and a vacuole are plant features."),
    ("Jack measures a cell as 4 mm wide in a photo magnified 400×. What is its real width?", "0.01 mm (10 micrometres)", ["1600 mm", "4 mm", "0.4 mm"], "Real size = image size ÷ magnification = 4 ÷ 400."),
    ("Ruby's slide is blurry at 400×. What should she adjust?", "the fine focus knob", ["the coarse focus knob at high power", "the eyepiece colour", "the stage clips"], "At high power, only use fine focus."),
    ("Kai sees bubbles under the cover slip. How could he avoid this next time?", "lower the cover slip slowly at an angle", ["drop it flat quickly", "use no water", "press it hard"], "This pushes air out."),
    ("Why should onion cells be stained with iodine?", "Iodine stains the nucleus and cell wall so they are easier to see.", ["It makes the onion taste better.", "It kills the cells' DNA.", "It makes the cells grow."], "Staining increases contrast."),
    ("Ella sees no chloroplasts in onion skin cells, even though onions are plants. Why?", "Onion bulbs grow underground and do not photosynthesise.", ["Onions are animals.", "Her microscope is broken.", "All plant cells lack chloroplasts."], "Not every plant cell has chloroplasts."),
])


def main():
    sets = U.sets([
        ("Cell theory", [(POOL1, 4), (g_living, 4), (g_uni, 4), (g_size, 3), (g_b1, 3), (s1_b1, 2)]),
        ("Cell structures", [(p_job, 6), (p_which, 5), (c_pic, 5), (POOL1, 4)]),
        ("Plant and animal cells", [(p_pa, 7), (c_where, 5), (p_label, 4), (s1_inf, 4)]),
        ("Specialised cells", [(s_spec, 8), (s_diff, 6), (POOL1, 2), (c_b1, 4)]),
        ("Microscopes", [(c_mic, 6), (c_mag, 3), (POOL5, 6), (c_b5, 2), (p_b5, 2), (s1_b5, 1)]),
    ])
    make_au(YEAR, "cells", SORT, "AC9S8U01", "Biological sciences",
            "Investigate the structure and function of cells as the basic units of living things, comparing plant and animal cells and "
            "describing specialised cells; use light microscopes (summary of the Australian Curriculum v9.0 Science content description).",
            "Cells", "Cells",
            "Free Year 8 science worksheets on cells: cell theory, plant and animal cell structures, specialised cells and using a light "
            "microscope to calculate magnification. 100 questions with answers.",
            "Cells are the building blocks of life.", "Plant cells have a cell wall, chloroplasts and a large vacuole; animal cells do not.",
            "<p><b>All living things are made of cells, and every cell comes from another cell.</b></p><ul>"
            "<li>Animal and plant cells: nucleus, cytoplasm, cell membrane, mitochondria. Plant cells also: cell wall, chloroplasts, large vacuole.</li>"
            "<li>Specialised cells have shapes that suit their jobs: red blood cells, nerve cells, root hair cells, sperm cells.</li>"
            "<li>Total magnification = eyepiece × objective. Real size = image size ÷ magnification.</li></ul>",
            [("10× eyepiece and 40× objective?", ["multiply"], "400×"),
             ("Green, cell wall, big vacuole. Plant or animal?", ["chloroplasts and a cell wall"], "plant")],
            ["Thinking all cells have a cell wall and chloroplasts.", "Mixing up the cell membrane and the cell wall.",
             "Adding the lens values instead of multiplying them."],
            [("What are the main differences between plant and animal cells?", "Plant cells have a cell wall, chloroplasts and a large permanent vacuole. Animal cells do not, but both have a nucleus, cytoplasm, a membrane and mitochondria."),
             ("How do I calculate magnification?", "Multiply the eyepiece by the objective lens: 10× × 40× = 400×. To find real size, divide the image size by the magnification."),
             ("What is a specialised cell?", "A cell with a special shape or structure for its job, such as a nerve cell that is long and thin to carry messages.")],
            sets)


if __name__ == "__main__":
    main()
