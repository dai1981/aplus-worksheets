# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Respiratory and circulatory systems (Systems)
  python tools/gen_sg_science_p5_respiratory_and_circulatory_systems.py
Respiratory system: air enters through the nose, passes down the windpipe into the lungs; in the air sacs oxygen passes into
the blood and carbon dioxide passes out. Exhaled air has less oxygen and more carbon dioxide and water vapour than inhaled air.
Fish take in oxygen dissolved in water through gills; plants exchange gases through tiny openings in their leaves.
Circulatory system: the heart pumps blood through blood vessels to all parts of the body; blood carries oxygen, digested food
and water to the cells and carries carbon dioxide away. The systems work together; the heart rate and breathing rate rise
during exercise. UK pulse-rate questions are reused (no arteries, veins or capillaries here).
Wrong answers come from real mistakes: "we breathe out only carbon dioxide", "fish breathe in water through lungs",
"the heart cleans the blood", "plants take in only carbon dioxide".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63507)
R = U.R
P = People(R)
CI = use(U, "gen_uk_science_y6_the_circulatory_system", drop=["double loop", "Harvey", "red blood", "artery", "arteries", "vein", "capillar", "platelet", "plasma", "white blood", "left side", "right side", "liver"])
BR = use(U, "gen_uk_science_y8_breathing_and_gas_exchange", drop=["bronch", "alveol", "diffus", "intercostal", "diaphragm", "cartilage", "cilia", "trachea", "pressure",
                                                                   "asthma", "tar", "nitrogen", "percentage points", "argon"])

AIR = ["nose", "windpipe", "lungs", "air sacs"]


def g_path():
    i = R.randrange(3)
    k = R.choice(["next", "before"])
    if not once(("ap", i, k)):
        return None
    if k == "next":
        a, s0 = AIR[i + 1], AIR[i]
        q = "Air we breathe in passes through the %s. Where does it go next?" % s0
    else:
        a, s0 = AIR[i], AIR[i + 1]
        q = "Air reaches the %s. Where did it come from just before?" % s0
    w = [x for x in AIR + ["stomach", "gullet"] if x not in (a, s0)]
    return item(q, "the " + a, ["the " + x for x in R.sample(w, 3)], "nose → windpipe → lungs → air sacs.")


FUNC = [("the heart", "pumps blood around the body"), ("the blood vessels", "carry blood to and from all parts of the body"),
        ("the blood", "carries oxygen, digested food and water to the cells"), ("the lungs", "take in oxygen and remove carbon dioxide"),
        ("the windpipe", "carries air from the nose to the lungs"), ("the air sacs", "are where oxygen passes into the blood"),
        ("the gills", "take in oxygen dissolved in water for fish"), ("the tiny openings on leaves", "let gases enter and leave a plant")]


def g_func():
    p, f = R.choice(FUNC)
    k = R.choice(["what", "which"])
    if not once(("fn", p, k)):
        return None
    others = [x for x in FUNC if x[0] != p]
    if k == "which":
        return item("Which part %s?" % f.replace("carry ", "carries ").replace("take in", "takes in").replace("are where", "is where").replace("let gases", "lets gases"),
                    p, [x[0] for x in R.sample(others, 3)], "%s %s." % (p[0].upper() + p[1:], f))
    return item("What is the function of %s?" % p, f[0].upper() + f[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample(others, 3)], "%s %s." % (p[0].upper() + p[1:], f))


CARRY = [("oxygen", "from the lungs to all parts of the body"), ("carbon dioxide", "from all parts of the body to the lungs"),
         ("digested food", "from the small intestine to all parts of the body"), ("water", "from the intestines to all parts of the body")]


def g_carry():
    s, path = R.choice(CARRY)
    k = R.choice(["where", "what"])
    if not once(("ca", s, k)):
        return None
    if k == "where":
        return item("The blood carries %s. In which direction?" % s, path, [p for x, p in CARRY if x != s][:3], "The blood transports substances around the body.")
    return item("Which substance does the blood carry %s?" % path, s, [x for x, _ in CARRY if x != s], "The blood carries oxygen, digested food and water to the cells, and carbon dioxide to the lungs.")


