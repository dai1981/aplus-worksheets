# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Natural Hazards (4-ESS3-2)
  python tools/gen_us_science_g4_natural_hazards.py
Humans cannot stop natural Earth processes (earthquakes, floods, tsunamis, volcanic eruptions,
landslides) but can reduce their impacts: earthquake-resistant buildings, levees and floodwalls,
warning systems, evacuation routes, homes on stilts, planting on slopes. Students compare solutions
using criteria and constraints.
Wrong answers come from real mistakes: "people can stop earthquakes", "a levee stops all rain",
"the cheapest solution is always best".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(40116)
R = U.R
P = People(R)

SOL = {"earthquake": ["building with flexible frames and steel supports", "bolting houses to their foundations", "strapping heavy furniture and water heaters to walls",
                      "practicing “drop, cover and hold on” drills", "rubber pads under buildings that absorb shaking", "flexible gas pipes that bend instead of breaking", "building codes that require earthquake-safe walls"],
       "flood": ["building levees and floodwalls along a river", "raising houses on stilts", "making wetlands that soak up extra water",
                 "not building homes on low land next to rivers", "building storm drains to carry water away", "piling sandbags along a riverbank", "flood gates that close when the river rises", "pumps that move water out of low streets"],
       "tsunami": ["tsunami warning buoys in the ocean", "marked evacuation routes to high ground", "sea walls along the coast",
                   "warning sirens on the beach", "tall, strong buildings people can climb into", "planting mangrove forests along the shore to slow giant waves", "tower shelters on the beach that rise above giant waves"],
       "volcanic eruption": ["measuring small earthquakes and gases near the volcano to warn people", "evacuation plans for nearby towns", "not building homes in the path of old lava flows",
                             "dust masks to protect from falling ash", "channels that guide mudflows away from towns", "walls of earth that turn lava flows away from roads", "sweeping heavy ash off roofs so they do not collapse"],
       "landslide": ["planting trees and grass on steep slopes", "building retaining walls", "pipes that drain water out of hillsides",
                     "not building houses at the bottom of steep, loose slopes", "nets that catch falling rocks", "sensors that detect moving ground on hillsides"]}
PL = {"earthquake": "earthquakes", "flood": "floods", "tsunami": "tsunamis", "volcanic eruption": "volcanic eruptions", "landslide": "landslides"}


def cap(s):
    return s[0].upper() + s[1:]


GENERIC = ("evacuation", "siren", "stilts", "high ground", "sea walls", "tall, strong buildings", "wetlands", "drain", "levees")


def specific(x):
    return not any(g in x for g in GENERIC)


def g_which():
    h = R.choice(sorted(SOL))
    a = R.choice(SOL[h])
    w = [x for k in SOL if k != h for x in SOL[k] if specific(x)]
    return item("Which solution would best reduce damage from %s?" % PL[h], a, R.sample(w, 3), "%s helps protect people from %s." % (cap(a), PL[h]))


def g_what():
    h = R.choice(sorted(SOL))
    a = R.choice([x for x in SOL[h] if specific(x)] + (["building levees and floodwalls along a river"] if h == "flood" else []))
    return item("A town uses this plan: %s. Which hazard is it mainly designed for?" % a, PL[h], [PL[x] for x in R.sample([k for k in SOL if k != h], 3)],
                "This solution reduces the impact of %s." % PL[h])


def g_compare():
    h = R.choice(sorted(SOL))
    opts = R.sample(SOL[h], 3)
    cost = R.sample([2, 5, 8, 12, 20, 30, 50], 3)
    prot = R.sample(["low", "medium", "high"], 3)
    rows = [[cap(o), "$%d million" % c, pr] for o, c, pr in zip(opts, cost, prot)]
    tab = table(["Solution", "Cost", "Protection"], rows)
    town = R.choice(["Riverton", "Hill City", "Bay Town", "Pine Falls", "Clearwater", "Rock Point"])
    k = R.choice(["best", "cheap", "budget"])
    hi = opts[prot.index("high")]
    if k == "best":
        return item(tab + "%s is choosing a way to reduce damage from %s. Which solution gives the most protection?" % (town, PL[h]), cap(hi),
                    [cap(o) for o in opts if o != hi] + ["They all give the same protection."], "It has high protection.")
    if k == "cheap":
        lo = opts[cost.index(min(cost))]
        return item(tab + "%s wants to spend as little money as possible. Which solution costs the least?" % town, cap(lo),
                    [cap(o) for o in opts if o != lo] + ["They all cost the same."], "It costs $%d million." % min(cost))
    budget = R.choice([c for c in range(5, 60, 5)])
    ok = [o for o, c, pr in zip(opts, cost, prot) if c <= budget]
    if not ok:
        return None
    best = max(ok, key=lambda o: ["low", "medium", "high"].index(prot[opts.index(o)]))
    return item(tab + "%s can spend at most $%d million. Which solution gives the most protection within this limit?" % (town, budget), cap(best),
                [cap(o) for o in opts if o != best] + ["none of them"], "Only solutions costing $%d million or less meet the constraint. Of those, this one protects best." % budget)


