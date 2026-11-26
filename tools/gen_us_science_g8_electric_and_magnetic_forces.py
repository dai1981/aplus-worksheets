# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Electric and Magnetic Forces (MS-PS2-3, MS-PS2-5)
  python tools/gen_us_science_g8_electric_and_magnetic_forces.py
Ask questions about data to determine the factors that affect the strength of electric and magnetic forces
(amount of charge, distance, current, number of coils, iron core, magnet strength), and conduct an investigation
to provide evidence that fields exist between objects exerting forces on each other even though they are not in contact.
Wrong answers come from real mistakes: "like charges attract", "magnets attract all metals", "forces need contact",
"the force gets stronger farther away".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(80103)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def g_charge():
    pairs = [("positive", "positive", "repel"), ("negative", "negative", "repel"), ("positive", "negative", "attract"), ("negative", "positive", "attract")]
    a, b, r = R.choice(pairs)
    who = P.next()[0]
    obj = R.choice([("a balloon", "another balloon"), ("a glass rod", "a plastic rod"), ("a comb", "a bit of paper"), ("a pith ball", "a charged strip")])
    if not once((a, b, obj)):
        return None
    ans = "They %s." % r
    w = ["They %s." % ("attract" if r == "repel" else "repel"), "Nothing happens; they must touch first.", "They attract only if they touch."]
    return item("In %s's test, %s has a %s charge and %s has a %s charge. They are held close but not touching. What happens?" % (who, obj[0], a, obj[1], b), ans, w,
                "Like charges repel; opposite charges attract, even without touching.")


def g_poles():
    p1, p2 = R.choice([("N", "N"), ("S", "S"), ("N", "S"), ("S", "N")])
    who = P.next()[0]
    nm = {"N": "north", "S": "south"}
    r = "repel" if p1 == p2 else "attract"
    thing = R.choice(["two bar magnets", "two ring magnets", "two fridge magnets", "two horseshoe magnets"])
    if not once((p1, p2, thing)):
        return None
    return item("%s holds %s so that a %s pole faces a %s pole. What happens?" % (who, thing, nm[p1], nm[p2]), "They %s." % r,
                ["They %s." % ("attract" if r == "repel" else "repel"), "Nothing happens.", "They spin in circles."], "Like poles repel; opposite poles attract.")


def g_dist():
    who = P.next()[0]
    kind = R.choice(["magnet", "charge"])
    base = R.choice([8, 12, 16, 20, 24])
    d = [1, 2, 3, 4]
    vals = [round(base / (x * x), 1) for x in d]
    lab = "Distance between magnets (cm)" if kind == "magnet" else "Distance between charged balloons (cm)"
    rows = [[str(x), ("%g N" % v)] for x, v in zip(d, vals)]
    tab = table([lab, "Force"], rows)
    k = R.choice(["pattern", "closest", "far"])
    if not once((kind, k), 3):
        return None
    if k == "pattern":
        return item(tab + "What pattern does %s's data show?" % who, "The force gets weaker as the distance increases.", ["The force gets stronger as the distance increases.", "Distance has no effect.", "The force is zero at every distance."],
                    "Electric and magnetic forces get weaker with distance.")
    if k == "closest":
        return item(tab + "At which distance was the force strongest in %s's data?" % who, "1 cm", ["2 cm", "3 cm", "4 cm"], "Closest objects feel the strongest force.")
    return item(tab + "%s moves the objects to 10 cm apart. What will most likely happen to the force?" % who, "It will be even weaker.", ["It will be stronger than at 1 cm.", "It will be the same as at 1 cm.", "It will reverse direction."],
                "The trend continues: farther means weaker.")


