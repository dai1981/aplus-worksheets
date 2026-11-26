# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Biology): Human Reproduction
  python tools/gen_uk_science_y7_human_reproduction.py
Reproduction in humans (as an example of a mammal): the structure and function of the male and female reproductive
systems, the menstrual cycle (without details of hormones), gametes, fertilisation, gestation and birth, and the
effect of maternal lifestyle on the foetus through the placenta. Gestation periods of different mammals.
Wrong answers come from real mistakes: "fertilisation happens in the uterus", "the placenta blocks everything harmful",
"the egg is made in the uterus", "eggs and sperm have the full set of genes".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61704)
R = U.R
P = People(R)

PART = [("the testes", "make sperm cells"), ("the sperm ducts", "carry sperm from the testes towards the penis"), ("the glands", "add fluid to sperm to make semen"),
        ("the ovaries", "contain eggs and release one about once a month"), ("the oviducts", "carry the egg from the ovary to the uterus, and are where fertilisation happens"),
        ("the uterus", "is where the baby develops"), ("the cervix", "is a ring of muscle at the opening of the uterus"), ("the scrotum", "is the bag of skin that holds the testes")]


def g_part():
    p, f = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    verb = lambda x: x[1] if x[1].startswith("is") else x[1]
    if k:
        return item("What is the job of %s?" % p, f[0].upper() + f[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample([x for x in PART if x[0] != p], 3)],
                    "Each part of the reproductive system has a job.")
    return item("Which part of the reproductive system %s?" % f.replace("contain", "contains").replace("carry", "carries").replace("make sperm", "makes sperm").replace("add fluid", "adds fluid").replace("are where", "is where"),
                p, R.sample([x[0] for x in PART if x[0] != p], 3), "Each part of the reproductive system has a job.")


STEP = ["an egg is released from an ovary", "the egg travels along the oviduct", "a sperm cell fuses with the egg (fertilisation)", "the embryo attaches to the lining of the uterus",
        "the placenta forms", "the foetus develops for about 9 months", "the baby is born"]


def g_step():
    i = R.randrange(len(STEP) - 1)
    k = R.random() < 0.5
    if not once(("st", i, k)):
        return None
    if k:
        a = STEP[i + 1]
        return item("What happens next after %s?" % STEP[i], a, R.sample([x for x in STEP if x not in (a, STEP[i])], 3), "Egg released → fertilisation in the oviduct → implantation → placenta → gestation → birth.")
    a = STEP[i]
    return item("What happens just before %s?" % STEP[i + 1], a, R.sample([x for x in STEP if x not in (a, STEP[i + 1])], 3), "Egg released → fertilisation in the oviduct → implantation → placenta → gestation → birth.")


PLAC = [("oxygen", "from the mother to the foetus"), ("food (nutrients)", "from the mother to the foetus"), ("carbon dioxide", "from the foetus to the mother"),
        ("waste such as urea", "from the foetus to the mother"), ("alcohol", "from the mother to the foetus, which can harm it"),
        ("nicotine and other chemicals from smoking", "from the mother to the foetus, which can harm it"), ("some viruses", "from the mother to the foetus")]


def g_plac():
    s, d = R.choice(PLAC)
    if not once(("pl", s)):
        return None
    w = [x for x in ["from the mother to the foetus", "from the foetus to the mother", "it cannot cross the placenta", "only after the baby is born"]
         if not d.startswith(x)]
    return item("Through the placenta, how does %s move?" % s, d, w[:3], "The placenta passes oxygen and food to the foetus and takes away waste, but harmful substances can also cross.")


GEST = [("mouse", "3 weeks", 0.75), ("cat", "2 months", 2), ("dog", "2 months", 2), ("pig", "4 months", 4), ("human", "9 months", 9), ("cow", "9 months", 9),
        ("horse", "11 months", 11), ("elephant", "22 months", 22)]


def g_gest():
    rows = R.sample(GEST, 4)
    if len({r[2] for r in rows}) < 4:
        return None
    k = R.choice(["long", "short", "read"])
    ri = R.randrange(4)
    if not once(("ge", tuple(r[0] for r in rows), k, ri if k == "read" else 0)):
        return None
    tab = table(["Mammal", "Gestation period (about)"], [[r[0], r[1]] for r in rows])
    if k == "long":
        a = max(rows, key=lambda r: r[2])[0]
        return item(tab + "Which mammal in the table has the longest gestation period?", a, [r[0] for r in rows if r[0] != a], "Gestation is the time the young develops in the uterus.")
    if k == "short":
        a = min(rows, key=lambda r: r[2])[0]
        return item(tab + "Which mammal in the table has the shortest gestation period?", a, [r[0] for r in rows if r[0] != a], "Smaller mammals often have shorter gestation periods.")
    g = rows[ri][1]
    return item(tab + "About how long is the gestation period of a %s?" % rows[ri][0], g, uniq(g, [r[1] for r in rows] + ["1 year", "6 months"]), "Read the row.")


VOC = [("gamete", "a sex cell (a sperm or an egg)"), ("fertilisation", "the joining of a sperm nucleus and an egg nucleus"), ("embryo", "a fertilised egg in its first weeks as it divides"),
       ("foetus", "a developing baby once its organs have formed"), ("implantation", "when the embryo attaches to the lining of the uterus"),
       ("gestation", "the time from fertilisation to birth"), ("ovulation", "the release of an egg from an ovary"), ("menstruation", "the loss of the uterus lining as a period"),
       ("puberty", "the time when the body changes and the reproductive organs start to work"), ("placenta", "the organ that links the foetus's blood supply to the mother's")]


