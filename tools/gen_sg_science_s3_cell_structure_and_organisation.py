# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 1: Cell Structure and Organisation
  python tools/gen_sg_science_s3_cell_structure_and_organisation.py
Plant and animal cell structures as seen under light and electron microscopes (cell wall, cell membrane, cytoplasm, nucleus, vacuoles,
chloroplasts, mitochondria, ribosomes, rough and smooth endoplasmic reticulum, Golgi body), specialised cells and how their
structure fits their function, levels of organisation, and magnification.
UK KS3/KS4 cell makers are reused (Singapore names); organelle, specialised-cell and organisation rows are written here.
Wrong answers come from real mistakes: "animal cells have a cell wall", "ribosomes make lipids", "the cell membrane is fully
permeable", "red blood cells have a large nucleus", "magnification = real size ÷ image size".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 3, "Biology", 19
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_mag = src("gen_uk_science_y10_cell_structure_and_transport", "g_mag")
uk_pic = src("gen_uk_science_y7_cells", "g_pic")
uk_org = src("gen_uk_science_y7_cells", "g_org")
uk_where = src("gen_uk_science_y7_cells", "g_where")
uk_mic = src("gen_uk_science_y7_cells", "g_mic")

ORG = [("ribosomes", "makes proteins"), ("rough endoplasmic reticulum", "carries ribosomes and transports the proteins they make"),
       ("smooth endoplasmic reticulum", "makes lipids and breaks down harmful substances"),
       ("the Golgi body", "modifies and packages proteins into vesicles for secretion"),
       ("the mitochondria", "releases energy by aerobic respiration"), ("the chloroplasts", "absorbs light energy for photosynthesis"),
       ("the nucleus", "contains DNA and controls the activities of the cell"), ("the partially permeable cell membrane", "controls what enters and leaves the cell"),
       ("the cellulose cell wall", "is fully permeable and supports the plant cell"), ("the large central vacuole", "stores cell sap and keeps the plant cell firm")]
g_orgf = rows(R, ORG, "What is the function of %s?", "Which part of a cell does this: it %s?")

SPEC = [("red blood cell", "no nucleus and a biconcave shape", "more room for haemoglobin and a larger surface area to take up oxygen"),
        ("root hair cell", "a long, narrow extension", "a larger surface area to absorb water and mineral salts"),
        ("xylem vessel", "no cytoplasm or cross-walls and lignified walls", "an empty, continuous tube that carries water and gives support"),
        ("muscle cell", "many mitochondria", "more energy released by respiration for contraction"),
        ("palisade mesophyll cell", "many chloroplasts", "more light absorbed for photosynthesis"),
        ("sperm cell", "a tail (flagellum) and many mitochondria", "energy to swim to the egg"),
        ("pancreatic cell that secretes enzymes", "a lot of rough endoplasmic reticulum and a large Golgi body", "many proteins made and packaged for secretion"),
        ("guard cell", "a thicker inner wall", "a change of shape that opens and closes the stoma")]


def g_spec():
    c, feat, why = R.choice(SPEC)
    k = R.choice(["feat", "why", "which"])
    others = [x for x in SPEC if x[0] != c]
    if k == "feat":
        return tq("Which feature is typical of a %s?" % c, feat, [x[1] for x in R.sample(others, 3)], "A %s has %s: %s." % (c, feat, why))
    if k == "why":
        return tq("A %s has %s. How does this help it?" % (c, feat), why, [x[2] for x in R.sample(others, 3)], "Structure fits function.")
    return tq("Which cell has %s, giving %s?" % (feat, why), "a " + c, ["a " + x[0] for x in R.sample(others, 3)], "Each specialised cell is adapted to its job.")


LEVEL = [("a red blood cell", "cell"), ("a root hair cell", "cell"), ("muscle tissue", "tissue"), ("xylem tissue", "tissue"), ("epithelium", "tissue"),
         ("the heart", "organ"), ("a leaf", "organ"), ("the stomach", "organ"), ("the digestive system", "organ system"), ("the circulatory system", "organ system"),
         ("the shoot system of a plant", "organ system"), ("the kidney", "organ"), ("palisade mesophyll", "tissue")]


