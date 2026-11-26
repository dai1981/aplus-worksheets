# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Biology): Respiration
  python tools/gen_uk_science_y8_respiration.py
Aerobic and anaerobic respiration in living organisms: the word equations, where respiration happens (mitochondria),
the breakdown of glucose to release energy, anaerobic respiration in muscles (lactic acid, oxygen debt) and in yeast
(fermentation: ethanol and carbon dioxide), and comparing respiration with photosynthesis and with burning.
Reuses the input/output, comparison, yeast and body questions of the US Grade 7 unit in British English.
Wrong answers come from real mistakes: "respiration is breathing", "plants do not respire", "respiration makes energy",
"anaerobic respiration releases more energy".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61803)
R = U.R
P = People(R)
uk_sci.USED.clear()
CR = adopt_us("gen_us_science_g7_cellular_respiration", U)
us_io, us_cmp, us_yeast, us_body = ukm(CR.g_io), ukm(CR.g_compare), ukm(CR.g_yeast), ukm(CR.g_body)

EQ = {"aerobic": ("glucose + oxygen", "carbon dioxide + water"),
      "anaerobic in muscles": ("glucose", "lactic acid"),
      "anaerobic in yeast (fermentation)": ("glucose", "ethanol + carbon dioxide")}
ALLP = ["carbon dioxide + water", "lactic acid", "ethanol + carbon dioxide", "glucose + oxygen", "oxygen + water"]


def g_eq():
    kind = R.choice(sorted(EQ))
    k = R.random() < 0.5
    if not once(("eq", kind, k)):
        return None
    inp, out = EQ[kind]
    if k:
        return item("Complete the word equation for %s respiration: %s → ?" % (kind, inp), out, [x for x in ALLP if x != out][:3],
                    "Aerobic: glucose + oxygen → carbon dioxide + water. Muscles without oxygen: glucose → lactic acid. Yeast: glucose → ethanol + carbon dioxide.")
    w = [x for x in sorted(EQ) if x != kind] + ["photosynthesis"]
    return item("Which type of respiration has this word equation: %s → %s?" % (inp, out), kind + " respiration" if kind != "photosynthesis" else kind,
                [x + " respiration" if x != "photosynthesis" else x for x in w], "Look for oxygen as a reactant and for the products.")


FACT = [("needs oxygen", "aerobic", "anaerobic"), ("releases more energy from each glucose molecule", "aerobic", "anaerobic"),
        ("can happen when there is no oxygen", "anaerobic", "aerobic"), ("produces lactic acid in human muscles", "anaerobic", "aerobic"),
        ("is used to make bread rise and to brew beer", "anaerobic", "aerobic"), ("produces water", "aerobic", "anaerobic"),
        ("happens in muscles during a sprint when not enough oxygen arrives", "anaerobic", "aerobic"),
        ("goes on all the time in the cells of a resting person", "aerobic", "anaerobic")]


def g_type():
    f, a, b = R.choice(FACT)
    if not once(("ty", f)):
        return None
    return item("Which type of respiration %s?" % f, a + " respiration", [b + " respiration", "photosynthesis", "breathing"],
                "Aerobic uses oxygen and releases more energy; anaerobic needs no oxygen and releases less.")


WHERE = [("Where in a cell does most aerobic respiration happen?", "in the mitochondria", ["in the nucleus", "in the cell wall", "in the vacuole"]),
         ("Which living things respire?", "all living things, including plants", ["only animals", "only plants", "only humans"]),
         ("When do plants respire?", "all the time, day and night", ["only at night", "only in sunlight", "never"]),
         ("What is respiration for?", "to release energy from glucose for the cell", ["to make energy from nothing", "to move air in and out", "to make glucose"]),
         ("How does glucose reach muscle cells?", "in the blood plasma", ["through the lungs only", "in red blood cells only", "through the skin"]),
         ("How does oxygen reach muscle cells?", "carried by red blood cells", ["dissolved in lactic acid", "through the stomach", "in the bones"])]


def g_where():
    q, a, w = R.choice(WHERE)
    if not once(("wh", q)):
        return None
    return item(q, a, w, "Respiration happens in every living cell.")


def g_sprint():
    who = P.next()[0]
    rest = R.choice([60, 64, 68, 70, 72])
    peak = rest + R.choice([60, 70, 80, 90])
    back = R.choice([3, 4, 5, 6, 8])
    k = R.choice(["why", "pant", "rise", "rec"])
    if not once(("sp", rest, peak, k)) or not once(("sp", k), 2 if k in ("why", "pant") else 5):
        return None
    tab = table(["Time", "Heart rate (beats per minute)"], [["before the sprint", str(rest)], ["just after the sprint", str(peak)], ["%d minutes later" % back, str(rest)]])
    intro = tab + "%s ran a 200 m sprint. " % who
    if k == "why":
        return item(intro + "Why did the heart rate rise?", "to carry more oxygen and glucose to the muscles for respiration", ["to cool the body down", "because the heart was tired", "to make lactic acid faster"], "More respiration needs more oxygen.")
    if k == "pant":
        return item(intro + "Why did the runner keep breathing hard after stopping?", "to repay the oxygen debt and break down lactic acid", ["to make more lactic acid", "because the lungs were empty", "to digest food"], "Oxygen debt.")
    if k == "rise":
        d = peak - rest
        return item(intro + "By how much did the heart rate rise?", "%d beats per minute" % d, uniq("%d beats per minute" % d, ["%d beats per minute" % peak, "%d beats per minute" % rest, "%d beats per minute" % (peak + rest)]), "%d − %d = %d." % (peak, rest, d))
    return item(intro + "How long did the heart rate take to return to normal?", "%d minutes" % back, uniq("%d minutes" % back, ["%d minutes" % x for x in (1, 2, 3, 4, 5, 6, 8, 10)]), "Read the last row.")


