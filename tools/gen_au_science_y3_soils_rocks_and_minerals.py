# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, AC9S3U02: soils, rocks and minerals - their observable properties and their uses,
including Australian minerals (iron ore, gold, bauxite, opal) and rocks (Sydney sandstone, granite, basalt).
  python tools/gen_au_science_y3_soils_rocks_and_minerals.py
Reuses the UK Year 3 rock and soil makers with Australian names (tarmac -> bitumen), plus own questions on Australian minerals.
Wrong answers come from real mistakes: thinking soil is only "dirt" with nothing living in it, mixing up rocks and minerals, and
thinking all rocks are hard and heavy.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

RK = "gen_uk_science_y3_comparing_and_grouping_rocks"
SO = "gen_uk_science_y3_soils"
rk_look = src(RK, "g_look")
rk_man = limit(src(RK, "g_man"), 4)
rk_test = limit(src(RK, "g_test"), 4)
rk_type = limit(src(RK, "g_type"), 4)
rk_use = src(RK, "g_use", drop=["church", "cathedral"])
rk_b1 = src.B(RK, "B1")
rk_b5 = src.B(RK, "B5")
so_jar = src(SO, "g_jar", rep=[(r"found at just above", "found just above"), (r"found at near", "found near"), (r"found at floating on", "found floating on"), (r"What will be found at floating", "What will be found floating")])
so_lay = src(SO, "g_lay")
so_made = limit(src(SO, "g_made"), 5)
so_type = src(SO, "g_type")
so_worm = src(SO, "g_worm")
so_b1 = src.B(SO, "B1")
so_b5 = src.B(SO, "B5")

MIN = [("iron ore", "making steel for cars, bridges and buildings"), ("bauxite", "making aluminium for cans and planes"),
       ("gold", "jewellery and electronics"), ("opal", "gemstones for jewellery; it is Australia's national gemstone"),
       ("salt (halite)", "flavouring and keeping food"), ("quartz", "making glass and watch parts"), ("copper", "electrical wires"),
       ("coal", "burning in power stations to make electricity"), ("lithium", "batteries for phones and electric cars")]


def g_min():
    m, use = R.choice(MIN)
    if R.random() < 0.5:
        w = sorted({x[1] for x in MIN if x[0] != m})
        return tq("What is %s mainly used for?" % m, use, R.sample(w, 3), "Australia mines %s." % m)
    w = sorted({x[0] for x in MIN if x[0] != m})
    return tq("Which mineral or rock from Australian mines is used for %s?" % use.split(";")[0], m, R.sample(w, 3), "%s: %s." % (m[0].upper() + m[1:], use))


POOL1 = pool(R, [
    ("What is the difference between a rock and a mineral?", "Rocks are made of one or more minerals.", ["Minerals are made of rocks.", "They are the same thing.", "Rocks are alive."], "Granite is a rock made of quartz, feldspar and mica."),
    ("What is soil made of?", "tiny bits of rock, humus, water, air and living things", ["only rock", "only water", "only dead leaves"], "Soil is a mixture."),
    ("Why do earthworms help soil?", "They mix it and make tunnels that let in air and water.", ["They make the soil harder.", "They turn soil into rock.", "They eat all the humus."], "Healthy soil has many living things."),
    ("Which soil holds the most water?", "clay soil", ["sandy soil", "gravel", "pebbles"], "Clay has tiny grains packed close together."),
    ("Which soil lets water drain through fastest?", "sandy soil", ["clay soil", "wet mud", "potter's clay"], "Sand has big grains with spaces between them."),
    ("What are many old buildings in Sydney made from?", "sandstone", ["marble", "ice", "coal"], "Sydney sits on a large area of sandstone."),
    ("What is Uluru mainly made of?", "sandstone", ["granite", "ice", "coal"], "Its red colour comes from iron in the rock."),
    ("Why does Uluru look red?", "Iron minerals in the rock have rusted.", ["It is painted.", "It is hot inside.", "It reflects the sunset all day."], "Rusty iron is red."),
    ("Which rock is made when lava from a volcano cools?", "basalt", ["sandstone", "chalk", "limestone"], "Basalt is an igneous rock."),
    ("How can you test how hard a rock is?", "Try to scratch it with a fingernail, a coin and a steel nail.", ["Smell it.", "Paint it.", "Weigh it only."], "Harder rocks are harder to scratch."),
])
POOL5 = pool(R, [
    ("Mia pours 100 mL of water into sand, potting mix and clay. She collects 80 mL, 50 mL and 20 mL. Which soil held the most water?", "clay", ["sand", "potting mix", "they all held the same"], "100 − 20 = 80 mL stayed in the clay."),
    ("In Mia's test, what should she keep the same?", "the amount of soil and water and the size of the funnels", ["the type of soil", "nothing", "the result"], "Only the soil should change."),
    ("Jack drops a little vinegar on four rocks. Only one fizzes. Which rock is it most likely to be?", "limestone", ["granite", "basalt", "sandstone"], "Limestone contains calcium carbonate, which reacts with vinegar."),
    ("Ruby uses a hand lens to look at granite. What will she see?", "different coloured crystals", ["tiny shells", "layers of sand", "holes full of air"], "Granite is made of mineral crystals."),
    ("Kai wants to find out which soil grows the tallest bean plants. What should he change?", "the type of soil", ["the type of seed", "the amount of water", "the amount of light"], "Change one thing."),
    ("Ella finds a rock with small rounded grains and layers. What kind of rock is it most likely to be?", "sedimentary (such as sandstone)", ["igneous (such as granite)", "a mineral crystal", "metal"], "Layers form as sand settles."),
])


