# -*- coding: utf-8 -*-
"""
UK A level Physics question makers (Year 12 = AS content, Year 13 = the rest). Units are listed in UNITS(year).
Constants as on the A level data sheets: h = 6.63 × 10⁻³⁴ J s, c = 3.00 × 10⁸ m/s, e = 1.60 × 10⁻¹⁹ C,
mₑ = 9.11 × 10⁻³¹ kg, g = 9.81 N/kg, G = 6.67 × 10⁻¹¹ N m² kg⁻², R = 8.31 J mol⁻¹ K⁻¹, k = 1.38 × 10⁻²³ J/K.
Wrong answers come from real mistakes: forgetting to convert nm or eV, using diameter for radius, squaring the wrong term,
adding parallel resistances, using T for f, forgetting the square root.
"""
import math
import random
from uk_alsci import nf, nq, tq, once_maker, U

R = random.Random(0)
H, C, E, ME, G, GG, RG, KB, NA, KC, U_ = 6.63e-34, 3.00e8, 1.60e-19, 9.11e-31, 9.81, 6.67e-11, 8.31, 1.38e-23, 6.02e23, 8.99e9, 1.66e-27
X10 = " × 10<sup>%s</sup>"


def ch(xs):
    return R.choice(xs)


def K(f, *kinds):
    g = lambda: f(R.choice(kinds))
    g.__name__ = f.__name__ + '_' + '_'.join(kinds)
    return g


# =================================================================== Year 12: particles and quantum phenomena
NUC = [("C", 6, 12), ("C", 6, 14), ("N", 7, 14), ("O", 8, 16), ("Na", 11, 23), ("Mg", 12, 24), ("Al", 13, 27), ("Cl", 17, 35), ("Cl", 17, 37),
       ("K", 19, 40), ("Fe", 26, 56), ("Co", 26 + 1, 60), ("Cu", 29, 63), ("Sr", 38, 90), ("I", 53, 131), ("Cs", 55, 137), ("Ra", 88, 226),
       ("U", 92, 235), ("U", 92, 238), ("Pu", 94, 239), ("Am", 95, 241), ("Rn", 86, 222), ("Po", 84, 210), ("Pb", 82, 206), ("Th", 90, 234), ("He", 2, 4), ("Li", 3, 7)]


def nuc(s, z, a):
    return "<sup>%d</sup><sub>%d</sub>%s" % (a, z, s)


def p_nucleus(k=None):
    s, z, a = ch(NUC)
    k = k or ch(["n", "n", "sc", "nuc"])
    if k == "n":
        return nq("How many neutrons are in the nucleus %s?" % nuc(s, z, a), a - z, [a, z, a + z], "", "Neutrons = nucleon number − proton number = %d − %d = <b>%d</b>." % (a, z, a - z), sf=3)
    if k == "nuc":
        return nq("A neutral atom of %s has how many particles (protons, neutrons and electrons) in total?" % nuc(s, z, a), a + z, [a, a - z, 2 * a], "",
                  "%d nucleons + %d electrons = <b>%d</b>." % (a, z, a + z))
    sc = z * E / (a * 1.67e-27)
    return nq("Calculate the specific charge of the nucleus %s. Take the mass of a nucleon as 1.67 × 10<sup>−27</sup> kg." % nuc(s, z, a), sc,
              [a * E / (a * 1.67e-27), z * E / ((a - z) * 1.67e-27), z * E * a * 1.67e-27], " C/kg",
              "Specific charge = charge ÷ mass = (%d × 1.60 × 10<sup>−19</sup>) ÷ (%d × 1.67 × 10<sup>−27</sup>) = <b>%s C/kg</b>." % (z, a, nf(sc)))


def p_photon(k=None):
    lam = ch(list(range(250, 760, 10)))
    k = k or ch(["J", "eV", "f"])
    En = H * C / (lam * 1e-9)
    if k == "J":
        return nq("Calculate the energy of a photon of wavelength %d nm." % lam, En, [H * C / lam, H / (lam * 1e-9), En / E], " J",
                  "E = hc/λ = (6.63 × 10<sup>−34</sup> × 3.00 × 10<sup>8</sup>) ÷ (%d × 10<sup>−9</sup>) = <b>%s J</b>." % (lam, nf(En)))
    if k == "eV":
        return nq("Calculate the energy, in eV, of a photon of wavelength %d nm." % lam, En / E, [En, En * E, H * C / (lam * 1e-9) / E * 1000], " eV",
                  "E = hc/λ = %s J. Divide by 1.60 × 10<sup>−19</sup>: <b>%s eV</b>." % (nf(En), nf(En / E)))
    f = C / (lam * 1e-9)
    return nq("Calculate the frequency of light of wavelength %d nm." % lam, f, [C * lam * 1e-9, C / lam, lam * 1e-9 / C], " Hz",
              "f = c/λ = 3.00 × 10<sup>8</sup> ÷ (%d × 10<sup>−9</sup>) = <b>%s Hz</b>." % (lam, nf(f)))


METALS = [("caesium", 2.1), ("potassium", 2.3), ("sodium", 2.3), ("calcium", 2.9), ("magnesium", 3.7), ("zinc", 4.3), ("aluminium", 4.1), ("copper", 4.7), ("silver", 4.3)]


def p_photoelectric(k=None):
    m, phi = ch(METALS)
    k = k or ch(["ke", "f0", "ke2"])
    if k == "f0":
        f0 = phi * E / H
        return nq("The work function of %s is %.1f eV. Calculate its threshold frequency." % (m, phi), f0, [phi / H, H / (phi * E), phi * E * H], " Hz",
                  "f₀ = φ/h = (%.1f × 1.60 × 10<sup>−19</sup>) ÷ 6.63 × 10<sup>−34</sup> = <b>%s Hz</b>." % (phi, nf(f0)))
    lam = ch(list(range(150, int(1240 / phi) - 20, 10)))
    Eph = H * C / (lam * 1e-9) / E
    ke = Eph - phi
    if ke <= 0.1:
        return None
    if k == "ke":
        return nq("Light of wavelength %d nm falls on %s (work function %.1f eV). Calculate the maximum kinetic energy of the photoelectrons in eV." % (lam, m, phi),
                  ke, [Eph + phi, Eph, phi - Eph if phi > Eph else Eph * phi], " eV",
                  "Photon energy = hc/λ = %s eV. E<sub>k(max)</sub> = hf − φ = %s − %.1f = <b>%s eV</b>." % (nf(Eph), nf(Eph), phi, nf(ke)))
    vs = ke
    return nq("Light of wavelength %d nm falls on %s (work function %.1f eV). What stopping potential is needed to stop the fastest photoelectrons?" % (lam, m, phi),
              vs, [Eph, Eph + phi, vs * E], " V", "eV<sub>s</sub> = hf − φ, so V<sub>s</sub> = %s − %.1f = <b>%s V</b>." % (nf(Eph), phi, nf(vs)))


def p_debroglie(k=None):
    k = k or ch(["e", "e", "p", "V"])
    if k == "V":
        V = ch([50, 100, 150, 200, 500, 1000, 2000, 5000])
        v = math.sqrt(2 * E * V / ME)
        lam = H / (ME * v)
        return nq("Electrons are accelerated from rest through a potential difference of %s V. Calculate their de Broglie wavelength." % "{:,}".format(V), lam,
                  [H / (E * V), H / (ME * v * v), H * ME * v], " m",
                  "½mv² = eV gives v = %s m/s. λ = h/(mv) = <b>%s m</b>." % (nf(v), nf(lam)))
    if k == "e":
        v = ch([1, 1.5, 2, 2.5, 3, 4, 5, 6, 8]) * 10 ** ch([5, 6])
        lam = H / (ME * v)
        return nq("Calculate the de Broglie wavelength of an electron moving at %s m/s." % nf(v), lam, [H * ME * v, ME * v / H, H / (ME * v * v)], " m",
                  "λ = h/(mv) = 6.63 × 10<sup>−34</sup> ÷ (9.11 × 10<sup>−31</sup> × %s) = <b>%s m</b>." % (nf(v), nf(lam)))
    m = ch([1.67e-27, 6.64e-27])
    name = "proton" if m < 2e-27 else "alpha particle"
    v = ch([2, 3, 4, 5, 6, 8]) * 10 ** ch([4, 5, 6])
    lam = H / (m * v)
    return nq("Calculate the de Broglie wavelength of a %s (mass %s kg) moving at %s m/s." % (name, nf(m), nf(v)), lam, [H * m * v, H / (ME * v), m * v / H], " m",
              "λ = h/(mv) = <b>%s m</b>." % nf(lam))


def p_levels(k=None):
    n1, n2 = sorted(R.sample([1, 2, 3, 4, 5], 2))
    E1, E2 = -13.6 / n1 ** 2, -13.6 / n2 ** 2
    dE = E2 - E1
    k = k or ch(["E", "lam"])
    q0 = "In a hydrogen atom the energy levels are −13.6 eV, −3.40 eV, −1.51 eV, −0.85 eV and −0.54 eV (n = 1 to 5). An electron falls from n = %d to n = %d. " % (n2, n1)
    if k == "E":
        return nq(q0 + "Calculate the energy of the photon emitted in eV.", dE, [-E1 - E2, -E2, -E1], " eV", "ΔE = %s − (%s) = <b>%s eV</b>." % (nf(E2), nf(E1), nf(dE)))
    lam = H * C / (dE * E)
    return nq(q0 + "Calculate the wavelength of the photon emitted.", lam, [H * C / dE, H * C / (-E1 * E), H * dE * E / C], " m",
              "ΔE = %s eV = %s J. λ = hc/ΔE = <b>%s m</b>." % (nf(dE), nf(dE * E), nf(lam)))


PART = [("What is the quark composition of a proton?", "uud", ["udd", "uds", "uūd"], "A proton has charge +1: ⅔ + ⅔ − ⅓ = +1."),
        ("What is the quark composition of a neutron?", "udd", ["uud", "uds", "ddd"], "⅔ − ⅓ − ⅓ = 0."),
        ("A π⁺ meson is made of which quarks?", "u and anti-d", ["u and d", "anti-u and d", "u, u and d"], "Mesons are a quark and an antiquark: ⅔ + ⅓ = +1."),
        ("Which particle is a lepton?", "muon", ["proton", "pion", "kaon"], "Leptons (electron, muon, neutrinos) are not made of quarks."),
        ("Which particle is a baryon?", "neutron", ["electron", "pion", "neutrino"], "Baryons are made of three quarks."),
        ("Which particle is a meson?", "kaon", ["proton", "muon", "positron"], "Mesons are a quark–antiquark pair: pions and kaons."),
        ("Which particle contains a strange quark?", "kaon", ["pion", "proton", "muon"], "Kaons have strangeness ±1."),
        ("Which force acts on leptons but not through the strong interaction?", "the weak interaction", ["the strong nuclear force", "the gluon force", "no force at all"], "Leptons feel the weak (and electromagnetic if charged) interaction only."),
        ("What is the exchange particle for the electromagnetic force?", "the virtual photon", ["the W boson", "the gluon", "the pion"], "Charged particles exchange virtual photons."),
        ("Which exchange particle is involved in β⁻ decay?", "W⁻ boson", ["W⁺ boson", "virtual photon", "gluon"], "In β⁻ decay a d quark becomes a u quark by emitting a W⁻."),
        ("Which exchange particle is involved in electron capture?", "W⁺ boson", ["W⁻ boson", "virtual photon", "Z boson"], "p + e⁻ → n + νₑ; a u quark becomes a d quark."),
        ("What is the antiparticle of the electron?", "the positron", ["the proton", "the antineutrino", "the muon"], "Same mass, opposite charge."),
        ("In β⁻ decay, which particles are emitted?", "an electron and an electron antineutrino", ["a positron and a neutrino", "an electron and a neutrino", "an alpha particle and a photon"], "n → p + e⁻ + ν̄ₑ; lepton number is conserved."),
        ("In β⁺ decay, which particles are emitted?", "a positron and an electron neutrino", ["an electron and an antineutrino", "a positron and an antineutrino", "two photons"], "p → n + e⁺ + νₑ."),
        ("Which quantity is NOT always conserved in particle interactions?", "strangeness", ["charge", "baryon number", "lepton number"], "Strangeness can change by ±1 in weak interactions."),
        ("What is the baryon number of an antiproton?", "−1", ["+1", "0", "+⅓"], "Antibaryons have baryon number −1."),
        ("What is the lepton number of a positron?", "−1", ["+1", "0", "+½"], "Antileptons have lepton number −1."),
        ("A proton and an antiproton annihilate. What is produced?", "two photons", ["one photon", "a neutron", "an electron and a positron at rest"], "Two photons conserve momentum."),
        ("What happens in pair production?", "a photon becomes a particle and its antiparticle", ["two photons become one", "a neutron becomes a proton", "an electron becomes a positron"], "The photon energy must be at least 2mc²."),
        ("Which particle is the only stable baryon?", "the proton", ["the neutron", "the pion", "the electron"], "A free neutron decays with a half-life of about 10 minutes."),
        ("What is the charge of a strange quark?", "−⅓e", ["+⅓e", "+⅔e", "−⅔e"], "s has the same charge as d."),
        ("What does a kaon usually decay into?", "pions", ["protons", "neutrons", "photons only"], "Kaons decay by the weak interaction into pions (or muons)."),
        ("What is the specific charge of a particle?", "its charge divided by its mass", ["its mass divided by its charge", "its charge times its mass", "its charge in coulombs per mole"], "Unit: C/kg."),
        ("Which observation is evidence that electrons behave as waves?", "electron diffraction", ["the photoelectric effect", "line spectra", "pair production"], "Diffraction is a wave property."),
        ("Which observation is evidence that light behaves as particles?", "the photoelectric effect", ["electron diffraction", "two-slit interference", "polarisation"], "Emission is instant and depends on frequency, not intensity."),
        ("Increasing the intensity of light above the threshold frequency…", "increases the number of photoelectrons per second", ["increases their maximum kinetic energy", "lowers the work function", "has no effect"], "More photons per second, same energy each."),
        ("What is one electronvolt?", "1.60 × 10⁻¹⁹ J", ["1.60 × 10⁻¹⁹ V", "6.63 × 10⁻³⁴ J", "9.11 × 10⁻³¹ J"], "The energy gained by an electron moved through 1 V."),
        ("In a fluorescent tube, what makes the coating glow?", "ultraviolet photons from the mercury vapour", ["infrared from the electrodes", "electrons hitting the glass", "X-rays"], "Excited mercury atoms emit UV, which the coating absorbs and re-emits as visible light.")]
