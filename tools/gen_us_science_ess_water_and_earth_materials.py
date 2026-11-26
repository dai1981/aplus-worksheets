# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Water and Earth Materials (HS-ESS2-5)
  python tools/gen_us_science_ess_water_and_earth_materials.py
Plan and conduct an investigation of the properties of water and its effects on Earth materials and surface processes.
Water's properties (expands when it freezes, dissolves minerals, high heat capacity, cohesion and capillary action),
frost wedging, chemical weathering and caves, porosity and permeability, and how stream speed sets the size of
sediment carried.
Wrong answers come from real mistakes: "water shrinks when it freezes", "pure rainwater cannot weather rock",
"clay lets water through fastest", "slow streams carry boulders".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90411)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


PROP = [("Water expands about 9% when it freezes.", "Ice in cracks pries rocks apart (frost wedging)."),
        ("Water with dissolved CO₂ is slightly acidic.", "It slowly dissolves limestone, forming caves and sinkholes."),
        ("Water has a very high heat capacity.", "Oceans and lakes keep nearby climates milder."),
        ("Water molecules stick to each other and to surfaces (cohesion and adhesion).", "Water rises through tiny spaces in soil by capillary action."),
        ("Water is a good solvent for many minerals.", "Rivers carry dissolved salts to the sea, making it salty."),
        ("Liquid water flows downhill and carries particles.", "Rivers carve valleys and build deltas."),
        ("Ice is less dense than liquid water.", "Lakes freeze from the top down, and the ice protects the water below.")]


@safe
def g_prop():
    p, e = R.choice(PROP)
    k = R.random() < 0.55
    if not once(("pr", p, k)):
        return None
    if k:
        return item("%s Which effect on Earth's surface does this cause?" % p, e, R.sample([x[1] for x in PROP if x[1] != e], 3), "Water's unusual properties shape Earth's surface.")
    return item("Which property of water explains this: %s" % e, p, R.sample([x[0] for x in PROP if x[0] != p], 3), "Match the effect to the property.")


@safe
def g_expand():
    v = R.choice([50, 80, 100, 120, 150, 200, 250, 300, 400, 500, 600, 750, 800, 1000])
    k = R.choice(["ice", "inc"])
    if not once(("ex", v, k)):
        return None
    if k == "ice":
        g = "%s mL" % num(v * 1.09, 1)
        return item("Water expands by about 9%% when it freezes. %s mL of water freezes in a rock crack. About what volume does the ice take up?" % num(v), g,
                    uniq(g, ["%s mL" % num(v * 0.91, 1), "%s mL" % num(v, 1), "%s mL" % num(v + 9, 1), "%s mL" % num(v * 1.9, 1)]), "%s × 1.09 = %s mL." % (num(v), num(v * 1.09, 1)))
    g = "%s mL" % num(v * 0.09, 1)
    return item("A student freezes %s mL of water in a plastic cup. By about how much does the volume increase? (Water expands about 9%% when it freezes.)" % num(v), g,
                uniq(g, ["%s mL" % num(v * 1.09, 1), "9 mL", "0 mL", "%s mL" % num(v * 0.9, 1)]), "9%% of %s = %s mL." % (num(v), num(v * 0.09, 1)))


@safe
def g_poro():
    who = P.next()[0]
    tot = R.choice([100, 200, 250, 400, 500])
    pct = R.choice([10, 15, 20, 25, 30, 35, 40, 45])
    pore = tot * pct / 100
    if pore != int(pore) or not once(("po", tot, pct)):
        return None
    g = "%d%%" % pct
    return item("%s fills a %d mL beaker with dry sediment, then adds %s mL of water until it reaches the top of the sediment. What is the porosity?" % (who, tot, num(pore)), g,
                uniq(g, ["%d%%" % (100 - pct), "%s%%" % num(pore), "%s%%" % num(tot / pore, 1), "%d%%" % (pct * 2)]), "%s ÷ %d × 100 = %d%%." % (num(pore), tot, pct))


SED = [("gravel", 40, "very fast"), ("coarse sand", 30, "fast"), ("fine sand", 20, "medium"), ("silt", 10, "slow"), ("clay", 5, "very slow")]


