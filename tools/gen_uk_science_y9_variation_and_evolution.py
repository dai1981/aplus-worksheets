# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Biology): Variation and Evolution
  python tools/gen_uk_science_y9_variation_and_evolution.py
Differences between species, variation within a species (continuous and discontinuous, genetic and environmental),
natural selection and evolution, selective breeding, genetic engineering, competition, extinction and the importance
of biodiversity and gene banks. Reuses the natural-selection and artificial-selection questions of the US Grade 8
units in British English.
Wrong answers come from real mistakes: "animals change because they want to", "individuals evolve in their lifetime",
"all variation is caused by genes", "extinct species can come back".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us

U = Unit(61902)
R = U.R
P = People(R)
uk_sci.USED.clear()
NS = adopt_us("gen_us_science_g8_natural_selection", U)
AS = adopt_us("gen_us_science_g8_artificial_selection_and_genetic_engineering", U)
us_graph, us_pct, us_which = ukm(NS.g_graph), ukm(NS.g_pct), ukm(NS.g_which)
us_data, us_meth, us_pro, us_wild = ukm(AS.g_data), ukm(AS.g_meth), ukm(AS.g_pro), ukm(AS.g_wild)

VAR = [("height", "continuous"), ("body mass", "continuous"), ("hand span", "continuous"), ("foot length", "continuous"), ("the time taken to run 100 m", "continuous"),
       ("blood group", "discontinuous"), ("whether you can roll your tongue", "discontinuous"), ("natural eye colour (brown, blue, green)", "discontinuous"),
       ("whether ear lobes are attached or free", "discontinuous"), ("shoe size", "discontinuous")]


def g_var():
    v, t = R.choice(VAR)
    if not once(("va", v)):
        return None
    return item("Is %s an example of continuous or discontinuous variation?" % v, t + " variation", [("discontinuous" if t == "continuous" else "continuous") + " variation", "no variation", "environmental change"],
                "Continuous: any value in a range (bar chart with no gaps, or histogram). Discontinuous: distinct groups.")


CAUSE = [("natural eye colour", "genetic"), ("blood group", "genetic"), ("a scar from a fall", "environmental"), ("the language you speak", "environmental"),
         ("dyed hair colour", "environmental"), ("a pierced ear", "environmental"), ("height", "both genetic and environmental"), ("body mass", "both genetic and environmental"),
         ("natural hair colour", "genetic"), ("muscle strength", "both genetic and environmental")]


def g_cause():
    c, a = R.choice(CAUSE)
    if not once(("ca", c)):
        return None
    return item("Is %s caused by genes, by the environment, or by both?" % c, a, [x for x in ["genetic", "environmental", "both genetic and environmental", "neither"] if x != a],
                "Some features are inherited, some come from how we live, and many depend on both.")


STEP = ["There is variation in a population.", "Some individuals have features that suit the environment better.", "They are more likely to survive and reproduce.",
        "They pass on their useful genes to their offspring.", "Over many generations, the useful feature becomes more common."]


def g_step():
    i = R.randrange(len(STEP) - 1)
    if not once(("st", i)):
        return None
    return item("In natural selection, which step comes straight after this: “%s”" % STEP[i], STEP[i + 1], [x for x in STEP if x not in (STEP[i], STEP[i + 1])][:3], "Variation → survival → reproduction → genes passed on → change over time.")


EXT = [("Why did the dodo become extinct?", "People hunted it and brought animals that ate its eggs.", ["It evolved into a pigeon.", "It flew away.", "It was too clever."]),
       ("What is a species?", "a group of organisms that can breed to produce fertile offspring", ["any animals that look alike", "all the animals in a habitat", "only one animal"]),
       ("Why is a mule (horse × donkey) not a separate species?", "Mules are infertile and cannot breed.", ["They are too big.", "They live too long.", "They are a new species."]),
       ("What is a gene bank?", "a store of seeds, eggs or tissue to protect species and their genes", ["a bank that lends money for science", "a type of fossil", "a zoo for plants only"]),
       ("Why does biodiversity matter?", "Ecosystems with many species are more stable and give us food, medicines and materials.", ["It does not matter.", "Fewer species means more food.", "Only rare species matter."]),
       ("Which of these can cause extinction?", "loss of habitat, new diseases, new predators and climate change", ["more variation", "plenty of food", "gene banks"]),
       ("Who proposed the theory of evolution by natural selection?", "Charles Darwin (and Alfred Russel Wallace)", ["Isaac Newton", "Gregor Mendel only", "Rosalind Franklin"]),
       ("What evidence supports evolution?", "fossils showing gradual changes over millions of years", ["animals changing overnight", "ghost stories", "the shape of clouds"])]


