# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Plate Tectonics (MS-ESS2-3)
  python tools/gen_us_science_g7_plate_tectonics.py
Analyze and interpret data on the distribution of fossils and rocks, continental shapes, and seafloor structures
to provide evidence of the past plate motions: matching coastlines (South America and Africa), Mesosaurus and
Glossopteris fossils on several continents, matching rock layers and mountain belts, mid-ocean ridges, rock age
increasing away from ridges, trenches. Boundaries: divergent, convergent, transform.
Wrong answers come from real mistakes: "continents float on the ocean", "plates move several meters a year",
"the youngest seafloor is at the edges of oceans".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(70115)
R = U.R
P = People(R)

EVID = [("The coastlines of South America and Africa fit together like puzzle pieces.", "continental shapes"),
        ("Fossils of Mesosaurus, a small freshwater reptile, are found only in South America and Africa.", "fossils"),
        ("Fossils of the plant Glossopteris are found in South America, Africa, India, Antarctica and Australia.", "fossils"),
        ("The same kinds of rock layers and mountain belts appear in eastern North America and western Europe.", "rock formations"),
        ("A long underwater mountain chain runs down the middle of the Atlantic Ocean.", "seafloor structures"),
        ("Seafloor rock is youngest at mid-ocean ridges and older farther away.", "seafloor structures"),
        ("Deep trenches lie along the edges of the Pacific Ocean.", "seafloor structures"),
        ("Glacier scratches are found in rocks in Africa and India, which are warm today.", "rock formations")]


def g_evid():
    s, k = R.choice(EVID)
    who = P.next()[0]
    return item("%s reads: “%s” What kind of evidence for plate motion is this?" % (who, s), k, [x for x in ["continental shapes", "fossils", "rock formations", "seafloor structures"] if x != k],
                "All four kinds of evidence show that the continents and seafloor have moved.")


def g_explain():
    s, k = R.choice(EVID)
    who = P.next()[0]
    expl = {"continental shapes": "The continents were once joined and have moved apart.", "fossils": "The continents were once connected, so the organisms lived across one land area.",
            "rock formations": "The rocks formed together when the continents were joined.", "seafloor structures": "New seafloor forms at ridges and spreads outward as plates move apart."}
    if "trenches" in s:
        a = "Old seafloor sinks back into Earth where plates collide."
    else:
        a = expl[k]
    w = ["Animals swam across the ocean carrying the rocks.", "The continents have never moved.", "Earth is getting smaller.", "Wind blew the fossils across the ocean."]
    return item("%s reads: “%s” What is the best explanation?" % (who, s), a, R.sample(w, 3), "Plates carrying continents and seafloor move a few centimeters per year.")


def g_age():
    rate = R.choice([2, 3, 4, 5])  # cm per year -> km per million years = 10*rate
    km_per_my = rate * 10
    d = [0, km_per_my * 10, km_per_my * 20, km_per_my * 40]
    ages = [0, 10, 20, 40]
    rows = [["{:,} km".format(x), "%d million years" % a if a else "brand new"] for x, a in zip(d, ages)]
    who = P.next()[0]
    tab = table(["Distance from the mid-ocean ridge", "Age of the seafloor rock"], rows)
    k = R.choice(["where", "pattern", "predict"])
    if k == "where":
        return item(tab + "Where is the youngest seafloor in %s's data?" % who, "at the mid-ocean ridge", ["farthest from the ridge", "in the middle of the continents", "spread evenly everywhere"],
                    "New rock forms at the ridge as magma rises and cools.")
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % who, "The seafloor gets older farther from the ridge.", ["The seafloor gets younger farther from the ridge.", "All seafloor is the same age.", "The ridge is the oldest part."],
                    "This is evidence of seafloor spreading.")
    x = km_per_my * 30
    return item(tab + "Using %s's data, about how old is the seafloor {:,} km from the ridge?".format(x) % who, "30 million years", ["3 million years", "60 million years", "300 million years"],
                "Every {:,} km away from the ridge adds about 10 million years, so {:,} km is about 30 million years.".format(km_per_my * 10, x))


BOUND = {"divergent": ("plates move apart", ["the Mid-Atlantic Ridge", "the East African Rift", "Iceland splitting slowly"]),
         "convergent": ("plates push together", ["the Himalayas", "the Andes Mountains", "the volcanoes of Japan"]),
         "transform": ("plates slide past each other", ["the San Andreas Fault in California", "the Alpine Fault in New Zealand"])}


def g_bound():
    k = R.choice(sorted(BOUND))
    how, ex = BOUND[k]
    who = P.next()[0]
    x = R.choice(ex)
    if R.random() < 0.5:
        return item("%s studies %s, where %s. What kind of plate boundary is it?" % (who, x, how), "a %s boundary" % k, ["a %s boundary" % y for y in BOUND if y != k] + ["not a boundary"],
                    "At a %s boundary, %s." % (k, how))
    return item("%s studies %s. What happens to the plates there?" % (who, x), "The " + how + ".", ["The " + BOUND[y][0] + "." for y in BOUND if y != k] + ["The plates stop moving forever."],
                "%s is at a %s boundary." % (x[0].upper() + x[1:], k))


