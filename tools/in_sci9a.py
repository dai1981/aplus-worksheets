# -*- coding: utf-8 -*-
"""Class 9 Science, Unit I Matter – Its Nature and Behaviour: NCERT chapters 1–4 (question makers)."""
from fractions import Fraction as F
from sci_chem import sub, molar
from uk_alsci import nf, nq, tq, once_maker
from in_sci import pairs, name, _R, U, K

MI = "−"


def ch(xs):
    return _R[0].choice(xs)


def sn(x):
    return (MI if x < 0 else "") + "{:,}".format(abs(x))


# =================================================================== Chapter 1: matter in our surroundings
SUBST = [("water", 0, 100), ("ethanol (alcohol)", -114, 78), ("mercury", -39, 357), ("iron", 1538, 2862), ("oxygen", -218, -183), ("nitrogen", -210, -196),
         ("naphthalene", 80, 218), ("sodium chloride (common salt)", 801, 1413), ("sulphur", 115, 445), ("lead", 327, 1749), ("acetone", -95, 56), ("bromine", -7, 59),
         ("copper", 1085, 2562), ("chloroform", -64, 61), ("benzene", 6, 80), ("aluminium", 660, 2519)]


def c_state(k=None):
    R = _R[0]
    s, mp, bp = ch(SUBST)
    st = R.choice(["solid", "liquid", "gas"])
    span = max(10, (bp - mp) // 3)
    if st == "solid":
        t = mp - R.randrange(10, 200, 5)
    elif st == "liquid":
        if bp - mp < 20:
            return None
        t = R.randrange(mp + 5, bp - 4)
        t -= t % 5 if bp - mp > 40 else 0
        if not (mp + 2 < t < bp - 2):
            return None
    else:
        t = bp + R.randrange(10, 300, 5)
    if t < -273:
        return None
    return tq("The melting point of %s is %s °C and its boiling point is %s °C. What is its physical state at %s °C?" % (s, sn(mp), sn(bp), sn(t)), st,
              [x for x in ["solid", "liquid", "gas", "plasma"] if x != st],
              "Below %s °C it is solid, between %s °C and %s °C liquid, above %s °C gas. At %s °C it is a <b>%s</b>." % (sn(mp), sn(mp), sn(bp), sn(bp), sn(t), st))


def c_temp(k=None):
    R = _R[0]
    k = k or ch(["toK", "toC"])
    if k == "toK":
        t = R.choice(list(range(-200, 400, 5)))
        return nq("Convert %s °C into the Kelvin scale." % sn(t), t + 273, [t - 273, 273 - t, t + 373], " K", "T(K) = t(°C) + 273 = %s + 273 = <b>%d K</b>." % (sn(t), t + 273))
    T = R.choice(list(range(50, 700, 5)))
    return nq("Convert %d K into the Celsius scale." % T, T - 273, [T + 273, 273 - T, T - 373], " °C", "t(°C) = T(K) − 273 = %d − 273 = <b>%s °C</b>." % (T, sn(T - 273)))


PROC = [("a solid changing into a liquid", "melting (fusion)"), ("a liquid changing into a gas at its boiling point", "boiling (vaporisation)"),
        ("a gas changing into a liquid", "condensation"), ("a liquid changing into a solid", "freezing (solidification)"),
        ("a solid changing directly into a gas without becoming a liquid", "sublimation"), ("a gas changing directly into a solid", "deposition"),
        ("a liquid changing into vapour at the surface, below its boiling point", "evaporation"), ("particles of one substance mixing on their own with another", "diffusion")]
PROC_EX = [("Camphor disappears slowly from an open dish.", "sublimation"), ("Water droplets form on the outside of a glass of iced water.", "condensation"),
           ("Wet clothes dry on a clothes line.", "evaporation"), ("Ice cubes turn into water on a plate.", "melting (fusion)"),
           ("Water in an ice tray becomes ice in the freezer.", "freezing (solidification)"), ("The smell of hot food reaches you several metres away.", "diffusion"),
           ("Naphthalene balls get smaller in a cupboard.", "sublimation"), ("Water in a kettle bubbles at 100 °C.", "boiling (vaporisation)"),
           ("Ammonium chloride heated in a china dish forms a white solid on the cool funnel above.", "deposition"), ("A drop of ink spreads through a glass of still water.", "diffusion"),
           ("Dew forms on grass on a cool morning.", "condensation"), ("Molten wax hardens as a candle cools.", "freezing (solidification)"),
           ("A puddle on the road disappears on a sunny day.", "evaporation"), ("Solid iodine gives violet vapour when gently warmed.", "sublimation")]
MAT1 = [("What is matter?", "anything that has mass and occupies space", ["only things we can see", "only solids and liquids", "anything that gives light"], "Air is matter too."),
        ("Why can gases be compressed easily?", "the particles are far apart with large spaces between them", ["the particles are very heavy", "the particles do not move", "gases have no mass"], "That is why LPG and CNG are stored compressed."),
        ("Which state of matter has a fixed shape and a fixed volume?", "solid", ["liquid", "gas", "all three"], "Liquids have a fixed volume but no fixed shape."),
        ("Why does a gas fill its whole container?", "its particles move freely and fast in all directions", ["its particles are attracted to the walls", "it has a fixed shape", "its particles are stuck together"], "The force of attraction between gas particles is very weak."),
        ("What happens to the rate of diffusion when the temperature rises?", "it increases", ["it decreases", "it stays the same", "diffusion stops"], "Particles move faster when they have more kinetic energy."),
        ("Why does the temperature stay at 0 °C while ice is melting?", "the heat supplied is used to overcome the forces of attraction between particles", ["the thermometer stops working", "ice does not take in heat", "the heat escapes into the air"], "This hidden heat is the latent heat of fusion."),
        ("What is the latent heat of vaporisation?", "the heat needed to change 1 kg of a liquid into vapour at its boiling point", ["the heat needed to melt 1 kg of a solid", "the heat given out by a gas", "the heat needed to warm water by 1 °C"], "Steam at 100 °C has more energy than water at 100 °C."),
        ("Why does steam cause worse burns than boiling water at the same temperature?", "steam also gives out its latent heat of vaporisation when it condenses on the skin", ["steam is hotter than 100 °C always", "water cannot burn", "steam has no energy"], "The extra energy is the latent heat."),
        ("Which factor does NOT increase the rate of evaporation?", "an increase in humidity", ["a larger surface area", "a higher temperature", "a faster wind"], "Humid air already holds a lot of water vapour."),
        ("Why does evaporation cause cooling?", "particles with more energy escape, so the liquid loses heat energy", ["the liquid becomes heavier", "evaporation gives out heat", "cold air enters the liquid"], "Sweating cools the body this way."),
        ("Why do we wear cotton clothes in summer?", "cotton absorbs sweat, which then evaporates and cools the body", ["cotton is waterproof", "cotton reflects all heat", "cotton is heavy"], "Evaporation from the cloth takes heat from the body."),
        ("Why is water stored in an earthen pot (matka) cool?", "water seeps through the pores and evaporates from the surface, causing cooling", ["clay is a refrigerant", "the pot is always in the shade", "clay absorbs heat from the water"], "Evaporation causes cooling."),
        ("What is the boiling point of water at normal atmospheric pressure?", "100 °C (373 K)", ["0 °C (273 K)", "50 °C (323 K)", "212 °C (485 K)"], "Pressure changes the boiling point."),
        ("What is dry ice?", "solid carbon dioxide", ["frozen water", "solid nitrogen", "frozen alcohol"], "It changes directly into gas when the pressure is lowered."),
        ("How can a gas be changed into a liquid?", "by increasing the pressure and lowering the temperature", ["by lowering the pressure", "by heating it", "by shaking it"], "This is how LPG is made."),
        ("Why does a liquid take the shape of its container?", "its particles can slide past each other", ["its particles are fixed in place", "it has no particles", "it is lighter than air"], "Liquids flow."),
        ("Which has the highest rate of diffusion?", "gases", ["solids", "liquids", "all are equal"], "Gas particles move fastest and have the most space."),
        ("What happens to the particles of a solid when it is heated?", "they vibrate faster and move further apart", ["they stop moving", "they become smaller", "they disappear"], "With enough heat the solid melts."),
        ("A sponge can be squeezed, yet it is a solid. Why?", "it has tiny holes filled with air that are pushed out", ["it is really a liquid", "its particles are compressed", "it has no mass"], "The solid part itself is not compressed."),
        ("Which is an example of matter?", "air", ["love", "smell", "heat"], "Smell is the sense; the gas particles that cause it are matter."),
        ("What is the SI unit of temperature?", "kelvin (K)", ["degree Celsius (°C)", "joule (J)", "degree Fahrenheit"], "0 °C = 273 K."),
        ("Why does an ice-cold glass become wet on the outside?", "water vapour in the air condenses on the cold surface", ["water leaks through the glass", "the ice melts through the glass", "the glass sweats"], "The vapour comes from the air, not the glass."),
        ("Why does acetone on your palm feel cold?", "it evaporates quickly, taking heat from your hand", ["acetone is always at 0 °C", "it freezes on your hand", "it reacts with skin"], "Evaporation causes cooling."),
        ("What happens to the boiling point of water at a hill station?", "it is lower, because the air pressure is lower", ["it is higher", "it stays at 100 °C", "water cannot boil there"], "That is why cooking takes longer in the hills."),
        ("Why does a solid have a fixed shape?", "its particles are tightly packed with strong forces between them", ["its particles move freely", "it has no particles", "its particles are far apart"], "The particles only vibrate about fixed positions."),
        ("Which change of state happens at every temperature, not just at one point?", "evaporation", ["boiling", "melting", "freezing"], "Boiling happens only at the boiling point.")]


# =================================================================== Chapter 2: is matter around us pure?
CLASS = [("iron", "an element"), ("sulphur", "an element"), ("oxygen gas", "an element"), ("mercury", "an element"), ("graphite", "an element"),
         ("pure water", "a compound"), ("carbon dioxide", "a compound"), ("common salt (sodium chloride)", "a compound"), ("iron sulphide", "a compound"), ("sugar (sucrose)", "a compound"), ("ammonia", "a compound"),
         ("salt dissolved in water", "a homogeneous mixture"), ("air", "a homogeneous mixture"), ("brass", "a homogeneous mixture"), ("soda water", "a homogeneous mixture"), ("vinegar", "a homogeneous mixture"),
         ("sand and water", "a heterogeneous mixture"), ("iron filings and sulphur powder", "a heterogeneous mixture"), ("oil and water", "a heterogeneous mixture"), ("soil", "a heterogeneous mixture"), ("chalk powder in water", "a heterogeneous mixture"), ("glucose", "a compound"), ("copper", "an element"), ("sea water", "a homogeneous mixture"), ("a fruit salad", "a heterogeneous mixture"), ("nitrogen gas", "an element"), ("steel", "a homogeneous mixture")]
SUS = [("sugar dissolved in water", "a true solution"), ("salt dissolved in water", "a true solution"), ("copper sulphate in water", "a true solution"), ("soda water", "a true solution"),
       ("chalk powder in water", "a suspension"), ("muddy river water", "a suspension"), ("sand stirred in water", "a suspension"), ("flour mixed in water", "a suspension"),
       ("milk", "a colloid"), ("fog", "a colloid"), ("shaving cream", "a colloid"), ("butter", "a colloid"), ("smoke", "a colloid"), ("starch solution", "a colloid"), ("lemonade without pulp", "a true solution"), ("ink (blue)", "a colloid"), ("paint stirred in water", "a suspension"), ("glucose dissolved in water", "a true solution"), ("cloud", "a colloid")]
COLL = [("fog", "aerosol (liquid in gas)"), ("clouds", "aerosol (liquid in gas)"), ("smoke", "aerosol (solid in gas)"), ("car exhaust", "aerosol (solid in gas)"),
        ("milk", "emulsion (liquid in liquid)"), ("face cream", "emulsion (liquid in liquid)"), ("shaving cream", "foam (gas in liquid)"), ("foam rubber", "foam (gas in solid)"), ("sponge", "foam (gas in solid)"),
        ("jelly", "gel (liquid in solid)"), ("cheese", "gel (liquid in solid)"), ("butter", "gel (liquid in solid)"), ("milk of magnesia", "sol (solid in liquid)"), ("mud", "sol (solid in liquid)"), ("coloured gemstone", "solid sol (solid in solid)")]
CHG = {"a physical change": ["ice melting", "water boiling", "sugar dissolving in water", "glass breaking", "wax melting", "iodine subliming", "paper being cut", "a rubber band stretching", "water freezing", "a metal wire being bent"],
       "a chemical change": ["iron rusting", "wood burning", "milk turning into curd", "food being cooked", "a candle wick burning", "fruit ripening", "food being digested", "magnesium burning", "silver tarnishing", "baking soda reacting with vinegar"]}
PURE = [("What is a pure substance?", "a substance made of only one kind of particle", ["any substance that looks clean", "a mixture of two elements", "anything in a sealed bottle"], "Elements and compounds are pure substances."),
        ("Which property is shown by a mixture but not by a compound?", "its components keep their own properties", ["it has a fixed composition", "it forms with heat or light", "it cannot be separated physically"], "In iron sulphide, iron is no longer magnetic."),
        ("Why is a solution stable?", "the solute particles do not settle down", ["the solute particles are very heavy", "it has no solvent", "it scatters light"], "Its particles are smaller than 1 nm."),
        ("What is the Tyndall effect?", "scattering of a beam of light by colloid particles", ["the settling of a suspension", "the dissolving of sugar", "the boiling of a solution"], "A true solution does not show it."),
        ("What is a saturated solution?", "a solution in which no more solute can dissolve at that temperature", ["a solution with no solute", "any coloured solution", "a solution that has boiled"], "Heating usually lets more solute dissolve."),
        ("What is the solubility of a substance?", "the amount of it that dissolves in 100 g of solvent to make a saturated solution at a given temperature", ["the mass of the solvent", "the boiling point of the solution", "the colour of the solution"], "It changes with temperature."),
        ("Which of these is an alloy?", "brass", ["sodium chloride", "water", "mercury"], "Brass is about 30% zinc and 70% copper; an alloy is a mixture."),
        ("Which is a physical change?", "ice melting", ["iron rusting", "wood burning", "milk turning sour"], "No new substance is formed."),
        ("Which is a chemical change?", "burning of a candle wick", ["melting of wax", "dissolving salt", "breaking glass"], "Burning makes new substances."),
        ("Why can a suspension be separated by filtration?", "its particles are big enough to be stopped by filter paper", ["its particles are smaller than 1 nm", "it is a pure substance", "it is a compound"], "Colloid particles pass through filter paper."),
        ("Which is the dispersed phase in milk?", "fat droplets", ["water", "air", "sugar"], "Water is the dispersion medium."),
        ("Why is air a mixture and not a compound?", "its gases keep their properties and its composition can change", ["it is invisible", "it cannot be separated", "it has a fixed formula"], "Its composition changes from place to place."),
        ("Which gas forms about 78% of air by volume?", "nitrogen", ["oxygen", "argon", "carbon dioxide"], "Oxygen is about 21%."),
        ("What is a metalloid?", "an element with properties between metals and non-metals", ["a metal alloy", "a liquid metal", "a gas"], "Boron, silicon and germanium are metalloids."),
        ("Which non-metal is a liquid at room temperature?", "bromine", ["mercury", "iodine", "sulphur"], "Mercury is the liquid metal."),
        ("Which property is typical of metals?", "they are ductile and conduct electricity", ["they are brittle", "they are dull", "they do not conduct heat"], "Metals are also lustrous and sonorous."),
        ("Is a 5% solution of sugar homogeneous or heterogeneous?", "homogeneous", ["heterogeneous", "it is a compound", "it is a suspension"], "It is uniform throughout."),
        ("What is the solvent in tincture of iodine?", "alcohol", ["water", "iodine", "oil"], "Iodine is the solute."),
        ("Why does a compound need a chemical reaction to be separated into its elements?", "its elements are chemically joined in a fixed ratio", ["it is a mixture", "it is a solid", "it is coloured"], "Water can be split by electrolysis."),
        ("In which mixture are the components visible separately?", "a heterogeneous mixture", ["a homogeneous mixture", "a compound", "an element"], "Sand in water is an example."),
        ("What is the dispersion medium in fog?", "air (a gas)", ["water (a liquid)", "dust (a solid)", "smoke"], "Fog is liquid droplets dispersed in air.")]


def _commas(f):
    import re
    def g(*a):
        it = f(*a)
        if it:
            for key in ("q", "e"):
                it[key] = re.sub(r"(?<![\d.,])(\d{4,})(?![\d.,])", lambda m: "{:,}".format(int(m.group())), it[key])
        return it
    g.__name__ = f.__name__
    return g


@_commas
def c_conc(k=None):
    R = _R[0]
    k = k or ch(["mm", "mm2", "solute", "mv"])
    nm = name()
    solute = ch(["sugar", "salt", "urea", "glucose", "copper sulphate", "potassium nitrate"])
    if k == "mm":
        a = R.choice([5, 10, 12, 15, 20, 25, 30, 40, 50])
        w = R.choice([70, 80, 90, 100, 110, 120, 150, 175, 200, 220, 250])
        p = a / (a + w) * 100
        return nq("%s dissolves %d g of %s in %d g of water. What is the concentration of the solution in mass by mass percentage?" % (nm, a, solute, w), p, [a / w * 100, w / (a + w) * 100, a / (a + w)], "%",
                  "Mass of solution = %d + %d = %d g; %d ÷ %d × 100 = <b>%s%%</b>." % (a, w, a + w, a, a + w, nf(p)))
    if k == "mm2":
        m = R.choice([200, 250, 300, 400, 500, 800, 1000])
        a = R.choice([10, 20, 25, 40, 50, 60, 80])
        if a >= m / 2:
            return None
        p = a / m * 100
        return nq("A solution of mass %d g contains %d g of %s. What is its mass by mass percentage concentration?" % (m, a, solute), p, [a / (m + a) * 100, m / a, (m - a) / m * 100], "%",
                  "%d ÷ %d × 100 = <b>%s%%</b> (divide by the mass of the solution)." % (a, m, nf(p)))
    if k == "solute":
        p = R.choice([2, 4, 5, 8, 10, 12, 15, 20, 25])
        m = R.choice([100, 200, 250, 400, 500, 1000])
        a = p * m / 100
        return nq("How much %s is needed to make %d g of a %d%% (mass by mass) solution?" % (solute, m, p), a, [p, m - a, a * 10], " g",
                  "%d%% of %d g = <b>%s g</b> of %s; the rest, %s g, is water." % (p, m, nf(a), solute, nf(m - a)))
    a = R.choice([2, 5, 10, 15, 20, 25, 30, 50])
    v = R.choice([100, 200, 250, 400, 500, 1000])
    p = a / v * 100
    return nq("%d g of %s is dissolved to make %d mL of solution. What is its mass by volume percentage?" % (a, solute, v), p, [v / a, a / v, a / (v + a) * 100], "%",
              "Mass of solute ÷ volume of solution × 100 = %d ÷ %d × 100 = <b>%s%%</b>." % (a, v, nf(p)))


# =================================================================== Chapter 3: atoms and molecules
SYM = [("hydrogen", "H"), ("helium", "He"), ("carbon", "C"), ("nitrogen", "N"), ("oxygen", "O"), ("fluorine", "F"), ("neon", "Ne"), ("sodium", "Na"), ("magnesium", "Mg"),
       ("aluminium", "Al"), ("silicon", "Si"), ("phosphorus", "P"), ("sulphur", "S"), ("chlorine", "Cl"), ("argon", "Ar"), ("potassium", "K"), ("calcium", "Ca"),
       ("iron", "Fe"), ("copper", "Cu"), ("zinc", "Zn"), ("silver", "Ag"), ("gold", "Au"), ("lead", "Pb"), ("mercury", "Hg"), ("iodine", "I"), ("bromine", "Br"), ("cobalt", "Co")]
CAT = [("sodium", "Na", 1), ("potassium", "K", 1), ("silver", "Ag", 1), ("ammonium", "NH4", 1), ("hydrogen", "H", 1), ("copper(II)", "Cu", 2), ("magnesium", "Mg", 2),
       ("calcium", "Ca", 2), ("zinc", "Zn", 2), ("iron(II)", "Fe", 2), ("iron(III)", "Fe", 3), ("aluminium", "Al", 3)]
AN = [("chloride", "Cl", 1), ("bromide", "Br", 1), ("hydroxide", "OH", 1), ("nitrate", "NO3", 1), ("hydrogencarbonate", "HCO3", 1), ("oxide", "O", 2), ("sulphide", "S", 2),
      ("sulphate", "SO4", 2), ("carbonate", "CO3", 2), ("phosphate", "PO4", 3)]
POLY = {"NH4", "OH", "NO3", "HCO3", "SO4", "CO3", "PO4"}


def formula(c, a):
    from math import gcd
    (cn, cs, cv), (an, as_, av) = c, a
    g = gcd(cv, av)
    nc, na = av // g, cv // g

    def part(s, k):
        if k == 1:
            return s
        return ("(%s)%d" % (s, k)) if s in POLY else "%s%d" % (s, k)
    return part(cs, nc) + part(as_, na)


def c_formula(k=None):
    R = _R[0]
    c, a = ch(CAT), ch(AN)
    if c[1] == "H" and a[1] in ("OH", "HCO3", "O"):
        return None
    if c[1] == "NH4" and a[1] in ("OH", "O", "HCO3"):
        return None
    right = formula(c, a)
    flip = formula((c[0], c[1], a[2]), (a[0], a[1], c[2]))
    plain = c[1] + a[1]
    nob = right.replace("(", "").replace(")", "")
    ws = [sub(x) for x in sorted({flip, plain, nob, formula((c[0], c[1], 1), (a[0], a[1], 1)) if c[2] != a[2] else plain + "2"}) if x != right]
    nm_ = "%s %s" % (c[0], a[0])
    if c[1] == "H":
        nm_ = "hydrogen %s" % a[0]
    return tq("Write the formula of %s. (Valency of %s = %d, %s = %d)" % (nm_, c[0], c[2], a[0], a[2]), sub(right), ws,
              "Cross over the valencies: %s<sup>%d</sup> and %s<sup>%d</sup> give <b>%s</b>%s." % (sub(c[1]), c[2], sub(a[1]), a[2], sub(right), " (brackets keep a polyatomic ion together)" if "(" in right else ""))


MOLF = ["H2O", "CO2", "NH3", "CH4", "HCl", "H2SO4", "HNO3", "NaCl", "CaCO3", "MgO", "Na2CO3", "C2H5OH", "C6H12O6", "CaCl2", "Al2O3", "Fe2O3", "SO2", "NaOH", "KCl", "CuO",
        "MgCl2", "Na2SO4", "Ca(OH)2", "Al2(SO4)3", "K2CO3", "ZnO", "N2", "O2", "Cl2", "CH3COOH", "C2H6", "C12H22O11", "P4O10"]
AM9 = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "Al": 27, "S": 32, "Cl": 35.5, "K": 39, "Ca": 40, "Fe": 56, "Cu": 63.5, "Zn": 65, "P": 31}


