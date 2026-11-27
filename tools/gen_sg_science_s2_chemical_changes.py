# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Chemical Changes
  python tools/gen_sg_science_s2_chemical_changes.py
Chemical changes form new substances; word equations; atoms are rearranged, not created or destroyed, so mass is conserved;
combustion, thermal decomposition, oxidation (rusting, respiration) and neutralisation; chemical changes caused by mixing,
heating, light (photosynthesis), oxygen and electric current (electroplating); benefits (cooking, respiration) and harms
(rusting, food going bad, burning).
UK KS3 chemical reaction makers are reused.
Wrong answers come from real mistakes: "melting is a chemical change", "mass is lost when something burns in a sealed
flask", "rusting needs only water", "new atoms are made in a reaction".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64204)
R = U.R
P = People(R)
CR = luse(U, "gen_uk_science_y8_chemical_reactions", drop=[r"displacement", r"exothermic", r"endothermic"])

CH = [("frying an egg", "chemical"), ("burning a candle wick", "chemical"), ("an iron gate rusting", "chemical"), ("milk turning sour", "chemical"),
      ("baking a cake", "chemical"), ("a banana ripening and turning brown", "chemical"), ("striking a match", "chemical"), ("digesting food in the stomach", "chemical"),
      ("ice melting", "physical"), ("water boiling", "physical"), ("sugar dissolving in water", "physical"), ("cutting paper", "physical"),
      ("melting chocolate", "physical"), ("crushing a can", "physical"), ("breaking a glass", "physical"), ("water vapour condensing on a cold window", "physical")]


def g_ch():
    s, a = R.choice(CH)
    if not once(("ch", s)):
        return None
    ans = "a chemical change, because a new substance is formed" if a == "chemical" else "a physical change, because no new substance is formed"
    return item("Is %s a physical change or a chemical change?" % s, ans,
                ["a physical change, because no new substance is formed" if a == "chemical" else "a chemical change, because a new substance is formed",
                 "a chemical change, because the change can always be reversed" if a == "chemical" else "a chemical change, because it looks different",
                 "neither, because nothing changes"], "Look for a new substance: a colour change, gas, heat or light that cannot easily be reversed.")


TYPES = [("magnesium + oxygen → magnesium oxide", "combustion"), ("methane + oxygen → carbon dioxide + water", "combustion"), ("charcoal (carbon) + oxygen → carbon dioxide", "combustion"),
         ("calcium carbonate → calcium oxide + carbon dioxide", "thermal decomposition"), ("copper(II) carbonate → copper(II) oxide + carbon dioxide", "thermal decomposition"),
         ("iron + oxygen + water → rust (hydrated iron(III) oxide)", "oxidation (rusting)"), ("glucose + oxygen → carbon dioxide + water", "oxidation (respiration)"),
         ("hydrochloric acid + sodium hydroxide → sodium chloride + water", "neutralisation"), ("sulfuric acid + potassium hydroxide → potassium sulfate + water", "neutralisation"),
         ("zinc carbonate → zinc oxide + carbon dioxide", "thermal decomposition"), ("ethanol + oxygen → carbon dioxide + water", "combustion"),
         ("nitric acid + calcium hydroxide → calcium nitrate + water", "neutralisation")]
TALL = ["combustion", "thermal decomposition", "oxidation (rusting)", "oxidation (respiration)", "neutralisation"]


def g_type():
    e, a = R.choice(TYPES)
    if not once(("ty", e)):
        return None
    w = [x for x in TALL if x != a and not (x.startswith("oxidation") and a.startswith("oxidation"))]
    return item("Which type of chemical change is shown by this word equation?<br>%s" % e, a, R.sample(w, 3),
                {"combustion": "Burning in oxygen gives out heat and light.", "thermal decomposition": "One substance breaks down on heating.",
                 "neutralisation": "An acid and an alkali make a salt and water."}.get(a, "A substance reacts with oxygen."))


WE = [("magnesium", "oxygen", "magnesium oxide"), ("iron", "sulfur", "iron(II) sulfide"), ("carbon", "oxygen", "carbon dioxide"), ("hydrogen", "oxygen", "water"),
      ("sodium", "chlorine", "sodium chloride"), ("copper", "oxygen", "copper(II) oxide"), ("zinc", "sulfur", "zinc sulfide"), ("calcium", "oxygen", "calcium oxide")]


def g_we():
    a, b, c = R.choice(WE)
    k = R.choice(["prod", "react"])
    if not once(("we", a, k)):
        return None
    others = [x[2] for x in WE if x[2] != c]
    if k == "prod":
        return item("What is the product? %s + %s → ?" % (a, b), c, R.sample(others, 2) + ["%s and %s, unchanged" % (a, b)], "The elements combine to form a compound.")
    return item("Which are the reactants in this reaction? %s + %s → %s" % (a, b, c), "%s and %s" % (a, b), [c, "%s only" % c, "%s and %s" % (c, a)], "Reactants are on the left of the arrow.")


