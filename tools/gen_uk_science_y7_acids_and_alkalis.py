# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Chemistry): Acids and Alkalis
  python tools/gen_uk_science_y7_acids_and_alkalis.py
Defining acids and alkalis in terms of neutralisation reactions; the pH scale for measuring acidity/alkalinity;
universal indicator colours; acids and alkalis at home; neutralisation (acid + alkali → salt + water), naming salts,
and everyday uses; a table of pH as alkali is added to acid.
Wrong answers come from real mistakes: "pH 1 is weakly acidic", "all acids are dangerous", "neutral means pH 0",
"neutralisation makes the acid disappear with nothing formed".
"""
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61708)
R = U.R
P = People(R)


def kind(p):
    if p == 7:
        return "neutral"
    if p < 7:
        return "a strong acid" if p <= 3 else "a weak acid"
    return "a strong alkali" if p >= 11 else "a weak alkali"


def g_ph():
    p = R.randint(0, 14)
    k = R.random() < 0.6
    if k:
        if not once(("ph", p)):
            return None
        a = kind(p)
        return item("A solution has a pH of %d. What is it?" % p, a, [x for x in ["a strong acid", "a weak acid", "neutral", "a weak alkali", "a strong alkali"] if x != a][:3] if p not in (7,) else ["a strong acid", "a strong alkali", "a weak acid"],
                    "pH below 7 is acidic (lower is stronger), 7 is neutral, above 7 is alkaline (higher is stronger).")
    vs = R.sample(range(0, 15), 4)
    q = R.choice(["most acidic", "most alkaline"])
    if not once(("pv", tuple(sorted(vs)), q)):
        return None
    a = min(vs) if q == "most acidic" else max(vs)
    return item("Which pH is %s: %s?" % (q, ", ".join(str(x) for x in sorted(vs))), "pH %d" % a, ["pH %d" % x for x in vs if x != a], "The lower the pH, the more acidic; the higher, the more alkaline.")


UI = [("red", "pH 1–2", "a strong acid"), ("orange", "pH 3–4", "an acid"), ("yellow", "pH 5–6", "a weak acid"), ("green", "pH 7", "neutral"),
      ("blue", "pH 8–10", "a weak alkali"), ("purple", "pH 11–14", "a strong alkali")]


def g_ui():
    c, r, d = R.choice(UI)
    k = R.choice(["range", "colour", "what"])
    if not once(("ui", c, k)):
        return None
    if k == "range":
        return item("Universal indicator turns %s. What is the pH?" % c, r, R.sample([x[1] for x in UI if x[1] != r], 3), "Red–orange–yellow: acid; green: neutral; blue–purple: alkali.")
    if k == "colour":
        return item("What colour is universal indicator in a solution of %s?" % r, c, R.sample([x[0] for x in UI if x[0] != c], 3), "Red–orange–yellow: acid; green: neutral; blue–purple: alkali.")
    return item("Universal indicator turns %s. What kind of solution is it?" % c, d, R.sample(sorted({x[2] for x in UI if x[2] != d and not (x[2] == "an acid" and "acid" in d) and not ("acid" in x[2] and d == "an acid")}), 3),
                "Red–orange–yellow: acid; green: neutral; blue–purple: alkali.")


SUBS = [("lemon juice", "acidic"), ("vinegar", "acidic"), ("cola", "acidic"), ("stomach acid", "acidic"), ("orange juice", "acidic"), ("sour milk", "acidic"),
        ("soap", "alkaline"), ("bleach", "alkaline"), ("oven cleaner", "alkaline"), ("baking soda solution", "alkaline"), ("toothpaste", "alkaline"), ("washing-up liquid", "alkaline"),
        ("pure water", "neutral"), ("salt solution", "neutral")]


def g_sub():
    x, a = R.choice(SUBS)
    if not once(("su", x)):
        return None
    return item("Is %s acidic, alkaline or neutral?" % x, a, [y for y in ["acidic", "alkaline", "neutral"] if y != a] + ["a metal"], "Sour foods are often acidic; cleaning products are often alkaline.")


SALT = [("hydrochloric acid", "chloride"), ("sulfuric acid", "sulfate"), ("nitric acid", "nitrate")]
BASE = [("sodium hydroxide", "sodium"), ("potassium hydroxide", "potassium"), ("calcium hydroxide", "calcium"), ("magnesium oxide", "magnesium"), ("copper oxide", "copper")]


def g_salt():
    a, an = R.choice(SALT)
    b, cat = R.choice(BASE)
    if not once(("sa", a, b)):
        return None
    g = "%s %s" % (cat, an)
    w = ["%s %s" % (cat, x[1]) for x in SALT if x[1] != an] + ["%s %s" % (R.choice([y[1] for y in BASE if y[1] != cat]), an)]
    return item("%s reacts with %s. Which salt is made?" % (a[0].upper() + a[1:], b), g, w, "Hydrochloric acid → chloride; sulfuric acid → sulfate; nitric acid → nitrate. The metal comes from the alkali or base.")


USE = [("Indigestion tablets are taken for too much stomach acid.", "They contain a base that neutralises the acid."),
       ("Farmers spread lime on fields.", "Lime neutralises acidic soil so crops grow better."),
       ("Toothpaste is slightly alkaline.", "It neutralises acids made by bacteria in the mouth."),
       ("A bee sting is acidic and is treated with baking soda.", "The alkaline baking soda neutralises the acid."),
       ("Lakes damaged by acid rain have lime added.", "Lime neutralises the acid in the water.")]


def g_use():
    s, a = R.choice(USE)
    if not once(("us", s)):
        return None
    return item("%s Why?" % s, a, R.sample([x[1] for x in USE if x[1] != a], 3), "Neutralisation: acid + alkali (or base) → salt + water.")


def g_titr():
    who = P.next()[0]
    start = R.choice([1, 2])
    seq = [start, start + 1, start + 2, 4, 6, 7, 9, 11, 12]
    drops = list(range(0, 18, 2))
    sel = sorted(R.sample(range(len(seq)), 5))
    if 5 not in sel:
        sel = sorted(set(sel[:4] + [5]))
    rows = [(drops[i], seq[i]) for i in sel]
    neutral = [d for d, p in rows if p == 7][0]
    k = R.choice(["neutral", "start", "end", "colour"])
    if not once(("ti", tuple(rows), k)):
        return None
    tab = table(["Drops of alkali added", "pH"], [[str(d), str(p)] for d, p in rows])
    intro = tab + "%s added alkali drop by drop to some acid and measured the pH. " % who
    if k == "neutral":
        g = "%d drops" % neutral
        return item(intro + "After how many drops was the solution neutral?", g, uniq(g, ["%d drops" % d for d, _ in rows]), "Neutral is pH 7.")
    if k == "start":
        a = kind(rows[0][1])
        return item(intro + "What was the solution at the start?", a, [x for x in ["a strong alkali", "neutral", "a weak alkali", "a weak acid", "a strong acid"] if x != a][:3], "Look at the first pH.")
    if k == "end":
        a = kind(rows[-1][1])
        return item(intro + "What was the solution at the end?", a, [x for x in ["a strong acid", "neutral", "a weak acid", "a weak alkali", "a strong alkali"] if x != a][:3], "Look at the last pH.")
    return item(intro + "What colour would universal indicator be when the pH was 7?", "green", ["red", "purple", "yellow"], "Neutral is green.")


B1 = bank([
    ("What is the pH of a neutral solution?", "7", ["0", "1", "14"], "Pure water is neutral."),
    ("What does an indicator do?", "changes colour to show if a solution is acidic, neutral or alkaline", ["makes a solution neutral", "measures temperature", "turns acids into alkalis"], "Litmus and universal indicator."),
    ("What colour does an acid turn blue litmus paper?", "red", ["blue", "green", "purple"], "Acids turn litmus red."),
    ("What colour does an alkali turn red litmus paper?", "blue", ["red", "orange", "yellow"], "Alkalis turn litmus blue."),
    ("What is neutralisation?", "a reaction between an acid and an alkali that makes a salt and water", ["a reaction that makes an acid stronger", "melting an acid", "mixing two acids"], "Acid + alkali → salt + water."),
    ("What does the hazard symbol 'corrosive' mean?", "it can burn and destroy skin and eyes", ["it is safe to drink", "it is a gas", "it glows in the dark"], "Wear goggles."),
    ("Which is more acidic: pH 2 or pH 5?", "pH 2", ["pH 5", "they are the same", "neither is acidic"], "Lower pH, stronger acid."),
    ("What is an alkali?", "a base that dissolves in water", ["an acid that dissolves in water", "a neutral salt", "a type of indicator"], "Sodium hydroxide is an alkali."),
])
B5 = bank([
    ("Why should you add acid to water, and not water to concentrated acid?", "Adding water to concentrated acid can make it spit dangerously.", ["Water is stronger than acid.", "It makes no difference.", "Acid floats on water."], "Safety."),
    ("What safety equipment should you wear when using acids and alkalis?", "safety goggles", ["sunglasses", "gloves made of wool", "nothing"], "Protect your eyes."),
    ("A pupil says all acids are dangerous. Is that right?", "No. Weak acids like those in fruit are safe to eat.", ["Yes, all acids burn.", "Yes, even lemon juice.", "No, no acids are dangerous."], "Strength matters."),
    ("Why is red cabbage water used as an indicator at home?", "It changes colour in acids and alkalis.", ["It neutralises acids.", "It is always purple.", "It makes salt."], "Natural indicator."),
    ("How could you find the exact amount of alkali needed to neutralise some acid?", "Add the alkali slowly, measuring the pH, until it reaches 7.", ["Pour it all in at once.", "Guess.", "Add more acid."], "Careful method."),
])


def body():
    think = ("<p><b>The pH scale shows how acidic or alkaline a solution is.</b></p>"
             "<ul><li>pH below 7: acid (lower is stronger). pH 7: neutral. Above 7: alkali (higher is stronger).</li>"
             "<li>Universal indicator: red/orange/yellow for acids, green for neutral, blue/purple for alkalis.</li>"
             "<li>Neutralisation: acid + alkali → salt + water. Hydrochloric acid makes chlorides, sulfuric acid sulfates, nitric acid nitrates.</li></ul>")
    ex = [("pH 13 is?", ["Far above 7"], "a strong alkali"),
          ("Hydrochloric acid + sodium hydroxide → ?", ["Chloride salt"], "sodium chloride + water")]
    mist = ["Thinking pH 1 is weakly acidic.", "Thinking neutral means pH 0.", "Thinking all acids are dangerous."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The pH scale", B1 + [(g_ph, 12)]),
        ("Indicators", [(g_ui, 12), (g_sub, 6), (g_ph, 2)]),
        ("Acids and alkalis at home", [(g_sub, 7), (g_use, 4), (g_ph, 9)]),
        ("Neutralisation", [(g_salt, 12), (g_titr, 8)]),
        ("Thinking about acids", B5 + [(g_titr, 10), (g_ui, 3), (g_salt, 2)]),
    ])
    make_ks3(7, "acids-and-alkalis", 8, "Chemistry", "Chemical reactions",
             "Defining acids and alkalis in terms of neutralisation reactions; the pH scale for measuring acidity/alkalinity; and indicators; reactions of acids with alkalis to produce a salt plus water.",
             "Acids and Alkalis",
             "Year 7 Science: Acids and Alkalis Worksheets (pH Scale, Indicators, Neutralisation)",
             "Acids and Alkalis",
             "Free Year 7 science worksheets on acids and alkalis: the pH scale, universal indicator and litmus, acids and alkalis at home, neutralisation and naming salts. 100 questions with answers.",
             "pH 7 is neutral.",
             "Below 7 is acidic, above 7 is alkaline. Acid + alkali → salt + water.",
             body(),
             [("What is the pH scale?", "A scale from 0 to 14. Below 7 is acidic, 7 is neutral and above 7 is alkaline. The further from 7, the stronger."),
              ("What happens in neutralisation?", "An acid reacts with an alkali to make a salt and water, for example hydrochloric acid + sodium hydroxide → sodium chloride + water."),
              ("What colours does universal indicator show?", "Red, orange or yellow for acids, green for neutral, and blue or purple for alkalis.")],
             sets)


if __name__ == "__main__":
    main()