def g_compare():
    gas = R.choice(["oxygen", "carbon dioxide", "water vapour"])
    if not once(("cp", gas)):
        return None
    more = gas != "oxygen"
    return item("Compared with the air we breathe in, the air we breathe out has ___ %s." % gas, "more" if more else "less",
                ["less" if more else "more", "the same amount of", "no"], "Exhaled air has less oxygen and more carbon dioxide and water vapour.")


def g_rate():
    act = [("resting", (14, 18), (70, 80)), ("walking", (20, 24), (90, 100)), ("jogging", (28, 34), (120, 135)), ("running", (38, 46), (150, 170))]
    br = [R.randint(*a[1]) for a in act]
    hr = [R.randint(*a[2]) for a in act]
    k = R.choice(["hi", "why", "both", "read", "diff"])
    if not once(("rt", k), 3 if k in ("read", "diff") else 1):
        return None
    tb = table(["Activity", "Breaths per minute", "Heartbeats per minute"], [[a[0], str(b), str(h)] for a, b, h in zip(act, br, hr)])
    q0 = "%s measured a classmate's breathing rate and heart rate.<br>%s" % (P.next()[0], tb)
    if k == "hi":
        return item(q0 + "During which activity were both rates the highest?", "running", ["resting", "walking", "jogging"], "The more active the body, the higher both rates.")
    if k == "why":
        return item(q0 + "Why do both rates go up during exercise?", "The muscles need more oxygen and digested food, and must remove more carbon dioxide.",
                    ["The lungs need less air.", "The heart needs to rest.", "The blood becomes thinner."], "The respiratory and circulatory systems work together.")
    if k == "both":
        return item(q0 + "What does the table show?", "As the activity becomes more vigorous, both the breathing rate and the heart rate increase.",
                    ["The breathing rate falls when the heart rate rises.", "Exercise does not affect the heart rate.", "The breathing rate is always higher than the heart rate."],
                    "Both rates rise with exercise.")
    if k == "read":
        i = R.randrange(4)
        return item(q0 + "What was the heart rate while %s?" % act[i][0], "%d beats per minute" % hr[i], ["%d beats per minute" % hr[j] for j in range(4) if j != i], "Read the row for %s." % act[i][0])
    d = hr[3] - hr[0]
    return item(q0 + "By how much did the heart rate rise from resting to running?", "%d beats per minute" % d, ["%d beats per minute" % x for x in (hr[3], hr[0], d + 10)],
                "%d − %d = %d." % (hr[3], hr[0], d))


def g_recover():
    rest = R.randint(68, 80)
    vals = [rest + R.randint(55, 70)]
    while len(vals) < 6:
        vals.append(max(rest, vals[-1] - R.randint(10, 22)))
    if vals[-1] != rest or vals[-2] == rest and vals[-3] == rest:
        return None
    k = R.choice(["back", "drop1", "trend", "why"])
    if not once(("rc", k), 2 if k in ("back", "drop1") else 1):
        return None
    tb = table(["Minutes after stopping", "0", "1", "2", "3", "4", "5"], [["Pulse rate (beats per minute)"] + [str(v) for v in vals]])
    q0 = "%s skipped for 3 minutes, then measured %s pulse rate every minute. %s resting pulse rate is %d beats per minute.<br>%s" % ((lambda p: (p[0], p[2], p[2].capitalize()))(P.next()) + (rest, tb))
    if k == "back":
        m = vals.index(rest)
        return item(q0 + "After how many minutes did the pulse rate return to the resting rate?", "%d minutes" % m if m != 1 else "1 minute",
                    ["%d minutes" % x for x in range(0, 6) if x != m and x != 1][:3], "Find the first reading equal to %d." % rest)
    if k == "drop1":
        d = vals[0] - vals[1]
        return item(q0 + "By how much did the pulse rate fall in the first minute?", "%d beats per minute" % d, ["%d beats per minute" % x for x in (vals[0], vals[1], d + 10)],
                    "%d − %d = %d." % (vals[0], vals[1], d))
    if k == "trend":
        return item(q0 + "What does the table show?", "The pulse rate fell after exercise until it returned to the resting rate.",
                    ["The pulse rate kept rising after exercise.", "The pulse rate stayed the same.", "The pulse rate fell below the resting rate."], "The heart slows down as the muscles need less oxygen.")
    return item(q0 + "Why did the pulse rate fall after skipping stopped?", "The muscles needed less oxygen and digested food, so the heart pumped more slowly.",
                ["The heart stopped working.", "The lungs took in more air.", "The blood was used up."], "The body returns to its resting state.")


