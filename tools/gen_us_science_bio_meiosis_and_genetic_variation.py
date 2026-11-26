# -*- coding: utf-8 -*-
"""
US High School Biology: Meiosis and Genetic Variation (HS-LS3-1, HS-LS3-2)
  python tools/gen_us_science_bio_meiosis_and_genetic_variation.py
Ask questions to clarify relationships about the role of DNA and chromosomes in coding the instructions for
characteristic traits passed from parents to offspring; make and defend a claim that inheritable genetic variations
may result from new combinations through meiosis, viable errors during replication, and/or mutations caused by
environmental factors.
Chromosomes, genes and alleles; diploid and haploid numbers; stages of meiosis; mitosis vs meiosis; independent
assortment (2^n combinations), crossing over, fertilization and mutation as sources of variation.
Wrong answers come from real mistakes: "gametes have the same number of chromosomes", "meiosis makes 2 identical cells",
"only mutations cause variation".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90113)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SPECIES = [("human", 46), ("dog", 78), ("cat", 38), ("fruit fly", 8), ("corn", 20), ("chimpanzee", 48), ("horse", 64), ("mouse", 40), ("potato", 48), ("chicken", 78), ("rice", 24), ("pea plant", 14)]


def g_num():
    sp, n = R.choice(SPECIES)
    k = R.choice(["gamete", "zygote", "pairs", "after1"])
    if not once((sp, k)):
        return None
    if k == "after1":
        return item("A %s cell (2n = %d) finishes meiosis I. How many chromosomes are in each of the two new cells?" % (sp, n), str(n // 2), [str(n), str(n * 2), str(n // 4)],
                    "Homologs separate in meiosis I, so each cell has %d (each still with two chromatids)." % (n // 2))
    if k == "gamete":
        return item("A %s body cell has %d chromosomes (2n). How many are in each egg or sperm cell?" % (sp, n), str(n // 2), [str(n), str(n * 2), str(n // 4)],
                    "Meiosis halves the number: n = %d." % (n // 2))
    if k == "zygote":
        return item("A %s egg and sperm each have %d chromosomes. How many does the fertilized egg have?" % (sp, n // 2), str(n), [str(n // 2), str(n * 2), str(n // 2 + 1)],
                    "%d + %d = %d." % (n // 2, n // 2, n))
    return item("A %s body cell has %d chromosomes. How many homologous pairs is that?" % (sp, n), str(n // 2), [str(n), str(n * 2), str(n // 2 + 2)], "%d ÷ 2 = %d pairs." % (n, n // 2))


def g_assort():
    if R.random() < 0.5:
        sp, c = R.choice([x for x in SPECIES if x[1] <= 48])
        n = c // 2
        if not once(("sp", sp)):
            return None
        return item("A %s has %d chromosomes in each body cell. By independent assortment alone, how many different gametes are possible?" % (sp, c), comma(2 ** n),
                    [comma(2 * n), comma(c), comma(2 ** (n - 1))], "%d pairs: 2^%d = %s." % (n, n, comma(2 ** n)))
    n = R.randint(2, 12)
    if not once(n):
        return None
    a = 2 ** n
    return item("An organism has %d pairs of chromosomes. By independent assortment alone, how many different gamete combinations are possible?" % n, comma(a), [comma(2 * n), comma(n * n), comma(2 ** (n - 1))],
                "2^%d = %s." % (n, comma(a)))


ST = [("Homologous chromosomes pair up and swap pieces (crossing over).", "prophase I"), ("Homologous pairs line up in the middle of the cell.", "metaphase I"),
      ("Homologous chromosomes separate to opposite poles.", "anaphase I"), ("Sister chromatids separate to opposite poles.", "anaphase II"),
      ("Single chromosomes line up in the middle of two cells.", "metaphase II"), ("Four haploid cells are formed.", "telophase II and cytokinesis")]


def g_stage():
    s, a = R.choice(ST)
    if not once(s):
        return None
    return item("Which stage of meiosis? %s" % s, a, R.sample([x[1] for x in ST if x[1] != a], 3), "Meiosis I separates homologs; meiosis II separates sister chromatids.")


CMP = [("number of divisions", "two", "one"), ("number of cells produced", "four", "two"), ("chromosome number in new cells", "half (haploid)", "same (diploid)"),
       ("are the new cells identical?", "no, genetically different", "yes, identical"), ("main purpose", "making gametes for sexual reproduction", "growth and repair"),
       ("crossing over happens?", "yes", "no")]


def g_cmp():
    f, me, mi = R.choice(CMP)
    k = R.choice(["meiosis", "mitosis"])
    if not once((f, k)):
        return None
    a = me if k == "meiosis" else mi
    b = mi if k == "meiosis" else me
    w = [b] + R.sample([x for x in ["one", "three", "eight", "double", "only in plants", "only in bacteria"] if x not in (a, b)], 2)
    return item("%s: %s?" % (k.capitalize(), f.rstrip("?")), a, w, "Meiosis: %s. Mitosis: %s." % (me, mi))


SRC = [("Two chromatids from a homologous pair swap a section in prophase I.", "crossing over"),
       ("Each homologous pair lines up independently of the others in metaphase I.", "independent assortment"),
       ("Any sperm can join with any egg.", "random fertilization"),
       ("UV light changes a base in a skin cell's DNA.", "a mutation caused by the environment"),
       ("DNA polymerase puts in the wrong base and it is not repaired.", "a replication error (mutation)"),
       ("A chemical in cigarette smoke damages DNA.", "a mutation caused by the environment"),
       ("Homologous chromosomes trade alleles, making new combinations on one chromosome.", "crossing over"),
       ("Siblings with the same parents get different mixes of chromosomes.", "independent assortment")]


def g_src():
    s, a = R.choice(SRC)
    if not once(s):
        return None
    return item("%s Which source of genetic variation is this?" % s, a, R.sample(sorted({x[1] for x in SRC if x[1] != a}), 3), "Meiosis, fertilization and mutation create variation.")


def g_inherit():
    k = R.choice(["body", "gamete"])
    who = P.next()[0]
    if not once((k, who)) or not once(k, 3):
        return None
    if k == "body":
        return item("%s's father gets a mutation in a skin cell from sunburn. Can it be passed to his children?" % who, "No. Only mutations in sex cells (gametes) can be inherited.",
                    ["Yes, all mutations are inherited.", "Yes, but only to daughters.", "Only if he gets more sunburns."], "Body-cell mutations are not inherited.")
    return item("A mutation happens in a cell that makes %s's mother's eggs. Can it be inherited?" % who, "Yes. It can be in an egg that is fertilized.",
                ["No, never.", "Only if it is in skin cells.", "Only in boys."], "Gamete mutations can be passed on.")


B1 = bank([
    ("What is a chromosome?", "a long DNA molecule with many genes, wrapped around proteins", ["a single gene", "a protein only", "a type of cell"], "Genes are on chromosomes."),
    ("What is an allele?", "a different version of the same gene", ["a whole chromosome", "a type of cell", "a protein"], "For example, blue or brown eye alleles."),
    ("What does diploid (2n) mean?", "two sets of chromosomes, one from each parent", ["one set of chromosomes", "no chromosomes", "four sets"], "Body cells are diploid."),
    ("What does haploid (n) mean?", "one set of chromosomes", ["two sets", "no DNA", "a double cell"], "Gametes are haploid."),
    ("Why must gametes be haploid?", "So the zygote has the normal diploid number after fertilization.", ["So they are bigger.", "So they can photosynthesize.", "So they copy DNA faster."], "n + n = 2n."),
    ("What are homologous chromosomes?", "a matching pair, one from each parent, with the same genes", ["two identical sister chromatids", "two different species' chromosomes", "two sex cells"], "Same genes, maybe different alleles."),
    ("What is crossing over?", "homologous chromosomes swapping segments", ["DNA copying itself", "cells splitting in two", "a chromosome being lost"], "Prophase I."),
    ("Where are the instructions for traits stored?", "in the DNA sequence of genes", ["in the cell membrane", "in fat", "in sugar"], "Genes code for proteins."),
])
B5 = bank([
    ("Two children of the same parents look different. Which best explains it?", "Meiosis and fertilization give each child a different mix of alleles.", ["They have different parents.", "Only mutations explain it.", "Their DNA is identical."], "New combinations."),
    ("Nondisjunction makes a gamete with an extra chromosome 21. What can result?", "Down syndrome (three copies of chromosome 21)", ["no effect ever", "a haploid zygote", "a new species"], "An error in meiosis."),
    ("Which claim is best supported: inheritable variation comes only from mutations?", "False. Meiosis and fertilization also create new combinations.", ["True.", "True for plants only.", "True for animals only."], "Several sources."),
    ("A geneticist sees chromosomes swap pieces under a microscope during meiosis. What stage is she most likely viewing?", "prophase I", ["anaphase II", "interphase", "telophase II"], "Crossing over happens in prophase I."),
    ("A plant has 2n = 14. How many chromosomes are in its pollen (sperm) cells?", "7", ["14", "28", "3"], "14 ÷ 2 = 7."),
])


def body():
    think = ("<p><b>Meiosis makes gametes with half the chromosomes, each one different.</b></p>"
             "<ul><li>Diploid body cell (2n) → meiosis I and II → four haploid gametes (n).</li>"
             "<li>Variation: crossing over, independent assortment (2<sup>n</sup> combinations), random fertilization and mutations.</li>"
             "<li>Only mutations in gametes are inherited.</li></ul>")
    ex = [("Human 2n = 46. Sperm?", ["Halve it"], "23"),
          ("3 chromosome pairs. Gamete combinations?", ["2^3"], "8")]
    mist = ["Thinking gametes have the full chromosome number.", "Thinking meiosis makes two identical cells.", "Thinking only mutations cause variation."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Chromosomes and genes", B1 + [(g_num, 6), (g_cmp, 6)]),
        ("Haploid and diploid", [(g_num, 14), (g_stage, 6)]),
        ("Stages of meiosis", [(g_cmp, 6), (g_assort, 11), (g_src, 3)]),
        ("Sources of variation", [(g_src, 5), (g_inherit, 4), (g_num, 6), (g_assort, 5)]),
        ("Inheritance claims", B5 + [(g_num, 10), (g_assort, 5)]),
    ])
    make("biology", "meiosis-and-genetic-variation", 13, "HS-LS3-1, HS-LS3-2",
         "Ask questions to clarify relationships about the role of DNA and chromosomes in coding the instructions for characteristic traits passed from parents to offspring. "
         "Make and defend a claim based on evidence that inheritable genetic variations may result from new genetic combinations through meiosis, viable errors occurring during replication, and/or mutations caused by environmental factors.",
         "Meiosis and Genetic Variation",
         "Meiosis Worksheets: Haploid Cells, Crossing Over and Variation (High School Biology)",
         "Meiosis and Variation",
         "Free high school biology worksheets on meiosis and genetic variation (NGSS HS-LS3-1, HS-LS3-2): chromosomes, haploid and diploid, stages of meiosis and sources of variation. 100 questions with answers.",
         "Meiosis halves and mixes chromosomes.",
         "Crossing over, independent assortment, fertilization and mutation make each offspring different.",
         body(),
         [("How is meiosis different from mitosis?", "Meiosis has two divisions and makes four genetically different haploid cells. Mitosis has one division and makes two identical diploid cells."),
          ("Where does genetic variation come from?", "Crossing over, independent assortment, random fertilization and mutations (replication errors or damage from the environment)."),
          ("Are all mutations inherited?", "No. Only mutations in cells that make eggs or sperm can be passed to offspring.")],
         sets)


if __name__ == "__main__":
    main()
