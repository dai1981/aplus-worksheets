# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Weather Hazards (3-ESS3-1)
  python tools/gen_us_science_g3_weather_hazards.py
Make a claim about the merit of a design solution that reduces the impacts of a weather-related hazard:
floods (levees, raised houses), hurricanes (shutters, strong roofs, evacuation), tornadoes (storm shelters,
warning sirens), lightning (lightning rods), blizzards (snowplows, snow fences), droughts (rain barrels,
water-saving), high winds (windbreaks). Compare solutions using evidence.
Wrong answers come from real mistakes: "people can stop storms", "a solution for one hazard works for all",
"the cheapest solution is always best".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(30115)
R = U.R
P = People(R)

SOL = {"flood": ["building a levee along the river", "raising houses on posts", "storm drains that carry water away", "a dam upstream that holds back water", "planting a rain garden that soaks up water"],
       "hurricane": ["putting storm shutters over windows", "strapping roofs tightly to the walls", "a seawall along the coast", "planning evacuation routes inland", "building houses that can stand strong winds"],
       "tornado": ["building an underground storm shelter", "warning sirens that sound when a tornado is near", "a safe room with strong concrete walls", "practicing tornado drills at school"],
       "lightning": ["a lightning rod on the roof", "going indoors when thunder roars", "surge protectors for computers and TVs"],
       "blizzard": ["snowplows that clear the roads", "snow fences that stop snow from drifting onto roads", "salt spread on icy roads", "keeping extra blankets and food at home"],
       "drought": ["rain barrels that collect water", "planting crops that need little water", "drip hoses that water roots slowly", "fixing leaky pipes to save water"]}
PL = {"flood": "floods", "hurricane": "hurricanes", "tornado": "tornadoes", "lightning": "lightning", "blizzard": "blizzards", "drought": "droughts"}
GENERIC = ("evacuation", "warning", "drills", "houses that can stand", "blankets", "seawall", "dam")


def cap(s):
    return s[0].upper() + s[1:]


def g_which():
    h = R.choice(sorted(SOL))
    a = R.choice(SOL[h])
    close = [{"flood", "hurricane"}, {"tornado", "hurricane"}, {"flood", "drought"}]
    w = [x for k in SOL if k != h and {k, h} not in close for x in SOL[k] if not any(g in x for g in GENERIC)]
    p = P.next()
    return item("%s's town often has %s. Which solution would best reduce the damage from %s?" % (p[0], PL[h], PL[h]), a, R.sample(w, 3), "%s helps with %s." % (cap(a), PL[h]))


def g_what():
    h = R.choice(sorted(SOL))
    a = R.choice([x for x in SOL[h] if not any(g in x for g in GENERIC)])
    p = P.next()
    close = [{"flood", "hurricane"}, {"tornado", "hurricane"}]
    return item("%s sees a town using %s. Which weather hazard is this mainly for?" % (p[0], a), PL[h], [PL[x] for x in R.sample([k for k in SOL if k != h and {k, h} not in close], 3)],
                "This solution reduces the impact of %s." % PL[h])


def g_data():
    h = R.choice(["flood", "blizzard", "hurricane"])
    sol = R.choice([x for x in SOL[h] if not any(g in x for g in GENERIC)])
    what = {"flood": "homes flooded", "blizzard": "car accidents", "hurricane": "homes damaged"}[h]
    before = R.randint(20, 60)
    after = R.randint(3, before - 8)
    ch = bar_chart(["before", "after"], [before, after], what, "bar graph before and after a solution", ymax=70, step=10, w=230)
    p = P.next()
    k = R.choice(["claim", "diff"])
    if k == "claim":
        return item(fig(ch) + "%s's town tried %s to protect against %s. Which claim does the data support?" % (p[0], sol, PL[h]),
                    "The solution reduced the damage.", ["The solution made the damage worse.", "The solution did nothing.", "The solution stopped %s from happening." % PL[h]],
                    "%s went from %d to %d. The hazard still happens, but it does less damage." % (cap(what), before, after))
    return item(fig(ch) + "%s's town tried %s. How many fewer %s were there after the solution?" % (p[0], sol, what), "%d" % (before - after),
                ["%d" % before, "%d" % after, "%d" % (before + after)], "%d − %d = %d." % (before, after, before - after))