def g_coil():
    who = P.next()[0]
    var = R.choice(["coils", "batteries", "core"])
    if var == "coils":
        xs = [10, 20, 30, 40]
        lab = "Number of coils"
    elif var == "batteries":
        xs = [1, 2, 3, 4]
        lab = "Number of batteries (more current)"
    else:
        xs = None
    if xs:
        k = R.choice([2, 3, 4, 5])
        rows = [[str(x), str(k * (i + 1))] for i, x in enumerate(xs)]
        tab = table([lab, "Paper clips picked up"], rows)
        kk = R.choice(["what", "var"])
        if not once((var, kk, k)):
            return None
        if kk == "what":
            a = "More coils make a stronger electromagnet." if var == "coils" else "More current makes a stronger electromagnet."
            w = ["More coils make a weaker electromagnet." if var == "coils" else "More current makes a weaker electromagnet.", "The electromagnet does not change.", "Paper clips are not magnetic."]
            return item(tab + "What conclusion fits %s's electromagnet data?" % who, a, w, "Count the clips: they rise as %s increases." % lab.lower())
        return item(tab + "In %s's electromagnet test, what was the independent variable?" % who, lab.split(" (")[0].lower(), ["the number of paper clips", "the type of paper clip", "the length of the table"],
                    "The independent variable is the one changed on purpose.")
    if not once(("core", 0), 2):
        return None
    rows = [["no core (air)", str(R.choice([2, 3]))], ["wooden pencil", str(R.choice([2, 3]))], ["iron nail", str(R.choice([14, 16, 18]))]]
    tab = table(["Core inside the coil", "Paper clips picked up"], rows)
    return item(tab + "What does %s's data show about electromagnets?" % who, "An iron core makes the electromagnet much stronger.", ["A wooden core makes it stronger.", "The core has no effect.", "An iron core turns it off."],
                "Iron becomes magnetized and adds to the field.")


FIELD = [("A magnet moves a paper clip through a sheet of paper.", "A magnetic field passes through the paper."),
         ("A compass needle swings when a magnet is brought near.", "The magnet's field pushes on the magnetic needle."),
         ("Iron filings form curved lines around a bar magnet.", "They line up along the magnetic field lines."),
         ("A charged balloon makes hair rise before it touches the hair.", "The balloon's electric field pulls on the hair."),
         ("A rubbed comb bends a thin stream of tap water.", "The comb's electric field attracts the water."),
         ("A compass needle moves when current flows in a nearby wire.", "Electric current makes a magnetic field."),
         ("A magnet floats above another magnet with like poles facing.", "The fields push the magnets apart without contact.")]


def g_field():
    s, a = R.choice(FIELD)
    who = P.next()[0]
    if not once(s, 2):
        return None
    w = [x[1] for x in FIELD if x[1] != a]
    w = R.sample(w, 2) + ["The objects must be touching in secret."]
    return item("%s observes: “%s” What explains this?" % (who, s), a, w, "Fields let forces act at a distance.")


MAT = [("an iron nail", True), ("a steel paper clip", True), ("a steel bolt", True), ("an aluminum can", False), ("a copper penny", False), ("a plastic spoon", False),
       ("a gold ring", False), ("a steel spoon", True), ("a wooden block", False), ("a cobalt magnet piece", True)]


def g_mat():
    who = P.next()[0]
    yes = [m for m, v in MAT if v]
    no = [m for m, v in MAT if not v]
    if R.random() < 0.5:
        a = R.choice(yes)
        if not once(("y", a)):
            return None
        return item("%s tests objects with a magnet. Which one will the magnet attract?" % who, a, R.sample(no, 3), "Magnets attract iron, nickel, cobalt and steel, not all metals.")
    a = R.choice(no)
    if not once(("n", a)):
        return None
    return item("%s tests objects with a magnet. Which one will the magnet NOT attract?" % who, a, R.sample(yes, 3), "Aluminum, copper and gold are metals, but magnets do not attract them.")