def g_level():
    x, lv = R.choice(LEVEL)
    return tq("At which level of organisation is %s?" % x, lv, [y for y in ("cell", "tissue", "organ", "organ system", "organism") if y != lv][:3] if lv != "cell" else ["tissue", "organ", "organ system"],
              "cell → tissue (similar cells) → organ (several tissues) → organ system → organism.")


POOL1 = pool(R, [
    ("Which structures are found in plant cells but not in animal cells?", "a cellulose cell wall, chloroplasts and a large central vacuole", ["a nucleus and cytoplasm", "mitochondria and ribosomes", "a cell membrane and Golgi body"], "Animal cells may have small, temporary vacuoles."),
    ("Which structures can be seen only with an electron microscope?", "ribosomes and endoplasmic reticulum", ["the nucleus and cell wall", "chloroplasts and the vacuole", "the cytoplasm"], "The electron microscope has a much higher resolution."),
    ("What is a tissue?", "a group of similar cells working together to perform a function", ["a group of organs", "a single specialised cell", "a group of organ systems"], "For example muscle tissue."),
    ("What is an organ?", "a structure made of several tissues working together", ["a group of similar cells", "a single cell", "a part of a cell"], "For example the stomach."),
    ("Why does a plant cell not burst when it takes in a lot of water?", "The strong cellulose cell wall resists the pressure.", ["The vacuole pumps the water out.", "Chloroplasts absorb the water.", "The membrane is fully permeable."], "The cell becomes turgid."),
    ("What does “partially permeable” mean for the cell membrane?", "It lets some substances through but not others.", ["It lets every substance through.", "It lets nothing through.", "It is made of cellulose."], "The cell wall, by contrast, is fully permeable."),
    ("Why do cells that secrete enzymes have a lot of rough endoplasmic reticulum?", "Enzymes are proteins made by the ribosomes on it.", ["Enzymes are lipids.", "It stores glucose.", "It releases energy."], "The Golgi body then packages them."),
    ("What is the function of vesicles?", "to carry substances such as proteins to the cell membrane for secretion", ["to make proteins", "to absorb light", "to control the cell"], "Vesicles bud off the Golgi body."),
    ("Which formula gives the magnification of a drawing?", "magnification = image size ÷ actual size", ["magnification = actual size ÷ image size", "magnification = image size × actual size", "magnification = image size − actual size"], "Use the same units for both."),
    ("How many micrometres (µm) are there in 1 mm?", "1000", ["10", "100", "1 000 000"], "1 mm = 1000 µm."),
])
POOL5 = pool(R, [
    ("A cell has a cell wall, chloroplasts and a large vacuole. Which cell is it?", "a palisade mesophyll cell", ["a red blood cell", "a muscle cell", "a sperm cell"], "These are plant cell features."),
    ("A cell has no cell wall and many mitochondria. Which cell could it be?", "a muscle cell", ["a root hair cell", "a palisade cell", "a xylem vessel"], "Muscle cells need a lot of energy."),
    ("Why do root hair cells have no chloroplasts?", "They are underground and get no light.", ["They are too small.", "They do not need energy.", "Chloroplasts would block water."], "They absorb water and mineral salts."),
    ("A drawing of a cell is 60 mm long at ×300 magnification. What is the actual length?", "0.2 mm (200 µm)", ["18 000 mm", "5 mm", "0.02 mm"], "60 ÷ 300 = 0.2 mm."),
    ("Why are electron micrographs able to show mitochondria in detail?", "The electron microscope has a much higher resolution than a light microscope.", ["It uses coloured light.", "It makes cells bigger.", "It uses living cells."], "Resolution is the ability to see two close points as separate."),
    ("Mature xylem vessels contain no cytoplasm. Why is this useful?", "Water can flow through the empty tubes without obstruction.", ["It lets them photosynthesise.", "It makes them more flexible.", "It lets them divide quickly."], "They are dead and lignified."),
    ("Which sequence goes from the smallest to the largest level of organisation?", "cell → tissue → organ → organ system", ["organ → tissue → cell → organ system", "tissue → cell → organ → organ system", "cell → organ → tissue → organ system"], "Similar cells form tissues; tissues form organs."),
    ("Why are red blood cells unable to divide?", "They have no nucleus.", ["They have a cell wall.", "They have no cytoplasm.", "They are too large."], "New red blood cells are made in the bone marrow."),
])


