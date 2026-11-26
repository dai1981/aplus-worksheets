# -*- coding: utf-8 -*-
"""
US High School Biology: Natural Selection and Adaptation (HS-LS4-2, HS-LS4-4)
  python tools/gen_us_science_bio_natural_selection_and_adaptation.py
Construct an explanation based on evidence that the process of evolution primarily results from four factors:
(1) the potential for a species to increase in number, (2) the heritable genetic variation of individuals due to
mutation and sexual reproduction, (3) competition for limited resources, and (4) the proliferation of those organisms
that are better able to survive and reproduce. Construct an explanation of how natural selection leads to adaptation.
Peppered moths, antibiotic and pesticide resistance, Galápagos finch beaks, rock pocket mice; trait data over generations.
Wrong answers come from real mistakes: "individuals change because they need to" (Lamarck), "the strongest always win",
"traits acquired during life are inherited".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90116)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


FACT = ["more offspring than can survive", "heritable variation", "competition for limited resources", "better-adapted individuals survive and reproduce more"]
FSC = [("A cod lays millions of eggs, but only a few grow up.", 0), ("One oak tree drops thousands of acorns each year.", 0), ("A pair of rabbits can have over 30 young in a year.", 0),
       ("Some beetles in a population are green and some are brown, and color is passed to offspring.", 1), ("A mutation gives a few bacteria a gene that breaks down an antibiotic.", 1),
       ("Siblings from the same parents have different beak sizes.", 1), ("Deer in a crowded forest struggle to find enough food in winter.", 2),
       ("Seedlings in a thick forest compete for sunlight.", 2), ("Only a few nesting sites are on a small island, and many birds want them.", 2),
       ("Moths that match the tree bark are eaten less and leave more offspring.", 3), ("Mice with fur that matches the ground have more pups that survive.", 3),
       ("Finches with deep beaks crack the hard seeds in a drought and raise more chicks.", 3)]


def g_factor():
    s, k = R.choice(FSC)
    if not once(("f", s)):
        return None
    return item("%s Which factor of natural selection does this show?" % s, FACT[k], [x for x in FACT if x != FACT[k]], "The four factors: overproduction, variation, competition and differential survival.")


SCEN = [("In England, soot darkened tree bark in the 1800s. Dark peppered moths became more common.", "Dark moths were hidden from birds, so they survived and reproduced more.",
         "The moths turned dark because they needed to hide."),
        ("A doctor's patient stops taking antibiotics early. The infection comes back and the drug no longer works.", "Resistant bacteria survived and multiplied.",
         "The bacteria learned to resist the drug."),
        ("A farmer sprays the same insecticide for years. It kills fewer insects each year.", "Insects with resistance genes survived and passed them on.",
         "Each insect got used to the spray."),
        ("After a drought on a Galápagos island, only large, hard seeds were left. The next generation of finches had deeper beaks.", "Finches with deeper beaks survived to breed.",
         "Each finch's beak grew to fit the seeds."),
        ("On dark lava rock, most rock pocket mice have dark fur. On light sand nearby, most have light fur.", "Mice that match the ground are seen less by owls and leave more young.",
         "The mice changed color to match where they live."),
        ("Snowshoe hares with white winter coats survive better in snowy areas.", "White hares are harder for predators to see in snow, so more survive.",
         "Hares choose their color each year."),
        ("Cane toads spread across Australia. Toads at the front of the spread now have longer legs.", "Toads with longer legs reached new areas first and bred there.",
         "Toads stretched their legs by hopping, and their young inherited it."),
        ("Some HIV viruses in a patient change their surface proteins and escape a drug.", "Variants the drug cannot stop survive and multiply.",
         "The virus decides to change.")]


def g_scen():
    s, a, lam = R.choice(SCEN)
    k = R.random() < 0.6
    if not once(("s", s, k)):
        return None
    if k:
        return item("%s Which explanation is best?" % s, a, [lam, "The environment does not affect which individuals survive.", "All individuals changed in the same way during their lives."],
                    "Natural selection acts on traits that are already present and inherited.")
    return item("%s A student says: “%s” What is wrong with this claim?" % (s, lam), "Individuals do not change their genes to meet a need; selection acts on existing variation.",
                ["Nothing is wrong.", "Only plants evolve.", "Evolution is too slow to see."], "That is Lamarck's idea, not natural selection.")


def g_data():
    who = P.next()[0]
    gen = [0, 5, 10, 15, 20]
    sp, tr, env = R.choice([("peppered moths", "dark", "soot darkens the trees"), ("beetles", "brown", "the soil turns darker"),
                            ("mice", "dark", "lava rock covers the area"), ("bacteria", "resistant", "an antibiotic is used"),
                            ("lizards", "long-legged", "the habitat has more open ground"), ("fish", "dull-colored", "predators move into the lake")])
    a = R.randint(5, 25)
    v = [a]
    for _ in range(4):
        v.append(min(98, v[-1] + R.randint(8, 22)))
    k = R.choice(["trend", "change", "read", "why"])
    if not once(("d", sp, tuple(v), k)) or (k in ("trend", "why") and not once((k, sp), 1)):
        return None
    tab = table(["Generation", "%% of %s that are %s" % (sp, tr)], [[str(g), "%d%%" % x] for g, x in zip(gen, v)])
    if k == "trend":
        return item(tab + "After %s, %s tracked a population of %s. What do the data show?" % (env, who, sp), "The %s trait became more common." % tr,
                    ["The %s trait became less common." % tr, "The trait stayed the same.", "The %s trait disappeared." % tr], "The percent rises each time.")
    if k == "change":
        i, j = sorted(R.sample(range(5), 2))
        return item(tab + "By how many percentage points did %s %s rise from generation %d to %d (%s's data)?" % (tr, sp, gen[i], gen[j], who), str(v[j] - v[i]),
                    [str(v[j]), str(v[i] + v[j]), str(v[j] - v[i] + 4)], "%d − %d = %d." % (v[j], v[i], v[j] - v[i]))
    if k == "read":
        i = R.randint(1, 4)
        return item(tab + "In %s's data, what percent of the %s were %s in generation %d?" % (who, sp, tr, gen[i]), "%d%%" % v[i],
                    ["%d%%" % v[i - 1], "%d%%" % (100 - v[i]), "%d%%" % (v[i] + 3)], "Read the row for generation %d." % gen[i])
    return item(tab + "After %s, why did the %s %s become more common in %s's data?" % (env, tr, sp, who), "They survived and reproduced more, passing on the trait.",
                ["Each individual changed during its life.", "They chose to change.", "The trait has no effect on survival."], "Differential reproduction.")


def g_beak():
    who = P.next()[0]
    b = R.randint(85, 95) / 10
    d = R.randint(3, 8) / 10
    a = round(b + d, 1)
    k = R.choice(["diff", "why", "pred"])
    if not once(("b", b, d, k)) or (k != "diff" and not once(("bk", k), 3)):
        return None
    tab = table(["Year", "Average beak depth of medium ground finches (mm)"], [["before drought", "%.1f" % b], ["after drought", "%.1f" % a]])
    if k == "diff":
        return item(tab + "By how many millimeters did the average beak depth change in %s's data?" % who, "%.1f mm" % d,
                    ["%.1f mm" % (d + 0.2), "%.1f mm" % a, "%.1f mm" % (b + a)], "%.1f − %.1f = %.1f." % (a, b, d))
    if k == "why":
        return item(tab + "In %s's study, only large, hard seeds were left after the drought. Why did the average beak get deeper?" % who,
                    "Birds with deeper beaks ate more, survived and had more chicks.", ["Each bird's beak grew from cracking seeds.", "Birds chose deeper beaks.", "Rain made beaks grow."],
                    "Selection on existing variation.")
    return item(tab + "In %s's study, rainy years return and small, soft seeds become common again. What is likely to happen to beak depth over the next generations?" % who,
                "It is likely to decrease again.", ["It will keep increasing forever.", "It cannot change again.", "All finches will lose their beaks."], "Selection follows the environment.")


def g_resist():
    who = P.next()[0]
    n = R.choice([1000, 2000, 5000, 10000, 20000, 50000])
    p = R.choice([1, 2, 4, 5, 10])
    r = n * p // 100
    k = R.choice(["left", "killed", "pct"])
    if not once(("r", n, p, k)):
        return None
    if k == "left":
        return item("%s's sample has %s bacteria. %d%% of them have a resistance gene. An antibiotic kills all the others. How many bacteria are left?" % (who, comma(n), p), comma(r),
                    [comma(n - r), comma(n), comma(r * 10)], "%d%% of %s = %s." % (p, comma(n), comma(r)))
    if k == "killed":
        return item("%s bacteria are in a culture, and %d%% are resistant. An antibiotic kills every non-resistant cell. How many are killed (%s's lab)?" % (comma(n), p, who), comma(n - r),
                    [comma(r), comma(n), comma(n + r)], "%s − %s = %s." % (comma(n), comma(n), comma(r)) if False else "%s − %s = %s." % (comma(n), comma(r), comma(n - r)))
    return item("After an antibiotic, the %s survivors in %s's culture are all resistant and multiply. What percent of the new population is resistant?" % (comma(r), who), "about 100%",
                ["%d%%" % p, "50%", "0%"], "Only resistant cells were left to reproduce.")


B1 = bank([
    ("What is natural selection?", "Individuals with helpful inherited traits survive and reproduce more.", ["Individuals change to fit their needs.", "Only the strongest survive.", "Animals choose their traits."], "Differential survival and reproduction."),
    ("What is an adaptation?", "an inherited trait that helps an organism survive and reproduce in its environment", ["a change an animal makes during its life", "any trait at all", "a learned habit"], "Shaped by selection."),
    ("What does 'fitness' mean in evolution?", "how well an organism survives and reproduces", ["how strong it is", "how fast it runs", "how much it exercises"], "Measured in offspring."),
    ("What are the sources of heritable variation?", "mutation and sexual reproduction", ["exercise and diet", "learning", "the weather only"], "New alleles and new combinations."),
    ("Does natural selection act on individuals or populations?", "It acts on individuals, but populations evolve.", ["Individuals evolve during their lives.", "Neither.", "Only on species."], "Allele frequencies change."),
    ("A weightlifter builds big muscles. Will her children inherit them?", "No. Acquired traits are not inherited.", ["Yes, always.", "Only her sons.", "Only if she keeps training."], "Only genes are inherited."),
    ("Why do species produce more offspring than can survive?", "It leads to competition, so only some survive to reproduce.", ["So every one survives.", "It has no effect.", "To stop evolution."], "Overproduction."),
    ("Which trait is most likely to be selected for in a cold climate?", "thick fur that is inherited", ["a sunburn", "a cut paw", "a learned trick"], "Heritable and helpful."),
])
B5 = bank([
    ("Why do doctors tell patients to finish all their antibiotics?", "to kill the bacteria before resistant ones can multiply", ["to make the bacteria stronger", "because the pills taste good", "to cause mutations"], "Prevents selection for resistance."),
    ("Why can't natural selection make a trait that is not in the population?", "Selection only acts on variation that already exists.", ["It can make any trait it needs.", "Traits appear when needed.", "Animals invent traits."], "Mutation supplies new variation."),
    ("A trait that helps in one environment harms in another. What does this show?", "Fitness depends on the environment.", ["Traits are always good.", "Traits never matter.", "Evolution has a goal."], "No perfect organism."),
    ("Which evidence would best support that dark moths were selected by birds?", "Birds ate more light moths than dark moths on dark trees.", ["Dark moths were larger.", "Moths liked the dark.", "There were more trees."], "Measure predation."),
    ("Why does evolution happen faster in bacteria than in elephants?", "Bacteria reproduce much faster, so there are many generations quickly.", ["Bacteria try harder.", "Elephants cannot evolve.", "Bacteria never die."], "Generation time."),
])


def body():
    think = ("<p><b>Nature selects inherited traits that help survival.</b></p>"
             "<ul><li>Four factors: more offspring than can survive, inherited variation, competition for limited resources, and better-adapted individuals leaving more offspring.</li>"
             "<li>Over many generations, the helpful trait becomes more common. That is an <b>adaptation</b>.</li>"
             "<li>Individuals do not change to meet a need. Populations change because some individuals reproduce more.</li></ul>")
    ex = [("10,000 bacteria, 2% resistant. After the antibiotic?", ["2% of 10,000"], "200 resistant bacteria"),
          ("Dark moths: 10% → 60% after soot. Why?", ["Dark moths hid from birds"], "they survived and reproduced more")]
    mist = ["Thinking individuals change because they need to (Lamarck).", "Thinking traits gained during life are inherited.", "Thinking “survival of the fittest” means the strongest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Four factors", B1 + [(g_factor, 8), (g_scen, 4)]),
        ("Adaptation stories", [(g_scen, 10), (g_factor, 4), (g_resist, 6)]),
        ("Traits over generations", [(g_data, 12), (g_beak, 8)]),
        ("Resistance", [(g_resist, 10), (g_data, 4), (g_beak, 6)]),
        ("Explaining evolution", B5 + [(g_data, 5), (g_beak, 5), (g_resist, 5)]),
    ])
    make("biology", "natural-selection-and-adaptation", 16, "HS-LS4-2, HS-LS4-4",
         "Construct an explanation based on evidence that the process of evolution primarily results from four factors: (1) the potential for a species to increase in number, "
         "(2) the heritable genetic variation of individuals in a species due to mutation and sexual reproduction, (3) competition for limited resources, and (4) the proliferation of those organisms that are better able to survive and reproduce in the environment. "
         "Construct an explanation based on evidence for how natural selection leads to adaptation of populations.",
         "Natural Selection and Adaptation",
         "Natural Selection Worksheets: Adaptation, Resistance and Finch Beaks (High School Biology)",
         "Natural Selection",
         "Free high school biology worksheets on natural selection and adaptation (NGSS HS-LS4-2, HS-LS4-4): the four factors, peppered moths, antibiotic resistance and finch beak data. 100 questions with answers.",
         "Nature selects helpful inherited traits.",
         "Individuals that survive and reproduce more pass their traits on, so populations adapt.",
         body(),
         [("What are the four factors of natural selection?", "More offspring than can survive, heritable variation, competition for limited resources, and better-adapted individuals surviving and reproducing more."),
          ("How does antibiotic resistance evolve?", "A few bacteria already have resistance genes. The antibiotic kills the others, so the resistant ones multiply and the population becomes resistant."),
          ("Do individuals evolve?", "No. Individuals do not change their genes to meet a need. Populations evolve as helpful traits become more common over generations.")],
         sets)


if __name__ == "__main__":
    main()
