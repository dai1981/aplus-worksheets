# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U01: the nervous and endocrine systems coordinating the body's response to a
stimulus, reflexes, hormones, and homeostasis by negative feedback (body temperature, blood glucose, water balance).
  python tools/gen_au_science_y9_nervous_and_endocrine_systems.py
Reuses the SG Secondary 4 homeostasis makers, the UK Year 11 homeostasis and hormones makers, the US Biology homeostasis and
feedback makers and the US Grade 6 nervous system makers with Australian names, plus own questions on heat stress at outdoor
sport and type 1 diabetes.
Wrong answers come from real mistakes: thinking hormones act faster than nerves, thinking a reflex goes through the brain first,
and thinking negative feedback means "something bad happens".
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

S4 = "gen_sg_science_s4_homeostasis_coordination_and_response"
K11 = "gen_uk_science_y11_homeostasis_and_hormones"
BIO = "gen_us_science_bio_homeostasis_and_feedback"
G6 = "gen_us_science_g6_senses_and_the_nervous_system"
s_skin = src(S4, "g_skin")
s_glu = src(S4, "g_glu")
s_act = src(S4, "g_act")
s_nvh = src(S4, "g_nvh")
s_neu = src(S4, "g_neu")
s_acc = limit(src(S4, "g_acc"), 3)
k_arc = src(K11, "g_arc")
k_gland = src(K11, "g_gland")
k_react = limit(src(K11, "g_react"), 10)
k_b1 = src.B(K11, "B1")
k_b5 = src.B(K11, "B5", drop=["contracept", "condom"])
b_loop = src(BIO, "g_loop")
b_b1 = src.B(BIO, "B1")
b_b5 = src.B(BIO, "B5")
n_path = limit(src(G6, "g_path"), 6)
n_rec = src(G6, "g_rec")
n_b1 = src.B(G6, "B1")

POOL1 = pool(R, [
    ("What is a stimulus?", "a change in the environment that the body detects", ["a hormone", "a muscle", "a response to a change"], "A hot stove or a loud noise is a stimulus."),
    ("Which system sends fast electrical messages along neurons?", "the nervous system", ["the endocrine system", "the digestive system", "the skeletal system"], "Nerve impulses take milliseconds."),
    ("Which system sends chemical messages (hormones) in the blood?", "the endocrine system", ["the nervous system", "the respiratory system", "the muscular system"], "Hormones are slower but last longer."),
    ("Which is faster: a nerve response or a hormone response?", "a nerve response", ["a hormone response", "they are always the same", "neither responds"], "Nerves carry electrical impulses."),
    ("What is homeostasis?", "keeping conditions inside the body, such as temperature, steady", ["changing body temperature on purpose", "growing taller", "digesting food"], "Body temperature stays near 37 °C."),
    ("What does negative feedback do?", "reverses a change to bring a condition back to normal", ["makes a change bigger", "stops the body working", "only happens when you are sick"], "Negative does not mean bad."),
    ("Which hormone lowers blood glucose?", "insulin", ["glucagon", "adrenaline", "oestrogen"], "Insulin is made by the pancreas."),
    ("In type 1 diabetes, what does the pancreas fail to make?", "insulin", ["glucagon", "blood", "bile"], "People with type 1 diabetes inject insulin or use a pump."),
    ("Why is a reflex so fast?", "the impulse goes through the spinal cord without waiting for the brain to decide", ["it uses hormones", "it goes to the brain twice", "it uses the blood"], "Reflexes protect the body."),
    ("Which hormone gets the body ready for 'fight or flight'?", "adrenaline", ["insulin", "growth hormone", "thyroxine"], "It raises heart rate and breathing rate."),
    ("A cricket player at the Adelaide Oval sweats on a 40 °C day. How does sweating help?", "Sweat evaporates and takes heat away from the skin.", ["Sweat warms the body.", "Sweat adds water to the blood.", "Sweat stops the heart."], "Evaporation cools the body."),
    ("What happens to blood vessels near the skin when you are too hot?", "They widen so more heat is lost (vasodilation).", ["They narrow to keep heat in.", "They disappear.", "They fill with sweat."], "Red, flushed skin shows this."),
])
POOL5 = pool(R, [
    ("Mia measures reaction times by catching a dropped ruler: 18, 15, 13 and 12 cm on four tries. What pattern does she see?", "Her reaction time improves with practice.", ["Her reactions get slower.", "There is no pattern.", "The ruler gets heavier."], "A shorter catch distance means a faster reaction."),
    ("Jack tests whether music affects reaction time. Which variable should he keep the same?", "the person, the ruler and the drop height", ["the type of music", "the reaction time", "nothing"], "Only the music should change."),
    ("A graph shows blood glucose rising after breakfast and falling back within 2 hours. Which hormone causes the fall?", "insulin", ["glucagon", "adrenaline", "no hormone"], "Insulin helps cells take in glucose."),
    ("Ruby records a runner's body temperature: 37.0 °C, 38.2 °C after the race, 37.1 °C after 20 minutes rest. What does this show?", "Negative feedback returned the temperature to normal.", ["The runner has a fever.", "Temperature never changes.", "Positive feedback made it hotter."], "Sweating and vasodilation cooled the runner."),
    ("Kai says, 'Hormones work faster than nerves.' Which evidence shows he is wrong?", "Pulling your hand from a hot pan takes a fraction of a second, but growth hormone acts over years.", ["Insulin works in milliseconds.", "Nerves are in the blood.", "Hormones are electrical."], "Nerves are fast; hormones are slower and longer lasting."),
    ("Noah tests his reaction time with his right hand (writing hand) and left hand: 0.21 s and 0.27 s. What could he conclude?", "His writing hand reacts faster, perhaps because of practice.", ["Both hands are the same.", "His left hand is faster.", "Reaction time cannot be measured."], "Repeat with more people to check."),
    ("Zara drinks 1 L of water and collects her urine each hour. What pattern would she expect?", "more urine for a few hours, then back to normal", ["no urine at all", "less urine than usual", "urine stops for a day"], "The kidneys remove extra water by negative feedback."),
    ("A surf lifesaver on Bondi Beach has hot, red skin on a summer day. Which two responses are cooling him?", "sweating and widening of skin blood vessels", ["shivering and goosebumps", "narrowing of skin blood vessels", "making more glucagon"], "Both release heat from the body."),
    ("Liam measures pulse rate before and after exercise. Why should he take readings until it is steady again?", "to see how long negative feedback takes to return it to normal", ["to make the test longer", "because pulse never changes", "to change the variable"], "Recovery time shows fitness."),
    ("Ella investigates how many touch receptors are in different skin areas using two pins. Which area will feel two points when they are closest together?", "the fingertips", ["the back", "the elbow", "the thigh"], "Fingertips have many receptors."),
])


