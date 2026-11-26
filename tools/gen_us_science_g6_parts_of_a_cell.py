# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Parts of a Cell (MS-LS1-2)
  python tools/gen_us_science_g6_parts_of_a_cell.py
Develop and use a model to describe the function of a cell as a whole and ways the parts contribute:
nucleus, cytoplasm, cell membrane, mitochondria, cell wall, chloroplasts, vacuole. Plant vs. animal cells.
Assessment boundary: only these parts; no ribosomes, ER, Golgi in detail.
Wrong answers come from real mistakes: "animal cells have cell walls", "plants have no mitochondria",
"the nucleus makes food", "chloroplasts are in all cells".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, circle, line, text, People, INK, GREEN, LEAF

U = Unit(60102)
R = U.R
P = People(R)

JOB = {"nucleus": "controls the cell's activities and holds the genetic information (DNA)",
       "cell membrane": "controls what enters and leaves the cell",
       "cytoplasm": "a jelly-like fluid that holds the other parts",
       "mitochondria": "release energy from food (sugar) for the cell to use",
       "cell wall": "a stiff outer layer that supports and protects a plant cell",
       "chloroplasts": "capture sunlight to make food (sugar) by photosynthesis",
       "vacuole": "stores water and other materials"}
WHERE = {"nucleus": "both", "cell membrane": "both", "cytoplasm": "both", "mitochondria": "both", "cell wall": "plant", "chloroplasts": "plant", "vacuole": "both (large in plant cells)"}


def cell_svg(kind, marks, label=None):
    """kind 'plant' or 'animal'; marks {part: letter}."""
    W, H = 380, 240
    s = []
    if kind == "plant":
        s.append(rect(40, 20, 240, 200, "#e3f1d4", "#5a7d2a", 6, 6))
        s.append(rect(48, 28, 224, 184, "#f6fbef", INK, 1.5, 4))
        s.append(rect(62, 45, 100, 130, "#d6ecfa", "#6a9cc4", 1.5, 30))
        for x, y in [(235, 150), (75, 195), (255, 195), (190, 45)]:
            s.append("<ellipse cx='%d' cy='%d' rx='13' ry='7' fill='%s' stroke='%s' stroke-width='1'/>" % (x, y, LEAF, INK))
        nuc = (225, 95)
    else:
        s.append("<ellipse cx='160' cy='120' rx='130' ry='95' fill='#fdf1e4' stroke='%s' stroke-width='2'/>" % INK)
        s.append("<ellipse cx='200' cy='85' rx='16' ry='10' fill='#d6ecfa' stroke='#6a9cc4' stroke-width='1.5'/>")
        nuc = (150, 125)
    s.append(circle(nuc[0], nuc[1], 24, "#c9b3e6", INK, 1.5) + circle(nuc[0] + 4, nuc[1] - 3, 7, "#8e6cc0", "none", 0))
    for x, y in ([(150, 198), (110, 195)] if kind == "plant" else [(90, 90), (220, 160), (110, 170)]):
        s.append("<ellipse cx='%d' cy='%d' rx='14' ry='7' fill='#f4a582' stroke='%s' stroke-width='1'/>" % (x, y, INK)
                 + "<path d='M%d %d q4 -5 8 0 q4 5 8 0' fill='none' stroke='%s' stroke-width='1'/>" % (x - 8, y, INK))
    pts = {"plant": {"cell wall": (280, 35), "cell membrane": (272, 70), "nucleus": nuc, "chloroplasts": (235, 150), "vacuole": (140, 110), "mitochondria": (150, 198), "cytoplasm": (190, 140)},
           "animal": {"cell membrane": (285, 94), "nucleus": nuc, "mitochondria": (220, 160), "vacuole": (200, 85), "cytoplasm": (245, 125)}}[kind]
    ys = sorted(marks, key=lambda m: pts[m][1])
    for i, m in enumerate(ys):
        x, y = pts[m]
        ty = 30 + i * (180 / max(1, len(ys) - 1)) if len(ys) > 1 else 120
        s.append(line(x, y, 330, ty, INK, 1) + circle(x, y, 2.5, INK, INK, 0) + text(345, ty + 6, marks[m], 16))
    return svg_wrap(W, H, "".join(s), label or "a model of %s %s cell with labeled parts" % ("a" if kind == "plant" else "an", kind)).replace("<svg ", "<svg data-pf='lg' ", 1)


PLANT_PARTS = ["cell wall", "cell membrane", "nucleus", "chloroplasts", "vacuole", "mitochondria"]
ANIMAL_PARTS = ["cell membrane", "nucleus", "mitochondria", "cytoplasm"]