B1 = bank([
    ("What is the function of the respiratory system?", "to take in oxygen and remove carbon dioxide", ["to pump blood", "to digest food", "to remove undigested food"], "Breathing brings air into the lungs."),
    ("What is the function of the circulatory system?", "to transport substances such as oxygen and digested food around the body", ["to take in air", "to break down food", "to support the body"], "The heart pumps blood through blood vessels."),
    ("Which gas does the body need from the air?", "oxygen", ["carbon dioxide", "nitrogen only", "water vapour"], "Cells use oxygen to release energy from food."),
    ("Which gas does the body get rid of when we breathe out?", "carbon dioxide", ["oxygen only", "hydrogen", "nitrogen only"], "Carbon dioxide is a waste gas."),
    ("Where does oxygen pass into the blood?", "in the air sacs of the lungs", ["in the windpipe", "in the nose", "in the heart"], "The air sacs have very thin walls."),
    ("What are the three main parts of the circulatory system?", "the heart, blood vessels and blood", ["the lungs, windpipe and nose", "the stomach and intestines", "bones and muscles"], "Blood flows through blood vessels."),
    ("Why does exhaled air make a cold mirror misty?", "It contains water vapour that condenses on the mirror.", ["It contains smoke.", "It contains more oxygen.", "It is colder than the mirror."], "We breathe out water vapour."),
    ("What is the pulse?", "the beat felt at the wrist or neck when the heart pumps blood", ["the sound of breathing", "the movement of food", "the movement of the lungs"], "Each pulse beat matches one heartbeat."),
])
B2 = bank([
    ("How do fish take in oxygen?", "Their gills take in oxygen dissolved in the water.", ["They breathe air through lungs.", "They take in oxygen through their scales.", "They do not need oxygen."], "Water flows over the gills."),
    ("Why does a fish die when it is taken out of water for a long time?", "Its gills cannot take in oxygen from the air.", ["It gets too much oxygen.", "It is too cold.", "Its scales dry up and turn into lungs."], "Gills work in water."),
    ("How do plants take in and give out gases?", "through tiny openings, mostly on the underside of the leaves", ["through their flowers only", "through their roots only", "they do not exchange gases"], "Gases move in and out through these openings."),
    ("Which gases do plants take in?", "oxygen (for respiration) and carbon dioxide (in light, to make food)", ["only carbon dioxide", "only oxygen", "no gases"], "Plants respire all the time."),
    ("How do the respiratory and circulatory systems work together?", "The lungs take in oxygen and the blood carries it to all parts of the body.", ["The heart takes in air.", "The lungs pump blood.", "They do not work together."], "The systems depend on each other."),
    ("Why does the heart beat faster during exercise?", "to pump more blood carrying oxygen and digested food to the muscles", ["to cool the body", "to take in more air", "to make the blood thicker"], "Active muscles need more oxygen."),
    ("Why do we breathe faster during exercise?", "to take in more oxygen and remove more carbon dioxide", ["to cool the lungs", "to take in less air", "to make the heart slower"], "The muscles are working harder."),
    ("Which organ is NOT part of the respiratory system?", "the heart", ["the lungs", "the windpipe", "the nose"], "The heart is part of the circulatory system."),
])
B3 = bank([
    ("Why is smoking harmful to the lungs?", "Smoke damages the air sacs, so less oxygen can pass into the blood.", ["Smoke adds oxygen.", "Smoke cleans the lungs.", "Smoke makes the lungs bigger."], "Smokers often get out of breath easily."),
    ("How does regular exercise help the heart?", "It makes the heart stronger.", ["It makes the heart smaller.", "It stops the heart.", "It removes blood."], "A strong heart pumps more blood with each beat."),
    ("Why should we breathe through the nose rather than the mouth?", "Hairs and mucus in the nose trap dust and germs.", ["The nose makes oxygen.", "The mouth has no air.", "The nose pumps blood."], "The air is also warmed and moistened."),
    ("Why is a person's pulse rate higher after running?", "The heart beats faster to pump more blood to the muscles.", ["The blood vessels are shorter.", "The lungs stop working.", "The body needs less oxygen."], "The pulse rate equals the heart rate."),
    ("Limewater turns chalky with carbon dioxide. Which turns limewater chalky faster: inhaled air or exhaled air?", "exhaled air", ["inhaled air", "both the same", "neither"], "Exhaled air has more carbon dioxide."),
])
B4 = bank([
    ("Which of these is carried by the blood?", "digested food", ["undigested food", "air bubbles from the stomach", "saliva"], "Digested food is absorbed into the blood in the small intestine."),
    ("Why does the body need oxygen?", "to release energy from digested food", ["to digest food", "to make blood red only", "to make carbon dioxide useful"], "Cells use oxygen and food to release energy."),
    ("Where is carbon dioxide produced in the body?", "in all the cells of the body", ["only in the lungs", "only in the heart", "only in the nose"], "Cells release energy from food and make carbon dioxide."),
    ("Which statement about the heart is correct?", "It is a muscular organ that pumps blood all the time.", ["It stops when we sleep.", "It is part of the respiratory system.", "It takes in oxygen from the air."], "The heart never rests."),
    ("Where is the heart found?", "in the chest, between the lungs", ["in the stomach", "in the head", "in the neck"], "The ribs protect the heart and lungs."),
    ("What protects the lungs and heart?", "the ribcage", ["the skull", "the backbone only", "the stomach"], "The ribs form a cage around them."),
    ("Which body systems work together to bring digested food to the muscles?", "the digestive and circulatory systems", ["the respiratory and skeletal systems", "the muscular system only", "the respiratory system only"], "Food is digested and absorbed, then carried by the blood."),
    ("When we breathe in, what happens to our chest?", "It moves up and out as the lungs fill with air.", ["It moves down and in.", "It stays still.", "It fills with blood."], "The lungs expand."),
    ("Why do tadpoles use gills but adult frogs use lungs?", "Tadpoles live in water; adult frogs breathe air on land.", ["Gills are bigger than lungs.", "Tadpoles do not need oxygen.", "Adult frogs live only in water."], "Each matches where the animal lives."),
    ("How do the tiny openings on leaves help a plant at night?", "They let in oxygen for respiration and let out carbon dioxide.", ["They let in light.", "They let in carbon dioxide to make food.", "They are closed so no gases move."], "Plants respire all the time."),
])
B5 = bank([
    ("Siti bubbled her exhaled air through limewater and pumped room air through another tube of limewater. What did she find?", "Only the limewater with exhaled air turned chalky quickly.", ["Both stayed clear.", "Only the room air turned it chalky.", "Both turned chalky at the same time."], "Exhaled air has more carbon dioxide."),
    ("Ravi counted his pulse for 15 seconds and got 20 beats. What is his pulse rate per minute?", "80 beats per minute", ["20 beats per minute", "35 beats per minute", "300 beats per minute"], "20 × 4 = 80."),
    ("Mei Ling measured her pulse at rest, then right after skipping for 2 minutes. Why did she measure it at rest first?", "to compare the result after exercise with the normal rate", ["to make her heart stronger", "to make skipping easier", "to cool down"], "The resting rate is the control."),
    ("Why should the pulse be measured three times and the average found?", "to make the result more reliable", ["to make the heart beat faster", "to use up time", "one reading is always exact"], "Repeating reduces errors."),
    ("A fish tank was left without an air pump on a hot day. The fish swam near the surface. Why?", "There was more oxygen near the surface, where air meets the water.", ["They wanted to see the light.", "The water at the bottom was too cold.", "They were looking for food only."], "Warm water holds less oxygen."),
])


