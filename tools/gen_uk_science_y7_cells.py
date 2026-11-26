# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Biology): Cells
  python tools/gen_uk_science_y7_cells.py
Cells as the fundamental unit of living organisms: the functions of the cell wall, cell membrane, cytoplasm, nucleus,
vacuole, mitochondria and chloroplasts; similarities and differences between plant and animal cells (labelled
diagrams); and using a light microscope (parts, method and total magnification).
Wrong answers come from real mistakes: "animal cells have a cell wall", "the nucleus makes food", "mitochondria are
only in animal cells", "magnifications are added, not multiplied".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, fig, People, once
from uk_sci_pics import cell
from sci_phys import uniq

U = Unit(61701)
R = U.R
P = People(R)

ORG = [("the nucleus", "controls the cell and contains the genetic material (DNA)"), ("the cell membrane", "controls what enters and leaves the cell"),
       ("the cytoplasm", "is a jelly where most chemical reactions happen"), ("the mitochondria", "are where respiration releases energy"),
       ("the cell wall", "strengthens and supports the cell"), ("the chloroplasts", "are where photosynthesis makes food"),
       ("the vacuole", "is filled with cell sap and keeps the cell firm")]


def g_org():
    o, j = R.choice(ORG)
    k = R.random() < 0.5
    if not once(("or", o, k)):
        return None
    if k:
        return item("What is the job of %s?" % o, "It " + j + "." if not o.endswith(("mitochondria", "chloroplasts")) else "They " + j[4:] + ".",
                    [("It " + x[1] + "." if not x[0].endswith(("mitochondria", "chloroplasts")) else "They " + x[1][4:] + ".") for x in R.sample([x for x in ORG if x[0] != o], 3)],
                    "Each part of a cell has a job.")
    d = j if not o.endswith(("mitochondria", "chloroplasts")) else j
    return item("Which part of a cell %s?" % d.replace("are where", "is where").replace("are ", "is "), o, R.sample([x[0] for x in ORG if x[0] != o], 3), "Each part of a cell has a job.")


WHERE = {"the nucleus": "both", "the cell membrane": "both", "the cytoplasm": "both", "the mitochondria": "both",
         "the cell wall": "plant cells only", "the chloroplasts": "plant cells only", "a large permanent vacuole": "plant cells only"}
WA = {"both": "both plant and animal cells", "plant cells only": "plant cells only"}


def g_where():
    o = R.choice(sorted(WHERE))
    if not once(("wh", o)):
        return None
    a = WA[WHERE[o]]
    return item("Where %s %s found: in animal cells, plant cells or both?" % ("are" if o.split()[-1] in ("chloroplasts", "mitochondria", "ribosomes", "vacuoles") else "is", o), a, [x for x in ["both plant and animal cells", "plant cells only", "animal cells only", "neither"] if x != a][:3],
                "Plant cells have everything animal cells have, plus a cell wall, chloroplasts and a large vacuole.")


PLANT = ["cell wall", "cell membrane", "nucleus", "vacuole", "chloroplast", "cytoplasm"]
ANIMAL = ["cell membrane", "nucleus", "cytoplasm", "mitochondria"]


def g_pic():
    kind = R.choice(["plant", "animal"])
    parts = R.sample(PLANT, 5) if kind == "plant" else ANIMAL[:]
    lab = dict(zip(parts, R.sample("ABCDE"[:len(parts)], len(parts))))
    p = R.choice(parts)
    k = R.random() < 0.5
    if not once(("pc", kind, p, lab[p], k)):
        return None
    pic = fig(cell(kind, lab))
    nm = {"chloroplast": "a chloroplast", "mitochondria": "a mitochondrion"}.get(p, "the " + p)
    if k:
        return item(pic + "This is %s %s cell. Which letter labels %s?" % ("a" if kind == "plant" else "an", kind, nm), lab[p], R.sample([lab[x] for x in parts if x != p], 3),
                    "Follow each line to the part it touches.")
    return item(pic + "This is %s %s cell. Which part is labelled %s?" % ("a" if kind == "plant" else "an", kind, lab[p]), nm,
                R.sample([{"chloroplast": "a chloroplast", "mitochondria": "a mitochondrion"}.get(x, "the " + x) for x in parts if x != p], 3), "Follow each line to the part it touches.")


