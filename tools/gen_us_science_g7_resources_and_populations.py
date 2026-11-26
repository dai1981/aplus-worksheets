# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Resources and Populations (MS-LS2-1)
  python tools/gen_us_science_g7_resources_and_populations.py
Analyze and interpret data to provide evidence for the effects of resource availability on organisms and
populations. Limiting factors (food, water, space, shelter, sunlight), carrying capacity, competition,
population graphs (growth, leveling off, crashes after drought), cause and effect.
Wrong answers come from real mistakes: "a population can grow forever", "more food never changes population size",
"competition only happens between different species".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(70108)
R = U.R
P = People(R)
SPEC = [("deer", "forest"), ("rabbits", "meadow"), ("squirrels", "park"), ("frogs", "pond"), ("trout", "stream"), ("prairie dogs", "grassland"), ("elk", "valley"), ("ducks", "wetland")]


def g_graph():
    sp, place = R.choice(SPEC)
    years = ["2016", "2017", "2018", "2019", "2020", "2021"]
    kind = R.choice(["drought", "level", "food"])
    if kind == "drought":
        base = R.randint(60, 90)
        vals = [base, base + R.randint(5, 10), base + R.randint(10, 15), R.randint(25, 40), R.randint(30, 45), R.randint(40, 55)]
        q, a, w, e = ("A drought hit the %s in 2019. What does %s's graph of %s show?", "The population dropped after the drought because food and water became scarce.",
                      ["The drought made the population grow.", "The population did not change.", "The population went to zero forever."], "Fewer resources means fewer individuals can survive.")
    elif kind == "level":
        vals = [20, 45, 70, 82, 85, 84]
        q, a, w, e = ("%s's graph shows the %s population in a %s over six years. What best explains why the population stopped growing?" % ("%s", "%s", place), "It reached the carrying capacity; there were only enough resources for about 85.",
                      ["The animals stopped having young forever.", "Populations always stop at 85.", "The graph is wrong."], "Limited food, water and space keep the population from growing forever.")
        who = P.next()[0]
        ch = bar_chart(years, vals, sp, "bar graph of a population over time", ymax=100, step=20, w=380)
        return item(fig(ch) + q % (who, sp), a, w, e)
    else:
        base = R.randint(30, 50)
        vals = [base, base + R.randint(0, 3), base + R.randint(0, 3), base + R.randint(12, 18), base + R.randint(22, 30), base + R.randint(30, 38)]
        q, a, w, e = ("Extra food became available in the %s in 2019. What does %s's graph of %s show?", "The population grew after more food was available.",
                      ["The population shrank because of the food.", "Food has no effect on populations.", "The population stayed exactly the same."], "More resources can support more individuals.")
    who = P.next()[0]
    ch = bar_chart(years, vals, sp, "bar graph of a population over time", ymax=100, step=20, w=380)
    return item(fig(ch) + q % (place, who, sp), a, w, e)


def g_limit():
    who = P.next()[0]
    rows = [("A dry summer leaves little water in a pond.", "water"), ("Too many deer eat all the young plants in a forest.", "food"),
            ("Trees shade the forest floor so small plants cannot grow.", "sunlight"), ("Not enough hollow trees for owls to nest in.", "shelter"),
            ("Barnacles crowd onto a rock with no more room.", "space"), ("A cold winter freezes the plants rabbits eat.", "food"),
            ("A new parking lot covers a meadow where foxes dug dens.", "shelter"), ("Too many fish crowd a small tank.", "space")]
    s, a = R.choice(rows)
    return item("%s notes: “%s” Which limiting factor is affecting the population?" % (who, s), a, [x for x in ["food", "water", "sunlight", "shelter", "space"] if x != a][:3] if a != "space" else ["food", "water", "sunlight"],
                "A limiting factor is a resource that keeps a population from growing.")


def g_compete():
    who = P.next()[0]
    pairs = [("two kinds of birds", "insects in the same trees"), ("lions and hyenas", "zebras on the savanna"), ("oak seedlings", "sunlight and water on the forest floor"),
             ("trout in a crowded stream", "food and space"), ("weeds and tomato plants", "water and nutrients in a garden"), ("two squirrels", "acorns under one tree")]
    a, b = R.choice(pairs)
    return item("%s observes %s using %s. What is happening?" % (who, a, b), "competition for limited resources", ["predation", "they are helping each other", "photosynthesis"],
                "When organisms need the same limited resource, they compete.")


def g_table():
    sp, place = R.choice(SPEC)
    food = [100, 200, 300, 400]
    pop = [R.randint(8, 14)]
    for _ in range(3):
        pop.append(pop[-1] + R.randint(7, 12))
    rows = [["%d kg" % f, "%d" % p] for f, p in zip(food, pop)]
    who = P.next()[0]
    tab = table(["Food available each week", "Number of %s" % sp], rows)
    if R.random() < 0.5:
        return item(tab + "What relationship does %s's data show?" % who, "More food supports a larger population.", ["More food causes a smaller population.", "Food does not matter.", "The population decides the food."],
                    "As food increases, the population increases.")
    return item(tab + "If food in %s's study dropped to 100 kg a week, about how many %s could the area support?" % (who, sp), "about %d" % pop[0],
                ["about %d" % pop[-1], "about %d" % (pop[-1] * 2), "an unlimited number"], "The data shows about %d with 100 kg of food." % pop[0])


