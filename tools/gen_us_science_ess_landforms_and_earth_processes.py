# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Landforms and Earth Processes (HS-ESS2-1)
  python tools/gen_us_science_ess_landforms_and_earth_processes.py
Develop a model to illustrate how Earth's internal and surface processes operate at different spatial and temporal
scales to form continental and ocean-floor features.
Internal (constructive) processes: plate motion, volcanism, uplift; surface (destructive) processes: weathering,
erosion and deposition by water, ice, wind and waves; rates of uplift and erosion; time scales from seconds to
millions of years.
Wrong answers come from real mistakes: "mountains stay the same height forever", "erosion only builds landforms",
"all landforms form quickly", "the Grand Canyon was cut in a few years".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90407)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


FEAT = [("the Himalayas rising as India pushes into Asia", "internal"), ("the Hawaiian Islands built by lava over a hot spot", "internal"), ("the Mid-Atlantic Ridge", "internal"),
        ("the East African Rift Valley", "internal"), ("the Mariana Trench", "internal"), ("Mount St. Helens", "internal"),
        ("the Grand Canyon cut by the Colorado River", "surface"), ("the Mississippi River Delta", "surface"), ("U-shaped valleys in Yosemite", "surface"),
        ("sand dunes in the Sahara", "surface"), ("sea arches along a rocky coast", "surface"), ("a beach formed from sand carried by waves", "surface")]
TXT = {"internal": "internal processes (plate motion, magma, uplift)", "surface": "surface processes (weathering, erosion and deposition)"}


@safe
def g_feat():
    f, k = R.choice(FEAT)
    if not once(("ft", f)):
        return None
    return item("What mainly formed %s?" % f, TXT[k], [TXT["surface" if k == "internal" else "internal"], "only human activity", "meteorite impacts"],
                "Internal processes build up; surface processes wear down and move material.")


AGENT = [("a river", "a V-shaped valley and a delta"), ("a glacier", "a U-shaped valley and moraines"), ("wind", "sand dunes and wind-carved rocks"),
         ("ocean waves", "sea cliffs, sea arches and sea stacks"), ("groundwater", "caves and sinkholes in limestone"), ("gravity", "landslides and rockfalls")]


@safe
def g_agent():
    a, l = R.choice(AGENT)
    k = R.random() < 0.5
    if not once(("ag", a, k)):
        return None
    if k:
        return item("Which landforms are made by erosion and deposition from %s?" % a, l, R.sample([x[1] for x in AGENT if x[1] != l], 3), "Each agent leaves typical landforms.")
    return item("Which agent of erosion makes %s?" % l, a, R.sample([x[0] for x in AGENT if x[0] != a], 3), "Match the landform to the agent.")


