# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Interactions in Ecosystems (MS-LS2-2)
  python tools/gen_us_science_g7_interactions_in_ecosystems.py
Construct an explanation that predicts patterns of interactions among organisms across ecosystems:
competition, predation, and symbiosis (mutualism, commensalism, parasitism). Predator-prey cycles
(snowshoe hare and lynx), predicting effects when one population changes.
Wrong answers come from real mistakes: "mutualism means one is harmed", "a parasite always kills its host quickly",
"when predators increase, prey increase too".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(70109)
R = U.R
P = People(R)

EX = {"mutualism": ["bees get nectar from flowers and carry pollen between them", "clownfish live in sea anemones and help keep them clean", "oxpecker birds eat ticks off zebras",
                    "bacteria in your intestines get food and help you digest", "ants protect acacia trees and live in their thorns", "fungi on plant roots get sugar and help roots take in water"],
      "commensalism": ["barnacles ride on a whale without hurting it", "a bird builds a nest in a tree", "remora fish ride along with sharks and eat scraps",
                       "cattle egrets eat insects stirred up by grazing cows", "moss grows on the bark of a tree", "a hermit crab lives in an empty snail shell"],
      "parasitism": ["a tick sucks blood from a dog", "a tapeworm lives in an animal's intestine", "mistletoe takes water and nutrients from a tree",
                     "fleas live on a cat", "a mosquito feeds on a person's blood", "lice live on a person's head"],
      "predation": ["an owl catches a mouse", "a lion hunts a zebra", "a frog eats a fly", "a lynx catches a snowshoe hare", "a hawk dives for a rabbit", "a ladybug eats aphids"],
      "competition": ["two kinds of birds eat the same insects", "lions and hyenas hunt the same zebras", "weeds and corn take the same water", "two male deer fight over the same territory",
                      "trees grow taller to reach the same sunlight", "squirrels and jays gather the same acorns"]}
WHO = {"mutualism": "both benefit", "commensalism": "one benefits and the other is not helped or harmed", "parasitism": "one benefits and the other is harmed",
       "predation": "one organism hunts and eats another", "competition": "organisms need the same limited resource"}


def g_kind():
    k = R.choice(sorted(EX))
    x = R.choice(EX[k])
    who = P.next()[0]
    return item("%s observes that %s. What kind of interaction is this?" % (who, x), k, R.sample([c for c in EX if c != k], 3), "In %s, %s." % (k, WHO[k]))


def g_which():
    k = R.choice(sorted(EX))
    x = R.choice(EX[k])
    who = P.next()[0]
    w = [y for c in EX if c != k for y in EX[c]]
    return item("%s needs an example of %s (%s). Which is the best example?" % (who, k, WHO[k]), x, R.sample(w, 3), "That is %s." % k)


def g_cycle():
    years = ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6"]
    hare = [40, 80, 100, 60, 30, 50]
    lynx = [10, 15, 30, 40, 25, 12]
    rows = [[y, "%d" % h, "%d" % l] for y, h, l in zip(years, hare, lynx)]
    who = P.next()[0]
    tab = table(["Year", "Snowshoe hares (thousands)", "Lynx (thousands)"], rows)
    k = R.choice(["after", "why", "lag", "predict"])
    if k == "after":
        return item(tab + "In %s's data, what happened to the lynx population after the hares peaked in Y3?" % who, "It peaked a year later, then fell.",
                    ["It fell right away to zero.", "It never changed.", "It rose forever."], "More hares meant more food for lynx, so lynx increased until hares became scarce.")
    if k == "why":
        return item(tab + "Why did the hare population fall after Y3 in %s's data?" % who, "Many lynx were eating hares, and food for hares also ran low.",
                    ["Lynx stopped hunting.", "Hares turned into lynx.", "More food appeared."], "Predators and limited food reduce prey populations.")
    if k == "lag":
        return item(tab + "Which statement best describes the pattern in %s's data?" % who, "Predator numbers rise and fall a little after prey numbers.",
                    ["Predators and prey always change in opposite years at random.", "Prey numbers follow predator numbers exactly.", "There is no pattern."], "This is a predator-prey cycle.")
    return item(tab + "Hares rise again in Y6 in %s's data. What will most likely happen to the lynx in the next year or two?" % who, "The lynx population will increase.",
                ["The lynx population will drop to zero.", "Lynx will stop eating hares.", "Nothing will happen."], "More prey supports more predators.")


def g_predict():
    who = P.next()[0]
    cases = [("Wolves are removed from a park.", "deer", "increase at first, then may crash when they eat too many plants"),
             ("A disease kills many of the bees in an orchard.", "apple crop", "decrease because fewer flowers are pollinated"),
             ("Many cats are released near a bird colony.", "birds", "decrease because of more predation"),
             ("A new weed spreads in a farm field.", "corn", "decrease because of more competition for water and light"),
             ("Ticks increase in a forest.", "deer health", "decrease because more parasites feed on them"),
             ("Sea otters are protected and increase.", "sea urchins", "decrease because otters eat urchins")]
    s, pop, a = R.choice(cases)
    return item("%s reads: “%s” Predict what happens to the %s." % (who, s, pop), "It will " + a + ".",
                ["It will " + x + "." for x in ["stay exactly the same", "grow without any limit", "turn into a different species"]], "Changes in one population affect others it interacts with.")


