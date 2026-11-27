# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Models): Model of Cells - the Basic Unit of Life
  python tools/gen_sg_science_s1_cells.py
Parts of a typical cell and their functions (cell wall, cell membrane, cytoplasm, nucleus with DNA, vacuole, chloroplast),
plant and animal cells as models, cells -> tissues -> organs -> systems, division of labour, specialised cells,
the light microscope and inferring plant or animal from cell structures.
UK KS3 cell makers are reused (mitochondria and ribosomes are left out: not in the Singapore syllabus).
Wrong answers come from real mistakes: "animal cells have a cell wall", "the cell wall controls what enters",
"all plant cells have chloroplasts", "magnifications are added".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64106)
R = U.R
P = People(R)
DROP = [r"mitochondri", r"ribosome", r"respiration releases"]
CE = luse(U, "gen_uk_science_y7_cells", drop=DROP)
SP = luse(U, "gen_uk_science_y7_specialised_cells_and_organisation", drop=DROP + [r"diffus"])

CELLS = [  # description, plant or animal, why
    ("has a cell wall, a large central vacuole and chloroplasts", "a plant cell", "Only plant cells have a cell wall and chloroplasts."),
    ("has a nucleus, cytoplasm and a cell membrane but no cell wall", "an animal cell", "Animal cells have no cell wall."),
    ("has a cell wall and a large vacuole but no chloroplasts, and comes from an onion bulb", "a plant cell", "Not every plant cell has chloroplasts; a cell wall shows it is a plant cell."),
    ("is round, has no cell wall and carries oxygen in the blood", "an animal cell", "A red blood cell is an animal cell."),
    ("has a cell wall and many chloroplasts, and comes from a leaf", "a plant cell", "Leaf cells make food in their chloroplasts."),
    ("has a long tail, a nucleus and no cell wall", "an animal cell", "A sperm cell is an animal cell."),
    ("is from the inside of a person's cheek and has an irregular shape", "an animal cell", "Cheek cells have no cell wall, so their shape is not fixed."),
    ("has a cell wall and a long, thin extension that takes in water from the soil", "a plant cell", "A root hair cell is a plant cell with no chloroplasts."),
]


def g_infer():
    d, a, e = R.choice(CELLS)
    if not once(("in", d)):
        return None
    return item("A cell %s. What kind of cell is it most likely to be?" % d, a,
                [x for x in ["a plant cell", "an animal cell", "a bacterium with no genetic material", "not a cell at all"] if x != a][:3], e)


B1 = bank([
    ("Which part of the cell contains DNA, the genetic material?", "the nucleus", ["the cytoplasm", "the cell wall", "the vacuole"], "DNA in the nucleus carries the instructions for the cell."),
    ("Why do we call the drawings of plant and animal cells in textbooks 'models'?", "They show the main parts of a typical cell, but real cells vary in shape and size.", ["They are photographs of one real cell.", "They show every part of every cell exactly.", "They are toys."], "A model is a simplified way of showing an idea."),
    ("Which part keeps the shape of a plant cell fixed?", "the cell wall", ["the cell membrane", "the nucleus", "the cytoplasm"], "The cell wall is rigid; it gives shape and support."),
    ("Which part is partially permeable and controls the movement of substances in and out of the cell?", "the cell membrane", ["the cell wall", "the vacuole", "the chloroplast"], "The cell wall is fully permeable."),
    ("What is meant by division of labour in a multicellular organism?", "Different cells are specialised to carry out different jobs.", ["Every cell does every job.", "Cells divide into two all the time.", "Only one cell does all the work."], "This makes the organism work efficiently."),
    ("Which is the correct order, from smallest to largest?", "cell, tissue, organ, system, organism", ["tissue, cell, organ, system, organism", "cell, organ, tissue, system, organism", "organism, system, organ, tissue, cell"], "Cells make tissues; tissues make organs."),
    ("Who first used the word 'cell' after looking at cork under an early microscope?", "Robert Hooke", ["Isaac Newton", "Charles Darwin", "Marie Curie"], "Better microscopes later let scientists see the nucleus and other parts."),
])
B5 = bank([
    ("Jun Jie used ×10 eyepiece and ×40 objective lenses. A cell is 0.05 mm wide. How wide does its image look?", "20 mm", ["0.05 mm", "2 mm", "50 mm"], "×10 × ×40 = ×400; 0.05 mm × 400 = 20 mm."),
    ("Why must a thin, single layer of onion skin be used on a slide?", "So that light can pass through it and the cells can be seen clearly.", ["So that the cells die.", "So that it is heavier.", "So that it does not need a stain."], "Thick samples block light."),
    ("When focusing under high power, which knob should be used?", "the fine focusing knob only", ["the coarse focusing knob", "both knobs as fast as possible", "no knob"], "The coarse knob may crush the slide on high power."),
    ("A cell has a cell membrane, cytoplasm and a nucleus. Which conclusion is correct?", "It could be either a plant or an animal cell; more evidence is needed.", ["It must be a plant cell.", "It must be an animal cell.", "It is not a living cell."], "Both kinds of cell have these parts."),
    ("Cells in the small intestine are folded and have tiny projections. What is the most likely reason?", "to increase the surface area for absorbing digested food", ["to store water", "to make food by photosynthesis", "to carry messages"], "The shape of a specialised cell suits its job."),
    ("Why is the nucleus important when a cell divides?", "It passes the genetic information (DNA) to the new cells.", ["It makes the cell wall.", "It stores water.", "It carries out photosynthesis."], "Each new cell needs its own copy of DNA."),
])