B1 = bank([
    ("What are the two kinds of electric charge?", "positive and negative", ["north and south", "hot and cold", "big and small"], "North and south are magnetic poles."),
    ("What happens when two objects with like charges are brought close?", "They repel.", ["They attract.", "Nothing.", "They stick together."], "Like charges repel."),
    ("Do magnets attract all metals?", "No. They attract iron, nickel, cobalt and steel.", ["Yes, all metals.", "Only gold.", "Only aluminum."], "Copper and aluminum are not attracted."),
    ("What is a field?", "a region around an object where it can push or pull on other objects without touching", ["a flat area of grass", "the surface of a magnet", "a type of battery"],
     "Electric, magnetic and gravitational fields act at a distance."),
    ("How can you make an electromagnet stronger?", "add more coils, more current or an iron core", ["use fewer coils", "remove the battery", "use a plastic core"], "All three increase the strength."),
    ("What happens to a magnetic force as magnets move farther apart?", "It gets weaker.", ["It gets stronger.", "It stays the same.", "It reverses."], "Distance weakens the force."),
    ("Why does a balloon stick to a wall after you rub it on your hair?", "It gains a charge that attracts charges in the wall.", ["It becomes sticky.", "Gravity changes.", "Air pushes it."], "Static electricity."),
    ("What does an electric current in a wire produce?", "a magnetic field around the wire", ["sound only", "gravity", "nothing"], "This is how electromagnets work."),
])
B5 = bank([
    ("Ava wants to know if distance affects magnetic force. What should she change?", "the distance between the magnets", ["the type of magnets each time", "the color of the table", "nothing"], "Change only distance."),
    ("Leo's electromagnet lifts 6 clips with 1 battery and 12 clips with 2. What question could he test next?", "Does adding coils also increase the clips lifted?", ["Do paper clips like magnets?", "What color is the wire?", "Is the battery heavy?"],
     "A testable question about a factor."),
    ("Mia places a sheet of paper over a magnet and sprinkles iron filings. What is she showing?", "the shape of the magnetic field", ["that paper is magnetic", "that filings are charged", "the weight of the magnet"], "Filings trace field lines."),
    ("A student says magnets need to touch to push each other. What evidence disproves this?", "Two magnets repel when held apart with a gap.", ["Magnets are heavy.", "Magnets are shiny.", "Magnets break."], "Forces act through fields."),
    ("Why should Ava keep the magnet's strength the same in a distance test?", "so only distance could cause the change", ["to make it faster", "because strong magnets are dangerous", "to change two variables"], "Control variables."),
])


def body():
    think = ("<p><b>Electric forces</b> act between charged objects: <b>like charges repel</b>, <b>opposite charges attract</b>. "
             "<b>Magnetic forces</b> act between magnets and on iron, nickel, cobalt and steel: <b>like poles repel</b>, opposite poles attract.</p>"
             "<p>These forces act at a distance through <b>fields</b>. Iron filings and compasses show a magnetic field.</p>"
             "<p>Strength depends on: <b>distance</b> (closer → stronger), <b>amount of charge</b> or magnet strength, and for an electromagnet the <b>current</b>, <b>number of coils</b> and an <b>iron core</b>.</p>")
    ex = [("Two balloons both have a negative charge. What happens?", ["Like charges."], "They repel."),
          ("An electromagnet with 20 coils lifts 8 clips. What will 40 coils likely do?", ["More coils → stronger."], "lift more clips")]
    mist = ["Thinking like charges or like poles attract.",
            "Thinking magnets attract every metal.",
            "Thinking forces need contact. Fields act at a distance."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Charges and poles", B1 + [(g_charge, 6), (g_poles, 6)]),
        ("Attract or repel", [(g_charge, 8), (g_poles, 6), (g_mat, 6)]),
        ("Fields at a distance", [(g_field, 12), (g_dist, 8)]),
        ("Electromagnets", [(g_coil, 14), (g_mat, 6)]),
        ("Investigating forces", B5 + [g_dist, g_coil, g_field, g_mat, g_charge]),
    ])
    make("grade-8", "electric-and-magnetic-forces", 3, "MS-PS2-3",
         "Ask questions about data to determine the factors that affect the strength of electric and magnetic forces.",
         "Electric and Magnetic Forces",
         "Grade 8 Electric and Magnetic Forces Worksheets: Charges, Magnets, Fields and Electromagnets",
         "Electric and Magnetic Forces",
         "Free middle school science worksheets on electric and magnetic forces (NGSS MS-PS2-3, MS-PS2-5): charges and poles, fields acting at a distance, and factors that make electromagnets stronger. 100 practice questions with answers.",
         "Like charges and like poles repel.",
         "Electric and magnetic forces act through fields. They are stronger when objects are closer, with more charge or more current.",
         body(),
         [("What affects the strength of an electromagnet?", "The amount of current, the number of coils of wire and whether there is an iron core."),
          ("Can electric and magnetic forces act without touching?", "Yes. Charged objects and magnets have fields that push or pull on other objects at a distance."),
          ("Why don't magnets attract aluminum cans?", "Magnets only attract a few metals such as iron, nickel, cobalt and steel. Aluminum is not one of them.")],
         sets)


if __name__ == "__main__":
    main()