B1 = bank([
    ("What is symbiosis?", "a close, long-term relationship between two different species", ["a kind of food", "competition for water", "one animal eating another once"], "Mutualism, commensalism and parasitism are types of symbiosis."),
    ("In mutualism, who benefits?", "both organisms", ["only one organism", "neither organism", "only the larger organism"], "Bees and flowers both benefit."),
    ("In parasitism, what happens to the host?", "It is harmed", ["It is helped", "It is not affected", "It always dies right away"], "A parasite usually does not kill its host quickly."),
    ("A predator is", "an organism that hunts and eats other organisms", ["an organism that is eaten", "a plant", "a decomposer"], "Prey are the organisms that are eaten."),
    ("If the number of predators increases, what usually happens to the prey?", "The prey population decreases.", ["The prey population increases.", "The prey are not affected.", "The prey become predators."],
     "More predators eat more prey."),
    ("Why do similar interactions happen in very different ecosystems?", "Organisms everywhere need food, shelter and mates, so they compete, hunt and cooperate.", ["Ecosystems are all the same.", "Animals copy each other.", "Interactions happen only in forests."],
     "Patterns repeat across ecosystems."),
    ("A shark and a remora: the remora eats scraps and the shark is unaffected. What is this?", "commensalism", ["mutualism", "parasitism", "predation"], "One benefits; the other is not affected."),
    ("What do organisms compete for?", "limited resources like food, water, space, light and mates", ["unlimited resources", "nothing", "only sunlight"], "Competition happens when resources are limited."),
])
B5 = bank([
    ("Ava removes the ants from some acacia trees. Those trees get eaten more by animals. What does this show?", "The ants and trees have a mutualism that protects the tree.", ["Ants harm the trees.", "Trees do not need ants.", "Ants eat the trees."],
     "Evidence for a mutualism."),
    ("Leo graphs barn owls and mice on a farm. When mice increase, owls increase a year later. Why?", "More food (mice) supports more owl chicks.", ["Owls make mice.", "Mice eat owls.", "It is random."], "Predators follow prey."),
    ("Mia finds that cowbirds lay eggs in other birds' nests, and the other birds raise the cowbird chicks. What kind of relationship is this?", "parasitism", ["mutualism", "commensalism", "competition only"],
     "The host birds are harmed."),
    ("Why do scientists study interactions before bringing a new species into an area?", "The new species may compete with, eat or harm native species.", ["New species never interact.", "Interactions only help.", "To make the area colder."],
     "Predicting interactions prevents problems."),
    ("Two species of barnacles live on the same rock. When one is removed, the other spreads into its area. What does this show?", "They were competing for space.", ["They were mutualists.", "They were parasites.", "Space is unlimited."],
     "Removing a competitor frees resources."),
])


def body():
    think = ("<p>Organisms interact in patterns that repeat in every ecosystem:</p><ul>"
             "<li><b>Competition</b>: organisms need the same limited resource.</li><li><b>Predation</b>: a predator hunts and eats prey.</li>"
             "<li><b>Mutualism</b>: both benefit (bees and flowers).</li><li><b>Commensalism</b>: one benefits, the other is not helped or harmed (barnacles on a whale).</li>"
             "<li><b>Parasitism</b>: one benefits, the other is harmed (ticks on a dog).</li></ul>"
             "<p>Predator and prey populations often rise and fall in <b>cycles</b>: when prey increase, predators increase a little later; then prey decrease, and predators follow.</p>")
    ex = [("Oxpeckers eat ticks off zebras. Both benefit. Which interaction?", ["Both benefit."], "mutualism"),
          ("Wolves are removed. What happens to deer at first?", ["Less predation."], "They increase.")]
    mist = ["Mixing up commensalism (one is unaffected) and parasitism (one is harmed).",
            "Thinking more predators lead to more prey.",
            "Thinking parasites always kill their hosts quickly."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Kinds of interactions", B1 + [(g_kind, 12)]),
        ("Symbiosis, predation and competition", [(g_kind, 10), (g_which, 10)]),
        ("Predator and prey cycles", [(g_cycle, 12), (g_which, 8)]),
        ("Predicting changes", [(g_predict, 12), (g_kind, 8)]),
        ("Explaining patterns", B5 + [g_cycle, g_predict, g_which, g_kind]),
    ])
    make("grade-7", "interactions-in-ecosystems", 9, "MS-LS2-2",
         "Construct an explanation that predicts patterns of interactions among organisms across multiple ecosystems.",
         "Interactions in Ecosystems",
         "Grade 7 Ecosystem Interactions Worksheets: Predation, Competition and Symbiosis",
         "Interactions in Ecosystems",
         "Free middle school science worksheets on interactions in ecosystems (NGSS MS-LS2-2): competition, predation, mutualism, commensalism and parasitism, and predator-prey cycles. 100 practice questions with answers.",
         "Organisms compete, hunt and help each other.",
         "Predation, competition, mutualism, commensalism and parasitism happen in every ecosystem and affect population sizes.",
         body(),
         [("What are the three types of symbiosis?", "Mutualism (both benefit), commensalism (one benefits, the other is not affected) and parasitism (one benefits, the other is harmed)."),
          ("What is a predator-prey cycle?", "When prey increase, predators have more food and increase; then prey decrease, and predators decrease after them."),
          ("Why do the same kinds of interactions happen in different ecosystems?", "All organisms need resources, so they compete, eat others or cooperate in similar ways everywhere.")],
         sets)


if __name__ == "__main__":
    main()
