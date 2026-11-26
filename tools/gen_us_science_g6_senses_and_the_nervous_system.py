# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Senses and the Nervous System (MS-LS1-8)
  python tools/gen_us_science_g6_senses_and_the_nervous_system.py
Sensory receptors respond to stimuli by sending messages along nerves (neurons) to the brain, which
processes them for immediate behavior or stores them as memories. Stimulus, receptor, sensory neuron,
brain/spinal cord, motor neuron, response. Reflexes go through the spinal cord. Reaction-time data.
Assessment boundary: no mechanisms of how the brain stores information.
Wrong answers come from real mistakes: "receptors decide the response", "messages go from the muscles to
the brain to make you move", "a reflex goes through the brain first".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(60104)
R = U.R
P = People(R)

REC = [("light", "eyes", "receptors in the eyes"), ("sound", "ears", "receptors in the ears"), ("chemicals in the air", "nose", "receptors in the nose"),
       ("chemicals in food", "tongue", "taste buds on the tongue"), ("pressure and touch", "skin", "receptors in the skin"), ("heat and cold", "skin", "receptors in the skin"),
       ("pain from a scrape", "skin", "receptors in the skin"), ("balance and head motion", "inner ear", "receptors in the inner ear"), ("colors", "eyes", "receptors in the eyes"),
       ("the pitch of a song", "ears", "receptors in the ears"), ("sweet and salty tastes", "tongue", "taste buds on the tongue"), ("the smell of perfume", "nose", "receptors in the nose")]
STIM = [("the smell of smoke", "nose", "leaves the building"), ("a flash of lightning", "eyes", "goes indoors"), ("a car horn", "ears", "steps back onto the curb"),
        ("sour milk", "tongue", "spits it out"), ("a fire alarm", "ears", "walks outside"), ("a friend calling", "ears", "turns around"),
        ("a red stop sign", "eyes", "stops the bike"), ("a cold wind", "skin", "zips up a coat"), ("the smell of bread baking", "nose", "walks to the kitchen"),
        ("a ball flying toward the face", "eyes", "ducks"), ("a buzzing bee", "ears", "moves away"), ("a wet, slippery floor", "eyes", "walks slowly")]


def cap(s):
    return s[0].upper() + s[1:]


def g_rec():
    st, org, rec = R.choice(REC)
    p = P.next()
    w = sorted({r for s_, o, r in REC if o != org})
    return item("%s is learning about receptors. Which receptors respond to %s?" % (p[0], st), rec, R.sample(w, 3),
                "%s respond to %s and send messages to the brain." % (cap(rec), st))


def g_path():
    st, org, rsp = R.choice(STIM)
    p = P.next()
    k = R.choice(["order", "stimulus", "response", "which"])
    if k == "order":
        return item("%s notices %s and %s. Which shows the path of the message in order?" % (p[0], st, rsp),
                    "receptors → sensory nerves → brain → motor nerves → muscles",
                    ["muscles → motor nerves → brain → sensory nerves → receptors", "brain → receptors → muscles → nerves", "receptors → muscles → brain → nerves"],
                    "Stimulus → receptor → sensory neuron → brain → motor neuron → muscle (response).")
    if k == "stimulus":
        return item("%s notices %s and %s. What is the stimulus?" % (p[0], st, rsp), st, [rsp, "the brain", "the " + org],
                    "The stimulus is the information from the environment that the receptors detect.")
    if k == "response":
        return item("%s notices %s and %s. What is the response?" % (p[0], st, rsp), rsp, [st, "the brain", "the " + org],
                    "The response is what the body does after the brain processes the information.")
    return item("%s notices %s and %s. Which part of the body decides how to respond?" % (p[0], st, rsp), "the brain",
                ["the " + org, "the muscles", "the receptors"], "Receptors detect; the brain processes and decides; muscles carry out the response.")


