# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Ecosystem Changes (MS-LS2-4)
  python tools/gen_us_science_g7_ecosystem_changes.py
Construct an argument supported by empirical evidence that changes to physical or biological components of an
ecosystem affect populations: fire, flood, drought, volcanic eruption (physical); invasive species, disease,
removing a predator, overhunting (biological). Ecological succession after a disturbance. Data before and after.
Wrong answers come from real mistakes: "a change affects only one population", "ecosystems never recover",
"invasive species always help".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(70111)
R = U.R
P = People(R)

CHANGES = [("A forest fire burns a large area.", "physical"), ("A long drought dries up streams.", "physical"), ("A volcano covers land with ash.", "physical"),
           ("A flood covers a river valley with mud.", "physical"), ("A hurricane knocks down many trees.", "physical"), ("A cold snap freezes a lake for months.", "physical"),
           ("Zebra mussels from Europe spread in the Great Lakes.", "biological"), ("A disease kills many bats.", "biological"), ("Wolves are returned to a national park.", "biological"),
           ("Hunters remove most of the sea otters from a coast.", "biological"), ("Kudzu vines spread over forests in the South.", "biological"), ("Beavers build a dam on a stream.", "biological")]


def g_type():
    s, k = R.choice(CHANGES)
    who = P.next()[0]
    return item("%s reads: “%s” Is this a change to a physical (nonliving) or biological (living) part of the ecosystem?" % (who, s), k,
                ["biological" if k == "physical" else "physical", "neither", "both equally"], "Physical parts include water, soil, temperature and fire; biological parts are living things.")


EFFECTS = [("Wolves returned to Yellowstone", "elk", "decreased, and willow trees along rivers grew back", ["increased forever", "stayed exactly the same", "turned into wolves"]),
           ("Sea otters were overhunted", "sea urchins", "increased and ate the kelp forests", ["decreased", "disappeared at once", "were not affected"]),
           ("Zebra mussels spread in a lake", "native mussels", "decreased because zebra mussels outcompeted them for food", ["increased", "were not affected", "ate the zebra mussels"]),
           ("A disease killed many bats", "night-flying insects", "increased because fewer bats ate them", ["decreased", "stayed the same", "turned into bats"]),
           ("A drought dried a pond", "frogs", "decreased because they lost water and food", ["increased", "were not affected", "moved into the trees permanently"]),
           ("Cane toads were brought to Australia", "native predators that ate the toxic toads", "decreased because the toads poisoned them", ["increased", "were not affected", "became toads"])]


def g_effect():
    ch, pop, a, w = R.choice(EFFECTS)
    who = P.next()[0]
    return item("%s learns: %s. What happened to the %s?" % (who, ch, pop), "They " + a + ".", ["They " + x + "." for x in w],
                "A change to one part of an ecosystem affects other populations.")


def g_data():
    sp = R.choice([("native fish", "an invasive fish"), ("songbirds", "outdoor cats"), ("native plants", "an invasive vine"), ("frogs", "a fungus disease")])
    years = ["2015", "2016", "2017", "2018", "2019"]
    start = R.randint(70, 95)
    vals = [start, start - R.randint(0, 3), start - R.randint(15, 25), start - R.randint(30, 40), start - R.randint(40, 55)]
    ch = bar_chart(years, vals, sp[0], "bar graph of a population over time", ymax=100, step=20, w=340)
    who = P.next()[0]
    if R.random() < 0.5:
        return item(fig(ch) + "%s's graph shows %s in a lake area. %s arrived in 2016. Which claim does the data support?" % (who, sp[0], sp[1][0].upper() + sp[1][1:]),
                    "The %s population declined after %s arrived." % (sp[0], sp[1]), ["The %s population grew after %s arrived." % (sp[0], sp[1]), "Nothing changed.", "The graph shows the arrival caused growth."],
                    "The numbers drop after 2016.")
    return item(fig(ch) + "By how much did %s decrease from 2015 to 2019 in %s's data?" % (sp[0], who), "%d" % (vals[0] - vals[-1]),
                ["%d" % vals[-1], "%d" % vals[0], "%d" % (vals[0] - vals[2])], "%d − %d = %d." % (vals[0], vals[-1], vals[0] - vals[-1]))


SUCC = ["bare soil or rock", "grasses and wildflowers", "shrubs and small trees", "a mature forest"]


def g_succ():
    i = R.randrange(3)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s studies a burned forest recovering over many years. Which stage comes after “%s”?" % (who, SUCC[i]), SUCC[i + 1],
                    [s for s in SUCC if s not in (SUCC[i], SUCC[i + 1])] + ["the same stage forever"], "This gradual recovery is called succession.")
    return item("%s watches an abandoned farm field over 50 years. What process is changing the field from grasses to forest?" % who, "ecological succession",
                ["photosynthesis only", "erosion", "migration"], "Communities change over time after a disturbance.")


