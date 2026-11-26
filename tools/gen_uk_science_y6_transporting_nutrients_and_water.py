# -*- coding: utf-8 -*-
"""
UK Year 6 science: Transporting Nutrients and Water (Animals, including humans)
  python tools/gen_uk_science_y6_transporting_nutrients_and_water.py
How food is broken down and its nutrients absorbed (mouth to large intestine), how blood carries nutrients and water
to every cell, how the body takes in and loses water, and simple calculations about intestine length and drinks.
Wrong answers come from real mistakes: "food goes from the mouth straight into the stomach through the windpipe",
"nutrients are absorbed in the stomach", "the large intestine is longer than the small intestine",
"water only leaves the body as urine".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61606)
R = U.R
P = People(R)

ORG = [("the mouth", "Teeth chew food into small pieces and saliva starts to break it down."),
       ("the oesophagus", "A muscular tube squeezes food down to the stomach."),
       ("the stomach", "Acid and churning muscles break food down into a thick liquid."),
       ("the small intestine", "Digested nutrients pass through its walls into the blood."),
       ("the large intestine", "Water is taken back into the body from the leftover waste."),
       ("the rectum", "Solid waste (faeces) is stored until it leaves the body.")]
PATH = [o for o, _ in ORG]


def g_org():
    o, j = R.choice(ORG)
    k = R.random() < 0.5
    if not once(("or", o, k)):
        return None
    if k:
        return item("What happens to food in %s?" % o, j, R.sample([x[1] for x in ORG if x[0] != o], 3), "%s: %s" % (o[0].upper() + o[1:], j))
    return item("In which part of the digestive system does this happen? %s" % j, o, R.sample([x for x in PATH if x != o], 3), "%s: %s" % (o[0].upper() + o[1:], j))


def g_next():
    i = R.randrange(len(PATH) - 1)
    k = R.random() < 0.5
    if not once(("ne", i, k)):
        return None
    if k:
        a = PATH[i + 1]
        w = [x for x in PATH if x not in (a, PATH[i])]
        if PATH[i] == "the mouth":
            w = ["the windpipe"] + w
        return item("Food leaves %s. Where does it go next?" % PATH[i], a, R.sample(w[:4], 3) if PATH[i] != "the mouth" else w[:3], "Mouth → oesophagus → stomach → small intestine → large intestine → rectum.")
    a = PATH[i]
    return item("Food arrives in %s. Where has it just come from?" % PATH[i + 1], a, R.sample([x for x in PATH if x not in (a, PATH[i + 1])], 3),
                "Mouth → oesophagus → stomach → small intestine → large intestine → rectum.")


TRANS = [("Which part of the blood carries dissolved nutrients and water?", "plasma", ["red blood cells", "platelets", "white blood cells"], "Plasma is the liquid part of blood."),
         ("Where do digested nutrients enter the blood?", "the small intestine", ["the stomach", "the mouth", "the large intestine"], "Its walls are thin and have a huge surface."),
         ("Which organ pumps the blood that carries nutrients to the muscles?", "the heart", ["the stomach", "the lungs", "the small intestine"], "The circulatory system transports nutrients."),
         ("What carries nutrients from the small intestine to the cells of the body?", "the blood", ["the nerves", "the bones", "the air in the lungs"], "Blood is the body's transport system."),
         ("Where is most water taken back into the body from leftover food?", "the large intestine", ["the oesophagus", "the mouth", "the rectum"], "This stops us losing too much water."),
         ("Which organs filter waste and extra water out of the blood?", "the kidneys", ["the lungs", "the heart", "the oesophagus"], "Kidneys make urine."),
         ("Why do the cells of the body need nutrients?", "for energy and to grow and repair", ["to make them heavier", "to turn into blood vessels", "to make hair grow only"], "Cells use nutrients."),
         ("What do the tiny finger-like villi in the small intestine do?", "give a huge surface so nutrients are absorbed quickly", ["chew food", "store faeces", "make saliva"], "More surface, faster absorption."),
         ("Which gas does blood carry to the cells along with nutrients?", "oxygen", ["carbon dioxide", "nitrogen", "helium"], "Cells need both to release energy."),
         ("How does the body lose water?", "in urine, sweat and breath", ["only in urine", "only by crying", "it never loses water"], "We lose water in several ways.")]


def g_trans():
    q, a, w, e = R.choice(TRANS)
    if not once(("tr", q)):
        return None
    return item(q, a, w, e)


def g_len():
    h = R.choice([1.2, 1.25, 1.4, 1.5])
    L = R.choice([6, 7, 7.5])
    t = L / h
    if t != int(t) or not once(("le", h, L)):
        return None
    who = P.next()[0]
    g = "%d times" % t
    return item("An adult's small intestine is about %s m long. %s is %s m tall. About how many times longer than %s's height is the small intestine?" % (num(L, 2), who, num(h, 2), who), g,
                uniq(g, ["%d times" % (t * 2), "%s times" % num(L - h, 2), "%d times" % (t + 1), "%s times" % num(L * h, 2)]), "%s ÷ %s = %d." % (num(L, 2), num(h, 2), t))


def g_drink():
    who = P.next()[0]
    gl = R.choice([150, 200, 250, 300])
    n = R.choice([2, 3, 4, 5, 6, 7])
    k = R.choice(["tot", "more"])
    tot = gl * n
    if not once(("dr", gl, n, k)):
        return None
    if k == "tot":
        a = "%s ml" % format(tot, ",")
        return item("%s drinks %d glasses of water. Each glass holds %d ml. How much water is that in total?" % (who, n, gl), a,
                    uniq(a, ["%s ml" % format(gl + n, ","), "%s ml" % format(tot * 10, ","), "%s ml" % format(gl * (n - 1), ","), "%s ml" % format(gl, ",")]), "%d × %d = %s ml." % (n, gl, format(tot, ",")))
    need = 1500 - tot
    if need <= 0:
        return None
    a = "%s ml" % format(need, ",")
    return item("Children are advised to drink about 1,500 ml of fluid a day. %s has drunk %d glasses of %d ml. How much more should %s drink?" % (who, n, gl, who), a,
                uniq(a, ["%s ml" % format(tot, ","), "%s ml" % format(1500 + tot, ","), "%s ml" % format(1500 - gl, ","), "%s ml" % format(need + gl, ",")]),
                "%d × %d = %s ml; 1,500 − %s = %s ml." % (n, gl, format(tot, ","), format(tot, ","), format(need, ",")))


TEETH = [("incisors", "cutting and biting food"), ("canines", "tearing and gripping food"), ("molars", "grinding and chewing food")]


def g_teeth():
    t, j = R.choice(TEETH)
    k = R.random() < 0.5
    if not once(("te", t, k)):
        return None
    if k:
        return item("What is the main job of the %s?" % t, j, [x[1] for x in TEETH if x[0] != t] + ["swallowing food"], "Teeth start digestion by breaking food into smaller pieces.")
    return item("Which teeth are best for %s?" % j, t, [x[0] for x in TEETH if x[0] != t] + ["wisdom teeth only"], "Incisors cut, canines tear, molars grind.")


def g_loss():
    who = P.next()[0]
    rows = [("urine", R.choice([1200, 1300, 1400, 1500])), ("sweat", R.choice([300, 400, 500, 600, 800])), ("breathing out", R.choice([300, 350, 400])), ("faeces", 100)]
    k = R.choice(["tot", "most", "sweat", "hot"])
    tot = sum(v for _, v in rows)
    if not once(("lo", k, tot if k != "sweat" else rows[1][1])) or (k in ("most", "hot") and not once(("lk", k), 2)):
        return None
    tab = table(["Way water leaves the body", "Water lost in a day (ml)"], [[a, format(b, ",")] for a, b in rows])
    if k == "tot":
        a = "%s ml" % format(tot, ",")
        return item(tab + "In %s's data, how much water did the body lose in total that day?" % who, a,
                    uniq(a, ["%s ml" % format(rows[0][1], ","), "%s ml" % format(tot - 100, ","), "%s ml" % format(tot + 500, ","), "%s ml" % format(rows[0][1] + rows[1][1], ",")]), "Add all four rows.")
    if k == "most":
        return item(tab + "In %s's data, which way loses the most water?" % who, "urine", ["sweat", "breathing out", "faeces"], "Read the biggest number.")
    if k == "sweat":
        a = "%s ml" % format(rows[1][1], ",")
        return item(tab + "How much water was lost in sweat in %s's data?" % who, a, uniq(a, ["%s ml" % format(v, ",") for _, v in rows] + ["%s ml" % format(rows[1][1] + 100, ",")]), "Read the sweat row.")
    return item(tab + "On a hot day, which number in %s's table would be most likely to go up?" % who, "sweat", ["faeces", "breathing out", "none of them"], "We sweat more to cool down.")


B1 = bank([
    ("What is digestion?", "breaking food down into small pieces the body can absorb", ["growing new teeth", "pumping blood", "breathing out carbon dioxide"], "Food must be broken down first."),
    ("Which tube carries food from the mouth to the stomach?", "the oesophagus", ["the windpipe", "the small intestine", "a vein"], "The windpipe carries air."),
    ("Where does digestion start?", "in the mouth", ["in the stomach", "in the rectum", "in the heart"], "Chewing and saliva."),
    ("What does saliva do?", "makes food soft and starts to break it down", ["kills all germs in food", "turns food into blood", "stops us tasting food"], "It contains enzymes."),
    ("Which is the longest part of the digestive system?", "the small intestine", ["the large intestine", "the oesophagus", "the stomach"], "About 6 to 7 m in an adult."),
    ("How do nutrients get from the gut to the muscles?", "They are carried in the blood.", ["They walk through the bones.", "They are breathed out.", "They stay in the gut."], "Blood transports them."),
    ("Why do we need to drink water every day?", "The body loses water all the time and every cell needs it.", ["Water gives us protein.", "Water makes bones grow.", "We do not need water."], "Keep hydrated."),
    ("Which part of the body stores faeces before it leaves?", "the rectum", ["the stomach", "the oesophagus", "the small intestine"], "The end of the large intestine."),
])
B5 = bank([
    ("Why does a person feel thirsty after running on a hot day?", "They lost water in sweat and need to replace it.", ["Running makes water.", "Their stomach is full.", "Sweat adds water to the body."], "Water balance."),
    ("Plants also transport water. Which part carries water up from the roots?", "the stem", ["the petals", "the seeds", "the pollen"], "Like blood vessels in animals."),
    ("A model gut is made with tights, mashed food and water. What does squeezing the tights show?", "how nutrients and water pass through the walls of the intestine", ["how teeth chew", "how the heart pumps air", "how the lungs breathe"], "Models help explain."),
    ("Why is fibre important for transporting food through the gut?", "It helps the muscles of the gut move food along.", ["It is absorbed into the blood.", "It gives lots of protein.", "It stops digestion."], "Keeps things moving."),
    ("Diarrhoea can make people dehydrated. Why?", "Water leaves with the waste instead of being absorbed in the large intestine.", ["They drink too much.", "Their blood turns to water.", "Their heart stops."], "Too little water taken back."),
])


def body():
    think = ("<p><b>Food is broken down, absorbed into the blood, and carried to every cell.</b></p>"
             "<ul><li>Path: mouth → oesophagus → stomach → small intestine → large intestine → rectum.</li>"
             "<li>Nutrients pass through the walls of the small intestine into the blood. Water is taken back in the large intestine.</li>"
             "<li>The heart pumps blood; the plasma carries nutrients and water to the cells. Kidneys remove waste and extra water.</li></ul>")
    ex = [("Where do nutrients enter the blood?", ["Food is broken down in the stomach", "Absorbed through the small intestine walls"], "the small intestine"),
          ("4 glasses of 250 ml. Total?", ["4 × 250"], "1,000 ml")]
    mist = ["Thinking food goes down the windpipe.", "Thinking nutrients are absorbed in the stomach.", "Thinking water only leaves the body in urine."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The digestive system", B1 + [(g_org, 8), (g_next, 4)]),
        ("Journey of food", [(g_next, 6), (g_org, 4), (g_teeth, 6), (g_trans, 4)]),
        ("Carried by the blood", [(g_trans, 6), (g_loss, 10), (g_len, 4)]),
        ("Water in the body", [(g_drink, 14), (g_loss, 6)]),
        ("Thinking it through", B5 + [(g_drink, 8), (g_loss, 6), (g_len, 1)]),
    ])
    make_uk(6, "transporting-nutrients-and-water", 6, "Animals, including humans",
            "Describe the ways in which nutrients and water are transported within animals, including humans.",
            "Transporting Nutrients and Water",
            "Year 6 Science: Transporting Nutrients and Water Worksheets (Digestion and Blood)",
            "Nutrients and Water",
            "Free Year 6 science worksheets on transporting nutrients and water: the digestive system, absorption in the small intestine, blood plasma, water balance and the kidneys. 100 questions with answers.",
            "Digested food rides in the blood.",
            "Nutrients enter the blood in the small intestine and travel to every cell.",
            body(),
            [("How are nutrients transported in the body?", "Food is digested into small pieces, absorbed through the walls of the small intestine into the blood, and the heart pumps the blood to every cell."),
             ("Where is water absorbed?", "Mostly in the large intestine, where water is taken back from the leftover waste. Blood then carries water around the body."),
             ("How does the body lose water?", "In urine made by the kidneys, in sweat, and in the water vapour we breathe out.")],
            sets)


if __name__ == "__main__":
    main()