def g_peas():
    who = P.next()[0]
    t0 = R.choice([18, 19, 20, 21, 22])
    up = R.choice([3, 4, 5, 6, 7, 8])
    k = R.choice(["why", "ctrl", "rise", "conc", "fair"])
    if not once(("pe", t0, up, k)) or not once(("pe", k), 2 if k in ("why", "ctrl", "conc", "fair") else 8):
        return None
    tab = table(["Flask", "Start (°C)", "After 2 days (°C)"], [["A: live germinating peas", str(t0), str(t0 + up)], ["B: boiled (dead) peas", str(t0), str(t0)]])
    intro = tab + "%s put peas in two vacuum flasks with thermometers. " % who
    if k == "why":
        return item(intro + "Why did flask A get warmer?", "The live peas respired and released energy as heat.", ["The peas photosynthesised.", "The flask made heat.", "Boiled peas absorbed the cold."], "Respiration transfers energy.")
    if k == "ctrl":
        return item(intro + "Why was flask B included?", "as a control, to show the rise is caused by living peas", ["to make the test quicker", "to keep the peas cool", "it was not needed"], "Compare with no respiration.")
    if k == "rise":
        g = "%d °C" % up
        return item(intro + "By how much did the temperature in flask A rise?", g, uniq(g, ["%d °C" % (t0 + up), "%d °C" % t0, "%d °C" % (up + 2), "0 °C"]), "%d − %d = %d." % (t0 + up, t0, up))
    if k == "conc":
        return item(intro + "What can you conclude?", "Living seeds respire and release energy.", ["Dead seeds respire faster.", "Seeds do not respire.", "Respiration absorbs heat."], "Only the live peas warmed.")
    return item(intro + "Which variable should be kept the same in both flasks?", "the mass of peas", ["whether the peas are alive", "the temperature after 2 days", "the colour of the flask label only"], "Change only alive/dead.")


def g_ytemp():
    who = P.next()[0]
    temps = [10, 25, 40, 60]
    best = R.choice([30, 35, 40])
    temps = [5, 20, best, 70]
    v = [R.choice([2, 3, 4]), R.choice([10, 12, 14, 15]), R.choice([24, 26, 28, 30, 32]), 0]
    k = R.choice(["best", "hot", "cold", "diff", "dep"])
    if not once(("yt", best, v[1], v[2], k)) or not once(("yt", k), 2 if k in ("hot", "cold", "dep") else 8):
        return None
    tab = table(["Temperature (°C)", "Bubbles of gas per minute"], [[str(t), str(x)] for t, x in zip(temps, v)])
    intro = tab + "%s counted bubbles from yeast in sugar solution at different temperatures. " % who
    if k == "best":
        g = "%d °C" % best
        return item(intro + "At which temperature did the yeast respire fastest?", g, ["%d °C" % t for t in temps if t != best], "Most bubbles per minute.")
    if k == "hot":
        return item(intro + "Why were there no bubbles at 70 °C?", "The heat killed the yeast and destroyed its enzymes.", ["The sugar ran out.", "Yeast respires fastest when hot.", "The gas was too hot to see."], "Enzymes are damaged by high temperatures.")
    if k == "cold":
        return item(intro + "Why were there only a few bubbles at 5 °C?", "Respiration is slow when it is cold.", ["The yeast was dead.", "There was no sugar.", "Cold yeast makes oxygen instead."], "Reactions slow down in the cold.")
    if k == "diff":
        d = v[2] - v[1]
        return item(intro + "How many more bubbles per minute were there at %d °C than at 20 °C?" % best, str(d), uniq(str(d), [str(v[2]), str(v[1]), str(v[2] + v[1]), str(d + 5)]), "%d − %d = %d." % (v[2], v[1], d))
    return item(intro + "What is the dependent variable?", "the number of bubbles per minute", ["the temperature", "the type of yeast", "the amount of sugar"], "What is measured.")


