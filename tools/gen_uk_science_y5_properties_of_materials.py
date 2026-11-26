# -*- coding: utf-8 -*-
"""
UK Year 5 science: Properties of Materials (Properties and changes of materials)
  python tools/gen_uk_science_y5_properties_of_materials.py
Comparing and grouping materials by hardness, solubility, transparency, electrical and thermal conductivity and
response to magnets; choosing materials for a job; scratch tests and insulation tests.
Wrong answers come from real mistakes: "all metals are magnetic", "a good thermal insulator keeps things cold only",
"hard means heavy", "glass conducts electricity".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61504)
R = U.R
P = People(R)

# material: magnetic, electrical conductor, thermal conductor, transparent
MAT = {"iron": (1, 1, 1, 0), "steel": (1, 1, 1, 0), "nickel": (1, 1, 1, 0), "aluminium": (0, 1, 1, 0), "copper": (0, 1, 1, 0),
       "plastic": (0, 0, 0, 0), "wood": (0, 0, 0, 0), "glass": (0, 0, 0, 1), "rubber": (0, 0, 0, 0), "wool": (0, 0, 0, 0),
       "paper": (0, 0, 0, 0), "brass": (0, 1, 1, 0), "graphite (pencil lead)": (0, 1, 1, 0)}
PROPQ = [(0, "magnetic (attracted to a magnet)"), (1, "a good electrical conductor"), (2, "a good thermal conductor (lets heat through easily)"), (3, "transparent")]


def g_prop():
    m = R.choice(sorted(MAT))
    i, txt = R.choice(PROPQ)
    if not once(("pr", m, i)):
        return None
    v = MAT[m][i]
    note = {0: "Only iron, steel, nickel and cobalt are magnetic; most metals are not.", 1: "Metals and graphite conduct electricity; plastic, wood, glass and rubber do not.",
            2: "Metals let heat through quickly; wood, plastic, wool and rubber are thermal insulators.", 3: "Glass is transparent; the others block light."}[i]
    ans = "Yes" if v else "No"
    return item("Is %s %s?" % (m, txt), ans, ["No" if v else "Yes", "Only when it is wet", "Only when it is cold"], note)


def g_pick():
    i, txt = R.choice(PROPQ)
    yes = [m for m in MAT if MAT[m][i]]
    no = [m for m in MAT if not MAT[m][i]]
    k = R.random() < 0.6
    if k:
        a = R.choice(yes)
        w = R.sample(no, 3)
        q = "Which material is %s" % txt
    else:
        a = R.choice(no)
        w = R.sample(yes, 3) if len(yes) >= 3 else None
        q = "Which material is NOT %s" % txt
    if not w or not once(("pk", i, k, a), 2):
        return None
    o = sorted([a] + w)
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, "Group materials by testing their properties.")


# (use, why, best material, wrong materials, wrong reasons): wrong ones are clearly worse for that job
USE = [("a saucepan base", "it is a good thermal conductor", "steel", ["wood", "plastic", "wool"], ["it is transparent", "it is flexible", "it absorbs water"]),
       ("a saucepan handle", "it is a thermal insulator", "hard plastic", ["copper", "steel", "aluminium"], ["it is magnetic", "it is a good thermal conductor", "it is transparent"]),
       ("electrical wires", "it is a good electrical conductor", "copper", ["plastic", "wood", "glass"], ["it is transparent", "it is an electrical insulator", "it absorbs water"]),
       ("the covering on wires", "it is an electrical insulator", "plastic", ["copper", "aluminium", "steel"], ["it is a good electrical conductor", "it is magnetic", "it is very hard"]),
       ("a window", "it is transparent", "glass", ["wood", "steel", "brick"], ["it is magnetic", "it is a good electrical conductor", "it absorbs water"]),
       ("a winter hat", "it is a good thermal insulator", "wool", ["aluminium foil", "steel", "glass"], ["it is transparent", "it is a good thermal conductor", "it is magnetic"]),
       ("wellington boots", "it is waterproof and flexible", "rubber", ["paper", "cotton", "glass"], ["it absorbs water", "it is transparent", "it is magnetic"]),
       ("a drill tip", "it is very hard", "diamond", ["chalk", "rubber", "wax"], ["it is soft", "it is flexible", "it is soluble"]),
       ("a tea towel", "it absorbs water", "cotton", ["plastic", "glass", "aluminium"], ["it is waterproof", "it is magnetic", "it is transparent"]),
       ("a cool box", "it is a good thermal insulator", "polystyrene foam", ["copper", "steel", "aluminium"], ["it is a good thermal conductor", "it is magnetic", "it is transparent"])]


def g_use():
    u, why, m, wm, wr = R.choice(USE)
    k = R.random() < 0.5
    if not once(("us", u, k)):
        return None
    if k:
        return item("Why is %s used for %s?" % (m, u), "because " + why, ["because " + x for x in wr], "Materials are chosen for their properties.")
    return item("Which material is best for %s, because %s?" % (u, why), m, wm, "Match the property to the job.")


SCR = ["chalk", "copper coin", "iron nail", "glass", "fingernail", "wood"]
HARD = {"fingernail": 2, "chalk": 1, "wood": 3, "copper coin": 4, "iron nail": 5, "glass": 6}


def g_scratch():
    who = P.next()[0]
    ms = R.sample(SCR, 4)
    k = R.choice(["hard", "soft", "pair"])
    if not once(("sc", tuple(sorted(ms)), k)):
        return None
    rows = []
    for m in ms:
        scr = [x for x in ms if x != m and HARD[m] > HARD[x]]
        rows.append([m, ", ".join(scr) if scr else "nothing"])
    tab = table(["Material", "It scratched"], rows)
    intro = tab + "%s tested which materials could scratch the others. " % who
    if k == "hard":
        a = max(ms, key=lambda m: HARD[m])
        return item(intro + "Which material is the hardest?", a, [m for m in ms if m != a], "The hardest material scratches all the others.")
    if k == "soft":
        a = min(ms, key=lambda m: HARD[m])
        return item(intro + "Which material is the softest?", a, [m for m in ms if m != a], "The softest material scratches nothing.")
    x, y = R.sample(ms, 2)
    a = x if HARD[x] > HARD[y] else y
    return item(intro + "Which is harder: %s or %s?" % (x, y), a, [y if a == x else x, "They are equally hard.", "You cannot tell from this test."], "A harder material scratches a softer one.")


def g_ins():
    who = P.next()[0]
    mats = R.sample(["wool", "cotton", "foil", "bubble wrap", "newspaper", "felt"], 4)
    val = {"wool": 58, "bubble wrap": 60, "felt": 56, "newspaper": 52, "cotton": 50, "foil": 44}
    temps = [val[m] + R.choice([-1, 0, 1]) for m in mats]
    if len(set(temps)) < 4:
        return None
    k = R.choice(["best", "worst", "read", "fair"])
    ri = R.randrange(4)
    if not once(("in", tuple(mats), tuple(temps), k, ri if k == "read" else 0)) or (k == "fair" and not once(("if",), 3)):
        return None
    tab = table(["Wrapping", "Temperature after 20 minutes (°C)"], [[m, str(t)] for m, t in zip(mats, temps)])
    intro = tab + "%s wrapped cans of hot water (70 °C) in different materials. " % who
    if k == "best":
        a = mats[temps.index(max(temps))]
        return item(intro + "Which material was the best thermal insulator?", a, [m for m in mats if m != a], "The water that stayed hottest lost heat most slowly.")
    if k == "worst":
        a = mats[temps.index(min(temps))]
        return item(intro + "Which material let heat escape fastest?", a, [m for m in mats if m != a], "The lowest temperature means the most heat was lost.")
    if k == "read":
        g = "%d °C" % temps[ri]
        return item(intro + "What was the temperature of the can wrapped in %s?" % mats[ri], g, uniq(g, ["%d °C" % t for t in temps] + ["70 °C"]), "Read the row.")
    return item(intro + "What should %s keep the same to make the test fair?" % who, "the amount and starting temperature of the water, and the thickness of the wrapping",
                ["the type of wrapping", "the final temperature", "nothing"], "Only the material should change.")


B1 = bank([
    ("What does a thermal insulator do?", "slows down the movement of heat", ["makes things hotter", "makes heat move faster", "conducts electricity"], "It works for keeping things hot or cold."),
    ("Are all metals magnetic?", "No. Only a few, such as iron, steel and nickel, are magnetic.", ["Yes, every metal is magnetic.", "No metals are magnetic.", "Only gold is magnetic."], "Aluminium and copper are not."),
    ("What does soluble mean?", "able to dissolve in a liquid such as water", ["able to float", "able to conduct electricity", "able to bend"], "Salt and sugar are soluble."),
    ("Which material is transparent?", "clear glass", ["wood", "metal", "brick"], "Light passes through."),
    ("What is hardness?", "how easily a material can be scratched", ["how heavy it is", "how cold it is", "how shiny it is"], "Harder materials scratch softer ones."),
    ("Why are cooking spoons for hot pans often made of wood?", "Wood is a thermal insulator, so the handle does not get hot.", ["Wood conducts heat well.", "Wood is magnetic.", "Wood is transparent."], "Comfort and safety."),
    ("Which material conducts electricity?", "copper", ["plastic", "rubber", "glass"], "Metals conduct."),
    ("What does flexible mean?", "able to bend without breaking", ["very hard", "see-through", "magnetic"], "Rubber is flexible."),
])
B5 = bank([
    ("Why is a test with a magnet useful for sorting cans at a recycling centre?", "Steel cans are attracted to magnets, but aluminium cans are not.", ["All cans are magnetic.", "Magnets melt cans.", "Magnets make cans lighter."], "Use properties to sort."),
    ("A thermos flask keeps soup hot. What would it do to cold juice?", "keep it cold, because it slows down heat moving in", ["make it hot", "make it freeze", "make it fizzy"], "Insulators work both ways."),
    ("Why are electrical plugs covered in plastic but have metal pins?", "Metal pins conduct electricity; plastic insulates to keep you safe.", ["Plastic conducts better.", "Metal is see-through.", "It looks nice."], "Two properties, two jobs."),
    ("How could you test which fabric is most waterproof?", "Pour the same amount of water on each and measure how much goes through.", ["Smell each fabric.", "Weigh dry fabric only.", "Use different amounts of water."], "Fair test."),
    ("Why must the same thickness of each material be used in an insulation test?", "Thicker layers insulate better, which would make the test unfair.", ["Thickness does not matter.", "Thin materials are always best.", "To save time."], "Control variables."),
])


def body():
    think = ("<p><b>Materials are chosen for their properties.</b></p>"
             "<ul><li>Hardness, solubility, transparency, flexibility, electrical and thermal conductivity, and whether they are magnetic.</li>"
             "<li>Metals conduct electricity and heat. Only some metals (iron, steel, nickel) are magnetic.</li>"
             "<li>Plastic, wood, rubber and wool are insulators. Test properties fairly before choosing.</li></ul>")
    ex = [("Saucepan handle: which property?", ["It must not get hot"], "a thermal insulator, such as hard plastic"),
          ("Is aluminium magnetic?", ["Only iron, steel, nickel and cobalt are"], "No")]
    mist = ["Thinking all metals are magnetic.", "Thinking insulators only keep things hot.", "Confusing hardness with weight."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Properties", B1 + [(g_prop, 8), (g_pick, 4)]),
        ("Grouping materials", [(g_prop, 12), (g_pick, 8)]),
        ("Choosing materials", [(g_use, 16), (g_pick, 4)]),
        ("Hardness tests", [(g_scratch, 16), (g_ins, 4)]),
        ("Insulation tests", B5 + [(g_ins, 12), (g_use, 3)]),
    ])
    make_uk(5, "properties-of-materials", 4, "Properties and changes of materials",
            "Compare and group together everyday materials on the basis of their properties, including their hardness, solubility, transparency, conductivity (electrical and thermal), and response to magnets. "
            "Give reasons, based on evidence from comparative and fair tests, for the particular uses of everyday materials, including metals, wood and plastic.",
            "Properties of Materials",
            "Year 5 Science: Properties of Materials Worksheets (Conductors, Insulators, Magnets)",
            "Properties of Materials",
            "Free Year 5 science worksheets on properties of materials: hardness, solubility, transparency, electrical and thermal conductivity, magnetic materials and choosing materials for a job. 100 questions with answers.",
            "Choose materials by their properties.",
            "Hard or soft, see-through or not, conductor or insulator, magnetic or not.",
            body(),
            [("What are the properties of materials?", "Features such as hardness, flexibility, transparency, solubility, whether a material conducts heat or electricity, and whether it is attracted to a magnet."),
             ("Are all metals magnetic?", "No. Only iron, nickel, cobalt and alloys such as steel are magnetic. Aluminium, copper and gold are not."),
             ("What is a thermal insulator?", "A material that slows down the movement of heat, such as wool, plastic or wood. It keeps hot things hot and cold things cold.")],
            sets)


if __name__ == "__main__":
    main()