def g_mass():
    k = R.choice(["burn", "seal", "dec", "open"])
    a = R.choice([12, 24, 36, 48])
    if not once(("ms", k, a)) or not once(("msk", k), 4):
        return None
    if k == "burn":
        cu = a * 8 // 3
        o = cu // 4
        return item("%d g of copper is heated in air and reacts completely with %d g of oxygen. What mass of copper(II) oxide is formed?" % (cu, o), "%d g" % (cu + o),
                    ["%d g" % cu, "%d g" % (cu - o), "%d g" % o], "Mass is conserved: %d + %d = %d g." % (cu, o, cu + o))
    if k == "seal":
        b = R.choice([10, 20, 30])
        return item("A %d g solution is mixed with a %d g solution in a sealed flask and a solid forms. What is the total mass now?" % (a * 5, b), "%d g" % (a * 5 + b),
                    ["%d g" % (a * 5), "%d g" % (a * 5 + b - 5), "%d g" % b], "No atoms escape a sealed flask, so the mass stays the same.")
    if k == "dec":
        c = a * 25 // 12
        co = c * 44 // 100
        return item("%d g of calcium carbonate is heated and breaks down. %d g of carbon dioxide escapes. What mass of calcium oxide is left?" % (c, co), "%d g" % (c - co),
                    ["%d g" % c, "%d g" % (c + co), "%d g" % co], "Mass of products = mass of reactant: %d − %d = %d g." % (c, co, c - co))
    return item("Marble chips react with acid in an open beaker on a balance. The mass shown goes down from %d g to %d g. Why?" % (a * 5, a * 5 - 2), "Carbon dioxide gas escapes into the air.",
                ["Mass is destroyed in the reaction.", "The acid evaporates completely.", "The atoms become smaller."], "Mass is conserved; the gas leaves the beaker.")


CAUSE = [("Bread turns brown in a toaster.", "heating"), ("Plants make glucose in their leaves.", "light"), ("A copper key is coated with silver in a solution.", "electric current"),
         ("An iron nail rusts.", "oxygen (and water)"), ("Vinegar and baking soda fizz when mixed.", "mixing"), ("Photographic film darkens.", "light"),
         ("A cut apple turns brown.", "oxygen (and water)"), ("Sugar turns into black carbon when heated strongly.", "heating"), ("Water splits into hydrogen and oxygen in an electrolysis cell.", "electric current"),
         ("Two clear solutions form a yellow solid when mixed.", "mixing")]
CALL = ["heating", "light", "electric current", "oxygen (and water)", "mixing"]


def g_cause():
    s, a = R.choice(CAUSE)
    if not once(("ca", s)):
        return None
    return item(s + " What causes this chemical change?", a, R.sample([x for x in CALL if x != a], 3), "Chemical changes can be caused by mixing, heating, light, oxygen or electricity.")


B1 = bank([
    ("What is a chemical change?", "a change in which one or more new substances are formed", ["a change of state only", "a change in shape", "a change that is always easy to reverse"], "Burning, rusting and cooking are chemical changes."),
    ("What happens to atoms in a chemical reaction?", "They are rearranged to form new substances; none are created or destroyed.", ["New atoms are made.", "Atoms are destroyed.", "Atoms change into other elements."], "This is why mass is conserved."),
    ("Which is a sign that a chemical change may have happened?", "A gas is given off and the colour changes.", ["The substance changes shape.", "Ice turns into water.", "Salt dissolves in water."], "Heat or light given out is another sign."),
    ("What two things does iron need to rust?", "oxygen and water", ["oxygen only", "water only", "heat and light"], "Salt water speeds up rusting."),
    ("How can rusting of an iron gate be prevented?", "by painting it to keep out air and water", ["by keeping it wet", "by heating it", "by putting salt on it"], "Oiling and galvanising also help."),
    ("Which chemical change gives us energy from food?", "respiration, an oxidation of glucose", ["thermal decomposition", "neutralisation", "rusting"], "glucose + oxygen → carbon dioxide + water"),
    ("Why do we keep food in the refrigerator?", "Low temperatures slow down the chemical changes that make food go bad.", ["Cold stops all reactions forever.", "It adds oxygen to food.", "It makes food heavier."], "Food spoilage is a harmful chemical change."),
    ("What is electroplating used for?", "coating an object with a thin layer of metal to protect it or make it look attractive", ["melting metals", "making metals magnetic", "measuring current"], "For example, chromium-plated taps."),
])
B5 = bank([
    ("Copper(II) carbonate is green. When heated, it turns black and gives off a gas that turns limewater milky. What has happened?", "thermal decomposition, forming copper(II) oxide and carbon dioxide", ["combustion of copper", "neutralisation", "melting"], "Limewater detects carbon dioxide."),
    ("Magnesium ribbon burns with a bright white light and forms a white powder. Why is the powder heavier than the ribbon?", "Oxygen from the air has combined with the magnesium.", ["Mass is created.", "The ribbon absorbed water.", "The light added mass."], "Mass of product = mass of magnesium + oxygen."),
    ("Why do cars rust faster near the sea?", "Salt in the air speeds up rusting.", ["Sea air has no oxygen.", "Waves hit the cars.", "Sand rubs the paint off."], "Rusting needs oxygen and water; salt speeds it up."),
    ("Which change is both a chemical change and useful to us?", "cooking rice", ["iron rusting", "milk going sour", "a forest fire"], "Cooking makes food easier to digest."),
    ("A student says that burning paper is a physical change because the paper only changes shape. Why is he wrong?", "New substances (ash, carbon dioxide and water) are formed.", ["Paper is not made of atoms.", "Burning is a change of state.", "The mass stays the same in an open room."], "Burning cannot be reversed."),
    ("Which shows a word equation correctly?", "zinc + sulfuric acid → zinc sulfate + hydrogen", ["zinc → sulfuric acid + zinc sulfate", "zinc sulfate + hydrogen → zinc", "zinc + hydrogen → sulfuric acid"], "Reactants on the left, products on the right."),
])


