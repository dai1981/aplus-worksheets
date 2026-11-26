# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: The Big Bang (HS-ESS1-2)
  python tools/gen_us_science_ess_the_big_bang.py
Construct an explanation of the Big Bang theory based on astronomical evidence of light spectra, motion of distant
galaxies, and composition of matter in the universe.
Redshift and blueshift, z = Δλ ÷ λ and v ≈ zc, Hubble's law v = H₀d (H₀ = 70 km/s/Mpc), galaxy distance-speed data,
the cosmic microwave background, the abundance of hydrogen and helium, and the age of the universe.
Wrong answers come from real mistakes: "the Big Bang was an explosion at one center in space", "redshift means
the galaxy is hot", "nearby galaxies recede fastest", "the universe is only a few thousand years old".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90402)
R = U.R
P = People(R)
USED = {}
H0 = 70


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_hubble():
    d = R.choice([10, 20, 50, 100, 150, 200, 300, 400, 500, 1000])
    k = R.choice(["v", "d"])
    if not once(("hb", d, k)):
        return None
    v = H0 * d
    if k == "v":
        g = "%s km/s" % num(v)
        return item("A galaxy is %s Mpc away. Using Hubble's law (v = H₀d, H₀ = 70 km/s/Mpc), how fast is it moving away?" % num(d), g,
                    uniq(g, ["%s km/s" % num(d / H0, 2), "%s km/s" % num(d + H0), "%s km/s" % num(v * 2), "%s km/s" % num(v / 10)]), "v = 70 × %s = %s km/s." % (num(d), num(v)))
    g = "%s Mpc" % num(d)
    return item("A galaxy moves away at %s km/s. Using v = H₀d with H₀ = 70 km/s/Mpc, how far away is it?" % num(v), g,
                uniq(g, ["%s Mpc" % num(v * H0), "%s Mpc" % num(v), "%s Mpc" % num(d * 2), "%s Mpc" % num(d / 2, 1)]), "d = v ÷ H₀ = %s ÷ 70 = %s Mpc." % (num(v), num(d)))


@safe
def g_shift():
    l0 = R.choice([400, 450, 500, 600, 656])
    dl = R.choice([2, 4, 5, 6, 10, 12, 20, 30])
    sign = R.choice([1, 1, -1])
    k = R.choice(["type", "z", "v"])
    if not once(("sh", l0, dl, sign, k)):
        return None
    lo = l0 + sign * dl
    z = dl / l0
    if k == "type":
        g = "redshift: it is moving away" if sign > 0 else "blueshift: it is moving toward us"
        return item("A spectral line is %s nm in the lab but %s nm in a galaxy's spectrum. What does this show?" % (num(l0), num(lo)), g,
                    uniq(g, ["redshift: it is moving away", "blueshift: it is moving toward us", "the galaxy is very hot", "the galaxy is not moving", "the galaxy is very cold"]),
                    "Longer wavelength = redshift (away); shorter = blueshift (toward).")
    if sign < 0:
        return None
    if k == "z":
        g = num(z, 4)
        return item("A spectral line at %s nm in the lab is seen at %s nm in a galaxy. What is the redshift z = Δλ ÷ λ?" % (num(l0), num(lo)), g,
                    uniq(g, [num(dl, 0), num(lo / l0, 4), num(l0 / dl, 1), num(z * 2, 4)]), "z = %s ÷ %s = %s." % (num(dl), num(l0), num(z, 4)))
    v = z * 300000
    g = "%s km/s" % num(v, 0)
    return item("A line at %s nm in the lab appears at %s nm in a galaxy's light. About how fast is the galaxy moving away? (v ≈ zc, c = 300,000 km/s)" % (num(l0), num(lo)), g,
                uniq(g, ["%s km/s" % num(dl * 300000, 0), "%s km/s" % num(300000 / z, 0), "%s km/s" % num(v / 10, 0), "%s km/s" % num(v * 2, 0)]), "z = %s; v ≈ %s × 300,000 = %s km/s." % (num(z, 4), num(z, 4), num(v, 0)))


