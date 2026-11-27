# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 12: Molecular Genetics
  python tools/gen_sg_science_s4_molecular_genetics.py
The structure of DNA (double helix of nucleotides, complementary base pairing A–T and C–G), genes and chromosomes; how a gene
codes for a protein (transcription to mRNA in the nucleus, translation at ribosomes, three bases per amino acid); genetic
engineering (restriction enzymes, plasmids, DNA ligase, transgenic bacteria making insulin, GM crops) and its benefits and concerns.
US NGSS DNA makers and UK KS3 terms are reused (Singapore names); base percentages and genetic engineering are written here.
Wrong answers come from real mistakes: "A pairs with G", "mRNA contains thymine", "each base codes for one amino acid", "a gene is a
chromosome", "plasmids are found in the nucleus of human cells".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 18
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

us_comp = src("gen_us_science_bio_dna_and_protein_synthesis", "g_comp")
us_mrna = src("gen_us_science_bio_dna_and_protein_synthesis", "g_mrna")
us_trans = src("gen_us_science_bio_dna_and_protein_synthesis", "g_trans")
us_count = src("gen_us_science_bio_dna_and_protein_synthesis", "g_count", rep=[(r"\b[Aa]n? mRNA coding region", "The mRNA coding region")])
uk_term = src("gen_uk_science_y9_inheritance_and_dna", "g_term", drop=["dominant", "recessive", "heredity"])


def g_pct():
    a = R.choice([15, 18, 20, 22, 24, 25, 26, 28, 30, 32, 35])
    g = 50 - a
    k = R.choice(["T", "G", "C"])
    ans = a if k == "T" else g
    return nq("In a sample of double-stranded DNA, %d%% of the bases are adenine (A). What percentage are %s?" % (a, {"T": "thymine (T)", "G": "guanine (G)", "C": "cytosine (C)"}[k]),
              ans, [100 - a, a if k != "T" else g, 100 - 2 * a] if k != "T" else [g, 100 - a, 2 * a], "%",
              "A pairs with T, so T = %d%%. A + T = %d%%, so G + C = %d%% and G = C = %d%%." % (a, 2 * a, 100 - 2 * a, g))


def g_pct2():
    c = R.choice([12, 15, 18, 20, 21, 24, 27, 30, 33])
    a = 50 - c
    return nq("A DNA molecule contains %d%% cytosine. What percentage of its bases are adenine?" % c, a, [c, 100 - c, 100 - 2 * c], "%",
              "C = G = %d%%, so C + G = %d%%. A + T = %d%%, so A = %d%%." % (c, 2 * c, 100 - 2 * c, a))


TERM = [("a nucleotide", "a unit of DNA made of a sugar, a phosphate group and a base"), ("a gene", "a length of DNA that codes for one polypeptide"),
        ("a chromosome", "a long, coiled DNA molecule in the nucleus carrying many genes"), ("the double helix", "the shape of DNA: two strands twisted around each other"),
        ("complementary base pairing", "A always pairs with T and C always pairs with G"), ("a codon (triplet)", "a sequence of three bases that codes for one amino acid"),
        ("transcription", "making mRNA from the DNA of a gene in the nucleus"), ("translation", "using the mRNA sequence at a ribosome to join amino acids into a polypeptide")]
g_term = rows(R, TERM, "What is %s?", "Which term means %s?")

GE = [("restriction enzymes", "cut DNA at specific base sequences, leaving sticky ends"), ("DNA ligase", "joins the human gene into the plasmid"),
      ("a plasmid", "a small ring of DNA in a bacterium, used as a vector"), ("a transgenic bacterium", "a bacterium that contains a gene from another organism"),
      ("a fermenter", "a large vessel where transgenic bacteria are grown to make products such as insulin"), ("sticky ends", "short single-stranded ends of cut DNA that pair with complementary ends")]
g_ge = rows(R, GE, "In genetic engineering, what is the role of %s?", "In genetic engineering, which term is described? “%s”")

ORD = ["Cut the human insulin gene out with a restriction enzyme.", "Cut a plasmid open with the same restriction enzyme.", "Join the gene into the plasmid with DNA ligase.",
       "Insert the recombinant plasmid into a bacterium.", "Grow the bacteria in a fermenter and extract the insulin."]