p_part = None


# =================================================================== Year 12: waves and optics
def w_vfl(k=None):
    k = k or ch(["sound", "light", "water", "string"])
    if k == "sound":
        v, f = 340, ch([170, 256, 340, 440, 512, 680, 850, 1000, 1360, 2000, 3400])
        return nq("Sound travels at 340 m/s in air. Calculate the wavelength of a %d Hz note." % f, v / f, [f / v, v * f, v / f * 2], " m", "λ = v/f = 340 ÷ %d = <b>%s m</b>." % (f, nf(v / f)))
    if k == "light":
        lam = ch(list(range(400, 710, 10)))
        f = C / (lam * 1e-9)
        return nq("Calculate the frequency of red to violet light with wavelength %d nm." % lam, f, [C * lam * 1e-9, C / lam, 1 / (lam * 1e-9)], " Hz", "f = c/λ = <b>%s Hz</b>." % nf(f))
    if k == "water":
        f, lam = ch([0.2, 0.25, 0.4, 0.5, 0.8, 1.2, 1.5, 2]), ch([0.5, 0.8, 1.2, 1.5, 2, 2.5, 3, 4, 6])
        return nq("Water waves have frequency %s Hz and wavelength %s m. Calculate their speed." % (nf(f, 2), nf(lam, 2)), f * lam, [f / lam, lam / f, 1 / f], " m/s", "v = fλ = <b>%s m/s</b>." % nf(f * lam))
    T = ch([0.002, 0.004, 0.005, 0.01, 0.02, 0.025, 0.05])
    return nq("A wave has a period of %s s. Calculate its frequency." % nf(T, 2), 1 / T, [T, 2 * math.pi / T, 1 / T / 1000], " Hz", "f = 1/T = <b>%s Hz</b>." % nf(1 / T))


MEDIA = [("water", 1.33), ("glass", 1.50), ("crown glass", 1.52), ("acrylic", 1.49), ("diamond", 2.42), ("ice", 1.31), ("quartz", 1.54), ("flint glass", 1.62)]


def w_refr(k=None):
    m, n = ch(MEDIA)
    k = k or ch(["v", "snell", "crit", "fibre"])
    if k == "v":
        return nq("The refractive index of %s is %.2f. Calculate the speed of light in it." % (m, n), C / n, [C * n, n / C, C / n / 10], " m/s", "n = c/v, so v = 3.00 × 10<sup>8</sup> ÷ %.2f = <b>%s m/s</b>." % (n, nf(C / n)))
    if k == "crit":
        c = math.degrees(math.asin(1 / n))
        return nq("Calculate the critical angle for light going from %s (n = %.2f) into air." % (m, n), c, [math.degrees(math.asin(1 / n)) / 2, math.degrees(math.acos(1 / n)), math.degrees(math.atan(1 / n))], "°",
                  "sin C = 1/n = 1/%.2f, so C = <b>%s°</b>." % (n, nf(c)))
    if k == "fibre":
        n1, n2 = ch([(1.50, 1.45), (1.48, 1.46), (1.52, 1.48), (1.60, 1.50), (1.47, 1.44)])
        c = math.degrees(math.asin(n2 / n1))
        return nq("An optical fibre has a core of refractive index %.2f and cladding of %.2f. Calculate the critical angle at the boundary." % (n1, n2), c,
                  [math.degrees(math.asin(1 / n1)), math.degrees(math.asin(n2 / n1)) / 2, 90 - c], "°", "sin C = n₂/n₁ = %.2f/%.2f, C = <b>%s°</b>." % (n2, n1, nf(c)))
    i = ch(list(range(15, 76, 5)))
    r = math.degrees(math.asin(math.sin(math.radians(i)) / n))
    return nq("Light in air hits %s (n = %.2f) at an angle of incidence of %d°. Calculate the angle of refraction." % (m, n, i), r, [i / n, math.degrees(math.asin(min(1, math.sin(math.radians(i)) * n / 2))) if n > 2 else i * n / 2, 90 - r], "°",
              "sin r = sin %d° ÷ %.2f, r = <b>%s°</b>." % (i, n, nf(r)))


def w_slits(k=None):
    lam = ch([450, 480, 500, 520, 550, 589, 600, 633, 650, 700])
    s = ch([0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 0.80, 1.0])
    D = ch([1.0, 1.2, 1.5, 2.0, 2.5, 3.0])
    w = lam * 1e-9 * D / (s * 1e-3)
    k = k or ch(["w", "lam"])
    if k == "w":
        return nq("In a double-slit experiment, light of wavelength %d nm passes through slits %s mm apart. The screen is %s m away. Calculate the fringe spacing." % (lam, nf(s, 2), nf(D, 2)), w,
                  [lam * 1e-9 * s * 1e-3 / D, lam * 1e-9 / (D * s * 1e-3), w * 1000], " m", "w = λD/s = (%d × 10<sup>−9</sup> × %s) ÷ (%s × 10<sup>−3</sup>) = <b>%s m</b>." % (lam, nf(D, 2), nf(s, 2), nf(w)))
    return nq("Fringes %s mm apart are seen on a screen %s m from two slits %s mm apart. Calculate the wavelength of the light." % (nf(w * 1000), nf(D, 2), nf(s, 2)), lam * 1e-9,
              [w * D / (s * 1e-3), w / (D * s * 1e-3) * 1e-6, lam * 1e-12], " m", "λ = ws/D = <b>%s m</b> (%d nm)." % (nf(lam * 1e-9), lam))


def w_grating(k=None):
    N = ch([100, 200, 300, 400, 500, 600, 750, 800])
    lam = ch([450, 486, 500, 532, 550, 589, 600, 633, 656, 700])
    d = 1e-3 / N
    k = k or ch(["angle", "order", "d"])
    if k == "d":
        return nq("A diffraction grating has %d lines per mm. Calculate the slit spacing d." % N, d, [1 / N, N * 1e-3, 1e-3 / N / 1000], " m", "d = 1 ÷ (%d × 10<sup>3</sup>) = <b>%s m</b>." % (N, nf(d)))
    nmax = int(d / (lam * 1e-9))
    if k == "order":
        if nmax < 1 or abs(d / (lam * 1e-9) - round(d / (lam * 1e-9))) < 0.05:
            return None
        return nq("Light of wavelength %d nm is shone on a grating with %d lines per mm. What is the highest order of maximum that can be seen?" % (lam, N), nmax,
                  [nmax + 1, 2 * nmax + 1, max(nmax - 1, 0) if nmax > 1 else 3 * nmax + 2], "", "n ≤ d/λ = %s, so n<sub>max</sub> = <b>%d</b>." % (nf(d / (lam * 1e-9)), nmax))
    n = ch([1, 2]) if nmax >= 2 else 1
    th = math.degrees(math.asin(n * lam * 1e-9 / d))
    return nq("Light of wavelength %d nm passes through a grating with %d lines per mm. Calculate the angle of the order %d maximum." % (lam, N, n), th,
              [math.degrees(math.asin(lam * 1e-9 / d)) if n == 2 else 2 * th, n * lam * 1e-9 / d * 180 / math.pi * 1.5, 90 - th], "°",
              "sin θ = nλ/d = %d × %d × 10<sup>−9</sup> ÷ %s = %s, θ = <b>%s°</b>." % (n, lam, nf(d), nf(n * lam * 1e-9 / d), nf(th)))


def w_stationary():
    L = ch([0.40, 0.50, 0.60, 0.65, 0.75, 0.80, 1.0, 1.2])
    v = ch([120, 150, 180, 200, 240, 300, 330, 360, 400])
    n = ch([1, 2, 3, 4])
    f = n * v / (2 * L)
    names = {1: "first harmonic (fundamental)", 2: "second harmonic", 3: "third harmonic", 4: "fourth harmonic"}
    return nq("A string of length %s m is fixed at both ends. Waves travel along it at %d m/s. Calculate the frequency of the %s." % (nf(L, 2), v, names[n]), f,
              [v / (2 * L), n * v / L, n * v * 2 * L, v / L * n / 4 if n > 1 else v / L], " Hz", "λ = 2L/n = %s m, f = v/λ = <b>%s Hz</b>." % (nf(2 * L / n), nf(f)))


def w_phase(k=None):
    lam = ch([0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 2.0])
    frac = ch([0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 1.25])
    dx = lam * frac
    k = k or ch(["phase", "cons"])
    if k == "phase":
        ph = (frac * 360) % 360
        return nq("Two points on a wave are %s m apart and the wavelength is %s m. What is their phase difference in degrees (between 0° and 360°)?" % (nf(dx), nf(lam, 2)), ph,
                  [(frac * 180) % 360, (360 - ph) % 360 if ph not in (0, 180) else 90, frac * 2 * math.pi], "°", "Phase difference = (Δx/λ) × 360° = %s × 360°, so <b>%s°</b> (reduced to 0–360°)." % (nf(frac), nf(ph))) if ph else None
    cons = abs(frac - round(frac)) < 1e-9
    return tq("Two coherent sources in phase send waves of wavelength %s m to a point. The path difference is %s m. What happens there?" % (nf(lam, 2), nf(dx)),
              "constructive interference (a maximum)" if cons else ("destructive interference (a minimum)" if abs(frac * 2 - round(frac * 2)) < 1e-9 else "neither a full maximum nor a minimum"),
              ["destructive interference (a minimum)", "constructive interference (a maximum)", "neither a full maximum nor a minimum", "no waves arrive"],
              "Path difference = %s λ: a whole number of wavelengths gives a maximum, an odd number of half wavelengths gives a minimum." % nf(frac))


