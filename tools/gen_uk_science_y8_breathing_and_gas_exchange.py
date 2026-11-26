# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Biology): Breathing and Gas Exchange
  python tools/gen_uk_science_y8_breathing_and_gas_exchange.py
The structure and functions of the gas exchange system, the mechanism of breathing (diaphragm, intercostal muscles,
volume and pressure), the bell-jar model, inhaled and exhaled air, the effect of exercise, asthma and smoking on the
system, and measuring lung volume. Reuses the body-system questions of the US Grade 6 unit in British English.
Wrong answers come from real mistakes: "air is sucked in by the lungs themselves", "we breathe out only carbon dioxide",
"the diaphragm moves up when we breathe in", "gas exchange happens in the trachea".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61802)
R = U.R
P = People(R)
uk_sci.USED.clear()
BS = adopt_us("gen_us_science_g6_body_systems", U)

PATH = ["the nose or mouth", "the trachea (windpipe)", "a bronchus", "a bronchiole", "an alveolus (air sac)"]
JOB = [("the trachea (windpipe)", "carries air from the throat to the bronchi and is held open by rings of cartilage"),
       ("the bronchi", "two tubes that carry air from the trachea into each lung"),
       ("the bronchioles", "small branching tubes that carry air to the alveoli"),
       ("the alveoli", "tiny air sacs where oxygen passes into the blood and carbon dioxide passes out"),
       ("the diaphragm", "a sheet of muscle under the lungs that contracts and flattens when we breathe in"),
       ("the intercostal muscles", "muscles between the ribs that move the ribcage up and out"),
       ("the ribs", "bones that protect the lungs and heart"),
       ("cilia", "tiny hairs on cells lining the airways that sweep mucus and dirt up and away from the lungs")]


def g_path():
    i = R.randrange(len(PATH) - 1)
    k = R.random() < 0.5
    if not once(("pa", i, k)):
        return None
    if k:
        a = PATH[i + 1]
        return item("On its way into the lungs, air passes through %s. Where does it go next?" % PATH[i], a, [x for x in PATH if x not in (a, PATH[i])][:3],
                    "Nose or mouth → trachea → bronchi → bronchioles → alveoli.")
    a = PATH[i]
    return item("Where does air come from just before it reaches %s?" % PATH[i + 1], a, [x for x in PATH if x not in (a, PATH[i + 1])][:3],
                "Nose or mouth → trachea → bronchi → bronchioles → alveoli.")


def g_job():
    p, j = R.choice(JOB)
    k = R.random() < 0.5
    if not once(("jo", p, k)):
        return None
    if k:
        return item("Which part of the gas exchange system is described here? “%s.”" % (j[0].upper() + j[1:]), p,
                    R.sample([x[0] for x in JOB if x[0] != p], 3), "Each part has a job.")
    return item("What is the job of %s?" % p, j[0].upper() + j[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample([x for x in JOB if x[0] != p], 3)], "Each part has a job.")


MECH = [("the diaphragm", "contracts and flattens (moves down)", "relaxes and domes upwards"),
        ("the intercostal muscles", "contract", "relax"),
        ("the ribcage", "moves up and out", "moves down and in"),
        ("the volume of the chest", "increases", "decreases"),
        ("the pressure inside the chest", "decreases", "increases")]


def g_mech():
    part, inh, exh = R.choice(MECH)
    k = R.random() < 0.5
    if not once(("me", part, k)):
        return None
    a = inh if k else exh
    b = exh if k else inh
    return item("When you breathe %s, what happens to %s?" % ("in" if k else "out", part), a, [b, "stays exactly the same", "fills with blood"],
                "Breathing in: diaphragm and intercostals contract, ribs up and out, volume up, pressure down, air rushes in.")


AIR = [("nitrogen", 78, 78), ("oxygen", 21, 16), ("carbon dioxide", 0.04, 4)]


