# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Natural Resources (MS-ESS3-1)
  python tools/gen_us_science_g7_natural_resources.py
Construct a scientific explanation based on evidence for how the uneven distributions of Earth's mineral, energy
and groundwater resources are the result of past and current geoscience processes: oil and natural gas from
ancient marine organisms buried in sediment; coal from ancient swamp plants; metal ores concentrated by magma and
hot water near plate boundaries; groundwater stored in porous rock (aquifers); resources are limited and nonrenewable
on human time scales.
Wrong answers come from real mistakes: "oil comes from dinosaurs", "resources are spread evenly", "groundwater is an
underground lake everywhere", "minerals can be replaced quickly".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(70116)
R = U.R
P = People(R)

ORIGIN = {"oil and natural gas": "tiny marine organisms buried in ocean sediments, then heated and pressed for millions of years",
          "coal": "plants from ancient swamps buried and squeezed for millions of years",
          "copper and gold ores": "hot, mineral-rich water and magma near volcanoes and plate boundaries",
          "groundwater": "rain and snowmelt soaking into porous rock and sediment (aquifers)",
          "rock salt": "seawater evaporating in shallow basins long ago",
          "iron ore": "iron that settled out of ancient oceans in layers"}


def g_origin():
    k = R.choice(sorted(ORIGIN))
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s asks how %s formed. What is the best explanation?" % (who, k), "from " + ORIGIN[k], ["from " + ORIGIN[x] for x in R.sample([y for y in ORIGIN if y != k], 3)],
                    "%s formed from %s." % (k[0].upper() + k[1:], ORIGIN[k]))
    return item("%s reads about a resource that formed from %s. Which resource is it?" % (who, ORIGIN[k]), k, R.sample([y for y in ORIGIN if y != k], 3), "That is how %s formed." % k)


def g_where():
    who = P.next()[0]
    cases = [("Scientists search for oil.", "in thick layers of sedimentary rock that were once under the sea", ["in solid granite mountains", "inside active volcanoes", "on top of glaciers"]),
             ("A company looks for coal.", "in rock layers that were once swamps", ["in deep ocean trenches", "in volcanic ash only", "in sand dunes"]),
             ("Geologists look for copper deposits.", "near old volcanoes and plate boundaries", ["in the middle of flat swamps", "only in rivers", "in clouds"]),
             ("A town wants to dig a well for water.", "in porous sand and gravel layers that hold groundwater", ["in solid unbroken granite", "on a mountain peak", "in a salt flat"]),
             ("Miners look for diamonds.", "in rock that rose from deep in the mantle through ancient volcanic pipes", ["in beach sand made from shells", "in coal swamps", "in the ocean floor ridges only"])]
    s, a, w = R.choice(cases)
    return item("%s learns: “%s” Where are they most likely to find it?" % (who, s), a, w, "Resources are found where geologic processes concentrated them.")


def g_use():
    who = P.next()[0]
    total = R.choice([500, 800, 1000, 1200, 2000])
    rate = R.choice([10, 20, 25, 40, 50])
    yrs = total // rate
    if total % rate:
        return None
    k = R.choice(["oil", "water"])
    if k == "oil":
        return item("%s reads that an oil field holds about %s million barrels, and %d million barrels are pumped each year. If this continues, about how many years will the oil last?" % (who, comma(total), rate),
                    "%d years" % yrs, ["%d years" % (yrs * 2), "%d years" % (total + rate), "forever"], "%s ÷ %d = %d years. Oil formed over millions of years, so it is nonrenewable." % (comma(total), rate, yrs))
    return item("%s learns that an aquifer holds %s billion liters. People pump out %d billion liters a year, and rain refills only a small amount. About how many years until it runs low (ignoring refill)?" % (who, comma(total), rate),
                "%d years" % yrs, ["%d years" % (yrs * 2), "%d years" % rate, "It can never run low."], "%s ÷ %d = %d years. Pumping faster than refilling depletes groundwater." % (comma(total), rate, yrs))