# =================================================================== Year 12: mechanics and materials
def m_resolve(k=None):
    F = ch([10, 15, 20, 25, 40, 50, 60, 80, 120, 200])
    a = ch([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    k = k or ch(["h", "v"])
    hx, vy = F * math.cos(math.radians(a)), F * math.sin(math.radians(a))
    q = "A force of %d N acts at %d° above the horizontal. Calculate its %s component." % (F, a, "horizontal" if k == "h" else "vertical")
    val, oth = (hx, vy) if k == "h" else (vy, hx)
    return nq(q, val, [oth, F * math.tan(math.radians(a)), F / math.cos(math.radians(a))], " N", "%s = %d %s %d° = <b>%s N</b>." % ("F<sub>x</sub>" if k == "h" else "F<sub>y</sub>", F, "cos" if k == "h" else "sin", a, nf(val)))


def m_moment():
    w1 = ch([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    d1, d2 = ch([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8]), ch([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75])
    if abs(d1 - d2) < 1e-9:
        return None
    w2 = w1 * d1 / d2
    return nq("A uniform beam is balanced on a pivot at its centre. A %d N weight hangs %s m to the left of the pivot. What weight must hang %s m to the right to balance it?" % (w1, nf(d1, 2), nf(d2, 2)),
              w2, [w1 * d2 / d1, w1, w1 * d1 * d2], " N", "Principle of moments: %d × %s = W × %s, W = <b>%s N</b>." % (w1, nf(d1, 2), nf(d2, 2), nf(w2)))


def m_suvat(k=None):
    k = k or ch(["v", "s", "t", "a"])
    u, a, t = ch([0, 2, 3, 4, 5, 8, 10, 12]), ch([0.5, 1.5, 2, 2.5, 3, 4, 9.81]), ch([2, 3, 4, 5, 6, 8, 10])
    v, s = u + a * t, u * t + 0.5 * a * t * t
    if k == "v":
        return nq("An object starts at %d m/s and accelerates at %s m/s² for %d s. Calculate its final velocity." % (u, nf(a), t), v, [a * t, u + a, u * t + a], " m/s", "v = u + at = %d + %s × %d = <b>%s m/s</b>." % (u, nf(a), t, nf(v)))
    if k == "s":
        return nq("An object starts at %d m/s and accelerates at %s m/s² for %d s. Calculate the distance travelled." % (u, nf(a), t), s, [u * t + a * t * t, v * t, 0.5 * a * t * t], " m", "s = ut + ½at² = <b>%s m</b>." % nf(s))
    if k == "a":
        return nq("A car speeds up from %d m/s to %s m/s over %s m. Calculate its acceleration." % (u, nf(v), nf(s)), a, [(v - u) / s, (v * v - u * u) / s, v * v / (2 * s)], " m/s²",
                  "v² = u² + 2as, so a = (v² − u²)/(2s) = <b>%s m/s²</b>." % nf(a))
    h = ch([5, 10, 15, 20, 25, 30, 45, 50, 80, 100])
    tt = math.sqrt(2 * h / G)
    return nq("A stone is dropped from rest from a height of %d m. Ignoring air resistance, how long does it take to reach the ground? (g = 9.81 m/s²)" % h, tt, [h / G, 2 * h / G, math.sqrt(h / G)], " s",
              "s = ½gt², t = √(2s/g) = √(2 × %d ÷ 9.81) = <b>%s s</b>." % (h, nf(tt)))


def m_proj(k=None):
    u, h = ch([3, 4, 5, 6, 8, 10, 12, 15, 20]), ch([1.2, 1.5, 2, 2.5, 5, 10, 20, 45])
    t = math.sqrt(2 * h / G)
    k = k or ch(["x", "t", "vy", "angle"])
    lead = "A ball is thrown horizontally at %d m/s from a height of %s m. Ignore air resistance (g = 9.81 m/s²). " % (u, nf(h, 2))
    if k == "t":
        return nq(lead + "How long is it in the air?", t, [h / u, math.sqrt(h / G), 2 * h / G], " s", "Vertically: h = ½gt², t = <b>%s s</b>." % nf(t))
    if k == "x":
        return nq(lead + "How far does it travel horizontally?", u * t, [u * h / G, u * math.sqrt(h / G), u * 2 * t], " m", "t = %s s, x = ut = <b>%s m</b>." % (nf(t), nf(u * t)))
    if k == "vy":
        return nq(lead + "Calculate its vertical velocity as it lands.", G * t, [math.sqrt(2 * G * h) + u, u, G * h], " m/s", "v<sub>y</sub> = gt = √(2gh) = <b>%s m/s</b>." % nf(G * t))
    U0, ang = ch([10, 12, 15, 20, 25, 30]), ch([20, 30, 40, 45, 50, 60, 70])
    T = 2 * U0 * math.sin(math.radians(ang)) / G
    rng = U0 * math.cos(math.radians(ang)) * T
    return nq("A ball is kicked at %d m/s at %d° above level ground. Ignoring air resistance, calculate its range." % (U0, ang), rng,
              [U0 * T, U0 * math.sin(math.radians(ang)) * T, U0 * U0 / G], " m", "Time of flight = 2u sin θ/g = %s s. Range = u cos θ × t = <b>%s m</b>." % (nf(T), nf(rng)))


def m_energy(k=None):
    k = k or ch(["ke", "gpe", "power", "eff", "v"])
    m = ch([0.5, 2, 5, 10, 50, 60, 70, 800, 1200, 1500])
    if k == "ke":
        v = ch([2, 3, 5, 8, 10, 12, 15, 20, 25])
        return nq("Calculate the kinetic energy of a %s kg mass moving at %d m/s." % (nf(m), v), 0.5 * m * v * v, [m * v * v, 0.5 * m * v, m * v], " J", "E<sub>k</sub> = ½mv² = <b>%s J</b>." % nf(0.5 * m * v * v))
    if k == "gpe":
        h = ch([0.5, 1.2, 2, 3, 5, 10, 25, 40])
        return nq("Calculate the gain in gravitational potential energy when a %s kg mass is lifted %s m. (g = 9.81 N/kg)" % (nf(m), nf(h)), m * G * h, [m * h, 0.5 * m * G * h, m * G / h], " J", "ΔE<sub>p</sub> = mgΔh = <b>%s J</b>." % nf(m * G * h))
    if k == "power":
        W, t = ch([600, 1200, 2400, 3000, 4500, 6000, 9000, 12000]), ch([2, 3, 4, 5, 6, 8, 10, 15, 20, 30])
        return nq("A motor does %s J of work in %d s. Calculate its power output." % (nf(W, 4), t), W / t, [W * t, t / W, W / t / 60], " W", "P = W/t = <b>%s W</b>." % nf(W / t))
    if k == "v":
        h = ch([0.8, 1.25, 2, 3.2, 5, 7.2, 10, 20])
        v = math.sqrt(2 * G * h)
        return nq("A ball is dropped from %s m. Use conservation of energy to find its speed just before it lands (ignore air resistance)." % nf(h), v, [2 * G * h, G * h, math.sqrt(G * h)], " m/s", "mgh = ½mv², v = √(2gh) = <b>%s m/s</b>." % nf(v))
    inp, out = ch([(500, 350), (1200, 900), (2000, 1500), (800, 640), (2500, 1000), (60, 9), (100, 35), (40, 30)])
    return nq("A machine takes in %d J and gives out %d J of useful energy. Calculate its efficiency." % (inp, out), out / inp * 100, [inp / out * 100, (inp - out) / inp * 100, out / inp], "%",
              "Efficiency = useful out ÷ total in × 100%% = <b>%s%%</b>." % nf(out / inp * 100))


def m_momentum(k=None):
    m1, m2 = ch([0.5, 1, 1.5, 2, 3, 4, 800, 1200]), ch([0.5, 1, 2, 2.5, 3, 5, 1000, 1500])
    if (m1 > 100) != (m2 > 100):
        return None
    u1 = ch([2, 3, 4, 5, 6, 8, 10, 12, 15])
    k = k or ch(["stick", "p", "imp"])
    if k == "p":
        return nq("Calculate the momentum of a %s kg object moving at %d m/s." % (nf(m1), u1), m1 * u1, [0.5 * m1 * u1 * u1, m1 / u1, m1 * u1 * u1], " kg m/s", "p = mv = <b>%s kg m/s</b>." % nf(m1 * u1))
    if k == "imp":
        F, t = ch([20, 50, 100, 200, 400, 1500, 3000]), ch([0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
        return nq("A force of %d N acts for %s s. Calculate the change in momentum." % (F, nf(t)), F * t, [F / t, t / F, F * t * t], " N s", "Impulse = FΔt = <b>%s N s</b>." % nf(F * t))
    v = m1 * u1 / (m1 + m2)
    return nq("A %s kg trolley moving at %d m/s collides with a stationary %s kg trolley and they stick together. Calculate their speed just after the collision." % (nf(m1), u1, nf(m2)), v,
              [u1 * m2 / (m1 + m2), m1 * u1 / m2, u1 / 2 if m1 != m2 else u1], " m/s", "Momentum is conserved: %s × %d = (%s + %s)v, v = <b>%s m/s</b>." % (nf(m1), u1, nf(m1), nf(m2), nf(v)))


MATS = [("steel", 2.0e11), ("copper", 1.2e11), ("aluminium", 7.0e10), ("brass", 1.0e11), ("nylon", 3.0e9), ("glass", 7.0e10), ("titanium", 1.1e11)]


def m_materials(k=None):
    k = k or ch(["hooke", "stress", "strain", "E", "energy", "density"])
    if k == "hooke":
        F, x = ch([2, 4, 5, 6, 8, 10, 12, 20, 25]), ch([0.01, 0.02, 0.025, 0.04, 0.05, 0.08, 0.1])
        return nq("A spring extends by %s m when a %d N force is applied. Calculate its spring constant." % (nf(x), F), F / x, [F * x, x / F, F / x / 100], " N/m", "k = F/ΔL = <b>%s N/m</b>." % nf(F / x))
    if k == "energy":
        F, x = ch([5, 10, 20, 40, 50, 80, 100, 150]), ch([0.02, 0.04, 0.05, 0.1, 0.15, 0.2])
        return nq("A wire is stretched by %s m by a force that rises steadily to %d N (within the limit of proportionality). Calculate the elastic strain energy stored." % (nf(x), F),
                  0.5 * F * x, [F * x, 0.5 * F * x * x, F / x], " J", "E = ½FΔL = <b>%s J</b>." % nf(0.5 * F * x))
    if k == "density":
        m, V = ch([0.27, 0.54, 0.79, 1.13, 2.7, 7.9, 8.9, 19.3]), ch([1e-4, 2e-4, 5e-4, 1e-3])
        return nq("A block has a mass of %s kg and a volume of %s m³. Calculate its density." % (nf(m), nf(V)), m / V, [m * V, V / m, m / V / 1000], " kg/m³", "ρ = m/V = <b>%s kg/m³</b>." % nf(m / V))
    mat, Ey = ch(MATS)
    d = ch([0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2])  # mm diameter
    A = math.pi * (d * 1e-3 / 2) ** 2
    F = ch([20, 40, 50, 60, 80, 100, 150])
    L = ch([1.0, 1.5, 2.0, 2.5, 3.0])
    stress = F / A
    strain = stress / Ey
    if k == "stress":
        return nq("A %s wire of diameter %s mm supports a load of %d N. Calculate the tensile stress in the wire." % (mat, nf(d, 2), F), stress,
                  [F / (math.pi * (d * 1e-3) ** 2), F / (math.pi * (d * 1e-3 / 2)), F / A / 1e6], " Pa", "A = π(d/2)² = %s m². σ = F/A = <b>%s Pa</b>." % (nf(A), nf(stress)))
    if k == "strain":
        dl = strain * L
        if dl > 0.01:
            return None
        return nq("A %s m %s wire stretches by %s mm under a load. Calculate the tensile strain." % (nf(L, 2), mat, nf(dl * 1000)), strain, [dl * 1000 / L, L / dl, strain * 100], "",
                  "Strain = ΔL/L = %s ÷ %s = <b>%s</b> (no unit)." % (nf(dl), nf(L, 2), nf(strain)))
    dl = strain * L
    if dl > 0.01:
        return None
    return nq("A wire %s m long and %s mm in diameter stretches %s mm under a %d N load. Calculate the Young modulus of the material." % (nf(L, 2), nf(d, 2), nf(dl * 1000), F), Ey,
              [F * L / (math.pi * (d * 1e-3) ** 2 * dl), F * dl / (A * L), Ey / 1000], " Pa", "E = stress/strain = FL/(AΔL) = <b>%s Pa</b>." % nf(Ey))


# =================================================================== Year 12: electricity
def e_charge(k=None):
    k = k or ch(["Q", "N", "I", "V"])
    I, t = ch([0.2, 0.5, 1.5, 2, 2.5, 3, 4, 5]), ch([10, 20, 30, 60, 120, 300, 600])
    if k == "Q":
        return nq("A current of %s A flows for %d s. Calculate the charge that passes." % (nf(I), t), I * t, [I / t, t / I, I * t / 60], " C", "Q = It = <b>%s C</b>." % nf(I * t))
    if k == "N":
        Q = I * t
        return nq("A current of %s A flows for %d s. How many electrons pass a point?" % (nf(I), t), Q / E, [Q * E, Q, I / E], "", "Q = It = %s C. N = Q/e = <b>%s</b>." % (nf(Q), nf(Q / E)))
    if k == "V":
        W, Q = ch([12, 24, 36, 45, 60, 90, 180]), ch([2, 3, 4, 5, 6, 8, 10, 15])
        return nq("%d J of energy is transferred when %d C of charge passes through a component. Calculate the potential difference across it." % (W, Q), W / Q, [W * Q, Q / W, W / Q / 2], " V", "V = W/Q = <b>%s V</b>." % nf(W / Q))
    Q = ch([6, 12, 30, 45, 90, 120, 360])
    return nq("%d C of charge flows in %d s. Calculate the current." % (Q, t), Q / t, [Q * t, t / Q, Q / t * 60], " A", "I = Q/t = <b>%s A</b>." % nf(Q / t))


WIRES = [("copper", 1.7e-8), ("aluminium", 2.8e-8), ("nichrome", 1.1e-6), ("constantan", 4.9e-7), ("tungsten", 5.6e-8), ("iron", 1.0e-7)]


def e_resist(k=None):
    k = k or ch(["ohm", "rho", "rho2"])
    if k == "ohm":
        V, I = ch([1.5, 3, 4.5, 6, 9, 12, 230]), ch([0.05, 0.1, 0.2, 0.25, 0.5, 1.5, 2])
        return nq("A potential difference of %s V drives a current of %s A through a resistor. Calculate its resistance." % (nf(V), nf(I)), V / I, [V * I, I / V, V / I / 1000], " Ω", "R = V/I = <b>%s Ω</b>." % nf(V / I))
    w, rho = ch(WIRES)
    L, d = ch([0.5, 1.0, 1.5, 2.0, 5.0, 10.0]), ch([0.2, 0.25, 0.3, 0.4, 0.5, 0.8, 1.0])
    A = math.pi * (d * 1e-3 / 2) ** 2
    Rw = rho * L / A
    if k == "rho":
        return nq("Calculate the resistance of a %s m length of %s wire of diameter %s mm (resistivity %s Ω m)." % (nf(L), w, nf(d, 2), nf(rho, 2)), Rw,
                  [rho * L / (math.pi * (d * 1e-3) ** 2), rho * A / L, rho * L / (d * 1e-3)], " Ω", "A = π(d/2)² = %s m². R = ρL/A = <b>%s Ω</b>." % (nf(A), nf(Rw)))
    return nq("A wire %s m long with cross-sectional area %s m² has a resistance of %s Ω. Calculate the resistivity of the material." % (nf(L), nf(A), nf(Rw)), rho,
              [Rw * L / A, Rw / (A * L), Rw * A], " Ω m", "ρ = RA/L = <b>%s Ω m</b>." % nf(rho))


def e_combo(k=None):
    r1, r2, r3 = R.sample([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 47, 100], 3)
    k = k or ch(["par2", "par3", "mix", "ser"])
    if k == "ser":
        return nq("Resistors of %d Ω, %d Ω and %d Ω are connected in series. Calculate the total resistance." % (r1, r2, r3), r1 + r2 + r3,
                  [1 / (1 / r1 + 1 / r2 + 1 / r3), (r1 + r2 + r3) / 3, r1 * r2 * r3 / (r1 + r2 + r3)], " Ω", "In series, R = R₁ + R₂ + R₃ = <b>%d Ω</b>." % (r1 + r2 + r3))
    if k == "par2":
        t = r1 * r2 / (r1 + r2)
        return nq("Resistors of %d Ω and %d Ω are connected in parallel. Calculate the total resistance." % (r1, r2), t, [r1 + r2, (r1 + r2) / 2, 1 / r1 + 1 / r2], " Ω", "1/R = 1/%d + 1/%d, R = <b>%s Ω</b>." % (r1, r2, nf(t)))
    if k == "par3":
        t = 1 / (1 / r1 + 1 / r2 + 1 / r3)
        return nq("Resistors of %d Ω, %d Ω and %d Ω are connected in parallel. Calculate the total resistance." % (r1, r2, r3), t, [r1 + r2 + r3, 1 / r1 + 1 / r2 + 1 / r3, (r1 + r2 + r3) / 3], " Ω", "1/R = 1/%d + 1/%d + 1/%d, R = <b>%s Ω</b>." % (r1, r2, r3, nf(t)))
    t = r1 + r2 * r3 / (r2 + r3)
    return nq("A %d Ω resistor is in series with a parallel pair of %d Ω and %d Ω. Calculate the total resistance." % (r1, r2, r3), t, [r1 + r2 + r3, 1 / (1 / r1 + 1 / r2 + 1 / r3), r1 + (r2 + r3) / 2], " Ω",
              "Parallel pair = %s Ω, plus %d Ω = <b>%s Ω</b>." % (nf(r2 * r3 / (r2 + r3)), r1, nf(t)))


def e_power(k=None):
    k = k or ch(["IV", "I2R", "V2R", "kwh"])
    if k == "IV":
        I, V = ch([0.5, 2, 3, 4.5, 5, 8, 10, 13]), ch([6, 12, 24, 230])
        return nq("A heater draws %s A from a %d V supply. Calculate its power." % (nf(I), V), I * V, [V / I, I * I * V, I * V / 1000], " W", "P = IV = <b>%s W</b>." % nf(I * V))
    if k == "I2R":
        I, Rr = ch([0.2, 0.5, 1.5, 2, 3, 4, 5]), ch([2, 5, 10, 12, 20, 50, 100])
        return nq("A current of %s A flows through a %d Ω resistor. Calculate the power dissipated." % (nf(I), Rr), I * I * Rr, [I * Rr, I * Rr * Rr, I * I / Rr], " W", "P = I²R = <b>%s W</b>." % nf(I * I * Rr))
    if k == "V2R":
        V, Rr = ch([3, 6, 9, 12, 24, 230]), ch([4, 6, 8, 12, 24, 48, 100, 1000])
        return nq("A %d Ω resistor is connected across %d V. Calculate the power." % (Rr, V), V * V / Rr, [V / Rr, V * Rr, V * V * Rr], " W", "P = V²/R = <b>%s W</b>." % nf(V * V / Rr))
    P, t = ch([0.5, 1.5, 2, 2.5, 3, 9]), ch([0.5, 1.5, 2, 3, 4, 6])
    return nq("A %s kW appliance runs for %s hours. Calculate the energy transferred in joules." % (nf(P), nf(t)), P * 1000 * t * 3600, [P * t, P * 1000 * t, P * t * 3600], " J",
              "E = Pt = %s W × %s s = <b>%s J</b>." % (nf(P * 1000), nf(t * 3600), nf(P * 1000 * t * 3600)))


def e_divider():
    Vin = ch([5, 6, 9, 12, 15, 24])
    r1, r2 = R.sample([100, 200, 220, 330, 470, 1000, 2200, 4700, 10000], 2)
    out = Vin * r2 / (r1 + r2)
    return nq("A potential divider has R₁ = %s Ω (top) and R₂ = %s Ω (bottom) across a %d V supply. Calculate the output voltage across R₂." % (nf(r1, 4), nf(r2, 4), Vin), out,
              [Vin * r1 / (r1 + r2), Vin * r2 / r1, Vin / 2], " V", "V<sub>out</sub> = V<sub>in</sub> × R₂/(R₁ + R₂) = <b>%s V</b>." % nf(out))


def e_emf(k=None):
    emf, r = ch([1.5, 3.0, 4.5, 6.0, 9.0, 12.0]), ch([0.2, 0.5, 0.8, 1.0, 1.5, 2.0])
    Rl = ch([2, 3, 4, 5, 8, 10, 12, 20])
    I = emf / (Rl + r)
    k = k or ch(["I", "V", "r", "lost"])
    if k == "I":
        return nq("A cell of e.m.f. %s V and internal resistance %s Ω is connected to a %d Ω resistor. Calculate the current." % (nf(emf), nf(r), Rl), I, [emf / Rl, emf / r, emf / (Rl - r) if Rl > r else emf * Rl], " A", "I = ε/(R + r) = <b>%s A</b>." % nf(I))
    if k == "V":
        return nq("A cell of e.m.f. %s V and internal resistance %s Ω is connected to a %d Ω resistor. Calculate the terminal potential difference." % (nf(emf), nf(r), Rl), I * Rl, [emf, I * r, emf + I * r], " V",
                  "I = %s A. V = IR = <b>%s V</b>." % (nf(I), nf(I * Rl)))
    if k == "lost":
        return nq("A cell of e.m.f. %s V and internal resistance %s Ω drives a current through a %d Ω resistor. Calculate the lost volts." % (nf(emf), nf(r), Rl), I * r, [I * Rl, emf * r, emf - I * r], " V",
                  "I = %s A. Lost volts = Ir = <b>%s V</b>." % (nf(I), nf(I * r)))
    V = I * Rl
    return nq("A cell of e.m.f. %s V gives a terminal p.d. of %s V when the current is %s A. Calculate its internal resistance." % (nf(emf), nf(V), nf(I)), r, [V / I, emf / I, (emf + V) / I], " Ω", "r = (ε − V)/I = <b>%s Ω</b>." % nf(r))


# =================================================================== Year 13: circular motion and oscillations
def c_circ(k=None):
    k = k or ch(["w", "v", "a", "F", "rpm"])
    r = ch([0.2, 0.3, 0.5, 0.8, 1.2, 2.0, 5.0, 25, 50])
    if k == "rpm":
        n = ch([30, 45, 60, 78, 120, 300, 600, 1200, 3000])
        w = 2 * math.pi * n / 60
        return nq("A wheel turns at %d revolutions per minute. Calculate its angular speed." % n, w, [n / 60, 2 * math.pi * n, n * 60 / (2 * math.pi)], " rad/s", "ω = 2πf = 2π × %s = <b>%s rad/s</b>." % (nf(n / 60), nf(w)))
    T = ch([0.5, 1, 2, 2.5, 4, 5, 8, 10])
    w = 2 * math.pi / T
    v = w * r
    if k == "w":
        return nq("An object goes round a circle once every %s s. Calculate its angular speed." % nf(T), w, [1 / T, 2 * math.pi * T, math.pi / T], " rad/s", "ω = 2π/T = <b>%s rad/s</b>." % nf(w))
    if k == "v":
        return nq("An object moves in a circle of radius %s m with period %s s. Calculate its linear speed." % (nf(r), nf(T)), v, [r / T, 2 * math.pi * T / r, w], " m/s", "v = 2πr/T = <b>%s m/s</b>." % nf(v))
    if k == "a":
        return nq("An object moves at %s m/s in a circle of radius %s m. Calculate its centripetal acceleration." % (nf(v), nf(r)), v * v / r, [v / r, v * v * r, v * r], " m/s²", "a = v²/r = <b>%s m/s²</b>." % nf(v * v / r))
    m = ch([0.1, 0.2, 0.5, 1, 2, 60, 800, 1200])
    return nq("A %s kg mass moves at %s m/s in a circle of radius %s m. Calculate the centripetal force." % (nf(m), nf(v), nf(r)), m * v * v / r, [m * v / r, m * v * v * r, m * v * v / (2 * r)], " N", "F = mv²/r = <b>%s N</b>." % nf(m * v * v / r))


def c_shm(k=None):
    k = k or ch(["spring", "pend", "vmax", "amax", "f", "x"])
    if k == "spring":
        m, kk = ch([0.1, 0.2, 0.25, 0.4, 0.5, 1.0, 2.0]), ch([10, 20, 25, 40, 50, 80, 100, 200])
        T = 2 * math.pi * math.sqrt(m / kk)
        return nq("A %s kg mass oscillates on a spring of stiffness %d N/m. Calculate the period." % (nf(m), kk), T, [2 * math.pi * math.sqrt(kk / m), 2 * math.pi * m / kk, math.sqrt(m / kk)], " s", "T = 2π√(m/k) = <b>%s s</b>." % nf(T))
    if k == "pend":
        l = ch([0.25, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5])
        T = 2 * math.pi * math.sqrt(l / G)
        return nq("Calculate the period of a simple pendulum of length %s m. (g = 9.81 m/s²)" % nf(l), T, [2 * math.pi * math.sqrt(G / l), 2 * math.pi * l / G, math.sqrt(l / G)], " s", "T = 2π√(l/g) = <b>%s s</b>." % nf(T))
    A, f = ch([0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15]), ch([0.5, 1, 1.5, 2, 2.5, 4, 5])
    w = 2 * math.pi * f
    if k == "vmax":
        return nq("An object moves with simple harmonic motion of amplitude %s m and frequency %s Hz. Calculate its maximum speed." % (nf(A), nf(f)), w * A, [f * A, w * w * A, w / A], " m/s", "v<sub>max</sub> = ωA = 2π × %s × %s = <b>%s m/s</b>." % (nf(f), nf(A), nf(w * A)))
    if k == "amax":
        return nq("An object moves with SHM of amplitude %s m and frequency %s Hz. Calculate its maximum acceleration." % (nf(A), nf(f)), w * w * A, [w * A, f * f * A, w * w / A], " m/s²", "a<sub>max</sub> = ω²A = <b>%s m/s²</b>." % nf(w * w * A))
    if k == "f":
        T = 1 / f
        return nq("An oscillator completes %d oscillations in %s s. Calculate its frequency." % (int(f * 10), nf(10.0)), f, [T, f * 2 * math.pi, 10 / f], " Hz", "f = number ÷ time = %d ÷ 10 = <b>%s Hz</b>." % (int(f * 10), nf(f))) if f * 10 == int(f * 10) else None
    t = ch([0.05, 0.1, 0.15, 0.2, 0.3])
    x = A * math.cos(w * t)
    if abs(x) < 1e-4:
        return None
    return nq("An oscillator released from x = %s m at t = 0 has frequency %s Hz. Calculate its displacement at t = %s s." % (nf(A), nf(f), nf(t)), x, [A * math.sin(w * t), A * math.cos(f * t), A * math.cos(math.radians(w * t))], " m",
              "x = A cos(ωt) with ωt in radians = %s, x = <b>%s m</b>." % (nf(w * t), nf(x)))


# =================================================================== Year 13: thermal physics
LIQ = [("water", 4200), ("aluminium", 900), ("copper", 390), ("iron", 450), ("oil", 2000), ("concrete", 880), ("lead", 130)]


def t_heat(k=None):
    k = k or ch(["Q", "dT", "latent", "melt", "mix"])
    if k in ("Q", "dT"):
        s, c = ch(LIQ)
        m, dT = ch([0.2, 0.25, 0.5, 0.8, 1.0, 1.5, 2.0]), ch([5, 10, 15, 20, 25, 40, 60])
        Q = m * c * dT
        if k == "Q":
            return nq("How much energy is needed to raise the temperature of %s kg of %s (c = %d J kg⁻¹ K⁻¹) by %d K?" % (nf(m), s, c, dT), Q, [c * dT, m * c, m * c * (dT + 273)], " J", "Q = mcΔθ = <b>%s J</b>." % nf(Q))
        return nq("%s J of energy is supplied to %s kg of %s (c = %d J kg⁻¹ K⁻¹). Calculate the temperature rise." % (nf(Q), nf(m), s, c), dT, [Q / c, Q * m / c, Q / (m * c) + 273], " K", "Δθ = Q/(mc) = <b>%s K</b>." % nf(dT))
    if k == "latent":
        m = ch([0.05, 0.1, 0.2, 0.25, 0.5, 1.2])
        return nq("Calculate the energy needed to boil away %s kg of water at 100 °C (specific latent heat of vaporisation 2.26 × 10<sup>6</sup> J/kg)." % nf(m), m * 2.26e6, [2.26e6 / m, m * 3.34e5, m * 4200 * 100], " J", "Q = mL = <b>%s J</b>." % nf(m * 2.26e6))
    if k == "melt":
        m = ch([0.02, 0.05, 0.1, 0.15, 0.2, 0.4])
        return nq("Calculate the energy needed to melt %s kg of ice at 0 °C (specific latent heat of fusion 3.34 × 10<sup>5</sup> J/kg)." % nf(m), m * 3.34e5, [3.34e5 / m, m * 2.26e6, m * 2100 * 273], " J", "Q = mL = <b>%s J</b>." % nf(m * 3.34e5))
    m1, t1, m2, t2 = ch([0.1, 0.2, 0.3]), ch([60, 70, 80, 90]), ch([0.1, 0.2, 0.4]), ch([10, 15, 20])
    T = (m1 * t1 + m2 * t2) / (m1 + m2)
    return nq("%s kg of water at %d °C is mixed with %s kg of water at %d °C. Assuming no energy is lost, calculate the final temperature." % (nf(m1), t1, nf(m2), t2), T, [(t1 + t2) / 2, (m1 * t2 + m2 * t1) / (m1 + m2), t1 - t2], " °C",
              "Energy lost by the hot water = energy gained by the cold: T = (m₁θ₁ + m₂θ₂)/(m₁ + m₂) = <b>%s °C</b>." % nf(T))


def t_gas(k=None):
    k = k or ch(["pV", "n", "boyle", "charles", "ke", "rms", "N"])
    if k in ("pV", "n", "N"):
        n, T, V = ch([0.1, 0.25, 0.5, 1, 2, 3]), ch([273, 290, 300, 310, 350, 400]), ch([0.001, 0.0025, 0.005, 0.01, 0.024, 0.05])
        p = n * RG * T / V
        if k == "pV":
            return nq("Calculate the pressure of %s mol of an ideal gas in a volume of %s m³ at %d K." % (nf(n), nf(V), T), p, [n * RG * (T - 273) / V if T > 273 else n * T / V, n * RG * T * V, n * T / V], " Pa", "p = nRT/V = <b>%s Pa</b>." % nf(p))
        if k == "N":
            N = p * V / (KB * T)
            return nq("A gas at %s Pa and %d K occupies %s m³. How many molecules are there? (k = 1.38 × 10<sup>−23</sup> J/K)" % (nf(p), T, nf(V)), N, [p * V / (RG * T), p * V * KB * T, N / NA], "", "N = pV/(kT) = <b>%s</b>." % nf(N))
        return nq("A gas at %s Pa occupies %s m³ at %d K. How many moles are there?" % (nf(p), nf(V), T), n, [p * V / T, p * V * RG * T, p / (RG * T)], " mol", "n = pV/(RT) = <b>%s mol</b>." % nf(n))
    if k == "boyle":
        p1, V1, V2 = ch([100, 120, 150, 200, 250]), ch([2.0, 3.0, 4.0, 5.0, 6.0]), ch([1.0, 1.5, 2.5, 8.0, 10.0])
        return nq("A gas at %d kPa occupies %s dm³. It is compressed or expanded to %s dm³ at constant temperature. Calculate the new pressure." % (p1, nf(V1), nf(V2)), p1 * V1 / V2, [p1 * V2 / V1, p1 * V1 * V2, p1], " kPa", "p₁V₁ = p₂V₂, p₂ = <b>%s kPa</b>." % nf(p1 * V1 / V2))
    if k == "charles":
        V1, c1, c2 = ch([1.0, 2.0, 2.5, 3.0, 4.0]), ch([0, 15, 20, 27, 50]), ch([60, 100, 127, 177, 227])
        V2 = V1 * (c2 + 273) / (c1 + 273)
        return nq("A gas occupies %s dm³ at %d °C. It is heated to %d °C at constant pressure. Calculate its new volume." % (nf(V1), c1, c2), V2, [V1 * c2 / c1 if c1 else V1 * c2, V1 * (c1 + 273) / (c2 + 273), V1 * (c2 - c1)], " dm³",
                  "V/T is constant with T in kelvin: V₂ = %s × %d/%d = <b>%s dm³</b>." % (nf(V1), c2 + 273, c1 + 273, nf(V2)))
    T = ch([200, 273, 293, 300, 350, 500, 1000, 5800])
    if k == "ke":
        return nq("Calculate the mean kinetic energy of a gas molecule at %d K." % T, 1.5 * KB * T, [KB * T, 1.5 * RG * T, 0.5 * KB * T], " J", "E<sub>k</sub> = (3/2)kT = <b>%s J</b>." % nf(1.5 * KB * T))
    gas, M = ch([("nitrogen", 0.028), ("oxygen", 0.032), ("helium", 0.004), ("hydrogen", 0.002), ("carbon dioxide", 0.044)])
    m = M / NA
    v = math.sqrt(3 * KB * T / m)
    return nq("Calculate the root-mean-square speed of %s molecules (molar mass %s kg/mol) at %d K." % (gas, nf(M), T), v, [3 * KB * T / m, math.sqrt(KB * T / m), math.sqrt(3 * RG * T / M) / 2], " m/s",
              "½m c<sub>rms</sub>² = (3/2)kT, c<sub>rms</sub> = √(3kT/m) = <b>%s m/s</b>." % nf(v))


# =================================================================== Year 13: gravitational and electric fields
PLAN = [("Earth", 5.97e24, 6.37e6), ("the Moon", 7.35e22, 1.74e6), ("Mars", 6.42e23, 3.39e6), ("Jupiter", 1.90e27, 6.99e7), ("Venus", 4.87e24, 6.05e6)]


def f_grav(k=None):
    k = k or ch(["g", "F", "orbitv", "orbitT", "V", "h"])
    p, M, r = ch(PLAN)
    if k == "g":
        return nq("Calculate the gravitational field strength at the surface of %s (mass %s kg, radius %s m)." % (p, nf(M), nf(r)), GG * M / r ** 2, [GG * M / r, GG * M * r ** 2, GG * M / (2 * r) ** 2], " N/kg", "g = GM/r² = <b>%s N/kg</b>." % nf(GG * M / r ** 2))
    if k == "V":
        return nq("Calculate the gravitational potential at the surface of %s (mass %s kg, radius %s m)." % (p, nf(M), nf(r)), -GG * M / r, [GG * M / r, -GG * M / r ** 2, -GG * M * r], " J/kg", "V = −GM/r = <b>%s J/kg</b>." % nf(-GG * M / r))
    if k == "h":
        alt = ch([200, 400, 800, 2000, 20000, 36000]) * 1e3
        if p != "Earth":
            return None
        rr = r + alt
        return nq("A satellite orbits %s km above Earth's surface (Earth mass 5.97 × 10<sup>24</sup> kg, radius 6.37 × 10<sup>6</sup> m). Calculate the gravitational field strength there." % "{:,}".format(int(alt / 1000)),
                  GG * M / rr ** 2, [GG * M / alt ** 2, GG * M / rr, GG * M / r ** 2], " N/kg", "r = R + h = %s m. g = GM/r² = <b>%s N/kg</b>." % (nf(rr), nf(GG * M / rr ** 2)))
    if k == "F":
        m1, m2, d = ch([50, 60, 70, 100, 1000]), ch([60, 80, 1000, 5000]), ch([0.5, 1, 2, 5, 10])
        F = GG * m1 * m2 / d ** 2
        return nq("Calculate the gravitational force between masses of %d kg and %d kg that are %s m apart." % (m1, m2, nf(d)), F, [GG * m1 * m2 / d, m1 * m2 / d ** 2, GG * (m1 + m2) / d ** 2], " N", "F = Gm₁m₂/r² = <b>%s N</b>." % nf(F))
    if k == "kep":
        r1, T1 = ch([(1.0, 1.0), (1.0, 365)]), None
        a2 = ch([0.39, 0.72, 1.52, 2.8, 5.2, 9.5, 19.2])
        T1 = 1.0
        T2 = T1 * a2 ** 1.5
        return nq("Earth orbits the Sun at 1.0 AU with a period of 1.0 year. Use Kepler's third law (T² ∝ r³) to find the period of a planet orbiting at %s AU." % nf(a2), T2,
                  [a2 ** 2, a2 ** (2 / 3), a2], " years", "T² ∝ r³, so T = %s<sup>3/2</sup> = <b>%s years</b>." % (nf(a2), nf(T2)))
    alt = ch([250, 300, 350, 400, 500, 600, 800, 1000, 1500, 2000, 5000, 10000, 20000, 25000]) * 1e3
    if p != "Earth":
        p, M, r = PLAN[0]
    rr = r + alt
    v = math.sqrt(GG * M / rr)
    if k == "orbitv":
        return nq("A satellite orbits %s km above Earth's surface (Earth mass 5.97 × 10<sup>24</sup> kg, radius 6.37 × 10<sup>6</sup> m). Calculate its orbital speed." % "{:,}".format(int(alt / 1000)), v,
                  [math.sqrt(GG * M / alt), GG * M / rr, math.sqrt(2 * GG * M / rr)], " m/s", "v = √(GM/r) with r = %s m: <b>%s m/s</b>." % (nf(rr), nf(v)))
    T = 2 * math.pi * rr / v
    return nq("A satellite orbits %s km above Earth's surface (Earth mass 5.97 × 10<sup>24</sup> kg, radius 6.37 × 10<sup>6</sup> m). Calculate its orbital period." % "{:,}".format(int(alt / 1000)), T,
              [2 * math.pi * alt / math.sqrt(GG * M / alt), rr / v, T / 60], " s", "T = 2πr/v (or T² = 4π²r³/GM) = <b>%s s</b>." % nf(T))


def f_elec(k=None):
    k = k or ch(["coul", "E", "plates", "Vpt", "force"])
    if k == "coul":
        q1, q2, r = ch([1, 2, 3, 4, 5, 8]) * 1e-6, ch([1, 2, 5, 6, 10]) * 1e-6, ch([0.02, 0.05, 0.1, 0.2, 0.3, 0.5])
        F = KC * q1 * q2 / r ** 2
        return nq("Two point charges of %s C and %s C are %s m apart in air. Calculate the force between them. (1/4πε₀ = 8.99 × 10<sup>9</sup> N m² C⁻²)" % (nf(q1), nf(q2), nf(r)), F,
                  [KC * q1 * q2 / r, q1 * q2 / r ** 2, KC * (q1 + q2) / r ** 2], " N", "F = Q₁Q₂/(4πε₀r²) = <b>%s N</b>." % nf(F))
    if k == "E":
        q, r = ch([1, 2, 5, 10, 20]) * 1e-9, ch([0.01, 0.02, 0.05, 0.1, 0.2])
        return nq("Calculate the electric field strength %s m from a point charge of %s C." % (nf(r), nf(q)), KC * q / r ** 2, [KC * q / r, q / r ** 2, KC * q * r ** 2], " N/C", "E = Q/(4πε₀r²) = <b>%s N/C</b>." % nf(KC * q / r ** 2))
    if k == "Vpt":
        q, r = ch([1, 2, 5, 10, 20]) * 1e-9, ch([0.01, 0.02, 0.05, 0.1, 0.2])
        return nq("Calculate the electric potential %s m from a point charge of +%s C." % (nf(r), nf(q)), KC * q / r, [KC * q / r ** 2, -KC * q / r, q / r], " V", "V = Q/(4πε₀r) = <b>%s V</b>." % nf(KC * q / r))
    V, d = ch([100, 200, 500, 1000, 1500, 3000, 5000]), ch([0.005, 0.01, 0.02, 0.025, 0.04, 0.05])
    Ef = V / d
    if k == "plates":
        return nq("Two parallel plates %s m apart have a potential difference of %d V between them. Calculate the field strength between them." % (nf(d), V), Ef, [V * d, d / V, V / d / 1000], " V/m", "E = V/d = <b>%s V/m</b>." % nf(Ef))
    return nq("An electron is between parallel plates %s m apart with %d V across them. Calculate the force on it." % (nf(d), V), Ef * E, [V * E, Ef / E, Ef * E * d], " N", "F = EQ = (V/d) × e = <b>%s N</b>." % nf(Ef * E))


# =================================================================== Year 13: capacitors and magnetic fields
def k_cap(k=None):
    k = k or ch(["Q", "E", "E2", "ser", "par", "tau", "dis"])
    C_ = ch([10, 22, 47, 100, 220, 470, 1000, 2200]) * 1e-6
    V = ch([1.5, 3, 5, 6, 9, 12, 25])
    cf = nf(C_ * 1e6) + " μF"
    if k == "Q":
        return nq("A %s capacitor is charged to %s V. Calculate the charge stored." % (cf, nf(V)), C_ * V, [C_ / V, V / C_, 0.5 * C_ * V], " C", "Q = CV = <b>%s C</b>." % nf(C_ * V))
    if k == "E":
        return nq("A %s capacitor is charged to %s V. Calculate the energy stored." % (cf, nf(V)), 0.5 * C_ * V * V, [C_ * V * V, 0.5 * C_ * V, C_ * V], " J", "E = ½CV² = <b>%s J</b>." % nf(0.5 * C_ * V * V))
    if k == "E2":
        Q = C_ * V
        return nq("A capacitor stores %s C of charge at %s V. Calculate the energy stored." % (nf(Q), nf(V)), 0.5 * Q * V, [Q * V, 0.5 * Q * Q / V * 2, Q / V], " J", "E = ½QV = <b>%s J</b>." % nf(0.5 * Q * V))
    c1, c2 = R.sample([10, 22, 47, 100, 220, 470], 2)
    if k == "ser":
        t = c1 * c2 / (c1 + c2)
        return nq("Capacitors of %d μF and %d μF are connected in series. Calculate the total capacitance." % (c1, c2), t, [c1 + c2, (c1 + c2) / 2, 1 / c1 + 1 / c2], " μF", "1/C = 1/%d + 1/%d, C = <b>%s μF</b>." % (c1, c2, nf(t)))
    if k == "par":
        return nq("Capacitors of %d μF and %d μF are connected in parallel. Calculate the total capacitance." % (c1, c2), c1 + c2, [c1 * c2 / (c1 + c2), (c1 + c2) / 2, abs(c1 - c2)], " μF", "In parallel, C = C₁ + C₂ = <b>%d μF</b>." % (c1 + c2))
    Rr = ch([1, 2.2, 4.7, 10, 22, 47, 100]) * 1e3
    tau = Rr * C_
    if k == "tau":
        return nq("A %s capacitor discharges through a %s kΩ resistor. Calculate the time constant." % (cf, nf(Rr / 1000)), tau, [Rr / C_, C_ / Rr, 0.69 * tau], " s", "τ = RC = <b>%s s</b>." % nf(tau))
    t = tau * ch([0.5, 1, 1.5, 2, 3])
    Q0 = C_ * V
    Qt = Q0 * math.exp(-t / tau)
    return nq("A %s capacitor charged to %s V discharges through a %s kΩ resistor. Calculate the charge left after %s s." % (cf, nf(V), nf(Rr / 1000), nf(t)), Qt,
              [Q0 * (1 - math.exp(-t / tau)), Q0 * math.exp(-tau / t), Q0 / 2], " C", "Q = Q₀e<sup>−t/RC</sup>, Q₀ = %s C, RC = %s s: Q = <b>%s C</b>." % (nf(Q0), nf(tau), nf(Qt)))


def k_mag(k=None):
    k = k or ch(["BIL", "BQv", "r", "flux", "emf", "trans", "trI"])
    if k == "BIL":
        B, I, L = ch([0.02, 0.05, 0.1, 0.2, 0.25, 0.4]), ch([0.5, 1.5, 2, 3, 4, 5]), ch([0.05, 0.1, 0.2, 0.3, 0.5])
        return nq("A wire %s m long carries %s A at right angles to a magnetic field of %s T. Calculate the force on it." % (nf(L), nf(I), nf(B)), B * I * L, [B * I / L, I * L / B, B * L], " N", "F = BIL = <b>%s N</b>." % nf(B * I * L))
    if k in ("BQv", "r"):
        B, v = ch([0.01, 0.02, 0.05, 0.1, 0.2, 0.5]), ch([1, 2, 3, 5, 8]) * 10 ** ch([5, 6])
        part, m = ch([("an electron", ME), ("a proton", 1.67e-27)])
        if k == "BQv":
            return nq("%s moves at %s m/s at right angles to a %s T magnetic field. Calculate the magnetic force on it." % (part.capitalize(), nf(v), nf(B)), B * E * v, [B * v, B * E / v, m * v * v], " N", "F = BQv = <b>%s N</b>." % nf(B * E * v))
        r = m * v / (B * E)
        return nq("%s moves at %s m/s at right angles to a %s T magnetic field. Calculate the radius of its circular path." % (part.capitalize(), nf(v), nf(B)), r, [m * v * v / (B * E), B * E / (m * v), m / (B * E)], " m",
                  "BQv = mv²/r, so r = mv/(BQ) = <b>%s m</b>." % nf(r))
    if k == "flux":
        B, a = ch([0.02, 0.05, 0.1, 0.2, 0.3, 0.5]), ch([0.01, 0.02, 0.04, 0.05, 0.1])
        N = ch([50, 100, 200, 250, 500])
        return nq("A coil of %d turns, each of area %s m², is at right angles to a %s T field. Calculate the flux linkage." % (N, nf(a), nf(B)), N * B * a, [B * a, N * B / a, N * B * a / 2], " Wb turns", "NΦ = NBA = <b>%s Wb turns</b>." % nf(N * B * a))
    if k == "emf":
        N, B, a, t = ch([50, 100, 200, 500]), ch([0.05, 0.1, 0.2, 0.4, 0.5]), ch([0.002, 0.005, 0.01, 0.02]), ch([0.01, 0.02, 0.05, 0.1, 0.2])
        return nq("A %d-turn coil of area %s m² is in a %s T field at right angles. The field falls to zero in %s s. Calculate the average induced e.m.f." % (N, nf(a), nf(B), nf(t)), N * B * a / t,
                  [B * a / t, N * B * a * t, N * B / t], " V", "ε = NΔΦ/Δt = %d × %s × %s ÷ %s = <b>%s V</b>." % (N, nf(B), nf(a), nf(t), nf(N * B * a / t)))
    Np, Ns = ch([(200, 50), (1000, 50), (500, 25), (2000, 100), (100, 500), (240, 12), (4600, 240), (50, 1000)])
    Vp = ch([12, 24, 230, 400])
    Vs = Vp * Ns / Np
    if k == "trans":
        return nq("An ideal transformer has %d turns on the primary and %d on the secondary. The primary voltage is %d V. Calculate the secondary voltage." % (Np, Ns, Vp), Vs, [Vp * Np / Ns, Vp * Ns * Np, Vp - Ns], " V", "V<sub>s</sub>/V<sub>p</sub> = N<sub>s</sub>/N<sub>p</sub>, V<sub>s</sub> = <b>%s V</b>." % nf(Vs))
    Ip = ch([0.1, 0.2, 0.5, 1, 2])
    return nq("An ideal transformer steps %d V to %s V. The primary current is %s A. Calculate the secondary current." % (Vp, nf(Vs), nf(Ip)), Ip * Vp / Vs, [Ip * Vs / Vp, Ip, Ip * Vp * Vs], " A", "V<sub>p</sub>I<sub>p</sub> = V<sub>s</sub>I<sub>s</sub>, I<sub>s</sub> = <b>%s A</b>." % nf(Ip * Vp / Vs))


# =================================================================== Year 13: nuclear physics
ISO = [("iodine-131", 8.0, "days"), ("radon-222", 3.8, "days"), ("cobalt-60", 5.3, "years"), ("strontium-90", 29, "years"), ("carbon-14", 5730, "years"),
       ("technetium-99m", 6.0, "hours"), ("phosphorus-32", 14, "days"), ("caesium-137", 30, "years"), ("polonium-210", 138, "days"), ("sodium-24", 15, "hours")]
UNIT_S = {"hours": 3600, "days": 86400, "years": 3.16e7}


def n_decay(k=None):
    name, T, u = ch(ISO)
    k = k or ch(["left", "frac", "lam", "A", "time"])
    if k == "left":
        N0, n = ch([800, 1000, 1600, 2400, 4000, 6400]), ch([1, 2, 3, 4, 5])
        return nq("The half-life of %s is %s %s. A sample has an activity of %d Bq. What is its activity after %s %s?" % (name, nf(T), u, N0, nf(n * T), u), N0 / 2 ** n,
                  [N0 / (2 * n), N0 - N0 / 2 ** n, N0 / 2 ** (n + 1)], " Bq", "%s %s is %d half-lives: %d ÷ 2<sup>%d</sup> = <b>%s Bq</b>." % (nf(n * T), u, n, N0, n, nf(N0 / 2 ** n)))
    if k == "frac":
        t = T * ch([0.5, 1.5, 2.5, 0.25, 3.5])
        f = 0.5 ** (t / T)
        return nq("The half-life of %s is %s %s. What fraction of a sample remains after %s %s?" % (name, nf(T), u, nf(t), u), f, [1 - f, t / T / 2, 0.5 * t / T if t < 2 * T else 1 / (t / T) ** 2], "",
                  "N/N₀ = (½)<sup>t/T½</sup> = (½)<sup>%s</sup> = <b>%s</b>." % (nf(t / T), nf(f)))
    lam = math.log(2) / (T * UNIT_S[u])
    if k == "lam":
        return nq("The half-life of %s is %s %s. Calculate its decay constant in s⁻¹." % (name, nf(T), u), lam, [math.log(2) / T, T * UNIT_S[u] / math.log(2), 1 / (T * UNIT_S[u])], " s⁻¹",
                  "λ = ln 2 / T½ = 0.693 ÷ %s s = <b>%s s⁻¹</b>." % (nf(T * UNIT_S[u]), nf(lam)))
    if k == "A":
        N = ch([1, 2, 5, 8]) * 10 ** ch([12, 15, 18, 20])
        return nq("A sample contains %s nuclei of %s (half-life %s %s). Calculate its activity." % (nf(N), name, nf(T), u), lam * N, [N / (T * UNIT_S[u]), lam * N / 2, N * math.log(2) / T], " Bq",
                  "A = λN, λ = %s s⁻¹: A = <b>%s Bq</b>." % (nf(lam), nf(lam * N)))
    f = ch([0.1, 0.2, 0.3, 0.6, 0.75, 0.05])
    t = T * math.log(1 / f) / math.log(2)
    return nq("How long does it take for the activity of %s (half-life %s %s) to fall to %s%% of its starting value?" % (name, nf(T), u, nf(f * 100, 2)), t, [T / f, T * f * 2, T * math.log(f) / math.log(0.5) / 2], " " + u,
              "t = T½ × ln(1/f)/ln 2 = <b>%s %s</b>." % (nf(t), u))


def n_nuclear(k=None):
    k = k or ch(["radius", "decay", "beta", "BE", "inv", "emc"])
    if k == "radius":
        s, z, a = ch(NUC)
        r = 1.2e-15 * a ** (1 / 3)
        return nq("Calculate the radius of a %s nucleus. (r₀ = 1.2 × 10<sup>−15</sup> m)" % nuc(s, z, a), r, [1.2e-15 * a, 1.2e-15 * a ** 0.5, 1.2e-15 * z ** (1 / 3)], " m", "R = r₀A<sup>1/3</sup> = 1.2 × 10<sup>−15</sup> × %d<sup>1/3</sup> = <b>%s m</b>." % (a, nf(r)))
    if k in ("decay", "beta"):
        s, z, a = ch([x for x in NUC if x[2] > 200]) if k == "decay" else ch(NUC)
        if k == "decay":
            return tq("%s decays by alpha emission. What are the nucleon and proton numbers of the new nucleus?" % nuc(s, z, a), "A = %d, Z = %d" % (a - 4, z - 2),
                      ["A = %d, Z = %d" % (a - 2, z - 4), "A = %d, Z = %d" % (a - 4, z - 4), "A = %d, Z = %d" % (a, z - 2)], "An alpha particle is <sup>4</sup><sub>2</sub>He: A falls by 4, Z falls by 2.")
        return tq("%s decays by β⁻ emission. What are the nucleon and proton numbers of the new nucleus?" % nuc(s, z, a), "A = %d, Z = %d" % (a, z + 1),
                  ["A = %d, Z = %d" % (a, z - 1), "A = %d, Z = %d" % (a - 1, z + 1), "A = %d, Z = %d" % (a + 1, z)], "A neutron becomes a proton: A stays the same, Z goes up by 1.")
    if k == "BE":
        nm, z, a, mass = ch([("helium-4", 2, 4, 4.00151), ("carbon-12", 6, 12, 11.99671), ("oxygen-16", 8, 16, 15.99052), ("iron-56", 26, 56, 55.92068), ("lithium-7", 3, 7, 7.01436), ("nitrogen-14", 7, 14, 13.99923)])
        dm = z * 1.00728 + (a - z) * 1.00867 - mass
        be = dm * 931.5
        return nq("The nuclear mass of %s is %s u. Proton mass = 1.00728 u, neutron mass = 1.00867 u, 1 u = 931.5 MeV. Calculate the binding energy per nucleon." % (nm, nf(mass, 7)), be / a,
                  [be, dm / a, be / z], " MeV", "Mass defect = %s u. Binding energy = %s MeV. Per nucleon: ÷ %d = <b>%s MeV</b>." % (nf(dm, 4), nf(be, 4), a, nf(be / a)))
    if k == "inv":
        I1, d1, d2 = ch([200, 320, 400, 600, 800, 1200]), ch([0.1, 0.2, 0.25]), ch([0.4, 0.5, 0.6, 0.8, 1.0])
        return nq("The count rate from a gamma source is %d counts per minute at %s m (after subtracting background). What is it at %s m?" % (I1, nf(d1), nf(d2)), I1 * (d1 / d2) ** 2,
                  [I1 * d1 / d2, I1 * (d2 / d1) ** 2, I1 - (d2 - d1) * 100], " counts per minute", "Inverse square law: I ∝ 1/x², I = %d × (%s/%s)² = <b>%s</b>." % (I1, nf(d1), nf(d2), nf(I1 * (d1 / d2) ** 2)))
    m = ch([1, 2, 5, 10, 0.5, 0.1]) * 1e-3
    return nq("Calculate the energy released if %s kg of mass is converted completely into energy." % nf(m), m * C * C, [m * C, m * C * C / 2, m / C ** 2], " J", "E = mc² = <b>%s J</b>." % nf(m * C * C))


# =================================================================== unit definitions
def UNITS(year):
    global p_part
    p_part = once_maker(PART)
    if year == 12:
        return [
            U("Physics", 11, "particles-and-quantum-phenomena", "Particles and radiation",
              "Constituents of the atom, specific charge, stable and unstable nuclei, particles and antiparticles, classification of particles, quarks, conservation laws, the photoelectric effect, energy levels and photon emission, and wave–particle duality.",
              "Particles, Photons and Quantum Phenomena", "particles and quantum phenomena",
              "Free Year 12 A level physics worksheets on particles and quantum phenomena: specific charge, photon energy, the photoelectric effect, energy levels, de Broglie wavelength, quarks and leptons. 100 questions with answers.",
              "E = hf = hc/λ, and hf = φ + Ek(max).", "Convert nm to m and eV to J (× 1.60 × 10⁻¹⁹).",
              "<p>Light comes in photons of energy <i>E</i> = <i>hf</i> = <i>hc</i>/λ. In the photoelectric effect one photon frees one electron: <i>hf</i> = φ + <i>E</i><sub>k(max)</sub>. Below the threshold frequency no electrons are emitted, however bright the light.</p>"
              "<p>Electrons also behave as waves: λ = <i>h</i>/(<i>mv</i>). Hadrons are made of quarks (baryons qqq, mesons q q̄); leptons are not. Charge, baryon number and lepton number are always conserved.</p>",
              [("Find the energy of a 500 nm photon in eV.", ["E = hc/λ = 3.98 × 10<sup>−19</sup> J", "÷ 1.60 × 10<sup>−19</sup>"], "2.49 eV"),
               ("A metal has φ = 2.3 eV. Photons of 3.1 eV hit it. Find E<sub>k(max)</sub>.", ["3.1 − 2.3"], "0.8 eV")],
              ["Forgetting to change nm into m (× 10⁻⁹).", "Thinking brighter light gives faster photoelectrons.", "Mixing up baryons (three quarks) and mesons (quark and antiquark)."],
              [("What is the photoelectric equation?", "hf = φ + Ek(max): the photon energy equals the work function plus the maximum kinetic energy of the electron."),
               ("What is the de Broglie wavelength?", "λ = h/(mv). Moving particles such as electrons have a wavelength, shown by electron diffraction.")],
              lambda: [("Nuclei and specific charge", [(p_nucleus, 20)]), ("Photons and energy levels", [(p_photon, 12), (p_levels, 8)]),
                       ("The photoelectric effect", [(p_photoelectric, 20)]), ("Wave–particle duality", [(p_debroglie, 16), (p_part, 4)]),
                       ("Particles, quarks and conservation", [(p_part, 20)])]),
            U("Physics", 12, "waves-and-optics", "Waves",
              "Progressive and stationary waves, the wave equation, phase difference, refraction and refractive index, total internal reflection and optical fibres, interference and Young's double-slit experiment, diffraction and the diffraction grating.",
              "Waves, Interference and Optics", "waves and optics",
              "Free Year 12 A level physics worksheets on waves: v = fλ, phase difference, stationary waves, refraction and critical angles, Young's double slits and diffraction gratings. 100 questions with answers.",
              "v = fλ; dsinθ = nλ; w = λD/s.", "Path difference of a whole number of wavelengths gives a maximum.",
              "<p>For any wave <i>v</i> = <i>f</i>λ and <i>f</i> = 1/<i>T</i>. A stationary wave on a string fixed at both ends has λ = 2<i>L</i>/<i>n</i>. Light slows in glass: <i>n</i> = <i>c</i>/<i>v</i>, and <i>n</i>₁ sin θ₁ = <i>n</i>₂ sin θ₂. Total internal reflection happens beyond the critical angle, sin <i>C</i> = <i>n</i>₂/<i>n</i>₁.</p>"
              "<p>Coherent sources interfere: a path difference of <i>n</i>λ gives a bright fringe. Young's slits: <i>w</i> = λ<i>D</i>/<i>s</i>. A grating: <i>d</i> sin θ = <i>n</i>λ.</p>",
              [("Grating with 300 lines per mm, λ = 600 nm. Angle of first order?", ["d = 3.33 × 10<sup>−6</sup> m", "sin θ = 0.18"], "10.4°"),
               ("Critical angle for glass, n = 1.50?", ["sin C = 1/1.50"], "41.8°")],
              ["Using lines per mm as d without taking 1/N.", "Leaving the slit separation in mm.", "Using λ = L (not 2L) for the fundamental."],
              [("What is the diffraction grating equation?", "d sin θ = nλ, where d is the slit spacing (1 ÷ lines per metre) and n is the order."),
               ("When does total internal reflection happen?", "When light goes into a medium with a lower refractive index and the angle of incidence is bigger than the critical angle.")],
              lambda: [("Wave speed, frequency and wavelength", [(w_vfl, 20)]), ("Refraction and total internal reflection", [(w_refr, 20)]),
                       ("Stationary waves and phase", [(w_stationary, 10), (w_phase, 10)]), ("Young's double slits", [(w_slits, 20)]),
                       ("Diffraction gratings", [(w_grating, 20)])]),
            U("Physics", 13, "mechanics-and-materials", "Mechanics and materials",
              "Scalars and vectors, moments, motion along a straight line and projectile motion, Newton's laws, momentum and impulse, work, energy, power and efficiency, density, Hooke's law, stress, strain and the Young modulus.",
              "Mechanics and Materials", "mechanics and materials",
              "Free Year 12 A level physics worksheets on mechanics and materials: resolving forces, moments, suvat, projectiles, momentum, energy and power, Hooke's law, stress, strain and the Young modulus. 100 questions with answers.",
              "Resolve, then use suvat in each direction.", "Young modulus = stress ÷ strain = FL/(AΔL).",
              "<p>Resolve a force <i>F</i> at angle θ into <i>F</i> cos θ and <i>F</i> sin θ. For constant acceleration use the suvat equations; for projectiles treat horizontal (constant speed) and vertical (acceleration <i>g</i>) motion separately. Momentum is conserved in collisions.</p>"
              "<p>Stress = <i>F</i>/<i>A</i>, strain = Δ<i>L</i>/<i>L</i>, and the Young modulus <i>E</i> = stress/strain. Use the area of the cross-section π(<i>d</i>/2)².</p>",
              [("Ball thrown horizontally at 5 m/s from 1.8 m. Range?", ["t = √(2 × 1.8/9.81) = 0.606 s", "x = 5 × 0.606"], "3.03 m"),
               ("Wire 2.0 m, d = 0.5 mm, 50 N, ΔL = 2.5 mm. Young modulus?", ["A = 1.96 × 10<sup>−7</sup> m²", "E = (50 × 2.0)/(1.96 × 10<sup>−7</sup> × 2.5 × 10<sup>−3</sup>)"], "2.0 × 10<sup>11</sup> Pa")],
              ["Using the diameter instead of the radius for the area.", "Letting horizontal speed change in projectile motion.", "Forgetting that strain has no unit."],
              [("How do you solve a projectile problem?", "Split the motion: horizontally the speed is constant; vertically the acceleration is g. Time links the two."),
               ("What is the Young modulus?", "Tensile stress ÷ tensile strain. It measures the stiffness of a material, in pascals.")],
              lambda: [("Resolving forces and moments", [(m_resolve, 10), (m_moment, 10)]), ("Motion and suvat", [(m_suvat, 20)]),
                       ("Projectiles and momentum", [(m_proj, 12), (m_momentum, 8)]), ("Energy, power and efficiency", [(m_energy, 20)]),
                       ("Materials", [(m_materials, 20)])]),
            U("Physics", 14, "electricity", "Electricity",
              "Current, potential difference and resistance, resistivity, circuits with series and parallel resistors, energy and power, potential dividers, electromotive force and internal resistance.",
              "Electricity: Resistivity, Circuits and EMF", "electricity",
              "Free Year 12 A level physics worksheets on electricity: charge and current, resistance and resistivity, series and parallel circuits, power, potential dividers, e.m.f. and internal resistance. 100 questions with answers.",
              "ε = I(R + r); R = ρL/A.", "Parallel resistors: add the reciprocals.",
              "<p>Current is the rate of flow of charge, <i>I</i> = Δ<i>Q</i>/Δ<i>t</i>; potential difference is energy per unit charge, <i>V</i> = <i>W</i>/<i>Q</i>. Resistance <i>R</i> = <i>V</i>/<i>I</i>, and for a wire <i>R</i> = ρ<i>L</i>/<i>A</i>.</p>"
              "<p>Series: <i>R</i> = <i>R</i>₁ + <i>R</i>₂. Parallel: 1/<i>R</i> = 1/<i>R</i>₁ + 1/<i>R</i>₂. A real cell has internal resistance: ε = <i>I</i>(<i>R</i> + <i>r</i>), and the terminal p.d. is ε − <i>Ir</i>.</p>",
              [("6 Ω and 3 Ω in parallel?", ["1/R = 1/6 + 1/3 = 1/2"], "2 Ω"),
               ("ε = 6.0 V, r = 0.5 Ω, R = 5.5 Ω. Current?", ["I = 6.0 ÷ (5.5 + 0.5)"], "1.0 A")],
              ["Adding parallel resistances.", "Using the diameter in A = πr².", "Forgetting the internal resistance when finding the current."],
              [("What is resistivity?", "ρ = RA/L, a property of the material (unit Ω m), not of one particular wire."),
               ("What are lost volts?", "The p.d. across the internal resistance of a cell, Ir. The terminal p.d. is ε − Ir.")],
              lambda: [("Charge, current and potential difference", [(e_charge, 20)]), ("Resistance and resistivity", [(e_resist, 20)]),
                       ("Series and parallel circuits", [(e_combo, 14), (e_divider, 6)]), ("Power and energy", [(e_power, 20)]),
                       ("E.m.f. and internal resistance", [(e_emf, 14), (e_divider, 6)])]),
        ]
    return [
        U("Physics", 9, "circular-motion-and-oscillations", "Further mechanics",
          "Circular motion (angular speed, centripetal acceleration and force) and simple harmonic motion (defining equation, the mass–spring system and simple pendulum, maximum speed and acceleration).",
          "Circular Motion and Simple Harmonic Motion", "circular motion and oscillations",
          "Free Year 13 A level physics worksheets on circular motion and simple harmonic motion: angular speed, centripetal force, mass–spring systems, pendulums and SHM equations. 100 questions with answers.",
          "a = v²/r = ω²r; SHM: a = −ω²x.", "T = 2π√(m/k) and T = 2π√(l/g).",
          "<p>An object moving in a circle at constant speed accelerates towards the centre: <i>a</i> = <i>v</i>²/<i>r</i> = ω²<i>r</i>, with ω = 2π<i>f</i> = <i>v</i>/<i>r</i>. The resultant (centripetal) force is <i>F</i> = <i>mv</i>²/<i>r</i>.</p>"
          "<p>In simple harmonic motion <i>a</i> = −ω²<i>x</i>. The maximum speed is ω<i>A</i> and the maximum acceleration is ω²<i>A</i>. A mass on a spring: <i>T</i> = 2π√(<i>m</i>/<i>k</i>); a pendulum: <i>T</i> = 2π√(<i>l</i>/<i>g</i>).</p>",
          [("Mass 0.5 kg on a 50 N/m spring. Period?", ["T = 2π√(0.5/50)"], "0.628 s"),
           ("A = 0.05 m, f = 2 Hz. Maximum speed?", ["ω = 4π = 12.6 rad/s", "v = ωA"], "0.628 m/s")],
          ["Using f instead of ω = 2πf.", "Thinking centripetal force is a separate extra force.", "Using degrees in x = A cos ωt."],
          [("What is centripetal force?", "The resultant force towards the centre that keeps an object moving in a circle: F = mv²/r."),
           ("What defines simple harmonic motion?", "Acceleration proportional to displacement and directed towards the equilibrium position: a = −ω²x.")],
          lambda: [("Angular speed and linear speed", [(K(c_circ, "w", "rpm", "v"), 20)]), ("Centripetal force and acceleration", [(K(c_circ, "a", "F"), 20)]), ("Springs and pendulums", [(K(c_shm, "spring", "pend"), 20)]),
                   ("SHM equations", [(K(c_shm, "vmax", "amax", "x", "f"), 20)]), ("Mixed problems", [(c_circ, 10), (c_shm, 10)])]),
        U("Physics", 10, "thermal-physics-and-ideal-gases", "Thermal physics",
          "Thermal energy transfer (specific heat capacity and specific latent heat), the ideal gas laws, the equation pV = nRT = NkT, the kinetic theory model and the mean kinetic energy of molecules.",
          "Thermal Physics and Ideal Gases", "thermal physics and ideal gases",
          "Free Year 13 A level physics worksheets on thermal physics: specific heat capacity, latent heat, gas laws, pV = nRT, molecular kinetic energy and r.m.s. speed. 100 questions with answers.",
          "pV = nRT = NkT, with T in kelvin.", "Mean kinetic energy = (3/2)kT.",
          "<p>Heating: <i>Q</i> = <i>mc</i>Δθ; changing state: <i>Q</i> = <i>mL</i>. For an ideal gas <i>pV</i> = <i>nRT</i> = <i>NkT</i>, always with <i>T</i> in kelvin (°C + 273).</p>"
          "<p>Boyle's law (constant <i>T</i>): <i>pV</i> constant. Charles's law (constant <i>p</i>): <i>V</i>/<i>T</i> constant. The mean kinetic energy of a molecule is (3/2)<i>kT</i>.</p>",
          [("2.0 dm³ at 27 °C heated to 127 °C at constant pressure. New volume?", ["V/T constant", "2.0 × 400/300"], "2.67 dm³"),
           ("Mean kinetic energy at 300 K?", ["1.5 × 1.38 × 10<sup>−23</sup> × 300"], "6.21 × 10<sup>−21</sup> J")],
          ["Using °C in the gas laws.", "Using c instead of L when the state changes.", "Mixing up R (per mole) and k (per molecule)."],
          [("Why must temperatures be in kelvin?", "The gas laws are proportionalities that start from absolute zero, 0 K = −273 °C."),
           ("What is specific latent heat?", "The energy needed to change the state of 1 kg of a substance without changing its temperature.")],
          lambda: [("Specific heat capacity", [(K(t_heat, "Q", "dT"), 20)]), ("Latent heat and mixing", [(K(t_heat, "latent", "melt", "mix"), 20)]), ("Gas laws", [(K(t_gas, "boyle", "charles"), 20)]),
                   ("The ideal gas equation", [(K(t_gas, "pV", "n", "N"), 20)]), ("Kinetic theory", [(K(t_gas, "ke", "rms"), 12), (t_heat, 8)])]),
        U("Physics", 11, "gravitational-and-electric-fields", "Fields and their consequences",
          "Newton's law of gravitation, gravitational field strength and potential, orbits of planets and satellites, Coulomb's law, electric field strength (radial and uniform) and electric potential.",
          "Gravitational and Electric Fields", "gravitational and electric fields",
          "Free Year 13 A level physics worksheets on gravitational and electric fields: Newton's law of gravitation, field strength and potential, satellite orbits, Coulomb's law and uniform fields. 100 questions with answers.",
          "Radial fields follow an inverse square law.", "Measure r from the centre, not the surface.",
          "<p>Gravity: <i>F</i> = <i>Gm</i>₁<i>m</i>₂/<i>r</i>², <i>g</i> = <i>GM</i>/<i>r</i>², <i>V</i> = −<i>GM</i>/<i>r</i>. For a circular orbit gravity provides the centripetal force: <i>v</i> = √(<i>GM</i>/<i>r</i>) and <i>T</i>² ∝ <i>r</i>³.</p>"
          "<p>Electric: <i>F</i> = <i>Q</i>₁<i>Q</i>₂/(4πε₀<i>r</i>²), <i>E</i> = <i>F</i>/<i>Q</i>. Between parallel plates the field is uniform: <i>E</i> = <i>V</i>/<i>d</i>.</p>",
          [("Satellite 400 km above Earth. r?", ["r = 6.37 × 10<sup>6</sup> + 4.0 × 10<sup>5</sup>"], "6.77 × 10<sup>6</sup> m"),
           ("Plates 2 cm apart, 500 V. E?", ["E = 500 ÷ 0.02"], "2.5 × 10<sup>4</sup> V/m")],
          ["Using the height above the surface as r.", "Forgetting to square r.", "Giving gravitational potential as positive."],
          [("Why is gravitational potential negative?", "Zero potential is at infinity, and work must be done to move a mass away from a planet, so potential is less than zero nearby."),
           ("What is a uniform electric field?", "A field with the same strength everywhere, such as between parallel plates: E = V/d.")],
          lambda: [("Newton's law of gravitation", [(K(f_grav, "g", "F", "V", "h"), 20)]), ("Orbits", [(K(f_grav, "orbitv", "orbitT", "kep"), 20)]), ("Coulomb's law", [(K(f_elec, "coul", "E", "Vpt"), 20)]),
                   ("Uniform electric fields", [(K(f_elec, "plates", "force"), 20)]), ("Comparing fields", [(f_grav, 10), (f_elec, 10)])]),
        U("Physics", 12, "capacitors-and-magnetic-fields", "Fields and their consequences",
          "Capacitance, energy stored by a capacitor, charging and discharging through a resistor and the time constant; magnetic flux density, force on a current-carrying wire and on a moving charge, electromagnetic induction and transformers.",
          "Capacitors, Magnetic Fields and Induction", "capacitors and magnetic fields",
          "Free Year 13 A level physics worksheets on capacitors and magnetic fields: Q = CV, energy stored, the time constant RC, F = BIL, F = BQv, flux linkage, Faraday's law and transformers. 100 questions with answers.",
          "Q = CV; E = ½CV²; τ = RC.", "ε = NΔΦ/Δt; F = BIL; F = BQv.",
          "<p>A capacitor stores charge <i>Q</i> = <i>CV</i> and energy ½<i>QV</i> = ½<i>CV</i>². Discharging through a resistor, <i>Q</i> = <i>Q</i>₀<i>e</i><sup>−<i>t</i>/<i>RC</i></sup>; the time constant <i>RC</i> is the time to fall to 37%.</p>"
          "<p>In a magnetic field a wire feels <i>F</i> = <i>BIL</i> and a moving charge <i>F</i> = <i>BQv</i>. A changing flux linkage induces an e.m.f.: ε = <i>N</i>ΔΦ/Δ<i>t</i>. For an ideal transformer <i>V</i><sub>s</sub>/<i>V</i><sub>p</sub> = <i>N</i><sub>s</sub>/<i>N</i><sub>p</sub>.</p>",
          [("470 μF charged to 12 V. Energy?", ["½ × 470 × 10<sup>−6</sup> × 12²"], "0.0338 J"),
           ("100-turn coil, Φ falls by 0.002 Wb in 0.05 s. e.m.f.?", ["100 × 0.002 ÷ 0.05"], "4.0 V")],
          ["Forgetting to change μF into F.", "Using E = CV² without the half.", "Missing the number of turns N."],
          [("What is the time constant of a capacitor circuit?", "RC: the time for the charge (or current or p.d.) to fall to 1/e, about 37%, of its starting value."),
           ("What does Faraday's law say?", "The induced e.m.f. equals the rate of change of flux linkage: ε = NΔΦ/Δt.")],
          lambda: [("Capacitance and energy", [(K(k_cap, "Q", "E", "E2", "ser", "par"), 20)]), ("Charging and discharging", [(K(k_cap, "tau", "dis"), 20)]), ("Forces in magnetic fields", [(K(k_mag, "BIL", "BQv", "r"), 20)]),
                   ("Induction and transformers", [(K(k_mag, "flux", "emf", "trans", "trI"), 20)]), ("Mixed problems", [(k_cap, 10), (k_mag, 10)])]),
        U("Physics", 13, "nuclear-physics", "Nuclear physics",
          "Radioactive decay (half-life, decay constant, activity and exponential decay), the inverse square law for gamma radiation, nuclear radius, mass and energy, binding energy, and alpha and beta decay equations.",
          "Nuclear Physics and Radioactive Decay", "nuclear physics",
          "Free Year 13 A level physics worksheets on nuclear physics: half-life, decay constant, activity, nuclear radius, binding energy per nucleon, decay equations and the inverse square law. 100 questions with answers.",
          "A = λN and λ = ln 2 / T½.", "Binding energy comes from the mass defect: E = Δm c².",
          "<p>Radioactive decay is random but follows <i>N</i> = <i>N</i>₀<i>e</i><sup>−λ<i>t</i></sup>, with λ = ln 2/<i>T</i>½ and activity <i>A</i> = λ<i>N</i>. Use seconds when finding λ in s⁻¹.</p>"
          "<p>The nucleus has radius <i>R</i> = <i>r</i>₀<i>A</i><sup>1/3</sup>. Its mass is less than the mass of its separate nucleons; this mass defect × <i>c</i>² is the binding energy (1 u = 931.5 MeV).</p>",
          [("T½ = 8.0 days. λ?", ["8.0 days = 6.91 × 10<sup>5</sup> s", "0.693 ÷ 6.91 × 10<sup>5</sup>"], "1.00 × 10<sup>−6</sup> s⁻¹"),
           ("Activity 800 Bq, 3 half-lives later?", ["800 ÷ 2³"], "100 Bq")],
          ["Using days in A = λN without converting to seconds.", "Dividing by the number of half-lives instead of by 2 each time.", "Getting Z wrong in β⁻ decay (it goes up by 1)."],
          [("What is the decay constant?", "The probability per second that a nucleus decays: λ = ln 2 / T½."),
           ("What is binding energy?", "The energy needed to separate a nucleus into its protons and neutrons, equal to the mass defect × c².")],
          lambda: [("Half-life", [(K(n_decay, "left", "frac", "time"), 20)]), ("Decay constant and activity", [(K(n_decay, "lam", "A"), 20)]), ("Nuclear radius and decay equations", [(K(n_nuclear, "radius", "decay", "beta"), 20)]),
                   ("Mass, energy and gamma intensity", [(K(n_nuclear, "BE", "inv", "emc"), 20)]), ("Mixed problems", [(n_decay, 10), (n_nuclear, 10)])]),
    ]
