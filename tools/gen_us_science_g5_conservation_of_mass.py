# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Conservation of Mass (5-PS1-2)
  python tools/gen_us_science_g5_conservation_of_mass.py
Whether matter is heated, cooled or mixed, and whether the change is physical or chemical,
the total mass (weight) stays the same, as long as nothing gets in or out.
Questions use measurements, tables and bar graphs of mass before and after.
Wrong answers come from real mistakes: "ice weighs more than water", "gas has no mass",
"dissolved sugar adds no mass", "an open cup that loses gas shows matter was destroyed".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, figure, People, BLUE, GREEN, ORANGE

U = Unit(50105)
R = U.R
P = People(R)


def g(v):
    return "%d g" % v


# ------------------------------------------------------------ set 1: heating and cooling
def g_melt():
    m = R.randint(15, 250)
    k = R.choice([("an ice cube", "melts", "the water"), ("a chocolate bar", "melts", "the melted chocolate"), ("a stick of butter", "melts", "the melted butter"),
                  ("a cup of water", "freezes", "the ice"), ("a candle", "melts in a closed jar", "the melted wax"), ("juice in a sealed pop mold", "freezes", "the frozen pop")])
    return item("%s in a sealed container has a mass of %d g. It %s. What is the mass of %s?" % (cap(k[0]), m, k[1], k[2]),
                g(m), [g(m + R.randint(3, 20)), g(max(1, m - R.randint(3, 20))), "0 g"],
                "Melting and freezing do not add or remove particles. The mass stays %d g." % m)


def g_heat_sealed():
    m = R.randint(80, 400)
    return item("A sealed jar of water with a mass of %d g is heated until the water is very hot. Nothing can get in or out. What is the mass now?" % m,
                g(m), [g(m - R.randint(5, 30)), g(m + R.randint(5, 30)), "It cannot be measured."],
                "The particles move faster when heated, but none are added or lost. The mass stays %d g." % m)


def cap(s):
    return s[0].upper() + s[1:]


B1 = bank([
    ("What does “conservation of mass” mean?", "Matter is not created or destroyed, so the total mass stays the same.", ["Things always get lighter when they change.", "Only solids have mass.", "Mass changes when the shape changes."],
     "In any change, the particles are rearranged, but the total amount of matter (and its mass) stays the same."),
    ("Ice melts in a sealed bag. Which statement is true?", "The water has the same mass as the ice.", ["The water has more mass.", "The water has less mass.", "Water has no mass."],
     "Melting changes the state, not the amount of matter."),
    ("Water freezes and takes up more space. Does it also have more mass?", "No. It takes up more space, but its mass stays the same.", ["Yes, ice always has more mass.", "Yes, because it is a solid.", "No, it has less mass."],
     "Ice takes up a little more space than the same water, but it has exactly the same mass."),
    ("Which tool measures mass?", "a balance or scale", ["a thermometer", "a measuring tape", "a graduated cylinder"],
     "Balances and scales measure mass, in grams (g) or kilograms (kg)."),
    ("In a sealed container, which change would change the total mass?", "none of these: heating, cooling or mixing", ["heating it", "cooling it", "mixing two substances"],
     "If nothing can get in or out, the total mass stays the same no matter what changes happen inside."),
    ("Matter can change state, shape or substance. What cannot change if nothing gets in or out?", "the total mass", ["the temperature", "the shape", "the state"],
     "Temperature, shape and state can all change, but the total mass is conserved."),
])


# ------------------------------------------------------------ set 2: mixing and dissolving
def g_dissolve():
    w = R.randint(100, 400)
    s = R.randint(5, 60)
    k = R.choice(["salt", "sugar", "drink powder", "baking soda"])
    return item("%d g of %s is dissolved in %d g of water. What is the mass of the solution?" % (s, k, w),
                g(w + s), [g(w), g(w - s), g(s)], "%d + %d = %d g. The %s is still there, so its mass is too." % (w, s, w + s, k))


def g_missing():
    a = R.randint(50, 300)
    b = R.randint(10, 80)
    k = R.choice([("water", "salt"), ("vinegar", "baking soda"), ("milk", "cocoa powder"), ("water", "sugar"), ("juice", "ice")])
    p = P.next()
    return item("%s mixes %d g of %s with some %s. The mixture has a mass of %d g. Nothing escaped. How much %s did %s add?" % (p[0], a, k[0], k[1], a + b, k[1], p[1]),
                g(b), [g(a + b), g(a), g(a - b) if a > b else g(a + 2 * b)], "%d − %d = %d g." % (a + b, a, b))


