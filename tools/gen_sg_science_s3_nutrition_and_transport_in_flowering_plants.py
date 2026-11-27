# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 10: Nutrition and Transport in Flowering Plants
  python tools/gen_sg_science_s3_nutrition_and_transport_in_flowering_plants.py
Leaf structure and adaptations; photosynthesis (word and chemical equations, chlorophyll, light, carbon dioxide and temperature as
limiting factors, testing leaves for starch, the use of nitrate and magnesium ions); xylem and phloem; uptake of water by root hair
cells; transpiration and the factors that affect it; wilting; translocation of sucrose and amino acids in the phloem.
UK KS3/KS4 photosynthesis and plant makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "plants get their food from the soil", "phloem carries water", "transpiration is faster in
humid air", "stomata are mainly on the upper surface", "the light intensity halves when the lamp is twice as far".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool, ex

LV, SUBJ, SORT = 3, "Biology", 23
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_isq = src("gen_uk_science_y11_photosynthesis_and_respiration", "g_isq")
uk_leafad = src("gen_uk_science_y8_photosynthesis", "g_leafad")
uk_starch = src("gen_uk_science_y8_photosynthesis", "g_starch")
uk_plant = src("gen_uk_science_y10_organisation_and_enzymes", "g_plant", drop=["absorb water", "open and close"])
uk_rate = src("gen_uk_science_y8_photosynthesis", "g_rate")

LEAF = [("the waxy cuticle", "reduces water loss by evaporation"), ("the upper epidermis", "is transparent and lets light through to the mesophyll"),
        ("palisade mesophyll cells", "are packed with chloroplasts and carry out most photosynthesis"),
        ("spongy mesophyll", "has many air spaces for gases to diffuse through the leaf"),
        ("stomata", "let carbon dioxide in and oxygen and water vapour out"), ("guard cells", "open and close the stomata"),
        ("xylem in the veins", "brings water and mineral ions to the leaf"), ("phloem in the veins", "carries sucrose away from the leaf")]
g_leaf = rows(R, LEAF, "What is the role of %s in a leaf?", "Which part of a leaf %s?")

TRP = [("higher temperature", "faster"), ("higher humidity", "slower"), ("windy conditions", "faster"), ("brighter light", "faster"),
       ("lower temperature", "slower"), ("still air", "slower"), ("drier air", "faster"), ("darkness (stomata close)", "slower")]


def g_trp():
    c, a = R.choice(TRP)
    return tq("What is the effect of %s on the rate of transpiration?" % c, a, [x for x in ("faster", "slower", "no change", "transpiration stops") if x != a],
              "Transpiration is faster when the air is warm, dry and moving and the stomata are open in light.")


def g_pot():
    d = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15])
    t = R.choice([2, 4, 5, 10])
    rate = d / t
    return nq("In a potometer, the air bubble moves %d cm along the tube in %d minutes. What is the rate of water uptake in cm per minute?" % (d, t), rate,
              [t / d, d * t, d], " cm/min", "Rate = distance ÷ time = %d ÷ %d." % (d, t), sf=3)


def g_pot2():
    r_ = R.choice([0.5, 1, 1.5, 2, 2.5, 3])
    area = R.choice([0.5, 1, 2])
    d = R.choice([5, 6, 8, 10, 12])
    vol = d * area
    return nq("The capillary tube of a potometer has a cross-sectional area of %s mm². The bubble moves %d mm. What volume of water was taken up?" % (ex(area), d), vol,
              [d / area, d + area, area], " mm³", "Volume = area × distance = %s × %d." % (ex(area), d))


