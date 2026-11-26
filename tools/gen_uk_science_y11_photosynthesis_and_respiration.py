# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Biology): Photosynthesis and Respiration (Bioenergetics)
  python tools/gen_uk_science_y11_photosynthesis_and_respiration.py
Photosynthesis as an endothermic reaction, its equations, limiting factors (light, carbon dioxide, temperature), the
inverse square law for light intensity (higher tier), uses of glucose, aerobic and anaerobic respiration in muscles,
plants and yeast, the response to exercise and oxygen debt, and metabolism. Reuses the US Biology photosynthesis and
respiration questions in British English.
Wrong answers come from real mistakes: "plants get glucose from the soil", "anaerobic respiration makes carbon dioxide
in muscles", "moving the lamp twice as far halves the light", "plants only respire at night".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62101)
PH, CR = "bio_photosynthesis", "bio_cellular_respiration"
NOATP = (("energy (ATP)", "energy"), ("+ ATP", "+ energy"))
us_elodea, us_io, us_lim = us(PH, "g_elodea"), us(PH, "g_io"), us(PH, "g_lim")
us_pratio = us(PH, "g_ratio")
us_rratio = us(CR, "g_ratio", rep=NOATP, drop=("ATP",))
us_yeast = us(CR, "g_yeast")

EQ = [("photosynthesis", "carbon dioxide + water", "glucose + oxygen"),
      ("aerobic respiration", "glucose + oxygen", "carbon dioxide + water"),
      ("anaerobic respiration in muscles", "glucose", "lactic acid"),
      ("anaerobic respiration in yeast (fermentation)", "glucose", "ethanol + carbon dioxide")]


def g_eq():
    n, re_, pr = R.choice(EQ)
    k = R.choice(["in", "out", "which"])
    if not once(("eq", n, k)):
        return None
    if k == "which":
        return item("Which process is this? %s → %s" % (re_, pr), n, [x[0] for x in EQ if x[0] != n], "Match the reactants and products.")
    a = re_ if k == "in" else pr
    pool = sorted(set([x[1] for x in EQ] + [x[2] for x in EQ]) - {a})
    if k == "in" and n == "anaerobic respiration in yeast (fermentation)":
        pool = [x for x in pool if x != "glucose"]
    return item("What are the %s of %s?" % ("reactants" if k == "in" else "products", n), a, R.sample(pool, 3),
                "%s: %s → %s." % (n[0].upper() + n[1:], re_, pr))


def g_isq():
    d = R.choice([5, 10, 15, 20, 25, 30])
    m = R.choice([2, 3, 4])
    up = R.random() < 0.5
    if not once(("isq", d, m, up)):
        return None
    if up:
        a = "It becomes 1/%d as much." % (m * m)
        w = ["It becomes 1/%d as much." % m, "It stays the same.", "It becomes %d times as much." % (m * m)]
        return item("A lamp is %d cm from a pondweed. It is moved to %d cm. What happens to the light intensity?" % (d, d * m), a, w,
                    "Light intensity ∝ 1/distance². %d times the distance → 1/%d²." % (m, m))
    a = "It becomes %d times as much." % (m * m)
    w = ["It becomes %d times as much." % m, "It stays the same.", "It becomes 1/%d as much." % (m * m)]
    return item("A lamp is %d cm from a pondweed. It is moved to %d cm. What happens to the light intensity?" % (d * m, d), a, w,
                "Light intensity ∝ 1/distance². 1/%d of the distance → %d² times." % (m, m))


