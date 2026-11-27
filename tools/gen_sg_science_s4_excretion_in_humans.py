# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 7: Excretion in Humans
  python tools/gen_sg_science_s4_excretion_in_humans.py
Excretion and the excretory products (carbon dioxide, urea, excess water and salts); the urinary system; the structure of a nephron;
ultrafiltration in the glomerulus and selective reabsorption in the tubule; the composition of plasma, filtrate and urine; the role
of ADH in water balance; kidney dialysis and transplants.
Everything is written here.
Wrong answers come from real mistakes: "egestion of faeces is excretion", "glucose is normally found in urine", "proteins are filtered
into the Bowman's capsule", "the bladder makes urine", "ADH makes more dilute urine".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool, ex, table

LV, SUBJ, SORT = 4, "Biology", 15
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

PART = [("the kidney", "filters blood and makes urine"), ("the ureter", "carries urine from the kidney to the bladder"), ("the bladder", "stores urine"),
        ("the urethra", "carries urine out of the body"), ("the renal artery", "brings blood containing urea to the kidney"),
        ("the renal vein", "carries filtered blood away from the kidney"), ("the glomerulus", "is a knot of capillaries where ultrafiltration happens"),
        ("the Bowman's capsule", "collects the filtrate from the glomerulus"), ("the proximal convoluted tubule", "reabsorbs all glucose and amino acids and much water"),
        ("the collecting duct", "reabsorbs water under the control of ADH")]
g_part = rows(R, PART, "What is the role of %s?", "Which structure %s?")

SUBS = [("water", "yes", "yes", "yes"), ("glucose", "yes", "yes", "no"), ("amino acids", "yes", "yes", "no"), ("urea", "yes", "yes", "yes"),
        ("mineral salts", "yes", "yes", "yes"), ("plasma proteins", "yes", "no", "no"), ("red blood cells", "no (in blood, not plasma)", "no", "no")]


def g_where():
    s, pl, fil, ur = R.choice(SUBS[:-1])
    k = R.choice(["fil", "ur"])
    if k == "fil":
        a = "yes" if fil == "yes" else "no"
        why = "It is small enough to be filtered through the glomerulus." if a == "yes" else "Proteins are too large to pass through the glomerulus walls."
        return tq("Is %s found in the glomerular filtrate of a healthy person?" % s, a, ["no" if a == "yes" else "yes", "only in people with diabetes", "only after exercise"], why)
    a = "yes" if ur == "yes" else "no"
    why = {"glucose": "All glucose is reabsorbed in the proximal tubule.", "amino acids": "All amino acids are reabsorbed.", "plasma proteins": "Proteins are not filtered at all."}.get(s, "It is excreted in urine.")
    return tq("Is %s normally found in the urine of a healthy person?" % s, a, ["no" if a == "yes" else "yes", "only at night", "only after exercise"], why)


DONE = set()


def g_tab():
    gl_p = R.choice([0.09, 0.1, 0.12])
    ur_p = R.choice([0.02, 0.03, 0.04])
    ur_u = R.choice([1.8, 2.0, 2.4, 2.7, 3.0])
    rows_ = [("protein", "8.0", "0", "0"), ("glucose", ex(gl_p), ex(gl_p), "0"), ("urea", ex(ur_p), ex(ur_p), ex(ur_u)), ("salts", "0.72", "0.72", "1.5")]
    t = table(["substance", "plasma / g per 100 cm³", "filtrate / g per 100 cm³", "urine / g per 100 cm³"], rows_)
    k = R.choice(["prot", "glu", "urea", "urea", "urea", "salt"])
    if k in ("prot", "glu", "salt"):
        if k in DONE:
            return None
        DONE.add(k)
    if k == "salt":
        return nq(t + "By how many times are salts more concentrated in urine than in plasma?", 1.5 / 0.72, [1.5 - 0.72, 0.72 / 1.5, 1.5], "",
                  "1.5 ÷ 0.72. Excess salts are excreted.")
    if k == "prot":
        return tq(t + "Why is there protein in the plasma but none in the filtrate?", "Protein molecules are too large to pass through the glomerulus.", ["All protein is reabsorbed.", "Protein is used up in the kidney.", "Protein is made into urea at once."], "Ultrafiltration lets only small molecules through.")
    if k == "glu":
        return tq(t + "Glucose is in the filtrate but not in the urine. Why?", "All glucose is reabsorbed into the blood by the tubule (selective reabsorption).", ["Glucose is too large to be filtered.", "Glucose is turned into urea.", "Glucose is stored in the bladder."], "Reabsorption uses active transport.")
    return nq(t + "By how many times is urea more concentrated in urine than in the filtrate?", ur_u / ur_p, [ur_u - ur_p, ur_p / ur_u, ur_u], "",
              "%s ÷ %s. Water is reabsorbed, so urea becomes more concentrated." % (ex(ur_u), ex(ur_p)))


