# -*- coding: utf-8 -*-
"""
US High School Biology: Changes in Trait Frequency (HS-LS4-3)
  python tools/gen_us_science_bio_changes_in_trait_frequency.py
Apply concepts of statistics and probability to support explanations that organisms with an advantageous heritable
trait tend to increase in proportion to organisms lacking this trait.
Percent of a population with a trait, survival rates, allele frequencies (p and q) from genotype counts, average trait
values over generations, and directional, stabilizing and disruptive selection.
Wrong answers come from real mistakes: "count individuals, not alleles", "a higher count means a higher rate",
"averages never shift".
"""
from fractions import Fraction
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90117)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def dec(x):
    s = "%.2f" % x
    return s


def g_pct():
    who = P.next()[0]
    sp, tr = R.choice([("beetles", "green"), ("rabbits", "white"), ("snails", "striped"), ("moths", "dark"), ("lizards", "long-legged"), ("guppies", "spotted"),
                       ("sparrows", "long-winged"), ("crickets", "silent")])
    n = R.choice([20, 25, 40, 50, 80, 200, 250, 400, 500])
    k = R.randint(1, 19) * n // 20
    if k == 0 or k == n or not once(("p", sp, n, k)):
        return None
    pc = Fraction(100 * k, n)
    if pc.denominator != 1:
        return None
    pc = int(pc)
    if R.random() < 0.6:
        return item("%s counted %d %s. %d of them were %s. What percent were %s?" % (who, n, sp, k, tr, tr), "%d%%" % pc,
                    ["%d%%" % (100 - pc), "%d%%" % k, "%d%%" % (pc + 10 if pc <= 85 else pc - 15)], "%d ÷ %d × 100 = %d%%." % (k, n, pc))
    return item("In a population of %d %s, %d%% are %s. How many %s %s are there (%s's survey)?" % (n, sp, pc, tr, tr, sp, who), str(k),
                [str(n - k), str(pc), str(k + n // 10)], "%d%% of %d = %d." % (pc, n, k))


def g_prob():
    who = P.next()[0]
    sp, a, b, why = R.choice([("mice", "dark", "light", "on dark lava rock"), ("moths", "dark", "light", "on sooty bark"), ("beetles", "brown", "green", "on brown soil"),
                              ("fish", "dull", "bright", "in a lake with herons"), ("frogs", "green", "yellow", "in a green pond"), ("hares", "white", "brown", "in deep snow")])
    na, nb = R.choice([100, 200, 400, 500]), R.choice([100, 200, 400, 500])
    ra, rb = R.choice([40, 50, 60, 70, 75, 80]), R.choice([10, 20, 25, 30])
    sa, sb = na * ra // 100, nb * rb // 100
    k = R.choice(["rate", "better", "count", "trap"])
    if not once(("pr", na, nb, ra, rb, k)) or (k == "better" and not once(("bt", sp), 1)) or (k == "trap" and (sb <= sa or not once(("tp", sp), 1))):
        return None
    tab = table(["%s %s" % (sp.capitalize(), why), "Released", "Survived"], [[a, str(na), str(sa)], [b, str(nb), str(sb)]])
    if k == "rate":
        return item(tab + "What percent of the %s %s survived in %s's study?" % (a, sp, who), "%d%%" % ra, ["%d%%" % rb, "%d%%" % (100 - ra), "%d%%" % (sa // 10)],
                    "%d ÷ %d × 100 = %d%%." % (sa, na, ra))
    if k == "count":
        return item(tab + "How many %s %s survived in %s's study?" % (b, sp, who), str(sb), [str(nb), str(sa), str(nb - sb)], "Read the Survived column.")
    if k == "trap":
        return item(tab + "More %s %s survived than %s %s. Does that mean the %s trait is an advantage?" % (b, sp, a, sp, b),
                    "No. Compare survival rates: %d%% of %s survived but only %d%% of %s." % (ra, a, rb, b),
                    ["Yes, more survived, so it is better.", "Yes, counts are all that matter.", "There is no way to tell from rates."], "Use rates, not raw counts, when group sizes differ.")
    return item(tab + "Which trait gives an advantage %s, based on %s's survival rates?" % (why, who), a, [b, "Neither trait.", "Both equally."], "%d%% vs %d%%." % (ra, rb))


def g_freq():
    who = P.next()[0]
    n = R.choice([50, 100, 200])
    AA = R.randint(1, n // 2)
    Aa = R.randint(1, n - AA - 1)
    aa = n - AA - Aa
    if aa <= 0:
        return None
    p = Fraction(2 * AA + Aa, 2 * n)
    if (p * 100).denominator != 1:
        return None
    k = R.choice(["p", "q", "dom"])
    if not once(("fq", AA, Aa, aa, k)):
        return None
    tab = table(["Genotype", "Number of individuals"], [["AA", str(AA)], ["Aa", str(Aa)], ["aa", str(aa)]])
    if k == "p":
        w = [dec(Fraction(AA, n)), dec(Fraction(AA + Aa, n)), dec(1 - p)]
        return item(tab + "%s sampled %d plants. What is the frequency of allele A?" % (who, n), dec(p), w,
                    "Alleles: 2 × %d + %d = %d A out of %d. %d ÷ %d = %s." % (AA, Aa, 2 * AA + Aa, 2 * n, 2 * AA + Aa, 2 * n, dec(p)))
    if k == "q":
        q = 1 - p
        w = [dec(Fraction(aa, n)), dec(p), dec(Fraction(aa + Aa, n))]
        return item(tab + "In %s's sample of %d snails, what is the frequency of allele a?" % (who, n), dec(q), w,
                    "a alleles: 2 × %d + %d = %d out of %d = %s." % (aa, Aa, 2 * aa + Aa, 2 * n, dec(q)))
    c = AA + Aa
    return item(tab + "A is dominant. How many of %s's %d mice show the dominant trait?" % (who, n), str(c), [str(AA), str(Aa), str(aa)], "AA and Aa both show it: %d + %d = %d." % (AA, Aa, c))


SEL = [("In a dry area, taller cacti survive better, and the population gets taller each generation.", 0),
       ("Very small and very large human babies have lower survival than medium-sized babies.", 1),
       ("In a lake, small-beaked and large-beaked birds survive, but medium beaks cannot handle either seed type.", 2),
       ("Over many years, giraffes with longer necks reach more leaves and leave more offspring.", 0),
       ("Galls made by flies are attacked by wasps if small and by birds if large, so medium galls survive best.", 1),
       ("Rock pocket mice on dark lava become darker over many generations.", 0),
       ("Salmon: large males fight for mates and tiny males sneak in, but medium males do poorly.", 2),
       ("Clutch size in a bird: too few eggs means few chicks, too many means chicks starve, so medium clutches do best.", 1),
       ("Bacteria exposed to an antibiotic become more resistant each generation.", 0),
       ("Snails on both light sand and dark rock: light and dark shells survive, but medium shells stand out in both.", 2),
       ("Moths with average wing size fly best; very short or very long wings are selected against.", 1),
       ("Hunters target the largest elk antlers, and average antler size shrinks.", 0),
       ("A plant has two pollinators: one visits short flowers and one visits long flowers, so in-between flowers set less seed.", 2),
       ("Fish with medium body size survive best in a stream with both fast current and predators.", 1)]
SN = ["directional selection", "stabilizing selection", "disruptive selection", "genetic drift (random change)"]


def g_select():
    s, k = R.choice(SEL)
    if not once(("se", s)):
        return None
    return item("%s Which type of selection is this?" % s, SN[k], [x for x in SN if x != SN[k]],
                ["One extreme is favored, so the average shifts.", "The middle is favored, so variation shrinks.", "Both extremes are favored, so the population splits."][k])


def g_mean():
    who = P.next()[0]
    tr, unit, sp = R.choice([("beak depth", "mm", "finches"), ("body length", "cm", "lizards"), ("leg length", "mm", "toads"), ("antler length", "cm", "elk"), ("shell thickness", "mm", "snails")])
    k = R.choice(["mean", "shift"])
    if k == "mean":
        v = R.sample(range(8, 30), 5)
        if sum(v) % 5 or not once(("mn", tuple(sorted(v)))):
            return None
        m = sum(v) // 5
        return item("%s measured the %s of 5 %s: %s %s. What is the mean?" % (who, tr, sp, ", ".join(map(str, v)), unit), "%d %s" % (m, unit),
                    ["%d %s" % (sum(v), unit), "%d %s" % (sorted(v)[2] if sorted(v)[2] != m else m + 1, unit), "%d %s" % (max(v) - min(v), unit)], "Add (%d) and divide by 5." % sum(v))
    b = R.randint(20, 60)
    d = R.randint(2, 9)
    g = R.randint(2, 6)
    if not once(("sh", b, d, g)):
        return None
    tab = table(["Generation", "Average %s (%s)" % (tr, unit)], [["1", str(b)], [str(g), str(b + d)]])
    if R.random() < 0.5:
        return item(tab + "In %s's population of %s, by how much did the average %s change?" % (who, sp, tr), "%d %s" % (d, unit),
                    ["%d %s" % (b + d, unit), "%d %s" % (d * g, unit), "0 %s" % unit], "%d − %d = %d." % (b + d, b, d))
    return item(tab + "In %s's %s, what does the change in the average %s suggest?" % (who, sp, tr), "Individuals with greater %s left more offspring." % tr,
                ["Every individual grew during its life.", "The trait is not inherited.", "There was no selection at all."], "The average shifted in one direction.")


B1 = bank([
    ("What is an allele frequency?", "the fraction of all copies of a gene in a population that are one allele", ["the number of individuals with a trait", "how often a gene mutates", "the size of a population"], "Count alleles, not individuals."),
    ("What does it mean when a population evolves?", "The frequencies of alleles or traits change over generations.", ["One animal changes its traits.", "The population gets bigger.", "Nothing changes."], "Evolution is genetic change in populations."),
    ("If an advantageous trait is inherited, what happens to its proportion over time?", "It tends to increase.", ["It tends to decrease.", "It stays the same.", "It disappears."], "Carriers leave more offspring."),
    ("Why do scientists use percentages instead of counts?", "to compare groups of different sizes", ["because counts are always wrong", "to make numbers bigger", "because percents are random"], "Rates are fair comparisons."),
    ("In a population with alleles A and a, p is the frequency of A. What is q?", "q = 1 − p", ["q = p", "q = 2p", "q = p²"], "p + q = 1."),
    ("What is directional selection?", "selection that favors one extreme of a trait", ["selection that favors the average", "selection that favors both extremes", "random change"], "The average shifts."),
    ("What is stabilizing selection?", "selection that favors the average trait", ["selection that favors one extreme", "selection that favors both extremes", "no selection"], "Variation shrinks."),
    ("What is disruptive selection?", "selection that favors both extremes over the average", ["selection that favors the average", "selection that favors one extreme", "random change"], "The population may split."),
])
B5 = bank([
    ("A sample of 5 moths shows more dark moths. Why is this weak evidence?", "The sample is too small to be reliable.", ["Five is plenty.", "Dark moths are always rare.", "Samples do not matter."], "Large samples reduce chance."),
    ("Two populations start at 10% for a helpful trait. Which data best support selection?", "The trait rises steadily to 60% over many generations.", ["It jumps up and down at random.", "It stays at 10%.", "It drops to 0%."], "A steady increase."),
    ("Why do scientists repeat survival experiments several times?", "to check that the result is not due to chance", ["to make the animals tired", "to change the answer", "for no reason"], "Repeated trials."),
    ("A trait increases from 20% to 25% in one generation. What else would strengthen the claim of selection?", "data from more generations and a reason the trait helps survival", ["a photo of one animal", "a smaller sample", "a guess"], "Pattern plus mechanism."),
    ("In a bar graph of beak sizes, the whole curve moves to larger sizes. Which selection does this show?", "directional", ["stabilizing", "disruptive", "none"], "One direction."),
])


def body():
    think = ("<p><b>Helpful inherited traits become a bigger share of the population.</b></p>"
             "<ul><li>Use rates and percents, not raw counts, to compare groups.</li>"
             "<li>Allele frequency: count alleles. Each AA has 2 A, each Aa has 1 A. p + q = 1.</li>"
             "<li>Directional selection shifts the average; stabilizing favors the middle; disruptive favors both ends.</li></ul>")
    ex = [("100 plants: 36 AA, 48 Aa, 16 aa. Frequency of A?", ["A alleles: 72 + 48 = 120", "120 ÷ 200"], "0.60"),
          ("Dark mice: 60 of 100 survived. Light: 40 of 200. Better trait?", ["60% vs 20%"], "dark fur")]
    mist = ["Counting individuals instead of alleles.", "Comparing raw counts when the groups are different sizes.", "Thinking each animal changes during its life."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Trait percents", B1 + [(g_select, 6), (g_pct, 6)]),
        ("Survival rates", [(g_prob, 12), (g_pct, 8)]),
        ("Allele frequencies", [(g_freq, 14), (g_select, 6)]),
        ("Averages and selection", [(g_mean, 12), (g_prob, 4), (g_freq, 4)]),
        ("Statistical evidence", B5 + [(g_mean, 5), (g_freq, 5), (g_prob, 5)]),
    ])
    make("biology", "changes-in-trait-frequency", 17, "HS-LS4-3",
         "Apply concepts of statistics and probability to support explanations that organisms with an advantageous heritable trait tend to increase in proportion to organisms lacking this trait.",
         "Changes in Trait Frequency",
         "Trait Frequency Worksheets: Allele Frequencies, Survival Rates and Selection (Biology)",
         "Trait Frequency",
         "Free high school biology worksheets on changes in trait frequency (NGSS HS-LS4-3): percents, survival rates, allele frequencies and directional, stabilizing and disruptive selection. 100 questions with answers.",
         "Helpful traits become more common.",
         "Use rates, percents and allele frequencies to show the change.",
         body(),
         [("How do you find an allele frequency?", "Count the copies of the allele (AA has 2, Aa has 1) and divide by the total number of alleles, which is twice the number of individuals."),
          ("Why compare rates instead of counts?", "Groups often have different sizes. A rate such as percent surviving gives a fair comparison."),
          ("What are the three types of selection?", "Directional selection favors one extreme, stabilizing selection favors the average and disruptive selection favors both extremes.")],
         sets)


if __name__ == "__main__":
    main()
