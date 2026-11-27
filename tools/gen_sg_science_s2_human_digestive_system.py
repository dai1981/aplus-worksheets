# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Systems): Human Digestive System
  python tools/gen_sg_science_s2_human_digestive_system.py
Why we need a digestive system; the mouth, gullet (oesophagus), stomach, small intestine, large intestine, rectum and anus, and
the liver, gall bladder and pancreas; physical and chemical digestion; carbohydrases, proteases and lipases and their end products
(simple sugars, amino acids, fatty acids and glycerol) used for respiration, growth and repair; absorption in the small intestine;
diabetes and food choices; helpful and harmful bacteria in the gut.
UK KS3 enzyme makers are reused.
Wrong answers come from real mistakes: "digestion is finished in the stomach", "the large intestine absorbs most digested food",
"enzymes are living things", "bile is an enzyme".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64208)
R = U.R
P = People(R)
FD = luse(U, "gen_uk_science_y8_food_and_digestion", drop=[r"\bbile\b"])

ORG = [("the mouth", "Teeth break food into small pieces and saliva starts to digest starch."),
       ("the gullet (oesophagus)", "It moves food from the mouth to the stomach by peristalsis."),
       ("the stomach", "It churns food and makes gastric juice with protease and acid to start digesting proteins."),
       ("the small intestine", "It completes digestion and absorbs digested food into the blood."),
       ("the large intestine", "It absorbs water and mineral salts from undigested food."),
       ("the rectum", "It stores faeces before they are removed from the body."),
       ("the anus", "It is the opening through which faeces leave the body."),
       ("the liver", "It makes bile, which breaks fats into small droplets."),
       ("the pancreas", "It makes pancreatic juice with carbohydrase, protease and lipase."),
       ("the gall bladder", "It stores bile until it is needed in the small intestine.")]


def g_org():
    o, j = R.choice(ORG)
    k = R.choice(["job", "which"])
    if not once(("or", o, k)):
        return None
    if k == "job":
        return item("What is the main job of %s?" % o, j, R.sample([x[1] for x in ORG if x[0] != o], 3), "%s: %s" % (o[0].upper() + o[1:], j))
    return item("Which part of the digestive system does this? %s" % j, o, R.sample([x[0] for x in ORG if x[0] != o], 3), "%s: %s" % (o[0].upper() + o[1:], j))


PATH = ["mouth", "gullet", "stomach", "small intestine", "large intestine", "rectum", "anus"]


def g_path():
    i = R.randrange(len(PATH) - 1)
    k = R.choice(["next", "before"])
    if not once(("pa", i, k)):
        return None
    if k == "next":
        a = PATH[i + 1]
        return item("Food passes through the %s. Which part does it enter next?" % PATH[i], "the " + a, ["the " + x for x in R.sample([x for x in PATH + ["liver", "pancreas"] if x not in (a, PATH[i])], 3)],
                    "The order is: mouth → gullet → stomach → small intestine → large intestine → rectum → anus.")
    a = PATH[i]
    return item("Food enters the %s. Which part did it come from?" % PATH[i + 1], "the " + a, ["the " + x for x in R.sample([x for x in PATH + ["liver"] if x not in (a, PATH[i + 1])], 3)],
                "The order is: mouth → gullet → stomach → small intestine → large intestine → rectum → anus.")


DIG = [("Teeth chew a piece of bread into small pieces.", "physical digestion"), ("The stomach walls churn food.", "physical digestion"),
       ("Bile breaks fat into small droplets.", "physical digestion"), ("Amylase in saliva breaks starch into sugars.", "chemical digestion"),
       ("Protease in the stomach breaks proteins into smaller pieces.", "chemical digestion"), ("Lipase breaks fats into fatty acids and glycerol.", "chemical digestion"),
       ("The tongue rolls chewed food into a ball.", "physical digestion"), ("Carbohydrase from the pancreas breaks starch into sugars.", "chemical digestion"),
       ("The incisors bite off a piece of an apple.", "physical digestion"), ("Protease in the small intestine breaks proteins into amino acids.", "chemical digestion")]


def g_dig():
    s, a = R.choice(DIG)
    if not once(("dg", s)):
        return None
    return item(s + " Is this physical or chemical digestion?", a, [x for x in ["physical digestion", "chemical digestion", "absorption", "egestion"] if x != a],
                "Physical digestion breaks food into smaller pieces; chemical digestion uses enzymes to break large molecules into small ones.")


ENZ = [("carbohydrase", "starch (a carbohydrate)", "simple sugars such as glucose", ["the mouth", "the small intestine"]),
       ("protease", "proteins", "amino acids", ["the stomach", "the small intestine"]),
       ("lipase", "fats and oils", "fatty acids and glycerol", ["the small intestine"])]


