# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Processes That Shape Earth's Surface (MS-ESS2-2)
  python tools/gen_us_science_g7_shaping_earths_surface.py
Construct an explanation based on evidence for how geoscience processes have changed Earth's surface at varying
time and spatial scales: slow and large (mountain building, canyon carving, glaciers, continental drift), fast and
local (earthquakes, landslides, volcanic eruptions, flash floods, meteor impacts). Rates (mm per year) and
calculations over long times.
Wrong answers come from real mistakes: "all landforms formed quickly", "slow processes cannot make big changes",
"the Grand Canyon formed in a few years".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(70114)
R = U.R
P = People(R)

FAST = ["a landslide covers a road", "a volcanic eruption builds a new cone of ash", "an earthquake opens a crack in the ground", "a flash flood carves a gully",
        "a meteor makes a crater", "a hurricane moves a beach's sand", "a rockfall drops boulders from a cliff", "a tsunami washes away a coastline's sand dunes"]
SLOW = ["a river carves a deep canyon", "mountains are pushed up by colliding plates", "a glacier carves a U-shaped valley", "wind shapes desert rocks into arches",
        "continents drift apart and an ocean widens", "rock layers build up on a sea floor", "waves wear back a sea cliff", "a delta grows at the mouth of a river"]


def g_speed():
    who = P.next()[0]
    if R.random() < 0.5:
        x = R.choice(FAST)
        return item("%s reads that %s. Does this change happen quickly (minutes to days) or slowly (thousands to millions of years)?" % (who, x), "quickly",
                    ["slowly", "It never happens.", "It happens only on other planets."], "Earthquakes, landslides and eruptions change the surface quickly in small areas.")
    x = R.choice(SLOW)
    return item("%s reads that %s. Does this change happen quickly (minutes to days) or slowly (thousands to millions of years)?" % (who, x), "slowly",
                ["quickly", "It never happens.", "It happens in one afternoon."], "Many large landforms are built by slow processes over very long times.")