def g_isq():
    b = R.choice([5, 10, 15, 20, 25])
    k = R.choice([2, 3, 4, 5])
    d1, d2 = (b, b * k) if R.random() < 0.6 else (b * k, b)
    if d1 > 100 or d2 > 100:
        return None
    from fractions import Fraction as F
    r_ = F(d1, d2) ** 2
    def show(x):
        if x.denominator == 1:
            return "%d times as much" % x.numerator
        if x.numerator == 1:
            return "1/%d as much" % x.denominator
        return "%d/%d as much" % (x.numerator, x.denominator)
    if r_ == 1:
        return None
    lin = F(d1, d2)
    wr = [show(lin), show(1 / r_), "the same"]
    a = show(r_)
    if len({a} | set(wr)) < 4:
        return None
    return tq("A lamp is moved from %d cm to %d cm from a water plant. What happens to the light intensity reaching the plant?" % (d1, d2), a, wr,
              "Light intensity ∝ 1 ÷ distance²: (%d ÷ %d)² = %s." % (d1, d2, a.replace(" as much", "")))


def g_bub():
    n = R.choice([12, 15, 18, 20, 24, 30, 36, 40, 45, 48, 60])
    t = R.choice([2, 3, 4, 5])
    if n % t:
        return None
    return nq("A water plant gives off %d bubbles of oxygen in %d minutes. What is the rate of photosynthesis in bubbles per minute?" % (n, t), n / t, [t / n, n * t, n], " bubbles/min",
              "Rate = %d ÷ %d. Counting bubbles measures the oxygen released." % (n, t))


LIM = [("At low light intensity, the rate of photosynthesis rises as light increases. What is the limiting factor?", "light intensity"),
       ("At high light intensity, the rate levels off. At 0.04% carbon dioxide and 25 °C, what is likely to be the limiting factor?", "carbon dioxide concentration"),
       ("A plant in a greenhouse at 5 °C on a sunny winter day with extra carbon dioxide photosynthesises slowly. What is the limiting factor?", "temperature"),
       ("At dawn, the rate of photosynthesis is low but rising. What is the limiting factor?", "light intensity"),
       ("Adding more carbon dioxide raises the rate of photosynthesis. What was the limiting factor before?", "carbon dioxide concentration"),
       ("Warming the water from 10 °C to 25 °C raises the rate of photosynthesis of pondweed in bright light. What was the limiting factor?", "temperature")]


def g_lim():
    q, a = R.choice(LIM)
    return tq(q, a, [x for x in ("light intensity", "carbon dioxide concentration", "temperature", "oxygen concentration") if x != a],
              "The limiting factor is the one that, when increased, increases the rate.")


MIN = [("nitrate ions", "to make amino acids and proteins for growth"), ("magnesium ions", "to make chlorophyll")]


def g_min():
    m, use = R.choice(MIN)
    k = R.random() < 0.5
    if k:
        return tq("Why do plants need %s?" % m, use, [x for x in ("to make amino acids and proteins for growth", "to make chlorophyll", "to make starch", "to open the stomata") if x != use],
                  "Nitrate: amino acids and proteins. Magnesium: chlorophyll.")
    sym = "yellow leaves (lack of chlorophyll)" if m.startswith("mag") else "stunted growth"
    return tq("A plant lacking %s is most likely to show which symptom?" % m, sym, [x for x in ("yellow leaves (lack of chlorophyll)", "stunted growth", "extra flowers", "thicker cuticle") if x != sym],
              "Nitrate: proteins for growth. Magnesium: part of the chlorophyll molecule.")


XP = [("water and mineral ions", "xylem"), ("sucrose", "phloem"), ("amino acids", "phloem")]


def g_xp():
    x, t = R.choice(XP)
    return tq("Which tissue transports %s in a flowering plant?" % x, t, [y for y in ("xylem", "phloem", "the cortex", "the epidermis") if y != t],
              "Xylem: water and mineral ions, upwards. Phloem: sucrose and amino acids (translocation), up and down.")


DEF = [("transpiration", "the loss of water vapour from the leaves through the stomata"), ("translocation", "the transport of sucrose and amino acids in the phloem"),
       ("photosynthesis", "the making of glucose from carbon dioxide and water using light energy absorbed by chlorophyll"),
       ("a limiting factor", "something that is in short supply and so restricts the rate of a process"), ("wilting", "drooping of a plant when its cells lose turgor")]
g_def = rows(R, DEF, "What is meant by %s?", "Which term means %s?")

