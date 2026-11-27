# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U04: igneous, sedimentary and metamorphic rocks, how they form and change in
the rock cycle, and Australian examples (Uluru, Kata Tjuta, the Organ Pipes, Wave Rock, Sydney sandstone).
  python tools/gen_au_science_y8_rock_cycle.py
Reuses the UK Year 8 rock makers, the US Grade 7 rock cycle makers and the UK Year 3 rock makers with Australian names.
Wrong answers come from real mistakes: thinking large crystals mean fast cooling, thinking metamorphic rocks melt, and thinking the
rock cycle has a fixed order.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

R8 = "gen_uk_science_y8_rocks_and_the_rock_cycle"
RC = "gen_us_science_g7_the_rock_cycle"
R3 = "gen_uk_science_y3_comparing_and_grouping_rocks"
r_crys = src(R8, "g_crystal")
r_from = src(R8, "g_from")
r_rock = src(R8, "g_rock")
r_sed = src(R8, "g_sed")
r_wea = src(R8, "g_wea")
r_por = src(R8, "g_por")
r_b1 = src.B(R8, "B1")
r_b5 = src.B(R8, "B5")
c_type = limit(src(RC, "g_type"), 8)
c_path = src(RC, "g_path")
c_en = src(RC, "g_energy")
c_diag = src(RC, "g_diag")
c_b1 = src.B(RC, "B1")
c_b5 = src.B(RC, "B5")
y3_type = limit(src(R3, "g_type"), 5)

AUR = [("Uluru", "arkose, a sandstone (sedimentary)", "sand and gravel eroded from ancient mountains, then pressed and cemented"),
       ("Kata Tjuta", "conglomerate (sedimentary)", "rounded pebbles and boulders cemented together"),
       ("the Organ Pipes in Victoria", "basalt (igneous)", "lava that cooled slowly and cracked into columns"),
       ("Wave Rock in Western Australia", "granite (igneous)", "magma that cooled slowly deep underground"),
       ("Sydney's harbour cliffs", "Hawkesbury sandstone (sedimentary)", "layers of river sand pressed together"),
       ("the slate roofs of old Adelaide houses", "slate (metamorphic)", "mudstone changed by heat and pressure")]


def g_aur():
    n, rock, how = R.choice(AUR)
    if R.random() < 0.5:
        w = sorted({x[1] for x in AUR if x[1] != rock})
        return tq("What kind of rock is %s made of?" % n, rock, R.sample(w, 3), "It formed from %s." % how)
    w = sorted({x[2] for x in AUR if x[2] != how})
    return tq("How did the rock of %s form?" % n, "from " + how, ["from " + x for x in R.sample(w, 3)], "%s is %s." % (n[0].upper() + n[1:], rock))


POOL1 = pool(R, [
    ("How do igneous rocks form?", "when magma or lava cools and becomes solid", ["when layers of sediment are pressed together", "when rocks are heated and squeezed without melting", "when plants rot"], "Granite and basalt are igneous."),
    ("How do sedimentary rocks form?", "layers of sediment are deposited, compacted and cemented", ["magma cools", "rock melts", "lightning strikes sand"], "Sandstone and limestone are sedimentary."),
    ("How do metamorphic rocks form?", "existing rocks are changed by heat and pressure without melting", ["lava cools quickly", "sand is cemented", "ice freezes"], "Marble and slate are metamorphic."),
    ("Why does granite have large crystals but basalt has small ones?", "Granite cooled slowly underground; basalt cooled quickly at the surface.", ["Granite cooled quickly.", "Basalt is older.", "Crystals grow faster at the surface."], "Slow cooling gives time for large crystals to grow."),
    ("In which kind of rock are fossils usually found?", "sedimentary rock", ["igneous rock", "metamorphic rock", "all equally"], "Sediments bury dead organisms gently."),
    ("Which rock forms when limestone is heated and squeezed?", "marble", ["granite", "sandstone", "basalt"], "Limestone is metamorphosed into marble."),
    ("Does the rock cycle always happen in the same order?", "No. Any rock can change into any other type by different paths.", ["Yes, always igneous → sedimentary → metamorphic.", "Yes, only in one direction.", "It happens only once."], "It is a cycle with many paths."),
    ("What drives melting and metamorphism in the rock cycle?", "heat from inside Earth", ["sunlight", "wind", "the Moon"], "The Sun drives weathering and erosion."),
    ("Australian opals form in which kind of rock?", "sedimentary rock", ["igneous rock only", "metamorphic rock only", "in volcanoes"], "Silica-rich water filled cracks in sedimentary rock."),
    ("Which process turns loose sand into sandstone?", "compaction and cementation", ["melting", "evaporation", "metamorphism"], "Minerals in water glue the grains together."),
])
POOL5 = pool(R, [
    ("Mia cools melted salol (a crystal-forming substance) on a warm slide and on a cold slide. Which gives bigger crystals?", "the warm slide (slower cooling)", ["the cold slide", "both the same", "neither forms crystals"], "This models granite and basalt."),
    ("Jack soaks four rocks of the same size in water and weighs them before and after. Which result shows the most porous rock?", "the rock with the biggest increase in mass", ["the rock with no change", "the heaviest rock before", "the smallest rock"], "Porous rocks soak up water."),
    ("Ruby drops dilute acid on a rock and it fizzes. What does this suggest?", "The rock contains calcium carbonate, such as limestone or marble.", ["It is granite.", "It is basalt.", "It is made of plastic."], "Carbonates react with acid to make carbon dioxide."),
    ("Kai models sedimentary rock by layering sand, mud and gravel in water. What should he see after it settles?", "layers, with larger particles at the bottom", ["one mixed layer", "larger particles on top", "no layers"], "Heavier particles settle first."),
    ("Why is granite used for kitchen benches?", "It is hard, strong and resists scratching.", ["It is soft and absorbent.", "It is light and floats.", "It dissolves in water."], "Igneous rocks with interlocking crystals are hard."),
    ("A geologist finds a rock with bands of crystals and no fossils. Which type is it most likely to be?", "metamorphic", ["sedimentary", "igneous with large holes", "a fossil"], "Banding forms under pressure."),
])