def c_mass(k=None):
    from sci_chem import atoms
    f = ch(MOLF)
    if any(e not in AM9 for e in atoms(f)):
        return None
    at = atoms(f)
    m = sum(AM9[e] * n for e, n in at.items())
    simple = sum(AM9[e] for e in at)
    wrong2 = sum(AM9[e] * n for e, n in at.items() if e != "O") + 8 * at.get("O", 0)
    wrong3 = sum(n for n in at.values())
    use = "formula unit mass" if f[:2] in ("Na", "Ca", "Mg", "Al", "Fe", "K2", "Zn", "Cu", "KC") else "molecular mass"
    given = ", ".join("%s = %s u" % (e, nf(AM9[e])) for e in at)
    return nq("Find the %s of %s. (%s)" % (use, sub(f), given), m, [simple, wrong2, m * 2, wrong3 * 12], " u",
              "%s = <b>%s u</b>." % (" + ".join("%d × %s" % (n, nf(AM9[e])) if n > 1 else nf(AM9[e]) for e, n in at.items()), nf(m)))


NA = 6.022e23


def c_mole(k=None):
    R = _R[0]
    from sci_chem import atoms
    k = k or ch(["n", "mass", "particles", "fromN"])
    f = ch(["H2O", "CO2", "NH3", "CH4", "O2", "N2", "NaCl", "CaCO3", "HCl", "C", "Na", "Mg", "Fe", "Al", "S", "Ca", "Zn"])
    at = atoms(f)
    M = sum(AM9[e] * n for e, n in at.items())
    show = "molar mass of %s = %s g/mol" % (sub(f), nf(M))
    if k == "n":
        n = R.choice([0.1, 0.2, 0.25, 0.5, 1.5, 2, 2.5, 3, 4, 5])
        m = n * M
        return nq("How many moles are there in %s g of %s? (%s)" % (nf(m), sub(f), show), n, [m * M, M / m, n * 2], " mol",
                  "n = mass ÷ molar mass = %s ÷ %s = <b>%s mol</b>." % (nf(m), nf(M), nf(n)))
    if k == "mass":
        n = R.choice([0.1, 0.2, 0.25, 0.5, 1.5, 2, 2.5, 3, 4, 5])
        m = n * M
        return nq("What is the mass of %s mol of %s? (%s)" % (nf(n), sub(f), show), m, [M / n, M, n / M], " g",
                  "mass = n × molar mass = %s × %s = <b>%s g</b>." % (nf(n), nf(M), nf(m)))
    if k == "particles":
        n = R.choice([0.1, 0.2, 0.25, 0.5, 2, 3, 4, 5])
        m = n * M
        what = "atoms" if len(at) == 1 and list(at.values())[0] == 1 else "molecules" if f not in ("NaCl", "CaCO3") else "formula units"
        return nq("How many %s are there in %s g of %s? (%s, N<sub>0</sub> = 6.022 × 10<sup>23</sup>)" % (what, nf(m), sub(f), show), n * NA, [m * NA, NA / n, M * NA], "",
                  "n = %s ÷ %s = %s mol; number = %s × 6.022 × 10<sup>23</sup> = <b>%s</b>." % (nf(m), nf(M), nf(n), nf(n), nf(n * NA)))
    n = R.choice([0.5, 1, 2, 3, 5, 0.25, 0.1])
    N = n * NA
    return nq("How many moles is %s particles of %s? (N<sub>0</sub> = 6.022 × 10<sup>23</sup>)" % (nf(N), sub(f)), n, [N * NA / 1e46, n * 10, n / 10, NA / N * 10], " mol",
              "n = %s ÷ 6.022 × 10<sup>23</sup> = <b>%s mol</b>." % (nf(N), nf(n)))


