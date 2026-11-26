# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Climate and Energy Flow (HS-ESS2-4)
  python tools/gen_us_science_ess_climate_and_energy_flow.py
Use a model to describe how variations in the flow of energy into and out of Earth's systems result in changes in
climate.
Earth's energy budget (incoming, reflected, absorbed, outgoing), what warms and cools the climate, the time scales of
causes (eruptions, solar cycles, ocean circulation, Milankovitch cycles, plate tectonics), and ice-core data.
Wrong answers come from real mistakes: "weather and climate are the same", "ice ages are caused by volcanoes alone",
"greenhouse gases block incoming sunlight", "an energy imbalance has no effect".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90410)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


CAUSE = [("a large volcanic eruption", "1 to 3 years"), ("the 11-year solar cycle", "about a decade"), ("El Niño and La Niña", "a few years"),
         ("changes in the tilt of Earth's axis", "about 41,000 years"), ("changes in the shape of Earth's orbit", "about 100,000 years"),
         ("the wobble (precession) of Earth's axis", "about 23,000 years"), ("continents moving and mountains rising", "millions of years"),
         ("the rise in greenhouse gases from burning fossil fuels", "decades to centuries")]


@safe
def g_scale():
    c, t = R.choice(CAUSE)
    if not once(("sc", c)):
        return None
    return item("Over about what time scale does %s change Earth's climate?" % c, t, R.sample(sorted({x[1] for x in CAUSE if x[1] != t}), 3), "Different causes act on very different time scales.")


EFF = [("More CO₂ and methane in the atmosphere", "warming"), ("A large eruption puts sulfur particles in the stratosphere", "cooling"), ("The Sun's output drops slightly for decades", "cooling"),
       ("More snow and ice cover the land", "cooling"), ("Large areas of ice melt, exposing dark ocean", "warming"), ("Earth's orbit brings more summer sunlight to the far north", "warming"),
       ("Less summer sunlight reaches high northern latitudes", "cooling"), ("Ocean currents carry less warm water north", "cooling"), ("Deforestation releases stored carbon", "warming"),
       ("More low, bright clouds form over the oceans", "cooling")]


@safe
def g_eff():
    s, t = R.choice(EFF)
    if not once(("ef", s)):
        return None
    return item("%s. Does this tend to warm or cool the climate?" % s, t, ["cooling" if t == "warming" else "warming", "no change at all", "it only changes weather for one day"],
                "More energy kept in → warming; less energy in or more reflected → cooling.")


@safe
def g_budget():
    who = P.next()[0]
    inc = 340
    refl = R.randint(90, 110)
    absb = inc - refl
    out = absb - R.choice([0, 0.5, 1, 2, -1])
    k = R.choice(["abs", "bal", "pct"])
    if not once(("bg", refl, out if k == "bal" else 0, k)):
        return None
    if k == "abs":
        g = "%s W/m²" % num(absb)
        return item("In %s's model, %d W/m² of sunlight reaches Earth and %d W/m² is reflected. How much is absorbed?" % (who, inc, refl), g,
                    uniq(g, ["%s W/m²" % num(inc + refl), "%s W/m²" % num(refl), "%s W/m²" % num(inc), "%s W/m²" % num(absb / 2)]), "%d − %d = %d W/m²." % (inc, refl, absb))
    if k == "pct":
        g = "about %d%%" % round(100 * refl / inc)
        return item("Earth reflects %d W/m² of the %d W/m² of incoming sunlight. What is Earth's albedo?" % (refl, inc), g,
                    uniq(g, ["about %d%%" % round(100 * absb / inc), "about %d%%" % refl, "about 100%", "about %d%%" % round(refl / 10)]), "%d ÷ %d ≈ %s." % (refl, inc, g))
    diff = absb - out
    if diff > 0:
        g = "Earth gains energy and warms."
    elif diff < 0:
        g = "Earth loses energy and cools."
    else:
        g = "Earth's temperature stays steady."
    return item("Earth absorbs %s W/m² and gives off %s W/m² of infrared to space. What happens?" % (num(absb), num(out, 1)), g,
                uniq(g, ["Earth gains energy and warms.", "Earth loses energy and cools.", "Earth's temperature stays steady.", "The Sun gets hotter."]), "Compare energy in and out.")


