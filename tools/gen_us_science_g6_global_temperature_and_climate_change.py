# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Global Temperature and Climate Change (MS-ESS3-5)
  python tools/gen_us_science_g6_global_temperature_and_climate_change.py
Ask questions to clarify evidence of the factors that have caused the rise in global temperatures over the past
century: the greenhouse effect, carbon dioxide and methane from burning fossil fuels, cutting forests and farming;
evidence from temperature records, CO2 measurements (Mauna Loa), ice cores, melting glaciers and sea ice, sea level rise.
Data (rounded): CO2 about 317 ppm (1960), 339 (1980), 370 (2000), 414 (2020); global temperature about 1 °C
warmer than in the late 1800s.
Wrong answers come from real mistakes: "the greenhouse effect is always bad", "climate change means every day
is hotter", "the ozone hole causes global warming".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(60111)
R = U.R
P = People(R)

CO2 = [(1960, 317), (1970, 326), (1980, 339), (1990, 354), (2000, 370), (2010, 390), (2020, 414)]


def g_co2():
    pts = sorted(R.sample(CO2, 4))
    who = P.next()[0]
    ch = bar_chart([str(y) for y, _ in pts], [v for _, v in pts], "CO₂ (ppm)", "bar graph of carbon dioxide in the air", ymax=450, step=50, w=320)
    k = R.choice(["trend", "diff", "why"])
    if k == "trend":
        return item(fig(ch) + "%s graphed carbon dioxide (CO₂) measured at Mauna Loa, Hawaii. What trend does it show?" % who, "CO₂ in the air has been increasing.",
                    ["CO₂ in the air has been decreasing.", "CO₂ has stayed the same.", "CO₂ went up and down randomly."], "Each later year has a higher value.")
    if k == "diff":
        a, b = pts[0], pts[-1]
        return item(fig(ch) + "Using %s's graph, how much did CO₂ increase from %d to %d?" % (who, a[0], b[0]), "%d ppm" % (b[1] - a[1]),
                    ["%d ppm" % b[1], "%d ppm" % a[1], "%d ppm" % (b[1] - pts[-2][1])], "%d − %d = %d ppm." % (b[1], a[1], b[1] - a[1]))
    return item(fig(ch) + "%s asks what is mainly causing the rise shown in the graph. What is the best answer?" % who, "people burning fossil fuels like coal, oil and gas",
                ["volcanoes erupting more every year", "the ozone hole", "more sunlight from a closer sun"], "Burning fossil fuels releases CO₂ that was stored underground for millions of years.")


CAUSES = [("burning coal in power plants", "adds carbon dioxide"), ("driving gasoline cars", "adds carbon dioxide"), ("cutting down and burning forests", "adds carbon dioxide and removes trees that take it in"),
          ("raising large herds of cattle", "adds methane"), ("landfills full of rotting garbage", "adds methane"), ("heating homes with natural gas", "adds carbon dioxide")]
FIX = ["using solar and wind energy instead of coal", "planting trees", "driving electric cars charged with clean energy", "insulating homes to use less heating",
       "biking or walking for short trips", "reducing food waste"]
NOFIX = ["burning more coal", "cutting down more forests", "leaving lights on all day", "driving more gasoline cars"]


def g_cause():
    a, b = R.choice(CAUSES)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s's class is studying causes of global warming. How does %s contribute?" % (who, a), "It " + b + ", a greenhouse gas, to the air.",
                    ["It makes a hole in the ozone layer that lets in heat.", "It makes Earth closer to the sun.", "It does not affect the air."],
                    "Greenhouse gases trap heat in the atmosphere.")
    return item("%s's class wants to reduce greenhouse gases. Which action would help?" % who, R.choice(FIX), R.sample(NOFIX, 3), "This reduces greenhouse gases or removes CO₂ from the air.")


