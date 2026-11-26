# -*- coding: utf-8 -*-
"""
US High School Physics: Wave-Particle Duality of Light (HS-PS4-3)
  python tools/gen_us_science_phys_wave_particle_duality.py
Evaluate the claims, evidence, and reasoning behind the idea that electromagnetic radiation can be described either by a
wave model or a particle model, and that for some situations one model is more useful than the other.
Evidence for the wave model (interference, diffraction, polarization) and the particle model (photoelectric effect,
photon detectors), photon energy E = hf = hc/λ, threshold frequency and which photons carry more energy.
Wrong answers come from real mistakes: "brighter light always ejects electrons", "red photons have more energy than
blue", "light is either a wave or a particle, not both", "E = h/f".
"""
from sci_common import Unit, item, bank, lesson, make, People
from sci_phys import num, sci, uniq, safe

U = Unit(90314)
R = U.R
P = People(R)
USED = {}
H = 6.63e-34
C = 3e8


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_photon():
    k = R.choice(["f", "l"])
    if k == "f":
        f = R.choice([1e14, 2e14, 4e14, 5e14, 6e14, 7.5e14, 1e15, 3e15, 1e16, 1e18])
        if not once(("pf", f)):
            return None
        E = H * f
        g = "%s J" % sci(E)
        return item("What is the energy of a photon with frequency %s Hz? (h = 6.63 × 10<sup>−34</sup> J·s)" % sci(f), g,
                    uniq(g, ["%s J" % sci(H / f), "%s J" % sci(f / H), "%s J" % sci(E * 10), "%s J" % sci(H * f * C)]), "E = hf = 6.63 × 10<sup>−34</sup> × %s = %s J." % (sci(f), sci(E)))
    l = R.choice([400e-9, 500e-9, 600e-9, 700e-9, 300e-9, 1e-6, 1e-3, 1e-10])
    if not once(("pl", l)):
        return None
    E = H * C / l
    g = "%s J" % sci(E)
    return item("What is the energy of a photon with wavelength %s m? (E = hc ÷ λ, h = 6.63 × 10<sup>−34</sup> J·s, c = 3.0 × 10<sup>8</sup> m/s)" % sci(l), g,
                uniq(g, ["%s J" % sci(H * l / C), "%s J" % sci(H * C * l), "%s J" % sci(E / 10), "%s J" % sci(H / l)]), "E = hc ÷ λ = %s J." % sci(E))


COL = ["red", "orange", "yellow", "green", "blue", "violet"]
SPEC = ["radio waves", "microwaves", "infrared", "visible light", "ultraviolet", "X-rays", "gamma rays"]


@safe
def g_cmp():
    if R.random() < 0.5:
        a, b = sorted(R.sample(range(6), 2))
        if not once(("cc", a, b)):
            return None
        return item("Which carries more energy per photon: %s light or %s light?" % (COL[b], COL[a]), "%s light" % COL[b], ["%s light" % COL[a], "They carry the same energy.", "It depends on brightness only."],
                    "Shorter wavelength (higher frequency) → more energy per photon.")
    a, b = sorted(R.sample(range(7), 2))
    if not once(("cs", a, b)):
        return None
    return item("Which has higher-energy photons: %s or %s?" % (SPEC[a], SPEC[b]), SPEC[b], [SPEC[a], "They have the same photon energy.", "Neither is made of photons."], "E = hf: higher frequency, more energy.")


EV = [("Light passing through two narrow slits makes bright and dark bands on a screen.", "wave"), ("Light spreads out after passing through a tiny opening.", "wave"),
      ("Polarized sunglasses block glare from a road.", "wave"), ("Soap bubbles show colored bands.", "wave"), ("Light bends when it goes from air into water.", "wave"),
      ("Ultraviolet light knocks electrons off a metal plate, but red light does not, no matter how bright.", "particle"),
      ("A very dim light makes a detector click one photon at a time.", "particle"), ("A solar cell produces current only when light above a certain frequency hits it.", "particle"),
      ("A digital camera sensor counts individual photons hitting each pixel.", "particle"), ("X-rays scatter off electrons like colliding balls and lose energy.", "particle")]


