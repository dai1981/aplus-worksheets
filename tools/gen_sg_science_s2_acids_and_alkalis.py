# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Chemical Changes (acids, alkalis and indicators)
  python tools/gen_sg_science_s2_acids_and_alkalis.py
Acidic, alkaline and neutral solutions and the pH scale; indicators (litmus, Universal Indicator and natural indicators such as
red cabbage and butterfly pea flower); reactions of acids with alkalis (neutralisation), with metals (hydrogen, the 'pop' test)
and with carbonates (carbon dioxide, limewater); uses of neutralisation.
UK KS3 acid and alkali makers are reused.
Wrong answers come from real mistakes: "pH 12 is a strong acid", "red litmus turns red in alkali", "acids and metals give
carbon dioxide", "neutralisation makes only water".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64205)
R = U.R
P = People(R)
AC = luse(U, "gen_uk_science_y7_acids_and_alkalis", drop=[r"washing-up", r"oven cleaner", r"\blime\b", r"acid rain"])

LIT = [("acidic", "blue litmus turns red; red litmus stays red"), ("alkaline", "red litmus turns blue; blue litmus stays blue"), ("neutral", "neither litmus paper changes colour")]


def g_lit():
    t, r = R.choice(LIT)
    k = R.choice(["what", "res"])
    if not once(("li", t, k)):
        return None
    if k == "what":
        return item("A solution is tested with red and blue litmus paper: %s. What kind of solution is it?" % r, t, [x for x in ["acidic", "alkaline", "neutral", "a pure metal"] if x != t],
                    "Acids turn blue litmus red; alkalis turn red litmus blue.")
    return item("What happens when red and blue litmus paper are dipped into %s %s solution?" % ("an" if t[0] in "ae" else "a", t), r[0].upper() + r[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in LIT if x[0] != t] + ["Both turn green."],
                "Acids turn blue litmus red; alkalis turn red litmus blue.")


SUB = [("vinegar", 3, "acidic"), ("lemon juice", 2, "acidic"), ("pure water", 7, "neutral"), ("soap solution", 9, "alkaline"), ("stomach acid", 1, "acidic"),
       ("toothpaste", 8, "alkaline"), ("sodium hydroxide solution", 14, "alkaline"), ("sugar solution", 7, "neutral"), ("bleach", 12, "alkaline"), ("cola drink", 3, "acidic"),
       ("ammonia cleaning solution", 11, "alkaline"), ("salt solution", 7, "neutral")]


def g_ph():
    s, ph, t = R.choice(SUB)
    k = R.choice(["type", "most"])
    if k == "type":
        if not once(("pt", s)):
            return None
        return item("%s has a pH of %d. Is it acidic, alkaline or neutral?" % (s[0].upper() + s[1:], ph), t, [x for x in ["acidic", "alkaline", "neutral", "a salt"] if x != t],
                    "Below 7 is acidic, 7 is neutral, above 7 is alkaline.")
    pick = R.sample(SUB, 4)
    if len({x[1] for x in pick}) < 4:
        return None
    lo = R.choice([True, False])
    best = min(pick, key=lambda x: x[1]) if lo else max(pick, key=lambda x: x[1])
    if not once(("pm", tuple(sorted(x[0] for x in pick)), lo)):
        return None
    return item("Which is the most %s? %s" % ("acidic" if lo else "alkaline", "; ".join("%s (pH %d)" % (x[0], x[1]) for x in pick)), best[0], [x[0] for x in pick if x != best],
                "The %s the pH, the more %s the solution." % ("lower" if lo else "higher", "acidic" if lo else "alkaline"))


NAT = [("red cabbage juice", "red or pink", "green or yellow"), ("butterfly pea flower tea", "pink or purple", "green"), ("turmeric solution", "yellow", "red-brown")]


def g_nat():
    n, ac, al = R.choice(NAT)
    k = R.choice(["acid", "alk"])
    if not once(("na", n, k)):
        return None
    a = ac if k == "acid" else al
    o = al if k == "acid" else ac
    return item("%s is a natural indicator. What colour does it turn in %s?" % (n[0].upper() + n[1:], "lime juice (an acid)" if k == "acid" else "soap solution (an alkali)"), a,
                [o, "colourless", "black"] if "black" not in (a, o) else [o, "colourless", "white"], "%s is %s in acids and %s in alkalis." % (n[0].upper() + n[1:], ac, al))


