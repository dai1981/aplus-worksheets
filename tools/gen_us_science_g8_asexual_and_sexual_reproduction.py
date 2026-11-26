# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Asexual and Sexual Reproduction (MS-LS3-2)
  python tools/gen_us_science_g8_asexual_and_sexual_reproduction.py
Develop and use a model to describe why asexual reproduction results in offspring with identical genetic information
and sexual reproduction results in offspring with genetic variation. Half of the chromosomes from each parent,
alleles (dominant / recessive), Punnett squares and probabilities, examples of asexual reproduction.
Wrong answers come from real mistakes: "offspring get all genes from one parent in sexual reproduction",
"a recessive trait can never show up", "Bb x Bb gives 50% recessive", "asexual offspring vary a lot".
"""
from sci_common import Unit, item, bank, lesson, make, People

U = Unit(80113)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


TRAITS = [("pea plants", "P", "purple flowers", "white flowers"), ("guinea pigs", "B", "black fur", "white fur"), ("pea plants", "T", "tall stems", "short stems"),
          ("pea plants", "Y", "yellow seeds", "green seeds"), ("rabbits", "B", "brown fur", "white fur"), ("dogs", "S", "short fur", "long fur"),
          ("tomato plants", "R", "red fruit", "yellow fruit"), ("fruit flies", "W", "red eyes", "white eyes")]


def square(a, b):
    cells = [[x + y if x.isupper() or not y.isupper() else y + x for y in b] for x in a]
    td = "style='border:1px solid #888;padding:6px 14px;text-align:center'"
    rows = "<tr><td %s></td><th %s>%s</th><th %s>%s</th></tr>" % (td, td, b[0], td, b[1])
    for i, x in enumerate(a):
        rows += "<tr><th %s>%s</th><td %s>%s</td><td %s>%s</td></tr>" % (td, x, td, cells[i][0], td, cells[i][1])
    return "<table style='border-collapse:collapse;margin:6px 0'>%s</table>" % rows, [c for r in cells for c in r]


def g_punnett():
    org, L, dom, rec = R.choice(TRAITS)
    l = L.lower()
    ga = R.choice([L + l, L + L, l + l])
    gb = R.choice([L + l, l + l])
    if ga == l + l and gb == l + l:
        return None
    k = R.choice(["rec", "dom", "het"])
    if not once((org, L, ga, gb, k)):
        return None
    who = P.next()[0]
    tab, cells = square(list(ga), list(gb))
    nrec = sum(1 for c in cells if c == l + l)
    nhet = sum(1 for c in cells if c[0] == L and c[1] == l)
    pct = {0: "0%", 1: "25%", 2: "50%", 3: "75%", 4: "100%"}
    if k == "rec":
        a = pct[nrec]
        q = "What percent of the offspring are expected to have %s?" % rec
    elif k == "dom":
        a = pct[4 - nrec]
        q = "What percent of the offspring are expected to have %s?" % dom
    else:
        a = pct[nhet]
        q = "What percent of the offspring are expected to be heterozygous (%s%s)?" % (L, l)
    w = [x for x in ["0%", "25%", "50%", "75%", "100%"] if x != a]
    R.shuffle(w)
    return item("In %s, the allele for %s (%s) is dominant over the allele for %s (%s). %s crosses two parents: %s × %s.%s%s" % (org, dom, L, rec, l, who, ga, gb, tab, q), a, w[:3],
                "Count the boxes in the Punnett square: each box is 25%.")


def g_geno():
    org, L, dom, rec = R.choice(TRAITS)
    l = L.lower()
    g = R.choice([L + L, L + l, l + l])
    k = R.choice(["pheno", "name"])
    if not once(("g", org, L, g, k)):
        return None
    who = P.next()[0]
    if k == "pheno":
        a = rec if g == l + l else dom
        return item("In %s, the allele for %s (%s) is dominant over the allele for %s (%s). One of %s's %s has the genotype %s. What is its phenotype?" % (org, dom, L, rec, l, who, org, g), a,
                    [rec if a == dom else dom, "a mix of both traits", "it cannot be known"], "One dominant allele is enough to show the dominant trait." if g != l + l else "Two recessive alleles show the recessive trait.")
    nm = {L + L: "homozygous dominant", L + l: "heterozygous", l + l: "homozygous recessive"}
    return item("%s writes the genotype %s for a %s trait. How is this genotype described?" % (who, g, org[:-1] if org.endswith("s") else org), nm[g], [v for x, v in nm.items() if x != g] + ["a mutation"],
                "Same two alleles = homozygous; different alleles = heterozygous.")


ASEX = [("A strawberry plant sends out runners that grow new plants.", "asexual"), ("A bacterium splits into two cells.", "asexual"), ("A hydra grows a bud that breaks off.", "asexual"),
        ("A potato sprouts new plants from its eyes.", "asexual"), ("A sea star regrows a whole body from one arm.", "asexual"), ("Yeast cells form buds that separate.", "asexual"),
        ("A gardener plants a cutting from a geranium.", "asexual"), ("A frog's egg is fertilized by sperm.", "sexual"), ("Bees carry pollen so flowers make seeds.", "sexual"),
        ("Two dogs have a litter of puppies.", "sexual"), ("Salmon release eggs and sperm in a stream.", "sexual"), ("An oak tree grows from an acorn after pollination.", "sexual")]


def g_kind():
    s, a = R.choice(ASEX)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once(("k", s, t)):
        return None
    if t:
        return item("%s reads: “%s” What type of reproduction is this?" % (who, s), a + " reproduction", [("sexual" if a == "asexual" else "asexual") + " reproduction", "no reproduction", "mutation only"],
                    "Asexual: one parent. Sexual: two parents (egg and sperm, or pollen and egg).")
    gen = "identical to the parent's" if a == "asexual" else "a mix of genes from two parents"
    return item("%s reads: “%s” How will the offspring's genetic information compare with the parent's?" % (who, s), "It will be " + gen + ".",
                ["It will be " + ("a mix of genes from two parents" if a == "asexual" else "identical to one parent's") + ".", "It will have no genes.", "It will be completely random with no parent genes."],
                "Asexual reproduction copies one parent's DNA; sexual reproduction combines DNA from two parents.")


B1 = bank([
    ("Why are offspring from asexual reproduction identical to the parent?", "They receive a copy of all of one parent's genetic information.", ["They get half from each of two parents.", "They have no DNA.", "They mutate on purpose."], "One parent, copied DNA."),
    ("Why do offspring from sexual reproduction show variation?", "They get half their chromosomes from each parent, in new combinations.", ["They are copies of one parent.", "They choose their own genes.", "They have no chromosomes."], "Mixing creates variation."),
    ("How many sets of chromosomes does a human get from each parent?", "one set (23 chromosomes) from each parent", ["all 46 from the mother", "all 46 from the father", "none"], "23 + 23 = 46."),
    ("What is an allele?", "a different version of the same gene", ["a whole chromosome", "a kind of cell", "an offspring"], "For example, B or b."),
    ("What does a dominant allele do?", "It shows its trait even when only one copy is present.", ["It is always hidden.", "It needs two copies to show.", "It never passes to offspring."], "Shown by a capital letter."),
    ("When does a recessive trait appear?", "when an organism has two recessive alleles", ["never", "when one recessive allele is present", "only in asexual reproduction"], "For example, bb."),
    ("What is one advantage of asexual reproduction?", "One parent can make many offspring quickly.", ["It creates lots of variation.", "It needs two parents.", "It always takes years."], "Fast and simple."),
    ("What is one advantage of sexual reproduction?", "Variation helps some offspring survive if the environment changes.", ["All offspring are identical.", "Only one parent is needed.", "It is always faster."], "Variation is useful."),
])
B5 = bank([
    ("Ava's banana plants are all clones grown from cuttings. A new disease appears. Why is this risky?", "They are genetically identical, so if one is vulnerable, all are.", ["Clones are always stronger.", "Diseases cannot affect plants.", "The bananas will vary."],
     "No variation means no resistant plants."),
    ("Leo's two black guinea pigs have a white baby. What must be true?", "Both parents carry a hidden recessive white allele (Bb).", ["The baby is not theirs.", "Black is recessive.", "White babies come from mutations only."],
     "Bb × Bb can give bb."),
    ("Mia models sexual reproduction by picking one card from each of two parents' decks. What do the cards represent?", "alleles", ["proteins", "cells", "food"], "Each parent gives one allele."),
    ("Why do siblings (not identical twins) look different from each other?", "Each got a different combination of their parents' alleles.", ["They have different parents.", "They have no genes.", "Only the oldest gets genes."],
     "Random combinations."),
    ("Some aphids reproduce asexually in summer and sexually in fall. What is a likely benefit?", "Fast growth in good times and variation before harsh conditions.", ["They avoid all mutations.", "They never change.", "It makes them slower."],
     "Both strategies have advantages."),
])


def body():
    think = ("<p><b>Asexual reproduction</b> has <b>one parent</b>. The offspring get a copy of the parent's DNA, so they are <b>genetically identical</b> (bacteria splitting, budding, runners, cuttings).</p>"
             "<p><b>Sexual reproduction</b> has <b>two parents</b>. Each parent gives <b>half</b> of the chromosomes, one allele for each gene, so offspring have <b>genetic variation</b>.</p>"
             "<p>A <b>Punnett square</b> shows the possible allele combinations. A dominant allele (B) shows its trait with one copy; a recessive trait (bb) shows only with two copies. Each box is 25%.</p>")
    tab, _ = square(["B", "b"], ["B", "b"])
    ex = [("Bb × Bb: chance of bb?", [tab, "1 of 4 boxes is bb."], "25%"),
          ("A hydra buds. Offspring's DNA?", ["One parent."], "identical to the parent")]
    mist = ["Thinking sexual offspring get all their genes from one parent.",
            "Thinking a recessive trait can never appear in offspring of two dominant-looking parents.",
            "Reading Bb × Bb as 50% recessive. It is 25%."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("One parent or two", B1 + [(g_kind, 12)]),
        ("Genetic information", [(g_kind, 8), (g_geno, 12)]),
        ("Punnett squares", [(g_punnett, 16), (g_geno, 4)]),
        ("Predicting offspring", [(g_punnett, 14), (g_geno, 6)]),
        ("Modeling variation", B5 + [g_punnett, g_kind, g_geno]),
    ])
    make("grade-8", "asexual-and-sexual-reproduction", 13, "MS-LS3-2",
         "Develop and use a model to describe why asexual reproduction results in offspring with identical genetic information and sexual reproduction results in offspring with genetic variation.",
         "Asexual and Sexual Reproduction",
         "Grade 8 Asexual and Sexual Reproduction Worksheets: Alleles, Punnett Squares and Variation",
         "Asexual and Sexual Reproduction",
         "Free middle school science worksheets on asexual and sexual reproduction (NGSS MS-LS3-2): identical vs. varied offspring, alleles, dominant and recessive traits, and Punnett square probabilities. 100 practice questions with answers.",
         "One parent copies; two parents mix.",
         "Asexual offspring are genetically identical. Sexual offspring get half their alleles from each parent, which creates variation.",
         body(),
         [("Why are asexual offspring identical to their parent?", "They get a copy of all of one parent's genetic information."),
          ("Why does sexual reproduction create variation?", "Each parent passes on half of its chromosomes, and different offspring get different combinations of alleles."),
          ("How do you use a Punnett square?", "Write one parent's alleles across the top and the other's down the side, fill in each box, and count: each box is a 25% chance.")],
         sets)


if __name__ == "__main__":
    main()
