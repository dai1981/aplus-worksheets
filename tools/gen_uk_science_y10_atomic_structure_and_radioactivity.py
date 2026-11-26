# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Physics): Atomic Structure and Radioactivity
  python tools/gen_uk_science_y10_atomic_structure_and_radioactivity.py
The nuclear model of the atom, isotopes, radioactive decay, alpha, beta and gamma radiation (nature, penetration and
ionising power), nuclear equations, half-life, activity and count rate, contamination and irradiation, background
radiation and the hazards and uses of radiation. Reuses the US Chemistry nuclear questions in British English.
Wrong answers come from real mistakes: "gamma is the most ionising", "half-life is half the time to decay
completely", "irradiated objects become radioactive", "alpha passes through paper".
"""
from uk_sci import item, bank, once
from uk_ks4 import U4, build

U, R, P, us = U4(62013)
NC = "chem_nuclear_chemistry"
us_change, us_decay, us_half, us_pen = [us(NC, "g_" + n, drop=("fission", "fusion")) for n in ("change", "decay", "half", "pen")]

RAD = [("alpha particles", "2 protons and 2 neutrons (a helium nucleus)", "stopped by a sheet of paper or a few cm of air", "strongly ionising"),
       ("beta particles", "fast-moving electrons from the nucleus", "stopped by a few mm of aluminium", "moderately ionising"),
       ("gamma rays", "electromagnetic waves", "reduced by thick lead or several metres of concrete", "weakly ionising")]


def g_rad():
    r, what, stop, ion = R.choice(RAD)
    k = R.choice(["what", "stop", "ion"])
    if not once(("ra", r, k)):
        return None
    i = {"what": 1, "stop": 2, "ion": 3}[k]
    q = {"what": "What are %s?" % r, "stop": "What stops %s?" % r, "ion": "How ionising are %s?" % r}[k]
    return item(q, [what, stop, ion][i - 1], [x[i] for x in RAD if x[0] != r] + [{"what": "neutrons from the electron shells", "stop": "nothing can stop them", "ion": "not ionising at all"}[k]],
                "Alpha: most ionising, least penetrating. Gamma: least ionising, most penetrating.")


ALPHA = [(238, 92), (234, 92), (232, 90), (230, 90), (226, 88), (222, 86), (218, 84), (214, 84), (210, 84), (241, 95)]
BETA = [(14, 6), (40, 19), (131, 53), (137, 55), (210, 82), (210, 83), (90, 38), (32, 15), (60, 27), (3, 1), (24, 11), (234, 90)]


def g_eq():
    k = R.choice(["alpha", "beta"])
    a, z = R.choice(ALPHA if k == "alpha" else BETA)
    if not once(("eq", k, a, z)):
        return None
    if k == "alpha":
        g = "mass number %d, atomic number %d" % (a - 4, z - 2)
        w = ["mass number %d, atomic number %d" % (a - 2, z - 4), "mass number %d, atomic number %d" % (a, z - 2), "mass number %d, atomic number %d" % (a - 4, z + 2)]
    else:
        g = "mass number %d, atomic number %d" % (a, z + 1)
        w = ["mass number %d, atomic number %d" % (a - 1, z), "mass number %d, atomic number %d" % (a, z - 1), "mass number %d, atomic number %d" % (a - 4, z - 2)]
    return item("A nucleus with mass number %d and atomic number %d emits %s particle. What are the mass number and atomic number of the new nucleus?" % (a, z, "an alpha" if k == "alpha" else "a beta"), g, w,
                "Alpha: mass −4, atomic −2. Beta: a neutron becomes a proton, so atomic +1 and mass unchanged.")


def g_hl():
    k = R.choice(["left", "time", "frac"])
    h = R.choice([2, 3, 5, 6, 8, 10, 12, 30])
    n = R.choice([1, 2, 3, 4])
    c0 = R.choice([800, 1600, 640, 1200, 2400, 320])
    if not once(("hl", k, h, n, c0)):
        return None
    c = c0 // 2 ** n
    unit = R.choice(["hours", "days", "minutes"])
    if k == "left":
        g = "{:,} counts per minute".format(c)
        return item("A sample has a count rate of {:,} counts per minute. Its half-life is %d %s. What is the count rate after %d %s?".format(c0) % (h, unit, h * n, unit), g,
                    [x for x in ["{:,} counts per minute".format(c0 // (2 * n)), "{:,} counts per minute".format(c * 2), "{:,} counts per minute".format(c0 - c), "{:,} counts per minute".format(c // 2 if c > 1 else c0)] if x != g][:3],
                    "%d %s = %d half-lives: halve %d times." % (h * n, unit, n, n))
    if k == "time":
        g = "%d %s" % (h * n, unit)
        return item("The count rate of a sample falls from {:,} to {:,} counts per minute. Its half-life is %d %s. How long did this take?".format(c0, c) % (h, unit), g,
                    [x for x in ["%d %s" % (h * (n + 1), unit), "%d %s" % (h, unit), "%d %s" % (h * 2 ** n, unit), "%d %s" % (h * n * 2, unit)] if x != g][:3], "%d half-lives." % n)
    fr = "1/%d" % (2 ** n)
    return item("What fraction of a radioactive sample remains after %d half-li%s?" % (n, "fe" if n == 1 else "ves"), fr, [x for x in ["1/%d" % (2 * n), "1/%d" % (2 ** (n + 1)), "1/%d" % (2 ** n + 1), "1/%d" % n] if x != fr and x != "1/1"][:3],
                "Halve %d time%s." % (n, "" if n == 1 else "s"))


B1 = bank([
    ("What is the radius of a nucleus compared with an atom?", "about 1/10,000 of the radius of the atom", ["about half", "about the same", "about 10 times bigger"], "Mostly empty space."),
    ("What is radioactive decay?", "an unstable nucleus giving out radiation to become more stable", ["an atom losing electrons in a reaction", "a nucleus absorbing light", "a chemical reaction with oxygen"], "Random process."),
    ("What does 'random' mean for radioactive decay?", "You cannot predict which nucleus will decay next or when.", ["Every nucleus decays at the same time.", "Decay happens only when heated.", "It can be stopped by cooling."], "Only the overall pattern is predictable."),
    ("What is activity?", "the rate at which a source of unstable nuclei decays, measured in becquerels (Bq)", ["the energy of an alpha particle", "the mass of a sample", "the half-life"], "1 Bq = 1 decay per second."),
])
B5 = bank([
    ("What is the difference between irradiation and contamination?", "Irradiation is exposure to radiation; contamination is radioactive material getting onto or into an object.", ["They are the same.", "Irradiation makes objects radioactive.", "Contamination is harmless."], "Irradiated objects do not become radioactive."),
    ("Which radiation is most dangerous inside the body?", "alpha, because it is strongly ionising and is absorbed by nearby cells", ["gamma, because it is most penetrating", "beta, because it is fastest", "none of them"], "Outside the body, alpha is stopped by skin."),
    ("Name a source of background radiation.", "radon gas from rocks", ["mobile phones", "visible light", "radio waves"], "Also cosmic rays and medical X-rays."),
    ("Why are gamma emitters used as medical tracers?", "Gamma passes out of the body and is weakly ionising.", ["Gamma is stopped by skin.", "Alpha is safer inside the body.", "Gamma has a long half-life."], "Detected outside the body."),
    ("Why is it important that peer review is used for findings about radiation?", "Other scientists check the evidence before it is accepted.", ["It makes radiation safer.", "It changes the half-life.", "It stops all research."], "Checking findings."),
])

if __name__ == "__main__":
  build(U, 10, "atomic-structure-and-radioactivity", 13, "Physics", "Atomic structure",
      "The structure of an atom and the nuclear model; isotopes; the development of the model of the atom; radioactive decay and nuclear radiation: alpha, beta and gamma; nuclear equations; half-lives and the random nature of radioactive decay; radioactive contamination and irradiation; background radiation and the hazards and uses of nuclear radiation.",
      "Atomic Structure and Radioactivity", "Atomic Structure and Radioactivity",
      "Free Year 10 GCSE Combined Science worksheets on radioactivity: alpha, beta and gamma radiation, nuclear equations, half-life, activity, contamination and irradiation, and background radiation. 100 questions with answers.",
      "Half-life is the time for half the nuclei to decay.",
      "Alpha is most ionising; gamma is most penetrating.",
      "<p><b>Unstable nuclei decay randomly, giving out radiation.</b></p><ul><li>Alpha (helium nucleus): stopped by paper, strongly ionising. Beta (electron): stopped by aluminium. Gamma (EM wave): reduced by thick lead.</li>"
      "<li>Alpha decay: mass number −4, atomic number −2. Beta decay: atomic number +1.</li>"
      "<li>Half-life: the time for the count rate (or number of nuclei) to halve.</li></ul>",
      [("800 counts, half-life 2 h. After 6 h?", ["3 half-lives", "800 → 400 → 200 → 100"], "100"), ("²³⁸U emits alpha. New mass number?", ["238 − 4"], "234")],
      ["Thinking gamma is the most ionising.", "Thinking irradiated objects become radioactive.", "Thinking half-life is half the time for all of it to decay."],
      [("What are alpha, beta and gamma radiation?", "Alpha particles are helium nuclei, beta particles are fast electrons from the nucleus, and gamma rays are electromagnetic waves."),
       ("What is half-life?", "The time it takes for the number of unstable nuclei in a sample, or its count rate, to halve."),
       ("What is the difference between irradiation and contamination?", "Irradiation is being exposed to radiation from outside; contamination is radioactive atoms getting onto or into something. Irradiated objects do not become radioactive.")],
      [("The nucleus", B1 + [(g_rad, 7), (us_pen, 4), (us_decay, 5)]),
       ("Alpha, beta and gamma", [(us_change, 11), (g_eq, 9)]),
       ("Nuclear equations", [(g_eq, 6), (us_decay, 7), (us_change, 7)]),
       ("Half-life", [(g_hl, 14), (us_half, 6)]),
       ("Uses and hazards", B5 + [(us_half, 8), (g_hl, 7)])])