RX = [("magnesium", "hydrochloric acid", "magnesium chloride + hydrogen", "metal"), ("zinc", "sulfuric acid", "zinc sulfate + hydrogen", "metal"),
      ("iron", "hydrochloric acid", "iron(II) chloride + hydrogen", "metal"), ("calcium carbonate", "hydrochloric acid", "calcium chloride + water + carbon dioxide", "carbonate"),
      ("sodium carbonate", "sulfuric acid", "sodium sulfate + water + carbon dioxide", "carbonate"), ("copper(II) carbonate", "hydrochloric acid", "copper(II) chloride + water + carbon dioxide", "carbonate"),
      ("sodium hydroxide", "hydrochloric acid", "sodium chloride + water", "alkali"), ("potassium hydroxide", "nitric acid", "potassium nitrate + water", "alkali")]


def g_rx():
    a, b, p, t = R.choice(RX)
    k = R.choice(["gas", "prod"])
    if not once(("rx", a, k)):
        return None
    if k == "gas":
        gas = {"metal": "hydrogen, which burns with a 'pop' sound", "carbonate": "carbon dioxide, which turns limewater milky", "alkali": "no gas; a salt and water form"}[t]
        return item("%s reacts with %s. Which gas is produced?" % (a[0].upper() + a[1:], b), gas,
                    [x for x in ["hydrogen, which burns with a 'pop' sound", "carbon dioxide, which turns limewater milky", "no gas; a salt and water form", "oxygen, which relights a glowing splint"] if x != gas],
                    "Acid + metal → salt + hydrogen. Acid + carbonate → salt + water + carbon dioxide. Acid + alkali → salt + water.")
    others = [x[2] for x in RX if x[2] != p]
    return item("Complete the word equation: %s + %s → ?" % (a, b), p, R.sample(others, 3), "The salt is named from the metal and the acid.")


B1 = bank([
    ("What is the pH of a neutral solution?", "7", ["0", "14", "1"], "Pure water is neutral."),
    ("What colour is Universal Indicator in a neutral solution?", "green", ["red", "purple", "orange"], "Red to yellow is acidic; blue to purple is alkaline."),
    ("What is neutralisation?", "the reaction between an acid and an alkali to form a salt and water", ["the reaction of a metal with oxygen", "the dissolving of salt in water", "the breaking down of a substance by heat"], "The pH moves towards 7."),
    ("Which gas is given off when an acid reacts with a metal such as zinc?", "hydrogen", ["carbon dioxide", "oxygen", "nitrogen"], "A lighted splint gives a 'pop'."),
    ("Which gas is given off when an acid reacts with a carbonate?", "carbon dioxide", ["hydrogen", "oxygen", "chlorine"], "It turns limewater milky."),
    ("Why is Universal Indicator more useful than litmus?", "It shows how strongly acidic or alkaline a solution is, not just whether it is acidic or alkaline.", ["It is always red.", "It only works with acids.", "It is a natural indicator."], "It gives a pH value from its colour."),
    ("Why do farmers add slaked lime (calcium hydroxide) to soil?", "to neutralise acidic soil so that crops grow better", ["to make the soil more acidic", "to kill all plants", "to add water"], "Most crops grow best near pH 7."),
    ("Why does an antacid tablet relieve indigestion?", "It is a weak alkali that neutralises excess stomach acid.", ["It is a strong acid.", "It makes more acid.", "It dissolves food."], "Indigestion is caused by too much acid."),
])
B5 = bank([
    ("A student adds sodium hydroxide solution drop by drop to hydrochloric acid with Universal Indicator. How does the colour change?", "red → orange → yellow → green", ["green → red", "purple → blue → green → red", "it stays red"], "The pH rises towards 7."),
    ("Why should you not taste or touch chemicals to find out if they are acids or alkalis?", "Many are corrosive or toxic; use indicators instead.", ["Tasting is the best test.", "All acids are safe.", "Alkalis are sweet."], "Safety first in the laboratory."),
    ("A bee sting is acidic. Which would be best to put on it?", "a weak alkali such as baking soda solution", ["vinegar", "lemon juice", "concentrated acid"], "The alkali neutralises the acid."),
    ("Marble statues slowly wear away in polluted rain. Why?", "Marble is calcium carbonate, which reacts with acids in the rain.", ["Marble is an alkali that dissolves in water.", "Rain is neutral.", "Marble is a metal."], "Carbon dioxide is given off."),
    ("Butterfly pea flower tea turns pink when lime juice is added. What does this show?", "Lime juice is acidic.", ["Lime juice is alkaline.", "The tea is a metal.", "Lime juice is neutral."], "Natural indicators change colour with pH."),
    ("A solution turns Universal Indicator purple. What is its likely pH?", "13", ["2", "5", "7"], "Purple means strongly alkaline."),
])


