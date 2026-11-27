# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Chemistry (6092), Topic 5: Acid-Base Chemistry
  python tools/gen_sg_science_s3_acid_base_chemistry.py
Acids (H⁺ ions) and alkalis (OH⁻ ions), pH and Universal Indicator, strong and weak acids, neutralisation (H⁺ + OH⁻ → H₂O),
reactions of acids with metals, bases and carbonates, preparation of salts (titration, excess insoluble solid, precipitation)
and solubility rules, ammonia and the Haber process (reversible reactions and conditions), and the classification of oxides
as acidic, basic, amphoteric or neutral.
SG and UK pH and salt makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "a weak acid is a dilute acid", "all salts are made by titration", "lead(II) chloride
is soluble", "aluminium oxide is only basic", "the Haber process uses a platinum catalyst".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Chemistry", 17
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

sg_ph = src("gen_sg_science_s2_acids_and_alkalis", "g_ph")
uk_salt = src("gen_uk_science_y10_chemical_changes", "g_salt")
uk_acid = keep(src("gen_uk_science_y8_metals_and_non_metals", "g_acid"), lambda it: "nitric" not in it["q"])

ACID = {"hydrochloric acid": ("chloride", "HCl"), "sulfuric acid": ("sulfate", "H₂SO₄"), "nitric acid": ("nitrate", "HNO₃")}
MET = [("magnesium", "magnesium"), ("zinc", "zinc"), ("iron", "iron(II)"), ("calcium", "calcium")]
BASE = [("copper(II) oxide", "copper(II)", "water"), ("magnesium oxide", "magnesium", "water"), ("sodium hydroxide", "sodium", "water"), ("potassium hydroxide", "potassium", "water"),
        ("zinc oxide", "zinc", "water"), ("calcium hydroxide", "calcium", "water")]
CARB = [("calcium carbonate", "calcium"), ("sodium carbonate", "sodium"), ("copper(II) carbonate", "copper(II)"), ("zinc carbonate", "zinc"), ("magnesium carbonate", "magnesium")]


def g_prod():
    acid = R.choice(list(ACID))
    an = ACID[acid][0]
    k = R.choice(["metal", "base", "carb"])
    if k == "metal":
        if acid == "nitric acid":
            return None
        m, c = R.choice(MET)
        a = "%s %s and hydrogen" % (c, an)
        wr = ["%s %s and water" % (c, an), "%s oxide and hydrogen" % c, "%s %s, water and carbon dioxide" % (c, an)]
        return tq("What are the products when %s reacts with %s?" % (m, acid), a, wr, "acid + metal → salt + hydrogen.")
    if k == "base":
        b, c, _ = R.choice(BASE)
        a = "%s %s and water" % (c, an)
        return tq("What are the products when %s reacts with %s?" % (b, acid), a, ["%s %s and hydrogen" % (c, an), "%s %s, water and carbon dioxide" % (c, an), "%s hydroxide and hydrogen" % c],
                  "acid + base → salt + water (neutralisation).")
    b, c = R.choice(CARB)
    if c == "calcium" and acid == "sulfuric acid":
        return None
    a = "%s %s, water and carbon dioxide" % (c, an)
    return tq("What are the products when %s reacts with %s?" % (b, acid), a, ["%s %s and water" % (c, an), "%s %s and hydrogen" % (c, an), "%s oxide and carbon dioxide" % c],
              "acid + carbonate → salt + water + carbon dioxide.")


SALT = [("sodium chloride", "titration of an acid with an alkali (sodium hydroxide)"), ("potassium nitrate", "titration of an acid with an alkali (potassium hydroxide)"),
        ("ammonium sulfate", "titration of an acid with aqueous ammonia"), ("copper(II) sulfate", "adding excess insoluble copper(II) oxide to the acid, then filtering"),
        ("zinc chloride", "adding excess zinc (or zinc oxide) to the acid, then filtering"), ("magnesium sulfate", "adding excess magnesium carbonate to the acid, then filtering"),
        ("barium sulfate", "precipitation: mixing two solutions, such as barium nitrate and sodium sulfate"), ("silver chloride", "precipitation: mixing silver nitrate and sodium chloride solutions"),
        ("lead(II) iodide", "precipitation: mixing lead(II) nitrate and potassium iodide solutions"), ("calcium carbonate", "precipitation: mixing calcium chloride and sodium carbonate solutions")]
