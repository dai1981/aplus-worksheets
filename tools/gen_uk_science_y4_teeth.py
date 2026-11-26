# -*- coding: utf-8 -*-
"""
UK Year 4 science: Teeth (Animals, including humans)
  python tools/gen_uk_science_y4_teeth.py
Types of human teeth and their jobs (incisors, canines, premolars, molars), milk and adult teeth, how animals' teeth
match their diet, looking after teeth, and the eggshell tooth-decay investigation.
Wrong answers come from real mistakes: "molars are for biting", "adults have 20 teeth", "herbivores have big
canines", "sugar is fine if you brush once a week".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61405)
R = U.R
P = People(R)

TYPES = [("incisors", "cutting and biting", "flat, sharp front teeth"), ("canines", "tearing and gripping", "pointed teeth either side of the incisors"),
         ("premolars", "crushing and grinding", "teeth with two points, between canines and molars"), ("molars", "grinding and chewing", "large, flat teeth at the back")]


def g_type():
    t, j, d = R.choice(TYPES)
    k = R.choice(["job", "which", "look"])
    if not once(("ty", t, k)):
        return None
    if k == "job":
        return item("What is the main job of %s?" % t, j + " food", [x[1] + " food" for x in TYPES if x[0] != t], "Incisors cut, canines tear, premolars and molars grind.")
    if k == "which":
        return item("Which teeth are mainly used for %s food?" % j, t, [x[0] for x in TYPES if x[0] != t], "Incisors cut, canines tear, premolars and molars grind.")
    return item("Which teeth are %s?" % d, t, [x[0] for x in TYPES if x[0] != t], "Learn where each type sits in the mouth.")


FOOD = [("biting into an apple", "incisors"), ("tearing a piece of meat", "canines"), ("grinding up a mouthful of nuts", "molars"), ("biting through a carrot stick", "incisors"),
        ("chewing a mouthful of bread", "molars"), ("ripping into a chicken leg", "canines")]


def g_food():
    f, t = R.choice(FOOD)
    if not once(("fd", f)):
        return None
    return item("Which teeth do the most work when %s?" % f, t, [x[0] for x in TYPES if x[0] != t], "Match the job to the tooth.")


ANI = [("lion", "carnivore", "long, sharp canines for killing and tearing"), ("tiger", "carnivore", "long, sharp canines for killing and tearing"),
       ("shark", "carnivore", "rows of sharp, pointed teeth"), ("cow", "herbivore", "flat, wide molars for grinding grass"),
       ("horse", "herbivore", "flat, wide molars for grinding grass"), ("sheep", "herbivore", "flat, wide molars for grinding grass"),
       ("rabbit", "herbivore", "long front incisors for gnawing and flat back teeth"), ("human", "omnivore", "a mix of incisors, canines and molars"),
       ("bear", "omnivore", "a mix of sharp canines and flat molars"), ("pig", "omnivore", "a mix of sharp canines and flat molars"),
       ("fox", "carnivore", "sharp canines for gripping prey"), ("beaver", "herbivore", "strong orange incisors for gnawing wood")]


def g_ani():
    a, d, t = R.choice(ANI)
    k = R.random() < 0.5
    if not once(("an", a, k)):
        return None
    if k:
        return item("What kind of teeth would you expect a %s to have?" % a, t, R.sample(sorted({x[2] for x in ANI if x[1] != d}), 3) if d != "omnivore" else
                    ["only flat, wide molars", "only long, sharp canines", "no teeth at all"], "Teeth match what an animal eats.")
    an = "an " if d[0] == "o" else "a "
    if not once(("at", t)):
        return None
    return item("An animal's skull has %s. What is the animal most likely to be?" % t, an + d, ["a " + x if x[0] != "o" else "an " + x for x in ("herbivore", "carnivore", "omnivore") if x != d] + ["a producer"],
                "Sharp canines: meat. Flat molars: plants. Both: omnivore.")


def g_egg():
    who = P.next()[0]
    drinks = R.sample(["water", "milk", "orange juice", "cola", "diet cola", "apple juice", "vinegar"], 4)
    score = {"water": 0, "milk": 1, "orange juice": 6, "cola": 8, "diet cola": 6, "apple juice": 5, "vinegar": 10}
    v = [score[d] for d in drinks]
    if len(set(v)) < 4:
        return None
    k = R.choice(["most", "least", "why", "read"])
    ri = R.randrange(4)
    if not once(("eg", tuple(drinks), k, ri if k == "read" else 0)) or (k == "why" and not once(("ew",), 3)):
        return None
    tab = table(["Drink", "Damage to the eggshell after 5 days (0 = none, 10 = worst)"], [[d, str(x)] for d, x in zip(drinks, v)])
    intro = tab + "%s left pieces of eggshell (which is like tooth enamel) in different drinks. " % who
    if k == "most":
        a = drinks[v.index(max(v))]
        return item(intro + "Which drink did the most damage?", a, [d for d in drinks if d != a], "The highest score means the most damage.")
    if k == "least":
        a = drinks[v.index(min(v))]
        return item(intro + "Which of these drinks would be kindest to teeth?", a, [d for d in drinks if d != a], "The lowest score means the least damage.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "What damage score did %s get?" % drinks[ri], g, uniq(g, [str(x) for x in v] + [str(v[ri] + 2), "3"]), "Read the row.")
    return item(intro + "Why was eggshell used in the test?", "It is made of a similar hard material to tooth enamel.", ["Teeth are made of eggs.", "Eggshell is soft.", "It tastes like teeth."], "A model for teeth.")


B1 = bank([
    ("How many milk (baby) teeth do children usually have?", "20", ["32", "10", "50"], "They start falling out at about age 6."),
    ("How many adult teeth do most people have?", "32", ["20", "16", "48"], "Including wisdom teeth."),
    ("What is the hard white outer layer of a tooth called?", "enamel", ["gum", "plaque", "saliva"], "The hardest substance in the body."),
    ("What is plaque?", "a sticky layer of bacteria that forms on teeth", ["a type of tooth", "a kind of toothbrush", "the root of a tooth"], "It makes acid from sugar."),
    ("How often should you brush your teeth?", "twice a day, for about two minutes", ["once a week", "only when they hurt", "once a month"], "Morning and night."),
    ("What does fluoride in toothpaste do?", "makes enamel stronger and helps prevent decay", ["makes teeth grow longer", "turns teeth white instantly", "feeds the bacteria"], "Protects enamel."),
    ("Why do sugary foods cause tooth decay?", "Bacteria in plaque turn sugar into acid that attacks enamel.", ["Sugar is sharp.", "Sugar makes teeth grow.", "Sugar cools teeth."], "Acid damages teeth."),
    ("Who helps us look after our teeth with check-ups?", "a dentist", ["a vet", "a pharmacist", "a plumber"], "Visit regularly."),
])
B5 = bank([
    ("In the eggshell test, why must each piece of shell be the same size?", "so the only difference is the drink", ["to make it quicker", "to use less egg", "size does not matter"], "Fair test."),
    ("Why do dentists suggest drinking water or milk instead of fizzy drinks?", "They do much less damage to tooth enamel.", ["They have more sugar.", "They make teeth grow.", "Fizzy drinks have no sugar."], "Healthy choices."),
    ("A skull has long, sharp canines and no flat molars. What did the animal probably eat?", "meat", ["grass", "leaves", "seeds only"], "Teeth are clues to diet."),
    ("Why do rabbits' incisors keep growing all their lives?", "Gnawing tough plants wears them down all the time.", ["Rabbits never eat.", "They are made of fur.", "Carrots make them grow."], "Adaptation."),
    ("What would happen to teeth if people never brushed them?", "Plaque would build up and cause decay and gum disease.", ["Teeth would get stronger.", "Teeth would turn into molars.", "Nothing at all."], "Hygiene matters."),
])


def body():
    think = ("<p><b>Different teeth do different jobs.</b></p>"
             "<ul><li>Incisors cut and bite; canines tear and grip; premolars and molars crush and grind.</li>"
             "<li>Children have 20 milk teeth; most adults have 32. Teeth match an animal's diet: sharp canines for meat, flat molars for plants.</li>"
             "<li>Sugar feeds bacteria in plaque, which make acid that decays enamel. Brush twice a day with fluoride toothpaste.</li></ul>")
    ex = [("Biting into an apple uses?", ["Front teeth cut"], "incisors"),
          ("Flat molars, small canines. Diet?", ["Grinding plants"], "herbivore")]
    mist = ["Thinking molars are for biting.", "Thinking adults have 20 teeth.", "Thinking herbivores have big canines."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Types of teeth", B1 + [(g_type, 10), (g_food, 2)]),
        ("Teeth at work", [(g_food, 4), (g_ani, 10), (g_type, 2), (g_egg, 4)]),
        ("Animal teeth", [(g_ani, 7), (g_egg, 13)]),
        ("Tooth decay test", [(g_egg, 20)]),
        ("Caring for teeth", B5 + [(g_egg, 15)]),
    ])
    make_uk(4, "teeth", 5, "Animals, including humans",
            "Identify the different types of teeth in humans and their simple functions.",
            "Teeth",
            "Year 4 Science: Teeth Worksheets (Incisors, Canines, Molars and Tooth Decay)",
            "Teeth",
            "Free Year 4 science worksheets on teeth: incisors, canines, premolars and molars, milk and adult teeth, animal teeth and diet, tooth decay and the eggshell investigation. 100 questions with answers.",
            "Cut, tear, grind.",
            "Incisors cut, canines tear, molars grind; sugar and acid damage enamel.",
            body(),
            [("What are the types of teeth?", "Incisors at the front cut and bite, canines tear and grip, and premolars and molars at the back crush and grind food."),
             ("How many teeth do we have?", "Children have 20 milk teeth. These are replaced by adult teeth, and most adults have 32."),
             ("What causes tooth decay?", "Bacteria in plaque feed on sugar and make acid, which slowly dissolves the hard enamel. Brushing and less sugar help prevent it.")],
            sets)


if __name__ == "__main__":
    main()
