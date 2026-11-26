# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Climate Change Data and Models (HS-ESS3-5)
  python tools/gen_us_science_ess_climate_change_data_and_models.py
Reading temperature records, finding a rate of change (°C per decade), forecasting with a rate, sea-level rise and
Arctic sea ice, evidence of impacts, and what climate models and emission scenarios tell us.
Wrong answers come from real mistakes: "one cold winter disproves warming", "rate = the last value",
"models give one exact number", "all scenarios end at the same temperature".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90416)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def sg(v):
    return ("+" + num(v, 2)) if v > 0 else num(v, 2)


@safe
def g_rate():
    who = P.next()[0]
    y0 = R.choice([1970, 1980, 1990])
    span = R.choice([20, 30, 40])
    rate = R.choice([0.15, 0.18, 0.2, 0.25, 0.3])
    a0 = R.choice([0.1, 0.2, 0.3, 0.4])
    a1 = round(a0 + rate * span / 10, 2)
    if y0 + span > 2020 or not once(("rt", y0, span, rate, a0)):
        return None
    region = R.choice(["global", "U.S.", "ocean surface"])
    if region in ("global", "ocean surface") and rate > 0.2:
        return None
    tab = table(["Year", "Temperature vs 1951–1980 average (°C)"], [[str(y0), sg(a0)], [str(y0 + span), sg(a1)]])
    g = "%s °C per decade" % num(rate, 2)
    return item(tab + "%s's table shows %s average temperatures. What is the rate of warming?" % (who, region), g,
                uniq(g, ["%s °C per decade" % num(a1, 2), "%s °C per decade" % num(a1 - a0, 2), "%s °C per decade" % num(rate / 10, 3), "%s °C per decade" % num(rate * 2, 2)]),
                "(%s − %s) ÷ %d decades = %s °C per decade." % (num(a1, 2), num(a0, 2), span // 10, num(rate, 2)))


@safe
def g_fc():
    who = P.next()[0]
    now = R.choice([1.0, 1.1, 1.2, 1.3])
    rate = R.choice([0.2, 0.25, 0.3, 0.4])
    yrs = R.choice([20, 30, 40, 50])
    fut = round(now + rate * yrs / 10, 2)
    if not once(("fc", now, rate, yrs)):
        return None
    g = "about %s °C" % num(fut, 2)
    return item("In %s's model, warming is now %s °C above the pre-industrial level and rising %s °C per decade. If this rate continues, about how warm will it be in %d years?" % (who, num(now, 2), num(rate, 2), yrs), g,
                uniq(g, ["about %s °C" % num(now + rate * yrs, 2), "about %s °C" % num(rate * yrs / 10, 2), "about %s °C" % num(now, 2), "about %s °C" % num(now + rate, 2)]),
                "%s + %s × %d decades = %s °C." % (num(now, 2), num(rate, 2), yrs // 10, num(fut, 2)))


@safe
def g_sea():
    who = P.next()[0]
    r = R.choice([3, 3.5, 4, 4.5, 5, 6, 8])
    yrs = R.choice([10, 20, 30, 50])
    k = R.choice(["rise", "rise", "rate"])
    if not once(("se", r, yrs, k)):
        return None
    cm = r * yrs / 10
    if k == "rise":
        g = "%s cm" % num(cm, 2)
        return item("%s reads that sea level is rising about %s mm per year. At this rate, how much will it rise in %d years?" % (who, num(r, 2), yrs), g,
                    uniq(g, ["%s cm" % num(r * yrs, 2), "%s cm" % num(cm / 10, 2), "%s cm" % num(r, 2), "%s cm" % num(cm * 2, 2)]), "%s mm × %d = %s mm = %s cm." % (num(r, 2), yrs, num(r * yrs, 2), num(cm, 2)))
    g = "%s mm per year" % num(r, 2)
    return item("A tide gauge in %s's town shows sea level rose %s cm in %d years. What is the average rate?" % (who, num(cm, 2), yrs), g,
                uniq(g, ["%s mm per year" % num(cm / yrs, 3), "%s mm per year" % num(r * 10, 2), "%s mm per year" % num(cm, 2), "%s mm per year" % num(yrs / cm, 2)]),
                "%s cm = %s mm; %s ÷ %d = %s mm per year." % (num(cm, 2), num(cm * 10, 2), num(cm * 10, 2), yrs, num(r, 2)))


@safe
def g_ice():
    who = P.next()[0]
    rows = [("1980", 7.7), ("1990", 6.2), ("2000", 6.3), ("2010", 4.9), ("2020", 3.9)]
    tab = table(["Year", "September Arctic sea ice (million km²)"], [[y, num(v, 2)] for y, v in rows])
    k = R.choice(["loss", "pct", "trend", "dip", "read"])
    if not once(("ic", k, who)) or not once(("ick", k), 2):
        return None
    if k == "loss":
        return item(tab + "From %s's table, how much September sea ice was lost from 1980 to 2020?" % who, "3.8 million km²", ["3.9 million km²", "7.7 million km²", "11.6 million km²"], "7.7 − 3.9 = 3.8.")
    if k == "pct":
        return item(tab + "From %s's table, by about what percent did September sea ice shrink from 1980 to 2020?" % who, "about 50%", ["about 4%", "about 200%", "about 10%"], "3.8 ÷ 7.7 ≈ 0.49.")
    if k == "trend":
        return item(tab + "What is the overall trend in %s's table?" % who, "Arctic sea ice is shrinking over time.", ["Arctic sea ice is growing.", "There is no change.", "It goes up every single decade."], "Look at the long-term pattern.")
    if k == "dip":
        return item(tab + "From 1990 to 2000 the ice did not shrink. What does %s's table show about this?" % who, "Short-term ups and downs happen, but the long-term trend is still down.",
                    ["Warming stopped forever.", "The data must be wrong.", "Sea ice is now growing."], "Trends are judged over decades.")
    return item(tab + "In %s's table, what was the September sea ice in 2010?" % who, "4.9 million km²", ["6.3 million km²", "3.9 million km²", "6.2 million km²"], "Read the row.")


IMP = [("Mountain glaciers worldwide are shrinking.", "rising temperatures"), ("Spring flowers bloom and birds migrate earlier than 50 years ago.", "warmer, earlier springs"),
       ("Corals turn white and die in hot summers.", "marine heat waves"), ("The ground in Alaska sinks as frozen soil melts.", "permafrost thaw"),
       ("Some plants and animals are moving uphill and toward the poles.", "shifting climate zones"), ("Coastal towns flood more often at high tide.", "sea-level rise"),
       ("Shells of sea snails grow thinner in more acidic water.", "ocean acidification from CO₂"), ("Fire seasons in the western U.S. are longer.", "hotter, drier summers")]


@safe
def g_imp():
    s, c = R.choice(IMP)
    k = R.random() < 0.6
    if not once(("im", s, k)):
        return None
    if k:
        return item("%s Which climate change is this evidence of?" % s, c, R.sample([x[1] for x in IMP if x[1] != c], 3), "Many independent kinds of evidence point the same way.")
    return item("Which observation is evidence of %s?" % c, s, R.sample([x[0] for x in IMP if x[0] != s], 3), "Match the evidence to the change.")


SCEN = [("Which emissions scenario leads to the least warming by 2100?", "cutting emissions quickly to near zero", ["emissions keep rising fast", "emissions stay at today's level", "emissions double"]),
        ("In a high-emissions scenario, about how much warmer could Earth be by 2100 than before 1850?", "about 4 to 5 °C", ["about 0.1 °C", "about 40 °C", "no warmer at all"]),
        ("In a low-emissions scenario, about how much warmer could Earth be by 2100 than before 1850?", "about 1.5 to 2 °C", ["about 10 °C", "about 0 °C", "about 6 °C"]),
        ("Why do climate models give a range instead of one exact number?", "Future emissions and some processes, like clouds, are uncertain.", ["Models are random guesses.", "Scientists disagree on whether CO₂ traps heat.", "Computers cannot add."]),
        ("How do scientists test a climate model?", "They check whether it can reproduce past climate that was already measured.", ["They wait 100 years.", "They only ask other models.", "They do not test models."]),
        ("Why do models run several scenarios?", "Future warming depends on choices people make about emissions.", ["To confuse people.", "Because the Sun will change.", "Because only one scenario is possible."]),
        ("Two models give 2.6 °C and 3.1 °C for the same scenario. What should a forecaster report?", "a likely range, such as about 2.5 to 3 °C", ["only the lower number", "that warming is impossible", "the average of 3.1 and 0"]),
        ("Which factor is NOT a main input to a global climate model?", "the number of cars sold in one city last week", ["greenhouse gas levels", "energy from the Sun", "aerosols from volcanoes"]),
        ("Why will sea level keep rising for centuries even if emissions stop?", "The deep ocean keeps warming and ice sheets keep melting slowly.", ["Rivers will stop flowing.", "The Moon will pull more water.", "It will not keep rising."]),
        ("What do regional climate models add to global models?", "more detail about changes in a smaller area, like one state", ["data about other planets", "weather for tomorrow only", "nothing at all"])]


@safe
def g_scen():
    q, a, w = R.choice(SCEN)
    if not once(("sc", q)):
        return None
    return item(q, a, w, "Climate models forecast ranges of outcomes under different emissions scenarios.")


B1 = bank([
    ("What does a temperature anomaly mean?", "how much warmer or colder a temperature is than a long-term average", ["the hottest temperature ever", "a broken thermometer", "the temperature at night"], "Compared with a baseline."),
    ("About how much has Earth warmed since the late 1800s?", "about 1.2 °C", ["about 12 °C", "about 0.01 °C", "it has cooled"], "Global average."),
    ("A city has a very cold winter. Does this disprove global warming?", "No. Climate is about long-term global averages, not one season in one place.", ["Yes, warming has stopped.", "Yes, the planet is cooling.", "Yes, models are wrong."], "Weather vs climate."),
    ("Which data do scientists use to track climate change?", "thermometer records, satellites, ice cores, tide gauges and sea ice maps", ["only one weather station", "only newspapers", "only animal surveys"], "Many data sources."),
    ("What is the main cause of warming since the mid-1900s?", "greenhouse gases from burning fossil fuels and cutting forests", ["changes in the Sun", "volcanoes", "Earth moving closer to the Sun"], "Human causes."),
    ("Why is sea level rising?", "Ocean water expands as it warms, and melting land ice adds water.", ["Fish are getting bigger.", "It rains more.", "The seafloor is sinking everywhere."], "Two causes."),
    ("What is a forecast in climate science?", "an evidence-based estimate of future change, often given as a range", ["an exact prediction of tomorrow's weather", "a guess with no data", "a story"], "Range."),
    ("Why does melting sea ice not raise sea level much, but melting Greenland ice does?", "Sea ice already floats in the ocean; Greenland's ice is on land.", ["Sea ice is saltier.", "Greenland ice is warmer.", "They both raise it equally."], "Land vs sea ice."),
])
B5 = bank([
    ("A student says, \"The warming rate is the last value in the table.\" What is the mistake?", "A rate is the change divided by the time, not one value.", ["There is no mistake.", "A rate is the first value.", "A rate is the sum of the values."], "Change ÷ time."),
    ("Why is a 30-year record better than a 5-year record for finding a climate trend?", "Short records can be hidden by natural ups and downs.", ["5 years is always better.", "Climate changes every day.", "Older data are wrong."], "Long baselines."),
    ("How can people use climate forecasts?", "to plan for heat, floods and water supply, such as raising roads or saving water", ["to stop the Sun", "to pick lottery numbers", "they cannot use them"], "Planning."),
    ("A forecast says a coastal city will see 30 to 60 cm of sea-level rise by 2100. What does the range show?", "uncertainty about future emissions and how fast ice melts", ["the forecast is useless", "sea level will fall", "an exact answer"], "Uncertainty."),
    ("Which evidence would most strengthen a claim that a region is warming?", "several independent records (temperature, ice, plant timing) showing the same trend", ["one hot day", "one person's memory", "a single photo"], "Multiple lines of evidence."),
])


def body():
    think = ("<p><b>Use data to find the rate, then forecast with a range.</b></p>"
             "<ul><li>Rate of change = (later value − earlier value) ÷ time. Climate rates are often given per decade.</li>"
             "<li>Forecast: today's value + rate × time. Models give ranges because future emissions are uncertain.</li>"
             "<li>Evidence: rising temperatures, shrinking glaciers and Arctic sea ice, rising seas, earlier springs, coral bleaching.</li></ul>")
    ex = [("+0.2 °C in 1980, +0.8 °C in 2010. Rate?", ["0.6 ÷ 3 decades"], "0.2 °C per decade"),
          ("Sea level rises 4 mm/year. Rise in 50 years?", ["4 × 50 = 200 mm"], "20 cm")]
    mist = ["Using one cold winter to judge the climate.", "Using the last value as the rate.", "Thinking models give one exact number."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Climate data", B1 + [(g_imp, 8), (g_scen, 4)]),
        ("Rates of change", [(g_rate, 16), (g_sea, 4)]),
        ("Forecasting", [(g_fc, 14), (g_rate, 6)]),
        ("Sea level and ice", [(g_sea, 12), (g_ice, 8)]),
        ("Models and scenarios", B5 + [(g_scen, 6), (g_fc, 5), (g_imp, 4)]),
    ])
    make("earth-and-space-science", "climate-change-data-and-models", 16, "HS-ESS3-5",
         "Analyze geoscience data and the results from global climate models to make an evidence-based forecast of the current rate of global or regional climate change and associated future impacts to Earth systems.",
         "Climate Change Data and Models",
         "Climate Change Worksheets: Warming Rates, Sea Level, Sea Ice and Climate Models (Earth Science)",
         "Climate Data and Models",
         "Free high school Earth and space science worksheets on climate change data and models (NGSS HS-ESS3-5): warming rates, forecasts, sea-level rise, Arctic sea ice, evidence of impacts and emissions scenarios. 100 questions with answers.",
         "Find the rate, then forecast.",
         "Temperature, ice and sea-level data show the trend; models give a range.",
         body(),
         [("How do you find the rate of climate change from data?", "Subtract the earlier value from the later value and divide by the time between them. For temperature, the rate is often given in °C per decade."),
          ("Why do climate forecasts give a range?", "Future emissions depend on human choices, and some processes such as clouds and ice-sheet melting are not known exactly."),
          ("What evidence shows the climate is changing?", "Rising global temperatures, shrinking glaciers and Arctic sea ice, rising sea level, earlier springs and more frequent heat waves all point to warming.")],
         sets)


if __name__ == "__main__":
    main()
