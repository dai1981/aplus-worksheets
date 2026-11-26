# -*- coding: utf-8 -*-
"""
UK Year 6 science: The Circulatory System (Animals, including humans)
  python tools/gen_uk_science_y6_the_circulatory_system.py
The heart, blood vessels (arteries, veins, capillaries) and blood (red and white blood cells, platelets, plasma),
the double loop through the lungs and body, and measuring pulse rate before and after exercise.
Wrong answers come from real mistakes: "veins carry blood away from the heart", "the heart is on the left side of the
chest only", "pulse per minute = the beats counted in 15 seconds", "blood goes straight from the body back to the body".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61604)
R = U.R
P = People(R)

PART = [("the heart", "pumping blood around the body"), ("arteries", "carrying blood away from the heart"), ("veins", "carrying blood back to the heart"),
        ("capillaries", "letting oxygen and nutrients pass into the cells"), ("red blood cells", "carrying oxygen from the lungs to the body"),
        ("white blood cells", "fighting germs that cause disease"), ("platelets", "helping blood clot to stop bleeding"),
        ("plasma", "carrying nutrients, water and waste as a liquid"), ("the lungs", "giving the blood oxygen and taking away carbon dioxide")]


def g_part():
    p, f = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    if k:
        return item("What is the main job of %s?" % p, f, R.sample([x[1] for x in PART if x[1] != f], 3), "%s: %s." % (p[0].upper() + p[1:], f))
    return item("Which part of the circulatory system has this job: %s?" % f, p, R.sample([x[0] for x in PART if x[0] != p], 3), "%s: %s." % (p[0].upper() + p[1:], f))


LOOP = ["the body's organs and muscles", "the right side of the heart", "the lungs", "the left side of the heart"]


def g_loop():
    i = R.randrange(4)
    k = R.random() < 0.5
    if not once(("lo", i, k)):
        return None
    if k:
        a = LOOP[(i + 1) % 4]
        return item("Blood leaves %s. Where does it go next?" % LOOP[i], a, [x for x in LOOP if x not in (a, LOOP[i])] + ["the stomach"],
                    "Body → right side of heart → lungs → left side of heart → body.")
    a = LOOP[(i - 1) % 4]
    return item("Blood arrives at %s. Where has it just come from?" % LOOP[i], a, [x for x in LOOP if x not in (a, LOOP[i])] + ["the brain only"],
                "Body → right side of heart → lungs → left side of heart → body.")


OXY = [("blood leaving the lungs", "rich in oxygen"), ("blood in the left side of the heart", "rich in oxygen"), ("blood in the arteries going to the leg muscles", "rich in oxygen"),
       ("blood coming back from the body in the veins", "low in oxygen"), ("blood in the right side of the heart", "low in oxygen"), ("blood leaving a hard-working muscle", "low in oxygen")]


def g_oxy():
    w, a = R.choice(OXY)
    if not once(("ox", w)):
        return None
    return item("Is %s rich in oxygen or low in oxygen?" % w, a, ["low in oxygen" if a == "rich in oxygen" else "rich in oxygen", "it has no oxygen at all", "it is pure oxygen"],
                "Blood picks up oxygen in the lungs and gives it to the body's cells.")


def g_pulse():
    who = P.next()[0]
    sec = R.choice([10, 15, 20, 30])
    bpm = R.choice(range(60, 181, 6 if sec == 10 else 4 if sec == 15 else 3 if sec == 20 else 2))
    n = bpm * sec // 60
    if bpm * sec % 60 or not once(("pu", sec, n)):
        return None
    g = "%d beats per minute" % bpm
    return item("%s counts %d pulse beats in %d seconds. What is %s's pulse rate?" % (who, n, sec, who), g,
                uniq(g, ["%d beats per minute" % n, "%s beats per minute" % format(n * sec, ","), "%d beats per minute" % (n + 60), "%d beats per minute" % (bpm * 2)]),
                "There are %d lots of %d seconds in a minute: %d × %d = %d." % (60 // sec, sec, n, 60 // sec, bpm))


def g_avg():
    who = P.next()[0]
    a = R.choice(range(64, 100))
    xs = [a + d for d in R.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4], 3)]
    if sum(xs) % 3 or not once(("av", tuple(sorted(xs)))):
        return None
    m = sum(xs) // 3
    g = "%d beats per minute" % m
    return item("%s measures a resting pulse three times: %s beats per minute. What is the mean (average)?" % (who, ", ".join(map(str, xs))), g,
                uniq(g, ["%d beats per minute" % sum(xs), "%d beats per minute" % max(xs), "%d beats per minute" % min(xs), "%d beats per minute" % (m + 3)]),
                "Add them and divide by 3: %d ÷ 3 = %d." % (sum(xs), m))


def g_ex():
    who = P.next()[0]
    acts = [("resting", R.choice(range(66, 86, 2))), ("walking", 0), ("jogging", 0), ("sprinting", 0)]
    r = acts[0][1]
    acts[1] = ("walking", r + R.choice([10, 14, 18]))
    acts[2] = ("jogging", acts[1][1] + R.choice([24, 30, 36]))
    acts[3] = ("sprinting", acts[2][1] + R.choice([20, 26, 32]))
    k = R.choice(["most", "diff", "why", "pattern", "read"])
    if not once(("ex", k, r, acts[2][1] if k in ("diff", "read") else 0)) or (k in ("most", "why", "pattern") and not once(("exk", k), 2)):
        return None
    tab = table(["Activity (1 minute)", "Pulse rate (beats per minute)"], [[a, str(b)] for a, b in acts])
    if k == "most":
        return item(tab + "After which activity was %s's pulse rate highest?" % who, "sprinting", ["resting", "walking", "jogging"], "Harder exercise makes the heart beat faster.")
    if k == "diff":
        d = acts[2][1] - r
        g = "%d beats per minute" % d
        return item(tab + "How much higher was %s's pulse after jogging than at rest?" % who, g, uniq(g, ["%d beats per minute" % acts[2][1], "%d beats per minute" % (acts[3][1] - r), "%d beats per minute" % (acts[1][1] - r), "%d beats per minute" % r]),
                    "%d − %d = %d." % (acts[2][1], r, d))
    if k == "read":
        return item(tab + "What was %s's pulse rate after walking?" % who, "%d beats per minute" % acts[1][1], ["%d beats per minute" % acts[x][1] for x in (0, 2, 3)], "Read the walking row.")
    if k == "why":
        return item(tab + "Why does the pulse rate go up during exercise?", "The muscles need more oxygen and food, so the heart pumps blood faster.",
                    ["The heart gets tired and slows down.", "The lungs stop working.", "Blood gets thicker."], "Working muscles need more oxygen.")
    return item(tab + "What pattern does %s's table show?" % who, "The harder the exercise, the higher the pulse rate.", ["The harder the exercise, the lower the pulse rate.", "Pulse rate does not change.", "Walking gives the highest pulse rate."],
                "As the activity gets harder, the numbers go up.")


B1 = bank([
    ("What are the three main parts of the circulatory system?", "the heart, blood vessels and blood", ["the lungs, stomach and brain", "bones, muscles and skin", "the mouth, teeth and tongue"], "Heart pumps, vessels carry, blood transports."),
    ("Which organ pumps blood around the body?", "the heart", ["the lungs", "the brain", "the liver"], "The heart is a muscle."),
    ("What is your pulse?", "the beat of blood being pushed through an artery by the heart", ["air going into the lungs", "food moving through the gut", "a muscle getting longer"], "Each pulse is one heartbeat."),
    ("Where can you easily feel your pulse?", "on the inside of your wrist or the side of your neck", ["on your elbow", "on your knee cap", "on your fingernail"], "Arteries are close to the skin there."),
    ("Which blood vessels carry blood away from the heart?", "arteries", ["veins", "capillaries", "nerves"], "A for arteries, A for away."),
    ("Which gas does blood pick up in the lungs?", "oxygen", ["carbon dioxide", "nitrogen", "helium"], "Oxygen is carried by red blood cells."),
    ("Which waste gas does blood carry to the lungs?", "carbon dioxide", ["oxygen", "hydrogen", "nitrogen"], "We breathe it out."),
    ("Why is the circulatory system called a double loop?", "Blood passes through the heart twice: once to the lungs and once to the body.", ["There are two hearts.", "Blood goes round twice as fast.", "Only half the blood moves."], "Heart → lungs → heart → body."),
])
B5 = bank([
    ("Why should you measure your pulse three times and find the mean?", "to make the result more reliable", ["to make the heart beat faster", "because one reading is always wrong", "to use up time"], "Repeats reduce the effect of mistakes."),
    ("Why do fit people often have a lower resting pulse?", "Their heart is stronger and pumps more blood with each beat.", ["Their heart is smaller.", "They have less blood.", "Their heart has stopped."], "Exercise strengthens the heart."),
    ("How long does it take for the pulse to return to resting after exercise? How could you find out?", "Measure the pulse every minute after stopping until it matches the resting rate.", ["Guess it.", "Measure it once a week.", "Count breaths instead."], "Plan a fair investigation."),
    ("Who first described how blood circulates around the body in 1628?", "William Harvey", ["Alexander Fleming", "Charles Darwin", "Isaac Newton"], "An English doctor."),
    ("Why does a cut eventually stop bleeding?", "Platelets help the blood clot.", ["Red blood cells stop moving.", "The heart stops.", "Veins close forever."], "Clotting forms a scab."),
])


def body():
    think = ("<p><b>The heart pumps blood through blood vessels to every part of the body.</b></p>"
             "<ul><li>Arteries carry blood away from the heart; veins carry it back; capillaries let oxygen and nutrients reach the cells.</li>"
             "<li>Double loop: body → heart → lungs (pick up oxygen) → heart → body.</li>"
             "<li>Blood: red blood cells carry oxygen, white blood cells fight germs, platelets clot, plasma carries nutrients and water.</li>"
             "<li>Pulse rate (beats per minute) = beats counted × how many of those time periods fit in 60 seconds.</li></ul>")
    ex = [("20 beats in 15 seconds. Pulse rate?", ["60 ÷ 15 = 4", "20 × 4"], "80 beats per minute"),
          ("Blood leaves the lungs. Next?", ["Lungs → left side of heart"], "the heart, then the body")]
    mist = ["Mixing up arteries and veins.", "Forgetting to scale up: 20 beats in 15 seconds is not 20 per minute.", "Thinking blood goes from the body straight back to the body without the lungs."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The heart and blood", B1 + [(g_part, 8), (g_loop, 4)]),
        ("Parts and jobs", [(g_part, 10), (g_loop, 4), (g_oxy, 6)]),
        ("Measuring pulse rate", [(g_pulse, 14), (g_avg, 6)]),
        ("Pulse and exercise", [(g_ex, 14), (g_avg, 6)]),
        ("Investigating the heart", B5 + [(g_pulse, 7), (g_ex, 5), (g_avg, 3)]),
    ])
    make_uk(6, "the-circulatory-system", 4, "Animals, including humans",
            "Identify and name the main parts of the human circulatory system, and describe the functions of the heart, blood vessels and blood.",
            "The Circulatory System",
            "Year 6 Science: The Circulatory System Worksheets (Heart, Blood and Pulse Rate)",
            "Circulatory System",
            "Free Year 6 science worksheets on the circulatory system: the heart, arteries, veins and capillaries, blood cells, the double loop and pulse rate investigations. 100 questions with answers.",
            "The heart pumps blood round the body.",
            "Arteries away, veins back; blood carries oxygen from the lungs to the cells.",
            body(),
            [("What does the circulatory system do?", "It moves blood around the body. Blood carries oxygen and nutrients to the cells and takes away waste such as carbon dioxide."),
             ("What is the difference between arteries and veins?", "Arteries carry blood away from the heart. Veins carry blood back to the heart. Tiny capillaries join them."),
             ("How do you work out a pulse rate?", "Count the beats for a set time, such as 15 seconds, then multiply to find the beats in 60 seconds. For 15 seconds, multiply by 4.")],
            sets)


if __name__ == "__main__":
    main()