def g_chem_sealed():
    a = R.randint(40, 200)
    b = R.randint(5, 40)
    k = R.choice([("vinegar", "baking soda", "gas bubbles fill the bag"), ("water", "an antacid tablet", "the bag puffs up with gas"),
                  ("milk", "vinegar", "white lumps form"), ("hydrogen peroxide", "yeast", "foam and gas fill the bag")])
    return item("In a sealed bag, %d g of %s is mixed with %d g of %s, and %s. What is the total mass after the change?" % (a, k[0], b, k[1], k[2]),
                g(a + b), [g(a), g(a + b + R.randint(4, 15)), g(a + b - R.randint(4, 15))],
                "New substances form, but no particles get in or out of the sealed bag: %d + %d = %d g." % (a, b, a + b))


B2 = bank([
    ("Sugar disappears when it dissolves in tea. Is its mass gone too?", "No. The tea's mass goes up by the mass of the sugar.", ["Yes, the mass disappears.", "Half of the mass is gone.", "The tea gets lighter."],
     "The sugar particles are spread through the tea. Their mass is still there."),
    ("Two clear liquids are mixed in a closed jar and a yellow solid forms. What happens to the total mass?", "It stays the same.", ["It goes up because a solid formed.", "It goes down because the liquids are used up.", "It becomes zero."],
     "A chemical change rearranges particles into new substances. The total mass does not change."),
    ("Which is true for both physical and chemical changes in a closed container?", "The total mass stays the same.", ["Physical changes lose mass.", "Chemical changes add mass.", "Both always lose mass."],
     "The type of change does not matter. If nothing gets in or out, the mass is conserved."),
    ("Water and sand are mixed. Before: water 150 g and sand 40 g. What mass should the mixture have?", "190 g", ["150 g", "110 g", "40 g"],
     "150 + 40 = 190 g. Mixing does not add or remove matter."),
])


# ------------------------------------------------------------ set 3: open vs closed
def g_open():
    a = R.randint(120, 300)
    lost = R.randint(3, 12)
    k = R.choice([("vinegar and baking soda", "fizzes"), ("water and an antacid tablet", "fizzes"), ("soda", "loses its bubbles")])
    return item("In an <b>open</b> cup, %s %s. The mass goes from %d g to %d g. What is the best explanation?" % (k[0], k[1], a, a - lost),
                "A gas with a mass of %d g escaped into the air." % lost, ["%d g of matter was destroyed." % lost, "The scale is broken.", "Gas has no mass, so the mass should not change."],
                "The gas floated out of the open cup. If the cup were sealed, the mass would stay %d g." % a)


def g_evap():
    a = R.randint(150, 400)
    d = R.randint(10, 60)
    days = R.randint(2, 6)
    return item("An open dish of water has a mass of %d g. After %d days in the sun its mass is %d g. Where did the %d g go?" % (a, days, a - d, d),
                "It evaporated into the air as water vapor.", ["It was destroyed by the sun.", "It turned into the dish.", "It turned into salt."],
                "The water particles left the dish as a gas. They still exist in the air.")


def g_burn():
    a = R.randint(20, 90)
    b = R.randint(5, 15)
    return item("A %d g candle burns for an hour in an open room. Now it has a mass of %d g. What happened to the missing wax?" % (a, a - b),
                "It changed into gases (and soot) that went into the air.", ["It was destroyed.", "It turned into light only.", "It is still in the candle."],
                "Burning wax makes new substances, mostly gases. They escaped, so the candle is lighter, but the matter still exists.")


B3 = bank([
    ("Why do scientists use a sealed container to test conservation of mass?", "so no gas or other matter can get in or out", ["so it gets hotter", "so the change happens faster", "so you can see inside"],
     "In an open container, a gas can escape and make it look like mass was lost."),
    ("A log burns in a campfire and only a little ash is left. Was matter destroyed?", "No. Most of the matter became gases that went into the air.", ["Yes, fire destroys matter.", "Yes, the ash has all the mass.", "No, the log is still whole."],
     "Burning turns wood into ash, smoke and invisible gases. The total matter is the same."),
    ("A sealed bag puffs up when vinegar and baking soda mix. What happens to the mass on the scale?", "It stays the same.", ["It goes up because the bag is bigger.", "It goes down because gas is light.", "It drops to zero."],
     "The gas is trapped inside the bag. Bigger is not the same as heavier."),
    ("A glass of soda left open goes flat and loses a little mass. Why?", "Carbon dioxide gas bubbled out into the air.", ["The soda was destroyed.", "The glass got lighter.", "Sugar evaporated."],
     "The gas that made the bubbles escaped from the open glass."),
])


