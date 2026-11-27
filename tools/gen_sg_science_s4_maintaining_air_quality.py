# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 12: Maintaining Air Quality
  python tools/gen_sg_science_s4_maintaining_air_quality.py
Composition of clean dry air; sources and effects of air pollutants (carbon monoxide, sulfur dioxide, oxides of nitrogen, unburnt
hydrocarbons, ground-level ozone, particulates); acid rain and flue gas desulfurisation; catalytic converters; the ozone layer and
CFCs; the carbon cycle, greenhouse gases and global warming; the Singapore haze and the PSI.
UK KS3/KS4 atmosphere makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "air is mostly oxygen", "carbon dioxide causes acid rain", "the catalytic converter removes
carbon dioxide", "the ozone hole causes global warming", "nitrogen oxides come from nitrogen in the fuel".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, rows, pool, ex

LV, SUBJ, SORT = 4, "Chemistry", 14
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_ghg = src("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_ghg")
uk_src = src("gen_uk_science_y8_the_atmosphere_and_climate", "g_src")

AIR = [("nitrogen", 78), ("oxygen", 21), ("argon", 0.9), ("carbon dioxide", 0.04)]


def g_air():
    g, pc = R.choice(AIR[:2])
    v = R.choice([100, 200, 250, 300, 400, 500, 600, 800, 1000, 1500, 2000])
    a = v * pc / 100
    other = 99 - pc
    return nq("A sample of %d cm³ of clean, dry air is taken. About what volume of it is %s?" % (v, g), a, [v * other / 100, v * (100 - pc) / 100 if pc != 21 else v / 5 * 4, pc],
              " cm³", "%s is about %d%% of air: %d × %d ÷ 100." % (g.capitalize(), pc, v, pc))


g_comp = rows(R, [("nitrogen", "about 78%"), ("oxygen", "about 21%"), ("argon", "about 0.9%"), ("carbon dioxide", "about 0.04%")],
              "About what percentage of clean, dry air is %s?", "Which gas makes up %s of clean, dry air?")

SRC = [("carbon monoxide", "incomplete combustion of carbon-containing fuels, e.g. in car engines"),
       ("sulfur dioxide", "burning fossil fuels that contain sulfur, and volcanoes"),
       ("oxides of nitrogen", "nitrogen and oxygen from the air reacting at high temperatures in car engines and lightning"),
       ("unburnt hydrocarbons", "fuel that does not burn completely in car engines"),
       ("methane", "decomposition of vegetation and waste gases from digestion in cattle"),
       ("particulates (fine dust and soot)", "forest fires and incomplete combustion of diesel")]
EFF = [("carbon monoxide", "combines with haemoglobin and reduces the blood's ability to carry oxygen"),
       ("sulfur dioxide", "irritates the eyes and lungs, and forms acid rain"),
       ("oxides of nitrogen", "form acid rain and photochemical smog, and irritate the lungs"),
       ("unburnt hydrocarbons", "react with oxides of nitrogen in sunlight to form photochemical smog and ground-level ozone"),
       ("ground-level ozone", "irritates the eyes and lungs and damages crops"),
       ("particulates (fine dust and soot)", "get deep into the lungs and worsen asthma and heart disease")]
g_src = rows(R, SRC, "What is the main source of %s in the air?", "Which pollutant comes from this source: %s?")
g_eff = rows(R, EFF, "What is a harmful effect of %s?", "Which pollutant has this effect: it %s?")

CYC = [("photosynthesis", "removes carbon dioxide from the air"), ("respiration", "adds carbon dioxide to the air"),
       ("combustion of fossil fuels", "adds carbon dioxide to the air"), ("dissolving in the oceans", "removes carbon dioxide from the air"),
       ("decay of dead organisms by decomposers", "adds carbon dioxide to the air"), ("burning forests to clear land", "adds carbon dioxide to the air")]


