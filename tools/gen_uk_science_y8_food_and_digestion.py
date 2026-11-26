# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Biology): Food and Digestion
  python tools/gen_uk_science_y8_food_and_digestion.py
The content of a healthy human diet (carbohydrates, lipids, proteins, vitamins, minerals, dietary fibre and water) and
why each is needed; calculating energy in food; deficiency diseases; the tissues and organs of the digestive system and
how food is broken down by enzymes and absorbed; the importance of bacteria in the gut.
Reuses the nutrient questions of the Year 6 diet unit and the organ questions of the Year 6 transport unit (new seed).
Wrong answers come from real mistakes: "enzymes are alive", "digestion happens only in the stomach", "fat has no use",
"fibre is digested for energy".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y6_diet_exercise_and_lifestyle as D6
import gen_uk_science_y6_transporting_nutrients_and_water as T6
from sci_phys import uniq

U = Unit(61801)
R = U.R
P = People(R)
D6.U = T6.U = U
D6.R = T6.R = R
D6.P = T6.P = P
uk_sci.USED.clear()

ENZ = [("amylase", "starch", "sugars", "the mouth (saliva) and small intestine"), ("protease", "proteins", "amino acids", "the stomach and small intestine"),
       ("lipase", "lipids (fats and oils)", "fatty acids and glycerol", "the small intestine")]


def g_enz():
    e, s, p, where = R.choice(ENZ)
    k = R.choice(["sub", "prod", "enz"])
    if not once(("en", e, k)):
        return None
    if k == "sub":
        return item("Which food molecule does %s break down?" % e, s, [x[1] for x in ENZ if x[1] != s] + ["vitamins"], "Amylase → starch, protease → proteins, lipase → lipids.")
    if k == "prod":
        return item("What does %s break %s down into?" % (e, s), p, [x[2] for x in ENZ if x[2] != p] + ["fibre"], "Big molecules are broken into small ones that can be absorbed.")
    return item("Which enzyme breaks down %s?" % s, e, [x[0] for x in ENZ if x[0] != e] + ["bile"], "Amylase → starch, protease → proteins, lipase → lipids.")


DEF = [("scurvy (bleeding gums)", "vitamin C"), ("rickets (soft, bent bones)", "vitamin D"), ("anaemia (tiredness, pale skin)", "iron"),
       ("weak bones and teeth", "calcium"), ("constipation", "fibre"), ("kwashiorkor (swollen belly, poor growth)", "protein")]


def g_def():
    d, n = R.choice(DEF)
    k = R.random() < 0.5
    if not once(("de", d, k)):
        return None
    if k:
        return item("A lack of which nutrient causes %s?" % d, n, R.sample([x[1] for x in DEF if x[1] != n], 3), "A deficiency disease happens when the diet lacks a nutrient.")
    return item("Which problem can be caused by too little %s in the diet?" % n, d, R.sample([x[0] for x in DEF if x[0] != d], 3), "A deficiency disease happens when the diet lacks a nutrient.")


FOODS = [("cornflakes", 1600), ("bread", 1000), ("cheese", 1700), ("apple", 220), ("chocolate", 2200), ("baked beans", 350), ("crisps", 2200), ("chicken", 700)]


def g_energy():
    f, e = R.choice(FOODS)
    m = R.choice([20, 25, 30, 40, 50, 60, 80, 150, 200])
    if not once(("eg", f, m)):
        return None
    t = e * m // 100
    g = "{:,} kJ".format(t)
    return item("%s contains %s kJ of energy per 100 g. How much energy is in a %d g portion?" % (f[0].upper() + f[1:], "{:,}".format(e), m), g,
                uniq(g, ["{:,} kJ".format(e * m), "{:,} kJ".format(e), "{:,} kJ".format(t * 10), "{:,} kJ".format(e + m)]), "%s × %d ÷ 100 = %s kJ." % ("{:,}".format(e), m, "{:,}".format(t)))


NEED = [("a 13-year-old who sits most of the day", 8000), ("a 13-year-old who plays a lot of sport", 11000), ("an office worker", 9500), ("a builder", 13000),
        ("a professional cyclist in a race", 20000), ("a pregnant woman", 10500)]


def g_need():
    rows = R.sample(NEED, 4)
    k = R.choice(["most", "least", "diff"])
    if not once(("ne", tuple(r[0] for r in rows), k)):
        return None
    tab = table(["Person", "Energy needed per day (kJ)"], [[a, "{:,}".format(b)] for a, b in rows])
    if k == "most":
        a = max(rows, key=lambda r: r[1])[0]
        return item(tab + "Who needs the most energy each day?", a, [r[0] for r in rows if r[0] != a], "More activity needs more energy.")
    if k == "least":
        a = min(rows, key=lambda r: r[1])[0]
        return item(tab + "Who needs the least energy each day?", a, [r[0] for r in rows if r[0] != a], "Less activity needs less energy.")
    hi, lo = max(rows, key=lambda r: r[1]), min(rows, key=lambda r: r[1])
    d = hi[1] - lo[1]
    g = "{:,} kJ".format(d)
    return item(tab + "How much more energy does %s need than %s?" % (hi[0], lo[0]), g, uniq(g, ["{:,} kJ".format(hi[1]), "{:,} kJ".format(lo[1]), "{:,} kJ".format(hi[1] + lo[1]), "{:,} kJ".format(d + 1000)]),
                "%s − %s = %s kJ." % ("{:,}".format(hi[1]), "{:,}".format(lo[1]), "{:,}".format(d)))


