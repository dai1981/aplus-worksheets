# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Biology): Health and Drugs
  python tools/gen_uk_science_y9_health_and_drugs.py
Medicinal and recreational drugs and their effects on behaviour, health and life processes; alcohol (units and the
UK low-risk guideline of no more than 14 units a week), smoking (nicotine, tar, carbon monoxide), caffeine, solvents;
how medicines are tested; and healthy choices. Questions are factual health education.
Wrong answers come from real mistakes: "legal drugs are harmless", "alcohol is a stimulant", "tar is the addictive
part of tobacco", "antibiotics cure colds".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61903)
R = U.R
P = People(R)
uk_sci.USED.clear()

DRINK = [("a pint (568 ml) of beer", 568, 4, "pints (568 ml each) of beer"), ("a pint (568 ml) of cider", 568, 5, "pints (568 ml each) of cider"),
         ("a 175 ml glass of wine", 175, 12, "175 ml glasses of wine"), ("a 250 ml glass of wine", 250, 12, "250 ml glasses of wine"),
         ("a 25 ml measure of spirits", 25, 40, "25 ml measures of spirits"), ("a 330 ml bottle of beer", 330, 5, "330 ml bottles of beer"), ("a 125 ml glass of wine", 125, 12, "125 ml glasses of wine")]
NW = {2: "two", 3: "three"}


def un(x):
    return ("%.1f" % x).replace(".0", "") + " units"


def g_units():
    d, ml, pct, pl = R.choice(DRINK)
    n = R.choice([1, 2, 3])
    k = R.random() < 0.5
    if not once(("un", d, n, k)):
        return None
    u = ml * pct / 1000 * n
    g = un(u)
    dd = d if n == 1 else NW[n] + " " + pl
    if k:
        q = "Units of alcohol = strength (%%) × volume (ml) ÷ 1,000. How many units are in %s at %d%% strength?" % (dd, pct)
    else:
        q = "Units of alcohol = strength (%%) × volume (ml) ÷ 1,000. An adult drinks %s (%d%%). How many units is this?" % (dd, pct)
    return item(q, g, uniq(g, [un(ml * pct / 100 * n), un(pct * n), un(ml / 100 * n), un(u * 2), un(u / 2)]),
                "%d × %d ÷ 1,000 × %d = %.1f units. Adults are advised to drink no more than 14 units a week." % (pct, ml, n, u))


SMOKE = [("nicotine", "It is addictive and raises heart rate and blood pressure."), ("tar", "It coats the lungs and causes cancer."),
         ("carbon monoxide", "It joins with red blood cells and reduces how much oxygen the blood can carry."), ("particles of soot", "They irritate the airways and damage the alveoli.")]


def g_smoke():
    s, a = R.choice(SMOKE)
    k = R.random() < 0.5
    if not once(("sm", s, k)):
        return None
    if k:
        return item("What harm does %s in cigarette smoke do?" % s, a, R.sample([x[1] for x in SMOKE if x[1] != a], 3), "Tobacco smoke contains thousands of chemicals.")
    return item("Which substance in cigarette smoke: %s" % a[0].lower() + a[1:], s, R.sample([x[0] for x in SMOKE if x[0] != s] + ["oxygen"], 3), "Nicotine addicts; tar causes cancer; carbon monoxide reduces oxygen carried.")


DR = [("alcohol", "a depressant: it slows down the nervous system"), ("caffeine", "a stimulant: it speeds up the nervous system"), ("nicotine", "a stimulant: it speeds up the heart rate"),
      ("paracetamol", "a painkiller (medicine)"), ("antibiotics", "medicines that kill bacteria"), ("solvents (such as glue)", "vapours that are breathed in and can cause brain damage and sudden death")]


def g_dr():
    d, a = R.choice(DR)
    k = R.random() < 0.5
    if not once(("dr", d, k)):
        return None
    cat = a.split(":")[0]
    others = [x for x in DR if x[0] != d and x[1].split(":")[0] != cat]
    if k:
        return item("Which best describes %s?" % d, a[0].upper() + a[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample(others, 3)], "A drug is a substance that changes how the body works.")
    return item("Which drug is described here: “%s”?" % (a[0].upper() + a[1:]), d, R.sample([x[0] for x in others], 3), "Depressants slow the nervous system; stimulants speed it up.")