@safe
def g_data():
    who = P.next()[0]
    H = R.choice([65, 68, 70, 72, 75])
    ds = sorted(R.sample([20, 40, 60, 80, 100, 150, 200, 250, 300], 4))
    vs = [H * d + R.choice([-40, -20, 0, 20, 40]) for d in ds]
    k = R.choice(["trend", "H", "pred"])
    if not once(("dt", H, tuple(ds), k)) or (k == "trend" and not once("dtt", 3)):
        return None
    tab = table(["Galaxy distance (Mpc)", "Speed away from us (km/s)"], [[num(d), num(v)] for d, v in zip(ds, vs)])
    if k == "trend":
        return item(tab + "What pattern do %s's galaxy data show?" % who, "Farther galaxies move away faster.", ["Nearby galaxies move away fastest.", "All galaxies move at the same speed.", "Galaxies are moving toward us."],
                    "This is Hubble's law: evidence the universe is expanding.")
    if k == "H":
        g = "about %d km/s/Mpc" % H
        return item(tab + "Estimate H₀ from %s's data (speed ÷ distance)." % who, g, uniq(g, ["about %d km/s/Mpc" % (H * 10), "about %s km/s/Mpc" % num(1 / H, 3), "about %d km/s/Mpc" % (H // 2), "about %d km/s/Mpc" % (H + 30)]),
                    "For example, %s ÷ %s ≈ %d." % (num(vs[-1]), num(ds[-1]), round(vs[-1] / ds[-1])))
    d = ds[-1] * 2
    g = "about %s km/s" % num(H * d)
    return item(tab + "Using %s's data, predict the speed of a galaxy %s Mpc away." % (who, num(d)), g,
                uniq(g, ["about %s km/s" % num(vs[-1]), "about %s km/s" % num(H * d / 2), "about %s km/s" % num(H * d * 2), "about 0 km/s"]), "≈ %d × %s." % (H, num(d)))


EV = [("Almost every distant galaxy's light is redshifted.", "The universe is expanding."), ("A faint microwave glow comes evenly from every direction in the sky.", "This is leftover radiation from the hot early universe (the CMB)."),
      ("About 75% of normal matter is hydrogen and about 25% is helium.", "This matches what the Big Bang model predicts for the first few minutes."),
      ("The farther a galaxy is, the faster it moves away.", "Space itself is stretching everywhere (Hubble's law)."),
      ("Very distant galaxies look younger and less developed.", "We see them as they were billions of years ago, when the universe was younger."),
      ("The CMB has a temperature of about 2.7 K that is almost the same in every direction.", "The early universe was hot, dense and very uniform, then cooled as it expanded.")]


@safe
def g_ev():
    s, a = R.choice(EV)
    k = R.random() < 0.6
    if not once(("ev", s, k)):
        return None
    if k:
        return item("Evidence: %s What does it support?" % s, a, R.sample([x[1] for x in EV if x[1] != a], 3), "Three main lines of evidence: redshift, the CMB and light-element abundances.")
    return item("Which evidence supports this idea: “%s”" % a, s, R.sample([x[0] for x in EV if x[0] != s], 3), "Match the evidence to the idea.")


B1 = bank([
    ("What is the Big Bang theory?", "The universe began about 13.8 billion years ago in a hot, dense state and has been expanding ever since.", ["A star exploded in the middle of space.", "The universe has always been the same.", "Earth formed first, then the stars."],
     "Expansion of space."),
    ("What is redshift?", "light from an object moving away is stretched to longer wavelengths", ["light from a hot object", "light from a red star", "light that is reflected"], "Doppler effect for light."),
    ("Is the Big Bang an explosion into empty space from one center?", "No. Space itself expands everywhere at once.", ["Yes, from the center of the universe.", "Yes, from the Sun.", "Yes, from the Milky Way."], "No center."),
    ("What is the cosmic microwave background (CMB)?", "faint radiation left over from the hot early universe", ["light from nearby stars", "radio signals from Earth", "heat from the Sun"], "Discovered in 1965."),
    ("Why is the CMB now in the microwave range?", "The universe's expansion stretched the early light to much longer wavelengths.", ["It came from microwave ovens.", "It was always microwaves.", "Stars make microwaves."], "Cooling by expansion."),
    ("How old is the universe?", "about 13.8 billion years", ["about 4.6 billion years", "about 6,000 years", "about 1 trillion years"], "From expansion rate and CMB."),
    ("Which elements formed mostly in the first few minutes after the Big Bang?", "hydrogen and helium (and a little lithium)", ["iron and gold", "carbon and oxygen", "uranium"], "Heavier elements came from stars."),
    ("What does Hubble's law say?", "A galaxy's speed away from us is proportional to its distance.", ["All galaxies move toward us.", "Nearby galaxies are fastest.", "Galaxies do not move."], "v = H₀d."),
])
B5 = bank([
    ("Two radio engineers found a steady 'noise' from every direction in 1965. Why was it important?", "It was the CMB, strong evidence for the Big Bang.", ["It came from pigeons.", "It proved the universe is static.", "It came from the Moon."], "Penzias and Wilson."),
    ("How does a raisin bread model show expansion?", "As the dough rises, every raisin moves away from every other, faster for raisins farther apart.", ["Raisins move toward the center.", "Only one raisin moves.", "Raisins stay still."], "Model of Hubble's law."),
    ("Why can't the age of the universe be less than the age of its oldest stars?", "The universe must have existed before any star formed in it.", ["Stars are older than the universe.", "Ages cannot be measured.", "Stars form before galaxies."], "Consistency check."),
    ("The Andromeda galaxy is blueshifted. Does this disprove expansion?", "No. Gravity pulls nearby galaxies together; distant galaxies still recede.", ["Yes, it disproves expansion.", "Yes, all galaxies are blueshifted.", "No, because blue is a kind of red."], "Local motion."),
    ("A student claims the universe is not expanding because the solar system is not growing. What is the best reply?", "Gravity holds the solar system together; expansion shows up between distant galaxies.", ["The solar system is growing fast.", "The student is right.", "Expansion only happens on Earth."], "Scale matters."),
])


def body():
    think = ("<p><b>The universe began hot and dense about 13.8 billion years ago and is still expanding.</b></p>"
             "<ul><li>Redshift: light from distant galaxies is stretched; farther galaxies recede faster (Hubble's law v = H₀d).</li>"
             "<li>The cosmic microwave background is leftover glow from the early universe.</li>"
             "<li>About 75% hydrogen and 25% helium matches Big Bang predictions; heavier elements came later from stars.</li></ul>")
    ex = [("Galaxy 200 Mpc away (H₀ = 70)?", ["70 × 200"], "14,000 km/s"),
          ("Line 500 nm → 505 nm. z?", ["5 ÷ 500"], "0.01")]
    mist = ["Thinking the Big Bang exploded from one center in space.", "Thinking redshift means the galaxy is hot.", "Thinking nearby galaxies recede fastest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The Big Bang", B1 + [(g_ev, 6), (g_shift, 6)]),
        ("Redshift and blueshift", [(g_shift, 16), (g_ev, 4)]),
        ("Hubble's law", [(g_hubble, 12), (g_data, 8)]),
        ("Galaxy data", [(g_data, 12), (g_hubble, 3), (g_shift, 5)]),
        ("Evidence for the Big Bang", B5 + [(g_ev, 1), (g_data, 4), (g_hubble, 2), (g_shift, 8)]),
    ])
    make("earth-and-space-science", "the-big-bang", 2, "HS-ESS1-2",
         "Construct an explanation of the Big Bang theory based on astronomical evidence of light spectra, motion of distant galaxies, and composition of matter in the universe.",
         "The Big Bang",
         "Big Bang Worksheets: Redshift, Hubble's Law and the Cosmic Microwave Background (Earth Science)",
         "The Big Bang",
         "Free high school Earth and space science worksheets on the Big Bang (NGSS HS-ESS1-2): redshift, Hubble's law, galaxy data, the cosmic microwave background and hydrogen and helium. 100 questions with answers.",
         "The universe is expanding.",
         "Redshift, the CMB and hydrogen-helium amounts all support the Big Bang.",
         body(),
         [("What is the evidence for the Big Bang?", "Redshifted light from distant galaxies (expansion), the cosmic microwave background, and the amounts of hydrogen and helium in the universe."),
          ("What is Hubble's law?", "A galaxy's speed away from us is proportional to its distance: v = H₀d, with H₀ about 70 km/s per megaparsec."),
          ("What is redshift?", "When a light source moves away, its light is stretched to longer (redder) wavelengths.")],
         sets)


if __name__ == "__main__":
    main()
