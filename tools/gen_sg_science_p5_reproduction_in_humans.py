# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Reproduction in humans (Cycles)
  python tools/gen_sg_science_p5_reproduction_in_humans.py
The male reproductive system (testes make sperms) and the female reproductive system (ovaries make eggs; the womb is where
the baby develops). Fertilisation is the joining of a sperm and an egg; the fertilised egg develops into a baby in the womb,
getting food and oxygen from the mother through the umbilical cord. Children inherit characteristics from both parents;
some characteristics (a scar, the language we speak) are not inherited.
Wrong answers come from real mistakes: "the baby grows in the stomach", "the sperm is made in the ovary",
"a child gets all its characteristics from the mother", "a scar can be passed on to children".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63502)
R = U.R
P = People(R)
HR = use(U, "gen_uk_science_y7_human_reproduction",
         drop=["gestation", "sperm duct", "penis", "menstru", "as a period", "foetus", "cervix", "oviduct", "gamete", "semen", "gland", "scrotum", "ovulation", "implantation", "embryo", "nucleus", "placenta", "urea", "nicotine", "alcohol"])

ORG = {"testes": ("male", "make sperms"), "ovaries": ("female", "make eggs"),
       "womb (uterus)": ("female", "is where the fertilised egg develops into a baby"), "umbilical cord": (None, "carries food and oxygen from the mother to the developing baby")}


def g_org():
    o = R.choice(sorted(ORG))
    sex, job = ORG[o]
    k = R.choice(["job", "name", "sex"])
    if k == "sex" and not sex:
        return None
    if not once(("og", o, k)):
        return None
    others = [x for x in sorted(ORG) if x != o]
    if k == "job":
        return item("What do the %s do?" % o if o.endswith("s") else "What does the %s do?" % o, "It %s." % job if not o.endswith("s") else "They %s." % job,
                    [("They %s." if x.endswith("s") else "It %s.") % ORG[x][1] for x in others][:3], "The %s %s." % (o, job))
    if k == "name":
        return item("Which part %s?" % job.replace("make ", "makes ").replace("is where", "is the place where"), "the " + o, ["the " + x for x in others][:3], "The %s %s." % (o, job))
    return item("Are the %s part of the male or the female reproductive system?" % o if o.endswith("s") else "Is the %s part of the male or the female reproductive system?" % o,
                "the %s reproductive system" % sex, ["the %s reproductive system" % ("female" if sex == "male" else "male"), "the digestive system", "the respiratory system"],
                "The testes make sperms; the ovaries make eggs.")


STEPS = ["The testes make sperms and an ovary releases an egg.", "A sperm joins with the egg (fertilisation).", "The fertilised egg moves to the womb.",
         "The fertilised egg develops into a baby in the womb for about 9 months.", "The baby is born."]


def g_step():
    i = R.randrange(len(STEPS) - 1)
    k = R.choice(["next", "before"])
    if not once(("st", i, k)):
        return None
    w = [x for j, x in enumerate(STEPS) if j not in (i, i + 1)][:3]
    if k == "next":
        return item("<i>%s</i> What happens next?" % STEPS[i], STEPS[i + 1], w, "egg and sperm → fertilisation → development in the womb → birth.")
    return item("<i>%s</i> What happened just before this?" % STEPS[i + 1], STEPS[i], w, "egg and sperm → fertilisation → development in the womb → birth.")


INH = ["eye colour", "the shape of the earlobes (attached or free)", "dimples", "the ability to roll the tongue", "natural hair colour", "curly or straight hair", "blood group", "skin colour at birth",
       "freckles from birth", "a widow's peak hairline", "the shape of the nose"]
NOT_INH = ["a scar from a fall", "the language a person speaks", "a short haircut", "a tan from swimming in the sun", "the ability to ride a bicycle", "pierced ears",
           "a broken arm", "a favourite food",
           "a missing tooth from an accident", "painted nails", "knowing how to swim", "muscles built by exercise"]


def g_inh():
    k = R.choice(["yes", "no"])
    if k == "yes":
        a = R.choice(INH)
        w = R.sample(NOT_INH, 3)
        q = "Which of these characteristics can be passed from parents to their children?"
        e = "%s is inherited from the parents." % (a[0].upper() + a[1:])
    else:
        a = R.choice(NOT_INH)
        w = R.sample(INH, 3)
        q = "Which of these characteristics is NOT passed from parents to their children?"
        e = "%s is not inherited; it happens during a person's life." % (a[0].upper() + a[1:])
    if not once(("ih", a)):
        return None
    return item(q, a, w, e)


