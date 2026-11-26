# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Gravity in the Solar System (MS-ESS1-2)
  python tools/gen_us_science_g8_gravity_in_the_solar_system.py
Develop and use a model to describe the role of gravity in the motions within galaxies and the solar system.
Orbits as a balance of forward motion and gravity's pull; planets farther from the Sun move slower and take longer;
the Sun holds the solar system, the Milky Way's gravity holds stars; the solar system formed from a collapsing cloud.
Wrong answers come from real mistakes: "planets orbit because nothing pulls on them", "without gravity a planet would
fall into the Sun", "outer planets move faster", "the Sun orbits Earth".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(80119)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# distance from the Sun (AU), orbital period (Earth years), average orbital speed (km/s)
PL = [("Mercury", 0.39, 0.24, 47.9), ("Venus", 0.72, 0.62, 35.0), ("Earth", 1.0, 1.0, 29.8), ("Mars", 1.52, 1.88, 24.1),
      ("Jupiter", 5.2, 11.9, 13.1), ("Saturn", 9.5, 29.5, 9.7), ("Uranus", 19.2, 84.0, 6.8), ("Neptune", 30.1, 164.8, 5.4)]


def g_pl():
    who = P.next()[0]
    rows = sorted(R.sample(PL, 4), key=lambda r: r[1])
    k = R.choice(["fast", "slow", "long", "pattern", "predict"])
    if not once((tuple(r[0] for r in rows), k)):
        return None
    tab = table(["Planet", "Distance from the Sun (AU)", "Time for one orbit (Earth years)", "Average orbital speed (km/s)"],
                [[n, "%g" % d, "%g" % t, "%g" % v] for n, d, t, v in rows])
    names = [r[0] for r in rows]
    if k == "fast":
        return item(tab + "Which planet in %s's table moves fastest in its orbit?" % who, names[0], names[1:], "The planet closest to the Sun is pulled hardest by gravity and moves fastest.")
    if k == "slow":
        return item(tab + "Which planet in %s's table moves slowest in its orbit?" % who, names[-1], names[:-1], "Farther planets feel a weaker pull and move slower.")
    if k == "long":
        return item(tab + "Which planet in %s's table takes the longest to orbit the Sun?" % who, names[-1], names[:-1], "Farther planets travel a longer path, more slowly.")
    if k == "pattern":
        return item(tab + "What pattern does %s's table show?" % who, "Planets farther from the Sun move more slowly and take longer to orbit.",
                    ["Planets farther from the Sun move faster.", "All planets take one year to orbit.", "Distance has no effect on orbits."], "Gravity weakens with distance.")
    return item(tab + "A dwarf planet orbits farther out than every planet in %s's table. What can you predict?" % who, "It takes longer to orbit than any of them.",
                ["It orbits faster than any of them.", "It does not orbit the Sun.", "It takes exactly one year."], "Follow the pattern: farther → slower, longer orbit.")


