# -*- coding: utf-8 -*-
"""
US High School Biology: The Carbon Cycle (HS-LS2-5)
  python tools/gen_us_science_bio_carbon_cycle.py
Develop a model to illustrate the role of photosynthesis and cellular respiration in the cycling of carbon among the
biosphere, atmosphere, hydrosphere, and geosphere.
Processes (photosynthesis, respiration, decomposition, combustion, ocean exchange, fossil fuel formation), reservoirs,
atmospheric CO2 data (Mauna Loa), seasonal ups and downs, and human effects.
Wrong answers come from real mistakes: "respiration removes CO2 from the air", "carbon is used up", "the ocean holds no carbon".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, svg_wrap, arrow, People
from ws_common import text, INK

U = Unit(90110)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


PROC = [("photosynthesis", "from the atmosphere into living things"), ("cellular respiration", "from living things into the atmosphere"),
        ("decomposition", "from dead organisms into the atmosphere and soil"), ("burning fossil fuels", "from the geosphere into the atmosphere"),
        ("ocean absorbing CO<sub>2</sub>", "from the atmosphere into the hydrosphere"), ("formation of fossil fuels over millions of years", "from dead organisms into the geosphere"),
        ("volcanic eruptions", "from the geosphere into the atmosphere"), ("shell-building sea animals forming limestone", "from the hydrosphere into the geosphere"),
        ("forest fires", "from living things into the atmosphere"), ("animals eating plants", "from producers into consumers")]


def g_proc():
    p, a = R.choice(PROC)
    k = R.random() < 0.6
    if not once((p, k)):
        return None
    if k:
        return item("Where does %s move carbon?" % p, a, R.sample([x[1] for x in PROC if x[1] != a], 3), "%s moves carbon %s." % (p[0].upper() + p[1:], a))
    return item("Which process moves carbon %s?" % a, p, R.sample([x[0] for x in PROC if x[1] != a], 3), "%s." % (p[0].upper() + p[1:]))


AIR = [("photosynthesis", "removes"), ("cellular respiration", "adds"), ("burning gasoline", "adds"), ("cutting down and burning forests", "adds"),
       ("planting trees", "removes"), ("decomposition of leaves", "adds"), ("the ocean dissolving CO2", "removes"), ("burning coal for electricity", "adds"),
       ("a cow breathing out", "adds"), ("algae growing in a lake", "removes"), ("a campfire", "adds"), ("a growing cornfield on a sunny day", "removes"),
       ("a volcano erupting", "adds"), ("seaweed growing in the ocean", "removes"), ("a factory burning natural gas", "adds"), ("restoring a wetland with new plants", "removes"),
       ("bacteria breaking down food waste in a landfill", "adds"), ("a jet plane burning fuel", "adds"), ("young trees growing in a new forest", "removes"), ("people breathing out", "adds")]


def g_air():
    a, k = R.choice(AIR)
    if not once(a):
        return None
    return item("Does %s add CO<sub>2</sub> to the air or remove it?" % a, "It %s CO<sub>2</sub>." % k, ["It %s CO<sub>2</sub>." % ("adds" if k == "removes" else "removes"), "It has no effect on carbon.", "It turns CO<sub>2</sub> into energy."],
                "Photosynthesis removes CO2; respiration and burning add it.")


ML = {1960: 317, 1970: 326, 1980: 339, 1990: 354, 2000: 370, 2010: 390, 2020: 414}


def g_ml():
    who = P.next()[0]
    ys = sorted(R.sample(sorted(ML), 4))
    k = R.choice(["inc", "rate", "trend", "pred"])
    if not once((tuple(ys), k)) or not once(("mk", k), {"inc": 22, "rate": 22, "trend": 3, "pred": 3}[k]):
        return None
    tab = table(["Year", "CO<sub>2</sub> in the air (ppm)"], [[str(y), str(ML[y])] for y in ys])
    a, b = ys[0], ys[-1]
    if k == "inc":
        d = ML[b] - ML[a]
        return item(tab + "Mauna Loa data. By how much did CO<sub>2</sub> rise from %d to %d?" % (a, b), "%d ppm" % d, ["%d ppm" % ML[b], "%d ppm" % (ML[a] + ML[b]), "%d ppm" % (d + 10)],
                    "%d − %d = %d." % (ML[b], ML[a], d))
    if k == "rate":
        d = ML[b] - ML[a]
        yrs = b - a
        r = d / yrs
        return item(tab + "What was the average rise per year from %d to %d?" % (a, b), "%.1f ppm per year" % r, ["%.1f ppm per year" % (r * 2), "%d ppm per year" % d, "%.1f ppm per year" % (r / 2)],
                    "%d ÷ %d ≈ %.1f." % (d, yrs, r))
    if k == "trend":
        return item(tab + "What is the main cause of this rise in CO<sub>2</sub>?", "burning fossil fuels and cutting down forests",
                    ["more photosynthesis", "fewer volcanoes", "colder oceans"], "Humans add carbon from the geosphere.")
    return item(tab + "If the trend continues, what will CO<sub>2</sub> most likely be in 2030?", "higher than %d ppm" % ML[2020] if b == 2020 else "higher than %d ppm" % ML[b],
                ["lower than %d ppm" % ML[ys[0]], "exactly %d ppm" % ML[ys[0]], "zero"], "The line keeps going up.")


RES = [("coal deep underground", "geosphere"), ("limestone rock", "geosphere"), ("CO<sub>2</sub> gas in the air", "atmosphere"), ("methane in the air", "atmosphere"),
       ("sugar in a leaf", "biosphere"), ("proteins in a deer", "biosphere"), ("carbon dissolved in seawater", "hydrosphere"), ("shells made of calcium carbonate on the sea floor", "geosphere"),
       ("wood in a living tree", "biosphere"), ("oil in rock layers", "geosphere"), ("bicarbonate in a lake", "hydrosphere"), ("fat in a whale", "biosphere")]


def g_res():
    r, a = R.choice(RES)
    if not once(r):
        return None
    return item("Which carbon reservoir holds %s?" % r, "the %s" % a, ["the %s" % x for x in ["atmosphere", "biosphere", "hydrosphere", "geosphere"] if x != a], "%s is part of the %s." % (r[0].upper() + r[1:], a))


PATHS = [("A carbon atom in CO<sub>2</sub> enters a grass leaf. Which process?", "photosynthesis"), ("A rabbit eats the grass. Then the rabbit releases the carbon as CO<sub>2</sub>. Which process?", "cellular respiration"),
         ("A dead tree's carbon is released by fungi. Which process?", "decomposition"), ("Carbon in coal returns to the air at a power plant. Which process?", "combustion (burning)"),
         ("Carbon from the air dissolves into the ocean. Which process?", "diffusion into seawater"), ("Plankton remains are buried and pressed for millions of years. What forms?", "fossil fuels such as oil")]


def g_path():
    q, a = R.choice(PATHS)
    if not once(q):
        return None
    return item("Trace a carbon atom. %s" % q, a, R.sample([x[1] for x in PATHS if x[1] != a], 3), "Each step moves carbon to a new reservoir.")


B1 = bank([
    ("What are the four main carbon reservoirs?", "atmosphere, biosphere, hydrosphere and geosphere", ["sun, moon, stars and planets", "only the air", "only living things"], "Air, life, water, rock."),
    ("Which process takes CO<sub>2</sub> out of the air?", "photosynthesis", ["cellular respiration", "burning wood", "decomposition"], "Plants use CO2."),
    ("Which process puts CO<sub>2</sub> back into the air from living things?", "cellular respiration", ["photosynthesis", "fossil fuel formation", "limestone formation"], "All organisms respire."),
    ("Where is most of Earth's carbon stored?", "in rocks and sediments (the geosphere)", ["in the air", "in animals", "in clouds"], "Limestone and fossil fuels."),
    ("What are fossil fuels made of?", "remains of ancient organisms", ["melted rock", "ocean salt", "sunlight"], "Coal, oil and gas."),
    ("Is carbon used up in the carbon cycle?", "No. Atoms move between reservoirs but are not used up.", ["Yes, every year.", "Yes, by plants.", "Only in winter."], "Matter is conserved."),
    ("How do decomposers return carbon?", "They break down dead matter and release CO<sub>2</sub>.", ["They store it forever.", "They turn it into light.", "They remove it from the air."], "Respiration by fungi and bacteria."),
    ("Why does the ocean matter in the carbon cycle?", "It absorbs and releases large amounts of CO<sub>2</sub>.", ["It has no carbon.", "It only stores salt.", "It makes oxygen only."], "A huge carbon sink."),
])
B5 = bank([
    ("CO<sub>2</sub> at Mauna Loa goes up and down every year. Why does it drop each summer in the Northern Hemisphere?", "Plants are growing and photosynthesizing more.", ["People burn less fuel.", "The ocean boils.", "Volcanoes stop."], "Seasonal cycle."),
    ("Extra CO<sub>2</sub> dissolves in the ocean. What happens to seawater?", "It becomes more acidic.", ["It becomes saltier.", "It freezes.", "Nothing at all."], "Ocean acidification."),
    ("A student models a sealed jar with a plant and a snail. Why can both stay alive in light?", "The plant uses CO2 from the snail; the snail uses O2 from the plant.", ["The snail photosynthesizes.", "The jar makes air.", "Neither needs gases."], "Photosynthesis and respiration balance."),
    ("Why does cutting down a rainforest add carbon to the air?", "Burning or rotting trees release CO<sub>2</sub>, and fewer trees remove it.", ["Trees store no carbon.", "Rainforests make CO2 only.", "It removes carbon."], "Two effects."),
    ("Which human action helps move carbon from the air into the biosphere?", "planting forests", ["driving more cars", "burning coal", "draining wetlands"], "Trees store carbon."),
])


def cycle_svg():
    box = lambda x, y, t: "<rect x='%d' y='%d' width='130' height='34' rx='8' fill='#eef6e8' stroke='%s' stroke-width='1.4'/>" % (x - 65, y - 17, INK) + text(x, y + 5, t, 12)
    s = box(230, 24, "CO2 in the air") + box(80, 140, "plants") + box(230, 210, "animals") + box(380, 140, "fossil fuels, rock")
    s += arrow(180, 40, 100, 120, "#3c8d40", 2.5, 8) + text(110, 76, "photosynthesis", 11)
    s += arrow(120, 160, 190, 196, INK, 2, 7) + text(130, 196, "eating", 11)
    s += arrow(250, 192, 250, 42, "#d9822b", 2.5, 8) + text(300, 120, "respiration", 11)
    s += arrow(370, 122, 290, 40, "#c0392b", 2.5, 8) + text(380, 76, "burning", 11)
    return svg_wrap(460, 232, s, "carbon cycle model: photosynthesis moves CO2 from air to plants, animals eat plants, respiration and burning return CO2 to the air")


def body():
    think = ("<div class='qfig'>%s</div><p><b>Carbon atoms move; they are never used up.</b></p>"
             "<ul><li>Photosynthesis takes CO<sub>2</sub> out of the air; respiration and decomposition put it back.</li>"
             "<li>Burning fossil fuels moves ancient carbon from rock into the air faster than it returns.</li></ul>") % cycle_svg()
    ex = [("Which process removes CO2 from the air?", ["Plants use CO2"], "photosynthesis"),
          ("CO2: 339 ppm in 1980, 414 ppm in 2020. Rise?", ["414 − 339"], "75 ppm")]
    mist = ["Thinking respiration removes CO2. It adds it.", "Thinking carbon is used up. It moves between reservoirs.", "Forgetting the ocean and rocks store carbon."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Carbon reservoirs", B1 + [(g_proc, 6), (g_res, 6)]),
        ("Carbon processes", [(g_proc, 14), (g_air, 6)]),
        ("Adding and removing CO2", [(g_air, 10), (g_res, 4), (g_path, 4), (g_proc, 2)]),
        ("Mauna Loa data", [(g_ml, 18), (g_path, 2)]),
        ("Human effects", B5 + [(g_ml, 13), (g_air, 2)]),
    ])
    make("biology", "carbon-cycle", 10, "HS-LS2-5",
         "Develop a model to illustrate the role of photosynthesis and cellular respiration in the cycling of carbon among the biosphere, atmosphere, hydrosphere, and geosphere.",
         "The Carbon Cycle",
         "Carbon Cycle Worksheets: Photosynthesis, Respiration and CO2 Data (High School Biology)",
         "Carbon Cycle",
         "Free high school biology worksheets on the carbon cycle (NGSS HS-LS2-5): reservoirs, photosynthesis, respiration, decomposition, fossil fuels and Mauna Loa CO2 data. 100 questions with answers.",
         "Carbon moves; it is never used up.",
         "Photosynthesis takes CO2 out of the air; respiration and burning put it back.",
         body(),
         [("What are the main carbon reservoirs?", "The atmosphere, the biosphere (living things), the hydrosphere (oceans and lakes) and the geosphere (rocks and fossil fuels)."),
          ("How do photosynthesis and respiration cycle carbon?", "Photosynthesis moves carbon from CO2 in the air into sugars. Respiration breaks the sugars down and returns CO2 to the air."),
          ("Why is CO2 in the air rising?", "Burning fossil fuels and clearing forests add carbon to the atmosphere faster than plants and oceans remove it.")],
         sets)


if __name__ == "__main__":
    main()
