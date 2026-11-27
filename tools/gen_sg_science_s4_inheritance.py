# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 14: Inheritance
  python tools/gen_sg_science_s4_inheritance.py
Genes, alleles, genotype and phenotype, dominant and recessive, homozygous and heterozygous; monohybrid crosses and genetic diagrams
(3 : 1 and 1 : 1 ratios), test crosses; codominance and multiple alleles (ABO blood groups); sex determination; continuous and
discontinuous variation; mutation (sickle-cell anaemia, Down syndrome); natural and artificial selection.
US NGSS Punnett and heredity makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "the dominant allele is the more common one", "a 3 : 1 ratio means exactly 3 of every 4
offspring", "the father decides the sex because he is stronger", "height is discontinuous variation", "Tt is homozygous".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 20
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

ABO = [(r"\bAn and B\b", "A and B")]
us_mono = src("gen_us_science_bio_punnett_squares_and_heredity", "g_mono")
us_ratio = src("gen_us_science_bio_punnett_squares_and_heredity", "g_ratio", rep=[(r"\b1 (\w+) flowers\b", r"1 \1-flowered"), (r"\b(\d) (\w+) (fur|seeds|stems)\b", r"\1 with \2 \3")])
us_blood = src("gen_us_science_bio_punnett_squares_and_heredity", "g_blood", rep=ABO)

TERM = [("an allele", "one of two or more forms of a gene"), ("the genotype", "the alleles an organism has, such as Tt"),
        ("the phenotype", "the observable features of an organism, such as tall"), ("a dominant allele", "an allele that is expressed whenever it is present"),
        ("a recessive allele", "an allele that is expressed only when no dominant allele is present"), ("homozygous", "having two identical alleles of a gene, such as TT or tt"),
        ("heterozygous", "having two different alleles of a gene, such as Tt"), ("codominance", "both alleles are expressed in the heterozygote"),
        ("a test cross", "crossing an organism of dominant phenotype with a homozygous recessive to find its genotype")]
g_term = rows(R, TERM, "What is meant by %s?", "Which term means %s?")

GT = [("TT", "homozygous dominant"), ("Tt", "heterozygous"), ("tt", "homozygous recessive"), ("AA", "homozygous dominant"), ("Aa", "heterozygous"),
      ("aa", "homozygous recessive"), ("Rr", "heterozygous"), ("rr", "homozygous recessive"), ("BB", "homozygous dominant")]


def g_gt():
    g, a = R.choice(GT)
    return tq("Which word describes the genotype %s?" % g, a, [x for x in ("homozygous dominant", "heterozygous", "homozygous recessive", "codominant") if x != a],
              "Two identical alleles: homozygous. Two different alleles: heterozygous.")


def gl(g):
    return g + (" (homozygous dominant)" if g[0].isupper() and g[1].isupper() else " (heterozygous)" if g[0].isupper() else " (homozygous recessive)") if g[1] != "Y" else g + " (not possible for this gene)"


def g_test():
    k = R.random() < 0.5
    trait = R.choice([("black fur", "B", "b", "white fur", "mouse"), ("tall stems", "T", "t", "short stems", "pea plant"), ("purple flowers", "P", "p", "white flowers", "pea plant"),
                      ("round seeds", "R", "r", "wrinkled seeds", "pea plant")])
    dom, D, d, rec, org = trait
    if k:
        return tq("A %s with %s is crossed with one with %s. All offspring have %s. What is the genotype of the %s parent?" % (org, dom, rec, dom, dom), gl(D + D),
                  [gl(D + d), gl(d + d), "it cannot be worked out from this cross"], "If it were %s%s, about half the offspring would have %s." % (D, d, rec))
    return tq("A %s with %s is crossed with one with %s. About half of the offspring have %s. What is the genotype of the %s parent?" % (org, dom, rec, rec, dom), gl(D + d),
              [gl(D + D), gl(d + d), "it cannot be worked out from this cross"], "A %s%s × %s%s cross gives a 1 : 1 ratio." % (D, d, d, d))


def g_sex():
    k = R.choice(["boy", "girl", "egg", "sperm", "chance"])
    d = {"boy": ("Which sex chromosomes does a boy have?", "XY", ["XX", "YY", "XO"], "Females are XX; males are XY."),
         "girl": ("Which sex chromosomes does a girl have?", "XX", ["XY", "YY", "YO"], "Females are XX; males are XY."),
         "egg": ("Which sex chromosome does every human egg contain?", "X", ["Y", "either X or Y", "no sex chromosome"], "The mother is XX, so all eggs have an X."),
         "sperm": ("Which sex chromosomes can human sperm contain?", "either X or Y (half each)", ["only X", "only Y", "both X and Y"], "The father is XY."),
         "chance": ("What is the chance that a couple's next baby will be a boy?", "50%", ["25%", "75%", "100% if the first three were girls"], "Each fertilisation is independent: half the sperm carry Y.")}[k]
    return tq(*d)