def g_ord():
    i = R.randrange(len(ORD) - 1)
    a = ORD[i + 1]
    return tq("In making human insulin by genetic engineering, which step comes straight after this: “%s”" % ORD[i], a, [x for j, x in enumerate(ORD) if j not in (i, i + 1)][:3],
              "Cut gene → cut plasmid → join with ligase → put into bacterium → grow and extract.")


PROS = [("GM crops resistant to pests", "benefit", "Less insecticide is needed."), ("Golden rice with extra vitamin A", "benefit", "It can reduce vitamin A deficiency."),
        ("Insulin made by bacteria", "benefit", "It is cheap, plentiful and identical to human insulin."),
        ("Genes for herbicide resistance spreading to wild plants", "concern", "It could create 'superweeds'."),
        ("Reduced variety of crops as farmers grow the same GM strain", "concern", "It lowers biodiversity."),
        ("Large companies owning patents on GM seeds", "concern", "Poor farmers may have to buy seed every year.")]


def g_pros():
    x, t, why = R.choice(PROS)
    return tq("Is this a benefit or a concern of genetic engineering? %s" % x, "a " + t, ["a " + ("concern" if t == "benefit" else "benefit"), "neither, it is unrelated", "a type of mutation"], why)


POOL1 = pool(R, [
    ("Where is DNA found in a human cell?", "in the chromosomes in the nucleus", ["in the ribosomes", "in the cell membrane", "in the cytoplasm only"], "A small amount is also in mitochondria."),
    ("Which base pairs with adenine in DNA?", "thymine", ["guanine", "cytosine", "uracil"], "A–T and C–G."),
    ("Which base in mRNA replaces thymine?", "uracil", ["adenine", "guanine", "cytosine"], "mRNA uses A, U, C and G."),
    ("Where does translation happen?", "at the ribosomes in the cytoplasm", ["in the nucleus", "in the mitochondria", "in the cell wall"], "mRNA leaves the nucleus through pores."),
    ("Why does the sequence of bases matter?", "It decides the order of amino acids in the protein.", ["It decides the size of the cell.", "It gives the cell energy.", "It is the same in all genes."], "Each triplet codes for one amino acid."),
    ("How many bases code for one amino acid?", "three", ["one", "two", "four"], "A triplet or codon."),
    ("Why is the genetic code described as universal?", "The same codons code for the same amino acids in almost all organisms.", ["All organisms have the same genes.", "Every cell makes the same protein.", "DNA is found only in humans."], "This is why bacteria can make human insulin."),
    ("What is genetic engineering?", "changing the genetic material of an organism by adding a gene from another organism", ["choosing parents with good features", "making clones by cuttings", "changing the diet of an animal"], "Transgenic organisms."),
    ("Why must the same restriction enzyme cut both the human DNA and the plasmid?", "So they have matching (complementary) sticky ends that can join.", ["So the plasmid dissolves.", "So the bacterium dies.", "So the DNA is copied."], "DNA ligase then seals the joins."),
    ("Why is human insulin from bacteria useful to people with diabetes?", "It is made in large amounts and is identical to human insulin, so allergic reactions are rare.", ["It cures diabetes.", "It is made from pigs.", "It is not a protein."], "Before this, insulin came from animal pancreases."),
])
POOL5 = pool(R, [
    ("A gene is 900 bases long on the coding strand. How many amino acids could it code for?", "300", ["900", "450", "2700"], "900 ÷ 3."),
    ("A change in one base of a gene can change a protein. Why?", "The triplet may code for a different amino acid, changing the protein's shape.", ["Bases are amino acids.", "The whole chromosome is lost.", "The cell stops making mRNA."], "This is a gene mutation."),
    ("Why can mRNA leave the nucleus but DNA cannot?", "mRNA is a small single strand that passes through nuclear pores; DNA is a very long molecule.", ["DNA is too short.", "mRNA is made in the cytoplasm.", "DNA is not in the nucleus."], "The DNA stays protected in the nucleus."),
    ("Which is a correct sequence?", "DNA → mRNA → protein", ["protein → mRNA → DNA", "mRNA → DNA → protein", "DNA → protein → mRNA"], "Transcription, then translation."),
    ("A DNA strand reads ATG CGT. Which is the base sequence of its complementary strand?", "TAC GCA", ["UAC GCA", "ATG CGT", "GCA TAC"], "A–T and C–G."),
    ("Why might some people object to GM foods?", "They worry about possible long-term effects on health and the environment.", ["GM foods contain no DNA.", "GM foods are always poisonous.", "GM crops cannot grow."], "Strict testing is carried out."),
    ("Every body cell contains the same genes. Why are muscle cells different from nerve cells?", "Different genes are switched on, so different proteins are made.", ["They have different DNA.", "Muscle cells have no nucleus.", "Nerve cells have no genes."], "Gene expression differs."),
    ("Which shows the parts of a DNA nucleotide?", "a sugar, a phosphate and a base", ["an amino acid and a base", "glucose and glycerol", "a protein and a fatty acid"], "The sugar in DNA is deoxyribose."),
])


