# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 8: Homeostasis, Co-ordination and Response
  python tools/gen_sg_science_s4_homeostasis_coordination_and_response.py
Homeostasis and negative feedback; control of body temperature by the skin (sweating, vasodilation and vasoconstriction, shivering);
control of blood glucose by insulin and glucagon, and diabetes; the nervous system (central and peripheral, sensory, relay and motor
neurones, reflex arcs, voluntary and reflex actions); the eye (structure, pupil reflex, accommodation); hormones and endocrine glands,
adrenaline; comparing nervous and hormonal control.
UK KS4 and US NGSS homeostasis makers are reused (Singapore names, mmol/L for glucose); the rest is written here.
Wrong answers come from real mistakes: "blood vessels move closer to the skin surface", "insulin turns glucose into glycogen in the
muscles only", "the lens gets thicker for distant objects", "reflexes are controlled by the brain", "hormones travel along nerves".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 16
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_arc = src("gen_uk_science_y11_homeostasis_and_hormones", "g_arc")
uk_gland = src("gen_uk_science_y11_homeostasis_and_hormones", "g_gland", drop=["FSH", "TSH", "thyroxine", "thyroid"])
uk_react = src("gen_uk_science_y11_homeostasis_and_hormones", "g_react")

SKIN = [("sweating increases", "hot", "Water in sweat evaporates, taking heat (latent heat) from the skin."),
        ("arterioles in the skin dilate (vasodilation)", "hot", "More blood flows near the skin surface, so more heat is lost by radiation."),
        ("arterioles in the skin constrict (vasoconstriction)", "cold", "Less blood flows near the skin surface, so less heat is lost."),
        ("shivering starts", "cold", "Rapid muscle contractions release heat from respiration."),
        ("sweating decreases", "cold", "Less heat is lost by evaporation."),
        ("the metabolic rate increases", "cold", "More respiration releases more heat.")]


def g_skin():
    r_, cond, why = R.choice(SKIN)
    if R.random() < 0.5:
        return tq("When %s, which is the body responding to?" % r_, "a body temperature above normal" if cond == "hot" else "a body temperature below normal",
                  ["a body temperature above normal" if cond == "cold" else "a body temperature below normal", "a rise in blood glucose", "a fall in blood glucose"], why)
    return tq("How does it help body temperature control when %s?" % r_, why, R.sample([x[2] for x in SKIN if x[2] != why], 3), "The hypothalamus detects blood temperature and controls these responses.")


def g_glu():
    v = R.choice([2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.5])
    hi = v > 7
    k = R.choice(["hormone", "liver", "result"])
    nm = P.next()[0]
    if k == "hormone":
        a = "insulin" if hi else "glucagon"
        return tq("%s's blood glucose is %s mmol/L (normal is about 4–7 mmol/L). Which hormone does the pancreas release more of?" % (nm, v), a,
                  [x for x in ("insulin", "glucagon", "adrenaline", "ADH") if x != a], "High glucose → insulin; low glucose → glucagon.")
    if k == "liver":
        a = "Glucose is converted to glycogen and stored." if hi else "Glycogen is converted to glucose, which is released into the blood."
        return tq("%s's blood glucose is %s mmol/L (normal is about 4–7 mmol/L). What does the liver do?" % (nm, v), a,
                  [x for x in ("Glucose is converted to glycogen and stored.", "Glycogen is converted to glucose, which is released into the blood.", "The liver makes insulin.", "Glucose is converted into urea.") if x != a],
                  "Insulin and glucagon both act on the liver.")
    a = "It falls back towards normal." if hi else "It rises back towards normal."
    return tq("%s's blood glucose is %s mmol/L. After the pancreas responds, what happens to the blood glucose level?" % (nm, v), a,
              [x for x in ("It falls back towards normal.", "It rises back towards normal.", "It keeps moving further from normal.", "It drops to zero.") if x != a], "Negative feedback.")


