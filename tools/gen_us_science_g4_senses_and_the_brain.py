# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Senses and the Brain (4-LS1-2)
  python tools/gen_us_science_g4_senses_and_the_brain.py
Animals receive different kinds of information through their senses, process it in the brain,
and respond in different ways. Model: information (stimulus) -> sense receptor -> nerves -> brain -> response.
Some information is stored as memories that guide later actions.
Assessment boundary: no mechanisms of how the brain stores or recalls information.
Wrong answers come from real mistakes: "the eyes decide what to do", "the response comes before
the brain gets the message", "we see with our ears".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, text, arrow, People, INK, BLUE

U = Unit(40111)
R = U.R
P = People(R)

SENSE = {"sight": "eyes", "hearing": "ears", "smell": "nose", "taste": "tongue", "touch": "skin"}
# (information, sense, response)
STIM = [("sees a car coming", "sight", "stops at the curb"), ("hears the school bell", "hearing", "walks to class"),
        ("smells smoke", "smell", "tells an adult"), ("tastes sour milk", "taste", "spits it out"),
        ("touches a hot pan", "touch", "pulls {pos} hand away"), ("sees a red traffic light", "sight", "waits to cross"),
        ("hears a dog growl", "hearing", "backs away slowly"), ("smells cookies baking", "smell", "walks to the kitchen"),
        ("tastes too much salt in soup", "taste", "adds water to the soup"), ("feels a mosquito bite", "touch", "brushes it away"),
        ("sees a ball flying at {pos} face", "sight", "ducks"), ("hears thunder", "hearing", "goes inside"),
        ("smells something burning in the oven", "smell", "turns the oven off"), ("feels cold wind", "touch", "zips up a jacket"),
        ("tastes a bitter berry", "taste", "stops eating it"), ("hears a friend call {pos} name", "hearing", "turns around"),
        ("sees a friend wave", "sight", "waves back"), ("feels a sharp rock under {pos} foot", "touch", "steps off it")]
STEPS = ["information", "sense organ", "brain", "response"]


def model_svg(labels, label="information goes to a sense organ, then to the brain, then to a response"):
    W = 4 * 120 + 10
    s = []
    for i, t in enumerate(labels):
        x = 10 + i * 120
        s.append(rect(x, 15, 96, 44, "#eef4fb", BLUE, 2, 6) + text(x + 48, 42, t, 13))
        if i < len(labels) - 1:
            s.append(arrow(x + 98, 37, x + 118, 37, INK, 2, 8))
    return svg_wrap(W, 74, "".join(s), label)


def pick():
    st, sense, rsp = R.choice(STIM)
    p = P.next()
    return st.format(pos=p[2]), sense, rsp.format(pos=p[2]), p


def g_organ():
    st, sense, rsp, p = pick()
    org = SENSE[sense]
    w = [v for v in SENSE.values() if v != org]
    return item("%s %s. Which sense organ takes in this information?" % (p[0], st), "the " + org,
                ["the " + x for x in R.sample(w, 3)], "This information is taken in by the %s (%s)." % (org, sense))


def g_brain():
    st, sense, rsp, p = pick()
    org = SENSE[sense]
    k = R.choice(["where", "next", "first", "resp"])
    if k == "where":
        return item("%s %s and %s. Where is the information processed before %s responds?" % (p[0], st, rsp, p[1]), "in the brain",
                    ["in the " + org, "in the stomach", "in the feet"], "Sense organs send messages along nerves to the brain, which decides how to respond.")
    if k == "next":
        return item("%s %s. Nerves in %s %s send a message. Where does the message go next?" % (p[0], st, p[2], org),
                    "to the brain", ["straight to the muscles without going to the brain", "back out of the body", "to the heart to be pumped"],
                    "Messages from sense organs travel to the brain to be processed.")
    if k == "resp":
        return item("%s %s and %s. Which part is the response?" % (p[0], st, rsp), "%s %s" % (p[1], rsp),
                    ["%s %s" % (p[1], st), "%s %s" % (p[2], org), "%s brain" % p[2]], "The response is what %s does after the brain processes the information." % p[0])
    return item("%s %s and then %s. What happened first?" % (p[0], st, rsp), "%s %s took in information." % (cap_(p[2]), org),
                ["%s %s." % (p[0], rsp), "%s brain told %s muscles to move." % (cap_(p[2]), p[2]), "%s brain processed the information." % cap_(p[2])],
                "First the senses take in information. Then the brain processes it. Last comes the response.")