def g_cyc():
    pr, eff = R.choice(CYC)
    wr = sorted({e for _, e in CYC if e != eff}) + ["adds nitrogen to the air", "turns carbon dioxide into methane"]
    return tq("In the carbon cycle, what does %s do?" % pr, eff, wr[:3],
              "Photosynthesis and dissolving in the oceans remove carbon dioxide; respiration, combustion and decay add it.")


PSI = [(50, "Good"), (100, "Moderate"), (200, "Unhealthy"), (300, "Very unhealthy"), (500, "Hazardous")]


def g_psi():
    v = R.randint(15, 420)
    lo = 0
    for hi, band in PSI:
        if v <= hi:
            break
        lo = hi
    others = [b for _, b in PSI if b != band]
    return tq("The 24-hour PSI in Singapore is %d. Which air quality band is this?" % v, band, R.sample(others, 3),
              "PSI bands: 0–50 Good, 51–100 Moderate, 101–200 Unhealthy, 201–300 Very unhealthy, above 300 Hazardous.")


CAT = [("2CO + 2NO", "2CO₂ + N₂"), ("2CO + O₂", "2CO₂"), ("C₈H₁₈ + 12½O₂", "8CO₂ + 9H₂O"), ("2NO", "N₂ + O₂")]


def g_cat():
    l, r = R.choice(CAT)
    wr = [x for _, x in CAT if x != r] + ["2C + 2NO₂", "CO₂ + NO₂"]
    return tq("In a catalytic converter: %s → ? What are the products?" % l, r, R.sample([w for w in wr if w != r], 3),
              "The catalytic converter (platinum or rhodium) turns CO, NO and unburnt hydrocarbons into CO₂, N₂ and H₂O.")


TOWN = ["Jurong", "Tampines", "Woodlands", "Pasir Ris", "Bukit Timah", "Changi", "Clementi", "Sengkang"]


def g_rain():
    ts = R.sample(TOWN, 4)
    acid = R.choice([3.8, 4.0, 4.2, 4.4, 4.5])
    rest = R.sample([5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.2], 3)
    ph = [acid] + rest
    order = list(range(4))
    R.shuffle(order)
    data = "; ".join("%s pH %s" % (ts[i], ex(ph[i])) for i in order)
    return tq("Rainwater samples were tested: %s. Which sample is acid rain?" % data, ts[0], ts[1:],
              "Clean rain is about pH 5.6 because of dissolved carbon dioxide. Acid rain has a lower pH (here pH %s) from dissolved sulfur dioxide and nitrogen dioxide." % ex(acid))


