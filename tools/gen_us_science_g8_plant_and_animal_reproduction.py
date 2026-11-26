# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Plant and Animal Reproduction (MS-LS1-4, MS-LS1-5)
  python tools/gen_us_science_g8_plant_and_animal_reproduction.py
Use argument based on empirical evidence and scientific reasoning to support an explanation for how characteristic
animal behaviors and specialized plant structures affect the probability of successful reproduction; construct a
scientific explanation based on evidence for how environmental and genetic factors influence the growth of organisms.
Wrong answers come from real mistakes: "flowers are bright to look nice for people", "plant growth depends only on genes",
"a bigger animal always reproduces more", "seeds spread by themselves without help".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(80111)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


BEH = [("A male peacock spreads his colorful tail feathers.", "It attracts a mate."),
       ("Frogs call loudly at night near a pond.", "It attracts a mate."),
       ("A bowerbird decorates its nest area with blue objects.", "It attracts a mate."),
       ("Fireflies flash light patterns in summer.", "It attracts a mate."),
       ("Penguins take turns keeping their egg warm.", "It protects the young so more survive."),
       ("A mother bear defends her cubs from wolves.", "It protects the young so more survive."),
       ("Wolves bring food back to pups in the den.", "It protects the young so more survive."),
       ("Sea turtles bury their eggs in warm sand.", "It protects the young so more survive."),
       ("Salmon swim upstream to lay eggs in safe gravel streams.", "It protects the young so more survive."),
       ("Elephants travel in herds that guard the calves.", "It protects the young so more survive."),
       ("A male stickleback fish builds a nest and fans the eggs.", "It protects the young so more survive."),
       ("Birds sing to claim and defend a nesting area.", "It attracts a mate.")]


def g_beh():
    s, a = R.choice(BEH)
    who = P.next()[0]
    if not once(("b", s)):
        return None
    other = "It protects the young so more survive." if a == "It attracts a mate." else "It attracts a mate."
    return item("%s observes: “%s” How does this behavior increase the chance of successful reproduction?" % (who, s), a, [other, "It helps the animal grow taller.", "It has no effect on reproduction."],
                "Behaviors that attract mates or protect young help an animal pass on its genes.")


STR = [("Bright, sweet-smelling flowers with nectar", "attract pollinators like bees and butterflies"),
       ("Dandelion seeds with fluffy parachutes", "let the wind carry seeds far away"),
       ("Burdock seeds with tiny hooks", "stick to animal fur to be carried to new places"),
       ("Juicy berries with seeds inside", "get eaten by animals that drop the seeds elsewhere"),
       ("Long tube-shaped red flowers", "attract hummingbirds that carry pollen"),
       ("Maple seeds with wings", "spin through the air away from the parent tree"),
       ("Coconuts with a hard, floating shell", "float across the ocean to new islands"),
       ("Corn plants with feathery tassels", "release pollen that the wind carries to other plants"),
       ("Flowers that open at night and smell strong", "attract moths and bats as pollinators"),
       ("Acorns that squirrels bury and forget", "get planted in new places by animals")]


def g_str():
    s, a = R.choice(STR)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once(("s", s, t)):
        return None
    if t:
        return item("%s studies a plant structure: %s. How does it help the plant reproduce?" % (who, s.lower()), "They " + a + ".",
                    ["They " + x[1] + "." for x in R.sample([y for y in STR if y[1] != a], 2)] + ["They make the plant look nice for people."],
                    "Plant structures help with pollination or seed dispersal.")
    pol = any(w in a for w in ["pollen", "pollinator"])
    return item("%s studies a plant structure: %s. What does this structure mainly help with?" % (who, s.lower()), "pollination" if pol else "seed dispersal",
                ["seed dispersal" if pol else "pollination", "photosynthesis", "taking in water"], "Pollination moves pollen; dispersal moves seeds.")