B1 = bank([
    ("What is a natural hazard?", "a natural Earth process that can harm people, like an earthquake or flood", ["a broken toy", "a planned fire drill", "a sunny day"],
     "Earthquakes, floods, tsunamis, volcanoes and landslides are natural hazards."),
    ("Can people stop earthquakes from happening?", "No, but they can reduce the damage.", ["Yes, with big walls.", "Yes, by building more roads.", "Yes, with warning sirens."],
     "We cannot stop Earth's processes, but we can prepare."),
    ("What does a levee do?", "holds back river water to protect land from floods", ["stops earthquakes", "warns of tsunamis", "cools lava"], "A levee is a wall of soil or concrete along a river."),
    ("What causes most tsunamis?", "earthquakes under the ocean", ["strong winds on land", "heavy rain in cities", "melting snow on mountains"],
     "A sudden movement of the sea floor pushes up a huge wave."),
    ("Why are warning systems important?", "They give people time to get to safety.", ["They stop the hazard.", "They make hazards smaller.", "They cause hazards."],
     "Early warnings save lives."),
    ("What should you do during an earthquake inside a building?", "drop, cover and hold on", ["run outside right away", "stand by a window", "ride an elevator"],
     "Get under a sturdy table and hold on."),
    ("What is a criterion for a flood solution?", "It must keep water out of homes.", ["It must be painted blue.", "It must take 100 years to build.", "It must stop the rain."],
     "Criteria tell what the solution must do."),
    ("What is a constraint for a flood solution?", "It must cost less than the town can spend.", ["It must keep water out of homes.", "It must work well.", "It must protect people."],
     "Constraints are limits like money, time and materials."),
])
B5 = bank([
    ("Ava's class builds model houses on a tray and shakes it. Which house design should hold up best?", "a house with a wide base and cross braces", ["a tall, thin house with no braces", "a house made of loose blocks", "a house balanced on one corner"],
     "Wide bases and braces resist shaking."),
    ("Leo tests two model levees with a cup of water. Levee A leaks; levee B holds. What should he do next?", "test levee B again to be sure the result repeats", ["stop testing", "use levee A", "change the cup color"],
     "Repeated tests show the design is reliable."),
    ("A town near the ocean has a tsunami warning siren but no marked path to high ground. What would improve the plan most?", "mark evacuation routes to high ground", ["remove the siren", "build more houses on the beach", "paint the siren red"],
     "People need to know where to go after the warning."),
    ("Why might a town choose wetlands instead of a concrete wall to reduce floods?", "Wetlands soak up water and give homes to wildlife.", ["Wetlands stop all rain.", "Concrete walls never work.", "Wetlands make floods bigger."],
     "Different solutions have different benefits."),
    ("Mia compares two earthquake solutions. One costs less but protects less. What should she consider?", "how much protection the town needs and how much it can spend", ["only which is cheapest", "only which is newest", "which has a longer name"],
     "Compare solutions using criteria and constraints."),
    ("Which solution helps both people near volcanoes and people near rivers?", "having an evacuation plan", ["bolting houses to foundations", "rock nets", "strapping water heaters"],
     "Evacuation plans help with many hazards."),
])


def body():
    think = ("<p><b>Natural hazards</b> are Earth processes that can harm people: earthquakes, floods, tsunamis, volcanic eruptions and landslides. "
             "People cannot stop these processes, but they can <b>reduce their impacts</b>.</p>"
             "<ul><li>Earthquakes: flexible buildings, bolting houses down, drills.</li>"
             "<li>Floods: levees, houses on stilts, wetlands, not building on low land.</li>"
             "<li>Tsunamis: warning buoys and sirens, evacuation routes to high ground.</li>"
             "<li>Volcanoes: monitoring and evacuation plans. Landslides: plants and retaining walls.</li></ul>"
             "<p>Engineers compare solutions using <b>criteria</b> (what it must do) and <b>constraints</b> (limits such as cost).</p>")
    ex = [("A town by a river floods every spring. Name two solutions.", ["Keep water out.", "Lift homes above the water."], "a levee and houses on stilts"),
          ("A seawall costs $50 million but the town can spend $20 million. Can they build it?", ["Cost is a constraint.", "50 > 20."], "No, it does not meet the constraint.")]
    mist = ["Thinking people can stop earthquakes or volcanoes.",
            "Choosing the cheapest solution without checking how well it works.",
            "Picking a solution made for a different hazard."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Natural hazards", B1 + [(g_which, 6), (g_what, 6)]),
        ("Solutions for each hazard", [(g_which, 10), (g_what, 10)]),
        ("Matching plans to hazards", [(g_what, 12), (g_which, 8)]),
        ("Comparing solutions", [(g_compare, 14), (g_which, 6)]),
        ("Testing designs", B5 + [g_compare, g_which, g_what]),
    ])
    make("grade-4", "natural-hazards", 16, "4-ESS3-2",
         "Generate and compare multiple solutions to reduce the impacts of natural Earth processes on humans.",
         "Natural Hazards",
         "Grade 4 Natural Hazards Worksheets: Earthquakes, Floods, Tsunamis and Solutions",
         "Natural Hazards",
         "Free Grade 4 science worksheets on natural hazards (NGSS 4-ESS3-2): earthquakes, floods, tsunamis, volcanoes and landslides, solutions that reduce damage, and comparing designs using criteria and constraints. 100 practice questions with answers.",
         "We cannot stop natural hazards, but we can reduce the damage.",
         "Levees, strong buildings, warning systems and evacuation routes protect people. Compare solutions with criteria and constraints.",
         body(),
         [("Can people stop natural hazards?", "No. People cannot stop earthquakes, floods or eruptions, but they can design solutions that reduce the damage."),
          ("How do people reduce flood damage?", "They build levees and floodwalls, raise houses on stilts, protect wetlands, and avoid building on low land near rivers."),
          ("How do you compare solutions?", "Check which ones meet the criteria (what the solution must do) and the constraints (limits like cost), then choose the best fit.")],
         sets)


if __name__ == "__main__":
    main()