RATIO = [("water", "hydrogen", "oxygen", 1, 8), ("carbon dioxide", "carbon", "oxygen", 3, 8), ("ammonia", "nitrogen", "hydrogen", 14, 3), ("magnesium oxide", "magnesium", "oxygen", 3, 2),
         ("calcium oxide", "calcium", "oxygen", 5, 2), ("sulphur dioxide", "sulphur", "oxygen", 1, 1), ("hydrogen chloride", "hydrogen", "chlorine", 2, 71)]


def c_law(k=None):
    R = _R[0]
    k = k or ch(["ratio", "cons"])
    if k == "ratio":
        cpd, a, b, x, y = ch(RATIO)
        t = R.choice([1, 2, 3, 4, 5, 6, 10, 0.5])
        ma = x * t
        mb = y * t
        return nq("In %s, %s and %s always combine in the mass ratio %d : %d. What mass of %s combines with %s g of %s?" % (cpd, a, b, x, y, b, nf(ma), a), mb, [ma * x / y, ma + y, mb / 2, ma * y], " g",
                  "Law of constant proportions: %s × %d ÷ %d = <b>%s g</b> of %s." % (nf(ma), y, x, nf(mb), b))
    a = R.choice([5.3, 4.2, 6.0, 8.4, 10.6, 2.65])
    b = R.choice([6.0, 7.3, 9.8, 3.65, 4.9])
    c = round(a * R.choice([0.5, 0.6, 0.7, 0.8]), 1)
    d = round(a + b - c, 2)
    return nq("%s g of sodium carbonate reacts with %s g of ethanoic acid, giving %s g of carbon dioxide and the rest as water and sodium ethanoate. What is the total mass of water and sodium ethanoate?" % (nf(a), nf(b), nf(c)),
           d, [a + b, a + b + c, abs(a - b), d / 2], " g", "Law of conservation of mass: total mass of products = %s + %s = %s g, so %s − %s = <b>%s g</b>." % (nf(a), nf(b), nf(a + b), nf(a + b), nf(c), nf(d)))


