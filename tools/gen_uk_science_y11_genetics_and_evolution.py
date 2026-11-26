# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Biology): Genetics and Evolution
  python tools/gen_uk_science_y11_genetics_and_evolution.py
Sexual and asexual reproduction, meiosis, DNA and the genome, genetic inheritance with Punnett squares, inherited
disorders (cystic fibrosis, polydactyly), sex determination, variation, natural selection and evolution, selective
breeding and genetic engineering, evidence for evolution (fossils, antibiotic resistance) and classification.
Reuses the US Biology heredity, meiosis, natural selection and evidence questions in British English.
Wrong answers come from real mistakes: "a carrier has the disorder", "each child has a 25% chance of being a boy",
"bacteria become resistant because they get used to antibiotics", "gametes have 46 chromosomes".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62103)
PS, ME, NS, EV = "bio_punnett_squares_and_heredity", "bio_meiosis_and_genetic_variation", "bio_natural_selection_and_adaptation", "bio_evidence_for_evolution"
us_mono, us_expect, us_ratio = us(PS, "g_mono"), us(PS, "g_expect", rep=((" are with ", " have "),)), us(PS, "g_ratio")
us_num, us_cmp = us(ME, "g_num", drop=("meiosis I",)), us(ME, "g_cmp", drop=("II", "crossing"))
us_resist, us_factor, us_scen = us(NS, "g_resist"), us(NS, "g_factor"), us(NS, "g_scen")
us_layer, us_trans = us(EV, "g_layer"), us(EV, "g_trans")

DIS = [("cystic fibrosis", "recessive", "f"), ("polydactyly", "dominant", "D")]
CROSS = {"recessive": [("FF", "Ff"), ("Ff", "Ff"), ("Ff", "ff"), ("FF", "ff"), ("ff", "ff")],
         "dominant": [("Dd", "dd"), ("Dd", "Dd"), ("DD", "dd"), ("dd", "dd")]}


def _kids(a, b):
    return [x + y for x in a for y in b]


def g_dis():
    name, kind, _ = R.choice(DIS)
    a, b = R.choice(CROSS[kind])
    k = R.choice(["has", "carrier"]) if kind == "recessive" else "has"
    if not once(("dis", name, a, b, k)):
        return None
    kids = _kids(a, b)
    if kind == "recessive":
        n = sum(1 for g in kids if g == "ff") if k == "has" else sum(1 for g in kids if sorted(g) == ["F", "f"])
        al = "F is the normal allele and f causes cystic fibrosis"
    else:
        n = sum(1 for g in kids if "D" in g)
        al = "D causes polydactyly and d is the normal allele"
    pc = n * 25
    if k == "carrier" and pc == 0 and not once(("dis0",), 1):
        return None
    what = "have %s" % name if k == "has" else "be a carrier"
    return item("Cystic fibrosis is caused by a recessive allele. " * (kind == "recessive") + "Polydactyly is caused by a dominant allele. " * (kind == "dominant") +
                "Here %s. The parents are %s and %s. What is the chance that a child will %s?" % (al, a, b, what), "%d%%" % pc,
                [x for x in ["0%", "25%", "50%", "75%", "100%"] if x != "%d%%" % pc][:3] if pc else ["25%", "50%", "100%"],
                "Punnett square: %s. A carrier has one recessive allele but not the disorder." % ", ".join(kids))


SPP = [("Homo sapiens", "humans"), ("Panthera leo", "lions"), ("Panthera tigris", "tigers"), ("Canis lupus", "wolves"), ("Felis catus", "domestic cats"),
       ("Quercus robur", "English oak trees"), ("Bellis perennis", "daisies"), ("Erinaceus europaeus", "European hedgehogs"), ("Vulpes vulpes", "red foxes")]


def g_bin():
    sp, common = R.choice(SPP)
    k = R.choice(["genus", "species"])
    if not once(("bin", sp, k)):
        return None
    g, s = sp.split()
    a = g if k == "genus" else s
    w = [s if k == "genus" else g, common.split()[-1], R.choice([x[0].split()[0] for x in SPP if x[0].split()[0] != g])]
    if len(set(w + [a])) < 4:
        return None
    return item("The scientific name of %s is <i>%s</i>. What is the %s name?" % (common, sp, k), a, w, "Binomial system: genus first (capital letter), then species.")


HIER = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]


def g_hier():
    i = R.randrange(len(HIER) - 1)
    k = R.choice(["after", "before"])
    if not once(("hi", i, k)):
        return None
    if k == "before":
        return item("In the Linnaean system, which group comes straight before %s?" % HIER[i + 1], HIER[i], R.sample([x for x in HIER if x not in (HIER[i], HIER[i + 1])], 3),
                    "Kingdom, phylum, class, order, family, genus, species.")
    return item("In the Linnaean system, which group comes straight after %s?" % HIER[i], HIER[i + 1], R.sample([x for x in HIER if x not in (HIER[i], HIER[i + 1])], 3),
                "Kingdom, phylum, class, order, family, genus, species.")