def g_label():
    kind = R.choice(["plant", "animal"])
    parts = R.sample(PLANT_PARTS if kind == "plant" else ANIMAL_PARTS, 4)
    letters = dict(zip(parts, "ABCD"))
    p = R.choice(parts)
    k = R.choice(["name", "job"])
    pic = fig(cell_svg(kind, letters))
    if k == "name":
        return item(pic + "This is a model of %s %s cell. Which letter points to the %s?" % ("a" if kind == "plant" else "an", kind, p), letters[p],
                    [letters[x] for x in parts if x != p], "The %s %s." % (p, JOB[p].replace("release", "releases").replace("capture", "captures")))
    return item(pic + "In this %s cell model, which labeled part %s?" % (kind, JOB[p].replace("release", "releases").replace("capture", "captures") if p not in ("cytoplasm",) else "is a jelly-like fluid that holds the other parts"),
                letters[p], [letters[x] for x in parts if x != p], "That part is the %s." % p)


def g_job():
    p = R.choice(sorted(JOB))
    w = [JOB[x] for x in JOB if x != p]
    return item("%s is labeling a cell model. What is the main job of the %s?" % (P.next()[0], p), JOB[p][0].upper() + JOB[p][1:], [x[0].upper() + x[1:] for x in R.sample(w, 3)], "The %s %s." % (p, JOB[p]))


def g_which():
    p = R.choice(sorted(JOB))
    j = JOB[p].replace("release", "releases").replace("capture", "captures")
    w = [x for x in JOB if x != p and not {x, p} <= {"cell wall", "cell membrane"}]
    who = P.next()[0]
    return item(("%s's notes say one cell part %s. Which part is it?" % (who, j)) if p != "cytoplasm" else "%s's notes describe a jelly-like fluid that holds the other parts. Which part is it?" % who, "the " + p, ["the " + x for x in R.sample(w, 3)],
                "The %s %s." % (p, JOB[p]))


def g_plantanimal():
    k = R.choice(["plantonly", "both", "animal"])
    if k == "plantonly":
        p = R.choice(["cell wall", "chloroplasts"])
        return item("Which part is found in plant cells but NOT in animal cells?", "the " + p, ["the nucleus", "the cell membrane", "the mitochondria"],
                    "Only plant cells have a cell wall and chloroplasts.")
    if k == "both":
        p = R.choice(["nucleus", "cell membrane", "mitochondria", "cytoplasm"])
        return item("Which part is found in BOTH plant and animal cells?", "the " + p, ["the cell wall", "the chloroplasts", "the cell wall and chloroplasts only"],
                    "Both plant and animal cells have a nucleus, cell membrane, cytoplasm and mitochondria.")
    q = R.choice([("A cell has a cell wall, chloroplasts and a large vacuole. What kind of cell is it?", "a plant cell", ["an animal cell", "a red blood cell", "a nerve cell"]),
                  ("A cell has a nucleus, mitochondria and a cell membrane, but no cell wall and no chloroplasts. What kind of cell is it most likely?", "an animal cell", ["a leaf cell", "a plant cell", "a cell from a pine needle"]),
                  ("A cell from a carrot root has a cell wall but no chloroplasts. What kind of cell is it?", "a plant cell that does not get sunlight", ["an animal cell", "a bacterium", "a nerve cell"])])
    return item(q[0], q[1], q[2], "Cell walls and chloroplasts are found in plant cells; root cells do not get light, so they have no chloroplasts.")


