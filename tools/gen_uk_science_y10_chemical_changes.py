# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Chemistry): Chemical Changes
  python tools/gen_uk_science_y10_chemical_changes.py
The reactivity series, extraction of metals and reduction, displacement, reactions of acids with metals, metal oxides,
hydroxides and carbonates, naming salts, the pH scale and neutralisation (H⁺ + OH⁻ → H₂O), strong and weak acids,
and electrolysis of molten and aqueous ionic compounds. Reuses questions from the Year 8 and Year 9 units (new seed)
and the displacement question of the US Chemistry unit.
Wrong answers come from real mistakes: "the gas from acid + carbonate is hydrogen", "a strong acid is a concentrated
acid", "metals form at the anode", "electrolysis of brine gives sodium".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62008)
y9_ext, y9_red = us.uk("gen_uk_science_y9_reactivity_and_extraction", "g_ext"), us.uk("gen_uk_science_y9_reactivity_and_extraction", "g_red")
y8_acid, y8_rs = us.uk("gen_uk_science_y8_metals_and_non_metals", "g_acid"), us.uk("gen_uk_science_y8_metals_and_non_metals", "g_rs")
us_act = us("chem_types_of_chemical_reactions", "g_act")

BASES = [("copper oxide", "copper", "water"), ("magnesium oxide", "magnesium", "water"), ("sodium hydroxide", "sodium", "water"),
         ("calcium carbonate", "calcium", "water and carbon dioxide"), ("zinc carbonate", "zinc", "water and carbon dioxide"), ("potassium hydroxide", "potassium", "water")]
ACIDS = [("hydrochloric acid", "chloride"), ("sulfuric acid", "sulfate"), ("nitric acid", "nitrate")]


def g_salt():
    b, m, rest = R.choice(BASES)
    a, an = R.choice(ACIDS)
    k = R.random() < 0.5
    if not once(("sa", b, a, k)):
        return None
    salt = "%s %s" % (m, an)
    if k:
        return item("%s reacts with %s. What are the products?" % (b[0].upper() + b[1:], a), "%s and %s" % (salt, rest),
                    ["%s and hydrogen" % salt, "%s and %s" % (salt, "carbon dioxide only" if "carbon" in rest else "oxygen"), "%s %s and %s" % (m, [x[1] for x in ACIDS if x[1] != an][0], rest)],
                    "acid + base → salt + water; acid + carbonate → salt + water + carbon dioxide.")
    return item("Which salt is made when %s reacts with %s?" % (b, a), salt, ["%s %s" % (m, x[1]) for x in ACIDS if x[1] != an] + ["%s oxide" % m if "oxide" not in b else "%s carbonate" % m],
                "Hydrochloric → chloride, sulfuric → sulfate, nitric → nitrate.")


PH = [(1, "strongly acidic"), (3, "weakly acidic"), (5, "weakly acidic"), (7, "neutral"), (9, "weakly alkaline"), (11, "alkaline"), (14, "strongly alkaline")]


def g_ph():
    k = R.choice(["kind", "ion", "ten"])
    if k == "kind":
        p, d = R.choice(PH)
        if not once(("ph", p)):
            return None
        return item("A solution has a pH of %d. How is it best described?" % p, d, R.sample(sorted({x[1] for x in PH if x[1] != d}), 3), "pH < 7 acidic, 7 neutral, > 7 alkaline.")
    if k == "ion":
        if not once(("ion",), 2):
            return None
        q = R.choice([("Which ions make a solution acidic?", "hydrogen ions, H⁺", ["hydroxide ions, OH⁻", "sodium ions, Na⁺", "chloride ions, Cl⁻"]),
                      ("Which ions make a solution alkaline?", "hydroxide ions, OH⁻", ["hydrogen ions, H⁺", "sulfate ions, SO₄²⁻", "chloride ions, Cl⁻"])])
        if not once(("ionq", q[0])):
            return None
        return item(q[0], q[1], q[2], "Neutralisation: H⁺ + OH⁻ → H₂O.")
    a, b = sorted(R.sample([1, 2, 3, 4], 2))
    if not once(("ten", a, b)):
        return None
    t = 10 ** (b - a)
    g = "{:,} times".format(t)
    return item("Acid A has pH %d and acid B has pH %d. How many times greater is the concentration of H⁺ ions in acid A?" % (a, b), g,
                [x for x in ["{:,} times".format(b - a), "{:,} times".format(t * 10), "2 times", "100 times", "10 times", "1,000 times"] if x != g][:3], "Each fall of 1 in pH means 10 times more H⁺ ions (higher tier).")


EL = [("molten lead bromide", "lead", "bromine"), ("molten sodium chloride", "sodium", "chlorine"), ("molten zinc chloride", "zinc", "chlorine"),
      ("aqueous sodium chloride (brine)", "hydrogen", "chlorine"), ("aqueous copper sulfate", "copper", "oxygen"), ("aqueous potassium bromide", "hydrogen", "bromine"),
      ("aqueous copper chloride", "copper", "chlorine"), ("aqueous sodium sulfate", "hydrogen", "oxygen"), ("molten aluminium oxide", "aluminium", "oxygen")]