B1 = bank([
    ("How many chromosomes are in a human gamete?", "23", ["46", "92", "12"], "Meiosis halves the number."),
    ("What is one advantage of asexual reproduction?", "Only one parent is needed, so it is fast.", ["It produces variation.", "It needs two parents.", "It uses meiosis."], "Offspring are clones."),
    ("What is the genome?", "all the genetic material of an organism", ["one gene", "the nucleus only", "a single chromosome"], "The human genome has been studied to find genes linked to diseases."),
    ("What is a gene?", "a short section of DNA that codes for a protein", ["a whole chromosome", "a type of cell", "a sex cell"], "Genes code for sequences of amino acids."),
])
B2 = bank([
    ("What does homozygous mean?", "two identical alleles, such as BB or bb", ["two different alleles", "one allele only", "having a disorder"], "Heterozygous means two different alleles, such as Bb."),
    ("What is a phenotype?", "the characteristic that is shown, such as brown eyes", ["the alleles present", "the number of chromosomes", "the DNA base sequence only"], "The genotype is the alleles."),
    ("What is the chance that a baby is a girl?", "50%", ["25%", "75%", "100%"], "XX × XY gives XX, XX, XY, XY."),
    ("Which sex chromosomes does a human male have?", "XY", ["XX", "YY", "X only"], "Females are XX."),
])
B4 = bank([
    ("What is selective breeding?", "choosing parents with useful characteristics to breed together", ["changing genes with enzymes", "cloning a cell", "letting nature choose"], "Repeated over many generations."),
    ("What is genetic engineering?", "transferring a gene from one organism to another", ["breeding the best animals", "growing cells in a dish", "using antibiotics"], "For example, bacteria that make human insulin."),
    ("Why do bacteria become resistant to antibiotics?", "A mutation makes some resistant; they survive and reproduce.", ["They get used to the antibiotic.", "Antibiotics make them stronger.", "They learn to avoid it."], "Natural selection."),
    ("Why should patients finish a course of antibiotics?", "to kill all the bacteria so none survive to become resistant", ["to make them taste better", "so the body makes more antibiotics", "to stop viruses"], "Also, do not use antibiotics for viral infections."),
])
B5 = bank([
    ("Why are there gaps in the fossil record?", "Many soft-bodied organisms did not form fossils, and many fossils have been destroyed.", ["Fossils are always complete.", "Evolution stopped.", "Animals did not exist then."], "Fossils form only in certain conditions."),
    ("What are the three domains in Woese's system?", "archaea, bacteria and eukaryota", ["plants, animals and fungi", "kingdom, phylum and class", "vertebrates, invertebrates and plants"], "Based on chemical analysis."),
])

if __name__ == "__main__":
  build(U, 11, "genetics-and-evolution", 3, "Biology", "Inheritance, variation and evolution",
      "Sexual and asexual reproduction; meiosis; DNA and the genome; genetic inheritance, including Punnett squares; inherited disorders; sex determination; variation; evolution by natural selection; selective breeding and genetic engineering; evidence for evolution, including fossils and antibiotic resistance; classification of living organisms.",
      "Genetics and Evolution", "Genetics and Evolution",
      "Free Year 11 GCSE Combined Science worksheets on inheritance and evolution: meiosis, Punnett squares, cystic fibrosis, sex determination, natural selection, antibiotic resistance and classification. 100 questions with answers.",
      "Each parent gives one allele of every gene.",
      "Use a Punnett square to find the chances.",
      "<p><b>Meiosis makes gametes with half the chromosomes.</b></p><ul><li>Dominant alleles show with one copy; recessive alleles need two copies.</li>"
      "<li>A carrier has one recessive allele but not the disorder.</li>"
      "<li>Natural selection: variation → the best adapted survive and reproduce → their alleles become more common.</li></ul>",
      [("Ff × Ff. Chance of cystic fibrosis?", ["FF, Ff, Ff, ff", "1 out of 4"], "25%"), ("Scientific name Panthera leo. Genus?", ["Genus first"], "Panthera")],
      ["Thinking a carrier has the disorder.", "Thinking bacteria get used to antibiotics.", "Thinking gametes have 46 chromosomes."],
      [("How do you work out the chance of an inherited disorder?", "Draw a Punnett square with each parent's alleles. Count the boxes with the genotype you want out of 4."),
       ("What is a carrier?", "Someone with one recessive allele for a disorder. They do not have the disorder but can pass the allele on."),
       ("How does antibiotic resistance show evolution?", "A mutation makes some bacteria resistant. When an antibiotic is used, these survive and reproduce, so resistant bacteria become common.")],
      [("Meiosis and DNA", B1 + [(us_num, 8), (us_cmp, 4), (us_mono, 4)]),
       ("Punnett squares", B2 + [(us_mono, 6), (us_ratio, 5), (us_expect, 5)]),
       ("Inherited disorders", [(g_dis, 11), (us_expect, 9)]),
       ("Natural selection", B4 + [(us_resist, 6), (us_factor, 5), (us_scen, 5)]),
       ("Evidence and classification", B5 + [(us_layer, 4), (us_trans, 2), (g_bin, 6), (g_hier, 6)])])
