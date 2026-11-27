# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 6, AC9S6U02: the solar system - the Sun, the eight planets, their order, kinds,
distances and orbits, and models of the solar system.
  python tools/gen_au_science_y6_the_solar_system.py
Reuses the UK Year 5 solar system makers (order, kind of planet, distances, years) with Australian names, plus own
questions on scale models and Australian astronomy (the Parkes radio telescope, First Nations star knowledge).
Wrong answers come from real mistakes: thinking the Sun orbits the Earth, that the Moon is a planet, that planets give off
their own light, and that the planets are evenly spaced.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 6, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

SS = "gen_uk_science_y5_the_solar_system"
uk_order = src(SS, "g_order")
uk_type = src(SS, "g_type")
uk_fact = src(SS, "g_fact", rep=[(r"Which planet is the planet that ", "Which planet "), (r"Which planet is the planet with ", "Which planet has ")])
uk_year = limit(src(SS, "g_year"), 6)
uk_dist = limit(src(SS, "g_dist"), 5)
uk_b1 = src.B(SS, "B1")
uk_b5 = src.B(SS, "B5")

PL = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
AU_DIST = {"Mercury": 0.4, "Venus": 0.7, "Earth": 1, "Mars": 1.5, "Jupiter": 5.2, "Saturn": 9.5, "Uranus": 19, "Neptune": 30}


def g_scale():
    p = R.choice([x for x in PL if x != "Earth"])
    d = AU_DIST[p]
    cm = d * 10
    a = ("%g" % cm) + " cm" if cm < 100 else ("%g m" % (cm / 100))
    w = set()
    for f in (2, 0.5, 10):
        v = cm * f
        w.add(("%g cm" % v) if v < 100 else ("%g m" % (v / 100)))
    w.discard(a)
    return tq("In a scale model, Earth is 10 cm from the Sun. %s is %g times as far from the Sun as Earth. How far from the Sun should %s go?" % (p, d, p),
              a, sorted(w)[:3], "%g × 10 cm = %g cm." % (d, cm))


DATA = {"Mercury": (4900, 58, "rocky"), "Venus": (12100, 108, "rocky"), "Earth": (12700, 150, "rocky"), "Mars": (6800, 228, "rocky"),
        "Jupiter": (143000, 778, "gas giant"), "Saturn": (120500, 1430, "gas giant"), "Uranus": (51100, 2870, "ice giant"), "Neptune": (49500, 4500, "ice giant")}


def g_cmp():
    a, b = R.sample(PL, 2)
    k = R.choice(["wider", "narrower", "closer to the Sun", "further from the Sun"])
    i = 0 if k in ("wider", "narrower") else 1
    big = DATA[a][i] > DATA[b][i]
    ans = a if (big and k in ("wider", "further from the Sun")) or (not big and k in ("narrower", "closer to the Sun")) else b
    other = b if ans == a else a
    return tq("Which planet is %s: %s or %s?" % (k, a, b), ans, [other, "They are exactly the same.", "the Moon"],
              "%s: about %s km wide, %s million km from the Sun. %s: about %s km wide, %s million km from the Sun." %
              (a, DATA[a][0], DATA[a][1], b, DATA[b][0], DATA[b][1]))