def g_elec():
    s, cat, an = R.choice(EL)
    k = R.random() < 0.5
    if not once(("el", s, k)):
        return None
    opts = sorted({x[1] for x in EL} | {x[2] for x in EL})
    if k:
        return item("Which product forms at the negative electrode (cathode) during electrolysis of %s?" % s, cat, R.sample([x for x in opts if x not in (cat, an)], 2) + [an],
                    "Molten: the metal forms. Aqueous: hydrogen forms unless the metal is less reactive than hydrogen.")
    return item("Which product forms at the positive electrode (anode) during electrolysis of %s?" % s, an, R.sample([x for x in opts if x not in (cat, an)], 2) + [cat],
                "Halide ions give the halogen; otherwise oxygen forms.")


B1 = bank([
    ("What is oxidation in terms of oxygen?", "gain of oxygen", ["loss of oxygen", "gain of hydrogen", "loss of mass"], "Reduction is loss of oxygen."),
    ("What is oxidation in terms of electrons?", "loss of electrons (OIL RIG)", ["gain of electrons", "gain of protons", "loss of neutrons"], "Higher tier."),
    ("What is made when a metal reacts with an acid?", "a salt and hydrogen", ["a salt and water only", "carbon dioxide", "an alkali"], "Squeaky pop test."),
    ("What is the test for carbon dioxide?", "It turns limewater milky.", ["It relights a glowing splint.", "It gives a squeaky pop.", "It bleaches litmus paper."], "Acid + carbonate."),
])
B5 = bank([
    ("What is the difference between a strong and a weak acid?", "A strong acid is fully ionised in water; a weak acid is only partly ionised.", ["A strong acid is more concentrated.", "A weak acid has more water.", "There is no difference."], "Strength is not concentration."),
    ("Why must ionic compounds be molten or dissolved for electrolysis?", "The ions must be free to move to the electrodes.", ["Solids have no ions.", "It keeps them cool.", "Electrons must move in the solid."], "Mobile ions."),
    ("Why is aluminium extracted by electrolysis?", "It is more reactive than carbon.", ["It is less reactive than carbon.", "It is found pure.", "Electrolysis is cheap."], "Expensive because of electricity."),
    ("Why is cryolite used in the extraction of aluminium?", "It lowers the melting point of aluminium oxide, saving energy.", ["It makes more aluminium.", "It is a catalyst for oxygen.", "It stops the anodes burning."], "Energy saving."),
    ("Why must the carbon anodes be replaced in aluminium extraction?", "Oxygen made at the anode reacts with the carbon to form carbon dioxide.", ["They melt.", "Aluminium coats them.", "They dissolve in cryolite."], "Anodes wear away."),
])

if __name__ == "__main__":
  build(U, 10, "chemical-changes", 8, "Chemistry", "Chemical changes",
      "Reactivity of metals: metal oxides, the reactivity series, extraction of metals and reduction, oxidation and reduction in terms of electrons; reactions of acids with metals, neutralisation of acids and salt production, soluble salts, the pH scale and neutralisation, strong and weak acids; electrolysis of molten ionic compounds and aqueous solutions, and the extraction of metals using electrolysis.",
      "Chemical Changes", "Chemical Changes",
      "Free Year 10 GCSE Combined Science worksheets on chemical changes: the reactivity series, extraction and reduction, acids and salts, pH and neutralisation, strong and weak acids, and electrolysis. 100 questions with answers.",
      "acid + base → salt + water",
      "Metals form at the cathode; non-metals at the anode.",
      "<p><b>Metals react according to the reactivity series.</b></p><ul><li>Metals below carbon are extracted by reduction with carbon; reactive metals by electrolysis.</li>"
      "<li>acid + metal → salt + hydrogen; acid + base → salt + water; acid + carbonate → salt + water + carbon dioxide.</li>"
      "<li>In electrolysis, positive ions go to the cathode and negative ions go to the anode.</li></ul>",
      [("Copper oxide + sulfuric acid?", ["base + acid"], "copper sulfate + water"), ("Electrolysis of brine: cathode?", ["Sodium is more reactive than hydrogen"], "hydrogen")],
      ["Thinking acid + carbonate gives hydrogen.", "Thinking strong means concentrated.", "Thinking brine electrolysis gives sodium."],
      [("How do you name a salt?", "Use the metal's name, then the acid part: hydrochloric acid makes chlorides, sulfuric acid sulfates and nitric acid nitrates."),
       ("What happens in electrolysis?", "An electric current passes through a molten or dissolved ionic compound. Positive ions move to the cathode and gain electrons; negative ions move to the anode and lose electrons."),
       ("What is the difference between strong and weak acids?", "Strong acids such as hydrochloric acid ionise completely in water. Weak acids such as ethanoic acid only partly ionise.")],
      [("Reactivity and extraction", B1 + [(y8_rs, 6), (y9_ext, 6), (y9_red, 4)]),
       ("Displacement and redox", [(us_act, 10), (y9_red, 6), (y8_rs, 4)]),
       ("Acids and salts", [(g_salt, 12), (y8_acid, 8)]),
       ("pH and neutralisation", [(g_ph, 10), (g_salt, 10)]),
       ("Electrolysis", B5 + [(g_elec, 15)])])