VAR = [("height of students in a class", "continuous variation"), ("body mass", "continuous variation"), ("hand span", "continuous variation"),
       ("leaf length on a tree", "continuous variation"), ("ABO blood group", "discontinuous variation"), ("the ability to roll the tongue", "discontinuous variation"),
       ("whether ear lobes are attached or free", "discontinuous variation"), ("sex (male or female)", "discontinuous variation")]


def g_var():
    x, a = R.choice(VAR)
    return tq("Which type of variation is shown by %s?" % x, a, [y for y in ("continuous variation", "discontinuous variation", "no variation", "only environmental variation") if y != a],
              "Continuous variation has a range of values and is usually controlled by many genes and the environment; discontinuous variation has distinct groups.")


def g_cross():
    D, d, dom, rec, org = R.choice([("H", "h", "normal", "sickle-cell", "a couple"), ("T", "t", "tall", "short", "two pea plants"), ("B", "b", "brown eyes", "blue eyes", "a couple"),
                                    ("F", "f", "free ear lobes", "attached ear lobes", "a couple")])
    p1, p2 = R.choice([(D + d, D + d), (D + d, d + d), (D + D, D + d), (D + D, d + d)])
    kids = [a + b for a in p1 for b in p2]
    rec_n = sum(1 for k in kids if k == d + d)
    a = "%d%%" % (rec_n * 25)
    q = ("Two pea plants with the genotypes %s and %s are crossed. What is the chance that an offspring has the %s phenotype?" % (p1, p2, rec) if "plants" in org
         else "A couple have the genotypes %s and %s. What is the chance that a child has the %s phenotype?" % (p1, p2, rec))
    return tq(q, a,
              [x for x in ("0%", "25%", "50%", "75%", "100%") if x != a][:3] if a != "0%" else ["25%", "50%", "75%"],
              "Gametes: %s and %s; offspring: %s. %d out of 4 are %s%s." % (" or ".join(sorted(set(p1))), " or ".join(sorted(set(p2))), ", ".join(kids), rec_n, d, d))


POOL1 = pool(R, [
    ("What is a gene?", "a length of DNA that controls a characteristic by coding for a protein", ["a whole chromosome", "a type of cell", "a pair of alleles only"], "Genes are found at fixed positions (loci) on chromosomes."),
    ("Why is a recessive feature sometimes seen in a child when neither parent shows it?", "Both parents are heterozygous carriers and each passed on the recessive allele.", ["The child has a mutation in every cell.", "Recessive alleles are always expressed.", "Only the father's alleles matter."], "Tt × Tt gives 1 in 4 tt."),
    ("Why is the observed ratio of offspring often not exactly 3 : 1?", "Fertilisation is random, so small numbers of offspring do not match the expected ratio exactly.", ["The alleles changed.", "The parents were not real.", "Dominant alleles are rarer."], "Larger samples get closer to the ratio."),
    ("In the ABO blood groups, which alleles are codominant?", "Iᴬ and Iᴮ", ["Iᴬ and i", "Iᴮ and i", "all three"], "i is recessive to both."),
    ("Which genotype gives blood group O?", "ii", ["IᴬIᴮ", "Iᴬi", "Iᴮi"], "Only two recessive alleles give group O."),
    ("Which genotype gives blood group AB?", "IᴬIᴮ", ["Iᴬi", "ii", "IᴮIᴮ"], "Both A and B antigens are made."),
    ("What is a mutation?", "a random change in a gene or chromosome", ["a change caused by learning", "a normal part of digestion", "a change in phenotype due to diet"], "Radiation and some chemicals increase the rate of mutation."),
    ("What causes Down syndrome?", "an extra copy of chromosome 21 (47 chromosomes)", ["a missing X chromosome", "a single recessive allele", "a bacterial infection"], "It results from a fault in meiosis."),
    ("What is natural selection?", "Organisms with features better suited to the environment survive and reproduce, passing on their alleles.", ["Farmers choose which animals breed.", "All organisms survive equally.", "Organisms change their genes on purpose."], "It leads to evolution."),
    ("What is artificial selection?", "humans choosing organisms with desired features to breed", ["survival of the fittest in the wild", "random mutation", "the spread of disease"], "Examples: high-yield rice, dog breeds."),
])
POOL5 = pool(R, [
    ("Sickle-cell anaemia is common where malaria is common. Why?", "Heterozygous people are more resistant to malaria, so the allele is selected for.", ["Malaria causes the mutation.", "Mosquitoes carry the allele.", "Sickle cells cure malaria."], "An example of natural selection in humans."),
    ("Bacteria become resistant to an antibiotic over many generations. Which process explains this?", "natural selection of bacteria with a resistance mutation", ["artificial selection by doctors", "bacteria learning to resist", "the antibiotic becoming weaker"], "Resistant bacteria survive and multiply."),
    ("A woman with blood group A and a man with blood group B have a child with blood group O. What are the parents' genotypes?", "Iᴬi and Iᴮi", ["IᴬIᴬ and IᴮIᴮ", "IᴬIᴮ and ii", "ii and ii"], "Both must carry i."),
    ("Two tall pea plants produce 302 tall and 98 short offspring. What were the parents' genotypes?", "both heterozygous (Tt × Tt)", ["one homozygous dominant and one homozygous recessive (TT × tt)", "one homozygous dominant and one heterozygous (TT × Tt)", "both homozygous recessive (tt × tt)"], "About 3 : 1 shows both are heterozygous."),
    ("Why do identical twins differ slightly in height and mass?", "Their environments (such as diet and exercise) differ, even though their genes are the same.", ["They have different genes.", "One has a mutation in every cell.", "Height is discontinuous."], "Phenotype = genotype + environment."),
    ("Why is a test cross done with a homozygous recessive organism?", "It gives only recessive alleles, so the offspring show which alleles the other parent carries.", ["It always gives dominant offspring.", "It makes new mutations.", "It is cheaper."], "Any recessive offspring shows the parent was heterozygous."),
    ("Which is an advantage of selective breeding of rice?", "Higher yields or resistance to disease can be produced.", ["It increases genetic variation in the crop.", "It is faster than genetic engineering for every trait.", "It makes rice photosynthesise at night."], "It reduces variation, which can be a disadvantage."),
    ("Which statement about sex determination is correct?", "The sex of a child depends on whether the sperm carries an X or a Y chromosome.", ["The mother decides the sex of a child.", "A child receives a Y chromosome from the mother.", "Boys are XX."], "Eggs always carry an X."),
])