def g_air():
    tab = table(["Gas", "Inhaled air (%)", "Exhaled air (%)"], [[g, str(a), str(b)] for g, a, b in AIR])
    k = R.choice(["more", "less", "same", "why", "diff_o", "diff_c"])
    if not once(("ai", k)):
        return None
    if k == "more":
        return item(tab + "Which gas is there more of in exhaled air than in inhaled air?", "carbon dioxide", ["oxygen", "nitrogen", "none of them"], "Cells make carbon dioxide in respiration.")
    if k == "less":
        return item(tab + "Which gas is there less of in exhaled air?", "oxygen", ["carbon dioxide", "nitrogen", "water vapour"], "Oxygen passes into the blood in the alveoli.")
    if k == "same":
        return item(tab + "Why is the amount of nitrogen the same in both?", "The body does not use nitrogen gas.", ["Nitrogen is used up and made again.", "Nitrogen is made by the lungs.", "Nitrogen is all absorbed."], "It goes in and out unchanged.")
    if k == "why":
        return item(tab + "Why does exhaled air contain more carbon dioxide?", "It is made by respiration in cells and passes from the blood into the alveoli.", ["The lungs make it from oxygen.", "It comes from the food in the stomach.", "The air in the room is dirty."], "Waste product of respiration.")
    if k == "diff_o":
        return item(tab + "By how many percentage points does oxygen fall between inhaled and exhaled air?", "5", ["16", "21", "37"], "21 − 16 = 5.")
    return item(tab + "About how many times more carbon dioxide is in exhaled air than in inhaled air?", "100 times", ["4 times", "10 times", "2 times"], "4 ÷ 0.04 = 100.")


ADAPT = [("Alveoli have a huge total surface area.", "Lots of gas can be exchanged at once."),
         ("Alveoli walls are only one cell thick.", "Gases only have a short distance to diffuse."),
         ("Alveoli are surrounded by many capillaries.", "Blood carries oxygen away quickly and brings carbon dioxide."),
         ("Alveoli walls are moist.", "Gases dissolve before they diffuse through."),
         ("The trachea has rings of cartilage.", "It stays open so air can always get through."),
         ("Airways are lined with mucus.", "Dirt and germs are trapped before they reach the alveoli.")]


def g_adapt():
    s, a = R.choice(ADAPT)
    if not once(("ad", s)):
        return None
    return item("%s Why is this useful?" % s, a, R.sample([x[1] for x in ADAPT if x[1] != a], 3), "Structure fits function.")


def g_rate():
    who = P.next()[0]
    rest = R.choice([12, 14, 15, 16, 18])
    vals = [rest, rest + R.choice([6, 8, 10]), rest + R.choice([16, 18, 20, 24]), rest + R.choice([4, 6])]
    acts = ["resting", "walking", "running", "2 minutes after running"]
    k = R.choice(["max", "why", "diff", "vol"])
    if not once(("ra", rest, k), 2):
        return None
    tab = table(["Activity", "Breaths per minute"], [[a, str(v)] for a, v in zip(acts, vals)])
    intro = tab + "%s counted breaths per minute. " % who
    if k == "max":
        return item(intro + "During which activity was the breathing rate highest?", "running", ["resting", "walking", "2 minutes after running"], "Exercise raises the breathing rate.")
    if k == "why":
        return item(intro + "Why does the breathing rate go up during exercise?", "Muscles need more oxygen for respiration and make more carbon dioxide.", ["The lungs get bigger.", "The heart stops working.", "The body needs less oxygen."], "More respiration in the muscles.")
    if k == "diff":
        d = vals[2] - vals[0]
        return item(intro + "By how many breaths per minute did the rate rise from resting to running?", str(d), uniq(str(d), [str(vals[2]), str(vals[0]), str(vals[2] + vals[0]), str(d + 2)]), "%d − %d = %d." % (vals[2], vals[0], d))
    v = R.choice([0.5, 0.6])
    t = round(rest * v, 1)
    g = "%s litres" % t
    return item(intro + "At rest each breath moves %s litres of air. How much air is breathed in per minute at rest?" % v, g,
                uniq(g, ["%s litres" % round(rest + v, 1), "%s litres" % rest, "%s litres" % round(t * 10, 1), "%s litres" % v]), "%d × %s = %s litres." % (rest, v, t))