def body():
    think = ("<p><b>In a chemical change, new substances form. Atoms are rearranged, so mass is conserved.</b></p>"
             "<ul><li>Write <b>word equations</b>: reactants → products, e.g. magnesium + oxygen → magnesium oxide.</li>"
             "<li><b>Combustion</b> (burning in oxygen), <b>thermal decomposition</b> (breaking down on heating), <b>oxidation</b> (rusting, respiration), <b>neutralisation</b> (acid + alkali).</li>"
             "<li>Chemical changes can be caused by mixing, heating, light, oxygen and electric current.</li>"
             "<li>Some are useful (cooking, respiration); some are harmful (rusting, food going bad).</li></ul>")
    ex = [("12 g of magnesium reacts with 8 g of oxygen. Mass of magnesium oxide?", ["Mass is conserved"], "20 g"),
          ("calcium carbonate → calcium oxide + carbon dioxide. Type?", ["One substance breaks down on heating"], "thermal decomposition")]
    mist = ["Calling melting or dissolving a chemical change. No new substance forms.", "Thinking mass is lost when a gas is made. In a sealed flask the mass stays the same.",
            "Saying rusting needs only water. It needs oxygen and water.", "Saying new atoms are made. Atoms are only rearranged."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Physical and chemical changes", B1[:3] + [(g_ch, 10), (CR.g_sign, 5), (B1[6], 1), (CR.B1[0], 1)]),
        ("Word equations", CR.B1[1:3] + [(g_we, 8), (g_type, 6), (CR.g_burn, 4)]),
        ("Types of chemical change", B1[3:6] + [(g_type, 6), (CR.g_type, 5), (g_cause, 6)]),
        ("Conservation of mass", [(g_mass, 10), (CR.g_cons, 6), (g_ch, 2), (B1[7], 1), (g_cause, 1)]),
        ("Exam-style questions", B5 + CR.B5 + [(g_mass, 4), (g_cause, 3), (g_we, 2), (CR.g_sign, 3)]),
    ])
    make_lss(2, "chemical-changes", 4, "Interactions", "Chemical Changes",
             "Identify chemical changes as changes in which new substances are formed and represent them with word equations; recognise that atoms are rearranged and mass is conserved; "
             "recognise combustion, thermal decomposition, oxidation (rusting and respiration) and neutralisation; investigate chemical changes caused by mixing, heating, light, oxygen "
             "and electric current; recognise their benefits and harmful effects (summary of the MOE Lower Secondary Science Syllabus).",
             "Chemical Changes", seo(2, "Chemical Changes"), "Chemical changes",
             "Free Secondary 2 science worksheets for Singapore students on chemical changes: physical vs chemical change, word equations, combustion, thermal decomposition, rusting and conservation of mass. With answers.",
             "A chemical change makes new substances.", "Atoms are rearranged, so mass is conserved.",
             body(),
             [("How can you tell a chemical change has happened?", "A new substance forms. Signs include a colour change, a gas given off, a solid forming, or heat and light given out."),
              ("Why is mass conserved in a reaction?", "Atoms are only rearranged; none are created or destroyed."),
              ("What are the main types of chemical change?", "Combustion, thermal decomposition, oxidation (such as rusting and respiration) and neutralisation.")],
             sets)


if __name__ == "__main__":
    main()