def g_tab():
    ps = R.sample(PL, 4)
    tab = "<table class='sn-table'><tr><th>Planet</th><th>Width (km)</th><th>Distance from the Sun (million km)</th></tr>%s</table>" % "".join(
        "<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % (p, DATA[p][0], DATA[p][1]) for p in ps)
    k = R.choice(["widest", "narrowest", "closest", "furthest"])
    i = 0 if k in ("widest", "narrowest") else 1
    f = max if k in ("widest", "furthest") else min
    ans = f(ps, key=lambda p: DATA[p][i])
    from au_sci import once
    if not once(("tab", tuple(sorted(ps)), k)):
        return None
    return tq("%sWhich planet in the table is the %s%s?" % (tab, k, "" if i == 0 else " from the Sun" if k == "furthest" else " to the Sun"), ans,
              [p for p in ps if p != ans], "Compare the numbers in the %s column." % ("width" if i == 0 else "distance"))


POOL1 = pool(R, [
    ("What is at the centre of our solar system?", "the Sun", ["the Earth", "the Moon", "Jupiter"], "All eight planets orbit the Sun."),
    ("Which planet is closest to the Sun?", "Mercury", ["Venus", "Earth", "Neptune"], "Mercury is the first planet."),
    ("Which planet is the largest?", "Jupiter", ["Saturn", "Earth", "Neptune"], "Jupiter is a gas giant more than 11 times as wide as Earth."),
    ("Why can we see planets such as Venus in the night sky?", "They reflect light from the Sun.", ["They make their own light.", "They are on fire.", "They are stars."], "Only stars, such as the Sun, give off their own light."),
    ("Which planet is known for its blue colour and the fastest winds?", "Neptune", ["Mercury", "Mars", "Earth"], "Neptune's winds are the fastest in the solar system."),
    ("Which planet has the most moons found so far?", "Saturn", ["Mercury", "Venus", "Earth"], "Saturn and Jupiter each have dozens of moons; Mercury and Venus have none."),
    ("What is the Sun?", "a star", ["a planet", "a moon", "a comet"], "It is the closest star to Earth."),
    ("What keeps the planets in their orbits around the Sun?", "the pull of the Sun's gravity", ["wind in space", "magnets", "the Moon"], "Gravity pulls the planets towards the Sun as they move."),
    ("Which planets are rocky?", "Mercury, Venus, Earth and Mars", ["Jupiter, Saturn, Uranus and Neptune", "only Earth", "all eight"], "The four inner planets are rocky."),
    ("What is found between Mars and Jupiter?", "the asteroid belt", ["the Sun", "the Moon", "Saturn's rings"], "Millions of rocky asteroids orbit there."),
    ("Which planet takes the longest to orbit the Sun?", "Neptune", ["Mercury", "Earth", "Jupiter"], "It is furthest from the Sun, about 165 Earth years."),
    ("How long does Earth take to orbit the Sun once?", "about 365 days", ["24 hours", "about 30 days", "about 10 years"], "This is one year."),
])
POOL5 = pool(R, [
    ("Mia makes a model with planets placed evenly 10 cm apart. What is wrong with her model?", "The real gaps between planets get much bigger further from the Sun.", ["Nothing is wrong.", "The planets should touch.", "The Sun should be at the end."], "The outer planets are very far apart."),
    ("Why do scientists use models of the solar system?", "It is too big to see all at once, so models help explain it.", ["Models are more accurate than real data.", "Space is not real.", "Models change the orbits."], "Models can show size or distance, but rarely both."),
    ("In a model, the Sun is a 1 m wide ball. Earth would be about the size of a pea. What does this show?", "The Sun is much bigger than Earth.", ["Earth is bigger than the Sun.", "They are the same size.", "Peas are planets."], "About 109 Earths fit across the Sun."),
    ("The Parkes radio telescope in New South Wales helped receive pictures from which event in 1969?", "the first Moon landing", ["the first car race", "the first flight to Mars", "the discovery of Jupiter"], "Australia's telescopes still track spacecraft."),
    ("For thousands of years, First Nations Australians have used the stars to know when to hunt and gather foods. What does this show?", "Observing patterns in the sky is a kind of science.", ["Stars change every night at random.", "Stars cannot be used for anything.", "Only telescopes can study the sky."], "Long-term observation of patterns is science."),
    ("Jack reads that Mars has a year of about 687 days. How does this compare with Earth's year?", "It is almost twice as long.", ["It is shorter.", "It is the same.", "It is ten times as long."], "687 ÷ 365 is close to 2."),
    ("Which planet would make the best model for a 'hot' planet with thick clouds?", "Venus", ["Neptune", "Uranus", "Mars"], "Venus is the hottest planet because its thick atmosphere traps heat."),
    ("Ruby says, 'The Sun goes around the Earth because it moves across the sky.' What is the scientific explanation?", "Earth spins on its axis, so the Sun only seems to move.", ["The Sun really goes around the Earth.", "The Moon pushes the Sun.", "The sky moves."], "The Earth rotates once each day."),
])


def main():
    sets = U.sets([
        ("The Sun and the planets", [(POOL1, 7), (uk_order, 6), (uk_type, 4), (uk_b1, 3)]),
        ("Planet facts", [(uk_fact, 8), (uk_type, 3), (POOL1, 3), (g_cmp, 6)]),
        ("Orbits and years", [(uk_year, 6), (uk_order, 6), (uk_b1, 4), (g_cmp, 4)]),
        ("Distances and scale", [(uk_dist, 5), (g_scale, 5), (g_tab, 6), (uk_order, 4)]),
        ("Models and explanations", [(POOL5, 8), (uk_b5, 5), (g_tab, 3), (POOL1, 2), (uk_fact, 2)]),
    ])
    make_au(YEAR, "the-solar-system", SORT, "AC9S6U02", "Earth and space sciences",
            "Describe the movement of Earth and other planets relative to the Sun and model how Earth's tilt, rotation on its axis and "
            "revolution around the Sun cause cycles of day and night and seasons (summary of the Australian Curriculum v9.0 Science content description).",
            "The Solar System", "The solar system",
            "Free Year 6 science worksheets on the solar system: the Sun, the eight planets in order, rocky planets and gas giants, orbits, "
            "distances and scale models. 100 questions with answers.",
            "Eight planets orbit the Sun.", "Rocky planets are close to the Sun; the gas and ice giants are far away.",
            "<p><b>The solar system is the Sun and everything that orbits it.</b></p><ul>"
            "<li>The eight planets in order: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.</li>"
            "<li>The four inner planets are small and rocky; the four outer planets are giants made mostly of gas and ice.</li>"
            "<li>The further a planet is from the Sun, the longer it takes to orbit, and the gaps between planets get much bigger.</li></ul>",
            [("Which planet is fourth from the Sun?", ["Mercury, Venus, Earth, Mars"], "Mars"),
             ("Earth is 10 cm from the Sun in a model. Jupiter is 5.2 times as far. Where does it go?", ["5.2 × 10 cm"], "52 cm")],
            ["Thinking the Sun orbits the Earth.", "Calling the Moon a planet.", "Spacing the planets evenly in a model."],
            [("What are the eight planets in order?", "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. A memory sentence: My Very Excellent Mother Just Served Us Noodles."),
             ("Why is Pluto not a planet?", "Pluto is a dwarf planet. It is very small and shares its orbit with many other icy objects."),
             ("Why do planets shine if they are not stars?", "Planets reflect light from the Sun. Only stars, like the Sun, make their own light.")],
            sets)


if __name__ == "__main__":
    main()