def body():
    think = ("<p><b>The respiratory system takes in oxygen; the circulatory system carries it to every part of the body.</b></p>"
             "<ul><li>Air: nose → windpipe → lungs → air sacs. In the air sacs, oxygen passes into the blood and carbon dioxide passes out.</li>"
             "<li>Exhaled air has <b>less oxygen</b> and <b>more carbon dioxide and water vapour</b> than inhaled air.</li>"
             "<li>The <b>heart</b> pumps <b>blood</b> through <b>blood vessels</b>. Blood carries oxygen, digested food and water to the cells and carbon dioxide away.</li>"
             "<li>Fish use gills; plants exchange gases through tiny openings on the leaves.</li></ul>")
    ex = [("Why does the heart beat faster during a race?", ["Muscles need more oxygen and digested food", "The heart pumps more blood"], "To supply the muscles."),
          ("Which gas is there more of in exhaled air?", ["Cells release carbon dioxide", "It is breathed out"], "Carbon dioxide (and water vapour).")]
    mist = ["Thinking we breathe out only carbon dioxide. Exhaled air still has a lot of oxygen.",
            "Thinking fish breathe air with lungs. They use gills to take in oxygen dissolved in water.",
            "Thinking the heart cleans the blood. It pumps the blood.",
            "Thinking plants take in only carbon dioxide. They take in oxygen for respiration too."]
    return lesson(think, ex, mist)