def g_data():
    rows = [("non-smoker", R.choice([10, 12, 15])), ("1–14 a day", R.choice([70, 75, 80])), ("15–24 a day", R.choice([190, 200, 210])), ("25 or more a day", R.choice([330, 350, 380]))]
    k = R.choice(["pattern", "times", "cause", "highest"])
    if not once(("da", rows[0][1], rows[3][1], k)) or not once(("da", k), 2 if k in ("pattern", "cause", "highest") else 4):
        return None
    tab = table(["Cigarettes smoked", "Lung cancer deaths per 100,000 people per year"], [[a, str(b)] for a, b in rows])
    if k == "pattern":
        return item(tab + "What does the data show?", "The more cigarettes smoked, the higher the risk of dying from lung cancer.", ["Smoking lowers the risk.", "There is no link.", "Only non-smokers get lung cancer."], "A strong correlation.")
    if k == "highest":
        return item(tab + "Which group has the highest death rate?", "25 or more a day", [r[0] for r in rows[:3]], "Read the largest number.")
    if k == "cause":
        return item(tab + "Which substance in smoke is mainly linked to lung cancer?", "tar", ["nicotine", "carbon monoxide", "oxygen"], "Tar contains carcinogens.")
    t = rows[3][1] / rows[0][1]
    g = "about %d times" % round(t)
    return item(tab + "About how many times higher is the rate for people who smoke 25 or more a day than for non-smokers?", g,
                uniq(g, ["about %d times" % round(t / 2), "about %d times" % round(t * 2), "about 2 times", "about %d times" % (rows[3][1] - rows[0][1])]), "%d ÷ %d ≈ %d." % (rows[3][1], rows[0][1], round(t)))