POOL1 = pool(R, [
    ("What is the word equation for photosynthesis?", "carbon dioxide + water → glucose + oxygen (light energy, chlorophyll)", ["glucose + oxygen → carbon dioxide + water", "carbon dioxide + oxygen → glucose + water", "water + oxygen → glucose + carbon dioxide"], "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂."),
    ("What is the role of chlorophyll?", "It absorbs light energy and converts it into chemical energy.", ["It stores glucose.", "It takes in carbon dioxide.", "It makes the leaf waterproof."], "Found in chloroplasts."),
    ("Why is a plant kept in the dark for 48 hours before a starch test?", "to destarch the leaves so any starch found was made during the experiment", ["to kill the plant", "to make more chlorophyll", "to open the stomata"], "Stored starch is used up."),
    ("A variegated leaf is tested for starch. Only the green parts turn blue-black. What does this show?", "Chlorophyll is needed for photosynthesis.", ["Light is not needed.", "Carbon dioxide is not needed.", "White parts make more starch."], "The white parts lack chlorophyll."),
    ("Why do plants need nitrate ions?", "to make amino acids and proteins", ["to make chlorophyll only", "to make starch", "to open stomata"], "A lack causes stunted growth."),
    ("Why do plants need magnesium ions?", "to make chlorophyll", ["to make proteins", "to make cellulose", "to transport water"], "A lack causes yellow leaves."),
    ("How does water enter root hair cells?", "by osmosis, as the cell sap has a lower water potential than the soil water", ["by active transport", "by diffusion of sucrose", "through the stomata"], "Mineral ions enter by active transport."),
    ("Why are most stomata on the lower surface of a leaf?", "It is cooler and shaded, so less water is lost.", ["It gets more light.", "Carbon dioxide is heavier.", "The upper surface has no cells."], "The upper surface has a thicker cuticle."),
    ("What happens to the glucose made in photosynthesis?", "It is used in respiration, stored as starch or converted to sucrose for transport.", ["It is all released as oxygen.", "It is stored as glycogen.", "It turns into chlorophyll."], "It can also make cellulose and proteins."),
    ("Why do plants wilt on a hot, dry afternoon?", "They lose water by transpiration faster than they take it up.", ["They make too much glucose.", "Their phloem breaks.", "They photosynthesise too slowly."], "Cells lose turgor."),
])
POOL5 = pool(R, [
    ("In bright light and 0.04% carbon dioxide, raising the light intensity further does not increase the rate. What is the limiting factor?", "carbon dioxide concentration", ["light intensity", "the amount of chlorophyll only", "oxygen concentration"], "Something else is now in short supply."),
    ("Why does increasing temperature above about 40 °C reduce the rate of photosynthesis?", "The enzymes involved are denatured.", ["Light is absorbed less.", "There is less carbon dioxide.", "Chlorophyll melts."], "Photosynthesis is controlled by enzymes."),
    ("A ring of bark (phloem) is removed from a tree trunk. What happens just above the ring?", "Sugars build up and the bark swells.", ["Water stops reaching the leaves.", "The leaves wilt at once.", "Nothing changes."], "Phloem transports sugar; xylem is deeper."),
    ("A potometer measures water uptake, not exactly transpiration. Why?", "Some water taken up is used in photosynthesis and to keep cells turgid.", ["All water taken up is used for growth.", "Water is lost through the roots.", "The bubble does not move."], "Most water taken up is transpired."),
    ("Why is a leafy shoot cut under water before it is put into a potometer?", "to stop air entering the xylem and blocking water flow", ["to clean the shoot", "to kill the cells", "to close the stomata"], "Air bubbles break the water column."),
    ("Which equation shows photosynthesis?", "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂", ["C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O", "6CO₂ + 6O₂ → C₆H₁₂O₆ + 6H₂O", "CO₂ + H₂O → CH₄ + O₂"], "Light energy and chlorophyll are needed."),
    ("A plant has yellowing leaves even though it is well watered and in sunlight. Which mineral ion is it likely to be short of?", "magnesium", ["sodium", "chloride", "calcium carbonate"], "Magnesium is part of the chlorophyll molecule."),
    ("Why do farmers in greenhouses add carbon dioxide?", "Carbon dioxide is often the limiting factor, so more increases the rate of photosynthesis and yield.", ["Carbon dioxide cools the plants.", "Plants breathe out carbon dioxide only at night.", "It kills pests."], "Light and temperature are also controlled."),
])