@safe
def g_perm():
    who = P.next()[0]
    rows = R.sample(SED, 4)
    k = R.choice(["fast", "slow"])
    times = {"gravel": 8, "coarse sand": 20, "fine sand": 45, "silt": 150, "clay": 600}
    if not once(("pm", tuple(r[0] for r in rows), k)):
        return None
    tab = table(["Sediment", "Time for 100 mL of water to drain through (s)"], [[r[0], str(times[r[0]])] for r in rows])
    if k == "fast":
        a = min(rows, key=lambda r: times[r[0]])[0]
        return item(tab + "Which sediment in %s's test is the most permeable?" % who, a, [r[0] for r in rows if r[0] != a], "Water drains fastest through large, connected spaces.")
    a = max(rows, key=lambda r: times[r[0]])[0]
    return item(tab + "Which sediment in %s's test would make the best barrier to keep water in a pond?" % who, a, [r[0] for r in rows if r[0] != a], "Tiny pores let water through very slowly.")


STR = [(5, "clay only"), (20, "clay, silt and fine sand"), (50, "sand and small pebbles"), (100, "pebbles"), (300, "cobbles and small boulders")]


@safe
def g_stream():
    who = P.next()[0]
    i, j = sorted(R.sample(range(5), 2))
    k = R.choice(["which", "drop"])
    if not once(("st", i, j, k)):
        return None
    tab = table(["Stream speed (cm/s)", "Largest sediment carried"], [[str(v), s] for v, s in STR])
    if k == "which":
        return item(tab + "%s's stream flows at %d cm/s. What is the largest sediment it can carry?" % (who, STR[j][0]), STR[j][1], [STR[x][1] for x in range(5) if x != j][:3], "Faster water carries larger particles.")
    return item(tab + "A stream slows from %d cm/s to %d cm/s where it enters a lake. What happens to the larger sediment?" % (STR[j][0], STR[i][0]), "It is deposited because the slower water cannot carry it.",
                ["It is carried farther.", "It dissolves.", "It is pushed upstream."], "Slowing water drops its load: deltas form.")


WTH = [("Ice forms in a crack and splits a boulder.", "physical weathering"), ("Rainwater with CO₂ dissolves a marble statue.", "chemical weathering"),
       ("Iron in rocks reacts with water and oxygen and turns red-brown.", "chemical weathering"), ("Pebbles in a river knock together and become rounded.", "physical weathering"),
       ("Feldspar in granite slowly changes into clay in wet soil.", "chemical weathering"), ("Waves hurl sand against a cliff and wear it away.", "physical weathering")]


@safe
def g_wth():
    s, t = R.choice(WTH)
    if not once(("wt", s)):
        return None
    return item("%s Which type of weathering is this?" % s, t, ["chemical weathering" if t == "physical weathering" else "physical weathering", "deposition", "volcanism"],
                "Physical weathering breaks rock into pieces; chemical weathering changes the minerals.")


