# -*- coding: utf-8 -*-
"""
UK Year 3 science: Comparing and Grouping Rocks (Rocks)
  python tools/gen_uk_science_y3_comparing_and_grouping_rocks.py
Comparing and grouping rocks by appearance and simple physical properties (grains or crystals, layers, hardness,
whether water soaks in), igneous, sedimentary and metamorphic rocks, natural and man-made materials, and why rocks
are chosen for different uses. Investigation results: scratch tests and water-drop tests.
Wrong answers come from real mistakes: "all rocks are hard", "brick and concrete are rocks", "shiny rocks are
always the hardest", "rocks never change".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61307)
R = U.R
P = People(R)

ROCK = {"granite": ("igneous", "hard", "no", "has large crystals of different colours"),
        "basalt": ("igneous", "hard", "no", "is dark with tiny crystals"),
        "pumice": ("igneous", "fairly hard", "yes", "is full of holes and light enough to float"),
        "obsidian": ("igneous", "hard", "no", "is black, glassy and smooth"),
        "sandstone": ("sedimentary", "fairly soft", "yes", "is made of sand grains stuck together"),
        "chalk": ("sedimentary", "soft", "yes", "is white, soft and made of tiny shells"),
        "limestone": ("sedimentary", "fairly soft", "yes", "often has fossil shells in it"),
        "mudstone": ("sedimentary", "soft", "no", "is made of fine mud and crumbles easily"),
        "slate": ("metamorphic", "hard", "no", "splits into thin, flat sheets"),
        "marble": ("metamorphic", "hard", "no", "has swirly patterns and can be polished smooth")}
TYPES = {"igneous": "formed when hot, melted rock cools and hardens", "sedimentary": "formed from layers of sand, mud or shells pressed together",
         "metamorphic": "formed when other rocks are changed by great heat and pressure"}


def g_type():
    r = R.choice(sorted(ROCK))
    t = ROCK[r][0]
    k = R.random() < 0.5
    if k:
        if not once(("ty", r)):
            return None
        return item("Is %s an igneous, sedimentary or metamorphic rock?" % r, t, [x for x in sorted(TYPES) if x != t] + ["a man-made rock"], "%s rock is %s." % (t.capitalize(), TYPES[t]))
    others = [x for x in sorted(ROCK) if ROCK[x][0] != t]
    w = R.sample(others, 3)
    if not once(("tw", r)):
        return None
    o = sorted([r] + w)
    return item("Which of these is %s %s rock: %s or %s?" % ("an" if t[0] in "aeiou" else "a", t, ", ".join(o[:3]), o[3]), r, w, "%s rock is %s." % (t.capitalize(), TYPES[t]))


def g_how():
    t = R.choice(sorted(TYPES))
    k = R.random() < 0.5
    if not once(("hw", t, k)):
        return None
    if k:
        return item("How is %s rock formed?" % t, TYPES[t][7:], [TYPES[x][7:] for x in sorted(TYPES) if x != t] + ["made in factories from clay"], "Igneous: from melted rock. Sedimentary: from layers. Metamorphic: changed by heat and pressure.")
    return item("Which type of rock is %s?" % TYPES[t], t + " rock", [x + " rock" for x in sorted(TYPES) if x != t] + ["man-made rock"], "Igneous: from melted rock. Sedimentary: from layers. Metamorphic: changed by heat and pressure.")


def g_look():
    r = R.choice(sorted(ROCK))
    d = ROCK[r][3]
    if not once(("lk", r)):
        return None
    return item("Which rock %s?" % d, r, R.sample([x for x in sorted(ROCK) if x != r], 3), "Look closely at grains, crystals, holes, layers and colour.")


def g_test():
    who = P.next()[0]
    rs = R.sample(sorted(ROCK), 4)
    perm = [ROCK[r][2] for r in rs]
    scratch = ["no" if r in ("granite", "basalt", "obsidian") else "yes" for r in rs]
    k = R.choice(["perm", "imperm", "scratch", "hard", "roof"])
    if not once(("te", tuple(rs), k)):
        return None
    tab = table(["Rock", "Did a drop of water soak in?", "Could it be scratched with a steel nail?"], [[r, p, s] for r, p, s in zip(rs, perm, scratch)])
    intro = tab + "%s tested four rocks. " % who
    yes_p = [r for r, p in zip(rs, perm) if p == "yes"]
    no_p = [r for r, p in zip(rs, perm) if p == "no"]
    yes_s = [r for r, s in zip(rs, scratch) if s == "yes"]
    no_s = [r for r, s in zip(rs, scratch) if s == "no"]
    if k == "perm":
        if len(yes_p) != 1:
            return None
        return item(intro + "Which rock is permeable (lets water soak in)?", yes_p[0], no_p, "Water soaks into permeable rocks.")
    if k == "imperm":
        if len(no_p) != 1:
            return None
        return item(intro + "Which rock is impermeable (does not let water soak in)?", no_p[0], yes_p, "Water stays on top of impermeable rocks.")
    if k == "scratch":
        if len(yes_s) != 1:
            return None
        return item(intro + "Which rock is the only one that could be scratched with a nail?", yes_s[0], no_s, "Softer rocks can be scratched with a steel nail.")
    if k == "hard":
        if len(no_s) != 1:
            return None
        return item(intro + "Which rock is the only one too hard to scratch with a nail?", no_s[0], yes_s, "Hard rocks cannot be scratched with a nail.")
    good = [r for r, p, s in zip(rs, perm, scratch) if p == "no" and s == "no"]
    bad = [r for r in rs if r not in good]
    if len(good) != 1 or "obsidian" in rs or not once(("path",), 5):
        return None
    return item(intro + "Which rock would be best for a path that gets lots of rain and many feet?", good[0], bad, "It is hard and impermeable, so it does not wear away or soak up water.")


USE = [("slate", "roof tiles", "It is waterproof and splits into thin, flat sheets."), ("granite", "kerbstones and steps", "It is very hard and does not wear away."),
       ("marble", "statues", "It can be carved and polished to look beautiful."), ("chalk", "drawing on pavements", "It is soft, so it rubs off easily."),
       ("limestone", "building walls of old churches", "It is easy to cut into blocks."), ("pumice", "rubbing hard skin off feet", "It is rough and full of tiny holes.")]


def g_use():
    r, u, why = R.choice(USE)
    k = R.random() < 0.5
    if not once(("us", r, k)):
        return None
    if k:
        return item("Why is %s used for %s?" % (r, u), why, R.sample([x[2] for x in USE if x[0] != r], 3), "Rocks are chosen for their properties.")
    return item("Which rock is most often used for %s?" % u, r, R.sample([x[0] for x in USE if x[0] != r], 3), why)


NAT = ["granite", "chalk", "slate", "sandstone", "marble", "basalt", "pebbles on a beach", "a lump of limestone"]
MAN = ["a brick", "concrete", "glass", "a paving slab made of concrete", "a clay flowerpot", "tarmac", "a china mug", "a plastic toy rock"]


def g_man():
    k = R.random() < 0.5
    if k:
        a = R.choice(MAN)
        w = R.sample(NAT, 3)
        if not once(("mm", a)):
            return None
        o = sorted([a] + w)
        return item("Which of these is man-made, not a natural rock: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Bricks, concrete and glass are made by people; rocks form naturally.")
    a = R.choice(NAT)
    w = R.sample(MAN, 3)
    if not once(("mn", a)):
        return None
    o = sorted([a] + w)
    return item("Which of these is a natural rock: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Natural rocks form in the Earth over a very long time.")


B1 = bank([
    ("What are the three main types of rock?", "igneous, sedimentary and metamorphic", ["hard, soft and wet", "sand, mud and soil", "brick, glass and concrete"], "Named by how they formed."),
    ("What does permeable mean?", "lets water soak into it", ["very hard", "very shiny", "floats on water"], "Chalk and sandstone are permeable."),
    ("What does impermeable mean?", "does not let water soak in", ["soft and crumbly", "full of fossils", "very light"], "Slate and granite are impermeable."),
    ("How can you test how hard a rock is?", "try to scratch it with a coin or a steel nail", ["smell it", "weigh it", "put it in the fridge"], "Scratch test."),
    ("Which rock is made from hot, melted rock from a volcano?", "igneous rock", ["sedimentary rock", "metamorphic rock", "chalk"], "Magma or lava cools."),
    ("Is a brick a natural rock?", "No. It is made by people from baked clay.", ["Yes, it is igneous.", "Yes, it is sedimentary.", "Yes, it is metamorphic."], "Man-made."),
    ("What is a grain in a rock?", "a tiny rounded piece, like a grain of sand", ["a seed", "a crystal of ice", "a fossil bone"], "Sedimentary rocks often have grains."),
    ("Which tool helps you look closely at the grains in a rock?", "a magnifying glass", ["a thermometer", "a stopwatch", "a magnet"], "Observe closely."),
])
B5 = bank([
    ("Why do old gravestones made of limestone become hard to read?", "Rain slowly wears away the soft rock.", ["People paint over them.", "Limestone grows.", "Limestone is too hard to wear."], "Weathering."),
    ("Why do pebbles on a beach become smooth and rounded?", "Waves rub them against each other for a long time.", ["They are made that way in factories.", "The sun melts them.", "They are soft when they are found."], "Erosion."),
    ("Why does pumice float on water?", "It is full of tiny holes filled with air.", ["It is made of wood.", "It is very heavy.", "It is magnetic."], "Gas bubbles were trapped as lava cooled."),
    ("A rock fizzes when a drop of vinegar is put on it. Which rock could it be?", "limestone or chalk", ["granite", "slate", "obsidian"], "Acid reacts with chalk and limestone."),
    ("Why would chalk be a poor choice for a doorstep?", "It is soft and would wear away quickly.", ["It is too hard.", "It is too heavy.", "It is waterproof."], "Choose hard rock for steps."),
])


def body():
    think = ("<p><b>We group rocks by how they look and how they behave.</b></p>"
             "<ul><li>Look for grains, crystals, layers, holes and colour. Test hardness with a scratch test and whether water soaks in.</li>"
             "<li>Igneous rocks form from melted rock; sedimentary rocks form from layers; metamorphic rocks are changed by heat and pressure.</li>"
             "<li>Bricks, concrete and glass are man-made, not natural rocks.</li></ul>")
    ex = [("Water soaks into chalk. It is?", ["Water goes in"], "permeable"),
          ("Slate is used for roofs because?", ["Waterproof thin sheets"], "it is impermeable and splits into flat sheets")]
    mist = ["Thinking all rocks are hard.", "Thinking bricks and concrete are rocks.", "Thinking shiny rocks are always the hardest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Kinds of rock", B1 + [(g_type, 8), (g_man, 4)]),
        ("How rocks look", [(g_look, 8), (g_how, 6), (g_type, 6)]),
        ("Natural and man-made", [(g_man, 8), (g_type, 4), (g_use, 6), (g_test, 2)]),
        ("Testing rocks", [(g_test, 20)]),
        ("Choosing rocks", B5 + [(g_use, 6), (g_test, 7), (g_look, 2)]),
    ])
    make_uk(3, "comparing-and-grouping-rocks", 7, "Rocks",
            "Compare and group together different kinds of rocks on the basis of their appearance and simple physical properties.",
            "Comparing and Grouping Rocks",
            "Year 3 Science: Comparing and Grouping Rocks Worksheets (Igneous, Sedimentary, Metamorphic)",
            "Rocks",
            "Free Year 3 science worksheets on rocks: grouping rocks by appearance and properties, hardness and permeability tests, igneous, sedimentary and metamorphic rocks, and uses of rocks. 100 questions with answers.",
            "Look, scratch, drip, then group.",
            "Igneous, sedimentary and metamorphic rocks form in different ways.",
            body(),
            [("How can we group rocks?", "By how they look (grains, crystals, layers, colour) and by simple tests: how hard they are and whether water soaks in."),
             ("What are the three types of rock?", "Igneous rocks form when melted rock cools. Sedimentary rocks form from layers of sand, mud or shells. Metamorphic rocks are rocks changed by heat and pressure."),
             ("What does permeable mean?", "A permeable rock lets water soak into it, like chalk or sandstone. An impermeable rock does not, like slate or granite.")],
            sets)


if __name__ == "__main__":
    main()
