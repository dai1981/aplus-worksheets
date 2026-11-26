# -*- coding: utf-8 -*-
"""
UK Year 5 science: Growing Up and Old Age (Animals, including humans)
  python tools/gen_uk_science_y5_growing_up_and_old_age.py
The stages of human life (baby, toddler, child, teenager, adult, older adult), the changes at each stage including
puberty, growth in height and mass shown in data, and changes in old age.
Wrong answers come from real mistakes: "people grow fastest as teenagers" (it is in the first year), "growth carries
on all through adult life", "puberty happens at exactly the same age for everyone".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq, num

U = Unit(61503)
R = U.R
P = People(R)

STAGES = ["baby", "toddler", "child", "teenager", "adult", "older adult"]
DESC = [("baby", "cannot walk or talk yet and needs milk and care from adults", "need milk and care because they cannot walk or talk yet"),
        ("toddler", "is learning to walk and say first words", "learn to walk and say their first words"),
        ("child", "goes to primary school, grows steadily and loses baby teeth", "lose their baby teeth and grow steadily"),
        ("teenager", "goes through puberty and has a growth spurt", "go through puberty and have a growth spurt"),
        ("adult", "has stopped growing taller and may have children of their own", "stop growing taller and may have children of their own"),
        ("older adult", "may have grey hair, wrinkles and weaker bones", "get grey hair, wrinkles and weaker bones")]


def g_desc():
    st, d, inf = R.choice(DESC)
    k = R.random() < 0.5
    if not once(("de", st, k)):
        return None
    if k:
        return item("At which stage of life do people usually %s?" % inf, st, R.sample([x for x in STAGES if x != st], 3), "A %s %s." % (st, d))
    return item("Which description fits %s %s?" % ("an" if st[0] in "aeiou" else "a", st), "%s %s %s." % ("An" if st[0] in "aeiou" else "A", st, d),
                ["%s %s %s." % ("An" if st[0] in "aeiou" else "A", st, x[1]) for x in R.sample([x for x in DESC if x[0] != st], 3)], "Each stage has its own changes.")


def g_order():
    i = R.randrange(len(STAGES) - 1)
    k = R.random() < 0.5
    if not once(("or", i, k)):
        return None
    if k:
        a = STAGES[i + 1]
        return item("Which stage of human life comes after being a %s?" % STAGES[i], a, R.sample([x for x in STAGES if x not in (a, STAGES[i])], 3), " → ".join(STAGES) + ".")
    a = STAGES[i]
    return item("Which stage of human life comes just before being %s %s?" % ("an" if STAGES[i + 1][0] in "aeiou" else "a", STAGES[i + 1]), a,
                R.sample([x for x in STAGES if x not in (a, STAGES[i + 1])], 3), " → ".join(STAGES) + ".")


AGES = [0, 1, 2, 5, 10, 15, 20]
BASE = [50, 75, 87, 110, 140, 165, 175]


def g_height():
    who = P.next()[0]
    off = R.choice([-6, -4, -2, 0, 2, 4, 6])
    h = [b + (round(off * k / 6) if k else 0) for k, b in enumerate(BASE)]
    k = R.choice(["read", "read", "grow", "grow", "fast", "stop"])
    i, j = sorted(R.sample(range(7), 2))
    if not once(("he", off, k, i if k in ("read", "grow") else 0, j if k == "grow" else 0)) or (k in ("fast", "stop") and not once(("hk", k), 3)):
        return None
    tab = table(["Age (years)", "Height (cm)"], [[str(a), str(x)] for a, x in zip(AGES, h)])
    intro = tab + "This table shows how %s's height changed. " % who
    if k == "read":
        g = "%d cm" % h[i]
        return item(intro + "How tall was %s at %d year%s old?" % (who, AGES[i], "" if AGES[i] == 1 else "s") if AGES[i] else intro + "How long was %s at birth?" % who, g,
                    uniq(g, ["%d cm" % x for x in h] + ["%d cm" % (h[i] + 5)]), "Read the row for age %d." % AGES[i])
    if k == "grow":
        d = h[j] - h[i]
        g = "%d cm" % d
        return item(intro + "How much did %s grow between %s and age %d?" % (who, "birth" if AGES[i] == 0 else "age %d" % AGES[i], AGES[j]), g,
                    uniq(g, ["%d cm" % h[j], "%d cm" % (h[j] + h[i]), "%d cm" % (d + 10), "%d cm" % (AGES[j] - AGES[i])]), "%d − %d = %d cm." % (h[j], h[i], d))
    if k == "fast":
        return item(intro + "When did %s grow fastest (the most centimetres per year)?" % who, "in the first year of life", ["between 15 and 20", "between 10 and 15", "between 5 and 10"],
                    "About 25 cm in one year: babies grow fastest.")
    return item(intro + "What happens to height after about age 20?", "It stops increasing.", ["It doubles.", "It grows fastest.", "It grows 25 cm a year."], "Adults stop growing taller.")


def g_mass():
    b = R.choice([3, 3.2, 3.4, 3.5, 3.6, 4])
    k = R.choice(["double", "triple"])
    if not once(("ma", b, k)):
        return None
    f = 2 if k == "double" else 3
    when = "about 5 months old" if f == 2 else "about 1 year old"
    g = "about %s kg" % num(b * f, 2)
    return item("A baby has a mass of %s kg at birth. Babies usually %s their birth mass by %s. About what mass will the baby be then?" % (num(b, 2), "double" if f == 2 else "triple", when), g,
                uniq(g, ["about %s kg" % num(b + f, 2), "about %s kg" % num(b * f * 2, 2), "about %s kg" % num(b, 2), "about %s kg" % num(b * (5 - f), 2)]), "%s × %d = %s kg." % (num(b, 2), f, num(b * f, 2)))


def g_years():
    a = R.choice([("pregnancy lasts about 40 weeks", 40, "weeks", 4, "months", "about 10 lunar months, or about 9 calendar months")])
    k = R.choice(["life", "gap"])
    if k == "life":
        age = R.choice([9, 10, 11, 25, 30, 40])
        le = 81
        if not once(("lf", age)):
            return None
        g = "about %d years" % (le - age)
        return item("Life expectancy in the UK is about 81 years. If a %d-year-old lives to 81, how many more years is that?" % age, g,
                    uniq(g, ["about %d years" % (le + age), "about %d years" % age, "about %d years" % (le - age + 10), "about 81 years"]), "81 − %d = %d." % (age, le - age))
    x = R.choice([9, 10, 11])
    y = R.choice([32, 35, 38, 40, 45, 64, 70])
    if not once(("gp", x, y)):
        return None
    g = "%d years" % (y - x)
    who = P.next()[0]
    return item("%s is %d. %s's dad is %d. How many years older is %s's dad?" % (who, x, who, y, who), g,
                uniq(g, ["%d years" % (x + y), "%d years" % y, "%d years" % (y - x + 10), "%d years" % (y - x - 1)]), "%d − %d = %d." % (y, x, y - x))


OLD = [("Hair turns grey or white.", True), ("Skin becomes thinner and wrinkled.", True), ("Bones can become weaker.", True), ("Eyesight and hearing often get worse.", True),
       ("Muscles get smaller and weaker without exercise.", True), ("People grow 10 cm taller every year.", False), ("Baby teeth fall out.", False), ("A growth spurt begins.", False)]


def g_old():
    s, t = R.choice(OLD)
    if not once(("ol", s)):
        return None
    if t:
        return item("Is this a common change in old age? %s" % s, "Yes, this often happens as people get older.", ["No, this only happens to babies.", "No, this happens in puberty.", "No, this never happens to people."],
                    "Bodies change in old age; exercise and good food help.")
    when = {"People grow 10 cm taller every year.": "No, adults do not grow taller.", "Baby teeth fall out.": "No, this happens in childhood.", "A growth spurt begins.": "No, this happens in puberty."}[s]
    return item("Is this a common change in old age? %s" % s, when, ["Yes, this often happens as people get older.", "Yes, every older adult does this.", "Yes, but only in winter."], "Match each change to its stage.")


B1 = bank([
    ("What is puberty?", "the time when a child's body changes into an adult's body", ["the first year of life", "the time when hair turns grey", "a type of food"], "Usually between about 8 and 17."),
    ("Does puberty start at the same age for everyone?", "No, it starts at different ages for different people.", ["Yes, exactly at 12.", "Yes, exactly at 16.", "It never happens to boys."], "Everyone is different."),
    ("What controls the changes in puberty?", "hormones, chemical messages in the body", ["the weather", "the food you like", "the school you go to"], "Hormones are made by glands."),
    ("At about what age do most people stop growing taller?", "late teens or early twenties", ["5 years old", "40 years old", "70 years old"], "Bones stop lengthening."),
    ("How long is a human pregnancy, roughly?", "about 9 months", ["about 9 weeks", "about 2 years", "about 3 months"], "About 40 weeks."),
    ("What does a newborn baby need?", "milk, warmth, sleep and care", ["solid food only", "nothing at all", "to walk to school"], "Babies depend on adults."),
    ("When do humans grow fastest?", "in the first year of life", ["at age 30", "in old age", "at age 50"], "About 25 cm in a year."),
    ("Why do older adults often wear glasses?", "Eyesight usually gets weaker with age.", ["Glasses make them taller.", "Glasses keep them warm.", "Eyes grow bigger in old age."], "The lens of the eye stiffens."),
])
B5 = bank([
    ("How could you show how a person's height changes with age?", "plot height against age on a line graph", ["draw a pie chart of favourite foods", "use a classification key", "list their hobbies"], "Change over time: line graph."),
    ("Why might two children of the same age be different heights?", "They inherited different genes and may have had different diets.", ["One of them is lying.", "Height never varies.", "Only birthdays matter."], "Genes and environment."),
    ("Which habit helps keep bones strong in old age?", "regular exercise and foods with calcium", ["sitting all day", "eating only sweets", "never going outside"], "Healthy lifestyle."),
    ("Why do scientists say life expectancy in the UK has risen over the last 100 years?", "Better medicine, food and living conditions help people live longer.", ["People stopped ageing.", "The years became longer.", "Everyone moved abroad."], "Evidence from records."),
    ("A survey asks 30 adults their height. Which result best shows there is variation?", "Heights range from 150 cm to 190 cm.", ["Everyone is 170 cm.", "Only one person was asked.", "Heights were guessed."], "Data shows variation."),
])


def body():
    think = ("<p><b>Humans change as they grow from babies to older adults.</b></p>"
             "<ul><li>Baby → toddler → child → teenager → adult → older adult.</li>"
             "<li>We grow fastest in the first year. In puberty, hormones change a child's body into an adult's, with a growth spurt. Height stops increasing at about 20.</li>"
             "<li>In old age, hair may turn grey, skin wrinkles, bones and muscles get weaker, and eyesight and hearing may fade.</li></ul>")
    ex = [("Height 50 cm at birth, 75 cm at 1. Growth?", ["75 − 50"], "25 cm in one year"),
          ("Birth mass 3.5 kg, tripled at 1 year?", ["3.5 × 3"], "10.5 kg")]
    mist = ["Thinking people grow fastest as teenagers (it is the first year).", "Thinking adults keep growing taller.", "Thinking puberty starts at the same age for everyone."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stages of life", B1 + [(g_order, 6), (g_desc, 6)]),
        ("Changes at each stage", [(g_desc, 6), (g_order, 4), (g_old, 8), (g_mass, 2)]),
        ("Growth in height", [(g_height, 20)]),
        ("Growth in numbers", [(g_mass, 8), (g_years, 8), (g_height, 4)]),
        ("Thinking about growing", B5 + [(g_height, 8), (g_years, 7)]),
    ])
    make_uk(5, "growing-up-and-old-age", 3, "Animals, including humans",
            "Describe the changes as humans develop to old age.",
            "Growing Up and Old Age",
            "Year 5 Science: Growing Up and Old Age Worksheets (Human Life Stages and Growth)",
            "Growing Up and Old Age",
            "Free Year 5 science worksheets on how humans change from birth to old age: life stages, puberty, growth in height and mass, and changes in old age. 100 questions with answers.",
            "From baby to older adult.",
            "We grow fastest as babies, change in puberty and stop growing taller at about 20.",
            body(),
            [("What are the stages of human life?", "Baby, toddler, child, teenager (adolescent), adult and older adult. Each stage brings different changes to the body."),
             ("When do humans grow fastest?", "In the first year of life, when a baby can grow about 25 cm. There is another growth spurt during puberty."),
             ("What changes happen in old age?", "Hair may turn grey, skin becomes thinner and wrinkled, bones and muscles can weaken, and eyesight and hearing often get worse.")],
            sets)


if __name__ == "__main__":
    main()
