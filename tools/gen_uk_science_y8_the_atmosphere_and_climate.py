# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Chemistry: Earth and atmosphere): The Atmosphere and Climate
  python tools/gen_uk_science_y8_the_atmosphere_and_climate.py
The composition of the atmosphere, the carbon cycle (photosynthesis, respiration, combustion, decay, oceans), the
greenhouse effect, the production of carbon dioxide by human activity and its impact on climate, evidence for
climate change and ways to reduce emissions. Reuses the climate-change and human-impact questions of the US Grade 6–7
units in British English.
Wrong answers come from real mistakes: "the air is mostly oxygen", "the greenhouse effect is caused by the ozone hole",
"carbon dioxide is the most common gas in the air", "weather and climate are the same".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us, pie

U = Unit(61810)
R = U.R
P = People(R)
uk_sci.USED.clear()
GT = adopt_us("gen_us_science_g6_global_temperature_and_climate_change", U)
HI = adopt_us("gen_us_science_g7_human_impact_on_the_environment", U)
us_cause, us_co2, us_evid, us_temp = ukm(GT.g_cause), ukm(GT.g_co2), ukm(GT.g_evid), ukm(GT.g_temp)
us_imp = ukm(HI.g_impact)

AIR = [("nitrogen", "78%"), ("oxygen", "21%"), ("argon", "just under 1%"), ("carbon dioxide", "about 0.04%")]


def g_comp():
    k = R.choice(["most", "pct_n", "pct_o", "pct_c", "second", "least", "noble"])
    if not once(("cm", k)):
        return None
    tab = table(["Gas", "Approximate amount in dry air"], [list(r) for r in AIR])
    if k == "most":
        return item("Which gas makes up most of the air?", "nitrogen", ["oxygen", "carbon dioxide", "argon"], "About 78%.")
    if k == "second":
        return item("Which gas is the second most common in the air?", "oxygen", ["nitrogen", "carbon dioxide", "water vapour"], "About 21%.")
    if k == "pct_n":
        return item("About what percentage of the air is nitrogen?", "78%", ["21%", "50%", "99%"], "Roughly four-fifths.")
    if k == "pct_o":
        return item("About what percentage of the air is oxygen?", "21%", ["78%", "1%", "50%"], "Roughly one-fifth.")
    if k == "pct_c":
        return item("About what percentage of the air is carbon dioxide?", "0.04%", ["4%", "21%", "40%"], "A very small amount, but important.")
    if k == "least":
        return item(tab + "Which of these gases is present in the smallest amount?", "carbon dioxide", ["argon", "oxygen", "nitrogen"], "0.04%.")
    return item(tab + "Which gas in the table is a noble gas?", "argon", ["nitrogen", "oxygen", "carbon dioxide"], "Group 0.")


CC = [("photosynthesis by plants", "removes carbon dioxide from the air"), ("respiration by animals and plants", "adds carbon dioxide to the air"),
      ("burning fossil fuels", "adds carbon dioxide to the air"), ("decomposers breaking down dead material", "adds carbon dioxide to the air"),
      ("carbon dioxide dissolving in the oceans", "removes carbon dioxide from the air"), ("cutting down and burning forests", "adds carbon dioxide to the air"),
      ("planting new forests", "removes carbon dioxide from the air"), ("volcanoes erupting", "adds carbon dioxide to the air")]


def g_cc():
    p, a = R.choice(CC)
    if not once(("cc", p)):
        return None
    return item("In the carbon cycle, what does %s do?" % p, a, [x for x in ["adds carbon dioxide to the air", "removes carbon dioxide from the air", "has no effect on carbon dioxide", "turns carbon dioxide into nitrogen"] if x != a],
                "Photosynthesis and oceans remove it; respiration, decay and combustion add it.")


FF = [("coal", "carbon dioxide"), ("natural gas (methane)", "carbon dioxide and water"), ("petrol", "carbon dioxide and water"), ("diesel", "carbon dioxide and water")]


def g_ff():
    f, p = R.choice(FF)
    k = R.choice(["prod", "why", "renew"])
    if not once(("ff", f, k)) or not once(("ff", k), 4 if k == "prod" else 1):
        return None
    if k == "prod":
        return item("What is mainly made when %s burns completely?" % f, p, R.sample(["sulfur dioxide only", "oxygen and nitrogen", "hydrogen", "carbon dioxide and water" if p != "carbon dioxide and water" else "carbon dioxide only"], 3),
                    "Fossil fuels contain carbon (and hydrogen).")
    if k == "why":
        return item("Why are coal, oil and gas called fossil fuels?", "They formed from the remains of living things millions of years ago.", ["They contain dinosaur bones.", "They were made in factories.", "They come from rocks in the core."], "Stored carbon.")
    return item("Why are fossil fuels described as non-renewable?", "They take millions of years to form, so they will run out.", ["They can be regrown each year.", "They never run out.", "They are made from sunlight daily."], "Finite.")