# ------------------------------------------------------------ set 4: graphs and tables
def g_graph():
    a = R.randint(60, 180) // 5 * 5
    sealed = R.random() < 0.5
    b = a if sealed else a - R.choice([5, 10, 15])
    lab = ["Before", "After"]
    k = R.choice(["mixing vinegar and baking soda", "dropping an antacid tablet in water", "mixing yeast and hydrogen peroxide"])
    ch = bar_chart(lab, [a, b], "grams", "bar graph of mass before and after", ymax=(a // 50 + 1) * 50, step=25, w=200)
    q = fig(ch) + "The graph shows the mass of a cup before and after %s. Was the cup most likely sealed or open?" % k
    if sealed:
        return item(q, "sealed, because the mass did not change", ["open, because the mass went down", "open, because the mass went up", "sealed, because the mass went down"],
                    "Both bars are %d g. No gas escaped, so the cup was most likely sealed." % a)
    return item(q, "open, because gas escaped and the mass went down", ["sealed, because the mass did not change", "sealed, because the mass went down", "open, because the mass went up"],
                "The mass dropped from %d g to %d g. A gas from the change escaped, so the cup was open." % (a, b))


def g_table():
    rows = []
    kinds = [("melting ice", 0), ("freezing water", 0), ("dissolving salt", 0), ("mixing sand and water", 0),
             ("vinegar + baking soda (open cup)", 1), ("antacid in water (open cup)", 1), ("vinegar + baking soda (sealed bag)", 0), ("heating water (sealed jar)", 0)]
    pick = R.sample(kinds, 4)
    if sum(x[1] for x in pick) != 1:
        return None
    for name, lost in pick:
        a = R.randint(50, 250)
        rows.append([name, g(a), g(a - R.randint(4, 12) if lost else a)])
    k = [i for i, x in enumerate(pick) if x[1]][0]
    tab = table(["Change", "Mass before", "Mass after"], rows)
    w = [pick[i][0] for i in range(4) if i != k]
    return item(tab + "In which test did matter most likely leave the container?", pick[k][0], w,
                "Only in this test did the mass go down. A gas escaped from the open cup. In the others the mass stayed the same.")


def g_line():
    m = R.randint(100, 300)
    mins = [0, 5, 10, 15]
    ch = bar_chart([str(x) + " min" for x in mins], [m] * 4, "grams", "bar graph: mass of melting ice in a sealed bag", ymax=(m // 100 + 1) * 100, step=50, col=BLUE, w=280)
    return item(fig(ch) + "Ice melts in a sealed bag. Its mass is measured every 5 minutes. What does the graph show?", "The mass stays %d g as the ice melts." % m,
                ["The mass goes up as the ice melts.", "The mass goes down as the ice melts.", "The mass is 0 g after 15 minutes."],
                "All four bars are the same height: %d g. Melting does not change the mass." % m)


# ------------------------------------------------------------ set 5: investigations
B5 = bank([
    ("Ava weighs ice in an open cup: 100 g. An hour later the melted water weighs 98 g. What is the best explanation?", "A little water evaporated from the open cup.", ["Melting destroyed 2 g of ice.", "Liquid water always weighs less than ice.", "The scale added 2 g."],
     "Some water particles escaped as vapor. In a sealed cup the mass would stay 100 g."),
    ("Leo's sealed bag test shows 152 g before and 151 g after. What should he do?", "Repeat the test, because a 1 g difference may be a measuring error.", ["Decide that 1 g of matter was destroyed.", "Stop and change the question.", "Use an open cup next time."],
     "Small differences can come from the scale or from reading it. Repeating the test checks the result."),
    ("Which investigation best shows that mass is conserved in a chemical change?", "Weigh vinegar and baking soda in a sealed bag before and after mixing.", ["Mix them in an open bowl and look at the bubbles.", "Weigh only the baking soda.", "Measure the temperature of the vinegar."],
     "Weighing the whole sealed system before and after shows the total mass stays the same."),
    ("A student says gases have no mass. Which result shows the student is wrong?", "A cup loses mass when a gas escapes from it.", ["A balloon is light.", "You cannot see air.", "Gases spread out."],
     "If the escaping gas had no mass, the cup would not get lighter."),
    ("Why must all the parts be weighed together, like the bag, the cup and both substances?", "to measure the total mass of everything that was there before and after", ["to make the test faster", "to make the numbers bigger", "because a scale cannot weigh one thing"],
     "The total mass of all the matter is what stays the same."),
    ("Noah freezes 200 g of water in a sealed container. He predicts the ice will be 200 g. Is his prediction correct?", "Yes. Freezing does not change the mass.", ["No, ice is heavier.", "No, ice is lighter.", "No, frozen water has no mass."],
     "The particles are the same. They just lock into place."),
    ("Maya burns a piece of steel wool in a closed jar. The mass of the jar stays the same. Why?", "The new substances stayed inside the closed jar.", ["Steel wool has no mass.", "Burning never makes new substances.", "The jar absorbed the extra mass."],
     "Burning made new substances, but nothing could escape from the closed jar."),
    ("Two groups mix the same amounts of vinegar and baking soda. Group A uses a sealed bag; Group B uses an open cup. Whose mass goes down?", "Group B's, because gas escapes from the open cup", ["Group A's, because the bag puffs up", "Both groups'", "Neither group's"],
     "Only the open cup lets the carbon dioxide gas escape."),
])


def body():
    ch = bar_chart(["Before", "After"], [170, 170], "grams", "bar graph: mass before and after mixing in a sealed bag", ymax=200, step=50, w=200)
    think = ("<p>Matter is made of particles. In any change, the particles are rearranged, but none are created or destroyed. "
             "So the <b>total mass stays the same</b>. This is called <b>conservation of mass</b>.</p>"
             "<p>It is true when matter is <b>heated</b> or <b>cooled</b> (melting, freezing, boiling), when it is <b>mixed</b> or <b>dissolved</b>, "
             "and even in <b>chemical changes</b> that make new substances.</p>"
             + figure(ch, "150 g of vinegar and 20 g of baking soda in a sealed bag: 170 g before and after, even though a gas forms.")
             + "<p>If the mass seems to go down, something escaped, usually a gas or water vapor from an open container.</p>")
    ex = [("40 g of salt is dissolved in 300 g of water. What is the mass of the salt water?", ["The salt is still there as tiny particles.", "300 + 40 = 340."], "340 g"),
          ("In an open cup, an antacid fizzes in water. The mass goes from 210 g to 204 g. Was matter destroyed?", ["210 − 204 = 6 g.", "A gas escaped into the air."], "No. 6 g of gas left the cup.")]
    mist = ["Thinking ice is heavier than the same water. It takes up more space but has the same mass.",
            "Thinking a gas has no mass. When a gas escapes, the container gets lighter.",
            "Thinking a dissolved solid adds no mass. Its mass is still there.",
            "Testing a chemical change in an open cup and deciding matter was destroyed. Use a sealed container."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Heating and cooling", [g_melt, g_heat_sealed] + B1 + [(g_dissolve, 3)]),
        ("Mixing and dissolving", [g_dissolve, g_missing, g_chem_sealed] + B2),
        ("Open or sealed?", [g_open, g_evap, g_burn] + B3),
        ("Graphs and tables", [(g_graph, 8), (g_table, 7), (g_line, 5)]),
        ("Investigations", B5 + [(g_graph, 3), (g_open, 3), (g_table, 3)]),
    ])
    make("grade-5", "conservation-of-mass", 5, "5-PS1-2",
         "Measure and graph quantities to provide evidence that regardless of the type of change that occurs when heating, cooling, or mixing substances, the total weight of matter is conserved.",
         "Conservation of Mass",
         "Grade 5 Conservation of Mass Worksheets: Heating, Cooling, Mixing and Graphs",
         "Conservation of Mass",
         "Free Grade 5 science worksheets on conservation of mass (NGSS 5-PS1-2): mass before and after melting, freezing, dissolving and chemical changes, sealed vs open containers, and bar graphs. 100 practice questions with answers.",
         "In any change, the total mass stays the same.",
         "Heating, cooling, mixing and chemical changes rearrange particles but never destroy them. If the mass goes down, something escaped.",
         body(),
         [("What is the law of conservation of mass?", "Matter cannot be created or destroyed. In any change, the total mass before equals the total mass after, as long as nothing gets in or out."),
          ("Does ice weigh more than water?", "No. Ice takes up a little more space, but the same water has the same mass as a solid or a liquid."),
          ("Why does the mass go down when baking soda and vinegar fizz in an open cup?", "The reaction makes carbon dioxide gas, which escapes into the air. In a sealed bag the mass stays the same."),
          ("Is mass conserved in chemical changes?", "Yes. The particles rearrange into new substances, but the total mass stays the same.")],
         sets)


if __name__ == "__main__":
    main()
