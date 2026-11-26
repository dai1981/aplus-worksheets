# -*- coding: utf-8 -*-
"""
US High School Biology: DNA and Protein Synthesis (HS-LS1-1)
  python tools/gen_us_science_bio_dna_and_protein_synthesis.py
Construct an explanation based on evidence for how the structure of DNA determines the structure of proteins which
carry out the essential functions of life through systems of specialized cells.
Base pairing, transcription (DNA -> mRNA), codons and translation with a codon table, counting codons, and how
mutations change a protein.
Wrong answers come from real mistakes: "A pairs with U in DNA", "keeping T in mRNA", "reading one base as one amino acid",
"translation happens in the nucleus".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(90101)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


DNA_PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}
RNA_PAIR = {"A": "U", "T": "A", "G": "C", "C": "G"}
CODON = {"AUG": "Met (start)", "UUU": "Phe", "GGC": "Gly", "GCU": "Ala", "UGG": "Trp", "CAU": "His", "AAA": "Lys", "GAA": "Glu", "UCU": "Ser", "UAA": "Stop"}
SHORT = {k: v.split(" ")[0] for k, v in CODON.items()}


def sp(s):
    return "<b>%s</b>" % " ".join(s[i:i + 3] for i in range(0, len(s), 3))


def rand_dna(n):
    return "".join(R.choice("ATGC") for _ in range(n))


def g_comp():
    s = rand_dna(R.choice([6, 9]))
    if not once(s):
        return None
    a = "".join(DNA_PAIR[c] for c in s)
    w1 = "".join(RNA_PAIR[c] for c in s)                 # used U
    w2 = s[::-1]                                         # just reversed
    w3 = "".join({"A": "C", "C": "A", "G": "T", "T": "G"}[c] for c in s)   # wrong pairing rule
    if len({a, w1, w2, w3}) < 4:
        return None
    return item("A DNA strand reads %s. What is the complementary DNA strand?" % sp(s), sp(a), [sp(w1), sp(w2), sp(w3)], "In DNA, A pairs with T and G pairs with C.")


def g_mrna():
    s = rand_dna(R.choice([6, 9]))
    if "T" not in s and "A" not in s or not once(("m", s)):
        return None
    a = "".join(RNA_PAIR[c] for c in s)
    w1 = "".join(DNA_PAIR[c] for c in s)                 # kept T
    w2 = s.replace("T", "U")                             # copied instead of paired
    w3 = "".join({"A": "T", "T": "U", "G": "C", "C": "G"}[c] for c in s)
    if len({a, w1, w2, w3}) < 4:
        return None
    return item("A DNA template strand reads %s. What mRNA is made by transcription?" % sp(s), sp(a), [sp(w1), sp(w2), sp(w3)],
                "RNA uses U instead of T: A pairs with U, T with A, G with C, C with G.")


CT = table(["Codon", "Amino acid"], [[k, v] for k, v in CODON.items()])


def g_trans():
    cods = ["AUG"] + R.sample([k for k in CODON if k not in ("AUG", "UAA")], 2)
    stop = R.random() < 0.3
    if stop:
        cods = cods + ["UAA"]
    m = "".join(cods)
    if not once(m):
        return None
    aa = [SHORT[c] for c in cods if c != "UAA"]
    a = "–".join(aa)
    w = ["–".join(reversed(aa)), "–".join(aa[:1] + [SHORT[R.choice([k for k in CODON if k not in cods and k != "UAA"])]] + aa[2:]), "–".join(aa) + "–Stop"]
    if len({a} | set(w)) < 4:
        return None
    return item(CT + "Use the codon table. What amino acids does the mRNA %s code for?" % sp(m), a, w, "Read three bases at a time: %s." % ", ".join("%s = %s" % (c, SHORT[c]) for c in cods))


def g_count():
    n = R.choice([30, 45, 60, 90, 120, 150, 210, 300, 450, 600])
    k = R.choice(["codon", "base"])
    if not once((n, k)):
        return None
    if k == "codon":
        return item("An mRNA coding region has %d bases (including the stop codon). How many codons is that?" % n, str(n // 3), [str(n), str(n * 3), str(n // 2)],
                    "Each codon is 3 bases: %d ÷ 3 = %d." % (n, n // 3))
    aa = n // 3
    return item("A protein has %d amino acids. How many mRNA bases code for them (not counting the stop codon)?" % aa, str(aa * 3), [str(aa), str(aa * 2), str(aa + 3)],
                "3 bases per amino acid: %d × 3 = %d." % (aa, aa * 3))


NEIGH = [(x, y) for x in CODON for y in CODON if x != y and sum(p != q for p, q in zip(x, y)) == 1]


def g_sub():
    x, y = R.choice(NEIGH)
    if "AUG" in (x, y):
        return None
    other = R.choice([k for k in CODON if k not in ("AUG", "UAA", x, y)])
    pos = R.randrange(2)
    before = ["AUG"] + ([x, other] if pos == 0 else [other, x])
    after = ["AUG"] + ([y, other] if pos == 0 else [other, y])
    if not once((tuple(before), tuple(after))):
        return None
    if y == "UAA":
        a = "The protein stops early after %s." % "–".join(SHORT[c] for c in after[:after.index("UAA")])
    else:
        a = "One amino acid changes: %s becomes %s." % (SHORT[x], SHORT[y])
    w = ["Every amino acid after the change is different.", "The protein is unchanged.", "The protein gets one amino acid longer."]
    return item(CT + "One base changes: %s becomes %s. What happens to the protein?" % (sp("".join(before)), sp("".join(after))), a, w,
                "A substitution changes only one codon: %s → %s." % (x, y))


def g_mut():
    k = R.choice(["ins", "del", "silent", "nonsense", "frame"])
    who = P.next()[0]
    if not once(k):
        return None
    if k == "ins":
        return item("%s adds one base to the middle of a gene. What is the most likely effect?" % who, "The reading frame shifts, so many amino acids after it change.",
                    ["Only one amino acid changes.", "Nothing changes.", "The gene gets one extra amino acid only."], "Insertions and deletions cause frameshifts.")
    if k == "del":
        return item("%s removes one base near the start of a gene. Why is this usually harmful?" % who, "It shifts the reading frame and changes the protein's shape.",
                    ["It changes only the last amino acid.", "It makes the protein identical.", "It only changes the DNA color."], "A frameshift scrambles every codon after it.")
    if k == "silent":
        return item("In %s's model, GCU changes to GCC, and both code for Ala. What is this mutation called?" % who, "a silent mutation",
                    ["a frameshift mutation", "a nonsense mutation", "a deletion"], "The amino acid stays the same.")
    if k == "nonsense":
        return item("A mutation turns a codon into a stop codon. What is it called?", "a nonsense mutation", ["a silent mutation", "a frameshift mutation", "an insertion"],
                    "The protein is cut short.")
    return item("Which mutation usually changes a protein the most?", "deleting one base near the start of the gene", ["changing one base near the end", "a silent mutation", "deleting three bases in a row at the end"],
                "An early frameshift changes almost every codon.")


B1 = bank([
    ("What are the four DNA bases?", "adenine, thymine, guanine, cytosine", ["adenine, uracil, guanine, cytosine", "alanine, threonine, glycine, cysteine", "glucose, fructose, sucrose, starch"], "RNA uses uracil instead of thymine."),
    ("Which base pairs with adenine in DNA?", "thymine", ["uracil", "guanine", "cytosine"], "A–T and G–C."),
    ("Which base pairs with adenine in RNA?", "uracil", ["thymine", "guanine", "cytosine"], "RNA has U, not T."),
    ("What is a gene?", "a section of DNA that codes for a protein", ["a type of sugar", "a whole chromosome", "a ribosome"], "Genes are instructions."),
    ("What does transcription make?", "mRNA from a DNA template", ["a protein from mRNA", "DNA from protein", "glucose"], "DNA → mRNA."),
    ("What does translation make?", "a protein (a chain of amino acids)", ["mRNA", "DNA", "a chromosome"], "mRNA → protein."),
    ("Where does transcription happen in eukaryotic cells?", "in the nucleus", ["at the ribosome", "in the cell membrane", "in the mitochondria only"], "DNA stays in the nucleus."),
    ("Where does translation happen?", "at ribosomes", ["inside the nucleus", "in the cell wall", "in the vacuole"], "Ribosomes build proteins."),
    ("What is a codon?", "a group of three mRNA bases", ["one base", "a whole gene", "an amino acid"], "Three bases = one codon."),
    ("Which molecule carries amino acids to the ribosome?", "tRNA", ["mRNA", "DNA", "rRNA only"], "tRNA has an anticodon."),
])
B2 = bank([
    ("What is the start codon?", "AUG", ["UAA", "UGA", "GGG"], "AUG codes for Met and starts translation."),
    ("Why do proteins with different amino acid orders do different jobs?", "The order determines how the protein folds into its shape.", ["All proteins have the same shape.", "Amino acid order has no effect.", "Proteins are made of DNA."], "Shape determines function."),
    ("Name a protein job in the body.", "enzymes speed up reactions", ["storing genetic code", "making mRNA in the nucleus", "being a sugar"], "Proteins carry out life functions."),
    ("Every body cell has the same DNA. Why are muscle and nerve cells different?", "Different genes are turned on in each cell type.", ["They have different DNA.", "They have no genes.", "Muscles have no DNA."], "Gene expression differs."),
    ("What holds the two DNA strands together?", "hydrogen bonds between base pairs", ["peptide bonds", "glucose", "ribosomes"], "Bases pair across the middle."),
    ("What is the shape of DNA?", "a double helix", ["a single straight line", "a circle of protein", "a triple helix"], "Watson and Crick, using Franklin's data."),
    ("What is the anticodon for the mRNA codon AUG?", "UAC", ["AUG", "TAC", "UAG"], "tRNA anticodon pairs with the codon."),
    ("A stop codon is reached. What happens?", "Translation ends and the protein is released.", ["Translation starts.", "A new amino acid is added.", "DNA is copied."], "Stop codons code for no amino acid."),
])
B5 = bank([
    ("Sickle cell disease comes from one base change in a hemoglobin gene. Why does it matter?", "One amino acid changes, which changes the protein's shape and function.", ["The whole gene disappears.", "The DNA becomes RNA.", "It has no effect."], "Structure → function."),
    ("Insulin for diabetes is made by bacteria with a human insulin gene. Why does this work?", "All living things use the same genetic code.", ["Bacteria are human cells.", "Insulin is a sugar.", "Bacteria have no ribosomes."], "The code is nearly universal."),
    ("A scientist finds a mutation that changes UAU (Tyr) to UAA (stop). What is likely?", "The protein is cut short and may not work.", ["The protein is longer.", "Nothing changes.", "Only one amino acid changes."], "A nonsense mutation."),
    ("Evidence that DNA, not protein, carries genes came from viruses that inject only DNA. What did the viruses' new copies contain?", "the virus's DNA instructions", ["the host's proteins only", "no DNA", "only sugar"], "Hershey–Chase experiment."),
    ("A gene has 900 bases in its coding region (without the stop codon). How many amino acids?", "300", ["900", "2,700", "450"], "900 ÷ 3 = 300."),
])


def body():
    think = ("<p><b>DNA → mRNA → protein.</b> The order of bases in a gene sets the order of amino acids, and that order sets the protein's shape and job.</p>"
             "<ul><li><b>Pairing:</b> DNA A–T, G–C. RNA uses U: A–U.</li><li><b>Transcription</b> (nucleus): DNA template → mRNA.</li>"
             "<li><b>Translation</b> (ribosome): every 3 bases (a codon) → 1 amino acid. AUG starts; UAA, UAG, UGA stop.</li></ul>")
    ex = [("DNA template TAC GGA → mRNA?", ["T→A, A→U, C→G, G→C"], "AUG CCU"),
          ("mRNA with 60 coding bases → how many amino acids?", ["3 bases per amino acid", "60 ÷ 3"], "20")]
    mist = ["Pairing A with U in DNA. DNA uses T.", "Keeping T in mRNA. RNA uses U.", "Reading one base as one amino acid. A codon is 3 bases.",
            "Thinking translation happens in the nucleus. It happens at ribosomes."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("DNA and RNA basics", B1 + [(g_comp, 5), (g_mrna, 5)]),
        ("Base pairing", [(g_comp, 10), (g_mrna, 10)]),
        ("Codons and translation", B2 + [(g_trans, 8), (g_count, 4)]),
        ("Mutations", [(g_sub, 10), (g_mut, 5), (g_count, 5)]),
        ("Protein synthesis in action", B5 + [(g_trans, 6), (g_count, 5), (g_mrna, 4)]),
    ])
    make("biology", "dna-and-protein-synthesis", 1, "HS-LS1-1",
         "Construct an explanation based on evidence for how the structure of DNA determines the structure of proteins which carry out the essential functions of life through systems of specialized cells.",
         "DNA and Protein Synthesis",
         "DNA and Protein Synthesis Worksheets: Transcription and Translation (Biology)",
         "DNA and Protein Synthesis",
         "Free high school biology worksheets on DNA and protein synthesis (NGSS HS-LS1-1): base pairing, transcription, codon tables, translation and mutations. 100 questions with answers.",
         "DNA → mRNA → protein.",
         "Three bases make a codon; the order of amino acids sets the protein's shape and job.",
         body(),
         [("What is the difference between transcription and translation?", "Transcription copies a gene into mRNA in the nucleus. Translation reads the mRNA at a ribosome to build a protein."),
          ("How do you use a codon table?", "Split the mRNA into groups of three bases from the start codon AUG, then look up each codon's amino acid until a stop codon."),
          ("How can one base change matter?", "It can change one amino acid (substitution), stop the protein early (nonsense) or shift every codon after it (insertion or deletion).")],
         sets)


if __name__ == "__main__":
    main()