def g_react():
    trials = [R.randint(18, 30) for _ in range(3)]
    after = [t - R.randint(3, 7) for t in trials]
    rows = [["Trial %d" % (i + 1), "%d cm" % a, "%d cm" % b] for i, (a, b) in enumerate(zip(trials, after))]
    p = P.next()
    tab = table(["", "Ruler drop distance (first day)", "Ruler drop distance (after a week of practice)"], rows)
    k = R.choice(["avg", "change", "why"])
    if k == "avg":
        s = sum(trials)
        if s % 3:
            return None
        return item(tab + "%s caught a falling ruler. A shorter distance means a faster reaction. What was the average distance on the first day?" % p[0], "%d cm" % (s // 3),
                    ["%d cm" % s, "%d cm" % max(trials), "%d cm" % min(trials)], "(%d + %d + %d) ÷ 3 = %d cm." % (trials[0], trials[1], trials[2], s // 3))
    if k == "change":
        return item(tab + "What does %s's data show about practice?" % p[0], "Reaction time got faster after practice.",
                    ["Reaction time got slower after practice.", "Practice did not change reaction time.", "The ruler fell faster after practice."],
                    "Shorter catch distances mean faster reactions.")
    return item(tab + "Why did %s react faster after a week of practice?" % p[0], "The brain stored memories that helped it respond faster.",
                ["The ruler got lighter.", "The eyes grew bigger.", "The muscles stopped needing messages."], "Memories can make responses faster and more accurate.")


B1 = bank([
    ("What is a stimulus?", "information from the environment that causes a response, like light or sound", ["a body's response", "a kind of muscle", "a memory"],
     "Stimuli are detected by receptors."),
    ("What do sensory receptors do?", "detect stimuli and send messages to the brain", ["decide how to respond", "move the muscles", "store memories"],
     "Receptors are in the eyes, ears, nose, tongue and skin."),
    ("What carries messages through the nervous system?", "nerve cells (neurons)", ["red blood cells", "bones", "fat cells"], "Neurons carry electrical signals."),
    ("Which two parts make up the central nervous system?", "the brain and the spinal cord", ["the heart and lungs", "the eyes and ears", "the skin and muscles"],
     "Nerves branch out from the spinal cord to the whole body."),
    ("What is a reflex?", "a fast, automatic response that does not wait for the brain to decide", ["a slow, careful decision", "a memory", "a kind of sense organ"],
     "Pulling away from a hot stove is a reflex through the spinal cord."),
    ("Why is a reflex useful?", "It protects the body by responding very quickly.", ["It helps you remember.", "It slows the body down.", "It makes you think longer."],
     "Speed prevents injury."),
    ("What can the brain do with information besides responding right away?", "store it as a memory", ["send it back to the eyes", "turn it into blood", "nothing"],
     "Memories guide later behavior."),
    ("Which nerves carry messages from the brain to the muscles?", "motor nerves", ["sensory nerves", "taste buds", "blood vessels"], "Sensory nerves bring messages in; motor nerves send them out."),
])
B5 = bank([
    ("Ava tests reaction time with sound (a clap) and with sight (a light). How can she make it a fair test?", "use the same people, the same number of trials and change only the type of stimulus", ["change the people each time", "use one trial only", "change everything"],
     "Only one variable should change."),
    ("Leo's average ruler drop was 20 cm with his writing hand and 25 cm with his other hand. What can he conclude?", "He reacts faster with his writing hand.", ["He reacts faster with his other hand.", "Hands do not matter.", "The ruler was heavier the second time."],
     "Shorter distance means faster reaction."),
    ("A doctor taps below a patient's knee and the leg kicks. What is this?", "a reflex", ["a memory", "a decision", "a sense of smell"], "The knee-jerk reflex goes through the spinal cord."),
    ("Why does a person who has been stung by a bee jump away from a buzzing sound later?", "The brain stored a memory of the sting and uses it to respond.", ["The ear is afraid.", "Bees control people.", "It is a new reflex every time."],
     "Memory guides behavior."),
    ("Mia covers one eye and tries to touch two pencil tips together. It is harder. Why?", "The brain uses information from both eyes to judge distance.", ["One eye stops working.", "Pencils are too thin.", "Hands need both eyes to move."],
     "The brain combines information from receptors."),
])


def body():
    think = ("<p>The nervous system lets you sense and respond to the world.</p>"
             "<p><b>Stimulus</b> (light, sound, heat) → <b>receptors</b> (in eyes, ears, nose, tongue, skin) → <b>sensory nerves</b> → <b>brain and spinal cord</b> (process the information) → <b>motor nerves</b> → <b>muscles</b> (the <b>response</b>).</p>"
             "<p>Some information is stored as <b>memories</b> that guide later behavior. A <b>reflex</b>, like pulling away from a hot stove, is very fast because the spinal cord responds before the brain thinks about it.</p>")
    ex = [("You hear a car horn and step back. Stimulus? Response?", ["The horn is the stimulus.", "Stepping back is the response."], "horn; stepping back"),
          ("What decides how to respond?", ["Receptors detect; muscles act."], "the brain")]
    mist = ["Thinking receptors decide the response. The brain decides.",
            "Mixing up the stimulus and the response.",
            "Reversing the path: messages go from receptors to the brain, then to muscles."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stimulus and response", B1 + [(g_path, 6), (g_rec, 6)]),
        ("Receptors", [(g_rec, 12), (g_path, 8)]),
        ("The path of a message", [(g_path, 16), (g_rec, 4)]),
        ("Reaction time data", [(g_react, 14), (g_path, 6)]),
        ("Investigations and memory", B5 + [g_react, g_path, g_rec]),
    ])
    make("grade-6", "senses-and-the-nervous-system", 4, "MS-LS1-8",
         "Gather and synthesize information that sensory receptors respond to stimuli by sending messages to the brain for immediate behavior or storage as memories.",
         "Senses and the Nervous System",
         "Grade 6 Nervous System Worksheets: Stimulus, Receptors, Brain and Response",
         "Senses and the Nervous System",
         "Free middle school science worksheets on the nervous system (NGSS MS-LS1-8): stimuli and sensory receptors, nerves, the brain and spinal cord, reflexes, memory and reaction-time data. 100 practice questions with answers.",
         "Receptors sense; the brain decides; muscles respond.",
         "Messages travel from receptors along nerves to the brain, which sends signals to the muscles or stores memories.",
         body(),
         [("How does the nervous system work?", "Receptors detect a stimulus, sensory nerves carry the message to the brain, the brain processes it, and motor nerves tell the muscles how to respond."),
          ("What is a reflex?", "A reflex is a fast, automatic response, like pulling your hand from a hot stove, that is handled by the spinal cord."),
          ("How do memories help us?", "The brain stores information from past experiences, which helps us respond faster and better next time.")],
         sets)


if __name__ == "__main__":
    main()
