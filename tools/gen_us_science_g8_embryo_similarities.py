# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Embryo Similarities (MS-LS4-3)
  python tools/gen_us_science_g8_embryo_similarities.py
Analyze displays of pictorial data to compare patterns of similarities in the embryological development across
multiple species to identify relationships not evident in the fully formed anatomy. Early vertebrate embryos share
a tail, pharyngeal pouches (gill-like folds) and a notochord; species that stay similar longer are more closely related.
Wrong answers come from real mistakes: "human embryos have working gills", "embryos that look alike are the same
species", "adult appearance always shows relationships best".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(80115)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# a simple model: the later stage at which embryos of two species still look alike, the closer the relationship
SPECIES = ["human", "chimpanzee", "mouse", "chicken", "turtle", "fish", "frog", "rabbit", "pig", "lizard"]
# relationship rank (shared stages, 1-4) based on accepted vertebrate relationships
GROUP = {"human": "primate", "chimpanzee": "primate", "mouse": "mammal", "rabbit": "mammal", "pig": "mammal", "chicken": "reptile-bird", "turtle": "reptile-bird", "lizard": "reptile-bird",
         "frog": "amphibian", "fish": "fish"}
ORDER = ["fish", "amphibian", "reptile-bird", "mammal", "primate"]


def shared(a, b):
    ga, gb = GROUP[a], GROUP[b]
    if ga == gb:
        return 5
    return min(ORDER.index(ga), ORDER.index(gb)) + 1


STAGES = ["stage 1", "stage 2", "stage 3", "stage 4", "stage 5"]


def g_table():
    who = P.next()[0]
    base = R.choice(["human", "mouse", "chicken", "pig"])
    others = R.sample([s for s in SPECIES if s != base], 3)
    vals = [shared(base, o) for o in others]
    if len(set(vals)) < 3:
        return None
    if not once((base, tuple(sorted(others)))):
        return None
    tab = table(["Species compared with the %s" % base, "Embryos still look alike until"], [[o, STAGES[v - 1]] for o, v in zip(others, vals)])
    k = R.choice(["closest", "farthest"])
    if k == "closest":
        a = others[vals.index(max(vals))]
        return item(tab + "Based on %s's embryo data, which species is most closely related to the %s?" % (who, base), "the " + a, ["the " + o for o in others if o != a] + ["They are all equally related."],
                    "Embryos that stay similar to a later stage share a more recent common ancestor.")
    a = others[vals.index(min(vals))]
    return item(tab + "Based on %s's embryo data, which species is least closely related to the %s?" % (who, base), "the " + a, ["the " + o for o in others if o != a] + ["They are all equally related."],
                "Embryos that become different early share a more distant common ancestor.")


FEAT = [("a tail", "All early vertebrate embryos have a tail, even species that lose it as adults, like humans."),
        ("pharyngeal pouches (gill-like folds in the neck area)", "They become gills in fish but become parts of the ear, throat and jaw in humans."),
        ("a notochord (a flexible rod along the back)", "It is replaced by the backbone in most vertebrates."),
        ("limb buds", "Small bumps that grow into arms, legs, wings or flippers."),
        ("a head end with a developing brain", "All vertebrate embryos develop the brain at one end.")]


def g_feat():
    f, e = R.choice(FEAT)
    who = P.next()[0]
    sp = R.sample(["human", "chicken", "fish", "turtle", "pig", "frog"], 2)
    if not once((f, tuple(sorted(sp)))):
        return None
    return item("%s sees that early %s and %s embryos both have %s. What does this similarity suggest?" % (who, sp[0], sp[1], f), "The two species share a common ancestor.",
                ["They are the same species.", "The adults will look exactly alike.", "The similarity is a coincidence with no meaning."], e)


def g_fate():
    who = P.next()[0]
    cases = [("pharyngeal pouches", "fish", "gills"), ("pharyngeal pouches", "human", "parts of the ear, throat and jaw"), ("the embryo tail", "human", "the tailbone (coccyx)"),
             ("the embryo tail", "lizard", "a long tail"), ("front limb buds", "chicken", "wings"), ("front limb buds", "human", "arms"), ("front limb buds", "whale", "flippers"),
             ("the notochord", "human", "part of the discs between the vertebrae")]
    part, sp, fate = R.choice(cases)
    if not once((part, sp)):
        return None
    w = [c[2] for c in cases if c[2] != fate]
    return item("%s's chart shows that %s develop in every early vertebrate embryo. What do they become in a %s?" % (who, part, sp), fate, R.sample(w, 3),
                "The same early structure can become different parts in different species.")


