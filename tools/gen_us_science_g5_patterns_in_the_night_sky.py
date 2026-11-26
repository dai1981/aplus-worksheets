# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Patterns in the Night Sky (5-ESS1-2)
  python tools/gen_us_science_g5_patterns_in_the_night_sky.py
During one night, stars seem to rise in the east and set in the west because Earth spins (about 15°
each hour). Polaris stays almost still, and the Big Dipper circles it. During a year, Earth orbits the
sun, so the night side faces different directions in space and different constellations are seen
in different seasons (Orion in winter, Scorpius in summer).
Picture: Earth at four places on its orbit with constellations outside; at midnight we look away from the sun.
Wrong answers come from real mistakes: "the stars themselves move across the sky", "we see the
same stars all year", "the constellation behind the sun is seen at night".
"""
import math
from sci_common import Unit, item, bank, lesson, make, fig, figure, table, svg_wrap, circle, text, sun, People, INK, BLUE

U = Unit(50113)
R = U.R
P = People(R)
SEASON = {"Orion": "winter", "Leo": "spring", "Scorpius": "summer", "Pegasus": "fall", "Taurus": "winter", "Virgo": "spring",
          "Cygnus": "summer", "Andromeda": "fall", "Gemini": "winter", "Sagittarius": "summer"}
BEST = {"Orion": "January", "Taurus": "December", "Gemini": "February", "Leo": "April", "Virgo": "May", "Scorpius": "July",
        "Sagittarius": "August", "Cygnus": "August", "Pegasus": "October", "Andromeda": "November"}
ORBIT = [("December", "Orion"), ("March", "Leo"), ("June", "Scorpius"), ("September", "Pegasus")]


def orbit(order=None, label="Earth's orbit with four constellations"):
    """Earth at 4 positions (dark half = night side, facing away from the sun);
    constellation names far outside, in line with Earth (seen at midnight)."""
    W, H = 460, 330
    cx, cy, r = 230, 165, 82
    s = ["<circle cx='%d' cy='%d' r='%d' fill='none' stroke='#999999' stroke-width='1.5' stroke-dasharray='5 5'/>" % (cx, cy, r), sun(cx, cy, 18)]
    pos = order or ORBIT
    for k, (month, con) in enumerate(pos):
        a = math.radians(90 * k - 90)
        ux, uy = math.cos(a), math.sin(a)
        ex, ey = cx + r * ux, cy + r * uy
        s.append(circle(ex, ey, 11, "#8cc0e8", INK, 1.5))
        # night half: the half circle on the side away from the sun
        p1 = (ex - 11 * uy, ey + 11 * ux)
        p2 = (ex + 11 * uy, ey - 11 * ux)
        s.append("<path d='M%.1f %.1f A11 11 0 0 0 %.1f %.1f Z' fill='#33475b'/>" % (p1[0], p1[1], p2[0], p2[1]))
        if k == 0:
            s.append(text(ex + 16, ey - 14, month, 12, "start", weight=400))
        elif k == 2:
            s.append(text(ex + 16, ey + 24, month, 12, "start", weight=400))
        else:
            s.append(text(ex, ey + 30, month, 12, "middle", weight=400))
        if k in (0, 2):
            s.append(text(cx, cy + (r + 52) * uy + 5, con, 14, "middle", col=BLUE))
        else:
            s.append(text(cx + (r + 40) * ux, cy + 5, con, 14, "start" if ux > 0 else "end", col=BLUE))
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-pf='xl' ", 1)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ makers
def rot():
    k0 = R.randrange(4)
    return ORBIT[k0:] + ORBIT[:k0]


def g_orbit():
    order = rot()
    k = R.randrange(4)
    month, con = order[k]
    opp = order[(k + 2) % 4][1]
    w = [c for m, c in order if c != con]
    q = fig(orbit(order)) + "The picture shows Earth's orbit (not to scale). The dark half of Earth is the night side. In %s, which constellation can be seen high in the sky at midnight?" % month
    return item(q, con, w, "At midnight you face away from the sun. In %s that direction points toward %s. %s is behind the sun, so it is hidden in daylight." % (month, con, opp))


def g_orbit_hidden():
    k = R.randrange(4)
    month, con = ORBIT[k]
    opp = ORBIT[(k + 2) % 4][1]
    w = [c for m, c in ORBIT if c != opp]
    return item(fig(orbit(rot())) + "In %s, which constellation cannot be seen at night because it is in the same direction as the sun?" % month, opp, w,
                "In %s the sun is between Earth and %s, so %s is up only in the daytime sky and its stars are hidden by sunlight." % (month, opp, opp))


def g_month():
    k = R.randrange(4)
    month, con = ORBIT[k]
    j = R.choice([1, 2, 3])
    later = ORBIT[(k + j) % 4]
    if R.random() < 0.5:
        return item(fig(orbit(rot())) + "At midnight, %s is high in the sky. In which month is this?" % con, month, [m for m, c in ORBIT if m != month],
                    "In %s, Earth's night side faces toward %s." % (month, con))
    return item(fig(orbit(rot())) + "%s is high in the sky at midnight in %s. Which constellation is high at midnight %d months later?" % (con, month, 3 * j),
                later[1], [c for m, c in ORBIT if c != later[1]], "%d months later it is %s, and the night side faces %s." % (3 * j, later[0], later[1]))


def g_table():
    cs = R.sample(sorted(BEST), 4)
    rows = [[c, BEST[c]] for c in cs]
    t = R.choice(cs)
    season = SEASON[t]
    w = [c for c in cs if SEASON[c] != season]
    if len(w) < 3:
        return None
    return item(table(["Constellation", "Best month to see it in the evening"], rows) + "Which constellation is best seen on %s evenings?" % season,
                t, w[:3],
                "%s is best seen in %s, which is in %s." % (t, BEST[t], season))


def g_degrees():
    h = R.choice([2, 3, 4, 5, 6, 8])
    p = P.next()
    return item("Stars seem to move about 15° across the sky each hour because Earth spins. %s watches a star for %d hours. About how many degrees does it move?" % (p[0], h),
                "%d°" % (15 * h), ["%d°" % (15 + h), "%d°" % (h), "%d°" % (24 * h)], "15° × %d = %d°." % (h, 15 * h))


def g_rot():
    h = R.choice([6, 12, 18])
    return item("Earth turns 360° in 24 hours. How many degrees does it turn in %d hours?" % h, "%d°" % (360 * h // 24),
                ["%d°" % (360 // h), "%d°" % (h * 24), "%d°" % (360 - 15 * h + 15)], "360 ÷ 24 = 15° each hour. 15 × %d = %d°." % (h, 360 * h // 24))


B1 = bank([
    ("Why do stars seem to move across the sky during the night?", "Earth is spinning.", ["The stars are flying across space.", "The moon pushes them.", "Clouds carry them."],
     "As Earth spins toward the east, stars appear to rise in the east and set in the west, just like the sun."),
    ("Which way do most stars seem to move during the night?", "from east to west", ["from west to east", "from south to north", "they do not move"],
     "Like the sun, stars rise in the east and set in the west."),
    ("Which star stays in almost the same place all night, as seen from the United States?", "Polaris, the North Star", ["Sirius", "the sun", "Vega"],
     "Polaris is almost directly above Earth's North Pole, so it barely moves as Earth spins."),
    ("What does the Big Dipper seem to do during the night?", "It circles around Polaris.", ["It stays perfectly still.", "It moves straight up.", "It disappears at midnight."],
     "Stars near Polaris move in circles around it as Earth spins."),
    ("Why do we see different constellations in winter and summer?", "Earth moves around the sun, so at night we face different parts of space.", ["Stars change places every season.", "The sun moves the stars.", "Clouds hide half the stars each season."],
     "In one year Earth travels all the way around the sun, so the night sky changes with the seasons."),
    ("How long does it take Earth to orbit the sun once?", "about 365 days (one year)", ["24 hours", "one month", "one week"],
     "One trip around the sun is one year."),
    ("What is a constellation?", "a group of stars that forms a pattern in the sky", ["a planet with rings", "a single very bright star", "a cloud of dust"],
     "Orion, Leo and the Big Dipper's group (the Great Bear) are patterns of stars."),
    ("Orion is easy to see on winter evenings in the United States. When is it hard to see?", "in summer, because it is up in the daytime sky", ["in winter", "every night all year", "only at midnight in winter"],
     "In summer, Orion is in the same direction as the sun, so sunlight hides it."),
    ("Scorpius is a summer constellation in the United States. In which month would it be best to look for it?", "July", ["January", "December", "March"],
     "Summer months like July are best for Scorpius."),
    ("Why can we see the Big Dipper all year from most of the United States?", "It is close to Polaris, so it circles the pole and never sets.", ["It is the brightest group of stars.", "It moves with Earth.", "It is closer than the moon."],
     "Stars near Polaris stay above the horizon all night, all year."),
])
B5 = bank([
    ("Ava sketches the Big Dipper at 8 p.m. and again at 11 p.m. What will her second sketch show?", "The Big Dipper turned around Polaris.", ["The Big Dipper in exactly the same place.", "A completely different constellation shape.", "No stars at all."],
     "The pattern keeps its shape but turns around Polaris as Earth spins."),
    ("Leo records which constellations he sees at 9 p.m. each month for a year. What pattern will he find?", "The constellations change with the seasons and repeat the next year.", ["He will see the same stars every month.", "New stars appear each month.", "The stars stop moving in winter."],
     "As Earth orbits, the evening sky changes month by month and repeats every year."),
    ("A student says the stars move around Earth every night. Which evidence supports that Earth spins instead?", "Polaris, above Earth's axis, barely moves while other stars circle it.", ["Stars twinkle.", "Stars are different colors.", "Some stars are brighter."],
     "If Earth spins on an axis, stars near the axis should barely move, and that is what we see."),
    ("Which tool would help Mia measure how far a star moves in an hour?", "her fist held at arm's length (about 10°)", ["a thermometer", "a balance", "a ruler laid on the ground"],
     "A fist at arm's length covers about 10° of sky, a handy way to measure angles."),
    ("In a model, Noah walks a globe around a lamp. At each stop, he faces away from the lamp. What does facing away from the lamp show?", "the night sky seen at midnight at that time of year", ["the daytime sky", "the moon's phases", "the sun setting"],
     "Midnight is when you face directly away from the sun."),
    ("Why do astronomers make star charts for each month?", "The stars visible in the evening change during the year.", ["The stars move to new places forever.", "Stars only shine in some months.", "Each month has new stars."],
     "Monthly charts show which part of the sky is up in the evening."),
])


def body():
    think = ("<p><b>In one night:</b> Earth spins once every 24 hours (about 15° each hour), so the stars seem to rise in the east and set in the west. "
             "Polaris, the North Star, stays almost still, and the Big Dipper circles around it.</p>"
             "<p><b>In one year:</b> Earth orbits the sun once every 365 days. At night we look away from the sun, out into a different part of space each season. "
             "So some constellations are seen only part of the year: Orion on winter evenings, Scorpius in summer.</p>"
             + figure(orbit(), "At midnight we face away from the sun. In December that is toward Orion; in June it is toward Scorpius."))
    ex = [("A star moves about 15° each hour. How far does it move in 4 hours?", ["15° × 4"], "60°"),
          ("Why can't we see Orion on a summer night?", ["In summer, Orion is in the same direction as the sun.", "It is up during the day, hidden by sunlight."], "It is in the daytime sky.")]
    mist = ["Thinking the stars themselves move across the sky each night. Earth spins.",
            "Thinking we see the same stars all year. The night sky changes with the seasons.",
            "Mixing up the two motions: spinning (one day) and orbiting (one year)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stars during one night", B1 + [(g_degrees, 5), (g_rot, 5)]),
        ("Earth's orbit and the seasons", [(g_orbit, 8), (g_orbit_hidden, 6), (g_month, 6)]),
        ("Constellation data", [(g_table, 12), (g_degrees, 8)]),
        ("Spin and orbit", [(g_rot, 3), (g_orbit, 5), (g_orbit_hidden, 5), (g_month, 7)]),
        ("Investigations", B5 + [g_table, g_degrees, g_orbit, g_orbit_hidden]),
    ])
    make("grade-5", "patterns-in-the-night-sky", 13, "5-ESS1-2",
         "Represent data in graphical displays to reveal patterns of daily changes in length and direction of shadows, day and night, and the seasonal appearance of some stars in the night sky.",
         "Patterns in the Night Sky",
         "Grade 5 Night Sky Worksheets: Constellations, Seasons, Polaris and Earth's Orbit",
         "Night Sky",
         "Free Grade 5 science worksheets on patterns in the night sky (NGSS 5-ESS1-2): stars rising and setting, Polaris and the Big Dipper, and seasonal constellations caused by Earth's orbit. 100 practice questions with answers.",
         "Earth's spin moves the stars each night; its orbit changes them each season.",
         "Stars rise in the east and set in the west about 15° an hour. Different constellations are seen in different seasons because Earth orbits the sun.",
         body(),
         [("Why do stars move across the sky at night?", "They do not really move. Earth spins, so stars seem to rise in the east and set in the west, like the sun."),
          ("Why do we see different stars in different seasons?", "Earth orbits the sun once a year. At night we face away from the sun, toward a different part of space each season."),
          ("Why does Polaris stay in the same place?", "Polaris is almost straight above Earth's North Pole, along Earth's axis, so it barely moves as Earth spins."),
          ("When can you see Orion?", "From the United States, Orion is easiest to see on winter evenings. In summer it is in the daytime sky.")],
         sets)


if __name__ == "__main__":
    main()