def cap_(x):
    return x[0].upper() + x[1:]


def g_order():
    st, sense, rsp, p = pick()
    org = SENSE[sense]
    steps = ["%s %s %s in the information" % (cap_(p[2]), org, "take" if org in ("eyes", "ears") else "takes"),
             "A message travels along nerves to the brain", "The brain processes the message", "%s %s" % (p[0], rsp)]
    order = list(range(4))
    R.shuffle(order)
    lines = "<br>".join("%s. %s" % ("WXYZ"[i], steps[j]) for i, j in enumerate(order))
    ans = "".join("WXYZ"[order.index(j)] for j in range(4))
    wrong = set()
    for _ in range(40):
        x = list(ans)
        R.shuffle(x)
        wrong.add("".join(x))
    wrong.discard(ans)
    rev = ans[::-1]
    wl = R.sample(sorted(wrong - {rev}), 2) + [rev]
    return item("%s %s. Put the steps in order:<br>%s" % (p[0], st, lines), ", ".join(ans), [", ".join(w) for w in wl],
                "Information → sense organ → nerves to the brain → brain processes → response.")


def g_model():
    blanks = list(STEPS)
    i = R.choice([1, 2, 3])
    shown = [b if j != i else "?" for j, b in enumerate(blanks)]
    w = [x for x in ["muscles only", "the heart", "the stomach", "the information", "a sense organ", "the brain", "a response"] if x.replace("a ", "").replace("the ", "") != blanks[i]]
    ans = {"sense organ": "a sense organ", "brain": "the brain", "response": "a response"}[blanks[i]]
    w = [x for x in w if x != ans]
    return item(fig(model_svg(shown, "a model with one box missing")) + "What belongs in the box with the question mark?", ans, R.sample([x for x in w if x not in ("the information",)], 3),
                "The model is: information → sense organ → brain → response.")


ANIMAL = [("A bat", "hears echoes of its own calls", "find insects in the dark"), ("A snake", "senses the heat of a mouse's body", "find prey at night"),
          ("A dog", "smells a trail on the ground", "follow a lost hiker"), ("A cat", "feels air move against its whiskers", "move through tight spaces in the dark"),
          ("A shark", "smells a tiny amount of blood in the water", "find food far away"), ("An owl", "hears a mouse moving under the snow", "catch it"),
          ("A deer", "hears a twig snap", "run away from danger"), ("A bee", "sees colors on flowers", "find nectar"),
          ("A catfish", "tastes the water with its whiskers", "find food in muddy water"), ("An eagle", "sees a fish from high in the sky", "dive and catch it")]


def g_animal():
    an, sense_info, use = R.choice(ANIMAL)
    k = R.choice(["why", "brain"])
    if k == "why":
        others = [a[2] for a in ANIMAL if a[2] != use]
        return item("%s %s. How does this information help it?" % (an, sense_info), "It helps it %s." % use, ["It helps it %s." % x for x in R.sample(others, 3)],
                    "Animals use information from their senses to survive.")
    return item("%s %s. What does its brain do with this information?" % (an, sense_info), "processes it and tells the body how to respond",
                ["nothing; the senses move the body by themselves", "stores it in the stomach", "sends it back out of the body"],
                "The brain processes information from the senses and sends signals to the muscles.")