B1 = bank([
    ("Why are natural resources unevenly distributed on Earth?", "Different geologic processes happened in different places over Earth's history.", ["People moved them around.", "Resources are spread evenly.", "Rain carries them everywhere."],
     "Oil forms where marine sediments were buried; ores form near volcanoes."),
    ("Does oil come from dinosaurs?", "No. Most oil comes from tiny marine organisms like plankton.", ["Yes, all of it.", "It comes from trees.", "It comes from volcanoes."],
     "Plankton buried in sediment became oil."),
    ("Why are fossil fuels called nonrenewable?", "They take millions of years to form, much longer than we use them.", ["They are made every day.", "They are made in factories.", "They never run out."],
     "We use them much faster than they form."),
    ("What is an aquifer?", "a layer of porous rock or sediment that holds groundwater", ["an underground river of lava", "a cave full of air", "a lake on the surface"], "Water fills the spaces between grains."),
    ("Where are many metal ores found?", "near past and present volcanoes and plate boundaries", ["only in deserts", "only in oceans", "evenly in every backyard"], "Hot fluids concentrated the metals."),
    ("Why do some countries have lots of oil and others have none?", "Oil forms only where specific conditions existed in the past.", ["Some countries make oil.", "Oil moves with the wind.", "It is random luck only."],
     "Geologic history determines where resources are."),
    ("What happens when people pump groundwater faster than it refills?", "The water table drops and wells can run dry.", ["More water appears.", "Nothing happens.", "The water turns to oil."], "Groundwater can be depleted."),
    ("Which resource formed from ancient swamp plants?", "coal", ["oil", "copper", "rock salt"], "Swamp plants buried in layers became coal."),
])
B5 = bank([
    ("Ava finds a map showing that coal deposits in the U.S. are in specific regions. What explanation best fits?", "Those regions had swamps hundreds of millions of years ago.", ["Coal was spread by trucks.", "Coal forms anywhere it rains.", "Coal grows in mountains."],
     "Past environments explain today's resources."),
    ("Leo notices that gold mining towns are often near old volcanoes. Why?", "Magma and hot water concentrated gold in rocks there.", ["Volcanoes make gold from air.", "It is a coincidence.", "People carried gold to volcanoes."],
     "Geologic processes concentrate minerals."),
    ("Mia models an aquifer with gravel, sand and clay in a cup and pours water in. Which layer holds the most water?", "gravel and sand, which have more space between grains", ["clay, which has no space", "the cup itself", "none of them"],
     "Porous layers store water."),
    ("Why is recycling metals important?", "Metal ores are limited and took millions of years to form.", ["Metals grow back quickly.", "Mining has no effects.", "Recycling makes new ore."], "Conserving limited resources."),
    ("A region's well levels drop 1 meter per year. What is the most likely cause?", "People are using groundwater faster than it is replaced.", ["Too much rain.", "The wells are getting taller.", "Earthquakes add water."],
     "Overuse depletes aquifers."),
])


def body():
    think = ("<p>Earth's <b>mineral, energy and groundwater resources</b> are not spread evenly. They are found where <b>geologic processes</b> concentrated them, long ago or today.</p><ul>"
             + "".join("<li><b>%s</b>: from %s.</li>" % (k[0].upper() + k[1:], v) for k, v in ORIGIN.items()) + "</ul>"
             "<p>Most of these resources form over millions of years, so they are <b>nonrenewable</b> on human time scales. Groundwater can be used up if it is pumped faster than rain refills it.</p>")
    ex = [("Where would you look for oil?", ["Oil forms from buried marine organisms."], "in sedimentary rock that was once under the sea"),
          ("An oil field has 600 million barrels and 30 million are used a year. How long will it last?", ["600 ÷ 30"], "20 years")]
    mist = ["Thinking oil comes from dinosaurs.",
            "Thinking resources are spread evenly everywhere.",
            "Thinking minerals and fossil fuels are replaced quickly."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Where resources come from", B1 + [(g_origin, 12)]),
        ("How resources formed", [(g_origin, 12), (g_where, 8)]),
        ("Where to find resources", [(g_where, 14), (g_use, 6)]),
        ("Using limited resources", [(g_use, 14), (g_origin, 6)]),
        ("Explaining distributions", B5 + [g_where, g_use, g_origin]),
    ])
    make("grade-7", "natural-resources", 16, "MS-ESS3-1",
         "Construct a scientific explanation based on evidence for how the uneven distributions of Earth's mineral, energy, and groundwater resources are the result of past and current geoscience processes.",
         "Natural Resources",
         "Grade 7 Natural Resources Worksheets: Oil, Coal, Minerals and Groundwater",
         "Natural Resources",
         "Free middle school science worksheets on natural resources (NGSS MS-ESS3-1): how oil, coal, metal ores and groundwater form, why they are unevenly distributed, and how long limited resources last. 100 practice questions with answers.",
         "Resources are where geologic processes put them.",
         "Oil formed from buried sea life, coal from ancient swamps, and ores near volcanoes, so resources are uneven and limited.",
         body(),
         [("Why are resources like oil and metals found only in some places?", "They formed only where certain geologic processes happened, such as buried marine sediments for oil or magma and hot water for metal ores."),
          ("How did oil form?", "From tiny marine organisms buried in sediment and changed by heat and pressure over millions of years."),
          ("Can groundwater run out?", "Yes. If people pump water out of an aquifer faster than rain refills it, the water level drops and wells can dry up.")],
         sets)


if __name__ == "__main__":
    main()