def g_family():
    trait, a, b = R.choice([("dimples", "has dimples", "has no dimples"), ("tongue rolling", "can roll the tongue", "cannot roll the tongue"),
                            ("earlobes", "has free earlobes", "has attached earlobes"), ("hair", "has curly hair", "has straight hair"),
                            ("freckles", "has freckles", "has no freckles"), ("hairline", "has a widow's peak", "has a straight hairline")])
    nm, he, his = P.next()
    k = R.choice(["both", "from"])
    if not once(("fm", trait, k)):
        return None
    if k == "from":
        return item("%s %s, like %s father. %s mother %s. Where did %s get this characteristic from?" % (nm, a, his, his.capitalize(), b, nm),
                    "from %s father" % his, ["from %s mother only" % his, "from %s friends" % his, "%s made it by practising" % he],
                    "Children inherit characteristics from both parents; this one came from the father.")
    return item("%s %s. Which statement is correct?" % (nm, a), "%s inherited characteristics from both %s parents." % (nm, his),
                ["%s inherited characteristics only from %s mother." % (nm, his), "%s inherited characteristics only from %s father." % (nm, his), "%s did not inherit any characteristics." % nm],
                "A child gets half of the inherited information from each parent.")


def g_gest():
    data = [("mouse", 3, "weeks"), ("rabbit", 1, "month"), ("cat", 2, "months"), ("dog", 2, "months"), ("pig", 4, "months"), ("human", 9, "months"),
            ("cow", 9, "months"), ("horse", 11, "months"), ("elephant", 22, "months")]
    pick = R.sample(data, 4)
    def mo(x):
        return x[1] / 4.0 if x[2] == "weeks" else x[1]
    k = R.choice(["long", "short", "read", "diff"])
    if not once(("gs", k, tuple(sorted(x[0] for x in pick)))) or not once(("gsn", k), 3):
        return None
    tb = table(["Mammal", "Time the young develops inside the mother"], [[a, "%d %s" % (n, u)] for a, n, u in pick])
    q0 = "The table shows how long the young of some mammals develop inside the mother before birth.<br>%s" % tb
    s = sorted(pick, key=mo)
    if k == "long":
        return item(q0 + "Which mammal's young develops for the longest time?", s[-1][0], [x[0] for x in s[:-1]], "Compare the times; change weeks to months first.")
    if k == "short":
        return item(q0 + "Which mammal's young develops for the shortest time?", s[0][0], [x[0] for x in s[1:]], "Compare the times; change weeks to months first.")
    x = R.choice(pick)
    if k == "read":
        return item(q0 + "How long does the young of the %s develop inside the mother?" % x[0], "%d %s" % (x[1], x[2]),
                    ["%d %s" % (y[1], y[2]) for y in pick if y != x and (y[1], y[2]) != (x[1], x[2])][:3] if len({(y[1], y[2]) for y in pick}) == 4 else None,
                    "Read the row for the %s." % x[0])
    a, b = s[-1], s[-2]
    if a[2] != "months" or b[2] != "months" or a[1] == b[1]:
        return None
    d = a[1] - b[1]
    return item(q0 + "How many months longer is it for the %s than for the %s?" % (a[0], b[0]), "%d months" % d if d > 1 else "1 month",
                ["%d months" % (a[1] + b[1]), "%d months" % a[1], "%d months" % (d + 2)], "%d − %d = %d." % (a[1], b[1], d))


TRUE = ["Sperms are made in the testes.", "Eggs are made in the ovaries.", "Fertilisation is the joining of a sperm and an egg.",
        "A baby develops in the womb.", "A child inherits characteristics from both parents.", "The umbilical cord carries food and oxygen to the baby.",
        "A baby develops in the womb for about 9 months.", "Only one sperm fertilises an egg.",
        "The testes are part of the male reproductive system.", "The womb is part of the female reproductive system.", "A sperm can swim using its tail.",
        "An egg is much bigger than a sperm."]
FALSE = ["Sperms are made in the ovaries.", "Eggs are made in the testes.", "A baby develops in the mother's stomach.", "A child inherits characteristics only from the mother.",
         "Fertilisation happens after the baby is born.", "A scar can be passed from a parent to a child.", "The umbilical cord carries sperms to the egg.",
         "A baby develops in the womb for about 9 weeks.", "Many sperms join with one egg to make one baby.",
         "The ovaries are part of the male reproductive system.", "A child can inherit a parent's haircut.", "An egg swims to the sperm using its tail.",
         "A sperm is much bigger than an egg."]