@safe
def g_model():
    s, m = R.choice(EV)
    if not once(("md", s)):
        return None
    g = "the %s model" % m
    return item("%s Which model of light explains this best?" % s, g, ["the %s model" % ("particle" if m == "wave" else "wave"), "neither model", "the sound model"],
                "Interference, diffraction and polarization → wave. Photoelectric effect and photon counting → particle.")


@safe
def g_pe():
    who = P.next()[0]
    W = R.choice([2.1, 2.3, 2.7, 3.7, 4.3, 4.7, 5.1])
    metal = {2.1: "cesium", 2.3: "sodium", 2.7: "calcium", 3.7: "magnesium", 4.3: "zinc", 4.7: "copper", 5.1: "gold"}[W]
    Eph = R.choice([1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0])
    k = R.choice(["yes", "ke", "bright"])
    if abs(Eph - W) < 0.15 or not once(("pe", W, Eph, k)):
        return None
    yes = Eph > W
    if k == "yes":
        g = "Yes, because each photon has more energy than %s eV." % num(W) if yes else "No, because each photon has less energy than %s eV." % num(W)
        return item("%s shines light with %s eV photons on %s (it needs %s eV to free an electron). Are electrons emitted?" % (who, num(Eph), metal, num(W)), g,
                    ["No, because each photon has less energy than %s eV." % num(W) if yes else "Yes, because each photon has more energy than %s eV." % num(W), "Yes, if the light is bright enough.", "Only after waiting a few minutes."],
                    "One photon frees one electron; brightness does not matter if each photon is too weak.")
    if k == "ke":
        if not yes:
            return None
        g = "%s eV" % num(Eph - W, 1)
        return item("Photons of %s eV hit %s (work function %s eV). What is the maximum kinetic energy of the freed electrons?" % (num(Eph), metal, num(W)), g,
                    uniq(g, ["%s eV" % num(Eph + W, 1), "%s eV" % num(Eph, 1), "%s eV" % num(W, 1), "0 eV"]), "KE = %s − %s = %s eV." % (num(Eph), num(W), num(Eph - W, 1)))
    if yes:
        g = "More electrons are emitted, but each has the same maximum energy."
    else:
        g = "Still no electrons are emitted."
    return item("Light of %s eV photons shines on %s (work function %s eV). The light is made twice as bright. What happens?" % (num(Eph), metal, num(W)), g,
                uniq(g, ["More electrons are emitted, but each has the same maximum energy.", "Still no electrons are emitted.", "Each electron gets twice as much energy.", "Electrons are emitted only after a delay."]),
                "Brightness = number of photons; photon energy depends only on frequency.")