def D(mm):
    if mm >= 1000:
        return "%s m" % comma(mm // 1000) if mm % 1000 == 0 else "%s m" % ("{:,.1f}".format(mm / 1000))
    if mm % 10 == 0:
        return "%d cm" % (mm // 10)
    return "%d mm" % mm


def g_rate():
    who = P.next()[0]
    cases = [("The Himalayas rise about %d mm per year.", [4, 5, 10], 1, "taller"), ("The Atlantic Ocean widens about %d cm per year.", [2, 3, 4], 10, "wider"),
             ("A river cuts its canyon about %d mm deeper per year.", [1, 2, 3], 1, "deeper")]
    s_, rates, mul, word = R.choice(cases)
    r = R.choice(rates)
    yrs = R.choice([10000, 100000, 1000000])
    tot = r * mul * yrs
    ans = D(tot)
    w = [D(tot * 10), D(tot // 10), D(r * mul * 100)]
    if ans in w or len(set(w)) < 3:
        return None
    return item("%s learns: “%s” At this rate, about how much %s will %s get in %s years?" % (who, s_ % r, word, "they" if "Himalayas" in s_ else "it", comma(yrs)), ans, w,
                "%d %s × %s years = %s; 1,000 mm = 1 m." % (r, "cm" if mul == 10 else "mm", comma(yrs), ans))


EVID = [("Seashell fossils are found high in the Rocky Mountains.", "The rock formed under the sea and was slowly pushed up."),
        ("Rock layers on both sides of a canyon match.", "A river slowly cut down through the layers."),
        ("Scratches and large boulders are found in a valley far from mountains.", "A glacier once moved through the valley."),
        ("Fresh ash and cooled lava cover a town's fields.", "A volcano erupted recently."),
        ("The coasts of South America and Africa fit together like puzzle pieces.", "The continents were once joined and drifted apart."),
        ("A fence that was straight is now offset by 2 meters across a crack.", "An earthquake moved the ground along a fault.")]


def g_evid():
    s, a = R.choice(EVID)
    who = P.next()[0]
    return item("%s observes: “%s” What is the best explanation?" % (who, s), a, R.sample([e[1] for e in EVID if e[1] != a], 3), "Evidence in landforms tells how the surface changed.")


B1 = bank([
    ("How can slow processes make large changes to Earth's surface?", "Small changes add up over millions of years.", ["They cannot make large changes.", "Slow processes only work on Mars.", "They speed up over time."],
     "1 mm a year for a million years is 1 km."),
    ("Which process formed the Grand Canyon?", "the Colorado River slowly eroding rock for millions of years", ["one huge earthquake", "a meteor impact", "a single flood last century"], "Slow erosion over a very long time."),
    ("What causes mountains like the Himalayas to form?", "two tectonic plates colliding and pushing rock up", ["rivers depositing sand", "wind piling up dust", "glaciers melting"], "India is still pushing into Asia."),
    ("Which change happens fastest?", "a landslide", ["the formation of a canyon", "mountain building", "continents drifting"], "Landslides happen in seconds or minutes."),
    ("What does 'spatial scale' mean?", "the size of the area that is changed", ["the time it takes", "the weight of rocks", "the depth of the ocean"], "Changes can be local or affect whole continents."),
    ("Which tool helps scientists measure how fast continents move today?", "GPS satellites", ["a thermometer", "a rain gauge", "a magnifying glass"], "GPS can measure movement of a few centimeters per year."),
    ("Can a fast event and a slow process both shape the same landform?", "Yes. A canyon can grow slowly and also change suddenly in a flood or rockfall.", ["No, never.", "Only slow processes shape land.", "Only fast events shape land."],
     "Both scales matter."),
    ("Glaciers carve valleys into what shape?", "a U shape", ["a V shape", "a perfect circle", "a flat square"], "Rivers usually carve V-shaped valleys."),
])
B5 = bank([
    ("Ava pours water down a sand hill once and sees a small groove. She repeats it 50 times. What does this model?", "how slow, repeated erosion carves large valleys", ["a volcanic eruption", "an earthquake", "mountain building"],
     "Many small changes add up."),
    ("Leo finds that a delta grew 2 km in 500 years. About how many meters per year is that?", "4 meters per year", ["0.4 meters per year", "40 meters per year", "2 meters per year"], "2,000 m ÷ 500 = 4 m."),
    ("Mia compares two volcanoes: one built over a few weeks and one over 500,000 years. What does this show?", "Landforms can form at very different time scales.", ["All volcanoes form in a week.", "Volcanoes never grow.", "Time does not matter."],
     "Rates vary."),
    ("Why are very old mountains, like the Appalachians, lower and more rounded than young mountains, like the Rockies?", "Erosion has worn them down for a much longer time.", ["They were never tall.", "They are made of sand.", "Glaciers built them up."],
     "Time and erosion lower mountains."),
    ("Scientists find a thin layer of ash in rock layers across North America. What does it suggest?", "A large eruption spread ash over a huge area at one time.", ["The ash formed slowly over a million years.", "It is from a campfire.", "It is a fossil."],
     "A fast event can have a large spatial scale."),
])


def body():
    think = ("<p>Earth's surface is shaped by processes that work at very different <b>time scales</b> and <b>spatial scales</b>.</p>"
             "<ul><li><b>Fast and local</b>: earthquakes, landslides, volcanic eruptions, flash floods, meteor impacts.</li>"
             "<li><b>Slow and large</b>: mountain building, rivers carving canyons, glaciers carving valleys, continents drifting.</li></ul>"
             "<p>Slow processes can make huge changes because tiny changes add up: 5 mm per year for 1,000,000 years is 5,000 meters. "
             "Evidence in landforms (fossils, rock layers, scratches from glaciers) helps explain how the surface changed.</p>")
    ex = [("A river deepens its canyon 2 mm per year. How much in 1,000,000 years?", ["2 mm × 1,000,000 = 2,000,000 mm", "= 2,000 m"], "2,000 m"),
          ("Is a landslide fast or slow?", ["It happens in minutes."], "fast")]
    mist = ["Thinking all landforms formed quickly.",
            "Thinking slow processes cannot make big changes.",
            "Mixing up mm, cm and m when calculating over long times."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fast and slow changes", B1 + [(g_speed, 12)]),
        ("Time scales", [(g_speed, 12), (g_evid, 8)]),
        ("Rates of change", [(g_rate, 14), (g_speed, 6)]),
        ("Evidence in landforms", [(g_evid, 12), (g_rate, 8)]),
        ("Explaining Earth's surface", B5 + [g_rate, g_evid, g_speed]),
    ])
    make("grade-7", "shaping-earths-surface", 14, "MS-ESS2-2",
         "Construct an explanation based on evidence for how geoscience processes have changed Earth's surface at varying time and spatial scales.",
         "Processes That Shape Earth's Surface",
         "Grade 7 Earth's Surface Worksheets: Fast and Slow Changes, Rates and Evidence",
         "Shaping Earth's Surface",
         "Free middle school science worksheets on processes that shape Earth's surface (NGSS MS-ESS2-2): fast events and slow processes, rates of erosion and uplift, and evidence in landforms. 100 practice questions with answers.",
         "Small, slow changes add up to big landforms.",
         "Earthquakes and landslides change the land fast; rivers, glaciers and moving plates change it slowly over millions of years.",
         body(),
         [("What are examples of fast and slow changes to Earth's surface?", "Fast: earthquakes, landslides, eruptions and floods. Slow: mountain building, canyon carving by rivers, glaciers and continental drift."),
          ("How can slow processes create huge landforms?", "Tiny changes each year add up over millions of years. A few millimeters a year can become kilometers."),
          ("How do scientists know how Earth's surface changed?", "They use evidence such as rock layers, fossils, glacier scratches, matching coastlines and measurements of today's rates.")],
         sets)


if __name__ == "__main__":
    main()
