# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U04: energy flow between the geosphere, biosphere, hydrosphere and
atmosphere, the greenhouse effect, Earth's energy budget and albedo, feedbacks, evidence of climate change and its effects in
Australia, and responses to it.
  python tools/gen_au_science_y10_global_systems_and_climate_change.py
Reuses the US Earth and Space Science climate, climate change data and feedback makers, the US Grade 6 climate change makers and
the UK Year 8 atmosphere and climate makers with Australian names, plus own questions on Australian evidence (BoM and CSIRO
State of the Climate, coral bleaching, bushfire seasons, sea-level rise).
Wrong answers come from real mistakes: confusing the greenhouse effect with the ozone hole, thinking weather and climate are the
same, and thinking the greenhouse effect is entirely bad.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

CE = "gen_us_science_ess_climate_and_energy_flow"
CD = "gen_us_science_ess_climate_change_data_and_models"
FB = "gen_us_science_ess_feedbacks_in_earth_systems"
G6 = "gen_us_science_g6_global_temperature_and_climate_change"
A8 = "gen_uk_science_y8_the_atmosphere_and_climate"
NO = ["°F", "Fahrenheit", "inch", "feet", "foot", "mile", "[Bb]eaver", "U\\.S\\.", "Alaska"]
c_budget = limit(src(CE, "g_budget", drop=NO), 5)
c_eff = src(CE, "g_eff", drop=NO)
c_ice = src(CE, "g_ice", drop=NO)
c_b1 = src.B(CE, "B1", drop=NO)
c_b5 = src.B(CE, "B5", drop=NO)
d_fc = limit(src(CD, "g_fc", drop=NO), 5)
d_imp = src(CD, "g_imp", drop=NO)
d_sea = limit(src(CD, "g_sea", drop=NO), 4)
d_rate = src(CD, "g_rate", drop=NO)
d_scen = src(CD, "g_scen", drop=NO)
d_b5 = src.B(CD, "B5", drop=NO)
f_alb = limit(src(FB, "g_alb", drop=NO), 5)
f_fb = src(FB, "g_fb", drop=NO)
f_sys = src(FB, "g_sys", drop=NO)
f_b1 = src.B(FB, "B1", drop=NO)
g_cause = src(G6, "g_cause", drop=NO)
g_co2 = src(G6, "g_co2", drop=NO)
a_comp = src(A8, "g_comp", drop=NO)
a_src = src(A8, "g_src", drop=NO)
a_b5 = src.B(A8, "B5", drop=NO)

POOL1 = pool(R, [
    ("What is the greenhouse effect?", "Greenhouse gases absorb heat radiated from Earth's surface and re-emit some back, warming the planet.", ["The ozone layer has a hole that lets heat in.", "Plants make the air hot.", "The Sun gets hotter each year."], "Without it, Earth would be about −18 °C on average."),
    ("Which gases are the main greenhouse gases?", "water vapour, carbon dioxide, methane and nitrous oxide", ["oxygen and nitrogen", "helium and neon", "argon only"], "Oxygen and nitrogen do not absorb infrared radiation."),
    ("What is the enhanced greenhouse effect?", "extra warming caused by humans adding greenhouse gases to the atmosphere", ["the normal warming that keeps Earth habitable", "cooling caused by clouds", "the ozone hole"], "Burning fossil fuels is the biggest cause."),
    ("What is the difference between weather and climate?", "Weather is day-to-day conditions; climate is the average pattern over decades.", ["They mean the same thing.", "Climate changes every hour.", "Weather lasts for centuries."], "A cold day does not disprove climate change."),
    ("According to the Bureau of Meteorology and CSIRO, how much has Australia warmed since 1910?", "about 1.5 °C", ["about 15 °C", "it has cooled", "about 0.01 °C"], "Most of the warming has been since 1950."),
    ("Why is warmer ocean water a threat to the Great Barrier Reef?", "It causes coral bleaching, when corals expel the algae they need.", ["Corals grow faster.", "It makes the water clearer.", "It has no effect."], "Mass bleaching events have become more frequent."),
    ("What is albedo?", "the fraction of sunlight a surface reflects", ["the temperature of the ocean", "a greenhouse gas", "the amount of rain"], "Ice has a high albedo; oceans have a low albedo."),
    ("Why is melting sea ice a positive feedback?", "Darker ocean absorbs more sunlight, causing more warming and more melting.", ["Ice reflects more when it melts.", "It cools the planet.", "It stops all warming."], "Positive feedbacks amplify a change."),
    ("Which sphere includes all the water on Earth, such as oceans, rivers and ice?", "the hydrosphere", ["the geosphere", "the biosphere", "the atmosphere"], "Ice is sometimes called the cryosphere."),
    ("How do oceans affect climate?", "They store and move huge amounts of heat around the globe.", ["They have no effect.", "They make the air dry.", "They only affect fish."], "Ocean currents like the East Australian Current carry warm water south."),
    ("Which is a way to reduce greenhouse gas emissions?", "using renewable energy such as solar and wind", ["burning more coal", "clearing more forests", "driving more"], "Australia is a world leader in rooftop solar."),
    ("Why are sea levels rising?", "Warmer water expands and land ice is melting.", ["The sea floor is rising.", "More rain falls on the ocean only.", "Fish are adding water."], "Low-lying Pacific islands and coasts are at risk."),
])
POOL5 = pool(R, [
    ("Mia puts thermometers in two sealed jars under a lamp. One jar has extra CO₂. After 20 minutes it is 2 °C warmer. What does this model?", "the greenhouse effect of carbon dioxide", ["the ozone hole", "ocean currents", "the water cycle"], "CO₂ absorbs infrared radiation."),
    ("What is a limitation of Mia's jar model?", "A jar is a closed space; the real atmosphere is open and much larger.", ["It shows warming.", "It uses a thermometer.", "It has no limitations."], "Models simplify real systems."),
    ("Jack graphs Australia's average temperature since 1910. The line goes up and down each year but rises overall. How should he describe it?", "a long-term warming trend with year-to-year variation", ["no change", "a cooling trend", "random data with no pattern"], "Look at the trend, not single years."),
    ("Ruby puts a white card and a black card in the sun and measures their temperatures. The black card is hotter. What does this show about albedo?", "Dark surfaces absorb more sunlight (low albedo).", ["White surfaces absorb more.", "Colour has no effect.", "Black reflects more light."], "This is why melting ice speeds up warming."),
    ("Kai compares ice cores from Antarctica. Layers with more CO₂ also show higher temperatures. What can he say?", "CO₂ and temperature are strongly linked over long periods.", ["CO₂ has no effect.", "Ice cores show only rainfall.", "Temperature makes CO₂ disappear."], "Ice cores trap ancient air bubbles."),
    ("Ella reads that bushfire weather days in south-east Australia have increased. Which question could she investigate with data?", "Has the number of high fire-danger days changed since 1950?", ["Are bushfires scary?", "Which tree is the prettiest?", "Do people like summer?"], "A good question can be answered with data."),
    ("Noah models sea-level rise by putting ice in a cup of water and on a 'land' block above another cup. Which cup's water level rises?", "the cup where ice melts from the land block", ["the cup with floating ice", "neither", "both rise the same"], "Floating ice already displaces its own weight of water."),
    ("Zara reads two websites about climate change: one from CSIRO, one from an anonymous blog. Which is more reliable and why?", "CSIRO, because its research is peer reviewed and based on data", ["the blog, because it is shorter", "both equally", "neither"], "Check the source and the evidence."),
])