ATOM = [("Who proposed the atomic theory of matter in 1808?", "John Dalton", ["J. J. Thomson", "Ernest Rutherford", "Antoine Lavoisier"], "Dalton said matter is made of indivisible atoms."),
        ("Which law did Lavoisier establish?", "the law of conservation of mass", ["the law of constant proportions", "Ohm's law", "the law of gravitation"], "Proust gave the law of constant proportions."),
        ("Who gave the law of constant proportions?", "Joseph L. Proust", ["John Dalton", "Lavoisier", "Niels Bohr"], "A compound always has its elements in the same mass ratio."),
        ("What is the symbol of sodium, from its Latin name natrium?", "Na", ["So", "Sd", "S"], "Potassium is K from kalium."),
        ("Which element has the symbol Fe, from its Latin name ferrum?", "iron", ["fluorine", "fermium", "francium"], "Copper is Cu from cuprum."),
        ("What is atomicity?", "the number of atoms in one molecule", ["the mass of an atom", "the charge on an atom", "the size of an atom"], "O₂ has atomicity 2, O₃ has 3."),
        ("What is the atomicity of ozone, O₃?", "3 (triatomic)", ["2 (diatomic)", "1 (monoatomic)", "4 (tetra-atomic)"], "Oxygen gas, O₂, is diatomic."),
        ("Which element exists as single atoms (monoatomic)?", "argon", ["oxygen", "nitrogen", "chlorine"], "Noble gases are monoatomic."),
        ("What is the atomicity of phosphorus, P₄?", "4 (tetra-atomic)", ["1 (monoatomic)", "2 (diatomic)", "8 (polyatomic)"], "Sulphur is S₈."),
        ("What is one atomic mass unit (u)?", "one-twelfth of the mass of one carbon-12 atom", ["the mass of one hydrogen molecule", "the mass of one electron", "1 gram"], "It was earlier called amu."),
        ("What is an ion?", "a charged atom or group of atoms", ["a neutral molecule", "a very small atom", "a mixture"], "Cations are positive, anions negative."),
        ("What is a polyatomic ion?", "a group of atoms that carries a charge", ["a single charged atom", "a neutral molecule", "a large atom"], "Examples: SO₄²⁻, NH₄⁺, CO₃²⁻."),
        ("What is valency?", "the combining capacity of an element", ["the mass of an element", "the number of neutrons", "the size of an atom"], "Hydrogen has valency 1, oxygen 2."),
        ("What is the valency of oxygen?", "2", ["1", "3", "4"], "So water is H₂O."),
        ("What is the valency of carbon in CH₄?", "4", ["1", "2", "3"], "Carbon forms four bonds."),
        ("Which is a positively charged ion?", "NH₄⁺ (ammonium)", ["Cl⁻ (chloride)", "OH⁻ (hydroxide)", "SO₄²⁻ (sulphate)"], "Positive ions are cations."),
        ("Why can we not see an atom with our eyes?", "an atom is extremely small, with a radius of about 10⁻¹⁰ m", ["atoms are invisible gases", "atoms are always moving too fast", "atoms have no mass"], "Modern techniques can image atoms' surfaces."),
        ("Which postulate of Dalton's theory explains the law of conservation of mass?", "atoms are neither created nor destroyed in a chemical reaction", ["atoms of an element are identical", "atoms combine in whole-number ratios", "atoms are very small"], "They are only rearranged."),
        ("Which postulate of Dalton's theory explains the law of constant proportions?", "atoms combine in a fixed whole-number ratio to form compounds", ["atoms cannot be created", "atoms are indivisible", "atoms of different elements differ in mass"], "So the mass ratio is fixed."),
        ("What is one mole?", "the amount that contains 6.022 × 10²³ particles", ["1 gram of any substance", "1 litre of gas", "the mass of one atom"], "This number is Avogadro's number."),
        ("What is the molar mass of a substance?", "the mass of 1 mole of it in grams", ["the mass of one molecule in grams", "the volume of 1 mole", "its atomic number"], "Its value equals the atomic or molecular mass in u."),
        ("Which pair has the same number of atoms?", "1 mole of sodium and 1 mole of magnesium", ["1 g of sodium and 1 g of magnesium", "1 mole of sodium and 1 g of magnesium", "1 g of sodium and 1 mole of magnesium"], "A mole always has 6.022 × 10²³ particles."),
        ("What is the formula of calcium oxide?", "CaO", ["Ca₂O", "CaO₂", "Ca₂O₂"], "Both have valency 2, so the ratio is 1 : 1."),
        ("What is the formula unit mass of NaCl? (Na = 23 u, Cl = 35.5 u)", "58.5 u", ["23 u", "35.5 u", "12.5 u"], "Ionic compounds have formula units, not molecules."),
        ("Which element has the symbol Ag?", "silver", ["gold", "aluminium", "argon"], "From argentum."),
        ("Which element has the symbol Pb?", "lead", ["phosphorus", "lead oxide", "platinum"], "From plumbum.")]


