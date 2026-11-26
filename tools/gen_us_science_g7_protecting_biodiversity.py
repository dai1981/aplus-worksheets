# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Protecting Biodiversity (MS-LS2-5)
  python tools/gen_us_science_g7_protecting_biodiversity.py
Evaluate competing design solutions for maintaining biodiversity and ecosystem services (water purification,
pollination, nutrient recycling, erosion prevention, food). Solutions: wildlife corridors, protected areas,
removing invasive species, fish ladders, pollinator gardens, sustainable fishing limits, restoring wetlands.
Compare solutions with criteria and constraints (cost, effectiveness, effects on people).
Wrong answers come from real mistakes: "biodiversity means many individuals of one species",
"ecosystem services are only things people sell", "the cheapest solution is always best".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70112)
R = U.R
P = People(R)

SERV = [("bees pollinate fruit trees", "pollination"), ("wetlands filter dirty water", "water purification"), ("tree roots hold soil on hillsides", "erosion prevention"),
        ("decomposers break down dead leaves", "nutrient recycling"), ("forests take in carbon dioxide", "climate regulation"), ("oceans provide fish to eat", "food"),
        ("marshes soak up floodwater", "flood control"), ("plants release oxygen", "oxygen production")]


def g_serv():
    s, k = R.choice(SERV)
    who = P.next()[0]
    return item("%s learns that %s. Which ecosystem service is this?" % (who, s), k, R.sample([x[1] for x in SERV if x[1] != k], 3), "Ecosystem services are benefits people get from healthy ecosystems.")


PROB = [("Deer and bears are killed crossing a new highway.", "build wildlife overpasses or tunnels", ["widen the highway", "remove all nearby forest", "add brighter lights"]),
        ("Salmon cannot swim past a dam to lay eggs.", "add a fish ladder beside the dam", ["make the dam taller", "remove the salmon", "pour sand into the river"]),
        ("Bee populations are falling near farms.", "plant wildflower strips and reduce pesticide use", ["spray more pesticide", "remove all flowers", "pave the field edges"]),
        ("An invasive vine is smothering native plants.", "remove the vine and replant native species", ["plant more of the vine", "do nothing ever", "burn all the native plants"]),
        ("A fish population is shrinking from overfishing.", "set catch limits and protected zones", ["allow unlimited fishing", "catch the smallest fish first", "drain the lake"]),
        ("A wetland was drained and nearby towns now flood.", "restore the wetland", ["build more parking lots", "drain more wetlands", "cut the nearby trees"]),
        ("Forest animals are trapped in small patches between farms.", "connect the patches with wildlife corridors", ["remove more trees", "build fences around each patch", "add more farms"])]


def g_sol():
    p_, a, w = R.choice(PROB)
    who = P.next()[0]
    return item("%s's class studies this problem: “%s” Which solution would best protect biodiversity?" % (who, p_), a, w, "It solves the cause of the problem while protecting species.")


def g_matrix():
    sols = R.sample(["wildlife overpass", "underpass tunnel", "fence with gaps", "warning signs", "lower speed limit"], 3)
    crit = ["Effectiveness", "Cost (5 = cheapest)", "Effect on drivers"]
    while True:
        sc = [[R.randint(1, 5) for _ in crit] for _ in sols]
        tot = [sum(r) for r in sc]
        if len(set(tot)) == 3:
            break
    rows = [[s] + ["%d" % v for v in r] + ["%d" % t] for s, r, t in zip(sols, sc, tot)]
    tab = table(["Solution"] + crit + ["Total"], rows)
    who = P.next()[0]
    k = R.choice(["total", "eff"])
    if k == "total":
        a = sols[tot.index(max(tot))]
        return item(tab + "%s's town wants to protect deer crossing a road. Which solution scores best overall?" % who, a, [s for s in sols if s != a] + ["They tie."],
                    "%s has the highest total (%d)." % (a, max(tot)))
    col = [r[0] for r in sc]
    if col.count(max(col)) > 1:
        return None
    a = sols[col.index(max(col))]
    return item(tab + "If %s's town cares most about effectiveness, which solution should it choose?" % who, a, [s for s in sols if s != a] + ["the cheapest one"],
                "%s scored %d for effectiveness." % (a, max(col)))


