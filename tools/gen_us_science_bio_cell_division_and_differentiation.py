# -*- coding: utf-8 -*-
"""
US High School Biology: Cell Division and Differentiation (HS-LS1-4)
  python tools/gen_us_science_bio_cell_division_and_differentiation.py
Use a model to illustrate the role of cellular division (mitosis) and differentiation in producing and maintaining
complex organisms. The cell cycle and the phases of mitosis, chromosome numbers, cell counts after many divisions,
reading a microscope count of cells in each phase, stem cells and differentiation.
Wrong answers come from real mistakes: "mitosis halves the chromosome number", "a cell spends most of its life dividing",
"different cell types have different DNA".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90104)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


PH = [("Chromosomes condense and become visible; the nuclear membrane breaks down.", "prophase"),
      ("Chromosomes line up in the middle of the cell.", "metaphase"),
      ("Sister chromatids are pulled apart to opposite ends of the cell.", "anaphase"),
      ("Two new nuclei form around the chromosomes at each end.", "telophase"),
      ("The cytoplasm splits and two daughter cells form.", "cytokinesis"),
      ("The cell grows and copies its DNA.", "interphase"),
      ("Spindle fibers attach to the centromeres at the cell's middle line.", "metaphase"),
      ("The cell looks pinched in the middle as it splits in two.", "cytokinesis"),
      ("The chromosomes start to uncoil as new nuclear membranes appear.", "telophase"),
      ("DNA is replicated during the S stage.", "interphase")]
PHN = ["interphase", "prophase", "metaphase", "anaphase", "telophase", "cytokinesis"]


def g_phase():
    d, a = R.choice(PH)
    if not once(d):
        return None
    return item("Which stage is this? %s" % d, a, R.sample([p for p in PHN if p != a], 3), "%s: %s" % (a.capitalize(), d))


def g_order():
    i = R.randrange(5)
    k = R.choice(["after", "before"])
    j = i + 1 if k == "after" else i
    ask = PHN[i] if k == "after" else PHN[i + 1]
    ans = PHN[j]
    if not once((i, k)):
        return None
    return item("Which stage comes right %s %s?" % (k, ask), ans, R.sample([p for p in PHN if p not in (ans, ask)], 3), "Order: interphase, prophase, metaphase, anaphase, telophase, cytokinesis.")


SPECIES = [("human", 46), ("dog", 78), ("cat", 38), ("fruit fly", 8), ("corn", 20), ("chimpanzee", 48), ("horse", 64), ("garden onion", 16), ("mouse", 40), ("potato", 48)]


def g_chrom():
    sp, n = R.choice(SPECIES)
    k = R.choice(["daughter", "chromatids", "total"])
    if not once((sp, k)):
        return None
    if k == "daughter":
        return item("A %s body cell has %d chromosomes. How many chromosomes are in each daughter cell after mitosis?" % (sp, n), str(n), [str(n // 2), str(n * 2), str(n + 2)],
                    "Mitosis makes identical cells with the same number.")
    if k == "chromatids":
        return item("A %s cell has %d chromosomes. After DNA replication, how many sister chromatids are there?" % (sp, n), str(2 * n), [str(n), str(n // 2), str(4 * n)],
                    "Each chromosome is copied: %d × 2 = %d." % (n, 2 * n))
    return item("A %s cell with %d chromosomes divides by mitosis. How many chromosomes are in both daughter cells together?" % (sp, n), str(2 * n), [str(n), str(n // 2), str(3 * n)],
                "Two cells × %d = %d." % (n, 2 * n))


def g_cells():
    n = R.randint(2, 10)
    start = R.choice([1, 1, 2, 3, 5])
    if not once((n, start)):
        return None
    a = start * 2 ** n
    return item("%s divide%s by mitosis %d times in a row (every cell divides each time). How many cells are there at the end?" % (
        "One cell" if start == 1 else "%d cells" % start, "s" if start == 1 else "", n), comma(a), [comma(start * 2 * n), comma(start * 2 ** (n - 1)), comma(start * (n + 1))],
        "%s × 2^%d = %s." % (start, n, comma(a)))


def g_count():
    who = P.next()[0]
    vals = {"interphase": R.randint(70, 90), "prophase": R.randint(5, 12), "metaphase": R.randint(2, 6), "anaphase": R.randint(1, 4), "telophase": R.randint(2, 5)}
    if len(set(vals.values())) < 5:
        return None
    tot = sum(vals.values())
    k = R.choice(["most", "least", "pct", "total"])
    if not once((tuple(vals.values()), k)):
        return None
    tab = table(["Stage", "Number of onion root tip cells"], [[a, str(b)] for a, b in vals.items()])
    if k == "most":
        return item(tab + "%s counted cells under a microscope. Which stage takes the longest?" % who, "interphase", ["prophase", "metaphase", "anaphase"],
                    "Most cells are in interphase, so it lasts longest.")
    if k == "least":
        a = min(vals, key=vals.get)
        return item(tab + "From %s's count, which stage is the shortest?" % who, a, R.sample([x for x in vals if x != a], 3), "The fewest cells: %d." % vals[a])
    if k == "total":
        return item(tab + "How many cells did %s count in all?" % who, str(tot), [str(tot - vals["interphase"]), str(vals["interphase"]), str(tot + 10)], "Add all the numbers.")
    m = tot - vals["interphase"]
    return item(tab + "How many of %s's cells were dividing (not in interphase)?" % who, str(m), [str(vals["interphase"]), str(tot), str(vals["prophase"])],
                "%d − %d = %d." % (tot, vals["interphase"], m))


DIFF = [("A stem cell in bone marrow becomes a red blood cell.", "differentiation"), ("A skin cut heals as new skin cells are made.", "mitosis for repair"),
        ("A baby grows taller over many years.", "mitosis for growth"), ("An embryo's cells become heart, nerve and skin cells.", "differentiation"),
        ("A lizard regrows a lost tail.", "mitosis for repair"), ("A plant's root tip gets longer.", "mitosis for growth"),
        ("A stem cell in the brain becomes a neuron.", "differentiation"), ("Cells lining the intestine are replaced every few days.", "mitosis for repair")]


def g_diff():
    s, a = R.choice(DIFF)
    if not once(s):
        return None
    w = [x for x in ["differentiation", "mitosis for repair", "mitosis for growth", "meiosis to make sex cells"] if x != a]
    return item("%s Which process is this mainly?" % s, a, w, "Mitosis makes more cells; differentiation makes cells specialized.")


B1 = bank([
    ("What does mitosis produce?", "two identical daughter cells", ["four different sex cells", "one bigger cell", "two cells with half the DNA"], "Same chromosome number."),
    ("Why do multicellular organisms need mitosis?", "for growth and to repair or replace cells", ["to make eggs and sperm", "to digest food", "to make DNA different"], "More cells for growth and repair."),
    ("During which stage is DNA copied?", "interphase (S stage)", ["metaphase", "anaphase", "cytokinesis"], "Before mitosis begins."),
    ("What is a stem cell?", "an unspecialized cell that can become different cell types", ["a cell in a plant stem only", "a dead cell", "a sex cell"], "It can differentiate."),
    ("What is differentiation?", "cells becoming specialized for different jobs", ["cells copying DNA", "cells dying", "cells dividing in half"], "Same DNA, different genes on."),
    ("Do a muscle cell and a nerve cell in the same person have the same DNA?", "Yes, but they use different genes.", ["No, different DNA.", "Muscle cells have no DNA.", "Only nerve cells have DNA."], "Gene expression differs."),
    ("What can happen when the cell cycle is not controlled?", "cells divide too much and can form a tumor (cancer)", ["cells stop growing forever", "cells turn into sugar", "nothing happens"], "Cancer is uncontrolled division."),
    ("What structure pulls chromosomes apart?", "spindle fibers", ["the cell wall", "ribosomes", "the nucleolus"], "Spindles attach at centromeres."),
])
B5 = bank([
    ("Why are onion root tips used to study mitosis?", "The cells there divide quickly, so many are in mitosis.", ["They have no DNA.", "They are sex cells.", "They do not divide."], "Growing tips divide a lot."),
    ("A drug stops spindle fibers from forming. What happens to dividing cells?", "Chromosomes cannot separate, so mitosis stops.", ["Cells divide faster.", "DNA is not copied.", "Cells become stem cells."], "Some cancer drugs work this way."),
    ("Doctors grow new skin from a patient's stem cells. Why is this useful?", "The stem cells can differentiate into skin cells that match the patient.", ["Stem cells cannot divide.", "Skin cells become bone.", "It changes the patient's DNA."], "Medical use of differentiation."),
    ("If a cell cycle takes 24 hours and 90% of cells are in interphase, about how long is interphase?", "about 21.6 hours", ["about 2.4 hours", "about 9 hours", "about 24 minutes"], "0.9 × 24 = 21.6."),
    ("A model shows one fertilized egg becoming a whole body. Which two processes does it show?", "mitosis and differentiation", ["meiosis and photosynthesis", "only meiosis", "only respiration"], "Many cells, then specialized cells."),
])


def body():
    think = ("<p><b>One cell → many cells → many kinds of cells.</b></p>"
             "<ul><li><b>Interphase:</b> the cell grows and copies its DNA (most of the cycle).</li>"
             "<li><b>Mitosis:</b> prophase, metaphase, anaphase, telophase; then cytokinesis. Two identical cells, same chromosome number.</li>"
             "<li><b>Differentiation:</b> stem cells turn on different genes and become muscle, nerve or blood cells.</li></ul>")
    ex = [("A human cell (46 chromosomes) divides by mitosis. Daughter cells?", ["Mitosis keeps the number"], "46 each"),
          ("One cell divides 5 times. How many cells?", ["2^5"], "32")]
    mist = ["Thinking mitosis halves the chromosome number. Meiosis does that.", "Thinking a cell spends most of its time dividing. Most time is interphase.",
            "Thinking different cell types have different DNA. They use different genes."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The cell cycle", B1 + [(g_phase, 6), (g_order, 6)]),
        ("Phases of mitosis", [(g_phase, 4), (g_order, 4), (g_chrom, 12)]),
        ("Counting cells and chromosomes", [(g_chrom, 10), (g_cells, 10)]),
        ("Microscope data", [(g_count, 12), (g_diff, 8)]),
        ("Growth, repair and stem cells", B5 + [(g_count, 6), (g_cells, 6), (g_chrom, 3)]),
    ])
    make("biology", "cell-division-and-differentiation", 4, "HS-LS1-4",
         "Use a model to illustrate the role of cellular division (mitosis) and differentiation in producing and maintaining complex organisms.",
         "Cell Division and Differentiation",
         "Mitosis Worksheets: The Cell Cycle, Phases of Mitosis and Stem Cells (Biology)",
         "Mitosis and Differentiation",
         "Free high school biology worksheets on mitosis and differentiation (NGSS HS-LS1-4): the cell cycle, phases of mitosis, chromosome numbers and stem cells. 100 questions with answers.",
         "Mitosis makes identical cells.",
         "Differentiation turns them into many kinds of specialized cells.",
         body(),
         [("What are the phases of mitosis?", "Prophase, metaphase, anaphase and telophase, followed by cytokinesis. Before mitosis, the cell copies its DNA in interphase."),
          ("How many chromosomes do daughter cells have?", "The same number as the parent cell. A human cell with 46 chromosomes makes two cells with 46 each."),
          ("How do cells become different if they have the same DNA?", "During differentiation, each cell type turns on different genes.")],
         sets)


if __name__ == "__main__":
    main()