def g_ex():
    rest = R.choice([60, 64, 68, 70, 72, 75, 78])
    up = R.choice([40, 45, 50, 55, 60, 64, 70])
    k = R.choice(["inc", "inc", "above", "above", "pct", "why", "back"])
    if k == "pct" and up * 100 % rest:
        return None
    if not once(("ex", rest, up, k)) or (k in ("why", "back") and not once(("exk", k), 2)):
        return None
    tab = table(["", "Heart rate (beats per minute)"], [["at rest", str(rest)], ["after 5 minutes of running", str(rest + up)], ["5 minutes after stopping", str(rest + up // 4)]])
    name, _, pos = P.next()
    if k == "inc":
        return item(tab + "These are %s's results. By how much did %s heart rate increase during exercise?" % (name, pos), "%d beats per minute" % up,
                    ["%d beats per minute" % (rest + up), "%d beats per minute" % (up // 4), "%d beats per minute" % rest], "%d − %d = %d." % (rest + up, rest, up))
    if k == "above":
        return item(tab + "These are %s's results. 5 minutes after stopping, how far above the resting rate is %s heart rate?" % (name, pos), "%d beats per minute" % (up // 4),
                    ["%d beats per minute" % up, "%d beats per minute" % (rest + up // 4), "%d beats per minute" % (up - up // 4)], "%d − %d = %d. Extra oxygen is still needed (the oxygen debt)." % (rest + up // 4, rest, up // 4))
    if k == "pct":
        pc = up * 100 // rest
        return item(tab + "These are %s's results. What is the percentage increase in %s heart rate during exercise?" % (name, pos), "%d%%" % pc,
                    ["%d%%" % up, "%d%%" % (pc + 100), "%d%%" % (100 - pc if pc < 100 else pc // 2)], "%d ÷ %d × 100 = %d%%." % (up, rest, pc))
    if k == "why":
        return item(tab + "%s ran for 5 minutes and %s heart rate rose to %d beats per minute. Why does the heart rate increase during exercise?" % (name, pos, rest + up),
                    "to carry more oxygen and glucose to the muscles", ["to make more lactic acid", "to cool the blood down", "to slow down respiration"], "Muscles respire faster.")
    return item(tab + "%s's heart rate was still %d beats per minute 5 minutes after stopping. Why is it still above the resting rate?" % (name, rest + up // 4),
                "Extra oxygen is needed to break down lactic acid (the oxygen debt).", ["The muscles have stopped respiring.", "Glucose is made in the muscles.", "The lungs have stopped working."],
                "Lactic acid is taken to the liver and converted back to glucose.")


B1 = bank([
    ("Why is photosynthesis an endothermic reaction?", "Energy from light is taken in.", ["It gives out heat.", "It releases oxygen.", "It happens in the dark."], "Light energy is transferred to the chloroplasts."),
    ("Where in a plant cell does photosynthesis happen?", "in the chloroplasts", ["in the mitochondria", "in the nucleus", "in the cell wall"], "Chlorophyll absorbs light."),
    ("Name one use of the glucose made in photosynthesis.", "to make cellulose for cell walls", ["to make chlorophyll from carbon dioxide only", "to make oxygen", "to absorb light"], "Also respiration, starch for storage, fats, oils and amino acids (with nitrate ions)."),
    ("Why do plants store glucose as starch?", "Starch is insoluble, so it does not affect water movement in cells.", ["Starch is sweeter.", "Starch dissolves easily.", "Starch makes the leaf green."], "Insoluble store."),
])
B3 = bank([
    ("What is a limiting factor?", "the factor in shortest supply that stops the rate rising", ["the factor in greatest supply", "anything that kills the plant", "the product of photosynthesis"], "Light, CO₂ or temperature."),
    ("Why does photosynthesis slow down at very high temperatures?", "The enzymes are denatured.", ["There is too much light.", "Carbon dioxide runs out.", "The plant has too much water."], "Enzymes change shape."),
    ("How can a farmer increase photosynthesis in a greenhouse in winter?", "Use heaters, lamps and extra carbon dioxide.", ["Remove the soil.", "Shade the plants.", "Lower the temperature."], "Remove limiting factors, if it pays for itself."),
])
B5 = bank([
    ("Which type of respiration releases more energy per glucose?", "aerobic respiration", ["anaerobic respiration in muscles", "fermentation", "they release the same"], "Glucose is fully oxidised."),
    ("Do plants respire at night only?", "No, plants respire all the time.", ["Yes, only at night.", "No, only in the day.", "Plants never respire."], "Photosynthesis needs light; respiration does not."),
    ("What is metabolism?", "the sum of all the reactions in a cell or the body", ["breathing only", "digestion only", "the speed of the heart"], "Includes making starch, proteins and lipids."),
    ("Why do muscles feel tired after hard exercise?", "Lactic acid builds up in the muscles.", ["Oxygen builds up.", "Glucose is made.", "The muscles stop needing energy."], "Anaerobic respiration."),
    ("What is fermentation used for?", "making bread and alcoholic drinks", ["making oxygen", "making lactic acid in yeast", "making chlorophyll"], "Yeast makes ethanol and carbon dioxide."),
])

if __name__ == "__main__":
  build(U, 11, "photosynthesis-and-respiration", 1, "Biology", "Bioenergetics",
      "Photosynthesis as an endothermic reaction and its equation; the rate of photosynthesis and limiting factors (temperature, light intensity, carbon dioxide); the inverse square law (higher tier); uses of glucose; aerobic and anaerobic respiration; the response to exercise and the oxygen debt; metabolism.",
      "Photosynthesis and Respiration", "Photosynthesis and Respiration",
      "Free Year 11 GCSE Combined Science worksheets on bioenergetics: photosynthesis, limiting factors, the inverse square law, aerobic and anaerobic respiration, exercise and oxygen debt. 100 questions with answers.",
      "Photosynthesis stores energy; respiration releases it.",
      "Anaerobic respiration in muscles makes lactic acid only.",
      "<p><b>Plants make glucose; every living cell respires it.</b></p><ul><li>Photosynthesis: carbon dioxide + water → glucose + oxygen (light energy is taken in).</li>"
      "<li>The rate is limited by light, carbon dioxide or temperature. Light intensity ∝ 1/distance².</li>"
      "<li>Aerobic: glucose + oxygen → carbon dioxide + water. Anaerobic in muscles: glucose → lactic acid. In yeast: glucose → ethanol + carbon dioxide.</li></ul>",
      [("Lamp from 10 cm to 20 cm. Light intensity?", ["2 × distance", "1/2² = 1/4"], "1/4 as much"), ("Products of anaerobic respiration in muscles?", ["No oxygen used"], "lactic acid")],
      ["Thinking plants get their glucose from the soil.", "Thinking anaerobic respiration in muscles makes carbon dioxide.", "Thinking double the distance gives half the light (it is a quarter)."],
      [("What limits the rate of photosynthesis?", "Light intensity, carbon dioxide concentration and temperature. The one in shortest supply is the limiting factor."),
       ("What is the difference between aerobic and anaerobic respiration?", "Aerobic respiration uses oxygen and releases much more energy. Anaerobic respiration does not use oxygen; in muscles it makes lactic acid, in yeast it makes ethanol and carbon dioxide."),
       ("What is the oxygen debt?", "The extra oxygen needed after exercise to react with the lactic acid that built up in the muscles.")],
      [("Photosynthesis", B1 + [(g_eq, 4), (us_io, 6), (us_pratio, 6)]),
       ("Limiting factors", B3 + [(us_lim, 5), (us_elodea, 8), (g_isq, 4)]),
       ("Light intensity", [(g_isq, 10), (us_elodea, 5), (us_pratio, 5)]),
       ("Respiration", [(g_eq, 4), (us_rratio, 8), (us_yeast, 8)]),
       ("Exercise and metabolism", B5 + [(g_ex, 12), (us_rratio, 3)])])
