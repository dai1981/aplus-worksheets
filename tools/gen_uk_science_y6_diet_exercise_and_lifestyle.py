# -*- coding: utf-8 -*-
"""
UK Year 6 science: Diet, Exercise and Lifestyle (Animals, including humans)
  python tools/gen_uk_science_y6_diet_exercise_and_lifestyle.py
Nutrients and their jobs, foods rich in each nutrient, the Eatwell Guide, traffic-light food labels (per 100 g),
sugar in drinks (teaspoons), daily activity, and the effects of exercise, sleep, smoking, alcohol and medicines.
Wrong answers come from real mistakes: "fat has no job in the body", "medicines are always safe in any amount",
"exercise only affects muscles", "a label's grams per 100 g is the amount in the whole packet".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61605)
R = U.R
P = People(R)

FOOD = {"carbohydrates": ["bread", "rice", "pasta", "potatoes", "porridge oats", "noodles", "chapatis"],
        "protein": ["chicken", "fish", "eggs", "lentils", "beans", "tofu", "lean beef"],
        "fat": ["butter", "olive oil", "lard", "cream"],
        "vitamins and minerals": ["oranges", "carrots", "broccoli", "spinach", "strawberries", "peppers", "kiwi fruit"]}
JOB = {"carbohydrates": "give us energy", "protein": "help the body grow and repair itself", "fat": "store energy and keep us warm",
       "vitamins and minerals": "keep us healthy and help the body work properly", "fibre": "help food move through the gut",
       "water": "keep every cell working and stop us getting dehydrated"}


def g_food():
    n = R.choice(sorted(FOOD))
    f = R.choice(FOOD[n])
    if not once(("fo", f)):
        return None
    return item("%s: which nutrient is this food mainly a source of?" % (f[0].upper() + f[1:]), n, [x for x in sorted(FOOD) if x != n], "%s are rich in %s." % (f[0].upper() + f[1:], n))


def g_job():
    n = R.choice(sorted(JOB))
    k = R.random() < 0.5
    if not once(("jo", n, k)):
        return None
    j = JOB[n]
    if k:
        return item("Which nutrient's main job is to %s?" % j, n, R.sample([x for x in JOB if x != n], 3), "%s: %s." % (n[0].upper() + n[1:], j))
    w = R.sample([JOB[x] for x in JOB if x != n], 3)
    return item("What is the main job of %s in our diet?" % n, "to " + j, ["to " + x for x in w], "%s: %s." % (n[0].upper() + n[1:], j))


LIM = {"sugar": (5.0, 22.5), "fat": (3.0, 17.5), "salt": (0.3, 1.5)}
SNACK = {"sugar": ["breakfast cereal", "yoghurt", "cereal bar", "tomato soup", "fruit squash"], "fat": ["crisps", "cheese", "oven chips", "granola", "sausages"],
         "salt": ["bread", "baked beans", "ham", "crackers", "soup"]}


def g_label():
    nut = R.choice(sorted(LIM))
    lo, hi = LIM[nut]
    food = R.choice(SNACK[nut])
    if nut == "salt":
        g = R.choice([0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2, 1.6, 1.8, 2.0, 2.5])
    else:
        g = R.choice([1, 2, 3, 4.5, 6, 8, 10, 12, 15, 18, 20, 24, 26, 30, 35])
    band = "low (green)" if g <= lo else "high (red)" if g > hi else "medium (amber)"
    if not once(("la", nut, g)):
        return None
    gs = ("%g" % g)
    return item("The label for %s shows %s g of %s per 100 g. On a UK traffic-light label, is this low, medium or high in %s?" % (food, gs, nut, nut), band,
                [x for x in ["low (green)", "medium (amber)", "high (red)"] if x != band] + ["it has no %s" % nut],
                "For %s: %g g or less per 100 g is low; more than %g g is high." % (nut, lo, hi))


def g_spoon():
    who = P.next()[0]
    tsp = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13])
    drink = R.choice(["can of fizzy drink", "bottle of fruit juice", "milkshake", "iced coffee", "sports drink", "smoothie"])
    g = tsp * 4
    if not once(("sp", tsp, drink)):
        return None
    a = "%d teaspoons" % tsp
    return item("%s's %s contains %d g of sugar. One teaspoon of sugar is about 4 g. About how many teaspoons of sugar is that?" % (who, drink, g), a,
                uniq(a, ["%d teaspoons" % g, "%d teaspoons" % (g * 4), "%d teaspoons" % (tsp + 4), "%d teaspoons" % max(1, tsp // 2)]), "%d ÷ 4 = %d." % (g, tsp))


def g_active():
    who = P.next()[0]
    parts = R.sample([("cycling to school", [10, 15, 20]), ("doing PE", [30, 45, 50]), ("playing football", [20, 30, 40]), ("swimming", [20, 25, 30]),
                      ("dancing", [15, 20, 25]), ("walking the dog", [10, 15, 20])], 2)
    m = [(a, R.choice(v)) for a, v in parts]
    tot = sum(x for _, x in m)
    if not once(("ac", tuple(m))):
        return None
    need = 60 - tot
    if need > 0:
        a = "%d more minutes" % need
        w = ["%d more minutes" % tot, "%d more minutes" % (60 + tot), "no more minutes"]
    else:
        a = "no more minutes"
        w = ["%d more minutes" % tot, "%d more minutes" % (tot - 60 + 10), "%d more minutes" % 60]
    return item("Children should be active for at least 60 minutes a day. %s spent %d minutes %s and %d minutes %s. How much more activity does %s need today?" % (who, m[0][1], m[0][0], m[1][1], m[1][0], who), a, w,
                "%d + %d = %d minutes; 60 − %d = %s." % (m[0][1], m[1][1], tot, tot, need if need > 0 else "nothing more"))


EFF = [("Smoking cigarettes", "damages the lungs and heart and can cause cancer"), ("Drinking too much alcohol", "damages the liver and affects how the brain works"),
       ("Regular exercise", "makes the heart and muscles stronger"), ("Getting enough sleep", "helps the body grow and helps you concentrate"),
       ("Eating lots of sugary snacks", "can cause tooth decay and unhealthy weight gain"), ("Not drinking enough water", "can cause headaches and tiredness"),
       ("Eating plenty of fruit and vegetables", "gives the body vitamins, minerals and fibre"), ("Too much screen time late at night", "can make it harder to fall asleep")]


def g_eff():
    c, e = R.choice(EFF)
    k = R.random() < 0.6
    if not once(("ef", c, k)):
        return None
    if k:
        return item("What effect does this have on the body: %s?" % c.lower(), e, R.sample([x[1] for x in EFF if x[1] != e], 3), "%s %s." % (c, e))
    return item("Which choice %s?" % e, c.lower(), R.sample([x[0].lower() for x in EFF if x[0] != c], 3), "%s %s." % (c, e))


B1 = bank([
    ("What is a balanced diet?", "eating the right amounts of different kinds of food", ["eating only fruit", "eating the same meal every day", "eating as little as possible"], "Variety in the right amounts."),
    ("According to the Eatwell Guide, about how much of what we eat should be fruit and vegetables?", "about a third", ["almost none", "all of it", "about a tenth"], "At least 5 portions a day."),
    ("Which is the smallest part of the Eatwell Guide?", "oils and spreads", ["fruit and vegetables", "potatoes, bread, rice and pasta", "beans, fish, eggs and meat"], "Use them in small amounts."),
    ("What is a drug?", "a substance that changes the way the body works", ["any kind of food", "a type of exercise", "a vitamin made by plants"], "Medicines are drugs too."),
    ("How should medicines be used?", "only as a doctor, pharmacist or the label says", ["as much as you like", "by sharing them with friends", "only when you are not ill"], "Even medicines can harm."),
    ("Which organ is mostly damaged by drinking too much alcohol over many years?", "the liver", ["the ears", "the hair", "the bones of the feet"], "The liver breaks down alcohol."),
    ("Which substance in cigarettes makes them addictive?", "nicotine", ["oxygen", "vitamin C", "water"], "Nicotine is a drug."),
    ("What does exercise do to the heart over time?", "makes it stronger", ["makes it weaker", "makes it stop", "has no effect"], "The heart is a muscle."),
])
B5 = bank([
    ("A school wants pupils to be healthier. Which plan is best supported by evidence?", "more daily activity and more fruit and vegetables at lunch", ["longer screen time at lunch", "more fizzy drinks", "fewer PE lessons"], "Diet and exercise both matter."),
    ("Why is reading per 100 g on labels useful?", "It lets you compare different foods fairly.", ["It shows the whole packet's weight.", "It shows the price.", "It shows when the food was made."], "Same amount compared."),
    ("A drink is labelled 'no added sugar'. Does that mean it has no sugar?", "No. It can still contain natural sugars from fruit.", ["Yes, always.", "Yes, it is pure water.", "No, it has extra fat."], "Read the label."),
    ("Why might two people need different amounts of food energy?", "They differ in age, size and how active they are.", ["Everyone needs exactly the same.", "Only height matters.", "Energy needs depend on hair colour."], "Needs vary."),
    ("How could you test whether exercise affects reaction time?", "Measure reaction times before and after exercise for the same people, several times.", ["Ask people how they feel.", "Measure once in winter and once in summer.", "Test different people each time without repeats."], "Fair test with repeats."),
])


def body():
    think = ("<p><b>Diet, exercise and lifestyle choices change how well the body works.</b></p>"
             "<ul><li>Nutrients: carbohydrates (energy), protein (growth and repair), fats (stored energy), vitamins and minerals (health), fibre (digestion) and water.</li>"
             "<li>The Eatwell Guide: about a third fruit and vegetables, about a third starchy foods, smaller amounts of protein, dairy, and oils.</li>"
             "<li>Exercise strengthens the heart and muscles. Smoking, alcohol and misusing drugs harm organs; medicines must be used as directed.</li></ul>")
    ex = [("A drink has 28 g of sugar. Teaspoons (4 g each)?", ["28 ÷ 4"], "7 teaspoons"),
          ("Cereal: 25 g sugar per 100 g. Label colour?", ["More than 22.5 g is high"], "high (red)")]
    mist = ["Thinking fat has no job in the body.", "Thinking medicines are safe in any amount.", "Reading per 100 g as the amount in the whole packet."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Nutrients", B1 + [(g_food, 8), (g_job, 4)]),
        ("Food and its jobs", [(g_food, 10), (g_job, 8), (g_eff, 2)]),
        ("Reading food labels", [(g_label, 14), (g_spoon, 6)]),
        ("Exercise and lifestyle", [(g_eff, 12), (g_active, 8)]),
        ("Healthy choices", B5 + [(g_spoon, 6), (g_active, 5), (g_label, 4)]),
    ])
    make_uk(6, "diet-exercise-and-lifestyle", 5, "Animals, including humans",
            "Recognise the impact of diet, exercise, drugs and lifestyle on the way their bodies function.",
            "Diet, Exercise and Lifestyle",
            "Year 6 Science: Diet, Exercise and Lifestyle Worksheets (Nutrients and Food Labels)",
            "Diet and Lifestyle",
            "Free Year 6 science worksheets on diet, exercise and lifestyle: nutrients, the Eatwell Guide, traffic-light food labels, sugar in drinks, activity, smoking, alcohol and medicines. 100 questions with answers.",
            "What we eat and do changes our bodies.",
            "Balance nutrients, stay active, and avoid harmful drugs.",
            body(),
            [("What are the main nutrients?", "Carbohydrates for energy, protein for growth and repair, fats for stored energy, vitamins and minerals for health, plus fibre and water."),
             ("How do traffic-light labels work?", "They show whether a food is low (green), medium (amber) or high (red) in fat, saturated fat, sugar and salt per 100 g, so you can compare foods."),
             ("How does lifestyle affect the body?", "Exercise and good sleep help the heart and brain. Smoking damages the lungs and heart, and too much alcohol damages the liver.")],
            sets)


if __name__ == "__main__":
    main()