@safe
def g_rate():
    who = P.next()[0]
    k = R.choice(["up", "ero", "net", "time"])
    u = R.choice([1, 2, 3, 4, 5, 10])
    e = R.choice([0.1, 0.2, 0.5, 1, 2])
    t = R.choice([100000, 500000, 1000000, 2000000, 5000000])
    if not once(("rt", k, u, e, t)):
        return None
    if k == "up":
        h = u * t / 1e6
        g = "%s km" % num(h, 2)
        return item("A mountain range rises %d mm per year. How much higher would it be after %s years (ignoring erosion)? (1 km = 1,000,000 mm)" % (u, num(t)), g,
                    uniq(g, ["%s km" % num(h * 1000, 2), "%s km" % num(h / 1000, 4), "%s m" % num(h, 2), "%s km" % num(h * 10, 2)]), "%d × %s = %s mm = %s km." % (u, num(t), num(u * t), num(h, 2)))
    if k == "ero":
        h = e * t / 1000
        g = "%s m" % num(h, 2)
        return item("A river cuts down into rock %s mm per year. How deep will its canyon be after %s years? (1 m = 1,000 mm)" % (num(e, 1), num(t)), g,
                    uniq(g, ["%s m" % num(h * 1000, 0), "%s m" % num(h / 1000, 4), "%s km" % num(h, 2), "%s m" % num(h * 10, 1)]), "%s × %s = %s mm = %s m." % (num(e, 1), num(t), num(e * t), num(h, 2)))
    if k == "net":
        if e >= u:
            return None
        n = (u - e) * t / 1000
        g = "%s m higher" % num(n, 1)
        return item("%s's model: a mountain is uplifted %d mm per year and eroded %s mm per year. How much does its height change in %s years?" % (who, u, num(e, 1), num(t)), g,
                    uniq(g, ["%s m higher" % num(u * t / 1000, 1), "%s m lower" % num(e * t / 1000, 1), "%s m higher" % num((u + e) * t / 1000, 1), "no change"]),
                    "Net = (%d − %s) mm/yr × %s = %s m higher." % (u, num(e, 1), num(t), num(n, 1)))
    d = R.choice([100, 200, 500, 1000, 1500])
    yrs = d * 1000 / e
    g = "%s years" % num(yrs)
    return item("A river erodes downward %s mm per year. About how long would it take to cut a canyon %s m deep?" % (num(e, 1), num(d)), g,
                uniq(g, ["%s years" % num(d * e), "%s years" % num(d / e), "%s years" % num(yrs * 10), "%s years" % num(yrs / 1000)]), "%s m = %s mm; ÷ %s = %s years." % (num(d), num(d * 1000), num(e, 1), num(yrs)))


SCALE = [("a landslide", 1), ("a volcanic eruption building a new cone", 2), ("a sand dune moving across a desert", 3), ("a river delta growing", 4), ("a glacier carving a valley", 5),
         ("a mountain range rising", 6), ("an ocean basin opening", 7)]


@safe
def g_scale():
    a, b = R.sample(SCALE, 2)
    k = R.choice(["fast", "slow"])
    if not once(("sc", tuple(sorted((a[0], b[0]))), k)):
        return None
    fast, slow = (a, b) if a[1] < b[1] else (b, a)
    first, second = sorted([a, b])
    if k == "fast":
        return item("Which usually happens faster: %s or %s?" % (first[0], second[0]), fast[0], [slow[0], "They take exactly the same time.", "Neither changes Earth's surface."],
                    "Earth processes range from seconds to hundreds of millions of years.")
    return item("Which usually takes longer: %s or %s?" % (first[0], second[0]), slow[0], [fast[0], "They take exactly the same time.", "Neither changes Earth's surface."],
                "Plate-scale changes are the slowest.")


B1 = bank([
    ("What are constructive processes?", "processes that build landforms, such as volcanoes and uplift", ["processes that only wear land down", "weather patterns", "human building"], "Internal energy."),
    ("What are destructive processes?", "processes that wear land down, such as weathering and erosion", ["processes that build mountains", "volcanic eruptions only", "plate collisions"], "Surface energy from the Sun and gravity."),
    ("What is the difference between weathering and erosion?", "Weathering breaks rock down; erosion moves the pieces away.", ["They are the same.", "Erosion breaks rock; weathering moves it.", "Weathering only happens underwater."], "Break vs move."),
    ("What powers Earth's internal processes?", "heat from Earth's interior (radioactive decay and leftover heat)", ["sunlight", "wind", "the Moon"], "Mantle convection."),
    ("What powers most surface processes like erosion?", "the Sun (driving weather and the water cycle) and gravity", ["Earth's core only", "earthquakes only", "magnetism"], "External energy."),
    ("Why don't mountains keep getting taller forever?", "Erosion wears them down while uplift builds them up.", ["Gravity stops plates.", "Mountains melt.", "Snow pushes them down permanently."], "Balance of processes."),
    ("What is deposition?", "dropping sediment in a new place", ["breaking rocks apart", "melting rock", "lifting rocks up"], "Deltas, beaches, dunes."),
    ("Which feature forms on the ocean floor where plates pull apart?", "a mid-ocean ridge", ["a sand dune", "a delta", "a U-shaped valley"], "Ocean-floor feature."),
])
B5 = bank([
    ("The Appalachian Mountains are lower and rounder than the Rockies. What is the best explanation?", "The Appalachians are much older and have been eroded longer.", ["The Appalachians are younger.", "The Rockies have no erosion.", "The Appalachians are made of ice."], "Age and erosion."),
    ("A model of a coastline shows sea stacks forming. Which processes must the model include?", "wave erosion of weak rock over thousands of years", ["volcanic eruptions only", "glacier deposition only", "wind building dunes"], "Surface processes."),
    ("Why is Hawaii's Big Island the only one with active volcanoes?", "The Pacific Plate moved the older islands away from the hot spot.", ["The other islands are made of sand.", "The hot spot moves west fast.", "Erosion makes volcanoes."], "Plate motion over a hot spot."),
    ("Seafloor near a trench has thick sediment, but near the ridge it is thin. Why?", "Sediment has had more time to pile up on older seafloor.", ["Ridges blow sediment away.", "Trenches make sediment.", "Sediment sinks at ridges."], "Time scales."),
    ("A student models the Grand Canyon forming in 100 years. What should be revised?", "It took millions of years of slow river erosion and uplift.", ["Nothing; 100 years is right.", "It formed in one flood day.", "It was dug by people."], "Correct time scale."),
])