def g_compare():
    h = R.choice(sorted(SOL))
    if len(SOL[h]) < 3:
        return None
    opts = R.sample(SOL[h], 3)
    cost = R.sample([1, 2, 5, 10, 20, 40], 3)
    prot = R.sample(["some", "good", "great"], 3)
    rows = [[cap(o), "$%d,000" % c, pr] for o, c, pr in zip(opts, cost, prot)]
    tab = table(["Solution", "Cost", "Protection"], rows)
    p = P.next()
    k = R.choice(["best", "cheap", "budget"])
    rank = {"some": 0, "good": 1, "great": 2}
    if k == "best":
        a = opts[prot.index("great")]
        return item(tab + "%s's town is comparing ways to deal with %s. Which gives the most protection?" % (p[0], PL[h]), cap(a), [cap(o) for o in opts if o != a] + ["They are all the same."],
                    "It gives great protection.")
    if k == "cheap":
        a = opts[cost.index(min(cost))]
        return item(tab + "%s's town is comparing ways to deal with %s. Which costs the least?" % (p[0], PL[h]), cap(a), [cap(o) for o in opts if o != a] + ["They all cost the same."],
                    "It costs $%d,000." % min(cost))
    budget = R.choice([2, 5, 10, 20])
    ok = [o for o, c in zip(opts, cost) if c <= budget]
    if not ok or len(ok) == 3:
        return None
    a = max(ok, key=lambda o: rank[prot[opts.index(o)]])
    return item(tab + "%s's town can spend at most $%d,000 on %s. Which solution gives the most protection for that money?" % (p[0], budget, PL[h]), cap(a),
                [cap(o) for o in opts if o != a] + ["none of them"], "Only solutions that cost $%d,000 or less fit. Of those, this one protects best." % budget)


B1 = bank([
    ("What is a weather hazard?", "dangerous weather that can harm people or property, like a flood or tornado", ["a sunny day", "a gentle breeze", "a rainbow"],
     "Floods, hurricanes, tornadoes, lightning, blizzards and droughts are weather hazards."),
    ("Can people stop a hurricane?", "No, but they can prepare and reduce the damage.", ["Yes, with big fans.", "Yes, with walls.", "Yes, by closing windows."],
     "We cannot control weather, but we can design solutions."),
    ("What does a levee do?", "holds back a river so it does not flood towns", ["makes tornadoes smaller", "stops lightning", "melts snow"], "Levees are walls along rivers."),
    ("Where is the safest place during a tornado?", "an underground shelter or an inside room with no windows on the lowest floor", ["outside in an open field", "next to a big window", "in a car on the highway"],
     "Stay low and away from windows."),
    ("What does a lightning rod do?", "carries lightning safely into the ground", ["makes lightning", "stops rain", "warns about floods"], "It protects buildings."),
    ("Why do some houses near the coast sit on tall posts?", "so flood water and storm waves can pass under them", ["so they are closer to the sun", "to stop tornadoes", "to catch rain"],
     "Raised houses stay dry during floods."),
    ("What should you do when you hear thunder outside?", "go indoors right away", ["stand under a tall tree", "go swimming", "fly a kite"], "When thunder roars, go indoors."),
    ("How can weather forecasts help people?", "They warn people early so they can get ready", ["They stop storms.", "They make storms bigger.", "They are only for fun."],
     "Warnings give time to prepare."),
])
B5 = bank([
    ("Ava's class builds model houses and tests them with a fan. One roof is strapped down and one is not. Which should stay on?", "the strapped roof", ["the roof that is not strapped", "Both blow off.", "Neither moves at all."],
     "Straps hold roofs on in strong winds."),
    ("Leo says a town should build a levee. Which evidence would best support his claim?", "Towns with levees had fewer flooded homes.", ["Levees look nice.", "Levees are tall.", "His friend likes levees."],
     "Data about damage is good evidence."),
    ("Mia's town has many droughts. Which plan has the most merit?", "collect rainwater in barrels and plant crops that need less water", ["water lawns more often", "build snow fences", "add more lightning rods"],
     "The plan matches the hazard."),
    ("Two designs for a storm shelter both keep people safe. Design A costs much less. Which should the town choose?", "Design A, because it meets the goal for less money", ["Design B, because it costs more", "neither", "both, built on top of each other"],
     "Compare criteria and constraints."),
    ("Why might a solution for floods not help with blizzards?", "Each hazard causes different problems, so it needs its own solution.", ["Floods and blizzards are the same.", "Solutions work for every hazard.", "Blizzards never cause problems."],
     "Match the solution to the hazard."),
])