def g_temp():
    v = R.choice([35.2, 35.5, 35.8, 36.0, 36.2, 37.9, 38.2, 38.5, 38.8, 39.2])
    hot = v > 37
    a = "sweating increases and arterioles in the skin dilate" if hot else "shivering and vasoconstriction of skin arterioles"
    o = "shivering and vasoconstriction of skin arterioles" if hot else "sweating increases and arterioles in the skin dilate"
    return tq("A person's core body temperature is %s °C (normal is about 37 °C). How does the body respond?" % v, a, [o, "the pancreas releases insulin", "the pupils become smaller"],
              "The hypothalamus detects the change and the skin responds to bring the temperature back to 37 °C.")


EYE = [("the cornea", "refracts (bends) light entering the eye"), ("the iris", "controls the amount of light entering by changing the size of the pupil"),
       ("the lens", "focuses light onto the retina"), ("the retina", "contains rods and cones that detect light"),
       ("the optic nerve", "carries nerve impulses from the retina to the brain"), ("the ciliary muscles", "contract or relax to change the shape of the lens"),
       ("the suspensory ligaments", "hold the lens in place"), ("the fovea (yellow spot)", "has the most cones and gives the sharpest image"),
       ("the blind spot", "has no rods or cones because the optic nerve leaves there")]
g_eye = rows(R, EYE, "Which statement about %s is correct? It…", "Which part of the eye %s?")

ACC = [("looking at a distant object", "the ciliary muscles", "relax"), ("looking at a distant object", "the suspensory ligaments", "become taut"),
       ("looking at a distant object", "the lens", "becomes thinner (less convex)"), ("reading a book close up", "the ciliary muscles", "contract"),
       ("reading a book close up", "the suspensory ligaments", "slacken"), ("reading a book close up", "the lens", "becomes thicker (more convex)"),
       ("walking into bright sunlight", "the pupil", "becomes smaller"), ("walking into a dark room", "the pupil", "becomes larger"),
       ("walking into bright sunlight", "the circular muscles of the iris", "contract"), ("walking into a dark room", "the radial muscles of the iris", "contract")]
OPP = {"relax": "contract", "contract": "relax", "become taut": "slacken", "slacken": "become taut", "becomes thinner (less convex)": "becomes thicker (more convex)",
       "becomes thicker (more convex)": "becomes thinner (less convex)", "becomes smaller": "becomes larger", "becomes larger": "becomes smaller"}


def g_acc():
    sit, part, a = R.choice(ACC)
    ex2 = {"the lens": ["stays exactly the same", "moves closer to the retina"], "the pupil": ["stays exactly the same", "moves to the side of the iris"],
           "the suspensory ligaments": ["stay exactly the same", "pull the lens towards the retina"]}.get(part, ["stay exactly the same", "push the lens forwards"])
    w = [OPP[a]] + ex2
    return tq("When %s, what happens to %s?" % (sit, part), a, w,
              "Near object: ciliary muscles contract, ligaments slacken, lens thicker. Bright light: circular muscles contract and the pupil becomes smaller.")


NEU = [("a sensory neurone", "carries impulses from a receptor to the central nervous system"), ("a relay neurone", "connects sensory and motor neurones in the spinal cord or brain"),
       ("a motor neurone", "carries impulses from the central nervous system to an effector"), ("a receptor", "detects a stimulus"),
       ("an effector", "a muscle or gland that carries out a response"), ("the central nervous system", "the brain and spinal cord")]
g_neu = rows(R, NEU, "What is %s?", "Which term describes this: “%s”?")

ACTS = [("pulling your hand away from a hot pan", "a reflex action"), ("blinking when dust blows into your eye", "a reflex action"),
        ("the knee jerk when the tendon is tapped", "a reflex action"), ("the pupil shrinking in bright light", "a reflex action"),
        ("choosing a book to read", "a voluntary action"), ("writing your name", "a voluntary action"), ("kicking a ball into a goal", "a voluntary action"),
        ("raising your hand to answer a question", "a voluntary action")]


def g_act():
    x, a = R.choice(ACTS)
    return tq("Is %s a reflex action or a voluntary action?" % x, a, [y for y in ("a reflex action", "a voluntary action", "a hormonal response", "neither") if y != a],
              "Reflexes are rapid, automatic and do not need conscious thought; voluntary actions are controlled by the brain consciously.")


