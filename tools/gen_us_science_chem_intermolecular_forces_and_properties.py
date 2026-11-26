# -*- coding: utf-8 -*-
"""
US High School Chemistry: Intermolecular Forces and Properties (HS-PS1-3)
  python tools/gen_us_science_chem_intermolecular_forces_and_properties.py
Plan and conduct an investigation to gather evidence to compare the structure of substances at the bulk scale to infer
the strength of electrical forces between particles.
London dispersion forces, dipole-dipole forces and hydrogen bonds; boiling and melting points; states at room
temperature; evaporation and surface tension; ionic, molecular, metallic and network solids.
Every boiling-point comparison uses real data (SUB) and only pairs where the textbook reason is the true one.
Wrong answers come from real mistakes: "boiling breaks covalent bonds", "hydrogen bonds are bonds inside a molecule",
"bigger molecules always have weaker forces".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import sub

U = Unit(90204)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# name, formula, molar mass, boiling point (°C), melting point (°C), strongest force between particles
SUB = [("helium", "He", 4, -269, -272, "L"), ("neon", "Ne", 20, -246, -249, "L"), ("argon", "Ar", 40, -186, -189, "L"), ("krypton", "Kr", 84, -153, -157, "L"),
       ("xenon", "Xe", 131, -108, -112, "L"), ("fluorine", "F2", 38, -188, -220, "L"), ("chlorine", "Cl2", 71, -34, -101, "L"), ("bromine", "Br2", 160, 59, -7, "L"),
       ("iodine", "I2", 254, 184, 114, "L"), ("nitrogen", "N2", 28, -196, -210, "L"), ("oxygen", "O2", 32, -183, -218, "L"),
       ("methane", "CH4", 16, -162, -182, "L"), ("ethane", "C2H6", 30, -89, -183, "L"), ("propane", "C3H8", 44, -42, -188, "L"), ("butane", "C4H10", 58, -1, -138, "L"),
       ("pentane", "C5H12", 72, 36, -130, "L"), ("hexane", "C6H14", 86, 69, -95, "L"), ("octane", "C8H18", 114, 126, -57, "L"),
       ("water", "H2O", 18, 100, 0, "H"), ("ammonia", "NH3", 17, -33, -78, "H"), ("hydrogen fluoride", "HF", 20, 20, -83, "H"), ("methanol", "CH3OH", 32, 65, -98, "H"),
       ("ethanol", "C2H5OH", 46, 78, -114, "H"), ("hydrogen sulfide", "H2S", 34, -60, -86, "D"), ("hydrogen chloride", "HCl", 36, -85, -114, "D"),
       ("phosphine", "PH3", 34, -88, -133, "D"), ("chloromethane", "CH3Cl", 50, -24, -98, "D"), ("acetone", "C3H6O", 58, 56, -95, "D"),
       ("sodium chloride", "NaCl", 58, 1413, 801, "I"), ("potassium chloride", "KCl", 75, 1420, 770, "I"), ("magnesium oxide", "MgO", 40, 3600, 2852, "I")]
FN = {"L": "London dispersion forces only", "D": "dipole-dipole forces", "H": "hydrogen bonds", "I": "ionic attractions (it is an ionic compound)"}
RANK = {"L": 0, "D": 1, "H": 2, "I": 3}


def nm(s):
    return "%s (%s)" % (s[0], sub(s[1]))


def g_imf():
    s = R.choice(SUB)
    if not once(("im", s[0])):
        return None
    why = {"L": "Nonpolar particles only have London dispersion forces.", "D": "Polar molecules without H bonded to N, O or F have dipole-dipole forces.",
           "H": "H bonded to N, O or F gives hydrogen bonding.", "I": "Ions attract each other strongly."}[s[5]]
    return item("What is the strongest attraction between particles of %s?" % nm(s), FN[s[5]], [FN[x] for x in "LDHI" if x != s[5]], why)


def fair(a, b):
    """pair where the textbook reason is right"""
    if a[5] == b[5] == "L":
        return abs(a[3] - b[3]) > 15
    if a[5] == b[5]:
        return False
    hi, lo = (a, b) if RANK[a[5]] > RANK[b[5]] else (b, a)
    return hi[3] > lo[3] + 15 and max(lo[2], hi[2]) <= 2 * min(lo[2], hi[2]) and "I" not in (lo[5],)


def g_bp():
    a, b = R.sample(SUB, 2)
    if not fair(a, b) or not once(("bp", tuple(sorted((a[0], b[0]))))):
        return None
    hi, lo = (a, b) if a[3] > b[3] else (b, a)
    first, second = sorted([a, b])
    if hi[5] == lo[5]:
        why = "Both have only London forces; %s is larger (%d g/mol vs %d g/mol), so its forces are stronger." % (hi[0], hi[2], lo[2])
    else:
        why = "%s has %s, which are stronger than the %s in %s." % (hi[0].capitalize(), FN[hi[5]].split(" (")[0], FN[lo[5]].replace(" only", ""), lo[0])
    return item("Which has the higher boiling point, %s or %s?" % (nm(first), nm(second)), hi[0], [lo[0], "They boil at the same temperature.", "It depends only on the container."], why)


def g_order():
    fam = R.choice([["helium", "neon", "argon", "krypton", "xenon"], ["fluorine", "chlorine", "bromine", "iodine"], ["methane", "ethane", "propane", "butane", "pentane", "hexane", "octane"]])
    names = sorted(R.sample(fam, 3), key=fam.index)
    if not once(("or", tuple(names))):
        return None
    by = {s[0]: s for s in SUB}
    good = ", ".join(names)
    w = [", ".join(reversed(names)), ", ".join([names[1], names[0], names[2]]), ", ".join([names[0], names[2], names[1]])]
    return item("List from lowest to highest boiling point: %s." % ", ".join(nm(by[x]) for x in sorted(names)), good, w,
                "All have only London forces; more electrons (larger molar mass) means stronger forces.")


def state(s, t):
    return "solid" if t < s[4] else "liquid" if t < s[3] else "gas"


def g_state():
    who = P.next()[0]
    ss = R.sample([x for x in SUB if x[5] != "I"], 4)
    t = R.choice([25, -50, 0, 50])
    k = R.choice(["liquid", "gas", "one"])
    st = [state(s, t) for s in ss]
    if any(t in (s[3], s[4]) for s in ss):
        return None
    if not once(("st", tuple(x[0] for x in ss), t, k)):
        return None
    tab = table(["Substance", "Melting point (°C)", "Boiling point (°C)"], [[nm(s), str(s[4]).replace("-", "−"), str(s[3]).replace("-", "−")] for s in ss])
    tt = ("%d" % t).replace("-", "−")
    if k in ("liquid", "gas"):
        if st.count(k) != 1:
            return None
        i = st.index(k)
        return item(tab + "%s keeps all four at %s °C. Which one is a %s?" % (who, tt, k), ss[i][0], [x[0] for j, x in enumerate(ss) if j != i],
                    "A %s is between its melting and boiling points." % k if k == "liquid" else "A gas is above its boiling point.")
    s = R.choice(ss)
    a = state(s, t)
    return item(tab + "What state is %s at %s °C in %s's table?" % (s[0], tt, who), a, [x for x in ["solid", "liquid", "gas", "plasma"] if x != a],
                "Compare %s °C with the melting point (%s) and boiling point (%s)." % (tt, str(s[4]).replace("-", "−"), str(s[3]).replace("-", "−")))


SOLIDS = [("hard, brittle, high melting point, conducts only when melted or dissolved", "ionic solid", "table salt"),
          ("soft, low melting point, does not conduct", "molecular solid", "wax or sugar"),
          ("shiny, bends without breaking, conducts as a solid", "metallic solid", "copper"),
          ("very hard, very high melting point, does not conduct", "network covalent solid", "diamond or quartz"),
          ("dissolves in water to make a solution that conducts", "ionic solid", "potassium chloride"),
          ("melts below 100 °C and smells strongly", "molecular solid", "menthol"),
          ("conducts heat well and can be pulled into wires", "metallic solid", "aluminum"),
          ("does not melt until over 1,700 °C and is made of Si and O atoms all bonded together", "network covalent solid", "quartz (SiO₂)")]


def g_solid():
    p, t, ex = R.choice(SOLIDS)
    k = R.random() < 0.6
    if not once(("so", p, k)):
        return None
    types = ["ionic solid", "molecular solid", "metallic solid", "network covalent solid"]
    if k:
        return item("A solid has these properties: %s. What type of solid is it most likely?" % p, t, [x for x in types if x != t], "Example: %s." % ex)
    return item("Which properties best describe %s?" % (("an " if t[0] in "aeiou" else "a ") + t), p, R.sample(sorted({x[0] for x in SOLIDS if x[1] != t}), 3), "Example: %s." % ex)


B1 = bank([
    ("What are intermolecular forces?", "attractions between separate molecules", ["bonds inside a molecule", "forces inside the nucleus", "the charges on ions only"], "Between, not within."),
    ("When water boils, what is overcome?", "the attractions between water molecules", ["the covalent bonds inside each molecule", "the nucleus of each atom", "the electrons in hydrogen"], "Molecules stay H₂O."),
    ("Which force is found between all molecules?", "London dispersion forces", ["hydrogen bonds", "dipole-dipole forces", "ionic bonds"], "Temporary dipoles."),
    ("A hydrogen bond forms when H is bonded to which atoms?", "nitrogen, oxygen or fluorine", ["carbon or sulfur", "any metal", "helium or neon"], "Very electronegative atoms."),
    ("Stronger forces between particles usually mean what?", "higher melting and boiling points", ["lower boiling points", "more evaporation", "smaller molar mass"], "More energy to separate."),
    ("Why do larger nonpolar molecules have higher boiling points?", "More electrons give stronger London forces.", ["They are polar.", "They have hydrogen bonds.", "They are lighter."], "Bigger electron clouds."),
    ("What is a polar molecule?", "a molecule with a positive end and a negative end", ["a molecule with no charge anywhere", "an ion", "a metal"], "Uneven sharing and shape."),
    ("Which liquid evaporates faster at room temperature?", "the one with weaker forces between molecules", ["the one with stronger forces", "the heavier one always", "the one with hydrogen bonds"], "Volatile liquids have weak forces."),
])
B5 = bank([
    ("Water beads up on a waxed car. Which explains water's high surface tension?", "strong hydrogen bonds pull surface molecules together", ["water is nonpolar", "water has no forces", "wax is ionic"], "Cohesion."),
    ("A student puts equal drops of water and rubbing alcohol on a table. The alcohol disappears first. What can she infer?", "Forces between alcohol molecules are weaker.", ["Alcohol has stronger forces.", "Water is a gas.", "Both have the same forces."], "Evaporation rate."),
    ("Why is ice less dense than liquid water?", "Hydrogen bonds hold molecules in an open pattern.", ["Ice has fewer molecules.", "Ice is a gas.", "Water is ionic."], "So ice floats."),
    ("Which test would best compare the strength of forces in two liquids?", "measure their boiling points with the same setup", ["compare their colors", "weigh the containers", "smell them"], "Bulk properties reveal forces."),
    ("Why does salt (NaCl) melt at 801 °C but water ice melts at 0 °C?", "Ionic attractions in salt are much stronger than hydrogen bonds in ice.", ["Salt is a molecule.", "Ice has ionic bonds.", "Salt is lighter."], "Strength of attraction."),
])


def body():
    think = ("<p><b>Stronger attractions between particles mean higher boiling points.</b></p>"
             "<ul><li>London dispersion forces (all molecules) &lt; dipole-dipole forces (polar molecules) &lt; hydrogen bonds (H on N, O or F).</li>"
             "<li>Among similar molecules, more electrons (larger size) means stronger London forces.</li>"
             "<li>Boiling separates molecules; it does not break the covalent bonds inside them.</li></ul>")
    ex = [("Higher boiling point: H<sub>2</sub>O or H<sub>2</sub>S?", ["Water has hydrogen bonds"], "water"),
          ("Higher boiling point: Cl<sub>2</sub> or Br<sub>2</sub>?", ["Both London only", "Br<sub>2</sub> is larger"], "bromine")]
    mist = ["Thinking boiling breaks the bonds inside molecules.", "Calling the O–H bond inside water a hydrogen bond.", "Thinking larger molecules have weaker forces."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Types of attractions", B1 + [(g_imf, 12)]),
        ("Which force?", [(g_imf, 10), (g_solid, 6), (g_order, 4)]),
        ("Boiling points", [(g_bp, 14), (g_order, 6)]),
        ("States and data", [(g_state, 14), (g_solid, 6)]),
        ("Evidence from properties", B5 + [(g_bp, 6), (g_state, 6), (g_order, 3)]),
    ])
    make("chemistry", "intermolecular-forces-and-properties", 4, "HS-PS1-3",
         "Plan and conduct an investigation to gather evidence to compare the structure of substances at the bulk scale to infer the strength of electrical forces between particles.",
         "Intermolecular Forces and Properties",
         "Intermolecular Forces Worksheets: Hydrogen Bonds and Boiling Points (High School Chemistry)",
         "Intermolecular Forces",
         "Free high school chemistry worksheets on intermolecular forces (NGSS HS-PS1-3): London forces, dipole-dipole forces, hydrogen bonds, boiling points, states of matter and types of solids. 100 questions with answers.",
         "Stronger attractions, higher boiling points.",
         "Bulk properties such as boiling point show how strongly particles attract.",
         body(),
         [("What are the three main intermolecular forces?", "London dispersion forces (in all molecules), dipole-dipole forces (in polar molecules) and hydrogen bonds (H bonded to N, O or F)."),
          ("Why does water have a high boiling point for its size?", "Water molecules form hydrogen bonds, which are stronger than the forces between similar small molecules such as H₂S."),
          ("How can you compare forces in a lab?", "Measure bulk properties such as boiling point, melting point, evaporation rate or surface tension.")],
         sets)


if __name__ == "__main__":
    main()