B1 = bank([
    ("What is an embryo?", "an organism in its earliest stage of development", ["an adult animal", "a fossil", "a type of cell wall"], "Before birth or hatching."),
    ("What do early embryos of fish, chickens and humans have in common?", "a tail and pharyngeal pouches", ["feathers", "hair", "working lungs"], "Shared early structures."),
    ("Do human embryos have working gills?", "No. They have pharyngeal pouches that become parts of the ear, throat and jaw.", ["Yes, they breathe water.", "Yes, until birth.", "Only twins do."], "Gill-like, not gills."),
    ("Why can embryos show relationships that adults do not?", "Adults may look very different after development, but early shared structures remain visible in embryos.", ["Embryos are always the same species.", "Adults have no traits.", "Embryos are fossils."],
     "Development reveals ancestry."),
    ("Two species' embryos look alike until a late stage. What does this suggest?", "They are closely related.", ["They are distantly related.", "They are unrelated.", "They are the same species."], "Longer similarity, closer relation."),
    ("Which comparison is evidence for common ancestry?", "similar structures in early embryos of different species", ["different colors of adults", "the size of eggs only", "where the animals live"], "Embryology is one line of evidence."),
    ("Which two species would you expect to have the most similar embryos for the longest time?", "a human and a chimpanzee", ["a human and a fish", "a chicken and a frog", "a mouse and a fish"], "Closest relatives."),
    ("Why do human embryos have a tail?", "Humans share ancestors with other vertebrates that have tails.", ["Humans will grow tails later.", "It is a mistake.", "It is for swimming."], "It becomes the tailbone."),
])
B5 = bank([
    ("Ava compares drawings of embryos at three stages. At stage 1 all look alike; by stage 3 they look different. What pattern does this show?", "Species become more different as development goes on.", ["Species become more alike over time.", "All adults look the same.", "Development does not change shape."],
     "Similar early, different later."),
    ("Leo says a dolphin is a fish because its body looks like a fish's. What embryo evidence could correct him?", "Dolphin embryos develop like mammal embryos, including hind limb buds that disappear.", ["Dolphins swim.", "Dolphins live in the ocean.", "Dolphin embryos have scales."],
     "Embryos reveal mammal ancestry."),
    ("Mia ranks species by how long their embryos look like a chicken's. What is she really ranking?", "how closely related each species is to chickens", ["how big each species gets", "how fast each swims", "how many eggs each lays"], "Similarity tracks relationship."),
    ("Which kind of data is most useful for MS-LS4-3-style comparisons?", "pictures of embryos at the same stages for several species", ["photos of adults only", "weather data", "rock layer depth only"], "Compare like with like."),
    ("Why do scientists use several lines of evidence (fossils, anatomy, embryos, DNA)?", "Different evidence can confirm the same relationships.", ["Each one is always wrong.", "One kind is never enough to name a species.", "To make research slower."],
     "Agreement makes conclusions stronger."),
])


def body():
    think = ("<p>Early <b>embryos</b> of vertebrates look surprisingly alike. They share a <b>tail</b>, <b>pharyngeal pouches</b> (gill-like folds) and a <b>notochord</b>.</p>"
             "<p>As development continues, the embryos become different. The same early structure can become different parts: pharyngeal pouches become <b>gills in fish</b> but <b>parts of the ear and throat in humans</b>.</p>"
             "<p>The <b>longer two species' embryos stay alike</b>, the <b>more closely related</b> they are. Embryos can show relationships that adult bodies hide.</p>")
    ex = [("Human embryos look like chimpanzee embryos until late and like fish embryos only early. Closer relative?", ["Longer similarity = closer."], "the chimpanzee"),
          ("What do pharyngeal pouches become in a fish?", ["Same start, different end."], "gills")]
    mist = ["Thinking human embryos have working gills.",
            "Thinking embryos that look alike are the same species.",
            "Thinking adult appearance always shows relationships best."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Embryos and ancestry", B1 + [(g_feat, 4), (g_table, 8)]),
        ("Shared structures", [(g_fate, 8), (g_feat, 4), (g_table, 8)]),
        ("Comparing embryo data", [(g_table, 20)]),
        ("Development and relationships", [(g_table, 18), (g_feat, 2)]),
        ("Interpreting evidence", B5 + [(g_table, 15)]),
    ])
    make("grade-8", "embryo-similarities", 15, "MS-LS4-3",
         "Analyze displays of pictorial data to compare patterns of similarities in the embryological development across multiple species to identify relationships not evident in the fully formed anatomy.",
         "Embryo Similarities",
         "Grade 8 Embryo Similarities Worksheets: Comparing Embryos to Find Evolutionary Relationships",
         "Embryo Similarities",
         "Free middle school science worksheets on embryo similarities (NGSS MS-LS4-3): shared structures in early vertebrate embryos, what they become, and using embryo data to infer how closely species are related. 100 practice questions with answers.",
         "Embryos that stay alike longer are closer relatives.",
         "Early vertebrate embryos share a tail and gill-like pouches. Comparing development reveals relationships adults hide.",
         body(),
         [("Why do embryos of different animals look alike?", "They inherited the same early developmental plan from a common ancestor."),
          ("Do human embryos have gills?", "No. They have pharyngeal pouches, which become parts of the ear, throat and jaw, while in fish the same pouches become gills."),
          ("How can embryos show how closely species are related?", "Species whose embryos stay similar until later stages of development are usually more closely related.")],
         sets)


if __name__ == "__main__":
    main()
