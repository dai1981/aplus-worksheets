# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Plate Tectonics and the Age of the Crust (HS-ESS1-5)
  python tools/gen_us_science_ess_plate_tectonics_and_crust_age.py
Evaluate evidence of the past and current movements of continental and oceanic crust and the theory of plate tectonics
to explain the ages of crustal rocks.
Seafloor spreading rates (rate = distance ÷ age), seafloor age patterns, magnetic striping, why oceanic crust is young
and continental crust is old, plate boundaries and their features, and evidence for continental drift.
Wrong answers come from real mistakes: "the oldest seafloor is at the ridge", "oceanic crust is as old as Earth",
"plates move meters per year", "continents float on the ocean".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90405)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_rate():
    who = P.next()[0]
    r = R.choice([1, 2, 2.5, 3, 4, 5, 6, 8, 10])
    age = R.choice([1, 2, 4, 5, 8, 10, 20, 25, 40, 50])
    km = r * age * 10
    k = R.choice(["rate", "dist", "age"])
    if km != round(km, 1) or not once(("rt", r, age, k)):
        return None
    ridge = "the East Pacific Rise" if r >= 5 else "the Mid-Atlantic Ridge" if r <= 2.5 else "a mid-ocean ridge"
    if k == "rate":
        g = "%s cm per year" % num(r, 1)
        return item("%s finds seafloor rock %s km from %s that is %s million years old. What is the average spreading rate? (1 km = 100,000 cm)" % (who, num(km, 1), ridge, num(age)), g,
                    uniq(g, ["%s cm per year" % num(r * 10, 1), "%s cm per year" % num(km / age, 1), "%s cm per year" % num(r / 10, 2), "%s cm per year" % num(age / km, 3)]),
                    "%s km = %s cm; ÷ %s million years = %s cm/yr." % (num(km, 1), num(km * 100000), num(age), num(r, 1)))
    if k == "dist":
        g = "%s km" % num(km, 1)
        return item("A plate moves away from %s at %s cm per year. How far from the ridge is rock that formed %s million years ago? (100,000 cm = 1 km)" % (ridge, num(r, 1), num(age)), g,
                    uniq(g, ["%s km" % num(km * 10, 1), "%s km" % num(km / 10, 2), "%s km" % num(r * age, 1), "%s km" % num(km * 100000)]), "%s cm/yr × %s × 10<sup>6</sup> yr = %s cm = %s km." % (num(r, 1), num(age), num(r * age * 1e6), num(km, 1)))
    g = "%s million years" % num(age)
    return item("Seafloor spreads at %s cm per year. About how old is rock %s km from the ridge?" % (num(r, 1), num(km, 1)), g,
                uniq(g, ["%s million years" % num(age * 10), "%s million years" % num(age / 10, 2), "%s million years" % num(km, 1), "%s million years" % num(age * 2)]),
                "%s km = %s cm; ÷ %s cm/yr = %s years." % (num(km, 1), num(km * 100000), num(r, 1), num(age * 1e6)))


@safe
def g_ages():
    who = P.next()[0]
    step = R.choice([100, 200, 300])
    d = [step * i for i in range(5)]
    r = R.choice([2, 4, 5])
    ages = [x / (10 * r) for x in d]
    k = R.choice(["old", "young", "pat", "mirror"])
    if not once(("ag", step, r, k)):
        return None
    tab = table(["Distance from ridge (km)", "Age of seafloor (million years)"], [[str(a), num(b, 1)] for a, b in zip(d, ages)])
    if k == "old":
        return item(tab + "In %s's data, where is the oldest seafloor?" % who, "farthest from the ridge (%d km)" % d[-1], ["at the ridge (0 km)", "400 km from the ridge", "It is all the same age."], "New crust forms at the ridge and moves away.")
    if k == "young":
        return item(tab + "Where does new oceanic crust form, according to %s's data?" % who, "at the mid-ocean ridge", ["at the edges of continents", "far from the ridge", "everywhere at once"], "Age 0 at the ridge.")
    if k == "pat":
        return item(tab + "What pattern do %s's data show?" % who, "Seafloor gets older farther from the ridge.", ["Seafloor gets younger farther from the ridge.", "All the seafloor is the same age.", "Age changes at random."],
                    "Evidence for seafloor spreading.")
    return item(tab + "%s measured on one side of the ridge. What would she likely find on the other side?" % who, "the same pattern of ages, mirrored", ["much older rocks right at the ridge", "no rocks at all", "ages that get younger away from the ridge"],
                "Spreading is symmetrical.")


