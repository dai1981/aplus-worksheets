# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Forecasting Natural Hazards (MS-ESS3-2)
  python tools/gen_us_science_g8_forecasting_natural_hazards.py
Analyze and interpret data on natural hazards to forecast future catastrophic events and inform the development of
technologies to mitigate their effects. Patterns in where and how often hazards happen (plate boundaries, hurricane
season), warning signs (volcano gases and swelling, rising rivers), magnitude scale (10× shaking, about 32× energy per step),
recurrence intervals, travel-time calculations for tsunamis and storms, and mitigation technologies.
Wrong answers come from real mistakes: "earthquakes can be predicted to the exact day", "a 100-year flood happens only
once every 100 years", "magnitude 6 is twice magnitude 3", "hazards are random everywhere".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80122)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def g_mag():
    who = P.next()[0]
    a = R.choice([3, 4, 5, 6])
    d = R.choice([1, 2, 3])
    b = a + d
    k = R.choice(["shake", "energy"])
    if b > 9 or not once((a, b, k)):
        return None
    if k == "shake":
        f = 10 ** d
        return item("%s compares a magnitude %d earthquake with a magnitude %d earthquake. Each step on the scale means about 10 times more ground shaking. How many times more shaking does the magnitude %d quake cause?" % (who, b, a, b),
                    "about %s times" % comma(f), ["about %d times" % d, "about %d times" % (10 * d) if 10 * d != f else "about %d times" % (d + 1), "about %d times" % (b - a + 1) if b - a + 1 != d else "about 2 times"],
                    "10 × " * (d - 1) + "10 = %s." % comma(f))
    f = 32 ** d
    return item("Each magnitude step releases about 32 times more energy. About how many times more energy does a magnitude %d earthquake release than a magnitude %d earthquake, according to %s's notes?" % (b, a, who),
                "about %s times" % comma(f), ["about %d times" % (32 * d) if d > 1 else "about 10 times", "about %d times" % d if d > 1 else "about 2 times", "about %s times" % comma(10 ** d) if d > 1 else "about 64 times"],
                "32 multiplied %d time%s = %s." % (d, "" if d == 1 else "s", comma(f)))


def g_freq():
    who = P.next()[0]
    rows = [("magnitude 2 to 2.9", 1300000), ("magnitude 3 to 3.9", 130000), ("magnitude 4 to 4.9", 13000), ("magnitude 5 to 5.9", 1300), ("magnitude 6 to 6.9", 130), ("magnitude 7 to 7.9", 15), ("magnitude 8 or more", 1)]
    k = R.choice(["most", "pattern", "compare", "rare"])
    if not once(k, 3):
        return None
    tab = table(["Earthquake size", "About how many happen worldwide each year"], [[r, comma(n)] for r, n in rows])
    if k == "most":
        return item(tab + "According to %s's data, which size of earthquake is most common?" % who, "magnitude 2 to 2.9", ["magnitude 8 or more", "magnitude 6 to 6.9", "They are all equally common."], "Small earthquakes are far more common.")
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % who, "Larger earthquakes are much less frequent.", ["Larger earthquakes happen more often.", "All sizes happen equally often.", "Earthquakes happen once a year."],
                    "About 10 times fewer for each step up in magnitude.")
    if k == "compare":
        return item(tab + "Using %s's data, about how many times more common are magnitude 5 quakes than magnitude 6 quakes?" % who, "about 10 times", ["about 2 times", "about 100 times", "about the same"],
                    "1,300 ÷ 130 = 10.")
    return item(tab + "Based on %s's data, about how many magnitude 8 or larger earthquakes should we expect in the next 10 years?" % who, "about 10", ["about 1", "about 100", "none"], "About 1 per year × 10 years.")