B1 = bank([
    ("What are tectonic plates?", "large pieces of Earth's outer layer (lithosphere) that slowly move", ["clouds of gas", "ocean currents", "layers of ice"], "Continents and ocean floors ride on plates."),
    ("About how fast do plates move?", "a few centimeters per year, about as fast as fingernails grow", ["several meters per year", "a kilometer per day", "they never move"], "Slow, but it adds up over millions of years."),
    ("What was Pangaea?", "a supercontinent that existed about 300–200 million years ago", ["a kind of fossil", "an ocean", "a volcano"], "It broke apart into today's continents."),
    ("Who first proposed continental drift using fossils and continent shapes?", "Alfred Wegener", ["Isaac Newton", "Charles Darwin", "Albert Einstein"], "He proposed it in 1912."),
    ("What forms at a mid-ocean ridge?", "new ocean floor from rising magma", ["deep trenches", "old continents", "coral reefs only"], "This is seafloor spreading."),
    ("Why couldn't Mesosaurus have swum across the Atlantic?", "It was a small freshwater reptile that could not cross a salty ocean.", ["It could fly.", "The ocean was frozen.", "It was too big."],
     "Its fossils support the idea that the continents were joined."),
    ("Do continents float on the ocean?", "No. Continents are part of plates that move over the hot, slowly flowing mantle.", ["Yes, like rafts.", "Yes, but only in summer.", "They are anchored forever."],
     "The mantle rock can flow very slowly."),
    ("What often happens where an ocean plate meets a continental plate?", "The ocean plate sinks, forming a trench and volcanoes.", ["Nothing happens.", "A ridge forms.", "The continent sinks."], "The denser plate sinks."),
])
B5 = bank([
    ("Ava cuts out maps of South America and Africa and fits them together. The edges of the continental shelves fit even better than the coastlines. What does this support?", "The continents were once joined.", ["The maps are wrong.", "The oceans are shrinking.", "The continents are growing."],
     "Continental shapes are evidence of past motion."),
    ("Leo finds the same 250-million-year-old rock layers in Brazil and West Africa. What does this suggest?", "The two areas were connected when the rocks formed.", ["Rocks swim across oceans.", "Both rocks formed yesterday.", "It is a coincidence with no meaning."],
     "Matching rocks are evidence."),
    ("Mia plots earthquakes on a map. They form long lines. What do the lines show?", "the edges of tectonic plates", ["the paths of rivers", "where it rains most", "the equator"], "Most earthquakes happen at plate boundaries."),
    ("GPS shows Hawaii moving northwest about 7 cm per year. How far will it move in 1,000,000 years?", "70 km", ["7 km", "700 km", "7 m"], "7 cm × 1,000,000 = 7,000,000 cm = 70 km."),
    ("Why is new seafloor at ridges evidence that plates move?", "New rock forms in the middle and the older rock moves outward on both sides.", ["The ridge is older than the edges.", "Seafloor never changes.", "Ridges are made of sand."],
     "Seafloor spreading pushes plates apart."),
])


def body():
    think = ("<p>Earth's outer layer is broken into <b>tectonic plates</b> that move a few centimeters per year. Scientists use four kinds of evidence:</p>"
             "<ul><li><b>Continental shapes</b>: South America and Africa fit like puzzle pieces.</li>"
             "<li><b>Fossils</b>: the same land plants and animals (Glossopteris, Mesosaurus) are found on continents now separated by oceans.</li>"
             "<li><b>Rock formations</b>: matching rock layers and mountain belts on different continents.</li>"
             "<li><b>Seafloor structures</b>: mid-ocean ridges, deep trenches, and seafloor that gets older farther from the ridges.</li></ul>"
             "<p>At <b>divergent</b> boundaries plates move apart, at <b>convergent</b> boundaries they push together, and at <b>transform</b> boundaries they slide past each other.</p>")
    ex = [("The same fossil fern is found in Africa and India. What does this suggest?", ["Plants could not cross the ocean."], "The continents were once joined."),
          ("Where is the youngest seafloor?", ["New rock forms where plates spread apart."], "at mid-ocean ridges")]
    mist = ["Thinking continents float on the ocean.",
            "Thinking plates move meters per year. They move centimeters.",
            "Thinking the oldest seafloor is at the ridge."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Moving plates", B1 + [(g_evid, 12)]),
        ("Evidence for plate motion", [(g_evid, 8), (g_explain, 12)]),
        ("Seafloor data", [(g_age, 14), (g_explain, 6)]),
        ("Plate boundaries", [(g_bound, 14), (g_age, 6)]),
        ("Interpreting evidence", B5 + [g_bound, g_age, g_explain, g_evid]),
    ])
    make("grade-7", "plate-tectonics", 15, "MS-ESS2-3",
         "Analyze and interpret data on the distribution of fossils and rocks, continental shapes, and seafloor structures to provide evidence of the past plate motions.",
         "Plate Tectonics",
         "Grade 7 Plate Tectonics Worksheets: Continental Drift, Seafloor Spreading and Plate Boundaries",
         "Plate Tectonics",
         "Free middle school science worksheets on plate tectonics (NGSS MS-ESS2-3): evidence from fossils, rocks, continent shapes and the seafloor, seafloor age data, and plate boundaries. 100 practice questions with answers.",
         "Fossils, rocks and the seafloor show that plates move.",
         "Matching coastlines, fossils and rocks, plus seafloor that ages away from ridges, show continents have moved over millions of years.",
         body(),
         [("What evidence shows that continents have moved?", "Matching continent shapes, the same fossils and rock layers on different continents, and seafloor features like mid-ocean ridges and seafloor ages."),
          ("How fast do tectonic plates move?", "About 2 to 10 centimeters per year, roughly as fast as fingernails grow."),
          ("What are the three kinds of plate boundaries?", "Divergent (moving apart), convergent (pushing together) and transform (sliding past each other).")],
         sets)


if __name__ == "__main__":
    main()
