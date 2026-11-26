# -*- coding: utf-8 -*-
"""
UK Year 11 science (KS4, GCSE Combined Science Chemistry): Organic Chemistry
  python tools/gen_uk_science_y11_organic_chemistry.py
Crude oil as a mixture of hydrocarbons, alkanes (CnH2n+2) and their names, fractional distillation and the uses of
fractions, how boiling point, viscosity and flammability depend on chain length, complete combustion, cracking to
make smaller alkanes and alkenes (CnH2n), and the bromine water test.
Wrong answers come from real mistakes: "longer chains are more flammable", "alkenes are saturated", "cracking joins
small molecules", "bromine water turns colourless with alkanes".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62106)
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
ALK = ["methane", "ethane", "propane", "butane", "pentane", "hexane"]
ENE = {2: "ethene", 3: "propene", 4: "butene", 5: "pentene"}


def f(c, h):
    return ("C%s" % (c if c > 1 else "")).translate(SUB) + ("H%d" % h).translate(SUB)


def g_formula():
    n = R.randrange(1, 7)
    k = R.choice(["formula", "name", "h"])
    if not once(("fo", n, k)):
        return None
    if k == "formula":
        a = f(n, 2 * n + 2)
        return item("What is the formula of %s?" % ALK[n - 1], a, [f(n, 2 * n), f(n, 2 * n + 1), f(n + 1, 2 * n + 2)] if n > 1 else [f(1, 2), f(1, 3), f(2, 4)],
                    "Alkanes are CₙH₂ₙ₊₂.")
    if k == "name":
        return item("Which alkane has the formula %s?" % f(n, 2 * n + 2), ALK[n - 1], R.sample([x for x in ALK if x != ALK[n - 1]], 3), "Meth 1, eth 2, prop 3, but 4, pent 5, hex 6.")
    m = R.choice([7, 8, 10, 12, 16, 20])
    if not once(("foh", m)):
        return None
    return item("An alkane has %d carbon atoms. How many hydrogen atoms does it have?" % m, str(2 * m + 2), [str(2 * m), str(2 * m + 1), str(m + 2)], "2 × %d + 2 = %d." % (m, 2 * m + 2))


def g_prop():
    a, b = sorted(R.sample(range(1, 7), 2))
    k = R.choice(["bp", "visc", "flam"])
    if not once(("pr", a, b, k)):
        return None
    q = {"bp": "has the higher boiling point", "visc": "is more viscous", "flam": "is more flammable"}[k]
    ans = ALK[b - 1] if k != "flam" else ALK[a - 1]
    oth = ALK[a - 1] if ans == ALK[b - 1] else ALK[b - 1]
    return item("Which %s: %s or %s?" % (q.replace("has", "alkane has").replace("is ", "alkane is ", 1), ALK[a - 1], ALK[b - 1]), ans, [oth, "they are the same", "it depends on the amount"],
                "Longer chains: higher boiling point, more viscous, less flammable.")


FR = [("refinery gases (LPG)", "bottled gas for heating and cooking"), ("petrol", "fuel for cars"), ("kerosene", "fuel for aircraft"),
      ("diesel oil", "fuel for lorries and trains"), ("heavy fuel oil", "fuel for ships and power stations"), ("bitumen", "surfacing roads and roofs")]


def g_use():
    fr, use = R.choice(FR)
    k = R.choice(["use", "fr"])
    if not once(("fu", fr, k)):
        return None
    if k == "use":
        return item("What %s %s used for?" % ("are" if "gases" in fr else "is", fr), use, R.sample([x[1] for x in FR if x[0] != fr], 3), "Each fraction has molecules of similar chain length.")
    return item("Which fraction of crude oil is used for %s?" % use, fr, R.sample([x[0] for x in FR if x[0] != fr], 3), "Bitumen has the longest chains; refinery gases the shortest.")


def g_comb():
    n = R.randrange(1, 11)
    k = R.choice(["co2", "h2o"])
    if not once(("cb", n, k)):
        return None
    name = ALK[n - 1] if n <= 6 else "an alkane with %d carbon atoms" % n
    a = n if k == "co2" else n + 1
    wh = "carbon dioxide" if k == "co2" else "water"
    return item("One molecule of %s (%s) burns completely. How many molecules of %s are made?" % (name, f(n, 2 * n + 2), wh), str(a),
                [str(x) for x in [n + 1 if k == "co2" else n, 2 * n + 2, 2 * n] if x != a][:3] + ([str(a + 3)] if len({n + 1 if k == "co2" else n, 2 * n + 2, 2 * n} - {a}) < 3 else []),
                "Carbon → CO₂ (%d), hydrogen → H₂O (%d)." % (n, n + 1))


def g_crack():
    n = R.choice([8, 9, 10, 11, 12, 14, 16])
    m = R.choice(range(3, n - 1))
    e = n - m
    if e > 5 or not once(("ck", n, m)):
        return None
    k = R.choice(["ene", "ane"])
    big = f(n, 2 * n + 2)
    if k == "ene":
        a = f(e, 2 * e)
        return item("Cracking: %s → %s + ?. What is the missing product?" % (big, f(m, 2 * m + 2)), a, [f(e, 2 * e + 2), f(e, 2 * e - 2), f(e + 1, 2 * e)],
                    "Atoms are conserved: C%d − C%d = C%d, H%d − H%d = H%d (an alkene)." % (n, m, e, 2 * n + 2, 2 * m + 2, 2 * e))
    a = f(m, 2 * m + 2)
    return item("Cracking: %s → ? + %s (%s). What is the missing product?" % (big, f(e, 2 * e), ENE[e]), a, [f(m, 2 * m), f(m + 1, 2 * m + 2), f(m, 2 * m + 4)],
                "Atoms are conserved: the other product is an alkane, C%dH%d." % (m, 2 * m + 2))


def g_test():
    c = R.randrange(2, 7)
    ene = R.random() < 0.5
    k = R.choice(["type", "bw"])
    if not once(("tt", c, ene, k)):
        return None
    fo = f(c, 2 * c) if ene else f(c, 2 * c + 2)
    if k == "type":
        return item("Is %s an alkane or an alkene?" % fo, "an alkene" if ene else "an alkane", ["an alkane" if ene else "an alkene", "a polymer", "an element"],
                    "Alkanes CₙH₂ₙ₊₂; alkenes CₙH₂ₙ.")
    return item("Bromine water is shaken with %s. What do you see?" % fo, "It turns from orange to colourless." if ene else "It stays orange.",
                ["It stays orange." if ene else "It turns from orange to colourless.", "It turns blue.", "It turns milky."], "Alkenes decolourise bromine water; alkanes do not.")


B1 = bank([
    ("What is crude oil?", "a mixture of mainly hydrocarbons formed from ancient plankton", ["a pure compound", "a renewable fuel", "a mixture of metals"], "Formed over millions of years."),
    ("What is a hydrocarbon?", "a compound of hydrogen and carbon only", ["a compound of hydrogen and oxygen", "any fuel", "an element"], "Alkanes and alkenes are hydrocarbons."),
    ("Why are alkanes called saturated?", "They have only single carbon–carbon bonds.", ["They contain water.", "They have a double bond.", "They are liquids."], "Alkenes have a C=C double bond."),
])
B2 = bank([
    ("How does fractional distillation separate crude oil?", "Fractions with different boiling points condense at different heights.", ["By filtering.", "By magnetism.", "By colour."], "The column is hotter at the bottom."),
    ("Where do fractions with the shortest chains leave the column?", "at the top", ["at the bottom", "in the middle", "they stay as liquid"], "Low boiling points."),
])
B4 = bank([
    ("Why is cracking useful?", "It turns long-chain fractions into smaller, more useful fuels and alkenes.", ["It makes crude oil.", "It joins small molecules.", "It removes all carbon."], "There is more demand for petrol than for heavy oils."),
    ("What are alkenes used for?", "making polymers and other chemicals", ["only as fuels for ships", "making crude oil", "making bitumen"], "For example, poly(ethene)."),
    ("Name two ways to crack hydrocarbons.", "catalytic cracking and steam cracking", ["filtering and distilling", "freezing and melting", "burning and cooling"], "High temperature, catalyst or steam."),
])

if __name__ == "__main__":
  build(U, 11, "organic-chemistry", 6, "Chemistry", "Organic chemistry",
      "Crude oil, hydrocarbons and alkanes; fractional distillation and petrochemicals; properties of hydrocarbons (boiling point, viscosity, flammability) and complete combustion; cracking and alkenes; the test for alkenes with bromine water.",
      "Organic Chemistry", "Organic Chemistry",
      "Free Year 11 GCSE Combined Science worksheets on organic chemistry: crude oil, alkanes, fractional distillation, chain length and properties, combustion, cracking, alkenes and bromine water. 100 questions with answers.",
      "Alkanes are CₙH₂ₙ₊₂; alkenes are CₙH₂ₙ.",
      "Longer chains: higher boiling point, less flammable.",
      "<p><b>Crude oil is a mixture of hydrocarbons separated by boiling point.</b></p><ul><li>Alkanes: methane CH₄, ethane C₂H₆, propane C₃H₈, butane C₄H₁₀.</li>"
      "<li>Longer chains have higher boiling points, are more viscous and less flammable.</li>"
      "<li>Cracking breaks long alkanes into shorter alkanes and alkenes. Alkenes turn bromine water from orange to colourless.</li></ul>",
      [("Formula of an alkane with 5 carbons?", ["2 × 5 + 2 = 12"], "C₅H₁₂"), ("C₁₀H₂₂ → C₈H₁₈ + ?", ["C: 10 − 8 = 2", "H: 22 − 18 = 4"], "C₂H₄")],
      ["Thinking longer chains are more flammable.", "Thinking alkenes are saturated.", "Thinking bromine water goes colourless with alkanes."],
      [("What is the general formula of the alkanes?", "CₙH₂ₙ₊₂. For example, propane has 3 carbons and 8 hydrogens: C₃H₈."),
       ("What happens in cracking?", "Long-chain hydrocarbons are heated (with a catalyst or steam) and break into shorter alkanes and alkenes."),
       ("How do you test for an alkene?", "Shake it with bromine water. An alkene turns it from orange to colourless; an alkane leaves it orange.")],
      [("Hydrocarbons and alkanes", B1 + [(g_formula, 12), (g_test, 5)]),
       ("Fractional distillation", B2 + [(g_use, 10), (g_prop, 8)]),
       ("Properties and combustion", [(g_prop, 10), (g_comb, 10)]),
       ("Cracking", B4 + [(g_crack, 16), (g_formula, 1)]),
       ("Alkenes", [(g_test, 11), (g_crack, 6), (g_comb, 3)])])