EVID = ["Thermometer records show the average global temperature has risen about 1 °C since the late 1800s.", "Mountain glaciers around the world are shrinking.",
        "Arctic sea ice in summer covers less area than it did 40 years ago.", "Sea level has risen as ice melts and warm water expands.",
        "Air bubbles in ice cores show CO₂ is much higher now than in the past 800,000 years.", "Spring comes earlier and many plants bloom sooner."]
NOTEV = ["It was cold in my town last Tuesday.", "One summer day was very hot.", "My friend says winters used to be colder.", "A movie showed a big storm."]


def g_evid():
    who = P.next()[0]
    return item("%s is collecting evidence that Earth's climate is warming. Which is the strongest scientific evidence?" % who, R.choice(EVID), R.sample(NOTEV, 3),
                "Strong evidence comes from many measurements over many years, not one day or one opinion.")


def g_temp():
    yrs = [1900, 1940, 1980, 2000, 2020]
    vals = [-0.1, 0.1, 0.3, 0.6, 1.0]
    who = P.next()[0]
    rows = [[str(y), ("−" if v < 0 else "+") + "%.1f °C" % abs(v)] for y, v in zip(yrs, vals)]
    tab = table(["Year", "Global temperature compared with the 1880–1900 average"], rows)
    k = R.choice(["trend", "fast", "diff"])
    if k == "trend":
        return item(tab + "What does %s's data show?" % who, "Earth's average temperature has been rising.", ["Earth's average temperature has been falling.", "It has stayed the same.", "It only rose before 1940."],
                    "The values get higher over time.")
    if k == "fast":
        return item(tab + "In %s's data, when did the temperature rise fastest?" % who, "between 1980 and 2020", ["between 1900 and 1940", "between 1940 and 1980", "It rose at the same speed the whole time."],
                    "It rose 0.7 °C from 1980 to 2020, more than in any earlier 40 years.")
    return item(tab + "Using %s's data, how much warmer was 2020 than 1980?" % who, "0.7 °C", ["1.0 °C", "0.3 °C", "1.3 °C"], "1.0 − 0.3 = 0.7 °C.")


B1 = bank([
    ("What is the greenhouse effect?", "Gases in the atmosphere trap some of Earth's heat, keeping the planet warm enough for life.", ["The ozone layer lets heat in.", "Plants make the air hot.", "The sun gets closer in summer."],
     "Without it, Earth would be far colder. More greenhouse gases trap more heat."),
    ("Which gases are greenhouse gases?", "carbon dioxide, methane and water vapor", ["oxygen and nitrogen only", "helium and neon", "ozone only"], "These gases absorb heat."),
    ("Is the greenhouse effect always harmful?", "No. A natural greenhouse effect keeps Earth livable; extra greenhouse gases cause extra warming.", ["Yes, always.", "It does not exist.", "Only at night."],
     "The problem is the increase."),
    ("What human activity adds the most carbon dioxide to the air?", "burning fossil fuels", ["planting trees", "using solar panels", "recycling paper"], "Coal, oil and gas release CO₂ when burned."),
    ("How do forests help reduce carbon dioxide in the air?", "Trees take in carbon dioxide for photosynthesis.", ["Trees make carbon dioxide all day.", "Trees block sunlight.", "Trees cool the sun."],
     "Cutting forests removes this help."),
    ("Does global warming mean every day will be hotter?", "No. It means the long-term average is rising; there are still cold days.", ["Yes, every day.", "Yes, but only in winter.", "It means it never snows again."],
     "Climate is the long-term pattern."),
    ("Why is sea level rising?", "Melting land ice adds water, and warmer water expands.", ["Fish are making more water.", "Rivers are getting longer.", "The moon is closer."], "Both effects raise the ocean."),
    ("Which question would help scientists find what causes global warming?", "How has the amount of CO₂ in the air changed as temperatures rose?", ["What color is the sky?", "How many people like summer?", "What is the tallest mountain?"],
     "Good questions connect causes with evidence."),
])
B5 = bank([
    ("Ava wants to model the greenhouse effect. She puts thermometers in two jars in the sun, one covered with plastic wrap. Which will get warmer?", "the covered jar", ["the open jar", "They stay the same.", "Neither will warm."],
     "The cover traps heat, like greenhouse gases."),
    ("Leo reads that ice cores show CO₂ and temperature rose and fell together in the past. What does this suggest?", "CO₂ and temperature are connected.", ["CO₂ has no effect on climate.", "Ice makes CO₂.", "Temperature controls volcanoes."],
     "The pattern supports the link."),
    ("Mia hears a claim that global warming is caused by the hole in the ozone layer. Is this correct?", "No. The ozone hole and global warming are different problems.", ["Yes, exactly.", "Yes, the hole lets in heat.", "Only in Antarctica."],
     "Global warming is mainly caused by greenhouse gases."),
    ("A town switches its power plant from coal to wind. What should happen to its CO₂ emissions?", "They should go down.", ["They should go up.", "They stay the same.", "They double."],
     "Wind turbines do not burn fuel."),
    ("Why do scientists use temperature records from thousands of places around the world?", "to find the global average, not just local weather", ["to find the hottest town", "because one thermometer is enough", "to measure rainfall"],
     "Global trends need global data."),
])


