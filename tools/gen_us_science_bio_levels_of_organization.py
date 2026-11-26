# -*- coding: utf-8 -*-
"""
US High School Biology: Levels of Organization and Body Systems (HS-LS1-2)
  python tools/gen_us_science_bio_levels_of_organization.py
Develop and use a model to illustrate the hierarchical organization of interacting systems that provide specific
functions within multicellular organisms. Cell -> tissue -> organ -> organ system -> organism; which organ belongs to
which system; how systems work together (exercise, eating, breathing, responding).
Wrong answers come from real mistakes: "a tissue is bigger than an organ", "the heart is in the respiratory system",
"each system works alone".
"""
from sci_common import Unit, item, bank, lesson, make, fig, svg_wrap, arrow, People
from ws_common import text, INK

U = Unit(90102)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


LEVELS = ["cell", "tissue", "organ", "organ system", "organism"]


def ladder_svg():
    s = ""
    for i, l in enumerate(LEVELS):
        x = 20 + i * 104
        s += "<rect x='%d' y='20' width='92' height='40' rx='8' fill='#eef6e8' stroke='%s' stroke-width='1.5'/>" % (x, INK) + text(x + 46, 45, l, 13)
        if i:
            s += arrow(x - 10, 40, x - 2, 40, INK, 2, 6)
    return svg_wrap(540, 80, s, "levels of organization: cell, tissue, organ, organ system, organism")


EX = [("a red blood cell", "cell"), ("a neuron", "cell"), ("a skin cell", "cell"), ("a muscle cell", "cell"), ("a root hair cell", "cell"),
      ("cardiac muscle", "tissue"), ("nerve tissue", "tissue"), ("the lining of the stomach", "tissue"), ("bone tissue", "tissue"), ("xylem", "tissue"),
      ("the heart", "organ"), ("a lung", "organ"), ("the stomach", "organ"), ("the brain", "organ"), ("a kidney", "organ"), ("a leaf", "organ"),
      ("the digestive system", "organ system"), ("the nervous system", "organ system"), ("the circulatory system", "organ system"), ("the shoot system of a plant", "organ system"),
      ("a human", "organism"), ("an oak tree", "organism"), ("a frog", "organism")]


def g_level():
    e, lv = R.choice(EX)
    if not once(e):
        return None
    return item("Which level of organization is %s?" % e, lv, R.sample([l for l in LEVELS if l != lv], 3), "%s is a%s %s." % (e[0].upper() + e[1:], "n" if lv[0] in "aeiou" else "", lv))


def g_order():
    k = R.choice(["small", "large", "next", "before"])
    i = R.randrange(1, 4)
    if not once((k, i if k in ("next", "before") else 0)):
        return None
    if k == "small":
        right = " → ".join(LEVELS)
        w = [" → ".join(["tissue", "cell", "organ", "organ system", "organism"]), " → ".join(["cell", "organ", "tissue", "organ system", "organism"]),
             " → ".join(["cell", "tissue", "organ system", "organ", "organism"])]
        return item("Which list goes from smallest to largest?", right, w, "Cells form tissues, tissues form organs, organs form systems.")
    if k == "large":
        return item("Which level is the largest?", "organism", ["organ system", "organ", "tissue"], "An organism is made of all its systems.")
    if k == "next":
        return item("What level comes right after %s (going from small to large)?" % LEVELS[i], LEVELS[i + 1], [l for l in LEVELS if l not in (LEVELS[i], LEVELS[i + 1])][:3],
                    "%s → %s." % (LEVELS[i], LEVELS[i + 1]))
    return item("What level is made of many %ss working together?" % LEVELS[i - 1], LEVELS[i], [l for l in LEVELS if l not in (LEVELS[i], LEVELS[i - 1])][:3],
                "Many %ss make up a%s %s." % (LEVELS[i - 1], "n" if LEVELS[i][0] in "aeiou" else "", LEVELS[i]))


SYS = {"heart": "circulatory", "blood vessels": "circulatory", "lungs": "respiratory", "trachea": "respiratory", "diaphragm": "respiratory",
       "stomach": "digestive", "small intestine": "digestive", "liver": "digestive", "brain": "nervous", "spinal cord": "nervous",
       "kidneys": "excretory (urinary)", "bladder": "excretory (urinary)", "biceps": "muscular", "femur": "skeletal", "skin": "integumentary",
       "thyroid gland": "endocrine", "pancreas (making insulin)": "endocrine", "white blood cells": "immune"}