POOL1 = pool(R, [
    ("Which gas is the most abundant in clean, dry air?", "nitrogen", ["oxygen", "carbon dioxide", "argon"], "About 78% of air is nitrogen."),
    ("Why does carbon monoxide form in car engines?", "There is not enough oxygen for complete combustion of the fuel.", ["The fuel contains carbon monoxide.", "Nitrogen reacts with oxygen.", "The engine is too cold."], "Complete combustion gives carbon dioxide."),
    ("Why do oxides of nitrogen form in car engines?", "The high temperature makes nitrogen and oxygen from the air react.", ["Petrol contains nitrogen.", "The catalytic converter makes them.", "They come from unburnt fuel."], "N₂ + O₂ → 2NO."),
    ("How is acid rain formed?", "Sulfur dioxide and nitrogen dioxide dissolve in rainwater (with oxygen) to form sulfuric and nitric acids.", ["Carbon dioxide forms carbonic acid only.", "Ozone dissolves in rain.", "Methane reacts with water."], "Rain is slightly acidic anyway; acid rain has a much lower pH."),
    ("What are two effects of acid rain?", "It damages limestone buildings and statues, and lowers the pH of lakes, killing fish.", ["It thickens the ozone layer and cools the Earth.", "It makes soils more fertile.", "It removes CO₂ from the air."], "Acids react with carbonates and metals."),
    ("How do catalytic converters reduce pollution?", "They convert carbon monoxide, oxides of nitrogen and unburnt hydrocarbons into carbon dioxide, nitrogen and water.", ["They remove carbon dioxide.", "They turn sulfur dioxide into sulfur.", "They make the engine burn less fuel."], "Platinum and rhodium are the catalysts."),
    ("What is flue gas desulfurisation?", "removing sulfur dioxide from power-station waste gases using calcium carbonate or calcium oxide", ["removing carbon dioxide from car exhausts", "adding sulfur to fuels", "removing nitrogen from the air"], "CaCO₃ + SO₂ → CaSO₃ + CO₂."),
    ("Why is powdered limestone added to acidic lakes?", "Calcium carbonate neutralises the acid.", ["It adds oxygen to the water.", "It kills algae.", "It makes the lake more acidic."], "Limestone is a base."),
    ("What does the ozone layer do?", "It absorbs much of the harmful ultraviolet radiation from the Sun.", ["It traps heat and causes global warming.", "It makes acid rain.", "It produces oxygen for breathing."], "Less ozone means more skin cancer and cataracts."),
    ("Which compounds have damaged the ozone layer?", "chlorofluorocarbons (CFCs)", ["carbon dioxide", "sulfur dioxide", "methane"], "Chlorine atoms from CFCs break down ozone; CFCs are now banned."),
    ("Name two greenhouse gases.", "carbon dioxide and methane", ["nitrogen and oxygen", "argon and neon", "oxygen and hydrogen"], "They absorb infrared radiation from the Earth."),
    ("What is the enhanced greenhouse effect?", "Extra greenhouse gases from human activities trap more heat, causing global warming.", ["The ozone hole lets in more heat.", "The Sun gives out more energy.", "Acid rain warms the oceans."], "Leads to melting ice and rising sea levels."),
])
POOL5 = pool(R, [
    ("Singapore is a low-lying island. Which effect of global warming is a particular risk?", "rising sea levels", ["more acid rain", "a thicker ozone layer", "less rainfall in the tropics only"], "Thermal expansion of seawater and melting ice raise the sea level."),
    ("What causes most of the haze in Singapore in some years?", "forest and peatland fires in the region", ["volcanoes in Singapore", "power stations using coal in Singapore", "ozone from CFCs"], "The haze is mainly fine particulates (PM2.5)."),
    ("During haze, why are N95 masks recommended?", "They filter out most of the fine particulates.", ["They remove sulfur dioxide by chemical reaction.", "They add oxygen to the air.", "They block ultraviolet light."], "Particulates harm the lungs and heart."),
    ("Which strategy reduces global warming?", "using more solar energy instead of burning fossil fuels", ["cutting down rainforests", "using more CFCs", "burning more natural gas"], "Singapore installs solar panels on HDB rooftops."),
    ("Why are catalytic converters less effective when the car first starts?", "The catalyst works only when it is hot.", ["The fuel is too cold to burn.", "The catalyst is used up overnight.", "There is too much oxygen."], "Short journeys produce more pollution."),
    ("Why can carbon dioxide not be removed by a catalytic converter?", "It is the product of complete combustion and is not toxic, so converters make it rather than remove it.", ["Carbon dioxide does not form in engines.", "It is removed by the exhaust pipe.", "It reacts with nitrogen."], "Reducing CO₂ needs less fuel to be burned."),
    ("Which gas in car exhausts forms acid rain?", "nitrogen dioxide", ["carbon monoxide", "carbon dioxide", "water vapour"], "NO₂ dissolves in rain to form nitric acid."),
    ("Which equation shows how calcium carbonate removes sulfur dioxide?", "CaCO₃ + SO₂ → CaSO₃ + CO₂", ["CaCO₃ + CO₂ → CaO + SO₂", "CaO + CO₂ → CaCO₃", "CaCO₃ → CaO + CO₂"], "The calcium sulfite is oxidised to calcium sulfate (gypsum)."),
    ("Why is methane an important greenhouse gas even though there is less of it than carbon dioxide?", "Each molecule traps much more heat than a carbon dioxide molecule.", ["It is not a greenhouse gas.", "It destroys the ozone layer.", "It forms acid rain."], "Sources include rice fields, cattle and landfills."),
    ("A student says the ozone hole causes global warming. Why is this wrong?", "The ozone layer absorbs ultraviolet light; global warming is caused by greenhouse gases trapping infrared radiation.", ["The ozone hole cools the Earth.", "There is no ozone layer.", "Ozone is a fuel."], "They are two different problems."),
])