BND = [("Two plates pull apart under the ocean.", "a mid-ocean ridge with new crust"), ("Two plates pull apart on land, as in East Africa.", "a rift valley"),
       ("An ocean plate sinks under a continent, as off South America.", "a deep trench and a chain of volcanic mountains"), ("Two continental plates collide, as India hit Asia.", "very high folded mountains like the Himalayas"),
       ("One ocean plate sinks under another, as near Japan.", "a trench and a curved chain of volcanic islands"), ("Two plates slide past each other, as at the San Andreas Fault.", "frequent earthquakes but few volcanoes")]


@safe
def g_bnd():
    s, f = R.choice(BND)
    k = R.random() < 0.6
    if not once(("bd", s, k)):
        return None
    if k:
        return item("%s What feature forms?" % s, f, R.sample([x[1] for x in BND if x[1] != f], 3), "Divergent: ridges and rifts. Convergent: trenches, volcanoes, mountains. Transform: earthquakes.")
    return item("Which boundary makes %s?" % f, s.rstrip("."), R.sample([x[0].rstrip(".") for x in BND if x[0] != s], 3), "Match the motion to the feature.")


EV = [("The same fossil reptile, Mesosaurus, is found in South America and Africa.", "These continents were once joined."),
      ("Rock layers and mountain belts match across the Atlantic Ocean.", "The rocks formed together before the continents split."),
      ("Coal from tropical swamps is found in Antarctica.", "Antarctica was once near the equator."),
      ("Glacier scratches in India and Africa point in directions that only make sense if the continents were joined.", "The southern continents were together near the South Pole."),
      ("Magnetic stripes on the seafloor are symmetric on both sides of the ridge.", "New crust forms at the ridge and spreads both ways."),
      ("GPS stations show Hawaii moving about 7 cm per year toward Japan.", "Plates are moving today."),
      ("The coastlines of South America and Africa fit together like puzzle pieces.", "The continents may once have been joined.")]


@safe
def g_ev():
    s, a = R.choice(EV)
    k = R.random() < 0.6
    if not once(("ev", s, k)):
        return None
    if k:
        return item("Evidence: %s What does it support?" % s, a, R.sample([x[1] for x in EV if x[1] != a], 3), "Many lines of evidence support plate tectonics.")
    return item("Which evidence best supports this idea: “%s”" % a, s, R.sample([x[0] for x in EV if x[0] != s], 3), "Match the evidence.")


B1 = bank([
    ("Why is the oldest oceanic crust only about 180 million years old?", "Oceanic crust is destroyed at subduction zones and recycled into the mantle.", ["The oceans are young.", "Old crust dissolves in seawater.", "Earth is only 180 million years old."], "Subduction."),
    ("Why can continental rocks be up to 4 billion years old?", "Continental crust is thick and light, so it does not sink back into the mantle.", ["Continents are made of iron.", "Continents formed last.", "Rain protects them."], "Buoyant crust."),
    ("Where is the youngest seafloor?", "at mid-ocean ridges", ["near continents", "in deep trenches", "at the North Pole"], "New crust forms there."),
    ("About how fast do tectonic plates move?", "a few centimeters per year, about as fast as fingernails grow", ["a few meters per year", "a few kilometers per year", "they do not move"], "Slow but steady."),
    ("What is subduction?", "one plate sinking beneath another into the mantle", ["two plates pulling apart", "plates sliding past", "new crust forming"], "At convergent boundaries."),
    ("What drives plate motion?", "convection in the mantle and the pull of sinking slabs", ["the Moon's gravity", "ocean waves", "wind"], "Internal heat."),
    ("What do magnetic stripes on the seafloor record?", "flips in Earth's magnetic field as new rock cooled", ["ocean temperature", "earthquakes", "fish migrations"], "Paleomagnetism."),
    ("Who proposed continental drift in 1912?", "Alfred Wegener", ["Charles Darwin", "Isaac Newton", "Albert Einstein"], "Later explained by plate tectonics."),
])
B5 = bank([
    ("Wegener's idea was rejected at first. What evidence later convinced scientists?", "seafloor spreading and magnetic stripes found in the 1950s–60s", ["a single fossil", "a map of coastlines only", "a vote"], "Mechanism and data."),
    ("A scientist drills seafloor cores at increasing distances from a ridge. What should the sediment show?", "thicker, older sediment farther from the ridge", ["the same thickness everywhere", "thinner sediment farther away", "no sediment near continents"], "Time to accumulate."),
    ("The Atlantic Ocean is widening at about 2.5 cm per year. What will happen over millions of years?", "Europe and North America will move farther apart.", ["The ocean will disappear soon.", "The continents will merge next year.", "Nothing will change."], "Prediction."),
    ("Why are there no seafloor rocks as old as many continental rocks?", "Old seafloor has already been subducted.", ["Seafloor never forms.", "Old seafloor floats away.", "Scientists cannot date seafloor."], "Recycling."),
    ("How do GPS measurements strengthen plate tectonics?", "They directly measure plates moving today at predicted rates.", ["They show plates are still.", "They measure fossils.", "They only measure weather."], "Modern evidence."),
])


