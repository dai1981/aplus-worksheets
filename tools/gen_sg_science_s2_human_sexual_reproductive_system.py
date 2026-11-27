# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Systems): Human Sexual Reproductive System
  python tools/gen_sg_science_s2_human_sexual_reproductive_system.py
Fertilisation (fusion of the nuclei of an egg and a sperm) and development; heredity and variation; physical changes at
puberty caused by hormones; the male and female reproductive systems and the menstrual cycle; the effects of smoking,
alcohol and drugs, including on the foetus; reasons for the growing human population; temporary and permanent birth
control methods; sexually transmitted infections (syphilis, gonorrhoea, AIDS).
UK KS3 reproduction makers are reused for the steps and words.
Wrong answers come from real mistakes: "fertilisation happens in the uterus", "the sperm duct makes sperm", "AIDS can be cured
with antibiotics", "the egg is released on day 1 of the cycle".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64210)
R = U.R
P = People(R)
HR = luse(U, "gen_uk_science_y7_human_reproduction", drop=[r"gestation period of", r"mammal in the table"])

PARTS = [("the testes", "makes sperm and the male sex hormone"), ("the scrotum", "is a sac that holds the testes outside the body, where it is cooler"),
         ("the sperm duct", "carries sperm from the testes to the urethra"), ("the prostate gland", "adds a fluid to the sperm to make semen"),
         ("the urethra in the male", "carries semen or urine out through the penis"), ("the ovaries", "releases an egg about once every 28 days and makes female sex hormones"),
         ("the oviduct (fallopian tube)", "carries the egg to the uterus and is where fertilisation usually happens"), ("the uterus (womb)", "is where the foetus develops"),
         ("the cervix", "is the ring of muscle at the neck of the uterus"), ("the vagina", "receives sperm during sexual intercourse and is the birth canal")]


def g_part():
    p, j = R.choice(PARTS)
    k = R.choice(["job", "which"])
    if not once(("pt", p, k)):
        return None
    if k == "job":
        return item("What does %s do?" % p, j[0].upper() + j[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample([x for x in PARTS if x[0] != p], 3)],
                    "%s: %s." % (p[0].upper() + p[1:], j))
    return item("Which part of the reproductive system %s?" % j, p, R.sample([x[0] for x in PARTS if x[0] != p], 3), "%s: %s." % (p[0].upper() + p[1:], j))


PUB = [("growth of facial hair", "boys"), ("voice becoming deeper", "boys"), ("shoulders becoming broader", "boys"), ("the start of sperm production", "boys"),
       ("breasts developing", "girls"), ("hips becoming wider", "girls"), ("the start of menstruation (periods)", "girls"), ("the start of egg release by the ovaries", "girls"),
       ("hair growing in the armpits", "both boys and girls"), ("a growth spurt", "both boys and girls"), ("pubic hair growing", "both boys and girls"), ("skin becoming oilier, sometimes with pimples", "both boys and girls")]


def g_pub():
    c, a = R.choice(PUB)
    if not once(("pb", c)):
        return None
    return item("During puberty, who usually experiences %s?" % c, a, [x for x in ["boys", "girls", "both boys and girls", "only adults over 30"] if x != a],
                "These changes are caused by sex hormones during puberty.")


def g_cycle():
    L = 28
    k = R.choice(["ov", "fert", "men", "next"])
    d = R.choice([1, 3, 5, 8, 10])
    if not once(("cy", k, d)) or not once(("cyk", k), 5 if k == "next" else 2):
        return None
    if k == "ov":
        return item("In a regular 28-day menstrual cycle that starts on day 1, on about which day is an egg released (ovulation)?", "day 14", ["day 1", "day 5", "day 28"],
                    "Ovulation usually happens about halfway through the cycle.")
    if k == "fert":
        return item("In a 28-day cycle, during which days is fertilisation most likely?", "about days 11 to 17", ["days 1 to 5", "days 22 to 28", "any day equally"], "Sperm can survive a few days and the egg about a day around ovulation.")
    if k == "men":
        return item("Menstruation in a 28-day cycle lasts from day 1 to day %d. What is happening?" % (d + 2 if d < 6 else 5), "The thickened lining of the uterus breaks down and is lost with some blood.",
                    ["An egg is fertilised.", "The uterus lining is thickening.", "An egg is being released."], "This happens when the egg is not fertilised.")
    st = d
    nx = st + 28
    nxs = ("%d March" % nx) if nx <= 31 else ("%d April" % (nx - 31))
    ov = "%d March" % (st + 13)
    if R.random() < 0.5:
        return item("A girl's period started on %d March. She has a regular 28-day cycle. When is her next period likely to start?" % st, nxs,
                    ["%d March" % (st + 14), ov if ov != nxs else "%d March" % (st + 7), ("%d March" % (nx - 1)) if nx - 1 <= 31 else ("%d April" % (nx - 32))],
                    "Add 28 days to the first day of the period.")
    return item("A woman's period started on %d March. She has a regular 28-day cycle. On about which date is an egg likely to be released?" % st, ov,
                ["%d March" % st, "%d March" % (st + 5), nxs], "Ovulation is at about day 14: %d March + 13 days." % st)