SCN = [("If the Sun's gravity suddenly disappeared, what would Earth do?", "move off in a straight line into space", ["fall into the Sun", "stop moving", "orbit faster"],
        "Without gravity's pull, nothing would curve Earth's path (Newton's first law)."),
       ("If a planet stopped moving forward, what would the Sun's gravity do?", "pull it straight toward the Sun", ["keep it in the same orbit", "push it away", "nothing"],
        "An orbit needs both forward motion and gravity."),
       ("What keeps the Moon in orbit around Earth?", "Earth's gravity pulling on the moving Moon", ["the Moon's magnetism", "air pressure", "the Sun pushing it"], "Gravity bends the Moon's path into a curve."),
       ("What holds the stars of the Milky Way together?", "gravity, mostly from the galaxy's huge mass", ["magnetic fields only", "nothing; they are fixed", "light pressure"], "Galaxies are held together by gravity."),
       ("What does the Sun orbit?", "the center of the Milky Way galaxy", ["Earth", "Jupiter", "nothing; it stays still"], "One trip takes about 230 million years."),
       ("Why is the Sun at the center of our solar system's orbits?", "It has more than 99% of the solar system's mass, so its gravity dominates.", ["It is the hottest.", "It is the brightest.", "It was placed there by Jupiter."],
        "Mass determines gravity."),
       ("Why are planets round?", "Gravity pulls their material toward the center from all sides.", ["They spin like tops.", "Wind smooths them.", "Comets carve them."], "Large bodies become round."),
       ("Why does a comet speed up as it gets close to the Sun?", "The Sun's gravity pulls harder when the comet is closer.", ["The comet's engine turns on.", "Sunlight pushes it forward.", "The comet loses mass."],
        "Closer → stronger pull → faster."),
       ("How did gravity help form the solar system?", "It pulled a spinning cloud of gas and dust together into the Sun and planets.", ["It pushed the planets out of the Sun.", "It had no role.", "It formed only the Moon."],
        "The nebula collapsed under gravity."),
       ("Why do moons orbit planets instead of flying off?", "The planet's gravity pulls on the moving moon.", ["Moons are glued in place.", "Moons have no motion.", "The Sun pushes them back."], "Same idea at a smaller scale.")]


def g_scn():
    q, a, w, e = R.choice(SCN)
    who = P.next()[0]
    if not once(("s", q)):
        return None
    return item("%s asks: “%s”" % (who, q), a, w, e)


def g_scale():
    who = P.next()[0]
    k = R.choice(["mass", "dist"])
    if k == "mass":
        f = R.choice([2, 3, 4])
        if not once(("m", f)):
            return None
        return item("In %s's model, a star has %d times the mass of the Sun. A planet orbits it at the same distance as Earth. How does the pull on the planet compare with the Sun's pull on Earth (if the planets have equal mass)?" % (who, f),
                    "%d times stronger" % f, ["%d times weaker" % f, "the same", "%d times stronger" % (f * f)], "Gravity is proportional to mass.")
    f = R.choice([2, 3, 4])
    if not once(("d", f)):
        return None
    return item("In %s's model, a planet moves to %d times its distance from the Sun. What happens to the Sun's pull on it?" % (who, f), "It becomes %d times weaker." % (f * f),
                ["It becomes %d times weaker." % f, "It becomes %d times stronger." % f, "It stays the same."], "Gravity weakens with the square of distance: %d² = %d." % (f, f * f))


B1 = bank([
    ("What two things make an orbit?", "forward motion and gravity pulling toward the center", ["only forward motion", "only gravity", "magnetism and wind"], "Gravity curves the path."),
    ("Which object has the strongest gravity in our solar system?", "the Sun", ["Jupiter", "Earth", "the Moon"], "It has the most mass."),
    ("What is a galaxy?", "a huge system of stars, gas and dust held together by gravity", ["a single star", "a planet's moon", "a cloud on Earth"], "The Milky Way has hundreds of billions of stars."),
    ("Which planet takes the shortest time to orbit the Sun?", "Mercury", ["Neptune", "Earth", "Jupiter"], "It is closest: about 88 days."),
    ("Why do outer planets take longer to orbit the Sun?", "They travel a longer path and move more slowly because the Sun's pull is weaker.", ["They are heavier.", "They spin faster.", "They have more moons."], "Distance matters."),
    ("What is 1 astronomical unit (AU)?", "the average distance from Earth to the Sun, about 150 million km", ["the distance to the Moon", "one light-year", "the width of Earth"], "Used for solar system distances."),
    ("Does Earth's gravity reach the Moon?", "Yes. It keeps the Moon in orbit.", ["No, it stops at the atmosphere.", "Only at night.", "Only during eclipses."], "Gravity reaches far into space."),
    ("What shape are most planetary orbits?", "nearly circular ellipses", ["squares", "straight lines", "spirals into the Sun"], "Slightly stretched circles."),
])
B5 = bank([
    ("Ava swings a ball on a string in a circle. In her model, what does the string represent?", "the Sun's gravity pulling the planet inward", ["the planet's speed", "sunlight", "the planet's mass"], "Gravity is the inward pull."),
    ("Leo lets go of the string while the ball is swinging. What does the ball do, and what does it model?", "It flies off in a straight line, like a planet without gravity.", ["It falls straight down to the center.", "It keeps circling.", "It stops."],
     "No inward pull, no curve."),
    ("Mia's model shows a cloud of gas and dust shrinking and spinning faster. What forms at the center?", "a star like the Sun", ["a planet", "a moon", "a comet"], "Most mass collects at the center."),
    ("Why would a spacecraft need more speed to orbit close to Jupiter than close to the Moon?", "Jupiter's much larger mass pulls harder.", ["Jupiter is colder.", "The Moon has no gravity.", "Jupiter is closer to the Sun."], "More mass, more speed needed."),
    ("Which model best describes the solar system?", "planets orbiting the Sun, held by the Sun's gravity", ["the Sun orbiting Earth", "planets fixed in place", "planets orbiting Jupiter"], "Sun-centered model."),
])