SYSN = sorted(set(SYS.values()))


def g_sys():
    o = R.choice(sorted(SYS))
    if not once(("s", o)):
        return None
    a = SYS[o]
    return item("Which organ system does the %s belong to?" % o, "the %s system" % a, ["the %s system" % x for x in R.sample([x for x in SYSN if x != a], 3)],
                "The %s is part of the %s system." % (o, a))


INTER = [("getting oxygen to muscle cells", "respiratory and circulatory"), ("moving nutrients from food to cells", "digestive and circulatory"),
         ("pulling your hand away from a hot stove", "nervous and muscular"), ("removing wastes from the blood", "excretory and circulatory"),
         ("controlling blood sugar after a meal", "endocrine and circulatory"), ("standing up and walking", "skeletal and muscular"),
         ("fighting an infection carried in the blood", "immune and circulatory"), ("breathing faster when you run", "nervous and respiratory")]


def g_inter():
    t, a = R.choice(INTER)
    if not once(("i", t)):
        return None
    w = R.sample(sorted({x[1] for x in INTER if x[1] != a}), 3)
    return item("Which two systems work together most directly for %s?" % t, "the %s systems" % a, ["the %s systems" % x for x in w], "Systems interact to keep the body working.")


EXER = [("the heart rate", "goes up", "to pump more oxygen-rich blood to the muscles"), ("the breathing rate", "goes up", "to take in more oxygen and remove more carbon dioxide"),
        ("sweating", "goes up", "to cool the body"), ("blood flow to the digestive system", "goes down", "so more blood can go to working muscles"),
        ("the amount of sugar the muscles use", "goes up", "to release more energy in cellular respiration")]


def g_exer():
    who = P.next()[0]
    th, ch, why = R.choice(EXER)
    k = R.random() < 0.5
    if not once((th, k)):
        return None
    if k:
        return item("%s runs hard for 10 minutes. What happens to %s?" % (who, th), "It %s." % ch, ["It %s." % ("goes down" if ch == "goes up" else "goes up"), "It stops completely.", "It stays exactly the same."],
                    "It %s %s." % (ch, why))
    w = R.sample([x[2] for x in EXER if x[2] != why], 3)
    return item("During %s's run, %s %s. Why?" % (who, th, ch), why, w, "The systems respond together.")


def g_data():
    who = P.next()[0]
    rest_h, rest_b = R.randint(62, 78), R.randint(12, 16)
    ex_h, ex_b = rest_h + R.randint(50, 80), rest_b + R.randint(14, 24)
    k = R.choice(["heart", "breath", "why"])
    if not once((rest_h, ex_h, k)):
        return None
    tab = "<table class='sn-table'><tr><th></th><th>Heart rate (beats/min)</th><th>Breathing rate (breaths/min)</th></tr><tr><td>Resting</td><td>%d</td><td>%d</td></tr><tr><td>After exercise</td><td>%d</td><td>%d</td></tr></table>" % (rest_h, rest_b, ex_h, ex_b)
    if k == "heart":
        d = ex_h - rest_h
        return item(tab + "%s measured these numbers. By how much did the heart rate increase?" % who, "%d beats/min" % d, ["%d beats/min" % ex_h, "%d beats/min" % (ex_h + rest_h), "%d beats/min" % (d + 10)],
                    "%d − %d = %d." % (ex_h, rest_h, d))
    if k == "breath":
        d = ex_b - rest_b
        return item(tab + "By how much did %s's breathing rate increase?" % who, "%d breaths/min" % d, ["%d breaths/min" % ex_b, "%d breaths/min" % (ex_b + rest_b), "%d breaths/min" % (d + 4)],
                    "%d − %d = %d." % (ex_b, rest_b, d))
    return item(tab + "What do %s's data show?" % who, "The circulatory and respiratory systems both speed up to supply oxygen.", ["Only the heart changes.", "Exercise slows the body down.", "The systems work separately."],
                "Both rates rose together.")


