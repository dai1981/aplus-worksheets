# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 9: Chemical Energetics
  python tools/gen_sg_science_s4_chemical_energetics.py
Exothermic and endothermic reactions, enthalpy change ΔH (negative for exothermic, positive for endothermic), energy profile
diagrams with activation energy, bond breaking (endothermic) and bond making (exothermic), and calculating ΔH from bond energies.
US and UK energetics makers are reused (Singapore names); energy profiles are drawn here.
Wrong answers come from real mistakes: "bond breaking releases energy", "ΔH is positive for an exothermic reaction",
"activation energy is the energy given out", "the products of an exothermic reaction are higher in energy".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex, fig
from sci_common import svg_wrap, text, line, BLUE, RED, INK, GREEN

LV, SUBJ, SORT = 4, "Chemistry", 11
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

us_bond = src("gen_us_science_chem_energy_in_chemical_reactions", "g_bond", rep=[(r"What is the energy change\?", "What is the enthalpy change, ΔH?")])
us_exo = src("gen_us_science_chem_energy_in_chemical_reactions", "g_exo")
uk_temp = src("gen_uk_science_y9_exothermic_and_endothermic_reactions", "g_temp")

EX = [("burning methane in a gas stove", "exothermic"), ("neutralising hydrochloric acid with sodium hydroxide", "exothermic"), ("respiration in cells", "exothermic"),
      ("magnesium reacting with dilute acid", "exothermic"), ("rusting of iron", "exothermic"), ("adding water to calcium oxide (quicklime)", "exothermic"),
      ("photosynthesis", "endothermic"), ("thermal decomposition of calcium carbonate", "endothermic"), ("dissolving ammonium nitrate in water", "endothermic"),
      ("electrolysis of water", "endothermic"), ("melting ice", "endothermic"), ("condensing steam", "exothermic"), ("sherbet (citric acid and sodium hydrogencarbonate) dissolving on the tongue", "endothermic"),
      ("a hand warmer pack (iron powder oxidising)", "exothermic"), ("a cold pack for sports injuries", "endothermic")]


def g_ex():
    q, a = R.choice(EX)
    return tq("Is %s exothermic or endothermic?" % q, a, ["endothermic" if a == "exothermic" else "exothermic", "neither: no energy change", "both at the same time"],
              "Exothermic: energy given out to the surroundings (ΔH negative). Endothermic: energy taken in (ΔH positive).")


def g_temp():
    t0 = R.choice([24.0, 25.0, 26.5, 28.0, 29.5, 30.0])
    d = R.choice([-8.5, -6.0, -4.5, -3.0, 3.5, 5.0, 7.5, 10.0, 12.5])
    t1 = t0 + d
    k = R.choice(["type", "sign"])
    if k == "type":
        return tq("The temperature of a reaction mixture changes from %.1f °C to %.1f °C. What type of reaction is it?" % (t0, t1), "exothermic" if d > 0 else "endothermic",
                  ["endothermic" if d > 0 else "exothermic", "neither: temperature changes do not show energy changes", "a physical change only"],
                  "A temperature rise means energy is given out to the surroundings (exothermic); a fall means energy is taken in (endothermic).")
    return tq("The temperature of a reaction mixture changes from %.1f °C to %.1f °C. What is the sign of ΔH?" % (t0, t1), "negative" if d > 0 else "positive",
              ["positive" if d > 0 else "negative", "zero", "it cannot be known"], "Exothermic reactions have a negative ΔH; endothermic reactions have a positive ΔH.")


