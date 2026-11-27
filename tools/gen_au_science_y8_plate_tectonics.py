# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U03: the theory of plate tectonics - Earth's layers, evidence for moving plates
(Gondwana fossils, matching coastlines, sea-floor spreading), plate boundaries and the landforms and events they cause.
  python tools/gen_au_science_y8_plate_tectonics.py
Own questions on the Indo-Australian Plate, Gondwana, New Zealand and plate speeds, plus the US Grade 7 plate tectonics and
earth-surface makers and the UK Year 8 Earth-structure makers with Australian names.
Wrong answers come from real mistakes: thinking plates float on liquid magma, thinking continents move quickly, and mixing up
which boundary forms mountains and which forms new sea floor.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

PT = "gen_us_science_g7_plate_tectonics"
SE = "gen_us_science_g7_shaping_earths_surface"
RK = "gen_uk_science_y8_rocks_and_the_rock_cycle"
p_bound = src(PT, "g_bound")
p_age = src(PT, "g_age")
p_evid = src(PT, "g_evid")
p_expl = src(PT, "g_explain")
p_b1 = src.B(PT, "B1")
p_b5 = src.B(PT, "B5")
s_evid = src(SE, "g_evid")
s_b1 = src.B(SE, "B1")
r_layer = src(RK, "g_layer")

BD = [("convergent (plates move together)", ["fold mountains such as the Himalayas", "deep ocean trenches", "volcanoes along the Andes", "the Southern Alps of New Zealand pushing up"]),
      ("divergent (plates move apart)", ["mid-ocean ridges", "new sea floor", "rift valleys in East Africa", "Iceland splitting slowly apart"]),
      ("transform (plates slide past each other)", ["the San Andreas Fault", "the Alpine Fault in New Zealand", "sudden earthquakes along a fault line"])]


def g_bd():
    k, fs = R.choice(BD)
    f = R.choice(fs)
    if R.random() < 0.5:
        return tq("Which kind of plate boundary forms %s?" % f, k, [x[0] for x in BD if x[0] != k] + ["no boundary: it is far from any plate edge"],
                  "Convergent: plates collide. Divergent: plates separate. Transform: plates slide past.")
    w = [R.choice(x[1]) for x in BD if x[0] != k] + ["a flat desert in the middle of a plate"]
    return tq("Which feature is most likely at a %s boundary?" % k.split(" (")[0], f, w, "%s: %s." % (k, f))


def g_speed():
    from au_sci import once
    v = R.choice([2, 3, 5, 6, 7, 10])
    yrs = R.choice([100, 1000, 10000, 100000, 1000000])
    if not once(("sp", v, yrs)):
        return None
    cm = v * yrs
    def fmt(c):
        if c >= 100000:
            return "%g km" % (c / 100000)
        if c >= 100:
            return "%g m" % (c / 100)
        return "%d cm" % c
    w = {fmt(cm * 10), fmt(cm / 10), fmt(cm * 100)} - {fmt(cm)}
    w = sorted(w)
    if len(w) < 3:
        return None
    return tq("A plate moves about %d cm per year. About how far does it move in %s years?" % (v, "{:,}".format(yrs)), fmt(cm), w[:3],
              "%d cm × %s = %s cm = %s." % (v, "{:,}".format(yrs), "{:,}".format(cm), fmt(cm)))


LAY = [("crust", "the thin, solid outer layer we live on"), ("mantle", "the thick layer of hot rock that flows very slowly"),
       ("outer core", "the layer of liquid iron and nickel"), ("inner core", "the solid centre of iron and nickel")]


def g_lay():
    n, d = R.choice(LAY)
    if R.random() < 0.5:
        return tq("Which layer of Earth is %s?" % d, "the " + n, ["the " + x[0] for x in LAY if x[0] != n], "From outside in: crust, mantle, outer core, inner core.")
    return tq("What is Earth's %s like?" % n, d, [x[1] for x in LAY if x[0] != n], "From outside in: crust, mantle, outer core, inner core.")


