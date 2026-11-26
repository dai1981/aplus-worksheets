# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Kepler's Laws and Orbits (HS-ESS1-4)
  python tools/gen_us_science_ess_keplers_laws_and_orbits.py
Use mathematical or computational representations to predict the motion of orbiting objects in the solar system.
Kepler's three laws (ellipses, equal areas, T² = a³ in years and AU), planet data tables, orbital speed v = 2πr ÷ T,
and how gravity keeps planets, moons and satellites in orbit.
Wrong answers come from real mistakes: "orbits are perfect circles with the Sun at the center", "planets move at a
constant speed", "T = a", "farther planets orbit faster".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90404)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


AT = [(1, 1), (4, 8), (9, 27), (16, 64), (25, 125), (36, 216), (0.25, 0.125), (0.04, 0.008), (100, 1000), (49, 343)]


@safe
def g_k3():
    a, T = R.choice(AT)
    k = R.choice(["T", "a"])
    obj = R.choice(["an asteroid", "a comet", "a dwarf planet", "a newly found object"])
    if not once(("k3", a, k)):
        return None
    if k == "T":
        g = "%s years" % num(T, 3)
        return item("%s orbits the Sun with an average distance of %s AU. Using T² = a³, what is its orbital period?" % (obj[0].upper() + obj[1:], num(a, 2)), g,
                    uniq(g, ["%s years" % num(a, 2), "%s years" % num(a * a, 4), "%s years" % num(a ** 0.5, 2), "%s years" % num(T * 2, 3)]), "T = √(a³) = √(%s) = %s years." % (num(a ** 3, 6), num(T, 3)))
    g = "%s AU" % num(a, 2)
    return item("%s takes %s years to orbit the Sun. Using T² = a³, what is its average distance from the Sun?" % (obj[0].upper() + obj[1:], num(T, 3)), g,
                uniq(g, ["%s AU" % num(T, 3), "%s AU" % num(T ** 0.5, 2), "%s AU" % num(T * T, 4), "%s AU" % num(a * 2, 2)]), "a = ∛(T²) = ∛(%s) = %s AU." % (num(T * T, 6), num(a, 2)))


PL = [("Mercury", 0.39, 0.24), ("Venus", 0.72, 0.62), ("Earth", 1.00, 1.00), ("Mars", 1.52, 1.88), ("Jupiter", 5.20, 11.9), ("Saturn", 9.54, 29.5), ("Uranus", 19.2, 84.0), ("Neptune", 30.1, 165)]


@safe
def g_table():
    who = P.next()[0]
    ps = sorted(R.sample(PL, 4), key=lambda x: x[1])
    k = R.choice(["fast", "slow", "ratio", "read"])
    if not once(("tb", tuple(p[0] for p in ps), k)) or (k == "read" and not once("tbr", 3)):
        return None
    tab = table(["Planet", "Average distance a (AU)", "Orbital period T (years)"], [[p[0], num(p[1], 2), num(p[2], 2)] for p in ps])
    if k == "fast":
        return item(tab + "Which planet in %s's table has the shortest year?" % who, ps[0][0], [p[0] for p in ps[1:]], "Closest to the Sun → shortest period.")
    if k == "slow":
        return item(tab + "Which planet in %s's table takes longest to orbit the Sun?" % who, ps[-1][0], [p[0] for p in ps[:-1]], "Farthest → longest period.")
    if k == "ratio":
        p = R.choice(ps)
        r = p[2] ** 2 / p[1] ** 3
        g = "about 1"
        return item(tab + "Calculate T² ÷ a³ for %s. What do you get?" % p[0], g, uniq(g, ["about %s" % num(p[2] / p[1], 2), "about %s" % num(p[1] ** 3, 1), "about 0", "about %s" % num(p[2] ** 2, 1)]),
                    "%s² ÷ %s³ ≈ %s — the same for every planet (Kepler's third law)." % (num(p[2], 2), num(p[1], 2), num(r, 2)))
    return item(tab + "According to %s's table, what happens to the orbital period as distance from the Sun increases?" % who, "It increases faster than the distance does.", ["It decreases.", "It stays the same.", "It increases exactly as fast as distance."],
                "T² = a³, so T grows like a<sup>1.5</sup>.")


