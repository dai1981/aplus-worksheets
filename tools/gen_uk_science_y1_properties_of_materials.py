# -*- coding: utf-8 -*-
"""
UK Year 1 science: Properties of Materials (Everyday materials)
  python tools/gen_uk_science_y1_properties_of_materials.py
Describe the simple physical properties of a variety of everyday materials (hard or soft, rough or smooth, shiny or
dull, bendy or stiff, waterproof or not, see-through or not, stretchy, absorbent) and compare and group materials on
the basis of their properties, with a soaking-up test.
Wrong answers come from real mistakes: "shiny means hard", "all metals are bendy", "waterproof means it floats",
"glass is soft because it is smooth".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61110)
R = U.R
P = People(R)

PROP = [("a stone", "hard", ["soft", "stretchy", "see-through"]), ("a pillow", "soft", ["hard", "see-through", "shiny"]), ("sandpaper", "rough", ["smooth", "see-through", "stretchy"]),
        ("a glass marble", "smooth", ["rough", "soft", "stretchy"]), ("kitchen foil", "shiny", ["dull", "stretchy", "absorbent"]), ("a brick", "dull", ["shiny", "see-through", "stretchy"]),
        ("a pipe cleaner", "bendy", ["stiff", "see-through", "waterproof"]), ("a wooden ruler", "stiff", ["stretchy", "soft", "see-through"]),
        ("a plastic raincoat", "waterproof", ["absorbent", "hard", "rough"]), ("a sponge", "absorbent", ["waterproof", "hard", "see-through"]),
        ("a window", "see-through", ["soft", "stretchy", "absorbent"]), ("an elastic band", "stretchy", ["stiff", "hard", "see-through"]),
        ("cotton wool", "soft", ["hard", "shiny", "stiff"]), ("a metal spoon", "hard", ["soft", "stretchy", "absorbent"]), ("tree bark", "rough", ["smooth", "shiny", "stretchy"]),
        ("a mirror", "shiny", ["dull", "soft", "rough"]), ("a wellington boot", "waterproof", ["absorbent", "see-through", "rough"]), ("a paper towel", "absorbent", ["waterproof", "hard", "shiny"]),
        ("a woolly jumper", "soft", ["hard", "shiny", "see-through"]), ("a pair of tights", "stretchy", ["stiff", "hard", "shiny"])]


def g_prop():
    o, p, w = R.choice(PROP)
    if not once(("pr", o)):
        return None
    return item("Which word best describes %s?" % o, p, w, "Feel and look at a material to describe it.")


OPP = [("hard", "soft"), ("rough", "smooth"), ("shiny", "dull"), ("bendy", "stiff"), ("waterproof", "absorbent"), ("see-through", "not see-through")]


def g_opp():
    a, b = R.choice(OPP)
    k = R.random() < 0.5
    x, y = (a, b) if k else (b, a)
    if not once(("op", x)):
        return None
    w = R.sample([z for pair in OPP for z in pair if z not in (x, y)], 3)
    return item("What is the opposite of %s?" % x, y, w, "Properties come in pairs, like hard and soft.")


GROUPS = {"hard": ["a stone", "a metal spoon", "a brick", "a wooden block", "a glass marble"], "soft": ["a pillow", "cotton wool", "a teddy bear", "a woolly hat", "a sponge"],
          "shiny": ["kitchen foil", "a mirror", "a new coin", "a metal spoon"], "bendy": ["a pipe cleaner", "a rubber band", "a sheet of paper", "a sock"],
          "waterproof": ["a plastic bag", "a wellington boot", "an umbrella", "a raincoat"]}
NOTG = {"hard": ["a pillow", "cotton wool", "a sponge", "a sock", "a teddy bear"], "soft": ["a stone", "a brick", "a metal spoon", "a glass marble"],
        "shiny": ["a brick", "a stone", "a woolly hat", "cotton wool", "a sock"], "bendy": ["a brick", "a stone", "a glass marble", "a wooden block"],
        "waterproof": ["a paper towel", "a sponge", "a cotton T-shirt", "a woolly hat", "a newspaper"]}


def g_group():
    gname = R.choice(sorted(GROUPS))
    a = R.choice(GROUPS[gname])
    if not once(("gr", gname, a)):
        return None
    w = R.sample(NOTG[gname], 3)
    o = sorted([a] + w)
    return item("Which of these belongs in the '%s' group: %s or %s?" % (gname, ", ".join(o[:3]), o[3]), a, w, "Group materials by their properties.")


def g_soak():
    who = P.next()[0]
    mats = R.sample(["paper towel", "sponge", "plastic sheet", "kitchen foil", "cotton cloth", "newspaper", "felt", "bin bag"], 4)
    abs_ = {"paper towel": "yes", "sponge": "yes", "plastic sheet": "no", "kitchen foil": "no", "cotton cloth": "yes", "newspaper": "yes", "felt": "yes", "bin bag": "no"}
    res = [abs_[m] for m in mats]
    k = R.choice(["mop", "not", "count"])
    if not once(("so", tuple(mats), k)):
        return None
    tab = table(["Material", "Did it soak up the spilt water?"], [[m, r] for m, r in zip(mats, res)])
    intro = tab + "%s tested which materials soak up water (are absorbent). " % who
    ys = [m for m, r in zip(mats, res) if r == "yes"]
    ns = [m for m, r in zip(mats, res) if r == "no"]
    if k == "mop":
        if len(ys) != 1:
            return None
        return item(intro + "Which material would be best for mopping up a spill?", ys[0], ns, "It soaks up water.")
    if k == "not":
        if len(ns) != 1:
            return None
        return item(intro + "Which material did NOT soak up any water?", ns[0], ys, "It is waterproof.")
    g = str(len(ys))
    return item(intro + "How many materials soaked up water?", g, [str(x) for x in range(5) if x != len(ys)][:3], "Count the 'yes' rows.")


B1 = bank([
    ("What does 'waterproof' mean?", "does not let water through", ["soaks up water", "floats on water", "melts in water"], "Raincoats are waterproof."),
    ("What does 'absorbent' mean?", "soaks up water", ["keeps water out", "is see-through", "is very hard"], "Sponges are absorbent."),
    ("Which material is see-through?", "glass", ["wood", "metal", "rock"], "Windows."),
    ("Which material is soft?", "wool", ["stone", "metal", "glass"], "Woolly jumpers."),
    ("Which material is shiny?", "metal foil", ["a brick", "a woolly hat", "a cardboard box"], "It reflects light."),
    ("Which material is stretchy?", "an elastic band", ["a stone", "a glass", "a brick"], "It gets longer when pulled."),
    ("Which material is rough?", "sandpaper", ["glass", "a mirror", "silk"], "Bumpy to touch."),
    ("How can you find out if a material is hard or soft?", "Press it with your finger.", ["Smell it.", "Listen to it.", "Taste it."], "Use touch."),
])
B5 = bank([
    ("Which material would make a good raincoat for a teddy?", "plastic, because it is waterproof", ["paper, because it is light", "cotton wool, because it is soft", "glass, because it is see-through"], "Choose by property."),
    ("Which material would be best for a window?", "glass, because it is see-through", ["wood, because it is hard", "wool, because it is soft", "foil, because it is shiny"], "We need to see out."),
    ("Is something shiny always hard?", "No. Some shiny things, like foil, are easy to bend.", ["Yes, always.", "Shiny things are soft.", "Shiny things are waterproof."], "Properties are separate."),
    ("How could you test which material is the most waterproof?", "Drip the same amount of water on each and see which stays dry underneath.", ["Look at the colours.", "Use different amounts of water.", "Test only one."], "Fair test."),
    ("Why are pillows filled with soft material?", "so they are comfy to lie on", ["so they are waterproof", "so they are shiny", "so they are see-through"], "Soft for comfort."),
])


def body():
    pic = K.row(["rock", "sock", "umbrella", "glass"], words=["hard", "soft", "waterproof", "see-through"], size=80, label="hard, soft, waterproof and see-through materials")
    ex = [("Sandpaper feels?", ["Bumpy"], "rough"),
          ("A sponge soaks up water. It is?", ["Soaks up"], "absorbent")]
    mist = ["Thinking shiny means hard.", "Thinking waterproof means it floats.", "Thinking glass is soft because it is smooth."]
    return kid_lesson(pic, "Materials have properties.",
                      ["Hard or soft, rough or smooth, shiny or dull.", "Bendy or stiff, waterproof or absorbent, see-through or not.", "We can sort materials by their properties."], ex, mist)


def main():
    sets = U.sets([
        ("Describing materials", B1 + [(g_prop, 12)]),
        ("Opposites", [(g_opp, 10), (g_prop, 6), (g_group, 2), (g_soak, 2)]),
        ("Sorting by property", [(g_group, 14), (g_opp, 1), (g_soak, 5)]),
        ("Soaking-up test", [(g_soak, 20)]),
        ("Thinking about materials", B5 + [(g_soak, 12), (g_group, 3)]),
    ])
    make_uk(1, "properties-of-materials", 10, "Everyday materials",
            "Describe the simple physical properties of a variety of everyday materials. Compare and group together a variety of everyday materials on the basis of their simple physical properties.",
            "Properties of Materials",
            "Year 1 Science: Properties of Materials Worksheets (Hard, Soft, Waterproof)",
            "Properties of Materials",
            "Free Year 1 science worksheets on the properties of materials: hard and soft, rough and smooth, shiny and dull, bendy, waterproof and absorbent, sorting and a soaking-up test. 100 questions with answers.",
            "Materials have properties.",
            "Hard or soft, rough or smooth, waterproof or absorbent.",
            body(),
            [("What are the properties of a material?", "Words that describe how it looks and feels and what it does: hard, soft, rough, smooth, shiny, dull, bendy, stiff, stretchy, waterproof, absorbent, see-through."),
             ("What does waterproof mean?", "It does not let water through, like a plastic raincoat or a wellington boot."),
             ("How can we group materials?", "Put materials with the same property together, for example all the hard things in one group and all the soft things in another.")],
            sets)


if __name__ == "__main__":
    main()