def g_true():
    k = R.choice(["t", "f"])
    if k == "t":
        a = R.choice(TRUE)
        w = R.sample(FALSE, 3)
        q = "Which statement is correct?"
    else:
        a = R.choice(FALSE)
        w = R.sample(TRUE, 3)
        q = "Which statement is NOT correct?"
    if not once(("tf", a)):
        return None
    return item(q, a, w, "Check each statement against the facts about human reproduction.")


B1 = bank([
    ("What is the function of reproduction?", "to make new individuals of the same kind so the species continues", ["to digest food", "to take in oxygen", "to remove waste"], "Without reproduction, a species would die out."),
    ("Where does a baby develop before it is born?", "in the womb (uterus)", ["in the stomach", "in the ovary", "in the small intestine"], "The womb protects the developing baby."),
    ("What is fertilisation in humans?", "the joining of a sperm and an egg", ["the birth of a baby", "the release of an egg", "the growth of the baby"], "The fertilised egg develops into a baby."),
    ("About how long does a baby develop in the womb?", "about 9 months", ["about 9 weeks", "about 2 years", "about 3 days"], "Most babies are born about 9 months after fertilisation."),
    ("How does the developing baby get food and oxygen?", "from the mother's blood, through the umbilical cord", ["by eating with its mouth", "by breathing air in the womb", "from the father"], "The umbilical cord links the baby to the mother."),
    ("How many sperms are needed to fertilise one egg?", "one", ["two", "hundreds", "none"], "Only one sperm joins with the egg."),
])
B2 = bank([
    ("Which reproductive cell is bigger?", "the egg", ["the sperm", "they are the same size", "neither is a cell"], "The egg is one of the largest cells in the body."),
    ("Which reproductive cell can swim?", "the sperm", ["the egg", "both", "neither"], "A sperm has a tail to swim to the egg."),
    ("Why does the fertilised egg need the womb?", "The womb protects it and lets it get food and oxygen from the mother.", ["The womb digests food for it.", "The womb makes sperms.", "The womb gives it light."], "The baby develops there for about 9 months."),
    ("Which parent passes on characteristics to a child?", "both parents", ["only the mother", "only the father", "neither parent"], "The sperm and the egg each carry information from one parent."),
    ("Twins who look exactly alike came from one fertilised egg. Why do they look so alike?", "They inherited the same characteristics.", ["They eat the same food.", "They wear the same clothes.", "They live in the same house."], "Identical twins share the same inherited information."),
    ("Why do brothers and sisters often look alike but not exactly the same?", "Each child inherits a different mix of characteristics from the same parents.", ["They have different parents.", "They eat different food.", "Only one child inherits characteristics."], "Each sperm and egg carries a different mix."),
    ("Which statement about the umbilical cord is correct?", "It carries food and oxygen to the baby and removes waste.", ["It carries sperms to the egg.", "It makes eggs.", "It is cut before fertilisation."], "It is cut after the baby is born, leaving the belly button."),
    ("What is the belly button?", "the place where the umbilical cord was attached", ["a muscle", "a scar from a fall", "part of the stomach"], "Everyone has one."),
])
B3 = bank([
    ("Ahmad has a scar on his knee. Will his children be born with the scar?", "No. A scar is not inherited.", ["Yes, all scars are inherited.", "Only his sons will.", "Only if the scar is big."], "A scar happens during life; it is not passed on."),
    ("Mei Ling speaks Mandarin and English. Will her baby be born able to speak them?", "No. Languages are learnt, not inherited.", ["Yes, languages are inherited.", "Only Mandarin.", "Only English."], "Children learn the language they hear."),
    ("A child has dimples. Neither of his parents has dimples, but his grandmother does. What does this show?", "Characteristics can be passed down through the family.", ["Dimples are learnt.", "Dimples come from friends.", "The child is not related to the grandmother."], "Inherited characteristics may skip a generation."),
    ("Which of these is an inherited characteristic?", "having freckles from birth", ["having a sun tan", "having a tattoo", "having short hair from a haircut"], "Freckles you are born with are inherited."),
    ("Why is a healthy diet important for a pregnant mother?", "The baby gets its food from the mother's blood.", ["The baby eats from the mother's stomach.", "The baby needs no food.", "It makes the baby's eyes change colour."], "Food passes to the baby through the umbilical cord."),
])
B5 = bank([
    ("Siti recorded whether people in her family could roll their tongues. Her mother can; her father cannot; Siti can. What can she conclude?", "Siti may have inherited this characteristic from her mother.", ["Siti learnt it from her father.", "Tongue rolling is not inherited.", "Siti got it from a friend."], "It is an inherited characteristic."),
    ("A pupil surveyed 30 pupils: 18 had free earlobes and 12 had attached earlobes. How many more had free earlobes?", "6", ["12", "18", "30"], "18 − 12 = 6."),
    ("Ravi wants to find out whether eye colour is inherited. Which data would be most useful?", "the eye colours of children and their parents", ["the eye colours of his classmates only", "the heights of his family", "how much his family eats"], "Compare children with their own parents."),
    ("Why is it important that only one sperm fertilises an egg?", "One egg and one sperm make one fertilised egg that develops into one baby.", ["More sperms make the baby bigger.", "Two sperms are always needed.", "The egg needs no sperm."], "Fertilisation joins one sperm with one egg."),
    ("A table shows that a baby's mass at birth is about 3 kg and at 1 year is about 9 kg. How many times heavier is the baby at 1 year?", "3 times", ["6 times", "9 times", "12 times"], "9 ÷ 3 = 3."),
])


