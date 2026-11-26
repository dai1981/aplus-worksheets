# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: The Sun and Nuclear Fusion (HS-ESS1-1)
  python tools/gen_us_science_ess_the_sun_and_nuclear_fusion.py
Develop a model based on evidence to illustrate the life span of the sun and the role of nuclear fusion in the sun's
core to release energy that eventually reaches Earth in the form of radiation.
Layers of the Sun, hydrogen fusion into helium, E = mc², how long energy takes to reach Earth, the Sun's life span,
star mass and lifetime, and the sunspot cycle.
Wrong answers come from real mistakes: "the Sun burns like a fire", "fusion splits atoms", "massive stars live longer",
"sunlight takes years to reach Earth".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, sci, uniq, safe

U = Unit(90401)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


LAY = [("core", "where hydrogen nuclei fuse into helium at about 15 million °C"), ("radiative zone", "where energy slowly moves outward as light is absorbed and re-emitted"),
       ("convection zone", "where hot gas rises and cooler gas sinks, carrying energy up"), ("photosphere", "the visible surface that gives off most of the sunlight we see"),
       ("chromosphere", "a thin reddish layer above the visible surface"), ("corona", "the very hot outer atmosphere seen during a total solar eclipse")]


@safe
def g_layer():
    n, d = R.choice(LAY)
    k = R.random() < 0.5
    if not once(("ly", n, k)):
        return None
    if k:
        return item("Which layer of the Sun is %s?" % d, "the %s" % n, ["the %s" % x[0] for x in R.sample([x for x in LAY if x[0] != n], 3)], "From inside out: core, radiative zone, convection zone, photosphere, chromosphere, corona.")
    return item("What happens in the Sun's %s?" % n, d, R.sample([x[1] for x in LAY if x[1] != d], 3), "Energy is made in the core and travels outward.")


@safe
def g_emc():
    m = R.choice([1e-3, 2e-3, 0.01, 0.05, 1, 4.3e9, 1e6, 0.5])
    if not once(("em", m)):
        return None
    E = m * 9e16
    g = "%s J" % sci(E)
    return item("If %s kg of mass is converted to energy in fusion, how much energy is released? (E = mc², c = 3.0 × 10<sup>8</sup> m/s)" % (sci(m) if m < 0.01 or m >= 1e5 else num(m, 3)), g,
                uniq(g, ["%s J" % sci(m * 3e8), "%s J" % sci(E / 10), "%s J" % sci(E * 10), "%s J" % sci(m * 9e8)]), "E = %s × (3.0 × 10<sup>8</sup>)² = %s J." % (sci(m), sci(E)))


@safe
def g_life():
    who = P.next()[0]
    stars = [("0.5 Sun masses", 57), ("1 Sun mass (the Sun)", 10), ("2 Sun masses", 1.2), ("5 Sun masses", 0.1), ("10 Sun masses", 0.03), ("0.8 Sun masses", 25)]
    s = R.sample(stars, 4)
    k = R.choice(["long", "short", "read", "rule"])
    if not once(("lf", tuple(x[0] for x in s), k)) or (k == "rule" and not once("lr", 3)):
        return None
    tab = table(["Star mass", "Main-sequence life span (billion years)"], [[a, num(b, 2)] for a, b in s])
    if k == "long":
        a = max(s, key=lambda x: x[1])
        return item(tab + "Using %s's table, which star stays on the main sequence longest?" % who, a[0], [x[0] for x in s if x != a], "Smaller stars use their fuel slowly.")
    if k == "short":
        a = min(s, key=lambda x: x[1])
        return item(tab + "Using %s's table, which star has the shortest life?" % who, a[0], [x[0] for x in s if x != a], "Massive stars burn fuel very fast.")
    if k == "read":
        a = R.choice(s)
        g = "%s billion years" % num(a[1], 2)
        return item(tab + "About how long does a star of %s last on the main sequence?" % a[0], g, uniq(g, ["%s billion years" % num(x[1], 2) for x in s] + ["%s billion years" % num(a[1] * 2, 2)]), "Read the row.")
    return item(tab + "What pattern do %s's data show?" % who, "More massive stars have shorter lives.", ["More massive stars live longer.", "All stars live 10 billion years.", "Mass has no effect on life span."],
                "Higher core pressure and temperature → much faster fusion.")