def body():
    think = ("<p>Earth's average temperature has risen about <b>1 °C</b> since the late 1800s. Scientists ask questions and gather evidence to find out why.</p>"
             "<p><b>The greenhouse effect</b>: gases like carbon dioxide (CO₂) and methane trap heat. This keeps Earth livable, but <b>more</b> of these gases trap <b>more</b> heat.</p>"
             "<p>Main human causes: <b>burning fossil fuels</b> (coal, oil, gas), <b>cutting forests</b> and some farming. "
             "Evidence: rising temperature records, rising CO₂ measurements, shrinking glaciers and sea ice, and rising sea level.</p>")
    ex = [("CO₂ rose from 317 ppm (1960) to 414 ppm (2020). How much?", ["414 − 317"], "97 ppm"),
          ("Which helps: planting trees or burning more coal?", ["Trees take in CO₂."], "planting trees")]
    mist = ["Thinking the greenhouse effect is always bad. It keeps Earth warm; extra gases cause the problem.",
            "Thinking global warming means every day is hotter.",
            "Mixing up the ozone hole with global warming."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The greenhouse effect", B1 + [(g_cause, 6), (g_evid, 6)]),
        ("Causes and solutions", [(g_cause, 14), (g_evid, 6)]),
        ("Carbon dioxide data", [(g_co2, 14), (g_temp, 6)]),
        ("Temperature evidence", [(g_temp, 6), (g_evid, 8), (g_co2, 6)]),
        ("Asking questions about evidence", B5 + [g_co2, g_cause, g_evid, g_temp]),
    ])
    make("grade-6", "global-temperature-and-climate-change", 11, "MS-ESS3-5",
         "Ask questions to clarify evidence of the factors that have caused the rise in global temperatures over the past century.",
         "Global Temperature and Climate Change",
         "Grade 6 Climate Change Worksheets: Greenhouse Effect, CO₂ Data and Evidence",
         "Climate Change",
         "Free middle school science worksheets on global temperature and climate change (NGSS MS-ESS3-5): the greenhouse effect, carbon dioxide and methane, CO₂ and temperature data, and evidence such as melting ice. 100 practice questions with answers.",
         "Greenhouse gases are warming Earth.",
         "Burning fossil fuels adds carbon dioxide that traps heat. Temperature records, CO₂ data and melting ice are evidence.",
         body(),
         [("What is causing global temperatures to rise?", "Mainly greenhouse gases like carbon dioxide from burning fossil fuels, plus cutting forests, which trap more heat in the atmosphere."),
          ("What evidence shows Earth is warming?", "Temperature records, rising carbon dioxide measurements, shrinking glaciers and sea ice, and rising sea level."),
          ("Is the greenhouse effect bad?", "The natural greenhouse effect keeps Earth warm enough for life. Adding extra greenhouse gases causes extra warming.")],
         sets)


if __name__ == "__main__":
    main()
