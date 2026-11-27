# -*- coding: utf-8 -*-
"""Class 12 Chemistry (NCERT Chemistry Part I and II, 10 chapters): question makers and UNITS()."""
import math
from in_sci import _R
from in_srs import ch, A, N, B, SU, pairs, tq, nf, al_chem as C
from in_s11c import T, fm, b_conc
from in_s11b import OD, FAM

CH = "Chemistry"
R_ = 8.314
F_ = 96500


def ri(a, b, step=1):
    return _R[0].randrange(a, b + 1, step)


def rf(a, b, step):
    return round(_R[0].randint(round(a / step), round(b / step)) * step, 6)


def K(f, *kinds):
    return lambda: f(ch(kinds))


def fam(g, *fs):
    FAM[id(g)] = [list(x) for x in fs]


# =================================================================== 1 solutions
SOLV = [("water", 0.52, 1.86), ("benzene", 2.53, 5.12), ("ethanol", 1.20, 1.99), ("camphor", 5.95, 40.0)]
SOL = [("glucose", 180, 1), ("urea", 60, 1), ("sucrose", 342, 1), ("NaCl", 58.5, 2), ("KCl", 74.5, 2), ("CaCl₂", 111, 3), ("MgCl₂", 95, 3), ("K₂SO₄", 174, 3)]


def colli(k=None):
    k = k or ch(["Tb", "Tf", "pi", "M", "rel", "i", "henry", "raoult"])
    nm, M, i = ch(SOL)
    if k in ("Tb", "Tf"):
        s, kb, kf = SOLV[0] if k == "Tf" or ch([0, 1]) else ch(SOLV)
        Kc = kb if k == "Tb" else kf
        w, W = rf(1, 30, 0.5), ri(100, 500, 50)
        m = w / M / (W / 1000)
        d = i * Kc * m
        what = "elevation of boiling point" if k == "Tb" else "depression of freezing point"
        sym = "K<sub>b</sub>" if k == "Tb" else "K<sub>f</sub>"
        return N("%s g of %s is dissolved in %d g of %s. What is the %s? (%s = %s K kg mol⁻¹%s)" % (nf(w), nm, W, s, what, sym, nf(Kc), "; assume complete dissociation, i = %d" % i if i > 1 else ""), d,
                 [Kc * m if i > 1 else Kc * m * 2, Kc * w / M / W, d / Kc if Kc != 1 else d * 2], " K", "m = %s mol kg⁻¹; ΔT = i%sm = <b>%s K</b>." % (nf(m), sym, nf(d)))
    if k == "pi":
        c, T_ = rf(0.01, 0.5, 0.01), ri(273, 310)
        return N("What is the osmotic pressure of a %s M solution of %s at %d K? (R = 0.0821 L atm K⁻¹ mol⁻¹%s)" % (nf(c), nm, T_, "; i = %d" % i if i > 1 else ""), i * c * 0.0821 * T_,
                 [c * 0.0821 * T_ if i > 1 else c * 0.0821 * T_ * 2, i * c * 0.0821, i * c * 8.314 * T_], " atm", "π = iCRT = <b>%s atm</b>." % nf(i * c * 0.0821 * T_))
    if k == "M":
        w, W, d = rf(1, 20, 0.5), ri(100, 500, 50), rf(0.1, 2, 0.05)
        Mm = 1.86 * w * 1000 / (d * W)
        return N("%s g of a non-electrolyte dissolved in %d g of water lowers the freezing point by %s K. What is its molar mass? (K<sub>f</sub> = 1.86 K kg mol⁻¹)" % (nf(w), W, nf(d)), Mm,
                 [1.86 * w / (d * W), Mm / 1000, d * W / (1.86 * w)], " g mol⁻¹", "M = K<sub>f</sub> × w × 1000/(ΔT × W) = <b>%s g mol⁻¹</b>." % nf(Mm))
    if k == "rel":
        n2, n1 = rf(0.1, 2, 0.1), ri(5, 50)
        return N("A solution contains %s mol of a non-volatile solute in %d mol of solvent. What is the relative lowering of vapour pressure?" % (nf(n2), n1), n2 / (n1 + n2), [n2 / n1, n1 / (n1 + n2), n2], "",
                 "Raoult's law: Δp/p° = x(solute) = %s ÷ %s = <b>%s</b>." % (nf(n2), nf(n1 + n2), nf(n2 / (n1 + n2))))
    if k == "i":
        return N("What is the van't Hoff factor of %s, assuming complete dissociation in water?" % nm, i, [i + 1, 1 if i > 1 else 2, i * 2], "", "%s gives %d particle%s per formula unit: i = <b>%d</b>." % (nm, i, "" if i == 1 else "s", i)) if nm not in ("glucose", "urea", "sucrose") or ch([0, 1, 1]) else None
    if k == "henry":
        gas, kh = ch([("nitrogen", 76.48), ("oxygen", 34.86), ("argon", 40.3), ("methane", 0.413), ("carbon dioxide", 1.67), ("hydrogen", 69.16)])
        p = rf(0.5, 5, 0.5)
        return N("Henry's law constant (K<sub>H</sub>) of %s in water is %s kbar. What is its mole fraction in water when its partial pressure is %s bar? (p = K<sub>H</sub>x)" % (gas, nf(kh), nf(p)), p / (kh * 1000),
                 [p * kh, p / kh, kh / p], "", "x = p/K<sub>H</sub> = %s ÷ (%s × 1000) = <b>%s</b>." % (nf(p), nf(kh), nf(p / (kh * 1000))))
    p0, x = ri(20, 200), rf(0.05, 0.95, 0.05)
    return N("Pure liquid A has a vapour pressure of %d kPa. What is the partial vapour pressure of A in an ideal solution where its mole fraction is %s?" % (p0, nf(x)), p0 * x, [p0 * (1 - x), p0 / x, p0], " kPa",
             "Raoult's law: p<sub>A</sub> = x<sub>A</sub>p°<sub>A</sub> = <b>%s kPa</b>." % nf(p0 * x))


B1 = [("Which concentration term does not change with temperature?", "molality", ["molarity", "normality", "volume per cent"], "It is based on mass of solvent."),
      ("What are colligative properties?", "properties that depend only on the number of solute particles, not their nature", ["properties that depend on colour", "properties of pure solvents", "chemical properties of solutes"], "e.g. osmotic pressure."),
      ("Which colligative property is best for finding the molar mass of proteins?", "osmotic pressure", ["boiling point elevation", "freezing point depression", "vapour pressure lowering"], "It can be measured at room temperature and is large for dilute solutions."),
      ("What is an ideal solution?", "one that obeys Raoult's law at all concentrations, with ΔH(mix) = 0 and ΔV(mix) = 0", ["one with no solute", "one that boils at 100 °C", "one with ΔH(mix) negative"], "e.g. benzene and toluene."),
      ("A solution shows positive deviation from Raoult's law. What happens to the A–B interactions?", "they are weaker than A–A and B–B interactions", ["they are stronger", "they are equal", "there are none"], "e.g. ethanol and acetone."),
      ("What is an azeotrope?", "a mixture that boils at a constant temperature with the same composition in liquid and vapour", ["a pure liquid", "a solid solution", "a gas mixture"], "It cannot be separated by fractional distillation."),
      ("Why do scuba divers get 'the bends'?", "nitrogen dissolved at high pressure forms bubbles in the blood when pressure falls", ["oxygen is too low", "water is too cold", "helium is toxic"], "Henry's law: solubility rises with pressure."),
      ("What is reverse osmosis used for?", "desalination of sea water", ["making salt", "boiling water", "freezing water"], "Pressure greater than the osmotic pressure is applied."),
      ("What is an isotonic solution?", "a solution with the same osmotic pressure as another", ["a solution with no solute", "a very concentrated solution", "a solution that boils easily"], "0.9% NaCl is isotonic with blood."),
      ("What happens to red blood cells placed in pure water?", "they swell and may burst", ["they shrink", "nothing happens", "they turn white"], "Water is hypotonic, so it enters the cells."),
      ("What is the van't Hoff factor for a solute that associates (like ethanoic acid in benzene)?", "less than 1", ["more than 1", "exactly 1", "zero"], "Particles join to form dimers."),
      ("Why is salt spread on icy roads?", "it lowers the freezing point of water", ["it raises the freezing point", "it heats the ice", "it absorbs sunlight"], "Depression of freezing point."),
      ("How does the solubility of a gas in water change when temperature rises?", "it decreases", ["it increases", "it stays the same", "it becomes infinite"], "Fish need cold water rich in oxygen."),
      ("What is the unit of the cryoscopic constant K<sub>f</sub>?", "K kg mol⁻¹", ["K mol kg⁻¹", "mol L⁻¹", "atm"], "ΔT<sub>f</sub> = K<sub>f</sub>m.")]