def g_travel():
    who = P.next()[0]
    k = R.choice(["tsunami", "hurricane"])
    if k == "tsunami":
        v = R.choice([600, 700, 800])
        d = v * R.choice([2, 3, 4, 5, 6])
        if not once(("ts", v, d)):
            return None
        t = d // v
        return item("A tsunami travels across the deep ocean at about %d km/h. %s's town is %s km from the earthquake. About how many hours does the town have to evacuate?" % (v, who, comma(d)), "about %d hours" % t,
                    ["about %d hours" % (t * 2), "about %d hours" % (t + 3), "about %s hours" % comma(d)], "time = distance ÷ speed = %s ÷ %d = %d hours." % (comma(d), v, t))
    v = R.choice([15, 20, 25, 30])
    d = v * R.choice([8, 10, 12, 18, 24])
    if not once(("hu", v, d)):
        return None
    t = d // v
    return item("A hurricane is %s km from %s's city and moving toward it at about %d km/h. If it keeps this speed, about how long until it arrives?" % (comma(d), who, v), "about %d hours" % t,
                ["about %d hours" % (t // 2), "about %d hours" % (t + 12), "about %s hours" % comma(d * v)], "%s ÷ %d = %d hours." % (comma(d), v, t))


SIGN = [("small earthquakes increase under a volcano and the ground swells", "a volcanic eruption"),
        ("a volcano releases more sulfur dioxide gas than usual", "a volcanic eruption"),
        ("a river gauge shows water rising after days of heavy rain upstream", "a flood"),
        ("satellites show a spinning storm with warm ocean water ahead of it", "a hurricane"),
        ("Doppler radar shows rotation inside a thunderstorm", "a tornado"),
        ("ocean buoys detect a sudden change in sea level after an undersea earthquake", "a tsunami"),
        ("the sea quickly pulls back far from the beach after strong shaking", "a tsunami"),
        ("months without rain and very dry, windy weather", "a wildfire"),
        ("heavy rain soaks a steep hillside that lost its trees in a fire", "a landslide or mudflow")]


def g_sign():
    s, a = R.choice(SIGN)
    who = P.next()[0]
    if not once(("s", s)):
        return None
    w = sorted({x[1] for x in SIGN if x[1] != a})
    return item("%s's data shows that %s. Which hazard is most likely to follow?" % (who, s), a, R.sample(w, 3), "Monitoring warning signs helps scientists forecast hazards.")


TECH = [("earthquakes", "buildings with base isolators and flexible steel frames"), ("tsunamis", "ocean buoys and warning sirens with marked evacuation routes"),
        ("hurricanes", "storm shutters, stronger roof straps and early warnings from satellites"), ("floods", "levees, floodplain maps and raised buildings"),
        ("volcanic eruptions", "gas and tilt sensors with evacuation plans"), ("tornadoes", "Doppler radar warnings and underground shelters"),
        ("wildfires", "cleared defensible space around homes and fire-resistant roofs"), ("landslides", "retaining walls, drainage and planting trees on slopes")]


def g_tech():
    h, a = R.choice(TECH)
    who = P.next()[0]
    if not once(("t", h)):
        return None
    return item("%s's town wants to reduce damage from %s. Which technology would help most?" % (who, h), a, R.sample([x[1] for x in TECH if x[0] != h], 3), "Mitigation technology matches the hazard.")


def g_rec():
    who = P.next()[0]
    n = R.choice([10, 20, 25, 50, 100])
    k = R.choice(["chance", "again"])
    if not once((n, k)):
        return None
    if k == "chance":
        return item("%s's town is in a %d-year flood zone. What is the chance of such a flood in any one year?" % (who, n), "%g%%" % (100 / n),
                    ["10%" if n != 10 else "1%", "%d%%" % n if n != 100 else "50%", "100%"], "A %d-year flood has a 1 in %d chance each year." % (n, n))
    return item("A %d-year flood happened in %s's town last year. Could another one happen this year?" % (n, who), "Yes. The chance is the same every year, so it could happen again.",
                ["No, not for another %d years." % n, "No, floods cannot happen twice.", "Yes, it is now certain to happen."], "Recurrence intervals describe probability, not a schedule.")


B1 = bank([
    ("Where do most earthquakes and volcanoes happen?", "along tectonic plate boundaries", ["evenly everywhere", "only in deserts", "only near the equator"], "A clear pattern in the data."),
    ("Can scientists predict the exact day of an earthquake?", "No. They can forecast the chance of a quake in an area over years.", ["Yes, to the minute.", "Yes, with a thermometer.", "Only for small quakes."], "Forecasts are probabilities."),
    ("What does a seismometer measure?", "ground shaking from earthquakes", ["wind speed", "rainfall", "temperature"], "Used to locate and measure quakes."),
    ("When is hurricane season in the Atlantic Ocean?", "June through November", ["December through February", "every month equally", "only in April"], "Warm ocean water fuels hurricanes."),
    ("Why are hurricane forecasts better today than 50 years ago?", "Satellites, aircraft data and computer models track storms more accurately.", ["Hurricanes are smaller now.", "People guess better.", "Hurricanes move slower now."],
     "Technology improves forecasts."),
    ("What does a hazard map show?", "areas most at risk from a hazard, like floods or earthquakes", ["the location of all stores", "only roads", "weather for tomorrow"], "Used for planning."),
    ("What is the difference between a forecast and a prediction of an exact event?", "A forecast gives the probability of an event in a time period and area.", ["They are the same.", "A forecast is always exact.", "A forecast is a guess with no data."],
     "Probability, not certainty."),
    ("Why do scientists study records of past hazards?", "Patterns in past events help forecast where and how often hazards may happen.", ["Past events never repeat.", "Records are only for history class.", "To find buried treasure."],
     "Data informs forecasts."),
])
B5 = bank([
    ("Ava's city sits on a fault that had big earthquakes about every 150 years, and the last one was 140 years ago. What is the best conclusion?", "A large earthquake is likely in the coming decades, so the city should prepare.", ["An earthquake will happen in exactly 10 years.", "There will never be another earthquake.", "The fault is now safe."],
     "Patterns give probabilities."),
    ("Leo's data shows tornadoes in his state peak in May. How should a school use this?", "Practice tornado drills before and during spring.", ["Ignore drills in spring.", "Build schools on hilltops.", "Close schools all year."], "Use data to plan."),
    ("Mia compares building damage after an earthquake. Buildings with base isolators had far less damage. What does this support?", "Engineering can reduce the effects of earthquakes.", ["Earthquakes can be stopped.", "Isolators cause earthquakes.", "Damage is random."],
     "Mitigation technology works."),
    ("Why does Hawaii have a tsunami warning center?", "It is surrounded by the Pacific, where many undersea earthquakes happen.", ["Hawaii has no earthquakes.", "It is too cold.", "Tsunamis only happen in lakes."], "Hazard patterns guide warning systems."),
    ("A volcano's sensors show rising gas and swelling for weeks. What should officials do?", "Raise the alert level and prepare evacuation plans.", ["Wait until lava appears.", "Remove the sensors.", "Ignore the data."], "Act on warning signs."),
])


def body():
    think = ("<p>Natural hazards are not random. Data show <b>patterns</b>: earthquakes and volcanoes cluster at <b>plate boundaries</b>, hurricanes form over warm oceans in <b>hurricane season</b>, floods follow heavy rain.</p>"
             "<ul><li>Scientists <b>forecast</b> hazards as <b>probabilities</b> using past records and <b>warning signs</b> (volcano gas and swelling, rising rivers, radar rotation, ocean buoys).</li>"
             "<li>Each earthquake <b>magnitude</b> step means about <b>10×</b> more shaking and about <b>32×</b> more energy.</li>"
             "<li>A <b>100-year flood</b> has a 1% chance each year; it can happen two years in a row.</li>"
             "<li>Engineers design <b>mitigation</b> technology: warning systems, stronger buildings, levees, shelters.</li></ul>")
    ex = [("A tsunami moves at 800 km/h. A coast is 3,200 km away. Warning time?", ["3,200 ÷ 800"], "about 4 hours"),
          ("Magnitude 7 vs. magnitude 5 shaking?", ["10 × 10"], "about 100 times more")]
    mist = ["Thinking earthquakes can be predicted to the exact day.",
            "Thinking a 100-year flood happens only once every 100 years.",
            "Thinking magnitude 6 is just twice magnitude 3."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Patterns in hazards", B1 + [(g_sign, 6), (g_freq, 6)]),
        ("Warning signs and data", [(g_sign, 3), (g_mag, 10), (g_freq, 4), (g_rec, 3)]),
        ("Calculating warning time", [(g_travel, 16), (g_rec, 4)]),
        ("Reducing the effects", [(g_tech, 8), (g_mag, 6), (g_rec, 3), (g_travel, 3)]),
        ("Forecasting with evidence", B5 + [g_mag, g_travel, g_freq, g_rec]),
    ])
    make("grade-8", "forecasting-natural-hazards", 22, "MS-ESS3-2",
         "Analyze and interpret data on natural hazards to forecast future catastrophic events and inform the development of technologies to mitigate their effects.",
         "Forecasting Natural Hazards",
         "Grade 8 Forecasting Natural Hazards Worksheets: Earthquakes, Tsunamis, Hurricanes and Floods",
         "Forecasting Natural Hazards",
         "Free middle school science worksheets on forecasting natural hazards (NGSS MS-ESS3-2): hazard patterns, warning signs, earthquake magnitude and frequency data, tsunami and hurricane travel time, flood recurrence and mitigation technology. 100 practice questions with answers.",
         "Hazard data give probabilities, not exact dates.",
         "Patterns and warning signs help scientists forecast hazards, and engineers use the data to design ways to reduce damage.",
         body(),
         [("Can scientists predict earthquakes?", "Not the exact time. They forecast the probability of earthquakes in an area over years using records of past quakes and fault data."),
          ("What does a 100-year flood mean?", "A flood that has a 1% chance of happening in any given year. It can happen in back-to-back years."),
          ("How do people reduce damage from natural hazards?", "With warning systems, hazard maps, stronger buildings, levees, shelters and evacuation plans based on hazard data.")],
         sets)


if __name__ == "__main__":
    main()
