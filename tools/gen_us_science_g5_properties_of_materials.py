# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Identify Materials by Their Properties (5-PS1-3)
  python tools/gen_us_science_g5_properties_of_materials.py
Properties: color, hardness, shine, response to magnets, electrical and thermal conductivity,
solubility, and measurements of mass and volume. Mystery materials and powders are identified
from a table of test results (the table is in the question, the values are real).
Density is not used as a property (NGSS assessment boundary).
Wrong answers come from real mistakes: "all metals stick to magnets", "a nickel is magnetic",
"pencil lead cannot conduct", "the biggest object has the most of a property".
"""
from sci_common import Unit, item, bank, lesson, make, figure, fig, svg_wrap, rect, circle, text, line, table, BLUE, GREEN, INK, People

U = Unit(50102)
R = U.R
P = People(R)

MAGNETIC = ["an iron nail", "a steel paper clip", "a steel screw", "iron filings", "a steel washer", "an iron key ring"]
METAL_NOT_MAG = ["an aluminum can", "a copper wire", "a gold ring", "a brass key", "a US penny", "a US nickel coin", "a silver spoon", "aluminum foil"]
NONMETAL = ["a wooden pencil", "a rubber eraser", "a glass marble", "a plastic button", "a cotton ball", "a paper cup", "a rubber band", "a plastic straw"]
CONDUCT_OTHER = ["the graphite in a pencil"]

# mystery material table: attracted to magnet, conducts electricity, floats in water, dissolves in water
MATS = {
    "iron nail": (1, 1, 0, 0), "copper wire": (0, 1, 0, 0), "wooden stick": (0, 0, 1, 0), "glass marble": (0, 0, 0, 0),
    "salt": (0, 0, 0, 1), "plastic foam": (0, 0, 1, 0), "steel paper clip": (1, 1, 0, 0), "aluminum spoon": (0, 1, 0, 0),
    "sugar": (0, 0, 0, 1), "cork": (0, 0, 1, 0),
}
PROPS = ["Attracted to a magnet?", "Conducts electricity?", "Floats in water?", "Dissolves in water?"]
DESC = [("is attracted to a magnet", "is not attracted to a magnet"), ("conducts electricity", "does not conduct electricity"),
        ("floats in water", "sinks in water"), ("dissolves in water", "does not dissolve in water")]

# powders: dissolves in water, fizzes with vinegar, turns dark blue-black with iodine
POWDERS = {"baking soda": (1, 1, 0), "cornstarch": (0, 0, 1), "table salt": (1, 0, 0), "chalk dust": (0, 1, 0)}
PTESTS = ["Dissolves in water?", "Fizzes with vinegar?", "Turns dark with iodine?"]
PDESC = [("dissolves in water", "does not dissolve in water"), ("fizzes when vinegar is added", "does not fizz with vinegar"),
         ("turns blue-black with iodine", "does not change color with iodine")]

MOHS = {"talc": 1, "gypsum": 2, "calcite": 3, "fluorite": 4, "apatite": 5, "feldspar": 6, "quartz": 7, "topaz": 8}


def andj(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def yn(v):
    return "yes" if v else "no"


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 1: vocabulary
B1 = bank([
    ("What is a property of a material?", "something you can observe or measure about it", ["the name of the material", "the price of the material", "where the material was bought"],
     "Properties are things you can observe or measure, like color, hardness or whether it is attracted to a magnet."),
    ("Which property describes how easily a material can be scratched?", "hardness", ["color", "solubility", "reflectivity"],
     "Hardness tells how well a material resists being scratched. A harder material scratches a softer one."),
    ("Which property describes whether a material dissolves in water?", "solubility", ["hardness", "magnetism", "shine"],
     "A material that dissolves in water, like salt or sugar, is soluble in water."),
    ("Reflectivity describes how a material", "reflects light, like a shiny mirror", ["feels when you touch it", "smells", "dissolves in water"],
     "A shiny metal spoon or a mirror has high reflectivity. A brick reflects very little light."),
    ("A material that lets electricity flow through it easily is called", "an electrical conductor", ["an electrical insulator", "a magnet", "a solution"],
     "Metals like copper are good electrical conductors. That is why wires are made of copper."),
    ("A material that does not let electricity flow through it easily is called", "an electrical insulator", ["an electrical conductor", "a battery", "a mineral"],
     "Rubber, plastic and glass are insulators. Wires are covered in plastic or rubber to keep us safe."),
    ("A material that lets heat move through it quickly is called", "a good thermal conductor", ["a good thermal insulator", "a soluble material", "a magnetic material"],
     "Metals are good thermal conductors, so a metal spoon in hot soup gets hot quickly."),
    ("Why do pot handles often have plastic or wooden covers?", "Plastic and wood are poor conductors of heat.", ["Plastic and wood are magnetic.", "Plastic and wood make the pot heat faster.", "Plastic and wood are shiny."],
     "Plastic and wood are thermal insulators. Heat moves through them slowly, so the handle stays cool enough to hold."),
    ("Which property can you observe just by looking?", "color", ["electrical conductivity", "mass", "solubility"],
     "You can see color. To find conductivity, mass or solubility you need to test or measure."),
    ("Which tool would you use to measure the mass of a mineral sample?", "a balance", ["a graduated cylinder", "a thermometer", "a magnet"],
     "A balance measures mass in grams."),
    ("Which tool is best for measuring the volume of a liquid?", "a graduated cylinder", ["a balance", "a hand lens", "a magnet"],
     "A graduated cylinder has marks in milliliters (mL) for measuring liquid volume."),
    ("Which property would best help you tell a piece of iron from a piece of aluminum that look the same?", "whether it is attracted to a magnet", ["its color", "whether it is a solid", "its shape"],
     "Both are shiny gray solid metals, but only iron is attracted to a magnet."),
    ("Which statement is true about properties?", "Different materials can be identified by their properties.", ["All metals have exactly the same properties.", "A property can only be found by tasting.", "Size is the only property that matters."],
     "Each material has its own set of properties. Testing several properties lets you identify it."),
])


ACTS = [("tries to scratch a mineral with a steel nail", "hardness"), ("holds a magnet near a bolt", "response to magnets"),
        ("puts a spoon in a circuit to see if the bulb lights", "electrical conductivity"), ("stirs a powder into water to see if it disappears", "solubility"),
        ("shines a flashlight on a rock to see if it sparkles", "reflectivity"), ("puts a rod in hot water and feels how fast the other end warms up", "thermal conductivity"),
        ("puts a sample on a balance", "mass"), ("drops a stone into a graduated cylinder of water", "volume"),
        ("compares a sample to a color chart", "color"), ("rubs a metal coin and watches it shine under a lamp", "reflectivity"),
        ("scratches a fingernail across a piece of gypsum", "hardness"), ("drags a magnet through a pile of sand", "response to magnets"),
        ("touches the wires of a battery and bulb to a piece of foil", "electrical conductivity"), ("drops a sugar cube into warm tea and waits", "solubility")]
PROPNAMES = ["hardness", "response to magnets", "electrical conductivity", "solubility", "reflectivity", "thermal conductivity", "mass", "volume", "color"]


def g_which_prop():
    act, pr = R.choice(ACTS)
    p = P.next()
    w = R.sample([x for x in PROPNAMES if x != pr], 3)
    return item("%s %s. Which property is %s testing?" % (p[0], act, p[1]), pr, w,
                "This test shows the material's %s." % pr)


# ------------------------------------------------------------ set 2: magnets, electricity, heat
def g_magnet():
    if R.random() < 0.5:
        a = R.choice(MAGNETIC)
        w = R.sample(METAL_NOT_MAG, 2) + R.sample(NONMETAL, 1)
        return item("Which object will a magnet pick up?", a, w,
                    cap(a) + " contains iron, so it is attracted to a magnet. Many metals, like aluminum, copper and gold, are not.")
    a = R.choice(METAL_NOT_MAG)
    w = R.sample(MAGNETIC, 3)
    return item("Which metal object will <b>not</b> stick to a magnet?", a, w,
                cap(a) + " is a metal, but it has no iron in it, so a magnet does not attract it. Iron and steel are attracted to magnets.")


def g_conduct():
    if R.random() < 0.55:
        a = R.choice(METAL_NOT_MAG + MAGNETIC + CONDUCT_OTHER)
        w = R.sample(NONMETAL, 3)
        why = "Graphite is not a metal, but it does conduct electricity." if "graphite" in a else "Metals conduct electricity."
        return item("A bulb is in a circuit with a gap. Which object placed across the gap will make the bulb light?", a, w,
                    why + " " + cap(w[0]) + " is an insulator.")
    a = R.choice(NONMETAL)
    w = R.sample(METAL_NOT_MAG + MAGNETIC, 3)
    return item("Which object is an electrical <b>insulator</b>?", a, w, cap(a) + " does not let electricity flow through it. All the other objects are metals, which are conductors.")


def g_spoon():
    hot = R.choice(["hot soup", "hot cocoa", "boiling water", "hot tea"])
    a = R.choice(["metal", "steel", "silver"])
    return item("A %s spoon, a wooden spoon and a plastic spoon are put in %s at the same time. Which handle feels warm first?" % (a, hot),
                "the %s spoon" % a, ["the wooden spoon", "the plastic spoon", "They all warm up at the same time."],
                "Metal is a good thermal conductor, so heat moves up the %s spoon fastest. Wood and plastic are insulators." % a)


B2 = bank([
    ("Is every metal attracted to a magnet?", "No. Iron and steel are, but metals like aluminum and copper are not.", ["Yes, every metal is attracted.", "No metal is attracted to a magnet.", "Only shiny metals are attracted."],
     "Only some metals, mainly iron, steel, nickel and cobalt, are attracted to magnets. An aluminum can is not."),
    ("A US nickel coin does not stick to a magnet. Why?", "It is made mostly of copper, which is not magnetic.", ["It is too small.", "It is not a metal.", "Coins cannot be tested with magnets."],
     "A US nickel is about three-fourths copper. There is not enough nickel in it to be attracted."),
    ("Why are electrical wires made of copper covered with plastic?", "Copper conducts electricity and plastic insulates it.", ["Copper and plastic both insulate.", "Plastic conducts electricity better than copper.", "Copper is magnetic."],
     "The copper carries the electricity. The plastic cover keeps the electricity from reaching your hand."),
    ("Which kitchen item works best as an oven mitt?", "a thick cotton glove", ["a thin aluminum sheet", "a steel plate", "a copper pot"],
     "Cloth is a thermal insulator. Metals would let the heat through quickly."),
    ("You tap two spoons on a hot pan. Which material would carry heat to your hand fastest?", "copper", ["wood", "plastic", "rubber"],
     "Copper is one of the best thermal conductors, which is why some pots have copper bottoms."),
    ("A mystery object conducts electricity but is not attracted to a magnet. What could it be?", "an aluminum can", ["an iron nail", "a rubber eraser", "a glass marble"],
     "Aluminum is a metal, so it conducts electricity, but it is not magnetic."),
    ("A mystery object is attracted to a magnet. What else can you predict about it?", "It probably conducts electricity, because it is likely iron or steel.", ["It will float in water.", "It will dissolve in water.", "It is made of plastic."],
     "Objects attracted to magnets are usually iron or steel. These are metals, which conduct electricity."),
    ("Pencil “lead” is really graphite. A student touches the wires of a circuit to the graphite and the bulb lights. What does this show?", "Graphite conducts electricity.", ["Graphite is a magnet.", "Graphite is a metal.", "The bulb was broken."],
     "Graphite is not a metal, but it conducts electricity. Testing is the only way to be sure."),
    ("A cooler keeps drinks cold. What property should the walls of the cooler have?", "They should be good thermal insulators.", ["They should be good electrical conductors.", "They should be attracted to magnets.", "They should dissolve in water."],
     "Thermal insulators slow down the movement of heat into the cooler."),
    ("Which pair of objects are both conductors of electricity?", "a steel key and a copper penny", ["a rubber band and a steel key", "a plastic cup and a glass marble", "a wooden spoon and a paper towel"],
     "Steel and copper are metals, and metals conduct electricity."),
])


# ------------------------------------------------------------ set 3: hardness, dissolving and measurements
def g_scratch():
    ms = R.sample(sorted(MOHS), 3)
    ms.sort(key=lambda m: MOHS[m])
    soft, mid, hard = ms
    order = [(hard, mid), (mid, soft), (hard, soft)]
    R.shuffle(order)
    lines = "; ".join("%s scratches %s" % (cap(a), b) for a, b in order[:2])
    shown = order[:2]
    can = []
    if (hard, mid) in shown:
        can.append("hardest")
    if (mid, soft) in shown:
        can.append("softest")
    if not can:
        return None
    ask = R.choice(can)
    ans = hard if ask == "hardest" else soft
    w = [m for m in ms if m != ans] + ["All three are equally hard."]
    return item("A student does a scratch test on three minerals: %s. Which mineral is the %s?" % (lines, ask),
                ans, w, "A harder mineral scratches a softer one. %s is %s." % (cap(ans), "never scratched, so it is the hardest" if ask == "hardest" else "scratched and scratches nothing, so it is the softest"))


def g_displace():
    a = R.choice([30, 40, 50, 60])
    v = R.randint(6, 25)
    k = R.choice(["rock", "metal bolt", "marble", "mineral sample", "key", "toy car"])
    return item("A graduated cylinder holds %d mL of water. When a %s is dropped in, the water rises to %d mL. What is the volume of the %s?" % (a, k, a + v, k),
                "%d mL" % v, ["%d mL" % (a + v), "%d mL" % a, "%d mL" % (2 * a + v)],
                "The %s pushes aside its own volume of water: %d − %d = %d mL (1 mL = 1 cubic centimeter)." % (k, a + v, a, v))


def g_balance():
    m = R.randint(12, 95)
    c = R.choice([5, 10, 20])
    k = R.choice(["rock", "copper wire", "piece of wood", "seashell", "steel bolt"])
    return item("A %s is placed in a cup on a balance. The cup alone has a mass of %d g. The cup and the %s together have a mass of %d g. What is the mass of the %s?" % (k, c, k, m + c, k),
                "%d g" % m, ["%d g" % (m + c), "%d g" % c, "%d g" % (m + 2 * c)],
                "Subtract the mass of the cup: %d − %d = %d g." % (m + c, c, m))


def g_dissolve():
    yes = ["salt", "sugar", "drink mix powder", "baking soda"]
    no = ["sand", "pepper", "chalk dust", "cornstarch", "small pebbles", "cooking oil"]
    if R.random() < 0.5:
        a = R.choice(yes)
        return item("Which of these dissolves in water?", a, R.sample(no, 3), cap(a) + " dissolves: it breaks into particles too small to see and spreads through the water.")
    a = R.choice(no)
    return item("Which of these does <b>not</b> dissolve in water?", a, R.sample(yes, 3),
                cap(a) + " does not dissolve. You can still see it in the water, or it settles to the bottom" + (" or floats on top." if a == "cooking oil" else "."))


B3 = bank([
    ("Your fingernail can scratch talc and gypsum, but not calcite. What does this tell you?", "Your fingernail is harder than talc and gypsum but softer than calcite.", ["Calcite is the softest of the three.", "Talc is harder than calcite.", "Fingernails cannot be used to test hardness."],
     "Something that scratches a mineral is harder than it. Your fingernail is softer than calcite."),
    ("A mineral scratches glass. Glass cannot scratch the mineral. What can you say?", "The mineral is harder than glass.", ["The glass is harder.", "They are equally hard.", "The mineral will dissolve in water."],
     "The harder material makes the scratch."),
    ("You stir sand into water and stir sugar into water. What do you observe?", "The sugar disappears; the sand stays visible and settles.", ["Both disappear.", "The sand disappears; the sugar stays.", "Both float on top."],
     "Sugar is soluble in water. Sand is not, so you can still see it."),
    ("Which property helps you separate a mix of iron filings and sand?", "Iron is attracted to a magnet.", ["Sand conducts electricity.", "Iron dissolves in water.", "Sand is attracted to a magnet."],
     "A magnet pulls out the iron filings and leaves the sand behind."),
    ("A cube of wood and a cube of steel are the same size. Which measurement will be different?", "mass", ["volume", "length of each side", "number of faces"],
     "They take up the same space, so their volumes are equal, but the steel has more mass."),
    ("Which unit is used for the volume of a liquid?", "milliliters (mL)", ["grams (g)", "degrees (°C)", "centimeters (cm)"],
     "Liquid volume is measured in milliliters or liters."),
    ("Diamond is the hardest natural mineral. Which statement is true?", "Diamond can scratch every other mineral.", ["Every mineral can scratch diamond.", "Diamond dissolves in water.", "Diamond is attracted to a magnet."],
     "The hardest mineral scratches all softer ones, and nothing natural scratches it."),
    ("Two clear liquids look the same. Which test would help tell water from vinegar?", "Smell them, or add baking soda and look for fizzing.", ["Look at their color.", "Measure 10 mL of each.", "Check if they are liquids."],
     "Vinegar has a sharp smell and fizzes with baking soda. Water does neither. (Only smell by wafting the air toward you.)"),
])


# ------------------------------------------------------------ set 4: mystery materials (tables)
def g_mystery():
    names = sorted(MATS)
    for _ in range(40):
        four = R.sample(names, 4)
        vecs = [MATS[n] for n in four]
        if len(set(vecs)) < 4:
            continue
        t = R.choice(four)
        tv = MATS[t]
        props = [0, 1, 2, 3]
        R.shuffle(props)
        use = []
        for p in props:
            use.append(p)
            left = [n for n in four if all(MATS[n][k] == tv[k] for k in use)]
            if left == [t]:
                break
        if len(use) < 2 and R.random() < 0.6:
            continue
        rows = [[n] + [yn(MATS[n][k]) for k in range(4)] for n in four]
        tab = table(["Material"] + PROPS, rows)
        clue = andj([DESC[k][0 if tv[k] else 1] for k in use])
        w = [n for n in four if n != t]
        return item(tab + "A mystery material %s. Use the table. Which material is it?" % clue, t, w,
                    "Only the %s %s." % (t, clue))
    return None


def g_powder():
    names = sorted(POWDERS)
    t = R.choice(names)
    tv = POWDERS[t]
    order = [0, 1, 2]
    R.shuffle(order)
    use = []
    for k in order:
        use.append(k)
        if [n for n in names if all(POWDERS[n][j] == tv[j] for j in use)] == [t]:
            break
    rows = [[n] + [yn(POWDERS[n][k]) for k in range(3)] for n in names]
    clue = andj([PDESC[k][0 if tv[k] else 1] for k in use])
    return item(table(["Powder"] + PTESTS, rows) + "A white powder %s. Which powder is it?" % clue, t, [n for n in names if n != t],
                "Look across each row. Only %s %s." % (t, clue))


def g_powder_test():
    a, b = R.sample(sorted(POWDERS), 2)
    diff = [k for k in range(3) if POWDERS[a][k] != POWDERS[b][k]]
    k = R.choice(diff)
    tests = ["add water and stir", "add a few drops of vinegar", "add a drop of iodine"]
    w = [tests[j] for j in range(3) if POWDERS[a][j] == POWDERS[b][j]]
    w += ["look at the color", "feel if it is a powder", "measure 5 g of each"]
    return item(table(["Powder"] + PTESTS, [[n] + [yn(POWDERS[n][j]) for j in range(3)] for n in sorted(POWDERS)])
                + "Which test would tell %s apart from %s?" % (a, b), tests[k], w[:3],
                "%s? %s: %s. %s: %s. The results are different, so this test tells them apart." % (PTESTS[k][:-1], cap(a), yn(POWDERS[a][k]), cap(b), yn(POWDERS[b][k])))


# ------------------------------------------------------------ set 5: investigations
B5 = bank([
    ("Maya wants to find out which material is the best thermal insulator for a lunch box. What should she keep the same in her test?", "the starting temperature and amount of the food, and the time", ["the material of each box", "nothing", "only the color of the boxes"],
     "Only the material should change. Everything else must stay the same for a fair test."),
    ("Leo tests 4 objects in a circuit. The bulb lights for a key, a foil ball and a coin, but not for a button. Which conclusion is best?", "The key, foil and coin are conductors; the button is an insulator.", ["All four are conductors.", "Only the button is a conductor.", "The bulb is broken."],
     "Objects that let the bulb light are conductors. The button stops the electricity, so it is an insulator."),
    ("Ava finds a shiny gray rock that is attracted to a magnet. Which mineral could it be?", "magnetite", ["quartz", "talc", "calcite"],
     "Magnetite contains a lot of iron, so it is attracted to a magnet. Quartz, talc and calcite are not."),
    ("A class wants to know which material makes the best wire for a circuit. Which property should they test?", "electrical conductivity", ["color", "hardness", "solubility"],
     "A wire must carry electricity well, so test how well each material conducts."),
    ("Omar sorts 10 objects into “attracted to a magnet” and “not attracted.” Which conclusion is supported?", "All attracted objects contain iron or steel, but not all metals are attracted.", ["All metals are attracted.", "Only large objects are attracted.", "Plastic objects are attracted."],
     "Some metals, like aluminum and copper, end up in the “not attracted” group."),
    ("Students test which material keeps ice frozen longest: foil, wool or plastic wrap. The ice in wool lasts longest. What does this show?", "Wool is the best thermal insulator of the three.", ["Wool is the best conductor of heat.", "Foil keeps ice cold longest.", "Wool is attracted to magnets."],
     "Wool slows the movement of heat from the air to the ice, so the ice melts more slowly."),
    ("Noah tests whether salt dissolves faster in warm or cold water. Which plan is a fair test?", "Use the same amount of salt and water in two cups, changing only the temperature.", ["Use more salt in the warm cup.", "Stir only the cold cup.", "Use different cups and different amounts."],
     "Change only one variable (temperature). Keep the salt, water and stirring the same."),
    ("A jeweler wants to test if a gold ring is real without damaging it. Which test is best?", "Check if it is attracted to a magnet (real gold is not).", ["Scratch it with a nail.", "Dissolve it in water.", "Break it in half."],
     "Real gold is not magnetic. If a magnet pulls it, the ring has iron or steel in it."),
    ("Which observation could identify a sample as a metal?", "It is shiny and conducts electricity.", ["It is soft and dissolves in water.", "It is clear and breaks easily.", "It floats on water."],
     "Metals are usually shiny and good conductors of electricity and heat."),
    ("Sofia's mystery liquid freezes at 0 °C and boils at 100 °C. Which liquid is it most likely?", "water", ["cooking oil", "vinegar with salt", "maple syrup"],
     "Pure water freezes at 0 °C and boils at 100 °C. The temperatures where a substance changes state help identify it."),
    ("Two powders look the same. One fizzes with vinegar, and one does not. Why is this a useful test?", "It shows the powders are different materials with different properties.", ["It shows they are the same material.", "It measures their mass.", "It shows they are both magnetic."],
     "Different results on the same test mean different materials."),
])


def body():
    rows = [["iron nail", "yes", "yes", "no"], ["copper wire", "no", "yes", "no"], ["wooden stick", "no", "no", "no"], ["salt", "no", "no", "yes"]]
    think = ("<p>A <b>property</b> is something you can observe or measure about a material. Every material has its own set of properties, "
             "so you can use them like clues to identify it.</p>"
             "<ul><li><b>Color and shine</b> (reflectivity): you can see them.</li>"
             "<li><b>Hardness</b>: a harder material scratches a softer one.</li>"
             "<li><b>Magnetism</b>: iron and steel are attracted to a magnet. Many metals, like aluminum and copper, are not.</li>"
             "<li><b>Conductivity</b>: metals let electricity and heat move through them. Rubber, plastic, wood and glass are insulators.</li>"
             "<li><b>Solubility</b>: salt and sugar dissolve in water; sand does not.</li>"
             "<li><b>Measurements</b>: mass with a balance (g) and volume with a graduated cylinder (mL).</li></ul>"
             + table(["Material", "Attracted to a magnet?", "Conducts electricity?", "Dissolves in water?"], rows))
    ex = [("A mystery material conducts electricity but is not attracted to a magnet. Use the table above.",
           ["Conducts electricity: iron nail or copper wire.", "Not attracted to a magnet: not the iron nail."], "copper wire"),
          ("Water in a graduated cylinder is at 40 mL. A rock is dropped in and the water rises to 52 mL. What is the volume of the rock?",
           ["The rock pushes aside its own volume of water.", "52 − 40 = 12."], "12 mL")]
    mist = ["Thinking every metal sticks to a magnet. Only iron, steel and a few others do.",
            "Using one clue when two materials share it. Keep testing until only one material fits all the clues.",
            "Reading the water level after the object is in as the object's volume. Subtract the starting level.",
            "Thinking only metals conduct electricity. Graphite (pencil lead) conducts too."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Properties of materials", B1 + [(g_which_prop, 8)]),
        ("Magnets, electricity and heat", [g_magnet, g_conduct, g_spoon] + B2),
        ("Hardness, dissolving and measuring", [g_scratch, g_displace, g_balance, g_dissolve] + B3),
        ("Identify the mystery material", [(g_mystery, 10), g_powder, g_powder_test]),
        ("Investigations", B5 + [(g_mystery, 9)]),
    ])
    make("grade-5", "properties-of-materials", 2, "5-PS1-3",
         "Make observations and measurements to identify materials based on their properties.",
         "Identify Materials by Their Properties",
         "Grade 5 Properties of Materials Worksheets: Magnets, Conductors, Hardness, Solubility",
         "Properties of Materials",
         "Free Grade 5 science worksheets on properties of materials (NGSS 5-PS1-3): hardness, shine, magnetism, electrical and thermal conductivity, solubility, mass and volume, and mystery-material tables. 100 practice questions with answers.",
         "Use properties as clues to identify a material.",
         "Test magnetism, conductivity, hardness and solubility, and measure mass and volume, until only one material fits every clue.",
         body(),
         [("What are the properties of materials?", "Properties are things you can observe or measure, such as color, hardness, shine, whether it is attracted to a magnet, whether it conducts electricity or heat, and whether it dissolves in water."),
          ("Are all metals magnetic?", "No. Iron and steel are attracted to magnets, but aluminum, copper, gold and silver are not. A US nickel coin is mostly copper, so it does not stick to a magnet."),
          ("What is the difference between a conductor and an insulator?", "A conductor lets electricity or heat move through it easily, like copper or steel. An insulator slows it down, like rubber, plastic, wood or glass."),
          ("How do you find the volume of a rock?", "Put water in a graduated cylinder, read the level, drop in the rock and read again. The difference is the rock’s volume in mL.")],
         sets)


if __name__ == "__main__":
    main()
