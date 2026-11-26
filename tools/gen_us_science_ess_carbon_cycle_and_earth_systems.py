# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: The Carbon Cycle and Earth Systems (HS-ESS2-6, HS-ESS3-6)
  python tools/gen_us_science_ess_carbon_cycle_and_earth_systems.py
Develop a quantitative model to describe the cycling of carbon among the hydrosphere, atmosphere, geosphere, and
biosphere; use a computational representation to illustrate the relationships among Earth systems and how those
relationships are being modified due to human activity.
Carbon reservoirs (gigatons of carbon), fluxes between spheres, a yearly carbon budget (emissions, ocean and land sinks,
the airborne fraction, 2.1 Gt C per ppm), the Keeling curve and ocean acidification.
Wrong answers come from real mistakes: "most carbon is in the air", "the ocean absorbs no CO₂", "all emitted CO₂ stays
in the air", "a lower pH means less acidic".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90412)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


RES = [("the atmosphere", 870), ("the ocean (dissolved carbon)", 38000), ("soils", 1700), ("living plants", 450), ("known fossil fuel reserves", 1000), ("permafrost", 1400), ("sedimentary rocks like limestone", 60000000)]


@safe
def g_res():
    who = P.next()[0]
    rs = R.sample(RES, 4)
    k = R.choice(["big", "small"])
    if not once(("rs", tuple(sorted(r[0] for r in rs)), k)):
        return None
    tab = table(["Reservoir", "Carbon stored (billion tons)"], [[r[0], num(r[1])] for r in rs])
    a = max(rs, key=lambda r: r[1]) if k == "big" else min(rs, key=lambda r: r[1])
    return item(tab + "In %s's model, which reservoir holds the %s carbon?" % (who, "most" if k == "big" else "least"), a[0], [r[0] for r in rs if r != a],
                "Rocks hold by far the most carbon; the atmosphere holds relatively little.")


FLUX = [("photosynthesis", "from the atmosphere into the biosphere"), ("respiration by plants and animals", "from the biosphere into the atmosphere"),
        ("CO₂ dissolving into the ocean surface", "from the atmosphere into the hydrosphere"), ("burning coal, oil and gas", "from the geosphere into the atmosphere"),
        ("volcanic eruptions", "from the geosphere into the atmosphere"), ("shells and sediment settling on the seafloor and becoming rock", "from the hydrosphere into the geosphere"),
        ("cutting and burning forests", "from the biosphere into the atmosphere"), ("dead plants buried and turned into coal over millions of years", "from the biosphere into the geosphere"),
        ("rock weathering that uses CO₂ from rainwater", "from the atmosphere into the geosphere"), ("decomposers breaking down dead organisms", "from the biosphere into the atmosphere")]


@safe
def g_flux():
    p, d = R.choice(FLUX)
    k = R.random() < 0.6
    if not once(("fx", p, k)):
        return None
    if k:
        return item("Which way does %s move carbon?" % p, d, R.sample(sorted({x[1] for x in FLUX if x[1] != d}), 3), "Follow the carbon from one sphere to another.")
    return item("Which process moves carbon %s?" % d, p, R.sample([x[0] for x in FLUX if x[1] != d], 3), "Match the process to the flow.")


@safe
def g_budget():
    who = P.next()[0]
    em = R.choice([8, 9, 9.5, 10, 10.5, 11])
    oc = R.choice([2, 2.5, 2.8, 3])
    ln = R.choice([2.5, 3, 3.2, 3.5])
    air = round(em - oc - ln, 1)
    k = R.choice(["air", "frac", "ppm"])
    if air <= 0 or not once(("bg", em, oc, ln, k)):
        return None
    if k == "air":
        g = "%s billion tons" % num(air, 1)
        return item("%s's model: humans emit %s billion tons of carbon per year; the ocean takes up %s and land plants take up %s. How much stays in the atmosphere each year?" % (who, num(em, 1), num(oc, 1), num(ln, 1)), g,
                    uniq(g, ["%s billion tons" % num(em, 1), "%s billion tons" % num(em + oc + ln, 1), "0 billion tons", "%s billion tons" % num(oc + ln, 1)]), "%s − %s − %s = %s." % (num(em, 1), num(oc, 1), num(ln, 1), num(air, 1)))
    if k == "frac":
        f = round(100 * air / em)
        g = "about %d%%" % f
        return item("Of %s billion tons of carbon emitted, %s billion tons stay in the air. About what percent is that (the airborne fraction)?" % (num(em, 1), num(air, 1)), g,
                    uniq(g, ["about %d%%" % (100 - f), "about 100%", "about %d%%" % round(air * 10), "about 0%"]), "%s ÷ %s × 100 ≈ %d%%." % (num(air, 1), num(em, 1), f))
    ppm = air / 2.1
    g = "about %s ppm" % num(ppm, 1)
    return item("%s billion tons of carbon are added to the atmosphere in a year. About how much does CO₂ rise? (2.1 billion tons of carbon ≈ 1 ppm)" % num(air, 1), g,
                uniq(g, ["about %s ppm" % num(air * 2.1, 1), "about %s ppm" % num(air, 1), "about %s ppm" % num(ppm * 10, 1), "about 0 ppm"]), "%s ÷ 2.1 ≈ %s ppm." % (num(air, 1), num(ppm, 1)))