@safe
def g_age():
    who = P.next()[0]
    k = R.choice(["left", "frac", "light"])
    if k == "light":
        d = R.choice([("Mercury", 58), ("Earth", 150), ("Mars", 228), ("Jupiter", 778), ("Saturn", 1430), ("Venus", 108), ("Uranus", 2870), ("Neptune", 4500), ("Pluto", 5900)])
        if not once(("lt", d[0])):
            return None
        t = d[1] * 1e9 / 3e8
        g = "about %s minutes" % num(t / 60, 1)
        return item("Sunlight travels %s million km to reach %s. About how long does it take? (c = 3.0 × 10<sup>8</sup> m/s)" % (num(d[1]), d[0]), g,
                    uniq(g, ["about %s seconds" % num(t / 60, 1), "about %s hours" % num(t / 60, 1), "about %s minutes" % num(t / 6, 0), "instantly"]), "%s × 10<sup>9</sup> m ÷ 3.0 × 10<sup>8</sup> m/s = %s s." % (num(d[1]), num(t, 0)))
    age = R.choice([4.6])
    total = R.choice([9, 9.5, 10, 10.5, 11, 12])
    if k == "left":
        if not once(("lf2", total)):
            return None
        g = "about %s billion years" % num(total - age, 1)
        return item("Models say a Sun-like star spends about %s billion years fusing hydrogen in its core. The Sun is 4.6 billion years old. About how much longer will this stage last?" % num(total, 1), g,
                    uniq(g, ["about %s billion years" % num(total + age, 1), "about %s billion years" % num(total, 1), "about 4.6 billion years", "it has already ended"]), "%s − 4.6 = %s." % (num(total, 1), num(total - age, 1)))
    if not once(("fr", total)):
        return None
    g = "about %d%%" % round(100 * age / total)
    return item("If the Sun's hydrogen-fusing stage lasts %s billion years and it is 4.6 billion years old, about what percent of that stage has passed?" % num(total, 1), g,
                uniq(g, ["about %d%%" % round(100 - 100 * age / total), "about 100%", "about %d%%" % round(age * 10), "about 4.6%"]), "4.6 ÷ %s × 100." % num(total, 1))


@safe
def g_spot():
    who = P.next()[0]
    start = R.choice([1986, 1996, 2008, 2019])
    yrs = [start + i for i in range(0, 12, 2)]
    peak = R.randint(2, 3)
    top = R.randint(100, 220)
    vals = [round(top * (1 - abs(i - peak) / 3.5)) for i in range(len(yrs))]
    vals = [max(v, R.randint(5, 20)) for v in vals]
    k = R.choice(["peak", "next", "cycle"])
    if not once(("ss", start, peak, top, k)):
        return None
    tab = table(["Year", "Average sunspot number"], [[str(y), str(v)] for y, v in zip(yrs, vals)])
    pk = yrs[vals.index(max(vals))]
    if k == "peak":
        return item(tab + "In %s's data, which year had the most sunspots?" % who, str(pk), [str(y) for y in yrs if y != pk][:3], "The highest number.")
    if k == "next":
        g = "around %d" % (pk + 11)
        return item(tab + "The sunspot cycle is about 11 years long. Using %s's data, when is the next peak likely?" % who, g, uniq(g, ["around %d" % (pk + 1), "around %d" % (pk + 5), "around %d" % (pk + 22), "never"]),
                    "%d + 11 = %d." % (pk, pk + 11))
    return item(tab + "What do sunspot records like %s's show about the Sun?" % who, "Its activity rises and falls in a cycle of about 11 years.", ["It never changes.", "It is cooling quickly.", "Sunspots appear only once."],
                "The solar cycle.")