def main():
    sets = U.sets([
        ("Clean air", [(g_air, 8), (g_comp, 5), (POOL1, 4), (g_cyc, 3)]),
        ("Air pollutants", [(g_src, 7), (g_eff, 7), (uk_src, 4), (POOL1, 2)]),
        ("Acid rain and reducing pollution", [(g_cat, 3), (POOL1, 4), (g_psi, 5), (g_rain, 6), (g_src, 2)]),
        ("The carbon cycle and global warming", [(g_cyc, 3), (uk_ghg, 7), (uk_src, 3), (g_eff, 3), (POOL5, 4)]),
        ("Exam-style questions", [(POOL5, 6), (g_psi, 3), (g_rain, 2), (g_air, 4), (g_src, 2), (g_comp, 3)]),
    ])
    make_ol(LV, SUBJ, "maintaining-air-quality", SORT, "Maintaining Air Quality",
            "Describe the composition of clean, dry air; state the sources of air pollutants such as carbon monoxide, sulfur dioxide, oxides of nitrogen, unburnt "
            "hydrocarbons, methane and ozone and describe their effects; describe the formation of acid rain and ways of reducing it, including flue gas "
            "desulfurisation; describe how catalytic converters remove pollutants; describe the importance of the ozone layer and its depletion by CFCs; describe "
            "the carbon cycle and the effect of increased greenhouse gases on global warming (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Maintaining Air Quality", "Air quality",
            "Free Secondary 4 O-Level Chemistry worksheets on maintaining air quality: composition of air, air pollutants, acid rain, catalytic converters, the ozone "
            "layer, the carbon cycle, global warming and the haze. 100 questions with answers.",
            "Know each pollutant: source, effect, removal.", "Air: 78% nitrogen, 21% oxygen, 0.9% argon, 0.04% carbon dioxide.",
            "<p><b>Most air pollution comes from burning fuels.</b></p><ul>"
            "<li>Carbon monoxide: incomplete combustion, toxic. Sulfur dioxide: sulfur in fuels, acid rain. Oxides of nitrogen: N₂ + O₂ in hot engines, acid rain and smog.</li>"
            "<li>Catalytic converters turn CO, NO and hydrocarbons into CO₂, N₂ and H₂O. Flue gas desulfurisation uses CaCO₃ or CaO to remove SO₂.</li>"
            "<li>The ozone layer absorbs UV; CFCs destroy it. Carbon dioxide and methane trap infrared radiation and cause global warming.</li></ul>",
            [("How much oxygen is in 400 cm³ of air?", ["21% of 400 = 0.21 × 400"], "about 84 cm³"),
             ("2CO + 2NO → ? in a catalytic converter", ["C goes to CO₂, N goes to N₂"], "2CO₂ + N₂")],
            ["Saying air is mostly oxygen.", "Saying carbon dioxide causes acid rain (it is SO₂ and NO₂).", "Saying a catalytic converter removes carbon dioxide.",
             "Mixing up the ozone hole (UV) and global warming (infrared, greenhouse gases)."],
            [("What causes acid rain?", "Sulfur dioxide from burning fuels that contain sulfur and nitrogen dioxide from car engines dissolve in rainwater to form sulfuric and nitric acids."),
             ("What does a catalytic converter do?", "It uses hot platinum and rhodium catalysts to change carbon monoxide, oxides of nitrogen and unburnt hydrocarbons into carbon dioxide, nitrogen and water."),
             ("What is the difference between the ozone layer problem and global warming?", "CFCs destroy ozone, so more ultraviolet light reaches the Earth. Global warming is caused by greenhouse gases such as carbon dioxide and methane trapping infrared radiation.")],
            sets)


if __name__ == "__main__":
    main()