def main():
    sets = U.sets([
        ("Three kinds of rock", [(POOL1, 5), (r_rock, 6), (y3_type, 5), (r_b1, 4)]),
        ("How rocks form", [(r_from, 5), (r_crys, 4), (r_sed, 4), (c_type, 4), (POOL1, 3)]),
        ("The rock cycle", [(c_path, 6), (c_en, 5), (c_diag, 3), (c_b1, 4), (POOL1, 2)]),
        ("Australian rocks", [(g_aur, 10), (r_wea, 5), (c_type, 3), (r_por, 2)]),
        ("Investigations", [(POOL5, 6), (r_b5, 4), (c_b5, 4), (g_aur, 2), (r_por, 2), (c_type, 1), (r_wea, 1)]),
    ])
    make_au(YEAR, "rock-cycle", SORT, "AC9S8U04", "Earth and space sciences",
            "Investigate the formation of igneous, sedimentary and metamorphic rocks and describe how they change in the rock cycle over "
            "different timescales (summary of the Australian Curriculum v9.0 Science content description).",
            "The Rock Cycle", "The rock cycle",
            "Free Year 8 science worksheets on the rock cycle: igneous, sedimentary and metamorphic rocks, crystal size, fossils, and "
            "Australian rocks such as Uluru, Kata Tjuta and the Organ Pipes. 100 questions with answers.",
            "Rocks change from one type to another.", "Cooling makes igneous rock, layering makes sedimentary rock, heat and pressure make metamorphic rock.",
            "<p><b>Rocks form in three main ways and change from one type to another in the rock cycle.</b></p><ul>"
            "<li>Igneous: magma or lava cools. Slow cooling underground gives large crystals (granite); fast cooling gives small crystals (basalt).</li>"
            "<li>Sedimentary: sediments are deposited, compacted and cemented (sandstone, limestone); may contain fossils.</li>"
            "<li>Metamorphic: heat and pressure change rock without melting it (marble, slate). Any rock can be weathered, melted or changed again.</li></ul>",
            [("Large crystals. Cooled fast or slow?", ["crystals had time to grow"], "slowly"),
             ("Limestone heated and squeezed becomes…", ["metamorphism without melting"], "marble")],
            ["Thinking large crystals mean fast cooling.", "Thinking metamorphic rocks form by melting.",
             "Thinking the rock cycle always follows one fixed order."],
            [("What are the three types of rock?", "Igneous rocks form from cooled magma or lava, sedimentary rocks from layers of sediment, and metamorphic rocks from rocks changed by heat and pressure."),
             ("What is Uluru made of?", "Uluru is made of arkose, a coarse sandstone. Iron minerals in the rock have rusted, giving it its red colour."),
             ("Why are fossils found in sedimentary rocks?", "Sediments bury dead plants and animals gently, so their shapes are preserved. Melting and high pressure would destroy fossils in other rocks.")],
            sets)


if __name__ == "__main__":
    main()
