# -*- coding: utf-8 -*-
"""
US High School Biology: Photosynthesis (HS-LS1-5)
  python tools/gen_us_science_bio_photosynthesis.py
Use a model to illustrate how photosynthesis transforms light energy into stored chemical energy.
6CO2 + 6H2O -> C6H12O6 + 6O2 with light; chloroplasts, chlorophyll, light-dependent reactions and the Calvin cycle;
counting molecules from the equation; Elodea bubble data and limiting factors (light, carbon dioxide, temperature).
Wrong answers come from real mistakes: "plants get their mass from the soil", "oxygen comes from carbon dioxide",
"plants only do photosynthesis and never respire".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90105)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


EQ = "6CO<sub>2</sub> + 6H<sub>2</sub>O → C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> + 6O<sub>2</sub>"


def g_ratio():
    n = R.randint(2, 40)
    k = R.choice(["co2", "o2", "h2o", "glu"])
    if not once((n, k)):
        return None
    if k == "co2":
        return item("Equation: %s. How many CO<sub>2</sub> molecules are needed to make %d glucose molecules?" % (EQ, n), str(6 * n), [str(n), str(n + 6), str(12 * n)], "6 CO2 per glucose: 6 × %d = %d." % (n, 6 * n))
    if k == "o2":
        return item("Equation: %s. A leaf makes %d glucose molecules. How many O<sub>2</sub> molecules are released?" % (EQ, n), str(6 * n), [str(n), str(2 * n), str(6 + n)], "6 O2 per glucose.")
    if k == "h2o":
        return item("Equation: %s. How many water molecules are used to make %d glucose molecules?" % (EQ, n), str(6 * n), [str(12 * n), str(n), str(3 * n)], "6 H2O per glucose.")
    m = 6 * n
    return item("Equation: %s. A plant takes in %d CO<sub>2</sub> molecules (with enough water and light). How many glucose molecules can it make?" % (EQ, m), str(n), [str(m), str(6 * m), str(m // 2)],
                "%d ÷ 6 = %d." % (m, n))


IO = [("carbon dioxide", "input"), ("water", "input"), ("light energy", "input"), ("glucose", "output"), ("oxygen", "output")]


def g_io():
    a, k = R.choice(IO)
    t = R.choice(["is", "where"])
    if not once((a, t)):
        return None
    if t == "is":
        return item("In photosynthesis, is %s an input or an output?" % a, k, ["output" if k == "input" else "input", "neither", "a waste that stays in the cell forever"], "Inputs: CO2, H2O, light. Outputs: glucose, O2.")
    src = {"carbon dioxide": "from the air through stomata", "water": "from the soil through the roots", "light energy": "from the sun", "glucose": "made in the chloroplasts",
           "oxygen": "released into the air through stomata"}[a]
    return item("Where does the %s in photosynthesis come from or go?" % a, src, R.sample([v for kk, v in {"carbon dioxide": "from the air through stomata", "water": "from the soil through the roots",
                "light energy": "from the sun", "glucose": "made in the chloroplasts", "oxygen": "released into the air through stomata"}.items() if kk != a], 3), "Follow each molecule.")


def g_elodea():
    who = P.next()[0]
    d = [10, 20, 30, 40, 50]
    base = R.randint(36, 48)
    vals = [base - i * R.randint(6, 8) for i in range(5)]
    k = R.choice(["most", "trend", "diff", "var"])
    if not once((tuple(vals), k)) or not once(("ek", k), {"most": 3, "trend": 3, "var": 3, "diff": 20}[k]):
        return None
    tab = table(["Distance of lamp (cm)", "Oxygen bubbles per minute"], [[str(a), str(b)] for a, b in zip(d, vals)])
    if k == "most":
        return item(tab + "%s tested an Elodea plant. At which distance was photosynthesis fastest?" % who, "10 cm", ["50 cm", "30 cm", "40 cm"], "Most bubbles = fastest rate.")
    if k == "trend":
        return item(tab + "What pattern do %s's data show?" % who, "Closer light (more light) gives more oxygen bubbles.", ["Farther light gives more bubbles.", "Light has no effect.", "Bubbles stop at 20 cm."],
                    "Light is a limiting factor.")
    if k == "var":
        return item(tab + "In %s's test, what is the independent variable?" % who, "the distance of the lamp", ["the number of bubbles", "the type of plant", "the water temperature"], "It is what the student changes.")
    i, j = sorted(R.sample(range(5), 2))
    return item(tab + "How many more bubbles per minute were there at %d cm than at %d cm?" % (d[i], d[j]), str(vals[i] - vals[j]), [str(vals[i]), str(vals[i] + vals[j]), str(vals[i] - vals[j] + 2)],
                "%d − %d = %d." % (vals[i], vals[j], vals[i] - vals[j]))


LIM = [("A greenhouse plant has lots of light and water, but the air has little CO<sub>2</sub>. What limits photosynthesis?", "carbon dioxide", ["light", "water", "oxygen"]),
       ("A plant on a shady forest floor has plenty of water and CO<sub>2</sub>. What limits its photosynthesis?", "light", ["carbon dioxide", "oxygen", "soil"]),
       ("Plants in a drought close their stomata. What drops first?", "the carbon dioxide entering the leaf", ["the light reaching the leaf", "the number of chloroplasts", "the temperature of the sun"]),
       ("On a very cold day, photosynthesis is slow even in bright light. Why?", "The enzymes work slowly at low temperature.", ["There is no light in winter.", "CO2 freezes.", "Chlorophyll is destroyed."]),
       ("A farmer adds CO<sub>2</sub> to a greenhouse. What is the likely effect if light is plentiful?", "Photosynthesis speeds up.", ["Photosynthesis stops.", "Plants make less glucose.", "Nothing at all."]),
       ("Leaves at the top of a tree get more light. Compared with shaded leaves, what do they usually do?", "make more glucose", ["make less glucose", "make no oxygen", "have no chloroplasts"])]


def g_lim():
    q, a, w = R.choice(LIM)
    if not once(q):
        return None
    return item(q, a, w, "The factor in shortest supply limits the rate.")


STAGE = [("Water is split and oxygen is released.", "light-dependent reactions"), ("Light energy is captured by chlorophyll.", "light-dependent reactions"),
         ("ATP and NADPH are made.", "light-dependent reactions"), ("Carbon dioxide is fixed into sugar.", "the Calvin cycle"),
         ("ATP and NADPH are used to build glucose.", "the Calvin cycle"), ("This stage happens in the thylakoid membranes.", "light-dependent reactions"),
         ("This stage happens in the stroma.", "the Calvin cycle"), ("The enzyme RuBisCO grabs CO2.", "the Calvin cycle")]


def g_stage():
    s, a = R.choice(STAGE)
    if not once(s):
        return None
    return item("Which stage of photosynthesis? %s" % s, a, [x for x in ["light-dependent reactions", "the Calvin cycle", "glycolysis", "the Krebs cycle"] if x != a], "Light reactions make ATP/NADPH; the Calvin cycle uses them.")


B1 = bank([
    ("What does photosynthesis do?", "changes light energy into chemical energy stored in glucose", ["changes glucose into light", "breaks down food for energy", "makes water from oxygen"], "Energy is stored in sugar bonds."),
    ("Where does photosynthesis happen in a plant cell?", "in chloroplasts", ["in mitochondria", "in the nucleus", "in the cell wall"], "Chloroplasts contain chlorophyll."),
    ("What pigment captures light?", "chlorophyll", ["hemoglobin", "melanin", "keratin"], "It looks green."),
    ("Why do leaves look green?", "Chlorophyll reflects green light.", ["Chlorophyll absorbs only green light.", "Leaves are made of green sugar.", "Water is green."], "It absorbs red and blue."),
    ("Where does the oxygen released by photosynthesis come from?", "water molecules", ["carbon dioxide", "glucose", "the soil"], "Water is split in the light reactions."),
    ("Where does most of a tree's mass come from?", "carbon dioxide from the air", ["the soil", "the sun's mass", "oxygen"], "Carbon atoms come from CO2."),
    ("Through what openings does CO<sub>2</sub> enter a leaf?", "stomata", ["roots", "xylem", "flowers"], "Guard cells open them."),
    ("Do plants also do cellular respiration?", "Yes, all the time, to use the glucose they make.", ["No, never.", "Only at night in winter.", "Only in their roots."], "Plants need energy too."),
])
B5 = bank([
    ("A plant is kept in the dark for two days. What happens to its stored starch?", "It is used up by respiration.", ["It increases.", "It turns into chlorophyll.", "It stays exactly the same."], "No light, no new sugar."),
    ("A sealed jar with a plant and a mouse keeps the mouse alive longer in light. Why?", "The plant releases oxygen in light.", ["The plant eats carbon dioxide only at night.", "Light makes air.", "The mouse photosynthesizes."], "Classic Priestley experiment."),
    ("Why might a farmer use red and blue grow lights?", "Chlorophyll absorbs red and blue light best.", ["Green light is absorbed best.", "Plants cannot use red light.", "The lights are cheaper only."], "Match the absorption."),
    ("A model shows energy flowing from the sun to glucose. What happens when an animal eats the plant?", "It gets the stored chemical energy.", ["It gets light directly.", "It gets no energy.", "It becomes a producer."], "Energy flows through food."),
    ("Scientists track radioactive oxygen in water. Where does it end up after photosynthesis?", "in the O<sub>2</sub> gas released", ["in glucose", "in CO2", "in the chlorophyll"], "Evidence that O2 comes from water."),
])


def body():
    think = ("<p><b>Light energy → chemical energy (glucose).</b></p>"
             "<p>%s</p><ul><li><b>Light-dependent reactions</b> (thylakoids): light splits water, releases O<sub>2</sub>, makes ATP and NADPH.</li>"
             "<li><b>Calvin cycle</b> (stroma): uses ATP and NADPH to turn CO<sub>2</sub> into glucose.</li>"
             "<li>The rate is limited by light, CO<sub>2</sub> and temperature.</li></ul>") % EQ
    ex = [("How many CO2 molecules make 3 glucose?", ["6 per glucose", "6 × 3"], "18"),
          ("Lamp moves closer, more bubbles. Why?", ["More light"], "Photosynthesis speeds up.")]
    mist = ["Thinking plants get their mass from soil. It comes from CO2.", "Thinking the O2 comes from CO2. It comes from water.", "Thinking plants never do cellular respiration."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Inputs and outputs", B1 + [(g_io, 8), (g_stage, 4)]),
        ("The equation", [(g_ratio, 16), (g_io, 2), (g_stage, 2)]),
        ("Two stages", [(g_stage, 2), (g_ratio, 10), (g_lim, 6), (g_elodea, 2)]),
        ("Elodea data", [(g_elodea, 16), (g_ratio, 4)]),
        ("Limiting factors", B5 + [(g_elodea, 6), (g_ratio, 9)]),
    ])
    make("biology", "photosynthesis", 5, "HS-LS1-5",
         "Use a model to illustrate how photosynthesis transforms light energy into stored chemical energy.",
         "Photosynthesis",
         "Photosynthesis Worksheets: Equation, Light Reactions, Calvin Cycle (High School Biology)",
         "Photosynthesis",
         "Free high school biology worksheets on photosynthesis (NGSS HS-LS1-5): the equation, chloroplasts, light reactions, the Calvin cycle and Elodea data. 100 questions with answers.",
         "Light energy becomes chemical energy.",
         "6CO2 + 6H2O → C6H12O6 + 6O2, powered by light in the chloroplast.",
         body(),
         [("What is the equation for photosynthesis?", "6CO2 + 6H2O → C6H12O6 + 6O2, using light energy captured by chlorophyll."),
          ("What are the two stages?", "The light-dependent reactions in the thylakoids make ATP, NADPH and O2. The Calvin cycle in the stroma uses them to turn CO2 into glucose."),
          ("What limits the rate of photosynthesis?", "Light intensity, carbon dioxide concentration and temperature.")],
         sets)


if __name__ == "__main__":
    main()
