# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 5: Transport in Humans
  python tools/gen_sg_science_s3_transport_in_humans.py
Blood: plasma, red blood cells, white blood cells (phagocytes and lymphocytes) and platelets; blood clotting; the structure of the
heart and the cardiac cycle; double circulation; arteries, veins and capillaries; tissue fluid; coronary heart disease and its
risk factors; heart rate and cardiac output.
Everything is written here (the KS4 makers do not fit the 6093 wording).
Wrong answers come from real mistakes: "all arteries carry oxygenated blood", "the right ventricle has the thickest wall", "veins have
thick walls", "platelets carry oxygen", "the atria pump blood to the lungs".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool

LV, SUBJ, SORT = 3, "Biology", 24
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

BLOOD = [("red blood cells", "carry oxygen as oxyhaemoglobin"), ("phagocytes", "engulf and digest bacteria (phagocytosis)"),
         ("lymphocytes", "make antibodies against pathogens"), ("platelets", "help the blood to clot"),
         ("plasma", "transports dissolved glucose, amino acids, urea, hormones and carbon dioxide")]
g_blood = rows(R, BLOOD, "What is the function of %s?", "Which part of the blood has this role: “%s”?")

HEART = [("the right atrium", "receives deoxygenated blood from the body through the vena cava"),
         ("the left atrium", "receives oxygenated blood from the lungs through the pulmonary vein"),
         ("the right ventricle", "pumps deoxygenated blood to the lungs through the pulmonary artery"),
         ("the left ventricle", "pumps oxygenated blood to the body through the aorta"),
         ("the bicuspid and tricuspid valves", "stop blood flowing back from the ventricles into the atria"),
         ("the semilunar valves", "stop blood flowing back from the arteries into the ventricles"),
         ("the septum", "separates oxygenated and deoxygenated blood")]
g_heart = rows(R, HEART, "What is the role of %s?", "Which part of the heart has this role: “%s”?")

VES = [("the aorta", "oxygenated", "from the left ventricle to the body"), ("the vena cava", "deoxygenated", "from the body to the right atrium"),
       ("the pulmonary artery", "deoxygenated", "from the right ventricle to the lungs"), ("the pulmonary vein", "oxygenated", "from the lungs to the left atrium"),
       ("the hepatic portal vein", "deoxygenated", "from the small intestine to the liver"), ("the renal artery", "oxygenated", "from the aorta to the kidney"),
       ("the coronary artery", "oxygenated", "to the muscle of the heart wall")]


def g_ves():
    v, o, path = R.choice(VES)
    if R.random() < 0.5:
        return tq("Does %s carry oxygenated or deoxygenated blood?" % v, o, [x for x in ("oxygenated", "deoxygenated", "no blood", "only plasma") if x != o],
                  "%s carries %s blood %s." % (v[0].upper() + v[1:], o, path))
    others = [x for x in VES if x[0] != v]
    return tq("Which blood vessel carries blood %s?" % path, v, [x[0] for x in R.sample(others, 3)], "Arteries carry blood away from the heart; veins carry it back.")


VT = [("arteries", "thick, muscular, elastic walls and a narrow lumen", "carry blood at high pressure away from the heart"),
      ("veins", "thin walls, a wide lumen and valves", "return blood at low pressure to the heart"),
      ("capillaries", "walls one cell thick", "allow exchange of substances with tissue cells")]


def g_vt():
    v, st, fn = R.choice(VT)
    o = [x for x in VT if x[0] != v]
    k = R.choice(["st", "fn", "which"])
    if k == "st":
        return tq("Which structure is typical of %s?" % v, st, [x[1] for x in o] + ["a cellulose wall"], "Structure fits function: %s %s." % (v, fn))
    if k == "fn":
        return tq("Why do %s have %s?" % (v, st), "They " + fn + ".", ["They " + x[2] + "." for x in o] + ["They make blood cells."],
                  "Structure fits function.")
    return tq("Which blood vessels have %s?" % st, v, [x[0] for x in o] + ["lymph vessels only"], "Structure fits function.")