def main():
    sets = U.sets([
        ("Stimulus and response", [(POOL1, 5), (n_rec, 5), (n_path, 4), (s_act, 3), (n_b1, 3)]),
        ("The nervous system and reflexes", [(s_neu, 6), (k_arc, 6), (k_react, 4), (POOL1, 2), (s_acc, 2)]),
        ("Hormones", [(k_gland, 7), (s_nvh, 6), (k_b1, 4), (POOL1, 3)]),
        ("Homeostasis and negative feedback", [(s_skin, 5), (b_loop, 5), (s_glu, 5), (k_react, 2), (b_b1, 3)]),
        ("Investigations", [(POOL5, 10), (k_b5, 3), (b_b5, 4), (k_react, 2), (s_glu, 1), (POOL1, 1)]),
    ])
    make_au(YEAR, "nervous-and-endocrine-systems", SORT, "AC9S9U01", "Biological sciences",
            "Compare the role of body systems in regulating and coordinating the body's response to a stimulus, and describe the "
            "operation of a negative feedback mechanism (summary of the Australian Curriculum v9.0 Science content description).",
            "Nervous and Endocrine Systems", "Nervous and endocrine",
            "Free Year 9 science worksheets on the nervous and endocrine systems: stimulus and response, neurons and reflex arcs, "
            "hormones, homeostasis and negative feedback for temperature and blood glucose. 100 questions with answers.",
            "Nerves are fast; hormones last longer.", "Negative feedback reverses a change to keep the body's conditions steady.",
            "<p><b>Two systems coordinate the body's response to a stimulus.</b></p><ul>"
            "<li>Nervous system: receptor → sensory neuron → spinal cord or brain → motor neuron → effector. Fast and short.</li>"
            "<li>Endocrine system: glands release hormones into the blood. Slower but longer lasting (insulin, adrenaline).</li>"
            "<li>Homeostasis uses negative feedback: a change is detected and reversed, such as sweating when too hot.</li></ul>",
            [("Hand touches a hot pan. Order?", ["receptor in skin", "sensory neuron", "spinal cord", "motor neuron", "muscle"], "a reflex arc"),
             ("Blood glucose rises after lunch. Response?", ["pancreas releases insulin"], "glucose falls back to normal")],
            ["Thinking hormones act faster than nerves.", "Thinking a reflex goes to the brain to decide first.",
             "Thinking 'negative feedback' means something bad happens."],
            [("What is the difference between the nervous and endocrine systems?", "The nervous system uses electrical impulses along neurons for fast, short responses. The endocrine system uses hormones in the blood for slower, longer lasting responses."),
             ("What is negative feedback?", "It is a control system that reverses a change. If body temperature rises, the body sweats and widens skin blood vessels to bring it back to about 37 °C."),
             ("Why are reflexes important?", "Reflexes are fast, automatic responses that protect the body, such as blinking or pulling away from something hot.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
