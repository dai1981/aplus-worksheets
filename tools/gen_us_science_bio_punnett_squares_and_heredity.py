# -*- coding: utf-8 -*-
"""
US High School Biology: Punnett Squares and Heredity (HS-LS3-3)
  python tools/gen_us_science_bio_punnett_squares_and_heredity.py
Apply concepts of statistics and probability to explain the variation and distribution of expressed traits in a population.
Monohybrid crosses (genotype and phenotype probabilities, expected numbers), dihybrid 9:3:3:1, incomplete dominance,
codominance and ABO blood types, X-linked traits, and comparing expected with observed offspring.
Wrong answers come from real mistakes: "Aa x Aa gives 50% recessive", "a carrier shows the trait",
"probabilities change after earlier births".
"""
from fractions import Fraction
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90114)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


TRAITS = [("pea plants", "P", "purple flowers", "white flowers"), ("pea plants", "T", "tall stems", "short stems"), ("pea plants", "Y", "yellow seeds", "green seeds"),
          ("guinea pigs", "B", "black fur", "white fur"), ("rabbits", "F", "brown fur", "white fur"), ("fruit flies", "W", "normal wings", "vestigial wings"),
          ("tomato plants", "R", "red fruit", "yellow fruit"), ("dogs", "S", "short hair", "long hair"), ("corn", "G", "green leaves", "albino leaves")]
GEN = ["AA", "Aa", "aa"]


def cross(g1, g2):
    kids = [tuple(sorted(x + y, key=lambda c: (c.lower(), c.islower()))) for x in g1 for y in g2]
    return ["".join(k) for k in kids]


def ps_table(g1, g2, L):
    a, b = [L if c == "A" else L.lower() for c in g1], [L if c == "A" else L.lower() for c in g2]
    rows = [[b[0]] + ["".join(sorted(b[0] + x, key=lambda c: (c.lower(), c.islower()))) for x in a], [b[1]] + ["".join(sorted(b[1] + x, key=lambda c: (c.lower(), c.islower()))) for x in a]]
    return table([""] + a, rows)


def gname(g, L):
    return g.replace("A", L).replace("a", L.lower())


def pct(f):
    return "%g%%" % float(f * 100)


def g_mono():
    org, L, dom, rec = R.choice(TRAITS)
    g1, g2 = R.choice(GEN), R.choice(GEN)
    k = R.choice(["rec", "dom", "het", "homo"])
    if not once((org, L, g1, g2, k)) or not once((g1, g2, k), 3):
        return None
    kids = cross(g1, g2)
    nrec = sum(1 for x in kids if x == "aa")
    nhet = sum(1 for x in kids if x == "Aa")
    nhomo = sum(1 for x in kids if x == "AA")
    pic = ps_table(g1, g2, L)
    if k == "rec":
        a = Fraction(nrec, 4)
        q = "What is the chance an offspring has %s?" % rec
    elif k == "dom":
        a = Fraction(4 - nrec, 4)
        q = "What is the chance an offspring has %s?" % dom
    elif k == "het":
        a = Fraction(nhet, 4)
        q = "What is the chance an offspring is heterozygous (%s)?" % gname("Aa", L)
    else:
        a = Fraction(nhomo, 4)
        q = "What is the chance an offspring is homozygous dominant (%s)?" % gname("AA", L)
    w = [pct(Fraction(x, 4)) for x in range(5) if Fraction(x, 4) != a]
    R.shuffle(w)
    return item(pic + "In %s, %s (%s) is dominant over %s (%s). A %s parent is crossed with a %s parent. %s" % (org, dom, L, rec, L.lower(), gname(g1, L), gname(g2, L), q),
                pct(a), w[:3], "Count the boxes: %d of 4." % int(a * 4))


