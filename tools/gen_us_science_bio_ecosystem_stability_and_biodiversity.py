# -*- coding: utf-8 -*-
"""
US High School Biology: Ecosystem Stability and Biodiversity (HS-LS2-6, HS-LS2-7)
  python tools/gen_us_science_bio_ecosystem_stability_and_biodiversity.py
Evaluate claims that complex interactions in ecosystems maintain relatively consistent numbers and types of organisms in
stable conditions, but changing conditions may result in a new ecosystem; design, evaluate and refine a solution for
reducing the impacts of human activities on the environment and biodiversity.
Disturbances, primary and secondary succession, keystone species, invasive species, species richness from survey data,
and solutions to human impacts.
Wrong answers come from real mistakes: "an ecosystem never changes", "more individuals means more biodiversity",
"invasive species are always harmless".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(90111)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SUCC = [("Lava cools into new bare rock. Lichens grow first.", "primary succession"), ("A glacier melts back and leaves bare rock.", "primary succession"),
        ("A new volcanic island rises from the sea.", "primary succession"), ("A forest fire burns trees but leaves the soil.", "secondary succession"),
        ("A farm field is abandoned and weeds move in.", "secondary succession"), ("A hurricane knocks down trees; soil and seeds remain.", "secondary succession"),
        ("Loggers clear a forest, and shrubs grow back.", "secondary succession"), ("A landslide scrapes a slope down to bare bedrock.", "primary succession")]


def g_succ():
    s, a = R.choice(SUCC)
    if not once(s):
        return None
    return item("%s Which kind of succession follows?" % s, a, [x for x in ["primary succession", "secondary succession", "no succession", "extinction"] if x != a],
                "Primary starts with no soil; secondary starts where soil remains.")


def g_survey():
    who = P.next()[0]
    sp = ["oak", "maple", "pine", "fern", "moss", "beetle", "spider", "salamander", "sparrow", "squirrel"]
    A = {s: R.randint(1, 12) for s in R.sample(sp, R.randint(5, 8))}
    B = {s: R.randint(10, 60) for s in R.sample(sp, R.randint(2, 4))}
    if len(A) == len(B) or not once((tuple(sorted(A)), tuple(sorted(B)))):
        return None
    k = R.choice(["rich", "count", "ind", "more"])
    rows = [[s, str(A.get(s, 0)), str(B.get(s, 0))] for s in sp if s in A or s in B]
    tab = table(["Species", "Site A count", "Site B count"], rows)
    na, nb = sum(A.values()), sum(B.values())
    if k == "rich":
        return item(tab + "%s surveyed two sites. How many species were found at site A?" % who, str(len(A)), [str(len(B)), str(na), str(len(rows))],
                    "Count the species with a number above 0 at site A.")
    if k == "count":
        return item(tab + "How many individual organisms did %s count at site B?" % who, str(nb), [str(len(B)), str(na), str(nb + 10)], "Add site B's column.")
    if k == "ind":
        return item(tab + "Which site has greater biodiversity in %s's survey?" % who,
                    "site A", ["site B", "They are equal.", "Neither has any."], "Biodiversity depends on the number of different species (and evenness).")
    return item(tab + "Which site in %s's survey is likely to recover better from a disease that kills one species?" % who, "site A, because it has more species",
                ["site B, because it has more individuals", "Neither can recover.", "Both are exactly the same."], "More diverse ecosystems are more stable.")


DIST = [("A new road splits a forest in two.", "habitat fragmentation"), ("Fertilizer runoff causes algae blooms in a lake.", "pollution"),
        ("Burmese pythons spread through the Everglades.", "invasive species"), ("Too many fish are caught each year.", "overharvesting"),
        ("Warmer oceans bleach coral reefs.", "climate change"), ("A wetland is drained to build houses.", "habitat destruction"),
        ("Zebra mussels clog Great Lakes pipes and outcompete native mussels.", "invasive species"), ("Plastic waste collects in the ocean.", "pollution")]
SOL = {"habitat fragmentation": "build wildlife corridors or overpasses", "pollution": "reduce runoff and waste with buffers and better treatment",
       "invasive species": "remove the invaders and check boats and cargo", "overharvesting": "set catch limits and protected areas",
       "climate change": "reduce greenhouse gas emissions", "habitat destruction": "protect and restore habitats"}


def g_dist():
    s, a = R.choice(DIST)
    k = R.random() < 0.5
    if not once((s, k)):
        return None
    if k:
        return item("%s Which human impact is this?" % s, a, R.sample([x for x in SOL if x != a], 3), "Name the threat to biodiversity.")
    return item("%s Which solution best fits this problem?" % s, SOL[a], R.sample([SOL[x] for x in SOL if x != a], 3), "Match the solution to the cause.")


KEY = [("Sea otters eat sea urchins, which eat kelp. Otters disappear.", "Urchins increase and kelp forests shrink."),
       ("Wolves return to Yellowstone and hunt elk.", "Elk browse less by rivers, and willows and beavers return."),
       ("Beavers build dams that create ponds.", "Many new wetland species can live there."),
       ("A disease kills most of the starfish on a rocky shore.", "Mussels take over and fewer species remain.")]


def g_key():
    s, a = R.choice(KEY)
    if not once(s):
        return None
    return item("%s What is the most likely result?" % s, a, R.sample([x[1] for x in KEY if x[1] != a], 2) + ["Nothing changes in the ecosystem."], "A keystone species has a large effect.")


def g_data():
    who = P.next()[0]
    years = [2016, 2018, 2020, 2022, 2024]
    base = R.randint(40, 70)
    drop = R.randint(4, 9)
    vals = [base, base - drop, base - 2 * drop, base - 2 * drop + R.randint(1, 3), base - 2 * drop + R.randint(4, 8)]
    k = R.choice(["low", "change", "claim"])
    if not once((base, drop, k)):
        return None
    tab = table(["Year", "Native fish species in the river"], [[str(y), str(v)] for y, v in zip(years, vals)])
    if k == "low":
        return item(tab + "A dam was built in 2016 and removed in 2020. When was the number of species lowest in %s's data?" % who, "2020", ["2016", "2024", "2018"], "The smallest number: %d." % min(vals))
    if k == "change":
        return item(tab + "How many species did %s's river lose from 2016 to 2020?" % who,
                    str(vals[0] - vals[2]), [str(vals[2]), str(vals[0]), str(vals[0] - vals[2] + 3)], "%d − %d = %d." % (vals[0], vals[2], vals[0] - vals[2]))
    return item(tab + "The dam was removed in 2020. Which claim do %s's data support?" % who, "Species began to return after the dam was removed.", ["Removing the dam made things worse.", "The river never changed.", "Dams increase biodiversity."],
                "Numbers rose after 2020.")


B1 = bank([
    ("What is biodiversity?", "the variety of living things in an area", ["the number of animals of one kind", "the size of an ecosystem", "the amount of rain"], "Many kinds of species."),
    ("Why are diverse ecosystems more stable?", "If one species declines, others can fill its role.", ["They have fewer species.", "They never face disturbances.", "Diversity has no effect."], "Redundancy."),
    ("What is ecological succession?", "a gradual change in the species in an area over time", ["a sudden extinction", "a kind of migration", "a single storm"], "Pioneer → climax."),
    ("What are pioneer species?", "the first organisms to live in a bare area, like lichens and mosses", ["the top predators", "animals that migrate", "trees in an old forest"], "They start soil formation."),
    ("What is a keystone species?", "a species with a large effect on its ecosystem compared with its numbers", ["the most common species", "a species found only in caves", "any plant"], "Like sea otters."),
    ("What is an invasive species?", "a non-native species that spreads and harms an ecosystem", ["any native species", "a species that is endangered", "a species that migrates"], "Zebra mussels, pythons."),
    ("Can a stable ecosystem change into a new kind of ecosystem?", "Yes, if conditions change enough.", ["No, never.", "Only on Mars.", "Only in labs."], "New ecosystems can form."),
    ("Which human activity is the biggest threat to biodiversity today?", "habitat destruction", ["planting gardens", "bird watching", "recycling"], "Loss of habitat."),
])
B5 = bank([
    ("A town wants to protect frogs that cross a road to breed. Which solution is best?", "a tunnel under the road", ["a wider road", "more streetlights", "a parking lot"], "Wildlife crossings."),
    ("An engineer designs a fish ladder for a dam. What problem does it solve?", "It lets fish swim upstream past the dam to spawn.", ["It makes more electricity.", "It stops all fish.", "It cleans plastic."], "Reduce human impact."),
    ("A student claims a 'pretty' imported plant is harmless. What evidence would test this claim?", "data on whether it spreads and crowds out native plants", ["a photo of its flowers", "its price", "its color"], "Evaluate with evidence."),
    ("A lake's species count drops after farms upstream use more fertilizer. Which solution helps most?", "planting buffer strips to catch runoff", ["adding more fertilizer", "draining the lake", "building a parking lot"], "Stop the cause."),
    ("Why do scientists compare a disturbed area with an undisturbed one?", "to measure the effect of the disturbance", ["to make the test harder", "to count rocks", "for no reason"], "A control site."),
])


def body():
    think = ("<p><b>Stable ecosystems stay similar; big changes can make new ones.</b></p>"
             "<ul><li>Many interacting species keep numbers fairly steady. More biodiversity → more stability.</li>"
             "<li>After a disturbance: <b>primary succession</b> (no soil) or <b>secondary succession</b> (soil remains).</li>"
             "<li>Human impacts (habitat loss, pollution, invasive species, overharvesting, climate change) need targeted solutions.</li></ul>")
    ex = [("A fire burns a forest but leaves soil. Which succession?", ["Soil remains"], "secondary"),
          ("Site A: 8 species, 40 animals. Site B: 2 species, 100 animals. More biodiverse?", ["Count species, not individuals"], "site A")]
    mist = ["Thinking an ecosystem never changes.", "Thinking more individuals means more biodiversity.", "Thinking invasive species are harmless."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stability and change", B1 + [(g_succ, 6), (g_key, 2), (g_dist, 4)]),
        ("Succession", [(g_succ, 2), (g_dist, 6), (g_survey, 8), (g_key, 2), (g_data, 2)]),
        ("Measuring biodiversity", [(g_survey, 14), (g_data, 6)]),
        ("Human impacts", [(g_dist, 6), (g_data, 8), (g_survey, 6)]),
        ("Designing solutions", B5 + [(g_survey, 10), (g_data, 5)]),
    ])
    make("biology", "ecosystem-stability-and-biodiversity", 11, "HS-LS2-6, HS-LS2-7",
         "Evaluate claims, evidence, and reasoning that the complex interactions in ecosystems maintain relatively consistent numbers and types of organisms in stable conditions, but changing conditions may result in a new ecosystem. "
         "Design, evaluate, and refine a solution for reducing the impacts of human activities on the environment and biodiversity.",
         "Ecosystem Stability and Biodiversity",
         "Biodiversity Worksheets: Succession, Invasive Species and Human Impacts (Biology)",
         "Biodiversity",
         "Free high school biology worksheets on ecosystem stability and biodiversity (NGSS HS-LS2-6, HS-LS2-7): succession, keystone and invasive species, survey data and solutions. 100 questions with answers.",
         "Biodiversity keeps ecosystems stable.",
         "Big changes can create a new ecosystem; smart solutions reduce human impacts.",
         body(),
         [("What is the difference between primary and secondary succession?", "Primary succession starts on bare rock with no soil. Secondary succession starts after a disturbance that leaves soil behind."),
          ("Why does biodiversity make ecosystems more stable?", "With many species, if one declines, others can fill its role, so the ecosystem recovers better."),
          ("How can people reduce their impact?", "Protect habitats, build wildlife corridors, control invasive species, set catch limits and reduce pollution and emissions.")],
         sets)


if __name__ == "__main__":
    main()
