# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 6: Respiration in Humans
  python tools/gen_sg_science_s3_respiration_in_humans.py
Aerobic and anaerobic respiration (equations, energy released, lactic acid and oxygen debt); the human gas exchange system (trachea,
bronchi, bronchioles, alveoli) and how alveoli are adapted for gas exchange; the mechanism of breathing (intercostal muscles,
diaphragm, volume and pressure); differences between inspired and expired air; effects of tobacco smoke (nicotine, tar, carbon
monoxide) on health.
UK KS3/KS4 breathing and respiration makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "respiration is breathing", "anaerobic respiration in muscles makes ethanol", "the diaphragm
relaxes when you breathe in", "expired air has no oxygen", "tar causes addiction".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool

LV, SUBJ, SORT = 3, "Biology", 25
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_job = src("gen_uk_science_y8_breathing_and_gas_exchange", "g_job")
uk_path = src("gen_uk_science_y8_breathing_and_gas_exchange", "g_path")
uk_brate = src("gen_uk_science_y8_breathing_and_gas_exchange", "g_rate")
uk_sprint = src("gen_uk_science_y8_respiration", "g_sprint")
uk_type = src("gen_uk_science_y8_respiration", "g_type")
uk_eq = src("gen_uk_science_y11_photosynthesis_and_respiration", "g_eq")
us_ratio = src("gen_uk_science_y11_photosynthesis_and_respiration", "us_rratio")

MECH = [("the external intercostal muscles", "contract", "relax", ["stay contracted", "pull the ribs down"]),
        ("the internal intercostal muscles", "relax", "contract (in forced expiration)", ["contract and lift the ribs", "stay contracted"]),
        ("the diaphragm", "contracts and flattens", "relaxes and domes upwards", ["relaxes and flattens", "contracts and domes upwards"]),
        ("the ribcage", "moves upwards and outwards", "moves downwards and inwards", ["stays still", "moves downwards and outwards"]),
        ("the volume of the thorax", "increases", "decreases", ["stays the same", "doubles"]),
        ("the air pressure in the lungs", "falls below atmospheric pressure", "rises above atmospheric pressure", ["stays equal to atmospheric pressure", "becomes zero"])]


def g_mech():
    part, ins, ex_, extra = R.choice(MECH)
    inh = R.random() < 0.5
    a, o = (ins, ex_) if inh else (ex_, ins)
    return tq("During %s, what happens to %s?" % ("inspiration (breathing in)" if inh else "expiration (breathing out)", part), a, [o] + extra,
              "Breathing in: external intercostals and diaphragm contract, ribs up and out, thorax volume up, pressure down, air rushes in. Breathing out is the reverse.")


AIR = [("oxygen", "about 21%", "about 16%"), ("carbon dioxide", "about 0.04%", "about 4%"), ("water vapour", "variable", "saturated"), ("nitrogen", "about 78%", "about 78%")]


def g_air():
    g, i, e = R.choice(AIR)
    k = R.random() < 0.5
    if g == "nitrogen":
        return tq("How does the percentage of nitrogen in expired air compare with inspired air?", "about the same (78%)", ["much higher", "much lower", "zero in expired air"],
                  "Nitrogen is not used by the body.")
    if k:
        return tq("About what percentage of expired air is %s?" % g, e, [x for x in ("about 16%", "about 4%", "about 21%", "about 0.04%", "saturated", "variable") if x not in (e, i)][:2] + [i],
                  "Inspired: 21% O₂, 0.04% CO₂. Expired: 16% O₂, 4% CO₂, saturated with water vapour.")
    return tq("About what percentage of inspired air is %s?" % g, i, [x for x in ("about 16%", "about 4%", "about 21%", "about 0.04%", "saturated", "variable") if x not in (e, i)][:2] + [e],
              "Inspired: 21% O₂, 0.04% CO₂. Expired: 16% O₂, 4% CO₂, saturated with water vapour.")


ALV = [("a large total surface area (millions of alveoli)", "more oxygen and carbon dioxide can diffuse at once"),
       ("a wall one cell thick", "a short diffusion distance"), ("a thin film of moisture", "oxygen dissolves before it diffuses into the blood"),
       ("a rich network of capillaries", "a steep concentration gradient is kept"), ("constant ventilation by breathing", "fresh air keeps the oxygen concentration high in the alveoli")]
g_alv = rows(R, ALV, "How does %s help gas exchange in the alveoli?", "Which feature of the alveoli means that %s?")

SMK = [("nicotine", "is addictive and raises heart rate and blood pressure"), ("tar", "can cause lung cancer and paralyses cilia"),
       ("carbon monoxide", "combines with haemoglobin, so the blood carries less oxygen"), ("irritant particles", "cause coughing, bronchitis and emphysema")]
