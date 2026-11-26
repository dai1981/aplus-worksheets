# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Habitats and Survival (3-LS4-3)
  python tools/gen_us_science_g3_habitats_and_survival.py
In a particular habitat some organisms can survive well, some survive less well, and some cannot survive
at all. A habitat gives food, water, shelter and the right temperature. Organisms' traits fit them to
their habitats (camel in desert, polar bear in Arctic, fish in water, cactus in desert, fern in shady forest).
Wrong answers come from real mistakes: "animals can live anywhere if they try", "a cactus grows best
in a swamp", "a fish could live on land for a while".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(30111)
R = U.R
P = People(R)

HAB = {"desert": ["camel", "cactus", "rattlesnake", "roadrunner", "desert tortoise", "jackrabbit", "desert lizard"],
       "Arctic": ["polar bear", "arctic fox", "walrus", "snowy owl", "musk ox", "arctic hare"],
       "ocean": ["shark", "octopus", "sea turtle", "whale", "clownfish", "jellyfish"],
       "pond": ["frog", "duck", "water lily", "tadpole", "dragonfly", "turtle"],
       "rain forest": ["toucan", "sloth", "jaguar", "poison dart frog", "orchid", "howler monkey"],
       "grassland": ["zebra", "lion", "bison", "prairie dog", "giraffe", "meadowlark"],
       "forest": ["deer", "black bear", "owl", "squirrel", "oak tree", "fern"]}
FIT = {"camel": "stores fat in its hump and can go a long time without water", "cactus": "stores water in its thick stem",
       "polar bear": "has thick fur and a layer of fat", "arctic fox": "has thick white fur", "shark": "breathes with gills",
       "toucan": "has a long beak to reach fruit in tall trees", "sloth": "hangs from branches with long claws", "frog": "can live in water and on land",
       "water lily": "has leaves that float on water", "zebra": "eats grass and runs fast in open land", "bison": "eats grass and grows a thick winter coat",
       "fern": "grows well in shady, damp places", "roadrunner": "can run fast on hot sand", "walrus": "has thick blubber for icy water"}


CLOSE = [{"forest", "rain forest"}, {"pond", "rain forest"}, {"pond", "forest"}, {"forest", "grassland"}, {"pond", "grassland"}, {"desert", "grassland"}]


def far(a, b):
    return a != b and {a, b} not in CLOSE


def cap(s):
    return s[0].upper() + s[1:]


def art(x):
    return ("an " if x[0] in "aeiou" else "a ") + x


def g_where():
    h = R.choice(sorted(HAB))
    o = R.choice(HAB[h])
    w = [x for x in HAB if far(x, h)]
    return item("In which habitat would %s survive best?" % art(o), "the " + h if h != "Arctic" else "the Arctic", ["the " + x for x in R.sample(w, 3)],
                "%s lives in the %s, where it can get what it needs." % (cap(art(o)), h))


def g_wont():
    h = R.choice(sorted(HAB))
    o = R.choice([x for x in HAB[h]])
    others = [x for k in HAB if far(k, h) for x in HAB[k]]
    p = P.next()
    return item("%s visits the %s. Which living thing could NOT survive well there?" % (p[0], h), art(R.choice(others)), [art(x) for x in R.sample(HAB[h], 3)],
                "Its traits fit a different habitat.")


def g_why():
    o = R.choice(sorted(FIT))
    h = [k for k in HAB if o in HAB[k]][0]
    others = [FIT[x] for x in FIT if x != o]
    return item("Why can %s survive well in the %s?" % (art(o), h), "It %s." % FIT[o], ["It %s." % x for x in R.sample(others, 3)], "This trait fits the %s habitat." % h)


MOVE = [("polar bear", "a hot desert", "It would get too hot because of its thick fur and fat."),
        ("cactus", "a wet swamp", "Its roots would get too much water and rot."),
        ("goldfish", "a dry field", "It needs water to breathe with its gills."),
        ("camel", "the Arctic", "It is not built to stay warm in freezing cold."),
        ("sea turtle", "a desert", "It needs the ocean for food and swimming."),
        ("fern", "a sunny desert", "It needs shade and damp soil."),
        ("sloth", "a grassland with no trees", "It needs trees to hang in and eat leaves from."),
        ("penguin", "a hot rain forest", "It is built for cold water and would get too hot.")]


def g_move():
    o, place, why = R.choice(MOVE)
    p = P.next()
    return item("%s wonders: what would happen to %s moved to %s?" % (p[0], art(o), place), "It would not survive well. " + why,
                ["It would survive even better.", "It would change its body right away to fit in.", "Nothing would change."], why)


def g_data():
    plants = R.choice([("cactus", "fern"), ("cactus", "moss"), ("sunflower", "fern"), ("desert sage", "water lily")])
    dry, wet = plants
    n = R.choice([20, 30, 40])
    a = [R.randint(n - 6, n), R.randint(0, 4)]
    b = [R.randint(0, 4), R.randint(n - 6, n)]
    rows = [[dry, "%d" % a[0], "%d" % a[1]], [wet, "%d" % b[0], "%d" % b[1]]]
    p = P.next()
    tab = table(["Plant (%d planted in each place)" % n, "Still alive in the dry place", "Still alive in the wet place"], rows)
    k = R.choice(["dry", "wet", "claim"])
    if k == "dry":
        return item(tab + "%s planted %d of each plant in a dry place and a wet place. Which plant survives well in the dry place?" % (p[0], n), dry,
                    [wet, "Both survive equally well.", "Neither survives at all."], "%d %s plants survived there." % (a[0], dry))
    if k == "wet":
        return item(tab + "In %s's test, which plant survives well in the wet place?" % p[0], wet, [dry, "Both survive equally well.", "Neither survives at all."],
                    "%d %s plants survived there." % (b[1], wet))
    return item(tab + "Which claim does %s's data support?" % p[0], "Some plants survive well in a habitat and others do not.",
                ["All plants grow the same everywhere.", "Water does not matter to plants.", "The %s grows best in the wet place." % dry], "Each plant survived well in only one place.")