KEEL = {1960: 317, 1970: 326, 1980: 339, 1990: 354, 2000: 370, 2010: 390, 2020: 414}


@safe
def g_keel():
    who = P.next()[0]
    a, b = sorted(R.sample(sorted(KEEL), 2))
    k = R.choice(["rise", "rate", "trend"])
    if not once(("kl", a, b, k)) or (k == "trend" and not once("klt", 3)):
        return None
    tab = table(["Year", "CO₂ at Mauna Loa (ppm)"], [[str(y), str(KEEL[y])] for y in sorted(KEEL)])
    d = KEEL[b] - KEEL[a]
    if k == "rise":
        g = "%d ppm" % d
        return item(tab + "Using %s's table, by how much did CO₂ rise from %d to %d?" % (who, a, b), g, uniq(g, ["%d ppm" % KEEL[b], "%d ppm" % (d + 10), "%d ppm" % (b - a), "%d ppm" % KEEL[a]]),
                    "%d − %d = %d ppm." % (KEEL[b], KEEL[a], d))
    if k == "rate":
        r = d / (b - a)
        g = "about %s ppm per year" % num(r, 1)
        return item(tab + "What was the average rate of CO₂ rise from %d to %d?" % (a, b), g, uniq(g, ["about %s ppm per year" % num(d, 1), "about %s ppm per year" % num(r * 10, 1), "about %s ppm per year" % num((b - a) / d, 2), "about 0 ppm per year"]),
                    "%d ppm ÷ %d years = %s." % (d, b - a, num(r, 1)))
    return item(tab + "What do %s's Mauna Loa data show?" % who, "CO₂ is rising, and the rise is getting faster.", ["CO₂ is falling.", "CO₂ is steady.", "CO₂ rises at exactly the same rate every decade."],
                "About 0.9 ppm/yr in the 1960s; about 2.4 ppm/yr by the 2010s.")


@safe
def g_ph():
    k = R.choice(["dir", "fold"])
    if k == "dir":
        s = R.choice(["The ocean absorbs more CO₂ from the air.", "CO₂ dissolves in seawater and forms carbonic acid.", "Atmospheric CO₂ keeps rising."])
        if not once(("ph", s)):
            return None
        return item("%s What happens to ocean pH?" % s, "It goes down (the water becomes more acidic).", ["It goes up (less acidic).", "It stays the same.", "It becomes exactly 7."],
                    "More H⁺ ions → lower pH. Since 1750, surface ocean pH fell from about 8.2 to 8.1.")
    d = R.choice([1, 2, 3])
    if not once(("fd", d)):
        return None
    g = "%d times" % 10 ** d
    return item("pH is a log scale. If the pH of water drops by %d unit%s, how many times more acidic is it?" % (d, "" if d == 1 else "s"), g, uniq(g, ["%d times" % d, "%d times" % (2 * d), "%d times" % (10 * d), "%d times" % 10 ** (d + 1)]),
                "Each pH unit is a factor of 10: 10<sup>%d</sup>." % d)