g_smk = rows(R, SMK, "Which harmful effect does the %s in cigarette smoke have?", "Which substance in cigarette smoke %s?")


def g_od():
    rest = R.choice([0.25, 0.3, 0.35])
    peak = R.choice([2.5, 3.0, 3.5, 4.0])
    need = R.choice([3.0, 3.5, 4.0, 4.5, 5.0])
    if need <= peak:
        return None
    t = R.choice([4, 5, 6, 8, 10])
    debt = round((need - peak) * t, 1)
    return nq("During %d minutes of hard exercise a runner needs %s dm³ of oxygen per minute, but can take in only %s dm³ per minute. How large is the oxygen debt?" % (t, need, peak), debt,
              [need * t, peak * t, need - peak], " dm³", "Oxygen debt = (%s − %s) × %d. It is repaid after exercise to break down lactic acid." % (need, peak, t))


POOL1 = pool(R, [
    ("What is respiration?", "the release of energy from food (glucose) in cells", ["breathing in and out", "the exchange of gases in the lungs", "making glucose using light"], "Breathing is ventilation, not respiration."),
    ("What is the word equation for aerobic respiration?", "glucose + oxygen → carbon dioxide + water (+ large amount of energy)", ["glucose → lactic acid (+ energy)", "carbon dioxide + water → glucose + oxygen", "glucose → ethanol + carbon dioxide"], "It happens in the mitochondria."),
    ("What is the word equation for anaerobic respiration in muscles?", "glucose → lactic acid (+ small amount of energy)", ["glucose → ethanol + carbon dioxide", "glucose + oxygen → carbon dioxide + water", "lactic acid → glucose"], "Muscles do not make ethanol."),
    ("What is the oxygen debt?", "the oxygen needed after exercise to remove the lactic acid made during anaerobic respiration", ["oxygen stored in the muscles", "oxygen breathed out", "the oxygen used in aerobic respiration during exercise"], "Lactic acid is broken down in the liver."),
    ("Why does aerobic respiration release more energy than anaerobic respiration?", "Glucose is completely broken down to carbon dioxide and water.", ["It is faster.", "It uses lactic acid.", "It happens without enzymes."], "Lactic acid still contains energy."),
    ("Why does the trachea have C-shaped rings of cartilage?", "to keep the airway open", ["to make mucus", "to exchange gases", "to pump air"], "The rings stop the trachea collapsing."),
    ("What do cilia and mucus in the airways do?", "Mucus traps dust and bacteria; cilia sweep it up to the throat.", ["They exchange gases.", "They warm the blood.", "They pump air into the alveoli."], "Tar paralyses cilia."),
    ("Where in the lungs does gas exchange take place?", "in the alveoli", ["in the trachea", "in the bronchi", "in the diaphragm"], "Oxygen diffuses into the blood; carbon dioxide diffuses out."),
    ("Why does breathing rate rise during exercise?", "More oxygen is needed and more carbon dioxide must be removed from faster respiration.", ["The lungs become smaller.", "The body needs less oxygen.", "Lactic acid is used for breathing."], "Carbon dioxide in the blood is detected by the brain."),
    ("Limewater turns cloudy faster with expired air than with inspired air. Why?", "Expired air contains more carbon dioxide.", ["Expired air contains more oxygen.", "Inspired air contains no gases.", "Expired air is colder."], "About 4% compared with 0.04%."),
])
POOL5 = pool(R, [
    ("Why do muscles ache after a sprint?", "Lactic acid builds up from anaerobic respiration.", ["Too much oxygen reaches them.", "They have run out of water.", "Carbon dioxide turns into lactic acid."], "It causes fatigue and cramp."),
    ("Why do smokers often feel short of breath?", "Carbon monoxide reduces the oxygen carried by the blood, and damaged alveoli give a smaller surface area.", ["Nicotine increases lung volume.", "Tar adds oxygen to the blood.", "Smoke cleans the airways."], "Emphysema breaks down alveolar walls."),
    ("A person with emphysema has fewer, larger air sacs. Why does this reduce gas exchange?", "The total surface area of the alveoli is smaller.", ["The walls are thinner.", "The air sacs hold more air.", "The blood flows faster."], "Less oxygen diffuses into the blood."),
    ("Why is carbon monoxide in cigarette smoke dangerous?", "It binds to haemoglobin more strongly than oxygen does.", ["It makes the blood clot instantly.", "It causes addiction.", "It forms tar in the lungs."], "Less oxygen reaches the tissues."),
    ("Why can a sprinter run 100 m mostly using anaerobic respiration but a marathon runner cannot?", "Anaerobic respiration releases little energy and builds up lactic acid, which causes fatigue.", ["Marathon runners do not need energy.", "Anaerobic respiration gives more energy.", "Lactic acid gives extra energy."], "Long races rely on aerobic respiration."),
    ("Which change happens during inspiration?", "The thorax volume increases and the pressure inside falls.", ["The diaphragm relaxes and domes upward.", "The ribs move down and in.", "The pressure in the lungs rises."], "Air moves from high to low pressure."),
    ("In a bell jar model, pulling the rubber sheet down inflates the balloons. What does the rubber sheet represent?", "the diaphragm", ["the ribs", "the trachea", "the alveoli"], "Contracting the diaphragm flattens it."),
    ("Why do yeast cells in bread dough produce carbon dioxide?", "They respire anaerobically, making ethanol and carbon dioxide, which makes the dough rise.", ["They photosynthesise.", "They respire to make lactic acid.", "They break down protein."], "This is fermentation, not human respiration."),
])