def main():
    sets = U.sets([
        ("Rocks", [(rk_look, 6), (rk_type, 4), (POOL1, 5), (rk_b1, 5)]),
        ("Minerals and their uses", [(g_min, 10), (rk_use, 5), (rk_man, 3), (POOL1, 2)]),
        ("Soils", [(so_type, 5), (so_lay, 4), (so_made, 4), (so_worm, 4), (POOL1, 3)]),
        ("Looking after soil", [(so_b1, 6), (so_jar, 5), (so_b5, 4), (g_min, 3), (rk_man, 1), (POOL1, 0), (so_worm, 1)]),
        ("Investigations", [(POOL5, 6), (rk_test, 4), (rk_b5, 4), (so_jar, 2), (so_type, 2), (g_min, 2)]),
    ])
    make_au(YEAR, "soils-rocks-and-minerals", SORT, "AC9S3U02", "Earth and space sciences",
            "Compare the observable properties of soils, rocks and minerals and justify their use for particular purposes "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Soils, Rocks and Minerals", "Soils, rocks and minerals",
            "Free Year 3 science worksheets on soils, rocks and minerals: sandstone, granite and basalt, Australian minerals such as iron ore, "
            "gold and opal, and sandy and clay soils. 100 questions with answers.",
            "Rocks are made of minerals.", "We choose rocks, minerals and soils for their properties.",
            "<p><b>Rocks are made of minerals, and soil is made from broken-down rock mixed with humus, water, air and living things.</b></p><ul>"
            "<li>Rocks differ in colour, grain size, hardness and how much water they let through.</li>"
            "<li>Australia mines many minerals: iron ore for steel, bauxite for aluminium, gold, copper, lithium and opal.</li>"
            "<li>Sandy soil drains fast; clay soil holds water. Loam, a mix, is best for most plants.</li></ul>",
            [("Which soil drains water fastest?", ["sand has big grains", "there are big gaps between them"], "sandy soil"),
             ("Iron ore is used to make…", ["iron ore is heated in a furnace"], "steel")],
            ["Mixing up rocks and minerals (rocks are made of minerals).", "Thinking soil has nothing living in it.",
             "Thinking all rocks are hard and heavy (pumice floats)."],
            [("What is the difference between a rock and a mineral?", "A mineral is a natural solid with the same make-up all through it, such as quartz. A rock is made of one or more minerals."),
             ("What is soil made of?", "Soil is made of tiny pieces of rock, humus (rotted plants and animals), water, air and living things such as worms and bacteria."),
             ("Why is Uluru red?", "Uluru is sandstone that contains iron minerals. The iron has rusted, which makes the rock look red.")],
            sets)


if __name__ == "__main__":
    main()