def main():
    sets = U.sets([
        ("Leaf structure", [(g_leaf, 10), (uk_leafad, 5), (uk_plant, 3), (POOL1, 2)]),
        ("Photosynthesis", [(POOL1, 5), (uk_starch, 4), (g_min, 3), (g_def, 3), (uk_rate, 5)]),
        ("Limiting factors", [(g_lim, 5), (g_isq, 6), (g_bub, 4), (uk_rate, 3), (POOL1, 2)]),
        ("Transport and transpiration", [(g_trp, 6), (g_xp, 3), (g_pot, 5), (g_def, 3), (uk_plant, 3)]),
        ("Exam-style questions", [(POOL5, 8), (g_pot2, 4), (g_isq, 4), (g_bub, 2), (g_leaf, 2)]),
    ])
    make_ol(LV, SUBJ, "nutrition-and-transport-in-flowering-plants", SORT, "Nutrition and Transport in Flowering Plants",
            "Describe the structure of a dicotyledonous leaf and how it is adapted for photosynthesis; state the word and chemical equations for photosynthesis; "
            "describe the role of chlorophyll; investigate the need for light, carbon dioxide and chlorophyll and the effects of limiting factors; state the "
            "importance of nitrate and magnesium ions; describe the uptake of water by root hair cells, the movement of water through the xylem and transpiration "
            "and the factors affecting it; describe wilting and the translocation of sucrose and amino acids in the phloem (summary of the Singapore-Cambridge "
            "O-Level Biology 6093 syllabus).",
            "Nutrition and Transport in Flowering Plants", "Plant nutrition and transport",
            "Free Secondary 3 O-Level Biology worksheets on nutrition and transport in flowering plants: leaf structure, photosynthesis, limiting factors, xylem, "
            "phloem, transpiration and potometers. 100 questions with answers.",
            "Leaves make glucose; xylem brings water; phloem carries sugar.", "Transpiration is fastest when warm, dry, windy and bright.",
            "<p><b>A leaf is a factory for glucose.</b></p><ul>"
            "<li>Carbon dioxide + water → glucose + oxygen, using light energy absorbed by chlorophyll.</li>"
            "<li>The rate is limited by the factor in shortest supply: light intensity, carbon dioxide concentration or temperature.</li>"
            "<li>Xylem carries water and mineral ions up from the roots; phloem carries sucrose and amino acids (translocation).</li>"
            "<li>Water evaporates from the mesophyll and diffuses out through the stomata: transpiration pulls water up the xylem.</li></ul>",
            [("Bubble moves 6 cm in 3 min. Rate?", ["6 ÷ 3"], "2 cm/min"),
             ("Lamp from 10 cm to 20 cm. Light?", ["intensity ∝ 1/d²", "(10/20)² = 1/4"], "1/4 as much")],
            ["Saying plants get their food from the soil.", "Mixing up xylem (water) and phloem (sugar).", "Saying transpiration is faster in humid air.",
             "Halving the light intensity when the distance doubles (it falls to a quarter)."],
            [("What are the limiting factors of photosynthesis?", "Light intensity, carbon dioxide concentration and temperature. The factor in the shortest supply limits the rate."),
             ("What is the difference between xylem and phloem?", "Xylem vessels are dead, lignified tubes that carry water and mineral ions up from the roots. Phloem is living tissue that carries sucrose and amino acids to all parts of the plant."),
             ("What affects the rate of transpiration?", "It is faster at higher temperature, lower humidity, higher wind speed and higher light intensity (when the stomata are open).")],
            sets)


if __name__ == "__main__":
    main()