POS = [("perihelion (closest to the Sun)", "fastest"), ("aphelion (farthest from the Sun)", "slowest")]


@safe
def g_k2():
    obj = R.choice(["Earth", "Mars", "Halley's Comet", "a comet", "an asteroid", "Mercury", "Pluto", "Venus", "Neptune", "a dwarf planet"])
    p, a = R.choice(POS)
    k = R.random() < 0.6
    if not once(("k2", obj, p, k)):
        return None
    if k:
        g = "It moves %s." % a
        return item("At %s, how does %s move compared with the rest of its orbit?" % (p, obj), g, uniq(g, ["It moves fastest.", "It moves slowest.", "It moves at the same speed everywhere.", "It stops moving."]),
                    "Kepler's second law: a line from the Sun sweeps equal areas in equal times, so the planet speeds up when close.")
    g = "the Sun's gravity pulls harder when it is closer"
    return item("Why does %s speed up as it approaches the Sun?" % obj, g, ["the Sun pushes it away", "it gets lighter", "space is thinner near the Sun"], "Gravity does work on it as it falls closer.")


@safe
def g_speed():
    case = R.choice([("The International Space Station", 6780, 92.7, "min"), ("A GPS satellite", 26600, 718, "min"), ("The Moon", 384400, 27.3, "days"), ("Earth around the Sun", 150000000, 365.25, "days"),
                     ("A weather satellite", 7200, 100, "min"), ("A geostationary satellite", 42200, 24, "h")])
    if not once(("sp", case[0])):
        return None
    t = case[2] * {"min": 60, "days": 86400, "h": 3600}[case[3]]
    v = 2 * 3.1416 * case[1] / t
    g = "about %s km/s" % num(v, 2)
    return item("%s orbits at a radius of %s km and takes %s %s per orbit. What is its average orbital speed? (v = 2πr ÷ T)" % (case[0], num(case[1]), num(case[2], 2), case[3]), g,
                uniq(g, ["about %s km/s" % num(case[1] / t, 3), "about %s km/s" % num(v * 60, 1), "about %s km/s" % num(v * 10, 1), "about %s km/s" % num(v / 2, 2)]),
                "2π × %s ÷ %s s = %s km/s." % (num(case[1]), num(t), num(v, 2)))