def main():
    sets = U.sets([
        ("Genes and alleles", [(g_term, 9), (g_gt, 6), (POOL1, 5)]),
        ("Monohybrid crosses", [(us_mono, 8), (g_cross, 7), (us_ratio, 5)]),
        ("Test crosses, codominance and sex", [(g_test, 5), (us_blood, 7), (g_sex, 4), (POOL1, 3), (POOL5, 1)]),
        ("Variation and selection", [(g_var, 7), (POOL1, 2), (POOL5, 3), (g_term, 4), (us_ratio, 2), (g_gt, 2)]),
        ("Exam-style questions", [(POOL5, 4), (us_mono, 5), (g_cross, 4), (us_blood, 3), (g_test, 2), (us_ratio, 2)]),
    ])
    make_ol(LV, SUBJ, "inheritance", SORT, "Inheritance",
            "Define gene, allele, dominant, recessive, codominant, homozygous, heterozygous, genotype and phenotype; use genetic diagrams to predict the results "
            "of monohybrid crosses, including 3 : 1 and 1 : 1 ratios and test crosses; explain codominance and multiple alleles using the ABO blood groups; describe "
            "sex determination; distinguish between continuous and discontinuous variation; describe mutation, including sickle-cell anaemia and Down syndrome; "
            "describe natural and artificial selection (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Inheritance", "Inheritance",
            "Free Secondary 4 O-Level Biology worksheets on inheritance: alleles, genotype, phenotype, monohybrid crosses, test crosses, blood groups, sex "
            "determination, variation, mutation and selection. 100 questions with answers.",
            "Tt × Tt → 3 : 1; Tt × tt → 1 : 1.", "Genotype is the alleles; phenotype is what you see.",
            "<p><b>Each parent passes one allele of each gene.</b></p><ul>"
            "<li>Dominant (T) shows whenever present; recessive (t) only in tt. TT and tt are homozygous; Tt is heterozygous.</li>"
            "<li>Draw gametes, then a Punnett square. Tt × Tt: 1 TT : 2 Tt : 1 tt, a 3 : 1 phenotype ratio.</li>"
            "<li>A test cross with tt shows if a dominant-looking parent is TT (all dominant) or Tt (1 : 1).</li>"
            "<li>ABO: Iᴬ and Iᴮ are codominant, i is recessive. Sex: XX female, XY male; the sperm decides.</li></ul>",
            [("Tt × tt. Chance of tt?", ["gametes T, t and t", "Tt, Tt, tt, tt"], "50%"),
             ("Iᴬi × Iᴮi. Possible groups?", ["IᴬIᴮ, Iᴬi, Iᴮi, ii"], "AB, A, B or O")],
            ["Saying the dominant allele is the more common one.", "Reading 3 : 1 as an exact result.", "Calling Tt homozygous.", "Saying height is discontinuous variation."],
            [("What is the difference between genotype and phenotype?", "The genotype is the pair of alleles an organism has, such as Tt. The phenotype is the feature you can observe, such as being tall, which also depends on the environment."),
             ("What is codominance?", "Both alleles are expressed in a heterozygote. In the ABO blood groups, a person with Iᴬ and Iᴮ has blood group AB."),
             ("How is the sex of a baby decided?", "All eggs carry an X chromosome. Half the sperm carry an X and half a Y. An egg fertilised by an X sperm gives a girl (XX); by a Y sperm gives a boy (XY).")],
            sets)


if __name__ == "__main__":
    main()