def X(n):
    return "×{:,}".format(n)


def g_mag():
    e = R.choice([5, 10, 15])
    o = R.choice([4, 10, 40, 100])
    k = R.choice(["total", "eye", "obj", "size"])
    if not once(("mg", e, o, k)):
        return None
    t = e * o
    if k == "total":
        g = X(t)
        return item("A microscope has a ×%d eyepiece lens and a ×%d objective lens. What is the total magnification?" % (e, o), g, uniq(g, [X(e + o), X(e), X(o), X(t * 10)]),
                    "Total magnification = eyepiece × objective = %d × %d = %s." % (e, o, X(t)[1:]))
    if k == "eye":
        g = X(e)
        return item("A microscope gives a total magnification of %s with a ×%d objective lens. What is the eyepiece magnification?" % (X(t), o), g, uniq(g, [X(t - o), X(t), X(o), X(e * 2)]),
                    "Eyepiece = total ÷ objective = %s ÷ %d = %d." % (X(t)[1:], o, e))
    if k == "obj":
        g = X(o)
        return item("A microscope gives a total magnification of %s with a ×%d eyepiece. What is the objective magnification?" % (X(t), e), g, uniq(g, [X(t - e), X(t), X(e), X(o * 2)]),
                    "Objective = total ÷ eyepiece = %s ÷ %d = %d." % (X(t)[1:], e, o))
    a = R.choice([0.01, 0.02, 0.05, 0.1])
    img = round(a * t, 2)
    g = "%g mm" % img
    return item("A cell is %g mm wide. It is viewed at %s. How wide does it look in the image?" % (a, X(t)), g, uniq(g, ["%g mm" % round(a + t, 2), "%g mm" % a, "%g mm" % round(img * 10, 2), "%g mm" % round(img / 10, 3)]),
                "Image size = real size × magnification = %g × %s = %g mm." % (a, X(t)[1:], img))


MIC = [("the eyepiece lens", "the lens you look through"), ("the objective lens", "the lens just above the slide that you choose for low or high power"),
       ("the stage", "the flat platform where the slide is placed"), ("the coarse focusing knob", "the knob that moves the stage a lot to get the image roughly in focus"),
       ("the fine focusing knob", "the knob that makes small changes to sharpen the image"), ("the light source (lamp or mirror)", "the part that shines light up through the slide")]


def g_mic():
    p, d = R.choice(MIC)
    k = R.random() < 0.5
    if not once(("mi", p, k)):
        return None
    if k:
        return item("Which part of a light microscope is %s?" % d, p, R.sample([x[0] for x in MIC if x[0] != p], 3), "Learn the parts of the microscope.")
    return item("What is %s of a light microscope?" % p, d, R.sample([x[1] for x in MIC if x[1] != d], 3), "Learn the parts of the microscope.")


