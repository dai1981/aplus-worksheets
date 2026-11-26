# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Fossils and Past Environments (3-LS4-1)
  python tools/gen_us_science_g3_fossils_and_past_environments.py
Fossils provide evidence about the types of organisms that lived long ago and the environments they lived in:
marine fossils on land show the area was once covered by water, tropical plant fossils in Antarctica show
it was once warm, mammoth fossils show cold grasslands. Kinds of fossils: bones and shells, imprints of
leaves, footprints (trace fossils), insects in amber. Extinct organisms (dinosaurs, mammoths, trilobites).
Assessment boundary: no specific fossil names or dating.
Wrong answers come from real mistakes: "a fossil is the living animal", "fish fossils mean the area is a
lake today", "all fossils are dinosaurs".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, People
from gen_us_science_g4_rock_layers_and_fossils import layers, FOSSIL

U = Unit(30109)
R = U.R
P = People(R)

# (fossil found, place found today, what the place was like long ago, wrong guesses)
FINDS = [("fossil seashells", "a desert in Utah", "covered by a shallow ocean", ["a snowy mountain top", "a dry desert just like today", "a thick rain forest"]),
         ("fossil palm leaves", "Antarctica", "warm enough for palm trees to grow", ["always covered in ice", "the bottom of a deep ocean", "a dry desert"]),
         ("fossil fish", "a hillside in Wyoming", "covered by a lake", ["a dry desert", "a glacier", "a volcano"]),
         ("fossil coral", "a field in Ohio", "covered by a warm, shallow sea", ["a cold, icy land", "a dry desert", "a high mountain"]),
         ("a woolly mammoth fossil", "Alaska", "a cold, grassy land where large hairy animals lived", ["a warm ocean", "a tropical rain forest", "a coral reef"]),
         ("fossil ferns", "a coal mine in Pennsylvania", "a warm, wet swamp with many plants", ["a dry desert", "a frozen land", "the deep ocean"]),
         ("a fossil whale", "a desert in Egypt", "covered by ocean", ["always a dry desert", "a snowy forest", "a mountain lake"]),
         ("fossil shark teeth", "a field in North Carolina", "covered by ocean", ["a dry desert", "a pine forest", "a cold mountain"]),
         ("dinosaur footprints", "rock beside a river in Texas", "muddy land where dinosaurs walked", ["the deep ocean", "a glacier", "a coral reef"]),
         ("fossil clams", "the top of a mountain", "under the ocean before the mountain was pushed up", ["always a mountain top", "a dry desert", "a forest"])]


def g_find():
    f, place, was, w = R.choice(FINDS)
    p = P.next()
    return item("%s reads that scientists found %s in %s. What was this place like long ago?" % (p[0], f, place), "It was %s." % was, ["It was %s." % x for x in w],
                "%s are evidence that the area was %s." % (f[0].upper() + f[1:], was))


KINDS = [("A leaf pressed into mud left its shape in the rock.", "an imprint fossil"), ("A dinosaur walked in mud, and its tracks turned to stone.", "a trace fossil (footprint)"),
         ("An insect was trapped in sticky tree sap that hardened.", "an insect in amber"), ("The bones of a dinosaur slowly turned to rock.", "a body fossil (bones)"),
         ("A clam's hard shell was buried and turned to stone.", "a body fossil (shell)"), ("A worm made tunnels in mud that hardened into rock.", "a trace fossil (burrow)"),
         ("A fern's shape was left in a thin layer of rock.", "an imprint fossil"), ("A woolly mammoth froze in ice and was found thousands of years later.", "a frozen body fossil")]


def g_kind():
    t, a = R.choice(KINDS)
    w = list(dict.fromkeys(k for _, k in KINDS if k != a and k.split(" (")[0] != a.split(" (")[0]))
    p = P.next()
    return item("%s reads a fossil card: “%s” What kind of fossil is this?" % (p[0], t), a, R.sample(w, 3), "%s" % a[0].upper() + a[1:] + ".")


