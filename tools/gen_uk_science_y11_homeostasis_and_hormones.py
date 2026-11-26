# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Biology): Homeostasis and Hormones
  python tools/gen_uk_science_y11_homeostasis_and_hormones.py
Homeostasis and control systems, the nervous system and reflex arcs, reaction time, the endocrine system, control of
blood glucose (insulin, glucagon, type 1 and type 2 diabetes), hormones in human reproduction, contraception, and
(higher tier) adrenaline, thyroxine and negative feedback. Blood glucose is in mmol/L (UK). Reuses the US Biology
feedback and temperature questions in British English.
Wrong answers come from real mistakes: "glucagon lowers blood glucose", "hormones travel along nerves", "the
sensory neurone carries impulses to the muscle", "type 2 diabetes is cured by insulin injections only".
"""
from uk_sci import item, bank, once, table
from uk_ks4 import U4, build

U, R, P, us = U4(62102)
HF = "bio_homeostasis_and_feedback"
us_loop, us_temp = us(HF, "g_loop"), us(HF, "g_temp")

ARC = ["stimulus", "receptor", "sensory neurone", "relay neurone", "motor neurone", "effector", "response"]


def g_arc():
    i = R.randrange(len(ARC) - 1)
    k = R.choice(["after", "before"])
    if k == "before":
        i += 1
    if not once(("arc", i, k)):
        return None
    a = ARC[i + 1] if k == "after" else ARC[i - 1]
    return item("In a reflex arc, what comes straight %s the %s?" % (k, ARC[i]), a, R.sample([x for x in ARC if x not in (a, ARC[i])], 3),
                "Stimulus → receptor → sensory neurone → relay neurone → motor neurone → effector → response.")


GL = [("pituitary gland", "FSH, LH and TSH"), ("thyroid gland", "thyroxine"), ("adrenal glands", "adrenaline"), ("pancreas", "insulin and glucagon"),
      ("ovaries", "oestrogen and progesterone"), ("testes", "testosterone")]


def g_gland():
    g, h = R.choice(GL)
    k = R.choice(["g", "h"])
    if not once(("gl", g, k)):
        return None
    if k == "h":
        return item("Which of these is released by the %s?" % g, h, R.sample([x[1] for x in GL if x[0] != g], 3), "The %s releases %s into the blood." % (g, h))
    return item("Which gland releases %s?" % h, "the " + g, R.sample(["the " + x[0] for x in GL if x[0] != g], 3), "The %s releases %s into the blood." % (g, h))


def g_react():
    u = R.choice(["s", "ms"])
    base = R.choice(range(20, 36)) / 100
    d = [R.choice([-3, -2, -1, 0, 1, 2, 3]) / 100 for _ in range(2)]
    t = [base + d[0], base + d[1], base - d[0] - d[1]]
    if len(set(t)) < 3 or min(t) < 0.15 or not once(("rt", base, tuple(d))):
        return None
    name = P.next()[0]
    f = (lambda x: "%.2f s" % x) if u == "s" else (lambda x: "%d ms" % round(x * 1000))
    tab = table(["Test", "Reaction time"], [[str(i + 1), f(x)] for i, x in enumerate(t)])
    return item(tab + "%s measured %s reaction time three times. What is the mean reaction time?" % (name, "her" if name in P_GIRLS else "his"), f(base),
                [f(max(t)), f(min(t)), f(sum(t))], "Add the three times and divide by 3.")


from uk_ks3 import GIRLS as P_GIRLS


def g_glu():
    v = R.choice([2.8, 3.0, 3.2, 3.4, 3.5, 3.6, 3.8, 7.8, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.5, 14.0, 15.0])
    k = R.choice(["hormone", "liver"])
    if not once(("gl", v, k)):
        return None
    name = P.next()[0]
    high = v > 7
    if k == "hormone":
        return item("%s's blood glucose is %.1f mmol/L (normal is about 4–7 mmol/L). Which hormone does the pancreas release?" % (name, v), "insulin" if high else "glucagon",
                    ["glucagon" if high else "insulin", "adrenaline", "no hormone"], "High → insulin (glucose into cells, stored as glycogen). Low → glucagon (glycogen → glucose).")
    return item("%s's blood glucose is %.1f mmol/L (normal is about 4–7 mmol/L). What happens in the liver?" % (name, v),
                "Glucose is converted to glycogen and stored." if high else "Glycogen is converted to glucose and released.",
                ["Glycogen is converted to glucose and released." if high else "Glucose is converted to glycogen and stored.", "The liver makes insulin.", "Nothing changes."],
                "Insulin and glucagon act on the liver.")


CY = [("FSH", "causes an egg to mature in the ovary"), ("LH", "stimulates the release of an egg (ovulation)"),
      ("oestrogen", "makes the lining of the uterus grow"), ("progesterone", "keeps the lining of the uterus thick")]


def g_cycle():
    h, j = R.choice(CY)
    k = R.choice(["h", "j"])
    if not once(("cy", h, k)):
        return None
    if k == "h":
        return item("In the menstrual cycle, what does %s do?" % h, j, [x[1] for x in CY if x[0] != h], "FSH → egg matures; LH → ovulation; oestrogen → lining grows; progesterone → lining kept.")
    return item("Which hormone %s?" % j, h, [x[0] for x in CY if x[0] != h], "FSH and LH come from the pituitary; oestrogen and progesterone from the ovaries.")


B1 = bank([
    ("What is homeostasis?", "keeping internal conditions constant", ["growing bigger", "changing body temperature to match the air", "making new cells"], "Body temperature, blood glucose, water levels."),
    ("What are the three parts of an automatic control system?", "receptors, coordination centres and effectors", ["bones, muscles and skin", "nerves, blood and hormones only", "genes, cells and organs"], "Receptors detect, coordination centres process, effectors respond."),
    ("Why are reflex actions fast?", "They do not involve the conscious part of the brain.", ["They use hormones.", "They go through the stomach.", "They use the motor neurone only."], "Automatic."),
    ("What crosses a synapse?", "a chemical that diffuses across the gap", ["an electrical wire", "blood", "a hormone from the pituitary"], "The chemical triggers an impulse in the next neurone."),
])
B3 = bank([
    ("How is the endocrine system different from the nervous system?", "Hormones travel in the blood and act more slowly for longer.", ["Hormones travel along neurones.", "Hormones act faster.", "There is no difference."], "Nerves are fast and short-lived."),
    ("Why is the pituitary called the 'master gland'?", "It releases hormones that make other glands release hormones.", ["It is the largest gland.", "It makes insulin.", "It controls bones only."], "In the brain."),
    ("What causes type 1 diabetes?", "The pancreas does not make enough insulin.", ["Body cells stop responding to insulin only.", "Too much glucagon.", "Eating too much salt."], "Treated with insulin injections."),
    ("How is type 2 diabetes often treated?", "a carbohydrate-controlled diet and exercise", ["only by surgery", "by eating more sugar", "it cannot be treated"], "Body cells no longer respond to insulin; obesity is a risk factor."),
])
B5 = bank([
    ("How does the contraceptive pill work?", "It contains hormones that stop FSH, so eggs do not mature.", ["It kills sperm in the stomach.", "It is a barrier.", "It removes the uterus."], "Oral contraceptives contain oestrogen and/or progesterone."),
    ("Which contraceptive also protects against sexually transmitted infections?", "condoms", ["the pill", "an implant", "a coil"], "Barrier method."),
    ("What does adrenaline do?", "increases the heart rate to prepare the body for 'fight or flight'", ["lowers blood glucose", "makes the uterus lining grow", "slows breathing"], "From the adrenal glands."),
    ("What does thyroxine control?", "the basal metabolic rate", ["blood glucose", "ovulation", "the menstrual cycle"], "Controlled by negative feedback."),
])

if __name__ == "__main__":
  build(U, 11, "homeostasis-and-hormones", 2, "Biology", "Homeostasis and response",
      "Homeostasis and control systems; the structure and function of the nervous system and reflex arcs; reaction time; the endocrine system; control of blood glucose concentration and diabetes; hormones in human reproduction and contraception; (higher tier) adrenaline, thyroxine and negative feedback.",
      "Homeostasis and Hormones", "Homeostasis and Hormones",
      "Free Year 11 GCSE Combined Science worksheets on homeostasis: reflex arcs, reaction time, hormones, blood glucose, diabetes, the menstrual cycle and contraception. 100 questions with answers.",
      "Homeostasis keeps the body's conditions constant.",
      "Insulin lowers blood glucose; glucagon raises it.",
      "<p><b>Nerves are fast; hormones are slower and last longer.</b></p><ul><li>Reflex arc: receptor → sensory neurone → relay neurone → motor neurone → effector.</li>"
      "<li>Blood glucose too high → insulin (glucose stored as glycogen). Too low → glucagon (glycogen → glucose).</li>"
      "<li>FSH matures an egg, LH causes ovulation, oestrogen and progesterone build and keep the uterus lining.</li></ul>",
      [("Blood glucose 11 mmol/L. Hormone?", ["Above 4–7", "Too high"], "insulin"), ("Reaction times 0.24, 0.26, 0.28 s. Mean?", ["0.78 ÷ 3"], "0.26 s")],
      ["Thinking glucagon lowers blood glucose.", "Thinking hormones travel along nerves.", "Thinking the sensory neurone carries impulses to the muscle."],
      [("What happens in a reflex arc?", "A receptor detects a stimulus, a sensory neurone carries the impulse to the spinal cord, a relay neurone passes it on, and a motor neurone carries it to an effector."),
       ("How is blood glucose controlled?", "The pancreas releases insulin when glucose is high and glucagon when it is low. Both act on the liver."),
       ("What is the difference between type 1 and type 2 diabetes?", "In type 1 the pancreas makes too little insulin. In type 2 the body cells stop responding to insulin.")],
      [("Homeostasis and nerves", B1 + [(us_loop, 4), (g_arc, 6), (us_temp, 4), (g_react, 2)]),
       ("Reaction time", [(g_react, 12), (g_arc, 4), (us_loop, 4)]),
       ("Hormones", B3 + [(g_gland, 8), (g_glu, 8)]),
       ("Blood glucose", [(g_glu, 16), (g_react, 4)]),
       ("Reproductive hormones", B5 + [(g_cycle, 7), (g_glu, 4), (g_react, 3), (g_gland, 2)])])