B1 = bank([
    ("What is a cell?", "the smallest unit of a living organism", ["a type of tissue", "a large organ", "a kind of molecule only"], "All living things are made of cells."),
    ("Which part do plant cells have that animal cells do not?", "a cell wall", ["a nucleus", "a cell membrane", "cytoplasm"], "Also chloroplasts and a large vacuole."),
    ("What is the cell wall of a plant made of?", "cellulose", ["protein", "fat", "glass"], "Strong fibres."),
    ("Why are plant leaves green?", "Their cells contain chloroplasts with green chlorophyll.", ["They are painted.", "Their nucleus is green.", "Their cell walls are green."], "Chlorophyll absorbs light."),
    ("Which part of the cell contains DNA?", "the nucleus", ["the cell wall", "the vacuole", "the cytoplasm only"], "Genetic information."),
    ("Why do root cells have no chloroplasts?", "Roots are underground with no light, so they cannot photosynthesise.", ["Roots are dead.", "Chloroplasts only grow in flowers.", "Roots are animal cells."], "No light, no chloroplasts."),
    ("Who first saw and named cells, using a microscope in 1665?", "Robert Hooke", ["Charles Darwin", "Isaac Newton", "Marie Curie"], "He looked at cork."),
    ("What is a unicellular organism?", "a living thing made of just one cell", ["a living thing with no cells", "a plant with one leaf", "an animal with one organ"], "Amoeba and bacteria."),
])
B5 = bank([
    ("When focusing a microscope, which objective lens should you start with?", "the lowest power", ["the highest power", "any lens at all", "no lens"], "Find the cells first, then zoom in."),
    ("Why is a stain such as iodine added to an onion cell slide?", "to make parts of the cells easier to see", ["to kill the cells", "to make the slide stick", "to make the cells grow"], "Contrast."),
    ("Why should you never use a mirror to reflect direct sunlight into a microscope?", "It can damage your eyes.", ["It makes cells move.", "It is too dark.", "It breaks the slide."], "Safety."),
    ("Why do muscle cells have lots of mitochondria?", "They need lots of energy from respiration.", ["They photosynthesise.", "They store water.", "They are plant cells."], "Structure fits function."),
    ("A cell has a cell wall but no chloroplasts. Where might it come from?", "inside a plant root", ["a human cheek", "a red blood cell", "a leaf surface in the sun"], "Root cells."),
])


def body():
    think = ("<p><b>All living things are made of cells.</b></p>"
             "<ul><li>Animal and plant cells have a nucleus, cell membrane, cytoplasm and mitochondria.</li>"
             "<li>Plant cells also have a cell wall, chloroplasts and a large vacuole.</li>"
             "<li>A light microscope magnifies cells: total magnification = eyepiece × objective.</li></ul>")
    ex = [("×10 eyepiece, ×40 objective. Total?", ["10 × 40"], "×400"),
          ("Which part controls the cell?", ["Contains DNA"], "the nucleus")]
    mist = ["Thinking animal cells have a cell wall.", "Thinking mitochondria are only in animal cells.", "Adding magnifications instead of multiplying them."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a cell", B1 + [(g_org, 12)]),
        ("Plant and animal cells", [(g_where, 7), (g_pic, 13)]),
        ("Labelled cells", [(g_pic, 12), (g_org, 8)]),
        ("The microscope", [(g_mic, 10), (g_mag, 10)]),
        ("Thinking about cells", B5 + [(g_mag, 10), (g_pic, 5)]),
    ])
    make_ks3(7, "cells", 1, "Biology", "Cells and organisation",
             "Cells as the fundamental unit of living organisms, including how to observe, interpret and record cell structure using a light microscope; the functions of the cell wall, cell membrane, cytoplasm, nucleus, vacuole, mitochondria and chloroplasts; the similarities and differences between plant and animal cells.",
             "Cells",
             "Year 7 Science: Cells Worksheets (Plant and Animal Cells, Microscopes)",
             "Cells",
             "Free Year 7 science worksheets on cells: the parts of plant and animal cells and their jobs, labelled cell diagrams, and using a light microscope with magnification. 100 questions with answers.",
             "All living things are made of cells.",
             "Plant cells also have a cell wall, chloroplasts and a large vacuole.",
             body(),
             [("What are the parts of an animal cell?", "A nucleus, cell membrane, cytoplasm and mitochondria."),
              ("How is a plant cell different from an animal cell?", "A plant cell also has a cell wall made of cellulose, chloroplasts for photosynthesis and a large permanent vacuole."),
              ("How do you work out magnification?", "Multiply the eyepiece magnification by the objective magnification. A ×10 eyepiece and ×40 objective give ×400.")],
             sets)


if __name__ == "__main__":
    main()