@safe
def g_ice():
    who = P.next()[0]
    times = [400, 300, 200, 130, 20, 0]
    co2 = [280, 190, 245, 285, 185, 280]
    dt = [2, -8, -3, 2, -8, 0]
    j = R.randrange(5)
    k = R.choice(["read", "read", "temp", "rel", "low", "now"])
    if not once(("ic", j if k in ("read", "temp") else 0, k)) or (k not in ("read", "temp") and not once(("ik", k), 3)):
        return None
    tab = table(["Thousand years ago", "CO₂ (ppm)", "Temperature vs today (°C)"], [[str(t), str(c), ("%+d" % d).replace("-", "−")] for t, c, d in zip(times, co2, dt)])
    if k == "read":
        g = "%d ppm" % co2[j]
        return item(tab + "From %s's ice-core table, what was the CO₂ level %s thousand years ago?" % (who, num(times[j])), g, uniq(g, ["%d ppm" % c for c in co2] + ["420 ppm"]), "Read the row.")
    if k == "temp":
        g = ("%+d °C" % dt[j]).replace("-", "−")
        return item(tab + "From %s's table, how did the temperature %s thousand years ago compare with today?" % (who, num(times[j])), g, uniq(g, [("%+d °C" % d).replace("-", "−") for d in dt] + ["+5 °C"]), "Read the row.")
    if k == "rel":
        return item(tab + "What relationship do %s's ice-core data show?" % who, "Higher CO₂ goes with warmer temperatures.", ["Higher CO₂ goes with colder temperatures.", "CO₂ and temperature are unrelated.", "CO₂ never changed."],
                    "CO₂ and temperature rise and fall together.")
    if k == "low":
        return item(tab + "When was it coldest in %s's data?" % who, "20 thousand years ago (an ice age)", ["130 thousand years ago", "today", "400 thousand years ago"], "−8 °C with low CO₂.")
    return item(tab + "Today CO₂ is about 420 ppm. How does this compare with %s's ice-core record?" % who, "It is far higher than any level in the record.", ["It is lower than during ice ages.", "It is the same as 20,000 years ago.", "It is about average."],
                "The ice-core maximum here is about 285 ppm.")


B1 = bank([
    ("What is the difference between weather and climate?", "Weather is day-to-day conditions; climate is the long-term average pattern.", ["They are the same.", "Climate changes hourly.", "Weather lasts for centuries."], "Time scale."),
    ("What sets Earth's climate in the long run?", "the balance between energy coming in from the Sun and energy going out to space", ["the Moon's phases", "earthquakes", "the number of people"], "Energy budget."),
    ("How do greenhouse gases warm Earth?", "They absorb infrared energy given off by Earth and send some back down.", ["They block incoming sunlight.", "They make the Sun brighter.", "They reflect sunlight."], "Outgoing energy trapped."),
    ("What are Milankovitch cycles?", "slow changes in Earth's orbit and tilt that change how sunlight is spread over the planet", ["daily changes in weather", "solar flares", "ocean tides"], "Ice-age pacemaker."),
    ("Why did a big volcanic eruption cool the climate for only a few years?", "The reflective particles fell out of the air within a few years.", ["Volcanoes cool Earth forever.", "Lava froze the oceans.", "It stopped the Sun."], "Short-term cause."),
    ("How does the ocean affect climate?", "It stores huge amounts of heat and moves it around the globe with currents.", ["It has no effect.", "It cools Earth only at night.", "It only affects fish."], "Heat capacity."),
    ("What do ice cores record?", "past air (CO₂) and temperatures from bubbles and isotopes in old ice", ["future weather", "earthquake strength", "the age of the Sun"], "Climate archive."),
    ("If Earth absorbs more energy than it gives off, what happens?", "It warms until a new balance is reached.", ["It cools.", "Nothing happens.", "The Sun dims."], "Imbalance."),
])
B5 = bank([
    ("Ice ages came and went about every 100,000 years for the last million years. Which cause fits this timing best?", "changes in the shape of Earth's orbit", ["volcanic eruptions", "the 11-year solar cycle", "El Niño"], "Match time scales."),
    ("Why do climate models include greenhouse gases, the Sun, volcanoes and aerosols?", "Each changes the flow of energy in or out, and models must include them all to match observations.", ["Only one cause matters.", "To make models slower.", "To predict tomorrow's weather."], "Model inputs."),
    ("During the last ice age, sea level was about 120 m lower. Why?", "Much of the water was locked up in huge ice sheets on land.", ["The oceans evaporated into space.", "The ocean floor rose.", "It rained less."], "Water stored as ice."),
    ("Why does a small change in Earth's tilt matter for ice ages?", "It changes how much summer sunlight reaches high latitudes, so ice can melt or build up.", ["It changes the Sun's color.", "It changes the length of a day greatly.", "It moves continents."], "Seasonal energy."),
    ("Satellites show the Sun's output has not risen since the 1980s while Earth warmed. What does this suggest?", "The recent warming is not caused by the Sun.", ["The Sun caused the warming.", "Satellites are wrong.", "Earth did not warm."], "Evaluate causes."),
])