def g_hr():
    sv = R.choice([60, 65, 70, 75, 80, 90, 100])
    hr = R.choice([60, 65, 70, 72, 75, 80, 90, 120, 150])
    if R.random() < 0.6:
        co = sv * hr / 1000
        return nq("A person has a heart rate of %d beats per minute and a stroke volume of %d cm³. What is the cardiac output in dm³ per minute?" % (hr, sv), co,
                  [sv * hr, sv / hr, (sv + hr) / 1000], " dm³/min", "Cardiac output = heart rate × stroke volume = %d × %d = %d cm³/min." % (hr, sv, sv * hr))
    n = R.choice([12, 14, 15, 18, 20, 22, 25, 30, 36, 40])
    t = R.choice([10, 15, 20, 30])
    if not 55 <= n * 60 / t <= 180 or (n * 60) % t:
        return None
    return nq("A student counts %d pulse beats in %d seconds. What is the heart rate in beats per minute?" % (n, t), n * 60 / t, [n, n * t, n * 30 / t], " beats/min",
              "Heart rate = %d × (60 ÷ %d)." % (n, t))


CHD = [("smoking", "Nicotine and carbon monoxide damage artery walls and raise blood pressure."),
       ("a diet high in saturated fat and cholesterol", "Fatty deposits build up in the coronary arteries."),
       ("lack of exercise", "It is linked to high blood pressure and obesity."), ("stress", "It raises blood pressure."),
       ("high blood pressure", "It damages the artery walls.")]


def g_chd():
    f, why = R.choice(CHD)
    return tq("Why does %s increase the risk of coronary heart disease?" % f, why, R.sample([x[1] for x in CHD if x[1] != why] + ["It thickens the heart valves."], 3),
              "In coronary heart disease, the coronary arteries are narrowed by fatty deposits (atherosclerosis), so less oxygen reaches the heart muscle.")


ROUTE = ["the vena cava", "the right atrium", "the right ventricle", "the pulmonary artery", "the lungs", "the pulmonary vein",
         "the left atrium", "the left ventricle", "the aorta", "the body organs"]


def g_route():
    i = R.randrange(len(ROUTE))
    nxt = ROUTE[(i + 1) % len(ROUTE)]
    if R.random() < 0.5:
        w = [ROUTE[(i + k) % len(ROUTE)] for k in (2, 3, -1, 5)]
        w = [x for x in dict.fromkeys(w) if x != nxt][:3]
        return tq("Blood is in %s. Where does it go next?" % ROUTE[i], nxt, w, "Body → vena cava → right atrium → right ventricle → pulmonary artery → lungs → pulmonary vein → left atrium → left ventricle → aorta → body.")
    prv = ROUTE[i - 1]
    w = [x for x in dict.fromkeys([ROUTE[(i + k) % len(ROUTE)] for k in (1, 2, -3, 4)]) if x != prv][:3]
    return tq("Blood enters %s. Where has it just come from?" % ROUTE[i], prv, w, "Follow the double circulation backwards.")


EXC = [("oxygen", "from the blood to the cells"), ("glucose", "from the blood to the cells"), ("amino acids", "from the blood to the cells"),
       ("carbon dioxide", "from the cells to the blood"), ("urea", "from the cells to the blood"), ("water and dissolved substances (forming tissue fluid)", "out of the capillaries at the arterial end")]


def g_exc():
    x, d = R.choice(EXC)
    return tq("In the tissues, which way do the particles of %s move across the capillary walls?" % x, d,
              [y for y in ("from the blood to the cells", "from the cells to the blood", "it does not cross the capillary wall", "out of the capillaries at the arterial end") if y != d][:3],
              "Food and oxygen leave the blood for the cells; waste such as carbon dioxide and urea enters the blood. Tissue fluid forms from plasma at the arterial end.")