def main():
    sets = U.sets([
        ("The structure of DNA", [(g_term, 6), (us_comp, 6), (g_pct, 5), (POOL1, 3)]),
        ("Base pairing", [(us_comp, 5), (g_pct, 5), (g_pct2, 5), (uk_term, 3), (POOL1, 2)]),
        ("From gene to protein", [(us_mrna, 6), (us_trans, 4), (us_count, 4), (g_term, 3), (POOL1, 3)]),
        ("Genetic engineering", [(g_ge, 9), (g_ord, 3), (g_pros, 4), (POOL1, 1), (POOL5, 2), (g_term, 1)]),
        ("Exam-style questions", [(POOL5, 6), (us_trans, 3), (us_count, 4), (g_pct2, 2), (g_ge, 2), (us_mrna, 3)]),
    ])
    make_ol(LV, SUBJ, "molecular-genetics", SORT, "Molecular Genetics",
            "Outline the structure of DNA as a double helix of nucleotides with complementary base pairing; describe a gene as a sequence of DNA that codes for a "
            "polypeptide and its location on a chromosome; state that the sequence of bases (triplets) determines the order of amino acids; outline how mRNA is made "
            "in the nucleus and used at ribosomes to make a protein; describe genetic engineering using restriction enzymes, plasmids and DNA ligase, for example to "
            "make human insulin, and discuss its benefits and concerns (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Molecular Genetics", "Molecular genetics",
            "Free Secondary 4 O-Level Biology worksheets on molecular genetics: DNA structure, base pairing, genes, mRNA, protein synthesis and genetic engineering. "
            "100 questions with answers.",
            "A–T and C–G. Three bases code for one amino acid.", "DNA → mRNA (nucleus) → protein (ribosome).",
            "<p><b>DNA is a code for proteins.</b></p><ul>"
            "<li>DNA: two strands of nucleotides in a double helix. A pairs with T, C pairs with G, so %A = %T and %C = %G.</li>"
            "<li>A gene is a length of DNA coding for a polypeptide. Each triplet of bases codes for one amino acid.</li>"
            "<li>Transcription makes mRNA (with U instead of T) in the nucleus; translation at ribosomes joins amino acids.</li>"
            "<li>Genetic engineering: restriction enzyme cuts the gene and plasmid, ligase joins them, bacteria make the protein (insulin).</li></ul>",
            [("DNA has 30% A. %G?", ["T = 30%", "G + C = 40%"], "20%"),
             ("Protein of 120 amino acids. Bases?", ["120 × 3"], "360")],
            ["Pairing A with G.", "Putting thymine in mRNA.", "Saying one base codes for one amino acid.", "Mixing up genes and chromosomes."],
            [("How do you work out base percentages in DNA?", "A = T and C = G. If A is 30%, then T is 30%, so C + G = 40% and C = G = 20%."),
             ("How does a gene control the making of a protein?", "The base sequence of the gene is copied into mRNA in the nucleus. The mRNA goes to a ribosome, where each triplet codes for one amino acid in the polypeptide."),
             ("How is human insulin made by bacteria?", "The insulin gene is cut out with a restriction enzyme and joined into a plasmid with DNA ligase. The plasmid is put into bacteria, which are grown in a fermenter and make insulin.")],
            sets)


if __name__ == "__main__":
    main()
