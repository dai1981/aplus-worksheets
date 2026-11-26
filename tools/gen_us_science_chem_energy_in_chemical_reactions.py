# -*- coding: utf-8 -*-
"""
US High School Chemistry: Energy in Chemical Reactions (HS-PS1-4)
  python tools/gen_us_science_chem_energy_in_chemical_reactions.py
Develop a model to illustrate that the release or absorption of energy from a chemical reaction system depends upon the
changes in total bond energy.
Exothermic and endothermic reactions, the sign of ΔH, bond energies (breaking absorbs, forming releases),
ΔH = bonds broken − bonds formed, and energy diagrams with activation energy.
Wrong answers come from real mistakes: "breaking bonds releases energy", "an exothermic reaction feels cold",
"ΔH = bonds formed − bonds broken", "the peak is ΔH".
"""
from sci_common import Unit, item, bank, lesson, make, table, svg_wrap, People
from sci_chem import sub, eq_html, split_eq

U = Unit(90209)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


BE = {"H–H": 436, "O=O": 498, "O–H": 463, "C–H": 413, "C=O": 799, "Cl–Cl": 242, "H–Cl": 431, "N≡N": 945, "N–H": 391, "Br–Br": 193, "H–Br": 366,
      "F–F": 158, "H–F": 567, "I–I": 151, "H–I": 299}
# equation, bonds in reactants, bonds in products
RX = [("H2 + Cl2 -> 2HCl", {"H–H": 1, "Cl–Cl": 1}, {"H–Cl": 2}), ("H2 + Br2 -> 2HBr", {"H–H": 1, "Br–Br": 1}, {"H–Br": 2}),
      ("H2 + F2 -> 2HF", {"H–H": 1, "F–F": 1}, {"H–F": 2}), ("H2 + I2 -> 2HI", {"H–H": 1, "I–I": 1}, {"H–I": 2}),
      ("2H2 + O2 -> 2H2O", {"H–H": 2, "O=O": 1}, {"O–H": 4}), ("N2 + 3H2 -> 2NH3", {"N≡N": 1, "H–H": 3}, {"N–H": 6}),
      ("CH4 + 2O2 -> CO2 + 2H2O", {"C–H": 4, "O=O": 2}, {"C=O": 2, "O–H": 4})]
RX += [(" -> ".join(reversed(e.split(" -> "))), b, a) for e, a, b in RX]


def tot(b):
    return sum(BE[k] * v for k, v in b.items())


def blist(b):
    return " + ".join("%d × %s (%d)" % (v, k, BE[k]) if v > 1 else "%s (%d)" % (k, BE[k]) for k, v in b.items())


def sgn(x):
    return ("+%d" % x) if x > 0 else ("−%d" % -x)


def g_bond():
    e, a, b = R.choice(RX)
    k = R.choice(["dh", "dh", "break", "form", "sign"])
    if not once(("bd", e, k)):
        return None
    l, r = split_eq(e)
    br, fo = tot(a), tot(b)
    dh = br - fo
    q = "%s. Bond energies (kJ/mol): %s." % (eq_html(l, r), ", ".join("%s = %d" % (x, BE[x]) for x in list(a) + [y for y in b if y not in a]))
    if k == "break":
        return item(q + " How much energy is needed to break the bonds in the reactants?", "%d kJ" % br, ["%d kJ" % fo, "%d kJ" % abs(dh), "%d kJ" % (br + fo)],
                    "%s = %d kJ." % (blist(a), br))
    if k == "form":
        return item(q + " How much energy is released when the product bonds form?", "%d kJ" % fo, ["%d kJ" % br, "%d kJ" % abs(dh), "%d kJ" % (br + fo)],
                    "%s = %d kJ." % (blist(b), fo))
    if k == "sign":
        t = "exothermic" if dh < 0 else "endothermic"
        return item(q + " Is the reaction exothermic or endothermic?", t, ["exothermic" if dh > 0 else "endothermic", "neither; no energy changes", "both at once"],
                    "Broken %d kJ − formed %d kJ = %s kJ." % (br, fo, sgn(dh)))
    return item(q + " What is ΔH?", "%s kJ" % sgn(dh), ["%s kJ" % sgn(-dh), "%d kJ" % (br + fo), "%s kJ" % sgn(dh * 2)],
                "ΔH = broken − formed = %d − %d = %s kJ." % (br, fo, sgn(dh)))


SCEN = [("A hand warmer gets hot when opened.", "exo"), ("A cold pack gets cold when squeezed.", "endo"), ("Wood burns in a campfire.", "exo"),
        ("Plants use light energy to make glucose in photosynthesis.", "endo"), ("Ammonium nitrate dissolves and the water gets colder.", "endo"),
        ("Cellular respiration releases energy for the body.", "exo"), ("Baking soda is heated to make a cake rise.", "endo"), ("Natural gas burns on a stove.", "exo"),
        ("Water is split into hydrogen and oxygen using electricity.", "endo"), ("Iron rusts slowly and releases a little heat.", "exo"),
        ("A thermite reaction melts iron.", "exo"), ("Limestone (CaCO₃) must be heated strongly to make lime.", "endo"),
        ("Citric acid and baking soda react and the cup feels cold.", "endo"), ("A match head flares when struck.", "exo")]


