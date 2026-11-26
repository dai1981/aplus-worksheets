# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Chemistry: Earth and atmosphere): Rocks and the Rock Cycle
  python tools/gen_uk_science_y8_rocks_and_the_rock_cycle.py
The structure of the Earth (crust, mantle, outer and inner core), igneous, sedimentary and metamorphic rocks and
how they form, crystal size and cooling rate, weathering (freeze-thaw, chemical, biological), erosion, transport,
deposition, compaction and cementation, the rock cycle, and the Earth as a source of limited resources.
Reuses the rock-type, rock-cycle and landscape questions of the US Grade 7 units in British English.
Wrong answers come from real mistakes: "metamorphic rock forms by melting", "weathering and erosion are the same",
"granite has small crystals because it is hard", "the mantle is liquid".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61809)
R = U.R
P = People(R)
uk_sci.USED.clear()
RC = adopt_us("gen_us_science_g7_the_rock_cycle", U)
SH = adopt_us("gen_us_science_g7_shaping_earths_surface", U)
us_type, us_path, us_en, us_diag = ukm(RC.g_type), ukm(RC.g_path), ukm(RC.g_energy), ukm(RC.g_diag)
us_rate, us_speed, us_evid = ukm(SH.g_rate), ukm(SH.g_speed), ukm(SH.g_evid)

ROCK = [("granite", "igneous"), ("basalt", "igneous"), ("obsidian", "igneous"), ("pumice", "igneous"), ("sandstone", "sedimentary"), ("limestone", "sedimentary"),
        ("chalk", "sedimentary"), ("mudstone", "sedimentary"), ("conglomerate", "sedimentary"), ("marble", "metamorphic"), ("slate", "metamorphic"), ("schist", "metamorphic"), ("gneiss", "metamorphic")]
FROM = [("marble", "limestone"), ("slate", "mudstone or shale"), ("quartzite", "sandstone")]


def g_rock():
    r, t = R.choice(ROCK)
    if not once(("ro", r)):
        return None
    return item("What type of rock is %s?" % r, t, [x for x in ["igneous", "sedimentary", "metamorphic", "a mineral, not a rock"] if x != t],
                "Igneous: cooled magma or lava. Sedimentary: layers of sediment. Metamorphic: changed by heat and pressure.")


def g_from():
    m, p = R.choice(FROM)
    k = R.random() < 0.5
    if not once(("fr", m, k)):
        return None
    if k:
        return item("Which rock is %s made from when it is changed by heat and pressure?" % m, p, R.sample([x[1] for x in FROM if x[1] != p] + ["granite", "basalt"], 3), "Metamorphic rocks form from other rocks.")
    return item("%s is heated and squeezed deep underground without melting. Which rock forms?" % p.capitalize(), m, R.sample([x[0] for x in FROM if x[0] != m] + ["granite", "chalk"], 3), "Metamorphism.")


LAYER = [("the crust", "thin, solid outer layer of rock"), ("the mantle", "thick layer of hot rock that can flow very slowly"),
         ("the outer core", "liquid layer of iron and nickel"), ("the inner core", "solid centre of iron and nickel")]


def g_layer():
    l, d = R.choice(LAYER)
    k = R.random() < 0.5
    if not once(("la", l, k)):
        return None
    if k:
        return item("Which layer of the Earth is the %s?" % d, l, [x[0] for x in LAYER if x[0] != l], "Crust → mantle → outer core → inner core.")
    return item("What is %s like?" % l, "a " + d, ["a " + x[1] for x in LAYER if x[0] != l], "Crust → mantle → outer core → inner core.")