B1 = bank([
    ("Where does the Sun's energy come from?", "nuclear fusion of hydrogen into helium in its core", ["burning gas like a fire", "nuclear fission of uranium", "chemical reactions with oxygen"], "Fusion."),
    ("What is nuclear fusion?", "light nuclei joining to form a heavier nucleus", ["a heavy nucleus splitting", "atoms burning in oxygen", "electrons jumping between atoms"], "Releases energy."),
    ("Why does fusion release energy?", "A little mass is converted into a lot of energy (E = mc²).", ["Atoms are destroyed.", "Oxygen burns.", "Heat is created from nothing."], "Mass defect."),
    ("Why does fusion only happen in the Sun's core?", "Only the core is hot and dense enough to push nuclei together.", ["The core has oxygen.", "The surface is too hot.", "Fusion needs light."], "Extreme conditions."),
    ("How does energy from the Sun reach Earth?", "as electromagnetic radiation (light and other waves) through space", ["by sound waves", "by conduction through space", "by wind only"], "Radiation."),
    ("How long has the Sun been shining?", "about 4.6 billion years", ["about 6,000 years", "about 46 million years", "about 100 billion years"], "Age of the solar system."),
    ("What will the Sun become after it runs out of hydrogen in its core?", "a red giant, then a white dwarf", ["a black hole", "a neutron star", "a planet"], "Sun-like star life cycle."),
    ("What are sunspots?", "cooler, darker areas on the Sun's surface caused by magnetic activity", ["holes in the Sun", "planets passing in front", "places with no light at all"], "Magnetic fields."),
])
B5 = bank([
    ("Scientists detect neutrinos coming from the Sun's core. Why is this important?", "Neutrinos are made in fusion, so they are direct evidence of fusion in the core.", ["They prove the Sun is burning coal.", "They show the Sun is cold.", "They are sunlight."], "Evidence for the model."),
    ("Why does energy made in the core take thousands of years to reach the surface?", "Light is absorbed and re-emitted countless times in the dense radiative zone.", ["The Sun is very slow.", "Energy moves at sound speed.", "It waits for sunspots."], "Random walk."),
    ("Solar flares can disrupt power grids and satellites. What causes them?", "sudden releases of magnetic energy on the Sun", ["Earth's earthquakes", "the Moon's gravity", "fusion stopping"], "Space weather."),
    ("Why couldn't the Sun be powered by chemical burning?", "Chemical burning would use it up in only a few thousand years.", ["The Sun has no fuel.", "Burning is too slow to see.", "Space has too much oxygen."], "Lifetime evidence."),
    ("Why do astronomers study other Sun-like stars?", "They show different stages, helping us model the Sun's past and future.", ["They are closer than the Sun.", "They are all the same age.", "They have no light."], "Stars as models."),
])


def body():
    think = ("<p><b>The Sun shines by fusing hydrogen into helium in its core.</b></p>"
             "<ul><li>Fusion turns a little mass into a lot of energy (E = mc²). Energy moves out through the radiative and convection zones and leaves as light.</li>"
             "<li>The Sun is about 4.6 billion years old and halfway through its ~10-billion-year main-sequence life.</li>"
             "<li>More massive stars fuse faster and have much shorter lives.</li></ul>")
    ex = [("1 g of mass converted. Energy?", ["0.001 × (3 × 10<sup>8</sup>)²"], "9.00 × 10<sup>13</sup> J"),
          ("Sunlight to Earth (150 million km)?", ["1.5 × 10<sup>11</sup> ÷ 3 × 10<sup>8</sup> = 500 s"], "about 8.3 minutes")]
    mist = ["Thinking the Sun burns like a fire.", "Confusing fusion (joining) with fission (splitting).", "Thinking massive stars live longer."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("How the Sun makes energy", B1 + [(g_layer, 7), (g_emc, 4), (g_age, 1)]),
        ("Layers of the Sun", [(g_layer, 4), (g_emc, 3), (g_age, 11), (g_spot, 2)]),
        ("Star mass and life span", [(g_life, 16), (g_age, 4)]),
        ("The sunspot cycle", [(g_spot, 16), (g_life, 4)]),
        ("Evidence about the Sun", B5 + [(g_spot, 7), (g_life, 5), (g_age, 3)]),
    ])
    make("earth-and-space-science", "the-sun-and-nuclear-fusion", 1, "HS-ESS1-1",
         "Develop a model based on evidence to illustrate the life span of the sun and the role of nuclear fusion in the sun's core to release energy that eventually reaches Earth in the form of radiation.",
         "The Sun and Nuclear Fusion",
         "Sun Worksheets: Nuclear Fusion, Layers, Life Span and Sunspots (High School Earth Science)",
         "The Sun",
         "Free high school Earth and space science worksheets on the Sun (NGSS HS-ESS1-1): nuclear fusion, E = mc², layers of the Sun, star life spans and the sunspot cycle. 100 questions with answers.",
         "Fusion powers the Sun.",
         "Hydrogen fuses into helium in the core; the energy reaches Earth as light.",
         body(),
         [("How does the Sun make energy?", "In its core, hydrogen nuclei fuse into helium. A small amount of mass becomes a large amount of energy (E = mc²)."),
          ("How long will the Sun last?", "The Sun is about 4.6 billion years old and will keep fusing hydrogen for about 5 billion more years before becoming a red giant."),
          ("Why do massive stars have shorter lives?", "Their cores are hotter and denser, so they fuse hydrogen much faster and run out sooner.")],
         sets)


if __name__ == "__main__":
    main()