def g_exo():
    s, t = R.choice(SCEN)
    k = R.random() < 0.6
    if not once(("sc", s, k)):
        return None
    if k:
        a = "exothermic" if t == "exo" else "endothermic"
        return item("%s Is this exothermic or endothermic?" % s, a, ["endothermic" if t == "exo" else "exothermic", "neither", "a physical change only"],
                    "Exothermic releases energy (surroundings warm up); endothermic absorbs energy." )
    a = "negative" if t == "exo" else "positive"
    return item("%s What is the sign of ΔH for this change?" % s, a, ["positive" if t == "exo" else "negative", "zero", "It has no ΔH."],
                "Energy released: ΔH &lt; 0. Energy absorbed: ΔH &gt; 0.")


def diagram(r, p, peak):
    W, H = 320, 220
    def y(v):
        return 190 - v * 1.6
    pr, pp, pk = y(r), y(p), y(peak)
    s = "<path d='M30,%d L95,%d C140,%d 150,%d 165,%d C180,%d 190,%d 235,%d L300,%d' fill='none' stroke='#2b6cb0' stroke-width='3'/>" % (
        pr, pr, pr, pk, pk, pk, pp, pp, pp)
    s += "<line x1='22' y1='200' x2='22' y2='12' stroke='#333' stroke-width='2'/><line x1='22' y1='200' x2='310' y2='200' stroke='#333' stroke-width='2'/>"
    s += "<text x='14' y='110' font-size='13' transform='rotate(-90 14 110)' text-anchor='middle'>Energy (kJ)</text>"
    s += "<text x='166' y='216' font-size='13' text-anchor='middle'>Reaction progress</text>"
    s += "<text x='62' y='%d' font-size='13' text-anchor='middle'>Reactants %d</text>" % (pr - 7, r)
    s += "<text x='268' y='%d' font-size='13' text-anchor='middle'>Products %d</text>" % (pp - 7, p)
    s += "<text x='165' y='%d' font-size='13' text-anchor='middle'>Peak %d</text>" % (pk - 7, peak)
    return "<svg viewBox='0 0 %d %d' role='img' aria-label='energy diagram'>%s</svg>" % (W, H, s)


def g_diag():
    r = R.randint(2, 10) * 10
    p = R.randint(1, 10) * 10
    if p == r:
        return None
    peak = max(r, p) + R.randint(2, 5) * 10
    if peak > 110:
        return None
    k = R.choice(["dh", "ea", "type", "eare"])
    if not once(("dg", r, p, peak, k)):
        return None
    pic = diagram(r, p, peak)
    dh, ea = p - r, peak - r
    if k == "dh":
        return item(pic + "Use the energy diagram. What is ΔH for the reaction?", "%s kJ" % sgn(dh), ["%s kJ" % sgn(-dh), "%d kJ" % ea, "%d kJ" % peak], "ΔH = products − reactants = %d − %d." % (p, r))
    if k == "ea":
        return item(pic + "Use the energy diagram. What is the activation energy of the forward reaction?", "%d kJ" % ea, ["%d kJ" % peak, "%d kJ" % abs(dh), "%d kJ" % (peak - p)],
                    "Ea = peak − reactants = %d − %d = %d kJ." % (peak, r, ea))
    if k == "eare":
        rv = peak - p
        w = ["%d kJ" % x for x in dict.fromkeys([ea, peak, abs(dh), rv + 10]) if x != rv][:3]
        return item(pic + "Use the energy diagram. What is the activation energy of the reverse reaction?", "%d kJ" % rv, w,
                    "Reverse Ea = peak − products = %d − %d = %d kJ." % (peak, p, rv))
    t = "exothermic" if dh < 0 else "endothermic"
    return item(pic + "Is the reaction in the diagram exothermic or endothermic?", t, ["exothermic" if dh > 0 else "endothermic", "neither", "It cannot be told from the diagram."],
                "Products are %s than reactants." % ("lower" if dh < 0 else "higher"))