B1 = bank([
    ("Where is most of Earth's carbon stored?", "in rocks such as limestone and in the deep ocean", ["in the atmosphere", "in living animals", "in the Sun"], "Huge, slow reservoirs."),
    ("How does photosynthesis affect atmospheric CO₂?", "It removes CO₂ from the air and stores carbon in plants.", ["It adds CO₂ to the air.", "It has no effect.", "It turns CO₂ into nitrogen."], "Biosphere sink."),
    ("Why has atmospheric CO₂ risen since the 1800s?", "Burning fossil fuels and clearing forests release carbon faster than sinks can absorb it.", ["Volcanoes erupted more.", "The ocean released CO₂.", "Plants grew less only."], "Human activity."),
    ("What are fossil fuels?", "the remains of ancient organisms buried and changed into coal, oil and gas", ["recently fallen leaves", "rocks from volcanoes", "minerals from meteorites"], "Geosphere carbon."),
    ("What does the ocean do with some of the CO₂ we emit?", "It absorbs about a quarter of it.", ["It absorbs none.", "It absorbs all of it.", "It turns it into oxygen gas."], "Ocean sink."),
    ("What is ocean acidification?", "the drop in ocean pH as seawater absorbs CO₂", ["the ocean becoming saltier", "the ocean warming", "the ocean freezing"], "Carbonic acid."),
    ("Why is ocean acidification a problem for corals and shellfish?", "It makes it harder for them to build calcium carbonate shells and skeletons.", ["It makes the water too cold.", "It adds too much oxygen.", "It makes them grow too fast."], "Carbonate chemistry."),
    ("Why does CO₂ at Mauna Loa go up and down each year?", "Northern Hemisphere plants take in CO₂ in summer and release it in winter.", ["Volcanoes erupt every summer.", "The ocean freezes.", "Cars stop in summer."], "Seasonal cycle."),
])
B5 = bank([
    ("A model shows emissions doubling but the ocean and land sinks staying the same. What will the model predict?", "CO₂ will rise much faster in the atmosphere.", ["CO₂ will fall.", "Nothing will change.", "The sinks will grow without limit."], "Computational model."),
    ("Which change would most reduce the carbon flowing into the atmosphere?", "replacing coal power plants with solar and wind", ["cutting more forests", "burning more natural gas", "draining wetlands"], "Reduce the source."),
    ("Why do scientists say the carbon cycle is 'out of balance'?", "Humans move carbon from slow geosphere reservoirs to the air far faster than natural processes return it.", ["The carbon cycle stopped.", "Plants make carbon.", "The ocean lost all carbon."], "Rates matter."),
    ("Why is protecting forests and wetlands part of climate solutions?", "They store large amounts of carbon and keep absorbing CO₂.", ["They release oxygen only.", "They make CO₂.", "They cool the Sun."], "Natural sinks."),
    ("Isotope studies show the extra CO₂ in the air has the carbon 'fingerprint' of fossil fuels. What does this support?", "Human burning of fossil fuels is the main source of the CO₂ rise.", ["Volcanoes caused the rise.", "The ocean caused the rise.", "The CO₂ is not rising."], "Evidence of the source."),
])


def body():
    think = ("<p><b>Carbon moves among the air, oceans, rocks and living things.</b></p>"
             "<ul><li>Reservoirs: rocks and the deep ocean hold the most; the air holds relatively little, so small changes matter.</li>"
             "<li>Humans move carbon from fossil fuels (geosphere) to the air. About half stays in the air; the ocean and land take up the rest.</li>"
             "<li>Budget: emissions − ocean uptake − land uptake = carbon added to the air (2.1 billion tons ≈ 1 ppm). Extra CO₂ also lowers ocean pH.</li></ul>")
    ex = [("Emit 10, ocean 2.5, land 3. Left in air?", ["10 − 2.5 − 3"], "4.5 billion tons"),
          ("4.2 billion tons added. ppm rise?", ["4.2 ÷ 2.1"], "about 2 ppm")]
    mist = ["Thinking most carbon is in the air.", "Thinking all emitted CO₂ stays in the air.", "Thinking a lower pH means less acidic."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Carbon reservoirs", B1 + [(g_res, 6), (g_flux, 6)]),
        ("Carbon flows", [(g_flux, 10), (g_res, 10)]),
        ("The carbon budget", [(g_budget, 16), (g_ph, 4)]),
        ("The Keeling curve", [(g_keel, 16), (g_budget, 4)]),
        ("Modeling human impacts", B5 + [(g_budget, 9), (g_keel, 5), (g_ph, 1)]),
    ])
    make("earth-and-space-science", "carbon-cycle-and-earth-systems", 12, "HS-ESS2-6, HS-ESS3-6",
         "Develop a quantitative model to describe the cycling of carbon among the hydrosphere, atmosphere, geosphere, and biosphere. "
         "Use a computational representation to illustrate the relationships among Earth systems and how those relationships are being modified due to human activity.",
         "The Carbon Cycle and Earth Systems",
         "Carbon Cycle Worksheets: Reservoirs, Carbon Budget, Keeling Curve and Ocean pH (Earth Science)",
         "Carbon Cycle",
         "Free high school Earth and space science worksheets on the carbon cycle (NGSS HS-ESS2-6, HS-ESS3-6): carbon reservoirs and flows, the yearly carbon budget, the Keeling curve and ocean acidification. 100 questions with answers.",
         "Carbon cycles through all four spheres.",
         "Humans move fossil carbon into the air; the ocean and land absorb only part of it.",
         body(),
         [("Where is carbon stored on Earth?", "In rocks (the largest store), the ocean, soils, living things, fossil fuels and the atmosphere."),
          ("How do humans change the carbon cycle?", "Burning fossil fuels and clearing forests move carbon into the atmosphere much faster than natural processes remove it."),
          ("What is ocean acidification?", "When seawater absorbs CO₂, it forms carbonic acid, which lowers the ocean's pH and makes it harder for shell-building organisms.")],
         sets)


if __name__ == "__main__":
    main()
