# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 20: Radioactivity
  python tools/gen_sg_science_s4_radioactivity.py
The nucleus (protons and neutrons, proton number Z and nucleon number A, nuclide notation), isotopes; background radiation;
alpha, beta and gamma emissions: their nature, ionising effect and penetrating power; nuclear equations for alpha and beta
decay; half-life calculations and decay graphs; uses (smoke detectors, thickness control, tracers, radiotherapy, carbon dating,
sterilisation) and safety precautions; nuclear fission and fusion.
UK and US radioactivity makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "a half-life is half the time for all the atoms to decay", "gamma rays are the most
ionising", "beta decay lowers the proton number", "after two half-lives nothing is left".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 8
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_eq = src("gen_uk_science_y10_atomic_structure_and_radioactivity", "g_eq")
uk_hl = src("gen_uk_science_y10_atomic_structure_and_radioactivity", "g_hl")
us_decay = src("gen_us_science_chem_nuclear_chemistry", "g_decay")
us_half = src("gen_us_science_chem_nuclear_chemistry", "g_half")

NUC = [("C", 6, 12), ("C", 6, 14), ("Na", 11, 23), ("Co", 27, 60), ("Sr", 38, 90), ("I", 53, 131), ("Cs", 55, 137), ("Ra", 88, 226), ("U", 92, 235), ("U", 92, 238),
       ("Am", 95, 241), ("Po", 84, 210), ("K", 19, 40), ("H", 1, 3)]


def nuc(s, z, a):
    return "<sup>%d</sup><sub>%d</sub>%s" % (a, z, s)


def g_pn():
    s, z, a = R.choice(NUC)
    k = R.choice(["p", "n", "e", "A"])
    if k == "p":
        return nq("How many protons are in the nucleus %s?" % nuc(s, z, a), z, [a, a - z, a + z], "", "The proton number (lower number) is %d." % z)
    if k == "n":
        return nq("How many neutrons are in the nucleus %s?" % nuc(s, z, a), a - z, [a, z, a + z], "", "Neutrons = A − Z = %d − %d = %d." % (a, z, a - z))
    if k == "e":
        return nq("How many electrons are in a neutral atom of %s?" % nuc(s, z, a), z, [a, a - z, 0], "", "A neutral atom has as many electrons as protons: %d." % z)
    return nq("What is the nucleon number of the nucleus %s?" % nuc(s, z, a), a, [z, a - z, a + z], "", "The nucleon number (top number) A = protons + neutrons = %d." % a)


EL = {82: "Pb", 83: "Bi", 84: "Po", 86: "Rn", 88: "Ra", 90: "Th", 91: "Pa", 92: "U", 93: "Np", 95: "Am", 7: "N", 6: "C", 12: "Mg", 11: "Na", 28: "Ni", 27: "Co",
      39: "Y", 38: "Sr", 54: "Xe", 53: "I", 56: "Ba", 55: "Cs", 20: "Ca", 19: "K", 2: "He", 1: "H", 89: "Ac", 85: "At", 87: "Fr", 94: "Pu", 96: "Cm",
      81: "Tl", 80: "Hg", 5: "B", 4: "Be", 3: "Li", 9: "F", 8: "O", 10: "Ne", 25: "Mn", 26: "Fe", 36: "Kr", 37: "Rb", 40: "Zr", 52: "Te", 51: "Sb", 17: "Cl", 18: "Ar",
      57: "La", 50: "Sn", 21: "Sc", 22: "Ti"}


def g_decay():
    k = R.choice(["alpha", "beta"])
    if k == "alpha":
        s, z, a = R.choice([("U", 92, 238), ("Ra", 88, 226), ("Po", 84, 210), ("Am", 95, 241), ("Th", 90, 230), ("Rn", 86, 222)])
        z2, a2 = z - 2, a - 4
        ans = nuc(EL.get(z2, "X"), z2, a2)
        wr = [nuc(EL.get(z - 4, "X"), z - 4, a - 2), nuc(EL.get(z + 1, "X"), z + 1, a), nuc(EL.get(z2, "X"), z2, a)]
        if "X" in "".join([ans] + wr):
            return None
        return tq("%s decays by emitting an alpha particle. What nucleus is formed?" % nuc(s, z, a), ans, wr,
                  "An alpha particle is <sup>4</sup><sub>2</sub>He: A falls by 4 and Z falls by 2, giving %s." % ans)
    s, z, a = R.choice([("C", 6, 14), ("Sr", 38, 90), ("I", 53, 131), ("Cs", 55, 137), ("Co", 27, 60), ("Na", 11, 24), ("K", 19, 40), ("H", 1, 3)])
    z2 = z + 1
    ans = nuc(EL.get(z2, "X"), z2, a)
    wr = [nuc(EL.get(z - 1, "X"), z - 1, a), nuc(s, z, a - 1), nuc(EL.get(z - 2, "X"), z - 2, a - 4)]
    if "X" in "".join([ans] + wr) or len(set(wr + [ans])) < 4:
        return None
    return tq("%s decays by emitting a beta particle. What nucleus is formed?" % nuc(s, z, a), ans, wr,
              "In beta decay a neutron becomes a proton and an electron is emitted: A stays the same and Z rises by 1, giving %s." % ans)


