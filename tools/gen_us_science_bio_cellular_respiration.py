# -*- coding: utf-8 -*-
"""
US High School Biology: Cellular Respiration (HS-LS1-7)
  python tools/gen_us_science_bio_cellular_respiration.py
Use a model to illustrate that cellular respiration is a chemical process whereby the bonds of food molecules and oxygen
molecules are broken and the bonds in new compounds are formed, resulting in a net transfer of energy.
C6H12O6 + 6O2 -> 6CO2 + 6H2O + ATP; glycolysis, the Krebs cycle and the electron transport chain; ATP counts
(about 36 aerobic vs 2 anaerobic per glucose); fermentation; yeast balloon data.
Wrong answers come from real mistakes: "respiration means breathing", "plants do not respire", "energy is created",
"fermentation makes more ATP".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90107)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


EQ = "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> + 6O<sub>2</sub> → 6CO<sub>2</sub> + 6H<sub>2</sub>O + energy (ATP)"


def g_ratio():
    n = R.randint(2, 40)
    k = R.choice(["o2", "co2", "h2o"])
    if not once((n, k)):
        return None
    nm = {"o2": "O<sub>2</sub> molecules are used", "co2": "CO<sub>2</sub> molecules are released", "h2o": "water molecules are made"}[k]
    return item("Equation: %s. A cell breaks down %d glucose molecules completely. How many %s?" % (EQ, n, nm), str(6 * n), [str(n), str(2 * n), str(6 + n)],
                "6 per glucose: 6 × %d = %d." % (n, 6 * n))


def g_atp():
    n = R.choice([2, 3, 4, 5, 8, 10, 12, 20, 25, 50, 100])
    k = R.choice(["aer", "ana", "diff"])
    if not once((n, k)):
        return None
    if k == "aer":
        return item("Aerobic respiration makes about 36 ATP per glucose. About how many ATP come from %d glucose molecules?" % n, comma(36 * n), [comma(2 * n), comma(36 + n), comma(18 * n)],
                    "36 × %d = %s." % (n, comma(36 * n)))
    if k == "ana":
        return item("Fermentation makes 2 ATP per glucose. How many ATP come from %d glucose molecules?" % n, comma(2 * n), [comma(36 * n), comma(n), comma(n + 2)], "2 × %d = %s." % (n, comma(2 * n)))
    return item("How many more ATP does aerobic respiration (about 36 per glucose) make than fermentation (2 per glucose) from %d glucose molecules?" % n, comma(34 * n),
                [comma(38 * n), comma(36 * n), comma(34)], "(36 − 2) × %d = %s." % (n, comma(34 * n)))


ST = [("Glucose is split into two pyruvate molecules.", "glycolysis"), ("This stage happens in the cytoplasm and needs no oxygen.", "glycolysis"),
      ("CO<sub>2</sub> is released as carbon atoms are removed in the mitochondrial matrix.", "the Krebs cycle"), ("This stage makes most of the ATP.", "the electron transport chain"),
      ("Oxygen accepts electrons and forms water.", "the electron transport chain"), ("This stage happens on the inner mitochondrial membrane.", "the electron transport chain"),
      ("This stage makes 2 ATP and 2 NADH from one glucose.", "glycolysis"), ("Acetyl-CoA enters a cycle that makes NADH and FADH<sub>2</sub>.", "the Krebs cycle")]


def g_stage():
    s, a = R.choice(ST)
    if not once(s):
        return None
    return item("Which stage of cellular respiration? %s" % s, a, [x for x in ["glycolysis", "the Krebs cycle", "the electron transport chain", "the Calvin cycle"] if x != a],
                "Glycolysis (cytoplasm) → Krebs cycle (matrix) → electron transport chain (inner membrane).")


def g_yeast():
    who = P.next()[0]
    temps = [10, 20, 30, 40, 60]
    base = [R.randint(1, 3), R.randint(5, 8), R.randint(11, 14), R.randint(15, 18), 0]
    k = R.choice(["best", "60", "trend", "var", "diff"])
    if not once((tuple(base), k)) or not once(("yk", k), {"best": 3, "60": 3, "trend": 3, "var": 3, "diff": 20}[k]):
        return None
    tab = table(["Water temperature (°C)", "Balloon width after 20 min (cm)"], [[str(a), str(b)] for a, b in zip(temps, base)])
    if k == "best":
        return item(tab + "%s mixed yeast, sugar and water in bottles with balloons. At which temperature did the yeast respire fastest?" % who, "40 °C", ["10 °C", "60 °C", "20 °C"],
                    "The biggest balloon means the most CO2.")
    if k == "60":
        return item(tab + "Why did the balloon not grow at 60 °C in %s's test?" % who, "The heat killed the yeast or damaged its enzymes.", ["Yeast grows best at 60 °C.", "There was too much sugar.", "Balloons cannot stretch when hot."],
                    "Enzymes stop working when too hot.")
    if k == "trend":
        return item(tab + "What gas filled %s's balloons?" % who, "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"], "Fermentation by yeast releases CO2.")
    if k == "var":
        return item(tab + "In %s's experiment, what is the dependent variable?" % who, "the balloon width (amount of gas)", ["the water temperature", "the kind of yeast", "the size of the bottle"],
                    "It is what is measured.")
    return item(tab + "How much wider was %s's balloon at 40 °C than at 20 °C?" % who, "%d cm" % (base[3] - base[1]), ["%d cm" % base[3], "%d cm" % (base[3] + base[1]), "%d cm" % (base[3] - base[1] + 2)],
                "%d − %d = %d." % (base[3], base[1], base[3] - base[1]))


FERM = [("muscle cells during a hard sprint", "lactic acid fermentation"), ("yeast making bread rise", "alcoholic fermentation"),
        ("bacteria turning milk into yogurt", "lactic acid fermentation"), ("yeast in grape juice making wine", "alcoholic fermentation"),
        ("your leg cells when they feel a burn after running", "lactic acid fermentation"), ("yeast making bubbles in a sugar solution", "alcoholic fermentation")]


def g_ferm():
    s, a = R.choice(FERM)
    if not once(s):
        return None
    return item("Which process happens in %s with too little oxygen?" % s, a, [x for x in ["lactic acid fermentation", "alcoholic fermentation", "photosynthesis", "the Calvin cycle"] if x != a],
                "Fermentation makes a little ATP without oxygen.")


B1 = bank([
    ("What is cellular respiration?", "breaking down glucose with oxygen to release energy as ATP", ["breathing air in and out", "making glucose from light", "copying DNA"], "Not the same as breathing."),
    ("Where does most of cellular respiration happen?", "in the mitochondria", ["in the chloroplasts", "in the nucleus", "in the cell wall"], "The cell's power plants."),
    ("What is ATP?", "a molecule that carries usable energy in cells", ["a type of sugar for storage", "a protein in hair", "a gas we breathe out"], "Cells spend ATP."),
    ("Do plant cells do cellular respiration?", "Yes. All living cells do.", ["No, only animals.", "Only at night.", "Only in the roots."], "Plants respire all the time."),
    ("How are photosynthesis and respiration related?", "The products of one are the reactants of the other.", ["They are the same reaction.", "They both make oxygen.", "They are unrelated."], "Carbon cycles between them."),
    ("Is energy created in cellular respiration?", "No. Energy stored in chemical bonds is transferred to ATP.", ["Yes, from nothing.", "Yes, from oxygen.", "No, energy is destroyed."], "Energy is conserved."),
    ("Why do we breathe faster when exercising?", "Cells need more oxygen for respiration and must remove more CO<sub>2</sub>.", ["To cool the lungs.", "To make glucose.", "To stop respiration."], "More ATP needed."),
    ("Which gas is released by cellular respiration?", "carbon dioxide", ["oxygen", "nitrogen", "hydrogen"], "We breathe it out."),
])
B5 = bank([
    ("Bromothymol blue turns yellow when CO<sub>2</sub> is added. A snail in a tube makes the liquid yellow. What does this show?", "The snail releases CO<sub>2</sub> from respiration.", ["The snail makes oxygen.", "The snail does photosynthesis.", "Nothing."], "An indicator for CO2."),
    ("A sprinter's muscles run short of oxygen. What builds up?", "lactic acid", ["alcohol", "oxygen", "starch"], "Lactic acid fermentation."),
    ("Germinating seeds in a sealed jar make the air warmer. Why?", "Respiration releases some energy as heat.", ["Seeds make light.", "Seeds do photosynthesis in the dark.", "Glass makes heat."], "Not all energy goes into ATP."),
    ("Cyanide blocks the electron transport chain. Why is it deadly?", "Cells can no longer make most of their ATP.", ["It makes extra ATP.", "It speeds up glycolysis to make enough ATP.", "It only affects plants."], "The ETC makes most ATP."),
    ("A model shows glucose's carbon atoms ending up in CO<sub>2</sub>. Which process does it show?", "cellular respiration", ["photosynthesis", "transcription", "mitosis"], "Carbon leaves as CO2."),
])


def body():
    think = ("<p><b>Food + oxygen → CO<sub>2</sub> + water + usable energy (ATP).</b></p><p>%s</p>"
             "<ul><li>Glycolysis (cytoplasm) → Krebs cycle (matrix) → electron transport chain (inner membrane).</li>"
             "<li>With oxygen: about 36 ATP per glucose. Without oxygen (fermentation): 2 ATP.</li></ul>") % EQ
    ex = [("5 glucose broken down completely. CO2 released?", ["6 per glucose", "6 × 5"], "30"),
          ("10 glucose by fermentation. ATP?", ["2 per glucose", "2 × 10"], "20")]
    mist = ["Thinking respiration means breathing.", "Thinking plants do not respire.", "Thinking energy is created. It is transferred.", "Thinking fermentation makes more ATP. It makes far less."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Respiration basics", B1 + [(g_ratio, 6), (g_stage, 6)]),
        ("The equation", [(g_ratio, 14), (g_stage, 2), (g_ferm, 4)]),
        ("Counting ATP", [(g_atp, 16), (g_ferm, 2), (g_ratio, 2)]),
        ("Yeast experiments", [(g_yeast, 16), (g_atp, 4)]),
        ("Energy in living things", B5 + [(g_atp, 8), (g_yeast, 4), (g_ratio, 3)]),
    ])
    make("biology", "cellular-respiration", 7, "HS-LS1-7",
         "Use a model to illustrate that cellular respiration is a chemical process whereby the bonds of food molecules and oxygen molecules are broken and the bonds in new compounds are formed resulting in a net transfer of energy.",
         "Cellular Respiration",
         "Cellular Respiration Worksheets: Glycolysis, Krebs Cycle, ATP and Fermentation (Biology)",
         "Cellular Respiration",
         "Free high school biology worksheets on cellular respiration (NGSS HS-LS1-7): the equation, glycolysis, the Krebs cycle, the electron transport chain, ATP and fermentation. 100 questions with answers.",
         "Food + oxygen → ATP.",
         "Bonds in glucose and oxygen break, new bonds form in CO2 and water, and energy moves to ATP.",
         body(),
         [("What is the equation for cellular respiration?", "C6H12O6 + 6O2 → 6CO2 + 6H2O + energy (ATP)."),
          ("What are the three stages?", "Glycolysis in the cytoplasm, the Krebs cycle in the mitochondrial matrix and the electron transport chain on the inner membrane."),
          ("How is fermentation different?", "It happens without oxygen and makes only 2 ATP per glucose, with lactic acid or alcohol and CO2 as products.")],
         sets)


if __name__ == "__main__":
    main()