B1 = bank([
    ("What is an ecosystem?", "all the living and nonliving things in an area and how they interact", ["only the animals in an area", "only the weather", "a single population"], "Soil, water, plants and animals together."),
    ("What is an invasive species?", "a species brought to a new area where it spreads and harms native species", ["a native species", "an extinct species", "a species that helps every other species"],
     "Zebra mussels and kudzu are invasive."),
    ("Can a small change affect many populations?", "Yes. Populations are connected through food webs and resources.", ["No, only one population is affected.", "Only plants are affected.", "Only predators are affected."],
     "Effects ripple through ecosystems."),
    ("What is ecological succession?", "the gradual change in the kinds of organisms in an area over time", ["a sudden flood", "the movement of animals each season", "a type of predator"],
     "After a fire, grasses come first, then shrubs, then trees."),
    ("Which is a biological change to an ecosystem?", "a new disease spreads among deer", ["a flood", "a drought", "a volcanic eruption"], "Living things are biological components."),
    ("Which is a physical change to an ecosystem?", "a wildfire", ["a new predator moves in", "an invasive plant spreads", "a disease kills fish"], "Fire, water and temperature are physical."),
    ("Why do scientists collect data before and after a change?", "to show how the change affected populations", ["to make graphs colorful", "because data never changes", "to stop the change"],
     "Evidence supports arguments."),
    ("Can ecosystems recover after a disturbance?", "Often yes, through succession, though it can take many years.", ["Never.", "Always within a day.", "Only if people build them again."],
     "Recovery takes time."),
])
B5 = bank([
    ("Ava claims that removing wolves caused elk to overeat willows. Which evidence supports her claim best?", "Willows grew back after wolves returned and elk numbers dropped.", ["Wolves howl at night.", "Elk have antlers.", "Willows are green."],
     "Before-and-after data links the cause and effect."),
    ("Leo finds that a lake with zebra mussels has clearer water but fewer native mussels. What does this show?", "A change can help some parts of an ecosystem and harm others.", ["Zebra mussels only help.", "Nothing changed.", "Clear water means more native mussels."],
     "Effects can be mixed."),
    ("Mia compares two forests: one burned 5 years ago and one burned 50 years ago. Which has more large trees?", "the forest burned 50 years ago", ["the forest burned 5 years ago", "They are the same.", "Neither has trees."],
     "Succession takes many years."),
    ("Why should claims about ecosystem changes be supported by data from many years?", "Populations naturally go up and down, so long-term data shows real trends.", ["One year is always enough.", "Data is not needed.", "Populations never change."],
     "Empirical evidence over time."),
    ("A dam turns a river into a lake. Which population will most likely increase?", "fish that live in still water", ["fish that need fast-flowing water", "desert lizards", "cactus"], "The physical change favors some species."),
])


def body():
    think = ("<p>Ecosystems have <b>physical</b> parts (water, soil, temperature, sunlight) and <b>biological</b> parts (living things). A change to any part can affect many populations.</p>"
             "<ul><li>Physical changes: fire, flood, drought, volcanic eruptions, hurricanes.</li>"
             "<li>Biological changes: invasive species, disease, adding or removing a predator, overhunting.</li></ul>"
             "<p>Because organisms are connected in food webs, a change can ripple through: removing sea otters let urchins increase and destroy kelp forests. "
             "After a disturbance, ecosystems often recover slowly through <b>succession</b>. Scientists use <b>data from before and after</b> to support their arguments.</p>")
    ex = [("A disease kills many bats. What happens to insects they ate?", ["Fewer predators."], "The insects increase."),
          ("Is a drought a physical or biological change?", ["Water is nonliving."], "physical")]
    mist = ["Thinking a change affects only one population.",
            "Thinking ecosystems never recover.",
            "Making a claim without data from before and after the change."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Physical and biological changes", B1 + [(g_type, 12)]),
        ("Effects on populations", [(g_effect, 12), (g_type, 8)]),
        ("Population data", [(g_data, 14), (g_effect, 6)]),
        ("Succession", [(g_succ, 10), (g_data, 6), (g_effect, 4)]),
        ("Arguments from evidence", B5 + [g_data, g_effect, g_succ, g_type]),
    ])
    make("grade-7", "ecosystem-changes", 11, "MS-LS2-4",
         "Construct an argument supported by empirical evidence that changes to physical or biological components of an ecosystem affect populations.",
         "Ecosystem Changes",
         "Grade 7 Ecosystem Change Worksheets: Disturbances, Invasive Species and Succession",
         "Ecosystem Changes",
         "Free middle school science worksheets on ecosystem changes (NGSS MS-LS2-4): physical and biological changes, invasive species, predators and disease, population data and ecological succession. 100 practice questions with answers.",
         "Changes to an ecosystem affect its populations.",
         "Fires, droughts, invasive species and disease change which populations grow or shrink. Data shows the effects.",
         body(),
         [("What kinds of changes affect ecosystems?", "Physical changes such as fires, floods and droughts, and biological changes such as invasive species, disease and the loss of predators."),
          ("Why can one change affect many populations?", "Organisms are connected through food webs and shared resources, so a change to one population affects others."),
          ("What is ecological succession?", "The gradual change in the community of organisms in an area over many years, such as a burned forest growing back.")],
         sets)


if __name__ == "__main__":
    main()