# =================================================================== Chapter 4: structure of the atom
E20 = [("hydrogen", "H", 1, 1), ("helium", "He", 2, 4), ("lithium", "Li", 3, 7), ("beryllium", "Be", 4, 9), ("boron", "B", 5, 11), ("carbon", "C", 6, 12), ("nitrogen", "N", 7, 14),
       ("oxygen", "O", 8, 16), ("fluorine", "F", 9, 19), ("neon", "Ne", 10, 20), ("sodium", "Na", 11, 23), ("magnesium", "Mg", 12, 24), ("aluminium", "Al", 13, 27),
       ("silicon", "Si", 14, 28), ("phosphorus", "P", 15, 31), ("sulphur", "S", 16, 32), ("chlorine", "Cl", 17, 35), ("argon", "Ar", 18, 40), ("potassium", "K", 19, 39), ("calcium", "Ca", 20, 40)]


def shells(z):
    out = []
    for cap in (2, 8, 8, 2):
        t = min(cap, z)
        out.append(t)
        z -= t
        if z == 0:
            break
    return out


def val(z):
    v = shells(z)[-1]
    if z in (2, 10, 18):
        return 0
    return v if v <= 4 else 8 - v


def cfg(z):
    return ", ".join(str(x) for x in shells(z))


def c_atom(k=None):
    R = _R[0]
    k = k or ch(["n", "p", "cfg", "val", "z", "e"])
    nm_, s, z, a = ch(E20)
    nuc = "<sup>%d</sup><sub>%d</sub>%s" % (a, z, s)
    if k == "n":
        return nq("How many neutrons are there in an atom of %s, %s?" % (nm_, nuc), a - z, [a, z, a + z, a - z + 1, a - z - 1, a + 1], "", "Neutrons = mass number − atomic number = %d − %d = <b>%d</b>." % (a, z, a - z))
    if k == "p":
        return nq("An atom of %s has mass number %d and %d neutrons. How many protons does it have?" % (nm_, a, a - z), z, [a, a - z, a + (a - z), z + 1, z - 1, a + 1], "", "Protons = %d − %d = <b>%d</b> (the atomic number)." % (a, a - z, z))
    if k == "e":
        return nq("How many electrons are there in a neutral atom of %s (atomic number %d, mass number %d)?" % (nm_, z, a), z, [a, a - z, z + 1, z - 1, a + z, z + 2], "", "A neutral atom has as many electrons as protons: <b>%d</b>." % z)
    if k == "cfg":
        wrong = set()
        for zz in (z - 1, z + 1, z + 2):
            if 1 <= zz <= 20:
                wrong.add(cfg(zz))
        sh = shells(z)
        if len(sh) > 1:
            wrong.add(", ".join(str(x) for x in [sh[0], sum(sh[1:])]) if sum(sh[1:]) <= 18 else "")
            if z > 18:
                wrong.add("2, 8, %d" % (z - 10))
        wrong.discard(cfg(z))
        wrong.discard("")
        return tq("What is the electronic configuration of %s (atomic number %d)?" % (nm_, z), cfg(z), sorted(wrong), "Fill shells K, L, M, N with 2, 8, 8 …: <b>%s</b>." % cfg(z))
    if k == "val":
        v = val(z)
        return nq("The electronic configuration of %s is %s. What is its valency?" % (nm_, cfg(z)), v, [shells(z)[-1], 8 - shells(z)[-1], len(shells(z)), v + 1, v + 2, abs(v - 1), 8], "",
                  "%s outer electron%s, so the valency is <b>%d</b>%s." % (shells(z)[-1], "" if shells(z)[-1] == 1 else "s", v, " (it needs %d more for an octet)" % v if shells(z)[-1] > 4 and v else ""))
    return tq("Which element has the electronic configuration %s?" % cfg(z), nm_, [x[0] for x in E20 if abs(x[2] - z) in (1, 2, 8)][:4], "%s electrons in all, so the atomic number is %d: <b>%s</b>." % (" + ".join(str(x) for x in shells(z)), z, nm_))