NVH = [("speed", "very fast (milliseconds)", "slower (seconds to hours)"), ("signal", "electrical impulses along neurones", "chemicals carried in the blood"),
       ("duration of effect", "short-lived", "longer-lasting"), ("area affected", "a specific effector", "often many target organs")]


def g_nvh():
    f, n, h = R.choice(NVH)
    ner = R.random() < 0.5
    a = n if ner else h
    others = [x[1] for x in NVH if x[0] != f] + [x[2] for x in NVH if x[0] != f]
    return tq("Compare nervous and hormonal control. For %s control, what is the %s?" % ("nervous" if ner else "hormonal", f), a, [h if ner else n] + R.sample(others, 2),
              "Nervous: fast, electrical, short-lived, precise. Hormonal: slower, chemical in blood, longer-lasting, widespread.")


POOL1 = pool(R, [
    ("What is homeostasis?", "keeping the internal environment of the body constant", ["changing body temperature with the weather", "the removal of waste", "the digestion of food"], "Examples: body temperature, blood glucose, water potential."),
    ("What is negative feedback?", "a change from the normal level is detected and corrected, bringing it back to normal", ["a change that makes itself bigger", "a response that never stops", "a signal sent only by hormones"], "Most homeostasis uses negative feedback."),
    ("Which part of the brain detects changes in blood temperature?", "the hypothalamus", ["the cerebellum", "the medulla", "the pituitary gland"], "It controls sweating and shivering."),
    ("Which organ releases insulin and glucagon?", "the pancreas (islets of Langerhans)", ["the liver", "the kidneys", "the adrenal glands"], "Insulin lowers, glucagon raises blood glucose."),
    ("How does insulin lower blood glucose?", "It makes liver and muscle cells take up glucose and convert it to glycogen.", ["It breaks down glycogen.", "It excretes glucose in urine.", "It turns glucose into protein."], "It also increases respiration of glucose."),
    ("What is type 1 diabetes?", "a condition in which the pancreas does not make enough insulin", ["too much glucagon", "a lack of sweat glands", "damage to the retina only"], "It is treated with insulin injections."),
    ("What is a hormone?", "a chemical made by an endocrine gland and carried in the blood to target organs", ["an electrical impulse", "an enzyme in the gut", "a type of white blood cell"], "Hormones are destroyed by the liver."),
    ("When is adrenaline released?", "in frightening or stressful situations", ["after a meal", "during sleep", "when it is cold only"], "It prepares the body for fight or flight."),
    ("What effects does adrenaline have?", "faster heart and breathing rate, more glucose in the blood and pupils widen", ["slower heart rate and less glucose", "sweating stops and pupils shrink", "digestion speeds up"], "More oxygen and glucose reach the muscles."),
    ("What is a synapse?", "a tiny gap between two neurones, crossed by chemical transmitters", ["the brain and spinal cord", "a type of receptor", "a gland that makes hormones"], "It makes impulses travel in one direction."),
])
POOL5 = pool(R, [
    ("Why is the pupil reflex useful?", "It stops too much light damaging the retina and lets in more light in dim conditions.", ["It focuses light on the lens.", "It makes the eye produce tears.", "It moves the eye to the light."], "It is an automatic reflex."),
    ("A person with type 2 diabetes is often advised to exercise and eat less sugar. Why?", "Their cells respond poorly to insulin, so controlling diet and weight helps keep blood glucose down.", ["Exercise makes the pancreas grow.", "Sugar cures diabetes.", "Exercise stops insulin being made."], "Type 2 is linked to obesity."),
    ("In a reflex arc, why is the response so fast?", "The impulse travels through a short pathway, often only the spinal cord, without conscious thought.", ["The brain decides very quickly.", "Hormones travel faster than nerves.", "The receptor is the effector."], "Reflexes protect the body."),
    ("Why does a person's skin look red when they are hot?", "Vasodilation brings more blood near the skin surface.", ["Blood vessels move up through the skin.", "Sweat is red.", "The skin cells make red pigment."], "Blood vessels do not move; arterioles widen."),
    ("Why does the body temperature stay close to 37 °C?", "Enzymes work best at this temperature.", ["Water boils at 37 °C.", "Blood clots above 37 °C.", "Cells stop dividing below 37 °C."], "Too hot denatures enzymes."),
    ("Someone has a damaged motor neurone in the arm. What happens when they touch a hot object?", "They feel the heat but cannot move the arm away by reflex.", ["They cannot feel the heat.", "They move faster than normal.", "Nothing reaches the spinal cord."], "The sensory neurone still works."),
    ("Why do older people often need reading glasses?", "The lens becomes less elastic, so it cannot become thick enough for near objects.", ["The retina grows.", "The pupil disappears.", "The cornea stops bending light."], "Accommodation becomes harder."),
    ("Blood glucose rises after a meal and then falls back to normal. What is this an example of?", "negative feedback", ["positive feedback", "a reflex action", "accommodation"], "Insulin brings the level back down."),
])