# =================================================================== 2 electrochemistry
def elc(k=None):
    k = k or ch(["nernst", "dG", "far", "Q", "lam", "cc", "kohl"])
    if k == "nernst":
        E0, n = rf(0.2, 1.6, 0.01), ch([1, 2])
        Q = ch([10, 100, 1000, 0.1, 0.01])
        E = E0 - 0.059 / n * math.log10(Q)
        return N("A cell has E°<sub>cell</sub> = %s V, n = %d and reaction quotient Q = %s at 298 K. What is E<sub>cell</sub>? (E = E° − (0.059/n) log Q)" % (nf(E0), n, nf(Q)), E,
                 [E0 + 0.059 / n * math.log10(Q), E0 - 0.059 * math.log10(Q), E0], " V", "E = %s − (0.059/%d) × %s = <b>%s V</b>." % (nf(E0), n, nf(math.log10(Q)), nf(E)))
    if k == "dG":
        E0, n = rf(0.2, 2, 0.01), ch([1, 2, 3, 6])
        G = -n * F_ * E0 / 1000
        return N("A cell reaction has n = %d and E°<sub>cell</sub> = %s V. What is ΔG°? (F = 96,500 C mol⁻¹)" % (n, nf(E0)), G, [-G, -F_ * E0 / 1000, G * 1000], " kJ mol⁻¹", "ΔG° = −nFE° = −%d × 96,500 × %s = <b>%s kJ mol⁻¹</b>." % (n, nf(E0), nf(G)))
    if k == "far":
        I, t = ri(1, 10), ri(10, 120, 10)
        nm, Mm, n = ch([("copper", 63.5, 2), ("silver", 108, 1), ("zinc", 65, 2), ("nickel", 58.7, 2), ("aluminium", 27, 3)])
        m = Mm * I * t * 60 / (n * F_)
        return N("A current of %d A is passed for %d minutes through a solution of a %s salt (the ion has charge +%d). What mass of %s is deposited? (M = %s g mol⁻¹, F = 96,500 C mol⁻¹)" % (I, t, nm, n, nm, nf(Mm)), m,
                 [m * n, Mm * I * t / (n * F_), m / 60], " g", "Q = It = %s C; m = MQ/(nF) = <b>%s g</b>." % (nf(I * t * 60), nf(m)))
    if k == "Q":
        I, t = ri(1, 10), ri(1, 60)
        return N("How much charge passes when a current of %d A flows for %d minutes?" % (I, t), I * t * 60, [I * t, I * t * 60 / F_, I / (t * 60)], " C", "Q = It = %d × %d × 60 = <b>%s C</b>." % (I, t, nf(I * t * 60)))
    if k == "lam":
        kap, c = rf(0.001, 0.05, 0.001), ch([0.01, 0.02, 0.05, 0.1, 0.001])
        L = kap * 1000 / c
        return N("A %s M solution has a conductivity of %s S cm⁻¹. What is its molar conductivity? (Λ<sub>m</sub> = κ × 1000/C)" % (nf(c), nf(kap)), L, [kap / c, kap * c * 1000, L / 1000], " S cm² mol⁻¹", "Λ<sub>m</sub> = %s × 1000 ÷ %s = <b>%s S cm² mol⁻¹</b>." % (nf(kap), nf(c), nf(L)))
    if k == "cc":
        Rv, kap = ri(50, 2000, 10), rf(0.001, 0.02, 0.001)
        return N("A conductivity cell filled with a solution of conductivity %s S cm⁻¹ has a resistance of %d Ω. What is its cell constant?" % (nf(kap), Rv), kap * Rv, [kap / Rv, Rv / kap, 1 / (kap * Rv)], " cm⁻¹", "G* = κR = <b>%s cm⁻¹</b>." % nf(kap * Rv))
    s = ch([("NaCl", 50.1, 76.3), ("KCl", 73.5, 76.3), ("CaCl₂", 119.0, 2 * 76.3), ("MgCl₂", 106.0, 2 * 76.3), ("KNO₃", 73.5, 71.4), ("NaNO₃", 50.1, 71.4)])
    return N("Using λ°(cation) = %s and λ°(anion part) = %s S cm² mol⁻¹, what is Λ°<sub>m</sub> of %s? (Kohlrausch's law)" % (nf(s[1]), nf(s[2]), s[0]), s[1] + s[2], [s[1] * s[2] / 100, abs(s[1] - s[2]), s[1] + s[2] / 2], " S cm² mol⁻¹",
             "Λ°<sub>m</sub> = λ°<sub>+</sub> + λ°<sub>−</sub> = <b>%s S cm² mol⁻¹</b>." % nf(s[1] + s[2]))


B2 = [("What is the standard hydrogen electrode assigned?", "E° = 0.00 V", ["E° = 1.00 V", "E° = −0.76 V", "E° = 0.34 V"], "It is the reference for all electrode potentials."),
      ("In a galvanic cell, where does oxidation occur?", "at the anode", ["at the cathode", "in the salt bridge", "at both electrodes"], "The anode is negative in a galvanic cell."),
      ("What is the role of a salt bridge?", "it completes the circuit and keeps the solutions electrically neutral", ["it supplies electrons", "it is a catalyst", "it stores energy"], "Usually KCl or KNO₃ in agar."),
      ("What happens to the molar conductivity of a solution when it is diluted?", "it increases", ["it decreases", "it stays the same", "it becomes zero"], "Ions move more freely."),
      ("What happens to the conductivity (κ) of a solution on dilution?", "it decreases", ["it increases", "it stays the same", "it doubles"], "There are fewer ions per unit volume."),
      ("Which law relates the mass of substance deposited to the charge passed?", "Faraday's first law of electrolysis", ["Kohlrausch's law", "Ohm's law", "Raoult's law"], "m = ZQ."),
      ("What is one faraday of charge?", "the charge on one mole of electrons, about 96,500 C", ["1 C", "1.6 × 10⁻¹⁹ C", "6.02 × 10²³ C"], "F = N<sub>A</sub>e."),
      ("What is a fuel cell?", "a cell that converts the energy of burning a fuel such as H₂ directly into electricity", ["a rechargeable battery", "a dry cell", "a solar panel"], "Used in the Apollo space programme."),
      ("Which battery is used in cars?", "the lead storage battery", ["the dry cell", "the mercury cell", "the fuel cell"], "It is rechargeable."),
      ("What is corrosion of iron (rusting)?", "an electrochemical process in which iron is oxidised in the presence of water and oxygen", ["iron melting", "iron becoming a magnet", "iron dissolving in oil"], "Rust is hydrated iron(III) oxide."),
      ("How does galvanising protect iron?", "zinc coats the iron and is oxidised in preference to it", ["it paints the iron", "it makes iron magnetic", "it adds carbon"], "Sacrificial protection."),
      ("When is a cell reaction spontaneous?", "when E°<sub>cell</sub> is positive (ΔG° negative)", ["when E°<sub>cell</sub> is negative", "when E°<sub>cell</sub> is zero", "always"], "ΔG° = −nFE°."),
      ("What is the relation between E°<sub>cell</sub> and the equilibrium constant?", "E°<sub>cell</sub> = (0.059/n) log K at 298 K", ["E° = K", "E° = −RT ln K", "E° = nFK"], "At equilibrium E<sub>cell</sub> = 0."),
      ("Which electrolyte's Λ°<sub>m</sub> cannot be found by extrapolating to zero concentration?", "a weak electrolyte such as ethanoic acid", ["a strong electrolyte such as KCl", "NaCl", "HCl"], "Kohlrausch's law is used instead."),
      ("What is the unit of molar conductivity?", "S cm² mol⁻¹", ["S cm⁻¹", "Ω", "S"], "Λ<sub>m</sub> = κ/C.")]