def g_hl():
    k = R.choice(["frac", "mass", "time", "T", "count"])
    T = R.choice([2, 5, 6, 8, 10, 15, 20, 30])
    unit = R.choice(["minutes", "hours", "days", "years"])
    n = R.choice([1, 2, 3, 4, 5])
    if k == "frac":
        return tq("What fraction of a radioactive sample remains after %d half-lives?" % n, "1/%d" % 2 ** n, ["1/%d" % (2 * n), "1/%d" % 2 ** (n + 1), "%d/%d" % (2 ** n - 1, 2 ** n)],
                  "After each half-life half is left: (1/2)<sup>%d</sup> = 1/%d." % (n, 2 ** n))
    m0 = R.choice([16, 32, 40, 64, 80, 120, 160, 200, 320])
    m = m0 / 2 ** n
    if k == "mass":
        return nq("A sample contains %d g of a radioactive isotope with a half-life of %d %s. What mass of the isotope remains after %d %s?" % (m0, T, unit, n * T, unit), m,
                  [m0 / (2 * n), m0 / 2, m0 / 2 ** (n + 1)], " g", "%d %s = %d half-lives; %d ÷ 2<sup>%d</sup> = %s g." % (n * T, unit, n, m0, n, nf(m)))
    if k == "time":
        return nq("A radioactive isotope has a half-life of %d %s. How long does it take for %d g to decay to %s g?" % (T, unit, m0, N(m)), n * T,
                  [T * m0 / m / 2, T * (n + 1), T * n / 2], " " + unit, "%d → %s g is %d half-lives: %d × %d = %d %s." % (m0, N(m), n, n, T, n * T, unit))
    if k == "T":
        return nq("The activity of a sample falls from %d counts/min to %s counts/min in %d %s. What is the half-life?" % (m0 * 10, N(m * 10), n * T, unit), T,
                  [n * T, n * T / 2 ** n, n * T * 2], " " + unit, "%d → %s is %d halvings, so T½ = %d ÷ %d = %d %s." % (m0 * 10, N(m * 10), n, n * T, n, T, unit))
    bg = R.choice([20, 30, 40])
    c0 = R.choice([400, 640, 800, 960])
    c = c0 / 2 ** n
    return nq("A Geiger counter reads %d counts/min near a source, including a background count of %d counts/min. The source's half-life is %d %s. What will the counter read after %d %s?" %
              (c0 + bg, bg, T, unit, n * T, unit), c + bg, [(c0 + bg) / 2 ** n, c, c0 / 2], " counts/min",
              "Subtract the background first: %d. After %d half-lives: %s. Add the background back: %s counts/min." % (c0, n, N(c), N(c + bg)))


RAD = [("alpha", "2 protons and 2 neutrons (a helium nucleus)", "+2", "a few cm of air or a sheet of paper", "strongly ionising"),
       ("beta", "a fast-moving electron from the nucleus", "−1", "a few mm of aluminium", "moderately ionising"),
       ("gamma", "electromagnetic radiation of very short wavelength", "0", "several cm of lead or thick concrete (reduced, not completely)", "weakly ionising")]


def g_rad():
    r, what, ch, stop, ion = R.choice(RAD)
    k = R.choice(["what", "stop", "ion", "charge", "which_stop", "which_ion"])
    if k == "what":
        return tq("What is %s radiation?" % r, what, [x[1] for x in RAD if x[0] != r] + ["a proton on its own"], "Alpha: He nucleus. Beta: electron. Gamma: EM wave.")
    if k == "stop":
        return tq("What is needed to absorb most %s radiation?" % r, stop, [x[3] for x in RAD if x[0] != r] + ["nothing: it passes through everything"], "Penetration: alpha < beta < gamma.")
    if k == "ion":
        return tq("How ionising is %s radiation?" % r, ion, [x[4] for x in RAD if x[0] != r] + ["not ionising at all"], "Ionising power: alpha > beta > gamma.")
    if k == "charge":
        return tq("What is the relative charge of %s?" % ("an alpha particle" if r == "alpha" else "a beta particle" if r == "beta" else "gamma radiation"), ch,
                  [x[2] for x in RAD if x[0] != r] + ["+1"], "Alpha +2, beta −1, gamma 0 (uncharged).")
    if k == "which_stop":
        return tq("Which radiation is stopped by a sheet of paper?", "alpha", ["beta", "gamma", "all three"], "Alpha particles are large and highly ionising, so they lose energy quickly.")
    return tq("Which radiation is the most penetrating?", "gamma", ["alpha", "beta", "they are all the same"], "Gamma rays are uncharged and weakly ionising.")