EXTINCT = ["Tyrannosaurus rex", "a woolly mammoth", "a trilobite", "a saber-toothed cat", "a dodo bird", "a Stegosaurus", "a mastodon", "a passenger pigeon"]
ALIVE = ["an elephant", "a crocodile", "a horseshoe crab", "a shark", "a sea turtle", "a dragonfly", "a cockroach", "a ginkgo tree"]


def g_ext():
    k = R.choice(["ext", "alive", "rel"])
    p = P.next()
    if k == "ext":
        return item("%s visits a fossil museum. Which of these is extinct (no longer alive anywhere)?" % p[0], R.choice(EXTINCT), R.sample(ALIVE, 3),
                    "Extinct organisms are known only from fossils and records.")
    if k == "alive":
        return item("%s sees fossils of these organisms. Which one still has relatives that look very similar living today?" % p[0], R.choice(ALIVE), R.sample(EXTINCT, 3),
                    "Some living things, like sharks and crocodiles, look a lot like their fossils.")
    pairs = [("a woolly mammoth", "an elephant"), ("a saber-toothed cat", "a lion"), ("a mastodon", "an elephant"), ("an ancient horse fossil", "a modern horse"), ("a giant sloth", "a tree sloth")]
    a, b = R.choice(pairs)
    others = [x for x in ["a shark", "a frog", "a snake", "an eagle", "a beetle", "a lion", "an elephant", "a modern horse", "a tree sloth"] if x != b]
    return item("%s studies a fossil of %s. It looks most like which animal living today?" % (p[0], a.replace("an ancient horse fossil", "an ancient horse")),
                b, R.sample([x for x in others if x not in (b,)], 3), "%s and %s have similar body parts." % (a[0].upper() + a[1:], b))


def g_layer():
    n = R.choice([3, 4])
    fs = [None] * n
    pos = R.sample(range(n), 2)
    sea = R.choice([f for f in FOSSIL if FOSSIL[f] in ("ocean", "water")])
    land = R.choice([f for f in FOSSIL if FOSSIL[f] == "land"])
    fs[pos[0]], fs[pos[1]] = sea, land
    low = min(pos)
    first = fs[low]
    env_first = "water" if first == sea else "land"
    env_next = "land" if env_first == "water" else "water"
    p = P.next()
    seq = {"water": "It was covered by water first, and later it became dry land.", "land": "It was dry land first, and later it was covered by water."}
    return item(fig(layers(fs)) + "%s finds a %s fossil and a %s fossil in these rock layers. What happened to this place over time?" % (p[0], sea, land),
                seq[env_first], [seq[env_next], "It has always been the same.", "Both fossils formed at the same time."],
                "The lower fossil (%s) is older. Water animals mean water; land plants or footprints mean land." % first)