B1 = bank([
    ("What happens to water's volume when it freezes?", "It expands by about 9%.", ["It shrinks.", "It stays the same.", "It doubles."], "Ice is less dense."),
    ("What is frost wedging?", "Water freezes in cracks, expands and breaks rock apart.", ["Ice melting into rock.", "Wind carrying snow.", "Frost growing on leaves."], "Physical weathering."),
    ("How do limestone caves form?", "Slightly acidic groundwater dissolves the limestone.", ["Wind carves them.", "Volcanoes blow them out.", "Animals dig them."], "Chemical weathering."),
    ("What is porosity?", "the percent of a rock or sediment that is open space", ["how fast water flows through it", "its color", "its weight"], "Pore space."),
    ("What is permeability?", "how easily water can flow through a material", ["how much space it has", "how hard it is", "how old it is"], "Connected pores."),
    ("Why do coastal cities have milder temperatures than inland cities?", "Water's high heat capacity keeps the ocean's temperature steady.", ["The ocean is always warm.", "Salt heats the air.", "Coasts get less sunlight."], "Heat capacity."),
    ("Which water property lets it dissolve so many minerals?", "Water molecules are polar.", ["Water is very heavy.", "Water is a metal.", "Water is a gas."], "Universal solvent."),
    ("Why is ocean water salty?", "Rivers carry dissolved minerals from weathered rock into the sea, where water evaporates and leaves salt behind.", ["Fish make salt.", "Rain is salty.", "Salt comes from the Moon."], "Dissolved load."),
])
B5 = bank([
    ("Design an investigation: does freezing break rock? What is a good plan?", "Soak identical rock samples, freeze and thaw some many times, keep others at room temperature, and compare cracks.",
     ["Freeze one rock once and look.", "Heat rocks in an oven only.", "Ask people if rocks break."], "Control and repetition."),
    ("Why are potholes worse after winters with many freeze–thaw cycles?", "Each cycle of freezing water widens cracks in the road.", ["Snow is heavy.", "Salt makes roads grow.", "Ice is soft."], "Frost wedging."),
    ("A gravestone made of marble is harder to read than one made of granite of the same age. Why?", "Marble dissolves more easily in slightly acidic rain.", ["Granite is softer.", "Marble is newer.", "Granite absorbs letters."], "Chemical weathering rate."),
    ("Why do deltas form where rivers enter the ocean?", "The river slows down and drops the sediment it was carrying.", ["The ocean pushes sand upstream.", "Fish build them.", "The river speeds up."], "Deposition."),
    ("A farmer's field floods easily and water stays on top. Which soil is likely?", "clay, because it has low permeability", ["gravel", "coarse sand", "pebbles"], "Drainage."),
])


def body():
    think = ("<p><b>Water's special properties shape Earth's surface.</b></p>"
             "<ul><li>Expands 9% when frozen → frost wedging. Slightly acidic and polar → dissolves minerals, forms caves.</li>"
             "<li>High heat capacity moderates climate; cohesion moves water through soil.</li>"
             "<li>Faster streams carry bigger sediment; slowing water deposits it. Porosity = pore volume ÷ total × 100.</li></ul>")
    ex = [("200 mL of water freezes. Ice volume?", ["200 × 1.09"], "218 mL"),
          ("400 mL sediment holds 120 mL water. Porosity?", ["120 ÷ 400"], "30%")]
    mist = ["Thinking water shrinks when it freezes.", "Thinking clay drains water fastest.", "Thinking slow streams can carry boulders."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Water's properties", B1 + [(g_prop, 8), (g_wth, 3), (g_expand, 1)]),
        ("Weathering", [(g_wth, 2), (g_prop, 5), (g_expand, 13)]),
        ("Porosity and permeability", [(g_poro, 14), (g_perm, 6)]),
        ("Streams and sediment", [(g_stream, 14), (g_expand, 6)]),
        ("Investigating water", B5 + [(g_poro, 7), (g_stream, 5), (g_perm, 3)]),
    ])
    make("earth-and-space-science", "water-and-earth-materials", 11, "HS-ESS2-5",
         "Plan and conduct an investigation of the properties of water and its effects on Earth materials and surface processes.",
         "Water and Earth Materials",
         "Water and Weathering Worksheets: Frost Wedging, Porosity and Stream Sediment (Earth Science)",
         "Water and Earth Materials",
         "Free high school Earth and space science worksheets on water and Earth materials (NGSS HS-ESS2-5): water's properties, frost wedging, chemical weathering, porosity, permeability and stream sediment. 100 questions with answers.",
         "Water shapes rock and land.",
         "Freezing, dissolving and flowing water weather, move and deposit Earth materials.",
         body(),
         [("How does water break rock?", "Water seeps into cracks, freezes and expands about 9%, prying the rock apart (frost wedging). Slightly acidic water also dissolves some minerals."),
          ("What is the difference between porosity and permeability?", "Porosity is how much open space a material has. Permeability is how easily water flows through it, which needs connected spaces."),
          ("Why do rivers drop sediment?", "When a river slows down, it no longer has enough energy to carry larger particles, so they settle out.")],
         sets)


if __name__ == "__main__":
    main()