def body():
    think = ("<p><b>The cell is the basic unit of life. Each part of a cell has a job.</b></p>"
             "<ul><li><b>Nucleus</b>: controls the cell; contains DNA. <b>Cell membrane</b>: controls what enters and leaves. <b>Cytoplasm</b>: where most reactions happen.</li>"
             "<li>Only plant cells have a <b>cell wall</b> (shape and support), <b>chloroplasts</b> (photosynthesis) and a large central <b>vacuole</b> (cell sap).</li>"
             "<li>Cells → tissues → organs → systems → organism. Specialised cells share the work: <b>division of labour</b>.</li>"
             "<li>Total magnification = eyepiece × objective.</li></ul>")
    ex = [("A cell has a cell wall but no chloroplasts. Plant or animal?", ["Only plant cells have a cell wall"], "a plant cell, for example a root hair cell"),
          ("Eyepiece ×10, objective ×10. Total magnification?", ["Multiply, do not add"], "×100")]
    mist = ["Saying animal cells have a cell wall. Only plant cells do.",
            "Mixing up the cell wall and the cell membrane. The membrane controls what goes in and out.",
            "Thinking every plant cell has chloroplasts. Root cells do not.",
            "Adding the eyepiece and objective magnifications instead of multiplying."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a cell", B1[:4] + CE.B1 + [(CE.g_org, 6), (CE.g_where, 2)]),
        ("Plant and animal cells", [(CE.g_pic, 10), (g_infer, 6), (CE.g_where, 4)]),
        ("Cells, tissues and organs", B1[4:] + SP.B1 + [(g_infer, 2)] + [(SP.g_level, 6), (SP.g_spec, 6)]),
        ("The microscope", [(CE.g_mic, 8), (CE.g_mag, 8)] + CE.B5[:4]),
        ("Exam-style questions", B5 + SP.B5[:2] + [(CE.g_pic, 4), (CE.g_mag, 4), (g_infer, 2), (SP.g_spec, 2)]),
    ])
    make_lss(1, "cells", 6, "Models", "Model of Cells – the Basic Unit of Life",
             "Describe the functions of the parts of a typical cell, including the nucleus which contains DNA; recognise plant and animal cells as models and cells as the building blocks "
             "of tissues, organs and systems; explain division of labour at the cellular level; identify the cell wall, cell membrane, cytoplasm, nucleus, vacuole and chloroplast "
             "under a light microscope and infer whether a cell is from a plant or an animal (summary of the MOE Lower Secondary Science Syllabus).",
             "Model of Cells: the Basic Unit of Life", seo(1, "Cells"), "Cells",
             "Free Secondary 1 science worksheets for Singapore students on cells: parts of plant and animal cells, specialised cells, tissues and organs, and the light microscope, with answers.",
             "The cell is the basic unit of life.", "Plant cells also have a cell wall, chloroplasts and a large vacuole.",
             body(),
             [("What is the difference between a plant cell and an animal cell?", "Plant cells have a cell wall, a large central vacuole and often chloroplasts. Animal cells have none of these."),
              ("What does the nucleus do?", "It controls the activities of the cell and contains DNA, the genetic material."),
              ("How do you work out total magnification?", "Multiply the eyepiece magnification by the objective magnification.")],
             sets)


if __name__ == "__main__":
    main()