USE = [("a smoke detector", "alpha", "Alpha particles ionise air between two plates; smoke absorbs them and the current falls, setting off the alarm."),
       ("controlling the thickness of paper or aluminium foil", "beta", "The amount of beta getting through changes with thickness; alpha would be stopped and gamma would hardly change."),
       ("sterilising medical instruments", "gamma", "Gamma passes through the packaging and kills microorganisms."),
       ("killing cancer cells (radiotherapy) from outside the body", "gamma", "Gamma can reach a tumour deep inside the body."),
       ("a medical tracer injected into the body", "gamma", "Gamma passes out of the body to a detector and is weakly ionising."),
       ("detecting leaks in underground water pipes", "gamma", "A gamma tracer passes through the soil to a detector above.")]


def g_use():
    u, r, why = R.choice(USE)
    return tq("Which type of radiation is used for %s?" % u, r, [x for x in ("alpha", "beta", "gamma", "X-rays") if x != r], why)


POOL1 = pool(R, [
    ("What are isotopes?", "atoms of the same element with the same number of protons but different numbers of neutrons", ["atoms with different numbers of protons", "atoms that have lost electrons", "atoms of different elements with the same mass"], "Carbon-12 and carbon-14."),
    ("What is radioactive decay?", "the random, spontaneous emission of radiation from an unstable nucleus", ["the burning of a radioactive fuel", "the splitting of every atom at once", "a chemical reaction of a metal"], "It cannot be speeded up by heating."),
    ("What is the half-life of a radioactive isotope?", "the time taken for half of the radioactive nuclei in a sample to decay", ["half the time for all the nuclei to decay", "the time for the sample to lose half its mass of all substances", "the age of the sample"], "Each isotope has its own half-life."),
    ("What is background radiation?", "low-level radiation that is always present from natural and artificial sources", ["radiation only from nuclear power stations", "radiation from mobile phones", "radiation only in laboratories"], "Subtract it from readings."),
    ("Which is a natural source of background radiation?", "radon gas from rocks and soil", ["X-ray machines", "nuclear weapons tests", "smoke detectors"], "Cosmic rays and food are other natural sources."),
    ("Why is radioactive decay described as random?", "It is impossible to predict which nucleus will decay next or when.", ["It happens at the same time for all nuclei.", "It depends on the temperature.", "It can be controlled."], "Only the rate for a large number can be predicted."),
    ("Why is ionising radiation harmful to living cells?", "It can damage DNA, killing cells or causing mutations that may lead to cancer.", ["It makes cells radioactive forever.", "It cools the cells.", "It removes oxygen from cells."], "Ionisation breaks molecules."),
    ("What is nuclear fission?", "the splitting of a large nucleus (such as uranium-235) into two smaller nuclei, releasing energy and neutrons", ["two small nuclei joining", "an electron leaving an atom", "a chemical reaction"], "Used in nuclear power stations."),
    ("What is nuclear fusion?", "the joining of two light nuclei to form a heavier nucleus, releasing energy", ["the splitting of a heavy nucleus", "the decay of a nucleus by alpha emission", "burning hydrogen in oxygen"], "It powers the Sun."),
    ("What happens to the proton number in alpha decay?", "It decreases by 2.", ["It increases by 1.", "It stays the same.", "It decreases by 4."], "The nucleon number decreases by 4."),
])
POOL5 = pool(R, [
    ("Why is an alpha source safe in a smoke detector but dangerous if swallowed?", "Outside the body, alpha cannot pass through skin; inside, it is strongly ionising and damages nearby cells.", ["Alpha becomes gamma inside the body.", "It is never dangerous.", "The detector makes it safe forever."], "Inside the body there is no protection."),
    ("Why should radioactive sources be handled with long tongs?", "Increasing the distance from the source reduces the exposure.", ["Tongs absorb the radiation.", "It keeps the source cool.", "It makes the source decay faster."], "Also limit time and use shielding."),
    ("Why is a beta source used to control the thickness of paper, rather than alpha or gamma?", "Alpha would be stopped by the paper and gamma would pass through almost unchanged; beta's count changes with thickness.",
     ["Beta is the safest radiation.", "Beta has the longest half-life.", "Beta is not ionising."], "The detector reading controls the rollers."),
    ("Why is a gamma emitter with a short half-life chosen as a medical tracer?", "Gamma can be detected outside the body, and the short half-life means the activity soon falls.", ["Gamma is strongly ionising.", "A short half-life makes it last for years.", "It is cheaper."], "Usually a half-life of hours."),
    ("Carbon-14 has a half-life of about 5700 years. A wooden tool has 1/4 of the carbon-14 of living wood. How old is it?", "about 11 400 years", ["about 2850 years", "about 5700 years", "about 22 800 years"], "1/4 means 2 half-lives."),
    ("Radiation from a source passes through paper but is stopped by 3 mm of aluminium. What is it?", "beta", ["alpha", "gamma", "X-rays only"], "Alpha would be stopped by the paper; gamma would pass the aluminium."),
    ("A detector reading barely changes when paper and then aluminium are placed in front of a source, but falls with thick lead. What does the source emit?", "gamma", ["alpha", "beta", "alpha and beta only"], "Only gamma gets through aluminium."),
    ("Why is nuclear waste stored safely for a very long time?", "Some isotopes have very long half-lives and stay radioactive for thousands of years.", ["It becomes more radioactive.", "It might catch fire.", "Its half-life increases with time."], "Shielded storage deep underground."),
    ("A nucleus emits a gamma ray. What happens to its proton and nucleon numbers?", "Both stay the same.", ["Z falls by 2 and A falls by 4.", "Z rises by 1.", "A falls by 1."], "Gamma emission only removes energy."),
    ("Which change can alter the half-life of a radioactive isotope?", "none: heating, cooling and pressure do not change it", ["heating it strongly", "putting it in water", "dissolving it in acid"], "Half-life is a property of the nucleus."),
])