def body():
    think = ("<p><b>Climate changes when the flow of energy in and out of Earth changes.</b></p>"
             "<ul><li>Absorbed sunlight = incoming − reflected. If more energy comes in than goes out, Earth warms.</li>"
             "<li>Warming: more greenhouse gases, less ice. Cooling: volcanic particles, less sunlight, more snow and ice.</li>"
             "<li>Causes act on different time scales: eruptions (years), solar and ocean cycles (years to decades), orbit changes (tens of thousands of years), moving continents (millions).</li></ul>")
    ex = [("340 W/m² in, 100 reflected. Absorbed?", ["340 − 100"], "240 W/m²"),
          ("A big eruption adds sulfur particles. Effect?", ["Reflects sunlight"], "cooling for 1–3 years")]
    mist = ["Mixing up weather and climate.", "Thinking greenhouse gases block incoming sunlight.", "Thinking one cause explains every climate change."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Weather, climate and energy", B1 + [(g_eff, 7), (g_scale, 5)]),
        ("Warming and cooling", [(g_eff, 2), (g_scale, 2), (g_budget, 16)]),
        ("Earth's energy budget", [(g_budget, 14), (g_ice, 6)]),
        ("Ice-core evidence", [(g_ice, 8), (g_budget, 12)]),
        ("Explaining climate change", B5 + [(g_budget, 10), (g_ice, 5)]),
    ])
    make("earth-and-space-science", "climate-and-energy-flow", 10, "HS-ESS2-4",
         "Use a model to describe how variations in the flow of energy into and out of Earth's systems result in changes in climate.",
         "Climate and Energy Flow",
         "Climate Worksheets: Energy Budget, Milankovitch Cycles and Ice Cores (Earth Science)",
         "Climate and Energy",
         "Free high school Earth and space science worksheets on climate and energy flow (NGSS HS-ESS2-4): Earth's energy budget, warming and cooling causes, time scales and ice-core data. 100 questions with answers.",
         "Energy in vs. energy out sets climate.",
         "Greenhouse gases, the Sun, orbits, volcanoes and ice all change the energy balance.",
         body(),
         [("What controls Earth's climate?", "The balance between incoming sunlight that Earth absorbs and the infrared energy Earth gives off to space."),
          ("What causes ice ages?", "Mainly slow changes in Earth's orbit and tilt (Milankovitch cycles), amplified by feedbacks from ice and greenhouse gases."),
          ("How are weather and climate different?", "Weather is the short-term state of the atmosphere; climate is the average pattern over 30 years or more.")],
         sets)


if __name__ == "__main__":
    main()