def body():
    think = ("<p><b>Gravity</b> controls motion in space. An <b>orbit</b> happens when an object moving forward is pulled toward a larger mass: the pull bends its path into a curve.</p>"
             "<ul><li>The <b>Sun</b> has more than 99% of the solar system's mass, so the planets orbit it.</li>"
             "<li>Planets <b>closer</b> to the Sun feel a stronger pull, move <b>faster</b> and have <b>shorter</b> years. Farther planets are slower with longer years.</li>"
             "<li>Gravity formed the solar system from a collapsing cloud and holds the <b>Milky Way</b> together; the Sun orbits the galaxy's center.</li></ul>")
    ex = [("Without the Sun's gravity, how would Earth move?", ["No force to curve its path."], "in a straight line"),
          ("Neptune or Mars: which moves faster?", ["Closer → faster."], "Mars")]
    mist = ["Thinking a planet would fall into the Sun without gravity. It would fly off straight.",
            "Thinking outer planets move faster.",
            "Thinking nothing pulls on orbiting planets."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Gravity and orbits", B1 + [(g_scn, 6), (g_pl, 6)]),
        ("Planet data", [(g_pl, 16), (g_scn, 4)]),
        ("Patterns in orbits", [(g_pl, 14), (g_scale, 6)]),
        ("Gravity on every scale", [(g_pl, 20)]),
        ("Using models", B5 + [(g_pl, 15)]),
    ])
    make("grade-8", "gravity-in-the-solar-system", 19, "MS-ESS1-2",
         "Develop and use a model to describe the role of gravity in the motions within galaxies and the solar system.",
         "Gravity in the Solar System",
         "Grade 8 Gravity in the Solar System Worksheets: Orbits, Planets and Galaxies",
         "Gravity in the Solar System",
         "Free middle school science worksheets on gravity in the solar system (NGSS MS-ESS1-2): how gravity makes orbits, planet distance and orbital speed data, and gravity's role in forming the solar system and holding galaxies together. 100 practice questions with answers.",
         "Gravity keeps planets and stars in orbit.",
         "Forward motion plus gravity's pull makes an orbit. Closer planets move faster; gravity also holds galaxies together.",
         body(),
         [("Why do planets orbit the Sun?", "Each planet is moving forward, and the Sun's gravity pulls it inward. Together they bend its path into an orbit."),
          ("Why do planets farther from the Sun take longer to orbit?", "They travel a longer path and the Sun's weaker pull at that distance means they move more slowly."),
          ("What role does gravity play in galaxies?", "Gravity holds the stars, gas and dust of a galaxy together, and stars like the Sun orbit the galaxy's center.")],
         sets)


if __name__ == "__main__":
    main()