def main():
    sets = U.sets([
        ("Earth's spheres and energy flow", [(POOL1, 5), (f_sys, 5), (c_budget, 4), (c_eff, 3), (c_b1, 3)]),
        ("The greenhouse effect", [(a_comp, 5), (a_src, 5), (g_cause, 4), (POOL1, 3), (g_co2, 3)]),
        ("Albedo and feedbacks", [(f_alb, 5), (f_fb, 6), (c_ice, 4), (f_b1, 3), (POOL1, 2)]),
        ("Evidence and effects of climate change", [(d_fc, 4), (d_sea, 4), (d_imp, 4), (d_rate, 3), (d_scen, 3), (POOL1, 2)]),
        ("Investigations", [(POOL5, 6), (c_b5, 4), (d_b5, 4), (a_b5, 4), (d_scen, 2)]),
    ])
    make_au(YEAR, "global-systems-and-climate-change", SORT, "AC9S10U04", "Earth and space sciences",
            "Use models of energy flow between the geosphere, biosphere, hydrosphere and atmosphere to explain patterns of global "
            "climate change (summary of the Australian Curriculum v9.0 Science content description).",
            "Global Systems and Climate Change", "Climate change",
            "Free Year 10 science worksheets on global systems and climate change: Earth's spheres, energy flow, the greenhouse "
            "effect, albedo and feedbacks, evidence of climate change and its effects in Australia. 100 questions with answers.",
            "More greenhouse gases trap more heat.", "Human emissions enhance the natural greenhouse effect, warming the atmosphere and oceans.",
            "<p><b>Energy flows between Earth's four spheres: geosphere, biosphere, hydrosphere and atmosphere.</b></p><ul>"
            "<li>Greenhouse gases absorb heat radiated from Earth's surface. Extra CO₂ and methane from human activity enhance this effect.</li>"
            "<li>Feedbacks: melting ice lowers albedo (positive feedback) and speeds up warming.</li>"
            "<li>Evidence: rising temperatures, sea levels and ocean heat; more coral bleaching and fire-danger days in Australia.</li></ul>",
            [("Ice melts and exposes dark ocean. Effect?", ["albedo falls", "more sunlight absorbed"], "more warming (positive feedback)"),
             ("Is a cold week evidence against climate change?", ["weather is short term", "climate is long-term average"], "no")],
            ["Confusing the greenhouse effect with the ozone hole.", "Thinking weather and climate are the same.",
             "Thinking the natural greenhouse effect is bad (it keeps Earth warm enough for life)."],
            [("What causes climate change?", "Mainly the extra greenhouse gases from burning fossil fuels, clearing land and farming, which trap more heat in the atmosphere."),
             ("What is the evidence that the climate is changing?", "Thermometer records, rising sea levels, shrinking ice sheets and glaciers, warmer oceans, and changes in when plants flower and animals migrate."),
             ("How is climate change affecting Australia?", "Australia has warmed about 1.5 °C since 1910, with more extreme heat, longer fire seasons, coral bleaching on the Great Barrier Reef and rising sea levels.")],
            sets)


if __name__ == "__main__":
    main()
