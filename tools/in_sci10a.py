# -*- coding: utf-8 -*-
"""Class 10 Science, Unit I Chemical Substances – Nature and Behaviour: NCERT chapters 1–4 (question makers)."""
import random
from fractions import Fraction as F
from sci_chem import split_eq, tally, eq_html, sub
from uk_alsci import nf, nq, tq, once_maker
from in_sci import pairs, name, _R

R = random.Random(0)


def ch(xs):
    return _R[0].choice(xs)


# =================================================================== Chapter 1: chemical reactions and equations
EQ1 = [("2H2 + O2 -> 2H2O", "hydrogen burns in oxygen"), ("2Mg + O2 -> 2MgO", "magnesium ribbon burns in air"), ("3Fe + 4H2O -> Fe3O4 + 4H2", "iron reacts with steam"),
       ("CaO + H2O -> Ca(OH)2", "quicklime reacts with water"), ("CaCO3 -> CaO + CO2", "limestone is heated"), ("2FeSO4 -> Fe2O3 + SO2 + SO3", "ferrous sulphate crystals are heated"),
       ("2Pb(NO3)2 -> 2PbO + 4NO2 + O2", "lead nitrate is heated"), ("2H2O -> 2H2 + O2", "water is electrolysed"), ("2AgCl -> 2Ag + Cl2", "silver chloride is left in sunlight"),
       ("2AgBr -> 2Ag + Br2", "silver bromide is left in sunlight"), ("Fe + CuSO4 -> FeSO4 + Cu", "an iron nail is dipped in copper sulphate solution"),
       ("Zn + CuSO4 -> ZnSO4 + Cu", "zinc is added to copper sulphate solution"), ("Pb + CuCl2 -> PbCl2 + Cu", "lead is added to copper chloride solution"),
       ("Na2SO4 + BaCl2 -> BaSO4 + 2NaCl", "sodium sulphate and barium chloride solutions are mixed"), ("2Cu + O2 -> 2CuO", "copper powder is heated in air"),
       ("CuO + H2 -> Cu + H2O", "hydrogen is passed over hot copper oxide"), ("ZnO + C -> Zn + CO", "zinc oxide is heated with carbon"), ("MnO2 + 4HCl -> MnCl2 + 2H2O + Cl2", "manganese dioxide reacts with hydrochloric acid"),
       ("Zn + H2SO4 -> ZnSO4 + H2", "zinc granules react with dilute sulphuric acid"), ("CH4 + 2O2 -> CO2 + 2H2O", "methane (natural gas) burns"), ("C6H12O6 + 6O2 -> 6CO2 + 6H2O", "glucose is respired in cells"),
       ("2Na + 2H2O -> 2NaOH + H2", "sodium reacts with water"), ("4Na + O2 -> 2Na2O", "sodium reacts with oxygen"), ("2Al + Fe2O3 -> Al2O3 + 2Fe", "aluminium reacts with iron(III) oxide (thermit reaction)"),
       ("Fe2O3 + 2Al -> 2Fe + Al2O3", "iron oxide is reduced by aluminium"), ("NaOH + HCl -> NaCl + H2O", "sodium hydroxide neutralises hydrochloric acid"), ("2KClO3 -> 2KCl + 3O2", "potassium chlorate is heated"),
       ("N2 + 3H2 -> 2NH3", "ammonia is made from nitrogen and hydrogen"), ("2SO2 + O2 -> 2SO3", "sulphur dioxide is oxidised"), ("C + O2 -> CO2", "coal burns")]


def c_balance(k=None):
    eq, what = ch(EQ1)
    L, Rr = split_eq(eq)
    assert tally(L) == tally(Rr), eq
    sp = L + Rr
    if all(c == 1 for c, _ in sp):
        return None
    k = k or ch(["coef", "coef", "set"])
    skel = " + ".join("_ " + sub(f) for _, f in L) + " → " + " + ".join("_ " + sub(f) for _, f in Rr)
    if k == "set":
        a = ", ".join(str(c) for c, _ in sp)
        R2 = _R[0]
        wr = set()
        for _ in range(30):
            w = [c for c, _ in sp]
            i = R2.randrange(len(w))
            w[i] = max(1, w[i] + R2.choice([-1, 1, 2]))
            wr.add(", ".join(str(x) for x in w))
        wr.discard(a)
        wr.add(", ".join("1" for _ in sp))
        wr.discard(a)
        return tq("When %s, the reaction is %s. Which coefficients (in order) balance it?" % (what, skel), a, R2.sample(sorted(wr), min(3, len(wr))), "Balanced: %s. Count each atom on both sides." % eq_html(L, Rr))
    c, f = ch(sp)
    others = sorted({x for x in [1, 2, 3, 4, 5, 6, 7] if x != c})
    return tq("Balance the equation for the reaction when %s: %s. What is the coefficient of %s?" % (what, skel, sub(f)), str(c), [str(x) for x in _R[0].sample(others, 3)],
              "Balanced equation: %s." % eq_html(L, Rr))


TYPES = [("CaO + H₂O → Ca(OH)₂", "combination"), ("2Mg + O₂ → 2MgO", "combination"), ("C + O₂ → CO₂", "combination"), ("2H₂ + O₂ → 2H₂O", "combination"),
         ("NH₃ + HCl → NH₄Cl", "combination"), ("2CO + O₂ → 2CO₂", "combination"), ("N₂ + 3H₂ → 2NH₃", "combination"),
         ("CaCO₃ → CaO + CO₂ (on heating)", "decomposition"), ("2FeSO₄ → Fe₂O₃ + SO₂ + SO₃ (on heating)", "decomposition"), ("2Pb(NO₃)₂ → 2PbO + 4NO₂ + O₂", "decomposition"),
         ("2H₂O → 2H₂ + O₂ (electrolysis)", "decomposition"), ("2AgCl → 2Ag + Cl₂ (in sunlight)", "decomposition"), ("2AgBr → 2Ag + Br₂ (in sunlight)", "decomposition"), ("2KClO₃ → 2KCl + 3O₂", "decomposition"),
         ("2H₂O₂ → 2H₂O + O₂", "decomposition"), ("Fe + CuSO₄ → FeSO₄ + Cu", "displacement"), ("Zn + CuSO₄ → ZnSO₄ + Cu", "displacement"), ("Pb + CuCl₂ → PbCl₂ + Cu", "displacement"),
         ("Zn + 2HCl → ZnCl₂ + H₂", "displacement"), ("Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag", "displacement"), ("Mg + 2HCl → MgCl₂ + H₂", "displacement"), ("2Na + 2H₂O → 2NaOH + H₂", "displacement"),
         ("Na₂SO₄ + BaCl₂ → BaSO₄ + 2NaCl", "double displacement"), ("NaOH + HCl → NaCl + H₂O", "double displacement"), ("AgNO₃ + NaCl → AgCl + NaNO₃", "double displacement"),
         ("Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃", "double displacement"), ("CuSO₄ + 2NaOH → Cu(OH)₂ + Na₂SO₄", "double displacement"), ("BaCl₂ + H₂SO₄ → BaSO₄ + 2HCl", "double displacement"),
         ("2Cu + O₂ → 2CuO (on heating)", "combination"), ("2NaCl → 2Na + Cl₂ (electrolysis of molten salt)", "decomposition"), ("Fe₂O₃ + 2Al → 2Fe + Al₂O₃", "displacement"),
         ("KOH + HNO₃ → KNO₃ + H₂O", "double displacement"), ("2Al + 3CuCl₂ → 2AlCl₃ + 3Cu", "displacement"), ("CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂", "double displacement")]
TYPE_E = {"combination": "Two or more reactants form a single product.", "decomposition": "A single reactant breaks down into simpler products.",
          "displacement": "A more reactive element pushes a less reactive one out of its compound.", "double displacement": "Two compounds exchange ions; often a precipitate or water forms."}


def c_type(k=None):
    eq, t = ch(TYPES)
    return tq("What type of reaction is %s?" % eq, t, [x for x in ["combination", "decomposition", "displacement", "double displacement"] if x != t], TYPE_E[t])


REDOX = [("CuO + H₂ → Cu + H₂O", "H₂", "CuO"), ("ZnO + C → Zn + CO", "C", "ZnO"), ("MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂", "HCl", "MnO₂"), ("Fe₂O₃ + 2Al → 2Fe + Al₂O₃", "Al", "Fe₂O₃"),
         ("Fe₂O₃ + 3CO → 2Fe + 3CO₂", "CO", "Fe₂O₃"), ("PbO + C → Pb + CO", "C", "PbO"), ("2Cu + O₂ → 2CuO", "Cu", "O₂"), ("2Mg + O₂ → 2MgO", "Mg", "O₂"),
         ("H₂S + Cl₂ → 2HCl + S", "H₂S", "Cl₂"), ("CuO + C → Cu + CO", "C", "CuO"), ("2H₂S + SO₂ → 3S + 2H₂O", "H₂S", "SO₂"), ("4Na + O₂ → 2Na₂O", "Na", "O₂"),
         ("ZnO + CO → Zn + CO₂", "CO", "ZnO"), ("2Fe + 3Cl₂ → 2FeCl₃", "Fe", "Cl₂")]


def c_redox(k=None):
    eq, red, ox = ch(REDOX)
    k = k or ch(["oxd", "red", "oa", "ra"])
    sp = sorted({p.strip().split(" ")[0].lstrip("0123456789") for side in eq.split(" → ") for p in side.split(" + ")})
    q = {"oxd": "Which substance is oxidised in %s?", "red": "Which substance is reduced in %s?", "oa": "Which substance is the oxidising agent in %s?", "ra": "Which substance is the reducing agent in %s?"}[k] % eq
    a = red if k in ("oxd", "ra") else ox
    wr = [x for x in sp if x != a]
    if len(wr) < 3:
        wr += ["none of them"]
    return tq(q, a, wr, "%s gains oxygen or loses hydrogen, so it is oxidised (the reducing agent); %s loses oxygen or gains hydrogen, so it is reduced (the oxidising agent)." % (red, ox))


OBS1 = [("What is seen when magnesium ribbon burns in air?", "a dazzling white flame and a white powder (magnesium oxide)", ["a blue flame and a black powder", "a green flame and no product", "a red flame and a brown gas"], "2Mg + O₂ → 2MgO."),
        ("Why is magnesium ribbon cleaned with sandpaper before burning?", "to remove the layer of magnesium oxide on its surface", ["to make it heavier", "to add oxygen to it", "to stop it from burning"], "The oxide layer slows the reaction."),
        ("What colour is the precipitate when lead nitrate solution is added to potassium iodide?", "yellow (lead iodide)", ["white", "blue", "green"], "Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃."),
        ("What happens to the colour of copper sulphate solution when an iron nail is dipped in it?", "it changes from blue to light green", ["it changes from green to blue", "it turns colourless at once", "it turns red"], "Iron displaces copper; FeSO₄ is pale green."),
        ("What is seen on the iron nail left in copper sulphate solution?", "a brownish coating of copper", ["a white coating of salt", "black rust", "no change"], "Iron is more reactive than copper."),
        ("What is the colour change when ferrous sulphate crystals are heated?", "green crystals turn to a reddish-brown solid with a smell of burning sulphur", ["white to blue", "blue to white", "black to green"], "2FeSO₄ → Fe₂O₃ + SO₂ + SO₃."),
        ("What colour gas is given off when lead nitrate is heated?", "brown (nitrogen dioxide)", ["green", "colourless only", "violet"], "NO₂ is a brown gas."),
        ("Why is silver chloride kept in dark coloured bottles?", "light decomposes it into silver and chlorine", ["it reacts with glass", "it absorbs water", "it turns into gold"], "This photolytic decomposition is used in black and white photography."),
        ("Why does a chips packet contain nitrogen gas?", "to prevent the oil from becoming rancid by oxidation", ["to make the chips heavier", "to add flavour", "to keep insects in"], "Nitrogen is unreactive."),
        ("What is rancidity?", "oxidation of fats and oils in food, changing smell and taste", ["rusting of iron", "melting of butter", "freezing of oil"], "Antioxidants and air-tight containers slow it."),
        ("What is corrosion?", "the slow attack of a metal by air, water or chemicals around it", ["the melting of a metal", "the shining of a metal", "the making of an alloy"], "Rusting of iron is an example."),
        ("Which coating forms on copper left in moist air?", "a green coating (basic copper carbonate)", ["a reddish-brown coating", "a black coating of silver sulphide", "a white coating"], "Silver gets a black coating instead."),
        ("Why is respiration called an exothermic reaction?", "energy is released when glucose is oxidised", ["energy is taken in from the surroundings", "it needs sunlight", "it produces ice"], "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy."),
        ("Why is decomposition of calcium carbonate an endothermic reaction?", "heat must be supplied to break it down", ["it gives out heat", "it needs light only", "it happens at room temperature"], "CaCO₃ → CaO + CO₂ on heating."),
        ("What is formed when quicklime reacts with water?", "slaked lime, with a lot of heat", ["limestone and cold water", "sodium hydroxide", "chalk powder"], "CaO + H₂O → Ca(OH)₂ + heat; used for whitewashing."),
        ("Why does a whitewash become shiny after two or three days?", "calcium hydroxide reacts with carbon dioxide to form calcium carbonate", ["the water evaporates and leaves salt", "the lime melts", "the wall absorbs oxygen"], "Ca(OH)₂ + CO₂ → CaCO₃ + H₂O."),
        ("Which gas is collected at the cathode in the electrolysis of water?", "hydrogen, twice the volume of oxygen", ["oxygen, twice the volume of hydrogen", "chlorine", "carbon dioxide"], "2H₂O → 2H₂ + O₂."),
        ("What is a precipitate?", "an insoluble solid formed in a reaction in solution", ["a gas given off", "a coloured solution", "a liquid that boils"], "BaSO₄ is a white precipitate."),
        ("Why must a chemical equation be balanced?", "mass is conserved: atoms are not created or destroyed", ["to make it look neat", "to show the colour change", "to show the heat"], "The law of conservation of mass."),
        ("Which of these is a physical state symbol for a solution in water?", "(aq)", ["(s)", "(l)", "(g)"], "aq means aqueous."),
        ("Which change shows that a chemical reaction has happened?", "a gas is given off and the temperature changes", ["the substance is cut into pieces", "ice melts", "sugar dissolves and can be recovered"], "Other signs: colour change, precipitate."),
        ("Why are food items stored in airtight containers?", "to slow down oxidation (rancidity)", ["to keep them warm", "to add oxygen", "to make them crisp"], "Less air means less oxidation."),
        ("What is the effect of painting iron gates?", "it stops air and water reaching the iron, preventing rusting", ["it makes iron rust faster", "it makes iron magnetic", "it turns iron into steel"], "Galvanising and oiling also protect iron."),
        ("What is an exothermic reaction?", "a reaction that gives out heat", ["a reaction that takes in heat", "a reaction that needs light", "a reaction with no energy change"], "Burning of natural gas is exothermic."),
        ("Why does a test tube become warm when quicklime is added to water?", "the reaction is exothermic", ["the reaction is endothermic", "water is boiling", "a gas is absorbed"], "Heat is released."),
        ("Which reaction is used in black and white photography?", "decomposition of silver bromide by light", ["burning of magnesium", "rusting of iron", "neutralisation"], "2AgBr → 2Ag + Br₂."),
        ("What does the arrow in a chemical equation mean?", "'reacts to form' or 'gives'", ["'is equal to'", "'is heated'", "'is dissolved'"], "Reactants are on the left, products on the right.")]