B1 = bank([
    ("What happens to energy when chemical bonds break?", "Energy is absorbed.", ["Energy is released.", "Nothing happens.", "Mass is lost."], "Breaking needs energy."),
    ("What happens to energy when chemical bonds form?", "Energy is released.", ["Energy is absorbed.", "Nothing happens.", "Atoms are destroyed."], "Forming releases energy."),
    ("What is an exothermic reaction?", "a reaction that releases energy to the surroundings", ["a reaction that absorbs energy", "a reaction with no energy change", "a reaction that only happens in cold places"], "Surroundings warm."),
    ("What is an endothermic reaction?", "a reaction that absorbs energy from the surroundings", ["a reaction that releases heat", "a burning reaction", "a reaction that makes light"], "Surroundings cool."),
    ("In an exothermic reaction, how do the product bonds compare with the reactant bonds?", "The product bonds are stronger (more energy released forming them).", ["The product bonds are weaker.", "They are exactly equal.", "Products have no bonds."], "Net release."),
    ("What does ΔH stand for?", "the change in enthalpy (heat energy) of a reaction", ["the change in mass", "the change in hydrogen", "the speed of a reaction"], "Negative = exothermic."),
    ("What is activation energy?", "the energy needed to start a reaction", ["the energy released", "the energy of the products", "the total bond energy"], "The hump on the diagram."),
    ("A reaction has ΔH = −250 kJ. What does the negative sign mean?", "250 kJ of energy is released.", ["250 kJ is absorbed.", "No energy changes.", "The reaction cannot happen."], "Exothermic."),
])
B5 = bank([
    ("Why does a match need to be struck before it burns, even though burning is exothermic?", "Striking supplies the activation energy.", ["Burning is endothermic.", "Matches have no bonds.", "Striking removes oxygen."], "Energy barrier."),
    ("An engineer designs a cold pack. Which kind of reaction should she use?", "an endothermic reaction", ["an exothermic reaction", "a combustion reaction", "a reaction with ΔH &lt; 0"], "Absorbs heat."),
    ("A student says burning fuel releases energy stored in the fuel's bonds. What is a better model?", "More energy is released forming CO₂ and H₂O bonds than is used to break the fuel and O₂ bonds.",
     ["Energy pops out when bonds break.", "Fuel has no bonds.", "Energy is created."], "Net bond energy change."),
    ("If a reaction is exothermic in one direction, what is the reverse reaction?", "endothermic, with the same amount of energy", ["also exothermic", "neither", "twice as exothermic"], "Reverse sign."),
    ("Which evidence would show a reaction is endothermic?", "The thermometer in the solution drops.", ["The beaker gets hot.", "Light is given off.", "A flame appears."], "Energy is absorbed from the water."),
])


def body():
    think = ("<p><b>ΔH = energy to break bonds − energy released forming bonds.</b></p>"
             "<ul><li>Breaking bonds absorbs energy; forming bonds releases energy.</li>"
             "<li>More released than absorbed: exothermic, ΔH &lt; 0 (surroundings get warmer). More absorbed: endothermic, ΔH &gt; 0.</li>"
             "<li>On an energy diagram, ΔH = products − reactants; activation energy = peak − reactants.</li></ul>")
    ex = [("H<sub>2</sub> + Cl<sub>2</sub> → 2HCl: broken 678 kJ, formed 862 kJ. ΔH?", ["678 − 862"], "−184 kJ (exothermic)"),
          ("Reactants 60 kJ, products 20 kJ, peak 90 kJ. Ea?", ["90 − 60"], "30 kJ")]
    mist = ["Thinking breaking bonds releases energy.", "Thinking an exothermic reaction feels cold.", "Reading the peak height as ΔH."]
    return lesson(think, ex, mist)


def commas(t):
    import re
    parts = re.split(r"(<[^>]*>)", t)
    return "".join(x if x.startswith("<") else re.sub(r"(?<![\d.,#])(\d{4,})(?![\d.])", lambda m: "{:,}".format(int(m.group(1))), x) for x in parts)


def main():
    sets = U.sets([
        ("Exothermic and endothermic", B1 + [(g_exo, 12)]),
        ("Everyday reactions", [(g_exo, 10), (g_diag, 10)]),
        ("Energy diagrams", [(g_diag, 14), (g_bond, 6)]),
        ("Bond energies", [(g_bond, 16), (g_diag, 4)]),
        ("Modeling energy changes", B5 + [(g_bond, 8), (g_diag, 7)]),
    ])
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = commas(it["q"]), commas(it["e"]), [commas(c) for c in it["c"]]
    make("chemistry", "energy-in-chemical-reactions", 9, "HS-PS1-4",
         "Develop a model to illustrate that the release or absorption of energy from a chemical reaction system depends upon the changes in total bond energy.",
         "Energy in Chemical Reactions",
         "Reaction Energy Worksheets: Exothermic, Endothermic and Bond Energies (High School Chemistry)",
         "Reaction Energy",
         "Free high school chemistry worksheets on energy in chemical reactions (NGSS HS-PS1-4): exothermic and endothermic reactions, bond energies, ΔH and energy diagrams. 100 questions with answers.",
         "Breaking absorbs; forming releases.",
         "ΔH is the energy to break bonds minus the energy released forming new ones.",
         body(),
         [("How do you calculate ΔH from bond energies?", "Add the energies of all bonds broken in the reactants, then subtract the energies of all bonds formed in the products."),
          ("How can you tell if a reaction is exothermic?", "It releases energy, so the surroundings get warmer and ΔH is negative. On a diagram, the products are lower than the reactants."),
          ("What is activation energy?", "The energy needed to start a reaction: the peak of the energy diagram minus the energy of the reactants.")],
         sets)


if __name__ == "__main__":
    main()