def body():
    think = ("<p><b>Internal processes build land up; surface processes wear it down.</b></p>"
             "<ul><li>Internal (heat from inside): plate motion, volcanoes, uplift, ridges, trenches, rifts.</li>"
             "<li>Surface (Sun and gravity): weathering, erosion and deposition by water, ice, wind and waves.</li>"
             "<li>Processes act over seconds (landslides) to hundreds of millions of years (ocean basins). Net change = uplift − erosion.</li></ul>")
    ex = [("Uplift 5 mm/yr for 1,000,000 years?", ["5,000,000 mm"], "5 km"),
          ("Uplift 3 mm/yr, erosion 1 mm/yr, 100,000 yr?", ["2 mm/yr × 100,000"], "200 m higher")]
    mist = ["Thinking mountains stay the same height forever.", "Thinking erosion builds landforms only.", "Thinking big landforms form in a few years."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Building up and wearing down", B1 + [(g_feat, 10), (g_agent, 2)]),
        ("Agents of erosion", [(g_agent, 10), (g_scale, 10)]),
        ("Rates of change", [(g_rate, 18), (g_scale, 2)]),
        ("Time and space scales", [(g_scale, 12), (g_rate, 8)]),
        ("Modeling landforms", B5 + [(g_rate, 12), (g_scale, 3)]),
    ])
    make("earth-and-space-science", "landforms-and-earth-processes", 7, "HS-ESS2-1",
         "Develop a model to illustrate how Earth's internal and surface processes operate at different spatial and temporal scales to form continental and ocean-floor features.",
         "Landforms and Earth Processes",
         "Landform Worksheets: Uplift, Erosion, Deposition and Time Scales (High School Earth Science)",
         "Landforms",
         "Free high school Earth and space science worksheets on landforms (NGSS HS-ESS2-1): internal and surface processes, agents of erosion, uplift and erosion rates and time scales. 100 questions with answers.",
         "Uplift builds; erosion wears down.",
         "Internal heat raises land; the Sun and gravity drive erosion and deposition.",
         body(),
         [("What is the difference between internal and surface processes?", "Internal processes, driven by Earth's heat, build land through plate motion, volcanoes and uplift. Surface processes, driven by the Sun and gravity, wear land down by weathering, erosion and deposition."),
          ("How fast do landforms change?", "Some changes take seconds (landslides) and others take millions of years (mountain ranges and ocean basins)."),
          ("Why do old mountains look rounded?", "Erosion has worn them down for a long time, and uplift has slowed or stopped.")],
         sets)


if __name__ == "__main__":
    main()