B1 = bank([
    ("What is a fossil?", "the remains or traces of a living thing from long ago, preserved in rock, ice or amber", ["a living animal", "a shiny rock with no life in it", "a kind of crystal"],
     "Fossils tell us about life long ago."),
    ("What can fossils tell us?", "what kinds of living things lived long ago and what their environment was like", ["what the weather will be tomorrow", "how old you are", "what color dinosaurs were for sure"],
     "Fossils are evidence of the past."),
    ("What does extinct mean?", "no longer living anywhere on Earth", ["sleeping for the winter", "very large", "living only in zoos"], "Dinosaurs are extinct."),
    ("Which body parts most often become fossils?", "hard parts like bones, teeth and shells", ["soft skin", "eyes", "feathers only"], "Hard parts last longer."),
    ("A fossil footprint shows", "that an animal walked there long ago", ["that the animal is still alive", "the color of the animal", "what the animal ate for lunch"],
     "Trace fossils show what animals did."),
    ("Fossils of ocean animals are found in a desert. What does this show?", "The desert was once covered by ocean water.", ["Ocean animals lived in the desert.", "Someone dropped them there.", "The desert is under water today."],
     "Environments change over a long time."),
    ("Where do most fossils form?", "in layers of mud and sand that slowly turn to rock", ["in the air", "on top of mountains of ice only", "inside volcanoes"],
     "Buried remains are protected and slowly turn to stone."),
    ("Why are there no dinosaurs today?", "They became extinct long ago.", ["They are hiding.", "They turned into rocks while alive.", "They live only in deserts."],
     "We know about them from fossils."),
])
B5 = bank([
    ("Ava finds a rock with a leaf shape in it. What should she conclude?", "A plant lived here long ago.", ["The rock is alive.", "Leaves grow on rocks.", "It snowed here yesterday."],
     "The imprint is evidence of a plant."),
    ("Leo finds fossil coral in a cold place far from the sea. Coral lives in warm, shallow seas today. What does this suggest?", "The place was once a warm, shallow sea.", ["Coral lives in cold mountains.", "The fossil grew there last year.", "The place was always cold."],
     "Compare fossils to living relatives to learn about past environments."),
    ("Mia makes a model fossil by pressing a shell into clay. What kind of fossil does this model?", "an imprint (mold) fossil", ["amber", "a frozen fossil", "a living shell"],
     "The shape of the shell is left behind."),
    ("Scientists find mammoth fossils with thick fur in Alaska. What does this tell them?", "The area was cold when mammoths lived there.", ["The area was a hot desert.", "Mammoths lived in the ocean.", "Mammoths are alive today."],
     "Thick fur helps in cold places."),
    ("Why do scientists compare fossils with plants and animals living today?", "to learn how the fossil organisms lived and what their environment was like", ["to make the fossils alive", "to find gold", "to measure the weather"],
     "Similar living organisms give clues."),
])


def body():
    think = ("<p><b>Fossils</b> are the remains or traces of living things from long ago: bones, shells, leaf prints, footprints and insects in amber.</p>"
             "<p>Fossils are <b>evidence</b> of what lived long ago and what the <b>environment</b> was like. Seashells in a desert mean the desert was once ocean. "
             "Palm leaves in Antarctica mean it was once warm. Many fossils are of <b>extinct</b> organisms, like dinosaurs and woolly mammoths.</p>"
             + figure(layers(["clam", None, "fern"]), "A clam fossil in a lower layer and a fern in a higher layer: the area was ocean, then land."))
    ex = [("Fossil fish are found on a dry hill. What was the hill like long ago?", ["Fish live in water."], "It was under water."),
          ("Is a woolly mammoth extinct?", ["None are alive today."], "Yes.")]
    mist = ["Thinking the fossil environment is the same as the environment today.",
            "Thinking all fossils are dinosaurs.",
            "Thinking a fossil is the living animal."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What fossils are", B1 + [(g_kind, 6), (g_ext, 6)]),
        ("Kinds of fossils", [(g_kind, 8), (g_ext, 12)]),
        ("Fossils and past environments", [(g_find, 14), (g_layer, 6)]),
        ("Fossils in rock layers", [(g_layer, 12), (g_find, 8)]),
        ("Using fossil evidence", B5 + [g_find, g_layer, g_ext, g_kind]),
    ])
    make("grade-3", "fossils-and-past-environments", 9, "3-LS4-1",
         "Analyze and interpret data from fossils to provide evidence of the organisms and the environments in which they lived long ago.",
         "Fossils and Past Environments",
         "Grade 3 Fossils Worksheets: What Fossils Tell Us About Life Long Ago",
         "Fossils",
         "Free Grade 3 science worksheets on fossils (NGSS 3-LS4-1): kinds of fossils, extinct organisms, and how fossils show what past environments were like, with rock layer pictures. 100 practice questions with answers.",
         "Fossils show what lived long ago and where.",
         "Seashells in a desert mean the land was once under the sea. Fossils are evidence of past life and past environments.",
         body(),
         [("What is a fossil?", "A fossil is the remains or traces of a living thing from long ago, like a bone, shell, leaf print or footprint."),
          ("How do fossils tell us about past environments?", "If ocean fossils are found on land, the land was once under water. If palm fossils are found in a cold place, it was once warm."),
          ("What does extinct mean?", "An extinct organism no longer lives anywhere on Earth, like dinosaurs and woolly mammoths.")],
         sets)


if __name__ == "__main__":
    main()