BC = [("a condom", "temporary", "It stops sperm from entering the vagina, and also reduces the spread of STIs."),
      ("the contraceptive pill", "temporary", "Hormones stop the ovaries from releasing eggs."),
      ("a vasectomy", "permanent", "The sperm ducts are cut and tied, so sperm cannot leave the body."),
      ("tubal ligation", "permanent", "The oviducts are cut and tied, so eggs cannot meet sperm."),
      ("an intra-uterine device (IUD)", "temporary", "It stops a fertilised egg from attaching to the uterus wall."),
      ("a diaphragm", "temporary", "It covers the cervix and stops sperm from entering the uterus.")]


def g_bc():
    m, t, how = R.choice(BC)
    k = R.choice(["type", "how"])
    if not once(("bc", m, k)):
        return None
    if k == "type":
        return item("Is %s a temporary or a permanent method of birth control?" % m, t, [x for x in ["temporary", "permanent", "not a birth control method", "a cure for STIs"] if x != t], how)
    return item("How does %s prevent pregnancy?" % m, how, R.sample([x[2] for x in BC if x[0] != m], 3), how)


STI = [("syphilis", "bacteria", "It can be cured with antibiotics if treated early."), ("gonorrhoea", "bacteria", "It can be cured with antibiotics."),
       ("AIDS", "a virus (HIV)", "It cannot be cured with antibiotics; medicines can only control it.")]


def g_sti():
    n, c, t = R.choice(STI)
    k = R.choice(["cause", "cure"])
    if not once(("st", n, k)):
        return None
    if k == "cause":
        return item("What causes %s?" % n, c, [x for x in ["bacteria", "a virus (HIV)", "a lack of vitamins", "eating too much sugar"] if x != c], "%s is caused by %s." % (n, c))
    opts = ["It can be cured with antibiotics.", "It cannot be cured with antibiotics; medicines can only control it.", "It is cured by taking vitamins.", "It goes away by itself within a day."]
    a = opts[0] if c == "bacteria" else opts[1]
    return item("Which statement about treating %s is correct?" % n, a, [x for x in opts if x != a], "Bacterial STIs can be cured with antibiotics; viral STIs such as AIDS cannot.")


B1 = bank([
    ("What is fertilisation?", "the fusion of the nucleus of a sperm with the nucleus of an egg", ["the release of an egg", "the birth of a baby", "the growth of the uterus lining"], "It forms a fertilised egg (zygote)."),
    ("Why does a child look partly like each parent?", "It receives genetic information from both the egg and the sperm.", ["It receives genes only from its mother.", "It learns to look like them.", "It receives genes only from its father."], "Sexual reproduction passes on genes from both parents."),
    ("Why do brothers and sisters with the same parents look different?", "Each child receives a different combination of genetic information from the parents.", ["They have different parents.", "Only twins have genes.", "Genes change after birth."], "This causes variation."),
    ("What causes the physical changes during puberty?", "sex hormones", ["vitamins", "digestive enzymes", "antibiotics"], "Testes and ovaries start making hormones."),
    ("How does smoking during pregnancy harm the baby?", "Harmful substances cross the placenta and can lead to a low birth weight.", ["It makes the baby stronger.", "The placenta blocks all chemicals.", "It only affects the mother."], "Alcohol and drugs can also harm the foetus."),
    ("Which is a reason for the growth of the world's human population?", "better medical care and sanitation, so fewer babies die and people live longer", ["more diseases", "less food", "fewer doctors"], "Vaccines and clean water also help."),
    ("Which method of birth control also reduces the risk of STIs?", "a condom", ["the contraceptive pill", "a vasectomy", "tubal ligation"], "It acts as a barrier."),
    ("Which is a consequence that teenagers should consider before having pre-marital sex?", "an unplanned pregnancy or an STI, which can affect health, studies and relationships", ["better exam results", "no possible effects", "a cure for diseases"], "Making informed, responsible decisions protects health."),
])
B5 = bank([
    ("A man has had a vasectomy. Why can he not father a child?", "Sperm cannot travel from the testes through the cut sperm ducts.", ["He no longer makes semen.", "His testes are removed.", "He has no hormones."], "Semen is still made by the glands."),
    ("Why are the testes outside the body in the scrotum?", "Sperm develop best at a temperature slightly below body temperature.", ["To protect them from heat in the sun.", "To make them grow bigger.", "So that urine can flow."], "It is about 2 °C cooler."),
    ("An egg released on day 14 is not fertilised. What happens next?", "The uterus lining breaks down and menstruation begins at the end of the cycle.", ["A baby develops.", "The ovary stops working.", "A new egg is released the next day."], "The cycle starts again."),
    ("Why should HIV not be treated with antibiotics?", "Antibiotics kill bacteria but do not work against viruses.", ["Antibiotics make HIV stronger only in women.", "HIV is a bacterium.", "HIV is cured by vitamins."], "Antiviral medicines can control HIV but not cure it."),
    ("Which part of the female reproductive system does the fertilised egg move to and attach to?", "the lining of the uterus", ["the ovary", "the vagina", "the cervix"], "There it develops into an embryo."),
    ("Why does a woman who drinks alcohol during pregnancy risk harming her baby?", "Alcohol can cross the placenta and affect the development of the baby's brain.", ["Alcohol cannot cross the placenta.", "It only affects the mother's liver.", "It makes the baby grow faster."], "Doctors advise no alcohol during pregnancy."),
])