POOL1 = pool(R, [
    ("What is the theory of plate tectonics?", "Earth's crust and upper mantle are broken into large plates that move slowly.", ["Earth's crust is one solid piece.", "Continents move quickly every year.", "Plates float on liquid lava."], "Plates move a few centimetres a year."),
    ("Which plate is Australia on?", "the Indo-Australian Plate (the Australian Plate)", ["the Pacific Plate", "the Eurasian Plate", "the Antarctic Plate only"], "It moves north about 7 cm a year."),
    ("In which direction is the Australian Plate moving?", "north (slightly north-east)", ["south", "west", "it is not moving"], "Australia moves towards Asia."),
    ("What was Gondwana?", "a supercontinent that included Australia, Antarctica, South America, Africa and India", ["a type of rock", "an ancient ocean", "a volcano in Victoria"], "It broke apart over millions of years."),
    ("Fossils of the plant Glossopteris are found in Australia, Antarctica, India and South America. What does this suggest?", "These continents were once joined.", ["Seeds were blown across oceans.", "The plant grew everywhere on Earth.", "The fossils were moved by people."], "This was key evidence for continental drift."),
    ("Who first proposed continental drift in 1912?", "Alfred Wegener", ["Isaac Newton", "Charles Darwin", "Albert Einstein"], "His idea was not widely accepted until sea-floor evidence was found."),
    ("Why did many scientists reject Wegener's idea at first?", "He could not explain what force moved the continents.", ["He had no fossil evidence.", "He said the Earth was flat.", "He used no maps."], "Convection in the mantle was later suggested."),
    ("What moves the plates?", "slow convection currents in the mantle and the pull of sinking plates", ["wind", "ocean waves", "the Moon"], "Hot rock rises and cooler rock sinks over millions of years."),
    ("Why does Australia have fewer large earthquakes and volcanoes than New Zealand?", "Australia is in the middle of a plate; New Zealand sits on a plate boundary.", ["Australia is bigger.", "Australia has no crust.", "New Zealand is colder."], "Most earthquakes happen at boundaries."),
    ("What forms where an ocean plate sinks under another plate?", "a deep ocean trench and often volcanoes", ["a mid-ocean ridge", "a flat plain", "a coral reef"], "This is called subduction."),
    ("What is the evidence from rocks on the sea floor near mid-ocean ridges?", "The rock is youngest at the ridge and older further away.", ["The rock is oldest at the ridge.", "All the rock is the same age.", "There is no rock there."], "New sea floor forms at the ridge."),
    ("Why do South America and Africa look like they fit together?", "They were once joined and have moved apart.", ["They are the same shape by chance only.", "They are on the same plate today.", "People drew the maps that way."], "Matching rocks and fossils support this."),
])
POOL5 = pool(R, [
    ("Mia measures the distance between two GPS stations across a boundary: it grows 3 cm each year. What kind of boundary is it?", "divergent", ["convergent", "transform", "no boundary"], "Moving apart means divergent."),
    ("Jack plots earthquakes on a world map. Where are most of them?", "along plate boundaries", ["in the middle of plates", "only in deserts", "randomly everywhere"], "The pattern shows where plates meet."),
    ("Ruby models convection by heating water with food colouring. What does the moving colour represent?", "convection currents in the mantle", ["ocean waves", "wind", "the inner core spinning"], "Warm material rises and cool material sinks."),
    ("Kai uses a jigsaw of continents to show Gondwana. What is a limitation of his model?", "Coastlines have changed, and the real fit uses the edges of the continental shelves.", ["It shows plates moving too slowly.", "There are no limitations.", "Continents never fit together."], "Models simplify reality."),
    ("A volcano erupts in Indonesia. Why is Indonesia volcanic but most of Australia is not?", "Indonesia is near where the Australian Plate sinks under the Eurasian Plate.", ["Indonesia is closer to the Sun.", "Australia has no rocks.", "Indonesia is on top of the inner core."], "Subduction zones have many volcanoes."),
    ("Why do scientists keep revising the theory of plate tectonics?", "New evidence from GPS, sea-floor mapping and earthquakes improves it.", ["It has been proven wrong.", "Plates change direction every year.", "Old evidence must be deleted."], "Scientific theories develop with new evidence."),
])


def main():
    sets = U.sets([
        ("Earth's layers", [(g_lay, 8), (r_layer, 6), (POOL1, 4), (p_b1, 2)]),
        ("Evidence for moving plates", [(POOL1, 8), (p_evid, 3), (p_expl, 3), (p_age, 3), (p_b1, 3)]),
        ("Plate boundaries", [(g_bd, 10), (p_bound, 6), (s_evid, 4)]),
        ("How fast plates move", [(g_speed, 10), (POOL1, 0), (p_b5, 4), (s_b1, 4), (g_bd, 2)]),
        ("Models and investigations", [(POOL5, 6), (g_bd, 3), (g_speed, 3), (s_evid, 1), (p_bound, 3), (g_lay, 2), (s_b1, 2)]),
    ])
    make_au(YEAR, "plate-tectonics", SORT, "AC9S8U03", "Earth and space sciences",
            "Explain how the theory of plate tectonics accounts for the formation of landforms and geological events, and describe the "
            "evidence for it (summary of the Australian Curriculum v9.0 Science content description).",
            "Plate Tectonics", "Plate tectonics",
            "Free Year 8 science worksheets on plate tectonics: Earth's layers, Gondwana and evidence for continental drift, plate boundaries, "
            "earthquakes and volcanoes, and how fast the Australian Plate moves. 100 questions with answers.",
            "Earth's surface is made of moving plates.", "Plates move a few centimetres a year; most earthquakes and volcanoes occur at their boundaries.",
            "<p><b>Earth's crust and upper mantle are broken into plates that move slowly over the hotter mantle.</b></p><ul>"
            "<li>Layers: crust, mantle, outer core (liquid), inner core (solid).</li>"
            "<li>Evidence: matching coastlines, Gondwana fossils such as Glossopteris, rock ages on the sea floor, GPS measurements.</li>"
            "<li>Boundaries: convergent (mountains, trenches, volcanoes), divergent (ridges, new sea floor), transform (earthquakes along faults).</li></ul>",
            [("Plates move apart at a mid-ocean ridge. Boundary?", ["moving apart"], "divergent"),
             ("7 cm per year for 1 000 years?", ["7 × 1000 = 7000 cm"], "70 m")],
            ["Thinking plates float on liquid magma (the mantle is mostly solid rock that flows very slowly).", "Thinking continents move quickly.",
             "Mixing up convergent boundaries (mountains, trenches) and divergent boundaries (new sea floor)."],
            [("What evidence supports plate tectonics?", "Matching coastlines and rocks, the same fossils on different continents, younger sea floor near mid-ocean ridges, earthquake patterns and GPS measurements."),
             ("Why does Australia have few volcanoes?", "Australia sits near the middle of the Indo-Australian Plate, far from the boundaries where most volcanoes and earthquakes happen."),
             ("What was Gondwana?", "A supercontinent that included Australia, Antarctica, South America, Africa and India. It began breaking up about 180 million years ago.")],
            sets, allow=("america", "india"))


if __name__ == "__main__":
    main()