def g_daph():
    who = P.next()[0]
    base = R.choice([200, 210, 220, 230, 240])
    up = [0, R.choice([20, 25, 30]), R.choice([45, 50, 55]), R.choice([70, 75, 80])]
    alc = R.random() < 0.5
    k = R.choice(["pattern", "diff", "why", "ctrl", "dv"])
    if not once(("dp", base, up[3], alc, k)) or not once(("dp", alc, k), 2 if k in ("pattern", "why", "ctrl", "dv") else 8):
        return None
    drug = "alcohol" if alc else "caffeine"
    vals = [base - u for u in up] if alc else [base + u for u in up]
    tab = table(["%s concentration (%%)" % drug.capitalize(), "Heartbeats per minute"], [[c, str(v)] for c, v in zip(["0", "0.5", "1.0", "1.5"], vals)])
    intro = tab + "%s counted the heart rate of water fleas (Daphnia) in different %s solutions. " % (who, drug)
    if k == "pattern":
        a = "More alcohol made the heart rate slower." if alc else "More caffeine made the heart rate faster."
        b = "More alcohol made the heart rate faster." if alc else "More caffeine made the heart rate slower."
        return item(intro + "What do the results show?", a, [b, "The drug had no effect.", "The heart stopped at 0%."], "Alcohol is a depressant; caffeine is a stimulant.")
    if k == "diff":
        d = abs(vals[3] - vals[0])
        return item(intro + "By how many beats per minute did the heart rate change from 0%% to 1.5%%?", str(d), uniq(str(d), [str(vals[3]), str(vals[0]), str(d + 10), str(d // 2)]), "%d − %d = %d." % (max(vals[0], vals[3]), min(vals[0], vals[3]), d))
    if k == "why":
        return item(intro + "Why are water fleas used for this experiment?", "Their bodies are see-through, so the heart can be seen beating under a microscope.", ["They have no heart.", "They drink a lot.", "They are mammals."], "Transparent.")
    if k == "ctrl":
        return item(intro + "Which variable should be kept the same?", "the temperature of the water", ["the drug concentration", "the heart rate", "the name of the flea"], "Temperature also changes heart rate.")
    return item(intro + "What is the dependent variable?", "the heart rate", ["the %s concentration" % drug, "the size of the flea", "the temperature"], "What is measured.")


B1 = bank([
    ("What is a drug?", "a substance that changes the way the body or mind works", ["any food", "only an illegal substance", "a type of vitamin"], "Medicinal or recreational."),
    ("What is the difference between a medicinal and a recreational drug?", "Medicinal drugs treat illness; recreational drugs are taken for their effects on mood.", ["There is no difference.", "Recreational drugs cure disease.", "Medicinal drugs are all illegal."], "Medicines help health."),
    ("Are legal drugs always safe?", "No. Alcohol and tobacco are legal but cause serious harm.", ["Yes, always.", "Yes, if they are expensive.", "Only in summer."], "Legal is not the same as safe."),
    ("What does addiction mean?", "a strong need to keep taking a drug, with withdrawal symptoms when stopping", ["liking a food", "a healthy habit", "being allergic"], "Nicotine is very addictive."),
    ("Why do antibiotics not cure colds?", "Colds are caused by viruses, and antibiotics only kill bacteria.", ["Colds are caused by bacteria.", "Antibiotics are too weak.", "Colds are not illnesses."], "Use antibiotics only when needed."),
    ("What is the UK low-risk guideline for adults' alcohol?", "no more than 14 units a week, spread over several days", ["no more than 14 units a day", "40 units a week", "there is no guideline"], "Chief Medical Officers' advice."),
])
B5 = bank([
    ("Why is drinking alcohol in pregnancy dangerous?", "Alcohol passes through the placenta and can harm the baby's development.", ["It feeds the baby.", "The placenta blocks it.", "It only affects the mother."], "No safe amount."),
    ("Which organ is damaged most by long-term heavy drinking?", "the liver", ["the lungs", "the small intestine", "the bones"], "Cirrhosis."),
    ("Why does alcohol slow down reaction times?", "It is a depressant that slows the nervous system.", ["It is a stimulant.", "It speeds up nerves.", "It strengthens muscles."], "Never drink and drive."),
    ("How are new medicines tested before use?", "on cells and tissues in a lab, then on healthy volunteers, then on patients", ["only on the scientist", "they are not tested", "by selling them first"], "Clinical trials."),
    ("What is a placebo in a drug trial?", "a dummy treatment with no active drug, used for comparison", ["the strongest dose", "a side effect", "the patient's name"], "Double-blind trials."),
    ("Why is passive smoking harmful?", "Non-smokers breathe in the same harmful chemicals from smoke nearby.", ["It is not harmful.", "Smoke is filtered by air.", "Only smokers inhale."], "Second-hand smoke."),
])


def body():
    think = ("<p><b>A drug is any substance that changes how the body works.</b></p>"
             "<ul><li>Medicines treat illness; recreational drugs such as alcohol, nicotine and caffeine change mood and behaviour.</li>"
             "<li>Alcohol is a depressant. Units = strength (%) × volume (ml) ÷ 1,000. Adults should have no more than 14 units a week.</li>"
             "<li>Smoke contains nicotine (addictive), tar (causes cancer) and carbon monoxide (reduces oxygen in the blood).</li></ul>")
    ex = [("A 250 ml glass of wine at 12%?", ["12 × 250 ÷ 1,000"], "3 units"),
          ("Which part of smoke is addictive?", ["Not tar"], "nicotine")]
    mist = ["Thinking legal drugs are harmless.", "Thinking alcohol is a stimulant.", "Thinking antibiotics cure colds."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Drugs and medicines", B1 + [(g_dr, 9), (g_smoke, 4), (g_daph, 1)]),
        ("Alcohol", [(g_units, 14), (g_dr, 2), (g_daph, 4)]),
        ("Smoking", [(g_smoke, 3), (g_data, 8), (g_units, 6), (g_daph, 3)]),
        ("Drugs and the body", [(g_daph, 14), (g_units, 6)]),
        ("Healthy choices", B5 + [(g_units, 8), (g_data, 4), (g_daph, 2)]),
    ])
    make_ks3(9, "health-and-drugs", 3, "Biology", "Health",
             "The effects of recreational drugs (including substance misuse) on behaviour, health and life processes; the consequences of imbalances in the diet; the impact of smoking on the human gas exchange system.",
             "Health and Drugs",
             "Year 9 Science: Health and Drugs Worksheets (Alcohol Units, Smoking, Medicines)",
             "Health and Drugs",
             "Free Year 9 science worksheets on health and drugs: medicines and recreational drugs, alcohol units, depressants and stimulants, smoking, testing medicines and health data. 100 questions with answers.",
             "Drugs change how the body works.",
             "Units = strength × volume ÷ 1,000; nicotine addicts and tar causes cancer.",
             body(),
             [("How do you work out units of alcohol?", "Multiply the strength (%) by the volume in ml and divide by 1,000. For example, 250 ml of 12% wine is 12 × 250 ÷ 1,000 = 3 units."),
              ("What are the harmful substances in cigarette smoke?", "Nicotine is addictive, tar causes cancer, and carbon monoxide reduces the oxygen the blood can carry."),
              ("What is the difference between a stimulant and a depressant?", "A stimulant such as caffeine speeds up the nervous system. A depressant such as alcohol slows it down.")],
             sets)


if __name__ == "__main__":
    main()