def main():
    sets = U.sets([
        ("Aerobic and anaerobic respiration", [(uk_type, 6), (uk_eq, 6), (POOL1, 5), (us_ratio, 3)]),
        ("The gas exchange system", [(uk_job, 7), (uk_path, 4), (g_alv, 6), (POOL1, 3)]),
        ("The mechanism of breathing", [(g_mech, 10), (g_air, 5), (POOL5, 1), (POOL1, 2), (g_od, 2)]),
        ("Exercise and oxygen debt", [(g_od, 6), (uk_sprint, 5), (uk_brate, 5), (us_ratio, 4)]),
        ("Smoking and exam-style questions", [(g_smk, 6), (POOL5, 6), (g_mech, 2), (g_alv, 3), (g_air, 1), (g_od, 2)]),
    ])
    make_ol(LV, SUBJ, "respiration-in-humans", SORT, "Respiration in Humans",
            "Define aerobic and anaerobic respiration and state their word equations; describe the effect of lactic acid in muscles and the oxygen debt; identify "
            "the parts of the human gas exchange system and describe how the alveoli are adapted for gas exchange; describe the role of the intercostal muscles "
            "and diaphragm in breathing and the differences between inspired and expired air; describe the effects of nicotine, tar and carbon monoxide in tobacco "
            "smoke (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Respiration in Humans", "Respiration in humans",
            "Free Secondary 3 O-Level Biology worksheets on respiration in humans: aerobic and anaerobic respiration, oxygen debt, the lungs, alveoli, breathing, "
            "inspired and expired air, and smoking. 100 questions with answers.",
            "Respiration releases energy; breathing moves air.", "No oxygen: glucose → lactic acid, a small amount of energy.",
            "<p><b>Respiration happens in every cell; breathing happens in the lungs.</b></p><ul>"
            "<li>Aerobic: glucose + oxygen → carbon dioxide + water + a lot of energy. Anaerobic (muscles): glucose → lactic acid + a little energy.</li>"
            "<li>Air: nose → trachea → bronchi → bronchioles → alveoli. Alveoli: large surface area, thin wall, moist, many capillaries.</li>"
            "<li>Breathing in: external intercostals and diaphragm contract; thorax volume up, pressure down, air in.</li>"
            "<li>Smoke: nicotine (addictive), tar (cancer, cilia), carbon monoxide (less oxygen carried).</li></ul>",
            [("Need 4 dm³/min, get 3 dm³/min, 5 min. Oxygen debt?", ["(4 − 3) × 5"], "5 dm³"),
             ("Diaphragm when breathing in?", ["contracts", "flattens"], "contracts and flattens")],
            ["Calling breathing “respiration”.", "Saying muscles make ethanol.", "Saying the diaphragm relaxes when you breathe in.",
             "Saying expired air contains no oxygen (it has about 16%)."],
            [("What is the difference between aerobic and anaerobic respiration?", "Aerobic respiration uses oxygen and breaks glucose down completely to carbon dioxide and water, releasing a lot of energy. Anaerobic respiration in muscles uses no oxygen, makes lactic acid and releases much less energy."),
             ("How are alveoli adapted for gas exchange?", "There are millions of them, giving a huge surface area; their walls are one cell thick; they are moist; and they are covered with capillaries that keep a steep concentration gradient."),
             ("What happens when you breathe in?", "The external intercostal muscles contract, raising the ribs, and the diaphragm contracts and flattens. The volume of the thorax increases, the pressure falls and air rushes into the lungs.")],
            sets)


if __name__ == "__main__":
    main()