def profile(h_r, h_p, peak):
    W, H = 420, 250
    L, B = 60, 210
    Y = lambda v: B - v * 1.6
    s = [line(L, 20, L, B, w=2), line(L, B, W - 20, B, w=2), text(W / 2 + 10, H - 12, "progress of reaction", fs=12, weight=400),
         "<text x='16' y='%d' font-size='12' text-anchor='middle' transform='rotate(-90 16 %d)'>energy</text>" % ((20 + B) // 2, (20 + B) // 2)]
    xr1, xr2, xm, xp1, xp2 = L + 10, L + 90, L + 170, L + 250, L + 330
    s.append("<path d='M%d %.1f L%d %.1f C%d %.1f %d %.1f %d %.1f C%d %.1f %d %.1f %d %.1f L%d %.1f' fill='none' stroke='%s' stroke-width='3'/>" % (
        xr1, Y(h_r), xr2, Y(h_r), xr2 + 40, Y(h_r), xm - 30, Y(peak), xm, Y(peak), xm + 30, Y(peak), xp1 - 40, Y(h_p), xp1, Y(h_p), xp2, Y(h_p), BLUE))
    s.append(text(xr1 + 26, Y(h_r) - 8, "reactants", fs=12, weight=400) + text(xp1 + 40, Y(h_p) - 8, "products", fs=12, weight=400))
    s.append(line(xr2 + 2, Y(h_r), xr2 + 2, Y(peak), col=RED, w=1.5) + line(xr2 - 6, Y(peak), xm, Y(peak), col="#999", w=1, extra=" stroke-dasharray='4 3'") + text(xr2 - 4, (Y(h_r) + Y(peak)) / 2, "A", fs=14, col=RED, anchor="end"))
    s.append(line(xp1 + 70, Y(h_r), xp1 + 70, Y(h_p), col=GREEN, w=1.5) + line(xp1 - 10, Y(h_r), xp1 + 80, Y(h_r), col="#999", w=1, extra=" stroke-dasharray='4 3'") +
             text(xp1 + 76, (Y(h_r) + Y(h_p)) / 2 + 4, "B", fs=14, col=GREEN, anchor="start"))
    return svg_wrap(W, H, "".join(s), "energy profile diagram").replace("<svg ", "<svg data-pf='lg' ", 1)


def g_prof():
    exo = R.random() < 0.5
    h_r, h_p = (70, 25) if exo else (25, 70)
    peak = R.choice([100, 105, 110])
    svg = fig(profile(h_r, h_p, peak))
    k = R.choice(["type", "A", "B", "cat", "sign", "num", "num", "num"])
    q = svg + "The energy profile diagram shows a reaction. "
    if k == "num":
        er = R.choice([100, 150, 200, 250, 300])
        d = R.choice([40, 60, 80, 90, 120, 150])
        ep = er - d if exo else er + d
        pk = max(er, ep) + R.choice([50, 80, 100, 120, 150])
        if R.random() < 0.5:
            return nq(q + "The reactants have %d kJ/mol, the products %d kJ/mol and the peak %d kJ/mol. What is the activation energy?" % (er, ep, pk), pk - er,
                      [pk - ep, abs(ep - er), pk], " kJ/mol", "Ea = peak − reactants = %d − %d = %d kJ/mol." % (pk, er, pk - er))
        a = ("−%d" % d if exo else "+%d" % d) + " kJ/mol"
        return tq(q + "The reactants have %d kJ/mol, the products %d kJ/mol and the peak %d kJ/mol. What is ΔH?" % (er, ep, pk), a,
                  [("+%d" % d if exo else "−%d" % d) + " kJ/mol", "+%d kJ/mol" % (pk - er), "−%d kJ/mol" % (pk - ep)], "ΔH = products − reactants = %d − %d." % (ep, er))
    if k == "type":
        return tq(q + "Is the reaction exothermic or endothermic?", "exothermic" if exo else "endothermic", ["endothermic" if exo else "exothermic", "neither", "it depends on the catalyst"],
                  "The products are %s in energy than the reactants." % ("lower" if exo else "higher"))
    if k == "A":
        return tq(q + "What does the arrow labelled A show?", "the activation energy", ["the enthalpy change, ΔH", "the energy of the products", "the energy given out by a catalyst"],
                  "A goes from the reactants up to the peak: the minimum energy needed for a reaction.")
    if k == "B":
        return tq(q + "What does the arrow labelled B show?", "the enthalpy change of the reaction, ΔH", ["the activation energy", "the energy of the catalyst", "the bond energy of the reactants"],
                  "B is the difference between the energies of the reactants and the products.")
    if k == "sign":
        return tq(q + "What is the sign of ΔH?", "negative" if exo else "positive", ["positive" if exo else "negative", "zero", "it has no sign"], "Exothermic ΔH < 0; endothermic ΔH > 0.")
    return tq(q + "How does adding a catalyst change the diagram?", "The peak is lower (smaller activation energy), but ΔH stays the same.",
              ["ΔH becomes larger.", "The products become lower in energy.", "The peak becomes higher."], "A catalyst gives an alternative pathway with a lower activation energy.")


BE = {"H–H": 436, "Cl–Cl": 242, "H–Cl": 431, "O=O": 498, "O–H": 463, "C–H": 413, "C=O": 799, "N≡N": 945, "N–H": 391, "Br–Br": 193, "H–Br": 366, "C–C": 348, "C=C": 612, "C–Cl": 338}
RXB = [("H₂ + Cl₂ → 2HCl", {"H–H": 1, "Cl–Cl": 1}, {"H–Cl": 2}), ("H₂ + Br₂ → 2HBr", {"H–H": 1, "Br–Br": 1}, {"H–Br": 2}),
       ("2H₂ + O₂ → 2H₂O", {"H–H": 2, "O=O": 1}, {"O–H": 4}), ("CH₄ + 2O₂ → CO₂ + 2H₂O", {"C–H": 4, "O=O": 2}, {"C=O": 2, "O–H": 4}),
       ("N₂ + 3H₂ → 2NH₃", {"N≡N": 1, "H–H": 3}, {"N–H": 6}), ("C₂H₄ + H₂ → C₂H₆", {"C=C": 1, "C–H": 4, "H–H": 1}, {"C–C": 1, "C–H": 6}),
       ("CH₄ + Cl₂ → CH₃Cl + HCl", {"C–H": 4, "Cl–Cl": 1}, {"C–H": 3, "C–Cl": 1, "H–Cl": 1})]


def g_bond():
    eq, br, mk = R.choice(RXB)
    bi = sum(BE[b] * n for b, n in br.items())
    mo = sum(BE[b] * n for b, n in mk.items())
    dh = bi - mo
    used = sorted(set(br) | set(mk))
    data = ", ".join("%s = %d" % (b, BE[b]) for b in used)
    k = R.choice(["dh", "dh", "in", "out"])
    if k == "in":
        return nq("%s. Bond energies (kJ/mol): %s. How much energy is taken in to break the bonds in the reactants?" % (eq, data), bi, [mo, bi - mo, bi + mo], " kJ",
                  "Bonds broken: " + " + ".join("%d × %d" % (n, BE[b]) for b, n in br.items()) + " = %d kJ." % bi)
    if k == "out":
        return nq("%s. Bond energies (kJ/mol): %s. How much energy is given out when the bonds in the products form?" % (eq, data), mo, [bi, bi - mo, bi + mo], " kJ",
                  "Bonds made: " + " + ".join("%d × %d" % (n, BE[b]) for b, n in mk.items()) + " = %d kJ." % mo)
    a = ("+%d" % dh if dh > 0 else "−%d" % -dh) + " kJ/mol"
    wr = [("+%d" % -dh if -dh > 0 else "−%d" % dh) + " kJ/mol", "+%d kJ/mol" % (bi + mo), "−%d kJ/mol" % bi]
    return tq("%s. Bond energies (kJ/mol): %s. What is the enthalpy change, ΔH?" % (eq, data), a, wr,
              "ΔH = energy to break bonds − energy released making bonds = %d − %d = %s." % (bi, mo, a))


POOL1 = pool(R, [
    ("What is an exothermic reaction?", "a reaction that gives out energy to the surroundings, so the temperature rises", ["a reaction that takes in energy", "a reaction that needs a catalyst", "a reaction with no energy change"], "ΔH is negative."),
    ("What is an endothermic reaction?", "a reaction that takes in energy from the surroundings, so the temperature falls", ["a reaction that gives out heat", "a reaction that only happens in the cold", "a fast reaction"], "ΔH is positive."),
    ("Is bond breaking exothermic or endothermic?", "endothermic: energy is taken in", ["exothermic: energy is given out", "neither", "it depends on the bond"], "Energy is needed to pull atoms apart."),
    ("Is bond making exothermic or endothermic?", "exothermic: energy is given out", ["endothermic: energy is taken in", "neither", "only with a catalyst"], "Forming bonds releases energy."),
    ("Why is a reaction exothermic overall?", "More energy is released in making the new bonds than is taken in to break the old bonds.", ["No bonds are broken.", "Bond breaking releases energy.", "The reactants are cold."], "ΔH = bonds broken − bonds made."),
    ("What is activation energy?", "the minimum energy that colliding particles need to react", ["the energy given out by a reaction", "the energy stored in the products", "the energy of a catalyst"], "Shown as the hump on an energy profile."),
    ("What is the unit of enthalpy change in O-Level Chemistry?", "kJ/mol", ["kJ/g", "J/°C", "mol/dm³"], "Energy per mole of reaction."),
    ("Why does a match need to be struck before it burns, even though burning is exothermic?", "Striking supplies the activation energy.", ["Burning is endothermic.", "Striking adds oxygen.", "The match is too cold."], "Once started, the reaction keeps itself going."),
])
POOL5 = pool(R, [
    ("Why is a polystyrene cup used to measure the temperature change of a reaction?", "It is a good insulator, so less energy is lost to the surroundings.", ["It reacts with the chemicals.", "It is a good conductor.", "It makes the reaction faster."], "A lid also reduces losses."),
    ("Dissolving ammonium nitrate in water makes the beaker feel cold. What is the sign of ΔH?", "positive", ["negative", "zero", "it has no sign"], "Endothermic."),
    ("For the reaction CaCO₃ → CaO + CO₂, ΔH = +178 kJ/mol. What does this tell you?", "It is endothermic: 178 kJ are taken in per mole of CaCO₃ decomposed.", ["It is exothermic.", "It gives out 178 kJ.", "It needs no heating."], "Positive ΔH."),
    ("Hydrogen is burned as a fuel. Why is it a 'clean' fuel?", "The only product is water.", ["It produces carbon dioxide only.", "It takes in energy.", "It produces sulfur dioxide."], "2H₂ + O₂ → 2H₂O, ΔH negative."),
    ("Why is natural gas a good fuel?", "Its combustion is highly exothermic and it burns cleanly.", ["Its combustion is endothermic.", "It produces no carbon dioxide.", "It has a high activation energy that is never reached."], "Methane burns to CO₂ and H₂O."),
    ("In an energy profile for an endothermic reaction, where are the products?", "higher in energy than the reactants", ["lower than the reactants", "at the same level", "at the top of the hump"], "Energy has been taken in."),
    ("ΔH for a reaction is −92 kJ/mol. What is ΔH for the reverse reaction?", "+92 kJ/mol", ["−92 kJ/mol", "0 kJ/mol", "−184 kJ/mol"], "The reverse reaction has the opposite sign."),
    ("Which change to a reaction does a catalyst NOT affect?", "the enthalpy change, ΔH", ["the activation energy", "the rate of reaction", "the pathway of the reaction"], "Reactants and products have the same energies."),
])


def main():
    sets = U.sets([
        ("Exothermic and endothermic reactions", [POOL1, (g_ex, 8), (g_temp, 4)]),
        ("Temperature changes and ΔH", [(g_temp, 7), (us_exo, 5), (uk_temp, 4), (g_ex, 4)]),
        ("Energy profile diagrams", [(g_prof, 12), POOL1, (POOL5, 2)]),
        ("Bond energies", [(g_bond, 12), (us_bond, 6), POOL1]),
        ("Exam-style questions", [(POOL5, 8), (g_bond, 5), (g_prof, 4), (g_ex, 3)]),
    ])
    make_ol(LV, SUBJ, "chemical-energetics", SORT, "Chemical Energetics",
            "Describe the meaning of exothermic and endothermic reactions and represent them by energy profile diagrams; state that ΔH is negative for exothermic and positive "
            "for endothermic reactions; describe activation energy and show it on energy profile diagrams; describe bond breaking as endothermic and bond making as "
            "exothermic and explain the enthalpy change of a reaction in these terms; calculate enthalpy changes from bond energies (summary of the Singapore-Cambridge "
            "O-Level Chemistry 6092 syllabus).",
            "Chemical Energetics", "Chemical energetics",
            "Free Secondary 4 O-Level Chemistry worksheets on chemical energetics: exothermic and endothermic reactions, ΔH, energy profile diagrams, activation energy and "
            "bond energy calculations. 100 questions with answers.",
            "Exothermic: ΔH negative. Endothermic: ΔH positive.", "ΔH = energy to break bonds − energy from making bonds.",
            "<p><b>Reactions give out or take in energy.</b></p><ul>"
            "<li>Exothermic: energy given out, temperature rises, products lower in energy, ΔH negative. Endothermic: the opposite.</li>"
            "<li>Activation energy is the minimum energy colliding particles need to react; a catalyst lowers it but does not change ΔH.</li>"
            "<li>Breaking bonds takes in energy; making bonds gives out energy. ΔH = Σ(bonds broken) − Σ(bonds made).</li></ul>",
            [("H₂ + Cl₂ → 2HCl. H–H 436, Cl–Cl 242, H–Cl 431. ΔH?", ["broken: 436 + 242 = 678", "made: 2 × 431 = 862", "678 − 862"], "−184 kJ/mol"),
             ("Temperature falls from 25.0 °C to 19.5 °C. Type?", ["energy taken in"], "endothermic")],
            ["Saying bond breaking releases energy.", "Giving an exothermic reaction a positive ΔH.",
             "Calculating ΔH as bonds made − bonds broken (the sign comes out wrong).", "Thinking a catalyst changes ΔH."],
            [("How do you calculate ΔH from bond energies?", "Add up the energies of all the bonds broken in the reactants, add up the energies of all the bonds made in the products, then ΔH = bonds broken − bonds made."),
             ("How do you read an energy profile diagram?", "If the products are lower than the reactants the reaction is exothermic; if higher, endothermic. The hump from the reactants to the peak is the activation energy."),
             ("Why do exothermic reactions need activation energy?", "Bonds in the reactants must start to break before new bonds can form, and this needs a minimum amount of energy.")],
            sets)


if __name__ == "__main__":
    main()