def g_enz():
    e, sub, prod, where = R.choice(ENZ)
    k = R.choice(["sub", "prod", "enz"])
    if not once(("ez", e, k)):
        return None
    if k == "sub":
        return item("Which food substance does %s digest?" % e, sub, [x[1] for x in ENZ if x[0] != e] + ["water"], "%s digests %s." % (e[0].upper() + e[1:], sub))
    if k == "prod":
        return item("What are the end products when %s %s digested?" % (sub, "are" if sub.split()[0] in ("proteins", "fats") else "is"), prod, [x[2] for x in ENZ if x[0] != e] + ["starch"], "%s → %s" % (sub, prod))
    return item("Which class of enzyme breaks %s down into %s?" % (sub, prod), e, [x[0] for x in ENZ if x[0] != e] + ["bile"], "Enzymes are named after the substance they digest.")


DAM = [("the gall bladder is removed", "Fats are digested more slowly because less bile is released at a time."),
       ("the large intestine absorbs too little water", "The faeces are watery (diarrhoea)."),
       ("the pancreas stops making its juice", "Starch, proteins and fats are not fully digested in the small intestine."),
       ("the stomach makes no acid", "More bacteria in food survive, and stomach protease works poorly."),
       ("part of the small intestine is removed", "Less digested food is absorbed into the blood."),
       ("a person has very few teeth", "Food is not broken into small pieces, so enzymes act more slowly.")]


def g_dam():
    c, a = R.choice(DAM)
    if not once(("dm", c)):
        return None
    return item("What is the most likely effect if %s?" % c, a, R.sample([x[1] for x in DAM if x[0] != c], 3), a)


def g_amy():
    from sg_sci import table
    temps = [10, 20, 30, 40, 50, 60]
    best = R.choice([30, 40])
    t = {x: (R.randint(2, 4) if x == best else 99) for x in temps}
    for x in temps:
        if x != best:
            d = abs(x - best) // 10
            t[x] = t[best] + d * R.randint(3, 5) if x < 60 else 0
    t[60] = 0
    nm = P.next()[0]
    k = R.choice(["best", "60", "why"])
    if not once(("am", best, tuple(t.values()), k)) or not once(("amk", k), 4):
        return None
    rows = [[str(x), ("starch still present after 30 min" if t[x] == 0 else str(t[x]))] for x in temps]
    tb = table(["Temperature (°C)", "Time for starch to disappear (min)"], rows)
    q = tb + "%s mixed amylase with starch at different temperatures and tested with iodine. " % nm
    if k == "best":
        return item(q + "At which temperature did amylase work fastest?", "%d °C" % best, ["%d °C" % x for x in R.sample([x for x in temps if x != best], 3)],
                    "The starch disappeared in the shortest time at %d °C." % best)
    if k == "60":
        return item(q + "Why was starch still present at 60 °C?", "The enzyme was destroyed (denatured) by the high temperature.", ["Amylase works fastest at 60 °C.", "There was no starch.", "Iodine does not work when hot."],
                    "Enzymes are proteins and stop working at high temperatures.")
    return item(q + "How did %s know that the starch had disappeared?" % nm, "The iodine solution stayed brown instead of turning blue-black.", ["The iodine turned blue-black.", "The mixture turned green.", "Bubbles were given off."],
                "Iodine turns blue-black with starch.")


B1 = bank([
    ("Why do we need a digestive system?", "to break large food molecules into small, soluble ones that can be absorbed into the blood", ["to make food larger", "to store food forever", "to make the blood"], "Small molecules can pass through the wall of the small intestine."),
    ("What happens to the products of digestion after they are absorbed?", "They are used for respiration, growth and repair of tissues.", ["They are all removed as faeces.", "They are turned into water.", "They stay in the small intestine."], "Glucose is used in respiration to release energy."),
    ("Where is most digested food absorbed?", "the small intestine", ["the stomach", "the large intestine", "the gullet"], "Its long, folded lining has a large surface area."),
    ("Why is the inner wall of the small intestine folded with many tiny villi?", "to give a large surface area for absorbing digested food", ["to store water", "to make bile", "to chew food"], "A larger surface area speeds up absorption."),
    ("What are enzymes?", "proteins that speed up the breakdown of food without being used up", ["living cells", "a kind of vitamin", "a type of fat"], "Each enzyme acts on one kind of food."),
    ("Is bile an enzyme?", "No. It breaks fats into small droplets so that lipase can work faster.", ["Yes, it digests proteins.", "Yes, it digests starch.", "No, it digests sugar."], "Bile is made in the liver and stored in the gall bladder."),
    ("How do helpful bacteria in the large intestine help us?", "They help to digest some food and make some vitamins.", ["They make stomach acid.", "They cause food poisoning only.", "They absorb all the water."], "Harmful bacteria can cause diarrhoea."),
    ("Which food choices help to prevent type 2 diabetes?", "eating less sugar and refined carbohydrates, more wholegrains and vegetables, and exercising regularly", ["drinking more sweet bubble tea", "eating only white rice", "never exercising"], "Singapore's 'War on Diabetes' encourages healthier choices."),
])
B5 = bank([
    ("A student puts starch solution and saliva in a test tube at 37 °C. After 10 minutes, iodine solution stays brown. What does this show?", "The starch has been digested by amylase in saliva.", ["Starch is still there.", "Saliva contains protein.", "Iodine digests starch."], "Iodine turns blue-black only when starch is present."),
    ("Why does food move along the gullet even when you lie down?", "Muscles in the gullet wall squeeze food along by peristalsis.", ["Gravity always pulls it.", "The teeth push it.", "Air blows it down."], "Peristalsis is wave-like muscle contraction."),
    ("Why do people who eat too little fibre often get constipation?", "Fibre helps the muscles of the intestines push food along.", ["Fibre is digested into glucose.", "Fibre makes acid.", "Fibre stops absorption."], "Wholegrains, fruit and vegetables are rich in fibre."),
    ("A person has part of the small intestine removed. Which problem is most likely?", "Less digested food is absorbed into the blood.", ["Less water is absorbed in the mouth.", "Teeth stop working.", "The stomach makes no acid."], "The small intestine is the main site of absorption."),
    ("Which statement about the stomach is correct?", "It contains acid that kills many bacteria and helps protease work.", ["It absorbs most digested food.", "It digests fats only.", "It makes bile."], "Food leaves the stomach as a semi-liquid."),
    ("Why does chewing food well help digestion?", "It breaks food into smaller pieces with a larger surface area for enzymes to act on.", ["It makes the food bigger.", "It removes all enzymes.", "It stops saliva from working."], "Physical digestion helps chemical digestion."),
])