g_salt = rows(R, SALT, "Which method is best to prepare a sample of %s?")

SOL = [("sodium chloride", "soluble"), ("potassium sulfate", "soluble"), ("ammonium carbonate", "soluble"), ("copper(II) nitrate", "soluble"), ("zinc chloride", "soluble"),
       ("silver chloride", "insoluble"), ("lead(II) chloride", "insoluble"), ("barium sulfate", "insoluble"), ("calcium sulfate", "insoluble (sparingly soluble)"),
       ("lead(II) sulfate", "insoluble"), ("calcium carbonate", "insoluble"), ("copper(II) carbonate", "insoluble"), ("magnesium sulfate", "soluble"), ("iron(II) nitrate", "soluble")]


def g_sol():
    s, a = R.choice(SOL)
    return tq("Is %s soluble or insoluble in water?" % s, a, [x for x in ("soluble", "insoluble", "insoluble (sparingly soluble)", "soluble only in hot water") if x != a][:3],
              "All Na, K and ammonium salts and all nitrates are soluble; chlorides are soluble except AgCl and PbCl₂; sulfates except BaSO₄, PbSO₄ and CaSO₄; carbonates are insoluble except Na, K and ammonium.")


OX = [("sulfur dioxide", "acidic"), ("carbon dioxide", "acidic"), ("nitrogen dioxide", "acidic"), ("phosphorus(V) oxide", "acidic"),
      ("magnesium oxide", "basic"), ("calcium oxide", "basic"), ("copper(II) oxide", "basic"), ("sodium oxide", "basic"), ("iron(III) oxide", "basic"),
      ("aluminium oxide", "amphoteric"), ("zinc oxide", "amphoteric"), ("lead(II) oxide", "amphoteric"),
      ("carbon monoxide", "neutral"), ("water", "neutral"), ("nitrogen monoxide", "neutral")]


def g_ox():
    o, a = R.choice(OX)
    return tq("How is %s classified?" % o, "a%s %s oxide" % ("n" if a[0] in "aeiou" else "", a), ["a%s %s oxide" % ("n" if x[0] in "aeiou" else "", x) for x in ("acidic", "basic", "amphoteric", "neutral") if x != a],
              "Non-metal oxides are usually acidic (CO and NO are neutral); metal oxides are basic; Al₂O₃, ZnO and PbO are amphoteric (react with both acids and alkalis).")


IND = [("Universal Indicator in a strong acid (pH 1)", "red"), ("Universal Indicator in a neutral solution (pH 7)", "green"), ("Universal Indicator in a strong alkali (pH 14)", "violet (purple)"),
       ("blue litmus paper in an acid", "red"), ("red litmus paper in an alkali", "blue"), ("methyl orange in an acid", "red"), ("methyl orange in an alkali", "yellow"),
       ("phenolphthalein in an alkali", "pink"), ("phenolphthalein in an acid", "colourless"), ("Universal Indicator in a weak acid (pH 5)", "orange-yellow")]
g_ind = rows(R, IND, "What colour is %s?")

STRONG = [("hydrochloric acid", "a strong acid"), ("sulfuric acid", "a strong acid"), ("nitric acid", "a strong acid"), ("ethanoic acid", "a weak acid"),
          ("citric acid", "a weak acid"), ("carbonic acid", "a weak acid"), ("sodium hydroxide", "a strong alkali"), ("potassium hydroxide", "a strong alkali"), ("aqueous ammonia", "a weak alkali")]


def g_strong():
    s, a = R.choice(STRONG)
    return tq("Is %s a strong or a weak acid or alkali?" % s, a, [x for x in ("a strong acid", "a weak acid", "a strong alkali", "a weak alkali") if x != a],
              "Strong acids and alkalis ionise completely in water; weak ones ionise only partially.")


