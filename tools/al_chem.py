# -*- coding: utf-8 -*-
"""
UK A level Chemistry question makers (Year 12 = AS content, Year 13 = the rest). Units are listed in UNITS(year).
Relative atomic masses to one decimal place as on the A level periodic table; R = 8.31 J mol⁻¹ K⁻¹; Kw = 1.00 × 10⁻¹⁴ mol² dm⁻⁶.
Enthalpy, entropy and electrode potential data are standard textbook values.
Wrong answers come from real mistakes: forgetting to change cm³ into dm³, using kJ with J K⁻¹, filling 4s after 3d in ions,
counting from the wrong end of a chain, subtracting reactants from products the wrong way round, missing the 5:1 ratio.
"""
import math
import random
import re
from fractions import Fraction as F
from uk_alsci import nf, nq, tq, once_maker, U

R = random.Random(0)
RG = 8.31
AR = {"H": 1.0, "C": 12.0, "N": 14.0, "O": 16.0, "F": 19.0, "Na": 23.0, "Mg": 24.3, "Al": 27.0, "Si": 28.1, "P": 31.0, "S": 32.1, "Cl": 35.5,
      "K": 39.1, "Ca": 40.1, "Mn": 54.9, "Fe": 55.8, "Cu": 63.5, "Zn": 65.4, "Br": 79.9, "Ag": 107.9, "I": 126.9, "Ba": 137.3, "Li": 6.9}
SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def ch(xs):
    return R.choice(xs)


def K(f, *kinds):
    g = lambda: f(R.choice(kinds))
    g.__name__ = f.__name__ + "_" + "_".join(kinds)
    return g


def fm(f):
    """C2H5OH -> C<sub>2</sub>H<sub>5</sub>OH ; charges written as ^2- -> superscript"""
    if "^" in f:
        f, c = f.split("^")
        c = "<sup>%s</sup>" % c.replace("-", "−")
    else:
        c = ""
    return re.sub(r"(?<=[A-Za-z\)\]])(\d+)", r"<sub>\1</sub>", f) + c


def parse(f):
    out = {}

    def rec(s, mult):
        i = 0
        while i < len(s):
            if s[i] == "(":
                j, d = i, 0
                while True:
                    d += {"(": 1, ")": -1}.get(s[j], 0)
                    if d == 0:
                        break
                    j += 1
                m = re.match(r"\d+", s[j + 1:])
                n = int(m.group()) if m else 1
                rec(s[i + 1:j], mult * n)
                i = j + 1 + (len(m.group()) if m else 0)
                continue
            m = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
            out[m.group(1)] = out.get(m.group(1), 0) + mult * (int(m.group(2)) if m.group(2) else 1)
            i += len(m.group())
    rec(f.split("^")[0].replace("·", ""), 1)
    return out


def mr(f):
    return sum(AR[e] * n for e, n in parse(f).items())


# =================================================================== Year 12: atomic structure and amount of substance
ELEMS = [(1, "H"), (3, "Li"), (5, "B"), (6, "C"), (7, "N"), (8, "O"), (9, "F"), (11, "Na"), (12, "Mg"), (13, "Al"), (14, "Si"), (15, "P"), (16, "S"),
         (17, "Cl"), (19, "K"), (20, "Ca"), (21, "Sc"), (22, "Ti"), (23, "V"), (24, "Cr"), (25, "Mn"), (26, "Fe"), (27, "Co"), (28, "Ni"), (29, "Cu"),
         (30, "Zn"), (31, "Ga"), (33, "As"), (34, "Se"), (35, "Br")]