def body():
    think = ("<p><b>Humans reproduce sexually: a sperm from the father joins with an egg from the mother.</b></p>"
             "<ul><li>The <b>testes</b> make sperms. The <b>ovaries</b> make eggs.</li>"
             "<li><b>Fertilisation</b> is the joining of a sperm and an egg.</li>"
             "<li>The fertilised egg develops into a baby in the <b>womb</b> for about 9 months, getting food and oxygen through the <b>umbilical cord</b>.</li>"
             "<li>Children inherit characteristics from <b>both</b> parents. Scars, haircuts and languages are not inherited.</li></ul>")
    ex = [("Where are eggs made?", ["Eggs are female reproductive cells", "They are made in the ovaries"], "In the ovaries."),
          ("A father has a scar. Will his baby have it?", ["A scar happens during life", "It is not inherited"], "No.")]
    mist = ["Thinking the baby grows in the mother's stomach. It grows in the womb.",
            "Mixing up the testes and the ovaries.",
            "Thinking a child gets all its characteristics from one parent. It inherits from both.",
            "Thinking scars, tans or languages can be inherited."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reproductive systems", B1 + [(g_org, 7), (g_true, 5)]),
        ("Fertilisation and development", B2 + [(g_step, 6), (g_org, 3), (g_true, 3)]),
        ("Inherited characteristics", B3 + [(g_inh, 8), (g_family, 4), (g_true, 3)]),
        ("Mixed practice", HR.B1 + HR.B5 + [(g_inh, 5), (g_true, 4), (g_step, 2), (g_gest, 3), (g_org, 2), (g_family, 2)]),
        ("PSLE-style questions", B5 + [(g_gest, 5), (g_family, 3), (g_inh, 3), (g_true, 4)]),
    ])
    make_sg(5, "reproduction-in-humans", 2, "Cycles", "Cycles in plants and animals (Reproduction in humans)",
            "Identify the organs of the human male and female reproductive systems and their functions: the testes produce sperms and the ovaries produce eggs. "
            "Describe fertilisation as the joining of a sperm and an egg, and that the fertilised egg develops into a baby in the womb. "
            "Recognise that characteristics are passed down from parents to their children (summary of the MOE Primary Science Syllabus).",
            "Reproduction in Humans",
            "Primary 5 Science: Reproduction in Humans Worksheets (with Answers)",
            "Reproduction in humans",
            "Free Primary 5 science worksheets for Singapore pupils on human reproduction: testes and ovaries, sperms and eggs, fertilisation, the womb, and inherited characteristics. 100 questions with answers.",
            "A sperm and an egg join to start a new life.",
            "The baby develops in the womb for about 9 months.",
            body(),
            [("Where does fertilisation take place?", "Inside the mother's body, when a sperm joins with an egg. The fertilised egg then develops in the womb."),
             ("How does a baby get food in the womb?", "Through the umbilical cord, which carries food and oxygen from the mother's blood to the baby."),
             ("Which characteristics are inherited?", "Characteristics such as eye colour, dimples, the shape of the earlobes and tongue rolling are inherited from both parents. Scars, haircuts and languages are not.")],
            sets)


if __name__ == "__main__":
    main()