B1 = bank([
    ("What are the seven parts of a balanced diet?", "carbohydrates, lipids, proteins, vitamins, minerals, fibre and water", ["only fruit and vegetables", "sugar, salt and fat", "bread, milk and meat only"], "Each has a job."),
    ("What are enzymes?", "proteins that speed up the breakdown of large food molecules", ["living cells that eat food", "a type of fat", "vitamins"], "Biological catalysts."),
    ("Why must food be digested?", "Large molecules must be broken down into small ones that can be absorbed into the blood.", ["To make it taste better.", "To make it bigger.", "To turn it into fibre."], "Small enough to pass through the gut wall."),
    ("Where are most digested nutrients absorbed into the blood?", "the small intestine", ["the stomach", "the large intestine", "the mouth"], "Long, with villi."),
    ("What are villi?", "tiny finger-like folds in the small intestine that increase its surface area", ["teeth in the stomach", "a type of enzyme", "bacteria in the gut"], "Faster absorption."),
    ("What does the large intestine mainly absorb?", "water", ["proteins", "starch", "enzymes"], "From the leftover waste."),
    ("Why is fibre important even though it is not digested?", "It helps food move through the gut and prevents constipation.", ["It gives lots of energy.", "It builds muscle.", "It is broken down by amylase."], "Roughage."),
    ("What does the stomach produce to kill bacteria in food?", "hydrochloric acid", ["bile", "saliva", "amylase only"], "Acidic conditions."),
])
B5 = bank([
    ("How do bacteria in the large intestine help us?", "They help digest some food and make some vitamins.", ["They make all our energy.", "They make stomach acid.", "They have no use."], "Gut bacteria."),
    ("Why do athletes eat more carbohydrates before a race?", "Carbohydrates are the body's main source of energy.", ["They build muscle fastest.", "They contain no energy.", "They stop sweating."], "Energy stores."),
    ("A food label says 'per 100 g'. Why is this useful?", "It lets you compare different foods fairly.", ["It shows the price.", "It shows the whole packet.", "It is the daily amount."], "Fair comparison."),
    ("How could you test a food for starch?", "Add iodine solution: it turns blue-black if starch is present.", ["Add water: it fizzes.", "Burn it.", "Shine a torch on it."], "Food tests."),
    ("Why can eating too much energy-rich food lead to weight gain?", "Energy not used is stored as fat.", ["Food turns into muscle.", "Extra energy is always lost as heat.", "Weight never changes."], "Energy balance."),
])


def body():
    think = ("<p><b>A balanced diet gives the body the right amounts of seven food groups.</b></p>"
             "<ul><li>Carbohydrates and lipids give energy, proteins build and repair, vitamins and minerals keep us healthy, fibre helps digestion, water is needed by every cell.</li>"
             "<li>Enzymes break big molecules into small ones: amylase → starch, protease → protein, lipase → lipid.</li>"
             "<li>Nutrients are absorbed in the small intestine; water in the large intestine.</li></ul>")
    ex = [("Energy in 50 g of a food with 1,600 kJ per 100 g?", ["1,600 × 50 ÷ 100"], "800 kJ"),
          ("Which enzyme digests protein?", ["Prote-"], "protease")]
    mist = ["Thinking enzymes are alive.", "Thinking digestion happens only in the stomach.", "Thinking fibre is digested for energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("A balanced diet", B1 + [(D6.g_food, 6), (D6.g_job, 6)]),
        ("Deficiency diseases", [(g_def, 10), (D6.g_job, 4), (D6.g_food, 6)]),
        ("Digestive system", [(T6.g_org, 8), (T6.g_next, 6), (g_enz, 6)]),
        ("Enzymes and energy", [(g_enz, 3), (g_energy, 17)]),
        ("Energy needs", B5 + [(g_need, 10), (g_energy, 5)]),
    ])
    make_ks3(8, "food-and-digestion", 1, "Biology", "Nutrition and digestion",
             "Content of a healthy human diet: carbohydrates, lipids (fats and oils), proteins, vitamins, minerals, dietary fibre and water, and why each is needed; calculations of energy requirements in a healthy daily diet; the consequences of imbalances in the diet, including obesity, starvation and deficiency diseases; the tissues and organs of the human digestive system, including adaptations to function and how the digestive system digests food (enzymes simply as biological catalysts); the importance of bacteria in the human digestive system.",
             "Food and Digestion",
             "Year 8 Science: Food and Digestion Worksheets (Nutrients, Enzymes, Energy)",
             "Food and Digestion",
             "Free Year 8 science worksheets on food and digestion: nutrients, deficiency diseases, energy in food, the digestive system, enzymes and gut bacteria. 100 questions with answers.",
             "Enzymes break big molecules into small ones.",
             "Nutrients are absorbed in the small intestine; a balanced diet has seven food groups.",
             body(),
             [("What are the parts of a balanced diet?", "Carbohydrates, lipids (fats and oils), proteins, vitamins, minerals, dietary fibre and water, in the right amounts."),
              ("What do digestive enzymes do?", "They break large food molecules into small ones: amylase breaks starch into sugars, protease breaks proteins into amino acids and lipase breaks lipids into fatty acids and glycerol."),
              ("How do you calculate the energy in a portion?", "Multiply the energy per 100 g by the mass of the portion and divide by 100.")],
             sets)


if __name__ == "__main__":
    main()