POOL1 = pool(R, [
    ("What is an acid?", "a substance that produces hydrogen ions (H⁺) in water", ["a substance that produces hydroxide ions in water", "any substance that tastes sour", "a substance with pH above 7"], "H⁺ ions make a solution acidic."),
    ("What is an alkali?", "a soluble base that produces hydroxide ions (OH⁻) in water", ["any base", "a substance that produces H⁺ ions", "a salt"], "All alkalis are bases, but not all bases are alkalis."),
    ("What is a base?", "a substance that reacts with an acid to form a salt and water only", ["a substance that produces H⁺ ions", "a substance with pH 7", "any metal"], "Metal oxides and hydroxides are bases."),
    ("Write the ionic equation for neutralisation.", "H⁺(aq) + OH⁻(aq) → H₂O(l)", ["H⁺ + Cl⁻ → HCl", "Na⁺ + OH⁻ → NaOH", "H₂ + O → H₂O"], "The spectator ions do not change."),
    ("What is the difference between a strong acid and a concentrated acid?", "Strong means fully ionised; concentrated means a lot of acid dissolved in a small volume of water.",
     ["They mean the same thing.", "Strong means a lot of acid per dm³.", "Concentrated means fully ionised."], "A dilute strong acid is still strong."),
    ("Why does 0.1 mol/dm³ hydrochloric acid have a lower pH than 0.1 mol/dm³ ethanoic acid?", "Hydrochloric acid is fully ionised, so it has a higher concentration of H⁺ ions.", ["Ethanoic acid is more concentrated.", "Hydrochloric acid has no H⁺ ions.", "pH does not depend on H⁺ ions."], "Lower pH means more H⁺."),
    ("What gas is given off when an acid reacts with a carbonate, and how is it tested?", "carbon dioxide; it turns limewater milky", ["hydrogen; it pops with a lighted splint", "oxygen; it relights a glowing splint", "chlorine; it bleaches damp litmus"], "Carbonate + acid → salt + water + CO₂."),
    ("What gas is given off when a metal reacts with dilute acid, and how is it tested?", "hydrogen; it burns with a 'pop' with a lighted splint", ["carbon dioxide; turns limewater milky", "oxygen; relights a glowing splint", "ammonia; turns red litmus blue"], "Metal + acid → salt + hydrogen."),
    ("Why do farmers add lime (calcium hydroxide) to soil?", "to neutralise acidic soil", ["to make the soil more acidic", "to add nitrogen", "to kill weeds"], "Most crops grow best near pH 7."),
    ("Which ions are present in all alkaline solutions?", "hydroxide ions, OH⁻", ["hydrogen ions, H⁺", "chloride ions, Cl⁻", "sodium ions, Na⁺"], "More OH⁻ means a higher pH."),
])
POOL5 = pool(R, [
    ("What are the conditions used in the Haber process to make ammonia?", "about 450 °C, about 200 atm and an iron catalyst", ["25 °C, 1 atm and no catalyst", "1000 °C and a platinum catalyst", "450 °C and 1 atm only"], "N₂ + 3H₂ ⇌ 2NH₃."),
    ("Why is the Haber process reaction described as reversible?", "Ammonia can break down back into nitrogen and hydrogen under the same conditions.", ["It only goes forward.", "It can be reversed by adding water.", "The catalyst is used up."], "The ⇌ sign shows a reversible reaction."),
    ("Where do the raw materials for the Haber process come from?", "nitrogen from the air and hydrogen from natural gas (methane) and steam", ["nitrogen from water and hydrogen from air", "both from crude oil only", "both from ammonia"], "Unreacted gases are recycled."),
    ("Why is ammonia important?", "It is used to make fertilisers such as ammonium nitrate and ammonium sulfate.", ["It is used as a fuel in cars.", "It is used to make drinking water.", "It is used as a food preservative."], "Fertilisers supply nitrogen to crops."),
    ("Why should an ammonium fertiliser not be mixed with lime (calcium hydroxide)?", "They react and ammonia gas escapes, so nitrogen is lost.", ["The fertiliser becomes acidic.", "Lime makes the soil too wet.", "It makes the fertiliser poisonous."], "Ammonium salt + base → ammonia gas."),
    ("Why is excess copper(II) oxide added when making copper(II) sulfate crystals?", "to make sure all the acid is used up; the extra solid is then filtered off", ["to make more acid", "to speed up crystallisation", "to make the solution colourless"], "Then crystallise the filtrate."),
    ("Why can sodium chloride not be made by adding excess sodium to hydrochloric acid?", "Sodium reacts too violently with acid, so it is unsafe.", ["Sodium does not react with acids.", "Sodium chloride is insoluble.", "Sodium is a non-metal."], "Use titration of NaOH with HCl instead."),
    ("Aluminium oxide reacts with both hydrochloric acid and sodium hydroxide. What does this show?", "It is amphoteric.", ["It is acidic.", "It is basic.", "It is neutral."], "Zinc oxide behaves the same way."),
    ("How is an insoluble salt such as barium sulfate obtained after precipitation?", "Filter the mixture, wash the residue with distilled water and dry it.", ["Evaporate the mixture to dryness.", "Crystallise the filtrate.", "Distil the mixture."], "The salt is the residue."),
    ("Which oxide dissolves in water to form an acidic solution?", "sulfur dioxide", ["calcium oxide", "sodium oxide", "carbon monoxide"], "SO₂ forms sulfurous acid; it causes acid rain."),
])


