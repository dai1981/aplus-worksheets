# -*- coding: utf-8 -*-
"""
UK Year 5 science: The Solar System (Earth and space)
  python tools/gen_uk_science_y5_the_solar_system.py
The Sun at the centre, the eight planets in order, what makes each planet special, how long each takes to orbit the
Sun, distances from the Sun, the Sun, Earth and Moon as approximately spherical bodies, and the ideas of Ptolemy,
Copernicus and Galileo.
Wrong answers come from real mistakes: "the Sun moves round the Earth", "Pluto is the ninth planet", "the Moon is a
planet", "planets further out take less time to orbit".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61508)
R = U.R
P = People(R)

PL = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
ORD = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
YEAR = {"Mercury": "88 days", "Venus": "225 days", "Earth": "365 days", "Mars": "687 days", "Jupiter": "12 years", "Saturn": "29 years", "Uranus": "84 years", "Neptune": "165 years"}
DAYS = {"Mercury": 88, "Venus": 225, "Earth": 365, "Mars": 687, "Jupiter": 4333, "Saturn": 10759, "Uranus": 30687, "Neptune": 60190}
DIST = {"Mercury": 58, "Venus": 108, "Earth": 150, "Mars": 228, "Jupiter": 778, "Saturn": 1434, "Uranus": 2871, "Neptune": 4495}
FACT = [("the largest", "Jupiter"), ("the smallest", "Mercury"), ("the hottest planet, because its thick clouds trap heat", "Venus"),
        ("the red planet, with rusty dust", "Mars"), ("famous for its bright, wide rings", "Saturn"), ("the planet that spins on its side", "Uranus"),
        ("furthest from the Sun", "Neptune"), ("the only planet known to have life", "Earth"), ("closest to the Sun", "Mercury"),
        ("the planet with the Great Red Spot, a giant storm", "Jupiter")]


def g_order():
    i = R.randrange(8)
    k = R.choice(["pos", "after", "before"])
    if (k == "after" and i == 7) or (k == "before" and i == 0) or not once(("or", i, k)):
        return None
    if k == "pos":
        return item("Which planet is %s from the Sun?" % ORD[i], PL[i], R.sample([p for p in PL if p != PL[i]], 3), "My Very Easy Method Just Speeds Up Naming: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.")
    j = i + 1 if k == "after" else i - 1
    return item("Which planet is %s %s, %s the Sun?" % ("next out from" if k == "after" else "next in from", PL[i], "further from" if k == "after" else "closer to"), PL[j],
                R.sample([p for p in PL if p not in (PL[i], PL[j])], 3), "Order from the Sun: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.")


def g_fact():
    f, p = R.choice(FACT)
    if not once(("fa", f)):
        return None
    return item("Which planet is %s?" % f, p, R.sample([x for x in PL if x != p], 3), "%s is %s." % (p, f))


def g_year():
    a, b = R.sample(PL, 2)
    k = R.choice(["read", "cmp", "more"])
    if not once(("yr", tuple(sorted((a, b))) if k != "read" else a, k)):
        return None
    tab = table(["Planet", "Time to orbit the Sun once"], [[p, YEAR[p]] for p in PL])
    if k == "read":
        return item(tab + "How long does %s take to orbit the Sun once?" % a, YEAR[a], R.sample([YEAR[x] for x in PL if x != a], 3), "Read the row for %s." % a)
    if k == "cmp":
        lo = a if DAYS[a] > DAYS[b] else b
        return item(tab + "Which takes longer to orbit the Sun: %s or %s?" % (a, b), lo, [b if lo == a else a, "They take the same time.", "Neither orbits the Sun."],
                    "Planets further from the Sun take longer to orbit.")
    if DAYS[a] > 700 or DAYS[b] > 700:
        return None
    hi, lo = (a, b) if DAYS[a] > DAYS[b] else (b, a)
    d = DAYS[hi] - DAYS[lo]
    g = "%s days" % format(d, ",")
    return item(tab + "How many more days does %s take to orbit the Sun than %s?" % (hi, lo), g,
                uniq(g, ["%s days" % format(DAYS[hi] + DAYS[lo], ","), "%d days" % DAYS[hi], "%d days" % (d + 10), "%d days" % DAYS[lo]]), "%d − %d = %d days." % (DAYS[hi], DAYS[lo], d))


def g_dist():
    a, b = R.sample(PL[:6], 2)
    k = R.choice(["diff", "closer"])
    if not once(("ds", tuple(sorted((a, b))), k)):
        return None
    tab = table(["Planet", "Average distance from the Sun (million km)"], [[p, format(DIST[p], ",")] for p in PL[:6]])
    if k == "closer":
        c = a if DIST[a] < DIST[b] else b
        return item(tab + "Which is closer to the Sun: %s or %s?" % (a, b), c, [b if c == a else a, "They are the same distance.", "It changes every day, so you cannot say."], "Smaller distance = closer.")
    hi, lo = (a, b) if DIST[a] > DIST[b] else (b, a)
    d = DIST[hi] - DIST[lo]
    g = "%s million km" % format(d, ",")
    return item(tab + "How much further from the Sun is %s than %s?" % (hi, lo), g,
                uniq(g, ["%s million km" % format(DIST[hi] + DIST[lo], ","), "%s million km" % format(DIST[hi], ","), "%s million km" % format(d + 100, ","), "%s million km" % format(DIST[lo], ",")]),
                "%s − %s = %s million km." % (format(DIST[hi], ","), format(DIST[lo], ","), format(d, ",")))


GROUP = [("Mercury", "rocky planet"), ("Venus", "rocky planet"), ("Earth", "rocky planet"), ("Mars", "rocky planet"),
         ("Jupiter", "gas giant"), ("Saturn", "gas giant"), ("Uranus", "ice giant"), ("Neptune", "ice giant")]


def g_type():
    p, t = R.choice(GROUP)
    if not once(("ty", p)):
        return None
    A = lambda x: ("an " if x[0] in "aeiou" else "a ") + x
    return item("What kind of planet is %s?" % p, A(t), [A(x) for x in ("rocky planet", "gas giant", "ice giant") if x != t] + ["a star"],
                "Mercury to Mars are rocky; Jupiter and Saturn are gas giants; Uranus and Neptune are ice giants.")


B1 = bank([
    ("What is at the centre of our solar system?", "the Sun", ["the Earth", "the Moon", "Jupiter"], "All the planets orbit the Sun."),
    ("How many planets are in our solar system?", "eight", ["nine", "seven", "twelve"], "Pluto is now called a dwarf planet."),
    ("What is the Sun?", "a star", ["a planet", "a moon", "a comet"], "It makes its own light."),
    ("What does orbit mean?", "to travel round another object in space", ["to spin on the spot", "to fall to Earth", "to shine brightly"], "Earth orbits the Sun."),
    ("How long does the Earth take to orbit the Sun?", "about 365 days (one year)", ["one day", "one month", "one week"], "That is why a year is 365 days."),
    ("What shape are the Sun, Earth and Moon?", "roughly spheres (ball-shaped)", ["flat discs", "cubes", "cones"], "Gravity pulls them into balls."),
    ("Is the Moon a planet?", "No. It is a natural satellite that orbits the Earth.", ["Yes, the ninth planet.", "Yes, the closest planet.", "No, it is a star."], "Moons orbit planets."),
    ("Why is Pluto no longer called a planet?", "It is a dwarf planet that shares its orbit with many other icy objects.", ["It exploded.", "It is too hot.", "It is part of the Moon."], "Reclassified in 2006."),
])
B5 = bank([
    ("Long ago, people such as Ptolemy thought what about the Earth?", "that it was at the centre and everything orbited it", ["that it orbited the Sun", "that it was flat and still", "that it was a star"], "A geocentric model."),
    ("Which scientist suggested in 1543 that the planets orbit the Sun?", "Nicolaus Copernicus", ["Isaac Newton", "Charles Darwin", "Mary Anning"], "A heliocentric model."),
    ("What did Galileo see through his telescope that supported the Sun-centred model?", "moons orbiting Jupiter and the phases of Venus", ["rings round the Moon", "the Earth from space", "Pluto"], "Not everything orbits Earth."),
    ("What evidence shows the Earth is round?", "photos from space and the curved shadow of Earth on the Moon in an eclipse", ["the ground looks flat", "the Sun is round", "the sea is blue"], "Several kinds of evidence."),
    ("Why does Neptune take much longer than Earth to orbit the Sun?", "It is much further away, so its orbit is much longer and it moves more slowly.", ["It is smaller.", "It is closer to the Sun.", "It spins faster."], "Distance matters."),
])


def body():
    think = ("<p><b>The Sun is a star at the centre of our solar system; eight planets orbit it.</b></p>"
             "<ul><li>In order: Mercury, Venus, Earth, Mars (rocky), Jupiter, Saturn (gas giants), Uranus, Neptune (ice giants).</li>"
             "<li>Planets further from the Sun take longer to orbit: Earth takes 365 days, Neptune 165 years.</li>"
             "<li>The Sun, Earth and Moon are roughly spheres. The Moon orbits the Earth.</li></ul>")
    ex = [("Which planet is 4th from the Sun?", ["Mercury, Venus, Earth, Mars"], "Mars"),
          ("Mars 687 days, Earth 365 days. Difference?", ["687 − 365"], "322 days")]
    mist = ["Thinking the Sun moves round the Earth.", "Calling Pluto or the Moon a planet.", "Thinking planets further out orbit faster."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Our solar system", B1 + [(g_order, 8), (g_type, 4)]),
        ("The planets", [(g_order, 10), (g_fact, 10)]),
        ("Orbit times", [(g_year, 16), (g_type, 4)]),
        ("Distances", [(g_dist, 16), (g_order, 4)]),
        ("Ideas about space", B5 + [(g_year, 8), (g_dist, 7)]),
    ])
    make_uk(5, "the-solar-system", 8, "Earth and space",
            "Describe the movement of the Earth, and other planets, relative to the Sun in the solar system. Describe the Sun, Earth and Moon as approximately spherical bodies.",
            "The Solar System",
            "Year 5 Science: The Solar System Worksheets (Planets, Orbits and Distances)",
            "The Solar System",
            "Free Year 5 science worksheets on the solar system: the Sun and the eight planets in order, planet facts, orbit times, distances from the Sun and how ideas about space changed. 100 questions with answers.",
            "Eight planets orbit the Sun.",
            "The further a planet is from the Sun, the longer its year.",
            body(),
            [("What are the planets in order?", "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. A rhyme such as 'My Very Easy Method Just Speeds Up Naming' helps."),
             ("Why do outer planets have longer years?", "They are further from the Sun, so they have a much longer path to travel and move more slowly in their orbit."),
             ("Is Pluto a planet?", "Not any more. Since 2006 Pluto has been classed as a dwarf planet.")],
            sets)


if __name__ == "__main__":
    main()