B1 = bank([
    ("Why do both plant and animal cells need mitochondria?", "All cells need energy released from food.", ["Only animals use energy.", "Mitochondria make sunlight.", "Plants do not need energy."],
     "Plants make sugar in chloroplasts and release its energy in mitochondria."),
    ("What would happen to a cell if its cell membrane stopped working?", "It could not control what goes in and out.", ["It would make more food.", "It would grow a cell wall.", "Nothing would change."],
     "The membrane is the cell's gatekeeper."),
    ("Why are leaves green?", "Their cells have many chloroplasts, which contain a green pigment.", ["Their cell walls are green paint.", "Their nucleus is green.", "Water is green."],
     "Chlorophyll in chloroplasts is green."),
    ("Which part keeps a plant cell's shape firm, like a box?", "the cell wall", ["the cell membrane", "the nucleus", "the mitochondria"], "The stiff wall supports the plant."),
    ("Why does a plant wilt when it lacks water?", "Its vacuoles shrink, so the cells lose their firmness.", ["The nucleus disappears.", "Chloroplasts turn into mitochondria.", "The cell wall grows."],
     "Full vacuoles push against the cell wall and keep the plant upright."),
    ("A cell is like a school. Which part is like the principal's office that gives instructions?", "the nucleus", ["the cell membrane", "the cytoplasm", "the vacuole"],
     "The nucleus controls the cell."),
    ("A cell is like a factory. Which part is like the power plant?", "the mitochondria", ["the vacuole", "the cell wall", "the nucleus"], "Mitochondria release energy."),
    ("What is the cell as a whole able to do?", "carry out all the processes of life, like using energy, growing and responding", ["only store water", "only make sugar", "nothing on its own"],
     "The parts work together so the cell can live."),
])
B5 = bank([
    ("Ava looks at an Elodea leaf under a microscope and sees green dots moving around. What are the green dots?", "chloroplasts", ["mitochondria", "nuclei", "cell walls"],
     "Chloroplasts are green and easy to see in leaf cells."),
    ("Leo stains cheek cells with iodine and sees a dark spot in each cell. What is the dark spot?", "the nucleus", ["a chloroplast", "a cell wall", "a vacuole"], "Stain makes the nucleus stand out."),
    ("Mia builds a 3D cell model with a clear bag, gelatin, and a plum. What does the gelatin stand for?", "the cytoplasm", ["the nucleus", "the cell wall", "the mitochondria"],
     "The gelatin is a jelly-like fluid, like cytoplasm."),
    ("In Mia's model, the bag stands for the cell membrane. What could she add to model a plant cell?", "a stiff box around the bag for the cell wall, and green beads for chloroplasts", ["nothing; plant cells are the same", "a second plum", "a red bead for blood"],
     "Plant cells also have a cell wall and chloroplasts."),
    ("Why might a muscle cell have many more mitochondria than a skin cell?", "Muscle cells need a lot of energy to move the body.", ["Muscles need no energy.", "Skin cells make sugar.", "Muscles have no nucleus."],
     "Cells that do more work need more mitochondria."),
])


def body():
    think = ("<p>A cell is like a tiny factory. Its parts work together so the cell can live:</p><ul>"
             + "".join("<li><b>%s</b>: %s.</li>" % (k[0].upper() + k[1:], v) for k, v in JOB.items()) + "</ul>"
             + figure(cell_svg("plant", {"cell wall": "A", "nucleus": "B", "chloroplasts": "C", "vacuole": "D"}), "Plant cell: A cell wall, B nucleus, C chloroplast, D vacuole.")
             + "<p>Both plant and animal cells have a nucleus, cell membrane, cytoplasm and mitochondria. Only plant cells have a <b>cell wall</b> and <b>chloroplasts</b>, and they have a large vacuole.</p>")
    ex = [("Which part makes food in a plant cell?", ["Food is made using sunlight."], "chloroplasts"),
          ("Does an animal cell have a cell wall?", ["Only plant cells have one."], "No.")]
    mist = ["Thinking animal cells have cell walls.",
            "Thinking plant cells do not have mitochondria. They do.",
            "Mixing up the cell membrane (gatekeeper) and the cell wall (stiff support)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Cell parts and their jobs", B1 + [(g_job, 6), (g_which, 6)]),
        ("What does each part do?", [(g_job, 10), (g_which, 10)]),
        ("Cell models", [(g_label, 16), (g_job, 4)]),
        ("Plant and animal cells", [(g_plantanimal, 10), (g_label, 6), (g_which, 4)]),
        ("Investigating cells", B5 + [g_label, g_plantanimal, g_which]),
    ])
    make("grade-6", "parts-of-a-cell", 2, "MS-LS1-2",
         "Develop and use a model to describe the function of a cell as a whole and ways the parts of cells contribute to the function.",
         "Parts of a Cell",
         "Grade 6 Cell Parts Worksheets: Organelles and Plant vs. Animal Cells",
         "Parts of a Cell",
         "Free middle school science worksheets on parts of a cell (NGSS MS-LS1-2): nucleus, cell membrane, cytoplasm, mitochondria, cell wall, chloroplasts and vacuoles, labeled cell models and plant vs. animal cells. 100 practice questions with answers.",
         "Each cell part has a job.",
         "The nucleus controls the cell, mitochondria release energy, and chloroplasts make food in plant cells.",
         body(),
         [("What are the main parts of a cell?", "The nucleus, cell membrane, cytoplasm and mitochondria. Plant cells also have a cell wall, chloroplasts and a large vacuole."),
          ("How are plant and animal cells different?", "Plant cells have a cell wall, chloroplasts and a large vacuole. Animal cells do not have a cell wall or chloroplasts."),
          ("What do mitochondria do?", "They release energy from food (sugar) so the cell can use it.")],
         sets)


if __name__ == "__main__":
    main()