def body():
    think = ("<p><b>A new individual begins when the nucleus of a sperm fuses with the nucleus of an egg.</b></p>"
             "<ul><li>Male: testes make sperm; sperm ducts carry them; glands add fluid to make semen. Female: ovaries release eggs; fertilisation happens in the oviduct; the foetus develops in the uterus.</li>"
             "<li>The child gets genetic information from both parents, so it is similar to but different from them.</li>"
             "<li>Puberty changes are caused by sex hormones. In a 28-day menstrual cycle, an egg is released at about day 14.</li>"
             "<li>Birth control can be temporary (condom, pill) or permanent (vasectomy, tubal ligation). Bacterial STIs can be cured with antibiotics; AIDS cannot.</li></ul>")
    ex = [("Where does fertilisation usually happen?", ["The egg meets sperm on its way to the uterus"], "in the oviduct"),
          ("Is a vasectomy temporary or permanent?", ["The sperm ducts are cut and tied"], "permanent")]
    mist = ["Saying fertilisation happens in the uterus. It usually happens in the oviduct.", "Saying the sperm duct makes sperm. The testes make sperm.",
            "Thinking AIDS can be cured with antibiotics. It is caused by a virus.", "Thinking the egg is released on day 1. Day 1 is the start of menstruation."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fertilisation and heredity", B1[:3] + HR.B1 + [(HR.g_step, 6), (HR.g_voc, 4)]),
        ("The reproductive systems", [(g_part, 14), (HR.g_voc, 3), (HR.g_step, 3)]),
        ("Puberty and the menstrual cycle", B1[3:4] + [(g_pub, 10), (g_cycle, 6), (g_part, 3)]),
        ("Birth control and STIs", B1[6:8] + [(g_bc, 10), (g_sti, 5), (B1[5], 1), (B1[4], 1)]),
        ("Exam-style questions", B5 + HR.B5 + [(g_cycle, 3), (g_bc, 2), (g_part, 3), (g_sti, 1), (g_pub, 2), (HR.g_step, 2)]),
    ])
    make_lss(2, "human-sexual-reproductive-system", 10, "Systems", "Human Sexual Reproductive System",
             "Recognise that fertilisation is the fusion of the nuclei of an egg and a sperm and that sexual reproduction passes on genetic information; state the physical changes at puberty "
             "caused by hormones; describe the parts of the male and female reproductive systems, fertilisation and the menstrual cycle; recognise the harmful effects of substance abuse, "
             "including on the foetus; outline temporary and permanent methods of birth control; state the consequences of sexually transmitted infections such as syphilis, gonorrhoea "
             "and AIDS (summary of the MOE Lower Secondary Science Syllabus).",
             "Human Sexual Reproductive System", seo(2, "Human Reproduction"), "Human reproduction",
             "Free Secondary 2 science worksheets for Singapore students on human reproduction: reproductive systems, fertilisation, puberty, the menstrual cycle, birth control and STIs. With answers.",
             "Fertilisation: a sperm nucleus fuses with an egg nucleus.", "It usually happens in the oviduct.",
             body(),
             [("Where does fertilisation take place?", "Usually in the oviduct (fallopian tube). The fertilised egg then attaches to the lining of the uterus."),
              ("What causes the changes at puberty?", "Sex hormones made by the testes in boys and the ovaries in girls."),
              ("Can all STIs be cured with antibiotics?", "No. Syphilis and gonorrhoea, caused by bacteria, can be cured with antibiotics. AIDS, caused by a virus (HIV), cannot.")],
             sets)


if __name__ == "__main__":
    main()