ORDER = [("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6), ("4s", 2), ("3d", 10), ("4p", 6)]
SHOW = ["1s", "2s", "2p", "3s", "3p", "3d", "4s", "4p"]


def fill(z):
    d = {}
    left = z
    for s, cap in ORDER:
        if left <= 0:
            break
        d[s] = min(cap, left)
        left -= d[s]
    if z == 24:
        d["3d"], d["4s"] = 5, 1
    if z == 29:
        d["3d"], d["4s"] = 10, 1
    return d


def cfg(d):
    return " ".join("%s%s" % (s, str(d[s]).translate(SUP)) for s in SHOW if d.get(s))


def c_config(k=None):
    z, s = ch(ELEMS)
    k = k or ch(["atom", "atom", "ion", "count"])
    d = fill(z)
    if k == "count":
        sub = ch([x for x in d if d[x] and x[1] in "pd"] or ["1s"])
        tot = sum(v for kk, v in d.items() if kk[1] == sub[1])
        return nq("How many electrons are in %s orbitals altogether in an atom of %s (Z = %d)?" % (sub[1], s, z), tot, [d[sub], tot + 2, z - tot], "",
                  "Configuration %s: add every %s sub-shell to get <b>%d</b>." % (cfg(d), sub[1], tot))
    if k == "ion":
        tm = [(24, "Cr", 3), (25, "Mn", 2), (26, "Fe", 2), (26, "Fe", 3), (27, "Co", 2), (28, "Ni", 2), (29, "Cu", 2), (29, "Cu", 1), (30, "Zn", 2), (22, "Ti", 3), (23, "V", 3), (21, "Sc", 3)]
        z, s, c = ch(tm)
        d = fill(z)
        good = dict(d)
        n = c
        take = min(n, good.get("4s", 0))
        good["4s"] -= take
        good["3d"] = good.get("3d", 0) - (n - take)
        bad = fill(z - c)
        bad2 = dict(d)
        bad2["3d"] -= min(c, bad2["3d"])
        r = "[Ar] " + cfg({k2: v for k2, v in good.items() if k2 in ("3d", "4s")})
        wr = ["[Ar] " + cfg({k2: v for k2, v in bad.items() if k2 in ("3d", "4s")}), "[Ar] " + cfg({k2: v for k2, v in bad2.items() if k2 in ("3d", "4s")}),
              "[Ar] " + cfg({"3d": good.get("3d", 0) + 1, "4s": 0}) if good.get("3d", 0) < 10 else "[Ar] 3d⁹ 4s¹"]
        return tq("What is the electron configuration of %s<sup>%d+</sup>?" % (s, c), r.strip(), [w.strip() for w in wr],
                  "Transition metals lose their 4s electrons first, then 3d. %s is [Ar] %s." % (s, cfg({k2: v for k2, v in d.items() if k2 in ("3d", "4s")})))
    r = cfg(d)
    wr = []
    if z in (24, 29):
        dd = fill(z)
        dd["4s"], dd["3d"] = 2, dd["3d"] - 1
        wr.append(cfg(dd))
    w1 = fill(z + 1)
    w2 = fill(z - 1) if z > 2 else fill(z + 2)
    wr += [cfg(w1), cfg(w2)]
    if "3d" in d and z not in (24, 29):
        dd = dict(d)
        dd["3d"] += dd.get("4s", 0)
        dd["4s"] = 0
        wr.append(cfg(dd))
    if d.get("2p") and len(wr) < 3:
        dd = dict(d)
        dd["2s"], dd["2p"] = d["2s"] - 1, d["2p"] + 1
        wr.append(cfg(dd))
    return tq("What is the electron configuration of %s (Z = %d)?" % (s, z), r, wr, "Fill 1s 2s 2p 3s 3p 4s 3d in order%s." % (" (chromium and copper take one 4s electron into 3d)" if z in (24, 29) else ""))


ISOS = [("chlorine", 35, 75.8, 37), ("copper", 63, 69.2, 65), ("boron", 10, 19.9, 11), ("bromine", 79, 50.7, 81), ("lithium", 6, 7.6, 7),
        ("gallium", 69, 60.1, 71), ("rubidium", 85, 72.2, 87), ("silver", 107, 51.8, 109), ("antimony", 121, 57.2, 123), ("iridium", 191, 37.3, 193)]


def c_ram(k=None):
    el, m1, p1, m2 = ch(ISOS)
    if R.random() < 0.5:
        p1 = ch([10, 20, 25, 30, 40, 60, 70, 75, 80, 90]) * 1.0
        el = "a sample of " + el
    ar = (m1 * p1 + m2 * (100 - p1)) / 100
    return nq("A mass spectrum of %s shows %d with abundance %s%% and %d with abundance %s%%. Calculate the relative atomic mass." % (el, m1, nf(p1, 3), m2, nf(100 - p1, 3)), ar,
              [(m1 + m2) / 2, (m1 * (100 - p1) + m2 * p1) / 100, m1 * p1 / 100 + m2], "",
              "A<sub>r</sub> = (%d × %s + %d × %s) ÷ 100 = <b>%s</b>." % (m1, nf(p1, 3), m2, nf(100 - p1, 3), nf(ar)), sf=4)


SUBS = ["NaCl", "NaOH", "CaCO3", "MgO", "H2SO4", "HCl", "CuSO4", "KMnO4", "Na2CO3", "CO2", "NH3", "C2H5OH", "C6H12O6", "CH4", "C3H8", "Al2O3", "Fe2O3",
        "MgCl2", "CaCl2", "KBr", "NaHCO3", "Ca(OH)2", "Mg(OH)2", "C4H10", "CH3COOH", "ZnO", "BaCl2", "AgNO3", "K2CO3", "Li2O"]


def c_moles(k=None):
    f = ch(SUBS)
    M = mr(f)
    k = k or ch(["n", "m", "N", "Mr"])
    if k == "Mr":
        return nq("Calculate the relative formula mass of %s." % fm(f), M, [M + 16, M - 1, sum(AR[e] for e in parse(f))], "", "Add the relative atomic masses: <b>%s</b>." % nf(M, 4), sf=4)
    mass = ch([0.5, 1.2, 2.0, 2.5, 4.0, 5.0, 8.0, 10.0, 12.5, 25.0, 50.0])
    n = mass / M
    if k == "n":
        return nq("How many moles are in %s g of %s?" % (nf(mass), fm(f)), n, [M / mass, mass * M, mass / (M + 2)], " mol", "n = m/M = %s ÷ %s = <b>%s mol</b>." % (nf(mass), nf(M, 4), nf(n)))
    if k == "m":
        nn = ch([0.010, 0.025, 0.050, 0.10, 0.15, 0.20, 0.25, 0.50, 1.5, 2.5])
        return nq("Calculate the mass of %s mol of %s." % (nf(nn, 2), fm(f)), nn * M, [nn / M, M / nn, nn * (M - 1)], " g", "m = nM = %s × %s = <b>%s g</b>." % (nf(nn, 2), nf(M, 4), nf(nn * M)))
    return nq("How many molecules or formula units are in %s g of %s? (L = 6.02 × 10<sup>23</sup> mol⁻¹)" % (nf(mass), fm(f)), n * 6.02e23, [mass * 6.02e23, n / 6.02e23, M * 6.02e23], "",
              "n = %s mol; N = nL = <b>%s</b>." % (nf(n), nf(n * 6.02e23)))


def c_conc(k=None):
    k = k or ch(["n", "c", "V", "mass", "dil"])
    c, V = ch([0.050, 0.10, 0.15, 0.20, 0.25, 0.50, 1.0, 2.0]), ch([10.0, 20.0, 25.0, 50.0, 100.0, 250.0, 500.0])
    n = c * V / 1000
    if k == "n":
        return nq("How many moles of solute are in %s cm³ of a %s mol dm⁻³ solution?" % (nf(V), nf(c, 2)), n, [c * V, c / V, V / c / 1000], " mol", "n = c × V = %s × (%s ÷ 1000) = <b>%s mol</b>." % (nf(c, 2), nf(V), nf(n)))
    if k == "c":
        return nq("%s mol of solute is dissolved to make %s cm³ of solution. Calculate the concentration." % (nf(n), nf(V)), c, [n / V, n * V, n * 1000], " mol dm⁻³", "c = n/V = %s ÷ %s dm³ = <b>%s mol dm⁻³</b>." % (nf(n), nf(V / 1000), nf(c)))
    if k == "V":
        return nq("What volume of %s mol dm⁻³ solution contains %s mol of solute?" % (nf(c, 2), nf(n)), V, [n / c, n * c * 1000, c / n], " cm³", "V = n/c = %s dm³ = <b>%s cm³</b>." % (nf(n / c), nf(V)))
    if k == "mass":
        f = ch(["NaOH", "NaCl", "CuSO4", "Na2CO3", "KMnO4", "HCl", "KBr", "AgNO3"])
        M = mr(f)
        return nq("Calculate the mass of %s needed to make %s cm³ of a %s mol dm⁻³ solution." % (fm(f), nf(V), nf(c, 2)), n * M, [c * V * M, c * M, n / M], " g",
                  "n = %s mol; m = n × M = %s × %s = <b>%s g</b>." % (nf(n), nf(n), nf(M, 4), nf(n * M)))
    V2 = V * ch([2, 4, 5, 10])
    return nq("%s cm³ of a %s mol dm⁻³ solution is diluted to %s cm³. Calculate the new concentration." % (nf(V), nf(c, 2), nf(V2)), c * V / V2, [c * V2 / V, c, c - V / V2], " mol dm⁻³",
              "c₁V₁ = c₂V₂: %s × %s ÷ %s = <b>%s mol dm⁻³</b>." % (nf(c, 2), nf(V), nf(V2), nf(c * V / V2)))


def c_gas(k=None):
    k = k or ch(["V", "n", "p", "Mr"])
    n, T = ch([0.010, 0.020, 0.050, 0.10, 0.25, 0.50, 1.0]), ch([273, 293, 298, 300, 350, 373, 400])
    p = ch([100, 101, 120, 150, 200, 250]) * 1000.0
    V = n * RG * T / p
    if k == "V":
        return nq("Calculate the volume, in cm³, occupied by %s mol of gas at %s kPa and %d K." % (nf(n, 2), nf(p / 1000), T), V * 1e6, [V, n * RG * T / (p / 1000), n * RG * (T - 273) / p * 1e6 if T > 273 else V * 1e3], " cm³",
                  "V = nRT/p = %s m³ = <b>%s cm³</b>." % (nf(V), nf(V * 1e6)))
    if k == "n":
        return nq("A gas occupies %s cm³ at %s kPa and %d K. How many moles are there?" % (nf(V * 1e6), nf(p / 1000), T), n, [p * V * 1e6 / (RG * T), p / 1000 * V / (RG * T), p * V * RG / T], " mol",
                  "Convert: V = %s m³, p = %s Pa. n = pV/(RT) = <b>%s mol</b>." % (nf(V), nf(p), nf(n)))
    if k == "p":
        return nq("%s mol of gas is in a %s cm³ container at %d K. Calculate the pressure in kPa." % (nf(n, 2), nf(V * 1e6), T), p / 1000, [n * RG * T / (V * 1e6), p, n * RG * T / V / 1e6], " kPa",
                  "p = nRT/V with V = %s m³: %s Pa = <b>%s kPa</b>." % (nf(V), nf(p), nf(p / 1000)))
    f = ch(["CO2", "CH4", "O2", "N2", "C3H8", "C2H6", "NH3", "SO2", "C4H10"])
    M = mr(f)
    m = n * M
    return nq("%s g of a gas occupies %s cm³ at %s kPa and %d K. Calculate its relative molecular mass." % (nf(m), nf(V * 1e6), nf(p / 1000), T), M, [m / (p * V * 1e6 / (RG * T)), n, m * n], "",
              "n = pV/(RT) = %s mol; M<sub>r</sub> = m/n = <b>%s</b> (%s)." % (nf(n), nf(M), fm(f)))


EMP = [("CH2", {"C": 85.7, "H": 14.3}), ("CH4", {"C": 75.0, "H": 25.0}), ("CH2O", {"C": 40.0, "H": 6.7, "O": 53.3}), ("C2H6O", {"C": 52.2, "H": 13.0, "O": 34.8}),
       ("MgO", {"Mg": 60.3, "O": 39.7}), ("Fe2O3", {"Fe": 69.9, "O": 30.1}), ("Na2SO4", {"Na": 32.4, "S": 22.6, "O": 45.0}), ("C3H8", {"C": 81.8, "H": 18.2}),
       ("CH2Cl", {"C": 24.3, "H": 4.0, "Cl": 71.7}), ("NO2", {"N": 30.4, "O": 69.6}), ("P2O5", {"P": 43.7, "O": 56.3}), ("C2H4O", {"C": 54.5, "H": 9.1, "O": 36.4}),
       ("CaC2O4", {"Ca": 31.3, "C": 18.8, "O": 50.0}), ("SO3", {"S": 40.1, "O": 59.9}), ("C2H5", {"C": 82.8, "H": 17.2}), ("Al2O3", {"Al": 52.9, "O": 47.1})]


def c_emp(k=None):
    f, pc = ch(EMP)
    k = k or ch(["emp", "mol"])
    if k == "mol":
        mult = ch([2, 3, 4])
        if f in ("CH4", "MgO", "Fe2O3", "Na2SO4", "C3H8", "P2O5", "CaC2O4", "SO3", "Al2O3", "NO2"):
            return None
        Mm = mr(f) * mult
        mol = "".join("%s%s" % (e, (n * mult) if n * mult > 1 else "") for e, n in parse(f).items())
        wr = ["".join("%s%s" % (e, (n * (mult + 1)) if n * (mult + 1) > 1 else "") for e, n in parse(f).items()), f,
              "".join("%s%s" % (e, (n * mult + 1)) for e, n in parse(f).items())]
        return tq("A compound has the empirical formula %s and M<sub>r</sub> = %s. What is its molecular formula?" % (fm(f), nf(Mm)), fm(mol), [fm(w) for w in wr],
                  "M<sub>r</sub> of %s = %s; %s ÷ %s = %d, so multiply by %d." % (fm(f), nf(mr(f)), nf(Mm), nf(mr(f)), mult, mult))
    wr = []
    els = list(pc)
    tot = parse(f)
    wr.append("".join("%s%s" % (e, int(round(pc[e])) if False else "") for e in els))
    wr = ["".join("%s%s" % (e, "" if n == 1 else n) for e, n in ((e, tot[e] + (1 if i == 0 else 0)) for i, e in enumerate(els))),
          "".join("%s%s" % (e, "" if n == 1 else n) for e, n in ((e, tot[e] + (1 if i == len(els) - 1 else 0)) for i, e in enumerate(els))),
          "".join("%s%s" % (e, "" if n == 1 else n) for e, n in ((e, max(1, tot[e] * 2 - (1 if i == 0 else 0))) for i, e in enumerate(els)))]
    data = ", ".join("%s %s%%" % (e, nf(pc[e], 3)) for e in els)
    return tq("A compound contains %s by mass. What is its empirical formula?" % data, fm(f), [fm(w) for w in wr],
              "Divide each %% by A<sub>r</sub>, then divide by the smallest: %s." % ", ".join("%s %s" % (e, nf(pc[e] / AR[e])) for e in els))


YLD = [("CaCO3 → CaO + CO2", "CaCO3", 1, "CaO", 1, ["CaCO3"], ["CaO", "CO2"]), ("2Mg + O2 → 2MgO", "Mg", 2, "MgO", 2, ["Mg", "O2"], ["MgO"]),
       ("C2H4 + H2O → C2H5OH", "C2H4", 1, "C2H5OH", 1, ["C2H4", "H2O"], ["C2H5OH"]), ("N2 + 3H2 → 2NH3", "N2", 1, "NH3", 2, ["N2", "H2", "H2", "H2"], ["NH3", "NH3"]),
       ("Fe2O3 + 3CO → 2Fe + 3CO2", "Fe2O3", 1, "Fe", 2, ["Fe2O3", "CO", "CO", "CO"], ["Fe", "Fe", "CO2", "CO2", "CO2"]),
       ("C6H12O6 → 2C2H5OH + 2CO2", "C6H12O6", 1, "C2H5OH", 2, ["C6H12O6"], ["C2H5OH", "C2H5OH", "CO2", "CO2"]),
       ("CH4 + Cl2 → CH3Cl + HCl", "CH4", 1, "CH3Cl", 1, ["CH4", "Cl2"], ["CH3Cl", "HCl"]), ("2NaHCO3 → Na2CO3 + H2O + CO2", "NaHCO3", 2, "Na2CO3", 1, ["NaHCO3", "NaHCO3"], ["Na2CO3", "H2O", "CO2"])]


def c_yield(k=None):
    eq, a, na, b, nb, rs, ps = ch(YLD)
    k = k or ch(["yield", "ae", "theo"])
    AR.setdefault("Cl", 35.5)
    if k == "ae":
        want = sum(mr(p) for p in ps if p == b)
        tot = sum(mr(r) for r in rs)
        ae = want / tot * 100
        return nq("Calculate the percentage atom economy for making %s by this reaction: %s." % (fm(b), fm(eq)), ae, [mr(b) / tot * 100, 100 - ae, want / sum(mr(p) for p in ps) * 90], "%",
                  "Atom economy = M<sub>r</sub> of desired product ÷ total M<sub>r</sub> of reactants × 100 = %s ÷ %s × 100 = <b>%s%%</b>." % (nf(want, 4), nf(tot, 4), nf(ae)))
    ma = ch([5.0, 10.0, 12.0, 20.0, 25.0, 50.0, 100.0])
    theo = ma / mr(a) * nb / na * mr(b)
    if k == "theo":
        return nq("%s g of %s reacts completely: %s. Calculate the maximum (theoretical) mass of %s." % (nf(ma), fm(a), fm(eq), fm(b)), theo, [ma / mr(a) * mr(b), ma * mr(b) / mr(a) * na / nb, ma * nb / na], " g",
                  "n(%s) = %s mol, n(%s) = %s mol, m = <b>%s g</b>." % (fm(a), nf(ma / mr(a)), fm(b), nf(ma / mr(a) * nb / na), nf(theo)))
    act = theo * ch([0.45, 0.6, 0.72, 0.8, 0.85, 0.9, 0.95])
    y = act / theo * 100
    return nq("%s g of %s gave %s g of %s (%s). Calculate the percentage yield." % (nf(ma), fm(a), nf(act), fm(b), fm(eq)), y, [act / ma * 100, theo / act * 100, act / (ma / mr(a) * mr(b)) * 100], "%",
              "Theoretical mass = %s g; yield = %s ÷ %s × 100 = <b>%s%%</b>." % (nf(theo), nf(act), nf(theo), nf(y)))


def c_titr(k=None):
    acid, base, ratio = ch([("HCl", "NaOH", 1), ("HNO3", "KOH", 1), ("H2SO4", "NaOH", 2), ("H2SO4", "KOH", 2), ("HCl", "Na2CO3", F(1, 2)), ("CH3COOH", "NaOH", 1)])
    cb, Vb = ch([0.050, 0.080, 0.10, 0.12, 0.15, 0.20]), ch([20.0, 25.0])
    Va = ch([12.5, 15.2, 18.6, 21.4, 22.8, 23.5, 24.1, 26.3, 28.9])
    nb = cb * Vb / 1000
    na = nb / float(ratio)
    ca = na / (Va / 1000)
    return nq("%s cm³ of %s mol dm⁻³ %s was neutralised by %s cm³ of %s. Calculate the concentration of the %s." % (nf(Vb), nf(cb, 2), fm(base), nf(Va), fm(acid), fm(acid)), ca,
              [nb / (Va / 1000), cb * Va / Vb, na / Va], " mol dm⁻³",
              "n(%s) = %s mol; ratio acid : base = 1 : %s, so n(%s) = %s mol; c = n/V = <b>%s mol dm⁻³</b>." % (fm(base), nf(nb), str(ratio), fm(acid), nf(na), nf(ca)))


# =================================================================== Year 12: bonding and energetics
SHAPES = [("CH4", 4, 0, "tetrahedral", "109.5°"), ("NH3", 3, 1, "pyramidal", "107°"), ("H2O", 2, 2, "bent (non-linear)", "104.5°"), ("CO2", 2, 0, "linear", "180°"),
          ("BF3", 3, 0, "trigonal planar", "120°"), ("SF6", 6, 0, "octahedral", "90°"), ("PCl5", 5, 0, "trigonal bipyramidal", "90° and 120°"), ("NH4^+", 4, 0, "tetrahedral", "109.5°"),
          ("XeF4", 4, 2, "square planar", "90°"), ("BeCl2", 2, 0, "linear", "180°"), ("PH3", 3, 1, "pyramidal", "107°"), ("H3O^+", 3, 1, "pyramidal", "107°"),
          ("AlCl3", 3, 0, "trigonal planar", "120°"), ("SiCl4", 4, 0, "tetrahedral", "109.5°"), ("H2S", 2, 2, "bent (non-linear)", "104.5°"), ("ClF3", 3, 2, "T-shaped", "87.5°"),
          ("NH2^-", 2, 2, "bent (non-linear)", "104.5°"), ("SF4", 4, 1, "seesaw", "about 102° and 173°"), ("BH4^-", 4, 0, "tetrahedral", "109.5°"), ("CCl4", 4, 0, "tetrahedral", "109.5°")]
ALLSH = sorted({s[3] for s in SHAPES})
ALLANG = sorted({s[4] for s in SHAPES})


def c_shape(k=None):
    f, bp, lp, sh, ang = ch(SHAPES)
    k = k or ch(["shape", "angle", "lp"])
    if k == "shape":
        return tq("What is the shape of %s?" % fm(f), sh, R.sample([x for x in ALLSH if x != sh], 4), "%d bonding pairs and %d lone pair%s around the central atom: <b>%s</b>." % (bp, lp, "" if lp == 1 else "s", sh))
    if k == "angle":
        if sh in ("seesaw", "T-shaped"):
            return None
        return tq("What is the bond angle in %s?" % fm(f), ang, R.sample([x for x in ALLANG if x != ang and "about" not in x], 4),
                  "%d bonding pairs, %d lone pairs. Lone pairs repel more than bonding pairs, so each lone pair closes the angle by about 2.5°." % (bp, lp))
    return nq("How many lone pairs of electrons are on the central atom in %s?" % fm(f), lp, [bp, lp + 1, abs(bp - lp) + (1 if bp == lp else 0)], "", "%s: %d bonding pairs and <b>%d</b> lone pairs." % (fm(f), bp, lp))


BOND = [("What type of bonding is in sodium chloride?", "ionic", ["covalent", "metallic", "hydrogen bonding"], "Electrostatic attraction between oppositely charged ions."),
        ("Why does diamond have a very high melting point?", "many strong covalent bonds must be broken", ["it has strong intermolecular forces", "it has ionic bonds", "it has delocalised electrons"], "Diamond is a giant covalent (macromolecular) structure."),
        ("Why does graphite conduct electricity?", "it has delocalised electrons between the layers", ["it has free ions", "it has hydrogen bonds", "its layers are held by covalent bonds"], "Each carbon uses three electrons in bonds; the fourth is delocalised."),
        ("Which substance has hydrogen bonding between its molecules?", "NH₃", ["CH₄", "HCl", "H₂S"], "Hydrogen bonding needs H bonded to N, O or F."),
        ("Why does water have a higher boiling point than H₂S?", "water molecules form hydrogen bonds", ["H₂S has fewer electrons", "water has covalent bonds", "H₂S is ionic"], "Hydrogen bonds are stronger than the other intermolecular forces in H₂S."),
        ("What is electronegativity?", "the power of an atom to attract the pair of electrons in a covalent bond", ["the energy to remove an electron", "the charge on an ion", "the number of bonds an atom forms"], "Fluorine is the most electronegative element."),
        ("Which molecule is polar?", "HCl", ["CO₂", "CCl₄", "BF₃"], "CO₂, CCl₄ and BF₃ are symmetrical, so the dipoles cancel."),
        ("Which molecule has polar bonds but is non-polar overall?", "CO₂", ["H₂O", "NH₃", "HF"], "CO₂ is linear, so the two C=O dipoles cancel."),
        ("Why do the boiling points of the noble gases increase down the group?", "there are more electrons, so van der Waals forces are stronger", ["the atoms form covalent bonds", "hydrogen bonding increases", "the nuclear charge decreases"], "Bigger atoms have bigger induced dipole–dipole forces."),
        ("What is a co-ordinate (dative covalent) bond?", "a shared pair of electrons where both electrons come from one atom", ["a bond between two ions", "a bond with three shared pairs", "a hydrogen bond"], "For example the bond from N to H⁺ in NH₄⁺."),
        ("Why can metals be hammered into shape?", "layers of positive ions can slide over each other", ["the electrons are fixed in place", "the bonds are weak", "they contain molecules"], "The delocalised electrons hold the ions together as layers slide."),
        ("Why does magnesium have a higher melting point than sodium?", "Mg²⁺ has a larger charge and there are more delocalised electrons", ["Mg atoms are larger", "Mg is covalent", "Na forms hydrogen bonds"], "Stronger metallic bonding."),
        ("Which substance conducts electricity when molten but not when solid?", "sodium chloride", ["copper", "graphite", "iodine"], "Ions are fixed in the solid but free to move when molten."),
        ("What kind of structure does iodine have?", "simple molecular", ["giant covalent", "giant ionic", "metallic"], "Weak van der Waals forces between I₂ molecules, so it sublimes easily."),
        ("What is the strongest type of intermolecular force?", "hydrogen bonding", ["permanent dipole–dipole forces", "van der Waals forces", "covalent bonding"], "Covalent bonds are within molecules, not between them."),
        ("Which change makes a molecule's van der Waals forces stronger?", "a longer chain with more electrons", ["more branching", "fewer electrons", "a lower boiling point"], "Straight long chains have more surface contact."),
        ("Why does ice float on water?", "hydrogen bonds hold the molecules in an open lattice", ["ice contains air", "ice has covalent bonds between molecules", "water is non-polar"], "Ice is less dense than liquid water.")]


def c_calor(k=None):
    fuel = ch([("methanol", "CH3OH", 32.0), ("ethanol", "C2H5OH", 46.0), ("propan-1-ol", "C3H7OH", 60.0), ("butan-1-ol", "C4H9OH", 74.0), ("hexane", "C6H14", 86.0)])
    k = k or ch(["comb", "neut"])
    if k == "neut":
        V, c = ch([25.0, 50.0]), ch([1.0, 2.0])
        dT = ch([6.4, 6.8, 13.2, 13.6, 6.5, 13.4])
        if (c == 1.0) != (dT < 10):
            return None
        q = 2 * V * 4.18 * dT
        n = c * V / 1000
        dH = -q / n / 1000
        return nq("%s cm³ of %s mol dm⁻³ HCl is mixed with %s cm³ of %s mol dm⁻³ NaOH. The temperature rises by %s K. Calculate the enthalpy of neutralisation (c = 4.18 J g⁻¹ K⁻¹)." % (nf(V), nf(c, 2), nf(V), nf(c, 2), nf(dT, 2)), dH,
                  [-V * 4.18 * dT / n / 1000, -q / n, q / n / 1000], " kJ mol⁻¹", "q = mcΔT = %s × 4.18 × %s = %s J; n = %s mol; ΔH = −q/n = <b>%s kJ mol⁻¹</b>." % (nf(2 * V), nf(dT, 2), nf(q), nf(n), nf(dH)))
    name, f, M = fuel
    mw = ch([100.0, 150.0, 200.0, 250.0])
    mf = ch([0.25, 0.30, 0.40, 0.45, 0.50, 0.60])
    dT = ch([12.0, 15.0, 18.0, 20.0, 22.0, 25.0, 30.0])
    q = mw * 4.18 * dT
    n = mf / M
    dH = -q / n / 1000
    return nq("Burning %s g of %s (M<sub>r</sub> %s) heats %s g of water by %s K. Calculate the enthalpy of combustion (c = 4.18 J g⁻¹ K⁻¹)." % (nf(mf, 2), name, nf(M), nf(mw), nf(dT)), dH,
              [-q / mf / 1000, -q / n, -(mw + mf) * 4.18 * dT / n / 1000 * 2], " kJ mol⁻¹", "q = mcΔT = %s J; n = %s mol; ΔH = −q/n = <b>%s kJ mol⁻¹</b>." % (nf(q), nf(n), nf(dH)))


HESS = [("CH4 + 2O2 → CO2 + 2H2O", {"CH4": -74.8, "CO2": -393.5, "H2O": -285.8}, {"CH4": 1, "O2": 2}, {"CO2": 1, "H2O": 2}),
        ("C2H6 + 3½O2 → 2CO2 + 3H2O", {"C2H6": -84.7, "CO2": -393.5, "H2O": -285.8}, {"C2H6": 1, "O2": 3.5}, {"CO2": 2, "H2O": 3}),
        ("C2H5OH + 3O2 → 2CO2 + 3H2O", {"C2H5OH": -277.7, "CO2": -393.5, "H2O": -285.8}, {"C2H5OH": 1, "O2": 3}, {"CO2": 2, "H2O": 3}),
        ("CaCO3 → CaO + CO2", {"CaCO3": -1206.9, "CaO": -635.1, "CO2": -393.5}, {"CaCO3": 1}, {"CaO": 1, "CO2": 1}),
        ("C3H8 + 5O2 → 3CO2 + 4H2O", {"C3H8": -103.8, "CO2": -393.5, "H2O": -285.8}, {"C3H8": 1, "O2": 5}, {"CO2": 3, "H2O": 4}),
        ("Fe2O3 + 3CO → 2Fe + 3CO2", {"Fe2O3": -824.2, "CO": -110.5, "CO2": -393.5}, {"Fe2O3": 1, "CO": 3}, {"Fe": 2, "CO2": 3}),
        ("C2H4 + H2 → C2H6", {"C2H4": 52.3, "C2H6": -84.7}, {"C2H4": 1, "H2": 1}, {"C2H6": 1}),
        ("NH3 + HCl → NH4Cl", {"NH3": -46.1, "HCl": -92.3, "NH4Cl": -314.4}, {"NH3": 1, "HCl": 1}, {"NH4Cl": 1}),
        ("2NO + O2 → 2NO2", {"NO": 90.3, "NO2": 33.2}, {"NO": 2, "O2": 1}, {"NO2": 2}),
        ("MgCO3 → MgO + CO2", {"MgCO3": -1095.8, "MgO": -601.7, "CO2": -393.5}, {"MgCO3": 1}, {"MgO": 1, "CO2": 1}),
        ("SO2 + ½O2 → SO3", {"SO2": -296.8, "SO3": -395.7}, {"SO2": 1, "O2": 0.5}, {"SO3": 1}),
        ("C2H4 + H2O → C2H5OH", {"C2H4": 52.3, "H2O": -285.8, "C2H5OH": -277.7}, {"C2H4": 1, "H2O": 1}, {"C2H5OH": 1})]
COMB = [("methane", "CH4", 1, 4, 0, -890.3), ("ethane", "C2H6", 2, 6, 0, -1559.7), ("propane", "C3H8", 3, 8, 0, -2219.9), ("butane", "C4H10", 4, 10, 0, -2877.5),
        ("ethene", "C2H4", 2, 4, 0, -1411.0), ("benzene", "C6H6", 6, 6, 0, -3267.5), ("methanol", "CH3OH", 1, 4, 1, -726.0), ("ethanol", "C2H5OH", 2, 6, 1, -1366.8),
        ("propan-1-ol", "C3H7OH", 3, 8, 1, -2021.0), ("butan-1-ol", "C4H9OH", 4, 10, 1, -2675.6), ("ethanoic acid", "CH3COOH", 2, 4, 2, -874.2), ("glucose", "C6H12O6", 6, 12, 6, -2803.0),
        ("pentane", "C5H12", 5, 12, 0, -3509.0), ("hexane", "C6H14", 6, 14, 0, -4163.0), ("propene", "C3H6", 3, 6, 0, -2058.0), ("propanone", "CH3COCH3", 3, 6, 1, -1790.0)]
BE = {"C–H": 413, "C–C": 347, "C=C": 612, "O=O": 498, "C=O": 805, "O–H": 464, "H–H": 436, "Cl–Cl": 243, "H–Cl": 432, "C–Cl": 346, "N≡N": 945, "N–H": 391,
      "Br–Br": 193, "H–Br": 366, "C–Br": 290, "C–O": 358, "H–I": 299, "I–I": 151}
BEQ = [("H2 + Cl2 → 2HCl", {"H–H": 1, "Cl–Cl": 1}, {"H–Cl": 2}), ("H2 + Br2 → 2HBr", {"H–H": 1, "Br–Br": 1}, {"H–Br": 2}), ("H2 + I2 → 2HI", {"H–H": 1, "I–I": 1}, {"H–I": 2}),
       ("N2 + 3H2 → 2NH3", {"N≡N": 1, "H–H": 3}, {"N–H": 6}), ("CH4 + 2O2 → CO2 + 2H2O", {"C–H": 4, "O=O": 2}, {"C=O": 2, "O–H": 4}),
       ("CH4 + Cl2 → CH3Cl + HCl", {"C–H": 1, "Cl–Cl": 1}, {"C–Cl": 1, "H–Cl": 1}), ("C2H4 + H2 → C2H6", {"C=C": 1, "H–H": 1}, {"C–C": 1, "C–H": 2}),
       ("C2H4 + Br2 → C2H4Br2", {"C=C": 1, "Br–Br": 1}, {"C–C": 1, "C–Br": 2}), ("C2H4 + HBr → C2H5Br", {"C=C": 1, "H–Br": 1}, {"C–C": 1, "C–H": 1, "C–Br": 1}),
       ("2H2 + O2 → 2H2O", {"H–H": 2, "O=O": 1}, {"O–H": 4}), ("C2H6 + Cl2 → C2H5Cl + HCl", {"C–H": 1, "Cl–Cl": 1}, {"C–Cl": 1, "H–Cl": 1}),
       ("CH3OH + 1½O2 → CO2 + 2H2O", {"C–H": 3, "C–O": 1, "O–H": 1, "O=O": 1.5}, {"C=O": 2, "O–H": 4}), ("C2H5OH + 3O2 → 2CO2 + 3H2O", {"C–H": 5, "C–C": 1, "C–O": 1, "O–H": 1, "O=O": 3}, {"C=O": 4, "O–H": 6}),
       ("C2H4 + Cl2 → C2H4Cl2", {"C=C": 1, "Cl–Cl": 1}, {"C–C": 1, "C–Cl": 2}), ("C2H4 + H2O → C2H5OH", {"C=C": 1, "O–H": 1}, {"C–C": 1, "C–H": 1, "C–O": 1}),
       ("C3H8 + 5O2 → 3CO2 + 4H2O", {"C–H": 8, "C–C": 2, "O=O": 5}, {"C=O": 6, "O–H": 8})]


def c_hess(k=None):
    k = k or ch(["form", "bond"])
    if k == "comb":
        nm, f, c, h, o, dc = ch(COMB)
        dfH = c * -393.5 + h / 2 * -285.8 - dc
        return nq("Use enthalpies of combustion (kJ mol⁻¹): C −393.5, H₂ −285.8, %s %s. Calculate the standard enthalpy of formation of %s (%s)." % (fm(f), nf(dc, 5), nm, fm(f)), dfH,
                  [dc - (c * -393.5 + h / 2 * -285.8), c * -393.5 + h * -285.8 - dc, -393.5 - 285.8 - dc, c * -393.5 + h / 2 * -285.8 + dc], " kJ mol⁻¹",
                  "Δ<sub>f</sub>H = ΣΔ<sub>c</sub>H(elements) − Δ<sub>c</sub>H(compound) = %d × (−393.5) + %d × (−285.8) − (%s) = <b>%s kJ mol⁻¹</b>." % (c, h // 2, nf(dc, 5), nf(dfH, 4)), sf=4)
    if k == "unk":
        eq, br, mk = ch(BEQ)
        allb = [(x, n, 1) for x, n in br.items()] + [(x, n, -1) for x, n in mk.items()]
        x, n, sg = ch(allb)
        dH = sum(BE[y] * m for y, m in br.items()) - sum(BE[y] * m for y, m in mk.items())
        other = [(y, m, t) for y, m, t in allb if y != x]
        if not other:
            return None
        tab = ", ".join("%s %d" % (y, BE[y]) for y in sorted({y for y, m, t in other}))
        rest = sum(BE[y] * m * t for y, m, t in other)
        val = (dH - rest) / (n * sg)
        return nq("For %s, ΔH = %s kJ mol⁻¹. Mean bond enthalpies (kJ mol⁻¹): %s. Calculate the mean bond enthalpy of the %s bond." % (fm(eq), nf(dH, 4), tab, x), val,
                  [abs(dH - rest), (dH - rest) * n * sg, (dH + rest) / n if n else 0, abs((dH - rest) / (n * sg)) + 50], " kJ mol⁻¹",
                  "ΔH = bonds broken − bonds made. Put in the known values and solve: %s = <b>%s kJ mol⁻¹</b>." % (x, nf(val, 4)), sf=4)
    if k == "form":
        eq, data, rs, ps = ch(HESS)
        g = lambda side: sum(n * data.get(s, 0.0) for s, n in side.items())
        dH = g(ps) - g(rs)
        tab = ", ".join("%s %s" % (fm(s), nf(v, 4)) for s, v in data.items())
        return nq("Use these standard enthalpies of formation (kJ mol⁻¹): %s. Calculate ΔH for %s." % (tab, fm(eq)), dH,
                  [g(rs) - g(ps), sum(data.get(s, 0.0) for s in ps) - sum(data.get(s, 0.0) for s in rs), g(ps) + g(rs), g(ps), -g(rs)], " kJ mol⁻¹",
                  "ΔH = ΣΔ<sub>f</sub>H(products) − ΣΔ<sub>f</sub>H(reactants) = %s − (%s) = <b>%s kJ mol⁻¹</b>. Elements have Δ<sub>f</sub>H = 0." % (nf(g(ps), 4), nf(g(rs), 4), nf(dH, 4)), sf=4)
    eq, br, mk = ch(BEQ)
    b = sum(BE[x] * n for x, n in br.items())
    m = sum(BE[x] * n for x, n in mk.items())
    dH = b - m
    used = sorted(set(br) | set(mk))
    tab = ", ".join("%s %d" % (x, BE[x]) for x in used)
    return nq("Use these mean bond enthalpies (kJ mol⁻¹): %s. Calculate ΔH for %s." % (tab, fm(eq)), dH, [m - b, b + m, b - m / 2 if m else b], " kJ mol⁻¹",
              "ΔH = bonds broken − bonds made = %d − %d = <b>%s kJ mol⁻¹</b>." % (b, m, nf(dH, 4)), sf=4)


# =================================================================== Year 12: kinetics and equilibria
EQS = [("N2 + 3H2 ⇌ 2NH3", {"N2": 1, "H2": 3}, {"NH3": 2}, -92, "the Haber process"), ("2SO2 + O2 ⇌ 2SO3", {"SO2": 2, "O2": 1}, {"SO3": 2}, -197, "the Contact process"),
       ("H2 + I2 ⇌ 2HI", {"H2": 1, "I2": 1}, {"HI": 2}, -10, "making hydrogen iodide"), ("N2O4 ⇌ 2NO2", {"N2O4": 1}, {"NO2": 2}, 58, "dinitrogen tetroxide dissociating"),
       ("CO + 2H2 ⇌ CH3OH", {"CO": 1, "H2": 2}, {"CH3OH": 1}, -91, "making methanol"), ("CH4 + H2O ⇌ CO + 3H2", {"CH4": 1, "H2O": 1}, {"CO": 1, "H2": 3}, 206, "steam reforming"),
       ("C2H4 + H2O ⇌ C2H5OH", {"C2H4": 1, "H2O": 1}, {"C2H5OH": 1}, -45, "hydrating ethene"), ("CO + H2O ⇌ CO2 + H2", {"CO": 1, "H2O": 1}, {"CO2": 1, "H2": 1}, -41, "the water–gas shift reaction"),
       ("PCl5 ⇌ PCl3 + Cl2", {"PCl5": 1}, {"PCl3": 1, "Cl2": 1}, 88, "phosphorus pentachloride dissociating")]


def kcx(rs, ps, br="[", kt="]"):
    t = lambda side: " ".join("[%s]%s" % (fm(s), ("<sup>%d</sup>" % n) if n > 1 else "") for s, n in side.items())
    return t(ps), t(rs)


def c_kc(k=None):
    eq, rs, ps, dH, name = ch(EQS)
    k = k or ch(["expr", "calc", "shiftT", "shiftP", "cat"])
    if k == "expr":
        top, bot = kcx(rs, ps)
        top2, bot2 = kcx(ps, rs)
        flat = lambda side: " ".join("[%s]" % fm(s) for s in side)
        return tq("What is the expression for K<sub>c</sub> for %s?" % fm(eq), "%s / %s" % (top, bot), ["%s / %s" % (top2, bot2), "%s / %s" % (flat(ps), flat(rs)), "%s × %s" % (top, bot), "%s / %s" % (flat(rs), flat(ps)), "%s − %s" % (top, bot)],
                  "Products over reactants, each concentration raised to the power of its coefficient.")
    if k == "units":
        dg = sum(ps.values()) - sum(rs.values())
        U_ = {0: "no units", 1: "mol dm⁻³", -1: "mol⁻¹ dm³", 2: "mol² dm⁻⁶", -2: "mol⁻² dm⁶"}
        return tq("What are the units of K<sub>c</sub> for %s?" % fm(eq), U_[dg], [v for kk, v in U_.items() if kk != dg],
                  "Put mol dm⁻³ in for every concentration and cancel: %d on top and %d below." % (sum(ps.values()), sum(rs.values())))
    if k == "calc":
        conc = {s: ch([0.10, 0.20, 0.25, 0.40, 0.50, 0.80, 1.2, 1.5, 2.0]) for s in list(rs) + list(ps)}
        val = 1.0
        for s, n in ps.items():
            val *= conc[s] ** n
        for s, n in rs.items():
            val /= conc[s] ** n
        lin = 1.0
        for s in ps:
            lin *= conc[s]
        for s in rs:
            lin /= conc[s]
        dg = sum(ps.values()) - sum(rs.values())
        unit = "" if dg == 0 else (" mol%s dm%s" % (("⁻" if dg < 0 else "") + (str(abs(dg)).translate(SUP) if abs(dg) > 1 else "¹") if True else "", (("⁻" if dg > 0 else "") + (str(3 * abs(dg)).translate(SUP)))))
        if dg == 0:
            unit = ""
        elif dg == 1:
            unit = " mol dm⁻³"
        elif dg == -1:
            unit = " mol⁻¹ dm³"
        elif dg == -2:
            unit = " mol⁻² dm⁶"
        elif dg == 2:
            unit = " mol² dm⁻⁶"
        data = ", ".join("[%s] = %s" % (fm(s), nf(conc[s], 2)) for s in conc)
        return nq("At equilibrium for %s: %s mol dm⁻³. Calculate K<sub>c</sub>." % (fm(eq), data), val, [lin, 1 / val, val * 2 if dg else val ** 0.5], unit, "K<sub>c</sub> = products ÷ reactants with powers = <b>%s</b>%s." % (nf(val), unit))
    if k == "cat":
        return tq("A catalyst is added to %s (%s) at equilibrium. What happens?" % (fm(eq), name), "the position of equilibrium does not change; equilibrium is reached faster",
                  ["the equilibrium shifts to the right", "the equilibrium shifts to the left", "K<sub>c</sub> increases"], "A catalyst speeds up the forward and backward reactions equally.")
    if k == "shiftT":
        up = ch([True, False])
        right = (dH > 0) == up
        ans = "the equilibrium shifts to the right and K<sub>c</sub> increases" if right else "the equilibrium shifts to the left and K<sub>c</sub> decreases"
        return tq("For %s, ΔH = %s kJ mol⁻¹. What happens if the temperature is %s?" % (fm(eq), nf(dH), "increased" if up else "decreased"), ans,
                  ["the equilibrium shifts to the right and K<sub>c</sub> increases", "the equilibrium shifts to the left and K<sub>c</sub> decreases", "nothing changes", "the equilibrium shifts to the right but K<sub>c</sub> stays the same"],
                  "The forward reaction is %s. %s favours the %s direction. Only temperature changes K<sub>c</sub>." % ("endothermic" if dH > 0 else "exothermic", "Heating" if up else "Cooling", "endothermic" if up else "exothermic"))
    gl, gr = sum(n for s, n in rs.items() if s not in ("I2",)) if "I2" not in rs else sum(rs.values()), sum(ps.values())
    gl = sum(rs.values())
    if gl == gr:
        ans = "no change in the position of equilibrium"
    else:
        up = ch([True, False])
        ans = ("the equilibrium shifts to the right" if (gr < gl) == up else "the equilibrium shifts to the left")
        return tq("What happens to the equilibrium %s (all gases) if the pressure is %s?" % (fm(eq), "increased" if up else "decreased"), ans,
                  ["the equilibrium shifts to the right", "the equilibrium shifts to the left", "no change in the position of equilibrium", "K<sub>c</sub> increases"],
                  "There are %d moles of gas on the left and %d on the right. %s pressure favours the side with %s moles." % (gl, gr, "Higher" if up else "Lower", "fewer" if up else "more"))
    return tq("What happens to the equilibrium %s (all gases) if the pressure is increased?" % fm(eq), ans, ["the equilibrium shifts to the right", "the equilibrium shifts to the left", "K<sub>c</sub> increases"],
              "There are the same number of moles of gas on each side.")


def c_ice(k=None):
    a0 = ch([1.0, 2.0, 3.0, 4.0, 5.0])
    b0 = ch([1.0, 2.0, 3.0, 4.0, 5.0])
    x = ch([0.5, 0.6, 0.8, 1.0, 1.2, 1.5])
    if x >= min(a0, b0):
        return None
    V = ch([1.0, 2.0, 5.0])
    kc = (x / V) ** 2 / ((a0 - x) / V * (b0 - x) / V)
    return nq("%s mol of ethanoic acid and %s mol of ethanol are mixed in %s dm³. At equilibrium %s mol of ethyl ethanoate has formed: CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O. Calculate K<sub>c</sub>." % (nf(a0, 2), nf(b0, 2), nf(V, 2), nf(x, 2)),
              kc, [x * x / (a0 * b0), x / ((a0 - x) * (b0 - x)), (a0 - x) * (b0 - x) / (x * x)], "",
              "At equilibrium: acid %s, alcohol %s, ester %s, water %s mol. V cancels: K<sub>c</sub> = %s² ÷ (%s × %s) = <b>%s</b>." % (nf(a0 - x, 2), nf(b0 - x, 2), nf(x, 2), nf(x, 2), nf(x, 2), nf(a0 - x, 2), nf(b0 - x, 2), nf(kc)))


MB = [("In a Maxwell–Boltzmann distribution, what does the area under the curve represent?", "the total number of molecules", ["the activation energy", "the average energy", "the rate of reaction"], "The area stays the same when the temperature changes."),
      ("What happens to the Maxwell–Boltzmann curve at a higher temperature?", "the peak moves to the right and gets lower", ["the peak moves to the left and gets higher", "the area under the curve increases", "the curve starts at a higher energy"], "More molecules have higher energies, but the total number is the same."),
      ("Why does a small rise in temperature greatly increase the rate?", "many more molecules have energy greater than the activation energy", ["the activation energy falls", "the molecules become larger", "the concentration increases"], "The tail of the distribution beyond E<sub>a</sub> grows a lot."),
      ("How does a catalyst increase the rate of a reaction?", "it provides an alternative route with a lower activation energy", ["it gives the molecules more energy", "it shifts the equilibrium to the right", "it increases the temperature"], "More molecules then have at least the activation energy."),
      ("What is the activation energy?", "the minimum energy needed for a reaction to happen", ["the energy released by a reaction", "the average kinetic energy of the molecules", "the enthalpy change"], "Collisions with less energy do not react."),
      ("Where does the Maxwell–Boltzmann curve start?", "at the origin, because no molecules have zero energy", ["at the activation energy", "half way up the y-axis", "at the most probable energy"], "It never touches the x-axis at high energy either."),
      ("What does 'dynamic equilibrium' mean?", "the forward and backward rates are equal, so concentrations stay constant", ["the reactions have stopped", "there are equal amounts of reactants and products", "only the forward reaction happens"], "It needs a closed system."),
      ("What is Le Chatelier's principle?", "a system at equilibrium shifts to oppose a change in conditions", ["equilibrium always lies to the right", "a catalyst moves equilibrium", "pressure has no effect on gases"], "Use it to predict the effect of changing temperature, pressure or concentration."),
      ("Why is the Haber process run at about 450 °C even though a lower temperature gives a higher yield?", "it is a compromise that gives a fast enough rate", ["the catalyst only works above 1000 °C", "the reaction is endothermic", "a higher temperature increases the yield"], "A low temperature favours the exothermic forward reaction but is too slow."),
      ("Why is a high pressure expensive in industry?", "strong equipment and lots of energy for compressors are needed", ["it slows the reaction", "it lowers the yield", "it breaks the catalyst"], "Pressures are a compromise between yield and cost."),
      ("Increasing the concentration of a reactant…", "increases the rate because collisions are more frequent", ["increases the activation energy", "gives each molecule more energy", "decreases the rate"], "More particles in the same volume."),
      ("Which factor changes the value of K<sub>c</sub>?", "temperature", ["pressure", "concentration", "a catalyst"], "K<sub>c</sub> depends only on temperature."),
      ("What happens to the rate of a gas reaction if the pressure is doubled?", "it increases, because the particles are closer together", ["it halves", "it does not change", "it decreases because K<sub>c</sub> changes"], "Higher pressure means higher concentration of gas."),
      ("Why does powdered calcium carbonate react faster with acid than marble chips?", "it has a larger surface area, so collisions are more frequent", ["it has a lower activation energy", "its particles have more energy", "it is a catalyst"], "More particles are exposed to the acid."),
      ("What happens to the activation energy when a catalyst is added?", "a different route with a lower activation energy is used", ["it increases", "it stays the same but molecules move faster", "it becomes zero"], "The original route is still there; the catalysed route is easier."),
      ("Which part of the Maxwell–Boltzmann curve shows the molecules that can react?", "the area to the right of the activation energy", ["the peak of the curve", "the area to the left of the activation energy", "the point where the curve starts"], "Only these molecules have enough energy."),
      ("What is the mode of a Maxwell–Boltzmann distribution?", "the most probable energy, at the peak", ["the mean energy", "the activation energy", "the highest energy"], "The mean energy is a little to the right of the peak."),
      ("Why do most collisions not lead to a reaction?", "the particles do not have enough energy or the right orientation", ["the particles are too small", "the temperature is too high", "the products form too slowly"], "Successful collisions need E ≥ E<sub>a</sub>."),
      ("What happens to the yield of ammonia if ammonia is removed as it forms?", "the equilibrium shifts right, so more ammonia forms", ["the equilibrium shifts left", "the reaction stops", "K<sub>c</sub> increases"], "Removing a product makes the system replace it."),
      ("A reaction mixture is at equilibrium. More reactant is added. What happens?", "the equilibrium shifts to the right", ["the equilibrium shifts to the left", "K<sub>c</sub> increases", "nothing changes"], "The system uses up some of the added reactant.")]


# =================================================================== Year 12: redox and inorganic chemistry
OXS = [("Mn", "MnO4^-", 7), ("Cr", "Cr2O7^2-", 6), ("S", "SO4^2-", 6), ("S", "SO2", 4), ("S", "H2S", -2), ("N", "NO3^-", 5), ("N", "NH4^+", -3), ("N", "NO2", 4), ("N", "N2O", 1),
       ("Cl", "ClO^-", 1), ("Cl", "ClO3^-", 5), ("Cl", "ClO4^-", 7), ("Fe", "Fe2O3", 3), ("Fe", "Fe3O4", F(8, 3)), ("Mn", "MnO2", 4), ("C", "CO", 2), ("C", "C2O4^2-", 3), ("P", "PO4^3-", 5),
       ("S", "S2O3^2-", 2), ("S", "S4O6^2-", F(5, 2)), ("I", "IO3^-", 5), ("Cr", "CrO4^2-", 6), ("V", "VO2^+", 5), ("V", "VO^2+", 4), ("Cu", "Cu2O", 1), ("O", "H2O2", -1), ("H", "NaH", -1), ("Br", "BrO3^-", 5),
       ("S", "H2SO4", 6), ("S", "SO3^2-", 4), ("N", "HNO2", 3), ("N", "NO", 2), ("N", "N2H4", -2), ("N", "NH3", -3), ("C", "CH4", -4), ("C", "CO2", 4), ("C", "CH3OH", -2),
       ("Cl", "HClO", 1), ("Cl", "Cl2O7", 7), ("Cl", "ClO2", 4), ("Mn", "MnO4^2-", 6), ("Mn", "Mn2O3", 3), ("Cr", "Cr2O3", 3), ("Fe", "FeO4^2-", 6), ("P", "P4O10", 5), ("P", "PCl3", 3),
       ("I", "IO4^-", 7), ("I", "ICl", 1), ("O", "OF2", 2), ("O", "Na2O2", -1), ("Pb", "PbO2", 4), ("Sn", "SnCl4", 4), ("Cu", "CuO", 2), ("V", "V2O5", 5), ("Ti", "TiCl4", 4), ("Co", "CoCl2", 2)]


HALF = [("MnO₄⁻ → Mn²⁺ (in acid)", 5, "reduction", "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O"), ("Cr₂O₇²⁻ → 2Cr³⁺ (in acid)", 6, "reduction", "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O"),
        ("Fe²⁺ → Fe³⁺", 1, "oxidation", "Fe²⁺ → Fe³⁺ + e⁻"), ("Cl₂ → 2Cl⁻", 2, "reduction", "Cl₂ + 2e⁻ → 2Cl⁻"), ("2I⁻ → I₂", 2, "oxidation", "2I⁻ → I₂ + 2e⁻"),
        ("NO₃⁻ → NO (in acid)", 3, "reduction", "NO₃⁻ + 4H⁺ + 3e⁻ → NO + 2H₂O"), ("NO₃⁻ → NO₂ (in acid)", 1, "reduction", "NO₃⁻ + 2H⁺ + e⁻ → NO₂ + H₂O"),
        ("SO₄²⁻ → SO₂ (in acid)", 2, "reduction", "SO₄²⁻ + 4H⁺ + 2e⁻ → SO₂ + 2H₂O"), ("SO₄²⁻ → H₂S (in acid)", 8, "reduction", "SO₄²⁻ + 10H⁺ + 8e⁻ → H₂S + 4H₂O"),
        ("H₂O₂ → 2H₂O (in acid)", 2, "reduction", "H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O"), ("Zn → Zn²⁺", 2, "oxidation", "Zn → Zn²⁺ + 2e⁻"), ("Al → Al³⁺", 3, "oxidation", "Al → Al³⁺ + 3e⁻"),
        ("Cu²⁺ → Cu", 2, "reduction", "Cu²⁺ + 2e⁻ → Cu"), ("2S₂O₃²⁻ → S₄O₆²⁻", 2, "oxidation", "2S₂O₃²⁻ → S₄O₆²⁻ + 2e⁻"), ("C₂O₄²⁻ → 2CO₂", 2, "oxidation", "C₂O₄²⁻ → 2CO₂ + 2e⁻"),
        ("2IO₃⁻ → I₂ (in acid)", 10, "reduction", "2IO₃⁻ + 12H⁺ + 10e⁻ → I₂ + 6H₂O"), ("O₂ → 2H₂O (in acid)", 4, "reduction", "O₂ + 4H⁺ + 4e⁻ → 2H₂O"),
        ("2Br⁻ → Br₂", 2, "oxidation", "2Br⁻ → Br₂ + 2e⁻"), ("H₂ → 2H⁺", 2, "oxidation", "H₂ → 2H⁺ + 2e⁻"), ("MnO₂ → Mn²⁺ (in acid)", 2, "reduction", "MnO₂ + 4H⁺ + 2e⁻ → Mn²⁺ + 2H₂O"),
        ("Sn²⁺ → Sn⁴⁺", 2, "oxidation", "Sn²⁺ → Sn⁴⁺ + 2e⁻"), ("VO₂⁺ → VO²⁺ (in acid)", 1, "reduction", "VO₂⁺ + 2H⁺ + e⁻ → VO²⁺ + H₂O")]


def c_halfe(k=None):
    sp, n, kind, full = ch(HALF)
    k = k or ch(["n", "kind"])
    if k == "kind":
        return tq("Is this change oxidation or reduction: %s?" % sp, kind, [x for x in ["oxidation", "reduction", "neither", "both"] if x != kind],
                  "%s. Electrons on the left mean reduction (gain); on the right mean oxidation (loss)." % full)
    return nq("How many electrons appear in the balanced half-equation for %s?" % sp, n, [n + 1, n * 2, abs(n - 2) or 3, n + 3], "", "%s: <b>%d</b> electron%s." % (full, n, "" if n == 1 else "s"))


HALS = [("chlorine", "Cl₂", 1), ("bromine", "Br₂", 2), ("iodine", "I₂", 3)]
HCOL = {"Br⁻": "the solution turns orange", "I⁻": "the solution turns brown"}


def c_disp(k=None):
    (hn, hf, a), (_, ion_from, b) = ch(HALS), ch(HALS)
    ions = {1: "Cl⁻", 2: "Br⁻", 3: "I⁻"}
    salt = {1: "potassium chloride", 2: "potassium bromide", 3: "potassium iodide"}[b]
    if a == b:
        return None
    k = k or ch(["see", "eq"])
    if a < b:
        ans = HCOL[ions[b]]
        e = "%s is a stronger oxidising agent than %s, so it displaces it: %s + 2%s → 2%s + %s." % (hn.capitalize(), ions[b].replace("⁻", "") + "₂" if False else {2: "bromine", 3: "iodine"}[b], hf, ions[b], ions[a], {2: "Br₂", 3: "I₂"}[b])
    else:
        ans = "no reaction"
        e = "%s is a weaker oxidising agent than %s, so it cannot displace it." % (hn.capitalize(), {1: "chlorine", 2: "bromine"}[b])
    if k == "eq":
        if a > b:
            return None
        return tq("Which ionic equation shows %s water reacting with %s solution?" % (hn, salt), "%s + 2%s → 2%s + %s" % (hf, ions[b], ions[a], {2: "Br₂", 3: "I₂"}[b]),
                  ["%s + %s → %s + %s" % (hf, ions[b], ions[a], {2: "Br₂", 3: "I₂"}[b]), "%s + 2%s → 2%s + %s" % ({2: "Br₂", 3: "I₂"}[b], ions[a], ions[b], hf), "%s + 2%s → %s + %s" % (hf, ions[b], ions[a], {2: "Br₂", 3: "I₂"}[b])], e)
    return tq("%s water is added to %s solution. What is seen?" % (hn.capitalize(), salt), ans, [x for x in ["no reaction", "the solution turns orange", "the solution turns brown", "a white precipitate forms"] if x != ans], e)


G2X = [("Which group 2 metal reacts most vigorously with cold water?", "barium", ["magnesium", "beryllium", "calcium"], "Reactivity increases down group 2."),
       ("Which group 2 hydroxide is used as an antacid (milk of magnesia)?", "magnesium hydroxide", ["barium hydroxide", "calcium hydroxide", "strontium hydroxide"], "It is only sparingly soluble, so it is mild."),
       ("What is used to extract titanium from TiCl₄?", "magnesium", ["carbon", "calcium hydroxide", "barium"], "TiCl₄ + 2Mg → Ti + 2MgCl₂."),
       ("Why does the atomic radius increase down group 2?", "each element has an extra shell of electrons", ["the nuclear charge decreases", "the atoms lose electrons", "metallic bonding gets stronger"], "Extra shells outweigh the increase in nuclear charge."),
       ("Why does the melting point generally decrease down group 2?", "the metallic bonding gets weaker as the ions get bigger", ["the ions get smaller", "there are more delocalised electrons", "the bonds become covalent"], "Larger ions attract the delocalised electrons less strongly."),
       ("What is seen when calcium reacts with water?", "fizzing and a cloudy white solution", ["a brown precipitate", "no reaction", "a purple flame"], "Ca + 2H₂O → Ca(OH)₂ + H₂; Ca(OH)₂ is slightly soluble."),
       ("Which equation shows magnesium reacting slowly with cold water?", "Mg + 2H₂O → Mg(OH)₂ + H₂", ["Mg + H₂O → MgO + H₂", "Mg + H₂O → MgH₂ + O", "2Mg + O₂ → 2MgO"], "With steam MgO forms instead."),
       ("How can SO₂ be removed from power-station flue gases?", "react it with calcium oxide or calcium carbonate", ["dissolve it in water", "burn it", "react it with chlorine"], "This makes calcium sulfite."),
       ("What is the pH of a solution of barium hydroxide?", "about 13–14 (strongly alkaline)", ["about 7", "about 2", "about 9"], "Ba(OH)₂ is the most soluble group 2 hydroxide.")]
HALX = [("What colour is bromine water?", "orange", ["purple", "pale green", "colourless"], "Iodine solution is brown; chlorine water is pale green."),
        ("What colour is iodine vapour?", "purple", ["orange", "brown", "pale green"], "Solid iodine is grey-black."),
        ("Why are the boiling points of the halogens higher down the group?", "bigger molecules have stronger van der Waals forces", ["hydrogen bonding increases", "the covalent bonds get stronger", "the electronegativity increases"], "More electrons give bigger induced dipoles."),
        ("How does electronegativity change down group 7?", "it decreases", ["it increases", "it stays the same", "it increases then decreases"], "The bonding pair is further from the nucleus."),
        ("Which halide ion reduces concentrated sulfuric acid to sulfur dioxide but not further?", "Br⁻", ["Cl⁻", "I⁻", "F⁻"], "Br⁻ is a stronger reducing agent than Cl⁻ but weaker than I⁻."),
        ("Which silver halide dissolves in dilute ammonia?", "silver chloride", ["silver bromide", "silver iodide", "all of them"], "AgBr needs concentrated ammonia; AgI does not dissolve."),
        ("Why is the silver nitrate acidified with nitric acid in the halide test?", "to remove carbonate ions that would also give a precipitate", ["to make the precipitate dissolve", "to add chloride ions", "to change the colour"], "Hydrochloric acid would add Cl⁻ ions."),
        ("What is the oxidation state of chlorine in NaClO, formed in bleach?", "+1", ["−1", "+5", "0"], "Na is +1 and O is −2."),
        ("What is seen when chlorine reacts with water in sunlight?", "bubbles of oxygen form and the solution becomes colourless", ["a white precipitate forms", "the solution turns orange", "no change"], "2Cl₂ + 2H₂O → 4HCl + O₂.")]
P3X = [("Why does the first ionisation energy drop from phosphorus to sulfur?", "sulfur has a pair of electrons in one 3p orbital, which repel", ["sulfur has fewer protons", "sulfur's electron is in 4s", "phosphorus is a metal"], "Paired electrons are easier to remove."),
       ("Why does sulfur (S₈) have a higher melting point than phosphorus (P₄)?", "S₈ molecules are larger, with stronger van der Waals forces", ["sulfur is giant covalent", "sulfur has hydrogen bonds", "phosphorus is ionic"], "Both are simple molecular."),
       ("Why does argon have the lowest melting point in period 3?", "it exists as single atoms with very weak van der Waals forces", ["it is metallic", "it has ionic bonds", "it is giant covalent"], "There are no bonds between atoms."),
       ("Why does aluminium conduct electricity better than sodium?", "aluminium has more delocalised electrons per atom", ["aluminium atoms are bigger", "aluminium is covalent", "sodium has no free electrons"], "Al gives three electrons per atom to the sea of electrons."),
       ("How does electronegativity change across period 3?", "it increases", ["it decreases", "it stays the same", "it decreases then increases"], "The nuclear charge increases while shielding stays about the same.")]


def c_ox(k=None):
    el, sp, n = ch(OXS)
    if isinstance(n, F):
        return None
    s = lambda v: ("+%d" % v if v > 0 else str(v).replace("-", "−"))
    return tq("What is the oxidation state of %s in %s?" % (el, fm(sp)), s(n), [s(n - 2), s(-n) if n else "+1", s(n + 1)],
              "Oxygen is −2 (−1 in peroxides), hydrogen +1 (−1 in metal hydrides); the total equals the charge on the species.")


INORG = [("Which reagent is used to test for halide ions?", "acidified silver nitrate solution", ["barium chloride solution", "sodium hydroxide solution", "limewater"], "Silver halides form coloured precipitates."),
         ("What colour precipitate forms when silver nitrate is added to chloride ions?", "white", ["cream", "yellow", "green"], "AgCl is white and dissolves in dilute ammonia."),
         ("What colour precipitate forms when silver nitrate is added to bromide ions?", "cream", ["white", "yellow", "brown"], "AgBr dissolves in concentrated ammonia only."),
         ("What colour precipitate forms when silver nitrate is added to iodide ions?", "yellow", ["white", "cream", "black"], "AgI does not dissolve in ammonia."),
         ("How does the oxidising power of the halogens change down group 7?", "it decreases", ["it increases", "it stays the same", "it increases then decreases"], "The atoms get bigger, so they attract an extra electron less strongly."),
         ("Which halide ion is the strongest reducing agent?", "I⁻", ["F⁻", "Cl⁻", "Br⁻"], "Iodide reduces concentrated sulfuric acid all the way to H₂S."),
         ("Which gas forms when concentrated sulfuric acid is added to solid sodium chloride?", "hydrogen chloride", ["sulfur dioxide", "hydrogen sulfide", "chlorine"], "Cl⁻ is too weak a reducing agent to reduce H₂SO₄."),
         ("Which product shows that iodide reduces concentrated sulfuric acid strongly?", "hydrogen sulfide (bad-egg smell)", ["hydrogen chloride", "oxygen", "chlorine"], "Sulfur goes from +6 to −2."),
         ("What forms when chlorine reacts with cold dilute sodium hydroxide?", "NaCl, NaClO and water", ["NaCl and oxygen", "HCl and NaClO₃", "Cl₂O and NaH"], "Chlorine is both oxidised and reduced (disproportionation)."),
         ("What is disproportionation?", "the same element is both oxidised and reduced", ["two elements swap electrons", "a reaction with no electron transfer", "an element gains oxygen only"], "For example Cl₂ + H₂O → HCl + HClO."),
         ("Why is chlorine added to drinking water?", "it kills bacteria", ["it removes hardness", "it adds minerals", "it neutralises acids"], "The benefit outweighs the risk from chlorinated compounds."),
         ("How does the solubility of group 2 hydroxides change down the group?", "it increases", ["it decreases", "it stays the same", "it increases then decreases"], "Mg(OH)₂ is sparingly soluble; Ba(OH)₂ is quite soluble."),
         ("How does the solubility of group 2 sulfates change down the group?", "it decreases", ["it increases", "it stays the same", "it increases then decreases"], "BaSO₄ is insoluble."),
         ("Which reagent tests for sulfate ions?", "acidified barium chloride solution", ["silver nitrate solution", "sodium hydroxide solution", "limewater"], "A white precipitate of BaSO₄ forms."),
         ("Why is barium sulfate safe to use in a 'barium meal'?", "it is insoluble, so it is not absorbed", ["barium is not toxic", "it dissolves quickly", "it is a strong acid"], "Soluble barium compounds are toxic."),
         ("How does the reactivity of group 2 metals with water change down the group?", "it increases", ["it decreases", "it stays the same", "only magnesium reacts"], "The outer electrons are lost more easily."),
         ("What forms when magnesium burns in steam?", "magnesium oxide and hydrogen", ["magnesium hydroxide and oxygen", "magnesium hydride", "magnesium carbonate"], "Mg + H₂O → MgO + H₂."),
         ("Which group 2 hydroxide is used to treat acid soil?", "calcium hydroxide", ["barium hydroxide", "beryllium hydroxide", "strontium hydroxide"], "Slaked lime neutralises acidity."),
         ("How does the first ionisation energy change down group 2?", "it decreases", ["it increases", "it stays the same", "it increases then decreases"], "Outer electrons are further from the nucleus and more shielded."),
         ("What is an oxidising agent?", "an electron acceptor", ["an electron donor", "a proton donor", "a substance that is oxidised"], "The oxidising agent is itself reduced."),
         ("Which half-equation shows oxidation?", "Fe²⁺ → Fe³⁺ + e⁻", ["Cl₂ + 2e⁻ → 2Cl⁻", "Cu²⁺ + 2e⁻ → Cu", "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O"], "Oxidation is loss of electrons."),
         ("Why does the atomic radius decrease across period 3?", "the nuclear charge increases with similar shielding", ["there are more shells", "the atoms lose electrons", "metallic bonding gets weaker"], "Electrons are pulled closer to the nucleus."),
         ("Which period 3 element has the highest melting point?", "silicon", ["sodium", "sulfur", "argon"], "Silicon is a giant covalent (macromolecular) structure."),
         ("Why is there a dip in first ionisation energy from Mg to Al?", "aluminium's outer electron is in a higher-energy 3p sub-shell", ["aluminium has fewer protons", "magnesium has a paired 3p electron", "aluminium has more shells"], "The 3p electron is also slightly shielded by 3s.")]


# =================================================================== Year 12: organic chemistry
STEM = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept"}


def chain(n, pos, grp):
    """condensed formula for a chain of n carbons with a group at carbon pos (1-based)"""
    parts = []
    for i in range(1, n + 1):
        h = 3 if i in (1, n) else 2
        if n == 1:
            h = 4
        g = ""
        if i == pos and grp in ("OH", "Cl", "Br", "CH3"):
            h -= 1
            g = "(%s)" % grp if 1 < i < n or grp == "CH3" else grp
        parts.append((i, h, g))
    s = ""
    for i, h, g in parts:
        c = "C" + ("H" if h == 1 else "H%d" % h if h else "")
        if grp in ("OH", "Cl", "Br") and i == pos and i in (1, n):
            c = ("CH%d" % h if h > 1 else "CH") + g if i == n else (g + "CH%d" % h if h > 1 else g + "CH")
            if i == 1:
                c = "CH%d%s" % (h, g) if h > 1 else "CH" + g
                c = c.replace("CH2OH", "CH2OH")
            s += c
            continue
        s += c + g
    if grp == "=":
        # double bond between pos and pos+1
        atoms = []
        for i in range(1, n + 1):
            h = 3 if i in (1, n) else 2
            if i in (pos, pos + 1):
                h -= 1
            atoms.append("CH%d" % h if h > 1 else ("CH" if h == 1 else "C"))
        s = "".join(a + ("=" if i == pos else "") for i, a in enumerate(atoms, 1))
    return s


def c_name(k=None):
    grp = ch(["OH", "Cl", "Br", "CH3", "="])
    n = ch([3, 4, 5, 6])
    if grp == "=":
        pos = ch(range(1, n))
        low = min(pos, n - pos)
        if low != pos:
            return None
        nm = "%s-%d-ene" % (STEM[n], pos) if n > 3 else "propene"
        wr = ["%s-%d-ene" % (STEM[n], n - pos) if n - pos != pos else "%s-%d-ene" % (STEM[n], pos + 1), "%sane" % STEM[n], "%s-%d-ene" % (STEM[n + 1], pos)]
        if n == 3:
            wr = ["propane", "prop-2-ene", "butene"]
    else:
        pos = ch(range(1, n + 1))
        if grp == "CH3" and (pos in (1, n)):
            return None
        low = min(pos, n + 1 - pos)
        if grp == "CH3":
            if n < 4:
                return None
            nm = "%d-methyl%sane" % (low, STEM[n])
            wr = ["%d-methyl%sane" % (n + 1 - low, STEM[n]) if n + 1 - low != low else "%d-methyl%sane" % (low + 1, STEM[n]), "%sane" % STEM[n + 1], "%d-methyl%sane" % (low, STEM[n + 1])]
        elif grp == "OH":
            nm = "%san-%d-ol" % (STEM[n], low)
            wr = ["%san-%d-ol" % (STEM[n], n + 1 - low) if n + 1 - low != low else "%san-%d-ol" % (STEM[n], low + 1), "%d-hydroxy%sane" % (low, STEM[n]), "%san-%d-ol" % (STEM[n + 1], low)]
        else:
            h = {"Cl": "chloro", "Br": "bromo"}[grp]
            nm = "%d-%s%sane" % (low, h, STEM[n])
            wr = ["%d-%s%sane" % (n + 1 - low, h, STEM[n]) if n + 1 - low != low else "%d-%s%sane" % (low + 1, h, STEM[n]), "%d-%s%sane" % (low, h, STEM[n - 1]), "%d-%s%sane" % (low, h, STEM[n + 1])]
    return tq("What is the IUPAC name of %s?" % fm(chain(n, pos, grp)), nm, wr,
              "The longest chain has %d carbons (%s-). Number from the end that gives the lowest locant." % (n + (0 if grp != "CH3" else 0), STEM[n]))


def c_formula(k=None):
    k = k or ch(["alk", "comb", "mr", "ene"])
    n = ch(list(range(1, 21)) + [22, 25, 30])
    if k == "alk":
        return tq("What is the molecular formula of the alkane with %d carbon atoms?" % n, fm("C%dH%d" % (n, 2 * n + 2) if n > 1 else "CH4"),
                  [fm("C%dH%d" % (n, 2 * n)), fm("C%dH%d" % (n, 2 * n + 1)), fm("C%dH%d" % (n, 2 * n + 4))], "Alkanes are C<sub>n</sub>H<sub>2n+2</sub>.") if n > 1 else None
    if k == "ene":
        if n < 2:
            return None
        return tq("What is the molecular formula of the alkene with %d carbon atoms and one C=C bond?" % n, fm("C%dH%d" % (n, 2 * n)),
                  [fm("C%dH%d" % (n, 2 * n + 2)), fm("C%dH%d" % (n, 2 * n - 2)), fm("C%dH%d" % (n, 2 * n + 1))], "Alkenes are C<sub>n</sub>H<sub>2n</sub>.")
    if k == "mr":
        return nq("Calculate the M<sub>r</sub> of the alkane with %d carbon atoms." % n, 14 * n + 2, [14 * n, 12 * n + 2 * n, 13 * n + 2], "", "C<sub>%d</sub>H<sub>%d</sub>: %d × 12.0 + %d × 1.0 = <b>%d</b>." % (n, 2 * n + 2, n, 2 * n + 2, 14 * n + 2))
    o2 = F(3 * n + 1, 2)
    s = lambda v: str(v.numerator) if v.denominator == 1 else "%s½" % (v.numerator // 2) if v.denominator == 2 and v.numerator > 1 else "½"
    return tq("How many moles of oxygen are needed to burn one mole of C<sub>%d</sub>H<sub>%d</sub> completely?" % (n, 2 * n + 2), s(o2), [s(o2 + 1), s(F(2 * n + 1, 1)), s(F(n + 1, 1) + F(n, 2))],
              "C<sub>n</sub>H<sub>2n+2</sub> + (3n+1)/2 O<sub>2</sub> → nCO<sub>2</sub> + (n+1)H<sub>2</sub>O. %d CO₂ need %d O atoms, %d H₂O need %d O atoms: %d ÷ 2 = %s." % (n, 2 * n, n + 1, n + 1, 3 * n + 1, s(o2))) if n > 1 else None


MECH = [("What type of mechanism happens when chlorine reacts with methane in UV light?", "free-radical substitution", ["electrophilic addition", "nucleophilic substitution", "elimination"], "UV light splits Cl₂ into radicals (initiation)."),
        ("What type of mechanism happens when bromine reacts with ethene?", "electrophilic addition", ["free-radical substitution", "nucleophilic substitution", "elimination"], "The C=C bond is electron-rich and attracts electrophiles."),
        ("What type of mechanism happens when bromoethane reacts with aqueous NaOH?", "nucleophilic substitution", ["electrophilic addition", "elimination", "free-radical substitution"], "OH⁻ attacks the δ+ carbon."),
        ("What forms when bromoethane is heated with ethanolic KOH?", "ethene (elimination)", ["ethanol (substitution)", "ethane", "bromoethene"], "In ethanol, OH⁻ acts as a base."),
        ("Which test shows that a compound is an alkene?", "bromine water turns from orange to colourless", ["limewater turns milky", "a squeaky pop", "universal indicator turns purple"], "Bromine adds across the C=C."),
        ("What is the major product when HBr adds to propene?", "2-bromopropane", ["1-bromopropane", "propane", "1,2-dibromopropane"], "It goes via the more stable secondary carbocation."),
        ("Why does a C=C bond prevent rotation and allow E/Z isomers?", "the π bond stops rotation", ["it is weaker than a single bond", "the carbons are charged", "it contains a lone pair"], "Each carbon of the C=C must have two different groups."),
        ("Which alcohol can be oxidised to a ketone?", "propan-2-ol", ["propan-1-ol", "2-methylpropan-2-ol", "methanol"], "Secondary alcohols give ketones."),
        ("Which alcohol is not oxidised by acidified potassium dichromate?", "2-methylpropan-2-ol", ["ethanol", "propan-2-ol", "butan-1-ol"], "Tertiary alcohols resist oxidation."),
        ("What colour change is seen when acidified potassium dichromate oxidises an alcohol?", "orange to green", ["green to orange", "purple to colourless", "blue to green"], "Cr₂O₇²⁻ is reduced to Cr³⁺."),
        ("How is a primary alcohol oxidised to an aldehyde rather than an acid?", "distil the aldehyde off as it forms", ["heat under reflux", "use excess oxidising agent", "add water"], "Reflux would oxidise it further to a carboxylic acid."),
        ("What is the condition for making ethanol by fermentation?", "yeast, about 35 °C, no air", ["phosphoric acid catalyst at 300 °C", "UV light", "nickel catalyst"], "Yeast enzymes work best at warm temperatures, anaerobically."),
        ("What catalyst is used to hydrate ethene to ethanol?", "phosphoric acid", ["nickel", "yeast", "iron"], "Steam and ethene at about 300 °C and 60 atm."),
        ("What is cracking?", "breaking long-chain alkanes into shorter alkanes and alkenes", ["joining small molecules into polymers", "burning alkanes", "separating crude oil by boiling point"], "Thermal cracking gives many alkenes; catalytic cracking gives branched alkanes and aromatics."),
        ("Why is the C–I bond the most reactive carbon–halogen bond?", "it has the lowest bond enthalpy", ["it is the most polar", "iodine is the most electronegative", "it is the shortest bond"], "Bond strength matters more than polarity."),
        ("How many structural isomers does C₅H₁₂ have?", "3", ["2", "4", "5"], "Pentane, 2-methylbutane and 2,2-dimethylpropane."),
        ("How many structural isomers does C₄H₁₀ have?", "2", ["1", "3", "4"], "Butane and methylpropane."),
        ("What is a homologous series?", "compounds with the same functional group and general formula", ["compounds with the same molecular formula", "polymers made from one monomer", "compounds with the same M<sub>r</sub>"], "Each member differs by CH₂."),
        ("Which pollutant forms from incomplete combustion?", "carbon monoxide", ["nitrogen", "water", "oxygen"], "Not enough oxygen gives CO and soot."),
        ("How do catalytic converters remove carbon monoxide and NO?", "2CO + 2NO → 2CO₂ + N₂", ["CO + H₂O → CO₂ + H₂", "NO + O₂ → NO₃", "CO → C + O"], "A platinum or rhodium catalyst is used."),
        ("What is the nucleophile when a halogenoalkane reacts with KCN in ethanol?", "CN⁻", ["K⁺", "C₂H₅OH", "OH⁻"], "The product is a nitrile with one more carbon atom."),
        ("What forms when 1-bromopropane is warmed with excess ethanolic ammonia?", "propylamine", ["propan-1-ol", "propene", "propanenitrile"], "NH₃ acts as a nucleophile; excess limits further substitution."),
        ("In free-radical substitution, which step makes two radicals from one molecule?", "initiation", ["propagation", "termination", "elimination"], "Cl₂ → 2Cl• in UV light."),
        ("Which step of free-radical substitution removes radicals?", "termination", ["initiation", "propagation", "addition"], "Two radicals join, for example Cl• + Cl• → Cl₂."),
        ("Why are CFCs harmful to the ozone layer?", "UV light makes chlorine radicals that break down ozone", ["they absorb oxygen", "they are greenhouse gases only", "they react with nitrogen"], "One Cl• can destroy thousands of O₃ molecules."),
        ("What is the repeating unit of poly(ethene)?", "–CH₂–CH₂–", ["–CH=CH–", "–CH₂–", "–C₂H₆–"], "The C=C opens up to join the monomers."),
        ("Why are addition polymers like poly(propene) hard to dispose of?", "they are unreactive and not biodegradable", ["they dissolve in water", "they are too reactive", "they contain metals"], "They are saturated with strong non-polar bonds."),
        ("What is a carbocation?", "an ion with a positively charged carbon atom", ["a carbon with a lone pair", "a free radical", "a negatively charged carbon"], "Formed in electrophilic addition."),
        ("Which carbocation is the most stable?", "a tertiary carbocation", ["a primary carbocation", "a secondary carbocation", "a methyl carbocation"], "Alkyl groups push electrons towards the positive carbon."),
        ("Which alcohol forms a carboxylic acid when heated under reflux with excess acidified dichromate?", "ethanol", ["propan-2-ol", "2-methylpropan-2-ol", "cyclohexanol"], "Primary alcohols are oxidised to aldehydes and then acids."),
        ("What is made when an alcohol is dehydrated with hot concentrated phosphoric acid?", "an alkene", ["an aldehyde", "a ketone", "a halogenoalkane"], "Water is eliminated.")]


# =================================================================== Year 13: thermodynamics and kinetics
def c_gibbs(k=None):
    k = k or ch(["G", "T", "feas"])
    dH = ch([-180, -120, -92, -57, -46, 35, 58, 92, 117, 178, 206])
    dS = ch([-200, -160, -120, -90, 85, 120, 160, 175, 200, 250])
    T = ch([298, 350, 400, 500, 800, 1000, 1200])
    G = dH - T * dS / 1000
    if k == "G":
        return nq("For a reaction ΔH = %d kJ mol⁻¹ and ΔS = %d J K⁻¹ mol⁻¹. Calculate ΔG at %d K." % (dH, dS, T), G, [dH - T * dS, dH + T * dS / 1000, dH * 1000 - T * dS], " kJ mol⁻¹",
                  "ΔG = ΔH − TΔS = %d − %d × (%s) = <b>%s kJ mol⁻¹</b>. Change ΔS into kJ K⁻¹ mol⁻¹ first." % (dH, T, nf(dS / 1000), nf(G)))
    if k == "T":
        if dH * dS <= 0:
            return None
        Tm = dH * 1000 / dS
        return nq("For a reaction ΔH = %d kJ mol⁻¹ and ΔS = %d J K⁻¹ mol⁻¹. Calculate the temperature at which ΔG = 0." % (dH, dS), Tm, [dH / dS, dS / dH * 1000, dH * dS], " K",
                  "T = ΔH/ΔS = %d000 ÷ %d = <b>%s K</b>." % (dH, dS, nf(Tm)))
    feas = G <= 0
    return tq("For a reaction ΔH = %d kJ mol⁻¹ and ΔS = %d J K⁻¹ mol⁻¹. Is it feasible at %d K?" % (dH, dS, T), "yes, because ΔG is negative" if feas else "no, because ΔG is positive",
              ["yes, because ΔG is negative", "no, because ΔG is positive", "yes, because ΔH is negative", "no, because ΔS is negative"],
              "ΔG = %s kJ mol⁻¹. A reaction is feasible when ΔG ≤ 0." % nf(G))


SVAL = [("CaCO3 → CaO + CO2", {"CaCO3": 92.9, "CaO": 39.7, "CO2": 213.6}, {"CaCO3": 1}, {"CaO": 1, "CO2": 1}),
        ("N2 + 3H2 → 2NH3", {"N2": 191.6, "H2": 130.6, "NH3": 192.3}, {"N2": 1, "H2": 3}, {"NH3": 2}),
        ("2SO2 + O2 → 2SO3", {"SO2": 248.1, "O2": 205.0, "SO3": 256.6}, {"SO2": 2, "O2": 1}, {"SO3": 2}),
        ("CH4 + 2O2 → CO2 + 2H2O", {"CH4": 186.2, "O2": 205.0, "CO2": 213.6, "H2O": 69.9}, {"CH4": 1, "O2": 2}, {"CO2": 1, "H2O": 2}),
        ("H2 + Cl2 → 2HCl", {"H2": 130.6, "Cl2": 223.0, "HCl": 186.8}, {"H2": 1, "Cl2": 1}, {"HCl": 2}),
        ("C2H4 + H2 → C2H6", {"C2H4": 219.5, "H2": 130.6, "C2H6": 229.5}, {"C2H4": 1, "H2": 1}, {"C2H6": 1}),
        ("N2O4 → 2NO2", {"N2O4": 304.2, "NO2": 240.0}, {"N2O4": 1}, {"NO2": 2}),
        ("MgCO3 → MgO + CO2", {"MgCO3": 65.7, "MgO": 26.9, "CO2": 213.6}, {"MgCO3": 1}, {"MgO": 1, "CO2": 1})]


SIGN = [("ice melting", "positive", "A liquid is more disordered than a solid."), ("steam condensing to water", "negative", "A gas becomes a liquid: less disorder."),
        ("CaCO₃(s) → CaO(s) + CO₂(g)", "positive", "A gas is made from a solid."), ("N₂(g) + 3H₂(g) → 2NH₃(g)", "negative", "4 moles of gas become 2."),
        ("2SO₂(g) + O₂(g) → 2SO₃(g)", "negative", "3 moles of gas become 2."), ("N₂O₄(g) → 2NO₂(g)", "positive", "1 mole of gas becomes 2."),
        ("sodium chloride dissolving in water", "positive", "The ions spread out through the solution."), ("2H₂(g) + O₂(g) → 2H₂O(l)", "negative", "3 moles of gas become a liquid."),
        ("C₂H₄(g) + H₂(g) → C₂H₆(g)", "negative", "2 moles of gas become 1."), ("2H₂O₂(l) → 2H₂O(l) + O₂(g)", "positive", "A gas is produced from a liquid."),
        ("iodine subliming", "positive", "A solid becomes a gas."), ("Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)", "positive", "A gas is produced."),
        ("NH₃(g) + HCl(g) → NH₄Cl(s)", "negative", "2 moles of gas become a solid."), ("PCl₅(g) → PCl₃(g) + Cl₂(g)", "positive", "1 mole of gas becomes 2.")]


def c_entropy(k=None):
    k = k or ch(["calc", "sign"])
    if k == "sign":
        q, a, e = ch(SIGN)
        return tq("Is ΔS positive or negative for %s?" % q, a, [x for x in ["positive", "negative", "zero", "it cannot be predicted"] if x != a], e)
    eq, data, rs, ps = ch(SVAL)
    g = lambda side: sum(n * data[s] for s, n in side.items())
    dS = g(ps) - g(rs)
    tab = ", ".join("%s %s" % (fm(s), nf(v, 4)) for s, v in data.items())
    return nq("Standard entropies (J K⁻¹ mol⁻¹): %s. Calculate ΔS for %s." % (tab, fm(eq)), dS, [g(rs) - g(ps), sum(data[s] for s in ps) - sum(data[s] for s in rs), g(ps) + g(rs), g(ps), dS / 1000], " J K⁻¹ mol⁻¹",
              "ΔS = ΣS(products) − ΣS(reactants) = %s − %s = <b>%s J K⁻¹ mol⁻¹</b>." % (nf(g(ps), 4), nf(g(rs), 4), nf(dS, 4)), sf=4)


def c_order(k=None):
    k = k or ch(["order", "k", "units", "rate"])
    m, n = ch([0, 1, 2]), ch([0, 1, 2])
    if k == "order":
        f = ch([2, 3, 4])
        o = ch([0, 1, 2])
        mult = f ** o
        r0 = ch([1.2, 2.0, 2.5, 3.6, 4.8, 6.0]) * 1e-4
        return nq("When [A] is multiplied by %d (other concentrations fixed), the initial rate goes from %s to %s mol dm⁻³ s⁻¹. What is the order with respect to A?" % (f, nf(r0), nf(r0 * mult)), o,
                  [(o + 1) % 3, (o + 2) % 3, f], "", "Rate × %s when [A] × %d: %d<sup>%d</sup> = %s, so order = <b>%d</b>." % (nf(mult), f, f, o, nf(mult), o))
    a, b = ch([0.10, 0.20, 0.25, 0.40, 0.50]), ch([0.10, 0.20, 0.30, 0.50])
    kk = ch([0.012, 0.025, 0.040, 0.15, 0.36, 1.5, 2.4])
    rate = kk * a ** m * b ** n
    tot = m + n
    units = {0: "mol dm⁻³ s⁻¹", 1: "s⁻¹", 2: "mol⁻¹ dm³ s⁻¹", 3: "mol⁻² dm⁶ s⁻¹", 4: "mol⁻³ dm⁹ s⁻¹"}
    eq = "rate = k" + ("[A]" if m == 1 else "[A]²" if m == 2 else "") + ("[B]" if n == 1 else "[B]²" if n == 2 else "")
    if k == "units":
        return tq("What are the units of k for %s?" % eq, units[tot], [units[(tot + 1) % 5], units[(tot + 2) % 5], units[(tot + 4) % 5]], "Overall order %d. Units = mol dm⁻³ s⁻¹ ÷ (mol dm⁻³)<sup>%d</sup>." % (tot, tot))
    if tot == 0:
        return None
    if k == "k":
        return nq("%s. When [A] = %s and [B] = %s mol dm⁻³ the rate is %s mol dm⁻³ s⁻¹. Calculate k." % (eq, nf(a, 2), nf(b, 2), nf(rate)), kk, [rate / (a * b), rate * a * b, rate / a], " " + units[tot],
                  "k = rate ÷ concentrations with their powers = <b>%s</b>." % nf(kk))
    a2 = a * ch([2, 3])
    return nq("%s with k = %s %s. Calculate the rate when [A] = %s and [B] = %s mol dm⁻³." % (eq, nf(kk), units[tot], nf(a2, 2), nf(b, 2)), kk * a2 ** m * b ** n,
              [kk * a2 * b, kk * (a2 * b) ** 2, kk * a2 ** (m + 1) * b ** n], " mol dm⁻³ s⁻¹", "Substitute: rate = <b>%s mol dm⁻³ s⁻¹</b>." % nf(kk * a2 ** m * b ** n))


def c_arr(k=None):
    Ea = ch([40, 50, 60, 75, 80, 90, 100, 120])
    A = ch([1e10, 2e10, 5e11, 1e12, 3e13])
    T = ch([298, 310, 350, 400, 500])
    kk = A * math.exp(-Ea * 1000 / (RG * T))
    k = k or ch(["k", "ln"])
    if k == "ln":
        return nq("For a reaction E<sub>a</sub> = %d kJ mol⁻¹. Calculate the value of E<sub>a</sub>/RT at %d K (R = 8.31 J K⁻¹ mol⁻¹)." % (Ea, T), Ea * 1000 / (RG * T), [Ea / (RG * T), Ea * 1000 * RG / T, RG * T / (Ea * 1000)], "",
                  "E<sub>a</sub>/RT = %d000 ÷ (8.31 × %d) = <b>%s</b>." % (Ea, T, nf(Ea * 1000 / (RG * T))))
    return nq("Use k = Ae<sup>−Ea/RT</sup> to find k when A = %s s⁻¹, E<sub>a</sub> = %d kJ mol⁻¹ and T = %d K." % (nf(A), Ea, T), kk, [A * math.exp(-Ea / (RG * T)), A * math.exp(Ea * 1000 / (RG * T)) if Ea * 1000 / (RG * T) < 600 else None, kk * 10, A * math.exp(-Ea * 1000 / (RG * (T - 273)))], " s⁻¹",
              "Ea/RT = %s; k = %s × e<sup>−%s</sup> = <b>%s s⁻¹</b>." % (nf(Ea * 1000 / (RG * T)), nf(A), nf(Ea * 1000 / (RG * T)), nf(kk)))


def c_kp(k=None):
    eq, rs, ps, dH, name = ch(EQS[:2] + EQS[3:6] + EQS[7:])
    tot = ch([100, 150, 200, 250, 500, 1000])
    mol = {s: ch([0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0]) for s in list(rs) + list(ps)}
    N = sum(mol.values())
    pp = {s: mol[s] / N * tot for s in mol}
    k = k or ch(["pp", "kp"])
    if k == "pp":
        s = ch(list(mol))
        return nq("An equilibrium mixture for %s at %d kPa contains %s. Calculate the partial pressure of %s." % (fm(eq), tot, ", ".join("%s mol %s" % (nf(mol[x], 2), fm(x)) for x in mol), fm(s)), pp[s],
                  [mol[s] * tot, mol[s] / N, tot / len(mol)], " kPa", "Mole fraction = %s ÷ %s; × %d kPa = <b>%s kPa</b>." % (nf(mol[s], 2), nf(N, 3), tot, nf(pp[s])))
    val = 1.0
    for s, n in ps.items():
        val *= pp[s] ** n
    for s, n in rs.items():
        val /= pp[s] ** n
    lin = 1.0
    for s in ps:
        lin *= pp[s]
    for s in rs:
        lin /= pp[s]
    data = ", ".join("p(%s) = %s kPa" % (fm(s), nf(pp[s])) for s in pp)
    return nq("At equilibrium for %s: %s. Calculate K<sub>p</sub> (in kPa units)." % (fm(eq), data), val, [lin, 1 / val, val * tot], "", "K<sub>p</sub> = products ÷ reactants, each partial pressure raised to its coefficient: <b>%s</b>." % nf(val))


# =================================================================== Year 13: acids, bases and electrode potentials
def c_ph(k=None):
    k = k or ch(["strong", "H", "base", "dil", "weak", "ka", "buffer"])
    if k == "strong":
        c = ch([0.001, 0.0025, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.0])
        di = ch([1, 1, 2])
        acid = "HCl" if di == 1 else "H2SO4"
        if di == 2 and c > 0.5:
            return None
        pH = -math.log10(c * di)
        return nq("Calculate the pH of %s mol dm⁻³ %s (assume it is fully dissociated)." % (nf(c), fm(acid)), pH, [-math.log10(c) if di == 2 else -math.log10(c * 2), math.log10(c * di), -math.log(c * di)], "",
                  "[H⁺] = %s mol dm⁻³; pH = −log[H⁺] = <b>%s</b>." % (nf(c * di), nf(pH)), sf=3)
    if k == "H":
        pH = ch([1.5, 2.3, 2.9, 3.4, 4.2, 5.7, 8.6, 9.3, 11.2, 12.5])
        return nq("A solution has a pH of %s. Calculate [H⁺]." % nf(pH, 2), 10 ** -pH, [10 ** pH, pH / 10, 10 ** -(14 - pH)], " mol dm⁻³", "[H⁺] = 10<sup>−pH</sup> = <b>%s mol dm⁻³</b>." % nf(10 ** -pH))
    if k == "base":
        c = ch([0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25, 0.50])
        b, n = ch([("NaOH", 1), ("KOH", 1), ("Ba(OH)2", 2)])
        H = 1e-14 / (c * n)
        return nq("Calculate the pH of %s mol dm⁻³ %s at 298 K (K<sub>w</sub> = 1.00 × 10<sup>−14</sup> mol² dm⁻⁶)." % (nf(c), fm(b)), -math.log10(H), [-math.log10(c * n), -math.log10(1e-14 / c) if n == 2 else 14 + math.log10(c * 2), 14 - math.log10(c * n)], "",
                  "[OH⁻] = %s; [H⁺] = K<sub>w</sub>/[OH⁻] = %s; pH = <b>%s</b>." % (nf(c * n), nf(H), nf(-math.log10(H))))
    if k == "dil":
        c, f = ch([0.1, 0.05, 0.2, 0.01]), ch([10, 100, 4, 5])
        return nq("%s mol dm⁻³ HCl is diluted %d times (for example 10 cm³ made up to %d cm³). Calculate the new pH." % (nf(c), f, 10 * f), -math.log10(c / f), [-math.log10(c) * f, -math.log10(c) + f, -math.log10(c * f)], "",
                  "New [H⁺] = %s; pH = <b>%s</b>." % (nf(c / f), nf(-math.log10(c / f))))
    acid, Ka = ch([("ethanoic acid", 1.74e-5), ("methanoic acid", 1.78e-4), ("propanoic acid", 1.35e-5), ("benzoic acid", 6.31e-5), ("hydrofluoric acid", 6.76e-4), ("butanoic acid", 1.51e-5), ("chloroethanoic acid", 1.38e-3), ("nitrous acid", 4.0e-4), ("hypochlorous acid", 3.0e-8)])
    c = ch([0.010, 0.020, 0.050, 0.10, 0.20, 0.25, 0.50, 1.0])
    if k == "weak":
        H = math.sqrt(Ka * c)
        return nq("Calculate the pH of %s mol dm⁻³ %s (K<sub>a</sub> = %s mol dm⁻³)." % (nf(c, 2), acid, nf(Ka)), -math.log10(H), [-math.log10(c), -math.log10(Ka * c), -math.log10(Ka)], "",
                  "[H⁺] = √(K<sub>a</sub> × c) = %s; pH = <b>%s</b>." % (nf(H), nf(-math.log10(H))))
    if k == "kph":
        H = math.sqrt(Ka * c)
        pH = round(-math.log10(H), 2)
        H = 10 ** -pH
        return nq("A %s mol dm⁻³ solution of %s has a pH of %s. Calculate K<sub>a</sub>." % (nf(c, 2), acid, nf(pH, 3)), H * H / c, [H / c, H * H, H * c], " mol dm⁻³",
                  "[H⁺] = 10<sup>−%s</sup> = %s; K<sub>a</sub> = [H⁺]²/[HA] = <b>%s mol dm⁻³</b>." % (nf(pH, 3), nf(H), nf(H * H / c)))
    if k == "ka":
        return nq("The K<sub>a</sub> of %s is %s mol dm⁻³. Calculate its pK<sub>a</sub>." % (acid, nf(Ka)), -math.log10(Ka), [math.log10(Ka), -math.log(Ka), 1 / Ka], "", "pK<sub>a</sub> = −log K<sub>a</sub> = <b>%s</b>." % nf(-math.log10(Ka)))
    ra, rb = ch([0.10, 0.20, 0.25, 0.50]), ch([0.10, 0.15, 0.20, 0.40])
    H = Ka * ra / rb
    return nq("A buffer contains %s mol dm⁻³ %s and %s mol dm⁻³ of its sodium salt (K<sub>a</sub> = %s mol dm⁻³). Calculate its pH." % (nf(ra, 2), acid, nf(rb, 2), nf(Ka)), -math.log10(H),
              [-math.log10(Ka * rb / ra), -math.log10(math.sqrt(Ka * ra)), -math.log10(Ka)], "", "[H⁺] = K<sub>a</sub>[HA]/[A⁻] = %s; pH = <b>%s</b>." % (nf(H), nf(-math.log10(H))))


EO = [("Mg²⁺/Mg", -2.37, "Mg"), ("Al³⁺/Al", -1.66, "Al"), ("Zn²⁺/Zn", -0.76, "Zn"), ("Fe²⁺/Fe", -0.44, "Fe"), ("Ni²⁺/Ni", -0.25, "Ni"), ("Pb²⁺/Pb", -0.13, "Pb"),
      ("2H⁺/H₂", 0.00, "H₂"), ("Cu²⁺/Cu", 0.34, "Cu"), ("I₂/2I⁻", 0.54, "I⁻"), ("Fe³⁺/Fe²⁺", 0.77, "Fe²⁺"), ("Ag⁺/Ag", 0.80, "Ag"), ("Br₂/2Br⁻", 1.09, "Br⁻"), ("Cl₂/2Cl⁻", 1.36, "Cl⁻"), ("MnO₄⁻/Mn²⁺", 1.51, "Mn²⁺")]


def c_ecell(k=None):
    a, b = sorted(R.sample(EO, 2), key=lambda x: x[1])
    k = k or ch(["E", "neg", "feas"])
    E = b[1] - a[1]
    if k == "E":
        return nq("Calculate the standard e.m.f. of a cell made from the %s (E° = %s V) and %s (E° = %s V) half-cells." % (a[0], nf(a[1]), b[0], nf(b[1])), E, [a[1] + b[1], -E, abs(a[1]) + abs(b[1]) if a[1] * b[1] < 0 else b[1] * 2 - a[1]], " V",
                  "E°<sub>cell</sub> = E°(more positive) − E°(more negative) = %s − (%s) = <b>%s V</b>." % (nf(b[1]), nf(a[1]), nf(E)))
    if k == "neg":
        return tq("A cell is made from the %s (E° = %s V) and %s (E° = %s V) half-cells. Which half-cell is the negative electrode?" % (a[0], nf(a[1]), b[0], nf(b[1])), "the %s half-cell" % a[0],
                  ["the %s half-cell" % b[0], "both are positive", "the salt bridge"], "The more negative E° is the negative electrode, where oxidation happens.")
    ok = ch([True, False])
    ox, red = (b, a) if ok else (a, b)
    return tq("Use E° values (%s: %s V; %s: %s V). Is it feasible for the oxidised form in %s to oxidise the reduced form in %s under standard conditions?" % (a[0], nf(a[1]), b[0], nf(b[1]), ox[0], red[0]),
              "yes" if ok else "no", ["no" if ok else "yes", "only with a catalyst", "only if heated"], "A reaction is feasible when the oxidising agent's E° is more positive than the reducing agent's (E°<sub>cell</sub> > 0).")


# =================================================================== Year 13: transition metals
CPLX = [("[Cu(H2O)6]^2+", 2, 6, "octahedral", "blue"), ("[CuCl4]^2-", 2, 4, "tetrahedral", "yellow"), ("[Fe(CN)6]^3-", 3, 6, "octahedral", "orange-red"),
        ("[Ag(NH3)2]^+", 1, 2, "linear", "colourless"), ("[Co(NH3)6]^3+", 3, 6, "octahedral", "yellow-brown"), ("[Cr(H2O)6]^3+", 3, 6, "octahedral", "violet"),
        ("[Fe(H2O)6]^2+", 2, 6, "octahedral", "pale green"), ("[Fe(H2O)6]^3+", 3, 6, "octahedral", "yellow-brown"), ("[CoCl4]^2-", 2, 4, "tetrahedral", "blue"),
        ("[Co(H2O)6]^2+", 2, 6, "octahedral", "pink"), ("[Cu(NH3)4(H2O)2]^2+", 2, 6, "octahedral", "deep blue"), ("[Cr(OH)6]^3-", 3, 6, "octahedral", "green"),
        ("[Pt(NH3)2Cl2]", 2, 4, "square planar", "pale yellow"), ("[Ni(H2O)6]^2+", 2, 6, "octahedral", "green"), ("[Mn(H2O)6]^2+", 2, 6, "octahedral", "very pale pink"),
        ("[Fe(CN)6]^4-", 2, 6, "octahedral", "yellow"), ("[Co(NH3)6]^2+", 2, 6, "octahedral", "straw-coloured"), ("[Ni(NH3)6]^2+", 2, 6, "octahedral", "blue-violet"),
        ("[Cr(NH3)6]^3+", 3, 6, "octahedral", "purple"), ("[Ag(S2O3)2]^3-", 1, 2, "linear", "colourless"), ("[Al(H2O)6]^3+", 3, 6, "octahedral", "colourless"),
        ("[Cu(en)3]^2+", 2, 6, "octahedral", "violet-blue"), ("[Fe(C2O4)3]^3-", 3, 6, "octahedral", "green"), ("[Cu(EDTA)]^2-", 2, 6, "octahedral", "blue"), ("[Zn(NH3)4]^2+", 2, 4, "tetrahedral", "colourless")]


def c_tm(k=None):
    f, ox, cn, sh, col = ch(CPLX)
    k = k or ch(["ox", "cn", "shape", "col", "lig"])
    if k == "lig":
        lig = re.findall(r"\(([A-Za-z0-9]+)\)(\d*)", f) or re.findall(r"(Cl)(\d)", f)
        if not lig or len(lig) > 1 or ("(" in f and "Cl" in f):
            return None
        nm, num = lig[0]
        num = int(num or 1)
        dent = {"en": 2, "C2O4": 2, "EDTA": 6, "S2O3": 1}.get(nm, 1)
        return nq("How many ligands surround the metal ion in %s?" % fm(f), num, [cn if cn != num else cn + 2, num + 2, num * 2 if num * 2 != cn else num + 1, max(1, num - 1)], "",
                  "%s has %d %s ligand%s, each forming %d co-ordinate bond%s (co-ordination number %d)." % (fm(f), num, fm(nm), "" if num == 1 else "s", dent, "" if dent == 1 else "s", cn))
    metal = re.match(r"\[([A-Z][a-z]?)", f).group(1)
    s = lambda v: "+%d" % v
    if k == "ox":
        return tq("What is the oxidation state of %s in %s?" % (metal, fm(f)), s(ox), [s(ox + 1), s(ox + 2) if ox < 5 else "+1", "0" if ox else "+2"], "Water and ammonia are neutral ligands; Cl⁻, OH⁻ and CN⁻ are −1.")
    if k == "cn":
        return nq("What is the co-ordination number of %s in %s?" % (metal, fm(f)), cn, [cn - 2 if cn > 2 else 3, cn + 2, ox], "", "Count the co-ordinate bonds to the metal ion: <b>%d</b>." % cn)
    if k == "shape":
        return tq("What is the shape of %s?" % fm(f), sh, [x for x in ["octahedral", "tetrahedral", "square planar", "linear"] if x != sh], "Co-ordination number %d: %s." % (cn, sh))
    fam = lambda c: {"violet": "purple", "blue-violet": "purple", "violet-blue": "purple", "deep blue": "blue", "yellow-brown": "yellow", "pale yellow": "yellow", "straw-coloured": "yellow",
                     "pale green": "green", "very pale pink": "pink", "orange-red": "orange"}.get(c, c)
    cols = sorted({c[4] for c in CPLX if fam(c[4]) != fam(col) and not set(c[4].split('-') + c[4].split()) & set(col.split('-') + col.split())})
    return tq("What colour is %s in solution?" % fm(f), col, R.sample(cols, 3), "%s is %s." % (fm(f), col))


TMB = [("What is a transition metal?", "an element that can form at least one stable ion with a partially filled d sub-shell", ["any element in the d-block", "a metal that is magnetic", "a metal that forms only one ion"], "Zinc is in the d-block but Zn²⁺ is 3d¹⁰, so it is not a transition metal."),
       ("What is a ligand?", "a molecule or ion that forms a co-ordinate bond with a metal ion by donating a lone pair", ["a metal ion in a complex", "a type of catalyst", "a negative electrode"], "Examples: H₂O, NH₃, Cl⁻, CN⁻."),
       ("Why are transition metal complexes coloured?", "d electrons absorb visible light and move to a higher energy d orbital", ["the metal emits light", "the ligands are coloured", "the complexes contain carbon"], "The colour seen is the complementary colour."),
       ("What is a bidentate ligand?", "a ligand that forms two co-ordinate bonds to the metal ion", ["a ligand with two charges", "a pair of ligands", "a ligand with no lone pairs"], "Examples: ethane-1,2-diamine and ethanedioate."),
       ("Which ligand is hexadentate?", "EDTA⁴⁻", ["NH₃", "Cl⁻", "ethane-1,2-diamine"], "EDTA forms six co-ordinate bonds."),
       ("Why does the chelate effect happen?", "replacing monodentate ligands with multidentate ones increases the entropy", ["the bonds become ionic", "the enthalpy change is very large", "fewer particles form"], "More particles are released, so ΔS is positive."),
       ("What is the catalyst in the Contact process?", "vanadium(V) oxide", ["iron", "nickel", "platinum"], "V₂O₅ is reduced to V₂O₄ and then reoxidised."),
       ("What is the catalyst in the Haber process?", "iron", ["vanadium(V) oxide", "nickel", "manganese(IV) oxide"], "A heterogeneous catalyst."),
       ("Why do transition metals make good catalysts?", "they have variable oxidation states", ["they are very reactive", "they have full d sub-shells", "they are always liquids"], "They can pass electrons back and forth."),
       ("What happens when excess ammonia is added to [Cu(H₂O)₆]²⁺?", "a deep blue solution of [Cu(NH₃)₄(H₂O)₂]²⁺ forms", ["a white precipitate forms", "an orange solution forms", "nothing happens"], "First a pale blue precipitate, which dissolves in excess."),
       ("What forms when concentrated HCl is added to [Cu(H₂O)₆]²⁺?", "yellow [CuCl₄]²⁻", ["blue [Cu(NH₃)₄]²⁺", "a white precipitate", "green Cu(OH)₂"], "Cl⁻ is larger, so only four fit around Cu²⁺."),
       ("What is the colour change when MnO₄⁻ is reduced in a titration?", "purple to colourless", ["orange to green", "colourless to purple", "blue to yellow"], "MnO₄⁻ acts as its own indicator."),
       ("Which ion forms a green precipitate with NaOH that slowly turns brown in air?", "Fe²⁺", ["Fe³⁺", "Cu²⁺", "Al³⁺"], "Fe(OH)₂ is oxidised to Fe(OH)₃."),
       ("Which ion gives an orange-brown precipitate with NaOH?", "Fe³⁺", ["Fe²⁺", "Cu²⁺", "Co²⁺"], "Fe(OH)₃."),
       ("What is cisplatin used for?", "an anti-cancer drug", ["a fertiliser", "a catalyst for the Haber process", "a dye"], "It binds to DNA and stops cell division."),
       ("What is meant by a homogeneous catalyst?", "a catalyst in the same phase as the reactants", ["a catalyst that is a solid", "a catalyst that is used up", "a catalyst in a different phase"], "For example Fe²⁺ in the reaction of I⁻ with S₂O₈²⁻."),
       ("Why can Fe²⁺ catalyse the reaction between I⁻ and S₂O₈²⁻?", "it is oxidised to Fe³⁺ by S₂O₈²⁻ and then reduced back by I⁻", ["it gives the ions more energy", "it forms a precipitate", "it removes the products"], "Two steps between oppositely charged ions are faster than one between two negative ions."),
       ("Why does a catalyst poison reduce the efficiency of a heterogeneous catalyst?", "it is adsorbed onto the active sites and blocks them", ["it raises the activation energy of the reaction", "it reacts with the products", "it dissolves the catalyst"], "For example sulfur poisons the iron catalyst in the Haber process."),
       ("What is autocatalysis?", "a product of the reaction acts as a catalyst", ["the catalyst is used up", "the reaction needs no activation energy", "two catalysts work together"], "Mn²⁺ catalyses the reaction between MnO₄⁻ and C₂O₄²⁻."),
       ("Why does adding EDTA⁴⁻ to [Cu(H₂O)₆]²⁺ happen easily?", "one EDTA replaces six water molecules, increasing the entropy", ["EDTA is a stronger acid", "the copper is oxidised", "water is a bidentate ligand"], "1 particle + 1 particle → 7 particles.")]


def c_redox_titr(k=None):
    k = k or ch(["mn", "cr", "pct"])
    c = ch([0.010, 0.015, 0.020, 0.025, 0.050])
    V = ch([12.4, 15.6, 18.2, 20.5, 22.3, 24.8, 26.1])
    if k in ("mn", "pct"):
        n = c * V / 1000
        fe = 5 * n
        if k == "mn":
            return nq("%s cm³ of %s mol dm⁻³ KMnO₄ reacts with Fe²⁺ ions: MnO₄⁻ + 8H⁺ + 5Fe²⁺ → Mn²⁺ + 4H₂O + 5Fe³⁺. How many moles of Fe²⁺ reacted?" % (nf(V), nf(c, 2)), fe, [n, n / 5, c * V * 5], " mol",
                      "n(MnO₄⁻) = %s mol; × 5 = <b>%s mol</b>." % (nf(n), nf(fe)))
        mt = fe * 55.8 / ch([0.7, 0.8, 0.85, 0.9])
        return nq("A sample of impure iron wire of mass %s g is dissolved in acid. The Fe²⁺ reacts with %s cm³ of %s mol dm⁻³ KMnO₄ (1 MnO₄⁻ : 5 Fe²⁺). Calculate the percentage of iron by mass." % (nf(mt), nf(V), nf(c, 2)), fe * 55.8 / mt * 100,
                  [n * 55.8 / mt * 100, fe * 55.8 / mt, fe / mt * 100], "%", "n(Fe²⁺) = 5 × %s = %s mol; mass = %s g; %% = <b>%s%%</b>." % (nf(n), nf(fe), nf(fe * 55.8), nf(fe * 55.8 / mt * 100)))
    n = c * V / 1000
    return nq("%s cm³ of %s mol dm⁻³ K₂Cr₂O₇ reacts with Fe²⁺: Cr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 7H₂O + 6Fe³⁺. How many moles of Fe²⁺ reacted?" % (nf(V), nf(c, 2)), 6 * n, [n, 5 * n, 2 * n], " mol",
              "n(Cr₂O₇²⁻) = %s mol; × 6 = <b>%s mol</b>." % (nf(n), nf(6 * n)))


# =================================================================== Year 13: further organic chemistry and analysis
ACIDS = [(1, "methanoic acid", "methanoate", "HCOOH"), (2, "ethanoic acid", "ethanoate", "CH3COOH"), (3, "propanoic acid", "propanoate", "C2H5COOH"), (4, "butanoic acid", "butanoate", "C3H7COOH"), (5, "pentanoic acid", "pentanoate", "C4H9COOH")]
ALCS = [(1, "methanol", "methyl"), (2, "ethanol", "ethyl"), (3, "propan-1-ol", "propyl"), (4, "butan-1-ol", "butyl"), (5, "pentan-1-ol", "pentyl")]


def c_ester(k=None):
    a, al = ch(ACIDS), ch(ALCS)
    nm = "%s %s" % (al[2], a[2])
    wr = ["%s %s" % (ALCS[a[0] - 1][2], ACIDS[al[0] - 1][2]), "%s %s" % (al[2], ACIDS[a[0] % 5][2]), "%s %s" % (ALCS[al[0] % 5][2], a[2])]
    k = k or ch(["name", "from"])
    if k == "name":
        return tq("What is the name of the ester made from %s and %s?" % (a[1], al[1]), nm, wr, "The alcohol part is named first (%s), then the acid part (%s)." % (al[2], a[2]))
    return tq("%s is hydrolysed. Which acid and alcohol form?" % nm.capitalize(), "%s and %s" % (a[1], al[1]),
              ["%s and %s" % (ACIDS[al[0] - 1][1], ALCS[a[0] - 1][1]), "%s and %s" % (ACIDS[a[0] % 5][1], al[1]), "%s and %s" % (a[1], ALCS[al[0] % 5][1])], "Split at the C–O bond: the -oate part gives the acid, the -yl part gives the alcohol.")


NMR = [("ethanol, CH₃CH₂OH", 3, "triplet (CH₃), quartet (CH₂), singlet (OH)"), ("propanone, CH₃COCH₃", 1, "one singlet"), ("ethanal, CH₃CHO", 2, "doublet (CH₃) and quartet (CHO)"),
       ("methyl ethanoate, CH₃COOCH₃", 2, "two singlets"), ("propan-2-ol, (CH₃)₂CHOH", 3, "doublet, septet and singlet"), ("1-chloropropane, CH₃CH₂CH₂Cl", 3, "triplet, sextet and triplet"),
       ("2-chloropropane, CH₃CHClCH₃", 2, "doublet and septet"), ("ethyl ethanoate, CH₃COOCH₂CH₃", 3, "singlet, quartet and triplet"), ("methylpropane, (CH₃)₃CH", 2, "doublet and multiplet"),
       ("butanone, CH₃COCH₂CH₃", 3, "singlet, quartet and triplet"), ("propanal, CH₃CH₂CHO", 3, "triplet, multiplet and triplet"), ("benzene, C₆H₆", 1, "one singlet"),
       ("1,2-dibromoethane, BrCH₂CH₂Br", 1, "one singlet"), ("methanol, CH₃OH", 2, "two singlets"), ("chloroethane, CH₃CH₂Cl", 2, "triplet and quartet"),
       ("ethanoic acid, CH₃COOH", 2, "two singlets"), ("propanoic acid, CH₃CH₂COOH", 3, "triplet, quartet and singlet"), ("2-methylpropan-2-ol, (CH₃)₃COH", 2, "two singlets"),
       ("1,1-dichloroethane, CH₃CHCl₂", 2, "doublet and quartet"), ("pentan-3-one, CH₃CH₂COCH₂CH₃", 2, "triplet and quartet"), ("methyl propanoate, CH₃CH₂COOCH₃", 3, "triplet, quartet and singlet"),
       ("bromoethane, CH₃CH₂Br", 2, "triplet and quartet"), ("2-bromopropane, CH₃CHBrCH₃", 2, "doublet and septet"), ("butane, CH₃CH₂CH₂CH₃", 2, "triplet and sextet")]


def c_nmr(k=None):
    nm, env, split = ch(NMR)
    k = k or ch(["env", "split", "n1"])
    if k == "env":
        return nq("How many peaks are there in the ¹H NMR spectrum of %s?" % nm, env, [env + 1, env - 1 if env > 1 else 4, sum(int(c) for c in re.findall(r"H[₀-₉]", nm) and ["2"] or ["5"]) + env], "",
                  "Count the different hydrogen environments: <b>%d</b> (%s)." % (env, split))
    if k == "split":
        if env == 1 and "singlet" in split:
            return None
        others = [x[2] for x in NMR if x[2] != split and x[1] == env] + [x[2] for x in NMR if x[2] != split]
        return tq("Which splitting pattern is seen in the ¹H NMR spectrum of %s?" % nm, split, others, "Use the n + 1 rule: a peak splits into n + 1 lines where n is the number of H atoms on the adjacent carbon(s).")
    n = ch([0, 1, 2, 3, 6])
    pat = {0: "singlet", 1: "doublet", 2: "triplet", 3: "quartet", 6: "septet"}
    return tq("In ¹H NMR, a group of protons has %d hydrogen atom%s on the adjacent carbon atoms. What is its splitting pattern?" % (n, "" if n == 1 else "s"), pat[n], [v for kk, v in pat.items() if kk != n], "n + 1 rule: %d + 1 = %d lines." % (n, n + 1))


ORG = [("CH3CH2OH", "ethanol"), ("CH3COCH3", "propanone"), ("CH3CHO", "ethanal"), ("C6H6", "benzene"), ("CH3COOH", "ethanoic acid"), ("C3H8", "propane"),
       ("C6H5NO2", "nitrobenzene"), ("C6H5NH2", "phenylamine"), ("CH3COOC2H5", "ethyl ethanoate"), ("C3H7OH", "propan-1-ol"), ("C4H10", "butane"), ("C2H5NH2", "ethylamine"),
       ("CH3CH2CHO", "propanal"), ("C6H5OH", "phenol"), ("CH3CONH2", "ethanamide")]


def c_anal(k=None):
    k = k or ch(["ms", "rf", "ir"])
    if k == "ms":
        f, nm = ch(ORG)
        M = mr(f)
        return nq("At what m/z value is the molecular ion peak of %s (%s)?" % (nm, fm(f)), M, [M - 15, M + 1, M - 17], "", "The M⁺ peak is at the M<sub>r</sub>: <b>%s</b>." % nf(M, 4), sf=4)
    if k == "rf":
        d, s = ch([1.2, 2.4, 3.1, 3.6, 4.5, 5.2, 6.0]), ch([6.5, 7.0, 8.0, 9.0, 10.0])
        return nq("In thin-layer chromatography a spot moves %s cm and the solvent front moves %s cm. Calculate the R<sub>f</sub> value." % (nf(d, 2), nf(s, 2)), d / s, [s / d, s - d, d / (s + d)], "",
                  "R<sub>f</sub> = distance moved by spot ÷ distance moved by solvent = <b>%s</b>." % nf(d / s))
    bond, rng, ex = ch([("O–H (alcohols)", "3230–3550 cm⁻¹", "ethanol"), ("O–H (acids)", "2500–3000 cm⁻¹", "ethanoic acid"), ("C=O", "1680–1750 cm⁻¹", "propanone"),
                        ("N–H (amines)", "3300–3500 cm⁻¹", "ethylamine"), ("C–H", "2850–3300 cm⁻¹", "ethane"), ("C≡N", "2220–2260 cm⁻¹", "propanenitrile"), ("C=C", "1620–1680 cm⁻¹", "ethene")])
    if R.random() < 0.5:
        return tq("A compound such as %s shows a strong infrared absorption at %s. Which bond causes it?" % (ex, rng), bond,
                  [b for b in ["O–H (alcohols)", "O–H (acids)", "C=O", "N–H (amines)", "C–H", "C≡N", "C=C"] if b != bond and b[:3] != bond[:3]] or ["C–O"], "Use the data sheet of characteristic infrared absorptions.")
    return tq("In an infrared spectrum, which absorption range shows the %s bond (for example in %s)?" % (bond, ex), rng,
              [r for r in ["3230–3550 cm⁻¹", "2500–3000 cm⁻¹", "1680–1750 cm⁻¹", "2220–2260 cm⁻¹", "1620–1680 cm⁻¹", "1000–1300 cm⁻¹"] if r != rng], "Use the data sheet of characteristic infrared absorptions.")


ORG2 = [("Which reagent distinguishes an aldehyde from a ketone?", "Tollens' reagent (silver mirror with the aldehyde)", ["bromine water", "2,4-DNPH", "sodium carbonate"], "Aldehydes are oxidised; ketones are not."),
        ("What does 2,4-dinitrophenylhydrazine (2,4-DNPH) detect?", "a carbonyl group (orange precipitate)", ["a C=C bond", "an OH group", "a carboxylic acid only"], "Both aldehydes and ketones react."),
        ("What is formed when an aldehyde is reduced with NaBH₄?", "a primary alcohol", ["a secondary alcohol", "a carboxylic acid", "a ketone"], "H⁻ (hydride) attacks the carbonyl carbon."),
        ("What mechanism happens when HCN (from KCN and acid) reacts with ethanal?", "nucleophilic addition", ["electrophilic addition", "nucleophilic substitution", "electrophilic substitution"], "CN⁻ attacks the δ+ carbonyl carbon."),
        ("Why does benzene react by substitution rather than addition?", "substitution keeps the stable delocalised ring of electrons", ["benzene has no C=C bonds", "addition is too fast", "benzene is not reactive at all"], "The delocalised π system gives extra stability."),
        ("What is the electrophile in the nitration of benzene?", "NO₂⁺", ["NO₃⁻", "HNO₃", "H₂SO₄"], "Made from concentrated nitric and sulfuric acids."),
        ("What catalyst is used in Friedel–Crafts acylation?", "aluminium chloride", ["iron", "sulfuric acid", "nickel"], "AlCl₃ generates the acylium ion RCO⁺."),
        ("Why is phenylamine a weaker base than ethylamine?", "the nitrogen lone pair is delocalised into the benzene ring", ["phenylamine has no lone pair", "ethylamine is an acid", "phenylamine is ionic"], "The lone pair is less available to accept a proton."),
        ("What type of polymer is nylon-6,6?", "a polyamide (condensation polymer)", ["a polyester", "an addition polymer", "a polyalkene"], "Made from a diamine and a dicarboxylic acid with loss of water."),
        ("What type of polymer is Terylene (PET)?", "a polyester (condensation polymer)", ["a polyamide", "an addition polymer", "a protein"], "Made from a diol and a dicarboxylic acid."),
        ("Why are polyesters biodegradable while polyalkenes are not?", "their ester links can be hydrolysed", ["they contain no carbon", "they are ionic", "they dissolve in water"], "Polyalkenes have only non-polar C–C and C–H bonds."),
        ("What is the product when an acyl chloride reacts with water?", "a carboxylic acid and HCl", ["an ester", "an amide", "an alcohol and Cl₂"], "Nucleophilic addition–elimination."),
        ("What is the product when ethanoyl chloride reacts with ammonia?", "ethanamide", ["ethylamine", "ethanoic acid", "ethyl ethanoate"], "Addition–elimination gives an amide."),
        ("What type of isomerism do amino acids (except glycine) show?", "optical isomerism", ["E/Z isomerism", "structural isomerism only", "no isomerism"], "They have a chiral carbon."),
        ("What is a racemic mixture?", "equal amounts of two enantiomers, so it does not rotate plane-polarised light", ["a mixture of E and Z isomers", "a pure enantiomer", "a mixture of structural isomers"], "The rotations cancel."),
        ("What is the zwitterion of an amino acid?", "an ion with both a positive (NH₃⁺) and a negative (COO⁻) group", ["a negatively charged ion only", "a peptide", "a free radical"], "Found at the isoelectric point."),
        ("Which reagent reduces nitrobenzene to phenylamine?", "tin and concentrated hydrochloric acid", ["NaBH₄", "acidified dichromate", "UV light"], "Followed by adding NaOH."),
        ("Which compound gives a red precipitate when warmed with Fehling's solution?", "propanal", ["propanone", "propan-2-ol", "propanoic acid"], "Aldehydes reduce Cu²⁺ to Cu₂O."),
        ("What is made when propanone is reduced with NaBH₄?", "propan-2-ol", ["propan-1-ol", "propanal", "propanoic acid"], "Ketones are reduced to secondary alcohols."),
        ("Why does the product of HCN adding to ethanal form a racemic mixture?", "CN⁻ can attack the planar carbonyl from either side equally", ["the product has no chiral carbon", "only one enantiomer forms", "the reaction is an elimination"], "Equal amounts of both enantiomers form."),
        ("What gas forms when a carboxylic acid reacts with sodium carbonate?", "carbon dioxide", ["hydrogen", "oxygen", "chlorine"], "This fizzing is a test for carboxylic acids."),
        ("What is the catalyst for making an ester from an alcohol and a carboxylic acid?", "concentrated sulfuric acid", ["nickel", "aluminium chloride", "sodium hydroxide"], "The reaction is reversible and slow without it."),
        ("Why is benzene less reactive than cyclohexene towards bromine?", "its delocalised electrons are spread out, so the electron density is lower", ["benzene has more double bonds", "benzene is ionic", "bromine is a nucleophile"], "Benzene needs a halogen carrier such as FeBr₃."),
        ("Which is the strongest base?", "ethylamine", ["ammonia", "phenylamine", "water"], "The alkyl group pushes electrons onto the nitrogen lone pair."),
        ("What links the amino acids in a protein?", "peptide (amide) links", ["ester links", "glycosidic bonds", "hydrogen bonds only"], "Formed by condensation, losing water."),
        ("What is used to give a coloured spot for amino acids in chromatography?", "ninhydrin", ["iodine solution", "bromine water", "Tollens' reagent"], "Amino acids are colourless."),
        ("Which polymer is made by addition polymerisation?", "poly(chloroethene) (PVC)", ["nylon-6,6", "Terylene", "Kevlar"], "Condensation polymers lose a small molecule as they form.")]


# =================================================================== unit definitions
def UNITS(year):
    b_bond, b_mb, b_mech, b_tm, b_org2 = once_maker(BOND), once_maker(MB), once_maker(MECH), once_maker(TMB), once_maker(ORG2)
    b_hal, b_g2, b_p3 = once_maker(INORG[0:11] + HALX), once_maker(INORG[11:19] + G2X), once_maker(INORG[19:24] + P3X)
    if year == 12:
        return [
            U("Chemistry", 6, "atomic-structure-and-amount-of-substance", "Physical chemistry",
              "Atomic structure, electron configurations, mass spectrometry and relative atomic mass, the mole and the Avogadro constant, concentrations of solutions, the ideal gas equation, empirical and molecular formulae, percentage yield, atom economy and titrations.",
              "Atomic Structure and Amount of Substance", "atomic structure and amount of substance",
              "Free Year 12 A level chemistry worksheets on atomic structure and the mole: electron configurations, relative atomic mass, moles, concentration, pV = nRT, empirical formulae, yield and titrations. 100 questions with answers.",
              "n = m/M = cV = pV/RT.", "Change cm³ into dm³ (÷ 1000) and into m³ (÷ 10⁶).",
              "<p>The amount of substance in moles is the link between every calculation: <i>n</i> = <i>m</i>/<i>M</i> for solids, <i>n</i> = <i>cV</i> for solutions (<i>V</i> in dm³) and <i>n</i> = <i>pV</i>/<i>RT</i> for gases (<i>p</i> in Pa, <i>V</i> in m³, <i>T</i> in K). Use the balanced equation to change moles of one substance into moles of another.</p>"
              "<p>Electrons fill 1s, 2s, 2p, 3s, 3p, 4s, 3d. Chromium and copper are exceptions (3d⁵4s¹ and 3d¹⁰4s¹), and transition metal ions lose their 4s electrons first.</p>",
              [("How many moles in 25.0 cm³ of 0.100 mol dm⁻³ NaOH?", ["V = 0.0250 dm³", "n = 0.100 × 0.0250"], "2.50 × 10⁻³ mol"),
               ("Electron configuration of Fe²⁺?", ["Fe is [Ar] 3d⁶ 4s²", "lose the two 4s electrons"], "[Ar] 3d⁶")],
              ["Leaving volumes in cm³.", "Removing 3d electrons before 4s when forming ions.", "Forgetting the mole ratio from the equation."],
              [("What is the ideal gas equation?", "pV = nRT, with p in pascals, V in m³, T in kelvin and R = 8.31 J K⁻¹ mol⁻¹."),
               ("What is atom economy?", "The mass of the desired product as a percentage of the total mass of reactants, from the balanced equation.")],
              lambda: [("Electron configurations and A<sub>r</sub>", [(c_config, 12), (c_ram, 8)]), ("Moles and mass", [(c_moles, 20)]), ("Solutions and titrations", [(c_conc, 12), (c_titr, 8)]),
                       ("Gases and formulae", [(c_gas, 12), (c_emp, 8)]), ("Yield and atom economy", [(c_yield, 14), (c_titr, 6)])]),
            U("Chemistry", 7, "bonding-and-energetics", "Physical chemistry",
              "Ionic, covalent and metallic bonding, shapes of simple molecules and ions, bond polarity and intermolecular forces, enthalpy change, calorimetry, Hess's law, enthalpies of formation and combustion, and mean bond enthalpies.",
              "Bonding, Shapes of Molecules and Energetics", "bonding and energetics",
              "Free Year 12 A level chemistry worksheets on bonding and energetics: shapes of molecules and bond angles, intermolecular forces, calorimetry, Hess's law and mean bond enthalpies. 100 questions with answers.",
              "Electron pairs repel: lone pairs repel most.", "ΔH = Σ(bonds broken) − Σ(bonds made).",
              "<p>The shape of a molecule depends on the number of electron pairs round the central atom. Lone pairs repel more than bonding pairs, so each lone pair closes the bond angle by about 2.5° (CH₄ 109.5°, NH₃ 107°, H₂O 104.5°).</p>"
              "<p>In calorimetry <i>q</i> = <i>mc</i>Δ<i>T</i> and Δ<i>H</i> = −<i>q</i>/<i>n</i>. By Hess's law, Δ<i>H</i> = ΣΔ<sub>f</sub><i>H</i>(products) − ΣΔ<sub>f</sub><i>H</i>(reactants). With bond enthalpies, Δ<i>H</i> = bonds broken − bonds made.</p>",
              [("Shape of NH₃?", ["3 bonding pairs, 1 lone pair"], "pyramidal, 107°"),
               ("0.46 g of ethanol heats 100 g of water by 20 K. ΔH?", ["q = 100 × 4.18 × 20 = 8360 J", "n = 0.0100 mol"], "−836 kJ mol⁻¹")],
              ["Forgetting the minus sign for an exothermic ΔH.", "Using the mass of fuel instead of water in q = mcΔT.", "Doing reactants − products in Hess's law."],
              [("Why does a lone pair reduce the bond angle?", "Lone pairs are closer to the central atom and repel more strongly than bonding pairs."),
               ("What is Hess's law?", "The enthalpy change of a reaction does not depend on the route taken, as long as the start and end are the same.")],
              lambda: [("Shapes of molecules", [(c_shape, 20)]), ("Bonding and intermolecular forces", [(b_bond, 14), (c_shape, 6)]), ("Calorimetry", [(c_calor, 20)]),
                       ("Hess's law", [(K(c_hess, "form"), 10), (K(c_hess, "comb"), 10)]), ("Bond enthalpies", [(K(c_hess, "bond"), 11), (K(c_hess, "unk"), 9)])]),
            U("Chemistry", 8, "kinetics-and-equilibria", "Physical chemistry",
              "Collision theory, the Maxwell–Boltzmann distribution and catalysts, dynamic equilibrium and Le Chatelier's principle, the equilibrium constant Kc and its calculation from equilibrium amounts.",
              "Kinetics and Chemical Equilibria", "kinetics and equilibria",
              "Free Year 12 A level chemistry worksheets on kinetics and equilibria: Maxwell–Boltzmann distributions, catalysts, Le Chatelier's principle, Kc expressions and Kc calculations. 100 questions with answers.",
              "Kc = products over reactants, with powers.", "Only temperature changes the value of Kc.",
              "<p>Reactions need collisions with at least the activation energy. A catalyst gives a route with a lower <i>E</i><sub>a</sub>; a higher temperature moves the Maxwell–Boltzmann peak right, so many more molecules exceed <i>E</i><sub>a</sub>.</p>"
              "<p>At dynamic equilibrium the forward and backward rates are equal. Le Chatelier: the position shifts to oppose a change. For aA + bB ⇌ cC + dD, <i>K</i><sub>c</sub> = [C]<sup>c</sup>[D]<sup>d</sup> / [A]<sup>a</sup>[B]<sup>b</sup>.</p>",
              [("K<sub>c</sub> for N₂ + 3H₂ ⇌ 2NH₃?", ["products over reactants with powers"], "[NH₃]² / [N₂][H₂]³"),
               ("Effect of raising the temperature on an exothermic equilibrium?", ["the endothermic (backward) direction is favoured"], "shifts left, K<sub>c</sub> falls")],
              ["Thinking a catalyst shifts the equilibrium.", "Forgetting to raise concentrations to their coefficients.", "Thinking pressure changes K<sub>c</sub>."],
              [("What is the Maxwell–Boltzmann distribution?", "A graph of the number of molecules against their energy. The area under it is the total number of molecules."),
               ("Does a catalyst change the equilibrium position?", "No. It speeds up the forward and backward reactions equally, so equilibrium is reached sooner.")],
              lambda: [("Collision theory and catalysts", [(b_mb, 15), (K(c_kc, "cat"), 5)]), ("Le Chatelier's principle", [(K(c_kc, "shiftT", "shiftP"), 20)]),
                       ("K<sub>c</sub> expressions", [(K(c_kc, "expr"), 6), (K(c_kc, "units"), 6), (K(c_kc, "calc"), 8)]), ("Calculating K<sub>c</sub>", [(K(c_kc, "calc"), 20)]),
                       ("Equilibrium amounts", [(c_ice, 20)])]),
            U("Chemistry", 9, "redox-and-inorganic-chemistry", "Inorganic chemistry",
              "Oxidation states, redox reactions and half-equations, periodicity across period 3, the group 2 metals and their compounds, the halogens and halide ions, and tests for ions.",
              "Redox, Group 2 and the Halogens", "redox and inorganic chemistry",
              "Free Year 12 A level chemistry worksheets on redox and inorganic chemistry: oxidation states, half-equations, period 3 trends, group 2 and group 7 reactions, and tests for ions. 100 questions with answers.",
              "OIL RIG: oxidation is loss, reduction is gain of electrons.", "Oxidation states add up to the charge on the species.",
              "<p>Assign oxidation states with simple rules: elements are 0, O is −2 (except peroxides), H is +1 (except metal hydrides), and the total equals the overall charge. An oxidising agent accepts electrons and is itself reduced.</p>"
              "<p>Down group 2 reactivity and hydroxide solubility increase, while sulfate solubility decreases. Down group 7 oxidising power decreases and the halide ions become stronger reducing agents. Silver nitrate tests: Cl⁻ white, Br⁻ cream, I⁻ yellow.</p>",
              [("Oxidation state of Mn in MnO₄⁻?", ["4 × (−2) = −8", "Mn − 8 = −1"], "+7"),
               ("Test result for bromide ions with acidified AgNO₃?", ["AgBr forms"], "cream precipitate")],
              ["Forgetting the overall charge when finding oxidation states.", "Saying oxidation is gain of electrons.", "Mixing up the trends in solubility of group 2 hydroxides and sulfates."],
              [("What is a disproportionation reaction?", "One where the same element is both oxidised and reduced, for example chlorine with cold dilute NaOH."),
               ("Why does oxidising power decrease down group 7?", "The atoms are bigger and more shielded, so they attract an extra electron less strongly.")],
              lambda: [("Oxidation states", [(c_ox, 20)]), ("Half-equations", [(c_halfe, 20)]), ("Group 2", [(b_g2, 14), (c_ox, 6)]),
                       ("The halogens", [(b_hal, 14), (c_disp, 6)]), ("Period 3 and mixed problems", [(b_p3, 8), (c_halfe, 6), (c_ox, 6)])]),
            U("Chemistry", 10, "organic-chemistry-alkanes-alkenes-and-alcohols", "Organic chemistry",
              "Nomenclature and isomerism, alkanes and fuels, halogenoalkanes and nucleophilic substitution, alkenes and electrophilic addition, alcohols and their oxidation, and polymers.",
              "Organic Chemistry: Alkanes, Alkenes and Alcohols", "organic chemistry",
              "Free Year 12 A level chemistry worksheets on organic chemistry: IUPAC names, general formulae, combustion, free-radical substitution, electrophilic addition, nucleophilic substitution and alcohols. 100 questions with answers.",
              "Name from the longest chain; number for the lowest locant.", "Primary alcohol → aldehyde → acid; secondary → ketone.",
              "<p>Name compounds from the longest carbon chain (meth-, eth-, prop-, but-, pent-, hex-) and number from the end that gives the substituent or functional group the lowest number. Alkanes are C<sub>n</sub>H<sub>2n+2</sub>, alkenes C<sub>n</sub>H<sub>2n</sub>.</p>"
              "<p>Alkanes react with halogens by free-radical substitution; alkenes undergo electrophilic addition; halogenoalkanes undergo nucleophilic substitution (aqueous OH⁻) or elimination (ethanolic OH⁻). Acidified dichromate oxidises primary and secondary alcohols (orange → green).</p>",
              [("Name CH₃CHBrCH₂CH₃.", ["4 carbons: butane", "Br on C2"], "2-bromobutane"),
               ("Moles of O₂ to burn 1 mol of C₃H₈?", ["3CO₂ + 4H₂O need 10 O atoms"], "5")],
              ["Numbering from the wrong end of the chain.", "Writing 'hydroxy' instead of the -ol suffix.", "Thinking tertiary alcohols are oxidised."],
              [("What is electrophilic addition?", "An electrophile is attracted to the electron-rich C=C double bond and adds across it, as with Br₂ or HBr."),
               ("How do you tell primary, secondary and tertiary alcohols apart?", "Warm with acidified potassium dichromate: primary and secondary turn it green, tertiary do not.")],
              lambda: [("Naming organic compounds", [(c_name, 20)]), ("Formulae and combustion", [(c_formula, 20)]), ("Mechanisms", [(b_mech, 20)]),
                       ("More naming", [(c_name, 14), (c_formula, 6)]), ("Reactions and conditions", [(b_mech, 8), (c_name, 6), (c_formula, 6)])]),
        ]
    return [
        U("Chemistry", 5, "thermodynamics-and-rate-equations", "Physical chemistry",
          "Entropy, Gibbs free-energy change and feasibility, rate equations, orders of reaction and rate constants, the Arrhenius equation, and equilibrium constant Kp for homogeneous systems.",
          "Thermodynamics, Rate Equations and Kp", "thermodynamics and rate equations",
          "Free Year 13 A level chemistry worksheets on thermodynamics and kinetics: entropy, ΔG = ΔH − TΔS, rate equations, orders, rate constants and their units, the Arrhenius equation and Kp. 100 questions with answers.",
          "ΔG = ΔH − TΔS; feasible when ΔG ≤ 0.", "Change ΔS from J K⁻¹ mol⁻¹ into kJ K⁻¹ mol⁻¹.",
          "<p>A reaction is feasible when Δ<i>G</i> = Δ<i>H</i> − <i>T</i>Δ<i>S</i> ≤ 0. The temperature at which it becomes feasible is <i>T</i> = Δ<i>H</i>/Δ<i>S</i> (with matching units). Δ<i>S</i> = Σ<i>S</i>(products) − Σ<i>S</i>(reactants).</p>"
          "<p>A rate equation has the form rate = <i>k</i>[A]<sup>m</sup>[B]<sup>n</sup>; the orders come from experiments, not the equation. <i>k</i> = <i>Ae</i><sup>−Ea/RT</sup>. For gases, <i>K</i><sub>p</sub> uses partial pressures: <i>p</i> = mole fraction × total pressure.</p>",
          [("ΔH = +178 kJ mol⁻¹, ΔS = +161 J K⁻¹ mol⁻¹. Minimum T?", ["T = 178000 ÷ 161"], "1110 K"),
           ("Doubling [A] quadruples the rate. Order in A?", ["2² = 4"], "2")],
          ["Mixing kJ and J in ΔG = ΔH − TΔS.", "Taking orders from the balanced equation.", "Using °C in the Arrhenius equation."],
          [("What does a negative ΔG mean?", "The reaction is feasible (it can happen without continuous energy input), though it may still be slow."),
           ("How do you find the order of a reaction?", "Change one concentration at a time: if the rate stays the same the order is 0, doubles → 1, quadruples → 2.")],
          lambda: [("Entropy and Gibbs free energy", [(K(c_entropy, "calc"), 6), (K(c_entropy, "sign"), 8), (c_gibbs, 6)]), ("Feasibility", [(c_gibbs, 20)]), ("Orders of reaction", [(K(c_order, "order", "units"), 20)]),
                   ("Rate constants and Arrhenius", [(K(c_order, "k", "rate"), 12), (c_arr, 8)]), ("K<sub>p</sub>", [(c_kp, 20)])]),
        U("Chemistry", 6, "acids-bases-and-electrode-potentials", "Physical chemistry",
          "Brønsted–Lowry acids and bases, pH of strong and weak acids and strong bases, Kw, Ka and pKa, buffer solutions, electrode potentials, standard e.m.f. of cells and predicting feasibility.",
          "Acids, Bases and Electrode Potentials", "acids, bases and electrode potentials",
          "Free Year 13 A level chemistry worksheets on acids, bases and electrode potentials: pH of strong and weak acids, Kw, Ka and pKa, buffers, cell e.m.f. and feasibility. 100 questions with answers.",
          "pH = −log[H⁺].", "E°cell = E°(positive) − E°(negative).",
          "<p>For a strong acid [H⁺] equals the acid concentration (twice for H₂SO₄). For a strong base use <i>K</i><sub>w</sub> = [H⁺][OH⁻] = 1.00 × 10⁻¹⁴. For a weak acid [H⁺] = √(<i>K</i><sub>a</sub><i>c</i>); for a buffer [H⁺] = <i>K</i><sub>a</sub>[HA]/[A⁻].</p>"
          "<p>The half-cell with the more negative <i>E</i>° is the negative electrode, where oxidation happens. <i>E</i>°<sub>cell</sub> = <i>E</i>°(more positive) − <i>E</i>°(more negative). A reaction is feasible if the oxidising agent has the more positive <i>E</i>°.</p>",
          [("pH of 0.010 mol dm⁻³ HCl?", ["[H⁺] = 0.010", "−log 0.010"], "2.00"),
           ("Zn (−0.76 V) and Cu (+0.34 V) cell e.m.f.?", ["0.34 − (−0.76)"], "1.10 V")],
          ["Using √(Ka c) for a strong acid.", "Forgetting Kw for strong bases.", "Subtracting the E° values the wrong way round."],
          [("What is a buffer?", "A solution that resists changes in pH when small amounts of acid or base are added, for example a weak acid with its salt."),
           ("What does a positive E°cell mean?", "The cell reaction is feasible under standard conditions.")],
          lambda: [("Strong acids and bases", [(K(c_ph, "strong", "H", "base", "dil"), 20)]), ("Weak acids", [(K(c_ph, "weak", "ka", "kph"), 20)]), ("Buffers", [(K(c_ph, "buffer"), 14), (K(c_ph, "weak"), 6)]),
                   ("Cell e.m.f.", [(c_ecell, 20)]), ("Mixed problems", [(c_ph, 10), (c_ecell, 10)])]),
        U("Chemistry", 7, "transition-metals", "Inorganic chemistry",
          "Properties of transition metals, complex ions and ligands, shapes and co-ordination numbers, colour, variable oxidation states, catalysts, reactions of ions in aqueous solution and redox titrations.",
          "Transition Metals and Complex Ions", "transition metals",
          "Free Year 13 A level chemistry worksheets on transition metals: complex ions, ligands, co-ordination numbers, shapes, colours, catalysts and redox titrations with manganate(VII) and dichromate(VI). 100 questions with answers.",
          "Ligands donate lone pairs to the metal ion.", "MnO₄⁻ : Fe²⁺ = 1 : 5; Cr₂O₇²⁻ : Fe²⁺ = 1 : 6.",
          "<p>A transition metal forms at least one stable ion with a partly filled d sub-shell. Ligands form co-ordinate bonds to the metal ion; six small ligands give an octahedral complex, four Cl⁻ give tetrahedral, Ag(NH₃)₂⁺ is linear and cisplatin is square planar.</p>"
          "<p>Complexes are coloured because d electrons absorb visible light. In titrations MnO₄⁻ (purple → colourless) reacts with Fe²⁺ in a 1 : 5 ratio.</p>",
          [("Oxidation state of Fe in [Fe(CN)₆]³⁻?", ["6 × (−1) + x = −3"], "+3"),
           ("20.0 cm³ of 0.020 mol dm⁻³ KMnO₄ reacts with Fe²⁺. n(Fe²⁺)?", ["n(MnO₄⁻) = 4.0 × 10⁻⁴", "× 5"], "2.0 × 10⁻³ mol")],
          ["Forgetting the charges on ligands such as Cl⁻ and CN⁻.", "Using a 1 : 1 ratio in redox titrations.", "Saying the colour seen is the colour absorbed."],
          [("Why are transition metal complexes coloured?", "Ligands split the d orbitals; electrons absorb visible light to jump between them, and we see the complementary colour."),
           ("What is a ligand?", "A molecule or ion with a lone pair that forms a co-ordinate bond to a metal ion.")],
          lambda: [("Complex ions", [(c_tm, 20)]), ("Ligands, colour and catalysts", [(b_tm, 12), (K(c_tm, "lig"), 8)]), ("Shapes and co-ordination numbers", [(K(c_tm, "cn", "shape"), 20)]),
                   ("Redox titrations", [(c_redox_titr, 20)]), ("Mixed problems", [(c_tm, 8), (b_tm, 4), (c_redox_titr, 8)])]),
        U("Chemistry", 8, "further-organic-chemistry-and-analysis", "Organic chemistry",
          "Optical isomerism, aldehydes and ketones, carboxylic acids and esters, acylation, aromatic chemistry, amines, polymers, amino acids, and analysis by mass spectrometry, infrared, NMR spectroscopy and chromatography.",
          "Further Organic Chemistry and Spectroscopy", "further organic chemistry",
          "Free Year 13 A level chemistry worksheets on further organic chemistry: naming esters, carbonyl tests, aromatic chemistry, polymers, mass spectra, infrared, ¹H NMR and chromatography. 100 questions with answers.",
          "NMR: peaks = environments; n + 1 rule for splitting.", "Esters: alcohol part first (ethyl), acid part second (ethanoate).",
          "<p>Esters are named alcohol part first, then acid part: ethanol + propanoic acid gives ethyl propanoate. Aldehydes give a silver mirror with Tollens' reagent; ketones do not. Benzene reacts by electrophilic substitution to keep its delocalised ring.</p>"
          "<p>In ¹H NMR each hydrogen environment gives a peak, split into <i>n</i> + 1 lines by <i>n</i> hydrogens on the next carbon. The molecular ion in a mass spectrum is at <i>M</i><sub>r</sub>. R<sub>f</sub> = spot distance ÷ solvent distance.</p>",
          [("Ester from ethanoic acid and propan-1-ol?", ["alcohol part: propyl", "acid part: ethanoate"], "propyl ethanoate"),
           ("Splitting of the CH₃ peak in CH₃CH₂Cl?", ["2 H on the next carbon", "2 + 1 = 3"], "triplet")],
          ["Naming the acid part of an ester first.", "Counting the H atoms in the group itself for the n + 1 rule.", "Thinking ketones give a silver mirror."],
          [("What does the n + 1 rule say?", "A peak is split into n + 1 lines, where n is the number of hydrogens on the neighbouring carbon atoms."),
           ("How do you tell an aldehyde from a ketone?", "Warm with Tollens' reagent: an aldehyde gives a silver mirror; a ketone does not react.")],
          lambda: [("Esters", [(c_ester, 20)]), ("Carbonyls, aromatics and amines", [(b_org2, 17), (c_ester, 3)]), ("Mass spectra and chromatography", [(K(c_anal, "ms", "rf"), 20)]),
                   ("NMR spectroscopy", [(c_nmr, 20)]), ("Infrared and mixed analysis", [(K(c_anal, "ir"), 7), (c_nmr, 6), (K(c_anal, "ms", "rf"), 7)])]),
    ]