POOL1 = pool(R, [
    ("What is meant by double circulation?", "Blood passes through the heart twice in each complete circuit of the body.", ["Blood flows in two directions in each vessel.", "There are two hearts.", "Blood is pumped twice per second."], "Pulmonary circulation and systemic circulation."),
    ("Why is the wall of the left ventricle thicker than that of the right ventricle?", "It pumps blood at high pressure all round the body, not just to the nearby lungs.", ["It holds more blood.", "It receives blood from the lungs.", "It pumps deoxygenated blood."], "Both ventricles pump the same volume."),
    ("Why do red blood cells have no nucleus?", "There is more room for haemoglobin to carry oxygen.", ["They do not need to carry oxygen.", "They are dead cells.", "The nucleus would block capillaries."], "They are also biconcave."),
    ("What happens when a blood vessel is cut?", "Platelets help to change soluble fibrinogen into insoluble fibrin threads, which trap blood cells to form a clot.", ["Red blood cells make antibodies.", "Phagocytes form a scab by themselves.", "Plasma turns into fibrinogen."], "The clot stops blood loss and entry of pathogens."),
    ("What is tissue fluid?", "plasma that has passed out through capillary walls and bathes the cells", ["blood inside the arteries", "the fluid in the heart", "lymph in the lymph nodes"], "It does not contain red blood cells or large proteins."),
    ("Why do veins have valves?", "to stop blood flowing backwards, as the pressure is low", ["to raise blood pressure", "to make blood clot", "to pump blood"], "Muscles squeeze veins and push blood towards the heart."),
    ("What does haemoglobin combine with in the lungs?", "oxygen, forming oxyhaemoglobin", ["carbon dioxide, forming glucose", "nitrogen", "urea"], "Oxyhaemoglobin releases oxygen in the tissues."),
    ("Why is the pulmonary artery unusual?", "It is an artery that carries deoxygenated blood.", ["It carries blood to the heart.", "It has valves along its length.", "It carries oxygenated blood to the lungs."], "Arteries carry blood away from the heart."),
    ("Which chambers contract together to pump blood out of the heart into the arteries?", "the ventricles", ["the atria", "the right atrium and right ventricle", "the semilunar valves"], "Ventricular systole."),
    ("What causes the 'lub' sound of the heartbeat?", "the closing of the bicuspid and tricuspid valves", ["the closing of the semilunar valves", "the opening of the atria", "blood entering the vena cava"], "'Dub' is the semilunar valves closing."),
])
POOL5 = pool(R, [
    ("A coronary artery becomes blocked. Why can this cause a heart attack?", "The heart muscle beyond the blockage gets no oxygen and glucose, so it cannot respire and dies.", ["The heart fills with too much blood.", "The valves stop working.", "Blood flows backwards into the lungs."], "Coronary arteries supply the heart muscle."),
    ("During exercise, the heart rate rises. Why?", "More oxygen and glucose must reach the muscles for faster respiration, and more carbon dioxide must be removed.", ["The muscles need less blood.", "The blood becomes thicker.", "The heart needs to cool down."], "Cardiac output increases."),
    ("Blood leaves the heart from the left ventricle. Which route does it take to reach the lungs?", "aorta → body → vena cava → right atrium → right ventricle → pulmonary artery", ["aorta → pulmonary vein → lungs", "pulmonary vein → left atrium → lungs", "vena cava → left ventricle → lungs"], "Double circulation."),
    ("Why do people with fewer red blood cells (anaemia) feel tired?", "Less oxygen is carried to the cells for respiration.", ["They have too much glucose.", "Their blood cannot clot.", "They make too many antibodies."], "Iron is needed to make haemoglobin."),
    ("Why is a hole in the septum between the ventricles harmful?", "Oxygenated and deoxygenated blood mix, so less oxygen reaches the body.", ["The heart beats faster than normal.", "Blood cannot reach the lungs at all.", "The valves close too early."], "The septum keeps the two sides separate."),
    ("Capillaries are very narrow and have thin walls. Why is this useful?", "Substances diffuse quickly between the blood and the cells over a short distance.", ["Blood flows quickly at high pressure.", "They store blood.", "They pump blood to tissues."], "Red blood cells pass in single file."),
    ("Why does blood pressure fall as blood moves from arteries to veins?", "Friction and the huge total cross-section of the capillaries slow it and reduce pressure.", ["Veins pump blood back.", "Blood is lost at each organ.", "The valves increase pressure."], "Veins have valves and are squeezed by muscles."),
    ("Which change to lifestyle reduces the risk of coronary heart disease?", "stopping smoking and exercising regularly", ["eating more saturated fat", "drinking less water", "sleeping in the afternoon"], "A balanced diet low in saturated fat also helps."),
])