ISO = [("chlorine", 35, 37), ("bromine", 79, 81), ("copper", 63, 65), ("boron", 10, 11), ("lithium", 6, 7), ("gallium", 69, 71)]


def c_avg(k=None):
    R = _R[0]
    el, a, b = ch(ISO)
    p = R.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
    m = (a * p + b * (100 - p)) / 100
    return nq("A sample of %s has %d%% of atoms of mass %d u and %d%% of mass %d u. What is its average atomic mass?" % (el, p, a, 100 - p, b), m, [(a + b) / 2, (a * (100 - p) + b * p) / 100, a + b], " u",
              "%d × %s + %d × %s = <b>%s u</b>." % (a, nf(p / 100, 2), b, nf((100 - p) / 100, 2), nf(m)), sf=4) if p != 50 else None


MODEL = [("J. J. Thomson", "the electron, and the 'plum pudding' model of the atom"), ("Ernest Rutherford", "the nucleus, from the alpha-particle scattering experiment"),
         ("Niels Bohr", "electrons revolving in fixed orbits (shells) without radiating energy"), ("James Chadwick", "the neutron, in 1932"), ("E. Goldstein", "canal rays, which led to the proton")]
STRUCT = [("What did Rutherford see when alpha particles hit a thin gold foil?", "most passed straight through, a few were deflected and very few bounced back", ["all bounced back", "all were absorbed", "all were deflected"], "So most of the atom is empty space with a small dense nucleus."),
          ("Why was gold foil used in Rutherford's experiment?", "gold can be beaten into a very thin layer", ["gold is magnetic", "gold is cheap", "gold is radioactive"], "The foil was about 1,000 atoms thick."),
          ("What is the charge and mass of an electron?", "−1 charge and almost negligible mass (about 1/2,000 of a proton)", ["+1 charge and 1 u", "no charge and 1 u", "−1 charge and 1 u"], "Protons are +1, neutrons have no charge; both are about 1 u."),
          ("What is the atomic number of an element?", "the number of protons in its nucleus", ["the number of neutrons", "the sum of protons and neutrons", "the number of shells"], "It is written as Z."),
          ("What is the mass number?", "the total number of protons and neutrons in the nucleus", ["the number of electrons", "the number of protons only", "the atomic number doubled"], "It is written as A."),
          ("What are isotopes?", "atoms of the same element with the same atomic number but different mass numbers", ["atoms of different elements with the same mass number", "ions of an element", "molecules of an element"], "Carbon-12 and carbon-14 are isotopes."),
          ("What are isobars?", "atoms of different elements with the same mass number", ["atoms with the same atomic number", "ions with the same charge", "elements in the same group"], "Calcium-40 and argon-40 are isobars."),
          ("Which pair are isobars?", "⁴⁰₂₀Ca and ⁴⁰₁₈Ar", ["¹²₆C and ¹⁴₆C", "³⁵₁₇Cl and ³⁷₁₇Cl", "¹H and ²H"], "Same mass number, different atomic numbers."),
          ("Which pair are isotopes?", "³⁵₁₇Cl and ³⁷₁₇Cl", ["⁴⁰₂₀Ca and ⁴⁰₁₈Ar", "¹⁴₇N and ¹⁴₆C", "²³₁₁Na and ²⁴₁₂Mg"], "Same atomic number, different mass numbers."),
          ("Which isotope is used to treat goitre?", "an isotope of iodine", ["an isotope of uranium", "an isotope of cobalt", "carbon-12"], "Cobalt isotopes are used for cancer; uranium for nuclear reactors."),
          ("Which isotope is used as fuel in nuclear reactors?", "an isotope of uranium", ["an isotope of iodine", "an isotope of hydrogen", "an isotope of chlorine"], "Uranium-235 splits and releases energy."),
          ("What is the maximum number of electrons in the second (L) shell?", "8", ["2", "18", "32"], "The rule is 2n²: for n = 2, 2 × 4 = 8."),
          ("What is the maximum number of electrons in the M shell according to 2n²?", "18", ["8", "2", "32"], "But the outermost shell holds no more than 8."),
          ("What are valence electrons?", "the electrons in the outermost shell", ["the electrons in the innermost shell", "the protons", "all the electrons"], "They decide how an atom reacts."),
          ("Why are noble gases unreactive?", "their outermost shell is full (an octet, or a duplet for helium)", ["they have no electrons", "they are too heavy", "they have no nucleus"], "Their valency is zero."),
          ("What was a problem with Rutherford's model?", "a revolving electron should lose energy and fall into the nucleus", ["it had no nucleus", "it had no electrons", "it said atoms are solid"], "Bohr solved this with fixed orbits."),
          ("What did Thomson's model compare the atom to?", "a Christmas pudding (a watermelon), with electrons like seeds in a positive sphere", ["a solar system", "an empty box", "a hard ball"], "It could not explain the scattering experiment."),
          ("Why do isotopes have the same chemical properties?", "they have the same electronic configuration", ["they have the same mass", "they have the same number of neutrons", "they are radioactive"], "Their physical properties differ."),
          ("Where is almost all of the mass of an atom?", "in the nucleus", ["in the electrons", "spread evenly through the atom", "in the empty space"], "Protons and neutrons are much heavier than electrons."),
          ("What are nucleons?", "protons and neutrons", ["electrons and protons", "electrons only", "neutrons and electrons"], "They are the particles in the nucleus."),
          ("Why is an atom neutral overall?", "it has equal numbers of protons and electrons", ["it has no particles with charge", "it has more neutrons", "it has no electrons"], "The charges cancel."),
          ("An atom has 3 electrons in its outermost shell. What is its valency?", "3", ["5", "8", "1"], "It loses 3 electrons, like aluminium."),
          ("An atom has 7 electrons in its outermost shell. What is its valency?", "1", ["7", "8", "2"], "It gains 1 electron, like chlorine.")]