def main():
    sets = U.sets([
        ("The nucleus and isotopes", [(g_pn, 10), POOL1, (us_decay, 2)]),
        ("Alpha, beta and gamma", [(g_rad, 12), POOL1, (POOL5, 2)]),
        ("Nuclear equations", [(g_decay, 8), (uk_eq, 6), (us_decay, 3), POOL1]),
        ("Half-life", [(g_hl, 12), (uk_hl, 4), (us_half, 4)]),
        ("Uses, safety and exam-style questions", [(POOL5, 8), (g_use, 6), (g_hl, 4), (g_decay, 2)]),
    ])
    make_ol(LV, SUBJ, "radioactivity", SORT, "Radioactivity",
            "Describe the structure of an atom in terms of a nucleus of protons and neutrons with electrons around it; use nuclide notation (proton number Z, nucleon number A) "
            "and explain the term isotope; show awareness of background radiation and its sources; describe the nature, ionising effect and penetrating power of alpha, beta "
            "and gamma emissions; write nuclear equations for alpha and beta decay; define half-life and use it in calculations, including with decay data; describe uses "
            "of radioactivity and the precautions needed; describe nuclear fission and fusion (summary of the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Radioactivity", "Radioactivity",
            "Free Secondary 4 O-Level Physics worksheets on radioactivity: nuclide notation, isotopes, alpha, beta and gamma radiation, nuclear equations, half-life, uses and "
            "safety. 100 questions with answers.",
            "Half-life: the time for half the nuclei to decay.", "Alpha: Z − 2, A − 4. Beta: Z + 1, A unchanged.",
            "<p><b>Unstable nuclei decay randomly and emit radiation.</b></p><ul>"
            "<li>Nuclide notation <sup>A</sup><sub>Z</sub>X: Z = protons, A = protons + neutrons. Isotopes have the same Z but different numbers of neutrons.</li>"
            "<li>Alpha (He nucleus): most ionising, stopped by paper. Beta (electron): stopped by a few mm of aluminium. Gamma (EM wave): most penetrating, reduced by lead.</li>"
            "<li>Alpha decay: A − 4, Z − 2. Beta decay: A unchanged, Z + 1.</li>"
            "<li>After n half-lives, (1/2)ⁿ of the nuclei remain. Subtract background radiation before halving counts.</li></ul>",
            [("Ra-226 (Z = 88) emits an alpha particle. New nucleus?", ["A = 226 − 4", "Z = 88 − 2"], "radon-222 (Z = 86)"),
             ("80 g, half-life 6 days. Mass left after 18 days?", ["18 ÷ 6 = 3 half-lives", "80 ÷ 2³"], "10 g")],
            ["Thinking nothing is left after two half-lives. A quarter is left.", "Saying gamma is the most ionising. Alpha is.",
             "Lowering the proton number in beta decay. It rises by 1.", "Forgetting to subtract the background count."],
            [("How do you calculate with half-life?", "Count the number of half-lives that have passed, then halve the amount (or count rate) that many times. Subtract background radiation first."),
             ("What stops alpha, beta and gamma radiation?", "Alpha is stopped by paper or a few cm of air, beta by a few mm of aluminium, and gamma is reduced by thick lead or concrete."),
             ("What happens to the nucleus in alpha and beta decay?", "Alpha decay: the nucleon number falls by 4 and the proton number by 2. Beta decay: a neutron turns into a proton, so the proton number rises by 1 and the nucleon number is unchanged.")],
            sets)


if __name__ == "__main__":
    main()