# =================================================================== Chapter 2: acids, bases and salts
PH = [("lemon juice", 2.2), ("vinegar", 2.8), ("tomato juice", 4.2), ("black coffee", 5.0), ("milk", 6.5), ("pure water", 7.0), ("human blood", 7.4), ("sea water", 8.0),
      ("baking soda solution", 8.3), ("milk of magnesia", 10.5), ("household ammonia", 11.6), ("sodium hydroxide solution", 13.8), ("gastric juice", 1.2), ("rain water (slightly acidic)", 5.6),
      ("soap solution", 10.0), ("lime water", 12.4), ("toothpaste", 9.0), ("orange juice", 3.5), ("saliva before a meal", 7.0), ("hydrochloric acid (dilute)", 1.0)]


def c_ph(k=None):
    k = k or ch(["class", "num", "colour", "comp"])
    if k == "num":
        v = ch([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        a = "strongly acidic" if v <= 3 else "weakly acidic" if v < 7 else "neutral" if v == 7 else "weakly basic" if v <= 10 else "strongly basic"
        return tq("A solution has a pH of %d. How would you describe it?" % v, a, _R[0].sample([x for x in ["strongly acidic", "weakly acidic", "neutral", "weakly basic", "strongly basic"] if x != a], 3),
                  "Below 7 is acidic (lower = stronger), 7 is neutral, above 7 is basic (higher = stronger).")
    if k == "colour":
        v = ch([1, 2, 3, 5, 7, 9, 11, 13])
        col = {1: "red", 2: "red", 3: "orange", 5: "yellow", 7: "green", 9: "blue", 11: "indigo", 13: "violet"}[v]
        return tq("What colour does universal indicator turn in a solution of pH %d?" % v, col, [c for c in ["red", "orange", "yellow", "green", "blue", "violet"] if c != col and abs(["red", "orange", "yellow", "green", "blue", "indigo", "violet"].index(c) - ["red", "orange", "yellow", "green", "blue", "indigo", "violet"].index(col)) > 1][:3],
                  "Universal indicator runs from red (strong acid) through green (neutral) to violet (strong base).")
    if k == "comp":
        (a, x), (b, y) = _R[0].sample(PH, 2)
        if x == y:
            return None
        hi = a if x < y else b
        return tq("Which is more acidic: %s or %s?" % (a, b), hi, [b if hi == a else a, "both are equally acidic", "neither is acidic"],
                  "%s has pH about %s and %s about %s. Lower pH means more acidic." % (a.capitalize(), nf(x, 2), b, nf(y, 2)))
    s, v = ch(PH)
    a = "acidic" if v < 7 else "neutral" if v == 7 else "basic"
    return tq("Is %s (pH about %s) acidic, basic or neutral?" % (s, nf(v, 2)), a, [x for x in ["acidic", "basic", "neutral", "it cannot be said from pH"] if x != a], "pH below 7: acidic; 7: neutral; above 7: basic.")


IND = [("blue litmus in an acid", "turns red"), ("red litmus in a base", "turns blue"), ("phenolphthalein in a base", "turns pink"), ("phenolphthalein in an acid", "stays colourless"),
       ("methyl orange in an acid", "turns red"), ("methyl orange in a base", "turns yellow"), ("red litmus in an acid", "stays red"), ("blue litmus in a base", "stays blue")]
SALT = [("baking soda", "NaHCO₃", "sodium hydrogencarbonate", "cooking, antacids and soda-acid fire extinguishers"),
        ("washing soda", "Na₂CO₃·10H₂O", "sodium carbonate decahydrate", "removing permanent hardness of water and in the glass and soap industries"),
        ("bleaching powder", "CaOCl₂", "calcium oxychloride", "bleaching cotton and disinfecting drinking water"),
        ("plaster of Paris", "CaSO₄·½H₂O", "calcium sulphate hemihydrate", "plaster for fractured bones, toys and decorations"),
        ("gypsum", "CaSO₄·2H₂O", "calcium sulphate dihydrate", "making plaster of Paris"), ("common salt", "NaCl", "sodium chloride", "making caustic soda, bleaching powder and baking soda"),
        ("caustic soda", "NaOH", "sodium hydroxide", "making soaps and detergents"), ("blue vitriol", "CuSO₄·5H₂O", "copper sulphate pentahydrate", "showing water of crystallisation (blue crystals)"),
        ("slaked lime", "Ca(OH)₂", "calcium hydroxide", "whitewashing walls"), ("quicklime", "CaO", "calcium oxide", "making slaked lime and treating acidic soil"),
        ("limestone", "CaCO₃", "calcium carbonate", "making cement and quicklime")]
NEUT = [("hydrochloric acid", "sodium hydroxide", "sodium chloride"), ("sulphuric acid", "sodium hydroxide", "sodium sulphate"), ("nitric acid", "potassium hydroxide", "potassium nitrate"),
        ("hydrochloric acid", "calcium hydroxide", "calcium chloride"), ("sulphuric acid", "copper oxide", "copper sulphate"), ("nitric acid", "sodium hydroxide", "sodium nitrate"),
        ("hydrochloric acid", "magnesium hydroxide", "magnesium chloride"), ("sulphuric acid", "zinc oxide", "zinc sulphate"), ("hydrochloric acid", "ammonium hydroxide", "ammonium chloride"),
        ("nitric acid", "calcium hydroxide", "calcium nitrate"), ("sulphuric acid", "potassium hydroxide", "potassium sulphate"), ("hydrochloric acid", "zinc oxide", "zinc chloride"),
        ("acetic acid", "sodium hydroxide", "sodium acetate"), ("nitric acid", "copper oxide", "copper nitrate"),
        ("hydrochloric acid", "potassium hydroxide", "potassium chloride"), ("sulphuric acid", "magnesium oxide", "magnesium sulphate"), ("nitric acid", "magnesium hydroxide", "magnesium nitrate"),
        ("hydrochloric acid", "copper oxide", "copper chloride"), ("sulphuric acid", "calcium hydroxide", "calcium sulphate"), ("nitric acid", "zinc oxide", "zinc nitrate"),
        ("acetic acid", "potassium hydroxide", "potassium acetate"), ("sulphuric acid", "ammonium hydroxide", "ammonium sulphate")]
GAS = [("zinc", "dilute sulphuric acid", "hydrogen", "burns with a pop sound"), ("sodium carbonate", "dilute hydrochloric acid", "carbon dioxide", "turns lime water milky"),
       ("sodium hydrogencarbonate", "dilute hydrochloric acid", "carbon dioxide", "turns lime water milky"), ("magnesium", "dilute hydrochloric acid", "hydrogen", "burns with a pop sound"),
       ("calcium carbonate (marble)", "dilute hydrochloric acid", "carbon dioxide", "turns lime water milky"), ("zinc", "sodium hydroxide solution (heated)", "hydrogen", "burns with a pop sound"),
       ("iron filings", "dilute sulphuric acid", "hydrogen", "burns with a pop sound"), ("aluminium", "sodium hydroxide solution", "hydrogen", "burns with a pop sound")]


def c_salt(k=None):
    k = k or ch(["name", "use", "formula", "neut", "gas", "ind"])
    if k == "neut":
        a, b, s = ch(NEUT)
        return tq("Which salt is formed when %s reacts with %s?" % (a, b), s, sorted({x[2] for x in NEUT if x[2] != s and (x[0] == a or x[1] == b)} | {"water only"})[:3] if len({x[2] for x in NEUT if x[2] != s and (x[0] == a or x[1] == b)}) >= 2 else _R[0].sample(sorted({x[2] for x in NEUT if x[2] != s}), 3),
                  "Acid + base → salt + water. The metal comes from the base and the non-metal part from the acid.")
    if k == "gas":
        m, acid, g, test = ch(GAS)
        return tq("Which gas is given off when %s reacts with %s?" % (m, acid), "%s, which %s" % (g, test),
                  [x for x in ["hydrogen, which burns with a pop sound", "carbon dioxide, which turns lime water milky", "oxygen, which relights a glowing splint", "chlorine, which bleaches damp litmus"] if not x.startswith(g)][:3],
                  "Metals give hydrogen with acids; carbonates and hydrogencarbonates give carbon dioxide.")
    if k == "ind":
        s, r = ch(IND)
        return tq("What happens to %s?" % s, r, [x for x in ["turns red", "turns blue", "turns pink", "stays colourless", "turns yellow", "stays red", "stays blue"] if x != r][:3] if r not in ("stays red", "stays blue") else [x for x in ["turns blue", "turns pink", "turns yellow"]],
                  "Acids turn blue litmus red; bases turn red litmus blue and phenolphthalein pink.")
    c, f, chem, use = ch(SALT)
    if k == "formula":
        return tq("What is the chemical formula of %s?" % c, f, _R[0].sample([x[1] for x in SALT if x[1] != f], 3), "%s is %s, %s." % (c.capitalize(), chem, f))
    if k == "use":
        return tq("What is %s mainly used for?" % c, use, _R[0].sample([x[3] for x in SALT if x[3] != use], 3), "%s (%s) is used for %s." % (c.capitalize(), f, use))
    return tq("What is the common name of %s (%s)?" % (chem, f), c, _R[0].sample([x[0] for x in SALT if x[0] != c], 3), "%s is called %s." % (f, c))


ACID = [("Why should water never be added to concentrated acid?", "the reaction gives out so much heat that the mixture can splash out", ["the acid becomes stronger", "the water turns into ice", "a precipitate forms"], "Always add acid slowly to water, stirring."),
        ("Which ion makes a solution acidic?", "H⁺ (as H₃O⁺, hydronium)", ["OH⁻", "Na⁺", "Cl⁻"], "Acids give H⁺ ions in water."),
        ("Which ion makes a solution basic?", "OH⁻", ["H⁺", "Cl⁻", "SO₄²⁻"], "Bases that dissolve in water (alkalis) give OH⁻ ions."),
        ("Why does dry HCl gas not change the colour of dry blue litmus?", "without water, HCl does not form H⁺ ions", ["dry litmus has no colour", "HCl is a base", "the gas is too cold"], "Acids show their properties only in water."),
        ("What is the pH range of the human body for life to work?", "about 7.0 to 7.8", ["about 1 to 2", "about 10 to 12", "exactly 4"], "Small changes in pH affect enzymes."),
        ("Why does tooth decay start when the pH in the mouth falls below 5.5?", "acid from bacteria dissolves tooth enamel (calcium phosphate)", ["the teeth become magnetic", "saliva turns basic", "sugar freezes"], "Basic toothpaste neutralises the acid."),
        ("How is the sting of a bee (methanoic acid) treated?", "rub on a mild base such as baking soda", ["rub on vinegar", "rub on lemon juice", "pour on acid"], "The base neutralises the acid."),
        ("What is used to treat acidity in the stomach?", "an antacid such as milk of magnesia", ["vinegar", "lemon juice", "hydrochloric acid"], "Mg(OH)₂ is a mild base."),
        ("What is an alkali?", "a base that dissolves in water", ["any acid", "an insoluble base", "a type of salt only"], "For example NaOH and KOH."),
        ("What does the chlor-alkali process make from brine?", "sodium hydroxide, chlorine and hydrogen", ["sodium carbonate only", "baking soda and oxygen", "plaster of Paris"], "2NaCl + 2H₂O → 2NaOH + Cl₂ + H₂."),
        ("What is water of crystallisation?", "a fixed number of water molecules in a crystal of a salt", ["water that has frozen", "water in a solution", "water given off in respiration"], "Blue copper sulphate has 5 molecules of water per formula unit."),
        ("What happens when blue copper sulphate crystals are heated?", "they turn white as water of crystallisation is lost", ["they turn red", "they melt into a blue liquid", "they turn black at once"], "Adding water makes them blue again."),
        ("Why must plaster of Paris be stored in a moisture-proof container?", "it reacts with water and sets into hard gypsum", ["it becomes poisonous", "it turns into salt", "it melts"], "CaSO₄·½H₂O + 1½H₂O → CaSO₄·2H₂O."),
        ("What is a strong acid?", "an acid that gives a lot of H⁺ ions in water", ["a concentrated acid only", "an acid with a high pH", "an acid that does not dissolve"], "HCl is strong; acetic acid is weak."),
        ("Which acid is found in curd?", "lactic acid", ["citric acid", "acetic acid", "oxalic acid"], "Vinegar has acetic acid; lemon has citric acid."),
        ("Which acid is found in tamarind?", "tartaric acid", ["lactic acid", "methanoic acid", "oxalic acid"], "Tomato has oxalic acid; nettle and ant stings have methanoic acid."),
        ("What happens to the pH of a solution when it is diluted with water?", "an acid's pH rises towards 7", ["an acid's pH falls", "it always becomes 14", "it does not change"], "The H⁺ ions become less concentrated."),
        ("What is formed when a metal oxide reacts with an acid?", "a salt and water", ["hydrogen gas", "carbon dioxide", "a metal and oxygen"], "Metal oxides are basic oxides."),
        ("What is formed when carbon dioxide (a non-metal oxide) reacts with lime water?", "calcium carbonate (a white precipitate) and water", ["calcium chloride", "hydrogen", "a blue solution"], "Non-metal oxides are acidic."),
        ("Why is the soil sometimes treated with quicklime or slaked lime?", "to neutralise soil that is too acidic", ["to make it more acidic", "to add nitrogen", "to kill earthworms"], "Plants grow best in a certain pH range."),
        ("What are olfactory indicators?", "substances whose smell changes in acids or bases, such as onion and clove oil", ["indicators that change colour", "electrical meters", "metals that rust"], "They help visually impaired students."),
        ("Which gas is used to make bleaching powder from slaked lime?", "chlorine", ["carbon dioxide", "hydrogen", "oxygen"], "Ca(OH)₂ + Cl₂ → CaOCl₂ + H₂O."),
        ("How is baking soda made?", "from sodium chloride, water, carbon dioxide and ammonia", ["by heating limestone", "by electrolysis of water", "from gypsum"], "NaCl + H₂O + CO₂ + NH₃ → NH₄Cl + NaHCO₃."),
        ("Why does baking powder make a cake soft and spongy?", "heating gives carbon dioxide gas, which makes the dough rise", ["it adds water", "it melts the sugar", "it removes air"], "Tartaric acid in baking powder neutralises the sodium carbonate formed."),
        ("Which acid is found in the human stomach?", "hydrochloric acid", ["sulphuric acid", "nitric acid", "acetic acid"], "It helps digestion; too much causes acidity."),
        ("What is the name for a solution with a pH of 7?", "neutral", ["acidic", "basic", "alkaline"], "Pure water is neutral.")]


# =================================================================== Chapter 3: metals and non-metals
SERIES = ["potassium", "sodium", "calcium", "magnesium", "aluminium", "zinc", "iron", "lead", "copper", "mercury", "silver", "gold"]
SALTS = {"zinc": "zinc sulphate", "iron": "iron sulphate", "copper": "copper sulphate", "silver": "silver nitrate", "lead": "lead nitrate", "magnesium": "magnesium sulphate", "aluminium": "aluminium sulphate"}
EC = {"Be": (4, "2, 2"), "B": (5, "2, 3"), "Si": (14, "2, 8, 4"), "P": (15, "2, 8, 5"), "Na": (11, "2, 8, 1"), "Mg": (12, "2, 8, 2"), "Al": (13, "2, 8, 3"), "K": (19, "2, 8, 8, 1"), "Ca": (20, "2, 8, 8, 2"), "Cl": (17, "2, 8, 7"), "O": (8, "2, 6"), "S": (16, "2, 8, 6"),
      "F": (9, "2, 7"), "N": (7, "2, 5"), "C": (6, "2, 4"), "Li": (3, "2, 1"), "Ne": (10, "2, 8"), "Ar": (18, "2, 8, 8")}
IONIC = [("NaCl", "Na", "Cl", 1), ("MgCl₂", "Mg", "Cl", 2), ("MgO", "Mg", "O", 2), ("CaCl₂", "Ca", "Cl", 2), ("Na₂O", "Na", "O", 1), ("KCl", "K", "Cl", 1), ("CaO", "Ca", "O", 2), ("K₂S", "K", "S", 1), ("NaF", "Na", "F", 1), ("Al₂O₃", "Al", "O", 3)]


def c_metal(k=None):
    k = k or ch(["disp", "react", "config", "ionic"])
    if k == "disp":
        m = ch(list(SALTS))
        sm = ch([x for x in SALTS if x != m])
        yes = SERIES.index(m) < SERIES.index(sm)
        ans = "yes, because %s is more reactive than %s" % (m, sm) if yes else "no, because %s is less reactive than %s" % (m, sm)
        return tq("Will %s displace %s from %s solution?" % (m, sm, SALTS[sm]), ans, ["yes, because %s is more reactive than %s" % (sm, m), "no, because %s is less reactive than %s" % (sm, m), "only if the solution is boiled"],
                  "Reactivity series: K > Na > Ca > Mg > Al > Zn > Fe > Pb > Cu > Hg > Ag > Au. A metal displaces a less reactive metal.")
    if k == "react":
        a, b = sorted(_R[0].sample(range(len(SERIES)), 2))
        return tq("Which is more reactive: %s or %s?" % (SERIES[b], SERIES[a]) if _R[0].random() < 0.5 else "Which is more reactive: %s or %s?" % (SERIES[a], SERIES[b]), SERIES[a],
                  [SERIES[b], "both are equally reactive", "neither reacts with anything"], "In the reactivity series %s is above %s." % (SERIES[a], SERIES[b]))
    if k == "config":
        el, (z, c) = ch(sorted(EC.items()))
        wr = set()
        parts = [int(x) for x in c.split(", ")]
        for d in (-1, 1):
            p = parts[:]
            p[-1] += d
            if p[-1] > 0:
                wr.add(", ".join(map(str, p)))
        wr.add(", ".join(map(str, parts[:-1] + [parts[-1] + 8] if parts[-1] + 8 <= 8 else parts[::-1])))
        wr.add("2, %d" % (z - 2) if z > 10 else "%d, %d" % (2, z))
        wr.discard(c)
        return tq("What is the electronic configuration of %s (atomic number %d)?" % (el, z), c, sorted(wr)[:3] if len(wr) >= 3 else sorted(wr) + ["2, 8, 8, 8"], "Fill shells K, L, M with 2, 8, 8 electrons: %s." % c)
    f, m, n, val = ch(IONIC)
    k2 = ch(["give", "charge"])
    if k2 == "give":
        return tq("In forming %s, how many electrons does each %s atom lose?" % (f, m), str(val), [str(x) for x in [1, 2, 3, 4] if x != val][:3],
                  "%s (%s) loses %d electron%s to get a full outer shell." % (m, EC[m][1], val, "" if val == 1 else "s"))
    q = {"Cl": 1, "O": 2, "S": 2, "F": 1}[n]
    return tq("What is the charge on the %s ion in %s?" % (n, f), "%d−" % q if q > 1 else "1−", ["%d+" % q, "%d−" % (q + 1), "0"], "%s (%s) gains %d electron%s." % (n, EC[n][1], q, "" if q == 1 else "s"))


MET = [("Which metal is liquid at room temperature?", "mercury", ["sodium", "iron", "gallium"], "Bromine is the liquid non-metal."),
       ("Which non-metal is a good conductor of electricity?", "graphite", ["sulphur", "diamond", "iodine"], "Graphite has free electrons."),
       ("Which non-metal is lustrous?", "iodine", ["sulphur", "carbon (charcoal)", "phosphorus"], "Iodine crystals are shiny."),
       ("Why is sodium kept under kerosene?", "it reacts strongly with air and water and can catch fire", ["it melts in air", "it smells", "it is very heavy"], "Potassium is also kept in kerosene."),
       ("Which metals can be cut with a knife?", "sodium and potassium", ["iron and copper", "gold and silver", "aluminium and zinc"], "They are soft alkali metals."),
       ("What is an amphoteric oxide?", "an oxide that reacts with both acids and bases, such as Al₂O₃ and ZnO", ["an oxide that reacts with neither", "an acidic oxide only", "a basic oxide only"], "Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O."),
       ("Why does calcium float when added to water?", "bubbles of hydrogen stick to its surface", ["calcium is lighter than water", "it reacts with oxygen", "it turns into gas"], "Magnesium floats in hot water for the same reason."),
       ("Which metal does not react with water even in steam?", "copper", ["iron", "magnesium", "sodium"], "Lead, silver and gold also do not react."),
       ("What is aqua regia?", "a mixture of concentrated hydrochloric and nitric acids (3 : 1) that dissolves gold", ["pure water", "a strong base", "a mixture of salts"], "It means 'royal water'."),
       ("Why do ionic compounds have high melting points?", "strong forces of attraction between oppositely charged ions", ["they contain molecules", "they are liquids", "they have weak bonds"], "A lot of energy is needed to break the lattice."),
       ("When do ionic compounds conduct electricity?", "when molten or dissolved in water", ["only when solid", "never", "only when frozen"], "The ions can then move."),
       ("How are highly reactive metals such as sodium obtained?", "by electrolytic reduction of their molten chlorides", ["by heating with carbon", "by heating alone", "by panning"], "Carbon cannot reduce them."),
       ("How is zinc obtained from zinc blende (ZnS)?", "roasting to ZnO, then reduction with carbon", ["electrolysis of the ore", "heating with water", "dissolving in acid"], "2ZnS + 3O₂ → 2ZnO + 2SO₂; ZnO + C → Zn + CO."),
       ("What is calcination?", "heating a carbonate ore strongly in limited air", ["heating a sulphide ore in excess air", "melting the metal", "electrolysis"], "ZnCO₃ → ZnO + CO₂."),
       ("What is roasting?", "heating a sulphide ore strongly in excess air", ["heating a carbonate ore in limited air", "dissolving the ore", "cooling the ore"], "This turns the sulphide into an oxide."),
       ("Which metal is used in the thermit reaction to join railway tracks?", "aluminium", ["copper", "sodium", "silver"], "Fe₂O₃ + 2Al → 2Fe + Al₂O₃ + heat."),
       ("What is gangue?", "the unwanted earthy impurities in an ore", ["the pure metal", "an alloy", "the slag on rust"], "It is removed before extraction."),
       ("How is copper purified?", "electrolytic refining with impure copper as the anode", ["heating with carbon", "galvanising", "roasting"], "Pure copper collects on the cathode."),
       ("What is galvanisation?", "coating iron with a thin layer of zinc", ["coating iron with copper", "mixing iron with carbon", "painting iron with oil"], "Zinc protects iron even if scratched."),
       ("What is an alloy?", "a homogeneous mixture of a metal with other metals or a non-metal", ["a pure metal", "a compound of a metal and oxygen", "an ore"], "Brass, bronze and steel are alloys."),
       ("What is brass made of?", "copper and zinc", ["copper and tin", "iron and carbon", "lead and tin"], "Bronze is copper and tin."),
       ("What is solder made of, and why is it used for welding wires?", "lead and tin; it has a low melting point", ["iron and carbon; it is very hard", "copper and zinc; it is magnetic", "gold and silver; it shines"], "Alloys often melt lower than their metals."),
       ("Why is 22-carat gold used for jewellery instead of 24-carat gold?", "pure gold is too soft, so it is alloyed with silver or copper", ["24-carat gold rusts", "22-carat gold is pure", "pure gold is brittle and breaks"], "22-carat gold is 22 parts gold in 24."),
       ("What happens when a metal reacts with dilute nitric acid?", "hydrogen is usually not given off because nitric acid is an oxidising agent", ["only hydrogen forms", "the metal turns into a non-metal", "no reaction happens with any metal"], "Mg and Mn give hydrogen with very dilute nitric acid."),
        ("Which metal is the best conductor of electricity?", "silver", ["iron", "lead", "mercury"], "Copper is next and is cheaper, so it is used in wires."),
        ("Which metals are the poorest conductors of heat?", "lead and mercury", ["silver and copper", "gold and aluminium", "iron and zinc"], "Most metals conduct heat well."),
        ("What is the property of metals that lets them be drawn into wires?", "ductility", ["malleability", "sonority", "lustre"], "Malleability means they can be beaten into sheets."),
        ("Why are metals sonorous?", "they make a ringing sound when struck", ["they are shiny", "they are soft", "they react with water"], "That is why bells are made of metal.")]


# =================================================================== Chapter 4: carbon and its compounds
STEM = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec"}
FG = [("alcohol", "–OH", "ol"), ("aldehyde", "–CHO", "al"), ("ketone", "–CO–", "one"), ("carboxylic acid", "–COOH", "oic acid"), ("halogen (chloro)", "–Cl", "chloro-")]


def c_carbon(k=None):
    k = k or ch(["formula", "name", "bonds", "fg", "homolog"])
    n = ch(list(range(1, 11)))
    fam = ch(["ane", "ene", "yne"])
    if fam != "ane" and n == 1:
        return None
    h = {"ane": 2 * n + 2, "ene": 2 * n, "yne": 2 * n - 2}[fam]
    f = "C%sH%d" % (n if n > 1 else "", h)
    nm = STEM[n] + fam
    if k == "formula":
        return tq("What is the molecular formula of %s?" % nm, sub(f), [sub("C%sH%d" % (n if n > 1 else "", x)) for x in {2 * n + 2, 2 * n, 2 * n - 2, 2 * n + 4} - {h} if x > 0][:3],
                  "%s: C<sub>n</sub>H<sub>%s</sub>." % ({"ane": "Alkanes", "ene": "Alkenes", "yne": "Alkynes"}[fam], {"ane": "2n+2", "ene": "2n", "yne": "2n−2"}[fam]))
    if k == "name":
        wr = [STEM[n] + x for x in ("ane", "ene", "yne") if x != fam] + [STEM[n + 1 if n < 10 else n - 1] + fam]
        return tq("What is the name of the hydrocarbon %s?" % sub(f), nm, wr, "%d carbons: %s-; %s." % (n, STEM[n], {"ane": "only single bonds: -ane", "ene": "one double bond: -ene", "yne": "one triple bond: -yne"}[fam]))
    if k == "bonds":
        if fam != "ane":
            return None
        return nq("How many covalent bonds are there in a molecule of %s (%s)?" % (nm, sub(f)), 3 * n + 1, [3 * n, 2 * n + 2, 4 * n], "",
                  "C–H bonds: %d; C–C bonds: %d; total = 3n + 1 = <b>%d</b>." % (2 * n + 2, n - 1, 3 * n + 1))
    if k == "homolog":
        return nq("By how many atomic mass units do successive members of a homologous series differ?", 14, [12, 2, 16], " u", "Each member differs by CH₂: 12 + 2 = <b>14 u</b>.") if n == 1 else \
            tq("Which is the next member of the homologous series after %s?" % sub(f), sub("C%dH%d" % (n + 1, h + 2)), [sub("C%dH%d" % (n + 1, h)), sub("C%sH%d" % (n if n > 1 else "", h + 2)), sub("C%dH%d" % (n + 2, h + 4))],
               "Add CH₂: C<sub>%d</sub>H<sub>%d</sub>." % (n + 1, h + 2)) if n < 10 else None
    g, grp, suf = ch(FG)
    nn = ch([1, 2, 3, 4]) if g != "ketone" else ch([3, 4, 5])
    if g == "halogen (chloro)":
        nm2 = "chloro" + STEM[nn] + "ane"
    elif g == "carboxylic acid":
        nm2 = STEM[nn] + "anoic acid"
    else:
        nm2 = STEM[nn] + "an" + suf
    return tq("Which functional group is present in %s?" % nm2, "%s (%s)" % (g, grp), ["%s (%s)" % (x[0], x[1]) for x in FG if x[0] != g][:3] if _R[0].random() < 0.5 else _R[0].sample(["%s (%s)" % (x[0], x[1]) for x in FG if x[0] != g], 3),
              "The ending tells the group: -ol alcohol, -al aldehyde, -one ketone, -oic acid carboxylic acid, chloro- halogen.")


CARB = [("Why does carbon form covalent bonds rather than ionic bonds?", "it would need too much energy to gain or lose four electrons", ["it has no electrons", "it is a metal", "it only forms ions"], "It shares electrons instead."),
        ("What is catenation?", "carbon's ability to form bonds with other carbon atoms, making long chains", ["carbon changing into diamond", "burning of carbon", "carbon dissolving in water"], "This gives a huge number of compounds."),
        ("What is tetravalency?", "carbon has a valency of four", ["carbon has four protons", "carbon forms four ions", "carbon has four shells"], "It can bond with four other atoms."),
        ("What are structural isomers?", "compounds with the same molecular formula but different structures", ["the same compound in different states", "atoms of the same element", "compounds with different formulas but one structure"], "Butane and isobutane are isomers."),
        ("How many structural isomers does butane (C₄H₁₀) have?", "2", ["1", "3", "4"], "n-butane and isobutane (2-methylpropane)."),
        ("What is formed when ethanol reacts with sodium?", "sodium ethoxide and hydrogen", ["ethanoic acid and water", "ethene and water", "carbon dioxide only"], "2Na + 2CH₃CH₂OH → 2CH₃CH₂ONa + H₂."),
        ("What happens when ethanol is heated with excess hot concentrated sulphuric acid?", "it is dehydrated to ethene", ["it forms ethanoic acid", "it forms an ester", "nothing happens"], "Concentrated H₂SO₄ removes water."),
        ("What is esterification?", "an acid reacts with an alcohol to form a sweet-smelling ester", ["an ester is split by a base", "a hydrocarbon burns", "hydrogen is added to oil"], "CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O."),
        ("What is saponification?", "an ester reacts with a base (NaOH) to give an alcohol and the sodium salt of the acid (soap)", ["an acid reacts with an alcohol", "a fuel burns", "oil hardens with hydrogen"], "This is how soap is made."),
        ("What is hydrogenation of vegetable oils?", "adding hydrogen with a nickel catalyst to make fats such as vanaspati ghee", ["removing hydrogen from oil", "adding oxygen to oil", "burning oil"], "It turns unsaturated oils into saturated fats."),
        ("Why does a saturated hydrocarbon burn with a clean blue flame?", "it burns completely in enough oxygen", ["it contains double bonds", "it has a lot of soot", "it contains sulphur"], "Unsaturated ones give a sooty yellow flame."),
        ("What is formed when ethanol is oxidised by alkaline potassium permanganate?", "ethanoic acid", ["ethene", "methane", "an ester"], "KMnO₄ is an oxidising agent."),
        ("What is glacial acetic acid?", "pure ethanoic acid, which freezes in cold weather", ["vinegar with ice", "a 5% solution of acetic acid", "an ester"], "It freezes at 290 K."),
        ("What is denatured alcohol?", "ethanol with poisonous methanol added so it cannot be drunk", ["pure ethanol", "alcohol with water", "an ester"], "A dye is also added."),
        ("Why are detergents better than soaps in hard water?", "detergents do not form scum with calcium and magnesium ions", ["detergents contain calcium", "soaps do not dissolve", "detergents make water soft"], "Soap forms an insoluble scum."),
        ("What is a micelle?", "a cluster of soap molecules with tails inside the oily dirt and heads outside in water", ["a crystal of salt", "a type of ester", "a bubble of gas"], "The dirt is then rinsed away."),
        ("What type of bond is in a molecule of nitrogen?", "a triple bond", ["a single bond", "a double bond", "an ionic bond"], "N≡N."),
        ("What type of bond is in a molecule of oxygen?", "a double bond", ["a single bond", "a triple bond", "an ionic bond"], "O=O."),
        ("Why are covalent compounds usually poor conductors of electricity?", "they do not form ions", ["they are always solids", "they contain metals", "they have high melting points"], "No charged particles can move."),
        ("Which allotrope of carbon is a football-shaped molecule of 60 atoms?", "buckminsterfullerene", ["diamond", "graphite", "charcoal"], "C₆₀ looks like a geodesic dome."),
        ("Why is diamond so hard?", "each carbon is bonded to four others in a rigid 3D structure", ["it has free electrons", "it is made of layers", "it is a metal"], "Graphite has layers that slide."),
        ("What is a substitution reaction of methane?", "a hydrogen atom is replaced by chlorine in sunlight", ["hydrogen is added", "methane burns", "methane dissolves in water"], "CH₄ + Cl₂ → CH₃Cl + HCl."),
        ("What is the general formula of the alkenes?", "CₙH₂ₙ", ["CₙH₂ₙ₊₂", "CₙH₂ₙ₋₂", "CₙHₙ"], "Ethene is C₂H₄."),
        ("Which compound has a triple bond?", "ethyne", ["ethane", "ethene", "ethanol"], "Ethyne is C₂H₂."),
        ("What is formed when ethanoic acid reacts with sodium carbonate?", "sodium ethanoate, carbon dioxide and water", ["ethanol and oxygen", "an ester only", "methane"], "This is a test for carboxylic acids."),
        ("Which gas is produced when ethanol burns in air?", "carbon dioxide (with water)", ["hydrogen", "chlorine", "ammonia"], "C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O."),
        ("What is a cyclic hydrocarbon with six carbons and alternating double bonds?", "benzene", ["cyclohexane", "hexane", "hexene"], "Benzene is C₆H₆.")]


def UNITS10a():
    from in_sci import U, K
    b_obs, b_acid, b_met, b_carb = once_maker(OBS1), once_maker(ACID), once_maker(MET), once_maker(CARB)
    CH = "Chemical Substances – Nature and Behaviour"
    return [
        U(1, "chemical-reactions-and-equations", 1, CH,
          "Chemical reactions: chemical equation, balanced chemical equation, implications of a balanced chemical equation, types of chemical reactions: combination, decomposition, displacement, double displacement, precipitation, endothermic and exothermic reactions, oxidation and reduction.",
          "Chemical Reactions and Equations", "chemical reactions and equations",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 1: balancing chemical equations, types of reactions, oxidation and reduction, corrosion and rancidity. 100 questions with answers.",
          "Atoms are never created or destroyed in a reaction.", "Balance by changing coefficients, never the formulas.",
          "<p>A chemical equation shows reactants turning into products. Because mass is conserved, the number of each kind of atom must be the same on both sides, so we balance it by putting numbers (coefficients) in front of formulas.</p>"
          "<p>Reactions are combination (A + B → AB), decomposition (AB → A + B), displacement (a more reactive element takes the place of a less reactive one) and double displacement (two compounds swap ions). A substance that gains oxygen or loses hydrogen is oxidised; one that loses oxygen or gains hydrogen is reduced.</p>",
          [("Balance Fe + H₂O → Fe₃O₄ + H₂.", ["3 Fe on the right, so 3Fe", "4 O, so 4H₂O", "8 H, so 4H₂"], "3Fe + 4H₂O → Fe₃O₄ + 4H₂"),
           ("CuO + H₂ → Cu + H₂O: what is reduced?", ["CuO loses oxygen"], "CuO (H₂ is oxidised)")],
          ["Changing a subscript (H₂O to H₂O₂) to balance an equation.", "Calling every reaction with a gas a decomposition.", "Mixing up the oxidising agent with the substance that is oxidised."],
          [("What is a balanced chemical equation?", "An equation with the same number of atoms of each element on both sides, showing that mass is conserved."),
           ("What is the difference between displacement and double displacement?", "In displacement one element replaces another in a compound; in double displacement two compounds exchange ions.")],
          lambda: [("Balancing equations", [(K(c_balance, "coef"), 20)]), ("Types of reactions", [(c_type, 20)]), ("Oxidation and reduction", [(c_redox, 20)]),
                   ("Observations, corrosion and rancidity", [(b_obs, 16), (c_type, 4)]), ("Mixed problems", [(K(c_balance, "set"), 10), (c_redox, 6), (b_obs, 4)])]),
        U(2, "acids-bases-and-salts", 2, CH,
          "Acids, bases and salts: their definitions in terms of furnishing of H⁺ and OH⁻ ions, general properties, examples and uses, neutralisation, concept of pH scale, importance of pH in everyday life; preparation and uses of sodium hydroxide, bleaching powder, baking soda, washing soda and plaster of Paris.",
          "Acids, Bases and Salts", "acids, bases and salts",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 2: indicators, the pH scale, neutralisation, reactions of acids and bases, and baking soda, washing soda, bleaching powder and plaster of Paris. 100 questions with answers.",
          "pH below 7 is acidic, 7 is neutral, above 7 is basic.", "Acid + base → salt + water.",
          "<p>Acids give H⁺ ions in water and turn blue litmus red; bases give OH⁻ ions and turn red litmus blue and phenolphthalein pink. The pH scale runs from 0 to 14: the lower the pH, the stronger the acid; the higher, the stronger the base.</p>"
          "<p>Acids react with metals to give hydrogen, with carbonates to give carbon dioxide, and with bases to give a salt and water (neutralisation). Common salts have everyday uses: baking soda (NaHCO₃), washing soda (Na₂CO₃·10H₂O), bleaching powder (CaOCl₂) and plaster of Paris (CaSO₄·½H₂O).</p>",
          [("Salt from sulphuric acid and sodium hydroxide?", ["metal part: sodium", "acid part: sulphate"], "sodium sulphate (+ water)"),
           ("A solution has pH 3. Describe it.", ["below 7, and far below"], "strongly acidic")],
          ["Thinking a higher pH means more acidic.", "Adding water to concentrated acid.", "Mixing up baking soda (NaHCO₃) and washing soda (Na₂CO₃·10H₂O)."],
          [("Why is pH important in everyday life?", "Our body works in a narrow pH range, tooth decay starts below pH 5.5, plants need suitable soil pH, and antacids treat excess stomach acid."),
           ("What is neutralisation?", "The reaction between an acid and a base to form a salt and water.")],
          lambda: [("Indicators and pH", [(K(c_ph, "class", "num", "colour"), 20)]), ("Comparing pH", [(K(c_ph, "comp"), 14), (K(c_salt, "ind"), 6)]),
                   ("Reactions of acids and bases", [(K(c_salt, "neut", "gas"), 20)]), ("Salts in daily life", [(K(c_salt, "name", "use", "formula"), 20)]), ("Applying ideas", [(b_acid, 20)])]),
        U(3, "metals-and-non-metals", 3, CH,
          "Metals and non-metals: properties of metals and non-metals, reactivity series, formation and properties of ionic compounds, basic metallurgical processes, corrosion and its prevention.",
          "Metals and Non-metals", "metals and non-metals",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 3: properties of metals and non-metals, the reactivity series, displacement, ionic compounds, extraction of metals, corrosion and alloys. 100 questions with answers.",
          "A more reactive metal displaces a less reactive one.", "K Na Ca Mg Al Zn Fe Pb [H] Cu Hg Ag Au",
          "<p>Metals are usually lustrous, malleable, ductile and good conductors; non-metals are usually dull and brittle. Metals lose electrons to form positive ions; non-metals gain electrons to form negative ions, and the attraction between them makes ionic compounds with high melting points.</p>"
          "<p>The reactivity series lists metals from most to least reactive. A metal displaces any metal below it from a salt solution. Very reactive metals are extracted by electrolysis, metals in the middle by roasting or calcination and then reduction with carbon, and the least reactive by heating alone.</p>",
          [("Will copper displace silver from silver nitrate?", ["copper is above silver"], "yes"),
           ("Electronic configuration of Mg (Z = 12)?", ["2 in K, 8 in L, 2 in M"], "2, 8, 2")],
          ["Thinking a less reactive metal can displace a more reactive one.", "Saying ionic compounds conduct electricity as solids.", "Mixing up roasting (sulphide ores) and calcination (carbonate ores)."],
          [("Why are ionic compounds hard with high melting points?", "Strong electrostatic forces between oppositely charged ions hold them in a rigid lattice."),
           ("How can corrosion of iron be prevented?", "By painting, oiling, greasing, galvanising, chrome plating, anodising or making alloys such as stainless steel.")],
          lambda: [("The reactivity series", [(K(c_metal, "react"), 20)]), ("Displacement reactions", [(K(c_metal, "disp"), 20)]), ("Electronic configuration and ions", [(K(c_metal, "config", "ionic"), 20)]),
                   ("Properties and extraction", [(b_met, 20)]), ("Mixed problems", [(K(c_metal, "ionic", "config"), 10), (K(c_metal, "disp"), 6), (K(c_metal, "react"), 4)])]),
        U(4, "carbon-and-its-compounds", 4, CH,
          "Carbon compounds: covalent bonding in carbon compounds, versatile nature of carbon, homologous series, nomenclature of carbon compounds containing functional groups (halogens, alcohol, ketones, aldehydes, alkanes and alkynes), saturated and unsaturated hydrocarbons, chemical properties of carbon compounds (combustion, oxidation, addition and substitution reaction), ethanol and ethanoic acid (only properties and uses), soaps and detergents.",
          "Carbon and its Compounds", "carbon and its compounds",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 4: covalent bonds, homologous series, naming alkanes, alkenes and alkynes, functional groups, ethanol, ethanoic acid, soaps and detergents. 100 questions with answers.",
          "Alkanes CₙH₂ₙ₊₂, alkenes CₙH₂ₙ, alkynes CₙH₂ₙ₋₂.", "Successive members differ by CH₂ (14 u).",
          "<p>Carbon shares electrons to form covalent bonds. Its valency of four and catenation give a huge number of compounds. Hydrocarbons with only single bonds are saturated (alkanes); those with double or triple bonds are unsaturated (alkenes, alkynes).</p>"
          "<p>Name compounds by the number of carbons (meth-, eth-, prop-, but-, pent-…) and the functional group: -ol (alcohol), -al (aldehyde), -one (ketone), -oic acid (carboxylic acid), chloro- (halogen). Members of a homologous series have the same functional group and differ by CH₂.</p>",
          [("Formula of propene?", ["3 carbons", "alkene: CₙH₂ₙ"], "C₃H₆"),
           ("Covalent bonds in propane?", ["8 C–H + 2 C–C"], "10")],
          ["Writing CₙH₂ₙ₊₂ for an alkene.", "Forgetting the C–C bonds when counting bonds.", "Thinking soaps work well in hard water."],
          [("What is a homologous series?", "A family of carbon compounds with the same functional group and similar chemical properties, where each member differs by a CH₂ unit."),
           ("How do soaps clean dirt?", "Soap molecules form micelles: the hydrocarbon tails dissolve in the oily dirt and the ionic heads face the water, so the dirt is washed away.")],
          lambda: [("Formulae of hydrocarbons", [(K(c_carbon, "formula"), 20)]), ("Naming hydrocarbons", [(K(c_carbon, "name"), 20)]), ("Bonds and homologous series", [(K(c_carbon, "bonds", "homolog"), 20)]),
                   ("Functional groups", [(K(c_carbon, "fg"), 12), (b_carb, 8)]), ("Properties and reactions", [(b_carb, 14), (K(c_carbon, "fg"), 4), (K(c_carbon, "formula"), 2)])]),
    ]