def body():
    think = ("<p><b>Weather hazards</b> are dangerous weather events: floods, hurricanes, tornadoes, lightning, blizzards and droughts. "
             "People cannot stop them, but they can <b>design solutions</b> that reduce the damage.</p>"
             "<ul><li>Floods: levees, houses on posts, storm drains.</li><li>Hurricanes: storm shutters, strapped roofs, evacuation routes.</li>"
             "<li>Tornadoes: storm shelters, warning sirens.</li><li>Lightning: lightning rods; go indoors.</li>"
             "<li>Blizzards: snowplows, snow fences. Droughts: rain barrels, saving water.</li></ul>"
             "<p>To make a claim about a solution's <b>merit</b>, compare evidence: Does it reduce the damage? How much does it cost?</p>")
    ex = [("Which solution helps with lightning?", ["Lightning strikes tall buildings."], "a lightning rod"),
          ("Flooded homes went from 40 to 10 after a levee was built. Did the levee help?", ["Fewer homes flooded."], "Yes.")]
    mist = ["Thinking people can stop storms.",
            "Choosing a solution made for a different hazard.",
            "Picking the cheapest solution without checking if it protects well."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Weather hazards", B1 + [(g_which, 6), (g_what, 6)]),
        ("Solutions for each hazard", [(g_which, 12), (g_what, 8)]),
        ("Does the solution work?", [(g_data, 14), (g_which, 6)]),
        ("Comparing solutions", [(g_compare, 14), (g_what, 6)]),
        ("Making claims", B5 + [g_compare, g_data, g_which, g_what]),
    ])
    make("grade-3", "weather-hazards", 15, "3-ESS3-1",
         "Make a claim about the merit of a design solution that reduces the impacts of a weather-related hazard.",
         "Weather Hazards",
         "Grade 3 Weather Hazards Worksheets: Floods, Hurricanes, Tornadoes and Design Solutions",
         "Weather Hazards",
         "Free Grade 3 science worksheets on weather hazards (NGSS 3-ESS3-1): floods, hurricanes, tornadoes, lightning, blizzards and droughts, solutions that reduce damage, and judging solutions with data. 100 practice questions with answers.",
         "We cannot stop storms, but we can reduce the damage.",
         "Levees, storm shelters, lightning rods and other designs protect people. Use evidence to judge which solution works best.",
         body(),
         [("What are weather hazards?", "Dangerous weather such as floods, hurricanes, tornadoes, lightning, blizzards and droughts."),
          ("How do people reduce damage from weather hazards?", "They build levees, storm shelters and lightning rods, use storm shutters, clear snow and save water."),
          ("How do you judge a design solution?", "Look at evidence, like how much damage happened before and after, and compare the cost and protection.")],
         sets)


if __name__ == "__main__":
    main()
