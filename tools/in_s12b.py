# -*- coding: utf-8 -*-
"""Class 12 Biology (NCERT Biology, 13 chapters): question tables, banks and UNITS()."""
import math
from in_sci import _R
from in_srs import ch, A, B, SU, pairs, tq, nf, al_bio as BI
from in_s11b import OD, FAM, T, A0

BIO = "Biology"


def ri(a, b, step=1):
    return _R[0].randrange(a, b + 1, step)


def K(f, *kinds):
    return lambda: f(ch(kinds))


def fam(g, *fs):
    FAM[id(g)] = [list(x) for x in fs]


def PR(rows, fwd, back=None, pool=None):
    return pairs(rows, fwd, back, pool)


# =================================================================== 1 sexual reproduction in flowering plants
G1 = {"a part of the stamen": ["anther", "filament", "microsporangium", "connective"], "a part of the pistil": ["stigma", "style", "ovary", "ovule"],
      "a part of the mature embryo sac": ["egg cell", "two synergids", "three antipodal cells", "central cell with two polar nuclei"],
      "a part of a mature pollen grain": ["vegetative cell", "generative cell", "exine of sporopollenin", "intine", "germ pore"],
      "an outbreeding device": ["dichogamy (pollen and stigma ripen at different times)", "self-incompatibility", "unisexual flowers", "herkogamy (anther and stigma placed apart)"],
      "a wind-pollinated plant": ["maize", "wheat", "grasses", "rice"], "a water-pollinated plant": ["Vallisneria", "Hydrilla", "Zostera (sea grass)"], "an insect-pollinated plant": ["salvia", "sunflower", "mango", "orchids"]}
fam(G1, ["a part of the stamen", "a part of the pistil", "a part of the mature embryo sac", "a part of a mature pollen grain"], ["an outbreeding device"],
    ["a wind-pollinated plant", "a water-pollinated plant", "an insect-pollinated plant"])
P1 = [("autogamy", "pollen goes to the stigma of the same flower"), ("geitonogamy", "pollen goes to another flower on the same plant"), ("xenogamy", "pollen goes to a flower of a different plant"),
      ("apomixis", "seeds form without fertilisation"), ("polyembryony", "more than one embryo forms in a seed, as in citrus"), ("parthenocarpy", "fruits develop without fertilisation, as in banana"),
      ("syngamy", "a male gamete fuses with the egg to form the zygote"), ("triple fusion", "a male gamete fuses with the two polar nuclei to form the primary endosperm nucleus"),
      ("emasculation", "removing the anthers from a bisexual flower before they shed pollen"), ("bagging", "covering a flower to stop unwanted pollen reaching it")]
PLOID = [("the endosperm", "triploid (3n)"), ("the zygote", "diploid (2n)"), ("the egg cell", "haploid (n)"), ("a pollen grain cell", "haploid (n)"), ("the nucellus", "diploid (2n)"),
         ("the megaspore mother cell", "diploid (2n)"), ("a synergid", "haploid (n)"), ("an antipodal cell", "haploid (n)"), ("the integuments", "diploid (2n)")]
B1 = [("How many nuclei are there in a typical mature embryo sac (Polygonum type)?", "8 nuclei in 7 cells", ["7 nuclei in 8 cells", "4 nuclei in 4 cells", "16 nuclei"], "Three antipodals, two synergids, one egg and a central cell with two polar nuclei."),
      ("What is the outer layer of the pollen grain made of?", "sporopollenin", ["cellulose", "chitin", "lignin"], "It resists heat, acids and alkalis."),
      ("At what stage are pollen grains shed in most angiosperms?", "the 2-celled stage", ["the 1-celled stage", "the 3-celled stage", "the 8-celled stage"], "In about 40% of species they are shed at the 3-celled stage."),
      ("Through which structure does the pollen tube usually enter the ovule?", "the micropyle", ["the chalaza", "the funicle", "the hilum"], "The synergids guide it with their filiform apparatus."),
      ("What is the filiform apparatus?", "finger-like thickenings of the synergids that guide the pollen tube", ["a part of the anther", "the seed coat", "the hilum"], "It is at the micropylar end."),
      ("Why is double fertilisation so called?", "two fusions happen in the embryo sac: syngamy and triple fusion", ["two eggs are fertilised", "two pollen tubes enter", "fertilisation happens twice a year"], "It is unique to flowering plants."),
      ("What is a perisperm?", "the remains of the nucellus in some seeds, such as black pepper", ["the seed coat", "the endosperm", "the cotyledon"], "It persists in the seed."),
      ("What is a cleistogamous flower?", "a flower that never opens and is always self-pollinated", ["a flower pollinated by bats", "a male flower", "a flower with no petals"], "e.g. Viola, Oxalis, Commelina."),
      ("How long can pollen grains of rice and wheat stay viable?", "about 30 minutes", ["several months", "several years", "a few seconds"], "Some families keep viable pollen for months."),
      ("What is the scutellum?", "the single cotyledon of a grass embryo", ["the seed coat", "the root cap", "the endosperm"], "It is shield-shaped."),
      ("Which part of a monocot embryo covers the plumule?", "the coleoptile", ["the coleorhiza", "the scutellum", "the epicotyl"], "The coleorhiza covers the radicle."),
      ("What is a false fruit?", "a fruit that develops from the thalamus as well as the ovary, such as apple", ["a fruit with no seeds", "a fruit without a peel", "a fruit made only from the ovary"], "Strawberry and cashew are also false fruits."),
      ("Which tapetum function supports pollen development?", "it nourishes the developing pollen grains", ["it protects the ovule", "it forms the seed coat", "it makes the stigma sticky"], "It is the innermost wall layer of the microsporangium."),
      ("What is the 'pollen–pistil interaction'?", "the events from pollen landing on the stigma to the pollen tube entering the ovule, including compatibility checks", ["insects visiting flowers", "seed dispersal", "fruit ripening"], "The pistil recognises compatible pollen."),
      ("Why can seeds stay alive for many years?", "they become dry and dormant, with very low metabolism", ["they keep growing slowly", "they photosynthesise", "they are frozen"], "Some lupin seeds germinated after about 10,000 years.")]


# =================================================================== 2 human reproduction
G2 = {"a part of the male reproductive system": ["testis", "epididymis", "vas deferens", "seminal vesicle", "prostate gland", "bulbourethral gland"],
      "a part of the female reproductive system": ["ovary", "oviduct (fallopian tube)", "uterus", "cervix", "vagina", "fimbriae"],
      "a hormone made by the anterior pituitary": ["FSH", "LH", "prolactin"], "a hormone made by the placenta": ["hCG", "hPL", "placental oestrogens", "placental progestogens"],
      "a hormone made by the ovary": ["oestrogen from the growing follicles", "progesterone from the corpus luteum", "relaxin (in late pregnancy)"],
      "a part of a human sperm": ["head with acrosome", "neck", "middle piece with mitochondria", "tail"], "a layer around the ovum": ["zona pellucida", "corona radiata", "plasma membrane of the ovum"]}
fam(G2, ["a part of the male reproductive system", "a part of the female reproductive system"], ["a hormone made by the anterior pituitary", "a hormone made by the placenta", "a hormone made by the ovary"], ["a part of a human sperm", "a layer around the ovum"])
P2 = [("Sertoli cells", "nourishing the developing sperm"), ("Leydig cells", "making testosterone"), ("acrosome", "holding enzymes that help the sperm enter the ovum"), ("corpus luteum", "making progesterone after ovulation"),
      ("Graafian follicle", "the mature follicle that releases the ovum"), ("trophoblast", "the outer layer of the blastocyst that attaches to the uterus"), ("inner cell mass", "the cells of the blastocyst that form the embryo"),
      ("placenta", "exchanging food, oxygen and wastes between mother and foetus"), ("ampulla of the oviduct", "the usual site of fertilisation"), ("endometrium", "the inner lining of the uterus where the embryo implants")]


