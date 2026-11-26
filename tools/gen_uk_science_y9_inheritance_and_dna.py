# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Biology): Inheritance and DNA
  python tools/gen_uk_science_y9_inheritance_and_dna.py
Heredity as the process by which genetic information is passed from one generation to the next; DNA, chromosomes,
genes and alleles; the double helix and the work of Watson, Crick, Franklin and Wilkins; base pairing; dominant and
recessive alleles and simple Punnett squares; mutations. Reuses the Punnett-square and base-pairing questions of the
US Biology unit and the mutation questions of the US Grade 8 unit in British English.
Wrong answers come from real mistakes: "a gene is bigger than a chromosome", "you get all your genes from your
mother", "a recessive trait can never appear", "the double helix was found by one person".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us

U = Unit(61901)
R = U.R
P = People(R)
uk_sci.USED.clear()
PS = adopt_us("gen_us_science_bio_punnett_squares_and_heredity", U)
DN = adopt_us("gen_us_science_bio_dna_and_protein_synthesis", U)
GM = adopt_us("gen_us_science_g8_genes_and_mutations", U)
us_mono, us_ratio, us_exp = ukm(PS.g_mono), ukm(PS.g_ratio), ukm(PS.g_expect)
us_comp = ukm(DN.g_comp)
us_chain, us_eff = ukm(GM.g_chain), ukm(GM.g_eff)

SIZE = ["a base", "a gene", "a chromosome", "the nucleus", "a cell"]


def g_size():
    a, b = sorted(R.sample(range(len(SIZE)), 2))
    k = R.random() < 0.5
    if not once(("sz", a, b, k)):
        return None
    if k:
        return item("Which is larger: %s or %s?" % (SIZE[b], SIZE[a]) if R.random() < 0.5 else "Which is larger: %s or %s?" % (SIZE[a], SIZE[b]), SIZE[b],
                    [SIZE[a], "They are the same size.", "It depends on the person."], "Cell > nucleus > chromosome > gene > base.")
    return item("Which list goes from smallest to largest?", "base, gene, chromosome, nucleus, cell", ["gene, base, chromosome, cell, nucleus", "chromosome, gene, base, nucleus, cell", "cell, nucleus, chromosome, gene, base"], "A gene is a section of a chromosome.") if once(("szl",)) else None


TERM = [("DNA", "the molecule that carries genetic information, shaped like a double helix"), ("a chromosome", "a long, coiled strand of DNA in the nucleus"),
        ("a gene", "a section of DNA that codes for a characteristic"), ("an allele", "a different version of the same gene"),
        ("a dominant allele", "an allele that shows its effect even if only one copy is present"), ("a recessive allele", "an allele that shows its effect only if two copies are present"),
        ("heredity", "the passing of genetic information from parents to offspring"), ("a mutation", "a change in the DNA")]


def g_term():
    t, d = R.choice(TERM)
    k = R.random() < 0.5
    if not once(("te", t, k)):
        return None
    if k:
        return item("What is %s?" % t, d[0].upper() + d[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample([x for x in TERM if x[0] != t], 3)], "Key words of inheritance.")
    return item("Which word means %s?" % d, t, R.sample([x[0] for x in TERM if x[0] != t], 3), "Key words of inheritance.")


CHR = [("How many chromosomes are in a normal human body cell?", "46 (23 pairs)", ["23", "92", "12"]),
       ("How many chromosomes are in a human egg or sperm cell?", "23", ["46", "92", "2"]),
       ("Why do sex cells have half the number of chromosomes?", "so the fertilised egg has the full number, half from each parent", ["so they can swim faster", "because they are smaller", "so they never divide"]),
       ("Where are chromosomes found in a cell?", "in the nucleus", ["in the cell wall", "in the cytoplasm only", "in the vacuole"]),
       ("Which pair of sex chromosomes does a typical female have?", "XX", ["XY", "YY", "X only"]),
       ("Which pair of sex chromosomes does a typical male have?", "XY", ["XX", "YY", "Y only"]),
       ("What is the chance that a baby will be a boy?", "50%", ["25%", "75%", "100%"]),
       ("From whom do you inherit your chromosomes?", "half from your mother and half from your father", ["all from your mother", "all from your father", "from your grandparents only"])]


def g_chr():
    q, a, w = R.choice(CHR)
    if not once(("ch", q)):
        return None
    return item(q, a, w, "Each parent gives one chromosome of each pair.")