B1 = bank([
    ("What is a tissue?", "a group of similar cells doing the same job", ["a single cell", "a group of organs", "a whole organism"], "Cells → tissue."),
    ("What is an organ?", "a structure made of different tissues working together", ["one kind of cell", "a group of organisms", "a molecule"], "The heart has muscle, nerve and connective tissue."),
    ("Which is the smallest level of organization in an organism?", "cell", ["tissue", "organ", "organ system"], "The cell is the basic unit of life."),
    ("What is the main job of the circulatory system?", "carry blood with oxygen and nutrients around the body", ["break down food", "make hormones", "sense the world"], "Heart and blood vessels."),
    ("What is the main job of the respiratory system?", "take in oxygen and release carbon dioxide", ["pump blood", "digest food", "move bones"], "Lungs exchange gases."),
    ("What does the nervous system do?", "sends signals to control and coordinate the body", ["stores fat", "makes red blood cells only", "filters blood"], "Brain, spinal cord, nerves."),
    ("Where do oxygen and carbon dioxide move between the lungs and blood?", "the alveoli", ["the stomach", "the kidneys", "the spinal cord"], "Tiny air sacs with capillaries."),
    ("What is the job of the excretory system?", "remove wastes from the body", ["make movement", "send nerve signals", "pump blood"], "Kidneys filter blood."),
])
B5 = bank([
    ("A person's kidneys stop working. Which other system is most directly affected?", "the circulatory system, because wastes build up in the blood", ["the skeletal system only", "no other system", "the hair"], "Systems depend on each other."),
    ("A model shows a lung with a blocked airway. What happens to muscle cells?", "They get less oxygen.", ["They get more oxygen.", "Nothing.", "They get more nutrients."], "Respiratory problems affect all cells."),
    ("In a plant, which systems work together to move water from soil to leaves?", "the root system and the shoot system", ["the nervous and muscular systems", "only the flowers", "the digestive system"], "Roots absorb; xylem carries."),
    ("Why does a heart attack damage the heart muscle?", "Blocked blood vessels stop oxygen from reaching heart tissue.", ["The heart has no cells.", "The lungs stop working first.", "Bones press on the heart."], "Tissues need blood supply."),
    ("A student builds a model with boxes inside boxes: cell, tissue, organ, system. What does this show?", "Each level is made of the level below it.", ["Each level works alone.", "Cells are bigger than organs.", "Only organs matter."], "Hierarchical organization."),
])


def body():
    think = ("<div class='qfig'>%s</div><p><b>Small parts build bigger parts.</b> Many cells form a tissue; tissues form an organ; organs form a system; systems form an organism.</p>"
             "<ul><li>Each system has a job (circulatory, respiratory, digestive, nervous...).</li><li>Systems work together: lungs load oxygen, the heart moves it, muscles use it.</li></ul>") % ladder_svg()
    ex = [("Cardiac muscle: which level?", ["Many similar cells, one job"], "tissue"),
          ("You run. Which systems speed up together?", ["Muscles need more oxygen", "Lungs and heart supply it"], "respiratory and circulatory")]
    mist = ["Thinking a tissue is bigger than an organ.", "Putting the heart in the respiratory system.", "Thinking each system works alone."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Levels of organization", B1 + [(g_level, 8), (g_order, 4)]),
        ("Cells, tissues and organs", [(g_level, 12), (g_order, 4), (g_sys, 4)]),
        ("Organ systems", [(g_sys, 12), (g_inter, 4), (g_exer, 4)]),
        ("Systems working together", [(g_inter, 4), (g_exer, 6), (g_data, 6), (g_sys, 2), (g_order, 2)]),
        ("Models and evidence", B5 + [(g_data, 8), (g_exer, 2), (g_level, 3), (g_order, 2)]),
    ])
    make("biology", "levels-of-organization", 2, "HS-LS1-2",
         "Develop and use a model to illustrate the hierarchical organization of interacting systems that provide specific functions within multicellular organisms.",
         "Levels of Organization and Body Systems",
         "Levels of Organization Worksheets: Cells, Tissues, Organs and Systems (Biology)",
         "Levels of Organization",
         "Free high school biology worksheets on levels of organization (NGSS HS-LS1-2): cells, tissues, organs, organ systems and how systems work together. 100 questions with answers.",
         "Cell → tissue → organ → system.",
         "Organ systems work together to keep the whole organism alive.",
         body(),
         [("What are the levels of organization?", "Cell, tissue, organ, organ system and organism, from smallest to largest."),
          ("How do body systems work together?", "During exercise, the respiratory system takes in oxygen, the circulatory system delivers it and the nervous system speeds both up."),
          ("Do plants have organ systems?", "Yes. The root system takes in water and minerals, and the shoot system (stems, leaves, flowers) makes food and reproduces.")],
         sets)


if __name__ == "__main__":
    main()
