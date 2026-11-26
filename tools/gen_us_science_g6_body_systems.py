# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Body Systems (MS-LS1-3)
  python tools/gen_us_science_g6_body_systems.py
The body is a system of interacting subsystems made of groups of cells: cells -> tissues -> organs ->
organ systems -> organism. Circulatory, respiratory, digestive, nervous, muscular, skeletal and excretory
systems and how they work together (exercise, eating, responding).
Assessment boundary: the function of the systems and their interactions, not the mechanism of one system.
Wrong answers come from real mistakes: "systems work alone", "the heart is part of the respiratory system",
"a tissue is bigger than an organ".
"""
from sci_common import Unit, item, bank, lesson, make, People

U = Unit(60103)
R = U.R
P = People(R)

SYS = {"circulatory": (["heart", "blood vessels", "blood"], "moves blood that carries oxygen and nutrients to every cell"),
       "respiratory": (["lungs", "trachea (windpipe)", "diaphragm"], "takes in oxygen and gets rid of carbon dioxide"),
       "digestive": (["stomach", "small intestine", "esophagus"], "breaks food down into nutrients the body can use"),
       "nervous": (["brain", "spinal cord", "nerves"], "collects information and sends messages that control the body"),
       "muscular": (["skeletal muscles", "biceps", "tendons"], "moves the body by pulling on bones"),
       "skeletal": (["bones", "skull", "ribs"], "supports the body and protects organs"),
       "excretory": (["kidneys", "bladder", "skin (sweat)"], "removes wastes from the body")}


def g_organ():
    k = R.choice(sorted(SYS))
    o = R.choice(SYS[k][0])
    clash = {"muscular": ["skeletal"], "skeletal": ["muscular"]}
    w = [x for x in SYS if x != k and x not in clash.get(k, [])]
    p = P.next()
    return item("%s is studying the %s. Which organ system is this body part in?" % (p[0], o), "the %s system" % k, ["the %s system" % x for x in R.sample(w, 3)],
                "The %s is part of the %s system, which %s." % (o, k, SYS[k][1]))


def g_job():
    k = R.choice(sorted(SYS))
    w = [SYS[x][1] for x in SYS if x != k]
    if R.random() < 0.5:
        return item("%s asks: what is the main job of the %s system?" % (P.next()[0], k), "It " + SYS[k][1] + ".",
                    ["It " + x + "." for x in R.sample(w, 3)], "The %s system %s." % (k, SYS[k][1]))
    return item("%s reads about a body system that %s. Which system is it?" % (P.next()[0], SYS[k][1]), "the %s system" % k,
                ["the %s system" % x for x in R.sample([y for y in SYS if y != k], 3)], "The %s system %s." % (k, SYS[k][1]))


LEVELS = ["cell", "tissue", "organ", "organ system", "organism"]
EX = {"cell": ["a muscle cell", "a nerve cell", "a red blood cell", "a skin cell"], "tissue": ["muscle tissue", "nerve tissue", "bone tissue", "skin tissue"],
      "organ": ["the heart", "the stomach", "a lung", "the brain", "a kidney"], "organ system": ["the digestive system", "the circulatory system", "the nervous system", "the respiratory system"],
      "organism": ["a person", "a dog", "a frog", "a horse"]}


def g_level():
    k = R.choice(["which", "order", "next"])
    if k == "which":
        lv = R.choice(LEVELS)
        x = R.choice(EX[lv])
        return item("%s is an example of which level of organization?" % (x[0].upper() + x[1:]), "a " + lv if lv[0] not in "aeiou" else "an " + lv,
                    [("an " if y[0] in "aeiou" else "a ") + y for y in LEVELS if y != lv][:3] if lv != "organism" else ["a cell", "a tissue", "an organ system"],
                    "Levels: cell → tissue → organ → organ system → organism.")
    if k == "order":
        return item("Which list goes from smallest to largest?", "cell, tissue, organ, organ system, organism",
                    ["tissue, cell, organ, organism, organ system", "organ, tissue, cell, organism, organ system", "cell, organ, tissue, organ system, organism"],
                    "Groups of cells form tissues, tissues form organs, organs form systems, and systems form the organism.")
    i = R.randrange(4)
    return item("A group of %ss working together forms %s. What fills the blank?" % (LEVELS[i], "a(n) ____"), "an " + LEVELS[i + 1] if LEVELS[i + 1][0] in "aeiou" else "a " + LEVELS[i + 1],
                [("an " if y[0] in "aeiou" else "a ") + y for y in LEVELS if y not in (LEVELS[i], LEVELS[i + 1])][:3],
                "%ss → %s." % (LEVELS[i].capitalize(), LEVELS[i + 1]))


INTER = [("You run a race and breathe hard.", ["respiratory", "circulatory"], "The lungs take in more oxygen, and the heart pumps faster to carry it to the muscles."),
         ("You eat lunch and later have energy to play.", ["digestive", "circulatory"], "The digestive system breaks food into nutrients, and the blood carries them to cells."),
         ("You touch a hot pan and pull your hand back.", ["nervous", "muscular"], "Nerves send a message to the brain, and muscles move the hand."),
         ("You lift a heavy backpack.", ["muscular", "skeletal"], "Muscles pull on bones to lift the bag."),
         ("You drink lots of water and later use the bathroom.", ["excretory", "circulatory"], "The kidneys filter wastes and extra water out of the blood."),
         ("You catch a ball thrown to you.", ["nervous", "muscular"], "The eyes and brain track the ball, and muscles move your hands."),
         ("You exercise and start to sweat.", ["excretory", "circulatory"], "Blood carries heat to the skin, and sweat helps cool you."),
         ("You climb stairs quickly.", ["muscular", "respiratory"], "Leg muscles work hard and need more oxygen from the lungs.")]


def g_inter():
    s, ks, why = R.choice(INTER)
    a = "the %s and %s systems" % tuple(ks)
    others = [("the %s and %s systems" % (x, y)) for x in SYS for y in SYS if x < y and {x, y} != set(ks) and not ({x, y} & set(ks))]
    p = P.next()
    return item("%s writes in a health journal: “%s” Which two body systems work together most here?" % (p[0], s), a, R.sample(others, 3), why)


B1 = bank([
    ("Why do body systems need to work together?", "Each system does a job that other systems depend on.", ["They never work together.", "Only the brain does any work.", "Systems compete with each other."],
     "For example, muscles need oxygen from the respiratory system and blood from the circulatory system."),
    ("What is a tissue?", "a group of similar cells working together", ["a single cell", "a group of organs", "a whole organism"], "Muscle tissue is many muscle cells."),
    ("What is an organ?", "a structure made of different tissues that work together", ["one cell", "a group of organisms", "a kind of blood"], "The heart is made of muscle, nerve and other tissues."),
    ("Which system brings oxygen into the body?", "the respiratory system", ["the digestive system", "the skeletal system", "the excretory system"], "The lungs take in oxygen."),
    ("Which two systems work together to deliver oxygen to cells?", "respiratory and circulatory", ["skeletal and digestive", "excretory and skeletal", "nervous and skeletal"],
     "Lungs take in oxygen; blood carries it."),
    ("Why does your heart beat faster when you exercise?", "Your muscles need more oxygen and nutrients, so blood must move faster.", ["Your heart gets bored.", "Your bones need blood.", "Your stomach is full."],
     "The circulatory system responds to the muscles' needs."),
    ("Which system controls and coordinates the other systems?", "the nervous system", ["the skeletal system", "the digestive system", "the excretory system"],
     "The brain and nerves send signals."),
    ("What happens to food in the digestive system?", "It is broken down into nutrients that pass into the blood.", ["It turns into bones.", "It goes straight to the brain.", "It stays the same."],
     "Nutrients are absorbed in the small intestine."),
])
B5 = bank([
    ("Ava measures her pulse at rest (70 beats per minute) and after jumping jacks (120 beats per minute). What does this show?", "The circulatory system responds to exercise.", ["Exercise slows the heart.", "Pulse never changes.", "The digestive system controls the heart."],
     "The heart beats faster to deliver more oxygen."),
    ("Leo counts 14 breaths per minute at rest and 30 after running. Which two systems explain the change?", "respiratory and muscular", ["skeletal and excretory", "digestive and skeletal", "excretory and nervous"],
     "Working muscles need more oxygen."),
    ("If the spinal cord is badly injured, why might a person not be able to move their legs?", "Messages from the brain cannot reach the leg muscles.", ["The legs have no bones.", "The heart stops.", "The stomach stops working."],
     "The nervous and muscular systems work together."),
    ("Mia models the body as a city. The roads that carry deliveries are most like which system?", "the circulatory system", ["the skeletal system", "the nervous system", "the excretory system"],
     "Blood vessels carry materials around the body."),
    ("A student has a fever and is breathing fast. Which statement is best supported?", "Body systems interact, so a problem in one can affect others.", ["Only one system is ever affected.", "Fevers affect only the skin.", "Breathing is not related to health."],
     "The body works as a whole system."),
])


def body():
    think = ("<p>The body is organized in levels: <b>cells → tissues → organs → organ systems → organism</b>.</p><ul>"
             + "".join("<li><b>%s system</b> (%s): %s.</li>" % (k.capitalize(), ", ".join(v[0]), v[1]) for k, v in SYS.items()) + "</ul>"
             "<p>Systems <b>work together</b>. When you exercise, the nervous system signals the muscles, the lungs take in more oxygen, and the heart pumps faster to deliver it.</p>")
    ex = [("Is the stomach a tissue, an organ or a system?", ["It is made of several tissues."], "an organ"),
          ("Which systems work together when you run?", ["Muscles move.", "Lungs and heart supply oxygen."], "muscular, respiratory and circulatory")]
    mist = ["Thinking each system works alone.",
            "Mixing up the order of levels: a tissue is smaller than an organ.",
            "Putting the heart in the respiratory system. It is in the circulatory system."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Levels of organization", B1 + [(g_level, 6), (g_job, 6)]),
        ("Organs and systems", [(g_organ, 12), (g_level, 8)]),
        ("What each system does", [(g_job, 14), (g_organ, 6)]),
        ("Systems working together", [(g_inter, 14), (g_job, 6)]),
        ("Investigating the body", B5 + [g_inter, g_organ, g_level, g_job]),
    ])
    make("grade-6", "body-systems", 3, "MS-LS1-3",
         "Use argument supported by evidence for how the body is a system of interacting subsystems composed of groups of cells.",
         "Body Systems",
         "Grade 6 Body Systems Worksheets: Cells, Tissues, Organs and How Systems Work Together",
         "Body Systems",
         "Free middle school science worksheets on body systems (NGSS MS-LS1-3): cells, tissues, organs and organ systems, the circulatory, respiratory, digestive and nervous systems, and how systems interact. 100 practice questions with answers.",
         "Body systems work together.",
         "Cells form tissues, tissues form organs, and organs form systems. Systems like the heart and lungs interact to keep you alive.",
         body(),
         [("What are the levels of organization in the body?", "Cells form tissues, tissues form organs, organs form organ systems, and organ systems make up the organism."),
          ("How do the respiratory and circulatory systems work together?", "The lungs take in oxygen, and the heart pumps blood that carries the oxygen to every cell."),
          ("What happens to body systems during exercise?", "The muscles work harder, the nervous system coordinates them, and the heart and lungs speed up to deliver more oxygen.")],
         sets)


if __name__ == "__main__":
    main()