B1 = bank([
    ("Is respiration the same as breathing?", "No. Respiration is a chemical reaction in cells; breathing moves air in and out of the lungs.", ["Yes, they are the same.", "Respiration happens in the lungs only.", "Breathing releases energy from glucose."], "A common mix-up."),
    ("Does respiration make energy?", "No. It releases energy stored in glucose.", ["Yes, from nothing.", "Yes, from oxygen alone.", "It makes glucose."], "Energy is transferred, not made."),
    ("What is the energy from respiration used for?", "moving, keeping warm, growing and repairing cells", ["only for thinking", "nothing", "making oxygen"], "Many life processes."),
    ("Which test shows that exhaled air contains carbon dioxide?", "Breathe through limewater: it turns milky.", ["Iodine turns blue-black.", "A glowing splint relights.", "Litmus turns blue."], "Limewater test."),
    ("What gas do we need for aerobic respiration?", "oxygen", ["carbon dioxide", "nitrogen", "hydrogen"], "Breathed in."),
    ("Which sugar is broken down in respiration?", "glucose", ["starch", "cellulose", "lactose only"], "From digested food."),
    ("Which organelle is called the powerhouse of the cell?", "the mitochondrion", ["the nucleus", "the chloroplast", "the cell membrane"], "Site of aerobic respiration."),
    ("Why do muscle cells contain many mitochondria?", "They need to release a lot of energy for movement.", ["They store fat.", "They make glucose.", "They need no energy."], "Structure fits function."),
    ("Why do muscles ache after hard exercise?", "Lactic acid builds up from anaerobic respiration.", ["The bones are broken.", "Too much oxygen.", "The muscles are digesting food."], "It is removed later with oxygen."),
])
B5 = bank([
    ("Why does bread rise?", "Yeast respires anaerobically and the carbon dioxide gas makes bubbles in the dough.", ["The oven adds air.", "Flour expands in heat.", "The yeast makes oxygen."], "Fermentation."),
    ("Why is the ethanol in bread not a problem?", "It evaporates during baking.", ["Bread has no ethanol.", "It turns into sugar.", "It is removed with water."], "Cooked off."),
    ("How is respiration like burning?", "Both use oxygen and release energy, carbon dioxide and water from a fuel.", ["Both happen only in flames.", "Both make glucose.", "Neither releases energy."], "Respiration is slow and controlled."),
    ("Germinating peas in a flask get warmer over two days. Why?", "They are respiring and releasing energy as heat.", ["They are photosynthesising in the dark.", "The flask makes heat.", "Peas absorb heat from nothing."], "Seeds respire."),
    ("Why do athletes train at high altitude?", "The body makes more red blood cells, so more oxygen reaches the muscles.", ["There is more oxygen up high.", "It makes them breathe less.", "Lactic acid cannot form there."], "Adaptation of the body."),
])


def body():
    think = ("<p><b>Respiration is a chemical reaction in every living cell that releases energy from glucose.</b></p>"
             "<ul><li>Aerobic: glucose + oxygen → carbon dioxide + water (in the mitochondria; releases a lot of energy).</li>"
             "<li>Anaerobic in muscles: glucose → lactic acid. In yeast: glucose → ethanol + carbon dioxide.</li>"
             "<li>After hard exercise we keep breathing hard to repay the oxygen debt.</li></ul>")
    ex = [("Yeast without oxygen makes?", ["Fermentation"], "ethanol + carbon dioxide"),
          ("Which type releases more energy?", ["Glucose is fully broken down"], "aerobic")]
    mist = ["Thinking respiration is breathing.", "Thinking plants do not respire.", "Saying respiration makes energy (it releases it)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What respiration is", B1 + [(g_where, 6), (us_io, 5)]),
        ("Aerobic and anaerobic", [(g_type, 8), (g_eq, 5), (us_cmp, 5), (us_body, 2)]),
        ("Exercise", [(g_sprint, 12), (us_cmp, 4), (us_body, 2), (us_yeast, 2)]),
        ("Living things respire", [(g_peas, 12), (g_ytemp, 8)]),
        ("Thinking about respiration", B5 + [(g_ytemp, 10), (g_peas, 2), (g_sprint, 1), (us_yeast, 1), (g_eq, 1)]),
    ])
    make_ks3(8, "respiration", 3, "Biology", "Cellular processes and respiration",
             "Aerobic and anaerobic respiration in living organisms, including the breakdown of organic molecules to enable all the other chemical processes necessary for life; a word summary for aerobic respiration; the process of anaerobic respiration in humans and micro-organisms, including fermentation, and a word summary for anaerobic respiration; the differences between aerobic and anaerobic respiration in terms of the reactants, the products formed and the implications for the organism.",
             "Respiration",
             "Year 8 Science: Respiration Worksheets (Aerobic, Anaerobic, Fermentation)",
             "Respiration",
             "Free Year 8 science worksheets on respiration: aerobic and anaerobic word equations, mitochondria, lactic acid and oxygen debt, yeast and fermentation. 100 questions with answers.",
             "Respiration releases energy from glucose.",
             "Aerobic needs oxygen and releases more energy; anaerobic needs none.",
             body(),
             [("What is the word equation for aerobic respiration?", "Glucose + oxygen → carbon dioxide + water. It happens in the mitochondria and releases energy for the cell."),
              ("What is anaerobic respiration?", "Respiration without oxygen. In human muscles glucose becomes lactic acid; in yeast it becomes ethanol and carbon dioxide. It releases much less energy."),
              ("Do plants respire?", "Yes. All living cells respire all the time, day and night. Plants photosynthesise only in the light.")],
             sets)


if __name__ == "__main__":
    main()