def g_ppm():
    who = P.next()[0]
    yrs = [1960, 1980, 2000, 2020]
    base = R.choice([315, 316, 317])
    v = [base, base + R.choice([22, 23, 24]), base + R.choice([52, 53, 54, 55]), base + R.choice([95, 96, 97, 98])]
    k = R.choice(["rise", "trend", "first", "cause", "pred"])
    if not once(("pp", tuple(v), k)) or not once(("pp", k), 3 if k in ("trend", "cause", "pred") else 8):
        return None
    tab = table(["Year", "Carbon dioxide (parts per million)"], [[str(y), str(x)] for y, x in zip(yrs, v)])
    intro = tab + "%s looked up measurements of carbon dioxide in the air. " % who
    if k == "rise":
        d = v[3] - v[0]
        return item(intro + "By how much did the carbon dioxide level rise from 1960 to 2020?", "%d ppm" % d, ["%d ppm" % v[3], "%d ppm" % (v[2] - v[0]), "%d ppm" % (d + 20)], "%d − %d = %d." % (v[3], v[0], d))
    if k == "first":
        d1, d2 = v[1] - v[0], v[3] - v[2]
        return item(intro + "How much did the level rise between 2000 and 2020?", "%d ppm" % d2, ["%d ppm" % d1, "%d ppm" % v[3], "%d ppm" % (d2 + 10)], "%d − %d = %d. It is rising faster than before." % (v[3], v[2], d2))
    if k == "trend":
        return item(intro + "What does the data show?", "Carbon dioxide is rising, and rising faster in recent years.", ["Carbon dioxide is falling.", "It has stayed the same.", "It rose and then fell."], "Compare each 20-year rise.")
    if k == "cause":
        return item(intro + "What is the main cause of this rise?", "burning fossil fuels and cutting down forests", ["more photosynthesis", "volcanoes only", "the ozone hole"], "Human activity.")
    return item(intro + "If the trend continues, what would you expect in 2040?", "a higher level than in 2020", ["a lower level than in 1960", "exactly the 2020 level", "zero"], "Extrapolate with care.")


SRC = [("burning petrol in cars", "carbon dioxide"), ("cattle digesting grass", "methane"), ("rice paddy fields", "methane"), ("rotting rubbish in landfill sites", "methane"),
       ("coal-fired power stations", "carbon dioxide"), ("burning forests to clear land", "carbon dioxide"), ("leaks from natural gas pipes", "methane")]


def g_src():
    s, g = R.choice(SRC)
    if not once(("sr", s)):
        return None
    return item("Which greenhouse gas is mainly released by %s?" % s, g, [x for x in ["carbon dioxide", "methane", "oxygen", "nitrogen"] if x != g], "Carbon dioxide from burning; methane from cattle, rice and landfill.")


B1 = bank([
    ("What is the greenhouse effect?", "Gases in the atmosphere trap heat radiated from the Earth, keeping it warmer.", ["The ozone layer has a hole in it.", "Plants grow in greenhouses.", "The Sun gets hotter each year."], "Natural, but people are increasing it."),
    ("Name two greenhouse gases.", "carbon dioxide and methane", ["nitrogen and oxygen", "argon and helium", "hydrogen and neon"], "Also water vapour."),
    ("What is the difference between weather and climate?", "Weather is day to day; climate is the average weather over many years.", ["They are the same.", "Climate changes every hour.", "Weather lasts for centuries."], "Long-term averages."),
    ("Why would the Earth be very cold without any greenhouse effect?", "Heat from the ground would escape straight into space.", ["The Sun would go out.", "There would be no wind.", "The oceans would boil."], "About −18 °C on average."),
    ("How has the amount of carbon dioxide in the air changed since the 1800s?", "It has risen a lot.", ["It has fallen to zero.", "It has stayed exactly the same.", "It has risen then fallen back."], "Since the Industrial Revolution."),
])
B5 = bank([
    ("What is one effect of global warming?", "Sea levels rise as ice melts and water expands.", ["The oceans freeze.", "There is less extreme weather.", "The air becomes pure oxygen."], "Also more extreme weather."),
    ("Why does melting sea ice speed up warming?", "Dark water absorbs more sunlight than white ice reflects.", ["Ice is warm.", "Water reflects all light.", "It adds oxygen."], "A feedback."),
    ("How can people reduce their carbon dioxide emissions?", "use less energy, travel by bike or public transport, and use renewable electricity", ["burn more coal", "leave lights on", "cut down forests"], "Many small changes."),
    ("Why is methane from cattle farming a concern?", "Methane is a powerful greenhouse gas.", ["Methane makes oxygen.", "It cools the Earth.", "It is a noble gas."], "Agriculture."),
    ("Why do scientists study air bubbles trapped in ancient ice?", "They show how much carbon dioxide was in the air long ago.", ["They contain fossils of fish.", "They show the age of the Moon.", "They are pure oxygen."], "Ice cores."),
    ("What is a carbon footprint?", "the amount of greenhouse gas released by a person's activities", ["the size of a person's shoe", "the carbon in the soil", "a fossil of a footprint"], "Can be reduced."),
    ("Why are renewable energy sources such as wind and solar better for the climate?", "They do not release carbon dioxide when making electricity.", ["They make more carbon dioxide.", "They use coal.", "They cool the Sun."], "Low carbon."),
    ("How do trees help to slow climate change?", "They take in carbon dioxide for photosynthesis and store the carbon.", ["They give out carbon dioxide only.", "They make methane.", "They have no effect."], "Carbon store."),
    ("What does acid rain come from?", "sulfur dioxide and nitrogen oxides from burning fuels dissolving in rain", ["carbon dioxide from plants", "oxygen in clouds", "argon in the air"], "Damages buildings and lakes."),
    ("Why is it hard to stop climate change quickly?", "Carbon dioxide stays in the air for a long time and the world uses lots of fossil fuels.", ["It is not happening.", "Carbon dioxide disappears in a day.", "Only one country is involved."], "Global problem."),
    ("How did the Earth's early atmosphere get its oxygen?", "Algae and plants made it by photosynthesis.", ["Volcanoes released it.", "It came from the Moon.", "Animals breathed it out."], "Over billions of years."),
])