B1 = bank([
    ("What is a population?", "all the members of one species living in an area", ["all the species in an area", "one animal", "the nonliving parts of an area"], "All the deer in a forest form a population."),
    ("What is a limiting factor?", "something that keeps a population from growing, like limited food, water or space", ["something that makes a population grow forever", "a kind of predator only", "a type of weather map"],
     "Resources are limited."),
    ("What is carrying capacity?", "the largest population an environment can support with its resources", ["the number of animals a truck can carry", "the smallest possible population", "the total number of species"],
     "Populations often level off near it."),
    ("Can a population grow forever?", "No. Limited resources eventually stop the growth.", ["Yes, always.", "Only small animals can.", "Only plants can."], "Food, water and space run out."),
    ("When resources are plentiful, what usually happens to a population?", "It grows.", ["It shrinks.", "It disappears.", "It stays the same no matter what."], "More resources support more individuals."),
    ("Which is a resource plants compete for?", "sunlight", ["prey", "nests", "mates only"], "Plants need light, water and nutrients."),
    ("What happens to individuals when resources are scarce?", "They compete, and some may not survive or reproduce.", ["They all grow bigger.", "They stop needing food.", "Nothing changes."],
     "Scarcity affects survival."),
    ("Can members of the same species compete?", "Yes. They need the same resources.", ["No, never.", "Only plants do.", "Only in winter."], "Competition within a species is common."),
])
B5 = bank([
    ("Ava counts dandelions in two plots: one watered, one not. The watered plot has twice as many. What resource is limiting in the dry plot?", "water", ["sunlight", "space", "shelter"],
     "Only water was different."),
    ("Leo's data shows a rabbit population rose for three years and then crashed. What is the most likely cause?", "The rabbits used up their food supply.", ["Rabbits get tired of growing.", "More food appeared.", "The rabbits moved to the moon."],
     "Overpopulation can deplete resources."),
    ("Mia plants 10 seeds in one pot and 1 seed in another pot of the same size. Which plant will likely grow biggest?", "the single plant", ["one of the 10 crowded plants", "They will all be the same.", "None will grow."],
     "Crowded plants compete for water, light and nutrients."),
    ("Why do scientists count populations over many years instead of one year?", "to see patterns and how they relate to changes in resources", ["to make the numbers bigger", "because one year is always wrong", "to find new species only"],
     "Long-term data show trends."),
    ("A lake gets fertilizer runoff and algae grow quickly. Then fish die when oxygen runs low. Which resource became limiting for the fish?", "oxygen in the water", ["sunlight", "space on land", "food from fertilizer"],
     "Algae growth and decay used up oxygen."),
])


def body():
    think = ("<p>A <b>population</b> is all the members of one species in an area. Populations need <b>resources</b>: food, water, space, shelter and (for plants) sunlight.</p>"
             "<p>When resources are plentiful, populations <b>grow</b>. When they are scarce, individuals <b>compete</b>, and fewer survive and reproduce. "
             "A resource that limits growth is a <b>limiting factor</b>. The largest population an area can support is its <b>carrying capacity</b>, so many population graphs level off.</p>"
             "<p>Data and graphs show the <b>cause and effect</b>: a drought can cause a population to fall; extra food can cause it to rise.</p>")
    ex = [("A drought dries a pond. What happens to the frog population?", ["Less water and food."], "It decreases."),
          ("A deer population stays near 85 for years. What is 85?", ["The environment supports about 85."], "the carrying capacity")]
    mist = ["Thinking a population can grow forever.",
            "Thinking competition happens only between different species.",
            "Ignoring how one limiting factor can control a population."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Populations and resources", B1 + [(g_limit, 6), (g_compete, 6)]),
        ("Limiting factors", [(g_limit, 14), (g_compete, 6)]),
        ("Population graphs", [(g_graph, 14), (g_table, 6)]),
        ("Resource data", [(g_table, 12), (g_graph, 8)]),
        ("Analyzing evidence", B5 + [g_graph, g_table, g_limit, g_compete]),
    ])
    make("grade-7", "resources-and-populations", 8, "MS-LS2-1",
         "Analyze and interpret data to provide evidence for the effects of resource availability on organisms and populations of organisms in an ecosystem.",
         "Resources and Populations",
         "Grade 7 Population Worksheets: Limiting Factors, Carrying Capacity and Competition",
         "Resources and Populations",
         "Free middle school science worksheets on resources and populations (NGSS MS-LS2-1): limiting factors, carrying capacity, competition and population graphs and data. 100 practice questions with answers.",
         "Resources limit how big a population can grow.",
         "More food, water and space support larger populations. Scarce resources lead to competition and smaller populations.",
         body(),
         [("What is a limiting factor?", "A resource such as food, water, space or shelter that keeps a population from growing larger."),
          ("What is carrying capacity?", "The largest population of a species that an environment can support over time with its resources."),
          ("How does a drought affect populations?", "Less water and food means fewer organisms can survive, so populations usually decrease.")],
         sets)


if __name__ == "__main__":
    main()