B1 = bank([
    ("What are the five senses?", "sight, hearing, smell, taste and touch", ["sight, sleep, smell, taste and talk", "hearing, running, eating, sleeping and seeing", "heart, lungs, brain, stomach and skin"],
     "Each sense takes in a different kind of information."),
    ("What carries messages from the senses to the brain?", "nerves", ["bones", "blood only", "muscles"], "Nerves carry messages quickly through the body."),
    ("What does the brain do with information from the senses?", "It processes the information and decides how to respond.", ["It throws the information away.", "It stores all of it in the eyes.", "It turns it into food."],
     "The brain is the control center."),
    ("Which sense organ is the largest?", "the skin", ["the eyes", "the nose", "the tongue"], "The skin covers your whole body and senses touch, heat, cold and pain."),
    ("What is a memory?", "information stored in the brain that can guide later actions", ["a sense organ", "a kind of nerve", "a muscle"],
     "If you once touched a hot stove, you remember not to touch it again."),
    ("Why do you pull your hand away from something hot very quickly?", "Nerves send the message fast so you can move before you get badly hurt.", ["Your hand thinks for itself.", "Heat pushes your hand away.", "Your eyes tell your hand to move."],
     "Some responses happen very fast to protect the body."),
    ("Which part of the body tells muscles to move?", "the brain", ["the eyes", "the ears", "the skin"], "The brain sends messages along nerves to the muscles."),
    ("A response is", "what the body does after the brain processes information", ["the information that enters a sense organ", "a kind of sense organ", "a memory"],
     "Running, stopping, turning and talking are responses."),
])
B5 = bank([
    ("Ava drops a ruler between Leo's fingers. He catches it faster after five tries. What helped him improve?", "His brain learned and remembered what to expect.", ["His fingers grew longer.", "The ruler got slower.", "His eyes got bigger."],
     "Practice builds memories that make responses quicker."),
    ("In the ruler-drop test, which sense starts the reaction?", "sight", ["smell", "taste", "hearing only"], "Leo sees the ruler start to fall."),
    ("A dog hears its owner's car and runs to the door. What is the response?", "running to the door", ["hearing the car", "the sound of the car", "the dog's ears"],
     "The response is what the dog does."),
    ("Mia wears a blindfold and identifies fruits by smell. Which sense is she testing?", "smell", ["sight", "hearing", "touch"], "The blindfold blocks sight."),
    ("A baby touches a cactus, says “ouch,” and never touches it again. What does this show?", "Information can be stored as a memory and guide later actions.", ["Babies cannot feel touch.", "The cactus moved away.", "Memories are stored in the hand."],
     "The brain remembered the pain."),
    ("Why is it harder to taste food when you have a stuffy nose?", "Smell and taste work together, and the nose cannot take in smells.", ["The tongue stops working.", "Food has no taste when you are sick.", "The ears are blocked."],
     "The brain uses information from more than one sense at the same time."),
])


def body():
    think = ("<p>Animals take in <b>information</b> with their <b>senses</b>: sight (eyes), hearing (ears), smell (nose), taste (tongue) and touch (skin). "
             "Messages travel along <b>nerves</b> to the <b>brain</b>. The brain processes the information and sends messages to the muscles, and the body <b>responds</b>.</p>"
             + figure(model_svg(["information", "sense organ", "brain", "response"]), "Information → sense organ → brain → response.")
             + "<p>The brain can also store information as <b>memories</b>. Memories help animals respond better next time.</p>")
    ex = [("You smell smoke and tell an adult. What is the response?", ["Smoke is the information.", "The nose takes it in; the brain processes it."], "telling an adult"),
          ("Where are messages from the ears processed?", ["Ears send messages along nerves."], "in the brain")]
    mist = ["Thinking the sense organ decides what to do. The brain decides.",
            "Putting the response before the brain gets the message.",
            "Mixing up the information (a sound) with the sense organ (the ear)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The five senses", B1 + [(g_organ, 8), (g_model, 4)]),
        ("From senses to the brain", [(g_organ, 6), (g_brain, 10), (g_model, 4)]),
        ("Modeling a response", [(g_order, 10), (g_model, 4), (g_brain, 6)]),
        ("How animals use their senses", [(g_animal, 12), (g_order, 4), (g_organ, 4)]),
        ("Investigations and memory", B5 + [g_animal, g_order, g_brain, g_organ]),
    ])
    make("grade-4", "senses-and-the-brain", 11, "4-LS1-2",
         "Use a model to describe that animals receive different types of information through their senses, process the information in their brain, and respond to the information in different ways.",
         "Senses and the Brain",
         "Grade 4 Senses Worksheets: How the Brain Processes Information and Responds",
         "Senses and the Brain",
         "Free Grade 4 science worksheets on senses and the brain (NGSS 4-LS1-2): the five senses, nerves, how the brain processes information, responses, memories and how animals use their senses. 100 practice questions with answers.",
         "Senses take in information; the brain decides how to respond.",
         "Information goes from a sense organ along nerves to the brain. The brain processes it and tells the body how to respond.",
         body(),
         [("How do the senses and the brain work together?", "Sense organs take in information and send messages along nerves to the brain. The brain processes the messages and tells the muscles how to respond."),
          ("What is a response?", "A response is what an animal does after its brain processes information, like running away from a loud noise."),
          ("How do memories help animals?", "Information stored as memories helps animals respond better later, like remembering that a stove is hot.")],
         sets)


if __name__ == "__main__":
    main()
