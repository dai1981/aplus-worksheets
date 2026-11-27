# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U01: the roles of mitosis and meiosis, chromosomes, DNA and genes in
heredity, dominant and recessive alleles, genotypes and phenotypes, Punnett squares and pedigrees, and mutations.
  python tools/gen_au_science_y10_genetics_and_inheritance.py
Reuses the US Biology meiosis, DNA, Punnett square makers, the US Grade 8 genes and mutations makers and the UK Year 9 and
Year 11 inheritance makers with Australian names, plus own questions on cell division and Australian examples.
Wrong answers come from real mistakes: mixing up mitosis and meiosis, thinking dominant means common, and thinking a 3:1
ratio means exactly 3 of every 4 offspring.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

ME = "gen_us_science_bio_meiosis_and_genetic_variation"
DN = "gen_us_science_bio_dna_and_protein_synthesis"
PU = "gen_us_science_bio_punnett_squares_and_heredity"
GM = "gen_us_science_g8_genes_and_mutations"
I9 = "gen_uk_science_y9_inheritance_and_dna"
G11 = "gen_uk_science_y11_genetics_and_evolution"
ADV = ["tRNA", "mRNA", "translation", "ribosome", "anaphase", "metaphase", "prophase", "telophase", "dihybrid", "9 : 3", "polymerase", "codon", "amino acid"]
m_num = limit(src(ME, "g_num", drop=ADV), 6)
m_cmp = src(ME, "g_cmp", drop=ADV)
m_stage = src(ME, "g_stage", drop=ADV)
m_src = src(ME, "g_src", drop=ADV)
m_b1 = src.B(ME, "B1", drop=ADV)
d_comp = limit(src(DN, "g_comp", drop=ADV), 4)
d_b1 = src.B(DN, "B1", drop=ADV)
p_mono = limit(src(PU, "g_mono", drop=ADV), 6)
p_ratio = limit(src(PU, "g_ratio", drop=ADV), 5)
p_expect = limit(src(PU, "g_expect", drop=ADV, rep=[(r"About how many are with ", "About how many have ")]), 8)
p_b1 = src.B(PU, "B1", drop=ADV)
p_b5 = src.B(PU, "B5", drop=ADV)
g_type = limit(src(GM, "g_type", drop=ADV), 7)
g_eff = limit(src(GM, "g_eff", drop=ADV), 7)
i_term = src(I9, "g_term", drop=ADV)
i_chr = src(I9, "g_chr", drop=ADV)
i_b5 = src.B(I9, "B5", drop=ADV)
k_b1 = src.B(G11, "B1", drop=ADV)

POOL1 = pool(R, [
    ("What is a gene?", "a section of DNA that codes for a protein (a trait)", ["a whole chromosome", "a type of cell", "the nucleus"], "Genes are carried on chromosomes."),
    ("Where is DNA found in a human cell?", "in the chromosomes in the nucleus", ["in the cell membrane", "in the cytoplasm only", "in the cell wall"], "Humans have 46 chromosomes in 23 pairs."),
    ("What does mitosis produce?", "two identical body cells with the full number of chromosomes", ["four gametes with half the chromosomes", "one gamete", "cells with no DNA"], "Mitosis is for growth and repair."),
    ("What does meiosis produce?", "four gametes, each with half the number of chromosomes", ["two identical body cells", "one large cell", "cells with double the chromosomes"], "Meiosis makes sex cells."),
    ("Why is meiosis needed for sexual reproduction?", "Gametes have half the chromosomes, so the fertilised egg has the full number.", ["It makes identical clones.", "It repairs skin.", "It doubles the chromosomes."], "23 + 23 = 46."),
    ("What is an allele?", "a different version of a gene", ["a whole chromosome", "a type of protein only", "a gamete"], "For example, an allele for brown or blue eyes."),
    ("What is a genotype?", "the alleles an organism has, such as Bb", ["what the organism looks like", "the number of chromosomes", "a mutation"], "The phenotype is the observed trait."),
    ("What does 'heterozygous' mean?", "having two different alleles, such as Tt", ["having two identical alleles", "having no alleles", "having three alleles"], "Homozygous is TT or tt."),
    ("A dominant allele is shown by a capital letter. What does dominant mean?", "It shows its trait even when only one copy is present.", ["It is the most common allele.", "It is always good.", "It needs two copies to show."], "A recessive trait needs two copies."),
    ("Which base pairs with adenine (A) in DNA?", "thymine (T)", ["guanine (G)", "cytosine (C)", "uracil (U)"], "C pairs with G."),
    ("What is a mutation?", "a change in the DNA sequence", ["a type of cell division", "a dominant allele", "a normal protein"], "Mutations can be harmful, helpful or have no effect."),
    ("Why do identical twins have the same genes?", "They come from one fertilised egg that split in two.", ["They come from two eggs.", "They had the same diet.", "They grew up together."], "Non-identical twins come from two eggs."),
])
POOL5 = pool(R, [
    ("Mia crosses two pea plants that are both Tt (T = tall). Out of 400 offspring, about how many would be short?", "about 100", ["about 300", "about 200", "none"], "tt is 1/4 of the offspring."),
    ("Jack counts 312 tall and 98 short plants from a Tt × Tt cross. Why is this not exactly 3:1?", "Fertilisation is random, so results only come close to the expected ratio.", ["The Punnett square is wrong.", "There was a mutation in every plant.", "Short is dominant."], "Bigger samples get closer to 3:1."),
    ("Ruby flips two coins to model a Bb × Bb cross 100 times. What does each coin stand for?", "the allele each parent passes on", ["a whole chromosome", "the offspring", "the environment"], "Heads = B, tails = b."),
    ("Kai uses a pedigree chart. Two parents without a condition have a child with it. What does this suggest?", "The condition is recessive and both parents are carriers.", ["The condition is dominant.", "The child has no genes.", "The parents are homozygous dominant."], "Each parent passed on a recessive allele."),
    ("Ella extracts DNA from strawberries using detergent, salt and cold ethanol. Why is detergent used?", "to break open the cell and nuclear membranes", ["to colour the DNA", "to make the DNA longer", "to kill the strawberries"], "The DNA then clumps in the ethanol."),
    ("A test cross is done to find whether a black guinea pig is BB or Bb. It is crossed with a white bb guinea pig. Some offspring are white. What is the black parent?", "Bb (heterozygous)", ["BB (homozygous dominant)", "bb (homozygous recessive)", "it cannot be known"], "Only a Bb parent can pass on b."),
    ("Noah models chromosomes with coloured pipe cleaners. In meiosis, how many 'chromosomes' should each gamete get from a cell with 4?", "2", ["4", "8", "1"], "Gametes have half the number."),
    ("Zara reads that CSIRO scientists bred cotton plants resistant to insects. Which tool did they use?", "genetic modification of the plants' DNA", ["mitosis only", "random mutations in seeds bought from shops", "changing the soil"], "Bt cotton is grown widely in Australia."),
])