def body():
    think = ("<p><b>Plates move, so crust is made, moved and recycled.</b></p>"
             "<ul><li>New oceanic crust forms at mid-ocean ridges and gets older with distance. Spreading rate = distance ÷ age.</li>"
             "<li>Oceanic crust sinks at subduction zones, so it is never older than about 180 million years. Light continental crust stays, so it can be billions of years old.</li>"
             "<li>Evidence: matching fossils and rocks, magnetic stripes, seafloor ages and GPS.</li></ul>")
    ex = [("Rock 500 km from the ridge is 20 million years old. Rate?", ["5 × 10<sup>7</sup> cm ÷ 2 × 10<sup>7</sup> yr"], "2.5 cm per year"),
          ("Where is the oldest seafloor?", ["Farthest from the ridge"], "near trenches and continental edges")]
    mist = ["Thinking the oldest seafloor is at the ridge.", "Thinking oceanic crust is as old as Earth.", "Thinking plates move meters per year."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Moving plates", B1 + [(g_ev, 6), (g_bnd, 6)]),
        ("Plate boundaries", [(g_bnd, 6), (g_ages, 6), (g_rate, 8)]),
        ("Seafloor spreading", [(g_rate, 16), (g_ages, 4)]),
        ("Crust ages", [(g_rate, 10), (g_ev, 6), (g_ages, 4)]),
        ("Evaluating evidence", B5 + [(g_rate, 10), (g_ages, 5)]),
    ])
    make("earth-and-space-science", "plate-tectonics-and-crust-age", 5, "HS-ESS1-5",
         "Evaluate evidence of the past and current movements of continental and oceanic crust and the theory of plate tectonics to explain the ages of crustal rocks.",
         "Plate Tectonics and the Age of the Crust",
         "Plate Tectonics Worksheets: Seafloor Spreading, Crust Ages and Boundaries (Earth Science)",
         "Plate Tectonics",
         "Free high school Earth and space science worksheets on plate tectonics (NGSS HS-ESS1-5): seafloor spreading rates, crust ages, magnetic stripes, plate boundaries and evidence for drift. 100 questions with answers.",
         "Seafloor is young; continents are old.",
         "New crust forms at ridges and is recycled at trenches; light continental crust stays.",
         body(),
         [("Why is seafloor younger than continents?", "Oceanic crust forms at ridges and sinks back into the mantle at subduction zones within about 200 million years, but light continental crust is not subducted."),
          ("How do you find a seafloor spreading rate?", "Divide the distance from the ridge by the age of the rock, converting km to cm and million years to years."),
          ("What is the evidence for plate tectonics?", "Matching fossils and rocks across oceans, symmetric magnetic stripes, seafloor ages that increase away from ridges, and GPS measurements of moving plates.")],
         sets)


if __name__ == "__main__":
    main()