def main():
    sets = U.sets([
        ("Homeostasis and temperature", [(POOL1, 4), (g_skin, 8), (g_temp, 6), (POOL5, 2)]),
        ("Blood glucose", [(g_glu, 12), (POOL1, 4), (uk_gland, 2), (g_nvh, 2)]),
        ("The nervous system", [(g_neu, 7), (uk_arc, 6), (g_act, 5), (uk_react, 2)]),
        ("The eye", [(g_eye, 12), (g_acc, 7), (uk_react, 1)]),
        ("Hormones and exam-style questions", [(POOL5, 6), (g_nvh, 4), (POOL1, 2), (g_acc, 2), (g_act, 2), (g_glu, 4)]),
    ])
    make_ol(LV, SUBJ, "homeostasis-coordination-and-response", SORT, "Homeostasis, Co-ordination and Response",
            "Define homeostasis and explain negative feedback; describe the control of body temperature by the skin and the hypothalamus; describe the control "
            "of blood glucose by insulin and glucagon and the treatment of diabetes; describe the nervous system, the structure and functions of sensory, relay "
            "and motor neurones, reflex arcs and voluntary and reflex actions; describe the structure of the eye, the pupil reflex and accommodation; define a "
            "hormone, describe the effects of adrenaline and compare nervous and hormonal control (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Homeostasis, Co-ordination and Response", "Homeostasis",
            "Free Secondary 4 O-Level Biology worksheets on homeostasis, co-ordination and response: negative feedback, temperature control, insulin and glucagon, "
            "diabetes, neurones, reflex arcs, the eye and hormones. 100 questions with answers.",
            "Detect the change, correct it, return to normal.", "Nerves: fast and electrical. Hormones: slower, chemicals in the blood.",
            "<p><b>The body keeps conditions steady by negative feedback.</b></p><ul>"
            "<li>Too hot: sweating, vasodilation. Too cold: shivering, vasoconstriction. The hypothalamus controls these.</li>"
            "<li>High blood glucose → insulin → glucose to glycogen. Low → glucagon → glycogen to glucose.</li>"
            "<li>Reflex arc: stimulus → receptor → sensory neurone → relay neurone → motor neurone → effector.</li>"
            "<li>Near object: ciliary muscles contract, suspensory ligaments slacken, lens thicker. Bright light: the pupil becomes smaller.</li></ul>",
            [("Blood glucose 10 mmol/L. Hormone?", ["above normal", "lower it"], "insulin"),
             ("Reading close up. Ciliary muscles?", ["need a thicker lens"], "contract")],
            ["Saying blood vessels move to the skin surface.", "Saying the lens gets thicker for distant objects.", "Saying reflexes need the brain to decide.",
             "Saying hormones travel along nerves."],
            [("How does the body cool down?", "Sweat glands release more sweat, which evaporates and removes heat, and arterioles in the skin dilate so more heat is lost from blood near the surface."),
             ("What is the difference between insulin and glucagon?", "Insulin is released when blood glucose is high and makes the liver store glucose as glycogen. Glucagon is released when blood glucose is low and makes the liver convert glycogen to glucose."),
             ("How does the eye focus on a near object?", "The ciliary muscles contract, the suspensory ligaments slacken and the lens becomes thicker, so light is refracted more onto the retina.")],
            sets)


if __name__ == "__main__":
    main()