def main():
    sets = U.sets([
        ("Blood", [(g_blood, 7), (POOL1, 4), (g_hr, 4), (g_exc, 3), (g_chd, 2)]),
        ("The heart", [(g_heart, 9), (POOL1, 3), (g_route, 8)]),
        ("Blood vessels and circulation", [(g_vt, 6), (g_ves, 7), (POOL1, 2), (g_exc, 3), (g_route, 2)]),
        ("Heart rate and heart disease", [(g_hr, 10), (g_chd, 3), (g_heart, 2), (g_route, 3), (POOL5, 2)]),
        ("Exam-style questions", [(POOL5, 6), (g_hr, 4), (g_ves, 4), (g_vt, 2), (g_blood, 2), (g_route, 2)]),
    ])
    make_ol(LV, SUBJ, "transport-in-humans", SORT, "Transport in Humans",
            "Describe the components of blood and their functions, including the roles of phagocytes, lymphocytes and platelets and the process of blood clotting; "
            "describe the structure and function of the heart, the cardiac cycle and double circulation; relate the structure of arteries, veins and capillaries "
            "to their functions; describe the formation of tissue fluid; describe coronary heart disease and the factors that increase the risk (summary of the "
            "Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Transport in Humans", "Transport in humans",
            "Free Secondary 3 O-Level Biology worksheets on transport in humans: blood, clotting, the heart, double circulation, arteries, veins, capillaries, cardiac "
            "output and coronary heart disease. 100 questions with answers.",
            "Arteries away, veins back to the heart.", "The left ventricle has the thickest wall: it pumps to the whole body.",
            "<p><b>Blood goes through the heart twice in each circuit.</b></p><ul>"
            "<li>Right side: body → vena cava → right atrium → right ventricle → pulmonary artery → lungs. Left side: lungs → pulmonary vein → left atrium → left ventricle → aorta → body.</li>"
            "<li>Arteries: thick, elastic walls, high pressure. Veins: thin walls, valves, low pressure. Capillaries: one cell thick, for exchange.</li>"
            "<li>Red blood cells carry oxygen; phagocytes engulf bacteria; lymphocytes make antibodies; platelets help clotting.</li>"
            "<li>Cardiac output = heart rate × stroke volume.</li></ul>",
            [("Heart rate 70, stroke volume 80 cm³. Cardiac output?", ["70 × 80 = 5600 cm³/min"], "5.6 dm³/min"),
             ("Which vessel brings oxygenated blood to the heart?", ["from the lungs"], "pulmonary vein")],
            ["Saying all arteries carry oxygenated blood (not the pulmonary artery).", "Saying the right ventricle has the thickest wall.",
             "Saying veins have thick walls.", "Mixing up phagocytes (engulf) and lymphocytes (antibodies)."],
            [("What is double circulation?", "Blood passes through the heart twice for each complete circuit: once to the lungs (pulmonary circulation) and once to the rest of the body (systemic circulation)."),
             ("How are arteries different from veins?", "Arteries carry blood away from the heart at high pressure and have thick, muscular, elastic walls. Veins carry blood back at low pressure and have thinner walls, a wider lumen and valves."),
             ("What causes coronary heart disease?", "Fatty deposits build up in the coronary arteries, narrowing them so less oxygen reaches the heart muscle. Smoking, a high-fat diet, lack of exercise and stress increase the risk.")],
            sets)


if __name__ == "__main__":
    main()