def g_grow():
    who = P.next()[0]
    var = R.choice(["light", "water", "fertilizer", "temp"])
    plant = R.choice(["bean plants", "corn seedlings", "tomato plants", "sunflowers", "radishes"])
    lv = {"light": (["2 h", "6 h", "10 h", "14 h"], "hours of light per day"), "water": (["0 mL", "50 mL", "100 mL", "400 mL"], "water per day"),
          "fertilizer": (["none", "a little", "the right amount", "too much"], "fertilizer"), "temp": (["5 °C", "15 °C", "25 °C", "40 °C"], "temperature")}[var]
    shapes = {"light": [3, 9, 15, 18], "water": [0, 10, 16, 6], "fertilizer": [8, 12, 17, 5], "temp": [2, 9, 16, 4]}[var]
    sc = R.choice([1, 2])
    vals = [v * sc for v in shapes]
    k = R.choice(["best", "factor", "diff", "diff"])
    if not once((var, plant, k), 3 if k == "diff" else 1) or (k != "diff" and not once((var, k), 2)):
        return None
    ph = {"light": "different hours of light per day", "water": "different amounts of water each day", "fertilizer": "different amounts of fertilizer", "temp": "different temperatures"}[var]
    ph = ("at " if var == "temp" else "with ") + ph
    pr = "at" if var == "temp" else "with"
    ch = bar_chart(lv[0], vals, "height (cm)", "bar graph of plant height for different amounts of %s" % lv[1], ymax=max(vals) + (4 if sc == 1 else 6), step=4 if sc == 1 else 6, w=320)
    best = lv[0][vals.index(max(vals))]
    if k == "diff":
        i, j = sorted(R.sample(range(4), 2), key=lambda x: -vals[x])
        if vals[i] == vals[j]:
            return None
        d = vals[i] - vals[j]
        return item(fig(ch) + "%s grew %s %s. How much taller were the plants %s %s than the plants %s %s?" % (who, plant, ph, pr, lv[0][i], pr, lv[0][j]), "%d cm" % d,
                    ["%d cm" % vals[i], "%d cm" % (vals[i] + vals[j]), "%d cm" % (d + 2)], "%d − %d = %d cm." % (vals[i], vals[j], d))
    if k == "best":
        return item(fig(ch) + "%s grew %s %s. Which condition gave the tallest plants?" % (who, plant, ph), best, [x for x in lv[0] if x != best],
                    "Read the tallest bar.")
    return item(fig(ch) + "%s grew %s from the same seed packet %s. What does the graph show?" % (who, plant, ph),
                "An environmental factor changed how much the plants grew.", ["Genes alone decided the plants' height.", "The plants grew the same in every condition.", "Taller plants were a different species."],
                "Same genes, different environments → different growth.")


GE = [("Two identical twin calves get different amounts of food. One grows much larger.", "environmental"),
      ("Great Dane puppies grow much bigger than Chihuahua puppies on the same food.", "genetic"),
      ("Hydrangea flowers are blue in acidic soil and pink in basic soil.", "environmental"),
      ("A plant from tall parent plants grows tall in good conditions.", "genetic"),
      ("Fish in a crowded pond grow smaller than the same kind of fish in a large lake.", "environmental"),
      ("Corn grown in a drought is much shorter than the same corn with enough water.", "environmental"),
      ("A dwarf variety of apple tree stays small even with lots of sun and water.", "genetic"),
      ("Seedlings grown in the dark are pale and thin.", "environmental"),
      ("Some cattle breeds naturally grow more muscle than others.", "genetic"),
      ("Flamingos turn pink only if their diet contains certain pigments.", "environmental")]


def g_ge():
    s, a = R.choice(GE)
    who = P.next()[0]
    if not once(("ge", s)):
        return None
    return item("%s reads: “%s” Is the difference mainly caused by an environmental factor or a genetic factor?" % (who, s), a,
                ["genetic" if a == "environmental" else "environmental", "neither; it is random", "the season of the year only"], "Genes set the possible range; the environment affects where in that range an organism grows.")