def g_expect():
    org, L, dom, rec = R.choice(TRAITS)
    g1, g2 = R.choice([("Aa", "Aa"), ("Aa", "aa"), ("AA", "Aa")])
    n = R.choice([40, 80, 100, 120, 200, 400, 600, 1000])
    if not once((org, L, g1, g2, n)):
        return None
    kids = cross(g1, g2)
    f = Fraction(sum(1 for x in kids if x == "aa"), 4)
    if f == 0:
        f = Fraction(sum(1 for x in kids if x == "Aa"), 4)
        what = "heterozygous (%s)" % gname("Aa", L)
    else:
        what = "with %s" % rec
    a = int(n * f)
    return item("Two %s %s are crossed and produce %s offspring. About how many are %s?" % (gname(g1, L) + " and " + gname(g2, L), org, comma(n), what), comma(a),
                [comma(n // 2) if a != n // 2 else comma(n // 4 * 3), comma(n - a), comma(int(n * f / 2))], "%s × %s = %s." % (comma(n), pct(f), comma(a)))


def g_ratio():
    org, L, dom, rec = R.choice(TRAITS)
    g1, g2 = R.choice([("Aa", "Aa"), ("Aa", "aa"), ("AA", "aa"), ("AA", "Aa")])
    if not once(("r", org, L, g1, g2)):
        return None
    kids = cross(g1, g2)
    d = sum(1 for x in kids if x != "aa")
    r_ = 4 - d
    a = "%d %s : %d %s" % (d, dom, r_, rec) if r_ else "all %s" % dom
    opts = ["3 %s : 1 %s" % (dom, rec), "1 %s : 1 %s" % (dom, rec), "all %s" % dom, "1 %s : 3 %s" % (dom, rec)]
    a = {"3 1": opts[0], "2 2": opts[1], "4 0": opts[2]}["%d %d" % (d, r_)]
    return item("Cross: %s × %s %s (%s dominant). What phenotype ratio do you expect?" % (gname(g1, L), gname(g2, L), org, dom), a, [o for o in opts if o != a], "Use a Punnett square.")


def g_blood():
    pairs = [("AO", "BO"), ("AA", "BB"), ("AO", "AO"), ("AB", "OO"), ("BO", "OO"), ("AB", "AB"), ("AA", "OO"), ("AO", "BB")]
    g1, g2 = R.choice(pairs)
    types = {}
    for x in g1:
        for y in g2:
            s = set(x + y) - {"O"} or {"O"}
            t = "AB" if s == {"A", "B"} else s.pop()
            types[t] = types.get(t, 0) + 1
    t = R.choice(["A", "B", "AB", "O"])
    if not once((g1, g2, t)):
        return None
    f = Fraction(types.get(t, 0), 4)
    w = [pct(Fraction(x, 4)) for x in range(5) if Fraction(x, 4) != f]
    R.shuffle(w)
    nm = lambda g: "I<sup>%s</sup>%s" % (g[0], "i" if g[1] == "O" else "I<sup>%s</sup>" % g[1]) if g[0] != "O" else "ii"
    return item("ABO blood type: A and B are codominant, O is recessive. Parents' genotypes are %s and %s. What is the chance of a child with type %s blood?" % (nm(g1), nm(g2), t),
                pct(f), w[:3], "Make a Punnett square and count type %s." % t)


def g_inc():
    who = P.next()[0]
    k = R.choice(["pink", "red", "white", "ratio"])
    p = R.choice([("red", "white", "pink", "snapdragons"), ("red", "white", "pink", "four o'clock flowers"), ("black", "white", "gray", "chickens (Andalusian)")])
    if not once((p, k)):
        return None
    big, small, mid, org = p
    if k == "ratio":
        return item("In %s, %s × %s gives all %s offspring (incomplete dominance). Two %s ones are crossed. Ratio?" % (org, big, small, mid, mid),
                    "1 %s : 2 %s : 1 %s" % (big, mid, small), ["3 %s : 1 %s" % (big, small), "all %s" % mid, "1 %s : 1 %s" % (big, small)], "Like Rr × Rr: 1 RR : 2 Rr : 1 rr.")
    f = {"pink": "50%", "red": "25%", "white": "25%"}[k]
    col = {"pink": mid, "red": big, "white": small}[k]
    return item("In %s, two %s parents are crossed (incomplete dominance). What percent of offspring are %s?" % (org, mid, col), f, [x for x in ["0%", "25%", "50%", "75%", "100%"] if x != f][:3],
                "1 : 2 : 1, so %s are %s." % (f, col))


def g_xlink():
    who = P.next()[0]
    case = R.choice([("carrier", "normal"), ("carrier", "colorblind"), ("normal", "colorblind")])
    q = R.choice(["son", "daughter"])
    if not once((case, q)):
        return None
    mom, dad = case
    # sons get mom's X; daughters get one from each
    if q == "son":
        f = {"carrier": Fraction(1, 2), "normal": Fraction(0)}[mom]
    else:
        f = {("carrier", "normal"): Fraction(0), ("carrier", "colorblind"): Fraction(1, 2), ("normal", "colorblind"): Fraction(0)}[case]
    w = [pct(x) for x in [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)] if x != f]
    return item("Red-green color blindness is X-linked recessive. The mother is %s and the father is %s. What is the chance a %s is color-blind?" % (
        "a carrier" if mom == "carrier" else "not a carrier", "color-blind" if dad == "colorblind" else "not color-blind", q), pct(f), w,
        "Sons get their X from their mother; daughters get one X from each parent.")


B1 = bank([
    ("What is a genotype?", "the alleles an organism has, like Aa", ["the trait you can see", "the number of chromosomes", "a kind of cell"], "Genes, not looks."),
    ("What is a phenotype?", "the trait you can observe", ["the alleles", "the DNA sequence only", "the number of genes"], "What it looks like."),
    ("What does homozygous mean?", "two identical alleles (AA or aa)", ["two different alleles", "no alleles", "three alleles"], "Same + same."),
    ("What does heterozygous mean?", "two different alleles (Aa)", ["two identical alleles", "one allele", "no dominant allele"], "Different."),
    ("What is a dominant allele?", "an allele that shows its trait when one copy is present", ["an allele that only shows with two copies", "the most common allele", "a mutated allele"], "Capital letter."),
    ("A carrier of a recessive disorder has which genotype?", "heterozygous (Aa)", ["homozygous recessive (aa)", "homozygous dominant (AA)", "no alleles"], "Carriers do not show the trait."),
    ("Each child of Aa × Aa parents has what chance of being aa?", "25%, every time", ["25% only for the first child", "50%", "0% after an aa child"], "Each birth is independent."),
    ("What does a Punnett square show?", "the possible allele combinations in offspring and their chances", ["the exact offspring that will be born", "a cell dividing", "a food web"], "Probability, not a promise."),
])
B5 = bank([
    ("Mendel crossed tall Tt plants and counted 787 tall and 277 short. What ratio is this close to?", "3 : 1", ["1 : 1", "1 : 2 : 1", "9 : 3 : 3 : 1"], "787 ÷ 277 ≈ 2.8."),
    ("A dihybrid cross AaBb × AaBb gives what phenotype ratio?", "9 : 3 : 3 : 1", ["3 : 1", "1 : 1 : 1 : 1", "1 : 2 : 1"], "Two traits, independent."),
    ("A breeder wants to know if a black dog is BB or Bb. Which cross is a good test?", "cross it with a recessive (bb) dog", ["cross it with another BB dog", "cross it with a cat", "look at its fur only"], "A test cross."),
    ("Why do observed numbers rarely match expected ratios exactly?", "Chance; small samples vary more.", ["Punnett squares are wrong.", "Genes change every birth.", "Ratios only work in peas."], "Larger samples get closer."),
    ("Two brown-eyed parents have a blue-eyed child. What are the parents' genotypes (brown dominant)?", "both heterozygous (Bb)", ["both homozygous dominant (BB)", "one BB and one bb", "both homozygous recessive (bb)"], "Each passed a b allele."),
])


def body():
    think = ("<p><b>Each parent gives one allele; a Punnett square shows the chances.</b></p>%s"
             "<ul><li>Aa × Aa: 25%% AA, 50%% Aa, 25%% aa → 3 dominant : 1 recessive.</li>"
             "<li>Expected number = total × probability. Real counts vary by chance.</li>"
             "<li>Other patterns: incomplete dominance (1 : 2 : 1), codominance (AB blood), X-linked traits.</li></ul>") % ps_table("Aa", "Aa", "A")
    ex = [("Aa × aa. Chance of aa?", ["Squares: Aa, Aa, aa, aa"], "50%"),
          ("Aa × Aa, 200 offspring. About how many aa?", ["25% of 200"], "50")]
    mist = ["Saying Aa × Aa gives 50% recessive. It is 25%.", "Thinking a carrier (Aa) shows a recessive trait.", "Thinking chances change after earlier births."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Genotypes and phenotypes", B1 + [(g_mono, 8), (g_ratio, 4)]),
        ("Monohybrid crosses", [(g_mono, 14), (g_ratio, 6)]),
        ("Expected numbers", [(g_expect, 14), (g_mono, 6)]),
        ("Other inheritance patterns", [(g_inc, 7), (g_blood, 8), (g_xlink, 5)]),
        ("Probability in populations", B5 + [(g_blood, 7), (g_expect, 6), (g_inc, 2)]),
    ])
    make("biology", "punnett-squares-and-heredity", 14, "HS-LS3-3",
         "Apply concepts of statistics and probability to explain the variation and distribution of expressed traits in a population.",
         "Punnett Squares and Heredity",
         "Punnett Square Worksheets: Genotype, Phenotype and Probability (High School Biology)",
         "Punnett Squares",
         "Free high school biology worksheets on Punnett squares and heredity (NGSS HS-LS3-3): genotype and phenotype probabilities, expected numbers, incomplete dominance, blood types and X-linked traits. 100 questions with answers.",
         "Punnett squares show the chances.",
         "Each parent gives one allele; expected number = total × probability.",
         body(),
         [("How do you use a Punnett square?", "Write one parent's alleles across the top and the other's down the side, fill in each box, then count boxes to find probabilities."),
          ("What ratio does Aa × Aa give?", "Genotypes 1 AA : 2 Aa : 1 aa, and phenotypes 3 dominant : 1 recessive."),
          ("Why don't real results match exactly?", "Each offspring is a chance event. Larger samples usually come closer to the expected ratio.")],
         sets)


if __name__ == "__main__":
    main()