B1 = bank([
    ("What is biodiversity?", "the variety of different species and living things in an area", ["the number of individuals of one species", "the amount of water in an area", "the size of the largest animal"],
     "More kinds of living things means more biodiversity."),
    ("Why is biodiversity important for ecosystems?", "Ecosystems with many species are more stable and recover better from changes.", ["It makes ecosystems weaker.", "It is not important.", "It only matters in zoos."],
     "Many species can fill each role."),
    ("What are ecosystem services?", "benefits people get from ecosystems, like clean water, pollination and food", ["services sold at a store", "only tourist trips", "services only for animals"],
     "Healthy ecosystems help people."),
    ("Which human activity most reduces biodiversity?", "destroying habitats to build roads and cities", ["planting native gardens", "protecting parks", "recycling"], "Habitat loss is the biggest threat."),
    ("What is a wildlife corridor?", "a strip of habitat that connects separated areas so animals can move between them", ["a road for cars", "a fence that keeps animals in", "a zoo hallway"],
     "Corridors help populations stay connected."),
    ("When comparing solutions, what is a constraint?", "a limit such as cost, time or space", ["the goal of the solution", "the best solution", "a type of species"], "Constraints limit possible solutions."),
    ("Why might a town choose a more expensive solution?", "It works much better and meets the most important criteria.", ["Expensive is always better.", "Cost never matters.", "To waste money."],
     "Balance criteria and constraints."),
    ("How do bees help people?", "They pollinate many of the crops we eat.", ["They make soil.", "They clean water.", "They stop floods."], "Pollination is an ecosystem service."),
])
B5 = bank([
    ("Ava's class compares two plans: a fence (cheap, protects 40% of deer) and an overpass (expensive, protects 90%). The criterion is to protect at least 80%. Which plan meets it?", "the overpass", ["the fence", "both", "neither"],
     "Only the overpass meets the criterion."),
    ("Leo argues for restoring a wetland instead of building a concrete flood wall. Which evidence supports his argument?", "Wetlands control floods and also provide habitat and clean water.", ["Wetlands cost nothing.", "Flood walls are always useless.", "Wetlands are pretty."],
     "Multiple ecosystem services add value."),
    ("Mia counts 25 species in a protected park and 6 in a nearby parking-lot edge. What does this suggest?", "Protecting habitat helps maintain biodiversity.", ["Parking lots increase biodiversity.", "Parks have fewer species.", "Counting species is not useful."],
     "Data supports the claim."),
    ("Why do scientists monitor a solution after it is built?", "to check if it actually maintains biodiversity and improve it if needed", ["to make it more expensive", "because nothing ever changes", "to remove it right away"],
     "Evaluate and improve."),
    ("A fishing town needs jobs and healthy fish populations. Which solution balances both?", "set fishing seasons and catch limits", ["ban all fishing forever", "allow unlimited fishing", "drain the fishing grounds"],
     "Good solutions consider people and the ecosystem."),
])


def body():
    think = ("<p><b>Biodiversity</b> is the variety of living things in an area. Ecosystems with high biodiversity are more stable and provide <b>ecosystem services</b>: clean water, pollination, food, flood control, fertile soil and oxygen.</p>"
             "<p>Human activities like habitat loss, pollution, overfishing and invasive species reduce biodiversity. People design <b>solutions</b>: wildlife corridors and overpasses, fish ladders, protected areas, restoring wetlands, removing invasive species and planting pollinator gardens.</p>"
             "<p>To <b>evaluate competing solutions</b>, compare how well each meets the <b>criteria</b> (protects species and services) and <b>constraints</b> (cost, space, effects on people), often with a decision matrix.</p>")
    ex = [("Wetlands filtering water is which ecosystem service?", ["Cleaning water."], "water purification"),
          ("Animals die crossing a highway. Name a solution.", ["They need a safe way to cross."], "a wildlife overpass or tunnel")]
    mist = ["Thinking biodiversity means many individuals of one species.",
            "Thinking ecosystem services are only things people buy.",
            "Choosing the cheapest solution without checking if it works."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Biodiversity and ecosystem services", B1 + [(g_serv, 12)]),
        ("Ecosystem services", [(g_serv, 12), (g_sol, 8)]),
        ("Design solutions", [(g_sol, 14), (g_matrix, 6)]),
        ("Comparing solutions", [(g_matrix, 14), (g_sol, 6)]),
        ("Evaluating evidence", B5 + [g_matrix, g_sol, g_serv]),
    ])
    make("grade-7", "protecting-biodiversity", 12, "MS-LS2-5",
         "Evaluate competing design solutions for maintaining biodiversity and ecosystem services.",
         "Protecting Biodiversity",
         "Grade 7 Biodiversity Worksheets: Ecosystem Services and Design Solutions",
         "Protecting Biodiversity",
         "Free middle school science worksheets on protecting biodiversity (NGSS MS-LS2-5): biodiversity, ecosystem services, wildlife corridors and other solutions, and comparing solutions with decision matrices. 100 practice questions with answers.",
         "Biodiversity keeps ecosystems healthy.",
         "People can protect species and ecosystem services with solutions like wildlife corridors, and compare them using criteria and constraints.",
         body(),
         [("What is biodiversity?", "The variety of different species and other living things in an area."),
          ("What are ecosystem services?", "Benefits that healthy ecosystems give people, such as clean water, pollination, food, flood control and fertile soil."),
          ("How do you compare solutions for protecting biodiversity?", "Score each solution against the criteria and constraints, such as how well it works, its cost and its effects on people.")],
         sets)


if __name__ == "__main__":
    main()