def main():
    sets = U.sets([
        ("DNA, genes and chromosomes", [(POOL1, 6), (i_term, 5), (i_chr, 4), (d_comp, 3), (d_b1, 2)]),
        ("Mitosis and meiosis", [(m_cmp, 6), (m_num, 5), (m_stage, 4), (m_src, 3), (m_b1, 2)]),
        ("Alleles, genotypes and phenotypes", [(p_mono, 6), (POOL1, 4), (p_b1, 4), (k_b1, 3), (g_type, 3)]),
        ("Punnett squares and ratios", [(p_ratio, 5), (p_expect, 4), (p_mono, 3), (POOL5, 3), (g_eff, 3), (POOL1, 2)]),
        ("Investigations", [(POOL5, 5), (p_b5, 5), (i_b5, 4), (g_eff, 1), (g_type, 1), (p_expect, 2), (m_src, 2)]),
    ])
    make_au(YEAR, "genetics-and-inheritance", SORT, "AC9S10U01", "Biological sciences",
            "Explain the role of meiosis and mitosis and the function of chromosomes, DNA and genes in heredity and predict patterns "
            "of inheritance (summary of the Australian Curriculum v9.0 Science content description).",
            "Genetics and Inheritance", "Genetics",
            "Free Year 10 science worksheets on genetics: DNA, genes and chromosomes, mitosis and meiosis, alleles, genotypes and "
            "phenotypes, Punnett squares, ratios and pedigrees. 100 questions with answers.",
            "Two alleles, one from each parent.", "Meiosis halves the chromosomes; fertilisation joins one allele from each parent.",
            "<p><b>Genes are sections of DNA on chromosomes; we get one set from each parent.</b></p><ul>"
            "<li>Mitosis makes two identical body cells (growth, repair). Meiosis makes four gametes with half the chromosomes.</li>"
            "<li>Each gene has alleles. Dominant (B) shows with one copy; recessive (b) shows only as bb.</li>"
            "<li>A Punnett square predicts the chance of each genotype: Bb × Bb gives 1 BB : 2 Bb : 1 bb (3 : 1 phenotypes).</li></ul>",
            [("Bb × Bb. Chance of bb?", ["Punnett square: BB, Bb, Bb, bb"], "1 in 4 (25%)"),
             ("A cell has 46 chromosomes. A gamete has?", ["meiosis halves the number"], "23")],
            ["Mixing up mitosis (identical body cells) and meiosis (gametes).", "Thinking a dominant allele is the most common one.",
             "Thinking a 3 : 1 ratio means exactly 3 of every 4 offspring."],
            [("What is the difference between genotype and phenotype?", "The genotype is the alleles an organism has, such as Bb. The phenotype is the trait you can see, such as brown fur."),
             ("Why are Punnett square results only probabilities?", "Which sperm fertilises which egg is random, so the real numbers of offspring only come close to the predicted ratio, especially in large samples."),
             ("What is the difference between mitosis and meiosis?", "Mitosis makes two identical cells with the full set of chromosomes. Meiosis makes four different gametes with half the chromosomes.")],
            sets)


if __name__ == "__main__":
    main()