def main():
    sets = U.sets([
        ("Acids, alkalis and pH", [POOL1, (g_ind, 6), (sg_ph, 4), (g_strong, 3)]),
        ("Reactions of acids", [(g_prod, 10), (uk_acid, 4), (uk_salt, 3), POOL1]),
        ("Strong and weak; oxides", [(g_strong, 5), (g_ox, 9), POOL1, (POOL5, 2)]),
        ("Preparing salts", [(g_salt, 8), (g_sol, 8), (POOL5, 4)]),
        ("Ammonia and exam-style questions", [(POOL5, 8), (g_prod, 4), (g_salt, 3), (g_sol, 3), (g_ox, 2)]),
    ])
    make_ol(LV, SUBJ, "acid-base-chemistry", SORT, "Acid-Base Chemistry",
            "Describe acids in terms of hydrogen ions and alkalis in terms of hydroxide ions; describe the pH scale and the use of Universal Indicator; distinguish between "
            "strong and weak acids and alkalis; describe neutralisation as H⁺ + OH⁻ → H₂O and the reactions of acids with metals, bases and carbonates; describe the "
            "preparation, separation and purification of salts using the solubility rules; describe the manufacture of ammonia by the Haber process and the idea of a "
            "reversible reaction; classify oxides as acidic, basic, amphoteric or neutral (summary of the Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Acid-Base Chemistry", "Acids and bases",
            "Free Secondary 3 O-Level Chemistry worksheets on acid-base chemistry: acids and alkalis, pH and indicators, strong and weak acids, neutralisation, preparing salts, "
            "solubility rules, the Haber process and types of oxides. 100 questions with answers.",
            "Acids give H⁺; alkalis give OH⁻.", "Choose the salt method from the solubility rules.",
            "<p><b>Acids produce H⁺ ions in water; alkalis produce OH⁻ ions.</b></p><ul>"
            "<li>pH below 7 acidic, 7 neutral, above 7 alkaline. Strong acids and alkalis ionise completely.</li>"
            "<li>acid + metal → salt + hydrogen; acid + base → salt + water; acid + carbonate → salt + water + carbon dioxide.</li>"
            "<li>Salts: titration (Na, K, ammonium salts), excess insoluble solid then filter (other soluble salts), precipitation (insoluble salts).</li>"
            "<li>Oxides: non-metal oxides acidic, metal oxides basic, Al₂O₃ and ZnO amphoteric, CO and NO neutral. Haber process: N₂ + 3H₂ ⇌ 2NH₃, 450 °C, 200 atm, iron catalyst.</li></ul>",
            [("How do you make zinc sulfate crystals?", ["add excess zinc oxide to dilute sulfuric acid", "filter", "heat to saturation and cool"], "crystallisation"),
             ("How do you make lead(II) chloride?", ["it is insoluble", "mix lead(II) nitrate and sodium chloride solutions", "filter, wash, dry"], "precipitation")],
            ["Using 'weak' to mean 'dilute'.", "Making every salt by titration.", "Thinking lead(II) chloride and silver chloride are soluble.",
             "Thinking all metal oxides are only basic: Al₂O₃ and ZnO are amphoteric."],
            [("How do you choose a method to make a salt?", "If the salt is insoluble, use precipitation. If it is a soluble sodium, potassium or ammonium salt, use titration. For other soluble salts, add an excess of the insoluble metal, base or carbonate to the acid and filter."),
             ("What is the difference between a strong acid and a weak acid?", "A strong acid ionises completely in water to give H⁺ ions; a weak acid ionises only partially, so it has fewer H⁺ ions at the same concentration."),
             ("What conditions are used in the Haber process?", "About 450 °C, a pressure of about 200 atmospheres and an iron catalyst, with unreacted nitrogen and hydrogen recycled.")],
            sets)


if __name__ == "__main__":
    main()