def cyc(k=None):
    k = k or ch(["ov", "days", "sperm"])
    if k == "ov":
        L = ri(21, 35)
        return A0("A woman has a regular menstrual cycle of %d days. Ovulation usually happens about 14 days before the next period. On about which day of the cycle does she ovulate?" % L, L - 14,
                  [L // 2 if L // 2 != L - 14 else L // 2 + 1, 14 if L != 28 else 21, L - 10], "", "Day of ovulation ≈ cycle length − 14 = %d − 14 = <b>day %d</b>." % (L, L - 14))
    if k == "days":
        w = ri(30, 41)
        return A0("A baby is born at %d weeks of pregnancy. How many days is that?" % w, w * 7, [w * 30, w * 5, w + 7], " days", "%d × 7 = <b>%d days</b>; a full-term pregnancy is about 9 months (280 days)." % (w, w * 7))
    n = ri(2, 90) * 50
    return A0("Spermatogenesis starts with %d primary spermatocytes. How many sperms form?" % n, 4 * n, [n, 2 * n, 8 * n], "", "Each primary spermatocyte gives 4 sperms after meiosis: <b>%d</b>." % (4 * n))


B2 = [("How many sperms are released in a normal ejaculation?", "about 200 to 300 million", ["about 1,000", "about 1 million", "about 10 billion"], "At least 60% must have normal shape and 40% vigorous motility."),
      ("How many ova does one primary oocyte give rise to?", "one", ["two", "four", "eight"], "The other products are polar bodies."),
      ("At what stage does a human secondary oocyte complete meiosis II?", "after a sperm enters it", ["before ovulation", "at birth", "at puberty"], "A second polar body is then released."),
      ("Which hormone surge causes ovulation?", "LH (luteinising hormone)", ["FSH", "progesterone", "prolactin"], "It peaks around day 14."),
      ("What happens to the corpus luteum if fertilisation does not happen?", "it degenerates, progesterone falls and menstruation begins", ["it grows larger", "it becomes a Graafian follicle", "it makes the placenta"], "The endometrium is shed."),
      ("Which part of the blastocyst forms the embryo?", "the inner cell mass", ["the trophoblast", "the zona pellucida", "the corona radiata"], "The trophoblast helps form the placenta."),
      ("When does the human heart begin to form?", "by the end of the first month of pregnancy", ["after six months", "at birth", "after one week"], "By the end of the second month limbs and digits develop."),
      ("What is parturition?", "the process of childbirth", ["fertilisation", "implantation", "milk production"], "Oxytocin from the pituitary causes strong uterine contractions."),
      ("Why is colostrum important for a newborn baby?", "it contains antibodies (IgA) that protect the baby", ["it has no nutrients", "it helps the baby sleep", "it stops growth"], "It is the first milk."),
      ("What is menopause?", "the stop of the menstrual cycle at about 50 years of age", ["the first menstruation", "the release of an egg", "pregnancy"], "Menarche is the first menstruation."),
      ("Where are sperms stored and matured?", "in the epididymis", ["in the prostate", "in the bladder", "in the seminal vesicle"], "They travel through the vas deferens."),
      ("What is the role of the zona pellucida after a sperm enters?", "it changes to block entry of other sperms", ["it dissolves completely", "it forms the placenta", "it produces hormones"], "This ensures only one sperm fertilises the ovum."),
      ("How long does a human menstrual cycle usually last?", "about 28 to 29 days", ["about 7 days", "about 3 months", "about 1 year"], "Menstruation lasts 3–5 days."),
      ("Which cells undergo meiosis to form sperms?", "primary spermatocytes", ["Sertoli cells", "Leydig cells", "spermatids"], "Spermatids then change into sperms (spermiogenesis).")]


# =================================================================== 3 reproductive health
G3 = {"a barrier method of contraception": ["condoms", "diaphragms", "cervical caps", "vaults"], "a natural method of contraception": ["periodic abstinence", "coitus interruptus (withdrawal)", "lactational amenorrhoea"],
      "an intra-uterine device (IUD)": ["Copper T", "Multiload 375", "LNG-20", "Lippes loop"], "a surgical method of contraception": ["vasectomy", "tubectomy"],
      "a sexually transmitted infection (STI)": ["gonorrhoea", "syphilis", "genital herpes", "chlamydiasis", "trichomoniasis", "hepatitis B", "HIV infection"],
      "an assisted reproductive technology (ART)": ["IVF (test-tube baby)", "ZIFT", "GIFT", "ICSI", "artificial insemination (IUI)"]}
fam(G3, ["a barrier method of contraception", "a natural method of contraception", "an intra-uterine device (IUD)", "a surgical method of contraception"], ["a sexually transmitted infection (STI)"], ["an assisted reproductive technology (ART)"])
P3 = [("ZIFT", "transferring a zygote or early embryo (up to 8 cells) into the fallopian tube"), ("IUT", "transferring an embryo with more than 8 cells into the uterus"), ("GIFT", "transferring an ovum from a donor into the fallopian tube"),
      ("ICSI", "injecting a sperm directly into an ovum in the laboratory"), ("IUI", "placing semen into the uterus (artificial insemination)"), ("amniocentesis", "testing the amniotic fluid for genetic disorders in the foetus")]
B3 = [("What is the main aim of family planning programmes?", "to have a healthy, smaller family by spacing and limiting births", ["to stop all births", "to increase the population", "to choose the sex of the baby"], "India started such a programme in 1951."),
      ("How do oral contraceptive pills work?", "they stop ovulation and implantation, and change the cervical mucus", ["they kill sperm in the testes", "they block the oviduct surgically", "they increase ovulation"], "'Saheli' is a non-steroidal once-a-week pill developed in India."),
      ("Why is amniocentesis for sex determination banned in India?", "it is misused to find and abort female foetuses", ["it is always painful", "it is too expensive", "it is not accurate"], "It is allowed only to detect genetic disorders."),
      ("What is the legal minimum age of marriage for women in India?", "18 years", ["16 years", "21 years", "25 years"], "For men it is 21 years."),
      ("Up to which week of pregnancy is medical termination of pregnancy (MTP) considered relatively safe?", "the first trimester (about 12 weeks)", ["the third trimester", "the last week", "any time"], "It is legal in India under certain conditions."),
      ("How do copper-releasing IUDs prevent pregnancy?", "Cu ions reduce sperm motility and their ability to fertilise", ["they release progesterone only", "they block the vas deferens", "they make the uterus bigger"], "Hormone-releasing IUDs make the uterus unsuitable for implantation."),
      ("What is infertility?", "the inability to conceive even after two years of unprotected sexual activity", ["having many children", "a sexually transmitted infection", "a type of contraception"], "Causes can be in either partner."),
      ("Which STIs are not completely curable?", "genital herpes, hepatitis B and HIV infection", ["gonorrhoea and syphilis", "all STIs", "none of them"], "Early detection and treatment of others help."),
      ("How can sexually transmitted infections be prevented?", "by avoiding unknown partners, using condoms and getting early check-ups", ["by eating more", "by sleeping more", "by taking antibiotics daily"], "Many STIs can lead to infertility if untreated."),
      ("What are emergency contraceptives?", "pills or IUDs used within 72 hours of unprotected intercourse", ["vaccines", "barrier devices only", "surgery"], "They are not for regular use."),
      ("What is vasectomy?", "cutting and tying the vas deferens in a male", ["removing the uterus", "tying the oviducts", "a hormone injection"], "It is a terminal (permanent) method."),
      ("What does RCH stand for in India's health programmes?", "Reproductive and Child Health Care", ["Rural Clinic and Hospital", "Red Cross Health", "Research on Child Hormones"], "It aims at awareness and better reproductive health.")]


# =================================================================== 4 principles of inheritance
def gen(k=None):
    k = k or ch(["mono", "di", "test", "back", "inc", "blood"])
    R = _R[0]
    if k == "mono":
        n = R.randint(5, 50) * 4
        t = ch(["tall", "short"])
        v = n * 3 // 4 if t == "tall" else n // 4
        return A0("In pea, tall (T) is dominant over dwarf (t). Two heterozygous tall plants (Tt × Tt) give %d offspring. How many are expected to be %s?" % (n, "tall" if t == "tall" else "dwarf"), v,
                  [n // 2, n, n * 3 // 8 if t == "tall" else n * 3 // 4], "", "Tt × Tt gives 3 tall : 1 dwarf, so %s of %d = <b>%d</b>." % ("¾" if t == "tall" else "¼", n, v))
    if k == "di":
        n = R.randint(2, 30) * 16
        c, f = ch([("round and yellow", 9), ("round and green", 3), ("wrinkled and yellow", 3), ("wrinkled and green", 1)])
        return A0("In pea, round (R) is dominant over wrinkled (r) and yellow (Y) over green (y). An RrYy × RrYy cross gives %d seeds. How many are expected to be %s?" % (n, c), n * f // 16,
                  [n * (f + 3 if f < 9 else 3) // 16, n // 4, n * (16 - f) // 16], "", "The F₂ ratio is 9 : 3 : 3 : 1, so %d/16 of %d = <b>%d</b>." % (f, n, n * f // 16))
    if k == "test":
        n = R.randint(5, 50) * 2
        return A0("A heterozygous tall pea plant (Tt) is test-crossed with a dwarf plant (tt), giving %d offspring. How many are expected to be dwarf?" % n, n // 2, [n // 4, n * 3 // 4, n], "",
                  "Tt × tt gives 1 tall : 1 dwarf: <b>%d</b>." % (n // 2))
    if k == "back":
        n = R.randint(5, 25) * 4
        return A0("A dihybrid RrYy is test-crossed with rryy, giving %d offspring. How many are expected to be wrinkled and green?" % n, n // 4, [n // 16 if n % 16 == 0 else n // 8, n // 2, n * 3 // 4], "",
                  "The test-cross ratio is 1 : 1 : 1 : 1, so <b>%d</b>." % (n // 4))
    if k == "inc":
        n = R.randint(5, 50) * 4
        c, f = ch([("red", 1), ("pink", 2), ("white", 1)])
        return A0("In snapdragon, flower colour shows incomplete dominance (RR red, Rr pink, rr white). A cross Rr × Rr gives %d plants. How many are expected to be %s?" % (n, c), n * f // 4,
                  [n * 3 // 4, n // 2 if f == 1 else n // 4, n], "", "The ratio is 1 red : 2 pink : 1 white, so <b>%d</b>." % (n * f // 4))
    return T(BI.m_cross)()


G4 = {"a character studied by Mendel in pea": ["stem height", "flower colour", "seed shape", "seed colour", "pod shape", "pod colour", "flower position"],
      "an example of incomplete dominance": ["flower colour in snapdragon (dog flower)", "starch grain size in pea seeds (with respect to grain size)"], "an example of codominance": ["ABO blood groups (I<sup>A</sup>I<sup>B</sup>)"],
      "a Mendelian disorder": ["haemophilia", "sickle-cell anaemia", "colour blindness", "phenylketonuria", "thalassaemia", "cystic fibrosis"],
      "a chromosomal disorder": ["Down's syndrome", "Turner's syndrome", "Klinefelter's syndrome"], "an X-linked recessive disorder": ["red–green colour blindness", "haemophilia A"]}
fam(G4, ["a character studied by Mendel in pea"], ["an example of incomplete dominance", "an example of codominance"], ["a Mendelian disorder", "a chromosomal disorder", "an X-linked recessive disorder"])
SYN = [("Down's syndrome", "an extra copy of chromosome 21 (trisomy 21)"), ("Klinefelter's syndrome", "an extra X chromosome in a male (XXY)"), ("Turner's syndrome", "a missing X chromosome in a female (XO)"),
       ("sickle-cell anaemia", "a single base change making valine replace glutamic acid in β-globin"), ("phenylketonuria", "lack of the enzyme that converts phenylalanine into tyrosine"),
       ("haemophilia", "a protein needed for blood clotting is missing")]
SEXD = [("humans and Drosophila", "XX–XY (male heterogametic)"), ("birds", "ZW–ZZ (female heterogametic)"), ("grasshoppers", "XX–XO (male has one X)"), ("honey bees", "haplodiploidy (males develop from unfertilised eggs)")]
B4 = [("What is the law of segregation?", "the two alleles of a gene separate during gamete formation", ["alleles always stay together", "genes blend in offspring", "dominant alleles disappear"], "Each gamete gets one allele."),
      ("What is the law of independent assortment?", "alleles of different genes separate independently into gametes", ["genes on one chromosome stay together", "all alleles are dominant", "only one gene is inherited"], "Seen in a dihybrid cross."),
      ("What is the F₂ phenotypic ratio of a Mendelian dihybrid cross?", "9 : 3 : 3 : 1", ["3 : 1", "1 : 2 : 1", "1 : 1 : 1 : 1"], "The genotypic ratio of a monohybrid cross is 1 : 2 : 1."),
      ("What is the genotypic ratio in the F₂ of a monohybrid cross?", "1 : 2 : 1", ["3 : 1", "9 : 3 : 3 : 1", "1 : 1"], "TT : Tt : tt."),
      ("What is a test cross?", "crossing an organism with a homozygous recessive to find its genotype", ["crossing two dominants", "self-pollination", "crossing two F₁ plants"], "A 1 : 1 result shows heterozygosity."),
      ("Who proposed the chromosomal theory of inheritance?", "Sutton and Boveri", ["Mendel", "Morgan", "Darwin"], "Genes are on chromosomes."),
      ("Why did Morgan use Drosophila?", "it breeds quickly, has many visible variations and is easy to grow", ["it is large", "it has one chromosome", "it lives for years"], "He found linkage and recombination."),
      ("What is linkage?", "the tendency of genes on the same chromosome to be inherited together", ["genes on different chromosomes", "crossing over always", "blending of traits"], "Recombination happens when crossing over separates them."),
      ("Which parent decides the sex of a human child?", "the father", ["the mother", "both equally", "neither"], "Sperms carry either X or Y."),
      ("What is pleiotropy?", "one gene affecting several characters, as in phenylketonuria", ["many genes affecting one character", "a blending of traits", "a chromosome mutation"], "Polygenic inheritance is the reverse."),
      ("What is polygenic inheritance?", "a trait controlled by several genes, such as human skin colour", ["one gene controlling many traits", "inheritance through one sex", "a single dominant gene"], "It gives continuous variation."),
      ("What is aneuploidy?", "the gain or loss of one or a few chromosomes", ["doubling of all chromosome sets", "a gene mutation", "crossing over"], "Polyploidy is an increase in whole sets."),
      ("Why are haemophilia and colour blindness more common in males?", "males have only one X chromosome, so one recessive allele shows its effect", ["males have two X chromosomes", "they are dominant traits", "the Y chromosome causes them"], "Females are usually carriers."),
      ("Which blood groups can children of I<sup>A</sup>i × I<sup>B</sup>i parents have?", "A, B, AB and O", ["only A and B", "only AB", "only O"], "Each parent can pass on either allele.")]


# =================================================================== 5 molecular basis of inheritance
def mol(k=None):
    k = k or ch(["len", "codon", "aa", "bp"])
    if k == "len":
        bp = ri(1, 99) * 10 ** ri(2, 4)
        return A0("A DNA molecule has %s base pairs. How long is it? (distance between base pairs = 0.34 nm)" % nf(bp), bp * 0.34, [bp / 0.34, bp * 0.34 * 2, bp * 3.4], " nm", "Length = %s × 0.34 nm = <b>%s nm</b>." % (nf(bp), nf(bp * 0.34)))
    if k == "codon":
        n = ri(10, 500)
        return A0("A polypeptide has %d amino acids. How many nucleotides (excluding the stop codon) are needed in its mRNA?" % n, 3 * n, [n, 2 * n, 3 * n + 3], "", "Each amino acid needs one codon of three bases: 3 × %d = <b>%d</b>." % (n, 3 * n))
    if k == "aa":
        c = ri(20, 300)
        return A0("An mRNA has a reading frame of %d codons, the last being a stop codon. How many amino acids are in the polypeptide?" % c, c - 1, [c, 3 * c, c - 2], "", "The stop codon codes for no amino acid: <b>%d</b>." % (c - 1))
    bp = ri(10, 500) * 10
    return A0("A DNA segment has %d base pairs. How many hydrogen bonds hold it together if 30%% of its bases are adenine?" % bp, int(bp * 0.6) * 2 + int(bp * 0.4) * 3,
              [bp * 2, bp * 3, int(bp * 2.5)], "", "A = T = 30%%, G = C = 20%%. A–T pairs = %d (2 bonds), G–C pairs = %d (3 bonds): total = <b>%s</b>." % (int(bp * 0.6), int(bp * 0.4), nf(int(bp * 0.6) * 2 + int(bp * 0.4) * 3)))


G5 = {"a purine base": ["adenine", "guanine"], "a pyrimidine base": ["cytosine", "thymine", "uracil"], "an enzyme of DNA replication": ["DNA polymerase", "DNA ligase", "helicase", "primase", "topoisomerase"],
      "a part of the lac operon": ["the promoter", "the operator", "the z gene (β-galactosidase)", "the y gene (permease)", "the a gene (transacetylase)"], "a stop codon": ["UAA", "UAG", "UGA"], "a start codon": ["AUG"]}
fam(G5, ["a purine base", "a pyrimidine base"], ["an enzyme of DNA replication"], ["a part of the lac operon"], ["a stop codon", "a start codon"])
P5 = [("Frederick Griffith", "transformation in Streptococcus pneumoniae using mice"), ("Hershey and Chase", "showing with bacteriophages that DNA is the genetic material"), ("Meselson and Stahl", "showing that DNA replicates semi-conservatively, using ¹⁵N"),
      ("Watson and Crick", "the double-helix model of DNA"), ("Erwin Chargaff", "showing that A = T and G = C in DNA"), ("Jacob and Monod", "the lac operon model of gene regulation"), ("George Gamow", "suggesting that the genetic code is made of three bases"),
      ("Har Gobind Khorana", "making RNA molecules with known base sequences to crack the code"), ("Alec Jeffreys", "DNA fingerprinting")]
B5 = [("What is the sugar in DNA?", "deoxyribose", ["ribose", "glucose", "fructose"], "RNA has ribose."),
      ("What is the backbone of a DNA strand made of?", "alternating sugar and phosphate groups", ["bases only", "amino acids", "fatty acids"], "The bases point inwards."),
      ("What does semi-conservative replication mean?", "each new DNA molecule has one old strand and one new strand", ["both strands are new", "both strands are old", "DNA does not replicate"], "Meselson and Stahl showed this."),
      ("In which direction does DNA polymerase add nucleotides?", "5′ → 3′", ["3′ → 5′", "both directions", "randomly"], "So one strand is made in short Okazaki fragments."),
      ("What are Okazaki fragments?", "short DNA pieces made on the lagging strand", ["pieces of RNA", "parts of the ribosome", "introns"], "DNA ligase joins them."),
      ("What is transcription?", "making RNA from a DNA template", ["making protein from RNA", "copying DNA", "joining amino acids"], "RNA polymerase does this."),
      ("What is translation?", "making a polypeptide from the code in mRNA", ["making RNA from DNA", "copying DNA", "splicing"], "It happens on ribosomes."),
      ("What is splicing?", "removing introns and joining exons in the primary RNA transcript of eukaryotes", ["copying DNA", "adding amino acids", "breaking proteins"], "A cap and a poly-A tail are also added."),
      ("Why is the genetic code called degenerate?", "most amino acids are coded by more than one codon", ["it changes often", "it is not universal", "codons overlap"], "There are 61 sense codons for 20 amino acids."),
      ("What does 'the code is universal' mean?", "the same codons code for the same amino acids in nearly all organisms", ["every gene is the same", "all proteins are the same", "codons are read in any order"], "This allows genetic engineering."),
      ("What is the function of tRNA?", "it brings the correct amino acid to the ribosome by matching its anticodon to the codon", ["it carries the code from DNA", "it forms the ribosome", "it is a protein"], "It has a clover-leaf shape."),
      ("How many base pairs are there in the human genome?", "about 3 × 10⁹ (3 billion)", ["about 3 million", "about 30,000", "about 3 × 10¹²"], "The Human Genome Project finished in 2003."),
      ("What does the Human Genome Project show about the number of human genes?", "there are about 20,000–25,000 genes", ["there are about 1 million genes", "there are about 100 genes", "every base is part of a gene"], "Less than 2% of the genome codes for proteins."),
      ("What is a VNTR?", "a variable number of tandem repeats used in DNA fingerprinting", ["a type of RNA", "a protein", "a hormone"], "Their number differs between people.")]


# =================================================================== 6 evolution
G6 = {"evidence for evolution from homologous organs": ["forelimbs of whales, bats, cheetahs and humans", "thorns of Bougainvillea and tendrils of Cucurbita", "hearts of vertebrates"],
      "an example of analogous organs": ["wings of a butterfly and a bird", "eyes of an octopus and a mammal", "flippers of penguins and dolphins", "sweet potato (root) and potato (stem)"],
      "an example of natural selection in action": ["industrial melanism in peppered moths", "antibiotic-resistant bacteria", "herbicide-resistant weeds", "DDT-resistant mosquitoes"],
      "a factor affecting Hardy–Weinberg equilibrium": ["gene migration (gene flow)", "genetic drift", "mutation", "genetic recombination", "natural selection"],
      "an ancestor in human evolution": ["Dryopithecus", "Ramapithecus", "Australopithecus", "Homo habilis", "Homo erectus", "Neanderthal man"]}
fam(G6, ["evidence for evolution from homologous organs", "an example of analogous organs", "an example of natural selection in action"], ["a factor affecting Hardy–Weinberg equilibrium"], ["an ancestor in human evolution"])
P6 = [("Homo habilis", "the first human-like being, with a brain of about 650–800 cc, who probably did not eat meat"), ("Homo erectus", "a brain of about 900 cc and probably ate meat"),
      ("Neanderthal man", "a brain of about 1400 cc, who buried their dead"), ("Australopithecus", "a hominid of East African grasslands who hunted with stone weapons"), ("Homo sapiens", "modern humans, who arose in Africa")]
B6 = [("What did the Miller–Urey experiment show?", "simple organic molecules such as amino acids can form from gases like CH₄, H₂, NH₃ and water vapour with electric sparks", ["life came from space", "cells form from rocks", "DNA formed first in oceans"], "It supported Oparin and Haldane's idea."),
      ("Who proposed the theory of natural selection?", "Charles Darwin (and Alfred Wallace)", ["Lamarck", "Hugo de Vries", "Oparin"], "Darwin sailed on HMS Beagle."),
      ("What is adaptive radiation?", "evolution of many different species from one ancestor spreading into new habitats", ["a type of mutation", "the spread of radiation", "migration of birds"], "e.g. Darwin's finches and Australian marsupials."),
      ("What is convergent evolution?", "unrelated organisms evolving similar features because they live in similar habitats", ["related organisms becoming different", "a sudden mutation", "a fossil record"], "Analogous organs show it."),
      ("What is divergent evolution?", "related organisms evolving different features from a common structure", ["unrelated organisms becoming similar", "no change at all", "random drift only"], "Homologous organs show it."),
      ("Who proposed the mutation theory of evolution?", "Hugo de Vries, working with the evening primrose", ["Darwin", "Lamarck", "Mendel"], "He called large sudden changes saltation."),
      ("What does the Hardy–Weinberg principle state?", "allele frequencies stay constant in a population if no evolutionary forces act", ["allele frequencies always change", "all alleles are dominant", "populations never change"], "p² + 2pq + q² = 1."),
      ("What is the founder effect?", "a new population started by a few individuals has allele frequencies different from the original one", ["a mutation in one person", "migration of all individuals", "the death of all founders"], "A type of genetic drift."),
      ("How did industrial melanism support natural selection?", "dark moths survived better on soot-covered trees, so their numbers rose", ["moths changed colour on purpose", "light moths ate soot", "birds became dark"], "Seen in England after industrialisation."),
      ("Where did modern Homo sapiens arise?", "in Africa", ["in Australia", "in South America", "in Antarctica"], "They then spread across continents."),
      ("What is the brain capacity of modern humans (approximately)?", "about 1350–1450 cc", ["about 650 cc", "about 900 cc", "about 2500 cc"], "Neanderthals had about 1400 cc."),
      ("Which theory said that characters acquired during life are inherited?", "Lamarck's theory (use and disuse)", ["Darwin's theory", "the mutation theory", "the Hardy–Weinberg principle"], "e.g. the long neck of the giraffe.")]


# =================================================================== 7 human health and disease
G7 = {"a disease caused by bacteria": ["typhoid", "pneumonia", "tuberculosis", "diphtheria", "plague"], "a disease caused by a virus": ["common cold", "AIDS", "dengue", "chikungunya", "polio"],
      "a disease caused by a protozoan": ["malaria", "amoebiasis (amoebic dysentery)"], "a disease caused by a worm (helminth)": ["ascariasis", "filariasis (elephantiasis)"], "a disease caused by fungi": ["ringworm"],
      "a primary lymphoid organ": ["bone marrow", "thymus"], "a secondary lymphoid organ": ["spleen", "lymph nodes", "tonsils", "Peyer's patches", "appendix"],
      "an antibody type": ["IgA", "IgM", "IgE", "IgG"]}
fam(G7, ["a disease caused by bacteria", "a disease caused by a virus", "a disease caused by a protozoan", "a disease caused by a worm (helminth)", "a disease caused by fungi"], ["a primary lymphoid organ", "a secondary lymphoid organ"], ["an antibody type"])
P7 = [("typhoid", "Salmonella typhi"), ("pneumonia", "Streptococcus pneumoniae and Haemophilus influenzae"), ("malaria", "Plasmodium"), ("amoebiasis", "Entamoeba histolytica"),
      ("ascariasis", "Ascaris (roundworm)"), ("filariasis", "Wuchereria"), ("common cold", "rhinoviruses"), ("ringworm", "Microsporum, Trichophyton and Epidermophyton"), ("AIDS", "HIV (human immunodeficiency virus)")]
DRUG = [("opioids such as heroin (smack)", "the poppy plant Papaver somniferum"), ("cannabinoids such as marijuana and hashish", "Cannabis sativa"), ("cocaine (coke)", "the coca plant Erythroxylum coca"),
        ("nicotine", "tobacco"), ("morphine", "the latex of the poppy plant")]
B7 = [("What is the Widal test used to confirm?", "typhoid", ["malaria", "AIDS", "tuberculosis"], "It detects antibodies against Salmonella."),
      ("Which stage of Plasmodium enters the human body when an infected mosquito bites?", "sporozoites", ["gametocytes", "merozoites", "oocysts"], "They first multiply in the liver."),
      ("Which toxin causes the chill and high fever of malaria?", "haemozoin", ["histamine", "insulin", "interferon"], "It is released when red blood cells burst."),
      ("Which mosquito transmits malaria?", "the female Anopheles", ["the male Anopheles", "Aedes", "Culex"], "Aedes spreads dengue and chikungunya."),
      ("What is innate immunity?", "non-specific defence present from birth, such as skin, mucus and phagocytes", ["immunity from vaccines", "antibodies made after infection", "immunity passed only by milk"], "It acts against any foreign agent."),
      ("Which cells make antibodies?", "B-lymphocytes (plasma cells)", ["T-lymphocytes", "red blood cells", "platelets"], "T cells give cell-mediated immunity."),
      ("What is active immunity?", "immunity built when the body makes its own antibodies after infection or vaccination", ["antibodies given ready-made", "antibodies from the mother", "no immunity"], "It is slow but long-lasting."),
      ("What is passive immunity?", "ready-made antibodies given to the body, as from mother's milk or anti-tetanus serum", ["making one's own antibodies", "vaccination", "infection"], "It is quick but short-lived."),
      ("Which cells does HIV mainly attack?", "helper T-lymphocytes", ["red blood cells", "B-lymphocytes", "platelets"], "Immunity falls and other infections follow."),
      ("Which test is widely used to diagnose AIDS?", "ELISA", ["Widal", "PCR only", "the Mantoux test"], "It detects antibodies to HIV."),
      ("What is an allergy?", "an exaggerated immune response to an allergen such as pollen or dust", ["an infection", "an autoimmune disease", "a cancer"], "IgE antibodies and histamine are involved."),
      ("What is an autoimmune disease?", "a disease in which the immune system attacks the body's own cells", ["an allergy", "a bacterial infection", "a vitamin deficiency"], "e.g. rheumatoid arthritis."),
      ("What is metastasis?", "the spread of cancer cells to new sites in the body", ["the death of cancer cells", "a type of vaccine", "a benign tumour"], "Malignant tumours show it."),
      ("What is the main cause of cancer at the cell level?", "loss of contact inhibition, so cells divide uncontrollably", ["too much vitamin C", "lack of exercise only", "infection by every virus"], "Carcinogens can cause it."),
      ("Why should adolescents avoid drugs and alcohol?", "they harm health, cause dependence and can damage the nervous system and liver", ["they improve memory", "they are needed for growth", "they cure stress safely"], "Seek help from parents, teachers and counsellors.")]


# =================================================================== 8 microbes in human welfare
G8 = {"a microbe used in making food": ["Lactobacillus (curd)", "Saccharomyces cerevisiae (bread)", "Propionibacterium shermanii (Swiss cheese)", "Penicillium roqueforti (Roquefort cheese)"],
      "a microbe that produces an acid or enzyme": ["Aspergillus niger (citric acid)", "Acetobacter aceti (acetic acid)", "Clostridium butylicum (butyric acid)", "Lactobacillus (lactic acid)"],
      "a biofertiliser": ["Rhizobium", "Azotobacter", "Azospirillum", "Anabaena", "Nostoc", "mycorrhizal fungi (Glomus)"],
      "a biocontrol agent": ["Bacillus thuringiensis (Bt)", "Trichoderma", "baculoviruses (Nucleopolyhedrovirus)", "ladybird beetles", "dragonflies"],
      "a microbe in sewage treatment or biogas": ["methanogens (Methanobacterium)", "flocs of aerobic bacteria", "anaerobic sludge digesters"]}
fam(G8, ["a microbe used in making food", "a microbe that produces an acid or enzyme"], ["a biofertiliser", "a biocontrol agent", "a microbe in sewage treatment or biogas"])
P8 = [("penicillin", "the first antibiotic, discovered by Alexander Fleming from Penicillium notatum"), ("cyclosporin A", "an immunosuppressant from Trichoderma polysporum used in organ transplants"),
      ("statins", "blood-cholesterol-lowering agents from the yeast Monascus purpureus"), ("streptokinase", "a 'clot buster' from Streptococcus, used to remove clots in blood vessels"),
      ("lipases", "enzymes used in detergents to remove oily stains"), ("pectinases and proteases", "enzymes used to clear fruit juices"), ("Bt toxin", "a protein from Bacillus thuringiensis that kills insect larvae")]
B8 = [("Which microbe turns milk into curd?", "Lactobacillus (lactic acid bacteria)", ["Saccharomyces", "Rhizobium", "Aspergillus"], "LAB also increase vitamin B₁₂ in curd."),
      ("Why does dough rise when yeast is added?", "yeast produces carbon dioxide by fermentation", ["yeast produces oxygen", "yeast heats the dough", "yeast removes water"], "Used in making bread and idli."),
      ("What gives Swiss cheese its large holes?", "CO₂ produced by Propionibacterium shermanii", ["air pumped in", "fungus growth", "water bubbles"], ""),
      ("What is the main gas in biogas?", "methane", ["carbon dioxide", "hydrogen", "nitrogen"], "Made by methanogens from cattle dung."),
      ("What is BOD (biochemical oxygen demand)?", "the amount of oxygen used if all organic matter in a litre of water is oxidised by bacteria", ["the oxygen in air", "the oxygen in blood", "the boiling point of water"], "A high BOD means polluted water."),
      ("In sewage treatment, what are flocs?", "masses of bacteria and fungal filaments in the secondary (biological) treatment", ["stones and grit", "large floating objects", "chlorine tablets"], "They break down organic matter."),
      ("What is the activated sludge?", "part of the settled flocs sent back to the aeration tank as an inoculum", ["primary sludge", "clear effluent", "methane gas"], "The rest goes to anaerobic digesters."),
      ("Which organisation helped popularise biogas plants in India?", "IARI and KVIC", ["NASA", "WHO", "ISRO"], "Biogas is used for cooking and lighting."),
      ("Why are cyanobacteria important in paddy fields?", "they fix atmospheric nitrogen", ["they kill pests", "they make the water warm", "they eat rice"], "e.g. Anabaena and Nostoc."),
      ("How do mycorrhizae help plants?", "they absorb phosphorus from the soil and pass it to the plant", ["they fix nitrogen", "they make the plant flower", "they photosynthesise for the plant"], "They also give resistance to root pathogens."),
      ("Which alcoholic drinks are made by distillation after fermentation?", "whisky, brandy and rum", ["wine and beer", "curd and cheese", "vinegar"], "Wine and beer are not distilled."),
      ("Why are biocontrol methods better than chemical pesticides?", "they are specific and cause less harm to other organisms and the environment", ["they are always cheaper", "they work faster", "they kill all insects"], "Integrated pest management uses them.")]


# =================================================================== 9 biotechnology: principles and processes
G9 = {"a tool of recombinant DNA technology": ["restriction endonuclease", "DNA ligase", "a plasmid vector", "Taq polymerase", "competent host cells"],
      "a feature of a good cloning vector": ["an origin of replication (ori)", "a selectable marker", "a single recognition site for a restriction enzyme"],
      "a selectable marker gene": ["ampicillin resistance (amp<sup>R</sup>)", "tetracycline resistance (tet<sup>R</sup>)", "kanamycin resistance", "lacZ (blue–white selection)"],
      "a method of introducing DNA into host cells": ["heat shock with CaCl₂", "microinjection", "gene gun (biolistics)", "using a disarmed pathogen vector", "electroporation"],
      "a step of PCR": ["denaturation", "annealing of primers", "extension by Taq polymerase"]}
fam(G9, ["a tool of recombinant DNA technology", "a feature of a good cloning vector", "a selectable marker gene"], ["a method of introducing DNA into host cells"], ["a step of PCR"])
P9 = [("EcoRI", "a restriction enzyme from Escherichia coli RY13 that cuts at GAATTC"), ("gel electrophoresis", "separating DNA fragments by size in an agarose gel"), ("ethidium bromide", "staining DNA so it shows orange under UV light"),
      ("elution", "cutting out and recovering DNA bands from a gel"), ("bioreactor", "a large vessel in which cells are grown to make products"), ("downstream processing", "separating and purifying the product before marketing"),
      ("Agrobacterium tumefaciens", "a bacterium that transfers T-DNA into plants"), ("insertional inactivation", "inserting a gene into a marker so the marker stops working")]
B9 = [("Who made the first recombinant DNA?", "Stanley Cohen and Herbert Boyer (1972)", ["Watson and Crick", "Mendel", "Khorana"], "They linked an antibiotic resistance gene to a plasmid."),
      ("What are palindromic sequences?", "DNA sequences that read the same on both strands in the 5′ → 3′ direction", ["sequences with only adenine", "RNA sequences", "repeated proteins"], "Restriction enzymes recognise them."),
      ("What are sticky ends?", "short single-stranded overhangs left when some restriction enzymes cut DNA", ["blunt cuts", "the ends of proteins", "plasmid origins"], "They help DNA ligase join fragments."),
      ("Which way do DNA fragments move in gel electrophoresis?", "towards the anode, because DNA is negatively charged", ["towards the cathode", "they do not move", "upwards"], "Smaller fragments move further."),
      ("Why is Taq polymerase used in PCR?", "it is heat-stable and works after the high-temperature denaturation step", ["it is the fastest", "it cuts DNA", "it joins DNA"], "It comes from Thermus aquaticus."),
      ("Why must cells be made 'competent'?", "so that they can take up foreign DNA", ["so they divide faster", "so they make antibiotics", "so they die"], "Treatment with CaCl₂ and heat shock is used."),
      ("What does blue–white selection show?", "colonies with recombinant plasmids are white because lacZ is inactivated", ["all colonies are blue", "recombinant colonies are blue", "only dead cells are white"], "Non-recombinants make β-galactosidase and turn blue."),
      ("What is a vector?", "a DNA molecule, such as a plasmid, that carries foreign DNA into a host cell", ["a disease-causing insect", "a restriction enzyme", "a ribosome"], "Plasmids and bacteriophages are vectors."),
      ("Which enzyme is used to break the cell wall of fungi before DNA isolation?", "chitinase", ["lysozyme", "cellulase", "ribonuclease"], "Lysozyme for bacteria, cellulase for plant cells."),
      ("How are proteins removed during DNA isolation?", "by treating with protease", ["by heating", "by adding salt only", "by ribonuclease"], "Ribonuclease removes RNA."),
      ("How is purified DNA finally precipitated?", "by adding chilled ethanol", ["by boiling", "by adding water", "by adding salt only"], "It appears as fine threads."),
      ("What is the most commonly used bioreactor?", "the stirred-tank bioreactor", ["the sparger tank", "the beaker", "the petri dish"], "It mixes and aerates the culture.")]


# =================================================================== 10 biotechnology and its applications
G10 = {"a genetically modified crop": ["Bt cotton", "Golden rice (vitamin A rich)", "Bt brinjal", "Flavr Savr tomato"], "a product of recombinant DNA used in medicine": ["human insulin (Humulin)", "human growth hormone", "hepatitis B vaccine", "interferon", "α-1-antitrypsin"],
       "a cry gene": ["cryIAc", "cryIIAb", "cryIAb"], "a use of transgenic animals": ["studying diseases", "making biological products", "testing vaccine safety", "testing chemical safety"]}
fam(G10, ["a genetically modified crop"], ["a product of recombinant DNA used in medicine"], ["a cry gene"], ["a use of transgenic animals"])
P10 = [("Bt cotton", "resisting bollworms with a toxin gene from Bacillus thuringiensis"), ("RNA interference", "silencing a nematode gene to protect tobacco roots from Meloidogyne incognita"), ("Rosie the cow", "producing milk rich in human α-lactalbumin"),
       ("gene therapy", "correcting a gene defect, as first done for ADA deficiency in 1990"), ("Eli Lilly", "the company that made human insulin from E. coli in 1983"), ("GEAC", "the Indian committee that decides on the validity of GM research and release of GM organisms"),
       ("biopiracy", "using bio-resources of a country without proper permission or payment"), ("ELISA", "detecting antigens or antibodies by an antigen–antibody reaction")]
B10 = [("Why does the Bt toxin not kill the bacterium that makes it?", "it is made as an inactive protoxin", ["the bacterium is immune to all toxins", "the toxin is made outside the cell", "it is not a toxin"], "It is activated by the alkaline pH of the insect gut."),
       ("How does the Bt toxin kill insect larvae?", "it becomes active in their alkaline gut, makes pores in gut cells and causes death", ["it poisons the soil", "it starves the plant", "it repels the insect"], "It works on bollworms, beetles and flies."),
       ("How is human insulin made by rDNA technology?", "genes for the A and B chains are put into E. coli; the chains are made separately and joined by disulphide bonds", ["it is taken from pigs", "it is made by yeast only", "it is extracted from human blood"], "This avoids allergy to animal insulin."),
       ("What is the C-peptide?", "an extra stretch in proinsulin that is removed to make mature insulin", ["a part of DNA", "a vaccine", "a type of RNA"], "Insulin is made as a prohormone."),
       ("What was the first clinical gene therapy given for?", "adenosine deaminase (ADA) deficiency", ["diabetes", "cancer", "AIDS"], "In 1990, to a 4-year-old girl."),
       ("Why is early detection of disease by PCR useful?", "it can detect a pathogen when its numbers are very low, before symptoms appear", ["it cures the disease", "it is slower but cheaper", "it only works after symptoms"], "It amplifies tiny amounts of DNA."),
       ("What is a transgenic animal?", "an animal whose DNA has been changed to carry and express a foreign gene", ["an animal from another country", "a cloned animal always", "a wild animal"], "Over 95% are mice."),
       ("Why was Golden rice developed?", "to provide vitamin A (β-carotene) and fight its deficiency", ["to make rice sweeter", "to make rice grow faster", "to make rice yellow for colour"], "It is a biofortified crop."),
       ("What is the advantage of GM crops?", "they can be more tolerant to stress, need less pesticide and give better nutrition", ["they never need water", "they need no soil", "they cannot be eaten"], "They raise concerns that must be checked by bodies like GEAC."),
       ("What is a patent?", "the right given by a government to an inventor to stop others using the invention commercially", ["a disease", "a type of crop", "a vaccine"], "Basmati rice and turmeric patents raised concerns about biopiracy.")]


# =================================================================== 11 organisms and populations
def popn(k=None):
    k = k or ch(["birth", "death", "growth", "density", "net"])
    R = _R[0]
    N0 = R.randint(2, 50) * 20
    if k == "birth":
        b = R.randint(2, 40) * 2
        return A0("A pond has %d lotus plants. Last year %d new plants were added by reproduction. What is the birth rate per plant per year?" % (N0, b), b / N0, [N0 / b, b * N0, b], "", "Birth rate = new individuals ÷ population = %d ÷ %d = <b>%s</b>." % (b, N0, nf(b / N0)))
    if k == "death":
        d = R.randint(1, N0 // 10 or 1)
        return A0("In a laboratory population of %d fruit flies, %d died in a week. What is the death rate per fly per week?" % (N0, d), d / N0, [N0 / d, d * N0, 1 - d / N0], "", "Death rate = deaths ÷ population = <b>%s</b>." % nf(d / N0))
    if k == "growth":
        B_, D, I, E = R.randint(10, 80), R.randint(5, 60), R.randint(0, 30), R.randint(0, 30)
        Nt = N0 + B_ + I - D - E
        return A0("A population of %d deer has %d births, %d immigrants, %d deaths and %d emigrants in a year. What is the population at the end of the year?" % (N0, B_, I, D, E), Nt,
                  [N0 + B_ - D, N0 + B_ + D + I + E, N0 - B_ + D - I + E], "", "N<sub>t+1</sub> = N<sub>t</sub> + (B + I) − (D + E) = <b>%d</b>." % Nt)
    if k == "density":
        n, a = R.randint(20, 500), R.randint(2, 50)
        return A0("A survey counts %d trees of a species in %d hectares. What is the population density?" % (n, a), n / a, [a / n, n * a, n - a], " trees per hectare", "Density = number ÷ area = <b>%s trees per hectare</b>." % nf(n / a))
    r = ch([0.01, 0.02, 0.05, 0.1, 0.015, 0.2])
    return A0("A population of %d grows exponentially with an intrinsic rate of increase r = %s per year. What is its rate of growth (dN/dt) now?" % (N0, nf(r)), r * N0, [N0 / r, r, N0 + r], " per year", "dN/dt = rN = %s × %d = <b>%s per year</b>." % (nf(r), N0, nf(r * N0)))


G11 = {"an example of mutualism": ["lichens (alga and fungus)", "mycorrhizae (fungus and plant roots)", "fig and wasp", "orchid Ophrys and its bee pollinator"],
       "an example of commensalism": ["an orchid growing on a mango branch", "barnacles on a whale", "cattle egrets and grazing cattle", "sea anemone and clownfish"],
       "an example of parasitism": ["Cuscuta on hedge plants", "lice on humans", "the liver fluke", "koel laying eggs in a crow's nest (brood parasitism)"],
       "an example of competition": ["Abingdon tortoise and goats on the Galapagos", "flamingoes and fishes for zooplankton in Andean lakes"],
       "an example of predation": ["a tiger eating a deer", "a sparrow eating seeds", "the prickly pear cactus eaten by a moth in Australia"],
       "a way of coping with unfavourable conditions": ["hibernation (bears)", "aestivation (snails and fish)", "diapause (zooplankton)", "migration (Siberian cranes to Bharatpur)"]}
fam(G11, ["an example of mutualism", "an example of commensalism", "an example of parasitism", "an example of competition", "an example of predation"], ["a way of coping with unfavourable conditions"])
B11 = [("What is the logistic growth curve shaped like?", "an S (sigmoid) curve", ["a J curve", "a straight line", "a U curve"], "Growth levels off at the carrying capacity K."),
       ("What is the exponential growth curve shaped like?", "a J curve", ["an S curve", "a straight line", "a bell curve"], "Resources are assumed unlimited."),
       ("What is carrying capacity (K)?", "the largest population a habitat can support", ["the birth rate", "the death rate", "the number of species"], "Logistic growth: dN/dt = rN(K − N)/K."),
       ("What is Allen's rule?", "mammals in colder climates have shorter ears and limbs to reduce heat loss", ["birds migrate in winter", "plants grow taller in shade", "animals hibernate in summer"], "It is an adaptation."),
       ("Why do people get altitude sickness at high places?", "the low atmospheric pressure means the body gets less oxygen", ["it is too hot", "there is too much oxygen", "the gravity is stronger"], "The body adapts by making more red blood cells."),
       ("What is Gause's competitive exclusion principle?", "two closely related species competing for the same resources cannot live together for long", ["all species share resources equally", "predators help prey", "competition never happens"], "Resource partitioning can allow coexistence."),
       ("What is an age pyramid with a broad base like?", "an expanding population", ["a declining population", "a stable population", "a population with no young"], "Many young individuals."),
       ("What is the effect of predators on prey populations?", "they keep prey numbers under control and help maintain species diversity", ["they always wipe out the prey", "they have no effect", "they increase prey numbers forever"], "Biological control uses this."),
       ("What is the term for animals like most fishes and amphibians whose body temperature changes with the surroundings?", "conformers", ["regulators", "homeotherms", "migrators"], "Regulators keep a constant internal state."),
       ("Why are very small animals rarely found in polar regions?", "they have a large surface area relative to volume and lose heat fast", ["they cannot find food", "they are eaten by bears", "they cannot swim"], "Shrews and hummingbirds are small exceptions in warm places."),
       ("What is the natality rate?", "the number of births in a population over a given time", ["the number of deaths", "the number of immigrants", "the population density"], "Mortality is the number of deaths."),
       ("What is mimicry in monarch butterflies?", "they taste bad because of chemicals from the plants eaten as caterpillars, so birds avoid them", ["they look like leaves", "they are poisonous to touch", "they move very fast"], "A defence against predators.")]


# =================================================================== 12 ecosystem
def eco(k=None):
    k = k or ch(["ten", "npp", "lev"])
    R = _R[0]
    if k == "ten":
        E = R.randint(1, 9) * 10 ** R.randint(3, 5)
        n = R.randint(2, 4)
        lv = {2: "primary consumers (herbivores)", 3: "secondary consumers", 4: "tertiary consumers"}[n]
        return A0("Producers in a food chain fix %s J of energy. Using the 10%% law, how much energy reaches the %s?" % (nf(E), lv), E * 0.1 ** (n - 1), [E * 0.1 ** n, E * 0.1, E / (n * 10)], " J",
                  "Only about 10%% passes to each level: %s × 0.1<sup>%d</sup> = <b>%s J</b>." % (nf(E), n - 1, nf(E * 0.1 ** (n - 1))))
    if k == "npp":
        g = R.randint(10, 90) * 100
        r = R.randint(2, 6) * g // 10
        return A0("An ecosystem has a gross primary productivity of %d kcal m⁻² yr⁻¹ and plants use %d kcal m⁻² yr⁻¹ in respiration. What is the net primary productivity?" % (g, r), g - r, [g + r, r, g / r], " kcal m⁻² yr⁻¹",
                  "NPP = GPP − R = <b>%d kcal m⁻² yr⁻¹</b>." % (g - r))
    E = R.randint(1, 9) * 10
    return A0("Tertiary consumers in a food chain receive %d J. Using the 10%% law, how much energy did the producers fix?" % E, E * 1000, [E * 100, E * 10, E * 10000], " J", "Go back three levels: %d × 10³ = <b>%s J</b>." % (E, nf(E * 1000)))


G12 = {"a producer": ["phytoplankton", "grass", "a tree", "algae"], "a primary consumer": ["grasshopper", "deer", "cow", "zooplankton", "rabbit"], "a secondary consumer": ["frog", "fish eating zooplankton", "wolf", "snake eating frogs"],
       "a decomposer": ["bacteria", "fungi", "earthworm (detritivore)"], "a step of decomposition": ["fragmentation", "leaching", "catabolism", "humification", "mineralisation"],
       "a biotic component": ["plants", "animals", "microorganisms"], "an abiotic component": ["temperature", "water", "light", "soil"]}
fam(G12, ["a producer", "a primary consumer", "a secondary consumer", "a decomposer"], ["a step of decomposition"], ["a biotic component", "an abiotic component"])
PYR = [("the pyramid of energy", "always upright"), ("the pyramid of numbers in a grassland", "upright"), ("the pyramid of numbers in a tree ecosystem", "spindle-shaped (inverted in part)"),
       ("the pyramid of biomass in the sea", "inverted"), ("the pyramid of biomass in a forest", "upright")]
B12 = [("What percentage of photosynthetically active radiation (PAR) do plants capture?", "about 2–10%", ["about 50%", "about 100%", "about 0.01%"], "PAR is about 50% of incident solar radiation."),
       ("What is stratification in a forest?", "vertical layering of plants: trees, shrubs and herbs", ["the soil layers", "the food chain", "the water cycle"], "Each layer has different conditions."),
       ("What is the first link of a detritus food chain?", "dead organic matter (detritus)", ["green plants", "herbivores", "carnivores"], "Decomposers break it down."),
       ("What is ecological succession?", "a gradual, predictable change in the species of an area leading to a climax community", ["a sudden change", "the extinction of species", "the food chain"], "Pioneer species come first."),
       ("Which are the pioneer species on bare rock?", "lichens", ["trees", "grasses", "shrubs"], "They break down rock to form soil."),
       ("What is the climax community?", "the final stable community of a succession", ["the first community", "a community of only animals", "a desert"], "It is in balance with the climate."),
       ("Why is the pyramid of energy always upright?", "energy is lost at each step, so less is available at higher levels", ["energy increases upwards", "all energy is passed on", "animals make energy"], "About 10% passes on."),
       ("Which factors speed up decomposition?", "warm, moist conditions with plenty of oxygen", ["cold, dry conditions", "no oxygen", "high lignin content"], "Detritus rich in chitin and lignin decomposes slowly."),
       ("What is standing crop?", "the mass of living material at each trophic level at a given time", ["the yield of a farm", "dead matter", "the energy flow"], "Measured as biomass or number."),
       ("Why are food chains usually limited to 3–4 trophic levels?", "too little energy is left at higher levels", ["animals cannot eat more", "there is no space", "plants stop growing"], "Most energy is lost as heat."),
       ("What is primary productivity?", "the rate at which producers make biomass by photosynthesis", ["the number of animals", "the rate of decomposition", "the energy of the Sun"], "GPP − respiration = NPP."),
       ("What is humus like?", "dark, amorphous, resistant to microbes and a reservoir of nutrients", ["light and quick to decay", "made only of sand", "a living organism"], "It forms by humification.")]


# =================================================================== 13 biodiversity and conservation
G13 = {"an in-situ conservation method": ["biosphere reserves", "national parks", "wildlife sanctuaries", "sacred groves", "biodiversity hotspots"], "an ex-situ conservation method": ["zoological parks", "botanical gardens", "seed banks", "cryopreservation of gametes", "wildlife safari parks"],
       "a cause of biodiversity loss ('the Evil Quartet')": ["habitat loss and fragmentation", "over-exploitation", "alien species invasions", "co-extinctions"],
       "a recently extinct animal": ["the dodo (Mauritius)", "the quagga (Africa)", "Steller's sea cow (Russia)", "the thylacine (Australia)"], "an alien invasive species in India": ["Parthenium (carrot grass)", "Lantana", "water hyacinth (Eichhornia)", "the African catfish Clarias gariepinus"]}
fam(G13, ["an in-situ conservation method", "an ex-situ conservation method"], ["a cause of biodiversity loss ('the Evil Quartet')"], ["a recently extinct animal", "an alien invasive species in India"])
P13 = [("the Western Ghats and Sri Lanka", "a biodiversity hotspot covering part of India"), ("the Indo-Burma region", "a biodiversity hotspot including north-east India"), ("the Himalaya", "a biodiversity hotspot of India's northern mountains"),
       ("the Earth Summit (Rio de Janeiro, 1992)", "the meeting that called on nations to conserve biodiversity"), ("the World Summit on Sustainable Development (Johannesburg, 2002)", "the meeting where nations pledged to reduce the rate of biodiversity loss"),
       ("Khasi and Jaintia Hills, Meghalaya", "a place with sacred groves"), ("the Amazon rain forest", "the 'lungs of the planet', with the greatest species richness")]
B13 = [("What is the most species-rich group of animals?", "insects", ["mammals", "birds", "fishes"], "More than 70% of all recorded animal species."),
       ("What percentage of the world's land area does India have, and of its species diversity?", "about 2.4% of land and about 8.1% of species", ["10% of land and 2% of species", "50% of both", "1% of both"], "India is one of 12 mega-diversity countries."),
       ("How does species diversity change from the equator to the poles?", "it decreases", ["it increases", "it stays the same", "it is highest at the poles"], "The tropics are the richest."),
       ("What does the species–area relationship of Alexander von Humboldt state?", "species richness increases with area, but only up to a limit", ["species richness falls with area", "area has no effect", "only islands have species"], "log S = log C + Z log A."),
       ("What does the 'rivet popper' hypothesis say?", "losing species is like removing rivets from a plane: losing key ones can make the ecosystem collapse", ["more rivets make planes slower", "species are not linked", "only pests matter"], "Proposed by Paul Ehrlich."),
       ("What are biodiversity hotspots?", "regions with very high species richness and many endemic species, under threat", ["regions with no species", "very hot deserts", "zoos"], "There are 34 hotspots in the world; India has parts of three."),
       ("What are sacred groves?", "forest patches protected by local communities for religious reasons", ["zoos", "botanical gardens", "seed banks"], "Found in Meghalaya, Rajasthan, the Western Ghats and elsewhere."),
       ("What is co-extinction?", "the extinction of a species that depends on another species that has become extinct", ["two species fighting", "a species moving away", "the birth of a new species"], "e.g. a parasite dying with its host."),
       ("Why was the Nile perch harmful in Lake Victoria?", "it led to the extinction of more than 200 species of cichlid fish", ["it cleaned the lake", "it fed people only", "it had no effect"], "An example of alien species invasion."),
       ("What does the IUCN Red List record?", "the conservation status of species and those threatened with extinction", ["new species found", "the best farms", "the number of zoos"], "Updated regularly."),
       ("What is genetic diversity?", "variation in genes within a species, as in thousands of varieties of rice in India", ["variety of ecosystems", "number of species", "variety of habitats"], "e.g. Rauwolfia vomitoria populations differ in reserpine."),
       ("Why should we conserve biodiversity?", "for food, medicines and other products, for ecosystem services, and for ethical reasons", ["only for zoos", "it has no use", "only for tourism"], "Amazon forests make a lot of oxygen.")]

# ------------------------------------------------------------------- more items for larger pools
G2.update({"a stage of early embryo development": ["morula", "blastocyst", "gastrula"],
           "an extra-embryonic membrane": ["amnion", "chorion", "allantois", "yolk sac"]})
fam(G2, ["a part of the male reproductive system", "a part of the female reproductive system"], ["a hormone made by the anterior pituitary", "a hormone made by the placenta", "a hormone made by the ovary"],
    ["a part of a human sperm", "a layer around the ovum"], ["a stage of early embryo development", "an extra-embryonic membrane"])
G3.update({"a hormonal method of contraception": ["oral pills", "injectables", "implants under the skin", "Saheli (once a week)"]})
fam(G3, ["a barrier method of contraception", "a natural method of contraception", "an intra-uterine device (IUD)", "a surgical method of contraception", "a hormonal method of contraception"],
    ["a sexually transmitted infection (STI)"], ["an assisted reproductive technology (ART)"])
B3 += [("What is lactational amenorrhoea?", "the absence of menstruation while a mother fully breastfeeds, which can prevent pregnancy for up to six months after birth", ["a disease of the uterus", "a surgical method", "an STI"], "It works only with intense breastfeeding."),
       ("What is the main side effect risk of unsafe, illegal MTPs?", "they can be dangerous and even fatal when done by unqualified people", ["they have no risk", "they cause twins", "they improve fertility"], "MTP should be done by qualified medical staff."),
       ("What is a test-tube baby?", "a baby born after fertilisation outside the body (IVF) and embryo transfer", ["a baby grown in a test tube", "a cloned baby", "a premature baby"], "The embryo develops in the mother's uterus."),
       ("Why is India's population growth a reproductive health concern?", "a fast-growing population strains health care, food and other resources", ["it has no effect", "it improves health", "it lowers birth rates"], "Awareness and contraception help.")]
G7.update({"a carcinogen": ["X-rays", "ultraviolet radiation", "tobacco smoke", "asbestos"], "a treatment for cancer": ["surgery", "radiotherapy", "chemotherapy", "immunotherapy with α-interferon"],
           "a way of detecting cancer": ["biopsy", "CT scan", "MRI", "blood and bone marrow tests"]})
fam(G7, ["a disease caused by bacteria", "a disease caused by a virus", "a disease caused by a protozoan", "a disease caused by a worm (helminth)", "a disease caused by fungi"], ["a primary lymphoid organ", "a secondary lymphoid organ"], ["an antibody type"],
    ["a carcinogen", "a treatment for cancer", "a way of detecting cancer"])
G8.update({"a drink made by fermentation": ["wine", "beer", "whisky", "brandy", "rum"], "an antibiotic made by microbes": ["penicillin", "streptomycin", "tetracycline", "erythromycin"],
           "an enzyme made by microbes": ["lipase", "streptokinase", "pectinase", "protease"], "a stage of sewage treatment": ["primary treatment (filtering and settling)", "secondary treatment in aeration tanks", "settling of flocs in a settling tank"]})
fam(G8, ["a microbe used in making food", "a microbe that produces an acid or enzyme"], ["a biofertiliser", "a biocontrol agent", "a microbe in sewage treatment or biogas"], ["a drink made by fermentation"],
    ["an antibiotic made by microbes", "an enzyme made by microbes"], ["a stage of sewage treatment"])
G10.update({"a technique of molecular diagnosis": ["PCR", "ELISA", "a DNA probe with autoradiography"], "an Indian plant linked to patent and biopiracy debates": ["Basmati rice", "turmeric", "neem"]})
fam(G10, ["a genetically modified crop"], ["a product of recombinant DNA used in medicine"], ["a cry gene"], ["a use of transgenic animals"], ["a technique of molecular diagnosis"], ["an Indian plant linked to patent and biopiracy debates"])
G13.update({"a level of biodiversity": ["genetic diversity", "species diversity", "ecological diversity"], "an ecosystem service of forests": ["producing oxygen", "pollination", "controlling floods and erosion", "regulating the climate"],
            "an endangered animal of India": ["the Bengal tiger", "the Asiatic lion", "the one-horned rhinoceros", "the Great Indian Bustard"]})
fam(G13, ["an in-situ conservation method", "an ex-situ conservation method"], ["a cause of biodiversity loss ('the Evil Quartet')"], ["a recently extinct animal", "an alien invasive species in India", "an endangered animal of India"],
    ["a level of biodiversity"], ["an ecosystem service of forests"])


def UNITS():
    b = {k: B(globals()["B%d" % k]) for k in range(1, 14)}
    od = {k: OD(globals()["G%d" % k]) for k in range(1, 14) if k != 4}
    od[4] = OD(G4)
    p1 = PR(P1, "What is %s?", "Which term describes this: %s?")
    ploid = PR(PLOID, "What is the ploidy of %s in a flowering plant?", None, pool=["tetraploid (4n)"])
    p2 = PR(P2, "What is the role of the %s?", "Which cell or structure is responsible for %s?")
    p3 = PR(P3, "What is %s?", "Which technique is %s?")
    syn = PR(SYN, "What causes %s?", "Which disorder is caused by %s?")
    sexd = PR(SEXD, "Which mechanism of sex determination is found in %s?", "In which organisms is the sex determined by %s?")
    p5 = PR(P5, "What is %s known for?", "Who is known for %s?")
    p6 = PR(P6, "Which description fits %s?", "Which ancestor of humans is described as having %s?")
    p7 = PR(P7, "Which organism causes %s?", "Which disease is caused by %s?")
    drug = PR(DRUG, "Where do %s come from?", None, pool=["the neem tree", "sugarcane"])
    p8 = PR(P8, "What is %s?", "Which product is %s?")
    p9 = PR(P9, "What is %s?", "Which term matches this description: %s?")
    p10 = PR(P10, "What is %s known for?", "Which term or product matches this: %s?")
    pyr = PR(PYR, "What is the shape of %s?", None, pool=["circular"])
    p13 = PR(P13, "What is %s known as?", "Which place or event is %s?")
    S = lambda *a, **kw: SU(BIO, *a, **kw)
    return [
        S(25, "sexual-reproduction-in-flowering-plants", 1,
          "Flower structure; development of male and female gametophytes; pollination – types, agencies and examples; out breeding devices; pollen–pistil interaction; double fertilization; post fertilization events – development of endosperm and embryo, development of seed and formation of fruit; special modes – apomixis, parthenocarpy, polyembryony; significance of seed dispersal and fruit formation.",
          "Sexual Reproduction in Flowering Plants", "sexual reproduction in flowering plants",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 1 Sexual Reproduction in Flowering Plants: stamen and pistil, pollen and embryo sac, pollination, outbreeding devices, double fertilisation, seeds, fruits and apomixis. 100 questions with answers.",
          "Double fertilisation: syngamy + triple fusion.", "Endosperm is triploid; the zygote is diploid.",
          "<p>The stamen (anther and filament) makes pollen grains, each with a vegetative cell and a generative cell inside a tough exine of sporopollenin. The pistil (stigma, style, ovary) holds ovules; a megaspore develops into a 7-celled, 8-nucleate embryo sac. Pollen reaches the stigma by self-pollination (autogamy, geitonogamy) or cross-pollination (xenogamy) carried by wind, water or animals; outbreeding devices prevent selfing.</p>"
          "<p>In double fertilisation one male gamete fuses with the egg (syngamy, forming the zygote) and the other with the two polar nuclei (triple fusion, forming the triploid endosperm). The ovule becomes the seed and the ovary the fruit. Apomixis gives seeds without fertilisation; parthenocarpy gives seedless fruits.</p>",
          [("Ploidy of the endosperm?", ["2 polar nuclei + 1 gamete"], "3n"), ("Pollen to another flower on the same plant?", ["same plant"], "geitonogamy")],
          ["Calling geitonogamy cross-pollination genetically.", "Saying the embryo sac has 8 cells.", "Mixing up the coleoptile and coleorhiza."],
          [("What is double fertilisation?", "Syngamy (male gamete + egg) and triple fusion (male gamete + two polar nuclei) taking place in the same embryo sac."),
           ("What are outbreeding devices?", "Ways flowers avoid self-pollination, such as dichogamy, self-incompatibility and unisexual flowers.")],
          lambda: [("Flower and gametophytes", [(od[1], 14), (b[1], 6)]), ("Pollination", [(od[1], 12), (p1, 6), (b[1], 2)]), ("Outbreeding devices and pollen–pistil interaction", [(od[1], 14), (b[1], 2), (p1, 4)]),
                   ("Double fertilisation", [(ploid, 6), (p1, 6), (b[1], 2), (od[1], 6)]), ("Seeds, fruits and apomixis", [(od[1], 20)])]),
        S(26, "human-reproduction", 2,
          "Male and female reproductive systems; microscopic anatomy of testis and ovary; gametogenesis – spermatogenesis and oogenesis; menstrual cycle; fertilisation, embryo development up to blastocyst formation, implantation; pregnancy and placenta formation (elementary idea); parturition (elementary idea); lactation (elementary idea).",
          "Human Reproduction", "human reproduction",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 2 Human Reproduction: male and female reproductive systems, gametogenesis, the menstrual cycle, fertilisation, implantation, placenta, parturition and lactation. 100 questions with answers.",
          "Spermatogenesis gives four sperms; oogenesis gives one ovum.", "LH surge → ovulation; progesterone keeps the uterus ready.",
          "<p>The testes make sperms (spermatogenesis) and testosterone; Sertoli cells nourish developing sperms and Leydig cells make hormones. The ovaries make ova (oogenesis), one ovum and polar bodies from each primary oocyte. In the 28-day menstrual cycle FSH and oestrogen build the follicle and endometrium, an LH surge causes ovulation around day 14, and the corpus luteum makes progesterone.</p>"
          "<p>Fertilisation usually happens in the ampulla of the oviduct. The zygote divides to form a blastocyst that implants in the endometrium; the placenta exchanges materials and makes hormones such as hCG. Parturition is helped by oxytocin, and lactation provides colostrum rich in antibodies.</p>",
          [("100 primary spermatocytes → sperms?", ["× 4"], "400"), ("Hormone surge for ovulation?", ["mid-cycle"], "LH")],
          ["Saying one primary oocyte gives four ova.", "Putting fertilisation in the uterus.", "Mixing up Sertoli and Leydig cells."],
          [("What happens in the menstrual cycle if the egg is not fertilised?", "The corpus luteum breaks down, progesterone falls and the endometrium is shed as menstruation."),
           ("Where does fertilisation take place in humans?", "Usually in the ampulla of the fallopian tube (oviduct).")],
          lambda: [("Reproductive systems", [(od[2], 14), (b[2], 6)]), ("Gametogenesis", [(K(cyc, "sperm"), 8), (od[2], 8), (b[2], 4)]), ("The menstrual cycle", [(K(cyc, "ov"), 6), (od[2], 10), (b[2], 1), (p2, 3)]),
                   ("Fertilisation and implantation", [(p2, 10), (od[2], 10)]), ("Pregnancy, birth and lactation", [(p2, 3), (K(cyc, "days"), 4), (od[2], 13)])]),
        S(27, "reproductive-health", 3,
          "Need for reproductive health and prevention of Sexually Transmitted Diseases (STDs); birth control – need and methods, contraception and medical termination of pregnancy (MTP); amniocentesis; infertility and assisted reproductive technologies – IVF, ZIFT, GIFT (elementary idea for general awareness).",
          "Reproductive Health", "reproductive health",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 3 Reproductive Health: reproductive health programmes, contraceptive methods, MTP, sexually transmitted infections, infertility and assisted reproductive technologies. 100 questions with answers.",
          "Reproductive health means physical, emotional, social and behavioural well-being.", "Contraceptives can be natural, barrier, IUD, hormonal or surgical.",
          "<p>Reproductive health covers all aspects of reproduction: physical, emotional, behavioural and social well-being. India's RCH programmes spread awareness about safe practices, family planning and preventing sexually transmitted infections (STIs), many of which can be prevented by safe practices and treated if found early.</p>"
          "<p>Contraceptive methods include natural methods, barriers (condoms, diaphragms), IUDs such as Copper T, hormonal pills and surgical methods (vasectomy, tubectomy). Infertile couples can be helped by assisted reproductive technologies such as IVF, ZIFT, GIFT, ICSI and artificial insemination.</p>",
          [("Copper T is a?", ["placed in the uterus"], "intra-uterine device"), ("Embryo up to 8 cells into oviduct?", ["zygote transfer"], "ZIFT")],
          ["Thinking all STIs are curable.", "Calling vasectomy a temporary method.", "Mixing up ZIFT and GIFT."],
          [("How do IUDs work?", "They increase sperm phagocytosis in the uterus, and copper ions reduce sperm movement; hormonal IUDs make the uterus unsuitable for implantation."),
           ("What is IVF?", "Fertilising an ovum outside the body in the laboratory and transferring the embryo into the woman's body.")],
          lambda: [("Reproductive health in India", [(b[3], 6), (od[3], 14)]), ("Contraception", [(od[3], 16), (b[3], 4)]), ("Sexually transmitted infections", [(od[3], 17), (b[3], 3)]),
                   ("Infertility and ART", [(p3, 7), (od[3], 13)]), ("Mixed questions", [(od[3], 18), (p3, 2)])]),
        S(28, "principles-of-inheritance-and-variation", 4,
          "Heredity and variation: Mendelian inheritance; deviations from Mendelism – incomplete dominance, co-dominance, multiple alleles and inheritance of blood groups, pleiotropy; elementary idea of polygenic inheritance; chromosome theory of inheritance; chromosomes and genes; sex determination – in human being, birds and honey bee; linkage and crossing over; sex linked inheritance – haemophilia, colour blindness; Mendelian disorders in humans – thalassemia; chromosomal disorders in humans; Down's syndrome, Turner's and Klinefelter's syndromes.",
          "Principles of Inheritance and Variation", "principles of inheritance",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 4 Principles of Inheritance and Variation: monohybrid and dihybrid crosses, test crosses, incomplete dominance, blood groups, sex determination, linkage and genetic disorders. 100 questions with answers.",
          "Monohybrid F₂: 3 : 1; dihybrid F₂: 9 : 3 : 3 : 1.", "Test cross with the homozygous recessive reveals the genotype.",
          "<p>Mendel's pea crosses showed dominance, segregation and independent assortment: a monohybrid F₂ is 3 : 1 (genotypes 1 : 2 : 1) and a dihybrid F₂ is 9 : 3 : 3 : 1. A test cross with the recessive parent gives 1 : 1 if the plant is heterozygous. Some traits show incomplete dominance (pink snapdragons), codominance and multiple alleles (ABO blood groups), pleiotropy or polygenic inheritance.</p>"
          "<p>Genes lie on chromosomes and linked genes tend to be inherited together. Sex is determined by XX–XY in humans, ZW–ZZ in birds and haplodiploidy in honey bees. Disorders may be Mendelian (haemophilia, sickle-cell anaemia, phenylketonuria) or chromosomal (Down's, Turner's, Klinefelter's syndromes).</p>",
          [("Tt × Tt, 400 offspring. Dwarf?", ["¼ × 400"], "100"), ("RrYy × RrYy, 160 seeds. Wrinkled green?", ["1/16 × 160"], "10")],
          ["Writing 3 : 1 for genotypes.", "Thinking blood group O is dominant.", "Saying the mother decides the sex of a human child."],
          [("What is a test cross?", "Crossing an organism of unknown genotype with a homozygous recessive one; a 1 : 1 result shows it is heterozygous."),
           ("What is codominance?", "Both alleles are fully expressed in the heterozygote, as I<sup>A</sup> and I<sup>B</sup> in blood group AB.")],
          lambda: [("Monohybrid crosses", [(K(gen, "mono", "test"), 16), (b[4], 4)]), ("Dihybrid crosses", [(K(gen, "di", "back"), 16), (b[4], 4)]), ("Deviations from Mendel", [(K(gen, "inc", "blood"), 12), (od[4], 6), (b[4], 2)]),
                   ("Chromosomes, sex and linkage", [(sexd, 6), (b[4], 1), (od[4], 13)]), ("Genetic disorders", [(syn, 9), (od[4], 11)])]),
        S(29, "molecular-basis-of-inheritance", 5,
          "Search for genetic material and DNA as genetic material; structure of DNA and RNA; DNA packaging; DNA replication; central dogma; transcription, genetic code, translation; gene expression and regulation – lac operon; Genome, Human and rice genome projects; DNA fingerprinting.",
          "Molecular Basis of Inheritance", "molecular basis of inheritance",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 5 Molecular Basis of Inheritance: DNA structure, Chargaff's rules, replication, transcription, the genetic code, translation, the lac operon, the Human Genome Project and DNA fingerprinting. 100 questions with answers.",
          "DNA → RNA → protein (central dogma).", "A pairs with T (or U), G with C; each codon has three bases.",
          "<p>DNA is a double helix of two antiparallel strands, with adenine paired to thymine (two hydrogen bonds) and guanine to cytosine (three); base pairs are 0.34 nm apart. Griffith, Avery and Hershey–Chase showed DNA is the genetic material; Meselson and Stahl showed replication is semi-conservative. DNA polymerase works 5′ → 3′, making Okazaki fragments on the lagging strand.</p>"
          "<p>Transcription copies a gene into RNA; in eukaryotes introns are spliced out. Translation reads mRNA codons on ribosomes; the triplet code is degenerate, universal and starts at AUG. The lac operon switches genes on when lactose is present. DNA fingerprinting uses VNTRs.</p>",
          [("30% A. % G?", ["(100 − 60) ÷ 2"], "20%"), ("Complementary to ATGC?", ["A–T, G–C"], "TACG")],
          ["Pairing A with G.", "Counting the stop codon as an amino acid.", "Saying the genetic code overlaps."],
          [("What is semi-conservative replication?", "Each new DNA double helix keeps one original strand and has one newly made strand."),
           ("How does the lac operon work?", "Without lactose a repressor blocks the operator; lactose (the inducer) removes it so the genes for lactose use are transcribed.")],
          lambda: [("DNA structure", [(T(BI.m_chargaff), 8), (K(mol, "len", "bp"), 6), (b[5], 6)]), ("The search for the genetic material", [(p5, 12), (od[5], 6), (b[5], 2)]), ("Replication", [(T(BI.m_dna), 12), (od[5], 4), (b[5], 2), (K(mol, "bp"), 2)]),
                   ("Transcription and the genetic code", [(T(BI.m_mrna), 12), (K(mol, "codon", "aa"), 6), (b[5], 1), (od[5], 1)]), ("Gene regulation and genomes", [(od[5], 12), (p5, 2), (K(mol, "len"), 6)])]),
        S(30, "evolution", 6,
          "Origin of life; biological evolution and evidences for biological evolution (paleontology, comparative anatomy, embryology and molecular evidences); Darwin's contribution, modern synthetic theory of evolution; mechanism of evolution – variation (mutation and recombination) and natural selection with examples, types of natural selection; gene flow and genetic drift; Hardy–Weinberg's principle; adaptive radiation; human evolution.",
          "Evolution", "evolution",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 6 Evolution: origin of life, evidence for evolution, homologous and analogous organs, natural selection, Hardy–Weinberg principle, adaptive radiation and human evolution. 100 questions with answers.",
          "Natural selection: variation + survival of the fittest.", "Hardy–Weinberg: p² + 2pq + q² = 1.",
          "<p>The Miller–Urey experiment showed that organic molecules could form from simple gases. Evidence for evolution comes from fossils, homologous organs (divergent evolution), analogous organs (convergent evolution), embryology and molecules. Darwin explained evolution by natural selection acting on heritable variation; examples include industrial melanism and antibiotic resistance.</p>"
          "<p>The Hardy–Weinberg principle says allele frequencies stay constant (p² + 2pq + q² = 1) unless gene flow, genetic drift, mutation, recombination or natural selection act. Adaptive radiation produced Darwin's finches and Australian marsupials. Human evolution runs from Dryopithecus and Australopithecus through Homo habilis and Homo erectus to Homo sapiens.</p>",
          [("q² = 0.09. q?", ["√0.09"], "0.3"), ("Wings of bird and butterfly?", ["similar function"], "analogous organs")],
          ["Calling homologous organs analogous.", "Saying individuals evolve.", "Forgetting 2pq for heterozygotes."],
          [("What is the difference between homologous and analogous organs?", "Homologous organs have the same basic structure but different functions (common ancestry); analogous organs have the same function but different structures (convergent evolution)."),
           ("What does the Hardy–Weinberg principle state?", "Allele and genotype frequencies in a population stay constant from generation to generation if no evolutionary forces act.")],
          lambda: [("Origin of life and evidence", [(b[6], 5), (od[6], 15)]), ("Natural selection", [(od[6], 12), (b[6], 2), (T(BI.m_hw), 6)]), ("Hardy–Weinberg principle", [(T(BI.m_hw), 18), (b[6], 2)]),
                   ("Adaptive radiation and drift", [(od[6], 14), (T(BI.m_hw), 6)]), ("Human evolution", [(p6, 7), (od[6], 13)])]),
        S(31, "human-health-and-disease", 7,
          "Pathogens; parasites causing human diseases (malaria, dengue, chikungunya, filariasis, ascariasis, typhoid, pneumonia, common cold, amoebiasis, ring worm) and their control; basic concepts of immunology – vaccines; cancer, HIV and AIDS; adolescence – drug and alcohol abuse.",
          "Human Health and Disease", "human health and disease",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 7 Human Health and Disease: common diseases and their pathogens, malaria, immunity and antibodies, vaccines, AIDS, cancer, and drug and alcohol abuse. 100 questions with answers.",
          "Each disease has its own pathogen and way of spreading.", "Active immunity: own antibodies; passive: ready-made antibodies.",
          "<p>Infectious diseases are caused by bacteria (typhoid, pneumonia), viruses (common cold, dengue, AIDS), protozoans (malaria, amoebiasis), worms (ascariasis, filariasis) and fungi (ringworm). Malaria is spread by the female Anopheles mosquito, and Plasmodium multiplies in the liver and red blood cells.</p>"
          "<p>The body defends itself with innate immunity and acquired immunity; B-lymphocytes make antibodies and T-lymphocytes give cell-mediated immunity. Vaccines give active immunity. HIV destroys helper T cells, causing AIDS. Cancer is uncontrolled cell division. Drugs and alcohol harm health and cause dependence, so adolescents should avoid them and seek help.</p>",
          [("Typhoid is caused by?", ["a bacterium"], "Salmonella typhi"), ("Antibodies from mother's milk?", ["ready-made"], "passive immunity")],
          ["Calling malaria a viral disease.", "Saying vaccines give passive immunity.", "Thinking antibiotics cure the common cold."],
          [("What is the difference between active and passive immunity?", "In active immunity the body makes its own antibodies after infection or vaccination; in passive immunity ready-made antibodies are given."),
           ("How does HIV cause AIDS?", "It infects and destroys helper T-lymphocytes, so the immune system weakens and other infections take hold.")],
          lambda: [("Diseases and pathogens", [(od[7], 12), (p7, 8)]), ("Malaria and other diseases", [(p7, 6), (b[7], 6), (od[7], 8)]), ("Immunity", [(od[7], 16), (b[7], 4)]),
                   ("AIDS and cancer", [(b[7], 2), (od[7], 18)]), ("Drugs and alcohol", [(drug, 3), (od[7], 17)])]),
        S(32, "microbes-in-human-welfare", 8,
          "Microbes in food processing, industrial production, sewage treatment, energy generation and microbes as bio-control agents and bio-fertilizers. Antibiotics; production and judicious use.",
          "Microbes in Human Welfare", "microbes in human welfare",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 8 Microbes in Human Welfare: microbes in household foods, industrial products, antibiotics, sewage treatment, biogas, biocontrol agents and biofertilisers. 100 questions with answers.",
          "Microbes make curd, bread, cheese, antibiotics, enzymes and biogas.", "Biofertilisers and biocontrol agents reduce chemical use.",
          "<p>Lactobacillus turns milk into curd, yeast makes dough rise and gives alcohol, and other microbes make cheeses. Industries use microbes to make acids (citric, acetic, lactic), enzymes (lipases, streptokinase), antibiotics such as penicillin, cyclosporin A and statins.</p>"
          "<p>In sewage treatment, aerobic bacteria in flocs lower the BOD, and anaerobic bacteria in digesters make biogas, mostly methane. Biocontrol agents such as Bt, Trichoderma and baculoviruses control pests; biofertilisers such as Rhizobium, Azotobacter, cyanobacteria and mycorrhizae enrich the soil.</p>",
          [("Microbe for curd?", ["lactic acid bacteria"], "Lactobacillus"), ("Main gas in biogas?", ["from methanogens"], "methane")],
          ["Saying biogas is mostly CO₂.", "Calling Rhizobium a biocontrol agent.", "Thinking wine is distilled."],
          [("What is BOD?", "The amount of oxygen bacteria would use to oxidise the organic matter in one litre of water; it measures pollution."),
           ("Why are biofertilisers useful?", "They add nutrients such as nitrogen and phosphorus to soil naturally, reducing the use of chemical fertilisers.")],
          lambda: [("Microbes in household products", [(od[8], 14), (b[8], 6)]), ("Industrial products", [(p8, 9), (od[8], 11)]), ("Sewage treatment and biogas", [(b[8], 3), (od[8], 17)]),
                   ("Biocontrol agents", [(od[8], 18), (p8, 2)]), ("Biofertilisers", [(od[8], 20)])]),
        S(33, "biotechnology-principles-and-processes", 9,
          "Genetic engineering (Recombinant DNA technology).",
          "Biotechnology: Principles and Processes", "biotechnology principles and processes",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 9 Biotechnology: Principles and Processes: restriction enzymes, vectors, selectable markers, gel electrophoresis, PCR, transformation, bioreactors and downstream processing. 100 questions with answers.",
          "Cut with a restriction enzyme, join with DNA ligase, carry with a vector.", "PCR: denaturation → annealing → extension; DNA doubles each cycle.",
          "<p>Recombinant DNA technology cuts DNA with restriction enzymes (such as EcoRI, which cuts at GAATTC and leaves sticky ends), joins it into a vector with DNA ligase and puts it into a competent host. A good vector has an origin of replication, selectable markers such as antibiotic resistance, and a cloning site; insertional inactivation of lacZ gives white recombinant colonies.</p>"
          "<p>Fragments are separated by gel electrophoresis (smaller ones move further towards the anode) and seen with ethidium bromide. PCR copies DNA in cycles of denaturation, primer annealing and extension by heat-stable Taq polymerase, doubling it each cycle. Products are made in bioreactors and purified by downstream processing.</p>",
          [("2 molecules after 5 PCR cycles?", ["2 × 2⁵"], "64"), ("Enzyme that joins DNA?", ["seals the backbone"], "DNA ligase")],
          ["Saying DNA moves to the cathode.", "Forgetting that DNA doubles in every PCR cycle.", "Thinking blue colonies are recombinant."],
          [("Why is Taq polymerase used in PCR?", "It comes from a hot-spring bacterium and is not destroyed at the high temperature used to separate the DNA strands."),
           ("What is insertional inactivation?", "Putting the foreign gene inside a marker gene so the marker stops working, which shows which colonies are recombinant.")],
          lambda: [("Tools of genetic engineering", [(od[9], 12), (b[9], 6), (p9, 2)]), ("Vectors and markers", [(od[9], 13), (b[9], 3), (p9, 4)]), ("Gel electrophoresis", [(T(BI.m_biotech, "gel"), 12), (p9, 6), (od[9], 2)]),
                   ("PCR", [(T(BI.m_biotech, "pcr", "pcrn"), 16), (od[9], 4)]), ("Introducing DNA and bioreactors", [(od[9], 16), (p9, 1), (T(BI.m_biotech, "gel"), 3)])]),
        S(34, "biotechnology-and-its-applications", 10,
          "Application of biotechnology in health and agriculture: genetically modified organisms – Bt crops; transgenic animals; biosafety issues, biopiracy and patents.",
          "Biotechnology and its Applications", "biotechnology and its applications",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 10 Biotechnology and its Applications: Bt crops, RNA interference, genetically engineered insulin, gene therapy, molecular diagnosis, transgenic animals, biosafety, patents and biopiracy. 100 questions with answers.",
          "Bt crops make their own insect-killing protein.", "Recombinant DNA gives insulin, vaccines and gene therapy.",
          "<p>In agriculture, Bt cotton carries cry genes from Bacillus thuringiensis whose protoxin becomes active in the alkaline gut of insect larvae. RNA interference protects tobacco from nematodes. Golden rice is rich in vitamin A. In medicine, E. coli makes human insulin (A and B chains joined by disulphide bonds), gene therapy treated ADA deficiency, and PCR and ELISA allow early diagnosis.</p>"
          "<p>Transgenic animals are used to study diseases and make products such as α-lactalbumin-rich milk (Rosie the cow). In India GEAC decides on the safety of GM research. Patents and biopiracy raise questions about the use of a nation's bio-resources.</p>",
          [("Bt toxin gene for bollworms?", ["cry"], "cryIAc"), ("First gene therapy?", ["1990"], "ADA deficiency")],
          ["Saying the Bt toxin kills the bacterium that makes it.", "Calling a cloned animal transgenic.", "Thinking insulin is made as one chain in E. coli."],
          [("How does Bt cotton resist pests?", "It makes an inactive Bt protoxin that becomes active in the alkaline gut of bollworms and kills them."),
           ("What is RNA interference?", "Silencing a specific mRNA with complementary double-stranded RNA, used to protect tobacco roots from nematodes.")],
          lambda: [("Biotechnology in agriculture", [(od[10], 10), (b[10], 4), (p10, 4), (T(BI.m_biotech, "gel"), 2)]), ("Biotechnology in medicine", [(od[10], 10), (p10, 4), (T(BI.m_biotech, "pcrn"), 3), (T(BI.m_biotech, "pcr"), 3)]),
                   ("Transgenic animals", [(od[10], 12), (p10, 3), (T(BI.m_biotech, "pcr"), 3), (b[10], 2)]), ("Ethics, patents and biopiracy", [(od[10], 14), (T(BI.m_biotech, "gel"), 6)]), ("Mixed questions", [(od[10], 14), (b[10], 1), (p10, 2), (T(BI.m_biotech, "gel"), 3)])]),
        S(35, "organisms-and-populations", 11,
          "Population interactions – mutualism, competition, predation, parasitism; population attributes – growth, birth rate and death rate, age distribution.",
          "Organisms and Populations", "organisms and populations",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 11 Organisms and Populations: population density, birth and death rates, growth models, age pyramids, adaptations and population interactions. 100 questions with answers.",
          "N(t+1) = N(t) + (B + I) − (D + E).", "Exponential growth is J-shaped; logistic growth is S-shaped.",
          "<p>A population has attributes such as density, birth rate (natality), death rate (mortality), sex ratio and age distribution. Its size changes as N<sub>t+1</sub> = N<sub>t</sub> + (B + I) − (D + E). With unlimited resources growth is exponential (dN/dt = rN, a J curve); with limited resources it is logistic (an S curve) and levels off at the carrying capacity K.</p>"
          "<p>Species interact by mutualism (+/+), competition (−/−), predation and parasitism (+/−), commensalism (+/0) and amensalism (−/0). Organisms cope with unfavourable conditions by migration, hibernation, aestivation or diapause.</p>",
          [("N = 1000, B = 80, D = 50, I = 10, E = 20?", ["1000 + 90 − 70"], "1020"), ("Orchid on mango branch?", ["+/0"], "commensalism")],
          ["Forgetting immigration and emigration.", "Calling a lichen parasitism.", "Saying logistic growth is J-shaped."],
          [("What is carrying capacity?", "The largest population size that a habitat's resources can support."),
           ("What is mutualism?", "An interaction in which both species benefit, such as lichens and mycorrhizae.")],
          lambda: [("Population attributes", [(K(popn, "birth", "death", "density"), 14), (b[11], 4), (od[11], 2)]), ("Population growth", [(K(popn, "growth", "net"), 16), (b[11], 3), (od[11], 1)]), ("Adaptations", [(od[11], 10), (b[11], 2), (T(BI.m_pop, "lincoln"), 8)]),
                   ("Population interactions", [(od[11], 18), (K(popn, "growth"), 2)]), ("Mixed questions", [(od[11], 12), (K(popn, "birth", "death", "density", "growth", "net"), 8)])]),
        S(36, "ecosystem", 12,
          "Ecosystems: patterns, components; productivity and decomposition; energy flow; pyramids of number, biomass, energy.",
          "Ecosystem", "ecosystem",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 12 Ecosystem: components, productivity, decomposition, food chains, energy flow and the 10% law, and ecological pyramids. 100 questions with answers.",
          "Only about 10% of energy passes to the next trophic level.", "NPP = GPP − respiration.",
          "<p>An ecosystem has biotic (producers, consumers, decomposers) and abiotic components. Primary productivity is the rate at which producers make organic matter; NPP = GPP − R. Decomposition (fragmentation, leaching, catabolism, humification, mineralisation) recycles nutrients and is fastest when warm and moist.</p>"
          "<p>Energy flows one way from the Sun through producers to consumers; at each step only about 10% passes on (the 10% law), so food chains are short and the pyramid of energy is always upright. Pyramids of number and biomass can be inverted, as for biomass in the sea.</p>",
          [("Producers 10,000 J. Secondary consumers?", ["× 0.1²"], "100 J"), ("GPP 5000, R 2000. NPP?", ["GPP − R"], "3000")],
          ["Saying energy is recycled in ecosystems.", "Thinking every pyramid is upright.", "Adding respiration to get NPP."],
          [("Why is the pyramid of energy always upright?", "Energy is lost as heat at each level, so each higher level always has less energy."),
           ("What is the 10% law?", "Only about 10% of the energy at one trophic level is passed to the next.")],
          lambda: [("Ecosystem components", [(od[12], 16), (b[12], 4)]), ("Productivity", [(K(eco, "npp"), 14), (b[12], 3), (T(BI.m_energy, "gpp", "npp"), 2), (od[12], 1)]), ("Decomposition", [(od[12], 14), (b[12], 2), (K(eco, "npp"), 4)]),
                   ("Energy flow", [(K(eco, "ten", "lev"), 18), (T(BI.m_energy, "eff"), 2)]), ("Ecological pyramids", [(pyr, 3), (od[12], 13), (K(eco, "ten"), 4)])]),
        S(37, "biodiversity-and-conservation", 13,
          "Biodiversity – concept, patterns, importance; loss of biodiversity; biodiversity conservation; hotspots, endangered organisms, extinction, Red Data Book, Sacred Groves, biosphere reserves, national parks, wildlife sanctuaries and Ramsar sites.",
          "Biodiversity and Conservation", "biodiversity and conservation",
          "Free CBSE Class 12 Biology worksheets for NCERT Chapter 13 Biodiversity and Conservation: levels and patterns of biodiversity, the species–area relationship, causes of loss, hotspots, and in-situ and ex-situ conservation. 100 questions with answers.",
          "Biodiversity: genetic, species and ecological.", "In-situ: protect in the wild; ex-situ: protect outside the natural home.",
          "<p>Biodiversity exists at the genetic, species and ecological levels. It is highest in the tropics and falls towards the poles; species richness rises with area up to a limit (Humboldt's species–area relationship). India has about 2.4% of the world's land but about 8.1% of its species.</p>"
          "<p>The main causes of biodiversity loss are habitat loss and fragmentation, over-exploitation, alien species invasions and co-extinctions — the 'Evil Quartet'. Conservation is in-situ (biosphere reserves, national parks, sanctuaries, sacred groves, hotspots) or ex-situ (zoos, botanical gardens, seed banks, cryopreservation).</p>",
          [("Seed bank is?", ["outside the habitat"], "ex-situ conservation"), ("Cichlids lost in Lake Victoria due to?", ["alien species"], "the Nile perch")],
          ["Calling zoos in-situ conservation.", "Saying biodiversity rises towards the poles.", "Thinking hotspots have few endemic species."],
          [("What is the 'Evil Quartet'?", "The four main causes of biodiversity loss: habitat loss and fragmentation, over-exploitation, alien species invasions and co-extinctions."),
           ("What is in-situ conservation?", "Protecting species in their natural habitats, as in national parks, sanctuaries and biosphere reserves.")],
          lambda: [("Levels and patterns of biodiversity", [(b[13], 5), (od[13], 15)]), ("Loss of biodiversity", [(od[13], 17), (b[13], 3)]), ("Hotspots and sacred groves", [(p13, 9), (od[13], 11)]),
                   ("In-situ and ex-situ conservation", [(od[13], 18), (p13, 2)]), ("Mixed questions", [(od[13], 19), (b[13], 1)])]),
    ]