B1 = bank([
    ("What is a photon?", "a packet (quantum) of electromagnetic energy", ["a type of electron", "a sound particle", "a piece of the nucleus"], "Light as a particle."),
    ("What does E = hf say?", "A photon's energy is proportional to its frequency.", ["Brighter light has higher-energy photons.", "Energy depends on wavelength squared.", "All photons have the same energy."], "h is Planck's constant."),
    ("Which experiment supports the wave model of light?", "the double-slit interference experiment", ["the photoelectric effect", "counting photons with a detector", "solar cell thresholds"], "Young, 1801."),
    ("Which experiment supports the particle model of light?", "the photoelectric effect", ["double-slit interference", "diffraction through a gap", "polarization by filters"], "Einstein, 1905."),
    ("Is light a wave or a particle?", "Both models are needed; each explains different evidence.", ["Only a wave.", "Only a particle.", "Neither."], "Wave-particle duality."),
    ("Why can ultraviolet light cause sunburn but visible light cannot?", "UV photons carry more energy, enough to damage skin cells.", ["UV is brighter.", "Visible light has no energy.", "UV is a sound wave."], "Photon energy."),
    ("What is the work function of a metal?", "the minimum energy needed to free an electron from its surface", ["the color of the metal", "the mass of an electron", "the speed of light in the metal"], "Threshold energy."),
    ("If light's wavelength gets shorter, what happens to its photon energy?", "It increases.", ["It decreases.", "It stays the same.", "It becomes zero."], "E = hc ÷ λ."),
])
B5 = bank([
    ("Why did the photoelectric effect puzzle scientists who used only the wave model?", "The wave model predicted bright light of any color would free electrons, but it did not.", ["Light did not reach the metal.", "Electrons were too heavy.", "The metal was a wave."], "Evidence against a pure wave model."),
    ("An engineer designs a camera sensor. Which model is more useful for counting how much light hits each pixel?", "the particle (photon) model", ["the wave model only", "neither model", "the sound model"], "Choose the useful model."),
    ("An engineer designs an anti-glare lens coating. Which model is more useful?", "the wave model (interference)", ["the particle model only", "neither model", "the nuclear model"], "Thin-film interference."),
    ("Why do solar panels work in sunlight but not under a strong red lamp of the same brightness for some materials?", "Red photons may not have enough energy to free electrons in that material.", ["Red light has no photons.", "The lamp is too cold.", "Solar panels need heat."], "Threshold."),
    ("Electrons also show interference through two slits. What does this suggest?", "Matter can also behave like a wave.", ["Electrons are photons.", "Interference is impossible.", "Electrons have no mass."], "Duality applies to matter too."),
])


def body():
    think = ("<p><b>Light acts like a wave and like a stream of particles (photons).</b></p>"
             "<ul><li>Wave model explains interference, diffraction and polarization.</li>"
             "<li>Particle model explains the photoelectric effect: one photon frees one electron only if E = hf is above the work function.</li>"
             "<li>Higher frequency (shorter wavelength) → more energy per photon. Brighter light → more photons, not stronger ones.</li></ul>")
    ex = [("Photon energy at 5 × 10<sup>14</sup> Hz?", ["6.63 × 10<sup>−34</sup> × 5 × 10<sup>14</sup>"], "3.32 × 10<sup>−19</sup> J"),
          ("3.0 eV photons on a 2.3 eV metal. Max KE?", ["3.0 − 2.3"], "0.7 eV")]
    mist = ["Thinking brighter light always frees electrons.", "Thinking red photons have more energy than blue.", "Thinking light must be only a wave or only a particle."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Two models of light", B1 + [(g_model, 8), (g_cmp, 4)]),
        ("Evidence for each model", [(g_model, 1), (g_cmp, 13), (g_pe, 6)]),
        ("Photon energy", [(g_photon, 14), (g_cmp, 6)]),
        ("The photoelectric effect", [(g_pe, 17), (g_photon, 3)]),
        ("Choosing a model", B5 + [(g_pe, 7), (g_cmp, 8)]),
    ])
    make("physics", "wave-particle-duality", 14, "HS-PS4-3",
         "Evaluate the claims, evidence, and reasoning behind the idea that electromagnetic radiation can be described either by a wave model or a particle model, and that for some situations one model is more useful than the other.",
         "Wave-Particle Duality of Light",
         "Wave-Particle Duality Worksheets: Photons, E = hf and the Photoelectric Effect (Physics)",
         "Wave-Particle Duality",
         "Free high school physics worksheets on wave-particle duality (NGSS HS-PS4-3): wave and particle models of light, photon energy E = hf and the photoelectric effect. 100 questions with answers.",
         "Light is both a wave and a particle.",
         "Interference needs the wave model; the photoelectric effect needs photons.",
         body(),
         [("What is wave-particle duality?", "Light shows wave behavior (interference, diffraction) in some experiments and particle behavior (photons) in others, so both models are needed."),
          ("How do you find the energy of a photon?", "E = hf, where h = 6.63 × 10⁻³⁴ J·s, or E = hc ÷ λ using the wavelength."),
          ("Why doesn't bright red light free electrons from some metals?", "Each red photon has too little energy. Brighter light has more photons, but each one is still too weak.")],
         sets)


if __name__ == "__main__":
    main()