def g_crystal():
    who = P.next()[0]
    rows = [("basalt", "lava on the surface", "cooled quickly", "small"), ("granite", "magma deep underground", "cooled slowly", "large"),
            ("obsidian", "lava in water", "cooled very quickly", "none (glassy)"), ("gabbro", "magma underground", "cooled slowly", "large")]
    k = R.choice(["why", "fast", "slow", "pattern", "pred"])
    if not once(("cr", k)) and not once(("cr2", k)):
        return None
    tab = table(["Rock", "Formed from", "Cooling", "Crystal size"], [list(r) for r in rows])
    intro = tab + "%s compared some igneous rocks. " % who
    if k == "why":
        return item(intro + "Why does granite have large crystals?", "The magma cooled slowly, so the crystals had time to grow.", ["It cooled quickly.", "It was squeezed by layers.", "It is made of sediment."], "Slow cooling: large crystals.")
    if k == "fast":
        return item(intro + "Which rock cooled fastest?", "obsidian", ["granite", "gabbro", "basalt"], "No crystals at all.")
    if k == "slow":
        return item(intro + "Where do igneous rocks with large crystals form?", "deep underground", ["on the surface", "in rivers", "in the sea bed as sediment"], "Insulated, slow cooling.")
    if k == "pattern":
        return item(intro + "What pattern does the table show?", "The slower the cooling, the larger the crystals.", ["The faster the cooling, the larger the crystals.", "Cooling has no effect.", "All igneous rocks have the same crystals."], "Cooling rate.")
    return item(intro + "Molten wax is cooled in a fridge and in a warm oven. Which would give larger crystals?", "the one cooled slowly in the warm oven", ["the one in the fridge", "both the same", "neither has crystals"], "A model of cooling magma.")


WEA = [("Water gets into a crack, freezes and expands, and the crack gets wider.", "physical weathering (freeze-thaw)"),
       ("Rainwater, which is slightly acidic, slowly dissolves limestone.", "chemical weathering"),
       ("Plant roots grow into cracks and split the rock.", "biological weathering"),
       ("Burrowing animals break up rock near the surface.", "biological weathering"),
       ("A rock in a desert heats up by day and cools at night until its surface peels.", "physical weathering"),
       ("Acid rain damages a marble statue.", "chemical weathering")]


def g_wea():
    s, a = R.choice(WEA)
    if not once(("we", s)):
        return None
    return item("%s What kind of weathering is this?" % s, a, [x for x in ["physical weathering (freeze-thaw)", "physical weathering", "chemical weathering", "biological weathering", "erosion, not weathering"] if x != a and not (a.startswith("physical") and x.startswith("physical"))][:3],
                "Weathering breaks rock where it is; erosion carries it away.")


SED = ["weathering", "erosion and transport", "deposition", "compaction", "cementation"]


def g_sed():
    i = R.randrange(len(SED) - 1)
    if not once(("se", i)):
        return None
    return item("In the formation of sedimentary rock, which stage comes straight after %s?" % SED[i], SED[i + 1], [x for x in SED if x not in (SED[i], SED[i + 1])][:3],
                "Weathering → erosion and transport → deposition → compaction → cementation.")


def g_por():
    who = P.next()[0]
    rocks = [("sandstone", R.choice([6, 7, 8, 9])), ("granite", 0), ("chalk", R.choice([10, 11, 12, 13])), ("marble", R.choice([0, 1]))]
    k = R.choice(["most", "why", "none", "type"])
    if not once(("po", rocks[0][1], rocks[2][1], k)) or not once(("po", k), 4):
        return None
    tab = table(["Rock", "Mass of water soaked up (g)"], [[r, str(v)] for r, v in rocks])
    intro = tab + "%s soaked equal-sized rocks in water. " % who
    if k == "most":
        return item(intro + "Which rock is the most porous?", "chalk", ["sandstone", "granite", "marble"], "It soaked up the most water.")
    if k == "why":
        return item(intro + "Why do sedimentary rocks soak up water?", "They are made of grains with gaps between them.", ["They have interlocking crystals.", "They are hotter.", "They are magnetic."], "Porous.")
    if k == "none":
        return item(intro + "Why does granite soak up no water?", "Its crystals interlock with no gaps.", ["It is too heavy.", "It is a sedimentary rock.", "It dissolves."], "Igneous rocks are not porous.")
    return item(intro + "Why must the rocks be the same size?", "so it is a fair test", ["so they look nice", "to make them float", "it does not matter"], "Control variable.")