def UNITS9a():
    MA = "Matter – Its Nature and Behaviour"
    b = {n: once_maker(v) for n, v in [("mat", MAT1), ("pure", PURE), ("atom", ATOM), ("str", STRUCT)]}
    proc = pairs(PROC, "What is the name of %s?", "What happens in %s?")
    pex = pairs(PROC_EX, "%s Which process is this?")
    cls = pairs(CLASS, "Which best describes %s: an element, a compound, a homogeneous mixture or a heterogeneous mixture?")
    from in_sci9b import odd_one
    chg = odd_one(CHG, "Which of these is %s?", "Which of these is not %s?")
    sus = pairs(SUS, "Is %s a true solution, a suspension or a colloid?", pool=["a pure compound"])
    coll = pairs(COLL, "What type of colloid is %s?")
    sym = pairs(SYM, "What is the symbol of %s?", "Which element has the symbol %s?")
    mod = pairs(MODEL, "What did %s discover or propose?", "Who discovered or proposed %s?")
    return [
        U(1, "matter-in-our-surroundings", 1, MA,
          "Matter in Our Surroundings: Definition of matter; Particulate Nature of Matter; States of Matter: solid, liquid and gas and their characteristics; change of state – melting (absorption of heat), freezing, evaporation (cooling by evaporation), condensation, sublimation.",
          "Matter in Our Surroundings", "matter in our surroundings",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 1: states of matter, particles, diffusion, Kelvin and Celsius, melting and boiling points, latent heat, sublimation and evaporation. 100 questions with answers.",
          "Matter is made of tiny particles that are always moving.", "Kelvin = Celsius + 273.",
          "<p>Matter has mass and takes up space. Its particles are very small, have spaces between them, keep moving and attract each other. In solids the particles are packed tightly and only vibrate; in liquids they slide past each other; in gases they move freely and fast.</p>"
          "<p>Heating gives particles more energy, so solids melt and liquids boil; the temperature stays constant during a change of state because the heat (latent heat) is used to overcome the attraction between particles. Some solids such as camphor sublime. Evaporation happens at any temperature and causes cooling.</p>",
          [("Convert 25 °C to kelvin.", ["add 273"], "298 K"), ("Why does the temperature stay at 0 °C while ice melts?", ["heat is used to separate particles"], "latent heat of fusion")],
          ["Forgetting to add (not subtract) 273 when changing °C to K.", "Thinking evaporation happens only at the boiling point.", "Saying the temperature rises while ice is melting."],
          [("What is the difference between evaporation and boiling?", "Evaporation happens at any temperature from the surface; boiling happens throughout the liquid at the boiling point."),
           ("Why does evaporation cause cooling?", "The fastest particles escape, and the liquid takes heat from its surroundings to replace the energy lost.")],
          lambda: [("States of matter", [(c_state, 14), (b["mat"], 6)]), ("Celsius and Kelvin", [(c_temp, 20)]), ("Changes of state", [(proc, 10), (pex, 10)]),
                   ("Evaporation and latent heat", [(b["mat"], 14), (c_state, 6)]), ("Mixed problems", [(pex, 2), (c_temp, 8), (b["mat"], 2), (c_state, 8)])]),
        U(2, "is-matter-around-us-pure", 2, MA,
          "Is Matter Around Us Pure: Elements, compounds and mixtures. Heterogeneous and homogeneous mixtures, colloids and suspensions. Physical and chemical changes (excluding separating the components of a mixture); Pure and Impure substances.",
          "Is Matter Around Us Pure?", "is matter around us pure",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 2: elements, compounds and mixtures, solutions, concentration, suspensions, colloids and the Tyndall effect, and physical and chemical changes. 100 questions with answers.",
          "A pure substance has only one kind of particle.", "Mass % = mass of solute ÷ mass of solution × 100.",
          "<p>Pure substances are elements (one kind of atom) and compounds (elements joined chemically in a fixed ratio). Mixtures keep the properties of their parts: homogeneous mixtures (solutions such as salt water and air) are uniform, heterogeneous ones (sand and water) are not.</p>"
          "<p>A true solution has particles smaller than 1 nm and does not scatter light; a colloid scatters light (the Tyndall effect) but does not settle; a suspension settles and can be filtered. Concentration is the amount of solute in a given amount of solution, for example mass by mass percentage.</p>",
          [("20 g of salt in 180 g of water. Mass %?", ["solution = 200 g", "20 ÷ 200 × 100"], "10%"), ("Is milk a solution, suspension or colloid?", ["it scatters light but does not settle"], "a colloid")],
          ["Dividing by the mass of the solvent instead of the solution.", "Calling air a compound.", "Saying colloids settle like suspensions."],
          [("Is water an element, a compound or a mixture?", "Pure water is a compound of hydrogen and oxygen in a fixed ratio by mass (1 : 8)."),
           ("What is the Tyndall effect?", "The scattering of a beam of light by the particles of a colloid, which makes the path of the beam visible.")],
          lambda: [("Elements, compounds and mixtures", [(cls, 20)]), ("Concentration of solutions", [(c_conc, 20)]), ("Solutions, suspensions and colloids", [(sus, 12), (coll, 8)]),
                   ("Physical and chemical changes", [(chg, 14), (b["pure"], 6)]), ("Mixed problems", [(b["pure"], 12), (c_conc, 4), (coll, 4)])]),
        U(3, "atoms-and-molecules", 3, MA,
          "Atoms and Molecules: Atoms and molecules, Law of Chemical Combination, Chemical formula of common compounds, Atomic and molecular masses.",
          "Atoms and Molecules", "atoms and molecules",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 3: laws of chemical combination, Dalton's theory, symbols, valency and chemical formulae, molecular and formula unit mass, and the mole concept. 100 questions with answers.",
          "Cross over the valencies to write a formula.", "1 mole = 6.022 × 10²³ particles; n = mass ÷ molar mass.",
          "<p>Mass is neither created nor destroyed in a reaction (law of conservation of mass), and a compound always has its elements in the same ratio by mass (law of constant proportions). Dalton explained both with atoms.</p>"
          "<p>To write a formula, cross over the valencies of the ions (Al³⁺ and O²⁻ give Al₂O₃). Molecular mass is the sum of the atomic masses of all atoms in a molecule. One mole of anything has 6.022 × 10²³ particles, and its mass in grams equals the atomic or molecular mass in u.</p>",
          [("Formula of aluminium sulphate?", ["Al³⁺ and SO₄²⁻", "cross over: Al₂(SO₄)₃"], "Al₂(SO₄)₃"), ("Moles in 36 g of water?", ["M = 18 g/mol", "36 ÷ 18"], "2 mol")],
          ["Leaving out brackets around a polyatomic ion.", "Adding atomic masses without multiplying by the number of atoms.", "Mixing up the mass of 1 mole with the mass of 1 molecule."],
          [("What is the difference between a molecule and a formula unit?", "A molecule is a group of atoms bonded together (H₂O); ionic compounds such as NaCl are made of ions, so we use a formula unit."),
           ("What is the mole?", "The amount of substance that contains 6.022 × 10²³ particles (atoms, molecules or ions).")],
          lambda: [("Symbols and laws of combination", [(sym, 12), (c_law, 8)]), ("Writing chemical formulae", [(c_formula, 20)]), ("Molecular and formula unit mass", [(c_mass, 20)]),
                   ("The mole concept", [(c_mole, 20)]), ("Mixed problems", [(b["atom"], 14), (c_law, 6)])]),
        U(4, "structure-of-the-atom", 4, MA,
          "Structure of atom: Sub-atomic particles: Electrons, protons and neutrons, Models of atom; Valency, Atomic Number and Mass Number, Isotopes and Isobars.",
          "Structure of the Atom", "structure of the atom",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 4: electrons, protons and neutrons, the Thomson, Rutherford and Bohr models, electronic configuration, valency, isotopes and isobars. 100 questions with answers.",
          "Atomic number = protons; mass number = protons + neutrons.", "Shells fill as 2, 8, 8 …",
          "<p>An atom has a small, dense, positive nucleus of protons and neutrons, with electrons in shells (K, L, M, N) around it. The atomic number Z is the number of protons; the mass number A is protons plus neutrons, so neutrons = A − Z.</p>"
          "<p>Shells hold at most 2n² electrons, and the outermost shell holds at most 8. Valency is the number of electrons an atom loses or gains to get a full outer shell. Isotopes have the same Z but different A; isobars have the same A but different Z.</p>",
          [("Neutrons in ²³₁₁Na?", ["23 − 11"], "12"), ("Configuration of sulphur (Z = 16)?", ["2 + 8 + 6"], "2, 8, 6; valency 2")],
          ["Taking the mass number as the number of neutrons.", "Putting more than 8 electrons in the outer shell of calcium (2, 8, 8, 2, not 2, 8, 10).", "Mixing up isotopes and isobars."],
          [("How is valency worked out from the configuration?", "If the outer shell has 1–4 electrons, valency equals that number; if it has 5–7, valency is 8 minus that number."),
           ("Why do isotopes have the same chemical properties?", "They have the same number of electrons arranged in the same way.")],
          lambda: [("Particles and models of the atom", [(mod, 6), (b["str"], 14)]), ("Atomic number and mass number", [(K(c_atom, "n", "p", "e"), 20)]),
                   ("Electronic configuration", [(K(c_atom, "cfg", "z"), 20)]), ("Valency", [(K(c_atom, "val"), 14), (b["str"], 6)]), ("Isotopes and average atomic mass", [(c_avg, 16), (K(c_atom, "n"), 4)])]),
    ]
