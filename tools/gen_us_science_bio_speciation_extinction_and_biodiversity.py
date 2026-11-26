# -*- coding: utf-8 -*-
"""
US High School Biology: Speciation, Extinction and Biodiversity (HS-LS4-5, HS-LS4-6)
  python tools/gen_us_science_bio_speciation_extinction_and_biodiversity.py
Evaluate the evidence supporting claims that changes in environmental conditions may result in (1) increases in the
number of individuals of some species, (2) the emergence of new species over time, and (3) the extinction of other
species. Create or revise a simulation to test a solution to mitigate adverse impacts of human activity on biodiversity.
Geographic, behavioral and temporal isolation; adaptive radiation; extinction and mass extinction; population data;
simulations that compare solutions.
Wrong answers come from real mistakes: "a new species forms in one generation", "extinction only happened to dinosaurs",
"a change helps or harms every species the same way".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90118)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ISO = ["geographic isolation", "behavioral isolation", "temporal isolation", "mechanical isolation"]
ISC = [("A river changes course and splits a population of squirrels into two groups.", 0), ("The Grand Canyon separates two groups of squirrels.", 0),
       ("A few finches are blown to a distant island and never return.", 0), ("Rising sea level turns a hill into an island and cuts off a lizard population.", 0),
       ("A new highway and city cut a forest in two, and salamanders cannot cross.", 0),
       ("Two meadowlark species look alike but sing different songs, so they do not mate.", 1), ("Fireflies of two species flash different light patterns.", 1),
       ("Two bird species have different courtship dances.", 1), ("Female frogs only respond to the call of their own species.", 1),
       ("One frog species breeds in early spring and another in late summer.", 2), ("Two pine species release pollen in different months.", 2),
       ("Two skunk species mate in different seasons.", 2), ("Two flower species have shapes that fit different pollinators.", 3),
       ("Two snail species have shells that coil in opposite directions, so their bodies cannot line up to mate.", 3)]


def g_iso():
    s, k = R.choice(ISC)
    if not once(("i", s)):
        return None
    return item("%s Which kind of isolation is this?" % s, ISO[k], [x for x in ISO if x != ISO[k]],
                ["A physical barrier separates them.", "Different mating behaviors.", "Different breeding times.", "Body parts do not fit."][k])


ENV = [("A volcanic eruption wipes out most plants on an island. A plant with seeds that survive fire spreads quickly.", "increase in some species"),
       ("Warmer winters let a pine beetle survive farther north, and its numbers boom.", "increase in some species"),
       ("A lake dries up, and deer have more grassland to graze.", "increase in some species"),
       ("Wolves are removed, and the deer population grows very large.", "increase in some species"),
       ("Cichlid fish in Lake Victoria split into hundreds of species with different diets.", "emergence of new species"),
       ("Finches on the Galápagos Islands evolved into many species with different beaks.", "emergence of new species"),
       ("Apple maggot flies began laying eggs on apples instead of hawthorn and are becoming separate species.", "emergence of new species"),
       ("Squirrels on two sides of the Grand Canyon became different species over a very long time.", "emergence of new species"),
       ("An asteroid impact ended the age of dinosaurs.", "extinction of species"),
       ("The golden toad of Costa Rica disappeared after its cloud forest became warmer and drier.", "extinction of species"),
       ("Passenger pigeons were hunted until none were left.", "extinction of species"),
       ("A fungus disease spread and wiped out several frog species.", "extinction of species")]
EO = ["increase in some species", "emergence of new species", "extinction of species", "no change in any species"]


def g_env():
    s, a = R.choice(ENV)
    k = R.random() < 0.6
    if not once(("e", s, k)):
        return None
    if k:
        return item("%s Which result of environmental change is this?" % s, a, [x for x in EO if x != a], "Change can help some species, make new ones and end others.")
    if a == "increase in some species":
        return item("%s Why did one species increase?" % s, "The change gave it more resources or removed a limit on its numbers.",
                    ["Every species increases after any change.", "It chose to have more young.", "Changes never help any species."], "Changes help some species and harm others.")
    if a == "emergence of new species":
        return item("%s How long did this take?" % s, "many generations", ["one generation", "one year", "a few days"], "Speciation is gradual.")
    return item("%s Why did the species go extinct?" % s, "It could not survive or adapt fast enough to the change.",
                ["It moved to another planet.", "It became a new species overnight.", "Extinctions never have causes."], "Change was faster than adaptation.")


def g_rate():
    who = P.next()[0]
    sp = R.choice(["frogs", "bees", "monarch butterflies", "coral colonies", "freshwater mussels", "songbirds", "bats", "salamanders"])
    yrs = [2000, 2005, 2010, 2015, 2020]
    a = R.choice([800, 1000, 1200, 1500, 2000, 2400])
    v = [a]
    for _ in range(4):
        v.append(v[-1] - R.randint(1, 4) * a // 20)
    k = R.choice(["drop", "pct", "low", "claim"])
    if v[-1] <= 0 or not once(("r", sp, a, tuple(v), k)) or (k == "claim" and not once(("rc", sp))) or (k == "low" and not once("rl", 3)):
        return None
    tab = table(["Year", "%s counted" % sp.capitalize()], [[str(y), comma(x)] for y, x in zip(yrs, v)])
    if k == "drop":
        i, j = sorted(R.sample(range(5), 2))
        return item(tab + "By how much did %s's count of %s fall from %d to %d?" % (who, sp, yrs[i], yrs[j]), comma(v[i] - v[j]),
                    [comma(v[j]), comma(v[i] + v[j]), comma(v[i] - v[j] + 50)], "%s − %s = %s." % (comma(v[i]), comma(v[j]), comma(v[i] - v[j])))
    if k == "pct":
        d = a - v[-1]
        pc = 100 * d / a
        if pc != int(pc):
            return None
        return item(tab + "By what percent did %s's count of %s fall from 2000 to 2020?" % (who, sp), "%d%%" % pc, ["%d%%" % (100 - pc), "%d%%" % (d // 10), "%d%%" % (pc + 10)],
                    "%s ÷ %s × 100 = %d%%." % (comma(d), comma(a), pc))
    if k == "low":
        return item(tab + "In which year did %s count the fewest %s?" % (who, sp), "2020", ["2000", "2010", "2005"], "The smallest number.")
    return item(tab + "Which claim do %s's data support about the %s?" % (who, sp), "The population is declining and could be at risk of extinction.",
                ["The population is growing fast.", "The population did not change.", "The species is already extinct."], "Steady decline.")


SOLS = [("wildlife corridor", "panthers", "habitat fragmentation"), ("catch limit", "cod", "overfishing"), ("invasive species removal", "native birds", "rats on an island"),
        ("fishing-free marine reserve", "reef fish", "overfishing"), ("wetland restoration", "ducks", "drained marshes"), ("buffer strips along streams", "trout", "farm runoff"),
        ("dam removal", "salmon", "blocked rivers"), ("native plant gardens", "pollinators", "loss of wildflowers")]


def g_sim():
    who = P.next()[0]
    sol, sp, prob = R.choice(SOLS)
    a = R.randint(30, 80) * 10
    b = a + R.randint(5, 40) * 10
    c = a - R.randint(5, 25) * 10
    k = R.choice(["best", "diff", "why", "test"])
    if not once(("s", sol, a, b, c, k)) or (k in ("why", "test", "best") and not once((k, sol))):
        return None
    tab = table(["Simulation (after 20 years)", "Number of %s" % sp], [["no action", comma(c)], ["%s" % sol, comma(b)], ["start of simulation", comma(a)]])
    if k == "best":
        return item(tab + "%s modeled ways to protect %s from %s. Which result supports using the %s?" % (who, sp, prob, sol),
                    "With the %s, the population grew to %s instead of falling to %s." % (sol, comma(b), comma(c)),
                    ["With no action, the population grew.", "The %s made no difference." % sol, "Both runs ended with the same number."], "Compare the outcomes.")
    if k == "diff":
        return item(tab + "In %s's simulation, how many more %s were there with the %s than with no action?" % (who, sp, sol), comma(b - c),
                    [comma(b - a), comma(a - c), comma(b + c)], "%s − %s = %s." % (comma(b), comma(c), comma(b - c)))
    if k == "why":
        return item(tab + "Why does %s include a 'no action' run in the simulation of %s?" % (who, sp), "It is a control to compare the solution against.",
                    ["It makes the model faster.", "It is the solution being tested.", "It has no purpose."], "A control run.")
    return item(tab + "What should %s do next to make the conclusion about the %s stronger?" % (who, sol), "Run the simulation many times and test it with real field data.",
                ["Run it once and stop.", "Change the numbers until they look good.", "Ignore the no-action run."], "Repeat and check against reality.")


B1 = bank([
    ("What is a species?", "a group of organisms that can breed and produce fertile offspring", ["any animals that look alike", "all animals in one place", "a group of different kinds"], "Biological species concept."),
    ("What is speciation?", "the formation of a new species", ["the death of a species", "the growth of one population", "a change in one animal"], "Usually takes many generations."),
    ("What usually starts speciation?", "isolation that stops two groups from interbreeding", ["one large population mixing freely", "a single mutation in one animal", "a change in weather for a day"], "Gene flow stops."),
    ("What is extinction?", "when no members of a species are left alive", ["when a species moves", "when a population shrinks a little", "when a species changes color"], "Gone forever."),
    ("What is adaptive radiation?", "one ancestor evolving into many species with different ways of life", ["one species staying the same", "many species becoming one", "a type of extinction"], "Darwin's finches."),
    ("What is a mass extinction?", "many species going extinct in a short time over large areas", ["one species going extinct", "a slow loss over millions of years", "a new species forming"], "Five big ones in Earth's history."),
    ("Can an environmental change help some species while harming others?", "Yes. It can help some, harm others and lead to new species.", ["No, all are harmed.", "No, all are helped.", "Only plants are affected."], "Different effects."),
    ("Why are many species at risk today?", "Human activities change habitats faster than species can adapt.", ["Species are too old.", "There is too much biodiversity.", "Evolution has stopped."], "Rapid change."),
])
B5 = bank([
    ("Why do scientists use simulations to test conservation plans?", "They can try many plans quickly without harming real ecosystems.", ["Simulations are always perfect.", "Field data are useless.", "They are cheaper than nothing."], "Models test ideas."),
    ("A simulation shows a corridor helps panthers. What is a limit of this result?", "The model may leave out real factors, so it should be checked in the field.", ["There are no limits.", "Models are never useful.", "Panthers cannot use corridors."], "Models simplify."),
    ("Which evidence best supports that a river split one species into two?", "DNA and traits differ more and more on the two sides over time.", ["Both sides look the same.", "One photo of a squirrel.", "The river is wide."], "Divergence."),
    ("Which change would most likely increase the risk of extinction?", "a small population that lives in only one place", ["a large population spread widely", "a species with many habitats", "a species that eats many foods"], "Small, limited ranges are risky."),
    ("Why is biodiversity important to people?", "It supports food, medicine, clean water and stable ecosystems.", ["It has no value.", "It only matters to zoos.", "It causes disease."], "Ecosystem services."),
])


def body():
    think = ("<p><b>Environmental change can grow, create or end species.</b></p>"
             "<ul><li>Some species increase when a change gives them resources.</li>"
             "<li>Isolation (geographic, behavioral, temporal, mechanical) stops interbreeding; over many generations a new species can form.</li>"
             "<li>Species that cannot adapt fast enough go extinct. Simulations help test solutions that protect biodiversity.</li></ul>")
    ex = [("A river splits squirrels into two groups. Which isolation?", ["A physical barrier"], "geographic"),
          ("Bees: 1,200 → 900. Percent drop?", ["300 ÷ 1,200 × 100"], "25%")]
    mist = ["Thinking a new species forms in one generation.", "Thinking a change affects every species the same way.", "Thinking extinction only happened to dinosaurs."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Species and isolation", B1 + [(g_iso, 6), (g_env, 6)]),
        ("Environmental change", [(g_iso, 6), (g_env, 8), (g_rate, 6)]),
        ("Population data", [(g_rate, 14), (g_env, 2), (g_sim, 4)]),
        ("Simulations", [(g_sim, 14), (g_rate, 6)]),
        ("Protecting biodiversity", B5 + [(g_sim, 6), (g_rate, 9)]),
    ])
    make("biology", "speciation-extinction-and-biodiversity", 18, "HS-LS4-5, HS-LS4-6",
         "Evaluate the evidence supporting claims that changes in environmental conditions may result in: (1) increases in the number of individuals of some species, (2) the emergence of new species over time, and (3) the extinction of other species. "
         "Create or revise a simulation to test a solution to mitigate adverse impacts of human activity on biodiversity.",
         "Speciation, Extinction and Biodiversity",
         "Speciation and Extinction Worksheets: Isolation, New Species and Biodiversity (Biology)",
         "Speciation and Extinction",
         "Free high school biology worksheets on speciation, extinction and biodiversity (NGSS HS-LS4-5, HS-LS4-6): isolation, environmental change, population data and simulations. 100 questions with answers.",
         "Change can grow, create or end species.",
         "Isolation leads to new species; species that cannot adapt go extinct.",
         body(),
         [("How does a new species form?", "A population is split by isolation. Over many generations, the groups change differently until they can no longer interbreed."),
          ("What can happen to species when the environment changes?", "Some species increase, some evolve into new species and some go extinct."),
          ("How do simulations help protect biodiversity?", "They let scientists compare solutions, such as corridors or catch limits, with a no-action control before trying them in the real world.")],
         sets)


if __name__ == "__main__":
    main()