B1 = bank([
    ("What is a habitat?", "the place where a living thing gets the food, water, shelter and space it needs", ["only the food an animal eats", "a kind of weather", "a zoo"],
     "Deserts, oceans and forests are habitats."),
    ("Can every animal live in every habitat?", "No. Some survive well, some less well and some not at all.", ["Yes, if they try hard.", "Only small animals can.", "Only in summer."],
     "Traits fit living things to certain habitats."),
    ("Which habitat is very dry with little rain?", "a desert", ["a rain forest", "a pond", "an ocean"], "Desert plants and animals save water."),
    ("Which habitat is very cold and icy?", "the Arctic", ["a desert", "a rain forest", "a grassland"], "Arctic animals have thick fur or fat."),
    ("Why can't a fish live on land?", "It needs water to breathe with its gills.", ["It is too heavy.", "It does not like sunlight.", "It can live on land for a few weeks."],
     "Gills only work in water."),
    ("What might happen if a pond dries up?", "Fish and frogs may die or have to move.", ["Fish will grow legs at once.", "Nothing changes.", "More fish will live there."],
     "When a habitat changes, some living things cannot survive."),
    ("Which plant could survive in a desert?", "a cactus", ["a water lily", "a fern", "seaweed"], "A cactus stores water in its stem."),
    ("What do all habitats provide for the living things there?", "what they need to survive, like food, water and shelter", ["only toys", "only sunlight", "only cold air"],
     "Living things need food, water, air and shelter."),
])
B5 = bank([
    ("Ava puts pill bugs in a box with a wet side and a dry side. After 10 minutes, most are on the wet side. What does this show?", "Pill bugs survive better in damp places.", ["Pill bugs like dry places.", "Pill bugs cannot move.", "The box is too small."],
     "Their choice shows the habitat they need."),
    ("Leo grows grass seeds in sand and in soil. The soil grass grows much better. What can he conclude?", "Grass survives better in soil than in sand.", ["Grass cannot grow anywhere.", "Sand is better for grass.", "Seeds don't need soil or sand."],
     "Some places fit a plant better."),
    ("Mia wants to know which habitat is best for a tadpole. Where should she test it?", "in pond water", ["in dry sand", "in a hot oven", "in a paper bag"], "Tadpoles need water."),
    ("A desert gets much more rain for many years. Which plants might start to grow well there?", "plants that need more water", ["no plants at all", "only cactuses", "plants that need ice"],
     "When a habitat changes, which living things survive well can change."),
    ("Why might a deer survive less well in a city than in a forest?", "There is less food and shelter and more danger from cars.", ["Cities are too cold.", "Deer cannot see buildings.", "Deer only eat bread."],
     "The habitat may not give it what it needs."),
])


def body():
    think = ("<p>A <b>habitat</b> is the place where a living thing gets food, water, shelter and space. Deserts, the Arctic, oceans, ponds, rain forests, grasslands and forests are habitats.</p>"
             "<p>In a habitat, some living things <b>survive well</b>, some <b>survive less well</b> and some <b>cannot survive at all</b>. "
             "Their <b>traits</b> must fit the habitat: a camel can go a long time without water, a polar bear has thick fur and fat, a fish has gills.</p>")
    ex = [("Could a polar bear survive in a hot desert?", ["It has thick fur and fat for the cold."], "No, it would get too hot."),
          ("Where would a cactus survive best?", ["A cactus stores water."], "in a desert")]
    mist = ["Thinking any animal can live anywhere if it tries.",
            "Forgetting that plants need the right habitat too.",
            "Thinking a living thing changes its body right away when moved."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is a habitat?", B1 + [(g_where, 6), (g_why, 6)]),
        ("Living things and their habitats", [(g_where, 10), (g_wont, 10)]),
        ("Traits that fit a habitat", [(g_why, 10), (g_move, 8), (g_wont, 2)]),
        ("Survival data", [(g_data, 14), (g_move, 6)]),
        ("Investigations", B5 + [g_data, g_where, g_why, g_wont]),
    ])
    make("grade-3", "habitats-and-survival", 11, "3-LS4-3",
         "Construct an argument with evidence that in a particular habitat some organisms can survive well, some survive less well, and some cannot survive at all.",
         "Habitats and Survival",
         "Grade 3 Habitats Worksheets: Which Living Things Survive in Each Habitat",
         "Habitats",
         "Free Grade 3 science worksheets on habitats and survival (NGSS 3-LS4-3): deserts, the Arctic, oceans, ponds, rain forests and grasslands, traits that fit a habitat, and plant survival data. 100 practice questions with answers.",
         "Living things survive best in habitats that fit their traits.",
         "In each habitat some living things survive well, some less well and some not at all.",
         body(),
         [("What is a habitat?", "A habitat is the place where a living thing gets the food, water, shelter and space it needs."),
          ("Why can't every animal live in every habitat?", "Its traits fit some places better than others. A fish needs water to breathe, and a polar bear needs cold."),
          ("What happens when a habitat changes?", "Some living things may survive less well or have to move, and others may start to survive better.")],
         sets)


if __name__ == "__main__":
    main()
