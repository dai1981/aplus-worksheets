# -*- coding: utf-8 -*-
"""
UK Year 6 science: Fossils (Evolution and inheritance)
  python tools/gen_uk_science_y6_fossils.py
How fossils form, body and trace fossils, rock layers (deeper is older), what fossils tell us about the past,
time spans in millions of years, and Mary Anning.
Wrong answers come from real mistakes: "fossils form in a few years", "the top layer is the oldest",
"a footprint cannot be a fossil", "humans and dinosaurs lived at the same time".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig
from uk_sci_pics import layers
from sci_phys import uniq

U = Unit(61607)
R = U.R
P = People(R)

STEPS = ["An animal dies and sinks to the bottom of a sea or lake.", "Its body is quickly covered by mud or sand.",
         "The soft parts rot away, leaving bones or shell.", "More layers build up and press the sediment into rock.",
         "Minerals slowly replace the bones, turning them to stone.", "Millions of years later, the rock wears away and the fossil is found."]


def g_step():
    i = R.randrange(len(STEPS) - 1)
    k = R.random() < 0.5
    if not once(("st", i, k)):
        return None
    if k:
        a = STEPS[i + 1]
        return item("How does a fossil form? This happens: \"%s\" What happens next?" % STEPS[i], a, R.sample([x for x in STEPS if x not in (a, STEPS[i])], 3),
                    "Order: dies → covered → soft parts rot → layers press → minerals replace → found.")
    a = STEPS[i]
    return item("How does a fossil form? This happens: \"%s\" What happened just before?" % STEPS[i + 1], a, R.sample([x for x in STEPS if x not in (a, STEPS[i + 1])], 3),
                "Order: dies → covered → soft parts rot → layers press → minerals replace → found.")


FOS = {"trilobite": 500, "coral": 430, "fern": 350, "ammonite": 190, "belemnite": 175, "dinosaur bone": 150, "shark tooth": 90, "sea urchin": 80, "mammoth tooth": 1}
ROCK = ["sandstone", "mudstone", "limestone", "chalk", "shale", "clay"]


def g_layer():
    n = R.choice([4, 5])
    fs = sorted(R.sample(sorted(FOS), n), key=lambda f: FOS[f])
    rk = R.sample(ROCK, n)
    k = R.choice(["old", "young", "pair"])
    if not once(("la", tuple(fs), k)):
        return None
    pic = fig(layers([(r, f) for r, f in zip(rk, fs)], "rock layers with fossils, newest at the top"))
    intro = pic + "These rock layers have not been disturbed. "
    if k == "old":
        return item(intro + "Which fossil is the oldest?", fs[-1], R.sample(fs[:-1], 3), "The bottom layer formed first, so it is the oldest.")
    if k == "young":
        return item(intro + "Which fossil is the youngest?", fs[0], R.sample(fs[1:], 3), "The top layer formed last, so it is the youngest.")
    i, j = sorted(R.sample(range(n), 2))
    return item(intro + "Which is older: the %s or the %s?" % (fs[i], fs[j]), "the %s" % fs[j], ["the %s" % fs[i], "They are the same age.", "You cannot tell from rock layers."],
                "The %s is in a deeper layer, so it is older." % fs[j])


TYPE = [("a dinosaur's footprint in rock", "trace fossil"), ("a worm's burrow in rock", "trace fossil"), ("fossilised dinosaur dung", "trace fossil"),
        ("a dinosaur egg's broken shell pattern left in mud", "trace fossil"), ("an ammonite shell turned to stone", "body fossil"),
        ("a fossilised fish skeleton", "body fossil"), ("a shark tooth in chalk", "body fossil"), ("an insect trapped in amber", "body fossil"),
        ("a leaf print in shale", "body fossil")]


def g_type():
    t, a = R.choice(TYPE)
    if not once(("ty", t)):
        return None
    return item("Is %s a body fossil or a trace fossil?" % t, a, ["trace fossil" if a == "body fossil" else "body fossil", "not a fossil at all", "a living thing"],
                "Body fossils are parts of the living thing; trace fossils are signs it left behind, such as footprints.")


CLUE = [("Fossils of fish and shells are found on top of a mountain.", "The rock there was once under the sea."),
        ("Fossils of tree ferns are found in Antarctica.", "Antarctica was once much warmer."),
        ("A fossil skull has long, sharp, pointed teeth.", "The animal probably ate meat."),
        ("A fossil skull has flat, ridged teeth.", "The animal probably ate plants."),
        ("Fossil footprints are far apart.", "The animal was probably running."),
        ("Coral fossils are found in rocks in Yorkshire.", "The area was once a warm, shallow sea."),
        ("Woolly mammoth bones are found in London clay.", "Britain was once much colder.")]


def g_clue():
    c, a = R.choice(CLUE)
    if not once(("cl", c)):
        return None
    return item("%s What does this tell scientists?" % c, a, R.sample([x[1] for x in CLUE if x[1] != a], 3), "Fossils are evidence of how living things and places were in the past.")


AGES = [("the first fish", 530), ("the first land plants", 470), ("the first dinosaurs", 230), ("the first flowering plants", 130),
        ("the end of the dinosaurs", 66), ("the first ammonites", 400), ("the last ammonites", 66), ("the first mammals", 200)]


def g_age():
    a, b = R.sample(AGES, 2)
    if a[1] == b[1]:
        return None
    o, y = (a, b) if a[1] > b[1] else (b, a)
    k = R.random() < 0.5
    if not once(("ag", o[0], y[0], k)):
        return None
    if k:
        d = o[1] - y[1]
        g = "%d million years" % d
        return item("%s: about %d million years ago. %s: about %d million years ago. How long was there between them?" % (o[0][0].upper() + o[0][1:], o[1], y[0][0].upper() + y[0][1:], y[1]), g,
                    uniq(g, ["%s million years" % format(o[1] + y[1], ","), "%d million years" % o[1], "%d million years" % (d + 100), "%d years" % d]), "%d − %d = %d million years." % (o[1], y[1], d))
    return item("Which came first: %s (about %d million years ago) or %s (about %d million years ago)?" % (a[0], a[1], b[0], b[1]), o[0], [y[0], "They happened at the same time.", "It cannot be known."],
                "The bigger number of millions of years ago is earlier.")


B1 = bank([
    ("What is a fossil?", "the remains or traces of a living thing from long ago, preserved in rock", ["any old stone", "a living animal that hides in rock", "a type of crystal"], "Usually millions of years old."),
    ("How long do most fossils take to form?", "millions of years", ["a few days", "a few years", "about a hundred years"], "Rock forms very slowly."),
    ("Which kind of rock are most fossils found in?", "sedimentary rock", ["igneous rock", "rock made from lava", "rock from the Moon"], "Layers of sediment bury the remains."),
    ("What is a scientist who studies fossils called?", "a palaeontologist", ["an astronaut", "a dentist", "a meteorologist"], "Palaeo means ancient."),
    ("Who found the first complete ichthyosaur skeleton at Lyme Regis in the early 1800s?", "Mary Anning", ["Charles Darwin", "Alfred Wallace", "Rosalind Franklin"], "She found fossils on the Jurassic Coast."),
    ("Why do we rarely find fossils of jellyfish?", "They have no hard parts, so they usually rot away.", ["They never lived long ago.", "They are too big.", "They live on land."], "Hard parts fossilise best."),
    ("In undisturbed rock layers, where are the oldest fossils?", "in the bottom layers", ["in the top layers", "in the middle only", "they are all the same age"], "New layers form on top."),
    ("Did people live at the same time as the dinosaurs (other than birds)?", "No. The dinosaurs died out about 66 million years before humans appeared.", ["Yes, they lived together.", "Yes, in Britain only.", "No, people came first."], "Look at the timeline."),
])
B5 = bank([
    ("How do fossils show that living things have changed over time?", "Older rocks contain different living things from those alive today.", ["All fossils look exactly like animals today.", "Fossils are always the same age.", "Fossils change shape each year."], "Evidence for evolution."),
    ("Why are fossils of the same kind of animal found in South America and Africa?", "The continents were once joined together.", ["The animal swam across.", "Someone moved the fossils.", "Fossils grow on their own."], "Continents move."),
    ("A fossil is found in rock made from sand. What does this suggest about the place it lived?", "It was probably a beach, river or desert with sand.", ["It was always a mountain top.", "It lived in space.", "It lived in lava."], "Rock tells us the environment."),
    ("Why should fossil hunters on the Jurassic Coast stay away from cliffs?", "Cliffs can fall without warning.", ["Cliffs have no fossils.", "Fossils only exist in museums.", "Cliffs are made of glass."], "Safety on the coast."),
    ("Why was Mary Anning not given full credit for her finds at the time?", "Women were not allowed to join scientific societies then.", ["She did not find any fossils.", "She lived after Darwin.", "Her fossils were fake."], "History of science."),
])


def body():
    think = ("<p><b>Fossils are the remains or traces of living things preserved in rock.</b></p>"
             "<ul><li>A body is buried quickly in mud or sand; soft parts rot; layers press into rock; minerals replace the bones over millions of years.</li>"
             "<li>Body fossils are bones, shells and teeth; trace fossils are footprints, burrows and dung.</li>"
             "<li>In undisturbed layers, deeper rock is older. Fossils show that living things and places have changed over time.</li></ul>")
    ex = [("Fossil A is in the top layer, fossil B at the bottom. Older?", ["New layers form on top"], "fossil B"),
          ("230 and 66 million years ago. Difference?", ["230 − 66"], "164 million years")]
    mist = ["Thinking the top layer is the oldest.", "Thinking a footprint cannot be a fossil.", "Thinking people and dinosaurs lived at the same time."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What fossils are", B1 + [(g_type, 8), (g_step, 4)]),
        ("How fossils form", [(g_step, 6), (g_type, 1), (g_clue, 7), (g_age, 6)]),
        ("Rock layers", [(g_layer, 16), (g_age, 4)]),
        ("Fossils as evidence", [(g_age, 12), (g_layer, 8)]),
        ("Thinking like a palaeontologist", B5 + [(g_layer, 8), (g_age, 7)]),
    ])
    make_uk(6, "fossils", 7, "Evolution and inheritance",
            "Recognise that living things have changed over time and that fossils provide information about living things that inhabited the Earth millions of years ago.",
            "Fossils",
            "Year 6 Science: Fossils Worksheets (How Fossils Form, Rock Layers, Mary Anning)",
            "Fossils",
            "Free Year 6 science worksheets on fossils: how fossils form, body and trace fossils, rock layers, what fossils tell us, timelines and Mary Anning. 100 questions with answers.",
            "Fossils are clues from millions of years ago.",
            "Deeper rock layers are older; fossils show how life has changed.",
            body(),
            [("How are fossils formed?", "A living thing is buried quickly in mud or sand. Its soft parts rot, the sediment hardens into rock, and over millions of years minerals replace the hard parts."),
             ("How do we know which fossils are older?", "In undisturbed rock, layers build up on top of each other, so fossils in deeper layers are older than those above."),
             ("Who was Mary Anning?", "A fossil hunter from Lyme Regis in Dorset who, in the early 1800s, found ichthyosaur and plesiosaur skeletons that changed how scientists thought about the past.")],
            sets)


if __name__ == "__main__":
    main()
