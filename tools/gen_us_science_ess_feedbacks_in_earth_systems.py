# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Feedbacks in Earth Systems (HS-ESS2-2)
  python tools/gen_us_science_ess_feedbacks_in_earth_systems.py
Analyze geoscience data to make the claim that one change to Earth's surface can create feedbacks that cause changes
to other Earth systems.
Earth's spheres, positive (amplifying) and negative (stabilizing) feedback loops, albedo and absorbed energy,
and data on sea ice, glaciers, dams and deforestation.
Wrong answers come from real mistakes: "positive feedback means good", "a change in one sphere stays in that sphere",
"dark surfaces reflect more sunlight", "negative feedback makes things worse".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90409)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


FB = [("Warming melts sea ice, exposing dark ocean that absorbs more sunlight, which causes more warming.", "positive"),
      ("Warming thaws permafrost, which releases methane, which causes more warming.", "positive"),
      ("Warmer air holds more water vapor, a greenhouse gas, which causes more warming.", "positive"),
      ("Drought kills plants, so less water evaporates from leaves, so less rain falls, making the drought worse.", "positive"),
      ("Wildfires burn forests, releasing CO₂ that warms the climate and dries more forests.", "positive"),
      ("More CO₂ helps some plants grow faster, and they take more CO₂ out of the air.", "negative"),
      ("Warmer oceans evaporate more water, forming more low clouds that reflect sunlight and cool the surface.", "negative"),
      ("More rainfall speeds up rock weathering, which removes CO₂ from the air over long times.", "negative"),
      ("A hotter Earth gives off more infrared energy to space, which cools it down.", "negative"),
      ("More prey lets predators increase, and the predators then reduce the prey.", "negative")]


@safe
def g_fb():
    s, t = R.choice(FB)
    if not once(("fb", s)):
        return None
    a = "a positive (amplifying) feedback" if t == "positive" else "a negative (stabilizing) feedback"
    return item("%s What kind of feedback is this?" % s, a, ["a negative (stabilizing) feedback" if t == "positive" else "a positive (amplifying) feedback", "no feedback at all", "a feedback that only affects rocks"],
                "Positive feedback makes the change bigger; negative feedback makes it smaller.")


SYS = [("A volcano erupts and puts ash and gases high into the sky.", "the atmosphere (cooler temperatures for a year or two)"),
       ("A dam is built across a river.", "the hydrosphere and biosphere (a lake forms, fish migration is blocked, sediment is trapped)"),
       ("A large forest is cut down.", "the atmosphere and geosphere (more CO₂, more soil erosion)"),
       ("Glaciers melt quickly in a warm period.", "the hydrosphere (sea level rises)"),
       ("Coral reefs die from warm water.", "the geosphere and hydrosphere (coasts erode faster without reefs)"),
       ("A city paves over a large area.", "the hydrosphere (more runoff and flooding)"),
       ("Beavers build dams in a valley.", "the hydrosphere (ponds and wetlands form)"),
       ("Heavy rain falls on bare hills.", "the geosphere (landslides and soil erosion)")]


@safe
def g_sys():
    s, a = R.choice(SYS)
    if not once(("sy", s)):
        return None
    return item("%s Which other Earth system is most directly changed, and how?" % s, a, R.sample([x[1] for x in SYS if x[1] != a], 3), "A change in one sphere spreads to others.")


ALB = [("fresh snow", 85), ("sea ice", 60), ("desert sand", 40), ("grassland", 25), ("forest", 15), ("open ocean", 6), ("asphalt", 5), ("cropland", 20)]