B1 = bank([
    ("What is the main job of the gas exchange system?", "to take oxygen into the blood and remove carbon dioxide", ["to digest food", "to pump blood", "to make carbon dioxide from food"], "Breathing makes gas exchange possible."),
    ("Where does gas exchange take place?", "in the alveoli", ["in the trachea", "in the stomach", "in the bronchi"], "Tiny air sacs."),
    ("By which process do oxygen and carbon dioxide move between the alveoli and the blood?", "diffusion", ["digestion", "evaporation", "filtration"], "From high to low concentration."),
    ("Is breathing the same as respiration?", "No. Breathing moves air in and out; respiration releases energy in cells.", ["Yes, they are the same.", "Respiration happens only in the lungs.", "Breathing happens only in cells."], "A common mix-up."),
    ("Why does air move into the lungs when you breathe in?", "The chest volume increases, so the pressure falls below the air outside.", ["The lungs suck it in like a pump.", "The stomach pushes it in.", "The heart pulls it in."], "Air moves from high to low pressure."),
    ("In the bell-jar model of the lungs, what does the rubber sheet represent?", "the diaphragm", ["the ribs", "the trachea", "the lungs"], "Pull it down: the balloons inflate."),
    ("In the bell-jar model, what do the balloons represent?", "the lungs", ["the alveoli walls", "the heart", "the diaphragm"], "They inflate when the sheet is pulled."),
    ("What is one weakness of the bell-jar model?", "The glass jar cannot move like a real ribcage.", ["It has no rubber sheet.", "The balloons are too small to see.", "It shows the ribs perfectly."], "Models are not perfect."),
])
B5 = bank([
    ("How does smoking damage the gas exchange system?", "Tar coats the airways and damages cilia and alveoli.", ["It cleans the lungs.", "It makes the alveoli bigger and better.", "It only affects the teeth."], "Smokers cough to clear mucus."),
    ("What happens in the airways during an asthma attack?", "The muscles around the bronchioles tighten and the lining swells, so less air gets through.", ["The alveoli burst.", "The diaphragm stops completely.", "The trachea grows longer."], "Inhalers relax the muscles."),
    ("How does a reliever inhaler help someone with asthma?", "It relaxes the muscles around the airways so they widen.", ["It adds oxygen to the blood directly.", "It kills bacteria.", "It makes the lungs larger."], "Widens the bronchioles."),
    ("Why do regular swimmers often have a larger lung volume?", "Exercise strengthens the breathing muscles.", ["Water fills their lungs.", "They breathe less.", "Their alveoli disappear."], "Training effect."),
    ("How could you measure the volume of air you breathe out in one breath?", "Breathe out through a tube into an upside-down bottle of water and see how much water is pushed out.", ["Weigh yourself before and after.", "Count your heartbeats.", "Measure your chest with a ruler only."], "Displacement of water."),
])


def body():
    think = ("<p><b>Breathing moves air in and out; gas exchange happens in the alveoli.</b></p>"
             "<ul><li>Air path: nose or mouth → trachea → bronchi → bronchioles → alveoli.</li>"
             "<li>Breathing in: diaphragm and intercostal muscles contract, ribs move up and out, chest volume increases, pressure falls, air flows in.</li>"
             "<li>In the alveoli, oxygen diffuses into the blood and carbon dioxide diffuses out.</li></ul>")
    ex = [("Breathing in: what does the diaphragm do?", ["It contracts"], "flattens and moves down"),
          ("Oxygen: 21% inhaled, 16% exhaled. Difference?", ["21 − 16"], "5 percentage points")]
    mist = ["Thinking the lungs suck air in by themselves.", "Thinking we breathe out only carbon dioxide.", "Mixing up breathing and respiration."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of the system", B1[:3] + [(g_path, 8), (g_job, 9)]),
        ("How we breathe", B1[3:] + [(g_mech, 10), (g_job, 5)]),
        ("Gas exchange", [(g_adapt, 6), (g_air, 6), (ukm(BS.g_job), 4), (ukm(BS.g_inter), 4)]),
        ("Breathing and exercise", [(g_rate, 16), (ukm(BS.g_level), 4)]),
        ("Health and the lungs", B5 + [(g_rate, 10), (ukm(BS.g_inter), 3), (g_job, 2)]),
    ])
    make_ks3(8, "breathing-and-gas-exchange", 2, "Biology", "Gas exchange systems",
             "The structure and functions of the gas exchange system in humans, including adaptations to function; the mechanism of breathing to move air in and out of the lungs, using a pressure model to explain the movement of gases, including simple measurements of lung volume; the impact of exercise, asthma and smoking on the human gas exchange system; the role of leaf stomata in gas exchange in plants.",
             "Breathing and Gas Exchange",
             "Year 8 Science: Breathing and Gas Exchange Worksheets (Lungs, Alveoli, Diaphragm)",
             "Breathing and Gas Exchange",
             "Free Year 8 science worksheets on breathing and gas exchange: the lungs, alveoli, the diaphragm, inhaled and exhaled air, exercise, asthma and smoking. 100 questions with answers.",
             "Gas exchange happens in the alveoli.",
             "Breathing in: the diaphragm contracts, chest volume rises, pressure falls.",
             body(),
             [("What happens when you breathe in?", "The diaphragm contracts and flattens and the intercostal muscles pull the ribs up and out. The chest volume increases, the pressure falls and air flows into the lungs."),
              ("Why are alveoli good at gas exchange?", "They have a huge surface area, walls one cell thick, a moist lining and a rich blood supply, so gases diffuse quickly."),
              ("How is exhaled air different from inhaled air?", "It has less oxygen (about 16% instead of 21%), much more carbon dioxide (about 4% instead of 0.04%) and more water vapour.")],
             sets)


if __name__ == "__main__":
    main()