ADH = [("You drink a lot of water.", "less ADH", "a large volume of dilute urine"), ("You sweat a lot on a hot day.", "more ADH", "a small volume of concentrated urine"),
       ("You eat very salty food.", "more ADH", "a small volume of concentrated urine"), ("You drink several glasses of a dilute fruit drink.", "less ADH", "a large volume of dilute urine"),
       ("You run a long race without drinking.", "more ADH", "a small volume of concentrated urine"),
       ("You play football for an hour in the afternoon sun.", "more ADH", "a small volume of concentrated urine"),
       ("You drink two large bottles of water after a meal.", "less ADH", "a large volume of dilute urine"),
       ("You eat a packet of salted crackers and drink nothing.", "more ADH", "a small volume of concentrated urine"),
       ("On a cool, rainy day you drink many cups of tea.", "less ADH", "a large volume of dilute urine"),
       ("You wake up after a night of not drinking anything.", "more ADH", "a small volume of concentrated urine")]


def g_vol():
    f = R.choice([150, 160, 170, 180])
    u = R.choice([1.2, 1.5, 1.8, 2.0])
    pc = (f - u) / f * 100
    return nq("The kidneys filter %d dm³ of fluid a day, but only %s dm³ of urine is made. What percentage of the filtrate is reabsorbed?" % (f, ex(u)), pc,
              [u / f * 100, 100 - u, f - u], "%", "(%d − %s) ÷ %d × 100. Almost all the water is reabsorbed." % (f, ex(u), f))


def g_adh():
    sit, h, ur = R.choice(ADH)
    if R.random() < 0.5:
        return tq("%s How does the amount of ADH released change?" % sit, h, [x for x in ("more ADH", "less ADH", "no change in ADH", "ADH stops working on the kidney") if x != h],
                  "ADH makes the collecting ducts more permeable to water. Low water potential of blood → more ADH.")
    return tq("%s What kind of urine is produced?" % sit, ur, [x for x in ("a large volume of dilute urine", "a small volume of concentrated urine", "urine containing glucose", "no urine at all") if x != ur],
              "More ADH → more water reabsorbed → less, more concentrated urine.")


POOL1 = pool(R, [
    ("What is excretion?", "the removal of waste products of metabolism and substances in excess from the body", ["the removal of undigested food", "taking in food", "releasing energy from glucose"], "Egestion of faeces is not excretion."),
    ("Which organ excretes carbon dioxide?", "the lungs", ["the kidneys", "the skin", "the liver"], "Carbon dioxide is made in respiration."),
    ("Where is urea made?", "in the liver, by deamination of excess amino acids", ["in the kidneys", "in the bladder", "in the stomach"], "It is carried in the blood to the kidneys."),
    ("What is ultrafiltration?", "the filtering of small molecules out of the blood in the glomerulus under high pressure", ["reabsorbing glucose into the blood", "storing urine", "removing carbon dioxide"], "The afferent arteriole is wider than the efferent arteriole."),
    ("Why is blood pressure high in the glomerulus?", "The vessel leading in is wider than the vessel leading out.", ["The heart is next to the kidney.", "The glomerulus pumps blood.", "Urine pushes on the blood."], "This forces small molecules out."),
    ("What is selective reabsorption?", "the return of useful substances such as glucose, amino acids, some salts and water from the tubule into the blood", ["filtering proteins", "making urea", "storing water in the bladder"], "Glucose is reabsorbed by active transport."),
    ("Why are the cells of the proximal tubule rich in mitochondria?", "They need energy for the active transport of glucose and amino acids.", ["They make urine.", "They filter blood.", "They store glycogen."], "They also have microvilli."),
    ("Where is ADH produced?", "in the brain (the pituitary gland releases it)", ["in the kidney", "in the bladder", "in the liver"], "It acts on the collecting ducts."),
    ("Which substance is found in the renal artery but less in the renal vein?", "urea", ["glucose (in a healthy person)", "red blood cells", "plasma proteins"], "Urea is removed in urine."),
    ("Why is excretion necessary?", "Waste substances such as urea are toxic if they build up.", ["It provides energy.", "It digests food.", "It makes hormones."], "The kidneys also control water and salt levels."),
])
POOL5 = pool(R, [
    ("In kidney dialysis, why does the dialysis fluid contain glucose at the same concentration as normal blood?", "so that glucose does not diffuse out of the blood", ["so that glucose diffuses into the blood", "to provide energy to the machine", "to remove urea"], "Urea diffuses out because the fluid has none."),
    ("Why does the dialysis fluid contain no urea?", "so that urea diffuses from the blood into the fluid down a concentration gradient", ["to keep urea in the blood", "because urea is a protein", "so that the fluid stays sterile"], "The fluid is constantly replaced."),
    ("Why is the dialysis fluid kept flowing in the opposite direction to the blood?", "to keep a steep concentration gradient along the whole membrane", ["to cool the blood", "to stop blood clotting", "to pump blood faster"], "Countercurrent flow."),
    ("Why is the dialysis membrane partially permeable?", "Small molecules such as urea pass through, but blood cells and proteins do not.", ["It lets everything through.", "It stops urea passing.", "It pumps glucose into the fluid."], "It acts like the glomerulus."),
    ("Give one advantage of a kidney transplant over dialysis.", "The patient does not need dialysis several times a week and can eat a more normal diet.", ["There is no risk of rejection.", "No drugs are ever needed.", "It is always available at once."], "Drugs must be taken to stop rejection."),
    ("Glucose is found in a person's urine. What is the most likely cause?", "diabetes: the blood glucose is too high for all of it to be reabsorbed", ["drinking too much water", "a high-protein diet", "a damaged bladder"], "This is checked with a urine test strip."),
    ("Protein is found in a person's urine. What does this suggest?", "The glomeruli are damaged.", ["The person drank a lot.", "The person ate a lot of sugar.", "The liver is making too much urea."], "Normally proteins are too large to be filtered."),
    ("On a hot day, a person produces less urine. Why?", "More water is lost in sweat, so more ADH is released and more water is reabsorbed.", ["Less ADH is released.", "The kidneys stop filtering.", "Urea is stored in the bladder."], "Negative feedback keeps the water potential of blood steady."),
])