def g_ext():
    q, a, w = R.choice(EXT)
    if not once(("ex", q)):
        return None
    return item(q, a, w, "Species change over long periods; some die out.")


B1 = bank([
    ("What is variation?", "the differences between individuals", ["the way animals move", "the number of chromosomes", "a type of habitat"], "Within and between species."),
    ("Which graph is best for continuous variation such as height?", "a histogram", ["a bar chart with gaps", "a pie chart", "a pictogram"], "Grouped data."),
    ("Why do offspring of the same parents look different?", "Each gets a different mix of the parents' genes.", ["They have no genes.", "They copy their friends.", "Genes change every day."], "Sexual reproduction mixes genes."),
    ("Can an animal evolve in its own lifetime?", "No. Populations evolve over many generations.", ["Yes, if it tries hard.", "Yes, by eating more.", "Only if it moves house."], "Changes in gene frequency."),
])
B5 = bank([
    ("Why are some bacteria now resistant to antibiotics?", "Resistant bacteria survived and reproduced, so resistance became common.", ["Bacteria chose to be resistant.", "Antibiotics make bacteria stronger.", "People became resistant."], "Natural selection we can see."),
    ("Why do giraffes have long necks, according to natural selection?", "Ancestors with longer necks reached more food, survived and passed on the genes.", ["They stretched their necks and passed this on.", "They wanted to be tall.", "Necks grow from eating leaves."], "Not by stretching."),
    ("What is competition?", "living things trying to get the same limited resources", ["animals helping each other", "plants making food", "the end of a species"], "Food, water, space, mates."),
    ("How is selective breeding different from natural selection?", "Humans choose which individuals breed.", ["It happens without people.", "It takes millions of years.", "It does not use genes."], "Artificial selection."),
])


def body():
    think = ("<p><b>Variation plus natural selection leads to evolution.</b></p>"
             "<ul><li>Continuous variation has any value in a range; discontinuous variation has separate groups. Variation can be genetic, environmental or both.</li>"
             "<li>Individuals with useful features survive, reproduce and pass on their genes, so the population changes over many generations.</li>"
             "<li>People use selective breeding. Species can become extinct; gene banks help protect them.</li></ul>")
    ex = [("Blood group: continuous or discontinuous?", ["Separate groups"], "discontinuous"),
          ("A scar: genetic or environmental?", ["Caused by an injury"], "environmental")]
    mist = ["Thinking animals change because they want to.", "Thinking one animal evolves in its lifetime.", "Thinking all variation is genetic."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Variation", B1 + [(g_var, 9), (g_cause, 7)]),
        ("Natural selection", [(g_step, 3), (us_which, 9), (us_pct, 8)]),
        ("Evidence and change", [(us_graph, 8), (us_pct, 6), (g_cause, 2), (g_ext, 4)]),
        ("Selective breeding", [(us_data, 8), (us_meth, 6), (us_wild, 4), (us_pro, 2)]),
        ("Extinction and biodiversity", B5 + [(g_ext, 3), (us_pro, 5), (us_which, 4), (us_wild, 2), (us_meth, 2)]),
    ])
    make_ks3(9, "variation-and-evolution", 2, "Biology", "Genetics and evolution",
             "Differences between species; the variation between individuals within a species being continuous or discontinuous, to include measurement and graphical representation of variation; the variation between species and between individuals of the same species means some organisms compete more successfully, which can drive natural selection; changes in the environment may leave individuals within a species, and some entire species, less well adapted to compete successfully and reproduce, which in turn may lead to extinction; the importance of maintaining biodiversity and the use of gene banks to preserve hereditary material before extinction.",
             "Variation and Evolution",
             "Year 9 Science: Variation and Evolution Worksheets (Natural Selection, Extinction)",
             "Variation and Evolution",
             "Free Year 9 science worksheets on variation and evolution: continuous and discontinuous variation, genetic and environmental causes, natural selection, selective breeding, extinction and gene banks. 100 questions with answers.",
             "Natural selection changes populations over time.",
             "Useful features help survival; the genes are passed on.",
             body(),
             [("What is the difference between continuous and discontinuous variation?", "Continuous variation can take any value in a range, like height. Discontinuous variation falls into separate groups, like blood group."),
              ("How does natural selection work?", "Individuals vary. Those best suited to the environment survive and reproduce, passing on their genes, so over many generations the useful features become common."),
              ("Why are gene banks important?", "They store seeds, eggs and tissue so that species and their genes can be protected and even restored if they become rare.")],
             sets)


if __name__ == "__main__":
    main()