B1 = bank([
    ("Who used X-ray images to help show that DNA is a double helix?", "Rosalind Franklin (with Maurice Wilkins)", ["Charles Darwin", "Isaac Newton", "Marie Curie"], "Photo 51."),
    ("Who built the first model of the DNA double helix in 1953?", "James Watson and Francis Crick", ["Gregor Mendel", "Louis Pasteur", "Alexander Fleming"], "Using Franklin's data."),
    ("Which bases pair together in DNA?", "A with T, and C with G", ["A with C, and T with G", "A with G, and C with T", "each base with itself"], "Complementary pairs."),
    ("What did Gregor Mendel study to discover the rules of inheritance?", "pea plants", ["fruit flies", "finches", "bacteria"], "He bred them for many years."),
])
B5 = bank([
    ("Two brown-eyed parents have a blue-eyed child. How is this possible?", "Both parents carry a recessive blue allele.", ["Blue is dominant.", "The child made a new gene.", "It is impossible."], "Carriers."),
    ("Why do identical twins look so alike?", "They have the same DNA, because they came from one fertilised egg.", ["They eat the same food.", "They share a bedroom.", "They have half the same DNA."], "Same genes."),
    ("Why might identical twins have slightly different features?", "The environment also affects characteristics.", ["Their DNA changes completely.", "One has more chromosomes.", "They are not related."], "Genes and environment."),
    ("What can cause mutations?", "radiation such as X-rays and UV light, and some chemicals", ["eating fruit", "sleeping", "drinking water"], "Mutagens."),
])


def body():
    think = ("<p><b>DNA carries the instructions passed from parents to offspring.</b></p>"
             "<ul><li>DNA is coiled into chromosomes in the nucleus; a gene is a section of DNA; alleles are versions of a gene.</li>"
             "<li>Body cells have 46 chromosomes in 23 pairs: one of each pair from each parent.</li>"
             "<li>A dominant allele shows with one copy; a recessive allele needs two. Punnett squares predict the chances.</li></ul>")
    ex = [("Bb × bb: chance of bb?", ["Bb, Bb, bb, bb"], "50%"),
          ("Gene or chromosome: which is bigger?", ["A gene is part of a chromosome"], "chromosome")]
    mist = ["Thinking a gene is bigger than a chromosome.", "Thinking a recessive trait can never appear.", "Thinking all your genes come from one parent."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("DNA, genes and chromosomes", B1 + [(g_size, 4), (g_term, 8), (us_comp, 4)]),
        ("Chromosomes", [(g_chr, 7), (g_term, 6), (g_size, 3), (us_comp, 4)]),
        ("Dominant and recessive", [(us_mono, 12), (us_ratio, 8)]),
        ("Predicting offspring", [(us_exp, 10), (us_mono, 5), (us_ratio, 5)]),
        ("Mutations", B5 + [(us_chain, 6), (us_eff, 6), (us_exp, 4)]),
    ])
    make_ks3(9, "inheritance-and-dna", 1, "Biology", "Genetics and evolution",
             "Heredity as the process by which genetic information is transmitted from one generation to the next; a simple model of chromosomes, genes and DNA in heredity, including the part played by Watson, Crick, Wilkins and Franklin in the development of the DNA model.",
             "Inheritance and DNA",
             "Year 9 Science: Inheritance and DNA Worksheets (Genes, Chromosomes, Punnett Squares)",
             "Inheritance and DNA",
             "Free Year 9 science worksheets on inheritance and DNA: chromosomes, genes and alleles, the double helix, dominant and recessive alleles, Punnett squares and mutations. 100 questions with answers.",
             "Genes on chromosomes pass from parents to children.",
             "46 chromosomes in 23 pairs; dominant alleles show with one copy.",
             body(),
             [("What is the difference between DNA, a gene and a chromosome?", "DNA is the molecule of genetic information. A chromosome is a long coiled strand of DNA. A gene is a short section of a chromosome that codes for one characteristic."),
              ("Who discovered the structure of DNA?", "James Watson and Francis Crick built the double helix model in 1953, using X-ray images made by Rosalind Franklin and Maurice Wilkins."),
              ("How does a Punnett square work?", "Write one parent's alleles along the top and the other's down the side, then fill each box with one allele from each. The boxes show the chances for the offspring.")],
             sets)


if __name__ == "__main__":
    main()