def body():
    think = ("<p><b>Indicators show whether a solution is acidic, neutral or alkaline.</b></p>"
             "<ul><li><b>pH scale</b>: below 7 acidic, 7 neutral, above 7 alkaline. Universal Indicator: red (strong acid) → green (neutral) → purple (strong alkali).</li>"
             "<li><b>Litmus</b>: acids turn blue litmus red; alkalis turn red litmus blue. Natural indicators: red cabbage, butterfly pea flower.</li>"
             "<li>acid + alkali → salt + water (<b>neutralisation</b>).</li>"
             "<li>acid + metal → salt + <b>hydrogen</b>. acid + carbonate → salt + water + <b>carbon dioxide</b>.</li></ul>")
    ex = [("A solution has pH 3. Acidic, neutral or alkaline?", ["Below 7"], "acidic"),
          ("zinc + hydrochloric acid → ?", ["acid + metal → salt + hydrogen"], "zinc chloride + hydrogen")]
    mist = ["Thinking a high pH is strongly acidic. High pH is alkaline.", "Mixing up litmus colours: acids turn blue litmus red.",
            "Saying acids and metals give carbon dioxide. They give hydrogen.", "Forgetting the salt: neutralisation gives a salt and water."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Acids, alkalis and pH", B1[:2] + AC.B1 + [(g_ph, 8), (AC.g_ph, 4), (AC.g_sub, 4)]),
        ("Indicators", B1[5:6] + [(g_lit, 6), (AC.g_ui, 6), (g_nat, 6), (g_ph, 1)]),
        ("Neutralisation", B1[2:3] + B1[6:8] + [(AC.g_titr, 6), (AC.g_salt, 6), (g_rx, 3), (g_ph, 2)]),
        ("Acids with metals and carbonates", B1[3:5] + [(g_rx, 12), (AC.g_salt, 3), (g_lit, 3)]),
        ("Exam-style questions", B5 + AC.B5 + [(g_rx, 3), (AC.g_titr, 3), (g_ph, 3), (g_nat, 2)]),
    ])
    make_lss(2, "acids-and-alkalis", 5, "Interactions", "Chemical Changes (Acids, alkalis and indicators)",
             "Investigate the reactions between acids and alkalis, acids and metals, and acids and carbonates, and represent them with word equations; investigate the effect of acidic, "
             "alkaline and neutral solutions on litmus, Universal Indicator and natural indicators; recognise uses of neutralisation (summary of the MOE Lower Secondary Science Syllabus).",
             "Acids, Alkalis and Indicators", seo(2, "Acids, Alkalis and Indicators"), "Acids and alkalis",
             "Free Secondary 2 science worksheets for Singapore students on acids and alkalis: pH, litmus, Universal Indicator, natural indicators, neutralisation and reactions with metals and carbonates. With answers.",
             "Below pH 7 acidic, 7 neutral, above 7 alkaline.", "acid + alkali → salt + water.",
             body(),
             [("What does litmus show?", "Acids turn blue litmus red. Alkalis turn red litmus blue. Neutral solutions do not change either."),
              ("What gas is made when an acid reacts with a metal?", "Hydrogen. It burns with a 'pop' when a lighted splint is held near it."),
              ("What is a natural indicator?", "A plant extract that changes colour in acids and alkalis, such as red cabbage juice or butterfly pea flower tea.")],
             sets)


if __name__ == "__main__":
    main()
