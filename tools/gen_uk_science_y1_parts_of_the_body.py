# -*- coding: utf-8 -*-
"""
UK Year 1 science: Parts of the Body (Animals, including humans)
  python tools/gen_uk_science_y1_parts_of_the_body.py
Identify, name, draw and label the basic parts of the human body: a labelled picture of a child (head, neck,
shoulder, arm, elbow, hand, tummy, hip, leg, knee, foot), parts of the face, counting body parts, and which part we use
for an action.
Wrong answers come from real mistakes: "the elbow is in the leg", "the knee is in the arm", "we have ten fingers on
one hand", "we hear with our nose".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, fig, People, once
from uk_sci_pics import body as body_svg, BODY_PT

U = Unit(61107)
R = U.R
P = People(R)

PARTS = sorted(BODY_PT)
NM = {"head": "the head", "neck": "the neck", "shoulder": "a shoulder", "arm": "an arm", "elbow": "an elbow", "hand": "a hand", "tummy": "the tummy",
      "hip": "a hip", "leg": "a leg", "knee": "a knee", "foot": "a foot"}


def g_pic():
    ps = R.sample(PARTS, 5)
    lab = dict(zip(ps, R.sample("ABCDE", 5)))
    p = R.choice(ps)
    k = R.random() < 0.5
    if not once(("pc", p, lab[p], k)):
        return None
    pic = fig(body_svg(lab))
    if k:
        return item(pic + "Which letter points to %s?" % NM[p], lab[p], R.sample([lab[x] for x in ps if x != p], 3), "Follow the line from the letter to the body.")
    return item(pic + "Which part of the body is labelled %s?" % lab[p], NM[p], R.sample([NM[x] for x in ps if x != p], 3), "Follow the line from the letter to the body.")


WHERE = [("an elbow", "in the middle of your arm"), ("a knee", "in the middle of your leg"), ("a wrist", "between your arm and your hand"),
         ("an ankle", "between your leg and your foot"), ("a shoulder", "where your arm joins your body"), ("the neck", "between your head and your body"),
         ("a heel", "at the back of your foot"), ("the chin", "at the bottom of your face")]


def g_where():
    p, w = R.choice(WHERE)
    k = R.random() < 0.5
    if not once(("wh", p, k)):
        return None
    if k:
        return item("Where is %s?" % p, w, R.sample([x[1] for x in WHERE if x[1] != w], 3), "Point to each part on your own body.")
    return item("Which body part is %s?" % w, p, R.sample([x[0] for x in WHERE if x[0] != p], 3), "Point to each part on your own body.")


DO = [("kick a ball", "your foot"), ("clap", "your hands"), ("nod", "your head"), ("hop", "one leg"), ("wave", "your hand and arm"), ("chew", "your teeth"),
      ("write your name", "your hand"), ("shrug", "your shoulders"), ("kneel down", "your knees"), ("wiggle your toes", "your feet"), ("smile", "your mouth"),
      ("bend your arm", "your elbow")]


def g_do():
    a, p = R.choice(DO)
    if not once(("do", a)):
        return None
    groups = [{"your hands", "your hand", "your hand and arm", "your elbow"}, {"your foot", "one leg", "your feet", "your knees"}, {"your mouth", "your teeth"}]
    same = next((g for g in groups if p in g), {p})
    return item("Which part of your body do you use to %s?" % a, p, R.sample(sorted({x[1] for x in DO if x[1] not in same}), 3), "We use different parts of the body to move.")


COUNT = [("fingers on one hand (including the thumb)", 5), ("toes on both feet", 10), ("eyes", 2), ("ears", 2), ("noses", 1), ("legs", 2), ("arms", 2),
         ("thumbs", 2), ("fingers and thumbs on both hands", 10), ("knees", 2), ("toes on one foot", 5), ("elbows", 2)]


def g_count():
    t, n = R.choice(COUNT)
    if not once(("co", t)):
        return None
    return item("How many %s does a person usually have?" % t, str(n), [str(x) for x in (1, 2, 4, 5, 10, 20) if x != n][:3], "Count on your own body.")


FACE = [("eyes", "to see"), ("ears", "to hear"), ("nose", "to smell"), ("mouth", "to talk and smile"), ("eyebrows", "to stop sweat running into your eyes"),
        ("teeth", "to bite and chew"), ("tongue", "to taste")]


def g_face():
    p, j = R.choice(FACE)
    k = R.random() < 0.5
    if not once(("fa", p, k)):
        return None
    if k:
        return item("What do we use our %s for?" % p, j, R.sample([x[1] for x in FACE if x[1] != j], 3), "Each part of the face has a job.")
    return item("Which part of the face do we use %s?" % j, "the " + p, R.sample(["the " + x[0] for x in FACE if x[0] != p], 3), "Each part of the face has a job.")


B1 = bank([
    ("Which body part is at the top of your body?", "the head", ["the foot", "the knee", "the hip"], "Your head has your face."),
    ("Which body part joins your head to your body?", "the neck", ["the elbow", "the knee", "the ankle"], "It lets you turn your head."),
    ("Where are your knees?", "in your legs", ["in your arms", "on your head", "in your tummy"], "Knees bend your legs."),
    ("Where are your elbows?", "in your arms", ["in your legs", "on your feet", "on your face"], "Elbows bend your arms."),
    ("What is at the end of your arm?", "a hand", ["a foot", "a knee", "a hip"], "Hands have fingers."),
    ("What is at the end of your leg?", "a foot", ["a hand", "an elbow", "a shoulder"], "Feet have toes."),
    ("Which part of your body has toes?", "your feet", ["your hands", "your head", "your arms"], "Ten toes."),
    ("Do all people have the same body parts?", "Yes, most people have the same parts, but everyone looks different.", ["No, everyone has different parts.", "Only children do.", "Only grown-ups do."], "Same parts, different looks."),
])
B5 = bank([
    ("Why do we have joints such as knees and elbows?", "so our arms and legs can bend", ["so we can see", "to keep us warm", "to help us hear"], "Bending helps us move."),
    ("How could you find out who has the longest arms in your class?", "Measure everyone's arm with a tape measure.", ["Guess.", "Look at their shoes.", "Measure only one person."], "Measure carefully."),
    ("What happens to your body parts as you grow up?", "They get bigger.", ["They get smaller.", "They disappear.", "They swap places."], "Growing."),
    ("Which body part do you use to catch a ball?", "your hands", ["your ears", "your knees", "your nose"], "Hands grip."),
    ("Why should you wear a helmet when you ride a bike?", "to protect your head", ["to keep your feet dry", "to see better", "to hear music"], "Keep your head safe."),
])


def body():
    pic = body_svg({"head": "A", "arm": "B", "hand": "C", "leg": "D", "foot": "E"}, "a child: A head, B arm, C hand, D leg, E foot")
    ex = [("Which part bends in the middle of your leg?", ["It is in your leg"], "the knee"),
          ("How many fingers on one hand?", ["Include the thumb"], "5")]
    mist = ["Thinking the elbow is in the leg.", "Thinking the knee is in the arm.", "Thinking we hear with our nose."]
    return kid_lesson(pic, "We can name the parts of our body.",
                      ["Head, neck, shoulders, arms, hands, tummy, legs and feet.", "Elbows bend our arms; knees bend our legs.", "Our face has eyes, ears, a nose and a mouth."], ex, mist)


def main():
    sets = U.sets([
        ("Naming parts", B1 + [(g_pic, 12)]),
        ("Labelled body", [(g_pic, 14), (g_count, 6)]),
        ("Where is it?", [(g_where, 12), (g_count, 6), (g_pic, 2)]),
        ("Using our body", [(g_do, 12), (g_face, 8)]),
        ("Thinking about our body", B5 + [(g_face, 5), (g_pic, 10)]),
    ])
    make_uk(1, "parts-of-the-body", 7, "Animals, including humans",
            "Identify, name, draw and label the basic parts of the human body.",
            "Parts of the Body",
            "Year 1 Science: Parts of the Body Worksheets (Label the Body)",
            "Parts of the Body",
            "Free Year 1 science worksheets on the parts of the human body: labelling a picture, the face, counting body parts and which part we use for each action. 100 questions with answers.",
            "Head, arms, hands, legs, feet.",
            "Elbows bend our arms; knees bend our legs.",
            body(),
            [("What are the main parts of the body?", "The head, neck, shoulders, arms, elbows, hands, tummy, hips, legs, knees and feet."),
             ("Where are the elbows and knees?", "Elbows are in the middle of our arms. Knees are in the middle of our legs. They let us bend."),
             ("What are the parts of the face?", "Eyes, eyebrows, ears, a nose, a mouth with teeth and a tongue, cheeks and a chin.")],
            sets)


if __name__ == "__main__":
    main()