B1 = bank([
    ("What is the difference between weathering and erosion?", "Weathering breaks rock down where it is; erosion carries the pieces away.", ["They are the same.", "Erosion makes new rock.", "Weathering happens only in rivers."], "Then deposition."),
    ("How does sediment become sedimentary rock?", "Layers are squashed (compaction) and stuck together (cementation).", ["It melts and cools.", "It is heated until it glows.", "It freezes."], "Over millions of years."),
    ("Where are fossils most often found?", "in sedimentary rocks", ["in igneous rocks", "in magma", "in the core"], "Heat destroys them."),
    ("What is magma?", "molten rock underground", ["cooled lava", "a sedimentary rock", "a type of fossil"], "Lava when it erupts."),
    ("How do metamorphic rocks form?", "Existing rock is changed by heat and pressure without melting.", ["Lava cools quickly.", "Sediments are cemented.", "Rock dissolves in water."], "Marble, slate."),
])
B5 = bank([
    ("Why are the Earth's resources such as metal ores limited?", "They took millions of years to form and are being used much faster.", ["They are made again every year.", "They never run out.", "They come from the core."], "Finite resources."),
    ("Why is recycling aluminium better than mining new ore?", "It saves ore and uses much less energy.", ["It uses more energy.", "Recycled aluminium is radioactive.", "Ore is unlimited."], "Conserve resources."),
    ("What does the rock cycle show?", "how rocks change from one type to another over very long times", ["how rocks are made in one day", "that rocks never change", "only how volcanoes work"], "Driven by heat and weather."),
    ("Why are pebbles on a beach rounded?", "They have been rolled and knocked against each other by water.", ["They were made round.", "Heat melted them.", "Plants shaped them."], "Erosion."),
    ("Which rock fizzes when a drop of acid is put on it?", "limestone (calcium carbonate)", ["granite", "basalt", "slate"], "Carbonates release carbon dioxide."),
])


def body():
    think = ("<p><b>There are three types of rock, and the rock cycle links them.</b></p>"
             "<ul><li>Igneous: magma or lava cools. Slow cooling gives large crystals; fast cooling gives small ones.</li>"
             "<li>Sedimentary: weathering, erosion, deposition, compaction and cementation. Porous, often with fossils.</li>"
             "<li>Metamorphic: heat and pressure change rock without melting (limestone → marble).</li></ul>")
    ex = [("Basalt: large or small crystals?", ["Lava cooled quickly"], "small"),
          ("Water freezes in a crack. Type of weathering?", ["Ice expands"], "freeze-thaw")]
    mist = ["Thinking metamorphic rock forms by melting.", "Mixing up weathering and erosion.", "Thinking the mantle is a liquid."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The Earth and its rocks", B1 + [(g_layer, 7), (g_rock, 8)]),
        ("Igneous and metamorphic", [(g_crystal, 6), (g_from, 5), (g_rock, 4), (us_type, 5)]),
        ("Weathering and sediment", [(g_wea, 5), (g_sed, 3), (g_por, 7), (us_speed, 5)]),
        ("The rock cycle", [(us_path, 5), (us_en, 5), (us_diag, 2), (us_type, 4), (us_evid, 2), (g_por, 2)]),
        ("Rocks over time", B5 + [(us_rate, 10), (us_speed, 3), (us_evid, 2)]),
    ])
    make_ks3(8, "rocks-and-the-rock-cycle", 9, "Chemistry", "Earth and atmosphere",
             "The composition of the Earth; the structure of the Earth; the rock cycle and the formation of igneous, sedimentary and metamorphic rocks; Earth as a source of limited resources and the efficacy of recycling.",
             "Rocks and the Rock Cycle",
             "Year 8 Science: Rocks and the Rock Cycle Worksheets (Igneous, Sedimentary, Metamorphic)",
             "Rocks and the Rock Cycle",
             "Free Year 8 science worksheets on rocks: the structure of the Earth, igneous, sedimentary and metamorphic rocks, crystal size, weathering, erosion and the rock cycle. 100 questions with answers.",
             "Rocks change from one type to another.",
             "Igneous from magma, sedimentary from layers, metamorphic from heat and pressure.",
             body(),
             [("What are the three types of rock?", "Igneous (formed when magma or lava cools), sedimentary (formed from layers of sediment) and metamorphic (formed when rock is changed by heat and pressure)."),
              ("Why do some igneous rocks have large crystals?", "Magma that cools slowly deep underground gives crystals time to grow. Lava that cools quickly on the surface forms small crystals."),
              ("What is the difference between weathering and erosion?", "Weathering breaks rock into smaller pieces where it is. Erosion moves the pieces away, for example in rivers or by wind.")],
             sets)


if __name__ == "__main__":
    main()