def body():
    think = ("<p><b>Digestion breaks large food molecules into small, soluble ones that can be absorbed into the blood.</b></p>"
             "<ul><li>Path: mouth → gullet → stomach → small intestine → large intestine → rectum → anus.</li>"
             "<li><b>Physical digestion</b>: teeth, churning, bile. <b>Chemical digestion</b>: enzymes.</li>"
             "<li><b>Carbohydrase</b>: starch → sugars. <b>Protease</b>: proteins → amino acids. <b>Lipase</b>: fats → fatty acids and glycerol.</li>"
             "<li>The <b>small intestine</b> absorbs digested food; the <b>large intestine</b> absorbs water.</li></ul>")
    ex = [("Which enzyme digests proteins, and into what?", ["Name from the food"], "protease, into amino acids"),
          ("Where is most digested food absorbed?", ["Large surface area"], "the small intestine")]
    mist = ["Saying digestion is finished in the stomach. It is completed in the small intestine.", "Saying the large intestine absorbs most food. It absorbs mainly water.",
            "Calling enzymes living things. They are proteins.", "Calling bile an enzyme. It only breaks fat into droplets."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why we digest food", B1[:2] + FD.B1 + [(g_path, 8), (g_org, 5)]),
        ("Parts of the digestive system", [(g_org, 12), (g_path, 4), (B1[2], 1), (B1[3], 1), (g_dig, 2)]),
        ("Physical and chemical digestion", B1[4:6] + [(g_dig, 4), (g_enz, 6), (FD.g_enz, 6), (g_org, 2)]),
        ("Enzymes and absorption", [(g_enz, 3), (FD.g_enz, 3), (g_path, 4), (g_org, 3)] + B1[6:8] + FD.B5[:1] + [(g_dig, 2), (g_amy, 4), (g_dam, 2)]),
        ("Exam-style questions", B5 + FD.B5[1:] + [(g_org, 3), (g_enz, 3), (g_path, 2), (g_dig, 1), (g_amy, 4), (g_dam, 3)]),
    ])
    make_lss(2, "human-digestive-system", 8, "Systems", "Human Digestive System",
             "Explain the importance of the digestive system; explain how the mouth, gullet, stomach, small intestine, large intestine, rectum and anus work together; describe how food "
             "is digested, including carbohydrases, proteases and lipases, and that the products are used for respiration, growth and repair; appreciate food and lifestyle choices in "
             "fighting diabetes; recognise helpful and harmful bacteria in the gut (summary of the MOE Lower Secondary Science Syllabus).",
             "Human Digestive System", seo(2, "Human Digestive System"), "Digestive system",
             "Free Secondary 2 science worksheets for Singapore students on the human digestive system: organs and their jobs, physical and chemical digestion, enzymes and absorption. With answers.",
             "Digestion makes food small enough to absorb.", "Absorbed in the small intestine; water absorbed in the large intestine.",
             body(),
             [("What do digestive enzymes do?", "They speed up the breakdown of large food molecules into small, soluble ones: carbohydrase for starch, protease for proteins, lipase for fats."),
              ("Where is digested food absorbed?", "In the small intestine, whose folded lining gives a large surface area."),
              ("What does the large intestine do?", "It absorbs water and mineral salts from undigested food.")],
             sets)


if __name__ == "__main__":
    main()
