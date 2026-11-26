# -*- coding: utf-8 -*-
"""
UK Year 3 science: Magnetic Materials (Forces and magnets)
  python tools/gen_uk_science_y3_magnetic_materials.py
Comparing and grouping everyday materials by whether they are attracted to a magnet, identifying magnetic materials
(iron, steel, nickel, cobalt), noticing that not all metals are magnetic (aluminium, copper, brass, gold, silver),
reading results tables, sorting cans for recycling, and using magnets to separate mixtures.
Wrong answers come from real mistakes: "all metals are magnetic", "shiny things are magnetic", "magnets attract
aluminium foil", "heavy things are magnetic".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61314)
R = U.R
P = People(R)

MAG = ["an iron nail", "a steel paperclip", "a steel spoon", "a steel drawing pin", "iron filings", "a steel food can", "a steel key ring", "a steel safety pin",
       "a nickel button", "steel scissors blades", "an iron bolt", "a steel screw"]
NON = ["an aluminium drinks can", "aluminium foil", "a copper pipe", "a brass key", "a gold ring", "a silver bracelet", "a plastic ruler", "a wooden pencil",
       "a rubber", "a glass marble", "a paper cup", "a cotton sock", "a wool scarf", "a cork"]
NONMETAL_METALS = ["an aluminium drinks can", "aluminium foil", "a copper pipe", "a brass key", "a gold ring", "a silver bracelet"]


def g_is():
    k = R.random() < 0.5
    m = R.choice(MAG if k else NON)
    if not once(("is", m)):
        return None
    ans = "Yes, it is attracted to a magnet." if k else "No, it is not attracted to a magnet."
    return item("Will a magnet attract %s?" % m, ans, ["No, it is not attracted to a magnet." if k else "Yes, it is attracted to a magnet.", "Only if it is shiny.", "Only if it is heavy."],
                "Iron, steel, nickel and cobalt are magnetic. Most other materials, including many metals, are not.")


def g_pick():
    k = R.choice(["mag", "non", "metal"])
    if k == "mag":
        a = R.choice(MAG)
        w = R.sample(NON, 3)
        q = "Which of these would a magnet pick up"
    elif k == "non":
        a = R.choice(NON)
        w = R.sample(MAG, 3)
        q = "Which of these would a magnet NOT pick up"
    else:
        a = R.choice(NONMETAL_METALS)
        w = R.sample(MAG, 3)
        q = "Which of these is a metal that a magnet would NOT pick up"
    if not once(("pk", k, a)):
        return None
    o = sorted([a] + w)
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, "Only iron, steel, nickel and cobalt are magnetic. Aluminium, copper, brass, gold and silver are metals that are not.")


def g_table():
    who = P.next()[0]
    nm = R.choice([2, 3])
    rows = R.sample(MAG, nm) + R.sample(NON, 5 - nm)
    R.shuffle(rows)
    res = ["yes" if r in MAG else "no" for r in rows]
    k = R.choice(["which", "not", "count", "group"])
    if not once(("tb", tuple(rows), k)):
        return None
    tab = table(["Object", "Attracted to the magnet?"], [[r, x] for r, x in zip(rows, res)])
    intro = tab + "%s tested some objects with a magnet. " % who
    ys = [r for r, x in zip(rows, res) if x == "yes"]
    ns = [r for r, x in zip(rows, res) if x == "no"]
    if k == "which":
        if len(ns) < 3:
            return None
        return item(intro + "Which object is made of a magnetic material?", R.choice(ys), R.sample(ns, 3), "It was attracted to the magnet.")
    if k == "not":
        if len(ys) < 3:
            return None
        return item(intro + "Which object is made of a non-magnetic material?", R.choice(ns), ys, "Look for 'no' in the table.")
    if k == "count":
        return item(intro + "How many objects were attracted to the magnet?", str(nm), [str(x) for x in (1, 2, 3, 5) if x != nm][:3], "Count the 'yes' rows.")
    return item(intro + "Into which group would %s sort %s?" % (who, ys[0]), "magnetic materials", ["non-magnetic materials", "light sources", "liquids"], "It was attracted to the magnet.")


SORT = [("Recycling centres use a magnet to sort cans. Which cans does it pick up?", "steel cans", ["aluminium cans", "both kinds of can", "neither kind of can"]),
        ("How could you separate a mixture of iron filings and sand?", "Pass a magnet over it: the iron filings stick to the magnet.", ["Add water and stir.", "Shake it in the sun.", "Blow on it."]),
        ("How could you pick up spilled steel pins from a carpet quickly?", "Sweep a magnet over the carpet.", ["Use a sponge.", "Pour water on them.", "Use a fan."]),
        ("How could you find out if a can is steel or aluminium?", "Hold a magnet to it: steel cans are attracted.", ["Weigh it.", "Look at its colour.", "Shake it."]),
        ("A scrapyard magnet lifts some metal but not all. Which metal stays behind?", "aluminium", ["iron", "steel", "nickel"]),
        ("How could you separate steel paperclips from plastic beads?", "Use a magnet to pull out the paperclips.", ["Sieve them through a tea strainer.", "Melt the beads.", "Freeze them."]),
        ("A cereal is fortified with iron. How could you show there is iron in it?", "Crush it in water and stir with a strong magnet: tiny bits of iron collect on it.", ["Look at the box colour.", "Taste it.", "Heat it in the oven."]),
        ("Why are fridge doors usually made of steel on the outside?", "Steel is magnetic, so fridge magnets stick to it.", ["Steel is a light source.", "Steel is not a metal.", "Magnets stick to all fridges."])]


def g_sort():
    q, a, w = R.choice(SORT)
    if not once(("so", q)):
        return None
    return item(q, a, w, "Magnets attract iron and steel, so they can be used to sort and separate materials.")


B1 = bank([
    ("Which metals are magnetic?", "iron, steel, nickel and cobalt", ["all metals", "gold and silver", "aluminium and copper"], "Only a few metals."),
    ("Are all metals magnetic?", "No. Only some, such as iron and steel.", ["Yes, every metal.", "Yes, if they are shiny.", "Only metals that are heavy."], "Aluminium and copper are not."),
    ("Is aluminium foil magnetic?", "No. Aluminium is a metal that is not magnetic.", ["Yes, all foil is magnetic.", "Yes, because it is shiny.", "Only when it is folded."], "A common mistake."),
    ("Is a plastic spoon attracted to a magnet?", "No. Plastic is not magnetic.", ["Yes, always.", "Only if it is red.", "Only if it is wet."], "Non-magnetic."),
    ("What is a magnetic material?", "a material that is attracted to a magnet", ["any material that is hard", "any shiny material", "a material that gives out light"], "Iron and steel."),
    ("Steel is mostly made from which magnetic metal?", "iron", ["gold", "copper", "aluminium"], "That is why steel is magnetic."),
    ("Is a wooden spoon magnetic?", "No. Wood is not magnetic.", ["Yes.", "Only if it is long.", "Only if it is new."], "Non-magnetic."),
    ("What should you do before saying an object is magnetic?", "test it with a magnet", ["guess from its colour", "guess from how heavy it is", "look at its shape"], "Test, do not guess."),
])
B5 = bank([
    ("A pupil predicts that every shiny object will be magnetic. How could they test this?", "Test lots of shiny objects with a magnet and record the results.", ["Ask a friend.", "Test only one object.", "Look at the objects in the dark."], "Test the idea."),
    ("Why might a magnet not pick up a heavy iron bar?", "The magnet is not strong enough to lift it, even though iron is magnetic.", ["Iron is not magnetic.", "Heavy things are never magnetic.", "Iron repels magnets."], "Attracted but too heavy."),
    ("Some coins are attracted to a magnet and some are not. What does this tell you?", "They are made of different metals.", ["The magnet is broken.", "Coins are made of plastic.", "Only old coins are metal."], "Different materials."),
    ("Why are magnets kept away from computers and bank cards?", "Strong magnets can damage some of the things that store information.", ["Magnets eat cards.", "Computers are magnetic toys.", "It does not matter."], "Care with magnets."),
    ("A magnet attracts a steel paperclip through a wooden table. What does this show?", "Magnetic force can pass through wood, which is not magnetic.", ["Wood is magnetic.", "The paperclip is wooden.", "Magnets only work through metal."], "Through non-magnetic materials."),
])


def body():
    think = ("<p><b>Only some materials are attracted to magnets.</b></p>"
             "<ul><li>Magnetic materials: iron, steel, nickel and cobalt.</li>"
             "<li>Not all metals are magnetic: aluminium, copper, brass, gold and silver are not. Plastic, wood, glass and fabric are not.</li>"
             "<li>Magnets can sort materials, such as steel cans from aluminium cans.</li></ul>")
    ex = [("Steel paperclip: magnetic?", ["Steel contains iron"], "Yes"),
          ("Aluminium can: magnetic?", ["A metal, but not magnetic"], "No")]
    mist = ["Thinking all metals are magnetic.", "Thinking shiny things are magnetic.", "Thinking magnets attract aluminium foil."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Magnetic or not?", B1 + [(g_is, 12)]),
        ("Which metals?", [(g_is, 8), (g_pick, 12)]),
        ("Testing objects", [(g_table, 20)]),
        ("Sorting with magnets", [(g_sort, 8), (g_pick, 6), (g_table, 6)]),
        ("Thinking about materials", B5 + [(g_table, 8), (g_pick, 5), (g_is, 2)]),
    ])
    make_uk(3, "magnetic-materials", 14, "Forces and magnets",
            "Compare and group together a variety of everyday materials on the basis of whether they are attracted to a magnet, and identify some magnetic materials.",
            "Magnetic Materials",
            "Year 3 Science: Magnetic Materials Worksheets (Iron, Steel and Not All Metals)",
            "Magnetic Materials",
            "Free Year 3 science worksheets on magnetic materials: which materials magnets attract, iron and steel, metals that are not magnetic, testing and sorting with magnets. 100 questions with answers.",
            "Iron and steel are magnetic.",
            "Not all metals are magnetic: aluminium and copper are not.",
            body(),
            [("Which materials are magnetic?", "Iron, steel (which is mostly iron), nickel and cobalt. Things made from them, like steel paperclips and iron nails, are attracted to magnets."),
             ("Are all metals magnetic?", "No. Aluminium, copper, brass, gold and silver are metals that are not attracted to magnets."),
             ("How are magnets used to sort materials?", "Recycling centres use magnets to pull steel cans out from aluminium cans. You can also use a magnet to separate iron filings from sand.")],
            sets)


if __name__ == "__main__":
    main()