PULSE = upto(CI.g_pulse, 6)
AVG = upto(CI.g_avg, 3)
CIE = upto(CI.g_ex, 4)
BRR = upto(BR.g_rate, 2)
BRA = upto(BR.g_air, 3)


def main():
    sets = U.sets([
        ("Breathing", B1 + [(g_path, 5), (g_func, 4), (g_compare, 3)]),
        ("Gases in living things", B2 + [(g_func, 5), (g_compare, 2), (g_carry, 5)]),
        ("The heart and blood", CI.B1 + B4[:6] + [(g_carry, 3), (g_func, 3), (PULSE, 3), (g_path, 3)]),
        ("Keeping healthy", B3 + CI.B5 + B4[6:] + [(g_rate, 3), (PULSE, 2), (BRR, 2)]),
        ("PSLE-style experiments", B5 + [(g_rate, 4), (g_recover, 4), (CIE, 3), (BRA, 2), (AVG, 2), (g_compare, 1)]),
    ])
    make_sg(5, "respiratory-and-circulatory-systems", 7, "Systems", "Human system (Respiratory and circulatory systems)",
            "Identify the organs of the human respiratory system and the circulatory system and their functions, and describe how the two systems work together "
            "to take in oxygen and transport it, digested food and water to all parts of the body and remove carbon dioxide. Compare how fish (gills) and plants "
            "(tiny openings in leaves) take in and give out gases (summary of the MOE Primary Science Syllabus).",
            "Respiratory and Circulatory Systems",
            "Primary 5 Science: Respiratory and Circulatory Systems Worksheets (with Answers)",
            "Respiratory and circulatory systems",
            "Free Primary 5 science worksheets for Singapore pupils on the respiratory and circulatory systems: lungs, air sacs, heart, blood, pulse rate, fish gills and plant gas exchange. 100 questions with answers.",
            "The lungs take in oxygen; the blood carries it.",
            "The heart pumps blood to every part of the body.",
            body(),
            [("How do the respiratory and circulatory systems work together?", "The lungs take in oxygen, which passes into the blood in the air sacs. The heart pumps the blood to carry the oxygen to all parts of the body. Carbon dioxide is carried back to the lungs and breathed out."),
             ("What is the difference between inhaled and exhaled air?", "Exhaled air has less oxygen and more carbon dioxide and water vapour than inhaled air."),
             ("How do fish breathe?", "Fish take in oxygen dissolved in water through their gills.")],
            sets)


if __name__ == "__main__":
    main()
