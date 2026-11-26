# -*- coding: utf-8 -*-
"""
UK Year 5 science: Reversible and Irreversible Changes (Properties and changes of materials)
  python tools/gen_uk_science_y5_reversible_and_irreversible_changes.py
Dissolving, mixing and changes of state are reversible; burning, cooking, rusting and the reaction of acid with
bicarbonate of soda make new materials and are not usually reversible. Signs of a new material, a balloon-and-fizz
investigation and a rusting investigation.
Wrong answers come from real mistakes: "melting is irreversible", "dissolving makes a new material",
"burnt toast can be turned back into bread", "iron rusts in dry air".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61507)
R = U.R
P = People(R)

REV = ["melting chocolate", "freezing water into ice", "dissolving sugar in water", "boiling water into steam", "mixing sand and water",
       "melting candle wax", "condensation forming on a cold window", "melting butter", "freezing orange juice into ice lollies", "dissolving salt in water"]
IRR = ["burning wood", "cooking an egg", "baking a cake", "an iron gate rusting", "mixing vinegar and bicarbonate of soda", "toasting bread",
       "milk going sour", "concrete setting hard", "burning a candle wick", "frying an egg", "striking a match", "plaster of Paris setting"]


def g_rev():
    k = R.random() < 0.5
    c = R.choice(REV if k else IRR)
    if not once(("rv", c)):
        return None
    if k:
        return item("Is %s a reversible or an irreversible change?" % c, "reversible", ["irreversible", "it makes a new material", "it cannot happen"], "Changes of state, dissolving and mixing can be reversed.")
    return item("Is %s a reversible or an irreversible change?" % c, "irreversible", ["reversible", "it is only a change of state", "it is the same as dissolving"], "A new material is made, so it cannot easily be changed back.")


def g_pick():
    k = R.random() < 0.5
    if k:
        a = R.choice(IRR)
        w = R.sample(REV, 3)
        q = "Which change makes a new material"
    else:
        a = R.choice(REV)
        w = R.sample(IRR, 3)
        q = "Which change can be reversed"
    if not once(("pk", k, a), 2):
        return None
    o = sorted([a] + w)
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, "Burning, cooking, rusting and fizzing reactions make new materials.")


SIGN = ["bubbles of gas are given off", "the colour changes for good", "heat or light is given out", "a new smell is made", "the change cannot be undone"]
NOTS = ["the material changes shape", "the material gets colder", "the solid melts into a liquid", "the material dissolves and disappears from view", "the material is cut into pieces"]


def g_sign():
    a = R.choice(SIGN)
    w = R.sample(NOTS, 3)
    if not once(("sg", a), 3):
        return None
    o = sorted([a] + w)
    return item("Which is a sign that a new material has been made: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Gas, colour change, heat and light are signs of an irreversible change.")


def g_fizz():
    who = P.next()[0]
    spoons = [1, 2, 3, 4]
    base = R.choice([6, 7, 8])
    vals = [base, base * 2 - R.choice([0, 1]), base * 3 - R.choice([1, 2]), base * 4 - R.choice([2, 3])]
    k = R.choice(["read", "read", "gas", "pattern", "rev", "diff"])
    ri = R.randrange(4)
    if not once(("fz", tuple(vals), k, ri if k == "read" else 0)) or (k in ("gas", "pattern", "rev") and not once(("fk", k), 2)):
        return None
    tab = table(["Spoons of bicarbonate of soda", "Balloon width (cm)"], [[str(a), str(b)] for a, b in zip(spoons, vals)])
    intro = tab + "%s put bicarbonate of soda in a balloon and stretched it over a bottle of vinegar. " % who
    if k == "read":
        g = "%d cm" % vals[ri]
        return item(intro + "How wide did the balloon get with %d spoon%s?" % (spoons[ri], "" if ri == 0 else "s"), g, uniq(g, ["%d cm" % v for v in vals] + ["%d cm" % (vals[ri] + 3)]), "Read the row.")
    if k == "gas":
        return item(intro + "Which gas filled the balloon?", "carbon dioxide", ["oxygen", "air from the vinegar", "steam"], "Vinegar (an acid) reacts with bicarbonate of soda to make carbon dioxide.")
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "More bicarbonate of soda made more gas.", ["More bicarbonate of soda made less gas.", "The amount made no difference.", "The balloon got smaller each time."], "The widths go up.")
    if k == "rev":
        return item(intro + "Is this change reversible?", "No. New materials, including a gas, are made.", ["Yes, just let the balloon down.", "Yes, it is like dissolving.", "Yes, it is a change of state."], "It is a chemical reaction.")
    d = vals[3] - vals[0]
    g = "%d cm" % d
    return item(intro + "How much wider was the balloon with 4 spoons than with 1 spoon?", g, uniq(g, ["%d cm" % vals[3], "%d cm" % vals[0], "%d cm" % (d + 2), "%d cm" % (vals[3] + vals[0])]),
                "%d − %d = %d cm." % (vals[3], vals[0], d))


TUBES = [("tap water and air", "some rust"), ("salt water and air", "the most rust"), ("dry air only (with a drying agent)", "no rust"),
         ("boiled water with oil on top (no air)", "no rust or very little")]


def g_rust():
    who = P.next()[0]
    k = R.choice(["most", "none", "need", "read", "salt"])
    ri = R.randrange(4)
    if not once(("ru", k, ri if k == "read" else who)) or (k != "read" and not once(("rk", k), 3)):
        return None
    tab = table(["Nail kept in", "After one week"], [[a, b] for a, b in TUBES])
    intro = tab + "%s left iron nails in four test tubes. " % who
    if k == "most":
        return item(intro + "Which nail rusted most?", "the one in salt water and air", ["the one in dry air", "the one in boiled water with oil", "they all rusted the same"], "Salt speeds up rusting.")
    if k == "none":
        return item(intro + "Why did the nail in dry air not rust?", "There was no water.", ["There was no iron.", "The air was too warm.", "Dry air makes iron stronger."], "Rusting needs water and air (oxygen).")
    if k == "need":
        return item(intro + "What does iron need in order to rust?", "both water and air (oxygen)", ["only water", "only air", "only salt"], "Take either away and rusting stops.")
    if k == "salt":
        return item(intro + "Why do cars rust faster in winter in the UK?", "Salt spread on icy roads speeds up rusting.", ["Cold stops rust.", "Snow is dry.", "Cars are not made of iron."], "Salt water rusts iron fastest.")
    a, b = TUBES[ri]
    w = [x[1] for x in TUBES if x[1] != b and not ("no rust" in x[1] and "no rust" in b)] + ["it turned to gold", "it dissolved"]
    return item(intro + "What happened to the nail kept in %s?" % a, b, w[:3], "Read the row.")


B1 = bank([
    ("What is a reversible change?", "a change that can be undone, such as melting or dissolving", ["a change that makes a new material", "a change that cannot be undone", "any change involving fire"], "No new material."),
    ("What is an irreversible change?", "a change that makes a new material and cannot easily be undone", ["melting ice", "dissolving salt", "mixing sand and water"], "Burning, cooking, rusting."),
    ("When wood burns, what new materials are made?", "ash, smoke and gases such as carbon dioxide", ["more wood", "water only", "nothing"], "Burning needs oxygen."),
    ("Why is burning dangerous to investigate?", "It gives out heat and flames that can cause burns and fires.", ["It is cold.", "It is reversible.", "It makes ice."], "Only with adult supervision."),
    ("Is melting chocolate reversible?", "Yes, it sets again when it cools.", ["No, it makes a new material.", "No, it burns.", "No, it turns into gas."], "Change of state."),
    ("What is rust?", "a new material formed when iron reacts with water and oxygen", ["a type of paint", "melted iron", "dissolved iron"], "Iron oxide."),
    ("What happens when vinegar is added to bicarbonate of soda?", "It fizzes and makes carbon dioxide gas.", ["Nothing happens.", "It freezes.", "It turns into salt water only."], "A new gas is made."),
    ("Can a cooked egg be uncooked?", "No, cooking is an irreversible change.", ["Yes, by cooling it.", "Yes, by adding water.", "Yes, by stirring."], "The proteins have changed for good."),
])
B5 = bank([
    ("How are iron railings stopped from rusting?", "painting or oiling them to keep water and air away", ["keeping them wet", "adding salt", "heating them"], "Barrier methods."),
    ("A pupil says dissolving salt is irreversible because the salt disappears. How could you show it is reversible?", "Evaporate the water and get the salt back.", ["Filter it.", "Freeze it.", "Stir it more."], "Evidence."),
    ("Why might baking powder in a cake mixture make the cake rise?", "It reacts to make bubbles of carbon dioxide gas.", ["It melts.", "It dissolves and disappears.", "It freezes the cake."], "An irreversible change helps baking."),
    ("Which shows that burning is an irreversible change?", "Ash cannot be turned back into wood.", ["Wood is brown.", "Flames are hot.", "Wood floats."], "New materials."),
    ("In the balloon investigation, why use the same amount of vinegar each time?", "so only the amount of bicarbonate changes", ["to make more gas", "to stop the reaction", "vinegar does not matter"], "Fair test."),
])


def body():
    think = ("<p><b>Some changes can be undone; others make new materials.</b></p>"
             "<ul><li>Reversible: melting, freezing, boiling, condensing, dissolving and mixing.</li>"
             "<li>Irreversible: burning, cooking, rusting, and acids reacting with bicarbonate of soda. New materials are made.</li>"
             "<li>Signs of a new material: gas bubbles, a lasting colour change, heat or light given out, a new smell.</li></ul>")
    ex = [("Toasting bread?", ["The bread changes colour and cannot change back"], "irreversible"),
          ("Melting butter?", ["It sets again when cooled"], "reversible")]
    mist = ["Thinking melting is irreversible.", "Thinking dissolving makes a new material.", "Thinking iron rusts without water."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reversible or not?", B1 + [(g_rev, 12)]),
        ("New materials", [(g_rev, 10), (g_pick, 6), (g_sign, 4)]),
        ("Fizzing reactions", [(g_fizz, 16), (g_sign, 4)]),
        ("Rusting", [(g_rust, 12), (g_pick, 8)]),
        ("Investigating changes", B5 + [(g_fizz, 8), (g_rust, 4), (g_sign, 3)]),
    ])
    make_uk(5, "reversible-and-irreversible-changes", 7, "Properties and changes of materials",
            "Demonstrate that dissolving, mixing and changes of state are reversible changes. Explain that some changes result in the formation of new materials, and that this kind of change is not usually reversible, "
            "including changes associated with burning and the action of acid on bicarbonate of soda.",
            "Reversible and Irreversible Changes",
            "Year 5 Science: Reversible and Irreversible Changes Worksheets (Burning, Rusting, Fizzing)",
            "Reversible Changes",
            "Free Year 5 science worksheets on reversible and irreversible changes: melting, dissolving, burning, cooking, rusting, vinegar and bicarbonate of soda, and signs of new materials. 100 questions with answers.",
            "Can it be changed back?",
            "Melting and dissolving can be undone; burning and rusting make new materials.",
            body(),
            [("What is the difference between reversible and irreversible changes?", "A reversible change, such as melting or dissolving, can be undone. An irreversible change, such as burning or cooking, makes new materials and cannot easily be undone."),
             ("Is dissolving reversible?", "Yes. The dissolved solid is still there and can be got back by evaporating the liquid."),
             ("What happens when vinegar and bicarbonate of soda mix?", "They react and fizz, making carbon dioxide gas and new materials. It is an irreversible change.")],
            sets)


if __name__ == "__main__":
    main()