def g_voc():
    w, d = R.choice(VOC)
    k = R.random() < 0.5
    if not once(("vo", w, k)):
        return None
    if k:
        return item("What does '%s' mean?" % w, d, R.sample([x[1] for x in VOC if x[1] != d], 3), "Learn the key words.")
    return item("Which word means %s?" % d, w, R.sample([x[0] for x in VOC if x[0] != w], 3), "Learn the key words.")


B1 = bank([
    ("What are gametes?", "sex cells: sperm in males and eggs in females", ["any body cells", "blood cells", "a type of tissue"], "They carry half the genetic information."),
    ("Where does fertilisation usually happen?", "in the oviduct", ["in the uterus", "in the ovary", "in the vagina"], "Then the embryo moves to the uterus."),
    ("What is fertilisation?", "when the nucleus of a sperm cell joins with the nucleus of an egg cell", ["when an egg is released", "when a baby is born", "when the uterus lining breaks down"], "Two gametes join."),
    ("About how long is human gestation?", "about 9 months (40 weeks)", ["about 9 weeks", "about 2 years", "about 3 months"], "Pregnancy."),
    ("What is the placenta?", "an organ that passes oxygen and nutrients to the foetus and removes waste", ["a muscle in the cervix", "a kind of gamete", "the bag holding the testes"], "Attached by the umbilical cord."),
    ("What does the umbilical cord do?", "joins the foetus to the placenta", ["makes sperm", "releases eggs", "protects the brain"], "A lifeline."),
    ("How long is a typical menstrual cycle?", "about 28 days", ["about 7 days", "about 1 year", "about 2 days"], "It varies from person to person."),
    ("What is the amniotic fluid for?", "It cushions and protects the foetus.", ["It feeds the mother.", "It makes sperm.", "It carries the egg."], "A protective liquid."),
])
B5 = bank([
    ("Why are pregnant women advised not to smoke or drink alcohol?", "Harmful substances can cross the placenta and damage the foetus.", ["The placenta blocks them.", "It only affects the mother.", "It makes the baby grow faster."], "Maternal lifestyle matters."),
    ("Why does a sperm cell have a tail?", "to swim to the egg", ["to carry food", "to attach to the uterus", "to make it heavier"], "Adapted for its job."),
    ("Why is an egg cell much bigger than a sperm cell?", "It contains a food store for the embryo.", ["It has more tails.", "It must swim fast.", "It has no nucleus."], "Food for the early embryo."),
    ("What happens to the lining of the uterus if an egg is not fertilised?", "It breaks down and leaves the body as a period.", ["It turns into a baby.", "It becomes a placenta.", "It stays for ever."], "The menstrual cycle."),
    ("Why does a mother need a healthy diet during pregnancy?", "The foetus gets its nutrients from her blood through the placenta.", ["The foetus eats separate food.", "Diet does not matter.", "The placenta makes food from nothing."], "Healthy lifestyle."),
])


def body():
    think = ("<p><b>Humans reproduce sexually: a sperm cell and an egg cell join at fertilisation.</b></p>"
             "<ul><li>Testes make sperm; ovaries release an egg about once a month. Fertilisation happens in the oviduct.</li>"
             "<li>The embryo implants in the uterus. The placenta passes oxygen and nutrients to the foetus and takes away waste.</li>"
             "<li>Gestation lasts about 9 months. Smoking, alcohol and some drugs can cross the placenta and harm the foetus.</li></ul>")
    ex = [("Where does fertilisation happen?", ["The egg travels along it"], "the oviduct"),
          ("What does the placenta give the foetus?", ["From the mother's blood"], "oxygen and nutrients")]
    mist = ["Thinking fertilisation happens in the uterus.", "Thinking the placenta blocks everything harmful.", "Thinking eggs are made in the uterus."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reproductive systems", B1 + [(g_part, 12)]),
        ("Parts and jobs", [(g_part, 3), (g_step, 10), (g_plac, 4), (g_gest, 3)]),
        ("From egg to baby", [(g_voc, 10), (g_plac, 3), (g_step, 2), (g_gest, 5)]),
        ("Words and gestation", [(g_voc, 8), (g_gest, 12)]),
        ("Thinking about pregnancy", B5 + [(g_gest, 15)]),
    ])
    make_ks3(7, "human-reproduction", 4, "Biology", "Reproduction",
             "Reproduction in humans (as an example of a mammal), including the structure and function of the male and female reproductive systems, menstrual cycle (without details of hormones), gametes, fertilisation, gestation and birth, to include the effect of maternal lifestyle on the foetus through the placenta.",
             "Human Reproduction",
             "Year 7 Science: Human Reproduction Worksheets (Fertilisation, Gestation, Placenta)",
             "Human Reproduction",
             "Free Year 7 science worksheets on human reproduction: the reproductive systems, gametes, fertilisation, the menstrual cycle, gestation, the placenta and the effect of lifestyle on the foetus. 100 questions with answers.",
             "A sperm and an egg join at fertilisation.",
             "The placenta feeds the foetus, but harmful substances can cross it too.",
             body(),
             [("Where does fertilisation happen?", "In the oviduct. The fertilised egg then moves to the uterus and attaches to its lining."),
              ("What does the placenta do?", "It passes oxygen and nutrients from the mother's blood to the foetus and takes carbon dioxide and waste away. Alcohol, nicotine and some drugs can also cross it."),
              ("How long is a human pregnancy?", "About 9 months, or 40 weeks.")],
             sets)


if __name__ == "__main__":
    main()