B1 = bank([
    ("What is Kepler's first law?", "Planets move in ellipses with the Sun at one focus.", ["Planets move in perfect circles around the Sun's center.", "Planets move in straight lines.", "The Sun orbits Earth."], "Ellipses."),
    ("What is Kepler's second law?", "A line from the Sun to a planet sweeps out equal areas in equal times.", ["Planets move at constant speed.", "All planets have the same year.", "Orbits are circles."], "Faster when closer."),
    ("What is Kepler's third law?", "The square of a planet's period is proportional to the cube of its average distance (T² = a³).", ["T = a.", "Closer planets have longer years.", "All periods are equal."], "In years and AU."),
    ("What is an astronomical unit (AU)?", "the average distance from Earth to the Sun, about 150 million km", ["one light-year", "the radius of Earth", "the distance to the Moon"], "1 AU."),
    ("What force keeps the planets in orbit?", "the Sun's gravity", ["magnetism", "air pressure", "nothing; they float"], "Newton explained Kepler's laws."),
    ("Do farther planets orbit faster or slower?", "slower", ["faster", "the same", "they do not orbit"], "Weaker gravity, longer path."),
    ("What is eccentricity?", "a measure of how stretched an ellipse is", ["the speed of a planet", "the tilt of a planet", "the size of the Sun"], "0 = circle."),
    ("Why do satellites in low orbit go around Earth faster than the Moon?", "They are closer, where gravity is stronger.", ["They are heavier.", "They have engines on.", "The Moon is lighter."], "Same law for moons and satellites."),
])
B5 = bank([
    ("Astronomers find a planet around another star with a 4-year orbit around a Sun-like star. How far is it?", "about 2.5 AU", ["4 AU", "16 AU", "1 AU"], "a = ∛(16) ≈ 2.5."),
    ("Halley's Comet returns about every 76 years. What does Kepler's third law say about its average distance?", "about 18 AU (∛(76²) ≈ 18)", ["76 AU", "8.7 AU", "1 AU"], "Use T² = a³."),
    ("How did Newton's law of gravitation improve Kepler's laws?", "It explained why the laws work and applies to any orbiting objects.", ["It proved Kepler wrong.", "It only works for Earth.", "It made orbits circles."], "Physical cause."),
    ("Why do mission planners launch probes to Mars about every 26 months?", "Earth and Mars line up for the shortest path at that interval.", ["Mars stops moving then.", "Rockets only work every 26 months.", "Mars is closest to the Sun then."], "Orbital timing."),
    ("A computer model of orbits shows a planet speeding up far from the Sun. What is wrong?", "Planets move slowest when farthest from the Sun.", ["Nothing is wrong.", "Planets move at constant speed.", "Gravity is stronger far away."], "Check against Kepler's second law."),
])


def body():
    think = ("<p><b>Gravity makes planets follow Kepler's three laws.</b></p>"
             "<ul><li>1: Orbits are ellipses with the Sun at one focus. 2: Planets move fastest when closest (equal areas in equal times).</li>"
             "<li>3: T² = a³ (T in years, a in AU). Farther planets have much longer years.</li>"
             "<li>Orbital speed v = 2πr ÷ T.</li></ul>")
    ex = [("a = 4 AU. Period?", ["T² = 64", "T = 8"], "8 years"),
          ("T = 27 years. Distance?", ["a³ = 729", "a = 9"], "9 AU")]
    mist = ["Thinking orbits are perfect circles centered on the Sun.", "Thinking planets move at a constant speed.", "Using T = a instead of T² = a³."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Kepler's laws", B1 + [(g_k2, 8), (g_k3, 4)]),
        ("Equal areas", [(g_k2, 8), (g_k3, 6), (g_speed, 4), (g_table, 2)]),
        ("T² = a³", [(g_k3, 8), (g_table, 12)]),
        ("Planet data", [(g_table, 16), (g_speed, 2), (g_k2, 2)]),
        ("Predicting orbits", B5 + [(g_table, 13), (g_k2, 2)]),
    ])
    make("earth-and-space-science", "keplers-laws-and-orbits", 4, "HS-ESS1-4",
         "Use mathematical or computational representations to predict the motion of orbiting objects in the solar system.",
         "Kepler's Laws and Orbits",
         "Kepler's Laws Worksheets: Ellipses, Equal Areas and T² = a³ (High School Earth Science)",
         "Kepler's Laws",
         "Free high school Earth and space science worksheets on Kepler's laws and orbits (NGSS HS-ESS1-4): ellipses, equal areas, T² = a³, planet data and orbital speed. 100 questions with answers.",
         "T² = a³ for every planet.",
         "Orbits are ellipses; planets speed up near the Sun; farther planets have longer years.",
         body(),
         [("What are Kepler's three laws?", "1: orbits are ellipses with the Sun at one focus. 2: a planet sweeps equal areas in equal times, so it moves faster near the Sun. 3: T² = a³ (years and AU)."),
          ("How do you use T² = a³?", "Cube the distance in AU and take the square root to get the period in years, or square the period and take the cube root to get the distance."),
          ("Why do planets speed up near the Sun?", "The Sun's gravity is stronger there and pulls the planet faster as it falls closer.")],
         sets)


if __name__ == "__main__":
    main()