@safe
def g_alb():
    k = R.choice(["abs", "cmp", "e"])
    if k == "cmp":
        a, b = R.sample(ALB, 2)
        if not once(("ac", tuple(sorted((a[0], b[0]))))):
            return None
        more = a if a[1] < b[1] else b
        first, second = sorted([a, b])
        return item("Which absorbs more sunlight: %s (albedo %d%%) or %s (albedo %d%%)?" % (first[0], first[1], second[0], second[1]), more[0], [b[0] if more is a else a[0], "They absorb the same.", "Neither absorbs sunlight."],
                    "Lower albedo → less reflected → more absorbed.")
    s, al = R.choice(ALB)
    if k == "abs":
        if not once(("ab", s)):
            return None
        g = "%d%%" % (100 - al)
        return item("%s reflects %d%% of sunlight (albedo %d%%). What percent does it absorb?" % (s[0].upper() + s[1:], al, al), g, uniq(g, ["%d%%" % al, "100%", "0%", "%d%%" % (100 - al // 2)]), "100 − %d = %d%%." % (al, 100 - al))
    I = R.choice([200, 300, 400, 500, 1000])
    if not once(("ae", s, I)):
        return None
    E = I * (100 - al) / 100
    g = "%s W/m²" % num(E, 1)
    return item("Sunlight of %d W/m² falls on %s (albedo %d%%). How much energy is absorbed per square meter?" % (I, s, al), g,
                uniq(g, ["%s W/m²" % num(I * al / 100, 1), "%d W/m²" % I, "%s W/m²" % num(I - al, 1), "%s W/m²" % num(E / 2, 1)]), "%d × (1 − %s) = %s W/m²." % (I, num(al / 100, 2), num(E, 1)))


@safe
def g_data():
    who = P.next()[0]
    yrs = [1980, 1990, 2000, 2010, 2020]
    base = R.choice([7.5, 7.8, 8.0])
    drops = [0] + sorted(R.sample([0.3, 0.5, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.5], 4))
    vals = [round(base - d, 1) for d in drops]
    k = R.choice(["change", "trend", "fb"])
    if len(set(vals)) < 5 or not once(("dt", base, tuple(vals), k)) or (k != "change" and not once(("dk", k), 3)):
        return None
    tab = table(["Year", "September Arctic sea-ice extent (million km²)"], [[str(y), num(v, 1)] for y, v in zip(yrs, vals)])
    if k == "change":
        g = "%s million km²" % num(vals[0] - vals[-1], 1)
        return item(tab + "By how much did sea-ice extent shrink from 1980 to 2020 in %s's data?" % who, g,
                    uniq(g, ["%s million km²" % num(vals[-1], 1), "%s million km²" % num(vals[0], 1), "%s million km²" % num(vals[0] + vals[-1], 1), "%s million km²" % num(vals[1] - vals[-1], 1)]),
                    "%s − %s = %s." % (num(vals[0], 1), num(vals[-1], 1), num(vals[0] - vals[-1], 1)))
    if k == "trend":
        return item(tab + "What trend do %s's data show?" % who, "Arctic sea ice is shrinking over time.", ["Arctic sea ice is growing.", "Sea ice is unchanged.", "Sea ice changes randomly with no trend."], "Each decade is lower.")
    return item(tab + "How could the change in %s's data speed up Arctic warming?" % who, "Less ice means more dark ocean absorbs sunlight, causing more melting (a positive feedback).",
                ["Less ice reflects more sunlight, cooling the Arctic.", "Sea ice has no effect on temperature.", "Melting ice adds energy to space."], "Ice–albedo feedback.")


B1 = bank([
    ("What are Earth's main systems (spheres)?", "geosphere, hydrosphere, atmosphere, biosphere and cryosphere", ["only land and water", "the Sun and the Moon", "the crust and the core"], "Interacting systems."),
    ("What is a feedback loop?", "a change that causes effects that then increase or decrease the original change", ["a one-time event", "a type of rock", "a measurement tool"], "Loops."),
    ("Does 'positive feedback' mean the result is good?", "No. It means the change gets bigger.", ["Yes, always.", "It means the change stops.", "It means nothing happens."], "Amplifying."),
    ("What does a negative feedback do?", "It reduces the change and helps keep a system stable.", ["It makes the change grow.", "It destroys the system.", "It has no effect."], "Stabilizing."),
    ("What is albedo?", "the fraction of sunlight a surface reflects", ["the temperature of a surface", "the color of the sky", "the amount of rain"], "Snow is high, ocean is low."),
    ("Why does melting snow speed up warming?", "Darker ground underneath absorbs more sunlight.", ["Snow absorbs more light.", "Melted snow reflects more.", "Snow has no effect."], "Lower albedo."),
    ("How can cutting a forest change the atmosphere?", "Fewer trees take in CO₂, and burning or decay releases more CO₂.", ["It makes more oxygen.", "It has no effect on air.", "It cools the whole planet."], "Biosphere → atmosphere."),
    ("Why did global temperatures drop after the 1991 Mount Pinatubo eruption?", "Sulfur gases made particles that reflected sunlight.", ["The volcano absorbed heat.", "Lava cooled the oceans.", "Ash added water vapor."], "Geosphere → atmosphere."),
])
B5 = bank([
    ("Scientists find that Arctic warming is about 3 times faster than the global average. Which feedback helps explain this?", "the ice–albedo feedback", ["a negative cloud feedback", "rock weathering", "predator–prey cycles"], "Amplification."),
    ("A river is dammed. Downstream beaches shrink. What is the best explanation?", "The dam traps sediment that used to rebuild the beaches.", ["The dam adds sand.", "Beaches always shrink.", "Fish eat the sand."], "Hydrosphere → geosphere."),
    ("Why do climate scientists study clouds so carefully?", "Clouds can cause either warming or cooling feedbacks.", ["Clouds have no effect.", "Clouds only cause rain.", "Clouds are part of the geosphere."], "Uncertain feedback."),
    ("Which data would best support a claim that deforestation increases local flooding?", "streamflow measurements before and after forest removal", ["photos of trees", "the price of wood", "the number of birds only"], "Before and after data."),
    ("Why are positive feedbacks a concern in climate change?", "They can make warming faster and larger than the first change.", ["They always stop warming.", "They are rare and harmless.", "They only happen on Mars."], "Tipping points."),
])


def body():
    think = ("<p><b>A change in one Earth system can set off feedbacks in others.</b></p>"
             "<ul><li>Systems: geosphere, hydrosphere, atmosphere, biosphere, cryosphere.</li>"
             "<li>Positive feedback amplifies a change (melting ice → darker surface → more warming). Negative feedback reduces it.</li>"
             "<li>Albedo: fraction of sunlight reflected. Absorbed = incoming × (1 − albedo).</li></ul>")
    ex = [("Albedo 6%, sunlight 400 W/m². Absorbed?", ["400 × 0.94"], "376 W/m²"),
          ("Permafrost thaws, releasing methane, more warming. Type?", ["The change grows"], "positive feedback")]
    mist = ["Thinking positive feedback means a good result.", "Thinking a change stays in one sphere.", "Thinking dark surfaces reflect more sunlight."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Earth's systems", B1 + [(g_sys, 5), (g_fb, 5), (g_alb, 2)]),
        ("Feedback loops", [(g_fb, 4), (g_sys, 2), (g_alb, 14)]),
        ("Albedo", [(g_alb, 14), (g_data, 6)]),
        ("Sea-ice data", [(g_data, 12), (g_alb, 8)]),
        ("Analyzing feedbacks", B5 + [(g_data, 7), (g_alb, 8)]),
    ])
    make("earth-and-space-science", "feedbacks-in-earth-systems", 9, "HS-ESS2-2",
         "Analyze geoscience data to make the claim that one change to Earth's surface can create feedbacks that cause changes to other Earth systems.",
         "Feedbacks in Earth Systems",
         "Earth Systems Worksheets: Feedback Loops, Albedo and Sea-Ice Data (High School Earth Science)",
         "Earth System Feedbacks",
         "Free high school Earth and space science worksheets on feedbacks in Earth systems (NGSS HS-ESS2-2): Earth's spheres, positive and negative feedback, albedo and sea-ice data. 100 questions with answers.",
         "One change can trigger many more.",
         "Positive feedbacks amplify a change; negative feedbacks dampen it.",
         body(),
         [("What is the difference between positive and negative feedback?", "Positive feedback makes a change grow larger. Negative feedback makes a change smaller and helps keep a system stable."),
          ("What is the ice–albedo feedback?", "Warming melts ice, exposing darker land or ocean that absorbs more sunlight, which causes more warming and more melting."),
          ("How can one change affect other Earth systems?", "For example, a volcano (geosphere) adds particles to the atmosphere that cool the climate, which can affect ice, oceans and living things.")],
         sets)


if __name__ == "__main__":
    main()