def main():
    sets = U.sets([
        ("Plant and animal cells", [(uk_pic, 6), (uk_where, 5), (uk_org, 5), (POOL1, 4)]),
        ("Organelles and their functions", [(g_orgf, 12), (POOL1, 4), (uk_mic, 4)]),
        ("Specialised cells", [(g_spec, 14), (uk_org, 2), (POOL1, 2), (POOL5, 2)]),
        ("Levels of organisation and magnification", [(g_level, 8), (uk_mag, 10), (g_orgf, 2)]),
        ("Exam-style questions", [(POOL5, 6), (g_spec, 6), (uk_mag, 4), (g_orgf, 4)]),
    ])
    make_ol(LV, SUBJ, "cell-structure-and-organisation", SORT, "Cell Structure and Organisation",
            "Identify the cell structures of typical plant and animal cells as seen under a light microscope and an electron microscope, including the cell wall, cell "
            "membrane, cytoplasm, nucleus, vacuoles, chloroplasts, mitochondria, ribosomes, rough and smooth endoplasmic reticulum and Golgi body, and state their functions; "
            "relate the structure of specialised cells to their functions; describe the levels of organisation (cells, tissues, organs and systems); calculate "
            "magnification and actual size (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Cell Structure and Organisation", "Cell structure",
            "Free Secondary 3 O-Level Biology worksheets on cell structure and organisation: plant and animal cells, organelles, specialised cells, levels of "
            "organisation and magnification. 100 questions with answers.",
            "Structure fits function.", "Plant cells add a cell wall, chloroplasts and a large vacuole.",
            "<p><b>Every part of a cell has a job.</b></p><ul>"
            "<li>Nucleus: DNA and control. Mitochondria: aerobic respiration. Ribosomes: proteins. Rough ER: carries ribosomes. Smooth ER: lipids. Golgi body: packages proteins.</li>"
            "<li>Plant cells also have a cellulose cell wall, chloroplasts and a large central vacuole with cell sap.</li>"
            "<li>Specialised cells are adapted: root hair cells (large surface area), red blood cells (no nucleus, biconcave), muscle cells (many mitochondria).</li>"
            "<li>Magnification = image size ÷ actual size, with both in the same unit.</li></ul>",
            [("Image 12 mm, actual 40 µm. Magnification?", ["12 mm = 12 000 µm", "12 000 ÷ 40"], "×300"),
             ("Why many mitochondria in sperm?", ["mitochondria release energy", "energy to swim"], "energy for movement")],
            ["Saying animal cells have a cell wall.", "Mixing up ribosomes (proteins) and smooth ER (lipids).", "Dividing actual size by image size.",
             "Forgetting to change mm to µm before dividing."],
            [("What is the difference between rough and smooth endoplasmic reticulum?", "Rough ER has ribosomes on it and transports the proteins they make. Smooth ER has no ribosomes and makes lipids and breaks down harmful substances."),
             ("How do you calculate magnification?", "Magnification = image size ÷ actual size. Change both lengths to the same unit first (1 mm = 1000 µm)."),
             ("Why do root hair cells have a long extension?", "It gives a large surface area for absorbing water by osmosis and mineral salts by active transport.")],
            sets)


if __name__ == "__main__":
    main()