def main():
    sets = U.sets([
        ("Excretion and the urinary system", [(POOL1, 5), (g_part, 8), (g_where, 4), (g_vol, 3)]),
        ("The nephron", [(g_part, 6), (POOL1, 4), (g_where, 4), (g_tab, 4), (g_vol, 2)]),
        ("Plasma, filtrate and urine", [(g_tab, 10), (g_where, 4), (POOL5, 2), (g_vol, 4)]),
        ("Water balance and ADH", [(g_adh, 12), (POOL1, 1), (g_tab, 3), (g_part, 2), (POOL5, 2)]),
        ("Dialysis and exam-style questions", [(POOL5, 4), (g_tab, 5), (g_vol, 3), (g_adh, 6), (g_part, 2)]),
    ])
    make_ol(LV, SUBJ, "excretion-in-humans", SORT, "Excretion in Humans",
            "Define excretion and state the excretory products; identify the parts of the urinary system; describe the structure of a nephron and explain "
            "ultrafiltration in the glomerulus and selective reabsorption in the tubule; compare the composition of plasma, filtrate and urine; describe the role "
            "of ADH in regulating the water potential of the blood; describe the principles of kidney dialysis (summary of the Singapore-Cambridge O-Level Biology "
            "6093 syllabus).",
            "Excretion in Humans", "Excretion",
            "Free Secondary 4 O-Level Biology worksheets on excretion in humans: the kidneys, nephron, ultrafiltration, selective reabsorption, urine, ADH and "
            "dialysis. 100 questions with answers.",
            "Filter everything small, then take back what is useful.", "More ADH → more water reabsorbed → less, concentrated urine.",
            "<p><b>Kidneys remove urea and control water.</b></p><ul>"
            "<li>Excretion removes waste of metabolism: carbon dioxide (lungs), urea, excess water and salts (kidneys).</li>"
            "<li>Ultrafiltration: high pressure in the glomerulus forces water, glucose, amino acids, salts and urea into the Bowman's capsule. Proteins and cells stay in the blood.</li>"
            "<li>Selective reabsorption: all glucose and amino acids and much water and salt return to the blood.</li>"
            "<li>ADH makes the collecting ducts more permeable to water. Dialysis uses a partially permeable membrane and fluid without urea.</li></ul>",
            [("Urea 0.03 in filtrate, 2.4 in urine. How many times?", ["2.4 ÷ 0.03"], "80"),
             ("Very salty meal. ADH?", ["blood water potential falls", "more ADH"], "more ADH, less urine")],
            ["Calling egestion of faeces excretion.", "Saying glucose is normally found in urine.", "Saying proteins are filtered into the Bowman's capsule.",
             "Saying ADH makes dilute urine."],
            [("What is the difference between ultrafiltration and selective reabsorption?", "Ultrafiltration forces small molecules out of the blood in the glomerulus under high pressure. Selective reabsorption returns useful substances, such as all glucose and amino acids and much water, from the tubule to the blood."),
             ("What does ADH do?", "When the blood has too little water, more ADH is released. It makes the collecting ducts more permeable, so more water is reabsorbed and a small volume of concentrated urine is made."),
             ("How does kidney dialysis work?", "Blood flows past a partially permeable membrane with dialysis fluid on the other side. The fluid has no urea but normal levels of glucose and salts, so urea and excess salts diffuse out of the blood.")],
            sets)


if __name__ == "__main__":
    main()