B1 = bank([
    ("Why do many flowers have bright colors and sweet nectar?", "to attract pollinators that carry pollen to other flowers", ["to look nice for people", "to scare away insects", "to make more sunlight"], "Pollinators help reproduction."),
    ("What is pollination?", "moving pollen from the male part of a flower to the female part", ["spreading seeds", "a plant making food", "a seed starting to grow"], "It leads to seeds."),
    ("What is seed dispersal?", "spreading seeds away from the parent plant", ["moving pollen", "a plant losing leaves", "water entering a root"], "Less crowding, more space to grow."),
    ("Why is it helpful for seeds to travel away from the parent plant?", "They have less competition for light, water and space.", ["They grow faster in the shade.", "The parent needs to eat them.", "It is not helpful."], "Spreading out helps survival."),
    ("Why do some birds sit on their eggs?", "to keep the eggs warm so they hatch", ["to hide them from the sun", "to make them heavier", "to cool them down"], "Parental care."),
    ("Which factors can affect how much a plant grows?", "both genes and the environment (light, water, nutrients, temperature)", ["only genes", "only the color of the pot", "only the age of the gardener"], "Both matter."),
    ("Why do fish like cod lay millions of eggs?", "Most eggs and young are eaten, so many eggs increases the chance some survive.", ["They like to be busy.", "Big numbers make the ocean warmer.", "All of the eggs survive."],
     "A strategy for reproduction."),
    ("How does a bee help a flower while collecting nectar?", "Pollen sticks to the bee and is carried to another flower.", ["The bee eats the seeds.", "The bee waters the flower.", "The bee makes the flower grow taller."],
     "A mutual relationship."),
])
B4 = bank([
    ("Why do some plants grow taller and thinner in the shade?", "They stretch toward light, an environmental response.", ["Shade changes their genes.", "They have more water.", "They are a different species."], "Environment affects growth."),
    ("A farmer adds nitrogen fertilizer and the corn grows taller. What kind of factor is fertilizer?", "an environmental factor", ["a genetic factor", "a behavior", "a structure"], "Nutrients come from the environment."),
    ("Why don't Chihuahuas grow as big as Great Danes even with lots of food?", "Their genes limit how big they can grow.", ["They eat less.", "They live in smaller houses.", "They exercise more."], "Genes set the range."),
    ("Too much fertilizer makes some plants wilt. What does this show?", "There is a best amount of a nutrient; too much can harm growth.", ["More is always better.", "Fertilizer has no effect.", "Plants grow only from genes."], "Look for the best condition."),
    ("Why might a pumpkin plant from a prize-winning parent still grow small fruit?", "Poor soil, little water or cold weather limited its growth.", ["Its genes changed.", "Pumpkins never grow big.", "The parent was too large."], "Genes need a good environment."),
    ("Tadpoles in warmer water turn into frogs faster. What does this show?", "Temperature affects growth and development.", ["Warm water changes their species.", "Genes are the only factor.", "Cold water makes them grow faster."], "Environment affects development."),
])
B5 = bank([
    ("Ava grows two groups of the same bean seeds, one in sun and one in shade. The sun group is taller. What can she conclude?", "Light, an environmental factor, affected growth.", ["Genes caused the difference.", "Shade beans are a different species.", "Nothing can be concluded."],
     "Same genes, different light."),
    ("Leo counts more hummingbird visits to red tube flowers than to white flat flowers. What claim does this support?", "Flower shape and color affect which pollinators visit.", ["Hummingbirds dislike flowers.", "White flowers make more seeds.", "Color has no effect."],
     "Structure affects pollination."),
    ("Mia finds that bird pairs that build nests in thorny bushes raise more chicks. Why?", "Thorns help protect the nest from predators.", ["Thorns feed the chicks.", "Thorns keep nests cold.", "Chicks like thorns."], "Behavior improves survival."),
    ("Why might scientists cover some flowers with bags in an experiment?", "to test what happens to seed production without pollinators", ["to keep the flowers warm", "to make them grow faster", "to hide them from people"], "A control for pollination."),
    ("A well-fed calf grows larger than its twin. What is the best explanation?", "Food, an environmental factor, affected growth even though their genes are the same.", ["Twins always have different genes.", "Food has no effect on growth.", "The calves are different species."],
     "Environment matters."),
])


def body():
    think = ("<p>Living things have <b>behaviors</b> and <b>structures</b> that raise the chance of <b>successful reproduction</b>:</p>"
             "<ul><li><b>Animal behaviors</b>: attracting a mate (songs, displays, calls) and caring for young (building nests, guarding, feeding).</li>"
             "<li><b>Plant structures</b>: bright flowers and nectar attract <b>pollinators</b>; wings, hooks, fluff and fruit help with <b>seed dispersal</b>.</li></ul>"
             "<p><b>Growth</b> depends on <b>genes</b> (the possible size) and the <b>environment</b> (light, water, food, temperature, space).</p>")
    ex = [("Why do dandelion seeds have fluff?", ["Wind carries them."], "for seed dispersal"),
          ("Same seeds, different light, different heights. Cause?", ["Genes are the same."], "an environmental factor (light)")]
    mist = ["Thinking flowers are colorful to look nice for people.",
            "Thinking growth depends only on genes.",
            "Thinking seeds spread without any help from wind, water or animals."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reproduction strategies", B1 + [(g_beh, 6), (g_str, 6)]),
        ("Animal behaviors and plant structures", [(g_beh, 6), (g_str, 8), (g_ge, 6)]),
        ("Genes and environment", [(g_str, 6), (g_grow, 10), (g_ge, 4)]),
        ("Factors in growth", B4 + [(g_grow, 14)]),
        ("Arguing from evidence", B5 + [g_grow, g_str, g_ge, g_beh]),
    ])
    make("grade-8", "plant-and-animal-reproduction", 11, "MS-LS1-4",
         "Use argument based on empirical evidence and scientific reasoning to support an explanation for how characteristic animal behaviors and specialized plant structures affect the probability of successful reproduction of animals and plants respectively.",
         "Plant and Animal Reproduction",
         "Grade 8 Reproduction Worksheets: Animal Behaviors, Pollination, Seed Dispersal and Growth",
         "Reproduction and Growth",
         "Free middle school science worksheets on plant and animal reproduction (NGSS MS-LS1-4, MS-LS1-5): mating and parenting behaviors, pollination and seed dispersal, and how genes and the environment affect growth. 100 practice questions with answers.",
         "Behaviors and structures help organisms reproduce.",
         "Mate displays, parental care, flowers and seed structures raise reproductive success. Genes and the environment both affect growth.",
         body(),
         [("How do animal behaviors help reproduction?", "Behaviors such as songs and displays attract mates, and behaviors such as nest building and guarding protect young so more survive."),
          ("How do plant structures help reproduction?", "Bright flowers and nectar attract pollinators, and structures such as wings, hooks and fruit help spread seeds."),
          ("What affects how big an organism grows?", "Its genes set the possible range, and environmental factors such as food, water, light and temperature affect how much it actually grows.")],
         sets)


if __name__ == "__main__":
    main()