def body():
    think = ("<p><b>The atmosphere is mostly nitrogen and oxygen, with a little carbon dioxide.</b></p>"
             "<ul><li>Air: about 78% nitrogen, 21% oxygen, 1% argon, 0.04% carbon dioxide.</li>"
             "<li>Carbon cycle: photosynthesis removes carbon dioxide; respiration, decay and burning add it.</li>"
             "<li>Greenhouse gases trap heat. Burning fossil fuels has raised carbon dioxide and warmed the climate.</li></ul>")
    ex = [("Burning coal: what does it add to the air?", ["Coal is mostly carbon"], "carbon dioxide"),
          ("Planting forests: effect on carbon dioxide?", ["Photosynthesis"], "removes it")]
    mist = ["Thinking the air is mostly oxygen.", "Blaming the greenhouse effect on the ozone hole.", "Mixing up weather and climate."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The air", B1[:2] + [(g_comp, 5), (g_ff, 4), (g_cc, 4), (g_src, 5)]),
        ("The carbon cycle", [(g_cc, 3), (g_ff, 1), (us_co2, 5), (us_cause, 4), (g_src, 1), (us_imp, 3), (g_ppm, 3)]),
        ("Greenhouse effect", B1[2:] + [(us_co2, 4), (us_cause, 4), (us_evid, 4), (us_temp, 2), (g_comp, 1), (g_ppm, 2)]),
        ("Carbon dioxide data", [(g_ppm, 14), (us_imp, 4), (us_cause, 1), (us_evid, 1)]),
        ("Climate change", B5 + [(us_imp, 3), (us_cause, 2), (us_co2, 2), (g_ppm, 2)]),
    ])
    make_ks3(8, "the-atmosphere-and-climate", 10, "Chemistry", "Earth and atmosphere",
             "The composition of the atmosphere; the production of carbon dioxide by human activity and the impact on climate; the carbon cycle.",
             "The Atmosphere and Climate",
             "Year 8 Science: The Atmosphere and Climate Worksheets (Carbon Cycle, Greenhouse Effect)",
             "Atmosphere and Climate",
             "Free Year 8 science worksheets on the atmosphere and climate: the gases in air, the carbon cycle, fossil fuels, the greenhouse effect, carbon dioxide data and climate change. 100 questions with answers.",
             "Carbon dioxide traps heat in the atmosphere.",
             "Air is 78% nitrogen and 21% oxygen; burning fossil fuels adds carbon dioxide.",
             body(),
             [("What is the air made of?", "About 78% nitrogen, 21% oxygen, just under 1% argon and about 0.04% carbon dioxide, with some water vapour."),
              ("What is the carbon cycle?", "The way carbon moves between the air, living things, oceans and rocks. Photosynthesis removes carbon dioxide; respiration, decay and combustion return it."),
              ("Why is the climate warming?", "Burning fossil fuels and cutting down forests have increased carbon dioxide and other greenhouse gases, which trap more heat.")],
             sets)


if __name__ == "__main__":
    main()