# =================================================================== 3 chemical kinetics
def kin(k=None):
    k = k or ch(["t12", "k12", "int", "zt12", "frac", "temp", "avg"])
    if k == "t12":
        kk = rf(0.001, 0.5, 0.001)
        return N("A first-order reaction has k = %s s⁻¹. What is its half-life?" % nf(kk), 0.693 / kk, [kk / 0.693, 0.693 * kk, 1 / kk], " s", "t<sub>½</sub> = 0.693/k = <b>%s s</b>." % nf(0.693 / kk))
    if k == "k12":
        t = ri(5, 200, 5)
        return N("A first-order reaction has a half-life of %d min. What is its rate constant?" % t, 0.693 / t, [t / 0.693, 0.693 * t, 1 / t], " min⁻¹", "k = 0.693/t<sub>½</sub> = <b>%s min⁻¹</b>." % nf(0.693 / t))
    if k == "int":
        t = ri(10, 100, 10)
        f = ch([2, 4, 5, 10, 8, 100])
        kk = 2.303 / t * math.log10(f)
        return N("In a first-order reaction the concentration falls to 1/%d of its starting value in %d min. What is k? (k = (2.303/t) log([R]₀/[R]))" % (f, t), kk, [kk * 2.303, math.log10(f) / t, kk * t], " min⁻¹", "k = (2.303/%d) × log %d = <b>%s min⁻¹</b>." % (t, f, nf(kk)))
    if k == "zt12":
        R0, kk = rf(0.1, 2, 0.1), rf(0.001, 0.05, 0.001)
        return N("A zero-order reaction has [R]₀ = %s mol L⁻¹ and k = %s mol L⁻¹ s⁻¹. What is its half-life?" % (nf(R0), nf(kk)), R0 / (2 * kk), [0.693 / kk, R0 / kk, 2 * kk / R0], " s", "For zero order t<sub>½</sub> = [R]₀/2k = <b>%s s</b>." % nf(R0 / (2 * kk)))
    if k == "frac":
        n = ri(1, 6)
        return N("What fraction of a first-order reactant remains after %d half-lives?" % n, 0.5 ** n, [1 / (2 * n), 1 - 0.5 ** n, 0.5 ** (n + 1)], "", "(½)<sup>%d</sup> = <b>%s</b>." % (n, nf(0.5 ** n)))
    if k == "temp":
        dT = ch([10, 20, 30, 40])
        q = ch([2, 3])
        return N("The rate of a reaction becomes %d times for every 10 K rise. By what factor does it increase for a rise of %d K?" % (q, dT), q ** (dT // 10), [q * dT // 10, q * 2, dT], " times", "Factor = %d<sup>%d</sup> = <b>%d</b>." % (q, dT // 10, q ** (dT // 10)))
    c1, c2, t = rf(0.5, 2, 0.1), rf(0.1, 0.4, 0.05), ri(10, 100, 10)
    return N("The concentration of a reactant falls from %s to %s mol L⁻¹ in %d s. What is the average rate of reaction?" % (nf(c1), nf(c2), t), (c1 - c2) / t, [(c1 + c2) / t, c1 / t, (c1 - c2) * t], " mol L⁻¹ s⁻¹",
             "Rate = −Δ[R]/Δt = %s ÷ %d = <b>%s mol L⁻¹ s⁻¹</b>." % (nf(c1 - c2), t, nf((c1 - c2) / t)))


B3 = [("What is the order of a reaction?", "the sum of the powers of the concentration terms in the rate law", ["the number of molecules in the balanced equation always", "the rate constant", "the speed of reaction"], "It is found by experiment."),
      ("What is molecularity?", "the number of particles taking part in an elementary step", ["the order of reaction", "the rate constant", "the number of products"], "It is always a whole number."),
      ("Can the order of a reaction be zero or a fraction?", "yes", ["no, never", "only zero", "only a fraction"], "Molecularity cannot."),
      ("What is a pseudo first-order reaction?", "a reaction that behaves as first order because one reactant is in large excess", ["a reaction of order zero", "a reaction with no rate", "a reversible reaction"], "e.g. hydrolysis of an ester in water."),
      ("What is the unit of k for a first-order reaction?", "s⁻¹", ["mol L⁻¹ s⁻¹", "L mol⁻¹ s⁻¹", "no unit"], "For zero order it is mol L⁻¹ s⁻¹."),
      ("Does the half-life of a first-order reaction depend on the starting concentration?", "no", ["yes, directly", "yes, inversely", "only at high temperature"], "t<sub>½</sub> = 0.693/k."),
      ("What does the Arrhenius equation relate?", "the rate constant to the temperature and activation energy", ["the order to concentration", "pressure to volume", "mass to charge"], "k = A e<sup>−Ea/RT</sup>."),
      ("How does a catalyst increase the rate of reaction?", "it provides a path with a lower activation energy", ["it raises the temperature", "it changes ΔG", "it shifts equilibrium"], "It is not used up."),
      ("What are effective collisions?", "collisions with enough energy and the right orientation to form products", ["all collisions", "collisions at low speed", "collisions with walls"], "Collision theory."),
      ("Why does the rate of reaction rise with temperature?", "more molecules have energy greater than the activation energy", ["molecules get bigger", "the activation energy rises", "fewer collisions happen"], "The Maxwell–Boltzmann distribution shifts."),
      ("What does the slope of a graph of ln k against 1/T give?", "−E<sub>a</sub>/R", ["E<sub>a</sub>", "A", "−RT"], "From the Arrhenius equation."),
      ("For a zero-order reaction, how does the concentration change with time?", "it falls linearly", ["it falls exponentially", "it stays constant", "it rises"], "[R] = [R]₀ − kt."),
      ("What is the rate-determining step?", "the slowest step in a reaction mechanism", ["the fastest step", "the first step always", "the last step always"], "It controls the overall rate."),
      ("What is the half-life of a zero-order reaction proportional to?", "the initial concentration", ["1/initial concentration", "nothing", "the square of the concentration"], "t<sub>½</sub> = [R]₀/2k.")]


# =================================================================== 4 d and f block
ION = [("Sc³⁺", 0), ("Ti³⁺", 1), ("V³⁺", 2), ("Cr³⁺", 3), ("Mn²⁺", 5), ("Fe²⁺", 4), ("Fe³⁺", 5), ("Co²⁺", 3), ("Ni²⁺", 2), ("Cu²⁺", 1), ("Cu⁺", 0), ("Zn²⁺", 0), ("Mn³⁺", 4), ("Cr²⁺", 4), ("Co³⁺", 4), ("V²⁺", 3), ("Ti⁴⁺", 0)]


def dblock(k=None):
    k = k or ch(["mu", "unp", "col"])
    ion, n = ch(ION)
    if k == "mu":
        mu = math.sqrt(n * (n + 2))
        return N("What is the spin-only magnetic moment of %s (aqueous, high spin)? (μ = √(n(n + 2)) BM)" % ion, round(mu, 2), [math.sqrt(n * (n + 1)) if n else 1.73, n, math.sqrt((n + 1) * (n + 3))], " BM",
                 "%s has %d unpaired electron%s: μ = √(%d × %d) = <b>%s BM</b>." % (ion, n, "" if n == 1 else "s", n, n + 2, nf(mu))) if n else \
            tq("What is the spin-only magnetic moment of %s?" % ion, "0 BM (diamagnetic)", ["1.73 BM", "2.83 BM", "3.87 BM"], "%s has no unpaired electrons." % ion)
    if k == "unp":
        return N("How many unpaired electrons are there in a free %s ion (high spin)?" % ion, n, [n + 1, n + 2, abs(n - 1) or 3], "", "Its d configuration gives <b>%d</b> unpaired electron%s." % (n, "" if n == 1 else "s"))
    a = "colourless" if n == 0 and ion not in ("Ti⁴⁺",) else ("colourless" if n == 0 else "coloured")
    return tq("Is the aqueous %s ion expected to be coloured or colourless?" % ion, a, ["coloured" if a == "colourless" else "colourless", "always black", "it depends only on the anion"],
              "Colour needs d–d transitions, so a partly filled d subshell. %s has %s." % (ion, "no unpaired d electrons (d⁰ or d¹⁰)" if n == 0 else "unpaired d electrons"))


DF = {"a 3d transition metal": ["titanium", "vanadium", "chromium", "manganese", "iron", "cobalt", "nickel", "copper"], "a lanthanoid": ["cerium", "neodymium", "europium", "gadolinium", "lutetium"],
      "an actinoid": ["thorium", "uranium", "plutonium", "americium"], "a d-block element that is not a typical transition element": ["zinc", "cadmium", "mercury"]}
B4 = [("Why are zinc, cadmium and mercury not regarded as transition elements?", "they have completely filled d orbitals in their atoms and common ions", ["they are not metals", "they are radioactive", "they have no d electrons at all"], "Zn²⁺ is d¹⁰."),
      ("Why do transition metals show variable oxidation states?", "the (n − 1)d and ns electrons have similar energies", ["they have no electrons", "they are very large", "they are gases"], "Manganese shows +2 to +7."),
      ("Which oxidation state of manganese is highest?", "+7, as in KMnO₄", ["+2", "+4", "+3"], "All 3d and 4s electrons are used."),
      ("Why are transition metal compounds often coloured?", "d–d transitions absorb visible light", ["they are metals", "they contain water", "they are radioactive"], "The colour seen is the complementary colour."),
      ("Why are transition metals good catalysts?", "they can change oxidation state and adsorb reactants on their surfaces", ["they are heavy", "they are cheap", "they do not react"], "e.g. Fe in the Haber process, V₂O₅ in the Contact process."),
      ("What is the lanthanoid contraction?", "the steady decrease in atomic and ionic radii across the lanthanoids", ["an increase in size", "a nuclear reaction", "a colour change"], "4f electrons shield the nucleus poorly."),
      ("Why do Zr and Hf have almost the same radius?", "lanthanoid contraction", ["they are isotopes", "they are in the same period", "they have the same mass"], "So they are hard to separate."),
      ("What is the common oxidation state of lanthanoids?", "+3", ["+1", "+2 only", "+7"], "Ce also shows +4, Eu +2."),
      ("What colour is potassium dichromate?", "orange", ["purple", "green", "blue"], "K₂Cr₂O₇."),
      ("What colour is potassium permanganate solution?", "deep purple", ["orange", "colourless", "yellow"], "KMnO₄."),
      ("In acid, dichromate is reduced to which ion?", "Cr³⁺ (green)", ["Cr²⁺", "CrO₄²⁻", "Cr⁶⁺"], "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O."),
      ("In acid, permanganate is reduced to which ion?", "Mn²⁺ (nearly colourless)", ["MnO₂", "MnO₄²⁻", "Mn³⁺"], "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O."),
      ("What are interstitial compounds?", "compounds formed when small atoms like H, C or N are trapped in the lattice of a metal", ["ionic salts", "alloys of two noble gases", "organic polymers"], "They are hard and have high melting points."),
      ("Why are actinoids harder to study than lanthanoids?", "most are radioactive and have short half-lives", ["they are gases", "they are very common", "they have no electrons"], "Many are made artificially."),
      ("Which element has the configuration [Ar] 3d⁵ 4s¹?", "chromium", ["manganese", "vanadium", "iron"], "Half-filled d subshell is extra stable.")]


# =================================================================== 5 coordination compounds
WERNER = [("[Co(NH₃)₆]Cl₃", 4, "1 complex ion + 3 Cl⁻"), ("[Co(NH₃)₅Cl]Cl₂", 3, "1 complex ion + 2 Cl⁻"), ("[Co(NH₃)₄Cl₂]Cl", 2, "1 complex ion + 1 Cl⁻"), ("[Pt(NH₃)₂Cl₂]", 1, "a neutral complex, no ions"),
          ("K₄[Fe(CN)₆]", 5, "4 K⁺ + 1 complex ion"), ("K₃[Fe(CN)₆]", 4, "3 K⁺ + 1 complex ion"), ("[Cu(NH₃)₄]SO₄", 2, "1 complex ion + 1 SO₄²⁻"), ("[Ni(CO)₄]", 1, "a neutral complex, no ions"),
          ("[Cr(H₂O)₆]Cl₃", 4, "1 complex ion + 3 Cl⁻"), ("[Cr(H₂O)₅Cl]Cl₂", 3, "1 complex ion + 2 Cl⁻"), ("K₂[PtCl₆]", 3, "2 K⁺ + 1 complex ion"), ("[Ag(NH₃)₂]Cl", 2, "1 complex ion + 1 Cl⁻")]


def coord(k=None):
    cpd, n, e = ch(WERNER)
    if (k or ch(["ions", "agcl"])) == "ions" or "Cl" not in cpd.split("]")[-1]:
        return N("How many ions does one formula unit of %s give in water?" % cpd, n, [n + 1, n - 1 if n > 1 else 3, n + 2], "", "%s: <b>%d</b>." % (e, n))
    m = {"Cl₃": 3, "Cl₂": 2}.get(cpd[-3:], 1)
    return N("How many moles of AgCl precipitate when excess AgNO₃ is added to one mole of %s?" % cpd, m, [m + 1, n, 3 if m != 3 else 6], " mol", "Only the chloride ions outside the square brackets are free: <b>%d mol</b>." % m)


LIG = [("ethane-1,2-diamine (en)", "bidentate"), ("oxalate (C₂O₄²⁻)", "bidentate"), ("EDTA⁴⁻", "hexadentate"), ("NH₃", "monodentate"), ("H₂O", "monodentate"), ("Cl⁻", "monodentate"),
       ("CN⁻", "monodentate (and ambidentate)"), ("NO₂⁻", "monodentate (and ambidentate)"), ("SCN⁻", "monodentate (and ambidentate)"), ("CO", "monodentate")]
CONAME = [("[Co(NH₃)₆]³⁺", "hexaamminecobalt(III) ion"), ("[Fe(CN)₆]⁴⁻", "hexacyanidoferrate(II) ion"), ("[Fe(CN)₆]³⁻", "hexacyanidoferrate(III) ion"), ("[Cu(NH₃)₄]²⁺", "tetraamminecopper(II) ion"),
          ("[Ni(CO)₄]", "tetracarbonylnickel(0)"), ("[PtCl₆]²⁻", "hexachloridoplatinate(IV) ion"), ("[Co(NH₃)₅Cl]²⁺", "pentaamminechloridocobalt(III) ion"), ("[Ag(NH₃)₂]⁺", "diamminesilver(I) ion"),
          ("[Cr(H₂O)₆]³⁺", "hexaaquachromium(III) ion"), ("[Zn(OH)₄]²⁻", "tetrahydroxidozincate(II) ion")]
B5 = [("What is a ligand?", "an ion or molecule that donates a pair of electrons to the central metal", ["a metal atom", "the counter ion", "a catalyst"], "Ligands are Lewis bases."),
      ("What is the coordination number of the metal in [Co(en)₃]³⁺?", "6", ["3", "4", "9"], "Each en is bidentate."),
      ("What is a chelate?", "a ring complex formed by a polydentate ligand", ["a neutral ligand", "a simple salt", "a double salt"], "Chelates are extra stable."),
      ("What is the difference between a double salt and a complex?", "a double salt gives all its ions in water; a complex ion stays intact", ["there is no difference", "a complex has no metal", "a double salt is a gas"], "e.g. Mohr's salt vs K₄[Fe(CN)₆]."),
      ("Which isomerism is shown by [Pt(NH₃)₂Cl₂]?", "geometrical (cis–trans) isomerism", ["optical isomerism only", "linkage isomerism", "ionisation isomerism"], "Cisplatin is an anticancer drug."),
      ("Which isomers are [Co(NH₃)₅(NO₂)]²⁺ and [Co(NH₃)₅(ONO)]²⁺?", "linkage isomers", ["ionisation isomers", "geometrical isomers", "hydrate isomers"], "NO₂⁻ binds through N or O."),
      ("Which isomers are [Co(NH₃)₅SO₄]Br and [Co(NH₃)₅Br]SO₄?", "ionisation isomers", ["linkage isomers", "optical isomers", "coordination isomers"], "They give different ions in solution."),
      ("What does crystal field theory say about d orbitals in an octahedral field?", "they split into a lower t₂g set and a higher e<sub>g</sub> set", ["they stay equal in energy", "they split into four sets", "they disappear"], "The gap is Δ₀."),
      ("Which is a strong field ligand?", "CN⁻", ["I⁻", "Br⁻", "Cl⁻"], "It causes a large splitting and low-spin complexes."),
      ("Why is [Ni(CO)₄] tetrahedral and diamagnetic?", "Ni(0) uses sp³ hybrids and all its electrons are paired", ["Ni is +2", "it is square planar", "CO is a weak ligand"], "CO pairs the 4s electrons into 3d."),
      ("What is the oxidation state of iron in K₄[Fe(CN)₆]?", "+2", ["+3", "+4", "0"], "4(+1) + x + 6(−1) = 0."),
      ("Which complex is used to treat lead poisoning?", "EDTA (as its calcium complex)", ["cisplatin", "haemoglobin", "Wilkinson's catalyst"], "It chelates Pb²⁺."),
      ("Which metal is at the centre of chlorophyll?", "magnesium", ["iron", "cobalt", "copper"], "Haemoglobin has iron; vitamin B₁₂ has cobalt."),
      ("What is the colour of [Ti(H₂O)₆]³⁺ due to?", "a d–d transition of its single d electron", ["charge on water", "a nuclear change", "the chloride ion"], "It absorbs green-yellow light and looks violet.")]


# =================================================================== 6–9 organic chapters
G6 = {"a primary (1°) haloalkane": ["1-bromobutane", "1-chloropropane", "bromoethane", "1-iodopentane", "1-bromopentane", "1-chloro-2-methylpropane"],
      "a secondary (2°) haloalkane": ["2-bromobutane", "2-chloropropane", "3-bromopentane", "2-iodobutane", "bromocyclohexane", "2-iodopropane"],
      "a tertiary (3°) haloalkane": ["2-bromo-2-methylpropane", "2-chloro-2-methylbutane", "3-chloro-3-methylpentane", "2-iodo-2-methylpropane", "1-bromo-1-methylcyclohexane"],
      "an aryl halide": ["chlorobenzene", "bromobenzene", "iodobenzene", "4-chlorotoluene", "1,4-dichlorobenzene", "fluorobenzene"], "a benzylic halide": ["benzyl chloride (C₆H₅CH₂Cl)", "benzyl bromide", "1-chloro-1-phenylethane"],
      "an allylic halide": ["3-chloropropene (allyl chloride)", "3-bromopropene", "3-chlorocyclohexene", "1-bromobut-2-ene"], "a vinylic halide": ["chloroethene (vinyl chloride)", "bromoethene", "2-chloropropene"],
      "a gem-dihalide": ["1,1-dichloroethane", "2,2-dibromopropane", "1,1-dibromopropane"], "a vic-dihalide": ["1,2-dichloroethane", "1,2-dibromopropane", "2,3-dibromobutane"]}
fam(G6, ["a primary (1°) haloalkane", "a secondary (2°) haloalkane", "a tertiary (3°) haloalkane"], ["an aryl halide", "a benzylic halide", "an allylic halide", "a vinylic halide"], ["a gem-dihalide", "a vic-dihalide"])
R6 = [("Finkelstein reaction", "R–Cl + NaI in dry acetone → R–I"), ("Swarts reaction", "R–Br + AgF → R–F"), ("Wurtz reaction", "2RX + 2Na in dry ether → R–R"), ("Wurtz–Fittig reaction", "ArX + RX + 2Na → Ar–R"),
      ("Fittig reaction", "2ArX + 2Na → Ar–Ar"), ("Sandmeyer reaction", "ArN₂⁺Cl⁻ + CuCl/HCl → Ar–Cl"), ("dehydrohalogenation", "R–CH₂CH₂X + alcoholic KOH → alkene"), ("Grignard reagent formation", "RX + Mg in dry ether → RMgX")]
B6 = [("Which mechanism does a tertiary haloalkane prefer with a weak nucleophile in a polar solvent?", "S<sub>N</sub>1", ["S<sub>N</sub>2", "E2 only", "free radical"], "A stable tertiary carbocation forms."),
      ("Which mechanism does a primary haloalkane usually follow?", "S<sub>N</sub>2", ["S<sub>N</sub>1", "electrophilic addition", "free radical"], "There is little steric hindrance."),
      ("What happens to the configuration in an S<sub>N</sub>2 reaction?", "it is inverted (Walden inversion)", ["it is kept", "it racemises", "it disappears"], "The nucleophile attacks from the back."),
      ("What happens to the configuration in an S<sub>N</sub>1 reaction of an optically active haloalkane?", "racemisation (mostly)", ["complete inversion", "complete retention", "no change"], "The planar carbocation is attacked from both sides."),
      ("Which is the most reactive towards S<sub>N</sub>2: CH₃Br, CH₃CH₂Br, (CH₃)₂CHBr or (CH₃)₃CBr?", "CH₃Br", ["(CH₃)₃CBr", "(CH₃)₂CHBr", "CH₃CH₂Br"], "Least steric hindrance."),
      ("What does Saytzeff's (Zaitsev's) rule say?", "in elimination, the more substituted alkene is the main product", ["the less substituted alkene forms", "no alkene forms", "H goes to the carbon with more H"], "e.g. 2-bromobutane gives mainly but-2-ene."),
      ("Why are aryl halides less reactive towards nucleophilic substitution?", "the C–X bond has partial double-bond character from resonance", ["they are gases", "they have no halogen", "they are ionic"], "The carbon is also sp² hybridised."),
      ("What is a chiral molecule?", "a molecule that is not superimposable on its mirror image", ["a molecule with a double bond", "a symmetrical molecule", "a molecule with no carbon"], "It usually has an asymmetric carbon."),
      ("What is a racemic mixture?", "an equal mixture of two enantiomers, which is optically inactive", ["a pure enantiomer", "a mixture of isomers of different formulae", "a racemate of gases"], "Rotations cancel."),
      ("Which compound was used as an anaesthetic but is now known to be harmful?", "chloroform (CHCl₃)", ["iodoform", "DDT", "freon"], "It forms poisonous phosgene in air and light."),
      ("Which compounds damage the ozone layer?", "freons (chlorofluorocarbons)", ["iodoform", "chlorobenzene", "methanol"], "They release chlorine radicals in the stratosphere."),
      ("Which insecticide is now banned in many countries because it builds up in food chains?", "DDT", ["freon", "iodoform", "carbon tetrachloride"], "It is not easily broken down."),
      ("What is the order of reactivity of haloalkanes with the same alkyl group?", "R–I > R–Br > R–Cl > R–F", ["R–F > R–Cl > R–Br > R–I", "all are equal", "R–Cl > R–I"], "The C–I bond is weakest."),
      ("What are ambident nucleophiles?", "nucleophiles that can attack through two different atoms, such as CN⁻ and NO₂⁻", ["nucleophiles with no charge", "electrophiles", "free radicals"], "KCN gives nitriles; AgCN gives isocyanides.")]

G7 = {"a primary (1°) alcohol": ["ethanol", "propan-1-ol", "butan-1-ol", "2-methylpropan-1-ol", "methanol", "pentan-1-ol", "benzyl alcohol", "3-methylbutan-1-ol"],
      "a secondary (2°) alcohol": ["propan-2-ol", "butan-2-ol", "pentan-3-ol", "cyclohexanol", "pentan-2-ol", "3-methylbutan-2-ol", "1-phenylethanol"],
      "a tertiary (3°) alcohol": ["2-methylpropan-2-ol", "2-methylbutan-2-ol", "3-methylpentan-3-ol", "1-methylcyclohexanol", "2-phenylpropan-2-ol"],
      "a phenol": ["phenol", "o-cresol", "catechol", "resorcinol", "picric acid", "quinol (hydroquinone)", "p-cresol", "m-nitrophenol"],
      "an ether": ["methoxymethane", "ethoxyethane", "methoxybenzene (anisole)", "methoxyethane", "ethoxybenzene (phenetole)", "1-methoxypropane", "2-ethoxypropane"],
      "a dihydric alcohol (diol)": ["ethane-1,2-diol", "propane-1,2-diol", "butane-2,3-diol"]}
fam(G7, ["a primary (1°) alcohol", "a secondary (2°) alcohol", "a tertiary (3°) alcohol"], ["a phenol", "an ether", "a dihydric alcohol (diol)"])
R7 = [("Lucas test", "telling 1°, 2° and 3° alcohols apart with conc. HCl and ZnCl₂"), ("Reimer–Tiemann reaction", "phenol + CHCl₃ + NaOH → salicylaldehyde"), ("Kolbe's reaction", "sodium phenoxide + CO₂ → salicylic acid"),
      ("Williamson synthesis", "an alkyl halide + a sodium alkoxide → an ether"), ("hydroboration–oxidation", "an alkene + B₂H₆, then H₂O₂/OH⁻ → an anti-Markovnikov alcohol"), ("acid-catalysed hydration", "an alkene + water with H⁺ → a Markovnikov alcohol"),
      ("dehydration at 443 K", "ethanol with conc. H₂SO₄ → ethene"), ("bromination of phenol in water", "phenol + bromine water → 2,4,6-tribromophenol (white precipitate)")]
B7 = [("Which is more acidic, phenol or ethanol?", "phenol", ["ethanol", "both are equal", "neither is acidic"], "The phenoxide ion is stabilised by resonance."),
      ("Which phenol is the most acidic?", "2,4,6-trinitrophenol (picric acid)", ["phenol", "o-cresol", "p-methylphenol"], "Electron-withdrawing –NO₂ groups stabilise the phenoxide ion."),
      ("Which alcohol reacts fastest with the Lucas reagent?", "a tertiary alcohol, which gives turbidity at once", ["a primary alcohol", "methanol", "a secondary alcohol"], "Tertiary carbocations form readily."),
      ("What does oxidation of a primary alcohol with PCC give?", "an aldehyde", ["a ketone", "a carboxylic acid", "an ether"], "Strong oxidants go on to the acid."),
      ("What does oxidation of a secondary alcohol give?", "a ketone", ["an aldehyde", "a carboxylic acid", "no reaction"], "e.g. propan-2-ol → propanone."),
      ("Why do alcohols have higher boiling points than ethers of similar mass?", "alcohols form hydrogen bonds", ["ethers are ionic", "alcohols are heavier", "ethers have no oxygen"], "Ethers cannot hydrogen-bond with each other."),
      ("What is denatured alcohol?", "ethanol made unfit to drink by adding poisons such as methanol and a dye", ["pure ethanol", "methanol only", "alcohol mixed with water"], "Methanol can cause blindness."),
      ("What is formed when phenol reacts with dilute HNO₃ at low temperature?", "a mixture of o- and p-nitrophenols", ["picric acid", "benzoic acid", "aniline"], "Conc. HNO₃ gives picric acid."),
      ("Why is o-nitrophenol steam volatile but p-nitrophenol is not?", "o-nitrophenol has intramolecular hydrogen bonding", ["p-nitrophenol is lighter", "o-nitrophenol is ionic", "p-nitrophenol has no –OH"], "p-Nitrophenol forms intermolecular H-bonds."),
      ("What is the product when anisole reacts with HI?", "phenol and iodomethane", ["iodobenzene and methanol", "benzene", "toluene"], "The O–CH₃ bond breaks, not the O–aryl bond."),
      ("Which reagent converts an alcohol into a haloalkane with SO₂ and HCl as gaseous by-products?", "thionyl chloride (SOCl₂)", ["PCl₃", "HBr", "NaCl"], "The by-products escape, leaving pure product."),
      ("What is the main product of heating ethanol with conc. H₂SO₄ at 413 K?", "ethoxyethane", ["ethene", "ethanoic acid", "ethanal"], "At 443 K ethene forms."),
      ("How do alcohols react with sodium metal?", "they give alkoxides and hydrogen gas", ["they give alkenes", "they do not react", "they give ethers directly"], "This shows they are weakly acidic.")]

G8 = {"an aldehyde": ["methanal", "ethanal", "benzaldehyde", "propanal", "butanal", "pentanal", "3-methylbutanal", "4-methylbenzaldehyde"],
      "a ketone": ["propanone", "butanone", "acetophenone", "pentan-3-one", "benzophenone", "hexan-2-one", "cyclohexanone", "3-methylbutan-2-one"],
      "a carboxylic acid": ["methanoic acid", "ethanoic acid", "benzoic acid", "propanoic acid", "oxalic acid", "butanoic acid", "phthalic acid", "hexanedioic acid (adipic acid)"],
      "an ester": ["ethyl ethanoate", "methyl benzoate", "methyl methanoate", "propyl ethanoate"], "an acyl chloride": ["ethanoyl chloride", "benzoyl chloride", "propanoyl chloride"],
      "an acid anhydride": ["ethanoic anhydride", "benzoic anhydride", "phthalic anhydride"]}
fam(G8, ["an aldehyde", "a ketone", "a carboxylic acid"], ["an ester", "an acyl chloride", "an acid anhydride"])
R8 = [("Rosenmund reduction", "an acyl chloride + H₂ over Pd/BaSO₄ → an aldehyde"), ("Stephen reaction", "a nitrile + SnCl₂/HCl, then water → an aldehyde"), ("Etard reaction", "toluene + CrO₂Cl₂ → benzaldehyde"),
      ("Clemmensen reduction", "C=O → CH₂ with Zn-Hg and conc. HCl"), ("Wolff–Kishner reduction", "C=O → CH₂ with hydrazine and KOH in ethylene glycol"), ("aldol condensation", "two aldehydes with α-H in dilute alkali → a β-hydroxy aldehyde"),
      ("Cannizzaro reaction", "an aldehyde with no α-H + conc. alkali → an alcohol and a carboxylic acid salt"), ("Hell–Volhard–Zelinsky reaction", "a carboxylic acid + Cl₂/red P → an α-chloro acid"),
      ("Tollens' test", "a silver mirror shows an aldehyde"), ("Fehling's test", "a red-brown precipitate shows an aliphatic aldehyde"), ("iodoform test", "a yellow precipitate shows a CH₃CO– group or CH₃CH(OH)–")]
B8 = [("Why are aldehydes more reactive than ketones in nucleophilic addition?", "they have less steric hindrance and less electron release to the carbonyl carbon", ["they are heavier", "they have no carbonyl", "ketones are gases"], "Ketones have two alkyl groups."),
      ("Which compound gives a positive iodoform test?", "ethanal", ["methanal", "benzaldehyde", "propanal"], "It has a CH₃CO– group."),
      ("Which aldehyde undergoes the Cannizzaro reaction?", "methanal (no α-hydrogen)", ["ethanal", "propanal", "butanal"], "Benzaldehyde also does."),
      ("Why are carboxylic acids more acidic than alcohols?", "the carboxylate ion is stabilised by resonance", ["they have more oxygen", "they are liquids", "alcohols have no hydrogen"], "The charge is spread over two oxygens."),
      ("Which is the strongest acid: CH₃COOH, ClCH₂COOH, Cl₂CHCOOH or Cl₃CCOOH?", "Cl₃CCOOH", ["CH₃COOH", "ClCH₂COOH", "Cl₂CHCOOH"], "Electron-withdrawing Cl atoms stabilise the anion."),
      ("Why do carboxylic acids have high boiling points?", "they form dimers by hydrogen bonding", ["they are ionic", "they are polymers", "they have no hydrogen"], "Higher than alcohols of similar mass."),
      ("What does ethanal form with HCN?", "a cyanohydrin", ["an acetal", "an oxime", "a hydrazone"], "Nucleophilic addition of CN⁻."),
      ("What is formed when an aldehyde reacts with hydroxylamine?", "an oxime", ["a hydrazone", "a semicarbazone", "an imine of ammonia only"], "C=N–OH."),
      ("What is decarboxylation?", "removal of CO₂ from a carboxylic acid salt, often with soda lime", ["adding CO₂", "adding water", "removing an OH group"], "Sodium ethanoate gives methane."),
      ("Which reagent reduces a carboxylic acid to a primary alcohol?", "LiAlH₄", ["NaBH₄", "H₂/Pd-BaSO₄", "Zn-Hg/HCl"], "NaBH₄ does not reduce acids."),
      ("What is formalin?", "a 40% solution of methanal in water", ["pure ethanal", "a solution of ethanoic acid", "a ketone"], "Used to preserve specimens."),
      ("Which test distinguishes an aldehyde from a ketone?", "Tollens' reagent (silver mirror)", ["the iodoform test", "litmus", "sodium metal"], "Ketones are not oxidised by mild oxidants.")]

G9 = {"a primary (1°) amine": ["methanamine", "ethanamine", "aniline", "propan-1-amine", "benzylamine", "butan-1-amine", "2-methylpropan-2-amine", "p-toluidine", "propan-2-amine"],
      "a secondary (2°) amine": ["N-methylmethanamine", "N-ethylethanamine", "N-methylaniline", "N-methylpropan-1-amine", "N-ethylaniline", "piperidine"],
      "a tertiary (3°) amine": ["N,N-dimethylmethanamine", "N,N-diethylethanamine", "N,N-dimethylaniline", "N-ethyl-N-methylethanamine", "N,N-diethylaniline"],
      "an amide": ["ethanamide", "benzamide", "methanamide", "propanamide"], "a nitro compound": ["nitrobenzene", "nitromethane", "nitroethane", "1-nitropropane", "4-nitrotoluene"],
      "a nitrile": ["ethanenitrile", "benzonitrile", "propanenitrile"], "an isocyanide": ["methyl isocyanide", "phenyl isocyanide", "ethyl isocyanide"],
      "a diazonium salt": ["benzenediazonium chloride", "4-methylbenzenediazonium chloride", "benzenediazonium fluoroborate"]}
fam(G9, ["a primary (1°) amine", "a secondary (2°) amine", "a tertiary (3°) amine"], ["an amide", "a nitro compound", "a nitrile", "an isocyanide", "a diazonium salt"])
R9 = [("Hoffmann bromamide degradation", "an amide + Br₂ + NaOH → a primary amine with one carbon fewer"), ("Gabriel phthalimide synthesis", "making pure primary aliphatic amines"), ("carbylamine reaction", "a primary amine + CHCl₃ + KOH → a foul-smelling isocyanide"),
      ("Hinsberg's test", "telling 1°, 2° and 3° amines apart with benzenesulphonyl chloride"), ("diazotisation", "aniline + NaNO₂ + HCl at 273–278 K → benzenediazonium chloride"), ("coupling reaction", "a diazonium salt + phenol → an orange azo dye"),
      ("Gattermann reaction", "ArN₂⁺ + Cu/HCl → ArCl"), ("reduction of nitrobenzene with Sn/HCl", "making aniline")]
B9 = [("Which is the strongest base in water: NH₃, CH₃NH₂, (CH₃)₂NH or C₆H₅NH₂?", "(CH₃)₂NH", ["C₆H₅NH₂", "NH₃", "CH₃NH₂"], "Alkyl groups and solvation make 2° amines strongest in water."),
      ("Why is aniline a weaker base than ammonia?", "its lone pair is delocalised into the benzene ring", ["it has no nitrogen", "it is a gas", "it is more soluble"], "Resonance reduces electron availability."),
      ("Which amines give the carbylamine test?", "only primary amines", ["only secondary amines", "only tertiary amines", "all amines"], "The isocyanide has a bad smell."),
      ("Why is aniline acetylated before nitration?", "to reduce the strong activating effect of –NH₂ and protect it", ["to make it a gas", "to make it more basic", "to remove the ring"], "Otherwise oxidation and meta products form."),
      ("Why does aniline give much meta-nitroaniline on direct nitration?", "in acid it is protonated to the anilinium ion, a meta director", ["–NH₂ is meta directing", "the ring is deactivated by water", "nitration needs light"], "C₆H₅NH₃⁺."),
      ("Why are diazonium salts of aromatic amines more stable than those of aliphatic amines?", "the positive charge is delocalised over the benzene ring", ["they are colder", "they have no nitrogen", "they are gases"], "Aliphatic ones decompose at once."),
      ("What colour is the azo dye formed from benzenediazonium chloride and phenol?", "orange", ["blue", "green", "colourless"], "p-Hydroxyazobenzene."),
      ("Which product forms when benzenediazonium chloride is warmed with water?", "phenol", ["benzene", "aniline", "chlorobenzene"], "Nitrogen gas is given off."),
      ("Which reagent replaces the diazonium group with hydrogen?", "hypophosphorous acid (H₃PO₂)", ["water", "CuCl", "KI"], "This gives benzene."),
      ("Why do primary amines have higher boiling points than tertiary amines of similar mass?", "primary amines form hydrogen bonds; tertiary amines cannot", ["tertiary amines are ionic", "primary amines are heavier", "tertiary amines are polymers"], "Tertiary amines have no N–H."),
      ("What is the product of Hoffmann bromamide degradation of ethanamide?", "methanamine", ["ethanamine", "ethanoic acid", "propanamine"], "One carbon is lost."),
      ("Which amine does not react with benzenesulphonyl chloride (Hinsberg)?", "a tertiary amine", ["a primary amine", "a secondary amine", "ammonia"], "It has no N–H hydrogen.")]

# =================================================================== 10 biomolecules
G10 = {"a monosaccharide": ["glucose", "fructose", "galactose", "ribose", "deoxyribose", "mannose", "glyceraldehyde"], "a disaccharide": ["sucrose", "maltose", "lactose"], "a polysaccharide": ["starch", "cellulose", "glycogen"],
       "a fat-soluble vitamin": ["vitamin A", "vitamin D", "vitamin E", "vitamin K"], "a water-soluble vitamin": ["vitamin C", "vitamin B₁", "vitamin B₁₂", "vitamin B₆", "vitamin B₂"],
       "an essential amino acid": ["valine", "leucine", "lysine", "phenylalanine", "tryptophan", "methionine", "threonine", "isoleucine"],
       "a non-essential amino acid": ["glycine", "alanine", "glutamic acid", "serine", "aspartic acid", "proline", "cysteine", "tyrosine"],
       "a base found in DNA": ["adenine", "guanine", "cytosine", "thymine"], "found in RNA but not in DNA": ["uracil", "ribose (as the sugar)"],
       "a fibrous protein": ["keratin", "collagen", "myosin", "fibroin (silk)"], "a globular protein": ["insulin", "albumin", "haemoglobin"]}
fam(G10, ["a monosaccharide", "a disaccharide", "a polysaccharide"], ["a fat-soluble vitamin", "a water-soluble vitamin"], ["an essential amino acid", "a non-essential amino acid"], ["a base found in DNA", "found in RNA but not in DNA"], ["a fibrous protein", "a globular protein"])
VIT = [("vitamin A", "xerophthalmia (hardening of the cornea) and night blindness"), ("vitamin B₁ (thiamine)", "beriberi"), ("vitamin B₂ (riboflavin)", "cheilosis (cracked lips)"),
       ("vitamin B₆ (pyridoxine)", "convulsions"), ("vitamin B₁₂", "pernicious anaemia"), ("vitamin C", "scurvy (bleeding gums)"), ("vitamin D", "rickets in children and osteomalacia in adults"),
       ("vitamin E", "fragile red blood cells and muscular weakness"), ("vitamin K", "slow clotting of blood")]
B10 = [("What is the product of hydrolysis of sucrose?", "glucose and fructose", ["glucose only", "galactose and glucose", "maltose"], "The mixture is called invert sugar."),
       ("What is the product of hydrolysis of lactose?", "glucose and galactose", ["glucose and fructose", "two glucose units", "fructose only"], "Lactose is milk sugar."),
       ("What does maltose give on hydrolysis?", "two molecules of α-D-glucose", ["glucose and fructose", "galactose", "sucrose"], "Malt sugar."),
       ("Which sugar is non-reducing?", "sucrose", ["glucose", "maltose", "lactose"], "Both its anomeric carbons are used in the glycosidic link."),
       ("Which polysaccharide is the storage form of glucose in animals?", "glycogen", ["starch", "cellulose", "chitin"], "It is stored in the liver and muscles."),
       ("Which polysaccharide cannot be digested by humans?", "cellulose", ["starch", "glycogen", "maltose"], "We lack the enzyme cellulase."),
       ("What is a zwitterion?", "a dipolar ion with both positive and negative charges, as amino acids are in solution", ["a positive ion", "a negative ion", "a neutral molecule with no charge"], "H₃N⁺–CHR–COO⁻."),
       ("What is the peptide bond?", "the –CO–NH– link between amino acids", ["the –O– link between sugars", "a hydrogen bond", "a phosphodiester link"], "Formed with loss of water."),
       ("What happens when a protein is denatured?", "it loses its higher structure and biological activity, though the primary structure stays", ["it gains amino acids", "it becomes a sugar", "its peptide bonds all break"], "e.g. boiling an egg."),
       ("Which base is found in RNA but not in DNA?", "uracil", ["thymine", "adenine", "guanine"], "DNA has thymine instead."),
       ("What sugar is present in DNA?", "β-D-2-deoxyribose", ["β-D-ribose", "glucose", "fructose"], "RNA has ribose."),
       ("Which vitamin cannot be stored in the body for long?", "water-soluble vitamins such as vitamin C", ["vitamin A", "vitamin D", "vitamin K"], "They are lost in urine."),
       ("What is the secondary structure of a protein?", "the α-helix or β-pleated sheet held by hydrogen bonds", ["the sequence of amino acids", "the joining of subunits", "the overall folding only"], "Primary structure is the sequence."),
       ("What is the open-chain form of glucose shown to have?", "an aldehyde group and five –OH groups", ["a ketone group", "no –OH groups", "a carboxylic acid group"], "It gives a silver mirror with Tollens' reagent.")]


def NM(pat):
    """c_name items whose answer matches pat"""
    import re
    g0 = T(C.c_name)

    def g():
        it = g0()
        return it if it and re.search(pat, re.sub("<[^>]+>", "", it["c"][it["a"]])) else None
    return g


def UNITS():
    b = {k: B(globals()["B%d" % k]) for k in range(1, 11)}
    od = {k: OD(globals()["G%d" % k]) for k in (6, 7, 8, 9, 10)}
    df = OD(DF)
    r = {k: pairs(globals()["R%d" % k], "What happens in this named reaction or test: %s?", "Which named reaction or test is this: %s?") for k in (6, 7, 8, 9)}
    lig = pairs(LIG, "How many donor atoms does the ligand %s use (its denticity)?", None, pool=["tridentate", "tetradentate"])
    con = pairs(CONAME, "What is the IUPAC name of %s?", "Which formula has the IUPAC name %s?")
    vit = pairs(VIT, "Which deficiency disease is caused by a lack of %s?", "Lack of which vitamin causes %s?")
    S = lambda *a, **kw: SU(CH, *a, **kw)
    return [
        S(15, "solutions", 1,
          "Types of solutions, expression of concentration of solutions of solids in liquids, solubility of gases in liquids, solid solutions, Raoult's law, colligative properties – relative lowering of vapour pressure, elevation of boiling point, depression of freezing point, osmotic pressure, determination of molecular masses using colligative properties, abnormal molecular mass, van't Hoff factor.",
          "Solutions", "solutions",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 1 Solutions: concentration terms, Henry's law, Raoult's law, colligative properties, osmotic pressure, molar mass and the van't Hoff factor. 100 questions with answers.",
          "Colligative properties depend only on the number of solute particles.", "ΔT(b) = iK(b)m; ΔT(f) = iK(f)m; π = iCRT.",
          "<p>Concentration may be given as mass per cent, mole fraction, molarity or molality. Henry's law says gas solubility is proportional to its partial pressure. Raoult's law gives the vapour pressure of a component as p = xp°; a non-volatile solute lowers the vapour pressure, and Δp/p° equals its mole fraction.</p>"
          "<p>Colligative properties — relative lowering of vapour pressure, boiling point elevation K<sub>b</sub>m, freezing point depression K<sub>f</sub>m and osmotic pressure CRT — depend only on the number of particles. Electrolytes give more particles, so they are multiplied by the van't Hoff factor i.</p>",
          [("0.1 m glucose in water. ΔTf?", ["1.86 × 0.1"], "0.186 K"), ("i for NaCl?", ["Na⁺ + Cl⁻"], "2")],
          ["Using molarity instead of molality for ΔT.", "Forgetting i for electrolytes.", "Using the mass of solution instead of the solvent."],
          [("What are colligative properties?", "Properties of solutions that depend only on the number of solute particles, such as osmotic pressure and freezing point depression."),
           ("What is the van't Hoff factor?", "The ratio of the actual number of particles in solution to the number of formula units dissolved.")],
          lambda: [("Concentration", [(K(b_conc, "M", "m", "x", "pct"), 15), (b[1], 5)]), ("Raoult's law and vapour pressure", [(K(colli, "raoult", "rel"), 14), (b[1], 2), (K(colli, "henry"), 4)]),
                   ("Boiling point and freezing point", [(K(colli, "Tb", "Tf"), 18), (b[1], 2)]), ("Osmotic pressure", [(K(colli, "pi"), 16), (b[1], 1), (K(colli, "i"), 3)]),
                   ("Molar mass and the van't Hoff factor", [(K(colli, "M"), 14), (K(colli, "Tf"), 6)])]),
        S(16, "electrochemistry", 2,
          "Redox reactions, EMF of a cell, standard electrode potential, Nernst equation and its application to chemical cells, relation between Gibbs energy change and EMF of a cell, conductance in electrolytic solutions, specific and molar conductivity, variations of conductivity with concentration, Kohlrausch's law, electrolysis and law of electrolysis (elementary idea), dry cell – electrolytic cells and Galvanic cells, lead accumulator, fuel cells, corrosion.",
          "Electrochemistry", "electrochemistry",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 2 Electrochemistry: galvanic cells, electrode potentials, the Nernst equation, ΔG = −nFE, conductivity, Kohlrausch's law, Faraday's laws, batteries and corrosion. 100 questions with answers.",
          "E(cell) = E(cathode) − E(anode); ΔG° = −nFE°.", "Nernst: E = E° − (0.059/n) log Q at 298 K.",
          "<p>A galvanic cell turns chemical energy into electricity: oxidation at the anode, reduction at the cathode. E°<sub>cell</sub> = E°<sub>cathode</sub> − E°<sub>anode</sub>; a positive value means ΔG° = −nFE° is negative and the reaction is spontaneous. The Nernst equation corrects E for concentrations.</p>"
          "<p>Conductivity κ falls on dilution, but molar conductivity Λ<sub>m</sub> = κ × 1000/C rises; Kohlrausch's law adds ionic contributions at infinite dilution. In electrolysis the mass deposited is m = MIt/(nF), with F = 96,500 C mol⁻¹.</p>",
          [("E° = 1.10 V, n = 2. ΔG°?", ["−2 × 96,500 × 1.10"], "−212 kJ mol⁻¹"), ("2 A for 965 s, Cu²⁺. Mass?", ["63.5 × 1930 ÷ (2 × 96,500)"], "0.635 g")],
          ["Adding electrode potentials instead of subtracting.", "Forgetting n in ΔG = −nFE.", "Using minutes instead of seconds in Q = It."],
          [("What is the Nernst equation?", "E = E° − (0.059/n) log Q at 298 K; it gives the cell e.m.f. at non-standard concentrations."),
           ("Why does molar conductivity increase on dilution?", "Ions are further apart and move more freely, so each mole of electrolyte carries current better.")],
          lambda: [("Galvanic cells and E°", [(T(C.c_ecell, "E", "neg"), 14), (b[2], 6)]), ("Nernst equation and Gibbs energy", [(K(elc, "nernst", "dG"), 16), (T(C.c_ecell, "feas"), 4)]),
                   ("Conductance", [(K(elc, "lam", "cc"), 16), (b[2], 3), (K(elc, "kohl"), 1)]), ("Kohlrausch's law and electrolysis", [(K(elc, "kohl"), 3), (K(elc, "far", "Q"), 17)]),
                   ("Batteries, corrosion and mixed problems", [(b[2], 3), (K(elc, "far", "nernst", "dG"), 17)])]),
        S(17, "chemical-kinetics", 3,
          "Rate of a reaction (average and instantaneous), factors affecting rate of reaction: concentration, temperature, catalyst; order and molecularity of a reaction, rate law and specific rate constant, integrated rate equations and half-life (only for zero and first order reactions), concept of collision theory (elementary idea, no mathematical treatment), activation energy, Arrhenius equation.",
          "Chemical Kinetics", "chemical kinetics",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 3 Chemical Kinetics: rate of reaction, rate laws, order and molecularity, integrated rate equations, half-life, activation energy and the Arrhenius equation. 100 questions with answers.",
          "First order: t(½) = 0.693/k.", "k = A e^(−Ea/RT).",
          "<p>The rate of reaction is the change in concentration per unit time. The rate law rate = k[A]<sup>x</sup>[B]<sup>y</sup> is found by experiment; x + y is the order. For a first-order reaction k = (2.303/t) log([R]₀/[R]) and t<sub>½</sub> = 0.693/k, independent of concentration; for zero order t<sub>½</sub> = [R]₀/2k.</p>"
          "<p>Molecules react only when they collide with energy above the activation energy and in the right orientation. The Arrhenius equation k = A e<sup>−Ea/RT</sup> explains why rates rise with temperature; catalysts lower E<sub>a</sub>.</p>",
          [("k = 0.0693 s⁻¹. t(½)?", ["0.693 ÷ 0.0693"], "10 s"), ("After 3 half-lives?", ["(½)³"], "0.125")],
          ["Confusing order and molecularity.", "Using 0.693/k for zero order.", "Forgetting that the half-life of first order is independent of concentration."],
          [("What is the difference between order and molecularity?", "Order comes from the experimental rate law and can be zero or fractional; molecularity is the number of particles in an elementary step and is a whole number."),
           ("Why does a catalyst speed up a reaction?", "It provides an alternative path with a lower activation energy.")],
          lambda: [("Rate of reaction", [(K(kin, "avg"), 12), (b[3], 4), (T(C.c_order, "rate"), 4)]), ("Rate laws and order", [(T(C.c_order, "order", "k"), 14), (T(C.c_order, "units"), 4), (b[3], 2)]),
                   ("Integrated rate equations", [(K(kin, "int", "zt12"), 17), (b[3], 3)]), ("Half-life", [(K(kin, "t12", "k12", "frac"), 20)]), ("Temperature and activation energy", [(T(C.c_arr, "k", "ln"), 15), (K(kin, "temp"), 3), (b[3], 2)])]),
        S(18, "the-d-and-f-block-elements", 4,
          "General introduction, electronic configuration, occurrence and characteristics of transition metals, general trends in properties of the first row transition metals – metallic character, ionization enthalpy, oxidation states, ionic radii, colour, catalytic property, magnetic properties, interstitial compounds, alloy formation. Lanthanoids – electronic configuration, oxidation states and lanthanoid contraction and its consequences. Actinoids – electronic configuration, oxidation states and comparison with lanthanoids.",
          "The d- and f-Block Elements", "d- and f-block elements",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 4 The d- and f-Block Elements: transition metal configurations, oxidation states, colour, magnetic moments, catalysts, KMnO₄ and K₂Cr₂O₇, lanthanoids and actinoids. 100 questions with answers.",
          "Spin-only μ = √(n(n + 2)) BM.", "Partly filled d orbitals give colour, paramagnetism and catalysis.",
          "<p>Transition metals have partly filled d orbitals in their atoms or common ions; Zn, Cd and Hg (d¹⁰) are not typical transition elements. Because the (n − 1)d and ns energies are close, they show variable oxidation states. Unpaired d electrons make compounds coloured (d–d transitions) and paramagnetic, with μ = √(n(n + 2)) BM.</p>"
          "<p>Potassium permanganate and dichromate are strong oxidising agents in acid. The lanthanoids (4f) show +3 states and a steady fall in size, the lanthanoid contraction; the actinoids (5f) are radioactive and show more oxidation states.</p>",
          [("Fe²⁺ (3d⁶). Unpaired electrons?", ["high spin"], "4"), ("μ for 3 unpaired electrons?", ["√15"], "3.87 BM")],
          ["Counting 4s electrons in the ion.", "Calling Zn a transition metal.", "Using √n instead of √(n(n + 2))."],
          [("Why are many transition metal compounds coloured?", "Their partly filled d orbitals allow d–d transitions that absorb visible light."),
           ("What is the lanthanoid contraction?", "The gradual decrease in atomic and ionic radii across the lanthanoid series because 4f electrons shield poorly.")],
          lambda: [("Transition metals", [(df, 12), (b[4], 4), (T(C.c_config, "atom"), 4)]), ("Electronic configuration", [(T(C.c_config, "ion", "atom"), 8), (K(dblock, "unp"), 8), (b[4], 2), (df, 2)]),
                   ("Magnetic properties and colour", [(K(dblock, "mu"), 12), (K(dblock, "col"), 6), (b[4], 2)]), ("Oxidation states and compounds", [(T(C.c_tm, "ox"), 12), (b[4], 3), (df, 5)]),
                   ("Lanthanoids and actinoids", [(df, 17), (b[4], 1), (K(dblock, "col"), 2)])]),
        S(19, "coordination-compounds", 5,
          "Coordination compounds – introduction, ligands, coordination number, colour, magnetic properties and shapes, IUPAC nomenclature of mononuclear coordination compounds. Bonding, Werner's theory, VBT and CFT; structure and stereoisomerism, importance of coordination compounds (in qualitative analysis, extraction of metals and biological system).",
          "Coordination Compounds", "coordination compounds",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 5 Coordination Compounds: Werner's theory, ligands and denticity, coordination number, oxidation state, IUPAC names, isomerism, VBT and crystal field theory. 100 questions with answers.",
          "The complex ion is written in square brackets.", "Coordination number = number of donor atoms bound to the metal.",
          "<p>In a coordination compound a central metal ion is bound to ligands that each donate electron pairs. The coordination number counts the donor atoms: [Co(en)₃]³⁺ has 6 because en is bidentate. Werner showed that only ions outside the square brackets are free, so [Co(NH₃)₅Cl]Cl₂ gives 3 ions and 2 mol of AgCl.</p>"
          "<p>IUPAC names list ligands alphabetically before the metal and its oxidation state, with -ate for anions. Complexes show geometrical, optical, linkage and ionisation isomerism. Crystal field theory splits d orbitals into t₂g and e<sub>g</sub>; strong field ligands such as CN⁻ give low-spin complexes.</p>",
          [("[Co(NH₃)₆]Cl₃: ions?", ["1 + 3"], "4"), ("Oxidation state of Fe in [Fe(CN)₆]³⁻?", ["x − 6 = −3"], "+3")],
          ["Counting chloride inside the brackets as free.", "Counting en as one donor atom.", "Forgetting -ate for anionic complexes."],
          [("What is the coordination number?", "The number of ligand donor atoms directly bonded to the central metal."),
           ("What did Werner's theory explain?", "That metals have primary (ionisable) valencies outside the coordination sphere and secondary valencies (coordination number) inside it.")],
          lambda: [("Werner's theory", [(K(coord, "ions", "agcl"), 7), (b[5], 6), (T(C.c_tm, "lig"), 7)]), ("Ligands and coordination number", [(lig, 7), (T(C.c_tm, "cn"), 13)]), ("Oxidation state and naming", [(T(C.c_tm, "ox"), 8), (con, 12)]),
                   ("Isomerism and bonding", [(b[5], 5), (T(C.c_tm, "shape"), 11), (K(dblock, "mu"), 4)]), ("Colour and uses", [(T(C.c_tm, "col"), 15), (con, 3), (T(C.c_tm, "shape"), 2)])]),
        S(20, "haloalkanes-and-haloarenes", 6,
          "Haloalkanes: nomenclature, nature of C–X bond, physical and chemical properties, optical rotation, mechanism of substitution reactions. Haloarenes: nature of C–X bond, substitution reactions (directive influence of halogen in monosubstituted compounds only). Uses and environmental effects of dichloromethane, trichloromethane, tetrachloromethane, iodoform, freons, DDT.",
          "Haloalkanes and Haloarenes", "haloalkanes and haloarenes",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 6 Haloalkanes and Haloarenes: naming and classifying halides, SN1 and SN2, elimination, optical activity, named reactions and environmental effects. 100 questions with answers.",
          "1° halides: S(N)2; 3° halides: S(N)1.", "Aryl halides resist nucleophilic substitution.",
          "<p>Haloalkanes are named as halo-substituted alkanes and classed as 1°, 2° or 3° by the carbon bearing the halogen. Primary halides react mainly by S<sub>N</sub>2 (one step, inversion of configuration); tertiary halides by S<sub>N</sub>1 (via a carbocation, racemisation). Alcoholic KOH causes elimination following Saytzeff's rule.</p>"
          "<p>Aryl halides react slowly in nucleophilic substitution because resonance gives the C–X bond partial double-bond character, but they undergo electrophilic substitution at ortho and para positions. Freons damage the ozone layer and DDT builds up in food chains.</p>",
          [("2-Bromobutane is?", ["Br on a carbon with two C"], "secondary"), ("NaI in acetone with R–Cl?", ["halogen exchange"], "Finkelstein reaction")],
          ["Thinking S<sub>N</sub>2 gives racemisation.", "Saying aryl halides react like alkyl halides.", "Mixing up Wurtz and Wurtz–Fittig."],
          [("Why do tertiary haloalkanes react by S<sub>N</sub>1?", "They form stable tertiary carbocations, and their crowded carbon blocks back-side attack."),
           ("Why are freons harmful?", "In the stratosphere they release chlorine radicals that destroy ozone.")],
          lambda: [("Naming and classifying halides", [(NM("bromo|chloro"), 8), (od[6], 12)]), ("Classes of halides", [(od[6], 16), (b[6], 4)]), ("Substitution and elimination", [(b[6], 5), (od[6], 9), (r[6], 6)]),
                   ("Named reactions", [(r[6], 7), (NM("bromo|chloro"), 8), (od[6], 5)]), ("Haloarenes and uses", [(od[6], 18), (b[6], 2)])]),
        S(21, "alcohols-phenols-and-ethers", 7,
          "Alcohols: nomenclature, methods of preparation, physical and chemical properties (of primary alcohols only), identification of primary, secondary and tertiary alcohols, mechanism of dehydration. Phenols: nomenclature, methods of preparation, physical and chemical properties, acidic nature of phenol, electrophilic substitution reactions, uses of phenols. Ethers: nomenclature, methods of preparation, physical and chemical properties, uses.",
          "Alcohols, Phenols and Ethers", "alcohols, phenols and ethers",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 7 Alcohols, Phenols and Ethers: classifying and naming alcohols, preparation, oxidation, acidity of phenols, named reactions and ethers. 100 questions with answers.",
          "1° alcohol → aldehyde → acid; 2° alcohol → ketone.", "Phenol is more acidic than alcohols.",
          "<p>Alcohols are 1°, 2° or 3° by the carbon bearing –OH; they hydrogen-bond, so they boil higher than ethers and alkanes of similar mass. Primary alcohols oxidise to aldehydes (PCC) and acids; secondary to ketones; tertiary resist oxidation. The Lucas test tells them apart.</p>"
          "<p>Phenols are more acidic than alcohols because the phenoxide ion is resonance-stabilised; –NO₂ groups make them stronger. The –OH group activates the ring for bromination, nitration, the Reimer–Tiemann and Kolbe reactions. Ethers are made by the Williamson synthesis and cleaved by HI.</p>",
          [("Propan-2-ol is?", ["–OH on a C with two C"], "secondary"), ("Phenol + bromine water?", ["tribromination"], "2,4,6-tribromophenol")],
          ["Saying ethanol is more acidic than phenol.", "Oxidising a 3° alcohol to a ketone.", "Breaking the O–aryl bond in anisole with HI."],
          [("Why is phenol more acidic than ethanol?", "The negative charge of the phenoxide ion is delocalised over the benzene ring, stabilising it."),
           ("How does the Lucas test distinguish alcohols?", "Tertiary alcohols turn cloudy at once, secondary in about five minutes, primary not at room temperature.")],
          lambda: [("Classifying and naming", [(od[7], 14), (NM("ol$"), 6)]), ("Preparation and properties of alcohols", [(b[7], 5), (od[7], 9), (r[7], 6)]), ("Phenols", [(od[7], 14), (b[7], 3), (r[7], 3)]),
                   ("Named reactions", [(r[7], 4), (od[7], 14), (NM("ol$"), 2)]), ("Ethers and mixed questions", [(od[7], 18), (b[7], 2)])]),
        S(22, "aldehydes-ketones-and-carboxylic-acids", 8,
          "Aldehydes and ketones: nomenclature, nature of carbonyl group, methods of preparation, physical and chemical properties, mechanism of nucleophilic addition, reactivity of alpha hydrogen in aldehydes, uses. Carboxylic acids: nomenclature, acidic nature, methods of preparation, physical and chemical properties, uses.",
          "Aldehydes, Ketones and Carboxylic Acids", "aldehydes, ketones and carboxylic acids",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 8 Aldehydes, Ketones and Carboxylic Acids: naming carbonyl compounds, nucleophilic addition, tests, aldol and Cannizzaro reactions, acidity and esters. 100 questions with answers.",
          "C=O undergoes nucleophilic addition.", "Aldehydes reduce Tollens' and Fehling's reagents; ketones do not.",
          "<p>Aldehydes and ketones contain the polar C=O group, which undergoes nucleophilic addition (HCN, NaHSO₃, ammonia derivatives). Aldehydes are more reactive than ketones and are oxidised by Tollens' and Fehling's reagents. Compounds with α-hydrogens undergo aldol condensation; those without undergo the Cannizzaro reaction.</p>"
          "<p>Carboxylic acids are acidic because the carboxylate ion is resonance-stabilised; electron-withdrawing groups make them stronger. They form esters with alcohols, are reduced to alcohols by LiAlH₄ and give α-halo acids in the HVZ reaction.</p>",
          [("Ethanal + Tollens'?", ["aldehyde oxidised"], "silver mirror"), ("Strongest: CH₃COOH or Cl₃CCOOH?", ["three Cl"], "Cl₃CCOOH")],
          ["Saying ketones give a silver mirror.", "Using NaBH₄ to reduce acids.", "Giving the Cannizzaro reaction to ethanal."],
          [("Why are aldehydes more reactive than ketones?", "The carbonyl carbon of an aldehyde is less crowded and less shielded by electron-releasing alkyl groups."),
           ("What is the aldol condensation?", "Two molecules of an aldehyde or ketone with α-hydrogens join in dilute alkali to give a β-hydroxy carbonyl compound.")],
          lambda: [("Naming carbonyl compounds", [(od[8], 15), (b[8], 5)]), ("Preparation and named reactions", [(r[8], 12), (od[8], 8)]), ("Tests and reactions", [(r[8], 6), (b[8], 3), (od[8], 11)]),
                   ("Carboxylic acids", [(od[8], 13), (b[8], 1), (T(C.c_ester, "name"), 6)]), ("Esters and mixed questions", [(T(C.c_ester, "name", "from"), 14), (od[8], 6)])]),
        S(23, "amines", 9,
          "Amines: nomenclature, classification, structure, methods of preparation, physical and chemical properties, uses, identification of primary, secondary and tertiary amines. Diazonium salts: preparation, chemical reactions and importance in synthetic organic chemistry.",
          "Amines", "amines",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 9 Amines: classifying and naming amines, preparation, basic strength, tests for amines, diazonium salts and coupling reactions. 100 questions with answers.",
          "Amines are bases because of the lone pair on nitrogen.", "Aniline + HNO₂ at 273–278 K → diazonium salt.",
          "<p>Amines are derivatives of ammonia, classed as 1°, 2° or 3° by the number of carbon groups on nitrogen. They are made by reducing nitro compounds, Gabriel synthesis and Hoffmann bromamide degradation. Alkylamines are stronger bases than ammonia; aniline is weaker because its lone pair is delocalised into the ring.</p>"
          "<p>Primary amines give the carbylamine test; Hinsberg's reagent separates the three classes. Aniline forms benzenediazonium chloride at 273–278 K, which can be replaced by –Cl, –Br, –CN, –OH or –H, or coupled with phenol to give azo dyes.</p>",
          [("(CH₃)₂NH is?", ["two C on N"], "secondary amine"), ("Ethanamide + Br₂/NaOH?", ["one C fewer"], "methanamine")],
          ["Saying aniline is a stronger base than ammonia.", "Giving the carbylamine test to secondary amines.", "Calling an amide an amine."],
          [("Why is aniline a weaker base than methanamine?", "Its nitrogen lone pair is delocalised into the benzene ring, so it is less available to accept a proton."),
           ("What is a diazonium salt used for?", "Making many aromatic compounds by replacing –N₂⁺, and making azo dyes by coupling.")],
          lambda: [("Classifying amines", [(od[9], 16), (b[9], 4)]), ("Preparation", [(r[9], 8), (od[9], 12)]), ("Basic strength", [(b[9], 4), (od[9], 16)]), ("Tests and diazonium salts", [(r[9], 5), (od[9], 15)]),
                   ("Mixed questions", [(od[9], 19), (b[9], 1)])]),
        S(24, "biomolecules", 10,
          "Carbohydrates – classification (aldoses and ketoses), monosaccharides (glucose and fructose), D-L configuration, oligosaccharides (sucrose, lactose, maltose), polysaccharides (starch, cellulose, glycogen); importance of carbohydrates. Proteins – elementary idea of amino acids, peptide bond, polypeptides, proteins, structure of proteins – primary, secondary, tertiary structure and quaternary structures (qualitative idea only), denaturation of proteins. Nucleic acids: DNA and RNA. Vitamins – classification and functions.",
          "Biomolecules", "biomolecules",
          "Free CBSE Class 12 Chemistry worksheets for NCERT Chapter 10 Biomolecules: carbohydrates, glucose and sugars, amino acids and proteins, protein structure, nucleic acids and vitamins. 100 questions with answers.",
          "Carbohydrates, proteins, nucleic acids and vitamins are the molecules of life.", "Sucrose → glucose + fructose; lactose → glucose + galactose.",
          "<p>Carbohydrates are monosaccharides (glucose, fructose), disaccharides (sucrose, maltose, lactose) or polysaccharides (starch, cellulose, glycogen). Sucrose is non-reducing; glucose has an aldehyde group and five –OH groups.</p>"
          "<p>Proteins are polymers of amino acids joined by peptide bonds; they have primary, secondary (α-helix, β-sheet), tertiary and quaternary structure and are denatured by heat. Nucleic acids are DNA (deoxyribose, thymine) and RNA (ribose, uracil). Vitamins are fat-soluble (A, D, E, K) or water-soluble (B group, C); lack of each causes a deficiency disease.</p>",
          [("Hydrolysis of lactose?", ["milk sugar"], "glucose + galactose"), ("Lack of vitamin C?", ["bleeding gums"], "scurvy")],
          ["Calling sucrose a reducing sugar.", "Saying DNA contains uracil.", "Mixing up fat- and water-soluble vitamins."],
          [("Why is sucrose a non-reducing sugar?", "Its glycosidic bond joins the reducing carbons of glucose and fructose, so no free aldehyde or ketone group remains."),
           ("What happens when a protein is denatured?", "Its secondary and tertiary structures unfold and it loses its activity, though the peptide bonds remain.")],
          lambda: [("Carbohydrates", [(od[10], 14), (b[10], 6)]), ("Sugars and their reactions", [(od[10], 16), (b[10], 4)]), ("Proteins", [(od[10], 18), (b[10], 1), (vit, 1)]),
                   ("Nucleic acids and vitamins", [(vit, 12), (od[10], 8)]), ("Mixed questions", [(od[10], 19), (vit, 1)])]),
    ]
