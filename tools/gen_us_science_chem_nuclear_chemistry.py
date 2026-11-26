# -*- coding: utf-8 -*-
"""
US High School Chemistry: Nuclear Chemistry (HS-PS1-8)
  python tools/gen_us_science_chem_nuclear_chemistry.py
Develop models to illustrate the changes in the composition of the nucleus of the atom and the energy released during
the processes of fission, fusion, and radioactive decay.
Alpha, beta and gamma decay with nuclide notation; changes in atomic and mass numbers; half-life; fission and fusion;
penetrating power of radiation; nuclear energy compared with chemical energy.
Wrong answers come from real mistakes: "beta decay lowers the mass number", "alpha decay subtracts 2 from the mass
number", "after two half-lives nothing is left", "fusion splits atoms".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_chem import num

U = Unit(90212)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SYM = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe "
       "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am").split()
NAME = {1: "hydrogen", 6: "carbon", 15: "phosphorus", 19: "potassium", 27: "cobalt", 38: "strontium", 53: "iodine", 55: "cesium", 84: "polonium", 86: "radon",
        88: "radium", 90: "thorium", 92: "uranium", 94: "plutonium", 95: "americium", 83: "bismuth", 82: "lead"}


def nuc(a, z):
    return "<sup>%d</sup><sub>%d</sub>%s" % (a, z, SYM[z - 1])


def short(a, z):
    return "%s-%d" % (SYM[z - 1], a)


# parent A, Z, decay type
PAR = [(238, 92, "alpha"), (14, 6, "beta"), (226, 88, "alpha"), (234, 90, "beta"), (210, 84, "alpha"), (60, 27, "beta"), (131, 53, "beta"), (90, 38, "beta"),
       (241, 95, "alpha"), (40, 19, "beta"), (32, 15, "beta"), (222, 86, "alpha"), (3, 1, "beta"), (137, 55, "beta"), (239, 94, "alpha"), (214, 82, "beta"), (218, 84, "alpha"),
       (210, 83, "beta")]
DZ = {"alpha": (-4, -2), "beta": (0, 1), "gamma": (0, 0), "positron": (0, -1)}


def g_decay():
    a, z, t = R.choice(PAR)
    k = R.choice(["prod", "prod", "type"])
    if not once(("dc", a, z, k)):
        return None
    da, dz = DZ[t]
    pa, pz = a + da, z + dz
    if k == "prod":
        w = set()
        for x in ["alpha", "beta", "positron"]:
            if x != t:
                w.add(nuc(a + DZ[x][0], z + DZ[x][1]))
        w.add(nuc(a - 2, z - 2) if t == "alpha" else nuc(a - 1, z + 1))
        w.add(nuc(a - 4, z + 2) if t == "alpha" else nuc(a, z - 1))
        w = sorted(x for x in w if x != nuc(pa, pz))
        nm = NAME.get(z, SYM[z - 1])
        return item("%s (%s) undergoes %s decay. What nucleus forms?" % (nuc(a, z), nm, t), nuc(pa, pz), R.sample(w, 3),
                    "%s decay: mass number %s, atomic number %s." % (t.capitalize(), "−4" if da else "same", {(-2): "−2", 1: "+1", 0: "same", -1: "−1"}[dz]))
    return item("%s decays to %s. What type of decay is this?" % (nuc(a, z), nuc(pa, pz)), "%s decay" % t, ["%s decay" % x for x in ["alpha", "beta", "gamma", "positron"] if x != t],
                "Compare the mass numbers and atomic numbers.")


def g_change():
    t = R.choice(["alpha", "beta", "gamma", "positron"])
    a = R.randint(20, 120) * 2
    z = R.randint(20, 90)
    k = R.choice(["z", "a", "n"])
    if z * 2 > a + 10 or a > 2.6 * z or not once(("cg", t, a, z, k)):
        return None
    da, dz = DZ[t]
    if k == "z":
        v = z + dz
        w = [str(x) for x in dict.fromkeys([z - 4 if t == "alpha" else z - 1, z, z + 2, z + 1, z - 2]) if x != v][:3]
        return item("A nucleus with atomic number %d undergoes %s decay. What is the new atomic number?" % (z, t), str(v), w, "%s decay changes the atomic number by %s." % (t.capitalize(), "%+d" % dz if dz else "0"))
    if k == "a":
        v = a + da
        w = [str(x) for x in dict.fromkeys([a - 2, a, a - 4, a + 1, a - 1]) if x != v][:3]
        return item("A nucleus with mass number %d undergoes %s decay. What is the new mass number?" % (a, t), str(v), w, "%s decay changes the mass number by %s." % (t.capitalize(), "%+d" % da if da else "0"))
    n0 = a - z
    v = n0 + da - dz
    w = [str(x) for x in dict.fromkeys([n0, n0 - 4, n0 + 1, n0 - 2, n0 - 1]) if x != v][:3]
    return item("A nucleus has %d protons and %d neutrons. It undergoes %s decay. How many neutrons does the new nucleus have?" % (z, n0, t), str(v), w,
                {"alpha": "An alpha particle carries away 2 neutrons.", "beta": "A neutron changes into a proton.", "gamma": "Gamma rays carry energy only.", "positron": "A proton changes into a neutron."}[t])


ISO = [("carbon-14", 5730, "years"), ("iodine-131", 8, "days"), ("cobalt-60", 5.3, "years"), ("strontium-90", 29, "years"), ("radon-222", 3.8, "days"),
       ("technetium-99m", 6, "hours"), ("phosphorus-32", 14, "days"), ("cesium-137", 30, "years"), ("polonium-210", 138, "days"), ("hydrogen-3 (tritium)", 12.3, "years")]


def g_half():
    who = P.next()[0]
    nm_, hl, u = R.choice(ISO)
    n = R.randint(1, 5)
    m0 = R.choice([16, 32, 64, 80, 96, 128, 160, 200, 240, 320, 400, 480])
    left = m0 / 2 ** n
    k = R.choice(["left", "time", "frac", "n"])
    if left != round(left, 2) or not once(("hl", nm_, n, m0, k)):
        return None
    t = hl * n
    if k == "left":
        return item("%s has %d g of %s (half-life %s %s). How much is left after %s %s?" % (who, m0, nm_, num(hl), u, num(t), u), "%s g" % num(left),
                    ["%s g" % num(m0 / (2 * n)), "%s g" % num(m0 - left), "0 g" if n > 1 else "%s g" % num(m0 / 4)] if m0 / (2 * n) != left else ["%s g" % num(m0 - left), "%s g" % num(left / 2), "%s g" % num(left * 2)],
                    "%s %s = %d half-lives: %d → %s g." % (num(t), u, n, m0, num(left)))
    if k == "time":
        return item("A %d g sample of %s (half-life %s %s) decays to %s g. How much time has passed?" % (m0, nm_, num(hl), u, num(left)), "%s %s" % (num(t), u),
                    ["%s %s" % (num(hl * (n + 1)), u), "%s %s" % (num(hl * (2 ** n)), u) if n > 1 else "%s %s" % (num(hl / 2), u), "%s %s" % (num(hl), u) if n > 1 else "%s %s" % (num(hl * 3), u)],
                    "%d half-lives × %s %s = %s %s." % (n, num(hl), u, num(t), u))
    if k == "frac":
        good = "1/%d" % (2 ** n)
        w = ["1/%d" % (2 * n), "1/%d" % (2 ** (n + 1)), "%d/%d" % (2 ** n - 1, 2 ** n)] if n > 1 else ["1/4", "0", "1/3"]
        w = [x for x in dict.fromkeys(w) if x != good][:3]
        if len(w) < 3:
            return None
        return item("What fraction of a %s sample is left after %s %s (half-life %s %s)?" % (nm_, num(t), u, num(hl), u), good, w, "(1/2)<sup>%d</sup> = %s." % (n, good))
    return item("How many half-lives pass when %d g of %s decays to %s g?" % (m0, nm_, num(left)), str(n), [str(x) for x in dict.fromkeys([n + 1, max(1, n - 1) if n > 1 else 3, n * 2, n + 2]) if x != n][:3],
                "%d g halves %d times to reach %s g." % (m0, n, num(left)))


FF = [("Two hydrogen nuclei join to form helium in the Sun.", "fusion"), ("A uranium-235 nucleus absorbs a neutron and splits into barium and krypton.", "fission"),
      ("A nuclear power plant splits uranium to boil water.", "fission"), ("Deuterium and tritium combine in an experimental reactor.", "fusion"),
      ("Plutonium-239 nuclei split and release more neutrons in a chain reaction.", "fission"), ("Stars much larger than the Sun build carbon and oxygen from helium.", "fusion"),
      ("A heavy nucleus breaks into two medium-sized nuclei.", "fission"), ("Light nuclei combine at millions of degrees.", "fusion")]


def g_ff():
    s, t = R.choice(FF)
    if not once(("ff", s)):
        return None
    return item("%s Which nuclear process is this?" % s, t, [x for x in ["fission", "fusion", "alpha decay", "a chemical reaction"] if x != t],
                "Fission splits heavy nuclei; fusion joins light nuclei.")


PEN = [("alpha", "a sheet of paper or skin"), ("beta", "a few millimeters of aluminum"), ("gamma", "thick lead or concrete")]


def g_pen():
    t, s = R.choice(PEN)
    k = R.choice(["stop", "what", "charge"])
    if not once(("pn", t, k)):
        return None
    if k == "stop":
        return item("What is needed to stop %s radiation?" % t, s, [x[1] for x in PEN if x[0] != t] + ["nothing can stop it"], "Alpha is least penetrating; gamma is most.")
    if k == "what":
        a = {"alpha": "2 protons and 2 neutrons (a helium nucleus)", "beta": "a high-energy electron", "gamma": "high-energy electromagnetic waves"}[t]
        return item("What is %s radiation made of?" % t, a, [v for kk, v in {"alpha": "2 protons and 2 neutrons (a helium nucleus)", "beta": "a high-energy electron",
                                                                              "gamma": "high-energy electromagnetic waves", "x": "a neutron only"}.items() if v != a], "Alpha: He nucleus; beta: electron; gamma: energy.")
    c = {"alpha": "+2", "beta": "−1", "gamma": "0"}[t]
    return item("What is the charge of %s radiation?" % t, c, [x for x in ["+2", "−1", "0", "+1"] if x != c], "Alpha +2, beta −1, gamma no charge.")


B1 = bank([
    ("What is radioactive decay?", "an unstable nucleus giving off particles or energy", ["an atom gaining electrons", "a chemical reaction with oxygen", "an atom melting"], "Nucleus changes."),
    ("What is a half-life?", "the time for half of a radioactive sample to decay", ["half the time for all of it to decay", "the age of the sample", "the time to double"], "Constant for each isotope."),
    ("How do nuclear reactions differ from chemical reactions?", "They change the nucleus and can change one element into another.", ["They only rearrange electrons.", "They release less energy.", "They never release energy."],
     "Transmutation."),
    ("Why does fission release so much energy?", "A little mass is converted to a lot of energy (E = mc²).", ["Electrons are destroyed.", "Bonds between molecules break.", "It absorbs heat."], "Mass defect."),
    ("Which process powers the Sun?", "nuclear fusion of hydrogen into helium", ["fission of uranium", "burning of coal", "chemical reactions with oxygen"], "Fusion."),
    ("What is a chain reaction in fission?", "neutrons from one split cause more nuclei to split", ["electrons jumping between atoms", "fusion in stars", "a slow decay"], "Self-sustaining."),
    ("Which radiation is the most penetrating?", "gamma rays", ["alpha particles", "beta particles", "visible light"], "Needs lead or concrete."),
    ("In beta decay, what changes inside the nucleus?", "A neutron changes into a proton and an electron is emitted.", ["A proton is lost.", "Two neutrons are lost.", "Nothing changes."], "Atomic number +1."),
])
B5 = bank([
    ("Why is carbon-14 used to date old wood but not dinosaur bones?", "Its half-life (5,730 years) is too short; almost none is left after millions of years.", ["Dinosaurs had no carbon.", "Carbon-14 never decays.", "Wood is radioactive."], "Choose a fitting half-life."),
    ("Why do hospitals use technetium-99m (half-life 6 hours) for scans?", "It gives off gamma rays and decays quickly, so little stays in the body.", ["It never decays.", "It gives off alpha particles.", "It lasts for years."], "Short half-life."),
    ("Why is fusion hard to use on Earth?", "It needs extremely high temperatures and pressures.", ["It releases no energy.", "It uses rare uranium.", "It makes long-lived waste like fission."], "Star-like conditions."),
    ("A smoke detector contains americium-241, an alpha emitter. Why is it safe in a room?", "Alpha particles are stopped by air and the plastic case.", ["Americium is not radioactive.", "Alpha passes through lead.", "It gives no radiation."], "Low penetration."),
    ("Compare the energy from 1 kg of uranium in fission with 1 kg of coal burned.", "Fission releases millions of times more energy.", ["Coal releases more.", "They are equal.", "Uranium releases none."], "Nuclear vs chemical."),
])


def body():
    think = ("<p><b>Nuclear changes alter the nucleus, so one element can become another.</b></p>"
             "<ul><li>Alpha (<sup>4</sup><sub>2</sub>He): mass −4, atomic number −2. Beta (electron): atomic number +1, mass same. Gamma: energy only.</li>"
             "<li>Half-life: after n half-lives, (1/2)<sup>n</sup> of the sample is left.</li>"
             "<li>Fission splits heavy nuclei; fusion joins light nuclei. Both turn a little mass into a lot of energy.</li></ul>")
    ex = [("<sup>238</sup><sub>92</sub>U alpha decay?", ["238 − 4, 92 − 2"], "<sup>234</sup><sub>90</sub>Th"),
          ("80 g, 3 half-lives. Left?", ["80 → 40 → 20 → 10"], "10 g")]
    mist = ["Thinking beta decay lowers the mass number.", "Thinking nothing is left after two half-lives.", "Mixing up fission (split) and fusion (join)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Radioactive decay", B1 + [(g_pen, 6), (g_change, 6)]),
        ("Alpha, beta and gamma", [(g_change, 12), (g_pen, 2), (g_decay, 6)]),
        ("Decay equations", [(g_decay, 16), (g_change, 4)]),
        ("Half-life", [(g_half, 17), (g_ff, 3)]),
        ("Fission, fusion and uses", B5 + [(g_ff, 3), (g_half, 7), (g_decay, 5)]),
    ])
    make("chemistry", "nuclear-chemistry", 12, "HS-PS1-8",
         "Develop models to illustrate the changes in the composition of the nucleus of the atom and the energy released during the processes of fission, fusion, and radioactive decay.",
         "Nuclear Chemistry",
         "Nuclear Chemistry Worksheets: Radioactive Decay, Half-Life, Fission and Fusion (Chemistry)",
         "Nuclear Chemistry",
         "Free high school chemistry worksheets on nuclear chemistry (NGSS HS-PS1-8): alpha, beta and gamma decay, nuclear equations, half-life, fission and fusion. 100 questions with answers.",
         "Nuclear changes alter the nucleus.",
         "Decay, fission and fusion change protons and neutrons and release huge energy.",
         body(),
         [("How do alpha and beta decay change a nucleus?", "Alpha decay lowers the mass number by 4 and the atomic number by 2. Beta decay raises the atomic number by 1 and keeps the mass number the same."),
          ("How do you solve half-life problems?", "Find how many half-lives have passed (time ÷ half-life) and halve the amount that many times."),
          ("What is the difference between fission and fusion?", "Fission splits a heavy nucleus into smaller ones. Fusion joins light nuclei into a heavier one. Both release large amounts of energy.")],
         sets)


if __name__ == "__main__":
    main()
